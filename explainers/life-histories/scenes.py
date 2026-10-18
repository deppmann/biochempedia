"""Life histories: why trade-offs hide in natural data  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  YELLOW = reproduction (eggs, chicks, nest, fledglings)
  BLUE   = the parent's own upkeep and survival (maintenance and repair)
  GREEN  = growth
  GREY   = storage, the bird, outlines, de-emphasized
  ORANGE = an imposed cost or change (load, handicap, manipulation, foraging cost)
  TEAL   = unmanipulated: natural variation, control nests
  TEXT   = rules and totals
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def bird(scale=1.0, loaded=False, flip=False):
    body = Ellipse(width=2.4, height=1.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55)
    head = Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55).move_to([1.25, 0.45, 0])
    beak = Polygon([1.6, 0.5, 0], [2.0, 0.42, 0], [1.6, 0.34, 0], stroke_color=GREY, stroke_width=3,
                   fill_color=GREY, fill_opacity=0.9)
    tail = Polygon([-1.1, 0.1, 0], [-2.0, 0.55, 0], [-2.0, -0.25, 0], stroke_color=GREY, stroke_width=3,
                   fill_color=GREY, fill_opacity=0.55)
    eye = Dot([1.35, 0.52, 0], radius=0.05, color=BG)
    g = VGroup(tail, body, head, beak, eye)
    load = None
    if loaded:
        load = RoundedRectangle(corner_radius=0.1, width=0.9, height=0.5, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=0.85).move_to([-0.1, 0.78, 0])
        g.add(load)
    g.scale(scale)
    g.load = load
    return g


def nest(width=2.6):
    bowl = Arc(radius=width / 2, start_angle=PI, angle=PI, stroke_color=YELLOW, stroke_width=5).rotate(PI)
    bowl.set_fill(YELLOW, 0.15)
    return bowl


def bar_segs(ws, cols, x0, y, h=1.0, op=0.45):
    out, x = VGroup(), x0
    for w, c in zip(ws, cols):
        r = Rectangle(width=max(w, 0.02), height=h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=op)
        r.move_to([x + w / 2, y, 0])
        out.add(r)
        x += w
    return out


class S00Title(TitleCard):
    LESSON = "Life histories and evolutionary trade-offs"
    TITLE = "Why trade-offs hide in natural data"


# ---------------------------------------------------------------------------------------------
class S01Skylark(SpokenScene):
    def construct(self):
        b = bird(1.2).move_to([-3.7, 0.5, 0])
        lab = T("breeding skylark", 28, GREY).next_to(b, DOWN, buff=0.35)
        self.at("harness onto")
        self.play(FadeIn(b), FadeIn(lab), run_time=0.7)
        load = bird(1.2, loaded=True).load.copy()
        load.move_to(b.get_center() + UP * 2.2)
        self.add(load)
        tgt = bird(1.2, loaded=True).move_to(b.get_center()).load.get_center()
        self.play(load.animate.move_to(tgt), run_time=0.7)
        ltxt = T("extra load: 3 to 4 g", 26, ORANGE).next_to(b, UP, buff=0.55)
        ltxt2 = T("about 10% of body mass", 24, ORANGE).next_to(ltxt, DOWN, buff=0.12)
        self.at("three to four grams")
        self.play(FadeIn(ltxt), run_time=0.4)
        self.at("body mass")
        self.play(FadeIn(ltxt2), run_time=0.4)
        n = nest(3.2).move_to([4.0, 0.7, 0])
        nl = T("nest", 28, YELLOW).next_to(n, DOWN, buff=0.25)
        self.at("Its nest tends")
        self.play(Create(n), FadeIn(nl), run_time=0.6)
        fl = T("fledglings", 28, YELLOW).next_to(n, UP, buff=0.3)
        fewer = VGroup(Arrow(UP * 0.5, DOWN * 0.5, color=YELLOW, buff=0, stroke_width=6),
                       T("fewer", 28, YELLOW)).arrange(RIGHT, buff=0.2).next_to(fl, UP, buff=0.2)
        self.at("fewer fledglings")
        self.play(FadeIn(fl), FadeIn(fewer, shift=DOWN * 0.2), run_time=0.6)
        food = chip("food taken away", GREY, 28).move_to([-1.0, -2.6, 0])
        cross = Line(food.get_corner(DL) + RIGHT * 0.1, food.get_corner(UR) + LEFT * 0.1, color=RED, stroke_width=6)
        self.at("nobody took any food")
        self.play(FadeIn(food), run_time=0.4)
        self.play(Create(cross), run_time=0.4)
        none = T("none", 28, RED).next_to(food, RIGHT, buff=0.35)
        self.play(FadeIn(none), run_time=0.3)
        q = T("?", 96, YELLOW, weight=BOLD).move_to([4.0, -1.2, 0])
        self.at("where did the chicks go")
        self.play(FadeIn(q, scale=0.6), Indicate(n, color=YELLOW), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Budget(SpokenScene):
    def construct(self):
        cols = [GREEN, BLUE, GREY, YELLOW]
        names = ["growth", "maintenance and repair", "storage", "reproduction"]
        x0, W, y = -5.5, 11.0, 0.7
        w0 = [2.4, 3.4, 2.0, 3.2]
        w1 = [2.4, 1.8, 2.0, 4.8]
        w2 = [2.0, 1.4, 1.6, 2.2]   # leaves room for the foraging block (3.8)
        outline = Rectangle(width=W, height=1.7, stroke_color=TEXT, stroke_width=3).move_to([0, y, 0])
        head = T("one limited budget", 36, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("limited budget")
        self.play(Create(outline), Write(head), run_time=0.9)
        segs = bar_segs(w0, cols, x0, y, h=1.7)
        chips = VGroup(*[chip(n, c, 24) for n, c in zip(names, cols)]).arrange(RIGHT, buff=0.25).move_to([0, -0.9, 0])
        sub = T("energy and nutrients", 26, GREY).next_to(outline, UP, buff=0.2)
        self.at("Energy and nutrients")
        self.play(FadeIn(sub), run_time=0.4)
        self.at("growth")
        self.play(FadeIn(segs[0]), FadeIn(chips[0]), run_time=0.4)
        self.at("maintenance and repair")
        self.play(FadeIn(segs[1]), FadeIn(chips[1]), run_time=0.4)
        self.at("storage")
        self.play(FadeIn(segs[2]), FadeIn(chips[2]), run_time=0.4)
        self.at("and reproduction")
        self.play(FadeIn(segs[3]), FadeIn(chips[3]), run_time=0.4)
        head2 = T("like a monthly paycheck", 36, TEXT, font=TITLE_FONT).move_to(head)
        self.at("monthly paycheck")
        self.play(ReplacementTransform(head, head2), run_time=0.5)
        more = T("more here", 26, YELLOW).move_to([x0 + sum(w1[:3]) + w1[3] / 2, 2.05, 0])
        less = T("less here", 26, BLUE).move_to([x0 + w1[0] + w1[1] / 2, 2.05, 0])
        self.at("more for one")
        self.play(Transform(segs, bar_segs(w1, cols, x0, y, h=1.7)), FadeIn(more), FadeIn(less), FadeOut(sub), run_time=1.3)
        tr = chip("trade-off: a negative link", TEXT, 30).move_to([0, -2.3, 0])
        self.at("negative link is a")
        self.play(FadeIn(tr, shift=UP * 0.2), run_time=0.5)
        self.at("cost paid")
        fx = x0 + sum(w2)
        cw = W - sum(w2)
        cost = Rectangle(width=cw, height=1.7, stroke_width=0, fill_color=ORANGE, fill_opacity=0.18).move_to([fx + cw / 2, y, 0])
        cout = DashedVMobject(Rectangle(width=cw, height=1.7, stroke_color=ORANGE, stroke_width=3).move_to(cost), num_dashes=40)
        ct = VGroup(T("a cost", 26, ORANGE, weight=BOLD), T("in this sketch", 22, ORANGE)).arrange(DOWN, buff=0.1).move_to(cost)
        self.play(FadeOut(more), FadeOut(less), FadeOut(tr), Transform(segs, bar_segs(w2, cols, x0, y, h=1.7)),
                  FadeIn(cost), Create(cout), FadeIn(ct), run_time=1.0)
        may = T("may leave less for young, upkeep, or both", 28, GREY).move_to([0, -2.3, 0])
        self.at("may leave less")
        self.play(FadeIn(may), Indicate(segs[3], color=YELLOW), Indicate(segs[1], color=BLUE), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Hidden(SpokenScene):
    def construct(self):
        x0 = -5.3
        head = T("birds with big clutches survive better", 32, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("bird populations")
        self.play(Write(head), run_time=1.0)
        leg = VGroup(chip("eggs", YELLOW, 24), chip("own survival", BLUE, 24)).arrange(RIGHT, buff=0.4).move_to([0, 2.15, 0])
        self.play(FadeIn(leg), run_time=0.4)
        big_y, small_y = 0.8, -1.0
        bo = Rectangle(width=8.4, height=1.3, stroke_color=TEXT, stroke_width=3).move_to([x0 + 4.2, big_y, 0])
        so = Rectangle(width=4.2, height=1.3, stroke_color=TEXT, stroke_width=3).move_to([x0 + 2.1, small_y, 0])
        bl = T("big budget", 24, GREY).next_to(bo, RIGHT, buff=0.3)
        sl = T("small budget", 24, GREY).next_to(so, RIGHT, buff=0.3)
        bsegs = bar_segs([4.2, 4.2], [YELLOW, BLUE], x0, big_y, h=1.3)
        ssegs = bar_segs([2.1, 2.1], [YELLOW, BLUE], x0, small_y, h=1.3)
        self.at("big clutches")
        self.play(Create(so), FadeIn(ssegs), Create(bo), FadeIn(bsegs), run_time=1.0)
        self.at("acquire more")
        self.play(FadeIn(sl), FadeIn(bl), run_time=0.6)
        self.at("afford more eggs")
        self.play(Indicate(bsegs[0], color=YELLOW), run_time=0.6)
        self.play(Indicate(bsegs[1], color=BLUE), run_time=0.6)
        note = T("in this sketch", 22, GREY).move_to([5.1, 2.15, 0])
        across = VGroup(T("across birds:", 28, TEXT), T("more eggs, better survival", 28, TEXT),
                        T("positive", 28, GREEN, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.4, 0])
        self.at("link is positive")
        self.play(FadeIn(across), FadeIn(note), run_time=0.7)
        within = VGroup(T("within one bird:", 28, TEXT), T("more eggs, less for itself", 28, TEXT),
                        T("negative", 28, RED, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -3.2, 0])
        self.at("any one bird")
        self.play(Indicate(bo, color=TEXT), run_time=0.6)
        self.at("spent on eggs")
        self.play(Transform(bsegs, bar_segs([5.8, 2.6], [YELLOW, BLUE], x0, big_y, h=1.3)), FadeIn(within), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Manipulate(SpokenScene):
    def construct(self):
        head = T("change one thing on purpose", 36, ORANGE, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("change one thing")
        self.play(Write(head), run_time=1.0)
        cs = VGroup(chip("enlarge a brood", ORANGE, 26), chip("add a handicap", ORANGE, 26),
                    chip("add back one nutrient", ORANGE, 26)).arrange(RIGHT, buff=0.35).move_to([0, 2.0, 0])
        self.at("Enlarge a brood")
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.4)
        self.at("Add a handicap")
        self.play(FadeIn(cs[1], shift=UP * 0.2), run_time=0.4)
        self.at("Add back one nutrient")
        self.play(FadeIn(cs[2], shift=UP * 0.2), run_time=0.4)
        mh = T("meta-analysis of 30 bird species", 26, GREY).move_to([0, 1.1, 0])
        self.at("Now take a")
        self.play(FadeIn(mh), run_time=0.5)
        cards = []
        for x, col, ttl in [(-3.2, TEAL, "natural clutch sizes"), (3.2, ORANGE, "researchers enlarge broods")]:
            box = RoundedRectangle(corner_radius=0.2, width=6.2, height=3.4, stroke_color=col, stroke_width=3,
                                   fill_color=col, fill_opacity=0.10).move_to([x, -1.2, 0])
            t = T(ttl, 28, col).move_to([x, -0.1, 0])
            cards.append((box, t))
        self.play(*[FadeIn(c[0]) for c in cards], *[FadeIn(c[1]) for c in cards], run_time=0.7)
        up = Arrow([-5.9, -2.5, 0], [-5.9, -0.8, 0], color=TEAL, buff=0, stroke_width=8)
        ut = T("better parental survival", 26, TEAL).move_to([-5.3, -1.65, 0], aligned_edge=LEFT)
        self.at("better parental survival")
        self.play(GrowArrow(up), FadeIn(ut), run_time=0.7)
        dn = Arrow([0.7, -0.8, 0], [0.7, -2.2, 0], color=ORANGE, buff=0, stroke_width=8)
        dt = VGroup(T("survival lower on average", 26, ORANGE), T("small effect", 24, GREY)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([1.3, -1.3, 0], aligned_edge=LEFT)
        self.at("lowered survival")
        self.play(GrowArrow(dn), FadeIn(dt), run_time=0.7)
        zero = T("interval per added chick: includes zero", 24, GOLD).move_to([3.2, -2.55, 0])
        self.at("includes zero")
        self.play(FadeIn(zero), dn.animate.set_opacity(0.35), run_time=0.8)
        self.at("is not supported")
        self.play(Indicate(zero, color=GOLD), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def dot_grid(n, ok, col, cols=5, r=0.2, gap=0.54):
    g = VGroup()
    for i in range(n):
        d = Circle(radius=r, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.0)
        d.move_to([(i % cols - (cols - 1) / 2) * gap, -(i // cols) * gap, 0])
        d.ok = i < ok
        g.add(d)
    return g


class S05Arithmetic(SpokenScene):
    def construct(self):
        key = T("first broods: a filled dot is a nest that succeeded", 24, GREY).move_to([0, 3.35, 0])
        ch = T("control nests", 28, TEAL).move_to([-3.4, 2.75, 0])
        hh = T("handicapped nests", 28, ORANGE).move_to([3.4, 2.75, 0])
        self.at("skylark numbers")
        self.play(FadeIn(key), FadeIn(ch), FadeIn(hh), run_time=0.7)
        gc = dot_grid(25, 19, TEAL).move_to([-3.4, 1.2, 0])
        gh = dot_grid(17, 8, ORANGE).move_to([3.4, 1.2, 0])
        gh.align_to(gc, UP)
        self.play(FadeIn(gc), FadeIn(gh), run_time=0.5)
        self.at("control nests succeeded")
        self.play(*[d.animate.set_fill(TEAL, 0.9) for d in gc if d.ok], run_time=1.2, lag_ratio=0.05)
        ct = M("19 of 25", 30, TEAL).move_to([-3.4, -0.5, 0])
        self.play(FadeIn(ct), run_time=0.3)
        self.at("handicapped nests did")
        self.play(*[d.animate.set_fill(ORANGE, 0.9) for d in gh if d.ok], run_time=1.0, lag_ratio=0.05)
        ht = M("8 of 17", 30, ORANGE).move_to([3.4, -0.5, 0])
        self.play(FadeIn(ht), run_time=0.3)
        cr = M("76.0%", 36, TEAL, weight=BOLD).move_to([-3.4, -1.2, 0])
        hr = M("47.1%", 36, ORANGE, weight=BOLD).move_to([3.4, -1.2, 0])
        self.at("That is")
        self.play(FadeIn(cr, shift=UP * 0.1), FadeIn(hr, shift=UP * 0.1), run_time=0.7)
        gap = chip("gap: -28.9 percentage points", TEXT, 28).move_to([-3.4, -2.2, 0])
        self.at("The gap is")
        self.play(FadeIn(gap, shift=UP * 0.15), run_time=0.6)
        rel = chip("relative reduction: 38.1%", TEXT, 28).move_to([3.4, -2.2, 0])
        self.at("Measured against the control rate")
        self.play(FadeIn(rel, shift=UP * 0.15), Indicate(cr, color=TEAL), run_time=0.8)
        self.at("two different numbers")
        self.play(Indicate(gap, color=GOLD), Indicate(rel, color=GOLD), run_time=0.9)
        fl = VGroup(T("fledglings per nest:", 28, YELLOW), M("2.0", 30, TEAL), T("to", 26, GREY), M("1.2", 30, ORANGE)
                    ).arrange(RIGHT, buff=0.25).move_to([0, -3.3, 0])
        self.at("Mean fledglings per nest")
        self.play(FadeIn(fl, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        b = bird(0.9, loaded=True).move_to([-4.5, 1.2, 0])
        bl = T("skylark with load", 24, GREY).next_to(b, DOWN, buff=0.3)
        self.add(b, bl)
        rows = []
        specs = [("reproductive output: reduced", YELLOW, "harness and load together"),
                 ("survival cost to adults: not established", BLUE, "adult return did not differ significantly"),
                 ("harness alone: no such group", ORANGE, "harness and load cannot be separated")]
        ys = [2.3, 1.0, -0.3]
        for (a, c, s), y in zip(specs, ys):
            t1 = T(a, 28, c)
            t2 = T(s, 22, GREY)
            g = VGroup(t1, t2).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([1.7, y, 0], aligned_edge=LEFT) if False else VGroup(t1, t2).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            g.move_to([0, y, 0], aligned_edge=LEFT).shift(RIGHT * -1.2)
            rows.append(g)
        self.at("reduced reproductive output")
        self.play(FadeIn(rows[0], shift=RIGHT * 0.3), run_time=0.6)
        bl2 = T("nest success gap: borderline", 22, GOLD).next_to(rows[0], DOWN, buff=0.08, aligned_edge=LEFT)
        self.at("borderline")
        self.play(FadeIn(bl2), run_time=0.4)
        self.at("did not establish")
        self.play(FadeOut(bl2), FadeIn(rows[1], shift=RIGHT * 0.3), run_time=0.6)
        self.at("harness alone")
        self.play(FadeIn(rows[2], shift=RIGHT * 0.3), run_time=0.6)
        rule = VGroup(T("A natural correlation can hide a trade-off.", 34, TEXT, font=TITLE_FONT),
                      T("Change one thing on purpose.", 34, ORANGE, font=TITLE_FONT)).arrange(DOWN, buff=0.2)
        box = SurroundingRectangle(rule, color=GOLD, buff=0.3, corner_radius=0.15, stroke_width=3)
        grp = VGroup(box, rule).move_to([0, -2.75, 0])
        self.at("Keep this rule")
        self.play(Create(box), FadeIn(rule), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "A natural correlation can hide a trade-off: change one thing."
