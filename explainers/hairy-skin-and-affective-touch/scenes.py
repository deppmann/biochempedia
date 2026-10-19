"""Hairy skin, stroking and affective touch (Biochemistrypedia explainer): a match between two curves.

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the brush stroke / stimulus (and the 1 to 10 cm/s band highlight)
  GREEN  = the human CT afferent and its firing (the recorded group)
  PURPLE = pleasantness ratings (the separate group of volunteers)
  BLUE   = the recording electrode
  ORANGE = mouse afferent populations (the three candidates)
  RED    = "not shown" / the cut / a link the data do not support
  GREY   = skin, nerve, axes, structure, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bell(x):
    """The inverted U of the sketch: peak inside the 1 to 10 cm/s band, in log10 velocity."""
    return float(np.exp(-((x - 0.5) / 0.62) ** 2))


def spikes(n, w, h=0.34, color=GREEN, x0=0.0, seed=0):
    """n spike ticks spread over width w (a sketch of firing rate, not data)."""
    rng = np.random.RandomState(seed)
    xs = np.sort(np.linspace(0.08, w - 0.08, n) + rng.uniform(-0.06, 0.06, n))
    return VGroup(*[Line([x0 + x, -h / 2, 0], [x0 + x, h / 2, 0], color=color, stroke_width=4) for x in xs])


def skin_bar(x0, x1, y, h=0.5):
    return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.28).move_to([(x0 + x1) / 2, y, 0])


def hair(x, y, h=0.9, lean=0.0):
    return Line([x, y, 0], [x + lean, y + h, 0], color=GREY, stroke_width=4)


def brush(x, y):
    handle = Line([x, y + 1.0, 0], [x, y + 0.35, 0], color=YELLOW, stroke_width=8)
    head = RoundedRectangle(corner_radius=0.06, width=0.9, height=0.26, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.55).move_to([x, y + 0.22, 0])
    bristles = VGroup(*[Line([x - 0.36 + 0.12 * i, y + 0.09, 0], [x - 0.36 + 0.12 * i, y - 0.06, 0],
                             color=YELLOW, stroke_width=3) for i in range(7)])
    return VGroup(handle, head, bristles)


def person(color, scale=1.0):
    head = Circle(radius=0.17, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3)
    body = Arc(radius=0.3, start_angle=0, angle=PI, stroke_color=color, stroke_width=3).next_to(head, DOWN, buff=0.05)
    return VGroup(head, body).scale(scale)


class Panel:
    """Axes for a log-velocity sketch: x in log10 cm/s from -1 to 2, y 0..1."""
    X0, X1 = -1.0, 2.0

    def __init__(self, cx, cy, w, h, color, ylabel, xlabel=True):
        self.cx, self.cy, self.w, self.h, self.color = cx, cy, w, h, color
        self.ox, self.oy = cx - w / 2, cy - h / 2
        self.xax = Line([self.ox, self.oy, 0], [self.ox + w, self.oy, 0], color=GREY, stroke_width=3)
        self.yax = Line([self.ox, self.oy, 0], [self.ox, self.oy + h, 0], color=GREY, stroke_width=3)
        self.ylab = T(ylabel, 24, color).rotate(PI / 2).next_to(self.yax, LEFT, buff=0.15)
        self.xlab = T("brush velocity, cm/s (log scale)", 22, GREY).next_to(self.xax, DOWN, buff=0.7) if xlabel else VGroup()
        self.tick1 = M("1", 24, GREY).move_to(self.px(0) + DOWN * 0.3)
        self.tick10 = M("10", 24, GREY).move_to(self.px(1) + DOWN * 0.3)
        self.band = Rectangle(width=self.px(1)[0] - self.px(0)[0], height=h, stroke_width=0,
                              fill_color=YELLOW, fill_opacity=0.14).move_to(
            [(self.px(0)[0] + self.px(1)[0]) / 2, self.oy + h / 2, 0])
        self.sketch = T("in this sketch", 22, GREY).move_to([cx + w / 2 - 1.0, self.oy + h + 0.28, 0])

    def px(self, x, y=0.0):
        return np.array([self.ox + (x - self.X0) / (self.X1 - self.X0) * self.w, self.oy + y * self.h * 0.92, 0])

    def curve(self, color=None):
        return ParametricFunction(lambda t: self.px(t, bell(t)), t_range=[self.X0, self.X1, 0.02],
                                  color=color or self.color, stroke_width=6)

    def dots(self, xs, color=None):
        return VGroup(*[Dot(self.px(x, bell(x)), radius=0.1, color=color or self.color) for x in xs])

    def frame(self):
        return VGroup(self.xax, self.yax, self.ylab, self.xlab, self.tick1, self.tick10)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Hairy skin, stroking and affective touch"
    TITLE = "A match between two curves"


# ---------------------------------------------------------------------------------------------
class S01Brush(SpokenScene):
    """A brush crosses forearm skin at three speeds; one fibre's firing changes; the question."""

    def construct(self):
        skin = skin_bar(-6.2, 0.9, 0.3)
        hairs = VGroup(*[hair(-5.8 + 0.62 * i, 0.55, 0.85, 0.12 * (-1) ** i) for i in range(12)])
        skin_lbl = T("hairy skin of a human forearm", 26, GREY).move_to([-3.0, -0.35, 0])
        ending = Ellipse(width=0.7, height=0.4, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                         fill_opacity=0.35).move_to([0.2, -0.35, 0])
        axon = VMobject(color=GREEN, stroke_width=5).set_points_as_corners(
            [[0.2, -0.55, 0], [0.2, -2.3, 0], [1.5, -2.3, 0]])
        fib_lbl = T("one slow nerve fibre", 26, GREEN).move_to([-2.4, -2.3, 0])
        self.play(FadeIn(skin), Create(hairs), run_time=0.8)
        self.at("soft brush")
        X0 = -5.8
        b = brush(X0, 0.95)
        self.play(FadeIn(b, shift=DOWN * 0.2), FadeIn(skin_lbl), run_time=0.6)
        self.play(FadeIn(ending), Create(axon), FadeIn(fib_lbl), run_time=0.8)

        # three rows of firing, one per stroke (sketch: slow, middle, fast)
        rows = [("slow", 3), ("middle", 12), ("fast", 4)]
        lx, tx0, y0 = 2.45, 3.25, 2.2
        heads, ticks = [], []
        for i, (nm, n) in enumerate(rows):
            y = y0 - 1.15 * i
            heads.append(T(nm, 26, GREY).move_to([lx, y, 0]))
            ticks.append(spikes(n, 2.9, 0.5, GREEN, x0=tx0, seed=i + 3).shift(UP * y))
        note = T("firing, in this sketch", 22, GREY).move_to([4.7, y0 + 0.85, 0])
        link = Arrow([1.5, -2.3, 0], [2.4, -1.6, 0], buff=0.0, color=GREEN, stroke_width=4, tip_length=0.2)
        D = 6.0   # sweep distance

        def back():
            self.play(FadeOut(b), run_time=0.2)
            b.move_to([X0, b.get_center()[1], 0])
            self.play(FadeIn(b), run_time=0.2)

        self.play(FadeIn(note), run_time=0.3)
        t1 = self.t_of("then faster") - 1.5 - self.elapsed()
        self.play(b.animate.shift(RIGHT * D), run_time=max(1.0, t1), rate_func=linear)
        self.play(FadeIn(heads[0]), FadeIn(ticks[0]), FadeIn(link), run_time=0.4)
        back()
        self.at("then faster")
        t2 = max(0.9, (self.t_of("changes how hard") - self.elapsed()) * 0.5)
        self.play(b.animate.shift(RIGHT * D), run_time=t2, rate_func=linear)
        self.play(FadeIn(heads[1]), FadeIn(ticks[1]), run_time=0.3)
        back()
        self.play(b.animate.shift(RIGHT * D), run_time=0.5, rate_func=linear)
        self.play(FadeIn(heads[2]), FadeIn(ticks[2]), FadeOut(b), run_time=0.3)
        self.at("changes how hard")
        self.play(Indicate(VGroup(heads[1], ticks[1]), color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("middle speeds")
        box = SurroundingRectangle(VGroup(heads[1], ticks[1]), color=YELLOW, buff=0.15, stroke_width=4)
        rated = T("rated most pleasant", 24, YELLOW).move_to([4.7, -0.95, 0])
        self.play(Create(box), FadeIn(rated), run_time=0.5)
        self.at("Is that why")
        q = T("?", 96, YELLOW, weight=BOLD).move_to([-3.2, 2.3, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fibre(SpokenScene):
    """Name the fibre, human versus mouse term, electrode through skin into the nerve."""

    def construct(self):
        skin = skin_bar(-6.0, 3.2, 1.9)
        skin_lbl = T("human hairy skin", 24, GREY).next_to(skin, UP, buff=0.12).align_to(skin, LEFT)
        ending = Ellipse(width=0.7, height=0.4, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                         fill_opacity=0.35).move_to([-2.8, 1.35, 0])
        nerve = RoundedRectangle(corner_radius=0.2, width=5.6, height=1.3, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.18).move_to([-3.2, -1.9, 0])
        others = VGroup(*[Line([-5.7, -1.9 + dy, 0], [-0.7, -1.9 + dy, 0], color=GREY, stroke_width=3)
                          for dy in (-0.4, 0.4)])
        axon = VMobject(color=GREEN, stroke_width=5).set_points_as_corners(
            [[-2.8, 1.15, 0], [-2.8, -1.9, 0], [-0.7, -1.9, 0]])
        nerve_lbl = T("nerve", 24, GREY).move_to([-3.2, -3.0, 0])
        self.play(FadeIn(skin), FadeIn(skin_lbl), FadeIn(nerve), FadeIn(others), FadeIn(nerve_lbl), run_time=0.8)
        self.at("is a touch")
        ct = chip("CT afferent", GREEN, size=26).move_to([-5.0, 1.0, 0])
        self.play(FadeIn(ending), Create(axon), run_time=0.8)
        self.play(FadeIn(ct, shift=LEFT * 0.2), run_time=0.5)
        self.at("no insulating wrap")
        wrap = VGroup(T("unmyelinated axon:", 24, GREEN), T("no insulating wrap", 24, GREEN)).arrange(
            DOWN, buff=0.1).move_to([-5.0, -0.1, 0])
        self.play(FadeIn(wrap), run_time=0.6)
        self.at("mouse papers")
        # human term versus mouse term
        mouse = chip("mouse: C-LTMR", ORANGE, size=26).move_to([-4.7, 3.15, 0])
        same = T("same cells? a question for later", 24, GREY).next_to(mouse, RIGHT, buff=0.3)
        self.play(FadeIn(mouse, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(same), run_time=0.5)
        self.at("fine electrode")
        elec = Line([3.6, 3.0, 0], [-1.0, -1.9, 0], color=BLUE, stroke_width=6)
        tip = Dot([-1.0, -1.9, 0], radius=0.09, color=BLUE)
        elec_lbl = T("fine electrode", 26, BLUE).move_to([4.9, 3.0, 0])
        self.play(Create(elec), run_time=1.2)
        self.play(FadeIn(tip), FadeIn(elec_lbl), run_time=0.4)
        self.at("single axons")
        trace_back = VGroup(
            Line([2.8, -2.2, 0], [6.2, -2.2, 0], color=GREY, stroke_width=3),
            T("one axon, in an awake person", 22, GREY).move_to([4.5, -0.6, 0]),
            T("in this sketch", 22, GREY).move_to([4.5, -3.0, 0]))
        sp = VGroup(*[Line([3.2 + 0.55 * k, -2.2, 0], [3.2 + 0.55 * k, -1.2, 0], color=GREEN, stroke_width=4)
                      for k in (0, 1, 2, 4, 5, 7)])
        self.play(FadeIn(trace_back), run_time=0.4)
        self.play(LaggedStart(*[Create(s) for s in sp], lag_ratio=0.2), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Firing(SpokenScene):
    """Firing versus brush velocity builds: points, then the inverted U, then the 1 to 10 cm/s band."""

    def construct(self):
        p = Panel(0.0, -0.45, 9.0, 4.6, GREEN, "CT firing")
        title = T("single CT afferents, human forearm", 28, GREEN).to_edge(UP, buff=0.55)
        self.play(Create(p.xax), Create(p.yax), FadeIn(title), FadeIn(p.sketch), run_time=0.9)
        self.at("stimulus feature")
        self.play(FadeIn(p.xlab), run_time=0.5)
        self.at("controlled velocities")
        sl = T("slower", 24, GREY).next_to(p.px(-1.0, 0), DOWN, buff=0.12).align_to(p.px(-1.0, 0), LEFT)
        fa = T("faster", 24, GREY).next_to(p.px(2.0, 0), DOWN, buff=0.12).align_to(p.px(2.0, 0), RIGHT)
        self.play(FadeIn(sl), FadeIn(fa), FadeIn(p.ylab), run_time=0.6)
        xs = [-0.7, -0.2, 0.3, 0.8, 1.3, 1.8]
        dots = p.dots(xs)
        self.at("healthy volunteers")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.3), run_time=1.8)
        self.at("inverted")
        curve = p.curve()
        self.play(Create(curve), run_time=2.0)
        self.at("highest for strokes")
        self.play(FadeIn(p.band), FadeIn(p.tick1), FadeIn(p.tick10), run_time=0.8)
        lab = T("about 1 to 10 cm/s: highest", 26, YELLOW).move_to([p.px(0.5)[0], p.oy + p.h + 0.3, 0])
        self.play(FadeIn(lab), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rating(SpokenScene):
    """A separate group rates the same strokes; same shape; different people."""

    def construct(self):
        pl = Panel(-3.35, -0.9, 4.6, 3.2, GREEN, "CT firing", xlabel=False)
        pr = Panel(3.35, -0.9, 4.6, 3.2, PURPLE, "rating", xlabel=False)
        cl, cr = pl.curve(), pr.curve()
        left = VGroup(pl.xax, pl.yax, pl.ylab, pl.band, pl.tick1, pl.tick10, cl)
        ppl_l = VGroup(*[person(GREEN, 1.1) for _ in range(3)]).arrange(RIGHT, buff=0.3).move_to([-3.35, 3.0, 0])
        cap_l = T("recorded group", 26, GREEN).next_to(ppl_l, DOWN, buff=0.15)
        xl = T("brush velocity, cm/s (log)", 22, GREY).move_to([0, -3.15, 0])
        self.add(left, ppl_l, cap_l, xl, pl.sketch)
        self.at("second experiment")
        self.play(Create(pr.xax), Create(pr.yax), run_time=0.7)
        self.at("separate group")
        ppl_r = VGroup(*[person(PURPLE, 1.1) for _ in range(3)]).arrange(RIGHT, buff=0.3).move_to([3.35, 3.0, 0])
        cap_r = T("a separate group", 26, PURPLE).next_to(ppl_r, DOWN, buff=0.15)
        self.play(FadeIn(ppl_r, shift=DOWN * 0.2), FadeIn(cap_r), run_time=0.8)
        self.at("rated how pleasant")
        ry = T("pleasantness rating", 24, PURPLE).rotate(PI / 2).next_to(pr.yax, LEFT, buff=0.15)
        self.play(FadeIn(ry), FadeIn(pr.band), FadeIn(pr.tick1), FadeIn(pr.tick10), FadeIn(pr.sketch), run_time=0.7)
        self.at("traced the same")
        self.play(Create(cr), run_time=2.0)
        self.at("different people")
        div = DashedLine([0, 3.4, 0], [0, -2.5, 0], color=RED, stroke_width=4)
        tag = T("different people", 28, RED, weight=BOLD).move_to([0, 2.7, 0])
        tagb = Rectangle(width=tag.width + 0.3, height=tag.height + 0.2, stroke_width=0, fill_color=BG,
                         fill_opacity=1).move_to(tag)
        self.play(Create(div), FadeIn(tagb), FadeIn(tag), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Cause(SpokenScene):
    """Two thermometers; then the two touch curves; then cordotomy rules out one route."""

    def mini(self, cx, cy, color, title, peak_at):
        w, h = 4.2, 2.2
        ox, oy = cx - w / 2, cy - h / 2
        xa = Line([ox, oy, 0], [ox + w, oy, 0], color=GREY, stroke_width=3)
        ya = Line([ox, oy, 0], [ox, oy + h, 0], color=GREY, stroke_width=3)
        c = ParametricFunction(lambda t: [ox + t * w, oy + 0.12 + 0.92 * h * np.exp(-((t - peak_at) / 0.22) ** 2), 0],
                               t_range=[0, 1, 0.01], color=color, stroke_width=6)
        tt = T(title, 26, color).move_to([cx, cy + h / 2 + 0.45, 0])
        return VGroup(xa, ya, c, tt), (ox + peak_at * w, oy)

    def construct(self):
        a, pa = self.mini(-3.4, 0.4, BLUE, "thermometer, room A", 0.5)
        b, pb = self.mini(3.4, 0.4, ORANGE, "thermometer, room B", 0.5)
        self.at("two thermometers")
        self.play(FadeIn(a), FadeIn(b), run_time=1.0)
        self.at("highest at noon")
        noon = VGroup(*[VGroup(DashedLine([p[0], p[1], 0], [p[0], p[1] + 2.0, 0], color=YELLOW, stroke_width=3),
                               T("noon", 24, YELLOW).move_to([p[0], p[1] - 0.35, 0])) for p in (pa, pb)])
        self.play(Create(noon), run_time=0.8)
        self.at("neither shows")
        link = DoubleArrow([-1.1, 0.4, 0], [1.1, 0.4, 0], color=GREY, stroke_width=5)
        x1 = Cross(Line([-0.25, 0.15, 0], [0.25, 0.65, 0]), stroke_color=RED, stroke_width=7).scale(0.9)
        x1.move_to(link)
        lbl = T("causes?", 24, RED).next_to(link, UP, buff=0.4)
        self.play(FadeIn(link), run_time=0.4)
        self.play(FadeIn(lbl), FadeIn(x1), run_time=0.5)
        self.at("same is true")
        self.play(FadeOut(a), FadeOut(b), FadeOut(noon), FadeOut(link), FadeOut(x1), FadeOut(lbl), run_time=0.5)
        # the two touch curves as mini panels
        c1, _ = self.mini(-3.4, 0.4, GREEN, "CT firing", 0.55)
        c2, _ = self.mini(3.4, 0.4, PURPLE, "pleasantness rating", 0.55)
        link2 = DoubleArrow([-1.1, 0.4, 0], [1.1, 0.4, 0], color=GREY, stroke_width=5)
        tag = T("a correspondence", 28, YELLOW, weight=BOLD).move_to([0, -1.6, 0])
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(link2), FadeIn(tag), run_time=0.8)
        self.at("needed for")
        needed = T("CT firing needed for pleasantness?  not shown", 28, RED).move_to([0, -2.6, 0])
        self.play(FadeIn(needed), run_time=0.6)
        self.at("later study")
        self.play(*[FadeOut(m) for m in (c1, c2, link2, tag, needed)], run_time=0.5)
        # the cordotomy box circuit
        skin = chip("brush on forearm skin", YELLOW, size=24).move_to([-4.3, 0.8, 0])
        tract = chip("anterolateral tract", GREY, size=24).move_to([0.0, 1.4, 0])
        rate = chip("pleasantness rating", PURPLE, size=24).move_to([4.3, 0.8, 0])
        a1 = DashedLine(skin.get_right(), tract.get_left(), color=GREY, stroke_width=4).add_tip(tip_length=0.2)
        a2 = DashedLine(tract.get_right(), rate.get_left(), color=GREY, stroke_width=4).add_tip(tip_length=0.2)
        assumed = T("assumed route, in this sketch", 24, GREY).move_to([0, 0.55, 0])
        self.play(FadeIn(skin), FadeIn(tract), FadeIn(rate), Create(a1), Create(a2), FadeIn(assumed), run_time=1.0)
        cut = chip("anterolateral tract", RED, size=24).move_to(tract)
        cut_lbl = T("cut: 19 patients tested before and after", 24, RED).next_to(tract, UP, buff=0.25)
        self.at("did not significantly")
        self.play(Transform(tract, cut), FadeIn(cut_lbl), run_time=0.7)
        unch = VGroup(T("ratings not", 24, PURPLE), T("significantly changed", 24, PURPLE)).arrange(DOWN, buff=0.08).next_to(rate, UP, buff=0.3)
        self.play(FadeIn(unch), run_time=0.6)
        self.at("rules out")
        self.play(Indicate(tract, color=RED, scale_factor=1.1), run_time=0.8)
        self.at("which route")
        unk = chip("route not identified", GREY, size=24).move_to([0.0, -1.9, 0])
        o1 = DashedLine(skin.get_bottom(), unk.get_left(), color=GREY, stroke_width=4)
        o2 = DashedLine(unk.get_right(), rate.get_bottom() + DOWN * 0.0, color=GREY, stroke_width=4)
        self.play(Create(o1), FadeIn(unk), Create(o2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Mouse(SpokenScene):
    """In mouse hairy skin, three candidate populations; the rule."""

    def column(self, cx, kind):
        sk = skin_bar(cx - 1.8, cx + 1.8, 0.0, 0.3)
        shaft = Line([cx, 0.15, 0], [cx, 1.5, 0], color=GREY, stroke_width=5)
        foll = RoundedRectangle(corner_radius=0.1, width=0.28, height=0.9, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.25).move_to([cx, -0.55, 0])
        soma = Circle(radius=0.36, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.3
                      ).move_to([cx, -2.3, 0])
        parts = [sk, shaft, foll, soma]
        ends = VGroup()
        if kind == "c":
            axon = Line([cx, -1.94, 0], [cx - 0.5, -1.1, 0], color=ORANGE, stroke_width=4)
            ends.add(axon)
            for s in (-1, 1):
                for k in range(3):
                    ends.add(Line([cx + s * 0.34, -0.9 + 0.32 * k, 0], [cx + s * 0.34, -0.7 + 0.32 * k, 0],
                                  color=ORANGE, stroke_width=5))
            ends.add(Line([cx - 0.5, -1.1, 0], [cx - 0.34, -0.9, 0], color=ORANGE, stroke_width=4))
        elif kind == "m":
            axon = Line([cx, -1.94, 0], [cx + 0.9, -0.1, 0], color=ORANGE, stroke_width=4)
            tipd = Dot([cx + 0.9, -0.1, 0], radius=0.1, color=ORANGE)
            ends.add(axon, tipd)
        else:
            axon = Line([cx, -1.94, 0], [cx, -1.25, 0], color=ORANGE, stroke_width=5)
            ends.add(axon)
            for k in range(3):
                ends.add(Ellipse(width=0.62, height=0.2, stroke_color=ORANGE, stroke_width=4).move_to(
                    [cx, -0.82 + 0.25 * k, 0]))
        return VGroup(*parts), ends

    def construct(self):
        head = T("in mouse hairy skin", 32, ORANGE).move_to([0, 3.3, 0])
        self.at("mouse hairy skin")
        self.play(FadeIn(head), run_time=0.6)
        specs = [(-4.2, "c", "TH-positive C-LTMR", "lanceolate endings"),
                 (0.0, "m", "MrgprB4 neurons", "unmyelinated, nonpeptidergic"),
                 (4.2, "f", "Aβ field-LTMR", "circumferential endings")]
        cols = []
        self.at("three afferent")
        for i, (cx, kind, nm, sub) in enumerate(specs):
            base, ends = self.column(cx, kind)
            l1 = T(nm, 26, ORANGE, weight=BOLD).move_to([cx, -2.95, 0])
            l2 = T(sub, 22, GREY).move_to([cx, -3.35, 0])
            cols.append((base, ends, l1, l2))
            self.play(FadeIn(base), FadeIn(ends), FadeIn(l1), FadeIn(l2), run_time=0.7)
            if i < 2:
                self.wait(0.5)
        self.at("not the same cells")
        self.play(*[Indicate(VGroup(c[0][3], c[1]), color=YELLOW, scale_factor=1.06) for c in cols], run_time=1.0)
        self.at("a job for")
        self.play(Indicate(cols[2][2], color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("Keep the rule")
        self.play(*[FadeOut(m) for c in cols for m in c], FadeOut(head), run_time=0.6)
        rule = T("Two matching curves are a correspondence.", 40, font=TITLE_FONT).move_to([0, 0.5, 0])
        rule2 = T("They do not show which fibre is needed.", 40, font=TITLE_FONT).move_to([0, -0.5, 0])
        fit(rule, max_w=11.5)
        fit(rule2, max_w=11.5)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.at("do not show")
        self.play(FadeIn(rule2, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Two matching curves do not show which fibre is needed."
