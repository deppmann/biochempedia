"""TNF receptor 1: one receptor, two messages  (Biochemistrypedia section film, Toll-like receptors and NF-kB)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

The one idea: NF-kB switches on the TNF gene; TNF binds TNF receptor 1 on the same cell and on its
neighbors; that receptor sends a "die" message and a "stay alive" message at once, and NF-kB's
survival genes normally make the second win. Block the NF-kB arm and the same TNF kills.

COLOR MAP (one color per concept, whole film)
  BLUE    = NF-kB
  ORANGE  = TNF, the cytokine
  PURPLE  = TNF receptor 1 and IKK (the relay)
  MAGENTA = the die message: death machinery, the cell killing itself
  GREEN   = the stay-alive message: survival arm, death-blocking genes, the cell surviving, genes on
  RED     = blocked / not so (strikes, the IκB that cannot be phosphorylated)
  GOLD    = a phosphate group
  GREY    = membranes, nucleus, DNA, labels
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
    return Succession(c.animate.scale(s), c.animate.scale(1 / s))


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
    TITLE = "One receptor, two messages"


# ---------------------------------------------------------------------------------------------
class S01Loop(Film):
    """NF-kB switches on the TNF gene; TNF capsules leave the cell."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=1.5, width=11.6, height=5.4, stroke_color=GREY, stroke_width=4).move_to([0, -0.8, 0])
        nuc = RoundedRectangle(corner_radius=0.4, width=10.0, height=2.7, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.08).move_to([0, -1.95, 0])
        nuc_lbl = T("nucleus", 24, GREY).move_to([4.2, -0.95, 0])
        dna = Line([-4.7, -2.8, 0], [4.7, -2.8, 0], color=GREY, stroke_width=6)
        g1 = bchip("gene", GREY, 22, pad=0.1).move_to([-0.4, -2.8, 0])
        g2 = bchip("TNF gene", GREY, 22, pad=0.1).move_to([1.4, -2.8, 0])
        g3 = bchip("gene", GREY, 22, pad=0.1).move_to([3.2, -2.8, 0])
        nf = nfkb(0.55, tab=False).move_to([-2.4, -1.75, 0])
        nf_lbl = T("NF-κB", 28, BLUE, weight=BOLD).move_to([-4.2, -1.75, 0])
        self.play(Create(cell), FadeIn(nuc), FadeIn(nuc_lbl), FadeIn(dna), FadeIn(VGroup(g1, g2, g3)),
                  FadeIn(nf), FadeIn(nf_lbl), run_time=1.5)

        self.at("switches on")
        self.play(*recolor(g1, GREEN), *recolor(g3, GREEN), Indicate(nf, color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("one of its target genes")
        self.play(*recolor(g2, GREEN), pulse(g2, GREEN, 1.15), run_time=0.9)

        t1 = capsule("TNF", ORANGE, 22, w=1.1, h=0.55).move_to([1.4, -2.1, 0])
        lab1 = T("tumor necrosis factor", 24, ORANGE).move_to([3.9, 0.3, 0])
        self.at("tumor necrosis factor")
        self.play(FadeIn(t1), run_time=0.3)
        self.play(t1.animate.move_to([0.6, 0.3, 0]), FadeIn(lab1), run_time=1.0)
        lab2 = T("cytokine: a signaling protein", 22, GREY).move_to([3.5, 1.05, 0])
        lab2.shift(RIGHT * min(0, 5.7 - lab2.get_right()[0]))
        self.at("a cytokine")
        self.play(FadeIn(lab2, shift=DOWN * 0.1), run_time=0.6)

        self.at("immune cells secrete")
        self.play(t1.animate.move_to([0.6, 3.0, 0]), run_time=1.6)
        q = T("?", 52, TEXT).move_to([3.4, 3.0, 0])
        self.at("Where does it go")
        self.play(FadeIn(q), Indicate(t1, color=ORANGE, scale_factor=1.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tnf_cell(cx, name):
    """a small cell with a receptor in its top membrane; returns a dict of parts."""
    d = {}
    d["cell"] = RoundedRectangle(corner_radius=0.5, width=3.8, height=3.9, stroke_color=GREY, stroke_width=4).move_to([cx, -0.55, 0])
    back = Rectangle(width=0.55, height=0.9, stroke_width=0, fill_color=BG, fill_opacity=1)
    rec = RoundedRectangle(corner_radius=0.12, width=0.55, height=0.9, stroke_color=PURPLE, stroke_width=4,
                           fill_color=PURPLE, fill_opacity=0.35)
    d["rec"] = VGroup(back, rec).move_to([cx, 1.4, 0]).set_z_index(2)
    d["rlab"] = T("TNF receptor 1", 22, PURPLE).move_to([cx, 0.75, 0])
    d["ikk"] = bchip("IKK", PURPLE, 24).move_to([cx, -0.4, 0])
    d["a1"] = arr([cx, 0.5, 0], [cx, -0.04, 0], PURPLE, w=4, tip=0.18)
    d["nf"] = bchip("NF-κB", BLUE, 24).move_to([cx, -1.55, 0])
    d["a2"] = arr([cx, -0.78, 0], [cx, -1.19, 0], PURPLE, w=4, tip=0.18)
    d["name"] = T(name, 24, GREY).move_to([cx, -2.85, 0])
    return d


class S02Spread(Film):
    """TNF lands on the same cell and its neighbors; each signals to IKK and NF-kB."""

    def construct(self):
        mid = tnf_cell(0.0, "this cell")
        lef = tnf_cell(-4.3, "neighbor")
        rig = tnf_cell(4.3, "neighbor")
        cells = [mid, lef, rig]
        t_mid = capsule("TNF", ORANGE, 22, w=1.1, h=0.55).move_to([0, 3.0, 0])
        self.play(*[FadeIn(VGroup(c["cell"], c["rec"])) for c in cells], FadeIn(t_mid), run_time=0.9)

        self.at("binds")
        self.play(t_mid.animate.move_to([0, 2.15, 0]), FadeIn(mid["rlab"]), run_time=0.8)
        self.at("on the same cell")
        self.play(FadeIn(mid["name"]), mid["cell"].animate.set_stroke(TEXT), run_time=0.6)
        t_l = capsule("TNF", ORANGE, 22, w=1.1, h=0.55).move_to([-4.3, 3.0, 0])
        t_r = capsule("TNF", ORANGE, 22, w=1.1, h=0.55).move_to([4.3, 3.0, 0])
        self.at("and on its neighbors")
        self.play(FadeIn(t_l), FadeIn(t_r), run_time=0.3)
        self.play(t_l.animate.move_to([-4.3, 2.15, 0]), t_r.animate.move_to([4.3, 2.15, 0]),
                  FadeIn(lef["rlab"]), FadeIn(rig["rlab"]), FadeIn(lef["name"]), FadeIn(rig["name"]), run_time=0.8)

        self.at("also signals to")
        self.play(*[FadeIn(c["ikk"]) for c in cells], *[GrowArrow(c["a1"]) for c in cells], run_time=0.8)
        self.at("kappa B")
        self.play(*[GrowArrow(c["a2"]) for c in cells], *[FadeIn(c["nf"]) for c in cells], run_time=0.8)
        self.at("the alarm spreads")
        self.play(*[pulse(c["nf"], BLUE, 1.2) for c in cells], run_time=1.0)

        q = T("?", 40, MAGENTA)
        qbox = VGroup(DashedVMobject(RoundedRectangle(corner_radius=0.12, width=0.7, height=0.7), num_dashes=24).set_color(MAGENTA),
                      q).move_to([1.2, -0.95, 0])
        qarr = DashedLine([0.7, 0.55, 0], [1.2, -0.55, 0], color=MAGENTA, stroke_width=4)
        self.at("second message")
        self.play(FadeIn(qarr), FadeIn(qbox), pulse(mid["rec"], MAGENTA, 1.2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def two_arms():
    """the one receptor with its two arms (die / stay alive); dict of mobjects, all built, none added."""
    d = {}
    d["mem"] = membrane_h(2.2)
    back = Rectangle(width=1.0, height=1.2, stroke_width=0, fill_color=BG, fill_opacity=1)
    rec = RoundedRectangle(corner_radius=0.2, width=1.0, height=1.2, stroke_color=PURPLE, stroke_width=4,
                           fill_color=PURPLE, fill_opacity=0.35)
    d["rec"] = VGroup(back, rec).move_to([0, 2.2, 0]).set_z_index(2)
    d["rlab"] = T("TNF receptor 1", 26, PURPLE).move_to([-2.6, 2.9, 0])
    d["tnf"] = capsule("TNF", ORANGE, 22, w=1.1, h=0.55).move_to([0, 3.1, 0])
    # the die arm
    d["die_a"] = arr([-0.35, 1.55, 0], [-3.2, -0.25, 0], MAGENTA)
    d["die_l"] = T("die", 30, MAGENTA, weight=BOLD).move_to([-2.6, 1.0, 0])
    d["death"] = bchip("death machinery", MAGENTA, 26).move_to([-3.7, -0.7, 0])
    d["kill_a"] = arr([-3.7, -1.05, 0], [-3.7, -1.9, 0], MAGENTA, w=4)
    d["kill"] = bchip("cell kills itself", MAGENTA, 24).move_to([-3.7, -2.3, 0])
    # the stay-alive arm
    d["stay_a"] = arr([0.35, 1.55, 0], [2.8, 0.95, 0], GREEN)
    d["stay_l"] = T("stay alive", 30, GREEN, weight=BOLD).move_to([1.95, 1.75, 0])
    d["nf"] = bchip("NF-κB", BLUE, 26).move_to([3.7, 0.9, 0])
    d["nf_a"] = arr([3.7, 0.55, 0], [3.7, -0.3, 0], GREEN, w=4)
    d["block"] = bchip("death-blocking genes", GREEN, 24).move_to([3.7, -0.7, 0])
    d["inhib"] = inhib([1.7, -0.7, 0], [-2.1, -0.7, 0], GREEN)
    return d


class S03Both(Film):
    """one receptor, two arms: die and stay alive; the second normally wins."""

    def construct(self):
        d = two_arms()
        self.play(FadeIn(d["mem"]), FadeIn(d["rec"]), FadeIn(d["rlab"]), FadeIn(d["tnf"]), run_time=0.9)

        self.at("death receptor")
        self.play(pulse(d["rec"], MAGENTA, 1.2), run_time=0.9)
        self.at("kill itself")
        self.play(GrowArrow(d["die_a"]), FadeIn(d["die_l"]), run_time=0.6)
        self.play(FadeIn(d["death"]), run_time=0.4)
        self.play(GrowArrow(d["kill_a"]), FadeIn(d["kill"]), run_time=0.6)
        self.at("Usually it does not")
        notlbl = T("usually not", 24, RED).move_to([-0.2, -2.3, 0])
        self.play(Create(strike(d["kill"])), FadeIn(notlbl), run_time=0.6)
        self.at("switches on genes")
        self.play(GrowArrow(d["stay_a"]), FadeIn(d["nf"]), run_time=0.7)
        self.play(GrowArrow(d["nf_a"]), FadeIn(d["block"]), run_time=0.6)
        self.at("block the death machinery")
        self.play(Create(d["inhib"]), pulse(d["death"], MAGENTA, 1.1), run_time=0.9)
        self.at("die and stay alive")
        self.play(FadeIn(d["stay_l"]), Indicate(d["die_l"], color=MAGENTA, scale_factor=1.3), run_time=0.8)
        self.at("at once")
        self.play(Indicate(d["die_l"], color=MAGENTA, scale_factor=1.3), Indicate(d["stay_l"], color=GREEN, scale_factor=1.3), run_time=0.8)
        live = bchip("cell usually survives", GREEN, 24).move_to([3.7, -2.3, 0])
        self.at("second message")
        self.play(d["die_a"].animate.set_opacity(0.35), d["die_l"].animate.set_opacity(0.35),
                  FadeIn(live), d["inhib"].animate.set_stroke(width=9), run_time=1.0)
        self.finish()


class S04Block(Film):
    """cultured cells with the NF-kB arm blocked: the same TNF kills."""

    def construct(self):
        d = two_arms()
        d["die_a"].set_opacity(0.35)
        d["die_l"].set_opacity(0.35)
        d["inhib"].set_stroke(width=9)
        sk = strike(d["kill"])
        notlbl = T("usually not", 24, RED).move_to([-0.2, -2.3, 0])
        live = bchip("cell usually survives", GREEN, 24).move_to([3.7, -2.3, 0])
        self.add(*d.values(), sk, notlbl, live)

        cult = T("cultured cells", 26, GREY).move_to([4.7, 3.15, 0])
        cap = ikb_cap(1.5, 26).move_to([5.45, 0.8, 0])
        ph = pbadge(0.26).move_to([5.45, 0.05, 0])
        phx = Line(ph.get_corner(DL) + DL * 0.08, ph.get_corner(UR) + UR * 0.08, color=RED, stroke_width=6)
        phlab = T("cannot be\nphosphorylated", 22, RED).move_to([5.2, 1.7, 0])
        self.at("cultured cells")
        self.play(FadeIn(cult), run_time=0.6)
        self.at("arm is blocked")
        cut = Cross(d["nf_a"], stroke_color=RED, stroke_width=7).scale(0.7)
        self.play(Create(cut), d["block"].animate.set_opacity(0.3), FadeOut(d["inhib"]), FadeOut(live), FadeOut(sk), FadeOut(notlbl), run_time=0.8)
        self.at("for example")
        self.play(FadeIn(cap), run_time=0.5)
        self.at("cannot be phosphorylated")
        self.play(FadeIn(ph), FadeIn(phlab), run_time=0.5)
        self.play(Create(phx), run_time=0.4)
        self.at("The same")
        self.play(d["die_a"].animate.set_opacity(1), d["die_l"].animate.set_opacity(1), run_time=0.6)
        self.play(*recolor(d["kill"], MAGENTA), pulse(d["kill"], MAGENTA, 1.15),
                  pulse(d["death"], MAGENTA, 1.12), run_time=1.0)
        later = T("the death arm: a later lesson", 24, GREY).move_to([-3.2, -3.15, 0])
        self.at("belongs to a later lesson")
        self.play(FadeIn(later), run_time=0.6)
        rule = T("NF-κB normally makes stay-alive win", 26, GREEN).move_to([2.6, -2.3, 0])
        self.at("Keep this rule")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S05End(EndCard):
    LINE = "NF-κB normally makes the stay-alive message win."
