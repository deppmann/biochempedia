"""Designing a causal circuit experiment: light alone can change behaviour (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  YELLOW = light (the stimulus)
  BLUE   = the targeted cells / opsin-carrying animals
  GREY   = fluorophore-only control, structure, de-emphasised
  GREEN  = the behaviour or measured outcome, and "driven / sufficient"
  RED    = suppress / block / struck out / "necessary" test
  GOLD   = numbers, the interaction, the effect size
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


class Sp(SpokenScene):
    """beat() capped at 1 s so animations stay short and the cues, not the animations, set the pace."""
    def beat(self, fraction):
        return min(1.0, super().beat(fraction))


def neuron(color=BLUE, s=1.0):
    soma = Circle(radius=0.5, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)
    dends = VGroup(*[Line(soma.get_center() + 0.5 * np.array([np.cos(a), np.sin(a), 0]),
                          soma.get_center() + 1.0 * np.array([np.cos(a), np.sin(a), 0]),
                          color=color, stroke_width=4) for a in (2.3, 2.9, 3.5, 1.2)])
    axon = Line(soma.get_center() + RIGHT * 0.5, soma.get_center() + RIGHT * 1.6, color=color, stroke_width=4)
    return VGroup(soma, dends, axon).scale(s)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22, **kw):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12, **kw)


def blockbar(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def light(label="light", size=26):
    return bchip(label, YELLOW, size=size)


def beam(start, end, spread=0.5):
    start, end = np.array(start, float), np.array(end, float)
    d = (end - start) / np.linalg.norm(end - start)
    perp = np.array([-d[1], d[0], 0])
    return Polygon(start, end + perp * spread, end - perp * spread, stroke_width=0,
                   fill_color=YELLOW, fill_opacity=0.28)


def strike(mob, color=RED):
    return Line(mob.get_corner(DL) + LEFT * 0.1, mob.get_corner(UR) + RIGHT * 0.1, color=color, stroke_width=6)


def box(w, h, color, label=None, size=24):
    r = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3.5,
                         fill_color=color, fill_opacity=0.10)
    g = VGroup(r)
    if label:
        t = T(label, size=size, color=color).move_to(r)
        g.add(t)
    return g


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Designing a Causal Circuit Experiment"
    TITLE = "Light Alone Can Change Behaviour"


# ---------------------------------------------------------------------------------------------
class S01Lightalone(Sp):
    def construct(self):
        cap = T("wild-type mice, no opsin: Owen, Liu and Kreitzer", size=24, color=GREY).to_edge(DOWN, buff=0.4)
        cell = neuron(GREY, 2.2).move_to(LEFT * 3.2 + DOWN * 0.5)
        nolab = T("no opsin", size=30, color=GREY).next_to(cell, DOWN, buff=0.45)
        region = T("dorsal striatum", size=30, color=GREY)
        self.at("Shine light")
        self.play(FadeIn(cell), FadeIn(nolab), run_time=0.4)
        lt = light(size=30).move_to(LEFT * 3.2 + UP * 3.0)
        region.next_to(lt, RIGHT, buff=0.4)
        self.play(FadeIn(lt), run_time=self.beat(0.03))
        b = beam(lt.get_bottom() + DOWN * 0.05, cell.get_center() + UP * 1.25, 0.9)
        self.play(FadeIn(b), FadeIn(region), run_time=self.beat(0.04))
        self.at("Its firing rate falls")
        fr = bchip("firing rate falls", GREEN, size=34).move_to(RIGHT * 2.2 + UP * 1.6)
        fa = Arrow(UP * 0.45, DOWN * 0.45, color=GREEN, stroke_width=9).next_to(fr, RIGHT, buff=0.3)
        self.play(FadeIn(fr, shift=LEFT * 0.2), GrowArrow(fa), run_time=self.beat(0.07))
        self.at("turning to one side")
        tn = bchip("turns to one side", GREEN, size=34).move_to(RIGHT * 2.2 + UP * 0.1)
        ta = CurvedArrow(tn.get_right() + RIGHT * 0.3 + UP * 0.3, tn.get_right() + RIGHT * 0.3 + DOWN * 0.5,
                         angle=-TAU / 4, color=GREEN, stroke_width=7)
        self.play(FadeIn(tn, shift=LEFT * 0.2), Create(ta), run_time=self.beat(0.07))
        self.at("Owen Liu and Kreitzer reported")
        self.play(FadeIn(cap), run_time=self.beat(0.05))
        self.at("So what does a")
        q = T("light on  versus  light off", size=44).move_to(RIGHT * 2.2 + DOWN * 1.6)
        self.play(FadeIn(q), run_time=self.beat(0.06))
        self.at("It compares light with no light")
        q2 = T("light  versus  no light", size=44, color=YELLOW).move_to(q)
        self.play(FadeOut(q), run_time=0.25)
        self.play(FadeIn(q2), run_time=0.35)
        q = q2
        self.at("in animals that happen")
        side = T("in animals that happen to carry an opsin", size=30, color=BLUE).next_to(q, DOWN, buff=0.4)
        self.play(FadeIn(side, shift=UP * 0.1), run_time=self.beat(0.06))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Manipulate(Sp):
    def construct(self):
        cells = VGroup(neuron(BLUE, 1.3), T("target cells", size=30, color=BLUE)).arrange(DOWN, buff=0.25)
        beh = bchip("behaviour", GREEN, size=38)
        cells.move_to(LEFT * 4.7 + UP * 1.7)
        beh.move_to(RIGHT * 4.7 + UP * 1.7)
        link = DashedLine(cells.get_right() + RIGHT * 0.3, beh.get_left() + LEFT * 0.2, color=GREY, stroke_width=5)
        self.at("A recording tells you")
        rec = T("recording", size=30, color=GREY).next_to(link, UP, buff=0.2)
        self.play(FadeIn(cells), FadeIn(beh), Create(link), FadeIn(rec), run_time=self.beat(0.06))
        self.at("goes with")
        gw = T("goes with", size=32, color=TEXT).next_to(link, DOWN, buff=0.2)
        self.play(FadeIn(gw), run_time=self.beat(0.04))
        self.at("whether the activity produces it")
        qm = T("produces?", size=32, color=YELLOW).move_to(gw)
        self.play(Transform(gw, qm), run_time=self.beat(0.05))
        self.at("change the activity on purpose")
        lt = light(size=30).move_to(LEFT * 2.0 + UP * 3.1)
        lbeam = arr(lt.get_left() + DOWN * 0.05, cells[0].get_center() + UP * 0.45 + RIGHT * 0.55, YELLOW, 6)
        solid = arr(cells.get_right() + RIGHT * 0.3, beh.get_left() + LEFT * 0.2, GREY)
        self.play(FadeOut(rec), FadeOut(gw), ReplacementTransform(link, solid), FadeIn(lt), GrowArrow(lbeam), run_time=self.beat(0.07))
        self.at("Drive the cells")
        rowA = VGroup(bchip("drive", GREEN, size=34), arr(LEFT, RIGHT, GREEN, 6), bchip("sufficient?", GREEN, size=38))
        rowA[1].scale(0.6)
        rowA.arrange(RIGHT, buff=0.3).move_to(LEFT * 2.8 + DOWN * 0.6)
        self.play(FadeIn(rowA, shift=RIGHT * 0.2), run_time=self.beat(0.06))
        self.at("Suppress them")
        rowB = VGroup(bchip("suppress", RED, size=34), arr(LEFT, RIGHT, RED, 6), bchip("necessary?", RED, size=38))
        rowB[1].scale(0.6)
        rowB.arrange(RIGHT, buff=0.3).move_to(LEFT * 2.8 + DOWN * 2.1)
        self.play(FadeIn(rowB, shift=RIGHT * 0.2), run_time=self.beat(0.06))
        self.at("Both answers hold only")
        lim = VGroup(bchip("the cells targeted", BLUE, size=30), bchip("the time illuminated", YELLOW, size=30),
                     bchip("the assay scored", GREEN, size=30)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        lim.move_to(RIGHT * 4.0 + DOWN * 1.35)
        self.play(FadeIn(lim[0], shift=LEFT * 0.2), run_time=self.beat(0.05))
        self.at("the time you illuminated")
        self.play(FadeIn(lim[1], shift=LEFT * 0.2), run_time=self.beat(0.05))
        self.at("assay you scored")
        self.play(FadeIn(lim[2], shift=LEFT * 0.2), run_time=self.beat(0.05))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Twobytwo(Sp):
    def construct(self):
        cw, ch = 3.3, 2.7
        x0, y0 = -0.1, -0.4
        cols = ["no light", "light"]
        rows = ["opsin", "fluorophore\nonly"]
        rcol = [BLUE, GREY]
        grid = VGroup()
        cellpos = {}
        for r in range(2):
            for c in range(2):
                pos = np.array([x0 + (c - 0.5) * cw, y0 + (0.5 - r) * ch, 0])
                rect = Rectangle(width=cw, height=ch, stroke_color=GREY, stroke_width=2).move_to(pos)
                grid.add(rect)
                cellpos[(r, c)] = pos
        hdrs = VGroup(*[T(cols[c], size=32, color=YELLOW if c else GREY).move_to(cellpos[(0, c)] + UP * (ch / 2 + 0.4)) for c in range(2)])
        rlabs = VGroup(*[T(rows[r], size=32, color=rcol[r], line_spacing=0.9).next_to(cellpos[(r, 0)] + LEFT * cw / 2, LEFT, buff=0.3) for r in range(2)])
        self.at("The minimum design crosses")
        self.play(Create(grid), run_time=self.beat(0.08))
        self.play(FadeIn(hdrs), FadeIn(rlabs), run_time=self.beat(0.06))
        base = 0.55
        heights = {(0, 0): base, (1, 0): base, (1, 1): 1.1, (0, 1): 1.85}

        def mk(r, c):
            h = heights[(r, c)]
            col = BLUE if r == 0 else GREY
            rec = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=GREEN if (r, c) == (0, 1) else col, fill_opacity=0.65)
            rec.move_to(cellpos[(r, c)] + DOWN * (ch / 2 - 0.25 - h / 2) + RIGHT * 0.7)
            ic = neuron(col, 0.42).move_to(cellpos[(r, c)] + LEFT * 0.7 + UP * 0.1)
            tag = []
            if c == 1:
                tag.append(Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=0.9, stroke_width=0).scale(0.16).rotate(PI).move_to(cellpos[(r, c)] + LEFT * 1.05 + UP * 0.95))
            return VGroup(ic, rec, *tag)
        order = [("Opsin with light", (0, 1)), ("Opsin without light", (0, 0)),
                 ("only with light", (1, 1)), ("only without light", (1, 0))]
        note = T("bar height: in this sketch", size=24, color=GREY).move_to(DOWN * 3.65 + RIGHT * x0)
        for phrase, key in order:
            self.at(phrase)
            if key == (0, 1):
                self.play(FadeIn(note), run_time=0.3)
            g = mk(*key)
            hl = Rectangle(width=cw, height=ch, stroke_color=YELLOW, stroke_width=5).move_to(cellpos[key])
            self.play(FadeIn(g), Create(hl), run_time=self.beat(0.05))
            self.play(FadeOut(hl), run_time=self.beat(0.02))
        self.at("the interaction")
        top_c = cellpos[(0, 1)] + DOWN * (ch / 2 - 0.25) + RIGHT * 0.7
        lo = top_c + UP * 1.1
        hi = top_c + UP * 1.85
        br = Brace(Line(lo + RIGHT * 0.5, hi + RIGHT * 0.5), direction=RIGHT, color=GOLD)
        lab = T("extra effect\nof light with\nthe opsin", size=28, color=GOLD, line_spacing=0.9).next_to(br, RIGHT, buff=0.15)
        br.shift(RIGHT * (cellpos[(0, 1)][0] + cw / 2 - br.get_left()[0] + 0.1))
        lab.next_to(br, RIGHT, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(lab), run_time=self.beat(0.08))
        self.at("extra effect of light")
        self.play(Indicate(lab, color=GOLD, scale_factor=1.1), run_time=self.beat(0.06))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Projection(Sp):
    def construct(self):
        names = VGroup(*[bchip(t, c, size=28) for t, c in [("cells", BLUE), ("projection", GREY), ("timing", YELLOW), ("behaviour", GREEN)]]).arrange(RIGHT, buff=0.4)
        names.move_to(UP * 3.2)
        self.at("A usable claim names")
        for n in names:
            self.play(FadeIn(n, shift=DOWN * 0.1), run_time=self.beat(0.025))
        cy = -0.1
        bla = box(3.0, 2.2, BLUE, None).move_to(LEFT * 4.9 + UP * cy)
        bla_l = T("basolateral\namygdala", size=28, color=BLUE, line_spacing=0.9).move_to(bla)
        cea = box(3.0, 2.2, GREY, None).move_to(UP * cy)
        cea_l = T("central\namygdala", size=28, color=GREY, line_spacing=0.9).move_to(cea)
        beh = box(3.0, 2.2, GREEN, None).move_to(RIGHT * 4.9 + UP * cy)
        beh_l = T("anxiety-related\nbehaviour", size=28, color=GREEN, line_spacing=0.9).move_to(beh)
        mice = T("freely moving mice", size=26, color=GREY).to_edge(DOWN, buff=0.35)
        self.at("colleagues lit basolateral")
        self.play(FadeIn(VGroup(bla, bla_l)), run_time=self.beat(0.04))
        self.at("terminals in the central amygdala")
        term = arr(bla.get_right(), cea.get_left(), GREY, 6)
        tl = T("terminals", size=26, color=GREY).next_to(term, UP, buff=0.12)
        self.play(GrowArrow(term), FadeIn(VGroup(cea, cea_l)), FadeIn(tl), run_time=self.beat(0.06))
        self.play(FadeIn(mice), FadeIn(VGroup(beh, beh_l)), run_time=self.beat(0.04))
        self.at("Activating those terminals")
        lt = light(size=30).move_to(cea.get_center() + UP * 2.0)
        bm = beam(lt.get_bottom() + DOWN * 0.05, cea.get_top() + DOWN * 0.1, 0.8)
        self.play(FadeIn(lt), FadeIn(bm), run_time=self.beat(0.05))
        self.at("terminals reduced anxiety")
        red = Arrow(UP * 0.45, DOWN * 0.45, color=GREEN, stroke_width=9).next_to(beh, DOWN, buff=0.25)
        redt = T("reduced", size=30, color=GREEN).next_to(red, RIGHT, buff=0.15)
        self.play(GrowArrow(red), FadeIn(redt), run_time=self.beat(0.05))
        self.at("excite axons passing through")
        pas = Line(cea.get_left() + DOWN * 0.6 + RIGHT * 0.25, cea.get_right() + DOWN * 0.6 + LEFT * 0.25, color=YELLOW, stroke_width=5)
        pq = T("?", size=44, color=YELLOW).next_to(cea, DOWN, buff=0.1)
        pl = T("axons passing through", size=26, color=YELLOW).next_to(pq, DOWN, buff=0.1)
        self.play(Create(pas), FadeIn(pq), FadeIn(pl), run_time=self.beat(0.06))
        self.at("parent cell bodies")
        back = CurvedArrow(cea.get_top() + LEFT * 0.9, bla.get_top() + RIGHT * 0.7, angle=TAU / 5, color=YELLOW, stroke_width=5)
        bq = T("?", size=44, color=YELLOW).next_to(bla, DOWN, buff=0.1)
        bl = T("parent cell bodies", size=26, color=YELLOW).next_to(bq, DOWN, buff=0.1)
        self.play(Create(back), FadeIn(bq), FadeIn(bl), run_time=self.beat(0.06))
        self.at("blocked glutamate receptors")
        blk = bchip("glutamate receptors blocked", RED, size=28).next_to(cea, DOWN, buff=0.95)
        bar = blockbar(blk.get_top(), cea.get_bottom() + DOWN * 0.02, RED)
        self.play(FadeOut(pas), FadeOut(pq), FadeOut(pl), FadeOut(back), FadeOut(bq), FadeOut(bl), FadeOut(red), FadeOut(redt),
                  run_time=self.beat(0.04))
        self.play(FadeIn(blk), Create(bar), run_time=self.beat(0.05))
        self.at("abolished the")
        ab = T("no reduction", size=30, color=GREEN).next_to(beh, DOWN, buff=0.3)
        self.play(FadeIn(ab), run_time=self.beat(0.05))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Arithmetic(Sp):
    def construct(self):
        base = DOWN * 2.1 + LEFT * 5.9
        sc = 0.05
        ax = Line(base + LEFT * 0.0, base + RIGHT * 4.5, color=GREY, stroke_width=3)
        h1, h2 = 60 * sc, 48 * sc
        b1 = Rectangle(width=1.6, height=h1, stroke_width=0, fill_color=BLUE, fill_opacity=0.7).move_to(base + RIGHT * 1.1 + UP * h1 / 2)
        b2 = Rectangle(width=1.6, height=h2, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to(base + RIGHT * 3.4 + UP * h2 / 2)
        l1 = T("opsin\nwith light", size=24, color=BLUE, line_spacing=0.9).next_to(ax, DOWN, buff=0.12).set_x(b1.get_x())
        l2 = T("fluorophore\nwith light", size=24, color=GREY, line_spacing=0.9).next_to(ax, DOWN, buff=0.12).set_x(b2.get_x())
        yl = T("avoidance time (s)", size=26, color=GREY).move_to(LEFT * 3.6 + UP * 2.55)
        inv = T("numbers invented for teaching", size=24, color=GREY).move_to(DOWN * 3.5).set_x(-3.6)
        self.at("Now the arithmetic")
        self.play(FadeIn(inv), Create(ax), FadeIn(yl), run_time=self.beat(0.05))
        self.at("seconds of avoidance")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=self.beat(0.05))
        v1 = M("60 s", 30, BLUE).next_to(b1, UP, buff=0.1)
        self.play(FadeIn(v1), run_time=self.beat(0.02))
        self.at("both lit")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=self.beat(0.05))
        v2 = M("48 s", 30, GREY).next_to(b2, UP, buff=0.1)
        self.play(FadeIn(v2), run_time=self.beat(0.02))
        self.at("The pooled standard deviation")
        sd = M("pooled SD = 12 s", 28, GOLD).move_to(LEFT * 3.6 + UP * 1.95)
        self.play(FadeIn(sd), run_time=self.beat(0.05))
        self.at("The difference divided by")
        d1 = M("d = (60 - 48) / 12 = 1.0", 30, GOLD).move_to(LEFT * 3.6 + UP * 3.2)
        self.play(FadeIn(d1), run_time=self.beat(0.06))
        axes = Axes(x_range=[0.4, 1.2, 0.1], y_range=[0, 100, 25], x_length=5.4, y_length=4.0,
                    axis_config={"color": GREY, "stroke_width": 3, "include_tip": False}).move_to(RIGHT * 3.5 + DOWN * 0.7)
        ticks = VGroup(*[M(str(v), 24, GREY).next_to(axes.c2p(v, 0), DOWN, buff=0.1) for v in (0.5, 1.0)],
                       *[M(str(v), 24, GREY).next_to(axes.c2p(0.4, v), LEFT, buff=0.1) for v in (0, 50, 100)])
        xl = T("effect size, d", size=26, color=GREY).next_to(axes, DOWN, buff=0.5)
        yl2 = T("animals per group", size=26, color=GREY).next_to(axes, UP, buff=0.15).set_x(axes.get_x())
        curve = axes.plot(lambda d: 2 * (1.96 + 0.84) ** 2 / d ** 2, x_range=[0.4, 1.2], color=GOLD, stroke_width=5)
        fm = M("n = 2(1.96+0.84)^2 / d^2", 26, GOLD).next_to(yl2, UP, buff=0.2)
        self.at("power and a")
        self.play(Create(axes), FadeIn(ticks), FadeIn(xl), FadeIn(yl2), run_time=self.beat(0.04))
        self.play(FadeIn(fm), Create(curve), run_time=self.beat(0.05))
        self.at("animals per group")
        p1 = Dot(axes.c2p(1.0, 15.68), color=YELLOW, radius=0.13)
        t1 = M("16", 34, YELLOW).next_to(p1, UR, buff=0.12)
        self.play(FadeIn(p1, scale=1.5), FadeIn(t1), run_time=self.beat(0.04))
        self.at("if the true effect is half")
        p2 = Dot(axes.c2p(0.5, 62.72), color=RED, radius=0.13)
        t2 = M("63", 34, RED).next_to(p2, UR, buff=0.12)
        h = T("half the effect: d = 0.5", size=26, color=RED).next_to(t2, RIGHT, buff=0.3)
        self.play(FadeIn(h), FadeIn(p2, scale=1.5), FadeIn(t2), run_time=self.beat(0.05))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Unit(Sp):
    def construct(self):
        self.at("Count animals")
        mice = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.15, width=1.25, height=1.25, stroke_color=BLUE, stroke_width=3,
                                                fill_color=BLUE, fill_opacity=0.15),
                               T("40\ntrials", size=24, color=GREY, line_spacing=0.85)) for _ in range(8)])
        for m in mice:
            m[1].move_to(m[0])
        mice.arrange(RIGHT, buff=0.22).move_to(UP * 2.3)
        cnt = T("8 animals", size=40, color=GOLD).next_to(mice, UP, buff=0.3)
        self.play(FadeIn(mice, lag_ratio=0.1), run_time=self.beat(0.08))
        self.play(FadeIn(cnt), run_time=self.beat(0.03))
        self.at("independent observations")
        bad = T("320 independent observations", size=36, color=RED).next_to(mice, DOWN, buff=0.4)
        self.play(FadeIn(bad), run_time=self.beat(0.04))
        self.play(Create(strike(bad)), run_time=self.beat(0.03))
        self.at("a small pilot overestimates")
        hs = [1.0, 1.55, 1.3, 2.6, 1.4, 1.1]
        true = 1.4
        pil = VGroup(*[Rectangle(width=0.5, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.6) for h in hs])
        pil.arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        pil.move_to(LEFT * 4.1)
        pil.align_to(DOWN * 3.15, DOWN)
        yb = pil[0].get_bottom()[1]
        tl = DashedLine([pil.get_left()[0] - 0.2, yb + true, 0], [pil.get_right()[0] + 0.2, yb + true, 0], color=GOLD, stroke_width=3)
        tlab = T("true effect", size=26, color=GOLD).next_to(tl, RIGHT, buff=0.15)
        skl = T("pilot estimates, in this sketch", size=24, color=GREY).next_to(pil, DOWN, buff=0.1)
        self.play(FadeIn(pil, lag_ratio=0.1), Create(tl), FadeIn(tlab), run_time=self.beat(0.06))
        self.play(FadeIn(skl), run_time=self.beat(0.02))
        self.at("the pilot that overshoots is the one followed up")
        pick = pil[3]
        self.play(pick.animate.set_fill(YELLOW, 0.9), run_time=self.beat(0.06))
        fu = T("followed up", size=28, color=YELLOW).next_to(pick, UP, buff=0.12)
        self.play(FadeIn(fu), run_time=self.beat(0.03))
        self.at("power the study on")
        rule = VGroup(bchip("control the light", YELLOW, size=34), bchip("count animals", BLUE, size=34),
                      bchip("size for the smaller effect", GOLD, size=34)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rule.move_to(RIGHT * 3.7 + DOWN * 1.8)
        self.play(FadeIn(rule[1], shift=LEFT * 0.2), run_time=self.beat(0.04))
        self.at("Control for the light")
        self.play(FadeIn(rule[0], shift=LEFT * 0.2), run_time=self.beat(0.04))
        self.at("size for the smaller effect")
        self.play(FadeIn(rule[2], shift=LEFT * 0.2), run_time=self.beat(0.04))
        self.finish()


class S07End(EndCard):
    LINE = "Control for the light, and size for the smaller effect."
