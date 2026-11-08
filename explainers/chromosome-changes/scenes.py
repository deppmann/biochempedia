"""Chromosome changes: one missed separation, one extra chromosome  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = homologue "A" of the parent being followed (chromosome 21A)
  YELLOW = homologue "B" of the same parent (21B)
  GREY   = everything else: cells, outlines, the other parent's chromosomes, arrows, labels
  RED    = the error and its abnormal products (failure to part, disomic, nullisomic, three copies,
           the verdict chips)
  GREEN  = a normal product
  TEAL   = the division that is running (meiosis I / meiosis II chip)
  TEXT   = the marker band on a chromosome
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

# stage for the meiosis scenes
X0, X1, X2 = -5.0, -1.2, 2.6
SEC_Y = [1.48, -1.48]
SP_Y = [2.2, 0.75, -0.75, -2.2]
R0, R1, R2 = 1.05, 0.85, 0.58
CAP_H = 0.7


def capsule(color, h=CAP_H, w=0.17, op=0.85):
    return RoundedRectangle(corner_radius=w / 2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=op)


def chromo(color, n=2, h=CAP_H):
    """A chromosome as n side-by-side chromatids (n=2: sisters still joined)."""
    caps = [capsule(color, h) for _ in range(n)]
    g = VGroup(*caps).arrange(RIGHT, buff=0.03)
    g.caps = caps
    return g


def cell(x, y, r, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.07).move_to([x, y, 0])


def arr(a, b, color=GREY, w=4):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def div_chip(text, color=GREY, x=0.0):
    c = chip(text, color, size=26)
    return c.move_to([x, 3.2, 0])


def sperm_icon(n, x, y):
    c = Circle(radius=0.36, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.1)
    caps = VGroup(*[capsule(BLUE, h=0.4, w=0.11) for _ in range(n)]).arrange(RIGHT, buff=0.04)
    return VGroup(c, caps.move_to(c)).move_to([x, y, 0])


def tall(color, label, h=3.0, w=0.32):
    """A whole chromosome with its marker band at the centromere; the band carries the allele number."""
    body = capsule(color, h=h, w=w, op=0.8)
    band = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.44, fill_color=TEXT, fill_opacity=1,
                            stroke_color=color, stroke_width=3).move_to(body)
    num = M(label, 26, BG, weight=BOLD).move_to(band)
    g = VGroup(body, band, num)
    g.body, g.band, g.num = body, band, num
    g.bn = VGroup(band, num)
    return g


def homologue_pair(x, y=0.3):
    a = tall(BLUE, "3").move_to([x - 0.8, y, 0])
    b = tall(YELLOW, "4").move_to([x + 0.8, y, 0])
    return VGroup(a, b)


def sister_pair(x, y=0.3):
    a = tall(BLUE, "3").move_to([x - 0.38, y, 0])
    b = tall(BLUE, "3").move_to([x + 0.38, y, 0])
    link = Line(a.band.get_right(), b.band.get_left(), color=TEXT, stroke_width=6)
    return VGroup(a, b, link)


HEAD_Y = 3.2


def column_label(text, x, y=1.95):
    return T(text, 26, GREY).move_to([x, y, 0])


def verdict(text, x=-3.4, y=-2.8):
    return chip(text, RED, size=30).move_to([x, y, 0])


# The original capsule, cell, chromosome and marker helpers are retained above.
# Gene bands below are schematic positions, not a molecular structure.
def gene_chromosome(color, x, y=0.25, h=2.6):
    body = capsule(color, h=h, w=0.30).move_to([x, y, 0])
    bands = VGroup(*[
        Rectangle(width=0.48, height=0.13, stroke_width=0,
                  fill_color=TEXT, fill_opacity=1).move_to([x, y + dy, 0])
        for dy in (-0.75, 0, 0.75)
    ])
    return VGroup(body, bands)


def heading(text, color=TEXT):
    return T(text, 32, color, weight=BOLD).move_to([0, 3.15, 0])


def start_model():
    st = cell(X0, 0, R0)
    a = chromo(BLUE).move_to([X0 - 0.35, 0, 0])
    b = chromo(YELLOW).move_to([X0 + 0.35, 0, 0])
    return st, a, b


def secondary_cells():
    return [cell(X1, y, R1) for y in SEC_Y]


def product_cells():
    return [cell(X2, y, R2) for y in SP_Y]


def first_arrows():
    return VGroup(*[arr([X0 + R0 + 0.05, 0.3 * sign, 0],
                       [X1 - R1 - 0.05, y - 0.15 * sign, 0])
                   for sign, y in zip((1, -1), SEC_Y)])


def second_arrows():
    return VGroup(*[arr([X1 + R1 + 0.05, y, 0], [X2 - R2 - 0.05, sy, 0])
                   for y, pr in zip(SEC_Y, [SP_Y[:2], SP_Y[2:]]) for sy in pr])


class S00Title(TitleCard):
    LESSON = "Chromosome number and structure"
    TITLE = "One Missed Separation, One Extra Chromosome"

    def construct(self):
        title = T(self.TITLE, 44, font=TITLE_FONT)
        fit(title, max_w=12.2)
        sub = T("Chromosome dose changes development", 28, GREY)
        lesson = T(self.LESSON, 24, TEAL)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        group = VGroup(lesson, title, rule, sub).arrange(DOWN, buff=0.42)
        self.play(FadeIn(group), run_time=0.7)
        self.finish()


class S01Count(SpokenScene):
    def construct(self):
        head = heading("Chromosome 21: two copies")
        a = gene_chromosome(BLUE, -1.0)
        b = gene_chromosome(YELLOW, 0)
        c = gene_chromosome(RED, 1.0)
        self.at("A cell")
        self.play(FadeIn(head), FadeIn(a), FadeIn(b), run_time=0.5)
        self.at("an extra")
        self.play(FadeIn(c, shift=DOWN * 0.3),
                  Transform(head, heading("Chromosome 21: extra gene copies", RED)), run_time=0.7)
        dose = T("Extra chromosome → extra gene dose", 30, RED).move_to([0, -1.7, 0])
        self.at("the wrong dose")
        self.play(FadeIn(dose), Indicate(c[1], color=RED), run_time=0.7)
        dev = T("→ altered development", 30, TEXT).move_to([0, -2.5, 0])
        self.at("That can change")
        self.play(FadeIn(dev), run_time=0.6)
        warning = T("Most aneuploid human embryos\ndo not survive pregnancy", 30, TEXT,
                    line_spacing=1.15).move_to([0, -2.15, 0])
        self.at("Most aneuploid")
        self.play(FadeOut(dose), FadeOut(dev), FadeIn(warning), run_time=0.6)
        example = T("Trisomy 21: seen regularly at birth", 30, TEXT).move_to([0, -1.8, 0])
        self.at("Trisomy 21")
        self.play(FadeOut(warning), FadeIn(example), run_time=0.6)
        self.at("three copies")
        self.play(Indicate(VGroup(a, b, c), color=TEXT, scale_factor=1.08), run_time=0.7)
        down = T("Down syndrome", 32, RED).move_to([0, -2.55, 0])
        self.at("causes down syndrome")
        self.play(FadeIn(down), run_time=0.5)
        self.at("The important change")
        self.play(FadeOut(example), FadeOut(down), FadeIn(dose),
                  Indicate(c[1], color=RED), run_time=0.6)
        question = T("How does a cell get that extra chromosome?", 30, TEXT).move_to([0, -2.6, 0])
        self.at("How does")
        self.play(FadeIn(question), run_time=0.6)
        self.finish()


class S01XDose(SpokenScene):
    def construct(self):
        head = heading("Extra X chromosomes are better tolerated")
        c21 = gene_chromosome(RED, -4.2)
        c21label = T("Extra 21", 28, RED).move_to([-4.2, 2.15, 0])
        x1 = gene_chromosome(BLUE, 0.5)
        x2 = gene_chromosome(YELLOW, 2.1)
        xs = T("X               X", 28, TEXT).move_to([1.3, 2.15, 0])
        self.at("Extra X chromosomes")
        self.play(FadeIn(head), FadeIn(c21), FadeIn(c21label), FadeIn(x1), FadeIn(x2), FadeIn(xs), run_time=0.7)
        note = T("Most extra X genes silenced; some escape", 30, TEXT).move_to([0, -2.05, 0])
        self.at("silence every X")
        # Dim the body and two gene bands, preserving one lit escape position.
        self.play(x2[0].animate.set_opacity(0.20),
                  x2[1][0].animate.set_opacity(0.18), x2[1][1].animate.set_opacity(0.18),
                  FadeIn(note), run_time=1.0)
        self.at("some genes escape")
        self.play(Indicate(x1[1][2], color=TEXT), Indicate(x2[1][2], color=TEXT), run_time=0.8)
        thought = T("Extra active escape-gene copies\nmay explain many features", 28, TEXT).move_to([0, -2.7, 0])
        self.at("are thought to explain")
        self.play(FadeOut(note), FadeIn(thought), run_time=0.6)
        syndrome = heading("Klinefelter syndrome", RED)
        self.at("Klinefelter syndrome")
        self.play(Transform(head, syndrome), run_time=0.5)
        y = capsule(GREY, h=1.5, w=0.3).move_to([3.7, 0.25, 0])
        ylabel = T("Y", 28, GREY).move_to([3.7, 2.15, 0])
        male = T("XXY male", 28, TEXT).move_to([2.1, -1.45, 0])
        self.at("usually an extra X")
        self.play(FadeOut(c21), FadeOut(c21label), FadeIn(y), FadeIn(ylabel), FadeIn(male), run_time=0.7)
        self.finish()


class S02Divisions(SpokenScene):
    def construct(self):
        head = heading("Nondisjunction: failure to part", RED)
        st, a, b = start_model()
        self.at("Nondisjunction")
        self.play(FadeIn(head), FadeIn(st), FadeIn(a), FadeIn(b), run_time=0.6)
        ring = SurroundingRectangle(VGroup(a, b), color=RED, buff=0.1, corner_radius=0.1)
        self.at("failure of chromosomes")
        self.play(Create(ring), VGroup(a, b).animate.shift(RIGHT * 0.25), run_time=0.6)
        secs = secondary_cells()
        arrows1 = first_arrows()
        self.at("At meiosis 1")
        self.play(FadeOut(ring), Transform(head, heading("Meiosis I: homologue separation", TEAL)),
                  *[FadeIn(c) for c in secs], GrowArrow(arrows1[0]), GrowArrow(arrows1[1]),
                  a.animate.move_to([X1, SEC_Y[0], 0]), b.animate.move_to([X1, SEC_Y[1], 0]), run_time=1.4)
        sps = product_cells()
        arrows2 = second_arrows()
        self.at("At meiosis 2")
        self.play(FadeOut(st), FadeOut(arrows1),
                  Transform(head, heading("Meiosis II: sister separation", TEAL)),
                  *[FadeIn(c) for c in sps], *[GrowArrow(ar) for ar in arrows2], run_time=0.5)
        self.at("the sister chromatids")
        self.play(a.caps[0].animate.move_to([X2, SP_Y[0], 0]),
                  a.caps[1].animate.move_to([X2, SP_Y[1], 0]),
                  b.caps[0].animate.move_to([X2, SP_Y[2], 0]),
                  b.caps[1].animate.move_to([X2, SP_Y[3], 0]), run_time=1.0)
        self.at("Follow chromosome")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        st, a, b = start_model()
        label = T("Human spermatocyte\nchromosome 21", 28, TEXT).move_to([-2.0, 0, 0])
        self.play(FadeIn(st), FadeIn(a), FadeIn(b), FadeIn(label), run_time=0.45)
        assumptions = VGroup(T("One error", 30, RED), T("Other divisions normal", 30, TEXT),
                             T("All four products recovered", 30, TEXT)).arrange(DOWN, buff=0.45).move_to([2.9, 0, 0])
        self.at("Assume one error")
        self.play(FadeIn(assumptions[0]), run_time=0.5)
        self.at("otherwise normal divisions")
        self.play(FadeIn(assumptions[1]), run_time=0.5)
        self.at("recovery of all")
        self.play(FadeIn(assumptions[2]), run_time=0.5)
        self.finish()


class S03First(SpokenScene):
    def construct(self):
        st, a, b = start_model()
        head = heading("Meiosis I: both homologues stay together", RED)
        self.at("Suppose both homologues")
        self.play(FadeIn(st), FadeIn(a), FadeIn(b), FadeIn(head), run_time=0.5)
        secs = secondary_cells()
        ars = first_arrows()
        self.at("the same cell")
        self.play(*[FadeIn(c) for c in secs], *[GrowArrow(ar) for ar in ars],
                  a.animate.move_to([X1 - 0.3, SEC_Y[0], 0]),
                  b.animate.move_to([X1 + 0.3, SEC_Y[0], 0]), run_time=1.0)
        sps = product_cells()
        ars2 = second_arrows()
        self.at("Meiosis 2 then")
        self.play(FadeOut(st), FadeOut(ars),
                  Transform(head, heading("Meiosis II runs normally", TEAL)),
                  *[FadeIn(c) for c in sps], *[GrowArrow(ar) for ar in ars2], run_time=0.6)
        self.at("That cell gives")
        self.play(a.caps[0].animate.move_to([X2 - 0.12, SP_Y[0], 0]),
                  b.caps[0].animate.move_to([X2 + 0.12, SP_Y[0], 0]),
                  a.caps[1].animate.move_to([X2 - 0.12, SP_Y[1], 0]),
                  b.caps[1].animate.move_to([X2 + 0.12, SP_Y[1], 0]), run_time=1.1)
        dis = VGroup(T("disomic", 30, RED, weight=BOLD), T("two copies each", 24, GREY)).arrange(DOWN, buff=0.15).move_to([4.9, 1.48, 0])
        self.at("These are disomic")
        self.play(FadeIn(dis), sps[0].animate.set_stroke(RED), sps[1].animate.set_stroke(RED), run_time=0.6)
        self.at("The other cell")
        self.play(Indicate(secs[1], color=RED), run_time=0.7)
        self.at("Its two sperm")
        self.play(sps[2].animate.set_stroke(RED), sps[3].animate.set_stroke(RED), run_time=0.6)
        nul = VGroup(T("nullisomic", 30, RED, weight=BOLD), T("no chromosome 21", 24, GREY)).arrange(DOWN, buff=0.15).move_to([4.9, -1.48, 0])
        self.at("These are nullosomic")
        self.play(FadeIn(nul), run_time=0.6)
        self.finish()


class S04Second(SpokenScene):
    def construct(self):
        st, a, b = start_model()
        secs = secondary_cells()
        ars = first_arrows()
        head = heading("Meiosis I is normal", TEAL)
        self.at("Now")
        self.play(FadeIn(st), FadeIn(a), FadeIn(b), FadeIn(head), run_time=0.4)
        self.at("meiosis 1 is normal")
        self.play(*[FadeIn(c) for c in secs], *[GrowArrow(ar) for ar in ars],
                  a.animate.move_to([X1, SEC_Y[0], 0]), b.animate.move_to([X1, SEC_Y[1], 0]), run_time=0.9)
        ring = SurroundingRectangle(a, color=RED, buff=0.1, corner_radius=0.1)
        self.at("sisters fail")
        self.play(Transform(head, heading("Meiosis II: sisters stay together in one cell", RED)),
                  Create(ring), run_time=0.6)
        sps = product_cells()
        ars2 = second_arrows()
        self.at("This gives")
        self.play(FadeOut(st), FadeOut(ars), FadeOut(ring),
                  *[FadeIn(c) for c in sps], *[GrowArrow(ar) for ar in ars2],
                  a.caps[0].animate.move_to([X2 - 0.12, SP_Y[0], 0]),
                  a.caps[1].animate.move_to([X2 + 0.12, SP_Y[0], 0]), run_time=0.8)
        dis = T("disomic", 28, RED).move_to([4.8, SP_Y[0], 0])
        nul = T("nullisomic", 28, RED).move_to([4.8, SP_Y[1], 0])
        self.at("one disomic sperm")
        self.play(FadeIn(dis), sps[0].animate.set_stroke(RED), run_time=0.45)
        self.at("one with none")
        self.play(FadeIn(nul), sps[1].animate.set_stroke(RED), run_time=0.45)
        normal = VGroup(*[T("normal", 28, GREEN).move_to([4.8, SP_Y[i], 0]) for i in (2, 3)])
        self.at("The other cell")
        self.play(b.caps[0].animate.move_to([X2, SP_Y[2], 0]),
                  b.caps[1].animate.move_to([X2, SP_Y[3], 0]),
                  sps[2].animate.set_stroke(GREEN), sps[3].animate.set_stroke(GREEN), FadeIn(normal), run_time=0.8)
        self.at("Joined to a normal egg")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        sperm = cell(-3.0, 0, 0.85, RED)
        pair = VGroup(*[capsule(BLUE, h=1.0, w=0.2).move_to([x, 0, 0]) for x in (-3.18, -2.82)])
        egg = cell(2.8, 0, 1.0)
        ec = capsule(GREY, h=1.0, w=0.2).move_to(egg)
        sl = T("disomic sperm", 28, RED).move_to([-3, -1.5, 0])
        el = T("normal egg", 28, GREY).move_to([2.8, -1.5, 0])
        self.play(FadeIn(sperm), FadeIn(pair), FadeIn(egg), FadeIn(ec), FadeIn(sl), FadeIn(el), run_time=0.5)
        zyg = cell(0, 0, 1.5, RED)
        tri = T("Trisomy 21: three copies", 34, RED).move_to([0, -2.25, 0])
        self.at("makes a zygote")
        self.play(FadeOut(sperm), FadeOut(egg), FadeOut(sl), FadeOut(el), FadeIn(zyg),
                  pair[0].animate.move_to([-0.55, 0, 0]), pair[1].animate.move_to([0, 0, 0]),
                  ec.animate.move_to([0.55, 0, 0]), FadeIn(tri), run_time=0.9)
        self.at("A sperm with none")
        empty = cell(-3, 0, 0.85, RED)
        egg2 = cell(2.8, 0, 1.0)
        ec2 = capsule(GREY, h=1.0, w=0.2).move_to(egg2)
        nl = T("nullisomic sperm", 28, RED).move_to([-3, -1.5, 0])
        self.play(FadeOut(zyg), FadeOut(pair), FadeOut(ec), FadeOut(tri),
                  FadeIn(empty), FadeIn(egg2), FadeIn(ec2), FadeIn(nl), FadeIn(el), run_time=0.6)
        mono = T("Monosomy 21: one copy", 34, RED).move_to([0, -2.25, 0])
        self.at("makes a zygote with only")
        self.play(FadeOut(empty), FadeOut(egg2), FadeOut(nl), FadeOut(el), FadeIn(zyg),
                  ec2.animate.move_to(ORIGIN), FadeIn(mono), run_time=0.7)
        self.finish()


class S05HumanContext(SpokenScene):
    def construct(self):
        head = heading("From the model to people")
        self.at("That is the model")
        self.play(FadeIn(head), run_time=0.5)
        origin = T("Most free trisomy 21: maternal origin", 32, TEXT).move_to([0, 1.8, 0])
        division = T("Most maternal errors: meiosis I", 32, TEXT).move_to([0, 0.8, 0])
        self.at("most free trisomy")
        self.play(FadeIn(origin), run_time=0.6)
        self.at("most maternal errors")
        self.play(FadeIn(division), run_time=0.6)
        risk = T("Risk rises with maternal age", 30, TEXT).move_to([-0.6, -1.1, 0])
        up = arr([4, -2, 0], [5.1, -0.2, 0], RED, 6)
        self.at("The risk rises")
        self.play(FadeIn(risk), GrowArrow(up), run_time=0.8)
        chain = VGroup(T("Missed separation", 32, RED),
                       T("↓", 30, GREY),
                       T("Extra or missing chromosome", 32, TEXT),
                       T("↓", 30, GREY),
                       T("Altered gene dose", 32, RED),
                       T("↓", 30, GREY),
                       T("Development and survival", 32, TEXT)).arrange(DOWN, buff=0.16).move_to([0, 0, 0])
        self.at("changes chromosome number")
        self.play(FadeOut(head), FadeOut(origin), FadeOut(division), FadeOut(risk), FadeOut(up),
                  FadeIn(VGroup(*chain[:3])), run_time=0.6)
        self.at("The extra or missing")
        self.play(FadeIn(VGroup(*chain[3:5])), run_time=0.6)
        self.at("consequences for development")
        self.play(FadeIn(VGroup(*chain[5:])), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Missed separation → changed chromosome dose → consequences for development and survival."

    def construct(self):
        line = T("Missed separation → changed chromosome dose\n→ consequences for development and survival.",
                 size=32, font=TITLE_FONT, line_spacing=1.25)
        sub = T("biochemistrypedia.com", 22, TEAL)
        group = VGroup(line, sub).arrange(DOWN, buff=0.6)
        self.play(FadeIn(group), run_time=0.8)
        self.finish()
