"""Stress signals: made all day, held back until needed  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the responder (p53, NRF2): the protein that is made all the time
  GREEN  = the part of the responder that switches genes on, and genes that are switched on
  PURPLE = the restraint: the claw that grips the responder (MDM2, Keap1) and the "held back" outline
  RED    = destruction: the ubiquitin tag, the proteasome, the ubiquitin ligase, a blocked kinase
  ORANGE = stress: the DNA break, ATM, the reactive chemical
  TEAL   = what the switched-on genes make (p21, DNA repair, protective enzymes, cell death)
  GOLD   = a phosphate (the round "P" badge)
  GREY   = DNA, labels, parts that are not switched on

No molecular structures: the responder is a labelled pill with a small square for the part that
switches genes on, the restraint is a labelled box with two jaws that grip the pill's neck, a
phosphate is a "P" badge, ubiquitin is a "Ub" badge, DNA is a line and a gene is a block on it.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=22, color=GREY):
    """a dashed chip: something that is NOT used."""
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


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


def ubtag(k=1.0):
    """the ubiquitin tag."""
    c = Circle(radius=0.27 * k, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=1)
    return VGroup(c, T("Ub", 22 * k, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    """swell and settle, without recolouring."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation per mobject)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def dna_line(x0, x1, y, w=6):
    return Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=w)


def gene_block(x, y, w=1.8, color=GREY):
    return Rectangle(width=w, height=0.24, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0])


def gene_on(g, color=GREEN):
    return g.animate.set_fill(color)


# ---------------------------------------------------------------------------------------------
# the responder (a pill), the restraint (a box with two jaws), the destroyer (a box)
# ---------------------------------------------------------------------------------------------
def pill(name="p53", s=1.0, w=1.9, center=(0, 0, 0), patch=False):
    """The responder. [back, body, patch, label]. The square at the front (left) end is the part that
    switches genes on; it is invisible until `patch` is set, so a pill can morph into a bigger one."""
    cx, cy = float(center[0]), float(center[1])
    h, W = 0.8 * s, w * s
    back = RoundedRectangle(corner_radius=h / 2, width=W, height=h, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
    body = RoundedRectangle(corner_radius=h / 2, width=W, height=h, stroke_color=BLUE, stroke_width=3 * s ** 0.5,
                            fill_color=BLUE, fill_opacity=0.28).move_to([cx, cy, 0])
    px = cx - W / 2 + h / 2
    pt = RoundedRectangle(corner_radius=0.08 * s, width=0.44 * s, height=0.44 * s, stroke_color=GREEN,
                          stroke_width=3 * s ** 0.5, fill_color=GREEN, fill_opacity=0.35).move_to([px, cy, 0])
    if not patch:
        pt.set_stroke(opacity=0).set_fill(opacity=0)
    lab = T(name, min(34, max(24, 26 * s)), BLUE, weight=BOLD).move_to([(px + 0.22 * s + cx + W / 2) / 2, cy, 0])
    g = VGroup(back, body, pt, lab)
    g.body, g.patch, g.label, g.s, g.W, g.h = body, pt, lab, s, W, h
    return g


def patch_state(p, color, fill=0.35):
    """recolour the 'switches genes on' square (read lazily, so it is right wherever the pill has moved to)."""
    st = {}

    def upd(m, a):
        if not st:
            st.update(s=p.patch.get_stroke_color(), f=p.patch.get_fill_color(), so=p.patch.get_stroke_opacity(),
                      fo=p.patch.get_fill_opacity())
        p.patch.set_stroke(interpolate_color(st["s"], ManimColor(color), a), opacity=interpolate(st["so"], 1.0, a))
        p.patch.set_fill(interpolate_color(st["f"], ManimColor(color), a), opacity=interpolate(st["fo"], fill, a))
    return UpdateFromAlphaFunc(p, upd)


def claw(name, p, color=PURPLE):
    """The restraint, built to fit pill `p`: a box over the pill's front end, with two jaws on its neck.
    [box, label, jawT, jawB]."""
    s = p.s
    cx, cy = p.body.get_center()[0], p.body.get_center()[1]
    xL = cx - p.W / 2
    xR = xL + 0.8 * s
    bw, bh = 2.15 * s, 1.55 * s
    box = RoundedRectangle(corner_radius=0.22 * s, width=bw, height=bh, stroke_color=color, stroke_width=3 * s ** 0.5,
                           fill_color=color, fill_opacity=0.3).move_to([xR - bw / 2, cy, 0])
    lab = T(name, min(32, max(24, 26 * s)), color, weight=BOLD).move_to([(xR - bw + xL) / 2, cy, 0])
    jw, jh = 0.62 * s, 0.2 * s
    jT = RoundedRectangle(corner_radius=0.08 * s, width=jw, height=jh, stroke_color=color, stroke_width=2,
                          fill_color=color, fill_opacity=1).move_to([xR - 0.05 * s + jw / 2, cy + p.h / 2 + jh / 2, 0])
    jB = jT.copy().move_to([xR - 0.05 * s + jw / 2, cy - p.h / 2 - jh / 2, 0])
    g = VGroup(box, lab, jT, jB)
    g.box, g.label, g.jT, g.jB, g.s = box, lab, jT, jB, s
    return g


def _roots(c):
    s = c.s
    x = c.box.get_right()[0] - 0.05 * s
    y = c.box.get_center()[1]
    return np.array([x, y + 0.4 * s, 0]), np.array([x, y - 0.4 * s, 0])


def jaw_anims(c, ang, run=True):
    """swing both jaws open by `ang` radians (negative closes them again)."""
    rT, rB = _roots(c)
    return [c.jT.animate.rotate(ang, about_point=rT), c.jB.animate.rotate(-ang, about_point=rB)]


def set_jaws(c, ang):
    """open the jaws at once (no animation)."""
    rT, rB = _roots(c)
    c.jT.rotate(ang, about_point=rT)
    c.jB.rotate(-ang, about_point=rB)
    return c


def destroyer(text, color=RED, size=26, center=(0, 0, 0), w=None, h=None):
    """the proteasome / ubiquitin ligase: a red box that things disappear into."""
    c = bchip(text, color, size=size, pad=0.32)
    if w:
        for m in (c[0], c[1]):
            m.stretch_to_fit_width(w)
    if h:
        for m in (c[0], c[1]):
            m.stretch_to_fit_height(h)
    c.move_to([center[0], center[1], 0])
    return c


def feed(p, dest, run=1.0):
    """send a pill into a destroyer: it slides over, shrinks and disappears."""
    return AnimationGroup(p.animate.scale(0.25).move_to(dest).set_opacity(0), run_time=run)


def break_dna(x, y, x0=-6.1, x1=6.1, gap=0.62):
    """double-stranded DNA with a break across both strands, orange where it is cut."""
    strands = VGroup()
    for dy in (0.13, -0.13):
        strands.add(Line([x0, y + dy, 0], [x - gap / 2, y + dy, 0], color=GREY, stroke_width=5))
        strands.add(Line([x + gap / 2, y + dy, 0], [x1, y + dy, 0], color=GREY, stroke_width=5))
    zig = VMobject(color=ORANGE, stroke_width=5).set_points_as_corners(
        [[x - 0.12, y + 0.34, 0], [x + 0.1, y + 0.12, 0], [x - 0.1, y - 0.06, 0], [x + 0.12, y - 0.34, 0]])
    return VGroup(strands, zig)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Stress Signals"
    TITLE = "Made all day, held back until needed"


# ---------------------------------------------------------------------------------------------
GX = -2.35                                              # S01: the gene, and the middle of the grid under it
GRID_S = 1.1
GRID_COLS = [GX - 1.25, GX + 1.25]
GRID_ROWS = [1.8, 0.65, -0.5, -1.65]
DNA_Y = 2.85
SHIFT_C = 1.4                                           # S01 ends with its picture moved down this far
GRID = [(c, r) for r in GRID_ROWS for c in GRID_COLS]   # top row first


# ---------------------------------------------------------------------------------------------
class S01Why(SpokenScene):
    """a guardian is made all day and destroyed at once: why? It must already be there, and held back."""

    def construct(self):
        dna = dna_line(-6.0, 1.4, DNA_Y)
        gene = gene_block(GX, DNA_Y)
        gl = T("p53 gene", 24, GREY).move_to([GX, DNA_Y + 0.42, 0])
        self.play(Create(dna), FadeIn(gene), FadeIn(gl), run_time=0.5)

        # made all day long: the pills drop from the gene one after another
        pills = [pill("p53", GRID_S, center=(GX, DNA_Y - 0.35)) for _ in GRID]
        drops = [Succession(FadeIn(p, run_time=0.12), p.animate(run_time=0.5).move_to([x, y, 0]))
                 for p, (x, y) in zip(pills, GRID)]
        self.at("make a protein")
        self.play(LaggedStart(*drops, lag_ratio=0.38))

        # half of any batch is destroyed within about twenty minutes
        ck = clock([3.9, 1.5, 0], 0.85)
        mins = T("about 20 minutes", 26, GREY).move_to([3.9, 0.15, 0])
        dest = destroyer("destroyed", RED, 26, center=(GX, -3.0), w=5.0)
        self.at("Half of any")
        self.play(FadeIn(ck), FadeIn(dest), run_time=0.5)
        self.at("within about")
        gone = pills[4:]
        sweep = Rotate(ck.hand, -TAU / 3, about_point=ck.c, run_time=1.4, rate_func=linear)
        go = [Succession(Wait(0.35 + 0.1 * i), p.animate(run_time=0.3).set_color(RED), feed(p, dest.get_center(), 0.5))
              for i, p in enumerate(gone)]
        self.play(FadeIn(mins), sweep, *go)
        self.play(pop(dest, 1.06), run_time=0.3)

        # so why?
        q = T("?", 150, TEXT, weight=BOLD).move_to([3.9, 1.2, 0])
        self.at("So why build")
        self.play(FadeOut(ck), FadeOut(mins), run_time=0.3)
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.at("only to destroy")
        self.play(pop(dest, 1.06), Wiggle(q, scale_value=1.15, rotation_angle=0.04 * TAU), run_time=0.8)

        # because a cell in danger cannot wait for a gene to be read and a protein to be built
        brk = break_dna(3.9, 2.95, x0=2.4, x1=5.4, gap=0.7)
        danger = T("danger", 26, ORANGE, weight=BOLD).move_to([3.9, 2.3, 0])
        self.at("Because a cell")
        self.play(FadeOut(q), run_time=0.3)
        self.at("in danger")
        self.play(FadeIn(brk), FadeIn(danger), run_time=0.5)
        ck2 = clock([3.9, -0.75, 0], 0.55)
        cw = T("cannot wait", 28, RED, weight=BOLD).move_to([3.9, -1.75, 0])
        self.at("cannot wait")
        self.play(FadeIn(ck2), FadeIn(cw), Rotate(ck2.hand, -TAU * 0.8, about_point=ck2.c, run_time=1.2, rate_func=linear))
        read = bchip("read the gene", GREY, 24).move_to([3.9, 1.45, 0])
        built = bchip("build the protein", GREY, 24).move_to([3.9, 0.35, 0])
        step = arr(read.get_bottom(), built.get_top(), GREY)
        self.at("to be read")
        self.play(FadeIn(read, shift=DOWN * 0.1), run_time=0.4)
        self.at("protein to be built")
        self.play(GrowArrow(step), FadeIn(built, shift=DOWN * 0.1), run_time=0.4)

        # so it is already there, and held back, and only has to let go
        hold = RoundedRectangle(corner_radius=0.25, width=5.0, height=2.6, stroke_color=PURPLE, stroke_width=5,
                                fill_color=PURPLE, fill_opacity=0.08).move_to([GX, (GRID_ROWS[0] + GRID_ROWS[1]) / 2, 0])
        held = T("held back", 28, PURPLE, weight=BOLD).move_to([GX + 3.9, (GRID_ROWS[0] + GRID_ROWS[1]) / 2, 0])
        keep = VGroup(dna, gene, gl, *pills[:4])
        self.at("If the guardian")
        self.play(FadeOut(VGroup(brk, danger, ck2, cw, read, built, step, dest)), keep.animate.shift(DOWN * SHIFT_C), run_time=0.7)
        for m in (hold, held):
            m.shift(DOWN * SHIFT_C)
        self.at("already there")
        self.play(*[pop(p, 1.08) for p in pills[:4]], run_time=0.7)
        self.at("holds it back")
        self.play(Create(hold), FadeIn(held), run_time=0.6)
        self.at("let go")
        self.play(hold.animate.scale(1.35).set_stroke(opacity=0).set_fill(opacity=0), FadeOut(held),
                  *[pop(p, 1.12) for p in pills[:4]], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
PX, PY, PS = -1.2, 0.0, 2.2                              # S02 and S03: the big pill
PROT = (4.4, -1.8)                                       # and the proteasome


class S02Brake(SpokenScene):
    """p53 switches genes on; MDM2 grips its front end, covers that part and tags it; the proteasome destroys it."""

    def construct(self):
        # carry over S01's last picture, then move in on one pill
        dna = dna_line(-6.0, 1.4, DNA_Y - SHIFT_C)
        gene = gene_block(GX, DNA_Y - SHIFT_C)
        gl = T("p53 gene", 24, GREY).move_to([GX, DNA_Y - SHIFT_C + 0.42, 0])
        small = [pill("p53", GRID_S, center=(x, y - SHIFT_C)) for x, y in GRID[:4]]
        self.add(dna, gene, gl, *small)
        big = pill("p53", PS, center=(PX, PY))
        self.play(FadeOut(VGroup(dna, gene, gl, *small[1:])), ReplacementTransform(small[0], big), run_time=0.9)

        tf = T("transcription factor", 30, GREY).move_to([0.9, PY - 1.45, 0])
        self.at("transcription factor")
        self.play(FadeIn(tf, shift=UP * 0.1), run_time=0.5)

        # binds DNA and switches genes on
        pcx = big.patch.get_center()[0]
        GY = -3.1
        dna2 = dna_line(-6.0, 0.8, GY)
        gene2 = gene_block(pcx, GY, w=1.8)
        dl = T("DNA", 24, GREY).move_to([-5.4, GY + 0.4, 0])
        self.at("binds DNA")
        self.play(Create(dna2), FadeIn(gene2), FadeIn(dl), run_time=0.5)
        go = arr([pcx, PY - 1.05, 0], [pcx, GY + 0.2, 0], GREEN, w=6)
        sg = T("switches genes on", 28, GREEN, weight=BOLD).move_to([pcx + 2.35, -2.1, 0])
        self.at("switches genes on")
        self.play(patch_state(big, GREEN, 0.5), GrowArrow(go), FadeIn(sg, shift=RIGHT * 0.1), gene_on(gene2, GREEN), run_time=0.8)

        # its restraint: a claw that grips the front end
        mdm = claw("MDM2", big)
        set_jaws(mdm, 0.55)
        mdm.shift(LEFT * 1.4)
        self.at("Its restraint")
        self.play(FadeOut(VGroup(dna2, gene2, dl, go, sg, tf)), run_time=0.4)
        self.at("protein called")
        self.play(FadeIn(mdm, shift=RIGHT * 0.5), run_time=0.5)
        self.play(mdm.animate.shift(RIGHT * 1.4), run_time=0.7)
        self.at("grips a short")
        self.play(*jaw_anims(mdm, -0.55), run_time=0.45)
        self.play(pop(mdm[0], 1.03), run_time=0.5)
        self.at("That grip covers")
        under = T("part that switches genes on", 26, GREY).move_to([-3.2, -2.3, 0])
        lead = Line([pcx, -2.0, 0], [pcx, PY - 0.55, 0], color=GREY, stroke_width=3)
        self.play(patch_state(big, GREY, 0.3), FadeIn(under), Create(lead), run_time=0.7)

        # tagged with ubiquitin, and sent to the proteasome
        tag = ubtag(1.5).move_to([-1.9, PY + 1.5, 0])
        ul = T("ubiquitin", 30, RED, weight=BOLD).move_to([1.5, PY + 2.15, 0])
        tag_to = [big.body.get_right()[0] - 0.75, PY + 1.35, 0]
        self.at("It also tags")
        self.play(FadeOut(under), FadeOut(lead), FadeIn(tag, scale=0.6), run_time=0.4)
        self.play(tag.animate.move_to(tag_to), run_time=0.6)
        big.add(tag)
        self.at("with ubiquitin")
        self.play(FadeIn(ul, shift=DOWN * 0.1), run_time=0.4)
        prot = destroyer("proteasome", RED, 26, center=PROT, w=2.9, h=1.7)
        self.at("sends it")
        self.play(FadeIn(prot), *jaw_anims(mdm, 0.4), FadeOut(ul), run_time=0.5)
        self.at("proteasome")
        self.play(big.animate.scale(0.25).move_to(prot.get_center()).set_opacity(0), run_time=1.0, rate_func=smooth)
        self.at("destroyed")
        self.play(pop(prot, 1.08), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Release(SpokenScene):
    """a DNA break switches on ATM; phosphates land on MDM2 and on p53's front end; the grip loosens. (same stage as S02)"""

    def construct(self):
        p = pill("p53", PS, center=(PX, PY), patch=True)
        p.patch.set_stroke(GREY).set_fill(GREY, 0.3)             # covered, as S02 left it
        mdm = claw("MDM2", p)
        prot = destroyer("proteasome", RED, 26, center=PROT, w=2.9, h=1.7)
        a0 = np.array([p.body.get_right()[0] + 0.1, PY - 0.2, 0])
        a1 = np.array([prot.get_left()[0] - 0.05, PROT[1] + 0.15, 0])
        route = arr(a0, a1, RED, w=9, tip=0.3)
        rl = T("destruction", 26, RED).move_to([0.9, -1.15, 0])
        self.add(p, mdm, prot, route, rl)

        # a break across both strands
        dna = break_dna(4.5, 2.7, x0=-6.1, x1=6.1, gap=0.7)
        dl = T("DNA", 24, GREY).move_to([-5.6, 3.15, 0])
        both = T("across both strands", 24, ORANGE).move_to([4.2, 3.3, 0])
        self.play(FadeIn(dna[0]), FadeIn(dl), run_time=0.4)
        self.at("breaks")
        self.play(Create(dna[1]), Flash(np.array([4.5, 2.7, 0]), color=ORANGE, line_length=0.3, flash_radius=0.45, num_lines=10), run_time=0.6)
        self.at("both strands")
        self.play(FadeIn(both, shift=DOWN * 0.1), run_time=0.4)

        # ATM switches on, and the kinases beneath it
        atm = bchip("ATM", GREY, 28).move_to([4.5, 1.65, 0])
        kin = bchip("kinases", ORANGE, 26).move_to([4.5, 0.45, 0])
        a_dna = arr([4.5, 2.35, 0], atm.get_top() + UP * 0.02, ORANGE)
        a_atm = arr(atm.get_bottom(), kin.get_top(), ORANGE)
        self.at("That switches on")
        self.play(GrowArrow(a_dna), FadeIn(atm), run_time=0.5)
        self.at("called")
        self.play(atm[1].animate.set_stroke(ORANGE).set_fill(ORANGE, 0.16), atm[2].animate.set_color(ORANGE),
                  Flash(atm.get_center(), color=ORANGE, line_length=0.25, flash_radius=0.6, num_lines=10), run_time=0.5)
        self.at("beneath")
        self.play(GrowArrow(a_atm), FadeIn(kin), run_time=0.5)

        # phosphates land on MDM2, then on the front end of p53
        p1, p2 = pbadge(1.5).move_to(kin.get_left() + LEFT * 0.5), pbadge(1.5).move_to(kin.get_left() + LEFT * 0.5)
        d1 = np.array([-3.0, PY + 1.55, 0])
        d2 = p.patch.get_corner(UR) + np.array([0.12, 0.12, 0])
        arc1 = ArcBetweenPoints(p1.get_center(), d1, angle=-0.7)
        arc2 = ArcBetweenPoints(p2.get_center(), d2, angle=-0.45)
        self.at("add phosphates")
        self.play(FadeIn(p1, scale=0.5), run_time=0.2)
        self.play(MoveAlongPath(p1, arc1), run_time=0.9)
        mdm.add(p1)
        self.at("also add")
        self.play(FadeIn(p2, scale=0.5), run_time=0.2)
        self.play(MoveAlongPath(p2, arc2), run_time=0.9)
        p.add(p2)

        self.at("stretch")
        self.play(pop(p2, 1.4), run_time=0.6)
        self.at("grips")
        self.play(pop(mdm[0], 1.03), run_time=0.5)

        # the grip loosens, destruction slows
        self.at("grip loosens")
        self.play(*jaw_anims(mdm, 0.55), run_time=0.5)
        self.play(patch_state(p, GREEN, 0.5), mdm.animate.shift(LEFT * 2.4).set_opacity(0.0), run_time=1.0)
        thin = arr(a0, a1, GREY, w=3, tip=0.2)
        self.at("destruction slows")
        self.play(Transform(route, thin), FadeOut(rl), prot.animate.set_opacity(0.45), run_time=0.9)
        self.play(FadeOut(VGroup(dna, dl, both, atm, kin, a_dna, a_atm)), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
POOL = [(x, y) for y in (3.0, 2.15, 1.3) for x in (-4.4, -2.5, -0.6, 1.3)]
POOL_ORDER = [5, 6, 4, 7, 1, 2, 9, 10, 0, 3, 8, 11]       # the first pill is the one that was freed
XS = [-4.0, 0.0, 4.0]                                     # the three gene columns
DNA2_Y = -2.75


class S04Pileup(SpokenScene):
    """p53 piles up; freed, it switches on p21, DNA repair and, if the damage is severe, cell death genes."""

    def construct(self):
        # carry over S03's last picture: the freed pill, a thin road to the proteasome
        big = pill("p53", PS, center=(PX, PY), patch=True)
        prot = destroyer("proteasome", RED, 26, center=PROT, w=2.9, h=1.7).set_opacity(0.45)
        a0 = np.array([big.body.get_right()[0] + 0.1, PY - 0.2, 0])
        a1 = np.array([prot.get_left()[0] - 0.05, PROT[1] + 0.15, 0])
        thin = arr(a0, a1, GREY, w=3, tip=0.2)
        big.patch.set_stroke(GREEN).set_fill(GREEN, 0.5)
        self.add(big, prot, thin)
        pills = [pill("p53", 0.9, center=POOL[i], patch=True) for i in POOL_ORDER]
        self.play(ReplacementTransform(big, pills[0]), FadeOut(prot), FadeOut(thin), run_time=0.8)

        # it piles up, and no new gene is read
        ghost = ghost_chip("read a new gene", 24).move_to([4.3, 2.15, 0])
        x = strike(ghost)
        self.at("piles up")
        self.play(LaggedStart(*[FadeIn(q, scale=0.6, run_time=0.35) for q in pills[1:]], lag_ratio=0.3))
        self.at("new gene")
        self.play(FadeIn(ghost), run_time=0.4)
        self.at("being read")
        self.play(Create(x), run_time=0.4)

        # free of its restraint: onto the DNA
        dna = dna_line(-6.1, 6.1, DNA2_Y)
        genes = [gene_block(xc, DNA2_Y, w=1.6) for xc in XS]
        gls = [T(t, 22, GREY).move_to([xc, DNA2_Y - 0.45, 0]) for t, xc in zip(("p21 gene", "repair genes", "cell-death genes"), XS)]
        self.at("Free of")
        self.play(Create(dna), *[FadeIn(g) for g in genes], *[FadeIn(g) for g in gls], run_time=0.6)
        rest = [(xc - 0.55, DNA2_Y + 0.75) for xc in XS]
        movers = [pills[8], pills[10], pills[11]]            # three pills of the bottom rows
        movers = [pills[POOL_ORDER.index(i)] for i in (8, 10, 11)]
        self.at("switches on")
        self.play(movers[0].animate.move_to([rest[0][0], rest[0][1], 0]), run_time=0.8)
        # p21 gene on; it makes p21, which blocks the division kinases
        p21 = bchip("p21", TEAL, 26).move_to([XS[0] + 0.6, -0.95, 0])
        up1 = arr([XS[0] + 0.6, DNA2_Y + 0.15, 0], p21.get_bottom(), TEAL)
        self.at("the gene for")
        self.play(gene_on(genes[0], GREEN), gls[0].animate.set_color(GREEN), GrowArrow(up1), run_time=0.5)
        self.play(FadeIn(p21, shift=UP * 0.15), run_time=0.4)
        kin = ghost_chip("division kinases", 24).move_to([XS[0] + 0.6, 0.15, 0])
        blk = inhib([XS[0] + 0.6, p21.get_top()[1] + 0.05, 0], [XS[0] + 0.6, kin.get_bottom()[1] - 0.02, 0], RED)
        self.at("blocks the")
        self.play(Create(blk), FadeIn(kin), run_time=0.5)
        self.at("cell division")
        self.play(kin.animate.set_opacity(0.4), Create(strike(kin)), run_time=0.5)

        # DNA repair genes
        rep = bchip("DNA repair", TEAL, 26).move_to([XS[1] + 0.6, -0.95, 0])
        up2 = arr([XS[1] + 0.6, DNA2_Y + 0.15, 0], rep.get_bottom(), TEAL)
        self.at("It switches on", nth=1)
        self.play(movers[1].animate.move_to([rest[1][0], rest[1][1], 0]), run_time=0.8)
        self.at("genes for")
        self.play(gene_on(genes[1], GREEN), gls[1].animate.set_color(GREEN), GrowArrow(up2), run_time=0.5)
        self.at("DNA repair")
        self.play(FadeIn(rep, shift=UP * 0.15), run_time=0.4)

        # and, if the damage is severe, genes that kill the cell
        sev = T("if the damage is severe", 24, ORANGE, weight=BOLD).move_to([XS[2] + 0.2, 0.15, 0])
        die = bchip("cell death", TEAL, 26).move_to([XS[2] + 0.6, -0.95, 0])
        up3 = arr([XS[2] + 0.6, DNA2_Y + 0.15, 0], die.get_bottom(), TEAL)
        self.at("damage is")
        self.play(FadeIn(sev, shift=DOWN * 0.1), movers[2].animate.move_to([rest[2][0], rest[2][1], 0]), run_time=0.9)
        self.at("also switches")
        self.play(gene_on(genes[2], GREEN), gls[2].animate.set_color(GREEN), GrowArrow(up3), run_time=0.5)
        self.at("kill the cell")
        self.play(FadeIn(die, shift=UP * 0.15), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
S5 = 1.3                                    # S05: pill scale
CX5, A5, Q5 = -1.0, 0.15, 1.75               # the pill's x, the catching height, the waiting height
GENE5 = 3.05
LIG = (4.9, 0.9)
NUC_TOP, NUC_BOT, DNA5 = -1.95, -3.5, -3.05


class S05Chemicals(SpokenScene):
    """Keap1 grips NRF2 as part of a tagging ligase; a reactive chemical stops tagging."""

    def construct(self):
        chem = bchip("reactive chemical", ORANGE, 24).move_to([-4.7, -1.45, 0])
        dna = dna_line(-6.0, 2.2, GENE5)
        gene = gene_block(CX5, GENE5)
        self.at("Chemical threats")
        self.play(FadeIn(chem, shift=UP * 0.1), Create(dna), FadeIn(gene), run_time=0.7)

        # a responder called NRF2, dropped from its gene
        p1 = pill("Nrf2", S5, w=2.1, center=(CX5, GENE5 - 0.55))
        self.at("responder called")
        self.play(FadeIn(p1, scale=0.6), run_time=0.3)
        self.play(p1.animate.move_to([CX5, A5, 0]), run_time=0.7)

        # it switches on genes for protective enzymes (in the nucleus)
        nuc = RoundedRectangle(corner_radius=0.35, width=10.3, height=NUC_TOP - NUC_BOT, stroke_color=GREY, stroke_width=3
                               ).move_to([-0.75, (NUC_TOP + NUC_BOT) / 2, 0])
        nl = T("nucleus", 24, GREY).move_to([-5.0, -2.35, 0])
        ndna = dna_line(-5.8, 4.2, DNA5, w=5)
        ngene = gene_block(CX5, DNA5, w=1.8)
        ngl = T("protective enzyme genes", 22, GREY).move_to([2.55, DNA5 + 0.5, 0])
        link = DashedLine([CX5, A5 - 0.6, 0], [CX5, DNA5 + 0.25, 0], color=GREY, stroke_width=4, dash_length=0.14)
        swl = T("switches on", 24, GREY).move_to([0.9, -1.3, 0])
        self.at("switches on genes")
        self.play(Create(nuc), FadeIn(nl), Create(ndna), FadeIn(ngene), run_time=0.7)
        self.at("protective enzymes")
        self.play(FadeIn(ngl), Create(link), FadeIn(swl), run_time=0.6)

        # made constantly: the next pill is already waiting
        gl = T("NRF2 gene", 24, GREY).move_to([4.2, GENE5, 0])
        p2 = pill("Nrf2", S5, w=2.1, center=(CX5, GENE5 - 0.55))
        self.at("cell makes")
        self.play(FadeOut(link), FadeOut(swl), FadeIn(gl), FadeIn(p2, scale=0.6), run_time=0.5)
        self.play(p2.animate.move_to([CX5, Q5, 0]), run_time=0.6)

        # Keap1 grips it as part of the ubiquitin ligase
        ref = pill("Nrf2", S5, w=2.1, center=(CX5, A5))
        kc = claw("Keap1", ref)
        set_jaws(kc, 0.55)
        kc.shift(LEFT * 1.4)
        self.at("constantly")
        self.play(FadeIn(kc, shift=RIGHT * 0.5), run_time=0.5)
        self.play(kc.animate.shift(RIGHT * 1.4), run_time=0.6)
        self.at("grips it")
        self.play(*jaw_anims(kc, -0.55), run_time=0.45)

        # the ligase tags Nrf2; the proteasome destroys the tagged protein
        lig = destroyer("proteasome", RED, 22, center=LIG, w=2.4, h=1.4)
        self.at("ubiquitin ligase")
        self.play(FadeIn(lig), run_time=0.5)
        tag = ubtag(1.1).move_to(p1.body.get_top() + UP * 0.2)
        self.at("tags it")
        self.play(FadeIn(tag, scale=0.6), run_time=0.4)
        p1.add(tag)
        self.at("for destruction")
        self.play(*jaw_anims(kc, 0.4), run_time=0.3)
        self.play(AnimationGroup(
            p1.animate(run_time=0.9).scale(0.25).move_to(lig.get_center()).set_opacity(0),
            Succession(Wait(0.4), p2.animate(run_time=0.5).move_to([CX5, A5, 0]),
                       AnimationGroup(*jaw_anims(kc, -0.4), run_time=0.3))))

        # a reactive chemical hits Keap1 and stays on it as a small orange mark
        self.at("reactive chemical")
        self.play(chem.animate.move_to([-3.6, -1.2, 0]), run_time=0.8)
        self.at("hits")
        mark = Dot([-3.6, A5 - 0.98, 0], radius=0.17, color=ORANGE)
        self.play(Flash(np.array([-3.6, A5 - 1.0, 0]), color=ORANGE, line_length=0.35, flash_radius=0.55, num_lines=10),
                  Wiggle(kc, scale_value=1.04, rotation_angle=0.02 * TAU), run_time=0.7)
        self.play(ReplacementTransform(chem, mark), run_time=0.4)

        # Keap1 keeps its grip, but tagging stops: cross out a Ub badge on Nrf2
        blocked_tag = ubtag(1.1).move_to(p2.body.get_top() + UP * 0.2)
        cross = strike(blocked_tag)
        self.at("tagging stops")
        self.play(FadeIn(blocked_tag, scale=0.6), run_time=0.4)
        self.play(Create(cross), run_time=0.3)

        # so a newly made Nrf2 finds Keap1 occupied, and goes on to the nucleus
        p3 = pill("Nrf2", S5, w=2.1, center=(CX5, GENE5 - 0.55))
        pts = [(CX5, GENE5 - 0.55), (CX5, 1.8), (1.9, 1.45), (1.9, -1.1), (CX5, -1.5), (CX5, -2.5)]
        path = VMobject().set_points_smoothly([np.array([x, y, 0]) for x, y in pts])
        self.at("so new")
        self.play(FadeIn(p3, scale=0.6), run_time=0.3)
        self.play(MoveAlongPath(p3, path), run_time=2.0, rate_func=smooth)
        self.at("nucleus")
        self.play(gene_on(ngene, GREEN), ngl.animate.set_color(GREEN), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the two side by side: made all the time, held back, stress arrives, restraint removed."""

    def construct(self):
        SR = 1.2
        XL = 0.2                                     # where both pills' front ends sit
        rows = []
        for name, kname, y, stress, gname in (("p53", "MDM2", 1.25, "DNA break", "p53 gene"),
                                              ("Nrf2", "Keap1", -1.1, "reactive chemical", "NRF2 gene")):
            w = 1.9 if name == "p53" else 2.1
            pl = pill(name, SR, w=w, center=(XL + w * SR / 2, y), patch=(name == "p53"))
            if name == "p53":
                pl.patch.set_stroke(GREY).set_fill(GREY, 0.3)
            kc = claw(kname, pl)
            st = bchip(stress, ORANGE, 22)
            kin = None
            if name == "p53":
                kin = bchip("ATM + kinases", ORANGE, 22).next_to(kc.box.get_left(), LEFT, buff=0.55)
                st.next_to(kin, LEFT, buff=0.55)
            else:
                st.next_to(kc.box.get_left(), LEFT, buff=0.6)
            ge = gene_block(5.2, y + 0.1, w=1.6)
            gt = T(gname, 22, GREY).move_to([5.2, y - 0.35, 0])
            rows.append(dict(p=pl, c=kc, st=st, kin=kin, ge=ge, gt=gt, y=y, w=w))
        names = ("made all the time", "held back", "stress arrives", "restraint removed")
        heads = VGroup(*[T(t, 22, GREY, weight=BOLD) for t in names]).arrange(RIGHT, buff=0.9).move_to([0, 3.15, 0])
        ars = [T("\u2192", 22, GREY).move_to((heads[k].get_right() + heads[k + 1].get_left()) / 2) for k in range(3)]

        def lit(i):
            return [h.animate.set_color(TEXT if k == i else GREY) for k, h in enumerate(heads)]

        # side by side
        self.play(*[FadeIn(r["p"]) for r in rows], *[FadeIn(r["c"]) for r in rows], run_time=0.8)
        # made all the time
        self.at("a responder is made")
        arrows = [arr([r["ge"].get_left()[0] - 0.05, r["y"] + 0.1, 0], [r["p"].body.get_right()[0] + 0.1, r["y"] + 0.1, 0], GREEN, w=5) for r in rows]
        self.play(FadeIn(heads), FadeIn(VGroup(*ars)), *lit(0),
                  *[FadeIn(r["ge"]) for r in rows], *[FadeIn(r["gt"]) for r in rows], run_time=0.7)
        self.play(*[r["ge"].animate.set_fill(GREEN) for r in rows], *[GrowArrow(a) for a in arrows], run_time=0.5)
        self.play(*[pop(r["p"], 1.04) for r in rows], run_time=0.5)
        # held back, or destroyed
        self.at("holds it back")
        self.play(*lit(1), *[pop(r["c"], 1.03) for r in rows], FadeOut(VGroup(*arrows)), run_time=0.7)
        tags = [ubtag(1.2).move_to([r["p"].body.get_right()[0] - 0.5, r["y"] + 0.7, 0]) for r in rows]
        self.at("or destroys")
        self.play(*[FadeIn(t, scale=0.6) for t in tags], run_time=0.5)
        # stress arrives: the damage kinases carry it to MDM2; the chemical hits Keap1 itself
        self.at("Stress removes")
        r1, r2 = rows
        self.play(*lit(2), FadeOut(VGroup(*[r[k] for r in rows for k in ("ge", "gt")])),
                  FadeIn(r1["st"], shift=RIGHT * 0.2), FadeIn(r2["st"], shift=RIGHT * 0.2), run_time=0.6)
        a1 = arr([r1["st"].get_right()[0], r1["y"], 0], [r1["kin"].get_left()[0], r1["y"], 0], ORANGE, w=5)
        a2 = arr([r1["kin"].get_right()[0], r1["y"], 0], [r1["c"].box.get_left()[0], r1["y"], 0], ORANGE, w=5)
        a3 = arr([r2["st"].get_right()[0], r2["y"], 0], [r2["c"].box.get_left()[0], r2["y"], 0], ORANGE, w=5)
        self.play(FadeIn(r1["kin"], shift=RIGHT * 0.2), GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), run_time=0.5)
        # the restraint is removed from p53; Keap1 keeps hold of its Nrf2, so a new one gets away
        self.at("the restraint")
        mark = Dot([r2["c"].box.get_left()[0] + 0.5, r2["y"] - 0.8, 0], radius=0.15, color=ORANGE)
        self.play(*lit(3), *jaw_anims(r1["c"], 0.4), *[FadeOut(t) for t in tags], FadeOut(VGroup(a3)),
                  ReplacementTransform(r2["st"], mark), run_time=0.6)
        pn = pill("Nrf2", SR, w=2.1, center=(XL + r2["w"] * SR + 0.55 + 2.1 * SR / 2, r2["y"]))
        self.play(r1["c"].animate.set_opacity(0.0), patch_state(r1["p"], GREEN, 0.5),
                  FadeOut(VGroup(a1, a2)), FadeOut(r1["st"]), FadeOut(r1["kin"]), FadeIn(pn, scale=0.6), run_time=0.8)
        self.at("already there")
        self.play(pop(r1["p"], 1.08), pop(pn, 1.08), run_time=0.6)
        # the rule
        rule = VGroup(T("A stress responder is made all the time", 30, TEXT, font=TITLE_FONT),
                      T("and held back, until stress removes the restraint.", 30, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.16)
        rule.move_to([0, -2.95, 0])
        self.at("keep this rule")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "A stress responder is made all the time and held back."
