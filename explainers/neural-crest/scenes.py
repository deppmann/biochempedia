"""Neural crest: where crest cells may not go  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = neural crest cells (the thing that moves)
  BLUE   = Eph B receptor on the crest cell
  RED    = ephrin B and the caudal half it keeps closed (keep out)
  GREEN  = rostral half (the way in)
  TEAL   = dorsal root ganglia (what the cells build)
  GREY   = neural tube, somite outlines, control protein, labels
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

CX = [-5.2 + 2.0 * i for i in range(5)]      # somite centres
TUBE_Y = 2.5
ROW_Y = -1.6


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def crest_cell(r=0.17):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.9)


def make_tube():
    return RoundedRectangle(corner_radius=0.3, width=10.0, height=0.9, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.2).move_to([-1.2, TUBE_Y, 0])


def tube_label(txt="neural tube"):
    return T(txt, 24, GREY).move_to([5.2, TUBE_Y - 0.35, 0])


def top_cells(n=9):
    xs = np.linspace(-5.7, 3.3, n)
    return VGroup(*[crest_cell().move_to([x, TUBE_Y + 0.27, 0]) for x in xs])


def pop(group, color, k=1.15):
    return LaggedStart(*[Indicate(m, color=color, scale_factor=k) for m in group], lag_ratio=0.1)


def lane_dots(cx, rostral=True):
    x0 = cx - 0.475 if rostral else cx + 0.475
    return [crest_cell(0.15).move_to([x0 + (j - 1) * 0.34, TUBE_Y + 0.27, 0]) for j in range(3)]


def somite(cx):
    outer = Rectangle(width=1.9, height=3.8, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([cx, -0.4, 0])
    scl = Rectangle(width=1.9, height=2.9, stroke_width=0, fill_color=TEXT, fill_opacity=0.08).move_to([cx, -0.85, 0])
    div = DashedLine([cx, 0.6, 0], [cx, -2.3, 0], color=GREY, stroke_width=2, dash_length=0.12)
    return VGroup(outer, scl, div)


def half(cx, rostral=True, color=GREEN, op=0.2):
    x = cx - 0.475 if rostral else cx + 0.475
    return Rectangle(width=0.95, height=2.9, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([x, -0.85, 0])


def ganglion(x, y=ROW_Y, w=1.0, h=0.75, color=TEAL):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45).move_to([x, y, 0])


def qmark(x, y):
    q = T("?", 56, GOLD, weight=BOLD)
    back = Circle(radius=0.42, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, q).move_to([x, y, 0])


def tab(color, w=0.34, h=0.5):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.55)


class S00Title(TitleCard):
    LESSON = "The Neural Crest: Cells That Leave Home"
    TITLE = "Where Crest Cells May Not Go"


# ---------------------------------------------------------------------------------------------
class S01Row(SpokenScene):
    """The puzzle: crest at the top of the tube, a repeating row of ganglia, question marks between."""

    def construct(self):
        tube = make_tube()
        self.at("spinal cord")
        self.play(Create(tube), run_time=1.0)
        gx = [c - 0.5 for c in CX]
        gang = VGroup(*[ganglion(x) for x in gx])
        glab = T("dorsal root\nganglia", 24, TEAL, line_spacing=0.8).move_to([5.2, ROW_Y, 0])
        self.at("dorsal root ganglia")
        self.play(LaggedStart(*[GrowFromCenter(g) for g in gang], lag_ratio=0.25), FadeIn(glab), run_time=1.6)
        self.at("neat repeating row")
        self.play(pop(gang, TEAL, 1.25), run_time=1.2)
        self.at("No central")
        self.wait(0.2)
        cells = top_cells()
        clab = T("neural crest", 24, YELLOW).move_to([5.2, TUBE_Y + 0.4, 0])
        self.at("neural crest")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cells], lag_ratio=0.1), FadeIn(clab), run_time=1.2)
        self.at("top of the")
        tl = tube_label()
        self.play(FadeIn(tl), run_time=0.5)
        lines = VGroup(*[DashedLine([x, TUBE_Y - 0.5, 0], [x, ROW_Y + 0.5, 0], color=GREY, stroke_width=2) for x in gx])
        qs = VGroup(*[qmark(x, 0.45) for x in gx])
        self.at("So what turns")
        self.play(Create(lines), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.2), run_time=1.0)
        self.at("into a row")
        self.play(pop(qs, GOLD, 1.25), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Leave(SpokenScene):
    """EMT: a cell in a sheet loosens, rounds up and crawls away."""

    def construct(self):
        n = 7
        w, h = 1.25, 3.4
        cells = VGroup()
        for i in range(n):
            col = YELLOW if i in (2, 3, 4) else GREY
            r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=col, stroke_width=3,
                                 fill_color=col, fill_opacity=0.28).move_to([(i - 3) * w, 0.9, 0])
            cells.add(r)
        edge = T("the tube's top edge", 26, GREY).move_to([0, 3.15, 0])
        self.at("Crest cells begin")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cells], lag_ratio=0.08), run_time=1.4)
        self.play(FadeIn(edge), run_time=0.5)
        sheet_lbl = T("cell in a sheet", 26, GREY).move_to([-2.3, -1.3, 0])
        self.at("loosen their grip")
        self.play(*[cells[i].animate.shift(RIGHT * 0.2 * (i - 3)) for i in range(n)], run_time=1.2)
        mid = cells[3]
        self.at("Then they crawl away")
        circ = Circle(radius=0.6, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5).move_to(mid)
        self.play(ReplacementTransform(mid, circ), run_time=0.7)
        path = CubicBezier(circ.get_center(), np.array([-0.2, -1.6, 0]), np.array([1.6, -2.1, 0]), np.array([3.8, -2.1, 0]))
        self.play(MoveAlongPath(circ, path), run_time=1.6)
        free_lbl = T("free cell", 26, YELLOW).next_to(circ, RIGHT, buff=0.3)
        self.at("from a cell in a sheet")
        self.play(FadeIn(sheet_lbl), cells[2].animate.set_stroke(width=6), run_time=0.7)
        self.at("to a free cell")
        self.play(FadeIn(free_lbl), run_time=0.6)
        emt = chip("epithelial-to-mesenchymal transition", GOLD, size=28)
        emt.move_to([-1.9, -3.1, 0])
        self.at("epithelial to mesenchymal transition")
        self.play(FadeIn(emt, shift=UP * 0.2), run_time=0.8)
        short = chip("EMT", GOLD, size=34).move_to(emt)
        self.at("shorten it")
        self.play(ReplacementTransform(emt, short), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def embryo_labels_right():
    soma = VGroup(Line([3.8, 1.2, 0], [4.4, 1.2, 0], color=GREY, stroke_width=2), T("somite", 24, GREY).move_to([5.3, 1.2, 0]))
    scl = VGroup(Line([3.8, -0.8, 0], [4.4, -0.8, 0], color=GREY, stroke_width=2), T("sclerotome", 24, GREY).move_to([5.4, -0.8, 0]))
    return soma, scl


class S03Route(SpokenScene):
    """Somite blocks beside the tube; rostral and caudal halves; the stream goes through the rostral halves."""

    def construct(self):
        tube = make_tube()
        tl = tube_label()
        lanes = [d for c in CX for d in lane_dots(c)]
        self.add(tube, tl, *lanes)
        self.at("In the chick trunk")
        self.wait(0.2)
        blocks = VGroup(*[somite(c) for c in CX])
        soma, scl = embryo_labels_right()
        self.at("through the somites")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.25) for b in blocks], lag_ratio=0.15), run_time=1.5)
        self.at("Somites are")
        self.play(FadeIn(soma), run_time=0.5)
        self.at("will form vertebrae")
        self.play(FadeIn(scl), run_time=0.5)
        ros = VGroup(*[half(c, True) for c in CX])
        cau = VGroup(*[half(c, False, GREY, 0.2) for c in CX])
        rl = T("rostral", 22, GREEN).move_to([CX[0] - 0.475, -2.7, 0])
        cl = T("caudal", 22, GREY).move_to([CX[0] + 0.475, -3.15, 0])
        self.at("front half")
        self.play(FadeIn(ros), FadeIn(rl), run_time=0.7)
        self.at("back half")
        self.play(FadeIn(cau), FadeIn(cl), run_time=0.7)
        # the stream: one cell per rostral half drops in, several lanes
        self.at("Crest cells pass only")
        anims = []
        for k, c in enumerate(CX):
            for j, dy in enumerate([0.8, -0.2, -1.2]):
                anims.append(lanes[3 * k + j].animate.move_to([c - 0.475 + (j - 1) * 0.34, dy, 0]))
        self.play(LaggedStart(*anims, lag_ratio=0.04), run_time=2.0)
        self.at("rostral half")
        self.play(pop(ros, GREEN, 1.04), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Keepout(SpokenScene):
    """Close-up of the boundary: Eph B tabs meet ephrin B tabs and the cell is pushed back."""

    def construct(self):
        ros = Rectangle(width=6.7, height=5.2, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12)
        ros.move_to([-2.35, -0.15, 0])
        cau = Rectangle(width=4.4, height=5.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
        cau.move_to([3.2, -0.15, 0])      # x from 1.0 to 5.4
        rlab = T("rostral half", 26, GREEN).move_to([-2.35, 3.05, 0])
        clab = T("caudal half", 26, GREY).move_to([3.2, 3.05, 0])
        self.play(FadeIn(ros), FadeIn(cau), FadeIn(rlab), FadeIn(clab), run_time=0.8)
        # crest cell with receptor tabs
        body = Circle(radius=0.95, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.45)
        rec = VGroup()
        for a in (-40, -13, 13, 40):
            t = tab(BLUE)
            ang = np.deg2rad(a)
            t.move_to([0.95 * np.cos(ang) + 0.1, 0.95 * np.sin(ang), 0]).rotate(ang)
            rec.add(t)
        cell = VGroup(body, rec).move_to([-3.3, 0.2, 0])
        rlab2 = T("Eph B receptor", 26, BLUE).move_to([-3.4, -1.85, 0])
        self.at("keeps them out")
        self.play(cau.animate.set_stroke(RED).set_fill(RED, 0.2), clab.animate.set_color(RED), run_time=0.8)
        self.at("receptor called")
        self.play(FadeIn(body, scale=0.8), run_time=0.6)
        self.play(FadeIn(rec), FadeIn(rlab2), run_time=0.6)
        eph = VGroup()
        for y in (1.5, 0.5, -0.5, -1.5):
            t = tab(RED, 0.4, 0.5).move_to([0.85, y + 0.2, 0])
            eph.add(t)
        elab = T("ephrin B", 26, RED).move_to([3.4, 0.2, 0])
        self.at("signal on their surface")
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.2) for t in eph], lag_ratio=0.15), FadeIn(elab), run_time=1.0)
        self.at("only when cells touch")
        self.wait(0.2)
        self.at("When a crest cell touches")
        # contact: receptor tabs reach ephrin tabs (cell right edge at x = -3.3+0.95+0.4 ~ 0.0 -> move +0.95)
        self.play(cell.animate.shift(RIGHT * 2.6), FadeOut(rlab2), run_time=1.2)
        self.at("repels it")
        flash = Flash(np.array([0.65, 0.2, 0]), color=RED, flash_radius=0.7, num_lines=10, line_length=0.3)
        rep = Arrow([0.3, 1.9, 0], [-1.1, 1.9, 0], color=RED, stroke_width=7, buff=0)
        self.play(flash, GrowArrow(rep), run_time=0.8)
        self.at("pushed away")
        away = T("repelled", 28, RED).move_to([-3.2, 2.1, 0])
        self.play(cell.animate.shift(LEFT * 2.8 + DOWN * 0.6), FadeIn(away), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Stripes(SpokenScene):
    """A stripe dish: cells avoid ephrin B stripes; soluble ephrin B removes the avoidance."""

    def construct(self):
        SW, NS = 1.35, 8
        x0 = -SW * NS / 2
        yc, hh = 0.1, 4.0
        stripes = VGroup()
        for i in range(NS):
            red = (i % 2 == 0)
            col = RED if red else GREY
            stripes.add(Rectangle(width=SW, height=hh, stroke_color=col, stroke_width=1.5, fill_color=col,
                                  fill_opacity=0.38 if red else 0.22).move_to([x0 + SW / 2 + i * SW, yc, 0]))
        frame = Rectangle(width=SW * NS + 0.2, height=hh + 0.2, stroke_color=TEXT, stroke_width=2, fill_opacity=0).move_to([0, yc, 0])
        case = T("Crest cells on stripes", 30, TEXT).move_to([0, 3.0, 0])
        grey_x = [x0 + SW / 2 + i * SW for i in range(NS) if i % 2 == 1]
        all_x = [x0 + SW / 2 + i * SW for i in range(NS)]
        self.at("in a dish")
        self.play(Create(frame), FadeIn(case), run_time=0.8)
        self.at("alternating stripes")
        self.play(LaggedStart(*[FadeIn(s) for s in stripes], lag_ratio=0.1), run_time=1.2)
        l_e = T("ephrin B", 24, RED).move_to([all_x[0], yc - hh / 2 - 0.45, 0])
        l_c = T("control protein", 24, GREY).move_to([all_x[3] + 0.5, yc - hh / 2 - 0.45, 0])
        self.at("and a control")
        self.play(FadeIn(l_e), FadeIn(l_c), run_time=0.6)
        rng = random.Random(7)
        N = 16
        start = [(rng.uniform(x0 + 0.3, -x0 - 0.3), rng.uniform(yc - hh / 2 + 0.35, yc + hh / 2 - 0.35)) for _ in range(N)]
        cells = VGroup(*[crest_cell(0.17).move_to([x, y, 0]) for x, y in start])
        self.at("plated trunk crest cells")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cells], lag_ratio=0.05), run_time=1.0)
        # case A result: cells go to the grey stripes
        tgt = []
        for k, (x, y) in enumerate(start):
            gx = min(grey_x, key=lambda g: abs(g - x))
            tgt.append((gx + rng.uniform(-0.4, 0.4), y))
        self.at("The cells avoided")
        self.play(*[c.animate.move_to([tx, ty, 0]) for c, (tx, ty) in zip(cells, tgt)], run_time=2.0)
        resA = T("cells avoid the ephrin B stripes", 28, YELLOW).move_to([0, -3.15, 0])
        self.play(FadeIn(resA), run_time=0.5)
        sceptic = T("just a poor surface?", 28, GOLD).move_to([0, 3.0, 0])
        self.at("could say the stripe")
        self.play(FadeOut(resA), ReplacementTransform(case, sceptic), run_time=0.6)
        self.wait(0.3)
        # case B: fresh dish, soluble ephrin B
        caseB = T("Same stripes, plus soluble ephrin B", 30, TEXT).move_to([0, 3.0, 0])
        self.at("So they added soluble")
        self.play(ReplacementTransform(sceptic, caseB),
                  *[c.animate.move_to([x, y, 0]) for c, (x, y) in zip(cells, start)], run_time=1.0)
        dots = VGroup(*[Circle(radius=0.08, stroke_color=TEXT, stroke_width=1, fill_color=RED, fill_opacity=1).move_to(
            [rng.uniform(x0 + 0.1, -x0 - 0.1), rng.uniform(yc - hh / 2 + 0.1, yc + hh / 2 - 0.1), 0]) for _ in range(45)])
        self.at("to the medium")
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02), run_time=1.0)
        self.at("free in the liquid")
        self.play(LaggedStart(*[Indicate(d, color=TEXT, scale_factor=1.9) for d in dots], lag_ratio=0.02), run_time=1.0)
        resB = T("no avoidance of the stripes", 28, YELLOW).move_to([0, -3.15, 0])
        self.at("That blocked the avoidance")
        drift = [(x + rng.uniform(-0.25, 0.25), y + rng.uniform(-0.2, 0.2)) for x, y in start]
        self.play(*[c.animate.move_to([x, y, 0]) for c, (x, y) in zip(cells, drift)], FadeIn(resB), run_time=1.2)
        # finish: Eph B meets ephrin B
        eph = chip("Eph B", BLUE, size=44)
        ephr = chip("ephrin B", RED, size=44)
        pair = VGroup(eph, ephr).arrange(RIGHT, buff=1.6).move_to([0, 0.5, 0])
        link = Arrow(ephr.get_left(), eph.get_right(), color=TEXT, buff=0.12, stroke_width=6)
        need = T("the avoidance needs this signal", 32, TEXT).move_to([0, -1.2, 0])
        self.at("The avoidance needs")
        self.play(*[FadeOut(m) for m in (stripes, frame, cells, dots, l_e, l_c, caseB, resB)], run_time=0.7)
        self.play(FadeIn(pair), GrowFromCenter(link), run_time=0.8)
        self.play(FadeIn(need), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """Back in the embryo: cells go through rostral halves, are turned back at caudal halves, gather into a row."""

    def construct(self):
        tube = make_tube()
        tl = tube_label()
        lanes = [d for c in CX for d in lane_dots(c)]
        tries = [crest_cell(0.16).move_to([c + 0.475, TUBE_Y + 0.27, 0]) for c in CX]
        top = VGroup(*lanes, *tries)
        blocks = VGroup(*[somite(c) for c in CX])
        ros = VGroup(*[half(c, True) for c in CX])
        cau = VGroup(*[half(c, False, RED, 0.22) for c in CX])
        self.at("Back in the embryo")
        self.play(FadeIn(tube), FadeIn(tl), FadeIn(top), run_time=0.6)
        self.play(FadeIn(blocks), FadeIn(ros), FadeIn(cau), run_time=0.9)
        movers = lanes
        entering = []
        for k, c in enumerate(CX):
            for j, dy in enumerate([0.8, -0.2, -1.2]):
                entering.append(movers[3 * k + j].animate.move_to([c - 0.475 + (j - 1) * 0.34, dy, 0]))
        self.at("Crest cells enter")
        self.play(LaggedStart(*entering, lag_ratio=0.04), run_time=1.8)
        self.at("not the caudal half")
        self.play(*[t.animate.move_to([c + 0.475, 0.9, 0]) for t, c in zip(tries, CX)], run_time=0.9)
        xs = VGroup(*[VGroup(Line([c + 0.2, 0.55, 0], [c + 0.75, 0.0, 0], color=TEXT, stroke_width=6),
                             Line([c + 0.2, 0.0, 0], [c + 0.75, 0.55, 0], color=TEXT, stroke_width=6)) for c in CX])
        self.play(*[t.animate.move_to([c - 0.2, 1.1, 0]) for t, c in zip(tries, CX)], FadeIn(xs), run_time=0.8)
        self.play(FadeOut(xs), FadeOut(VGroup(*tries)), run_time=0.4)
        # gather into ganglia
        gang = VGroup(*[ganglion(c - 0.475, y=-0.8, w=0.8, h=1.9) for c in CX])
        glab = T("dorsal root\nganglia", 24, TEAL, line_spacing=0.8).move_to([5.2, -0.8, 0])
        self.at("dorsal root ganglia are segmented")
        self.play(*[FadeOut(m) for m in movers],
                  LaggedStart(*[GrowFromCenter(g) for g in gang], lag_ratio=0.15), FadeIn(glab), run_time=1.6)
        self.at("Where crest cells may not go")
        self.play(pop(cau, RED, 1.04), run_time=1.2)
        self.at("what they build")
        self.play(pop(gang, TEAL, 1.12), run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Where crest cells may not go helps shape what they build."
