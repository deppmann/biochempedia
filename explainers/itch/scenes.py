"""Itch: its own receptors, its own relay, and where the evidence stops  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = MrgprA3-positive sensory neurons (mouse)
  PURPLE = itch-causing substances (histamine, chloroquine, "itch substance")
  ORANGE = pain: pain substance, capsaicin, wiping, pain-type behaviour
  GREEN  = scratching / itch behaviour, and the relay arrows
  TEAL   = peptides and the channel chip (Nppb, GRP, TRPV1)
  PINK   = spinal cells of the relay (NPRA cells, GRPR cells, spinal GRP neurons)
  RED    = removed / deleted / lost
  YELLOW = the open question, the rule
  GREY   = frames, labels, de-emphasised

Anatomy rules kept: neurons are simple cells; the spinal cord is one labelled schematic box (dorsal horn),
no crossing pathway, no body, no brain. Every claim is a mouse claim from the lesson; no number is drawn
that the lesson does not give (the only number on screen is "about 70 percent").
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB8"
TEALC = "#3FB8C0"


def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dim(c, o=0.35):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def pulse(*cs, color=YELLOW, s=1.1, **kw):
    return Indicate(VGroup(*[x for c in cs for x in c[1:]]), color=color, scale_factor=s, **kw)


def undim(c):
    return [c[1].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[2].animate.set_opacity(1)]


def arr(a, b, color=GREEN, w=6, tip=0.22):
    return Arrow(np.array(a, float), np.array(b, float), buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(mob, color=RED, w=7):
    r = 0.5 * min(mob.width, mob.height) + 0.05
    c = mob.get_center()
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]), color=color, stroke_width=w))


def neuron(color=BLUE, scale=1.0):
    """a simple sensory neuron: a soma with a peripheral ending (left, down) and a central branch (up)"""
    soma = Circle(radius=0.3 * scale, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.25)
    tail = Line(soma.get_bottom(), soma.get_bottom() + DOWN * 0.7 * scale, color=color, stroke_width=3.5)
    top = Line(soma.get_top(), soma.get_top() + UP * 0.5 * scale, color=color, stroke_width=3.5)
    return VGroup(tail, top, soma)


def neuron_row(n, color, x0, x1, y):
    xs = np.linspace(x0, x1, n)
    return VGroup(*[neuron(color).move_to([x, y, 0]) for x in xs])


class S00Title(TitleCard):
    LESSON = "Itch: a sense of its own"
    TITLE = "Itch Has Its Own Relay, With Limits"


# ---------------------------------------------------------------------------------------------
class S01Cluster(SpokenScene):
    """a gene cluster deleted; histamine scratching normal, chloroquine scratching much less; the question"""

    def construct(self):
        head = T("in mice", 24, GREY).move_to([0, 3.3, 0])
        gene = bchip("Mrgpr gene cluster", GREY, 30).move_to([0, 2.5, 0])
        self.at("one cluster")
        self.play(FadeIn(head), FadeIn(gene, shift=DOWN * 0.2), run_time=0.8)
        self.at("can be deleted")
        x = cross(gene)
        self.play(Create(x), *dim(gene, 0.5), run_time=0.8)
        # row 1: histamine
        self.at("scratch normally")
        h = bchip("histamine", PURPLE, 34).move_to([-4.3, 0.7, 0])
        ha = arr([-2.5, 0.7, 0], [-0.6, 0.7, 0])
        hr = bchip("scratching: normal", GREEN, 34).move_to([3.0, 0.7, 0])
        self.play(FadeIn(h, shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(ha), FadeIn(hr, shift=RIGHT * 0.2), run_time=0.8)
        self.at("much less")
        c = bchip("chloroquine", PURPLE, 34).move_to([-4.3, -1.0, 0])
        ca = arr([-2.5, -1.0, 0], [-0.6, -1.0, 0])
        cr = bchip("scratching: much less", GREEN, 34).move_to([3.0, -1.0, 0])
        down = Arrow([5.9, -0.45, 0], [5.9, -1.35, 0], buff=0, color=RED, stroke_width=7, tip_length=0.25)
        self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(ca), FadeIn(cr, shift=RIGHT * 0.2), run_time=0.7)
        self.play(*dim(cr, 0.6), GrowArrow(down), run_time=0.6)
        self.at("could not happen")
        self.play(pulse(hr, cr, s=1.05), run_time=1.2)
        self.at("weak pain")
        own = bchip("a sense of its own?", YELLOW, 32).move_to([-3.2, -2.9, 0])
        wp = bchip("only weak pain?", ORANGE, 32).move_to([3.2, -2.9, 0])
        orr = T("or", 28, GREY).move_to([0, -2.9, 0])
        self.play(FadeIn(own, shift=UP * 0.2), FadeIn(orr), FadeIn(wp, shift=UP * 0.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ablation(SpokenScene):
    """remove the MrgprA3 neurons: scratching falls, pain assays unchanged; the cheek assay"""

    def construct(self):
        head = T("in mice", 24, GREY).move_to([0, 3.35, 0])
        ns = neuron_row(6, BLUE, -2.6, 2.6, 2.1)
        lab = T("neurons marked by MrgprA3", 28, BLUE).move_to([0, 3.35, 0])
        head.move_to([-5.0, 3.35, 0])
        self.at("removed one group")
        self.play(FadeIn(ns, lag_ratio=0.15), FadeIn(lab), FadeIn(head), run_time=1.2)
        self.at("neurons are marked")
        self.play(Indicate(ns, color=YELLOW, scale_factor=1.06), run_time=1.0)
        # results area
        r1a = bchip("itch substance", PURPLE, 30).move_to([-4.2, 0.0, 0])
        a1 = arr([-2.2, 0, 0], [-0.7, 0, 0])
        r1 = bchip("scratching", GREEN, 32).move_to([1.3, 0.0, 0])
        r2a = bchip("pain assays", ORANGE, 30).move_to([-4.2, -1.8, 0])
        a2 = arr([-2.4, -1.8, 0], [-0.7, -1.8, 0])
        r2 = bchip("wiping", ORANGE, 32).move_to([1.3, -1.8, 0])
        self.play(FadeIn(r1a), GrowArrow(a1), FadeIn(r1), FadeIn(r2a), GrowArrow(a2), FadeIn(r2), run_time=1.0)
        self.at("Scratching fell")
        xs = VGroup(*[cross(n[2], RED, 5) for n in ns])
        self.play(Create(xs), *[n.animate.set_opacity(0.3) for n in ns], run_time=1.0)
        fell = Arrow([4.2, 0.5, 0], [4.2, -0.5, 0], buff=0, color=RED, stroke_width=7, tip_length=0.25)
        fl = T("fell", 30, RED).next_to(fell, RIGHT, buff=0.2)
        self.play(*dim(r1, 0.45), GrowArrow(fell), FadeIn(fl), run_time=0.9)
        self.at("did not change")
        same = T("unchanged", 30, GREEN).move_to([4.2, -1.8, 0])
        self.play(FadeIn(same), pulse(r2, color=ORANGE), run_time=1.0)
        self.at("cheek assay")
        ck = T("cheek assay", 26, GREY, weight=BOLD).move_to([-4.2, 1.0, 0])
        hp = T("hindpaw", 28, TEXT).next_to(r1, DOWN, buff=0.18)
        fp = T("forelimb", 28, TEXT).next_to(r2, DOWN, buff=0.18)
        self.play(FadeIn(ck), run_time=0.6)
        self.at("scratching with")
        self.play(FadeIn(hp), pulse(r1, color=GREEN, s=1.12), run_time=1.0)
        self.at("with a forelimb")
        self.play(FadeIn(fp), pulse(r2, color=ORANGE, s=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rescue(SpokenScene):
    """capsaicin normally gives wiping; TRPV1 restored only in MrgprA3 neurons gives itch-related behaviour"""

    def construct(self):
        cap = bchip("capsaicin", ORANGE, 34).move_to([-4.9, 1.0, 0])
        wipe = bchip("wiping", ORANGE, 34).move_to([4.6, 1.0, 0])
        mid = T("normally", 28, GREY).move_to([-0.1, 1.5, 0])
        ar = arr([-3.4, 1.0, 0], [3.2, 1.0, 0], ORANGE)
        self.at("put one thing back")
        self.play(FadeIn(cap, shift=RIGHT * 0.2), run_time=0.7)
        self.at("normally evokes wiping")
        self.play(GrowArrow(ar), FadeIn(mid), FadeIn(wipe, shift=LEFT * 0.2), run_time=1.0)
        self.wait(self.beat(0.05))
        # now the null background: two neuron groups
        self.at("restored working")
        self.play(FadeOut(ar), FadeOut(mid), FadeOut(wipe), cap.animate.move_to([-5.0, 3.2, 0]), run_time=0.8)
        bl = neuron_row(4, BLUE, -4.4, -1.6, 0.9)
        gr = neuron_row(4, GREY, 1.6, 4.4, 0.9)
        bt = T("MrgprA3 neurons", 28, BLUE).move_to([-3.0, 2.05, 0])
        gt = T("other neurons", 28, GREY).move_to([3.0, 2.05, 0])
        bg = T("Trpv1-null background, schematic", 24, GREY).move_to([0, 2.65, 0])
        self.play(FadeIn(bl), FadeIn(gr), FadeIn(bt), FadeIn(gt), FadeIn(bg), run_time=1.0)
        trpv = bchip("working TRPV1", TEALC, 28).move_to([-3.0, -1.3, 0])
        ln = VGroup(*[Line(trpv.get_top(), n[2].get_bottom() + DOWN * 0.7, color=TEALC, stroke_width=3) for n in bl])
        self.at("only in the")
        self.play(FadeIn(trpv, shift=UP * 0.2), Create(ln), run_time=1.0)
        self.play(*[n[2].animate.set_fill(TEALC, 0.5) for n in bl], run_time=0.5)
        self.at("then evoked")
        itch = bchip("itch-related behaviour", GREEN, 30).move_to([4.3, 3.2, 0])
        a3 = arr([-3.4, 3.2, 0], [2.0, 3.2, 0], ORANGE)
        self.play(GrowArrow(a3), FadeIn(itch, shift=LEFT * 0.2), run_time=1.0)
        self.at("Ablation shows")
        t1 = T("ablation: needed, in these assays", 28, RED).move_to([-3.1, -2.45, 0])
        self.play(FadeIn(t1, shift=UP * 0.15), run_time=0.8)
        self.at("The rescue shows")
        t2 = T("rescue: what they can drive, alone", 28, GREEN).move_to([-3.1 + 6.3, -3.2, 0])
        t2.move_to([0, -3.2, 0])
        t1.move_to([0, -2.45, 0])
        self.play(FadeIn(t2, shift=UP * 0.15), Indicate(bl, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Relay(SpokenScene):
    """the spinal peptide relay: Nppb, NPRA cells, GRP, GRPR cells; three tests fix the order"""

    def construct(self):
        frame = RoundedRectangle(corner_radius=0.3, width=12.4, height=6.7, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.06).move_to([0, 0.0, 0])
        ft = T("Nppb from sensory neurons, rest in dorsal horn: schematic", 20, GREY).move_to([0, 3.0, 0])
        self.at("One mouse")
        self.play(FadeIn(frame), FadeIn(ft), run_time=0.8)
        y = 0.9
        xs = [-4.7, -1.6, 1.6, 4.7]
        n1 = bchip("Nppb", TEALC, 32).move_to([xs[0], y, 0])
        n2 = bchip("NPRA cells", PINK, 28).move_to([xs[1], y, 0])
        n3 = bchip("GRP", TEALC, 32).move_to([xs[2], y, 0])
        n4 = bchip("GRPR cells", PINK, 28).move_to([xs[3], y, 0])
        a12 = arr([xs[0] + 1.0, y, 0], [xs[1] - 1.2, y, 0], GREY)
        a23 = arr([xs[1] + 1.2, y, 0], [xs[2] - 0.8, y, 0], GREY)
        a34 = arr([xs[2] + 0.8, y, 0], [xs[3] - 1.2, y, 0], GREY)
        self.at("relay starts")
        self.play(*[FadeIn(n, scale=0.9) for n in (n1, n2, n3, n4)], *[FadeIn(a) for a in (a12, a23, a34)], run_time=1.0)
        res = bchip("scratching to itch agents", GREEN, 28).move_to([0, -2.4, 0])
        self.play(FadeIn(res), run_time=0.5)
        # test 1: Nppb null
        self.at("lost almost all")
        x1 = cross(n1)
        lost = T("responses almost gone", 28, RED).move_to([0, -1.2, 0])
        self.play(Create(x1), *dim(n1, 0.35), *dim(res, 0.3), FadeIn(lost), run_time=1.0)
        # test 2: Nppb given
        self.at("injected around the cord")
        self.play(FadeOut(x1), FadeOut(lost), *undim(n1), run_time=0.5)
        giv = T("given by injection around the cord", 24, TEALC).move_to([-3.1, 2.15, 0])
        self.play(FadeIn(giv), pulse(n1), FadeOut(res), run_time=1.0)
        note1 = T("still evokes scratching, in both kinds of mice", 26, GREEN).move_to([0, -1.2, 0])
        self.play(FadeIn(note1), run_time=0.6)
        # test 3: NPRA cells removed
        self.at("of the cells")
        self.play(FadeOut(giv), FadeOut(note1), run_time=0.4)
        x2 = Rectangle(width=0.7 * n2[1].width, height=n2[1].height, stroke_width=0, fill_color=RED, fill_opacity=0.5).move_to(n2[1].get_left() + RIGHT * 0.35 * n2[1].width)
        rm = T("about 70 percent removed", 26, RED).move_to([-2.9, 2.05, 0])
        self.play(FadeIn(x2), FadeIn(rm), run_time=0.9)
        self.at("still evoked scratching", nth=1)
        giv2 = T("GRP given", 26, TEALC).move_to([2.6, 2.05, 0])
        note2 = T("still evokes scratching", 26, GREEN).move_to([0, -1.2, 0])
        self.play(FadeIn(giv2), pulse(n3), FadeIn(note2), run_time=1.0)
        # order
        self.at("root fits")
        self.play(FadeOut(giv2), FadeOut(note2), FadeOut(rm), FadeOut(x2), run_time=0.6)
        self.play(LaggedStart(*[Indicate(a, color=TEXT, scale_factor=1.25) for a in (a12, a23, a34)], lag_ratio=0.5), run_time=2.4)
        self.at("Direct contacts")
        dc = T("direct synaptic contacts: not shown", 26, YELLOW).move_to([0, -1.2, 0])
        self.play(FadeIn(dc), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Source(SpokenScene):
    """where does the GRP come from? two candidate sources, studies that disagree"""

    def construct(self):
        grp = bchip("spinal GRP acting on GRPR", TEALC, 32).move_to([0, 3.0, 0])
        sens = bchip("sensory neurons", BLUE, 30).move_to([-3.4, 0.9, 0])
        spin = bchip("spinal GRP neurons", PINK, 30).move_to([3.4, 0.9, 0])
        a1 = DashedLine([-3.0, 1.45, 0], [-1.0, 2.55, 0], color=GREY, stroke_width=5)
        a2 = DashedLine([3.0, 1.45, 0], [1.0, 2.55, 0], color=GREY, stroke_width=5)
        q = T("?", 60, YELLOW, weight=BOLD).move_to([0, 1.7, 0])
        self.at("contested step")
        self.play(FadeIn(grp, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(sens), FadeIn(spin), Create(a1), Create(a2), FadeIn(q), run_time=1.2)
        self.at("In one study")
        s1 = T("one study", 26, GREY, weight=BOLD).move_to([-3.4, -0.35, 0])
        self.play(FadeIn(s1), run_time=0.4)
        self.at("deleting")
        d = VGroup(T("delete Grp in", 28, TEXT), T("sensory neurons:", 28, TEXT),
                   T("less non-histamine", 28, GREEN), T("scratching", 28, GREEN)).arrange(DOWN, buff=0.12)
        d.move_to([-3.4, -2.0, 0])
        self.play(FadeIn(d, shift=UP * 0.15), pulse(sens), run_time=1.0)
        self.at("Removing spinal")
        s1b = T("same study", 26, GREY, weight=BOLD).move_to([3.4, -0.35, 0])
        r = VGroup(T("remove spinal Grp", 28, TEXT), T("neurons: no reduction", 28, RED),
                   T("in that study's tests", 28, RED)).arrange(DOWN, buff=0.12)
        r.move_to([3.4, -1.85, 0])
        self.play(FadeIn(s1b), FadeIn(r, shift=UP * 0.15), pulse(spin), run_time=1.0)
        self.at("Another study")
        self.play(FadeOut(s1b), FadeOut(r), run_time=0.5)
        s2 = T("another study", 26, GREY, weight=BOLD).move_to([3.4, -0.35, 0])
        r2 = VGroup(T("remove spinal GRP", 28, TEXT), T("neurons: itch-related", 28, GREEN),
                    T("behaviour reduced", 28, GREEN)).arrange(DOWN, buff=0.12)
        r2.move_to([3.4, -1.85, 0])
        self.play(FadeIn(s2), FadeIn(r2, shift=UP * 0.15), run_time=1.0)
        self.at("do not settle")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.4), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Scope(SpokenScene):
    """the same neurons driven two ways give two behaviours; the human caveat; the rule"""

    def construct(self):
        nb = bchip("MrgprA3\nneurons", BLUE, 32).move_to([-5.0, 0.6, 0])
        self.at("Keep the scope")
        self.play(FadeIn(nb, scale=0.9), run_time=0.8)
        self.at("fast ionotropic stimulation")
        s1 = bchip("fast ionotropic\nstimulation", GREY, 26).move_to([-0.5, 2.0, 0])
        a1 = arr(nb.get_right() + UP * 0.2, s1.get_left())
        self.play(GrowArrow(a1), FadeIn(s1), run_time=0.9)
        self.at("mostly evoked")
        r1 = bchip("mostly pain-type\nbehaviour", ORANGE, 26).move_to([4.7, 2.0, 0])
        a1b = arr(s1.get_right(), r1.get_left(), ORANGE)
        self.play(GrowArrow(a1b), FadeIn(r1), run_time=0.9)
        self.at("linked stimulation")
        s2 = bchip("Gq-linked\nstimulation", GREY, 26).move_to([-0.5, 0.0, 0])
        a2 = arr(nb.get_right() + DOWN * 0.2, s2.get_left())
        self.play(GrowArrow(a2), FadeIn(s2), run_time=0.9)
        self.at("evoked itch")
        r2 = bchip("itch\nbehaviour", GREEN, 26).move_to([4.7, 0.0, 0])
        a2b = arr(s2.get_right(), r2.get_left(), GREEN)
        self.play(GrowArrow(a2b), FadeIn(r2), run_time=0.9)
        self.at("under every manipulation")
        self.play(pulse(r1, r2, s=1.08), run_time=1.2)
        self.at("Nothing here shows")
        h = VGroup(T("mouse MrgprA3 and human MRGPRX1 are different genes:", 26, GREY),
                   T("nothing here shows a MrgprA3 lineage in people", 26, YELLOW)).arrange(DOWN, buff=0.1)
        h.move_to([0, -1.9, 0])
        self.play(FadeIn(h, shift=UP * 0.15), run_time=1.0)
        self.at("Being needed")
        rule = T("needed in an assay is not the same as itch-only", 30, TEXT, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Needed in an assay does not mean itch-only."
