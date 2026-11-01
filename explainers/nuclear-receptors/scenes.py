"""Nuclear receptors: the receptor is the gene switch  (Biochemistrypedia explainer)

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

The retained close-up helpers below preserve the original film's drawing vocabulary.
This overview uses the pocket, hinge and DNA grip; it does not show helix 12.
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


# Overview framing reuses the old pocket, hinge, DNA grip, histones and opaque chips.
# Helix 12 and its groove are intentionally outside this film's overview.
def receptor(k, x, y, bound=False):
    r = Rec(k, [x, y, 0], 'closed', 'solid')
    hinge, dbd, dy, stretch = chain_parts(r)
    g = VGroup(r.body, r.pocket_fill, r.pocket_line, hinge, dbd)
    if bound:
        g.add(hdot(r))
    return g, r, dy, stretch


def dna_line(y, x=0, width=11.8):
    return Line([x-width/2, y, 0], [x+width/2, y, 0], color=GREY, stroke_width=6)


def pool(x, y, kind=0):
    shapes = VGroup()
    for dx, dy in [(-0.45, 0), (0.45, 0), (0, 0.45)]:
        m = (Square(side_length=0.28, fill_color=PURPLE, fill_opacity=0.8, stroke_width=2)
             if kind == 0 else Circle(radius=0.16, fill_color=PURPLE, fill_opacity=0.8, stroke_width=2) if kind == 1
             else Triangle(fill_color=PURPLE, fill_opacity=0.8, stroke_width=2).scale(0.18))
        shapes.add(m.set_color(PURPLE).move_to([x+dx, y+dy, 0]))
    return shapes


class S00Title(TitleCard):
    LESSON = 'Nuclear receptors'
    TITLE = 'The Receptor Is the Gene Switch'


class S01Catch(SpokenScene):
    def construct(self):
        cell = big_cell()
        rec, r, dy, stretch = receptor(0.48, -2.7, -0.2)
        label = T('intracellular receptor', 28, BLUE).move_to([-2.7, -2.4, 0])
        h = hdot(r).move_to([-4.8, 0.55, 0])
        self.at('Nuclear receptors')
        self.play(FadeIn(cell), FadeIn(rec), FadeIn(label), run_time=0.6)
        self.at('catch chemical signals')
        self.play(FadeIn(h), run_time=0.2)
        self.play(h.animate.move_to(hdot(r)), run_time=0.6)
        nucleus = VGroup(RoundedRectangle(width=6, height=3.6, corner_radius=0.4, color=GREY).move_to([2.5, -0.6, 0]),
                         T('nucleus', 24, GREY).move_to([4.5, 0.85, 0]))
        dna = dna_line(dy, 2.6, 5.1)
        genes = VGroup(*[gene_block(x, dy, 0.65) for x in [1, 2.6, 4.2]])
        self.at('control whether genes')
        self.play(FadeOut(label), FadeIn(nucleus), FadeIn(dna), FadeIn(genes),
                  rec.animate.shift(RIGHT*4.2), h.animate.shift(RIGHT*4.2), run_time=0.7)
        tf = T('receptor = transcription factor', 30, BLUE).move_to([0, 2.7, 0])
        self.at('receptor itself')
        self.play(FadeIn(tf), Indicate(rec, color=BLUE), run_time=0.6)
        rnas = VGroup(*[bchip('RNA', GREEN, 22, pad=0.12).move_to([x, -2.45, 0]) for x in [1, 2.6, 4.2]])
        self.at('many genes at once')
        self.play(*[Indicate(g, color=GREEN) for g in genes], FadeIn(rnas, shift=UP*0.15), run_time=0.7)
        proteins = VGroup(*[bchip('protein', GREEN, 22, pad=0.12).move_to([x, -3.15, 0]) for x in [1, 2.6, 4.2]])
        self.at('protein take time')
        self.play(FadeIn(proteins, shift=DOWN*0.15), run_time=0.6)
        timeline = VGroup(arr([-5.4, -2.7, 0], [-0.5, -2.7, 0], GREY),
                          T('hours', 26, TEXT).move_to([-3, -3.2, 0]))
        marker = Dot([-5.2, -2.7, 0], color=GREEN)
        self.at('builds over hours')
        self.play(FadeIn(timeline), FadeIn(marker), run_time=0.3)
        self.play(marker.animate.shift(RIGHT*4.2), run_time=1.1)
        self.at('after the hormone has gone')
        self.play(FadeOut(h), Indicate(proteins, color=GREEN), run_time=0.7)
        # The last sentence returns to the membrane entry step, as narrated.
        entry, er, _, _ = receptor(0.48, -2.7, -0.2)
        hormone = hdot(er).move_to([er.pcx, 2.5, 0])
        tag = T('steroid hormone', 26, YELLOW).move_to([0.2, 2.5, 0])
        self.at('A steroid hormone')
        self.play(FadeOut(VGroup(nucleus, dna, genes, rnas, proteins, timeline, marker, tf, rec)),
                  FadeIn(entry), FadeIn(hormone), FadeIn(tag), run_time=0.5)
        self.at('crosses the membrane')
        self.play(hormone.animate.move_to(hdot(er)), run_time=1.0)
        self.finish()


class S02Chain(SpokenScene):
    def construct(self):
        rec, r, dy, stretch = receptor(0.72, -2.6, 1.05)
        self.at('The receptor')
        self.play(FadeIn(rec), run_time=0.6)
        labels = VGroup(T('hormone-binding domain', 26, BLUE).move_to([3.3, 1.1, 0]),
                        T('hinge', 26, BLUE).move_to([3.3, -0.15, 0]),
                        T('DNA-binding domain', 26, BLUE).move_to([3.3, -0.9, 0]))
        links = VGroup(*[arr([1.1, y, 0], [x, y, 0], BLUE, w=3) for x,y in [(-0.1,1.1),(-2.3,-0.15),(-1.3,-0.9)]])
        self.at('one chain with two grips')
        self.play(FadeIn(labels[1]), GrowArrow(links[1]), run_time=0.5)
        h = hdot(r).shift(UP*1.7)
        self.at('One region binds')
        self.play(FadeIn(labels[0]), GrowArrow(links[0]), FadeIn(h), run_time=0.4)
        self.play(h.animate.move_to(hdot(r)), run_time=0.6)
        dna = dna_line(dy)
        self.at('Another recognizes')
        self.play(FadeIn(labels[2]), GrowArrow(links[2]), Create(dna), Create(stretch), run_time=0.7)
        self.at('work in pairs')
        self.play(FadeOut(VGroup(rec, h, labels, links, dna, stretch)), run_time=0.3)
        pair = VGroup()
        for x in [-1.35, 1.35]:
            g, _, yy, ss = receptor(0.34, x, 0.4)
            pair.add(g, ss)
        line = dna_line(yy)
        response = T('response element', 28, TEXT).move_to([0, -1.6, 0])
        self.play(FadeIn(pair), Create(line), run_time=0.6)
        self.at('called a response element')
        self.play(FadeIn(response), run_time=0.6)
        title = T('glucocorticoid receptor + same receptor', 30, BLUE).move_to([0, 2.7, 0])
        self.at('The glucocorticoid receptor')
        self.play(FadeIn(title), pair[2].animate.shift(RIGHT*1.6), run_time=0.5)
        self.at('after hormone arrives')
        hormones = VGroup(*[Dot([x-0.48, 0.57, 0], radius=0.14, color=YELLOW) for x in [-1.35, 1.35]])
        self.play(FadeIn(hormones), pair[2].animate.shift(LEFT*1.6), run_time=0.7)
        thyroid = T('thyroid hormone receptor + RXR', 30, BLUE).move_to(title)
        names = VGroup(T('thyroid receptor', 24, BLUE).move_to([-2.4, 1.6, 0]),
                       T('RXR', 24, BLUE).move_to([2.4, 1.6, 0]))
        self.at('The thyroid hormone receptor')
        self.play(FadeOut(hormones), ReplacementTransform(title, thyroid), FadeIn(names), run_time=0.7)
        self.at('different partner')
        self.play(Indicate(pair[2], color=BLUE), run_time=0.6)
        jobs = T('hormone recognition  •  DNA recognition\nTwo jobs in the same protein', 28, TEXT).move_to([0, -2.7, 0])
        self.at('Hormone recognition')
        self.play(FadeIn(jobs), Indicate(pair, color=BLUE), run_time=0.8)
        self.finish()


class S04Loosen(SpokenScene):
    def construct(self):
        pair = VGroup()
        for x in [-1.35,1.35]:
            g, _, yy, ss = receptor(0.34, x, 0.4)
            pair.add(g, ss)
        dna = dna_line(yy)
        names = T('thyroid hormone receptor + RXR', 30, BLUE).move_to([0,2.7,0])
        helper = bchip('co-repressor', PURPLE, 26).move_to([0,1.8,0])
        self.add(pair, dna, names, helper)
        h = Dot([-3.5,1.5,0], radius=0.16,color=YELLOW)
        self.at('Hormone binding')
        self.play(FadeIn(h), run_time=0.2)
        self.play(h.animate.move_to([-1.82,0.57,0]), pair[0][0].animate.stretch(1.08,0), run_time=0.7)
        self.at('releases a correpressor')
        self.play(helper.animate.shift(UP*0.5).set_opacity(0), run_time=0.6)
        active = bchip('co-activator', PURPLE, 26).move_to([0,1.8,0])
        self.at('brings in a coactivator')
        self.play(FadeIn(active, shift=DOWN*0.25), run_time=0.6)
        # Reuse the old histone discs with DNA wound around them.
        hist = VGroup(*[VGroup(Circle(radius=0.55, stroke_width=0,fill_color=GREY,fill_opacity=0.55),
                              Circle(radius=0.65,color=GREY,stroke_width=7)).move_to([x,-0.65,0]) for x in [-1.15,0,1.15]])
        chrom = T('chromatin: DNA around histones',26,GREY).move_to([0,-2.1,0])
        self.at('act on chromatin')
        self.play(FadeOut(VGroup(pair,dna,names,h)), active.animate.move_to([-3.8,2.5,0]),
                  FadeIn(hist),FadeIn(chrom), run_time=0.7)
        line = dna_line(-0.65)
        self.add(line.set_z_index(-3))
        enzyme = bchip('enzymes',PURPLE,26).move_to([0,2.5,0])
        link = arr(active.get_right(),enzyme.get_left(),PURPLE)
        self.at('bring enzymes')
        self.play(GrowArrow(link),FadeIn(enzyme),run_time=0.6)
        acs=VGroup()
        for x in [-1.15,0,1.15]:
            c=Circle(radius=0.25,color=GOLD,fill_color=GOLD,fill_opacity=1)
            acs.add(VGroup(c,T('Ac',22,BG).move_to(c)).move_to([x,1.3,0]))
        self.at('add acetyl groups')
        self.play(FadeIn(acs),run_time=0.4)
        self.at('to histones')
        self.play(*[a.animate.move_to([x,0.2,0]) for a,x in zip(acs,[-1.15,0,1.15])],run_time=0.7)
        loose=T('looser packing',28,GREEN).move_to(chrom)
        self.at('loosens the packing')
        self.play(*[m.animate.shift(RIGHT*d) for m,d in zip(hist,[-1.2,0,1.2])],
                  *[m.animate.shift(RIGHT*d) for m,d in zip(acs,[-1.2,0,1.2])],ReplacementTransform(chrom,loose),run_time=0.8)
        pol=bchip('RNA polymerase',TEXT,24).move_to([4.2,0.3,0])
        rna=bchip('RNA',GREEN,24).move_to([4.4,-1.6,0])
        self.at('polymerase start')
        self.play(FadeIn(pol,shift=DOWN*0.3),FadeIn(rna,shift=DOWN*0.2),run_time=0.7)
        # Clear the active case before the separate removal comparison.
        rep=bchip('co-repressor + enzymes',PURPLE,26).move_to([0,2.5,0])
        comp=T('separate comparison: acetyl removal',26,TEXT).move_to([0,3.35,0])
        self.at('Correpressors bring enzymes')
        self.play(FadeOut(VGroup(active,enzyme,link,pol,rna,loose)),FadeIn(rep),FadeIn(comp),run_time=0.5)
        self.at('remove those groups')
        self.play(acs.animate.shift(UP*1.2),run_time=0.6)
        self.play(FadeOut(acs),run_time=0.3)
        cells=VGroup(*[VGroup(RoundedRectangle(width=4,height=3,corner_radius=0.4,color=GREY).move_to([x,-0.3,0]),
                              pool(x,-0.4,i),T('cell '+str(i+1),26,GREY).move_to([x,-2.3,0])) for i,x in enumerate([-3.2,3.2])])
        helpers=T('Different cellular helper pools',30,PURPLE).move_to([0,2.6,0])
        self.at('own mix')
        self.play(FadeOut(VGroup(hist,line,rep,comp)),FadeIn(cells),FadeIn(helpers),run_time=0.7)
        self.finish()


class S08Lipids(SpokenScene):
    def construct(self):
        title=T('Signals from the cell’s own lipids',34,font=TITLE_FONT).move_to([0,3,0])
        rows=[]
        for y,lig,name in [(1.6,'fatty acids','PPARs'),(0,'oxidized cholesterol','LXR'),(-1.6,'bile acids','FXR')]:
            l=bchip(lig,YELLOW,26).move_to([-3.6,y,0])
            rec,r,dy,ss=receptor(0.21,0,y+0.15)
            lab=T(name,30,BLUE).move_to([1.9,y+0.45,0])
            dna=VGroup(dna_line(y,4.4,2.5),gene_block(4.4,y,0.9),T('DNA',22,GREY).move_to([4.4,y-0.5,0]))
            a=arr(l.get_right(),[-1,y,0],YELLOW)
            b=arr([1,y,0],[2.9,y,0],BLUE)
            rows.append(VGroup(l,rec,lab,dna,a,b))
        self.at('the family reaches')
        self.play(FadeIn(title),FadeIn(rows[0]),run_time=0.6)
        self.at('ppars bind fatty acids')
        self.play(Indicate(rows[0],scale_factor=1.03),run_time=0.7)
        self.at('lxr binds oxidized cholesterol')
        self.play(FadeIn(rows[1]),run_time=0.7)
        self.at('fxr binds bile acids')
        self.play(FadeIn(rows[2]),run_time=0.7)
        gamma=T('PPAR-γ',30,BLUE).move_to([0,2.5,0])
        route=rows[0].copy().shift(DOWN*1.1)
        route[2].become(T('PPAR-γ',30,BLUE).move_to(route[2]))
        cell=Circle(radius=0.55,color=GREY).move_to([-1.8,-1.7,0])
        fat=VGroup(Circle(radius=0.9,color=GREY),Circle(radius=0.65,color=YELLOW,fill_color=YELLOW,fill_opacity=0.25)).move_to([2.5,-1.7,0])
        change=arr([-0.9,-1.7,0],[1.3,-1.7,0],GREEN)
        fatlabel=T('fat cell',28,TEXT).move_to([2.5,-3,0])
        self.at('ppar gamma drives')
        self.play(FadeOut(VGroup(*rows,title)),FadeIn(route),FadeIn(gamma),FadeIn(cell),run_time=0.5)
        self.at('making of fat cells')
        self.play(GrowArrow(change),TransformFromCopy(cell,fat),FadeIn(fatlabel),run_time=0.8)
        rule=T('intracellular signal → gene control',30,TEXT).move_to([0,3.3,0])
        self.at('an intracellular signal')
        self.play(ReplacementTransform(gamma,rule),Indicate(route,color=BLUE),run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        opening_rec, _, opening_y, opening_stretch = receptor(0.45,0,0.4,True)
        opening = VGroup(opening_rec,dna_line(opening_y),opening_stretch,
                         T('intracellular signal → gene control',30,TEXT).move_to([0,3.3,0]))
        self.add(opening)
        drugs=VGroup(bchip('prednisone',YELLOW,28),bchip('dexamethasone',YELLOW,28)).arrange(RIGHT,buff=0.6).move_to([0,2.7,0])
        gr=bchip('glucocorticoid receptor',BLUE,30).move_to([0,1.1,0])
        arrows=VGroup(*[arr(d.get_bottom(),gr.get_top(),YELLOW) for d in drugs])
        benefit=T('reduced inflammation',30,GREEN).move_to([0,-0.3,0])
        self.at('Prednisone and dexamethasone')
        self.play(FadeOut(opening),FadeIn(drugs),run_time=0.5)
        self.at('through the glucocorticoid receptor')
        self.play(FadeIn(gr),FadeIn(arrows),run_time=0.6)
        self.at('calm inflammation')
        self.play(FadeIn(benefit),run_time=0.6)
        long=VGroup(T('long treatment',26,GREY).move_to([0,-1.5,0]),
                    arr([-3.4,0.7,0],[-3.4,-1.8,0],GREY),arr([3.4,0.7,0],[3.4,-1.8,0],GREY))
        effects=VGroup(T('raised blood glucose',26,RED).move_to([-3,-2.5,0]),T('thinner bone',26,RED).move_to([3,-2.5,0]))
        self.at('Long treatment')
        self.play(FadeIn(long),run_time=0.4)
        self.at('raises blood glucose')
        self.play(FadeIn(effects[0]),run_time=0.5)
        self.at('thins bone')
        self.play(FadeIn(effects[1]),run_time=0.5)
        tam=bchip('tamoxifen',RED,28).move_to([0,3.15,0])
        self.at('Tissue context')
        self.play(FadeOut(VGroup(drugs,gr,arrows,benefit,long,effects)),run_time=0.4)
        columns=VGroup()
        for x,name in [(-4.3,'breast'),(0,'uterus'),(4.3,'bone\nafter menopause')]:
            rec,r,dy,ss=receptor(0.28,x,0.1,False)
            dot=hdot(r).set_color(RED)
            line=dna_line(dy,x,3.5)
            columns.add(VGroup(rec,dot,line,ss,T(name,26,TEXT).move_to([x,2,0])))
        self.at('Tamoxifen')
        self.play(FadeIn(tam),FadeIn(columns),run_time=0.6)
        block=T('blocks estrogen',24,RED).move_to([-4.3,-1.7,0])
        mimics=VGroup(*[T('imitates estrogen',24,GREEN).move_to([x,-1.7,0]) for x in [0,4.3]])
        self.at('blocks estrogen')
        self.play(FadeIn(block),run_time=0.4)
        self.at('imitates it')
        self.play(FadeIn(mimics[0]),run_time=0.4)
        self.at('after menopause')
        self.play(FadeIn(mimics[1]),run_time=0.4)
        self.at('still binds DNA')
        self.play(*[Indicate(c[2],color=TEXT) for c in columns],run_time=0.6)
        af=VGroup(*[bchip('AF-1',BLUE,22,pad=0.12).move_to([x+0.6,0.95,0]) for x in [-4.3,0,4.3]])
        self.at('switching surface')
        self.play(FadeIn(af),run_time=0.5)
        self.at('can still work')
        self.play(Indicate(af,color=BLUE),run_time=0.6)
        pools=VGroup(*[pool(x,-2.8,i) for i,x in enumerate([-4.3,0,4.3])])
        maybe=T('Helper pools can help explain the difference',26,PURPLE).move_to([0,-3.5,0])
        self.at('can depend on')
        self.play(FadeIn(pools),FadeIn(maybe),run_time=0.7)
        signal=bchip('signal',YELLOW,28).move_to([-4.7,1.8,0])
        rec,r,dy,ss=receptor(0.45,0,0.4,True)
        dna=VGroup(dna_line(dy),ss,T('receptor on DNA',26,BLUE).move_to([0,-1.8,0]))
        helpers=bchip('cellular helpers',PURPLE,28).move_to([4.3,1.8,0])
        links=VGroup(arr(signal.get_right(),[-1.6,0.8,0],YELLOW),arr(helpers.get_left(),[1.6,0.8,0],PURPLE))
        self.at('The signal')
        self.play(FadeOut(VGroup(tam,columns,block,mimics,af,pools,maybe)),FadeIn(signal),FadeIn(rec),FadeIn(dna),run_time=0.5)
        self.at('cells helpers together')
        self.play(FadeIn(helpers),FadeIn(links),run_time=0.5)
        out=bchip('gene transcription',GREEN,30).move_to([0,-2.9,0])
        self.at('shape gene control')
        self.play(FadeIn(out,shift=DOWN*0.15),run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = 'The receptor itself controls gene transcription.'
