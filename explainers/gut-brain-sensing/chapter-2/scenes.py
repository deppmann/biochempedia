"""How the Gut Teaches Preference  (chapter 2 of gut-brain-sensing)

COLOR MAP (same as chapter 1)
  GOLD  = gut sensor cell (and sugar)        BLUE = vagal neuron / axon
  TEAL  = glutamate / lumen                  GREY = diffuse hormone / sweetener
  WHITE (TEXT) = unidentified, fat           GREEN = active / restored
  RED   = blocked or silenced                VIO = taste (tongue) route
Bars and gauges are schematic unless labelled "computed" (40.8 and 8.9 points come from the lesson).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

_ic = interpolate_color


def interpolate_color(a, b, t):
    return _ic(ManimColor(a), ManimColor(b), t)


WHITE = TEXT
VIO = "#B48EF0"
AMINO = "#E58FB5"
V = lambda x, y: np.array([x, y, 0.0])

# ----------------------------------------------------------------- carried world geometry
VAG = CubicBezier(V(-4.4, -1.85), V(-4.4, -0.2), V(-2.2, 0.7), V(0.8, 0.7))
MOUTH = V(3.6, 0.7)
BOT_S, BOT_W = V(4.1, 2.55), V(5.9, 2.55)
T_S = CubicBezier(V(4.1, 1.95), V(4.1, 1.5), V(3.9, 1.1), MOUTH)
T_W = CubicBezier(V(5.9, 1.95), V(5.9, 1.4), V(4.4, 1.2), MOUTH)
BASE = -2.9          # baseline of the time strip
X_LICK = (0.0, 0.9)
X_PREF = (4.4, 5.5)
PREF_H = 1.6


def hl(m, c, w, op=1.0):
    m.set_stroke(c, w, opacity=op)
    return m


def travelers(path, n=4, color=BLUE, speed=0.18, r=0.1):
    g = VGroup()
    for i in range(n):
        d = Dot(radius=r, color=color)
        d.t = i / n
        d.move_to(path.point_from_proportion(d.t))

        def up(m, dt, path=path, speed=speed):
            m.t = (m.t + dt * speed) % 1
            m.move_to(path.point_from_proportion(m.t))
        d.add_updater(up)
        g.add(d)
    return g


def drift_dots(n, x0, x1, y0, y1, color=GOLD, seed=1, r=0.09, speed=0.6, kinds=None):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for i in range(n):
        c = color if kinds is None else kinds[i % len(kinds)][0]
        rr = r if kinds is None else kinds[i % len(kinds)][1]
        d = Dot(radius=rr, color=c).move_to([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        d.v = np.array([rng.uniform(0.3, 0.7) * speed * (1 if rng.rand() > 0.3 else -1), rng.uniform(-0.25, 0.25), 0])

        def up(m, dt, x0=x0, x1=x1, y0=y0, y1=y1):
            m.shift(m.v * dt)
            p = m.get_center()
            if p[0] > x1:
                m.move_to([x0, p[1], 0])
            if p[0] < x0:
                m.move_to([x1, p[1], 0])
            if p[1] > y1 or p[1] < y0:
                m.v[1] *= -1
                m.shift(np.array([0, m.v[1] * dt * 2, 0]))
        d.add_updater(up)
        g.add(d)
    return g


def mouse():
    body = Ellipse(width=4.4, height=2.4, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.28).move_to(V(0.1, 0.45))
    head = Circle(radius=0.9, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.28).move_to(V(2.7, 0.75))
    ear = Circle(radius=0.36, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.28).move_to(V(2.35, 1.65))
    eye = Dot(V(3.05, 1.0), radius=0.07, color=TEXT)
    tail = ArcBetweenPoints(V(-2.0, 0.9), V(-3.3, 2.0), angle=-1.0).set_stroke(TEXT, 5)
    return VGroup(tail, body, head, ear, eye)


def gut_small():
    lumen = Rectangle(width=4.6, height=0.9, stroke_width=0, fill_color=TEAL, fill_opacity=0.3).move_to(V(-4.3, -3.35))
    tissue = Rectangle(width=4.6, height=1.0, stroke_width=0, fill_color=GREY, fill_opacity=0.3).move_to(V(-4.3, -2.4))
    cell = RoundedRectangle(width=1.2, height=1.5, corner_radius=0.25, stroke_color=GOLD, stroke_width=5,
                            fill_color=GOLD, fill_opacity=0.38).move_to(V(-4.4, -2.55))
    cell.t = 0.0
    cell.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_fill(m.get_fill_color() if False else GOLD, 0.38 + 0.1 * np.sin(m.t * 2.5))))
    return lumen, tissue, cell


def sugar_lumen(seed=3):
    return drift_dots(7, -6.4, -2.2, -3.7, -3.05, GOLD, seed, 0.09, 0.5)


def bottles(label=True):
    g = VGroup()
    for p, c in ((BOT_S, GOLD), (BOT_W, GREY)):
        g.add(RoundedRectangle(width=0.9, height=1.2, corner_radius=0.2, stroke_color=c, stroke_width=4,
                               fill_color=c, fill_opacity=0.35).move_to(p))
    if label:
        g.add(T("sugar", 28, GOLD).move_to(BOT_S + V(0.0, 0.9)), T("sweetener", 28, TEXT).move_to(BOT_W + V(0.0, 0.9)))
    return g


def tongue_routes(color=VIO):
    return VGroup(hl(T_S.copy(), color, 7), hl(T_W.copy(), color, 7))


def bar(x, color, tr, w=0.6, scale=1.0, base=BASE):
    def b():
        h = max(tr.get_value() * scale, 0.001)
        c = color() if callable(color) else color
        r = Rectangle(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.95)
        r.move_to([x, base + h / 2, 0])
        return r
    return always_redraw(b)


def frame_rect(x, h=PREF_H, w=0.8):
    return Rectangle(width=w, height=h, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.6, fill_opacity=0).move_to([x, BASE + h / 2, 0])


def strip_axis():
    line = Arrow(V(-0.8, BASE), V(6.5, BASE), buff=0, stroke_width=5, color=TEXT, max_tip_length_to_length_ratio=0.05)
    l1 = T("first sip", 28, TEXT).move_to(V(0.5, -3.45))
    l2 = T("later choice", 28, TEXT).move_to(V(5.0, -3.45))
    return VGroup(line, l1, l2)


def x_cross(center, size=0.4, color=RED, w=9):
    return VGroup(Line(center + V(-size, -size), center + V(size, size)), Line(center + V(-size, size), center + V(size, -size))).set_stroke(color, w)


class Base(SpokenScene):
    def clock(self):
        self.ph = ValueTracker(0.0)
        self.ph.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.ph)

    # carried world pieces ------------------------------------------------
    def carried(self, tongue=True, bottle_labels=True, tongue_color=VIO, dots=True, vag_travel=True):
        self.mouse = mouse()
        self.lumen, self.tissue, self.cell = gut_small()
        self.vag = hl(VAG.copy(), BLUE, 12)
        self.bulb = Dot(V(0.8, 0.7), radius=0.2, color=BLUE)
        self.cell_lab = T("gut cell", 28, GOLD).move_to(V(-5.9, -2.45))
        self.gut = VGroup(self.lumen, self.tissue, self.cell, self.cell_lab)
        self.add(self.mouse, self.gut)
        if dots:
            self.sdots = sugar_lumen()
            self.add(self.sdots)
        self.add(self.vag, self.bulb)
        if vag_travel:
            self.vtr = travelers(VAG, 5, BLUE, 0.2, 0.13)
            self.add(self.vtr)
        if tongue:
            self.bot = bottles(bottle_labels)
            self.tr = tongue_routes(tongue_color)
            self.ttr = VGroup(travelers(T_S, 3, tongue_color, 0.2, 0.1), travelers(T_W, 3, tongue_color, 0.2, 0.1))
            self.add(self.tr, self.bot, self.ttr)


# =========================================================================== scenes
class S00Hook(Base):
    def construct(self):
        self.clock()
        mo = mouse()
        lumen, tissue, cell = gut_small()
        vag = hl(VAG.copy(), BLUE, 12)
        bulb = Dot(V(0.8, 0.7), radius=0.2, color=BLUE)
        sd = sugar_lumen()
        self.play(FadeIn(mo), FadeIn(lumen), FadeIn(tissue), GrowFromCenter(cell), run_time=1.5)
        self.add(sd)
        lab = T("gut cell", 28, GOLD).move_to(V(-5.9, -2.45))
        self.play(FadeIn(lab), run_time=0.5)
        self.at("route from")
        self.play(Create(vag), FadeIn(bulb), run_time=1.5)
        self.add(travelers(VAG, 5, BLUE, 0.2, 0.13))
        qm = T("?", 90, WHITE, weight=BOLD).move_to(V(0.8, 0.75))
        self.at("How can")
        bot = bottles(True)
        tr = tongue_routes()
        self.play(FadeIn(bot), Create(tr), run_time=1.5)
        self.add(VGroup(travelers(T_S, 3, VIO, 0.2, 0.1), travelers(T_W, 3, VIO, 0.2, 0.1)))
        self.at("when sweet taste")
        self.play(tr.animate.set_stroke(opacity=0.35), run_time=0.8)
        self.at("absent")
        self.play(FadeIn(qm, scale=1.6), run_time=0.8)
        qm.t = 0.0

        def qup(m, dt):
            m.t += dt
            m.set_opacity(0.6 + 0.4 * np.sin(m.t * 4))
        qm.add_updater(qup)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Sensing the Gut: Enteroendocrine Cells and Nutrient Signals"
    TITLE = "How the Gut Teaches Preference"


class S02TwoMeasures(Base):
    def construct(self):
        self.clock()
        self.carried(bottle_labels=True)
        self.qm = None
        axis = strip_axis()
        lick_t = ValueTracker(0.0)
        lk = VGroup(bar(X_LICK[0], GOLD, lick_t), bar(X_LICK[1], GREY, lick_t))
        pf = VGroup(frame_rect(X_PREF[0]), frame_rect(X_PREF[1]))
        self.at("First")
        self.play(Create(axis[0]), run_time=1.2)
        self.play(FadeIn(axis[1]), FadeIn(axis[2]), run_time=0.6)
        self.at("Initial attraction")
        lab_i = T("initial attraction", 28, VIO).move_to(V(5.1, -0.1))
        self.add(lk)
        self.play(FadeIn(lab_i), self.tr.animate.set_stroke(width=11), run_time=0.8)
        self.at("first sip")
        self.play(lick_t.animate.set_value(0.6), run_time=1.8, rate_func=linear)
        self.play(self.tr.animate.set_stroke(width=7), run_time=0.4)
        self.at("Learned")
        lab_p = T("post-ingestive learning", 28, BLUE).move_to(V(-3.6, 2.95))
        self.play(FadeIn(pf), FadeIn(lab_p), self.vag.animate.set_stroke(width=18), run_time=1.0)
        self.at("signals arrive")
        self.play(self.cell.animate.set_stroke(width=9), run_time=1.0)
        self.play(self.vag.animate.set_stroke(width=12), self.cell.animate.set_stroke(width=5), run_time=0.8)
        self.finish()


class S03Matched(Base):
    def construct(self):
        self.clock()
        self.carried()
        axis = strip_axis()
        lick_t = ValueTracker(0.6)
        lk = VGroup(bar(X_LICK[0], GOLD, lick_t), bar(X_LICK[1], GREY, lick_t))
        pref_s, pref_w = ValueTracker(0.0), ValueTracker(0.0)
        pf = VGroup(frame_rect(X_PREF[0]), frame_rect(X_PREF[1]))
        pb = VGroup(bar(X_PREF[0], GOLD, pref_s, 0.8, PREF_H), bar(X_PREF[1], GREY, pref_w, 0.8, PREF_H))
        lab_i = T("initial attraction", 28, VIO).move_to(V(5.1, -0.1))
        lab_p = T("post-ingestive learning", 28, BLUE).move_to(V(-3.6, 2.95))
        self.add(axis, lk, pf, pb, lab_i, lab_p)
        eq = T("=", 44, TEXT).move_to(V(0.45, -1.7))
        self.at("matched")
        self.play(lick_t.animate.set_value(0.9), run_time=2.5, rate_func=linear)
        self.at("Naive mice")
        self.play(FadeIn(eq), lick_t.animate.set_value(1.2), run_time=3.0, rate_func=linear)
        sch = T("schematic time course", 28, TEXT).move_to(V(2.6, -1.0))
        hand = Triangle(color=TEXT, fill_opacity=1).scale(0.18).rotate(PI).move_to(V(-0.8, BASE + 0.3))
        self.at("Then")
        self.play(FadeIn(sch), FadeIn(hand), FadeOut(eq), run_time=0.6)
        self.play(hand.animate.move_to(V(6.3, BASE + 0.3)), pref_s.animate.set_value(0.95), pref_w.animate.set_value(0.15),
                  run_time=2.6, rate_func=linear)
        self.finish()


class S04Predict(Base):
    def construct(self):
        self.clock()
        self.carried()
        axis = strip_axis()
        lick_t = ValueTracker(1.2)
        lk = VGroup(bar(X_LICK[0], GOLD, lick_t), bar(X_LICK[1], GREY, lick_t))
        pref_s, pref_w = ValueTracker(0.95), ValueTracker(0.15)
        pf = VGroup(frame_rect(X_PREF[0]), frame_rect(X_PREF[1]))
        pb = VGroup(bar(X_PREF[0], GOLD, pref_s, 0.8, PREF_H), bar(X_PREF[1], GREY, pref_w, 0.8, PREF_H))
        lab_i = T("initial attraction", 28, VIO).move_to(V(5.1, -0.1))
        self.add(axis, lk, pf, pb, lab_i)
        # a repeating sweep keeps the strip alive
        hand = Triangle(color=TEXT, fill_opacity=1).scale(0.18).rotate(PI).move_to(V(-0.8, BASE + 0.3))
        hand.u = 0.0

        def hup(m, dt):
            m.u = (m.u + dt * 0.12) % 1
            m.move_to(V(-0.8 + 7.1 * m.u, BASE + 0.3))
        hand.add_updater(hup)
        self.add(hand)
        self.at("Suppose")
        self.play(Indicate(pb[0], color=GOLD, scale_factor=1.1), run_time=1.5)
        q = VGroup(T("No sweet-taste signal:", 32, TEXT), T("does sugar preference develop?", 32, TEXT)).arrange(DOWN, buff=0.15)
        fit(q, max_w=6.4)
        q.move_to(V(-3.5, 3.05))
        self.at("What should happen")
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.8)
        self.at("cannot signal")
        cr = x_cross(V(4.4, 1.5), 0.4)
        self.play(self.tr.animate.set_color(RED), self.ttr.animate.set_color(RED), Create(cr), run_time=1.0)
        self.at("during the choice")
        self.play(pref_s.animate.set_value(0.0), pref_w.animate.set_value(0.0), run_time=1.2)
        self.finish()


class S05Pause(Base):
    def construct(self):
        self.clock()
        self.carried(tongue_color=RED)
        axis = strip_axis()
        lick_t = ValueTracker(1.2)
        lk = VGroup(bar(X_LICK[0], GOLD, lick_t), bar(X_LICK[1], GREY, lick_t))
        pf = VGroup(frame_rect(X_PREF[0]), frame_rect(X_PREF[1]))
        cr = x_cross(V(4.4, 1.5), 0.4)
        q = VGroup(T("No sweet-taste signal:", 32, TEXT), T("does sugar preference develop?", 32, TEXT)).arrange(DOWN, buff=0.15)
        fit(q, max_w=6.4)
        q.move_to(V(-3.5, 3.05))
        lab_i = T("initial attraction", 28, VIO).move_to(V(5.1, -0.1))
        self.add(axis, lk, pf, cr, q, lab_i)
        tick = Dot(V(0.0, -3.9 + 0.0), radius=0.01)
        hand = Triangle(color=TEXT, fill_opacity=1).scale(0.18).rotate(PI).move_to(V(-0.8, BASE + 0.3))
        self.add(hand)
        for i in range(1, 6):
            self.play(hand.animate.move_to(V(-0.8 + 1.4 * i, BASE + 0.3)), run_time=0.9, rate_func=linear)
        self.finish()


class S06Reveal(Base):
    def construct(self):
        self.clock()
        self.carried(tongue_color=RED)
        axis = strip_axis()
        lick_t = ValueTracker(1.2)
        lk = VGroup(bar(X_LICK[0], GOLD, lick_t), bar(X_LICK[1], GREY, lick_t))
        pref_s, pref_w = ValueTracker(0.0), ValueTracker(0.0)
        pf = VGroup(frame_rect(X_PREF[0]), frame_rect(X_PREF[1]))
        pb = VGroup(bar(X_PREF[0], GOLD, pref_s, 0.8, PREF_H), bar(X_PREF[1], GREY, pref_w, 0.8, PREF_H))
        cr = x_cross(V(4.4, 1.5), 0.4)
        self.add(axis, lk, pf, pb, cr)
        # a pulse from luminal sugar through the cell and up the vagus
        pulse = Dot(radius=0.2, color=GOLD)

        def route(a):
            if a < 0.2:
                return V(-4.4, -3.5) + (V(-4.4, -1.85) - V(-4.4, -3.5)) * (a / 0.2)
            return VAG.point_from_proportion((a - 0.2) / 0.8)
        self.at("It still")
        self.add(pulse)
        self.play(UpdateFromAlphaFunc(pulse, lambda m, a: m.move_to(route(a))), run_time=1.6, rate_func=linear)
        self.play(pref_s.animate.set_value(1.0), run_time=0.7)
        chk = Text("✓", font_size=70, color=GREEN, weight=BOLD).move_to(V(4.4, BASE + PREF_H + 0.5))
        self.play(FadeIn(chk, scale=1.5), run_time=0.3)
        self.at("Mice lacking")
        for _ in range(2):
            self.play(UpdateFromAlphaFunc(pulse, lambda m, a: m.move_to(route(a))), run_time=2.0, rate_func=linear)
        self.at("In mice")
        msg = VGroup(T("taste not required", 36, GREEN), T("for learned preference", 36, GREEN)).arrange(DOWN, buff=0.15).move_to(V(-3.5, 3.0))
        self.play(FadeIn(msg, shift=DOWN * 0.2), run_time=1.0)
        self.play(UpdateFromAlphaFunc(pulse, lambda m, a: m.move_to(route(a))), run_time=2.2, rate_func=linear)
        self.play(UpdateFromAlphaFunc(pulse, lambda m, a: m.move_to(route(a))), run_time=2.2, rate_func=linear)
        self.finish()


# ----------------------------------------------------------- big gut view (s07, s09)
CELL_B = V(-4.5, 0.95)
BIG_AX = CubicBezier(V(-4.5, -0.35), V(-4.5, -2.2), V(-1.5, -1.2), V(1.6, -1.2))


def big_gut(cell_color=GOLD):
    lumen = Rectangle(width=7.4, height=1.3, stroke_width=0, fill_color=TEAL, fill_opacity=0.3).move_to(V(-2.9, 3.15))
    tissue = Rectangle(width=7.4, height=3.0, stroke_width=0, fill_color=GREY, fill_opacity=0.25).move_to(V(-2.9, 0.85))
    neigh = VGroup(*[RoundedRectangle(width=1.4, height=2.4, corner_radius=0.3, stroke_color=GREY, stroke_width=2,
                                      fill_color=GREY, fill_opacity=0.3).move_to(V(x, 1.0)) for x in (-2.0, -0.2)])
    cell = RoundedRectangle(width=1.7, height=2.6, corner_radius=0.3, stroke_color=cell_color, stroke_width=5,
                            fill_color=cell_color, fill_opacity=0.4).move_to(CELL_B)
    axon = hl(BIG_AX.copy(), BLUE, 12)
    return lumen, tissue, neigh, cell, axon


class S07GutSignal(Base):
    def construct(self):
        self.clock()
        lumen, tissue, neigh, cell, axon = big_gut()
        cell.t = 0.0
        cell.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_fill(GOLD, 0.4 + 0.1 * np.sin(m.t * 2.5))))
        sg = RoundedRectangle(width=1.5, height=0.5, corner_radius=0.12, stroke_color=WHITE, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(V(-4.5, 2.2))
        sgl = T("SGLT1", 28, WHITE).move_to(sg)
        # gauge
        gx, gb, gh = 4.6, -2.3, 4.0
        gbox = Rectangle(width=1.4, height=gh, stroke_color=BLUE, stroke_width=4, fill_opacity=0).move_to(V(gx, gb + gh / 2))
        lev = ValueTracker(0.08)
        gfill = bar(gx, BLUE, lev, 1.4, gh, base=gb)
        glab = T("vagal response", 28, BLUE).move_to(V(gx, 2.2 + 0.0))
        sch = T("schematic", 28, TEXT).move_to(V(gx, -2.75))
        self.add(lumen, tissue, neigh, cell, axon, gbox, gfill, glab, sch)
        self.play(FadeIn(sg), FadeIn(sgl), run_time=0.6)
        vt = travelers(BIG_AX, 4, BLUE, 0.2, 0.12)
        self.add(vt)
        sdots = drift_dots(6, -6.4, -0.4, 2.7, 3.6, GOLD, 5, 0.12, 0.6)
        adots = drift_dots(6, -6.4, -0.4, 2.7, 3.6, GREY, 6, 0.12, 0.6)
        chip_g = solid_chip("sugar", GOLD, 28).move_to(V(-1.0, 3.2))
        chip_a = solid_chip("acesulfame K", GREY, 28).move_to(V(-1.0, 3.2))
        self.at("delivered sugar")
        self.add(sdots)
        self.play(FadeIn(chip_g), lev.animate.set_value(0.9), run_time=1.6)
        self.at("acesulfame K")
        self.play(FadeOut(sdots), FadeOut(chip_g), lev.animate.set_value(0.08), run_time=1.0)
        self.add(adots)
        self.play(FadeIn(chip_a), run_time=0.5)
        self.at("Blocking")
        self.play(FadeOut(adots), FadeOut(chip_a), run_time=0.6)
        self.add(sdots)
        self.play(FadeIn(chip_g), lev.animate.set_value(0.9), run_time=1.3)
        rb = VGroup(Rectangle(width=1.7, height=0.7, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.5), x_cross(V(0, 0), 0.3, RED, 8)).move_to(sg).shift(DOWN * 0.75)
        self.play(FadeIn(rb), run_time=0.6)
        self.at("sharply")
        self.play(lev.animate.set_value(0.2), run_time=1.5)
        self.at("Intestinal")
        need = T("SGLT1 needed", 34, TEXT).move_to(V(-1.2, -1.9))
        self.play(FadeIn(need, shift=UP * 0.2), Indicate(rb, color=RED), run_time=1.2)
        self.at("gut sugar signal")
        self.play(Indicate(gbox, color=BLUE, scale_factor=1.05), run_time=1.5)
        self.finish()


def solid_chip(text, color=TEXT, size=28, pad=0.22):
    c = chip(text, color, size, pad)
    c[0].set_fill(interpolate_color(BG, color, 0.2), opacity=1)
    return c


class S08Brainstem(Base):
    def construct(self):
        self.clock()
        self.carried()
        axis = strip_axis()
        lick_t = ValueTracker(1.2)
        lk = VGroup(bar(X_LICK[0], GOLD, lick_t), bar(X_LICK[1], GREY, lick_t))
        pref_s, pref_w = ValueTracker(1.0), ValueTracker(0.15)
        colw = ValueTracker(0.0)
        pf = VGroup(frame_rect(X_PREF[0]), frame_rect(X_PREF[1]))
        pb = VGroup(bar(X_PREF[0], GOLD, pref_s, 0.8, PREF_H),
                    bar(X_PREF[1], lambda: interpolate_color(GREY, GREEN, colw.get_value()), pref_w, 0.8, PREF_H))
        self.add(axis, lk, pf, pb)
        nA = Circle(radius=0.28, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.5).move_to(V(1.6, 0.2))
        nB = Circle(radius=0.28, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.5).move_to(V(1.6, 1.2))
        sA = hl(Line(V(0.8, 0.7), nA.get_center(), buff=0), BLUE, 6)
        sB = hl(Line(V(0.8, 0.7), nB.get_center(), buff=0), BLUE, 6)
        bs = T("brainstem", 28, TEXT).move_to(V(-1.0, 2.4))
        self.at("Silencing")
        self.play(FadeIn(nA), FadeIn(nB), Create(sA), Create(sB), FadeIn(bs), run_time=1.0)
        self.play(nA.animate.set_stroke(RED).set_fill(RED, 0.5), run_time=0.8)
        lA = T("silenced", 28, RED).move_to(V(1.9, -1.15))
        self.play(FadeIn(lA), run_time=0.4)
        self.at("prevents")
        self.play(pref_s.animate.set_value(0.0), run_time=1.5)
        self.at("leaves")
        box = SurroundingRectangle(lk, color=GREEN, buff=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.8)
        lI = T("unchanged", 28, GREEN).move_to(V(-0.6, -1.05))
        self.play(FadeIn(lI), run_time=0.5)
        self.at("Activating")
        self.play(FadeOut(box), FadeOut(lI), FadeOut(lA), run_time=0.5)
        self.play(nB.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), run_time=0.8)
        lB = T("activated", 28, GREEN).move_to(V(1.9, -1.15))
        self.play(FadeIn(lB), run_time=0.4)
        self.at("create preference")
        self.play(pref_w.animate.set_value(0.85), colw.animate.set_value(1.0), run_time=1.2)
        self.at("previously")
        lbl = T("low before", 28, TEXT).move_to(V(-1.0, -1.7))
        self.play(Indicate(pb[1], color=GREEN, scale_factor=1.15), run_time=1.5)
        self.play(pref_w.animate.set_value(1.1), run_time=1.5)
        self.finish()


class S09SensorCell(Base):
    def construct(self):
        self.clock()
        lumen, tissue, neigh, cell, axon = big_gut()
        cell.t = 0.0
        dim = ValueTracker(0.0)
        cell.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt),
                                        m.set_fill(interpolate_color(GOLD, RED, dim.get_value() * 0.8),
                                                   (0.4 + 0.1 * np.sin(m.t * 2.5)) * (1 - 0.6 * dim.get_value()))))
        sdots = drift_dots(6, -6.4, -0.4, 2.7, 3.6, GOLD, 5, 0.12, 0.6)
        vt = travelers(BIG_AX, 4, BLUE, 0.2, 0.12)
        self.add(lumen, tissue, cell, axon, sdots, vt)
        # counters (first sip), unchanged
        cx = (3.5, 4.3)
        ct = ValueTracker(0.6)
        lk = VGroup(bar(cx[0], GOLD, ct, 0.6, 1.0, base=1.3), bar(cx[1], GREY, ct, 0.6, 1.0, base=1.3))
        lab_fs = T("first sip", 28, TEXT).move_to(V(5.9, 1.7))
        title1 = T("advantage above chance", 28, TEXT).move_to(V(3.85, 3.55))
        title2 = T("computed from reported preferences", 24, TEXT).move_to(V(3.85, 3.0))
        s1, s2 = ValueTracker(0.0), ValueTracker(0.0)
        k = 0.075
        base = -2.9
        b1 = bar(2.4, GREEN, s1, 1.2, k, base)
        b2 = bar(4.8, RED, s2, 1.2, k, base)
        n1 = always_redraw(lambda: M(f"{s1.get_value():.1f}", 30, GREEN).move_to(V(2.4, base + s1.get_value() * k + 0.35)))
        n2 = always_redraw(lambda: M(f"{s2.get_value():.1f}", 30, RED).move_to(V(4.8, base + s2.get_value() * k + 0.35)))
        c1 = T("control", 28, TEXT).move_to(V(2.4, -3.4))
        c2 = T("silenced", 28, TEXT).move_to(V(4.8, -3.4))
        lab = T("CCK-labelled", 28, GOLD).move_to(V(-1.9, 0.95))
        self.at("targeted")
        self.play(Indicate(cell, color=GOLD, scale_factor=1.08), run_time=1.0)
        self.at("CCK")
        self.play(FadeIn(lab), FadeIn(lk), FadeIn(lab_fs), FadeIn(title1), FadeIn(title2), run_time=0.8)
        self.at("labeled")
        self.add(n1, n2, b1, b2)
        self.play(s1.animate.set_value(40.8), FadeIn(c1), FadeIn(c2), run_time=2.0)
        self.at("Silencing")
        ring = Circle(radius=1.0, color=RED, stroke_width=6).move_to(CELL_B)
        self.play(Create(ring), dim.animate.set_value(1.0), run_time=1.2)
        self.at("strongly")
        self.play(s2.animate.set_value(8.9), run_time=2.0)
        self.at("Initial attraction")
        self.play(Indicate(lk, color=GREEN, scale_factor=1.12), run_time=1.5)
        self.finish()


class S10Separate(Base):
    def construct(self):
        self.clock()
        lumen = Rectangle(width=13.2, height=1.0, stroke_width=0, fill_color=TEAL, fill_opacity=0.3).move_to(V(0, 3.3))
        cell = RoundedRectangle(width=1.1, height=1.2, corner_radius=0.25, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.4).move_to(V(-4.8, 2.3))
        trunk = CubicBezier(V(-4.8, 1.7), V(-4.8, 0.3), V(-4.2, 0.1), V(-3.4, 0.1))
        up = CubicBezier(V(-3.4, 0.1), V(-1.8, 0.1), V(-1.0, 1.0), V(1.0, 1.0))
        lo = CubicBezier(V(-3.4, 0.1), V(-1.8, 0.1), V(-1.0, -2.2), V(1.0, -2.2))
        bT, bU, bL = hl(trunk.copy(), BLUE, 12), hl(up.copy(), BLUE, 12), hl(lo.copy(), BLUE, 12)
        allp = Line(V(-4.8, 1.7), V(-4.8, 1.7))
        self.add(lumen, cell)
        sugar = drift_dots(7, -6.4, 6.4, 2.95, 3.65, GOLD, 2, 0.1, 0.6)
        fat = drift_dots(7, -6.4, 6.4, 2.95, 3.65, WHITE, 3, 0.18, 0.5)
        self.at("Sugar")
        self.add(sugar)
        self.play(FadeIn(sugar), run_time=0.8)
        self.at("Fat")
        self.add(fat)
        self.play(FadeIn(fat), run_time=0.8)
        ft = VGroup(T("fat taste lost:", 30, RED), T("fat preference stays", 30, WHITE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(V(-1.2, 1.8))
        self.at("loss of fat")
        self.play(FadeIn(ft, shift=RIGHT * 0.2), run_time=0.8)
        self.at("Imaging")
        self.play(FadeOut(ft), Create(bT), Create(bU), Create(bL), run_time=1.0)
        # lamps
        def lamp(x, y, color=BG):
            return Circle(radius=0.22, stroke_color=TEXT, stroke_width=3, fill_color=color, fill_opacity=1).move_to(V(x, y))
        lu = [lamp(1.4, y) for y in (1.4, 0.8, 0.2)]
        ll = lamp(1.4, -2.2)
        tu = [T("sugar", 28, GOLD).next_to(lu[0], RIGHT, buff=0.25), T("fat", 28, WHITE).next_to(lu[1], RIGHT, buff=0.25),
              T("amino acids", 28, AMINO).next_to(lu[2], RIGHT, buff=0.25)]
        tl = T("fat", 28, WHITE).next_to(ll, RIGHT, buff=0.25)
        hU = T("broad responders", 30, BLUE).move_to(V(3.4, 2.3))
        hL = T("fat-only", 30, BLUE).move_to(V(2.3, -1.4))
        self.at("broad")
        self.play(FadeIn(hU), *[FadeIn(m) for m in lu], *[FadeIn(t) for t in tu], run_time=0.6)
        trU = travelers(up, 3, BLUE, 0.25, 0.1)
        trL = travelers(lo, 3, BLUE, 0.25, 0.1)
        self.add(trU, trL)
        self.play(lu[0].animate.set_fill(GOLD, 1), lu[1].animate.set_fill(WHITE, 1), lu[2].animate.set_fill(AMINO, 1), run_time=0.4)
        self.at("distinct")
        self.play(FadeIn(hL), FadeIn(ll), FadeIn(tl), run_time=0.8)
        self.play(ll.animate.set_fill(WHITE, 1), run_time=0.6)
        self.at("The broad")
        self.play(*[m.animate.set_fill(BG, 1) for m in lu], run_time=0.5)
        self.play(Indicate(hU, color=BLUE), run_time=0.8)
        self.at("sugar and")
        self.play(lu[0].animate.set_fill(GOLD, 1), run_time=0.4)
        self.at("amino")
        self.play(lu[2].animate.set_fill(AMINO, 1), run_time=0.4)
        self.at("fat is not")
        self.play(lu[1].animate.set_fill(WHITE, 1), Indicate(tu[1], color=WHITE, scale_factor=1.2), run_time=1.0)
        self.play(Indicate(hL, color=BLUE), run_time=0.8)
        self.finish()


class S11Knockouts(Base):
    def construct(self):
        self.clock()
        c1, c2 = 1.8, 5.0
        h1 = T("sugar response", 28, GOLD).move_to(V(c1, 3.3))
        h2 = T("fat response", 28, WHITE).move_to(V(c2, 3.3))
        rule = Line(V(-6.6, 2.85), V(6.6, 2.85), color=GREY, stroke_width=3)
        ra = T("SGLT1 absent", 32, TEXT).move_to(V(-4.2, 1.4))
        rb = VGroup(T("fat-receptor", 32, TEXT), T("combinations absent", 32, TEXT)).arrange(DOWN, buff=0.1).move_to(V(-4.0, -1.5))
        self.add(h1, h2, rule)

        def lamp(x, y):
            L = Circle(radius=0.62, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.9).move_to(V(x, y))
            L.t = 0.0
            L.on = True
            L.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_fill(m.get_stroke_color(), (0.65 + 0.3 * np.sin(m.t * 3)) if m.on else 0.12)))
            return L
        s_a, f_a = lamp(c1, 1.4), lamp(c2, 1.4)
        s_b, f_b = lamp(c1, -1.5), lamp(c2, -1.5)
        self.at("Remove")
        self.play(FadeIn(ra), FadeIn(s_a), FadeIn(f_a), run_time=1.2)
        self.at("sodium glucose")
        self.wait(0.8)
        self.at("gut sugar")
        s_a.on = False
        self.play(s_a.animate.set_stroke(RED), run_time=0.8)
        xa = x_cross(s_a.get_center(), 0.35, RED, 8)
        self.play(Create(xa), run_time=0.5)
        self.at("fat responses remain")
        self.play(Indicate(f_a, color=GREEN, scale_factor=1.2), run_time=1.4)
        self.at("Remove combinations")
        self.play(FadeIn(rb), FadeIn(s_b), FadeIn(f_b), run_time=1.2)
        self.at("fat responses fall")
        f_b.on = False
        self.play(f_b.animate.set_stroke(RED), run_time=0.8)
        xb = x_cross(f_b.get_center(), 0.35, RED, 8)
        self.play(Create(xb), run_time=0.5)
        self.at("The inputs")
        self.play(Indicate(VGroup(s_a, f_b), color=TEXT, scale_factor=1.15), run_time=1.5)
        sep = T("inputs separate", 34, TEXT).move_to(V(-4.0, 0.0))
        self.play(FadeIn(sep), run_time=0.8)
        self.finish()


# ----------------------------------------------------------- four stations (s12-s14)
SX = (-4.8, -1.6, 1.6, 4.8)
ST = (("epithelial\nsensor", GOLD), ("vagal\nresponse", BLUE), ("brainstem\nlearning", WHITE), ("behavior", GREEN))


def station(i, y=1.4):
    txt, c = ST[i]
    box = RoundedRectangle(width=2.7, height=2.2, corner_radius=0.25, stroke_color=c, stroke_width=5, fill_color=c, fill_opacity=0.2)
    lab = T(txt, 30, c, line_spacing=0.9)
    return VGroup(box, lab.move_to(box)).move_to(V(SX[i], y))


def stations(y=1.4):
    return VGroup(*[station(i, y) for i in range(4)])


def links(y=1.4):
    return VGroup(*[Arrow(V(SX[i] + 1.4, y), V(SX[i + 1] - 1.4, y), buff=0.05, stroke_width=5, color=TEXT, max_tip_length_to_length_ratio=0.5) for i in range(3)])


def pulse_across(scene_mob_y=1.4):
    d = Dot(radius=0.16, color=TEXT)
    d.u = 0.0

    def up(m, dt):
        m.u = (m.u + dt * 0.12) % 1
        m.move_to(V(-6.0 + 12.0 * m.u, scene_mob_y - 0.95))
    d.add_updater(up)
    return d


class S12Rule(Base):
    def construct(self):
        self.clock()
        st = stations(1.5)
        lk = links(1.5)
        self.at("Here")
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in st], lag_ratio=0.3), run_time=2.4)
        self.at("Match")
        self.play(Create(lk), run_time=0.8)
        p = pulse_across(1.5)
        self.add(p)
        for ph, i in (("epithelial", 0), ("vagal", 1), ("brainstem", 2), ("behavior", 3)):
            self.at(ph)
            self.play(Indicate(st[i], color=ST[i][1], scale_factor=1.1), run_time=1.0)
        self.at("Do not merge")
        cl = VGroup()
        names = ("milliseconds", "seconds", "hours")
        rates = (6.0, 1.2, 0.15)
        for x, n, r in zip((-4.0, 0.0, 4.0), names, rates):
            c = Circle(radius=0.75, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.08).move_to(V(x, -1.6))
            h = Line(V(x, -1.6), V(x, -0.95), color=TEXT, stroke_width=6)
            h.r = r
            h.add_updater(lambda m, dt: m.rotate(-dt * m.r, about_point=m.get_start()))
            cl.add(c, h, T(n, 30, TEXT).move_to(V(x, -2.8)))
        self.play(FadeIn(cl), run_time=1.0)
        dm = T("different measurements", 34, TEXT).move_to(V(0, -3.5))
        self.play(FadeIn(dm), run_time=0.8)
        self.finish()


class S13Scope(Base):
    def construct(self):
        self.clock()
        st = stations(1.5).move_to(V(0, 1.2))
        # stations sit at y 1.2 after shift (centre of the group)
        lk = links(1.2)
        pul = pulse_across(1.2)
        bd = DashedVMobject(RoundedRectangle(width=13.0, height=4.0, corner_radius=0.3, stroke_color=TEXT, stroke_width=4), num_dashes=70).move_to(V(0, 1.5))
        bl = T("mouse evidence", 30, TEXT).move_to(V(0, 3.2))
        self.add(st, lk, pul)
        self.at("These")
        self.play(Create(bd), FadeIn(bl), run_time=1.5)
        card1 = VGroup(RoundedRectangle(width=5.6, height=1.5, corner_radius=0.2, stroke_color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=1),
                       VGroup(T("germline deletion:", 30, TEXT), T("whole animal", 30, TEXT)).arrange(DOWN, buff=0.1)).move_to(V(-3.3, -1.6))
        card1[1].move_to(card1[0])
        card2 = VGroup(RoundedRectangle(width=5.6, height=1.5, corner_radius=0.2, stroke_color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=1),
                       VGroup(T("labelled population:", 30, TEXT), T("not perfectly pure", 30, TEXT)).arrange(DOWN, buff=0.1)).move_to(V(3.3, -1.6))
        card2[1].move_to(card2[0])
        self.at("Germ")
        self.play(FadeIn(card1, shift=UP * 0.3), run_time=1.0)
        self.at("Silencing")
        self.play(FadeIn(card2, shift=UP * 0.3), run_time=1.0)
        hum = VGroup(Circle(radius=0.25, color=TEXT, stroke_width=4), Line(V(0, -0.25), V(0, -1.0)), Line(V(0, -0.5), V(-0.4, -0.85)),
                     Line(V(0, -0.5), V(0.4, -0.85)), Line(V(0, -1.0), V(-0.3, -1.5)), Line(V(0, -1.0), V(0.3, -1.5))).set_stroke(TEXT, 4)
        hum.scale(0.8).move_to(V(-4.6, -3.05))
        hl_ = T("behavior not tested here", 30, TEXT).move_to(V(0.0, -3.05))
        self.at("Human")
        self.play(FadeIn(hum, shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(hl_), run_time=0.8)
        self.finish()


class S14Handoff(Base):
    def construct(self):
        self.clock()
        st = stations(1.2).move_to(V(0, 1.2))
        # shrink to a row of 22-pt chips at the top
        chips = VGroup(*[solid_chip(t.replace("\n", " "), ST[i][1], 22, 0.2) for i, (t, _) in enumerate(ST)]).arrange(RIGHT, buff=0.3).move_to(V(0, 3.3))
        fit(chips, max_w=12.4)
        box = RoundedRectangle(width=8.4, height=0.9, corner_radius=0.2, stroke_color=TEXT, stroke_width=4, fill_opacity=0).move_to(V(0, -3.25))
        boxl = T("Exact evidence and three routes below", 30, TEXT).move_to(box)
        self.add(st)
        self.play(Transform(st, chips), FadeIn(box), FadeIn(boxl), run_time=0.9)
        names = [T(n, 30, WHITE) for n in ("genotypes", "sample sizes", "preference calculation")]
        cs = [solid_chip(n, WHITE, 30) for n in ("genotypes", "sample sizes", "preference calculation")]
        for c, x in zip(cs, (-4.4, -0.9, 3.5)):
            c.move_to(V(x, 1.6))
        self.at("exact genotypes")
        self.play(FadeIn(cs[0], shift=DOWN * 0.2), run_time=0.7)
        self.at("sample")
        self.play(FadeIn(cs[1], shift=DOWN * 0.2), run_time=0.7)
        self.at("preference calculation")
        self.play(FadeIn(cs[2], shift=DOWN * 0.2), run_time=0.7)
        self.at("to the text")
        self.play(*[c.animate.move_to(V(0, -3.0)).scale(0.5).set_opacity(0) for c in cs], run_time=1.5)
        self.at("harder naming")
        lanes = VGroup()
        for y in (1.7, 0.5, -0.7):
            ln = RoundedRectangle(width=9.0, height=0.8, corner_radius=0.2, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.08).move_to(V(-0.8, y))
            lab = T("GLP-1?", 30, WHITE).move_to(V(-4.2, y))
            q = T("?", 44, WHITE, weight=BOLD).move_to(V(2.5, y))
            lanes.add(VGroup(ln, lab, q))
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.4) for l in lanes], lag_ratio=0.35), run_time=3.0)
        ar = Arrow(V(0, -1.4), V(0, -2.6), buff=0, stroke_width=6, color=TEXT)
        self.at("routes")
        self.play(Create(ar), run_time=0.8)
        self.finish()


class S15End(EndCard):
    LINE = "In mice, the gut teaches preference through separable sensory routes."
