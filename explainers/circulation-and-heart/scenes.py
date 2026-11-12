"""One Flow, Two Pressures: circulation-and-heart film 1.

COLOUR MAP: BLUE oxygen-poor blood; RED oxygen-rich blood; GOLD ventricles (lifts);
pressure = height on a vertical axis (schematic); GREY channel = resistance (narrowness).
All shapes are schematic. Counters run at 5 L per min (real time).
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


def mammal(k=1.0, o=(0, 0), c=(0, 0)):
    S1, S2, B1, B2 = (-4.4, -1.45), (-1.6, -2.75), (0.5, 2.6), (6.0, -2.75)
    L = lambda a, b, s: (a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s)
    f = [0, .055, .075, .095, .295, .315, .35, .47, .49, .51, .88, .90, 1.0]
    P = [(-4.9, -2.75), (-4.9, -1.45), S1, L(S1, S2, .04), L(S1, S2, .96), S2, (0, -2.75), (0, 2.6), B1,
         L(B1, B2, .04), L(B1, B2, .96), B2, (-4.9, -2.75)]
    t = Track(f, P, [(0, B), (.095, B), (.295, R), (.51, R), (.88, B), (1, B)], hide=.90, k=k, o=o, c=c)
    t.lifts = [(-4.9, -2.75, -1.45), (0.0, -2.75, 2.6)]
    t.chans = [(S1, S2, .8, .8), (B1, B2, .75, .3)]
    t.floor = (-5.4, 6.4, -2.75)
    return t


def fish(k=1.0, o=(0, 0), c=(0, 0)):
    G1, G2, F1, F2 = (-4.4, 2.4), (-1.9, 0.3), (-1.9, 0.3), (6.0, -2.75)
    L = lambda a, b, s: (a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s)
    f = [0, .20, .23, .25, .43, .45, .93, 1.0]
    P = [(-4.9, -2.75), (-4.9, 2.4), G1, L(G1, G2, .05), L(G1, G2, .95), G2, F2, (-4.9, -2.75)]
    t = Track(f, P, [(0, B), (.25, B), (.43, R), (.78, R), (.93, B), (1, B)], hide=.93, k=k, o=o, c=c)
    t.lifts = [(-4.9, -2.75, 2.4)]
    t.chans = [(G1, G2, .26, .26), (F1, F2, .75, .3)]
    t.floor = (-5.4, 6.4, -2.75)
    return t


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


def axis_mob():
    ar = Arrow([-6.2, -2.75, 0], [-6.2, 3.3, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    lab = T("pressure (schematic)", 24, TEXT).rotate(PI / 2).move_to([-6.6, 0.3, 0])
    return VGroup(ar, lab)


def dimension(x, y0, y1, color=GOLD):
    return DoubleArrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=4, tip_length=0.18)


def hline(x0, x1, y, color=GREY):
    return DashedLine([x0, y, 0], [x1, y, 0], color=color, stroke_width=2.5, dash_length=0.15)


def heart_halves(scale=0.117):
    def pts(a, b):
        ts = np.linspace(a, b, 80)
        return [np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]) * scale for t in ts]
    left = Polygon(*pts(np.pi, 2 * np.pi), color=B, stroke_width=3, fill_color=B, fill_opacity=0.55)
    right = Polygon(*pts(0, np.pi), color=R, stroke_width=3, fill_color=R, fill_opacity=0.55)
    return VGroup(left, right)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Circulation and the Heart"
    TITLE = "One Flow, Two Pressures"


class S01Question(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        heart = heart_halves().move_to([0, -0.1, 0])
        c0 = heart.get_center()

        def beat(m):
            m.become(m.base.copy().scale(1 + 0.07 * pulse(tr.get_value()), about_point=c0))
        heart.base = heart.copy()
        heart.add_updater(beat)
        self.play(FadeIn(heart), run_time=0.5)
        cl = counter(tr, "flow, right side", [-2.3, -3.0], 3.1)
        cr = counter(tr, "flow, left side", [2.3, -3.0], 3.1)
        self.at("pump the same")
        self.play(FadeIn(cl), FadeIn(cr), run_time=0.6)

        def bar(x, color, peak, base):
            box = Rectangle(width=0.9, height=5.0, color=GREY, stroke_width=3).move_to([x, 0.7, 0])
            fill = Rectangle(width=0.9, height=0.1, stroke_width=0, fill_color=color, fill_opacity=0.9)

            def u(m):
                h = 5.0 * (base + (peak - base) * pulse(tr.get_value()))
                m.become(Rectangle(width=0.9, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
                         .move_to([x, -1.8 + h / 2, 0]))
            fill.add_updater(u)
            u(fill)
            lab = T("pressure", 26, color).move_to([x, 3.55, 0])
            return VGroup(box, fill, lab)
        self.at("why does the")
        bl, br = bar(-4.0, B, 0.2, 0.1), bar(4.0, R, 0.95, 0.4)
        self.play(FadeIn(bl), FadeIn(br), run_time=0.6)
        self.at("than the right")
        q = T("?", 110, YELLOW).move_to([0, 2.4, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


class S02Flow(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        Tb = 1.4
        w, d = 1.5, 2.0
        cx, cy = -4.4, 0.4
        th = np.linspace(0, np.pi, 40)
        pts = [np.array([cx + w * np.cos(t), cy - d * np.sin(t), 0]) for t in th]
        cup = Polygon(*pts, color=GOLD, stroke_width=6, fill_color=GOLD, fill_opacity=0.2)
        cup.base = cup.copy()

        def sq(m):
            ph = (tr.get_value() / Tb) % 1
            s = 1 - 0.22 * np.exp(-((ph - 0.12) / 0.07) ** 2)
            m.become(m.base.copy().stretch(s, 1, about_point=[cx, cy, 0]))
        cup.add_updater(sq)
        jx, jy0, jh, jw = 3.4, -2.4, 3.4, 2.2
        jug = Rectangle(width=jw, height=jh, color=TEXT, stroke_width=4).move_to([jx, jy0 + jh / 2, 0])
        fillr = Rectangle(width=jw, height=0.1, stroke_width=0, fill_color=R, fill_opacity=0.7)

        def lvl(m):
            n = tr.get_value() / Tb
            v = 0.1 * (int(n) + smooth((n % 1 - 0.45) / 0.12))
            h = max(0.05, jh * min(v, 0.95))
            m.become(Rectangle(width=jw - 0.1, height=h, stroke_width=0, fill_color=R, fill_opacity=0.7)
                     .move_to([jx, jy0 + 0.05 + h / 2, 0]))
        fillr.add_updater(lvl)
        scoop = Circle(radius=0.32, stroke_width=0, fill_color=R, fill_opacity=1)

        def sc(m):
            ph = (tr.get_value() / Tb) % 1
            st = np.array([cx + 0.2, cy - 0.9, 0])
            if ph < 0.15:
                m.move_to(st).set_opacity(1)
            elif ph < 0.55:
                a = (ph - 0.15) / 0.4
                x = st[0] + (jx - st[0]) * a
                y = st[1] + (cy + 1.4 - st[1]) * 4 * a * (1 - a) + (jy0 + jh + 0.1 - st[1]) * a * a * 0 + (0.8 - st[1]) * 0
                y = st[1] + (2.0 - st[1]) * np.sin(np.pi * a) + (1.0 - st[1]) * a
                m.move_to([x, y, 0]).set_opacity(1)
            elif ph < 0.65:
                m.set_opacity(0)
            else:
                m.move_to(st).set_opacity(smooth((ph - 0.65) / 0.2))
        scoop.add_updater(sc)
        self.add(fillr)
        self.play(FadeIn(cup), FadeIn(jug), FadeIn(scoop), run_time=0.7)
        self.at("flow is the volume")
        jl = T("flow (litres per minute)", 28, TEXT).move_to([2.9, -3.2, 0])
        self.play(FadeIn(jl), run_time=0.5)
        self.at("heart rate")
        mb = Polygon([-0.4, -0.6, 0], [0.4, -0.6, 0], [0.2, 0.6, 0], [-0.2, 0.6, 0], color=TEXT, stroke_width=4,
                     fill_color=TEXT, fill_opacity=0.12).move_to([-4.4, 2.0, 0])
        pend = Line([-4.4, 1.45, 0], [-4.4, 2.6, 0], color=GOLD, stroke_width=5)
        pend.base = pend.copy()

        def sw(m):
            m.become(m.base.copy().rotate(0.45 * np.cos(np.pi * tr.get_value() / Tb), about_point=[-4.4, 1.45, 0]))
        pend.add_updater(sw)
        hr = T("heart rate", 28, GREEN).move_to([-2.4, 2.0, 0])
        self.play(FadeIn(mb), FadeIn(pend), FadeIn(hr), run_time=0.6)
        self.at("stroke volume")
        sv = T("stroke volume", 28, R)

        def svu(m):
            m.move_to([-1.2, 1.2, 0])
            if m.get_center()[1] < 1.1:
                m.set_y(1.1)
            if m.get_center()[1] > 1.2:
                m.set_y(1.2)
            if m.get_center()[0] < -9:
                m.set_x(-3.2)
        sv.add_updater(svu)
        self.play(FadeIn(sv), run_time=0.5)
        eq1 = T("flow", 36, TEXT)
        eqs = [T("=", 36, TEXT), T("heart rate", 36, GREEN), T("×", 36, TEXT), T("stroke volume", 36, R)]
        row = VGroup(eq1, *eqs).arrange(RIGHT, buff=0.3).move_to([0.5, 3.35, 0])
        self.at("flow is its")
        self.play(FadeIn(row[0]), FadeIn(row[1]), run_time=0.4)
        self.at("heart rate times")
        self.play(FadeIn(row[2]), run_time=0.4)
        self.at("stroke volume,")
        self.play(FadeIn(row[3]), FadeIn(row[4]), run_time=0.5)
        self.finish()


def ring_scene_base(sc, tr, labels=True):
    rg = ring()
    m = ring_mobs()
    lt = T("lungs", 30, TEXT).move_to([0, 3.2, 0])
    bt = T("body", 30, TEXT).move_to([0, -3.3, 0])
    return rg, m, lt, bt


class S03Loop(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        rg, m, lt, bt = ring_scene_base(self, tr)
        dots = stream(tr, rg)
        self.play(FadeIn(m["pipe"]), FadeIn(m["lungs"]), FadeIn(m["body"]), FadeIn(m["rv"]), FadeIn(m["lv"]),
                  FadeIn(dots), run_time=1.0)
        self.at("right ventricle")
        rvl = T("right ventricle", 28, GOLD).move_to([-3.0, 0, 0])
        self.play(FadeIn(rvl), Indicate(m["rv"], color=GOLD), run_time=0.8)
        self.at("oxygen poor")
        c1 = chip("oxygen-poor", B, 28).move_to([-2.6, 1.1, 0])
        self.play(FadeIn(c1), run_time=0.5)
        self.at("lungs.")
        self.play(FadeIn(lt), Indicate(m["lungs"], color=GREY), run_time=0.8)
        self.at("oxygen rich")
        c2 = chip("oxygen-rich", R, 28).move_to([2.6, 1.1, 0])
        self.play(FadeIn(c2), run_time=0.5)
        self.at("left side")
        lvl = T("left ventricle", 28, GOLD).move_to([3.0, 0, 0])
        self.play(FadeIn(lvl), Indicate(m["lv"], color=GOLD), run_time=0.8)
        self.at("the body.")
        self.play(FadeIn(bt), Indicate(m["body"], color=GREY), run_time=0.8)
        self.finish()


class S04Series(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        rg, m, lt, bt = ring_scene_base(self, tr)
        dots = stream(tr, rg)
        self.add(*m.values(), lt, bt, dots)
        cr = counter(tr, "flow", [-3.5, 0, 0], 2.0)
        cl = counter(tr, "flow", [3.5, 0, 0], 2.0)
        self.play(FadeIn(cr), FadeIn(cl), run_time=0.6)
        bead = Circle(radius=0.22, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.9)
        t0 = tr.get_value()

        def bu(mm):
            u = ((tr.get_value() - t0) / PERIOD) % 1
            mm.move_to(rg.pos(u))
        bead.add_updater(bu)
        bl = T("one drop", 28, TEXT)
        bl.add_updater(lambda mm: mm.move_to(bead.get_center() - bead.get_center() / max(np.linalg.norm(bead.get_center()), 1e-6) * 1.0 + np.array([0, 0, 0])))
        self.at("in series")
        self.play(FadeIn(bead), FadeIn(bl), run_time=0.5)
        s1 = T("in series:", 32, YELLOW).move_to([0, 0.55, 0])
        self.play(FadeIn(s1), run_time=0.4)
        self.at("leaving one side")
        self.play(FadeOut(bl), run_time=0.4)
        self.at("average flows")
        s2 = T("average flows equal", 32, YELLOW).move_to([0, 0.0, 0])
        self.play(FadeIn(s2), run_time=0.5)
        self.at("be equal")
        s3 = T("about 5 L per min each", 26, TEXT).move_to([0, -0.7, 0])
        self.play(FadeIn(s3), run_time=0.5)
        self.finish()


class S05Height(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        rg, m, lt, bt = ring_scene_base(self, tr)
        ml = mammal()
        a = ValueTracker(0)
        dots = stream(tr, None, mix=(rg, ml, a))
        self.add(*m.values(), lt, bt, dots)
        self.wait(0.6)
        self.at("height.")
        fl = ml.floor_mob()
        chans = [ml.chan_mob(0), ml.chan_mob(1)]
        lifts = [ml.lift_mob(0, tr), ml.lift_mob(1, tr)]
        ax = axis_mob()
        self.play(a.animate.set_value(1), FadeOut(VGroup(*m.values())), FadeOut(lt), FadeOut(bt),
                  FadeIn(fl), *[FadeIn(c) for c in chans], *[FadeIn(l) for l in lifts], FadeIn(ax),
                  run_time=3.0, rate_func=smooth)
        self.at("lift that raises")
        ll = T("lift = ventricle", 28, GOLD).move_to([-3.2, 1.3, 0])
        self.play(FadeIn(ll), Indicate(lifts[1], color=GOLD, scale_factor=1.05), run_time=0.9)
        self.at("rolls downhill")
        sl = T("slope = circuit", 28, TEXT).move_to([4.0, 1.9, 0])
        self.play(FadeIn(sl), Indicate(chans[1], color=TEXT), run_time=0.9)
        self.at("high pressure")
        hi = T("high", 26, TEXT).move_to([-5.85, 3.5, 0])
        self.play(FadeIn(hi), run_time=0.4)
        self.at("to low")
        lo = T("low", 26, TEXT).move_to([-5.85, -3.2, 0])
        self.play(FadeIn(lo), run_time=0.4)
        self.finish()


class S06Resistance(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        P = [(-5.6, 2.3), (-3.2, 1.9), (-0.8, 1.2), (1.4, 0.0), (3.2, -1.4), (4.6, -2.6), (5.4, -3.3)]
        W = [0.9, 0.8, 0.62, 0.42, 0.26, 0.18, 0.15]
        up = [(p[0], p[1] + w / 2, 0) for p, w in zip(P, W)]
        dn = [(p[0], p[1] - w / 2, 0) for p, w in zip(P, W)][::-1]
        chan = Polygon(*(up + dn), color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
        fr = np.linspace(0, 1, len(P))
        tk = Track(fr, P, [(0, R), (1, R)], hide=0.95)
        dots = stream(tr, tk, n=12, r=0.1)
        self.play(FadeIn(chan), FadeIn(dots), run_time=1.2)
        self.at("narrow vessels")
        ind = Circumscribe(VGroup(*[Dot(p) for p in [(3.2, -1.4, 0), (5.4, -3.3, 0)]]), color=YELLOW, run_time=1.2)
        self.play(ind)
        rl = T("resistance", 30, GREY).move_to([4.0, 0.3, 0])
        self.at("call that")
        self.play(FadeIn(rl), run_time=0.5)
        dim = dimension(-6.3, 2.3, -3.3)
        h1 = hline(-6.3, -5.6, 2.3)
        h2 = hline(-6.3, 5.4, -3.3)
        dl = VGroup(T("pressure drop", 28, GOLD), T("(mean in − mean out)", 26, GOLD)).arrange(DOWN, buff=0.15).move_to([-3.6, -0.9, 0])
        self.at("the pressure drop")
        self.play(FadeIn(dim), FadeIn(h1), FadeIn(h2), FadeIn(dl), run_time=0.8)
        eq = [T("pressure drop", 34, GOLD), T("=", 34, TEXT), T("flow", 34, TEXT), T("×", 34, TEXT), T("resistance", 34, GREY)]
        row = VGroup(*eq).arrange(RIGHT, buff=0.28).move_to([0.5, 3.35, 0])
        self.play(FadeIn(row[0]), run_time=0.3)
        self.at("equals the")
        self.play(FadeIn(row[1]), FadeIn(row[2]), run_time=0.4)
        self.at("times its")
        self.play(FadeIn(row[3]), FadeIn(row[4]), run_time=0.4)
        self.finish()


def landscape_full(sc, tr, with_axis=True):
    ml = mammal()
    fl = ml.floor_mob()
    chans = [ml.chan_mob(0), ml.chan_mob(1)]
    lifts = [ml.lift_mob(0, tr), ml.lift_mob(1, tr)]
    dots = stream(tr, ml)
    items = [fl, *chans, *lifts, dots]
    if with_axis:
        items.append(axis_mob())
    sc.add(*items)
    return ml, chans, lifts


class S07Lungs(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        ml, chans, lifts = landscape_full(self, tr)
        self.wait(0.4)
        self.at("resist the flow")
        lab = VGroup(T("lungs: low resistance,", 28, TEXT), T("small drop", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([-3.3, 1.9, 0])
        self.play(FadeIn(lab), Indicate(chans[0], color=TEXT), run_time=1.0)
        self.at("needs only")
        c = counter(tr, "flow", [-4.3, 0.2, 0], 2.0)
        self.play(FadeIn(c), Indicate(lifts[0], color=GOLD, scale_factor=1.08), run_time=1.0)
        self.finish()


class S08Body(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        ml, chans, lifts = landscape_full(self, tr)
        c1 = counter(tr, "flow", [-4.3, 0.2, 0], 2.0)
        self.add(c1)
        self.at("resists far more")
        lab = VGroup(T("body: high resistance,", 28, TEXT), T("big drop", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([4.0, 2.2, 0])
        self.play(FadeIn(lab), Indicate(chans[1], color=TEXT), run_time=1.0)
        self.at("left ventricle")
        c2 = counter(tr, "flow", [-1.9, 0.2, 0], 2.0)
        self.play(FadeIn(c2), Indicate(lifts[1], color=GOLD, scale_factor=1.05), run_time=0.9)
        self.at("much higher")
        h = hline(-4.4, 6.4, -1.45, YELLOW)
        self.play(Create(h), run_time=1.0)
        self.finish()


def brackets(sc, tr):
    h1 = hline(-4.4, -1.1, -1.45, YELLOW)
    d1 = dimension(-1.1, -1.45, -2.75)
    t1 = T("small drop", 28, GOLD).move_to([-2.9, -0.95, 0])
    h2 = hline(0.5, 6.4, 2.6, YELLOW)
    d2 = dimension(6.4, 2.6, -2.75)
    t2 = T("large drop", 28, GOLD).move_to([4.9, 1.3, 0])
    return VGroup(h1, d1, t1), VGroup(h2, d2, t2)


class S09Rule(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        ml, chans, lifts = landscape_full(self, tr)
        c1 = counter(tr, "flow", [-4.3, 0.2, 0], 2.0)
        c2 = counter(tr, "flow", [-1.9, 0.2, 0], 2.0)
        self.add(c1, c2)
        small, large = brackets(self, tr)
        self.at("different costs")
        self.play(FadeIn(small), FadeIn(large), run_time=1.0)
        self.at("with more resistance")
        self.play(Indicate(chans[1], color=TEXT), run_time=1.0)
        ban = VGroup(T("At the same flow, the harder", 30, YELLOW), T("circuit costs more pressure.", 30, YELLOW)).arrange(DOWN, buff=0.1).move_to([0.8, 3.35, 0])
        self.at("bigger pressure")
        self.play(FadeIn(ban), run_time=0.8)
        self.at("two separate pumps")
        self.play(Indicate(lifts[0], color=GOLD, scale_factor=1.08), Indicate(lifts[1], color=GOLD, scale_factor=1.04), run_time=1.2)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        ml, chans, lifts = landscape_full(self, tr, with_axis=False)
        self.add(Rectangle(width=15, height=9, stroke_width=0, fill_color=BG, fill_opacity=0.85))
        tag = T("mean, steady state", 28, YELLOW).move_to([-3.6, 3.4, 0])
        self.play(FadeIn(tag), run_time=0.6)
        self.at("bookkeeping")
        panel = Rectangle(width=9.4, height=3.7, color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.96).move_to([0, 0.9, 0])
        title = T("pressure within one beat (schematic)", 26, TEXT).move_to([0, 2.45, 0])

        def wave(ph):
            return 0.3 + 0.7 * np.exp(-((ph - 0.2) / 0.1) ** 2) + 0.12 * np.exp(-((ph - 0.42) / 0.05) ** 2)
        mean = float(np.mean([wave(p) for p in np.linspace(0, 1, 400)]))
        y0, hh = -0.2, 2.0
        trace = VMobject(color=R, stroke_width=5)

        def tu(m):
            t = tr.get_value()
            xs = np.linspace(-4.2, 4.2, 200)
            pts = [[x, y0 + hh * wave(((x + 4.2) / 8.4 * 3 - t / 1.0) % 1), 0] for x in xs]
            m.set_points_as_corners(pts)
        trace.add_updater(tu)
        tu(trace)
        ml_ = hline(-4.2, 4.2, y0 + hh * mean, YELLOW)
        mt = T("mean", 28, YELLOW).move_to([5.7, y0 + hh * mean, 0])
        self.play(FadeIn(panel), FadeIn(title), FadeIn(trace), run_time=0.8)
        self.at("averages over")
        self.play(Create(ml_), FadeIn(mt), run_time=0.8)
        self.at("heart and the vessels")
        hs = heart_halves(0.05).move_to([-3.0, -2.6, 0])
        vs = Polygon([-1.2, 0.45, 0], [1.2, 0.2, 0], [1.2, -0.2, 0], [-1.2, -0.45, 0], color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.5).move_to([3.0, -2.6, 0])
        da = DoubleArrow([-1.6, -2.6, 0], [1.6, -2.6, 0], buff=0, color=TEXT, stroke_width=5)
        fl = T("flow set together", 28, TEXT).move_to([0, -3.3, 0])
        self.play(FadeIn(hs), FadeIn(vs), run_time=0.6)
        self.at("set the flow")
        self.play(GrowFromCenter(da), FadeIn(fl), run_time=0.8)
        self.finish()


FISH_STOPS = None


def fish_world(sc, tr, k=1.0, o=(0, 0), c=(0, 0), draw=("lift", "gill", "body"), r=0.1, n=14):
    ft = fish(k, o, c)
    return ft


def fish_mobs(ft, tr):
    return ft.floor_mob(), ft.lift_mob(0, tr), ft.chan_mob(0), ft.chan_mob(1)


class S11Fish(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        ft = fish()
        ft.reach = 0.2
        fl, lift, gill, body = fish_mobs(ft, tr)
        sil = VGroup(Ellipse(width=10.2, height=5.6, color=GREY, stroke_width=3, stroke_opacity=0.4,
                             fill_color=GREY, fill_opacity=0.1).move_to([0.2, -0.1, 0]),
                     Polygon([4.9, 0, 0], [6.6, 1.3, 0], [6.6, -1.5, 0], color=GREY, stroke_width=3, stroke_opacity=0.4,
                             fill_color=GREY, fill_opacity=0.1),
                     Dot([-4.3, 1.0, 0], radius=0.14, color=GREY))
        dots = stream(tr, ft, r=0.14)
        reach = ValueTracker(0.2)

        def ru(m):
            ft.reach = reach.get_value()
        reach.add_updater(ru)
        self.add(reach)
        self.play(FadeIn(fl), FadeIn(lift), FadeIn(dots), run_time=0.8)
        self.at("teleost")
        tl = T("teleost fish (trout)", 28, TEXT).move_to([1.0, 3.3, 0])
        self.play(FadeIn(sil), FadeIn(tl), run_time=1.0)
        self.at("one ventricle")
        vl = T("ventricle", 28, GOLD).move_to([-4.9, -3.3, 0])
        self.play(FadeIn(vl), Indicate(lift, color=GOLD, scale_factor=1.05), run_time=0.8)
        self.at("narrow gill")
        self.play(FadeIn(gill), reach.animate.set_value(0.46), run_time=1.0)
        gl = T("gill capillaries", 28, GREY).move_to([-0.6, 1.9, 0])
        self.play(FadeIn(gl), run_time=0.4)
        self.at("onto the body")
        self.play(FadeIn(body), reach.animate.set_value(1.1), run_time=1.0)
        bl = T("body", 28, TEXT).move_to([3.5, 0.9, 0])
        self.play(FadeIn(bl), run_time=0.4)
        self.finish()


def fish_static(sc, tr):
    ft = fish()
    fl, lift, gill, body = fish_mobs(ft, tr)
    dots = stream(tr, ft, r=0.14)
    sc.add(fl, lift, gill, body, dots)
    return ft


def cards():
    cs = [chip(t, GREY, 28) for t in ("same", "higher", "lower")]
    row = VGroup(*cs).arrange(RIGHT, buff=0.25).move_to([3.3, 3.3, 0])
    return cs, row


def question_marks(sc):
    ref = hline(-4.4, 6.0, 2.4, YELLOW)
    rl = T("ventricle pressure", 28, YELLOW).move_to([-2.9, 3.0, 0])
    return ref, rl


class S12Predict(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        fish_static(self, tr)
        ref, rl = question_marks(self)
        cs, row = cards()
        self.at("blood leaves")
        self.play(Create(ref), FadeIn(rl), run_time=1.0)
        self.at("reaches the body")
        ring_ = Circle(radius=0.35, color=YELLOW, stroke_width=5).move_to([-1.9, 0.3, 0])
        self.play(Create(ring_), run_time=0.8)
        self.at("the same as")
        self.play(FadeIn(cs[0]), run_time=0.4)
        self.at("higher")
        self.play(FadeIn(cs[1]), run_time=0.4)
        self.at("lower")
        self.play(FadeIn(cs[2]), run_time=0.4)
        self.finish()


class S13Pause(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        fish_static(self, tr)
        ref, rl = question_marks(self)
        cs, row = cards()
        ring_ = Circle(radius=0.35, color=YELLOW, stroke_width=5).move_to([-1.9, 0.3, 0])
        self.add(ref, rl, row, ring_)
        timer = VMobject()
        center = np.array([5.9, -3.2, 0])
        total = 5.0

        def tu(m):
            f = max(0.0, 1 - tr.get_value() / total)
            arc = Arc(radius=0.4, start_angle=PI / 2, angle=2 * PI * f, color=YELLOW, stroke_width=6, arc_center=center)
            m.become(arc)
        timer.add_updater(tu)
        self.add(timer, Circle(radius=0.4, color=GREY, stroke_width=2).move_to(center))
        self.wait(total - 0.05)
        self.finish()


class S14Reveal(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        fish_static(self, tr)
        ref, rl = question_marks(self)
        cs, row = cards()
        self.add(ref, rl, row)
        self.play(cs[2].animate.set_color(GREEN), *[c.animate.set_opacity(0.35) for c in cs[:2]], run_time=0.6)
        self.at("gill capillaries")
        d1 = dimension(-1.4, 2.4, 0.3)
        gl = VGroup(T("pressure spent", 28, GOLD), T("in the gills", 28, GOLD)).arrange(DOWN, buff=0.1).move_to([1.2, 1.2, 0])
        self.play(FadeIn(d1), FadeIn(gl), run_time=1.0)
        self.at("the body is supplied")
        d2 = dimension(-1.2, 0.3, -2.75, GREEN)
        wl = T("what is left for the body", 28, GREEN).move_to([-1.2, -3.35, 0])
        self.play(FadeIn(d2), FadeIn(wl), run_time=1.0)
        self.finish()


class S15Contrast(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        k = 0.5
        fo, mo = (-3.45, 0.4, 0), (3.45, 0.4, 0)
        c = (0.3, -0.075)
        ft = fish(k, fo, c)
        ml = mammal(k, mo, c)
        fm = VGroup(ft.floor_mob(), ft.lift_mob(0, tr), ft.chan_mob(0), ft.chan_mob(1))
        mm = VGroup(ml.floor_mob(), ml.lift_mob(0, tr), ml.lift_mob(1, tr), ml.chan_mob(0), ml.chan_mob(1))
        d1 = stream(tr, ft, r=0.09)
        d2 = stream(tr, ml, r=0.09)
        t1 = T("fish", 30, TEXT).move_to([-3.45, 2.5, 0])
        t2 = T("birds and mammals", 30, TEXT).move_to([3.45, 2.5, 0])
        self.play(FadeIn(fm), FadeIn(d1), FadeIn(t1), FadeIn(mm), FadeIn(d2), FadeIn(t2), run_time=1.0)
        self.at("that trade")
        self.play(Indicate(fm[2], color=GOLD), run_time=1.0)
        self.at("two pumps")
        self.play(Indicate(mm[1], color=GOLD), Indicate(mm[2], color=GOLD), run_time=1.2)
        self.at("lungs run")
        lo = T("lungs: low", 28, B).move_to(ml.T((-2.6, 0.3)))
        self.play(FadeIn(lo), run_time=0.5)
        self.at("body at high")
        hi = T("body: high", 28, R).move_to(ml.T((4.0, 2.3)))
        self.play(FadeIn(hi), run_time=0.5)
        self.at("both carry")
        c1 = counter(tr, "flow", [ml.T((-4.9, 0))[0], -2.4], 2.0)
        c2 = counter(tr, "flow", [ml.T((0.2, 0))[0] + 0.5, -2.4], 2.0)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.6)
        self.finish()


class S16Close(SpokenScene):
    def construct(self):
        tr = start_clock(self)
        ml, chans, lifts = landscape_full(self, tr)
        c1 = counter(tr, "flow", [-4.3, 0.2, 0], 2.0)
        c2 = counter(tr, "flow", [-1.9, 0.2, 0], 2.0)
        self.add(c1, c2)
        small, large = brackets(self, tr)
        self.at("same blood")
        self.play(Indicate(c1, color=YELLOW), Indicate(c2, color=YELLOW), run_time=1.2)
        self.at("harder circuit")
        self.play(FadeIn(small), FadeIn(large), run_time=1.0)
        self.at("bigger pressure")
        self.play(Indicate(large, color=YELLOW), run_time=1.2)
        self.finish()


class S17End(EndCard):
    LINE = "At the same flow, the harder circuit costs more pressure."
