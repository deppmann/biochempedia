"""A Neuron Must Work to Die  (chapter 1 of "The Death Machinery in Neurons")

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared by every chapter; taken from scenes.old.py)
  BLUE   = the neuron / a living cell
  YELLOW = NGF, the survival signal (and the brakes it applies)
  TEAL   = new gene expression: the drug that blocks it, the unknown new product
  ORANGE = pro-death BCL-2 family proteins (Bim, Bax)        (later chapters)
  PINK   = cytochrome c                                       (later chapters)
  PURPLE = CED-4 / Apaf-1 (and the apoptosome wheel)          (later chapters)
  RED    = the killers (CED-3 / caspases) and death itself
  GREEN  = protective: CED-9 / Bcl-2, "survives" (here: the well that keeps its NGF)
  GREY   = outlines, axes, labels, dead or inactive things, the "run-down" idea
  GOLD   = the "eat me" tag; here also the year credit and the counting rings
Survival curves are illustrative Weibull curves S(t) = exp(-(t/tau)^k), tau in days (the plots say so):
  keeps NGF tau=60 k=1;  no NGF tau=1.1 k=1.5 (about 9% alive at day 2);  drug tau=2.8 k=3.
"""

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F28CB1"
DARK = "#0A1030"      # dense (pyknotic) chromatin fill
LG = "#B4BAC6"        # lighter grey for secondary labels


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def neuron(r=0.75, color=BLUE):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    stubs = VGroup()
    for ang in (150, 210, 90):
        v = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(v * r, v * (r + 0.37 * r), color=color, stroke_width=4))
    nuc = Circle(radius=r * 0.3, stroke_width=0, fill_color=color, fill_opacity=0.55)
    g = VGroup(body, stubs, nuc)
    g.body, g.stubs, g.nuc = body, stubs, nuc
    return g


def place(n, c):
    """move a neuron so its BODY (not the stubs' bounding box) is centred on c"""
    n.shift(np.array(c, float) - n.body.get_center())
    return n


def small_neuron(r, color=BLUE):
    body = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.28)
    stubs = VGroup(*[Line(np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) * r,
                          np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) * r * 1.5,
                          color=color, stroke_width=3) for a in (150, 210, 90)])
    nuc = Circle(radius=r * 0.3, stroke_width=0, fill_color=color, fill_opacity=0.55)
    return VGroup(body, stubs, nuc)


def ring_dots(center, radius=1.2, n=6, color=YELLOW, r=0.12):
    return VGroup(*[Dot(center + radius * np.array([np.cos(a), np.sin(a), 0]), radius=r, color=color)
                    for a in np.linspace(0, TAU, n, endpoint=False) + 0.3])


def xmark(center, s=0.22, color=RED, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def pill(center, color=TEAL, w=1.1, h=0.5):
    body = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.5)
    mid = Line([0, -h / 2, 0], [0, h / 2, 0], color=color, stroke_width=3)
    return VGroup(body, mid).move_to(center)


def rna(c, ang, L=0.75, color=TEAL, w=6):
    """a plain new transcript: one smooth teal stroke"""
    h = L / 2
    m = CubicBezier(np.array([-h, 0, 0]), np.array([-h / 2, 0.22, 0]), np.array([h / 2, -0.22, 0]),
                    np.array([h, 0, 0]), stroke_color=color, stroke_width=w)
    return m.rotate(ang).move_to(c)


def unit(deg):
    return np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])


def dim_static(g, f):
    for m in g.family_members_with_points():
        m.set_fill(opacity=m.get_fill_opacity() * f)
        m.set_stroke(opacity=m.get_stroke_opacity() * f)
    return g


def dim_anims(g, f):
    """(dim animations, function that builds the restore animations when called)"""
    saved = [(m, m.get_fill_opacity(), m.get_stroke_opacity()) for m in g.family_members_with_points()]
    dims = [m.animate.set_fill(opacity=fo * f).set_stroke(opacity=so * f) for m, fo, so in saved]

    def rests():
        return [m.animate.set_fill(opacity=fo).set_stroke(opacity=so) for m, fo, so in saved]
    return dims, rests


def surv(t, tau, k):
    return float(np.exp(-(t / tau) ** k))


def t_at(model, s):
    tau, k = model
    return tau * (-np.log(s)) ** (1.0 / k)


# survival-curve models (tau days, k): illustrative Weibull curves
M_NGF, M_NONGF, M_DRUG = (60.0, 1.0), (1.1, 1.5), (2.8, 3.0)
M_SOON, M_SAME, M_LATE = (0.55, 1.5), M_NONGF, M_DRUG


class Plot:
    """Survival plot: x = days 0..tmax, y = fraction alive 0..1, placed in scene units."""

    def __init__(self, x0, x1, y0, y1, tmax=4):
        self.x0, self.x1, self.y0, self.y1, self.tmax = x0, x1, y0, y1, tmax
        self.xticks = []

    def P(self, t, s):
        return np.array([self.x0 + (self.x1 - self.x0) * t / self.tmax, self.y0 + (self.y1 - self.y0) * s, 0.0])

    def axes(self):
        P = self.P
        g = VGroup()
        for s in (0.5, 1.0):
            g.add(Line(P(0, s), P(self.tmax, s), color=GREY, stroke_width=1.5, stroke_opacity=0.35))
        g.add(Line(P(0, 0), P(0, 1) + UP * 0.12, color=GREY, stroke_width=3))
        g.add(Line(P(0, 0), P(self.tmax, 0) + RIGHT * 0.15, color=GREY, stroke_width=3))
        for s, txt in ((0, "0"), (0.5, "50"), (1, "100")):
            g.add(T(txt, 26, GREY).next_to(P(0, s), LEFT, buff=0.15))
        self.xticks = []
        for t in range(self.tmax + 1):
            g.add(Line(P(t, 0) + DOWN * 0.07, P(t, 0) + UP * 0.07, color=GREY, stroke_width=3))
            lab = T(str(t), 26, GREY).next_to(P(t, 0), DOWN, buff=0.14)
            g.add(lab)
            self.xticks.append(lab)
        ym = (self.y0 + self.y1) / 2
        g.add(T("neurons alive (%)", 26, LG).rotate(PI / 2).move_to([self.x0 - 1.25, ym, 0]))
        g.add(T("days", 26, LG).move_to(P(self.tmax / 2, 0) + DOWN * 0.8))
        note = T("illustrative curves", 24, GREY)
        note.move_to(P(self.tmax, 0) + DOWN * 0.8 + RIGHT * 0.15 - [note.width / 2, 0, 0])
        g.add(note)
        return g

    def tick_labels(self, axes):
        return self.xticks

    def curve(self, model, color, w=6, n=140, tmax=None):
        tau, k = model
        ts = np.linspace(0, tmax or self.tmax, n)
        m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
        m.set_points_smoothly([self.P(t, surv(t, tau, k)) for t in ts])
        return m

    def grow(self, scene, model, color, t0, t1, run_time, mob=None, w=6, n=45, rate=linear):
        tau, k = model
        if mob is None:
            mob = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
            mob.set_points_as_corners([self.P(t0, surv(t0, tau, k)), self.P(t0 + 0.001, surv(t0 + 0.001, tau, k))])
            scene.add(mob)

        def upd(m, a):
            t = t0 + max(a, 0.003) * (t1 - t0)
            ts = np.linspace(0, t, n)
            m.set_points_smoothly([self.P(x, surv(x, tau, k)) for x in ts])
        return mob, UpdateFromAlphaFunc(mob, upd, run_time=run_time, rate_func=rate)

    def dashed(self, model, color, w=5):
        return DashedVMobject(self.curve(model, color, w), num_dashes=30, dashed_ratio=0.6)

    def swatch(self, model, color, nudge=0.0):
        """a dot in the well's colour just past the end of its curve"""
        tau, k = model
        p = self.P(self.tmax, surv(self.tmax, tau, k)) + RIGHT * 0.34 + UP * nudge
        return Dot(p, radius=0.13, color=color)

    def side_tag(self, model, s, text, color, side=1, size=26, gap=0.32):
        """plain label placed beside its curve, at least `gap` clear of it (side +1 right, -1 left)"""
        t_ = T(text, size, color, weight=BOLD)
        hs = t_.height / (self.y1 - self.y0) / 2
        se = min(max(s - hs if side > 0 else s + hs, 0.002), 0.998)
        x = self.P(t_at(model, se), se)[0]
        t_.move_to([x + side * (gap + t_.width / 2), self.P(0, s)[1], 0])
        return t_


# ---------------------------------------------------------------------------------------------
# wells
# ---------------------------------------------------------------------------------------------
NPOS = [(-0.26, 0.10), (-0.05, -0.22), (0.12, 0.22), (0.30, -0.10)]
DPOS = [(-0.42, -0.30), (-0.17, 0.36), (-0.40, 0.33), (0.22, -0.38), (0.45, 0.36), (-0.02, 0.05),
        (0.43, 0.10), (-0.20, -0.38)]
CURVE_COL = [GREEN, RED, TEAL]


def make_well(cx, cy, w, h, dots=True, dead=False, dish=None, drug=False):
    col = dish or GREY
    d = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=col, stroke_width=4,
                         fill_color=col, fill_opacity=0.18 if drug else 0.08).move_to([cx, cy, 0])
    r = (0.17 if h < 2.5 else 0.15) * h
    ns = VGroup(*[small_neuron(r).move_to([cx + fx * w, cy + fy * h, 0]) for fx, fy in NPOS])
    if dead:
        for n in ns:
            n.scale(0.7)
            n.set_color(GREY)
    ds = VGroup(*[Dot([cx + fx * w, cy + fy * h, 0], radius=0.03 * h + 0.025, color=YELLOW) for fx, fy in DPOS])
    if not dots:
        ds.set_opacity(0)
    return VGroup(d, ns, ds)


WELL_CX, WELL_W, WELL_H = -4.7, 4.1, 1.65
WELL_Y = [2.875, 0.555, -1.765]
PLOT_B = Plot(-0.85, 6.3, -2.7, 2.3, 4)
BAND_X = 2.7   # centre of the top band above the plot


def well_label(i):
    if i == 0:
        g = T("NGF", 28, YELLOW, weight=BOLD)
    elif i == 1:
        g = T("no NGF", 28, YELLOW, weight=BOLD)
    else:
        g = VGroup(T("no NGF +", 26, YELLOW, weight=BOLD), T("protein synthesis blocked", 24, TEAL, weight=BOLD))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    y = WELL_Y[i] - WELL_H / 2 - 0.12
    g.move_to([0, 0, 0])
    g.align_to([-6.75, 0, 0], LEFT)
    g.align_to([0, y, 0], UP)
    return g


class StageB:
    """The wells-and-plot layout, built in the state reached after progress p (0..3)."""

    def __init__(self, p):
        self.p = p
        self.wells = [make_well(WELL_CX, WELL_Y[i], WELL_W, WELL_H,
                                dots=not (p >= i + 1 and i >= 1),
                                dead=(i == 1 and p >= 2),
                                dish=(CURVE_COL[i] if p >= i + 1 else None),
                                drug=(i == 2 and p >= 3)) for i in range(3)]
        self.labels = [well_label(i) for i in range(3)]
        self.plot = PLOT_B
        self.axes = self.plot.axes()
        self.curves = [self.plot.curve(M_NGF, GREEN), self.plot.curve(M_NONGF, RED), self.plot.curve(M_DRUG, TEAL)]
        self.sw = [self.plot.swatch(M_NGF, GREEN), self.plot.swatch(M_NONGF, RED),
                   self.plot.swatch(M_DRUG, TEAL, nudge=0.12)]

    def present(self):
        out = [self.axes] + list(self.wells)
        for i in range(self.p):
            out.append(self.labels[i])
            if i < 2:
                out.append(self.curves[i])
                out.append(self.sw[i])
        return out

    def add_to(self, scene):
        scene.add(*self.present())
        return self


def guess_set(plot):
    """the three dashed guesses and their tags beside the curves"""
    gs = [plot.dashed(M_SOON, TEAL), plot.dashed(M_SAME, TEAL), plot.dashed(M_LATE, TEAL)]
    tags = [plot.side_tag(M_SOON, 0.10, "sooner", TEAL, -1), plot.side_tag(M_SAME, 0.12, "same", TEAL, +1),
            plot.side_tag(M_LATE, 0.30, "later", TEAL, +1)]
    return gs, tags


def banner_q():
    a = T("What will the drug do?", 34, TEXT, weight=BOLD).move_to([BAND_X, 3.5, 0])
    b = T("sooner, later, or the same?", 34, TEAL, weight=BOLD).move_to([BAND_X, 2.88, 0])
    return a, b


def delayed_marks(plot):
    t50 = lambda m: m[0] * (np.log(2)) ** (1.0 / m[1])
    a = Arrow(plot.P(t50(M_NONGF), 0.5), plot.P(t50(M_DRUG), 0.5), buff=0, color=TEXT, stroke_width=5,
              tip_length=0.22)
    lab = T("death\ndelayed", 26, TEXT, weight=BOLD, line_spacing=0.8)
    hs = lab.height / (plot.y1 - plot.y0) / 2
    sl = 0.33
    xa = plot.P(t_at(M_NONGF, sl - hs), sl - hs)[0]     # red curve at the label's lowest edge
    xb = plot.P(t_at(M_DRUG, sl + hs), sl + hs)[0]      # teal curve at the label's highest edge
    lab.move_to([(xa + xb) / 2, plot.P(0, sl)[1], 0])
    return a, lab


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Death Machinery in Neurons"
    TITLE = "A Neuron Must Work to Die"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    """The question: run down, or do something?"""

    def construct(self):
        c = np.array([0.0, 0.1, 0.0])
        n = place(neuron(2.0), c)
        ring = ring_dots(c, 2.75, 8, YELLOW, 0.14)
        sig = T("survival signal", 30, YELLOW, weight=BOLD).move_to([4.75, 3.15, 0])
        sar = arr([3.2, 3.05, 0], ring[1].get_center() + [0.3, 0.08, 0], YELLOW)
        self.at("When a young neuron")
        self.play(FadeIn(n), FadeIn(ring), run_time=0.7)
        self.at("loses its")
        gone = AnimationGroup(*[d.animate.shift((d.get_center() - c) * 0.35).set_opacity(0) for d in ring], run_time=2.0)
        self.play(gone, Succession(Wait(0.5), AnimationGroup(FadeIn(sig, shift=DOWN * 0.1), GrowArrow(sar), run_time=0.5)))
        self.at("does it simply")
        self.play(FadeOut(sig), FadeOut(sar), run_time=0.4)
        left = bchip("run down?", GREY, 40).move_to([-3.9, -3.05, 0])
        right = bchip("do something?", TEAL, 40).move_to([3.9, -3.05, 0])
        al = arr(c + [-1.2, -1.55, 0], left.get_top() + [0.6, 0.08, 0], GREY)
        ar = arr(c + [1.2, -1.55, 0], right.get_top() + [-0.6, 0.08, 0], TEAL)
        dims, rests = dim_anims(n, 0.45)
        self.at("run down")
        self.play(GrowArrow(al), FadeIn(left, shift=DOWN * 0.15), *dims, run_time=0.7)
        self.at("Or does it do something")
        self.play(*rests(), GrowArrow(ar), FadeIn(right, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(SpokenScene):
    """Three wells of neurons, NGF named; then the layout settles into stage B."""

    def construct(self):
        xs = [-4.4, 0.0, 4.4]
        A = [make_well(x, -0.1, 3.8, 4.5) for x in xs]
        top = T("young rat sympathetic neurons", 32, LG).move_to([0, 3.15, 0])
        ldot = Dot(radius=0.12, color=YELLOW)
        ltxt = T("NGF, nerve growth factor", 32, YELLOW, weight=BOLD)
        legend = VGroup(ldot, ltxt).arrange(RIGHT, buff=0.25).move_to([0, -3.2, 0])
        B = [make_well(WELL_CX, WELL_Y[i], WELL_W, WELL_H) for i in range(3)]
        axes = PLOT_B.axes()

        self.play(*[FadeIn(w[0]) for w in A], run_time=0.25)
        self.at("young rat")
        self.play(*[FadeIn(w[1]) for w in A], FadeIn(top), run_time=0.9)
        self.at("nerve growth factor")
        self.play(*[LaggedStart(*[FadeIn(d, scale=0.4) for d in w[2]], lag_ratio=0.08, run_time=1.2) for w in A],
                  FadeIn(legend, run_time=0.8))
        for w in A:
            self.add(w[2])
        self.at("NGF")
        self.play(Indicate(legend, color=YELLOW, scale_factor=1.08), run_time=0.5)
        self.wait(0.15)
        self.play(*[Transform(a, b) for a, b in zip(A, B)], FadeOut(top), FadeOut(legend), FadeIn(axes),
                  run_time=0.85)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    """Well 1 keeps its NGF: a flat survival curve."""

    def construct(self):
        sb = StageB(0).add_to(self)
        w1 = sb.wells[0]
        self.at("The first well")
        self.play(w1[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.08), run_time=0.5)
        self.at("keeps its NGF")
        self.play(FadeIn(sb.labels[0], shift=UP * 0.1), run_time=0.7)
        self.at("Those neurons live")
        mob, anim = sb.plot.grow(self, M_NGF, GREEN, 0, 4, 1.7)
        self.play(anim, Succession(Wait(1.4), FadeIn(sb.sw[0], scale=0.5, run_time=0.3)))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(SpokenScene):
    """Well 2 loses its NGF: most neurons die in a day or two."""

    def construct(self):
        sb = StageB(1).add_to(self)
        w2 = sb.wells[1]
        self.at("The second well")
        self.play(w2[0].animate.set_stroke(RED).set_fill(RED, 0.08), run_time=0.5)
        self.at("loses its")
        gone = [d.animate.shift(RIGHT * 0.5 + UP * 0.2).set_opacity(0) for d in w2[2]]
        self.play(*gone, FadeIn(sb.labels[1], shift=UP * 0.1), run_time=0.8)
        self.at("Most of those")

        def rate(u, f=2.4 / 3.3):
            return 0.6 * (u / f) if u <= f else 0.6 + 0.4 * (u - f) / (1 - f)
        mob, a1 = sb.plot.grow(self, M_NONGF, RED, 0, 4.0, 3.3, rate=rate)
        ticks = sb.plot.tick_labels(sb.axes)
        shrink = AnimationGroup(*[n.animate.scale(0.7).set_color(GREY) for n in w2[1]], run_time=0.8)
        self.play(a1,
                  Succession(Wait(1.15), shrink),
                  Succession(Wait(2.05), Indicate(VGroup(ticks[1], ticks[2]), color=TEXT, scale_factor=1.3, run_time=0.7)),
                  Succession(Wait(3.0), FadeIn(sb.sw[1], scale=0.5, run_time=0.3)))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    """Well 3 loses its NGF and gets the drug."""

    def construct(self):
        sb = StageB(2).add_to(self)
        w3 = sb.wells[2]
        lab = sb.labels[2]
        self.at("The third well")
        self.play(w3[0].animate.set_stroke(TEAL).set_fill(TEAL, 0.08), run_time=0.5)
        self.at("loses its")
        gone = [d.animate.shift(RIGHT * 0.5 + UP * 0.2).set_opacity(0) for d in w3[2]]
        self.play(*gone, FadeIn(lab[0], shift=UP * 0.1), run_time=0.8)
        p = pill([-2.05, -2.25, 0])
        self.at("It also gets a drug")
        self.play(FadeIn(p, scale=0.6), run_time=0.4)
        self.play(p.animate.move_to([WELL_CX + 0.3, WELL_Y[2], 0]), run_time=0.9)
        self.at("stops protein synthesis")
        self.play(FadeOut(p, scale=0.4), w3[0].animate.set_fill(TEAL, 0.18), FadeIn(lab[1], shift=UP * 0.1),
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06(SpokenScene):
    """Question held: sooner, later, or the same? Three dashed guesses."""

    def construct(self):
        sb = StageB(3).add_to(self)
        qa, qb = banner_q()
        gs, tags = guess_set(sb.plot)
        self.at("What will that drug do")
        self.play(FadeIn(qa, shift=DOWN * 0.1), Indicate(sb.wells[2][0], color=TEAL, scale_factor=1.04), run_time=0.8)
        self.at("Will these neurons die")
        self.play(FadeIn(qb, shift=DOWN * 0.1), run_time=0.5)
        self.at("sooner")
        self.play(Create(gs[0]), run_time=0.6)
        self.play(FadeIn(tags[0]), run_time=0.2)
        self.at("later")
        self.play(Create(gs[2]), run_time=0.6)
        self.play(FadeIn(tags[2]), run_time=0.2)
        self.at("same schedule")
        self.play(Create(gs[1]), run_time=0.6)
        self.play(FadeIn(tags[1]), run_time=0.2)
        self.finish()


class S07Pause(NarratedScene):
    """The question held, still, for five seconds."""

    def construct(self):
        sb = StageB(3).add_to(self)
        qa, qb = banner_q()
        gs, tags = guess_set(sb.plot)
        self.add(qa, qb, *gs, *tags)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08(SpokenScene):
    """Later. The death is delayed."""

    def construct(self):
        sb = StageB(3).add_to(self)
        qa, qb = banner_q()
        gs, tags = guess_set(sb.plot)
        self.add(qa, qb, *gs, *tags)
        arrow, dl = delayed_marks(sb.plot)
        self.at("Later")
        mob, anim = sb.plot.grow(self, M_DRUG, TEAL, 0, 4, 1.4, w=7)
        self.bring_to_front(tags[2])
        self.play(FadeOut(qa), FadeOut(qb), FadeOut(gs[0]), FadeOut(gs[1]), FadeOut(tags[0]), FadeOut(tags[1]),
                  FadeOut(gs[2]), anim, Succession(Wait(1.1), FadeIn(sb.sw[2], scale=0.5, run_time=0.3)), run_time=1.4)
        self.at("the death is delayed")
        self.play(GrowArrow(arrow), FadeIn(dl, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def final_B():
    """stage B with all three curves, the 'later' tag and the delay arrow"""
    sb = StageB(3)
    arrow, dl = delayed_marks(sb.plot)
    tg = sb.plot.side_tag(M_LATE, 0.30, "later", TEAL, +1)
    return sb, arrow, dl, tg


class S09(SpokenScene):
    """The credit: 1988."""

    def construct(self):
        sb, arrow, dl, tg = final_B()
        sb.add_to(self)
        self.add(sb.curves[2], sb.sw[2], arrow, dl, tg)
        year = T("1988", 44, GOLD, font=TITLE_FONT)
        name = T("Martin, Johnson and colleagues", 28, TEXT)
        cred = VGroup(name, year).arrange(RIGHT, buff=0.4).move_to([BAND_X, 3.15, 0])
        self.at("1988")
        self.play(FadeIn(year, shift=DOWN * 0.1), run_time=0.5)
        self.at("Johnson's laboratory")
        self.play(FadeIn(name, shift=RIGHT * 0.15), run_time=0.6)
        self.at("this result")
        self.play(Indicate(sb.curves[2], color=TEAL, scale_factor=1.0), Indicate(dl, color=TEXT, scale_factor=1.1),
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10(SpokenScene):
    """RNA or protein synthesis blocked: deprived neurons are kept alive longer."""

    def construct(self):
        c = np.array([0.0, -0.3, 0.0])
        n = place(neuron(1.7), c)
        nl = T("no NGF", 32, YELLOW, weight=BOLD).move_to([0, -2.55, 0])
        self.add(n, nl)
        p1 = pill([-4.2, 3.0, 0], w=1.5, h=0.68)
        l1 = T("RNA synthesis blocked", 28, TEAL, weight=BOLD).move_to([-4.2, 2.1, 0])
        a1 = arr([-3.4, 1.7, 0], c + [-1.0, 1.35, 0], TEAL)
        p2 = pill([4.2, 3.0, 0], w=1.5, h=0.68)
        l2 = T("protein synthesis blocked", 28, TEAL, weight=BOLD).move_to([4.2, 2.1, 0])
        a2 = arr([3.4, 1.7, 0], c + [1.0, 1.35, 0], TEAL)
        self.at("RNA synthesis")
        self.play(FadeIn(p1, shift=DOWN * 0.15), FadeIn(l1), GrowArrow(a1), run_time=0.8)
        self.at("of protein synthesis")
        self.play(FadeIn(p2, shift=DOWN * 0.15), FadeIn(l2), GrowArrow(a2), run_time=0.8)
        alive = T("kept alive longer", 40, GREEN, weight=BOLD).move_to([0, -3.4, 0])
        self.at("kept deprived neurons")
        self.play(n.body.animate.set_stroke(GREEN), FadeIn(alive, shift=UP * 0.15), run_time=0.7)
        self.play(Indicate(n, color=GREEN, scale_factor=1.06), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def battery(center, segs_on=4, sc=1.0):
    w, h = 3.4, 1.9
    frame = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=GREY, stroke_width=5)
    nub = RoundedRectangle(corner_radius=0.06, width=0.25, height=0.7, stroke_width=0, fill_color=GREY,
                           fill_opacity=1).move_to(frame.get_right() + RIGHT * 0.12)
    segs = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.62, height=1.35, stroke_width=0, fill_color=GREEN,
                                     fill_opacity=1 if i < segs_on else 0.0)
                    .move_to(frame.get_left() + RIGHT * (0.5 + i * 0.75)) for i in range(4)])
    g = VGroup(frame, nub, segs).scale(sc).move_to(center)
    g.segs = segs
    return g


class S11(SpokenScene):
    """The run-down idea: a battery draining beside a neuron."""

    def construct(self):
        nc = np.array([-3.7, 0.35, 0.0])
        n = place(neuron(2.0), nc)
        bat = battery([3.55, 0.35, 0], sc=1.45)
        self.at("Why is that strange")
        self.play(FadeIn(n), FadeIn(bat), run_time=0.8)
        st = T("starved of what it needs", 30, LG).move_to([-3.7, -2.45, 0])
        self.at("A cell starved")
        self.play(FadeIn(st, shift=UP * 0.1), run_time=0.6)
        rl = T("the run-down idea", 34, LG, weight=BOLD).move_to([3.55, -2.45, 0])
        self.at("should simply run down")
        dims, _ = dim_anims(n, 0.4)
        self.play(FadeIn(rl, shift=UP * 0.1), *dims,
                  LaggedStart(*[s.animate.set_fill(GREEN, 0) for s in reversed(list(bat.segs))], lag_ratio=0.7),
                  run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
PLOT_F = Plot(-5.0, 5.9, -2.75, 2.55, 4)


class S12(SpokenScene):
    """Prediction: blocking protein synthesis should make death come sooner; the real curve is later."""

    def construct(self):
        pl = PLOT_F
        axes = pl.axes()
        red = pl.curve(M_NONGF, RED)
        rl = pl.side_tag(M_NONGF, 0.35, "no NGF", RED, +1)
        self.add(axes, red, rl)
        chipd = bchip("protein synthesis blocked", TEAL, 28).move_to([BAND_X - 2.2, 3.4, 0])
        self.at("Stopping protein synthesis")
        self.play(FadeIn(chipd, shift=DOWN * 0.1), run_time=0.6)
        pred = pl.dashed(M_SOON, GREY, 6)
        pl_lab = T("run-down\nprediction", 24, LG).move_to([-4.15, 3.2, 0])
        self.at("make it run down")
        self.play(Create(pred), FadeIn(pl_lab), run_time=0.7)
        real = pl.curve(M_DRUG, TEAL, 7)
        real_lab = pl.side_tag(M_DRUG, 0.45, "what happened", TEAL, +1)
        cross = xmark(pl.P(t_at(M_SOON, 0.72), 0.72), 0.24, RED, 8)
        self.at("faster")
        self.play(Create(cross), run_time=0.35)
        self.play(Create(real), FadeIn(real_lab), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def big_neuron(r=2.1, c=(0.0, 0.55, 0.0), lit=False):
    """c is the centre of the cell BODY"""
    c = np.array(c, float)
    n = place(neuron(r), c)
    angs = (20, 85, 150, 215, 280, 335)
    sq = VGroup(*[rna(c + unit(a) * 0.7 * r, np.radians(a + 90 + (20 if i % 2 else -20)))
                  for i, a in enumerate(angs)])
    if lit:
        n.nuc.set_fill(TEAL, 0.9)
    return n, sq, c


class S13(SpokenScene):
    """The nucleus lights up; new transcripts leave it one after another."""

    def construct(self):
        n, sq, c = big_neuron()
        self.add(n)
        self.at("Instead")
        self.play(n.nuc.animate.set_fill(TEAL, 0.95).scale(1.25), run_time=0.7)
        # Each full-opacity stroke appears at the nuclear boundary, then travels out.
        starts = [s.copy().move_to(c + unit(a) * n.nuc.radius * 1.25)
                  for s, a in zip(sq, (20, 85, 150, 215, 280, 335))]
        lab = T("needs new RNA and protein", 36, TEAL, weight=BOLD).move_to([0, -2.85, 0])
        self.at("make something")
        self.play(LaggedStart(*[Succession(FadeIn(s, run_time=0.1),
                                          Transform(s, t, run_time=0.5, rate_func=linear))
                                for s, t in zip(starts, sq)], lag_ratio=0.28),
                  FadeIn(lab, shift=UP * 0.15, run_time=0.5))
        self.finish()


class S14(SpokenScene):
    """Death is something the cell does. It is a program."""

    def construct(self):
        n, sq, c = big_neuron(lit=True)
        n.nuc.scale(1.25)
        self.add(n, sq)
        a = T("Death is something the cell does.", 38, TEXT, font=TITLE_FONT).move_to([0, -2.4, 0])
        b = T("It is a program.", 38, TEAL, font=TITLE_FONT, weight=BOLD).move_to([0, -3.0, 0])
        self.at("death is something")
        self.play(FadeIn(a, shift=UP * 0.15), run_time=0.8)
        self.at("a program")
        self.play(FadeIn(b, shift=UP * 0.15), Indicate(n.nuc, color=TEAL, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
LX, RX, CYC = -3.45, 3.45, -0.35


def panel(cx, title=None, tint=None):
    rect = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.5, stroke_color=GREY, stroke_width=3,
                            fill_color=tint or GREY, fill_opacity=0.12 if tint else 0.05).move_to([cx, -0.325, 0])
    g = VGroup(rect)
    if title:
        g.add(T(title, 38, TEXT, weight=BOLD).move_to([cx, 3.35, 0]))
    return g


def necro_cell(cx, cy, r=1.6):
    fill = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.22).move_to([cx, cy, 0])
    nuc = Circle(radius=r * 0.4, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.5).move_to([cx, cy, 0])
    arcs = VGroup(*[Arc(radius=r, start_angle=np.radians(a + 2), angle=np.radians(41), stroke_color=BLUE, stroke_width=5)
                    .move_arc_center_to([cx, cy, 0]) for a in range(0, 360, 45)])
    return fill, nuc, arcs


def fail_arcs_anim(arcs, cx, cy):
    out = []
    for i, a in enumerate(arcs):
        mid = np.radians(i * 45 + 22)
        d = np.array([np.cos(mid), np.sin(mid), 0])
        if i in (1, 4, 6):
            out.append(a.animate.shift(d * 0.25).set_color(RED).set_opacity(0))
        else:
            out.append(a.animate.shift(d * 0.18).set_color(RED))
    return out


def failed_state(arcs):
    gone = []
    for i, a in enumerate(arcs):
        mid = np.radians(i * 45 + 22)
        d = np.array([np.cos(mid), np.sin(mid), 0])
        if i in (1, 4, 6):
            gone.append(a)
        else:
            a.shift(d * 0.18).set_color(RED)
    arcs.remove(*gone)


SPILL = [(0.0, 1.0), (0.9, 1.15), (1.8, 1.3), (2.7, 0.95), (3.6, 1.2), (4.5, 1.1), (5.4, 1.25), (0.5, 0.55),
         (2.2, 0.6), (4.0, 0.5)]


def spill_dots(cx, cy, out=True):
    ds = VGroup()
    for ang, f in SPILL:
        rr = (2.4 + 0.12 * np.sin(ang * 3)) if out else 1.2 * f * 0.6
        ds.add(Dot([cx + rr * np.cos(ang), cy + rr * np.sin(ang), 0], radius=0.08, color=BLUE))
    return ds


def glow(cx, cy):
    """soft red glow: the inflamed tissue around the cell"""
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=RED, fill_opacity=o).move_to([cx, cy, 0])
                    for r, o in ((3.0, 0.08), (2.65, 0.08))])


def necro_swollen(failed=True):
    fill, nuc, arcs = necro_cell(LX, CYC)
    fill.scale(1.25)
    nuc.scale(1.15)
    arcs.scale(1.25, about_point=np.array([LX, CYC, 0]))
    if failed:
        failed_state(arcs)
    return fill, nuc, arcs


def infl_label():
    return T("inflammation", 30, RED, weight=BOLD).move_to([LX, 2.65, 0])


def necro_final():
    fill, nuc, arcs = necro_swollen(True)
    sp = spill_dots(LX, CYC)
    gl = glow(LX, CYC)
    return fill, nuc, arcs, sp, gl, infl_label()


def apop_clumps(cx, cy, s=1.0):
    offs = [(-0.36, 0.24), (0.36, 0.30), (0.0, -0.42)]
    return VGroup(*[Circle(radius=0.26 * s, stroke_color=TEXT, stroke_width=2.5, fill_color=DARK, fill_opacity=1)
                    .move_to([cx + dx * s, cy + dy * s, 0]) for dx, dy in offs])


APOP_R0, APOP_R1 = 1.6, 1.12     # cell radius before and after it shrinks


def apop_cell_final(cx, cy):
    body = Circle(radius=APOP_R1, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to([cx, cy, 0])
    return body, apop_clumps(cx, cy, 1.0)


class S15(SpokenScene):
    """Two broad ways cells die: necrosis first."""

    def construct(self):
        pl, pr = panel(LX), panel(RX)
        fill, nuc, arcs = necro_cell(LX, CYC)
        ttl = T("necrosis", 38, TEXT, weight=BOLD).move_to([LX, 3.35, 0])
        self.at("two broad ways")
        self.play(FadeIn(pl), FadeIn(pr), run_time=0.8)
        self.at("cells die")
        self.play(FadeIn(fill), FadeIn(nuc), FadeIn(arcs), run_time=0.7)
        self.at("The first is necrosis")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S16(SpokenScene):
    """In necrosis the cell swells and its membrane fails."""

    def construct(self):
        pl, pr = panel(LX, "necrosis"), panel(RX)
        fill, nuc, arcs = necro_cell(LX, CYC)
        self.add(pl, pr, fill, nuc, arcs)
        c1 = bchip("trauma", LG, 28)
        c2 = bchip("loss of blood supply", LG, 28)
        VGroup(c1, c2).arrange(RIGHT, buff=0.25).move_to([LX, 2.35, 0])
        self.at("after trauma")
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.5)
        self.at("loss of blood supply")
        self.play(FadeIn(c2, shift=DOWN * 0.1), run_time=0.5)
        ctr = np.array([LX, CYC, 0])
        self.at("the cell swells")
        self.play(fill.animate.scale(1.25), nuc.animate.scale(1.15), arcs.animate.scale(1.25, about_point=ctr),
                  FadeOut(c1), FadeOut(c2), run_time=1.5)
        self.at("membranes fail")
        self.play(*fail_arcs_anim(arcs, LX, CYC), run_time=0.9)
        self.finish()


class S17(SpokenScene):
    """Contents spill out; the tissue around it becomes inflamed."""

    def construct(self):
        pl, pr = panel(LX, "necrosis"), panel(RX)
        gl = glow(LX, CYC)
        fill, nuc, arcs = necro_swollen(True)
        self.add(pl, pr, gl, fill, nuc, arcs)
        gl.set_opacity(0)
        sp = spill_dots(LX, CYC)
        inside = spill_dots(LX, CYC, out=False)
        lab = infl_label()
        for d in sp:
            d.set_opacity(0)
        self.add(inside)
        self.at("contents spill")
        self.play(*[Transform(a, b.set_opacity(1)) for a, b in zip(inside, sp)], run_time=1.4)
        self.at("the tissue around it")
        self.play(*[m.animate.set_fill(RED, 0.08) for m in gl], run_time=0.9)
        self.at("becomes inflamed")
        self.play(pl[0].animate.set_fill(RED, 0.12), FadeIn(lab, shift=UP * 0.1), run_time=0.9)
        self.finish()


def left_final(dim=1.0):
    pl = panel(LX, "necrosis", tint=RED)
    fill, nuc, arcs, sp, gl, lab = necro_final()
    g = VGroup(pl, gl, fill, nuc, arcs, sp, lab)
    if dim < 1:
        dim_static(g, dim)
    return g


class S18(SpokenScene):
    """Apoptosis: the cell shrinks and its chromatin condenses into dense clumps."""

    def construct(self):
        left = left_final(0.4)
        pr = panel(RX)
        self.add(left, pr)
        ttl = T("apoptosis", 38, TEXT, weight=BOLD).move_to([RX, 3.35, 0])
        ctr = np.array([RX, CYC, 0])
        body = Circle(radius=APOP_R0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to(ctr)
        nuc = Circle(radius=APOP_R0 * 0.4, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.5).move_to(ctr)
        self.at("apoptosis")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), FadeIn(body), FadeIn(nuc), run_time=0.9)
        k = APOP_R1 / APOP_R0
        self.at("the cell shrinks")
        self.play(body.animate.scale(k), nuc.animate.scale(k), run_time=1.3)
        clumps = apop_clumps(RX, CYC, 1.0)
        self.at("chromatin condenses")
        self.play(nuc.animate.set_fill(DARK, 0.95).set_stroke(TEXT, 2.5), run_time=0.7)
        self.at("dense clumps")
        self.play(ReplacementTransform(nuc, clumps), run_time=0.65)
        self.finish()


FRAG = [(1.45, 1.5), (3.2, 1.8), (2.2, -0.1), (4.2, 0.7), (1.6, -1.6)]   # fragments settle here
ENG_C, ENG_R = np.array([4.8, -1.7, 0.0]), 1.6


class S19(SpokenScene):
    """The cell buds into wrapped fragments; a neighbour engulfs them."""

    def construct(self):
        left = left_final(0.4)
        pr = panel(RX, "apoptosis")
        body, clumps = apop_cell_final(RX, CYC)
        self.add(left, pr, body, clumps)
        offs = [(0.95 * np.cos(np.radians(90 + 72 * i)), 0.95 * np.sin(np.radians(90 + 72 * i))) for i in range(5)]
        blebs = VGroup()
        for dx, dy in offs:
            c = np.array([RX + dx, CYC + dy, 0])
            blebs.add(VGroup(Circle(radius=0.38, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to(c),
                             Circle(radius=0.13, stroke_color=TEXT, stroke_width=2, fill_color=DARK, fill_opacity=1).move_to(c)))
        self.at("breaks into membrane")
        self.add(blebs)
        self.play(FadeOut(clumps), run_time=0.3)
        self.play(FadeOut(body),
                  *[b.animate.move_to([x, y, 0]) for b, (x, y) in zip(blebs, FRAG)], run_time=1.3)
        nc = ENG_C
        nb = Circle(radius=ENG_R, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to(nc)
        nn = Circle(radius=0.22, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to(nc)
        self.at("other cells")
        self.play(FadeIn(nb), FadeIn(nn), run_time=0.7)
        tg = [[-0.65, 0.4], [0.1, 0.8], [0.7, 0.2], [-0.6, -0.45], [0.5, -0.65]]
        self.at("swallow")
        # Keep the fragments bright and in front as they cross the membrane.
        self.bring_to_front(blebs)
        self.play(*[Transform(b, b.copy().scale(0.6).move_to(nc + [x, y, 0]), rate_func=linear)
                    for b, (x, y) in zip(blebs, tg)], run_time=0.85)
        self.finish()


class S20(SpokenScene):
    """Close-up: the pyknotic nucleus."""

    def construct(self):
        c = np.array([-1.5, 0.2, 0.0])
        body = Circle(radius=2.4, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.22).move_to(c)
        clumps = apop_clumps(c[0], c[1], 1.7)
        self.at("A nucleus condensed")
        self.play(GrowFromCenter(body), run_time=0.7)
        self.play(FadeIn(clumps, scale=0.5), run_time=0.5)
        lab = T("pyknotic nucleus", 36, TEXT, font=TITLE_FONT).move_to([4.0, 1.5, 0])
        ar = arr([2.15, 1.3, 0], clumps[1].get_center() + RIGHT * 0.28, TEXT)
        self.at("is called")
        self.play(FadeIn(lab, shift=LEFT * 0.2), FadeIn(ar, run_time=0.2), run_time=0.5)
        self.finish()


class S21(SpokenScene):
    """Counting pyknotic nuclei in an embryo tissue section."""

    def construct(self):
        rs = np.random.RandomState(11)
        pyk = [(-4.6, 1.6), (-1.3, 2.2), (2.2, 1.0), (4.9, 2.1), (-3.0, -1.6), (1.0, -1.4)]
        pts = []
        for _ in range(900):
            x, y = rs.uniform(-6.0, 6.0), rs.uniform(-2.5, 2.6)
            if all((x - a) ** 2 + (y - b) ** 2 > 0.7 ** 2 for a, b in pts + pyk):
                pts.append((x, y))
            if len(pts) >= 28:
                break
        tissue = RoundedRectangle(corner_radius=0.25, width=12.8, height=6.0, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.06).move_to([0, 0.0, 0])
        norm = VGroup(*[Circle(radius=0.26, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.3)
                        .move_to([x, y, 0]) for x, y in pts])
        pk = VGroup(*[Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=DARK, fill_opacity=1)
                      .move_to([x, y, 0]) for x, y in pyk])
        cap = T("section of an embryo", 28, LG).move_to([-4.3, 3.4, 0])
        # the section fades in at once (no dark opening frame)
        self.play(FadeIn(tissue), FadeIn(norm), FadeIn(cap), run_time=0.3)
        lab = T("counted:", 32, LG).move_to([-1.4, -3.4, 0])
        self.at("neuron death in embryos")
        self.play(FadeIn(pk, scale=1.5), FadeIn(lab), run_time=0.5)
        self.at("counted")
        for i, (x, y) in enumerate(pyk):
            ring = Circle(radius=0.36, stroke_color=GOLD, stroke_width=5).move_to([x, y, 0])
            st = Line([-0.2 + 0.32 * i, -3.2, 0], [-0.2 + 0.32 * i, -3.6, 0], color=TEXT, stroke_width=6)
            self.play(Create(ring), Create(st), run_time=0.3)
            self.wait(0.05)
        self.finish()


# ---------------------------------------------------------------------------------------------
BOX_X = [-4.4, 0.0, 4.4]
BOX_TXT = [("What must\nbe made?", TEAL), ("What are\nthe parts?", RED),
           ("What keeps\nthem off while\nNGF is present?", YELLOW)]


def boxes(filled=0):
    rects, nums, txts = [], [], []
    for i, x in enumerate(BOX_X):
        col = BOX_TXT[i][1] if i < filled else GREY
        r = RoundedRectangle(corner_radius=0.2, width=4.0, height=5.2, stroke_color=col, stroke_width=4,
                             fill_color=col, fill_opacity=0.1 if i < filled else 0.04).move_to([x, 0.0, 0])
        n = T(str(i + 1), 72, GOLD, font=TITLE_FONT, weight=BOLD).move_to([x, 1.65, 0])
        t = VGroup(*[T(ln, 34, BOX_TXT[i][1], weight=BOLD) for ln in BOX_TXT[i][0].split("\n")]).arrange(DOWN, buff=0.18)
        t.move_to([x, -0.35, 0])
        rects.append(r)
        nums.append(n)
        txts.append(t)
    return rects, nums, txts


class S22(SpokenScene):
    """Three empty numbered boxes, from the first word."""

    def construct(self):
        rects, nums, txts = boxes(0)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(r, scale=0.94), FadeIn(n)) for r, n in zip(rects, nums)],
                              lag_ratio=0.25), run_time=1.1)
        self.at("three puzzles")
        self.play(*[Indicate(n, color=GOLD, scale_factor=1.2) for n in nums], run_time=0.7)
        self.finish()


def puzzle_scene(scene, k, cue):
    rects, nums, txts = boxes(k)
    r0, n0, t0 = boxes(k + 1)
    for i in range(3):
        if i < k:
            scene.add(r0[i], n0[i], t0[i])
        else:
            scene.add(rects[i], nums[i])
    r_new = rects[k]
    scene.at(cue)
    scene.play(Transform(r_new, r0[k]), FadeIn(t0[k], shift=UP * 0.15), run_time=0.9)
    scene.play(Indicate(t0[k], color=BOX_TXT[k][1], scale_factor=1.06), run_time=0.7)
    scene.finish()


class S23(SpokenScene):
    def construct(self):
        puzzle_scene(self, 0, "what must a deprived")


class S24(SpokenScene):
    def construct(self):
        puzzle_scene(self, 1, "which proteins carry out")


class S25(SpokenScene):
    def construct(self):
        puzzle_scene(self, 2, "what keeps those")


# ---------------------------------------------------------------------------------------------
class S26(SpokenScene):
    """The take-home fact: deprived, not just fading, runs a program."""

    def construct(self):
        n, sq, c = big_neuron(r=2.0, c=(0.0, -0.2, 0.0))
        ring = ring_dots(c, 2.75, 8, YELLOW, 0.14)
        head = T("One fact to hold on to", 38, GOLD, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.at("So hold on")
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(n), FadeIn(ring), run_time=0.7)
        dep = T("deprived", 36, YELLOW, weight=BOLD).move_to([-4.4, 0.7, 0])
        self.at("A deprived young")
        self.play(*[d.animate.shift((d.get_center() - c) * np.array([0.3, 0.12, 0])) for d in ring],
                  FadeIn(dep, shift=RIGHT * 0.1, run_time=0.4), run_time=2.1)
        self.play(FadeOut(ring), run_time=0.4)
        fade = bchip("fade", LG, 40).move_to([-4.4, -1.4, 0])
        self.at("does not just fade")
        dims, rests = dim_anims(n, 0.35)
        self.play(*dims, FadeIn(fade, shift=UP * 0.1), run_time=0.8)
        strike = Line(fade.get_left() + [0.05, 0, 0], fade.get_right() + [-0.05, 0, 0], color=RED, stroke_width=4)
        self.at("just fade")
        self.play(Create(strike), run_time=0.4)
        prog = T("runs a program", 36, TEAL, weight=BOLD).move_to([4.4, 0.7, 0])
        self.at("It runs a program")
        self.play(FadeOut(fade), FadeOut(strike), *rests(), n.nuc.animate.set_fill(TEAL, 0.95).scale(1.25),
                  FadeIn(prog, shift=LEFT * 0.1), run_time=0.8)
        starts = [s.copy().move_to(c + unit(a) * 0.55).scale(0.6).set_stroke(opacity=0)
                  for s, a in zip(sq, (20, 85, 150, 215, 280, 335))]
        self.add(*starts)
        lab = T("new RNA and protein", 36, TEAL, weight=BOLD).move_to([0, -3.2, 0])
        self.at("needs new RNA")
        self.play(LaggedStart(*[s.animate.set_stroke(opacity=1).scale(1 / 0.6).move_to(t.get_center())
                                for s, t in zip(starts, sq)], lag_ratio=0.3, run_time=1.5),
                  FadeIn(lab, shift=UP * 0.1, run_time=0.6))
        self.finish()


class S27End(EndCard):
    LINE = "A deprived cultured neuron runs a program that needs new RNA and protein."
