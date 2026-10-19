"""Retinal cell types: a count depends on its method  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = ganglion cells
  RED    = displaced amacrine cells, set aside
  YELLOW = imaging / light response / functional
  TEAL   = sequencing / expression (RNA)
  ORANGE = same-cell recording
  PURPLE = electron microscopy / shape / anatomical
  GOLD   = a supported type (the answer)
  GREEN  = mosaic
  GREY   = outlines, frames, de-emphasized
  TEXT   = neutral numbers
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def gcell(color=BLUE, s=1.0):
    """simple ganglion cell: soma, dendrites up, axon to the right."""
    soma = Circle(radius=0.28, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.35)
    parts = [soma]
    for dx in (-0.35, 0.0, 0.35):
        parts.append(Line([dx * 0.4, 0.26, 0], [dx * 1.2, 0.95, 0], color=color, stroke_width=4))
        parts.append(Line([dx * 1.2, 0.95, 0], [dx * 1.2 - 0.12, 1.25, 0], color=color, stroke_width=3))
        parts.append(Line([dx * 1.2, 0.95, 0], [dx * 1.2 + 0.12, 1.25, 0], color=color, stroke_width=3))
    parts.append(Line([0.28, 0, 0], [1.4, 0, 0], color=color, stroke_width=4))
    g = VGroup(*parts)
    g.scale(s)
    return g


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def card(num, label, color, size=44):
    c = chip(num, color, size=size)
    l = T(label, 24, color)
    return VGroup(c, l).arrange(DOWN, buff=0.2)


class S00Title(TitleCard):
    LESSON = "Forty kinds of ganglion cell"
    TITLE = "A count depends on its method"


# -------------------------------------------------------------------------------------------
class S01Disagree(SpokenScene):
    def construct(self):
        head = T("Mouse retinal ganglion cells: how many types?", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=1.2)
        labels = ["at least 32", "at least 35", "42", "46"]
        chips = [chip(l, TEXT, size=38) for l in labels]
        row = VGroup(*chips).arrange(RIGHT, buff=0.45).move_to([0, 1.5, 0])
        fit(row, max_w=12.3)
        self.at("gave at least")
        self.play(FadeIn(chips[0], shift=DOWN * 0.3), run_time=0.5)
        self.at("35", lead=0.1)
        self.play(FadeIn(chips[1], shift=DOWN * 0.3), run_time=0.5)
        self.at("42", lead=0.1)
        self.play(FadeIn(chips[2], shift=DOWN * 0.3), run_time=0.5)
        self.at("and 46", lead=0.0)
        self.play(FadeIn(chips[3], shift=DOWN * 0.3), run_time=0.5)
        self.at("Yet the numbers")
        self.play(*[Indicate(c, color=RED, scale_factor=1.08) for c in chips], run_time=0.9)
        cell = gcell(BLUE, 1.3).move_to([-2.4, -2.4, 0])
        nerve = RoundedRectangle(corner_radius=0.15, width=4.0, height=0.5, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.3).move_to([2.3, -2.4, 0])
        nlab = T("optic nerve", 26, GREY).next_to(nerve, DOWN, buff=0.2)
        clab = T("ganglion cell", 26, BLUE).next_to(cell, DOWN, buff=0.2).shift(LEFT * 0.2)
        self.at("Ganglion cell axons")
        self.play(FadeIn(cell), FadeIn(clab), run_time=0.6)
        self.at("optic nerve")
        ax = Line(cell[-1].get_end(), nerve.get_left(), color=BLUE, stroke_width=4)
        self.play(Create(ax), FadeIn(nerve), FadeIn(nlab), run_time=0.8)
        q = T("?", 80, GOLD, weight=BOLD).move_to([0, -0.1, 0])
        self.at("who is right")
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.play(Indicate(q, color=GOLD, scale_factor=1.2), run_time=0.8)
        self.finish()


# -------------------------------------------------------------------------------------------
class S02Imaging(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(3)
        head = T("Imaging: counted by light response", 34, YELLOW, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.at("Imaging counted")
        self.play(Write(head), run_time=1.0)
        panel = RoundedRectangle(corner_radius=0.2, width=6.8, height=4.4, stroke_color=GREY, stroke_width=3).move_to([-2.7, -0.5, 0])
        plab = T("ganglion cell layer, isolated mouse retina", 24, GREY).next_to(panel, UP, buff=0.15)
        dots, red_idx = [], set(rng.choice(8 * 12, 22, replace=False))
        k = 0
        for r in range(8):
            for c in range(12):
                p = [-5.45 + c * 0.55 + rng.uniform(-0.1, 0.1), 1.2 - r * 0.5 + rng.uniform(-0.08, 0.08) - 0.25, 0]
                dots.append(Dot(p, radius=0.11, color=GREY))
        dg = VGroup(*dots)
        tag = T("schematic", 22, GREY).next_to(panel, DOWN, buff=0.12).align_to(panel, LEFT)
        self.play(Create(panel), FadeIn(plab), FadeIn(dg), FadeIn(tag), run_time=0.9)
        self.at("light responses")
        self.play(*[d.animate.set_color(YELLOW) for d in dots], run_time=0.6)
        self.play(*[d.animate.scale(1.5) for d in dots], run_time=0.2)
        self.play(*[d.animate.scale(1 / 1.5) for d in dots], run_time=0.2)
        cnt = VGroup(M("11,210", 44, YELLOW), T("cells", 28, YELLOW)).arrange(RIGHT, buff=0.25).move_to([4.4, 1.8, 0])
        self.at("data set")
        self.play(FadeIn(cnt, shift=LEFT * 0.3), run_time=0.6)
        reds = [dots[i] for i in sorted(red_idx)]
        rlab = T("displaced amacrine cells", 26, RED).move_to([4.4, 0.6, 0])
        self.at("displaced amacrine")
        self.play(*[d.animate.set_color(RED) for d in reds], FadeIn(rlab), run_time=0.7)
        slab = T("14 groups set aside", 28, RED).next_to(rlab, DOWN, buff=0.25)
        self.at("set aside")
        self.play(FadeIn(slab), run_time=0.4)
        self.play(*[d.animate.shift(RIGHT * 1.5 + DOWN * 1.2).set_opacity(0) for d in reds], run_time=0.5)
        keep = [d for d in dots if d not in reds]
        self.at("What remained")
        self.play(*[d.animate.set_color(BLUE) for d in keep], FadeOut(rlab), FadeOut(slab), FadeOut(cnt), run_time=0.6)
        base_y, unit = -2.6, 0.1
        bar = Rectangle(width=2.6, height=32 * unit, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3)
        bar.move_to([4.6, base_y + 32 * unit / 2, 0])
        ext = DashedVMobject(Rectangle(width=2.6, height=1.3, stroke_color=YELLOW, stroke_width=3)).move_to(
            [4.6, base_y + 32 * unit + 0.65, 0])
        n32 = M("32", 54, YELLOW).move_to(bar).shift(DOWN * 0.3)
        lab_top = T("at least", 26, YELLOW).next_to(n32, UP, buff=0.1)
        lab_base = T("functional types", 24, YELLOW).next_to(bar, DOWN, buff=0.15)
        self.play(GrowFromEdge(bar, DOWN), FadeIn(n32), FadeIn(lab_top), FadeIn(lab_base), run_time=0.9)
        more = T("probably more", 24, YELLOW).move_to(ext)
        self.at("abundant")
        self.play(Create(ext), FadeIn(more), run_time=0.9)
        self.finish()


# -------------------------------------------------------------------------------------------
class S03Sequencing(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(7)
        head = T("Sequencing: counted by expression", 34, TEAL, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.at("Sequencing counted")
        self.play(Write(head), run_time=1.0)
        pos = []
        for r in range(5):
            for c in range(9):
                pos.append([-5.8 + c * 0.7 + rng.uniform(-0.1, 0.1), 1.7 - r * 0.8 + rng.uniform(-0.1, 0.1), 0])
        radii = rng.uniform(0.14, 0.29, 45)
        smallest = 12
        radii[smallest] = 0.1
        big = 31
        radii[big] = 0.29
        blobs = [Circle(radius=radii[i], stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.3).move_to(pos[i])
                 for i in range(45)]
        bg = VGroup(*blobs)
        sub = T("adult mice, 35,699 ganglion cell transcriptomes", 26, GREY).move_to([-3.0, -2.6, 0])
        self.at("In adult mice")
        self.play(FadeIn(sub), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in blobs], lag_ratio=0.03), run_time=1.6)
        cnt = VGroup(M("45", 54, TEAL), T("clusters", 30, TEAL)).arrange(RIGHT, buff=0.25).move_to([4.2, 1.9, 0])
        self.at("fell into")
        self.play(FadeIn(cnt, shift=LEFT * 0.3), run_time=0.5)
        b = blobs[big]
        p = b.get_center()
        a = Circle(radius=0.17, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.3).move_to(p + LEFT * 0.16)
        c2 = Circle(radius=0.17, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.3).move_to(p + RIGHT * 0.16)
        self.at("Subdividing one")
        self.play(Indicate(b, color=YELLOW, scale_factor=1.4), run_time=0.6)
        self.play(ReplacementTransform(b, VGroup(a, c2)), run_time=0.6)
        self.play(a.animate.shift(LEFT * 0.12), c2.animate.shift(RIGHT * 0.12), run_time=0.4)
        newcnt = VGroup(M("46", 54, TEAL), T("types", 30, TEAL)).arrange(RIGHT, buff=0.25).move_to(cnt)
        self.play(ReplacementTransform(cnt, newcnt), run_time=0.5)
        fine = T("the count depends on\nhow finely the data are split", 26, TEXT).move_to([4.0, 0.8, 0])
        self.at("how finely")
        self.play(FadeIn(fine), run_time=0.6)
        sm = blobs[smallest]
        ring = Circle(radius=0.28, stroke_color=GOLD, stroke_width=4).move_to(sm)
        e1 = M("0.15% of 35,699", 28, GOLD)
        e2 = M("0.0015 × 35,699 = 53.5", 26, GOLD)
        e3 = T("about 54 cells", 34, GOLD, weight=BOLD)
        eq = VGroup(e1, e2, e3).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.7, -1.2, 0])
        self.at("The smallest type")
        self.play(Create(ring), FadeIn(e1), run_time=0.6)
        self.play(FadeIn(e2), run_time=0.5)
        self.at("about")
        self.play(FadeIn(e3, scale=1.1), run_time=0.5)
        self.finish()


# -------------------------------------------------------------------------------------------
class S04Samecell(SpokenScene):
    def construct(self):
        head = T("Same-cell recording", 34, ORANGE, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.at("Recording from")
        self.play(Write(head), run_time=0.5)
        cell = gcell(BLUE, 2.2).move_to([-3.0, -0.6, 0])
        pip = Line([-5.6, -2.0, 0], [-3.6, -1.2, 0], color=ORANGE, stroke_width=6)
        pl = T("recording", 24, ORANGE).move_to([-5.0, -2.4, 0])
        one = T("one cell", 28, BLUE).move_to([-2.2, -2.9, 0])
        self.play(FadeIn(cell), Create(pip), FadeIn(pl), FadeIn(one), run_time=0.4)
        t1 = chip("light response", YELLOW, 28).move_to([3.8, 1.3, 0])
        t2 = chip("shape", PURPLE, 28).move_to([3.8, -0.2, 0])
        t3 = chip("RNA", TEAL, 28).move_to([3.8, -1.7, 0])
        l1 = Line(cell[-1].get_end(), t1.get_left(), color=YELLOW, stroke_width=3)
        l2 = DashedLine(cell[-1].get_end(), t2.get_left(), color=PURPLE, stroke_width=3)
        l3 = DashedLine(cell[-1].get_end(), t3.get_left(), color=TEAL, stroke_width=3)
        self.at("same cell")
        self.play(Create(l1), FadeIn(t1), run_time=0.6)
        self.at("In some cells")
        self.play(Create(l2), FadeIn(t2), Create(l3), FadeIn(t3), run_time=0.9)
        subs = T("in some cells", 24, GREY).move_to([3.0, 0.65, 0]).shift(RIGHT * 2.2)
        self.finish_part = None
        self.at("isolated mouse retina")
        stage1 = VGroup(cell, pip, pl, one, t1, t2, t3, l1, l2, l3)
        self.play(FadeOut(stage1), run_time=0.5)
        n1 = VGroup(M("1,859", 54, ORANGE), T("ganglion cells recorded", 28, ORANGE)).arrange(DOWN, buff=0.2).move_to([-3.4, 0.8, 0])
        n2 = VGroup(M("42", 54, ORANGE), T("functional types", 28, ORANGE)).arrange(DOWN, buff=0.2).move_to([3.6, 0.8, 0])
        ar = arr([-1.2, 0.8, 0], [1.2, 0.8, 0], ORANGE)
        self.play(FadeIn(n1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("sorted into")
        self.play(GrowArrow(ar), FadeIn(n2, shift=LEFT * 0.2), run_time=0.7)
        frame = Rectangle(width=9.0, height=0.7, stroke_color=GREY, stroke_width=3).move_to([0, -1.6, 0])
        fill = Rectangle(width=9.0 * 0.89, height=0.7, stroke_width=0, fill_color=ORANGE, fill_opacity=0.5)
        fill.align_to(frame, LEFT).align_to(frame, UP)
        pct = M("89%", 36, ORANGE).move_to(fill)
        cov = T("estimated share of the ganglion cell population covered by the 42 types", 24, GREY).move_to([0, -2.4, 0])
        self.at("estimated to cover")
        self.play(Create(frame), FadeIn(cov), run_time=0.5)
        self.play(GrowFromEdge(fill, LEFT), FadeIn(pct), run_time=1.0)
        self.at("not always one to one")
        self.play(FadeOut(VGroup(n1, n2, ar, frame, fill, pct, cov)), run_time=0.5)
        top = T("three sustained ON\ndirection-selective types", 28, YELLOW).move_to([-3.4, 2.2, 0])
        ts = [chip(f"type {i}", YELLOW, 32).move_to([-3.4, 0.6 - 1.4 * (i - 1), 0]) for i in (1, 2, 3)]
        cl = chip("RNA cluster C10", TEAL, 34).move_to([3.7, -0.8, 0])
        ars = [arr(t.get_right(), cl.get_left() + UP * (0.25 * (1 - i)), YELLOW, 4) for i, t in zip((0, 1, 2), ts)]
        self.at("Three sustained")
        self.play(FadeIn(top), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in ts], lag_ratio=0.3), run_time=1.2)
        self.at("single cluster")
        self.play(FadeIn(cl), LaggedStart(*[GrowArrow(a) for a in ars], lag_ratio=0.2), run_time=1.2)
        eq = M("3 types : 1 cluster", 34, TEXT).move_to([0.2, -3.0, 0])
        self.play(FadeIn(eq), run_time=0.5)
        self.finish()


# -------------------------------------------------------------------------------------------
class S05Anatomy(SpokenScene):
    def construct(self):
        head = T("Electron microscopy: counted by shape", 34, PURPLE, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.at("Electron microscopy")
        self.play(Write(head), run_time=1.0)
        base_y, unit = -2.7, 0.08
        b47 = Rectangle(width=2.0, height=47 * unit, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3)
        b47.move_to([-2.6, base_y + 47 * unit / 2, 0])
        b35 = Rectangle(width=2.0, height=35 * unit, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.65)
        b35.move_to([2.6, base_y + 35 * unit / 2, 0])
        n47 = M("47", 44, PURPLE).next_to(b47, UP, buff=0.15)
        n35 = M("35", 44, PURPLE).next_to(b35, UP, buff=0.15)
        l47 = T("anatomical clusters", 24, PURPLE).next_to(b47, DOWN, buff=0.15)
        l35 = T("supported lower bound", 24, PURPLE).next_to(b35, DOWN, buff=0.15)
        note = T("one mouse retinal patch", 26, GREY).move_to([0, 2.5, 0])
        self.at("In one mouse")
        self.play(FadeIn(note), run_time=0.5)
        self.at("anatomical clusters")
        self.play(GrowFromEdge(b47, DOWN), FadeIn(n47), FadeIn(l47), run_time=0.9)
        self.at("supported lower bound")
        self.play(GrowFromEdge(b35, DOWN), FadeIn(n35), FadeIn(l35), run_time=0.9)
        self.at("counts clusters")
        self.play(Indicate(VGroup(b47, n47), color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("they could support")
        self.play(Indicate(VGroup(b35, n35), color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("four numbers")
        self.play(FadeOut(VGroup(b47, b35, n47, n35, l47, l35, note)), run_time=0.5)
        cards = VGroup(card("≥ 32", "imaging", YELLOW, 40), card("≥ 35", "electron microscopy", PURPLE, 40),
                       card("42", "same-cell recording", ORANGE, 40), card("46", "sequencing", TEAL, 40))
        cards.arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to([0, 0.9, 0])
        fit(cards, max_w=12.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.2), run_time=1.2)
        self.at("Each reflects")
        cs = [chip(w, TEXT, 32) for w in ("a method", "a preparation", "a resolution")]
        row = VGroup(*cs).arrange(RIGHT, buff=0.5).move_to([0, -1.9, 0])
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.5)
        self.at("preparation")
        self.play(FadeIn(cs[1], shift=UP * 0.2), run_time=0.5)
        self.at("resolution")
        self.play(FadeIn(cs[2], shift=UP * 0.2), run_time=0.5)
        self.finish()


# -------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        head = T("When does a cluster become a type?", 34, GOLD, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.at("So when does")
        self.play(Write(head), run_time=1.0)
        cr = chip("response", YELLOW, 32).move_to([-3.4, 1.9, 0])
        cs = chip("shape", PURPLE, 32).move_to([-5.2, -1.6, 0])
        ce = chip("expression", TEAL, 32).move_to([-1.5, -1.6, 0])
        ring = Circle(radius=0.75, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.15).move_to([-3.4, 0.0, 0])
        tl = T("type", 30, GOLD, weight=BOLD).move_to(ring)
        ls = [Line(a, b, color=GOLD, stroke_width=3) for a, b in ((cr.get_bottom(), ring.get_top()), (cs.get_top() + RIGHT * 0.4, ring.get_center() + 0.75 * normalize(cs.get_top() + RIGHT * 0.4 - ring.get_center())), (ce.get_top() + LEFT * 0.4, ring.get_center() + 0.75 * normalize(ce.get_top() + LEFT * 0.4 - ring.get_center())))]
        self.at("response")
        self.play(FadeIn(cr, shift=DOWN * 0.2), FadeIn(cs, shift=UP * 0.2), FadeIn(ce, shift=UP * 0.2), run_time=0.9)
        self.at("tied to one another")
        self.play(*[Create(l) for l in ls], run_time=0.7)
        self.play(FadeIn(ring, scale=0.6), FadeIn(tl), run_time=0.6)
        self.bring_to_back_lines = None
        # mosaic: hexagon tiling
        hexes = VGroup()
        s = 0.5
        for q in range(-2, 3):
            for r in range(-2, 3):
                x = s * np.sqrt(3) * (q + r / 2)
                y = s * 1.5 * r
                if abs(x) < 2.0 and abs(y) < 1.6:
                    h = RegularPolygon(6, radius=s * 0.98, start_angle=PI / 2, stroke_color=GREEN, stroke_width=3,
                                       fill_color=GREEN, fill_opacity=0.2).move_to([x + 3.6, y - 0.3, 0])
                    hexes.add(h)
        mlab = T("mosaic: territories tile the retina", 26, GREEN).move_to([3.6, -2.7, 0])
        self.at("mosaic")
        self.play(LaggedStart(*[FadeIn(h, scale=0.7) for h in hexes], lag_ratio=0.05), FadeIn(mlab), run_time=1.5)
        gen = chip("genetic access", GREY, 28).move_to([3.6, 2.5, 0])
        gen[0].set_stroke(opacity=0.8)
        self.at("genetic access")
        self.play(FadeIn(gen, shift=DOWN * 0.2), run_time=0.6)
        self.at("more than one method")
        self.play(Indicate(ring, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what a number counted."
