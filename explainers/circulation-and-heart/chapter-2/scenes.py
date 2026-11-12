"""Harvey's Arithmetic: circulation-and-heart film 2 (chapter 2).

COLOUR MAP (same as film 1): BLUE oxygen-poor blood; RED oxygen-rich blood; GOLD ventricle (cup / lift);
GREEN heart rate; RED also stroke volume (the scoop); GREY vessels. Everything is a schematic cartoon.
Tank, clock and counters are computed from the lesson's own numbers: 70 mL (a deliberately low guess)
x 75 beats a minute x 30 minutes, against 5 L of blood in the body; then half the scoop, 35 mL.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

B, R = BLUE, RED
PERIOD = 12.0


def smooth(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


def pulse(t, T=0.9):
    return float(np.exp(-(((t / T) % 1 - 0.2) / 0.12) ** 2))


def start_clock(sc):
    sc.tr = ValueTracker(0)
    sc.tr.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(sc.tr)
    return sc.tr


class Track:
    def __init__(self, f, P, stops, hide=1.01, k=1.0, o=(0, 0), c=(0, 0)):
        self.f = np.array(f, float)
        self.P = np.array(P, float)
        self.stops, self.hide, self.k = stops, hide, k
        self.o, self.c = np.array(o, float)[:2], np.array(c, float)[:2]
        self.reach = 1.0
        self.lifts, self.chans, self.floor = [], [], None

    def T(self, p):
        q = self.o + self.k * (np.asarray(p, float)[:2] - self.c)
        return np.array([q[0], q[1], 0.0])

    def pos(self, u):
        return self.T([np.interp(u, self.f, self.P[:, 0]), np.interp(u, self.f, self.P[:, 1])])

    def col(self, u):
        s = self.stops
        for (a, ca), (b, cb) in zip(s[:-1], s[1:]):
            if u <= b:
                t = 0 if b == a else (u - a) / (b - a)
                return interpolate_color(ManimColor(ca), ManimColor(cb), float(np.clip(t, 0, 1)))
        return ManimColor(s[-1][1])

    def op(self, u):
        o = min(1.0, u / 0.03)
        if u > self.hide:
            o *= max(0.0, 1 - (u - self.hide) / 0.02)
        return o * float(np.clip((self.reach - u) / 0.02, 0, 1))

    # ---- mobs
    def floor_mob(self):
        x0, x1, y = self.floor
        a, b = self.T((x0, y)), self.T((x1, y - 1.05))
        band = Rectangle(width=b[0] - a[0], height=a[1] - b[1], stroke_width=0, fill_color=GREY, fill_opacity=0.2)
        band.move_to([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0])
        ln = Line(a, self.T((x1, y)), color=GREY, stroke_width=4, stroke_opacity=0.8)
        return VGroup(band, ln)

    def chan_mob(self, i):
        p0, p1, w0, w1 = self.chans[i]
        pts = [self.T((p0[0], p0[1] + w0 / 2)), self.T((p1[0], p1[1] + w1 / 2)),
               self.T((p1[0], p1[1] - w1 / 2)), self.T((p0[0], p0[1] - w0 / 2))]
        return Polygon(*pts, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.7)

    def lift_mob(self, i, tr):
        xc, yb, yt = self.lifts[i]
        h = 0.5
        shaft = Polygon(self.T((xc - h, yb)), self.T((xc + h, yb)), self.T((xc + h, yt)), self.T((xc - h, yt)),
                        color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.42)
        plat = Line(self.T((xc - h, yt)), self.T((xc + h, yt)), color=GOLD, stroke_width=9)
        cab = Rectangle(width=0.8 * self.k, height=0.16 * self.k, stroke_width=0, fill_color=GOLD, fill_opacity=0.95)
        per = 1.6

        def upd(m):
            y = yb + 0.1 + ((tr.get_value() / per + i * 0.4) % 1) * (yt - yb - 0.2)
            m.move_to(self.T((xc, y)))
        cab.add_updater(upd)
        upd(cab)
        return VGroup(shaft, plat, cab)



def ring():
    f = [0, .055, .075, .095, .295, .315, .35, .47, .49, .51, .88, .90, 1.0]
    P = [(-5.2, -1.2), (-5.2, 1.2), (-5.2, 2.3), (-4.4, 2.3), (4.4, 2.3), (5.2, 2.3), (5.2, 1.2), (5.2, -1.2),
         (5.2, -2.3), (4.4, -2.3), (-4.4, -2.3), (-5.2, -2.3), (-5.2, -1.2)]
    return Track(f, P, [(0, B), (.095, B), (.295, R), (.51, R), (.88, B), (1, B)])


def ring_mobs():
    pipe = RoundedRectangle(width=10.4, height=4.6, corner_radius=0.5, color=GREY, stroke_width=5, stroke_opacity=0.6)
    lungs = Rectangle(width=8.8, height=0.9, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([0, 2.3, 0])
    body = Rectangle(width=8.8, height=1.1, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([0, -2.3, 0])
    rv = RoundedRectangle(width=1.0, height=2.4, corner_radius=0.4, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.25).move_to([-5.2, 0, 0])
    lv = rv.copy().move_to([5.2, 0, 0])
    return dict(pipe=pipe, lungs=lungs, body=body, rv=rv, lv=lv)


def stream(tr, track, n=14, r=0.16, mix=None):
    dots = VGroup(*[Circle(radius=r, stroke_width=0, fill_opacity=1) for _ in range(n)])

    def upd(g):
        t = tr.get_value()
        for i, d in enumerate(g):
            u = (t / PERIOD + i / n) % 1
            if mix is None:
                p, c, o = track.pos(u), track.col(u), track.op(u)
            else:
                rg, ld, a = mix
                a = a.get_value()
                p = (1 - a) * rg.pos(u) + a * ld.pos(u)
                c = ld.col(u)
                o = (1 - a) + a * ld.op(u)
            d.move_to(p)
            d.set_fill(c, opacity=o)
    dots.add_updater(upd)
    upd(dots)
    return dots



def heart_halves(scale=0.117):
    def pts(a, b):
        ts = np.linspace(a, b, 80)
        return [np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]) * scale for t in ts]
    left = Polygon(*pts(np.pi, 2 * np.pi), color=B, stroke_width=3, fill_color=B, fill_opacity=0.55)
    right = Polygon(*pts(0, np.pi), color=R, stroke_width=3, fill_color=R, fill_opacity=0.55)
    return VGroup(left, right)



PAPER = "#C8B68A"
BREAD = "#D9A35B"
NERVE_UP = YELLOW
NERVE_DN = TEAL


def paper():
    return Rectangle(width=13.4, height=7.5, stroke_color=PAPER, stroke_width=3, stroke_opacity=0.5,
                     fill_color=PAPER, fill_opacity=0.10).set_z_index(-5)


def counter(tr, label, center, w=2.1):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=1.1, stroke_color=GREY, stroke_width=2.5,
                           fill_color=BG, fill_opacity=0.92)
    lab = T(label, 24, TEXT).move_to(box.get_center() + UP * 0.28)
    num = M("0.00 L", 28, TEXT).move_to(box.get_center() + DOWN * 0.2)
    g = VGroup(box, lab, num)
    st = {"s": None}

    def upd(m):
        s = f"{tr.get_value() * 5 / 60:.2f} L"
        if s != st["s"]:
            st["s"] = s
            num.become(M(s, 28, TEXT).move_to(box.get_center() + DOWN * 0.2))
    g.add_updater(upd)
    g.move_to([center[0], center[1], 0])
    return g




def ring_k(k=1.0, o=(0, 0)):
    f = [0, .055, .075, .095, .295, .315, .35, .47, .49, .51, .88, .90, 1.0]
    P = [(-5.2, -1.2), (-5.2, 1.2), (-5.2, 2.3), (-4.4, 2.3), (4.4, 2.3), (5.2, 2.3), (5.2, 1.2), (5.2, -1.2),
         (5.2, -2.3), (4.4, -2.3), (-4.4, -2.3), (-5.2, -2.3), (-5.2, -1.2)]
    return Track(f, P, [(0, B), (.095, B), (.295, R), (.51, R), (.88, B), (1, B)], k=k, o=o)


def ring_mobs_k(k=1.0, o=(0, 0)):
    d = ring_mobs()
    for m in d.values():
        m.scale(k, about_point=ORIGIN).shift([o[0], o[1], 0])
    return d


def start_clock(sc):
    sc.tr = ValueTracker(0)
    sc.tr.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(sc.tr)
    return sc.tr


def make_cup(tr, cx, cy, w=1.0, d=1.4, Tb=0.8, k=1.0):
    th = np.linspace(0, np.pi, 40)
    pts = [np.array([cx + w * k * np.cos(t), cy - d * k * np.sin(t), 0]) for t in th]
    cup = Polygon(*pts, color=GOLD, stroke_width=6, fill_color=GOLD, fill_opacity=0.28)
    cup.base = cup.copy()

    def sq(m):
        ph = (tr.get_value() / Tb) % 1
        s = 1 - 0.22 * np.exp(-((ph - 0.12) / 0.07) ** 2)
        m.become(m.base.copy().stretch(s, 1, about_point=[cx, cy, 0]))
    cup.add_updater(sq)
    return cup


def scoop_arc(tr, start, end, r=0.3, Tb=0.8, apex=1.2, color=None):
    """A red scoop that leaves the cup each beat, arcs to `end` and is gone."""
    dot = Circle(radius=r, stroke_width=0, fill_color=color or R, fill_opacity=1)
    st, en = np.array(start, float), np.array(end, float)

    def u(m):
        ph = (tr.get_value() / Tb) % 1
        if ph < 0.12:
            m.move_to(st).set_opacity(smooth(ph / 0.12))
        elif ph < 0.62:
            a = (ph - 0.12) / 0.5
            p = st + (en - st) * a
            p[1] += apex * np.sin(np.pi * a)
            m.move_to(p).set_opacity(1)
        else:
            m.set_opacity(0)
    dot.add_updater(u)
    u(dot)
    return dot


def metro(tr, speed, center, h=1.0):
    """The film-1 metronome: a trapezoid body and a swinging pendulum. `speed` = beats per second tracker."""
    cx, cy = center
    ph = ValueTracker(0)
    ph.add_updater(lambda m, dt: m.increment_value(dt * speed.get_value()))
    body = Polygon([cx - 0.4 * h, cy - 0.6 * h, 0], [cx + 0.4 * h, cy - 0.6 * h, 0], [cx + 0.2 * h, cy + 0.6 * h, 0],
                   [cx - 0.2 * h, cy + 0.6 * h, 0], color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)
    pivot = np.array([cx, cy - 0.5 * h, 0])
    pend = Line(pivot, pivot + UP * 1.25 * h, color=GOLD, stroke_width=6)
    bob = Dot(radius=0.11 * h + 0.03, color=GOLD)

    def sw(m):
        a = 0.5 * np.cos(np.pi * ph.get_value())
        tip = pivot + 1.25 * h * np.array([-np.sin(a), np.cos(a), 0])
        pend.put_start_and_end_on(pivot, tip)
        bob.move_to(pivot + 0.8 * h * np.array([-np.sin(a), np.cos(a), 0]))
    pend.add_updater(sw)
    sw(pend)
    g = VGroup(body, pend, bob)
    g.ph = ph
    return g


def dial(center, r, color, a_tr, wob=0.0, tr=None):
    """A round control dial; a_tr in 0..1 sets the needle from lower left, over the top, to lower right."""
    cx, cy = center
    face = Circle(radius=r, color=color, stroke_width=5, fill_color=BG, fill_opacity=0.95).move_to([cx, cy, 0])
    scale_arc = Arc(radius=r * 0.8, start_angle=-PI / 6, angle=4 * PI / 3, color=GREY, stroke_width=3).move_to([cx, cy, 0])
    scale_arc.set_stroke(opacity=0.8)
    needle = Line([cx, cy, 0], [cx, cy + r * 0.72, 0], color=color, stroke_width=6)
    hub = Dot([cx, cy, 0], radius=0.07, color=color)

    def nu(m):
        a = a_tr.get_value()
        ang = 7 * PI / 6 - a * 4 * PI / 3
        if wob and tr is not None:
            ang += wob * np.sin(tr.get_value() * 5.0)
        m.put_start_and_end_on([cx, cy, 0], [cx + 0.72 * r * np.cos(ang), cy + 0.72 * r * np.sin(ang), 0])
    needle.add_updater(nu)
    nu(needle)
    return VGroup(face, scale_arc, needle, hub)


def live_counter(fn, label, center, w=2.1, size=28, labsize=24):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=1.1, stroke_color=GREY, stroke_width=2.5,
                           fill_color=BG, fill_opacity=0.92)
    lab = T(label, labsize, TEXT).move_to(box.get_center() + UP * 0.28)
    num = M("0", size, TEXT).move_to(box.get_center() + DOWN * 0.2)
    g = VGroup(box, lab, num)
    st = {"s": None}

    def upd(m):
        s = fn()
        if s != st["s"]:
            st["s"] = s
            num.become(M(s, size, TEXT).move_to(box.get_center() + DOWN * 0.2))
    g.add_updater(upd)
    g.move_to([center[0], center[1], 0])
    return g


def heart_big(scale=0.2, center=(0.0, -0.2)):
    h = heart_halves(scale)
    h.move_to([center[0], center[1], 0])
    return h


def person(cx, base_y, fill=True):
    torso = RoundedRectangle(corner_radius=0.3, width=1.1, height=1.65, stroke_color=TEXT, stroke_width=3,
                             fill_color=R, fill_opacity=0.8 if fill else 0.0).move_to([cx, base_y + 0.825, 0])
    head = Circle(radius=0.32, stroke_color=TEXT, stroke_width=3, fill_color=R, fill_opacity=0.8 if fill else 0.0)
    head.move_to([cx, base_y + 1.65 + 0.34, 0])
    return VGroup(torso, head)


def clock_face(center, r=0.8):
    cx, cy = center
    face = Circle(radius=r, color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=0.9).move_to([cx, cy, 0])
    ticks = VGroup(*[Line([cx + (r - 0.12) * np.cos(a), cy + (r - 0.12) * np.sin(a), 0],
                          [cx + r * np.cos(a), cy + r * np.sin(a), 0], color=GREY, stroke_width=3)
                     for a in np.arange(0, 2 * PI, PI / 6)])
    return VGroup(face, ticks)


# the tank world (scenes 06 to 09) ---------------------------------------------------------------
TANK_X, TANK_W, TANK_Y0, TANK_H = -1.1, 1.8, -2.6, 5.2
BODY_X = 3.0
UNIT = 2.4              # tank height that equals the body's 5 L
CUP_X, CUP_Y = -4.9, 0.4
CLK = (5.4, 2.2)
CTR = (2.7, 1.9)


def tank_world(sc, tr, vmax, c0=0.0, with_scoops=True):
    """cup + tank + body + clock + counter, driven by one tracker c (0..1 = the half hour).
    vmax = body-fulls pumped by the end of the half hour (31.5 for the 70 mL guess, 15.75 for 35 mL)."""
    c = ValueTracker(c0)
    c.run = False
    c.add_updater(lambda m, dt: m.increment_value(dt / 7.0) if (m.run and m.get_value() < 1) else None)
    sc.add(c)
    cup = make_cup(tr, CUP_X, CUP_Y)
    tank = Rectangle(width=TANK_W, height=TANK_H, color=TEXT, stroke_width=4).move_to([TANK_X, TANK_Y0 + TANK_H / 2, 0])
    fillr = Rectangle(width=TANK_W - 0.1, height=0.05, stroke_width=0, fill_color=R, fill_opacity=0.75)
    spill = Rectangle(width=TANK_W + 0.3, height=0.12, stroke_width=0, fill_color=R, fill_opacity=0)

    def vf():
        return vmax * c.get_value() ** 2

    def lvl(m):
        h = (vf() * UNIT) % TANK_H if c.get_value() > 0 else 0.0
        h = max(h, 0.04)
        m.become(Rectangle(width=TANK_W - 0.1, height=h, stroke_width=0, fill_color=R, fill_opacity=0.75)
                 .move_to([TANK_X, TANK_Y0 + 0.05 + h / 2, 0]))
        o = float(np.clip((h - (TANK_H - 0.7)) / 0.7, 0, 1)) * 0.9
        spill.set_fill(R, opacity=o)
        spill.move_to([TANK_X, TANK_Y0 + TANK_H + 0.04, 0])
    fillr.add_updater(lvl)
    lvl(fillr)
    body = person(BODY_X, TANK_Y0)
    ref = DashedLine([TANK_X + TANK_W / 2, TANK_Y0 + UNIT, 0], [BODY_X - 0.55, TANK_Y0 + UNIT, 0], color=GREY,
                     stroke_width=2.5, dash_length=0.15)
    blab = T("all the blood\nin the body", 26, TEXT).move_to([BODY_X, 0.75, 0])
    clk = clock_face(CLK)
    hand = Line([CLK[0], CLK[1], 0], [CLK[0], CLK[1] + 0.6, 0], color=GOLD, stroke_width=6)

    def hu(m):
        ang = PI / 2 - c.get_value() * PI
        m.put_start_and_end_on([CLK[0], CLK[1], 0], [CLK[0] + 0.62 * np.cos(ang), CLK[1] + 0.62 * np.sin(ang), 0])
    hand.add_updater(hu)
    hu(hand)
    clab = T("half an hour", 24, TEXT).move_to([CLK[0], 1.05, 0])
    ctr = live_counter(lambda: f"{int(vf())} x body", "pumped", CTR, 3.0, 28, 24)
    d = dict(c=c, cup=cup, tank=tank, fill=fillr, spill=spill, body=body, ref=ref, blab=blab,
             clock=VGroup(clk, hand, clab), ctr=ctr, vf=vf)
    if with_scoops:
        d["scoop"] = None
    return d


def scoop_to_tank(tr, k=1.0, Tb=0.5):
    return scoop_arc(tr, [CUP_X, CUP_Y - 0.5, 0], [TANK_X, TANK_Y0 + TANK_H + 0.1, 0], r=0.3 * k, Tb=Tb, apex=1.0)


def tag(text, color=YELLOW, size=28):
    return T(text, size, color)


def card(text, color=GREY, size=28):
    lab = T(text, size, TEXT)
    box = RoundedRectangle(corner_radius=0.16, width=lab.width + 0.5, height=lab.height + 0.45, stroke_color=color,
                           stroke_width=3.5, fill_color=color, fill_opacity=0.14)
    return VGroup(box, lab.move_to(box))


# the heart world (scenes 12 to 14) ------------------------------------------------------------------
def heart_world(tr):
    heart = heart_big(0.2, (0.0, -0.2))
    cup = make_cup(tr, 0.0, 0.3, w=1.3, d=2.1, Tb=0.8)
    return heart, cup


# arm world (scenes 03, 04) --------------------------------------------------------------------------
VEIN_C = "#6F9DB5"
ART_C = "#7A8190"
BAND_X = -3.4
ART_Y, VEIN_Y = -0.2, 0.55


def arm_outline():
    arm = Polygon([-6.2, 1.15, 0], [-1.2, 1.0, 0], [4.0, 0.8, 0], [4.0, -0.9, 0], [-1.2, -1.1, 0], [-6.2, -1.25, 0],
                  color=GREY, stroke_width=4, fill_color=TEXT, fill_opacity=0.05)
    hand = Ellipse(width=1.9, height=1.7, color=GREY, stroke_width=4, fill_color=TEXT, fill_opacity=0.05).move_to([4.75, -0.05, 0])
    return VGroup(hand, arm)


def pulse_box(tr, amp, center=(3.4, 2.65)):
    cx, cy = center
    w, h = 3.4, 1.3
    box = Rectangle(width=w, height=h, color=GREY, stroke_width=3).move_to([cx, cy, 0])
    trace = VMobject(color=RED, stroke_width=5)

    def u(m):
        t = tr.get_value()
        pts = []
        for i in range(70):
            x = i / 69
            tt = t - (1 - x) * 1.3
            y = amp.get_value() * pulse(tt, 0.9) * 0.45
            pts.append([cx - w / 2 + 0.1 + x * (w - 0.2), cy - 0.3 + y * 1.2 - 0.0, 0])
        m.set_points_as_corners(pts)
    trace.add_updater(u)
    u(trace)
    lab = T("pulse at wrist", 26, TEXT).next_to(box, LEFT, buff=0.3)
    return VGroup(box, trace, lab)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Circulation and the Heart"
    TITLE = "Harvey's Arithmetic"


class S01Question(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        cupL = make_cup(tr, -3.6, 1.6, w=1.2, d=1.7, Tb=1.4)
        cupR = make_cup(tr, 3.6, 1.6, w=1.2, d=1.7, Tb=1.4)
        cl = counter(tr, "flow, right side", [-3.6, -1.6], 3.1)
        cr = counter(tr, "flow, left side", [3.6, -1.6], 3.1)
        self.play(FadeIn(cupL), FadeIn(cupR), run_time=0.8)
        self.at("same flow")
        self.play(FadeIn(cl), FadeIn(cr), run_time=0.7)
        self.at("how big is that flow")
        self.play(FadeOut(cupL), FadeOut(cupR), run_time=0.5)
        self.play(cl.animate.scale(1.3).move_to([-2.3, 0.3, 0]), cr.animate.scale(1.3).move_to([2.3, 0.3, 0]),
                  run_time=1.1)
        q = T("?", 110, YELLOW).move_to([0, 2.5, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("what did measuring")
        pg = paper()
        self.play(FadeIn(pg), FadeOut(q), cl.animate.set_opacity(0.35), cr.animate.set_opacity(0.35), run_time=1.4)
        self.finish()


class S02Galen(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg = paper()
        torso = RoundedRectangle(corner_radius=0.5, width=2.4, height=3.4, color=GREY, stroke_width=4,
                                 fill_color=TEXT, fill_opacity=0.05).move_to([0, -0.2, 0])
        head = Circle(radius=0.5, color=GREY, stroke_width=4, fill_color=TEXT, fill_opacity=0.05).move_to([0, 2.2, 0])
        ends = [np.array(p + [0.0]) for p in ([-3.4, 1.7], [3.4, 1.7], [-2.3, -3.0], [2.3, -3.0])]
        starts = [np.array(p + [0.0]) for p in ([-1.1, 1.2], [1.1, 1.2], [-0.6, -1.7], [0.6, -1.7])]
        limbs = VGroup(*[Line(s, e, color=GREY, stroke_width=14, stroke_opacity=0.55) for s, e in zip(starts, ends)])
        date = M("until 1628", 34, YELLOW).move_to([-4.6, 2.9, 0])
        self.play(FadeIn(pg), FadeIn(torso), FadeIn(head), FadeIn(limbs), run_time=1.0)
        self.at("account came from galen")
        self.play(FadeIn(date), run_time=0.6)
        self.at("blood was made")
        bread = VGroup(RoundedRectangle(corner_radius=0.18, width=1.0, height=0.65, color=BREAD, stroke_width=3,
                                        fill_color=BREAD, fill_opacity=0.7), T("food", 26, TEXT).move_to([0, -0.7, 0]))
        bread.move_to([-5.0, 0.3, 0])
        arr = Arrow([-4.3, 0.55, 0], [-0.75, 0.55, 0], buff=0, color=BREAD, stroke_width=5, tip_length=0.2)
        liver = Polygon([-0.6, 0.15, 0], [0.7, 0.15, 0], [0.9, 0.5, 0], [0.5, 0.85, 0], [-0.5, 0.8, 0],
                        color="#A56A45", stroke_width=3, fill_color="#A56A45", fill_opacity=0.85)
        liver.move_to([0.1, 0.5, 0])
        llab = T("liver", 26, TEXT).move_to([0.1, -0.35, 0])
        self.play(FadeIn(bread, shift=RIGHT * 0.3), GrowArrow(arr), run_time=1.0)
        self.play(FadeIn(liver), FadeIn(llab), run_time=0.6)
        on = ValueTracker(0)
        drops = VGroup(*[Circle(radius=0.14, stroke_width=0, fill_color=R, fill_opacity=0) for _ in range(8)])
        liver_c = np.array([0.1, 0.5, 0.0])

        def upd(g):
            t = tr.get_value()
            for i, d in enumerate(g):
                u = (t * 0.3 + i / 8) % 1
                s, e = liver_c, ends[i % 4]
                a = u
                p = s + (e - s) * a
                grow = 1.0
                op = 1.0
                if u > 0.82:
                    q = (u - 0.82) / 0.18
                    grow = 1 + 2.6 * q
                    op = 1 - q
                d.become(Circle(radius=0.14 * grow, stroke_width=0, fill_color=R, fill_opacity=op * on.get_value()).move_to(p))
        drops.add_updater(upd)
        self.add(drops)
        self.play(on.animate.set_value(1), run_time=1.0)
        self.at("tissues it reached")
        lab = T("Galen: made from food, used up", 30, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(lab), run_time=0.8)
        self.at("used it up")
        self.play(*[Indicate(l, color=RED, scale_factor=1.0) for l in limbs], run_time=1.2)
        self.finish()


def arm_scene_base(sc, tr, tight):
    pg = paper()
    arm = arm_outline()
    art = Line([-6.2, ART_Y, 0], [4.8, ART_Y, 0], color=ART_C, stroke_width=8)
    v_up = Line([-6.2, VEIN_Y, 0], [BAND_X, VEIN_Y, 0], color=VEIN_C, stroke_width=3 if tight else 6)
    v_dn = Line([BAND_X, VEIN_Y, 0], [4.8, VEIN_Y, 0], color=VEIN_C, stroke_width=3 if tight else 6)
    amp = ValueTracker(0.0 if tight else 1.0)
    pb = pulse_box(tr, amp)
    link = Line([3.0, 0.85, 0], [3.0, 1.95, 0], color=GREY, stroke_width=3)
    return pg, arm, art, v_up, v_dn, amp, pb, link


class S03BandTight(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg, arm, art, v_up, v_dn, amp, pb, link = arm_scene_base(self, tr, tight=False)
        self.play(FadeIn(pg), FadeIn(arm), run_time=1.0)
        self.at("tested this on")
        alab = T("artery, deep", 26, ART_C).move_to([-4.4, -0.85, 0]) if False else None
        self.play(FadeIn(art), FadeIn(v_up), FadeIn(v_dn), run_time=0.9)
        self.play(FadeIn(pb), FadeIn(link), run_time=0.8)
        self.at("tied a band")
        band = Rectangle(width=0.3, height=2.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                         fill_opacity=0.85).move_to([BAND_X, 0.0, 0])
        self.play(FadeIn(band, scale=1.4), run_time=0.8)
        self.at("tied tight")
        self.play(band.animate.stretch_to_fit_width(0.6).stretch_to_fit_height(2.2),
                  amp.animate.set_value(0.0), v_up.animate.set_stroke(width=3), v_dn.animate.set_stroke(width=3), run_time=1.6)
        self.at("stopped the pulse")
        lab = T("tight band: no pulse, veins flat", 30, YELLOW).move_to([-1.0, -2.6, 0])
        self.play(FadeIn(lab), run_time=0.8)
        self.finish()


class S04BandLoose(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg, arm, art, v_up, v_dn, amp, pb, link = arm_scene_base(self, tr, tight=True)
        band = Rectangle(width=0.6, height=2.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                         fill_opacity=0.85).move_to([BAND_X, 0.0, 0])
        self.add(pg, arm, art, v_up, v_dn, pb, link, band)
        self.wait(0.4)
        self.at("tied more loosely")
        self.play(band.animate.stretch_to_fit_width(0.3).stretch_to_fit_height(2.5), run_time=1.2)
        self.at("arteries drive blood in")
        self.play(amp.animate.set_value(1.0), run_time=1.0)
        n = 8
        red = VGroup(*[Circle(radius=0.15, stroke_width=0, fill_color=R, fill_opacity=1) for _ in range(n)])

        def ru(g):
            t = tr.get_value()
            for i, d in enumerate(g):
                u = (t * 0.18 + i / n) % 1
                d.move_to([-6.0 + u * 10.4, ART_Y, 0])
                d.set_fill(R, opacity=float(np.clip(min(u / 0.04, (1 - u) / 0.05), 0, 1)))
        red.add_updater(ru)
        ru(red)
        self.play(FadeIn(red), run_time=0.6)
        a_in = Arrow([-5.6, -1.7, 0], [-2.0, -1.7, 0], buff=0, color=R, stroke_width=6, tip_length=0.25)
        l_in = T("in by arteries", 30, R).move_to([-3.8, -2.4, 0])
        self.play(GrowArrow(a_in), FadeIn(l_in), run_time=0.8)
        self.at("stopped its return")
        blue = VGroup(*[Circle(radius=0.15, stroke_width=0, fill_color=B, fill_opacity=1) for _ in range(n)])

        def bu(g):
            t = tr.get_value()
            for i, d in enumerate(g):
                u = (t * 0.16 + i / n) % 1
                d.move_to([4.4 - u * (4.4 - (BAND_X + 0.5)), VEIN_Y, 0])
                d.set_fill(B, opacity=float(np.clip(min(u / 0.04, (1 - u) / 0.1), 0, 1)))
        blue.add_updater(bu)
        bu(blue)
        self.play(FadeIn(blue), run_time=0.6)
        self.at("veins below the band swelled")
        self.play(v_dn.animate.set_stroke(width=20), run_time=2.0)
        self.at("blood enters a limb")
        self.play(Indicate(l_in, color=R), run_time=0.9)
        self.at("leaves by veins")
        a_out = Arrow([0.2, 1.75, 0], [-3.4, 1.75, 0], buff=0, color=B, stroke_width=6, tip_length=0.25)
        l_out = T("out by veins", 30, B).move_to([-3.0, 2.4, 0])
        self.play(GrowArrow(a_out), FadeIn(l_out), run_time=0.8)
        self.finish()


class S05Scoop(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg = paper()
        cup = make_cup(tr, -3.2, 1.6, w=1.8, d=3.0, Tb=0.8)
        self.add(pg)
        self.play(FadeIn(cup), run_time=0.8)
        self.at("question of quantity")
        gl = T("ventricle", 30, GOLD).move_to([-3.2, -1.9, 0])
        self.play(FadeIn(gl), run_time=0.6)
        self.at("small guesses")
        sc = scoop_arc(tr, [-2.8, 0.2, 0], [3.4, 0.8, 0], r=0.3, Tb=0.8, apex=1.6)
        self.add(sc)
        self.wait(1.2)
        tg = tag("deliberately low guess", YELLOW, 30).move_to([2.2, -1.2, 0])
        self.play(FadeIn(tg), run_time=0.7)
        self.at("how much blood leaves")
        sp = speed_tracker(0.0)
        mb = metro(tr, sp, [0.4, 2.2], 0.9)
        sp.set_value(1.25)
        self.add(mb.ph)
        self.play(FadeIn(mb), run_time=0.7)
        self.at("each beat")
        self.play(Indicate(sc, color=YELLOW, scale_factor=1.4), run_time=1.0)
        self.finish()


def speed_tracker(v):
    return ValueTracker(v)


class S06Tank(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg = paper()
        w = tank_world(self, tr, 31.5)
        sc = scoop_to_tank(tr)
        self.add(pg)
        self.play(FadeIn(w["cup"]), run_time=0.5)
        self.add(sc)
        self.at("multiplied by")
        self.play(FadeIn(w["tank"]), FadeIn(w["fill"]), run_time=0.8)
        self.at("beats in half")
        self.play(FadeIn(w["body"]), FadeIn(w["blab"]), run_time=0.8)
        self.add(w["fill"], w["spill"])
        self.at("half an hour")
        self.add(w["ctr"])
        self.play(FadeIn(w["clock"]), FadeIn(w["ref"]), run_time=0.8)
        w["c"].run = True
        self.at("even that low product")
        self.wait(0.2)
        self.at("whole body contains")
        self.play(Indicate(w["body"], color=YELLOW, scale_factor=1.12), run_time=1.2)
        self.at("far more than food")
        bread = VGroup(RoundedRectangle(corner_radius=0.1, width=0.5, height=0.32, color=BREAD, stroke_width=3,
                                        fill_color=BREAD, fill_opacity=0.7), T("food", 26, TEXT).move_to([0, -0.4, 0]))
        bread.move_to([1.0, -1.7, 0])
        self.play(FadeIn(bread), run_time=0.8)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg = paper()
        w = tank_world(self, tr, 31.5, c0=1.0)
        self.add(pg, w["cup"], w["tank"], w["fill"], w["spill"], w["body"], w["ref"], w["clock"], w["ctr"], w["blab"])
        sc = scoop_to_tank(tr)
        self.add(sc)
        self.wait(0.8)
        self.at("test the argument")
        self.play(Indicate(w["tank"], color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.at("suppose his guess")
        self.wait(0.2)
        self.at("too big")
        self.remove(sc)
        half = scoop_arc(tr, [CUP_X, CUP_Y - 0.5, 0], [CUP_X + 2.2, CUP_Y + 0.6, 0], r=0.15, Tb=0.8, apex=0.8)
        self.add(half)
        hl = tag("scoop halved", YELLOW, 30).move_to([-4.9, -1.9, 0])
        self.play(FadeIn(hl), w["c"].animate.set_value(0.0), run_time=1.6)
        self.at("does his conclusion")
        cf = card("conclusion\nfalls").move_to([5.3, -0.2, 0])
        cs = card("conclusion\nstands").move_to([5.3, -1.7, 0])
        self.play(FadeIn(cf, shift=LEFT * 0.3), FadeIn(cs, shift=LEFT * 0.3), run_time=0.8)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        import os
        config.background_color = BG
        dur = float(os.environ.get("KX_DURATION", "5.0"))
        tr = start_clock(self)
        pg = paper()
        w = tank_world(self, tr, 15.75, c0=0.0)
        cup = w["cup"]
        half = Circle(radius=0.15, stroke_width=0, fill_color=R, fill_opacity=1).move_to([CUP_X + 1.5, CUP_Y + 0.2, 0])
        half.add_updater(lambda m: m.scale(1.0))
        hb = half.copy()
        half.add_updater(lambda m: m.become(hb.copy().scale(1 + 0.15 * np.sin(tr.get_value() * 4))))
        hl = tag("scoop halved", YELLOW, 30).move_to([-4.9, -1.9, 0])
        cf = card("conclusion\nfalls").move_to([5.3, -0.2, 0])
        cs = card("conclusion\nstands").move_to([5.3, -1.7, 0])
        self.add(pg, cup, w["tank"], w["fill"], w["body"], w["ref"], w["clock"], w["ctr"], w["blab"], half, hl, cf, cs)
        # 5-second ring timer, bottom right
        cx, cy = 6.15, -3.2
        base = Circle(radius=0.42, color=GREY, stroke_width=4).move_to([cx, cy, 0])
        arc = Arc(radius=0.42, start_angle=PI / 2, angle=-2 * PI, color=YELLOW, stroke_width=7).move_to([cx, cy, 0])
        t0 = tr.get_value()

        def au(m):
            f = max(0.001, 1 - (tr.get_value() - 0.0) / dur)
            m.become(Arc(radius=0.42, start_angle=PI / 2, angle=-2 * PI * f, color=YELLOW, stroke_width=7).move_to([cx, cy, 0]))
        arc.add_updater(au)
        self.add(base, arc)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg = paper()
        w = tank_world(self, tr, 15.75, c0=0.0)
        cs = card("conclusion\nstands", YELLOW).move_to([5.3, -1.7, 0])
        self.add(pg, w["cup"], w["tank"], w["fill"], w["spill"], w["body"], w["ref"], w["clock"], w["ctr"], w["blab"])
        sc = scoop_arc(tr, [CUP_X, CUP_Y - 0.5, 0], [TANK_X, TANK_Y0 + TANK_H + 0.1, 0], r=0.15, Tb=0.5, apex=1.0)
        self.add(sc)
        self.play(FadeIn(cs), run_time=0.5)
        glow = SurroundingRectangle(cs, color=YELLOW, buff=0.12, stroke_width=6)
        glow.add_updater(lambda m: m.set_stroke(opacity=0.55 + 0.45 * np.sin(tr.get_value() * 4)))
        self.add(glow)
        self.at("even with half")
        eq = M("35 mL × 75 per min × 30 min ≈ 79 L, nearly 16 × 5 L", 26, YELLOW)
        fit(eq, max_w=12.4)
        eq.move_to([0, 3.4, 0])
        self.play(FadeIn(eq), run_time=0.8)
        self.at("half an hour still")
        w["c"].run = True
        self.at("overflows the body")
        self.play(Indicate(w["body"], color=YELLOW, scale_factor=1.12), run_time=1.2)
        self.at("far more than")
        self.play(Indicate(w["tank"], color=YELLOW, scale_factor=1.03), run_time=1.2)
        self.finish()


class S10Circulates(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg = paper()
        w = tank_world(self, tr, 15.75, c0=0.9)
        self.add(pg, w["cup"], w["tank"], w["fill"], w["body"], w["ref"], w["clock"], w["ctr"], w["blab"])
        self.wait(0.4)
        rg = ring_k()
        m = ring_mobs()
        dots = stream(tr, rg)
        self.play(FadeOut(VGroup(w["cup"], w["tank"], w["fill"], w["body"], w["ref"], w["clock"], w["ctr"], w["blab"], pg)),
                  FadeIn(m["pipe"]), FadeIn(m["lungs"]), FadeIn(m["body"]), FadeIn(m["rv"]), FadeIn(m["lv"]),
                  FadeIn(dots), run_time=1.4)
        lt = T("lungs", 30, TEXT).move_to([0, 3.2, 0])
        bt = T("body", 30, TEXT).move_to([0, -3.3, 0])
        self.add(lt, bt)
        self.at("it leaves the heart")
        self.play(Indicate(m["lv"], color=GOLD), run_time=0.8)
        self.at("by the arteries")
        ar = T("arteries", 30, R).move_to([3.0, -0.9, 0])
        self.play(FadeIn(ar), run_time=0.6)
        self.at("comes back")
        self.play(Indicate(m["rv"], color=GOLD), run_time=0.8)
        self.at("by the veins")
        ve = T("veins", 30, B).move_to([-3.0, -0.9, 0])
        self.play(FadeIn(ve), run_time=0.6)
        self.at("again and again")
        self.wait(1.2)
        self.at("blood circulates")
        circ = Arc(radius=1.35, start_angle=PI / 2, angle=-1.7 * PI, color=YELLOW, stroke_width=7).move_to([0, 0.35, 0])
        circ.add_tip(tip_length=0.3)
        cl = T("circulation", 30, YELLOW).move_to([0, 0.35, 0])
        self.play(Create(circ), FadeIn(cl), run_time=1.4)
        self.finish()


def metro_tri(tr, label_y_unused=0):
    pass


class S11Output(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        pg = paper()
        self.add(pg)
        X1, X2, X3 = -4.6, 0.3, 4.6
        # cardiac output: the jug
        jx, jy0, jh, jw = X1, -2.9, 3.6, 2.4
        jug = Rectangle(width=jw, height=jh, color=TEXT, stroke_width=4).move_to([jx, jy0 + jh / 2, 0])
        fillr = Rectangle(width=jw, height=0.1, stroke_width=0, fill_color=R, fill_opacity=0.7)
        Tb = 0.8

        def lvl(m):
            n = tr.get_value() / Tb
            v = (0.07 * (int(n) + smooth((n % 1 - 0.45) / 0.2))) % 0.95
            h = max(0.05, jh * v)
            m.become(Rectangle(width=jw - 0.1, height=h, stroke_width=0, fill_color=R, fill_opacity=0.7)
                     .move_to([jx, jy0 + 0.05 + h / 2, 0]))
        fillr.add_updater(lvl)
        l1 = T("cardiac output", 32, TEXT).move_to([X1, 1.2, 0])
        # heart rate: metronome
        sp = speed_tracker(1.25)
        mb = metro(tr, sp, [X2, -0.8], 1.5)
        l2 = T("heart rate", 32, GREEN).move_to([X2, 1.2, 0])
        # stroke volume: cup and scoop
        cup = make_cup(tr, X3, -0.3, w=1.2, d=1.8, Tb=Tb)
        scp = scoop_arc(tr, [X3, -1.0, 0], [X3, 0.4, 0], r=0.3, Tb=Tb, apex=0.3)
        l3 = T("stroke volume", 32, R).move_to([X3, 1.2, 0])
        eq = T("=", 44, TEXT).move_to([-2.3, -0.4, 0])
        mul = T("×", 44, TEXT).move_to([2.5, -0.4, 0])
        self.add(fillr)
        self.play(FadeIn(jug), run_time=0.9)
        self.at("cardiac output is")
        self.play(FadeIn(l1), run_time=0.7)
        self.at("heart rate times")
        self.add(mb.ph)
        self.play(FadeIn(eq), FadeIn(l2), FadeIn(mb), run_time=0.9)
        self.at("stroke volume")
        self.play(FadeIn(mul), FadeIn(l3), FadeIn(cup), FadeIn(scp), run_time=0.9)
        self.at("the blood it ejects")
        self.play(Indicate(scp, color=YELLOW, scale_factor=1.6), run_time=1.0)
        self.finish()


def heart_scene(sc, tr, rate=True, stroke=True, ar=None, as_=None):
    heart, cup = heart_world(tr)
    objs = {"heart": heart, "cup": cup}
    ar = ar or ValueTracker(0.5)
    as_ = as_ or ValueTracker(0.5)
    objs["ar"], objs["as"] = ar, as_
    if rate:
        objs["rdial"] = dial((-2.7, 0.5), 0.6, GREEN, ar, 0.0, tr)
        objs["rlab"] = T("rate", 28, GREEN).move_to([-3.5, -0.45, 0])
    if stroke:
        objs["sdial"] = dial((0.2, -0.8), 0.6, R, as_, 0.0, tr)
        objs["slab"] = T("stroke volume", 28, R).move_to([4.4, -1.1, 0])
        objs["sleader"] = Line([0.85, -0.8, 0], [2.8, -1.1, 0], color=GREY, stroke_width=3)
    return objs


class S12Dials(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        o = heart_scene(self, tr)
        co = live_counter(lambda: f"{(55 + 45 * o['ar'].get_value()) * (50 + 40 * o['as'].get_value()) / 1000:.1f} L/min",
                          "flow", [4.9, 1.7, 0], 2.9, 28, 24)
        self.play(FadeIn(o["heart"]), FadeIn(o["cup"]), run_time=1.0)
        self.at("two dials")
        self.play(FadeIn(o["rdial"]), FadeIn(o["sdial"]), run_time=0.9)
        self.at("one dial sets")
        self.add(co)
        self.play(FadeIn(o["rlab"]), run_time=0.7)
        self.play(o["ar"].animate.set_value(0.8), run_time=1.4)
        self.at("the other sets")
        self.play(o["ar"].animate.set_value(0.5), run_time=0.8)
        self.play(FadeIn(o["slab"]), FadeIn(o["sleader"]), run_time=0.7)
        self.play(o["as"].animate.set_value(0.8), run_time=1.4)
        self.play(o["as"].animate.set_value(0.4), run_time=1.2)
        self.finish()


class S13Rate(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        o = heart_scene(self, tr, rate=True, stroke=False)
        self.add(o["heart"], o["cup"], o["rdial"], o["rlab"])
        self.wait(0.6)
        self.at("the rate dial")
        self.play(Indicate(o["rdial"], color=GREEN, scale_factor=1.2), run_time=1.0)
        sp = ValueTracker(0.0)
        sp.add_updater(lambda m, dt: m.set_value(0.5 + 1.2 * o["ar"].get_value()))
        self.add(sp)
        mb = metro(tr, sp, [4.9, 0.4], 1.6)
        self.add(mb.ph)
        self.play(FadeIn(mb), run_time=0.8)
        self.at("sinuatrial node")
        patch = Ellipse(width=0.8, height=0.5, color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.6).move_to([-1.7, 1.55, 0])
        patch.add_updater(lambda m: m.set_fill(GREEN, opacity=0.45 + 0.4 * np.sin(tr.get_value() * 5)))
        lead = Line([-1.9, 1.8, 0], [-2.3, 2.95, 0], color=GREY, stroke_width=3)
        sa = T("SA node", 30, GREEN).move_to([-2.6, 3.35, 0])
        self.play(FadeIn(patch), run_time=0.7)
        self.play(FadeIn(sa), FadeIn(lead), run_time=0.6)
        self.at("patch of pacemaker muscle")
        self.play(Indicate(patch, color=YELLOW, scale_factor=1.5), run_time=1.0)
        self.at("sympathetic nerves")
        nu = CubicBezier([-5.9, 2.6, 0], [-4.8, 2.6, 0], [-4.0, 1.2, 0], [-3.2, 0.9, 0], color=NERVE_UP, stroke_width=7)
        nul = T("sympathetic", 28, NERVE_UP).move_to([-5.0, 3.3, 0])
        self.play(Create(nu), FadeIn(nul), run_time=0.9)
        self.at("turn it up")
        self.play(o["ar"].animate.set_value(0.92), run_time=1.4)
        self.at("and the vagus")
        nd = CubicBezier([-5.9, -1.0, 0], [-4.8, -1.0, 0], [-4.0, 0.1, 0], [-3.25, 0.3, 0], color=NERVE_DN, stroke_width=7)
        ndl = T("vagus\n(parasympathetic)", 26, NERVE_DN).move_to([-5.0, -2.1, 0])
        self.play(Create(nd), FadeIn(ndl), run_time=0.9)
        self.at("turns it down")
        self.play(o["ar"].animate.set_value(0.15), run_time=1.4)
        self.finish()


class S14Stroke(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        o = heart_scene(self, tr, rate=False, stroke=True)
        w = ValueTracker(0)
        sd = dial((0.2, -0.8), 0.6, R, o["as"], 0.09, tr)
        self.add(o["heart"], o["cup"], sd)
        self.wait(0.5)
        self.at("stroke volume dial")
        self.play(Indicate(sd, color=R, scale_factor=1.2), run_time=1.0)
        self.at("three inputs")
        self.wait(0.3)
        self.at("how much the ventricle")
        fill_a = Arrow([-5.6, -0.8, 0], [-0.55, -0.8, 0], buff=0, color=B, stroke_width=9, tip_length=0.3)
        fl = T("filling", 30, B).move_to([-4.9, -1.5, 0])
        self.play(GrowArrow(fill_a), FadeIn(fl), run_time=1.0)
        self.at("how strongly it contracts")
        mus = VGroup(Ellipse(width=1.3, height=0.55, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.4),
                     Arc(radius=0.45, start_angle=0.3, angle=2.5, color=GOLD, stroke_width=4).shift(UP * 0.12)).move_to([0.2, 2.85, 0])
        mus_a = Arrow([0.2, 2.45, 0], [0.2, -0.1, 0], buff=0, color=GOLD, stroke_width=6, tip_length=0.25)
        ml = T("contraction\nstrength", 28, GOLD).move_to([-4.4, 3.2, 0])
        self.play(FadeIn(mus), GrowArrow(mus_a), FadeIn(ml), run_time=1.0)
        self.at("the pressure it must")
        vessel = Line([2.9, 0.4, 0], [6.4, 0.4, 0], color=GREY, stroke_width=24, stroke_opacity=0.7)
        pa = Arrow([5.4, 0.4, 0], [0.9, -0.55, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25)
        pl = T("pressure\npushed against", 28, TEXT).move_to([5.0, 1.75, 0])
        self.play(FadeIn(vessel), FadeIn(pl), GrowArrow(pa), run_time=1.0)
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        K, O = 0.72, (-2.2, 0.0)
        rg = ring_k(K, O)
        m = ring_mobs_k(K, O)
        dots = stream(tr, rg, n=14, r=0.16 * K + 0.03)
        ar, as_ = ValueTracker(0.55), ValueTracker(0.5)
        rd = dial((-3.9, 0.15), 0.55, GREEN, ar, 0.04, tr)
        rl = T("rate", 28, GREEN).move_to([-3.9, -0.7, 0])
        sd = dial((-0.9, 0.15), 0.55, R, as_, 0.04, tr)
        sl = T("stroke volume", 28, R).move_to([-0.9, -0.7, 0])
        amt = ValueTracker(0)
        ctr = live_counter(lambda: f"{amt.get_value():.0f} L", "in 30 min (low guess)", [4.6, 2.4, 0], 3.4, 30, 22)
        body = person(4.6, -2.7)
        bl = T("body: 5 L", 28, TEXT).move_to([4.6, 0.0, 0])
        self.play(FadeIn(m["pipe"]), FadeIn(m["lungs"]), FadeIn(m["body"]), FadeIn(m["rv"]), FadeIn(m["lv"]), FadeIn(dots),
                  run_time=1.4)
        self.at("rate time stroke")
        self.play(FadeIn(rd), FadeIn(rl), run_time=0.6)
        self.at("stroke volume adds")
        self.play(FadeIn(sd), FadeIn(sl), run_time=0.6)
        self.at("adds up to")
        self.add(ctr)
        self.wait(0.5)
        self.play(amt.animate.set_value(79), run_time=1.3, rate_func=linear)
        self.at("than you hold")
        self.play(FadeIn(body), FadeIn(bl), run_time=0.8)
        self.at("food could never")
        self.play(Indicate(ctr, color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.at("same few liters")
        self.play(Indicate(m["pipe"], color=YELLOW, scale_factor=1.0), run_time=1.4)
        self.at("again and again")
        self.play(Indicate(m["lv"], color=GOLD), Indicate(m["rv"], color=GOLD), run_time=1.0)
        self.finish()


class S16End(EndCard):
    LINE = "Half an hour of heartbeats outpumps your blood, so blood circulates."
