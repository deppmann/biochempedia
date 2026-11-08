"""There, but Not Working  (Chapter 1 of Synapses in the Brain: Adhesion, Scaffolds and Astrocytes)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by all chapters; taken from scenes.old.py)
  YELLOW = neuroligin            BLUE   = neurexin           (not used in this chapter)
  TEAL   = glutamate / acetylcholine vesicles and transmitter; PINK = GABA contacts and vesicles
  GREEN  = working / lit lamp / normal
  RED    = blocked / impaired / absent / magnesium block / "fails"
  GREY   = cells, membranes, scaffold (PSD-95), de-emphasized outlines
  GREYL  = light grey for every label that sits on the dark ground, and for receptors before they are named
  PURPLE = NMDA receptors and their response
  ORANGE = AMPA receptors and their response
  PINK   = GABA-A receptors
  TEXT (white) = stargazin, the co-agonist, glutamate receptors (s03), neutral labels and recordings
  GOLD   = the rule to keep (used once, in the guiding-idea card)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#D98CB3"
GREYL = "#C3C9D6"
PANEL = "#171b25"

NAMES = ["There", "Releases", "Responds"]


# ---------------------------------------------------------------------------------------------
# small drawing helpers
# ---------------------------------------------------------------------------------------------
WALLS = [(-1.0, 1.9), (-0.45, 0.5), (-0.45, -0.55), (-0.7, -1.0)]   # canonical receptor: a funnel with a stem


def _wall(cx, cy, s, sign):
    return [[cx + sign * x * s, cy + y * s, 0] for x, y in WALLS]


def chan(cx, cy, s=1.0, color=ORANGE, sw=5, ghost=False):
    """A receptor channel: a funnel that opens to the cleft, with a stem through the membrane.
    A labelled cartoon, not a structure. (cx, cy) is the centre of the membrane. VGroup(fill, left, right)."""
    pl = VMobject(stroke_color=GREY if ghost else color, stroke_width=sw).set_points_as_corners(_wall(cx, cy, s, -1))
    pr = VMobject(stroke_color=GREY if ghost else color, stroke_width=sw).set_points_as_corners(_wall(cx, cy, s, 1))
    fill = Polygon(*[[cx + x * s, cy + y * s, 0] for x, y in
                     [(-1.0, 1.9), (-0.45, 0.5), (-0.45, -0.55), (0.45, -0.55), (0.45, 0.5), (1.0, 1.9)]],
                   stroke_width=0, fill_color=color, fill_opacity=0)
    if ghost:
        pl, pr = DashedVMobject(pl, num_dashes=12), DashedVMobject(pr, num_dashes=12)
        for p in (pl, pr):
            p.set_stroke(GREY, sw)
    return VGroup(fill, pl, pr)


def light(ch, color, op=0.55):
    return ch[0].animate.set_fill(color, op)


def box(w, h, x, y, color=GREY, fo=.2, r=.3, sw=3):
    return RoundedRectangle(corner_radius=min(r, h / 2 - .01), width=w, height=h, stroke_color=color,
                            stroke_width=sw, fill_color=color, fill_opacity=fo).move_to([x, y, 0])


def leader(a, b, color=GREYL, w=2.5):
    return Line([*a, 0], [*b, 0], color=color, stroke_width=w)


def curve(x0, y0, w, h, td, tr=0.04, onset=0.12, n=70, color=TEXT, sw=5):
    """A synaptic-current-shaped response computed from a difference of two exponentials.
    h < 0 draws an inward current (downward)."""
    s = np.linspace(0, 1, n)
    t = np.clip(s - onset, 0, None)
    f = np.exp(-t / td) - np.exp(-t / tr)
    f = f / f.max()
    pts = [[x0 + w * a, y0 + h * b, 0] for a, b in zip(s, f)]
    return VMobject(stroke_color=color, stroke_width=sw).set_points_smoothly(pts)


def tick(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=30)


def zoom_into(scene, grp, point, new=(), factor=5.0, run=1.0):
    scene.play(grp.animate.scale(factor, about_point=np.array([point[0], point[1], 0.0])).set_opacity(0),
               *[FadeIn(m) for m in new], run_time=run)
    scene.remove(grp)


def idle_until(scene, t):
    rest = t - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


# ---------------------------------------------------------------------------------------------
# the lamp
# ---------------------------------------------------------------------------------------------
class Lamp(VGroup):
    def __init__(self, x, y, text, lit=False, r=0.4, size=28, color=TEXT):
        super().__init__()
        self.glow = Circle(radius=r * 1.55, stroke_width=0).move_to([x, y, 0])
        self.bulb = Circle(radius=r, stroke_width=4).move_to([x, y, 0])
        self.label = T(text, size, color).move_to([x, y - r - 0.42, 0]).align_to([0, y - r - 0.3, 0], UP)
        self.set_lit(lit)
        self.add(self.glow, self.bulb, self.label)

    def set_lit(self, lit):
        if lit:
            self.bulb.set_fill(GREEN, 0.9).set_stroke(GREEN)
            self.glow.set_fill(GREEN, 0.2)
        else:
            self.bulb.set_fill(GREY, 0.12).set_stroke(GREY)
            self.glow.set_fill(GREY, 0.0)
        return self

    def on(self):
        return AnimationGroup(self.bulb.animate.set_fill(GREEN, 0.9).set_stroke(GREEN),
                              self.glow.animate.set_fill(GREEN, 0.2))

    def off(self):
        return AnimationGroup(self.bulb.animate.set_fill(GREY, 0.12).set_stroke(GREY),
                              self.glow.animate.set_fill(GREY, 0.0))

    def fail(self):
        return AnimationGroup(self.bulb.animate.set_fill(RED, 0.25).set_stroke(RED),
                              self.glow.animate.set_fill(RED, 0.12))


def lamps_std(lits=(False, False, False), labels=NAMES):
    return [Lamp(x, -2.5, n, l) for x, n, l in zip((-3.6, 0, 3.6), labels, lits)]


BX = (-4.4, 0, 4.4)
LBY = 3.1       # lamp row of layout B


def lamps_B(lit=True, y=LBY):
    return [Lamp(x, y, n, lit, r=0.38) for x, n in zip(BX, NAMES)]


# ---------------------------------------------------------------------------------------------
# the synapse (terminal on top, receiving cell below). Canonical coordinates, scaled by k.
# ---------------------------------------------------------------------------------------------
AX = (-2.7, -1.9, -1.1)    # AMPA receptor x positions
NX = (1.1, 2.0)            # NMDA receptor x positions
VPOS = [(-1.8, 1.8), (-.9, 1.8), (0, 1.8), (.9, 1.8), (1.8, 1.8), (-1.35, 2.55), (-.45, 2.55), (.45, 2.55),
        (1.35, 2.55)]
RS = 0.34                  # receptor scale in canonical coordinates
RCY = 0.0                  # receptor membrane-centre y (canonical)


class SynG(VGroup):
    """mode: 'neutral' (all receptors one grey), 'color' (AMPA orange, NMDA purple), 'none' (no receptors)."""

    def __init__(self, cx=0.0, cy=0.0, k=1.0, mode="neutral", rec_sw=5):
        super().__init__()
        self.cx, self.cy, self.k = cx, cy, k
        self.term = box(5.6 * k, 2.0 * k, *self.P(0, 2.2)[:2], GREY, .18, .45 * k)
        self.post = box(7.0 * k, 1.0 * k, *self.P(0, -.15)[:2], GREY, .18, .3 * k)
        self.ves = VGroup(*[Dot(self.P(x, y), radius=max(.05, .15 * k), color=TEAL) for x, y in VPOS])
        ca, cn = (GREYL, GREYL) if mode == "neutral" else (ORANGE, PURPLE)
        self.ampa = VGroup(*[chan(*self.P(x, RCY)[:2], RS * k, ca, rec_sw) for x in AX]) if mode != "none" else VGroup()
        self.nmda = VGroup(*[chan(*self.P(x, RCY)[:2], RS * k, cn, rec_sw) for x in NX]) if mode != "none" else VGroup()
        self.add(self.term, self.post, self.ves, self.ampa, self.nmda)

    def P(self, x, y):
        return np.array([self.cx + self.k * x, self.cy + self.k * y, 0.0])

    def ghost_ampa(self, color=None):
        g = VGroup(*[chan(*self.P(x, RCY)[:2], RS * self.k, GREY, 5, ghost=True) for x in AX])
        if color is not None:
            for c in g:
                for w in c[1:]:
                    w.set_stroke(color, 4)
        return g

    def all_recs(self):
        return VGroup(*self.ampa, *self.nmda)

    def top_xs(self):
        return [self.P(x, 0)[0] for x in AX + NX]


def release(scene, syn, run=1.3, targets=None):
    """Vesicles fuse at the terminal floor and glutamate drifts across the cleft to the receptors."""
    k = syn.k
    pick = [syn.ves[i] for i in (1, 2, 3)]
    scene.play(*[v.animate.move_to([v.get_center()[0], syn.P(0, 1.3)[1], 0]).scale(1.25) for v in pick],
               run_time=0.4)
    xs = targets or syn.top_xs()
    dots = VGroup(*[Dot([x, syn.P(0, 1.2)[1], 0], radius=max(.05, .09 * k), color=TEAL) for x in xs])
    scene.play(FadeIn(dots, run_time=0.2))
    scene.play(*[d.animate.move_to([d.get_center()[0], syn.P(0, .74)[1], 0]) for d in dots],
               run_time=run - 0.6)
    return dots


# ---------------------------------------------------------------------------------------------
# measurement icons (layout B: lamps on top, one measurement frame under each)
# ---------------------------------------------------------------------------------------------
FY = -0.35        # centre of the frames
FH = 3.9
CAPY = -2.85


def frame(cx, cy, w=3.9, h=FH, dashed=False):
    r = RoundedRectangle(corner_radius=.2, width=w, height=h, stroke_color=GREY, stroke_width=3,
                         fill_color=PANEL, fill_opacity=1).move_to([cx, cy, 0])
    if dashed:
        return DashedVMobject(RoundedRectangle(corner_radius=.2, width=w, height=h, stroke_color=GREY,
                                               stroke_width=3), num_dashes=40).move_to([cx, cy, 0])
    return r


def gauge(cx, cy):
    arc = Arc(radius=.9, start_angle=PI * .85, angle=-PI * .7, stroke_color=GREY, stroke_width=5).move_to(
        [cx, cy - .1, 0])
    needle = Line([cx, cy - .45, 0], [cx + .45, cy + .2, 0], color=GREY, stroke_width=5)
    hub = Dot([cx, cy - .45, 0], radius=.08, color=GREY)
    return VGroup(arc, needle, hub)


def slots_B():
    return [VGroup(frame(x, FY, dashed=True), gauge(x, FY)) for x in BX]


def icon_micro(cx):
    s = SynG(cx, FY - 1.27 * .52, .52, "neutral", rec_sw=3)
    return s


def icon_dye_parts(cx):
    term = box(2.9, 1.7, cx, FY + .35, GREY, .3, .45, 2)
    pos = [(-.8, .1), (0, .1), (.8, .1), (-.4, .75), (.4, .75), (-1.0, .75)]
    pos = pos[:5]
    ves = VGroup(*[Circle(radius=.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=.08)
                   .move_to([cx + x, FY + y, 0]) for x, y in pos])
    return term, ves


def icon_rec_parts(cx):
    cell = Circle(radius=.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.4).move_to(
        [cx + .55, FY + 1.2, 0])
    pip = Polygon([cx - 1.6, FY + 1.75, 0], [cx - 1.4, FY + 1.8, 0], [cx + .1, FY + 1.28, 0],
                  stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=.9)
    base_y = FY - .2
    base = Arrow([cx - 1.25, base_y, 0], [cx + 1.65, base_y, 0], buff=0, color=GREY, stroke_width=3,
                 tip_length=.18)
    time = T("time", 26, GREYL).move_to([cx + 1.15, base_y + .3, 0])
    cur_a = Arrow([cx - 1.25, base_y, 0], [cx - 1.25, base_y - 1.15, 0], buff=0, color=GREY, stroke_width=3,
                  tip_length=.18)
    cur_l = T("current", 26, GREYL).rotate(PI / 2).move_to([cx - 1.65, base_y - .62, 0])
    tr = curve(cx - 1.2, base_y, 2.75, -1.1, td=.16, tr=.03, onset=.2, color=TEXT)
    return VGroup(cell, pip), VGroup(base, time, cur_a, cur_l), tr


CAPS = ["electron microscope", "dye in recycling vesicles", "recording"]


def cap(i):
    return T(CAPS[i], 28, GREYL).move_to([BX[i], CAPY, 0])


def icons_final():
    """The three finished measurement panels (frame, content, caption) in their end state."""
    out = []
    m = icon_micro(BX[0])
    out.append(VGroup(frame(BX[0], FY), m, cap(0)))
    term, ves = icon_dye_parts(BX[1])
    for v in ves:
        v.set_fill(TEAL, .9)
    out.append(VGroup(frame(BX[1], FY), term, ves, cap(1)))
    a, b, tr = icon_rec_parts(BX[2])
    out.append(VGroup(frame(BX[2], FY), a, b, tr, cap(2)))
    return out


# ---------------------------------------------------------------------------------------------
# the question layout (s12 .. s17): synapse left, two response panels right
# ---------------------------------------------------------------------------------------------
QSYN = dict(cx=-3.45, cy=0.23, k=0.85)
QL = (-6.0, -3.95, -1.7)
QLY = -1.55
PW, PH = 5.8, 2.9
PCX = 3.5
PYS = (1.6, -1.55)


def q_syn(mode="color"):
    return SynG(mode=mode, **QSYN)


def q_lamps(labels, lits=(False, False, False)):
    return [Lamp(x, QLY, n, l) for x, n, l in zip(QL, labels, lits)]


def resp_panel(cy, title, color, flat=False):
    cx = PCX
    T_ = cy + PH / 2
    fr = RoundedRectangle(corner_radius=.2, width=PW, height=PH, stroke_color=GREY, stroke_width=3,
                          fill_color=PANEL, fill_opacity=1).move_to([cx, cy, 0])
    ti = T(title, 28, color).move_to([cx - PW / 2 + .3 + 1.2, T_ - .38, 0])
    ti.align_to([cx - PW / 2 + .3, 0, 0], LEFT)
    y0 = T_ - 1.1
    xl, xr = cx - PW / 2 + .85, cx + PW / 2 - .3
    ax = Arrow([xl, y0, 0], [xr, y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=.18)
    tm = T("time", 26, GREYL).move_to([xr - .55, y0 + .3, 0])
    ca = Arrow([xl, y0, 0], [xl, y0 - 1.5, 0], buff=0, color=GREY, stroke_width=3, tip_length=.18)
    cl = T("current in", 26, GREYL).rotate(PI / 2).move_to([xl - .38, y0 - .8, 0])
    if flat:
        tr = Line([xl + .25, y0, 0], [xr - .3, y0, 0], color=color, stroke_width=7)
        none = T("no response", 28, RED).move_to([cx + .6, y0 - .8, 0])
    else:
        tr = curve(xl + .25, y0, xr - xl - .6, -1.25, td=.5, tr=.05, onset=.12, color=color, sw=6)
        none = None
    return dict(frame=fr, title=ti, axes=VGroup(ax, tm, ca, cl), trace=tr, none=none, y0=y0)


def q_panels():
    return resp_panel(PYS[0], "NMDA response", PURPLE), resp_panel(PYS[1], "AMPA response", ORANGE, flat=True)


def panel_group(p):
    return VGroup(p["frame"], p["title"], p["axes"], p["trace"], *([p["none"]] if p["none"] else []))


def q_title():
    return T("stargazer", 32, TEXT, font=TITLE_FONT).move_to([0, 3.42, 0])


def q_question():
    return T("Which property failed?", 34, TEXT).move_to([-3.45, -3.3, 0])


def q_full(lit=(False, False, False), labels=("There?", "Releases?", "Responds?"), question=True):
    syn = q_syn()
    lamps = q_lamps(labels, lit)
    pn, pa = q_panels()
    mob = [q_title(), syn, *lamps, panel_group(pn), panel_group(pa)]
    qn = q_question() if question else None
    if qn is not None:
        mob.append(qn)
    return syn, lamps, pn, pa, qn, mob


# =============================================================================================
#  s00  title
# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Synapses in the Brain: Adhesion, Scaffolds and Astrocytes"
    TITLE = "There, but Not Working"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREYL)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), Write(title), GrowFromCenter(rule),
                  run_time=0.8)
        self.wait(1.7)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()


# =============================================================================================
#  s01  the question
# =============================================================================================
class S01Q(SpokenScene):
    def construct(self):
        syn = SynG(0, -.5, 1.15, "neutral")
        lamps = lamps_std()
        title = T("There, but Not Working", 32, TEXT, font=TITLE_FONT).move_to([0, 3.52, 0])
        self.add(*lamps)
        self.play(Create(syn.term), FadeIn(syn.post), FadeIn(syn.ves), FadeIn(syn.ampa), FadeIn(syn.nmda),
                  FadeIn(title), run_time=0.8)
        self.at("there")
        self.play(Indicate(lamps[0], color=TEXT, scale_factor=1.08), Indicate(syn.term, color=TEXT, scale_factor=1.03), run_time=0.5)
        self.at("releases")
        self.play(Indicate(lamps[1], color=TEXT, scale_factor=1.08), Indicate(syn.ves, color=TEAL, scale_factor=1.15), run_time=0.5)
        self.at("responds")
        self.play(Indicate(lamps[2], color=TEXT, scale_factor=1.08), Indicate(syn.all_recs(), color=TEXT, scale_factor=1.25),
                  run_time=0.5)
        self.finish()


# =============================================================================================
#  s02  the muscle fiber
# =============================================================================================
class S02Nmj(SpokenScene):
    def construct(self):
        fiber = box(13.0, 2.5, 0, -2.45, GREY, .22, .5)
        flabel = T("muscle fiber", 34, GREYL).move_to([-4.3, -2.9, 0])
        plate = box(6.0, .3, 0, -1.2, GREY, .6, .1, 2)
        rcs = VGroup(*[chan(x, -1.12, .22, GREYL, 4) for x in (-2.4, -1.6, -.8, 0, .8, 1.6, 2.4)])
        axn = Rectangle(width=.7, height=2.15, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=.25).move_to([0, 2.725, 0])
        term = Ellipse(width=5.0, height=1.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                       fill_opacity=.3).move_to([0, .75, 0])
        term.set_z_index(1)
        ves = VGroup(*[Dot([x, y, 0], radius=.13, color=TEAL) for x, y in
                       [(-1.6, .55), (-.8, .35), (0, .3), (.8, .35), (1.6, .55), (-.8, .95), (.8, .95)]])
        ves.set_z_index(2)
        l_axon = T("one axon", 32, TEXT).move_to([3.4, 2.7, 0])
        ln_axon = leader((2.15, 2.7), (.4, 2.7))
        l_site = T("one site", 32, TEXT).move_to([5.1, -.1, 0])
        ln_site = leader((3.85, -.2), (2.7, -.6))
        l_ach = T("acetylcholine", 32, TEAL).move_to([-4.6, -.3, 0])
        ln_ach = leader((-3.05, -.3), (-.9, -.5), TEAL)
        self.add(fiber)
        self.at("muscle fiber", lead=0.25)
        self.play(FadeIn(flabel), run_time=0.6)
        self.at("one motor axon")
        self.play(FadeIn(axn, shift=DOWN * .5), FadeIn(term), FadeIn(ves), run_time=0.7)
        self.play(FadeIn(l_axon), Create(ln_axon), run_time=0.4)
        self.at("one site")
        self.play(FadeIn(plate), FadeIn(rcs), FadeIn(l_site), Create(ln_site),
                  Indicate(plate, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("one transmitter")
        dots = VGroup(*[Dot([x, -.28, 0], radius=.1, color=TEAL) for x in (-1.2, -.6, 0, .6, 1.2)])
        self.play(FadeIn(l_ach), Create(ln_ach), FadeIn(dots), run_time=0.4)
        self.play(dots.animate.shift(DOWN * .4), run_time=0.7)
        self.finish()


# =============================================================================================
#  s03  a neuron in the brain
# =============================================================================================
SEGS = [((0, .55), (0, 2.0)), ((0, 2.0), (-.9, 3.2)), ((0, 2.0), (.9, 3.3)), ((0, 1.35), (-1.7, 2.2)),
        ((0, .95), (1.7, 1.8)), ((-.5, -1.0), (-2.2, -1.8)), ((-2.2, -1.8), (-4.4, -2.0)),
        ((-2.2, -1.8), (-3.2, -3.2)), ((-.2, -1.0), (-.9, -2.4)), ((-.9, -2.4), (-1.8, -3.5)),
        ((.5, -1.0), (2.2, -1.8)), ((2.2, -1.8), (4.4, -2.1)), ((2.2, -1.8), (3.2, -3.2)),
        ((.2, -1.0), (.9, -2.4)), ((.9, -2.4), (1.7, -3.5))]
ZPT = (3.3, -1.95)


def neuron():
    soma = Polygon([-.75, -1.0, 0], [.75, -1.0, 0], [0, .55, 0], stroke_color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=.4)
    lines = VGroup(*[Line([*a, 0], [*b, 0], color=GREY, stroke_width=6) for a, b in SEGS])
    dots = []
    n = 0
    for a, b in SEGS:
        L = np.hypot(b[0] - a[0], b[1] - a[1])
        m = max(2, int(L / .16))
        d = np.array([b[0] - a[0], b[1] - a[1]]) / L
        nrm = np.array([-d[1], d[0]])
        for k in range(1, m):
            f = k / m
            p = np.array(a) + (np.array(b) - np.array(a)) * f + nrm * (.2 if k % 2 else -.2)
            n += 1
            col = PINK if n % 4 == 0 else TEAL
            root = np.array(a) + (np.array(b) - np.array(a)) * f
            dots.append(VGroup(Line([*root, 0], [*p, 0], color=col, stroke_width=2),
                               Dot([p[0], p[1], 0], radius=.065, color=col)))
    return soma, lines, VGroup(*dots)


class S03Brain(SpokenScene):
    def construct(self):
        soma, lines, dots = neuron()
        nl = T("cortical pyramidal neuron", 28, GREYL).move_to([-4.2, 3.25, 0])
        self.play(FadeIn(soma), Create(lines), FadeIn(nl), run_time=1.3)
        self.at("thousands of synapses")
        self.play(FadeIn(dots, lag_ratio=.04), run_time=1.0)
        idle_until(self, 2.5)
        ang = np.arctan2(-.3, 2.2)
        ring = RoundedRectangle(corner_radius=.3, width=2.7, height=.95, stroke_color=TEXT, stroke_width=4).rotate(
            ang).move_to([*ZPT, 0])
        self.play(Create(ring), run_time=0.3)
        self.wait(.3)
        # the dendrite view
        den = box(12.6, 1.5, 0, -2.35, GREY, .25, .4)
        tl = box(4.4, 2.2, -3.4, .65, GREY, .18, .35)
        tr_ = box(4.4, 2.2, 3.4, .65, GREY, .18, .35)
        vp = [(-1.2, -.1), (-.4, -.1), (.4, -.1), (1.2, -.1), (-.8, .6), (0, .6), (.8, .6)]
        vl = VGroup(*[Dot([-3.4 + dx, .5 + dy, 0], radius=.14, color=TEAL) for dx, dy in vp])
        vr = VGroup(*[Dot([3.4 + dx, .5 + dy, 0], radius=.14, color=PINK) for dx, dy in vp])
        rl = VGroup(*[chan(x, -1.72, .4, TEXT, 5) for x in (-4.4, -3.4, -2.4)])
        rr = VGroup(*[chan(x, -1.72, .4, PINK, 5) for x in (2.4, 3.4, 4.4)])
        grp = VGroup(soma, lines, dots, ring, nl)
        zoom_into(self, grp, ZPT, new=[den, tl, vl, rl, tr_, vr, rr], factor=7.0, run=0.7)
        self.at("excitatory")
        e_h = T("Excitatory", 38, TEXT).move_to([-3.4, 3.15, 0])
        e_g = T("glutamate", 30, TEAL).move_to([-3.4, 2.35, 0])
        self.play(FadeIn(e_h), FadeIn(e_g), Indicate(tl, color=TEXT, scale_factor=1.03), run_time=0.6)
        self.at("inhibitory")
        i_h = T("Inhibitory", 38, PINK).move_to([3.4, 3.15, 0])
        i_g = T("GABA", 30, PINK).move_to([3.4, 2.35, 0])
        self.play(FadeIn(i_h), FadeIn(i_g), Indicate(tr_, color=PINK, scale_factor=1.03), run_time=0.6)
        self.at("share one dendrite")
        d_l = T("one dendrite", 30, GREYL).move_to([0, -2.5, 0])
        self.play(FadeIn(d_l), Indicate(den, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("each contact")
        self.play(Indicate(VGroup(tl, vl), color=TEXT, scale_factor=1.04),
                  Indicate(VGroup(tr_, vr), color=PINK, scale_factor=1.04), run_time=0.9)
        self.at("its kind")
        gl = T("glutamate receptors", 26, TEXT).move_to([-3.4, -2.55, 0])
        gb = T("GABA receptors", 26, PINK).move_to([3.4, -2.55, 0])
        self.play(FadeIn(gl), FadeIn(gb), Indicate(rl, color=TEXT, scale_factor=1.3),
                  Indicate(rr, color=PINK, scale_factor=1.3), run_time=0.8)
        self.finish()


# =============================================================================================
#  s04  a finished synapse does three things
# =============================================================================================
class S04Three(SpokenScene):
    def construct(self):
        syn = SynG(0, -.5, 1.15, "neutral")
        lamps = lamps_std()
        self.add(syn, *lamps)
        self.at("three things")
        self.play(Indicate(VGroup(*lamps), color=TEXT, scale_factor=1.06), run_time=0.9)
        self.at("is there")
        self.play(lamps[0].on(), Indicate(syn.term, color=GREEN, scale_factor=1.03),
                  Indicate(syn.post, color=GREEN, scale_factor=1.03), run_time=0.7)
        self.at("it releases transmitter")
        release(self, syn, run=1.6)
        self.play(lamps[1].on(), run_time=0.4)
        self.at("other side")
        self.play(*[ch.animate.set_color(GREEN) for ch in syn.all_recs()],
                  syn.post.animate.set_fill(GREEN, .35), run_time=0.5)
        self.at("responds")
        self.play(lamps[2].on(), Indicate(syn.all_recs(), color=GREEN, scale_factor=1.3), run_time=0.6)
        self.finish()


# =============================================================================================
#  s05  they can come apart
# =============================================================================================
class S05Apart(SpokenScene):
    def construct(self):
        syn = SynG(0, -.5, 1.15, "neutral")
        lamps = lamps_std((True, True, True))
        syn.all_recs().set_color(GREEN)
        syn.post.set_fill(GREEN, .35)
        self.add(syn, *lamps)
        self.at("come apart", lead=0.3)
        self.play(FadeOut(syn),
                  *[l.animate.shift([x - ox, LBY + 2.5, 0]) for l, x, ox in zip(lamps, BX, (-3.6, 0, 3.6))], run_time=0.9)
        self.play(*[l.off() for l in lamps], run_time=0.3)
        self.at("each needs")
        sl = slots_B()
        self.play(LaggedStart(*[FadeIn(s) for s in sl], lag_ratio=.25), run_time=0.9)
        self.finish()


# =============================================================================================
#  s06  three measurements
# =============================================================================================
class S06Measure(SpokenScene):
    def construct(self):
        lamps = lamps_B(False)
        sl = slots_B()
        self.add(*lamps, *sl)
        self.at("microscope")
        m = icon_micro(BX[0])
        self.play(FadeOut(sl[0]), FadeIn(frame(BX[0], FY)), FadeIn(m), FadeIn(cap(0)), run_time=0.7)
        self.at("is there")
        self.play(lamps[0].on(), run_time=0.4)
        self.at("dye taken up")
        term, ves = icon_dye_parts(BX[1])
        self.play(FadeOut(sl[1]), FadeIn(frame(BX[1], FY)), FadeIn(term), FadeIn(ves), FadeIn(cap(1)), run_time=0.6)
        self.at("recycling vesicles")
        self.play(LaggedStart(*[v.animate.set_fill(TEAL, .9) for v in ves], lag_ratio=.25), run_time=1.0)
        self.at("shows release")
        self.play(lamps[1].on(), run_time=0.4)
        self.at("a recording")
        a, b, tr = icon_rec_parts(BX[2])
        self.play(FadeOut(sl[2]), FadeIn(frame(BX[2], FY)), FadeIn(a), FadeIn(b), FadeIn(cap(2)), run_time=0.5)
        self.at("shows the response")
        self.play(Create(tr), run_time=0.8)
        self.play(lamps[2].on(), run_time=0.4)
        self.finish()


class S07Beat(NarratedScene):
    def construct(self):
        self.add(*lamps_B(True), *icons_final())
        self.finish()


# =============================================================================================
#  s08  stargazer
# =============================================================================================
MFILL = "#262c3a"


def mouse_parts():
    ox, oy = 0.9, 0.2
    P = lambda x, y: [x + ox, y + oy, 0]
    sk = dict(stroke_color=GREYL, stroke_width=4, fill_color=MFILL, fill_opacity=1)
    tail = CubicBezier(P(-3.5, -.8), P(-4.9, -.8), P(-4.9, .6), P(-5.9, 1.0), stroke_color=GREYL, stroke_width=8)
    legs = VGroup(*[RoundedRectangle(corner_radius=.15, width=.5, height=1.1, **dict(sk, stroke_width=3)).move_to(
        P(x, -2.55)) for x in (-2.7, -1.7, 0.0, 1.0)])
    body = Ellipse(width=6.0, height=3.2, **sk).move_to(P(-.8, -.9))
    ear = Ellipse(width=.9, height=1.1, **dict(sk, stroke_width=3)).move_to(P(2.0, 1.35))
    head = Ellipse(width=2.8, height=2.2, **sk).move_to(P(2.7, -.1))
    snout = Polygon(P(3.7, .25), P(4.8, -.35), P(3.7, -.8), **dict(sk, stroke_width=3))
    eye = Dot(P(3.3, .15), radius=.12, color=TEXT)
    hd = VGroup(ear, head, snout, eye)
    piv = np.array(P(2.0, -.5))
    return VGroup(tail, legs, body), hd, piv


class S08Star(SpokenScene):
    def construct(self):
        base, hd, piv = mouse_parts()
        mouse = VGroup(base, hd)
        title = T("stargazer", 54, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        sub = T("a spontaneous mutant", 32, GREYL).move_to([0, -3.55, 0])
        self.at("take stargazer", lead=0.0)
        self.play(FadeIn(mouse, shift=UP * .2), FadeIn(title), run_time=0.9)
        self.play(FadeIn(sub), run_time=0.4)
        self.at("tosses its head upward", lead=0.0)
        self.play(hd.animate.rotate(32 * DEGREES, about_point=piv), run_time=0.9)
        self.at("seizures", lead=0.0)
        for _ in range(3):
            self.play(mouse.animate.shift([.13, .08, 0]).rotate(.015, about_point=ORIGIN), run_time=0.1)
            self.play(mouse.animate.shift([-.26, -.16, 0]).rotate(-.03, about_point=ORIGIN), run_time=0.1)
            self.play(mouse.animate.shift([.13, .08, 0]).rotate(.015, about_point=ORIGIN), run_time=0.1)
        self.finish()


# =============================================================================================
#  s09  the cerebellum, mossy fiber and granule cell
# =============================================================================================
def _wavy(a, b, cy, amp, ph, nw=26, f=1.0):
    return ParametricFunction(
        lambda t: np.array([f * a * np.cos(t) * (1 + amp * np.sin(nw * t + ph)),
                            cy + f * b * np.sin(t) * (1 + amp * np.sin(nw * t + ph)), 0]),
        t_range=[0, TAU, 0.01], stroke_color=GREYL, stroke_width=3)


def cerebellum():
    # Sagittal section: deep radial fissures divide leaf-like folia around arbor vitae.
    angles = np.linspace(-.15, PI + .15, 23)
    edge = [[-4.9, -1.6, 0], [-3.0, -2.55, 0], [0, -2.3, 0], [3.0, -2.4, 0], [5.15, -1.4, 0]]
    for t in angles:
        edge.extend([[5.25*np.cos(t), .1+2.9*np.sin(t), 0],
                     [4.45*np.cos(t+.055), .1+2.25*np.sin(t+.055), 0]])
    outline = VMobject(stroke_color=GREYL, stroke_width=4, fill_color=GREY, fill_opacity=.22)
    outline.set_points_smoothly(edge + [edge[0]])
    trunk = CubicBezier([0, -2.4, 0], [1, -1.7, 0], [.2, -.7, 0], [0, 1.0, 0],
                        stroke_color=GREYL, stroke_width=14)
    branches = VGroup()
    for t in np.linspace(.12, PI-.12, 13):
        end = np.array([4.45*np.cos(t), .1+2.2*np.sin(t), 0])
        start = np.array([.6*np.cos(t), -1.6+1.2*np.sin(t), 0])
        mid = np.array([2.3*np.cos(t), -.3+1.25*np.sin(t), 0])
        branches.add(CubicBezier(start, mid+DOWN*.3, mid, end, stroke_color=GREYL, stroke_width=5))
        for delta in (-.09, .09):
            tip = [4.95*np.cos(t+delta), .1+2.65*np.sin(t+delta), 0]
            branches.add(Line(mid, tip, color=GREYL, stroke_width=2))
    return VGroup(outline, trunk, branches)


def granule_view():
    cell = Circle(radius=1.9, stroke_color=GREYL, stroke_width=4, fill_color=GREY, fill_opacity=.25).move_to(
        [0, -1.0, 0])
    cl = T("granule cell", 34, TEXT).move_to([0, -1.0, 0])
    fiber = CubicBezier([-6.5, 3.4, 0], [-4.4, 3.4, 0], [-3.6, 1.65, 0], [-.9, 1.65, 0], stroke_color=GREY,
                        stroke_width=20, stroke_opacity=.6)
    term = box(3.4, 1.5, 0, 1.65, GREY, .3, .45)
    ves = VGroup(*[Dot([x, y, 0], radius=.14, color=TEAL) for x, y in [(-.9, 1.4), (0, 1.4), (.9, 1.4), (-.45, 1.95),
                                                                       (.45, 1.95)]])
    fl = T("mossy fiber", 32, TEXT).move_to([4.6, 2.5, 0])
    ln = leader((3.4, 2.5), (-2.6, 2.0))
    tl = T("terminal", 28, GREYL).move_to([4.6, 1.85, 0])
    return cell, cl, fiber, term, ves, fl, ln


class S09Gc(SpokenScene):
    def construct(self):
        cb = cerebellum()
        cb_l = T("cerebellum", 36, TEXT).move_to([0, -3.45, 0])
        self.at("cerebellum", lead=0.3)
        self.play(FadeIn(cb), FadeIn(cb_l), run_time=0.8)
        rp = (2.4, 1.0)
        ring = Circle(radius=.5, stroke_color=TEXT, stroke_width=4).move_to([*rp, 0])
        self.at("granule cells")
        self.play(Create(ring), run_time=0.35)
        cell, cl, fiber, term, ves, fl, ln = granule_view()
        zoom_into(self, VGroup(cb, cb_l, ring), rp, new=[cell, cl], factor=7.0, run=0.8)
        self.at("mossy fibers")
        self.play(Create(fiber), FadeIn(term), FadeIn(ves), FadeIn(fl), Create(ln), run_time=0.5)
        self.play(Indicate(cell, color=TEXT, scale_factor=1.02), run_time=0.5)
        self.finish()


# =============================================================================================
#  s10  AMPA receptors (the same funnel shape as the NMDA receptor of s11)
# =============================================================================================
MCY = -0.5          # membrane centre y in the zoomed synapse
SC = 0.8            # receptor scale in s10
AXS = (-4.8, -2.4, 0.0)
NXS = (2.4, 4.8)


def membrane_segments(xs, s, cy, thick, x0=-6.5, x1=6.5, color=GREY, fo=.3):
    """The membrane as bars with a gap at every receptor stem."""
    edges = [x0]
    segs = []
    for x in sorted(xs):
        segs.append((edges[-1], x - .45 * s))
        edges.append(x + .45 * s)
    segs.append((edges[-1], x1))
    return VGroup(*[box(b - a, thick, (a + b) / 2, cy, color, fo, .08, 2) for a, b in segs])


def terminal_zoom():
    term = box(9.0, 1.7, 0, 2.85, GREY, .18, .45)
    ves = VGroup(*[Dot([x, 2.85 + dy, 0], radius=.16, color=TEAL) for x, dy in
                   [(-3.6, -.25), (-2.2, -.25), (-.8, -.25), (.6, -.25), (2.0, -.25), (3.4, -.25), (-2.9, .3),
                    (-1.5, .3), (-.1, .3), (1.3, .3), (2.7, .3)]])
    return term, ves


class S10Receptors(SpokenScene):
    def construct(self):
        cell, cl, fiber, term, ves, fl, ln = granule_view()
        old = VGroup(cell, cl, fiber, term, ves, fl, ln)
        self.add(old)
        tz, vz = terminal_zoom()
        mem = membrane_segments(AXS, SC, MCY, 1.1 * SC)
        ampa = VGroup(*[chan(x, MCY, SC, ORANGE, 7) for x in AXS])
        al = T("AMPA receptor", 32, ORANGE).move_to([-2.4, -2.9, 0])
        lead_a = leader((-2.4, -2.55), (-2.4, -1.4), ORANGE)
        zoom_into(self, old, [0, .9], new=[tz, vz, mem], factor=2.4, run=0.7)
        self.play(FadeIn(ampa, shift=UP * .2), FadeIn(al), Create(lead_a), run_time=0.5)
        self.at("most")
        arrs = VGroup(*[tick([x, 1.0, 0], [x, -2.2, 0], ORANGE, w=14, tip=.35) for x in AXS])
        self.play(*[GrowArrow(a) for a in arrs], run_time=0.9)
        self.at("current")
        cl2 = T("fast excitatory current", 30, ORANGE).move_to([3.6, -1.5, 0])
        self.play(FadeIn(cl2), light_all(ampa, ORANGE), run_time=0.6)
        self.finish()


def light_all(chs, color, op=.5):
    return AnimationGroup(*[ch[0].animate.set_fill(color, op) for ch in chs])


# =============================================================================================
#  s11  NMDA receptor and the magnesium block (enlarged)
# =============================================================================================
S_ = 1.9
BCY = -0.65


def big_parts():
    ch = chan(0, BCY, S_, PURPLE, 9)
    mem = membrane_segments([0], S_, BCY, 1.1 * S_, -6.6, 6.6)
    yb = BCY - .55 * S_
    gl = [Line([-.45 * S_, yb, 0], [-.04 * S_, yb, 0], color=PURPLE, stroke_width=9),
          Line([.45 * S_, yb, 0], [.04 * S_, yb, 0], color=PURPLE, stroke_width=9)]
    return ch, mem, gl


def gate_open(gl):
    yb = BCY - .55 * S_
    return [Line([-.45 * S_, yb, 0], [-.45 * S_, yb - .45 * S_, 0], color=PURPLE, stroke_width=9),
            Line([.45 * S_, yb, 0], [.45 * S_, yb - .45 * S_, 0], color=PURPLE, stroke_width=9)]


def thin_cur():
    return tick([0, -2.15, 0], [0, -3.05, 0], PURPLE, w=4, tip=.25)


SITE_L = [-.725 * S_ - .22, 1.2 * S_ + BCY + .12, 0]
SITE_L2 = [SITE_L[0] - .25, SITE_L[1] + .5, 0]
SITE_R = [.725 * S_, 1.2 * S_ + BCY, 0]


def mg_ion(x, y):
    return VGroup(Circle(radius=.36, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=.95),
                  T("Mg", 24, TEXT, weight=BOLD)).move_to([x, y, 0])


def big_labels():
    return dict(
        out_l=T("outside", 28, GREYL).move_to([-5.7, 2.3, 0]),
        in_l=T("inside", 28, GREYL).move_to([-5.7, -1.9, 0]),
        nm_l=T("NMDA receptor", 32, PURPLE).move_to([-4.6, 3.3, 0]),
        gl_l=T("glutamate", 30, TEAL).move_to([-3.35, 1.95, 0]),
        co_l=T("co-agonist", 30, TEXT).move_to([3.55, 1.85, 0]),
        nr=T("near rest", 32, TEXT).move_to([-4.9, -3.4, 0]),
        mgl=T("magnesium from outside", 30, RED).move_to([0, 3.45, 0]),
        sm=T("small current", 28, PURPLE).move_to([2.2, -2.6, 0]),
        vd=T("voltage-dependent block", 34, TEXT).move_to([2.7, -3.4, 0]))


class S11Nmda(SpokenScene):
    def construct(self):
        # carry the zoomed synapse from s10
        tz, vz = terminal_zoom()
        mem0 = membrane_segments(AXS, SC, MCY, 1.1 * SC)
        ampa = VGroup(*[chan(x, MCY, SC, ORANGE, 7) for x in AXS])
        self.add(tz, vz, mem0, ampa)
        # the NMDA receptors join, on the first word
        mem1 = membrane_segments(AXS + NXS, SC, MCY, 1.1 * SC)
        nmda = VGroup(*[chan(x, MCY, SC, PURPLE, 7) for x in NXS])
        nl = T("NMDA receptor", 32, PURPLE).move_to([3.6, -2.9, 0])
        ln = leader((3.6, -2.55), (3.6, -1.4), PURPLE)
        self.play(FadeOut(mem0), FadeIn(mem1), FadeIn(nmda, shift=UP * .2), FadeIn(nl), Create(ln), run_time=0.5)
        idle_until(self, 1.0)
        old = VGroup(tz, vz, mem1, ampa, nmda, nl, ln)
        ch, mem, gl = big_parts()
        L = big_labels()
        # zoom: bring the right-hand NMDA receptor to the middle and enlarge it
        self.play(old.animate.shift([-NXS[0], 0, 0]).scale(2.0, about_point=np.array([0, MCY, 0])).set_opacity(0),
                  FadeIn(mem), FadeIn(ch), *[FadeIn(g) for g in gl], FadeIn(L["out_l"]), FadeIn(L["in_l"]),
                  FadeIn(L["nm_l"]), run_time=0.8)
        self.remove(old)
        self.at("open when")
        self.play(Indicate(VGroup(ch[1], ch[2]), color=PURPLE, scale_factor=1.03), run_time=0.6)
        # glutamate binds on the outer face of the left wall
        self.at("glutamate")
        g1 = Dot([-2.0, 3.0, 0], radius=.17, color=TEAL)
        g2 = Dot([-1.5, 3.3, 0], radius=.17, color=TEAL)
        self.play(FadeIn(g1), FadeIn(g2), g1.animate.move_to(SITE_L), g2.animate.move_to(SITE_L2),
                  FadeIn(L["gl_l"]), run_time=0.55)
        # the co-agonist binds on the outer face of the right wall
        self.at("and a")
        co = Square(side_length=.32, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=.9).move_to(
            [2.3, 3.2, 0])
        self.play(FadeIn(co), co.animate.move_to(SITE_R), FadeIn(L["co_l"]), run_time=0.6)
        self.at("bound")
        og = gate_open(gl)
        self.play(light(ch, PURPLE, .35), *[Transform(a, b) for a, b in zip(gl, og)], run_time=0.8)
        self.at("near rest")
        mg = mg_ion(0, BCY + .1)
        self.play(FadeIn(mg), FadeIn(L["nr"]), run_time=0.4)
        self.at("magnesium")
        self.play(FadeIn(L["mgl"]), Indicate(mg, color=RED, scale_factor=1.12), run_time=0.8)
        self.at("blocks most")
        arrow = thin_cur()
        self.play(GrowArrow(arrow), FadeIn(L["sm"]), FadeIn(L["vd"]), run_time=0.7)
        self.finish()


class S11bBeat(NarratedScene):
    def construct(self):
        ch, mem, gl = big_parts()
        og = gate_open(gl)
        ch[0].set_fill(PURPLE, .35)
        L = big_labels()
        items = [mem, ch, *og, mg_ion(0, BCY + .1), thin_cur(), *L.values(),
                 Dot(SITE_L, radius=.17, color=TEAL), Dot(SITE_L2, radius=.17, color=TEAL),
                 Square(side_length=.32, stroke_color=TEXT, stroke_width=2, fill_color=TEXT,
                        fill_opacity=.9).move_to(SITE_R)]
        self.add(*items)
        self.finish()


# =============================================================================================
#  s12  predict
# =============================================================================================
class S12Predict(SpokenScene):
    def construct(self):
        syn = q_syn()
        lamps = q_lamps(("There?", "Releases?", "Responds?"))
        pn, pa = q_panels()
        self.at("in stargazer", lead=0.0)
        self.play(FadeIn(q_title()), FadeIn(syn), run_time=0.6)
        self.at("these synapses")
        self.play(Indicate(syn.term, color=TEXT, scale_factor=1.02), Indicate(syn.post, color=TEXT, scale_factor=1.02),
                  run_time=0.7)
        self.at("give")
        self.play(FadeIn(pn["frame"]), FadeIn(pn["title"]), FadeIn(pn["axes"]), run_time=0.5)
        self.at("responses")
        self.play(Create(pn["trace"]), Indicate(syn.nmda, color=PURPLE, scale_factor=1.3), run_time=0.8)
        self.at("but no")
        self.play(FadeIn(pa["frame"]), FadeIn(pa["title"]), FadeIn(pa["axes"]), run_time=0.4)
        self.at("ampa responses")
        self.play(Create(pa["trace"]), FadeIn(pa["none"]), Indicate(syn.ampa, color=ORANGE, scale_factor=1.3),
                  run_time=0.8)
        self.at("predict")
        self.play(*[FadeIn(l, shift=UP * .2) for l in lamps], run_time=0.5)
        self.at("which property failed")
        q = q_question()
        self.play(FadeIn(q), Indicate(VGroup(*lamps), color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        syn, lamps, pn, pa, qn, mob = q_full()
        self.add(*mob)
        self.finish()


# =============================================================================================
#  s14 / s15 / s16  the answer, one lamp at a time
# =============================================================================================
class S14There(SpokenScene):
    def construct(self):
        syn, lamps, pn, pa, qn, mob = q_full()
        self.add(*mob)
        self.at("not being there")
        self.play(FadeOut(qn), Indicate(lamps[0], color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("synapses are present")
        self.play(lamps[0].on(), Transform(lamps[0].label, T("There", 28, TEXT).move_to(lamps[0].label)),
                  Indicate(syn.term, color=GREEN, scale_factor=1.03),
                  Indicate(syn.post, color=GREEN, scale_factor=1.03), run_time=0.8)
        self.finish()


def q_after_there():
    syn, lamps, pn, pa, qn, mob = q_full((True, False, False), ("There", "Releases?", "Responds?"), question=False)
    return syn, lamps, pn, pa, mob


class S15Release(SpokenScene):
    def construct(self):
        syn, lamps, pn, pa, mob = q_after_there()
        self.add(*mob)
        self.at("not release")
        self.play(Indicate(lamps[1], color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("needs glutamate")
        self.play(Indicate(pn["trace"], color=PURPLE, scale_factor=1.1), Indicate(syn.nmda, color=PURPLE,
                                                                                scale_factor=1.35), run_time=0.9)
        self.at("transmitter")
        dots = release(self, syn, run=1.5, targets=syn.top_xs())
        self.play(lamps[1].on(), Transform(lamps[1].label, T("Releases", 28, TEXT).move_to(lamps[1].label)),
                  light_all(syn.nmda, PURPLE, .6), run_time=0.7)
        self.finish()


def q_after_release():
    syn, lamps, pn, pa, qn, mob = q_full((True, True, False), ("There", "Releases", "Responds?"), question=False)
    light_all(syn.nmda, PURPLE)
    return syn, lamps, pn, pa, mob


class S16Respond(SpokenScene):
    def construct(self):
        syn, lamps, pn, pa, mob = q_after_release()
        self.add(*mob)
        self.at("what failed")
        self.play(Indicate(lamps[2], color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("one kind of response")
        lN = Lamp(-2.2, QLY, "NMDA", False, color=PURPLE)
        lA = Lamp(-.7, QLY, "AMPA", False, color=ORANGE)
        resp = T("Responds", 28, TEXT).move_to([-1.45, -.8, 0])
        self.play(FadeOut(lamps[2]), run_time=0.25)
        self.play(FadeIn(lN), FadeIn(lA), FadeIn(resp), run_time=0.55)
        self.at("responds through")
        self.play(lN.on(), light(syn.nmda[0], PURPLE, .6), light(syn.nmda[1], PURPLE, .6),
                  Indicate(pn["trace"], color=PURPLE, scale_factor=1.1), run_time=0.8)
        self.at("not the other")
        gh = syn.ghost_ampa()
        fl = T("fails", 28, RED).move_to([-.7, -2.85, 0])
        self.play(FadeOut(syn.ampa), FadeIn(gh), lA.fail(), FadeIn(fl),
                  Indicate(pa["none"], color=RED, scale_factor=1.15), run_time=0.9)
        self.finish()


class S17Beat(NarratedScene):
    def construct(self):
        syn, lamps, pn, pa, mob = q_after_release()
        lamps[0].label.become(T("There", 28, TEXT).move_to(lamps[0].label))
        lN = Lamp(-2.2, QLY, "NMDA", True, color=PURPLE)
        lA = Lamp(-.7, QLY, "AMPA", False, color=ORANGE)
        lA.bulb.set_fill(RED, .25).set_stroke(RED)
        lA.glow.set_fill(RED, .12)
        resp = T("Responds", 28, TEXT).move_to([-1.45, -.8, 0])
        fl = T("fails", 28, RED).move_to([-.7, -2.85, 0])
        gh = syn.ghost_ampa()
        syn.remove(syn.ampa)
        self.add(q_title(), syn, lamps[0], lamps[1], lN, lA, resp, fl, gh, panel_group(pn), panel_group(pa))
        self.finish()


# =============================================================================================
#  s18  stargazin brings AMPA receptors up to the membrane
# =============================================================================================
MY = 1.0     # membrane centre y
PXC = 0.5    # pair centre x
PS = 0.8
RXO = 1.05   # receptor offset from the pair centre
PCY0 = -1.1  # pair centre y before it rises
MEMT = 0.6


def membrane_cell(seated=False):
    if seated:
        mem = membrane_segments([PXC - RXO, PXC + RXO], PS, MY, MEMT, -6.5, 6.5)
    else:
        mem = box(13.0, MEMT, 0, MY, GREY, .3, .1, 2)
    cellb = Rectangle(width=13.0, height=4.4, stroke_width=0, fill_color=GREY, fill_opacity=.07).move_to(
        [0, MY - MEMT / 2 - 2.2, 0])
    return mem, cellb


def pair(cy, tail=1.0, color=ORANGE):
    """Two AMPA receptors with ONE stargazin between them, touching both. Returns (left, right, block, tail)."""
    l = chan(PXC - RXO, cy, PS, color, 6)
    r = chan(PXC + RXO, cy, PS, color, 6)
    for receptor in (l, r):
        receptor[0].set_fill(color, .15)
    wid = 2 * (RXO - .45 * PS)
    block = Rectangle(width=wid, height=.65, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                      fill_opacity=.85).move_to([PXC, cy - .02, 0])
    tl = Line([PXC, cy - .345, 0], [PXC, cy - .47 - tail, 0], color=TEXT, stroke_width=7)
    return l, r, block, tl


def sg_label(cy, text="stargazin: one small protein"):
    label = T(text, 28, TEXT).move_to([PXC, cy - 1.87, 0])
    return VGroup(label, leader((PXC, cy - 1.47), (PXC, label.get_top()[1])))


def ampa_label(cy):
    t = T("AMPA receptors", 30, ORANGE).move_to([4.5, cy + .5, 0])
    return t, leader((2.95, cy + .5), (PXC + RXO + .62, cy + .5), ORANGE)


class S18Stargazin(SpokenScene):
    def construct(self):
        mem, cellb = membrane_cell()
        out_l = T("outside", 28, GREYL).move_to([-5.5, 2.1, 0])
        in_l = T("inside the cell", 28, GREYL).move_to([-5.0, .1, 0])
        gene = chip("gene", GREYL, 32).move_to([-5.0, -2.3, 0])
        credit = T("Bredt and Nicoll laboratories, 2000", 26, GREYL).move_to([-3.5, -3.55, 0])
        l, r, block, tl = pair(PCY0)
        sg = VGroup(block, tl)
        sgl = sg_label(PCY0, "stargazin")
        ar = tick([-4.1, -2.3, 0], [-.4, -2.3, 0], GREYL, w=5)
        self.at("gene", lead=0.0)
        self.play(FadeIn(mem), FadeIn(cellb), FadeIn(out_l), FadeIn(in_l), FadeIn(gene), run_time=0.7)
        self.at("stargazin")
        self.play(GrowArrow(ar), run_time=0.4)
        self.play(FadeIn(sg, shift=UP * .2), FadeIn(sgl), FadeIn(credit), run_time=0.5)
        self.at("small membrane protein")
        self.play(Transform(sgl, sg_label(PCY0)), run_time=0.5)
        self.at("it brings")
        al, aln = ampa_label(PCY0)
        self.play(FadeIn(l, shift=RIGHT * .3), FadeIn(r, shift=LEFT * .3), FadeIn(al), Create(aln), FadeOut(ar),
                  FadeOut(gene), run_time=0.7)
        self.at("receptors")
        up = MY - PCY0
        grp = VGroup(l, r, block, tl, sgl, al, aln)
        self.play(grp.animate.shift([0, up, 0]), run_time=1.4)
        mem2, _ = membrane_cell(True)
        self.play(FadeOut(mem), FadeIn(mem2), run_time=0.3)
        self.finish()


# =============================================================================================
#  s19  the tail binds PSD-95, the scaffold
# =============================================================================================
class S19Psd(SpokenScene):
    def construct(self):
        mem, cellb = membrane_cell(True)
        l, r, block, tl = pair(MY)
        sgl = sg_label(MY)
        al, aln = ampa_label(MY)
        self.add(cellb, mem, l, r, block, tl, sgl, al, aln)
        sgl2 = T("stargazin", 30, TEXT).move_to([-2.4, -.95, 0])
        ln2 = leader((-1.4, -.95), (PXC, -.1))
        self.at("its tail", lead=0.0)
        self.play(FadeOut(sgl), run_time=0.2)
        self.play(FadeIn(sgl2), Create(ln2), Indicate(tl, color=TEXT, scale_factor=1.0), run_time=0.5)
        plate = box(5.0, 1.0, PXC, -2.0, GREY, .5, .12, 3)
        psd = T("PSD-95", 32, TEXT).move_to([PXC, -2.07, 0])
        tail2 = Line([PXC, MY - .47 - 1.0, 0], [PXC, -1.5, 0], color=TEXT, stroke_width=7)
        clip = RoundedRectangle(corner_radius=.1, width=.7, height=.5, stroke_color=TEXT, stroke_width=4).move_to(
            [PXC, -1.52, 0])
        self.at("binds")
        self.play(FadeIn(plate), FadeIn(psd), Create(tail2), run_time=0.6)
        self.play(Create(clip), run_time=0.4)
        self.at("a scaffold")
        scaf = T("scaffold", 30, GREYL).move_to([PXC, -3.0, 0])
        self.play(FadeIn(scaf), run_time=0.5)
        self.at("synapse")
        term = box(6.4, 1.1, PXC, 3.2, GREY, .18, .4)
        tves = VGroup(*[Dot([x, 3.2, 0], radius=.14, color=TEAL) for x in (PXC - 2.0, PXC - .7, PXC + .7, PXC + 2.0)])
        self.play(FadeIn(term), FadeIn(tves), run_time=0.7)
        self.at("holds the receptors")
        self.play(Indicate(VGroup(l, r), color=ORANGE, scale_factor=1.15), Indicate(plate, color=TEXT,
                                                                                    scale_factor=1.04),
                  run_time=1.0)
        self.finish()


# =============================================================================================
#  s20  a count misses it; a recording and receptor labeling show it
# =============================================================================================
PX = (-4.5, 0, 4.5)
PYC = 0.3
P_W, P_H = 4.1, 5.0


def mini6(cx, cy):
    out = VGroup()
    for i, (dx, dy) in enumerate([(-1.0, 1.5), (1.0, 1.5), (-1.0, .15), (1.0, .15), (-1.0, -1.2), (1.0, -1.2)]):
        out.add(SynG(cx + dx, cy + dy - .28 - .0, .22, "none"))
    return out


class S20Record(SpokenScene):
    def construct(self):
        fr = [frame(x, PYC, P_W, P_H) for x in PX]
        ttl = [T(t, 34, TEXT).move_to([x, 3.4, 0]) for t, x in zip(("count", "recording", "labeling receptors"), PX)]
        for t in ttl:
            t.set_opacity(.35)
        # panel 1: six synapses counted
        p1 = mini6(PX[0], PYC + .15).scale(.85).shift(UP * .18)
        n1 = T("6 synapses", 32, TEXT).move_to([PX[0], PYC - 1.85, 0])
        c1 = T("looks normal", 28, GREYL).move_to([PX[0], -2.75, 0])
        # panel 2: the recording
        cx = PX[1]
        y_n, y_a = PYC + 1.4, PYC - .5
        ax = VGroup(Arrow([cx - 1.4, y_n, 0], [cx + 1.8, y_n, 0], buff=0, color=GREY, stroke_width=3, tip_length=.18),
                    Arrow([cx - 1.4, y_a, 0], [cx + 1.8, y_a, 0], buff=0, color=GREY, stroke_width=3, tip_length=.18),
                    Arrow([cx - 1.4, y_n, 0], [cx - 1.4, y_n - 1.0, 0], buff=0, color=GREY, stroke_width=3,
                          tip_length=.18),
                    T("current", 26, GREYL).rotate(PI / 2).move_to([cx - 1.78, y_n - .5, 0]),
                    T("time", 26, GREYL).move_to([cx + 1.2, y_a - .55, 0]))
        trn = curve(cx - 1.35, y_n, 3.0, -1.0, td=.5, tr=.05, onset=.12, color=PURPLE, sw=6)
        tra = Line([cx - 1.35, y_a, 0], [cx + 1.6, y_a, 0], color=ORANGE, stroke_width=7)
        ln = T("NMDA", 28, PURPLE).move_to([cx + .9, y_n + .42, 0])
        la = T("AMPA", 28, ORANGE).move_to([cx + .9, y_a + .42, 0])
        none = T("none", 28, RED).move_to([cx + 1.1, y_a - .0 + .0 - .0 + 0, 0]).shift(DOWN * 0)
        none.move_to([cx - .1, y_a - .55, 0])
        c2 = T("NMDA current only", 28, PURPLE).move_to([cx, -2.75, 0])
        # panel 3: the labeled receptors
        s3 = SynG(PX[2], PYC - .1, .52, "color", rec_sw=4)
        gh = s3.ghost_ampa(ORANGE)
        lab = T("AMPA receptor label", 26, ORANGE).move_to([PX[2], PYC - 1.0, 0])
        lab_n = T("little at the synapse", 26, GREYL).move_to([PX[2], PYC - 1.6, 0])
        c3 = T("little AMPA receptor", 28, ORANGE).move_to([PX[2], -2.75, 0])
        s3.remove(s3.ampa)
        s3.all = None
        self.add(*fr, *ttl)
        self.at("a count", lead=0.1)
        self.play(ttl[0].animate.set_opacity(1), FadeIn(p1), FadeIn(n1), run_time=0.6)
        self.at("miss this defect")
        self.play(FadeIn(c1), run_time=0.6)
        self.at("a recording")
        self.play(ttl[1].animate.set_opacity(1), FadeIn(ax), FadeIn(ln), FadeIn(la), run_time=0.4)
        self.play(Create(trn), Create(tra), run_time=0.7)
        self.play(FadeIn(none), FadeIn(c2), run_time=0.4)
        self.at("labeling the receptors")
        self.play(ttl[2].animate.set_opacity(1), FadeIn(s3), FadeIn(gh), run_time=0.6)
        self.play(FadeIn(lab), FadeIn(lab_n), FadeIn(c3), run_time=0.6)
        self.finish()


# =============================================================================================
#  s21  the guiding idea
# =============================================================================================
class S21Rule(SpokenScene):
    def construct(self):
        head = T("Carry one idea", 60, TEXT, font=TITLE_FONT).move_to([0, 0.2, 0])
        l1 = T("A synapse that is there", 56, GOLD, font=TITLE_FONT).move_to([0, 0.6, 0])
        l2 = T("is not yet a synapse that works.", 56, GOLD, font=TITLE_FONT).move_to([0, -.7, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).move_to([0, -1.9, 0])
        self.at("carry one idea")
        self.play(FadeIn(head, shift=UP * .1), run_time=0.7)
        self.at("synapse that is there")
        self.play(head.animate.scale(0.5).move_to([0, 2.5, 0]).set_color(GREYL), FadeIn(l1, shift=UP * .15),
                  run_time=0.7)
        self.at("not yet")
        self.play(FadeIn(l2, shift=UP * .15), run_time=0.8)
        self.at("synapse that works")
        self.play(GrowFromCenter(rule), run_time=0.5)
        self.finish()


# =============================================================================================
#  s22  takeaway: each experiment lights only its own lamp
# =============================================================================================
class S22Take(SpokenScene):
    def construct(self):
        lamps = lamps_B(False)
        ics = icons_final()
        dims = [Rectangle(width=3.9, height=FH, stroke_width=0, fill_color=BG, fill_opacity=0).move_to([x, FY, 0])
                for x in BX]
        self.add(*lamps)
        self.at("each experiment")
        self.play(*[FadeIn(i, shift=UP * .15) for i in ics], run_time=0.8)
        self.add(*dims)
        self.at("only")
        self.play(lamps[0].on(), dims[1].animate.set_fill(BG, .72), dims[2].animate.set_fill(BG, .72), run_time=0.5)
        self.at("properties")
        self.play(lamps[0].off(), lamps[1].on(), dims[0].animate.set_fill(BG, .72), dims[1].animate.set_fill(BG, 0),
                  run_time=0.5)
        self.at("measures")
        self.play(lamps[1].off(), lamps[2].on(), dims[1].animate.set_fill(BG, .72), dims[2].animate.set_fill(BG, 0),
                  run_time=0.5)
        self.finish()


class S23End(EndCard):
    LINE = "Each experiment sees only the properties it measures."
