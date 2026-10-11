"""Calcineurin and NFAT: a phosphatase opens the door  (Biochemistrypedia section film)

COLOR MAP (one color per concept, whole video)
  PURPLE = transcription factors (CREB, NFAT, Fos-Jun)
  GOLD   = a phosphate (the little "P" badge)
  YELLOW = NFAT's import signal (the tag)
  TEAL   = calcium and calcium-calmodulin
  BLUE   = calcineurin (the phosphatase)
  PINK   = kinases
  ORANGE = the two drugs
  STEEL  = the drugs' helper proteins
  GREEN  = ON / more / up
  RED    = blocked, inhibited, shut down
  GREY   = membranes, outlines, the receptor, the gene, labels
Phosphate count and positions are schematic (marked on screen).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88AB8"
STEEL = "#A9BDD6"

N0 = np.array([-2.2, -1.0, 0])      # NFAT resting place in the cytoplasm
SLOTS = [(-0.9, 0.2), (-0.47, 0.5), (0.0, 0.64), (0.47, 0.5), (0.9, 0.2)]


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def set_chip(c, color, opa=1.0):
    return [c[1].animate.set_stroke(color, opacity=opa).set_fill(color, 0.16 * opa), c[2].animate.set_color(color).set_opacity(opa)]


def dimmed(c, o=0.35):
    c[1].set_stroke(opacity=o).set_fill(opacity=0.16 * o)
    c[2].set_opacity(o)
    return c


def pbadge(size=0.2):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def blob(text, color=PURPLE, w=2.0, h=1.2, size=30):
    e = Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    return VGroup(e, T(text, size, TEXT).move_to(e))


class NF:
    """NFAT: a purple blob, a yellow import-signal tag on top, and gold phosphates over the tag."""

    def __init__(self, c, phos=True, tag=True, label="NFAT"):
        self.c = np.array(c, float)
        self.body = blob(label, PURPLE, 1.9, 1.2, 28).move_to(self.c)
        self.tag = RoundedRectangle(corner_radius=0.06, width=0.9, height=0.3, stroke_color=YELLOW, stroke_width=2,
                                    fill_color=YELLOW, fill_opacity=0.9).move_to(self.c + [0, 0.62, 0])
        if not tag:
            self.tag.set_opacity(0)
        self.badges = [pbadge().move_to(self.c + [sx, sy, 0]) for sx, sy in SLOTS]
        if not phos:
            for b in self.badges:
                b.set_opacity(0)

    def parts(self):
        return VGroup(self.body, self.tag, *self.badges)

    def slot(self, i):
        return self.c + [SLOTS[i][0], SLOTS[i][1], 0]

    def go(self, p):
        d = np.array(p, float) - self.c
        self.c = np.array(p, float)
        return self.parts().animate.shift(d)


def stage(rec=True):
    mem = RoundedRectangle(corner_radius=0.1, width=12.6, height=0.32, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.35).move_to([0, 3.05, 0])
    nuc = RoundedRectangle(corner_radius=0.3, width=5.0, height=4.5, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.08).move_to([3.5, -0.95, 0])
    nuc_l = T("nucleus", 24, GREY).move_to([3.5, 0.95, 0])
    cyt_l = T("cytoplasm", 24, GREY).move_to([-1.2, -2.6, 0])
    g = VGroup(mem, nuc, nuc_l, cyt_l)
    r = None
    if rec:
        r = bchip("T-cell receptor", GREY, 22).move_to([-4.8, 2.5, 0])
        g.add(r)
    return g, r


def schematic_note():
    return T("schematic: not to scale, phosphate count idealised", 22, GREY).move_to([0, -3.4, 0])


class S00Title(TitleCard):
    LESSON = "Signaling to the Nucleus: CREB, AP-1 and Immediate Early Genes"
    TITLE = "Taking Phosphates Off Opens the Door"


# ---------------------------------------------------------------------------------------------
class S01Door(SpokenScene):
    def construct(self):
        # --- two switches side by side -------------------------------------------------------
        creb = blob("CREB", PURPLE).move_to([-3.4, 0.8, 0])
        self.play(FadeIn(creb, scale=0.9), run_time=0.6)
        cb = pbadge().move_to([-1.2, 2.0, 0])
        self.at("adding a phosphate")
        self.play(FadeIn(cb), run_time=0.2)
        self.play(cb.animate.move_to(creb.get_center() + [0.55, 0.45, 0]), run_time=0.6)
        on1 = T("ON", 34, GREEN, weight=BOLD).move_to([-3.4, 2.1, 0])
        cap1 = T("add a phosphate", 26, GOLD).move_to([-3.4, -0.5, 0])
        self.play(FadeIn(on1, shift=DOWN * 0.1), FadeIn(cap1), creb[0].animate.set_stroke(GREEN), run_time=0.5)

        nf = NF([3.4, 0.8, 0], tag=False)
        self.at("NFAT")
        self.play(FadeIn(nf.body, scale=0.9), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in nf.badges], lag_ratio=0.12), run_time=0.7)
        self.at("taking phosphates off")
        self.play(LaggedStart(*[b.animate.shift(UP * 1.1 + RIGHT * 0.1 * (i - 2)).set_opacity(0) for i, b in enumerate(nf.badges)],
                              lag_ratio=0.12), run_time=1.0)
        on2 = T("ON", 34, GREEN, weight=BOLD).move_to([3.4, 2.1, 0])
        cap2 = T("take phosphates off", 26, GOLD).move_to([3.4, -0.5, 0])
        self.play(FadeIn(on2, shift=DOWN * 0.1), FadeIn(cap2), nf.body[0].animate.set_stroke(GREEN), run_time=0.5)

        # --- the resting cell --------------------------------------------------------------
        st, rec = stage()
        for b in nf.badges:
            b.set_opacity(1)
        nf2 = NF(N0, tag=True)
        rest = T("resting T cell", 24, GREY).move_to([3.5, 2.5, 0])
        self.at("resting")
        self.play(FadeOut(VGroup(creb, cb, on1, cap1, nf.body, on2, cap2, *nf.badges)),
                  FadeIn(st), FadeIn(rest), run_time=0.7)
        self.play(FadeIn(nf2.body, scale=0.9), FadeIn(nf2.tag), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in nf2.badges], lag_ratio=0.1), run_time=0.6)
        note = schematic_note()
        self.play(FadeIn(note), run_time=0.3)
        self.at("stays in the cytoplasm")
        self.play(Wiggle(nf2.parts(), scale_value=1.04, rotation_angle=0.02 * TAU), run_time=0.7)
        self.at("many phosphates")
        self.play(*[Indicate(b, color=GOLD, scale_factor=1.3) for b in nf2.badges], run_time=0.8)
        self.at("hide its signal")
        lab = T("import signal", 24, YELLOW).move_to(N0 + [1.25, 1.2, 0])
        ln = Line(lab.get_left() + [-0.05, 0, 0], nf2.tag.get_right() + [0.06, 0.0, 0], color=YELLOW, stroke_width=3)
        self.play(FadeIn(lab, shift=LEFT * 0.1), Create(ln), Indicate(nf2.tag, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Strip(SpokenScene):
    def construct(self):
        st, rec = stage()
        nf = NF(N0, tag=True)
        self.add(st, nf.parts())
        calc = bchip("calcineurin", BLUE, 26).move_to([-4.8, -2.3, 0])
        dimmed(calc)
        self.add(calc)
        rs = np.random.RandomState(3)
        dots = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=TEAL, fill_opacity=1)
                        .move_to([rs.uniform(-5.8, -0.7), rs.uniform(0.75, 1.75), 0]) for _ in range(16)])

        self.at("receptor fires")
        self.play(Indicate(rec, color=YELLOW, scale_factor=1.15), rec[1].animate.set_stroke(YELLOW), run_time=0.6)
        self.at("calcium rises")
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.3) for d in dots], lag_ratio=0.06), run_time=1.1)
        hi = T("calcium stays high", 24, TEAL).move_to([-1.5, 2.45, 0])
        self.at("stays high")
        self.play(FadeIn(hi), run_time=0.4)

        cam = bchip("calcium-calmodulin", TEAL, 22).move_to([-4.4, 0.3, 0])
        self.at("Calcium and calmodulin")
        self.play(ReplacementTransform(VGroup(*dots[:5]), cam), run_time=0.7)
        self.at("switch on calcineurin")
        link = arr(cam.get_bottom(), [-4.8, -1.95, 0], TEAL, w=4)
        self.play(GrowArrow(link), *set_chip(calc, BLUE), run_time=0.6)
        plbl = T("protein phosphatase", 22, GREY).move_to([-4.8, -2.9, 0])
        self.at("protein phosphatase")
        self.play(FadeIn(plbl), run_time=0.4)

        self.at("strips the")
        grp = VGroup(calc, plbl)
        self.play(FadeOut(link), calc.animate.move_to([-4.4, -1.0, 0]), plbl.animate.move_to([-4.4, -1.7, 0]), run_time=0.8)
        self.at("phosphates from")
        self.play(LaggedStart(*[b.animate.shift([-0.6, 0.9, 0]).set_opacity(0) for b in nf.badges], lag_ratio=0.1),
                  run_time=1.0)
        lab = T("import signal", 24, YELLOW).move_to(N0 + [1.25, 1.2, 0])
        ln = Line(lab.get_left() + [-0.05, 0, 0], nf.tag.get_right() + [0.06, 0, 0], color=YELLOW, stroke_width=3)
        self.at("signal is exposed")
        self.play(FadeIn(lab, shift=LEFT * 0.1), Create(ln), Indicate(nf.tag, color=YELLOW, scale_factor=1.4),
                  nf.tag.animate.set_stroke(YELLOW, width=5), run_time=0.8)

        self.at("enters the nucleus")
        self.play(FadeOut(lab), FadeOut(ln), nf.go([3.4, -0.1, 0]), run_time=1.1)
        dna = Line([1.4, -2.45, 0], [5.6, -2.45, 0], color=GREY, stroke_width=6)
        self.at("binds DNA")
        self.play(Create(dna), nf.go([4.75, -1.35, 0]), run_time=0.9)
        fj = bchip("Fos-Jun", PURPLE, 22).move_to([2.7, -1.35, 0])
        self.at("beside")
        self.play(FadeIn(fj, scale=0.9), run_time=0.5)
        gene = bchip("interleukin-2 gene", GREY, 22).move_to([3.6, -2.45, 0])
        self.at("interleukin")
        self.play(FadeIn(gene), run_time=0.5)

        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Drugs(SpokenScene):
    def construct(self):
        tc = bchip("T cell", GREY, 28).move_to([0, 2.7, 0])
        csa = bchip("cyclosporin A", ORANGE, 24).move_to([-4.3, 2.7, 0])
        fk = bchip("FK506", ORANGE, 24).move_to([4.3, 2.7, 0])
        self.at("Cyclosporin A")
        self.play(FadeIn(tc), FadeIn(csa, shift=RIGHT * 0.3), run_time=0.5)
        self.at("FK506")
        self.play(FadeIn(fk, shift=LEFT * 0.3), run_time=0.5)
        tc2 = bchip("T cell shut down", RED, 28).move_to(tc)
        bl = inhib(csa.get_right() + [0.05, 0, 0], tc2.get_left() + [-0.05, 0, 0], RED)
        br = inhib(fk.get_left() + [-0.05, 0, 0], tc2.get_right() + [0.05, 0, 0], RED)
        self.at("both shut")
        self.play(Create(bl), Create(br), ReplacementTransform(tc, tc2), run_time=0.8)

        def cup(label):
            s = Sector(radius=0.95, start_angle=PI, angle=PI, stroke_color=STEEL, stroke_width=4,
                       fill_color=STEEL, fill_opacity=0.28)
            t = T(label, 22, TEXT).move_to(s.get_center() + [0, -0.12, 0])
            t.move_to([s.get_center()[0], s.get_top()[1] - 0.45, 0])
            return VGroup(s, t)

        h1 = cup("cyclophilin")
        h2 = cup("FKBP12")
        h1.move_to([-4.3, 2.7 - 0.36 - 0.475, 0])
        h2.move_to([4.3, 2.7 - 0.36 - 0.475, 0])
        self.at("small helper")
        self.play(FadeIn(h1, shift=UP * 0.3), FadeIn(h2, shift=UP * 0.3), run_time=0.7)
        self.at("FKBP12")
        self.play(Indicate(h2, color=STEEL, scale_factor=1.08), run_time=0.7)
        self.at("cyclophilin")
        self.play(Indicate(h1, color=STEEL, scale_factor=1.08), run_time=0.7)

        calc = bchip("calcineurin", BLUE, 30).move_to([0, -1.2, 0])
        pair1 = VGroup(csa, h1)
        pair2 = VGroup(fk, h2)
        self.at("In 1991")
        who = T("Schreiber's group and collaborators, 1991", 22, GREY).move_to([0, -3.2, 0])
        self.play(FadeOut(VGroup(bl, br)), FadeIn(calc), FadeIn(who), run_time=0.6)
        self.at("binds and inhibits")
        self.play(pair1.animate.move_to([-2.95, -1.2 + 0.0, 0]).shift(DOWN * 0.0), pair2.animate.move_to([2.95, -1.2, 0]), run_time=1.0)
        ib1 = inhib(pair1.get_right() + [0.02, 0, 0], calc.get_left() + [-0.02, 0, 0])
        ib2 = inhib(pair2.get_left() + [-0.02, 0, 0], calc.get_right() + [0.02, 0, 0])
        self.play(Create(ib1), Create(ib2), *set_chip(calc, RED), run_time=0.6)
        tube = T("in a test tube", 24, GREY).move_to([0, -2.3, 0])
        self.at("test tube")
        self.play(FadeIn(tube), run_time=0.4)
        q = T("?", 56, TEXT, weight=BOLD).move_to([0.6, 0.75, 0])
        dl = DashedLine([0, -0.55, 0], [0, 2.2, 0], color=TEXT, stroke_width=4)
        self.at("Is that why")
        self.play(Create(dl), FadeIn(q, scale=0.6), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Test(SpokenScene):
    def construct(self):
        who = T("Neil Clipstone and Gerald Crabtree, 1992", 28, TEXT).move_to([0, 3.0, 0])
        box = RoundedRectangle(corner_radius=0.3, width=6.4, height=3.4, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.08).move_to([0, 0.8, 0])
        tcl = T("T cell", 24, GREY).move_to(box.get_top() + [-2.6, -0.3, 0])
        self.at("In 1992")
        self.play(FadeIn(who, shift=DOWN * 0.1), FadeIn(box), FadeIn(tcl), run_time=0.7)
        rs = np.random.RandomState(5)
        pts = []
        while len(pts) < 14:
            p = np.array([rs.uniform(-2.8, 2.8), rs.uniform(-0.55, 2.0), 0])
            if all(np.linalg.norm(p - q) > 0.62 for q in pts) and not (p[0] < -1.6 and p[1] > 1.6):
                pts.append(p)
        enz = VGroup(*[Ellipse(width=0.5, height=0.34, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
                       .move_to(p) for p in pts])
        elab = T("extra calcineurin", 26, BLUE).move_to([0, -1.3, 0])
        self.at("extra calcineurin")
        self.play(LaggedStart(*[FadeIn(e, scale=0.4) for e in enz], lag_ratio=0.07), FadeIn(elab), run_time=1.2)

        csa = bchip("cyclosporin A", ORANGE, 24).move_to([-4.85, 0.8, 0])
        fk = bchip("FK506", ORANGE, 24).move_to([4.85, 0.8, 0])
        a1 = arr(csa.get_right(), [-3.3, 0.8, 0], ORANGE, w=4)
        a2 = arr(fk.get_left(), [3.3, 0.8, 0], ORANGE, w=4)
        self.at("more resistant")
        self.play(FadeIn(csa, shift=RIGHT * 0.3), FadeIn(fk, shift=LEFT * 0.3), GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        r1 = T("more resistant to both drugs", 26, GREEN).move_to([0, -2.0, 0])
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        r2 = T("NFAT-driven transcription: up", 26, GREEN).move_to([0, -2.75, 0])
        up = Arrow([4.0, -2.95, 0], [4.0, -2.45, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.22)
        self.at("transcription went up")
        self.play(FadeIn(r2, shift=UP * 0.1), GrowArrow(up), run_time=0.6)

        self.at("If more enzyme")
        c1 = bchip("more enzyme", BLUE, 24).move_to([-4.3, -2.35, 0])
        c2 = bchip("more drug needed", ORANGE, 24).move_to([0.05, -2.35, 0])
        c3 = bchip("the enzyme is the target", BLUE, 24).move_to([4.2, -2.35, 0])
        k1 = arr(c1.get_right(), c2.get_left(), GREY, w=4)
        k2 = arr(c2.get_right(), c3.get_left(), GREY, w=4)
        self.play(FadeOut(VGroup(r1, r2, up, csa, fk, a1, a2, elab)), run_time=0.5)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.4)
        self.at("more drug is needed")
        self.play(GrowArrow(k1), FadeIn(c2), run_time=0.5)
        self.at("the enzyme is the target")
        self.play(GrowArrow(k2), FadeIn(c3), run_time=0.6)

        # --- jam ---------------------------------------------------------------------------
        st, _ = stage(rec=False)
        nf = NF(N0, tag=True)
        calc = bchip("calcineurin", BLUE, 26).move_to([-4.4, -1.0, 0])
        jam = T("jammed", 24, RED).move_to([-4.4, -1.65, 0])
        dna = Line([1.4, -2.45, 0], [5.6, -2.45, 0], color=GREY, stroke_width=6)
        gene = bchip("interleukin-2 gene", GREY, 22).move_to([3.6, -2.45, 0])
        self.at("Jam calcineurin")
        self.play(FadeOut(VGroup(who, box, tcl, enz, c1, c2, c3, k1, k2)), FadeIn(st), FadeIn(nf.parts()),
                  FadeIn(calc), FadeIn(dna), FadeIn(gene), run_time=0.8)
        self.play(*set_chip(calc, RED), FadeIn(jam), run_time=0.5)
        self.at("keeps its phosphates")
        self.play(*[Indicate(b, color=GOLD, scale_factor=1.3) for b in nf.badges], run_time=0.8)
        stay = DashedLine(N0 + [1.2, 0, 0], [0.7, -1.0, 0], color=GREY, stroke_width=4)
        xm = T("✕", 34, RED, weight=BOLD).move_to([-0.15, -1.0, 0])
        xb = Circle(radius=0.24, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(xm)
        xm = VGroup(xb, xm)
        self.at("stays in the cytoplasm")
        self.play(Create(stay), FadeIn(xm), run_time=0.6)
        quiet = T("quiet", 24, GREY).move_to([3.6, -1.8, 0])
        self.at("stays quiet")
        self.play(FadeIn(quiet), run_time=0.4)
        self.finish()


class S05End(EndCard):
    LINE = "Jam calcineurin and NFAT keeps its phosphates."
