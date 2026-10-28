"""Signals and how far they travel: why far signals ride the blood  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the signal: secretin, the extract, the hormone, epinephrine (every dot that travels)
  PURPLE = the sender: gut loop, gland, nerve cell
  BLUE   = the receiver: pancreas, target, receiving cell, and the receptor cup on it
  TEAL   = the blood (vessel, loop, the word "blood")
  GREEN  = the receiver answers: juice, a lit target, breakdown, a stronger beat
  RED    = cut or blocked: the cut nerves, "diffusion cannot deliver"
  ORANGE = weak acid
  GOLD   = time: the time bar, the curve, the clock
  GREY   = tissue outlines, axes, brackets, labels, whatever is not involved

No molecular structures: organs are outlines, cells are rounded boxes, a signal is a dot, a receptor
is a small cup on the cell, the blood is a tube, and the plot is computed from t = x^2 / 2D.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

G0 = np.array([-3.75, 0.3, 0])      # gut loop
P0 = np.array([4.0, -0.45, 0])      # pancreas
NA = np.array([-1.42, 0.4, 0])      # the gap between them: left end, right end
NB = np.array([1.75, -0.4, 0])


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def backed(mob, pad=0.07):
    """a label with an opaque backing."""
    b = Rectangle(width=mob.width + 2 * pad, height=mob.height + 2 * pad, stroke_width=0, fill_color=BG,
                  fill_opacity=1).move_to(mob)
    return VGroup(b, mob)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def sdot(r=0.09, color=YELLOW):
    return Dot(radius=r, color=color)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def flash(*mobs, s=1.12, color=TEXT):
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def fall(d, x, y0, y1, rt=1.1):
    """a drop that fades in, falls from y0 to y1 and fades out."""
    def upd(m, a):
        m.move_to([x, y0 + (y1 - y0) * a, 0])
        m.set_opacity(min(1.0, 6 * a) * (1 - max(0.0, (a - 0.8) / 0.2)))
    return UpdateFromAlphaFunc(d, upd, run_time=rt, rate_func=linear)


def drip(drops, xs, y0, y1, rt=1.2, lag=0.3):
    return LaggedStart(*[fall(d, x, y0, y1, rt) for d, x in zip(drops, xs)], lag_ratio=lag)


def invisible(*mobs):
    for m in mobs:
        m.set_opacity(0)
    return mobs


def clock(c, r=0.5):
    c = np.array(c, float)
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    face = Circle(radius=r, stroke_color=GOLD, stroke_width=4).move_to(c)
    ticks = VGroup(*[Line(c + (r - 0.1) * v, c + r * v, color=GOLD, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(c, c + UP * (r - 0.13), color=TEXT, stroke_width=5)
    pin = Dot(c, radius=0.05, color=TEXT)
    g = VGroup(back, face, ticks, hand, pin)
    g.hand, g.c = hand, c
    return g


def sweep(g, turns=1.0):
    return Rotate(g.hand, -TAU * turns, about_point=g.c, rate_func=linear)


class Film(SpokenScene):
    def until(self, phrase, lo=0.6, slack=0.0):
        """seconds from now until just before the narrator says `phrase` (so a long move ends on its cue)."""
        return max(lo, self.t_of(phrase) - 0.2 - self.elapsed() - slack)

    def to_end(self, slack=1.0, lo=1.0):
        return max(lo, self.narration_s - self.elapsed() - slack)


# ---------------------------------------------------------------------------------------------
# random walks (the diffusion is computed, not drawn by hand)
# ---------------------------------------------------------------------------------------------
def walks(n, steps, s, start, xlo, xhi, ylo, yhi, seed=3):
    rng = np.random.default_rng(seed)

    def fold(v, lo, hi):
        w = hi - lo
        q = np.mod(v - lo, 2 * w)
        return lo + np.where(q > w, 2 * w - q, q)

    pos = np.zeros((steps + 1, n, 2))
    pos[0] = np.array(start[:2], float) + rng.normal(0, 0.06, (n, 2))
    for k in range(steps):
        p = pos[k] + rng.normal(0, s, (n, 2))
        p[:, 0] = fold(p[:, 0], xlo, xhi)
        p[:, 1] = fold(p[:, 1], ylo, yhi)
        pos[k + 1] = p
    return pos


def at_step(pos, k):
    k = min(max(k, 0.0), len(pos) - 1.001)
    i = int(k)
    f = k - i
    return pos[i] * (1 - f) + pos[i + 1] * f


class Cloud:
    """dots that follow precomputed random walks."""

    def __init__(self, pos, r=0.06, color=YELLOW):
        self.pos = pos
        self.dots = VGroup(*[Dot(radius=r, color=color) for _ in range(pos.shape[1])])
        self.show(0)

    def show(self, k):
        for d, p in zip(self.dots, at_step(self.pos, k)):
            d.move_to([p[0], p[1], 0])

    def anim(self, k0, k1, rt, extra=None):
        def upd(m, a):
            k = k0 + (k1 - k0) * a
            self.show(k)
            if extra:
                extra(k)
        return UpdateFromAlphaFunc(self.dots, upd, run_time=rt, rate_func=linear)


# ---------------------------------------------------------------------------------------------
# organs of scenes 1 and 2
# ---------------------------------------------------------------------------------------------
def gut_ring(c):
    w, h = 4.6, 3.4
    outer = RoundedRectangle(corner_radius=1.4, width=w, height=h, stroke_color=PURPLE, stroke_width=4,
                             fill_color=PURPLE, fill_opacity=0.22).move_to(c)
    hole = RoundedRectangle(corner_radius=0.7, width=w - 1.9, height=h - 1.9, stroke_color=PURPLE, stroke_width=3,
                            fill_color=BG, fill_opacity=1).move_to(c)
    lbl = T("gut loop", 26, PURPLE).move_to(c)
    g = VGroup(outer, hole, lbl)
    g.outer, g.lbl = outer, lbl
    return g


def pancreas(c):
    def f(t):
        return np.array([1.95 * np.cos(t) * (1 + 0.07 * np.sin(3 * t + 0.5)),
                         1.45 * np.sin(t) * (1 + 0.14 * np.cos(2 * t + 0.6)), 0])
    body = ParametricFunction(f, t_range=[0, TAU, TAU / 90], stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.22)
    return body.move_to(c)


def abdomen():
    frame = RoundedRectangle(corner_radius=0.6, width=12.4, height=6.9, stroke_color=GREY, stroke_width=2.5)
    frame.set_stroke(opacity=0.5)
    lbl = T("abdomen", 24, GREY).move_to([5.25, 3.0, 0])
    return VGroup(frame, lbl)


def nerves():
    d = (NB - NA) / np.linalg.norm(NB - NA)
    n = np.array([-d[1], d[0], 0])
    M = (NA + NB) / 2
    lefts, rights = [], []
    for off in (-0.17, 0.0, 0.17):
        a, b, m = NA + n * off, NB + n * off, M + n * off
        lefts.append(DashedLine(a, m, dash_length=0.1, dashed_ratio=0.6, color=GREY, stroke_width=4))
        rights.append(DashedLine(m, b, dash_length=0.1, dashed_ratio=0.6, color=GREY, stroke_width=4))
    r = 0.3
    x = VGroup(Line(M + (LEFT + UP) * r, M + (RIGHT + DOWN) * r, color=RED, stroke_width=9),
               Line(M + (LEFT + DOWN) * r, M + (RIGHT + UP) * r, color=RED, stroke_width=9))
    return VGroup(*lefts), VGroup(*rights), x, d, M


def qboxes():
    out = VGroup()
    for t in (0.18, 0.5, 0.82):
        c = NA + (NB - NA) * t
        shape = RoundedRectangle(corner_radius=0.14, width=0.95, height=0.95)
        back = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to(c)
        edge = DashedVMobject(shape.copy().move_to(c), num_dashes=26).set_color(GREY)
        q = T("?", 40, TEXT, weight=BOLD).move_to(c)
        out.add(VGroup(back, edge, q))
    return out


# the vessel between gut and pancreas (scene 2)
VH1, VH2 = np.array([1.3, 0.35, 0]), np.array([-1.3, 0.35, 0])


def bez(t):
    return ((1 - t) ** 3) * NA + 3 * ((1 - t) ** 2) * t * (NA + VH1) + 3 * (1 - t) * t ** 2 * (NB + VH2) + t ** 3 * NB


def lane(t0, t1):
    return ParametricFunction(bez, t_range=[t0, t1, 0.02]).set_stroke(opacity=0)


def vessel():
    return ParametricFunction(bez, t_range=[0, 1, 0.02], stroke_color=TEAL, stroke_width=34, stroke_opacity=0.4)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Signals and how far they travel"
    TITLE = "Why far signals ride the blood"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """cut the nerves, drip acid on the gut: the pancreas still answers. What carried the message?"""

    def construct(self):
        gut, body = gut_ring(G0), pancreas(P0)
        nl, nr, cutx, d, M = nerves()
        self.play(FadeIn(gut), FadeIn(body), FadeIn(nl), FadeIn(nr), run_time=0.35)

        self.at("every nerve")
        cutlbl = T("nerves cut", 24, RED).move_to(M + DOWN * 0.85)
        self.play(Create(cutx), nl.animate.shift(-d * 0.3), nr.animate.shift(d * 0.3), FadeIn(cutlbl), run_time=0.6)

        acid = T("weak acid", 26, ORANGE).move_to([G0[0], 3.17, 0])
        drops = [Dot(radius=0.13, color=ORANGE) for _ in range(3)]
        invisible(*drops)
        self.add(*drops)
        xs = [G0[0] - 0.6, G0[0], G0[0] + 0.6]
        self.at("then drip")
        self.play(FadeIn(acid), drip(drops, xs, 2.88, 2.12, 1.1, 0.35), run_time=1.3)
        self.play(*flash(gut.outer, s=1.04, color=ORANGE), run_time=0.4)

        plbl = T("pancreas", 26, BLUE).move_to(P0)
        self.at("The pancreas still")
        self.play(FadeIn(plbl), run_time=0.4)
        juice = [Dot(radius=0.12, color=GREEN) for _ in range(3)]
        invisible(*juice)
        self.add(*juice)
        jl = T("juice", 26, GREEN).move_to([2.2, -2.75, 0])
        jx = [P0[0] - 0.7, P0[0], P0[0] + 0.7]
        self.at("its juice")
        self.play(FadeIn(jl), drip(juice, jx, -2.2, -3.2, 1.1, 0.35), body.animate.set_stroke(GREEN), run_time=1.3)

        ab = abdomen()
        self.at("different part")
        self.play(FadeIn(ab), *flash(body, s=1.05), drip(juice, jx, -2.2, -3.2, 1.1, 0.35), run_time=1.3)

        lead = VGroup(T("the leading view:", 24, GREY), T("by nerve", 24, GREY)).arrange(DOWN, buff=0.1).move_to([0.1, 1.55, 0])
        self.at("leading view")
        self.play(FadeIn(lead, shift=DOWN * 0.1), run_time=0.5)
        self.at("But no wire")
        self.play(FadeOut(lead), *flash(cutx, s=1.25, color=RED), run_time=0.7)

        qs = qboxes()
        self.at("What carried")
        self.play(FadeOut(nl), FadeOut(nr), FadeOut(cutx), FadeOut(cutlbl),
                  LaggedStart(*[FadeIn(b, scale=0.8) for b in qs], lag_ratio=0.3), run_time=1.0)
        self.play(LaggedStart(*[pop(b[2], 1.5) for b in qs], lag_ratio=0.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Road(Film):
    """a chemical, secretin, rides the blood from the gut to the pancreas. But why ride? molecules can drift."""

    def construct(self):
        ab, gut, body, qs = abdomen(), gut_ring(G0), pancreas(P0), qboxes()
        plbl = T("pancreas", 26, BLUE).move_to(P0)
        acid = T("weak acid", 26, ORANGE).move_to([G0[0], 3.17, 0])
        jl0 = T("juice", 26, GREEN).move_to([2.2, -2.75, 0])        # where scene 1 left them
        body.set_stroke(GREEN)
        self.add(ab, gut, body, plbl, qs, acid, jl0)
        mid = bez(0.5)

        # the question marks become one chemical
        chem = sdot(0.2).move_to(mid)
        cl = T("chemical", 28, YELLOW).next_to(chem, UP, buff=0.3)
        self.at("was a chemical")
        self.play(FadeOut(qs), FadeOut(jl0), body.animate.set_stroke(BLUE), GrowFromCenter(chem), FadeIn(cl), run_time=0.7)
        sl = T("secretin", 28, YELLOW).move_to(cl)
        self.at("named secretin")
        self.play(ReplacementTransform(cl, sl), pop(chem, 1.3), run_time=0.7)

        # acid frees it from the gut lining
        drops = [Dot(radius=0.13, color=ORANGE) for _ in range(3)]
        invisible(*drops)
        self.add(*drops)
        xs = [G0[0] - 0.6, G0[0], G0[0] + 0.6]
        self.at("Acid released it")
        self.play(FadeOut(chem), FadeOut(sl), *flash(acid, s=1.1, color=ORANGE), drip(drops, xs, 2.88, 2.12, 1.0, 0.3), run_time=1.2)
        burst = VGroup(*[sdot(0.1) for _ in range(5)])
        for b, dy in zip(burst, (-0.3, -0.15, 0.0, 0.15, 0.3)):
            b.move_to(NA + UP * dy * 0.6 + LEFT * 0.2)
        self.at("gut lining")
        self.play(*flash(gut.outer, s=1.04, color=ORANGE), LaggedStart(*[FadeIn(b, scale=0.4) for b in burst], lag_ratio=0.15), run_time=0.8)

        # the blood carries it
        ves = vessel()
        bl = T("blood", 28, TEAL).move_to([0.1, -0.75, 0])
        ln = lane(0, 1)
        juice = [Dot(radius=0.12, color=GREEN) for _ in range(4)]
        invisible(*juice)
        self.add(*juice)
        jx = [3.3, 3.9, 4.5, 5.1]
        jl = T("juice", 26, GREEN).move_to([2.2, -2.75, 0])
        self.at("the blood carried")
        self.play(Create(ves), FadeIn(bl),
                  LaggedStart(*[MoveAlongPath(b, ln, rate_func=linear) for b in burst], lag_ratio=0.1), run_time=1.2)
        self.at("to the pancreas")
        self.play(FadeOut(burst), body.animate.set_stroke(GREEN), FadeIn(jl),
                  drip(juice[:3], jx[:3], -2.2, -3.2, 1.0, 0.3), run_time=0.9)

        # an extract injected into a vein: even more
        ex = bchip("extract", YELLOW, 26).move_to([0.1, 2.55, 0])
        self.at("An extract")
        self.play(FadeIn(ex, shift=DOWN * 0.15), run_time=0.5)
        inj = arr([0.1, 2.15, 0], [mid[0], mid[1] + 0.3, 0], YELLOW)
        self.at("injected into")
        self.play(GrowArrow(inj), run_time=0.5)
        shot = VGroup(*[sdot(0.1) for _ in range(8)])
        for sh in shot:
            sh.move_to(mid)
        ln2 = lane(0.5, 1)
        self.play(LaggedStart(*[MoveAlongPath(sh, ln2, rate_func=linear) for sh in shot], lag_ratio=0.1), run_time=1.3)
        ml = T("more juice", 26, GREEN).move_to(jl)
        self.at("even more")
        self.play(FadeOut(shot), ReplacementTransform(jl, ml), drip(juice, jx, -2.2, -3.2, 1.0, 0.2), run_time=1.1)
        self.play(drip(juice, jx, -2.2, -3.2, 1.0, 0.2), run_time=1.1)

        # but molecules can also just drift
        walk = walks(12, 160, 0.1, NA + LEFT * 0.1, -1.55, 1.7, -3.0, 3.1, seed=5)
        cloud = Cloud(walk, r=0.09)
        self.at("also drift")
        self.play(FadeOut(ves), FadeOut(bl), FadeOut(ex), FadeOut(inj), FadeOut(ml), body.animate.set_stroke(BLUE), FadeIn(cloud.dots), run_time=0.5)
        self.play(cloud.anim(0, 140, self.until("ride the blood", lo=1.2, slack=0.0)))

        # so why the blood?
        q = VGroup(Circle(radius=0.55, stroke_color=TEAL, stroke_width=5, fill_color=BG, fill_opacity=1),
                   T("?", 64, TEAL, weight=BOLD)).move_to([0.1, 0.2, 0])
        self.at("ride the blood")
        self.play(Create(ves), FadeOut(cloud.dots), GrowFromCenter(q), run_time=0.9)
        self.at("at all")
        self.play(pop(q, 1.25), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Wander(Film):
    """a cloud of molecules wanders out of a source. Near target: soon. Far target: four times as long."""

    def construct(self):
        YC = 0.2
        XS, XN, XF = -5.2, -0.2, 4.8             # cloud start, near target, far target (5.0 and 10.0 from the start)
        SUB, K1, K2 = 4, 120, 480                # sub-steps per unit; the near / far target is reached at K1 / K2 units
        s_unit = (5.0 / 1.44) / np.sqrt(K1)      # spread sqrt(2Dt) grows as the square root of time
        pos = walks(110, K2 * SUB, s_unit / np.sqrt(SUB), [XS, YC], XS, 6.1, YC - 2.4, YC + 2.4, seed=11)
        u = lambda k: k * SUB

        band = RoundedRectangle(corner_radius=0.3, width=12.4, height=4.8, stroke_color=GREY, stroke_width=2.5)
        band.set_stroke(opacity=0.5).move_to([0, YC, 0])
        src = Circle(radius=0.45, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to([-5.7, YC, 0])
        srcl = T("source", 24, PURPLE).move_to([-5.7, 3.05, 0])
        cloud = Cloud(pos, r=0.06)
        tracer = Dot(radius=0.1, color=YELLOW).set_stroke(TEXT, 2)
        trail = VMobject(stroke_color=YELLOW, stroke_width=3, stroke_opacity=0.9)
        self.play(FadeIn(band), FadeIn(src), FadeIn(srcl), run_time=0.4)
        self.add(cloud.dots, trail, tracer)

        def track(k):
            i = int(k)
            tracer.move_to([pos[i, 0, 0], pos[i, 0, 1], 0])
            pts = [[pos[j, 0, 0], pos[j, 0, 1], 0] for j in range(0, i + 1, 2)]
            if len(pts) > 1:
                trail.set_points_as_corners(pts)

        dl = T("diffusion", 28, TEXT).move_to([-2.9, 3.05, 0])
        self.at("drift is called")
        self.play(FadeIn(dl), cloud.anim(0, u(28), self.until("not heading"), track))
        self.at("not heading")
        self.play(cloud.anim(u(28), u(45), self.until("It wanders"), track))
        self.at("It wanders")
        self.play(*flash(tracer, s=1.8), cloud.anim(u(45), u(58), self.until("wander a distance"), track))

        # near target: the cloud gets there after a while
        near = Rectangle(width=0.3, height=4.8, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.08).move_to([XN, YC, 0])
        nearl = backed(T("near target", 24, BLUE)).move_to([XN, 3.05, 0])
        far = Rectangle(width=0.3, height=4.8, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.08).move_to([XF, YC, 0])
        farl = backed(T("far target", 24, BLUE)).move_to([XF, 3.05, 0])
        bar_y, bar_x0, c = -2.8, -4.9, 0.0135
        tlabel = T("time", 24, GOLD).move_to([-5.7, bar_y, 0])
        bar = Line([bar_x0, bar_y, 0], [bar_x0 + 0.01, bar_y, 0], color=GOLD, stroke_width=14)
        ramp = lambda f: 0.08 + 0.72 * min(1.0, max(0.0, (f - 0.02) / 0.13))

        def reach(k):
            P = at_step(pos, k)[:, 0]
            near.set_fill(BLUE, ramp(float(np.mean(P >= XN))))
            far.set_fill(BLUE, ramp(float(np.mean(P >= XF))))
            bar.put_start_and_end_on([bar_x0, bar_y, 0], [bar_x0 + max(0.01, k / SUB * c), bar_y, 0])

        self.at("wander a distance")
        self.play(FadeOut(trail), FadeOut(tracer), FadeOut(dl), FadeIn(near), FadeIn(nearl),
                  cloud.anim(u(58), u(70), self.until("with the square"), reach))
        formula = T("time grows as distance²", 26, GOLD).move_to([4.5, bar_y, 0])
        self.at("with the square")
        self.play(FadeIn(tlabel), FadeIn(bar), cloud.anim(u(70), u(K1), self.until("diffusion punishes", slack=0.5), reach))
        tn = T("near target", 22, GOLD).next_to([bar_x0 + K1 * c, bar_y, 0], DOWN, buff=0.15)
        self.play(FadeIn(tn), FadeIn(formula), *flash(near, s=1.1), run_time=0.4)

        # far target: much later
        self.at("diffusion punishes")
        self.play(FadeIn(far), FadeIn(farl), run_time=0.4)
        self.play(cloud.anim(u(K1), u(K2), self.to_end(slack=1.0), reach))
        tf = T("far target", 22, GOLD).next_to([bar_x0 + K2 * c, bar_y, 0], DOWN, buff=0.15)
        self.play(FadeIn(tf), *flash(far, s=1.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Numbers(Film):
    """time = x^2 / 2D, plotted: 20 nm gap, a millimeter, a centimeter (both axes in tenfold steps)."""

    def construct(self):
        D = 1e-5                                  # cm^2 / s, a small molecule in water (the lesson's value)
        X = lambda lx: -5.6 + (lx + 7) * 1.3      # log10(distance in cm)
        Y = lambda ly: -2.4 + (ly + 9) * 0.3333   # log10(time in s)
        P = lambda lx, ly: np.array([X(lx), Y(ly), 0])
        curve_ly = lambda lx: 2 * lx - np.log10(2 * D)      # t = x^2 / 2D
        ly_to_lx = lambda ly: (ly + np.log10(2 * D)) / 2

        xaxis = Arrow([-5.6, -2.4, 0], [5.3, -2.4, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        yaxis = Arrow([-5.6, -2.4, 0], [-5.6, 2.75, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        ticks = VGroup()
        for k in range(-7, 2):
            ticks.add(Line([X(k), -2.4, 0], [X(k), -2.28, 0], color=GREY, stroke_width=2))
        for k in range(-9, 7):
            ticks.add(Line([-5.6, Y(k), 0], [-5.48, Y(k), 0], color=GREY, stroke_width=2))
        xl = T("distance", 26, GREY).move_to([4.6, -2.0, 0])
        yl = T("time", 26, GOLD).move_to([-5.0, 2.75, 0])
        note = T("each tick is ten times more", 22, GREY).move_to([-2.9, -3.3, 0])
        mol = VGroup(Dot(radius=0.3, color=YELLOW), T("a small molecule", 36, YELLOW), T("in water", 30, GREY)).arrange(DOWN, buff=0.25).move_to([0, 0.2, 0])
        self.at("small molecule")
        self.play(FadeIn(mol, scale=0.6), run_time=0.6)
        self.at("change only")
        self.play(FadeOut(mol), Create(xaxis), Create(yaxis), FadeIn(ticks), run_time=0.8)
        self.play(FadeIn(xl), FadeIn(yl), FadeIn(note), run_time=0.5)

        def pt(lx, down=-2.4):
            p = P(lx, curve_ly(lx))
            return p, Dot(p, radius=0.14, color=GOLD), DashedLine([p[0], down, 0], p, color=GREY, stroke_width=2.5, dash_length=0.1)

        # 20 nm synaptic gap
        pA, dA, gA = pt(np.log10(2e-6))
        la = VGroup(T("20 nm synaptic gap", 24, TEXT), T("a fraction of a microsecond", 24, GOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        la.move_to([-2.2 + la.width / 2, pA[1], 0])
        leadA = DashedLine([pA[0] + 0.2, pA[1], 0], [-2.25, pA[1], 0], color=GREY, stroke_width=2.5, dash_length=0.1)
        self.at("synaptic gap")
        self.play(Create(gA), FadeIn(la[0]), run_time=0.7)
        self.at("fraction of a microsecond")
        self.play(GrowFromCenter(dA), Create(leadA), FadeIn(la[1]), run_time=0.7)

        # a millimeter
        yb = -2.85
        pB, dB, gB = pt(-1.0, yb)
        lb = VGroup(T("1 millimeter", 24, TEXT), T("about 8 minutes", 24, GOLD)).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        lb.move_to([pB[0] - 0.25 - lb.width / 2, pB[1] + 0.55, 0])
        self.at("a millimeter")
        self.play(Create(gB), FadeIn(lb[0]), run_time=0.6)
        self.at("minutes")
        self.play(GrowFromCenter(dB), FadeIn(lb[1]), run_time=0.7)

        # a centimeter
        pC, dC, gC = pt(0.0, yb)
        lc = VGroup(T("1 centimeter", 24, TEXT), T("about 14 hours", 24, GOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lc.move_to([pC[0] + 0.25 + lc.width / 2, pC[1] - 0.6, 0])
        self.at("a centimeter")
        self.play(Create(gC), FadeIn(lc[0]), run_time=0.6)
        self.at("hours")
        self.play(GrowFromCenter(dC), FadeIn(lc[1]), run_time=0.7)

        # the curve, computed from the equation, runs through all three
        lx0, lx1 = ly_to_lx(-9), ly_to_lx(6)
        curve = Line(P(lx0, curve_ly(lx0)), P(lx1, curve_ly(lx1)), color=GOLD, stroke_width=6)
        self.at("The centimeter is")
        self.play(Create(curve), run_time=1.2)

        # ten times farther, yet hours instead of minutes
        span = DoubleArrow([pB[0], yb, 0], [pC[0], yb, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.15)
        spl = T("ten times farther", 22, GREY).move_to([(pB[0] + pC[0]) / 2, yb - 0.45, 0])
        self.at("times farther")
        self.play(GrowFromCenter(span), FadeIn(spl), *flash(dB, dC, s=1.4), run_time=0.8)
        self.at("hours instead")
        self.play(*flash(lb[1], lc[1], s=1.2, color=TEXT), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Answers(Film):
    """too slow past a few hundred micrometers: ride the blood (far) or shrink the gap (near)."""

    def construct(self):
        CY = -0.3
        gland_c, targ_c = np.array([-4.8, CY, 0]), np.array([4.8, CY, 0])
        gland = Circle(radius=1.15, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.25).move_to(gland_c)
        targ = Circle(radius=1.15, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to(targ_c)
        gl = T("gland", 28, PURPLE).move_to([-4.8, CY + 1.55, 0])
        tl = T("target", 28, BLUE).move_to([4.8, CY + 1.55, 0])
        path = DashedLine([-3.55, CY, 0], [3.55, CY, 0], color=GREY, stroke_width=4, dash_length=0.14)
        ck = clock([0, 2.5, 0], 0.55)
        ckl = T("within a minute", 26, GOLD).next_to(ck, RIGHT, buff=0.35)
        self.play(FadeIn(gland), FadeIn(gl), FadeIn(targ), FadeIn(tl), FadeIn(path), run_time=0.3)

        # diffusion cannot reach in time
        wk = walks(14, 240, 0.09, [-3.45, CY], -3.45, -0.6, CY - 1.5, CY + 1.5, seed=9)
        cloud = Cloud(wk, r=0.09)
        br = DoubleArrow([-3.55, -1.95, 0], [3.55, -1.95, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.18)
        brl = T("past a few hundred µm", 26, GREY).move_to([0, -2.5, 0])
        self.at("few hundred")
        self.play(GrowFromCenter(br), FadeIn(brl), FadeIn(cloud.dots), run_time=0.7)
        xmark = VGroup(Line([-0.3, CY + 0.3, 0], [0.3, CY - 0.3, 0], color=RED, stroke_width=9),
                       Line([-0.3, CY - 0.3, 0], [0.3, CY + 0.3, 0], color=RED, stroke_width=9))
        self.at("cannot deliver")
        self.play(cloud.anim(0, 100, 1.6), Create(xmark), run_time=1.6)
        self.at("within a minute")
        self.play(FadeIn(ck), FadeIn(ckl), run_time=0.4)
        self.play(sweep(ck, 1.0), cloud.anim(100, 240, 1.8), run_time=1.8)

        # the blood
        ring = ParametricFunction(lambda t: np.array([4.15 * np.cos(t), CY + 1.9 * np.sin(t), 0]),
                                  t_range=[0, TAU, 0.05], stroke_color=TEAL, stroke_width=22, stroke_opacity=0.4)
        ringp = ParametricFunction(lambda t: np.array([4.15 * np.cos(PI - t), CY + 1.9 * np.sin(PI - t), 0]),
                                   t_range=[0, TAU, 0.02]).set_stroke(opacity=0)      # clockwise, from the gland round
        bl = T("blood", 28, TEAL).move_to([0, CY - 2.45, 0])
        load = VGroup(*[sdot(0.12) for _ in range(6)])
        for i, m in enumerate(load):
            a = i / 6 * TAU
            m.move_to(gland_c + 0.5 * np.array([np.cos(a), np.sin(a), 0]) + RIGHT * 0.45)
        self.at("releases its hormone")
        self.play(FadeOut(cloud.dots), FadeOut(br), FadeOut(brl), FadeOut(xmark), FadeOut(path), FadeIn(load, scale=0.5), run_time=0.7)
        self.at("into the blood")
        self.play(Create(ring), FadeIn(bl), run_time=1.0)
        ckl2 = T("about a minute", 26, GOLD).move_to(ckl)
        self.at("circulates around")
        self.play(ReplacementTransform(ckl, ckl2), run_time=0.4)
        lap = max(2.4, min(4.0, self.until("do the opposite", slack=0.4)))
        self.play(sweep(ck, 1.0),
                  LaggedStart(*[MoveAlongPath(m, ringp, rate_func=linear) for m in load], lag_ratio=0.06),
                  Succession(Wait(lap * 0.45), AnimationGroup(targ.animate.set_stroke(GREEN).set_fill(GREEN, 0.3),
                                                               tl.animate.set_color(GREEN), run_time=0.5)),
                  run_time=lap)

        # the opposite: a tiny gap
        self.at("do the opposite")
        old = VGroup(gland, gl, targ, tl, ring, bl, ck, ckl2, load)

        sender = RoundedRectangle(corner_radius=0.4, width=5.4, height=3.6, stroke_color=PURPLE, stroke_width=4,
                                  fill_color=PURPLE, fill_opacity=0.2).move_to([-2.8, 0.2, 0])
        recv = RoundedRectangle(corner_radius=0.4, width=5.4, height=3.6, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.15).move_to([2.8, 0.2, 0])
        sl = T("nerve cell", 30, PURPLE).move_to([-3.6, 0.2, 0])
        rl = T("receiving cell", 30, BLUE).move_to([3.9, 0.2, 0])
        cups = VGroup(*[AnnularSector(inner_radius=0.16, outer_radius=0.3, angle=PI, start_angle=-PI / 2, color=BLUE,
                                      fill_opacity=1, stroke_width=0).move_to([0.1 + 0.13, y, 0]) for y in (0.9, -0.5)])
        other = RoundedRectangle(corner_radius=0.3, width=5.4, height=1.2, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.1).move_to([0, -2.75, 0])
        ol = T("nearby cells", 26, GREY).move_to(other)
        pts = VGroup(*[sdot(0.1) for _ in range(5)])
        for p, y in zip(pts, (1.1, 0.65, 0.2, -0.25, -0.7)):
            p.move_to([-0.55, y, 0])
        self.play(FadeOut(old), FadeIn(sender), FadeIn(recv), FadeIn(sl), FadeIn(rl), FadeIn(cups), FadeIn(other), FadeIn(ol), run_time=0.9)
        self.at("A nerve cell")
        self.play(*flash(sender, sl, s=1.04, color=TEXT), run_time=0.8)
        pa = arr([-1.4, 2.2, 0], [-0.13, 2.2, 0], GREY, 4, 0.16)
        pb = arr([1.4, 2.2, 0], [0.13, 2.2, 0], GREY, 4, 0.16)
        gap = T("a gap of tens of nanometers", 26, GREY).move_to([0, 2.85, 0])
        self.at("only tens of")
        self.play(FadeIn(pts), GrowArrow(pa), GrowArrow(pb), FadeIn(gap), run_time=0.9)
        tm = T("almost at once", 26, GOLD).move_to([3.9, -0.8, 0])
        self.at("arrives almost")
        self.play(*[p.animate.move_to([0.1, y, 0]) for p, y in zip(pts, (0.9, 0.5, 0.2, -0.1, -0.5))], run_time=0.25)
        self.play(recv.animate.set_stroke(GREEN), rl.animate.set_color(GREEN), cups.animate.set_color(GREEN), FadeIn(tm), run_time=0.5)
        self.at("some spills out")
        self.play(pts[-1].animate.move_to([-0.65, -2.2, 0]),
                  pts[-2].animate.move_to([0.65, -2.2, 0]), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Receiver(Film):
    """the blood passes every organ; only the cell with a receptor answers."""

    def construct(self):
        VY, RY = 2.35, -0.55
        TOP = RY + 1.25
        xs = [-4.8, -1.6, 1.6, 4.8]
        ves = RoundedRectangle(corner_radius=0.4, width=12.4, height=0.9, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.25).move_to([0, VY, 0])
        vl = T("blood", 26, TEAL).move_to([-5.4, VY + 0.8, 0])

        def box(x, color):
            return RoundedRectangle(corner_radius=0.3, width=2.7, height=2.5, stroke_color=color, stroke_width=4,
                                    fill_color=color, fill_opacity=0.15).move_to([x, RY, 0])

        def cup(x):
            return AnnularSector(inner_radius=0.2, outer_radius=0.38, angle=PI, start_angle=PI, color=BLUE,
                                 fill_opacity=1, stroke_width=0).move_to([x, TOP, 0])

        # first row: pancreatic secretion measured; other organ responses unspecified
        orgs = [box(x, GREY) for x in xs]
        orgs[2].set_stroke(BLUE).set_fill(BLUE, 0.15)
        names = [T("organ", 26, GREY).move_to([xs[0], RY, 0]), T("organ", 26, GREY).move_to([xs[1], RY, 0]),
                 T("pancreas", 26, BLUE).move_to([xs[2], RY, 0]), T("organ", 26, GREY).move_to([xs[3], RY, 0])]
        unknown = VGroup(*[T("no such response", 20, GREY).move_to([xs[i], RY - 0.7, 0])
                           for i in (0, 1, 3)])
        row1 = VGroup(*orgs, *names, unknown)
        self.play(FadeIn(ves), FadeIn(vl), FadeIn(row1), run_time=0.5)

        reach = VGroup(*[sdot(0.14) for _ in xs])
        for r, x in zip(reach, xs):
            r.move_to([x - 1.0, VY, 0])
        self.add(reach)
        self.at("every organ")
        self.play(LaggedStart(*[r.animate.move_to([x, TOP + 0.45, 0]) for r, x in zip(reach, xs)], lag_ratio=0.18), run_time=1.4)
        jl = T("juice", 26, GREEN).move_to([xs[2] + 2.0, RY - 2.0, 0])
        jd = [Dot(radius=0.12, color=GREEN) for _ in range(3)]
        invisible(*jd)
        self.add(*jd)
        self.at("the pancreas")
        self.play(reach[2].animate.move_to([xs[2], TOP + 0.02, 0]),
                  orgs[2].animate.set_stroke(GREEN), run_time=0.7)
        self.play(FadeIn(jl), drip(jd, [xs[2] - 0.5, xs[2], xs[2] + 0.5], RY - 1.35, RY - 2.55, 1.1, 0.3), run_time=1.3)

        self.at("does not choose")
        self.play(*[Indicate(r, color=TEXT, scale_factor=1.5) for r in reach], run_time=0.9)
        rcp = T("receiver", 26, BLUE).move_to([xs[2], TOP + 0.75, 0])
        self.at("The receiver does")
        self.play(FadeIn(rcp), *flash(orgs[2], names[2], s=1.06, color=TEXT), run_time=0.9)

        # second row: epinephrine, one hormone, three different answers
        orgs2 = [box(x, BLUE) for x in xs[:3]] + [box(xs[3], GREY)]
        names2 = [T("liver cell", 26, BLUE).move_to([xs[0], RY, 0]), T("fat cell", 26, BLUE).move_to([xs[1], RY, 0]),
                  T("heart cell", 26, BLUE).move_to([xs[2], RY, 0]), T("no receptor", 26, GREY).move_to([xs[3], RY, 0])]
        cups2 = [cup(x) for x in xs[:3]]
        row2 = VGroup(*orgs2, *names2, *cups2)
        el = T("epinephrine", 28, YELLOW).move_to([0.3, VY + 0.8, 0])
        self.at("Epinephrine")
        self.play(FadeOut(row1), FadeOut(reach), FadeOut(rcp), FadeOut(jl), FadeOut(vl), run_time=0.4)
        self.play(FadeIn(row2), FadeIn(el), run_time=0.5)
        hormone = VGroup(*[sdot(0.14) for _ in xs])
        for h, x in zip(hormone, xs):
            h.move_to([x - 1.0, VY, 0])
        self.add(hormone)
        resp = [VGroup(T("glycogen", 22, GREEN), T("breakdown", 22, GREEN)).arrange(DOWN, buff=0.04).move_to([xs[0], RY - 1.25 - 0.5, 0]),
                VGroup(T("fat", 22, GREEN), T("breakdown", 22, GREEN)).arrange(DOWN, buff=0.04).move_to([xs[1], RY - 1.25 - 0.5, 0]),
                VGroup(T("stronger", 22, GREEN), T("beat", 22, GREEN)).arrange(DOWN, buff=0.04).move_to([xs[2], RY - 1.25 - 0.5, 0])]

        def answer(i):
            return [hormone[i].animate.move_to([xs[i], TOP + 0.02, 0]), orgs2[i].animate.set_stroke(GREEN),
                    names2[i].animate.set_color(GREEN), FadeIn(resp[i])]

        self.at("liver cells")
        self.play(hormone[0].animate.move_to([xs[0], TOP + 0.45, 0]), run_time=0.5)
        self.play(*answer(0), run_time=0.6)
        self.at("fat cells")
        self.play(hormone[1].animate.move_to([xs[1], TOP + 0.45, 0]), run_time=0.5)
        self.play(*answer(1), run_time=0.6)
        self.at("heart beat")
        self.play(hormone[2].animate.move_to([xs[2], TOP + 0.45, 0]), run_time=0.5)
        self.play(*answer(2), run_time=0.6)
        self.play(*[pop(m, 1.06) for m in (orgs2[2], names2[2])], run_time=0.4)
        self.play(*[pop(m, 1.06) for m in (orgs2[2], names2[2])], run_time=0.4)

        # the rule
        self.at("far messages")
        self.play(hormone[3].animate.move_to([xs[3], TOP + 0.45, 0]), run_time=0.7)
        rcl = T("receptor", 26, BLUE).move_to([xs[1], TOP + 0.75, 0])
        self.at("the receptor decides")
        self.play(FadeIn(rcl), *flash(*cups2, s=1.4), hormone[3].animate.move_to([xs[3] + 1.0, VY - 0.2, 0]).set_opacity(0.3), run_time=0.9)
        self.at("who answers")
        self.play(*[Indicate(o, color=GREEN, scale_factor=1.04) for o in orgs2[:3]], run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Far messages ride the blood; the receptor decides who answers."
