"""Mutation comes before selection  (Biochemistrypedia explainer, Genetics and Molecular Biology)

COLOR MAP (one color per concept, whole video)
  BLUE   = ordinary (sensitive) E. coli cells, the culture lawn, nodes of a dividing culture
  ORANGE = resistant cells / resistant colonies / a mutation and its descendants
  RED    = the virus, and "does not fit"
  GREY   = plates, tiles, outlines, axes
  TEAL   = repeated samples from one large culture (plating noise alone)
  YELLOW = the statistics: mean, variance, empty fraction, m, rate; highlights
  GREEN  = "fits"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
COUNTS = [0, 0, 1, 0, 3, 0, 0, 52, 2, 2]          # independent cultures (lesson)
BULK = [4, 8, 6, 3, 9, 5, 7, 6, 8, 4]             # bulk samples (lesson)


# ---------------------------------------------------------------------------------------------
def scatter(n, R, seed, dmin):
    """n points in a disk of radius R, no two closer than dmin (deterministic)."""
    rs = np.random.RandomState(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        a, r = rs.uniform(0, 2 * np.pi), R * np.sqrt(rs.uniform())
        p = np.array([r * np.cos(a), r * np.sin(a)])
        if all(np.linalg.norm(p - q) >= dmin for q in pts):
            pts.append(p)
    return pts


def dots_at(cx, cy, n, R, seed, dmin, rad, color):
    return VGroup(*[Dot([cx + p[0], cy + p[1], 0], radius=rad, color=color) for p in scatter(n, R, seed, dmin)])


def plate(cx, cy, r=0.85, lawn=True):
    return Circle(radius=r, stroke_color=GREY, stroke_width=3,
                  fill_color=BLUE, fill_opacity=0.28 if lawn else 0.0).move_to([cx, cy, 0])


def virus_drop(cx, cy, r, seed, n=5):
    """small red dots that start above a plate (not yet shown)."""
    rs = np.random.RandomState(seed)
    return VGroup(*[Dot([cx + rs.uniform(-r * 0.7, r * 0.7), cy + r + 0.55 + rs.uniform(0, 0.35), 0], radius=0.09, color=RED)
                    for _ in range(n)])


def sup(parts, size=34, color=TEXT):
    """a line of text with superscripts: parts is a list of str or ('^', str)."""
    pieces = []
    for p in parts:
        if isinstance(p, tuple):
            pieces.append(T(p[1], int(size * 0.62), color))
        else:
            pieces.append(T(p, size, color))
    g = VGroup(*pieces).arrange(RIGHT, buff=0.07, aligned_edge=DOWN)
    for p, m in zip(parts, pieces):
        if isinstance(p, tuple):
            m.shift(UP * size * 0.0045)
    return g


class S00Title(TitleCard):
    LESSON = "Mutation: Where Variation Comes From"
    TITLE = "Mutation Comes Before Selection"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """ten identical cultures meet the virus; the counts differ wildly."""

    def construct(self):
        xs = [-4.6 + 2.3 * i for i in range(5)]
        pos = [(x, 1.75) for x in xs] + [(x, -1.15) for x in xs]
        R = 0.85
        plates = [plate(x, y, R) for x, y in pos]
        self.at("Grow ten small cultures")
        self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in plates], lag_ratio=0.12), run_time=1.4)

        viruses = [virus_drop(x, y, R, 10 + i) for i, (x, y) in enumerate(pos)]
        self.at("bacterial virus")
        self.play(FadeIn(VGroup(*viruses)), run_time=0.4)
        self.play(*[v.animate.shift(DOWN * 0.95) for v in viruses], run_time=0.9)

        self.at("Nearly every cell dies")
        self.play(*[p.animate.set_fill(BLUE, 0.0) for p in plates], FadeOut(VGroup(*viruses)), run_time=1.0)

        cols = [dots_at(x, y, n, 0.66, 40 + i, 0.125, 0.06, ORANGE) for i, ((x, y), n) in enumerate(zip(pos, COUNTS))]
        self.at("A few survive")
        self.play(*[FadeIn(c, scale=1.6) for c in cols], run_time=0.8)

        nums = []
        for (x, y), n in zip(pos, COUNTS):
            nums.append(M(str(n), 36, TEXT, weight=BOLD).move_to([x, y - 1.3, 0]))
        wl = self._words()
        i0 = [i for i in range(len(wl) - 1) if wl[i][1] == "count" and wl[i + 1][1] == "them"][0]
        digits = [wl[i0 + 2 + k] for k in range(10)]
        times = [d[0] for d in digits]
        assert all(d[1].isdigit() for d in digits), digits
        self.at("Count them")
        for nm, tt in zip(nums, times):
            rest = tt - 0.12 - self.elapsed()
            if rest > 0.02:
                self.wait(rest)
            self.play(FadeIn(nm, scale=1.3), run_time=0.15)

        alike = T("same cells  ·  same virus  ·  same plates", 28, GREY).move_to([0, -3.25, 0])
        self.at("The cells")
        self.play(FadeIn(alike), run_time=0.5)
        why = T("why so different?", 32, YELLOW, weight=BOLD).move_to([0, -3.25, 0])
        box = SurroundingRectangle(VGroup(plates[7], nums[7]), color=YELLOW, buff=0.15, stroke_width=4)
        self.at("Why are the counts")
        self.play(ReplacementTransform(alike, why), Create(box), run_time=0.7)
        self.play(Indicate(nums[7], color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Induced(SpokenScene):
    """first explanation: the virus induces resistance; every cell has the same small chance."""

    def construct(self):
        h1 = bchip("1  the virus induces resistance", RED, 26).move_to([-3.4, 3.0, 0])
        h2 = bchip("2  mutants arise first", ORANGE, 26).move_to([3.6, 3.0, 0])
        self.at("Two explanations")
        self.play(FadeIn(h1, shift=DOWN * 0.15), FadeIn(h2, shift=DOWN * 0.15), run_time=0.7)

        xs = [-4.4 + 2.2 * i for i in range(5)]
        pos = [(x, 0.85) for x in xs] + [(x, -1.15) for x in xs]
        tiles = [Square(1.7, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=0.28).move_to([x, y, 0]) for x, y in pos]
        self.at("In the first")
        self.play(*dim(h2), *recolor(h1, RED), LaggedStart(*[FadeIn(t, scale=0.9) for t in tiles], lag_ratio=0.08), run_time=1.2)

        viruses = VGroup()
        for i, (x, y) in enumerate(pos):
            rs = np.random.RandomState(70 + i)
            for _ in range(4):
                viruses.add(Dot([x + rs.uniform(-0.6, 0.6), y + 1.15 + rs.uniform(0, 0.25), 0], radius=0.09, color=RED))
        viruses.set_opacity(0)
        self.at("the virus makes")
        self.play(viruses.animate.set_opacity(1), run_time=0.2)
        self.play(viruses.animate.shift(DOWN * 1.0), run_time=0.5)
        self.play(FadeOut(viruses), *[t.animate.set_fill(BLUE, 0.0) for t in tiles], run_time=0.3)
        cols = [dots_at(x, y, n, 0.6, 90 + i, 0.2, 0.07, ORANGE) for i, ((x, y), n) in enumerate(zip(pos, BULK))]
        self.at("a few of the cells")
        self.play(*[FadeIn(c, scale=1.5) for c in cols], run_time=0.7)

        same = T("the same small chance for every cell", 28, GREY).move_to([0, -2.6, 0])
        self.at("same small chance")
        self.play(FadeIn(same), run_time=0.5)
        self.at("random sampling")
        self.play(*[Indicate(c, color=ORANGE, scale_factor=1.12) for c in cols], run_time=0.9)
        rain = T("like raindrops on paving stones", 28, GREY).move_to([0, -2.6, 0])
        self.at("raindrops on paving stones")
        self.play(ReplacementTransform(same, rain), run_time=0.5)
        var = chip("variance  ≈  mean", YELLOW, 30).move_to([0, -3.3, 0])
        self.at("close to the mean")
        self.play(FadeIn(var, shift=UP * 0.12), run_time=0.5)
        self.finish()


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def dim(c, o=0.4):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


# ---------------------------------------------------------------------------------------------
class S03Mutation(SpokenScene):
    """second explanation: mutants arise during growth; early = jackpot, late = few, many = none."""

    LV, SP, DY, TOP = 4, 0.25, 1.05, 2.2

    def node(self, cx, l, i):
        n = 2 ** (self.LV - l)
        return np.array([cx + ((i + 0.5) * n - 8) * self.SP, self.TOP - l * self.DY, 0])

    def construct(self):
        cxs = [-4.3, 0.0, 4.3]
        h2 = chip("2  mutants arise during growth", ORANGE, 28).move_to([0, 3.1, 0])
        self.at("In the second")
        self.play(FadeIn(h2, shift=DOWN * 0.15), run_time=0.6)

        edges = [{} for _ in cxs]
        dots = [{} for _ in cxs]
        for k, cx in enumerate(cxs):
            dots[k][(0, 0)] = Dot(self.node(cx, 0, 0), radius=0.1, color=BLUE)
            for l in range(1, self.LV + 1):
                for i in range(2 ** l):
                    a, b = self.node(cx, l - 1, i // 2), self.node(cx, l, i)
                    edges[k][(l, i)] = Line(a, b, color=GREY, stroke_width=2.5)
                    dots[k][(l, i)] = Dot(b, radius=0.085 if l < self.LV else 0.1, color=BLUE)
        self.at("Follow three cultures")
        self.play(*[FadeIn(dots[k][(0, 0)]) for k in range(3)], run_time=0.4)
        for l in range(1, self.LV + 1):
            self.play(*[Create(edges[k][(l, i)]) for k in range(3) for i in range(2 ** l)],
                      *[FadeIn(dots[k][(l, i)]) for k in range(3) for i in range(2 ** l)], run_time=0.45)

        def mutate(k, l0, i0, cx):
            anims = []
            ring = Circle(radius=0.2, stroke_color=ORANGE, stroke_width=4).move_to(self.node(cx, l0, i0))
            for l in range(l0, self.LV + 1):
                lo, hi = i0 * 2 ** (l - l0), (i0 + 1) * 2 ** (l - l0)
                for i in range(lo, hi):
                    anims.append(dots[k][(l, i)].animate.set_color(ORANGE))
                    if l > l0:
                        anims.append(edges[k][(l, i)].animate.set_color(ORANGE))
            return ring, anims

        labels = []
        for k, (cx, t1, t2, c) in enumerate([(cxs[0], "early mutation", "large clone: a jackpot", ORANGE),
                                             (cxs[1], "late mutation", "only a few", ORANGE),
                                             (cxs[2], "no mutation", "no resistant cells", GREY)]):
            labels.append((T(t1, 26, c).move_to([cx, -2.8, 0]), T(t2, 24, c).move_to([cx, -3.35, 0])))

        self.at("An early mutation")
        ring, an = mutate(0, 1, 1, cxs[0])
        self.play(Create(ring), FadeIn(labels[0][0]), run_time=0.5)
        self.play(*an, run_time=0.7)
        self.at("a jackpot")
        self.play(FadeIn(labels[0][1]), run_time=0.4)
        self.at("a late one")
        ring2, an2 = mutate(1, 3, 5, cxs[1])
        self.play(Create(ring2), FadeIn(labels[1][0]), run_time=0.5)
        self.play(*an2, run_time=0.6)
        self.play(FadeIn(labels[1][1]), run_time=0.3)
        self.at("Many cultures have none")
        self.play(FadeIn(labels[2][0]), FadeIn(labels[2][1]), run_time=0.6)
        v = chip("variance  >>  mean", YELLOW, 30).move_to([0, 3.1, 0])
        self.at("far larger")
        self.play(ReplacementTransform(h2, v), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Compare(SpokenScene):
    """independent cultures versus repeated samples: same mean, very different scatter."""

    X0, K = -5.8, 0.21

    def x(self, v):
        return self.X0 + self.K * v

    def strip(self, vals, axis_y, color, seed):
        axis = Line([self.x(0) - 0.15, axis_y, 0], [self.x(56), axis_y, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([self.x(v), axis_y, 0], [self.x(v), axis_y - 0.12, 0], color=GREY, stroke_width=3),
                                M(str(v), 22, GREY).move_to([self.x(v), axis_y - 0.38, 0])) for v in range(0, 51, 10)])
        seen, dots = {}, VGroup()
        for v in vals:
            k = seen.get(v, 0)
            seen[v] = k + 1
            dots.add(Dot([self.x(v), axis_y + 0.2 + k * 0.23, 0], radius=0.1, color=color))
        return VGroup(axis, ticks), dots

    def construct(self):
        ay_top, ay_bot = 1.0, -2.0
        ax_b, dots_b = self.strip(COUNTS, ay_bot, ORANGE, 1)
        ax_t, dots_t = self.strip(BULK, ay_top, TEAL, 2)
        t_b = T("independent cultures", 28, ORANGE).move_to([3.0, -0.2, 0])
        t_t = T("samples from one large culture", 28, TEAL).move_to([2.4, 2.5, 0])

        self.play(FadeIn(ax_b), FadeIn(t_b), run_time=0.8)
        self.at("many independent cultures")
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots_b], lag_ratio=0.1), run_time=1.1)
        self.at("repeated samples")
        self.play(FadeIn(ax_t), FadeIn(t_t), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots_t], lag_ratio=0.1), run_time=1.1)
        tag = T("worked example: illustrative numbers", 24, GREY).move_to([0, 3.35, 0])
        self.at("illustrative numbers")
        self.play(FadeIn(tag), run_time=0.4)
        self.at("plating noise")
        self.play(Indicate(dots_t, color=TEAL, scale_factor=1.2), run_time=0.8)

        def meanline(axis_y, h):
            ln = DashedLine([self.x(6), axis_y, 0], [self.x(6), axis_y + h, 0], color=YELLOW, stroke_width=3, dash_length=0.1)
            lb = T("mean 6", 22, YELLOW).next_to(ln, UP, buff=0.05)
            return VGroup(ln, lb)
        mt, mb = meanline(ay_top, 1.0), meanline(ay_bot, 1.9)
        self.at("both sets have a mean")
        self.play(Create(mt), Create(mb), run_time=0.8)

        vt = chip("variance 4", YELLOW, 30).move_to([3.0, 1.75, 0])
        self.at("samples have a variance")
        self.play(FadeIn(vt, shift=LEFT * 0.15), run_time=0.5)
        vb = chip("variance about 262", YELLOW, 30).move_to([2.6, -0.85, 0])
        self.at("cultures have a variance")
        self.play(FadeIn(vb, shift=LEFT * 0.15), run_time=0.6)
        ratio = T("about 44 times the mean", 26, YELLOW).move_to([2.6, -1.5, 0])
        self.at("times the mean")
        self.play(FadeIn(ratio), run_time=0.5)

        ok = chip("mutation before exposure: fits", GREEN, 28).move_to([-3.0, -3.25, 0])
        no = chip("induction: does not", RED, 28).move_to([3.7, -3.25, 0])
        self.at("Mutation before exposure fits")
        self.play(FadeIn(ok, shift=UP * 0.15), run_time=0.5)
        self.at("induction does not")
        self.play(FadeIn(no, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Rate(SpokenScene):
    """the empty cultures give the number of mutation events, and so the rate."""

    def construct(self):
        xs = [-5.85 + 1.3 * i for i in range(10)]
        circles, nums = [], []
        for x, n in zip(xs, COUNTS):
            c = Circle(radius=0.52, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=0.0).move_to([x, 2.5, 0])
            circles.append(c)
            nums.append(M(str(n), 30, TEXT, weight=BOLD).move_to(c))
        g = VGroup(*circles, *nums)
        self.at("Now count mutation events")
        self.play(LaggedStart(*[FadeIn(VGroup(c, n), scale=0.9) for c, n in zip(circles, nums)], lag_ratio=0.07), run_time=1.1)

        asm = T("assumes every mutant counted · divisions ≈ final cell number", 22, GREY).move_to([0, 1.6, 0])
        self.at("assuming every mutant")
        self.play(FadeIn(asm), run_time=0.5)
        zero = [i for i, n in enumerate(COUNTS) if n == 0]
        self.at("Five of the ten")
        self.play(*[circles[i].animate.set_stroke(YELLOW, 5) for i in zero],
                  *[VGroup(circles[i], nums[i]).animate.set_opacity(0.35) for i in range(10) if i not in zero], run_time=0.7)
        self.play(*[Indicate(nums[i], color=YELLOW, scale_factor=1.3) for i in zero], run_time=0.8)

        l1 = VGroup(T("empty fraction  =  5 / 10  =  0.5", 36, YELLOW)).move_to([0, 1.0, 0])
        self.at("the empty fraction")
        self.play(FadeIn(l1, shift=UP * 0.12), run_time=0.6)
        l2 = VGroup(T("empty fraction  =  e", 36, YELLOW), T("−m", 26, YELLOW)).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)
        l2[1].shift(UP * 0.24)
        l2.move_to([0, 0.1, 0])
        self.at("Poisson distribution")
        self.play(FadeIn(l2, shift=UP * 0.12), run_time=0.6)
        l3 = T("m  =  −ln(0.5)  =  0.69 events per culture", 36, YELLOW).move_to([0, -0.8, 0])
        self.at("That makes m")
        self.play(FadeIn(l3, shift=UP * 0.12), run_time=0.6)
        l4 = VGroup(T("rate  =  0.69 / (2 × 10", 40, ORANGE), T("8", 28, ORANGE), T(")  =  3.5 × 10", 40, ORANGE),
                    T("−9", 28, ORANGE)).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)
        l4[1].shift(UP * 0.25)
        l4[3].shift(UP * 0.25)
        l4.move_to([0, -1.95, 0])
        sub = T("per cell, per division", 26, GREY).move_to([0, -2.75, 0])
        self.at("With about")
        self.play(FadeIn(l4, shift=UP * 0.12), run_time=0.6)
        self.at("the rate is")
        self.play(Indicate(l4, color=ORANGE, scale_factor=1.06), FadeIn(sub), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the resistant cells were already there; the virus only reveals them."""

    def construct(self):
        cx, cy, R = -3.0, 0.55, 2.4
        pl = Circle(radius=R, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=0.18).move_to([cx, cy, 0])
        pts = scatter(70, R - 0.2, 5, 0.31)
        pts_sorted = sorted(range(len(pts)), key=lambda i: np.linalg.norm(pts[i] - np.array([0.9, 0.7])))
        orange_idx = set(pts_sorted[:7]) | {pts_sorted[30], pts_sorted[55], pts_sorted[66]}
        cells = VGroup(*[Dot([cx + p[0], cy + p[1], 0], radius=0.09, color=ORANGE if i in orange_idx else BLUE)
                         for i, p in enumerate(pts)])
        orange = VGroup(*[cells[i] for i in sorted(orange_idx)])
        blue = VGroup(*[cells[i] for i in range(len(pts)) if i not in orange_idx])
        cap = T("before the virus", 28, GREY).move_to([cx, cy - R - 0.45, 0])

        self.at("So the virus did not")
        self.play(FadeIn(pl, scale=0.9), FadeIn(cells), FadeIn(cap), run_time=0.9)
        self.at("resistant cells")
        self.play(Indicate(orange, color=ORANGE, scale_factor=1.7), run_time=0.9)
        lab = T("resistant cells, already there", 26, ORANGE).move_to([cx, cy + R + 0.45, 0])
        self.at("already there")
        self.play(FadeIn(lab), run_time=0.5)

        rs = np.random.RandomState(8)
        vir = VGroup(*[Dot([cx + rs.uniform(-R * 0.8, R * 0.8), cy + R + 1.05 + rs.uniform(0, 0.4), 0], radius=0.08, color=RED)
                       for _ in range(16)])
        vir.set_opacity(0)
        self.at("only revealed them")
        self.play(vir.animate.set_opacity(1), FadeOut(lab), run_time=0.2)
        self.play(vir.animate.shift(DOWN * 1.9), run_time=0.8)
        cap2 = T("after the virus", 28, GREY).move_to(cap)
        self.play(FadeOut(vir), FadeOut(blue), ReplacementTransform(cap, cap2), run_time=0.9)
        self.play(*[d.animate.scale(1.6) for d in orange], run_time=0.6)

        c1 = bchip("1  mutation", ORANGE, 36).move_to([3.4, 1.4, 0])
        c2 = bchip("2  selection reveals it", RED, 36).move_to([3.4, -1.0, 0])
        ar = arr(c1.get_bottom(), c2.get_top(), GREY)
        self.at("Mutation comes first")
        self.play(FadeIn(c1, shift=LEFT * 0.15), run_time=0.5)
        self.at("Selection only reveals it")
        self.play(GrowArrow(ar), FadeIn(c2, shift=LEFT * 0.15), run_time=0.7)
        self.finish()


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S07End(EndCard):
    LINE = "Mutation comes first. Selection only reveals it."
