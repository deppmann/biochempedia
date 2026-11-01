"""Sensory coding: identical spikes, different meanings  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
All spike trains, bars and curves are drawn in this sketch from the lesson's own numbers or as
relative units; none is a recording.

COLOR MAP (one color per concept, whole video)
  YELLOW = the stimulus (load, light) and the stimulus axis
  TEAL   = the receptor potential (graded voltage)
  GREEN  = spikes, firing rate, outputs (the afferent's message)
  BLUE   = the steep flank / a highlighted comparison
  RED    = inhibition (lateral inhibition links, the cut)
  PURPLE = receptor proteins for smell (combination code)
  GREY   = structure, axes, neurons, de-emphasized
"""
import numpy as np
from scipy.interpolate import PchipInterpolator
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


def train(xs, y, h=0.7, color=GREEN, w=5):
    return VGroup(*[Line([x, y, 0], [x, y + h, 0], color=color, stroke_width=w) for x in xs])


def baseline(x0, x1, y, color=GREY):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2.5)


def spaced(n, x0, x1):
    return list(np.linspace(x0, x1, n))


def sketch_tag():
    return T("in this sketch", 22, GREY).to_corner(DL, buff=0.35)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.05
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.2, b - perp * 0.2, color=color, stroke_width=w + 1))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "Principles of sensory coding"
    TITLE = "Identical spikes, different meanings"


# ---------------------------------------------------------------------------------------------
class S01Load(SpokenScene):
    """a question box becomes two spike trains: heavier load, same-size spikes, shorter gaps."""

    def construct(self):
        ax0, ax1 = -2.6, 6.0
        yA, yB = 2.0, -1.9
        q = T("?", 120, YELLOW, weight=BOLD)
        qbox = RoundedRectangle(corner_radius=0.2, width=3.2, height=2.6, stroke_color=YELLOW, stroke_width=4,
                                fill_color=YELLOW, fill_opacity=0.1)
        qg = VGroup(qbox, q.move_to(qbox)).move_to([1.5, 0.0, 0])
        qlab = T("how hard was the touch?", 30, TEXT).next_to(qg, UP, buff=0.35)
        self.play(FadeIn(qg, scale=0.9), FadeIn(qlab), run_time=1.2)
        self.at("recorded one stretch receptor")
        musc = chip("frog muscle", GREY, 28).move_to([-4.8, 0.2, 0])
        self.play(FadeOut(qg), FadeOut(qlab), FadeIn(musc), run_time=0.7)
        rec = T("one stretch receptor", 26, BLUE).next_to(musc, DOWN, buff=0.3)
        self.play(FadeIn(rec), run_time=0.4)

        lightlab = chip("light load", YELLOW, 28).move_to([-4.8, yA, 0])
        heavylab = chip("heavy load", YELLOW, 28, pad=0.4).move_to([-4.8, yB, 0])
        trA = train(spaced(4, ax0 + 0.6, ax1 - 0.6), yA - 0.35, h=0.9)
        trB = train(spaced(10, ax0 + 0.3, ax1 - 0.3), yB - 0.35, h=0.9)
        bA, bB = baseline(ax0, ax1, yA - 0.35), baseline(ax0, ax1, yB - 0.35)
        self.at("loaded the muscle")
        self.play(FadeIn(lightlab), Create(bA), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in trA], lag_ratio=0.2), run_time=0.6)
        self.at("with weights")
        self.play(FadeIn(heavylab), Create(bB), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in trB], lag_ratio=0.1), run_time=0.8)
        tag = sketch_tag()
        self.add(tag)

        self.at("never grew bigger")
        top = DashedLine([ax0, yA + 0.55, 0], [ax1, yA + 0.55, 0], color=GREY, dash_length=0.12)
        topB = DashedLine([ax0, yB + 0.55, 0], [ax1, yB + 0.55, 0], color=GREY, dash_length=0.12)
        same = T("same size", 28, TEXT).move_to([ax1 - 1.0, 0.2, 0])
        self.play(Create(top), Create(topB), FadeIn(same), run_time=0.8)
        self.at("more often")
        xs = spaced(10, ax0 + 0.3, ax1 - 0.3)
        gap = DoubleArrow([xs[4], yB - 0.75, 0], [xs[5], yB - 0.75, 0], color=GREEN, stroke_width=4, tip_length=0.15, buff=0)
        glab = T("shorter gaps", 26, GREEN).next_to(gap, DOWN, buff=0.12)
        xsl = spaced(4, ax0 + 0.6, ax1 - 0.6)
        gapA = DoubleArrow([xsl[1], yA - 0.75, 0], [xsl[2], yA - 0.75, 0], color=GREEN, stroke_width=4, tip_length=0.15, buff=0)
        self.play(FadeOut(same), Create(gapA), Create(gap), FadeIn(glab), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Graded(SpokenScene):
    """stimulus -> graded receptor potential -> faster spikes, in three rows."""

    def construct(self):
        ys = [1.9, 0.1, -1.7]
        u = 0.95   # relative unit length
        heads = [T("stimulus", 28, YELLOW).move_to([-4.7, 3.05, 0]),
                 T("receptor potential", 28, TEAL).move_to([-0.8, 3.05, 0]),
                 T("spikes", 28, GREEN).move_to([4.1, 3.05, 0])]
        names = ["weak", "medium", "strong"]
        stim = VGroup(); lab = VGroup()
        for k, (y, n) in enumerate(zip(ys, names)):
            b = Rectangle(width=u * (k + 1), height=0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
            b.move_to([-6.2 + b.width / 2, y, 0])
            stim.add(b)
        self.at("starts with transduction")
        self.play(FadeIn(heads[0]), LaggedStart(*[GrowFromEdge(b, LEFT) for b in stim], lag_ratio=0.25), run_time=1.0)
        pot = VGroup()
        for k, y in enumerate(ys):
            b = Rectangle(width=u * (k + 1), height=0.6, stroke_width=0, fill_color=TEAL, fill_opacity=0.85)
            b.move_to([-2.2 + b.width / 2, y, 0])
            pot.add(b)
        arrs = VGroup(*[arr([-3.2, y, 0], [-2.35, y, 0], GREY) for y in ys])
        self.at("receptor potential")
        self.play(FadeIn(heads[1]), FadeIn(arrs), run_time=0.5)
        self.at("graded")
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in pot], lag_ratio=0.2), run_time=0.9)
        self.at("a stronger stimulus")
        self.play(Indicate(stim[2], color=YELLOW, scale_factor=1.08), Indicate(pot[2], color=TEAL, scale_factor=1.08), run_time=0.9)
        marks = VGroup(*[arr([0.8, y, 0], [1.65, y, 0], GREY) for y in ys])
        zone = T("spike initiating zone", 24, GREY).move_to([1.2, -2.45, 0])
        self.at("spike initiating zone")
        self.play(FadeIn(heads[2]), FadeIn(marks), FadeIn(zone), run_time=0.6)
        counts = [2, 4, 8]
        trs = VGroup(); bls = VGroup()
        for n, y in zip(counts, ys):
            bls.add(baseline(1.85, 6.2, y - 0.3))
            trs.add(train(spaced(n, 2.15, 6.0), y - 0.3, h=0.75))
        self.at("the faster the neuron fires")
        self.play(FadeIn(bls), run_time=0.3)
        self.play(*[LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in t], lag_ratio=0.2) for t in trs], run_time=1.8)
        tag = T("relative units, in this sketch", 22, GREY).to_corner(DL, buff=0.35)
        self.play(FadeIn(tag), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Time(SpokenScene):
    """a held step stimulus: rapidly adapting fires at onset (and offset), slowly adapting throughout."""

    def construct(self):
        x0, x1 = -5.8, 6.0
        on, off = -3.0, 3.2
        yS, yR, yL = 2.5, 0.3, -2.3
        ds = Line([x0, yS, 0], [on, yS, 0], color=YELLOW, stroke_width=6)
        up = Line([on, yS, 0], [on, yS + 0.7, 0], color=YELLOW, stroke_width=6)
        hold = Line([on, yS + 0.7, 0], [off, yS + 0.7, 0], color=YELLOW, stroke_width=6)
        dn = Line([off, yS + 0.7, 0], [off, yS, 0], color=YELLOW, stroke_width=6)
        ds2 = Line([off, yS, 0], [x1, yS, 0], color=YELLOW, stroke_width=6)
        slab = T("stimulus", 28, YELLOW).move_to([x0 + 0.9, yS + 0.7, 0])
        rl = T("rapidly adapting ending", 28, GREEN).move_to([-3.3, yR + 1.15, 0])
        sl = T("slowly adapting ending", 28, GREEN).move_to([-3.3, yL + 1.15, 0])
        bR, bL = baseline(x0, x1, yR), baseline(x0, x1, yL)
        self.at("differ in time")
        self.play(Create(VGroup(ds, up, hold, dn, ds2), lag_ratio=0.25), FadeIn(slab), run_time=1.5)
        self.at("rapidly adapting ending")
        self.play(FadeIn(rl), Create(bR), run_time=0.5)
        onx = [on + 0.15 + 0.2 * (1.25 ** k) * 0.5 * k for k in range(6)]
        onx = [on + 0.12, on + 0.4, on + 0.75, on + 1.2, on + 1.75]
        self.at("start of a held stimulus")
        t_on = train(onx, yR, h=0.75)
        self.play(LaggedStart(*[FadeIn(s) for s in t_on], lag_ratio=0.2), run_time=0.9)
        self.at("falls quiet")
        quiet = T("quiet", 26, GREY).move_to([0.1, yR + 0.45, 0])
        self.play(FadeIn(quiet), run_time=0.5)
        self.at("fire again when it is removed")
        offx = [off + 0.12, off + 0.42, off + 0.8]
        t_off = train(offx, yR, h=0.75)
        self.play(LaggedStart(*[FadeIn(s) for s in t_off], lag_ratio=0.25), run_time=0.7)
        pac = T("Pacinian corpuscle: vibration", 24, GREY).move_to([-1.7, yR - 0.5, 0])
        self.play(FadeIn(pac), run_time=0.4)
        self.at("slowly adapting ending")
        self.play(FadeIn(sl), Create(bL), run_time=0.5)
        self.at("keeps firing")
        lx = list(np.arange(on + 0.2, off - 0.05, 0.45))
        t_l = train(lx, yL, h=0.75)
        self.play(LaggedStart(*[FadeIn(s) for s in t_l], lag_ratio=0.08), run_time=2.0)
        mk = T("Merkel-cell afferent: steady indentation", 24, GREY).move_to([-0.4, yL - 0.5, 0])
        self.play(FadeIn(mk), run_time=0.4)
        self.at("one reports change")
        c1 = T("reports change", 28, GREEN, weight=BOLD).move_to([4.2, yR + 1.15, 0])
        self.play(FadeIn(c1), run_time=0.4)
        self.at("the stimulus itself")
        c2 = T("reports the stimulus", 28, GREEN, weight=BOLD).move_to([3.6, yL + 1.15, 0])
        self.play(FadeIn(c2), run_time=0.4)
        tag = sketch_tag()
        self.add(tag)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Flank(SpokenScene):
    """tuning curve through 50, 40, 20, 8 spikes/s; steep flank beats the peak for fine changes."""

    def construct(self):
        X0, X1 = -5.2, 5.4       # screen x for 0 and 45 degrees (axis end slightly beyond)
        Y0, Y1 = -2.7, 2.7       # screen y for 0 and 50 spikes/s

        def sx(d): return X0 + (X1 - X0) * d / 45.0
        def sy(r): return Y0 + (Y1 - Y0) * r / 50.0

        axx = Arrow([X0 - 0.3, Y0, 0], [X1 + 0.5, Y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18)
        axy = Arrow([X0 - 0.3, Y0, 0], [X0 - 0.3, Y1 + 0.55, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18)
        xl = T("angle (degrees)", 24, YELLOW).move_to([0.2, Y0 - 0.8, 0])
        yl = T("firing rate (spikes/s)", 24, GREEN).rotate(PI / 2).move_to([X0 - 0.85, 0, 0])
        ticks = VGroup(*[T(str(d), 24, GREY).move_to([sx(d), Y0 - 0.3, 0]) for d in (0, 15, 30, 45)])
        made = T("made-up neuron", 24, GREY).move_to([4.6, 3.3, 0])
        self.at("a tuning curve")
        self.play(Create(axx), Create(axy), FadeIn(xl), FadeIn(yl), FadeIn(ticks), run_time=1.2)
        pts = [(0, 50), (15, 40), (30, 20), (45, 8)]
        dots = [Dot([sx(d), sy(r), 0], radius=0.11, color=GREEN) for d, r in pts]
        vals = [T(str(r), 26, GREEN).next_to(dt, UP, buff=0.15) for dt, (d, r) in zip(dots, pts)]
        vals[0].next_to(dots[0], RIGHT, buff=0.35).shift(UP * 0.1)
        self.at("up neuron")
        self.play(FadeIn(made), run_time=0.4)
        self.at("spikes per second")
        self.play(FadeIn(dots[0]), FadeIn(vals[0]), run_time=0.4)
        f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
        ds = np.linspace(0, 45, 60)
        curve = VMobject(color=GREEN, stroke_width=5).set_points_smoothly([[sx(d), sy(float(f(d))), 0] for d in ds])
        self.at("degrees and")
        self.play(FadeIn(dots[3]), FadeIn(vals[3]), run_time=0.4)
        self.play(Create(curve), FadeIn(dots[1]), FadeIn(dots[2]), FadeIn(vals[1]), FadeIn(vals[2]), run_time=1.4)
        self.at("most useful at its peak")
        ring = Circle(radius=0.32, color=YELLOW, stroke_width=4).move_to(dots[0])
        qm = T("best here?", 28, YELLOW).move_to([sx(8), sy(50) + 0.5, 0])
        self.play(Create(ring), FadeIn(qm), run_time=0.6)
        self.at("often the reverse")
        self.play(FadeOut(ring), FadeOut(qm), run_time=0.4)
        self.at("steepest part")
        seg = VMobject(color=BLUE, stroke_width=9).set_points_smoothly(
            [[sx(d), sy(float(f(d))), 0] for d in np.linspace(15, 30, 20)])
        sl = T("steepest: 15 to 30 degrees", 26, BLUE).move_to([sx(26), sy(41), 0])
        self.play(Create(seg), FadeIn(sl), run_time=0.9)
        self.at("a small change there")
        dd = 4.0
        def window(d0, color):
            a = [sx(d0), sy(float(f(d0))), 0]; b = [sx(d0 + dd), sy(float(f(d0 + dd))), 0]
            h = Line([a[0], a[1], 0], [b[0], a[1], 0], color=color, stroke_width=4)
            v = Line([b[0], a[1], 0], [b[0], b[1], 0], color=color, stroke_width=6)
            return VGroup(h, v)
        w_flank = window(20, BLUE)
        w_peak = window(3, YELLOW)
        same = T("same small change in angle", 24, TEXT).move_to([sx(14), sy(50) + 0.5, 0])
        self.play(Create(w_peak), Create(w_flank), FadeIn(same), run_time=0.9)
        self.at("moves the rate more")
        self.play(Indicate(w_flank[1], color=BLUE, scale_factor=1.3), run_time=0.9)
        self.at("more noise")
        mk = Dot([sx(22.5), sy(float(f(22.5))), 0], radius=0.17, color=BLUE)
        nz = T("more noise: can shift", 26, RED).move_to([sx(34), sy(30), 0])
        self.play(FadeIn(mk), FadeIn(nz), run_time=0.5)
        self.at("back toward the peak")
        self.play(mk.animate.move_to([sx(11), sy(float(f(11))), 0]), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Edge(SpokenScene):
    """lateral inhibition: links, cut, then 10,10,10,20,20,20 -> 6,6,4,14,12,12."""

    def construct(self):
        xs = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]
        yU = 0.45
        units = VGroup(*[RoundedRectangle(corner_radius=0.12, width=1.1, height=0.7, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.25).move_to([x, yU, 0]) for x in xs])
        dots_l = T("...", 34, GREY).move_to([-6.25, yU, 0]); dots_r = T("...", 34, GREY).move_to([6.25, yU, 0])
        hdr = T("Limulus eye, one unit per receptor", 28, TEXT).move_to([0, 2.7, 0])
        self.at("can also suppress")
        self.play(FadeIn(hdr), LaggedStart(*[FadeIn(u, scale=0.9) for u in units], lag_ratio=0.12), FadeIn(dots_l), FadeIn(dots_r), run_time=1.3)
        links = VGroup()
        for i in range(5):
            a = [xs[i] + 0.55, yU - 0.12, 0]; b = [xs[i + 1] - 0.55, yU - 0.12, 0]
            links.add(inhib(b, a, RED, 4), inhib(a, b, RED, 4))
        self.at("suppressed its steady discharge")
        rec = RoundedRectangle(corner_radius=0.14, width=1.4, height=1.0, stroke_color=BLUE, stroke_width=4).move_to([xs[2], yU, 0])
        reclab = T("recorded unit", 26, BLUE).next_to(rec, UP, buff=0.2)
        lit = VGroup(*[Square(0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([x, yU + 1.6, 0]) for x in (xs[1], xs[2], xs[3])])
        self.play(Create(rec), FadeIn(reclab), FadeIn(lit), run_time=0.7)
        self.play(Create(links), run_time=0.9)
        self.at("abolished that inhibition")
        crosses = VGroup()
        for i in (1, 2):
            m = [(xs[i] + xs[i + 1]) / 2, yU - 0.12, 0]
            crosses.add(Line(np.array(m) + [-0.2, 0.2, 0], np.array(m) + [0.2, -0.2, 0], color=TEXT, stroke_width=6),
                        Line(np.array(m) + [-0.2, -0.2, 0], np.array(m) + [0.2, 0.2, 0], color=TEXT, stroke_width=6))
        cutl = T("connections to the recorded unit cut: no inhibition", 26, TEXT).move_to([0, -1.3, 0])
        self.play(Create(crosses), FadeIn(cutl), run_time=0.8)
        self.at("a simple sketch")
        self.play(FadeOut(crosses), FadeOut(cutl), FadeOut(links), FadeOut(rec), FadeOut(reclab), FadeOut(lit), FadeOut(hdr), run_time=0.6)
        self.play(*[u.animate.move_to([x, 0.75, 0]) for u, x in zip(units, xs)],
                  dots_l.animate.move_to([-6.25, 0.75, 0]), dots_r.animate.move_to([6.25, 0.75, 0]), run_time=0.7)
        yU = 0.75
        links2 = VGroup()
        for i in range(5):
            a = [xs[i] + 0.55, yU, 0]; b = [xs[i + 1] - 0.55, yU, 0]
            links2.add(inhib(b, a, RED, 3), inhib(a, b, RED, 3))
        formula = T("output = own light − 0.2 × (left + right)", 28, TEXT).move_to([0, -0.3, 0])
        exc = [10, 10, 10, 20, 20, 20]
        out = [6, 6, 4, 14, 12, 12]
        ex_bars = VGroup(); ex_lab = VGroup()
        base_e = 1.45
        for x, e in zip(xs, exc):
            b = Rectangle(width=1.1, height=0.095 * e, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85).move_to([x, base_e + 0.095 * e / 2, 0])
            ex_bars.add(b)
            ex_lab.add(T(str(e), 26, BG, weight=BOLD).move_to([x, base_e + 0.3, 0]))
        self.at("Each unit reports")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ex_bars], lag_ratio=0.1), FadeIn(ex_lab), Create(links2), run_time=1.4)
        self.play(FadeIn(formula), run_time=0.6)
        base_o = -3.15
        sc = 0.13
        o_bars = VGroup(); o_lab = VGroup()
        for x, o in zip(xs, out):
            b = Rectangle(width=1.1, height=sc * o, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([x, base_o + sc * o / 2, 0])
            o_bars.add(b)
            o_lab.add(T(str(o), 28, GREEN, weight=BOLD).move_to([x, base_o + sc * o + 0.3, 0]))
        bl = baseline(-5.8, 5.8, base_o)
        d6 = DashedLine([-5.8, base_o + sc * 6, 0], [5.8, base_o + sc * 6, 0], color=GREY, dash_length=0.12, stroke_width=2)
        d12 = DashedLine([-5.8, base_o + sc * 12, 0], [5.8, base_o + sc * 12, 0], color=GREY, dash_length=0.12, stroke_width=2)
        self.at("becomes")
        self.play(FadeIn(bl), FadeIn(d6), FadeIn(d12), run_time=0.4)
        for b, l in zip(o_bars, o_lab):
            self.play(GrowFromEdge(b, DOWN), FadeIn(l), run_time=0.45)
        self.at("edge is exaggerated")
        r1 = SurroundingRectangle(VGroup(o_bars[2], o_bars[3], o_lab[2], o_lab[3]), color=TEXT, buff=0.12, stroke_width=3)
        self.play(Create(r1), run_time=0.6)
        tag = sketch_tag()
        self.play(FadeIn(tag), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Code(SpokenScene):
    """rate = how strong, receptive field = where; labelled line vs population; smell combination; the rule."""

    def construct(self):
        c1 = chip("rate: how strong", GREEN, 36)
        c2 = chip("receptive field: where", YELLOW, 36)
        row = VGroup(c1, c2).arrange(RIGHT, buff=0.7).move_to([0, 0.5, 0])
        fit(row, max_w=12.3)
        self.at("Rate tells you")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.at("Receptive fields tell you")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        self.at("Quality is the harder")
        q = T("quality?", 44, TEXT, weight=BOLD).move_to([0, -1.5, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.at("line")
        self.play(FadeOut(row), FadeOut(q), run_time=0.5)

        # left pane: labelled line
        lt = T("labelled line", 30, GREEN, weight=BOLD).move_to([-3.3, 3.35, 0])
        fibre = Line([-5.3, 2.0, 0], [-1.4, 2.0, 0], color=GREY, stroke_width=6)
        soma = Circle(radius=0.38, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([-5.7, 2.0, 0])
        sp = train(spaced(6, -4.8, -1.8), 2.0, h=0.7, color=GREEN)
        sweet = chip("sweet", GREEN, 32).move_to([-3.3, 0.8, 0])
        one = T("one fibre, one meaning", 26, GREY).move_to([-3.3, 0.05, 0])
        self.play(FadeIn(lt), FadeIn(soma), Create(fibre), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s) for s in sp], lag_ratio=0.15), FadeIn(sweet), FadeIn(one), run_time=1.2)

        # right pane: population
        self.at("In a population code")
        pt = T("population code", 30, BLUE, weight=BOLD).move_to([3.3, 3.35, 0])
        hs = [1.3, 0.35, 0.9, 0.2, 1.5, 0.6]
        bars = VGroup(*[Rectangle(width=0.55, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([1.2 + 0.85 * k, 1.3 + h / 2, 0]) for k, h in enumerate(hs)])
        bbase = baseline(0.85, 6.1, 1.3)
        pat = T("pattern across many fibres", 26, GREY).move_to([3.5, 0.7, 0])
        self.play(FadeIn(pt), Create(bbase), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), run_time=1.4)
        self.play(FadeIn(pat), run_time=0.4)

        # bottom: smell
        self.at("In smell")
        st = T("smell: odorants and receptors", 28, PURPLE, weight=BOLD).move_to([-0.5, -0.75, 0])
        od = [chip("odorant A", YELLOW, 24).move_to([-3.4, -1.7, 0]), chip("odorant B", YELLOW, 24).move_to([-3.4, -2.5, 0])]
        rc = [chip(f"receptor {k + 1}", PURPLE, 22).move_to([2.4, y, 0]) for k, y in enumerate([-1.4, -2.2, -3.0])]
        links = []
        for a_, b_ in [(0, 0), (0, 1), (1, 1), (1, 2)]:
            links.append(Line(od[a_].get_right() + [0.05, 0, 0], rc[b_].get_left() + [-0.05, 0, 0], color=GREY, stroke_width=3))
        self.play(FadeIn(st), FadeIn(VGroup(*od)), FadeIn(VGroup(*rc)), run_time=0.8)
        self.at("several receptors")
        self.play(Create(links[0]), Create(links[1]), run_time=0.6)
        self.at("coded by a combination")
        self.play(Create(links[2]), Create(links[3]), run_time=0.6)
        self.at("still argue")
        vs = T("vs", 34, GREY).move_to([0, 2.3, 0])
        self.play(FadeIn(vs), run_time=0.4)
        self.at("Keep this")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        w1 = chip("rate", GREEN, 40); w2 = chip("source", YELLOW, 40); w3 = chip("pattern", BLUE, 40)
        rw = VGroup(w1, w2, w3).arrange(RIGHT, buff=0.6).move_to([0, 0.2, 0])
        txt = T("spikes look alike, so meaning lies in their", 34, TEXT).next_to(rw, UP, buff=0.7)
        self.play(FadeIn(txt), run_time=0.6)
        self.at("their rate")
        self.play(FadeIn(w1, shift=UP * 0.15), run_time=0.4)
        self.at("their source")
        self.play(FadeIn(w2, shift=UP * 0.15), run_time=0.4)
        self.at("their pattern")
        self.play(FadeIn(w3, shift=UP * 0.15), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "Spikes look alike; meaning lies in rate, source and pattern."
