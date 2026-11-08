"""TGF-beta and Smads: the ligand only introduces two kinases  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the ligand, TGF-beta
  BLUE   = type II receptor
  ORANGE = type I receptor
  PURPLE = the GS domain, the stretch of type I that type II phosphorylates
  TAN    = FKBP12, the small protein that sits on the GS domain
  GOLD   = a phosphate (the round "P" badge)
  GREEN  = active / on (kinase outline, a gene being read)
  TEAL   = Smads and the Smad complex (and the docking slot they fit)
  PINK   = partner proteins
  RED    = "stops dividing"
  GREY   = membrane, nucleus, DNA, inactive kinases, labels, parts not yet known

No molecular structures: receptors are bars with a labelled kinase blob, the Smad is a labelled
blob with a tail, a phosphate is a "P" badge, DNA is a line with ticks, a gene is a block on it.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F2994A"
TAN = "#C9A66B"
TEAL_S = "#3FB8C0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=36, w=1.0, h=0.85):
    """a dashed grey chip with a question mark: a part nobody has named yet."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h)
    return VGroup(DashedVMobject(box, num_dashes=24).set_color(GREY), t)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dashed_arr(a, b, color=GREY):
    a, b = np.array(a, float), np.array(b, float)
    line = DashedLine(a, b - (b - a) / np.linalg.norm(b - a) * 0.16, color=color, stroke_width=5, dash_length=0.15)
    d = (b - a) / np.linalg.norm(b - a)
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.11).rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(b - d * 0.1)
    return VGroup(line, tip)


def pbadge(k=1.0):
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def membrane(y, h=0.34):
    return RoundedRectangle(corner_radius=0.1, width=12.6, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, y, 0])


def glow(*mobs, s=1.1, color=None):
    """pulse each mobject in place (one animation per mobject). No recolour unless a colour is given."""
    if color is None:
        return [m.animate(rate_func=there_and_back).scale(s) for m in mobs]
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


# ---------------------------------------------------------------------------------------------
# receptors
# ---------------------------------------------------------------------------------------------
def rchain(kind, x, ym, k, show_label=True, lsize=24):
    """One receptor chain crossing the membrane once, with a kinase blob on its inner tail.

    kind "II": bar runs to the blob.   kind "I": the last stretch of the tail is the GS domain (g.gs).
    """
    col = BLUE if kind == "II" else ORANGE
    w = 0.3 * k
    top, mid, bot = ym + 0.6 * k, ym - 0.35 * k, ym - 1.35 * k
    stroke = 3

    def seg(y0, y1, name_col):
        back = Rectangle(width=w, height=y0 - y1, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, (y0 + y1) / 2, 0])
        body = RoundedRectangle(corner_radius=0.1 * k, width=w, height=y0 - y1, stroke_color=name_col, stroke_width=stroke,
                                fill_color=name_col, fill_opacity=0.4).move_to([x, (y0 + y1) / 2, 0])
        return VGroup(back, body)

    if kind == "II":
        bar = seg(top, bot + 0.05, col)
        gs = None
    else:
        bar = seg(top, mid, col)
        gs = seg(mid, bot + 0.05, col)
    bw, bh = 1.5 * k, 0.8 * k
    bc = np.array([x, bot - bh / 2 + 0.02, 0])
    bback = RoundedRectangle(corner_radius=0.3 * k, width=bw, height=bh, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(bc)
    blob = RoundedRectangle(corner_radius=0.3 * k, width=bw, height=bh, stroke_color=GREY, stroke_width=4,
                            fill_color=col, fill_opacity=0.3).move_to(bc)
    lbl = T("type " + kind, lsize, col, weight=BOLD).move_to(bc)
    if not show_label:
        lbl.set_opacity(0)
    parts = [bar, bback, blob, lbl] if gs is None else [bar, gs, bback, blob, lbl]
    g = VGroup(*parts)
    g.bar, g.gs, g.blob, g.lbl, g.kind, g.k, g.x = bar, gs, blob, lbl, kind, k, x
    g.top, g.mid, g.bot = top, mid, bot
    return g


def wide_chip(text, color, w, size=30, h=0.78):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, box, T(text, size, color))


def dimer(x, y, k):
    """the ligand: two chains joined, a yellow pair of lobes."""
    lw, lh = 1.3 * k, 0.62 * k
    l1 = RoundedRectangle(corner_radius=0.16, width=lw, height=lh, stroke_color=YELLOW, stroke_width=3,
                          fill_color=YELLOW, fill_opacity=0.3).move_to([x - lw / 2 - 0.02, y, 0])
    l2 = RoundedRectangle(corner_radius=0.16, width=lw, height=lh, stroke_color=YELLOW, stroke_width=3,
                          fill_color=YELLOW, fill_opacity=0.3).move_to([x + lw / 2 + 0.02, y, 0])
    link = Line([x - 0.15, y, 0], [x + 0.15, y, 0], color=YELLOW, stroke_width=7)
    back = Rectangle(width=2 * lw + 0.04, height=lh, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    lab = T("TGF-β", 26, YELLOW, weight=BOLD).move_to([x, y + lh / 2 + 0.34, 0])
    g = VGroup(back, l1, l2, link, lab)
    g.l1, g.l2, g.lab = l1, l2, lab
    return g


K2, YM2 = 1.5, 0.7         # scene 2 and 3 framing
II_X, I_X = 1.3, 3.7        # where the chains finish in scene 2
I_START = 5.0
DIM_Y = YM2 + 0.6 * K2 + 0.31 * K2     # the dimer resting on the type II bars


def activate(g):
    return g.blob.animate.set_stroke(GREEN, 6)


def complex2(final=True, labels=True):
    """four chains, membrane, ligand, as scene 2 leaves them."""
    mem = membrane(YM2)
    iiL, iiR = rchain("II", -II_X, YM2, K2, labels), rchain("II", II_X, YM2, K2, labels)
    ix = I_X if final else I_START
    iL, iR = rchain("I", -ix, YM2, K2, labels), rchain("I", ix, YM2, K2, labels)
    return mem, iiL, iiR, iL, iR


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "TGF-β and Smads"
    TITLE = "The ligand only introduces two kinases"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a protein named for one job; the path from membrane to gene is unknown."""

    def construct(self):
        mem_y = 1.55
        mem = membrane(mem_y)
        env = RoundedRectangle(corner_radius=0.5, width=11.6, height=2.1, stroke_color=GREY, stroke_width=3).move_to([0, -2.4, 0])
        dna = Line([-4.0, -2.9, 0], [5.0, -2.9, 0], color=GREY, stroke_width=6)
        gene = Rectangle(width=1.8, height=0.24, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([0, -2.9, 0])
        nuc_l = T("nucleus", 24, GREY).move_to([-4.8, -1.85, 0])
        dna_l = T("DNA", 24, GREY).move_to([-4.85, -2.9, 0])
        gene_l = T("gene", 26, GREY).move_to([0, -3.3, 0])
        mem_l = T("cell membrane", 24, GREY).move_to([-4.7, mem_y - 0.5, 0])
        world = VGroup(mem, env, dna, gene, nuc_l, dna_l, gene_l, mem_l)

        prot = bchip("a protein", GREY, size=34, pad=0.22).move_to([0, 2.6, 0])
        self.play(FadeIn(world), run_time=0.5)
        self.at("Scientists purified")
        self.play(FadeIn(prot, shift=DOWN * 0.3), run_time=0.5)

        tag1 = T("grows with EGF", 28).move_to([-4.3, 2.6, 0])
        a1 = arr([-1.3, 2.6, 0], [-2.0, 2.6, 0], GREY, 4, 0.18)
        self.at("grow like")
        self.play(FadeIn(tag1, shift=RIGHT * 0.2), GrowArrow(a1), run_time=0.5)

        lig = bchip("TGF-β", YELLOW, size=34, pad=0.22).move_to(prot)
        nm = T("transforming growth factor β", 26, YELLOW).move_to([0, 3.3, 0])
        self.at("named it")
        self.play(Transform(prot, lig), FadeIn(nm, shift=DOWN * 0.1), run_time=0.6)

        tag2 = T("holds cells back", 28).move_to([4.2, 2.6, 0])
        a2 = arr([1.3, 2.6, 0], [2.0, 2.6, 0], GREY, 4, 0.18)
        self.at("holding other cells")
        self.play(FadeIn(tag2, shift=LEFT * 0.2), GrowArrow(a2), run_time=0.5)

        self.at("What does")
        self.play(*glow(tag1, tag2, s=1.12), run_time=0.5)
        self.play(FadeOut(tag1), FadeOut(tag2), FadeOut(a1), FadeOut(a2), FadeOut(nm), run_time=0.4)
        self.at("once it lands")
        self.play(prot.animate.move_to([0, mem_y + 0.72, 0]), run_time=0.7)

        q1 = ghost_chip("?", 48, 1.6, 0.95).move_to([0, 0.45, 0])
        q2 = ghost_chip("?", 48, 1.6, 0.95).move_to([0, -0.8, 0])
        d0 = dashed_arr([0, mem_y - 0.2, 0], [0, 0.95, 0])
        d1 = dashed_arr([0, -0.07, 0], [0, -0.27, 0])
        d2 = dashed_arr([0, -1.3, 0], [0, -2.7, 0])
        self.at("Follow its message")
        self.play(FadeIn(d0), FadeIn(q1), run_time=0.4)
        self.play(FadeIn(d1), FadeIn(q2), run_time=0.4)
        self.at("to a gene")
        self.play(FadeIn(d2), Indicate(gene, color=TEXT, scale_factor=1.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Four(SpokenScene):
    """two kinds of receptor kinase; the ligand brings four chains around one dimer."""

    def construct(self):
        mem, iiL, iiR, iL, iR = complex2(final=False, labels=False)
        chains = [iiL, iiR, iL, iR]
        self.play(FadeIn(mem), *[FadeIn(c) for c in chains], run_time=0.8)

        self.at("two types")
        self.play(*[c.lbl.animate.set_opacity(1) for c in chains], run_time=0.5)

        self.at("active before")
        self.play(activate(iiL), activate(iiR), run_time=0.5)
        self.play(*glow(iiL.blob, iiR.blob, s=1.1), run_time=0.5)

        d = dimer(0, DIM_Y + 0.7, K2)
        self.at("is a dimer")
        self.play(FadeIn(d, shift=DOWN * 0.3), run_time=0.6)
        self.at("two chains")
        self.play(*glow(d.l1, d.l2, s=1.1), run_time=0.7)

        self.at("It binds")
        self.play(d.animate.shift(DOWN * 0.7), run_time=0.6)
        self.at("receptors", nth=1)
        self.play(*glow(iiL.bar, iiR.bar, s=1.15), run_time=0.7)

        self.at("recruit two")
        self.play(iL.animate.shift(RIGHT * (I_START - I_X)), iR.animate.shift(LEFT * (I_START - I_X)), run_time=1.1)

        self.at("Four receptor")
        self.play(*glow(iiL.bar, iiR.bar, iL.bar, iR.bar, s=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Match(SpokenScene):
    """type II puts phosphate on the GS domain of type I; FKBP12 comes off; the kinase turns on."""

    def construct(self):
        mem, iiL, iiR, iL, iR = complex2(final=True)
        d = dimer(0, DIM_Y, K2)
        for c in (iiL, iiR):
            c.blob.set_stroke(GREEN, 6)
        self.add(mem, iiL, iiR, iL, iR, d)
        self.wait(0.15)

        # zoom to one type II / type I pair (same parts, bigger)
        k3, ym3 = 2.0, 1.4
        mem3 = membrane(ym3)
        iiN = rchain("II", -1.6, ym3, k3, True, 30)
        iN = rchain("I", 1.6, ym3, k3, True, 30)
        iiN.blob.set_stroke(GREEN, 6)
        lig = wide_chip("TGF-β", YELLOW, 4.2, 32).move_to([0, iiN.top + 0.32, 0])
        self.play(FadeOut(iiL), FadeOut(iL), FadeOut(d), ReplacementTransform(iiR, iiN), ReplacementTransform(iR, iN),
                  ReplacementTransform(mem, mem3), FadeIn(lig), run_time=0.9)
        iiR, iR = iiN, iN
        ix = 1.6
        gs_y = (iR.mid + iR.bot) / 2
        pb = pbadge(1.4).move_to(iiR.blob.get_top() + RIGHT * 0.9)

        self.at("adds phosphate")
        self.play(FadeIn(pb, scale=0.4), *glow(iiR.blob, s=1.06), run_time=0.5)

        gs_lbl = T("GS domain", 28, PURPLE, weight=BOLD).move_to([4.5, iR.mid + 0.05, 0])
        leader = Line([3.5, iR.mid + 0.05, 0], [ix + 0.2, iR.mid - 0.2, 0], color=PURPLE, stroke_width=3)
        self.at("a stretch")
        self.play(iR.gs[1].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.55), run_time=0.5)
        self.at("called the")
        self.play(FadeIn(gs_lbl), Create(leader), run_time=0.5)

        # at rest the GS stretch holds the kinase inactive
        off = T("inactive", 26, GREY).move_to(iR.blob.get_bottom() + DOWN * 0.38)
        self.at("At rest")
        self.play(FadeIn(off), run_time=0.4)
        self.at("inactive shape")
        self.play(*glow(iR.blob, s=1.05), run_time=0.6)

        # the phosphate crosses
        self.at("Phosphate ends")
        target = np.array([ix + 0.0, iR.mid - 0.3, 0])
        path = ArcBetweenPoints(pb.get_center(), target, angle=-0.9)
        self.play(MoveAlongPath(pb, path), run_time=0.9)
        self.at("arrangement")
        self.play(FadeOut(off), run_time=0.4)

        slot = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.6, height=1.3).move_to([ix + 0.3 + 0.1 + 0.8, gs_y, 0]),
                              num_dashes=34).set_color(TEAL_S)
        slot_l = T("docking\nsite", 28, TEAL_S, line_spacing=0.8).move_to([5.0, gs_y - 0.2, 0])
        self.at("kinase turns on")
        self.play(activate(iR), run_time=0.5)
        self.play(*glow(iR.blob, s=1.06), run_time=0.4)
        self.at("docking site")
        self.play(Create(slot), FadeIn(slot_l), run_time=0.6)

        self.at("lit match")
        self.play(*glow(iiR.blob, s=1.06, color=YELLOW), run_time=0.7)
        self.at("as a fuse")
        self.play(*glow(iR.blob, s=1.06, color=YELLOW), run_time=0.7)
        self.at("holds the match")
        self.play(*glow(lig, s=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
K4, YM4 = 1.4, 2.4
II4, I4 = 1.17, 3.4


def smad(center, side, label="Smad", dock=True, fill=0.3):
    """A Smad: labelled blob with a tail on its inner edge (toward the centre line) and a pocket
    on the same edge. side=+1 for the right-hand Smad, -1 for the left. The tail sits low on the
    right Smad and high on the left; the pocket is opposite, so two Smads interlock."""
    c = np.array(center, float)
    s = -side                        # direction from the body toward the centre line
    body = RoundedRectangle(corner_radius=0.25, width=1.5, height=0.9, stroke_color=TEAL_S, stroke_width=3,
                            fill_color=TEAL_S, fill_opacity=fill).move_to(c)
    back = RoundedRectangle(corner_radius=0.25, width=1.5, height=0.9, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    lbl = T(label, 24, TEAL_S, weight=BOLD).move_to(c)
    ty = -0.22 * side
    edge = c + np.array([s * 0.75, ty, 0])
    tail = Line(edge, edge + np.array([s * 0.9, 0, 0]), color=TEAL_S, stroke_width=6)
    tip = edge + np.array([s * 0.9, 0, 0])
    p1 = pbadge(1.0).move_to(edge + np.array([s * 0.5, 0, 0]))
    p2 = pbadge(1.0).move_to(tip)
    pc = c + np.array([s * 0.75, -ty, 0])
    pocket = Sector(radius=0.26, angle=PI, start_angle=(-PI / 2 if s < 0 else PI / 2), fill_color=BG, fill_opacity=1,
                    stroke_color=TEAL_S, stroke_width=3).move_to(pc)
    pocket.move_arc_center_to(pc)
    g = VGroup(back, body, lbl, tail)
    g.body, g.lbl, g.tail, g.p1, g.p2, g.pocket, g.c, g.s = body, lbl, tail, p1, p2, pocket, c, s
    g.tip = tip
    return g


def mating(side):
    """final complex position of a Smad."""
    return np.array([side * 1.2, -1.4, 0])


class S04Smad(SpokenScene):
    """type I phosphorylates a Smad on two serines; two Smads and one Smad4 form the complex."""

    def construct(self):
        mem = membrane(YM4)
        ch = {}
        for name, kind, x in (("iiL", "II", -II4), ("iiR", "II", II4), ("iL", "I", -I4), ("iR", "I", I4)):
            ch[name] = rchain(kind, x, YM4, K4)
            ch[name].blob.set_stroke(GREEN, 6)
        iL, iR = ch["iL"], ch["iR"]
        for r in (iL, iR):
            r.gs[1].set_stroke(PURPLE).set_fill(PURPLE, 0.55)
        gs_y = (iR.mid + iR.bot) / 2
        slots = []
        for sd in (-1, 1):
            sl = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.5, height=1.0).move_to([sd * (I4 + 0.17 + 0.75 + 0.1), gs_y, 0]),
                                num_dashes=30).set_color(TEAL_S)
            slots.append(sl)
        self.play(FadeIn(mem), *[FadeIn(c) for c in ch.values()], *[FadeIn(s) for s in slots], run_time=0.7)

        # Smads dock: the tail's tip meets the GS stretch
        sR = smad([I4 + 0.2 + 0.05 + 0.9 + 0.75, gs_y + 0.22, 0], +1)
        sL = smad([-(I4 + 0.2 + 0.05 + 0.9 + 0.75), gs_y - 0.22, 0], -1)
        self.at("phosphorylates a")
        self.play(FadeOut(slots[0]), FadeOut(slots[1]), FadeIn(sL, shift=RIGHT * 0.4), FadeIn(sR, shift=LEFT * 0.4), run_time=0.7)

        self.at("transcription factor")
        self.play(*glow(sL.body, sR.body, s=1.1), run_time=0.7)

        tagR = T("Smad2\nor Smad3", 22, TEAL_S, line_spacing=0.8).move_to([5.3, 0.1, 0])
        tagL = T("Smad2\nor Smad3", 22, TEAL_S, line_spacing=0.8).move_to([-5.3, 0.1, 0])
        self.at("receptors phosphorylate")
        self.play(FadeIn(tagL), FadeIn(tagR), run_time=0.5)

        # two serines: two phosphates fly from the type I kinase to each tail
        pbs = []
        for r, sm in ((iL, sL), (iR, sR)):
            for p in (sm.p1, sm.p2):
                b = pbadge(1.0).move_to(r.blob.get_top() + np.array([0, -0.05, 0]))
                b.target = p
                pbs.append(b)
        self.at("serines")
        self.add(*pbs)
        self.play(*[b.animate.move_to(b.target.get_center()) for b in pbs], run_time=0.9)
        for sm in (sL, sR):
            sm.add(sm.p1, sm.p2)
        self.remove(*pbs)
        self.add(sL, sR)

        self.at("A phosphorylated tail")
        self.play(*glow(sL.p1, sL.p2, sR.p1, sR.p2, s=1.2), run_time=0.6)
        self.at("fits a pocket")
        self.play(FadeOut(tagL), FadeOut(tagR), FadeIn(sL.pocket), FadeIn(sR.pocket), run_time=0.5)
        self.play(*glow(sL.pocket, sR.pocket, s=1.25), run_time=0.5)
        sL.add(sL.pocket)
        sR.add(sR.pocket)
        self.add(sL, sR)

        # leave the receptor, meet
        self.at("leave the receptor")
        endL, endR = mating(-1), mating(1)
        recept = VGroup(mem, *ch.values())
        dR, dL = sR.get_center() - sR.c, sL.get_center() - sL.c      # the group centre is not the body centre
        pathR = ArcBetweenPoints(sR.get_center(), endR + dR, angle=-0.5)
        pathL = ArcBetweenPoints(sL.get_center(), endL + dL, angle=0.5)
        self.play(recept.animate.set_opacity(0.1), run_time=0.4)
        self.play(MoveAlongPath(sR, pathR), MoveAlongPath(sL, pathL), run_time=1.5)

        s4 = smad([0, -2.65, 0], +1, "Smad4", fill=0.5)
        s4.remove(s4.tail)
        self.at("join one")
        self.play(FadeIn(s4, shift=UP * 0.4), run_time=0.7)
        self.play(*glow(sL.body, sR.body, s4.body, s=1.08), run_time=0.8)
        self.play(FadeOut(recept), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
TRIO_CY = 0.45
DNA_Y = -1.25


def trio(cx, cy=TRIO_CY):
    """the Smad complex in compact form: three discs and a label."""
    r = 0.4
    a = Circle(radius=r, stroke_color=TEAL_S, stroke_width=3, fill_color=TEAL_S, fill_opacity=0.35).move_to([cx - 0.46, cy + 0.26, 0])
    b = Circle(radius=r, stroke_color=TEAL_S, stroke_width=3, fill_color=TEAL_S, fill_opacity=0.35).move_to([cx + 0.46, cy + 0.26, 0])
    c = Circle(radius=r, stroke_color=TEAL_S, stroke_width=3, fill_color=TEAL_S, fill_opacity=0.55).move_to([cx, cy - 0.4, 0])
    lab = T("Smad complex", 24, TEAL_S).move_to([cx, cy + 1.0, 0])
    g = VGroup(a, b, c, lab)
    g.lab = lab
    return g


def legs(cx, firm=False, partners=(), targets=None):
    """lines from the complex (and its partners) down to the DNA. targets: x of genes the complex reaches."""
    y0 = TRIO_CY - 0.8
    if not firm:
        return VGroup(DashedLine([cx, y0, 0], [cx, DNA_Y, 0], color=TEAL_S, stroke_width=3, dash_length=0.12))
    ls = []
    for tx in (targets or [cx]):
        ls.append(Line([cx, y0, 0], [tx, DNA_Y + 0.1, 0], color=TEAL_S, stroke_width=6))
    for px in partners:
        ls.append(Line([px, TRIO_CY - 0.5, 0], [px, DNA_Y, 0], color=PINK, stroke_width=6))
    return VGroup(*ls)


def partner_chip(text, x):
    return bchip(text, PINK, size=24, pad=0.14).move_to([x, TRIO_CY - 0.2, 0])


class S05Partners(SpokenScene):
    """the Smad complex reads a short site weakly; partners decide the gene, case by case."""

    def construct(self):
        # start where scene 4 ended
        sL = smad(mating(-1), -1)
        sR = smad(mating(1), +1)
        for sm in (sL, sR):
            sm.add(sm.p1, sm.p2)
            sm.add(sm.pocket)
        s4 = smad([0, -2.65, 0], +1, "Smad4", fill=0.5)
        s4.remove(s4.tail)
        old = VGroup(sL, sR, s4)
        self.add(old)
        self.wait(0.15)

        env = RoundedRectangle(corner_radius=0.5, width=12.4, height=6.7, stroke_color=GREY, stroke_width=3).move_to([0, 0.0, 0])
        nuc_l = T("nucleus", 24, GREY).move_to([-5.3, 2.95, 0])
        self.at("in the nucleus")
        self.play(Create(env), FadeIn(nuc_l), run_time=0.8)

        # DNA with many identical short sites
        dna = Line([-5.7, DNA_Y, 0], [5.7, DNA_Y, 0], color=GREY, stroke_width=6)
        xs = np.linspace(-5.3, 5.3, 19)
        ticks = VGroup(*[Line([x, DNA_Y, 0], [x, DNA_Y + 0.35, 0], color=GREY, stroke_width=4) for x in xs])
        dna_l = T("DNA", 24, GREY).move_to([-5.2, DNA_Y - 0.4, 0])
        tr = trio(0)
        self.at("and binds")
        self.play(FadeOut(old), FadeIn(dna), FadeIn(ticks), FadeIn(dna_l), FadeIn(tr), run_time=0.9)
        lg = legs(0)
        self.play(Create(lg), run_time=0.3)

        four = T("a few base pairs", 26, TEXT).move_to([0, DNA_Y - 0.75, 0])
        hit = ticks[9]
        self.at("few base pairs")
        self.play(FadeIn(four), hit.animate.set_color(TEXT).set_stroke(width=9), run_time=0.5)

        # weak: the complex slides about
        self.at("holds it weakly")
        for hx in [-2.4, 1.4, -0.8, 0.0]:
            self.play(tr.animate.move_to([hx, tr.get_center()[1], 0]), Transform(lg, legs(hx)), run_time=0.35)

        many = T("the same short site, millions of times in a genome", 26, TEXT).move_to([0, DNA_Y - 0.75, 0])
        self.at("millions of times")
        self.play(FadeOut(four), FadeIn(many), *[t.animate.set_color(TEXT) for t in ticks if t is not hit], run_time=0.6)
        self.wait(0.4)
        self.play(*[t.animate.set_color(GREY) for t in ticks if t is not hit], hit.animate.set_color(GREY).set_stroke(width=4), run_time=0.4)

        # genes: two blocks, unnamed
        G1X, G2X, CLX = -3.9, -2.1, -3.0
        g1 = Rectangle(width=1.1, height=0.26, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([G1X, DNA_Y, 0])
        g2 = Rectangle(width=1.1, height=0.26, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([G2X, DNA_Y, 0])
        q1 = T("?", 44, GREY).move_to([G1X, DNA_Y + 0.7, 0])
        q2 = T("?", 44, GREY).move_to([G2X, DNA_Y + 0.7, 0])
        self.at("pick a gene")
        self.play(FadeOut(many), FadeIn(g1), FadeIn(g2), FadeIn(q1), FadeIn(q2), run_time=0.6)

        # partners: firm grip
        pa = partner_chip("partner A", -2.1)
        pb_ = partner_chip("partner B", 2.1)
        self.at("partner proteins")
        self.play(tr.animate.move_to([0, tr.get_center()[1], 0]), Transform(lg, legs(0)), run_time=0.3)
        self.play(FadeIn(pa), FadeIn(pb_), FadeOut(q1), FadeOut(q2), run_time=0.5)
        self.play(Transform(lg, legs(0, True, (-2.1, 2.1))), run_time=0.4)
        self.at("its own partners")
        self.play(*glow(pa, pb_, s=1.1), run_time=0.7)

        # epithelial case
        cell = T("epithelial cell", 32, TEXT, weight=BOLD).move_to([0, 2.8, 0])
        self.at("epithelial cells")
        self.play(FadeIn(cell, shift=DOWN * 0.15), run_time=0.5)
        cluster = VGroup(tr, pa, pb_, lg)
        self.at("the partners")
        self.play(cluster.animate.shift(RIGHT * CLX), run_time=0.6)
        # re-draw the legs: the complex reaches both genes, the partners stand on their own sites
        newlg = legs(CLX, True, (-2.1 + CLX, 2.1 + CLX), (G1X, G2X))
        self.play(Transform(lg, newlg), run_time=0.2)
        lab1 = T("p15", 28, GREEN, weight=BOLD).move_to([G1X, DNA_Y - 0.5, 0])
        lab2 = T("p21", 28, GREEN, weight=BOLD).move_to([G2X, DNA_Y - 0.5, 0])
        self.at("turn on")
        self.play(FadeIn(lab1), g1.animate.set_fill(GREEN), run_time=0.5)
        self.at("and the cell")
        self.play(FadeIn(lab2), g2.animate.set_fill(GREEN), run_time=0.5)
        stop = T("stops dividing", 30, RED, weight=BOLD).move_to([CLX, 2.15, 0])
        self.at("stops dividing")
        self.play(FadeIn(stop, shift=DOWN * 0.1), run_time=0.5)

        # fibroblast case: clear every result first, in one move
        cell2 = T("fibroblast", 32, TEXT, weight=BOLD).move_to([0, 2.8, 0])
        tr2 = trio(0)
        self.at("In a fibroblast")
        self.play(FadeOut(cluster), FadeOut(stop), FadeOut(lab1), FadeOut(lab2), FadeOut(g1), FadeOut(g2),
                  FadeOut(cell), FadeIn(cell2), FadeIn(tr2), run_time=0.8)
        lg2 = legs(0)
        self.add(lg2)

        RX = 3.0
        pc = partner_chip("partner C", RX - 2.1)
        pd = partner_chip("partner D", RX + 2.1)
        g3 = Rectangle(width=2.0, height=0.26, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([RX, DNA_Y, 0])
        self.at("same pathway")
        self.play(FadeIn(g3), tr2.animate.move_to([RX, tr2.get_center()[1], 0]), Transform(lg2, legs(RX)), run_time=0.7)
        self.play(FadeIn(pc), FadeIn(pd), run_time=0.4)
        self.play(Transform(lg2, legs(RX, True, (RX - 2.1, RX + 2.1))), run_time=0.3)
        lab3 = T("collagen genes", 28, GREEN, weight=BOLD).move_to([RX, DNA_Y - 0.5, 0])
        self.at("collagen genes")
        self.play(FadeIn(lab3), g3.animate.set_fill(GREEN), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the whole relay in one row; the phosphate runs one way."""

    def construct(self):
        y = 0.4
        xs = [-4.7, -1.55, 1.55, 4.7]
        sz = 40
        lig = bchip("TGF-β", YELLOW, size=sz, pad=0.26).move_to([-3.1, 2.75, 0])
        c2 = bchip("type II", BLUE, size=sz, pad=0.26).move_to([xs[0], y, 0])
        c1 = bchip("type I", ORANGE, size=sz, pad=0.26).move_to([xs[1], y, 0])
        cs = bchip("Smad", TEAL_S, size=sz, pad=0.26).move_to([xs[2], y, 0])
        cg = bchip("genes", GREY, size=sz, pad=0.26).move_to([xs[3], y, 0])
        l2 = Line(lig.get_bottom() + LEFT * 0.5, c2.get_top(), color=YELLOW, stroke_width=5)
        l1 = Line(lig.get_bottom() + RIGHT * 0.5, c1.get_top(), color=YELLOW, stroke_width=5)

        self.at("The ligand brings")
        self.play(FadeIn(lig, shift=DOWN * 0.2), run_time=0.5)
        self.at("two kinases")
        self.play(FadeIn(c2), FadeIn(c1), Create(l2), Create(l1), run_time=0.7)
        self.at("together")
        self.play(*glow(c2, c1, s=1.06), run_time=0.7)

        a1 = arr(c2.get_right(), c1.get_left(), GREY, 6, 0.24)
        p = pbadge(1.4).move_to(c2.get_right() + RIGHT * 0.3)
        self.at("phosphorylates type")
        self.play(GrowArrow(a1), FadeIn(p, scale=0.5), run_time=0.5)
        self.play(p.animate.move_to(c1.get_left() + LEFT * 0.3), run_time=0.6)
        self.play(FadeOut(p), run_time=0.2)

        a2 = arr(c1.get_right(), cs.get_left(), GREY, 6, 0.24)
        p2 = pbadge(1.4).move_to(c1.get_right() + RIGHT * 0.3)
        self.at("phosphorylates a")
        self.play(GrowArrow(a2), FadeIn(cs), FadeIn(p2, scale=0.5), run_time=0.7)
        self.play(p2.animate.move_to(cs.get_left() + LEFT * 0.3), run_time=0.6)
        self.play(FadeOut(p2), run_time=0.2)

        self.at("one way")
        one = arr([-5.4, -1.0, 0], [2.4, -1.0, 0], GOLD, 8, 0.3)
        ow = T("the steps run one way", 30, GOLD).move_to([-1.5, -1.65, 0])
        self.play(GrowArrow(one), FadeIn(ow), run_time=0.8)

        a3 = arr(cs.get_right(), cg.get_left(), GREY, 6, 0.24)
        pa_ = bchip("partners", PINK, size=34, pad=0.22).move_to([3.1, -2.2, 0])
        pl = Line(pa_.get_top(), [3.1, y - 0.45, 0], color=PINK, stroke_width=5)
        self.at("In each cell")
        self.play(GrowArrow(a3), FadeIn(cg), run_time=0.5)
        self.at("the partners decide")
        self.play(FadeIn(pa_, shift=UP * 0.2), Create(pl), run_time=0.6)
        self.at("message of the")
        self.play(*glow(cs, s=1.1), run_time=0.7)

        self.at("Keep this rule")
        rest = [cs, cg, a2, a3, one, ow, pa_, pl, a1]
        self.play(*[m.animate.set_opacity(0.25) for m in rest], run_time=0.5)
        self.at("only introduces")
        self.play(*glow(lig, c2, c1, s=1.1, color=YELLOW), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "The ligand only introduces two kinases."
