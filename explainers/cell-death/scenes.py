"""Cell death and clearance: ask every dying cell two questions  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = phosphatidylserine (the lipid heads)
  BLUE   = annexin V (the lipid question and its readout)
  ORANGE = propidium iodide and the stained DNA (the membrane question and its readout)
  GREEN  = apoptotic cell / the clearest apoptotic signal
  RED    = leak, secondary necrosis, the double-positive puzzle
  GREY   = membranes, outlines, labels, the necrosis-from-the-start cell
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

# ---- stage geometry for the membrane scenes (s02 to s04) ----
MX0, MX1 = -6.2, 2.2
LIP_X = np.linspace(-5.4, 1.4, 8)
BLOB_X = [LIP_X[0], LIP_X[2], LIP_X[4]]
HOLES = [-0.057, 0.914]
HOLE_W = 0.46
PI_X = [LIP_X[1], LIP_X[3], -0.057, 0.914]
OUT_Y, IN_Y = 0.19, -0.19     # leaflet bar centres
BAR_H = 0.34
DNA_C = np.array([-2.0, -2.0, 0])


def bar_piece(x0, x1, y):
    return RoundedRectangle(corner_radius=0.06, width=x1 - x0, height=BAR_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.4).move_to([(x0 + x1) / 2, y, 0])


def bars_full():
    return VGroup(bar_piece(MX0, MX1, OUT_Y), bar_piece(MX0, MX1, IN_Y))


def bars_holed():
    edges = [MX0]
    for h in HOLES:
        edges += [h - HOLE_W / 2, h + HOLE_W / 2]
    edges.append(MX1)
    g = VGroup()
    for y in (OUT_Y, IN_Y):
        for i in range(0, len(edges), 2):
            g.add(bar_piece(edges[i], edges[i + 1], y))
    return g


def lipid_head(x, y):
    return Circle(radius=0.22, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([x, y, 0])


def annexin_blob(x, y):
    return RoundedRectangle(corner_radius=0.2, width=0.66, height=0.56, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.45).move_to([x, y, 0])


def pi_dot(x, y):
    return Circle(radius=0.17, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.95).move_to([x, y, 0])


def dna_blob(lit=False):
    c = ORANGE if lit else GREY
    box = RoundedRectangle(corner_radius=0.5, width=3.0, height=1.05, stroke_color=c, stroke_width=3.5,
                           fill_color=c, fill_opacity=0.35 if lit else 0.1).move_to(DNA_C)
    lab = T("DNA", 26, c if lit else GREY).move_to(box)
    return VGroup(box, lab)


def readout(name, sign, color):
    on = sign == "+"
    c = color if on else GREY
    label = T(f"{name}  {'+' if on else '−'}", 28, c, weight=BOLD if on else NORMAL)
    box = RoundedRectangle(corner_radius=0.14, width=3.0, height=0.8, stroke_color=c, stroke_width=3,
                           fill_color=c, fill_opacity=0.2 if on else 0.05)
    return VGroup(box, label.move_to(box))


def legend_row(mark, text, color):
    return VGroup(mark, T(text, 22, color)).arrange(RIGHT, buff=0.22)


def stage_labels():
    a = T("outside the cell", 24, GREY).move_to([-4.2, 3.1, 0])
    b = T("inside the cell", 24, GREY).move_to([-4.6, -3.1, 0])
    return VGroup(a, b)


def panel_items(readA="−", readB="−"):
    ra = readout("annexin V", readA, BLUE).move_to([4.5, -0.9, 0])
    rb = readout("PI", readB, ORANGE).move_to([4.5, -2.0, 0])
    return ra, rb


def legend():
    r1 = legend_row(lipid_head(0, 0).scale(0.9), "phosphatidylserine", YELLOW)
    r2 = legend_row(annexin_blob(0, 0).scale(0.8), "annexin V", BLUE)
    r3 = legend_row(pi_dot(0, 0), "propidium iodide", ORANGE)
    g = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    g.move_to([4.5, 2.0, 0])
    return g, r1, r2, r3


def membrane_stage(lipids_out=False, holed=False, lit=False, blobs_bound=False):
    """Rebuild the membrane stage in the same place for each scene."""
    bars = bars_holed() if holed else bars_full()
    ly = 0.58 if lipids_out else -0.58
    lips = VGroup(*[lipid_head(x, ly) for x in LIP_X])
    blobs = VGroup(*[annexin_blob(x, 1.08 if blobs_bound else 2.0) for x in BLOB_X])
    dots = VGroup(*[pi_dot(x, 2.5) for x in PI_X])
    dna = dna_blob(lit)
    return bars, lips, blobs, dots, dna


# ---- plot helpers (s05, s06) ----
PC = np.array([-1.5, 0.3, 0])
QW, QH = 3.6, 2.9
COUNTS = {"BL": "5,800", "BR": "2,900", "TR": "1,000", "TL": "300"}


def qcentre(k):
    dx = -1 if k in ("BL", "TL") else 1
    dy = -1 if k in ("BL", "BR") else 1
    return PC + np.array([dx * QW / 2, dy * QH / 2, 0])


def quad_box(k):
    tint = {"BL": GREY, "BR": GREEN, "TR": RED, "TL": ORANGE}[k]
    return Rectangle(width=QW, height=QH, stroke_color=GREY, stroke_width=3, fill_color=tint,
                     fill_opacity=0.10).move_to(qcentre(k))


def plot_frame():
    boxes = {k: quad_box(k) for k in COUNTS}
    g = VGroup(*boxes.values())
    xl = T("annexin V  −", 24, BLUE).move_to(PC + np.array([-QW / 2, -QH - 0.4, 0]))
    xr = T("annexin V  +", 24, BLUE).move_to(PC + np.array([QW / 2, -QH - 0.4, 0]))
    yt = T("PI  +", 24, ORANGE).move_to(PC + np.array([-QW - 0.7, QH / 2, 0]))
    yb = T("PI  −", 24, ORANGE).move_to(PC + np.array([-QW - 0.7, -QH / 2, 0]))
    return boxes, VGroup(g, xl, xr, yt, yb)


def count_mob(k, opacity=1.0):
    c = qcentre(k)
    m = M(COUNTS[k], 42, TEXT).move_to(c + np.array([0.3, -0.35, 0]))
    return m.set_opacity(opacity)


def cell_dot(color, text=None, size=0.26):
    d = Circle(radius=size, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.55)
    if text:
        return VGroup(d, T(text, 24, TEXT, weight=BOLD).move_to(d))
    return d


def dot_legend(color, text, y, mark_text=None):
    mark = cell_dot(color, mark_text, size=0.22)
    lab = T(text, 22, color)
    g = VGroup(mark, lab).arrange(RIGHT, buff=0.2)
    g.move_to([4.5, y, 0])
    g.set_x(2.95 + g.width / 2)
    return g


def dot_pos(k, dx=0.0, dy=0.0):
    return qcentre(k) + np.array([-1.15 + dx, 0.85 + dy, 0])


class S00Title(TitleCard):
    LESSON = "Cell death and clearance"
    TITLE = "Ask every dying cell two questions"


# ---------------------------------------------------------------------------------------------
class S01Ask(SpokenScene):
    def construct(self):
        C = np.array([-3.4, 0.0, 0])
        cell = Circle(radius=2.8, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.08).move_to(C)
        nuc = Circle(radius=0.95, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to(C + np.array([0.3, 0.3, 0]))
        q = T("?", 110, YELLOW, weight=BOLD).move_to(C + np.array([0.3, 0.3, 0]))
        self.play(FadeIn(cell, scale=0.95), FadeIn(nuc), FadeIn(q, scale=0.6), run_time=0.4)

        looks = chip("how it looks", GREY, size=24).move_to([1.1, 2.4, 0])
        endp = chip("where it ended up", GREEN, size=24).move_to([4.8, 2.4, 0])
        a1 = Arrow(looks.get_right(), endp.get_left(), buff=0.1, color=GREY, stroke_width=5, tip_length=0.22)
        cause = chip("what killed it", RED, size=24).move_to([4.4, 0.7, 0])
        a2 = DashedLine(looks.get_bottom() + DOWN * 0.05, cause.get_left() + LEFT * 0.05, color=GREY, stroke_width=4)
        cross = VGroup(Line(UL * 0.22, DR * 0.22, color=RED, stroke_width=7), Line(UR * 0.22, DL * 0.22, color=RED, stroke_width=7))
        cross.move_to(a2.get_center())
        self.at("Looking is not enough")
        self.play(FadeIn(looks, shift=RIGHT * 0.2), run_time=0.4)
        self.at("appearance names")
        self.play(GrowArrow(a1), FadeIn(endp, shift=LEFT * 0.2), run_time=0.5)
        self.at("not what killed it")
        self.play(FadeIn(cause), Create(a2), run_time=0.5)
        self.play(FadeIn(cross, scale=1.4), run_time=0.3)

        # clear the "cause" argument before the two questions
        qa = chip("ask about a lipid", BLUE, size=26).move_to([4.0, -0.7, 0])
        qb = chip("ask about the membrane", ORANGE, size=26).move_to([4.0, -2.2, 0])
        self.at("two questions")
        self.play(FadeOut(VGroup(looks, endp, a1, cause, a2, cross)), run_time=0.4)
        self.at("One is about a lipid")
        qa.move_to([3.5, 1.2, 0]); qb.move_to([3.5, -1.2, 0])
        ar_a = Arrow(qa.get_left(), cell.point_at_angle(PI * 0.15) + RIGHT * 0.05, buff=0.1, color=BLUE, stroke_width=5, tip_length=0.22)
        ar_b = Arrow(qb.get_left(), cell.point_at_angle(-PI * 0.15) + RIGHT * 0.05, buff=0.1, color=ORANGE, stroke_width=5, tip_length=0.22)
        self.play(FadeIn(qa, shift=LEFT * 0.2), GrowArrow(ar_a), run_time=0.5)
        self.at("The other is about the membrane")
        self.play(FadeIn(qb, shift=LEFT * 0.2), GrowArrow(ar_b), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Healthy(SpokenScene):
    def construct(self):
        bars, lips, blobs, dots, dna = membrane_stage()
        lab = stage_labels()
        ra, rb = panel_items()
        self.play(FadeIn(bars), FadeIn(lab), FadeIn(lips, shift=UP * 0.1), run_time=0.4)
        leg, r1, r2, r3 = legend()
        inner = T("inner face", 24, GREY).move_to([-4.6, -1.15, 0])
        self.play(FadeIn(r1), run_time=0.4)
        self.at("on the inner face")
        self.play(FadeIn(inner), Indicate(lips, color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("is a protein that binds")
        self.play(FadeIn(blobs, shift=DOWN * 0.3), FadeIn(r2), run_time=0.6)
        self.at("From outside")
        # annexin V approaches and bounces off
        self.play(*[b.animate.shift(DOWN * 1.1) for b in blobs], run_time=0.7)
        self.play(*[b.animate.shift(UP * 0.6) for b in blobs], run_time=0.5)
        self.at("DNA dye")
        self.play(FadeIn(dots, shift=DOWN * 0.2), FadeIn(r3), FadeIn(dna), run_time=0.6)
        self.at("keep it out")
        self.play(*[d.animate.shift(DOWN * 1.7) for d in dots], run_time=0.7)
        self.play(*[d.animate.shift(UP * 0.5) for d in dots], FadeIn(ra), FadeIn(rb), run_time=0.5)
        self.finish()


class S03Flip(SpokenScene):
    def construct(self):
        bars, lips, blobs, dots, dna = membrane_stage()
        for b in blobs:
            b.shift(DOWN * 0.55)
        for d in dots:
            d.shift(DOWN * 0.8)
        lab = stage_labels()
        ra, rb = panel_items()
        leg, r1, r2, r3 = legend()
        self.add(bars, lips, blobs, dots, dna, lab, leg, ra, rb)
        self.at("Now the cell dies")
        self.wait(0.3)
        self.at("The lipid turns up")
        self.play(*[l.animate.move_to([l.get_center()[0], 0.58, 0]) for l in lips], run_time=1.0)
        self.at("can reach it and bind")
        self.play(*[b.animate.move_to([b.get_center()[0], 1.08, 0]) for b in blobs], run_time=0.7)
        self.play(*[b.animate.set_fill(BLUE, 0.9) for b in blobs], run_time=0.3)
        self.at("reachable from outside")
        self.play(ReplacementTransform(ra, readout("annexin V", "+", BLUE).move_to(ra)), run_time=0.5)
        self.at("But the membrane still holds")
        self.play(*[d.animate.move_to([d.get_center()[0], 1.0, 0]) for d in dots], run_time=0.5)
        self.play(*[d.animate.shift(UP * 0.8) for d in dots], run_time=0.5)
        v = T("clearest apoptotic signal", 22, GREEN).move_to([4.5, -3.0, 0])
        self.at("clearest apoptotic signal")
        self.play(FadeIn(v, shift=UP * 0.1), Indicate(rb, color=GREY, scale_factor=1.03), run_time=0.6)
        self.finish()


class S04Leak(SpokenScene):
    def construct(self):
        bars, lips, blobs, dots, dna = membrane_stage(lipids_out=True, blobs_bound=True)
        for b in blobs:
            b.set_fill(BLUE, 0.9)
        for d in dots:
            d.move_to([d.get_center()[0], 1.8, 0])
        lab = stage_labels()
        ra, rb = panel_items("+", "−")
        leg, r1, r2, r3 = legend()
        v = T("clearest apoptotic signal", 22, GREEN).move_to([4.5, -3.0, 0])
        self.add(bars, lips, blobs, dots, dna, lab, leg, ra, rb, v)
        self.at("Then comes a leak")
        holed = bars_holed()
        leak = T("leaky membrane", 26, RED).move_to([0.4, -1.0, 0])
        self.play(FadeOut(bars), FadeIn(holed), FadeOut(v), FadeIn(leak), run_time=0.7)
        self.at("generally becomes leaky")
        self.wait(0.2)
        self.at("secondary necrosis")
        sn = T("secondary necrosis", 22, RED).move_to([4.5, -3.0, 0])
        self.play(FadeIn(sn, shift=UP * 0.1), run_time=0.5)
        self.at("Propidium iodide enters")
        movers = [dots[2], dots[3]]
        self.play(*[d.animate.move_to([d.get_center()[0], -0.1, 0]) for d in movers], run_time=0.8)
        self.play(*[d.animate.move_to(DNA_C + np.array([dx, 0, 0])) for d, dx in zip(movers, (-1.0, 1.0))], run_time=0.8)
        self.at("stains the DNA")
        dna2 = dna_blob(True)
        self.play(ReplacementTransform(dna, dna2), run_time=0.5)
        self.at("positive for both")
        self.play(ReplacementTransform(rb, readout("PI", "+", ORANGE).move_to(rb)), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Plot(SpokenScene):
    def construct(self):
        boxes, frame = plot_frame()
        title = T("made-up data: Jurkat cells", 24, GREY).move_to([4.5, 2.9, 0])
        sub = M("10,000 cells, drug 6 h", 22, TEXT).move_to([4.5, 2.2, 0])
        self.at("Now read the plot")
        self.play(FadeIn(frame), run_time=0.7)
        self.at("made up data")
        self.play(FadeIn(title), run_time=0.4)
        self.at("flow cytometer")
        self.play(FadeIn(sub), run_time=0.4)
        self.at("four boxes")
        self.play(*[Indicate(b, color=TEXT, scale_factor=1.03) for b in boxes.values()], run_time=0.8)
        self.at("negative for both")
        self.play(FadeIn(count_mob("BL"), scale=0.8), run_time=0.4)
        self.at("positive only")
        self.play(FadeIn(count_mob("BR"), scale=0.8), boxes["BR"].animate.set_fill(GREEN, 0.25), run_time=0.5)
        self.at("positive for both")
        self.play(FadeIn(count_mob("TR"), scale=0.8), boxes["TR"].animate.set_fill(RED, 0.25), run_time=0.5)
        self.at("propidium iodide only")
        self.play(FadeIn(count_mob("TL"), scale=0.8), run_time=0.4)
        self.at("is a puzzle")
        puzzle = T("one box, two stories?", 24, RED).move_to([4.5, 1.4, 0])
        self.play(Indicate(boxes["TR"], color=RED, scale_factor=1.05), FadeIn(puzzle), run_time=0.7)
        late = cell_dot(GREEN).move_to(dot_pos("TR"))
        late_l = dot_legend(GREEN, "late apoptotic", 0.5)
        self.at("late apoptotic cell")
        self.play(FadeIn(late, scale=1.4), FadeIn(late_l, shift=LEFT * 0.2), run_time=0.5)
        necro = cell_dot(GREY).move_to(dot_pos("TR", dy=-0.65))
        nec_l = dot_legend(GREY, "necrosis\nfrom the start", -0.3)
        self.at("necrosis from the start")
        self.play(FadeIn(necro, scale=1.4), FadeIn(nec_l, shift=LEFT * 0.2), run_time=0.5)
        self.at("One time point")
        t1 = T("one time point", 24, YELLOW).move_to([4.5, -1.3, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S06Time(SpokenScene):
    def construct(self):
        boxes, frame = plot_frame()
        boxes["BR"].set_fill(GREEN, 0.25)
        boxes["TR"].set_fill(RED, 0.25)
        counts = VGroup(*[count_mob(k, 0.3) for k in COUNTS])
        self.add(frame, counts)
        arrow = Arrow([3.0, 2.9, 0], [6.0, 2.9, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.25)
        tl = T("time", 26, YELLOW).next_to(arrow, UP, buff=0.12)
        self.at("follow the cells")
        self.play(GrowArrow(arrow), FadeIn(tl), run_time=0.6)
        d = cell_dot(GREEN).move_to(dot_pos("BL"))
        p0, p1, p2 = dot_pos("BL"), dot_pos("BR"), dot_pos("TR")
        self.play(FadeIn(d, scale=1.5), run_time=0.4)
        self.at("exposes the lipid first")
        t1 = Line(p0, p1, color=GREEN, stroke_width=5)
        self.play(Create(t1), d.animate.move_to(p1), run_time=0.9)
        self.at("for a while")
        pi_note = T("PI still −", 24, ORANGE).move_to([4.5, 1.6, 0])
        self.play(FadeIn(pi_note), Indicate(d, color=GREEN, scale_factor=1.3), run_time=0.7)
        self.at("pass through")
        self.play(Indicate(boxes["BR"], color=GREEN, scale_factor=1.04), run_time=0.6)
        self.at("double positive")
        t2 = Line(p1, p2, color=GREEN, stroke_width=5)
        self.play(FadeOut(pi_note), Create(t2), d.animate.move_to(p2), run_time=0.9)
        necro = cell_dot(GREY, "?").move_to(dot_pos("TR", dy=-0.65))
        nl = dot_legend(GREY, "necrosis\nfrom the start", 0.4)
        self.at("cannot settle")
        self.play(FadeIn(necro, scale=1.4), FadeIn(nl), run_time=0.6)
        r1 = T("One marker,", 30, TEXT, font=TITLE_FONT)
        r2 = T("one event.", 30, TEXT, font=TITLE_FONT)
        r3 = T("Combine markers.", 26, GOLD)
        r4 = T("Follow time.", 26, GOLD)
        rule = VGroup(r1, r2, r3, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.5, -1.6, 0])
        self.at("Keep the rule")
        self.play(FadeIn(r1), FadeIn(r2), run_time=0.5)
        self.at("Combine markers")
        self.play(FadeIn(r3), FadeIn(r4), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "One marker reports one event. Combine markers over time."
