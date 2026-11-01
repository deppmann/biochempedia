"""Toll-like receptors and NF-kB: a cell keeps its answer ready  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

The one idea: NF-kB is already made and folded, held in the cytoplasm by its inhibitor IkB, which
covers the signal that would send it into the nucleus. The receptor relay exists to switch on IKK;
IKK marks IkB, the proteasome destroys it, and the finished activator walks into the nucleus.

COLOR MAP (one color per concept, whole video)
  BLUE    = NF-kB, the finished activator held ready (its bright tab is the signal that sends it in)
  RED     = IkB, the inhibitor (the cap on the tab), and every "blocked / not needed" strike
  ORANGE  = the microbe and its molecule (bacterium, lipopolysaccharide)
  PURPLE  = the relay proteins (receptors, adaptor, IRAK, TRAF6, TAK1, IKK, the second ligase)
  YELLOW  = ubiquitin chains (the lysine-63 platform, the lysine-48 tag)
  GOLD    = a phosphate group (the little "P" badge)
  MAGENTA = the proteasome
  GREEN   = ON (a switched-on kinase, genes switched on)
  GREY    = membranes, nuclear envelope, DNA, labels, de-emphasized
  WHITE   = the signal dot that runs down the relay
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MAGENTA = "#E36FA8"
UBQ = YELLOW


# ---------------------------------------------------------------------------------------------
# a scene that audits itself: text outside the safe frame, text on text (written to audit.log)
# ---------------------------------------------------------------------------------------------
class Film(SpokenScene):
    def _audit(self):
        try:
            if not hasattr(self, "_seen"):
                self._seen = set()
            sid = os.environ.get("KX_SCENE_ID")
            texts = []
            for m in self.mobjects:
                for f in m.get_family():
                    if isinstance(f, Text) and len(f.submobjects):
                        if f.submobjects[0].get_fill_opacity() < 0.3:
                            continue
                        texts.append(f)
            log = Path(os.environ["KX_SCRIPT"]).parent / "audit.log"

            def note(key, msg):
                if key not in self._seen:
                    self._seen.add(key)
                    with open(log, "a") as lg:
                        lg.write(f"{sid} t={self.elapsed():6.2f} {msg}\n")

            for t in texts:
                l, r, u, d = t.get_left()[0], t.get_right()[0], t.get_top()[1], t.get_bottom()[1]
                if l < -6.3 or r > 6.3 or u > 3.5 or d < -3.5:
                    note(("out", t.text), f"OUT of safe frame: {t.text!r} x[{l:.2f},{r:.2f}] y[{d:.2f},{u:.2f}]")
            for i in range(len(texts)):
                for j in range(i + 1, len(texts)):
                    a, b = texts[i], texts[j]
                    ox = min(a.get_right()[0], b.get_right()[0]) - max(a.get_left()[0], b.get_left()[0])
                    oy = min(a.get_top()[1], b.get_top()[1]) - max(a.get_bottom()[1], b.get_bottom()[1])
                    if ox > 0.04 and oy > 0.04:
                        note(("ov", a.text, b.text), f"OVERLAP: {a.text!r} / {b.text!r}")
        except Exception as e:  # never let the audit break a render
            with open(Path(os.environ["KX_SCRIPT"]).parent / "audit.log", "a") as lg:
                lg.write(f"audit error {e!r}\n")

    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        self._audit()

    def wait(self, *args, **kwargs):
        super().wait(*args, **kwargs)
        self._audit()


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    """animations that recolor a bchip without touching its opaque backing."""
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def pulse(c, color, s=1.1, **kw):
    return Indicate(VGroup(*c[1:]), color=color, scale_factor=s, **kw)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    """a line ending in a T bar: blocked."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.32, b - perp * 0.32, color=color, stroke_width=w + 2))


def strike(chip_, color=RED):
    """a line through the middle of a chip: not needed / blocked, and the label stays readable."""
    y = chip_.get_center()[1]
    return Line([chip_.get_left()[0] - 0.12, y, 0], [chip_.get_right()[0] + 0.12, y, 0], color=color, stroke_width=5)


def pbadge(size=0.24):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def membrane_h(y, x0=-6.3, x1=6.3, h=0.3):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def capsule(text, color=ORANGE, size=24, w=2.0, h=0.62):
    box = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.25)
    back = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, box, T(text, size, color).move_to(box))


def bead(r=0.17, color=UBQ):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9)


def bead_chain(p0, p1, n, color=UBQ, r=0.17):
    """n beads on a line from p0 to p1; returns VGroup(line, bead, bead, ...)."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    line = Line(p0, p1, color=color, stroke_width=3)
    g = VGroup(line)
    for k in range(n):
        g.add(bead(r, color).move_to(p0 + (p1 - p0) * (k / max(n - 1, 1))))
    return g


def clock(r=0.6):
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1)
    ticks = VGroup(*[Line(face.get_center() + r * 0.78 * np.array([np.sin(a), np.cos(a), 0]),
                          face.get_center() + r * 0.94 * np.array([np.sin(a), np.cos(a), 0]), color=GREY, stroke_width=3)
                     for a in (0, PI / 2, PI, 3 * PI / 2)])
    hand = Line(face.get_center(), face.get_center() + UP * r * 0.72, color=TEXT, stroke_width=5)
    g = VGroup(face, ticks, hand, Dot(face.get_center(), radius=0.05, color=TEXT))
    g.face, g.hand = face, hand
    return g


def nfkb(s=1.0, label=None, lsize=30, tab=True):
    """NF-kB: two blue lobes (a pair of proteins) and a bright tab, the signal that sends it into the nucleus.
    Built around the origin (centre of the pair); .lobes, .tab, .label are the parts."""
    lobes = VGroup()
    for sx in (-1, 1):
        back = Ellipse(width=2.0 * s, height=1.7 * s, stroke_width=0, fill_color=BG, fill_opacity=1)
        lobe = Ellipse(width=2.0 * s, height=1.7 * s, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3)
        lobes.add(VGroup(back, lobe).move_to([sx * 0.85 * s, 0, 0]))
    tb = Polygon([-0.3 * s, -0.36 * s, 0], [0.3 * s, -0.36 * s, 0], [0, -1.0 * s, 0], stroke_color=BLUE,
                 stroke_width=3, fill_color=BLUE, fill_opacity=1)
    g = VGroup(lobes)
    if tab:
        g.add(tb)
    lab = None
    if label:
        lab = T(label, lsize, BLUE, weight=BOLD).next_to(lobes, UP, buff=0.18)
        g.add(lab)
    g.lobes, g.tab, g.label, g.s = lobes, tb, lab, s
    return g


def ikb_cap(w=2.3, size=28):
    """IkB: the red cap that sits over the tab."""
    h = 0.82
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.28)
    back = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(back, box, T("IκB", size, RED, weight=BOLD).move_to(box))
    g.set_z_index(3)
    g.w = w
    return g


GENE_X = [1.3, 2.9, 4.5]


def genes_row(y):
    return VGroup(*[bchip("gene", GREY, 22, pad=0.1).move_to([x, y, 0]) for x in GENE_X])


def nucleus_rect(top=-1.6, bottom=-3.5):
    return RoundedRectangle(corner_radius=0.35, width=12.4, height=top - bottom, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.08).move_to([0, (top + bottom) / 2, 0])


def dna_line(y):
    return Line([-5.8, y, 0], [5.8, y, 0], color=GREY, stroke_width=6)


def silhouette(shift):
    sil = VGroup(*[DashedVMobject(Ellipse(width=2.0, height=1.7).move_to([sx * 0.85, 0, 0]), num_dashes=30) for sx in (-1, 1)])
    return sil.set_color(BLUE).shift(shift)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Toll-like receptors and NF-κB"
    TITLE = "A cell keeps its answer ready"


# ---------------------------------------------------------------------------------------------
class S01Question(Film):
    """a macrophage meets a bacterium; the path from touch to genes is a row of question marks; the answer waits."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=2.0, width=8.6, height=5.7, stroke_color=GREY, stroke_width=4).move_to([0, -0.65, 0])
        nuc = RoundedRectangle(corner_radius=0.4, width=5.4, height=1.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.08).move_to([0, -2.65, 0])
        nuc_lbl = T("nucleus", 24, GREY).move_to([0, -2.28, 0])
        dna = Line([-2.4, -2.95, 0], [2.4, -2.95, 0], color=GREY, stroke_width=5)
        genes = VGroup(*[bchip("gene", GREY, 22, pad=0.1).move_to([x, -2.95, 0]) for x in (-1.4, 0, 1.4)])
        mac = T("macrophage", 26, GREY).move_to([-3.0, 2.75, 0])

        self.play(Create(cell), FadeIn(nuc), FadeIn(nuc_lbl), FadeIn(dna), FadeIn(genes), run_time=1.6)

        clk = clock(0.6).move_to([5.2, 0.5, 0])
        clk_lbl = T("minutes", 24, GREY).next_to(clk, DOWN, buff=0.2)
        self.at("answer within minutes")
        self.play(FadeIn(clk), FadeIn(clk_lbl), run_time=0.5)
        self.at("A macrophage")
        self.play(FadeIn(mac, shift=DOWN * 0.1), run_time=0.5)
        self.at("swallows microbes")
        self.play(Indicate(cell, color=TEXT, scale_factor=1.03), run_time=0.9)

        bac = capsule("bacterium", ORANGE, 24, w=2.0, h=0.62).move_to([4.4, 3.0, 0])
        self.at("of touching")
        self.play(FadeIn(bac), run_time=0.3)
        self.play(bac.animate.move_to([0, 2.2 + 0.31, 0]),
                  Rotate(clk.hand, angle=-TAU * 0.85, about_point=clk.face.get_center(), rate_func=linear),
                  run_time=1.6)
        self.at("gene expression")
        self.play(Indicate(genes, color=TEXT, scale_factor=1.12), run_time=0.9)

        # the unknown path from the touch to the genes
        ys = [1.2, 0.0, -1.2]
        boxes = VGroup()
        for y in ys:
            b = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=1.1, height=0.8), num_dashes=28).set_color(GREY)
            q = T("?", 38, TEXT)
            boxes.add(VGroup(b, q).move_to([0, y, 0]))
        segs = [(2.2, 1.6), (0.8, 0.4), (-0.4, -0.8), (-1.6, -2.0)]
        links = VGroup(*[arr([0, a, 0], [0, b, 0], GREY, w=3, tip=0.17) for a, b in segs])
        self.at("So what links")
        self.play(LaggedStart(GrowArrow(links[0]), FadeIn(boxes[0]), GrowArrow(links[1]), FadeIn(boxes[1]),
                              GrowArrow(links[2]), FadeIn(boxes[2]), GrowArrow(links[3]), lag_ratio=0.35), run_time=1.9)
        self.at("genes in the nucleus")
        self.play(Indicate(genes, color=TEXT, scale_factor=1.12), run_time=0.8)

        # the answer was waiting
        sil = silhouette([-0.5, 0.9, 0])
        cyto = T("cytoplasm", 24, GREY).move_to([3.0, 0.9, 0])
        self.at("The answer was waiting")
        self.play(FadeOut(boxes), FadeOut(links), FadeOut(clk), FadeOut(clk_lbl), run_time=0.5)
        self.play(FadeIn(sil, scale=0.85), run_time=0.6)
        self.at("in the cytoplasm")
        self.play(FadeIn(cyto), run_time=0.5)
        self.at("the whole time")
        self.play(Indicate(sil, color=BLUE, scale_factor=1.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ready(Film):
    """NF-kB, already made, held by IkB, which covers the tab that would send it into the nucleus."""

    def construct(self):
        C = np.array([-0.5, 0.9, 0])
        s = 1.3
        mem = membrane_h(3.0)
        nuc = nucleus_rect()
        nuc_lbl = T("nucleus", 24, GREY).move_to([-5.2, -1.95, 0])
        dna = dna_line(-3.1)
        genes = genes_row(-3.1)
        stage = VGroup(mem, nuc, nuc_lbl, dna, genes)

        sil = silhouette([-0.5, 0.9, 0])
        self.add(sil)
        nf = nfkb(s).shift(C)
        name = T("NF-κB", 40, BLUE, weight=BOLD).move_to([-4.5, 1.45, 0])
        kind = T("transcription factor", 24, GREY).move_to([-4.5, 0.85, 0])

        self.play(FadeIn(stage), ReplacementTransform(sil, nf.lobes), FadeIn(name), run_time=1.1)
        self.at("a transcription factor")
        self.play(FadeIn(kind, shift=DOWN * 0.1), run_time=0.5)

        self.at("a pair of proteins")
        lobeL, lobeR = nf.lobes[0], nf.lobes[1]
        self.play(lobeL.animate.shift(LEFT * 0.35), lobeR.animate.shift(RIGHT * 0.35), run_time=0.5)
        self.play(lobeL.animate.shift(RIGHT * 0.35), lobeR.animate.shift(LEFT * 0.35), run_time=0.5)

        tip = C + np.array([0, -1.0 * s, 0])
        nuc_top = np.array([C[0], -1.6, 0])
        path0 = arr(C + np.array([0, -0.55 * s, 0]), nuc_top, GREY, w=4, tip=0.2)
        path0.set_opacity(0.8)
        self.at("bind DNA")
        self.play(GrowArrow(path0), run_time=0.6)
        self.at("switch genes on")
        self.play(Indicate(genes, color=TEXT, scale_factor=1.12), run_time=0.8)

        rest = T("resting cell", 26, GREY).move_to([-4.9, 2.5, 0])
        self.at("In a resting cell")
        self.play(FadeIn(rest, shift=DOWN * 0.1), run_time=0.5)
        self.at("already made")
        self.play(Indicate(nf.lobes, color=BLUE, scale_factor=1.06), run_time=0.9)
        cyto = T("cytoplasm", 26, GREY).move_to([4.4, 1.6, 0])
        self.at("waits in the cytoplasm")
        self.play(FadeIn(cyto, shift=DOWN * 0.1), run_time=0.5)

        cap = ikb_cap(2.3).shift(C + np.array([0, -0.8 * s, 0]) + RIGHT * 3.9)
        cap_lbl = T("inhibitor", 24, RED).next_to(cap, RIGHT, buff=0.2)
        self.at("held by its inhibitor")
        self.play(FadeIn(cap, shift=LEFT * 0.3), FadeIn(cap_lbl, shift=LEFT * 0.3), run_time=0.7)

        sig_lbl = T("nuclear signal", 24, BLUE).move_to([-3.7, -0.35, 0])
        leader = Line(sig_lbl.get_right() + RIGHT * 0.05, tip + LEFT * 0.12 + UP * 0.12, color=BLUE, stroke_width=2.5)
        self.at("covers the signal")
        self.play(FadeIn(nf.tab, shift=DOWN * 0.15), FadeIn(sig_lbl), Create(leader), run_time=0.7)
        self.play(Indicate(nf.tab, color=BLUE, scale_factor=1.35), run_time=0.5)
        self.at("that would send")
        self.play(cap.animate.shift(LEFT * 3.9), FadeOut(cap_lbl), run_time=1.0)
        cap_bottom = C + np.array([0, -0.8 * s - 0.41, 0])
        blocked = inhib(cap_bottom, nuc_top + UP * 0.02, RED)
        self.at("into the nucleus")
        self.play(ReplacementTransform(path0, blocked), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Relay(Film):
    """a signal runs down the relay: receptor pair, tower, TRAF6, a lysine-63 chain as a platform, TAK1 and IKK."""

    def construct(self):
        X = -4.0
        mem = membrane_h(2.35)

        def receptor(x):
            box = RoundedRectangle(corner_radius=0.22, width=0.62, height=1.1, stroke_color=PURPLE, stroke_width=4,
                                   fill_color=PURPLE, fill_opacity=0.3)
            back = RoundedRectangle(corner_radius=0.22, width=0.62, height=1.1, stroke_width=0, fill_color=BG, fill_opacity=1)
            return VGroup(back, box).move_to([x, 2.35, 0]).set_z_index(2)

        recA, recB = receptor(X - 1.3), receptor(X + 1.3)
        lps = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9).move_to([X + 2.6, 3.2, 0])
        lps_lbl = T("lipopolysaccharide", 24, ORANGE)
        self.play(FadeIn(mem), FadeIn(recA), FadeIn(recB), FadeIn(lps, shift=DOWN * 0.2), run_time=0.8)
        self.at("lipopolysaccharide")
        self.play(lps.animate.move_to([X, 3.2, 0]), run_time=0.9)
        lps_lbl.next_to(lps, RIGHT, buff=0.25)
        self.play(FadeIn(lps_lbl), run_time=0.4)

        rec_lbl = T("two Toll-like receptors", 24, PURPLE).move_to([X + 3.6, 1.85, 0])
        self.at("holds two")
        self.play(FadeIn(rec_lbl), Indicate(VGroup(recA[1], recB[1]), color=PURPLE, scale_factor=1.1), run_time=0.6)
        self.at("side by side")
        self.play(recA.animate.move_to([X - 0.65, 2.35, 0]), recB.animate.move_to([X + 0.65, 2.35, 0]), run_time=0.9)

        def slab(text, y, size=26):
            box = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.62, stroke_color=PURPLE, stroke_width=3,
                                   fill_color=PURPLE, fill_opacity=0.22)
            back = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.62, stroke_width=0, fill_color=BG, fill_opacity=1)
            g = VGroup(back, box, T(text, size, PURPLE))
            g[2].move_to(box)
            return g.move_to([X, y, 0])

        sl = [slab("MyD88", 1.2), slab("IRAK", 0.55), slab("IRAK", -0.1)]
        dot = Dot([X, 1.7, 0], radius=0.14, color=TEXT)
        self.at("The")
        self.play(FadeIn(sl[0], shift=DOWN * 0.15), FadeIn(dot), run_time=0.6)
        self.at("stacks with")
        self.play(FadeIn(sl[1], shift=DOWN * 0.15), dot.animate.move_to([X, 0.55, 0]), run_time=0.5)
        self.play(FadeIn(sl[2], shift=DOWN * 0.15), dot.animate.move_to([X, -0.1, 0]), run_time=0.5)

        traf = bchip("TRAF6", PURPLE, 28).move_to([X, -1.5, 0])
        a_tr = arr([X, -0.5, 0], [X, -1.07, 0], GREY, w=4, tip=0.2)
        self.at("An activated")
        self.play(Indicate(VGroup(sl[1][1], sl[2][1]), color=PURPLE, scale_factor=1.08), run_time=0.7)
        self.at("binds")
        self.play(GrowArrow(a_tr), FadeIn(traf), dot.animate.move_to([X, -1.5, 0]), run_time=0.7)
        self.remove(dot)

        chain = bead_chain([X + 1.25, -1.5, 0], [5.4, -1.5, 0], 17, r=0.19)
        self.at("builds a ubiquitin chain")
        self.play(FadeIn(chain[0]), LaggedStart(*[FadeIn(b, scale=0.4) for b in chain[1:]], lag_ratio=0.09), run_time=1.8)
        lys = T("lysine-63 chain", 26, UBQ).move_to([1.2, -2.25, 0])
        self.at("lysine")
        self.play(FadeIn(lys, shift=UP * 0.1), run_time=0.5)

        plat = T("+ linear chains", 28, TEXT).move_to([1.2, -2.85, 0])
        self.at("Together with")
        self.play(FadeIn(plat, shift=UP * 0.1), Indicate(chain[1:], color=UBQ, scale_factor=1.25), run_time=0.8)

        tak = bchip("TAK1", PURPLE, 28).move_to([0.2, -0.8, 0])
        ikk = bchip("IKK", PURPLE, 28).move_to([3.2, -0.8, 0])
        self.at("gathers")
        self.play(FadeIn(tak, shift=DOWN * 0.5), FadeIn(ikk, shift=DOWN * 0.5), run_time=0.9)

        pb = pbadge().move_to(tak.get_right() + RIGHT * 0.3 + UP * 0.05)
        self.at("switches on")
        self.play(FadeIn(pb, scale=0.5), run_time=0.3)
        self.play(pb.animate.move_to(ikk.get_corner(UL) + np.array([-0.05, 0.1, 0])), run_time=0.7)
        on = T("ON", 30, GREEN, weight=BOLD).move_to([4.7, -0.8, 0])
        self.play(*recolor(ikk, GREEN), FadeIn(on, scale=0.8), run_time=0.6)
        ikk_lbl = T("IκB kinase", 24, GREY).move_to([3.2, 0.3, 0])
        self.at("kinase")
        self.play(FadeIn(ikk_lbl, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Destroy(Film):
    """IKK marks IkB with two phosphates; a second ligase adds a lysine-48 chain; the proteasome destroys the cap."""

    def construct(self):
        C = np.array([-0.5, 1.0, 0])
        s = 1.0
        nuc = nucleus_rect()
        nuc_lbl = T("nucleus", 24, GREY).move_to([-5.2, -1.95, 0])
        dna = dna_line(-3.1)
        genes = genes_row(-3.1)
        nf = nfkb(s, label="NF-κB", lsize=30).shift(C)
        cap = ikb_cap(2.3).shift(C + np.array([0, -0.8 * s, 0]))
        cap_bottom = C + np.array([0, -0.8 * s - 0.41, 0])
        nuc_top = np.array([C[0], -1.6, 0])
        blocked = inhib(cap_bottom, nuc_top + UP * 0.02, RED)
        ikk = bchip("IKK", PURPLE, 28).move_to([3.2, -0.8, 0])
        ikk[1].set_stroke(GREEN).set_fill(GREEN, 0.16)
        ikk[2].set_color(GREEN)
        on = T("ON", 30, GREEN, weight=BOLD).move_to([4.7, -0.8, 0])
        self.add(nuc, nuc_lbl, dna, genes, nf, cap, blocked, ikk, on)

        # two phosphates from IKK onto IkB
        p1, p2 = pbadge().move_to(ikk.get_left() + LEFT * 0.3), pbadge().move_to(ikk.get_left() + LEFT * 0.3)
        d1 = cap.get_center() + np.array([0.8, 0, 0])
        d2 = cap.get_center() + np.array([-0.8, 0, 0])
        for p in (p1, p2):
            p.set_z_index(4)
        self.at("adds two phosphates")
        self.play(FadeIn(p1, scale=0.5), run_time=0.25)
        self.play(p1.animate.move_to(d1), run_time=0.8)
        self.play(FadeIn(p2, scale=0.5), run_time=0.25)
        self.play(p2.animate.move_to(d2), run_time=0.8)

        self.at("still holds")
        self.play(Indicate(VGroup(cap[1], cap[2]), color=RED, scale_factor=1.08),
                  Wiggle(nf.lobes, scale_value=1.04, rotation_angle=0.015 * TAU), run_time=1.0)

        lig = bchip("ligase", PURPLE, 26).move_to([-5.3, 0.2, 0])
        self.at("A second ligase")
        self.play(FadeIn(lig, shift=RIGHT * 0.3), run_time=0.6)
        chain = bead_chain([-3.5, 0.2, 0], [-1.7, 0.2, 0], 5)
        self.at("adds a chain")
        self.play(FadeIn(chain[0]), LaggedStart(*[FadeIn(b, scale=0.4) for b in chain[1:]], lag_ratio=0.15), run_time=1.1)
        lys = T("lysine-48 chain", 26, UBQ).move_to([-2.6, -0.5, 0])
        self.at("lysine")
        self.play(FadeIn(lys, shift=UP * 0.1), run_time=0.5)

        prot = bchip("proteasome", MAGENTA, 26).move_to([-5.0, 0.2, 0])
        self.at("That chain sends")
        self.play(FadeOut(lig), run_time=0.4)
        self.at("to the proteasome")
        self.play(FadeIn(prot, shift=RIGHT * 0.3), run_time=0.6)
        taken = VGroup(cap, chain, p1, p2, lys)
        self.at("destroys it")
        self.play(taken.animate.scale(0.12).move_to(prot.get_center()).set_opacity(0), pulse(prot, MAGENTA, 1.15),
                  FadeOut(blocked), run_time=1.0)
        self.play(FadeOut(prot), run_time=0.3)

        sig_lbl = T("nuclear signal", 24, BLUE).move_to([-3.7, -0.35, 0])
        tip = C + np.array([0, -1.0 * s, 0])
        leader = Line(sig_lbl.get_right() + RIGHT * 0.05, tip + LEFT * 0.12 + UP * 0.12, color=BLUE, stroke_width=2.5)
        path = arr(tip + DOWN * 0.05, nuc_top, BLUE, w=5, tip=0.22)
        self.at("Now nothing covers")
        self.play(FadeIn(sig_lbl), Create(leader), Indicate(nf.tab, color=BLUE, scale_factor=1.35), run_time=0.8)
        self.at("into the nucleus")
        self.play(GrowArrow(path), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Enter(Film):
    """NF-kB drops into the nucleus, settles on the DNA, genes go on; nothing was transcribed or translated first."""

    def construct(self):
        C = np.array([-0.5, 1.0, 0])
        nuc = nucleus_rect()
        nuc_lbl = T("nucleus", 24, GREY).move_to([-5.2, -1.95, 0])
        dna = dna_line(-3.1)
        genes = genes_row(-3.1)
        mem = membrane_h(3.0)
        nf = nfkb(1.0, label="NF-κB", lsize=30).shift(C)
        self.add(mem, nuc, nuc_lbl, dna, genes, nf)

        self.at("already folded")
        self.play(Indicate(nf.lobes, color=BLUE, scale_factor=1.06), run_time=0.8)

        # enters the nucleus: the nucleus grows to fill the frame while NF-kB goes in
        big = nucleus_rect(top=3.3)
        dna.set_z_index(5)
        genes.set_z_index(6)
        lab = nf.label
        nf.remove(lab)
        self.add(lab)
        self.at("enters the nucleus")
        self.play(nf.animate.shift(DOWN * 1.9), lab.animate.shift(DOWN * 1.9), run_time=1.0)
        self.play(ReplacementTransform(nuc, big), FadeOut(mem), FadeOut(nuc_lbl), FadeOut(lab),
                  dna.animate.shift(UP * 0.9), genes.animate.shift(UP * 0.9),
                  nf.animate.shift(np.array([-0.5, 0.6, 0.0]) - nf.lobes.get_center()),
                  run_time=1.4)
        big_lbl = T("nucleus", 24, GREY).move_to([-5.2, 2.85, 0])
        self.play(FadeIn(big_lbl), run_time=0.3)

        # the two proteins settle on the DNA: the line passes in front of one and behind the other
        nf.lobes[0].set_z_index(1)
        nf.lobes[1].set_z_index(8)
        site = Line([-1.9, -2.2, 0], [-0.7, -2.2, 0], color=TEXT, stroke_width=10).set_z_index(5)
        site_lbl = T("site", 24, TEXT).move_to([-3.8, -2.85, 0])
        site_ldr = Line([-3.4, -2.7, 0], [-2.0, -2.3, 0], color=TEXT, stroke_width=2.5).set_z_index(5)
        self.at("wrap around the DNA")
        self.play(nf.animate.shift(np.array([-1.3, -2.0, 0.0]) - nf.lobes.get_center()), run_time=1.1)
        self.play(FadeOut(nf.tab), FadeIn(site), FadeIn(site_lbl), Create(site_ldr), run_time=0.4)
        self.at("each reads")
        self.play(Indicate(nf.lobes[0], color=BLUE, scale_factor=1.1), run_time=0.6)
        self.play(Indicate(nf.lobes[1], color=BLUE, scale_factor=1.1), run_time=0.6)

        self.at("switches on its genes")
        self.play(*[a for g in genes for a in recolor(g, GREEN)], run_time=0.9)

        gh = [bchip(name, GREY, 28).move_to([x, 0.9, 0]) for x, name in ((-2.6, "transcribe"), (2.6, "translate"))]
        strikes = [strike(c) for c in gh]
        self.at("Nothing had to be")
        self.play(FadeIn(gh[0], shift=DOWN * 0.1), FadeIn(gh[1], shift=DOWN * 0.1), run_time=0.6)
        self.at("transcribed")
        self.play(Create(strikes[0]), run_time=0.4)
        self.at("translated")
        self.play(Create(strikes[1]), run_time=0.4)

        clk = clock(0.6).move_to([5.3, 2.0, 0])
        clk_lbl = T("minutes", 24, GREY).next_to(clk, DOWN, buff=0.2)
        self.at("within minutes")
        self.play(FadeIn(clk), FadeIn(clk_lbl), run_time=0.4)
        self.play(Rotate(clk.hand, angle=-TAU * 0.85, about_point=clk.face.get_center(), rate_func=linear), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(Film):
    """the 1986 result in one picture, then the rule in three panels."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=0.9, width=7.4, height=5.9, stroke_color=GREY, stroke_width=4).move_to([-2.4, -0.1, 0])
        cell_lbl = T("cell line", 26, GREY).move_to([-5.0, 2.3, 0])
        gauge = Rectangle(width=0.75, height=3.6, stroke_color=BLUE, stroke_width=3).move_to([-0.3, -0.4, 0])
        g_lbl = T("NF-κB activity", 26, BLUE).move_to([-0.3, 1.9, 0])
        fill = Rectangle(width=0.75, height=0.02, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
        fill.align_to(gauge, DOWN).align_to(gauge, LEFT)

        self.play(Create(cell), FadeIn(cell_lbl), run_time=0.8)
        self.at("with no")
        self.play(Create(gauge), FadeIn(g_lbl), FadeIn(fill), run_time=0.8)

        ps = bchip("protein synthesis", GREY, 26).move_to([4.2, 1.9, 0])
        pstrike = strike(ps)
        self.at("block its protein synthesis")
        self.play(FadeIn(ps, shift=DOWN * 0.1), run_time=0.5)
        self.play(Create(pstrike), run_time=0.5)

        lps = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9).move_to([4.6, -0.3, 0])
        lps_lbl = T("lipopolysaccharide", 24, ORANGE).move_to([3.7, 0.5, 0])
        self.at("Lipopolysaccharide still makes")
        self.play(FadeIn(lps), FadeIn(lps_lbl), run_time=0.4)
        self.play(lps.animate.move_to([1.65, -0.3, 0]), run_time=0.9)
        newfill = Rectangle(width=0.75, height=3.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
        newfill.align_to(gauge, DOWN).align_to(gauge, LEFT).shift(UP * 0.15)
        self.at("activity appear")
        self.play(Transform(fill, newfill), run_time=1.3)

        nf = nfkb(0.95, label="NF-κB", lsize=28).shift([-3.5, -0.4, 0])
        cap = ikb_cap(2.1, 26).shift([-3.5, -0.4 - 0.8 * 0.95, 0])
        self.at("already have been there")
        self.play(FadeIn(nf), FadeIn(cap), run_time=0.9)
        self.at("inhibited")
        self.play(Indicate(VGroup(cap[1], cap[2]), color=RED, scale_factor=1.1), run_time=0.9)

        # the rule
        self.at("Here is the rule")
        self.play(*[FadeOut(m) for m in (cell, cell_lbl, gauge, g_lbl, fill, ps, pstrike, lps, lps_lbl, nf, cap)], run_time=0.7)

        PW, PH, PY = 3.95, 4.7, 0.2
        xs = [-4.15, 0.0, 4.15]
        panels = [RoundedRectangle(corner_radius=0.25, width=PW, height=PH, stroke_color=GREY, stroke_width=3).move_to([x, PY, 0]) for x in xs]
        caps = ["finish the\nactivator", "hold it outside\nthe nucleus", "remove its\ninhibitor"]
        cap_t = [T(c, 28, TEXT, line_spacing=0.8).move_to([x, PY - PH / 2 + 0.75, 0]) for c, x in zip(caps, xs)]
        SP = 0.85                      # scale of the NF-kB drawn in each panel
        NY = PY + 1.25                 # height of its centre
        CAPY = NY - 0.8 * SP           # the cap sits on the tab

        def mini_nuc(x):
            return RoundedRectangle(corner_radius=0.2, width=3.5, height=0.55, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.12).move_to([x, PY - 0.5, 0])

        # panel 1: a finished NF-kB
        nf1 = nfkb(SP).shift([xs[0], NY, 0])
        self.at("Finish the activator")
        self.play(Create(panels[0]), FadeIn(nf1), FadeIn(cap_t[0]), run_time=0.9)

        # panel 2: held outside the nucleus by IkB
        n2 = mini_nuc(xs[1])
        nf2 = nfkb(SP).shift([xs[1], NY, 0])
        cp2 = ikb_cap(1.9, 24).shift([xs[1], CAPY, 0])
        bar2 = inhib([xs[1], CAPY - 0.41, 0], [xs[1], PY - 0.22, 0], RED, w=4)
        self.at("hold it outside")
        self.play(Create(panels[1]), FadeIn(n2), FadeIn(nf2), FadeIn(cp2), FadeIn(bar2), FadeIn(cap_t[1]), run_time=1.0)

        # panel 3: the inhibitor removed, NF-kB goes in
        n3 = mini_nuc(xs[2])
        nf3 = nfkb(SP).shift([xs[2], NY, 0])
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=1.9, height=0.82), num_dashes=26).set_color(RED)
        ghost.move_to([xs[2], CAPY, 0])
        gx = strike(ghost)
        self.at("remove its inhibitor")
        self.play(Create(panels[2]), FadeIn(n3), FadeIn(nf3), FadeIn(ghost), Create(gx), FadeIn(cap_t[2]), run_time=1.0)
        self.play(FadeOut(ghost), FadeOut(gx), run_time=0.5)
        self.play(nf3.animate.shift(DOWN * 1.3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Finish the activator, hold it outside, remove its inhibitor."
