"""Epithelia: one sheet, two different faces  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = glucose
  ORANGE = sodium (and ions)
  PURPLE = what the gut holds that must stay out (gut contents, hemoglobin tracer)
  BLUE   = SGLT1 (apical carrier)
  GREEN  = GLUT2 (basolateral carrier)
  TEAL   = sodium-potassium pump
  GOLD   = ATP
  RED    = tight junction seal / a wrong result
  WHITE  = apical face (and the highlighted middle cell)
  PINK   = basolateral face
  GREY   = membranes, cells, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"

CTOP, CBOT = 1.5, -1.5          # cell top (apical) and base
CX = (-4.1, 0.0, 4.1)           # three cells
CW = 4.04                       # cell width
GAPX = (-2.1, 2.1)              # gaps between cells
SG_X = -1.0                     # SGLT1 on the apical membrane
GL_X = 1.0                      # GLUT2 on the base
PU_X = -1.0                     # pump on the base


def cell(cx, w=CW, top=CTOP, bot=CBOT, op=0.07):
    return Rectangle(width=w, height=top - bot, stroke_color=GREY, stroke_width=3,
                     fill_color=GREY, fill_opacity=op).move_to([cx, (top + bot) / 2, 0])


def seal_at(x, y=1.3):
    return Rectangle(width=0.3, height=0.4, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([x, y, 0])


def frame(hi=False, seals=True):
    cells = VGroup(*[cell(x) for x in CX])
    if hi:
        cells[1].set_fill(TEXT, 0.14).set_stroke(TEXT, 5)
    sl = VGroup(*[seal_at(x) for x in GAPX]) if seals else VGroup()
    gut = T("gut", 26, GREY).move_to([-5.7, 3.0, 0])
    blood = T("blood", 26, GREY).move_to([-5.7, -3.0, 0])
    return cells, sl, gut, blood


def glc(p, r=0.15):
    return Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([p[0], p[1], 0])


def na(p, r=0.11):
    return Circle(radius=r, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([p[0], p[1], 0])


def carrier(color, x, y, w=0.6, h=0.8):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.4).move_to([x, y, 0])


def path(m, pts):
    return MoveAlongPath(m, VMobject().set_points_as_corners([m.get_center(), *[[p[0], p[1], 0] for p in pts]]))


def cross(x, y, s=0.28, color=RED):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=7),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=7))


class S00Title(TitleCard):
    LESSON = "Epithelia and tissue organization"
    TITLE = "One sheet, two different faces"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a sheet one cell thick; glucose goes one way; gut contents are kept out; the puzzle."""

    def construct(self):
        cells, sl, gut, blood = frame(seals=False)
        sealbars = VGroup(*[seal_at(x) for x in GAPX])
        self.at("single layer of cells")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cells], lag_ratio=0.3),
                  FadeIn(gut), FadeIn(blood), run_time=1.6)
        self.at("moves glucose")
        gl = VGroup(glc([-0.5, 2.4]), glc([0, 2.65]), glc([0.5, 2.4]))
        gl_lbl = T("glucose", 26, YELLOW).move_to([-1.8, 2.5, 0])
        self.play(FadeIn(gl, scale=0.6), FadeIn(gl_lbl), run_time=0.6)
        self.play(gl.animate.shift(DOWN * 5.0), gl_lbl.animate.shift(DOWN * 5.0), run_time=2.4)
        self.at("seeping in between")
        sq = VGroup(*[Square(side_length=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(p)
                      for p in ([1.95, 2.7, 0], [2.25, 2.7, 0], [1.95, 2.35, 0], [2.25, 2.35, 0])])
        sq_lbl = T("gut contents", 26, PURPLE).move_to([4.2, 2.5, 0])
        self.play(FadeIn(sq), FadeIn(sq_lbl), run_time=0.6)
        self.play(sq.animate.shift(DOWN * 0.5), run_time=0.9)
        x = cross(2.1, 1.28, 0.24)
        self.play(Create(x), run_time=0.5)
        self.at("How can one thin sheet")
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, 0, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("which way is up")
        up = Arrow([0, -0.9, 0], [0, 0.9, 0], buff=0, color=TEXT, stroke_width=9, tip_length=0.4)
        up_lbl = T("up", 30, TEXT).next_to(up, RIGHT, buff=0.2)
        self.play(ReplacementTransform(q, up), FadeIn(up_lbl), run_time=0.7)
        self.at("are sealed")
        self.play(FadeOut(x), LaggedStart(*[GrowFromCenter(b) for b in sealbars], lag_ratio=0.3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Faces(SpokenScene):
    """apical face, basolateral face, different proteins on each, polarity."""

    def construct(self):
        cells, sl, gut, blood = frame()
        self.add(cells, sl, gut, blood)
        self.at("two faces")
        self.play(cells[1].animate.set_fill(TEXT, 0.14), run_time=0.7)
        self.at("looks into the gut")
        top = Line([-CW / 2, CTOP, 0], [CW / 2, CTOP, 0], color=TEXT, stroke_width=10)
        a_tag = T("apical face", 30, TEXT).move_to([0, 2.25, 0])
        self.play(Create(top), FadeIn(a_tag, shift=DOWN * 0.1), run_time=0.8)
        self.at("neighboring cells")
        side = VMobject(color=PINK, stroke_width=10)
        side.set_points_as_corners([[-CW / 2, CTOP - 0.25, 0], [-CW / 2, CBOT, 0], [CW / 2, CBOT, 0], [CW / 2, CTOP - 0.25, 0]])
        b_tag = T("basolateral face", 30, PINK).move_to([0, -0.95, 0])
        self.play(Create(side), FadeIn(b_tag), run_time=1.0)
        self.at("a thin mat")
        mat = Rectangle(width=12.4, height=0.12, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([0, -1.75, 0])
        mat_lbl = T("basement membrane", 24, GREY).move_to([4.0, -2.2, 0])
        self.play(FadeIn(mat), FadeIn(mat_lbl), run_time=0.8)
        self.at("different proteins")
        sh_a = VGroup(Circle(radius=0.17, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.35).move_to([-0.8, CTOP, 0]),
                      Triangle(stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.35).scale(0.2).move_to([0.8, CTOP, 0]))
        sh_b = VGroup(Square(side_length=0.32, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.35).move_to([-0.8, CBOT, 0]),
                      Square(side_length=0.3, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.35).rotate(PI / 4).move_to([0.8, CBOT, 0]))
        self.play(LaggedStart(*[GrowFromCenter(s) for s in [*sh_a, *sh_b]], lag_ratio=0.25), run_time=1.4)
        self.at("That difference")
        dbl = DoubleArrow([-0.9, 1.0, 0], [-0.9, -0.4, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.25)
        pol = T("apicobasal\npolarity", 26, TEXT).move_to([0.45, 0.3, 0])
        self.play(GrowFromCenter(dbl), FadeIn(pol), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Seal(SpokenScene):
    """zoom on a gap: junction stack, tight junction on top, tracer stops, ions untested."""

    def construct(self):
        top, bot, gw = 0.6, -3.3, 0.9
        w = 6.2 - gw / 2
        left = Rectangle(width=w, height=top - bot, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07
                         ).move_to([-(gw / 2 + w / 2), (top + bot) / 2, 0])
        right = left.copy().move_to([(gw / 2 + w / 2), (top + bot) / 2, 0])
        self.play(FadeIn(left), FadeIn(right), run_time=0.8)
        bars = VGroup(*[Rectangle(width=gw, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([0, y, 0])
                        for y, h in ((-0.35, 0.4), (-1.4, 0.25), (-2.4, 0.25))])
        self.at("stacked in a fixed order")
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.4), run_time=1.6)
        self.at("the most apical")
        tj_lbl = T("tight junction", 30, RED).move_to([0.8, -0.35, 0], aligned_edge=LEFT)
        ap_lbl = T("most apical", 24, TEXT).move_to([0.8, -0.85, 0], aligned_edge=LEFT)
        more = T("more junctions below", 24, GREY).move_to([0.8, -1.9, 0], aligned_edge=LEFT)
        self.play(bars[0].animate.set_fill(RED, 1), FadeIn(tj_lbl), FadeIn(ap_lbl), FadeIn(more), run_time=0.9)
        self.at("seals the space")
        self.play(Indicate(bars[0], color=RED, scale_factor=1.15), run_time=0.9)
        self.at("rat kidney tubules")
        rs = np.random.RandomState(4)
        pts = []
        while len(pts) < 24:
            p = (rs.uniform(-5.7, 5.7), rs.uniform(1.0, 2.8))
            if abs(p[0]) > 1.0 and not (-3.4 < p[0] < -1.0 and p[1] < 2.0) and all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.3 for q in pts):
                pts.append(p)
        fall = [(-0.25, 1.0), (0.0, 1.5), (0.25, 1.0), (-0.12, 1.9), (0.12, 2.3), (0.0, 2.7)]
        tr = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to([p[0], p[1], 0]) for p in pts])
        fl = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to([p[0], p[1], 0]) for p in fall])
        lum = T("rat kidney tubule", 26, TEXT).move_to([-4.0, 3.2, 0])
        tl = T("hemoglobin tracer", 26, PURPLE).move_to([4.0, 3.2, 0])
        self.play(FadeIn(tr), FadeIn(fl), FadeIn(lum), FadeIn(tl), run_time=1.0)
        self.at("tracer stopped")
        rest = [(-0.25, -0.02), (0.0, -0.02), (0.25, -0.02), (-0.12, 0.22), (0.12, 0.22), (0.0, 0.46)]
        self.play(LaggedStart(*[path(m, [(r[0], 0.6), r]) for m, r in zip(fl, rest)], lag_ratio=0.25), run_time=2.2)
        self.at("placed a barrier")
        self.play(Indicate(bars[0], color=RED, scale_factor=1.15), run_time=0.9)
        self.at("closed to ions")
        ions = VGroup(*[na([x, 1.35], 0.13) for x in (-3.0, -2.7, -2.4)])
        ion_l = T("ions", 26, ORANGE).move_to([-2.7, 0.95, 0])
        dash = DashedLine([-2.0, 1.35, 0], [-0.6, 0.75, 0], color=ORANGE, stroke_width=5, dash_length=0.12)
        qm = T("?", 56, ORANGE, weight=BOLD).move_to([-1.5, 1.45, 0])
        self.play(FadeIn(ions), FadeIn(ion_l), Create(dash), FadeIn(qm, scale=0.6), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def sg_label():
    lbl = T("SGLT1", 28, BLUE).move_to([-3.2, 2.0, 0])
    ln = Line([-2.6, 1.98, 0], [SG_X - 0.35, 1.62, 0], color=BLUE, stroke_width=3)
    return lbl, ln


def row_particles(x0, y=0.8):
    return [na([x0, y]), glc([x0 + 0.5, y]), na([x0 + 1.0, y])]


class S04In(SpokenScene):
    """SGLT1 takes glucose and two sodium ions in, twice."""

    def construct(self):
        cells, sl, gut, blood = frame()
        self.add(cells, sl, gut, blood)
        self.at("takes the route")
        self.play(cells[1].animate.set_fill(TEXT, 0.14).set_stroke(TEXT, 5), run_time=0.7)
        self.at("apical face")
        sg = carrier(BLUE, SG_X, CTOP)
        lbl, ln = sg_label()
        s1 = [na([-1.5, 2.4]), glc([-1.0, 2.4]), na([-0.5, 2.4])]
        l1 = [T("Na+", 22, ORANGE).move_to([-1.5, 2.75, 0]), T("glucose", 22, YELLOW).move_to([-1.0, 3.15, 0]),
              T("Na+", 22, ORANGE).move_to([-0.5, 2.75, 0])]
        self.play(GrowFromCenter(sg), FadeIn(lbl), Create(ln), FadeIn(VGroup(*s1)), FadeIn(VGroup(*l1)), run_time=1.0)
        self.at("carries glucose into the cell")
        self.play(FadeOut(VGroup(*l1)), run_time=0.3)
        self.play(*[path(m, [(m.get_center()[0] * 0.4 + SG_X * 0.6, 1.7)]) for m in s1], run_time=0.8)
        tg1 = row_particles(-1.5)
        self.play(*[path(m, [t]) if False else m.animate.move_to([t.get_center()[0], 0.8, 0]) for m, t in zip(s1, tg1)], run_time=0.9)
        self.at("For human")
        oo = T("human SGLT1, frog oocytes", 22, GREY).move_to([4.1, 2.45, 0])
        self.play(FadeIn(oo), run_time=0.6)
        s2 = [na([-1.5, 2.4]), glc([-1.0, 2.4]), na([-0.5, 2.4])]
        self.add(*s2)
        self.at("two sodium ions")
        ratio = T("2 Na+ per glucose", 30, TEXT).move_to([4.1, 2.95, 0])
        self.play(FadeIn(ratio), run_time=0.5)
        self.play(*[path(m, [(m.get_center()[0] * 0.4 + SG_X * 0.6, 1.7)]) for m in s2], run_time=0.8)
        tg2 = row_particles(0.2)
        self.play(*[m.animate.move_to([t.get_center()[0], 0.8, 0]) for m, t in zip(s2, tg2)], run_time=0.9)
        self.at("runs down its gradient")
        g1 = T("Na+ goes down\nits gradient", 24, ORANGE).move_to([0.0, 0.1, 0])
        self.play(FadeIn(g1, shift=DOWN * 0.15), run_time=0.7)
        self.at("against its own")
        g2 = T("glucose goes in\nagainst its gradient", 24, YELLOW).move_to([0.0, -0.9, 0])
        self.play(FadeIn(g2, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


class S05Out(SpokenScene):
    """GLUT2 lets glucose out; the pump sends sodium out and keeps the gradient."""

    def construct(self):
        cells, sl, gut, blood = frame(hi=True)
        sg = carrier(BLUE, SG_X, CTOP)
        lbl, ln = sg_label()
        n1, g1, n2 = row_particles(-1.5)
        n3, g2, n4 = row_particles(0.2)
        nas = [n1, n2, n3, n4]
        self.add(cells, sl, gut, blood, sg, lbl, ln, n1, g1, n2, n3, g2, n4)
        self.at("lets glucose leave")
        gl = carrier(GREEN, GL_X, CBOT)
        gl_l = T("GLUT2", 26, GREEN).move_to([2.9, -1.95, 0])
        self.play(GrowFromCenter(gl), FadeIn(gl_l), run_time=0.7)
        self.play(LaggedStart(path(g1, [(GL_X, -1.2), (0.7, -2.75)]), path(g2, [(GL_X, -1.2), (1.4, -2.75)]), lag_ratio=0.4),
                  run_time=2.2)
        self.at("concentration gradient")
        cg = T("glucose leaves down its\nconcentration gradient", 22, YELLOW).move_to([4.5, -2.85, 0])
        self.play(FadeIn(cg), run_time=0.6)
        self.at("In the standard account")
        std = T("standard account", 22, GREY).move_to([2.9, -2.3, 0])
        self.play(FadeIn(std), run_time=0.5)
        self.at("pump on the same face")
        pu = carrier(TEAL, PU_X, CBOT, w=0.9, h=0.8)
        pu_l = T("sodium-potassium pump", 24, TEAL).move_to([-3.4, -2.25, 0])
        self.play(GrowFromCenter(pu), FadeIn(pu_l), run_time=0.7)
        self.at("uses ATP")
        atp = chip("ATP", GOLD, size=24).move_to([PU_X, -0.62, 0])
        self.play(FadeIn(atp, shift=DOWN * 0.1), run_time=0.5)
        self.at("push sodium out")
        outs = [(-1.6, -2.85), (-1.2, -2.95), (-0.8, -2.85), (-0.4, -2.95)]
        self.play(LaggedStart(*[path(m, [(PU_X, -1.1), o]) for m, o in zip(nas, outs)], lag_ratio=0.2), run_time=1.6)
        self.play(FadeOut(VGroup(*nas)), run_time=0.3)
        self.at("keeps cytosolic sodium low")
        low = T("cytosolic Na+ low", 26, ORANGE).move_to([0.0, 0.0, 0])
        ar = Arrow([0.3, 2.7, 0], [0.3, 0.9, 0], buff=0, color=ORANGE, stroke_width=10, tip_length=0.35)
        arl = T("Na+ gradient", 24, ORANGE).move_to([2.2, 2.4, 0])
        self.play(FadeIn(low), GrowArrow(ar), FadeIn(arl), run_time=0.8)
        self.at("Without it")
        x = cross(PU_X, CBOT, 0.35)
        self.play(Create(x), pu.animate.set_opacity(0.4), FadeOut(low), run_time=0.9)
        self.at("runs down")
        self.play(ar.animate.scale(0.35, about_point=[0.3, 0.9, 0]), arl.animate.set_opacity(0.4), run_time=1.0)
        self.finish()


class S06Rule(SpokenScene):
    """SGLT1 on both faces would pull glucose back; each face its own transporters; the seal."""

    def construct(self):
        cells, sl, gut, blood = frame(hi=True)
        sg = carrier(BLUE, SG_X, CTOP)
        lbl, ln = sg_label()
        self.add(cells, sl, gut, blood, sg, lbl, ln)
        self.at("on both faces")
        c1 = carrier(BLUE, -1.0, CBOT)
        c2 = carrier(BLUE, 1.0, CBOT)
        cl = T("SGLT1 on the base", 24, BLUE).move_to([3.7, -1.95, 0])
        self.play(GrowFromCenter(c1), GrowFromCenter(c2), FadeIn(cl), run_time=0.8)
        self.at("would pull")
        b1, b2 = glc([-1.0, -2.7]), glc([1.0, -2.7])
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.4)
        self.play(path(b1, [(-1.0, -1.5), (-1.0, -0.5)]), path(b2, [(1.0, -1.5), (1.0, -0.5)]), run_time=1.6)
        self.at("against absorption")
        wrong = T("against absorption", 30, RED).move_to([0.0, 0.75, 0])
        self.play(FadeIn(wrong, shift=DOWN * 0.1), run_time=0.6)
        self.at("each face carries")
        pu = carrier(TEAL, PU_X, CBOT, w=0.9, h=0.8)
        gl = carrier(GREEN, GL_X, CBOT)
        gl_l = T("GLUT2", 26, GREEN).move_to([2.9, -1.95, 0])
        pu_l = T("sodium-potassium pump", 24, TEAL).move_to([-3.4, -2.25, 0])
        self.play(FadeOut(wrong), FadeOut(cl), FadeOut(b1), FadeOut(b2),
                  ReplacementTransform(c1, pu), ReplacementTransform(c2, gl), FadeIn(gl_l), FadeIn(pu_l), run_time=1.0)
        self.at("tight junction seals")
        tj = T("tight junction", 28, RED).move_to([4.4, 2.0, 0])
        tj_ln = Line([3.2, 1.9, 0], [2.3, 1.5, 0], color=RED, stroke_width=3)
        self.play(FadeIn(tj), Create(tj_ln), *[Indicate(s, color=RED, scale_factor=1.4) for s in sl], run_time=1.0)
        self.at("move glucose one way")
        gs = [glc([SG_X, 2.5]) for _ in range(3)]
        self.add(*gs)
        self.play(LaggedStart(*[path(g, [(SG_X, 1.4), (SG_X, 0.6), (GL_X, -0.7), (GL_X, -1.5), (GL_X + (i - 1) * 0.4, -2.7)])
                                for i, g in enumerate(gs)], lag_ratio=0.2), run_time=1.6)
        self.at("gut's contents out")
        sq = VGroup(*[Square(side_length=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(p)
                      for p in ([1.95, 3.0, 0], [2.25, 3.0, 0], [1.95, 2.65, 0], [2.25, 2.65, 0])])
        gc = T("gut contents", 24, PURPLE).move_to([4.4, 2.9, 0])
        self.play(FadeIn(sq), FadeIn(gc), run_time=0.5)
        self.play(sq.animate.shift(DOWN * 1.0), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Each face carries its own transporters, and the gaps are sealed."
