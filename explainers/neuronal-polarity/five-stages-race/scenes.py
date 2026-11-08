"""Neuronal polarity, chapter 2: Five Stages and a Race  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept; shared with the other chapters of this lesson, from scenes.old.py)
  YELLOW = the axon, and the leading neurite that becomes it
  BLUE   = dendrites, and a neurite called a future dendrite
  GREY   = cell body, neurites that have not been chosen, outlines, axes, the dish
  RED    = the cut (blade, cut end, "cut" marker), a crossed-out idea
  GOLD   = the open question and the race: question marks, "can be reassigned", the scoreboard
  PINK   = the "fixed for good" idea (its tag and its card); new in this chapter
  TEXT   = labels, citations, synapse dots
  (series colours not used in this chapter: GREEN PIP3 and feedback, ORANGE actin, TEAL microtubules,
   PURPLE ankyrin G and the initial segment)

The length-against-time curves are NOT measurements ("schematic, not data" is printed under every plot).
They are computed from one small rate rule (see sim()): every neurite relaxes toward about 2.4 length
units; a neurite that "breaks away" grows at a steady rate that saturates near 3.6. The neurite drawings
read the same numbers as the plot.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F28DB2"
SOMA_FILL = "#262b36"

DIRS = [10, 82, 154, 226, 298]          # neurite 0 points right; it is the one that wins in the uncut race
CA = np.array([-1.3, -0.3, 0.0])         # cell centre with the stage column on the left and the plot on the right
CB = np.array([-3.3, -0.3, 0.0])         # cell centre once the column is gone
CM = np.array([0.3, -0.3, 0.0])          # centre of the mature cell (stages 4 and 5)
C5 = np.array([1.0, -0.3, 0.0])          # centre of the stage 1 cell
CTR_POS = np.array([5.4, 3.25, 0.0])     # day counter
AX_L, DEND_L = 4.5, 2.9                  # stage 4 and 5: the axon stays the longest process

# ---------------------------------------------------------------- the rate rule behind every curve
DT = 0.01
TG = np.arange(0, 3.0 + 1e-9, DT)
K = len(TG)
LMAX = [2.40, 2.43, 2.37, 2.42, 2.38]    # every neurite relaxes toward about 2.4
KC, VWIN, LCAP = 3.0, 1.9, 3.6
KCUT = int(round(2.0 / DT))


def _sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def sim(win0=0, t0=1.45, cut=False, post0=2.39, win1=None, t1=2.2, lmax=None):
    """Five neurite lengths against time (units of the drawing). Optional cut of neurite 0 at t = 2."""
    lm = lmax or LMAX
    L = np.zeros((5, K))
    L[:, 0] = 0.05
    for k in range(K - 1):
        t = TG[k]
        for i in range(5):
            g = 0.0
            if not cut or k < KCUT:
                if i == win0:
                    g = _sig((t - t0) / 0.08)
            elif win1 is not None and i == win1:
                g = _sig((t - t1) / 0.08)
            relax = KC * (lm[i] - L[i, k])
            go = VWIN * (1 - (L[i, k] / LCAP) ** 6)
            L[i, k + 1] = L[i, k] + DT * ((1 - g) * relax + g * go)
        if cut and k + 1 == KCUT + 1:
            L[0, k + 1] = post0          # the cut: neurite 0 is shortened in one step
    return L


SIM_A = sim(cut=True, post0=2.39, win1=1)            # natural race, then cut level with the pack, a sibling wins
SIM_STUMP = sim(cut=True, post0=3.05, win1=0, t1=2.15)  # cut leaves the stump well ahead; it keeps climbing
SIM_B2 = sim(cut=True, post0=2.0, win1=1, t1=2.15, lmax=[2.40, 3.10, 2.37, 2.42, 2.38])  # a sibling is the one ahead
SIM_RUN = {1: SIM_A, 3: sim(cut=True, post0=2.39, win1=3), 0: sim(cut=True, post0=2.39, win1=0)}
SIM_B = SIM_RUN[3]                                   # the sibling that takes over in the Dotti and Banker scene
L_CUT = float(SIM_A[0, KCUT + 1])                    # 2.39: the stump after the cut
LS2 = [float(SIM_A[i, 100]) for i in range(5)]       # lengths at t = 1.0 (stage 2)
LS3 = [float(SIM_A[i, KCUT]) for i in range(5)]      # lengths at t = 2.0 (stage 3)
LPOST = [float(SIM_A[i, KCUT + 1]) for i in range(5)]  # just after the cut


def u(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def perp(d):
    return np.array([-d[1], d[0], 0.0])


# ---------------------------------------------------------------- the cell
class Neuron:
    """Soma plus neurites drawn as tapered bars. Lengths and widths are ValueTrackers; every piece
    follows the soma, so the whole group can be shifted."""

    def __init__(self, center, lengths, colors=None, angles=DIRS, w=0.30, soma_r=0.55, tip_r=None):
        n = len(angles)
        self.n = n
        self.dirs = [u(a) for a in angles]
        colors = colors or [GREY] * n
        self.tr = [ValueTracker(L) for L in lengths]
        self.w0 = [ValueTracker(w) for _ in range(n)]
        self.w1 = [ValueTracker(w) for _ in range(n)]
        self.soma = Circle(radius=soma_r, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL,
                           fill_opacity=1).move_to(center)
        self.polys, self.tips = [], []
        for i in range(n):
            d = self.dirs[i]
            nv = perp(d)
            p = VMobject(fill_color=colors[i], fill_opacity=1, stroke_color=colors[i], stroke_width=0)

            def fp(m, i=i, d=d, nv=nv):
                c = self.soma.get_center()
                Lc = max(self.tr[i].get_value(), 0.06)
                a, b = c + d * 0.05, c + d * Lc
                h0, h1 = self.w0[i].get_value() / 2, self.w1[i].get_value() / 2
                m.set_points_as_corners([a + nv * h0, b + nv * h1, b - nv * h1, a - nv * h0, a + nv * h0])

            p.add_updater(fp)
            fp(p)
            tr_ = tip_r or max(w * 0.5, 0.05)
            t = Dot(radius=tr_, color=colors[i])

            def ft(m, i=i, d=d):
                m.set_width(max(self.w1[i].get_value(), 0.07))
                m.move_to(self.soma.get_center() + d * max(self.tr[i].get_value(), 0.06))

            t.add_updater(ft)
            ft(t)
            self.polys.append(p)
            self.tips.append(t)
        self.group = VGroup(*self.polys, *self.tips, self.soma)

    def pt(self, i, L):
        return self.soma.get_center() + self.dirs[i] * L

    def rc(self, i, col):
        return [self.polys[i].animate.set_color(col), self.tips[i].animate.set_color(col)]

    def rc_all(self, cols):
        out = []
        for i, c in enumerate(cols):
            out += self.rc(i, c)
        return out


def driver(neuron, plot, clk):
    """Invisible object that copies the rate-rule lengths at the clock time onto the neurites."""
    m = Mobject()

    def f(_):
        k = int(round(clk.get_value() / DT))
        k = min(max(k, 0), K - 1)
        for i in range(neuron.n):
            neuron.tr[i].set_value(float(plot.L[i][k]))

    m.add_updater(f)
    return m


def bg_clock(scene, t0, t1, v0, v1):
    """A tracker that follows the scene's own time: v0 until t0, then linear to v1 at t1."""
    tr = ValueTracker(v0)

    def f(m):
        t = scene.renderer.time
        x = min(max((t - t0) / (t1 - t0), 0.0), 1.0)
        m.set_value(v0 + (v1 - v0) * x)

    tr.add_updater(f)
    return tr


# ---------------------------------------------------------------- the length-against-time plot
class Plot:
    def __init__(self, L, clk, x0=2.35, y0=-2.7, sx=1.4, sy=1.5, tmax=3.0, ymax=3.6, cols=None,
                 xlabel="time", ylabel="length", sw=6, lab=26, ticks=True, t0=0.0, kstart=0, schem=True):
        self.L, self.clk = L, clk
        self.x0, self.y0, self.sx, self.sy, self.t0 = x0, y0, sx, sy, t0
        self.ks = kstart
        cols = cols or [GREY] * 5
        w = (tmax - t0) * sx
        self.ay = Line([x0, y0, 0], [x0, y0 + ymax * sy, 0], color=GREY, stroke_width=3)
        self.ax = Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY, stroke_width=3)
        self.yl = T(ylabel, lab, GREY).next_to(self.ay.get_end(), UP, buff=0.1).align_to(self.ay, LEFT)
        parts = [self.ay, self.ax, self.yl]
        if ticks:
            self.xl = T(xlabel, lab, GREY).move_to([x0 + w, y0 - 0.34, 0])
            self.xl.align_to(self.ax.get_end(), RIGHT)
            for tt in (1, 2):
                if t0 < tt <= tmax:
                    px = x0 + (tt - t0) * sx
                    parts += [Line([px, y0, 0], [px, y0 + 0.14, 0], color=GREY, stroke_width=3),
                              T(f"day {tt}", lab, GREY).move_to([px, y0 - 0.34, 0])]
        else:
            self.xl = T(xlabel, lab, GREY).next_to(self.ax.get_end(), DOWN, buff=0.12).align_to(self.ax, RIGHT)
        parts.append(self.xl)
        if schem:
            parts.append(T("schematic, not data", 22, GREY).move_to([x0 + w / 2, y0 - (0.78 if ticks else 0.62), 0]))
        self.frame = VGroup(*parts)
        self.traces = []
        for i in range(5):
            m = VMobject(stroke_color=cols[i], stroke_width=sw, fill_opacity=0)

            def f(mm, i=i):
                k = int(round(self.clk.get_value() / DT))
                k = min(max(k, 1), K - 1)
                idx = list(range(0, k - 1, 3)) + [k - 1, k]
                idx = [j for j in idx if j >= self.ks]
                if len(idx) < 2:
                    idx = [self.ks, self.ks]
                mm.set_points_as_corners([self.P(TG[j], self.L[i][j]) for j in idx])

            m.add_updater(f)
            f(m)
            self.traces.append(m)
        self.tg = VGroup(*self.traces)
        self.group = VGroup(self.frame, self.tg)

    def P(self, t, l):
        return np.array([self.x0 + (t - self.t0) * self.sx, self.y0 + l * self.sy, 0.0])

    def cutline(self, ymax=3.6):
        x = self.x0 + (2.0 - self.t0) * self.sx
        ln = DashedLine([x, self.y0, 0], [x, self.y0 + ymax * self.sy, 0], color=RED, stroke_width=3, dash_length=0.12)
        lb = T("cut", 24, RED).move_to([x, self.y0 + ymax * self.sy + 0.25, 0])
        return VGroup(ln, lb)

    def rc(self, i, col):
        return self.traces[i].animate.set_color(col)


# ---------------------------------------------------------------- stage column, icons, counter
def veil(R, fill=0.22, sw=3):
    def f(th):
        r = R * (0.8 + 0.2 * abs(np.sin(3 * th + 0.4)))
        return np.array([r * np.cos(th), r * np.sin(th), 0.0])

    return ParametricFunction(f, t_range=[0, TAU], stroke_color=GREY, stroke_width=sw, fill_color=GREY,
                              fill_opacity=fill)


def veil_full(R):
    g = VGroup(veil(R))
    for m in range(6):
        th = (PI / 2 - 0.4 + m * PI) / 3
        r = R * 0.98
        g.add(Line(np.array([0.62 * np.cos(th), 0.62 * np.sin(th), 0]), np.array([r * np.cos(th), r * np.sin(th), 0]),
                   color=GREY, stroke_width=2, stroke_opacity=0.55))
    return g


def veil_edge(R, th=0.0):
    r = R * (0.8 + 0.2 * abs(np.sin(3 * th + 0.4)))
    return np.array([r * np.cos(th), r * np.sin(th), 0.0])


def mini(k, s=0.8):
    g = VGroup()
    if k == 1:
        g.add(veil(0.62 * s, fill=0.28, sw=2))
    else:
        for j, a in enumerate(DIRS):
            d = u(a)
            nv = perp(d)
            if k == 2:
                L, col = 0.5, GREY
            elif k == 3:
                L, col = (0.8, YELLOW) if j == 0 else (0.5, GREY)
            else:
                L, col = (0.8, YELLOW) if j == 0 else (0.58, BLUE)
            g.add(Line(d * 0.1 * s, d * L * s, color=col, stroke_width=4))
            if k >= 4 and j > 0:
                p = d * L * 0.6 * s
                g.add(Line(p, p + d * 0.22 * s + nv * 0.16 * s, color=BLUE, stroke_width=3),
                      Line(p, p + d * 0.22 * s - nv * 0.16 * s, color=BLUE, stroke_width=3))
            if k == 5 and j > 0:
                g.add(Dot(d * L * 0.9 * s + nv * 0.1 * s, radius=0.045, color=TEXT),
                      Dot(d * L * 0.45 * s - nv * 0.1 * s, radius=0.045, color=TEXT))
    g.add(Circle(radius=0.14 * s, stroke_color=GREY, stroke_width=2, fill_color=SOMA_FILL, fill_opacity=1))
    return g


NAMES = {1: "lamellipodia", 2: "minor neurites", 3: "axon", 4: "dendrites", 5: "maturation"}
COLX = -5.6
BW, BH = 2.4, 1.3
ICON_S = 0.52
ICON_OFF = np.array([0.35, 0.2, 0.0])


def col_center(k):
    return np.array([COLX, 2.84 - 1.42 * (k - 1), 0.0])


class Column:
    """The five stage boxes stacked on the left, each with its number and name. Boxes in `filled` carry their
    little cell icon; names show for the active and the filled boxes."""

    def __init__(self, active=None, filled=()):
        self.boxes, self.icons, self.names = [], {}, {}
        for k in range(1, 6):
            c = col_center(k)
            rect = RoundedRectangle(corner_radius=0.12, width=BW, height=BH, stroke_color=GREY, stroke_width=2.5,
                                    fill_opacity=0).move_to(c)
            num = T(str(k), 28, GREY, weight=BOLD).move_to(c + np.array([-0.9, 0.38, 0.0]))
            self.boxes.append(VGroup(rect, num))
            nm = T(NAMES[k], 26, GREY).move_to(c + DOWN * 0.43)
            if not (k in filled or k == active):
                nm.set_opacity(0)
            self.names[k] = nm
        parts = list(self.boxes) + list(self.names.values())
        for k in filled:
            ic = mini(k, ICON_S).move_to(col_center(k) + ICON_OFF)
            self.icons[k] = ic
            parts.append(ic)
        self.group = VGroup(*parts)
        if active:
            r, n = self.boxes[active - 1]
            r.set_stroke(TEXT, 5)
            n.set_color(TEXT)
            self.names[active].set_color(TEXT)

    def activate(self, k, prev=None):
        out = []
        if prev:
            r, n = self.boxes[prev - 1]
            out += [r.animate.set_stroke(GREY, 2.5), n.animate.set_color(GREY), self.names[prev].animate.set_color(GREY)]
        r, n = self.boxes[k - 1]
        out += [r.animate.set_stroke(TEXT, 5), n.animate.set_color(TEXT),
                self.names[k].animate.set_opacity(1).set_color(TEXT)]
        return out

    def fly(self, scene, k, src, run=0.8):
        """The big cell shrinks into box k and leaves its icon there."""
        icon = mini(k, ICON_S).move_to(col_center(k) + ICON_OFF)
        cp = VGroup(*[m.copy() for m in src])
        for m in cp.get_family():
            m.clear_updaters()
        scene.add(cp)
        s = icon.height / cp.height
        scene.play(cp.animate.scale(s).move_to(icon.get_center()), run_time=run)
        scene.remove(cp)
        scene.add(icon)
        self.icons[k] = icon


def row_boxes():
    boxes = []
    for k in range(1, 6):
        c = np.array([-5.0 + 2.5 * (k - 1), -0.3, 0.0])
        rect = RoundedRectangle(corner_radius=0.16, width=2.3, height=4.2, stroke_color=GREY, stroke_width=3,
                                fill_opacity=0).move_to(c)
        num = T(str(k), 44, GREY, weight=BOLD).move_to(c + UP * 1.4)
        boxes.append(VGroup(rect, num))
    return VGroup(*boxes)


class Ctr:
    """Day counter in the top right corner (static text or live from a tracker)."""

    def __init__(self, text="hours", w=2.5):
        self.box = RoundedRectangle(corner_radius=0.12, width=w, height=0.62, stroke_color=GREY, stroke_width=2.5,
                                    fill_opacity=0).move_to(CTR_POS)
        self.txt = M(text, 28).move_to(CTR_POS)
        self.group = VGroup(self.box, self.txt)

    def live(self, clk, fmt="day {:.1f}"):
        def f(m):
            m.become(M(fmt.format(clk.get_value()), 28).move_to(self.box.get_center()))

        self.txt.add_updater(f)
        f(self.txt)
        return self

    def static(self, text):
        self.txt.clear_updaters()
        self.txt.become(M(text, 28).move_to(self.box.get_center()))
        return self


def ring(p, col=TEXT, r=0.3, w=5):
    return Circle(radius=r, stroke_color=col, stroke_width=w).move_to(p)


def tickmark(n, i, Lc, col=RED, off=0.2):
    d = n.dirs[i]
    p = n.pt(i, Lc + off)
    nv = perp(d)
    return Line(p + nv * 0.26, p - nv * 0.26, color=col, stroke_width=7)


def fragment(n, i, La, Lb, col, w=0.30):
    d = n.dirs[i]
    nv = perp(d)
    a, b = n.pt(i, La), n.pt(i, Lb)
    poly = VMobject(fill_color=col, fill_opacity=1, stroke_color=col, stroke_width=0)
    poly.set_points_as_corners([a + nv * w / 2, b + nv * w / 2, b - nv * w / 2, a - nv * w / 2, a + nv * w / 2])
    return VGroup(poly, Dot(b, radius=max(w * 0.5, 0.05), color=col))


def lab(text, pos, size=26, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to(pos)


def stage_tag(k):
    return chip(f"stage {k}", GREY, 26).move_to([-5.7, 3.25, 0])


def tag_for(n, i, pos, text="fixed for good", size=26, at=1.25):
    c = chip(text, PINK, size).move_to(pos)
    p = n.pt(i, at)
    ln = Line(p, c.get_bottom(), color=PINK, stroke_width=4)
    dot = Dot(p, radius=0.09, color=PINK)
    return VGroup(ln, dot, c)


def hyp_card(text, color, y):
    box = RoundedRectangle(corner_radius=0.2, width=4.8, height=1.5, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.12).move_to([4.2, y, 0])
    t = T(text, 34, color).move_to(box)
    return VGroup(box, t)


def cite(text, pos, size=28):
    return T(text, size, GREY).move_to(pos)


# ---------------------------------------------------------------- runners (races on a track)
class Runners:
    def __init__(self, x0, x1, ys, scale, cols=None, r=0.2):
        self.x0, self.s, self.ys = x0, scale, ys
        cols = cols or [GREY] * 5
        self.d = [ValueTracker(0.0) for _ in ys]
        self.lanes = VGroup(*[Line([x0 - 0.25, y, 0], [x1, y, 0], color=GREY, stroke_width=2, stroke_opacity=0.5)
                              for y in ys])
        pad = min(0.55, abs(ys[0] - ys[1]) * 0.75)
        self.start = Line([x0, ys[0] + pad, 0], [x0, ys[-1] - pad, 0], color=TEXT, stroke_width=4)
        self.bars, self.dots = [], []
        for i, y in enumerate(ys):
            bar = Line([x0, y, 0], [x0 + 0.02, y, 0], color=cols[i], stroke_width=9)

            def fb(m, i=i, y=y):
                m.put_start_and_end_on([self.x0, y, 0], [self.x0 + max(self.d[i].get_value() * self.s, 0.02), y, 0])

            bar.add_updater(fb)
            fb(bar)
            dot = Dot(radius=r, color=cols[i])

            def fd(m, i=i, y=y):
                m.move_to([self.x0 + max(self.d[i].get_value() * self.s, 0.02), y, 0])

            dot.add_updater(fd)
            fd(dot)
            self.bars.append(bar)
            self.dots.append(dot)
        self.group = VGroup(self.lanes, self.start, *self.bars, *self.dots)

    def rc(self, i, col):
        return [self.bars[i].animate.set_color(col), self.dots[i].animate.set_color(col)]

    def tip(self, i):
        return np.array([self.x0 + self.d[i].get_value() * self.s, self.ys[i], 0.0])


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "One Axon, Many Dendrites: Neuronal Polarity"
    TITLE = "Five Stages and a Race"


class S01(SpokenScene):
    def construct(self):
        c = np.array([0.0, 0.15, 0.0])
        n = Neuron(c, [0.06] * 5)
        self.add(n.group)
        self.play(*[t.animate.set_value(2.6) for t in n.tr], run_time=1.0)
        qs = VGroup(*[T("?", 56, GOLD, weight=BOLD).move_to(n.pt(i, 3.2)) for i in range(5)])
        self.at("neurites truly equal")
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.25), run_time=1.6)
        self.at("fixed as the axon")
        self.play(*[q.animate.set_opacity(0.3) for q in qs[1:]], Indicate(qs[0], scale_factor=1.5, color=GOLD),
                  run_time=0.8)
        self.finish()


def pyramid(c, s=1.15):
    tri = Polygon([0, 0.3, 0], [-0.26, -0.2, 0], [0.26, -0.2, 0], stroke_color=GREY, stroke_width=3,
                  fill_color=SOMA_FILL, fill_opacity=1)
    ap = Line([0, 0.3, 0], [0, 0.68, 0], color=GREY, stroke_width=3)
    bl = Line([-0.2, -0.17, 0], [-0.48, -0.45, 0], color=GREY, stroke_width=3)
    br = Line([0.2, -0.17, 0], [0.48, -0.45, 0], color=GREY, stroke_width=3)
    ax = Line([0, -0.2, 0], [0, -0.56, 0], color=GREY, stroke_width=3)
    return VGroup(ap, bl, br, ax, tri).scale(s).move_to(c)


DISH_C = np.array([3.9, 0.4, 0.0])
PYR_OFF = [(-1.0, 0.9), (0.9, 0.8), (1.3, -0.3), (-1.3, -0.6), (0.1, 0.0), (0.4, -1.2)]


def brain_group():
    bc = np.array([-3.7, 0.4, 0.0])

    def part(w, h, off):
        return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL,
                       fill_opacity=1).move_to(bc + np.array([off[0], off[1], 0]))

    body = VGroup(part(1.1, 0.9, (-2.35, -0.35)), part(1.6, 1.25, (1.75, -1.3)), part(4.2, 3.4, (0.0, 0.2)))
    hip = Arc(radius=0.8, start_angle=0.2 * PI, angle=1.35 * PI, stroke_color=TEXT, stroke_width=16)
    hip.move_to(bc + np.array([0.1, 0.1, 0]))
    return body, hip, bc


class S02(SpokenScene):
    def construct(self):
        body, hip, bc = brain_group()
        head = cite("Banker laboratory", [0, 3.4, 0])
        self.add(head, body)
        self.at("grew neurons")
        arrow = Arrow([-0.8, 0.4, 0], [1.3, 0.4, 0], color=TEXT, buff=0, stroke_width=6)
        dish = Circle(radius=2.3, stroke_color=GREY, stroke_width=4).move_to(DISH_C)
        self.play(GrowArrow(arrow), Create(dish), run_time=1.0)
        self.at("embryonic rat")
        bl = lab("embryonic rat brain", bc + DOWN * 2.2, 26, GREY)
        self.play(FadeIn(bl), run_time=0.5)
        self.at("hippocampus")
        hl = lab("hippocampus", bc + UP * 2.6, 26, TEXT)
        ld = Line(bc + np.array([0.1, 0.9, 0]), hl.get_bottom() + DOWN * 0.05, color=TEXT, stroke_width=3)
        self.play(FadeIn(hip), FadeIn(hl), Create(ld), run_time=0.9)
        self.at("pyramidal cells")
        pyr = VGroup(*[pyramid(DISH_C + np.array([x, y, 0])) for x, y in PYR_OFF])
        un = lab("a fairly uniform population", DISH_C + DOWN * 2.75, 26, TEXT)
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in pyr], lag_ratio=0.2), FadeIn(un), run_time=1.3)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        body, hip, bc = brain_group()
        head = cite("Banker laboratory", [0, 3.4, 0])
        arrow = Arrow([-0.8, 0.4, 0], [1.3, 0.4, 0], color=TEXT, buff=0, stroke_width=6)
        dish = Circle(radius=2.3, stroke_color=GREY, stroke_width=4).move_to(DISH_C)
        pyr = VGroup(*[pyramid(DISH_C + np.array([x, y, 0])) for x, y in PYR_OFF])
        bl = lab("embryonic rat brain", bc + DOWN * 2.2, 26, GREY)
        hl = lab("hippocampus", bc + UP * 2.6, 26, TEXT)
        ld = Line(bc + np.array([0.1, 0.9, 0]), hl.get_bottom() + DOWN * 0.05, color=TEXT, stroke_width=3)
        un = lab("a fairly uniform population", DISH_C + DOWN * 2.75, 26, TEXT)
        left = VGroup(body, hip, bl, hl, ld, head, arrow, un)
        dishg = VGroup(dish, pyr)
        self.add(left, dishg)
        self.play(FadeOut(left), dishg.animate.scale(1.35).move_to([0, 0.2, 0]), run_time=0.5)
        self.at("low density")
        ld_ = lab("low density", [0, -3.4, 0], 30, TEXT)
        self.play(FadeIn(ld_), run_time=0.3)
        self.at("each neuron")
        pick = pyr[4]
        pc = pick.get_center()
        r1 = ring(pc, GOLD, 0.95)
        self.play(FadeIn(r1, scale=1.3), run_time=0.2)
        self.play(FadeOut(r1), FadeOut(ld_), FadeOut(dish), *[FadeOut(p) for i, p in enumerate(pyr) if i != 4],
                  pick.animate.scale(2.4, about_point=pc).shift(np.array([0, -0.2, 0]) - pc), run_time=0.7)
        cell = Circle(radius=1.9, stroke_color=GREY, stroke_width=5, fill_color=SOMA_FILL, fill_opacity=1)
        cell.move_to([0, -0.2, 0])
        self.play(ReplacementTransform(pick, cell), run_time=0.3)
        self.at("on its own")
        ctr = Ctr("day 0.0")
        self.play(FadeIn(ctr.group), run_time=0.4)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        rows = row_boxes()
        for b in rows:
            b[1].set_opacity(0)
        year = T("1988", 40, GOLD, font=TITLE_FONT)
        names = VGroup(T("Dotti,", 40), T("Sullivan and", 40), T("Banker", 40))
        line = VGroup(year, names[0], names[1], names[2]).arrange(RIGHT, buff=0.35).move_to([0, 3.05, 0])
        self.add(rows)
        self.play(FadeIn(year, shift=UP * 0.15), run_time=0.5)
        self.at("Carlos")
        self.play(FadeIn(names[0], shift=UP * 0.15), run_time=0.4)
        self.at("Sullivan")
        self.play(FadeIn(names[1], shift=UP * 0.15), run_time=0.4)
        self.at("Banker described")
        self.play(FadeIn(names[2], shift=UP * 0.15), run_time=0.4)
        self.at("five stages")
        self.play(LaggedStart(*[b[1].animate.set_opacity(1) for b in rows], lag_ratio=0.25), run_time=1.0)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        rows = row_boxes()
        year = T("1988", 40, GOLD, font=TITLE_FONT)
        names = VGroup(T("Dotti,", 40), T("Sullivan and", 40), T("Banker", 40))
        line = VGroup(year, names[0], names[1], names[2]).arrange(RIGHT, buff=0.35).move_to([0, 3.05, 0])
        self.add(rows, line)
        col = Column()
        v = veil_full(3.0).move_to(C5)
        v.save_state()
        v.scale(0.02)
        self.add(v)
        n = Neuron(C5, [0.06] * 5)
        n.group.remove(*n.polys, *n.tips)       # only the round cell at first
        soma = n.soma
        soma.scale(1.8)                          # a big round cell, radius 1.0
        self.at("Stage one")
        boxg = VGroup(*col.boxes)
        self.play(ReplacementTransform(rows, boxg), FadeOut(line), FadeIn(soma), run_time=1.0)
        self.remove(boxg)
        self.add(col.group)
        self.bring_to_front(soma)
        self.play(*col.activate(1), run_time=0.4)
        self.at("Within hours")
        ctr = Ctr("hours")
        self.play(FadeIn(ctr.group), run_time=0.4)
        self.at("the round cell")
        self.play(Indicate(soma, scale_factor=1.15, color=TEXT), run_time=0.7)
        self.at("spreads thin")
        self.play(Restore(v), run_time=1.1)
        self.bring_to_front(soma)
        self.at("flat veils")
        edge = C5 + veil_edge(3.0, 0.0)
        lm = lab("lamellipodia", [5.45, -0.3, 0], 30, TEXT)
        ln = Line(lm.get_left() + LEFT * 0.1, edge + RIGHT * 0.06, color=TEXT, stroke_width=3)
        self.play(FadeIn(lm), Create(ln), run_time=0.6)
        self.at("of membrane")
        self.play(FadeOut(lm), FadeOut(ln), run_time=0.15)
        col.fly(self, 1, [v, soma], run=0.8)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        col = Column(active=1, filled=[1])
        v = veil_full(3.0).move_to(C5)
        n = Neuron(C5, [0.06] * 5)
        n.soma.scale(1.8)
        ctr = Ctr("hours")
        self.add(col.group, v, n.group, ctr.group)
        clk = ValueTracker(0.0)
        plot = Plot(SIM_A, clk)
        shift = CA - C5
        ctr_new = Ctr("day 0.0").live(clk)
        self.add(plot.tg)
        self.play(FadeOut(ctr.group), run_time=0.3)
        self.play(v.animate.shift(shift).scale(2.3 / 3.0), n.soma.animate.shift(shift).scale(1 / 1.8),
                  FadeIn(plot.frame), *col.activate(2, prev=1), FadeIn(ctr_new.group), run_time=1.0)
        drv = driver(n, plot, clk)
        self.at("The veils condense")
        self.add(drv)
        self.play(clk.animate.set_value(1.0), v.animate.scale(0.25).set_opacity(0), run_time=1.4,
                  rate_func=rate_functions.smooth)
        self.remove(v)
        self.at("short neurites")
        self.play(*[Indicate(t, scale_factor=1.6, color=TEXT) for t in n.tips], run_time=0.7)
        self.at("all alike")
        al = lab("all alike", plot.P(1.0, 2.4) + np.array([1.25, 0.0, 0]), 30, GOLD)
        self.play(FadeIn(al), run_time=0.4)
        col.fly(self, 2, [n.group], run=0.8)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        col = Column(active=2, filled=[1, 2])
        n = Neuron(CA, LS2)
        clk = ValueTracker(1.0)
        plot = Plot(SIM_A, clk)
        ctr = Ctr("day 1.0").live(clk)
        self.add(col.group, n.group, plot.group, ctr.group)
        self.play(*col.activate(3, prev=2), run_time=0.4)
        self.at("After a day")
        self.play(Indicate(ctr.group, scale_factor=1.12, color=TEXT), run_time=0.6)
        drv = driver(n, plot, clk)
        self.at("one neurite grows")
        self.add(drv)
        self.play(clk.animate.set_value(2.0), run_time=2.5, rate_func=rate_functions.linear)
        self.at("It becomes the axon")
        axl = lab("axon", n.pt(0, LS3[0]) + np.array([-0.55, 0.7, 0]), 30, YELLOW)
        self.play(*n.rc(0, YELLOW), plot.rc(0, YELLOW), FadeIn(axl), run_time=0.6)
        col.fly(self, 3, [n.group], run=0.8)
        self.finish()


def branches(n, lens, w_col=BLUE):
    g = VGroup()
    for i in range(1, 5):
        d = n.dirs[i]
        nv = perp(d)
        L = lens[i]
        for f, side_len in ((0.55, 0.75), (0.8, 0.6)):
            p = n.pt(i, L * f)
            for sd in (-1, 1):
                g.add(Line(p, p + d * side_len * 0.8 + nv * sd * side_len * 0.62, color=w_col, stroke_width=5))
        g.add(Line(n.pt(i, L), n.pt(i, L) + d * 0.45, color=w_col, stroke_width=5))
    return g


def spines_for(n, L=DEND_L, w0=0.38, w1=0.10):
    sp, heads, dots = VGroup(), VGroup(), VGroup()
    fr = [0.3, 0.45, 0.6, 0.75, 0.9]
    for i in range(1, 5):
        d = n.dirs[i]
        nv = perp(d)
        for j, f in enumerate(fr):
            side = 1 if (i + j) % 2 == 0 else -1
            wf = (w0 + (w1 - w0) * f) / 2
            base = n.pt(i, L * f) + nv * side * wf
            tip = base + nv * side * 0.3
            sp.add(Line(base, tip, color=BLUE, stroke_width=4))
            heads.add(Dot(tip + nv * side * 0.03, radius=0.1, color=BLUE))
            dots.add(Dot(tip + nv * side * 0.16, radius=0.05, color=TEXT))
    return sp, heads, dots


def mature_cell(center=CM):
    cols = [YELLOW] + [BLUE] * 4
    lens = [AX_L] + [DEND_L] * 4
    n = Neuron(center, lens, cols)
    for i in range(1, 5):
        n.w0[i].set_value(0.38)
        n.w1[i].set_value(0.10)
    br = branches(n, lens)
    return n, br


class S08(SpokenScene):
    def construct(self):
        col = Column(active=3, filled=[1, 2, 3])
        n = Neuron(CA, LS3, [YELLOW] + [GREY] * 4)
        clk = ValueTracker(2.0)
        plot = Plot(SIM_A, clk, cols=[YELLOW] + [GREY] * 4)
        ctr = Ctr("day 2.0").live(clk)
        axl = lab("axon", n.pt(0, LS3[0]) + np.array([-0.55, 0.7, 0]), 30, YELLOW)
        self.add(col.group, n.group, plot.group, ctr.group, axl)
        self.play(*col.activate(4, prev=3), FadeOut(plot.group), FadeOut(axl),
                  n.soma.animate.shift(CM - CA), run_time=1.0)
        dayclk = bg_clock(self, 2.2, 5.0, 2.0, 6.0)
        ctr2 = Ctr("day 2.0").live(dayclk)
        self.remove(ctr.group)
        self.add(ctr2.group, dayclk)
        self.at("the other neurites")
        self.play(*[Indicate(n.tips[i], scale_factor=1.7, color=TEXT) for i in range(1, 5)], run_time=0.5)
        self.at("grow")
        self.play(*[n.tr[i].animate.set_value(DEND_L) for i in range(1, 5)], n.tr[0].animate.set_value(AX_L),
                  run_time=0.8)
        self.at("taper and branch")
        lens = [AX_L] + [DEND_L] * 4
        br = branches(n, lens, BLUE)
        self.play(*[n.w0[i].animate.set_value(0.38) for i in range(1, 5)],
                  *[n.w1[i].animate.set_value(0.10) for i in range(1, 5)],
                  *[a for i in range(1, 5) for a in n.rc(i, BLUE)], run_time=0.4)
        self.play(LaggedStart(*[Create(b) for b in br], lag_ratio=0.05), run_time=0.5)
        self.at("as dendrites")
        dl = lab("dendrites", n.pt(2, DEND_L) + np.array([-0.3, 0.75, 0]), 30, BLUE)
        self.play(FadeIn(dl), run_time=0.3)
        self.wait(0.8)
        col.fly(self, 4, [n.group, br], run=0.7)
        self.play(FadeOut(dl), run_time=0.2)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        col = Column(active=4, filled=[1, 2, 3, 4])
        n, br = mature_cell()
        ctr = Ctr("day 6.0")
        self.add(col.group, n.group, br, ctr.group)
        sp, heads, dots = spines_for(n)
        self.play(*col.activate(5, prev=4), run_time=0.4)
        self.at("second week")
        self.play(Transform(ctr.txt, M("week 2", 28).move_to(ctr.box.get_center())), run_time=0.5)
        self.at("spines form")
        hp = heads[1 * 5 + 3].get_center()
        sl = lab("spines", hp + np.array([-1.3, 1.1, 0]), 28, BLUE)
        sll = Line(sl.get_right() + RIGHT * 0.08, hp + np.array([-0.08, 0.1, 0]), color=BLUE, stroke_width=3)
        self.play(LaggedStart(*[AnimationGroup(Create(s), FadeIn(h, scale=0.3)) for s, h in zip(sp, heads)],
                              lag_ratio=0.04), run_time=0.75)
        self.play(FadeIn(sl), Create(sll), run_time=0.3)
        self.at("synapses multiply")
        dp = dots[2 * 5 + 3].get_center()
        dl = lab("synapses", dp + np.array([-0.5, -1.05, 0]), 28, TEXT)
        dll = Line(dl.get_top() + UP * 0.06, dp + np.array([0.0, -0.1, 0]), color=TEXT, stroke_width=3)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.03), run_time=0.5)
        self.play(FadeIn(dl), Create(dll), run_time=0.2)
        col.fly(self, 5, [n.group, br, sp, heads, dots], run=0.6)
        # A full two seconds with all five completed stage boxes visible.
        self.wait(2.0)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        col = Column(active=5, filled=[1, 2, 3, 4, 5])
        ctr = Ctr("week 2")
        self.add(col.group, ctr.group)
        n = Neuron(CA, LS2)
        clk = ValueTracker(1.0)
        plot = Plot(SIM_A, clk)
        cp = col.icons[2].copy()
        s = n.group.height / cp.height
        self.at("Back to stage")
        self.add(cp)
        self.play(cp.animate.scale(s).move_to(n.group.get_center()), *col.activate(2, prev=5),
                  Transform(ctr.txt, M("day 1.0", 28).move_to(ctr.box.get_center())),
                  FadeIn(plot.group), run_time=1.2)
        self.remove(cp)
        self.add(n.group)
        ctr.live(clk)
        self.at("neurites look alike")
        self.play(*[Indicate(t, scale_factor=1.6, color=TEXT) for t in n.tips],
                  *[Indicate(t, color=TEXT) for t in plot.traces], run_time=0.9)
        self.at("mean two things")
        self.play(FadeOut(col.group), FadeOut(ctr.group), FadeIn(stage_tag(2)), n.soma.animate.shift(CB - CA),
                  run_time=0.7)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        n = Neuron(CB, LS2)
        clk = ValueTracker(1.0)
        plot = Plot(SIM_A, clk)
        self.add(n.group, plot.group, stage_tag(2))
        self.at("one was fixed")
        tg = tag_for(n, 0, [-0.7, 1.45, 0])
        self.play(Create(tg[0]), FadeIn(tg[1]), FadeIn(tg[2], shift=UP * 0.15), run_time=0.8)
        self.at("as the axon")
        self.play(Indicate(tg[2], scale_factor=1.12, color=PINK), run_time=0.5)
        self.finish()


RUN_YS = [1.9, 0.95, 0.0, -0.95, -1.9]


class S12(SpokenScene):
    def construct(self):
        n = Neuron(CB, LS2)
        clk = ValueTracker(1.0)
        plot = Plot(SIM_A, clk)
        tg = tag_for(n, 0, [-0.7, 1.45, 0])
        self.add(n.group, plot.group, tg, stage_tag(2))
        rn = Runners(3.2, 6.5, RUN_YS, 1.0)
        tip_nums = VGroup(*[T(str(i + 1), 30, TEXT, weight=BOLD).move_to(n.pt(i, LS2[i] + 0.5)) for i in range(5)])
        lane_nums = VGroup(*[T(str(i + 1), 30, TEXT, weight=BOLD).move_to([2.75, y, 0]) for i, y in enumerate(RUN_YS)])
        flag = VGroup(Line([3.2, RUN_YS[0], 0], [3.2, RUN_YS[0] + 0.6, 0], color=PINK, stroke_width=4),
                      Polygon([3.2, RUN_YS[0] + 0.6, 0], [3.2, RUN_YS[0] + 0.3, 0], [3.65, RUN_YS[0] + 0.45, 0],
                              stroke_width=0, fill_color=PINK, fill_opacity=1))
        self.play(FadeOut(plot.group), FadeIn(rn.group), FadeIn(tip_nums), FadeIn(lane_nums), FadeIn(flag),
                  run_time=0.8)
        self.at("choice is open")
        cl = lab("can be reassigned", [4.8, 3.05, 0], 28, GOLD)
        self.play(FadeIn(cl, shift=UP * 0.1), run_time=0.5)
        self.at("they are competing")
        self.play(*[rn.d[i].animate.set_value(0.5) for i in range(5)], run_time=0.5)
        self.play(*[rn.d[i].animate.set_value(v) for i, v in enumerate([1.3, 1.0, 1.5, 1.2, 1.6])], run_time=0.8,
                  rate_func=rate_functions.ease_in_out_sine)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        n = Neuron(CB, LS2)
        clk = ValueTracker(1.0)
        plot = Plot(SIM_A, clk)
        tg = tag_for(n, 0, [-0.7, 1.45, 0])
        rn = Runners(3.2, 6.5, RUN_YS, 1.0)
        for i, v in enumerate([1.3, 1.0, 1.5, 1.2, 1.6]):
            rn.d[i].set_value(v)
        cl = lab("can be reassigned", [4.8, 3.05, 0], 28, GOLD)
        tip_nums = VGroup(*[T(str(i + 1), 30, TEXT, weight=BOLD).move_to(n.pt(i, LS2[i] + 0.5)) for i in range(5)])
        lane_nums = VGroup(*[T(str(i + 1), 30, TEXT, weight=BOLD).move_to([2.75, y, 0]) for i, y in enumerate(RUN_YS)])
        flag = VGroup(Line([3.2, RUN_YS[0], 0], [3.2, RUN_YS[0] + 0.6, 0], color=PINK, stroke_width=4),
                      Polygon([3.2, RUN_YS[0] + 0.6, 0], [3.2, RUN_YS[0] + 0.3, 0], [3.65, RUN_YS[0] + 0.45, 0],
                              stroke_width=0, fill_color=PINK, fill_opacity=1))
        st = stage_tag(2)
        self.add(n.group, tg, rn.group, cl, tip_nums, lane_nums, flag, st)
        t1 = T("A young neuron's cut", 46, TEXT, font=TITLE_FONT).move_to([2.7, 0.6, 0])
        self.play(FadeOut(VGroup(tg, rn.group, cl, tip_nums, lane_nums, flag, st)), FadeIn(t1, shift=UP * 0.15),
                  run_time=0.6)
        self.at("tests whether")
        t2 = T("Can the choice be undone?", 40, GOLD).move_to([2.7, -0.55, 0])
        self.play(FadeIn(t2, shift=UP * 0.15), run_time=0.5)
        self.finish()


def blade_shape():
    """A knife whose tip is at the origin and points down."""
    bl = Polygon([0, 0, 0], [0.16, 1.0, 0], [-0.16, 1.0, 0], stroke_width=0, fill_color=RED, fill_opacity=1)
    hd = Rectangle(width=0.24, height=0.6, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([0, 1.3, 0])
    return VGroup(bl, hd)


class S14(SpokenScene):
    def construct(self):
        n = Neuron(CB, LS3, [YELLOW] + [GREY] * 4)
        clk = ValueTracker(2.0)
        plot = Plot(SIM_A, clk, cols=[YELLOW] + [GREY] * 4)
        self.add(n.group, plot.group)
        self.at("at stage three")
        st = chip("stage 3", GREY, 26).move_to([-5.7, 3.25, 0])
        self.play(FadeIn(st), run_time=0.4)
        self.at("cut its leader")
        d = n.dirs[0]
        nv = perp(d)
        p = n.pt(0, L_CUT)
        blade = blade_shape()
        blade.rotate(np.radians(DIRS[0]), about_point=ORIGIN)
        blade.shift(p + nv * 1.3)
        self.play(FadeIn(blade, shift=DOWN * 0.2), run_time=0.2)
        self.play(blade.animate.shift(-nv * 1.6), run_time=0.35)
        frag = fragment(n, 0, L_CUT, LS3[0], YELLOW)
        n.tr[0].set_value(L_CUT)
        self.add(frag)
        cl = plot.cutline()
        tk = tickmark(n, 0, L_CUT)
        self.play(FadeOut(blade), frag.animate.shift(d * 0.5 + DOWN * 1.9).rotate(0.9).set_opacity(0),
                  FadeIn(tk), FadeIn(cl), run_time=0.8)
        self.remove(frag)
        self.at("length of its siblings")
        rg = DashedVMobject(Circle(radius=L_CUT, stroke_color=GREY, stroke_width=3).move_to(CB), num_dashes=40)
        self.play(Create(rg), run_time=0.7)
        self.at("erasing its lead")
        p0, p1 = plot.P(2.0, LS3[0]), plot.P(2.0, L_CUT)
        path = Line(p0, p1, color=YELLOW, stroke_width=7)
        dot = Dot(p0, radius=0.13, color=YELLOW)
        self.add(dot)
        self.play(Create(path), MoveAlongPath(dot, path), run_time=0.6, rate_func=rate_functions.ease_in_quad)
        clk.set_value(2.0 + DT)
        self.remove(path, dot)
        el = lab("lead\nerased", [6.0, 1.75, 0], 26, GOLD)
        bc, bcl = before_cut(plot)
        self.play(*n.rc(0, GREY), plot.rc(0, GREY), FadeIn(el), FadeIn(bc), Create(bcl), run_time=0.7)
        self.finish()


def before_cut(plot):
    bc = T("before the cut", 24, GREY).move_to([3.7, 2.35, 0])
    hp = plot.P(1.9, float(SIM_A[0, 190]))
    bcl = Line(bc.get_right() + RIGHT * 0.06, hp + UP * 0.05, color=GREY, stroke_width=3)
    return bc, bcl


def post_cut_cell(yellow_stump=False, center=CB, lens=None):
    n = Neuron(center, lens or LPOST, [YELLOW if yellow_stump else GREY] + [GREY] * 4)
    return n, tickmark(n, 0, L_CUT)


def stump_card_line(n, card, col=PINK):
    p = n.pt(0, 1.9)
    return VGroup(Line(card.get_left(), p, color=col, stroke_width=4), Dot(p, radius=0.09, color=col))


class S15(SpokenScene):
    def construct(self):
        n, tk = post_cut_cell()
        self.add(n.group, tk)
        self.at("fixed for good")
        cardA = hyp_card("Fixed for good", PINK, 1.9)
        cn = stump_card_line(n, cardA)
        self.play(FadeIn(cardA, shift=LEFT * 0.2), Create(cn[0]), FadeIn(cn[1]), run_time=0.7)
        self.at("which process should")
        q = T("?", 80, GOLD, weight=BOLD).move_to([-3.3, 3.15, 0])
        qt = lab("Which grows out as the axon?", [-3.3, -3.35, 0], 28, GOLD)
        self.play(FadeIn(q, scale=0.5), FadeIn(qt), run_time=0.7)
        self.at("And if the neurites")
        cardB = hyp_card("Can be reassigned", GOLD, -1.7)
        self.play(FadeIn(cardB, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


class S16Pause(NarratedScene):
    def construct(self):
        n, tk = post_cut_cell()
        cardA = hyp_card("Fixed for good", PINK, 1.9)
        cn = stump_card_line(n, cardA)
        q = T("?", 80, GOLD, weight=BOLD).move_to([-3.3, 3.15, 0])
        qt = lab("Which grows out as the axon?", [-3.3, -3.35, 0], 28, GOLD)
        self.add(n.group, tk, cardA, cn, hyp_card("Can be reassigned", GOLD, -1.7), q, qt)
        pp = T("Pause. Predict.", 40, TEXT).move_to([4.2, 0.55, 0])
        track = Line([1.9, -0.15, 0], [6.5, -0.15, 0], color=GREY, stroke_width=3, stroke_opacity=0.5)
        tr = bg_clock(self, 0.0, 5.0, 1.0, 0.0)
        bar = Line([1.9, -0.15, 0], [6.5, -0.15, 0], color=GOLD, stroke_width=10)

        def fb(m):
            m.put_start_and_end_on([1.9, -0.15, 0], [1.9 + 4.6 * max(tr.get_value(), 0.003), -0.15, 0])

        bar.add_updater(fb)
        self.add(tr)
        self.play(FadeIn(pp), FadeIn(track), FadeIn(bar), run_time=0.3)
        self.wait(self.narration_s - 0.3)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        n, tk = post_cut_cell()
        cardA = hyp_card("Fixed for good", PINK, 1.9)
        cardB = hyp_card("Can be reassigned", GOLD, -1.7)
        cn = stump_card_line(n, cardA)
        q = T("?", 80, GOLD, weight=BOLD).move_to([-3.3, 3.15, 0])
        qt = lab("Which grows out as the axon?", [-3.3, -3.35, 0], 28, GOLD)
        self.add(n.group, tk, cardA, cn, cardB, q, qt)
        self.play(FadeOut(q), FadeOut(qt), run_time=0.4)
        self.at("choice were fixed")
        self.play(Indicate(cardA[0], scale_factor=1.04, color=PINK), run_time=0.7)
        self.at("the stump should regrow")
        e = n.pt(0, 4.4)
        ghost = DashedLine(n.pt(0, L_CUT + 0.25), e, color=YELLOW, stroke_width=12, dash_length=0.2)
        gl = lab("if fixed: stump regrows", e + np.array([2.25, 0.05, 0]), 26, YELLOW)
        self.play(Create(ghost), FadeIn(gl), run_time=1.2)
        self.at("whatever its length")
        self.play(Indicate(gl, scale_factor=1.08, color=TEXT), run_time=0.8)
        self.at("Often, it did")
        xx = Cross(Dot(e, radius=0.2), stroke_color=RED, stroke_width=8).scale(1.3)
        self.play(FadeIn(xx, scale=0.6), ghost.animate.set_opacity(0.35), run_time=0.35)
        strike = Line(cardA.get_left() + RIGHT * 0.3, cardA.get_right() + LEFT * 0.3, color=RED, stroke_width=7)
        self.play(Create(strike), cardA.animate.set_opacity(0.45), cn.animate.set_opacity(0.35), run_time=0.5)
        self.wait(0.5)
        L3 = float(SIM_B[3, K - 1])
        self.play(*n.rc(3, YELLOW), n.tr[3].animate.set_value(L3), FadeOut(gl), run_time=0.9)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        L3 = float(SIM_B[3, K - 1])
        lens = [float(SIM_B[i, K - 1]) for i in range(5)]
        n = Neuron(CB, lens, [GREY, GREY, GREY, YELLOW, GREY])
        tk = tickmark(n, 0, L_CUT)
        cardA = hyp_card("Fixed for good", PINK, 1.9)
        cardA.set_opacity(0.45)
        cn = stump_card_line(n, cardA)
        cn.set_opacity(0.35)
        strike = Line(cardA.get_left() + RIGHT * 0.3, cardA.get_right() + LEFT * 0.3, color=RED, stroke_width=7)
        cardB = hyp_card("Can be reassigned", GOLD, -1.7)
        e = n.pt(0, 4.4)
        ghost = DashedLine(n.pt(0, L_CUT + 0.25), e, color=YELLOW, stroke_width=12, dash_length=0.2)
        ghost.set_opacity(0.35)
        xx = Cross(Dot(e, radius=0.2), stroke_color=RED, stroke_width=8).scale(1.3)
        self.add(n.group, tk, ghost, xx, cardA, strike, cn, cardB)
        clk = ValueTracker(3.0)
        plot = Plot(SIM_B, clk, cols=[GREY, GREY, GREY, YELLOW, GREY])
        cl = plot.cutline()
        drv = driver(n, plot, clk)
        self.add(drv)
        chipA = VGroup(chip("Fixed for good", PINK, 24), Line(LEFT * 1.1, RIGHT * 1.1, color=RED, stroke_width=6))
        chipA.set_opacity(0.6)
        chipA.move_to([-5.0, 3.25, 0])
        self.at("In 1987")
        yr = T("1987", 36, GOLD, font=TITLE_FONT)
        who = T("Dotti and Banker", 28, GREY)
        ci = VGroup(yr, who).arrange(RIGHT, buff=0.3).move_to([-1.2, 3.25, 0])
        ci.move_to([-3.1 + ci.width / 2, 3.25, 0])
        who.set_opacity(0)
        self.add(who)
        self.play(ReplacementTransform(cardA, chipA[0]), ReplacementTransform(strike, chipA[1]), FadeOut(cardB),
                  FadeOut(cn), FadeOut(ghost), FadeOut(xx), FadeIn(plot.group), FadeIn(cl), FadeIn(yr),
                  run_time=0.8)
        bc18, bcl18 = before_cut(plot)
        self.at("Carlos")
        self.play(who.animate.set_opacity(1), FadeIn(bc18), FadeIn(bcl18), run_time=0.4)
        self.at("another")
        rp = lab("replay", [-1.0, -3.3, 0], 26, GREY)
        self.play(*n.rc(3, BLUE), plot.rc(3, BLUE), clk.animate.set_value(2.0 + DT), FadeIn(rp), run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.at("a future dendrite")
        fd = lab("future dendrite", [-4.6, -3.3, 0], 28, BLUE)
        fl = Line(fd.get_top() + UP * 0.05, n.pt(3, L_CUT), color=BLUE, stroke_width=3)
        self.play(FadeIn(fd), Create(fl), run_time=0.5)
        self.at("could grow out", lead=0)
        # Keep the label and sibling blue throughout "future dendrite".
        ax = lab("axon", [-4.6, -3.3, 0], 28, YELLOW)
        self.play(*n.rc(3, YELLOW), plot.rc(3, YELLOW), FadeOut(fl), FadeOut(rp),
                  ReplacementTransform(fd, ax), FadeOut(bc18), FadeOut(bcl18),
                  FadeOut(plot.traces[0]), run_time=0.3)
        self.play(clk.animate.set_value(3.0), run_time=1.0, rate_func=rate_functions.linear)
        self.at("as the axon")
        self.play(Indicate(ax, color=YELLOW, scale_factor=1.05), run_time=0.3)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        cen = [(-4.4, 1.1), (0.0, 1.1), (4.4, 1.1), (-4.4, -2.0), (0.0, -2.0), (4.4, -2.0)]
        rot = [0, 144, 72, 216, 288, 36]
        stumps = [0.45, 0.75, 1.0, 1.3, 0.6, 0.9]
        ns = []
        for (x, y), r, s in zip(cen, rot, stumps):
            ang = [a + r for a in DIRS]
            nn = Neuron(np.array([x, y, 0.0]), [1.7, 1.3, 1.3, 1.3, 1.3], [YELLOW] + [GREY] * 4, angles=ang, w=0.16,
                        soma_r=0.26, tip_r=0.08)
            ns.append(nn)
        ci = cite("Goslin and Banker", [0, 3.35, 0])
        self.add(ci, *[nn.group for nn in ns])
        self.at("cut axons")
        blades, frags = VGroup(), []
        for nn, s in zip(ns, stumps):
            d = nn.dirs[0]
            blades.add(DashedLine(nn.pt(0, s) + perp(d) * 0.35, nn.pt(0, s) - perp(d) * 0.35, color=RED,
                                  stroke_width=5, dash_length=0.08))
            frags.append(fragment(nn, 0, s, 1.7, YELLOW, w=0.16))
        self.play(Create(blades), run_time=0.5)
        for nn, s, fg in zip(ns, stumps, frags):
            nn.tr[0].set_value(s)
            self.add(fg)
        self.play(FadeOut(blades), *[fg.animate.shift(RIGHT * 0.0).set_opacity(0) for fg in frags], run_time=0.7)
        self.at("different lengths")
        ticks = VGroup(*[tickmark(nn, 0, s, off=0.06) for nn, s in zip(ns, stumps)])
        self.play(FadeIn(ticks), run_time=0.5)
        self.finish()


def ruler_for(n, i, La, Lb, side, text):
    d = n.dirs[i]
    nv = perp(d) * side
    a, b = n.pt(i, La), n.pt(i, Lb)
    line = Line(a, b, color=GOLD, stroke_width=5)
    t1 = Line(a + nv * 0.15, a - nv * 0.15, color=GOLD, stroke_width=5)
    t2 = Line(b + nv * 0.15, b - nv * 0.15, color=GOLD, stroke_width=5)
    ruler = VGroup(line, t1, t2)

    def follow_tip(_):
        # The measured lead starts on the siblings' ring and ends on this tip.
        tip = n.pt(i, n.tr[i].get_value())
        line.put_start_and_end_on(a, tip)
        t2.put_start_and_end_on(tip + nv * 0.15, tip - nv * 0.15)

    ruler.add_updater(follow_tip)
    mid = (a + b) / 2
    rl = M(text, 28, GOLD).move_to(mid + nv * 0.7 + (RIGHT * 0.5 if side < 0 else np.zeros(3)))
    return ruler, rl


class S20(SpokenScene):
    def construct(self):
        # case A: the stump is ahead
        LA = [3.05] + [float(SIM_STUMP[i, KCUT + 1]) for i in range(1, 5)]
        nA = Neuron(CB, LA)
        tkA = tickmark(nA, 0, 3.05, off=0.0)
        clkA = ValueTracker(2.0 + DT)
        plotA = Plot(SIM_STUMP, clkA)
        clA = plotA.cutline()
        chA = T("in some neurons, the stump leads", 26, TEXT).move_to([-3.1, -3.35, 0])
        bcA, bclA = before_cut(plotA)
        self.add(nA.group, tkA, plotA.group, clA, bcA, bclA)
        self.at("remaining process")
        rr = max(LA[1:])
        rgA = DashedVMobject(Circle(radius=rr, stroke_color=GREY, stroke_width=3).move_to(CB), num_dashes=40)
        self.play(Create(rgA), Indicate(nA.tips[0], scale_factor=1.8, color=TEXT), run_time=0.7)
        self.at("more than about")
        rulerA, rlA = ruler_for(nA, 0, rr, 3.05, +1, "> ~10 µm")
        self.play(Create(rulerA), FadeIn(rlA), FadeIn(chA), run_time=0.7)
        drvA = driver(nA, plotA, clkA)
        self.add(drvA)
        self.play(clkA.animate.set_value(3.0), run_time=0.8, rate_func=rate_functions.linear)
        self.play(*nA.rc(0, YELLOW), plotA.rc(0, YELLOW), run_time=0.3)
        # case B: a sibling is ahead
        self.at("all the others")
        LB = [float(SIM_B2[i, KCUT + 1]) for i in range(5)]
        nB = Neuron(CB, LB)
        tkB = tickmark(nB, 0, LB[0])
        clkB = ValueTracker(2.0 + DT)
        plotB = Plot(SIM_B2, clkB)
        clB = plotB.cutline()
        chB = T("in others, a sibling leads", 26, TEXT).move_to([-3.1, -3.35, 0])
        rrB = max(LB[2:])
        rgB = DashedVMobject(Circle(radius=rrB, stroke_color=GREY, stroke_width=3).move_to(CB), num_dashes=40)
        rulerB, rlB = ruler_for(nB, 1, rrB, LB[1], -1, "> ~10 µm")
        self.play(FadeOut(VGroup(nA.group, tkA, plotA.group, clA, rgA, rulerA, rlA, chA, bcA, bclA)), run_time=0.2)
        self.play(FadeIn(VGroup(nB.group, tkB, plotB.group, clB, rgB, rulerB, rlB, chB)), run_time=0.3)
        drvB = driver(nB, plotB, clkB)
        self.add(drvB)
        self.wait(0.15)
        self.play(clkB.animate.set_value(3.0), run_time=0.8, rate_func=rate_functions.linear)
        self.play(*nB.rc(1, YELLOW), plotB.rc(1, YELLOW), run_time=0.3)
        self.finish()


def thumb(win=None, cut=False):
    g = VGroup()
    for j, a in enumerate(DIRS):
        d = u(a)
        L = 0.55 if j == win else 0.3
        g.add(Line(d * 0.08, d * L, color=YELLOW if j == win else GREY, stroke_width=5))
    if cut:
        d = u(DIRS[0])
        nv = perp(d)
        g.add(Line(d * 0.3 + nv * 0.12, d * 0.3 - nv * 0.12, color=RED, stroke_width=5))
    g.add(Circle(radius=0.1, stroke_color=GREY, stroke_width=2, fill_color=SOMA_FILL, fill_opacity=1))
    return g


class S21(SpokenScene):
    def construct(self):
        CS = np.array([-2.8, -0.3, 0.0])
        n, tk = post_cut_cell(center=CS)
        clk = ValueTracker(2.0 + DT)
        plot = Plot(SIM_RUN[1], clk, x0=1.9, sx=4.6, t0=2.0, ticks=False, xlabel="time after cut", kstart=KCUT + 1)
        drv = driver(n, plot, clk)
        slots = []
        for k, y in enumerate([2.55, 0.7, -1.15]):
            box = RoundedRectangle(corner_radius=0.12, width=1.2, height=1.7, stroke_color=GREY, stroke_width=2,
                                   stroke_opacity=0.6).move_to([-6.2, y, 0])
            num = T(str(k + 1), 24, GREY).move_to([-6.2, y - 0.62, 0])
            th = thumb().move_to([-6.2, y + 0.15, 0])
            slots.append((box, num, th))
        self.add(n.group, tk, plot.group, *[VGroup(*s) for s in slots], drv)
        self.at("nearly equal")
        rg = DashedVMobject(Circle(radius=2.42, stroke_color=GREY, stroke_width=3).move_to(CS), num_dashes=40)
        rl = T("run 1", 30, GREY).move_to([5.4, 3.25, 0])
        self.play(Create(rg), FadeIn(rl), run_time=0.3)

        def run(w, sim, k, text, pos, hold):
            plot.L = sim
            tip = CS + n.dirs[w] * float(sim[w, K - 1])
            self.play(clk.animate.set_value(3.0), *n.rc(w, YELLOW), plot.rc(w, YELLOW), run_time=0.6,
                      rate_func=rate_functions.linear)
            lb = T(text, 26, YELLOW).move_to(tip + pos)
            ux = np.sign(pos[0]) * (lb.width / 2 + 0.08) if abs(pos[0]) > abs(pos[1]) else 0.0
            uy = np.sign(pos[1]) * (lb.height / 2 + 0.1) if abs(pos[1]) >= abs(pos[0]) else 0.0
            uv = pos / np.linalg.norm(pos)
            ld = Line(tip + uv * 0.17, tip + pos - np.array([ux, uy, 0.0]), color=YELLOW, stroke_width=3)
            th2 = thumb(w, cut=(w == 0)).move_to(slots[k][2].get_center())
            self.play(FadeIn(lb), Create(ld), Transform(slots[k][2], th2), run_time=0.3)
            self.wait(hold)
            return lb, ld

        lb1, ld1 = run(1, SIM_RUN[1], 0, "new axon", np.array([1.5, 0.1, 0]), 1.1)
        # reset to neutral in the same beat as the new run label
        self.at("predicted")
        rl2 = T("run 2", 30, GREY).move_to(rl.get_center())
        self.play(clk.animate.set_value(2.0 + DT), *n.rc_all([GREY] * 5), *[plot.rc(i, GREY) for i in range(5)],
                  Transform(rl, rl2), FadeOut(lb1), FadeOut(ld1), run_time=0.3)
        lb2, ld2 = run(3, SIM_RUN[3], 1, "new axon", np.array([1.5, -0.6, 0]), 1.1)
        rl3 = T("run 3", 30, GREY).move_to(rl.get_center())
        self.play(clk.animate.set_value(2.0 + DT), *n.rc_all([GREY] * 5), *[plot.rc(i, GREY) for i in range(5)],
                  Transform(rl, rl3), FadeOut(lb2), FadeOut(ld2), run_time=0.3)
        lb3, ld3 = run(0, SIM_RUN[0], 2, "the cut one", np.array([-0.2, 1.0, 0]), 1.3)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        ys = [2.1, 1.05, 0.0, -1.05, -2.1]
        rn = Runners(-4.9, 3.3, ys, 2.9)
        lanes_nums = VGroup(*[T(f"neurite {i + 1}", 24, GREY).move_to([-5.95, y, 0]) for i, y in enumerate(ys)])
        axis = Arrow([-4.9, -3.05, 0], [3.3, -3.05, 0], color=GREY, buff=0, stroke_width=3, tip_length=0.2)
        axl = T("length", 26, GREY).move_to([4.4, -3.05, 0])
        self.add(rn.group, lanes_nums, axis, axl)
        self.play(rn.d[0].animate.set_value(0.45), *rn.rc(0, YELLOW),
                  *[rn.d[i].animate.set_value(0.22) for i in range(1, 5)], run_time=0.3)
        self.at("can be undone")
        self.play(rn.d[3].animate.set_value(0.75), rn.d[0].animate.set_value(0.5),
                  *rn.rc(3, YELLOW), *rn.rc(0, GREY), run_time=0.9)
        self.at("behaves like a race")
        board = VGroup(RoundedRectangle(corner_radius=0.2, width=2.8, height=1.7, stroke_color=GOLD, stroke_width=4,
                                        fill_color=GOLD, fill_opacity=0.1),
                       T("SCORE", 24, GREY), T("length", 44, GOLD)).move_to([5.2, 0.9, 0])
        board[1].move_to(board[0].get_center() + UP * 0.45)
        board[2].move_to(board[0].get_center() + DOWN * 0.25)
        self.play(FadeIn(board, scale=0.8),
                  *[rn.d[i].animate.set_value(v) for i, v in enumerate([0.85, 0.95, 0.8, 1.6, 0.9])], run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(*[rn.d[i].animate.set_value(v) for i, v in enumerate([1.5, 1.6, 1.4, 2.5, 1.5])], run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.at("length is part")
        p0 = rn.tip(1)
        br = DashedLine([p0[0], 2.9, 0], [p0[0], -2.9, 0], color=GOLD, stroke_width=3, dash_length=0.12)
        gap = DoubleArrow([p0[0], -0.55, 0], [rn.tip(3)[0], -0.55, 0], color=GOLD, buff=0, stroke_width=5,
                          tip_length=0.18)
        self.play(Create(br), Create(gap), run_time=0.7)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        n = Neuron(CB, LS2)
        clk = ValueTracker(1.0)
        plot = Plot(SIM_A, clk)
        self.add(n.group, plot.group)
        ci = cite("Goslin and Banker", [-3.3, -3.45, 0])
        self.play(FadeIn(ci), run_time=0.3)
        self.at("proposed")
        ul = lab("proposed: uncut neurons\nchoose the same way", [-3.3, 3.05, 0], 26, TEXT)
        self.play(FadeIn(ul), run_time=0.5)
        drv = driver(n, plot, clk)
        self.at("choose the same")
        self.add(drv)
        self.play(*n.rc(0, YELLOW), plot.rc(0, YELLOW), clk.animate.set_value(2.0), run_time=1.2,
                  rate_func=rate_functions.linear)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        dish = Ellipse(width=9.0, height=5.6, stroke_color=GREY, stroke_width=4).move_to([0, 0, 0])
        self.at("The ten")
        num = M("10 µm", 100, TEXT).move_to([0, -0.2, 0])
        self.add(dish)
        self.play(FadeIn(num, scale=0.8), run_time=0.5)
        self.at("these experiments")
        note = lab("these cultures", [0, 1.85, 0], 32, GREY)
        self.play(FadeIn(note), run_time=0.5)
        self.at("cultured neurons")
        pts = [(-3.0, 0.9), (3.0, 0.9), (-3.0, -1.3), (3.0, -1.3), (-1.4, -1.85), (1.4, -1.85)]
        cells = VGroup(*[Neuron(np.array([x, y, 0.0]), [0.7, 0.55, 0.6, 0.5, 0.65], angles=[a + 20 * k for a in DIRS],
                                w=0.1, soma_r=0.2, tip_r=0.05).group for k, (x, y) in enumerate(pts)])
        self.play(FadeIn(cells, lag_ratio=0.1), run_time=0.9)
        self.at("not a rule")
        small = M("10 µm", 52, TEXT).move_to([-3.6, 0.3, 0])
        note2 = lab("these cultures", [-3.6, -2.35, 0], 26, GREY)
        self.play(dish.animate.scale(0.5).move_to([-3.6, 0.3, 0]), FadeOut(num), FadeOut(note), FadeOut(cells),
                  FadeIn(small), FadeIn(note2), run_time=0.8)
        ar = Arrow([-1.0, 0.3, 0], [1.4, 0.3, 0], color=GREY, buff=0, stroke_width=6)
        cx = Cross(Dot([0.2, 0.3, 0], radius=0.3), stroke_color=RED, stroke_width=8)
        others = VGroup(
            Neuron(np.array([3.5, 2.0, 0.0]), [1.0, 0.8, 0.9], angles=[100, 220, 330], w=0.14, soma_r=0.26,
                   tip_r=0.07).group,
            Neuron(np.array([5.5, 0.3, 0.0]), [0.8, 0.9, 0.7, 0.8, 0.9, 0.7], angles=[0, 60, 120, 180, 240, 300],
                   w=0.14, soma_r=0.26, tip_r=0.07).group,
            Neuron(np.array([3.5, -1.3, 0.0]), [1.0, 1.1], angles=[60, 250], w=0.14, soma_r=0.26,
                   tip_r=0.07).group)
        ol = lab("every neuron", [4.4, -3.1, 0], 28, TEXT)
        self.play(GrowArrow(ar), FadeIn(others), FadeIn(ol), run_time=0.8)
        self.play(Create(cx), run_time=0.4)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        clk = ValueTracker(2.0)
        plot = Plot(SIM_A, clk, x0=-5.2, y0=-2.85, sx=2.9, sy=1.62, lab=28, sw=8,
                    cols=[YELLOW] + [GREY] * 4)
        sib_y = plot.P(2.0, 2.42)
        lead_y = plot.P(2.0, LS3[0])
        xg = sib_y[0] + 0.45
        midy = (sib_y[1] + lead_y[1]) / 2
        gap = DoubleArrow([xg, sib_y[1], 0], [xg, lead_y[1], 0], color=GOLD, buff=0, stroke_width=6, tip_length=0.2)
        fl = lab("far enough ahead", [xg + 2.45, midy, 0], 34, GOLD)
        self.add(plot.group, gap, fl)
        self.at("on the number")
        self.play(Indicate(gap, color=GOLD, scale_factor=1.08), run_time=0.6)
        self.at("far enough ahead")
        self.play(Indicate(fl, color=GOLD, scale_factor=1.04), run_time=0.6)
        self.at("win", lead=0)
        wl = lab("wins", plot.P(2.0, LS3[0]) + np.array([0.9, 0.45, 0]), 40, YELLOW, weight=BOLD)
        self.play(FadeIn(wl), run_time=0.2)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        t1 = T("Stage 2 behaves like a race.", 56, TEXT, font=TITLE_FONT).move_to([0, 0.5, 0])
        t2 = T("Next: What Makes a Winner", 40, GOLD).move_to([0, -0.6, 0])
        # Qualify the spoken shorthand visually; script.json and audio stay final.
        analogy = chip("Race analogy: neurites compete", GOLD, 28).move_to([0, -1.65, 0])
        self.add(t1, t2, analogy)
        self.at("what kind of race")
        self.play(t1.animate.move_to([0, 3.0, 0]), t2.animate.move_to([0, 2.0, 0]),
                  FadeOut(analogy), run_time=0.5)
        rn2 = Runners(-4.2, 4.8, [0.9, 0.0, -0.9, -1.8, -2.7], 1.7, r=0.22)
        self.play(FadeIn(rn2.group), run_time=0.4)
        self.play(*[rn2.d[i].animate.set_value(v) for i, v in enumerate([1.6, 1.8, 1.5, 1.7, 1.6])], run_time=0.5,
                  rate_func=rate_functions.ease_in_out_sine)
        self.at("only one winner")
        self.play(rn2.d[2].animate.set_value(4.2), *rn2.rc(2, YELLOW), run_time=0.9)
        self.finish()


class S27End(EndCard):
    LINE = "Stage two behaves like a race: get far enough ahead and win."
