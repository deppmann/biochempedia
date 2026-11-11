"""How Far Is Too Far? (Genetics: probability and crosses, chapter 2).

Same world as chapter 1.
COLOUR MAP (whole film, identical to chapter 1)
  GOLD   = round yellow seeds       GREEN = round green seeds
  ORANGE = wrinkled yellow seeds    TEAL  = wrinkled green seeds
  WHITE  = expected counts (dashed ghost lines), numbers, p-values
  GREY   = anything made by chance in a simulation
  BLUE   = chromosomes (not needed in this chapter)

Everything plotted here is computed: misses and whiskers from Mendel's counts and the multinomial
variance, the pile from 10,000 simulated crosses of 556 seeds under 9:3:3:1.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F28C38"
CLS = [GOLD, GREEN, ORANGE, TEAL]
PALEGREY = "#9AA3B2"
LINEC = "#C9CFDA"
WHISK = "#DDE3EE"
REDGREY = "#B5605E"

COLS = [-4.5, -1.5, 1.5, 4.5]
BASE = -2.4
SC = 0.0135
BARW = 1.7
MENDEL = [315, 108, 101, 32]
EXPECT = [312.75, 104.25, 104.25, 34.75]
PROBS = np.array([9, 3, 3, 1]) / 16
EXP_ARR = 556 * PROBS
GAPS = [o - e for o, e in zip(MENDEL, EXPECT)]
GLAB = ["+2.25", "+3.75", "−3.25", "−2.75"]
SDS = [math.sqrt(556 * p * (1 - p)) for p in PROBS]          # 11.7, 9.2, 9.2, 5.7
SDL = ["11.7", "9.2", "9.2", "5.7"]
TERMS = [g * g / e for g, e in zip(GAPS, EXPECT)]             # 0.016, 0.135, 0.101, 0.218
TERML = ["0.016", "0.135", "0.101", "0.218"]
EXPS = ["312.75", "104.25", "104.25", "34.75"]
CHI_M = sum(TERMS)                                            # 0.470

# "miss world": the ghost lines level to one zero line, misses drawn at a zoom of 0.25 per seed
Y0 = 0.1
ZS = 0.22

# chance world
RUNS = np.random.default_rng(21).multinomial(556, PROBS, size=400)


def chi(r):
    return float(((np.asarray(r) - EXP_ARR) ** 2 / EXP_ARR).sum())


C10 = np.array([chi(r) for r in np.random.default_rng(3).multinomial(556, PROBS, size=10000)])
EDGES = np.arange(0, 12.0001, 0.25)
HC, _ = np.histogram(C10, EDGES)
AX_Y = -2.45
HS = 4.0 / HC.max()
MEAN10 = float(C10.mean())
TAIL_FRAC = float((C10 > 7.81).mean())
FAR_FRAC = float((C10 > CHI_M).mean())


def X(v):
    return -6.0 + v


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def seed(i, r=0.25):
    col = CLS[i]
    if i < 2:
        m = Circle(radius=r)
    else:
        pts = [[r * (1 + 0.2 * math.sin(7 * t)) * math.cos(t), r * (1 + 0.2 * math.sin(7 * t)) * math.sin(t), 0]
               for t in np.linspace(0, TAU, 70, endpoint=False)]
        m = VMobject()
        m.set_points_smoothly(pts + [pts[0]])
    m.set_fill(col, 0.95).set_stroke(col, 2)
    return m


def mkbar(i, v, fill=0.6):
    r = Rectangle(width=BARW, height=1.0)
    r.set_fill(CLS[i], fill).set_stroke(CLS[i], 4)
    h = max(v * SC, 0.02)
    r.stretch_to_fit_height(h)
    r.move_to([COLS[i], BASE + h / 2, 0])
    return r


def set_heights(bars, vals):
    for r, x, v in zip(bars, COLS, vals):
        h = max(v * SC, 0.02)
        r.stretch_to_fit_height(h)
        r.move_to([x, BASE + h / 2, 0])


def ghost_lines(w=0.95):
    return VGroup(*[DashedLine([x - w, BASE + e * SC, 0], [x + w, BASE + e * SC, 0], color=TEXT, stroke_width=4)
                    for x, e in zip(COLS, EXPECT)])


def zero_lines(w=0.95):
    return VGroup(*[DashedLine([x - w, Y0, 0], [x + w, Y0, 0], color=TEXT, stroke_width=4) for x in COLS])


def tick(i, v, w=1.5, color=PALEGREY, sw=4, op=0.8):
    y = BASE + v * SC
    return Line([COLS[i] - w / 2, y, 0], [COLS[i] + w / 2, y, 0], color=color, stroke_width=sw).set_opacity(op)


def clouds(k_from, k_to):
    g = VGroup()
    for k in range(k_from, k_to):
        for i in range(4):
            g.add(tick(i, RUNS[k][i]))
    return g


def vsign(g):
    return 1 if g > 0 else -1


def miss_dots():
    return VGroup(*[Dot(radius=0.14, color=CLS[i]).move_to([COLS[i], Y0 + GAPS[i] * ZS, 0]) for i in range(4)])


def miss_arrows():
    out = VGroup()
    for i in range(4):
        s = vsign(GAPS[i])
        col = TEXT if s > 0 else PALEGREY
        a = Arrow([COLS[i], Y0, 0], [COLS[i], Y0 + GAPS[i] * ZS - s * 0.14, 0], buff=0, color=col, stroke_width=8,
                  max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)
        out.add(a)
    return out


def miss_labels():
    out = VGroup()
    for i in range(4):
        s = vsign(GAPS[i])
        col = TEXT if s > 0 else PALEGREY
        out.add(M(GLAB[i], 30, col).move_to([COLS[i] + 0.0, Y0 + GAPS[i] * ZS + s * 0.45, 0]))
    return out


def whiskers():
    out = VGroup()
    for i in range(4):
        h = SDS[i] * ZS
        x = COLS[i]
        out.add(VGroup(Line([x, Y0 - h, 0], [x, Y0 + h, 0], color=WHISK, stroke_width=7),
                       Line([x - 0.3, Y0 + h, 0], [x + 0.3, Y0 + h, 0], color=WHISK, stroke_width=7),
                       Line([x - 0.3, Y0 - h, 0], [x + 0.3, Y0 - h, 0], color=WHISK, stroke_width=7)))
    return out


def whisker_labels():
    return VGroup(*[M(SDL[i], 30, WHISK).move_to([COLS[i] + 0.35, Y0 + SDS[i] * ZS + 0.05, 0], aligned_edge=LEFT)
                    for i in range(4)])


def formula_parts():
    parts = [M("Σ", 54, TEXT), M("(O − E)²", 54, TEXT), M("/ E", 54, TEXT)]
    g = VGroup(*parts).arrange(RIGHT, buff=0.3).move_to([2.2, 3.0, 0])
    return parts, g


def term_row(y=-1.9, plus=True):
    g = VGroup()
    for i in range(4):
        g.add(M(TERML[i], 40, CLS[i]).move_to([COLS[i], y, 0]))
    if plus:
        for x in (-3.0, 0.0, 3.0):
            g.add(M("+", 40, TEXT).move_to([x, y, 0]))
    return g


# ---- chance world: axis, histogram, markers ------------------------------------------------------
def axis():
    line = Line([-6, AX_Y, 0], [6, AX_Y, 0], color=LINEC, stroke_width=4)
    ticks = VGroup(*[Line([X(v), AX_Y, 0], [X(v), AX_Y - 0.1, 0], color=LINEC, stroke_width=3) for v in range(13)])
    labs = VGroup(*[M(str(v), 28, TEXT).move_to([X(v), -2.88, 0]) for v in range(0, 13, 2)])
    name = T("χ² score", 28, TEXT).move_to([6.5, -3.45, 0], aligned_edge=RIGHT)
    return VGroup(line, ticks, labs, name)


def tri(x, color=TEXT, op=1.0, big=False):
    h = 0.5 if big else 0.4
    w = 0.3 if big else 0.2
    t = Polygon([x, AX_Y - 0.08, 0], [x - w, AX_Y - 0.08 - h, 0], [x + w, AX_Y - 0.08 - h, 0])
    t.set_fill(color, op).set_stroke(color, 2).set_opacity(op)
    return t


def hist_rects(frac=1.0, color=PALEGREY, op=0.65):
    g = VGroup()
    for k, c in enumerate(HC):
        h = max(c * HS * frac, 0.005)
        r = Rectangle(width=0.25, height=h).set_fill(color, op).set_stroke(BG, 1.5)
        r.move_to([X(EDGES[k] + 0.125), AX_Y + h / 2, 0])
        g.add(r)
    return g


def set_hist(g, frac):
    for k, r in enumerate(g):
        h = max(HC[k] * HS * frac, 0.005)
        r.stretch_to_fit_height(h)
        r.move_to([X(EDGES[k] + 0.125), AX_Y + h / 2, 0])


def region(lo, color, op=0.75, hi=12.0):
    g = VGroup()
    for k, c in enumerate(HC):
        a, b = max(EDGES[k], lo), min(EDGES[k + 1], hi)
        if b - a <= 1e-6:
            continue
        h = max(c * HS, 0.005)
        r = Rectangle(width=b - a, height=h).set_fill(color, op).set_stroke(width=0)
        r.move_to([X((a + b) / 2), AX_Y + h / 2, 0])
        g.add(r)
    return g


def top_of(v):
    k = min(int(v / 0.25), len(HC) - 1)
    return AX_Y + HC[k] * HS


def stack_dots(vals, color=PALEGREY, rad=0.12):
    cnt = {}
    out = []
    for v in vals:
        b = int(min(v, 11.99) / 0.25)
        n = cnt.get(b, 0)
        cnt[b] = n + 1
        out.append(np.array([X((b + 0.5) * 0.25), AX_Y + rad + 0.02 + n * 0.26, 0.0]))
    return out


# ---- simulation panel ------------------------------------------------------------------------------
SM = 0.0095
PX = [-5.0, -3.3, -1.6, 0.1]
PB = 0.0
SCORE_POS = np.array([3.6, 1.2, 0.0])


class Panel:
    """Four grey bars that run through simulated crosses (real multinomial draws), with the run's score beside them."""

    def __init__(self, tr, runs=RUNS, start=0, show_ghost=True, smooth=True):
        self.tr, self.runs, self.start, self.smooth = tr, runs, start, smooth
        self.bars = VGroup(*[Rectangle(width=1.3, height=1.0).set_fill(PALEGREY, 0.45).set_stroke(c, 4) for c in CLS])
        self.ghosts = VGroup(*[DashedLine([x - 0.75, PB + e * SM, 0], [x + 0.75, PB + e * SM, 0], color=TEXT, stroke_width=3)
                               for x, e in zip(PX, EXPECT)])
        self.score = M("", 60, PALEGREY)
        self.run = T("", 30, PALEGREY)
        self._last = None
        self.group = VGroup(self.bars, self.ghosts, self.score, self.run)
        self.group.add_updater(self._upd)
        self._upd(self.group)

    def at(self, u):
        k = int(u)
        k = max(0, min(k, len(self.runs) - 2))
        e = ease((u - int(u)) / 0.6) if self.smooth else (1.0 if u - int(u) > 0.5 else 0.0)
        a, b = self.runs[k], self.runs[k + 1]
        return k, e, [(1 - e) * p + e * q for p, q in zip(a, b)]

    def _upd(self, m, dt=0):
        u = self.tr.get_value() + self.start
        k, e, vals = self.at(u)
        for r, x, v in zip(self.bars, PX, vals):
            h = max(v * SM, 0.02)
            r.stretch_to_fit_height(h)
            r.move_to([x, PB + h / 2, 0])
        shown = k + (1 if e > 0.5 else 0)
        if shown != self._last:
            self._last = shown
            self.score.become(M(f"χ² = {chi(self.runs[shown]):.1f}", 60, PALEGREY).move_to(SCORE_POS))
            self.run.become(T(f"run {shown + 1}", 30, PALEGREY).move_to(SCORE_POS + np.array([0, -0.85, 0])))

    def freeze(self):
        self.group.clear_updaters()


def sim_label():
    return T("simulation: 9:3:3:1 true, 556 seeds per run", 26, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)


def mendel_marker(dim=False):
    t = tri(X(CHI_M), TEXT, 0.35 if dim else 1.0)
    lab = T("Mendel 0.47", 28, TEXT).move_to([-6.4, -3.45, 0], aligned_edge=LEFT)
    if dim:
        t.set_fill(opacity=0).set_stroke(TEXT, 3, opacity=0.6)
        lab.set_opacity(0.55)
    return VGroup(t, lab)


# ---- scenes -----------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Probability, Crosses and the Chi-Square Test"
    TITLE = "How Far Is Too Far?"


class S01Hook(SpokenScene):
    def construct(self):
        tr = ValueTracker(0)
        bars = VGroup(*[mkbar(i, 0.0, 0.5) for i in range(4)])
        bars.add_updater(lambda m: set_heights(m, [v * tr.get_value() for v in MENDEL]))
        gl = ghost_lines()
        gl.set_opacity(0)
        self.add(bars, gl)
        self.play(tr.animate.set_value(1.0), run_time=1.8, rate_func=smooth)
        bars.clear_updaters()
        self.play(gl.animate.set_opacity(1), run_time=0.8)
        # a ruler slides in and keeps hovering over the bars
        w = 4.6
        body = RoundedRectangle(corner_radius=0.06, width=w, height=0.7, fill_color="#E8D9C0", fill_opacity=0.92,
                                stroke_color="#F4EBDD", stroke_width=3)
        tks = VGroup(*[Line([x, 0.35, 0], [x, 0.35 - (0.32 if i % 5 == 0 else 0.18), 0], color=BG, stroke_width=3)
                       for i, x in enumerate(np.linspace(-w / 2 + 0.2, w / 2 - 0.2, 24))])
        rul = VGroup(body, tks).move_to([9.5, 2.95, 0])
        self.add(rul)
        self.play(rul.animate.move_to([-1.5, 2.95, 0]), run_time=1.6, rate_func=smooth)
        rul.t = 0.0

        def drift(m, dt):
            m.t += dt
            m.move_to([-1.5 + 3.0 * math.sin(0.55 * m.t), 2.95 + 0.12 * math.sin(1.7 * m.t), 0])
        rul.add_updater(drift)
        self.at("chapter 1 showed")
        cl = clouds(0, 30)
        self.play(LaggedStart(*[FadeIn(c) for c in cl], lag_ratio=0.02), run_time=3.0)
        self.at("now we measure")
        self.play(Indicate(gl, color=TEXT, scale_factor=1.05), run_time=1.5)
        self.finish()


class S02Misses(SpokenScene):
    def construct(self):
        bars = VGroup(*[mkbar(i, v, 0.5) for i, v in enumerate(MENDEL)])
        gl = ghost_lines()
        row = VGroup()
        for i in range(4):
            row.add(M(f"{MENDEL[i]} vs {EXPECT[i]:g}", 24, CLS[i]).move_to([COLS[i], -3.3, 0]))
        self.add(bars, gl, row)
        dots = VGroup(*[Dot(radius=0.14, color=CLS[i]).move_to([COLS[i], BASE + MENDEL[i] * SC, 0]) for i in range(4)])
        self.add(dots)
        self.play(Indicate(dots, color=TEXT, scale_factor=1.5), run_time=1.4)
        self.at("every class missed")
        zl = T("zoomed in: each miss, in seeds", 28, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)
        self.play(FadeOut(bars), FadeOut(row),
                  *[gl[i].animate.move_to([COLS[i], Y0, 0]) for i in range(4)],
                  *[dots[i].animate.move_to([COLS[i], Y0 + GAPS[i] * ZS, 0]) for i in range(4)],
                  FadeIn(zl), run_time=1.4)
        arr = miss_arrows()
        lab = miss_labels()
        self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.2), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1 * vsign(g)) for l, g in zip(lab, GAPS)], lag_ratio=0.2), run_time=0.9)
        spot = Rectangle(width=2.4, height=6.6, fill_color=TEXT, fill_opacity=0.10, stroke_width=0).move_to([COLS[0], 0, 0])
        spot.set_z_index(-5)
        spot.t = 0.0

        def sweep(m, dt):
            m.t += dt
            u = (m.t / 1.1) % 4.0
            k = int(u)
            e = ease((u - k) / 0.4)
            m.move_to([(1 - e) * COLS[k] + e * COLS[(k + 1) % 4] if k < 3 else COLS[3] + e * (COLS[0] - COLS[3]), 0, 0])
        spot.add_updater(sweep)
        self.add(spot)
        self.at("some came in high")
        self.play(Indicate(VGroup(lab[0], lab[1]), color=TEXT, scale_factor=1.3), run_time=1.0)
        self.at("some came in low")
        self.play(Indicate(VGroup(lab[2], lab[3]), color=PALEGREY, scale_factor=1.3), run_time=1.0)
        self.at("is that close enough")
        q = T("?", 120, TEXT, weight=BOLD).move_to([0, 2.9, 0])
        q.set_opacity(0)
        self.play(FadeIn(q, shift=UP * 0.2, scale=0.6), q.animate.set_opacity(1), run_time=0.8)
        self.play(Indicate(q, color=TEXT, scale_factor=1.25), run_time=1.0)
        self.finish()


def miss_world(scene, labels=True, label_text="zoomed in: each miss, in seeds"):
    gl = zero_lines()
    dots = miss_dots()
    arr = miss_arrows()
    lab = miss_labels()
    zl = T(label_text, 28, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)
    scene.add(gl, arr, dots, zl)
    if labels:
        scene.add(lab)
    return gl, dots, arr, lab, zl


class S03Scale(SpokenScene):
    def construct(self):
        gl, dots, arr, lab, zl = miss_world(self)
        self.at("a miss of a few seeds")
        self.play(Indicate(lab, color=TEXT, scale_factor=1.25), run_time=1.2)
        self.at("that depends on the class")
        self.play(LaggedStart(*[Indicate(d, color=CLS[i], scale_factor=1.9) for i, d in enumerate(dots)], lag_ratio=0.35),
                  run_time=2.2)
        self.at("in this cross")
        wk = whiskers()
        wl = whisker_labels()
        zl2 = T("whisker = chance's typical miss", 28, WHISK).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)
        self.play(FadeOut(lab), FadeOut(zl), run_time=0.4)
        self.play(FadeIn(zl2), LaggedStart(*[Create(w) for w in wk], lag_ratio=0.15), run_time=1.2)
        # grey dots: the misses of real simulated crosses (chance), wandering inside the whiskers
        samp = VGroup(*[Dot(radius=0.1, color=PALEGREY) for _ in range(4)])
        samp.t = 0.0

        def wander(m, dt):
            m.t += dt
            u = m.t / 0.45
            k = int(u) % 300
            e = ease((u - int(u)) / 0.5)
            for i, d in enumerate(m):
                a = (RUNS[k][i] - EXP_ARR[i]) * ZS
                b = (RUNS[k + 1][i] - EXP_ARR[i]) * ZS
                d.move_to([COLS[i] - 0.55, Y0 + (1 - e) * a + e * b, 0])
        samp.add_updater(wander)
        wander(samp, 0)
        self.add(samp)
        self.at("chance moves a bigger pile")
        self.play(LaggedStart(*[FadeIn(l) for l in wl], lag_ratio=0.25), run_time=1.2)
        self.at("the round yellow pile")
        self.play(Indicate(wk[0], color=GOLD, scale_factor=1.15), Indicate(wl[0], color=GOLD, scale_factor=1.2), run_time=1.6)
        self.at("the small wrinkled green pile")
        self.play(Indicate(wk[3], color=TEAL, scale_factor=1.15), Indicate(wl[3], color=TEAL, scale_factor=1.2), run_time=1.6)
        self.at("so judge each miss")
        self.play(LaggedStart(*[Indicate(VGroup(dots[i], arr[i], wk[i]), color=CLS[i], scale_factor=1.12) for i in range(4)],
                              lag_ratio=0.4), run_time=2.6)
        self.finish()


class S04Score(SpokenScene):
    def construct(self):
        gl, dots, arr, lab, zl = miss_world(self, labels=False, label_text="")
        self.remove(zl)
        tag = T("Karl Pearson, 1900", 28, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)
        parts, fg = formula_parts()
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.8)
        self.at("for each class")
        self.play(Indicate(dots, color=TEXT, scale_factor=1.6), run_time=0.7)
        self.at("square the miss")
        sq = VGroup()
        for i in range(4):
            s = abs(GAPS[i]) * ZS
            sq.add(Square(side_length=s).set_fill(CLS[i], 0.55).set_stroke(CLS[i], 4).move_to([COLS[i], -1.9, 0]))
        self.play(FadeIn(parts[1], shift=DOWN * 0.2),
                  *[TransformFromCopy(arr[i], sq[i]) for i in range(4)], run_time=1.0)
        self.at("high and low both count")
        self.play(LaggedStart(*[Indicate(sq[i], color=TEXT, scale_factor=1.25) for i in range(4)], lag_ratio=0.3), run_time=1.8)
        self.at("divide by the expected count")
        el = VGroup(*[M("÷ " + EXPS[i], 28, CLS[i]).move_to([COLS[i], -2.8, 0]) for i in range(4)])
        self.play(FadeIn(parts[2], shift=DOWN * 0.2), LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in el], lag_ratio=0.2),
                  run_time=1.4)
        self.at("that roughly puts each miss")
        tr_ = term_row(-1.9, plus=False)
        self.play(*[ReplacementTransform(sq[i], tr_[i]) for i in range(4)], FadeOut(el), run_time=1.6)
        self.at("then add the classes")
        plus = VGroup(*[M("+", 40, TEXT).move_to([x, -1.9, 0]) for x in (-3.0, 0.0, 3.0)])
        self.play(FadeIn(parts[0], shift=RIGHT * 0.2), LaggedStart(*[FadeIn(p, scale=0.6) for p in plus], lag_ratio=0.25),
                  run_time=1.2)
        self.play(Indicate(fg, color=TEXT, scale_factor=1.06), run_time=1.0)
        self.finish()


class S05Value(SpokenScene):
    def construct(self):
        parts, fg = formula_parts()
        row = term_row(-1.9, plus=True)
        self.add(fg, row)
        self.at("called chi square")
        big = M(f"χ² = {CHI_M:.2f}", 96, TEXT).move_to([0, 0.7, 0])
        self.play(ReplacementTransform(row, big), run_time=1.6)
        ax = axis()
        self.at("zero means a perfect match")
        self.play(FadeOut(fg), big.animate.scale(0.7).move_to([0, 1.2, 0]), Create(ax[0]), FadeIn(ax[1]), FadeIn(ax[2]), FadeIn(ax[3]),
                  run_time=1.2)
        pm = T("0 = perfect match", 30, TEXT).move_to([-6.4, -1.45, 0], aligned_edge=LEFT)
        self.play(FadeIn(pm, shift=DOWN * 0.1), run_time=0.6)
        self.at("and bigger means further off")
        ar = Arrow([-1.5, -1.45, 0], [5.0, -1.45, 0], buff=0, color=TEXT, stroke_width=8)
        bl = T("bigger = further off", 30, TEXT).move_to([1.75, -0.95, 0])
        self.play(GrowArrow(ar), FadeIn(bl, shift=UP * 0.1), run_time=1.4)
        self.at("mendel seeds score")
        mm = mendel_marker()
        self.play(FadeIn(mm[0], shift=DOWN * 0.5), FadeIn(mm[1]), run_time=0.9)
        self.play(Indicate(mm, color=TEXT, scale_factor=1.15), Indicate(big, color=TEXT, scale_factor=1.1), run_time=1.0)
        self.finish()


class S06Question(SpokenScene):
    def construct(self):
        ax = axis()
        mm = mendel_marker(dim=True)
        big = M(f"χ² = {CHI_M:.2f}", 67, TEXT).move_to([0, 1.2, 0])
        pm = T("0 = perfect match", 30, TEXT).move_to([-6.4, -1.45, 0], aligned_edge=LEFT)
        self.add(ax, mm, big, pm)
        self.play(Indicate(big, color=TEXT, scale_factor=1.15), run_time=1.0)
        self.at("we need to know")
        self.play(FadeOut(big), FadeOut(pm), run_time=0.7)
        tr = ValueTracker(0)
        self.start_u = 20
        pan = Panel(tr, start=20)
        pan.group.set_opacity(0)
        self.add(pan.group)
        self.play(pan.group.animate.set_opacity(1), run_time=0.8)
        self.play(tr.animate.set_value(3), run_time=2.0, rate_func=linear)
        self.at("so assume the ratio")
        lab = sim_label()
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.7)
        self.play(tr.animate.set_value(6), run_time=1.8, rate_func=linear)
        self.at("let a computer grow")
        self.play(tr.animate.set_value(80), run_time=3.0, rate_func=lambda x: x ** 2.0)
        self.at("score every run")
        self.play(Indicate(pan.score, color=TEXT, scale_factor=1.1), tr.animate.set_value(110), run_time=1.6, rate_func=linear)
        self.finish()


def s07_state(scene, run_to=20):
    ax = axis()
    mm = mendel_marker(dim=True)
    tr = ValueTracker(0)
    pan = Panel(tr, start=0)
    return ax, mm, tr, pan


class S07Predict(SpokenScene):
    def construct(self):
        ax, mm, tr, pan = s07_state(self)
        lab = sim_label()
        scores = [chi(RUNS[j]) for j in range(20)]
        lands = stack_dots(scores)
        dots = VGroup(*[Dot(radius=0.12, color=PALEGREY).move_to(SCORE_POS + np.array([0, -0.2, 0])) for _ in range(20)])
        for d in dots:
            d.set_opacity(0)
        self.add(ax, mm, lab, pan.group, dots)
        dur = 4.8

        def fall(m, dt):
            u = tr.get_value()
            for j, d in enumerate(m):
                s = u - j
                if s < 0:
                    d.set_opacity(0)
                    continue
                f = ease(min(s / 1.6, 1.0))
                src = SCORE_POS + np.array([0, -0.2, 0])
                d.move_to(src + (lands[j] - src) * f)
                d.set_opacity(1)
        dots.add_updater(fall)
        self.play(tr.animate.set_value(19.5), run_time=dur, rate_func=linear)
        self.at("where will the pile")
        pan.freeze()
        card = RoundedRectangle(corner_radius=0.2, width=4.9, height=2.2, stroke_color=TEXT, stroke_width=3,
                                fill_color=BG, fill_opacity=0.95).move_to([3.95, 1.0, 0])
        qt = T("Where will the pile\nof dots balance?", 38, TEXT).move_to(card)
        self.play(FadeOut(pan.score), FadeOut(pan.run), FadeIn(VGroup(card, qt), scale=0.9), run_time=0.9)
        self.play(Indicate(dots, color=TEXT, scale_factor=1.4), run_time=1.0)
        self.finish()


class S08Pause(SpokenScene):
    def construct(self):
        ax, mm, tr, pan = s07_state(self)
        tr.set_value(19.5)
        pan.freeze()
        pan._upd(pan.group)
        lab = sim_label()
        scores = [chi(RUNS[j]) for j in range(20)]
        lands = stack_dots(scores)
        dots = VGroup(*[Dot(radius=0.12, color=PALEGREY).move_to(p) for p in lands])
        card = RoundedRectangle(corner_radius=0.2, width=4.9, height=2.2, stroke_color=TEXT, stroke_width=3,
                                fill_color=BG, fill_opacity=0.95).move_to([3.95, 1.0, 0])
        qt = T("Where will the pile\nof dots balance?", 38, TEXT).move_to(card)
        pan.group.remove(pan.score, pan.run)
        self.add(ax, mm, lab, pan.group, dots, card, qt)
        # ring timer, bottom right
        rt = ValueTracker(0)
        ring_bg = Circle(radius=0.38, stroke_color=PALEGREY, stroke_width=4, fill_opacity=0).move_to([6.0, -1.5, 0])
        ring_bg.set_stroke(opacity=0.5)
        ring = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * max(rt.get_value(), 0.001),
                                         stroke_color=TEXT, stroke_width=7, fill_opacity=0).move_to([6.0, -1.5, 0]))
        self.add(ring_bg, ring)
        self.play(rt.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        ax, mm, tr, pan = s07_state(self)
        tr.set_value(19.5)
        pan.freeze()
        pan._upd(pan.group)
        pan.group.remove(pan.score, pan.run)
        scores = [chi(RUNS[j]) for j in range(20)]
        old = VGroup(*[Dot(radius=0.12, color=PALEGREY).move_to(p) for p in stack_dots(scores)])
        lab = sim_label()
        card = RoundedRectangle(corner_radius=0.2, width=4.9, height=2.2, stroke_color=TEXT, stroke_width=3,
                                fill_color=BG, fill_opacity=0.95).move_to([3.95, 1.0, 0])
        qt = T("Where will the pile\nof dots balance?", 38, TEXT).move_to(card)
        self.add(ax, mm, lab, pan.group, old, card, qt)
        # the card dissolves and the dots rain until the pile holds 10,000 runs
        gt = ValueTracker(0)
        hist = hist_rects(0.0)
        hist.add_updater(lambda m: set_hist(m, gt.get_value()))
        rng = np.random.default_rng(4)
        vals = rng.choice(len(HC), size=70, p=HC / HC.sum())
        rain = VGroup()
        for b in vals:
            d = Dot(radius=0.07, color=PALEGREY)
            d.ph = rng.random()
            d.bx = X(EDGES[b] + 0.125)
            d.bi = b
            rain.add(d)

        def drop(m, dt):
            t = gt.get_value()
            for d in m:
                c = (t * 9.0 + d.ph) % 1.0
                top = AX_Y + HC[d.bi] * HS * t
                d.move_to([d.bx, 3.2 + (top - 3.2) * c, 0])
                d.set_opacity(1.0 if t < 0.98 else 0.0)
        rain.add_updater(drop)
        cnt = M("0 runs", 32, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)
        cnt.add_updater(lambda m: m.become(M(f"{int(10000 * gt.get_value()):,} runs", 32, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)).set_opacity(min(1.0, max(0.0, (gt.get_value() - 0.12) * 12))))
        self.add(hist, rain, cnt)
        mx = X(MEAN10)
        fulc = tri(mx, TEXT, 1.0, big=True)
        flab = T("average = 3", 30, TEXT).move_to([mx, -3.45, 0])
        self.play(AnimationGroup(
            FadeOut(card), FadeOut(qt), FadeOut(pan.group), FadeOut(lab, run_time=0.3), FadeOut(mm), FadeOut(old),
            gt.animate.set_value(1.0).set_rate_func(linear).set_run_time(3.0),
            Succession(Wait(0.35), AnimationGroup(FadeIn(fulc, shift=UP * 0.3), FadeIn(flab), run_time=0.8)),
            run_time=3.0))
        hist.clear_updaters(); rain.clear_updaters(); cnt.clear_updaters()
        set_hist(hist, 1.0)
        self.remove(rain)
        cnt.become(M("10,000 runs", 32, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT))
        # four class boxes
        bx = [0.1, 1.7, 3.3, 4.9]
        boxes = VGroup()
        for i in range(4):
            b = RoundedRectangle(corner_radius=0.12, width=1.2, height=1.0, stroke_color=CLS[i], stroke_width=4,
                                 fill_color=CLS[i], fill_opacity=0.15).move_to([bx[i], 2.3, 0])
            boxes.add(VGroup(b, seed(i, 0.28).move_to(b)))
        avg = VGroup(*[M(f"{1 - p:.2f}", 30, CLS[i]).move_to([bx[i], 1.55, 0]) for i, p in enumerate(PROBS)])
        self.at("each class adds")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in boxes], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(a) for a in avg], lag_ratio=0.2), run_time=1.6)
        self.at("on average")
        self.play(Indicate(avg, color=TEXT, scale_factor=1.2), run_time=1.2)
        self.at("four classes share one total")
        br = VGroup(Line([bx[0] - 0.6, 3.05, 0], [bx[3] + 0.6, 3.05, 0], color=TEXT, stroke_width=5),
                    Line([bx[0] - 0.6, 3.05, 0], [bx[0] - 0.6, 2.9, 0], color=TEXT, stroke_width=5),
                    Line([bx[3] + 0.6, 3.05, 0], [bx[3] + 0.6, 2.9, 0], color=TEXT, stroke_width=5))
        tt = T("one total: 556 seeds", 28, TEXT).move_to([(bx[0] + bx[3]) / 2, 3.45, 0])
        self.play(FadeOut(avg), Create(br), FadeIn(tt, shift=DOWN * 0.1), run_time=1.4)
        self.at("once three counts are known")
        free = VGroup(*[T("free", 30, CLS[i]).move_to([bx[i], 1.55, 0]) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(f) for f in free], lag_ratio=0.2),
                  *[boxes[i][0].animate.set_fill(CLS[i], 0.45) for i in range(3)], run_time=1.4)
        self.at("the fourth is fixed")
        lock_b = RoundedRectangle(corner_radius=0.06, width=0.5, height=0.4, fill_color=TEXT, fill_opacity=1, stroke_width=0)
        shackle = Arc(radius=0.17, start_angle=0, angle=PI, stroke_color=TEXT, stroke_width=6)
        lock = VGroup(shackle, lock_b).arrange(DOWN, buff=-0.02).move_to([bx[3], 2.3, 0])
        sl = T("set by\nthe total", 28, TEAL).move_to([bx[3], 1.4, 0])
        self.play(boxes[3][1].animate.set_opacity(0.25), FadeIn(lock, scale=1.6), FadeIn(sl), run_time=1.2)
        self.at("so only three misses")
        self.play(LaggedStart(*[Indicate(boxes[i], color=CLS[i], scale_factor=1.2) for i in range(3)], lag_ratio=0.3), run_time=1.8)
        self.at("three is the degrees")
        flab2 = T("average = 3 = degrees of freedom", 30, TEXT).move_to([-2.0, -3.45, 0])
        self.play(ReplacementTransform(flab, flab2), Indicate(fulc, color=TEXT, scale_factor=1.3), run_time=1.4)
        self.finish()


def pile_world(scene, tail=False, dim_tri=False):
    ax = axis()
    hist = hist_rects(1.0)
    mx = X(MEAN10)
    fulc = tri(mx, TEXT, 1.0, big=True)
    flab = T("average = 3 = degrees of freedom", 28, TEXT).move_to([-2.0, -3.45, 0])
    scene.add(hist, ax, fulc, flab)
    return ax, hist, fulc, flab


class S10Tail(SpokenScene):
    def construct(self):
        ax, hist, fulc, flab = pile_world(self)
        cnt = M("10,000 runs", 32, TEXT).move_to([-6.6, 3.5, 0], aligned_edge=LEFT)
        self.add(cnt)
        pile_rain(self, n=36, op=0.7, drop_h=0.6)
        self.at("mark the far edge")
        edge = DashedLine([X(7.81), 3.0, 0], [X(7.81), AX_Y, 0], color=TEXT, stroke_width=5)
        el = M("7.81", 34, TEXT).move_to([X(7.81), 3.35, 0])
        self.play(Create(edge), FadeIn(el, shift=DOWN * 0.1), run_time=1.2)
        self.at("only one run in")
        tail = region(7.81, REDGREY, 0.9)
        tl = T(f"5% of chance runs", 32, REDGREY).move_to([3.7, -0.5, 0])
        pt = Arrow([4.6, -0.95, 0], [4.0, -1.85, 0], buff=0, color=REDGREY, stroke_width=6)
        self.play(FadeIn(tail), FadeIn(tl, shift=DOWN * 0.1), GrowArrow(pt), run_time=1.4)
        ripple(tail)
        self.at("counts out here")
        self.play(Indicate(tl, color=REDGREY, scale_factor=1.15), run_time=1.2)
        self.at("that is a reason")
        self.play(Indicate(el, color=TEXT, scale_factor=1.3), run_time=1.2)
        self.finish()


class S11Hold(SpokenScene):
    def construct(self):
        ax, hist, fulc, flab = pile_world(self)
        edge = DashedLine([X(7.81), 3.0, 0], [X(7.81), AX_Y, 0], color=TEXT, stroke_width=5)
        el = M("7.81", 34, TEXT).move_to([X(7.81), 3.35, 0])
        tail = region(7.81, REDGREY, 0.9)
        tl = T("5% of chance runs", 32, REDGREY).move_to([3.7, -0.5, 0])
        self.add(edge, el, tail, tl)
        ripple(tail)
        pile_rain(self, n=14, lo=7.81, r=0.1, color=REDGREY, op=0.9, period=1.6, drop_h=0.4)
        self.wait(2.4)
        self.finish()


class S12Mendel(SpokenScene):
    def construct(self):
        ax, hist, fulc, flab = pile_world(self)
        self.remove(fulc, flab)
        tail = region(7.81, REDGREY, 0.9)
        self.add(tail)
        self.play(FadeOut(tail), run_time=0.5)
        mx = X(CHI_M)
        self.at("drop mendel's score")
        mk = Polygon([mx, top_of(CHI_M) + 0.08, 0], [mx - 0.25, top_of(CHI_M) + 0.6, 0], [mx + 0.25, top_of(CHI_M) + 0.6, 0])
        mk.set_fill(TEXT, 1).set_stroke(TEXT, 2)
        mk.shift(UP * 2.2)
        mline = DashedLine([mx, top_of(CHI_M), 0], [mx, AX_Y, 0], color=TEXT, stroke_width=4)
        ml = T("Mendel 0.47", 30, TEXT).move_to([-6.4, 3.0, 0], aligned_edge=LEFT)
        self.play(mk.animate.shift(DOWN * 2.2), FadeIn(ml), run_time=1.3, rate_func=rush_into)
        self.play(Create(mline), run_time=0.6)
        pile_rain(self, n=36, op=0.7, seedv=8, drop_h=0.4)
        mk.t = 0.0
        mk0 = mk.get_center().copy()

        def bob(m, dt):
            m.t += dt
            m.move_to(mk0 + UP * 0.1 * math.sin(3.0 * m.t))
        mk.add_updater(bob)
        self.at("it sits far to the left")
        self.play(Indicate(mk, color=TEXT, scale_factor=1.4), run_time=1.0)
        self.at("deep inside the pile")
        self.play(Indicate(hist[1], color=TEXT, scale_factor=1.05), run_time=1.0)
        self.at("most chance runs")
        far = region(CHI_M, TEXT, 0.55)
        fl = T(f"{round(FAR_FRAC * 100):d}% of runs land further out", 32, TEXT).move_to([1.2, 1.9, 0])
        self.play(LaggedStart(*[FadeIn(r) for r in far], lag_ratio=0.03), FadeIn(fl, shift=DOWN * 0.1), run_time=2.4)
        self.at("that share of runs")
        pv = M(f"p ≈ {FAR_FRAC:.2f}", 64, TEXT).move_to([2.4, 0.5, 0])
        self.play(FadeIn(pv, scale=0.7), run_time=1.0)
        self.play(Indicate(pv, color=TEXT, scale_factor=1.1), run_time=1.0)
        self.finish()


def pile_rain(scene, n=40, op=0.85, lo=0.0, r=0.08, seedv=5, color=PALEGREY, period=2.4, top=3.0, drop_h=None):
    """Chance runs keep landing on the pile (a live simulation): dots fall onto bars chosen by the real histogram."""
    rng = np.random.default_rng(seedv)
    w = HC.astype(float)
    w[:int(lo / 0.25)] = 0
    w = w / w.sum()
    bins = rng.choice(len(HC), size=n, p=w)
    g = VGroup(*[Dot(radius=r, color=color) for _ in bins])
    for d, b in zip(g, bins):
        d.bx, d.bi, d.ph = X(EDGES[b] + 0.125 + rng.uniform(-0.1, 0.1)), b, rng.random()
    g.t = 0.0

    def drop(m, dt):
        m.t += dt
        for d in m:
            c = (m.t / period + d.ph) % 1.0
            tp = AX_Y + HC[d.bi] * HS + 0.06
            y0 = top if drop_h is None else tp + drop_h
            d.move_to([d.bx, y0 + (tp - y0) * c, 0])
            d.set_opacity(op * (1.0 if c < 0.92 else (1 - c) / 0.08))
    g.add_updater(drop)
    drop(g, 0)
    scene.add(g)
    return g


def ripple(tail):
    tail.t = 0.0

    def upd(m, dt):
        m.t += dt
        for k, r in enumerate(m):
            r.set_fill(REDGREY, 0.45 + 0.5 * max(0.0, math.sin(4.0 * m.t - 0.7 * k)))
    tail.add_updater(upd)


def dim_pile(scene, op=0.18):
    ax = axis()
    hist = hist_rects(1.0)
    g = VGroup(hist, ax)
    g.set_opacity(op)
    scene.add(g)
    return g


def card_box():
    return RoundedRectangle(corner_radius=0.2, width=12.2, height=2.7, stroke_color=TEXT, stroke_width=3,
                            fill_color=BG, fill_opacity=0.95).move_to([0, 1.6, 0])


def card_text():
    l1 = T("p = share of chance runs at least this far off,", 38, TEXT)
    l2 = T("if the ratio and every assumption hold.", 38, TEXT)
    return VGroup(l1, l2).arrange(DOWN, buff=0.25).move_to([0, 1.6, 0])


def assumption_chips():
    names = ["independent seeds", "correct scoring", "equal survival"]
    xs = [-4.1, 0.0, 4.1]
    return VGroup(*[chip(n, TEXT, 28).move_to([x, -0.45, 0]) for n, x in zip(names, xs)])


class S13Meaning(SpokenScene):
    def construct(self):
        dim_pile(self)
        pile_rain(self, n=40, op=0.3, seedv=3)
        box = card_box()
        txt = card_text()
        self.add(box)
        self.play(Write(txt[0]), run_time=1.6)
        self.play(Write(txt[1]), run_time=1.6)
        self.at("that means independent seeds")
        chips = assumption_chips()
        self.play(FadeIn(chips[0], shift=UP * 0.15), run_time=0.8)
        self.at("correct scoring")
        self.play(FadeIn(chips[1], shift=UP * 0.15), run_time=0.8)
        self.at("and equal survival")
        self.play(FadeIn(chips[2], shift=UP * 0.15), run_time=0.8)
        self.at("it is not the chance")
        wrong = T("the chance the ratio is true", 40, TEXT).move_to([0, -1.9, 0])
        self.play(FadeIn(wrong, shift=UP * 0.15), run_time=1.0)
        strike = Line(wrong.get_left() + LEFT * 0.15, wrong.get_right() + RIGHT * 0.15, color=REDGREY, stroke_width=8)
        self.play(Create(strike), run_time=0.9)
        self.finish()


class S14Large(SpokenScene):
    def construct(self):
        dim_pile(self)
        pile_rain(self, n=40, op=0.3, seedv=3)
        box = card_box()
        txt = card_text()
        chips = assumption_chips()
        wrong = T("the chance the ratio is true", 40, TEXT).move_to([0, -1.9, 0])
        strike = Line(wrong.get_left() + LEFT * 0.15, wrong.get_right() + RIGHT * 0.15, color=REDGREY, stroke_width=8)
        self.add(box, txt, chips, wrong, strike)
        self.play(FadeOut(VGroup(wrong, strike)), run_time=0.8)

        def stamp(word, col):
            b = RoundedRectangle(corner_radius=0.12, width=4.6, height=1.2, stroke_color=col, stroke_width=8,
                                 fill_color=BG, fill_opacity=0.9)
            return VGroup(b, T(word, 52, col, weight=BOLD).move_to(b)).rotate(-0.14)
        self.at("does not prove")
        pr = stamp("proven", PALEGREY).move_to([0, -2.1, 0])
        pr.scale(2.4).set_opacity(0)
        self.play(pr.animate.scale(1 / 1.5).set_opacity(0.9), run_time=0.7, rate_func=rush_into)
        self.wait(0.5)
        self.play(FadeOut(pr, shift=UP * 0.3), run_time=0.8)
        self.at("it gives no reason")
        nr = stamp("not rejected", TEXT).move_to([0, -2.1, 0])
        nr.scale(2.4).set_opacity(0)
        self.play(nr.animate.scale(1 / 2.4).set_opacity(1), run_time=0.5, rate_func=rush_into)
        self.play(Indicate(nr, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.at("other models might fit")
        om = T("other models may fit too", 34, TEXT).move_to([0, -3.35, 0])
        self.play(FadeIn(om, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S15Idea(SpokenScene):
    def construct(self):
        ax, hist, fulc, flab = pile_world(self)
        edge = DashedLine([X(7.81), 1.1, 0], [X(7.81), AX_Y, 0], color=TEXT, stroke_width=5)
        el = M("7.81", 30, TEXT).move_to([X(7.81), 1.45, 0])
        tail = region(7.81, REDGREY, 0.9)
        self.add(edge, el, tail)
        pile_rain(self, n=36, op=0.7, seedv=6, top=1.5)
        s1 = T("A ratio predicts a spread of counts.", 34, TEXT).move_to([-6.6, 3.4, 0], aligned_edge=LEFT)
        s2 = T("If the ratio holds, χ² averages its degrees of freedom.", 34, TEXT).move_to([-6.6, 2.7, 0], aligned_edge=LEFT)
        s3 = T("Far above that, doubt the ratio, but never call it proof.", 34, TEXT).move_to([-6.6, 2.0, 0], aligned_edge=LEFT)
        flab.set_opacity(0)
        fulc.t = 0.0

        def rock(m, dt):
            m.t += dt
        ripple(tail)
        self.at("a ratio predicts")
        self.play(FadeIn(s1, shift=RIGHT * 0.2), run_time=1.0)
        self.play(Indicate(hist, color=PALEGREY, scale_factor=1.03), run_time=1.2)
        self.at("if the ratio holds")
        self.play(FadeIn(s2, shift=RIGHT * 0.2), run_time=1.0)
        self.at("chi square averages")
        self.play(Indicate(fulc, color=TEXT, scale_factor=1.4), flab.animate.set_opacity(1), run_time=1.4)
        self.at("far above that")
        self.play(FadeIn(s3, shift=RIGHT * 0.2), run_time=1.0)
        self.at("but never call it proof")
        self.play(Indicate(tail, color=REDGREY, scale_factor=1.1), Indicate(el, color=TEXT, scale_factor=1.3), run_time=1.4)
        self.finish()


class S16End(EndCard):
    LINE = "Chi-square far above its degrees of freedom casts doubt on the ratio."
