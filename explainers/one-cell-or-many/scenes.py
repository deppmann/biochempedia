"""One Cell Does It All  (Biochemistrypedia high school Biology explainer, Unit 2)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = a cell (its outline) and the answer
  TEAL   = cilia / movement
  ORANGE = food and food vacuoles
  BLUE   = water and the contractile vacuole
  YELLOW = the thing named right now (a job, a specialized cell, a lit gene)
  PURPLE = DNA and genes
  RED    = an exception (the mature red blood cell loses its nucleus)
  GREY   = outlines, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

TEAL2 = "#3FB8C0"
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def paramecium(cx, cy, w=4.4, h=2.0, color=GREEN):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color,
                   fill_opacity=0.12).move_to([cx, cy, 0])


def small_cells(n_cols, n_rows, r=0.2, gap=0.12, color=GREEN):
    cells = VGroup(*[Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.18)
                     for _ in range(n_cols * n_rows)])
    cells.arrange_in_grid(n_rows, n_cols, buff=gap)
    return cells


def label(text, size=26, color=GREY):
    return T(text, size, color)


class S00Title(TitleCard):
    LESSON = "One Cell or Many"
    TITLE = "One Cell Does It All"


# ---------------------------------------------------------------------------------------------
class S01Slipper(SpokenScene):
    def construct(self):
        cell = paramecium(-3.6, 0.5, 4.6, 2.2)
        name = label("Paramecium: one cell", 28, GREEN).next_to(cell, DOWN, buff=0.3)
        self.play(GrowFromCenter(cell), FadeIn(name), run_time=0.9)
        self.at("swims")
        chips = VGroup(*[chip(t, YELLOW, size=26) for t in ["swims", "catches food", "pumps out extra water", "splits in two"]])
        chips.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([3.3, 0.9, 0])
        self.play(FadeIn(chips[0], shift=LEFT * 0.2), run_time=0.4)
        self.at("catches food")
        self.play(FadeIn(chips[1], shift=LEFT * 0.2), run_time=0.4)
        self.at("pumps out")
        self.play(FadeIn(chips[2], shift=LEFT * 0.2), run_time=0.4)
        self.at("splits in two")
        self.play(FadeIn(chips[3], shift=LEFT * 0.2), run_time=0.4)
        self.at("your body")
        grid = small_cells(8, 4, r=0.22, gap=0.1).move_to([3.3, 0.9, 0])
        gl = label("your body: trillions of cells", 26, GREEN).next_to(grid, DOWN, buff=0.3)
        self.play(FadeOut(chips), FadeIn(grid, lag_ratio=0.03), FadeIn(gl), run_time=1.1)
        self.at("survive alone")
        q = T("How can one cell survive alone?", 38, YELLOW, font=TITLE_FONT).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02One(SpokenScene):
    def construct(self):
        head = T("unicellular = one cell", 34, GREEN, font=TITLE_FONT).to_edge(UP, buff=0.5)
        cell = paramecium(0, -0.2, 6.2, 3.0)
        self.at("unicellular organism")
        self.play(Write(head), GrowFromCenter(cell), run_time=0.9)

        # cilia: short ticks around the outline
        ticks = VGroup()
        for th in np.linspace(0, 2 * np.pi, 40, endpoint=False):
            p = cell.point_at_angle(th)
            d = np.array([np.cos(th) / 3.1, np.sin(th) / 1.5, 0])
            d = d / np.linalg.norm(d)
            ticks.add(Line(p, p + d * 0.26, color=TEAL2, stroke_width=3.5))
        cl = label("cilia", 28, TEAL2).move_to([-5.2, 1.8, 0])
        cl_line = Line([-4.6, 1.65, 0], cell.point_at_angle(np.pi * 0.78) + np.array([-0.2, 0.2, 0]), color=TEAL2, stroke_width=2)
        self.at("with cilia")
        self.play(FadeIn(ticks, lag_ratio=0.03), FadeIn(cl), Create(cl_line), run_time=0.9)
        self.at("beat together")
        self.play(Indicate(ticks, color=TEAL2, scale_factor=1.06), run_time=1.2)

        # food vacuole
        fv = Circle(radius=0.38, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.25).move_to([-1.3, -0.5, 0])
        fl = label("food vacuole", 28, ORANGE).move_to([-4.8, -2.6, 0])
        fl_line = Line([-3.6, -2.45, 0], fv.get_center() + np.array([-0.35, -0.2, 0]), color=ORANGE, stroke_width=2)
        food = Dot([-3.9, -1.2, 0], radius=0.1, color=ORANGE)
        self.at("food vacuoles")
        self.play(FadeIn(food), run_time=0.3)
        self.play(food.animate.move_to(fv.get_center()), FadeIn(fv), FadeIn(fl), Create(fl_line), run_time=1.0)

        # water in, contractile vacuole
        water = VGroup(*[arr([x, 2.1 - 0.35 * 0, 0], [x * 0.85, 1.4, 0], BLUE, w=4, tip=0.16) for x in [1.2, 2.4, 3.5]])
        wl = label("water moves in (osmosis)", 26, BLUE).move_to([4.2, 2.45, 0])
        wl.set_x(min(wl.get_x(), 12.6 / 2 - wl.width / 2))
        water.shift(DOWN * 0.15)
        cv = Circle(radius=0.34, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to([1.5, 0.2, 0])
        cvl = label("contractile vacuole", 28, BLUE).move_to([4.2, -2.3, 0])
        cvl_line = Line([2.4, -2.15, 0], cv.get_center() + np.array([0.3, -0.25, 0]), color=BLUE, stroke_width=2)
        self.at("water keeps moving in")
        self.play(FadeIn(water, lag_ratio=0.2), FadeIn(wl), run_time=0.9)
        self.at("contractile vacuole")
        self.play(FadeIn(cv), FadeIn(cvl), Create(cvl_line), run_time=0.6)
        self.at("fills with")
        self.play(cv.animate.scale(1.9).set_fill(BLUE, 0.55), run_time=1.0)
        self.at("squeezes it out")
        out = arr(cv.get_center() + np.array([0.5, -0.1, 0]), [4.2, -0.5, 0], BLUE, w=4, tip=0.16)
        outl = label("water out", 26, BLUE).next_to(out, RIGHT, buff=0.15)
        self.play(cv.animate.scale(1 / 1.9).set_fill(BLUE, 0.15), GrowArrow(out), FadeIn(outl), run_time=0.7)

        # fission
        self.at("binary fission")
        fis = T("binary fission", 34, YELLOW, font=TITLE_FONT).to_edge(DOWN, buff=0.45)
        self.play(FadeOut(VGroup(ticks, cl, cl_line, fv, fl, fl_line, food, water, wl, cv, cvl, cvl_line, out, outl)),
                  Write(fis), run_time=0.8)
        self.at("one cell divides")
        c1 = paramecium(-1.9, -0.2, 3.4, 2.4)
        c2 = paramecium(1.9, -0.2, 3.4, 2.4)
        self.play(Transform(cell, c1), FadeIn(c2, shift=LEFT * 0.4), run_time=1.6)
        t2 = label("two cells", 28, GREEN).next_to(VGroup(c1, c2), UP, buff=0.35)
        self.play(FadeIn(t2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Many(SpokenScene):
    def construct(self):
        self.at("multicellular organism")
        head = T("multicellular = many cells", 34, GREEN, font=TITLE_FONT).to_edge(UP, buff=0.5)
        row = small_cells(9, 1, r=0.28, gap=0.22).move_to([0, 1.5, 0])
        self.play(Write(head), FadeIn(row, lag_ratio=0.1), run_time=1.2)
        self.at("specialized cell")
        sp = row[4]
        self.play(sp.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.4).scale(1.35), run_time=0.6)
        spl = label("specialized cell: a structure that suits one job", 28, YELLOW).next_to(row, DOWN, buff=0.35)
        self.play(FadeIn(spl), run_time=0.5)
        self.at("Similar cells")
        self.play(FadeOut(spl), FadeOut(row), run_time=0.5)
        names = ["cell", "tissue", "organ", "organ system"]
        ex = ["", "muscle", "the heart", "circulatory system"]
        chips = VGroup(*[chip(n, GREEN, size=30) for n in names]).arrange(RIGHT, buff=0.9).move_to([0, -0.3, 0])
        fit(chips, max_w=12.2)
        arrows = VGroup(*[arr(chips[i].get_right(), chips[i + 1].get_left(), GREY) for i in range(3)])
        self.play(FadeIn(chips[0]), run_time=0.3)
        self.play(GrowArrow(arrows[0]), FadeIn(chips[1], shift=RIGHT * 0.2), run_time=0.6)
        exl = [None] + [label(ex[i], 28, YELLOW).next_to(chips[i], DOWN, buff=0.4) for i in (1, 2, 3)]
        self.at("such as muscle")
        self.play(FadeIn(exl[1]), run_time=0.4)
        self.at("Several tissues")
        self.play(GrowArrow(arrows[1]), FadeIn(chips[2], shift=RIGHT * 0.2), run_time=0.6)
        self.at("such as the heart")
        self.play(FadeIn(exl[2]), run_time=0.4)
        self.at("Related organs")
        self.play(GrowArrow(arrows[2]), FadeIn(chips[3], shift=RIGHT * 0.2), run_time=0.6)
        self.at("circulatory system")
        self.play(FadeIn(exl[3]), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Shapes(SpokenScene):
    def construct(self):
        head = T("structure fits job", 34, GREEN, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=0.8)
        Y = 1.2
        # --- nerve cell (not to scale) ---
        cx = -4.5
        body = Circle(radius=0.5, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.18).move_to([cx - 0.9, Y, 0])
        axon = Line(body.get_right(), [cx + 1.5, Y, 0], color=GREEN, stroke_width=5)
        nerve = VGroup(body, axon)
        n1 = label("nerve cell", 30, YELLOW).move_to([cx, -0.3, 0])
        n2 = label("long extension", 24, GREY).next_to(n1, DOWN, buff=0.2)
        n2b = label("carries signals far", 24, GREY).next_to(n2, DOWN, buff=0.12)
        n3 = label("some human ones: about 1 m", 24, GREY).next_to(n2b, DOWN, buff=0.12)
        self.at("nerve cell")
        self.play(Create(nerve), run_time=0.8)
        self.play(FadeIn(n1), run_time=0.3)
        self.at("long extension")
        self.play(FadeIn(n2), FadeIn(n2b), run_time=0.3)
        self.at("reach about")
        self.play(FadeIn(n3), run_time=0.3)
        # --- red blood cell ---
        rx = -0.1
        disc = Ellipse(width=1.8, height=1.4, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.18).move_to([rx, Y, 0])
        dent = Ellipse(width=0.7, height=0.5, stroke_color=GREEN, stroke_width=3, fill_color=BG, fill_opacity=0.9).move_to([rx, Y, 0])
        r1 = label("red blood cell", 30, YELLOW).move_to([rx, -0.3, 0])
        r2 = label("small, flexible, dented", 24, GREY).next_to(r1, DOWN, buff=0.2)
        r3 = label("bends through narrow vessels", 24, GREY).next_to(r2, DOWN, buff=0.12)
        self.at("red blood cell")
        self.play(GrowFromCenter(disc), FadeIn(dent), FadeIn(r1), run_time=0.7)
        self.at("small, flexible")
        self.play(FadeIn(r2), run_time=0.3)
        self.at("bends through narrow vessels")
        self.play(FadeIn(r3), run_time=0.3)
        # --- root hair cell (soil block with hair tube) ---
        hx = 4.8
        soil = Rectangle(width=2.2, height=1.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([hx, Y - 0.3, 0])
        cellbody = Rectangle(width=1.3, height=0.6, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.18).move_to([hx, Y + 0.6 + 0.3, 0])
        rc = label("root cell", 22, GREEN).move_to(cellbody)
        tube = Rectangle(width=0.22, height=0.9, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.18)
        tube.move_to([hx, Y + 0.6 - 0.45, 0])
        sl = label("soil", 22, GREY).move_to([hx + 0.7, Y - 0.7, 0])
        h1 = label("root hair cell", 30, YELLOW).move_to([hx, -0.3, 0])
        h2 = label("long tube touching soil", 24, GREY).next_to(h1, DOWN, buff=0.2)
        h3 = label("water enters", 24, GREY).next_to(h2, DOWN, buff=0.12)
        self.at("root hair cell")
        self.play(FadeIn(soil), FadeIn(sl), FadeIn(cellbody), FadeIn(rc), GrowFromEdge(tube, UP), FadeIn(h1), run_time=0.9)
        self.at("long tube")
        self.play(FadeIn(h2), run_time=0.3)
        self.at("where water enters")
        self.play(FadeIn(h3), run_time=0.3)
        ns = label("sketches, not to scale", 22, GREY).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ns), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
def gene_bar(cx, cy, n=6, size=0.36):
    blocks = VGroup(*[Square(size, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE, fill_opacity=0.12) for _ in range(n)])
    blocks.arrange(RIGHT, buff=0.06).move_to([cx, cy, 0])
    return blocks


class S05Genes(SpokenScene):
    def construct(self):
        lx, rx, cy = -3.4, 3.4, 0.2
        muscle = RoundedRectangle(corner_radius=0.3, width=5.2, height=4.2, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.1).move_to([lx, cy - 0.2, 0])
        rbc = RoundedRectangle(corner_radius=0.3, width=5.2, height=3.8, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.1).move_to([rx, cy, 0])
        mn = label("muscle cell", 28, GREEN).next_to(muscle, UP, buff=0.2)
        rn = label("red blood cell in the making", 28, GREEN).next_to(rbc, UP, buff=0.2)
        self.at("different instructions")
        self.play(FadeIn(muscle), FadeIn(rbc), FadeIn(mn), FadeIn(rn), run_time=0.8)

        def nucleus(cx):
            box = RoundedRectangle(corner_radius=0.25, width=3.4, height=1.7, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, cy + 0.65, 0])
            bar = gene_bar(cx, cy + 0.65)
            dna = label("DNA", 28, PURPLE).next_to(bar, UP, buff=0.15)
            nl = label("nucleus", 22, GREY).next_to(bar, DOWN, buff=0.15)
            return box, bar, dna, nl
        b1, bar1, dna1, nl1 = nucleus(lx)
        b2, bar2, dna2, nl2 = nucleus(rx)
        extra = VGroup(*[Circle(radius=0.24, stroke_color=GREY, stroke_width=3) for _ in range(2)])
        extra[0].move_to([lx - 2.0, cy - 1.8, 0]); extra[1].move_to([lx + 2.0, cy - 1.8, 0])
        many = label("many nuclei", 22, GREY).move_to([lx, cy - 1.8, 0])
        self.at("with a nucleus")
        self.play(FadeIn(VGroup(b1, nl1, extra, many)), FadeIn(VGroup(b2, nl2)), run_time=0.6)
        self.at("essentially the same")
        self.play(FadeIn(bar1), FadeIn(bar2), FadeIn(dna1), FadeIn(dna2), run_time=0.8)
        same = T("the same DNA", 34, PURPLE, font=TITLE_FONT).to_edge(DOWN, buff=0.45)
        self.play(Write(same), run_time=0.7)
        self.at("gene expression")
        ge = T("gene expression", 34, YELLOW, font=TITLE_FONT).to_edge(UP, buff=0.45)
        note = label("blocks = genes (schematic)", 24, PURPLE).to_edge(DOWN, buff=0.4)
        self.play(FadeOut(same), Write(ge), FadeIn(note), run_time=0.7)
        self.at("A muscle cell uses")
        self.play(bar1[1].animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), run_time=0.5)
        g1 = VGroup(*[label(line, 24, YELLOW) for line in
                     ["genes for proteins that", "slide past each other", "to shorten the cell"]]).arrange(DOWN, buff=0.08).move_to([lx, cy - 0.85, 0])
        self.play(FadeIn(g1), run_time=0.4)
        self.at("genes for hemoglobin")
        self.play(bar2[4].animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), run_time=0.5)
        g2 = label("genes for hemoglobin", 24, YELLOW).move_to([rx, cy - 0.85, 0])
        self.play(FadeIn(g2), run_time=0.4)
        self.at("exception")
        self.play(FadeOut(VGroup(b2, bar2, dna2, nl2, g2)), rn.animate.become(label("mature red blood cell", 28, RED).move_to(rn)), run_time=0.8)
        nn = label("no nucleus", 34, RED).move_to([rx, cy, 0])
        self.play(FadeIn(nn), rbc.animate.set_stroke(RED), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        q = T("How can one cell survive alone?", 36, YELLOW, font=TITLE_FONT).to_edge(UP, buff=0.45)
        self.play(Write(q), run_time=0.9)
        # left: one cell with every job
        cell = paramecium(-3.5, 0.2, 5.6, 3.5)
        title_l = label("one cell: every job inside", 26, GREEN).next_to(cell, DOWN, buff=0.35)
        jobs = VGroup(*[T(t, 24, c) for t, c in [("cilia", TEAL2), ("food vacuoles", ORANGE),
                                                 ("contractile vacuole", BLUE), ("divides", YELLOW)]])
        jobs.arrange(DOWN, buff=0.2).move_to(cell)
        self.play(GrowFromCenter(cell), FadeIn(title_l), run_time=0.9)
        self.at("structures for every job")
        self.play(FadeIn(jobs, lag_ratio=0.2), run_time=1.4)
        # right: specialized cells share jobs
        self.at("shares those jobs")
        cells = VGroup(*[chip(t, GREEN, size=24) for t in ["nerve cell", "muscle cell", "red blood cell", "root hair cell"]])
        cells.arrange_in_grid(2, 2, buff=0.3).move_to([3.7, 0.2, 0])
        title_r = label("many cells: jobs shared out", 26, GREEN).next_to(cells, DOWN, buff=0.45)
        title_r.align_to(title_l, DOWN)
        self.play(FadeIn(cells, lag_ratio=0.25), FadeIn(title_r), run_time=1.4)
        self.at("shapes fit")
        self.play(Indicate(cells, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.at("different genes")
        d = T("nearly the same DNA, different genes", 36, PURPLE, font=TITLE_FONT).to_edge(DOWN, buff=0.45)
        self.play(Write(d), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Nearly the same DNA, but each kind uses different genes."
