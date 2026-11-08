"""Protein sorting: the address travels with the protein  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the signal / address (the stretch of sequence that carries sorting information)
  TEXT   = the protein chain itself (white beads)
  BLUE   = the readers: SRP, the SRP receptor, "machinery"
  INDIGO = the ER (lumen tint, Sec61)
  PINK   = GTP badge
  RED    = signal peptidase (the cutting enzyme), and stop / stays put
  ORANGE = mitochondrion
  GREEN  = chloroplast, and the "enough to sort" verdict
  MAGENTA= peroxisome
  GREY   = membranes, cell outline, ribosome, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

MAGENTA = "#D96BB0"
INDIGO = "#8A8CF5"
ORANGE = "#F29E4C"
PINK = "#F0A3C4"
PROT = TEXT
YM = -0.9          # ER membrane centre line (s03, s04)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def beads(n, ny=0, r=0.14, gap=0.04, vertical=False, yellow="start"):
    """A chain as a row of beads. vertical: index 0 is at the BOTTOM (the tip that left the ribosome first)."""
    bs = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=PROT, fill_opacity=1) for _ in range(n)])
    bs.arrange(UP if vertical else RIGHT, buff=gap)
    idx = range(ny) if yellow == "start" else range(n - ny, n)
    for i in idx:
        bs[i].set_fill(YELLOW)
    return bs


def ribosome(s=1.0):
    big = Ellipse(width=2.0, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.45)
    small = Ellipse(width=1.4, height=0.65, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.45)
    small.next_to(big, UP, buff=-0.25)
    return VGroup(big, small).scale(s)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def gtp():
    c = Circle(radius=0.36, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=1)
    return VGroup(c, T("GTP", 22, BG, weight=BOLD).move_to(c))


def mem_seg(x0, x1, y=YM):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=0.3, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def er_base():
    lumen = Rectangle(width=12.6, height=2.35, stroke_width=0, fill_color=INDIGO, fill_opacity=0.12).move_to([0, -2.225, 0])
    A, B, C = mem_seg(-6.3, 1.1), mem_seg(2.3, 6.3), mem_seg(1.1, 2.3)
    return lumen, A, B, C


def sec61():
    return VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.4, height=0.5, stroke_color=INDIGO, stroke_width=3,
                                     fill_color=INDIGO, fill_opacity=0.55).move_to([x, YM, 0]) for x in (1.3, 2.1)])


def receptor():
    return RoundedRectangle(corner_radius=0.12, width=1.1, height=0.5, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.45).move_to([-1.2, YM, 0])


def complex_at(x):
    """ribosome + label + 5-bead chain hanging down, tip just above the membrane."""
    ribo = ribosome().move_to([x, 0.78 + 0.65, 0])
    rl = T("ribosome", 24, GREY).next_to(ribo, UP, buff=0.12)
    ch = beads(5, 4, vertical=True)
    ch.move_to([x, -0.72 + ch.height / 2, 0])
    return ribo, rl, ch


def srp_at(x):
    return chip("SRP", BLUE, size=26, pad=0.18).move_to([x - 0.85, -0.17, 0])


class S00Title(TitleCard):
    LESSON = "Protein sorting into compartments"
    TITLE = "The address travels with the protein"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """test-tube product is longer than the secreted protein; the extra piece is an address, cut off."""

    def construct(self):
        XR = 3.7
        boxA = RoundedRectangle(corner_radius=0.3, width=11.6, height=2.2, stroke_color=GREY, stroke_width=3).move_to([0, 1.55, 0])
        labA = T("test tube: no membranes", 28, GREY).next_to(boxA, UP, buff=0.12, aligned_edge=LEFT)
        boxB = RoundedRectangle(corner_radius=0.3, width=11.6, height=2.2, stroke_color=GREY, stroke_width=3).move_to([0, -1.75, 0])
        labB = T("the cell secretes", 28, GREY).next_to(boxB, UP, buff=0.12, aligned_edge=LEFT)

        def bar(x0, x1, y, color=PROT):
            return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=0.9, stroke_color=color, stroke_width=2,
                                    fill_color=color, fill_opacity=0.9).move_to([(x0 + x1) / 2, y, 0])

        a_left = bar(-5.3, -3.1, 1.55)
        a_main = bar(-3.1, XR, 1.55)
        b_main = bar(-3.1, XR, -1.75)
        gap = DashedVMobject(Rectangle(width=2.2, height=0.9, stroke_color=GREY, stroke_width=3).move_to([-4.2, -1.75, 0]), num_dashes=24)
        q = T("?", 52, YELLOW, weight=BOLD).move_to([-4.2, -1.75, 0])

        self.at("secretory protein")
        self.play(FadeIn(boxA), FadeIn(labA), run_time=0.5)
        self.play(GrowFromEdge(VGroup(a_left, a_main), RIGHT), run_time=0.9)
        self.at("longer than")
        self.play(FadeIn(boxB), FadeIn(labB), run_time=0.5)
        self.play(GrowFromEdge(b_main, RIGHT), Create(gap), run_time=0.9)
        self.at("Why")
        self.play(FadeIn(q, scale=0.5), run_time=0.4)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=0.6)
        self.at("extra piece")
        self.play(a_left.animate.set_fill(YELLOW).set_stroke(YELLOW), run_time=0.6)
        addr = T("address", 28, YELLOW).move_to([-4.2, 0.82, 0])
        self.at("an address")
        self.play(FadeIn(addr, shift=UP * 0.1), run_time=0.5)
        ribo = ribosome(0.7).move_to([XR + 0.8, 1.55, 0])
        rl = T("ribosome", 24, GREY).move_to([XR + 0.8, 0.17, 0])
        self.at("on the ribosome")
        self.play(FadeIn(ribo, shift=LEFT * 0.2), FadeIn(rl), run_time=0.6)
        self.at("cuts it off")
        cut = a_left.copy().set_opacity(1).move_to([-4.2, -1.75, 0])
        self.play(FadeOut(q), FadeIn(cut), run_time=0.4)
        self.play(cut.animate.shift(UP * 0.55).set_opacity(0), FadeOut(gap), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Zip(SpokenScene):
    """a ribosome makes a chain in the cytosol; the signal is a stretch of it; no signal, no sorting."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=0.9, width=12.4, height=6.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.04).move_to([0, -0.1, 0])
        ribo = ribosome(1.0).move_to([-5.0, 1.5, 0])
        rl = T("ribosome", 24, GREY).next_to(ribo, UP, buff=0.12)
        chain = beads(12, 4, r=0.2, gap=0.05, yellow="end")
        for b in chain:
            b.set_fill(PROT)
        chain.move_to([-3.95 + chain.width / 2, 1.5, 0])
        cyt = T("cytosol", 28, GREY).move_to([4.9, 2.6, 0])

        self.at("starts on a ribosome")
        self.play(Create(cell), FadeIn(ribo), FadeIn(rl), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in chain], lag_ratio=0.06), run_time=1.0)
        self.at("the cytosol")
        self.play(FadeIn(cyt), run_time=0.4)
        self.at("the fluid")
        self.play(cell.animate.set_fill(GREY, 0.16), run_time=0.6)

        er = VGroup(Ellipse(width=3.4, height=1.3, stroke_color=INDIGO, stroke_width=3, fill_color=INDIGO, fill_opacity=0.18),
                    T("ER", 24, INDIGO)).move_to([-3.9, -2.0, 0])
        er[1].move_to(er[0])
        pe = VGroup(Ellipse(width=2.2, height=1.1, stroke_color=MAGENTA, stroke_width=3, fill_color=MAGENTA, fill_opacity=0.18),
                    T("peroxisome", 22, MAGENTA)).move_to([0.1, -2.1, 0])
        pe[1].move_to(pe[0])
        mi = VGroup(RoundedRectangle(corner_radius=0.5, width=3.2, height=1.5, stroke_color=ORANGE, stroke_width=3,
                                     fill_color=ORANGE, fill_opacity=0.18),
                    T("mitochondrion", 22, ORANGE)).move_to([3.9, -1.9, 0])
        mi[1].move_to(mi[0])
        self.at("outside the organelles")
        self.play(LaggedStart(*[FadeIn(o, scale=0.9) for o in (er, pe, mi)], lag_ratio=0.3), run_time=1.2)

        sig = chain[8:]
        sl = T("signal sequence", 28, YELLOW).move_to([sig.get_center()[0], 2.25, 0])
        self.at("signal sequence")
        self.play(*[b.animate.set_fill(YELLOW) for b in sig], FadeIn(sl, shift=DOWN * 0.1), run_time=0.7)
        zc = bchip("zip code", YELLOW, 24, pad=0.16).move_to([sig.get_center()[0], 0.75, 0])
        self.at("zip code")
        self.play(FadeIn(zc, shift=UP * 0.1), Indicate(sig, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("on the parcel")
        self.play(FadeOut(ribo), FadeOut(rl), run_time=0.5)

        b2 = beads(12, 0, r=0.2, gap=0.05).move_to([2.0, -0.1, 0])
        nl = T("no signal", 26, GREY).move_to([3.6, 0.5, 0])
        self.at("no signal")
        self.play(FadeIn(b2, shift=DOWN * 0.1), FadeIn(nl), run_time=0.7)
        sl2 = T("stays in the cytosol", 26, RED).move_to([2.0, -0.75, 0])
        self.at("stays in")
        self.play(b2.animate.shift(RIGHT * 0.4), run_time=0.35)
        self.play(b2.animate.shift(LEFT * 0.4), FadeIn(sl2), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Recognize(SpokenScene):
    """SRP binds the emerging signal, halts the chain, and brings the ribosome to its receptor."""

    def construct(self):
        lumen, A, B, C = er_base()
        memlbl = T("ER membrane", 24, GREY).move_to([-4.6, -1.5, 0])
        cyt = T("cytosol", 28, GREY).move_to([5.3, 2.6, 0])
        X0 = -4.6
        ribo, rl, ch = complex_at(X0)
        hyd = T("hydrophobic\nstretch", 24, YELLOW, line_spacing=0.7).move_to([X0 + 1.35, -0.1, 0])
        srp = srp_at(X0)
        halted = T("wheat germ: chain halted", 24, RED).move_to([X0 + 3.1, 1.45, 0])
        rec = receptor()
        rlbl = T("SRP receptor", 24, BLUE).move_to([-1.2, -1.5, 0])

        self.at("For the ER")
        self.play(FadeIn(lumen), FadeIn(A), FadeIn(B), FadeIn(C), FadeIn(memlbl), FadeIn(cyt), run_time=0.8)
        self.play(FadeIn(ribo), FadeIn(rl), run_time=0.5)
        self.at("hydrophobic stretch")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in ch], lag_ratio=0.15), FadeIn(hyd), run_time=1.0)
        self.at("being made")
        self.play(Indicate(ribo, color=GREY, scale_factor=1.06), run_time=0.7)
        self.at("binds it")
        self.play(FadeIn(srp, shift=RIGHT * 0.4), run_time=0.6)
        self.at("halts the growing")
        self.play(FadeIn(halted, shift=LEFT * 0.1), run_time=0.5)
        self.at("brings the ribosome")
        group = VGroup(ribo, rl, ch, srp, hyd, halted)
        self.play(group.animate.shift(RIGHT * (X0 * -1 - 1.2)), FadeIn(rec), FadeIn(rlbl), run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Handover(SpokenScene):
    """GTP holds SRP to its receptor; the ribosome passes to Sec61; GTP hydrolysis separates them;
    the chain threads through; signal peptidase cuts the signal off."""

    def construct(self):
        lumen, A, B, C = er_base()
        memlbl = T("ER membrane", 24, GREY).move_to([-4.6, -1.5, 0])
        cyt = T("cytosol", 28, GREY).move_to([5.3, 2.6, 0])
        rec = receptor()
        ribo, rl, ch = complex_at(-1.2)
        srp = srp_at(-1.2)
        rlbl = T("SRP receptor", 24, BLUE).move_to([-1.2, -1.5, 0])
        self.add(lumen, A, B, C, memlbl, cyt, rec, rlbl, ribo, rl, ch, srp)
        ch.set_z_index(1)
        ribo.set_z_index(3)

        g1 = gtp().move_to([srp.get_center()[0] - 0.25, 0.58, 0])
        g2 = gtp().move_to([-0.3, -0.2, 0])
        self.at("bound")
        self.play(FadeIn(g1, scale=0.5), FadeIn(g2, scale=0.5), run_time=0.6)
        self.at("hold together")
        self.play(Indicate(g1, color=PINK, scale_factor=1.15), Indicate(g2, color=PINK, scale_factor=1.15), run_time=0.8)

        pore = sec61()
        moving = VGroup(ribo, rl, ch)
        self.at("pass the ribosome")
        self.play(moving.animate.shift(RIGHT * 2.9), FadeOut(C), FadeIn(pore), run_time=1.5)
        slabel = T("Sec61", 26, INDIGO).move_to([3.9, -0.35, 0])
        self.at("channel")
        self.play(FadeIn(slabel, shift=LEFT * 0.1), run_time=0.5)
        self.at("hydrolysis")
        self.play(FadeOut(g1), FadeOut(g2), srp.animate.shift(LEFT * 0.7 + UP * 1.1), run_time=0.9)
        self.at("threads through")
        self.play(moving.animate.shift(DOWN * 1.55), run_time=1.3)
        new = beads(2, 0, vertical=True)
        new.move_to([1.7, -0.77 - new.height / 2 - 0.0, 0])
        self.play(ch.animate.shift(DOWN * 0.62), FadeIn(new, shift=DOWN * 0.15), run_time=0.8)
        lum = T("ER lumen", 24, INDIGO).move_to([5.0, -3.05, 0])
        self.at("an enzyme called")
        self.play(FadeIn(lum), run_time=0.4)
        # the junction between the 4 yellow and 3 white beads
        yb = VGroup(*ch[:4])
        jy = yb.get_top()[1]
        pep = chip("signal peptidase", RED, size=26, pad=0.16)
        pep.move_to([1.7 + 0.25 + pep.width / 2 + 0.12, jy - 0.25, 0])
        self.at("signal peptidase")
        self.play(FadeIn(pep, shift=LEFT * 0.3), run_time=0.6)
        self.at("cuts off")
        self.play(yb.animate.shift(LEFT * 2.2 + DOWN * 0.15), FadeOut(pep), run_time=1.0)
        el = T("extra piece", 28, YELLOW).move_to([-2.45, yb.get_center()[1] - 0.15, 0])
        self.at("extra piece")
        self.play(FadeIn(el, shift=RIGHT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Organelles(SpokenScene):
    """other organelles read finished chains: SKL at the carboxyl end; transplant to a mouse enzyme and a bacterial one."""

    def construct(self):
        mi = VGroup(RoundedRectangle(corner_radius=0.5, width=3.4, height=2.0, stroke_color=ORANGE, stroke_width=3,
                                     fill_color=ORANGE, fill_opacity=0.14),
                    RoundedRectangle(corner_radius=0.35, width=2.6, height=1.3, stroke_color=ORANGE, stroke_width=2,
                                     stroke_opacity=0.5, fill_opacity=0)).move_to([-4.2, -1.5, 0])
        ml = T("mitochondrion", 24, ORANGE).move_to([-4.2, -3.0, 0])
        ch_ = VGroup(Ellipse(width=3.2, height=1.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.14),
                     Ellipse(width=2.4, height=1.1, stroke_color=GREEN, stroke_width=2, stroke_opacity=0.5, fill_opacity=0)).move_to([0, -1.5, 0])
        cl = T("chloroplast", 24, GREEN).move_to([0, -3.0, 0])
        pe = Circle(radius=1.0, stroke_color=MAGENTA, stroke_width=3, fill_color=MAGENTA, fill_opacity=0.14).move_to([4.2, -1.5, 0])
        pl = T("peroxisome", 24, MAGENTA).move_to([4.2, -3.0, 0])

        self.at("Mitochondria")
        self.play(FadeIn(mi, scale=0.9), FadeIn(ml), run_time=0.6)
        self.at("chloroplasts")
        self.play(FadeIn(ch_, scale=0.9), FadeIn(cl), run_time=0.6)
        self.at("peroxisomes")
        self.play(FadeIn(pe, scale=0.9), FadeIn(pl), run_time=0.6)
        fin = beads(12, 0).move_to([0, 1.5, 0])
        fl = T("finished chain", 26, GREY).move_to([0, 2.2, 0])
        self.at("already finished")
        self.play(FadeIn(fin, shift=DOWN * 0.1), FadeIn(fl), run_time=0.7)

        # right: peroxisomal protein with SKL at the carboxyl end
        rw = beads(8, 0).move_to([3.35, 1.85, 0])
        ry = beads(3, 3).next_to(rw, RIGHT, buff=0.04)
        right = VGroup(rw, ry)
        rtag = T("peroxisomal protein", 24, GREY).move_to([3.0, 2.5, 0])
        self.at("tripeptide")
        self.play(FadeOut(fin), FadeOut(fl), FadeIn(right, shift=DOWN * 0.1), FadeIn(rtag), run_time=0.8)
        cend = T("carboxyl end", 24, GREY).move_to([ry.get_center()[0], 1.3, 0])
        self.at("carboxyl end")
        self.play(FadeIn(cend), run_time=0.4)
        skl = T("SKL", 30, YELLOW, weight=BOLD).move_to([ry.get_center()[0], 2.5, 0])
        self.at("such as")
        self.play(FadeIn(skl, shift=DOWN * 0.1), Indicate(ry, color=YELLOW, scale_factor=1.2), run_time=0.7)

        # left: first 53 residues of a yeast mitochondrial precursor + mouse enzyme
        ly = beads(4, 4).move_to([-5.45, 1.85, 0])
        lw = beads(8, 0).move_to([-3.0, 1.85, 0])
        ltag = T("first 53 residues of a\nyeast mitochondrial precursor", 22, YELLOW, line_spacing=0.7).move_to([-4.0, 3.0, 0])
        self.at("Join the first")
        self.play(ch_[0].animate.set_stroke(opacity=0.3).set_fill(opacity=0.04), ch_[1].animate.set_stroke(opacity=0.15), cl.animate.set_opacity(0.35), FadeIn(ly, shift=RIGHT * 0.2), FadeIn(ltag), run_time=0.7)
        lw_lbl = T("mouse enzyme", 24, GREY).move_to([-3.0, 1.2, 0])
        self.at("mouse enzyme")
        self.play(FadeIn(lw, shift=DOWN * 0.1), FadeIn(lw_lbl), run_time=0.7)
        self.at("and the fusion")
        self.play(ly.animate.next_to(lw, LEFT, buff=0.04), FadeOut(ml), run_time=0.4)
        left = VGroup(ly, lw)
        ml2 = T("yeast mitochondrion", 24, ORANGE).move_to([-4.2, -3.0, 0])
        self.at("the fusion enters")
        self.play(FadeOut(ltag), FadeOut(lw_lbl), left.animate.scale(0.65).move_to([-4.2, -1.5, 0]),
                  FadeIn(ml2), run_time=1.6)

        # right: add SKL to the end of a bacterial enzyme
        self.at("Add")
        self.play(ry.animate.shift(DOWN * 0.6 + RIGHT * 0.25), FadeOut(rtag), FadeOut(cend), run_time=0.5)
        bl = T("bacterial enzyme", 24, GREY).move_to([rw.get_center()[0], 2.5, 0])
        self.at("to the end")
        self.play(ry.animate.next_to(rw, RIGHT, buff=0.04), run_time=0.5)
        self.at("bacterial enzyme")
        self.play(FadeIn(bl), run_time=0.4)
        pl2 = T("peroxisome\nmammalian cells", 24, MAGENTA, line_spacing=0.7).move_to([4.2, -3.0, 0])
        self.at("enters peroxisomes")
        self.play(FadeOut(bl), FadeOut(skl), FadeOut(pl), right.animate.scale(0.45).move_to([4.2, -1.5, 0]), run_time=1.4)
        self.play(FadeIn(pl2), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the signal is in the protein; moving it moves the protein."""

    def construct(self):
        cyt = RoundedRectangle(corner_radius=0.4, width=7.8, height=6.4, stroke_color=GREY, stroke_width=2,
                               fill_color=GREY, fill_opacity=0.06).move_to([-2.4, -0.1, 0])
        cl = T("cytosol", 26, GREY).move_to([-1.1, 2.75, 0])
        org = RoundedRectangle(corner_radius=0.4, width=4.8, height=6.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to([3.9, -0.1, 0])
        ol = T("organelle", 26, GREY).move_to([3.9, -2.85, 0])
        self.add(cyt, cl, org, ol)

        A = beads(9, 4)
        A.move_to([-3.6, 1.9, 0])
        al = T("address", 28, YELLOW).move_to([A[:4].get_center()[0], 2.6, 0])
        m1 = bchip("receptor", BLUE, 24, pad=0.16).move_to([1.5, 1.9, 0])
        self.at("the protein itself")
        self.play(FadeIn(A, shift=DOWN * 0.1), FadeIn(al), run_time=0.8)
        self.at("read by a receptor")
        self.play(FadeIn(m1), run_time=0.5)
        self.play(VGroup(A, al).animate.move_to([4.3, 2.2, 0]), run_time=1.5)

        B = beads(9, 0).move_to([-3.6, -0.2, 0])
        bl = T("no signal", 26, GREY).move_to([-3.6, 0.4, 0])
        stay = T("stays in the cytosol", 26, RED).move_to([-3.6, -0.85, 0])
        self.at("no signal")
        self.play(FadeIn(B, shift=DOWN * 0.1), FadeIn(bl), run_time=0.7)
        self.at("stays in")
        self.play(B.animate.shift(RIGHT * 0.4), run_time=0.3)
        self.play(B.animate.shift(LEFT * 0.4), FadeIn(stay), run_time=0.3)

        tag = beads(4, 4).move_to([-3.6, 1.9, 0])
        self.at("attached to a protein")
        self.play(FadeOut(bl), FadeOut(stay), FadeIn(tag, shift=DOWN * 0.1), run_time=0.7)
        self.play(tag.animate.move_to(B[:4].get_center()), run_time=0.8)
        self.play(FadeOut(tag), *[b.animate.set_fill(YELLOW) for b in B[:4]], run_time=0.3)
        m2 = bchip("receptor", BLUE, 24, pad=0.16).move_to([1.5, -0.2, 0])
        self.at("send it elsewhere")
        self.play(FadeIn(m2), run_time=0.4)
        self.play(B.animate.move_to([4.3, -0.2, 0]), run_time=1.5)

        l1 = T("move the stretch", 30, YELLOW).move_to([-3.4, -1.2, 0])
        l2 = T("the protein moves", 30, TEXT).move_to([-3.4, -1.9, 0])
        l3 = bchip("sufficient to sort", GREEN, 28).move_to([-3.4, -2.7, 0])
        self.at("moving a stretch")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("moves the protein")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)
        self.at("sufficient to sort")
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "If moving a stretch moves the protein, it is sufficient to sort."
