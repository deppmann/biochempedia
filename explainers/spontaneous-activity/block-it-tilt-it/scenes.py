"""Block It, Tilt It: chapter 2 of "Activity before experience: spontaneous retinal waves"
(Biochemistrypedia chaptered film).  Timed to the SPOKEN words via self.at("...").

COLOR MAP (one color per concept; shared with every chapter of this lesson)
  BLUE   = the left eye: its cells, axons, territory
  ORANGE = the right eye: its cells, axons, territory (and, in this chapter, the more active eye)
  YELLOW = firing: a spike, a burst, a wave front, a wave event
  PURPLE = the thalamic cell (the target), the sodium channel
  GREEN  = kept, needed (the "Shows" box)
  RED    = failed, blocked, not separated
  PINK   = a drug (tetrodotoxin, epibatidine, the cAMP drugs)
  GOLD   = credits, the PREDICT tag
  GREY   = structure, outlines, labels, silence
One event glyph for a wave event everywhere: a short cluster of yellow vertical bars.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E86A9B"


# ------------------------------------------------------------------------------------------------
# shared pieces
# ------------------------------------------------------------------------------------------------
def eye_icon(color, w=1.0, nt=6):
    """An eye (almond + pupil) with up to six yellow activity ticks above it."""
    ell = Ellipse(width=w, height=0.55 * w, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.22)
    pup = Dot(ell.get_center(), radius=0.15 * w, color=color)
    ticks = VGroup(*[Line([(i - (nt - 1) / 2) * 0.13 * w, 0.52 * w, 0],
                          [(i - (nt - 1) / 2) * 0.13 * w, 0.52 * w + (0.5 if i % 2 else 0.4) * w, 0],
                          color=YELLOW, stroke_width=5) for i in range(nt)])
    g = VGroup(ell, pup, ticks)
    g.ell, g.pup, g.ticks, g.col, g.nt = ell, pup, ticks, color, nt
    return g


def _tick_order(nt):
    return sorted(range(nt), key=lambda i: (abs(i - (nt - 1) / 2), i))


def eye_ticks_set(g, n):
    order = _tick_order(g.nt)
    for rank, i in enumerate(order):
        g.ticks[i].set_stroke(opacity=1.0 if rank < n else 0.0)


def eye_state_anims(g, on):
    c = g.col if on else GREY
    return [g.ell.animate.set_stroke(c).set_fill(c, opacity=0.22 if on else 0.08), g.pup.animate.set_color(c)]


class Beam:
    """The balance beam analogy: left eye and right eye on the pans.  tr > 0 tips the left side down."""

    def __init__(self, cx, cy, L=4.2, hang=3.3, pw=1.25, w=1.7, post_d=1.2, labels=True, lsize=26):
        self.cx, self.cy, self.L, self.hang, self.pw, self.w = cx, cy, L, hang, pw, w
        self.tr = ValueTracker(0.0)
        self.nl = ValueTracker(0.0)
        self.nr = ValueTracker(0.0)
        self._last = (None, None)
        z = [0, 0, 0]
        base_y = cy - hang - post_d
        self.post = Polygon([cx, cy - 0.1, 0], [cx - 0.75, base_y, 0], [cx + 0.75, base_y, 0],
                            stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18)
        self.base = Line([cx - 1.3, base_y, 0], [cx + 1.3, base_y, 0], color=GREY, stroke_width=6)
        self.bar = Line(z, [1, 0, 0], color=TEXT, stroke_width=8)
        self.pivot = Dot([cx, cy, 0], radius=0.14, color=TEXT)
        self.hl = [Line(z, [1, 0, 0], color=GREY, stroke_width=3) for _ in range(2)]
        self.hr = [Line(z, [1, 0, 0], color=GREY, stroke_width=3) for _ in range(2)]
        self.panl = Line(z, [1, 0, 0], color=GREY, stroke_width=7)
        self.panr = Line(z, [1, 0, 0], color=GREY, stroke_width=7)
        self.eL = eye_icon(BLUE, w)
        self.eR = eye_icon(ORANGE, w)
        self.labels = labels
        self.lL = T("left eye", lsize, BLUE)
        self.lR = T("right eye", lsize, ORANGE)
        parts = [self.post, self.base, self.bar, self.pivot, *self.hl, *self.hr, self.panl, self.panr, self.eL, self.eR]
        if labels:
            parts += [self.lL, self.lR]
        self.group = VGroup(*parts)
        self.place(0.0)
        self.group.add_updater(lambda m: self.place(self.tr.get_value()))

    def place(self, a):
        cur = (round(self.nl.get_value(), 3), round(self.nr.get_value(), 3))
        if cur != self._last:
            self._last = cur
            for eye, n in ((self.eL, cur[0]), (self.eR, cur[1])):
                for rank, i in enumerate(_tick_order(eye.nt)):
                    eye.ticks[i].set_stroke(opacity=float(min(1.0, max(0.0, n - rank))))
        L, cx, cy = self.L, self.cx, self.cy
        tl = np.array([cx - L * np.cos(a), cy - L * np.sin(a), 0])
        tr = np.array([cx + L * np.cos(a), cy + L * np.sin(a), 0])
        self.bar.put_start_and_end_on(tl, tr)
        pw = self.pw
        for tip, hs, pan, eye, lab in ((tl, self.hl, self.panl, self.eL, self.lL), (tr, self.hr, self.panr, self.eR, self.lR)):
            P = tip + np.array([0, -self.hang, 0])
            pan.put_start_and_end_on(P + np.array([-pw, 0, 0]), P + np.array([pw, 0, 0]))
            hs[0].put_start_and_end_on(tip, P + np.array([-pw, 0, 0]))
            hs[1].put_start_and_end_on(tip, P + np.array([pw, 0, 0]))
            eye.shift(P + np.array([0, 0.42 * self.w, 0]) - eye.ell.get_center())
            if self.labels:
                lab.move_to(P + np.array([0, -0.48, 0]))

    def set_ticks(self, nl, nr):
        self.nl.set_value(nl)
        self.nr.set_value(nr)
        self.place(self.tr.get_value())

    def tick_anims(self, nl, nr):
        return [self.nl.animate.set_value(nl), self.nr.animate.set_value(nr)]

    def eyes_state(self, on):
        return eye_state_anims(self.eL, on) + eye_state_anims(self.eR, on)

    def tip(self, a):
        return self.tr.animate.set_value(a)


class Lgn:
    """The thalamus (LGN) as a box whose boundary slides: left side = left eye's territory (blue)."""

    def __init__(self, cx, cy, w, h, bx=0.0, fills=True):
        self.cx, self.cy, self.w, self.h = cx, cy, w, h
        self.bt = ValueTracker(bx)
        self.outline = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
        self.fills = fills
        if fills:
            self.left = Rectangle(stroke_width=0, fill_color=BLUE, fill_opacity=0.30)
            self.right = Rectangle(stroke_width=0, fill_color=ORANGE, fill_opacity=0.30)
            self.line = Line([0, 0, 0], [1, 0, 0], color=TEXT, stroke_width=3)
            self.group = VGroup(self.left, self.right, self.line, self.outline)
            self._upd(self.group)
            self.group.add_updater(self._upd)
        else:
            self.group = VGroup(self.outline)

    def _upd(self, m):
        pad = 0.1
        x0, x1 = self.cx - self.w / 2 + pad, self.cx + self.w / 2 - pad
        xb = self.cx + self.bt.get_value()
        hh = self.h - 2 * pad
        self.left.stretch_to_fit_width(max(xb - x0, 0.01)).stretch_to_fit_height(hh).move_to([(x0 + xb) / 2, self.cy, 0])
        self.right.stretch_to_fit_width(max(x1 - xb, 0.01)).stretch_to_fit_height(hh).move_to([(xb + x1) / 2, self.cy, 0])
        self.line.put_start_and_end_on([xb, self.cy + hh / 2, 0], [xb, self.cy - hh / 2, 0])

    def xb(self):
        return self.cx + self.bt.get_value()


def credit(l1, l2, cx=0.0, cy=3.0, size=26):
    a = T(l1, size, TEXT)
    b = T(l2, size, GOLD, weight=BOLD)
    g = VGroup(a, b).arrange(DOWN, buff=0.12).move_to([cx, cy, 0])
    box = RoundedRectangle(corner_radius=0.16, width=g.width + 0.7, height=g.height + 0.4,
                           stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to(g)
    return VGroup(box, a, b)


def predict_row(text, tag_y=3.55, q_y=3.0, qsize=30):
    tag = T("PREDICT", 26, GOLD, weight=BOLD).move_to([0, tag_y, 0])
    q = T(text, qsize, TEXT).move_to([0, q_y, 0])
    return tag, q


def qmark(x, y, size=110, color=TEXT):
    return T("?", size, color, weight=BOLD).move_to([x, y, 0])


def cross(x, y, r=0.3, color=RED, w=7):
    return VGroup(Line([x - r, y - r, 0], [x + r, y + r, 0], color=color, stroke_width=w),
                  Line([x - r, y + r, 0], [x + r, y - r, 0], color=color, stroke_width=w))


def make_clock(scene, t0=0.0):
    """A tracker that counts scene seconds on its own, so wave fronts keep moving under any animation."""
    c = ValueTracker(t0)
    c.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(c)
    return c


def retina(cx, cy, cols, rows, sp, color, r):
    cells = VGroup(*[Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25
                            ).move_to([cx + (i - (cols - 1) / 2) * sp, cy + (j - (rows - 1) / 2) * sp, 0])
                     for j in range(rows) for i in range(cols)])
    frame = RoundedRectangle(corner_radius=0.3, width=cols * sp + 0.35, height=rows * sp + 0.35,
                             stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
    return cells, frame


def wave_cells(cells, clock, starts, x0, v, color, halfw=0.4, cut=None, seed=0):
    """Light cells when a wave front (one per start time, all at speed v) is within halfw.
    After clock >= cut[0] the cells instead fire at random, out of step (disrupted waves)."""
    rng = np.random.RandomState(seed)
    ph = rng.uniform(0, 1, len(cells))
    for k, c in enumerate(cells):
        def u(m, k=k):
            t = clock.get_value()
            if cut is not None and t >= cut[0]:
                on = ((t * 3.1 + ph[k]) % 1.0) < 0.24
            else:
                on = any(0 <= t - t0 <= 6 and abs(m.get_x() - (x0 + (t - t0) * v)) < halfw for t0 in starts)
            m.set_fill(YELLOW if on else color, opacity=1.0 if on else 0.25)
            m.set_stroke(YELLOW if on else color)
        c.add_updater(u)


def calm(cells, color):
    for c in cells:
        c.clear_updaters()
        c.set_fill(color, opacity=0.25).set_stroke(color)


def scatter_pts(rng, x0, x1, y0, y1, n, dmin):
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        p = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        if all(np.linalg.norm(p - q) > dmin for q in pts):
            pts.append(p)
    return pts


def mixed_dots(cx, cy, w, h, n=18, seed=3, r=0.17, dmin=0.6, margin=0.38):
    rng = np.random.RandomState(seed)
    pts = scatter_pts(rng, cx - w / 2 + margin, cx + w / 2 - margin, cy - h / 2 + margin, cy + h / 2 - margin, 2 * n, dmin)
    cols = [BLUE] * (len(pts) // 2) + [ORANGE] * (len(pts) - len(pts) // 2)
    rng.shuffle(cols)
    return VGroup(*[Dot(p, radius=r, color=c) for p, c in zip(pts, cols)])


def sep_dots(cx, cy, w, h, n=9, seed=4, r=0.1, dmin=0.34, margin=0.2):
    rng = np.random.RandomState(seed)
    a = scatter_pts(rng, cx - w / 2 + margin, cx - 0.12, cy - h / 2 + margin, cy + h / 2 - margin, n, dmin)
    b = scatter_pts(rng, cx + 0.12, cx + w / 2 - margin, cy - h / 2 + margin, cy + h / 2 - margin, n, dmin)
    return VGroup(*[Dot(p, radius=r, color=BLUE) for p in a], *[Dot(p, radius=r, color=ORANGE) for p in b])


def wave_event(x, y, w=0.6, h=1.3, nb=5, color=YELLOW, sw=5):
    """The one glyph for a wave event: a short cluster of vertical bars (equal width every time)."""
    return VGroup(*[Line([x - w / 2 + w * i / (nb - 1), y - h / 2, 0], [x - w / 2 + w * i / (nb - 1), y + h / 2, 0],
                         color=color, stroke_width=sw) for i in range(nb)])


def hold_pulse(scene, qms, dur=5.0, label="think it over"):
    """A slow pulse of the question marks and a filling bar, so a silent pause does not look frozen."""
    tr = ValueTracker(0.0)
    bases = [q.height for q in qms]
    bar_w, bar_h, y = 4.6, 0.2, -3.62
    outline = Rectangle(width=bar_w, height=bar_h, stroke_color=GREY, stroke_width=2.5).move_to([1.2, y, 0])
    fill = Rectangle(width=0.01, height=bar_h, stroke_width=0, fill_color=GOLD, fill_opacity=0.85)
    lab = T(label, 26, GREY).move_to([-2.9, y, 0])
    scene.add(outline, lab, fill)

    def up(m):
        t = tr.get_value()
        s = 1 + 0.07 * np.sin(2 * np.pi * t / 1.25)
        for q, b in zip(qms, bases):
            q.scale_to_fit_height(b * s)
        w = max(0.01, bar_w * min(1.0, t / dur))
        fill.become(Rectangle(width=w, height=bar_h, stroke_width=0, fill_color=GOLD, fill_opacity=0.85
                              ).align_to(outline, LEFT).align_to(outline, UP))
    tr.add_updater(up)
    scene.add(tr)
    scene.play(tr.animate.set_value(dur), run_time=dur, rate_func=linear)


# ---- Hodgkin-Huxley membrane (standard squid-axon parameters), used for the traces in s03 ----
def hh_trace(gna_scale=1.0, tmax=30.0, dt=0.01, pulses=((4.0, 6.0, 14.0), (17.0, 19.0, 14.0))):
    gNa, gK, gL = 120.0 * gna_scale, 36.0, 0.3
    ENa, EK, EL = 50.0, -77.0, -54.4
    V = -65.0

    am = lambda V: 1.0 if abs(V + 40) < 1e-6 else 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    an = lambda V: 0.1 if abs(V + 55) < 1e-6 else 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
    bm = lambda V: 4 * np.exp(-(V + 65) / 18)
    ah = lambda V: 0.07 * np.exp(-(V + 65) / 20)
    bh = lambda V: 1 / (1 + np.exp(-(V + 35) / 10))
    bn = lambda V: 0.125 * np.exp(-(V + 65) / 80)
    m = am(V) / (am(V) + bm(V))
    h = ah(V) / (ah(V) + bh(V))
    n = an(V) / (an(V) + bn(V))
    ts, vs = [], []
    steps = int(tmax / dt)
    for k in range(steps + 1):
        t = k * dt
        I = sum(a for (s0, s1, a) in pulses if s0 <= t < s1)
        if k % 10 == 0:
            ts.append(t)
            vs.append(V)
        INa = gNa * m ** 3 * h * (V - ENa)
        IK = gK * n ** 4 * (V - EK)
        IL = gL * (V - EL)
        V += dt * (I - INa - IK - IL)
        m += dt * (am(V) * (1 - m) - bm(V) * m)
        h += dt * (ah(V) * (1 - h) - bh(V) * h)
        n += dt * (an(V) * (1 - n) - bn(V) * n)
    return np.array(ts), np.array(vs)


# ---- fetal cat drawings (s02, s03) ----
def fetal_curl(cx, cy):
    """A small fetal cat curled up inside an outline of the womb.  Not to scale."""
    womb = DashedVMobject(Ellipse(width=8.6, height=5.0, stroke_color=PINK, stroke_width=4), num_dashes=48)
    womb.set_stroke(PINK, 4, opacity=0.7).move_to([cx, cy, 0])
    O = np.array([cx - 0.1, cy - 0.35, 0])
    ang0 = 0.30 * PI
    body = AnnularSector(inner_radius=0.95, outer_radius=1.85, angle=PI * 1.3, start_angle=ang0, arc_center=O,
                         stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.16)
    hc = O + 1.4 * np.array([np.cos(ang0), np.sin(ang0), 0]) + np.array([0.3, 0.1, 0])
    head = Circle(radius=0.95, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1.0).move_to(hc)
    pc = lambda deg, rad=0.95: hc + rad * np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
    ears = VGroup(Polygon(pc(105), pc(145), pc(125, 1.4), stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1.0),
                  Polygon(pc(75), pc(35), pc(55, 1.4), stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1.0))
    eyes = VGroup(*[Arc(radius=0.2, start_angle=PI + 0.4, angle=PI - 0.8, stroke_color=GREY, stroke_width=4
                        ).move_to(hc + np.array([sx * 0.4, 0.05, 0])) for sx in (-1, 1)])
    nose = Dot(hc + np.array([0, -0.38, 0]), radius=0.09, color=GREY)
    bt_end = O + 1.4 * np.array([np.cos(ang0 + 1.3 * PI), np.sin(ang0 + 1.3 * PI), 0])
    tail = ArcBetweenPoints(bt_end + np.array([0.15, -0.1, 0]), bt_end + np.array([1.3, 0.25, 0]), angle=-PI * 0.9,
                            stroke_color=GREY, stroke_width=6)
    buds = VGroup(*[Ellipse(width=0.55, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2
                            ).move_to(O + 0.55 * np.array([np.cos(np.radians(d)), np.sin(np.radians(d)), 0])
                                      ).rotate(np.radians(d + 90)) for d in (170, 215, 260)])
    cat = VGroup(body, buds, tail, ears, head, eyes, nose)
    return womb, cat, head


def fetal_head(cx, cy, r=2.2):
    """Front view of a fetal cat head (closed eyes, big head), with the brain above the eyes."""
    hc = np.array([cx, cy, 0])
    head = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1.0).move_to(hc)
    pc = lambda deg, rad=r: hc + rad * np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
    ears = VGroup(Polygon(pc(100), pc(145), pc(122, 1.4 * r), stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1.0),
                  Polygon(pc(80), pc(35), pc(58, 1.4 * r), stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1.0))
    eyes = VGroup(*[Arc(radius=0.25, start_angle=PI + 0.4, angle=PI - 0.8, stroke_color=GREY, stroke_width=4
                        ).move_to(hc + np.array([sx * 0.8 * r / 2.2, -0.1, 0])) for sx in (-1, 1)])
    nose = Dot(hc + np.array([0, -0.62 * r / 2.2, 0]), radius=0.11, color=GREY)
    k = r / 2.2
    brain = Ellipse(width=2.7 * k, height=1.15 * k, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2
                    ).move_to(hc + np.array([0, 0.95 * k, 0]))
    return VGroup(ears, head, eyes, nose), brain


# ------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Activity before experience: spontaneous retinal waves"
    TITLE = "Block It, Tilt It"


# ------------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """two questions, shown on the beam: take the activity away; make the eyes unequal."""

    def construct(self):
        title = T("Block It, Tilt It", 42, font=TITLE_FONT).move_to([0, 3.3, 0])
        bm = Beam(0, 1.35, L=4.85, hang=2.9, pw=1.15, w=1.8, post_d=1.0)
        bm.set_ticks(4, 4)
        xL = cross(*bm.eL.ticks.get_center()[:2], r=0.72, color=RED, w=12)
        xR = cross(*bm.eR.ticks.get_center()[:2], r=0.72, color=RED, w=12)
        self.play(FadeIn(title), FadeIn(bm.group), run_time=0.8)
        self.at("take activity away")
        self.add(xL, xR)
        self.play(*bm.eyes_state(False), run_time=0.35)
        self.at("what happens", nth=1)
        self.play(*bm.tick_anims(4, 4), *bm.eyes_state(True), FadeOut(xL), FadeOut(xR), run_time=0.7)
        self.at("make the two")
        self.play(*bm.tick_anims(6, 2), bm.tip(0.27), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S02Cat(SpokenScene):
    def construct(self):
        womb, cat, head = fetal_curl(0.0, -0.4)
        card = credit("Shatz and Stryker", "1988", cy=3.05)
        q = chip("first question: take activity away", GREY, 26).move_to([0, -3.4, 0])
        flab = T("fetal cat", 28, TEXT).move_to([5.55, -0.4, 0])
        lead = Line(flab.get_left() + LEFT * 0.1, head.get_center() + np.array([1.05, -0.45, 0]), color=GREY, stroke_width=2.5)
        wl = T("womb", 28, PINK).move_to([-5.7, 1.4, 0])
        wlead = Line(wl.get_right() + RIGHT * 0.1, womb.get_center() + np.array([-4.0, 0.95, 0]), color=PINK, stroke_width=2.5)
        self.add(card)
        self.play(FadeIn(womb), Create(cat), run_time=1.5)
        self.at("asked the first")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.at("fetal cats")
        self.play(FadeIn(flab), Create(lead), FadeIn(wl), Create(wlead), run_time=0.8)
        self.finish()


class S03Pump(SpokenScene):
    def construct(self):
        hc = np.array([2.3, -0.55, 0])
        fh, brain = fetal_head(hc[0], hc[1], 2.5)
        pump = RoundedRectangle(corner_radius=0.35, width=1.7, height=0.65, stroke_color=GREY, stroke_width=4).move_to([2.3, -2.05, 0])
        pfill = RoundedRectangle(corner_radius=0.25, width=1.35, height=0.36, stroke_width=0, fill_color=PINK,
                                 fill_opacity=0.85).move_to(pump)
        pump_l = T("implanted osmotic pump", 26, GREY).move_to([-3.9, 1.75, 0])
        tube_end = brain.get_left() + np.array([0.15, 0.0, 0])
        tube = CubicBezier(pump.get_left(), pump.get_left() + np.array([-1.1, 0.4, 0]),
                           tube_end + np.array([-0.8, -0.5, 0]), tube_end, stroke_color=GREY, stroke_width=7)
        blab = T("brain", 26, GREY).move_to(brain)
        self.play(FadeIn(fh), FadeIn(brain), FadeIn(blab), FadeIn(pump), FadeIn(pfill), FadeIn(pump_l), run_time=0.5)
        self.at("infused")
        self.play(Create(tube), run_time=0.6)
        lab = chip("tetrodotoxin (TTX)", PINK, 26).move_to([-4.2, 0.3, 0])
        self.at("tetrodotoxin")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        drops = [Dot(tube.get_start(), radius=0.14, color=PINK) for _ in range(2)]
        for d in drops:
            self.add(d)
        self.play(*[Succession(Wait(0.3 * i), MoveAlongPath(d, tube, rate_func=linear, run_time=0.8)) for i, d in enumerate(drops)],
                  run_time=1.1)
        self.play(brain.animate.set_fill(PINK, 0.45).set_stroke(PINK), FadeOut(VGroup(*drops)), run_time=0.3)
        bar = Rectangle(width=5.2, height=0.45, stroke_color=GREY, stroke_width=3).move_to([-3.9, -1.6, 0])
        barf = Rectangle(width=5.2, height=0.45, stroke_width=0, fill_color=PINK, fill_opacity=0.85).move_to(bar)
        bl = T("two weeks", 30, TEXT).move_to([-3.9, -2.3, 0])
        self.at("two weeks")
        self.play(FadeIn(bar), FadeIn(bl), run_time=0.2)
        self.play(GrowFromEdge(barf, LEFT), run_time=0.9)
        # Remove the entire implantation picture before the channel close-up.
        self.remove(fh, brain, blab, pump, pfill, pump_l, tube, lab, bar, barf, bl)

        # the drug at the channel: the channel fills the left half, the voltage trace the right half
        cx = -3.2
        mem_l = Rectangle(width=2.7, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([cx - 0.55 - 1.35, -0.2, 0])
        mem_r = Rectangle(width=2.7, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([cx + 0.55 + 1.35, -0.2, 0])
        chan = RoundedRectangle(corner_radius=0.15, width=1.1, height=3.1, stroke_color=PURPLE, stroke_width=3,
                                fill_color=PURPLE, fill_opacity=0.35).move_to([cx, -0.2, 0])
        ch_lab = T("voltage-gated sodium channel", 26, PURPLE).move_to([cx, -2.25, 0])
        mem_lab = T("membrane", 26, GREY).move_to([cx - 2.2, 0.85, 0])
        plug = chip("TTX", PINK, 26, pad=0.12, fill_opacity=0.7).move_to([cx, 1.65, 0])
        na = [chip("Na+", TEXT, 26, pad=0.12, fill_opacity=0.12).move_to([cx + dx, 3.2, 0]) for dx in (-0.8, 0.8)]
        arr = [Arrow([cx + dx, 2.8, 0], [cx + dx, 2.15, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.2) for dx in (-0.8, 0.8)]
        xs = [cross(cx + dx, 2.5, 0.17, RED, 7) for dx in (-0.8, 0.8)]
        # voltage trace, computed from a Hodgkin-Huxley membrane with and without sodium conductance
        ts, v_on = hh_trace(1.0)
        _, v_off = hh_trace(0.0, pulses=())
        ox, oy, W, H = 1.2, -2.45, 5.4, 4.3
        pts = lambda vv: [[ox + W * t / 30.0, oy + H * (v + 80) / 130.0, 0] for t, v in zip(ts, vv)]
        axl = VGroup(Line([ox, oy, 0], [ox, oy + H, 0], color=GREY, stroke_width=3), Line([ox, oy, 0], [ox + W, oy, 0], color=GREY, stroke_width=3))
        trace_on = VMobject(color=YELLOW, stroke_width=5).set_points_as_corners(pts(v_on))
        trace_off = VMobject(color=RED, stroke_width=6).set_points_as_corners(pts(v_off))
        apl = T("membrane voltage", 26, TEXT).move_to([ox + W / 2, oy + H + 0.35, 0])
        tl = T("time", 26, GREY).move_to([ox + W / 2, oy - 0.4, 0])
        none = T("no action potentials", 26, RED).move_to([ox + W / 2, oy + H * 0.62, 0])
        self.at("blocks sodium channels")
        self.play(FadeIn(mem_l), FadeIn(mem_r), FadeIn(chan), FadeIn(ch_lab), FadeIn(mem_lab), run_time=0.6)
        self.at("channels")
        self.play(FadeIn(plug, shift=DOWN * 0.3), Create(axl), FadeIn(apl), FadeIn(tl), Create(trace_on, run_time=0.7), run_time=0.7)
        self.at("so it")
        self.play(*[FadeIn(n) for n in na], *[GrowArrow(a) for a in arr], *[FadeIn(x) for x in xs],
                  Transform(trace_on, trace_off), run_time=0.2)
        self.at("stops action potentials", lead=0)
        self.add(none)
        self.finish()


# ------------------------------------------------------------------------------------------------
def pq1_stage():
    tag, q = predict_row("With spikes blocked, do the two projections separate?")
    # two faint reference pictures, so a prediction can be made from the frame
    ra = VGroup(Rectangle(width=4.6, height=1.55, stroke_color=GREY, stroke_width=3).move_to([-4.2, 1.2, 0]),
                VGroup(*[Dot([-4.2 + side * 1.3 + col * 0.36, 1.2 + row * 0.36, 0],
                            radius=0.12, color=color)
                         for side, color in ((-1, BLUE), (1, ORANGE))
                         for row in (-1, 0, 1) for col in (-1, 0, 1)]))
    rb = VGroup(Rectangle(width=4.6, height=1.55, stroke_color=GREY, stroke_width=3).move_to([-4.2, -1.45, 0]),
                mixed_dots(-4.2, -1.45, 4.6, 1.55, n=9, seed=6, r=0.1, dmin=0.36, margin=0.2))
    la = T("normal: two separate layers", 26, GREY).move_to([-4.2, 2.2, 0])
    lb = T("start: overlapping", 26, GREY).move_to([-4.2, -0.45, 0])
    refs = VGroup(ra, rb, la, lb)
    for grp in (ra, rb):
        grp[0].set_stroke(GREY, 3, opacity=0.7).set_fill(opacity=0)
        grp[1].set_opacity(0.75)
    for tx in (la, lb):
        tx.set_opacity(0.8)
    lgn = Lgn(2.9, -0.35, 5.8, 4.2, fills=False)
    initial = mixed_dots(2.9, -0.35, 5.8, 4.2, n=14, seed=3, r=0.13).set_opacity(0.55)
    lgn.group.add(initial)
    lab = T("LGN, spikes blocked", 28, TEXT).move_to([2.9, 2.2, 0])
    leg = VGroup(Dot(radius=0.14, color=BLUE), T("left eye tracer", 26, BLUE), Dot(radius=0.14, color=ORANGE),
                 T("right eye tracer", 26, ORANGE)).arrange(RIGHT, buff=0.2).move_to([0, -2.95, 0])
    qm = qmark(2.9, -0.35, 130)
    qm.add_background_rectangle(color=BG, opacity=0.95, buff=0.15)
    return dict(tag=tag, q=q, refs=refs, lgn=lgn, initial=initial, lab=lab, leg=leg, qm=qm)


class S04Pq1(SpokenScene):
    def construct(self):
        st = pq1_stage()
        self.play(FadeIn(st["tag"]), FadeIn(st["q"], shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(st["refs"]), FadeIn(st["lgn"].group), FadeIn(st["lab"]), FadeIn(st["leg"]),
                  FadeIn(st["qm"]), run_time=0.9)
        self.at("spikes blocked")
        self.play(Indicate(st["lab"], color=PINK, scale_factor=1.08), run_time=0.7)
        self.at("projections separate")
        self.play(Indicate(st["qm"], color=GOLD, scale_factor=1.08), run_time=0.8)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        st = pq1_stage()
        self.add(st["tag"], st["q"], st["refs"], st["lgn"].group, st["lab"], st["leg"], st["qm"])
        hold_pulse(self, [st["qm"]])
        self.finish()


class S06Rev1(SpokenScene):
    def construct(self):
        st = pq1_stage()
        self.add(st["tag"], st["q"], st["refs"], st["lgn"].group, st["lab"], st["leg"], st["qm"])
        dots = mixed_dots(2.9, -0.35, 5.8, 4.2, n=18, seed=3)
        res = T("not separated", 42, RED, weight=BOLD).move_to([2.9, 2.3, 0])
        self.at("they did not")
        self.play(FadeOut(st["tag"]), FadeOut(st["q"]), FadeOut(st["qm"]), FadeOut(st["lab"]), FadeOut(st["initial"]), FadeIn(res, shift=DOWN * 0.15),
                  FadeIn(dots, lag_ratio=0.03), run_time=0.8)
        self.at("stayed mixed")
        rng = np.random.RandomState(8)
        off = [np.array([rng.uniform(-0.12, 0.12), rng.uniform(-0.12, 0.12), 0]) for _ in dots]
        self.play(*[d.animate.shift(o) for d, o in zip(dots, off)], run_time=0.5)
        self.play(*[d.animate.shift(-o) for d, o in zip(dots, off)], run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S07Student(SpokenScene):
    def construct(self):
        eL = eye_icon(BLUE, 1.9)
        eL.shift(np.array([-5.4, 1.55, 0]) - eL.ell.get_center())
        eR = eye_icon(ORANGE, 1.9)
        eR.shift(np.array([-5.4, -1.55, 0]) - eR.ell.get_center())
        eye_ticks_set(eL, 0)
        eye_ticks_set(eR, 0)
        lgn = Lgn(3.7, -0.15, 4.2, 4.9, fills=False)
        rng = np.random.RandomState(5)
        pts = scatter_pts(rng, 3.7 - 1.6, 3.7 + 1.6, -0.15 - 1.9, -0.15 + 1.9, 14, 0.78)
        cells = VGroup(*[Circle(radius=0.25, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to(p) for p in pts])
        lgn_l = T("LGN: thalamic cells", 26, PURPLE).move_to([3.7, 2.62, 0])
        xe = 1.6
        axL = Line([-4.3, 1.55, 0], [xe, 0.6, 0], color=BLUE, stroke_width=5)
        axR = Line([-4.3, -1.55, 0], [xe, -0.9, 0], color=ORANGE, stroke_width=5)
        tipL = Dot([xe, 0.6, 0], radius=0.14, color=BLUE)
        tipR = Dot([xe, -0.9, 0], radius=0.14, color=ORANGE)
        lL = T("left eye's axons", 26, BLUE).move_to([-1.5, 1.95, 0])
        lR = T("right eye's axons", 26, ORANGE).move_to([-1.5, -2.0, 0])
        q = T("Student: did the drug reach one eye, or both?", 30, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(q), FadeIn(eL), FadeIn(eR), Create(axL), Create(axR), FadeIn(tipL), FadeIn(tipR), FadeIn(lgn.group),
                  FadeIn(cells), FadeIn(lgn_l), FadeIn(lL), FadeIn(lR), run_time=0.65)
        self.at("reach one")
        self.play(Indicate(axL, color=BLUE, scale_factor=1.3), run_time=0.8)
        self.at("or both")
        self.play(Indicate(axR, color=ORANGE, scale_factor=1.3), run_time=0.8)
        shL = Line(axL.get_start(), axL.get_end(), color=PINK, stroke_width=26, stroke_opacity=0.45).set_z_index(-1)
        shR = Line(axR.get_start(), axR.get_end(), color=PINK, stroke_width=26, stroke_opacity=0.45).set_z_index(-1)
        self.at("both and likely")
        self.play(FadeIn(shL), FadeIn(shR), run_time=0.7)
        shg = Rectangle(width=4.2, height=4.9, stroke_width=0, fill_color=PINK, fill_opacity=0.28).move_to([3.7, -0.15, 0]).set_z_index(-1)
        self.at("thalamic cells")
        self.play(FadeIn(shg), run_time=0.8)
        ans = T("Answer: both, and likely the thalamic cells too", 36, TEXT, weight=BOLD)
        abox = SurroundingRectangle(ans, color=PINK, buff=0.2, corner_radius=0.15, stroke_width=4)
        ansg = VGroup(abox, ans).move_to([0, -3.3, 0])
        self.at("as well")
        self.play(FadeIn(ansg, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S08Limit(SpokenScene):
    def construct(self):
        def box(cx, w, col, head):
            bx = RoundedRectangle(corner_radius=0.25, width=w, height=6.0, stroke_color=col, stroke_width=4,
                                  fill_color=col, fill_opacity=0.08).move_to([cx, 0.0, 0])
            h = T(head, 44, col, weight=BOLD).move_to([cx, 2.2, 0])
            return bx, h
        b1, h1 = box(-3.35, 6.0, GREEN, "Shows")
        b2, h2 = box(3.35, 6.0, RED, "Cannot show")
        # "Shows": a big tick and one line of 36 pt text
        tick = VGroup(Circle(radius=0.75, stroke_color=GREEN, stroke_width=6, fill_color=GREEN, fill_opacity=0.15),
                      VMobject(color=GREEN, stroke_width=12).set_points_as_corners([[-0.35, -0.02, 0], [-0.1, -0.3, 0], [0.38, 0.28, 0]])
                      ).move_to([-3.35, 0.7, 0])
        s1 = T("spikes are needed", 38, TEXT).move_to([-3.35, -0.8, 0])
        # "Cannot show": two aligned bullets
        def bullet(txt, y):
            dot = Dot(radius=0.13, color=RED)
            t = T(txt, 36, TEXT, line_spacing=1.25)
            row = VGroup(dot, t).arrange(RIGHT, buff=0.3, aligned_edge=UP)
            dot.align_to(t, UP).shift(DOWN * 0.14)
            row.move_to([0, y, 0]).align_to([0.45, 0, 0], LEFT)
            return row
        r1 = bullet("competition between\nthe eyes", 0.85)
        r2 = bullet("that the spikes that\nmatter are retinal", -1.45)
        self.add(b1, h1, b2, h2)
        self.at("shows that spikes")
        self.play(FadeIn(tick, scale=0.7), FadeIn(s1, shift=UP * 0.1), run_time=0.7)
        self.at("cannot show")
        self.play(Indicate(h2, color=RED, scale_factor=1.08), run_time=0.6)
        self.at("the eyes")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.at("by their activity")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S09Ntf(SpokenScene):
    def construct(self):
        sig = chip("signal", YELLOW, 40).move_to([-4.3, 0.55, 0])
        wir = chip("wiring", GREY, 40).move_to([4.3, 0.55, 0])
        arr = Arrow([-2.6, 0.55, 0], [2.6, 0.55, 0], buff=0, color=GREY, stroke_width=7, tip_length=0.3)
        blk = Rectangle(width=0.35, height=1.5, stroke_width=0, fill_color=RED, fill_opacity=1.0).move_to([0, 0.55, 0])
        need = chip("needed", GREEN, 40).move_to([0, -1.0, 0])
        top = VGroup(sig, wir, arr, blk, need)
        def chip2(text, color):
            lab = T(text, 32, color, line_spacing=1.3)
            box = RoundedRectangle(corner_radius=0.16, width=lab.width + 0.9, height=lab.height + 0.8, stroke_color=color,
                                   stroke_width=2.5, fill_color=color, fill_opacity=0.14)
            return VGroup(box, lab.move_to(box))
        perm = chip2("permissive:\nthe signal must\nbe present", TEXT).move_to([-3.75, -1.65, 0])
        inst = chip2("instructive:\nits pattern tells\nthe wiring what to do", YELLOW).move_to([3.75, -1.65, 0])
        qm = T("?", 100, TEXT, weight=BOLD).move_to([0, -1.65, 0])
        self.play(FadeIn(sig), FadeIn(wir), GrowArrow(arr), run_time=0.5)
        self.at("a signal")
        self.play(FadeIn(blk, scale=1.5), sig.animate.set_opacity(0.35), run_time=0.7)
        self.at("it is needed")
        self.play(FadeIn(need, shift=UP * 0.15), run_time=0.6)
        self.at("cannot show whether")
        self.play(top.animate.shift(UP * 2.0), FadeIn(perm, shift=UP * 0.15), FadeIn(inst, shift=UP * 0.15), Write(qm), run_time=0.9)
        self.at("pattern tells the wiring")
        self.play(Indicate(inst, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.finish()


class S10Instruct(SpokenScene):
    def construct(self):
        bm = Beam(0, 1.45)
        bm.set_ticks(4, 4)
        lab0 = T("a signal that instructs", 38, YELLOW).move_to([0, 3.3, 0])
        lab = T("change where the activity is", 38, TEXT).move_to([0, 3.3, 0])
        self.play(FadeIn(bm.group), FadeIn(lab0), run_time=0.8)
        self.at("change where it is")
        self.play(FadeOut(lab0), FadeIn(lab, shift=DOWN * 0.1), run_time=0.6)
        self.at("eyes unequal")
        self.play(*bm.tick_anims(6, 2), bm.tip(0.2), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------------------------------------
def ferret_head(cx, cy):
    """A ferret: narrow skull, small ears set wide, long pointed snout."""
    # One continuous taper keeps the skull from hiding the pointed muzzle.
    skull = Polygon([cx - 0.78, cy + 0.9, 0], [cx + 0.78, cy + 0.9, 0],
                    [cx + 0.96, cy + 0.25, 0], [cx + 0.6, cy - 0.7, 0],
                    [cx + 0.12, cy - 1.55, 0], [cx - 0.12, cy - 1.55, 0],
                    [cx - 0.6, cy - 0.7, 0], [cx - 0.96, cy + 0.25, 0],
                    stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1.0).round_corners(0.18)
    ears = VGroup(*[Ellipse(width=0.38, height=0.28, stroke_color=GREY, stroke_width=3,
                            fill_color=BG, fill_opacity=1.0
                            ).move_to([cx + sx * 0.88, cy + 0.48, 0]) for sx in (-1, 1)])
    nose = Dot([cx, cy - 1.5, 0], radius=0.12, color=GREY)
    eL = eye_icon(BLUE, 0.65)
    eL.shift(np.array([cx - 0.48, cy + 0.1, 0]) - eL.ell.get_center())
    eR = eye_icon(ORANGE, 0.65)
    eR.shift(np.array([cx + 0.48, cy + 0.1, 0]) - eR.ell.get_center())
    eye_ticks_set(eL, 0)
    eye_ticks_set(eR, 0)
    ears.set_z_index(-1)
    return VGroup(ears, skull, nose, eL, eR), eL, eR


class S11Epi(SpokenScene):
    def construct(self):
        fh, eL, eR = ferret_head(0, 1.65)
        fh.scale(1.4, about_point=np.array([0, 1.65, 0])).shift(UP * 0.35)
        cL, fL = retina(-3.75, -1.25, 8, 4, 0.6, BLUE, 0.2)
        cR, fR = retina(3.75, -1.25, 8, 4, 0.6, ORANGE, 0.2)
        lL = T("left retina", 26, BLUE).move_to([-3.75, -3.0, 0])
        lR = T("right retina", 26, ORANGE).move_to([3.75, -3.0, 0])
        clock = make_clock(self)
        cut = [1e9]
        starts = [0.2, 2.4, 4.6, 6.8, 9.0]
        wave_cells(cL, clock, starts, -3.75 - 2.1 - 0.45, 3.4, BLUE, 0.45, cut=cut, seed=1)
        wave_cells(cR, clock, starts, 3.75 - 2.1 - 0.45, 3.4, ORANGE, 0.45, seed=2)
        cut[0] = self.t_of("disrupting its waves") - 0.1
        self.play(FadeIn(fh), FadeIn(cL), FadeIn(fL), FadeIn(cR), FadeIn(fR), FadeIn(lL), FadeIn(lR), run_time=0.5)
        self.at("epibatidine")
        syr_barrel = Rectangle(width=1.5, height=0.42, stroke_color=GREY, stroke_width=3, fill_color=PINK, fill_opacity=0.55)
        syr_plunger = Rectangle(width=0.15, height=0.7, stroke_width=0, fill_color=GREY, fill_opacity=1.0)
        syr_plunger.next_to(syr_barrel, LEFT, buff=0)
        needle = Line(syr_barrel.get_right(), syr_barrel.get_right() + np.array([1.2, -0.08, 0]), color=GREY, stroke_width=3)
        syr = VGroup(syr_barrel, syr_plunger, needle).move_to([-5.3, 2.35, 0])
        tipx = eL.ell.get_center() + np.array([-0.5, 0.0, 0])
        self.play(FadeIn(syr, run_time=0.2), syr.animate.shift(tipx - needle.get_end()), run_time=0.95, rate_func=smooth)
        epi = chip("epibatidine, thought to\ndisrupt cholinergic waves", PINK, 26).move_to([4.5, 2.5, 0])
        drop = Dot(needle.get_end(), radius=0.12, color=PINK)
        self.at("injected into one eye")
        self.play(FadeIn(epi, shift=UP * 0.1), drop.animate.move_to(eL.ell.get_center()), eL.ell.animate.set_stroke(PINK), run_time=0.6)
        dis = T("left: waves disrupted", 26, PINK).move_to([-3.75, -3.55, 0])
        self.play(FadeOut(drop), FadeOut(syr), run_time=0.4)
        self.at("disrupting its waves")
        self.play(FadeIn(dis), run_time=0.5)
        norm = T("right: normal waves", 26, ORANGE).move_to([3.75, -3.55, 0])
        self.at("the other eye kept")
        self.add(norm)
        self.play(Indicate(fR, color=ORANGE, scale_factor=1.03), run_time=0.7)
        self.finish()


def pq2_stage():
    tag, q = predict_row("Which eye wins territory in the thalamus?")
    recap = VGroup(T("left eye: waves disrupted", 26, BLUE), T("right eye: normal waves", 26, ORANGE)).arrange(RIGHT, buff=0.9).move_to([0, 2.4, 0])
    bm = Beam(-3.5, 0.85, L=1.9, hang=1.8, pw=0.7, w=0.9, post_d=0.9, labels=False)
    bm.set_ticks(4, 4)
    cover = Rectangle(width=5.6, height=4.1, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.8).move_to([-3.5, -0.6, 0])
    cqm = qmark(-3.5, -0.6, 140)
    lgn = Lgn(3.5, -0.6, 5.6, 4.1, fills=False)
    div = DashedLine([3.5, 1.45, 0], [3.5, -2.65, 0], color=TEXT, stroke_width=3)
    lq = qmark(3.5, -0.6, 140)
    l1 = T("left eye", 26, BLUE).move_to([2.1, -3.0, 0])
    l2 = T("right eye", 26, ORANGE).move_to([4.9, -3.0, 0])
    return dict(tag=tag, q=q, recap=recap, bm=bm, cover=cover, cqm=cqm, lgn=lgn, div=div, lq=lq, l1=l1, l2=l2)


class S12Pq2(SpokenScene):
    def construct(self):
        st = pq2_stage()
        self.play(FadeIn(st["tag"]), FadeIn(st["q"], shift=UP * 0.1), FadeIn(st["recap"]), run_time=0.7)
        self.play(FadeIn(st["bm"].group), FadeIn(st["lgn"].group), FadeIn(st["l1"]), FadeIn(st["l2"]), run_time=0.7)
        self.at("wins territory")
        self.play(FadeIn(st["cover"]), Write(st["cqm"]), Create(st["div"]), Write(st["lq"]), run_time=0.9)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        st = pq2_stage()
        self.add(st["bm"].group, st["cover"], st["cqm"], st["lgn"].group, st["div"], st["lq"], st["l1"], st["l2"], st["tag"], st["q"], st["recap"])
        hold_pulse(self, [st["cqm"], st["lq"]])
        self.finish()


class S14Rev2(SpokenScene):
    def construct(self):
        eL = eye_icon(BLUE, 3.0)
        eL.shift(np.array([-3.5, -1.15, 0]) - eL.ell.get_center())
        eye_ticks_set(eL, 0)
        eR = eye_icon(ORANGE, 3.0)
        eR.shift(np.array([3.5, -1.15, 0]) - eR.ell.get_center())
        eye_ticks_set(eR, 6)
        eL.ell.set_stroke(GREY).set_fill(GREY, 0.08)
        eL.pup.set_color(GREY)
        tL = T("treated eye", 34, BLUE).move_to([-3.5, -3.2, 0])
        tR = T("the active eye", 34, ORANGE, weight=BOLD).move_to([3.5, -3.2, 0])
        ring = SurroundingRectangle(VGroup(eR.ell, eR.ticks), color=ORANGE, buff=0.3, corner_radius=0.2, stroke_width=5)
        card = credit("Penn, Riquelme, Feller and Shatz", "1998", cy=3.2)
        self.play(FadeIn(eL), FadeIn(eR), FadeIn(tL), run_time=0.8)
        self.play(Create(ring), FadeIn(tR), run_time=0.7)
        self.at("1998")
        self.play(FadeIn(card), run_time=0.6)
        self.at("reported it")
        self.play(Indicate(ring, color=ORANGE, scale_factor=1.04), run_time=0.7)
        self.finish()


class S15Expand(SpokenScene):
    def construct(self):
        lgn = Lgn(0, 0.0, 10.4, 4.6, 0.0)
        lgn.line.set_stroke(TEXT, 4)
        lt = T("treated eye", 34, BLUE).move_to([-3.4, 2.75, 0])
        la = T("active eye", 34, ORANGE).move_to([3.4, 2.75, 0])
        x0, x1 = -5.1, 5.1
        wb = DoubleArrow([0, 0, 0], [1, 0, 0], buff=0, color=BLUE, stroke_width=5, tip_length=0.2)
        wo = DoubleArrow([0, 0, 0], [1, 0, 0], buff=0, color=ORANGE, stroke_width=5, tip_length=0.2)
        y = -3.4

        def upd(m):
            xb = lgn.xb()
            wb.put_start_and_end_on([x0, y, 0], [xb - 0.1, y, 0])
            wo.put_start_and_end_on([xb + 0.1, y, 0], [x1, y, 0])
        grp = VGroup(wb, wo)
        upd(grp)
        grp.add_updater(upd)
        graded = T("graded shift, not a full takeover", 28, TEXT).move_to([0, -2.85, 0])
        self.play(FadeIn(lgn.group), FadeIn(lt), FadeIn(la), FadeIn(grp), run_time=0.8)
        self.at("projection expanded")
        big = Arrow([2.4, 0.0, 0], [-0.4, 0.0, 0], buff=0, color=TEXT, stroke_width=10, tip_length=0.4).set_z_index(3)
        self.add(graded)
        self.play(GrowArrow(big), lgn.bt.animate.set_value(-1.5), run_time=1.6)
        self.at("shrank")
        self.play(Indicate(wb, color=BLUE, scale_factor=1.15), FadeOut(big), run_time=0.9)
        self.finish()


class S16Camp(SpokenScene):
    def construct(self):
        card = credit("Stellwagen and Shatz", "2002", cy=3.1)
        x_of = lambda t: -2.6 + t * 0.92
        yA, yB, yAx = 0.7, -1.3, -2.75
        ax = Arrow([-2.9, yAx, 0], [6.5, yAx, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        ticks = VGroup(*[Line([x_of(t), yAx - 0.12, 0], [x_of(t), yAx + 0.12, 0], color=GREY, stroke_width=3) for t in range(0, 10)])
        axl = T("time", 26, GREY).move_to([5.9, yAx - 0.42, 0])
        l1 = T("normal waves", 28, TEXT).move_to([-4.65, yA, 0])
        l2 = T("with drugs that\nraise cAMP", 28, PINK).move_to([-4.65, yB, 0])
        guide1 = Line([-2.9, yA - 0.85, 0], [6.4, yA - 0.85, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        guide2 = Line([-2.9, yB - 0.85, 0], [6.4, yB - 0.85, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        ev = lambda y, ts: VGroup(*[wave_event(x_of(t), y, w=0.6, h=1.3) for t in ts])
        w1 = ev(yA, [1.2, 6.6])
        w2 = ev(yB, [0.6, 2.4, 4.2, 6.0, 7.8])
        gap = DoubleArrow([x_of(1.2) + 0.5, yA + 0.95, 0], [x_of(6.6) - 0.5, yA + 0.95, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.15)
        gl = T("a minute or two between waves", 26, GREY).move_to([(x_of(1.2) + x_of(6.6)) / 2, yA + 1.4, 0])
        self.play(FadeIn(card), FadeIn(l1), FadeIn(guide1), GrowArrow(ax), FadeIn(ticks), FadeIn(axl), run_time=0.5)
        self.play(FadeIn(w1, lag_ratio=0.3), FadeIn(gap), FadeIn(gl), run_time=0.4)
        self.at("and shatz")
        self.play(FadeIn(guide2), run_time=0.4)
        self.at("more frequent")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(w2, lag_ratio=0.25), run_time=0.9)
        self.at("drugs that")
        self.play(Indicate(l2, color=PINK, scale_factor=1.1), run_time=0.6)
        self.finish()


class S17One(SpokenScene):
    def construct(self):
        cL, fL = retina(-3.5, 1.9, 6, 3, 0.6, BLUE, 0.2)
        cR, fR = retina(3.5, 1.9, 6, 3, 0.6, ORANGE, 0.2)
        lL = T("left retina", 26, BLUE).move_to([-3.5, 3.45, 0])
        lR = T("right retina", 26, ORANGE).move_to([3.5, 3.45, 0])
        lgn = Lgn(0, -1.6, 9.6, 3.0, 0.0)
        ll = T("left eye's layer", 28, BLUE).move_to([-2.6, -3.4, 0])
        lr = T("right eye's layer", 28, ORANGE).move_to([2.6, -3.4, 0])
        axL = Line([-3.5, 0.95, 0], [-3.0, 0.4, 0], color=BLUE, stroke_width=4, stroke_opacity=0.6)
        axR = Line([3.5, 0.95, 0], [3.0, 0.4, 0], color=ORANGE, stroke_width=4, stroke_opacity=0.6)
        clock = make_clock(self)
        v = 2.8
        wave_cells(cL, clock, [0.4, 3.6], -3.5 - 1.8 - 0.4, v, BLUE, 0.4, seed=1)
        wave_cells(cR, clock, [0.0, 0.8, 1.6, 2.4, 3.2, 4.0], 3.5 - 1.8 - 0.4, v, ORANGE, 0.4, seed=2)
        more = T("more frequent", 28, ORANGE, weight=BOLD).move_to([3.5, 0.45, 0])
        self.play(FadeIn(cL), FadeIn(fL), FadeIn(cR), FadeIn(fR), FadeIn(lL), FadeIn(lR), FadeIn(lgn.group), FadeIn(ll), FadeIn(lr), run_time=0.4)
        self.at("more active")
        self.play(FadeIn(more, shift=UP * 0.1), run_time=0.5)
        self.at("its layer")
        self.play(lgn.bt.animate.set_value(-1.5), run_time=1.3, rate_func=smooth)
        self.finish()


def pq3_stage(clock):
    tag, q = predict_row("Waves more frequent in both eyes: what happens to the layers?")
    cL, fL = retina(-3.5, 1.2, 6, 2, 0.7, BLUE, 0.24)
    cR, fR = retina(3.5, 1.2, 6, 2, 0.7, ORANGE, 0.24)
    wave_cells(cL, clock, [0.0 + 0.8 * k for k in range(20)], -3.5 - 2.1 - 0.4, 2.8, BLUE, 0.4, seed=1)
    wave_cells(cR, clock, [0.4 + 0.8 * k for k in range(20)], 3.5 - 2.1 - 0.4, 2.8, ORANGE, 0.4, seed=2)
    lL = T("more frequent waves", 26, BLUE).move_to([-3.5, 2.5, 0])
    lR = T("more frequent waves", 26, ORANGE).move_to([3.5, 2.5, 0])
    bm = Beam(-3.5, -0.5, L=2.0, hang=1.4, pw=0.65, w=0.75, post_d=0.9, labels=False)
    bm.set_ticks(6, 6)
    cover = Rectangle(width=5.4, height=3.0, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.8).move_to([-3.5, -1.65, 0])
    cqm = qmark(-3.5, -1.65, 110)
    lgn = Lgn(3.5, -1.65, 5.4, 3.0, fills=False)
    lq = qmark(3.5, -1.65, 110)
    return dict(tag=tag, q=q, cL=cL, fL=fL, cR=cR, fR=fR, lL=lL, lR=lR, bm=bm, cover=cover, cqm=cqm, lgn=lgn, lq=lq)


class S18Pq3(SpokenScene):
    def construct(self):
        clock = make_clock(self, 1.0)
        st = pq3_stage(clock)
        self.play(FadeIn(st["tag"]), FadeIn(st["q"], shift=UP * 0.1), FadeIn(st["cL"]), FadeIn(st["fL"]), FadeIn(st["cR"]), FadeIn(st["fR"]),
                  FadeIn(st["bm"].group), FadeIn(st["lgn"].group), run_time=0.8)
        self.at("more frequent")
        self.play(FadeIn(st["lL"]), FadeIn(st["lR"]), run_time=0.5)
        self.at("what happens to the layers")
        self.play(FadeIn(st["cover"]), Write(st["cqm"]), Write(st["lq"]), run_time=0.8)
        self.finish()


class S19Pause(NarratedScene):
    def construct(self):
        clock = make_clock(self, 1.0)
        st = pq3_stage(clock)
        self.add(st["cL"], st["fL"], st["cR"], st["fR"], st["lL"], st["lR"], st["bm"].group, st["cover"], st["cqm"], st["lgn"].group,
                 st["lq"], st["tag"], st["q"])
        hold_pulse(self, [st["cqm"], st["lq"]])
        self.finish()


class S20Rev3(SpokenScene):
    def construct(self):
        lgn = Lgn(3.5, -0.35, 6.0, 3.9, 0.0)
        lgn.line.set_stroke(TEXT, 4)
        ll = T("left eye's\nlayer", 26, BLUE, line_spacing=1.0).move_to([2.0, -3.1, 0])
        lr = T("right eye's\nlayer", 26, ORANGE, line_spacing=1.0).move_to([5.0, -3.1, 0])
        top = T("both eyes boosted, layers normal", 36, TEXT).move_to([0, 3.4, 0])
        bm = Beam(-3.3, 0.9, L=2.5, hang=2.2, pw=0.8, w=1.1, post_d=1.0)
        bm.set_ticks(6, 6)
        wl = DoubleArrow([0.65, -0.35, 0], [3.35, -0.35, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
        wr = DoubleArrow([3.65, -0.35, 0], [6.35, -0.35, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
        brk = Brace(lgn.outline, UP, color=PURPLE, buff=0.12)
        shared = T("one shared target", 28, PURPLE).next_to(brk, UP, buff=0.12)
        self.play(FadeIn(lgn.group), FadeIn(ll), FadeIn(lr), FadeIn(top), FadeIn(bm.group), run_time=0.9)
        self.at("the layers")
        self.play(Indicate(lgn.line, color=TEXT, scale_factor=1.3), run_time=0.7)
        self.at("normal in size")
        self.play(GrowFromCenter(wl), GrowFromCenter(wr), run_time=0.8)
        self.at("which fits")
        self.play(Indicate(bm.bar, color=TEXT, scale_factor=1.06), run_time=0.8)
        self.at("divide a shared")
        self.play(FadeOut(wl), FadeOut(wr), GrowFromCenter(brk), FadeIn(shared), run_time=0.9)
        self.finish()


class S21Diff(SpokenScene):
    def construct(self):
        bm = Beam(0, 1.35, L=3.9, hang=2.4, pw=1.1, w=1.35, post_d=0.8)
        bm.set_ticks(2, 2)
        top = T("territory follows the difference, not the total", 34, TEXT).move_to([0, 3.4, 0])
        an = T("analogy only", 26, GREY).move_to([5.5, -3.35, 0])
        lgn = Lgn(0, -3.2, 7.2, 0.75, 0.0)
        lgn.line.set_stroke(TEXT, 3)
        ll = T("LGN", 26, PURPLE).move_to([-4.9, -3.2, 0])
        self.play(FadeIn(bm.group), FadeIn(an), FadeIn(top), FadeIn(lgn.group), FadeIn(ll), run_time=0.8)
        self.at("difference between")
        self.play(*bm.tick_anims(4, 2), bm.tip(0.18), lgn.bt.animate.set_value(1.4), run_time=1.0)
        self.at("not the total")
        self.play(*bm.tick_anims(6, 6), bm.tip(0.0), lgn.bt.animate.set_value(0.0), run_time=1.1)
        self.finish()


class S22Caveat(SpokenScene):
    def construct(self):
        x_of = lambda t: -2.7 + t * 0.95
        tag = T("one caveat", 38, GOLD, weight=BOLD).move_to([0, 3.4, 0])
        yA, yB = 1.75, -0.3
        l1 = T("normal", 30, TEXT).move_to([-4.9, yA, 0])
        l2 = T("with drug", 30, PINK).move_to([-4.9, yB, 0])
        g1 = Line([-2.9, yA - 0.95, 0], [6.4, yA - 0.95, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        g2 = Line([-2.9, yB - 0.95, 0], [6.4, yB - 0.95, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        r1 = VGroup(*[wave_event(x_of(t), yA, w=0.9, h=1.5, nb=7) for t in (1.2, 6.0)])
        r2 = VGroup(*[wave_event(x_of(t), yB, w=0.9, h=1.5, nb=3) for t in (0.5, 2.4, 4.3, 6.2, 8.1)])
        cw, chh = 3.7, 1.0
        def mk(text, col):
            box = RoundedRectangle(corner_radius=0.14, width=cw, height=chh, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.16)
            return VGroup(box, T(text, 28, col).move_to(box))
        c1 = mk("wave frequency", YELLOW)
        c2 = mk("pattern", YELLOW)
        c3 = mk("number of spikes", GREY)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.35).move_to([0, -2.9, 0])
        only = T("not only", 28, GREY).move_to([c3.get_center() + np.array([0, 0.9, 0])])
        self.play(FadeIn(tag), FadeIn(l1), FadeIn(g1), FadeIn(l2), FadeIn(g2), run_time=0.8)
        self.at("these drugs")
        self.play(FadeIn(r1, lag_ratio=0.05), FadeIn(r2, lag_ratio=0.05), run_time=0.9)
        self.at("wave frequency")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("and pattern")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("not only")
        self.play(FadeIn(only), FadeIn(c3, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        def row(cy, h, col=GREY):
            return RoundedRectangle(corner_radius=0.25, width=12.4, height=h, stroke_color=col, stroke_width=2.5,
                                    fill_color=col, fill_opacity=0.06).move_to([0, cy, 0])
        p1, p2, p3 = row(2.55, 2.1), row(0.1, 2.5), row(-2.4, 2.2)
        # icon 1: activity bars, crossed out
        ic1 = VGroup(*[Line([-5.5 + 0.25 * i, 2.1, 0], [-5.5 + 0.25 * i, 2.1 + (0.95 if i % 2 else 0.75), 0], color=YELLOW, stroke_width=7) for i in range(5)])
        ic1x = cross(-5.0, 2.6, 0.7, RED, 10)
        # icon 2: the same balance as the opening, tipped
        bmi = Beam(-4.7, 0.8, L=1.0, hang=0.85, pw=0.4, w=0.55, post_d=0.5, labels=False)
        bmi.set_ticks(6, 2)
        bmi.tr.set_value(0.2)
        bmi.place(0.2)
        bmi.group.clear_updaters()
        # icon 3: muted wave events (frequency and pattern changed)
        ic3 = VGroup(wave_event(-5.6, -2.4, w=0.5, h=0.9, nb=5, color=GREY, sw=4), wave_event(-4.7, -2.4, w=0.5, h=0.9, nb=3, color=GREY, sw=4),
                     wave_event(-3.8, -2.4, w=0.5, h=0.9, nb=3, color=GREY, sw=4))
        b1 = chip("Block it", PINK, 42, pad=0.28).move_to([-1.7, 2.55, 0])
        t1 = T("activity is needed", 42, TEXT)
        t1.move_to([0, 2.55, 0]).align_to([0.2, 0, 0], LEFT)
        b2 = chip("Tilt it", YELLOW, 42, pad=0.28).move_to([-1.7, 0.1, 0])
        t2 = T("relative activity\nshifts territory", 40, TEXT, line_spacing=1.1)
        t2.move_to([0, 0.1, 0]).align_to([0.2, 0, 0], LEFT)
        b3 = chip("caveat", GREY, 34, pad=0.24).move_to([-1.7, -2.4, 0])
        t3 = T("the drugs changed\nfrequency and pattern too", 32, GREY, line_spacing=1.1)
        t3.move_to([0, -2.4, 0]).align_to([0.2, 0, 0], LEFT)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(p3), FadeIn(ic1), FadeIn(ic1x), FadeIn(bmi.group), run_time=0.8)
        self.at("blocking activity")
        self.play(FadeIn(b1, shift=RIGHT * 0.2), FadeIn(t1, shift=RIGHT * 0.2), run_time=0.8)
        self.at("tilting it")
        self.play(FadeIn(b2, shift=RIGHT * 0.2), run_time=0.6)
        self.at("relative activity")
        self.play(FadeIn(t2, shift=RIGHT * 0.2), run_time=1.0)
        self.at("the eyes")
        self.play(FadeIn(ic3), FadeIn(b3), FadeIn(t3), run_time=0.6)
        self.at("shifts the territory")
        self.play(Indicate(t2, color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.finish()


class S24End(EndCard):
    LINE = "Blocking shows activity is needed;\ntilting shows relative activity shifts territory."

    def construct(self):
        line = Text(self.LINE, font=TITLE_FONT, font_size=40, color=TEXT, line_spacing=1.1)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        VGroup(line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
