"""Reading a neuron's birth year  (Developmental Neuroscience explainer, adult neurogenesis)

COLOR MAP (one color per concept, whole film)
  ORANGE = carbon-14 (the atmospheric curve, the level written into DNA, the carbon-14 estimate)
  BLUE   = neurons (cells, nuclei)
  GREY   = structure, axes, other (non-neuronal) cells, cards
  YELLOW = the birth year marker
  PURPLE = the hippocampus (dentate gyrus outline)
  GREEN  = young neurons seen by a stain
  RED    = a lost marker / missing signal
  TEXT   = the rule and the average
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def level(y):
    if y < 1955:
        return 1.0
    if y <= 1963:
        return 1.0 + 0.9 * ((y - 1955) / 8.0) ** 1.6
    return 1.9 - 0.6 * (y - 1963) / 52.0   # schematic: a plain declining line


def make_axes(center, w, h):
    ax = Axes(x_range=[1935, 2015, 10], y_range=[0.0, 2.2, 0.5], x_length=w, y_length=h,
              axis_config={"include_tip": False, "include_numbers": False, "include_ticks": False,
                           "stroke_color": GREY, "stroke_width": 3})
    ax.move_to([center[0], center[1], 0])
    return ax


def year_label(ax, yr, color=GREY, size=22, drop=0.3):
    return M(str(yr), size, color).move_to(ax.c2p(yr, 0.0) + DOWN * drop)


def curve_pieces(ax):
    a = ax.plot(level, x_range=[1935, 1955], color=ORANGE, stroke_width=6)
    b = ax.plot(level, x_range=[1955, 1963], color=ORANGE, stroke_width=6)
    c = ax.plot(level, x_range=[1963, 2015], color=ORANGE, stroke_width=6)
    return a, b, c


def cell(r=0.8, color=BLUE, nuc=0.4):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)
    n = Circle(radius=r * nuc, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    return VGroup(body, n)


def dna_bar(frac, w=1.8, h=0.3):
    out = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=GREY, stroke_width=3,
                           fill_color=BG, fill_opacity=1)
    fill = Rectangle(width=max(0.001, (w - 0.1) * frac), height=h - 0.1, stroke_width=0,
                     fill_color=ORANGE, fill_opacity=0.95)
    fill.move_to(out.get_left() + RIGHT * (0.05 + fill.width / 2))
    return VGroup(out, fill)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dg_arc(r=1.9, color=PURPLE, n=14, scale_dots=0.13):
    """Dentate gyrus as a thick C-shaped arc with neurons (dots) along it. Returns (group, dots)."""
    arc = Arc(radius=r, start_angle=-0.2 * PI, angle=1.4 * PI, stroke_color=color, stroke_width=26)
    arc.set_stroke(opacity=0.35)
    dots = VGroup()
    for k in range(n):
        t = (k + 0.5) / n
        ang = -0.2 * PI + 1.4 * PI * t
        p = arc.get_arc_center() + r * np.array([np.cos(ang), np.sin(ang), 0])
        dots.add(Dot(p, radius=scale_dots, color=BLUE))
    return VGroup(arc, dots), dots


class S00Title(TitleCard):
    LESSON = "New neurons in the adult brain"
    TITLE = "Reading a neuron's birth year"


# ---------------------------------------------------------------------------------------------
class S01Birthday(SpokenScene):
    def construct(self):
        brain = Ellipse(width=6.0, height=4.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
        brain.move_to([-3.3, 0.85, 0])
        patch = Sector(radius=1.0, angle=PI * 0.9, start_angle=-0.45 * PI, stroke_width=0,
                       fill_color=BLUE, fill_opacity=0.55).scale([1.1, 1.5, 1]).move_to(brain.get_right() + LEFT * 0.75)
        patch.move_to(brain.get_right() + LEFT * 0.62 + UP * 0.0)
        blbl = T("cerebral cortex", 26, GREY).next_to(brain, UP, buff=0.2)
        back = T("back", 24, BLUE).next_to(brain, RIGHT, buff=0.15).shift(DOWN * 0.1)
        self.at("The neurons at the back")
        self.play(FadeIn(brain), FadeIn(blbl), run_time=0.6)
        self.play(FadeIn(patch), FadeIn(back), run_time=0.6)

        c = cell(1.5).move_to([4.0, 1.1, 0])
        zl1 = DashedLine(patch.get_top() + RIGHT * 0.2, c.get_top() + LEFT * 0.4, color=GREY, stroke_width=3)
        zl2 = DashedLine(patch.get_bottom() + RIGHT * 0.2, c.get_bottom() + LEFT * 0.4, color=GREY, stroke_width=3)
        self.at("are as old as you are")
        self.play(Create(zl1), Create(zl2), FadeIn(c, scale=0.6), run_time=0.8)
        tag = bchip("born: ?", YELLOW, 34).move_to([4.0, -1.0, 0])
        self.at("How could anyone know")
        self.play(FadeIn(tag, shift=UP * 0.15), Indicate(c, color=BLUE, scale_factor=1.06), run_time=0.8)

        doc = VGroup(RoundedRectangle(corner_radius=0.08, width=1.5, height=1.9, stroke_color=GREY, stroke_width=3,
                                      fill_color=BG, fill_opacity=1),
                     *[Line([-0.45, 0.45 - 0.3 * i, 0], [0.45, 0.45 - 0.3 * i, 0], color=GREY, stroke_width=3) for i in range(3)])
        doc.move_to([-5.2, -2.55, 0])
        xx = VGroup(Line(doc.get_corner(UL), doc.get_corner(DR), color=RED, stroke_width=7),
                    Line(doc.get_corner(UR), doc.get_corner(DL), color=RED, stroke_width=7))
        dlbl = T("no birth certificate", 26, GREY).next_to(doc, RIGHT, buff=0.3)
        self.at("A cell carries no birth certificate")
        self.play(FadeIn(doc), FadeIn(dlbl), run_time=0.5)
        self.play(Create(xx), run_time=0.5)

        bomb = bchip("nuclear bomb tests", ORANGE, 34).move_to([3.6, -2.6, 0])
        self.at("nuclear bomb tests")
        self.play(FadeIn(bomb, shift=UP * 0.2), run_time=0.7)
        self.play(Wiggle(tag, scale_value=1.08, rotation_angle=0.02 * TAU), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02BombCurve(SpokenScene):
    def construct(self):
        ax = make_axes([0, -0.5], 11.4, 4.5)
        a, b, c = curve_pieces(ax)
        ylab = T("carbon-14 in the air", 28, ORANGE).move_to([-4.2, 3.2, 0])
        base = DashedLine(ax.c2p(1935, 1.0), ax.c2p(2015, 1.0), color=GREY, stroke_width=2)
        sch = T("schematic", 24, GREY).move_to(ax.c2p(2003, 0.45))
        self.play(Create(ax), FadeIn(ylab), FadeIn(sch), run_time=0.8)
        self.at("steady rate")
        self.play(Create(base), Create(a), run_time=1.2)
        steady = T("steady", 26, GREY).move_to(ax.c2p(1945, 1.0) + UP * 0.35)
        self.play(FadeIn(steady), run_time=0.3)

        band = Rectangle(width=ax.c2p(1963, 0)[0] - ax.c2p(1955, 0)[0], height=ax.c2p(0, 2.2)[1] - ax.c2p(0, 0.0)[1],
                         stroke_width=0, fill_color=ORANGE, fill_opacity=0.14)
        band.move_to([(ax.c2p(1955, 0)[0] + ax.c2p(1963, 0)[0]) / 2, (ax.c2p(0, 2.2)[1] + ax.c2p(0, 0.0)[1]) / 2, 0])
        y55 = year_label(ax, 1955, ORANGE)
        y63 = year_label(ax, 1963, ORANGE)
        self.at("weapons tests")
        self.play(FadeIn(band), FadeIn(y55), FadeIn(y63), FadeOut(steady), run_time=0.8)
        self.at("nearly doubled")
        self.play(Create(b, rate_func=smooth), run_time=1.0)
        guide = DashedLine(ax.c2p(1938, 1.9), ax.c2p(1963, 1.9), color=ORANGE, stroke_width=2)
        dbl = DoubleArrow(ax.c2p(1938, 1.0), ax.c2p(1938, 1.9), buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        dlbl = T("nearly doubled", 26, TEXT).move_to(ax.c2p(1948.5, 1.45))
        self.play(Create(guide), GrowFromCenter(dbl), FadeIn(dlbl), run_time=0.5)
        self.at("northern hemisphere")
        self.play(Indicate(dlbl, color=TEXT, scale_factor=1.05), run_time=0.6)

        self.at("treaty")
        tl = DashedLine(ax.c2p(1963, 0.0), ax.c2p(1963, 2.2), color=YELLOW, stroke_width=3)
        tt = T("1963 treaty: no tests in the air", 26, YELLOW).move_to(ax.c2p(1990, 2.2) + UP * 0.2)
        self.play(Create(tl), FadeIn(tt, shift=RIGHT * 0.2), FadeOut(guide), FadeOut(dbl), FadeOut(dlbl), run_time=0.8)
        self.at("year by year")
        dot = Dot(ax.c2p(1963, level(1963)), radius=0.12, color=YELLOW)
        self.add(dot)
        self.play(Create(c, rate_func=linear), MoveAlongPath(dot, c, rate_func=linear), run_time=self.beat(0.2))
        y90 = year_label(ax, 1990, GREY)
        self.play(FadeIn(y90), FadeOut(dot), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03IntoDna(SpokenScene):
    def construct(self):
        y = 2.2
        air = bchip("air: carbon-14", ORANGE, 28).move_to([-4.9, y, 0])
        plants = bchip("plants", GREY, 28).move_to([-1.3, y, 0])
        people = bchip("people", GREY, 28).move_to([4.7, y, 0])
        animals = bchip("animals", GREY, 28).move_to([1.7, y + 1.0, 0])
        a1 = arrow(air.get_right(), plants.get_left(), ORANGE)
        a2 = arrow(plants.get_right(), people.get_left(), ORANGE)
        a3 = arrow(plants.get_right() + UP * 0.1, animals.get_left(), ORANGE)
        a4 = arrow(animals.get_right(), people.get_left() + UP * 0.1, ORANGE)
        self.at("Plants fix that carbon dioxide")
        self.play(FadeIn(air), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(plants, shift=RIGHT * 0.2), run_time=0.8)
        self.at("People eat the plants")
        self.play(GrowArrow(a2), FadeIn(people, shift=RIGHT * 0.2), run_time=0.8)
        self.at("or animals that ate them")
        self.play(GrowArrow(a3), FadeIn(animals), GrowArrow(a4), run_time=0.9)

        c = cell(1.35, BLUE, 0.35).move_to([0.0, -0.6, 0])
        cl = T("a cell that divides", 28, BLUE).next_to(c, LEFT, buff=0.5)
        down = arrow(people.get_bottom() + LEFT * 0.2, c.get_right() + UP * 0.35, ORANGE)
        self.at("ends up in the DNA")
        self.play(FadeIn(c, scale=0.8), FadeIn(cl), GrowArrow(down), run_time=0.8)
        dna = dna_bar(0.0, 3.0, 0.4).move_to([0.0, -2.65, 0])
        dlbl = T("DNA", 26, GREY).next_to(dna, LEFT, buff=0.3)
        self.play(FadeIn(dna), FadeIn(dlbl), run_time=0.4)
        fill = dna_bar(0.7, 3.0, 0.4).move_to(dna)
        self.play(Transform(dna, fill), run_time=0.9)

        self.at("each new cell records")
        c2 = c.copy()
        d2 = dna.copy()
        left = VGroup(c, dna)
        right = VGroup(c2, d2)
        self.add(right)
        self.play(FadeOut(VGroup(cl, dlbl, down)), left.animate.shift(LEFT * 3.3), right.animate.shift(RIGHT * 3.3), run_time=1.0)
        yr = T("that year's\nlevel", 28, ORANGE, line_spacing=0.8).move_to([0, -2.65, 0])
        self.play(FadeIn(yr), Indicate(VGroup(dna[1], d2[1]), color=ORANGE, scale_factor=1.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Frozen(SpokenScene):
    def construct(self):
        ax = make_axes([0, 1.75], 11.4, 3.0)
        a, b, c = curve_pieces(ax)
        ylab = T("carbon-14 in the air", 24, ORANGE).move_to([-4.6, 3.55, 0])
        yb, yt = 1975, 1990
        birth_x = ax.c2p(yb, level(yb))
        ylabs = [year_label(ax, 1963, ORANGE, 22, 0.28), year_label(ax, 2005, GREY, 22, 0.28)]
        plot = VGroup(ax, a, b, c, ylab, *ylabs)
        sch = T("schematic", 22, GREY).move_to(ax.c2p(2003, 0.45))
        plot.add(sch)
        self.add(plot)

        n = cell(0.95).move_to([-5.0, -1.75, 0])
        nl = T("a neuron", 28, BLUE).next_to(n, UP, buff=0.15)
        dna = dna_bar(0.0, 2.2, 0.36).move_to([-5.0, -3.2, 0])
        self.at("Now think about a neuron")
        self.play(FadeIn(n, scale=0.7), FadeIn(nl), FadeIn(dna), run_time=0.8)

        stop = bchip("no more DNA copying", GREY, 26).move_to([-1.2, -1.75, 0])
        self.at("stopped dividing")
        self.play(FadeIn(stop), run_time=0.5)

        self.at("keeps the carbon")
        vline = DashedLine(ax.c2p(yb, 0.0), ax.c2p(yb, 2.2), color=YELLOW, stroke_width=3)
        bl = T("birth year", 24, YELLOW).move_to(ax.c2p(yb, 2.2) + UP * 0.28)
        mk = Dot(birth_x, radius=0.13, color=YELLOW)
        self.play(Create(vline), FadeIn(bl), FadeIn(mk), FadeOut(stop), run_time=0.8)
        fill = dna_bar(0.7, 2.2, 0.36).move_to(dna)
        self.play(Transform(dna, fill), Indicate(mk, color=YELLOW), run_time=0.9)

        self.at("sorted nuclei")
        bin_n = bchip("neurons", BLUE, 26).move_to([-0.2, -3.05, 0])
        bin_o = bchip("other cells", GREY, 26).move_to([3.9, -3.05, 0])
        nuc_b = VGroup(*[Dot([-1.6 + 0.5 * i, -1.2 + (0.35 if i % 2 else 0), 0], radius=0.19, color=BLUE) for i in range(5)])
        nuc_g = VGroup(*[Dot([2.5 + 0.5 * i, -1.2 + (0.35 if i % 2 else 0), 0], radius=0.19, color=GREY) for i in range(5)])
        mixed = VGroup(*nuc_b, *nuc_g)
        self.play(FadeOut(VGroup(n, nl, dna)), FadeIn(mixed), run_time=0.6)
        self.play(FadeIn(bin_n), FadeIn(bin_o),
                  *[d.animate.move_to([-1.1 + 0.5 * i, -2.15, 0]) for i, d in enumerate(nuc_b)],
                  *[d.animate.move_to([3.0 + 0.5 * i, -2.15, 0]) for i, d in enumerate(nuc_g)], run_time=1.0)

        self.at("occipital cortex")
        mkn = Dot(birth_x, radius=0.2, color=BLUE)
        lk_n = DashedLine(bin_n.get_top() + UP * 0.9, mkn.get_center() + DOWN * 0.25, color=BLUE, stroke_width=3)
        nlab = T("same as birth year", 26, BLUE).move_to(birth_x + LEFT * 2.0 + DOWN * 0.75).set_x(birth_x[0] - 1.75)
        self.play(Indicate(VGroup(*bin_n[1:]), color=BLUE, scale_factor=1.1), Create(lk_n), FadeIn(mkn, scale=1.5), run_time=0.8)
        self.play(FadeIn(nlab), run_time=0.4)
        self.at("were younger")
        og = ax.c2p(yt, level(yt))
        mko = Dot(og, radius=0.2, color=GREY)
        olab = T("lower: born later", 26, GREY).move_to(og + UP * 0.6 + RIGHT * 0.3)
        lk_o = DashedLine(bin_o.get_top() + UP * 0.9, mko.get_center() + DOWN * 0.25, color=GREY, stroke_width=3)
        self.play(Indicate(VGroup(*bin_o[1:]), color=GREY, scale_factor=1.1), Create(lk_o), FadeIn(mko, scale=1.5), FadeIn(olab), run_time=0.8)

        self.at("many nuclei")
        self.play(FadeOut(VGroup(bin_n, bin_o, mkn, mko, olab, nlab, lk_n, lk_o, nuc_b, nuc_g, vline, bl, mk)),
                  plot.animate.scale(1.1).move_to([0, 0.2, 0]), run_time=0.8)
        xs = [1966, 1972, 1975, 1980, 1990]
        pts = VGroup(*[Dot(ax.c2p(x, level(x)), radius=0.15, color=BLUE) for x in xs])
        self.play(FadeIn(pts), run_time=0.5)
        mean_x = float(np.mean(xs))
        avg = Square(side_length=0.36, stroke_width=0, fill_color=TEXT, fill_opacity=1).rotate(PI / 4).move_to(ax.c2p(mean_x, level(mean_x)))
        alab = T("average", 30, TEXT).move_to(ax.c2p(mean_x, level(mean_x)) + DOWN * 0.9 + RIGHT * 1.0)
        self.at("average")
        self.play(*[p.animate.move_to(avg.get_center()) for p in pts], run_time=0.8)
        self.play(FadeIn(avg, scale=1.6), FadeOut(pts), FadeIn(alab), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Hippocampus(SpokenScene):
    def construct(self):
        title = T("the hippocampus: dentate gyrus (schematic)", 32, PURPLE).move_to([0, 3.2, 0])
        g, dots = dg_arc(2.9, PURPLE, 18, 0.17)
        g.move_to([-3.3, -0.1, 0])
        self.at("What about the hippocampus")
        self.play(FadeIn(title), FadeIn(g), run_time=1.0)
        self.at("one third")
        third = [dots[i] for i in range(0, 18, 3)]
        rings = VGroup(*[Circle(radius=0.3, stroke_color=ORANGE, stroke_width=5).move_to(d) for d in third])
        est = VGroup(T("carbon-14 estimate, 2013", 32, ORANGE), T("about one third\nsubject to exchange", 32, TEXT, line_spacing=0.8)
                     ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.4, 0.9, 0])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), FadeIn(est[0]), run_time=1.0)
        self.play(FadeIn(est[1]), run_time=0.4)
        self.at("per day")
        per = T("about 700 new neurons\nper hippocampus per day", 32, TEXT, line_spacing=0.8).move_to([3.4, -1.3, 0])
        self.play(FadeIn(per, shift=UP * 0.15), run_time=0.6)

        # two stain studies, equal weight
        self.at("looked for young neurons")
        self.play(FadeOut(VGroup(title, g, rings, est, per)), run_time=0.6)
        L, dl = dg_arc(2.0, PURPLE, 16, 0.13)
        R, dr = dg_arc(2.0, PURPLE, 16, 0.13)
        L.move_to([-3.4, 0.0, 0]); R.move_to([3.4, 0.0, 0])
        lh = VGroup(T("2018", 32, TEXT), T("adults aged 18 to 77", 26, GREY)).arrange(DOWN, buff=0.12).move_to([-3.4, 2.9, 0])
        rh = VGroup(T("the next month", 32, TEXT), T("healthy people aged 14 to 79", 26, GREY)).arrange(DOWN, buff=0.12).move_to([3.4, 2.9, 0])
        self.play(FadeIn(L), FadeIn(R), FadeIn(lh), FadeIn(rh), run_time=0.9)
        sch2 = T("schematic", 24, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(sch2), run_time=0.3)
        self.at("none were detected")
        nonel = T("none detected", 28, TEXT).move_to([-3.4, -2.6, 0])
        self.play(FadeIn(nonel), run_time=0.6)
        self.at("another reported")
        cen = R[0].get_arc_center()
        young = VGroup(*[Dot(cen + 1.45 * np.array([np.cos(a), np.sin(a), 0]), radius=0.12, color=GREEN)
                         for a in np.linspace(-0.1 * PI, 1.05 * PI, 16)])
        manyl = T("thousands of young neurons", 28, TEXT).move_to([3.4, -2.6, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in young], lag_ratio=0.05), FadeIn(manyl), run_time=1.2)
        self.at("still argued over")
        q = T("?", 120, YELLOW, weight=BOLD).move_to([0, 0.0, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Method(SpokenScene):
    def construct(self):
        head = T("why careful laboratories disagree", 34, font=TITLE_FONT).move_to([0, 3.2, 0])
        g0, _d0 = dg_arc(2.0, PURPLE, 16, 0.14)
        g0.move_to([0, -0.2, 0])
        q0 = T("?", 120, YELLOW, weight=BOLD).move_to([0, -0.5, 0])
        self.add(head)
        self.play(FadeIn(g0), FadeIn(q0), run_time=0.8)
        W, H, Y = 4.0, 4.8, -0.1
        xs = [-4.25, 0.0, 4.25]
        cards = []
        for x, name in zip(xs, ["tissue handling", "what markers mark", "carbon-14 model"]):
            box = RoundedRectangle(corner_radius=0.2, width=W, height=H, stroke_color=GREY, stroke_width=2.5).move_to([x, Y, 0])
            t = T(name, 28, TEXT).move_to([x, Y + H / 2 - 0.5, 0])
            cards.append((box, t))
        self.at("arguments are about method")
        self.play(FadeOut(g0), FadeOut(q0), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(t)) for b, t in cards], lag_ratio=0.2), run_time=1.2)

        # card 1: stain fades with time after death
        cx = xs[0]
        sd = VGroup(*[Dot([cx - 1.4 + 0.7 * i, Y + 0.7, 0], radius=0.2, color=GREEN) for i in range(5)])
        c1l = T("time after death", 26, GREY).move_to([cx, Y - 0.35, 0])
        c1a = arrow([cx - 1.4, Y - 0.85, 0], [cx + 1.4, Y - 0.85, 0], GREY, 4)
        self.at("weakens with time")
        self.play(FadeIn(sd), FadeIn(c1l), GrowArrow(c1a), run_time=0.6)
        self.play(sd.animate.set_opacity(0.12), run_time=1.6)
        self.at("marker was lost")
        lost = T("no signal:\nmarker lost?", 28, RED, line_spacing=0.8).move_to([cx, Y - 1.75, 0])
        self.play(FadeIn(lost, shift=UP * 0.1), run_time=0.6)

        # card 2: is the stain only newborn neurons?
        cx = xs[1]
        d2 = Dot([cx - 1.0, Y + 0.7, 0], radius=0.34, color=GREEN)
        r2 = VGroup(Dot([cx + 0.1, Y + 0.7, 0], radius=0.2, color=BLUE), Dot([cx + 0.9, Y + 0.7, 0], radius=0.2, color=BLUE))
        q2 = T("only newborn\nneurons?", 28, YELLOW, line_spacing=0.8).move_to([cx, Y - 0.6, 0])
        self.at("label only newborn neurons")
        self.play(FadeIn(d2, scale=0.5), run_time=0.5)
        self.play(FadeIn(r2), FadeIn(q2), run_time=0.7)
        self.play(Indicate(d2, color=GREEN, scale_factor=1.3), run_time=0.6)

        # card 3: model
        cx = xs[2]
        mm = bchip("turnover model", ORANGE, 26).move_to([cx, Y + 0.6, 0])
        as2 = T("rests on\nassumptions", 28, GREY, line_spacing=0.8).move_to([cx, Y - 0.7, 0])
        self.at("turnover model")
        self.play(FadeIn(mm, shift=DOWN * 0.1), FadeIn(as2), run_time=0.7)

        self.at("does not yet settle it")
        self.play(*[FadeOut(m) for m in (head, sd, c1l, c1a, lost, d2, r2, q2, mm, as2)],
                  *[FadeOut(m) for pair in cards for m in pair], run_time=0.7)
        g, dots = dg_arc(2.3, PURPLE, 18, 0.15)
        g.move_to([-3.4, 0.9, 0])
        q = T("?", 160, YELLOW, weight=BOLD).move_to([3.4, 0.9, 0])
        st = T("the evidence does not yet settle it", 34, TEXT).move_to([0, -1.7, 0])
        self.play(FadeIn(g), FadeIn(q, scale=0.6), FadeIn(st), run_time=0.8)
        self.at("what a study can show")
        rule = T("Ask what a study can show, and what it cannot.", 34, GOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what a marker study can show, and what it cannot."
