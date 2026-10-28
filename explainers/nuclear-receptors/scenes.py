"""Nuclear receptors: where helix 12 lies decides whether the groove is free  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the hormone (estradiol), the agonist
  BLUE   = the receptor (its hormone-binding block and its DNA-binding block)
  PINK   = helix 12, the lid
  ORANGE = the groove (the surface a co-activator fits into)
  PURPLE = a co-activator, the enzymes it brings, and the "helper proteins"
  GOLD   = an acetyl group (the round "Ac" badge)
  WHITE  = RNA polymerase (neutral machinery), tissue names
  RED    = the antagonist (tamoxifen) and whatever is blocked or ruled out
  GREEN  = on / free (gene switched on, groove free)
  GREY   = membrane, DNA, histones, gene, tissue names, labels

No molecular structures: the hormone-binding domain is a rounded block with a notch for the pocket and a
shallow notch for the groove; helix 12 is a pink capsule that swings on a hinge; the hormone is a dot or a
chip; DNA is a line, histones are discs, the gene is a block on the line.

ONE RULE FOR THE GROOVE (every scene): its outline is DASHED whenever helix 12 is not in its closed, agonist
position (lid open, lid blocked, or helix 12 lying in the groove), and SOLID only when the lid is closed.

One picture, three framings of the same parts (the block is scaled, never redrawn differently):
  CLOSE (scenes 3 and 5)  the hormone-binding block fills the frame.
  WIDE  (scenes 2 and 4)  the whole receptor stands on the DNA, block smaller.
  ROW   (scene 6)         three small copies, then two side by side.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F08BB4"
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
SW = 4                                   # one stroke width everywhere, so scaling a group never changes it

K3, O3 = 1.2, np.array([0.0, -1.5, 0.0])   # the hormone-binding block in the CLOSE framing
K2, O2 = 0.95, np.array([-2.45, 0.8, 0.0])
K4, O4 = 0.75, np.array([-3.45, 0.8, 0.0])
K6 = 0.65
COLS = [-3.2, 3.2]                 # the two columns of scene 6 (breast, uterus)
COL_Y = 0.35


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=22):
    """a dashed grey chip: something that is NOT part of this pathway."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def upath(cx, yt, w, d, r, color, sw=SW):
    """an open U hanging from the line y = yt (the outline of a notch): down, round the bottom, up."""
    r = min(r, w / 2, d)
    a, b, q = d - r, w - 2 * r, r * PI / 2
    total = 2 * a + b + 2 * q
    xl, xr, yb = cx - w / 2, cx + w / 2, yt - d

    def f(t):
        t = min(max(t, 0.0), total)
        if t <= a:
            return np.array([xl, yt - t, 0.0])
        t -= a
        if t <= q:
            th = t / r
            return np.array([xl + r - r * np.cos(th), yb + r - r * np.sin(th), 0.0])
        t -= q
        if t <= b:
            return np.array([xl + r + t, yb, 0.0])
        t -= b
        if t <= q:
            th = t / r
            return np.array([xr - r + r * np.sin(th), yb + r - r * np.cos(th), 0.0])
        t -= q
        return np.array([xr, yb + r + t, 0.0])
    return ParametricFunction(f, t_range=[0, total, total / 120], color=color, stroke_width=sw)


# ---------------------------------------------------------------------------------------------
# the receptor
# ---------------------------------------------------------------------------------------------
class Rec:
    """The hormone-binding block at scale k, centred on O.

    A rounded block (7.2k x 3.0k) with a round-bottomed notch for the pocket and a long shallow notch for the
    groove on its top face, and helix 12 as a capsule hinged just left of the pocket. Every part is its own
    mobject; layers() lists them in drawing order.
    """

    def __init__(self, k, O, lid="open", groove="dashed"):
        self.k, self.O = k, np.array(O, float)
        ox, oy = self.O[0], self.O[1]
        self.yt = yt = oy + 1.5 * k                       # the top face
        self.pcx, self.pw, self.pd = ox - 1.4 * k, 1.9 * k, 1.9 * k
        self.gx0, self.gx1, self.gd = ox + 0.0 * k, ox + 3.0 * k, 0.46 * k
        self.gcx = (self.gx0 + self.gx1) / 2
        self.P = np.array([ox - 2.8 * k, yt, 0.0])        # hinge of helix 12
        self.body = RoundedRectangle(corner_radius=0.5 * k, width=7.2 * k, height=3.0 * k, stroke_color=BLUE, stroke_width=SW,
                                     fill_color=BLUE, fill_opacity=0.2).move_to(self.O)
        self.body.set_z_index(-2)
        ph = self.pd + 1.2 * k
        self.pocket_fill = RoundedRectangle(corner_radius=self.pw / 2, width=self.pw, height=ph, stroke_width=0,
                                            fill_color=BG, fill_opacity=1).move_to([self.pcx, yt - self.pd + ph / 2, 0])
        self.pocket_fill.set_z_index(-1)
        self.pocket_line = upath(self.pcx, yt, self.pw, self.pd, self.pw / 2, BLUE)
        gw, gh = self.gx1 - self.gx0, self.gd + 0.4 * k
        self.groove_fill = RoundedRectangle(corner_radius=self.gd / 2, width=gw, height=gh, stroke_width=0,
                                            fill_color=BG, fill_opacity=1).move_to([self.gcx, yt - self.gd + gh / 2, 0])
        self.groove_fill.set_z_index(-1)
        self.groove_line = upath(self.gcx, yt, gw, self.gd, self.gd / 2, ORANGE)
        self.groove_dash = DashedVMobject(upath(self.gcx, yt, gw, self.gd, self.gd / 2, ORANGE), num_dashes=34)
        self.groove_dash.set_stroke(ORANGE, SW, opacity=0.9)
        self.groove_line.set_z_index(-1)
        self.groove_dash.set_z_index(-1)
        self.groove = self.groove_dash if groove == "dashed" else self.groove_line
        L, th = 2.6 * k, 0.42 * k
        shape = lambda **kw: RoundedRectangle(corner_radius=th / 2, width=L, height=th, **kw)
        back = shape(stroke_width=0, fill_color=BG, fill_opacity=1)
        edge = shape(stroke_color=PINK, stroke_width=SW, fill_color=PINK, fill_opacity=0.45)
        self.lid = VGroup(back, edge).move_to(self.P + np.array([L / 2, th / 2, 0]))
        self.lid.edge = edge
        if lid == "open":
            self.lid.rotate(PI / 2, about_point=self.P)

    def layers(self):
        return [self.body, self.pocket_fill, self.groove_fill, self.pocket_line, self.groove, self.lid]

    def lid_label_open(self):
        return np.array([self.P[0] - 0.55 * self.k, self.yt + 1.55 * self.k, 0])

    def lid_label_closed(self):
        return np.array([self.P[0] + 1.3 * self.k, self.yt + 0.75 * self.k, 0])

    def lid_in_groove(self):
        return np.array([self.gcx, self.yt - 0.23 * self.k, 0])


def hdot(rec):
    c = Circle(radius=0.42 * rec.k, stroke_color=YELLOW, stroke_width=SW, fill_color=YELLOW,
               fill_opacity=0.55).move_to([rec.pcx, rec.yt - 1.0 * rec.k, 0])
    c.set_z_index(3)
    return c


def hchip(rec):
    return bchip("estradiol", YELLOW, 24, pad=0.14).move_to([rec.pcx, rec.yt - 1.0 * rec.k, 0])


def tam_parts(rec, inside=True):
    """tamoxifen's active form: a red dot in the pocket and a side chain standing out of the mouth."""
    k = rec.k
    c = Circle(radius=0.42 * k, stroke_color=RED, stroke_width=SW, fill_color=RED, fill_opacity=0.55)
    c.move_to([rec.pcx, rec.yt - 1.0 * k, 0])
    s = RoundedRectangle(corner_radius=0.12 * k, width=0.26 * k, height=1.58 * k, stroke_color=RED, stroke_width=SW,
                         fill_color=RED, fill_opacity=0.55).move_to([rec.pcx, rec.yt + 0.21 * k, 0])
    s.set_z_index(1)
    c.set_z_index(2)
    return c, s


def tam_core(k, O):
    """the block with tamoxifen in the pocket and helix 12 lying in the groove. Returns (VGroup, Rec)."""
    rec = Rec(k, O, "closed", "dashed")      # helix 12 lies in the groove: the groove is not completed
    rec.lid.move_to(rec.lid_in_groove())
    c, s = tam_parts(rec)
    return VGroup(*rec.layers(), s, c), rec


def peg_shape(rec, text=True):
    """the co-activator's short helix, lying in the groove."""
    k = rec.k
    cap = RoundedRectangle(corner_radius=0.22 * k, width=2.3 * k, height=0.44 * k, stroke_color=PURPLE, stroke_width=SW,
                           fill_color=PURPLE, fill_opacity=0.5).move_to([rec.gcx, rec.yt - 0.23 * k, 0])
    g = VGroup(cap)
    if text:
        g.add(T("LXXLL", 22, TEXT, weight=BOLD).move_to(cap))
    g.cap = cap
    return g


def coact(rec, text=True, dy=0.7, raised=0.0):
    """chip + stem + helix, docked in the groove (raised = lifted clear of it)."""
    peg = peg_shape(rec, text)
    chip_m = bchip("co-activator", PURPLE, 24, pad=0.16).move_to([rec.gcx, rec.yt + dy, 0])
    stem = Line([rec.gcx, rec.yt - 0.2 * rec.k, 0], [rec.gcx, rec.yt + dy, 0], color=PURPLE, stroke_width=6)
    g = VGroup(stem, peg, chip_m)
    g.peg, g.chip, g.stem = peg, chip_m, stem
    g.shift(UP * raised)
    return g


def chain_parts(rec):
    """hinge, DNA-binding block, DNA line and the short stretch it holds, under the hormone-binding block."""
    k, ox = rec.k, rec.O[0]
    ybot = rec.O[1] - 1.5 * k
    hinge = RoundedRectangle(corner_radius=0.1 * k, width=0.4 * k, height=0.6 * k + 0.04, stroke_color=BLUE, stroke_width=SW,
                             fill_color=BLUE, fill_opacity=0.2).move_to([ox, ybot - 0.3 * k + 0.02, 0])
    dbd = RoundedRectangle(corner_radius=0.3 * k, width=3.0 * k, height=1.1 * k, stroke_color=BLUE, stroke_width=SW,
                           fill_color=BLUE, fill_opacity=0.2).move_to([ox, ybot - 1.15 * k, 0])
    dna_y = ybot - 1.7 * k - 0.07
    stretch = Line([ox - 0.85 * k, dna_y, 0], [ox + 0.85 * k, dna_y, 0], color=TEXT, stroke_width=10)
    return hinge, dbd, dna_y, stretch


def gene_block(x, y, w=2.0):
    return Rectangle(width=w, height=0.28, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([x, y, 0])


def big_cell():
    """the big cell of scenes 1 and 2: an open-topped outline + a membrane bar across the top."""
    outline = upath(0, 1.35, 12.4, 4.75, 0.35, GREY, 3)
    mem = RoundedRectangle(corner_radius=0.1, width=12.4, height=0.3, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.35).move_to([0, 1.5, 0])
    return VGroup(outline, mem)


def qbox():
    """the unknown catcher: a dashed box with a question mark."""
    box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=2.0, height=2.0), num_dashes=40).set_color(GREY)
    return VGroup(box, T("?", 80, TEXT, weight=BOLD)).move_to([2.6, -1.0, 0])


def lid_flight(lid, B, top, run_time=2.0):
    """helix 12 swings up out of the way, turns flat, and settles at B (a rigid flight: it never squashes)."""
    start, c0 = lid.copy(), lid.get_center().copy()

    def upd(m, a):
        th = -PI / 2 * smooth(min(1.0, a / 0.4))
        x = c0[0] + a * (B[0] - c0[0])
        if a < 0.3:
            y = c0[1] + (top - c0[1]) * smooth(a / 0.3)
        elif a < 0.65:
            y = top
        else:
            y = top + (B[1] - top) * smooth((a - 0.65) / 0.35)
        m.become(start.copy().rotate(th, about_point=c0).shift(np.array([x - c0[0], y - c0[1], 0])))
    return UpdateFromAlphaFunc(lid, upd, run_time=run_time, rate_func=linear)


class Film(SpokenScene):
    def outro(self, *anims, then=None, after=None, run_time=0.3):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing (`then`) and bring in the new framing's extras (`after`)."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.8)
        if after:
            self.play(*after, run_time=0.4)
        if then or after:
            self.wait(0.05)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Nuclear receptors"
    TITLE = "One helix decides on or off"


# ---------------------------------------------------------------------------------------------
class S01Catch(Film):
    """the uterus keeps estradiol; a steroid crosses the membrane alone; what inside catches it?"""

    def construct(self):
        PW, MY, PB = 5.9, 1.35, -3.3

        def panel(cx):
            outline = upath(cx, MY - 0.15, PW, MY - 0.15 - PB, 0.3, GREY, 3)
            mem = RoundedRectangle(corner_radius=0.1, width=PW, height=0.3, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.35).move_to([cx, MY, 0])
            return VGroup(outline, mem)
        pl, pr = panel(-3.3), panel(3.3)
        self.play(FadeIn(pl), FadeIn(pr), run_time=0.7)

        tag = bchip("radioactive estradiol", YELLOW, 24, pad=0.16).move_to([0, 3.0, 0])
        dl = [Dot([x, 2.0, 0], radius=0.16, color=YELLOW) for x in (-4.4, -3.3, -2.2)]
        dr = [Dot([x, 2.0, 0], radius=0.16, color=YELLOW) for x in (2.2, 3.3, 4.4)]
        self.at("radioactive")
        self.play(FadeIn(tag, shift=DOWN * 0.15), *[FadeIn(d, scale=0.5) for d in dl + dr], run_time=0.6)

        lab_l = T("most tissues", 26, GREY).move_to([-3.3, -2.9, 0])
        self.at("almost every tissue")
        self.play(FadeIn(lab_l), run_time=0.4)
        ins = [(-4.4, 0.3), (-3.3, -0.6), (-2.2, -1.5)]
        self.at("hormone go again")
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dl, ins)], run_time=0.6)
        self.play(*[d.animate.move_to([x, 2.0, 0]) for d, (x, y) in zip(dl, ins)], run_time=0.6)
        self.play(*[FadeOut(d) for d in dl], run_time=0.3)

        lab_r = T("uterus and vagina", 26, GREY).move_to([3.3, -2.9, 0])
        self.at("The uterus")
        self.play(FadeIn(lab_r), run_time=0.4)
        stay = [(2.2, 0.3), (3.3, -0.6), (4.4, -1.5)]
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dr, stay)], run_time=0.8)
        self.at("keep it")
        self.play(pr[0].animate.set_stroke(YELLOW, 6), *[Indicate(d, color=TEXT, scale_factor=1.6) for d in dr], run_time=0.8)

        # one big cell: how the hormone gets in
        cell = big_cell()
        hc = bchip("estradiol", YELLOW, 26, pad=0.16).move_to([-2.0, 2.55, 0])
        self.at("is a steroid")
        self.play(FadeOut(VGroup(pl, pr, lab_l, lab_r, tag, *dr)), run_time=0.5)
        self.play(FadeIn(cell), FadeIn(hc), run_time=0.6)
        fat = T("dissolves in fat", 24, YELLOW).next_to(hc, RIGHT, buff=0.3)
        self.at("dissolves in fat")
        self.play(FadeIn(fat, shift=RIGHT * 0.1), pop(hc, 1.08), run_time=0.6)
        self.at("crosses the cell membrane")
        self.play(FadeOut(fat), hc.animate.move_to([-2.0, 0.2, 0]), run_time=1.3)
        self.at("on its own")
        self.play(pop(hc, 1.1), run_time=0.5)

        ghost = ghost_chip("surface receptor", 24).move_to([3.4, 2.5, 0])
        cross = strike(ghost)
        self.at("nothing on the outer surface")
        self.play(FadeIn(ghost, shift=DOWN * 0.1), run_time=0.5)
        self.at("has to receive it")
        self.play(Create(cross), run_time=0.4)

        q = qbox()
        self.at("What inside the cell")
        self.play(FadeIn(q, scale=0.9), run_time=0.6)
        self.at("built to catch it")
        self.play(hc.animate.move_to([0.45, -1.0, 0]), run_time=0.8)
        self.play(pop(q, 1.08), run_time=0.5)
        self.outro(FadeOut(ghost), FadeOut(cross))


# ---------------------------------------------------------------------------------------------
class S02Chain(Film):
    """the catcher is one chain with two grips: it is the transcription factor. (WIDE)"""

    def construct(self):
        cell, q = big_cell(), qbox()
        hc = bchip("estradiol", YELLOW, 26, pad=0.16).move_to([0.45, -1.0, 0])
        self.add(cell, hc, q)

        rec = Rec(K2, O2, "closed", "solid")
        hinge, dbd, dna_y, stretch = chain_parts(rec)
        hov = hdot(rec).move_to([rec.pcx, rec.yt + 0.8, 0])
        self.at("catches the hormone")
        self.play(pop(hc, 1.12), run_time=0.6)

        lab = T("receptor", 34, BLUE, weight=BOLD).move_to([3.7, O2[1], 0])
        pt = arr([2.4, O2[1], 0], [1.2, O2[1], 0], BLUE)
        self.at("is a receptor")
        self.play(FadeOut(cell), FadeOut(q), FadeOut(hc), FadeIn(rec.body, scale=0.92), FadeIn(hov, scale=0.8), run_time=0.9)
        self.play(FadeIn(rec.pocket_fill), Create(rec.pocket_line), FadeIn(lab), GrowArrow(pt), run_time=0.6)

        in_dbd = T("binds DNA", 26, BLUE).move_to(dbd)
        self.at("one chain")
        self.play(FadeIn(hinge, shift=UP * 0.15), FadeIn(dbd, shift=UP * 0.15), run_time=0.7)

        def badge(n, pos):
            c = Circle(radius=0.24, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1)
            return VGroup(c, T(str(n), 24, TEXT, weight=BOLD).move_to(c)).move_to(pos)
        b1 = badge(1, [rec.body.get_right()[0] + 0.45, rec.yt - 0.3, 0])
        b2 = badge(2, [dbd.get_right()[0] + 0.45, dbd.get_center()[1], 0])
        self.at("two grips")
        self.play(FadeOut(lab), FadeOut(pt), FadeIn(b1, scale=0.5), FadeIn(b2, scale=0.5),
                  *glow(rec.body, dbd, s=1.03), run_time=0.8)

        in_hbd = T("binds hormone", 26, BLUE).move_to([rec.O[0] + 1.5 * rec.k, O2[1] - 0.2, 0])
        self.at("closes around the hormone")
        self.play(hov.animate.move_to([rec.pcx, rec.yt - 1.0 * rec.k, 0]), run_time=0.8)
        self.play(FadeIn(in_hbd), run_time=0.4)

        dna = Line([-6.2, dna_y - 0.9, 0], [6.2, dna_y - 0.9, 0], color=GREY, stroke_width=6)
        gene = gene_block(4.4, dna_y - 0.9)
        gene_lbl = T("gene", 24, GREY).move_to([4.4, dna_y - 0.9 - 0.5, 0])
        self.add(dna, gene, gene_lbl)
        self.at("takes hold")
        self.play(dna.animate.shift(UP * 0.9), gene.animate.shift(UP * 0.9), gene_lbl.animate.shift(UP * 0.9), run_time=0.6)
        spec = T("a specific short stretch", 24, TEXT).move_to([rec.O[0], dna_y - 0.5, 0])
        self.at("specific short stretch")
        self.play(Create(stretch), FadeIn(in_dbd), FadeIn(spec, shift=UP * 0.1), run_time=0.6)

        sm = ghost_chip("second messenger", 24).move_to([4.0, 2.4, 0])
        x1 = strike(sm)
        self.at("No second messenger")
        self.play(FadeIn(sm), run_time=0.3)
        self.play(Create(x1), run_time=0.3)
        kc = ghost_chip("kinase cascade", 24).move_to([4.0, 1.4, 0])
        x2 = strike(kc)
        self.at("kinase cascade")
        self.play(FadeIn(kc), run_time=0.3)
        self.play(Create(x2), run_time=0.3)

        tf = T("transcription factor", 32, BLUE, weight=BOLD).move_to([4.0, O2[1] - 0.3, 0])
        tp = arr([1.75, O2[1] - 0.3, 0], [1.15, O2[1] - 0.3, 0], BLUE)
        self.at("transcription factor")
        self.play(FadeOut(VGroup(sm, x1, kc, x2)), FadeOut(b1), FadeOut(b2), FadeIn(tf, shift=LEFT * 0.1), GrowArrow(tp), run_time=0.8)

        self.at("binds")
        self.play(*glow(dbd, s=1.06), run_time=0.6)
        ctl = arr([dbd.get_right()[0] + 0.3, dna_y + 0.35, 0], [gene.get_left()[0] - 0.1, dna_y + 0.35, 0], TEXT)
        self.at("controls whether")
        self.play(GrowArrow(ctl), run_time=0.6)
        rna = chip("RNA", GREY, size=24, pad=0.14).move_to([4.4, dna_y + 1.0, 0])
        ra = arr([4.4, dna_y + 0.25, 0], [4.4, dna_y + 0.65, 0], GREY, w=4, tip=0.16)
        self.at("copied into")
        self.play(*glow(gene, s=1.12), FadeIn(rna, shift=UP * 0.1), GrowArrow(ra), run_time=0.7)

        self.at("receptor is one")
        self.play(*glow(rec.body, dbd, hinge, s=1.03), *glow(tf, s=1.06), run_time=0.7)

        # zoom in on the hormone-binding block (CLOSE); the lid and the groove come into view
        rec3 = Rec(K3, O3, "open", "dashed")
        carry = VGroup(rec.body, rec.pocket_fill, rec.pocket_line, hov)
        rest = [hinge, dbd, in_dbd, in_hbd, dna, gene, gene_lbl, stretch, spec, tf, tp, ctl, rna, ra]
        self.outro(*[FadeOut(m) for m in rest],
                   then=[carry.animate.scale(K3 / K2, about_point=O2).shift(O3 - O2)],
                   after=[FadeIn(rec3.lid), FadeIn(rec3.groove_fill), FadeIn(rec3.groove), FadeOut(hov), FadeIn(hchip(rec3))])


# ---------------------------------------------------------------------------------------------
class S03Lid(Film):
    """helix 12 folds over the pocket like a lid and completes the groove a co-activator fits. (CLOSE)"""

    def construct(self):
        rec = Rec(K3, O3, "open", "dashed")
        hch = hchip(rec)
        self.add(*rec.layers(), hch)
        yt, k = rec.yt, rec.k

        lab12 = T("helix 12", 30, PINK, weight=BOLD)
        lab12.next_to(rec.lid_label_open(), LEFT, buff=0.1)
        self.at("moving part")
        self.play(FadeIn(lab12, shift=RIGHT * 0.1), *glow(rec.lid.edge, s=1.06, color=PINK), run_time=0.7)

        dom = T("hormone-binding domain", 28, BLUE).move_to([O3[0], O3[1] - 1.5 * k + 0.45, 0])
        self.at("last helix")
        self.play(FadeIn(dom, shift=UP * 0.1), *glow(rec.body, s=1.01, color=BLUE), run_time=0.7)

        ag = T("agonist: switches the receptor on", 28, YELLOW).move_to(dom)
        self.at("An agonist")
        self.play(ReplacementTransform(dom, ag), *glow(hch[1], hch[2], s=1.12, color=TEXT), run_time=0.8)
        self.at("With one in the pocket")
        self.play(*glow(hch[1], hch[2], s=1.15, color=TEXT), run_time=0.7)

        self.at("folds across")
        self.play(Rotate(rec.lid, -PI / 2, about_point=rec.P), lab12.animate.move_to(rec.lid_label_closed()),
                  FadeOut(ag), run_time=1.0)

        glab = T("groove", 30, ORANGE, weight=BOLD).move_to([rec.gcx, yt - 0.9 * k, 0])
        self.at("completes a shallow")
        self.play(FadeOut(rec.groove), FadeIn(rec.groove_line), FadeIn(glab, shift=UP * 0.1), run_time=0.7)
        self.play(*glow(rec.groove_line, s=1.03, color=TEXT), run_time=0.5)

        co = coact(rec, text=True, dy=0.85, raised=1.7)
        self.at("helper protein")
        self.play(FadeIn(co, shift=DOWN * 0.2), run_time=0.7)
        self.at("short helix")
        self.play(*glow(co.peg.cap, s=1.08, color=TEXT), run_time=0.7)
        self.at("fits the groove")
        self.play(co.animate.shift(DOWN * 1.7), run_time=0.9)
        self.play(*glow(rec.groove_line, co.peg.cap, s=1.03, color=TEXT), run_time=0.5)

        self.at("message gets through")
        self.play(*glow(rec.groove_line, rec.lid.edge, co.peg.cap, s=1.04, color=TEXT), run_time=0.8)

        # zoom out (WIDE): the receptor stands on the DNA with the co-activator still in the groove
        k4 = Rec(K4, O4, "closed", "solid")
        hd1 = hdot(rec)
        carry = VGroup(rec.body, rec.pocket_fill, rec.groove_fill, rec.pocket_line, rec.groove_line, rec.lid, co.peg.cap, hd1)
        co4 = coact(k4, text=False, dy=0.9)
        hinge, dbd, dna_y, stretch = chain_parts(k4)
        dna = Line([-6.2, dna_y, 0], [6.2, dna_y, 0], color=GREY, stroke_width=6)
        self.outro(FadeOut(lab12), FadeOut(glab), FadeOut(co.chip), FadeOut(co.stem), FadeOut(co.peg[1]),
                   FadeOut(hch), FadeIn(hd1),
                   then=[carry.animate.scale(K4 / K3, about_point=O3).shift(O4 - O3)],
                   after=[FadeIn(co4.chip), FadeIn(co4.stem), FadeIn(hinge), FadeIn(dbd), FadeIn(dna), FadeIn(stretch)])


# ---------------------------------------------------------------------------------------------
class S04Loosen(Film):
    """the co-activator brings enzymes; acetyl groups loosen the histones; the gene can be copied. (WIDE)"""

    def construct(self):
        rec = Rec(K4, O4, "closed", "solid")
        hinge, dbd, dna_y, stretch = chain_parts(rec)
        dna = Line([-6.2, dna_y, 0], [6.2, dna_y, 0], color=GREY, stroke_width=6)
        co = coact(rec, text=False, dy=0.9)
        hd = hdot(rec)
        GX = 5.1
        gene = gene_block(GX, dna_y, 1.4)
        gene_lbl = T("gene", 24, GREY).move_to([GX, dna_y - 0.5, 0])
        self.add(*rec.layers(), hd, hinge, dbd, dna, stretch, co, gene, gene_lbl)

        # histones: discs with the DNA wound round them
        R = 0.55
        packed, spread = [0.35, 1.5, 2.65], [-0.1, 1.5, 3.1]
        discs, rings = [], []
        for x in packed:
            discs.append(Circle(radius=R, stroke_width=0, fill_color=GREY, fill_opacity=0.55).move_to([x, dna_y, 0]))
            rings.append(Circle(radius=R + 0.1, stroke_color=GREY, stroke_width=7).move_to([x, dna_y, 0]))
        hist = [VGroup(r, d) for r, d in zip(rings, discs)]
        self.at("wound around")
        self.play(LaggedStart(*[GrowFromCenter(h) for h in hist], lag_ratio=0.25), run_time=1.0)
        hl = T("histones", 26, GREY).move_to([1.5, dna_y - 1.15, 0])
        self.at("histones")
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.5)

        tight = T("tightly packed", 26, GREY).move_to([1.5, dna_y - 1.15, 0])
        self.at("Tightly packed")
        self.play(ReplacementTransform(hl, tight), run_time=0.5)
        self.play(*[Wiggle(h, scale_value=1.05, rotation_angle=0.02 * TAU) for h in hist], run_time=0.7)

        enz = bchip("enzymes", PURPLE, 24, pad=0.16).move_to([1.5, 0.75, 0])
        link = Line(co.chip.get_right() + [0.02, 0, 0], enz.get_left() + [-0.02, 0.0, 0], color=PURPLE, stroke_width=6)
        self.at("brings enzymes")
        self.play(*glow(co.chip[1], co.chip[2], s=1.08, color=TEXT), Create(link), FadeIn(enz, shift=LEFT * 0.2), run_time=0.8)

        def ac():
            c = Circle(radius=0.24, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
            return VGroup(c, T("Ac", 22, BG, weight=BOLD).move_to(c))
        acs = [ac().move_to(enz.get_bottom() + [dx, -0.1, 0]) for dx in (-0.5, 0.0, 0.5)]
        ac_lbl = T("acetyl groups", 26, GOLD).next_to(enz, RIGHT, buff=0.4)
        self.at("acetyl groups")
        self.play(*[FadeIn(a, scale=0.5) for a in acs], FadeIn(ac_lbl, shift=RIGHT * 0.1), run_time=0.6)
        self.at("to histones")
        self.play(*[a.animate.move_to([x, dna_y + R + 0.3, 0]) for a, x in zip(acs, packed)], run_time=1.0)
        self.play(FadeOut(ac_lbl), run_time=0.3)

        loose = T("loosened", 26, GREEN).move_to([1.5, dna_y - 1.15, 0])
        self.at("loosens the packing")
        moves = []
        for h, a, p0, p1 in zip(hist, acs, packed, spread):
            moves += [h.animate.shift(RIGHT * (p1 - p0)), a.animate.shift(RIGHT * (p1 - p0))]
        self.play(*moves, ReplacementTransform(tight, loose), run_time=1.1)

        pol = bchip("RNA\npolymerase", TEXT, 22, pad=0.14).move_to([GX, dna_y + 1.7, 0])
        self.at("polymerase start")
        self.play(FadeIn(pol, shift=DOWN * 0.2), run_time=0.5)
        self.play(pol.animate.move_to([GX, dna_y + 0.95, 0]), run_time=0.5)

        self.at("Then the gene")
        self.play(gene.animate.set_fill(GREEN), gene_lbl.animate.set_color(GREEN), run_time=0.7)
        self.play(*glow(gene, s=1.12), run_time=0.5)

        # zoom in again (CLOSE)
        rec5 = Rec(K3, O3, "closed", "solid")
        co5 = coact(rec5, text=False, dy=0.85)
        carry = VGroup(rec.body, rec.pocket_fill, rec.groove_fill, rec.pocket_line, rec.groove_line, rec.lid, co.peg.cap, hd)
        out = [hinge, dbd, dna, stretch, gene, gene_lbl, pol, loose, enz, link, *acs, *hist, co.chip, co.stem]
        self.outro(*[FadeOut(m) for m in out],
                   then=[carry.animate.scale(K3 / K4, about_point=O4).shift(O3 - O4)],
                   after=[FadeIn(co5.chip), FadeIn(co5.stem), FadeOut(hd), FadeIn(hchip(rec5))])


# ---------------------------------------------------------------------------------------------
class S05Wrong(Film):
    """tamoxifen's side chain keeps the lid from closing; helix 12 lies in the groove instead. (CLOSE)"""

    def construct(self):
        rec = Rec(K3, O3, "closed", "solid")
        co = coact(rec, text=False, dy=0.85)
        hch = hchip(rec)
        self.add(*rec.layers(), hch, co)
        yt, k = rec.yt, rec.k

        # set the agonist picture aside: co-activator off, lid open, estradiol out
        self.at("An antagonist")
        self.play(co.animate.shift(UP * 1.7).set_opacity(0), run_time=0.6)
        self.play(Rotate(rec.lid, PI / 2, about_point=rec.P), hch.animate.shift(UP * 1.8).set_opacity(0),
                  FadeOut(rec.groove_line), FadeIn(rec.groove_dash), run_time=0.8)
        rec.groove = rec.groove_dash          # lid open: the groove is no longer complete

        anti = T("antagonist: occupies it without switching it on", 26, RED).move_to([O3[0], O3[1] - 1.5 * k + 0.45, 0])
        self.at("occupies the receptor")
        self.play(FadeIn(anti, shift=UP * 0.1), run_time=0.6)

        tc, ts = tam_parts(rec)
        tc.move_to([rec.pcx, yt + 1.3 * k, 0])
        lab = T("tamoxifen", 28, RED, weight=BOLD).next_to(tc, RIGHT, buff=0.3)
        self.at("liver converts")
        self.play(FadeIn(tc, scale=0.6), FadeIn(lab, shift=LEFT * 0.1), run_time=0.6)
        lab2 = T("4-hydroxytamoxifen", 28, RED, weight=BOLD).next_to(tc, RIGHT, buff=0.3)
        self.at("such as")
        self.play(ReplacementTransform(lab, lab2), *glow(tc, s=1.15, color=TEXT), run_time=0.8)

        self.at("That molecule")
        self.play(tc.animate.move_to([rec.pcx, yt - 1.0 * k, 0]), lab2.animate.move_to([rec.gcx, yt - 1.25 * k, 0]), run_time=0.9)

        side = T("side chain", 26, RED).next_to([rec.pcx + 0.25 * k, yt + 0.7 * k, 0], RIGHT, buff=0.15)
        self.at("one side chain")
        self.play(GrowFromEdge(ts, DOWN), run_time=0.8)
        self.play(FadeIn(side, shift=RIGHT * 0.1), FadeOut(lab2), run_time=0.4)
        self.at("too long")
        self.play(*glow(ts, s=1.12, color=TEXT), run_time=0.7)
        self.at("sticks out")
        self.play(pop(ts, 1.1), run_time=0.6)

        phi = float(np.arctan2(1.27, 1.0)) - 0.03
        tip = np.array([rec.pcx - 0.13 * k, yt + 1.0 * k, 0])
        self.at("lid should close")
        self.play(Rotate(rec.lid, -phi, about_point=rec.P), run_time=0.6)
        self.play(Flash(tip, color=RED, line_length=0.25, flash_radius=0.3, num_lines=8),
                  Rotate(rec.lid, 0.1, about_point=rec.P), run_time=0.3)
        self.play(Rotate(rec.lid, -0.1, about_point=rec.P), run_time=0.2)

        plab = T("helix 12 in the groove", 28, PINK, weight=BOLD).move_to([rec.gcx, yt - 0.95 * k, 0])
        self.at("Instead")
        self.play(FadeOut(side), Rotate(rec.lid, phi, about_point=rec.P), run_time=0.35)
        self.play(lid_flight(rec.lid, rec.lid_in_groove(), top=yt + 2.1 * k, run_time=1.3))
        self.play(FadeIn(plab, shift=UP * 0.1), *glow(rec.lid.edge, s=1.04, color=PINK), run_time=0.4)

        co2 = coact(rec, text=False, dy=0.85, raised=1.7)
        self.at("so the")
        self.play(FadeIn(co2, shift=DOWN * 0.2), run_time=0.4)
        self.play(co2.animate.shift(DOWN * (1.7 - 0.43 * k)), run_time=0.7)
        xm = VGroup(Line([rec.gcx - 0.3, yt + 0.5, 0], [rec.gcx + 0.3, yt - 0.1, 0]),
                    Line([rec.gcx - 0.3, yt - 0.1, 0], [rec.gcx + 0.3, yt + 0.5, 0])).set_color(RED).set_stroke(width=8)
        taken = T("groove taken", 28, RED, weight=BOLD).move_to([rec.gcx, yt - 0.95 * k, 0])
        self.at("nowhere to bind")
        self.play(Create(xm), ReplacementTransform(plab, taken), run_time=0.5)
        self.play(co2.animate.shift(UP * 0.7), run_time=0.5)

        # hand over to scene 6: shrink the finished picture into the first column
        core = VGroup(*rec.layers(), tc, ts)
        self.outro(FadeOut(co2), FadeOut(xm), FadeOut(anti), FadeOut(taken),
                   then=[core.animate.scale(K6 / K3, about_point=O3).shift(np.array([COLS[0], COL_Y, 0.0]) - O3)])


# ---------------------------------------------------------------------------------------------
class S06Rule(Film):
    """the same drug in breast and uterus; the helper proteins differ in kind; the rule: where helix 12 lies decides if the groove is free."""

    def construct(self):
        cols = COLS
        Oc = lambda x: np.array([x, COL_Y, 0.0])
        core, rec1 = tam_core(K6, Oc(cols[0]))
        self.add(core)
        c2 = core.copy().shift(RIGHT * (cols[1] - cols[0]))
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)

        def tissue(name, x):
            return bchip(name, TEXT, 28, pad=0.16).move_to([x, 3.0, 0])
        t1, t3 = tissue("breast", cols[0]), tissue("uterus", cols[1])
        v1 = T("blocks estrogen", 26, RED, weight=BOLD).move_to([cols[0], 2.4, 0])
        v3 = T("imitates estrogen", 26, GREEN, weight=BOLD).move_to([cols[1], 2.4, 0])

        self.at("blocks estrogen")
        self.play(FadeIn(t1, shift=DOWN * 0.1), FadeIn(v1, shift=DOWN * 0.1), run_time=0.7)
        self.at("imitates")
        self.play(FadeIn(t3, shift=DOWN * 0.1), FadeIn(v3, shift=DOWN * 0.1), run_time=0.7)

        # each copy stands on its DNA
        extras = []
        for x in cols:
            r = Rec(K6, Oc(x))
            hinge, dbd, dna_y, stretch = chain_parts(r)
            dna = Line([x - 2.4, dna_y, 0], [x + 2.4, dna_y, 0], color=GREY, stroke_width=6)
            extras.append(VGroup(dna, hinge, dbd, stretch))
        dna_lbl = T("DNA", 24, GREY).move_to([0, dna_y, 0])
        self.at("still binds")
        self.play(*[FadeIn(e, shift=UP * 0.1) for e in extras], FadeIn(dna_lbl), run_time=0.9)

        # helper proteins differ in kind (shape), not in number
        def square(x, y):
            return Square(side_length=0.3, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to([x, y, 0])

        def disc(x, y):
            return Dot([x, y, 0], radius=0.17, color=PURPLE)
        offs = [(-0.45, 0.0), (0.45, 0.0), (0.0, 0.45)]
        clusters = [VGroup(*[square(cols[0] + px, -2.65 + py) for px, py in offs]),
                    VGroup(*[disc(cols[1] + px, -2.65 + py) for px, py in offs])]
        arrows = [arr([x, -2.15, 0], [x, dna_y - 0.12, 0], PURPLE, w=4, tip=0.16) for x in cols]
        help_lbl = T("helper proteins differ by tissue", 26, PURPLE).move_to([0, -3.3, 0])
        self.at("helper proteins")
        self.play(*[FadeIn(c, shift=UP * 0.1) for c in clusters], FadeIn(help_lbl), *[GrowArrow(a) for a in arrows], run_time=0.9)
        self.at("each tissue")
        self.play(*[Indicate(c, color=TEXT, scale_factor=1.15) for c in clusters], run_time=0.8)

        # the rule: two receptors side by side
        RK, OL, OR = 0.8, np.array([-3.3, -0.2, 0]), np.array([3.3, -0.2, 0])
        recL = Rec(RK, OL, "closed", "solid")
        hdL = hdot(recL)
        coL = coact(recL, text=False, dy=0.8)
        coreR, recR = tam_core(RK, OR)
        coR = coact(recR, text=False, dy=0.8)
        coR.shift(UP * 0.43 * RK)          # its helix rests on top of helix 12: the groove is taken
        xm = VGroup(Line([recR.gcx - 0.25, recR.yt + 0.45, 0], [recR.gcx + 0.25, recR.yt - 0.05, 0]),
                    Line([recR.gcx - 0.25, recR.yt - 0.05, 0], [recR.gcx + 0.25, recR.yt + 0.45, 0])).set_color(RED).set_stroke(width=7)
        pL = T("helix 12", 26, PINK, weight=BOLD).move_to(recL.lid_label_closed())
        pR = T("helix 12", 26, PINK, weight=BOLD).move_to([recR.gcx, recR.yt - 0.9 * RK, 0])
        free = T("groove free", 32, GREEN, weight=BOLD).move_to([OL[0], -2.05, 0])
        taken = T("groove taken", 32, RED, weight=BOLD).move_to([OR[0], -2.05, 0])
        everything = VGroup(core, c2, t1, t3, v1, v3, dna_lbl, *extras, *clusters, *arrows, help_lbl)
        self.at("Keep this rule")
        self.play(FadeOut(everything), run_time=0.4)
        self.play(FadeIn(VGroup(*recL.layers(), hdL)), FadeIn(coreR), FadeIn(pL), FadeIn(pR), run_time=0.5)
        self.at("where helix")
        self.play(*glow(recL.lid.edge, s=1.06, color=TEXT), *glow(recR.lid.edge, s=1.06, color=TEXT), run_time=0.7)
        self.at("whether the groove is free")
        self.play(FadeIn(coL, shift=DOWN * 0.2), FadeIn(free, shift=UP * 0.1), run_time=0.7)
        self.at("for a")
        self.play(FadeIn(coR, shift=DOWN * 0.2), FadeIn(taken, shift=UP * 0.1), Create(xm), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Where helix 12 lies decides whether the groove is free."
