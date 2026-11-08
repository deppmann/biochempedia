"""What counts as alive?  (Biochemistrypedia high school Biology explainer, Living or Not)

COLOR MAP (one color per concept, whole video)
  BLUE   = a cell (bacterium, host cell, red blood cell)
  YELLOW = a virus (capsid, new virus parts, new viruses)
  ORANGE = genetic material (DNA or RNA, the virus's genes)
  TEAL   = ribosomes (parts that build proteins)
  PURPLE = nutrients taken in
  GREEN  = characteristic met / living
  RED    = characteristic not met / classed nonliving
  GREY   = outlines, the switch, the crystal, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

ROWS = ["made of cells", "use energy", "grow", "respond", "keep inside steady", "reproduce", "change over generations"]
ROW_Y = [2.5 - 0.86 * i for i in range(7)]
ROW_X = -6.1


def tick(c, color=GREEN, s=0.24):
    a, b, d = c + np.array([-s, 0.0, 0]), c + np.array([-s * 0.3, -s * 0.8, 0]), c + np.array([s * 1.1, s * 0.9, 0])
    return VGroup(Line(a, b, color=color, stroke_width=8), Line(b, d, color=color, stroke_width=8))


def cross(c, color=RED, s=0.22):
    return VGroup(Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=8),
                  Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=8))


def slot(i):
    return np.array([ROW_X + 0.3, ROW_Y[i], 0])


def row(i):
    box = RoundedRectangle(corner_radius=0.08, width=0.56, height=0.56, stroke_color=GREY, stroke_width=3).move_to(slot(i))
    txt = T(ROWS[i], 32, TEXT).next_to(box, RIGHT, buff=0.25)
    return VGroup(box, txt)


def heading_list():
    return T("Characteristics of life", 30, GREY).move_to([ROW_X + 2.5, 3.3, 0])


def virus(r=0.8, genes=True):
    cap = RegularPolygon(6, radius=r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.18)
    g = VGroup(cap)
    if genes:
        core = RoundedRectangle(corner_radius=0.06, width=r * 0.9, height=r * 0.5, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=0.55).move_to(cap)
        g.add(core)
        g.core = core
    g.cap = cap
    return g


def dots(centers, r=0.09, color=TEAL):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to(c) for c in centers])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rod(w, h=1.5, color=BLUE, at=ORIGIN):
    return RoundedRectangle(corner_radius=h / 2 - 0.01, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.14).move_to(at)


class S00Title(TitleCard):
    LESSON = "Living or not? Viruses and bacteria"
    TITLE = "What Counts as Alive?"


# ---------------------------------------------------------------------------------------------
class S01Switch(SpokenScene):
    def construct(self):
        plate = RoundedRectangle(corner_radius=0.25, width=3.0, height=4.0, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.12).move_to([-4.3, -0.7, 0])
        lever = RoundedRectangle(corner_radius=0.12, width=0.8, height=1.6, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.3).move_to(plate)
        plate_lbl = T("light switch", 32, GREY).move_to([-4.3, -3.2, 0])
        v = virus(0.7).move_to([-4.3, 2.1, 0])
        v_lbl = T("cold virus", 32, YELLOW, weight=BOLD).move_to([-4.3, 3.05, 0])
        self.at("A cold virus sits on a light switch")
        self.play(FadeIn(plate), FadeIn(lever), FadeIn(plate_lbl), run_time=0.7)
        self.play(FadeIn(v, shift=DOWN * 0.3), FadeIn(v_lbl), run_time=0.7)
        self.at("it does nothing on its own")
        idle = T("does nothing on its own", 32, TEXT).move_to([0.6, -0.7, 0])
        tm = T("for hours", 32, GREY).move_to([0.6, -1.4, 0])
        self.play(FadeIn(idle, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(tm), run_time=0.4)
        # fingertip picks it up
        self.at("A fingertip can still pick it up")
        tip = RoundedRectangle(corner_radius=0.4, width=2.0, height=1.0, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.3).move_to([0.2, 2.1, 0])
        tip_lbl = T("fingertip", 30, GREY).move_to([0.2, 3.05, 0])
        self.play(FadeOut(idle), FadeOut(tm), FadeIn(tip), FadeIn(tip_lbl), run_time=0.5)
        self.play(tip.animate.move_to([-2.75, 2.1, 0]), tip_lbl.animate.move_to([-1.9, 3.05, 0]), run_time=0.7)
        # nose cell
        self.at("Inside your nose")
        cell = RoundedRectangle(corner_radius=0.7, width=6.2, height=5.0, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.12).move_to([3.4, -0.2, 0])
        cell_lbl = T("one of your cells", 32, BLUE, weight=BOLD).move_to([3.4, 1.85, 0])
        self.play(FadeOut(plate), FadeOut(lever), FadeOut(plate_lbl), FadeOut(v_lbl), FadeOut(tip_lbl),
                  FadeIn(cell), FadeIn(cell_lbl), run_time=0.6)
        self.play(VGroup(v, tip).animate.shift(RIGHT * 4.4 + DOWN * 1.9), run_time=0.8)
        self.play(FadeOut(tip), v.animate.move_to([2.0, 0.1, 0]), run_time=0.6)
        self.at("to build new copies of it")
        c1 = virus(0.5).move_to([3.7, 0.9, 0]); c2 = virus(0.5).move_to([4.7, -0.2, 0]); c3 = virus(0.5).move_to([3.4, -0.9, 0])
        cp_lbl = T("new copies", 32, YELLOW, weight=BOLD).move_to([3.4, -1.9, 0])
        self.play(LaggedStart(FadeIn(c1, scale=0.5), FadeIn(c2, scale=0.5), FadeIn(c3, scale=0.5), lag_ratio=0.3),
                  FadeIn(cp_lbl), run_time=1.0)
        self.at("So what makes something alive")
        grp = Group(*self.mobjects)
        self.play(FadeOut(grp), run_time=0.5)
        q = T("What makes something alive?", 54, font=TITLE_FONT).move_to([0, 0.7, 0])
        q2 = T("Do bacteria and viruses pass the test?", 38, TEAL).move_to([0, -0.8, 0])
        self.play(Write(q), run_time=1.0)
        self.at("Do bacteria and viruses")
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Checklist(SpokenScene):
    def construct(self):
        head = heading_list()
        rows = [row(i) for i in range(7)]
        self.at("Biologists check a list")
        self.play(FadeIn(head), run_time=0.5)
        for cue, i in [("made of one or more cells", 0), ("take in and use energy", 1)]:
            self.at(cue)
            self.play(FadeIn(rows[i], shift=RIGHT * 0.2), run_time=0.4)
        self.at("called metabolism")
        meta = chip("metabolism", TEAL, 30).move_to([0.0, ROW_Y[1], 0])
        self.play(FadeIn(meta, shift=LEFT * 0.2), run_time=0.5)
        for cue, i in [("They grow", 2), ("respond", 3), ("keep their inside conditions steady", 4),
                       ("They reproduce", 5), ("change over many generations", 6)]:
            self.at(cue)
            self.play(FadeIn(rows[i], shift=RIGHT * 0.2), run_time=0.3)
        self.at("No single box decides it")
        note = T("No single box decides it", 38, GOLD).move_to([3.0, 3.0, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("A mature red blood cell")
        rbc = Circle(radius=1.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to([3.0, 1.1, 0])
        rbc_lbl = T("mature red blood cell", 32, BLUE, weight=BOLD).move_to([3.0, -0.5, 0])
        self.play(FadeIn(rbc), FadeIn(rbc_lbl), run_time=0.6)
        self.at("cannot divide")
        x6 = cross(slot(5))
        nd = T("cannot divide", 32, RED).move_to([3.0, -1.3, 0])
        self.play(Create(x6), FadeIn(nd), run_time=0.5)
        self.at("still a living cell")
        live = T("still a living cell", 34, GREEN, weight=BOLD).move_to([3.0, -2.2, 0])
        self.play(FadeIn(live), run_time=0.5)
        self.at("A crystal gets bigger")
        self.play(FadeOut(VGroup(rbc, rbc_lbl, nd, live, x6)), run_time=0.4)
        cr = Square(1.1, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([3.0, 1.1, 0])
        cr_lbl = T("crystal", 32, GREY, weight=BOLD).move_to([3.0, -0.5, 0])
        self.play(FadeIn(cr), FadeIn(cr_lbl), run_time=0.4)
        self.play(cr.animate.scale(1.6), run_time=0.8)
        self.at("no cells and no metabolism")
        self.play(Create(cross(slot(0))), Create(cross(slot(1))), run_time=0.6)
        nc = T("no cells, no metabolism", 32, RED).move_to([3.0, -1.5, 0])
        self.play(FadeIn(nc), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Bacterium(SpokenScene):
    def construct(self):
        head = heading_list()
        rows = [row(i) for i in range(7)]
        self.add(head, *rows)
        self.add(T("not a score: what each one can do on its own", 24, GREY).move_to([-3.3, -3.3, 0]))
        self.at("Now test a bacterium")
        b = rod(4.6, 2.2, BLUE, [3.0, 0.4, 0])
        b_lbl = T("bacterium", 38, BLUE, weight=BOLD).move_to([3.0, 2.5, 0])
        self.play(FadeIn(b, scale=0.9), FadeIn(b_lbl), run_time=0.7)
        self.at("It is a prokaryote")
        pro = T("prokaryote: one cell, no nucleus", 30, BLUE).move_to([3.0, -1.5, 0])
        self.play(FadeIn(pro), run_time=0.5)
        self.at("one cell with no nucleus")
        self.play(Create(tick(slot(0))), run_time=0.4)
        self.at("In a damp place with food")
        nut = VGroup(*[Circle(radius=0.15, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(p) for p in
                       [[-0.2, 1.3, 0], [-0.2, 0.4, 0], [-0.2, -0.5, 0]]])
        nut_lbl = T("nutrients", 30, PURPLE).move_to([-0.2, 2.1, 0])
        self.play(FadeIn(nut), FadeIn(nut_lbl), run_time=0.5)
        self.at("takes in nutrients")
        self.play(*[n.animate.move_to([2.2 + 0.6 * k, 0.4 + 0.3 * (k - 1), 0]) for k, n in enumerate(nut)], run_time=0.9)
        self.at("uses energy")
        self.play(Create(tick(slot(1))), FadeOut(nut_lbl), run_time=0.4)
        self.at("It grows")
        self.play(FadeOut(nut), FadeOut(pro), b.animate.stretch_to_fit_width(5.8), run_time=0.9)
        self.play(Create(tick(slot(2))), run_time=0.3)
        self.at("It responds to its surroundings")
        self.play(Wiggle(b, scale_value=1.04, rotation_angle=0.03 * TAU), Create(tick(slot(3))), run_time=0.8)
        self.at("splits in two")
        b1 = rod(2.7, 2.2, BLUE, [1.65, 0.4, 0]); b2 = rod(2.7, 2.2, BLUE, [4.55, 0.4, 0])
        self.play(ReplacementTransform(b, VGroup(b1, b2)), run_time=0.9)
        self.play(Create(tick(slot(5))), run_time=0.3)
        self.at("It has its own ribosomes")
        rb = dots([[1.0, 0.9, 0], [2.1, 0.2, 0], [1.5, 0.0, 0], [4.0, 0.9, 0], [5.1, 0.2, 0], [4.5, 0.0, 0]], 0.13)
        rb_lbl = T("ribosomes", 32, TEAL).move_to([3.1, -1.4, 0])
        self.play(FadeIn(rb, scale=0.4), FadeIn(rb_lbl), run_time=0.6)
        self.at("So a bacterium is a living cell")
        live = T("a living cell", 40, GREEN, weight=BOLD).move_to([3.1, -2.5, 0])
        self.play(FadeIn(live, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Virus(SpokenScene):
    def construct(self):
        head = heading_list()
        rows = [row(i) for i in range(7)]
        self.add(head, *rows)
        self.add(T("not a score: what each one can do on its own", 24, GREY).move_to([-3.3, -3.3, 0]))
        self.at("Now test a virus")
        v = virus(1.7).move_to([2.6, 0.5, 0])
        v_lbl = T("virus", 38, YELLOW, weight=BOLD).move_to([2.6, 2.85, 0])
        self.play(FadeIn(v, scale=0.8), FadeIn(v_lbl), run_time=0.7)
        self.at("genetic material")
        gl = T("DNA or RNA", 32, ORANGE).move_to([5.3, -0.9, 0])
        ga = arr([5.0, -0.55, 0], v.core.get_right() + np.array([0.0, -0.1, 0]), ORANGE)
        self.play(FadeIn(gl), GrowArrow(ga), run_time=0.6)
        self.at("protein coat")
        cl = T("capsid: protein coat", 32, YELLOW).move_to([2.6, -2.0, 0])
        self.play(FadeIn(cl), Indicate(v.cap, color=YELLOW, scale_factor=1.04), run_time=0.7)
        self.at("is not a cell")
        self.play(Create(cross(slot(0))), run_time=0.4)
        nc = T("not a cell", 34, RED, weight=BOLD).move_to([2.6, -2.9, 0])
        self.play(FadeIn(nc), run_time=0.3)
        self.at("no ribosomes of its own")
        rbx = dots([[4.45, 1.5, 0]], 0.13)
        rbl = T("ribosomes", 26, TEAL).next_to(rbx, RIGHT, buff=0.2)
        rbc = cross(np.array([4.45, 1.5, 0]), RED, 0.3)
        self.play(FadeIn(rbx), FadeIn(rbl), run_time=0.3)
        self.play(Create(rbc), run_time=0.3)
        self.at("Outside a cell")
        out = T("outside a cell", 30, GREY).move_to([5.3, 2.6, 0])
        self.play(FadeIn(out), run_time=0.4)
        self.at("use energy")
        self.play(Create(cross(slot(1))), run_time=0.4)
        self.at("or grow")
        self.play(Create(cross(slot(2))), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Host(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.7, width=9.6, height=6.2, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.1).move_to([1.2, 0.0, 0])
        v = virus(0.7, genes=False).move_to([-5.9, 1.4, 0])
        gen = RoundedRectangle(corner_radius=0.06, width=0.63, height=0.35, stroke_color=ORANGE, stroke_width=3,
                               fill_color=ORANGE, fill_opacity=0.55).move_to(v)
        self.add(v, gen)
        self.at("A host cell")
        c_lbl = T("host cell", 40, BLUE, weight=BOLD).move_to([-1.2, 2.5, 0])
        self.play(FadeIn(cell), FadeIn(c_lbl), run_time=0.7)
        self.at("that a virus infects")
        self.play(VGroup(v, gen).animate.move_to([-1.9, 1.2, 0]), run_time=1.0)
        self.at("the virus's genes")
        gl = T("virus genes", 30, ORANGE).move_to([-1.9, -0.55, 0])
        self.play(gen.animate.move_to([-1.9, 0.1, 0]), FadeIn(gl), run_time=0.7)
        self.at("get the cell to build")
        rb = dots([[0.9, 1.4, 0], [1.9, 0.7, 0], [2.8, 1.5, 0], [3.7, 0.6, 0]], 0.14)
        rb_lbl = T("cell's ribosomes", 30, TEAL).move_to([2.8, 2.5, 0])
        a1 = arr([-1.1, 0.3, 0], [0.5, 0.9, 0], ORANGE)
        self.play(FadeIn(rb), FadeIn(rb_lbl), GrowArrow(a1), run_time=0.8)
        self.at("new virus parts")
        parts = VGroup(*[RegularPolygon(6, radius=0.26, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.35).move_to(p)
                         for p in [[1.3, -0.3, 0], [2.4, -0.4, 0], [3.5, -0.3, 0], [4.6, 0.1, 0]]])
        pl = T("new virus parts", 30, YELLOW).move_to([3.0, -1.1, 0])
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in parts], lag_ratio=0.2), FadeIn(pl), run_time=1.0)
        self.at("come together as new viruses")
        new = [virus(0.55).move_to([1.2 + 1.5 * k, -1.9, 0]) for k in range(3)]
        nl = T("new viruses", 32, YELLOW, weight=BOLD).move_to([2.7, -2.65, 0])
        self.play(FadeOut(pl), *[ReplacementTransform(parts[k].copy(), new[k]) for k in range(3)], FadeOut(parts), run_time=1.0)
        self.play(FadeIn(nl), run_time=0.4)
        self.at("the ribosomes")
        self.play(Indicate(cell, color=BLUE, scale_factor=1.01), run_time=0.8)
        self.at("no metabolism of its own")
        nm = T("virus:\nno metabolism\nof its own", 30, RED).move_to([-1.2, -1.9, 0])
        self.play(FadeIn(nm), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        divider = Line([0, 3.4, 0], [0, -2.4, 0], color=GREY, stroke_width=2)
        bh = T("Bacterium", 46, BLUE, weight=BOLD).move_to([-3.4, 3.0, 0])
        vh = T("Virus", 46, YELLOW, weight=BOLD).move_to([3.4, 3.0, 0])
        bi = rod(2.2, 1.1, BLUE, [-3.4, 1.7, 0])
        vi = virus(0.6).move_to([3.4, 1.7, 0])
        self.add(divider, bh, vh, bi, vi)
        self.at("classes viruses as")
        vs = T("classed as nonliving", 38, RED, weight=BOLD).move_to([3.4, 0.55, 0])
        self.play(FadeIn(vs, shift=UP * 0.15), run_time=0.6)
        self.at("is not a cell")
        r1 = T("not a cell", 32, TEXT).move_to([3.4, -0.25, 0])
        self.play(FadeIn(r1), run_time=0.4)
        self.at("no metabolism of its own")
        r2 = T("no metabolism of its own", 32, TEXT).move_to([3.4, -0.95, 0])
        self.play(FadeIn(r2), run_time=0.4)
        self.at("copied only inside a host cell")
        r3 = T("copied only inside a host cell", 32, TEXT).move_to([3.4, -1.65, 0])
        self.play(FadeIn(r3), run_time=0.4)
        self.at("Most bacteria carry out")
        bs = T("living cell", 38, GREEN, weight=BOLD).move_to([-3.4, 0.55, 0])
        b1 = T("a whole cell", 32, TEXT).move_to([-3.4, -0.25, 0])
        b2 = T("most carry out life\nprocesses by themselves", 30, TEXT).move_to([-3.4, -1.15, 0])
        self.play(FadeIn(bs, shift=UP * 0.15), FadeIn(b1), FadeIn(b2), run_time=0.8)
        self.at("when conditions")
        b3 = T("when conditions suit them", 30, GREY).move_to([-3.4, -2.2, 0])
        self.play(FadeIn(b3), run_time=0.4)
        self.at("Scientists still discuss the question")
        dq = T("Scientists still discuss the question", 34, GOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(dq), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Bacteria are living cells; viruses are classed as nonliving."
