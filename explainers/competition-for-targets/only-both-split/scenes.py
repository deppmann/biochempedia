"""Only Both Loops Split Them  (Developmental Neuroscience, competition for targets, chapter 4)

COLOR MAP (one color per concept, same as the other chapters)
  BLUE   = a neuron whose fate is not yet decided (lighter blue = the second neuron, B)
  GREEN  = a winner / a neuron that is protected or survives
  RED    = a loser / a neuron that dies or is pushed toward death
  YELLOW = nerve growth factor (NGF) and the catch of it
  PURPLE = the receptor TrkA (its level)
  PINK   = the NGF signal: its timer, duration and strength (and Coronin-1, which lengthens it)
  ORANGE = the punishment signal (not used in this chapter)
  TEAL   = p75 (not used in this chapter)
  TEXT   = plain labels, endosome outlines, equations
  GOLD   = the question mark, "toy" / "schematic" tags and one highlight
  GREY   = target, axons, axes, panel frames, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E98BB8"
BLUE_B = "#8FB7C9"   # neuron B (a duller blue so A and B differ)


def P(x, y):
    return np.array([x, y, 0.0])


# ----------------------------------------------------------------------------------------------
# the toy models: computed, not sketched
# (1) the four panels: 12 neurons, share x_i of the NGF caught (capture in proportion to receptor)
#     level feedback:    dx_i/dt = r x_i (D_i - mean D)    (more signal -> more receptor -> bigger share)
#     duration feedback: D_i relaxes toward h(n x_i), a rising S-curve of the share
#     no duration feedback: D_i = 1 for everyone.  No level feedback: shares never change.
# (2) the two-neuron pie: the lesson's own arithmetic. Each round squares the ratio of A's share to B's
#     (52/48 -> 1.17 -> 1.38 -> 1.90 ...), giving A = 52, 54, 58, 65, 78, 93 percent in rounds 1 to 6.
# ----------------------------------------------------------------------------------------------
def hill(s, lo=0.4, hi=1.6, p=8):
    return lo + (hi - lo) * s ** p / (1 + s ** p)


def toy(mode, n=12, seed=1, sd=0.12, T=4.0, steps=320, r=1.0, q=4.0, x0=None):
    rng = np.random.default_rng(seed)
    x = 1 + sd * rng.standard_normal(n) if x0 is None else np.array(x0, float)
    x = x / x.sum()
    D = np.ones(n)
    dt = T / steps
    out = [x * n]
    for _ in range(steps):
        tg = hill(n * x) if mode in ("dur", "both") else np.ones(n)
        D = D + dt * q * (tg - D)
        if mode in ("level", "both"):
            dx = r * x * (D - (x * D).sum())
            x = np.maximum(x + dt * dx, 1e-4)
            x = x / x.sum()
        out.append(x * n)
    return np.array(out)


MODES = ["none", "level", "dur", "both"]
DATA = {m: toy(m) for m in MODES}
# with no feedback, level only or duration only the shares never move: the three runs are the same numbers,
# so the three failing panels share one band by construction
assert np.allclose(DATA["none"], DATA["level"]) and np.allclose(DATA["none"], DATA["dur"])

R1 = 0.52 / 0.48


def lead_ratio(v):
    """A's share over B's after v rounds (v = 0 is round 1): the ratio is squared every round."""
    return R1 ** (2.0 ** v)


def share_a(v):
    r = lead_ratio(v)
    return float(r / (1 + r))


# ----------------------------------------------------------------------------------------------
# small drawing helpers
# ----------------------------------------------------------------------------------------------
def soma(p, color=BLUE, r=0.3, op=0.85):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to(p)


def to_state(d, color, op=0.85):
    return d.animate.set_stroke(color, opacity=1.0 if op > 0.3 else op + 0.3).set_fill(color, opacity=op)


def ngf_dot(p, r=0.11):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=1.5, fill_color=YELLOW, fill_opacity=1).move_to(p)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar_fill(xl, y, w, frac, color, h=0.4):
    ww = max(w * frac, 0.02)
    return Rectangle(width=ww, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(P(xl + ww / 2, y))


def bar_frame(xl, y, w, h=0.4):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to(P(xl + w / 2, y))


def two_color(parts, size=28, buff=0.12):
    """A label made of coloured words, e.g. [("level", PURPLE), (" + ", TEXT), ("duration", PINK)]."""
    return VGroup(*[T(t, size, c) for t, c in parts]).arrange(RIGHT, buff=buff, aligned_edge=DOWN)


def pie(xa, c, r, lsize=28):
    """Two-neuron pie: A (strong blue) and B (dull blue). Both slices computed from the share xa."""
    a = Sector(radius=r, start_angle=PI / 2 - TAU * xa, angle=TAU * xa, arc_center=c, stroke_color=BLUE,
               stroke_width=3, fill_color=BLUE, fill_opacity=0.85)
    b = Sector(radius=r, start_angle=PI / 2, angle=TAU * (1 - xa), arc_center=c, stroke_color=BLUE_B,
               stroke_width=3, fill_color=BLUE_B, fill_opacity=0.4)
    ma = PI / 2 - PI * xa
    mb = PI / 2 + PI * (1 - xa)
    la = T(f"A {int(round(100 * xa))}", lsize, TEXT, weight=BOLD).move_to(c + 0.55 * r * P(np.cos(ma), np.sin(ma)))
    if (1 - xa) > 0.28:
        lpos = c + 0.55 * r * P(np.cos(mb), np.sin(mb))
    else:   # a small slice: put its label just outside, turned a little to the side so it clears a tag above the pie
        lpos = c + (r + 0.5) * P(np.cos(mb + 0.5), np.sin(mb + 0.5))
    lb = T(f"B {int(round(100 * (1 - xa)))}", lsize, TEXT, weight=BOLD).move_to(lpos)
    return VGroup(a, b, la, lb)


def left_at(mob, x, y):
    """Place a mobject with its left edge at x and its centre line at y."""
    return mob.move_to(P(x + mob.width / 2, y))


# ---- the four-panel grid ----------------------------------------------------------------------
TITLES = ["no feedback", "feedback: level only", "feedback: duration only", "feedback: both"]
TITLES2 = ["no feedback", "feedback:\nlevel only", "feedback:\nduration only", "feedback:\nboth"]
TCOL = [GREY, PURPLE, PINK, TEXT]
FULL = dict(centres=[(-3.2, 1.2), (3.2, 1.2), (-3.2, -2.1), (3.2, -2.1)], w=6.2, h=3.2, ts=26, yl="NGF share",
            lm=0.95, tm=0.9, two=False)
COMPACT = dict(centres=[(-4.75, 1.2), (-0.75, 1.2), (-4.75, -2.1), (-0.75, -2.1)], w=4.0, h=3.2, ts=26, yl="share",
               lm=0.8, tm=1.25, two=True)
VMAX = 3.6
TAG_X = -6.7   # left edge of the heading band (top 12% of the frame)
TAG_Y = 3.3


def make_panel(i, g):
    cx, cy = g["centres"][i]
    w, h = g["w"], g["h"]
    frame = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=GREY, stroke_width=2,
                             fill_color=GREY, fill_opacity=0.06).move_to(P(cx, cy))
    x0, x1, y0, y1 = cx - w / 2 + g["lm"], cx + w / 2 - 0.3, cy - h / 2 + 0.8, cy + h / 2 - g["tm"]
    axes = VGroup(Line(P(x0, y0), P(x1, y0), color=GREY, stroke_width=2.5),
                  Line(P(x0, y0), P(x0, y1), color=GREY, stroke_width=2.5))
    ylab = T(g["yl"], 26, GREY).rotate(PI / 2).move_to(P(cx - w / 2 + 0.4, (y0 + y1) / 2))
    xlab = T("time", 26, GREY).move_to(P((x0 + x1) / 2, y0 - 0.4))
    title = T((TITLES2 if g["two"] else TITLES)[i], g["ts"], TCOL[i], weight=BOLD, line_spacing=0.8)
    title.move_to(P(cx - w / 2 + 0.25 + title.width / 2, cy + h / 2 - 0.2 - title.height / 2))
    return dict(frame=frame, axes=axes, title=title, box=(x0, x1, y0, y1), ylab=ylab, xlab=xlab,
                shell=VGroup(frame, axes, ylab, xlab))


def panel_curves(i, box, sw=3.0):
    data = DATA[MODES[i]]
    x0, x1, y0, y1 = box
    steps = data.shape[0]
    out = []
    for j in range(data.shape[1]):
        pts = [P(x0 + (x1 - x0) * k / (steps - 1), y0 + min(data[k, j], VMAX) / VMAX * (y1 - y0))
               for k in range(0, steps, 4)]
        out.append(VMobject(stroke_color=BLUE, stroke_width=sw).set_points_smoothly(pts))
    return VGroup(*out)


def split_colors(i):
    fin = DATA[MODES[i]][-1]
    return [GREEN if v > 1.5 else (RED if v < 0.5 else BLUE) for v in fin]


def colour_curves(c, i, big=True):
    cols = split_colors(i)
    for k, m in enumerate(c):
        if cols[k] != BLUE:
            m.set_stroke(cols[k], width=(4.5 if cols[k] == GREEN else 3.6) if big else 3.5)
    return c


def result_label(i, panels):
    x0, x1, y0, y1 = panels[i]["box"]
    txt, col = ("splits", GREEN) if i == 3 else ("no split", TEXT)
    t = T(txt, 26, col, weight=BOLD)
    return t.move_to(P(x0 + 0.2 + t.width / 2, y1 - 0.2))


def schem_tag():
    t = T("schematic, not published data", 26, GOLD)
    return left_at(t, TAG_X, TAG_Y)


def head_text(txt, size=30):
    return left_at(T(txt, size, TEXT), TAG_X, TAG_Y)


def question_frame():
    """The frame of the question (s11 and the pause): four titled panels, four question marks, headline."""
    panels = [make_panel(i, FULL) for i in range(4)]
    head = T("Which conditions split the neurons\ninto winners and losers?", 26, TEXT, line_spacing=0.9,
             t2c={"winners": GREEN, "losers": RED})
    left_at(head, TAG_X, TAG_Y)
    qs = []
    for i in range(4):
        x0, x1, y0, y1 = panels[i]["box"]
        qs.append(T("?", 90, GOLD, weight=BOLD).move_to(P((x0 + x1) / 2, (y0 + y1) / 2 + 0.05)))
    cp = chip("Pause and predict", GOLD, 28, 0.18).move_to(P(4.6, TAG_Y))
    return panels, head, qs, cp


# ==============================================================================================
class S00Title(TitleCard):
    LESSON = "Competition: How Neurons Win a Target"
    TITLE = "Only Both Loops Split Them"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    def construct(self):
        c, r = P(-3.3, 0.2), 2.6
        pg = pie(0.52, c, r)
        frozen = T("frozen", 28, GREY).move_to(P(-3.3, -3.35))
        self.play(FadeIn(pg, scale=0.9), FadeIn(frozen), run_time=0.4)
        self.at("raising track")
        chip_a = chip("raise TrkA", PURPLE, 32).move_to(P(3.4, 2.1))
        self.play(FadeIn(chip_a, shift=DOWN * 0.2), run_time=0.5)
        a1 = arr(P(1.4, 1.5), P(-0.6, 0.9), GREY, 5, 0.25)
        same = T("still 52 to 48", 30, TEXT).move_to(P(3.4, 0.5))
        self.at("enough")
        self.play(GrowArrow(a1), FadeIn(same), run_time=0.6)
        self.at("what else must")
        nchip = chip("NGF", YELLOW, 32).move_to(P(2.1, -1.6))
        q = T("?", 150, GOLD, weight=BOLD).move_to(P(4.9, -1.6))
        a2 = arr(P(3.0, -1.6), P(4.0, -1.6), GREY, 5, 0.25)
        self.play(FadeIn(nchip, shift=UP * 0.2), GrowArrow(a2), FadeIn(q, scale=0.4), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(SpokenScene):
    def construct(self):
        ya, yb = 1.6, -1.6
        A = soma(P(-5.4, ya), BLUE, 0.8, 0.85)
        B = soma(P(-5.4, yb), BLUE_B, 0.8, 0.45)
        la = T("A", 36, TEXT, weight=BOLD).move_to(A)
        lb = T("B", 36, TEXT, weight=BOLD).move_to(B)
        nchip = chip("NGF", YELLOW, 34).move_to(P(5.6, 0.0))
        XL, W = -4.0, 6.6
        fr = [bar_frame(XL, y, W, 0.8) for y in (ya, yb)]
        self.play(FadeIn(A, scale=0.6), FadeIn(B, scale=0.6), FadeIn(la), FadeIn(lb), FadeIn(nchip),
                  *[FadeIn(f) for f in fr], run_time=0.7)
        self.at("controls")
        arrow = arr(P(5.0, 0.5), P(3.0, 1.45), YELLOW, 6, 0.28)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.at("how long")
        fl = [bar_fill(XL, y, W, 0.5, PINK, 0.8) for y in (ya, yb)]
        tl = [T("signal timer", 26, PINK).move_to(P(XL + 1.1, y + 0.8)) for y in (ya, yb)]
        self.play(*[GrowFromEdge(f, LEFT) for f in fl], *[FadeIn(t) for t in tl], run_time=0.6)
        self.at("signal lasts")
        longer = T("longer", 34, PINK, weight=BOLD).move_to(P(1.2, ya + 0.85))
        same = T("shorter", 30, TEXT).move_to(P(1.2, yb + 0.85))
        self.play(Transform(fl[0], bar_fill(XL, ya, W, 1.0, PINK, 0.8)), FadeIn(longer, shift=UP * 0.1),
                  run_time=1.2, rate_func=linear)
        self.play(FadeIn(same), run_time=0.3)
        self.wait(1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
# shared axon scene (s03, s04, s05)
AX_Y = -0.1
SOMA_P = P(-4.6, AX_Y)
TIP_X = 3.3
TARGET_X = 5.4


def axon_scene():
    gang_fill = RoundedRectangle(corner_radius=0.3, width=4.4, height=5.6, stroke_width=0, fill_color=GREY,
                                 fill_opacity=0.06).move_to(P(-4.6, 0.1))
    gang_line = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=4.4, height=5.6, stroke_color=GREY,
                                                stroke_width=3).move_to(P(-4.6, 0.1)), num_dashes=70)
    gl = T("ganglion", 26, GREY).move_to(P(-4.6, 2.55))
    gang = VGroup(gang_fill, gang_line, gl)
    s = soma(SOMA_P, BLUE, 1.4, 0.3)
    nuc = Circle(radius=0.65, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.45).move_to(SOMA_P)
    axon = Line(P(-3.2, AX_Y), P(TIP_X, AX_Y), color=GREY, stroke_width=12)
    tipb = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.6).move_to(P(TIP_X, AX_Y))
    target = RoundedRectangle(corner_radius=0.2, width=2.4, height=6.4, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.12).move_to(P(TARGET_X, 0.0))
    tl = T("target", 26, GREY).move_to(P(TARGET_X, -2.85))
    return gang, s, nuc, axon, tipb, target, tl


def caught_dots():
    return VGroup(*[ngf_dot(P(3.92, AX_Y + dy), 0.13) for dy in (0.32, -0.32)])


class S03(SpokenScene):
    def construct(self):
        gang, s, nuc, axon, tipb, target, tl = axon_scene()
        nchip = chip("NGF", YELLOW, 26, 0.16).move_to(P(TARGET_X, 2.7))
        dots = VGroup(*[ngf_dot(P(x, y), 0.13) for x, y in [(4.75, 0.9), (5.9, 0.5), (5.2, -1.0)]])
        self.play(FadeIn(gang), FadeIn(target), FadeIn(tl), FadeIn(nchip), FadeIn(dots), FadeIn(s), FadeIn(nuc),
                  Create(axon), FadeIn(tipb), run_time=0.8)
        self.at("caught")
        caught = caught_dots()
        self.play(FadeOut(dots[0]), FadeOut(dots[1]), FadeIn(caught, scale=0.4), run_time=0.5)
        self.at("axon tip")
        lt = T("axon tip", 26, GREY).move_to(P(2.2, 1.3))
        at = arr(P(2.6, 0.95), P(TIP_X - 0.1, 0.3), GREY, 4, 0.2)
        self.play(FadeIn(lt), GrowArrow(at), run_time=0.4)
        self.at("far from")
        far = DoubleArrow(P(-4.6, -3.25), P(TIP_X, -3.25), buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        fl = T("far", 30, TEXT).move_to(P(-0.6, -2.75))
        self.play(GrowFromCenter(far), FadeIn(fl), run_time=0.7)
        self.at("cell body")
        cb = T("cell body", 26, GREY).move_to(P(-4.6, -2.05))
        self.play(FadeIn(cb), Indicate(s, color=BLUE, scale_factor=1.06), run_time=0.7)
        self.at("yet it changes")
        q = T("?", 110, GOLD, weight=BOLD).move_to(P(-0.2, 1.2))
        self.play(FadeIn(q, scale=0.4), run_time=0.5)
        self.at("which genes")
        genes = VGroup(*[Rectangle(width=0.22, height=0.22, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                                   fill_opacity=0.15) for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to(SOMA_P)
        gl = T("genes", 26, TEXT).move_to(P(-3.5, 1.85))
        gline = Line(P(-3.7, 1.65), P(-4.27, 0.47), color=GREY, stroke_width=3)
        self.play(FadeIn(genes), FadeIn(gl), Create(gline), run_time=0.4)
        self.at("nucleus")
        nl = T("nucleus", 26, TEXT).move_to(P(-5.7, 1.85))
        nline = Line(P(-5.2, 1.65), P(-4.93, 0.47), color=GREY, stroke_width=3)
        self.play(FadeIn(nl), Create(nline), Indicate(nuc, color=TEXT, scale_factor=1.2), run_time=0.5)
        self.at("turns on")
        self.play(*[g.animate.set_fill(TEXT, opacity=0.95).set_stroke(TEXT) for g in genes], run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def endo(p, scale=1.0):
    """A signaling endosome: a vesicle outline, an NGF dot inside, a TrkA stub on its membrane."""
    ring = Circle(radius=0.4 * scale, stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.08)
    dot = ngf_dot(P(0.05 * scale, 0), 0.11 * scale)
    stub = Rectangle(width=0.13 * scale, height=0.34 * scale, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
    stub.move_to(P(-0.4 * scale, 0))
    return VGroup(ring, dot, stub).move_to(p)


def clock_tracker(scene):
    ck = ValueTracker(0.0)
    ck.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(ck)
    return ck


ES = 1.4   # endosome scale


class S04(SpokenScene):
    def construct(self):
        gang, s, nuc, axon, tipb, target, tl = axon_scene()
        caught = caught_dots()
        cb = T("cell body", 26, GREY).move_to(P(-4.6, -2.05))
        nl = T("nucleus", 26, TEXT).move_to(P(-5.7, 1.85))
        nline = Line(P(-5.2, 1.65), P(-4.93, 0.47), color=GREY, stroke_width=3)
        genes = VGroup(*[Rectangle(width=0.22, height=0.22, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT,
                                   fill_opacity=0.95) for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to(SOMA_P)
        self.add(gang, s, nuc, axon, tipb, target, tl, caught, cb, genes, nl, nline)
        X0, X1, DUR = TIP_X - 0.2, -1.6, 4.5
        e = endo(P(X0, AX_Y), ES)
        ck = clock_tracker(self)
        state = {"t0": None}

        def pos():
            if state["t0"] is None:
                return P(X0, AX_Y)
            f = min(max((ck.get_value() - state["t0"]) / DUR, 0.0), 1.0)
            f = f * f * (3 - 2 * f) * 0.35 + f * 0.65     # a gentle ease: still a steady trip
            return P(X0 + (X1 - X0) * f, AX_Y)
        e.add_updater(lambda m: m.move_to(pos()))
        # NGF and TrkA labels follow the endosome, each with a short leader
        nlab = T("NGF", 26, YELLOW)
        tlab = T("TrkA", 26, PURPLE)
        nlab.add_updater(lambda m: m.move_to(e.get_center() + P(0.55, 1.15)))
        tlab.add_updater(lambda m: m.move_to(e.get_center() + P(-0.95, 1.15)))
        nl_line = always_redraw(lambda: Line(e.get_center() + P(0.55 - 0.15, 1.15 - 0.2), e.get_center() + P(0.05 * ES + 0.08, 0.16),
                                             color=YELLOW, stroke_width=3))
        tl_line = always_redraw(lambda: Line(e.get_center() + P(-0.95 + 0.3, 1.15 - 0.2), e.get_center() + P(-0.4 * ES, 0.17 * ES),
                                             color=PURPLE, stroke_width=3))
        self.play(FadeIn(e, scale=0.5), FadeIn(nlab), FadeIn(tlab), FadeIn(nl_line), FadeIn(tl_line), run_time=0.7)
        self.at("travel back")
        state["t0"] = ck.get_value()
        a_sig = arr(P(2.9, -1.5), P(-2.8, -1.5), GREY, 6, 0.3)
        sl = T("signal", 28, GREY).move_to(P(0.0, -2.05))
        self.play(GrowArrow(a_sig), FadeIn(sl), run_time=0.8)
        self.at("endosomes")
        lab = T("endosome", 26, TEXT)
        lab.add_updater(lambda m: m.move_to(e.get_center() + P(0, -1.0)))
        lline = always_redraw(lambda: Line(e.get_center() + P(0, -0.82), e.get_center() + P(0, -0.58), color=TEXT, stroke_width=3))
        self.play(FadeIn(lab), FadeIn(lline), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    def construct(self):
        XL, W, H = -4.2, 9.4, 1.0
        y1, y2 = 2.0, -0.45
        y1i = 0.7      # the first row starts mid-frame and moves up when the second row arrives
        # carried from s04: the axon scene with the endosome near the cell body
        gang, s, nuc, axon, tipb, target, tl = axon_scene()
        caught = caught_dots()
        cb = T("cell body", 26, GREY).move_to(P(-4.6, -2.05))
        a_sig = arr(P(2.9, -1.5), P(-2.8, -1.5), GREY, 6, 0.3)
        sl = T("signal", 28, GREY).move_to(P(0.0, -2.05))
        e1 = endo(P(-1.6, AX_Y), ES)
        lab = T("endosome", 26, TEXT).move_to(e1.get_center() + P(0, -1.0))
        lline = Line(e1.get_center() + P(0, -0.82), e1.get_center() + P(0, -0.58), color=TEXT, stroke_width=3)
        nlab = T("NGF", 26, YELLOW).move_to(e1.get_center() + P(0.55, 1.15))
        tlab = T("TrkA", 26, PURPLE).move_to(e1.get_center() + P(-0.95, 1.15))
        l_n = Line(e1.get_center() + P(0.4, 0.95), e1.get_center() + P(0.05 * ES + 0.08, 0.16), color=YELLOW, stroke_width=3)
        l_t = Line(e1.get_center() + P(-0.65, 0.95), e1.get_center() + P(-0.4 * ES, 0.17 * ES), color=PURPLE, stroke_width=3)
        cb2 = T("nucleus", 26, TEXT).move_to(P(-5.7, 1.85))
        nl2 = Line(P(-5.2, 1.65), P(-4.93, 0.47), color=GREY, stroke_width=3)
        genes = VGroup(*[Rectangle(width=0.22, height=0.22, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT,
                                   fill_opacity=0.95) for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to(SOMA_P)
        old = VGroup(gang, s, nuc, axon, tipb, target, tl, caught, cb, a_sig, sl, lab, lline, nlab, tlab, l_n, l_t, cb2, nl2, genes)
        self.add(old, e1)
        fr1, fl1 = bar_frame(XL, y1i, W, H), bar_fill(XL, y1i, W, 1.0, PINK, H)
        t1 = T("signal timer", 26, PINK).move_to(P(XL + 1.2, y1i + 0.85))
        self.play(FadeOut(old), e1.animate.move_to(P(-5.5, y1i)), FadeIn(fr1), GrowFromEdge(fl1, LEFT), FadeIn(t1),
                  run_time=1.0)
        self.at("ngf")
        nchip = chip("NGF", YELLOW, 30).move_to(P(-4.6, -2.8))
        self.play(FadeIn(nchip, shift=UP * 0.2), run_time=0.4)
        self.at("induces")
        a1 = arr(P(-3.6, -2.8), P(-1.9, -2.8), YELLOW, 5, 0.25)
        self.play(GrowArrow(a1), run_time=0.4)
        self.at("coronin 1")
        cor = chip("Coronin-1", PINK, 30).move_to(P(0.2, -2.8))
        e2 = endo(P(-5.5, y2), ES)
        tag = Rectangle(width=0.5, height=0.22, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to(
            e2.get_center() + P(0, 0.5 * ES * 0.95))
        fr2, fl2 = bar_frame(XL, y2, W, H), bar_fill(XL, y2, W, 1.0, PINK, H)
        t1b = T("without Coronin-1", 26, TEXT).move_to(P(XL + 1.5, y1 + 0.85))
        t2 = T("with Coronin-1", 26, PINK).move_to(P(XL + 1.3, y2 + 0.85))
        self.play(FadeIn(cor, scale=0.7), FadeIn(e2, scale=0.6), FadeIn(tag), FadeIn(fr2), FadeIn(fl2),
                  Transform(t1, t1b), FadeIn(t2), e1.animate.move_to(P(-5.5, y1)), fr1.animate.move_to(P(XL + W / 2, y1)),
                  fl1.animate.move_to(P(XL + W / 2, y1)), run_time=0.9)
        self.at("keeps these")
        self.play(FadeOut(nchip), FadeOut(a1), FadeOut(cor),
                  Transform(fl1, bar_fill(XL, y1, W, 0.0, PINK, H), run_time=1.5, rate_func=linear),
                  Transform(fl2, bar_fill(XL, y2, W, 0.85, PINK, H), run_time=1.5, rate_func=linear))
        longer = T("lasts longer", 30, PINK, weight=BOLD).move_to(P(XL + W - 1.3, y2 - 0.85))
        self.play(FadeIn(longer, shift=UP * 0.1), run_time=0.4)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
CARD_W, CARD_H, CARD_Y = 4.2, 4.6, 0.3


class S06(SpokenScene):
    def construct(self):
        slots = [P(-4.5, CARD_Y), P(0.0, CARD_Y), P(4.5, CARD_Y)]
        box1 = RoundedRectangle(corner_radius=0.2, width=CARD_W, height=CARD_H, stroke_color=PINK, stroke_width=3,
                                fill_color=PINK, fill_opacity=0.1).move_to(slots[0])
        top = chip("Coronin-1", PINK, 38, 0.24).move_to(slots[0] + P(0, 1.6))
        self.play(FadeIn(box1), FadeIn(top, scale=0.8), run_time=0.5)
        self.at("required")
        l1 = T("required for\nnormal competition", 30, TEXT, line_spacing=0.9).move_to(slots[0] + P(0, 0.3))
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.6)
        self.at("in the mouse")
        l2 = T("in the mouse", 32, GREEN).move_to(slots[0] + P(0, -1.0))
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.5)
        self.at("one mechanism")
        om = T("one mechanism", 32, PINK, weight=BOLD).move_to(slots[0] + P(0, -CARD_H / 2 - 0.45))
        self.play(FadeIn(om, shift=UP * 0.1), Indicate(box1, color=PINK, scale_factor=1.03), run_time=0.7)
        self.at("there may be")
        ghosts = VGroup()
        for p in slots[1:]:
            b = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=CARD_W, height=CARD_H, stroke_color=GOLD,
                                                stroke_width=3).move_to(p), num_dashes=44)
            q = T("?", 100, GOLD, weight=BOLD).move_to(p)
            ghosts.add(VGroup(b, q))
        ghosts.set_opacity(0.7)
        ol = T("others?", 36, GOLD, weight=BOLD).move_to(P(2.25, CARD_Y - CARD_H / 2 - 0.45))
        self.play(LaggedStart(*[FadeIn(g, scale=0.9) for g in ghosts], lag_ratio=0.25), run_time=0.7)
        self.at("others")
        self.play(FadeIn(ol, shift=UP * 0.1), run_time=0.4)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
NEURON_XS = [-5, -3, -1, 1, 3, 5]
ROW_Y = -2.7


def neuron_row():
    return VGroup(*[soma(P(x, ROW_Y), BLUE, 0.6, 0.85) for x in NEURON_XS])


def wavy(y, x0, x1, amp, k, phase=0.0):
    n = 90
    pts = [P(x0 + (x1 - x0) * u / n, y + amp * np.sin(k * u / n * TAU + phase)) for u in range(n + 1)]
    return VMobject(stroke_color=GREY, stroke_width=4, stroke_opacity=0.55).set_points_smoothly(pts)


class S07(SpokenScene):
    def construct(self):
        row = VGroup(*[soma(P(x * 1.15, -2.65), BLUE, 0.85, 0.85) for x in NEURON_XS])
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in row], lag_ratio=0.1), run_time=0.9)
        self.at("model")
        sketch = VGroup(wavy(0.75, -4.6, 4.6, 0.14, 9), wavy(0.1, -4.6, 3.4, 0.14, 7, 1.0), wavy(-0.55, -4.6, 4.1, 0.14, 8, 2.0))
        eql = T("model equations (not shown)", 28, GREY).move_to(P(0, -1.2))
        self.play(FadeIn(sketch), FadeIn(eql), run_time=0.8)
        self.at("neuroscientists")
        head = T("computational neuroscientists", 32, GREY).move_to(P(0, 3.4))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("stefan")
        c1 = RoundedRectangle(corner_radius=0.2, width=5.6, height=1.7, stroke_color=TEXT, stroke_width=3,
                              fill_color=TEXT, fill_opacity=0.08).move_to(P(-3.3, 2.2))
        n1 = T("Stefan Mihalas", 52, TEXT).move_to(c1)
        self.play(FadeIn(VGroup(c1, n1), shift=UP * 0.2), run_time=0.6)
        self.at("ernst")
        c2 = RoundedRectangle(corner_radius=0.2, width=5.6, height=1.7, stroke_color=TEXT, stroke_width=3,
                              fill_color=TEXT, fill_opacity=0.08).move_to(P(3.3, 2.2))
        n2 = T("Ernst Niebur", 52, TEXT).move_to(c2)
        self.play(FadeIn(VGroup(c2, n2), shift=UP * 0.2), run_time=0.6)
        self.at("join the group")
        self.play(Indicate(row, color=BLUE, scale_factor=1.12), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08(SpokenScene):
    def construct(self):
        NY, TOPY = ROW_Y, 2.0
        row = neuron_row()
        self.add(row)
        ck = clock_tracker(self)
        state = {"t0": None}
        axons = VGroup(*[Line(P(x, NY + 0.6), P(x, TOPY), color=GREY, stroke_width=4) for x in NEURON_XS])
        self.at("neurons")
        self.play(Indicate(row, color=BLUE, scale_factor=1.1), run_time=0.6)
        self.at("competing")
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.1), run_time=1.0)
        self.at("ngf")
        tips = VGroup(*[ngf_dot(P(x, TOPY + 0.12), 0.14) for x in NEURON_XS])
        self.play(LaggedStart(*[FadeIn(t, scale=0.3) for t in tips], lag_ratio=0.1), run_time=0.6)
        self.at("the target makes")
        target = RoundedRectangle(corner_radius=0.2, width=12.2, height=1.1, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.15).move_to(P(0, 2.55))
        tl = T("target", 28, GREY).move_to(P(-5.4, 2.55))
        self.play(FadeIn(target), FadeIn(tl), FadeOut(tips), run_time=0.5)
        dots = VGroup()
        span = TOPY - (NY + 0.7)
        for x in NEURON_XS:
            for ph in (0.0, 0.34, 0.67):
                d = ngf_dot(P(x, TOPY), 0.12)

                def upd(m, x=x, ph=ph):
                    if state["t0"] is None:
                        m.set_opacity(0)
                        return
                    f = ((((ck.get_value() - state["t0"]) * 1.3) / span) + ph) % 1.0
                    m.set_opacity(1)
                    m.move_to(P(x, TOPY - f * span))
                d.add_updater(upd)
                dots.add(d)
        self.add(dots)
        state["t0"] = ck.get_value()
        self.at("constant rate")
        cr = chip("constant rate", YELLOW, 26, 0.16).move_to(P(0, 3.45))
        self.play(FadeIn(cr, scale=0.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09(SpokenScene):
    def construct(self):
        panels = [make_panel(i, FULL) for i in range(4)]
        h1 = head_text("four conditions")
        self.play(FadeIn(h1), LaggedStart(*[FadeIn(p["shell"], scale=0.95) for p in panels], lag_ratio=0.2), run_time=1.5)
        self.at("no feedback")
        self.play(FadeIn(panels[0]["title"], shift=RIGHT * 0.2), run_time=0.5)
        self.at("level alone")
        self.play(FadeIn(panels[1]["title"], shift=RIGHT * 0.2), run_time=0.5)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        panels = [make_panel(i, FULL) for i in range(4)]
        self.add(*[p["shell"] for p in panels], panels[0]["title"], panels[1]["title"], head_text("four conditions"))
        self.at("signal duration")
        self.play(FadeIn(panels[2]["title"], shift=RIGHT * 0.2), run_time=0.5)
        self.at("feedback on both")
        self.play(FadeIn(panels[3]["title"], shift=RIGHT * 0.2), run_time=0.5)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        panels, head, qs, cp = question_frame()
        h1 = head_text("four conditions")
        self.add(*[p["shell"] for p in panels], *[p["title"] for p in panels], h1)
        self.play(FadeOut(h1), FadeIn(head, shift=DOWN * 0.1), FadeIn(cp, scale=0.9), run_time=0.6)
        self.at("split")
        self.play(LaggedStart(*[FadeIn(q, scale=0.4) for q in qs], lag_ratio=0.15), run_time=0.9)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        panels, head, qs, cp = question_frame()
        self.add(*[p["shell"] for p in panels], *[p["title"] for p in panels], head, cp, *qs)
        ring_c = P(1.45, TAG_Y)
        tr = ValueTracker(0.0)
        ring = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()) - 1e-3,
                                         arc_center=ring_c, color=GOLD, stroke_width=6))
        base = Circle(radius=0.42, color=GREY, stroke_width=2).move_to(ring_c)
        self.add(base, ring)
        num = T("5", 30, GOLD, weight=BOLD).move_to(ring_c)
        self.add(num)
        for k in range(5, 0, -1):
            new = T(str(k), 30, GOLD, weight=BOLD).move_to(ring_c)
            self.remove(num)
            num = new
            self.add(num)
            self.play(tr.animate.set_value((5 - k + 1) / 5.0), run_time=1.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13(SpokenScene):
    def construct(self):
        panels, head, qs, cp = question_frame()
        self.add(*[p["shell"] for p in panels], *[p["title"] for p in panels], head, cp, *qs)
        curves = [panel_curves(i, panels[i]["box"]) for i in range(4)]
        tag = schem_tag()
        res = [result_label(i, panels) for i in range(4)]
        self.play(FadeOut(head), FadeOut(cp), *[FadeOut(q) for q in qs], FadeIn(tag), run_time=0.2)
        self.at("only feedback")
        self.play(*[Create(m, rate_func=linear) for m in curves[3]], run_time=0.6)
        self.at("both")
        colour_curves(curves[3], 3)
        self.play(*[curves[3][k].animate.set_stroke(split_colors(3)[k], width=4.5 if split_colors(3)[k] == GREEN else 3.6)
                    for k in range(12) if split_colors(3)[k] != BLUE],
                  panels[3]["frame"].animate.set_stroke(GREEN, width=4), FadeIn(res[3]), run_time=0.5)
        self.at("either one")
        anims = []
        for i in range(3):
            anims += [Create(m, rate_func=linear) for m in curves[i]]
        self.play(*anims, run_time=0.7)
        self.at("alone")
        self.play(*[FadeIn(res[i]) for i in range(3)], run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def final_grid(g):
    panels = [make_panel(i, g) for i in range(4)]
    cv = [colour_curves(panel_curves(i, panels[i]["box"], sw=3.0), i) for i in range(4)]
    res = [result_label(i, panels) for i in range(4)]
    panels[3]["frame"].set_stroke(GREEN, width=4)
    grp = VGroup(*[VGroup(p["shell"], p["title"]) for p in panels], *cv, *res)
    return panels, grp


class S14(SpokenScene):
    def construct(self):
        fpanels, full = final_grid(FULL)
        tag = schem_tag()
        self.add(full, tag)
        cpanels, comp = final_grid(COMPACT)
        c, r = P(4.3, -0.2), 2.3
        pg = pie(0.52, c, r, 26)
        toy_tag = chip("toy: two neurons", GOLD, 28, 0.18).move_to(P(4.3, 3.1))
        self.at("arithmetic")
        self.play(FadeOut(full), FadeIn(comp), FadeIn(pg, scale=0.9), FadeIn(toy_tag), run_time=0.9)
        self.at("both failures")
        self.play(cpanels[1]["frame"].animate.set_stroke(GOLD, width=5),
                  cpanels[2]["frame"].animate.set_stroke(GOLD, width=5), run_time=0.6)
        self.finish()


PIE_C = P(-3.4, 0.1)
PIE_R = 2.7
TOY_Y = 3.4


def toy_chip():
    return chip("toy: two neurons", GOLD, 26, 0.12).move_to(P(PIE_C[0], TOY_Y))


class S15(SpokenScene):
    def construct(self):
        pg = pie(0.52, PIE_C, PIE_R)
        toy_tag = toy_chip()
        self.add(pg, toy_tag)
        XL, BH = 1.6, 0.7
        ya, yb = 1.35, 0.4
        tag = chip("feedback: level only", PURPLE, 28, 0.18).move_to(P(3.9, 3.05))
        cap = T("TrkA level", 26, PURPLE).move_to(P(3.9, 2.2))
        la = T("A", 32, TEXT, weight=BOLD).move_to(P(1.05, ya))
        lb = T("B", 32, TEXT, weight=BOLD).move_to(P(1.05, yb))
        fa = bar_fill(XL, ya, 2.55, 1.0, PURPLE, BH)
        fb = bar_fill(XL, yb, 2.35, 1.0, PURPLE, BH)        # 52 : 48
        self.at("level alone")
        self.play(FadeIn(tag), FadeIn(cap), FadeIn(la), FadeIn(lb), GrowFromEdge(fa, LEFT), GrowFromEdge(fb, LEFT),
                  run_time=0.8)
        self.at("capture")
        cc = chip("catch in proportion to receptor", YELLOW, 26, 0.16).move_to(P(3.8, -1.1))
        ca = arr(P(0.85, -1.1), P(-0.75, -1.1), YELLOW, 5, 0.25)
        self.play(FadeIn(cc, shift=UP * 0.15), GrowArrow(ca), run_time=0.6)
        self.at("every ratio")
        res1 = T("still 52 to 48", 32, TEXT, weight=BOLD).move_to(P(PIE_C[0], -3.35))
        self.play(Transform(fa, bar_fill(XL, ya, 2.55 * 1.7, 1.0, PURPLE, BH)),
                  Transform(fb, bar_fill(XL, yb, 2.35 * 1.7, 1.0, PURPLE, BH)), run_time=1.2)
        self.play(FadeIn(res1), Indicate(pg, color=TEXT, scale_factor=1.03), run_time=0.7)
        self.at("duration alone")
        tag2 = chip("feedback: duration only", PINK, 28, 0.18).move_to(P(3.9, 3.05))
        cap2 = T("signal duration", 26, PINK).move_to(P(3.9, 2.2))
        cc2 = chip("catch unchanged", YELLOW, 26, 0.16).move_to(P(3.8, -1.1))
        self.play(Transform(tag, tag2), Transform(cap, cap2), Transform(cc, cc2),
                  Transform(fa, bar_fill(XL, ya, 4.2, 1.0, PINK, BH)),
                  Transform(fb, bar_fill(XL, yb, 4.2 / 1.17, 1.0, PINK, BH)), run_time=0.6)   # 52/48 squared = 1.17
        self.at("never changes")
        self.play(Indicate(cc, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("shares stay")
        self.play(Indicate(res1, color=GOLD, scale_factor=1.12), Indicate(pg, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        v = ValueTracker(0.0)
        pg = always_redraw(lambda: pie(share_a(v.get_value()), PIE_C, PIE_R))
        toy_tag = toy_chip()
        counter = always_redraw(lambda: T(f"round {min(6, int(v.get_value() + 0.5) + 1)} of 6", 34, TEXT, weight=BOLD)
                                .move_to(P(PIE_C[0], -3.35)))
        self.add(pg, toy_tag, counter)
        cx = 3.6
        sig = RoundedRectangle(corner_radius=0.14, width=4.4, height=0.95, stroke_color=GREY, stroke_width=2.5,
                               fill_color=GREY, fill_opacity=0.1).move_to(P(cx, 0.35))
        sigl = two_color([("level", PURPLE), ("+", TEXT), ("duration", PINK)], 32).move_to(sig)
        catch = chip("catch", YELLOW, 36).move_to(P(cx, 2.75))
        a_r = CurvedArrow(P(cx + 1.0, 2.55), P(cx + 1.9, 0.9), angle=-2.2, color=GREY, stroke_width=5, tip_length=0.25)
        a_l = CurvedArrow(P(cx - 1.9, 0.85), P(cx - 1.0, 2.4), angle=-2.2, color=GREY, stroke_width=5, tip_length=0.25)
        loop = T("the loop closes", 32, GOLD, weight=BOLD).move_to(P(cx, 1.55))
        self.at("level and duration")
        self.play(FadeIn(sig), FadeIn(sigl), run_time=0.6)
        self.at("close a loop")
        self.play(FadeIn(catch, scale=0.8), run_time=0.4)
        self.play(Create(a_r), Create(a_l), run_time=0.9)
        # lead and reward: A over B in the catch (lead) and in the signal (reward), the ratio squared each round
        XB, YL, YR = 2.3, -1.5, -2.4
        lead_l = T("lead", 28, YELLOW, weight=BOLD)
        left_at(lead_l, 0.45, YL)
        rew_l = T("reward", 28, PINK, weight=BOLD)
        left_at(rew_l, 0.45, YR)
        cap = T("A compared with B", 26, GREY).move_to(P(3.6, -3.3))

        def bar(y, val, color):
            ww = min(max(val * 3.0, 0.05), 2.7)
            return Rectangle(width=ww, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
                P(XB + ww / 2, y))

        def num(x):
            return f"{x:.0f}x" if x >= 100 else f"{x:.2f}x"

        def lead_val():
            return lead_ratio(v.get_value()) - 1.0

        def rew_val():
            return lead_ratio(v.get_value()) ** 2 - 1.0
        lead_b = always_redraw(lambda: bar(YL, lead_val(), YELLOW))
        rew_b = always_redraw(lambda: bar(YR, rew_val(), PINK))
        lead_n = always_redraw(lambda: left_at(M(num(lead_ratio(v.get_value())), 26, TEXT), 5.15, YL))
        rew_n = always_redraw(lambda: left_at(M(num(lead_ratio(v.get_value()) ** 2), 26, TEXT), 5.15, YR))
        self.at("signal that")
        self.play(FadeIn(lead_l), FadeIn(rew_l), FadeIn(cap), FadeIn(lead_b), FadeIn(rew_b), FadeIn(lead_n), FadeIn(rew_n),
                  run_time=0.5)
        self.at("rises faster")
        self.add(loop)
        self.play(FadeIn(loop, scale=0.8), v.animate.set_value(5.0), run_time=4.2, rate_func=linear)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        pg = pie(share_a(5.0), PIE_C, PIE_R).set_opacity(0.6)
        toy_tag = toy_chip()
        done = T("round 6 of 6", 34, GREY, weight=BOLD).move_to(P(PIE_C[0], -3.35))
        self.add(pg, toy_tag, done)
        self.at("toy reason")
        toy_c = chip("toy reason", GOLD, 40).move_to(P(3.5, 2.7))
        self.play(FadeIn(toy_c, scale=0.8), run_time=0.5)
        self.at("published equations")
        npub = T("not the published equations", 32, TEXT).move_to(P(3.5, 1.5))
        self.play(FadeIn(npub, shift=UP * 0.1), run_time=0.6)
        self.at("illustrates")
        c1 = left_at(chip("level", PURPLE, 34), 0.4, 0.2)
        c2 = left_at(chip("duration", PINK, 34), 0.4, -1.0)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        self.at("one loop")
        t1 = left_at(T("alone: no split", 32, TEXT), 3.3, 0.2)
        t2 = left_at(T("alone: no split", 32, TEXT), 3.3, -1.0)
        self.play(FadeIn(t1, shift=RIGHT * 0.1), FadeIn(t2, shift=RIGHT * 0.1), run_time=0.6)
        self.at("not enough")
        ne = T("one loop was not enough", 34, RED, weight=BOLD).move_to(P(3.5, -2.4))
        self.play(FadeIn(ne, scale=0.9), run_time=0.6)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        g = dict(centres=[None, None, None, (-2.9, -0.05)], w=7.6, h=6.5, ts=28, yl="NGF share", lm=0.95, tm=1.4, two=False)
        pn = make_panel(3, g)
        pn["title"].move_to(P(-2.9 - 3.8 + 0.25 + pn["title"].width / 2, 2.55))
        cur = colour_curves(panel_curves(3, pn["box"], sw=3.0), 3)
        sch = T("schematic, not the published curves", 26, GOLD)
        left_at(sch, -2.9 - 3.8 + 0.25, 2.05)
        card = RoundedRectangle(corner_radius=0.2, width=5.4, height=4.6, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.07).move_to(P(3.95, 0.0))
        ctitle = T("published simulations", 30, GOLD, weight=BOLD).move_to(P(3.95, 1.7))
        body1 = T("two loops together", 34, TEXT).move_to(P(3.95, 0.5))
        body2 = T("separated winners\nfrom losers", 34, TEXT, t2c={"winners": GREEN, "losers": RED}, line_spacing=0.9
                  ).move_to(P(3.95, -0.8))
        self.at("published simulations")
        self.play(FadeIn(card), FadeIn(ctitle), FadeIn(pn["shell"]), FadeIn(pn["title"]), FadeIn(sch), run_time=0.7)
        self.at("two loops")
        self.play(FadeIn(body1), *[Create(m, rate_func=linear) for m in cur], run_time=1.5)
        self.at("winners from")
        self.play(FadeIn(body2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the four stages
SX = [-5.0, -1.65, 1.65, 5.0]
SCY = 0.0
SW, SH = 3.2, 5.8
STAGE_TITLES = ["Naive", "Sensitization", "Competitive\nadvantage", "Selection"]
GW = 2.7
BH = 0.5
NEUR_Y = 1.0
TITLE_TOP = 2.7
# row y positions per stage: label then bar
ROWS = {0: dict(l1=-0.7, g1=-1.4),
        1: dict(l1=0.0, g1=-0.45, tl=-1.05, l2=-1.65, g2=-2.15),
        2: dict(l1=-0.1, g1=-0.55, l2=-1.4, g2=-1.95),
        3: dict()}


def stage(i, final):
    """Build stage box i. final=True: the finished box. final=False: start state, with handles for the scene."""
    cx = SX[i]
    d = {}
    R = ROWS[i]
    d["box"] = RoundedRectangle(corner_radius=0.15, width=SW, height=SH, stroke_color=GREY, stroke_width=2.5,
                                fill_color=GREY, fill_opacity=0.05).move_to(P(cx, SCY))
    d["num"] = T(str(i + 1), 90, GREY, weight=BOLD).set_opacity(0.22).move_to(P(cx, SCY))
    ttl = T(STAGE_TITLES[i], 26, TEXT, weight=BOLD, line_spacing=0.8)
    d["title"] = ttl.move_to(P(cx, TITLE_TOP - ttl.height / 2))
    XLg = cx - GW / 2
    if i == 0:
        d["neuron"] = soma(P(cx, NEUR_Y), BLUE, 0.45, 0.85)
        d["dots"] = VGroup(ngf_dot(P(cx - 1.1, NEUR_Y + 0.3), 0.14), ngf_dot(P(cx + 1.1, NEUR_Y - 0.4), 0.14))
        d["l1"] = T("NGF response", 26, GREY).move_to(P(cx, R["l1"]))
        d["g1f"] = bar_frame(XLg, R["g1"], GW, 0.6)
        d["g1"] = bar_fill(XLg, R["g1"], GW, 0.12, PINK, 0.6)
    elif i == 1:
        d["neuron"] = soma(P(cx, NEUR_Y), BLUE, 0.62 if final else 0.4, 0.85)
        d["l1"] = T("NGF received", 26, YELLOW).move_to(P(cx, R["l1"]))
        d["g1f"] = bar_frame(XLg, R["g1"], GW, BH)
        d["g1"] = bar_fill(XLg, R["g1"], GW, 0.9 if final else 0.0, YELLOW, BH)
        mx = XLg + 0.6 * GW
        d["mark"] = DashedLine(P(mx, R["g1"] - 0.27), P(mx, R["g1"] + 0.27), color=TEXT, stroke_width=3, dash_length=0.07)
        d["tl"] = T("threshold", 26, TEXT).move_to(P(mx, R["tl"]))
        d["l2"] = T("sensitivity", 26, PINK).move_to(P(cx, R["l2"]))
        d["g2f"] = bar_frame(XLg, R["g2"], GW, BH)
        d["g2"] = bar_fill(XLg, R["g2"], GW, 0.85 if final else 0.12, PINK, BH)
    elif i == 2:
        d["neuron"] = soma(P(cx, NEUR_Y - 0.05), BLUE, 0.7 if final else 0.48, 0.85)
        d["l1"] = T("TrkA level", 26, PURPLE).move_to(P(cx, R["l1"]))
        d["g1f"] = bar_frame(XLg, R["g1"], GW, BH)
        d["g1"] = bar_fill(XLg, R["g1"], GW, 0.85 if final else 0.3, PURPLE, BH)
        d["l2"] = T("downstream", 26, PINK).move_to(P(cx, R["l2"]))
        d["g2f"] = bar_frame(XLg, R["g2"], GW, BH)
        d["g2"] = bar_fill(XLg, R["g2"], GW, 0.85 if final else 0.25, PINK, BH)
    else:
        d["neuron"] = soma(P(cx, NEUR_Y - 0.05), GREEN, 0.8, 0.85) if final else soma(P(cx, NEUR_Y - 0.05), BLUE, 0.5, 0.85)
        if final:
            d["nb"] = VGroup(*[soma(P(cx + dx, -1.8), RED, 0.45, 0.3) for dx in (-0.75, 0.75)])
        else:
            d["nb"] = VGroup(*[soma(P(cx + dx, -1.8), BLUE_B, 0.45, 0.5) for dx in (-0.75, 0.75)])
    order = [k for k in ("neuron", "dots", "nb", "l1", "g1f", "g1", "mark", "tl", "l2", "g2f", "g2") if k in d]
    d["all"] = VGroup(d["box"], d["title"], *[d[k] for k in order])
    return d


def finished(i):
    return stage(i, True)["all"]


def stage_box_only(i):
    d = stage(i, False)
    return VGroup(d["box"], d["num"])


class S19(SpokenScene):
    def construct(self):
        boxes = [stage_box_only(i) for i in range(4)]
        self.add(*boxes)
        self.at("four stages")
        self.play(LaggedStart(*[Indicate(b[1], color=TEXT, scale_factor=1.25) for b in boxes], lag_ratio=0.2), run_time=1.2)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        boxes = [stage_box_only(i) for i in range(4)]
        self.add(*boxes)
        d = stage(0, False)
        self.at("naive")
        self.play(FadeIn(d["title"], shift=DOWN * 0.1), FadeOut(boxes[0][1]), run_time=0.5)
        self.at("young neuron")
        self.play(FadeIn(d["neuron"], scale=0.5), FadeIn(d["dots"], scale=0.4), run_time=0.7)
        self.at("responds poorly")
        self.play(FadeIn(d["l1"]), FadeIn(d["g1f"]), run_time=0.4)
        self.play(GrowFromEdge(d["g1"], LEFT), run_time=0.7)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        boxes = [stage_box_only(i) for i in range(4)]
        self.add(*boxes[1:], finished(0))
        d = stage(1, False)
        self.at("sensitization")
        self.play(FadeIn(d["title"], shift=DOWN * 0.1), FadeOut(boxes[1][1]), FadeIn(d["neuron"], scale=0.5), run_time=0.6)
        self.at("gets enough")
        self.play(FadeIn(d["l1"]), FadeIn(d["g1f"]), FadeIn(d["mark"]), run_time=0.4)
        self.play(Transform(d["g1"], bar_fill(SX[1] - GW / 2, ROWS[1]["g1"], GW, 0.9, YELLOW, BH)),
                  run_time=1.3, rate_func=linear)
        self.at("threshold")
        self.play(FadeIn(d["tl"]), Indicate(d["mark"], color=GOLD, scale_factor=1.6), run_time=0.7)
        self.at("from then on")
        g2 = bar_fill(SX[1] - GW / 2, ROWS[1]["g2"], GW, 0.12, PINK, BH)
        self.play(FadeIn(d["l2"]), FadeIn(d["g2f"]), FadeIn(g2), run_time=0.5)
        self.at("more sensitive")
        self.play(Transform(g2, bar_fill(SX[1] - GW / 2, ROWS[1]["g2"], GW, 0.85, PINK, BH)),
                  d["neuron"].animate.scale(0.62 / 0.4), run_time=1.6)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        boxes = [stage_box_only(i) for i in range(4)]
        self.add(*boxes[2:], finished(0), finished(1))
        d = stage(2, False)
        cx = SX[2]
        self.at("competitive advantage")
        self.play(FadeIn(d["title"], shift=DOWN * 0.1), FadeOut(boxes[2][1]), run_time=0.5)
        self.at("it raises")
        self.play(FadeIn(d["neuron"], scale=0.5), FadeIn(d["l1"]), FadeIn(d["g1f"]), FadeIn(d["g1"]), run_time=0.6)
        self.play(Transform(d["g1"], bar_fill(cx - GW / 2, ROWS[2]["g1"], GW, 0.85, PURPLE, BH)),
                  d["neuron"].animate.scale(0.7 / 0.48), run_time=1.0)
        self.at("strengthens")
        self.play(FadeIn(d["l2"]), FadeIn(d["g2f"]), FadeIn(d["g2"]), run_time=0.5)
        self.at("downstream")
        self.play(Transform(d["g2"], bar_fill(cx - GW / 2, ROWS[2]["g2"], GW, 0.85, PINK, BH)), run_time=1.1)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        boxes = [stage_box_only(i) for i in range(4)]
        self.add(boxes[3], finished(0), finished(1), finished(2))
        d = stage(3, False)
        cx = SX[3]
        self.at("selection")
        self.play(FadeIn(d["title"], shift=DOWN * 0.1), FadeOut(boxes[3][1]), FadeIn(d["neuron"], scale=0.5), run_time=0.5)
        self.at("wins the supply")
        ins = VGroup(*[ngf_dot(P(cx + dx, NEUR_Y + dy), 0.14) for dx, dy in [(-1.1, 0.7), (1.1, 0.5), (-1.0, -0.6)]])
        self.play(FadeIn(ins, scale=0.4), run_time=0.4)
        self.play(*[m.animate.move_to(d["neuron"].get_center()).set_opacity(0.0) for m in ins],
                  d["neuron"].animate.scale(0.8 / 0.5).set_stroke(GREEN).set_fill(GREEN, 0.85), run_time=1.0)
        self.at("neighbors")
        self.play(*[FadeIn(m, scale=0.5) for m in d["nb"]], run_time=0.4)
        self.at("lose")
        self.play(*[m.animate.set_stroke(RED, opacity=0.5).set_fill(RED, opacity=0.25) for m in d["nb"]], run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
WIN_Y = [P(-5.1, 1.5), P(-3.3, -0.1), P(-5.1, -1.7)]
LOS_Y = [P(5.1, 1.5), P(3.3, -0.1), P(5.1, -1.7)]


class S24(SpokenScene):
    def construct(self):
        w0 = [P(-3.7, 1.5), P(-2.3, -0.1), P(-3.7, -1.7)]
        l0 = [P(3.7, 1.5), P(2.3, -0.1), P(3.7, -1.7)]
        ws = VGroup(*[soma(p, GREEN, 0.65, 0.85) for p in w0])
        ls = VGroup(*[soma(p, RED, 0.5, 0.55) for p in l0])
        chip1 = chip("one more piece", GOLD, 32, 0.18).move_to(P(0, 3.2))
        self.play(FadeIn(ws, scale=0.6), FadeIn(ls, scale=0.6), FadeIn(chip1, shift=DOWN * 0.1), run_time=0.5)
        self.at("speeds the split")
        anims = []
        for k in range(3):
            anims += [ws[k].animate.move_to(WIN_Y[k]), ls[k].animate.move_to(LOS_Y[k]).set_fill(RED, 0.3).set_stroke(RED, opacity=0.6)]
        self.play(*anims, run_time=1.2)
        self.at("next chapter")
        a = arr(P(-1.9, -0.1), P(2.7, -0.1), GREY, 6, 0.3)
        q = T("?", 110, GOLD, weight=BOLD).move_to(P(0.4, 0.95))
        self.play(ws[1].animate.scale(1.5), GrowArrow(a), FadeIn(q, scale=0.4), run_time=0.9)
        self.at("winners treat")
        wl = T("winners", 34, GREEN).move_to(P(-4.4, -3.15))
        ll = T("losers", 34, RED).move_to(P(4.4, -3.15))
        self.play(FadeIn(wl), FadeIn(ll), run_time=0.6)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        tk = T("Takeaway", 64, GOLD, weight=BOLD).move_to(P(0, 0.2))
        self.play(FadeIn(tk), run_time=0.4)
        self.at("ngf")
        nchip = chip("NGF", YELLOW, 44).move_to(P(-5.4, 0.1))
        self.play(tk.animate.scale(0.6).move_to(P(-4.4, 3.3)), FadeIn(nchip, scale=0.8), run_time=0.6)
        self.at("raises")
        a1 = arr(P(-4.8, 0.5), P(-4.1, 1.35), YELLOW, 5, 0.22)
        self.play(GrowArrow(a1), run_time=0.3)
        self.at("receptor level")
        lv = chip("receptor level", PURPLE, 32).move_to(P(-2.6, 1.7))
        self.play(FadeIn(lv, shift=RIGHT * 0.2), run_time=0.4)
        self.at("and signal")
        a2 = arr(P(-4.8, -0.3), P(-4.1, -1.15), YELLOW, 5, 0.22)
        self.play(GrowArrow(a2), run_time=0.3)
        self.at("signal duration")
        du = chip("signal duration", PINK, 32).move_to(P(-2.6, -1.5))
        self.play(FadeIn(du, shift=RIGHT * 0.2), run_time=0.4)
        self.at("published model")
        PX = 4.0
        panel = RoundedRectangle(corner_radius=0.2, width=4.8, height=6.7, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.07).move_to(P(PX, -0.1))
        pm = T("published model", 30, GREY).move_to(P(PX, 2.85))
        cols = [PX - 1.3, PX, PX + 1.3]
        pos = [P(x, 0.55) for x in cols] + [P(x, -0.75) for x in cols]
        ns = VGroup(*[soma(p, BLUE, 0.45, 0.85) for p in pos])
        self.play(FadeIn(panel), FadeIn(pm), FadeIn(ns, scale=0.6), run_time=0.6)
        self.at("only the two")
        bx = -0.3
        br = VGroup(Line(P(bx - 0.4, 1.7), P(bx, 1.7), color=TEXT, stroke_width=5),
                    Line(P(bx - 0.4, -1.5), P(bx, -1.5), color=TEXT, stroke_width=5),
                    Line(P(bx, 1.7), P(bx, -1.5), color=TEXT, stroke_width=5),
                    arr(P(bx, 0.1), P(1.45, 0.1), TEXT, 5, 0.25))
        tg = T("together", 26, TEXT).move_to(P(bx + 1.05, 0.6))
        self.play(FadeIn(br), FadeIn(tg), run_time=0.5)
        self.at("split the neurons")
        wp = [P(x, 1.5) for x in cols]
        lp = [P(x, -2.0) for x in cols]
        anims = []
        for k in range(3):
            anims += [ns[k].animate.move_to(wp[k]).scale(1.25).set_stroke(GREEN).set_fill(GREEN, 0.9),
                      ns[3 + k].animate.move_to(lp[k]).scale(0.8).set_stroke(RED).set_fill(RED, 0.25)]
        self.play(*anims, run_time=1.0)
        wl = T("winners", 28, GREEN, weight=BOLD).move_to(P(PX, 0.55))
        ll = T("losers", 28, RED, weight=BOLD).move_to(P(PX, -2.85))
        self.play(FadeIn(wl), FadeIn(ll), run_time=0.4)
        self.wait(2.8)
        self.finish()


class S26End(EndCard):
    LINE = "Only feedback on both level and duration split the neurons."
