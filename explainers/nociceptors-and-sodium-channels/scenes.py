"""Nociceptors and the sodium channels of pain: blocking a channel is not silencing a neuron.

COLOR MAP (one color per concept, whole film)
  YELLOW = the gene (SCN9A)
  ORANGE = Nav1.7
  TEAL   = Nav1.8, its current, and its fitted curve
  PURPLE = Nav1.9
  RED    = loss: broken copy, blocker, blocked fraction
  GREEN  = the measured fraction of current that remains (marked points)
  TEXT   = the control spike trace (before the blocker)
  GREY   = membranes, axes, tags, sketch labels
"""
import numpy as np
from scipy.interpolate import PchipInterpolator
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEAL_C = "#3FB8C0"
KD = 0.38


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 1))


def mem_bar(cx, cy, w, h=0.34):
    return RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([cx, cy, 0])


def chan(text, color, cx, cy, size=30):
    """a labelled channel chip that straddles a membrane bar (opaque backing)."""
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    g = VGroup(back, *c)
    return g.move_to([cx, cy, 0])


def cross(mob, color=RED, w=6):
    r = mob.width / 2 * 0.8
    c = mob.get_center()
    return VGroup(Line(c + np.array([-r, r, 0]) * 0.8, c + np.array([r, -r, 0]) * 0.8, color=color, stroke_width=w),
                  Line(c + np.array([-r, -r, 0]) * 0.8, c + np.array([r, r, 0]) * 0.8, color=color, stroke_width=w))


def tag(lines, color=GREY, size=24, w=3.9):
    t = VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=0.1)
    return fit(t, max_w=w, max_h=3)


# fitted curve and its axes (shared by s03 and s04) -------------------------------------------
def frac(c):
    return 1.0 / (1.0 + c / KD)


def make_axes():
    ax = Axes(x_range=[-1, 2, 1], y_range=[0, 1, 0.5], x_length=6.6, y_length=4.8,
              axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True, "include_tip": False},
              tips=False)
    ax.shift(LEFT * 3.0 + DOWN * 0.5)
    xl = VGroup(*[T(s, 22, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v, s in [(-1, "0.1"), (0, "1"), (1, "10"), (2, "100")]])
    yl = VGroup(*[T(s, 22, GREY).next_to(ax.c2p(-1, v), LEFT, buff=0.15) for v, s in [(0, "0"), (0.5, "0.5"), (1, "1")]])
    xt = T("drug concentration (nM, log scale)", 24, GREY).next_to(ax, DOWN, buff=0.6)
    yt = T("fraction of maximal current", 24, GREY).next_to(ax.c2p(-1, 1), UP, buff=0.3).align_to(ax.c2p(-1, 1), LEFT)
    curve = ax.plot(lambda x: frac(10 ** x), x_range=[-1, 2, 0.01], color=TEAL_C, stroke_width=6, use_smoothing=False)
    return ax, VGroup(xl, yl, xt, yt), curve


def dot_at(ax, c, color):
    return Dot(ax.c2p(np.log10(c), frac(c)), radius=0.11, color=color)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Nociceptors and the sodium channels of pain"
    TITLE = "Blocking a Channel Is Not Silence"


# ---------------------------------------------------------------------------------------------
class S01Families(SpokenScene):
    def construct(self):
        self.at("Three families")
        fams = VGroup(*[chip(f"Family {i}", GREY, 34) for i in (1, 2, 3)]).arrange(RIGHT, buff=0.7).move_to([0, 2.3, 0])
        place = T("northern Pakistan", 28, GREY).next_to(fams, UP, buff=0.3)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in fams], lag_ratio=0.25), FadeIn(place), run_time=1.2)
        self.at("never experienced pain")
        nope = T("members who had never experienced pain", 32, TEXT).next_to(fams, DOWN, buff=0.5)
        self.play(FadeIn(nope, shift=UP * 0.15), run_time=0.8)

        self.at("two broken copies")
        self.play(FadeOut(nope), FadeOut(place), fams.animate.scale(0.6).to_corner(UL, buff=0.5), run_time=0.8)
        gene = chip("SCN9A", YELLOW, 44).move_to([-3.6, 1.5, 0])
        c1 = chip("copy 1", YELLOW, 30)
        c2 = chip("copy 2", YELLOW, 30)
        copies = VGroup(c1, c2).arrange(RIGHT, buff=0.6).next_to(gene, DOWN, buff=0.7)
        gl = T("the gene", 26, GREY).next_to(gene, UP, buff=0.2)
        self.play(FadeIn(gene, scale=0.9), FadeIn(gl), run_time=0.6)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        x1, x2 = cross(c1), cross(c2)
        self.play(Create(x1), Create(x2), c1.animate.set_opacity(0.45), c2.animate.set_opacity(0.45), run_time=0.7)
        brk = T("both copies broken", 28, RED).next_to(copies, DOWN, buff=0.3)
        self.play(FadeIn(brk), run_time=0.4)

        self.at("makes the channel")
        mem = mem_bar(3.4, 1.5, 4.4)
        nav = chan("Nav1.7", ORANGE, 3.4, 1.5, 40)
        a = arr(gene.get_right() + RIGHT * 0.05, [1.0, 1.5, 0], YELLOW)
        self.play(GrowArrow(a), FadeIn(mem), run_time=0.5)
        self.play(FadeIn(nav, scale=0.9), run_time=0.5)
        self.play(FadeOut(fams), run_time=0.3)

        self.at("cultured cells")
        ax = Axes(x_range=[0, 4, 1], y_range=[-0.4, 1, 1], x_length=5.2, y_length=2.2,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False, "include_tip": False}, tips=False)
        ax.move_to([3.4, -2.0, 0])
        base = DashedLine(ax.c2p(0, 0), ax.c2p(4, 0), color=GREY, dash_length=0.12, stroke_width=3)
        lbl = T("background", 24, GREY).next_to(ax.c2p(4, 0), UP, buff=0.12).shift(LEFT * 0.7)
        flat = Line(ax.c2p(0, 0), ax.c2p(4, 0), color=RED, stroke_width=6)
        yl = T("current", 24, GREY).next_to(ax, LEFT, buff=0.2)
        cap = T("mutant channels, in cultured cells", 26, TEXT).next_to(ax, UP, buff=0.35)
        # the mutant channel passes nothing: grey it
        self.play(FadeIn(ax), FadeIn(yl), FadeIn(cap), Create(base), FadeIn(lbl), run_time=0.7)
        self.play(Create(flat), nav.animate.set_opacity(0.45), run_time=0.8)
        nocur = T("no current above background", 28, RED).next_to(ax, DOWN, buff=0.25)
        self.play(FadeIn(nocur), run_time=0.4)

        self.at("Lose this channel")
        rule = T("Lose this channel, lose pain.", 34, TEXT, font=TITLE_FONT).move_to([-3.9, -2.7, 0])
        self.play(Write(rule), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Drug(SpokenScene):
    def construct(self):
        ycy = 0.5
        mem = mem_bar(0, ycy, 12.0, 0.42)
        mlab = T("nociceptor membrane (schematic)", 24, GREY).move_to([0, -3.4, 0])
        xs = [-4.1, 0, 4.1]
        c7 = chan("Nav1.7", ORANGE, xs[0], ycy, 38)
        c8 = chan("Nav1.8", TEAL_C, xs[1], ycy, 38)
        c9 = chan("Nav1.9", PURPLE, xs[2], ycy, 38)
        self.at("Nociceptor spikes")
        self.play(FadeIn(mem), FadeIn(mlab), run_time=0.6)
        self.at("three sodium channels")
        self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in (c7, c8, c9)], lag_ratio=0.3), run_time=1.4)

        self.at("selective blocker")
        b7 = chip("selective blocker", RED, 26).move_to([xs[0], ycy + 2.3, 0])
        i7 = inhib(b7.get_bottom() + DOWN * 0.05, c7.get_top() + UP * 0.05)
        self.play(FadeIn(b7, shift=DOWN * 0.2), run_time=0.5)
        self.play(Create(i7), run_time=0.4)
        self.at("did not significantly")
        t7 = tag(["no significant gain", "over placebo in", "one trial: painful", "diabetic neuropathy"], TEXT, 26, 3.9).next_to(c7, DOWN, buff=0.7)
        self.play(FadeIn(t7, shift=UP * 0.15), c9.animate.set_opacity(0.4), run_time=0.8)

        self.at("approved in the")
        b8 = chip("blocker", RED, 26).move_to([xs[1], ycy + 2.3, 0])
        i8 = inhib(b8.get_bottom() + DOWN * 0.05, c8.get_top() + UP * 0.05)
        self.play(FadeIn(b8, shift=DOWN * 0.2), run_time=0.5)
        self.play(Create(i8), run_time=0.4)
        t8 = tag(["approved in the", "United States,", "January 2025:", "moderate-to-severe", "acute pain in adults"], TEXT, 26, 3.9).next_to(c8, DOWN, buff=0.7)
        self.at("instead")
        self.play(FadeIn(t8, shift=UP * 0.15), t7.animate.set_opacity(0.5), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def panel_formula(sc, ax):
    f = M("I(C) = Imax / (1 + C / Kd)", 28, TEAL_C)
    return f


class S03Curve(SpokenScene):
    def construct(self):
        ax, labs, curve = make_axes()
        self.at("how is a blocker described")
        who = chip("human Nav1.8, cell line, 37 °C", TEAL_C, 26).move_to([3.7, 2.9, 0])
        who.set_width(min(who.width, 5.2))
        self.play(FadeIn(ax), FadeIn(labs), FadeIn(who, shift=DOWN * 0.15), run_time=1.0)
        self.at("fitted curve")
        self.play(Create(curve), run_time=2.0)
        fm = M("I(C) = Imax / (1 + C / Kd)", 28, TEAL_C).move_to([3.7, 1.7, 0])
        fm.set_width(min(fm.width, 5.0))
        self.play(FadeIn(fm), run_time=0.6)
        self.at("Half the current")
        kx = np.log10(KD)
        hl = DashedLine(ax.c2p(-1, 0.5), ax.c2p(kx, 0.5), color=YELLOW, dash_length=0.12, stroke_width=3)
        vl = DashedLine(ax.c2p(kx, 0.5), ax.c2p(kx, 0), color=YELLOW, dash_length=0.12, stroke_width=3)
        dot = Dot(ax.c2p(kx, 0.5), radius=0.12, color=YELLOW)
        half = T("half remains", 28, YELLOW).move_to([3.7, 0.0, 0])
        self.play(Create(hl), run_time=0.5)
        self.play(Create(vl), FadeIn(dot), FadeIn(half), run_time=0.6)
        self.at("In this fit")
        kd = M("Kd = 0.38 nM", 34, YELLOW).move_to([3.7, -1.0, 0])
        kd2 = T("at 37 °C", 28, GREY).next_to(kd, DOWN, buff=0.25)
        self.play(FadeIn(kd, scale=0.9), FadeIn(kd2), run_time=0.7)
        self.finish()


class S04Numbers(SpokenScene):
    def construct(self):
        ax, labs, curve = make_axes()
        kx = np.log10(KD)
        hl = DashedLine(ax.c2p(-1, 0.5), ax.c2p(kx, 0.5), color=YELLOW, dash_length=0.12, stroke_width=3)
        vl = DashedLine(ax.c2p(kx, 0.5), ax.c2p(kx, 0), color=YELLOW, dash_length=0.12, stroke_width=3)
        dot = Dot(ax.c2p(kx, 0.5), radius=0.12, color=YELLOW)
        who = chip("human Nav1.8, cell line, 37 °C", TEAL_C, 26).move_to([3.7, 2.9, 0])
        who.set_width(min(who.width, 5.2))
        fm = M("I(C) = Imax / (1 + C / Kd)", 28, TEAL_C).move_to([3.7, 1.7, 0])
        fm.set_width(min(fm.width, 5.0))
        kd = M("Kd = 0.38 nM", 34, YELLOW).move_to([3.7, 0.2, 0])
        self.add(ax, labs, curve, hl, vl, dot, who, fm, kd)
        self.at("Put in numbers")
        self.play(FadeOut(hl), FadeOut(vl), FadeOut(dot), kd.animate.move_to([3.7, 2.0, 0]).scale(0.8),
                  fm.animate.move_to([3.7, 2.9, 0]).set_opacity(0.0), FadeOut(who), run_time=0.7)
        self.at("fraction left")
        f1 = M("left = Kd / (Kd + C)", 26, TEAL_C).move_to([3.7, 1.0, 0])
        self.play(FadeIn(f1), run_time=0.7)
        self.at("that leaves")
        d1 = dot_at(ax, 10, GREEN)
        v1 = DashedLine(ax.c2p(1, 0), ax.c2p(1, frac(10)), color=GREEN, dash_length=0.12, stroke_width=3)
        e1 = M("C = 10 nM: 0.38/10.38", 26, GREEN).move_to([3.7, 0.0, 0])
        r1 = M("= 3.66% left", 34, GREEN).move_to([3.7, -0.8, 0])
        self.play(Create(v1), FadeIn(d1, scale=1.5), FadeIn(e1), run_time=0.8)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.at("reach 99")
        c99 = 99 * KD
        d2 = dot_at(ax, c99, RED)
        v2 = DashedLine(ax.c2p(np.log10(c99), 0), ax.c2p(np.log10(c99), frac(c99)), color=RED, dash_length=0.12, stroke_width=3)
        e2 = M("99% block: 1% left", 26, RED).move_to([3.7, -1.9, 0])
        self.play(Create(v2), FadeIn(d2, scale=1.5), FadeIn(e2), run_time=0.7)
        self.at("the concentration must be")
        r2 = M("C = 99 x 0.38 = 37.62 nM", 24, RED).move_to([3.7, -2.8, 0])
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def spike_fn(drug):
    if not drug:
        pts = [(0, 0), (0.45, 0.02), (0.62, 0.30), (0.78, 1.0), (0.95, 0.74), (1.15, 0.46),
               (1.5, 0.40), (1.85, 0.02), (2.1, -0.14), (2.6, 0.0), (3.0, 0.0)]
    else:
        pts = [(0, 0), (0.45, 0.02), (0.62, 0.30), (0.78, 0.68), (0.95, 0.48), (1.15, 0.28),
               (1.5, 0.24), (1.85, 0.0), (2.1, -0.10), (2.6, 0.0), (3.0, 0.0)]
    x, y = zip(*pts)
    return PchipInterpolator(x, y)


def train(drug, n, gap=3.0):
    f = spike_fn(drug)
    xs, ys = [], []
    for k in range(n):
        t = np.linspace(0, gap, 60, endpoint=False)
        xs.extend(t + k * gap)
        ys.extend(np.clip(f(np.minimum(t, 3.0)), -1, 2))
    return np.array(xs), np.array(ys)


class S05Neuron(SpokenScene):
    def construct(self):
        sk = chip("in this sketch (relative units)", GREY, 24).move_to([0, 3.35, 0])
        who = T("dissociated sensory neurons, adult human organ donors, 37 °C", 26, TEXT).move_to([0, 2.75, 0])
        self.at("Now ask the neuron")
        self.play(FadeIn(sk), FadeIn(who), run_time=0.7)

        # left: spike trains
        def tr_axes(cy):
            return Axes(x_range=[0, 15, 1], y_range=[-0.3, 1.1, 1], x_length=5.9, y_length=2.2,
                        axis_config={"color": GREY, "stroke_width": 2, "include_ticks": False, "include_tip": False},
                        tips=False).move_to([-3.4, cy, 0])
        a1, a2 = tr_axes(0.95), tr_axes(-1.7)
        x1, y1 = train(False, 5)
        c_tr = a1.plot_line_graph(x1, y1, line_color=TEXT, add_vertex_dots=False, stroke_width=4)
        l1 = T("before the blocker", 26, TEXT).next_to(a1, UP, buff=0.1).align_to(a1, LEFT)
        self.play(FadeIn(a1), FadeIn(l1), Create(c_tr["line_graph"]), run_time=1.6)

        self.at("generally reduced")
        x2, y2 = train(True, 3, gap=5.0)
        d_tr = a2.plot_line_graph(x2, y2, line_color=RED, add_vertex_dots=False, stroke_width=4)
        l2 = T("with the blocker: reduced, not eliminated", 26, RED).next_to(a2, UP, buff=0.1).align_to(a2, LEFT)
        self.play(FadeIn(a2), FadeIn(l2), Create(d_tr["line_graph"]), run_time=1.6)

        self.at("At 10 nanomolar")
        # right: one spike, before and after
        a3 = Axes(x_range=[0, 4, 1], y_range=[-0.3, 1.1, 1], x_length=5.4, y_length=4.2,
                  axis_config={"color": GREY, "stroke_width": 2, "include_ticks": False, "include_tip": False},
                  tips=False).move_to([3.6, -0.4, 0])
        fc, fd = spike_fn(False), spike_fn(True)
        s_c = a3.plot(lambda x: float(fc(x)), x_range=[0, 3, 0.01], color=TEXT, stroke_width=5, use_smoothing=False)
        s_d = a3.plot(lambda x: float(fd(x)), x_range=[0, 3, 0.01], color=RED, stroke_width=5, use_smoothing=False)
        t10 = T("at 10 nM", 26, GREY).next_to(a3, UP, buff=0.1)
        self.play(FadeIn(a3), FadeIn(t10), Create(s_c), run_time=0.6)
        self.play(Create(s_d), run_time=0.6)
        self.at("spike peak")
        pk = T("peak lowered", 24, RED).move_to(a3.c2p(2.9, 1.0))
        pa = arr(pk.get_left(), a3.c2p(0.9, 0.78), RED, 3, 0.18)
        self.play(FadeIn(pk), GrowArrow(pa), run_time=0.4)
        self.at("and the shoulder")
        sh = VGroup(T("shoulder", 24, RED), T("lowered", 24, RED)).arrange(DOWN, buff=0.05).move_to(a3.c2p(3.1, 0.62))
        sa = arr(sh.get_left(), a3.c2p(1.5, 0.27), RED, 3, 0.18)
        self.play(FadeIn(sh), GrowArrow(sa), run_time=0.4)
        self.at("largely spared")
        sp = VGroup(T("threshold and initial upstroke", 24, GREEN), T("largely spared", 24, GREEN)).arrange(DOWN, buff=0.05).move_to([3.6, -3.3, 0])
        ring = Ellipse(width=0.9, height=0.9, color=GREEN, stroke_width=4).move_to(a3.c2p(0.55, 0.15))
        self.play(Create(ring), FadeIn(sp), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        self.at("Why does the neuron still fire")
        base_y = -2.7
        H = 4.4
        bar = Rectangle(width=1.4, height=H, stroke_color=TEAL_C, stroke_width=3, fill_color=TEAL_C, fill_opacity=0.5)
        bar.move_to([-4.9, base_y + H / 2, 0])
        bll = VGroup(T("a neuron with a large", 24, TEAL_C), T("Nav1.8 current (sketch)", 24, TEAL_C)).arrange(DOWN, buff=0.08)
        bll.next_to(bar, UP, buff=0.25)
        self.play(FadeIn(bar, shift=UP * 0.2), FadeIn(bll), run_time=1.0)
        hd = T("authors' analysis: two possible reasons", 24, GREY).move_to([-2.2, 3.35, 0])
        self.at("two possible reasons")
        self.play(FadeIn(hd), run_time=0.4)
        self.at("even 99")
        blocked = Rectangle(width=1.4, height=H * 0.99, stroke_width=0, fill_color=RED, fill_opacity=0.6)
        blocked.move_to(bar.get_top() + DOWN * (H * 0.99) / 2)
        self.play(FadeIn(blocked), run_time=1.0)
        la = arr([-2.7, base_y + 0.9, 0], [-4.1, base_y + 0.12, 0], TEAL_C, 4, 0.18)
        lt = VGroup(T("1% left:", 26, TEAL_C), T("still nanoampere-level", 26, TEAL_C)).arrange(DOWN, buff=0.08)
        lt.move_to([-1.7, base_y + 1.5, 0])
        self.play(FadeIn(lt), GrowArrow(la), run_time=0.8)

        self.at("dominates the initial spikes")
        n7 = chan("Nav1.7", ORANGE, 3.4, 2.9, 36)
        n7l = VGroup(T("current dominates the", 26, ORANGE), T("initial spikes (these recordings)", 26, ORANGE)).arrange(DOWN, buff=0.06)
        n7l.next_to(n7, DOWN, buff=0.25)
        self.play(FadeIn(n7, scale=0.9), FadeIn(n7l), run_time=0.8)
        self.at("could also contribute")
        n7c = T("could also contribute to repetitive firing", 24, GREY).next_to(n7l, DOWN, buff=0.12)
        self.play(FadeIn(n7c), run_time=0.5)

        self.at("channel calculation")
        a = T("channel current left", 30, TEAL_C)
        ne = T("≠", 54, RED, weight=BOLD)
        b = T("neuron silent", 30, TEXT)
        col = VGroup(a, ne, b).arrange(DOWN, buff=0.15).move_to([3.4, -1.0, 0])
        self.play(FadeIn(a), run_time=0.4)
        self.play(FadeIn(b), run_time=0.4)
        self.play(FadeIn(ne, scale=1.4), run_time=0.4)

        self.at("certainly not a dose")
        dose = chip("a dose", GREY, 30).move_to([3.4, -3.0, 0])
        self.play(FadeIn(dose), run_time=0.4)
        self.play(Create(cross(dose, RED, 6)), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "A channel calculation is not neuronal silence."
