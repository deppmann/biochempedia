"""Chapter 4 of 6: Level and Time  (Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by every chapter of this lesson; from scenes.old.py and chapters 2 and 3)
  YELLOW = Sonic hedgehog (Shh), the level of signal, and the signaling (Gli activity) it causes
  TEAL   = notochord and floor plate (the source tissue)
  BLUE   = motor neurons (the pMN domain) and their markers (deeper blue "#5C8DF0", distinct from TEAL)
  PINK ramp = the ventral interneuron domains p0, p1, p2 (V0 to V2): palest = p0, deepest = p2 (more ventral = deeper)
  ORANGE = p3 (V3), the domain beside the floor plate, as in chapter 3.  No other use of orange in this chapter.
  RED    = repression (T-bars, cyclopamine's block) and nothing else
  PURPLE = Patched (the brake)
  GREEN  = "on": active Smoothened
  GOLD   = the address, "predict", credit cards
  TEXT   = neutral things, and TIME (clocks, bars of time, the working-level line)
  GREY   = tube wall, neutral cells, axes, "off"

Model for every curve (the lesson's own, in ShhGradientReadout.astro): signaling rate = c * exp(-t / tau(c)),
tau(c) = 8 * (1 + c / 2). A higher dose c has a longer tau, so it keeps signaling going longer.
The history of signaling is the area under that curve.  Time on the plots is in the lesson's relative units.
The dashed "working level" is a fixed line (WL = 1.0 on the rate axis): a cell is still signaling while its
trace is above it.  The low dose (c = 2) crosses it at t = tau * ln(2 / WL); the high dose (c = 8) is still above it at the end.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BLUE = "#5C8DF0"   # a deeper blue than the house BLUE, so motor neurons never read as the teal floor plate
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK0, PINK1, PINK2 = "#EAC9E2", "#E5A0CF", "#E0589F"   # p0 (palest), p1, p2 (deepest): a ventral-ward ramp

LESSON = "Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube"


# ---------------------------------------------------------------------------------------------
# small helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def TL(text, size=30, color=TEXT, gap=0.12, **kw):
    """centred multi-line text (Manim left-aligns the lines of one Text)"""
    return VGroup(*[T(l, size, color, **kw) for l in text.split("\n")]).arrange(DOWN, buff=gap * size / 30)


def smoothstep(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


class Scn(SpokenScene):
    def after(self, phrase, dt, nth=0):
        """wait until `dt` seconds after the narrator starts `phrase` (for names a transcriber may spell differently)."""
        rest = self.t_of(phrase, nth) + dt - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


# ---------------------------------------------------------------------------------------------
# the lesson's model
def tau_of(c):
    return 8 * (1 + c / 2)


def rate(c, t):
    return c * np.exp(-t / tau_of(c))


def total(c, T):
    return c * tau_of(c) * (1 - np.exp(-T / tau_of(c)))


WL = 1.0


def cross_t(c):
    """time at which the signaling rate of dose c falls to the working level"""
    return tau_of(c) * np.log(c / WL)


ZONES = [("dorsal", "stays dorsal", 0.0, GREY), ("p0", "V0 interneurons", 0.3, PINK0), ("p1", "V1 interneurons", 0.8, PINK1),
         ("p2", "V2 interneurons", 1.6, PINK2), ("pMN", "motor neurons", 3.0, BLUE), ("p3", "V3 interneurons", 8.0, ORANGE)]


def zone_of(s):
    z = ZONES[0]
    for zz in ZONES:
        if s >= zz[2]:
            z = zz
    return z


# ---------------------------------------------------------------------------------------------
# icons: the dial (level) and the clock (time)
class Dial(VGroup):
    A0, SPAN = 210 * DEGREES, 240 * DEGREES

    def __init__(self, cx, cy, r=1.7, color=YELLOW, value=0.3, needle=True):
        super().__init__()
        self.c = np.array([cx, cy, 0.0])
        self.r = r
        self.value = value
        rim = Arc(radius=r, start_angle=self.A0, angle=-self.SPAN, arc_center=self.c, stroke_color=color, stroke_width=8)
        ticks = VGroup()
        for v in np.linspace(0, 1, 9):
            a = self.A0 - self.SPAN * v
            u = np.array([np.cos(a), np.sin(a), 0])
            ticks.add(Line(self.c + u * r * 0.80, self.c + u * r * 0.93, stroke_color=color, stroke_width=4, stroke_opacity=0.8))
        self.hub = Dot(self.c, radius=0.11 * r / 1.4, color=color)
        a = self.A0 - self.SPAN * value
        self.needle = Line(self.c, self.c + 0.78 * r * np.array([np.cos(a), np.sin(a), 0]), stroke_color=color, stroke_width=8)
        self.add(rim, ticks)
        if needle:
            self.add(self.needle, self.hub)

    def turn_to(self, v):
        dv = v - self.value
        self.value = v
        return Rotate(self.needle, angle=-self.SPAN * dv, about_point=self.c)


class Clock(VGroup):
    def __init__(self, cx, cy, r=1.5, color=TEXT, frac=0.0, hand=True, wedge=False):
        super().__init__()
        self.c = np.array([cx, cy, 0.0])
        self.r = r
        face = Circle(radius=r, stroke_color=color, stroke_width=6, fill_color=color, fill_opacity=0.06).move_to(self.c)
        ticks = VGroup()
        for k in range(12):
            a = PI / 2 - k * TAU / 12
            u = np.array([np.cos(a), np.sin(a), 0])
            ln = 0.2 if k % 3 == 0 else 0.1
            ticks.add(Line(self.c + u * (r - ln - 0.04), self.c + u * (r - 0.04), stroke_color=color, stroke_width=4 if k % 3 == 0 else 3))
        self.add(face, ticks)
        self.wedge = None
        if wedge and frac > 0:
            self.wedge = Sector(radius=r * 0.88, start_angle=PI / 2, angle=-TAU * frac, arc_center=self.c,
                                fill_color=color, fill_opacity=0.35, stroke_width=0)
            self.add(self.wedge)
        a = PI / 2 - TAU * frac
        self.hand = Line(self.c, self.c + 0.78 * r * np.array([np.cos(a), np.sin(a), 0]), stroke_color=color, stroke_width=7)
        self.hub = Dot(self.c, radius=0.1 * r / 1.5, color=color)
        if hand:
            self.add(self.hand, self.hub)


# ---------------------------------------------------------------------------------------------
# the neural tube map (cross-section, dorsal up), shared with every chapter
DOM_COLOR = {"p3": ORANGE, "pMN": BLUE, "p2": PINK2, "p1": PINK1, "p0": PINK0}


class Tube:
    def __init__(self, cx=0.0, cy=0.0, W=4.8, H=4.8, N=24, cr=0.15, rings=(0.55, 0.78), nr=0.38):
        self.cx, self.cy, self.W, self.H, self.nr = cx, cy, W, H, nr
        self.outer = Ellipse(width=W, height=H, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.07).move_to([cx, cy, 0])
        self.canal = Ellipse(width=0.34 * W, height=0.34 * H, stroke_color=GREY, stroke_width=2.5,
                             fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
        self.cells, self.info = VGroup(), []
        for i in range(N):
            th = -PI / 2 + (i + 0.5) * 2 * PI / N
            m = -np.sin(th)
            if m <= 0:
                dom = "dorsal"
            elif m > 0.96:
                dom = "p3"
            elif m > 0.7:
                dom = "pMN"
            elif m > 0.5:
                dom = "p2"
            elif m > 0.25:
                dom = "p1"
            else:
                dom = "p0"
            for rho in rings:
                c = Circle(radius=cr, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.3)
                c.move_to([cx + rho * W / 2 * np.cos(th), cy + rho * H / 2 * np.sin(th), 0])
                self.cells.add(c)
                self.info.append((dom, np.cos(th)))
        self.epi = ParametricFunction(lambda t: np.array([cx + (W / 2 + 0.3) * np.cos(t), cy + (H / 2 + 0.3) * np.sin(t), 0]),
                                      t_range=[PI * 0.27, PI * 0.73], stroke_color=GREY, stroke_width=5).set_stroke(opacity=0.7)
        self.roof = RoundedRectangle(corner_radius=0.06, width=0.9 * W / 4.8, height=0.2, stroke_color=TEXT, stroke_width=2.5,
                                     fill_color=TEXT, fill_opacity=0.35).move_to([cx, cy + H / 2 - 0.17, 0])
        self.fp = RoundedRectangle(corner_radius=0.06, width=0.9 * W / 4.8, height=0.2, stroke_color=TEAL, stroke_width=3,
                                   fill_color=TEAL, fill_opacity=0.6).move_to([cx, cy - H / 2 + 0.17, 0])
        self.noto = Circle(radius=nr, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35
                           ).move_to([cx, cy - H / 2 - 0.1 - nr, 0])

    def group(self, noto=True, epi=True):
        g = VGroup(self.outer, self.canal, self.cells, self.roof, self.fp)
        if epi:
            g.add(self.epi)
        if noto:
            g.add(self.noto)
        return g

    def sel(self, dom=None, side=None):
        dom = [dom] if isinstance(dom, str) else dom
        out = []
        for c, (d, cs) in zip(self.cells, self.info):
            if (dom is None or d in dom) and (side is None or np.sign(cs) == side):
                out.append(c)
        return out

    def outer_cell(self, dom, side=+1, nth=0):
        """one OUTER-ring cell of this domain on the given side (nth from the ventral end)"""
        cand = [(k, c) for k, (c, (d, cs)) in enumerate(zip(self.cells, self.info)) if d == dom and np.sign(cs) == side and k % 2 == 1]
        cand.sort(key=lambda kc: kc[1].get_center()[1])
        return cand[min(nth, len(cand) - 1)][1]

    def paint(self, doms):
        for c, (d, _) in zip(self.cells, self.info):
            if d in doms and d in DOM_COLOR:
                c.set_stroke(DOM_COLOR[d]).set_fill(DOM_COLOR[d], 0.6)

    def recolor(self, doms):
        """animations that give the cells of these domains their identity colour"""
        out = []
        for c, (d, _) in zip(self.cells, self.info):
            if d in doms:
                out.append(c.animate.set_stroke(DOM_COLOR[d]).set_fill(DOM_COLOR[d], 0.6))
        return out


def explant(cx, cy, s=1.0, color=GREY, o=0.35):
    """a 3x3 explant of identical cells (same shape every time it is drawn)"""
    out = VGroup()
    for dy in (0.39, 0.0, -0.39):
        for dx in (-0.39, 0.0, 0.39):
            out.add(Circle(radius=0.185 * s, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=o)
                    .move_to([cx + dx * s, cy + dy * s, 0]))
    return out


# ---------------------------------------------------------------------------------------------
# the cell, membrane and brake (chapters 2 and 4): the stage fills the frame
MEM_Y = 1.3
P_SLOTS = [-0.9, -2.05, -3.2, -4.35, -5.5]
S_X = 3.8
BLK_H = 2.6
SHH_Y = 3.15
BAR_Y = 2.05


def cell_body():
    body = RoundedRectangle(corner_radius=0.5, width=12.4, height=5.0, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.06).move_to([0, -1.2, 0])
    mem = RoundedRectangle(corner_radius=0.18, width=12.4, height=0.5, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.35).move_to([0, MEM_Y, 0])
    return VGroup(body, mem)


def p_block(k, o=0.45):
    return RoundedRectangle(corner_radius=0.15, width=1.0, height=BLK_H, stroke_color=PURPLE, stroke_width=4,
                            fill_color=PURPLE, fill_opacity=o).move_to([P_SLOTS[k], MEM_Y, 0])


def s_block(on=False, o=None):
    col = GREEN if on else GREY
    return RoundedRectangle(corner_radius=0.15, width=1.4, height=BLK_H, stroke_color=col, stroke_width=4,
                            fill_color=col, fill_opacity=(0.6 if on else 0.3) if o is None else o).move_to([S_X, MEM_Y, 0])


def brake_bar(w=6):
    return inhib([P_SLOTS[0] + 0.55, BAR_Y, 0], [S_X - 0.75, BAR_Y, 0], RED, w)


def lab_p(x=None):
    return T("Patched", 26, PURPLE, weight=BOLD).move_to([P_SLOTS[0] if x is None else x, -0.4, 0])


def lab_s():
    return T("Smoothened", 26, TEXT, weight=BOLD).move_to([S_X, -0.4, 0])


def state_chip(txt, col):
    return T(txt, 28, col, weight=BOLD).move_to([S_X, -0.88, 0])


def shh_chip(y=SHH_Y):
    return chip("Sonic hedgehog", YELLOW, 28, pad=0.18).move_to([P_SLOTS[0], y, 0])


def shh_dot(k, y=2.95, r=0.16):
    return Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=0.97).move_to([P_SLOTS[k], y, 0])


GAUGE_X0, GAUGE_W, GAUGE_Y = -5.85, 4.4, -2.0


def gauge(val):
    """brake strength as a bar; val is a ValueTracker (0 to 1)"""
    frame = Rectangle(width=GAUGE_W, height=0.46, stroke_color=PURPLE, stroke_width=3, fill_opacity=0
                      ).move_to([GAUGE_X0 + GAUGE_W / 2, GAUGE_Y, 0])
    fill = always_redraw(lambda: Rectangle(width=max(GAUGE_W * val.get_value(), 0.02), height=0.46, stroke_width=0,
                                           fill_color=PURPLE, fill_opacity=0.85).move_to(
        [GAUGE_X0 + max(GAUGE_W * val.get_value(), 0.02) / 2, GAUGE_Y, 0]))
    lab = T("brake strength", 26, PURPLE).next_to(frame, UP, buff=0.12, aligned_edge=LEFT)
    return frame, fill, lab


def nucleus():
    return Ellipse(width=8.4, height=1.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([0, -2.6, 0])


def gene_chip():
    return chip("Patched1 gene", PURPLE, 26).move_to([-0.2, -2.7, 0])


def gli_chip():
    return chip("Gli", YELLOW, 26).move_to([3.7, -1.95, 0])


# ---------------------------------------------------------------------------------------------
# two cells and their traces (the heart of the chapter)
C_LO, C_HI = 2.0, 8.0
CS = (C_LO, C_HI)
CXS = (-3.55, 3.55)
CELL_Y = 2.8
CELL_W, CELL_H = 3.2, 1.6
AX_Y = -1.05
AX_W, AX_H = 5.8, 3.3
TMAX, YMAX = 40.0, 8.6
SLOT_ORDER = [4, 2, 6, 3, 5, 1, 7, 0, 8]
SLOT_DEG = [-160 + 17.5 * k for k in range(9)]


def cell_pt(cx, deg, off=0.0):
    a = deg * DEGREES
    return np.array([cx + (CELL_W / 2 + off) * np.cos(a), CELL_Y + (CELL_H / 2 + off) * np.sin(a), 0])


def cell_dots(cx, n):
    if n <= 3:
        specs = [(65, 0.3), (90, 0.3), (115, 0.3)]
    else:
        specs = [(40, 0.3), (65, 0.3), (90, 0.3), (115, 0.3), (140, 0.3), (52, 0.58), (78, 0.58), (102, 0.58), (128, 0.58)]
    return VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.97).move_to(cell_pt(cx, d, o)) for d, o in specs])


def patched_blocks(cx):
    out = []
    for slot in SLOT_ORDER:
        deg = SLOT_DEG[slot]
        b = RoundedRectangle(corner_radius=0.05, width=0.22, height=0.46, stroke_color=PURPLE, stroke_width=2.5,
                             fill_color=PURPLE, fill_opacity=0.75)
        b.rotate((deg + 90) * DEGREES).move_to(cell_pt(cx, deg))
        out.append(b)
    return out


def make_axes(cx):
    return Axes(x_range=[0, TMAX], y_range=[0, YMAX], x_length=AX_W, y_length=AX_H, tips=False,
                axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False}).move_to([cx, AX_Y, 0])


class TwoView:
    def __init__(self, T0=0.0):
        self.Tt = ValueTracker(T0)
        self.cells, self.axes, self.pb, self.dots, self.dose = [], [], [], [], []
        self.ylab, self.xlab, self.traces, self.heads, self.wl, self.wll = [], [], [], [], [], []
        for i, (cx, c) in enumerate(zip(CXS, CS)):
            self.cells.append(Ellipse(width=CELL_W, height=CELL_H, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1
                                      ).move_to([cx, CELL_Y, 0]))
            ax = make_axes(cx)
            self.axes.append(ax)
            self.ylab.append(T("Gli activity", 26, GREY).move_to([ax.c2p(0, 0)[0], 0.9, 0], aligned_edge=LEFT))
            self.xlab.append(T("time", 26, GREY).move_to([ax.c2p(TMAX, 0)[0] - 0.45, AX_Y - AX_H / 2 - 0.3, 0]))
            self.pb.append(patched_blocks(cx))
            self.dots.append(cell_dots(cx, 3 if i == 0 else 9))
            self.dose.append(T("low dose" if i == 0 else "high dose", 30, YELLOW, weight=BOLD).move_to([cx, 1.4, 0]))
            self.traces.append(always_redraw(lambda i=i: self._trace(i)))
            self.heads.append(always_redraw(lambda i=i: self._head(i)))
            self.wl.append(DashedLine(ax.c2p(0, WL), ax.c2p(TMAX, WL), color=TEXT, stroke_width=3, dash_length=0.14).set_stroke(opacity=0.9))
            self.wll.append(T("working level", 26, TEXT).move_to(ax.c2p(TMAX, WL) + LEFT * 1.25 + UP * 0.33))

    def _tt(self):
        return max(self.Tt.get_value(), 0.25)

    def _trace(self, i):
        c, ax, t1 = CS[i], self.axes[i], self._tt()
        return ax.plot(lambda t: rate(c, t), x_range=[0, t1, max(t1 / 80, 0.05)], color=YELLOW, stroke_width=7 if i else 6)

    def _head(self, i):
        t1 = self._tt()
        return Dot(self.axes[i].c2p(t1, rate(CS[i], t1)), radius=0.11, color=YELLOW)

    def fill_op(self, i):
        return 0.08 + 0.75 * rate(CS[i], self.Tt.get_value()) / 8.0

    def go_live(self, i, anim=True):
        """give the cell its dose colour and make it follow the signaling from now on"""
        def upd(m, i=i):
            m.set_fill(YELLOW, opacity=self.fill_op(i)).set_stroke(YELLOW)
        cell = self.cells[i]
        if anim:
            return cell.animate.set_fill(YELLOW, opacity=self.fill_op(i)).set_stroke(YELLOW), upd
        upd(cell)
        cell.add_updater(upd)
        return None, upd

    def live_all(self):
        for i in (0, 1):
            self.go_live(i, anim=False)

    def pb_group(self, i, n):
        return VGroup(*self.pb[i][:n])


def two_frame(sc, T0, npatch, dots=True, wl=False):
    """put the whole two-cell frame on screen, in the state it has at time T0"""
    v = TwoView(T0)
    v.live_all()
    sc.add(*v.cells, *v.axes, *v.ylab, *v.xlab, *v.dose, *v.traces, *v.heads)
    for i in (0, 1):
        sc.add(v.pb_group(i, npatch))
        if dots:
            sc.add(v.dots[i])
    if wl:
        sc.add(*v.wl, *v.wll)
    return v


# ---------------------------------------------------------------------------------------------
# credit cards (text centred, the card filled)
def credit(year, names, sub):
    card = RoundedRectangle(corner_radius=0.3, width=11.4, height=6.6, stroke_color=GOLD, stroke_width=5,
                            fill_color=GOLD, fill_opacity=0.06).move_to([0, 0, 0])
    yr = T(year, 100, GOLD, TITLE_FONT, BOLD).move_to([0, 2.15, 0])
    nm = TL(names, 52, TEXT, gap=0.18).move_to([0, 0.45, 0])
    sb = T(sub, 42, GREY).move_to([0, -1.05, 0])
    return card, yr, nm, sb


# =============================================================================================
class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "Level and Time"


# ---------------------------------------------------------------------------------------------
class S01Q(Scn):
    def construct(self):
        dial = Dial(-3.3, 0.6, 1.9, YELLOW, value=0.15)
        clock = Clock(3.3, 0.6, 1.9, TEXT, frac=0.0)
        q1 = T("how much Shh?", 44, YELLOW, weight=BOLD).move_to([-3.3, -2.0, 0])
        q2 = T("time?", 44, TEXT, weight=BOLD).move_to([3.3, -2.0, 0])
        self.play(FadeIn(dial, scale=0.9), run_time=0.7)
        self.at("how much")
        self.play(dial.turn_to(0.8), FadeIn(q1, shift=UP * 0.1), run_time=1.4)
        self.at("does time")
        self.play(FadeIn(clock, scale=0.9), run_time=0.6)
        self.play(Rotate(clock.hand, angle=-TAU * 0.6, about_point=clock.c), FadeIn(q2, shift=UP * 0.1), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Half(Scn):
    def construct(self):
        dial = Dial(-3.3, 0.5, 1.9, YELLOW, value=0.8)
        clock = Clock(3.3, 0.6, 1.9, TEXT, frac=0.6)
        t_q = T("time?", 44, TEXT, weight=BOLD).move_to([3.3, -2.0, 0])
        self.add(dial, clock, t_q)
        l_c = T("concentration", 40, YELLOW, weight=BOLD).move_to([-3.3, 2.95, 0])
        self.at("Concentration")
        self.play(FadeIn(l_c, shift=DOWN * 0.1), run_time=0.6)
        self.at("only half")
        b1 = Brace(Line([-5.3, -1.75, 0], [-1.3, -1.75, 0]), DOWN, buff=0.1, color=YELLOW)
        t1 = T("half", 40, YELLOW).move_to([-3.3, -2.65, 0])
        self.play(GrowFromCenter(b1), FadeIn(t1), FadeOut(t_q), run_time=0.7)
        empty = Dial(3.3, 0.5, 1.9, GREY, needle=False)
        q = T("?", 110, GREY, weight=BOLD).move_to([3.3, 0.35, 0])
        self.after("only half", 0.55)
        self.play(FadeOut(clock), FadeIn(empty), FadeIn(q, scale=0.6), run_time=0.5)
        b2 = Brace(Line([1.3, -1.75, 0], [5.3, -1.75, 0]), DOWN, buff=0.1, color=GREY)
        t2 = T("part of the other half", 36, GREY).move_to([3.3, -2.65, 0])
        self.at("other half")
        self.play(GrowFromCenter(b2), FadeIn(t2), run_time=0.5)
        self.at("lies in")
        part = Arc(radius=1.9, start_angle=Dial.A0, angle=-Dial.SPAN * 0.55, arc_center=empty.c, stroke_color=PURPLE, stroke_width=14)
        brk = chip("the brake", PURPLE, 36).move_to([3.3, 3.12, 0])
        ar = arr([3.3, 2.62, 0], [3.3, 2.36, 0], PURPLE, 6, 0.2)
        self.play(Create(part), FadeIn(brk, shift=DOWN * 0.1), GrowArrow(ar), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Brake(Scn):
    def construct(self):
        body = cell_body()
        p0, s0 = p_block(0), s_block(False)
        lp, ls, st = lab_p(), lab_s(), state_chip("off", GREY)
        self.play(FadeIn(body), FadeIn(p0), FadeIn(s0), run_time=0.8)
        self.play(FadeIn(lp), FadeIn(ls), run_time=0.4)
        bar = brake_bar(7)
        ana = T("an analogy, not physical contact", 26, GREY).move_to([0.5, -1.7, 0])
        self.at("holds the pathway")
        self.play(Create(bar), FadeIn(ana, shift=UP * 0.1), FadeIn(st), run_time=0.9)
        shh = shh_chip(3.4)
        self.at("and sonic")
        self.play(FadeIn(shh, shift=DOWN * 0.1), run_time=0.5)
        self.at("lifts it")
        on = state_chip("on", GREEN)
        self.play(shh.animate.move_to([P_SLOTS[0], SHH_Y, 0]), p0.animate.set_stroke(YELLOW, width=6), FadeOut(bar), FadeOut(ana),
                  s0.animate.set_stroke(GREEN).set_fill(GREEN, 0.6), Transform(st, on), run_time=0.9)
        self.finish()


class S04Twist(Scn):
    def construct(self):
        body = cell_body()
        p0, s0 = p_block(0), s_block(True)
        shh = shh_chip()
        self.add(body, p0, s0, lab_p(), lab_s(), state_chip("on", GREEN), shh)
        nuc = nucleus()
        nlab = T("nucleus", 26, GREY).move_to([-3.2, -2.7, 0])
        self.at("the twist")
        self.play(FadeIn(nuc, shift=UP * 0.2), FadeIn(nlab), run_time=0.8)
        gc = gene_chip()
        self.at("also one")
        self.play(FadeIn(gc, scale=0.85), run_time=0.7)
        a1 = arr([S_X, -1.1, 0], [S_X, -1.5, 0], GREEN, 6, 0.2)
        gl = gli_chip()
        a2 = arr([3.4, -2.3, 0], [1.2, -2.68, 0], GREEN, 6, 0.22)
        self.at("sonic hedgehog")
        self.play(GrowArrow(a1), FadeIn(gl, scale=0.85), run_time=0.4)
        self.play(GrowArrow(a2), Indicate(gc, color=GREEN, scale_factor=1.08), run_time=0.5)
        loop = Arrow([-1.2, -2.33, 0], [P_SLOTS[1], -0.03, 0], buff=0.0, color=PURPLE, stroke_width=6, tip_length=0.28,
                     max_tip_length_to_length_ratio=0.3)
        new_p = p_block(1)
        self.at("turns on")
        self.play(GrowArrow(loop), run_time=0.7)
        self.play(FadeIn(new_p, scale=0.6), run_time=0.5)
        self.finish()


class S05Twist2(Scn):
    def construct(self):
        body = cell_body()
        p0, p1, s0 = p_block(0), p_block(1), s_block(True)
        shh = shh_chip()
        on = state_chip("on", GREEN)
        lp = lab_p(-1.5)
        self.add(body, p0, p1, s0, lp, lab_s(), on, shh)
        val = ValueTracker(0.25)
        gf, gfill, glab = gauge(val)
        c0 = T("backwards?", 56, TEXT, weight=BOLD).move_to([0.5, -3.2, 0])
        self.at("backwards")
        self.play(FadeIn(c0, scale=0.9), FadeIn(gf), FadeIn(glab), run_time=0.6)
        self.add(gfill)
        c1 = T("more receptor, more sensitive?", 48, TEXT).move_to([0.5, -3.2, 0])
        p2 = p_block(2)
        self.at("more receptor")
        self.play(Transform(c0, c1), FadeIn(p2, scale=0.6), lp.animate.move_to([-2.05, -0.4, 0]), val.animate.set_value(0.4), run_time=0.8)
        c2 = T("Patched is a brake.", 56, PURPLE, weight=BOLD).move_to([0.5, -3.2, 0])
        self.at("But")
        self.play(Transform(c0, c2), run_time=0.3)
        bar = brake_bar(9)
        less = state_chip("less on", GREEN)
        self.at("patched is")
        self.remove(on)
        self.play(Create(bar, lag_ratio=0.8), s0.animate.set_fill(GREEN, 0.3), FadeIn(less), run_time=0.9)
        self.finish()


class S06Twist3(Scn):
    def construct(self):
        body = cell_body()
        blocks = [p_block(k) for k in range(3)]
        s0 = s_block(True, 0.3)
        bar = brake_bar(9)
        shh = shh_chip()
        lp = lab_p(-2.05)
        st = state_chip("less on", GREEN)
        val = ValueTracker(0.4)
        gf, gfill, glab = gauge(val)
        self.add(body, *blocks, s0, lp, lab_s(), st, bar, shh, gf, gfill, glab)
        lvl = T("levels off", 26, PURPLE)
        lvl.next_to(gf, RIGHT, buff=0.2)

        def s_act(a):   # how on Smoothened is, 0..1
            return s0.animate.set_fill(GREEN, 0.2 + 0.45 * a)

        def bar_w(w):
            return Transform(bar, brake_bar(w))

        self.at("signaling builds")
        self.play(s_act(0.9), bar_w(5), Transform(st, state_chip("on", GREEN)), val.animate.set_value(0.5), run_time=0.8)
        new = [p_block(3), p_block(4)]
        self.at("part of its")
        self.play(FadeIn(new[0], scale=0.6), val.animate.set_value(0.75), lp.animate.move_to([-2.6, -0.4, 0]), run_time=0.5)
        self.play(FadeIn(new[1], scale=0.6), val.animate.set_value(0.92), bar_w(9), s_act(0.45), lp.animate.move_to([-3.2, -0.4, 0]), run_time=0.5)
        self.play(val.animate.set_value(0.95), FadeIn(lvl), run_time=0.5)
        ds = [shh_dot(2), shh_dot(3), shh_dot(4)]
        self.at("then it takes")
        self.play(*[FadeIn(d, shift=DOWN * 0.3) for d in ds], s_act(1.0), run_time=0.9)
        lab = T("one contributor to adaptation", 42, TEXT, weight=BOLD).move_to([0.5, -3.2, 0])
        self.at("keep going")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Two(Scn):
    def construct(self):
        v = TwoView(0.0)
        self.add(*v.cells, *v.axes, *v.ylab, *v.xlab)
        for i in (0, 1):
            self.add(v.pb_group(i, 2))
        self.at("starting at once")
        a0, upd0 = v.go_live(0)
        a1, upd1 = v.go_live(1)
        self.add(*v.traces, *v.heads)
        self.play(a0, a1, v.Tt.animate.set_value(1.0), run_time=0.6, rate_func=linear)
        v.cells[0].add_updater(upd0)
        v.cells[1].add_updater(upd1)
        self.at("low dose")
        self.play(FadeIn(v.dose[0], scale=0.9), v.Tt.animate.set_value(1.8), run_time=0.6, rate_func=linear)
        self.at("sonic hedgehog")
        self.play(FadeIn(v.dots[0], shift=DOWN * 0.25), v.Tt.animate.set_value(2.4), run_time=0.6, rate_func=linear)
        self.at("the other")
        self.play(Indicate(v.cells[1], color=YELLOW, scale_factor=1.06), run_time=0.6)
        self.at("high dose")
        self.play(FadeIn(v.dose[1], scale=0.9), FadeIn(v.dots[1], shift=DOWN * 0.25), v.Tt.animate.set_value(3.0), run_time=0.7, rate_func=linear)
        self.finish()


class S08Two2(Scn):
    def construct(self):
        v = two_frame(self, 3.0, 2)
        lab = T("more Patched", 32, PURPLE, weight=BOLD).move_to([0, 2.25, 0])
        self.at("make more")
        self.play(FadeIn(lab, scale=0.9), *[FadeIn(b, scale=0.5) for i in (0, 1) for b in v.pb[i][2:3]], run_time=0.5)
        self.at("as they go")
        adds = [FadeIn(b, scale=0.5) for i in (0, 1) for b in v.pb[i][3:5]]
        self.play(v.Tt.animate.set_value(5.0), LaggedStart(*adds, lag_ratio=0.3), run_time=1.5, rate_func=linear)
        self.finish()


def predict_texts():
    head = T("Predict", 44, GOLD, weight=BOLD).move_to([0, 3.35, 0])
    q = TL("in which cell\ndoes signaling\nfade first?", 34, TEXT, gap=0.1).move_to([0, 2.0, 0])
    return head, q


class S09Predict1(Scn):
    def construct(self):
        v = two_frame(self, 5.0, 5)
        head, q = predict_texts()
        self.at("Predict")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("which cell")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        two_frame(self, 5.0, 5)
        head, q = predict_texts()
        self.add(head, q)
        self.wait(self.narration_s)


def hilite(v, i):
    """gold label and underline for one cell's dose label"""
    ul = Line([CXS[i] - 0.95, 1.12, 0], [CXS[i] + 0.95, 1.12, 0], color=GOLD, stroke_width=6)
    return v.dose[i].animate.set_color(GOLD), Create(ul), ul


class S11Reveal1(Scn):
    def construct(self):
        v = two_frame(self, 5.0, 5)
        head, q = predict_texts()
        self.add(head, q)
        self.play(FadeOut(head), FadeOut(q), *[Create(l) for l in v.wl], *[FadeIn(t) for t in v.wll], run_time=0.5)
        tx = cross_t(C_LO)
        # grow the traces; mark where the low dose falls to the working level
        self.play(v.Tt.animate.set_value(tx), run_time=0.45, rate_func=linear)
        ring = Circle(radius=0.2, stroke_color=GOLD, stroke_width=5).move_to(v.axes[0].c2p(tx, WL))
        fb = T("falls below", 26, GOLD, weight=BOLD).move_to(v.axes[0].c2p(tx, WL) + RIGHT * 1.35 + UP * 0.95)
        fbl = Line(v.axes[0].c2p(tx, WL) + UR * 0.22, fb.get_left() + LEFT * 0.08, color=GOLD, stroke_width=3)
        self.play(Create(ring), FadeIn(fb), Create(fbl), run_time=0.4)
        a, b, ul0 = hilite(v, 0)
        self.play(a, b, Indicate(v.cells[0], color=GOLD, scale_factor=1.08), v.Tt.animate.set_value(tx + 4), run_time=0.6, rate_func=linear)
        self.at("its signaling")
        self.play(v.Tt.animate.set_value(40.0), run_time=1.6, rate_func=linear)
        self.at("the high dose")
        a, b, ul1 = hilite(v, 1)
        self.play(v.dose[0].animate.set_color(YELLOW), FadeOut(ul0), a, b, Indicate(v.cells[1], color=GOLD, scale_factor=1.08), run_time=0.6)
        end = v.axes[1].c2p(40, rate(C_HI, 40))
        st = T("still above", 26, GOLD, weight=BOLD).move_to(v.axes[1].c2p(31, 6.2))
        sta = arr(st.get_bottom() + DOWN * 0.02 + RIGHT * 0.5, end + UP * 0.12, GOLD, 4, 0.16)
        self.at("keeps signaling")
        self.play(FadeIn(st), GrowArrow(sta), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Dessaud(Scn):
    def construct(self):
        card, yr, nm, sb = credit("2007", "Eric Dessaud, James Briscoe\nand colleagues", "chick neural cells")
        cells = VGroup(*[Ellipse(width=1.3, height=0.75, stroke_color=GREY, stroke_width=3, fill_color=YELLOW, fill_opacity=0.35)
                         .move_to([x, -2.25, 0]) for x in (-1.8, 0.0, 1.8)])
        self.add(card)
        self.at("2007")
        self.play(FadeIn(yr, scale=0.9), run_time=0.6)
        self.at("Eric")
        self.play(FadeIn(nm, shift=UP * 0.1), FadeIn(cells), run_time=0.7)
        self.at("chick neural")
        self.play(FadeIn(sb, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S13Dessaud2(Scn):
    def construct(self):
        v = TwoView(0.0)
        v.live_all()
        self.add(*v.cells, *v.axes, *v.ylab, *v.xlab, *v.dose, *v.traces, *v.heads, *v.wl, *v.wll)
        for i in (0, 1):
            self.add(v.pb_group(i, 2), v.dots[i])
        ad = T("adaptation", 40, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        self.at("adapt")
        self.play(FadeIn(ad, scale=0.9), run_time=0.6)

        def adds(ks):
            return [FadeIn(v.pb[i][k], scale=0.5) for k in ks for i in (0, 1)]
        pl = TL("rising\nPatched1", 28, PURPLE, gap=0.08, weight=BOLD).move_to([0, 2.15, 0])
        self.at("signaling inside")
        # first the brake builds (traces still at the top), then the traces fall
        self.play(FadeIn(pl, shift=UP * 0.1), LaggedStart(*adds([2, 3, 4, 5, 6, 7, 8]), lag_ratio=0.1), run_time=1.0)
        self.at("fades")
        self.play(v.Tt.animate.set_value(40.0), run_time=2.6, rate_func=linear)
        self.finish()


class S14Dessaud3(Scn):
    def construct(self):
        global AX_Y, AX_H
        keep = (AX_Y, AX_H)
        AX_Y, AX_H = -0.5, 2.4          # shorter plots, so the duration bars have room under them
        try:
            v = two_frame(self, 40.0, 9, wl=True)
        finally:
            AX_Y, AX_H = keep
        dials = [Dial(-6.15, CELL_Y, 0.5, YELLOW, value=0.2), Dial(6.15, CELL_Y, 0.5, YELLOW, value=0.8)]
        BAR_YY = -2.5
        xs = [(v.axes[i].c2p(0, 0)[0], v.axes[i].c2p(min(cross_t(CS[i]), TMAX), 0)[0]) for i in (0, 1)]
        bars = [RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=0.46, stroke_width=0, fill_color=TEXT, fill_opacity=0.92
                                 ).move_to([(x0 + x1) / 2, BAR_YY, 0]) for x0, x1 in xs]
        # the same label placement on both bars: just under the bar's start
        labs = [T("time signaling", 26, TEXT, weight=BOLD).move_to([x0 + 0.05, BAR_YY - 0.5, 0], aligned_edge=LEFT) for x0, _ in xs]
        going = VGroup(arr([xs[1][1] + 0.02, BAR_YY, 0], [xs[1][1] + 0.5, BAR_YY, 0], GOLD, 6, 0.22),
                       T("still going", 26, GOLD, weight=BOLD).move_to([xs[1][1] + 0.4, BAR_YY - 0.5, 0], aligned_edge=RIGHT))
        self.play(*[FadeIn(d, scale=0.8) for d in dials], run_time=0.5)
        self.at("concentrations")
        a, b, ul1 = hilite(v, 1)
        self.play(a, b, Indicate(v.cells[1], color=GOLD, scale_factor=1.08), run_time=0.6)
        self.at("kept signaling")
        tx = cross_t(C_LO)
        ring = Circle(radius=0.2, stroke_color=GOLD, stroke_width=5).move_to(v.axes[0].c2p(tx, WL))
        drop0 = DashedLine(v.axes[0].c2p(tx, WL) + DOWN * 0.2, [xs[0][1], BAR_YY + 0.3, 0], color=GOLD, stroke_width=3)
        drop1 = DashedLine(v.axes[1].c2p(40, rate(C_HI, 40)) + DOWN * 0.15, [xs[1][1], BAR_YY + 0.3, 0], color=GOLD, stroke_width=3)
        self.play(v.dose[1].animate.set_color(YELLOW), FadeOut(ul1), Create(ring), Create(drop0), Create(drop1), run_time=0.8)
        self.at("a level")
        # each dial shrinks to the start of its bar, then the bar grows out of it
        shr = [d.animate.scale(0.3).move_to([x0, BAR_YY, 0]).set_opacity(0.0) for d, (x0, _) in zip(dials, xs)]
        self.play(*shr, *[GrowFromEdge(bar, LEFT) for bar in bars], run_time=0.7)
        self.remove(*dials)
        lab = T("level becomes duration", 32, TEXT, weight=BOLD).move_to([0, -3.62, 0])
        self.at("becomes a")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        self.at("length of time")
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in labs], FadeIn(going), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
EXPL_X = (-4.3, 0.0, 4.3)
EXPL_FRAC = (0.25, 0.5, 0.85)
EXPL_Y = 1.1


def frame15():
    """the explant row: same dose, different exposure (static pieces, in order)"""
    expl = [explant(x, EXPL_Y, 2.4, YELLOW, 0.35) for x in EXPL_X]
    clocks = [Clock(x, -1.5, 1.05, TEXT, frac=f, wedge=True) for x, f in zip(EXPL_X, EXPL_FRAC)]
    dial = Dial(-2.2, 3.1, 0.5, YELLOW, value=0.6)
    same = T("the same dose", 36, YELLOW, weight=BOLD).move_to([0.6, 3.1, 0])
    q = T("what should longer exposure do?", 42, TEXT, weight=BOLD).move_to([0, -3.3, 0])
    return expl, clocks, dial, same, q


class S15Predict2(Scn):
    def construct(self):
        expl, clocks, dial, same, q = frame15()
        grey = [explant(x, EXPL_Y, 2.4, GREY, 0.3) for x in EXPL_X]
        self.play(LaggedStart(*[FadeIn(g, scale=0.9) for g in grey], lag_ratio=0.2), run_time=0.7)
        self.at("hold the dose")
        self.play(*[ReplacementTransform(g, e) for g, e in zip(grey, expl)], FadeIn(dial, scale=0.8), FadeIn(same, shift=DOWN * 0.1), run_time=0.9)
        self.at("change only")
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in clocks], lag_ratio=0.45), run_time=1.9)
        self.at("what should")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S16Pause(NarratedScene):
    def construct(self):
        expl, clocks, dial, same, q = frame15()
        self.add(*expl, *clocks, dial, same, q)
        ul = Line(q.get_left() + DOWN * 0.35, q.get_right() + DOWN * 0.35, color=GOLD, stroke_width=6)
        self.play(Create(ul), Indicate(q, scale_factor=1.12, color=GOLD), run_time=1.0)
        while self.elapsed() < self.narration_s - 1.6:
            self.play(LaggedStart(*[Indicate(e, scale_factor=1.1, color=GOLD) for e in expl], lag_ratio=0.35),
                      Indicate(q, scale_factor=1.1, color=GOLD), run_time=1.6)
        self.wait(max(0.05, self.narration_s - self.elapsed()))


class S17Reveal2(Scn):
    def construct(self):
        card, yr, nm, sb = credit("2010", "Dessaud, Sasai, Briscoe\nand colleagues", "chick explants")
        ex = explant(0.0, -2.3, 0.75, YELLOW, 0.35)
        self.add(card)
        self.at("2010")
        self.play(FadeIn(yr, scale=0.9), run_time=0.6)
        self.at("same laboratory")
        self.play(FadeIn(nm, shift=UP * 0.1), FadeIn(ex), run_time=0.7)
        self.at("chick explants")
        self.play(FadeIn(sb, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tube18():
    return Tube(cx=-2.4, cy=0.2, W=4.8, H=4.8, nr=0.36, cr=0.15)


def tissue_labels(tb):
    cx, cy, H = tb.cx, tb.cy, tb.H
    roof_y, fp_y, n_y = cy + H / 2 - 0.17, cy - H / 2 + 0.17, tb.noto.get_center()[1]
    L = []
    L.append((T("epidermis", 24, GREY).move_to([cx, 3.55, 0]), Line([cx, 3.3, 0], [cx, cy + H / 2 + 0.34, 0], color=GREY, stroke_width=2)))
    L.append((T("roof plate", 24, GREY).move_to([-5.85, roof_y, 0]), Line([-4.95, roof_y, 0], [cx - 0.5, roof_y, 0], color=GREY, stroke_width=2)))
    L.append((T("ventricular\nzone", 24, GREY, line_spacing=0.8).move_to([-5.85, cy, 0]), Line([-4.95, cy, 0], [cx - 1.15, cy, 0], color=GREY, stroke_width=2)))
    L.append((T("floor plate", 24, TEAL).move_to([-5.8, fp_y, 0]), Line([-4.85, fp_y, 0], [cx - 0.5, fp_y, 0], color=TEAL, stroke_width=2)))
    L.append((T("notochord", 24, TEAL).move_to([-5.85, n_y, 0]), Line([-4.95, n_y, 0], [cx - 0.38, n_y, 0], color=TEAL, stroke_width=2)))
    return L


# (row y, domains recoloured, arrow target domain, colour, neuron name, clock fraction, time word)
ROWS18 = [(1.7, ("p0", "p1"), "p1", PINK1, "V0 and V1", 0.25, "shorter"),
          (0.15, ("p2",), "p2", PINK2, "V2", 0.5, "longer"),
          (-1.4, ("pMN",), "pMN", BLUE, "motor neurons", 0.85, "longest")]


class S18Reveal2b(Scn):
    def construct(self):
        tb = tube18()
        labs = tissue_labels(tb)
        self.add(tb.group(), *[a for a, b in labs], *[b for a, b in labs])
        rows = []
        for y, doms, tgt, col, name, fr, word in ROWS18:
            ex = explant(2.1, y, 0.85, YELLOW, 0.35)
            ck = Clock(3.55, y, 0.62, TEXT, frac=fr, wedge=True)
            tw = T(word, 26, TEXT, weight=BOLD).move_to([4.35, y + 0.22, 0], aligned_edge=LEFT)
            nm = T(name, 24, col).move_to([4.35, y - 0.22, 0], aligned_edge=LEFT)
            cell = tb.outer_cell(tgt, +1)
            end = cell.get_center() + np.array([0.17, 0.0, 0.0])
            ar = arr([1.45, y, 0], end, col, 5, 0.2)
            rows.append((ex, ck, tw, nm, ar, doms, col))
        same = VGroup(Dial(2.35, 3.2, 0.42, YELLOW, value=0.6), T("same dose", 28, YELLOW, weight=BOLD).move_to([4.15, 3.2, 0]))
        self.at("fixed dose")
        self.play(FadeIn(same), run_time=0.5)

        def reveal(k):
            ex, ck, tw, nm, ar, doms, col = rows[k]
            return [FadeIn(ex), FadeIn(ck), FadeIn(tw), GrowArrow(ar), *tb.recolor(doms), ex.animate.set_stroke(col).set_fill(col, 0.5)]
        self.at("longer exposure")
        self.play(*reveal(0), run_time=0.6)
        self.at("progressively")
        self.play(*reveal(1), run_time=0.6)
        self.at("more ventral")
        self.play(*reveal(2), run_time=0.6)
        self.at("ventral identities")
        self.play(*[FadeIn(r[3], shift=RIGHT * 0.1) for r in rows], run_time=0.6)
        note = T("neuron names: illustrative", 24, GREY).move_to([4.2, -2.75, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


class S19Reveal2c(Scn):
    def construct(self):
        # the address card of chapter 3 (gold, "address"), now with a second line
        card = RoundedRectangle(corner_radius=0.3, width=11.6, height=6.2, stroke_color=GOLD, stroke_width=5,
                                fill_color=GOLD, fill_opacity=0.08).move_to([0, 0, 0])
        head = T("address", 90, GOLD, TITLE_FONT, BOLD).move_to([0, 2.0, 0])
        d1 = Dial(-3.9, 0.35, 0.95, YELLOW, value=0.7)
        t1 = T("level of signal", 64, YELLOW, weight=BOLD).move_to([-2.5, 0.35, 0], aligned_edge=LEFT)
        c2 = Clock(-3.9, -1.75, 0.95, TEXT, frac=0.55)
        t2 = T("time", 64, TEXT, weight=BOLD).move_to([-2.5, -1.75, 0], aligned_edge=LEFT)
        self.add(card, head, d1, t1)
        self.at("time a cell")
        self.play(FadeIn(c2, scale=0.8), FadeIn(t2, shift=LEFT * 0.2), run_time=0.8)
        self.at("address")
        self.play(Indicate(head, color=GOLD, scale_factor=1.1), Indicate(t2, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# upkeep: history of signaling and a ventral marker (c = 4, tau = 24)
CXR = 2.0
RA_Y, RB_Y = 1.9, -0.7
AX_H2, AX_W2 = 2.0, 8.4
TM2, TOFF = 60.0, 30.0
K_M = 0.4375
TAU_H = 35.0
YA = 1.5


def A_n(t):
    return np.exp(-t / 24.0) if t <= TOFF else np.exp(-TOFF / 24.0) * np.exp(-(t - TOFF) / 2.0)


def H_n(t):
    if t <= TOFF:
        return 1.2 * (1 - np.exp(-t / 24.0))
    return H_n(TOFF) * np.exp(-(t - TOFF) / TAU_H)


def M_n(t):
    h = H_n(t)
    return h ** 3 / (h ** 3 + K_M ** 3)


def row_axes(y, ymax):
    return Axes(x_range=[0, TM2], y_range=[0, ymax], x_length=AX_W2, y_length=AX_H2, tips=False,
                axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False}).move_to([CXR, y, 0])


class Upkeep:
    def __init__(self, T0):
        self.Tt = ValueTracker(T0)
        self.axA, self.axB = row_axes(RA_Y, YA), row_axes(RB_Y, 1.05)
        tt = lambda: max(self.Tt.get_value(), 0.3)
        self.hist = always_redraw(lambda: self.axA.plot(H_n, x_range=[0, min(tt(), TOFF), 0.3], color=YELLOW, stroke_width=8))

        def hist2():
            if tt() <= TOFF + 0.4:
                return VMobject()
            return self.axA.plot(H_n, x_range=[TOFF, tt(), 0.3], color=YELLOW, stroke_width=8).set_stroke(opacity=0.4)
        self.hist2 = always_redraw(hist2)
        self.mark = always_redraw(lambda: self.axB.plot(M_n, x_range=[0, tt(), 0.3], color=BLUE, stroke_width=8))
        self.act = always_redraw(lambda: DashedVMobject(
            self.axA.plot(A_n, x_range=[0, tt(), 0.3], color=YELLOW, stroke_width=5),
            num_dashes=max(8, int(tt() * 0.9)), dashed_ratio=0.55))
        x0 = self.axA.c2p(0, 0)[0]
        self.lA = T("history of signaling", 28, YELLOW, weight=BOLD).move_to([x0, 3.3, 0], aligned_edge=LEFT)
        self.lB = T("ventral marker", 28, BLUE, weight=BOLD).move_to([x0, 0.62, 0], aligned_edge=LEFT)
        self.yA = T("less to more", 26, GREY).rotate(PI / 2).move_to([x0 - 0.38, RA_Y, 0])
        self.yB = T("less to more", 26, GREY).rotate(PI / 2).move_to([x0 - 0.38, RB_Y, 0])
        self.xl = T("time", 26, GREY).move_to([self.axB.c2p(TM2, 0)[0] - 0.45, RB_Y - AX_H2 / 2 - 0.3, 0])
        self.cell = Ellipse(width=2.5, height=1.5, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.55).move_to([-5.3, 0.6, 0])
        self.dots = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.97).move_to(
            [-5.3 + 1.57 * np.cos(a * DEGREES), 0.6 + 1.02 * np.sin(a * DEGREES), 0]) for a in (50, 70, 90, 110, 130)])
        self.cl = T("one cell", 26, GREY).move_to([-5.3, -0.55, 0])


class S20Upkeep(Scn):
    def construct(self):
        u = Upkeep(0.0)
        self.add(u.cell, u.dots, u.cl, u.axA, u.lA, u.yA)
        self.at("identity")
        self.play(Create(u.axB), FadeIn(u.lB), FadeIn(u.xl), FadeIn(u.yB), run_time=0.7)
        self.add(u.hist, u.mark)
        self.at("how much")
        self.play(u.Tt.animate.set_value(TOFF), run_time=2.6, rate_func=linear)
        self.finish()


class S21Upkeep2(Scn):
    def construct(self):
        u = Upkeep(TOFF)
        self.add(u.cell, u.dots, u.cl, u.axA, u.axB, u.lA, u.lB, u.xl, u.yA, u.yB, u.hist, u.hist2, u.mark)
        note = TL("history is a record of past signaling,\nnot a stored total", 30, TEXT, gap=0.1).move_to([1.0, -3.05, 0])
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.3)
        # pathway activity, drawn while the signal continues
        a_static = DashedVMobject(u.axA.plot(A_n, x_range=[0, TOFF, 0.3], color=YELLOW, stroke_width=5), num_dashes=27, dashed_ratio=0.55)
        a_lab = T("pathway activity", 28, YELLOW, weight=BOLD).move_to(u.axA.c2p(6, 1.3), aligned_edge=LEFT)
        self.at("also needs")
        self.play(Create(a_static), FadeIn(a_lab), run_time=0.9)
        self.remove(a_static)
        self.add(u.act)
        xoff = u.axA.c2p(TOFF, 0)[0]
        line = DashedLine([xoff, u.axB.c2p(0, 0)[1], 0], [xoff, u.axA.c2p(0, YA)[1] + 0.1, 0], color=TEXT, stroke_width=3)
        off_lab = T("signal off", 28, TEXT, weight=BOLD).move_to([xoff + 0.2, 3.3, 0], aligned_edge=LEFT)
        self.at("for a while")
        self.play(FadeOut(u.dots), u.cell.animate.set_fill(YELLOW, 0.12), Create(line), FadeIn(off_lab), run_time=0.5)
        self.play(u.Tt.animate.set_value(TM2), run_time=2.6, rate_func=linear)
        dor = T("more dorsal", 28, BLUE, weight=BOLD).move_to(u.axB.c2p(52, 0.97))
        dar = arr(u.axB.c2p(56, 0.78), u.axB.c2p(TM2 - 0.8, M_n(TM2) + 0.1), BLUE, 4, 0.16)
        self.play(FadeIn(dor, shift=DOWN * 0.1), GrowArrow(dar), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
EXC_X, EXC_Y = -3.9, 0.55


def frame22():
    ex = explant(EXC_X, EXC_Y, 2.9, BLUE, 0.55)
    cap = T("chick explant", 28, GREY).move_to([EXC_X, EXC_Y - 1.95, 0])
    g_out = Rectangle(width=0.8, height=3.2, stroke_color=GREY, stroke_width=3).move_to([-0.9, -1.5 + 1.6, 0])
    g_lab = TL("pathway\nactivity", 26, YELLOW, gap=0.1).move_to([-0.9, -2.35, 0])
    return ex, cap, g_out, g_lab


class S22Cut(Scn):
    def construct(self):
        ex, cap, g_out, g_lab = frame22()
        lvl = ValueTracker(0.9)
        nb, nor = ValueTracker(9), ValueTracker(0)
        BASE = -1.5
        g_fill = always_redraw(lambda: Rectangle(width=0.8, height=max(3.2 * lvl.get_value(), 0.02), stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
                               .move_to([-0.9, BASE + max(3.2 * lvl.get_value(), 0.02) / 2, 0]))
        b_blue = always_redraw(lambda: Rectangle(width=1.2, height=max(0.34 * nb.get_value(), 0.02), stroke_width=0, fill_color=BLUE, fill_opacity=0.8)
                               .move_to([2.0, BASE + max(0.34 * nb.get_value(), 0.02) / 2, 0]))
        b_or = always_redraw(lambda: Rectangle(width=1.2, height=max(0.34 * nor.get_value(), 0.02), stroke_width=0, fill_color=PINK1, fill_opacity=0.85)
                             .move_to([4.7, BASE + max(0.34 * nor.get_value(), 0.02) / 2, 0]))
        base = Line([0.9, BASE, 0], [6.4, BASE, 0], color=GREY, stroke_width=3)
        t_blue = TL("motor\nneurons", 26, BLUE, gap=0.1).move_to([2.0, -2.35, 0])
        t_or = TL("more dorsal fates\n(e.g. V0 to V2)", 26, PINK1, gap=0.1).move_to([4.95, -2.35, 0])
        cnt = T("cells in the explant", 26, GREY).move_to([3.7, 2.55, 0])
        self.add(ex, cap, g_out, g_lab, g_fill, base, t_blue, t_or, b_blue, b_or, cnt)
        cyc = chip("cyclopamine", RED, 30).move_to([EXC_X, 3.45, 0])
        brc = Brace(Line([EXC_X - 1.65, 2.3, 0], [EXC_X + 1.65, 2.3, 0]), UP, buff=0.05, color=RED)
        self.at("cutting the signal")
        self.play(FadeIn(cyc, shift=DOWN * 0.15), GrowFromCenter(brc), run_time=0.5)
        blk = VGroup(*[inhib([EXC_X + dx, 2.7, 0], [EXC_X + dx, 2.36, 0], RED, 5) for dx in (-1.13, 0.0, 1.13)])
        self.at("off")
        self.play(Create(blk, lag_ratio=0), run_time=0.3)
        self.play(lvl.animate.set_value(0.1), run_time=0.9)
        conv = [ex[i].animate.set_stroke(PINK1).set_fill(PINK1, 0.6) for i in (4, 1, 3, 5, 7, 0)]
        self.at("made cells")
        self.play(LaggedStart(*conv, lag_ratio=0.25), run_time=1.2)
        self.at("to more dorsal")
        self.play(nor.animate.set_value(6), nb.animate.set_value(3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pathway_unit(cx, cy, frac, k, name):
    col = GREY
    lab = T(name, 28, TEXT, weight=BOLD).move_to([cx, cy + 1.4, 0])
    mem = Rectangle(width=1.9, height=0.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([cx - 0.8, cy + 0.55, 0])
    sx = cx - 0.8
    if k == 0:
        rec = VGroup(RoundedRectangle(corner_radius=0.08, width=0.4, height=0.9, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).move_to([sx, cy + 0.55, 0]))
    elif k == 1:
        rec = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.34, height=0.9, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).move_to([sx + dx, cy + 0.55, 0]) for dx in (-0.3, 0.3)])
    elif k == 2:
        rec = VGroup(Circle(radius=0.34, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).move_to([sx, cy + 0.55, 0]))
    else:
        rec = VGroup(Square(side_length=0.6, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).rotate(PI / 4).move_to([sx, cy + 0.55, 0]))
    ar = arr([sx, cy + 0.0, 0], [sx, cy - 0.75, 0], GREY, 5, 0.2)
    dot = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([sx, cy - 1.1, 0])
    ck = Clock(cx + 1.0, cy - 0.1, 0.72, TEXT, frac=0.0)
    return VGroup(lab, mem, rec, ar, dot, ck), ck


class S23General(Scn):
    def construct(self):
        pos = [(-3.5, 1.9, 0.3, "pathway A"), (3.5, 1.9, 0.6, "pathway B"), (-3.5, -1.9, 0.8, "pathway C"), (3.5, -1.9, 0.45, "pathway D")]
        built = [pathway_unit(x, y, f, k, n) for k, (x, y, f, n) in enumerate(pos)]
        units = [b[0] for b in built]
        self.add(*units)
        self.at("information")
        self.play(*[Rotate(b[1].hand, angle=-TAU * p[2], about_point=b[1].c) for b, p in zip(built, pos)], run_time=1.1, rate_func=smooth)
        self.at("many signaling")
        self.play(LaggedStart(*[Indicate(u, color=TEXT, scale_factor=1.06) for u in units], lag_ratio=0.2), run_time=1.4)
        tb = Tube(cx=-1.6, cy=0.2, W=4.6, H=4.6, nr=0.36, cr=0.14)
        self.at("here")
        self.play(FadeOut(VGroup(*units)), run_time=0.5)
        self.play(FadeIn(tb.group()), run_time=0.7)
        pid = T("positional identity", 36, GOLD, weight=BOLD).move_to([3.9, 1.4, 0])
        tgt = tb.outer_cell("p2", +1)
        ar = arr([pid.get_left()[0] - 0.1, pid.get_center()[1] - 0.15, 0], tgt.get_center() + np.array([0.2, 0.05, 0]), GOLD, 5, 0.2)
        self.at("positional identity")
        self.play(*tb.recolor(["p0", "p1", "p2", "pMN", "p3"]), FadeIn(pid), GrowArrow(ar), run_time=0.9)
        cell = tb.outer_cell("pMN", +1, 1)
        ring = Circle(radius=0.3, stroke_color=GOLD, stroke_width=5).move_to(cell.get_center())
        pg = T("a progenitor", 34, TEXT).move_to([3.9, -1.7, 0])
        ln = Line([pg.get_left()[0] - 0.1, pg.get_center()[1], 0], ring.get_center() + np.array([0.3, 0, 0]) * 1.0 + RIGHT * 0.0, color=GOLD, stroke_width=3)
        self.at("progenitor adopts")
        self.play(Create(ring), FadeIn(pg), Create(ln), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
SL_X0, SL_X1 = -3.4, 1.0
LV_Y, TM_Y = 1.5, -1.1


def slx(v):
    return SL_X0 + (SL_X1 - SL_X0) * (v - 0.5) / 9.5


ZNAMES = [("dorsal", GREY), ("p0", PINK0), ("p1", PINK1), ("p2", PINK2), ("pMN", BLUE), ("p3", ORANGE)]


class S24Sim(Scn):
    def construct(self):
        panel = RoundedRectangle(corner_radius=0.3, width=12.4, height=6.8, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.05).move_to([0, 0, 0])
        ct, tt = ValueTracker(0.5), ValueTracker(0.5)
        l1 = T("level", 46, YELLOW, weight=BOLD).move_to([-5.3, LV_Y, 0])
        l2 = T("time", 46, TEXT, weight=BOLD).move_to([-5.3, TM_Y, 0])
        tr1 = Line([SL_X0, LV_Y, 0], [SL_X1, LV_Y, 0], color=GREY, stroke_width=12)
        tr2 = Line([SL_X0, TM_Y, 0], [SL_X1, TM_Y, 0], color=GREY, stroke_width=12)
        k1 = always_redraw(lambda: Circle(radius=0.36, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.85).move_to([slx(ct.get_value()), LV_Y, 0]))
        k2 = always_redraw(lambda: Circle(radius=0.36, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.85).move_to([slx(tt.get_value()), TM_Y, 0]))
        ys = [2.3, 1.38, 0.46, -0.46, -1.38, -2.3]
        chips = VGroup(*[chip(n, c, 30) for n, c in ZNAMES])
        for ch, y in zip(chips, ys):
            ch[0].stretch_to_fit_width(2.6).move_to([4.3, y, 0])
            ch[1].move_to([4.3, y, 0])

        def upd(m):
            s = total(ct.get_value(), tt.get_value())
            cur = [z[0] for z in ZONES].index(zone_of(s)[0])
            for k, ch in enumerate(m):
                col = ZNAMES[k][1]
                ch[0].set_fill(col, 0.8 if k == cur else 0.08).set_stroke(col, width=6 if k == cur else 2)
                ch[1].set_color(BG if (k == cur and col != GREY) else (TEXT if k == cur else col))
        chips.add_updater(upd)
        upd(chips)
        arrow = arr([1.55, 0.2, 0], [2.7, 0.2, 0], GREY, 6, 0.25)
        cap = T("domain", 28, GREY).move_to([4.3, 3.0, 0])
        vent = arr([6.05, 1.6, 0], [6.05, -1.8, 0], GREY, 4, 0.2)
        vlab = T("more ventral", 26, GREY).rotate(-PI / 2).move_to([6.5, 0.0, 0])
        self.add(panel)
        self.at("the simulation")
        self.play(FadeIn(l1), FadeIn(l2), Create(tr1), Create(tr2), run_time=0.6)
        self.add(k1, k2)
        self.play(FadeIn(chips), GrowArrow(arrow), FadeIn(cap), GrowArrow(vent), FadeIn(vlab), run_time=0.7)
        self.at("set both")
        self.play(Indicate(l2, color=TEXT, scale_factor=1.12), tt.animate.set_value(3.0), run_time=0.8)
        self.at("the level")
        self.play(Indicate(l1, color=YELLOW, scale_factor=1.12), ct.animate.set_value(1.0), run_time=0.7)
        self.at("and the time")
        self.play(Indicate(l2, color=TEXT, scale_factor=1.12), tt.animate.set_value(6.0), run_time=0.8)
        self.at("watch the domain")
        self.play(ct.animate.set_value(4.0), tt.animate.set_value(10.0), run_time=1.3)
        self.finish()


class S25Takeaway(Scn):
    def construct(self):
        head = T("takeaway", 44, GOLD, weight=BOLD).move_to([0, 3.15, 0])
        self.at("the takeaway")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        dial = Dial(-3.3, 0.5, 1.9, YELLOW, value=0.15)
        l1 = T("how much signal", 44, YELLOW, weight=BOLD).move_to([-3.3, -2.1, 0])
        self.at("how much signal")
        self.play(FadeIn(dial, scale=0.9), FadeIn(l1, shift=UP * 0.1), run_time=0.6)
        self.play(dial.turn_to(0.8), run_time=0.5)
        clock = Clock(3.3, 0.5, 1.9, TEXT, frac=0.0)
        l2 = T("for how long", 44, TEXT, weight=BOLD).move_to([3.3, -2.1, 0])
        plus = T("+", 90, GREY, weight=BOLD).move_to([0, 0.5, 0])
        self.at("for how long")
        self.play(FadeIn(clock, scale=0.9), FadeIn(l2, shift=UP * 0.1), FadeIn(plus), run_time=0.6)
        self.play(Rotate(clock.hand, angle=-TAU * 0.6, about_point=clock.c), run_time=0.6)
        self.finish()


class S26End(EndCard):
    LINE = "A progenitor reads how much signal it gets and for how long."
