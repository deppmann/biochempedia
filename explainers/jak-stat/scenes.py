"""Cytokine receptors and JAK-STAT: one protein from receptor to gene  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the cytokine (interferon): the signal outside the cell
  BLUE   = receptor chains
  PURPLE = JAK, the borrowed tyrosine kinase
  TEAL   = STAT, the protein that travels to the DNA
  PINK   = the SH2 domain (the cup on each STAT that grips a phosphate)
  GOLD   = a phosphate (the round "P" badge)
  GREEN  = on / active (active JAK outline, gene switched on, the signal getting through)
  RED    = blocked or ruled out (the drug, the routes this pathway does not use)
  GREY   = membrane, nucleus, DNA, labels, parts not yet known

No molecular structures: receptor chains are bars, JAK and STAT are labelled blobs, the SH2 domain
is a cup on the blob, a phosphate is a "P" badge, DNA is a line and a gene is a block on it.

One picture, three framings (the same parts, rebuilt bigger where they are the subject):
  WIDE  (scenes 1 and 6)  the whole cell: membrane on top, nucleus and DNA at the bottom.
  TIGHT (scenes 2 and 3)  the receptor and its JAKs fill the frame; no nucleus.
  MID   (scenes 4 and 5)  receptor on top, STATs docking and pairing below it; no nucleus.
Each change of framing is animated at the end of a scene, after the narration (Film.outro, then=...),
so the next scene starts on exactly the picture the last one left.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"

NUC_TOP, NUC_BOT = -1.95, -3.45     # the nucleus, WIDE framing only
DNA_Y = -3.2
BOUND_Y = -2.6                      # the STAT pair sitting on the DNA


# ---------------------------------------------------------------------------------------------
# framings
# ---------------------------------------------------------------------------------------------
class Lay:
    """One framing. Sizes scale with k; the vertical positions are set by hand for each framing."""

    def __init__(self, k, mem_y, mem_h, ch_top, ch_bot, jak_y, x_in, x_out=0.0, pair_y=0.0, park_x=0.0, wait=None):
        self.k, self.mem_y, self.mem_h = k, mem_y, mem_h
        self.ch_top, self.ch_bot = ch_top, ch_bot      # a chain runs from outside (top) to the end of its tail
        self.jak_y = jak_y                              # the JAK sits on the tail just under the membrane
        self.x_in, self.x_out = x_in, x_out             # chain x after / before the cytokine sets them in position
        self.pair_y = pair_y                            # where the STAT pair forms
        self.park_x = park_x                            # where the cytokine waits before it binds
        self.wait = wait                                # where the two STATs wait in the cytoplasm
        self.sw = 3 * k ** 0.5                          # outline width
        self.pr = 0.18 * k                              # phosphate badge radius

    def jp(self, side):
        """the phosphate on a JAK: outer edge, mid height."""
        return np.array([side * (self.x_in + 0.65 * self.k), self.jak_y, 0])

    def dock(self, side):
        """the phosphorylated tyrosine at the end of a tail."""
        return np.array([side * self.x_in, self.ch_bot - 0.05 * self.k, 0])

    def docked(self, side):
        """STAT body centre when its cup is on that tail's phosphate."""
        return self.dock(side) + self.k * np.array([0.25, -0.75, 0])

    def pair(self, side):
        """STAT body centre in the finished pair."""
        return np.array([side * 0.9 * self.k, self.pair_y, 0])


WIDE = Lay(k=1.0, mem_y=2.1, mem_h=0.28, ch_top=2.8, ch_bot=0.3, jak_y=1.5, x_in=0.75, pair_y=-1.2)
TIGHT = Lay(k=1.9, mem_y=1.54, mem_h=0.4, ch_top=2.29, ch_bot=-1.9, jak_y=0.595, x_in=1.36, x_out=2.7, park_x=-4.75)
MID = Lay(k=1.5, mem_y=1.91, mem_h=0.34, ch_top=2.53, ch_bot=-0.12, jak_y=1.135, x_in=1.08, pair_y=-2.55,
          wait=(np.array([-4.4, -2.3, 0]), np.array([4.7, -2.3, 0])))


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=22):
    """a dashed grey chip: something that is NOT in this pathway."""
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


def pbadge(k=1.0):
    """a phosphate."""
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    """swell and settle, without recolouring (Indicate would hide the P on a badge)."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place. One animation per mobject: wrapping them in a new VGroup would
    re-add them to the scene on top of everything drawn later (it hid the phosphate badges)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def membrane(L):
    return RoundedRectangle(corner_radius=0.1, width=12.6, height=L.mem_h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, L.mem_y, 0])


def nucleus():
    """nucleus, DNA and a block of genes (WIDE framing)."""
    env = RoundedRectangle(corner_radius=0.5, width=10.4, height=NUC_TOP - NUC_BOT, stroke_color=GREY,
                           stroke_width=3).move_to([0, (NUC_TOP + NUC_BOT) / 2, 0])
    dna = Line([-3.9, DNA_Y, 0], [4.7, DNA_Y, 0], color=GREY, stroke_width=6)
    gene = Rectangle(width=2.5, height=0.22, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([3.15, DNA_Y, 0])
    nuc_lbl = T("nucleus", 22, GREY).move_to([-4.3, -2.3, 0])
    dna_lbl = T("DNA", 22, GREY).move_to([-4.45, DNA_Y + 0.02, 0])
    gene_lbl = T("genes", 24, GREY).move_to([3.15, -2.55, 0])
    g = VGroup(env, dna, gene, nuc_lbl, dna_lbl, gene_lbl)
    g.gene, g.gene_lbl = gene, gene_lbl
    return g


def cell():
    """the whole cell (WIDE): membrane plus nucleus."""
    mem, nuc = membrane(WIDE), nucleus()
    g = VGroup(mem, nuc)
    g.mem, g.nuc, g.gene, g.gene_lbl = mem, nuc, nuc.gene, nuc.gene_lbl
    return g


def gene_arrow():
    """the gene being read: an arrow running along it."""
    return Arrow([1.9, -2.95, 0], [4.4, -2.95, 0], buff=0, color=GREEN, stroke_width=5, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.45)


def gene_on(c, color=GREEN):
    return [c.gene.animate.set_fill(color), c.gene_lbl.animate.set_color(color)]


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def sig(L, text):
    """the cytokine chip."""
    return bchip(text, YELLOW, 24 * L.k, pad=0.15 * L.k)


def on_membrane(L, ch):
    return ch.next_to([0, L.mem_y + L.mem_h / 2, 0], UP, buff=0.08)


def parked(L, ch):
    return ch.next_to([L.park_x, L.ch_top, 0], UP, buff=0.02)


def on_chains(L, ch):
    return ch.next_to([0, L.ch_top, 0], UP, buff=0.02)


def chain(L, x):
    """one receptor chain: a bar that crosses the membrane once. No enzyme anywhere on it."""
    h, w, r = L.ch_top - L.ch_bot, 0.3 * L.k, 0.12 * L.k
    back = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    bar = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=BLUE, stroke_width=L.sw,
                           fill_color=BLUE, fill_opacity=0.4)
    return VGroup(back, bar).move_to([x, (L.ch_top + L.ch_bot) / 2, 0])


def jak(L, x, active=False):
    """the kinase held on the tail, just inside the membrane. [back, body, label]"""
    k = L.k
    back = RoundedRectangle(corner_radius=0.3 * k, width=1.3 * k, height=0.7 * k, stroke_width=0, fill_color=BG, fill_opacity=1)
    body = RoundedRectangle(corner_radius=0.3 * k, width=1.3 * k, height=0.7 * k, stroke_color=GREEN if active else PURPLE,
                            stroke_width=L.sw + 2 if active else L.sw, fill_color=PURPLE, fill_opacity=0.35)
    lbl = T("JAK", 24 * k, PURPLE, weight=BOLD)
    g = VGroup(back, body, lbl).move_to([x, L.jak_y, 0])
    g.body, g.lbl = body, lbl
    return g


def jglow(j, s=1.1):
    return glow(j[1], j[2], s=s)


def stat(L, center):
    """A STAT in its docking pose: SH2 cup on top (opening upward), its own tyrosine on a short tail beside it.

    g.rig turns as one rigid piece (spin_move); the label and the phosphate badge stay upright.
    """
    k, c = L.k, np.array(center, float)
    sb = 1.1 * k
    back = RoundedRectangle(corner_radius=0.26 * k, width=sb, height=sb, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    body = RoundedRectangle(corner_radius=0.26 * k, width=sb, height=sb, stroke_color=TEAL, stroke_width=L.sw,
                            fill_color=TEAL, fill_opacity=0.25).move_to(c)
    tail = Line(c + k * np.array([0.25, 0.4, 0]), c + k * np.array([0.25, 1.05, 0]), color=TEAL, stroke_width=7 * k ** 0.5)
    tip = Dot(c + k * np.array([0.25, 1.05, 0]), radius=0.08 * k, color=TEAL)
    cupc = c + k * np.array([-0.25, 0.75, 0])
    cup = AnnularSector(inner_radius=0.21 * k, outer_radius=0.34 * k, angle=200 * DEGREES, start_angle=170 * DEGREES,
                        color=PINK, fill_opacity=1, stroke_width=0).shift(cupc)
    mark = Dot(cupc, radius=0.01).set_opacity(0)      # invisible: remembers where the cup's centre is
    rig = VGroup(tail, tip, back, body, cup, mark)
    label = T("STAT", 22 * k, TEAL, weight=BOLD).move_to(c)
    g = VGroup(rig, label)
    g.rig, g.body, g.cup, g.mark, g.tip, g.label, g.p, g.k = rig, body, cup, mark, tip, label, None, k
    return g


def give_p(s, badge=None):
    """put a phosphate on the STAT's tyrosine."""
    s.p = (badge or pbadge(s.k)).move_to(s.tip.get_center())
    s.add(s.p)
    return s


def posed(L, center, angle):
    """a phosphorylated STAT already turned to its pairing pose."""
    s = stat(L, center)
    s.rig.rotate(angle, about_point=np.array(center, float))
    return give_p(s)


def spin_move(s, angle, new_center):
    """turn the STAT rigidly about its body while it travels; label and phosphate ride along upright."""
    start = s.rig.copy()
    c0 = s.body.get_center().copy()
    delta = np.array(new_center, float) - c0

    def upd(m, a):
        s.rig.become(start.copy().rotate(a * angle, about_point=c0).shift(a * delta))
        s.label.move_to(s.body.get_center())
        if s.p is not None:
            s.p.move_to(s.tip.get_center())
    return UpdateFromAlphaFunc(s, upd)


def ghost_cup(L, center):
    """where an SH2 cup used to grip."""
    a = AnnularSector(inner_radius=0.21 * L.k, outer_radius=0.34 * L.k, angle=200 * DEGREES, start_angle=170 * DEGREES,
                      color=PINK, fill_opacity=0.0, stroke_width=3).shift(center)
    a.set_stroke(PINK, 3, opacity=1)
    return DashedVMobject(a, num_dashes=18)


def complex_on(L):
    """the receptor in position with both JAKs active: [membrane, chains, JAKs, cytokine, JAK phosphates]."""
    mem = membrane(L)
    cyt = on_chains(L, sig(L, "cytokine"))
    chL, chR, jL, jR = chain(L, -L.x_in), chain(L, L.x_in), jak(L, -L.x_in, True), jak(L, L.x_in, True)
    pL, pR = pbadge(L.k).move_to(L.jp(-1)), pbadge(L.k).move_to(L.jp(1))
    return mem, cyt, chL, chR, jL, jR, pL, pR


def reframe(old, new):
    """morph each piece into the same piece of another framing."""
    return [Transform(a, b) for a, b in zip(old, new)]


class Film(SpokenScene):
    def outro(self, *anims, then=None, after=None, run_time=0.38):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing (`then`, and `after` once that has settled). These run after the last word, so
        they add a short breath between scenes."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.9)
        if after:
            self.play(*after, run_time=0.45)
        if then or after:
            self.wait(0.15)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Cytokine Receptors and JAK–STAT"
    TITLE = "One protein from receptor to gene"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """interferon in, genes on within minutes, even with no new protein: the path is already there. (WIDE)"""

    def construct(self):
        c = cell()
        ifn = on_membrane(WIDE, sig(WIDE, "interferon"))
        self.play(FadeIn(c), run_time=0.4)
        self.play(FadeIn(ifn, shift=DOWN * 0.35), run_time=0.6)

        self.at("a set of genes")
        self.play(Indicate(c.gene, color=TEXT, scale_factor=1.12), Indicate(c.gene_lbl, color=TEXT, scale_factor=1.12), run_time=0.6)
        ga = gene_arrow()
        self.at("switches on")
        self.play(*gene_on(c), GrowArrow(ga), run_time=0.45)
        ck = clock([4.3, 0.1, 0])
        mins = T("minutes", 24, GREY).move_to([4.3, -0.7, 0])
        self.at("within minutes")
        self.play(FadeIn(ck), FadeIn(mins), run_time=0.3)
        self.play(Rotate(ck.hand, -TAU / 5, about_point=ck.c), run_time=0.7)

        warn = T("warns cells of a virus", 24, GREY).next_to(ifn, RIGHT, buff=0.3)
        self.at("a protein that warns")
        self.play(FadeIn(warn, shift=RIGHT * 0.12), run_time=0.5)

        # run it again, this time with the drug: reset, and take the interferon away first
        self.at("The genes still")
        self.play(*gene_on(c, GREY), FadeOut(ga), FadeOut(warn), Rotate(ck.hand, TAU / 5, about_point=ck.c),
                  ifn.animate.shift(UP * 0.45), run_time=0.5)
        newp = bchip("new protein", GREY, 24).move_to([-4.0, 0.2, 0])
        drug = T("drug", 26, RED, weight=BOLD).move_to([-4.0, 1.3, 0])
        bar = inhib([-4.0, 1.05, 0], [-4.0, 0.66, 0])
        self.at("when a drug")
        self.play(FadeIn(newp), FadeIn(drug, shift=DOWN * 0.1), Create(bar), run_time=0.4)
        cross = strike(newp)
        self.at("stops the cells")
        self.play(Create(cross), newp[1].animate.set_stroke(opacity=0.6).set_fill(opacity=0.08),
                  newp[2].animate.set_opacity(0.7), run_time=0.4)
        ga2 = gene_arrow()
        self.at("making any new")
        self.play(ifn.animate.shift(DOWN * 0.45), run_time=0.3)
        self.play(*gene_on(c), GrowArrow(ga2), run_time=0.4)
        self.play(Rotate(ck.hand, -TAU / 5, about_point=ck.c), run_time=0.6)

        # so the whole path is already in the cell
        path = DashedLine([0, WIDE.mem_y - 0.2, 0], [0, -2.82, 0], color=GREY, stroke_width=4, dash_length=0.12)
        tipm = Triangle(fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.13).rotate(PI).move_to([0, -2.93, 0])
        qs, solids = VGroup(), []
        for y in (1.05, -0.15, -1.35):
            shape = RoundedRectangle(corner_radius=0.12, width=0.78, height=0.62)
            back = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to([0, y, 0])
            edge = DashedVMobject(shape.copy().move_to([0, y, 0]), num_dashes=20).set_color(GREY)
            q = T("?", 28, TEXT, weight=BOLD).move_to([0, y, 0])
            qs.add(VGroup(back, edge, q))
            solids.append(shape.copy().set_stroke(TEXT, 3).set_fill(GREY, 0.35).move_to([0, y, 0]))
        self.at("every part")
        self.play(Create(path), FadeIn(tipm), LaggedStart(*[FadeIn(b, scale=0.8) for b in qs], lag_ratio=0.25), run_time=1.0)
        surf = T("cell surface", 22, GREY).move_to([-4.9, WIDE.mem_y + 0.5, 0])
        self.at("from the cell surface")
        self.play(FadeIn(surf), Indicate(c.mem, color=TEXT, scale_factor=1.0), run_time=0.6)
        self.at("to those genes")
        self.play(Indicate(c.gene, color=TEXT, scale_factor=1.12), Indicate(c.gene_lbl, color=TEXT, scale_factor=1.12), run_time=0.6)
        self.at("must already be")
        self.play(*[Transform(b[1], s) for b, s in zip(qs, solids)], run_time=0.6)
        here = T("already in the cell, waiting", 24, TEXT).move_to([-3.55, -1.1, 0])
        self.at("waiting")
        self.play(FadeIn(here, shift=RIGHT * 0.12), run_time=0.5)
        self.at("What is the path")
        self.play(LaggedStart(*[pop(b[2], 1.6) for b in qs], lag_ratio=0.3), run_time=1.0)
        # clear the puzzle, then move in on the cell surface (TIGHT): the nucleus drops out of frame
        self.outro(FadeOut(VGroup(path, tipm, qs, here, surf, ck, mins, newp, drug, bar, cross, ga2)),
                   then=[*reframe([c.mem, ifn], [membrane(TIGHT), on_membrane(TIGHT, sig(TIGHT, "interferon"))]),
                         FadeOut(c.nuc, shift=DOWN * 1.2)])


# ---------------------------------------------------------------------------------------------
class S02Borrow(Film):
    """a receptor chain with no enzyme, and the separate kinase (JAK) held on its tail. (TIGHT)"""

    def construct(self):
        L = TIGHT
        mem = membrane(L)
        ifn = on_membrane(L, sig(L, "interferon"))
        self.add(mem, ifn)
        cyt = on_membrane(L, sig(L, "cytokine"))
        self.at("is a cytokine")
        self.play(ReplacementTransform(ifn, cyt), run_time=0.6)
        cap = T("a small secreted protein", 28, GREY).next_to(cyt, RIGHT, buff=0.35)
        self.at("a small secreted")
        self.play(FadeIn(cap, shift=RIGHT * 0.12), run_time=0.5)
        tell = Arrow([0, L.mem_y - L.mem_h / 2 - 0.1, 0], [0, -0.6, 0], buff=0, color=YELLOW, stroke_width=8, tip_length=0.32)
        self.at("tells other cells")
        self.play(GrowArrow(tell), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(tell), run_time=0.3)

        # the cytokine steps aside: nothing has bound yet
        self.at("Each chain")
        self.play(cyt.animate.become(parked(L, sig(L, "cytokine"))), FadeOut(cap), run_time=0.6)
        chL = chain(L, -L.x_out)
        rl = T("receptor chain", 28, BLUE).next_to([-L.x_out + 0.15 * L.k, (L.ch_top + L.mem_y + L.mem_h / 2) / 2, 0], RIGHT, buff=0.3)
        self.at("receptor crosses")
        self.play(GrowFromEdge(chL, UP), run_time=0.9)
        self.play(FadeIn(rl), run_time=0.3)

        # where a kinase would be if the chain had one: nothing
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=1.9, height=1.0), num_dashes=28).set_color(GREY)
        slot.move_to([-L.x_out, L.ch_bot - 0.65, 0])
        ne = T("no enzyme", 28, GREY).next_to(slot, RIGHT, buff=0.3)
        self.at("has no enzyme")
        self.play(Create(slot), FadeIn(ne), run_time=0.6)

        jL = jak(L, -L.x_out)
        tk = T("tyrosine kinase", 28, PURPLE).next_to(jL[1], RIGHT, buff=0.3)
        self.at("holds a separate")
        self.play(FadeOut(slot), FadeOut(ne), GrowFromCenter(VGroup(jL[0], jL[1])), run_time=0.6)
        self.play(FadeIn(tk, shift=RIGHT * 0.1), run_time=0.4)
        self.at("is called a")
        self.play(ReplacementTransform(tk, jL[2]), run_time=0.5)      # the description becomes the name on the blob
        self.play(*jglow(jL, 1.08), run_time=0.4)

        chR, jR = chain(L, L.x_out), jak(L, L.x_out)
        self.at("it is there")
        self.play(FadeIn(chR), FadeIn(jR), run_time=0.5)
        inplace = T("already in place", 28, GREY).move_to([0, -0.95, 0])
        self.at("before any")
        self.play(FadeIn(inplace), *jglow(jL, 1.06), *jglow(jR, 1.06), run_time=0.7)
        self.outro(FadeOut(rl), FadeOut(inplace))


# ---------------------------------------------------------------------------------------------
class S03Pair(Film):
    """the cytokine sets two chains in position; the two JAKs phosphorylate each other and switch on. (TIGHT)"""

    def construct(self):
        L = TIGHT
        mem = membrane(L)
        cyt = parked(L, sig(L, "cytokine"))
        chL, chR, jL, jR = chain(L, -L.x_out), chain(L, L.x_out), jak(L, -L.x_out), jak(L, L.x_out)
        self.add(mem, chL, chR, jL, jR, cyt)
        self.play(cyt.animate.become(on_chains(L, sig(L, "cytokine"))), run_time=1.0)

        self.at("sets receptor chains")
        d = L.x_out - L.x_in
        self.play(chL.animate.shift(RIGHT * d), jL.animate.shift(RIGHT * d),
                  chR.animate.shift(LEFT * d), jR.animate.shift(LEFT * d), run_time=1.1)
        self.at("and so they're")
        self.play(*jglow(jL, 1.06), *jglow(jR, 1.06), run_time=0.7)
        pos = T("in position", 28, GREY).next_to(jR[1], RIGHT, buff=0.35)
        self.at("in position")
        self.play(FadeIn(pos, shift=LEFT * 0.1), run_time=0.4)
        self.at("Now the two")
        self.play(FadeOut(pos), run_time=0.3)
        self.at("close enough")
        self.play(Flash(np.array([0, L.jak_y, 0]), color=TEXT, line_length=0.28, flash_radius=0.32, num_lines=10),
                  jL.animate(rate_func=there_and_back).shift(RIGHT * 0.09),
                  jR.animate(rate_func=there_and_back).shift(LEFT * 0.09), run_time=0.7)

        # each JAK puts a phosphate on the other
        x0, y0 = L.x_in - 0.42 * L.k, L.jak_y - 0.3 * L.k
        pR = pbadge(L.k).move_to([-x0, y0, 0])     # made by the left JAK, lands on the right one
        pL = pbadge(L.k).move_to([x0, y0, 0])      # and the other way round
        self.at("Each adds a")
        self.play(FadeIn(pR, scale=0.5), run_time=0.2)
        self.play(pR.animate(path_arc=2.0).move_to(L.jp(1)), run_time=0.5)
        self.play(FadeIn(pL, scale=0.5), run_time=0.2)
        self.play(pL.animate(path_arc=-2.0).move_to(L.jp(-1)), run_time=0.5)
        actL = T("active", 28, GREEN).next_to(L.jp(-1) + LEFT * L.pr, LEFT, buff=0.25)
        actR = T("active", 28, GREEN).next_to(L.jp(1) + RIGHT * L.pr, RIGHT, buff=0.25)
        self.at("both become")
        self.play(jL.body.animate.set_stroke(GREEN, L.sw + 2), jR.body.animate.set_stroke(GREEN, L.sw + 2), run_time=0.5)
        self.play(FadeIn(actL), FadeIn(actR), run_time=0.4)

        rec = T("receptor", 30, BLUE, weight=BOLD).move_to([-4.3, 3.02, 0])
        noenz = T("no enzyme of its own", 26, GREY).move_to([-4.3, 2.45, 0])
        self.at("A receptor with")
        self.play(FadeOut(actL), FadeOut(actR), FadeIn(rec),
                  Indicate(chL[1], color=TEXT, scale_factor=1.03), Indicate(chR[1], color=TEXT, scale_factor=1.03), run_time=0.6)
        self.at("no enzyme of")
        self.play(FadeIn(noenz), run_time=0.4)
        bor = T("borrowed kinase", 26, PURPLE, weight=BOLD).next_to(L.jp(1) + RIGHT * L.pr, RIGHT, buff=0.3)
        self.at("has borrowed")
        self.play(FadeIn(bor, shift=LEFT * 0.1), *jglow(jL, 1.06), *jglow(jR, 1.06), run_time=0.7)
        # pull back (MID): the tails need room below them for what docks there next
        m2, c2, chL2, chR2, jL2, jR2, pL2, pR2 = complex_on(MID)
        self.outro(FadeOut(rec), FadeOut(noenz), FadeOut(bor),
                   then=reframe([mem, cyt, chL, chR, jL, jR, pL, pR], [m2, c2, chL2, chR2, jL2, jR2, pL2, pR2]))


# ---------------------------------------------------------------------------------------------
class S04Dock(Film):
    """JAKs phosphorylate the tails; a waiting STAT docks there by its SH2 domain. (MID)"""

    def construct(self):
        L = MID
        mem, cyt, chL, chR, jL, jR, pL, pR = complex_on(L)
        self.add(mem, chL, chR, jL, jR, cyt, pL, pR)
        self.play(*jglow(jL, 1.06), *jglow(jR, 1.06), run_time=0.5)

        # a phosphate goes from each JAK down its tail to the tyrosine at the end
        dests = [L.dock(-1), L.dock(1)]
        tp = [pbadge(L.k).move_to([d[0], L.jak_y - 0.35 * L.k, 0]) for d in dests]      # each starts at its JAK
        self.at("now")
        self.play(*[FadeIn(p, scale=0.5) for p in tp], run_time=0.25)
        self.play(LaggedStart(*[p.animate.move_to(d) for p, d in zip(tp, dests)], lag_ratio=0.3), run_time=1.1)
        self.at("These")
        self.play(LaggedStart(*[pop(p, 1.4) for p in tp], lag_ratio=0.3), run_time=0.9)
        dock_lbl = T("docking sites", 28, GOLD).next_to(L.dock(-1) + LEFT * L.pr, LEFT, buff=0.4)
        self.at("docking sites")
        self.play(FadeIn(dock_lbl, shift=RIGHT * 0.1), pop(tp[0]), pop(tp[1]), run_time=0.6)

        # a STAT waits in the cytoplasm
        sA, sB = stat(L, L.wait[0]), stat(L, L.wait[1])
        cyto = T("cytoplasm", 24, GREY).move_to([-5.3, L.mem_y - L.mem_h / 2 - 0.4, 0])
        self.at("A protein called")
        self.play(FadeOut(dock_lbl), FadeIn(sA, shift=UP * 0.15), FadeIn(sB, shift=UP * 0.15), run_time=0.7)
        self.at("waits in the")
        self.play(FadeIn(cyto), sA.animate(rate_func=there_and_back).shift(UP * 0.15),
                  sB.animate(rate_func=there_and_back).shift(DOWN * 0.15), run_time=0.9)

        # its SH2 domain
        cupA = sA.mark.get_center()
        sh2 = T("SH2 domain", 30, PINK, weight=BOLD).move_to([-4.0, -0.05, 0])
        ptr = Line([cupA[0], -0.36, 0], [cupA[0], cupA[1] + 0.33, 0], color=PINK, stroke_width=4)
        self.at("It carries")
        self.play(FadeIn(sh2), Create(ptr), Indicate(sA.cup, color=TEXT, scale_factor=1.3),
                  Indicate(sB.cup, color=TEXT, scale_factor=1.3), run_time=0.8)
        desc = VGroup(T("binds a phosphate", 24, GREY), T("on a tyrosine", 24, GREY)).arrange(DOWN, buff=0.12).move_to([-4.0, 0.1, 0])
        self.at("a module that")
        self.play(sh2.animate.move_to([-4.0, 0.78, 0]), FadeIn(desc), run_time=0.5)
        self.at("binds a phosphate")
        self.play(pop(tp[0], 1.4), pop(tp[1], 1.4), Indicate(sA.cup, color=TEXT, scale_factor=1.25),
                  Indicate(sB.cup, color=TEXT, scale_factor=1.25), run_time=0.8)

        # dock: slide under the tail end, then rise so the cup closes on the phosphate
        dA, dB = L.docked(-1), L.docked(1)
        self.at("With that domain")
        self.play(FadeOut(sh2), FadeOut(desc), FadeOut(ptr),
                  sA.animate.shift(RIGHT * (dA[0] - L.wait[0][0])), sB.animate.shift(RIGHT * (dB[0] - L.wait[1][0])), run_time=0.9)
        self.at("docks on the")
        self.play(sA.animate.shift(UP * (dA[1] - L.wait[0][1])), sB.animate.shift(UP * (dB[1] - L.wait[1][1])), run_time=0.5)
        self.at("next to the")
        self.play(*jglow(jL, 1.06), *jglow(jR, 1.06), run_time=0.7)
        self.outro(FadeOut(cyto))


# ---------------------------------------------------------------------------------------------
class S05Grip(Film):
    """one phosphate on each STAT; the same SH2 cup now holds a partner: two grips instead of one. (MID)"""

    def construct(self):
        L = MID
        mem, cyt, chL, chR, jL, jR, pL, pR = complex_on(L)
        tp = [pbadge(L.k).move_to(L.dock(s)) for s in (-1, 1)]
        sA, sB = stat(L, L.docked(-1)), stat(L, L.docked(1))
        self.add(mem, chL, chR, jL, jR, cyt, pL, pR, *tp, sA, sB)

        # the JAK phosphorylates the docked STAT on its one tyrosine
        pa = pbadge(L.k).move_to([sA.tip.get_center()[0], L.jak_y - 0.3 * L.k, 0])      # each starts at the JAK just above
        pb = pbadge(L.k).move_to([sB.tip.get_center()[0], L.jak_y - 0.3 * L.k, 0])
        self.at("adds one phosphate")
        self.play(FadeIn(pa, scale=0.5), run_time=0.2)
        self.play(pa.animate.move_to(sA.tip.get_center()), run_time=0.5)
        self.play(FadeIn(pb, scale=0.5), run_time=0.2)
        self.play(pb.animate.move_to(sB.tip.get_center()), run_time=0.5)
        self.remove(pa, pb)          # from here each badge belongs to its STAT
        give_p(sA, pa)
        give_p(sB, pb)
        tyr = T("a single tyrosine", 26, TEAL).next_to(sB.tip.get_center() + RIGHT * L.pr, RIGHT, buff=0.3)
        self.at("on a single")
        self.play(FadeIn(tyr, shift=LEFT * 0.1), pop(pa, 1.4), pop(pb, 1.4), run_time=0.7)

        self.at("Now the same")
        self.play(FadeOut(tyr), Indicate(sA.cup, color=TEXT, scale_factor=1.3), Indicate(sB.cup, color=TEXT, scale_factor=1.3), run_time=0.8)
        # let go of the receptor
        self.at("something new to")
        self.play(sA.animate.shift(DOWN * (L.docked(-1)[1] - L.pair_y)), sB.animate.shift(DOWN * (L.docked(1)[1] - L.pair_y)), run_time=0.7)
        # turn to face each other
        gap = 0.4 * L.k
        self.at("loose pairs")
        self.play(spin_move(sA, -PI / 2, L.pair(-1) + LEFT * gap), spin_move(sB, PI / 2, L.pair(1) + RIGHT * gap), run_time=1.0)
        self.at("this grip")
        self.play(sA.animate.shift(RIGHT * gap), sB.animate.shift(LEFT * gap), run_time=0.5)
        self.play(Indicate(sA.cup, color=TEXT, scale_factor=1.25), pop(sB.p, 1.3), run_time=0.6)      # grip one
        self.at("each domain")
        self.play(Indicate(sB.cup, color=TEXT, scale_factor=1.25), pop(sA.p, 1.3), run_time=0.7)      # grip two

        two = T("two grips", 30, PINK, weight=BOLD).next_to([L.pair(1)[0] + 0.55 * L.k, L.pair_y, 0], RIGHT, buff=0.45)
        self.at("Two grips hold")
        self.play(FadeIn(two, shift=LEFT * 0.1), Indicate(sA.cup, color=TEXT, scale_factor=1.2),
                  Indicate(sB.cup, color=TEXT, scale_factor=1.2), run_time=0.7)
        gL, gR = ghost_cup(L, L.dock(-1)), ghost_cup(L, L.dock(1))
        one = T("one grip", 28, PINK).next_to(L.dock(-1) + LEFT * 0.34 * L.k, LEFT, buff=0.35)
        self.at("where one grip")
        self.play(FadeIn(one, shift=RIGHT * 0.1), FadeIn(gL), FadeIn(gR), run_time=0.6)
        self.at("to the receptor")
        self.play(pop(tp[0], 1.35), pop(tp[1], 1.35), run_time=0.6)
        twice = T("one domain, used twice", 26, PINK).move_to([4.1, -1.0, 0])
        self.at("same domain is")
        self.play(FadeIn(twice, shift=UP * 0.1), Indicate(sA.cup, color=TEXT, scale_factor=1.2),
                  Indicate(sB.cup, color=TEXT, scale_factor=1.2), run_time=0.8)
        # pull back to the whole cell (WIDE): the nucleus comes back, because the pair is going there
        W = WIDE
        m2, c2, chL2, chR2, jL2, jR2, pL2, pR2 = complex_on(W)
        tp2 = [pbadge(W.k).move_to(W.dock(s)) for s in (-1, 1)]
        sA2, sB2 = posed(W, W.pair(-1), -PI / 2), posed(W, W.pair(1), PI / 2)
        nuc = nucleus()
        self.outro(FadeOut(two), FadeOut(one), FadeOut(gL), FadeOut(gR), FadeOut(twice),
                   then=reframe([mem, cyt, chL, chR, jL, jR, pL, pR, *tp, sA, sB],
                                  [m2, c2, chL2, chR2, jL2, jR2, pL2, pR2, *tp2, sA2, sB2]),
                   after=[FadeIn(nuc, shift=UP * 0.3)])


# ---------------------------------------------------------------------------------------------
class S06Gene(Film):
    """the pair goes to the DNA; between receptor and gene there is one protein. (WIDE)"""

    def construct(self):
        L = WIDE
        mem, cyt, chL, chR, jL, jR, pL, pR = complex_on(L)
        nuc = nucleus()
        tp = [pbadge(L.k).move_to(L.dock(s)) for s in (-1, 1)]
        sA, sB = posed(L, L.pair(-1), -PI / 2), posed(L, L.pair(1), PI / 2)
        pair = VGroup(sA, sB)
        self.add(mem, nuc, chL, chR, jL, jR, cyt, pL, pR, *tp, pair)

        self.at("enters the")
        self.play(pair.animate.shift(DOWN * (L.pair_y - BOUND_Y)), run_time=0.95)
        site = Line([-1.45, DNA_Y, 0], [1.45, DNA_Y, 0], color=TEXT, stroke_width=10)
        seq = T("specific sequence", 22, TEXT).move_to([-2.9, -2.85, 0])
        self.at("binds a specific")
        self.play(Create(site), FadeIn(seq), run_time=0.6)
        ga = gene_arrow()
        tr = T("transcription on", 24, GREEN).move_to(nuc.gene_lbl)
        self.at("and switches on")
        self.play(nuc.gene.animate.set_fill(GREEN), GrowArrow(ga), ReplacementTransform(nuc.gene_lbl, tr), run_time=0.8)

        # count what lies between the receptor complex and the gene: one kind of protein
        X = -4.2
        rc = bchip("receptor complex", BLUE, 24).move_to([X, 1.15, 0])
        gn = bchip("gene", GREEN, 24).move_to([X, -1.35, 0])
        st = bchip("STAT relay", TEAL, 24).move_to([X, -0.1, 0])
        track = DashedLine(rc.get_bottom(), gn.get_top(), color=GREY, stroke_width=4, dash_length=0.1)
        self.at("count the proteins")
        self.play(FadeIn(rc[0]), FadeIn(gn[0]), Create(track), run_time=0.6)
        self.at("between the receptor")
        self.play(FadeIn(VGroup(rc[1], rc[2]), shift=DOWN * 0.1), run_time=0.4)
        self.at("and the gene")
        self.play(FadeIn(VGroup(gn[1], gn[2]), shift=UP * 0.1), run_time=0.4)
        a1, a2 = arr(rc.get_bottom(), st.get_top(), GREY), arr(st.get_bottom(), gn.get_top(), GREY)
        self.at("There is one")
        self.play(FadeOut(track), FadeIn(st, scale=0.7), GrowArrow(a1), GrowArrow(a2),
                  *glow(sA.body, sB.body, s=1.06), run_time=0.5)
        self.play(pop(st, 1.12), run_time=0.35)

        # the longer routes this pathway does not use
        sm = ghost_chip("second messenger").move_to([4.1, 1.2, 0])
        x1 = strike(sm)
        self.at("no second messenger")
        self.play(FadeIn(sm), run_time=0.3)
        self.play(Create(x1), run_time=0.3)
        ks = VGroup(*[ghost_chip("kinase") for _ in range(3)]).arrange(DOWN, buff=0.3).move_to([4.1, -0.65, 0])
        ka = VGroup(*[arr(ks[i].get_bottom(), ks[i + 1].get_top(), GREY, w=4, tip=0.14) for i in range(2)])
        x2 = strike(ks)
        self.at("no chain of")
        self.play(FadeIn(ks), FadeIn(ka), run_time=0.35)
        self.play(Create(x2), run_time=0.3)
        self.at("already waiting")
        self.play(FadeOut(VGroup(sm, x1, ks, ka, x2)), run_time=0.4)
        ck = clock([4.1, 0.1, 0])
        mins = T("minutes", 24, GREY).move_to([4.1, -0.7, 0])
        self.at("within minutes")
        self.play(FadeIn(ck), FadeIn(mins), run_time=0.3)
        self.play(Rotate(ck.hand, -TAU / 5, about_point=ck.c), run_time=0.6)

        # the rule
        self.at("keep this rule")
        self.play(*glow(sA.body, sB.body, sA.label, sB.label, s=1.08), *glow(st[1], st[2], s=1.08), run_time=0.55)
        self.at("with one phosphate")
        self.play(pop(sA.p, 1.6), pop(sB.p, 1.6), run_time=0.7)
        sigarrow = Arrow([0, -0.05, 0], [0, -1.98, 0], buff=0, color=GREEN, stroke_width=7, tip_length=0.26)
        self.at("carries the signal")
        self.play(GrowArrow(sigarrow), run_time=0.9)
        self.at("to gene")
        self.play(*glow(nuc.gene, s=1.1), *glow(tr, s=1.08), *glow(gn[1], gn[2], s=1.12), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A Stat, with one phosphate, carries the signal from receptor to gene."
