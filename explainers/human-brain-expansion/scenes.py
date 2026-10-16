"""Human brain expansion: more columns, not a thicker cortex  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = classical radial glia / founder progenitors (the units)
  YELLOW = neurons, and the columns they stack into
  GREEN  = area: the number of units, symmetric (doubling) divisions
  PURPLE = thickness: neurons per unit, asymmetric (adding) divisions
  PINK   = outer radial glia
  ORANGE = a gene or protein that is added, changed or removed
  RED    = not tested / no contact / missing
  GREY   = ventricle, brain surface, labels, de-emphasized
  GOLD   = the question mark and the final rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB8"


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.04, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=5, tip=0.2):
    return DoubleArrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                       max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar(x0, x1, y, color=GREY, h=0.24):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def dot(x, y, color, r=0.16):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


def sq(x, bottom, side, color):
    return Rectangle(width=side, height=side, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.3).move_to([x, bottom + side / 2, 0])


class S00Title(TitleCard):
    LESSON = "What makes the human brain big"
    TITLE = "More columns, not thicker cortex"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """thickness barely changes (about 2x) while area changes enormously (about 1000x): the puzzle."""

    def construct(self):
        # thickness panel
        t_title = T("wall thickness", 30, PURPLE).move_to([-3.3, 2.9, 0])
        bm = Rectangle(width=0.9, height=1.2, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3)
        bm.move_to([-4.3, -1.0 + 0.6, 0])
        bh = Rectangle(width=0.9, height=2.4, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3)
        bh.move_to([-2.3, -1.0 + 1.2, 0])
        l1 = T("mouse", 26, GREY).move_to([-4.3, -1.45, 0])
        l2 = T("human", 26, GREY).move_to([-2.3, -1.45, 0])
        r1 = M("about 2×", 30, PURPLE).move_to([-3.3, -2.0, 0])
        # area panel
        a_title = T("surface area", 30, GREEN).move_to([3.3, 2.9, 0])
        sm = sq(1.7, -1.0, 0.5, GREEN)
        sh = sq(4.6, -1.0, 3.0, GREEN)
        l3 = T("mouse", 26, GREY).move_to([1.7, -1.45, 0])
        l4 = T("human", 26, GREY).move_to([4.6, -1.45, 0])
        r2 = M("roughly 1,000×", 30, GREEN).move_to([3.3, -2.0, 0])
        ns = T("drawn schematically, not to scale", 22, GREY).move_to([3.3, -2.5, 0])
        q = T("?", 120, GOLD, weight=BOLD).move_to([0, 0.3, 0])
        ask = T("More area, without a thicker wall?", 34, TEXT, font=TITLE_FONT).move_to([0, -3.1, 0])

        self.play(FadeIn(t_title), FadeIn(a_title), FadeIn(l1), FadeIn(l2), FadeIn(l3), FadeIn(l4), run_time=0.5)
        self.at("twice as thick")
        self.play(FadeIn(bm, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(bh, shift=UP * 0.2), FadeIn(r1), run_time=0.7)
        self.at("a thousand times larger")
        self.play(FadeIn(sm), run_time=0.4)
        self.play(GrowFromEdge(sh, DOWN), FadeIn(r2), FadeIn(ns), run_time=1.1)
        self.at("That is the puzzle")
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("thickness changes little")
        self.play(Indicate(VGroup(bm, bh), color=PURPLE, scale_factor=1.05), run_time=0.8)
        self.at("area changes enormously")
        self.play(Indicate(sh, color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("How does a growing brain")
        self.play(FadeIn(ask, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
UX = [-4.5 + 1.8 * i for i in range(6)]
VEN_Y = -2.7


def unit_parts(x):
    patch = Ellipse(width=0.9, height=0.32, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.5).move_to([x, -2.42, 0])
    fibre = Line([x, -2.26, 0], [x, 2.55, 0], color=BLUE, stroke_width=3).set_opacity(0.55)
    return patch, fibre


def column_rect(x):
    return RoundedRectangle(corner_radius=0.12, width=0.62, height=2.1, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.12).move_to([x, 1.4, 0])


STACK_Y = [0.7, 1.15, 1.6, 2.05]


class S02Unit(SpokenScene):
    """a patch of progenitors makes a column; units set area, neurons per unit set thickness."""

    def construct(self):
        ven = bar(-6.3, 6.3, VEN_Y, GREY)
        pial = Line([-6.3, 2.62, 0], [6.3, 2.62, 0], color=GREY, stroke_width=3)
        ven_l = T("ventricle", 24, GREY).move_to([5.6, -3.25, 0])
        tag = chip("fetal rhesus monkey", GOLD, size=24, pad=0.16).move_to([0, -3.2, 0])
        self.at("fetal rhesus monkey")
        self.play(Create(ven), Create(pial), FadeIn(ven_l), FadeIn(tag), run_time=0.9)

        p0, f0 = unit_parts(UX[0])
        unit_l = T("one unit", 24, BLUE).move_to([UX[0], -3.2, 0])
        self.at("Neurons born at one spot")
        self.play(FadeIn(p0, scale=0.6), FadeIn(unit_l), run_time=0.5)
        dots = [dot(UX[0], -2.4, YELLOW) for _ in STACK_Y]
        self.at("climb the same")
        self.play(Create(f0), run_time=0.5)
        self.play(LaggedStart(*[Succession(FadeIn(d, scale=0.5, run_time=0.1),
                                           d.animate.move_to([UX[0], y, 0]).set_run_time(0.5))
                                for d, y in zip(dots, STACK_Y)], lag_ratio=0.3), run_time=1.6)
        self.at("stack into a column")
        col0 = column_rect(UX[0])
        self.play(Create(col0), run_time=0.6)

        head = T("radial unit hypothesis", 32, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.at("radial unit hypothesis")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)

        rest = [unit_parts(x) for x in UX[1:]]
        self.at("Each patch of progenitors")
        self.play(FadeOut(head), LaggedStart(*[AnimationGroup(FadeIn(p, scale=0.6), Create(f)) for p, f in rest],
                                             lag_ratio=0.2), run_time=1.4)
        self.at("makes one column")
        cols, allds = [], []
        for x in UX[1:]:
            ds = [dot(x, y, YELLOW) for y in STACK_Y]
            allds += ds
            cols.append(column_rect(x))
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.4) for d in allds], lag_ratio=0.03),
                  *[Create(c) for c in cols], run_time=1.6)

        a = darr([-4.9, 2.98, 0], [4.9, 2.98, 0], GREEN)
        a_l = btext("area", 28, GREEN).move_to([0, 2.98, 0])
        self.at("number of units")
        self.play(GrowFromCenter(a), FadeIn(a_l), run_time=0.7)
        t = darr([-5.55, 0.6, 0], [-5.55, 2.3, 0], PURPLE)
        t_l = T("thickness", 24, PURPLE).rotate(PI / 2).move_to([-6.0, 1.45, 0])
        self.at("number of neurons in each unit")
        self.play(GrowFromCenter(t), FadeIn(t_l), run_time=0.7)
        self.at("sets the thickness")
        self.play(Indicate(col0, color=PURPLE, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
LX, RX = -3.2, 3.3          # panel centres
BY = -1.75                   # ventricle bar
COL_B, COL_H = -1.3, 2.7    # column bottom and height


def founders(cx, n, span=5.6):
    """n founder circles plus n columns, spread over `span` centred at cx."""
    sp = span / n if n > 1 else 0
    g = VGroup()
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * sp
        w = min(0.5, sp * 0.72) if n > 1 else 0.5
        c = dot(x, BY + 0.25, BLUE, r=0.17)
        r = Rectangle(width=w, height=COL_H, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW,
                      fill_opacity=0.18).move_to([x, COL_B + COL_H / 2, 0])
        g.add(c, r)
    return g


class S03Arithmetic(SpokenScene):
    """a simple model: three symmetric rounds multiply units by eight; three asymmetric divisions add a sliver."""

    def construct(self):
        head = T("A simple model", 32, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(FadeIn(head), run_time=0.5)
        vl = bar(-6.2, -0.4, BY, GREY)
        vr = bar(0.4, 6.2, BY, GREY)
        t_l = T("symmetric divisions", 28, GREEN).move_to([LX, 2.6, 0])
        t_r = T("asymmetric divisions", 28, PURPLE).move_to([RX, 2.6, 0])

        self.at("founder cells divide symmetrically")
        cur = founders(LX, 1)
        self.play(Create(vl), FadeIn(t_l), FadeIn(cur, shift=UP * 0.15), run_time=0.8)
        self.at("the pool doubles each round")
        nxt = founders(LX, 2)
        two = M("×2", 36, GREEN).move_to([LX, 2.05, 0])
        self.play(FadeTransform(cur, nxt), FadeIn(two), run_time=0.8)
        cur = nxt

        self.at("asymmetric division")
        cr = founders(RX, 1)
        crd = cr[1]
        self.play(Create(vr), FadeIn(t_r), FadeIn(cr, shift=UP * 0.15), run_time=0.8)
        top = COL_B + COL_H
        sl1 = Rectangle(width=0.5, height=0.07, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE,
                        fill_opacity=1).move_to([RX, top + 0.035, 0])
        lab1 = M("+1 neuron", 28, PURPLE).move_to([RX, 2.05, 0])
        self.at("adds only one neuron")
        self.play(FadeIn(sl1, shift=DOWN * 0.15), FadeIn(lab1), run_time=0.6)

        # reset the symmetric panel and run three rounds
        self.at("three more symmetric rounds")
        self.play(FadeOut(cur), FadeOut(two), FadeOut(sl1), FadeOut(lab1), run_time=0.4)
        cur = founders(LX, 1)
        self.play(FadeIn(cur), run_time=0.3)
        eq = M("1", 32, GREEN).move_to([LX, -2.4, 0])
        self.play(FadeIn(eq), run_time=0.2)
        self.at("rounds give")
        for n in (2, 4, 8):
            nxt = founders(LX, n)
            new_eq = M(" → ".join(str(k) for k in (1, 2, 4, 8)[: (1, 2, 4, 8).index(n) + 1]), 32, GREEN)
            new_eq.move_to([LX, -2.4, 0])
            self.play(FadeTransform(cur, nxt), ReplacementTransform(eq, new_eq), run_time=0.7)
            cur, eq = nxt, new_eq
            self.wait(0.15)
        self.at("eight times as many units")
        res_l = T("eight times as many units", 28, GREEN).move_to([LX, -3.05, 0])
        self.play(FadeIn(res_l, shift=UP * 0.1), Indicate(cur, color=GREEN, scale_factor=1.03), run_time=0.8)

        self.at("Three extra asymmetric divisions")
        sl3 = Rectangle(width=0.5, height=0.2, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE,
                        fill_opacity=1).move_to([RX, top + 0.1, 0])
        lab3 = M("+3 neurons", 28, PURPLE).move_to([RX, 2.05, 0])
        self.play(FadeIn(sl3, shift=DOWN * 0.15), FadeIn(lab3), run_time=0.7)
        self.at("a few percent more")
        res_r = T("a few percent more", 28, PURPLE).move_to([RX, -3.05, 0])
        self.play(FadeIn(res_r, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def blob(a, b, eps, cx=0.0, cy=0.0):
    return ParametricFunction(
        lambda th: np.array([cx + a * (1 + eps * np.sin(11 * th)) * np.cos(th),
                             cy + b * (1 + eps * np.sin(11 * th)) * np.sin(th), 0]),
        t_range=[0, TAU, 0.02], stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.14)


def ring_dots(cx, cy, a, b, n, color=BLUE, r=0.1):
    g = VGroup()
    for k in range(n):
        th = TAU * k / n
        g.add(dot(cx + 0.78 * a * np.cos(th), cy + 0.78 * b * np.sin(th), color, r=r))
    return g


class S04Mouse(SpokenScene):
    """a delay in the switch could multiply units; the test in mouse: stabilized beta-catenin."""

    def construct(self):
        # --- Rakic's proposal: the switch comes a few cycles later ----------------------------
        head = T("Proposal for primates", 32, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        cw = 0.95

        def row(ng, y, label):
            g = VGroup()
            for i in range(ng):
                g.add(Rectangle(width=cw, height=0.7, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                                fill_opacity=0.3).move_to([-5.5 + cw * (i + 0.5), y, 0]))
            for i in range(5):
                g.add(Rectangle(width=cw, height=0.7, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                                fill_opacity=0.3).move_to([-5.5 + cw * (ng + i + 0.5), y, 0]))
            return g

        r1 = row(3, 1.3, "")
        r2 = row(5, -0.5, "")
        k1 = T("symmetric", 24, GREEN).move_to([-5.5 + cw * 1.5, 0.65, 0])
        k2 = T("asymmetric", 24, PURPLE).move_to([-5.5 + cw * 5.5, 0.65, 0])
        self.at("a delay of only a few")
        self.play(FadeIn(head), FadeIn(r1), FadeIn(k1), FadeIn(k2), run_time=0.9)
        sw1 = Line([-5.5 + cw * 3, 1.85, 0], [-5.5 + cw * 3, 1.7, 0])
        self.play(FadeIn(r2), run_time=0.7)
        add = VGroup(r2[3], r2[4])
        k3 = T("a few more cycles before the switch", 24, GREEN).move_to([-1.5, -1.3, 0])
        self.at("cell cycles")
        self.play(Indicate(add, color=GREEN, scale_factor=1.12), FadeIn(k3), run_time=0.9)
        res = T("could account for a large increase in cortical area", 28, TEXT).move_to([0, -2.5, 0])
        self.at("large increase in cortical area")
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.7)

        # --- the mouse test -------------------------------------------------------------------
        self.at("One test came from mice")
        self.play(FadeOut(VGroup(head, r1, r2, k1, k2, k3, res)), run_time=0.5)
        tag = chip("mouse", GOLD, size=24, pad=0.16).move_to([0, 3.15, 0])
        cy = -0.1
        ea, eb = 2.0, 1.55
        left = blob(ea, eb, 0.0, -3.2, cy)
        l_lbl = T("normal", 26, GREY).move_to([-3.2, -3.0, 0])
        ldots = ring_dots(-3.2, cy, ea, eb, 8)
        self.play(FadeIn(tag), FadeIn(left), FadeIn(ldots), FadeIn(l_lbl), run_time=0.7)

        right = blob(ea, eb, 0.0, 3.4, cy)
        rdots = ring_dots(3.4, cy, ea, eb, 8)
        chipb = chip("stabilized β-catenin", ORANGE, size=26).move_to([3.4, 2.75, 0])
        r_lbl = T("transgenic", 26, ORANGE).move_to([3.4, -3.0, 0])
        self.at("stabilized form")
        self.play(FadeIn(right), FadeIn(rdots), FadeIn(chipb, shift=DOWN * 0.15), FadeIn(r_lbl), run_time=0.8)
        more = ring_dots(3.4, cy, ea, eb, 16)
        self.at("More progenitors kept")
        self.play(Transform(rdots, more), Indicate(rdots, color=BLUE, scale_factor=1.1), run_time=1.0)
        big = blob(2.7, 2.1, 0.0, 3.4, cy)
        bigdots = ring_dots(3.4, cy, 2.7, 2.1, 16)
        self.at("large brains")
        self.play(Transform(right, big), Transform(rdots, bigdots), run_time=1.1)
        fold = blob(2.7, 2.1, 0.07, 3.4, cy)
        self.at("buckled into folds")
        f_lbl = T("folds", 28, YELLOW).move_to([3.4, -3.0, 0])
        self.play(Transform(right, fold), FadeIn(f_lbl), FadeOut(r_lbl), run_time=1.2)
        sm_lbl = T("smooth", 28, YELLOW)
        self.play(ReplacementTransform(l_lbl, sm_lbl.move_to([-3.2, -3.0, 0])), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Orgs(SpokenScene):
    """outer radial glia: fibre to the surface, no ventricle contact, dividing far from the ventricle."""

    def construct(self):
        ven = bar(-6.3, 0.9, -2.75, GREY)
        pial = Line([-6.3, 2.75, 0], [0.9, 2.75, 0], color=GREY, stroke_width=3)
        ven_l = T("ventricle", 24, GREY).move_to([-5.4, -3.25, 0])
        pial_l = T("brain surface", 24, GREY).move_to([-5.2, 3.2, 0])

        self.at("In primates")
        self.play(Create(ven), Create(pial), FadeIn(ven_l), FadeIn(pial_l), run_time=0.8)
        # classical radial glia, attached to the ventricle
        rg = Ellipse(width=0.8, height=0.34, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                     fill_opacity=0.5).move_to([-5.2, -2.45, 0])
        rg_f = Line([-5.2, -2.28, 0], [-5.2, 2.75, 0], color=BLUE, stroke_width=3).set_opacity(0.6)
        rg_l = T("classical", 24, BLUE).move_to([-5.2, -1.55, 0])
        rg_l.set_x(-5.2).shift(RIGHT * 0.0)
        rg_l.add_background_rectangle(BG, 1, buff=0.05)
        self.play(FadeIn(rg, scale=0.6), Create(rg_f), FadeIn(rg_l), run_time=0.8)

        tag = chip("human fetal cortex", GOLD, size=24, pad=0.16).move_to([-1.9, 3.2, 0])
        self.at("In human fetal cortex")
        self.play(FadeIn(tag), run_time=0.4)
        xs = [-3.5, -2.0, -0.5]
        tops = [-4.3, -2.0, 0.3]
        bodies = [Circle(radius=0.26, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.5)
                  .move_to([x, 0.0, 0]) for x in xs]
        self.at("outer radial glia")
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in bodies], lag_ratio=0.2), run_time=0.9)
        o_l = T("outer radial glia", 26, PINK).move_to([-2.0, -0.85, 0])
        self.play(FadeIn(o_l), run_time=0.4)
        fibres = [Line([x, 0.26, 0], [tx, 2.75, 0], color=PINK, stroke_width=3).set_opacity(0.8)
                  for x, tx in zip(xs, tops)]
        self.at("keep a long fiber")
        self.play(*[Create(f) for f in fibres], run_time=1.0)
        cross = VGroup(Line([-3.4, -1.85, 0], [-2.6, -1.35, 0], color=RED, stroke_width=5),
                       Line([-3.4, -1.35, 0], [-2.6, -1.85, 0], color=RED, stroke_width=5))
        # keep the cross clear of the label: put the note under the cells
        gap = DashedLine([-2.0, -1.2, 0], [-2.0, -2.45, 0], color=RED, stroke_width=3, dash_length=0.12)
        gap.shift(DOWN * 0.0)
        note = T("no process to the ventricle", 24, RED).move_to([-2.0, -1.75, 0])
        note.add_background_rectangle(BG, 1, buff=0.05)
        self.at("no process touching the ventricle")
        self.play(Create(gap), FadeIn(note), run_time=0.8)
        self.at("They divide there")
        d1 = bodies[1].copy()
        d2 = bodies[1].copy()
        self.add(d1, d2)
        self.play(d1.animate.shift(LEFT * 0.17), d2.animate.shift(RIGHT * 0.17), run_time=0.8)
        self.at("renew themselves")
        self.play(Indicate(d1, color=PINK, scale_factor=1.25), Indicate(d2, color=PINK, scale_factor=1.25), run_time=0.8)
        self.at("diverge")
        out_l = arr([-4.1, 2.35, 0], [-4.9, 2.35, 0], GREY, w=4, tip=0.18)
        out_r = arr([-0.1, 2.35, 0], [0.7, 2.35, 0], GREY, w=4, tip=0.18)
        self.play(GrowArrow(out_l), GrowArrow(out_r), run_time=0.6)

        # species strip
        rows = [("primates", "abundant", 2.0), ("ferret", "abundant", 0.9), ("mouse", "rare", -0.2)]
        grp = VGroup()
        for name, word, y in rows:
            nm = T(name, 28, TEXT).move_to([1.7, y, 0]).align_to([1.7, y, 0], LEFT)
            wd = T(word, 28, PINK).move_to([4.6, y, 0]).align_to([4.4, y, 0], LEFT)
            grp.add(VGroup(nm, wd))
        self.at("abundant in primates")
        self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.2) for g in grp[:2]], lag_ratio=0.4), run_time=1.0)
        self.at("rare in mouse")
        self.play(FadeIn(grp[2], shift=LEFT * 0.2), run_time=0.6)
        mm = T("marmoset", 26, TEXT).move_to([1.7, -1.5, 0]).align_to([1.7, -1.5, 0], LEFT)
        mm_d = T("present, cortex nearly smooth", 22, GREY).move_to([1.7, -2.05, 0]).align_to([1.7, -2.05, 0], LEFT)
        self.at("The marmoset has them too")
        self.play(FadeIn(mm), FadeIn(mm_d), run_time=0.7)
        self.at("do not guarantee folding")
        verdict = T("not enough for folding", 26, GOLD).move_to([3.95, -3.0, 0])
        self.play(FadeIn(verdict), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Genes(SpokenScene):
    """what was tested, in which system; nothing in a developing human brain; the rule."""

    def construct(self):
        head = T("Human genes, and where they were tested", 30, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        rows = [
            ("ARHGAP11B", "mouse embryo", "more basal progenitors", 2.3),
            ("ARHGAP11B", "marmoset fetus", "larger neocortex", 1.35),
            ("NOTCH2NL", "mouse cortex", "progenitors keep dividing", 0.4),
            ("NOTCH2NL deleted", "human organoid", "progenitors differentiate early", -0.55),
            ("SRGAP2C", "mouse neurons", "slower spine maturation", -1.5),
        ]
        built = []
        for g, s, r, y in rows:
            gc = chip(g, ORANGE, size=26, pad=0.16)
            gc.move_to([-4.2, y, 0])
            sy = T(s, 26, GREY).move_to([-0.9, y, 0]).align_to([-1.6, y, 0], LEFT)
            re = T(r, 24, TEXT).move_to([2.0, y, 0]).align_to([2.0, y, 0], LEFT)
            built.append((gc, sy, re))
        self.at("have been tested")
        self.play(FadeIn(head), run_time=0.6)
        self.at("increased basal progenitors")
        for gc, sy, re in built[0:1]:
            self.play(FadeIn(gc, shift=RIGHT * 0.2), FadeIn(sy), FadeIn(re), run_time=0.7)
        self.at("marmoset fetuses")
        for gc, sy, re in built[1:2]:
            self.play(FadeIn(gc, shift=RIGHT * 0.2), FadeIn(sy), FadeIn(re), run_time=0.7)
        self.at("kept progenitors dividing")
        for gc, sy, re in built[2:3]:
            self.play(FadeIn(gc, shift=RIGHT * 0.2), FadeIn(sy), FadeIn(re), run_time=0.7)
        self.at("deleting it")
        for gc, sy, re in built[3:4]:
            self.play(FadeIn(gc, shift=RIGHT * 0.2), FadeIn(sy), FadeIn(re), run_time=0.7)
        self.at("differentiate early")
        for gc, sy, re in built[4:5]:
            self.play(FadeIn(gc, shift=RIGHT * 0.2), FadeIn(sy), FadeIn(re), run_time=0.7)

        box = RoundedRectangle(corner_radius=0.14, width=11.6, height=0.95, stroke_color=RED, stroke_width=3,
                               fill_opacity=0).move_to([0, -2.75, 0])
        dash = DashedVMobject(box, num_dashes=60)
        txt = T("gene removed from a developing human brain", 26, RED).move_to([-1.6, -2.75, 0])
        no = T("not tested", 26, RED, weight=BOLD).move_to([4.6, -2.75, 0])
        self.at("developing human brain")
        self.play(Create(dash), FadeIn(txt), FadeIn(no), run_time=0.9)
        self.at("one gene made the human cortex")
        self.play(Indicate(VGroup(txt, no), color=RED, scale_factor=1.04), run_time=0.8)

        self.at("Keep the rule")
        self.play(FadeOut(VGroup(head, dash, txt, no, *[m for tr in built for m in tr])), run_time=0.6)
        rule = T("To gain area, change the founder phase", 38, GOLD, font=TITLE_FONT).move_to([0, 2.2, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.6)
        vv = bar(-5.5, 5.5, -2.6, GREY)
        f = founders(0, 1, span=10).move_to([0, -0.5, 0])
        self.at("To gain area")
        self.play(Create(vv), FadeIn(f), run_time=0.5)
        cur = f
        self.at("change the founder phase")
        for n in (2, 4, 8):
            nxt = founders(0, n, span=10.4).move_to([0, -0.5, 0])
            self.play(FadeTransform(cur, nxt), run_time=0.4)
            cur = nxt
        self.finish()


class S07End(EndCard):
    LINE = "To gain area, change the founder phase."
