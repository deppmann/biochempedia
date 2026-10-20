"""Copy first, then divide: the cell cycle and mitosis  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = DNA / chromosomes / sister chromatids (labelled bars, never a molecule)
  GOLD   = the centromere (little dot joining two sister chromatids)
  PURPLE = nuclear envelope / nucleus
  YELLOW = spindle fibers and the pinching ring (what moves things)
  GREEN  = new cells, new wall (cell plate), new tissue
  TEAL   = things that cross the cell membrane (oxygen, food, wastes)
  RED    = the problem: less membrane for the inside (falling ratio), "not a rest"
  ORANGE = an open question
  GREY   = membranes, cell outlines, tissue, de-emphasized
  TEXT   = stage names (prophase, ...), neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bar(h=1.3, w=0.18, color=BLUE):
    return RoundedRectangle(corner_radius=min(0.07, w / 2.5), width=w, height=h, stroke_color=color,
                            stroke_width=2, fill_color=color, fill_opacity=0.85)


def chrom(center, copied=True, h=1.3, w=0.18, gap=0.08, dot_r=0.09):
    """A chromosome as labelled blocks: one bar, or two sister-chromatid bars joined by a gold dot."""
    cx, cy = center[0], center[1]
    if copied:
        off = (w + gap) / 2
        l = bar(h, w).move_to([cx - off, cy, 0])
        r = bar(h, w).move_to([cx + off, cy, 0])
        dot = Dot([cx, cy, 0], radius=dot_r, color=GOLD).set_z_index(3)
        g = VGroup(l, r, dot)
        g.l, g.r, g.dot = l, r, dot
    else:
        l = bar(h, w).move_to([cx, cy, 0])
        g = VGroup(l)
        g.l, g.r, g.dot = l, None, None
    g.set_z_index(2)
    return g


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell_shape(w, h, center, color=GREY):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color,
                   fill_opacity=0.07).move_to(center)


def nucleus(r, center, dashed=False):
    c = Circle(radius=r, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.10).move_to(center)
    return c


def stage_chip(text):
    return chip(text, TEXT, size=32).move_to([0, 3.0, 0])


class S00Title(TitleCard):
    LESSON = "The Cell Cycle and Mitosis"
    TITLE = "Copy first, then divide"


# ---------------------------------------------------------------------------------------------
class S01Cut(SpokenScene):
    """a cut fills with new cells; an onion root tip adds cells; two open questions."""

    def construct(self):
        # --- left: skin with a cut ---------------------------------------------------------
        skin = RoundedRectangle(corner_radius=0.12, width=5.2, height=2.8, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.28).move_to([-3.3, 1.2, 0])
        gap = Rectangle(width=1.7, height=1.5, stroke_color=RED, stroke_width=3, fill_color=BG,
                        fill_opacity=1).move_to([-3.3, 1.75, 0])
        skin_lbl = T("a cut in skin", 28, TEXT).move_to([-3.3, -0.5, 0])
        self.at("A cut on your finger")
        self.play(FadeIn(skin), FadeIn(gap), FadeIn(skin_lbl), run_time=0.8)
        new = VGroup()
        for i in range(5):
            for j in range(3):
                new.add(Square(0.32, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.55)
                        .move_to([-3.3 - 0.64 + i * 0.32, 1.75 - 0.32 + j * 0.32, 0]))
        new.move_to(gap.get_center())
        self.at("closes in roughly")
        self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in new], lag_ratio=0.1), run_time=2.2)
        wk = T("closes in roughly a week or a little longer", 24, GREY).move_to([-3.3, -1.05, 0])
        self.play(FadeIn(wk), run_time=0.5)

        # --- right: onion root tip ---------------------------------------------------------
        root = RoundedRectangle(corner_radius=0.7, width=1.9, height=3.6, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.28).move_to([3.4, 1.2, 0])
        root_lbl = T("an onion root tip", 28, TEXT).move_to([3.4, -0.9, 0])
        self.at("Near the tip of an onion root")
        self.play(FadeIn(root), FadeIn(root_lbl), run_time=0.8)
        tipcells = VGroup()
        for i in range(3):
            for j in range(3):
                tipcells.add(Square(0.34, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.55)
                             .move_to([3.4 - 0.4 + i * 0.4, -0.35 + j * 0.4, 0]))
        self.at("cells divide")
        self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in tipcells], lag_ratio=0.12), run_time=1.6)
        down = arr([5.0, 1.9, 0], [5.0, -0.2, 0], YELLOW)
        soil = T("deeper into the soil", 24, GREY).move_to([5.0, -0.25, 0]).shift(LEFT * 0.0)
        self.at("pushes deeper")
        self.play(GrowArrow(down), run_time=0.7)
        self.play(root.animate.shift(DOWN * 0.0), run_time=0.1)
        self.play(FadeOut(wk), run_time=0.3)

        # --- the two questions -------------------------------------------------------------
        self.at("adds new cells")
        self.play(Indicate(new, color=GREEN, scale_factor=1.05), Indicate(tipcells, color=GREEN, scale_factor=1.05),
                  run_time=0.9)
        q1 = chip("more cells, not bigger cells?", ORANGE, size=28).move_to([-3.4, -2.45, 0])
        q2 = chip("a full set of instructions in each?", ORANGE, size=26).move_to([3.4, -2.45, 0])
        self.at("Why add more cells")
        self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.7)
        self.at("full set of instructions")
        self.play(FadeIn(q2, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Small(SpokenScene):
    """model cubes of side 2 and side 4: surface, volume, ratio 3 -> 1.5."""

    def construct(self):
        note = T("model cube (drawn flat), from geometry", 26, GREY).move_to([0, 3.1, 0])
        sq_a = Square(1.8, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to([-3.2, -0.1, 0])
        side_a = T("side 2", 26, TEXT).move_to(sq_a)
        # --- things cross the membrane --------------------------------------------------------
        self.at("Oxygen, food")
        sq_a.move_to([0, 0.5, 0])
        self.play(Create(sq_a), run_time=0.7)
        ox = arr([-3.2, 0.9, 0], [-1.05, 0.9, 0], TEAL)
        fd = arr([-3.2, 0.1, 0], [-1.05, 0.1, 0], TEAL)
        ws = arr([1.05, 0.5, 0], [3.2, 0.5, 0], TEAL)
        ox_l = T("oxygen", 26, TEAL).move_to([-4.2, 0.9, 0])
        fd_l = T("food", 26, TEAL).move_to([-4.2, 0.1, 0])
        ws_l = T("wastes", 26, TEAL).move_to([4.2, 0.5, 0])
        self.play(GrowArrow(ox), FadeIn(ox_l), run_time=0.6)
        self.play(GrowArrow(fd), FadeIn(fd_l), run_time=0.5)
        self.at("wastes")
        self.play(GrowArrow(ws), FadeIn(ws_l), run_time=0.6)
        mem_l = T("cell membrane", 26, GREY).move_to([0, -1.1, 0])
        self.at("cell membrane")
        self.play(FadeIn(mem_l), run_time=0.5)

        # --- model a cell as a cube ---------------------------------------------------------
        self.at("Model a cell as a cube")
        self.play(FadeOut(VGroup(ox, fd, ws, ox_l, fd_l, ws_l, mem_l)), FadeIn(note), run_time=0.6)
        self.at("sides of two units")
        sq_a_t = Square(1.8, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to([-3.2, -0.1, 0])
        self.play(Transform(sq_a, sq_a_t), FadeIn(side_a), run_time=0.8)
        rows_a = VGroup(M("surface 24 square units", 24, TEAL), M("volume 8 cubic units", 24, BLUE),
                        M("surface ÷ volume = 3", 24, TEXT)).arrange(DOWN, buff=0.16).move_to([-3.2, -2.3, 0])
        self.at("has a surface of")
        self.play(FadeIn(rows_a[0], shift=UP * 0.1), run_time=0.5)
        self.at("and a volume")
        self.play(FadeIn(rows_a[1], shift=UP * 0.1), run_time=0.5)

        # --- double the side ----------------------------------------------------------------
        sq_b = Square(3.6, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to([2.7, 0.8, 0])
        side_b = T("side 4", 26, TEXT).move_to(sq_b)
        self.at("Double the sides")
        self.play(TransformFromCopy(sq_a, sq_b), FadeIn(side_b), run_time=1.0)
        rows_b = VGroup(M("surface 96 square units", 24, TEAL), M("volume 64 cubic units", 24, BLUE),
                        M("surface ÷ volume = 1.5", 24, RED)).arrange(DOWN, buff=0.16).move_to([2.7, -2.3, 0])
        self.at("The surface grows")
        self.play(FadeIn(rows_b[0], shift=UP * 0.1), run_time=0.5)
        self.at("the volume to")
        self.play(FadeIn(rows_b[1], shift=UP * 0.1), run_time=0.5)

        # --- the ratio ----------------------------------------------------------------------
        self.at("Surface for each unit")
        self.play(FadeIn(rows_a[2], shift=UP * 0.1), run_time=0.5)
        self.at("falls from")
        self.play(FadeIn(rows_b[2], shift=UP * 0.1), rows_a[2].animate.set_color(TEXT), run_time=0.6)
        verdict = T("a bigger cell: less membrane for its inside", 28, RED).move_to([0, 3.1, 0])
        self.at("A bigger cell has less membrane")
        self.play(ReplacementTransform(note, verdict), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Copy(SpokenScene):
    """cell cycle strip; interphase is not a rest; S phase doubles each chromosome."""

    def construct(self):
        cell = cell_shape(6.4, 3.6, [0, -0.7, 0])
        nuc = nucleus(1.4, [0, -0.7, 0])
        c1 = chrom([-0.8, -0.7, 0], copied=False)
        c2 = chrom([0.8, -0.7, 0], copied=False)
        self.at("The cell cycle")
        self.play(Create(cell), FadeIn(nuc), FadeIn(c1), FadeIn(c2), run_time=1.0)
        newlbl = T("a new cell", 28, TEXT).move_to([0, 1.55, 0])
        self.play(FadeIn(newlbl), run_time=0.5)

        # strip
        g1 = chip("G1: grows", GREEN, 28)
        s = chip("S: copies DNA", BLUE, 28)
        g2 = chip("G2: gets ready", TEXT, 28)
        strip = VGroup(g1, s, g2).arrange(RIGHT, buff=0.5).move_to([0, 2.5, 0])
        brace_y = 3.1
        line = Line([strip.get_left()[0], brace_y, 0], [strip.get_right()[0], brace_y, 0], color=GREY, stroke_width=4)
        inter = T("interphase", 30, TEXT, weight=BOLD).move_to([-1.6, 3.4, 0])
        nr = T("not a rest", 30, RED).move_to([1.7, 3.4, 0])
        self.at("Interphase")
        self.play(ReplacementTransform(newlbl, inter), Create(line), run_time=0.8)
        self.at("is not a rest")
        self.play(FadeIn(nr, shift=LEFT * 0.2), run_time=0.5)
        self.at("the cell grows")
        self.play(FadeIn(g1), cell.animate.scale(1.12), run_time=1.2)
        self.at("In S phase")
        self.play(FadeIn(s), run_time=0.5)
        t1 = chrom([-0.8, -0.7, 0], copied=True)
        t2 = chrom([0.8, -0.7, 0], copied=True)
        self.at("it copies")
        self.play(ReplacementTransform(c1, t1), ReplacementTransform(c2, t2), run_time=1.3)
        self.at("gets ready")
        self.play(FadeIn(g2), run_time=0.5)
        self.play(Indicate(g2, color=TEXT, scale_factor=1.06), run_time=0.8)

        # zoom in on one copied chromosome
        big = chrom([0, -0.5, 0], True, 2.3, 0.55, 0.5, 0.2)
        l1 = T("chromosome", 28, BLUE).move_to([-3.7, -0.5, 0])
        a1 = arr([-2.6, -0.5, 0], [-0.9, -0.5, 0], BLUE, w=3, tip=0.18)
        self.at("Each copied chromosome")
        self.play(FadeOut(cell), FadeOut(nuc), FadeOut(t2), ReplacementTransform(t1, big), run_time=1.0)
        self.play(FadeIn(l1), GrowArrow(a1), run_time=0.6)
        br = Brace(VGroup(big.l, big.r), UP, color=BLUE, buff=0.12)
        l2 = T("sister chromatids", 28, BLUE).next_to(br, UP, buff=0.12)
        self.at("sister chromatids")
        self.play(GrowFromCenter(br), FadeIn(l2), run_time=0.7)
        l3 = T("centromere", 28, GOLD).move_to([0, -2.9, 0])
        a3 = arr([0, -2.5, 0], [0, -0.78, 0], GOLD, w=3, tip=0.18)
        self.at("the centromere")
        self.play(FadeIn(l3), GrowArrow(a3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Mitosis(SpokenScene):
    """one model cell, two chromosomes: prophase, metaphase, anaphase, telophase."""

    def construct(self):
        cy = -0.4
        cell = cell_shape(8.2, 5.0, [0, cy, 0])
        nuc = nucleus(1.5, [0, cy, 0])
        c1 = chrom([-0.8, cy, 0], True, 1.3, 0.18)
        c2 = chrom([0.8, cy, 0], True, 1.3, 0.18)
        note = T("model cell, 2 chromosomes shown", 22, GREY).move_to([0, -3.3, 0])
        self.add(cell, nuc, c1, c2)
        self.at("Mitosis divides the nucleus")
        stage = stage_chip("mitosis: the nucleus divides")
        self.play(FadeIn(stage), FadeIn(note), run_time=0.7)

        # --- prophase -------------------------------------------------------------------
        self.at("In prophase")
        nstage = stage_chip("prophase")
        self.play(ReplacementTransform(stage, nstage), run_time=0.5)
        stage = nstage
        self.at("coil up")
        self.play(Transform(c1, chrom([-0.8, cy, 0], True, 0.95, 0.3, 0.04)),
                  Transform(c2, chrom([0.8, cy, 0], True, 0.95, 0.3, 0.04)), run_time=1.0)
        env_lbl = T("nuclear envelope", 24, PURPLE).move_to([0, -2.4, 0])
        self.play(FadeIn(env_lbl), run_time=0.4)
        self.at("breaks down")
        self.play(FadeOut(nuc), FadeOut(env_lbl), run_time=1.0)

        # --- metaphase ------------------------------------------------------------------
        self.at("In metaphase")
        nstage = stage_chip("metaphase")
        self.play(ReplacementTransform(stage, nstage), run_time=0.5)
        stage = nstage
        self.at("spindle fibers")
        edge_l, edge_r = np.array([-4.0, cy, 0]), np.array([4.0, cy, 0])

        def fiber(edge, target):
            f = Line(edge, target.get_center(), color=YELLOW, stroke_width=4)
            f.set_z_index(1)
            f.add_updater(lambda m, e=edge, t=target: m.put_start_and_end_on(e, t.get_center()))
            return f

        # the chromosomes line up first (still in prophase positions), fibers appear from both ends
        fibs = VGroup(fiber(edge_l, c1.l), fiber(edge_r, c1.r), fiber(edge_l, c2.l), fiber(edge_r, c2.r))
        fl = T("spindle fibers", 26, YELLOW).move_to([-1.6, 1.15, 0])
        self.play(FadeIn(fibs), FadeIn(fl), c1.animate.move_to([0, cy + 0.75, 0]), c2.animate.move_to([0, cy - 0.75, 0]),
                  run_time=1.6)
        self.at("line the chromosomes up")
        self.wait(0.1)
        # a plate line to show the middle
        mid = DashedLine([0, cy - 2.2, 0], [0, cy + 2.2, 0], color=GREY, stroke_width=2).set_z_index(0)
        self.play(FadeIn(mid), run_time=0.5)

        # --- anaphase -------------------------------------------------------------------
        self.at("In anaphase")
        nstage = stage_chip("anaphase")
        self.play(ReplacementTransform(stage, nstage), FadeOut(fl), FadeOut(mid), run_time=0.5)
        stage = nstage
        self.at("sister chromatids separate")
        y1, y2 = cy + 0.75, cy - 0.75
        self.play(FadeOut(c1.dot), FadeOut(c2.dot),
                  c1.l.animate.shift(LEFT * 0.25), c1.r.animate.shift(RIGHT * 0.25),
                  c2.l.animate.shift(LEFT * 0.25), c2.r.animate.shift(RIGHT * 0.25), run_time=0.8)
        self.at("opposite ends")
        self.play(c1.l.animate.move_to([-2.7, y1, 0]), c2.l.animate.move_to([-2.7, y2, 0]),
                  c1.r.animate.move_to([2.7, y1, 0]), c2.r.animate.move_to([2.7, y2, 0]), run_time=2.0)

        # --- telophase ------------------------------------------------------------------
        self.at("In telophase")
        nstage = stage_chip("telophase")
        self.play(ReplacementTransform(stage, nstage), FadeOut(fibs), run_time=0.6)
        stage = nstage
        envL = Ellipse(width=1.5, height=3.0, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE,
                       fill_opacity=0.10).move_to([-2.7, cy, 0])
        envR = envL.copy().move_to([2.7, cy, 0])
        self.at("a new nuclear")
        self.play(FadeIn(envL), FadeIn(envR), run_time=1.0)
        lbl = T("a new nuclear envelope\naround each set", 26, PURPLE, line_spacing=0.9).move_to([0, cy, 0])
        self.at("around each set")
        self.play(FadeIn(lbl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Split(SpokenScene):
    """cytokinesis: animal furrow, plant cell plate."""

    def construct(self):
        A, B = 2.6, 1.8
        p = ValueTracker(0.0)

        def body():
            pp = p.get_value()

            def f(t):
                x = A * np.cos(t)
                y = B * np.sin(t) * (1 - pp * np.exp(-(x / (0.38 * A)) ** 2))
                return np.array([x, y, 0])
            return ParametricFunction(f, t_range=[0, TAU], stroke_color=GREY, stroke_width=4,
                                      fill_color=GREY, fill_opacity=0.07).shift([-3.4, 0.2, 0])

        animal = always_redraw(body)
        nL = nucleus(0.6, [-4.4, 0.2, 0])
        nR = nucleus(0.6, [-2.4, 0.2, 0])
        setL = VGroup(chrom([-4.55, 0.2, 0], False, 0.7, 0.14), chrom([-4.25, 0.2, 0], False, 0.7, 0.14))
        setR = VGroup(chrom([-2.55, 0.2, 0], False, 0.7, 0.14), chrom([-2.25, 0.2, 0], False, 0.7, 0.14))
        a_title = T("animal cell", 30, TEXT).move_to([-3.4, 2.5, 0])
        cyto = T("cytoplasm", 24, GREY).move_to([-3.4, -0.85, 0])

        self.at("Cytokinesis then")
        head = chip("cytokinesis", TEXT, 32).move_to([0, 3.1, 0])
        self.play(FadeIn(head), FadeIn(a_title), FadeIn(animal), FadeIn(nL), FadeIn(nR), FadeIn(setL), FadeIn(setR),
                  run_time=1.0)
        self.at("divides the cytoplasm")
        self.play(FadeIn(cyto), run_time=0.5)

        self.at("In an animal cell")
        self.play(Indicate(a_title, color=TEXT, scale_factor=1.08), run_time=0.6)
        ring_a = arr([-3.4, 2.4, 0], [-3.4, 1.4, 0], YELLOW, w=6)
        ring_b = arr([-3.4, -2.0, 0], [-3.4, -1.0, 0], YELLOW, w=6)
        ring_l = T("ring", 26, YELLOW).move_to([-2.6, 2.1, 0])
        self.at("a ring at the middle")
        self.play(FadeOut(a_title), GrowArrow(ring_a), GrowArrow(ring_b), FadeIn(ring_l), run_time=0.8)
        self.at("pinches the membrane")
        self.play(FadeOut(cyto), FadeOut(ring_l), p.animate.set_value(0.7), run_time=1.6)
        furrow = T("furrow", 28, YELLOW).move_to([-3.4, -2.6, 0])
        self.at("a furrow")
        self.play(FadeIn(furrow), p.animate.set_value(0.97), run_time=1.0)
        self.at("until the cell splits")
        left = Ellipse(width=2.7, height=2.9, stroke_color=GREEN, stroke_width=4, fill_color=GREY,
                       fill_opacity=0.07).move_to([-4.85, 0.2, 0])
        right = left.copy().move_to([-1.95, 0.2, 0])
        self.play(FadeOut(animal), FadeOut(ring_a), FadeOut(ring_b), FadeIn(left), FadeIn(right),
                  nL.animate.shift(LEFT * 0.45), setL.animate.shift(LEFT * 0.45),
                  nR.animate.shift(RIGHT * 0.45), setR.animate.shift(RIGHT * 0.45), run_time=1.0)
        two = T("two cells", 28, GREEN).move_to([-3.4, -2.6, 0])
        self.play(ReplacementTransform(furrow, two), run_time=0.5)

        # --- plant ---------------------------------------------------------------------
        p_title = T("plant cell", 30, TEXT).move_to([3.5, 2.5, 0])
        wall = Rectangle(width=4.8, height=3.4, stroke_color=GREY, stroke_width=10, fill_color=GREY,
                         fill_opacity=0.07).move_to([3.5, 0.2, 0])
        pL = nucleus(0.6, [2.4, 0.2, 0])
        pR = nucleus(0.6, [4.6, 0.2, 0])
        sL = VGroup(chrom([2.25, 0.2, 0], False, 0.7, 0.14), chrom([2.55, 0.2, 0], False, 0.7, 0.14))
        sR = VGroup(chrom([4.45, 0.2, 0], False, 0.7, 0.14), chrom([4.75, 0.2, 0], False, 0.7, 0.14))
        self.at("A plant cell has")
        self.play(FadeIn(p_title), FadeIn(wall), FadeIn(pL), FadeIn(pR), FadeIn(sL), FadeIn(sR), run_time=0.9)
        stiff = T("stiff wall", 28, GREY).move_to([3.5, -2.6, 0])
        self.play(FadeIn(stiff), run_time=0.5)
        self.at("cannot pinch")
        nopinch = T("cannot pinch", 28, RED).move_to([3.5, -2.6, 0])
        self.play(ReplacementTransform(stiff, nopinch), run_time=0.5)
        self.at("A cell plate")
        plate = Line([3.5, 0.2, 0], [3.5, 0.2, 0], color=GREEN, stroke_width=10)
        plate_t = Line([3.5, 1.9, 0], [3.5, -1.5, 0], color=GREEN, stroke_width=10)
        plate_l = T("cell plate", 28, GREEN).move_to([3.5, -2.6, 0])
        self.play(FadeOut(nopinch), FadeIn(plate_l), Transform(plate, plate_t), run_time=2.0)
        self.at("becomes a new wall")
        newwall = T("becomes a new wall", 28, GREEN).move_to([3.5, -2.6, 0])
        self.play(FadeOut(plate_l), FadeIn(newwall), plate.animate.set_stroke(width=14), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """two answers: ratio 3 -> 1.5, and copy first then share out."""

    def construct(self):
        q1 = chip("Why more cells,\nnot bigger ones?", ORANGE, 26).move_to([-3.4, 2.85, 0])
        q2 = chip("How does each new cell\nget a full copy?", ORANGE, 26).move_to([3.4, 2.85, 0])
        self.at("why more cells")
        self.play(FadeIn(q1), run_time=0.6)

        s1 = Square(1.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([-4.7, 0.0, 0])
        s2 = Square(2.8, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([-2.1, 0.7, 0])
        r1 = M("3", 34, TEXT).next_to(s1, DOWN, buff=0.3).align_to(s1, DOWN).shift(DOWN * 0.45)
        r2 = M("1.5", 34, RED).next_to(s2, DOWN, buff=0.3)
        r1.move_to([-4.7, -1.3, 0])
        r2.move_to([-2.1, -1.3, 0])
        lab = T("surface ÷ volume (model cubes)", 24, GREY).move_to([-3.4, -1.8, 0])
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.6)
        self.play(FadeIn(r1), FadeIn(lab), run_time=0.4)
        self.play(FadeIn(r2), run_time=0.4)
        self.at("A bigger cell")
        ans1 = T("one reason: a bigger cell has\nless membrane for its inside", 26, RED, line_spacing=0.9).move_to([-3.4, -2.6, 0])
        nc = T("real cells are not cubes", 22, GREY).move_to([-3.4, -3.35, 0])
        self.play(FadeIn(ans1), FadeIn(nc), Indicate(s2, color=RED, scale_factor=1.05), run_time=0.9)

        # --- second question -------------------------------------------------------------
        self.at("how does each")
        self.play(FadeIn(q2), run_time=0.6)
        cell = Circle(radius=1.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([3.4, 0.4, 0])
        c = chrom([3.4, 0.4, 0], copied=False, h=1.2, w=0.22)
        self.play(FadeIn(cell), FadeIn(c), run_time=0.6)
        cp = chrom([3.4, 0.4, 0], copied=True, h=1.2, w=0.22)
        step = T("1  copy first", 26, BLUE).move_to([3.4, -1.7, 0])
        self.at("copies its")
        self.play(ReplacementTransform(c, cp), FadeIn(step), run_time=1.0)
        c = cp
        self.at("Mitosis then shares")
        step2 = T("2  mitosis shares it out", 26, GREEN).move_to([3.4, -2.35, 0])
        self.play(FadeOut(c.dot), FadeIn(step2), run_time=0.4)
        cl = Circle(radius=1.1, stroke_color=GREEN, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([2.2, 0.4, 0])
        cr = Circle(radius=1.1, stroke_color=GREEN, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([4.6, 0.4, 0])
        self.play(FadeOut(cell), FadeIn(cl), FadeIn(cr), c.l.animate.move_to([2.2, 0.4, 0]),
                  c.r.animate.move_to([4.6, 0.4, 0]), run_time=1.4)
        same = T("same DNA, usually", 26, TEXT).move_to([3.4, -3.0, 0])
        self.at("usually have the same")
        self.play(FadeIn(same), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Copy the DNA first, then share it out."
