"""Endocrine system: a hormone chain, held in check (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = a hormone (the chemical carried in the blood: CRH, ACTH, cortisol, the testis signal)
  BLUE   = a gland or organ (testis, hypothalamus, pituitary, adrenal cortex)
  TEAL   = a receptor / target cell that responds
  RED    = negative feedback, a cut nerve link, a crossed-out step
  GREEN  = a response that happens (comb, cell responds)
  GREY   = outlines, blood vessel bar, de-emphasized things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tee(a, b, color=RED, w=5):
    """inhibition end: line from a to b with a bar across at b."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def gland(text, color=BLUE, size=30, w=3.3, h=2.0):
    box = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.16)
    lab = T(text, size, color)
    fit(lab, max_w=w - 0.3)
    return VGroup(box, lab.move_to(box))


def hdot(color=YELLOW, r=0.14):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def cross(center, s=0.3, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7))


# positions of the stress-axis chain, shared by s03, s04, s06
HX, PX, AX = -4.5, 0.0, 4.5
CY = 0.9
FB_Y = -2.7


def chain(show=True):
    hyp = gland("Hypothalamus").move_to([HX, CY, 0])
    pit = gland("Anterior pituitary").move_to([PX, CY, 0])
    adr = gland("Adrenal cortex").move_to([AX, CY, 0])
    a1 = arr(hyp.get_right(), pit.get_left(), YELLOW)
    a2 = arr(pit.get_right(), adr.get_left(), YELLOW)
    l1 = T("CRH", 28, YELLOW).next_to(a1, UP, buff=0.12)
    l2 = T("ACTH", 28, YELLOW).next_to(a2, UP, buff=0.12)
    cort = bchip("cortisol", YELLOW, 30).move_to([AX, -1.5, 0])
    a3 = arr(adr.get_bottom(), cort.get_top(), YELLOW)
    return dict(hyp=hyp, pit=pit, adr=adr, a1=a1, a2=a2, l1=l1, l2=l2, cort=cort, a3=a3)


def feedback(c):
    """red feedback: from cortisol chip left along FB_Y, up into hypothalamus and pituitary."""
    p0 = [AX, c["cort"].get_bottom()[1], 0]
    stem = Line(p0, [AX, FB_Y, 0], color=RED, stroke_width=5)
    bar = Line([AX, FB_Y, 0], [HX, FB_Y, 0], color=RED, stroke_width=5)
    up_h = tee([HX, FB_Y, 0], c["hyp"].get_bottom(), RED)
    up_p = tee([PX, FB_Y, 0], c["pit"].get_bottom(), RED)
    lab = T("negative feedback", 28, RED).move_to([(HX + PX) / 2, FB_Y - 0.5, 0])
    return stem, bar, up_h, up_p, lab


class S00Title(TitleCard):
    LESSON = "Hormones and the endocrine system"
    TITLE = "A hormone chain, held in check"


# ---------------------------------------------------------------------------------------------
class S01Rooster(SpokenScene):
    def construct(self):
        body = RoundedRectangle(corner_radius=0.5, width=11.0, height=6.2, stroke_color=GREY, stroke_width=4)
        body.move_to([0.0, -0.1, 0])
        body_l = T("young rooster, castrated", 26, GREY).move_to([-3.2, -2.75, 0])
        testis = bchip("testis", BLUE, 32).move_to([-6.0, 1.0, 0])
        abd = T("abdomen", 26, GREY).move_to([-3.9, -2.1, 0])
        self.at("castrated young roosters")
        self.play(Create(body), FadeIn(body_l), run_time=0.9)
        self.at("put a testis back")
        self.play(FadeIn(testis, shift=RIGHT * 0.2), run_time=0.5)
        self.at("into the belly")
        self.play(testis.animate.move_to([-3.9, -1.3, 0]), FadeIn(abd), run_time=1.3)
        comb = bchip("comb", GREEN, 32).move_to([3.8, 1.7, 0])
        comb[1].set_stroke(opacity=0.3); comb[1].set_fill(opacity=0.05); comb[2].set_opacity(0.3)
        self.add(comb)
        nerve = DashedLine([-3.2, -0.7, 0], [3.4, 1.2, 0], color=RED, stroke_width=4)
        nlab = T("original nerves cut", 28, RED).move_to([-0.8, 0.9, 0])
        self.at("cut off from its")
        self.play(Create(nerve), run_time=0.5)
        self.play(FadeIn(cross([0.1, 0.25, 0])), FadeIn(nlab), run_time=0.5)
        self.at("grew combs")
        self.play(comb[1].animate.set_stroke(GREEN, opacity=1).set_fill(GREEN, 0.3), comb[2].animate.set_opacity(1), run_time=0.5)
        self.play(Indicate(comb[2], color=GREEN, scale_factor=1.15), run_time=0.6)
        q = T("How, without its own nerves?", 34, YELLOW, font=TITLE_FONT).move_to([-1.2, 2.2, 0])
        self.at("How can an organ")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        vessel = RoundedRectangle(corner_radius=0.12, width=6.9, height=0.34, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.3).move_to([0.35, -1.3, 0])
        vlab = T("blood", 28, GREY).next_to(vessel, DOWN, buff=0.15)
        up = Line([3.8, -1.3, 0], [3.8, 1.1, 0], color=GREY, stroke_width=8)
        self.at("carried in the blood")
        self.play(FadeOut(q), FadeIn(vessel), FadeIn(vlab), run_time=0.6)
        self.play(Create(up), run_time=0.4)
        dots = VGroup(*[hdot() for _ in range(4)])
        for d in dots:
            d.move_to([-3.0, -1.3, 0])
        self.add(dots)
        path = [[-3.0, -1.3, 0], [3.8, -1.3, 0], [3.8, 1.1, 0]]
        anims = [Succession(Wait(0.4 * i), MoveAlongPath(d, VMobject().set_points_as_corners(path), run_time=2.6, rate_func=linear))
                 for i, d in enumerate(dots)]
        self.play(*anims)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Hormone(SpokenScene):
    def construct(self):
        head = T("A hormone", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=0.8)
        VY = 1.9
        g = gland("gland cells", w=2.6, h=1.3, size=28).move_to([-5.0, VY, 0])
        vessel = RoundedRectangle(corner_radius=0.14, width=10.0, height=0.55, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.28).move_to([1.2, VY, 0])
        vlab = T("blood", 28, GREY).next_to(vessel, UP, buff=0.12).align_to(vessel, RIGHT)
        self.at("one group of cells")
        self.play(FadeIn(g), run_time=0.5)
        self.at("releases into the blood")
        self.play(FadeIn(vessel), FadeIn(vlab), run_time=0.5)
        dots = VGroup(*[hdot() for _ in range(5)])
        for d in dots:
            d.move_to([-3.4, VY, 0])
        self.add(dots)
        hl = T("hormone", 28, YELLOW).move_to([-2.2, VY + 0.8, 0])
        self.play(FadeIn(hl), *[Succession(Wait(0.2 * i), d.animate.move_to([-3.0 + 1.2 * i, VY, 0]).set_run_time(0.6)) for i, d in enumerate(dots)])
        xs = [-3.9, 0.3, 4.5]
        cells = []
        for x in xs:
            cells.append(RoundedRectangle(corner_radius=0.3, width=3.2, height=2.0, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.12).move_to([x, -1.3, 0]))
        self.at("distant target cells")
        self.play(*[FadeIn(c) for c in cells], run_time=0.7)
        lab_cells = T("target cells", 28, GREY).move_to([0.3, -3.0, 0])
        self.play(FadeIn(lab_cells), run_time=0.3)
        cups = []
        for i in (0, 1):
            cups.append(Arc(radius=0.4, start_angle=PI, angle=PI, color=TEAL, stroke_width=7).move_to(
                [xs[i], cells[i].get_top()[1] + 0.14, 0]))
        self.at("have receptors for it")
        self.play(*[Create(c) for c in cups], run_time=0.6)
        rl = T("receptor", 28, TEAL).move_to([(xs[0] + xs[1]) / 2, 0.45, 0])
        self.play(FadeIn(rl), run_time=0.4)
        self.at("binds the hormone")
        d0 = hdot().move_to(dots[1].get_center())
        d1 = hdot().move_to(dots[3].get_center())
        self.add(d0, d1)
        self.play(d0.animate.move_to([xs[0], cells[0].get_top()[1] + 0.42, 0]),
                  d1.animate.move_to([xs[1], cells[1].get_top()[1] + 0.42, 0]), run_time=0.9)
        self.at("changes what the cell does")
        self.play(*[cells[i].animate.set_stroke(GREEN).set_fill(GREEN, 0.3) for i in (0, 1)], run_time=0.5)
        r1 = T("responds", 28, GREEN).move_to([xs[0], -1.3, 0])
        r2 = T("responds", 28, GREEN).move_to([xs[1], -1.3, 0])
        self.play(FadeIn(r1), FadeIn(r2), run_time=0.4)
        self.at("radio broadcast")
        d2 = hdot().move_to(dots[4].get_center())
        self.add(d2)
        self.play(d2.animate.move_to([xs[2], cells[2].get_top()[1] + 0.42, 0]), run_time=0.8)
        nr = T("no receptor,\nno response", 26, GREY).move_to([xs[2], -1.3, 0])
        self.play(FadeIn(nr), FadeOut(d2), run_time=0.5)
        self.at("only houses with a tuned set")
        self.play(Indicate(VGroup(cells[0], cells[1], r1, r2), color=GREEN, scale_factor=1.04), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Chain(SpokenScene):
    def construct(self):
        head = T("The stress axis, in humans", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=0.8)
        c = chain()
        brain = T("base of the brain", 24, GREY).next_to(c["hyp"], DOWN, buff=0.18)
        self.at("the hypothalamus sits")
        self.play(FadeIn(c["hyp"], shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(brain), run_time=0.4)
        self.at("controls the pituitary gland")
        self.play(FadeIn(c["pit"], shift=DOWN * 0.1), run_time=0.6)
        self.at("the stress axis")
        self.play(Indicate(head, color=GOLD, scale_factor=1.05), run_time=0.6)
        self.at("releases")
        self.play(GrowArrow(c["a1"]), FadeIn(c["l1"]), c["hyp"][0].animate.set_fill(BLUE, 0.4), run_time=0.7)
        self.play(c["pit"][0].animate.set_fill(BLUE, 0.4), run_time=0.4)
        self.at("makes the adrenal cortex")
        self.play(FadeIn(c["adr"], shift=DOWN * 0.1), GrowArrow(c["a2"]), FadeIn(c["l2"]), run_time=0.8)
        self.play(c["adr"][0].animate.set_fill(BLUE, 0.4), run_time=0.4)
        self.at("produce cortisol")
        self.play(GrowArrow(c["a3"]), FadeIn(c["cort"], shift=DOWN * 0.2), run_time=0.8)
        self.wait(0.8)
        self.finish()


def build_full():
    c = chain()
    fb = feedback(c)
    return c, fb


def static_chain(scene, c, with_fb=None):
    scene.add(c["hyp"], c["pit"], c["adr"], c["a1"], c["a2"], c["l1"], c["l2"], c["a3"], c["cort"])
    for (k, o) in (("hyp", 0.4), ("pit", 0.4), ("adr", 0.4)):
        c[k][0].set_fill(BLUE, o)


# ---------------------------------------------------------------------------------------------
class S04Feedback(SpokenScene):
    def construct(self):
        head = T("The stress axis, in humans", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.add(head)
        c, (stem, bar, up_h, up_p, lab) = build_full()
        static_chain(self, c)
        self.at("the loop closes")
        self.play(Indicate(c["cort"][2], color=YELLOW, scale_factor=1.2), run_time=0.7)
        self.at("rising cortisol lowers")
        self.play(Create(stem), run_time=0.4)
        self.play(Create(bar), run_time=0.9)
        self.play(Create(up_p), run_time=0.4)
        self.play(Create(up_h), run_time=0.4)
        self.play(*[o.animate.set_opacity(0.3) for o in (c["a1"], c["a2"], c["l1"], c["l2"])], run_time=0.6)
        self.at("negative feedback")
        self.play(FadeIn(lab), run_time=0.5)
        opp = T("opposes the change that caused it", 26, RED).move_to([3.0, FB_Y - 0.5, 0])
        self.at("opposes the change")
        self.play(FadeIn(opp), run_time=0.5)
        self.at("reduces the drive")
        self.play(*[o.animate.set_opacity(0.3) for o in (c["a1"], c["a2"], c["l1"], c["l2"])], run_time=0.3)
        self.at("both the hypothalamus")
        self.play(Indicate(up_h, color=RED, scale_factor=1.3), Indicate(up_p, color=RED, scale_factor=1.3), run_time=0.9)
        self.wait(0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Timing(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.2, 0.2], x_length=10.5, y_length=3.6,
                  axis_config={"color": GREY, "include_ticks": False, "include_tip": False, "stroke_width": 3})
        ax.move_to([0.4, -0.2, 0])
        xl = T("time over a day", 26, GREY).next_to(ax, DOWN, buff=0.2)
        yl = T("cortisol", 26, YELLOW).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        sk = T("in this sketch, relative units", 24, GREY).next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)
        def f_day(x):
            return 0.55 + 0.35 * np.cos((x / 10) * 2 * PI - 0.6)
        def f_pulse(x):
            return f_day(x) + 0.09 * np.sin(x * 2 * PI / 0.52) * (0.4 + 0.6 * f_day(x))
        head = T("Feedback does not fix a level", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=0.8)
        self.at("one fixed value")
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sk), run_time=0.8)
        flat = ax.plot(lambda x: 0.55, x_range=[0, 10], color=GREY, stroke_width=4)
        flat.set_stroke(opacity=0.0)
        self.add(flat)
        day = ax.plot(f_day, x_range=[0, 10], color=YELLOW, stroke_width=5)
        self.at("rises and falls over the day")
        self.play(Create(day), run_time=2.2, rate_func=linear)
        pulses = ax.plot(f_pulse, x_range=[0, 10, 0.02], color=YELLOW, stroke_width=4)
        self.at("pulses")
        self.play(ReplacementTransform(day, pulses), run_time=1.2)
        # one pulse period in this sketch: 0.52 of the 10 units that span the day
        p1x = 0.52 * 5 + 0.13
        a = ax.c2p(p1x, 1.15)[0]
        b = ax.c2p(p1x + 0.52, 1.15)[0]
        by = ax.c2p(0, 1.2)[1] + 0.45
        br = VGroup(Line([a, by, 0], [b, by, 0], color=GOLD, stroke_width=4),
                    Line([a, by - 0.12, 0], [a, by + 0.12, 0], color=GOLD, stroke_width=4),
                    Line([b, by - 0.12, 0], [b, by + 0.12, 0], color=GOLD, stroke_width=4))
        pl = T("pulses roughly every 60 to 90 minutes, in humans", 26, GOLD).move_to([(a + b) / 2, by + 0.5, 0])
        g1 = DashedLine([a, by - 0.12, 0], ax.c2p(p1x, f_pulse(p1x)), color=GOLD, stroke_width=2)
        g2 = DashedLine([b, by - 0.12, 0], ax.c2p(p1x + 0.52, f_pulse(p1x + 0.52)), color=GOLD, stroke_width=2)
        self.at("roughly every")
        self.play(Create(br), FadeIn(pl), Create(g1), Create(g2), run_time=0.7)
        # study panel
        self.at("In a study")
        self.play(*[FadeOut(o) for o in (ax, xl, yl, sk, pulses, br, pl, head, flat, g1, g2)], run_time=0.6)
        h2 = T("A study of 15 healthy men", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        blocked = bchip("own cortisol blocked", RED, 30).move_to([-4.3, 1.9, 0])
        dose = bchip("same daily dose", YELLOW, 30).move_to([-4.3, -0.2, 0])
        s1 = bchip("schedule 1", GREY, 30).move_to([0.2, 1.1, 0])
        s2 = bchip("schedule 2", GREY, 30).move_to([0.2, -1.5, 0])
        out = bchip("brain response to\nemotional stimuli\nchanged", GREEN, 28).move_to([4.5, -0.2, 0])
        self.play(Write(h2), FadeIn(blocked), run_time=0.8)
        self.at("same daily dose")
        self.play(FadeIn(dose), GrowArrow(arr(blocked.get_bottom(), dose.get_top(), GREY)), run_time=0.5)
        self.at("different schedules")
        sa1 = arr(dose.get_right(), s1.get_left(), YELLOW)
        sa2 = arr(dose.get_right(), s2.get_left(), YELLOW)
        self.play(GrowArrow(sa1), GrowArrow(sa2), FadeIn(s1), FadeIn(s2), run_time=0.8)
        self.at("how their brains responded")
        oa1 = arr(s1.get_right(), out.get_left(), GREEN)
        oa2 = arr(s2.get_right(), out.get_left(), GREEN)
        self.play(GrowArrow(oa1), GrowArrow(oa2), FadeIn(out), run_time=0.9)
        self.at("Timing carries information")
        self.play(Indicate(VGroup(s1, s2), color=GOLD, scale_factor=1.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        head = T("Same logic, different molecules", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=0.8)
        r1l = T("the bug Rhodnius prolixus", 32, WHITE)
        r1l.move_to([-6.2 + r1l.width / 2, 1.9, 0])
        r2l = T("frog tadpoles", 32, WHITE)
        r2l.move_to([-6.2 + r2l.width / 2, -0.9, 0])
        h1 = bchip("signal from the head", YELLOW, 36).move_to([-3.4, 0.8, 0])
        b1 = bchip("in the blood", GREY, 36).move_to([1.7, 0.8, 0])
        m1 = bchip("moult", GREEN, 36).move_to([5.0, 0.8, 0])
        a1 = arr(h1.get_right(), b1.get_left(), GREY)
        a2 = arr(b1.get_right(), m1.get_left(), GREY)
        t1 = bchip("thyroid hormone", YELLOW, 36).move_to([-3.6, -2.0, 0])
        m2 = bchip("metamorphosis", GREEN, 36).move_to([1.8, -2.0, 0])
        a3 = arr(t1.get_right(), m2.get_left(), GREY)
        self.at("name the animal")
        self.play(FadeIn(r1l), FadeIn(r2l), run_time=0.5)
        self.at("the bug")
        self.play(FadeIn(h1), run_time=0.5)
        self.at("travels in the blood")
        self.play(GrowArrow(a1), FadeIn(b1), run_time=0.6)
        self.at("is needed for the")
        self.play(GrowArrow(a2), FadeIn(m1), run_time=0.6)
        self.at("frog tadpoles")
        self.play(FadeIn(t1), run_time=0.5)
        self.at("drives metamorphosis")
        self.play(GrowArrow(a3), FadeIn(m2), run_time=0.6)
        self.at("To read any loop")
        self.play(*[FadeOut(o) for o in (r1l, r2l, h1, b1, m1, a1, a2, t1, m2, a3)], run_time=0.6)
        head2 = T("The stress axis, in humans", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        c, (stem, bar, up_h, up_p, lab) = build_full()
        fbs = [stem, bar, up_h, up_p]
        self.play(ReplacementTransform(head, head2),
                  *[FadeIn(o) for o in (c["hyp"], c["pit"], c["adr"], c["a1"], c["a2"], c["l1"], c["l2"], c["a3"], c["cort"], *fbs)],
                  run_time=0.9)
        self.at("remove or add one hormone")
        x = cross(c["cort"].get_center(), 0.5)
        self.play(Create(x), c["cort"].animate.set_opacity(0.35), *[o.animate.set_opacity(0.25) for o in fbs], run_time=0.7)
        qs = [T("?", 48, GOLD, weight=BOLD).move_to([HX, CY + 1.3, 0]), T("?", 48, GOLD, weight=BOLD).move_to([PX, CY + 1.3, 0])]
        self.at("predict the rest")
        self.play(*[FadeIn(q, scale=1.3) for q in qs], run_time=0.6)
        self.wait(0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Remove or add one hormone, then predict the rest of its loop."
