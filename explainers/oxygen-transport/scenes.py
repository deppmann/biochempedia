"""Why Blood Needs an S-Shaped Carrier (oxygen transport, one film).

COLOUR MAP: BLUE = oxygen / lung band; RED = hemoglobin, adult curve, capacity tank outline;
TEAL = one-site carriers (dashed loose, solid tight); GREY = venous-blood band; GOLD = release bracket.
All curves are computed: Severinghaus (P50 26.8 mmHg) or one-site P/(P+P50).
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

_orig_finish = NarratedScene.finish


def _finish(self):
    over = self.elapsed() - (self.narration_s + 0.4)
    with open("overrun.log", "a") as lg:
        lg.write(f"{type(self).__name__} elapsed {self.elapsed():.1f} narr {self.narration_s:.1f} over {over:+.1f}\n")
    _orig_finish(self)


NarratedScene.finish = _finish

# plot geometry (one world, reused by every plot scene)
PX0, PY0, PW, PH = -3.7, -2.7, 9.6, 4.9
XMAX = 120.0
SX = PW / XMAX
TX, TW = -5.9, 0.9           # capacity tank
XB = 3.0                     # x of the release bracket
SOFT = "#C9CED8"
P_LUNG, P_REST, P_WORK = 100.0, 40.0, 20.0


def px(p):
    return PX0 + p * SX


def py(s):
    return PY0 + s * PH


def sev(p):
    p = np.asarray(p, float)
    return 1.0 / (23400.0 / (p ** 3 + 150.0 * p + 1e-12) + 1.0)


def one(p, p50):
    return p / (p + p50)


S_LUNG = float(sev(P_LUNG))   # 0.9775
S_REST = float(sev(P_REST))   # 0.749
S_WORK = float(sev(P_WORK))   # 0.320


def curve_mob(fn, color, w=8, p_lo=0.0, p_hi=120.0, dashed=False):
    p_hi = max(p_hi, p_lo + 1.0)
    ps = np.linspace(p_lo, p_hi, 120)
    pts = [[px(p), py(float(fn(p))), 0] for p in ps]
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_smoothly(pts)
    m.set_fill(opacity=0)
    if dashed:
        return DashedVMobject(m, num_dashes=44, dashed_ratio=0.6)
    return m


def sev_curve(w=8, p_hi=120.0):
    return curve_mob(sev, RED, w, 0.0, p_hi)


def loose_curve(w=6):
    return curve_mob(lambda p: one(p, 26.8), TEAL, w, 0.0, 120.0, dashed=True)


def tight_curve(w=6):
    return curve_mob(lambda p: one(p, 3.0), TEAL, w, 0.0, 120.0)


def axes_y():
    g = VGroup(Line([PX0, PY0, 0], [PX0, PY0 + PH + 0.25, 0], color=GREY, stroke_width=3))
    for s in (0, 50, 100):
        g.add(Line([PX0, py(s / 100), 0], [PX0 - 0.1, py(s / 100), 0], color=GREY, stroke_width=3))
        g.add(M(str(s), 22, GREY).move_to([PX0 - 0.48, py(s / 100), 0]))
    g.add(T("saturation (%)", 28, TEXT).rotate(PI / 2).move_to([PX0 - 1.2, py(0.5), 0]))
    return g


def axes_x():
    g = VGroup(Line([PX0, PY0, 0], [px(XMAX) + 0.1, PY0, 0], color=GREY, stroke_width=3))
    for p in range(0, 121, 20):
        g.add(Line([px(p), PY0, 0], [px(p), PY0 - 0.1, 0], color=GREY, stroke_width=3))
        g.add(M(str(p), 22, GREY).move_to([px(p), PY0 - 0.38, 0]))
    g.add(T("PO2 (mmHg)", 28, TEXT).move_to([px(60), PY0 - 0.85, 0]))
    return g


def band(p, color, op=0.22, wp=8.0):
    return Rectangle(width=wp * SX, height=PH, stroke_width=0, fill_color=color,
                     fill_opacity=op).move_to([px(p), PY0 + PH / 2, 0])


def lung_label(txt="lungs: ~100 mmHg"):
    return T(txt, 28, BLUE).move_to([px(P_LUNG), 2.75, 0])


def tis_label(txt="resting tissue: ~40 mmHg", p=P_REST):
    return T(txt, 28, TEXT).move_to([px(p), 2.75, 0])


def tank_mob(t, L, grey=True):
    """Capacity tank: blue = oxygen still carried (to level t), gold = released (t to L), grey = unused capacity above L."""
    h = lambda s: max(s * PH, 0.0)
    g = VGroup()
    if h(t) > 0.01:
        g.add(Rectangle(width=TW, height=h(t), stroke_width=0, fill_color=BLUE,
                        fill_opacity=0.8).move_to([TX, PY0 + h(t) / 2, 0]))
    if h(L) - h(t) > 0.01:
        g.add(Rectangle(width=TW, height=h(L) - h(t), stroke_width=0, fill_color=GOLD,
                        fill_opacity=0.9).move_to([TX, PY0 + (h(L) + h(t)) / 2, 0]))
    if grey and PH - h(L) > 0.01:
        g.add(Rectangle(width=TW, height=PH - h(L), stroke_width=0, fill_color=GREY,
                        fill_opacity=0.35).move_to([TX, PY0 + (PH + h(L)) / 2, 0]))
    g.add(Rectangle(width=TW, height=PH, stroke_color=RED, stroke_width=5).move_to([TX, PY0 + PH / 2, 0]))
    return g


def tank_label():
    return T("capacity", 26, RED).move_to([TX, PY0 + PH + 0.4, 0])


def pdot(p, s, color, r=0.15):
    return Dot([px(p), py(s), 0], radius=r, color=color).set_z_index(5)


def bracket(pl, sl, pt, st, xb=XB, w=6):
    """Gold release bracket: guides from the lung point and tissue point to a vertical bar at xb."""
    yh, yl = py(sl), py(st)
    g = VGroup(DashedLine([px(pl), yh, 0], [xb, yh, 0], color=GOLD, stroke_width=3, dash_length=0.12),
               DashedLine([px(pt), yl, 0], [xb, yl, 0], color=GOLD, stroke_width=3, dash_length=0.12),
               Line([xb, yl, 0], [xb, yh, 0], color=GOLD, stroke_width=w))
    return g


def motes(scene, n=16, seed=1):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(max(n, 26)):
        d = Dot(radius=rng.uniform(0.05, 0.1), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.28, 0.5))
        d.move_to([rng.uniform(-6.5, 6.5), rng.uniform(-3.6, 3.6), 0])
        d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.4))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 3.7:
                m.shift(DOWN * 7.4)
            if abs(m.get_x()) > 6.6:
                m.shift(LEFT * 13.2 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-10)
    scene.add(g)
    return g


def hb_block(w=2.4, h=2.0, color=GREY, rounded=True, fill=0.28, slot_r=0.2):
    if rounded:
        body = RoundedRectangle(corner_radius=0.4, width=w, height=h)
    else:
        body = Rectangle(width=w, height=h)
    body.set_stroke(color, 4).set_fill(color, fill)
    slots = VGroup(*[Circle(radius=slot_r, stroke_color=TEXT, stroke_width=3).move_to([sx * w * 0.22, sy * h * 0.22, 0])
                     for sy in (1, -1) for sx in (-1, 1)])
    g = VGroup(body, slots)
    g.body, g.slots = body, slots
    return g


def o2dot(pos, r=0.17):
    pos = list(pos) + [0] * (3 - len(pos))
    return Dot(pos, radius=r, color=BLUE).set_z_index(6)


def bob(m, amp=0.08, speed=1.6, seed=0.0):
    m.base_y = m.get_y()
    m.t0 = seed

    def f(mm, dt):
        mm.t0 += dt
        mm.move_to([mm.get_x(), mm.base_y + amp * np.sin(speed * mm.t0), 0])
    m.add_updater(f)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Carrying Oxygen and Carbon Dioxide"
    TITLE = "Why Blood Needs an S-Shaped Carrier"


# ---------------------------------------------------------------------------------------------
class S01Hook(SpokenScene):
    def construct(self):
        motes(self, 12, 11)
        base, fh, fw = -2.1, 4.4, 2.8
        xl, xr = -3.4, 3.4
        fl = RoundedRectangle(corner_radius=0.2, width=fw, height=fh, stroke_color=TEXT, stroke_width=4).move_to([xl, base + fh / 2, 0])
        fr = RoundedRectangle(corner_radius=0.2, width=fw, height=fh, stroke_color=TEXT, stroke_width=4).move_to([xr, base + fh / 2, 0])
        ln = T("plasma alone", 30, BLUE).move_to([xl, -2.75, 0])
        rn = T("whole blood", 30, RED).move_to([xr, -2.75, 0])
        self.play(Create(fl), Create(fr), FadeIn(ln), FadeIn(rn), run_time=1.2)
        self.at("plasma carries")
        pl_h = 0.14
        plasma = Rectangle(width=fw - 0.1, height=pl_h, stroke_width=0, fill_color=BLUE, fill_opacity=0.75).move_to([xl, base + pl_h / 2 + 0.03, 0])
        self.play(GrowFromEdge(plasma, DOWN), run_time=0.8)
        self.at("about 3")
        pv = T("~3 mL O2 per liter", 30, BLUE).move_to([xl, 2.8, 0])
        self.play(FadeIn(pv, shift=UP * 0.1), run_time=0.6)
        self.at("a liter of your blood")
        bh = 3.6
        blood = Rectangle(width=fw - 0.1, height=bh, stroke_width=0, fill_color=RED, fill_opacity=0.6).move_to([xr, base + bh / 2 + 0.03, 0])
        self.play(GrowFromEdge(blood, DOWN), run_time=2.0)
        rng = random.Random(5)
        cells = VGroup()
        for _ in range(14):
            c = Ellipse(width=0.34, height=0.22, color="#FFB3AA", stroke_width=0, fill_opacity=0.55)
            c.move_to([xr + rng.uniform(-1.15, 1.15), rng.uniform(base + 0.2, base + bh - 0.1), 0])
            c.v = (rng.uniform(-0.25, 0.25), rng.uniform(-0.25, 0.25))

            def dr(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if abs(m.get_x() - xr) > 1.2:
                    m.v = (-m.v[0], m.v[1])
                if m.get_y() < base + 0.15 or m.get_y() > base + bh - 0.05:
                    m.v = (m.v[0], -m.v[1])
            c.add_updater(dr)
            cells.add(c)
        self.add(cells)
        self.at("about 200")
        bv = T("~200 mL O2 per liter", 30, RED).move_to([xr, 2.8, 0])
        self.play(FadeIn(bv, shift=UP * 0.1), run_time=0.6)
        self.at("what makes up")
        qm = T("?", 150, GOLD, weight=BOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(qm, scale=0.4), run_time=0.8)
        bob(qm, 0.12, 2.0)
        self.at("how does blood give it up")
        self.play(Indicate(qm, color=GOLD, scale_factor=1.25), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Hemoglobin(SpokenScene):
    def construct(self):
        motes(self, 10, 12)
        panel = RoundedRectangle(corner_radius=0.3, width=11.6, height=4.4, stroke_color=BLUE, stroke_width=3,
                                 fill_color=BLUE, fill_opacity=0.12).move_to([0, -0.1, 0])
        ph = ValueTracker(0)
        ph.add_updater(lambda m, dt: m.increment_value(dt * 1.6))
        self.add(ph)

        def waves():
            g = VGroup()
            for k, y in enumerate([1.1, 0.1, -0.9, -1.7]):
                g.add(FunctionGraph(lambda x, k=k: 0.13 * np.sin(1.6 * x + ph.get_value() + k * 1.3), x_range=[-5.5, 5.5, 0.1],
                                    color=BLUE, stroke_width=3).shift(UP * y).set_opacity(0.55))
            return g
        wv = always_redraw(waves)
        lab = T("plasma: mostly water", 34, BLUE).move_to([0, 3.0, 0])
        self.play(Create(panel), FadeIn(lab), run_time=1.2)
        self.add(wv)
        self.at("oxygen dissolves")
        o2s = VGroup()
        for (x, y) in [(-3.0, 0.5), (0.5, -0.9), (3.4, 0.9)]:
            d = o2dot([x, y], 0.12)
            d.v = (0.35, 0.2)

            def dr(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if abs(m.get_x()) > 5.2:
                    m.v = (-m.v[0], m.v[1])
                if abs(m.get_y() + 0.1) > 1.8:
                    m.v = (m.v[0], -m.v[1])
            d.add_updater(dr)
            o2s.add(d)
        o2l = T("oxygen dissolves poorly", 32, BLUE).move_to([0, -2.9, 0])
        self.play(FadeIn(o2s, lag_ratio=0.3), FadeIn(o2l), run_time=1.0)
        self.at("the difference rides")
        self.play(FadeOut(lab), FadeOut(o2l), FadeOut(o2s), run_time=0.5)
        cells = VGroup()
        targets = [(-3.6, 0.9), (-1.2, -0.6), (1.4, 0.8), (3.6, -0.7), (-2.4, -1.5), (2.4, -1.5)]
        for (x, y) in targets:
            cells.add(Ellipse(width=1.1, height=0.7, color=RED, stroke_width=3, fill_opacity=0.5).move_to([-8, y, 0]))
        self.play(LaggedStart(*[c.animate.move_to([x, y, 0]) for c, (x, y) in zip(cells, targets)], lag_ratio=0.15, run_time=1.6))
        for c in cells:
            c.add_updater(lambda m, dt: m.shift(RIGHT * 0.22 * dt))
        self.at("hemoglobin")
        hl = T("hemoglobin", 38, RED).move_to([0, 3.0, 0])
        self.play(FadeIn(hl, shift=DOWN * 0.1), run_time=0.6)
        self.at("an iron")
        hl2 = T("hemoglobin: an iron-containing protein", 34, RED).move_to([0, 3.0, 0])
        for c in cells:
            c.clear_updaters()
        bigcell = Ellipse(width=9.6, height=4.0, color=RED, stroke_width=5, fill_opacity=0.14).move_to([0, -0.1, 0])
        self.play(ReplacementTransform(cells[0], bigcell), FadeOut(VGroup(*cells[1:])), FadeOut(panel), FadeOut(wv),
                  Transform(hl, hl2), run_time=1.6)
        self.at("packed inside")
        blocks = VGroup(*[hb_block(2.2, 1.8, RED, fill=0.35, slot_r=0.19).move_to([x, -0.1, 0]) for x in (-2.9, 0, 2.9)])
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in blocks], lag_ratio=0.3, run_time=1.2))
        self.at("red blood cells")
        cl = T("inside red blood cells", 30, RED).move_to([0, -2.65, 0])
        self.play(FadeIn(cl, shift=UP * 0.1), run_time=0.5)
        slots = [s for b in blocks for s in b.slots]
        picks = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        dots = [o2dot([6.4 if i % 2 else -6.4, 3.4 - 0.3 * i, 0]) for i in picks]
        self.add(*dots)
        self.play(LaggedStart(*[d.animate.move_to(slots[i].get_center()) for d, i in zip(dots, picks)], lag_ratio=0.12, run_time=1.5))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Frame(SpokenScene):
    def construct(self):
        motes(self, 12, 13)
        ay = axes_y()
        self.play(Create(ay[0]), FadeIn(VGroup(*ay[1:])), run_time=1.4)
        self.at("share of")
        blk = hb_block(3.6, 3.0, RED, fill=0.32, slot_r=0.3).move_to([1.2, 0.3, 0])
        hbl = T("hemoglobin", 34, RED).move_to([1.2, 2.2, 0])
        reads = ["0 of 4 sites full: 0%", "1 of 4 sites full: 25%", "2 of 4 sites full: 50%", "3 of 4 sites full: 75%", "4 of 4 sites full: 100%"]
        rd = T(reads[0], 30, BLUE).move_to([1.2, -1.7, 0])
        self.play(FadeIn(blk, scale=0.9), FadeIn(hbl), FadeIn(rd), run_time=1.0)
        self.at("hold oxygen")
        dots = VGroup()
        for i in range(4):
            d = o2dot(blk.slots[i].get_center(), 0.26)
            dots.add(d)
            nr = T(reads[i + 1], 30, BLUE).move_to([1.2, -1.7, 0])
            self.remove(rd)
            self.add(nr)
            self.play(GrowFromCenter(d), run_time=0.45)
            rd = nr
            self.wait(0.15)
        self.at("plot it")
        ax = axes_x()
        self.play(FadeOut(VGroup(blk, hbl, rd, dots)), Create(ax[0]), run_time=0.8)
        self.play(FadeIn(VGroup(*ax[1:])), run_time=0.8)
        self.at("loads")
        lb = band(P_LUNG, BLUE, 0.22)
        ll = T("lungs", 28, BLUE).move_to([px(P_LUNG), 2.75, 0])
        self.play(GrowFromEdge(lb, DOWN), FadeIn(ll), run_time=0.9)
        self.at("unloads")
        rb = band(P_REST, GREY, 0.35)
        rl = tis_label("blood leaving resting tissue")
        self.play(GrowFromEdge(rb, DOWN), FadeIn(rl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Bands(SpokenScene):
    def construct(self):
        motes(self, 12, 14)
        lb, rb = band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35)
        ll, rl = lung_label("lungs"), tis_label("blood leaving resting tissue")
        self.add(axes_y(), axes_x(), lb, rb, ll, rl)
        self.at("blood loads")
        ll2 = lung_label()
        cell = Ellipse(width=1.5, height=1.0, color=RED, stroke_width=4, fill_opacity=0.4).move_to([px(P_LUNG), py(0.55), 0])
        self.play(Transform(ll, ll2), FadeIn(cell, scale=0.6), lb.animate.set_fill(BLUE, 0.4), run_time=0.9)
        self.play(lb.animate.set_fill(BLUE, 0.22), run_time=0.5)
        slots = [[-0.35, 0.18], [0.35, 0.18], [-0.35, -0.18], [0.35, -0.18]]
        dots = VGroup(*[o2dot([px(P_LUNG) + a, py(0.55) + b, 0], 0.13) for a, b in slots])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3, run_time=1.4))
        self.at("at rest")
        rl2 = tis_label()
        self.play(Transform(rl, rl2), rb.animate.set_fill(GREY, 0.6), run_time=0.8)
        self.play(rb.animate.set_fill(GREY, 0.35), run_time=0.4)
        self.at("it leaves the tissues")
        grp = VGroup(cell, dots)
        self.play(grp.animate.move_to([px(P_REST), py(0.55), 0]), run_time=1.8)
        drop = dots[3]
        self.play(drop.animate.shift(DOWN * 1.4 + LEFT * 0.4).set_opacity(0.0), run_time=1.0)
        bob(grp, 0.06, 2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Rule(SpokenScene):
    def construct(self):
        motes(self, 12, 15)
        self.add(axes_y(), axes_x(), band(P_LUNG, BLUE, 0.14), band(P_REST, GREY, 0.2))
        f, L = ValueTracker(0.0), ValueTracker(0.0)
        tank = always_redraw(lambda: tank_mob(f.get_value(), L.get_value(), grey=False))
        self.add(tank)
        self.play(FadeIn(tank_label()), run_time=0.6)
        self.at("each deciliter")
        c2 = M("~20 mL O2 per dL", 30, BLUE).move_to([0.9, 1.35, 0])
        c3 = T("(1 dL = 0.1 L)", 24, SOFT).move_to([0.9, 0.85, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), FadeIn(c3), run_time=0.7)
        self.at("maximum load")
        c1 = T("capacity (maximum load)", 32, RED).move_to([0.9, 2.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(tank, color=RED, scale_factor=1.04), run_time=1.0)
        self.at("the load actually carried")
        car = T("carried = capacity x saturation", 32, TEXT).move_to([0.9, 0.1, 0])
        self.play(FadeIn(car, shift=UP * 0.1), f.animate.set_value(S_LUNG), L.animate.set_value(S_LUNG), run_time=2.0)
        self.at("capacity times saturation")
        self.play(Indicate(car, color=BLUE), run_time=1.0)
        self.at("hemoglobin releases")
        e1 = T("oxygen released from hemoglobin =", 30, TEXT).move_to([0.9, -0.85, 0])
        e2 = T("capacity x (saturation in lungs - saturation in tissue)", 30, TEXT).move_to([0.9, -1.45, 0])
        fit(VGroup(e1, e2), max_w=9.2)
        self.play(Write(e1), run_time=0.8)
        self.play(Write(e2), run_time=1.1)
        self.at("capacity times the drop")
        self.play(Indicate(e2, color=GOLD), run_time=1.0)
        self.at("in saturation")
        note = T("+ a little dissolved O2", 24, SOFT).move_to([0.9, -2.1, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.at("from lung to tissue")
        self.play(f.animate.set_value(S_REST), run_time=2.2)
        self.at("that drop is the gap")
        dl, dt = pdot(P_LUNG, S_LUNG, BLUE), pdot(P_REST, S_REST, SOFT)
        br = bracket(P_LUNG, S_LUNG, P_REST, S_REST)
        dlab = T("the drop", 32, GOLD).move_to([1.7, 1.55, 0])
        self.play(FadeOut(VGroup(c1, c2, c3, car)), FadeIn(VGroup(dl, dt)), run_time=0.8)
        self.play(Create(br), FadeIn(dlab), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Loose(SpokenScene):
    def construct(self):
        motes(self, 12, 16)
        self.add(axes_y(), axes_x(), band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35),
                 lung_label(), tis_label(), tank_label())
        f = ValueTracker(S_LUNG)
        tank = always_redraw(lambda: tank_mob(f.get_value(), f.get_value()))
        self.add(tank)
        self.at("try a simple carrier")
        cart = hb_block(1.5, 1.1, TEAL, rounded=False, fill=0.3, slot_r=0.2)
        for s in cart.slots[1:]:
            s.set_opacity(0)
        cart.slots[0].move_to(cart.body.get_center())
        cart.move_to([-2.0, 0.85, 0])
        cl = T("one-site carrier", 30, TEAL).move_to([-2.0, 1.8, 0])
        self.play(FadeIn(cart, scale=0.8), FadeIn(cl), run_time=1.0)
        self.at("one binding site")
        self.play(Indicate(cart.slots[0], color=BLUE, scale_factor=1.5), run_time=1.0)
        self.at("loose grip")
        lc = loose_curve()
        self.play(Create(lc), run_time=1.3)
        self.at("half full")
        hd = pdot(26.8, 0.5, TEAL)
        hg = DashedLine([PX0, py(0.5), 0], [px(26.8), py(0.5), 0], color=TEAL, stroke_width=3)
        hl = T("half full", 30, TEAL).move_to([px(26.8) + 1.6, py(0.5) - 0.45, 0])
        self.play(Create(hg), FadeIn(hd), FadeIn(hl), run_time=1.0)
        self.at("in the lungs")
        self.play(FadeOut(VGroup(cart, cl, hg, hl, hd)), run_time=0.5)
        ld = pdot(P_LUNG, float(one(P_LUNG, 26.8)), TEAL)
        lv = T("79%", 30, TEAL).move_to([px(P_LUNG) + 0.95, py(float(one(P_LUNG, 26.8))) - 0.45, 0])
        self.play(FadeIn(ld, scale=2), FadeIn(lv), f.animate.set_value(float(one(P_LUNG, 26.8))), run_time=1.5)
        ar = Arrow([-2.7, 1.8, 0], [-5.35, 1.8, 0], color=SOFT, stroke_width=4, buff=0)
        em = T("rides around empty", 30, TEXT).move_to([-0.6, 1.8, 0])
        self.play(FadeIn(em), Create(ar), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tight_scene(scene, with_dot_label=True):
    scene.add(axes_y(), axes_x(), band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35),
              lung_label(), tis_label(), tank_label())
    s = float(one(P_LUNG, 3.0))
    scene.add(tank_mob(s, s), tight_curve(), pdot(P_LUNG, s, BLUE),
              T("97%", 30, BLUE).move_to([px(P_LUNG) + 0.95, py(s) - 0.45, 0]))


def question_card():
    box = RoundedRectangle(corner_radius=0.15, width=1.2, height=1.0, stroke_color=GOLD, stroke_width=4,
                           fill_color=BG, fill_opacity=1.0)
    q = T("?", 60, GOLD, weight=BOLD).move_to(box)
    return VGroup(box, q).move_to([px(P_REST), py(float(one(P_REST, 3.0))), 0]).set_z_index(8)


class S07Predict(SpokenScene):
    def construct(self):
        motes(self, 12, 17)
        self.add(axes_y(), axes_x(), band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35),
                 lung_label(), tis_label(), tank_label())
        tr = ValueTracker(26.8)
        v = lambda: tr.get_value()

        def cmob():
            return curve_mob(lambda p: one(p, v()), TEAL, 6, 0, 120, dashed=v() > 12)
        curve = always_redraw(cmob)
        ldot = always_redraw(lambda: pdot(P_LUNG, float(one(P_LUNG, v())), BLUE))
        llab = always_redraw(lambda: T(f"{one(P_LUNG, v()) * 100:.0f}%", 30, BLUE).move_to(
            [px(P_LUNG) + 0.95, py(float(one(P_LUNG, v()))) - 0.45, 0]))
        tank = always_redraw(lambda: tank_mob(float(one(P_LUNG, v())), float(one(P_LUNG, v()))))
        kc = [3.1, -1.4, 0]
        knob = Circle(radius=0.55, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.15).move_to(kc)
        ptr = always_redraw(lambda: Line(kc, [kc[0] + 0.5 * np.cos(PI / 2 - 1.9 * (26.8 - v()) / 23.8),
                                              kc[1] + 0.5 * np.sin(PI / 2 - 1.9 * (26.8 - v()) / 23.8), 0],
                                         color=TEAL, stroke_width=7))
        gl = T("grip", 32, TEAL).move_to([1.85, -1.4, 0])
        self.add(curve, ldot, llab, tank)
        self.at("tighten its grip")
        self.play(FadeIn(VGroup(knob, gl)), FadeIn(ptr), run_time=0.6)
        self.play(tr.animate.set_value(3.0), run_time=2.6, rate_func=smooth)
        self.at("what happens")
        card = question_card()
        self.play(FadeIn(card, scale=0.6), run_time=0.7)
        self.play(Indicate(card, color=GOLD, scale_factor=1.2), run_time=1.0)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        tight_scene(self)
        self.add(question_card())
        q = T("What happens when that blood reaches the tissue?", 32, GOLD).move_to([0, 3.4, 0])
        self.add(q)
        ring = Circle(radius=0.3, color=GOLD, stroke_width=6).move_to([6.3, 3.35, 0]).rotate(PI / 2)
        self.add(Circle(radius=0.3, color=GREY, stroke_width=3).move_to([6.3, 3.35, 0]))
        self.play(Create(ring), run_time=4.6, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Reveal(SpokenScene):
    def construct(self):
        motes(self, 12, 18)
        tight_scene(self)
        card = question_card()
        self.add(card)
        sl, st = float(one(P_LUNG, 3.0)), float(one(P_REST, 3.0))
        self.at("it holds on")
        td = pdot(P_REST, st, SOFT)
        tl = T("93%", 30, SOFT).move_to([px(P_REST), py(st) - 0.55, 0])
        self.play(FadeOut(card, shift=UP * 0.3), FadeIn(td, scale=2), FadeIn(tl), run_time=1.0)
        self.at("at tissue pressure")
        self.play(Indicate(td, color=GREY, scale_factor=2.0), run_time=1.0)
        self.at("almost nothing")
        br = bracket(P_LUNG, sl, P_REST, st)
        bl = T("< 1 mL per dL released", 30, GOLD).move_to([XB + 0.3, 0.8, 0])
        self.play(Create(br), run_time=1.0)
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.7)
        self.at("between lung and tissue pressures")
        sm = T("between 100 and 40 mmHg", 26, SOFT).move_to([1.1, -2.2, 0])
        self.play(FadeIn(sm), run_time=0.6)
        self.at("trade off")
        c1 = chip("loose grip: fills only to ~4/5", TEAL, 28).move_to([1.1, -0.05, 0])
        c2 = chip("tight grip: stays nearly full", TEAL, 28).move_to([1.1, -1.2, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.at("fill well")
        self.play(Indicate(c2, color=TEAL, scale_factor=1.1), run_time=0.9)
        self.at("give up a lot")
        self.play(Indicate(c1, color=TEAL, scale_factor=1.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ghosts(op=0.22):
    a, b = loose_curve(), tight_curve()
    return VGroup(a, b).set_stroke(opacity=op)


class S10Scurve(SpokenScene):
    def construct(self):
        motes(self, 12, 19)
        self.add(axes_y(), axes_x(), band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35),
                 lung_label(), tis_label(), tank_label())
        s = float(one(P_LUNG, 3.0))
        self.add(tank_mob(S_LUNG, S_LUNG))
        gh = VGroup(loose_curve(), tight_curve())
        self.add(gh)
        self.play(gh.animate.set_stroke(opacity=0.22), run_time=1.6)
        self.at("its curve is s shaped")
        pr = ValueTracker(0.5)
        rc = always_redraw(lambda: sev_curve(8, pr.get_value()))
        self.add(rc)
        self.play(pr.animate.set_value(120.0), run_time=4.1, rate_func=linear)
        lab = T("adult human blood", 32, RED).move_to([1.7, -0.4, 0])
        self.at("nearly flat")
        flat = curve_mob(sev, YELLOW, 14, 70.0, 112.0)
        self.play(FadeIn(flat), run_time=0.5)
        self.play(flat.animate.set_stroke(opacity=0.5), run_time=0.8)
        self.at("below that")
        steep = curve_mob(sev, YELLOW, 14, 14.0, 42.0)
        self.play(ReplacementTransform(flat, steep), FadeIn(lab, shift=UP * 0.1), run_time=1.0)
        self.at("falls steeply")
        self.play(Indicate(steep, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s_world(scene, rc=True, rest=True):
    scene.add(axes_y(), axes_x(), band(P_LUNG, BLUE, 0.22), lung_label(), tank_label(), ghosts())
    if rest:
        scene.add(band(P_REST, GREY, 0.35))
    if rc:
        scene.add(sev_curve())


class S11Rest(SpokenScene):
    def construct(self):
        motes(self, 12, 20)
        s_world(self)
        self.add(tis_label())
        t = ValueTracker(S_LUNG)
        tank = always_redraw(lambda: tank_mob(t.get_value(), S_LUNG))
        self.add(tank)
        ld = pdot(P_LUNG, S_LUNG, BLUE)
        lv = T("97.7%", 30, BLUE).move_to([5.2, 1.55, 0])
        self.play(FadeIn(ld, scale=2), FadeIn(lv), run_time=0.9)
        self.at("the tissue point")
        td = pdot(P_REST, S_REST, SOFT)
        tl = T("74.9%", 30, SOFT).move_to([px(P_REST) + 1.0, py(S_REST) - 0.4, 0])
        self.play(FadeIn(td, scale=2), FadeIn(tl), run_time=0.9)
        self.at("the shoulder")
        sh = T("the shoulder", 30, YELLOW).move_to([px(P_REST) + 1.0, py(S_REST) - 1.0, 0])
        self.play(FadeIn(sh, shift=UP * 0.1), Indicate(td, color=YELLOW, scale_factor=2.2), run_time=1.0)
        self.at("where the steep part begins")
        steep = curve_mob(sev, YELLOW, 14, 14.0, 42.0)
        self.play(Create(steep), run_time=1.2)
        self.play(steep.animate.set_stroke(opacity=0.0), run_time=0.8)
        self.at("blood gives up")
        br = bracket(P_LUNG, S_LUNG, P_REST, S_REST)
        self.play(Create(br), t.animate.set_value(S_REST), run_time=1.3)
        self.at("about a quarter")
        ql = T("about a quarter", 32, GOLD).move_to([XB + 0.3, py(S_REST) - 0.5, 0])
        self.play(FadeIn(ql, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(br[2], color=GOLD), run_time=1.0)
        self.finish()


class S12Work(SpokenScene):
    def construct(self):
        motes(self, 12, 21)
        s_world(self, rest=False)
        pt = ValueTracker(P_REST)
        P = lambda: pt.get_value()
        S = lambda: float(sev(P()))
        grey_band = always_redraw(lambda: band(P(), GREY, 0.35))
        tank = always_redraw(lambda: tank_mob(S(), S_LUNG))
        tdot = always_redraw(lambda: pdot(P(), S(), SOFT))
        tlab = always_redraw(lambda: T(f"{S() * 100:.1f}%", 30, SOFT).move_to([px(P()) + 1.0, py(S()) - 0.4, 0]))
        brk = always_redraw(lambda: bracket(P_LUNG, S_LUNG, P(), S()))
        rl = tis_label()
        ql = T("about a quarter", 32, GOLD).move_to([XB + 0.3, py(S_REST) - 0.5, 0])
        ld = pdot(P_LUNG, S_LUNG, BLUE)
        lv = T("97.7%", 30, BLUE).move_to([5.2, 1.55, 0])
        self.add(grey_band, tank, tdot, tlab, brk, rl, ql, ld, lv)
        self.at("three quarters")
        self.play(Indicate(tank, color=BLUE, scale_factor=1.05), FadeOut(ql), run_time=1.2)
        self.at("a reserve")
        rv = T("unused: a reserve", 32, BLUE).move_to([1.3, -0.4, 0])
        self.play(FadeIn(rv, shift=UP * 0.1), run_time=0.7)
        self.at("in hard work")
        self.play(FadeOut(rv), run_time=0.4)
        self.play(pt.animate.set_value(P_WORK), run_time=5.4, rate_func=smooth)
        rl2 = tis_label("hard-working tissue: ~20 mmHg", P_WORK)
        self.play(Transform(rl, rl2), run_time=0.8)
        self.at("now the same blood")
        self.play(Indicate(brk[2], color=GOLD, scale_factor=1.05), run_time=0.8)
        self.at("about two thirds")
        ql2 = T("about two-thirds released", 30, GOLD).move_to([XB, py(S_WORK) - 0.55, 0])
        self.play(FadeIn(ql2, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13Coop(SpokenScene):
    def construct(self):
        motes(self, 10, 22)
        sc = curve_mob(sev, RED, 9).scale(0.85).move_to([0, -0.3, 0])
        why = T("Why the S?", 50, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.play(Create(sc), FadeIn(why), run_time=2.0)
        self.at("hemoglobin has")
        blk = hb_block(4.2, 2.8, GREY, rounded=False, fill=0.3, slot_r=0.3).move_to([0, 0.3, 0])
        hl = T("hemoglobin", 34, RED).move_to([0, 2.3, 0])
        self.play(FadeOut(sc), FadeOut(why), FadeIn(blk, scale=0.85), FadeIn(hl), run_time=1.0)
        self.at("four binding sites")
        for s in blk.slots:
            self.play(Indicate(s, color=BLUE, scale_factor=1.35), run_time=0.45)
        bl = T("four binding sites", 32, TEXT).move_to([0, -1.9, 0])
        self.play(FadeIn(bl), run_time=0.5)
        self.at("in a simple picture")
        tag = T("simple picture", 30, GOLD).move_to([0, 3.15, 0])
        self.play(FadeOut(bl), FadeIn(tag), run_time=0.6)
        self.at("the molecule switches shape")
        a = hb_block(3.4, 2.6, GREY, rounded=False, fill=0.3, slot_r=0.26).move_to([-3.2, 0.5, 0])
        b = hb_block(3.4, 2.6, RED, rounded=True, fill=0.4, slot_r=0.26).move_to([3.2, 0.5, 0])
        al = T("low-affinity shape", 28, TEXT).move_to([-3.2, -1.2, 0])
        bl2 = T("high-affinity shape", 28, RED).move_to([3.2, -1.2, 0])
        arr = DoubleArrow([-1.1, 0.5, 0], [1.1, 0.5, 0], color=SOFT, stroke_width=5, buff=0)
        self.play(ReplacementTransform(blk, a), FadeOut(hl), FadeIn(b), FadeIn(arr), FadeIn(al), FadeIn(bl2), run_time=1.4)
        self.at("as a whole")
        self.play(Indicate(a, color=GREY, scale_factor=1.06), Indicate(b, color=RED, scale_factor=1.06), run_time=1.2)
        self.at("each oxygen")
        self.play(FadeOut(VGroup(a, b, al, bl2, arr, tag)), run_time=0.6)
        xs = [-4.8, -1.6, 1.6, 4.8]
        snaps = []
        bars = []
        for k, x in enumerate(xs):
            blk_k = hb_block(2.4, 1.8, GREY, rounded=False, fill=0.3, slot_r=0.2).move_to([x, 1.2, 0])
            ds = VGroup(*[o2dot(blk_k.slots[i].get_center(), 0.16) for i in range(k)])
            track = Rectangle(width=0.7, height=1.7, stroke_color=SOFT, stroke_width=3).move_to([x, -1.35, 0])
            hh = 0.2 + 0.43 * k
            fill = Rectangle(width=0.7, height=hh, stroke_width=0, fill_color=RED, fill_opacity=0.85).move_to([x, -2.2 + hh / 2, 0])
            snaps.append(VGroup(blk_k, ds, track, fill))
        self.play(FadeIn(snaps[0], scale=0.9), run_time=0.8)
        self.at("that binds")
        self.play(FadeIn(snaps[1], scale=0.9), run_time=0.8)
        cap = T("chance of the high-affinity shape", 28, RED).move_to([0, -3.15, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.at("the switch to")
        self.play(FadeIn(snaps[2], scale=0.9), run_time=0.8)
        self.at("more likely")
        self.play(FadeIn(snaps[3], scale=0.9), run_time=0.8)
        self.finish()


class S14Coop2(SpokenScene):
    def construct(self):
        motes(self, 10, 23)
        P = ValueTracker(0.0)
        nfill = lambda: int(round(4 * float(sev(P.get_value()))))
        blk = hb_block(3.6, 2.8, GREY, rounded=False, fill=0.3, slot_r=0.3).move_to([-3.5, 1.1, 0])
        bl = T("four-site hemoglobin", 30, TEXT).move_to([-3.5, 3.05, 0])
        fills = always_redraw(lambda: VGroup(*[o2dot(blk.slots[i].get_center(), 0.26) for i in range(nfill())]))
        # gauge
        gx0, gx1, gy = -5.6, -1.4, -1.5
        track = Line([gx0, gy, 0], [gx1, gy, 0], color=GREY, stroke_width=6)
        marker = always_redraw(lambda: Triangle(color=BLUE, fill_opacity=1).scale(0.2).rotate(PI).move_to(
            [gx0 + (gx1 - gx0) * P.get_value() / 60.0, gy + 0.3, 0]))
        glab = always_redraw(lambda: M(f"PO2 = {P.get_value():.0f} mmHg", 30, BLUE).move_to([-3.5, -2.3, 0]))
        note = T("at balance, one pressure at a time", 26, SOFT).move_to([-3.5, -3.05, 0])
        # compact S curve
        cx0, cw, cy0, ch = 0.7, 5.4, -2.4, 4.8
        cpx = lambda p: cx0 + p / 120.0 * cw
        cpy = lambda s: cy0 + s * ch
        ax = VGroup(Line([cx0, cy0, 0], [cx0, cy0 + ch + 0.2, 0], color=GREY, stroke_width=3),
                    Line([cx0, cy0, 0], [cx0 + cw + 0.1, cy0, 0], color=GREY, stroke_width=3),
                    T("saturation", 26, TEXT).rotate(PI / 2).move_to([cx0 - 0.45, cy0 + ch / 2, 0]),
                    T("PO2", 26, TEXT).move_to([cx0 + cw / 2, cy0 - 0.45, 0]))
        pts = [[cpx(p), cpy(float(sev(p))), 0] for p in np.linspace(0, 120, 100)]
        cur = VMobject(stroke_color=RED, stroke_width=7)
        cur.set_points_smoothly(pts)
        cdot = always_redraw(lambda: Dot([cpx(P.get_value()), cpy(float(sev(P.get_value()))), 0], radius=0.17, color=BLUE).set_z_index(5))
        self.play(FadeIn(blk), FadeIn(bl), Create(track), FadeIn(ax), Create(cur), run_time=1.2)
        self.add(fills, marker, glab, cdot)
        self.play(FadeIn(note), run_time=0.4)
        self.at("hold oxygen")
        self.play(P.animate.set_value(20.0), run_time=0.7)
        self.at("the rest fill")
        self.play(P.animate.set_value(40.0), run_time=0.7)
        self.wait(0.3)
        self.at("smaller rise")
        self.play(P.animate.set_value(60.0), run_time=0.7)
        self.at("emptying")
        self.play(P.animate.set_value(40.0), run_time=0.7)
        self.wait(0.2)
        self.play(P.animate.set_value(20.0), run_time=0.7)
        self.wait(0.2)
        self.play(P.animate.set_value(0.0), run_time=0.7)
        self.at("cooperative binding")
        steep = VMobject(stroke_color=YELLOW, stroke_width=14)
        steep.set_points_smoothly([[cpx(p), cpy(float(sev(p))), 0] for p in np.linspace(15, 45, 30)])
        cl = T("cooperative binding", 38, YELLOW).move_to([3.2, 3.1, 0])
        self.play(FadeIn(steep), FadeIn(cl, shift=DOWN * 0.1), run_time=0.9)
        self.play(Indicate(steep, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15Close(SpokenScene):
    def construct(self):
        motes(self, 12, 24)
        self.add(axes_y(), axes_x(), band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.3), band(P_WORK, GREY, 0.3),
                 tank_label())
        self.add(lung_label("lungs"), T("rest", 28, TEXT).move_to([px(P_REST), 2.75, 0]),
                 T("hard work", 28, TEXT).move_to([px(P_WORK) - 0.3, 2.75, 0]))
        q = ValueTracker(P_LUNG)
        Q = lambda: q.get_value()
        tank = always_redraw(lambda: tank_mob(float(sev(Q())), S_LUNG))
        self.add(tank)
        rc = sev_curve()
        self.play(Create(rc), run_time=2.2)
        self.at("a one site carrier cannot")
        gh = ghosts(0.0)
        self.add(gh)
        self.play(gh.animate.set_stroke(opacity=0.4), run_time=0.6)
        tr = ValueTracker(P_LUNG)
        td = always_redraw(lambda: pdot(tr.get_value(), float(one(tr.get_value(), 3.0)), TEAL, 0.14))
        self.add(td)
        self.play(tr.animate.set_value(P_REST), run_time=1.8, rate_func=linear)
        self.remove(td)
        tr2 = ValueTracker(P_LUNG)
        td2 = always_redraw(lambda: pdot(tr2.get_value(), float(one(tr2.get_value(), 26.8)), TEAL, 0.14))
        self.add(td2)
        self.play(tr2.animate.set_value(P_REST), run_time=1.8, rate_func=linear)
        self.remove(td2)
        self.play(gh.animate.set_stroke(opacity=0.22), run_time=0.4)
        self.at("cooperative binding")
        ld = pdot(P_LUNG, S_LUNG, BLUE)
        red = always_redraw(lambda: pdot(Q(), float(sev(Q())), RED, 0.17))
        brk = always_redraw(lambda: bracket(P_LUNG, S_LUNG, Q(), float(sev(Q()))) if Q() < 95 else VGroup())
        self.add(ld, red, brk)
        self.play(q.animate.set_value(P_REST), run_time=2.0, rate_func=smooth)
        self.at("load fully in the lungs")
        self.play(Indicate(ld, color=BLUE, scale_factor=2.2), run_time=1.0)
        self.at("still unload a lot")
        self.play(q.animate.set_value(P_WORK), run_time=2.2, rate_func=smooth)
        self.play(Indicate(brk, color=GOLD, scale_factor=1.03), run_time=1.0)
        self.finish()


class S16End(EndCard):
    LINE = "An S-curve lets one carrier load fully and unload a lot."
