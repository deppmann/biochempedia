"""Cell-free extracts and reconstitution: taking the cell apart, then rebuilding it  (methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = apparatus (tubes, column, press, mortar), cells and boxes of unknown parts, quiet text
  BLUE   = the soluble part: supernatant, cytosol, Fraction 1, the juice
  ORANGE = the particulate part: membrane fragments, the pellet, Golgi membranes, Fraction 2
  PURPLE = the one part under test, or a purified part (the protein you remove and add back,
           cytochrome c, NSF, APF-1, cyclin messenger RNA, the rebuild's purified proteins)
  GREEN  = activity present (the gauge fill, bubbles, restored, runs)
  RED    = activity absent, the pitfall, the inactivator
  YELLOW = highlight, and what you add to start a reaction (hormone, poly-U, ATP, dNTPs, high salt)
  GOLD   = dates, source tags and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.1, align=ORIGIN, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def tube_outline(cx, ytop, ybot, w, color=GREY, sw=3.5):
    return poly([[cx - w / 2, ytop], [cx - w / 2, ybot + 0.15], [cx - w / 2 + 0.15, ybot],
                 [cx + w / 2 - 0.15, ybot], [cx + w / 2, ybot + 0.15], [cx + w / 2, ytop]], color, sw)


def layer(cx, ybot, ytop, w, frac0, frac1, color, op=0.45):
    """A band of liquid inside a tube; frac0..frac1 measured up from the tube bottom."""
    h = ytop - ybot
    y0, y1 = ybot + 0.06 + frac0 * (h - 0.06), ybot + 0.06 + frac1 * (h - 0.06)
    return Rectangle(width=w - 0.12, height=max(y1 - y0, 0.001), stroke_width=0, fill_color=color,
                     fill_opacity=op if y1 > y0 else 0).move_to([cx, (y0 + y1) / 2, 0])


def make_tube(cx, ytop, ybot, w, layers=()):
    """VGroup(outline, *layers). layers = [(frac0, frac1, color), ...]. Keeps its geometry as attributes."""
    parts = [layer(cx, ybot, ytop, w, a, b, c) for a, b, c in layers]
    g = VGroup(tube_outline(cx, ytop, ybot, w), *parts)
    g.cx, g.ytop, g.ybot, g.w = cx, ytop, ybot, w
    return g


def dots_in(cx, ybot, ytop, w, n, color, r=0.07, seed=0, f0=0.1, f1=0.75, op=0.9):
    rng = np.random.RandomState(seed)
    h = ytop - ybot
    out = VGroup()
    for _ in range(n):
        x = cx + (rng.rand() - 0.5) * (w - 0.35)
        y = ybot + 0.2 + (f0 + rng.rand() * (f1 - f0)) * (h - 0.3)
        out.add(Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, y, 0]))
    return out


class Gauge(VGroup):
    """The activity read-out: a tall frame filled from the bottom. .to(level, color) animates it."""

    def __init__(self, cx, ybot, h, w=0.42, level=0.0, color=GREEN):
        self.cx, self.ybot, self.h, self.w = cx, ybot, h, w
        self.frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(
            [cx, ybot + h / 2, 0])
        self.fill = self._mk(level, color)
        super().__init__(self.frame, self.fill)

    def _mk(self, level, color):
        hh = max(level * (self.h - 0.1), 0.001)
        r = Rectangle(width=self.w - 0.1, height=hh, stroke_width=0, fill_color=color,
                      fill_opacity=0.9 if level > 0 else 0)
        return r.move_to([self.cx, self.ybot + 0.05 + hh / 2, 0])

    def to(self, level, color=GREEN, run_time=0.6):
        return Transform(self.fill, self._mk(level, color), run_time=run_time)


def date_tag(text, y=-3.2, size=26):
    return T(text, size, GOLD).move_to([0, y, 0])


def yeast(x, y, r=0.2, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.22).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Taking the Cell Apart, Then Rebuilding It"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a cell of unknown parts; fermentation tied to it; too small to break; inseparable; needed? enough?"""

    def construct(self):
        cc = np.array([-2.3, -0.2, 0.0])
        cell = Ellipse(width=7.8, height=5.8, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                       fill_opacity=0.08).move_to(cc)
        spots = [(-2.4, 1.3), (0.0, 1.55), (2.3, 1.2), (-2.2, -0.9), (0.1, -0.35), (2.2, -1.2)]
        boxes = VGroup()
        for dx, dy in spots:
            b = RoundedRectangle(corner_radius=0.14, width=1.0, height=1.0, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.16).move_to(cc + [dx, dy, 0])
            q = T("?", 38, TEXT, weight=BOLD).move_to(b)
            boxes.add(VGroup(b, q))
        cell_lbl = lab("living yeast", 24, GREY).move_to(cc + [0, -2.3, 0])

        self.at("Can a process")
        self.play(FadeIn(cell), LaggedStart(*[GrowFromCenter(b) for b in boxes], lag_ratio=0.12), FadeIn(cell_lbl),
                  run_time=1.2)

        self.at("many held that")
        date = T("before 1897", 30, GOLD).move_to([4.25, 3.0, 0])
        self.play(FadeIn(date, shift=DOWN * 0.1), run_time=0.4)

        self.at("fermentation was tied")
        ferm = chip("fermentation", GREEN, 28).move_to([4.25, 1.8, 0])
        tether = DashedLine(ferm.get_left() + [-0.05, 0, 0], cc + [3.55, 1.1, 0], color=GREY, stroke_width=3)
        tie = lab("tied to living yeast", 22, GREY).move_to([4.25, 1.05, 0])
        self.play(FadeIn(ferm, shift=LEFT * 0.2), Create(tether), run_time=0.5)
        self.play(FadeIn(tie), run_time=0.3)

        self.at("too small")
        cross = T("✕", 46, RED, weight=BOLD).move_to(cc + [3.9, -0.4, 0])
        small = lines("too small to", "break open", size=24, color=RED).move_to([4.5, -0.8, 0])
        self.play(FadeIn(cross, scale=1.4), FadeIn(small), run_time=0.5)

        self.at("Vitalists")
        insep = lines("inseparable from", "the intact cell", size=24, color=YELLOW).move_to([4.25, -2.3, 0])
        self.play(cell.animate.set_stroke(YELLOW, 9), FadeIn(insep), run_time=0.6)

        self.at("many parts")
        self.play(LaggedStart(*[Indicate(b, color=YELLOW, scale_factor=1.18) for b in boxes], lag_ratio=0.22),
                  run_time=1.1)

        self.at("Which does a process")
        right = VGroup(date, ferm, tether, tie, cross, small, insep)
        need = T("needed?", 46, YELLOW, weight=BOLD).move_to([4.25, 1.3, 0])
        self.play(FadeOut(right), cell.animate.set_stroke(GREY, 4), run_time=0.5)
        self.play(FadeIn(need, shift=LEFT * 0.2), run_time=0.4)
        self.at("which are enough")
        enough = T("enough?", 46, YELLOW, weight=BOLD).move_to([4.25, -0.3, 0])
        self.play(FadeIn(enough, shift=LEFT * 0.2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Break(SpokenScene):
    """grind in a mortar, press in canvas, juice drips into a tube; the tube ferments; read the gauge."""

    def construct(self):
        bx = -4.5
        bowl = Polygon([bx - 1.2, 1.3, 0], [bx + 1.2, 1.3, 0], [bx + 0.85, 0.2, 0], [bx - 0.85, 0.2, 0],
                       stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.22)
        cell_pos = [(-0.62, 0.5), (-0.22, 0.5), (0.22, 0.5), (0.62, 0.5), (-0.42, 0.92), (0.0, 0.92), (0.42, 0.92)]
        cells = VGroup(*[yeast(bx + dx, dy, 0.17) for dx, dy in cell_pos])
        bowl_lbl = lines("mortar", "brewer's yeast", size=22, color=GREY).move_to([bx, -0.45, 0])

        self.at("broke the cells")
        self.play(FadeIn(bowl), LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.1), FadeIn(bowl_lbl),
                  run_time=1.0)

        self.at("quartz sand")
        sand = VGroup(*[Circle(radius=0.035, stroke_width=0, fill_color=TEXT, fill_opacity=0.8).move_to(
            [bx + dx, dy, 0]) for dx, dy in [(-0.8, 0.35), (-0.3, 0.7), (0.1, 0.35), (0.5, 0.75), (0.8, 0.35),
                                              (-0.55, 1.1), (0.25, 1.1), (0.7, 1.12), (-0.1, 0.55), (-0.7, 0.8)]])
        sand_lbl = lab("quartz sand and diatomite", 22, TEXT).move_to([bx, 3.2, 0])
        pestle = Rectangle(width=0.32, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                           fill_opacity=0.6).move_to([bx, 2.0, 0])
        self.play(FadeIn(sand), FadeIn(sand_lbl), FadeIn(pestle), run_time=0.5)
        self.play(pestle.animate.shift(DOWN * 0.45), run_time=0.25)
        self.play(pestle.animate.shift(UP * 0.35), run_time=0.2)
        self.play(pestle.animate.shift(DOWN * 0.35), run_time=0.2)
        frag = VGroup()
        for dx, dy in cell_pos:
            frag.add(Circle(radius=0.05, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([bx + dx - 0.06, dy, 0]))
            frag.add(Circle(radius=0.05, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([bx + dx + 0.07, dy + 0.07, 0]))
            frag.add(Rectangle(width=0.14, height=0.05, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to(
                [bx + dx, dy - 0.08, 0]))
        self.play(ReplacementTransform(cells, frag), pestle.animate.shift(UP * 0.2), run_time=0.5)

        # --- the press
        px = -0.7
        self.at("squeezed it")
        low = Rectangle(width=2.4, height=0.22, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([px, -0.5, 0])
        bag = RoundedRectangle(corner_radius=0.18, width=1.9, height=0.6, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.18).move_to([px, -0.05, 0])
        bag_lbl = lab("canvas", 22, TEXT).move_to([px + 1.75, -0.05, 0])
        up = Rectangle(width=2.4, height=0.22, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([px, 1.5, 0])
        rod = Line([px, 1.61, 0], [px, 2.6, 0], color=GREY, stroke_width=6)
        bag_dots = VGroup(*[Circle(radius=0.05, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to(
            [px + dx, -0.2 + dy, 0]) for dx, dy in [(-0.6, 0.05), (-0.2, 0.1), (0.3, 0.05), (0.65, 0.1), (0.05, -0.05)]])
        self.play(FadeOut(pestle), FadeOut(sand_lbl), FadeIn(low), FadeIn(bag), FadeIn(bag_lbl), FadeIn(up), FadeIn(rod),
                  ReplacementTransform(frag, bag_dots), run_time=0.5)
        press_lbl = lab("hydraulic press", 22, GREY).move_to([px, 3.0, 0])
        tcx, tt, tb, tw = px, -1.1, -3.3, 0.9
        tube0 = make_tube(tcx, tt, tb, tw)
        drips = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([px + dx, -0.7, 0])
                         for dx in (-0.3, 0.0, 0.3)])
        self.play(FadeIn(tube0), FadeIn(press_lbl), up.animate.shift(DOWN * 1.1), rod.animate.shift(DOWN * 1.1),
                  bag.animate.stretch_to_fit_height(0.3).shift(DOWN * 0.15), bag_lbl.animate.shift(DOWN * 0.15), run_time=0.6)
        liq = layer(tcx, tb, tt, tw, 0, 0.5, BLUE)
        self.play(FadeIn(drips, shift=DOWN * 0.1), run_time=0.2)
        self.play(drips.animate.shift(DOWN * 1.7), FadeIn(liq), run_time=0.5)
        self.play(FadeOut(drips), run_time=0.1)

        self.at("A thousand grams")
        g1 = lab("1000 g of yeast", 24, GREY).move_to([bx, -1.4, 0])
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.4)
        self.at("of juice")
        g2 = lines("about 500 cc", "of juice", size=24, color=BLUE).move_to([1.6, -2.3, 0])
        self.play(FadeIn(g2, shift=LEFT * 0.1), run_time=0.4)

        # --- the juice, enlarged
        self.at("That juice fermented")
        stage_old = VGroup(bowl, bowl_lbl, sand, bag_dots, low, bag, bag_lbl, up, rod, press_lbl, g1, g2, tube0, liq)
        TX = -3.4
        big = make_tube(TX, 3.0, -1.6, 1.8, [(0, 0.78, BLUE)])
        self.play(FadeOut(stage_old), FadeIn(big), run_time=0.5)
        sugar = chip("sugar", YELLOW, 26).move_to([TX, 3.6 - 0.15, 0]).shift(UP * 0.05)
        sugar.move_to([TX, 3.35, 0])
        self.play(FadeIn(sugar), run_time=0.3)
        self.play(sugar.animate.move_to([TX, 1.9, 0]).scale(0.6), run_time=0.3)
        bubbles = VGroup(*[Circle(radius=0.09, stroke_color=GREEN, stroke_width=2.5, fill_opacity=0).move_to(
            [TX + dx, -1.0 + dy, 0]) for dx, dy in [(-0.45, 0.0), (0.1, 0.35), (0.45, 0.1), (-0.15, 0.7), (0.3, 0.95), (-0.5, 1.1)]])
        self.play(FadeOut(sugar), FadeIn(bubbles), run_time=0.3)
        self.play(bubbles.animate.shift(UP * 1.5), run_time=0.6, rate_func=linear)
        self.at("no living cells")
        nl = lab("no living cells", 26, TEXT).move_to([TX, -2.2, 0])
        self.play(FadeIn(nl), run_time=0.3)

        self.at("show the activity")
        gg = Gauge(-0.7, -1.6, 4.6, level=0.0)
        glab = lab("activity", 24, GREEN).move_to([-0.7, 3.25, 0])
        crude = lab("in the crude extract", 26, GREY).move_to([3.3, 2.4, 0])
        self.play(FadeIn(gg), FadeIn(glab), FadeIn(crude), run_time=0.4)
        self.play(gg.to(0.8, GREEN, 0.7))
        self.at("give it a number")
        num = chip("a number", YELLOW, 38).move_to([3.3, 0.6, 0])
        na = arr([-0.35, 1.9, 0], [num.get_left()[0] - 0.1, 0.8, 0], YELLOW, 4, 0.18)
        self.play(GrowArrow(na), FadeIn(num, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def unit(x0, ytop=1.6, ybot=-0.8, layers=(), gauge_level=None, gauge_color=GREEN, gauge_dx=1.15, w=1.1):
    """A test tube with its gauge beside it. Returns (tube group, gauge)."""
    tube = make_tube(x0, ytop, ybot, w, layers)
    gg = Gauge(x0 + gauge_dx, ybot, ytop - ybot, level=gauge_level or 0.0, color=gauge_color)
    return tube, gg


class S03Split(SpokenScene):
    """spin: pellet and supernatant, test alone and recombined; column: Fraction 1 and 2, dead alone, alive together."""

    def construct(self):
        # ---------------- the crude extract
        tx = -3.9
        tube = make_tube(0, 2.2, -1.4, 1.8, [(0, 0.8, BLUE)])
        rng_dots = dots_in(0, -1.4, 2.2, 1.8, 11, ORANGE, r=0.08, seed=3, f0=0.05, f1=0.75)
        crude_lbl = lab("crude extract", 26, GREY).move_to([0, -1.95, 0])
        self.at("Next, split")
        self.play(FadeIn(tube), FadeIn(rng_dots), FadeIn(crude_lbl), run_time=0.8)
        gone = VGroup(tube, rng_dots, crude_lbl)

        # ---------------- part B: the column
        self.at("A column can")
        col = Rectangle(width=1.7, height=3.1, stroke_color=GREY, stroke_width=3.5, fill_color=GREY, fill_opacity=0.08).move_to([0, 1.1, 0])
        beads = VGroup(*[Circle(radius=0.06, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to(
            [-0.7 + 1.4 * ((i * 0.37) % 1.0), 0.0 + 2.2 * ((i * 0.23 + 0.1) % 1.0), 0]) for i in range(26)])
        col_lbl = lines("DEAE-cellulose", "column", size=22, color=GREY).move_to([3.3, 1.1, 0])
        self.play(FadeOut(gone), FadeIn(col), FadeIn(beads), FadeIn(col_lbl), run_time=0.7)
        self.at("In a lysate")
        lys = chip("lysate of reticulocytes", GREY, 22).move_to([0, 3.15, 0])
        rng = np.random.RandomState(8)
        bd = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=BLUE, fill_opacity=0.95).move_to(
            [-0.55 + 0.22 * i, 2.35 + 0.03 * (i % 2), 0]) for i in range(6)])
        od = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to(
            [-0.45 + 0.22 * i, 2.05 + 0.03 * (i % 2), 0]) for i in range(5)])
        self.play(FadeIn(lys), FadeIn(bd), FadeIn(od), run_time=0.6)
        f1 = make_tube(-2.6, -0.8, -2.8, 1.1)
        f2 = make_tube(2.6, -0.8, -2.8, 1.1)
        v1 = poly([[0, -0.45], [0, -0.6], [-2.6, -0.65], [-2.6, -0.8]], GREY, 3)
        v2 = poly([[0, -0.45], [0, -0.6], [2.6, -0.65], [2.6, -0.8]], GREY, 3)
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(v1), FadeIn(v2), run_time=0.4)
        self.at("does not bind")
        tgt1 = [[-2.9 + 0.2 * (i % 3), -2.55 + 0.2 * (i // 3), 0] for i in range(6)]
        self.play(*[d.animate.move_to([0.0, -0.4, 0]) for d in bd], od.animate.shift(DOWN * 0.8), run_time=0.7)
        self.play(*[d.animate.move_to(p) for d, p in zip(bd, tgt1)], run_time=0.8)
        l1 = lines("Fraction 1", size=26, color=BLUE).move_to([-2.6, -3.15, 0])
        self.at("Fraction 1")
        self.play(FadeIn(l1), run_time=0.3)
        self.at("washed off with")
        salt = chip("high salt", YELLOW, 24).move_to([0, 3.15, 0])
        self.play(Transform(lys, salt), run_time=0.4)
        tgt2 = [[2.3 + 0.2 * (i % 3), -2.55 + 0.2 * (i // 3), 0] for i in range(5)]
        self.play(*[d.animate.move_to([0.0, -0.4, 0]) for d in od], run_time=0.7)
        self.play(*[d.animate.move_to(p) for d, p in zip(od, tgt2)], run_time=0.8)
        l2 = lines("Fraction 2", size=26, color=ORANGE).move_to([2.6, -3.15, 0])
        self.at("Fraction 2")
        self.play(FadeIn(l2), run_time=0.3)

        # ---------------- the test
        self.at("Neither supports")
        xa, xb, xc = -4.2, -0.4, 3.4
        ytop, ybot = 2.7, -0.6
        def big_unit(x0, color, label, lcolor):
            tb = make_tube(x0, ytop, ybot, 1.5, [(0, 0.5, color)])
            dd = dots_in(x0, ybot, ytop, 1.5, 6, color, r=0.09, seed=int(abs(x0) * 7), f0=0.08, f1=0.4, op=0.95)
            return VGroup(tb, dd), lines(*label, size=24, color=lcolor).move_to([x0 + 0.7, ybot - 0.7, 0])
        n1, nl1 = big_unit(xa, BLUE, ("Fraction 1", "alone"), BLUE)
        n2, nl2 = big_unit(xb, ORANGE, ("Fraction 2", "alone"), ORANGE)
        f1g = VGroup(f1, bd, l1)
        f2g = VGroup(f2, od, l2)
        self.play(FadeOut(VGroup(col, beads, col_lbl, lys, v1, v2)),
                  ReplacementTransform(f1g, VGroup(n1, nl1)), ReplacementTransform(f2g, VGroup(n2, nl2)), run_time=1.0)
        ga2 = Gauge(xa + 1.3, ybot, ytop - ybot, level=0.0)
        gb2 = Gauge(xb + 1.3, ybot, ytop - ybot, level=0.0)
        na = T("none", 26, RED).move_to([xa + 1.3, ytop + 0.35, 0])
        nb = T("none", 26, RED).move_to([xb + 1.3, ytop + 0.35, 0])
        act0 = lab("ATP-dependent breakdown", 22, GREEN).move_to([-2.3, 3.65, 0])
        self.play(FadeIn(ga2), FadeIn(gb2), FadeIn(na), FadeIn(nb), FadeIn(act0), run_time=0.5)
        self.at("Combined")
        uc2 = make_tube(xc, ytop, ybot, 1.5, [(0, 0.35, ORANGE), (0.35, 0.7, BLUE)])
        gc2 = Gauge(xc + 1.3, ybot, ytop - ybot, level=0.0)
        cl = lines("Fractions", "1 + 2", size=24, color=TEXT).move_to([xc + 0.7, ybot - 0.7, 0])
        self.play(FadeIn(uc2), FadeIn(gc2), FadeIn(cl), run_time=0.5)
        self.at("restore that activity")
        self.play(gc2.to(0.85, GREEN, 0.8))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Addback(SpokenScene):
    """one tube and gauge: remove / add back; inactivate / rescue; rebuild from purified parts."""

    def construct(self):
        tx, tt, tb, tw = -4.7, 2.8, -1.6, 1.5
        gx = -6.0
        tube = make_tube(tx, tt, tb, tw, [(0, 0.8, BLUE)])
        pdots = dots_in(tx, tb, tt, tw, 5, PURPLE, r=0.1, seed=5, f0=0.15, f1=0.7)
        gg = Gauge(gx, tb, tt - tb, level=0.85)
        glab = lab("activity", 24, GREEN).move_to([gx, 3.25, 0])
        cap = lab("extract", 24, GREY).move_to([tx, -2.15, 0])
        state = lab("", 24, GREEN).move_to([tx, -2.75, 0])

        self.at("Now test one")
        self.play(FadeIn(tube), FadeIn(pdots), FadeIn(gg), FadeIn(glab), FadeIn(cap), run_time=0.8)

        # --- remove with antibody, add back
        self.at("Remove one protein")
        ab = chip("antibody", GREY, 26).move_to([0.2, 1.2, 0])
        aa = arr([-1.1, 1.2, 0], [tx + 0.9, 1.2, 0], GREY, 4, 0.18)
        box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=2.6, height=1.5, stroke_color=PURPLE,
                                              stroke_width=3).move_to([4.0, 0.2, 0]), num_dashes=24)
        blab = lab("removed", 22, PURPLE).move_to([4.0, -0.85, 0])
        self.play(FadeIn(ab, shift=LEFT * 0.2), GrowArrow(aa), FadeIn(box), FadeIn(blab), run_time=0.6)
        self.play(*[d.animate.move_to([3.4 + 0.45 * (i % 3), 0.5 - 0.4 * (i // 3), 0]) for i, d in enumerate(pdots)],
                  run_time=0.8)
        self.at("activity is lost")
        lost = T("activity lost", 26, RED).move_to([tx, -2.75, 0])
        self.play(gg.to(0.0, RED, 0.6), FadeIn(lost), run_time=0.6)
        self.at("Add the pure protein")
        pure = chip("pure protein", PURPLE, 26).move_to([0.8, 2.4, 0])
        pa = arr([-0.6, 2.4, 0], [tx + 0.9, 2.1, 0], PURPLE, 4, 0.18)
        self.play(FadeOut(ab), FadeOut(aa), FadeIn(pure, shift=LEFT * 0.2), GrowArrow(pa),
                  FadeOut(box), FadeOut(blab), run_time=0.5)
        pd2 = dots_in(tx, tb, tt, tw, 5, PURPLE, r=0.1, seed=5, f0=0.15, f1=0.7)
        self.play(FadeOut(pdots), FadeIn(pd2, shift=DOWN * 0.4), run_time=0.5)
        self.at("and it returns")
        back = T("activity returns", 26, GREEN).move_to([tx, -2.75, 0])
        self.play(gg.to(0.85, GREEN, 0.7), ReplacementTransform(lost, back), run_time=0.7)

        # --- rebuild
        self.at("The last test")
        self.play(FadeOut(VGroup(pure, pa, pd2, back)), run_time=0.3)
        stage = Group(*[m for m in self.mobjects if m is not tube and m is not gg and m is not glab])
        empty = make_tube(tx, tt, tb, tw)
        self.play(FadeOut(stage), FadeOut(tube), FadeIn(empty), gg.to(0.0, GREY, 0.4), run_time=0.7)
        cap2 = lab("purified parts only", 24, PURPLE).move_to([tx, -2.15, 0])
        mm = lab("E. coli mismatch repair", 26, GREY).move_to([2.25, 3.2, 0])
        self.play(FadeIn(cap2), FadeIn(mm), run_time=0.4)
        self.at("for E. coli")
        dna = chip("DNA with a mismatch", GREY, 22, pad=0.16)
        names = [["MutH", "MutL", "MutS"], ["helicase II", "SSB"], ["exonuclease I", "ligase"]]
        rows = VGroup(VGroup(dna))
        for r in names:
            rows.add(VGroup(*[chip(n, PURPLE, 22, pad=0.16) for n in r]).arrange(RIGHT, buff=0.22))
        # polymerase III holoenzyme: a cluster of subunits inside a dashed outline (one of the eight proteins)
        lbl = T("DNA polymerase III holoenzyme", 22, PURPLE)
        subs = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=PURPLE, fill_opacity=0.9) for _ in range(4)]).arrange(RIGHT, buff=0.1)
        inner = VGroup(subs, lbl).arrange(RIGHT, buff=0.22)
        holo = VGroup(RoundedRectangle(corner_radius=0.14, width=inner.width + 0.8, height=inner.height + 0.45,
                                          stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE, fill_opacity=0.08).move_to(inner), inner)
        rows.insert(3, VGroup(holo))
        small = VGroup(chip("ATP", YELLOW, 22, pad=0.16), chip("dNTPs", YELLOW, 22, pad=0.16)).arrange(RIGHT, buff=0.22)
        allc = VGroup(*rows, small).arrange(DOWN, buff=0.13).move_to([2.25, 0.0, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for r in rows for c in r], lag_ratio=0.12), run_time=1.6)
        self.at("with ATP")
        self.play(FadeIn(small, shift=LEFT * 0.15), run_time=0.5)
        self.at("If the reaction runs")
        chips = [c for r in rows for c in r] + list(small)
        fill = layer(tx, tb, tt, tw, 0, 0.7, PURPLE, 0.4)
        self.play(*[c.animate.scale(0.2).move_to([tx, 0.5, 0]).set_opacity(0.0) for c in chips], FadeIn(fill), run_time=0.9)
        self.play(gg.to(0.85, GREEN, 0.8))
        self.at("those parts are enough")
        done = lab("those parts are enough", 30, GREEN).move_to([2.25, 0.2, 0])
        self.play(FadeIn(done, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """idealised bars: activity with cytosol + dATP, after immunodepletion, with cytochrome c added back."""

    def construct(self):
        base = -1.9
        xs = [-3.6, 0.4, 4.4]
        H = 3.0
        axis = Line([-5.8, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        yax = Line([-5.8, base, 0], [-5.8, base + H + 0.5, 0], color=GREY, stroke_width=3)
        ylab = lab("activity", 24, GREEN).move_to([-5.0, 2.25, 0])
        note = lines("example:", "idealised bars", size=22, color=YELLOW).move_to([-4.6, 3.1, 0])

        def bar(x, frac, color=GREEN):
            return Rectangle(width=1.5, height=max(frac * H, 0.001), stroke_color=color, stroke_width=3, fill_color=color,
                             fill_opacity=0.55 if frac > 0 else 0).move_to([x, base + frac * H / 2, 0])

        l1 = lines("cytosol of growing", "cells + dATP", size=22, color=TEXT).move_to([xs[0], base - 0.55, 0])
        self.play(Create(axis), Create(yax), FadeIn(ylab), FadeIn(note), FadeIn(l1), run_time=0.5)
        b1 = bar(xs[0], 0.001)
        self.at("of the apoptotic")
        b1t = bar(xs[0], 1.0)
        pr = lab("parts of the program start", 22, GREEN).move_to([xs[0], base + H + 0.3, 0])
        self.play(Transform(b1, b1t), run_time=0.8)
        self.play(FadeIn(pr), run_time=0.3)

        self.at("Fractionation gave")
        chip1 = chip("15 kDa protein", PURPLE, 28).move_to([0.4, 2.6, 0])
        fa = arr([-2.1, 2.45, 0], [chip1.get_left()[0] - 0.1, 2.6, 0], GREY, 4, 0.18)
        fl = lab("fractionate", 22, GREY).move_to([-3.2, 2.5, 0])
        self.play(GrowArrow(fa), FadeIn(fl), FadeIn(chip1, shift=LEFT * 0.2), run_time=0.6)
        self.at("proved to be")
        chip2 = chip("cytochrome c", PURPLE, 28).move_to([0.4, 2.6, 0])
        self.play(Transform(chip1, chip2), run_time=0.6)

        self.at("diminished the activity")
        l2 = lines("immunodepleted", "of cytochrome c", size=22, color=TEXT).move_to([xs[1], base - 0.55, 0])
        b2 = bar(xs[1], 0.001)
        self.play(FadeIn(l2), run_time=0.3)
        self.play(Transform(b2, bar(xs[1], 0.3, GREEN)), run_time=0.7)
        self.at("Adding cytochrome c")
        l3 = lines("cytochrome c", "added back", size=22, color=TEXT).move_to([xs[2], base - 0.55, 0])
        b3 = bar(xs[2], 0.001)
        c3 = chip("cytochrome c", PURPLE, 28).move_to([xs[2], 2.6, 0])
        self.play(FadeIn(l3), TransformFromCopy(chip1, c3), run_time=0.6)
        self.play(Transform(b3, bar(xs[2], 0.97, GREEN)), run_time=0.8)

        self.at("Diminished when removed")
        d = arr([xs[0] + 0.9, base + H - 0.1, 0], [xs[1] - 0.9, base + 1.2, 0], RED, 5, 0.2)
        dl = lab("diminished", 24, RED).move_to([-0.75, base + 2.4, 0])
        self.play(GrowArrow(d), FadeIn(dl), run_time=0.5)
        self.at("restored when added")
        r = arr([xs[1] + 0.9, base + 1.0, 0], [xs[2] - 0.9, base + H - 0.2, 0], GREEN, 5, 0.2)
        rl = lab("restored", 24, GREEN).move_to([2.45, base + 1.2, 0])
        self.play(GrowArrow(r), FadeIn(rl), run_time=0.5)
        self.at("the protein is needed")
        need = T("the protein is needed", 34, GOLD).move_to([-0.6, 3.25, 0])
        self.play(FadeOut(VGroup(fa, fl, chip1)), FadeIn(need, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def panel_unit(x0, y0, h=2.8, layers=(), level=0.0, gcolor=GREEN, w=1.2, gdx=0.95):
    tube = make_tube(x0, y0 + h / 2, y0 - h / 2, w, layers)
    gg = Gauge(x0 + gdx, y0 - h / 2, h, w=0.32, level=level, color=gcolor)
    return tube, gg


class S06Pitfalls(SpokenScene):
    """four Buchner controls on surviving cells; then how preparation changes what an extract holds."""

    def construct(self):
        self.at("Two things")
        head = T("1  could living cells be doing it?", 30, RED).move_to([0, 3.05, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)

        # a few living cells in the juice
        x0, y0 = -3.7, 0.1
        t1, g1 = panel_unit(x0, y0, layers=[(0, 0.8, BLUE)])
        few = VGroup(*[yeast(x0 + dx, y0 - 1.0 + dy, 0.1) for dx, dy in [(-0.2, 0.0), (0.15, 0.25), (-0.05, 0.55)]])
        fl = lines("a few living cells", "in the juice", size=24, color=TEXT).move_to([x0 + 2.9, y0, 0])
        self.at("few living cells")
        self.play(FadeIn(t1), FadeIn(few), FadeIn(fl), run_time=0.6)

        # P1  ten times as many cells
        self.at("ten times")
        cells = VGroup(*[yeast(x0 + dx, y0 - 1.15 + dy, 0.1) for dx, dy in
                         [(-0.3, 0.0), (-0.1, 0.0), (0.1, 0.0), (0.3, 0.0), (-0.2, 0.2), (0.0, 0.2), (0.2, 0.2), (-0.3, 0.4),
                          (-0.1, 0.4), (0.1, 0.4), (0.3, 0.4), (-0.2, 0.6), (0.0, 0.6), (0.2, 0.6), (-0.1, 0.8), (0.1, 0.8),
                          (0.0, 1.0), (-0.3, 0.8), (0.3, 0.8)]])
        c1 = lines("ten times as many", "yeast cells:", "no fermentation", size=24, colors=[TEXT, TEXT, RED]).move_to(
            [x0 + 2.9, y0, 0])
        self.play(Transform(few, cells), FadeIn(g1), ReplacementTransform(fl, c1), run_time=0.7)

        # P4  killed, dried yeast
        self.at("Killed dried yeast")
        x4 = 2.0
        t4, g4 = panel_unit(x4, y0, layers=[(0, 0.35, GREY)])
        xs4 = VGroup(*[T("✕", 24, RED).move_to([x4 + dx, y0 - 1.1 + dy, 0]) for dx, dy in [(-0.25, 0), (0.25, 0), (0, 0.3), (-0.25, 0.6), (0.25, 0.6)]])
        c4 = lines("killed dried yeast", "(zymin):", "still ferments", size=24, colors=[TEXT, TEXT, GREEN]).move_to([x4 + 2.9, y0, 0])
        self.play(FadeIn(t4), FadeIn(xs4), FadeIn(g4), FadeIn(c4), run_time=0.6)
        self.play(g4.to(0.85, GREEN, 0.6))

        # ------------- pitfall 2
        self.at("Second")
        grid = VGroup(head, t1, few, g1, c1, t4, xs4, g4, c4)
        head2 = T("2  how the extract is made changes what it holds", 30, YELLOW).move_to([0, 3.05, 0])
        self.play(FadeOut(grid), run_time=0.4)
        self.play(FadeIn(head2), run_time=0.4)
        xL, xR = -3.4, 3.0
        tt_, tb_ = 2.0, -1.5
        tl = make_tube(xL, tt_, tb_, 2.0, [(0, 0.8, BLUE)])
        dl = dots_in(xL, tb_, tt_, 2.0, 7, PURPLE, r=0.1, seed=2, f0=0.15, f1=0.75)
        gl = Gauge(xL + 1.45, tb_, tt_ - tb_, level=0.0)
        cl = lines("cytosol:", "cytochrome c free", size=22, color=TEXT).move_to([xL, -2.25, 0])
        self.at("how you prepare")
        self.play(FadeIn(tl), FadeIn(dl), FadeIn(gl), FadeIn(cl), run_time=0.6)
        self.play(gl.to(0.85, GREEN, 0.6))
        self.at("sucrose added")
        tr = make_tube(xR, tt_, tb_, 2.0, [(0, 0.8, BLUE)])
        mito = VGroup()
        for i, (dx, dy) in enumerate([(-0.45, 0.2), (0.35, 0.65), (-0.1, -0.5), (0.45, -0.1)]):
            e = Ellipse(width=0.62, height=0.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to(
                [xR + dx, 0.0 + dy, 0])
            p = Circle(radius=0.07, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95).move_to(e.get_center())
            mito.add(VGroup(e, p))
        gr = Gauge(xR + 1.45, tb_, tt_ - tb_, level=0.85)
        cr = lines("with sucrose, to keep", "mitochondria intact", size=22, color=TEXT).move_to([xR, -2.25, 0])
        ml = lab("mitochondria", 22, GREY).move_to([xR - 2.3, 1.0, 0])
        self.play(FadeIn(tr), FadeIn(mito), FadeIn(gr), FadeIn(cr), run_time=0.7)
        self.at("diminished the apoptotic")
        dim = T("diminished", 26, RED).move_to([xR + 1.45, tt_ + 0.45, 0])
        self.play(gr.to(0.3, GREEN, 0.7), FadeIn(dim), run_time=0.7)
        self.at("Intact mitochondria likely")
        cc = chip("cytochrome c", PURPLE, 26).move_to([0.0, 3.05 - 0.0, 0])
        cc.move_to([0, 2.45, 0])
        note = lab("likely: stays inside mitochondria", 24, PURPLE).move_to([xR, -3.15, 0])
        self.play(*[Indicate(m[1], color=YELLOW, scale_factor=1.9) for m in mito],
                  *[Indicate(d, color=YELLOW, scale_factor=1.7) for d in dl], FadeIn(note), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07UnlockedA(SpokenScene):
    """Sutherland and Rall (1950s); Nirenberg and Matthaei (1961)."""

    def construct(self):
        tag = date_tag("Sutherland, Rall, 1950s")
        TX = -3.4
        tube = make_tube(TX, 2.2, -1.4, 1.8, [(0, 0.8, BLUE), (0, 0.25, ORANGE)])
        dots = dots_in(TX, -1.4, 2.2, 1.8, 7, ORANGE, r=0.07, seed=9, f0=0.3, f1=0.75)
        gg = Gauge(-1.7, -1.4, 3.6, level=0.0)
        glab = lab("hormone response", 22, GREEN).move_to([-0.6, 2.45, 0])
        cap = lab("broken cells", 24, GREY).move_to([TX, -1.95, 0])
        hor = chip("hormone", YELLOW, 26).move_to([TX, 3.05, 0])

        self.at("Sutherland and Rall")
        self.play(FadeIn(tag), run_time=0.4)
        self.at("survived breaking")
        self.play(FadeIn(tube), FadeIn(dots), FadeIn(cap), FadeIn(hor, shift=DOWN * 0.1), FadeIn(gg), FadeIn(glab),
                  run_time=0.7)
        self.play(gg.to(0.8, GREEN, 0.6))
        self.at("split into")
        self.play(FadeOut(VGroup(tube, dots, cap, hor, gg, glab)), run_time=0.4)
        memb = RoundedRectangle(corner_radius=0.2, width=3.3, height=1.5, stroke_color=ORANGE, stroke_width=3.5,
                                fill_color=ORANGE, fill_opacity=0.25).move_to([-3.6, 0.5, 0])
        ml = lab("membrane step", 26, ORANGE).move_to([-3.6, 0.5, 0])
        stube = make_tube(3.6, 2.2, -1.3, 1.9, [(0, 0.7, BLUE)])
        sl = lab("soluble step", 26, BLUE).move_to([3.6, -1.85, 0])
        mid = arr([-1.7, 0.5, 0], [2.4, 0.5, 0], GREY, 4, 0.18)
        hf = chip("heat-stable factor", YELLOW, 22).move_to([0.35, 1.2, 0])
        hh = chip("hormone", YELLOW, 24).move_to([-3.6, 2.5, 0])
        ha = arr([-3.6, 2.2, 0], [-3.6, 1.3, 0], YELLOW, 4, 0.16)
        self.play(FadeIn(memb), FadeIn(ml), FadeIn(stube), FadeIn(sl), FadeIn(hh), GrowArrow(ha), run_time=0.7)
        self.play(GrowArrow(mid), FadeIn(hf), run_time=0.4)
        self.at("That needed broken")
        need = lab("separating the two steps needed broken cells", 26, TEXT).move_to([0.0, 3.1, 0])
        self.play(FadeIn(need, shift=DOWN * 0.1), run_time=0.5)

        # ---------------- Nirenberg and Matthaei
        self.at("Nirenberg")
        old = VGroup(tag, memb, ml, stube, sl, mid, need, hf, hh, ha)
        tag2 = date_tag("Nirenberg, Matthaei, 1961")
        NX = -3.0
        nt = make_tube(NX, 2.2, -1.4, 1.9, [(0, 0.78, BLUE)])
        nd = dots_in(NX, -1.4, 2.2, 1.9, 8, ORANGE, r=0.07, seed=4, f0=0.1, f1=0.7)
        ng = Gauge(-0.8, -1.4, 3.6, level=0.0)
        nglab = lab("protein synthesis", 22, GREEN).move_to([0.2, 2.45, 0])
        ncap = lab("E. coli extract", 24, GREY).move_to([NX, -1.95, 0])
        self.play(FadeOut(old), FadeIn(tag2), FadeIn(nt), FadeIn(nd), FadeIn(ng), FadeIn(nglab), FadeIn(ncap), run_time=0.8)
        self.at("synthetic poly")
        pu = chip("synthetic poly-U", YELLOW, 26).move_to([NX, 3.05, 0])
        self.play(FadeIn(pu, shift=DOWN * 0.1), run_time=0.4)
        nocell = lines("a template no", "cell would take up", size=24, color=YELLOW).move_to([3.4, 2.1, 0])
        self.at("no cell")
        self.play(FadeIn(nocell), run_time=0.4)
        self.at("It made")
        self.play(pu.animate.move_to([NX, 1.2, 0]).scale(0.6).set_opacity(0.0), ng.to(0.85, GREEN, 0.8), run_time=0.8)
        prod = chip("polyphenylalanine", GREEN, 28).move_to([3.4, 0.5, 0])
        pa = arr([-0.35, 0.2, 0], [prod.get_left()[0] - 0.1, 0.5, 0], GREEN, 4, 0.16)
        self.play(GrowArrow(pa), FadeIn(prod, shift=LEFT * 0.2), run_time=0.5)
        self.at("the first codon")
        first = lab("the first codon assignment", 26, GOLD).move_to([3.4, -0.5, 0])
        self.play(FadeIn(first, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08UnlockedB(SpokenScene):
    """Hershko, Ciechanover and Rose (late 1970s); Murray and Kirschner (1989); the rule."""

    def construct(self):
        tag = date_tag("Hershko and colleagues, late 1970s")
        xs = [-4.2, -0.4, 3.4]
        ytop, ybot = 2.7, -0.6
        self.at("In the late")
        self.play(FadeIn(tag), run_time=0.4)
        self.at("combined fractions")
        ua = make_tube(xs[0], ytop, ybot, 1.5, [(0, 0.5, BLUE)])
        ub = make_tube(xs[1], ytop, ybot, 1.5, [(0, 0.5, ORANGE)])
        ga = Gauge(xs[0] + 1.3, ybot, ytop - ybot, level=0.0)
        gb = Gauge(xs[1] + 1.3, ybot, ytop - ybot, level=0.0)
        la = lines("Fraction 1", "alone", size=22, color=BLUE).move_to([xs[0] + 0.7, -1.3, 0])
        lb = lines("Fraction 2", "alone", size=22, color=ORANGE).move_to([xs[1] + 0.7, -1.3, 0])
        self.play(FadeIn(ua), FadeIn(ub), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb), run_time=0.7)
        self.at("Neither fraction alone")
        na = T("none", 24, RED).move_to([xs[0] + 1.3, ytop + 0.35, 0])
        nb = T("none", 24, RED).move_to([xs[1] + 1.3, ytop + 0.35, 0])
        self.play(FadeOut(la), FadeOut(lb), run_time=0.01)
        la = lines("Fraction 1 alone", size=22, color=BLUE).move_to([xs[0] + 0.7, -1.3, 0])
        lb = lines("Fraction 2 alone", size=22, color=ORANGE).move_to([xs[1] + 0.7, -1.3, 0])
        gl = lab("ATP-dependent protein breakdown", 22, GREEN).move_to([0.0, 3.6, 0])
        self.play(FadeIn(la), FadeIn(lb), FadeIn(na), FadeIn(nb), FadeIn(gl), run_time=0.4)
        self.at("Together they restored")
        uc = make_tube(xs[2], ytop, ybot, 1.5, [(0, 0.45, ORANGE), (0.45, 0.9, BLUE)])
        gc = Gauge(xs[2] + 1.3, ybot, ytop - ybot, level=0.0)
        lc = lines("together", size=22, color=TEXT).move_to([xs[2] + 0.7, -1.3, 0])
        self.play(FadeIn(uc), FadeIn(gc), FadeIn(lc), run_time=0.5)
        self.play(gc.to(0.85, GREEN, 0.7))

        self.at("Only a tube")
        only = lab("fractions can be combined and recombined", 26, TEXT).move_to([0, -2.3, 0])
        self.play(FadeIn(only, shift=UP * 0.1), run_time=0.5)

        # ---------------- Murray and Kirschner
        self.at("Murray")
        old = VGroup(tag, ua, ub, ga, gb, la, lb, na, nb, uc, gc, lc, gl, only)
        tag2 = date_tag("Murray, Kirschner, 1989")
        rc = np.array([-3.0, 0.1, 0.0])
        R = 2.2
        arc1 = Arc(radius=R, start_angle=PI / 2, angle=-PI * 1.15, stroke_color=GREY, stroke_width=7).move_to(rc)
        arc1 = Arc(radius=R, start_angle=PI / 2, angle=-PI * 1.15, stroke_color=GREY, stroke_width=7, arc_center=rc)
        arc2 = Arc(radius=R, start_angle=PI / 2 - PI * 1.15, angle=-PI * 0.85, stroke_color=YELLOW, stroke_width=7, arc_center=rc)
        il = lab("interphase", 22, GREY).move_to(rc + [-0.0, -0.0, 0])
        il.move_to(rc + [0.7, 0.3, 0])
        ml_ = lab("mitosis", 22, YELLOW).move_to(rc + [-0.9, -0.3, 0])
        ex_lbl = lab("frog egg extract", 26, GREY).move_to(rc + [0, 2.8, 0])
        ang0 = PI / 2
        marker = Dot(rc + [0, R, 0], radius=0.17, color=GREEN)
        self.play(FadeOut(old), FadeIn(tag2), FadeIn(arc1), FadeIn(arc2), FadeIn(il), FadeIn(ml_), FadeIn(ex_lbl),
                  FadeIn(marker), run_time=0.8)
        self.at("extracts cycle")
        self.play(Rotate(marker, angle=-TAU, about_point=rc, rate_func=linear), run_time=1.4)
        cyc = lab("cycles in a tube", 24, GREEN).move_to(rc + [0, -2.8, 0])
        self.play(FadeIn(cyc), run_time=0.3)
        self.at("Destroying their messenger")
        mr = chip("messenger RNA", GREY, 26).move_to([3.1, 1.7, 0])
        xx = T("✕", 44, RED, weight=BOLD).next_to(mr, RIGHT, buff=0.15)
        self.play(FadeIn(mr, shift=LEFT * 0.2), run_time=0.4)
        self.play(FadeIn(xx, scale=1.5), run_time=0.3)
        self.at("arrested them in")
        # stop the marker on the interphase arc
        arr_lbl = lab("arrested in interphase", 24, RED).move_to([3.4, 0.4, 0])
        self.play(FadeOut(cyc), FadeIn(arr_lbl), marker.animate.move_to(rc + [R * np.cos(-0.5), R * np.sin(-0.5), 0]).set_color(RED),
                  run_time=0.6)
        self.at("Adding cyclin")
        cm = chip("cyclin messenger RNA", PURPLE, 26).move_to([3.4, -1.0, 0])
        self.play(FadeOut(VGroup(mr, xx, arr_lbl)), FadeIn(cm, shift=LEFT * 0.2), run_time=0.4)
        self.at("restored the cycles")
        self.play(marker.animate.set_color(GREEN), run_time=0.2)
        self.play(Rotate(marker, angle=-TAU, about_point=rc, rate_func=linear), run_time=1.4)
        res = lab("cycles restored", 24, GREEN).move_to([3.4, -2.0, 0])
        self.play(FadeIn(res), run_time=0.3)

        # ---------------- the rule
        self.at("shows what the parts")
        old2 = VGroup(arc1, arc2, il, ml_, ex_lbl, marker, cm, res, tag2)
        tb = make_tube(-3.8, 2.2, -1.2, 1.8, [(0, 0.45, BLUE), (0, 0.15, ORANGE)])
        pd = dots_in(-3.8, -1.2, 2.2, 1.8, 4, PURPLE, r=0.1, seed=1, f0=0.25, f1=0.4)
        tl = lines("the parts,", "in a tube", size=24, color=TEXT).move_to([-3.8, -1.85, 0])
        self.play(FadeOut(old2), FadeIn(tb), FadeIn(pd), FadeIn(tl), run_time=0.7)
        can = lab("what the parts can do", 28, GREEN).move_to([-3.8, 2.85, 0])
        self.play(FadeIn(can), run_time=0.4)
        self.at("not that the cell")
        cell = Circle(radius=1.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([3.4, 0.5, 0])
        q = T("?", 80, YELLOW, weight=BOLD).move_to(cell)
        ra = arr([-2.4, 0.5, 0], [1.5, 0.5, 0], GREY, 5, 0.22)
        cl = lab("how the cell uses them", 24, YELLOW).move_to([3.4, 2.85, 0])
        self.play(GrowArrow(ra), FadeIn(cell), FadeIn(q), FadeIn(cl), run_time=0.8)
        self.at("a separate experiment")
        sep = lines("a separate experiment is needed:", "a mutant or a cell test", size=26, color=GOLD).move_to([3.4, -2.0, 0])
        self.play(FadeIn(sep, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A tube shows what parts can do, not that cells use them."
