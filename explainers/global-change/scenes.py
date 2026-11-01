"""Global change: a warming mountain outruns its species  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  RED    = the isotherm and warming (the moving warm line)
  GREEN  = the species (dots on the slope)
  YELLOW = the lag, the gap between line and species
  TEAL   = the invented inputs (warming rate, lapse rate) and the arithmetic
  ORANGE = other possible drivers (barrier, forest loss, alternatives)
  GREY   = the mountain, the start level, labels
Scale on the mountain: 1 unit of height = 50 m, so 11 m = 0.22 units, 150 m = 3 units.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

PEAK = np.array([-3.4, 3.0, 0])
LFOOT = np.array([-6.2, -3.3, 0])
RFOOT = np.array([-0.6, -3.3, 0])
Y0 = -1.6           # start level of the isotherm and the species
U = 0.02            # height units per metre


def sl(y):
    return LFOOT[0] + (y - LFOOT[1]) * (PEAK[0] - LFOOT[0]) / (PEAK[1] - LFOOT[1])


def sr(y):
    return PEAK[0] + (PEAK[1] - y) * (RFOOT[0] - PEAK[0]) / (PEAK[1] - RFOOT[1])


def mountain():
    m = Polygon(LFOOT, PEAK, RFOOT, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
    return m


def iso(y, color=RED, dashed=True, w=5):
    a, b = np.array([sl(y) - 0.45, y, 0]), np.array([sr(y) + 0.3, y, 0])
    return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.18) if dashed else Line(a, b, color=color, stroke_width=w)


def lbl_on(text, y, color, size=24):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.16, height=t.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(back, t.move_to(back))
    g.move_to([sr(y) + 0.35 + g.width / 2, y, 0])
    return g


def dots(y, n=3, color=GREEN):
    xs = [sl(y) + 0.35, sl(y) + 0.65, sl(y) + 0.95]
    return VGroup(*[Dot([x, y + (0.08 if i == 1 else -0.06), 0], radius=0.12, color=color) for i, x in enumerate(xs[:n])])


def splabel(y, size=24):
    t = T("species", size, GREEN)
    back = Rectangle(width=t.width + 0.12, height=t.height + 0.08, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(back, t.move_to(back))
    return g.move_to([sl(y - 0.5) + 1.1, y - 0.5, 0])


def bracket(x, y0, y1, color):
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=4),
                  Line([x - 0.1, y0, 0], [x + 0.1, y0, 0], color=color, stroke_width=4),
                  Line([x - 0.1, y1, 0], [x + 0.1, y1, 0], color=color, stroke_width=4))


def panel_chip(text, color, size=24, w=None):
    c = chip(text, color, size=size)
    return c


class S00Title(TitleCard):
    LESSON = "Global change across scales"
    TITLE = "A warming mountain outruns its species"


# ---------------------------------------------------------------------------------------------
class S01Isotherm(SpokenScene):
    def construct(self):
        mt = mountain()
        line = iso(Y0)
        lab = lbl_on("isotherm", Y0, RED)
        sp = dots(Y0)
        sp_lab = splabel(Y0)
        q = T("?", 56, YELLOW, weight=BOLD).move_to([sl(Y0 + 1.5) + 1.0, Y0 + 1.5, 0])

        self.at("If a mountain warms")
        self.play(Create(mt), run_time=0.7)
        self.play(Create(line), FadeIn(lab), FadeIn(sp, scale=0.6), FadeIn(sp_lab), run_time=0.45)
        self.at("where does")
        self.play(FadeIn(q, scale=0.5), run_time=0.4)
        self.play(Indicate(sp, color=GREEN), run_time=0.8)

        # range
        rng = RoundedRectangle(corner_radius=0.2, width=2.0, height=0.6, stroke_color=GREEN, stroke_width=3,
                               fill_color=GREEN, fill_opacity=0.12).move_to(sp)
        self.at("range is the")
        self.play(FadeOut(q), Create(rng), run_time=0.6)
        rng_lbl = T("range: where its populations live and reproduce", 24, GREEN).move_to([3.7, 1.5, 0])
        rng_lbl = VGroup(T("range: where its", 24, GREEN), T("populations live", 24, GREEN), T("and reproduce", 24, GREEN)).arrange(DOWN, buff=0.12).move_to([3.7, 1.0, 0])
        self.at("the area where")
        self.play(FadeIn(rng_lbl, shift=LEFT * 0.2), run_time=0.6)

        # temperature falls with height
        ar = Arrow([1.2, -2.6, 0], [1.2, 2.2, 0], color=GREY, stroke_width=4, buff=0)
        cool = T("cooler", 24, BLUE).move_to([2.2, 2.1, 0])
        warm = T("warmer", 24, RED).move_to([2.2, -2.5, 0])
        self.at("Temperature falls as you climb")
        self.play(FadeOut(rng_lbl), GrowArrow(ar), FadeIn(cool), FadeIn(warm), run_time=0.9)

        # warming pushes the isotherm uphill
        warming = T("warming", 28, RED, weight=BOLD).move_to([4.9, -0.2, 0])
        up = Arrow([3.6, -1.2, 0], [3.6, 0.6, 0], color=RED, stroke_width=6, buff=0)
        self.at("So warming moves")
        self.play(FadeOut(VGroup(cool, warm, ar)), FadeIn(warming), GrowArrow(up), run_time=0.6)
        self.at("an isotherm")
        self.play(Indicate(VGroup(line, lab), color=RED), run_time=0.8)
        self.at("a line of equal temperature")
        eq = T("equal temperature all along the line", 24, RED).move_to([3.9, 2.5, 0])
        self.play(FadeIn(eq), run_time=0.5)
        self.at("uphill")
        d = 1.3
        line2 = iso(Y0 + d)
        lab2 = lbl_on("isotherm", Y0 + d, RED)
        self.play(FadeOut(eq), Transform(line, line2), Transform(lab, lab2), run_time=1.3)
        self.at("the edge should follow")
        sp2 = dots(Y0 + d)
        self.play(Transform(sp, sp2), rng.animate.move_to(sp2), sp_lab.animate.move_to(splabel(Y0 + d)), FadeOut(warming), FadeOut(up), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Velocity(SpokenScene):
    def construct(self):
        mt = mountain()
        ghost = DashedLine([sl(Y0) - 0.45, Y0, 0], [sr(Y0) + 0.3, Y0, 0], color=GREY, stroke_width=3, dash_length=0.12)
        ghost_lbl = T("start", 22, GREY).move_to([sr(Y0) + 0.3 + 0.55, Y0 - 0.42, 0])
        line = iso(Y0)
        lab = lbl_on("isotherm", Y0, RED)
        sp = dots(Y0)
        self.add(mt, ghost, ghost_lbl, line, lab, sp)

        head = T("climate velocity", 34, RED, font=TITLE_FONT).move_to([4.0, 3.15, 0])
        self.at("climate velocity")
        self.play(Write(head), run_time=0.9)

        c1 = chip("warming", TEAL, size=26)
        c2 = chip("lapse rate", TEAL, size=26)
        c1.move_to([4.0, 2.2, 0]); c2.move_to([4.0, 2.2, 0])
        self.at("how fast the air warms")
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.5)
        self.at("the lapse rate")
        self.play(c1.animate.move_to([4.0, 2.2, 0]), FadeIn(c2.move_to([4.0, 1.4, 0]), shift=DOWN * 0.2), run_time=0.5)
        note = T("how fast temperature falls with height", 24, GREY).move_to([4.0, 0.75, 0])
        self.at("how fast temperature falls with height")
        self.play(FadeIn(note), run_time=0.5)

        v1 = M("0.3 °C per decade", 26, TEAL).move_to([4.0, 2.2, 0])
        v2 = M("0.6 °C per 100 m", 26, TEAL).move_to([4.0, 1.4, 0])
        self.at("Suppose a mountainside warms")
        self.play(ReplacementTransform(c1, v1), FadeOut(note), run_time=0.6)
        self.at("Suppose temperature falls")
        self.play(ReplacementTransform(c2, v2), run_time=0.6)
        inv = T("invented round figures", 24, YELLOW).move_to([4.0, 0.6, 0])
        self.at("invented round figures")
        self.play(FadeIn(inv, scale=0.9), run_time=0.5)

        calc = M("0.3 ÷ 0.6 × 100 m", 30, TEAL).move_to([4.0, -0.4, 0])
        self.at("Divide the first")
        self.play(FadeOut(inv), FadeIn(calc, shift=UP * 0.2), run_time=0.7)
        res = M("= 50 m per decade", 32, RED, weight=BOLD).move_to([4.0, -1.3, 0])
        self.at("The isotherm climbs")
        line2, lab2 = iso(Y0 + 1.0), lbl_on("isotherm", Y0 + 1.0, RED)
        br = bracket(0.75, Y0, Y0 + 1.0, RED)
        self.play(Transform(line, line2), Transform(lab, lab2), FadeIn(res, shift=UP * 0.2), run_time=1.2)
        self.play(Create(br), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Species(SpokenScene):
    def construct(self):
        mt = mountain()
        ghost = DashedLine([sl(Y0) - 0.45, Y0, 0], [sr(Y0) + 0.3, Y0, 0], color=GREY, stroke_width=3, dash_length=0.12)
        ghost_lbl = T("start", 22, GREY).move_to([sr(Y0) + 0.3 + 0.55, Y0 - 0.42, 0])
        line = iso(Y0 + 1.0)
        lab = lbl_on("isotherm", Y0 + 1.0, RED)
        sp = dots(Y0)
        sp_lab = splabel(Y0)
        self.add(mt, ghost, ghost_lbl, line, lab, sp)

        self.at("Now add a species")
        self.play(FadeIn(sp_lab), Indicate(sp, color=GREEN), run_time=0.8)

        t1 = T("species, per decade", 26, GREEN).move_to([4.0, 2.6, 0])
        v = M("11 m", 40, GREEN, weight=BOLD).move_to([4.0, 1.9, 0])
        src = T("median, 2011 synthesis,", 22, GREY).move_to([4.0, 1.25, 0])
        src2 = T("terrestrial species", 22, GREY).move_to([4.0, 0.85, 0])
        self.at("the median")
        self.play(FadeIn(t1), run_time=0.4)
        self.at("meters per decade")
        d = 11 * U  # 0.22
        sp2 = dots(Y0 + d)
        self.play(FadeIn(v, scale=0.8), FadeIn(src), FadeIn(src2), Transform(sp, sp2), sp_lab.animate.move_to(splabel(Y0 + d)), run_time=1.2)

        # bars
        self.at("divided by")
        barL = 0.07
        bi = Rectangle(width=50 * barL, height=0.45, stroke_width=0, fill_color=RED, fill_opacity=0.9)
        bs = Rectangle(width=11 * barL, height=0.45, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
        bi.move_to([2.0 + 50 * barL / 2, -0.35, 0]); bs.move_to([2.0 + 11 * barL / 2, -1.15, 0])
        li = M("50 m", 24, RED).next_to(bi, RIGHT, buff=0.15)
        ls = M("11 m", 24, GREEN).next_to(bs, RIGHT, buff=0.15)
        li.move_to([2.0 + 50 * barL + 0.55, -0.35, 0]); ls.move_to([2.0 + 11 * barL + 0.55, -1.15, 0])
        tl = T("isotherm", 22, RED).move_to([2.75, 0.05, 0])
        ts = T("species", 22, GREEN).move_to([2.6, -0.75, 0])
        self.play(FadeOut(VGroup(src, src2, t1)), v.animate.move_to([4.0, 2.4, 0]), run_time=0.4)
        self.play(GrowFromEdge(bi, LEFT), FadeIn(li), FadeIn(tl), run_time=0.6)
        self.play(GrowFromEdge(bs, LEFT), FadeIn(ls), FadeIn(ts), run_time=0.6)
        calc = M("11 ÷ 50 = 0.22", 30, TEAL).move_to([4.0, -2.0, 0])
        self.at("so the species")
        self.play(FadeIn(calc, shift=UP * 0.2), run_time=0.6)
        pct = M("22%", 56, YELLOW, weight=BOLD).move_to([4.0, -3.0, 0])
        self.at("covers")
        self.play(FadeIn(pct, scale=0.7), bs.animate.set_fill(YELLOW, 1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Lag(SpokenScene):
    def construct(self):
        mt = mountain()
        ghost = DashedLine([sl(Y0) - 0.45, Y0, 0], [sr(Y0) + 0.3, Y0, 0], color=GREY, stroke_width=3, dash_length=0.12)
        ghost_lbl = T("start", 22, GREY).move_to([sr(Y0) + 0.3 + 0.55, Y0 - 0.42, 0])
        line = iso(Y0 + 1.0)
        lab = lbl_on("isotherm", Y0 + 1.0, RED)
        sp = dots(Y0 + 0.22)
        sp_lab = splabel(Y0 + 0.22)
        self.add(mt, ghost, ghost_lbl, line, lab, sp, sp_lab)

        clock = T("decade 1", 30, GREY).move_to([4.2, 3.1, 0])
        self.at("Run it for")
        self.play(FadeIn(clock), run_time=0.3)
        # decades 2 and 3
        n = clock
        for k, ph in ((2, "30 years"), (3, "three decades")):
            self.at(ph)
            nxt = T(f"decade {k}", 30, GREY).move_to([4.2, 3.1, 0])
            line2, lab2 = iso(Y0 + k), lbl_on("isotherm", Y0 + k, RED)
            sp2 = dots(Y0 + 0.22 * k)
            self.play(Transform(line, line2), Transform(lab, lab2), Transform(sp, sp2),
                      sp_lab.animate.move_to(splabel(Y0 + 0.22 * k)),
                      ReplacementTransform(n, nxt), run_time=0.8)
            n = nxt
        self.play(n.animate.set_color(YELLOW), run_time=0.3)

        r1 = M("3 × 50 = 150 m", 30, RED).move_to([4.2, 2.1, 0])
        self.at("The isotherm climbs")
        b150 = bracket(0.75, Y0, Y0 + 3, RED)
        l150 = M("150 m", 22, RED).move_to([0.75, Y0 + 3 + 0.35, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), Create(b150), FadeIn(l150), run_time=0.8)
        r2 = M("3 × 11 = 33 m", 30, GREEN).move_to([4.2, 1.2, 0])
        self.at("The species climbs")
        self.play(FadeIn(r2, shift=UP * 0.15), Indicate(sp, color=GREEN), run_time=0.8)

        ys, yi = Y0 + 0.22 * 3, Y0 + 3
        bx = -3.0
        gap = bracket(bx, ys, yi, YELLOW)
        gl = M("117 m", 30, YELLOW, weight=BOLD).move_to([bx - 0.75, (ys + yi) / 2, 0])
        gb = Rectangle(width=gl.width + 0.2, height=gl.height + 0.15, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(gl)
        self.at("It ends up")
        self.play(Create(gap), run_time=0.7)
        self.at("below the elevation")
        self.play(FadeIn(gb), FadeIn(gl), run_time=0.5)
        lagt = T("the lag", 30, YELLOW).move_to([4.2, -0.1, 0])
        lagt2 = T("species below the line", 24, GREY).move_to([4.2, -0.7, 0])
        self.at("that now has its former temperature")
        self.play(FadeIn(lagt), FadeIn(lagt2), Indicate(line, color=RED), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Assumptions(SpokenScene):
    def construct(self):
        mt = mountain()
        yi = Y0 + 3
        ys = Y0 + 0.66
        line = iso(yi)
        lab = lbl_on("isotherm", yi, RED)
        sp = dots(ys)
        sp_lab = splabel(ys)
        self.add(mt, line, lab, sp, sp_lab)
        gap = bracket(-3.0, ys, yi, YELLOW)
        gl = M("117 m", 30, YELLOW, weight=BOLD).move_to([-3.75, (ys + yi) / 2, 0])
        gb = Rectangle(width=gl.width + 0.2, height=gl.height + 0.15, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(gl)
        self.add(gap, gb, gl)

        def row(text, y, color=TEAL):
            return chip(text, color, size=22).move_to([4.0, y, 0])

        a2 = row("temperature alone sets the range", 1.4)
        a3 = row("nothing blocks the species", 0.6)
        hdr = T("assumptions", 28, GREY).move_to([4.0, 3.7, 0])
        a1 = chip("warming: constant", TEAL, size=22).move_to([4.0, 3.0, 0])
        a1b = chip("lapse rate: constant", TEAL, size=22).move_to([4.0, 2.2, 0])
        self.at("holds only under assumptions")
        self.play(FadeIn(hdr), FadeOut(VGroup(gap, gb, gl)), run_time=0.4)
        self.at("Warming")
        self.play(FadeIn(a1, shift=LEFT * 0.2), FadeIn(a1b, shift=LEFT * 0.2), run_time=0.6)
        self.at("Temperature alone")
        self.play(FadeIn(a2, shift=LEFT * 0.2), run_time=0.5)
        self.at("Nothing blocks the species")
        self.play(FadeIn(a3, shift=LEFT * 0.2), run_time=0.5)
        # barrier across the slope in front of the species
        by = ys + 0.55
        bar = Line([sl(by) + 0.1, by, 0], [sl(by) + 2.3, by, 0], color=ORANGE, stroke_width=9)
        bar_lbl = VGroup(T("road, farm", 22, ORANGE), T("or cliff", 22, ORANGE)).arrange(DOWN, buff=0.08).move_to([sl(by) + 1.4, by + 0.5, 0])
        self.at("such as a road")
        self.play(Create(bar), FadeIn(bar_lbl), run_time=0.8)
        self.play(Wiggle(sp, scale_value=1.1), run_time=0.5)

        # causes of lag
        causes = [("slow dispersal", ORANGE), ("cues other than temperature", ORANGE),
                  ("competitors already upslope", ORANGE), ("loss of forest", ORANGE)]
        cs = VGroup(*[chip(t, c, size=22) for t, c in causes]).arrange(DOWN, buff=0.25).move_to([4.0, 1.0, 0])
        hdr2 = T("possible reasons for a lag", 26, GREY).move_to([4.0, 3.3, 0])
        self.at("A real lag could reflect")
        self.play(FadeOut(VGroup(hdr, a1, a1b, a2, a3, bar, bar_lbl)), FadeIn(hdr2), run_time=0.5)
        self.at("slow dispersal")
        self.play(FadeIn(cs[0], shift=LEFT * 0.2), run_time=0.4)
        self.at("cues other than temperature")
        self.play(FadeIn(cs[1], shift=LEFT * 0.2), run_time=0.4)
        self.at("competitors already upslope")
        self.play(FadeIn(cs[2], shift=LEFT * 0.2), run_time=0.4)
        self.at("loss of forest")
        self.play(FadeIn(cs[3], shift=LEFT * 0.2), run_time=0.4)

        # variation: many species at different heights relative to the line
        self.at("the median hides wide variation")
        ds = VGroup(*[Dot([sl(yy) + 0.7, yy, 0], radius=0.14, color=GREEN) for yy in [yi - 2.3, yi - 1.5, yi - 0.7, yi]])
        ahead = Dot([sl(yi + 0.7) + 0.7, yi + 0.7, 0], radius=0.14, color=GREEN)
        self.play(FadeOut(VGroup(sp, sp_lab)), FadeOut(VGroup(cs, hdr2)), FadeIn(ds, lag_ratio=0.15), FadeIn(ahead), run_time=1.0)
        al = T("far ahead of the line", 24, GREEN).move_to([4.0, yi + 0.9, 0])
        l1 = Line([al.get_left()[0] - 0.1, al.get_center()[1], 0], ahead.get_center() + RIGHT * 0.18, color=GREEN, stroke_width=2)
        self.at("far ahead of the isotherm")
        self.play(FadeIn(al), Create(l1), Indicate(ahead, color=GREEN, scale_factor=1.6), run_time=0.7)
        bl = T("far behind the line", 24, GREEN).move_to([4.0, -1.3, 0])
        l2 = Line([bl.get_left()[0] - 0.1, bl.get_center()[1], 0], ds[0].get_center() + RIGHT * 0.18, color=GREEN, stroke_width=2)
        self.at("or far behind it")
        self.play(FadeIn(bl), Create(l2), Indicate(ds[0], color=GREEN, scale_factor=1.6), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Detection(SpokenScene):
    def construct(self):
        mt = mountain()
        yi = Y0 + 3
        self.add(mt)
        sp = dots(Y0)
        lab = splabel(Y0)
        self.at("Say a range moves uphill")
        self.play(FadeIn(sp), FadeIn(lab), run_time=0.5)
        d = 1.8
        sp2 = dots(Y0 + d)
        self.play(Transform(sp, sp2), lab.animate.move_to(splabel(Y0 + d)), run_time=1.3)

        det = VGroup(T("Detection", 30, GREEN, weight=BOLD), T("change beyond chance", 24, TEXT)).arrange(DOWN, buff=0.12)
        detb = RoundedRectangle(corner_radius=0.15, width=4.6, height=det.height + 0.4, stroke_color=GREEN, stroke_width=3)
        detg = VGroup(detb, det.move_to(detb)).move_to([4.1, 2.8, 0])
        self.at("That shows a change happened")
        self.play(FadeIn(detg, shift=LEFT * 0.2), run_time=0.7)

        q = T("cause?", 36, YELLOW, weight=BOLD).move_to([4.1, 1.3, 0])
        self.at("It does not show the cause")
        self.play(FadeIn(q, scale=0.7), run_time=0.5)

        # two drivers pushing
        w = chip("warming", RED, size=24).move_to([1.6, -0.2, 0])
        f = chip("forest loss", ORANGE, size=24).move_to([1.6, -1.4, 0])
        aw = Arrow(w.get_left(), [sl(Y0 + d) + 1.4, Y0 + d + 0.1, 0], color=RED, stroke_width=4, buff=0.1)
        af = Arrow(f.get_left(), [sl(Y0 + d) + 1.3, Y0 + d - 0.1, 0], color=ORANGE, stroke_width=4, buff=0.1)
        self.at("forest loss in warmer regions")
        self.play(FadeOut(q), FadeIn(f), GrowArrow(af), run_time=0.8)
        self.at("tended to accelerate")
        self.play(Indicate(sp, color=ORANGE, scale_factor=1.3), run_time=0.7)
        self.at("not proof that climate acted alone")
        self.play(FadeIn(w), GrowArrow(aw), run_time=0.8)
        tag = T("average shifts at 43 sites", 24, GREY).move_to([3.9, -2.4, 0])
        self.play(FadeIn(tag), run_time=0.3)

        att = VGroup(T("Attribution", 30, YELLOW, weight=BOLD), T("a cause, alternatives tested", 24, TEXT)).arrange(DOWN, buff=0.12)
        attb = RoundedRectangle(corner_radius=0.15, width=4.6, height=att.height + 0.4, stroke_color=YELLOW, stroke_width=3)
        attg = VGroup(attb, att.move_to(attb)).move_to([4.1, 1.3, 0])
        self.at("Attribution links a change")
        self.play(FadeOut(tag), FadeIn(attg, shift=LEFT * 0.2), run_time=0.7)
        self.at("tests the alternatives")
        self.play(Indicate(VGroup(w, f), color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Test the alternatives before you name the cause."
