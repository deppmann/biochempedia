"""Two Enemies, One Gall (film 2 of 2, Ecology and Evolution), authored 2026-11-11.

Same world and colour map as film 1 (../scenes.py): dark navy ground, CREAM / CHAR moths, BLUE birds, YELLOW
for the highlight (here the fitness curve), GREEN for plant / environment, GREY for guides, TEAL unused.
New in this film: ORANGE = wasps (the second enemy), GALLC = the gall, LARVA = the larva inside.

THE WORLD (kept through the film): a row of 12 galls sorted by size along y = -1.3, a "relative fitness" axis
rising above the row (baseline y = -0.62, dashed average line at 1), a histogram of gall sizes along the bottom.
Brightness of each gall, the curve, the dots and the bars all come from ONE toy model (World), so what is
drawn is computed:  attack by wasps falls with size, attack by birds rises with size, survival = (1-a_w)(1-a_b),
relative fitness = survival / mean survival.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

# ---------------------------------------------------------------- colours (film 1 map + new ones)
CREAM = "#F1E6C8"
CHAR = "#2B2B2E"
ORANGE = "#F28C28"
GALLC = "#C9974A"
GALLE = "#E8C07A"
DARKG = "#45404F"
LARVA = "#F4EDD2"
CAVITY = "#6E4F1E"

# ---------------------------------------------------------------- the model and the layout
N = 12
S = np.linspace(0, 1, N)
XS = -4.95 + 0.9 * np.arange(N)
RR = 0.12 + 0.32 * np.arange(N) / (N - 1)
GY = -1.3          # y of the row of galls
BASE = -0.62       # baseline of the fitness plot
FS = 2.1           # fitness-axis scale (units per 1.0 of relative fitness)
AXX = -5.75        # x of the fitness axis
HB = -3.75         # bottom of the histogram
HU = 6.5           # histogram height per unit probability
XLAB = -2.05       # y of the "gall size" axis label row
P0 = np.exp(-0.5 * ((S - 0.5) / 0.27) ** 2)
P0 = P0 / P0.sum()


def fy(f):
    return BASE + FS * f


def sx(s):
    return -4.95 + 9.9 * s


def attacks(aw, ab, s, k=9.0):
    return aw / (1 + np.exp(k * (s - 0.5))), ab / (1 + np.exp(-k * (s - 0.5)))


def _dip_raw(s):
    return 0.5 + 3.2 * (s - 0.5) ** 2


def _ramp_raw(s):
    return 0.35 + 1.3 * s


DIPK = float(P0 @ _dip_raw(S))
RAMPK = float(P0 @ _ramp_raw(S))


def f_dip(s):
    return _dip_raw(s) / DIPK


def f_ramp(s):
    return _ramp_raw(s) / RAMPK


def f_model(s, aw, ab, wa=1.0, ba=1.0):
    a_w, a_b = attacks(aw, ab, S)
    norm = float(P0 @ ((1 - wa * a_w) * (1 - ba * a_b)))
    a_w, a_b = attacks(aw, ab, s)
    return (1 - wa * a_w) * (1 - ba * a_b) / norm


def hist_after(aw, ab):
    h = P0 * f_model(S, aw, ab)
    return h / h.sum()


def hist_dip():
    h = P0.copy()
    for _ in range(2):
        h = h * f_dip(S)
        h = h / h.sum()
    return h


H_BEFORE = P0
H_SYM = hist_after(0.9, 0.9)
H_HEAVY = hist_after(0.95, 0.7)
H_DIP = hist_dip()


def f_shape(kind, s):
    return {"ramp": f_ramp, "hump": lambda x: f_model(x, 0.9, 0.9), "dip": f_dip}[kind](s)


# ---------------------------------------------------------------- icons
def moth(color, s=1.0):
    edge = TEXT if color == CHAR else "#B8AC88"
    kw = dict(fill_color=color, fill_opacity=0.97, stroke_color=edge, stroke_width=1.6)
    w1 = Ellipse(width=0.62, height=0.34, **kw).shift(LEFT * 0.3 + UP * 0.05).rotate(0.25)
    w2 = Ellipse(width=0.62, height=0.34, **kw).shift(RIGHT * 0.3 + UP * 0.05).rotate(-0.25)
    b = Ellipse(width=0.16, height=0.5, **kw).shift(DOWN * 0.03)
    return VGroup(w1, w2, b).scale(s)


def bird(s=1.0, face=1):
    body = Ellipse(width=0.65, height=0.42, color=BLUE, fill_opacity=1)
    head = Circle(radius=0.17, color=BLUE, fill_opacity=1).shift(RIGHT * 0.32 + UP * 0.19)
    beak = Polygon([0.45, 0.23, 0], [0.72, 0.13, 0], [0.45, 0.06, 0], color=BLUE, fill_opacity=1)
    tail = VGroup(*[Line([-0.23 + d, -0.1, 0], [-0.48 + d, -0.7, 0], color=BLUE, stroke_width=7) for d in (-0.08, 0.08)])
    g = VGroup(body, head, beak, tail).scale(1.5 * s)
    if face < 0:
        g.flip(UP)
    return g


def wasp(s=1.0, face=1):
    body = Ellipse(width=0.62, height=0.3, color=ORANGE, fill_opacity=1)
    head = Circle(radius=0.13, color="#3A2A1A", fill_opacity=1).shift(RIGHT * 0.38)
    st = VGroup(Line([-0.08, 0.15, 0], [-0.08, -0.15, 0]), Line([0.12, 0.14, 0], [0.12, -0.14, 0])).set_stroke("#3A2A1A", 6)
    sting = Polygon([-0.3, 0.05, 0], [-0.52, 0, 0], [-0.3, -0.05, 0], color="#3A2A1A", fill_opacity=1)
    w1 = Ellipse(width=0.5, height=0.22, color=TEXT, fill_opacity=0.5, stroke_width=1).shift(UP * 0.22 + LEFT * 0.08).rotate(0.5)
    w2 = Ellipse(width=0.5, height=0.22, color=TEXT, fill_opacity=0.5, stroke_width=1).shift(UP * 0.22 + RIGHT * 0.12).rotate(-0.3)
    g = VGroup(w1, w2, sting, body, st, head).scale(1.5 * s)
    if face < 0:
        g.flip(UP)
    return g


def gallfly(s=1.0):
    body = Ellipse(width=0.5, height=0.2, color="#8A8494", fill_opacity=1)
    head = Circle(radius=0.1, color="#6A6474", fill_opacity=1).shift(LEFT * 0.3)
    w1 = Ellipse(width=0.45, height=0.2, color=TEXT, fill_opacity=0.45, stroke_width=1).shift(UP * 0.18 + RIGHT * 0.02).rotate(0.4)
    return VGroup(w1, body, head).scale(1.5 * s)


def larva(s=1.0):
    body = RoundedRectangle(corner_radius=0.11, width=0.55, height=0.22, fill_color=LARVA, fill_opacity=1, stroke_color="#CDBF8F", stroke_width=2)
    segs = VGroup(*[Line([x, 0.09, 0], [x, -0.09, 0]) for x in (-0.12, 0.0, 0.12)]).set_stroke("#CDBF8F", 2)
    return VGroup(body, segs).scale(s)


def hov(m, amp=0.1, seed=0):
    """Hover: the icon drifts around m.base. Change m.base (not the position) to move it."""
    m.base = m.get_center().copy()
    m.tt = random.Random(seed).random() * 6
    m.amp = amp

    def u(mm, dt):
        mm.tt += dt
        mm.move_to(mm.base + np.array([mm.amp * np.sin(mm.tt * 1.7), mm.amp * 0.8 * np.sin(mm.tt * 2.3), 0]))
    m.add_updater(u)
    return m


def fly(m, pos, rt=1.0):
    st = m.base.copy()
    pos = np.array([pos[0], pos[1], 0.0])
    return UpdateFromAlphaFunc(m, lambda mm, a: setattr(mm, "base", st + (pos - st) * smooth(a)), run_time=rt)


# ---------------------------------------------------------------- the stem and the gall (scenes 1-2)
def make_stem():
    stem = Line([0, -3.8, 0], [0, 1.4, 0], color=GREEN, stroke_width=12)
    l1 = Ellipse(width=1.0, height=0.3, fill_color=GREEN, fill_opacity=0.85, stroke_width=0).rotate(0.5).move_to([-0.55, -1.0, 0])
    l2 = Ellipse(width=1.0, height=0.3, fill_color=GREEN, fill_opacity=0.85, stroke_width=0).rotate(-0.5).move_to([0.6, -2.2, 0])
    return VGroup(stem, l1, l2)


def gall_mob(gr, c=(0, 1.4), op=0.97):
    return always_redraw(lambda: Circle(radius=max(gr.get_value(), 0.01), fill_color=GALLC, fill_opacity=op,
                                        stroke_color=GALLE, stroke_width=3).move_to([c[0], c[1], 0]))


# scattered positions for the dozen galls (by size index), before they are lined up
_POS = [(-4.6, 2.0), (-1.5, 2.4), (1.8, 2.0), (4.9, 2.4), (-5.0, -0.2), (-2.2, 0.6), (0.9, -0.1), (3.6, 0.5),
        (-4.2, -2.3), (-1.0, -1.8), (2.2, -2.4), (5.0, -1.0)]
_PERM = [7, 2, 10, 4, 0, 9, 5, 11, 3, 8, 1, 6]
SCATTER = {}
for _k, _j in enumerate(_PERM):
    SCATTER[_j] = _POS[_k]


# ---------------------------------------------------------------- the world
class World:
    """Trackers: WA/BA = how far wasp / bird attack has been applied (0-1); AW/AB = attack strengths;
    MD = mix toward the schematic dip (disruptive)."""

    def __init__(self, wa=0.0, ba=0.0, aw=0.9, ab=0.9, md=0.0):
        self.WA, self.BA, self.AW, self.AB, self.MD = [ValueTracker(v) for v in (wa, ba, aw, ab, md)]

    def f_at(self, s):
        m = self.MD.get_value()
        fm = f_model(s, self.AW.get_value(), self.AB.get_value(), self.WA.get_value(), self.BA.get_value())
        return fm if m < 1e-4 else (1 - m) * fm + m * f_dip(s)

    # --- galls
    def row(self, scatter=False, op=0.97):
        gs = VGroup()
        for j in range(N):
            x, y = SCATTER[j] if scatter else (XS[j], GY)
            gs.add(Circle(radius=RR[j], fill_color=GALLC, fill_opacity=op, stroke_color=GALLE, stroke_width=3).move_to([x, y, 0]))
        lo, hi = ManimColor(DARKG), ManimColor(GALLC)

        def u(m):
            f = self.f_at(S)
            b = f / f.max()
            for g, bi in zip(m, b):
                g.set_fill(interpolate_color(lo, hi, float(bi)))
        gs.add_updater(u, call_updater=True)
        return gs

    # --- fitness plot furniture
    def axes(self):
        yax = Arrow([AXX, BASE, 0], [AXX, 3.45, 0], color=GREY, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        base = Line([AXX, BASE, 0], [5.15, BASE, 0], color=GREY, stroke_width=4)
        lab = T("relative fitness", 28).rotate(PI / 2).move_to([-6.35, 1.4, 0])
        return VGroup(yax, base), lab

    def avg(self):
        ln = DashedLine([AXX, fy(1), 0], [5.0, fy(1), 0], color=TEXT, stroke_width=3, dash_length=0.16)
        lb = T("average", 28).move_to([5.85, fy(1), 0])
        return ln, lb

    def xlab(self):
        a1 = Line([-3.6, XLAB, 0], [-1.05, XLAB, 0], color=GREY, stroke_width=3)
        a2 = Arrow([1.05, XLAB, 0], [3.6, XLAB, 0], color=GREY, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        return (T("small", 28).move_to([-4.6, XLAB, 0]), T("gall size", 28).move_to([0, XLAB, 0]),
                T("large", 28).move_to([4.6, XLAB, 0]), VGroup(a1, a2))

    # --- curve and dots, driven by the model
    def curve(self, color=YELLOW):
        c = VMobject(stroke_color=color, stroke_width=7)
        ss = np.linspace(0, 1, 80)

        def u(m):
            f = self.f_at(ss)
            m.set_points_as_corners([[sx(a), fy(b), 0] for a, b in zip(ss, f)])
        c.add_updater(u, call_updater=True)
        return c

    def dots(self, color=YELLOW):
        ds = VGroup(*[Dot(radius=0.1, color=color) for _ in range(N)])

        def u(m):
            f = self.f_at(S)
            for d, x, v in zip(m, XS, f):
                d.move_to([x, fy(v), 0])
        ds.add_updater(u, call_updater=True)
        return ds


def hist_bars(h, color=GALLC, op=0.8):
    return VGroup(*[Rectangle(width=0.8, height=max(HU * v, 0.02), fill_color=color, fill_opacity=op, stroke_width=0)
                    .move_to([x, HB + max(HU * v, 0.02) / 2, 0]) for x, v in zip(XS, h)])


def hist_ghost(h):
    return VGroup(*[Rectangle(width=0.8, height=max(HU * v, 0.02), stroke_color=GREY, stroke_width=2, fill_opacity=0)
                    .move_to([x, HB + max(HU * v, 0.02) / 2, 0]) for x, v in zip(XS, h)])


def hist_label(text="gall sizes before"):
    return T(text, 28).move_to([4.75, -2.75, 0])


def tag(text):
    t = T(text, 22, GREY)
    return t.move_to([-6.5 + t.width / 2, 3.65, 0])


def lean_dir_label():
    return T("directional", 40, YELLOW).move_to([2.3, 3.0, 0])


def stab_label():
    return T("stabilizing", 40, YELLOW).move_to([-2.2, 3.0, 0])


def mean_x(h):
    return sx(float(h @ S))


def base_world(sc, w, scatter=False, axes=True, avg=True, xlab=True, hist=None, hlabel="gall sizes before"):
    """Build the carried picture exactly where the previous scene left it; returns what it made."""
    d = {}
    d["row"] = w.row(scatter=scatter)
    sc.add(d["row"])
    if axes:
        a, lab = w.axes()
        d["axes"], d["ylab"] = a, lab
        sc.add(a, lab)
    if avg:
        ln, lb = w.avg()
        d["avg"], d["avglab"] = ln, lb
        sc.add(ln, lb)
    if xlab:
        s_, g_, l_, ar = w.xlab()
        d["xlab"] = VGroup(s_, g_, l_, ar)
        sc.add(d["xlab"])
    if hist is not None:
        d["hist"] = hist_bars(hist)
        d["hlab"] = hist_label(hlabel)
        sc.add(d["hist"], d["hlab"])
    return d


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Natural Selection in Ecological Context"
    TITLE = "Two Enemies, One Gall"


class S01Question(SpokenScene):
    def construct(self):
        moC = moth(CREAM, 1.8).move_to([-2.2, 0.8, 0])
        moD = moth(CHAR, 1.8).move_to([2.2, 0.8, 0])
        bC = Rectangle(width=1.2, height=2.3, fill_color=CREAM, fill_opacity=0.95, stroke_color=TEXT, stroke_width=2).move_to([-2.2, -3.2 + 1.15, 0])
        bD = Rectangle(width=1.2, height=1.0, fill_color=CHAR, fill_opacity=0.95, stroke_color=TEXT, stroke_width=2).move_to([2.2, -3.2 + 0.5, 0])
        lab = T("survival", 28).move_to([0, -3.55, 0])
        b = bird(1.0).move_to([0, 2.7, 0])
        hov(b)
        self.play(FadeIn(moC, scale=0.6), FadeIn(moD, scale=0.6), FadeIn(b), run_time=0.9)
        self.at("birds made")
        self.play(fly(b, [2.2, 1.9], 0.6))
        self.play(fly(b, [0, 2.7], 0.5))
        self.at("survive better")
        self.play(GrowFromEdge(bC, DOWN), GrowFromEdge(bD, DOWN), FadeIn(lab), run_time=1.2)
        echo = VGroup(moC, moD, bC, bD, lab, b)
        self.at("Now take a gall")
        b.clear_updaters()
        stem = make_stem()
        gr = ValueTracker(0.01)
        g = gall_mob(gr)
        self.play(FadeOut(echo, scale=0.4), run_time=0.5)
        self.play(Create(stem[0]), FadeIn(stem[1]), FadeIn(stem[2]), run_time=0.6)
        self.add(g)
        self.play(gr.animate.set_value(1.0), run_time=0.6)
        w = wasp(1.0)
        w.move_to([-7.5, 1.4, 0])
        hov(w, 0.08)
        self.add(w)
        self.at("If wasps attack small galls")
        self.play(fly(w, [-4.4, 1.4], 0.9), gr.animate.set_value(0.4), run_time=0.9)
        lw = T("small galls", 32, ORANGE).move_to([-4.4, 0.2, 0])
        self.at("small galls")
        self.play(FadeIn(lw), fly(w, [-1.6, 1.4], 0.45), run_time=0.45)
        self.play(fly(w, [-4.4, 1.4], 0.45), run_time=0.45)
        bd = bird(1.0, -1).move_to([7.5, 1.4, 0])
        hov(bd, 0.08)
        self.add(bd)
        self.at("birds attack large ones")
        self.play(fly(bd, [4.4, 1.4], 0.9), gr.animate.set_value(1.25), run_time=0.9)
        lb = T("large galls", 32, BLUE).move_to([4.4, 0.2, 0])
        self.at("large ones")
        self.play(FadeIn(lb), fly(bd, [1.9, 1.4], 0.45), run_time=0.45)
        self.play(fly(bd, [4.4, 1.4], 0.45), run_time=0.45)
        q = T("Which gall is safest?", 44, YELLOW).move_to([0, 3.25, 0])
        self.at("which gall is safest")
        self.play(Write(q), gr.animate.set_value(0.7), run_time=1.2)
        self.play(gr.animate.set_value(0.95), run_time=0.8)
        self.play(gr.animate.set_value(0.6), run_time=0.8)
        self.finish()


class S02Gall(SpokenScene):
    def construct(self):
        stem = make_stem()
        gr = ValueTracker(0.0)
        bud = Circle(radius=0.17, fill_color=GREEN, fill_opacity=1, stroke_width=0).move_to([0, 1.4, 0])
        lg = T("goldenrod", 32, GREEN).move_to([-2.5, -0.9, 0])
        self.at("goldenrod gall fly")
        self.play(GrowFromEdge(stem[0], DOWN), FadeIn(stem[1]), FadeIn(stem[2]), FadeIn(lg), FadeIn(bud, scale=0.4), run_time=0.8)
        fl = gallfly(1.0).move_to([6.8, 3.0, 0])
        hov(fl, 0.07)
        self.add(fl)
        lf = T("gall fly", 30).move_to([2.3, 2.9, 0])
        self.at("gall fly")
        self.play(fly(fl, [1.0, 2.6], 0.7), FadeIn(lf), run_time=0.7)
        self.at("lays an egg")
        self.play(fly(fl, [0.45, 1.95], 0.6), run_time=0.6)
        egg = Dot(radius=0.09, color=TEXT).move_to([0, 1.4, 0])
        le = T("egg", 30).move_to([1.3, 0.95, 0])
        self.at("egg in a bud")
        self.play(FadeIn(egg, scale=2.0), FadeIn(le), run_time=0.5)
        self.at("in a bud of")
        self.play(fly(fl, [6.8, 3.0], 1.0), FadeOut(lf), run_time=1.0)
        self.at("tall goldenrod")
        self.play(Indicate(stem[0], color=YELLOW, scale_factor=1.0), Indicate(lg, color=YELLOW), run_time=1.0)
        self.remove(fl)
        self.at("The plant grows a round gall")
        g = always_redraw(lambda: Circle(radius=max(gr.get_value(), 0.01), fill_color=GALLC, fill_opacity=0.6,
                                         stroke_color=GALLE, stroke_width=3).move_to([0, 1.4, 0]))
        self.add(g)
        self.bring_to_front(egg)
        self.play(FadeOut(lg), FadeOut(le), FadeOut(bud), gr.animate.set_value(1.1), run_time=1.6)
        lv = larva(1.0).move_to([0, 1.4, 0])
        self.at("around the larva")
        self.play(ReplacementTransform(egg, lv), run_time=0.6)
        llv = T("larva", 32).move_to([2.2, 1.4, 0])
        self.play(FadeIn(llv), run_time=0.4)
        lv.tt = 0.0
        lv.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.rotate(0.45 * np.cos(m.tt * 2.2) * dt)))
        cav = Circle(radius=0.6, fill_color=CAVITY, fill_opacity=0.0, stroke_color=GALLE, stroke_width=2).move_to([0, 1.4, 0])
        self.at("spends the winter inside")
        self.add(cav)
        self.bring_to_front(lv)
        self.play(cav.animate.set_fill(opacity=0.9), g.animate.set_stroke(width=6), FadeOut(llv), run_time=1.0)
        self.play(lv.animate.scale(1.5), run_time=0.8)
        ci = chip("insect", TEXT, 32).move_to([-3.6, 1.4, 0])
        cp = chip("plant", GREEN, 32).move_to([3.6, 1.4, 0])
        a1 = Arrow([-2.5, 1.4, 0], [-1.3, 1.4, 0], color=TEXT, buff=0, stroke_width=6)
        a2 = Arrow([2.5, 1.4, 0], [1.3, 1.4, 0], color=GREEN, buff=0, stroke_width=6)
        self.at("made by insect and plant together")
        self.play(FadeIn(ci, shift=RIGHT * 0.3), GrowArrow(a1), run_time=0.7)
        self.play(FadeIn(cp, shift=LEFT * 0.3), GrowArrow(a2), run_time=0.7)
        self.play(Indicate(g, color=YELLOW, scale_factor=1.06), run_time=0.8)
        gs = VGroup(*[Circle(radius=RR[j], fill_color=GALLC, fill_opacity=0.97, stroke_color=GALLE, stroke_width=3).move_to([SCATTER[j][0], SCATTER[j][1], 0]) for j in range(N)])
        self.at("galls vary widely")
        self.play(FadeOut(VGroup(stem, ci, cp, a1, a2, g, cav, lv)), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in [gs[j] for j in _PERM]], lag_ratio=0.18), run_time=2.2)
        self.finish()


class S03Axis(SpokenScene):
    def construct(self):
        w = World()
        row = w.row(scatter=True)
        self.add(row)
        self.at("Line the galls up")
        self.play(AnimationGroup(*[row[j].animate.move_to([XS[j], GY, 0]) for j in range(N)], lag_ratio=0.04, run_time=1.8))
        s_, g_, l_, ar = w.xlab()
        self.at("small on the left")
        self.play(FadeIn(s_), run_time=0.6)
        self.at("large on the right")
        self.play(FadeIn(l_), FadeIn(g_), Create(ar), run_time=0.8)
        hb = hist_bars(H_BEFORE)
        hl = hist_label("gall sizes before")
        self.play(AnimationGroup(*[GrowFromEdge(r, DOWN) for r in hb], lag_ratio=0.06), FadeIn(hl), run_time=1.5)
        axes, ylab = w.axes()
        self.at("Above them we will draw")
        self.play(Create(axes), run_time=1.0)
        self.at("relative fitness")
        self.play(FadeIn(ylab, shift=RIGHT * 0.2), run_time=0.8)
        sweep = Rectangle(width=0.9, height=0.95, fill_color=YELLOW, fill_opacity=0.25, stroke_color=YELLOW, stroke_width=3).move_to([XS[0], GY, 0])
        self.at("how well larvae")
        self.add(sweep)
        self.play(sweep.animate.move_to([XS[-1], GY, 0]), run_time=2.7, rate_func=linear)
        self.play(FadeOut(sweep), run_time=0.3)
        ln, lb = w.avg()
        self.at("compared with the average")
        self.play(Create(ln), FadeIn(lb), run_time=1.0)
        pt = Dot(radius=0.14, color=YELLOW).move_to([-0.45, fy(1.0) + 0.0, 0])
        self.at("A point above the dashed line")
        pt.move_to([-0.45, fy(1.55), 0])
        arr = Arrow([-0.45, fy(1.0) + 0.05, 0], [-0.45, fy(1.55) - 0.15, 0], color=YELLOW, buff=0, stroke_width=5)
        self.play(FadeIn(pt, scale=3), GrowArrow(arr), run_time=0.9)
        lbt = T("better than average", 32, YELLOW).move_to([2.2, fy(1.55), 0])
        self.at("better than average")
        self.play(FadeIn(lbt, shift=LEFT * 0.2), run_time=0.8)
        self.play(FadeOut(pt), FadeOut(arr), FadeOut(lbt), run_time=0.6)
        self.finish()


class S04Wasps(SpokenScene):
    def construct(self):
        w = World()
        d = base_world(self, w, hist=H_BEFORE)
        targets = [0, 1, 2, 3, 5]
        ws = []
        for k, j in enumerate(targets):
            x = wasp(0.55).move_to([-8.0 - 0.8 * k, 0.5 + 0.35 * (k % 3), 0])
            hov(x, 0.07, seed=k)
            ws.append(x)
            self.add(x)
        self.at("From the left come the wasps")
        self.play(*[fly(x, [XS[j] - 0.1, 0.45 + 0.5 * (k % 2)], 1.4 + 0.12 * k) for k, (x, j) in enumerate(zip(ws, targets))], run_time=2.0)
        c1 = T("parasitoid", 44, ORANGE).move_to([0, 3.0, 0])
        c2 = T("develops on or in a host", 32).move_to([0, 2.45, 0])
        c3 = T("and ultimately kills it", 32).move_to([0, 1.95, 0])
        self.at("parasitoid develops")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.8)
        self.at("ultimately kills it")
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.8)
        self.at("This parasitoid wasp attacks")
        self.play(FadeOut(VGroup(c1, c2, c3)), run_time=0.6)
        self.at("small galls more than")
        self.play(*[fly(x, [XS[j] - 0.05, -0.3 + 0.0 * (k % 2)], 0.8) for k, (x, j) in enumerate(zip(ws, targets))],
                  w.WA.animate.set_value(1.0), run_time=3.4, rate_func=linear)
        self.at("Many small galls go dark")
        self.play(Indicate(d["row"][0], color=ORANGE, scale_factor=1.3), Indicate(d["row"][1], color=ORANGE, scale_factor=1.3),
                  Indicate(d["row"][2], color=ORANGE, scale_factor=1.3), run_time=1.2)
        self.finish()


class S05Birds(SpokenScene):
    def construct(self):
        w = World(wa=1.0)
        d = base_world(self, w, hist=H_BEFORE)
        targets = [11, 10, 9, 8, 6]
        bs = []
        for k, j in enumerate(targets):
            x = bird(0.5, -1).move_to([8.0 + 0.9 * k, 0.55 + 0.35 * (k % 3), 0])
            hov(x, 0.07, seed=k + 3)
            bs.append(x)
            self.add(x)
        self.at("From the right come the birds")
        self.play(*[fly(x, [XS[j] + 0.1, 0.5 + 0.55 * (k % 2)], 1.3 + 0.12 * k) for k, (x, j) in enumerate(zip(bs, targets))], run_time=1.9)
        self.at("peck open the large galls")
        self.play(*[fly(x, [XS[j] + 0.05, -0.15], 0.7) for k, (x, j) in enumerate(zip(bs, targets))],
                  w.BA.animate.set_value(1.0), run_time=3.4, rate_func=linear)
        self.play(*[Indicate(d["row"][j], color=BLUE, scale_factor=1.3) for j in (11, 10, 9)], run_time=1.0)
        self.at("Many large galls go dark")
        ring = SurroundingRectangle(VGroup(d["row"][4], d["row"][7]), color=YELLOW, buff=0.12, stroke_width=4)
        self.play(*[fly(x, [XS[j] + 0.1, 0.9], 0.8) for x, j in zip(bs, targets)], Create(ring), run_time=1.2)
        self.play(FadeOut(ring), run_time=0.8)
        self.finish()


def icon_pair(wsc=1.0, bsc=1.0, y=2.55):
    wi = wasp(wsc).move_to([-4.85, y, 0])
    bi = bird(bsc, -1).move_to([4.85, y, 0])
    hov(wi, 0.07, seed=1)
    hov(bi, 0.07, seed=2)
    return wi, bi


class S06Hump(SpokenScene):
    def construct(self):
        w = World(wa=1.0, ba=1.0)
        d = base_world(self, w, hist=H_BEFORE)
        ring = SurroundingRectangle(VGroup(d["row"][4], d["row"][7]), color=YELLOW, buff=0.12, stroke_width=4)
        self.at("the middle survives best")
        self.play(Create(ring), run_time=0.9)
        self.play(Indicate(d["row"][5], scale_factor=1.3), Indicate(d["row"][6], scale_factor=1.3), run_time=0.9)
        wi, bi = icon_pair(1.0, 1.0)
        a1 = Arrow([-3.5, 2.55, 0], [-1.9, 2.55, 0], color=ORANGE, buff=0, stroke_width=8)
        a2 = Arrow([3.5, 2.55, 0], [1.9, 2.55, 0], color=BLUE, buff=0, stroke_width=8)
        for a, sgn in ((a1, 1), (a2, -1)):
            a.t0 = a.get_center().copy()
            a.tt = 0.0
            a.add_updater(lambda m, dt, sgn=sgn: (setattr(m, "tt", m.tt + dt), m.move_to(m.t0 + RIGHT * sgn * 0.18 * np.sin(m.tt * 3))))
        self.at("two named enemies")
        self.play(FadeOut(ring), FadeIn(wi, shift=RIGHT * 0.4), FadeIn(bi, shift=LEFT * 0.4), run_time=0.9)
        self.add(a1, a2)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        tg = tag("schematic toy model: equal-strength enemies, survival from both multiplied")
        self.at("Take a simple model")
        self.play(FadeIn(tg), run_time=0.8)
        eq = T("equal strength", 32).move_to([0, 2.55, 0])
        self.at("equally strong")
        self.play(FadeIn(eq), run_time=0.7)
        self.at("The fitness curve")
        self.play(FadeOut(VGroup(wi, bi, a1, a2, eq)), run_time=0.7)
        curve = w.curve()
        dots = w.dots()
        self.at("rises")
        self.play(Create(curve, run_time=3.4, rate_func=linear),
                  LaggedStart(*[FadeIn(dt, scale=2.5) for dt in dots], lag_ratio=1.0, run_time=3.4))
        self.add(dots)
        self.at("Favoring the middle")
        self.play(Indicate(curve, color=TEXT, scale_factor=1.04), run_time=1.2)
        sl = stab_label()
        self.at("stabilizing")
        self.play(FadeIn(sl, shift=DOWN * 0.2), run_time=0.7)
        ghost = hist_ghost(H_BEFORE)
        after = hist_bars(H_SYM)
        hl2 = hist_label("gall sizes after")
        self.at("Below the spread")
        self.add(ghost)
        self.play(Transform(d["hist"], after), Transform(d["hlab"], hl2), run_time=2.2)
        self.play(Indicate(d["hist"], color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.finish()


def s6_state(sc, w, with_curve=True, tagtext="schematic toy model: equal-strength enemies, survival from both multiplied", heavy=False):
    d = base_world(sc, w, hist=H_HEAVY if heavy else H_SYM, hlabel="gall sizes after")
    d["ghost"] = hist_ghost(H_BEFORE)
    sc.add(d["ghost"])
    if with_curve:
        d["curve"], d["dots"] = w.curve(), w.dots()
        sc.add(d["curve"], d["dots"])
    d["tag"] = tag(tagtext)
    d["stab"] = stab_label()
    sc.add(d["tag"], d["stab"])
    return d


def marker(x=0.0):
    ln = DashedLine([x, BASE, 0], [x, 2.85, 0], color=YELLOW, stroke_width=5, dash_length=0.14)
    lb = T("old average", 28, YELLOW).move_to([x + 2.4, 0.35, 0])
    return ln, lb


class S07Predict(SpokenScene):
    def construct(self):
        w = World(wa=1.0, ba=1.0)
        d = s6_state(self, w)
        wi, bi = icon_pair(1.0, 1.0)
        self.add(wi, bi)
        self.play(FadeOut(d["stab"]), run_time=0.5)
        self.at("make wasp attack heavier")
        self.play(wi.animate.scale(1.4), run_time=1.6)
        q = T("Does the average stay put?", 36, YELLOW).move_to([0, 3.15, 0])
        self.at("Does the average")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.8)
        ln, lb = marker(0.0)
        self.at("average surviving gall")
        self.play(Create(ln), FadeIn(lb), run_time=1.0)
        self.finish()


class S08Pause(SpokenScene):
    def construct(self):
        w = World(wa=1.0, ba=1.0)
        d = s6_state(self, w)
        wi, bi = icon_pair(1.4, 1.0)
        self.remove(d["stab"])
        self.add(wi, bi)
        q = T("Does the average stay put?", 36, YELLOW).move_to([0, 3.15, 0])
        ln, lb = marker(0.0)
        prog = ValueTracker(0.0)
        C = np.array([3.75, 3.15, 0])
        back = Circle(radius=0.28, color=GREY, stroke_width=3).move_to(C)
        ring = always_redraw(lambda: Arc(radius=0.28, start_angle=PI / 2, angle=-max(TAU * (1 - prog.get_value()), 0.01),
                                         arc_center=C, color=YELLOW, stroke_width=6))
        self.add(q, ln, lb, back, ring)
        self.play(prog.animate.set_value(1.0), run_time=4.9, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        w = World(wa=1.0, ba=1.0)
        d = s6_state(self, w)
        wi, bi = icon_pair(1.4, 1.0)
        self.remove(d["stab"])
        self.add(wi, bi)
        q = T("Does the average stay put?", 36, YELLOW).move_to([0, 3.15, 0])
        ln, lb = marker(0.0)
        self.add(q, ln, lb)
        no = T("No.", 56, RED).move_to([0, 3.15, 0])
        self.at("Now")
        self.play(FadeOut(q), run_time=0.25)
        self.play(FadeIn(no, scale=1.3), run_time=0.35)
        self.at("in the model")
        tg2 = tag("schematic toy model: wasp attack heavier than bird attack, survival from both multiplied")
        self.play(Transform(d["tag"], tg2), run_time=0.5)
        self.at("the peak slides")
        self.play(w.AW.animate.set_value(0.95), w.AB.animate.set_value(0.7), FadeOut(no), run_time=3.4, rate_func=smooth)
        self.play(Indicate(wi, scale_factor=1.15), run_time=1.0)
        self.at("The spread still narrows")
        self.play(Transform(d["hist"], hist_bars(H_HEAVY)), FadeOut(wi), FadeOut(bi), run_time=2.2)
        nx = mean_x(H_HEAVY)
        nm = DashedLine([nx, BASE, 0], [nx, 2.85, 0], color=YELLOW, stroke_width=5, dash_length=0.14)
        ar = Arrow([0.15, 3.1, 0], [nx + 0.45, 3.1, 0], color=YELLOW, buff=0, stroke_width=8)
        mm = T("mean moves up", 32, YELLOW).move_to([3.4, 3.1, 0])
        self.at("average moves up")
        self.play(Create(nm), GrowArrow(ar), FadeIn(mm), run_time=1.4)
        dl = lean_dir_label()
        self.at("directional selection")
        self.play(FadeOut(VGroup(lb, ar, mm)), FadeIn(dl, shift=DOWN * 0.2), run_time=0.9)
        st = stab_label()
        self.at("So one trait")
        self.play(FadeIn(st, shift=DOWN * 0.2), run_time=0.8)
        self.at("stabilizing")
        self.play(Indicate(st, scale_factor=1.15), Indicate(d["curve"], color=TEXT, scale_factor=1.0), run_time=1.1)
        self.at("a directional component")
        self.play(Indicate(dl, scale_factor=1.15), run_time=1.1)
        self.finish()


def s9_state(sc, w, tagtext="schematic: shape only"):
    d = base_world(sc, w, hist=H_HEAVY, hlabel="gall sizes after")
    d["ghost"] = hist_ghost(H_BEFORE)
    sc.add(d["ghost"])
    d["curve"], d["dots"] = w.curve(), w.dots()
    sc.add(d["curve"], d["dots"])
    d["tag"] = tag(tagtext)
    sc.add(d["tag"])
    return d


class S10Field(SpokenScene):
    def construct(self):
        w = World(wa=1.0, ba=1.0, aw=0.95, ab=0.7)
        d = s9_state(self, w, "schematic toy model: wasp attack heavier than bird attack, survival from both multiplied")
        stab, dirl = stab_label(), lean_dir_label()
        nx = mean_x(H_HEAVY)
        nm = DashedLine([nx, BASE, 0], [nx, 2.85, 0], color=YELLOW, stroke_width=5, dash_length=0.14)
        om = DashedLine([0, BASE, 0], [0, 2.85, 0], color=YELLOW, stroke_width=5, dash_length=0.14)
        wi0, bi0 = icon_pair(1.4, 1.0)
        self.add(stab, dirl, nm, om, wi0, bi0)
        tg2 = tag("schematic: shape only")
        self.at("A field study")
        self.play(FadeOut(VGroup(stab, dirl, nm, om, wi0, bi0)), Transform(d["tag"], tg2), run_time=0.7)
        pa = Polygon([-4.4, 2.2, 0], [-2.2, 2.2, 0], [-2.0, 2.65, 0], [-2.6, 3.25, 0], [-4.4, 3.25, 0], color=TEXT, stroke_width=3,
                     fill_color=GREEN, fill_opacity=0.18)
        self.play(Create(pa), run_time=0.8)
        lcp = T("central Pennsylvania", 30).move_to([-3.2, 1.85, 0])
        self.at("central Pennsylvania")
        self.play(FadeIn(lcp), run_time=0.6)
        rng = random.Random(5)
        fds = VGroup(*[Dot(radius=0.07, color=YELLOW).move_to([rng.uniform(-4.2, -2.5), rng.uniform(2.35, 3.1), 0]) for _ in range(20)])
        self.at("20 fields")
        self.play(LaggedStart(*[FadeIn(f, scale=2.5) for f in fds], lag_ratio=0.12), run_time=1.6)
        c2y = chip("2 years", TEXT, 28).move_to([-0.5, 2.8, 0])
        self.at("two years")
        self.play(FadeIn(c2y), run_time=0.7)
        self.play(FadeOut(c2y), run_time=0.3)
        wi = wasp(1.0).move_to([3.2, 3.05, 0])
        bi = bird(0.65, -1).move_to([5.4, 3.05, 0])
        hov(wi, 0.06, seed=1)
        hov(bi, 0.06, seed=2)
        gt = T(">", 56, ORANGE).move_to([4.3, 3.05, 0])
        self.at("Parasitoid attack was more frequent")
        self.play(FadeOut(VGroup(pa, lcp, fds)), FadeIn(wi), FadeIn(gt), FadeIn(bi), run_time=1.0)
        lp = T("more attack", 28, ORANGE).move_to([3.2, 2.4, 0])
        self.play(FadeIn(lp), run_time=0.5)
        self.at("Intermediate galls survived best")
        self.play(FadeOut(VGroup(wi, bi, gt, lp)), run_time=0.5)
        ring = Circle(radius=0.42, color=TEXT, stroke_width=5).move_to([sx(0.6), fy(1.38), 0])
        self.play(Create(ring), run_time=0.9)
        self.play(Indicate(ring, scale_factor=1.3, color=YELLOW), run_time=0.8)
        ar = Arrow([1.0, 2.75, 0], [4.9, 2.75, 0], color=YELLOW, buff=0, stroke_width=8)
        lg = T("larger galls favored", 32, YELLOW).move_to([2.95, 3.15, 0])
        self.at("selection also favored larger galls")
        self.play(FadeOut(ring), GrowArrow(ar), FadeIn(lg), run_time=1.2)
        self.finish()


class S11Disruptive(SpokenScene):
    def construct(self):
        w = World(wa=1.0, ba=1.0, aw=0.95, ab=0.7)
        d = s9_state(self, w)
        self.at("flip the hump")
        self.play(w.MD.animate.set_value(1.0), run_time=2.4, rate_func=smooth)
        ring_m = SurroundingRectangle(VGroup(d["row"][5], d["row"][6]), color=RED, buff=0.12, stroke_width=4)
        ring_e1 = SurroundingRectangle(d["row"][0], color=GREEN, buff=0.12, stroke_width=4)
        ring_e2 = SurroundingRectangle(d["row"][11], color=GREEN, buff=0.12, stroke_width=4)
        self.at("The middle does worst")
        self.play(Create(ring_m), run_time=0.8)
        self.at("both ends do better")
        self.play(Create(ring_e1), Create(ring_e2), run_time=0.8)
        self.play(FadeOut(VGroup(ring_m, ring_e1, ring_e2)), run_time=0.5)
        dl = T("disruptive", 40, YELLOW).move_to([0, 2.95, 0])
        self.at("That shape is called")
        self.play(Transform(d["hist"], hist_bars(H_DIP)), FadeIn(dl, shift=DOWN * 0.2), run_time=2.4)
        def band(x0, x1, color):
            r = Rectangle(width=x1 - x0, height=6.8, fill_color=color, fill_opacity=0.0, stroke_width=0).move_to([(x0 + x1) / 2, -0.4, 0])
            r.tt = 0.0
            r.on = ValueTracker(0.0)
            r.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.set_fill(opacity=m.on.get_value() * (0.16 + 0.08 * np.sin(m.tt * 2.6)))))
            return r
        bm = band(-1.8, 1.8, RED)
        be1, be2 = band(-5.55, -3.5, GREEN), band(3.5, 5.55, GREEN)
        self.add(bm, be1, be2)
        lm = T("commonest resource", 28, RED).move_to([0, 2.05, 0])
        le1 = T("different", 28, GREEN).move_to([-4.5, 0.35, 0])
        le2 = T("different", 28, GREEN).move_to([4.5, 0.35, 0])
        self.at("crowd onto")
        self.play(bm.on.animate.set_value(1.0), FadeIn(lm), run_time=1.0)
        self.at("something different")
        self.play(be1.on.animate.set_value(1.0), be2.on.animate.set_value(1.0), FadeIn(le1), FadeIn(le2), run_time=1.0)
        self.finish()


def mini_panel(cx, kind):
    frame = RoundedRectangle(corner_radius=0.12, width=3.6, height=2.7, stroke_color=GREY, stroke_width=2.5).move_to([cx, 1.55, 0])
    ss = np.linspace(0, 1, 80)
    f = f_shape(kind, ss)
    c = VMobject(stroke_color=YELLOW, stroke_width=6)
    c.set_points_as_corners([[cx - 1.5 + 3.0 * a, 0.45 + 1.0 * b, 0] for a, b in zip(ss, f)])
    av = DashedLine([cx - 1.6, 1.45, 0], [cx + 1.6, 1.45, 0], color=TEXT, stroke_width=2, dash_length=0.12)
    yl = T("relative fitness", 22).rotate(PI / 2).move_to([cx - 1.95, 1.55, 0])
    return VGroup(frame, av, yl), c


class S12Close(SpokenScene):
    def construct(self):
        w = World(wa=1.0, ba=1.0)
        row = w.row(op=0.35)
        self.add(row)
        xs = [-4.35, 0.0, 4.35]
        kinds = ["ramp", "hump", "dip"]
        names = ["directional", "stabilizing", "disruptive"]
        panels, curves, labels = [], [], []
        for cx, k, nm in zip(xs, kinds, names):
            p, c = mini_panel(cx, k)
            panels.append(p)
            curves.append(c)
            labels.append(T(nm, 30, YELLOW).move_to([cx, -0.12, 0]))
        self.at("One end")
        self.play(FadeIn(panels[0]), Create(curves[0]), run_time=1.0)
        self.at("the middle")
        self.play(FadeIn(panels[1]), Create(curves[1]), run_time=0.6)
        self.at("both ends")
        self.play(FadeIn(panels[2]), Create(curves[2]), run_time=0.8)
        self.at("Directional")
        self.play(FadeIn(labels[0], shift=UP * 0.15), run_time=0.6)
        self.at("stabilizing")
        self.play(FadeIn(labels[1], shift=UP * 0.15), run_time=0.6)
        self.at("disruptive")
        self.play(FadeIn(labels[2], shift=UP * 0.15), run_time=0.6)
        # one curve
        big = VMobject(stroke_color=YELLOW, stroke_width=7)
        ss = np.linspace(0, 1, 80)
        U = ValueTracker(1.0)
        FS_ = [f_shape(k, ss) for k in ("ramp", "hump", "dip")]

        def ub(m):
            u = U.get_value()
            i = int(np.floor(u)) % 3
            a = u - np.floor(u)
            f = (1 - a) * FS_[i] + a * FS_[(i + 1) % 3]
            m.set_points_as_corners([[sx(x), fy(y), 0] for x, y in zip(ss, f)])
        big.add_updater(ub, call_updater=True)
        axes, ylab = w.axes()
        ln, lb = w.avg()
        tgt = VMobject()
        tgt.set_points_as_corners([[sx(x), fy(y), 0] for x, y in zip(ss, FS_[1])])
        self.at("one curve")
        self.play(FadeOut(VGroup(*panels)), *[labels[i].animate.move_to([xs[i], 3.35, 0]) for i in range(3)], row.animate.set_opacity(0.97),
                  FadeIn(axes), FadeIn(ylab), Create(ln), FadeIn(lb), run_time=0.9)
        self.play(Transform(curves[0], tgt.copy().set_stroke(YELLOW, 7)), Transform(curves[1], tgt.copy().set_stroke(YELLOW, 7)),
                  Transform(curves[2], tgt.copy().set_stroke(YELLOW, 7)), run_time=0.9)
        self.remove(*curves)
        self.add(big)
        self.at("not boxes")
        self.play(U.animate.set_value(2.0), Indicate(labels[2], scale_factor=1.15), run_time=1.5)
        self.play(U.animate.set_value(3.0), Indicate(labels[0], scale_factor=1.15), run_time=1.3)
        self.at("read the curve first")
        self.play(U.animate.set_value(4.0), Indicate(labels[1], scale_factor=1.15), run_time=1.4)
        self.at("then name the mode")
        self.play(Indicate(labels[1], scale_factor=1.2, color=TEXT), Indicate(big, scale_factor=1.0, color=TEXT), run_time=1.4)
        self.finish()


class S13End(EndCard):
    LINE = "The shape of the fitness curve names the mode of selection."
