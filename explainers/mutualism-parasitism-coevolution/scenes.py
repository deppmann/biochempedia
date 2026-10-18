"""Mutualism, parasitism and coevolution: a phase lag is a clue  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREEN  = algae, the prey (and "shown / supported")
  ORANGE = rotifers, the predator
  YELLOW = the delay / phase lag, the quantity being measured
  BLUE   = clonal diversity (one clone vs several clones)
  TEAL   = the experimental evidence (manipulation, trade-off)
  RED    = limit: "not proof", "?"
  GREY   = axes, vessel, structure, de-emphasized
All curves are drawn "in this sketch": cos curves with period 30 days, relative units.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PERIOD = 30.0
PEAK0 = 10.0
TMAX = 90.0


class Plot:
    """Axis frame mapping day t (0..90) to screen x; value to screen y."""

    def __init__(self, x0, x1, yc, amp):
        self.x0, self.x1, self.yc, self.amp = x0, x1, yc, amp
        self.y_ax = yc - amp - 0.3

    def X(self, t):
        return self.x0 + (self.x1 - self.x0) * t / TMAX

    def val(self, t, lag=0.0):
        return np.cos(2 * np.pi * (t - PEAK0 - lag) / PERIOD)

    def P(self, t, lag=0.0):
        return np.array([self.X(t), self.yc + self.amp * self.val(t, lag), 0])

    def curve(self, lag, color, t0=0.0, t1=TMAX):
        return ParametricFunction(lambda t: self.P(t, lag), t_range=[t0, max(t1, t0 + 0.05), 0.5],
                                  color=color, stroke_width=5)

    def axis(self, ticks=(0, 30, 60, 90), size=22):
        line = Line([self.x0, self.y_ax, 0], [self.x1, self.y_ax, 0], color=GREY, stroke_width=3)
        g = VGroup(line)
        for t in ticks:
            g.add(Line([self.X(t), self.y_ax, 0], [self.X(t), self.y_ax - 0.12, 0], color=GREY, stroke_width=3))
            g.add(M(str(t), size, GREY).move_to([self.X(t), self.y_ax - 0.42, 0]))
        g.add(T("days", size, GREY).next_to(line, RIGHT, buff=0.12))
        return g

    def bracket(self, ta, tb, y, color=YELLOW):
        a, b = [self.X(ta), y, 0], [self.X(tb), y, 0]
        return VGroup(Line(a, b, color=color, stroke_width=4),
                      Line([a[0], y - 0.12, 0], [a[0], y + 0.12, 0], color=color, stroke_width=4),
                      Line([b[0], y - 0.12, 0], [b[0], y + 0.12, 0], color=color, stroke_width=4))

    def dot(self, t, lag, color, r=0.1):
        return Dot(self.P(t, lag), radius=r, color=color)


def tag(text="in this sketch: relative units"):
    return T(text, 22, GREY).move_to([6.2 - 0, 3.3, 0], aligned_edge=RIGHT)


def legend(x=-6.2, y=3.3, horizontal=False):
    a = VGroup(Dot(radius=0.1, color=GREEN), T("algae (prey)", 24, GREEN)).arrange(RIGHT, buff=0.15)
    b = VGroup(Dot(radius=0.1, color=ORANGE), T("rotifers (predator)", 24, ORANGE)).arrange(RIGHT, buff=0.15)
    if horizontal:
        g = VGroup(a, b).arrange(RIGHT, buff=0.7)
        return g.move_to([x, y, 0], aligned_edge=LEFT)
    g = VGroup(a, b).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    return g.move_to([x, y, 0], aligned_edge=UL).shift(DOWN * 0.3)


def glyph(kind, color=GREEN, r=0.14):
    if kind == "c":
        return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    if kind == "s":
        return Square(side_length=r * 1.8, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    return Triangle(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8).scale(r * 1.3)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "Mutualism, parasitism and coevolution"
    TITLE = "A phase lag is a clue"


# ---------------------------------------------------------------------------------------------
class S01Vessel(SpokenScene):
    def construct(self):
        # chemostat vessel
        vx0, vx1, vy0, vy1 = -6.0, -2.9, -1.9, 2.3
        vessel = RoundedRectangle(corner_radius=0.35, width=vx1 - vx0, height=vy1 - vy0, stroke_color=GREY,
                                  stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([(vx0 + vx1) / 2, (vy0 + vy1) / 2, 0])
        vlabel = T("chemostat", 28, GREY).next_to(vessel, DOWN, buff=0.25)
        rng = np.random.default_rng(4)
        pts = []
        while len(pts) < 24:
            p = np.array([rng.uniform(vx0 + 0.4, vx1 - 0.4), rng.uniform(vy0 + 0.4, vy1 - 0.4)])
            if all(np.linalg.norm(p - q) > 0.5 for q in pts):
                pts.append(p)
        algae = [Dot([p[0], p[1], 0], radius=0.09, color=GREEN) for p in pts[:14]]
        rots = [Ellipse(width=0.34, height=0.2, stroke_width=2, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.9)
                .move_to([p[0], p[1], 0]) for p in pts[14:24]]
        plot = Plot(-1.9, 5.4, 0.0, 1.3)
        inflow = arrow([vx0 + 0.6, 3.25, 0], [vx0 + 0.6, vy1 + 0.02, 0], GREY, 4)
        inl = T("nutrient medium in", 22, GREY).next_to(inflow, RIGHT, buff=0.12).shift(UP * 0.2)
        outflow = arrow([vx1 - 0.6, vy0 - 0.02, 0], [vx1 - 0.6, vy0 - 0.65, 0], GREY, 4)
        outl = T("out", 22, GREY).next_to(outflow, RIGHT, buff=0.12)
        outl.shift(DOWN * 0.0)
        vlabel.next_to(vessel, DOWN, buff=0.75).align_to(vessel, LEFT)

        self.at("chemostat")
        self.play(FadeIn(vessel), FadeIn(vlabel), run_time=0.6)
        self.play(*[FadeIn(m, scale=0.5) for m in algae + rots], run_time=0.8)
        self.at("steady flow")
        self.play(GrowArrow(inflow), FadeIn(inl), run_time=0.5)
        self.at("matching flow out")
        self.play(GrowArrow(outflow), FadeIn(outl), run_time=0.5)

        # counts follow the cycle; curves trace
        tr = ValueTracker(0.0)
        ax = plot.axis(size=22)
        leg = legend(x=-1.9, y=-2.75, horizontal=True)
        sk = T("in this sketch: relative units", 22, GREY).move_to([5.9, 3.3, 0], aligned_edge=RIGHT)

        def n_alg():
            return int(round(7 + 6.5 * plot.val(tr.get_value())))

        def n_rot():
            return int(round(5 + 4.5 * plot.val(tr.get_value(), 7.5)))

        def upd_alg(m):
            n = n_alg()
            for i, d in enumerate(algae):
                d.set_opacity(1.0 if i < n else 0.0)

        def upd_rot(m):
            n = n_rot()
            for i, d in enumerate(rots):
                d.set_fill(opacity=0.9 if i < n else 0.0).set_stroke(opacity=1.0 if i < n else 0.0)

        ga, gr = VGroup(*algae), VGroup(*rots)
        ga.add_updater(upd_alg); gr.add_updater(upd_rot)
        prey_c = always_redraw(lambda: plot.curve(0.0, GREEN, 0, tr.get_value()))
        pred_c = always_redraw(lambda: plot.curve(7.5, ORANGE, 0, tr.get_value()))
        cls = T("classical sketch", 22, GREY).move_to([5.9, 2.9, 0], aligned_edge=RIGHT)
        self.at("both populations")
        self.play(FadeIn(ax), FadeIn(leg), FadeIn(sk), FadeIn(cls), run_time=0.4)
        self.add(prey_c, pred_c)
        dur = max(2.0, self.t_of("watch when") - self.elapsed() - 0.4)
        self.play(tr.animate.set_value(90.0), run_time=dur, rate_func=linear)
        ga.clear_updaters(); gr.clear_updaters()
        self.remove(prey_c, pred_c)
        prey_c = plot.curve(0.0, GREEN); pred_c = plot.curve(7.5, ORANGE)
        self.add(prey_c, pred_c)

        # the question
        p1, p2 = plot.dot(10, 0, GREEN, 0.12), plot.dot(17.5, 7.5, ORANGE, 0.12)
        br = plot.bracket(10, 17.5, plot.yc + plot.amp + 0.5)
        q = T("how long after?", 28, YELLOW).move_to([plot.X(13.75) + 0.6, plot.yc + plot.amp + 1.0, 0])
        self.at("watch when")
        self.play(FadeIn(p2, scale=2), run_time=0.4)
        self.at("after the algae")
        self.play(FadeIn(p1, scale=2), run_time=0.4)
        self.at("how long after")
        self.play(Create(br), FadeIn(q), run_time=0.6)
        self.at("a clue")
        self.play(Indicate(q, color=YELLOW), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def base_plot_group(plot, lag):
    ax = plot.axis()
    prey = plot.curve(0.0, GREEN)
    pred = plot.curve(lag, ORANGE)
    return ax, prey, pred


class S02Lag(SpokenScene):
    def construct(self):
        plot = Plot(-5.4, 5.4, -0.1, 1.4)
        ax, prey, pred = base_plot_group(plot, 7.5)
        leg = legend(x=-6.2, y=3.35, horizontal=True)
        sk = T("in this sketch: relative units", 22, GREY).move_to([6.2, 3.35, 0], aligned_edge=RIGHT)
        self.add(ax, prey, pred, leg, sk)
        self.wait(0.3)

        # four phases
        steps = [("prey rise", 4, 0.0, GREEN, "prey rise"), ("predators multiply", 13, 7.5, ORANGE, "predators feed and multiply"),
                 ("prey crash", 24, 0.0, GREEN, "prey crash"), ("predators starve", 31, 7.5, ORANGE, "predators starve")]
        labels = []
        xs = [-4.5, -1.5, 1.5, 4.5]
        lab_y = -2.9
        marker = Dot(plot.P(4, 0), radius=0.14, color=YELLOW)
        for (txt, t, lag, col, cue), x in zip(steps, xs):
            lab = T(txt, 24, col)
            lab.move_to([x, lab_y, 0])
            labels.append(lab)
        # each cue
        self.at("quarter of a cycle")
        ph = plot.bracket(10, 17.5, plot.yc + plot.amp + 0.5)
        phl = T("lag: about a quarter cycle", 26, YELLOW).move_to([plot.X(17.5) + 0.3, plot.yc + plot.amp + 0.5, 0], aligned_edge=LEFT)
        self.play(Create(ph), FadeIn(phl), run_time=0.8)
        self.at("rise")
        self.play(FadeIn(labels[0], shift=UP * 0.1), FadeIn(marker.move_to(plot.P(4, 0))), run_time=0.4)
        self.at("feed and multiply")
        self.play(FadeIn(labels[1], shift=UP * 0.1), marker.animate.move_to(plot.P(13, 7.5)).set_color(YELLOW), run_time=0.5)
        self.at("prey crash")
        self.play(FadeIn(labels[2], shift=UP * 0.1), marker.animate.move_to(plot.P(24, 0)), run_time=0.5)
        self.at("starve")
        self.play(FadeIn(labels[3], shift=UP * 0.1), marker.animate.move_to(plot.P(31, 7.5)), run_time=0.5)
        self.at("phase lag is")
        self.play(FadeOut(marker), *[l.animate.set_opacity(0.35) for l in labels],
                  ph.animate.set_stroke(width=6), run_time=0.5)
        # period bracket
        pb = plot.bracket(10, 40, plot.yc + plot.amp + 1.05, GREY)
        pl = T("period", 26, GREY).move_to([plot.X(25), plot.yc + plot.amp + 1.5, 0])
        self.at("period")
        self.play(Create(pb), FadeIn(pl), run_time=0.7)
        f = M("phase lag (cycles) = delay (days) / period (days)", 26, YELLOW)
        fit(f, 11.5)
        f.move_to([0, -3.4, 0])
        self.at("equals delay")
        self.play(FadeOut(VGroup(*labels)), run_time=0.3)
        f.move_to([0, -2.95, 0])
        self.play(Write(f), run_time=1.2)
        self.finish()


class S03Runa(SpokenScene):
    def construct(self):
        plot = Plot(-5.4, 5.4, -0.1, 1.4)
        ax, prey, pred = base_plot_group(plot, 7.5)
        leg = legend(x=-6.2, y=3.35, horizontal=True)
        sk = T("in this sketch: relative units", 22, GREY).move_to([6.2, 3.35, 0], aligned_edge=RIGHT)
        inv = T("invented data, run A", 26, YELLOW).move_to([6.2, 2.8, 0], aligned_edge=RIGHT)
        self.add(ax, prey, pred, leg, sk)
        self.at("invented example")
        self.play(FadeIn(inv), run_time=0.4)
        self.at("regular")
        self.play(Indicate(prey, color=GREEN, scale_factor=1.0), run_time=0.8)
        # prey peaks
        pdots = VGroup(*[plot.dot(t, 0, GREEN, 0.12) for t in (10, 40, 70)])
        plabs = VGroup(*[M(f"{t}", 24, GREEN).move_to(plot.P(t, 0) + UP * 0.35) for t in (10, 40, 70)])
        self.at("days")
        self.play(*[FadeIn(d, scale=2) for d in pdots], FadeIn(plabs), run_time=0.6)
        pb = plot.bracket(10, 40, plot.yc + plot.amp + 1.05, GREY)
        pl = M("period = 40 - 10 = 30 days", 24, GREY).move_to([plot.X(25), plot.yc + plot.amp + 1.5, 0])
        self.at("so the period")
        self.play(Create(pb), FadeIn(pl), run_time=0.7)
        rd = plot.dot(17.5, 7.5, ORANGE, 0.12)
        rl = M("17.5", 24, ORANGE).move_to(plot.P(17.5, 7.5) + UP * 0.35 + RIGHT * 0.45)
        self.at("run A")
        self.play(FadeIn(rd, scale=2), FadeIn(rl), run_time=0.5)
        lb = plot.bracket(10, 17.5, plot.yc + plot.amp + 0.7)
        self.at("after the prey")
        self.play(Create(lb), run_time=0.5)
        calc1 = M("delay = 17.5 - 10 = 7.5 days", 26, YELLOW).move_to([0, -2.9, 0])
        self.play(Write(calc1), run_time=0.9)
        calc2 = M("7.5 / 30 = 0.25 cycle", 30, YELLOW).move_to([0, -3.4, 0])
        self.at("a quarter cycle")
        self.play(Write(calc2), run_time=0.8)
        self.at("classical")
        self.play(Indicate(calc2, color=YELLOW), run_time=0.8)
        self.finish()


class S04Runb(SpokenScene):
    def construct(self):
        plot = Plot(-5.4, 5.4, -0.1, 1.4)
        ax, prey, pred = base_plot_group(plot, 7.5)
        leg = legend(x=-6.2, y=3.35, horizontal=True)
        sk = T("in this sketch: relative units", 22, GREY).move_to([6.2, 3.35, 0], aligned_edge=RIGHT)
        inv = T("invented data, run B", 26, YELLOW).move_to([6.2, 2.8, 0], aligned_edge=RIGHT)
        pdots = VGroup(*[plot.dot(t, 0, GREEN, 0.12) for t in (10, 40, 70)])
        plabs = VGroup(*[M(f"{t}", 24, GREEN).move_to(plot.P(t, 0) + UP * 0.35) for t in (10, 40, 70)])
        pb = plot.bracket(10, 40, plot.yc + plot.amp + 1.05, GREY)
        pl = M("period = 30 days", 24, GREY).move_to([plot.X(25), plot.yc + plot.amp + 1.5, 0])
        self.add(ax, prey, pred, leg, sk, pdots, plabs, pb, pl)
        self.wait(0.2)
        predB = plot.curve(15.0, ORANGE)
        self.at("run B")
        self.play(ReplacementTransform(pred, predB), FadeIn(inv), run_time=1.3)
        rd = plot.dot(25, 15, ORANGE, 0.12)
        rl = M("25", 24, ORANGE).move_to(plot.P(25, 15) + UP * 0.35 + RIGHT * 0.3)
        self.at("day")
        self.play(FadeIn(rd, scale=2), FadeIn(rl), run_time=0.5)
        lb = plot.bracket(10, 25, plot.yc + plot.amp + 0.7)
        self.at("after the prey")
        self.play(Create(lb), run_time=0.6)
        calc1 = M("delay = 25 - 10 = 15 days", 26, YELLOW).move_to([0, -2.9, 0])
        self.play(Write(calc1), run_time=0.9)
        calc2 = M("15 / 30 = 0.50 cycle", 30, YELLOW).move_to([0, -3.4, 0])
        self.at("one half cycle")
        self.play(Write(calc2), run_time=0.8)
        # predator peaks at prey troughs
        self.at("predator peaks")
        dl = VGroup()
        for t in (25, 55):
            dl.add(DashedLine([plot.X(t), plot.y_ax, 0], [plot.X(t), plot.yc + plot.amp + 0.1, 0], color=YELLOW,
                              stroke_width=3, dash_length=0.12))
        tdots = VGroup(*[plot.dot(t, 0, GREEN, 0.09) for t in (25, 55)])
        self.play(Create(dl), FadeIn(tdots), run_time=0.9)
        anti = T("antiphase", 34, YELLOW, weight=BOLD).move_to([plot.X(40), plot.yc - 0.15, 0])
        back = Rectangle(width=anti.width + 0.3, height=anti.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(anti)
        self.at("antiphase")
        self.play(FadeIn(back), FadeIn(anti), run_time=0.5)
        self.finish()


class S05Clones(SpokenScene):
    def construct(self):
        L = Plot(-5.6, -0.9, 0.2, 1.45)
        R = Plot(0.9, 5.6, 0.2, 1.45)
        axL, axR = L.axis(size=22), R.axis(size=22)
        axL[-1].set_opacity(0); axR[-1].set_opacity(0)
        preyL, predL = L.curve(0.0, GREEN), L.curve(7.5, ORANGE)
        preyR, predR = R.curve(0.0, GREEN), R.curve(15.0, ORANGE)
        sk = T("in this sketch: relative units", 22, GREY).move_to([6.2, 3.35, 0], aligned_edge=RIGHT)
        hL = VGroup(glyph("c"), T("one clone", 30, BLUE)).arrange(RIGHT, buff=0.2)
        hR = VGroup(glyph("c"), glyph("s"), glyph("t"), T("several clones", 30, BLUE)).arrange(RIGHT, buff=0.2)
        hL.move_to([(L.x0 + L.x1) / 2, 2.95, 0]); hR.move_to([(R.x0 + R.x1) / 2, 2.95, 0])
        invL = T("invented numbers", 22, YELLOW).move_to([(L.x0 + L.x1) / 2, 2.52, 0])
        invR = T("invented numbers", 22, YELLOW).move_to([(R.x0 + R.x1) / 2, 2.52, 0])
        capr = T("rotifer: Brachionus", 22, ORANGE).move_to([-4.3, 3.35, 0])
        cap = T("alga: Chlorella", 22, GREEN).move_to([-1.0, 3.35, 0])
        self.at("grew the rotifer")
        self.play(FadeIn(capr), run_time=0.4)
        self.at("on the alga")
        self.play(FadeIn(cap), run_time=0.4)
        self.at("one clone")
        self.play(FadeIn(hL, shift=UP * 0.1), run_time=0.5)
        self.at("or several")
        self.play(FadeIn(hR, shift=UP * 0.1), FadeIn(sk), run_time=0.5)
        self.at("Several can")
        self.play(FadeIn(axL), FadeIn(axR), FadeIn(invL), FadeIn(invR), run_time=0.4)
        self.at("single clone prey")
        self.play(Create(preyL), Create(predL), run_time=1.4)
        lbL = L.bracket(10, 17.5, L.yc + L.amp + 0.4)
        tL = T("Run A: lag 0.25 cycle, a quarter", 24, YELLOW).move_to([(L.x0 + L.x1) / 2, -2.5, 0])
        self.play(Create(lbL), FadeIn(tL), run_time=0.5)
        self.at("multiclonal prey")
        self.play(Create(preyR), Create(predR), run_time=1.4)
        lbR = R.bracket(10, 25, R.yc + R.amp + 0.4)
        tR = T("Run B: lag 0.50 cycle, antiphase", 24, YELLOW).move_to([(R.x0 + R.x1) / 2, -2.5, 0])
        self.play(Create(lbR), FadeIn(tR), run_time=0.5)
        self.at("did not share")
        nt = T("real treatments: different periods; here one period, for clean arithmetic", 22, GREY).move_to([0, -3.4, 0])
        fit(nt, 12)
        self.play(FadeIn(nt), run_time=0.5)
        self.at("run B resembles")
        res = T("resembles the evolving-prey runs", 24, BLUE).move_to([(R.x0 + R.x1) / 2, -2.9, 0])
        bx = SurroundingRectangle(VGroup(hR, preyR, predR, tR, res), color=BLUE, buff=0.1, stroke_width=3, corner_radius=0.1)
        self.play(Create(bx), FadeIn(res), run_time=0.6)
        self.finish()


class S06Proof(SpokenScene):
    def construct(self):
        lag = chip("long lag: 0.50 cycle", YELLOW, 28).move_to([-4.0, 2.6, 0])
        tgt = chip("prey evolution?", GREY, 34).move_to([-0.1, 0.9, 0])
        e1 = chip("clonal diversity changed", TEAL, 28).move_to([3.9, 2.6, 0])
        e2t = T("resisting grazing:\npoorer at competing\nfor nutrients", 26, TEAL)
        e2 = VGroup(RoundedRectangle(corner_radius=0.14, width=e2t.width + 0.44, height=e2t.height + 0.44,
                                     stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.16), e2t)
        e2.move_to([4.2, 0.55, 0]); e2t.move_to(e2[0])
        a_lag = DashedLine(lag.get_bottom() + DOWN * 0.05, tgt.get_left() + LEFT * 0.05, color=RED, stroke_width=5, dash_length=0.18)
        nope = T("alone: not proof", 28, RED).move_to([-5.0, 1.45, 0])
        other = T("a long lag could have other causes", 24, RED).move_to([-4.0, -0.05, 0])
        self.at("lag alone")
        self.play(FadeIn(lag, shift=DOWN * 0.1), FadeIn(tgt), run_time=0.6)
        self.play(Create(a_lag), FadeIn(nope), run_time=0.7)
        self.at("other causes")
        self.play(FadeIn(other), run_time=0.5)
        ar1 = arrow(e1.get_left() + LEFT * 0.02, tgt.get_top() + RIGHT * 0.7 + UP * 0.02, TEAL, 5)
        ar2 = arrow(e2.get_left(), tgt.get_right(), TEAL, 5)
        self.at("changing the clonal diversity")
        self.play(FadeIn(e1, shift=DOWN * 0.1), GrowArrow(ar1), run_time=0.7)
        self.at("measured trade")
        self.play(FadeIn(e2, shift=DOWN * 0.1), GrowArrow(ar2), run_time=0.7)
        shown = chip("prey evolution: shown", GREEN, 30).move_to([-3.1, -1.7, 0])
        notp = chip("predator evolution: not investigated", GREY, 26).move_to([3.3, -1.7, 0])
        tgt2 = chip("prey evolution", GREEN, 34).move_to(tgt.get_center())
        self.at("study showed")
        self.play(ReplacementTransform(tgt, tgt2), run_time=0.6)
        self.play(FadeIn(shown, shift=UP * 0.1), run_time=0.5)
        self.at("did not investigate")
        self.play(FadeIn(notp, shift=UP * 0.1), run_time=0.5)
        rule = T("A phase lag is a pattern. The causal case comes from changing the prey's variation.", 28, YELLOW)
        fit(rule, 12.2)
        rule.move_to([0, -3.1, 0])
        self.at("keep this rule")
        self.play(Write(rule), run_time=1.5)
        self.finish()


class S07End(EndCard):
    LINE = "A phase lag is a pattern; the causal case comes from manipulation."
