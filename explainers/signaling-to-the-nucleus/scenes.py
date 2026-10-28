"""Signaling to the Nucleus: one phosphate flips a waiting factor  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the signal: growth factor, cAMP, calcium and calmodulin (what reaches the cell)
  TEAL   = CREB, the transcription factor that is already made and already on the DNA
  PURPLE = the kinases that act on CREB (PKA, CaMKIV, the kinases ERK switches on)
  GOLD   = a phosphate (the round "P" badge), and the "handle" it makes
  ORANGE = CBP, the co-activator, and the acetyl groups (Ac) it adds
  PINK   = KIX, the grip on CBP that closes on the phosphate
  BLUE   = the transcription machinery and RNA polymerase
  GREEN  = on (the gene switched on)
  RED    = blocked or ruled out (the drug, the ribosomes it stops, CBP's missing DNA grip)
  GREY   = membrane, nucleus, DNA, histones, labels, things not yet known or not in play

No molecular structures: CREB is two labelled lobes with a stalk, a kinase is a labelled blob, KIX is
a cup that closes on the phosphate, histones are beads, DNA is a line and a gene is a block on it.

One stage for the whole film (membrane on top, a thin cytoplasm strip, then a large nucleus). The
nucleus fills about two thirds of the frame, because the action is on the DNA and just above it.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F2994A"

MEM_Y, MEM_H = 2.6, 0.28            # the cell membrane
STRIP = 2.05                        # height of the cytoplasm strip, where messengers and kinases wait
NUC_TOP, NUC_BOT = 1.5, -3.5        # the nucleus
DNA_Y = -2.65
GX0, GX1, GH = 1.8, 5.6, 0.5        # the c-fos gene: a block on the DNA
GXC = (GX0 + GX1) / 2
CX, CREB_Y = -0.9, -1.95            # CREB sits on its site in front of the gene
LOBE_W, LOBE_H = 1.45, 1.25
CREB_XS = (CX - 0.76, CX + 0.76)    # the two CREB lobes
TIPS = [np.array([x, -0.5, 0]) for x in CREB_XS]   # the serine at the end of each CREB's stalk
TIP = TIPS[1]                       # the serine that KIX grips
PKA_POS = np.array([-3.4, 0.9, 0])     # where the freed PKA waits in the nucleus
BAR_Y = 0.05                        # the bar that gathers inputs for the serine on each CREB


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24):
    """a dashed grey chip: something that is NOT in play."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def dashed_arrow(a, b, color=YELLOW, w=5, dash=0.15):
    """an arrow with a dashed shaft: a path of several steps that the film does not show."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    line = DashedLine(a, b - d * 0.1, color=color, stroke_width=w, dash_length=dash)
    tipm = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.15).rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(b - d * 0.1)
    return VGroup(line, tipm)


def pbadge():
    """a phosphate."""
    c = Circle(radius=0.3, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 30, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    """swell and settle, without recolouring."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation per mobject)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def clock(center, r=0.6):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.15) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.2), color=TEXT, stroke_width=6)
    pin = Dot(center, radius=0.07, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def sig(text):
    """a chip for a signal."""
    return bchip(text, YELLOW, 24)


def kin(text, c):
    """a chip for a kinase."""
    return bchip(text, PURPLE, 26).move_to(c)


# ---------------------------------------------------------------------------------------------
# the stage
# ---------------------------------------------------------------------------------------------
def membrane():
    return RoundedRectangle(corner_radius=0.1, width=12.6, height=MEM_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, MEM_Y, 0])


def on_membrane(ch):
    return ch.next_to([0, MEM_Y + MEM_H / 2, 0], UP, buff=0.08)


def nucleus():
    """nucleus, DNA and the c-fos gene (grey: off). The gene's label is separate."""
    env = RoundedRectangle(corner_radius=0.5, width=12.4, height=NUC_TOP - NUC_BOT, stroke_color=GREY,
                           stroke_width=3).move_to([0, (NUC_TOP + NUC_BOT) / 2, 0])
    dna = Line([-5.7, DNA_Y, 0], [5.7, DNA_Y, 0], color=GREY, stroke_width=6)
    gene = Rectangle(width=GX1 - GX0, height=GH, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([GXC, DNA_Y, 0])
    nuc_lbl = T("nucleus", 24, GREY).move_to([5.1, DNA_Y - 0.6, 0])
    dna_lbl = T("DNA", 24, GREY).move_to([-5.15, DNA_Y - 0.55, 0])
    g = VGroup(env, dna, gene, nuc_lbl, dna_lbl)
    g.gene = gene
    return g


def gene_label():
    """the gene's name, on the gene block."""
    return T("c-fos", 26, BG, weight=BOLD).move_to([GXC, DNA_Y, 0])


def gene_arrow():
    """the gene being read: an arrow running along it."""
    return Arrow([GX0 + 0.2, DNA_Y + 0.5, 0], [GX1 - 0.2, DNA_Y + 0.5, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.45)


def site_line():
    """the short stretch of DNA that CREB binds."""
    return Line([CX - 1.5, DNA_Y, 0], [CX + 1.5, DNA_Y, 0], color=TEXT, stroke_width=12)


def creb():
    """CREB: a pair (two lobes, one label on each). .lobes, .labels"""
    lobes = [RoundedRectangle(corner_radius=0.35, width=LOBE_W, height=LOBE_H, stroke_color=TEAL, stroke_width=3,
                              fill_color=TEAL, fill_opacity=0.28).move_to([CX + dx, CREB_Y, 0]) for dx in (-0.76, 0.76)]
    labels = [T("CREB", 28, TEAL, weight=BOLD).move_to(lb) for lb in lobes]
    g = VGroup(*lobes, *labels)
    g.lobes, g.labels = lobes, labels
    return g


def stalk():
    """a stalk on each CREB, carrying its serine and ending in a dot. .lines, .dots"""
    lines = [Line([t[0], CREB_Y + LOBE_H / 2, 0], t, color=TEAL, stroke_width=8) for t in TIPS]
    dots = [Dot(t, radius=0.14, color=TEAL) for t in TIPS]
    g = VGroup(*lines, *dots)
    g.lines, g.dots = lines, dots
    return g


def serine_bar():
    """a bracket over both serines: what a kinase's arrow ends on, so it reaches the serine on each CREB."""
    x0, x1 = TIPS[0][0], TIPS[1][0]
    kw = dict(color=TEAL, stroke_width=5)
    leg = TIPS[0][1] + 0.15            # the legs reach down to the serines
    return VGroup(Line([x0, BAR_Y, 0], [x1, BAR_Y, 0], **kw), Line([x0, BAR_Y, 0], [x0, leg, 0], **kw),
                  Line([x1, BAR_Y, 0], [x1, leg, 0], **kw))


def bar_pt(f):
    """a point on top of the bar: f=0 over the left serine, f=1 over the right one."""
    return np.array([TIPS[0][0] + f * (TIPS[1][0] - TIPS[0][0]), BAR_Y + 0.08, 0])


def question_box():
    """a dashed box with a question mark, on the DNA where the unknown factor must be."""
    shape = RoundedRectangle(corner_radius=0.2, width=3.1, height=LOBE_H)
    back = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to([CX, CREB_Y, 0])
    edge = DashedVMobject(shape.copy().move_to([CX, CREB_Y, 0]), num_dashes=34).set_color(GREY)
    q = T("?", 56, TEXT, weight=BOLD).move_to([CX, CREB_Y, 0])
    return VGroup(back, edge, q)


def pka_blob(c):
    """PKA in the cytoplasm: a body with two small pieces (the catalytic subunits) on it."""
    c = np.array(c, float)
    back = RoundedRectangle(corner_radius=0.3, width=1.5, height=0.8, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    body = RoundedRectangle(corner_radius=0.3, width=1.5, height=0.8, stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.3).move_to(c)
    lbl = T("PKA", 28, PURPLE, weight=BOLD).move_to(c)
    mk = lambda dy: Circle(radius=0.2, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8).move_to(c + [0.72, dy, 0])
    return VGroup(back, body, lbl), mk(0.2), mk(-0.2)


def cup(center, tight=False):
    """KIX: a cup on CBP that opens downward and closes on the phosphate."""
    if tight:
        a = AnnularSector(inner_radius=0.34, outer_radius=0.58, angle=320 * DEGREES, start_angle=-70 * DEGREES,
                          color=PINK, fill_opacity=1, stroke_width=0)
    else:
        a = AnnularSector(inner_radius=0.42, outer_radius=0.6, angle=200 * DEGREES, start_angle=-10 * DEGREES,
                          color=PINK, fill_opacity=1, stroke_width=0)
    return a.shift(np.array(center, float))


CBP_W, CBP_H = 3.2, 1.2
CUP_DX, CUP_DY = -0.8, -1.18        # where KIX sits on CBP, from the centre of the blob


def cbp(c, text="co-activator"):
    """the co-activator: [back, body, label]."""
    c = np.array(c, float)
    back = RoundedRectangle(corner_radius=0.35, width=CBP_W, height=CBP_H, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    body = RoundedRectangle(corner_radius=0.35, width=CBP_W, height=CBP_H, stroke_color=ORANGE, stroke_width=3,
                            fill_color=ORANGE, fill_opacity=0.22).move_to(c)
    lbl = T(text, 30, ORANGE, weight=BOLD).move_to(c)
    return VGroup(back, body, lbl)


def ac_badge():
    c = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=1)
    return VGroup(c, T("Ac", 26, BG, weight=BOLD).move_to(c))


BEAD_Y = DNA_Y + GH / 2 + 0.42      # histone beads sit on top of the gene
BEAD_X = (3.1, 3.94, 4.78)          # packed; they loosen to BEAD_X shifted by BEAD_LOOSEN
BEAD_LOOSEN = (0.0, 0.4, 0.8)


def bead(x):
    return Circle(radius=0.42, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.7).move_to([x, BEAD_Y, 0])


def drug_block():
    """the drug, and the ribosomes it stops, in the cytoplasm strip. -> drug, bar, ribosomes, cross"""
    drug = T("drug", 28, RED, weight=BOLD).move_to([-5.2, STRIP, 0])
    bar = inhib([-4.6, STRIP, 0], [-4.05, STRIP, 0])
    rib = bchip("ribosomes", GREY, 26).move_to([-2.85, STRIP, 0])
    cross = strike(rib)
    rib[1].set_stroke(opacity=0.6).set_fill(opacity=0.08)
    rib[2].set_opacity(0.7)
    return drug, bar, rib, cross


class Film(SpokenScene):
    def outro(self, *anims, run_time=0.5):
        """hold until the narration ends, then clear what the next scene does not inherit."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Signaling to the Nucleus"
    TITLE = "One phosphate changes a waiting factor"


def glow_gene(nuc, s=1.1):
    return Indicate(nuc.gene, color=TEXT, scale_factor=s)


def bigx(center, size=0.26, w=9):
    """a red cross: this does not happen."""
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=RED, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=RED, stroke_width=w))


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """a growth factor switches on c-fos in minutes, even with ribosomes stopped: something was waiting."""

    def construct(self):
        mem, nuc, gl = membrane(), nucleus(), gene_label()
        self.play(FadeIn(mem), FadeIn(nuc), run_time=0.3)
        gf = on_membrane(sig("growth factor"))
        self.at("growth factor")
        self.play(FadeIn(gf, shift=DOWN * 0.35), run_time=0.5)

        ck = clock([3.7, 0.55, 0])
        mins = T("minutes", 28, GREY).move_to([3.7, -0.4, 0])
        self.at("within minutes")
        self.play(FadeIn(ck), FadeIn(mins), run_time=0.3)
        self.play(Rotate(ck.hand, -TAU / 5, about_point=ck.c), run_time=0.6)
        ga = gene_arrow()
        self.at("transcribing a")
        self.play(nuc.gene.animate.set_fill(GREEN), GrowArrow(ga), run_time=0.45)
        self.at("gene called")
        self.play(FadeIn(gl), run_time=0.3)

        # reset, and run it again with the ribosomes stopped
        self.at("Now use")
        self.play(FadeOut(gf, shift=UP * 0.1), FadeOut(ga), nuc.gene.animate.set_fill(GREY),
                  Rotate(ck.hand, TAU / 5, about_point=ck.c), run_time=0.5)
        drug, bar, rib, cross = drug_block()
        self.at("a drug")
        self.play(FadeIn(drug, shift=RIGHT * 0.1), run_time=0.35)
        self.at("stop every")
        self.play(Create(bar), FadeIn(rib), run_time=0.45)
        self.at("in the cell")
        self.play(Create(cross), run_time=0.35)

        self.at("The gene still")
        self.play(FadeIn(gf, shift=DOWN * 0.3), run_time=0.4)
        ga2 = gene_arrow()
        self.at("switches on")
        self.play(nuc.gene.animate.set_fill(GREEN), GrowArrow(ga2), run_time=0.4)
        self.play(Rotate(ck.hand, -TAU / 5, about_point=ck.c), run_time=0.6)

        # so something was already there
        qb = question_box()
        self.at("already made")
        self.play(FadeIn(qb, scale=0.8), run_time=0.5)
        here = VGroup(T("already made,", 28, TEXT), T("waiting", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([-4.4, CREB_Y, 0])
        self.at("and waiting")
        self.play(FadeIn(here, shift=RIGHT * 0.12), run_time=0.5)
        self.at("What was waiting")
        self.play(pop(qb[2], 1.5), run_time=0.6)
        top = CREB_Y + LOBE_H / 2 + 0.12
        doubt = DashedLine([0.0, MEM_Y - 0.2, 0], [CX, top + 0.1, 0], color=YELLOW, stroke_width=5, dash_length=0.16)
        tipm = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI).move_to([CX, top + 0.04, 0])
        qm = VGroup(Circle(radius=0.34, stroke_width=0, fill_color=BG, fill_opacity=1), T("?", 40, YELLOW, weight=BOLD)).move_to([-0.45, 0.45, 0])
        self.at("signal do")
        self.play(Create(doubt), FadeIn(tipm), FadeIn(qm), run_time=0.8)
        self.play(pop(qm, 1.4), pop(qb[2], 1.4), run_time=0.6)
        self.outro(FadeOut(VGroup(ck, mins, drug, bar, rib, cross, gf, doubt, tipm, qm, here, ga2)),
                   nuc.gene.animate.set_fill(GREY))


# ---------------------------------------------------------------------------------------------
class S02Waiting(Film):
    """a transcription factor that is already made, sitting on the DNA, is not yet enough. (the factor is CREB)"""

    def construct(self):
        mem, nuc, gl, qb = membrane(), nucleus(), gene_label(), question_box()
        self.add(mem, nuc, gl, qb)

        # the unknown becomes a transcription factor, and binds a short stretch of DNA
        tf = bchip("transcription factor", TEAL, 30).move_to([CX, -0.9, 0])
        self.play(FadeTransform(qb, tf), run_time=0.6)
        site = site_line()
        self.at("binds a short")
        self.play(tf.animate.move_to([CX, CREB_Y, 0]), Create(site), run_time=0.7)
        seq = T("short DNA sequence", 24, TEXT).move_to([CX, DNA_Y - 0.55, 0])
        self.at("short DNA")
        self.play(FadeIn(seq, shift=UP * 0.1), run_time=0.4)
        self.at("near a gene")
        self.play(glow_gene(nuc, 1.1), run_time=0.6)

        # making more is slow
        more = ghost_chip("make more factor", 28).move_to([-3.6, 0.35, 0])
        ck = clock([-0.6, 0.35, 0])
        slow = T("slow", 32, GREY).next_to(ck, RIGHT, buff=0.35)
        self.at("Making more")
        self.play(FadeIn(more, shift=RIGHT * 0.12), FadeIn(ck), run_time=0.5)
        self.at("is slow")
        self.play(FadeIn(slow), Rotate(ck.hand, -TAU, about_point=ck.c), run_time=0.9)
        xs = strike(more)
        self.at("gene responses")
        self.play(Create(xs), FadeOut(ck), FadeOut(slow), run_time=0.4)
        made = T("already made", 32, TEAL).move_to([CX, -0.95, 0])
        self.at("already made")
        self.play(FadeIn(made, shift=DOWN * 0.1), *glow(tf[1], tf[2], s=1.05), run_time=0.7)

        # the factor is CREB, in front of c-fos, as a pair
        c = creb()
        self.at("One such")
        self.play(FadeOut(tf), FadeIn(c), FadeOut(more), FadeOut(xs), run_time=0.6)
        self.at("in front")
        self.play(glow_gene(nuc, 1.1), run_time=0.7)
        pair = T("a pair", 30, TEAL).move_to([1.55, CREB_Y + 0.2, 0])
        self.at("as a pair")
        self.play(FadeIn(pair, shift=LEFT * 0.1), pop(c.lobes[0], 1.1), pop(c.lobes[1], 1.1), run_time=0.7)
        nos = T("no signal yet", 28, GREY).move_to([0, STRIP, 0])
        self.at("before any")
        self.play(FadeIn(nos), run_time=0.5)

        # sitting on the DNA is not enough
        self.at("Yet being")
        self.play(*glow(*c.lobes, *c.labels, s=1.05), run_time=0.6)
        ghost = DashedLine([GX0 + 0.2, DNA_Y + 0.5, 0], [GX1 - 0.2, DNA_Y + 0.5, 0], color=GREY, stroke_width=6, dash_length=0.16)
        off = T("gene still off", 28, GREY).move_to([GXC, DNA_Y + 1.15, 0])
        x2 = bigx([GXC, DNA_Y + 0.5, 0], 0.24)
        self.at("not enough")
        self.play(Create(ghost), FadeIn(off), run_time=0.5)
        self.play(FadeIn(x2, scale=0.6), run_time=0.3)
        self.outro(FadeOut(VGroup(made, pair, nos, seq, ghost, off, x2)))


# ---------------------------------------------------------------------------------------------
class S03Handle(Film):
    """cAMP frees PKA's catalytic subunits; one enters the nucleus and puts a phosphate on the serine of each CREB. (the handle)"""

    def construct(self):
        mem, nuc, gl, site, c = membrane(), nucleus(), gene_label(), site_line(), creb()
        self.add(mem, nuc, gl, site, c)
        pka, p1, p2 = pka_blob([-3.1, STRIP, 0])
        camp = sig("cAMP").move_to([-5.3, STRIP, 0])
        self.play(FadeIn(pka), FadeIn(p1), FadeIn(p2), FadeIn(camp), run_time=0.4)

        self.at("rises")
        self.play(camp.animate.move_to([-4.45, STRIP, 0]), run_time=0.5)
        self.play(pop(camp, 1.2), run_time=0.4)
        self.at("frees the")
        self.play(p1.animate.move_to([-1.2, STRIP + 0.2, 0]), p2.animate.move_to([-1.2, STRIP - 0.2, 0]), run_time=0.7)
        cat = T("catalytic subunits", 26, PURPLE).move_to([1.0, STRIP, 0])
        self.at("catalytic subunits")
        self.play(FadeIn(cat, shift=RIGHT * 0.1), pop(p1, 1.3), pop(p2, 1.3), run_time=0.7)
        self.at("kinase called")
        self.play(*glow(pka[1], pka[2], s=1.08), run_time=0.6)

        # some enter the nucleus
        self.at("Some of them")
        self.play(pop(p1, 1.3), pop(p2, 1.3), run_time=0.6)
        pk = kin("PKA", PKA_POS)
        self.at("enter the")
        self.play(p1.animate.move_to(PKA_POS), run_time=1.0)
        self.play(ReplacementTransform(p1, pk), run_time=0.3)

        # a phosphate onto the serine of each CREB
        st = stalk()
        self.at("There")
        self.play(*[Create(l) for l in st.lines], *[FadeIn(d, scale=0.5) for d in st.dots], run_time=0.5)
        pbs = [pbadge().move_to(pk.get_right() + RIGHT * 0.2) for _ in TIPS]
        self.at("puts a phosphate")
        self.play(FadeIn(pbs[0], scale=0.5), run_time=0.25)
        self.play(pbs[0].animate.move_to(TIPS[0]), FadeIn(pbs[1], scale=0.5), run_time=0.5)
        self.play(pbs[1].animate.move_to([CX, 0.65, 0]), run_time=0.35)      # over the first badge, not through it
        self.play(pbs[1].animate.move_to(TIPS[1]), run_time=0.35)
        ser = T("serine 133", 28, TEAL).move_to([CX, 0.4, 0])
        self.at("one serine")
        self.play(FadeIn(ser, shift=DOWN * 0.1), *[pop(p, 1.3) for p in pbs], run_time=0.6)

        # the phosphate is a handle
        hd = T("a handle", 32, GOLD, weight=BOLD).move_to([1.2, -0.95, 0])
        self.at("is a handle")
        self.play(FadeIn(hd, shift=UP * 0.1), *[pop(p, 1.5) for p in pbs], run_time=0.8)
        self.at("something another")
        self.play(*[glow(p[0], p[1], s=1.2)[i] for p in pbs for i in (0, 1)], run_time=0.7)
        self.outro(FadeOut(VGroup(camp, pka, p2, cat, ser, hd)))


# ---------------------------------------------------------------------------------------------
class S04Grip(Film):
    """KIX on CBP grips the phosphate; CBP acetylates histones and calls in the machinery; the gene turns on."""

    def construct(self):
        mem, nuc, gl, site, c = membrane(), nucleus(), gene_label(), site_line(), creb()
        st = stalk()
        pk = kin("PKA", PKA_POS)
        pbs = [pbadge().move_to(t) for t in TIPS]
        self.add(mem, nuc, gl, site, c, st, pk, *pbs)

        # a co-activator does not bind DNA itself
        H = np.array([2.0, 0.85, 0])
        co = cbp(H)
        self.at("helper protein")
        self.play(FadeIn(co, shift=DOWN * 0.2), run_time=0.6)
        reach = DashedLine([H[0], H[1] - CBP_H / 2 - 0.05, 0], [H[0], DNA_Y + GH / 2, 0], color=GREY, stroke_width=5, dash_length=0.16)
        no = bigx([H[0], -0.9, 0], 0.24)
        nod = T("does not bind DNA", 28, RED).move_to([4.2, -0.9, 0])
        self.at("does not bind")
        self.play(Create(reach), FadeIn(no, scale=0.6), FadeIn(nod, shift=LEFT * 0.1), run_time=0.7)

        # it is CBP, and it has a small domain called KIX
        name = T("CBP", 36, ORANGE, weight=BOLD).move_to(H)
        self.at("has a small")
        self.play(FadeOut(reach), FadeOut(no), FadeOut(nod), ReplacementTransform(co[2], name), run_time=0.6)
        cp = cup(H + np.array([CUP_DX, CUP_DY, 0]))
        kx = T("KIX", 30, PINK, weight=BOLD).move_to(H + np.array([CUP_DX + 1.25, CUP_DY + 0.05, 0]))
        self.at("domain called")
        self.play(FadeIn(cp, scale=0.5), FadeIn(kx, shift=LEFT * 0.1), run_time=0.6)
        grp = VGroup(co[0], co[1], name, cp, kx)

        # KIX grips the phosphate
        D = (TIP - np.array([CUP_DX, CUP_DY, 0])) - H
        self.at("grips")
        self.play(grp.animate.shift(D), run_time=1.0)
        self.at("far more tightly")
        self.play(Transform(cp, cup(TIP, tight=True)), run_time=0.5)
        tight = T("tight grip", 28, PINK).move_to([1.35, -1.0, 0])
        self.play(FadeIn(tight, shift=UP * 0.1), run_time=0.4)
        self.at("the phosphate is")
        self.play(pop(pbs[1], 1.4), run_time=0.7)

        # CBP acetylates the histones, which loosen
        beads = [bead(x) for x in BEAD_X]
        hist = T("histones", 28, GREY).move_to([1.85, BEAD_Y + 0.15, 0])
        self.at("adds acetyl")
        self.play(FadeOut(tight), LaggedStart(*[FadeIn(b, scale=0.6) for b in beads], lag_ratio=0.2), FadeIn(hist), run_time=0.9)
        acs = [ac_badge().move_to([2.2, 0.45, 0]) for _ in beads]
        self.at("acetyl groups")
        self.play(LaggedStart(*[a.animate.move_to([b.get_center()[0], BEAD_Y + 0.55, 0]) for a, b in zip(acs, beads)], lag_ratio=0.2), run_time=1.6)
        self.at("which loosens")
        self.play(*[b.animate.shift(RIGHT * d).set_fill(GREY, 0.25) for b, d in zip(beads, BEAD_LOOSEN)],
                  *[a.animate.shift(RIGHT * d) for a, d in zip(acs, BEAD_LOOSEN)], run_time=1.0)

        # it also contacts the machinery that brings in RNA polymerase
        mach = bchip("machinery", BLUE, 26).move_to([4.2, 0.7, 0])
        link = Line([H[0] + D[0] + CBP_W / 2, 0.7, 0], mach.get_left() + LEFT * 0.04, color=ORANGE, stroke_width=7)
        self.at("contacts the")
        self.play(Create(link), FadeIn(mach, shift=LEFT * 0.15), run_time=0.7)
        pol = bchip("RNA polymerase", BLUE, 26).move_to([4.2, 0.7, 0])
        self.at("brings in")
        self.play(FadeIn(pol, scale=0.8), run_time=0.3)
        self.play(pol.animate.move_to([3.72, -0.5, 0]), run_time=0.9)
        down = Arrow([3.72, -0.9, 0], [3.72, DNA_Y + GH / 2 + 0.05, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.22)
        self.at("polymerase")
        self.play(GrowArrow(down), nuc.gene.animate.set_fill(GREEN), run_time=0.7)
        self.outro(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------------------------
class S05Meet(Film):
    """calcium reaches the serine of each CREB through CaMKIV, and growth factors through ERK's kinases."""

    def construct(self):
        mem, nuc, gl, site, c, st, bar = membrane(), nucleus(), gene_label(), site_line(), creb(), stalk(), serine_bar()
        self.play(FadeIn(Group(mem, nuc, gl, site, c, st, bar)), run_time=0.4)

        # the cAMP route, shown dimmed: it is the one we just followed
        camp = sig("cAMP").move_to([-5.0, STRIP, 0])
        pk = kin("PKA", [-4.6, 0.3, 0])
        a_ck = arr(camp.get_bottom() + DOWN * 0.02, pk.get_top() + UP * 0.02, GREY, w=4, tip=0.16)
        a_kt = arr(pk.get_right() + RIGHT * 0.05, bar_pt(0.0), PURPLE, w=5)
        lane_l = VGroup(camp, pk, a_ck, a_kt)
        lane_l.save_state()
        self.at("different messenger")
        self.play(FadeIn(lane_l), run_time=0.5)
        self.play(lane_l.animate.set_opacity(0.4), run_time=0.4)

        # the calcium route
        ca = sig("calcium").move_to([-3.0, STRIP, 0])
        cm = sig("calmodulin").move_to([-0.6, STRIP, 0])
        self.at("messenger calcium")
        self.play(FadeIn(ca, shift=DOWN * 0.15), run_time=0.5)
        self.at("and calmodulin")
        self.play(FadeIn(cm, shift=LEFT * 0.15), run_time=0.5)
        pairbox = SurroundingRectangle(VGroup(ca, cm), color=YELLOW, buff=0.08, corner_radius=0.2, stroke_width=3)
        self.at("upstream kinase")
        self.play(Create(pairbox), run_time=0.5)
        cam = kin("CaMKIV", [CX, 0.9, 0])
        a_pc = arr([CX, pairbox.get_bottom()[1], 0], cam.get_top() + UP * 0.02, YELLOW, w=5)
        self.at("switch on")
        self.play(GrowArrow(a_pc), FadeIn(cam, scale=0.8), run_time=0.6)
        nl = T("largely in the nucleus", 26, GREY).move_to([2.4, 0.9, 0])
        self.at("found largely")
        self.play(FadeIn(nl, shift=DOWN * 0.1), run_time=0.5)
        pbs = [pbadge().move_to(cam.get_bottom() + DOWN * 0.1 + RIGHT * dx) for dx in (-0.35, 0.35)]
        self.at("phosphorylates")
        self.play(FadeIn(pbs[0], scale=0.5), FadeIn(pbs[1], scale=0.5), run_time=0.2)
        self.play(pbs[0].animate.move_to(TIPS[0]), pbs[1].animate.move_to(TIPS[1]), run_time=0.7)
        same = T("same serine", 28, TEAL).move_to([1.3, -0.95, 0])
        self.at("same serine")
        self.play(FadeIn(same, shift=LEFT * 0.1), *[pop(p, 1.3) for p in pbs], run_time=0.7)

        # two messengers meet at the serine of each CREB
        a_ct = arr(cam.get_bottom() + DOWN * 0.02, bar_pt(0.5), PURPLE, w=5)
        self.at("a place where")
        self.play(FadeOut(nl), GrowArrow(a_ct), Restore(lane_l), run_time=0.7)
        self.at("either one")
        self.play(Indicate(a_kt, color=TEXT, scale_factor=1.0), run_time=0.5)
        self.play(Indicate(a_ct, color=TEXT, scale_factor=1.0), run_time=0.5)
        self.at("same handle")
        self.play(*[pop(p, 1.5) for p in pbs], run_time=0.7)

        # growth factors reach it too, through ERK's kinases (a growth factor is outside the cell)
        gf = on_membrane(sig("growth factor")).set_x(4.9)
        self.at("Growth factors")
        self.play(FadeIn(gf, shift=DOWN * 0.3), run_time=0.5)
        self.at("that serine too")
        self.play(FadeOut(same), *[pop(p, 1.3) for p in pbs], run_time=0.6)
        kk = kin("kinases", [3.4, -0.2, 0])
        a_kk = arr(kk.get_left() + LEFT * 0.04, bar_pt(1.0), PURPLE, w=5)
        self.at("through kinases")
        self.play(FadeIn(kk, scale=0.8), GrowArrow(a_kk), run_time=0.6)
        erk = kin("ERK", [2.9, STRIP, 0])
        a1 = dashed_arrow([4.3, gf.get_bottom()[1] - 0.02, 0], erk.get_top() + RIGHT * 0.3 + UP * 0.02, YELLOW, w=5, dash=0.12)
        a2 = arr(erk.get_bottom() + DOWN * 0.02, kk.get_top() + UP * 0.02, PURPLE, w=4, tip=0.16)
        self.at("switches on")
        self.play(FadeIn(erk, scale=0.8), Create(a1[0]), FadeIn(a1[1]), GrowArrow(a2), run_time=0.7)
        self.outro(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------------------------
class S06Rule(Film):
    """back to c-fos: the signals reach CREB, already in place, so the ribosomes do not matter."""

    def construct(self):
        mem, nuc, gl, site, c, st, bar = membrane(), nucleus(), gene_label(), site_line(), creb(), stalk(), serine_bar()
        gf = on_membrane(sig("growth factor"))
        drug, bar_, rib, cross = drug_block()
        self.play(FadeIn(Group(mem, nuc, gl, site, c, st, bar, gf, drug, bar_, rib, cross)), run_time=0.5)

        self.at("go back")
        self.play(glow_gene(nuc, 1.1), run_time=0.6)
        by = DNA_Y - 0.4
        reg = VGroup(Line([CX - 1.5, by, 0], [GX0 - 0.1, by, 0], color=GREY, stroke_width=4),
                     Line([CX - 1.5, by, 0], [CX - 1.5, by + 0.14, 0], color=GREY, stroke_width=4),
                     Line([GX0 - 0.1, by, 0], [GX0 - 0.1, by + 0.14, 0], color=GREY, stroke_width=4))
        regl = T("control region", 24, GREY).move_to([(CX - 1.5 + GX0 - 0.1) / 2, by - 0.22, 0])
        self.at("control region")
        self.play(Create(reg), FadeIn(regl), run_time=0.6)
        self.at("site for")
        self.play(*glow(*c.lobes, *c.labels, s=1.06), run_time=0.7)

        # three signals can each reach it (the growth factor's path has several steps, so its arrow is dashed)
        camp, ca = sig("cAMP").move_to([2.4, STRIP, 0]), sig("calcium").move_to([4.6, STRIP, 0])
        a_g = dashed_arrow([-0.1, gf.get_bottom()[1], 0], bar_pt(0.0), YELLOW, w=5)
        a_c = arr(camp.get_bottom() + DOWN * 0.02, bar_pt(0.5), YELLOW, w=5)
        a_a = arr(ca.get_bottom() + DOWN * 0.02, bar_pt(1.0), YELLOW, w=5)
        self.at("calcium and")
        self.play(FadeIn(camp, shift=DOWN * 0.15), FadeIn(ca, shift=DOWN * 0.15), run_time=0.5)
        self.at("growth factors")
        self.play(Create(a_g[0]), FadeIn(a_g[1]), GrowArrow(a_c), GrowArrow(a_a), run_time=0.9)
        place = T("already in place", 30, TEAL).move_to([-4.0, CREB_Y + 0.1, 0])
        self.at("already in place")
        self.play(FadeIn(place, shift=RIGHT * 0.1), *glow(*c.lobes, *c.labels, s=1.05), run_time=0.7)

        # recap the signal response with the ribosomes stopped, without implying phosphate alone is sufficient
        self.at("That is why")
        self.play(*glow(*c.lobes, *c.labels, s=1.05), run_time=0.4)
        ga = gene_arrow()
        self.at("did not matter")
        self.play(nuc.gene.animate.set_fill(GREEN), GrowArrow(ga), *glow(drug, rib[2], s=1.12), run_time=0.7)

        # the rule
        made = T("already made", 32, TEAL).move_to([1.6, -1.0, 0])
        self.at("is already made")
        self.play(FadeOut(place), FadeIn(made, shift=DOWN * 0.1), *glow(*c.lobes, *c.labels, s=1.05), run_time=0.7)
        self.at("the signal")
        self.play(Indicate(a_g, color=TEXT, scale_factor=1.0), Indicate(a_c, color=TEXT, scale_factor=1.0),
                  Indicate(a_a, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("changes what")
        self.play(*glow(*c.lobes, *c.labels, s=1.12), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The factor is already made; the signal changes what it does."
