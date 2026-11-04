"""Neuronal polarity, chapter 4: Rig the Race  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept; shared with the other chapters of this lesson, from scenes.old.py)
  YELLOW = the axon, and a neurite that has been pushed over into becoming one (script says "gold")
  BLUE   = dendrites (not used in this chapter)
  GREY   = cell body, neurites not chosen, outlines, dishes, axes, citations
  GREEN  = PIP3 / the positive loop (loop arrows, the PI3-kinase chips)
  RED    = a blocked step (crosses, stop bars), "no axon", a result that does not match
  ORANGE = actin (growth-cone mesh, the actin chip)
  TEAL   = microtubules
  GOLD   = the open question and the idea of a threshold (question marks, the dashed line)
  PINK   = a drug (cytochalasin D, taxol, its puffs and the wash). In chapter 2 PINK tagged the
           "fixed for good" idea; here it is only ever a drug.
  TEXT   = labels, flashes
  (series colour not used here: PURPLE ankyrin G and the initial segment)

Everything drawn from numbers is computed: the bars in s21 are the lesson's race model (shared supply
split in proportion to length squared, fixed cost 2 um/h per neurite, floor 2 um) run with the supply
tripled to 60 um/h from four neurites at 15 um and one at 20 um. The tally dots in s11 are the idealized
counts the script gives (26 of 40, 8 of 40). The rest is schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PINK = "#F28DB2"
SOMA_FILL = "#262b36"

DIRS = [18, 90, 162, 234, 306]           # neurite 0 points to the upper right; it is the one we treat
CN = np.array([0.0, -0.3, 0.0])         # the big cell's centre
CONE_Y = 0.45
GOLD_SET = [0, 2, 4]                    # the neurites that turn into axons in the whole-cell results


def u(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def perp(d):
    return np.array([-d[1], d[0], 0.0])


def lab(text, pos, size=26, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to(pos)


def ring(p, col=TEXT, r=0.62, w=5):
    return Circle(radius=r, stroke_color=col, stroke_width=w).move_to(p)


def chk(pos, col=GREEN, s=1.0):
    p = np.array(pos, float)
    return VMobject(stroke_color=col, stroke_width=9).set_points_as_corners(
        [p + np.array([-0.28, 0.0, 0]) * s, p + np.array([-0.08, -0.22, 0]) * s, p + np.array([0.32, 0.30, 0]) * s])


def jiggle(line, amp, seed):
    """Make a line wriggle (rotate and drift a little) while the tracker `amp` is above zero."""
    rs = np.random.RandomState(seed)
    st = [0.0, rs.uniform(0, 6.28), rs.uniform(2.0, 4.0)]

    def f(m, dt):
        st[0] += dt
        a = amp.get_value()
        if a > 0:
            m.rotate(a * 1.5 * dt * np.cos(st[2] * st[0] + st[1]))
            m.shift(a * 0.09 * dt * np.array([np.cos(1.7 * st[0] + st[1]), np.sin(1.3 * st[0] + 2 * st[1]), 0.0]))

    line.add_updater(f)


# ---------------------------------------------------------------- the cell
class Neuron:
    """Soma plus neurites whose lengths are ValueTrackers. Each neurite ends in a small growth cone
    (a fan with an orange actin mesh) that follows the tip. `group` is soma + neurites;
    `cone_group` the five growth cones; `mt_dash` / `mt_solid` microtubule drawings (added on demand)."""

    def __init__(self, center=CN, lengths=(2.4,) * 5, colors=None, angles=DIRS, w=9.0, soma_r=0.5, sc=1.0,
                 mesh_n=15, seed=4):
        self.c = np.array(center, float)
        self.sc = sc
        self.n = len(angles)
        self.dirs = [u(a) for a in angles]
        colors = colors or [GREY] * self.n
        self.tr = [ValueTracker(L) for L in lengths]
        self.amp = [ValueTracker(0.0) for _ in range(self.n)]
        self.fade = [ValueTracker(0.0) for _ in range(self.n)]
        self.soma = Circle(radius=soma_r * sc, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL,
                           fill_opacity=1).move_to(self.c)
        self.lines, self.cones, self.meshes, self.mt_solid, self.mt_dash = [], [], [], [], []
        rng = np.random.RandomState(seed)
        a_, b_ = 0.52 * sc, 0.44 * sc        # growth cone semi-axes (along the neurite, across it)
        for i in range(self.n):
            d = self.dirs[i]
            nv = perp(d)
            ln = Line(self.c, self.c + d * lengths[i], color=colors[i], stroke_width=w * sc)
            ln.add_updater(lambda m, i=i, d=d: m.put_start_and_end_on(
                self.c + d * 0.1, self.c + d * max(self.tr[i].get_value(), 0.2)))
            self.lines.append(ln)
            centre = self.c + d * (lengths[i] + 0.3 * sc)
            fan = Ellipse(width=2 * a_, height=2 * b_, stroke_color=colors[i], stroke_width=4 * max(sc, 0.7),
                          fill_color=colors[i], fill_opacity=0.10).rotate(np.radians(angles[i])).move_to(centre)
            mesh = VGroup()
            for k in range(mesh_n):
                while True:
                    x, y = rng.uniform(-1, 1, 2)
                    if x * x + y * y < 0.55:
                        break
                p = centre + d * x * a_ * 0.85 + nv * y * b_ * 0.85
                ang = rng.uniform(0, PI)
                dv = np.array([np.cos(ang), np.sin(ang), 0.0]) * 0.11 * sc
                seg = Line(p - dv, p + dv, color=ORANGE, stroke_width=3.2 * max(sc, 0.75))
                jiggle(seg, self.amp[i], 100 * i + k)
                if k % 3 != 0:
                    seg.add_updater(lambda m, f=self.fade[i]: m.set_opacity(1 - f.get_value()) if f.get_value() > 0 else None)
                mesh.add(seg)
            fan.add_updater(lambda m, i=i: m.set_color(self.lines[i].get_color()))
            cone = VGroup(fan, mesh)

            def fc(m, i=i, d=d):
                tgt = self.c + d * (max(self.tr[i].get_value(), 0.2) + 0.3 * sc)
                m.shift(tgt - m[0].get_center())

            cone.add_updater(fc)
            self.cones.append(cone)
            self.meshes.append(mesh)
            ms = Line(self.c + d * (soma_r * sc + 0.15), self.c + d * lengths[i], color=TEAL, stroke_width=4 * max(sc, 0.8))
            ms.add_updater(lambda m, i=i, d=d, s=soma_r * sc: m.put_start_and_end_on(
                self.c + d * (s + 0.15), self.c + d * max(self.tr[i].get_value() - 0.05, s + 0.3)))
            self.mt_solid.append(ms)
            dsh = DashedLine(self.c + d * (soma_r * sc + 0.15), self.c + d * (lengths[i] - 0.05), color=TEAL,
                             stroke_width=5.5 * max(sc, 0.8), dash_length=0.18 * sc, dashed_ratio=0.6)
            self.mt_dash.append(dsh)
        self.group = VGroup(*self.lines, self.soma)
        self.cone_group = VGroup(*self.cones)
        self.mt_dash_group = VGroup(*self.mt_dash)
        self.mt_solid_group = VGroup(*self.mt_solid)

    def tip(self, i):
        return self.c + self.dirs[i] * self.tr[i].get_value()

    def cp(self, i):
        return self.c + self.dirs[i] * (self.tr[i].get_value() + 0.3 * self.sc)

    def rc(self, i, col):
        return [self.lines[i].animate.set_color(col)]

    def loose_state(self, i):
        """Instantly: a sparse, wriggling mesh."""
        self.fade[i].set_value(1.0)
        self.amp[i].set_value(1.0)

    def loosen_anim(self, i):
        return [self.fade[i].animate.set_value(1.0), self.amp[i].animate.set_value(1.0)]


# ---------------------------------------------------------------- big growth cones (s02 to s04, s26)
def big_cone(cx, cy, col, nm, seg, seed, s=1.0, shaft=2.2, amp=None, with_mesh=True):
    rng = np.random.RandomState(seed)
    a, b = 2.2 * s, 1.7 * s
    def edge(th):
        r = 1 + 0.04 * np.sin(11 * th)
        return np.array([cx + a * np.cos(th) * r, cy + b * np.sin(th) * r, 0.0])

    fan = ParametricFunction(edge, t_range=[0, TAU], stroke_color=col, stroke_width=5, fill_color=col,
                             fill_opacity=0.08)
    spikes = VGroup(*[Line(edge(th), edge(th) + np.array([np.cos(th) * 0.12, np.sin(th) * 0.4 * s, 0]),
                           color=col, stroke_width=4) for th in np.linspace(0.12 * PI, 0.88 * PI, 9)])
    nw = 0.5 * s
    yb = cy - b + 0.04
    sh = VGroup(Line([cx - nw, yb - shaft, 0], [cx - nw * 0.9, yb, 0], color=col, stroke_width=5),
                Line([cx + nw, yb - shaft, 0], [cx + nw * 0.9, yb, 0], color=col, stroke_width=5))
    mesh = VGroup()
    if with_mesh:
        for k in range(nm):
            while True:
                x, y = rng.uniform(-1, 1, 2)
                if x * x + y * y < 0.70:
                    break
            ang = rng.uniform(0, PI)
            c = np.array([cx + x * a * 0.92, cy + y * b * 0.92, 0.0])
            dv = np.array([np.cos(ang), np.sin(ang), 0.0]) * seg / 2 * s
            ln = Line(c - dv, c + dv, color=ORANGE, stroke_width=3.6)
            if amp is not None:
                jiggle(ln, amp, seed * 50 + k)
            mesh.add(ln)
    return dict(fan=fan, shaft=sh, mesh=mesh, outline=VGroup(fan, spikes, sh))


def pipette(tipp, frm):
    tipp, frm = np.array(tipp, float), np.array(frm, float)
    d = (frm - tipp) / np.linalg.norm(frm - tipp)
    nv = perp(d)
    return Polygon(tipp + nv * 0.04, frm + nv * 0.22, frm - nv * 0.22, tipp - nv * 0.04, color=GREY,
                   fill_color=GREY, fill_opacity=0.35, stroke_width=3)


def puff(center, n=6, seed=2, spread=0.42, r=0.09):
    rs = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        g.add(Dot(np.array(center) + np.array([rs.uniform(-spread, spread), rs.uniform(-spread, spread), 0]),
                  radius=r, color=PINK))
    return g


def bath(cx=0.0, cy=-0.25, w=12.2, h=6.7, nd=26, seed=7):
    """A dish full of drug: a pink-tinted dish with drug dots."""
    rs = np.random.RandomState(seed)
    dish = Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=PINK, fill_opacity=0.10)
    dish.move_to([cx, cy, 0])
    dots = VGroup()
    while len(dots) < nd:
        x, y = rs.uniform(-1, 1, 2)
        if x * x + y * y < 0.82:
            dots.add(Dot([cx + x * w / 2, cy + y * h / 2, 0], radius=0.065, color=PINK))
    return VGroup(dish, dots).set_z_index(-1)


DISH_C = np.array([0.0, -0.1, 0.0])


def bath_rect(nd=34, seed=7):
    """A wide rounded dish full of drug, sized so every growth cone (even the long gold ones) sits inside it."""
    rs = np.random.RandomState(seed)
    dish = RoundedRectangle(corner_radius=0.7, width=12.8, height=6.9, stroke_color=GREY, stroke_width=3,
                            fill_color=PINK, fill_opacity=0.10).move_to([0, -0.2, 0])
    dots = VGroup()
    while len(dots) < nd:
        x, y = rs.uniform(-6.0, 6.0), rs.uniform(-3.25, 2.85)
        dots.add(Dot([x, y, 0], radius=0.07, color=PINK))
    return VGroup(dish, dots).set_z_index(-1)


def treated_neuron():
    """Stage 2 cell, drug being puffed at neurite 0 (s07 and s10)."""
    n = Neuron()
    cp0 = n.cp(0)
    tipp = cp0 + np.array([0.62, 0.5, 0.0])
    pip = pipette(tipp, tipp + np.array([2.7, 1.6, 0.0]))
    pf = puff(cp0 + np.array([0.5, 0.3, 0.0]), n=5, seed=3, spread=0.28)
    lbl = VGroup(lab("cytochalasin D,", [4.9, -0.2, 0], 26, PINK), lab("low dose", [4.9, -0.6, 0], 26, PINK))
    return n, pip, pf, lbl


# ---------------------------------------------------------------- the two panels (s08, s09)
PANEL_X = (-3.5, 3.5)
PANEL_Y = 0.15
PSC = 0.82


def panel_cells():
    nl = Neuron(center=[PANEL_X[0], PANEL_Y, 0], lengths=(2.0,) * 5, sc=PSC, seed=11)
    nr = Neuron(center=[PANEL_X[1], PANEL_Y, 0], lengths=(2.0,) * 5, sc=PSC, seed=12)
    return nl, nr


def dish_outline(cx):
    return Ellipse(width=5.7, height=5.5, stroke_color=GREY, stroke_width=3).move_to([cx, PANEL_Y - 0.05, 0])


def panel_question():
    ql = lab("What happens to\nthat neurite?", [PANEL_X[0], -3.05, 0], 26, GOLD)
    qr = lab("What if the whole cell\nis bathed in the drug?", [PANEL_X[1], -3.05, 0], 26, GOLD)
    return ql, qr


# ---------------------------------------------------------------- the race model (s21, s22)
def model_run(S, c=2.0, floor=2.0, T_=48.0, dt=0.002):
    L = np.array([15, 15, 15, 15, 20.0])
    out = [L.copy()]
    step = int(0.1 / dt)
    for k in range(int(T_ / dt)):
        L = np.maximum(L + dt * (S * L * L / np.sum(L * L) - c), floor)
        if (k + 1) % step == 0:
            out.append(L.copy())
    return np.array(out)


MODEL = model_run(60.0)          # supply tripled from 20 to 60 um an hour
MODEL_END = MODEL[-1]


class LogChart:
    """Five bars on a log axis. Heights come from a ValueTracker (hours) or are fixed at `hours`."""

    def __init__(self, x0, dx, base, sy, bw, hours=None, clk=None, axis_x=None, cols=None, labels=True, tick_sz=26):
        self.x0, self.dx, self.base, self.sy, self.bw = x0, dx, base, sy, bw
        self.clk = clk
        self.cols = cols or [GREY] * 5
        self.bars = VGroup()
        for i in range(5):
            m = VMobject(fill_color=self.cols[i], fill_opacity=1, stroke_width=0)
            if clk is not None:
                m.add_updater(lambda mm, i=i: self._set(mm, i, self.val(i)))
            self._set(m, i, MODEL[int(round((hours or 0) / 0.1))][i])
            self.bars.add(m)
        ax = axis_x if axis_x is not None else x0 - dx * 0.6
        self.axis = Line([ax, base, 0], [ax, base + sy * 3.55, 0], color=GREY, stroke_width=3)
        self.floor = Line([ax, base, 0], [x0 + 4 * dx + dx * 0.6, base, 0], color=GREY, stroke_width=3)
        self.ticks = VGroup()
        for v in (1, 10, 100, 1000):
            y = base + sy * np.log10(v)
            self.ticks.add(Line([ax - 0.1, y, 0], [ax + 0.1, y, 0], color=GREY, stroke_width=3),
                           M(str(v), tick_sz, GREY).move_to([ax - 0.62, y, 0]))
        self.group = VGroup(self.axis, self.floor, self.ticks, self.bars)

    def val(self, i):
        k = int(min(max(round(self.clk.get_value() / 0.1), 0), len(MODEL) - 1))
        return MODEL[k][i]

    def _set(self, m, i, L):
        h = self.sy * np.log10(max(L, 1.0))
        x = self.x0 + i * self.dx
        h = max(h, 0.05)
        m.set_points_as_corners([[x - self.bw / 2, self.base, 0], [x + self.bw / 2, self.base, 0],
                                 [x + self.bw / 2, self.base + h, 0], [x - self.bw / 2, self.base + h, 0],
                                 [x - self.bw / 2, self.base, 0]])

    def top(self, i, hours=48.0):
        L = MODEL[int(round(hours / 0.1))][i]
        return np.array([self.x0 + i * self.dx, self.base + self.sy * np.log10(max(L, 1.0)), 0.0])


def cross_x(center, s=0.3, col=RED, w=8):
    c = np.array(center, float)
    return VGroup(Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=col, stroke_width=w),
                  Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=col, stroke_width=w))


# ================================================================ scenes
STAR_SC = 1.3
STAR_L = 2.5
STAR_C = [0.0, -0.3, 0.0]


def star(L=STAR_L, lengths=None, **kw):
    """The big five-neurite star used in s01, s02, s13 and s15 (fills about 80% of the frame height)."""
    return Neuron(center=STAR_C, lengths=lengths or [L] * 5, sc=STAR_SC, **kw)


def mt_label(text, pos, anchor, col=TEAL, size=28):
    t = lab(text, pos, size, col)
    ln = Line(np.array(pos, float) + np.array([0.0, 0.0, 0.0]), anchor, color=col, stroke_width=3)
    return t, ln


class S00Title(TitleCard):
    LESSON = "One Axon, Many Dendrites: Neuronal Polarity"
    TITLE = "Rig the Race"


class S01(SpokenScene):
    def construct(self):
        n = star(lengths=[0.2] * 5)
        self.add(n.group)
        self.at("the race")
        self.play(*[t.animate.set_value(STAR_L) for t in n.tr], run_time=1.0)
        self.at("cytoskeleton")
        self.play(FadeIn(n.cone_group), run_time=0.6)
        self.at("a tip")
        r = ring(n.cp(0), r=0.85)
        self.play(Create(r), run_time=0.5)
        self.at("rig it")
        q = T("?", 100, GOLD, weight=BOLD).move_to(n.cp(0) + np.array([1.25, 0.9, 0]))
        self.play(FadeIn(q, scale=1.4), run_time=0.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        n = star()
        r = ring(n.cp(0), r=0.85)
        q = T("?", 100, GOLD, weight=BOLD).move_to(n.cp(0) + np.array([1.25, 0.9, 0]))
        self.add(n.group, n.cone_group, r, q)
        stage = lab("stage 3: one neurite is longer", [-3.9, 3.3, 0], 28, GREY)
        self.play(FadeOut(r), FadeOut(q), FadeIn(stage), n.tr[0].animate.set_value(3.4), *n.rc(0, YELLOW), run_time=0.7)
        self.at("winner's")
        r2 = ring(n.cp(0), YELLOW, r=0.85)
        self.play(Create(r2), run_time=0.4)
        self.at("looks like")
        self.play(FadeOut(n.group), FadeOut(n.cone_group), FadeOut(r2), FadeOut(stage), run_time=0.3)
        sib, win = two_cones()
        self.play(FadeIn(sib["outline"], scale=0.35), FadeIn(win["outline"], scale=0.35),
                  FadeIn(cone_names()), run_time=0.6)
        self.finish()


def cone_names():
    return VGroup(lab("sibling", [-3.2, 3.0, 0], 30, GREY), lab("future axon", [3.2, 3.0, 0], 30, YELLOW))


def two_cones(amp=None, mesh=False):
    sib = big_cone(-3.2, CONE_Y, GREY, 78, 0.34, 1, shaft=1.6, with_mesh=mesh)
    win = big_cone(3.2, CONE_Y, YELLOW, 15, 0.9, 2, shaft=1.6, amp=amp, with_mesh=mesh)
    return sib, win


class S03(SpokenScene):
    def construct(self):
        amp = ValueTracker(1.0)
        sib, win = two_cones(amp=amp, mesh=True)
        names = cone_names()
        self.add(sib["outline"], win["outline"], names)
        self.play(FadeIn(sib["mesh"]), FadeIn(win["mesh"]), run_time=0.3)
        self.at("1999")
        cite = T("Bradke and Dotti, 1999", 28, TEXT).move_to([0, 3.55, 0])
        self.play(FadeIn(cite, shift=DOWN * 0.15), run_time=0.5)
        self.at("growth cones")
        self.play(Indicate(sib["fan"], color=GREY, scale_factor=1.05), Indicate(win["fan"], color=YELLOW, scale_factor=1.05),
                  run_time=0.8)
        self.at("cultured hippocampal")
        self.play(FadeIn(lab("cultured hippocampal neurons", [0, -3.45, 0], 28, GREY)), run_time=0.5)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        amp = ValueTracker(1.0)
        sib, win = two_cones(amp=amp, mesh=True)
        names = cone_names()
        cite = T("Bradke and Dotti, 1999", 28, TEXT).move_to([0, 3.55, 0])
        cult = lab("cultured hippocampal neurons", [0, -3.45, 0], 28, GREY)
        self.add(sib["outline"], win["outline"], sib["mesh"], win["mesh"], names, cite, cult)
        self.play(FadeOut(cult), run_time=0.3)
        self.at("future")
        self.play(Indicate(names[1], color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.at("looser")
        self.play(FadeIn(lab("looser, moving actin net", [3.2, -3.3, 0], 28, ORANGE)), run_time=0.5)
        self.at("than its siblings")
        self.play(FadeIn(lab("dense actin mat", [-3.2, -3.3, 0], 28, ORANGE)), Indicate(sib["fan"], color=GREY, scale_factor=1.04),
                  run_time=0.7)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        a = chip("loose actin", ORANGE, 44).move_to([0, 2.55, 0])
        w = chip("winning", YELLOW, 44).move_to([0, -2.55, 0])
        down = Arrow([-1.2, 1.7, 0], [-1.2, -1.7, 0], color=TEXT, buff=0, stroke_width=9, max_tip_length_to_length_ratio=0.2)
        up = Arrow([1.2, -1.7, 0], [1.2, 1.7, 0], color=TEXT, buff=0, stroke_width=9, max_tip_length_to_length_ratio=0.2)
        self.at("loose")
        self.play(FadeIn(a, shift=DOWN * 0.2), run_time=0.5)
        self.at("cause")
        self.play(GrowArrow(down), FadeIn(lab("cause", [-3.2, 0, 0], 38)), run_time=0.4)
        self.at("winning")
        self.play(FadeIn(w, shift=UP * 0.2), run_time=0.4)
        self.at("a consequence")
        self.play(GrowArrow(up), FadeIn(lab("consequence", [3.6, 0, 0], 38)), run_time=0.5)
        self.play(FadeIn(T("?", 110, GOLD, weight=BOLD).move_to([0, 0, 0]), scale=1.5), run_time=0.4)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        ys = [1.4, 0.0, -1.4]
        x0, bw, gap = -6.3, 0.88, 0.07

        def block(k, y, col=ORANGE, op=0.55):
            return RoundedRectangle(corner_radius=0.1, width=bw, height=0.62, stroke_color=col, stroke_width=3,
                                    fill_color=col, fill_opacity=op).move_to([x0 + bw / 2 + k * (bw + gap), y, 0])

        fil = [[block(k, y) for k in range(3)] for y in ys]
        head = lab("actin filaments, growing", [-2.6, 2.65, 0], 32, ORANGE)
        self.add(*[b for row in fil for b in row], head)
        self.at("Test it")
        for k in range(3, 9):
            new = [block(k, y) for y in ys]
            self.play(*[FadeIn(b, shift=LEFT * 0.25) for b in new], run_time=0.3)
            self.wait(0.14)
            for row, b in zip(fil, new):
                row.append(b)
        self.at("is a drug")
        drug = chip("cytochalasin D", PINK, 36).move_to([3.7, 2.85, 0])
        self.play(FadeIn(drug, shift=DOWN * 0.2), run_time=0.45)
        self.at("interferes")
        caps = VGroup()
        for row, y in zip(fil, ys):
            tip = row[-1].get_right() + np.array([0.3, 0, 0])
            caps.add(Dot(tip, radius=0.2, color=PINK))
        flying = VGroup(*[Dot(drug.get_bottom(), radius=0.2, color=PINK) for _ in range(3)])
        self.add(flying)
        self.play(FadeIn(lab("interferes with actin assembly", [0, -3.2, 0], 34, PINK)),
                  *[f.animate.move_to(c.get_center()) for f, c in zip(flying, caps)], run_time=0.9)
        mono = block(0, ys[1], ORANGE, 1.0).move_to(caps[1].get_center() + np.array([3.4, 0.0, 0]))
        self.add(mono)
        self.play(mono.animate.move_to(caps[1].get_center() + np.array([0.72, 0.0, 0])), run_time=0.7)
        nope = lab("cannot join", [4.3, 0.75, 0], 28, RED)
        self.play(mono.animate.shift(RIGHT * 1.2), FadeIn(nope), run_time=0.5)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        n, pip, pf, lbl = treated_neuron()
        self.play(FadeIn(n.group), FadeIn(n.cone_group), run_time=0.4)
        self.at("stage two")
        self.play(FadeIn(lab("stage 2", [-5.6, 3.25, 0], 32, GREY)), run_time=0.4)
        self.at("before any")
        self.play(*[Indicate(l, color=TEXT, scale_factor=1.0) for l in n.lines], run_time=0.7)
        self.at("apply")
        pip.shift(RIGHT * 1.6 + UP * 0.9)
        self.add(pip)
        self.play(pip.animate.shift(LEFT * 1.6 + DOWN * 0.9), run_time=0.3)
        self.at("low dose")
        self.play(FadeIn(pf, shift=LEFT * 0.2), FadeIn(lbl), run_time=0.5)
        self.at("one growth cone")
        self.play(*n.loosen_anim(0), run_time=1.0)
        self.finish()


def panel_titles(top=3.05):
    return VGroup(lab("local puff", [PANEL_X[0], top, 0], 28, PINK),
                  lab("whole-dish wash", [PANEL_X[1], top, 0], 28, PINK))


class S08(SpokenScene):
    def construct(self):
        nl, nr = panel_cells()
        dl, dr = dish_outline(PANEL_X[0]), dish_outline(PANEL_X[1])
        cp0 = nl.cp(0)
        tipp = cp0 + np.array([0.55, 0.42, 0.0])
        pip = pipette(tipp, tipp + np.array([0.9, 0.95, 0.0]))
        pf = puff(cp0 + np.array([0.45, 0.28, 0.0]), n=5, seed=3, spread=0.25)
        nl.loose_state(0)
        ql, qr = panel_question()
        tt = panel_titles()
        self.play(FadeIn(dl), FadeIn(nl.group), FadeIn(nl.cone_group), FadeIn(pip), FadeIn(pf), FadeIn(ql),
                  FadeIn(tt[0]), run_time=0.6)
        self.at("And what if")
        self.play(FadeIn(dr), FadeIn(nr.group), FadeIn(nr.cone_group), FadeIn(tt[1]), run_time=0.6)
        self.at("in the drug")
        b = bath(PANEL_X[1], PANEL_Y - 0.05, 5.7, 5.5, nd=18, seed=5)
        loosen = []
        for i in range(5):
            loosen += nr.loosen_anim(i)
        self.play(FadeIn(b), FadeIn(qr), *loosen, run_time=0.9)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        nl, nr = panel_cells()
        nl.loose_state(0)
        for i in range(5):
            nr.loose_state(i)
        cp0 = nl.cp(0)
        tipp = cp0 + np.array([0.55, 0.42, 0.0])
        pip = pipette(tipp, tipp + np.array([0.9, 0.95, 0.0]))
        pf = puff(cp0 + np.array([0.45, 0.28, 0.0]), n=5, seed=3, spread=0.25)
        ql, qr = panel_question()
        tt = panel_titles()
        b = bath(PANEL_X[1], PANEL_Y - 0.05, 5.7, 5.5, nd=18, seed=5)
        self.add(dish_outline(PANEL_X[0]), nl.group, nl.cone_group, pip, pf, tt[0],
                 b, nr.group, nr.cone_group, tt[1], ql, qr)
        pp = lab("pause and predict", [0, 3.55, 0], 30, GOLD)
        self.play(FadeIn(pp, scale=1.2), run_time=0.5)
        self.wait(max(self.narration_s - 0.5, 0.1))
        self.finish()


class S10(SpokenScene):
    def construct(self):
        n, pip, pf, lbl = treated_neuron()
        n.loose_state(0)
        self.add(n.group, n.cone_group, pip, pf, lbl)
        self.at("treated")
        r = ring(n.cp(0), PINK)
        self.play(Create(r), run_time=0.4)
        self.at("likely", lead=0.4)
        self.play(FadeOut(pip), FadeOut(pf), FadeOut(lbl), FadeOut(r), n.tr[0].animate.set_value(3.6), *n.rc(0, YELLOW),
                  run_time=1.0)
        self.at("become the axon")
        self.play(FadeIn(lab("more often than chance, not every time", [0, -3.35, 0], 30, TEXT)), run_time=0.5)
        self.finish()


def grid(cx, cy, cols=5, rows=8, sp=0.62, r=0.25):
    g = VGroup()
    for k in range(cols * rows):
        row, col = divmod(k, cols)
        g.add(Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(
            [cx + (col - (cols - 1) / 2) * sp, cy + ((rows - 1) / 2 - row) * sp, 0]))
    return g


class S11(SpokenScene):
    def construct(self):
        gl, gr = grid(-3.5, -0.2), grid(3.5, -0.2)
        head = lab("idealized data: one dot per neuron", [0, 3.62, 0], 26, GREY)
        key_dot = Dot([-3.3, 3.18, 0], radius=0.13, color=YELLOW)
        key = lab("gold dot = that neurite became the axon", [0.2, 3.18, 0], 26, TEXT)
        key_dot.next_to(key, LEFT, buff=0.18)
        tl = lab("untreated: random neurite watched", [-3.5, 2.68, 0], 26, TEXT)
        tr = lab("drug on one growth cone", [3.5, 2.68, 0], 26, PINK)
        self.play(FadeIn(head), FadeIn(key), FadeIn(key_dot), FadeIn(gl), FadeIn(gr), FadeIn(tl), FadeIn(tr), run_time=0.7)
        self.at("By chance")
        self.play(LaggedStart(*[g.animate.set_fill(YELLOW, 1).set_stroke(YELLOW) for g in gl[:8]], lag_ratio=0.2),
                  run_time=1.4)
        self.at("in five")
        n1 = M("8 of 40", 44, YELLOW).move_to([-3.5, -3.1, 0])
        c1 = lab("expected by chance: one in five", [-3.5, -3.62, 0], 26, TEXT)
        self.play(FadeIn(n1), FadeIn(c1), run_time=0.4)
        self.at("drugged one")
        self.play(LaggedStart(*[g.animate.set_fill(YELLOW, 1).set_stroke(YELLOW) for g in gr[:26]], lag_ratio=0.1),
                  run_time=1.3)
        self.at("more often")
        self.play(FadeIn(M("26 of 40", 44, YELLOW).move_to([3.5, -3.1, 0])),
                  FadeIn(lab("that neurite became the axon", [3.5, -3.62, 0], 26, TEXT)), run_time=0.4)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        n = Neuron(center=DISH_C, lengths=[2.4] * 5)
        self.add(n.group, n.cone_group)
        self.at("bathed")
        b = bath_rect()
        loosen = []
        for i in range(5):
            loosen += n.loosen_anim(i)
        self.play(FadeIn(b), FadeIn(lab("cytochalasin D,\nwhole dish", [-4.9, 2.7, 0], 26, PINK)), *loosen, run_time=1.2)
        self.bring_to_front(n.group, n.cone_group)
        self.at("several axons", lead=0.15)
        anims = []
        for i in GOLD_SET:
            anims += n.rc(i, YELLOW) + [n.tr[i].animate.set_value(3.0)]
        self.play(*anims, run_time=0.25)
        self.wait(2.6)  # Let the several-axon result remain fully gold for inspection.
        self.finish()


class S13(SpokenScene):
    def construct(self):
        n = star()
        self.add(n.group, n.mt_dash_group, n.cone_group)
        self.at("2008")
        yr = lab("2008", [-5.4, 2.7, 0], 36, GREY)
        self.play(FadeIn(yr, shift=DOWN * 0.15), run_time=0.5)
        self.at("Harold", lead=0.15)
        nm1 = lab("Witte", [-5.4, 2.05, 0], 30, TEXT)
        self.play(FadeIn(nm1), run_time=0.4)
        self.at("Dorothy", lead=0.15)
        nm2 = lab("Neukirchen", [-5.4, 1.45, 0], 30, TEXT)
        self.play(FadeIn(nm2), run_time=0.4)
        self.at("and Frank", lead=0.1)
        nm3 = lab("Bradke", [-5.4, 0.85, 0], 30, TEXT)
        self.play(FadeIn(nm3), run_time=0.4)
        self.at("did the same")
        self.play(Indicate(n.cone_group, color=ORANGE, scale_factor=1.0), run_time=0.8)
        self.at("microtubules")
        t, ln = mt_label("microtubules", [-4.4, -3.3, 0], n.c + n.dirs[3] * 1.9)
        self.play(FadeIn(t), Create(ln), run_time=0.8)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        ys = [2.1, 0.7, -0.7, -2.1]
        base = [8.2, 9.2, 7.6, 9.6]
        bars = VGroup()
        for k, (y, bl) in enumerate(zip(ys, base)):
            ph = k * 1.3

            clock = [0.0]

            def f(m, dt=0, y=y, bl=bl, ph=ph, clock=clock):
                clock[0] += dt
                length = bl + 1.3 * np.sin(3.2 * clock[0] + ph)
                m.put_start_and_end_on([-6.3, y, 0], [-6.3 + length, y, 0])

            ln = Line([-6.3, y, 0], [-1.0, y, 0], color=TEAL, stroke_width=12)
            ln.add_updater(f)
            f(ln)
            bars.add(ln)
        name = lab("microtubules", [-4.6, 3.0, 0], 30, TEAL)
        state = lab("dynamic: growing and shrinking", [0, -3.3, 0], 30, TEXT)
        self.add(bars, name, state)
        self.at("Taxol")
        tax = chip("taxol", PINK, 38).move_to([4.3, 3.0, 0])
        self.play(FadeIn(tax, shift=DOWN * 0.2), run_time=0.5)
        self.at("stabilizes", lead=0)
        for line in bars:
            line.clear_updaters()
            line.set_stroke(width=20)
        state.become(lab("stabilized: steady", [0, -3.3, 0], 30, TEXT))
        self.finish()


def flash_at(scene, p):
    glow = Circle(radius=0.55, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to(p)
    scene.play(FadeIn(glow, scale=0.3), Flash(p, color=TEXT, line_length=0.8, num_lines=16, flash_radius=1.4, run_time=0.6),
               run_time=0.4)
    return glow


def steady(n, i, w=9.0):
    n.mt_solid[i].set_stroke(width=w)
    return [FadeOut(n.mt_dash[i]), FadeIn(n.mt_solid[i])]


class S15(SpokenScene):
    def construct(self):
        n = star()
        self.add(n.group, n.mt_dash_group, n.cone_group)
        # Untreated bundles stay faint; the released drug produces one bright, solid bundle.
        for bundle in n.mt_dash:
            bundle.set_opacity(0.38)
        self.at("flash", lead=0.1)
        tl = lab("taxol analogue", [4.9, 1.55, 0], 28, PINK)
        ld = Line([3.85, 1.4, 0], n.cp(0) + np.array([0.0, 0.3, 0.0]), color=PINK, stroke_width=3)
        self.add(tl, ld)
        glow = flash_at(self, n.cp(0))
        self.at("released")
        drops = puff(n.cp(0), n=6, seed=5, spread=0.25)
        self.play(FadeIn(drops), run_time=0.3)
        self.at("taxol analog", lead=0)
        self.play(drops.animate.shift(-n.dirs[0] * 0.8), run_time=0.5)
        self.at("in one", lead=0.1)
        n.mt_solid[0].set_color("#71F4F3")
        self.play(*steady(n, 0, w=15), FadeOut(glow, scale=2.5), run_time=0.6)
        self.add(n.mt_solid[0])
        self.at("That", lead=0.5)
        self.play(FadeOut(drops), FadeOut(tl), FadeOut(ld),
                  n.lines[0].animate.set_color(YELLOW).set_stroke(width=23), run_time=0.5)
        self.play(n.tr[0].animate.set_value(3.4), run_time=1.2)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        n = Neuron(center=DISH_C, lengths=[2.4] * 5)
        self.add(n.group, n.mt_dash_group, n.cone_group)
        self.at("Low dose")
        b = bath_rect()
        self.play(FadeIn(b), FadeIn(lab("taxol, low dose,\nwhole neuron", [-4.9, 2.7, 0], 26, PINK)), run_time=0.6)
        self.bring_to_front(n.group, n.mt_dash_group, n.cone_group)
        self.at("whole neuron")
        self.play(Indicate(n.soma, color=PINK, scale_factor=1.3), run_time=0.6)
        self.at("led several")
        self.play(*sum([steady(n, i, 8.0) for i in GOLD_SET], []), run_time=0.6)
        self.bring_to_front(*[n.mt_solid[i] for i in GOLD_SET])
        self.at("grow as axons", lead=0.1)
        anims = []
        for i in GOLD_SET:
            anims += [n.lines[i].animate.set_color(YELLOW).set_stroke(width=16),
                      n.tr[i].animate.set_value(3.0)]
        self.play(*anims, run_time=0.25)
        self.wait(2.6)
        self.finish()


def loop_nodes():
    pk = chip("PI3-kinase makes PIP3", GREEN, 32).move_to([0, 2.8, 0])
    ac = chip("actin loosens", ORANGE, 32).move_to([4.5, 0.1, 0])
    mt = chip("microtubules advance", TEAL, 32).move_to([0, -2.6, 0])
    fs = chip("tip grows faster", TEXT, 32).move_to([-4.5, 0.1, 0])
    return pk, ac, mt, fs


def loop_arrows():
    spec = [([2.2, 2.45, 0], [4.3, 0.75, 0], -0.55), ([4.3, -0.55, 0], [2.4, -2.3, 0], -0.55),
            ([-2.4, -2.3, 0], [-4.3, -0.55, 0], -0.55), ([-4.3, 0.75, 0], [-2.2, 2.45, 0], -0.55)]
    g = VGroup()
    for a, b, ang in spec:
        g.add(CurvedArrow(np.array(a, float), np.array(b, float), angle=ang, color=GREEN, stroke_width=8))
    return g


class S17(SpokenScene):
    def construct(self):
        pk, ac, mt, fs = loop_nodes()
        arrows = loop_arrows()
        self.play(FadeIn(pk), FadeIn(ac), FadeIn(mt), FadeIn(fs), run_time=0.5)
        self.at("positive loop")
        lp = lab("positive loop", [0, 0.1, 0], 46, GREEN)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), FadeIn(lp), run_time=1.2)
        self.at("PI3", lead=0)
        # Put the block beside the kinase chip, leaving every word unobscured.
        x = cross_x(pk.get_left() + LEFT * 0.55, 0.4, RED, 11).set_z_index(5)
        self.play(Create(x), pk[1].animate.set_color(WHITE), run_time=0.2)
        self.at("blocked throughout")
        self.play(FadeIn(lab("blocked in every neurite", [0, -3.5, 0], 30, RED)), run_time=0.5)
        self.finish()


def stop_bar(n, i, col=RED, k=1.0):
    p = n.cp(i) + n.dirs[i] * 0.62 * k
    v = perp(n.dirs[i]) * 0.38 * k
    return Line(p - v, p + v, color=col, stroke_width=11)


class S18(SpokenScene):
    def construct(self):
        n = Neuron(center=[0, -0.1, 0], lengths=[1.55] * 5, sc=1.2)
        self.add(n.group, n.cone_group)
        self.at("reported")
        rep = lab("reported:", [-2.0, 3.4, 0], 26, GREY)
        self.play(FadeIn(rep), run_time=0.3)
        self.at("leave no", lead=0.3)
        bars = [stop_bar(n, i, k=1.2) for i in range(5)]
        t0 = lab("no axon forms", [0.35, 3.4, 0], 34, RED)
        t0.next_to(rep, RIGHT, buff=0.25)
        self.play(FadeIn(t0), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.15), run_time=1.3)
        self.at("does not free")
        others = chip("others take over", GREY, 30).move_to([0, -2.9, 0])
        arr = Arrow([0, -2.5, 0], [0, -1.3, 0], color=GREY, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(others), GrowArrow(arr), run_time=0.5)
        self.play(Create(cross_x([0, -1.95, 0], 0.4, RED, 10)), run_time=0.5)
        self.at("It stops")
        self.play(*[Indicate(b, color=RED, scale_factor=1.4) for b in bars], run_time=0.8)
        self.finish()


def card(cx, title, outcome, col):
    box = RoundedRectangle(corner_radius=0.25, width=6.1, height=6.1, stroke_color=col, stroke_width=4,
                           fill_color=col, fill_opacity=0.06).move_to([cx, -0.1, 0])
    t = lab(title, [cx, 2.55, 0], 34, col)
    o = lab(outcome, [cx, -2.65, 0], 36, TEXT)
    return box, t, o


class S19(SpokenScene):
    def construct(self):
        bl, tl, ol = card(-3.4, "local boost", "one winner", YELLOW)
        br, tr, orr = card(3.4, "loop blocked", "no winner", RED)
        nl = Neuron(center=[-3.4, -0.3, 0], lengths=[2.0, 1.4, 1.4, 1.4, 1.4], sc=0.95, mesh_n=10, seed=21,
                    colors=[YELLOW, GREY, GREY, GREY, GREY])
        nr = Neuron(center=[3.4, -0.3, 0], lengths=[1.4] * 5, sc=0.95, mesh_n=10, seed=22)
        bars = [stop_bar(nr, i, k=0.8) for i in range(5)]
        self.play(FadeIn(bl), FadeIn(br), FadeIn(tl), FadeIn(tr), FadeIn(nl.group), FadeIn(nl.cone_group),
                  FadeIn(nr.group), FadeIn(nr.cone_group), run_time=0.5)
        self.at("local boost")
        self.play(Indicate(bl, color=YELLOW, scale_factor=1.02), run_time=0.6)
        self.at("rigs it")
        self.play(FadeIn(ol), FadeIn(chk([-3.4 + 2.5, 2.55, 0])), run_time=0.5)
        self.at("Blocking the loop")
        self.play(*[Create(b) for b in bars], run_time=0.6)
        self.at("leaves no winner")
        self.play(FadeIn(orr), FadeIn(chk([3.4 + 2.5, 2.55, 0])), run_time=0.5)
        self.finish()


def several_axons(center=CN, lengths=None, sc=1.0):
    ls = lengths or [3.0 if i in GOLD_SET else 2.3 for i in range(5)]
    cols = [YELLOW if i in GOLD_SET else GREY for i in range(5)]
    n = Neuron(center=center, lengths=ls, colors=cols, sc=sc, seed=31)
    for i in range(5):
        n.loose_state(i)
    return n


class S20(SpokenScene):
    def construct(self):
        n = several_axons(center=DISH_C)
        self.add(n.group, n.cone_group)
        self.at("several axon")
        self.play(FadeIn(lab("several axons", [-4.9, 2.9, 0], 30, YELLOW)), run_time=0.5)
        self.at("second look")
        self.play(FadeIn(T("?", 130, GOLD, weight=BOLD).move_to([5.5, 1.6, 0]), scale=1.5), run_time=0.5)
        self.finish()


def spec_lines():
    return VGroup(lab("illustrative model, not a drug", [0, 3.45, 0], 26, GREY))


class S21(SpokenScene):
    def construct(self):
        clk = ValueTracker(0.0)
        ch = LogChart(-3.8, 1.9, -3.2, 1.6, 1.1, clk=clk, axis_x=-5.0)
        ylab = lab("length, micrometres (log scale)", [-6.5, -0.5, 0], 26, GREY).rotate(PI / 2)
        hours = VMobject()
        hours.add_updater(lambda m: m.become(M("hour {:.0f}".format(clk.get_value()), 30, TEXT).move_to([5.5, 3.1, 0])))
        self.add(hours)
        self.play(FadeIn(ch.group), FadeIn(ylab), FadeIn(spec_lines()), run_time=0.8)
        self.at("tripled")
        sup = lab("supply tripled: 60 micrometres an hour", [0, 2.9, 0], 28, TEXT)
        self.play(FadeIn(sup), run_time=0.5)
        self.at("one still wins")
        self.play(clk.animate.set_value(48.0), run_time=2.0, rate_func=linear)
        self.play(ch.bars[4].animate.set_fill(YELLOW), run_time=0.3)
        self.finish()


def small_chart():
    return LogChart(-4.6, 1.1, -3.0, 1.45, 0.74, hours=48.0, axis_x=-5.3,
                    cols=[GREY, GREY, GREY, GREY, YELLOW])


class S22(SpokenScene):
    def construct(self):
        big = LogChart(-3.8, 1.9, -3.2, 1.6, 1.1, hours=48.0, axis_x=-5.0,
                       cols=[GREY, GREY, GREY, GREY, YELLOW])
        bigy = lab("length, micrometres (log scale)", [-6.5, -0.5, 0], 26, GREY).rotate(PI / 2)
        allbig = VGroup(big.group, bigy)
        small = small_chart()
        smally = lab("length, micrometres (log scale)", [-3.3, 3.35, 0], 26, GREY)
        allsmall = VGroup(small.group, smally)
        self.add(allbig)
        self.at("plain speedup")
        mlab = lab("illustrative model: one winner", [-3.0, -3.55, 0], 26, GREY)
        self.play(Transform(allbig, allsmall), FadeIn(mlab), run_time=0.8)
        self.at("does not match", lead=0.3)
        eq = VGroup(Line([-0.35, 0.25, 0], [0.55, 0.25, 0], color=RED, stroke_width=10),
                    Line([-0.35, -0.25, 0], [0.55, -0.25, 0], color=RED, stroke_width=10),
                    Line([-0.2, -0.75, 0], [0.4, 0.75, 0], color=RED, stroke_width=10)).move_to([1.2, 0.0, 0])
        n = several_axons(center=[4.3, -0.4, 0], lengths=[1.8 if i in GOLD_SET else 1.35 for i in range(5)], sc=0.85)
        self.play(Create(eq), FadeIn(n.group), FadeIn(n.cone_group),
                  FadeIn(lab("drug result: several axons", [4.0, 2.7, 0], 26, YELLOW)), run_time=0.7)
        self.finish()


BAR_X = [-4.0, -2.25, -0.5, 1.25, 3.0]
BAR_BASE = -2.65
LINE_H = 3.3
AXIS_X = -5.0
LINE_X0, LINE_X1 = -5.0, 3.9
H0 = [1.3, 1.8, 1.5, 2.0, 1.4]
H1 = [4.4, 5.1, 4.7, 5.4, 4.9]


def bar_chart(hs):
    bars = VGroup()
    for i in range(5):
        m = VMobject(fill_color=GREY, fill_opacity=1, stroke_width=0)

        def f(mm, i=i):
            h = hs[i].get_value()
            x = BAR_X[i]
            mm.set_points_as_corners([[x - 0.45, BAR_BASE, 0], [x + 0.45, BAR_BASE, 0], [x + 0.45, BAR_BASE + h, 0],
                                      [x - 0.45, BAR_BASE + h, 0], [x - 0.45, BAR_BASE, 0]])
            mm.set_fill(YELLOW if h >= LINE_H else GREY, 1)

        m.add_updater(f)
        f(m)
        bars.add(m)
    base = Line([AXIS_X, BAR_BASE, 0], [3.9, BAR_BASE, 0], color=GREY, stroke_width=3)
    axis = Arrow([AXIS_X, BAR_BASE, 0], [AXIS_X, BAR_BASE + 5.7, 0], color=GREY, buff=0, stroke_width=4,
                 max_tip_length_to_length_ratio=0.05)
    ticks = VGroup(lab("low", [AXIS_X - 0.55, BAR_BASE + 0.1, 0], 26, GREY),
                   lab("high", [AXIS_X - 0.6, BAR_BASE + 5.4, 0], 26, GREY))
    names = VGroup(*[lab(f"neurite {i + 1}", [BAR_X[i], -3.45, 0], 26, GREY) for i in range(5)])
    return VGroup(base, axis, ticks, bars, names)


def thresh_line(color=GOLD):
    return DashedLine([LINE_X0, BAR_BASE + LINE_H, 0], [LINE_X1, BAR_BASE + LINE_H, 0], color=color, stroke_width=5,
                      dash_length=0.2)


def level_title():
    return lab("level of loose actin or stable microtubules (schematic)", [0.0, 3.55, 0], 26, GREY)


class S23(SpokenScene):
    def construct(self):
        hs = [ValueTracker(h) for h in H0]
        ch = bar_chart(hs)
        self.play(FadeIn(ch), FadeIn(level_title()), run_time=0.8)
        self.at("threshold")
        tl = thresh_line()
        tlab = lab("threshold", [5.35, BAR_BASE + LINE_H, 0], 28, GOLD)
        self.play(Create(tl), FadeIn(tlab), run_time=0.8)
        self.at("model does not")
        self.play(FadeIn(lab("one possible reading, not tested by the model", [0.0, 3.05, 0], 26, GOLD)), run_time=0.6)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        hs = [ValueTracker(h) for h in H0]
        ch = bar_chart(hs)
        tl = thresh_line()
        tlab = lab("threshold", [5.35, BAR_BASE + LINE_H, 0], 28, GOLD)
        note = lab("one possible reading, not tested by the model", [0.0, 3.05, 0], 26, GOLD)
        self.add(ch, level_title(), tl, tlab, note)
        self.at("the drug pushes")
        dlab = lab("drug", [4.7, -3.0, 0], 30, PINK)
        arrows = VGroup(*[Arrow([x, -3.18, 0], [x, -2.72, 0], color=PINK, buff=0, stroke_width=8,
                                max_tip_length_to_length_ratio=0.45) for x in BAR_X])
        self.play(FadeIn(arrows), FadeIn(dlab), FadeOut(note), run_time=0.5)
        self.play(*[h.animate.set_value(v) for h, v in zip(hs, H1)], run_time=3.2, rate_func=smooth)
        self.at("marks an axon")
        self.play(Transform(tlab, lab("marks an axon", [5.15, BAR_BASE + LINE_H, 0], 25, GOLD)), run_time=0.5)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        hs = [ValueTracker(h) for h in H1]
        ch = bar_chart(hs)
        tl = thresh_line()
        tlab = lab("marks an axon", [5.15, BAR_BASE + LINE_H, 0], 25, GOLD)
        win = lab("without winning the race", [0.0, 3.55, 0], 34, GOLD)
        self.add(ch, tl, tlab, win)
        self.play(*[h.animate.set_value(v) for h, v in zip(hs, H0)], run_time=0.35)
        self.at("crosses")
        self.play(*[h.animate.set_value(v) for h, v in zip(hs, H1)], run_time=1.4, rate_func=smooth)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        hs = [ValueTracker(h) for h in H1]
        prev = VGroup(bar_chart(hs), thresh_line(),
                      lab("marks an axon", [5.15, BAR_BASE + LINE_H, 0], 25, GOLD),
                      lab("without winning the race", [0.0, 3.55, 0], 34, GOLD))
        self.add(prev)
        cone = big_cone(0.0, 0.5, GREY, 26, 0.55, 8, s=1.15, shaft=1.3)
        yb = 0.5 - 1.7 * 1.15 + 0.04 - 1.3
        mts = VGroup(*[Line([x, yb, 0], [x, 0.5, 0], color=TEAL, stroke_width=7) for x in (-0.3, 0.0, 0.3)])
        a = chip("loose actin", ORANGE, 32).move_to([-4.7, 2.5, 0])
        m = chip("stable microtubules", TEAL, 32).move_to([4.6, 2.5, 0])
        ar1 = Arrow(a.get_bottom(), [-2.2, 1.1, 0], color=ORANGE, buff=0.1, stroke_width=7)
        ar2 = Arrow(m.get_bottom(), [2.2, 1.1, 0], color=TEAL, buff=0.1, stroke_width=7)
        prev.clear_updaters()
        self.play(FadeOut(prev), run_time=0.2)
        self.play(FadeIn(cone["outline"]), FadeIn(cone["mesh"]), FadeIn(mts), FadeIn(a), FadeIn(m),
                  run_time=0.3)
        self.at("Either way")
        self.at("the race reads")
        self.play(GrowArrow(ar1), GrowArrow(ar2), run_time=0.8)
        self.at("at the tip")
        self.play(Indicate(cone["outline"], color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("Next")
        self.play(FadeIn(lab("Next: Tracks That Point Two Ways", [0, -3.5, 0], 32, GOLD)), run_time=0.5)
        self.at("become tracks")
        self.play(Indicate(mts, color=TEAL, scale_factor=1.15), run_time=0.9)
        self.finish()


class S27End(EndCard):
    LINE = "Either way, the race reads the cytoskeleton at the tip."
