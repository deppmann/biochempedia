"""What a Dish Can Show  (chapter 2 of the film series on "Synapses in the Brain")

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared by every chapter of this lesson)
  YELLOW = neuroligin (the kidney-cell protein, the dendrite-side partner)
  BLUE   = neurexin (the axon-side partner, soluble neurexin, alpha-neurexins)
  TEAL   = synaptic vesicles, clusters of them, the terminal
  GREEN  = there / working / normal  (lit lamp, counted synapses)
  RED    = blocked / impaired / deleted (dim lamp, struck-out protein)
  GREY   = cells, axon, dendrite, de-emphasised outlines
  PURPLE = postsynaptic proteins, NMDA receptors
  ORANGE = AMPA receptors, excitatory tag
  PINK   = inhibitory tag
  TEXT   = antibodies, the question, the definitions
  GOLD   = the rule to keep (used once, in the last closing scene)
Lamps: There / Releases / Responds, as in chapter 1. Lit = green (seen), half = green half (poor),
  dim = red (fails), dashed = not tested.  LT = light grey for small text.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#D98CB3"

_house_chip = chip


def chip(*args, **kwargs):
    """House chip with a background plate so lines pass behind the label."""
    g = _house_chip(*args, **kwargs)
    back = RoundedRectangle(corner_radius=.14, width=g.width, height=g.height,
                            stroke_width=0, fill_color=BG, fill_opacity=1).move_to(g)
    return VGroup(back, g)


# ------------------------------------------------------------------------------------------------
# small drawing helpers
# ------------------------------------------------------------------------------------------------
LT = "#B9BFCB"      # light grey for small text (credits, axis notes)
AXC = "#7B8494"     # axon colour


def R(w, h, color=GREY, fill=.2, r=.3, sw=3, cx=0.0, cy=0.0):
    return RoundedRectangle(corner_radius=min(r, h / 2 - .01, w / 2 - .01), width=w, height=h,
                            stroke_color=color, stroke_width=sw, fill_color=color,
                            fill_opacity=fill).move_to([cx, cy, 0])


def stub(x, y, color, s=.3):
    return RoundedRectangle(corner_radius=.07, width=s, height=s, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=.85).move_to([x, y, 0])


def vdot(x, y, r=.13, op=1.0):
    return Dot([x, y, 0], radius=r, color=TEAL, fill_opacity=op)


def ab(x, y, s=1.0, color=TEXT):
    """An antibody cartoon: a simple Y."""
    return VGroup(Line([x, y - .2 * s, 0], [x, y, 0]), Line([x, y, 0], [x - .15 * s, y + .17 * s, 0]),
                  Line([x, y, 0], [x + .15 * s, y + .17 * s, 0])).set_stroke(color, 5 * s)


def cross_mark(x, y, s=.2, color=RED, w=5):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0]), Line([x - s, y + s, 0], [x + s, y - s, 0])).set_stroke(color, w)


def gone_chip(text, color, size, x, y):
    """A chip for a deleted protein: dashed red box, faded label, red cross at the corner (nothing struck through the text)."""
    c = chip(text, color, size).move_to([x, y, 0])
    c[1][0].set_stroke(RED, 3).set_fill(RED, .1)
    c[1][1].set_opacity(.6)
    x_ = cross_mark(c.get_right()[0] - .05, c.get_top()[1] - .02, .17)
    return VGroup(c, x_)


def tick(x, y, s=1.0):
    return VMobject(stroke_color=GREEN, stroke_width=8).set_points_as_corners(
        [[x - .2 * s, y, 0], [x - .06 * s, y - .16 * s, 0], [x + .22 * s, y + .2 * s, 0]])


def lamp(state="off", r=.38, x=0.0, y=0.0):
    """lit = seen (green), half = poor (half green), dim = fails (red), off = not tested (dashed)."""
    if state == "lit":
        glow = Circle(radius=r * 1.6, stroke_width=0, fill_color=GREEN, fill_opacity=.25)
        core = Circle(radius=r, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=.9)
        g = VGroup(glow, core)
    elif state == "half":
        glow = Circle(radius=r * 1.6, stroke_width=0, fill_color=GREEN, fill_opacity=.08)
        core = Circle(radius=r, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=.12)
        half = Sector(radius=r, start_angle=PI / 2, angle=PI, stroke_width=0, fill_color=GREEN, fill_opacity=.9)
        g = VGroup(glow, core, half)
    elif state == "dim":
        glow = Circle(radius=r * 1.6, stroke_width=0, fill_opacity=0)
        core = Circle(radius=r, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=.28)
        g = VGroup(glow, core)
    else:
        glow = Circle(radius=r * 1.6, stroke_width=0, fill_opacity=0)
        core = DashedVMobject(Circle(radius=r, stroke_color=LT, stroke_width=3), num_dashes=16)
        g = VGroup(glow, core)
    return g.move_to([x, y, 0])


def strip(states):
    """The three small lamps in the top-right corner."""
    pairs = []
    for n, s in zip(["There", "Releases", "Responds"], states):
        l = lamp(s, .2)
        pairs.append(VGroup(l, T(n, 22, TEXT).next_to(l, RIGHT, buff=.15)))
    g = VGroup(*pairs).arrange(RIGHT, buff=.35)
    return g.move_to([6.75 - g.width / 2, 3.45, 0])


def legend(items, y=-3.55):
    parts = []
    for st, tx in items:
        l = lamp(st, .16)
        parts.append(VGroup(l, T(tx, 22, LT).next_to(l, RIGHT, buff=.12)))
    return VGroup(*parts).arrange(RIGHT, buff=.45).move_to([0, y, 0])


def micro():
    """A microscope cartoon (for counting)."""
    base = Rectangle(width=1.9, height=.24, stroke_color=TEXT, fill_color=TEXT, fill_opacity=.5).move_to([0, -1.5, 0])
    pillar = Line([.8, -1.4, 0], [.8, .35, 0], color=TEXT, stroke_width=10)
    arm = Line([.8, .35, 0], [.3, .6, 0], color=TEXT, stroke_width=10)
    tube = Rectangle(width=.55, height=1.5, stroke_color=TEXT, fill_color=TEXT, fill_opacity=.25).move_to([0, .6, 0])
    eye = Rectangle(width=.8, height=.16, stroke_color=TEXT, fill_color=TEXT, fill_opacity=.6).move_to([0, 1.43, 0])
    obj = Rectangle(width=.28, height=.3, stroke_color=TEXT, fill_color=TEXT, fill_opacity=.6).move_to([0, -.3, 0])
    stage = Line([-.95, -.8, 0], [.6, -.8, 0], color=TEXT, stroke_width=9)
    spec = Circle(radius=.13, stroke_color=GREEN, fill_color=GREEN, fill_opacity=.9).move_to([0, -.64, 0])
    return VGroup(base, pillar, arm, tube, eye, obj, stage, spec)


def pipette():
    """A recording pipette touching a cell (for recording)."""
    body = Polygon([-.14, 1.3, 0], [.14, 1.3, 0], [.035, -.85, 0], [-.035, -.85, 0],
                   stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=.3)
    wire = Line([0, 1.3, 0], [0, 1.75, 0], color=TEXT, stroke_width=5)
    cell = Circle(radius=.62, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.3).move_to([0, -1.3, 0])
    return VGroup(body, wire, cell).rotate(PI / 7)


def brain_icon():
    """Lateral brain silhouette, with lobes, folds, cerebellum and brainstem."""
    outline = VMobject(stroke_color=GREY, stroke_width=5,
                       fill_color=PINK, fill_opacity=.22)
    outline.set_points_smoothly([np.array([x, y, 0]) for x, y in
        [(-2, -.35), (-2.15, .3), (-1.8, 1.0), (-1.1, 1.45),
         (-.2, 1.6), (.8, 1.4), (1.6, .9), (1.95, .25),
         (1.65, -.35), (.7, -.6), (.1, -.9), (-.8, -.8), (-2, -.35)]])
    cb = Ellipse(width=1.25, height=.85, stroke_color=GREY, stroke_width=4,
                 fill_color=PINK, fill_opacity=.3).move_to([1.1, -.85, 0])
    stem = VMobject(stroke_color=GREY, stroke_width=12).set_points_as_corners(
        [[.65, -.65, 0], [.5, -1.25, 0], [.85, -1.55, 0]])
    folds = VGroup()
    for pts in [[(-1.6,.25),(-1.2,.65),(-.8,.45),(-.55,.85)],
                [(-.3,1.25),(-.5,.6),(-.05,.2),(-.2,-.4)],
                [(.5,1.1),(.25,.7),(.8,.4),(.6,-.2)],
                [(1.4,.55),(1.05,.2),(1.35,-.15)]]:
        folds.add(VMobject(stroke_color=GREY, stroke_width=4).set_points_smoothly(
            [np.array([x,y,0]) for x,y in pts]))
    return VGroup(stem, cb, outline, folds)


def dish_icon():
    cell = R(4.4, 1.2, GREY, .22, .45, cx=0, cy=-.6)
    st = VGroup(*[stub(x, .08, YELLOW, .3) for x in (-1.3, 0, 1.3)])
    ax = R(5.0, .62, GREY, .15, .3, cx=0, cy=.45)
    ds = VGroup(*[vdot(x, y, .13) for x, y in [(-.4, .4), (-.15, .55), (.15, .4), (.38, .55), (0, .45)]])
    return VGroup(cell, st, ax, ds)


# ------------------------------------------------------------------------------------------------
# the dish: kidney cells below, axons from a pontine explant running down onto them
# ------------------------------------------------------------------------------------------------
CX = [-4.95, -1.65, 1.65, 4.95]     # four kidney cells
NL = [1, 3]                         # the two that make neuroligin
AXY = -.4                            # where axons lie on the cells
CELL_Y, CELL_H = -1.45, 2.9         # cell top at y = 0


def kcell(cx, nlg=False, w=2.9):
    return RoundedRectangle(corner_radius=.4, width=w, height=CELL_H, stroke_color=GREY, stroke_width=3,
                            fill_color=YELLOW if nlg else GREY, fill_opacity=.2).move_to([cx, CELL_Y, 0])


def axon_path(pts, w=34):
    m = VMobject(stroke_color=AXC, stroke_width=w, stroke_opacity=.75, fill_opacity=0, cap_style=CapStyleType.ROUND)
    m.set_points_smoothly([np.array([x, y, 0.]) for x, y in pts])
    return m


AXON_PTS = [
    [(-5.45, 2.2), (-5.4, 1.2), (-5.0, .65), (-4.4, AXY), (-3.6, AXY)],
    [(-5.35, 2.7), (-3.9, 2.0), (-3.1, 1.0), (-2.6, .58), (-2.3, AXY), (-.8, AXY)],
    [(-5.3, 3.1), (-2.5, 3.25), (.2, 2.6), (1.2, 1.3), (1.9, .6), (2.3, AXY), (6.3, AXY)],
]
SCAT = [[-4.7, -4.2, -3.8], [-2.5, -2.1, -1.65, -1.2, -.85], [2.1, 2.6, 3.05], [3.8, 4.4, 4.95, 5.5, 6.1]]
CLUS = [(-.4, 0), (-.13, .13), (.17, -.05), (.4, .08), (0, -.02)]


class Dish:
    """Everything in the pons-explant dish scenes, in the same place in every scene."""

    def __init__(self, clustered=False, lab=True):
        self.cells = [kcell(c, i in NL) for i, c in enumerate(CX)]
        self.labs = [T("neuroligin" if i in NL else "kidney cell", 26, YELLOW if i in NL else LT).move_to([c, -1.8, 0])
                     for i, c in enumerate(CX)]
        self.stubs = VGroup(*[stub(CX[i] + dx, -.15, YELLOW) for i in NL for dx in (-.8, 0, .8)])
        self.expl = Circle(radius=.75, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.25).move_to([-6.05, 2.75, 0])
        self.expl_t = T("pons", 26, TEXT).move_to(self.expl)
        self.axons = [axon_path(p) for p in AXON_PTS]
        self.dots = []
        for i, c in enumerate(CX):
            row = []
            for j, x in enumerate(SCAT[i]):
                if clustered and i in NL:
                    dx, dy = CLUS[j]
                    row.append(vdot(CX[i] + dx, AXY + dy, .2, 1))
                else:
                    row.append(vdot(x, AXY, .12, .5))
            self.dots.append(row)
        self.halos = [Circle(radius=.78, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=.14).move_to([CX[i], AXY, 0])
                      for i in NL]
        if not clustered:
            for h in self.halos:
                h.set_opacity(0)
        self.vlab = T("synaptic vesicle proteins", 26, TEAL).move_to([4.3, 1.75, 0])
        self.vlead = Line([4.3, 1.55, 0], [4.45, -.1, 0], color=TEAL, stroke_width=3)
        self.dishlab = T("kidney cells in a dish", 26, LT).move_to([0, -3.4, 0])

    def flat_dots(self):
        return [d for row in self.dots for d in row]

    def base(self):
        return [*self.cells, *self.labs, self.stubs, self.expl, self.expl_t, *self.axons, *self.flat_dots(), *self.halos]


# ------------------------------------------------------------------------------------------------
# tables of lamps
# ------------------------------------------------------------------------------------------------
XT, XR, XS = -0.3, 2.6, 5.5      # There, Releases, Responds column centres (even 2.9 gaps)
XC = (XR + XS) / 2               # centre of the two recording columns
YR = [1.45, -0.4, -2.35]         # three rows
HY = 2.42                        # header text height


class Table:
    def __init__(self):
        self.hdr = VGroup(T("There", 26, TEXT).move_to([XT, HY, 0]), T("Releases", 26, TEXT).move_to([XR, HY, 0]),
                          T("Responds", 26, TEXT).move_to([XS, HY, 0]),
                          Line([-6.7, 2.0, 0], [6.7, 2.0, 0], color=GREY, stroke_width=2).set_opacity(.5))
        # a bracket ties the pipette to both recording columns
        self.brk = VGroup(Line([XR - .75, 2.78, 0], [XS + .75, 2.78, 0]), Line([XR - .75, 2.78, 0], [XR - .75, 2.66, 0]),
                          Line([XS + .75, 2.78, 0], [XS + .75, 2.66, 0])).set_stroke(LT, 3)
        self.hdr.add(self.brk)
        self.micro = micro().scale_to_fit_height(.8).move_to([XT, 3.35, 0])
        self.pip = pipette().scale_to_fit_height(.8).move_to([XC, 3.35, 0])
        # row 1: no alpha-neurexins
        self.lab1 = T("no alpha-neurexins", 30, BLUE).move_to([-6.7, YR[0] + .3, 0], aligned_edge=LEFT)
        self.cred1 = VGroup(T("Missler, Südhof and", 24, LT), T("colleagues, 2003", 24, LT)).arrange(
            DOWN, aligned_edge=LEFT, buff=.05).move_to([-6.7, YR[0] - .45, 0], aligned_edge=LEFT)
        self.r1t = lamp("lit", .38, XT, YR[0])
        self.r1tn = T("inhibitory fewer", 24, TEXT).move_to([XT, YR[0] - .72, 0])
        self.r1r_off = lamp("off", .38, XR, YR[0])
        self.r1r = lamp("half", .38, XR, YR[0])
        self.r1rn = T("released poorly", 24, TEXT).move_to([XR, YR[0] - .72, 0])
        self.r1s = lamp("off", .38, XS, YR[0])
        self.r1sn = T("not tested", 24, LT).move_to([XS, YR[0] - .72, 0])
        # row 2: no neuroligins 1, 2, 3
        self.lab2 = T("no neuroligins 1, 2, 3", 26, YELLOW).move_to([-6.7, YR[1] + .1, 0], aligned_edge=LEFT)
        self.lab2b = T("brainstem", 26, LT).move_to([-6.7, YR[1] - .4, 0], aligned_edge=LEFT)
        self.r2t = lamp("lit", .38, XT, YR[1])
        self.r2tn = T("normal number", 24, TEXT).move_to([XT, YR[1] - .72, 0])
        self.r2c_off = DashedVMobject(R(4.8, 1.5, LT, 0, .4, 3, XC + .05, YR[1]), num_dashes=60)
        self.r2c_offt = T("recorded together", 24, LT).move_to([XC + .05, YR[1], 0])
        self.r2c = R(4.8, 1.5, RED, .2, .4, 4, XC + .05, YR[1])
        self.r2ct = VGroup(T("transmission impaired", 26, RED), T("release and response", 22, LT), T("not separated", 22, LT)).arrange(
            DOWN, buff=.06).move_to([XC + .05, YR[1], 0])
        # row 3: stargazer
        self.lab3 = T("stargazer", 30, TEXT).move_to([-6.7, YR[2], 0], aligned_edge=LEFT)
        self.r3t = lamp("lit", .38, XT, YR[2])
        self.r3r = lamp("lit", .38, XR, YR[2])
        self.r3a = lamp("lit", .3, XS - .85, YR[2])
        self.r3b = lamp("dim", .3, XS + .55, YR[2])
        self.r3al = T("NMDA", 24, PURPLE).move_to([XS - .85, YR[2] - .62, 0])
        self.r3bl = T("AMPA", 24, ORANGE).move_to([XS + .55, YR[2] - .62, 0])

    def upto(self, n):
        """Final state of the table at the start of the given step (what earlier scenes built)."""
        base = [self.hdr, self.micro, self.pip]
        r1 = [self.lab1, self.cred1, self.r1t, self.r1tn]
        r1b = r1 + [self.r1r, self.r1rn, self.r1s, self.r1sn]
        r2 = r1b + [self.lab2, self.lab2b, self.r2t, self.r2tn]
        r2b = r2 + [self.r2c, self.r2ct]
        steps = {"s16": [self.lab1, self.cred1], "s17": r1, "s19": r1b, "s20": r2, "s22": r2b,
                 "full": r2b + [self.lab3, self.r3t, self.r3r, self.r3a, self.r3b, self.r3al, self.r3bl]}
        return base + steps[n]


def hbars(y0, bar_h, gap, ref_len, items, axis_text, x0=-2.2, vsize=26):
    """Horizontal qualitative bars. items: (label, length, color, value_text, value_color).
    Dashed outline = the control mouse level. Returns (axis_group, [item_groups])."""
    n = len(items)
    ybot = y0 - (n - 1) * (bar_h + gap) - bar_h / 2
    base = Line([x0, y0 + bar_h / 2 + .12, 0], [x0, ybot - .1, 0], color=LT, stroke_width=3)
    axt = T(axis_text, 24, LT).move_to([x0 + ref_len / 2 - .6, ybot - .42, 0])
    groups = []
    for k, (lab, ln, col, vt, vc) in enumerate(items):
        y = y0 - k * (bar_h + gap)
        ref = DashedVMobject(Rectangle(width=ref_len, height=bar_h, stroke_color=LT, stroke_width=3), num_dashes=50).move_to([x0 + ref_len / 2, y, 0])
        bar = Rectangle(width=ln, height=bar_h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=.55).move_to([x0 + ln / 2, y, 0])
        lt = T(lab, 28, TEXT).move_to([x0 - .25, y, 0], aligned_edge=RIGHT)
        vtx = T(vt, vsize, vc).move_to([x0 + ref_len + .25, y, 0], aligned_edge=LEFT)
        groups.append((VGroup(ref, bar, lt), vtx, bar))
    return VGroup(base, axt), groups


# ------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Synapses in the Brain: Adhesion, Scaffolds and Astrocytes"
    TITLE = "What a Dish Can Show"


class S01Q(SpokenScene):
    def construct(self):
        dish = R(13.0, 5.5, LT, .04, .6, 3, 0, -.95)
        dl = T("dish", 26, LT).move_to([-5.9, -3.35, 0])
        cell = R(5.2, 2.5, GREY, .22, .8, cx=0, cy=-2.0)
        cl = T("kidney cell", 28, LT).move_to([0, -2.95, 0])
        stmt = T("Kidney cells do not make synapses.", 38, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        syn = chip("synapses", TEXT, 32).move_to([0, -1.65, 0])
        gone = gone_chip("synapses", TEXT, 32, 0, -1.65)
        self.play(FadeIn(dish), FadeIn(dl), FadeIn(cell), FadeIn(cl), run_time=.6)
        self.at("kidney cell")
        self.play(FadeIn(stmt), run_time=.5)
        self.at("make synapses")
        self.play(FadeIn(syn), run_time=.3)
        self.play(ReplacementTransform(syn, gone), run_time=.5)
        q = T("Can one protein make it build a terminal?", 38, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        ax = axon_path([(-6.3, 1.0), (-5.0, .7), (-3.3, -.1), (-2.8, -.95), (-2.6, -1.35)], 34)
        tip = VGroup(*[Line([-2.6, -1.4, 0], [-2.6 + .42 * np.cos(a), -1.4 + .42 * np.sin(a), 0]) for a in (-.7, -.2, .3)]).set_stroke(AXC, 6)
        axl = T("axon", 28, LT).move_to([-5.2, 1.35, 0])
        self.at("can one")
        self.play(FadeOut(gone), ReplacementTransform(stmt, q), run_time=.5)
        self.play(Create(ax, run_time=1.0), Succession(Wait(.75), FadeIn(tip, run_time=.25)), FadeIn(axl, run_time=.5))
        prot = chip("one neuronal protein", TEXT, 28).move_to([0, .25, 0])
        parr = Arrow([0, -.1, 0], [0, -.75, 0], color=TEXT, stroke_width=5, buff=0, tip_length=.2)
        self.at("neuronal protein")
        self.play(FadeIn(prot), GrowArrow(parr), run_time=.5)
        term = DashedVMobject(R(1.3, .95, TEAL, 0, .3, 4, -2.6, -1.2), num_dashes=30)
        tl = T("terminal?", 30, TEAL).move_to([-4.2, -2.4, 0])
        tla = Arrow([-3.65, -2.25, 0], [-2.95, -1.6, 0], color=TEAL, stroke_width=4, buff=0, tip_length=.18)
        self.at("build a terminal")
        self.play(FadeIn(term), FadeIn(tl), GrowArrow(tla), run_time=.6)
        self.finish()


class S02Pair(SpokenScene):
    def construct(self):
        top = R(12.4, 1.3, GREY, .15, .5, cx=0, cy=2.95)
        bot = R(12.4, 1.3, GREY, .15, .5, cx=0, cy=-2.95)
        tl = T("axon terminal", 28, LT).move_to([-4.6, 2.95, 0])
        bl = T("dendrite", 28, LT).move_to([-5.0, -2.95, 0])
        self.add(top, bot)
        nx_stem = Line([0, 2.3, 0], [0, 1.65, 0], color=BLUE, stroke_width=16)
        nx_cup = Arc(radius=1.5, start_angle=-PI / 6, angle=7 * PI / 6, arc_center=[0, .1, 0], color=BLUE, stroke_width=18)
        nxl = T("neurexin", 40, BLUE).move_to([-4.0, .9, 0])
        nxd = Line([-2.9, .9, 0], [-1.45, .6, 0], color=BLUE, stroke_width=3)
        self.at("sits on")
        self.play(Create(nx_stem), Create(nx_cup), FadeIn(nxl), Create(nxd), run_time=.6)
        self.at("the axon")
        self.play(FadeIn(tl), run_time=.3)

        def nlg(knob_y):
            stem = Line([0, -2.3, 0], [0, knob_y - .55, 0], color=YELLOW, stroke_width=16)
            knob = Circle(radius=.65, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=.85).move_to([0, knob_y, 0])
            return VGroup(stem, knob)
        low, high = nlg(-1.35), nlg(.45)
        nll = T("neuroligin", 40, YELLOW).move_to([4.4, -1.7, 0])
        nld = Line([2.85, -1.7, 0], [.15, -1.6, 0], color=YELLOW, stroke_width=3)
        nld2 = Line([2.85, -.9, 0], [.15, -.4, 0], color=YELLOW, stroke_width=3)
        self.at("its partner")
        self.play(FadeIn(low), FadeIn(nll), Create(nld), run_time=.6)
        self.play(FadeIn(bl), run_time=.2)
        self.at("on the dendrite")
        self.play(Transform(low, high), nll.animate.move_to([4.4, -.9, 0]), Transform(nld, nld2), run_time=.9)
        self.play(Indicate(VGroup(nx_cup, low), color=TEXT, scale_factor=1.05), run_time=.9)
        self.finish()


class S03Setup(SpokenScene):
    def construct(self):
        D = Dish()
        plain = [kcell(c) for c in CX]
        labs = [T("kidney cell", 26, LT).move_to([c, -1.8, 0]) for c in CX]
        cred = T("Scheiffele, Serafini and colleagues, 2000", 30, LT).move_to([0, 2.4, 0])
        lab4 = D.dishlab
        self.play(*[FadeIn(m) for m in plain + labs], FadeIn(lab4), run_time=.9)
        self.at("laboratory")
        self.play(FadeIn(cred), run_time=.5)
        self.at("made kidney cells")
        self.wait(.2)
        self.at("produce")
        nlabs = [T("neuroligin", 26, YELLOW).move_to([CX[i], -1.8, 0]) for i in NL]
        self.play(*[ReplacementTransform(plain[i], kcell(CX[i], True)) for i in NL],
                  *[ReplacementTransform(labs[i], nlabs[k]) for k, i in enumerate(NL)],
                  LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in D.stubs], lag_ratio=.12), run_time=1.3)
        self.finish()


class S04Axons(SpokenScene):
    def construct(self):
        D = Dish()
        self.add(*D.cells, *D.labs, D.stubs, D.dishlab)
        self.at("under axons")
        self.play(FadeIn(D.expl), *[Create(a) for a in D.axons], run_time=1.3)
        self.at("from the")
        self.play(FadeIn(D.expl_t), FadeIn(VGroup(*D.flat_dots())), run_time=.5)
        self.play(FadeIn(D.vlab), Create(D.vlead), run_time=.5)
        self.finish()


class S05Clusters(SpokenScene):
    def construct(self):
        D = Dish()
        self.add(*D.base(), D.vlab, D.vlead)
        sp = strip(["off", "off", "off"])
        lg = legend([("lit", "seen"), ("half", "poor"), ("off", "not tested"), ("dim", "fails")], -3.62).shift(RIGHT * 0)
        self.play(FadeIn(sp), FadeIn(lg), run_time=.4)
        self.at("crossed a")
        hl = [R(2.9, 1.2, YELLOW, 0, .3, 5, CX[i], AXY) for i in NL]
        self.play(*[Create(h) for h in hl], run_time=.6)
        self.at("synaptic vesicle proteins")
        self.play(*[FadeOut(h) for h in hl], Indicate(D.vlab, color=TEAL, scale_factor=1.06), run_time=.7)
        self.at("gathered into")
        anims = []
        for i in NL:
            for j, d in enumerate(D.dots[i]):
                dx, dy = CLUS[j]
                anims.append(d.animate.move_to([CX[i] + dx, AXY + dy, 0]).scale(1.7).set_fill(TEAL, opacity=1))
        self.play(*anims, FadeOut(D.vlab), FadeOut(D.vlead), run_time=.9)
        self.at("clusters")
        clabs = [VGroup(T("cluster", 26, TEAL).move_to([CX[i], -1.25, 0]),
                        Line([CX[i], -1.05, 0], [CX[i], -.8, 0], color=TEAL, stroke_width=3)) for i in NL]
        D2 = Dish(clustered=True)
        self.play(*[FadeIn(h) for h in D2.halos], *[FadeIn(c) for c in clabs], run_time=.6)
        new = strip(["lit", "off", "off"])
        self.play(ReplacementTransform(sp[0][0], new[0][0]), run_time=.5)
        self.finish()


def membrane(x0, x1, y):
    return R(x1 - x0, .32, GREY, .4, .1, 3, (x0 + x1) / 2, y)


VX, MY, VR = -0.9, -1.2, 1.9          # inset: vesicle x, membrane y, vesicle radius
YB = (2.7, -2.5)                         # antibody in the bath


def vesicle_closed(cy):
    return Circle(radius=VR, stroke_color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=.12).move_to([VX, cy, 0])


def vesicle_open(cy):
    return Arc(radius=VR, start_angle=-PI / 2 + .45, angle=2 * PI - .9, arc_center=[VX, cy, 0], color=TEAL, stroke_width=6)


def vstub(cy):
    return stub(VX - .88, cy - .88, TEAL, .42)


class S06Dye(SpokenScene):
    def construct(self):
        D = Dish(clustered=True)
        sp = strip(["lit", "off", "off"])
        self.add(*D.base(), sp)
        dep = chip("depolarized", TEXT, 32).move_to([3.8, 2.55, 0])
        ys = [(-2.2, .6), (-1.55, .85), (-.9, .6), (4.15, .6), (4.8, .85), (5.45, .6)]
        abs_ = VGroup(*[ab(x, y, 1.5) for x, y in ys])
        upt = T("antibodies in the bath", 28, TEXT).move_to([0, -3.25, 0])
        self.play(FadeIn(abs_), FadeIn(upt), run_time=.3)
        self.at("depolarized")
        self.play(FadeIn(dep), *[a.animate.set_stroke(TEXT, opacity=1) for a in D.axons], run_time=.5)
        self.at("clusters took up")
        flights = []
        for k, a in enumerate(abs_):
            cx = CX[NL[k // 3]]
            flights.append(a.animate.move_to([cx + (k % 3 - 1) * .35, AXY, 0]).scale(.6))
        glow = [Circle(radius=.95, stroke_color=TEXT, stroke_width=5, fill_color=TEAL,
                       fill_opacity=.5).move_to([CX[i], AXY, 0]) for i in NL]
        self.play(*[FadeIn(g) for g in glow], *flights,
                  *[d.animate.set_fill(TEXT, opacity=1) for i in NL for d in D.dots[i]], run_time=.7)
        self.at("antibodies")
        self.wait(.3)
        # inset: the inside face of a vesicle protein
        self.at("inside face")
        fade = [m for m in self.mobjects if m is not sp and m is not dep]
        self.play(FadeOut(Group(*fade), scale=1.35), run_time=.4)
        mem = membrane(-6.5, 6.5, MY)
        v = vesicle_closed(1.5)
        pst = vstub(1.5)
        tlab = T("axon terminal", 28, LT).move_to([-5.0, 3.1, 0])
        blab = T("bath", 28, LT).move_to([-5.8, -3.0, 0])
        y0 = ab(YB[0], YB[1], 2.4)
        ylab = T("antibody", 28, TEXT).move_to([YB[0] + .35, YB[1] - 1.05, 0], aligned_edge=LEFT)
        lab_in = T("inside face of the\nvesicle protein", 28, TEXT, line_spacing=1.1).move_to([4.2, 1.25, 0])
        lead = Line([2.55, 1.05, 0], [VX - .88 + .22, 1.5 - .88 + .1, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(mem), FadeIn(v), FadeIn(pst), FadeIn(tlab), FadeIn(blab), FadeIn(y0), FadeIn(ylab),
                  FadeIn(lab_in), Create(lead), run_time=.6)
        self.at("vesicle protein")
        self.play(Indicate(pst, color=TEXT, scale_factor=1.8), run_time=.8)
        # release and retrieval
        ml, mr = membrane(-6.5, VX - .82, MY), membrane(VX + .82, 6.5, MY)
        v_dock = vesicle_closed(.8)
        v_open = vesicle_open(.8)
        rel = T("released", 44, TEAL).move_to([-4.3, -2.2, 0])
        rela = Arrow([-3.0, -2.05, 0], [VX - .85, -1.3, 0], color=TEAL, stroke_width=5, buff=0, tip_length=.22)
        ret = T("retrieved", 44, TEAL).move_to([-4.9, 1.5, 0])
        reta = Arrow([-3.3, 1.5, 0], [VX - VR - .1, 1.5, 0], color=TEAL, stroke_width=5, buff=0, tip_length=.22)
        self.at("vesicles were being")
        self.play(FadeOut(lab_in), FadeOut(lead), FadeOut(ylab), Transform(v, v_dock), pst.animate.move_to([VX - .88, .8 - .88, 0]), run_time=.4)
        self.play(ReplacementTransform(v, v_open), FadeOut(mem), FadeIn(ml), FadeIn(mr),
                  y0.animate.move_to([VX, -2.25, 0]), run_time=.5)
        self.play(y0.animate.move_to([VX - .3, -.15, 0]), run_time=.4)
        self.at("released")
        self.play(FadeIn(rel), GrowArrow(rela), run_time=.4)
        v_back = vesicle_closed(1.5)
        self.at("retrieved")
        self.play(ReplacementTransform(v_open, v_back), FadeOut(ml), FadeOut(mr), FadeIn(mem),
                  pst.animate.move_to([VX - .88, 1.5 - .88, 0]), y0.animate.move_to([VX - .1, .72, 0]),
                  ReplacementTransform(rel, ret), ReplacementTransform(rela, reta), run_time=.8)
        new = strip(["lit", "lit", "off"])
        self.play(ReplacementTransform(sp[1][0], new[1][0]), run_time=.5)
        self.finish()


def mini(cx, kind, with_dots=True):
    """One small dish. kind: plain | nlg | block"""
    cell = R(3.9, 2.4, GREY, .2, .4, cx=cx, cy=-1.15) if kind == "plain" else RoundedRectangle(
        corner_radius=.4, width=3.9, height=2.4, stroke_color=GREY, stroke_width=3, fill_color=YELLOW,
        fill_opacity=.2).move_to([cx, -1.15, 0])
    axn = R(4.0, .6, AXC, .35, .28, cx=cx, cy=.4)
    parts = VGroup(cell)
    if kind != "plain":
        parts.add(*[stub(cx + dx, .2, YELLOW) for dx in (-1.0, 0, 1.0)])
    parts.add(axn)
    if with_dots:
        if kind == "nlg":
            pts = [(cx - .36, .33), (cx - .1, .52), (cx + .16, .3), (cx + .38, .5), (cx, .4)]
            parts.add(*[vdot(x, y, .17) for x, y in pts])
        else:
            pts = [(cx - 1.5, .4), (cx - .75, .5), (cx, .3), (cx + .75, .5), (cx + 1.5, .4)]
            parts.add(*[vdot(x, y, .11, .4) for x, y in pts])
    return parts


class S07Controls(SpokenScene):
    def construct(self):
        sp = strip(["lit", "lit", "off"])
        self.add(sp)
        MX = [-4.5, 0, 4.5]
        d1 = mini(MX[0], "plain")
        t1 = T("control cells", 28, LT).move_to([MX[0], 2.1, 0])
        r1 = T("no clusters", 32, LT).move_to([MX[0], -3.0, 0])
        self.at("control cells")
        self.play(FadeIn(d1), FadeIn(t1), run_time=.5)
        d2 = mini(MX[1], "nlg")
        t2 = T("neuroligin cells", 28, YELLOW).move_to([MX[1], 2.1, 0])
        r2 = T("clusters", 32, TEAL).move_to([MX[1], -3.0, 0])
        self.at("did not do this")
        self.play(FadeIn(r1), FadeIn(d2), FadeIn(t2), FadeIn(r2), run_time=.6)
        d3 = mini(MX[2], "block")
        t3 = VGroup(T("neuroligin cells", 28, YELLOW), T("+ soluble beta-neurexin", 26, BLUE)).arrange(DOWN, buff=.08).move_to([MX[2], 2.25, 0])
        sol = VGroup(*[stub(MX[2] + dx - .9, 1.35, BLUE) for dx in (-1.0, 0, 1.0)])
        self.at("soluble beta")
        self.play(FadeIn(d3), FadeIn(t3), FadeIn(sol), run_time=.7)
        self.at("which binds")
        self.play(*[s_.animate.shift(DOWN * .75 + RIGHT * .9) for s_ in sol], run_time=.8)
        r3 = T("blocked", 32, RED).move_to([MX[2], -3.0, 0])
        self.at("the effect")
        self.play(FadeIn(r3), run_time=.5)
        self.finish()


def rev_cell(color):
    return R(7.0, CELL_H, GREY, .2, .5, cx=0, cy=CELL_Y + 0) if color == GREY else RoundedRectangle(
        corner_radius=.5, width=7.0, height=CELL_H, stroke_color=GREY, stroke_width=3, fill_color=YELLOW,
        fill_opacity=.2).move_to([0, CELL_Y, 0])


def rev_stubs(color):
    return VGroup(*[stub(x, .18, color) for x in (-2.4, -1.2, 0, 1.2, 2.4)])


class S08Reverse(SpokenScene):
    def construct(self):
        cell_f = rev_cell(YELLOW)
        stubs_f = rev_stubs(YELLOW)
        band = R(12.4, .9, AXC, .3, .4, cx=0, cy=.7)
        dots = VGroup(*[vdot(x, y, .17) for x, y in [(-.5, .55), (-.2, .85), (.15, .58), (.45, .83), (0, .7)]])
        lab_ax = T("axon", 28, LT).move_to([-5.0, 1.75, 0])
        lab_nl = T("neuroligin", 28, YELLOW).move_to([0, -1.1, 0])
        self.add(cell_f, stubs_f, band, dots, lab_ax, lab_nl)
        self.at("other way")
        self.play(Indicate(stubs_f, color=YELLOW, scale_factor=1.2), run_time=.7)
        cell_b = rev_cell(GREY)
        stubs_b = rev_stubs(BLUE)
        lab_dn = T("dendrite", 28, LT).move_to([-5.0, 1.75, 0])
        lab_nx = T("neurexin", 28, BLUE).move_to([0, -1.1, 0])
        lab_bare = T("bare cell", 28, LT).move_to([0, -2.4, 0])
        self.at("on a bare cell")
        self.play(ReplacementTransform(cell_f, cell_b), ReplacementTransform(stubs_f, stubs_b), FadeOut(dots),
                  ReplacementTransform(lab_ax, lab_dn), ReplacementTransform(lab_nl, lab_nx), FadeIn(lab_bare), run_time=1.0)
        pp = VGroup(*[stub(x, .7, PURPLE, .3) for x in (-4.2, -2.4, 2.4, 4.2)])
        self.at("clusters postsynaptic proteins")
        self.play(FadeIn(pp), run_time=.5)
        self.play(*[m.animate.move_to([x, .7, 0]) for m, x in zip(pp, (-.7, -.25, .25, .7))], run_time=1.0)
        ppl = T("postsynaptic proteins", 28, PURPLE).move_to([0, 1.9, 0])
        self.play(FadeIn(ppl), run_time=.4)
        cred = T("Credit: Craig laboratory, 2004", 24, LT).move_to([0, -3.4, 0])
        self.at("in dendrites")
        self.play(FadeIn(cred), Indicate(pp, color=PURPLE, scale_factor=1.15), run_time=.7)
        self.finish()


def reverse_final():
    band = R(12.4, .9, AXC, .3, .4, cx=0, cy=.7)
    cell_b = rev_cell(GREY)
    stubs_b = rev_stubs(BLUE)
    lab_dn = T("dendrite", 28, LT).move_to([-5.0, 1.75, 0])
    lab_nx = T("neurexin", 28, BLUE).move_to([0, -1.1, 0])
    lab_bare = T("bare cell", 28, LT).move_to([0, -2.4, 0])
    pp = VGroup(*[stub(x, .7, PURPLE, .3) for x in (-.7, -.25, .25, .7)])
    ppl = T("postsynaptic proteins", 28, PURPLE).move_to([0, 1.9, 0])
    cred = T("Credit: Craig laboratory, 2004", 24, LT).move_to([0, -3.4, 0])
    return [band, cell_b, stubs_b, lab_dn, lab_nx, lab_bare, pp, ppl, cred]


class S09Beat(NarratedScene):
    def construct(self):
        self.add(*reverse_final())
        self.finish()


def eq_row(y=2.7, size=34):
    a = chip("bare cell", GREY, size)
    p = T("+", 40, TEXT)
    n = chip("neuroligin", YELLOW, size)
    arrow = Arrow(LEFT * .6, RIGHT * .6, color=GREY, stroke_width=6, buff=0)
    r = chip("terminal starts", TEAL, size)
    g = VGroup(a, p, n, arrow, r).arrange(RIGHT, buff=.35).move_to([0, y, 0])
    ph = VGroup(DashedVMobject(R(r.width, r.height, GREY, 0, .15, 3), num_dashes=36), T("?", size + 6, GREY)).move_to(r)
    return g, ph


def def_card(cy, h, word, lines, wsize=56, lsize=36, gap=.15):
    card = R(12.6, h, GREY, .1, .25, 3, 0, cy)
    w = T(word, wsize, TEXT, font=TITLE_FONT).move_to([0, cy + h / 2 - .2 - wsize / 100, 0])
    d = VGroup(*[T(s, lsize, TEXT) for s in lines]).arrange(DOWN, buff=gap)
    d.move_to([0, cy - (.3 if len(lines) > 1 else .0) - .2, 0])
    return VGroup(card, w, d)


class S10Suff(SpokenScene):
    def construct(self):
        g, ph = eq_row(2.7)
        a, p, n, arrow, r = g
        card = def_card(-.45, 4.4, "sufficient", ["adding it is enough to produce the effect,", "in a system otherwise ready"], 60, 36, .2)
        self.add(a, p, n, arrow, ph)
        self.at("is sufficient")
        self.play(FadeIn(card[0]), FadeIn(card[1]), FadeIn(card[2][0]), run_time=.7)
        self.at("under these conditions")
        self.play(FadeIn(card[2][1]), run_time=.6)
        self.at("to start a terminal")
        self.play(ReplacementTransform(ph, r), run_time=.7)
        self.finish()


def two_cards():
    c1 = def_card(2.45, 2.5, "sufficient", ["adding it is enough to produce the effect,", "in a system otherwise ready"], 44, 28, .1)
    c2 = def_card(-1.3, 4.0, "necessary", ["the effect does not happen without it"], 60, 38)
    q = T("?", 110, GREY).move_to([5.3, -1.3, 0])
    return c1, c2, q


class S11Nec(SpokenScene):
    def construct(self):
        g, ph = eq_row(2.7)
        big = def_card(-.45, 4.4, "sufficient", ["adding it is enough to produce the effect,", "in a system otherwise ready"], 60, 36, .2)
        self.add(g, big)
        c1, c2, q = two_cards()
        self.play(FadeOut(g), ReplacementTransform(big, c1), run_time=.5)
        self.at("necessary")
        self.play(FadeIn(c2), FadeIn(q), run_time=.6)
        self.finish()


def pred_cards():
    head = T("Predict", 48, TEXT, font=TITLE_FONT).move_to([-5.5, 3.25, 0])
    c1 = chip("no alpha-neurexins", BLUE, 28).move_to([-2.0, 3.25, 0])
    orr = T("or", 26, LT).move_to([.5, 3.25, 0])
    c2 = chip("no neuroligins 1, 2, 3", YELLOW, 28).move_to([3.3, 3.25, 0])
    out = []
    specs = [("Fewer\nsynapses", 3, None), ("Normal\nsynapses", 9, None), ("There, but\nnot working", 9, "dim")]
    for k, (txt, nfill, lp) in enumerate(specs):
        x = -4.3 + 4.3 * k
        card = R(4.0, 5.7, GREY, .1, .25, 3, x, -.7)
        dots = VGroup()
        for i in range(9):
            px, py = x + (i % 3 - 1) * .75, 1.3 + (1 - i // 3) * .75
            if i < nfill:
                dots.add(Dot([px, py, 0], radius=.24, color=GREEN))
            else:
                dots.add(Circle(radius=.24, stroke_color=GREY, stroke_width=2).move_to([px, py, 0]))
        parts = VGroup(card, dots)
        lab = T(txt, 36, TEXT, line_spacing=1.0).move_to([x, -1.2, 0])
        parts.add(lab)
        if lp:
            parts.add(lamp("dim", .38, x, -2.75))
        out.append(parts)
    return head, c1, orr, c2, out


class S12Predict(SpokenScene):
    def construct(self):
        c1_, c2_, q_ = two_cards()
        self.add(c1_, c2_, q_)
        head, c1, orr, c2, cards = pred_cards()
        self.at("mice lack")
        self.play(FadeOut(c1_), FadeOut(c2_), FadeOut(q_), FadeIn(head), FadeIn(c1), run_time=.5)
        self.at("or")
        self.play(FadeIn(orr), FadeIn(c2), run_time=.5)
        self.at("fewer synapses")
        self.play(FadeIn(cards[0]), run_time=.5)
        self.at("normal ones")
        self.play(FadeIn(cards[1]), run_time=.5)
        self.at("synapses that are there")
        self.play(FadeIn(cards[2]), run_time=.6)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        head, c1, orr, c2, cards = pred_cards()
        self.add(head, c1, orr, c2, *cards)
        self.finish()


def tool_panels():
    p1 = R(6.2, 5.0, GREY, .08, .3, 3, -3.4, .1)
    p2 = R(6.2, 5.0, GREY, .08, .3, 3, 3.4, .1)
    m = micro().scale_to_fit_height(3.0).move_to([-3.4, .55, 0])
    p = pipette().scale_to_fit_height(3.0).move_to([3.4, .55, 0])
    l1 = T("count the synapses", 32, TEXT).move_to([-3.4, -1.8, 0])
    l2 = T("record what they do", 32, TEXT).move_to([3.4, -1.8, 0])
    return p1, p2, m, p, l1, l2


class S14Measure(SpokenScene):
    def construct(self):
        p1, p2, m, p, l1, l2 = tool_panels()
        self.at("two measurements")
        self.play(FadeIn(p1), FadeIn(p2), run_time=.6)
        self.at("count the synapses")
        self.play(FadeIn(m, shift=UP * .2), FadeIn(l1), run_time=.7)
        self.at("record what they do")
        self.play(FadeIn(p, shift=UP * .2), FadeIn(l2), run_time=.7)
        self.finish()


class S15Nrx(SpokenScene):
    def construct(self):
        tb = Table()
        p1, p2, m, p, l1, l2 = tool_panels()
        self.add(p1, p2, m, p, l1, l2)
        self.play(FadeOut(p1), FadeOut(p2), FadeOut(l1), FadeOut(l2),
                  m.animate.scale_to_fit_height(.8).move_to([XT, 3.35, 0]),
                  p.animate.scale_to_fit_height(.8).move_to([XC, 3.35, 0]),
                  FadeIn(tb.hdr), FadeIn(tb.lab1), run_time=1.2)
        lg = legend([("lit", "seen"), ("half", "poor"), ("off", "not tested"), ("dim", "fails")], -3.55)
        self.play(FadeIn(lg), run_time=.5)
        self.at("marcus")
        self.play(FadeIn(tb.cred1), run_time=.5)
        chips = [gone_chip(f"alpha-neurexin {k}", BLUE, 30, -4.3 + 4.3 * (k - 1), -.7) for k in (1, 2, 3)]
        self.at("lacking")
        self.play(LaggedStart(*[FadeIn(c, scale=.9) for c in chips], lag_ratio=.35), run_time=1.0)
        self.at("alpha")
        self.play(Indicate(tb.lab1, color=BLUE, scale_factor=1.05), run_time=.7)
        self.play(FadeOut(VGroup(*chips)), FadeOut(lg), run_time=.4)
        self.finish()


def compact_bars(cx, y0, lengths, colors, values, title):
    x0, ref_len = cx - 2.05, 4.1
    axis = VGroup(T(title, 24, LT).move_to([cx, y0 + .65, 0]),
                  T("schematic; dashed = control", 22, LT).move_to([cx, y0 - 2.05, 0]))
    groups = []
    for k, (fraction, col, value) in enumerate(zip(lengths, colors, values)):
        y = y0 - k * .95
        ref = DashedVMobject(Rectangle(width=ref_len, height=.3, stroke_color=LT,
            stroke_width=2), num_dashes=36).move_to([cx, y, 0])
        bar = Rectangle(width=ref_len*fraction, height=.3, stroke_color=col,
            fill_color=col, fill_opacity=.65).move_to([x0+ref_len*fraction/2, y, 0])
        label = T(("excitatory", "inhibitory")[k], 24, TEXT).move_to([x0, y+.35, 0], aligned_edge=LEFT)
        val = T(value, 22, col).move_to([x0+ref_len, y+.35, 0], aligned_edge=RIGHT)
        groups.append((VGroup(ref, bar, label), val, bar))
    return axis, groups


def chart1(tb):
    return compact_bars(XT, -.55, [.97, .85], [GREEN, GREEN],
                        ["near normal", "moderately fewer"], "synapse density")


class S16Nrx2(SpokenScene):
    def construct(self):
        tb = Table()
        self.add(*tb.upto("s16"))
        ax, items = chart1(tb)
        self.at("excitatory synapses")
        self.play(FadeIn(ax), FadeIn(items[0][0]), run_time=.7)
        self.at("near normal")
        self.play(FadeIn(items[0][1]), FadeIn(tb.r1t), run_time=.5)
        self.at("inhibitory synapses")
        self.play(FadeIn(items[1][0]), run_time=.7)
        self.at("moderately fewer")
        self.play(FadeIn(items[1][1]), FadeIn(tb.r1tn), run_time=.5)
        self.finish()


class S17Nrx3(SpokenScene):
    def construct(self):
        tb = Table()
        self.add(*tb.upto("s17"))
        ax, items = chart1(tb)
        self.add(ax, *[VGroup(a, b) for a, b, _ in items])
        self.at("release transmitter")
        self.play(FadeIn(tb.r1r_off), run_time=.5)
        self.at("poorly")
        self.play(ReplacementTransform(tb.r1r_off, tb.r1r), FadeIn(tb.r1rn), FadeIn(tb.r1s), FadeIn(tb.r1sn), run_time=.7)
        self.finish()


class S18Beat(NarratedScene):
    def construct(self):
        tb = Table()
        self.add(*tb.upto("s19"))
        ax, items = chart1(tb)
        self.add(ax, *[VGroup(a, b) for a, b, _ in items])
        self.finish()


class S19Nlg(SpokenScene):
    def construct(self):
        tb = Table()
        self.add(*tb.upto("s19"))
        ax, items = chart1(tb)
        old = VGroup(ax, *[VGroup(a, b) for a, b, _ in items])
        self.add(old)
        self.play(FadeOut(old), run_time=.5)
        self.at("mice lacking")
        self.play(FadeIn(tb.lab2), run_time=.5)
        chips = [gone_chip(f"neuroligin {k}", YELLOW, 30, -4.3 + 4.3 * (k - 1), -2.4) for k in (1, 2, 3)]
        self.at("1")
        self.play(FadeIn(chips[0], scale=.9), run_time=.4)
        self.at("2")
        self.play(FadeIn(chips[1], scale=.9), run_time=.4)
        self.at("3")
        self.play(FadeIn(chips[2], scale=.9), run_time=.4)
        self.at("brainstem")
        self.play(FadeIn(tb.lab2b), FadeOut(VGroup(*chips)), run_time=.5)
        self.at("normal in number")
        self.play(FadeIn(tb.r2t), FadeIn(tb.r2tn), run_time=.7)
        self.finish()


def chart2():
    ax, items = compact_bars(XC, -1.9, [.85, .65], [RED, RED],
                             ["impaired", "impaired more"], "transmission")
    ax[1].move_to([XC, -3.4, 0])
    ax.add(T("relative size not shown", 26, TEXT).move_to([-3.5, -2.45, 0]))
    return ax, items


class S20Nlg2(SpokenScene):
    def construct(self):
        tb = Table()
        self.add(*tb.upto("s20"))
        self.at("transmission")
        self.play(FadeIn(tb.r2c_off), FadeIn(tb.r2c_offt), run_time=.5)
        self.at("impaired")
        self.play(ReplacementTransform(tb.r2c_off, tb.r2c), ReplacementTransform(tb.r2c_offt, tb.r2ct), run_time=.6)
        ax, items = chart2()
        self.at("more so")
        self.play(FadeIn(ax), FadeIn(items[0][0]), FadeIn(items[0][1]), run_time=.6)
        self.at("inhibitory")
        self.play(FadeIn(items[1][0]), FadeIn(items[1][1]), run_time=.6)
        self.finish()


class S21Beat(NarratedScene):
    def construct(self):
        tb = Table()
        self.add(*tb.upto("s22"))
        ax, items = chart2()
        self.add(ax, *[VGroup(a, b) for a, b, _ in items])
        self.finish()


class S22Table(SpokenScene):
    def construct(self):
        tb = Table()
        self.add(*tb.upto("s22"))
        ax, items = chart2()
        panel = VGroup(ax, *[VGroup(a, b) for a, b, _ in items])
        self.add(panel)
        self.play(FadeOut(panel), run_time=.4)
        self.at("stargazer")
        self.play(FadeIn(tb.lab3), run_time=.4)
        self.at("first film")
        self.play(LaggedStart(FadeIn(tb.r3t), FadeIn(tb.r3r), FadeIn(tb.r3a), FadeIn(tb.r3b),
                              FadeIn(tb.r3al), FadeIn(tb.r3bl), lag_ratio=.25), run_time=1.4)
        gbox = R(2.9, 5.35, GREEN, 0, .3, 5, XT, -.65)
        self.at("counting found")
        self.play(Create(gbox), run_time=.6)
        self.at("recording found")
        self.play(FadeOut(gbox), Indicate(tb.pip, color=TEXT, scale_factor=1.3), run_time=.7)
        red = VGroup(Circle(radius=.64, stroke_color=RED, stroke_width=5).move_to([XR, YR[0], 0]),
                     R(5.1, 1.8, RED, 0, .45, 5, XC + .05, YR[1]),
                     Circle(radius=.52, stroke_color=RED, stroke_width=5).move_to([XS + .55, YR[2], 0]))
        self.at("something wrong")
        self.play(LaggedStart(*[Create(b) for b in red], lag_ratio=.3), run_time=.9)
        self.finish()


def dot_grid(cx, cy, nfill, dim=(), color=GREEN, r=.32, sp=1.0):
    g = VGroup()
    for i in range(8):
        px, py = cx + (i % 4 - 1.5) * sp, cy + (.5 - i // 4) * sp
        if i < nfill and i not in dim:
            g.add(Dot([px, py, 0], radius=r, color=color))
        else:
            g.add(Circle(radius=r, stroke_color=GREY, stroke_width=2).move_to([px, py, 0]))
    return g


class S23Caveat(SpokenScene):
    def construct(self):
        pl = R(6.5, 7.0, GREY, .08, .3, 3, -3.4, -.1)
        pr = R(6.5, 7.0, GREY, .08, .3, 3, 3.4, -.1)
        lh = T("the usual result", 38, TEXT).move_to([-3.4, 2.4, 0])
        lg = dot_grid(-3.4, .5, 8)
        lc = T("number kept", 40, GREEN).move_to([-3.4, -1.5, 0])
        self.play(FadeIn(pl), FadeIn(lh), FadeIn(lg), FadeIn(lc), run_time=.9)
        self.at("never change number")
        self.play(Indicate(lc, color=GREEN, scale_factor=1.1), run_time=.7)
        rh = T("some interneurons", 38, TEXT).move_to([3.4, 2.4, 0])
        cx_ = chip("all neurexins deleted", BLUE, 30).move_to([3.4, 1.5, 0])
        rg = dot_grid(3.4, -.2, 8)
        self.at("deleting every")
        self.play(FadeIn(pr), FadeIn(rh), FadeIn(cx_), run_time=.6)
        self.at("interneurons")
        self.play(FadeIn(rg), run_time=.6)
        rc = VGroup(T("fewer synapses", 40, RED), T("size varies by cell type", 26, LT)).arrange(DOWN, buff=.15).move_to([3.4, -1.85, 0])
        self.at("lower synapse number")
        self.play(rg[7].animate.set_stroke(GREY, 2).set_fill(GREY, opacity=0).set_opacity(.4), FadeIn(rc), run_time=.8)
        self.finish()


class S24Why(SpokenScene):
    def construct(self):
        l1 = T("Why would the brain", 56, TEXT, font=TITLE_FONT).move_to([0, 2.4, 0])
        l2 = T("manage without it?", 56, TEXT, font=TITLE_FONT).move_to([0, 1.2, 0])
        b1 = DashedVMobject(R(5.6, 2.4, GREY, 0, .3, 3, -3.1, -1.4), num_dashes=50)
        b2 = DashedVMobject(R(5.6, 2.4, GREY, 0, .3, 3, 3.1, -1.4), num_dashes=50)
        q1 = T("overlap", 44, TEXT).move_to([-3.1, -1.4, 0])
        q2 = T("specify or check", 44, TEXT).move_to([3.1, -1.4, 0])
        self.play(FadeIn(l1), run_time=.5)
        self.at("manage without")
        self.play(FadeIn(l2), run_time=.5)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(q1), FadeIn(q2), run_time=.5)
        self.finish()


def stage_bands():
    top = R(13.2, 1.2, GREY, .15, .5, cx=0, cy=3.15)
    bot = R(13.2, 1.2, GREY, .15, .5, cx=0, cy=-3.15)
    tl = T("axon terminal", 26, LT).move_to([-5.0, 3.15, 0])
    bl = T("dendrite", 26, LT).move_to([-5.5, -3.15, 0])
    return top, bot, tl, bl


def rod(x, ca, cb, gap=.28):
    """A contact: stems from both membranes to two stubs; gap = half distance between the stubs."""
    u, l = gap, -gap
    s1 = Line([x, 2.55, 0], [x, u + .15, 0], color=ca, stroke_width=8)
    s2 = Line([x, -2.55, 0], [x, l - .15, 0], color=cb, stroke_width=8)
    a = stub(x, u, ca, .42)
    b = stub(x, l, cb, .42)
    return VGroup(s1, s2, a, b)


FAM_X = [-5.0, -1.9, 1.2, 4.3]


class S25R1(SpokenScene):
    def construct(self):
        top, bot, tl, bl = stage_bands()
        self.play(FadeIn(top), FadeIn(bot), FadeIn(tl), FadeIn(bl), run_time=.5)
        ov = T("overlap", 60, TEXT, font=TITLE_FONT).move_to([0, 0, 0])
        self.play(FadeIn(ov), run_time=.6)
        cols = [(BLUE, YELLOW), (TEXT, TEXT), (TEXT, TEXT), (TEXT, TEXT)]
        open_ = [rod(x, a, b, 1.0) for x, (a, b) in zip(FAM_X, cols)]
        closed = [rod(x, a, b, .28) for x, (a, b) in zip(FAM_X, cols)]
        names = [VGroup(T("neurexin–", 24, TEXT), T("neuroligin", 24, TEXT)).arrange(DOWN, buff=.04),
                 T("SynCAM", 26, TEXT), T("LRRTMs", 26, TEXT), T("cadherins", 26, TEXT)]
        for nm, x in zip(names, FAM_X):
            nm.move_to([x + .5, 0, 0], aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(o) for o in open_], lag_ratio=.2), run_time=1.2)
        self.at("several organizers")
        self.play(FadeOut(ov), *[FadeIn(n) for n in names], run_time=.5)
        self.at("start contacts")
        self.play(*[Transform(o, c) for o, c in zip(open_, closed)], run_time=.9)
        self.at("removing one family")
        x_ = cross_mark(FAM_X[0], 0, .25, RED, 7)
        self.play(FadeOut(open_[0]), names[0].animate.set_opacity(.85), FadeIn(x_), run_time=.7)
        hold = T("others still hold", 30, GREEN).move_to([2.7, -2.0, 0])
        self.at("leaves others")
        self.play(*[Indicate(o, color=GREEN, scale_factor=1.05) for o in open_[1:]], FadeIn(hold), run_time=.9)
        self.finish()


class S26R2(SpokenScene):
    def construct(self):
        top, bot, tl, bl = stage_bands()
        self.add(top, bot, tl, bl)
        XA, XB = -3.8, 3.8
        rA, rB = rod(XA, GREY, GREY, 1.0), rod(XB, GREY, GREY, 1.0)
        self.play(FadeIn(rA), FadeIn(rB), run_time=.4)
        self.play(Transform(rA, rod(XA, GREY, GREY)), Transform(rB, rod(XB, GREY, GREY)), run_time=.5)
        org = chip("organizer", TEXT, 32).move_to([0, 0, 0])
        arA = Arrow([-1.3, 0, 0], [XA + .45, 0, 0], buff=0, color=LT, stroke_width=5, tip_length=.22)
        arB = Arrow([1.3, 0, 0], [XB - .45, 0, 0], buff=0, color=LT, stroke_width=5, tip_length=.22)
        self.at("some organizers")
        self.play(FadeIn(org), run_time=.5)
        tagA = chip("excitatory", ORANGE, 28).move_to([-5.4, .0, 0])
        tagB = chip("inhibitory", PINK, 28).move_to([5.4, .0, 0])
        self.at("specify")
        self.play(GrowArrow(arA), GrowArrow(arB), run_time=.35)
        self.play(Transform(rA, rod(XA, ORANGE, ORANGE)), Transform(rB, rod(XB, PINK, PINK)), FadeIn(tagA), FadeIn(tagB), run_time=.5)
        ca, cb = tick(XA + .8, -1.15, 1.2), tick(XB - .8, -1.15, 1.2)
        chk = T("checked", 26, GREEN).move_to([0, -1.15, 0])
        self.at("check")
        self.play(Create(ca), Create(cb), FadeIn(chk), run_time=.6)
        st = VGroup(chip("starts contacts", GREY, 28), cross_mark(-1.35, 0, .2, RED, 6)).move_to([0, -2.0, 0])
        st[1].move_to(st[0].get_corner(UL) + LEFT * .05)
        st[0][1][0].set_stroke(RED, 3).set_fill(RED, .08)
        st[0][1][1].set_opacity(.6)
        self.at("rather than start")
        self.play(FadeIn(st), run_time=.5)
        self.finish()


class S27Take(SpokenScene):
    def construct(self):
        c1 = R(6.3, 6.0, GREY, .08, .3, 3, -3.4, .55)
        c2 = R(6.3, 6.0, GREY, .08, .3, 3, 3.4, .55)
        di = dish_icon().scale_to_fit_width(5.2).move_to([-3.4, 1.65, 0])
        mo = brain_icon().scale_to_fit_height(2.9).move_to([3.4, 1.65, 0])
        h1 = T("dish", 44, TEXT, font=TITLE_FONT).move_to([-3.4, -.3, 0])
        d1 = T("what one protein\ncan start", 30, TEXT).move_to([-3.4, -1.45, 0])
        h2 = T("mouse", 44, TEXT, font=TITLE_FONT).move_to([3.4, -.3, 0])
        d2 = T("what the brain\ncannot do without", 30, TEXT).move_to([3.4, -1.45, 0])
        self.at("a dish tests")
        self.play(FadeIn(c1), FadeIn(di), FadeIn(h1), run_time=.7)
        self.at("what one protein can start")
        self.play(FadeIn(d1), run_time=.5)
        self.at("a mouse tests")
        self.play(FadeIn(c2), FadeIn(mo), FadeIn(h2), run_time=.7)
        self.at("what the brain cannot do without")
        self.play(FadeIn(d2), run_time=.5)
        rule = T("Measure function, as well as count.", 42, GOLD, font=TITLE_FONT).move_to([0, -2.85, 0])
        pip = pipette().scale_to_fit_height(.9).move_to([-6.0, -3.05, 0])
        mic = micro().scale_to_fit_height(.9).move_to([6.0, -3.05, 0])
        self.at("measure function")
        self.play(FadeIn(rule), FadeIn(pip), run_time=.7)
        self.at("as well as count")
        self.play(FadeIn(mic), Indicate(rule, color=GOLD, scale_factor=1.04), run_time=.6)
        self.finish()


class S28End(NarratedScene):
    def construct(self):
        line = VGroup(T("A dish shows what can start;", 48, TEXT, font=TITLE_FONT),
                      T("a mouse shows what is needed.", 48, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=.22).move_to([0, 1.9, 0])
        icons = VGroup(lamp("lit", .6), micro().scale_to_fit_height(1.8),
                       pipette().scale_to_fit_height(1.8)).arrange(RIGHT, buff=1.6).move_to([0, -.6, 0])
        url = T("biochemistrypedia.com", 36, TEAL).move_to([0, -2.5, 0])
        self.play(FadeIn(line), FadeIn(icons), run_time=.6)
        self.play(FadeIn(url), run_time=.4)
        self.finish()
