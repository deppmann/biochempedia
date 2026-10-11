"""Toronto, 1921 to 1922: four names behind the first insulin (section film, pi3k-akt-insulin)

COLOR MAP (one color per concept, whole film)
  BLUE   = a named person (chips)
  GOLD   = the active substance / the extract / the drug
  GREY   = tissue, impurities, outlines, dates, de-emphasised things
  RED    = blood sugar curves, and the problems (unsafe, abscess)
  YELLOW = a highlight ring or pulse on whatever the narrator is naming
  TEAL   = the receptor fact (1982)
All curves and tissue are idealised sketches, labelled as such.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

TLX = [-5.2, -3.1, -1.0, 1.1, 3.2, 5.3]
TLN = ["Nov 1920", "Summer 1921", "11 Jan 1922", "23 Jan 1922", "1923", "1982"]


def pchip(name, subs=(), color=BLUE, size=26, sub_size=22):
    n = T(name, size, color, weight=BOLD)
    ss = [T(s, sub_size, GREY) for s in subs]
    col = VGroup(n, *ss).arrange(DOWN, buff=0.1)
    box = RoundedRectangle(corner_radius=0.14, width=col.width + 0.5, height=col.height + 0.4,
                           stroke_color=color, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    box_fill = box.copy().set_fill(color, 0.14)
    col.move_to(box)
    return VGroup(box, box_fill, col)


def tl_base():
    return Line([-6.0, -3.45, 0], [6.0, -3.45, 0], color=GREY, stroke_width=2).set_opacity(0.5)


def tl_tick(i, on=True):
    c = TEXT if on else GREY
    d = Dot([TLX[i], -3.45, 0], radius=0.09, color=c)
    t = T(TLN[i], 22, c).move_to([TLX[i], -3.0, 0])
    return VGroup(d, t)


def sugar(center, frac, label="blood sugar", w=3.4, h=2.0):
    x0, y0 = center[0] - w / 2, center[1] - h / 2
    ax = VGroup(Line([x0, y0, 0], [x0, y0 + h, 0], color=GREY, stroke_width=3),
                Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY, stroke_width=3))
    ys = y0 + h - 0.15
    ye = ys - frac * (h - 0.15)
    xs = np.linspace(x0 + 0.1, x0 + w, 40)
    ss = lambda u: u * u * (3 - 2 * u)
    pts = []
    for x in xs:
        u = (x - (x0 + 0.1)) / (w - 0.1)
        v = 0 if u < 0.3 else ss(min(1, (u - 0.3) / 0.6))
        pts.append([x, ys + (ye - ys) * v, 0])
    curve = VMobject(color=RED, stroke_width=6)
    curve.set_points_as_corners(pts)
    base = DashedLine([x0 + 0.1, ys, 0], [x0 + w, ys, 0], color=GREY, stroke_width=2).set_opacity(0.6)
    cap = T(label, 24, RED).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
    ide = T("idealised, not to scale", 22, GREY).next_to(ax, DOWN, buff=0.12).align_to(ax, LEFT)
    g = VGroup(ax, base, cap, ide)
    g.curve = curve
    return g


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "PI3K, AKT and insulin"
    TITLE = "Four Names Behind the First Insulin"


# ------------------------------------------------------------------------------------------
class S01Idea(SpokenScene):
    def construct(self):
        tline = tl_base()
        self.add(tline)
        pc = np.array([-2.6, 0.4, 0])
        outline = Ellipse(width=4.6, height=2.6, stroke_color=GREY, stroke_width=3).move_to(pc)
        tissue = Ellipse(width=4.6, height=2.6, stroke_width=0, fill_color=GREY, fill_opacity=0.32).move_to(pc)
        lbl = T("pancreas", 28, TEXT).next_to(outline, UP, buff=0.15)
        self.at("The pancreas")
        self.play(FadeIn(tissue), Create(outline), FadeIn(lbl), run_time=0.8)
        enz = T("enzyme-making tissue", 22, TEXT).move_to(pc + DOWN * 0.55)
        self.at("digestive enzymes")
        self.play(FadeIn(enz), run_time=0.5)
        rng = np.random.RandomState(4)
        spots = [(-0.9, 0.55), (0.2, 0.7), (-0.2, 0.15), (0.7, 0.25), (-1.3, 0.05)]
        isl = VGroup(*[Circle(radius=0.17, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.95)
                       .move_to(pc + np.array([x, y, 0])) for x, y in spots])
        isl_t = T("islets", 26, GOLD).move_to([-5.6, 1.7, 0])
        lead = Line(isl_t.get_right() + RIGHT * 0.05, isl[4].get_center() + UP * 0.12 + LEFT * 0.1, color=GOLD, stroke_width=2)
        self.at("in islets")
        self.play(LaggedStart(*[GrowFromCenter(i) for i in isl], lag_ratio=0.15), FadeIn(isl_t), Create(lead), run_time=1.0)
        hor = chip("hormone", GOLD, size=26).move_to([4.2, 1.7, 0])
        dot = Circle(radius=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(isl[3])
        ha = arrow([-1.0, 1.2, 0], hor.get_left() + LEFT * 0.0, GOLD)
        self.at("a hormone")
        self.play(FadeIn(hor), GrowArrow(ha), dot.animate.move_to(hor.get_left() + LEFT * 0.3), run_time=1.0)
        self.play(FadeOut(dot), run_time=0.2)
        ext = chip("extract lowers blood sugar", GOLD, size=22).move_to([4.0, 0.2, 0])
        self.at("extracts lowered")
        self.play(FadeIn(ext, shift=UP * 0.2), run_time=0.6)
        safe = chip("safe for a patient", GREY, size=22).move_to([4.0, -1.1, 0])
        xx = Line(safe.get_left() + LEFT * 0.15, safe.get_right() + RIGHT * 0.15, color=RED, stroke_width=6)
        self.at("none was safe")
        self.play(FadeIn(safe), run_time=0.4)
        self.at("for patients")
        self.play(Create(xx), safe[0].animate.set_stroke(RED), run_time=0.5)

        # ---- the idea --------------------------------------------------------------
        self.at("In November")
        self.play(FadeOut(hor), FadeOut(ha), FadeOut(ext), FadeOut(safe), FadeOut(xx), FadeIn(tl_tick(0)), run_time=0.7)
        ban = pchip("Frederick Banting", ["surgeon, no research training"]).move_to([3.4, 1.7, 0])
        mac = pchip("John Macleod", ["professor, Toronto"]).move_to([3.4, -0.5, 0])
        self.at("Frederick Banting")
        self.play(FadeIn(ban, shift=LEFT * 0.2), run_time=0.6)
        idea = arrow(ban.get_bottom(), mac.get_top(), YELLOW)
        idea_t = T("an idea", 24, YELLOW).next_to(idea, RIGHT, buff=0.15)
        self.at("took an idea")
        self.play(GrowArrow(idea), FadeIn(idea_t), run_time=0.6)
        self.at("John McLeod")
        self.play(FadeIn(mac, shift=UP * 0.2), run_time=0.6)
        duct = Line(pc + RIGHT * 2.3, pc + RIGHT * 3.6 + UP * 0.0, color=GREY, stroke_width=8)
        duct = Line([-0.3, 0.4, 0], [0.9, 0.4, 0], color=GREY, stroke_width=8)
        duct_t = T("duct", 22, GREY).move_to([0.05, 0.78, 0])
        dogs = T("in dogs (idealised drawing)", 22, GREY).move_to([-2.6, -1.45, 0])
        tie = Line([0.72, 0.1, 0], [0.72, 0.7, 0], color=YELLOW, stroke_width=9)
        self.at("Tie off")
        self.play(FadeIn(duct), FadeIn(duct_t), FadeIn(dogs), run_time=0.4)
        self.play(Create(tie), run_time=0.4)
        self.at("wastes away")
        self.play(FadeOut(tissue), FadeOut(enz), run_time=1.2)
        ring = SurroundingRectangle(isl, color=YELLOW, buff=0.22, corner_radius=0.2, stroke_width=4)
        left = T("what is left", 24, YELLOW).next_to(ring, DOWN, buff=0.12)
        self.at("extract what is left")
        self.play(Create(ring), FadeIn(left), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
class S02Dogs(SpokenScene):
    def construct(self):
        tline = tl_base()
        self.add(tline, tl_tick(0, on=False))
        mac = pchip("John Macleod", ["professor"]).move_to([-4.3, 2.3, 0])
        ban = pchip("Frederick Banting").move_to([4.3, 2.3, 0])
        self.at("Macleod gave")
        self.play(FadeIn(mac), FadeIn(ban), run_time=0.6)
        a = chip("laboratory space", GREY, size=24)
        b = chip("dogs", GREY, size=24)
        c = chip("two student assistants", GREY, size=24)
        row = VGroup(a, b, c).arrange(RIGHT, buff=0.4).move_to([0, 0.5, 0])
        gv = arrow(mac.get_bottom(), [-4.3, 1.1, 0], GREY)
        self.at("space")
        self.play(FadeIn(a, shift=DOWN * 0.2), run_time=0.5)
        self.at("dogs")
        self.play(FadeIn(b, shift=DOWN * 0.2), run_time=0.5)
        self.at("two student assistants")
        self.play(FadeIn(c, shift=DOWN * 0.2), run_time=0.5)
        s1 = chip("student assistant", GREY, size=26).move_to([-2.0, 0.5, 0])
        s2 = chip("student assistant", GREY, size=26).move_to([2.0, 0.5, 0])
        self.at("One was")
        self.play(FadeOut(a), FadeOut(b), FadeOut(c), FadeIn(s1), FadeIn(s2), run_time=0.6)
        best = pchip("Charles Best", size=26).move_to(s1.get_center())
        self.at("Charles Best")
        self.play(ReplacementTransform(s1, best), run_time=0.6)
        # ---- summer 1921 ---------------------------------------------------------------
        self.at("summer")
        self.play(FadeOut(mac), FadeOut(s2), FadeOut(best), FadeOut(ban), FadeIn(tl_tick(1)), run_time=0.7)
        ban2 = pchip("Banting").move_to([-5.0, 1.7, 0])
        best2 = pchip("Best").move_to([-5.0, 0.0, 0])
        ex = chip("extract", GOLD, size=26).move_to([-2.5, 0.85, 0])
        a1 = arrow(ban2.get_right(), ex.get_left(), GOLD)
        a2 = arrow(best2.get_right(), ex.get_left(), GOLD)
        self.at("Banting and Best made")
        self.play(FadeIn(ban2), FadeIn(best2), run_time=0.5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(ex), run_time=0.7)
        dog = chip("diabetic dogs", GREY, size=24).move_to([0.2, 0.85, 0])
        sg = sugar([4.3, 0.85, 0], 0.5, "dogs: blood sugar", w=2.9)
        a3 = arrow(ex.get_right(), dog.get_left(), GOLD)
        a4 = arrow(dog.get_right(), [2.85, 0.85, 0], GREY)
        self.at("lowered blood sugar")
        self.play(FadeIn(dog), GrowArrow(a3), GrowArrow(a4), FadeIn(sg), run_time=0.6)
        self.play(Create(sg.curve), run_time=1.2)
        # ---- 11 January 1922 -------------------------------------------------------------
        self.at("extract went into")
        self.play(*[FadeOut(m) for m in (ban2, best2, ex, a1, a2, a3, a4, dog, sg, sg.curve)], FadeIn(tl_tick(2)), run_time=0.7)
        th = pchip("Leonard Thompson", ["early teens"]).move_to([-3.4, 1.2, 0])
        ex2 = chip("their extract", GOLD, size=24).move_to([-3.4, -0.4, 0])
        inj = arrow(ex2.get_top(), th.get_bottom(), GOLD)
        self.play(FadeIn(th), FadeIn(ex2), run_time=0.5)
        self.play(GrowArrow(inj), run_time=0.4)
        sg2 = sugar([3.6, 1.0, 0], 0.15, "Leonard: blood sugar")
        self.at("blood sugar fell a little")
        self.play(FadeIn(sg2), run_time=0.4)
        self.play(Create(sg2.curve), run_time=1.0)
        ab = chip("abscess at injection site", RED, size=22).move_to([3.6, -1.2, 0])
        self.at("abscess formed")
        self.play(FadeIn(ab, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------
def beaker(center):
    rng = np.random.RandomState(7)
    body = RoundedRectangle(corner_radius=0.18, width=2.4, height=3.0, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.08).move_to(center)
    golds, greys = [], []
    for i in range(6):
        p = center + np.array([rng.uniform(-0.8, 0.8), rng.uniform(-1.0, 1.1), 0])
        golds.append(Circle(radius=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(p))
    for i in range(8):
        p = center + np.array([rng.uniform(-0.85, 0.85), rng.uniform(-1.1, 1.1), 0])
        greys.append(Circle(radius=0.09, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(p))
    return body, VGroup(*golds), VGroup(*greys)


class S03Collip(SpokenScene):
    def construct(self):
        self.add(tl_base(), tl_tick(0, on=False), tl_tick(1, on=False), tl_tick(2, on=False))
        bc = np.array([-4.2, 0.2, 0])
        body, golds, greys = beaker(bc)
        cap = T("the extract", 26, GOLD).next_to(body, UP, buff=0.15)
        self.at("The extract")
        self.play(FadeIn(body), FadeIn(golds), FadeIn(greys), FadeIn(cap), run_time=0.8)
        at = T("active substance", 24, GOLD).move_to([-0.5, 1.4, 0])
        al = Line(at.get_left() + LEFT * 0.05, golds[0].get_center(), color=GOLD, stroke_width=2)
        it = T("impurities", 24, GREY).move_to([-0.5, 0.2, 0])
        il = Line(it.get_left() + LEFT * 0.05, greys[0].get_center(), color=GREY, stroke_width=2)
        self.at("too impure")
        self.play(Indicate(greys, color=WHITE, scale_factor=1.6), FadeIn(it), Create(il), run_time=0.8)
        col = pchip("James Collip", ["biochemist, visiting from Alberta", "joined the group in December"]).move_to([3.4, 2.2, 0])
        self.at("James Collop")
        self.play(FadeOut(it), FadeOut(il), FadeIn(col, shift=LEFT * 0.2), run_time=0.8)
        # alcohol steps
        steps = VGroup()
        for i in range(3):
            r = Rectangle(width=0.9, height=0.5 + 0.5 * i, stroke_color=YELLOW, stroke_width=3,
                          fill_color=YELLOW, fill_opacity=0.25)
            steps.add(r)
        steps.arrange(RIGHT, buff=0.12, aligned_edge=DOWN).move_to([2.3, -0.2, 0])
        stl = T("alcohol concentration", 24, YELLOW).next_to(steps, UP, buff=0.2)
        stl2 = T("raised in steps", 24, YELLOW).next_to(steps, DOWN, buff=0.15)
        self.at("raised the alcohol")
        self.play(FadeIn(stl), FadeIn(stl2), run_time=0.4)
        bottom = bc[1] - 1.2
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in steps], lag_ratio=0.5), run_time=1.6)
        self.at("Impurities dropped")
        anims = []
        for k, d in enumerate(greys):
            anims.append(d.animate.move_to([bc[0] - 0.9 + 0.26 * k, bottom + 0.05, 0]).set_opacity(0.6))
        self.play(LaggedStart(*anims, lag_ratio=0.12), run_time=1.6)
        sol = T("impurities drop out", 22, GREY).move_to([-4.2, -1.8, 0])
        self.play(FadeIn(sol), run_time=0.3)
        self.at("the active substance")
        self.play(Indicate(golds, color=YELLOW, scale_factor=1.4), FadeIn(at), Create(al), run_time=0.8)
        self.at("tested each batch")
        self.play(FadeOut(steps), FadeOut(stl), FadeOut(stl2), FadeOut(sol), FadeOut(at), FadeOut(al), run_time=0.4)
        rab = chip("tested on rabbits", BLUE if False else GREY, size=26).move_to([1.4, 0.2, 0])
        ra = arrow(body.get_right() + RIGHT * 0.1, rab.get_left(), GREY)
        self.play(FadeIn(rab), GrowArrow(ra), run_time=0.6)
        bt = T("each batch", 22, GREY).next_to(ra, UP, buff=0.1)
        self.play(FadeIn(bt), run_time=0.3)
        # ---- 23 January ------------------------------------------------------------------
        self.at("same boy")
        self.play(FadeOut(rab), FadeOut(ra), FadeOut(bt), FadeOut(col), FadeIn(tl_tick(3)), run_time=0.6)
        th = pchip("Leonard Thompson", ["the same boy"]).move_to([-0.2, 1.4, 0])
        ar = arrow(body.get_right() + RIGHT * 0.1, th.get_left(), GOLD)
        self.play(FadeIn(th), GrowArrow(ar), run_time=0.6)
        sg = sugar([4.0, 0.6, 0], 0.75, "Leonard: blood sugar")
        self.play(FadeIn(sg), run_time=0.4)
        self.at("blood sugar fell")
        self.play(Create(sg.curve), run_time=1.2)
        q = T("about three quarters lower", 24, RED).next_to(sg, DOWN, buff=0.55).align_to(sg, LEFT)
        self.at("three quarters")
        self.play(FadeIn(q), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------------------------------
class S04Credit(SpokenScene):
    def construct(self):
        self.add(tl_base(), *[tl_tick(i, on=False) for i in range(4)])
        ban = pchip("Frederick Banting").move_to([-3.2, 1.5, 0])
        mac = pchip("John Macleod").move_to([3.2, 1.5, 0])
        nob = T("1923 Nobel Prize named", 28, YELLOW).move_to([0, 2.8, 0])
        self.at("The 1923 Nobel")
        self.play(FadeIn(tl_tick(4)), FadeIn(nob), run_time=0.5)
        self.at("Banting and McLeod")
        self.play(FadeIn(ban), FadeIn(mac), run_time=0.6)
        best = pchip("Charles Best").move_to([-3.2, -0.6, 0])
        col = pchip("James Collip").move_to([3.2, -0.6, 0])
        a1 = arrow(ban.get_bottom(), best.get_top(), GOLD)
        a2 = arrow(mac.get_bottom(), col.get_top(), GOLD)
        t1 = T("shared prize money", 22, GOLD).next_to(a1, RIGHT, buff=0.15)
        t2 = T("shared prize money", 22, GOLD).next_to(a2, LEFT, buff=0.15)
        self.at("Banting shared his prize money")
        self.play(GrowArrow(a1), FadeIn(best), FadeIn(t1), run_time=0.8)
        self.at("McLeod with")
        self.play(GrowArrow(a2), FadeIn(col), FadeIn(t2), run_time=0.8)
        left = T("left out of the two-name story", 24, YELLOW).move_to([0, -1.9, 0])
        self.at("misses half")
        self.play(FadeIn(left), Indicate(best[2], color=YELLOW), Indicate(col[2], color=YELLOW), run_time=0.9)
        # ---- drug, no mechanism ----------------------------------------------------------
        self.at("not known to be")
        self.play(*[FadeOut(m) for m in (ban, mac, best, col, a1, a2, t1, t2, left, nob)], run_time=0.6)
        drug = chip("a drug", GOLD, size=34).move_to([-3.4, 0.7, 0])
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.6, height=1.6, stroke_color=GREY, stroke_width=3)
                             .move_to([3.2, 0.7, 0]), num_dashes=40)
        q = T("?", 56, GREY, weight=BOLD).move_to([3.2, 0.7, 0])
        mt = T("mechanism", 28, GREY).next_to(box, UP, buff=0.2)
        rk = chip("the receptor is a tyrosine kinase", TEAL, size=24).move_to([3.2, -1.7, 0])
        self.play(FadeIn(drug, shift=RIGHT * 0.2), Create(box), FadeIn(q), FadeIn(mt), run_time=0.8)
        self.at("until 1982")
        self.play(FadeIn(tl_tick(5)), FadeIn(rk), run_time=0.7)
        self.at("The drug came first")
        self.play(Indicate(drug, color=YELLOW), run_time=0.8)
        self.at("the mechanism came later")
        self.play(Indicate(mt, color=YELLOW), run_time=0.8)
        self.finish()


class S05End(EndCard):
    LINE = "The drug came first. The mechanism came later."
