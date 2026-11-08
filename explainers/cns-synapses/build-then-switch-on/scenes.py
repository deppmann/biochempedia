"""Astrocytes Build and Switch On  (chapter 3 of "Synapses in the Brain", Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept; shared with chapters 1 and 2 where the concept recurs)
  GREY   = neurons, dishes, membranes, synapse outlines, de-emphasized
  TEAL   = synaptic vesicles and the transmitter inside them (and release events)
  ORANGE = AMPA receptors
  PURPLE = NMDA receptors
  GREEN  = working / responds / "on"
  RED    = blocked / absent / not responding
  TEXT   = astrocyte (white): glia, thrombospondin, glypicans, the rise they cause
  BLUE   = the recorded current trace
  YELLOW = action potentials (firing); neuroligin from chapters 1-2 does not appear in this chapter
  GOLD   = title rule only

Traces are computed: mini currents from a double-exponential waveform, action potentials from a
Hodgkin-Huxley simulation (the time axis of the mini traces is schematic, so no axes are drawn).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#D98CB3"

_house_chip = chip


def chip(*args, **kwargs):
    g = _house_chip(*args, **kwargs)
    back = RoundedRectangle(corner_radius=.14, width=g.width, height=g.height,
                            stroke_width=0, fill_color=BG, fill_opacity=1).move_to(g)
    return VGroup(back, g)


# ---------------------------------------------------------------------------------------------
# layout
# ---------------------------------------------------------------------------------------------
DX, DY = -2.6, 1.7                       # the dish strip (left zone); right zone x 1.6..6.8 holds notes
NX = [-5.6, -4.1, -2.6, -1.1, 0.4]       # neuron x positions
PX0, PX1, PY_C, PH = -6.4, 6.4, -1.6, 4.0  # trace panel
CUR_BASE = PY_C + 0.5                    # resting level of a current trace


def neuron(x, y, r=0.34, color=GREY):
    soma = Circle(r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=.3).move_to([x, y, 0])
    arms = []
    for a in (25, 155, 270):
        d = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
        arms.append(Line([x, y, 0] + d * r, [x, y, 0] + d * (r + .28), color=color, stroke_width=3))
    return VGroup(soma, *arms)


def stage_dish(n=5):
    d = RoundedRectangle(corner_radius=.2, width=7.6, height=1.4, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=.08).move_to([DX, DY, 0])
    ns = VGroup(*[neuron(x, DY) for x in NX[:n]])
    return d, ns


def fire(ns):
    return LaggedStart(*[Indicate(n, color=YELLOW, scale_factor=1.12) for n in ns], lag_ratio=.2)


def panel(label="recorded current", color=GREY, cy=PY_C, h=PH, w=None, x0=None, bar="time", bar_len=1.2):
    """Trace panel. Returns (box, lab): lab = the label (top-left) plus a 'schematic' tag and one time bar (bottom)."""
    w = w or (PX1 - PX0)
    x0 = PX0 if x0 is None else x0
    box = RoundedRectangle(corner_radius=.15, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                           fill_color=BG, fill_opacity=1).move_to([x0 + w / 2, cy, 0])
    lab = T(label, 26, color)
    lab.move_to([x0 + .25 + lab.width / 2, cy + h / 2 - .3, 0])
    tag = T("schematic", 22, GREY).move_to([x0 + .25 + .75, cy - h / 2 + .28, 0])
    xr = x0 + w - .3
    tb = Line([xr - bar_len, cy - h / 2 + .3, 0], [xr, cy - h / 2 + .3, 0], color=GREY, stroke_width=4)
    tl = T(bar, 22, GREY).next_to(tb, LEFT, buff=.12)
    return box, VGroup(lab, tag, tb, tl)


# ---------------------------------------------------------------------------------------------
# computed traces
# ---------------------------------------------------------------------------------------------
TT, NP = 2.0, 600
tt = np.linspace(0, TT, NP)
_s = np.linspace(0, 1, 5000)
KMAX = (np.exp(-_s / .06) - np.exp(-_s / .012)).max()
NOISE = np.convolve(np.random.default_rng(5).normal(0, 1, NP + 8), np.ones(5) / 5, "same")[:NP] * .05


def mini_wave(t0, amp, tr=.012, td=.06):
    s = np.clip(tt - t0, 0, None)
    k = (np.exp(-s / td) - np.exp(-s / tr)) / KMAX
    return -amp * np.where(tt >= t0, k, 0.0)


def mini_vals(events):
    v = NOISE.copy()
    for t0, a in events:
        v = v + mini_wave(t0, a)
    return v


def _glia_events():
    rng = np.random.default_rng(11)
    slots = np.linspace(.12, 1.85, 12)
    ts = slots + rng.uniform(-.04, .04, 12)
    ts[int(np.argmin(abs(ts - 1.15)))] = 1.15
    return [(float(t), 1.3 if abs(t - 1.15) < 1e-9 else float(rng.uniform(.8, 1.7))) for t in ts]


BASE_EV = [(1.15, 1.3)]
GLIA_EV = _glia_events()


def tx(t):
    return PX0 + .3 + t / TT * (PX1 - PX0 - .6)


def to_xy(vals, base):
    return np.column_stack([tx(tt), base + vals, np.zeros(NP)])


def trace_mob(vals, base=CUR_BASE, color=BLUE, w=4):
    return VMobject(stroke_color=color, stroke_width=w).set_points_as_corners(to_xy(vals, base))


def hh(I=10.0, T_ms=150.0, dt=0.01, t_on=5.0):
    V, m, h, n = -65.0, 0.0529, 0.5961, 0.3177
    out = []
    for i in range(int(T_ms / dt)):
        cur = I if i * dt >= t_on else 0.0
        am = .1 * (V + 40 + 1e-9) / (1 - np.exp(-(V + 40 + 1e-9) / 10)); bm = 4 * np.exp(-(V + 65) / 18)
        ah = .07 * np.exp(-(V + 65) / 20); bh = 1 / (1 + np.exp(-(V + 35) / 10))
        an = .01 * (V + 55 + 1e-9) / (1 - np.exp(-(V + 55 + 1e-9) / 10)); bn = .125 * np.exp(-(V + 65) / 80)
        m += dt * (am * (1 - m) - bm * m); h += dt * (ah * (1 - h) - bh * h); n += dt * (an * (1 - n) - bn * n)
        INa = 120 * m ** 3 * h * (V - 50); IK = 36 * n ** 4 * (V + 77); IL = .3 * (V + 54.387)
        V += dt * (cur - INa - IK - IL)
        out.append(V)
    return np.array(out)


HH_V = hh()
HH_IDX = np.linspace(0, len(HH_V) - 1, 900).astype(int)
HH_BASE = -2.7


def hh_trace():
    v = HH_V[HH_IDX]
    x = np.linspace(PX0 + .3, PX1 - .3, len(v))
    y = HH_BASE + (v + 65) * .022
    return VMobject(stroke_color=YELLOW, stroke_width=3.5).set_points_as_corners(np.column_stack([x, y, np.zeros(len(v))]))


# one action potential (from the same simulation), stretched in time so it shows on the mini time axis
_pk = int(np.argmax(HH_V[:3000]))
_tmpl = HH_V[_pk - 150:_pk + 600] + 65
_tmpl_t = np.arange(len(_tmpl)) * .01 * .012      # display seconds
SPIKE_W = _tmpl_t[-1]


def spike_wave(t0, h=1.25):
    w = np.interp(tt - t0, _tmpl_t, _tmpl / 105.0 * h, left=0, right=0)
    return w


def s07_series():
    mini_ev = [(.38, .9), (1.02, 1.1), (1.58, .85)]
    spk_t = [.68, 1.32, 1.82]
    base_v = mini_vals(mini_ev)
    full = base_v + sum(spike_wave(t) for t in spk_t)
    return mini_ev, spk_t, base_v, full


# ---------------------------------------------------------------------------------------------
# small drawing parts
# ---------------------------------------------------------------------------------------------
def receptor(x, y, color=ORANGE, s=1.0, dashed=False, op=1.0):
    w, h = .22 * s, .3 * s
    pts = [[x - w, y + h, 0], [x - w, y - h, 0], [x + w, y - h, 0], [x + w, y + h, 0]]
    m = VMobject(stroke_color=color, stroke_width=6 * min(1, s + .2)).set_points_as_corners(pts)
    if dashed:
        m = DashedVMobject(m, num_dashes=14)
    m.set_stroke(opacity=op)
    return m


def tile(x, y, s=1.0, state="plain"):
    """A small synapse profile: release side above (with vesicles), receiving side below."""
    col = {"plain": GREY, "dim": GREY, "active": GREEN, "astro": TEXT, "working": GREY}[state]
    pre = RoundedRectangle(corner_radius=.07, width=.8, height=.3, stroke_color=col, stroke_width=2.5,
                           fill_color=col, fill_opacity=.3).move_to([0, .2, 0])
    dots = VGroup(*[Dot([dx, .2, 0], radius=.05, color=TEAL) for dx in (-.15, .15)])
    post = RoundedRectangle(corner_radius=.04, width=.8, height=.1, stroke_color=col, stroke_width=2.5,
                            fill_color=col, fill_opacity=.6).move_to([0, -.1, 0])
    core = VGroup(pre, dots, post)
    if state == "dim":
        core.set_opacity(.35)
    core.scale(s).move_to([x, y, 0])
    cups = tile_cups(x, y, s) if state == "working" else VGroup()
    return VGroup(core, cups)


def tile_cups(x, y, s=1.0):
    return VGroup(receptor(x - .2 * s, y - .2 * s, ORANGE, s=.28 * s), receptor(x + .2 * s, y - .2 * s, ORANGE, s=.28 * s))


def membrane(y, x0, x1):
    return RoundedRectangle(corner_radius=.1, width=x1 - x0, height=.22, stroke_color=GREY, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=.3).move_to([(x0 + x1) / 2, y, 0])


def big_synapse(cx, post_y, w=4.4, hb=1.5, gap=.85, nves=6, vr=.14):
    bb = post_y + gap
    bouton = RoundedRectangle(corner_radius=.3, width=w, height=hb, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.12).move_to([cx, bb + hb / 2, 0])
    pos = [(-.32, .32), (0, .32), (.32, .32), (-.16, .8), (.16, .8), (.48, .8), (-.48, .8)][:nves]
    ves = VGroup(*[Dot([cx + .8 * w * dx, bb + dy, 0], radius=vr, color=TEAL) for dx, dy in pos])
    post = membrane(post_y, cx - w / 2 - .2, cx + w / 2 + .2)
    return bouton, ves, post


def astro(x, y, s=1.0):
    soma = Circle(.5 * s, stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=.18).move_to([x, y, 0])
    arms = []
    for i in range(8):
        a = np.radians(22 + i * 45)
        L = (.95 if i % 2 == 0 else .72) * s
        d = np.array([np.cos(a), np.sin(a), 0])
        p0 = np.array([x, y, 0]) + d * .5 * s
        p1 = np.array([x, y, 0]) + d * (.5 * s + L * .8)
        arms.append(Line(p0, p1, color=TEXT, stroke_width=3.5))
        side = np.array([np.cos(a + .6), np.sin(a + .6), 0])
        arms.append(Line(p1, p1 + side * .22 * s, color=TEXT, stroke_width=3))
    return VGroup(soma, *arms)


def glia_glyph(x, y, s=.26):
    """The one glia / astrocyte glyph (a small star), used in s02, s09, s10 and s17."""
    return astro(x, y, s)


def lamp(x, y, on, r=.45):
    return Circle(r, stroke_color=GREEN if on else GREY, stroke_width=4, fill_color=GREEN,
                  fill_opacity=.85 if on else 0).move_to([x, y, 0])


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=.2,
                 max_tip_length_to_length_ratio=.45, max_stroke_width_to_length_ratio=12)


def cap(text, x, y, size=22, color=GREY, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
# the formula cards (s08, s13)
# ---------------------------------------------------------------------------------------------
CARD_Y = 1.5
CARD_X = [-4.55, 0.0, 4.55]
TILE_POS = [(-1.05, CARD_Y), (0, CARD_Y), (1.05, CARD_Y), (-1.05, CARD_Y - .55), (0, CARD_Y - .55), (1.05, CARD_Y - .55)]
LIT = [0, 1, 2, 3]
TICK_F = [.1, .28, .37, .6, .82]
TICK_F2 = [.19, .46, .52, .72, .91]


def card_box(cx, cy=CARD_Y):
    return RoundedRectangle(corner_radius=.18, width=3.7, height=3.0, stroke_color=GREY, stroke_width=2.5,
                            fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])


def card_title(text, cx, cy=CARD_Y):
    return T(text, 24, TEXT, line_spacing=.8).move_to([cx, cy + .88, 0])


def card1_graphic(cx=CARD_X[0], cy=CARD_Y):
    xs = np.linspace(cx - 1.5, cx + 1.5, 220)
    y = np.zeros_like(xs)
    for f, a in [(.14, .75), (.48, .9), (.80, .7)]:
        x0 = cx - 1.5 + f * 3.0
        s = np.clip(xs - x0, 0, None)
        k = (np.exp(-s / .1) - np.exp(-s / .025)); k = k / k.max()
        y -= a * np.where(xs >= x0, k, 0)
    y += np.convolve(np.random.default_rng(2).normal(0, 1, 226), np.ones(7) / 7, "same")[:220] * .02
    return VMobject(stroke_color=BLUE, stroke_width=4).set_points_as_corners(
        np.column_stack([xs, cy - .1 + y, np.zeros_like(xs)]))


def card2_tiles(cx=CARD_X[1], states=None):
    states = states or ["dim"] * 6
    return VGroup(*[tile(cx + px, py, .8, st) for (px, py), st in zip(TILE_POS, states)])


def card3_graphic(cx=CARD_X[2], cy=CARD_Y, fr=TICK_F):
    base = Line([cx - 1.5, cy - .4, 0], [cx + 1.5, cy - .4, 0], color=GREY, stroke_width=3)
    ticks = VGroup(*[Line([cx - 1.5 + f * 3, cy - .4, 0], [cx - 1.5 + f * 3, cy + .15, 0], color=TEAL, stroke_width=5)
                     for f in fr])
    return base, ticks


def sym(ch, x):
    return T(ch, 44, TEXT).move_to([x, CARD_Y, 0])


# ---------------------------------------------------------------------------------------------
# predict frame (s11, s12)
# ---------------------------------------------------------------------------------------------
def predict_parts():
    title = T("Predict", 44, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
    box1 = RoundedRectangle(corner_radius=.2, width=5.4, height=5.0, stroke_color=GREY, stroke_width=2.5).move_to([-3.1, -.45, 0])
    tiles = VGroup(*[tile(-3.1 + dx, y, 1.4, "plain") for y in (1.2, .1, -1.0) for dx in (-1.4, 0, 1.4)])
    lab1 = T("more synapses", 30, TEXT).move_to([-3.1, -2.35, 0])
    card1 = VGroup(box1, tiles, lab1)
    box2 = RoundedRectangle(corner_radius=.2, width=5.4, height=5.0, stroke_color=GREY, stroke_width=2.5).move_to([3.1, -.45, 0])
    bouton, ves, post = big_synapse(3.1, -.45, w=3.8, hb=1.3, gap=.95, nves=5)
    rec = VGroup(*[receptor(x, -.45, ORANGE) for x in (2.0, 3.1, 4.2)])
    rng = np.random.default_rng(4)
    dots = VGroup(*[Dot([2.0 + 2.2 * (i % 5) / 4 + rng.uniform(-.1, .1), .05 + .35 * (i // 5), 0], radius=.07, color=TEAL)
                    for i in range(10)])
    lab2 = T("more release\nfrom each one", 30, TEXT, line_spacing=.8).move_to([3.1, -2.35, 0])
    card2 = VGroup(box2, bouton, ves, post, rec, dots, lab2)
    return title, card1, card2, T("or", 30, GREY).move_to([0, -.45, 0])


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Synapses in the Brain: Adhesion, Scaffolds and Astrocytes"
    TITLE = "Astrocytes Build and Switch On"


class S01Q(SpokenScene):
    def construct(self):
        d, ns = stage_dish()
        dl = cap("purified neurons", DX, 3.05, 24)
        box, lab = panel("recorded current")
        tr = trace_mob(mini_vals(BASE_EV))
        qbox = DashedVMobject(RoundedRectangle(corner_radius=.25, width=2.8, height=2.4, stroke_color=GREY, stroke_width=3),
                              num_dashes=40).move_to([4.2, 1.9, 0])
        q = T("?", 120, TEXT, font=TITLE_FONT).move_to([4.2, 1.9, 0])
        self.at("purified neurons")
        self.play(FadeIn(d), FadeIn(ns), FadeIn(dl), run_time=.8)
        self.at("fire")
        self.play(fire(ns), run_time=1.0)
        self.at("barely talk")
        self.play(FadeIn(box), FadeIn(lab), run_time=.4)
        self.play(Create(tr, rate_func=linear), run_time=1.8)
        self.at("what are they missing")
        self.play(FadeIn(qbox), FadeIn(q, scale=.6), run_time=.6)
        self.finish()


class S02Purify(SpokenScene):
    def construct(self):
        cx = [-4.4, 0.0, 4.4]
        cy = -.2
        boxes = [RoundedRectangle(corner_radius=.2, width=4.0, height=4.6, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=.07).move_to([x, cy, 0]) for x in cx]
        t1 = cap("mixed cells", cx[0], 2.4, 26)
        t2 = cap("antibody-coated dish", cx[1], 2.4, 24)
        t3 = cap("retinal ganglion cells", cx[2], 2.4, 24, TEXT)
        by = cy - 2.05
        bar = Rectangle(width=3.4, height=.18, stroke_width=0, fill_color=GREY, fill_opacity=.7).move_to([cx[1], by, 0])
        ticks = VGroup(*[Line([cx[1] - 1.5 + i * .5, by + .1, 0], [cx[1] - 1.5 + i * .5, by + .3, 0], color=GREY, stroke_width=3)
                         for i in range(7)])
        chp = chip("immunopanning", TEAL, 28).move_to([0, -3.3, 0])

        def rgc(p):
            return Circle(.24, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.4).move_to([*p, 0])

        def glia(p):
            return glia_glyph(p[0], p[1], .2)
        # legend: what each shape is
        lg1 = VGroup(Circle(.14, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.4),
                     T("ganglion cell", 24, GREY)).arrange(RIGHT, buff=.15).move_to([-5.2, -3.3, 0])
        lg2 = VGroup(glia_glyph(0, 0, .2), T("glia", 24, TEXT)).arrange(RIGHT, buff=.15).move_to([-5.2, -3.3, 0])
        lg2.next_to(lg1, RIGHT, buff=.3)
        rp = [(-1.0, 1.0), (.8, .4), (-.5, -.7), (1.0, -1.3)]
        gp = [(.2, 1.5), (-1.1, -.1), (.9, -.5), (-.1, -1.5)]
        rg = VGroup(*[rgc((cx[0] + a, cy + b)) for a, b in rp])
        gl = VGroup(*[glia((cx[0] + a, cy + b)) for a, b in gp])
        self.play(FadeIn(boxes[0]), FadeIn(t1), FadeIn(rg), FadeIn(gl), FadeIn(lg1), FadeIn(lg2), run_time=.8)
        self.at("purified")
        self.play(FadeIn(chp), FadeIn(boxes[1]), FadeIn(t2), FadeIn(bar), FadeIn(ticks), run_time=.4)
        tops_r = [(-.9, .9), (.8, .5), (-.3, -.1), (.9, -.7)]
        tops_g = [(.2, 1.5), (-1.1, .7), (.7, -.2), (-.6, -.9)]
        self.play(*[m.animate.move_to([cx[1] + a, cy + b, 0]) for m, (a, b) in zip(rg, tops_r)],
                  *[m.animate.move_to([cx[1] + a, cy + b, 0]) for m, (a, b) in zip(gl, tops_g)], run_time=.9)
        self.at("retinal ganglion cells")
        self.play(*[m.animate.move_to([cx[1] - 1.2 + i * .8, by + .5, 0]) for i, m in enumerate(gl)],
                  FadeIn(boxes[2]), FadeIn(t3), run_time=.8)
        self.play(*[m.animate.move_to([cx[2] + a, cy + b, 0]) for m, (a, b) in
                    zip(rg, [(-.9, .6), (.8, .9), (-.6, -.5), (.7, -.7)])], run_time=1.2)
        self.at("almost no glia")
        gtag = cap("glia stay on the dish", cx[1], by + 1.15, 24, TEXT)
        self.play(FadeIn(gtag), Indicate(gl, color=TEXT), run_time=.7)
        self.finish()


# (scene id s03_1997 maps to the CamelCase class name S031997)
class S031997(SpokenScene):
    def construct(self):
        d, ns = stage_dish()
        VGroup(d, ns).scale(1.1, about_point=[DX, DY, 0])
        box, lab = panel("recorded voltage", bar="20 ms", bar_len=12.2 * 20 / 145)
        cr = chip("Pfrieger and Barres\n1997", GREY, 26).move_to([4.3, 1.7, 0])
        rest = Line([PX0 + .3, HH_BASE, 0], [PX1 - .3, HH_BASE, 0], color=YELLOW, stroke_width=3.5)
        tr = hh_trace()
        self.add(d, ns, box, lab, rest)
        self.at("in 1997")
        self.play(FadeIn(cr, shift=UP * .1), run_time=.5)
        self.at("these neurons fired")
        self.play(fire(ns), run_time=1.0)
        self.at("fired action potentials")
        self.play(Create(tr, rate_func=linear), run_time=2.2)
        self.remove(rest)
        self.finish()


class S04Little(SpokenScene):
    def construct(self):
        d, ns = stage_dish()
        VGroup(d, ns).scale(1.1, about_point=[DX, DY, 0])
        box, lab = panel("recorded voltage", bar="20 ms", bar_len=12.2 * 20 / 145)
        old = hh_trace()
        self.add(d, ns, box, lab, old)
        box2, lab2 = panel("recorded current")
        tr = trace_mob(mini_vals(BASE_EV))
        self.at("synaptic activity")
        self.play(FadeOut(old), FadeOut(lab), run_time=.3)
        self.play(FadeIn(lab2), Create(tr, rate_func=linear), run_time=1.4)
        self.finish()


class S05Scope(SpokenScene):
    def construct(self):
        head = T("Astrocytes add to synapse formation", 34, TEXT, font=TITLE_FONT).move_to([0, 3.3, 0])
        fl = RoundedRectangle(corner_radius=.2, width=5.8, height=5.2, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.05).move_to([-3.3, -.2, 0])
        fr = RoundedRectangle(corner_radius=.2, width=5.8, height=5.2, stroke_color=TEXT, stroke_width=3,
                              fill_color=TEXT, fill_opacity=.05).move_to([3.3, -.2, 0])
        tl = cap("neurons alone", -3.3, 1.95, 30, GREY)
        tr_ = cap("added by astrocytes", 3.3, 1.95, 30, TEXT)
        gp = [(-3.3 + dx, y) for y in (.65, -.95) for dx in (-1.05, 1.05)]
        grey = VGroup(*[tile(x, y, 2.1, "plain") for x, y in gp])
        wp = [(3.3 + dx, y) for y, dxs in ((.65, (-1.85, 0, 1.85)), (-.95, (-.95, .95))) for dx in dxs]
        white = VGroup(*[tile(x, y, 2.1, "astro") for x, y in wp])
        self.play(FadeIn(head), run_time=.25)
        self.play(FadeIn(fl), FadeIn(fr), FadeIn(tl), FadeIn(tr_), run_time=.5)
        self.at("not the only source")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in grey], lag_ratio=.15), run_time=.9)
        self.at("only source")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in white], lag_ratio=.1), run_time=.9)
        self.at("neurons form some synapses")
        self.play(Indicate(grey, color=TEXT, scale_factor=1.05), run_time=.8)
        self.finish()


class S06Mini(SpokenScene):
    def construct(self):
        cx, py = -2.4, -.55
        bouton, _, post = big_synapse(cx, py, w=7.4, hb=2.9, gap=.95, nves=1)
        bb = py + .95
        vp = [(-2.7, .6), (-.9, .6), (.9, .6), (2.7, .6), (-1.8, 1.7), (0, 1.7), (1.8, 1.7)]
        ves = VGroup(*[Dot([cx + a, bb + b, 0], radius=.26, color=TEAL) for a, b in vp])
        rec = VGroup(*[receptor(x, py, ORANGE, s=1.4) for x in (cx - 1.8, cx - .9, cx, cx + .9, cx + 1.8)])
        box, lab = panel("recorded current", cy=-2.75, h=1.9)
        flat = trace_mob(mini_vals([]) * .55, -2.55)
        full = trace_mob(mini_vals(BASE_EV) * .55, -2.55)
        self.play(FadeIn(bouton), FadeIn(ves), FadeIn(post), FadeIn(rec), run_time=.35)
        self.at("readout")
        self.play(FadeIn(box), FadeIn(lab), FadeIn(flat), run_time=.35)
        v = ves[1]
        self.at("one vesicle")
        self.play(Indicate(v, color=YELLOW, scale_factor=1.6), run_time=.5)
        self.at("released")
        mouth = [cx - .9, bb + .02, 0]
        self.play(v.animate.move_to(mouth), run_time=.2)
        tr = [Dot(mouth, radius=.14, color=TEAL) for _ in range(5)]
        self.remove(v)
        self.add(*tr)
        self.play(*[m.animate.move_to([cx - 1.8 + i * .9, py + .32, 0]) for i, m in enumerate(tr)], run_time=.4)
        self.at("on its own")
        chp = chip("one vesicle, one mini", TEAL, 28).move_to([4.4, 1.6, 0])
        self.play(Transform(flat, full), FadeIn(chp), run_time=.7)
        self.finish()


class S07Ttx(SpokenScene):
    def construct(self):
        SC = 1.4
        d, ns = stage_dish()
        box, lab = panel("recording")
        mini_ev, spk_t, base_v, full = s07_series()
        base = PY_C - .05
        tr = trace_mob(full * SC, base)
        flat = trace_mob(base_v * SC, base)
        ov = VMobject(stroke_color=YELLOW, stroke_width=4)
        for t0 in spk_t:
            idx = np.where((tt >= t0 - .01) & (tt <= t0 + SPIKE_W))[0]
            pts = to_xy(full * SC, base)[idx]
            ov.start_new_path(pts[0])
            ov.add_points_as_corners(pts[1:])
        ap = cap("action potentials", 4.2, 2.35, 28, YELLOW)
        ttx = chip("tetrodotoxin", RED, 28).move_to([4.2, 3.25, 0])
        strike = Line(ap.get_left() + LEFT * .05, ap.get_right() + RIGHT * .05, color=RED, stroke_width=4)
        pk = .0241
        def trough(t0):
            idx = np.where((tt >= t0) & (tt <= t0 + .12))[0]
            j = idx[int(np.argmin(base_v[idx]))]
            return [tx(tt[j]), base + SC * base_v[j], 0]
        rings = VGroup(*[Circle(.42, stroke_color=TEAL, stroke_width=4).move_to(trough(t)) for t, a in mini_ev])
        dep = cap("depends on the synapses", 4.2, 2.35, 28, TEAL)
        notbusy = T("not on how busy\nthe neurons are", 30, TEXT, line_spacing=.8).move_to([4.2, 1.3, 0])
        self.play(FadeIn(d), FadeIn(ns), FadeIn(box), FadeIn(lab), FadeIn(tr), FadeIn(ov), FadeIn(ap), run_time=.5)
        self.at("tetrodotoxin")
        self.play(FadeIn(ttx, shift=DOWN * .1), run_time=.4)
        self.at("blocks action potentials")
        self.play(Transform(tr, flat), FadeOut(ov), Create(strike), ns.animate.set_opacity(.35), run_time=.9)
        self.at("what remains")
        self.play(Create(rings), run_time=.8)
        self.at("depends on the synapses")
        self.play(FadeOut(ap), FadeOut(strike), run_time=.25)
        self.play(FadeIn(dep), Indicate(rings, color=TEAL), run_time=.6)
        self.at("not on how busy")
        self.play(FadeIn(notbusy), run_time=.5)
        self.finish()


class S08Formula(SpokenScene):
    def construct(self):
        tag = chip("firing blocked", RED, 24, pad=.1).move_to([-4.6, 3.45, 0])
        b1, b2, b3 = card_box(CARD_X[0]), card_box(CARD_X[1]), card_box(CARD_X[2])
        t1 = card_title("mini frequency", CARD_X[0])
        t2 = card_title("synapses giving\ndetectable minis", CARD_X[1])
        t3 = card_title("average\nrelease rate", CARD_X[2])
        g1 = card1_graphic()
        g2 = card2_tiles()
        base3, ticks3 = card3_graphic()
        approx, times = sym("≈", -2.275), sym("×", 2.275)
        # bottom panel: mini size
        bp = RoundedRectangle(corner_radius=.18, width=12.6, height=3.3, stroke_color=GREY, stroke_width=2.5,
                              fill_color=BG, fill_opacity=1).move_to([0, -1.85, 0])
        big_base = Line([-6.0, -1.1, 0], [-3.0, -1.1, 0], color=BLUE, stroke_width=4)
        xs = np.linspace(-6.0, -3.0, 160)
        s = np.clip(xs + 5.0, 0, None)
        k = np.exp(-s / .35) - np.exp(-s / .07); k = k / k.max()
        blip = VMobject(stroke_color=BLUE, stroke_width=5).set_points_as_corners(
            np.column_stack([xs, -1.1 - 1.9 * np.where(xs >= -5.0, k, 0), np.zeros(160)]))
        szl = cap("mini size", -4.6, -.55, 26, TEXT)
        mem = membrane(-2.85, -1.6, 1.6)
        recs = VGroup(*[receptor(x, -2.85, ORANGE) for x in (-.8, 0, .8)])
        rl = T("receptors facing the vesicle", 24, ORANGE).move_to([1.7 + 2.3, -2.55, 0]).align_to([1.9, 0, 0], LEFT)
        ves = Circle(.42, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=.12).move_to([0, -1.25, 0])
        tdots = VGroup(*[Dot([dx, -1.25 + dy, 0], radius=.08, color=TEAL) for dx, dy in
                         [(-.15, .12), (.15, .12), (0, -.05), (-.17, -.17), (.17, -.17)]])
        vl = T("transmitter inside it", 24, TEAL).move_to([1.7 + 1.6, -1.25, 0]).align_to([.75, 0, 0], LEFT)
        self.at("with firing blocked")
        self.play(FadeIn(tag), run_time=.4)
        self.at("mini frequency")
        self.play(FadeIn(b1), FadeIn(t1), run_time=.4)
        self.play(Create(g1), run_time=.9)
        self.at("roughly")
        self.play(FadeIn(approx), run_time=.3)
        self.at("the number of synapses")
        self.play(FadeIn(b2), FadeIn(t2), FadeIn(g2), run_time=.6)
        self.at("giving detectable minis")
        self.play(*[Transform(g2[i], tile(CARD_X[1] + TILE_POS[i][0], TILE_POS[i][1], .8, "active")) for i in LIT],
                  run_time=.8)
        self.at("times")
        self.play(FadeIn(times), run_time=.3)
        self.at("average release rate")
        self.play(FadeIn(b3), FadeIn(t3), FadeIn(base3), run_time=.5)
        self.play(LaggedStart(*[Create(t) for t in ticks3], lag_ratio=.25), run_time=.9)
        self.at("mini size")
        self.play(FadeIn(bp), Create(big_base), run_time=.4)
        self.play(Create(blip), FadeIn(szl), run_time=.8)
        self.at("receptors facing")
        self.play(FadeIn(mem), FadeIn(recs), FadeIn(rl), run_time=.6)
        self.at("the vesicle")
        self.play(FadeIn(ves), run_time=.4)
        self.at("transmitter inside")
        self.play(FadeIn(tdots), FadeIn(vl), run_time=.6)
        self.finish()


class S09Glia(SpokenScene):
    def construct(self):
        d, ns = stage_dish()
        box, lab = panel("recorded current")
        tr = trace_mob(mini_vals(BASE_EV))
        self.add(d, ns, box, lab, tr)
        layer = glia_layer().move_to([DX, 4.8, 0])
        gl = cap("layer of glia", 4.2, 3.25, 28, TEXT)
        gap = DoubleArrow([DX, 2.45, 0], [DX, 2.85, 0], buff=0, color=GREY, stroke_width=4, tip_length=.12)
        nt = cap("does not touch the neurons", 4.2, 2.6, 26, GREY)
        self.at("layer of glia")
        self.play(layer.animate.move_to([DX, 3.25, 0]), FadeIn(gl), run_time=1.1)
        self.at("does not touch")
        self.play(GrowFromCenter(gap), FadeIn(nt), run_time=.6)
        self.finish()


def glia_layer():
    band = RoundedRectangle(corner_radius=.2, width=7.6, height=.8, stroke_color=TEXT, stroke_width=3,
                            fill_color=TEXT, fill_opacity=.08)
    cells = VGroup(*[glia_glyph(x, 0, .24) for x in (-3.3, -2.0, -.7, .6, 1.9, 3.2)])
    return VGroup(band, cells).move_to([DX, 3.25, 0])


class S10Rise(SpokenScene):
    def construct(self):
        SC = .65
        d, ns = stage_dish()
        box, lab = panel("recorded current")
        old = trace_mob(mini_vals(BASE_EV) * SC, -.75)
        l_old = cap("without glia", -5.0, -.4, 24, GREY)
        layer = glia_layer()
        gl = cap("layer of glia", 4.2, 3.25, 28, TEXT)
        new = trace_mob(mini_vals(GLIA_EV) * SC, -2.0)
        l_new = cap("with glia", -5.4, -1.45, 24, TEXT)
        mf = cap("mini frequency", 4.2, 2.8, 28, GREY)
        big = M("12×", 64, BLUE).move_to([4.2, 1.95, 0])
        surv = chip("survival unchanged", TEXT, 26).move_to([4.2, 1.0, 0])
        self.add(d, ns, layer, gl, box, lab, old, l_old)
        self.play(FadeIn(mf), run_time=.4)
        self.at("rose")
        self.play(FadeIn(l_new), Create(new, rate_func=linear, run_time=1.5), Succession(Wait(.55), FadeIn(big, scale=.7, run_time=.4)))
        self.at("did not change")
        self.play(FadeIn(surv), run_time=.5)
        self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        title, c1, c2, orr = predict_parts()
        self.play(FadeIn(title), run_time=.4)
        self.at("more synapses")
        self.play(FadeIn(c1[0]), FadeIn(c1[2]), LaggedStart(*[GrowFromCenter(t) for t in c1[1]], lag_ratio=.05), run_time=.7)
        self.at("or more release")
        self.play(FadeIn(orr), run_time=.3)
        self.at("release from each one")
        self.play(FadeIn(c2), run_time=.8)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        title, c1, c2, orr = predict_parts()
        self.add(title, c1, c2, orr)
        self.finish()


class S13Cant(SpokenScene):
    def construct(self):
        b1, b2, b3 = card_box(CARD_X[0]), card_box(CARD_X[1]), card_box(CARD_X[2])
        t1 = card_title("mini frequency", CARD_X[0])
        t2 = card_title("synapses giving\ndetectable minis", CARD_X[1])
        t3 = card_title("average\nrelease rate", CARD_X[2])
        g1 = card1_graphic()
        g2 = card2_tiles(states=["active"] * 4 + ["dim"] * 2)
        base3, ticks3 = card3_graphic()
        approx, times = sym("≈", -2.275), sym("×", 2.275)
        tag = chip("firing blocked", RED, 24, pad=.1).move_to([-4.6, 3.45, 0])
        box, lab = panel("recorded current", cy=-1.95, h=3.0)
        busy = trace_mob(mini_vals(GLIA_EV) * .6, -2.0, w=4)
        self.add(tag, b1, t1, g1, b2, t2, g2, b3, t3, base3, ticks3, approx, times)
        self.at("mini frequency")
        self.play(FadeIn(box), FadeIn(lab), Create(busy, rate_func=linear), run_time=.9)
        self.at("more minis")
        self.play(Circumscribe(b1, color=BLUE, stroke_width=6, fade_out=True), run_time=.9)
        self.at("more synapses")
        new = [tile(CARD_X[1] + px, CARD_Y - 1.1, .8, "active") for px in (-1.05, 0, 1.05)]
        self.play(Circumscribe(b2, color=TEXT, stroke_width=6, fade_out=True),
                  LaggedStart(*[GrowFromCenter(t) for t in new], lag_ratio=.2), run_time=.9)
        self.at("more release")
        more = VGroup(*[Line([CARD_X[2] - 1.5 + f * 3, CARD_Y - .4, 0], [CARD_X[2] - 1.5 + f * 3, CARD_Y + .15, 0],
                             color=TEAL, stroke_width=5) for f in TICK_F2])
        self.play(Circumscribe(b3, color=TEAL, stroke_width=6, fade_out=True),
                  LaggedStart(*[Create(t) for t in more], lag_ratio=.15), run_time=.9)
        self.at("synapses that start responding")
        self.play(Circumscribe(g2[4:], color=GREEN, stroke_width=6, fade_out=True),
                  *[Transform(g2[i], tile(CARD_X[1] + TILE_POS[i][0], TILE_POS[i][1], .8, "active")) for i in (4, 5)],
                  run_time=1.0)
        self.finish()


class S14Count(SpokenScene):
    def construct(self):
        cr = cap("Pfrieger and Barres, 1997", 0, 3.5, 26, GREY)
        fl = RoundedRectangle(corner_radius=.2, width=5.6, height=3.6, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.07).move_to([-3.3, .75, 0])
        fr = RoundedRectangle(corner_radius=.2, width=5.6, height=3.6, stroke_color=TEXT, stroke_width=3,
                              fill_color=TEXT, fill_opacity=.05).move_to([3.3, .75, 0])
        tl = cap("without glia", -3.3, 2.95, 28, GREY)
        tr_ = cap("with glia", 3.3, 2.95, 28, TEXT)
        grid = [(dx, .75 + dy) for dy in (1.05 - .1, -.05, -1.15) for dx in (-1.7, 0, 1.7)]
        lt = VGroup(*[tile(-3.3 + dx, y, 1.9, "plain") for dx, y in grid[:4]])
        rt = VGroup(*[tile(3.3 + dx, y, 1.9, "astro" if i >= 4 else "plain") for i, (dx, y) in enumerate(grid)])
        em = chip("electron microscopy", TEAL, 28).move_to([0, -1.75, 0])
        n23 = M("2.3×", 60, TEXT)
        more = T("more synapses with glia", 32, TEXT)
        res = VGroup(n23, more).arrange(RIGHT, buff=.4).move_to([0, -2.9, 0])
        self.play(FadeIn(fl), FadeIn(tl), FadeIn(fr), FadeIn(tr_), run_time=.5)
        self.at("also counted")
        self.play(FadeIn(cr), run_time=.4)
        self.at("counted synapses")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in lt], lag_ratio=.2), run_time=1.0)
        self.at("electron microscopy")
        self.play(FadeIn(em), run_time=.5)
        self.at("raised the count")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in rt], lag_ratio=.08), run_time=1.0)
        self.at("only about")
        self.play(FadeIn(res, shift=UP * .15), run_time=.6)
        self.finish()


class S15Split(SpokenScene):
    def construct(self):
        head = cap("same share of synapses giving detectable minis", 0, 3.4, 28, TEXT)
        W0, W1 = 2.4, 5.52
        lb = Rectangle(width=W0, height=1.2, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([-5.1, 1.9, 0])
        rb = Rectangle(width=W1, height=1.2, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([-.84, 1.9, 0])
        lsh = Rectangle(width=W0 * .4, height=1.2, stroke_width=0, fill_color=GREEN, fill_opacity=.7).align_to(lb, LEFT).align_to(lb, UP)
        rsh = Rectangle(width=W1 * .4, height=1.2, stroke_width=0, fill_color=GREEN, fill_opacity=.7).align_to(rb, LEFT).align_to(rb, UP)
        ll = cap("without glia", -5.1, 2.85, 26, GREY)
        rl = cap("with glia", -.84, 2.85, 26, TEXT)
        leg = VGroup(
            T("bar length = synapses", 24, TEXT),
            VGroup(Square(.3, stroke_width=0, fill_color=GREEN, fill_opacity=.7), T("give detectable minis", 24, GREEN)).arrange(RIGHT, buff=.15),
        ).arrange(DOWN, buff=.2, aligned_edge=LEFT).move_to([4.6, 1.9, 0])
        e12 = M("12×", 64, BLUE).move_to([-4.2, -.3, 0])
        d_ = T("÷", 50, TEXT).move_to([-2.1, -.3, 0])
        e23 = M("2.3×", 64, TEXT).move_to([0, -.3, 0])
        ap = T("≈", 50, TEXT).move_to([2.1, -.3, 0])
        e5 = M("5×", 64, TEAL).move_to([4.2, -.3, 0])
        c12 = cap("more minis", -4.2, -1.05, 26, GREY)
        c23 = cap("more synapses", 0, -1.05, 26, GREY)
        c5 = cap("more release per synapse", 4.2, -1.05, 24, GREY)
        chp = chip("the 1997 paper read it as: more effective synapses", TEXT, 28, pad=.12).move_to([0, -1.85, 0])
        note = chip("but minis also got larger, so some extra events\nmay simply have become detectable", TEXT, 28, pad=.12).next_to(chp, DOWN, buff=.32)
        self.at("same share")
        self.play(FadeIn(head), FadeIn(lb), FadeIn(rb), FadeIn(ll), FadeIn(rl), FadeIn(leg), run_time=.7)
        self.at("gave detectable minis")
        self.play(FadeIn(lsh), FadeIn(rsh), run_time=.7)
        self.at("each would release")
        self.play(FadeIn(e12), FadeIn(c12), FadeIn(d_), FadeIn(e23), FadeIn(c23), run_time=.8)
        self.at("five times")
        self.play(FadeIn(ap), FadeIn(e5, scale=.7), FadeIn(c5), run_time=.6)
        self.at("the paper read")
        self.play(FadeIn(chp, shift=UP * .1), FadeIn(note, shift=UP * .1), run_time=.6)
        self.finish()


class S15bLater(SpokenScene):
    def construct(self):
        base_y, unit = -2.4, .42
        xa0, xa1 = -6.4, -.3
        axis = Line([xa0, base_y, 0], [xa1, base_y, 0], color=GREY, stroke_width=3)
        one = DashedLine([xa0, base_y + unit, 0], [xa1, base_y + unit, 0], color=GREY, stroke_width=3)
        one_l = T("1× = without glia", 24, GREY).move_to([xa1 + .15, base_y + unit + .28, 0], aligned_edge=LEFT)
        title = T("synapses, with glia vs without", 26, TEXT).move_to([-3.35, 3.4, 0])

        def bar(x, mult):
            return Rectangle(width=1.7, height=unit * mult, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                             fill_opacity=.35).move_to([x, base_y + unit * mult / 2, 0])
        x97, x01 = -5.0, -1.9
        b97, b01 = bar(x97, 2.3), bar(x01, 7)
        n97 = M("2.3×", 40, TEXT).move_to([x97, base_y + unit * 2.3 + .4, 0])
        n01 = M("7×", 48, TEXT).move_to([x01, base_y + unit * 7 + .45, 0])
        l97 = T("1997\nPfrieger\nand Barres", 22, GREY, line_spacing=.8).move_to([x97, -3.15, 0])
        l01 = T("2001\nUllian and\ncolleagues", 22, GREY, line_spacing=.8).move_to([x01, -3.15, 0])
        cred = chip("Ullian and colleagues, 2001", TEXT, 26).move_to([4.3, 3.1, 0])
        own = cap("in their own cultures", 4.3, 2.3, 28, TEXT)
        fm = T("far more than\nthe 1997 count", 28, YELLOW, line_spacing=.8).move_to([4.3, 1.35, 0])
        gapar = DoubleArrow([-.8, base_y + unit * 2.3, 0], [-.8, base_y + unit * 7, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=.15)
        # neutral slider: moves both ways, no numbers
        sx0, sx1, sy = 2.2, 6.4, -.05
        track = Line([sx0, sy, 0], [sx1, sy, 0], color=GREY, stroke_width=5)
        handle = Dot([(sx0 + sx1) / 2, sy, 0], radius=.22, color=TEXT)
        ln = T("mostly\nnumber", 26, TEXT, line_spacing=.8).move_to([sx0 + .4, sy - .85, 0])
        le = T("mostly\nefficacy", 26, GREEN, line_spacing=.8).move_to([sx1 - .4, sy - .85, 0])
        dep = chip("depends on the culture", TEXT, 28).move_to([4.3, -2.8, 0])
        self.add(axis, one, one_l, title)
        self.play(FadeIn(l97), GrowFromEdge(b97, DOWN), FadeIn(n97), run_time=.6)
        self.at("in 2001")
        self.play(FadeIn(l01), run_time=.3)
        self.at("and colleagues")
        self.play(FadeIn(cred), run_time=.4)
        self.at("seven fold")
        self.play(GrowFromEdge(b01, DOWN), FadeIn(n01), run_time=1.0)
        self.at("in their own cultures")
        self.play(FadeIn(own), run_time=.4)
        self.at("far more")
        self.play(GrowFromCenter(gapar), FadeIn(fm), run_time=.4)
        self.at("the 1997 count")
        self.play(Indicate(b97, color=YELLOW, scale_factor=1.08), run_time=.8)
        self.at("how much is number")
        self.play(FadeIn(track), FadeIn(handle), FadeIn(ln), FadeIn(le), run_time=.5)
        self.play(handle.animate.move_to([sx0 + .5, sy, 0]), run_time=.7)
        self.at("how much is efficacy")
        self.play(handle.animate.move_to([sx1 - .5, sy, 0]), run_time=1.0)
        self.at("depends on the culture")
        self.play(FadeIn(dep), handle.animate.move_to([(sx0 + sx1) / 2 - .6, sy, 0]), run_time=1.0)
        self.finish()


class Divider(NarratedScene):
    TEXT_LINE = ""

    def construct(self):
        t = T(self.TEXT_LINE, 40, TEXT, font=TITLE_FONT)
        fit(t, max_w=11.5)
        r = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4).next_to(t, DOWN, buff=.35)
        g = VGroup(t, r).move_to([0, 0, 0])
        self.play(FadeIn(g, shift=UP * .1), run_time=.6)
        self.finish()


class S16Beat(Divider):
    TEXT_LINE = "Which astrocyte signals?"


class S17Tsp(SpokenScene):
    def construct(self):
        a = astro(-4.3, .4, 1.8)
        al = cap("astrocyte", -4.3, -2.5, 28, TEXT)
        nbox = RoundedRectangle(corner_radius=.2, width=6.4, height=4.8, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=.07).move_to([3.0, 0, 0])
        nl = cap("neurons", 3.0, -2.05, 28, GREY)
        cr = cap("Christopherson and colleagues, 2005", 0, -3.4, 24, GREY)
        chp = chip("thrombospondins", TEXT, 28).move_to([0, 3.2, 0])
        nrs = VGroup(*[neuron(3.0 + dx, 1.65, r=.3) for dx in (-1.7, 0, 1.7)])
        tiles = VGroup(*[tile(3.0 + dx, y, 1.5, "plain") for y in (.3, -.9) for dx in (-1.7, 0, 1.7)])
        # dots leave the astrocyte tips (right-hand arms) and cross into the neurons box
        tips = [(-4.3 + 1.8 * (.5 + .76 * np.cos(np.radians(ang))) * 1.0 + .0, .4 + 1.8 * (.5 + .76 * np.sin(np.radians(ang))))
                for ang in (22, 67, 112 - 45 * 0 - 45, -23, -68)]
        tips = [(-4.3 + 1.8 * (.5 + .76) * np.cos(np.radians(ang)) * (1 if i % 2 == 0 else .8),
                 .4 + 1.8 * (.5 + .76) * np.sin(np.radians(ang)) * (1 if i % 2 == 0 else .8))
                for i, ang in enumerate((22, 67, -23, -68, 0))]
        dots = VGroup(*[Dot([x, y, 0], radius=.12, color=TEXT) for x, y in tips])
        dst = [(.9, .9), (1.8, 1.7), (1.4, -.2), (2.2, .3), (1.2, .5)]
        self.play(FadeIn(a), FadeIn(al), FadeIn(nbox), FadeIn(nl), FadeIn(cr), FadeIn(nrs), run_time=.7)
        self.at("identified")
        self.play(FadeIn(chp, shift=DOWN * .1), run_time=.5)
        self.at("astrocyte proteins")
        self.add(dots)
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dots, dst)], run_time=1.3)
        self.play(*[d.animate.shift(RIGHT * .8) for d in dots], run_time=.5)
        self.at("induce synapses")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in tiles], lag_ratio=.1), FadeOut(dots), run_time=1.0)
        self.finish()


def three_columns():
    cx = [-4.4, 0, 4.4]
    frames = [RoundedRectangle(corner_radius=.2, width=4.0, height=5.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=.05).move_to([x, .35, 0]) for x in cx]
    words = [T("There", 32, TEXT).move_to([cx[0], 1.75, 0]), T("Releases", 32, TEXT).move_to([cx[1], 1.75, 0]),
             T("Responds", 32, TEXT).move_to([cx[2], 1.75, 0])]
    lamps = [lamp(cx[0], 2.55, True), lamp(cx[1], 2.55, True), lamp(cx[2], 2.55, False)]
    ic1 = tile(cx[0], .3, 2.4, "plain")
    bt, vs, ps = big_synapse(cx[1], -.45, w=2.8, hb=.9, gap=.6, nves=3)
    td = VGroup(*[Dot([cx[1] - .6 + .4 * i, -.2 + (.06 if i % 2 else -.04), 0], radius=.07, color=TEAL) for i in range(4)])
    ic2 = VGroup(bt, vs, ps, td)
    # empty AMPA slot: a gap in the membrane with a dashed cup in it (nothing cuts across the bar)
    ml = membrane(-.1, cx[2] - 1.4, cx[2] - .45)
    mr = membrane(-.1, cx[2] + .45, cx[2] + 1.4)
    slot = receptor(cx[2], -.1, ORANGE, s=1.1, dashed=True)
    flat = Line([cx[2] - 1.3, -1.05, 0], [cx[2] + 1.3, -1.05, 0], color=GREY, stroke_width=4)
    cur = T("current", 22, GREY).move_to([cx[2], -.8, 0])
    ic3 = VGroup(ml, mr, slot, flat, cur)
    d1 = T("looked normal by\nelectron microscopy", 24, TEXT, line_spacing=.8).move_to([cx[0], -1.95, 0])
    d2 = T("released\ntransmitter", 24, TEAL, line_spacing=.8).move_to([cx[1], -1.95, 0])
    d3 = T("no AMPA receptor\nresponse near rest", 24, RED, line_spacing=.8).move_to([cx[2], -1.95, 0])
    return frames, words, lamps, [ic1, ic2, ic3], [d1, d2, d3]


class S18Tsp2(SpokenScene):
    def construct(self):
        frames, words, lamps, icons, descs = three_columns()
        cr = cap("Christopherson and colleagues, 2005", 0, -3.45, 24, GREY)
        self.add(cr)
        self.at("looked normal")
        self.play(FadeIn(frames[0]), FadeIn(words[0]), FadeIn(icons[0]), FadeIn(descs[0]), run_time=.6)
        self.play(FadeIn(lamps[0]), run_time=.4)
        self.at("released transmitter")
        self.play(FadeIn(frames[1]), FadeIn(words[1]), FadeIn(icons[1]), FadeIn(descs[1]), run_time=.6)
        self.play(FadeIn(lamps[1]), run_time=.4)
        self.at("yet they")
        self.play(FadeIn(frames[2]), FadeIn(words[2]), FadeIn(icons[2]), FadeIn(lamps[2]), run_time=.7)
        self.at("no AMPA receptor responses")
        self.play(FadeIn(descs[2], shift=UP * .1), run_time=.6)
        self.finish()


class S19Silent(SpokenScene):
    def construct(self):
        cx, py = 0, .55
        bouton, ves, post = big_synapse(cx, py, w=8.4, hb=1.7, gap=1.05, nves=7)
        for i, v in enumerate(ves):
            v.move_to([-3.3 + i * 1.1, py + 1.05 + .4 + (.3 if i % 2 else 0), 0])
        slotA = receptor(-2.4, py, ORANGE, s=1.7, dashed=True)
        labA = T("AMPA", 30, ORANGE).move_to([-2.4, -.45, 0])
        subA = T("no working receptors", 26, ORANGE).move_to([-2.4, -1.05, 0])
        nmda = DashedVMobject(receptor(2.4, py, PURPLE, s=1.7), num_dashes=14).set_stroke(opacity=.55)
        qm = T("?", 44, PURPLE).move_to([3.15, py - .1, 0])
        labN = T("NMDA", 30, PURPLE).move_to([2.4, -.45, 0])
        mg = VGroup(Circle(.27, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.4),
                    T("Mg", 22, TEXT)).move_to([2.4, py + .95, 0])
        subN = T("if present, mostly blocked\nby magnesium", 26, PURPLE, line_spacing=.8).move_to([2.4, -1.35, 0])
        chp = chip("silent synapse: no AMPA response near rest", RED, 30).move_to([0, -3.0, 0])
        self.play(FadeIn(bouton), FadeIn(ves), FadeIn(post), FadeIn(chp, shift=UP * .1), run_time=.6)
        self.at("silent")
        self.play(Indicate(chp, color=RED, scale_factor=1.05), run_time=.6)
        self.at("lack working AMPA")
        self.play(Create(slotA), FadeIn(labA), FadeIn(subA), run_time=.8)
        self.at("and any")
        self.play(FadeIn(nmda), FadeIn(labN), FadeIn(qm), FadeIn(mg, shift=DOWN * .3), run_time=.7)
        self.at("mostly blocked")
        self.play(mg.animate.move_to([2.4, py + .4, 0]), run_time=.6)
        self.at("by magnesium")
        self.play(FadeIn(subN), run_time=.6)
        self.finish()


class S20Term(SpokenScene):
    def construct(self):
        old = VGroup(*[tile(-5.4 + 1.5 * i, 2.7, 1.2, "working") for i in range(5)])
        new = VGroup(*[tile(-5.4 + 1.5 * i, 1.4, 1.2, "plain") for i in range(5)])
        box, lab = panel("recorded current")
        tr = trace_mob(mini_vals(BASE_EV))
        by0, per = 1.0, .22
        cnt = ValueTracker(5)

        def col():
            v = cnt.get_value()
            r = Rectangle(width=1.2, height=per * v, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.35)
            r.move_to([4.6, by0 + per * v / 2, 0])
            n = M(str(int(round(v))), 44, TEXT).move_to([4.6, by0 + per * v + .35, 0])
            return VGroup(r, n)
        column = always_redraw(col)
        ticks = VGroup(*[VGroup(Line([3.75, by0 + per * k, 0], [3.95, by0 + per * k, 0], color=GREY, stroke_width=3),
                                T(str(k), 26, GREY).move_to([3.45, by0 + per * k, 0])) for k in (0, 5, 10)])
        bl = cap("synapse count", 5.0, .68, 24, TEXT)
        am = chip("AMPA minis: no change", ORANGE, 26).move_to([4.0, -.35, 0])
        self.add(old, box, lab, tr, ticks, column, bl)
        added = T("added, no AMPA", 26, ORANGE).move_to([-2.4, .62, 0])
        self.at("add to the count", lead=0)
        # Reveal one new silent profile per integer step in the count.
        for i, t in enumerate(new):
            self.play(FadeIn(t), cnt.animate.set_value(6 + i), run_time=.16)
        self.play(FadeIn(added), run_time=.2)
        self.at("but add no AMPA minis")
        self.play(FadeIn(am), run_time=.6)
        self.finish()


class S21Glyp(SpokenScene):
    def construct(self):
        a = astro(-4.9, 1.2, 1.2)
        al = cap("astrocyte", -4.9, -.5, 26, TEXT)
        cx, py = 2.4, .6
        bouton, ves, post = big_synapse(cx, py, w=5.6, hb=1.7, gap=.9, nves=7)
        sA = receptor(cx - 1.4, py, ORANGE, s=1.5, dashed=True)
        sB = receptor(cx + 1.4, py, ORANGE, s=1.5, dashed=True)
        gc = chip("glypicans 4 and 6", TEXT, 26, pad=.12).move_to([-4.9, 3.45, 0])
        # Use the actual right-facing branch tips; every dot terminates at a receptor slot.
        tips = [a[2].get_end(), a[16].get_end()]
        dots = VGroup(*[Dot(tips[i % 2], radius=.12, color=TEXT) for i in range(6)])
        dst = [(cx + dx, py, 0) for dx in (-1.65, 1.15, -1.4, 1.4, -1.15, 1.65)]
        paths = []
        for d, target in zip(dots, dst):
            source = d.get_center()
            paths.append(CubicBezier(source, source + RIGHT * 1.5,
                                     np.array(target) + LEFT * 1.4 + DOWN * .55, target))
        cups = VGroup(receptor(cx - 1.4, py - 1.0, ORANGE, s=1.5), receptor(cx + 1.4, py - 1.0, ORANGE, s=1.5))
        box, lab = panel("recorded current", cy=-2.25, h=2.7, w=12.4, x0=-6.2)
        xs = np.linspace(-5.9, 5.9, 260)

        def wavy(seed):
            return np.convolve(np.random.default_rng(seed).normal(0, 1, 266), np.ones(7) / 7, "same")[:260] * .02
        flat = VMobject(stroke_color=BLUE, stroke_width=4).set_points_as_corners(
            np.column_stack([xs, -2.25 + wavy(3), np.zeros(260)]))
        s_ = np.clip(xs - 1.8, 0, None)
        k = np.exp(-s_ / .35) - np.exp(-s_ / .07); k = k / k.max()
        resp = VMobject(stroke_color=ORANGE, stroke_width=5).set_points_as_corners(
            np.column_stack([xs, -2.25 + wavy(3) - .85 * np.where(xs >= 1.8, k, 0), np.zeros(260)]))
        ok = chip("responds", GREEN, 26).move_to([5.0, -1.45, 0])
        self.play(FadeIn(a), FadeIn(al), FadeIn(bouton), FadeIn(ves), FadeIn(post), FadeIn(sA), FadeIn(sB),
                  FadeIn(box), FadeIn(lab), FadeIn(flat), run_time=.8)
        self.at("found")
        self.play(FadeIn(gc), run_time=.5)
        self.at("also from astrocytes")
        self.play(LaggedStart(*[MoveAlongPath(d, path, rate_func=linear)
                               for d, path in zip(dots, paths)], lag_ratio=.12), run_time=1.9)
        self.at("recruit AMPA receptors")
        self.play(FadeOut(dots), FadeIn(cups), run_time=.4)
        self.play(cups.animate.shift(UP * 1.0), FadeOut(sA), FadeOut(sB), run_time=.9)
        self.at("the synapses respond")
        self.play(Transform(flat, resp), FadeIn(ok), run_time=.8)
        self.finish()


class S22Beat(Divider):
    TEXT_LINE = "Putting the two together"


class S23Split(SpokenScene):
    def construct(self):
        head = T("Astrocyte signals share the work", 34, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        f1 = RoundedRectangle(corner_radius=.2, width=5.6, height=5.0, stroke_color=GREY, stroke_width=3).move_to([-3.3, .25, 0])
        f2 = RoundedRectangle(corner_radius=.2, width=5.6, height=5.0, stroke_color=GREY, stroke_width=3).move_to([3.3, .25, 0])
        c1 = chip("thrombospondin", TEXT, 28).move_to([-3.3, 2.1, 0])
        c2 = chip("glypicans 4 and 6", TEXT, 28).move_to([3.3, 2.1, 0])
        pos = [(dx, y) for y in (.85, -.4) for dx in (-1.7, 0, 1.7)]
        t1 = VGroup(*[tile(-3.3 + dx, y, 1.4, "plain") for dx, y in pos])
        t2 = VGroup(*[tile(3.3 + dx, y, 1.4, "plain") for dx, y in pos])
        t2w = VGroup(*[tile(3.3 + dx, y, 1.4, "working") for dx, y in pos])
        l1 = T("mainly builds", 32, TEXT).move_to([-3.3, -1.75, 0])
        l2 = T("mainly switches on", 32, GREEN).move_to([3.3, -1.75, 0])
        note = cap("These assays do not show a fixed order.", 0, -3.35, 26, TEXT)
        self.at("so astrocyte signals")
        self.play(FadeIn(head), run_time=.5)
        self.at("share the work")
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(c1), FadeIn(c2), run_time=.7)
        self.at("mainly builds")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in t1], lag_ratio=.18), FadeIn(l1), run_time=1.3)
        self.at("mainly switch")
        self.play(FadeIn(note), LaggedStart(*[GrowFromCenter(t) for t in t2], lag_ratio=.08), run_time=.8)
        self.play(*[FadeIn(t[1], shift=UP * .1) for t in t2w], FadeIn(l2), run_time=.8)
        self.finish()


class S24Take(SpokenScene):
    def construct(self):
        tk = T("Takeaway", 28, GOLD, weight=BOLD).move_to([0, 3.5, 0])
        la, lb = lamp(-4.3, 2.55, True, .4), lamp(1.3, 2.55, False, .4)
        ta = T("there", 36, TEXT).next_to(la, RIGHT, buff=.3)
        tb = T("works", 36, TEXT).next_to(lb, RIGHT, buff=.3)
        nyet = chip("not yet", RED, 28).move_to([-.6, 2.55, 0])
        b1 = RoundedRectangle(corner_radius=.2, width=5.8, height=3.6, stroke_color=GREY, stroke_width=3).move_to([-3.4, -.55, 0])
        b2 = RoundedRectangle(corner_radius=.2, width=5.8, height=3.6, stroke_color=GREY, stroke_width=3).move_to([3.4, -.55, 0])
        tiles = VGroup(*[tile(-3.4 + dx, y, 1.3, "plain") for y in (.3, -.9) for dx in (-1.6, 0, 1.6)])
        c1 = chip("count it", TEXT, 32).move_to([-3.4, -1.75, 0])
        c1.scale_to_fit_height(.65)
        xs = np.linspace(.9, 5.9, 220)
        tr = VMobject(stroke_color=BLUE, stroke_width=4).set_points_as_corners(np.column_stack(
            [xs, -.45 + np.convolve(np.random.default_rng(8).normal(0, 1, 226), np.ones(7) / 7, "same")[:220] * .02
             - sum(0.9 * np.where(xs >= x0, (np.exp(-(xs - x0) / .3) - np.exp(-(xs - x0) / .06)) / .7, 0) for x0 in (2.0, 3.4, 4.8)),
             np.zeros(220)]))
        c2 = chip("record from it", BLUE, 32).move_to([3.4, -1.75, 0])
        c2.scale_to_fit_height(.65)
        note = cap("These assays do not show a fixed order of building and switching on.", 0, -3.3, 24, TEXT)
        lit = lamp(1.3, 2.55, True, .4)
        self.add(note)
        self.at("takeaway")
        self.play(FadeIn(tk), run_time=.4)
        self.at("a synapse that is there")
        self.play(FadeIn(la), FadeIn(ta), run_time=.5)
        self.at("not yet a synapse that works")
        self.play(FadeIn(lb), FadeIn(tb), FadeIn(nyet), run_time=.6)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(tiles), run_time=.5)
        self.at("count it")
        self.play(FadeIn(c1), run_time=.3)
        self.at("record from it")
        self.play(FadeIn(c2), Create(tr, rate_func=linear), run_time=.9)
        self.play(FadeOut(nyet), Transform(lb, lit), run_time=.4)
        self.finish()


class S25End(EndCard):
    LINE = "A synapse that is there is not yet a synapse that works."

    def construct(self):
        line = T(self.LINE, size=40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        l2 = T("Count it, and record from it.", size=34, font=TITLE_FONT, color=TEAL)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, l2, sub).arrange(DOWN, buff=.4)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(l2), run_time=self.beat(0.2))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
