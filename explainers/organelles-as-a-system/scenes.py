"""Organelles as a system: one protein, many cell parts  (Biochemistrypedia explainer, high school Biology)

COLOR MAP (one color per concept, whole video)
  GREY   = cell outline (cell membrane), labels of the membrane
  BLUE   = nucleus and its DNA
  PURPLE = messenger RNA
  PINK   = ribosomes
  TEAL   = endoplasmic reticulum (rough ER)
  GREEN  = Golgi apparatus
  YELLOW = the protein / insulin and the vesicles that carry it
  ORANGE = mitochondria and ATP
Schematic, not to scale. Shapes are labelled outlines only.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E58FB8"
ORANGE = "#F29E4C"
TEAL_ = TEAL

CY = -0.45
CELL_C = np.array([-0.6, CY, 0])
NUC = np.array([-4.3, -0.15, 0])
ER_C = np.array([-0.9, -0.3, 0])
GO_C = np.array([2.5, -0.3, 0])
EDGE = np.array([5.09, -0.3, 0])
MITO1 = np.array([-2.2, -2.3, 0])
MITO2 = np.array([2.2, -2.3, 0])
GOLD_ = "#D4A843"


def cell():
    return Ellipse(width=11.4, height=5.6, stroke_color=GREY, stroke_width=5, fill_color=GREY,
                   fill_opacity=0.06).move_to(CELL_C)


def nucleus():
    c = Circle(radius=1.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.12).move_to(NUC)
    dna = chip("DNA", BLUE, size=28, pad=0.14).move_to(NUC + UP * 0.45)
    return VGroup(c, dna)


def bars(center, color, n=3, w=2.4, gap=0.6, h=0.4):
    return VGroup(*[RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3.5,
                                     fill_color=color, fill_opacity=0.25).move_to(center + UP * (gap * (1 - i)))
                    for i in range(n)])


def er():
    return bars(ER_C, TEAL_)


def ribos():
    pts = [ER_C + np.array([dx, 0.6 + 0.2 + 0.12, 0]) for dx in (-0.9, -0.3, 0.3, 0.9)]
    return VGroup(*[Circle(radius=0.12, stroke_color=PINK, stroke_width=2, fill_color=PINK, fill_opacity=1).move_to(p)
                    for p in pts])


def golgi():
    return bars(GO_C, GREEN, w=2.2)


def mito(c):
    return Ellipse(width=1.5, height=0.8, stroke_color=ORANGE, stroke_width=3.5, fill_color=ORANGE, fill_opacity=0.2).move_to(c)


def lbl(text, color, pos, size=28):
    return T(text, size, color).move_to(pos)


def nlabel():
    return lbl("nucleus", BLUE, NUC + DOWN * 1.8, 28)


def protein_token(pos):
    return Square(side_length=0.3, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=1).move_to(pos)


def vesicle(pos, with_token=True, r=0.4):
    v = Circle(radius=r, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.1).move_to(pos)
    return VGroup(v, protein_token(pos)) if with_token else VGroup(v)


def atp_arrow(a, b):
    return Arrow(a, b, buff=0.05, color=ORANGE, stroke_width=5, tip_length=0.2)


def topline(text, color=TEXT, size=38):
    return T(text, size, color, font=TITLE_FONT).move_to([0, 3.3, 0])


def mrna_chip(pos):
    return chip("messenger RNA", PURPLE, size=24, pad=0.12).move_to(pos)


MRNA_REST = np.array([-0.9, 1.75, 0])
VPOS = [np.array([3.85, 0.5, 0]), np.array([4.0, -0.45, 0]), np.array([3.8, -1.3, 0])]


def base(scene):
    d = {"cell": cell(), "nuc": nucleus(), "nl": nlabel()}
    scene.add(d["cell"], d["nuc"], d["nl"])
    return d


def mito_set():
    m1, m2 = mito(MITO1), mito(MITO2)
    ml = T("mitochondria", 28, ORANGE).move_to([0.0, -2.5, 0])
    return m1, m2, ml


def atp_set():
    a1 = atp_arrow(np.array([-2.1, -1.85, 0]), np.array([-1.95, -1.2, 0]))
    a2 = atp_arrow(np.array([2.2, -1.85, 0]), np.array([2.4, -1.2, 0]))
    t1 = T("ATP", 28, ORANGE, weight=BOLD).next_to(a1, LEFT, buff=0.1)
    t2 = T("ATP", 28, ORANGE, weight=BOLD).next_to(a2, RIGHT, buff=0.1)
    return a1, a2, t1, t2


class S00Title(TitleCard):
    LESSON = "Organelles as a system"
    TITLE = "One protein, many cell parts"


# -------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        top = topline("After a meal")
        self.at("After a meal")
        self.play(Write(top), run_time=0.8)
        # blood sugar gauge: schematic, no numbers
        frame = Rectangle(width=1.1, height=3.6, stroke_color=GOLD_, stroke_width=4).move_to([0, -0.5, 0])
        fillr = Rectangle(width=1.1, height=0.8, stroke_width=0, fill_color=GOLD_, fill_opacity=0.5)
        fillr.move_to(frame.get_bottom() + UP * 0.4)
        gl = T("blood sugar", 32, GOLD_).next_to(frame, RIGHT, buff=0.4)
        self.play(Create(frame), FadeIn(gl), FadeIn(fillr), run_time=0.8)
        self.at("sugar level in your blood rises")
        new = Rectangle(width=1.1, height=2.8, stroke_width=0, fill_color=GOLD_, fill_opacity=0.5).move_to(frame.get_bottom() + UP * 1.4)
        up = Arrow(frame.get_left() + LEFT * 0.4 + DOWN * 1.0, frame.get_left() + LEFT * 0.4 + UP * 1.0, color=GOLD_, stroke_width=7, buff=0)
        self.play(Transform(fillr, new), GrowArrow(up), run_time=1.6)
        self.at("Small cells in your pancreas")
        c = cell()
        self.play(FadeOut(VGroup(frame, fillr, gl, up)), Transform(top, topline("A beta cell in the pancreas")), Create(c), run_time=1.2)
        self.at("release insulin")
        ins_g = VGroup(protein_token(ORIGIN), T("insulin", 34, YELLOW)).arrange(RIGHT, buff=0.25).move_to([0.2, 0.8, 0])
        self.play(FadeIn(ins_g, scale=0.9), run_time=0.5)
        self.at("protein hormone")
        self.play(Indicate(ins_g, color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("stored in the cell's nucleus")
        nuc = nucleus(); nl = nlabel()
        self.play(FadeIn(nuc, scale=0.9), FadeIn(nl), FadeOut(ins_g, shift=LEFT * 1.5), run_time=0.8)
        self.at("outer edge")
        edge_dot = Dot(EDGE, radius=0.14, color=GREY)
        el = T("outer edge:\ncell membrane", 28, GREY, line_spacing=0.9).move_to([3.7, 2.5, 0])
        ar = Arrow(el.get_bottom(), np.array([4.5, 0.9, 0]), color=GREY, buff=0.08, stroke_width=3, tip_length=0.18)
        self.play(FadeIn(el), GrowArrow(ar), FadeIn(edge_dot), run_time=0.7)
        self.at("How does it get")
        q = VGroup(*[T("?", 64, YELLOW, weight=BOLD).move_to([x, CY + 0.2, 0]) for x in (-1.5, 0.4, 2.3)])
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in q], lag_ratio=0.35), run_time=1.2)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


class S02Nucleus(SpokenScene):
    def construct(self):
        d = base(self)
        top = topline("1  Nucleus: the instructions")
        self.add(top)
        self.at("Start in the nucleus")
        self.play(d["nuc"][0].animate.set_stroke(width=8), run_time=0.5)
        self.at("holds most")
        self.play(d["nuc"][1].animate.scale(1.0).shift(UP * 0.35), run_time=0.5)
        self.at("its instructions")
        self.play(Indicate(d["nuc"][1], color=BLUE, scale_factor=1.15), run_time=0.7)
        self.at("The gene for insulin")
        gl = T("insulin gene", 24, BLUE).move_to(NUC + UP * 0.33)
        gene = Rectangle(width=1.1, height=0.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.9).move_to(NUC + DOWN * 0.05)
        self.play(FadeIn(gl), FadeIn(gene), run_time=0.6)
        self.at("copies that gene")
        mrna = mrna_chip(NUC + DOWN * 0.55)
        self.play(FadeIn(mrna, scale=0.6), run_time=0.6)
        self.at("Then the messenger")
        self.play(FadeOut(gl), FadeOut(gene), mrna.animate.move_to(MRNA_REST), run_time=1.4)
        self.finish()


class S03Ribosome(SpokenScene):
    def construct(self):
        d = base(self)
        top = topline("2  Ribosome on the rough ER: build the protein")
        self.add(top)
        mrna = mrna_chip(MRNA_REST)
        self.add(mrna)
        erb = er(); rb = ribos()
        self.at("reaches a ribosome")
        self.play(FadeIn(erb, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(rb, scale=0.4), mrna.animate.move_to(ER_C + UP * 1.55), run_time=0.7)
        self.at("builds proteins")
        rl = T("ribosome", 28, PINK).move_to(ER_C + RIGHT * 2.2 + UP * 0.85)
        rla = Arrow(rl.get_left() + LEFT * 0.0, rb[3].get_right() + UP * 0.0, color=PINK, buff=0.1, stroke_width=3, tip_length=0.15)
        self.play(FadeIn(rl), GrowArrow(rla), Indicate(rb, color=PINK, scale_factor=1.4), run_time=0.9)
        self.at("links building blocks")
        blocks = VGroup(*[Square(side_length=0.26, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=1) for _ in range(5)])
        blocks.arrange(RIGHT, buff=0.06)
        pl = T("protein chain", 28, YELLOW)
        grp = VGroup(blocks, pl).arrange(DOWN, buff=0.15).move_to([3.0, 0.5, 0])
        self.play(FadeOut(mrna), FadeOut(rl), FadeOut(rla),
                  LaggedStart(*[FadeIn(b, scale=0.4) for b in blocks], lag_ratio=0.25), FadeIn(pl), run_time=1.4)
        self.at("endoplasmic reticulum")
        erl = T("endoplasmic reticulum\n(ER)", 28, TEAL_, line_spacing=0.9).move_to(ER_C + DOWN * 1.65)
        self.play(FadeIn(erl), Indicate(erb, color=TEAL_, scale_factor=1.05), run_time=0.8)
        tok = protein_token(ER_C + DOWN * 0.0)
        self.play(grp.animate.scale(0.3).move_to(ER_C).set_opacity(0), FadeIn(tok), run_time=0.8)
        self.at("rough")
        self.play(Indicate(rb, color=PINK, scale_factor=1.4), run_time=0.7)
        self.at("the new protein folds")
        self.play(Indicate(tok, color=YELLOW, scale_factor=2.0), tok.animate.move_to(ER_C + DOWN * 0.6), run_time=0.9)
        self.at("In a beta cell")
        note = T("longer precursor,\ncut into insulin later", 26, YELLOW, line_spacing=0.9).move_to([3.05, -1.05, 0])
        na = Arrow(note.get_left() + LEFT * 0.05, tok.get_center() + RIGHT * 0.25, color=YELLOW, buff=0.1, stroke_width=3, tip_length=0.15)
        self.play(FadeIn(note), GrowArrow(na), run_time=0.8)
        self.finish()


class S04Golgi(SpokenScene):
    def construct(self):
        d = base(self)
        top = topline("3  Vesicle to the Golgi: sort and pack")
        self.add(top)
        erb = er(); rb = ribos()
        erl = T("ER", 28, TEAL_).move_to(ER_C + DOWN * 1.45)
        tok = protein_token(ER_C + DOWN * 0.6)
        self.add(erb, rb, erl, tok)
        self.at("Next, a vesicle forms")
        ves = VGroup(Circle(radius=0.4, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.1).move_to(tok), tok)
        self.play(FadeIn(ves[0], scale=0.5), run_time=0.5)
        vl = T("vesicle", 28, YELLOW).move_to(ER_C + RIGHT * 1.2 + DOWN * 1.45)
        self.play(FadeIn(vl), run_time=0.4)
        self.at("small bubble of membrane")
        self.play(Indicate(ves[0], color=YELLOW, scale_factor=1.5), run_time=0.8)
        gb = golgi()
        gl = T("Golgi apparatus", 28, GREEN).move_to(GO_C + LEFT * 0.3 + UP * 1.35)
        self.at("buds off")
        self.play(FadeIn(gb, shift=UP * 0.1), FadeIn(gl), ves.animate.move_to(ER_C + RIGHT * 1.9 + DOWN * 0.6), FadeOut(vl), run_time=0.9)
        self.at("delivers the protein")
        self.play(ves.animate.move_to(GO_C + LEFT * 1.55 + DOWN * 0.6), run_time=1.0)
        self.play(ves[1].animate.move_to(GO_C + DOWN * 0.6), FadeOut(ves[0]), run_time=0.6)
        self.play(FadeOut(ves[1]), run_time=0.3)
        self.at("sorts the protein")
        self.play(Indicate(gb, color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("new vesicles")
        vs = [vesicle(p) for p in VPOS]
        self.play(LaggedStart(*[FadeIn(v, scale=0.4) for v in vs], lag_ratio=0.3), run_time=1.1)
        self.at("stored in these vesicles")
        sl = T("storage\nvesicles", 28, YELLOW, line_spacing=0.9).move_to([2.3, -1.95, 0])
        self.play(FadeIn(sl), run_time=0.5)
        self.finish()


class S05Release(SpokenScene):
    def construct(self):
        d = base(self)
        top = topline("4  Out through the cell membrane")
        self.add(top)
        erb = er(); rb = ribos()
        erl = T("ER", 28, TEAL_).move_to(ER_C + DOWN * 1.45)
        gb = golgi(); gl = T("Golgi apparatus", 28, GREEN).move_to(GO_C + LEFT * 0.3 + UP * 1.35)
        vs = [vesicle(p) for p in VPOS]
        self.add(erb, rb, erl, gb, gl, *vs)
        self.at("more of these vesicles")
        ml = T("cell membrane", 28, GREY).move_to([3.7, 2.5, 0])
        mla = Arrow(ml.get_bottom(), np.array([4.5, 0.9, 0]), color=GREY, buff=0.08, stroke_width=3, tip_length=0.18)
        self.play(FadeIn(ml), GrowArrow(mla), vs[0].animate.move_to([4.5, 0.4, 0]), vs[1].animate.move_to([4.75, -0.5, 0]), run_time=1.3)
        self.at("fuse with the cell membrane")
        self.play(vs[0].animate.move_to([4.85, 0.4, 0]), vs[1].animate.move_to([5.0, -0.5, 0]), run_time=0.8)
        self.at("releases insulin outside")
        il = T("insulin", 28, YELLOW).move_to([5.9, 1.05, 0])
        self.play(vs[0][1].animate.shift(RIGHT * 0.8), vs[1][1].animate.shift(RIGHT * 0.8),
                  vs[0][0].animate.set_stroke(opacity=0.3), vs[1][0].animate.set_stroke(opacity=0.3), FadeIn(il), run_time=1.0)
        self.at("between meals")
        self.play(vs[2].animate.move_to([4.7, -1.4, 0]), run_time=0.9)
        self.play(vs[2][1].animate.shift(RIGHT * 0.8), vs[2][0].animate.set_stroke(opacity=0.3), run_time=0.6)
        self.at("both use energy")
        m1, m2, ml1 = mito_set()
        self.play(FadeIn(m1, scale=0.7), FadeIn(m2, scale=0.7), FadeIn(ml1), run_time=0.8)
        self.at("Mitochondria release energy")
        self.play(Indicate(m1, color=ORANGE, scale_factor=1.15), Indicate(m2, color=ORANGE, scale_factor=1.15), run_time=0.9)
        self.at("store it in")
        a1, a2, t1, t2 = atp_set()
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(t1), FadeIn(t2), run_time=0.8)
        self.at("cell parts can use")
        self.play(Indicate(VGroup(t1, t2), color=ORANGE, scale_factor=1.15), run_time=0.9)
        self.finish()


class S06Answer(SpokenScene):
    def construct(self):
        d = base(self)
        top = topline("How do the parts work together?")
        self.add(top)
        erb = er(); rb = ribos()
        erl = T("ER", 28, TEAL_).move_to(ER_C + DOWN * 1.45)
        gb = golgi(); gl = T("Golgi apparatus", 28, GREEN).move_to(GO_C + LEFT * 0.3 + UP * 1.35)
        m1, m2, ml1 = mito_set()
        self.add(erb, rb, erl, gb, gl, m1, m2, ml1)
        r1 = Arrow(NUC + RIGHT * 1.55 + UP * 0.2, ER_C + LEFT * 1.3 + UP * 0.2, color=PURPLE, buff=0.05, stroke_width=5, tip_length=0.2)
        r2 = Arrow(ER_C + RIGHT * 1.3 + DOWN * 0.3, GO_C + LEFT * 1.2 + DOWN * 0.3, color=YELLOW, buff=0.05, stroke_width=5, tip_length=0.2)
        r3 = Arrow(GO_C + RIGHT * 1.2 + DOWN * 0.3, EDGE + LEFT * 0.35, color=YELLOW, buff=0.05, stroke_width=5, tip_length=0.2)
        self.at("hands its product")
        self.play(GrowArrow(r1), run_time=0.4)
        self.play(GrowArrow(r2), run_time=0.4)
        self.play(GrowArrow(r3), run_time=0.4)
        self.at("keeps the instructions")
        self.play(d["nuc"][0].animate.set_stroke(width=9), run_time=0.5)
        self.at("Ribosomes build the protein")
        self.play(d["nuc"][0].animate.set_stroke(width=4), Indicate(rb, color=PINK, scale_factor=1.4), run_time=0.7)
        self.at("folds it")
        self.play(Indicate(erb, color=TEAL_, scale_factor=1.06), run_time=0.7)
        self.at("Vesicles carry it")
        v = vesicle(ER_C + RIGHT * 1.9 + DOWN * 0.6)
        self.play(FadeIn(v, scale=0.5), run_time=0.4)
        self.play(v.animate.move_to(GO_C + LEFT * 1.55 + DOWN * 0.6), run_time=0.7)
        self.at("sorts and packs it")
        self.play(FadeOut(v), Indicate(gb, color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("The membrane lets it out")
        v2 = vesicle(GO_C + RIGHT * 1.9 + DOWN * 0.3)
        self.play(FadeIn(v2, scale=0.5), run_time=0.3)
        self.play(v2.animate.move_to([4.85, -0.3, 0]), run_time=0.8)
        self.play(v2[1].animate.shift(RIGHT * 0.8), v2[0].animate.set_stroke(opacity=0.3), run_time=0.5)
        self.at("Mitochondria supply")
        a1, a2, t1, t2 = atp_set()
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(t1), FadeIn(t2), run_time=0.7)
        self.at("A factory is a useful model")
        self.play(Transform(top, T("A model: no manager gives orders", 36, TEXT, font=TITLE_FONT).move_to([0, 3.3, 0])), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Cell parts pass a protein along, using ATP."
