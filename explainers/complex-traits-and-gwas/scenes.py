"""Heritability describes populations, not people  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREY   = people, structure, labels
  BLUE   = additive genetic variance (the genetic part that makes children resemble parents)
  PURPLE = dominance variance
  ORANGE = environmental variance / the environment (soil, nutrition)
  YELLOW = the mean, variance, the heritability ratio (what is being measured)
  GREEN  = seedlings
  RED    = wrong reading / crossed out
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

HEIGHTS = [2.5, 3.4, 1.9, 3.7, 2.9, 2.2, 3.9, 1.7, 3.1]
XS = [-4.8 + 1.2 * i for i in range(9)]
BASE = -1.4
LONE = 4
MEAN = sum(HEIGHTS) / len(HEIGHTS)


def figure(h, x, base, color=GREY, w=0.5, r=0.18):
    body = RoundedRectangle(corner_radius=0.12, width=w, height=h - 2 * r, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.3).move_to([x, base + (h - 2 * r) / 2, 0])
    head = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color,
                  fill_opacity=0.3).move_to([x, base + h - r, 0])
    return VGroup(body, head)


def crowd(base=BASE):
    return [figure(h, x, base) for h, x in zip(HEIGHTS, XS)]


def vbracket(x, y0, y1, color, side=1, w=5):
    t = 0.18 * side
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=w),
                  Line([x, y0, 0], [x + t, y0, 0], color=color, stroke_width=w),
                  Line([x, y1, 0], [x + t, y1, 0], color=color, stroke_width=w))


def hbracket(y, x0, x1, color, side=1, w=5):
    t = 0.18 * side
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x0, y, 0], [x0, y + t, 0], color=color, stroke_width=w),
                  Line([x1, y, 0], [x1, y + t, 0], color=color, stroke_width=w))


def cross_over(mob, color=RED, w=7):
    c = mob.get_center()
    hw, hh = max(mob.width / 2, 0.35), max(mob.height / 2, 0.35)
    return VGroup(Line([c[0] - hw, c[1] + hh, 0], [c[0] + hw, c[1] - hh, 0], color=color, stroke_width=w),
                  Line([c[0] - hw, c[1] - hh, 0], [c[0] + hw, c[1] + hh, 0], color=color, stroke_width=w))


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def seg(x0, w, y, color, hgt=1.0):
    return Rectangle(width=w, height=hgt, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.45).move_to([x0 + w / 2, y, 0])


class S00Title(TitleCard):
    LESSON = "Complex traits, heritability and GWAS"
    TITLE = "Heritability describes populations, not people"


# ---------------------------------------------------------------------------------------------
class S01Person(SpokenScene):
    def construct(self):
        top = chip("heritability of height = 0.6", YELLOW, 30).move_to([0, 3.1, 0])
        figs = crowd()
        lone = figs[LONE]
        self.at("Suppose the heritability")
        mis = T("a common misreading comes next: is it 60% of one person?", 24, RED).move_to([0, 2.45, 0])
        self.play(FadeIn(top, shift=DOWN * 0.2), FadeIn(lone, shift=UP * 0.2), FadeIn(mis), run_time=0.8)
        self.at("your own height")
        topy = BASE + HEIGHTS[LONE]
        br = vbracket(-0.75, BASE, BASE + 0.6 * HEIGHTS[LONE], BLUE)
        lab = T("60% from genes?", 28, BLUE).next_to(br, LEFT, buff=0.25)
        self.play(Create(br), FadeIn(lab, shift=RIGHT * 0.2), run_time=0.8)
        self.at("It does not")
        x = cross_over(lab)
        self.play(Create(x), br.animate.set_color(RED), lab.animate.set_color(RED), run_time=0.5)
        self.wait(0.4)
        self.play(FadeOut(VGroup(x, br, lab, mis)), run_time=0.4)
        self.at("whole population")
        others = [f for i, f in enumerate(figs) if i != LONE]
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in others], lag_ratio=0.1), run_time=1.3)
        note = T("one population", 28, GREY).move_to([0, -2.1, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.at("variance")
        self.play(FadeOut(note), Indicate(top, color=YELLOW, scale_factor=1.05), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Variance(SpokenScene):
    def construct(self):
        figs = crowd()
        self.add(*figs)
        mean_y = BASE + MEAN
        formula = T("variance = average of (distance from the mean)²", 28, YELLOW).move_to([0, 3.2, 0])
        self.at("Variance is the")
        self.play(Write(formula), run_time=1.6)
        mline = DashedLine([-5.5, mean_y, 0], [5.4, mean_y, 0], color=YELLOW, stroke_width=4)
        mlab = T("mean", 24, YELLOW).move_to([5.85, mean_y, 0])
        self.at("from the mean")
        self.play(Create(mline), FadeIn(mlab), run_time=0.8)
        self.at("Here is a population")
        self.play(*[Indicate(f, color=TEXT, scale_factor=1.04) for f in figs], run_time=0.9)
        segs, sqs = [], []
        for i, (h, x) in enumerate(zip(HEIGHTS, XS)):
            ty = BASE + h
            segs.append(Line([x + 0.38, mean_y, 0], [x + 0.38, ty, 0], color=YELLOW, stroke_width=6))
            d = abs(h - MEAN)
            sq = Square(side_length=max(d, 0.04), stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                        fill_opacity=0.35).move_to([x, BASE - 0.4 - d / 2, 0])
            sqs.append(sq)
        self.at("distance from the mean")
        self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.1), run_time=1.0)
        self.at("square it")
        self.play(LaggedStart(*[GrowFromPoint(q, q.get_top()) for q in sqs], lag_ratio=0.1), run_time=1.2)
        lab = T("average of these squares = the variance", 26, YELLOW).move_to([0, -3.3, 0])
        self.at("average of those")
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.6)
        self.at("One person alone")
        lone_top = BASE + HEIGHTS[LONE]
        gone = [f for i, f in enumerate(figs) if i != LONE] + [s for i, s in enumerate(segs)] + sqs
        self.play(FadeOut(VGroup(*gone)), FadeOut(lab), mline.animate.move_to([0, lone_top, 0]).set_x(0),
                  mlab.animate.move_to([5.85, lone_top, 0]), run_time=1.0)
        lone_lab = T("one person: no spread, no variance", 28, YELLOW).move_to([0, -2.6, 0])
        self.at("no spread")
        self.play(FadeIn(lone_lab, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def bar_labels(x0, k, y, ve, names=True):
    pass


class S03Parts(SpokenScene):
    def construct(self):
        x0, k, y = -5.0, 0.1, 1.3
        outline = Rectangle(width=10, height=1.4, stroke_color=GREY, stroke_width=3).move_to([0, y, 0])
        div = Line([0, y - 0.7, 0], [0, y + 0.7, 0], color=GREY, stroke_width=3)
        self.at("Take a hypothetical")
        self.play(Create(outline), run_time=0.8)
        self.play(Create(div), run_time=0.5)
        gl = T("genetic parts", 26, BLUE).move_to([-2.5, y, 0])
        el = T("environmental part", 26, ORANGE).move_to([2.5, y, 0])
        self.at("genetic parts")
        self.play(FadeIn(gl), run_time=0.5)
        self.at("environmental part")
        self.play(FadeIn(el), run_time=0.6)
        va = seg(x0, 4.0, y, BLUE, 1.4)
        vd = seg(x0 + 4.0, 1.0, y, PURPLE, 1.4)
        ve = seg(x0 + 5.0, 5.0, y, ORANGE, 1.4)
        na = M("40", 30, BLUE).move_to(va)
        nd = M("10", 28, PURPLE).move_to(vd)
        ne = M("50", 30, ORANGE).move_to(ve)
        la = T("additive", 26, BLUE).move_to([va.get_center()[0], y - 1.1, 0])
        ld = T("dominance", 26, PURPLE).move_to([vd.get_center()[0], y - 1.1, 0])
        le = T("environment", 26, ORANGE).move_to([ve.get_center()[0], y - 1.1, 0])
        self.at("Additive variance")
        self.play(FadeOut(VGroup(div, gl, el)), GrowFromEdge(va, LEFT), FadeIn(na), FadeIn(la), run_time=0.9)
        self.at("Dominance variance")
        self.play(GrowFromEdge(vd, LEFT), FadeIn(nd), FadeIn(ld), run_time=0.7)
        li = T("interaction = 0", 24, GREY).move_to([vd.get_center()[0], y - 1.65, 0])
        self.at("interaction variance")
        self.play(FadeIn(li, shift=UP * 0.1), run_time=0.5)
        self.at("environmental variance")
        self.play(GrowFromEdge(ve, LEFT), FadeIn(ne), FadeIn(le), run_time=0.9)
        tb = hbracket(y + 1.0, x0, x0 + 10, YELLOW, side=-1)
        tl = T("total = 100", 28, YELLOW).move_to([0, y + 1.6, 0])
        self.at("the total")
        self.play(Create(tb), FadeIn(tl), FadeOut(outline), run_time=0.8)
        f1 = M("h² = 40 / 100 = 0.40", 32, YELLOW)
        t1 = T("narrow-sense: additive only", 26, BLUE)
        r1 = VGroup(t1, f1).arrange(RIGHT, buff=0.5).move_to([0, -1.8, 0])
        hl = Rectangle(width=4.0, height=1.4, stroke_color=YELLOW, stroke_width=7).move_to(va)
        self.at("Narrow sense heritability")
        self.play(Create(hl), run_time=0.5)
        self.at("variance over the total")
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.7)
        f2 = M("H² = 50 / 100 = 0.50", 32, YELLOW)
        t2 = T("broad-sense: adds dominance", 26, PURPLE)
        r2 = VGroup(t2, f2).arrange(RIGHT, buff=0.5).move_to([0, -2.9, 0])
        hl2 = Rectangle(width=5.0, height=1.4, stroke_color=YELLOW, stroke_width=7).move_to([x0 + 2.5, y, 0])
        self.at("Broad sense heritability")
        self.play(ReplacementTransform(hl, hl2), run_time=0.6)
        self.at("dominance part")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Nutrition(SpokenScene):
    def construct(self):
        x0, y1, y2 = -5.0, 2.0, -0.2
        def bar(y, ve):
            va = seg(x0, 4.0, y, BLUE, 1.1)
            vd = seg(x0 + 4.0, 1.0, y, PURPLE, 1.1)
            vv = seg(x0 + 5.0, ve * 0.1, y, ORANGE, 1.1)
            na = M("40", 28, BLUE).move_to(va)
            nd = M("10", 26, PURPLE).move_to(vd)
            nv = M(str(ve), 28, ORANGE).move_to(vv)
            return va, vd, vv, na, nd, nv
        top = bar(y1, 50)
        cap1 = T("before: total 100, h² = 0.40", 26, GREY).move_to([x0 + 3.0, y1 + 1.05, 0])
        self.add(*top, cap1)
        self.at("nutrition")
        bot = list(bar(y2, 50))
        cap2 = T("after better nutrition", 26, ORANGE).move_to([x0 + 1.9, y2 + 1.05, 0])
        self.play(*[FadeIn(m, shift=DOWN * 0.3) for m in bot], FadeIn(cap2), run_time=0.9)
        new_vv = seg(x0 + 5.0, 2.0, y2, ORANGE, 1.1)
        new_nv = M("20", 28, ORANGE).move_to(new_vv)
        self.at("falls")
        self.play(ReplacementTransform(bot[2], new_vv), ReplacementTransform(bot[5], new_nv), run_time=1.3)
        dl = DashedLine([0, y1 + 0.65, 0], [0, y2 - 0.65, 0], color=TEXT, stroke_width=3)
        dlab = btext("genetic variance, unchanged", 24, TEXT)
        dlab.move_to([0.25 + dlab.width / 2, (y1 + y2) / 2 + 0.1, 0])
        self.at("stays the same")
        self.play(Create(dl), FadeIn(dlab), run_time=0.8)
        tot = T("total = 70", 28, YELLOW).move_to([x0 + 7.0 + 1.5, y2, 0])
        self.at("the total")
        self.play(FadeIn(tot, shift=LEFT * 0.2), run_time=0.5)
        f = M("h² = 40 / 70 = 0.57", 34, YELLOW).move_to([0, -1.7, 0])
        self.at("Heritability is now")
        self.play(FadeIn(f, shift=UP * 0.15), run_time=0.8)
        a = M("0.40", 32, GREY)
        ar = Arrow(LEFT * 0.6, RIGHT * 0.6, color=YELLOW, buff=0, stroke_width=6)
        b = M("0.57", 34, YELLOW)
        cmp_ = VGroup(a, ar, b).arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
        self.at("went up")
        self.play(FadeIn(a), GrowArrow(ar), FadeIn(b), run_time=0.7)
        u = T("cm² ÷ cm²: no units", 26, GREY).move_to([0, -3.35, 0])
        self.at("units cancel")
        self.play(FadeIn(u, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Seeds(SpokenScene):
    def construct(self):
        # --- part A: average height rose ---
        ox, oy = -4.5, -2.3
        axes = VGroup(Line([ox, oy, 0], [ox + 9, oy, 0], color=GREY, stroke_width=4),
                      Line([ox, oy, 0], [ox, oy + 4.6, 0], color=GREY, stroke_width=4))
        xl = T("twentieth century", 26, GREY).move_to([0, oy - 0.5, 0])
        yl = T("average height", 26, GREY).move_to([ox + 0.1, oy + 5.1, 0]).align_to([ox, 0, 0], LEFT)
        pts = [[ox + 0.3 + t * 8.4, oy + 0.9 + 3.0 * t, 0]
               for t in np.linspace(0, 1, 30)]
        curve = VMobject(color=YELLOW, stroke_width=7).set_points_smoothly([np.array(p) for p in pts])
        self.at("High heritability")
        self.play(Create(axes), FadeIn(xl), FadeIn(yl), run_time=1.0)
        hh = chip("highly heritable within populations", BLUE, 26).move_to([2.0, oy + 4.5, 0])
        self.at("highly heritable")
        self.play(FadeIn(hh, shift=DOWN * 0.15), run_time=0.6)
        self.at("average height rose")
        self.play(Create(curve), run_time=1.6)
        self.wait(0.4)
        # --- part B: seed trays ---
        self.at("Lewontin's")
        self.play(FadeOut(VGroup(axes, xl, yl, curve, hh)), run_time=0.6)
        seeds = VGroup(*[Circle(radius=r, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5)
                         for r in [0.12, 0.2, 0.15, 0.24, 0.13, 0.19]]).arrange(RIGHT, buff=0.3)
        seed_lab = T("a varied stock of seed", 26, GREEN)
        stock = VGroup(seeds, seed_lab).arrange(DOWN, buff=0.2).move_to([0, 3.1, 0])
        self.at("varied stock of seed")
        self.play(FadeIn(stock, shift=DOWN * 0.15), run_time=0.7)
        soilY = -1.9
        poor_h = [v * 1.3 for v in [0.8, 1.4, 1.0, 1.8, 1.2, 1.6]]
        diff = 1.1

        def tray(cx, soil_op, label, lc):
            soil = Rectangle(width=4.6, height=0.55, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                             fill_opacity=soil_op).move_to([cx, soilY, 0])
            lb = T(label, 26, lc).move_to([cx, soilY - 0.7, 0])
            return soil, lb

        def plants(cx, add):
            out = VGroup()
            for j, h in enumerate(poor_h):
                x = cx - 1.75 + 0.7 * j
                top = soilY + 0.275 + h + add
                out.add(VGroup(Line([x, soilY + 0.275, 0], [x, top, 0], color=GREEN, stroke_width=6),
                               Circle(radius=0.16, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                                      fill_opacity=0.8).move_to([x, top, 0])))
            return out
        s1, l1 = tray(-3.3, 0.2, "poor soil", ORANGE)
        s2, l2 = tray(3.3, 0.65, "rich soil", ORANGE)
        p1 = plants(-3.3, 0.0)
        p2 = plants(3.3, diff)
        self.at("rich soil")
        self.play(FadeIn(s2), FadeIn(l2), FadeIn(s1), FadeIn(l1), run_time=0.8)
        self.play(LaggedStart(*[GrowFromPoint(p, p.get_bottom()) for p in list(p2) + list(p1)], lag_ratio=0.07),
                  run_time=1.2)
        self.at("Within each tray")
        base_y = soilY + 0.275
        groups = VGroup()
        for cx, add in ((-3.3, 0.0), (3.3, diff)):
            br = vbracket(cx - 2.05, base_y + min(poor_h) + add, base_y + max(poor_h) + add, BLUE, side=1)
            gl = T("genetic", 24, BLUE).move_to([cx, base_y + max(poor_h) + add + 0.65, 0])
            groups.add(br, gl)
        self.play(Create(groups), run_time=1.0)
        mp = base_y + sum(poor_h) / 6
        m1 = DashedLine([-5.5, mp, 0], [0, mp, 0], color=ORANGE, stroke_width=3)
        m2 = DashedLine([0, mp + diff, 0], [5.5, mp + diff, 0], color=ORANGE, stroke_width=3)
        env = Arrow([0, mp, 0], [0, mp + diff, 0], color=ORANGE, buff=0, stroke_width=9, tip_length=0.3, max_tip_length_to_length_ratio=0.5)
        env_lab = T("environment", 24, ORANGE).move_to([0, mp + diff + 0.55, 0])
        self.at("between the trays")
        self.play(Create(m1), Create(m2), run_time=0.6)
        self.play(GrowArrow(env), FadeIn(env_lab), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        # --- two groups, heritability inside each, nothing across the gap ---
        def mini(cx, cy, n=5):
            hs = [1.2, 1.6, 1.0, 1.8, 1.4]
            return VGroup(*[figure(hs[i] * 0.8, cx - 1.6 + 0.8 * i, cy - 1.5, w=0.36, r=0.13) for i in range(n)])
        fr1 = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.6, stroke_color=GREY, stroke_width=3).move_to([-4.1, 0.4, 0])
        fr2 = fr1.copy().move_to([4.1, 0.4, 0])
        m1, m2 = mini(-4.1, 0.4), mini(4.1, 0.4)
        h1 = chip("heritability", YELLOW, 26).move_to([-4.1, 1.5, 0])
        h2 = chip("heritability", YELLOW, 26).move_to([4.1, 1.5, 0])
        self.at("within a group")
        self.play(Create(fr1), Create(fr2), FadeIn(m1), FadeIn(m2), FadeIn(h1), FadeIn(h2), run_time=1.2)
        q = T("?", 80, RED, weight=BOLD).move_to([0, 0.7, 0])
        ql = T("why groups differ", 26, GREY).move_to([0, -0.3, 0])
        self.at("why groups differ")
        self.play(FadeIn(q, scale=0.6), FadeIn(ql), run_time=0.7)
        # --- one person ---
        self.at("It cannot split")
        self.play(FadeOut(VGroup(fr1, fr2, m1, m2, h1, h2, q, ql)), run_time=0.6)
        lone = figure(HEIGHTS[LONE], 0, BASE)
        self.play(FadeIn(lone, shift=UP * 0.2), run_time=0.5)
        bg = vbracket(-0.8, BASE, BASE + 0.6 * HEIGHTS[LONE], BLUE)
        bg_l = T("genetic", 26, BLUE).next_to(bg, LEFT, buff=0.25)
        be = vbracket(0.8, BASE + 0.6 * HEIGHTS[LONE], BASE + HEIGHTS[LONE], ORANGE, side=-1)
        be_l = T("environmental", 26, ORANGE).next_to(be, RIGHT, buff=0.25)
        self.play(Create(bg), Create(be), FadeIn(bg_l), FadeIn(be_l), run_time=0.8)
        xs = cross_over(VGroup(bg_l, be_l, lone), w=8)
        self.at("because one person")
        self.play(Create(xs), run_time=0.5)
        nv = T("one person: no variance", 30, RED).move_to([0, -2.5, 0])
        self.play(FadeIn(nv, shift=UP * 0.1), run_time=0.5)
        # --- the rule ---
        self.at("ratio of variances")
        self.play(FadeOut(VGroup(lone, bg, be, bg_l, be_l, xs, nv)), run_time=0.6)
        crowd_s = VGroup(*[figure(h * 0.75, x * 0.85, -2.6, w=0.4, r=0.15) for h, x in zip(HEIGHTS, XS)])
        frame = RoundedRectangle(corner_radius=0.2, width=9.0, height=3.7, stroke_color=YELLOW, stroke_width=3).move_to([0, -1.15, 0])
        flab = T("one population, one environment", 26, YELLOW).move_to([0, -3.3, 0])
        self.play(Create(frame), FadeIn(crowd_s), FadeIn(flab), run_time=0.9)
        self.at("Keep this rule")
        r1 = T("Heritability describes", 44, font=TITLE_FONT).move_to([0, 3.0, 0])
        r2 = T("a population in an environment,", 44, font=TITLE_FONT).move_to([0, 2.15, 0])
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("a population in")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        r3 = T("never a person.", 44, RED, font=TITLE_FONT).move_to([0, 1.3, 0])
        lone2 = figure(HEIGHTS[LONE] * 0.75, 5.7, -2.6, w=0.4, r=0.15)
        self.at("never a person")
        self.play(FadeIn(r3, shift=UP * 0.1), FadeIn(lone2), run_time=0.6)
        self.play(Create(cross_over(lone2, w=6)), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "Heritability describes a population in an environment, never a person."
