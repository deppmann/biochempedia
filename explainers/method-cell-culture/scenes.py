"""Cell, primary and explant culture: keeping living tissue alive in a dish  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the apparatus: coverslip, slide, dish
  TEAL   = the medium: lymph, clot, culture medium, coating
  GREEN  = living tissue, cells and fibres
  YELLOW = the one thing you change or read: a factor, a halo, a result
  PURPLE = a partner: explant partner, tumour fragment, engineered cell
  ORANGE = the seal (wax) and handling steps
  RED    = pitfall: contamination, wrong identity, an animal result that disagrees
  GREY   = fixed specimens, outlines, labels
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def smooth(pts, color=GREEN, w=4):
    m = VMobject()
    m.set_points_smoothly([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def blob(c, r=0.3, color=GREEN, op=0.35, w=3):
    return Circle(radius=r, stroke_color=color, stroke_width=w, fill_color=color, fill_opacity=op).move_to([c[0], c[1], 0])


def neurites(c, n, L, rng, color=GREEN, w=4):
    g = VGroup()
    a0 = rng.rand() * 6.28
    for k in range(n):
        a = a0 + k * 6.28 / n + rng.randn() * 0.3
        ln = L * (0.6 + 0.6 * rng.rand())
        pts = [[c[0], c[1]]]
        x, y, th = c[0], c[1], a
        for s in range(3):
            th += rng.randn() * 0.45
            x += np.cos(th) * ln / 3
            y += np.sin(th) * ln / 3
            pts.append([x, y])
        g.add(smooth(pts, color, w))
    return g


def neuron(c, r=0.26, n=4, L=1.0, seed=0, color=GREEN):
    rng = np.random.RandomState(seed)
    return VGroup(neurites(c, n, L, rng, color, 4), blob(c, r, color, 0.5))


def mesh(x0, x1, y0, y1, n, rng, color=TEAL, w=1.8, op=0.8):
    g = VGroup()
    for _ in range(n):
        a = [x0 + (x1 - x0) * rng.rand(), y0 + (y1 - y0) * rng.rand()]
        b = [x0 + (x1 - x0) * rng.rand(), y0 + (y1 - y0) * rng.rand()]
        g.add(Line([a[0], a[1], 0], [b[0], b[1], 0], color=color, stroke_width=w, stroke_opacity=op))
    return g


def radial(c, n, L0, L1, rng, color=GREEN, w=3, start=0.45):
    """n short wavy fibres radiating from c; lengths between L0 and L1."""
    g = VGroup()
    for k in range(n):
        a = k * 6.28 / max(n, 1) + rng.randn() * 0.12
        ln = L0 + (L1 - L0) * rng.rand()
        d = np.array([np.cos(a), np.sin(a)])
        p0 = np.array(c) + d * start
        pts = [p0, p0 + d * ln * 0.5 + np.array([-d[1], d[0]]) * rng.randn() * 0.08, p0 + d * ln]
        g.add(smooth(pts, color, w))
    return g


def tubeless_dish(c, w, h, color=BLUE, fill=TEAL, op=0.10):
    return RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=fill, fill_opacity=op).move_to([c[0], c[1], 0])


def src(text, x, y, size=24, color=GOLD):
    return T(text, size, color).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Keeping Living Tissue Alive in a Dish"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """fixed row of fibres: growing or just becoming visible? Someone had to watch; the animal is tangled, the dish isolates."""

    def construct(self):
        base_y = -2.3
        xs = np.linspace(-5.0, 5.0, 8)
        hs = [0.7, 1.2, 1.8, 2.3, 2.9, 3.3, 3.8, 4.2]
        slab = Rectangle(width=12.6, height=0.55, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.25).move_to([0, base_y - 0.28, 0])
        fibs = VGroup(*[VGroup(Line([x, base_y, 0], [x, base_y + h, 0], color=GREY, stroke_width=9),
                               blob([x, base_y + h], 0.14, GREY, 0.9)) for x, h in zip(xs, hs)])
        slab_lbl = lab("fixed tissue", 26, GREY).move_to([0, base_y - 0.28, 0])
        head = lab("Every specimen was fixed", 30, GREY, weight=BOLD).move_to([-3.4, 3.1, 0])

        self.at("Every specimen")
        self.play(FadeIn(slab), FadeIn(slab_lbl), FadeIn(head), run_time=0.6)
        self.at("A row of")
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in fibs], lag_ratio=0.15), run_time=1.6)
        self.at("could show stages")
        grow_arr = arr([xs[0], base_y + hs[0] + 0.45, 0], [xs[-1] + 0.1, base_y + hs[-1] + 0.45, 0], YELLOW, w=7, tip=0.3)
        c1 = chip("one fibre growing?", YELLOW, 30).move_to([-2.6, 1.8, 0])
        self.play(GrowArrow(grow_arr), FadeIn(c1), run_time=0.9)
        self.at("becoming visible")
        self.play(FadeOut(grow_arr), FadeOut(c1), *[f.animate.set_opacity(0.2) for f in fibs], run_time=0.4)
        c2 = chip("old fibres becoming visible?", YELLOW, 30).move_to([-2.4, 1.8, 0])
        self.play(FadeIn(c2), LaggedStart(*[f.animate.set_opacity(1.0) for f in fibs], lag_ratio=0.2), run_time=1.6)
        self.at("Someone had to watch")
        self.play(FadeOut(VGroup(fibs, slab, slab_lbl, head, c2)), run_time=0.5)

        dish = tubeless_dish([0, -0.3], 12.4, 5.6)
        medium = lab("medium", 26, TEAL).move_to([-5.2, -2.45, 0])
        dish_lbl = lab("a dish", 26, BLUE).move_to([5.2, -2.45, 0])
        soma = blob([-3.0, -0.8], 0.4, GREEN, 0.5)
        f_pts = [[-3.0, -0.8], [-2.1, -0.4], [-1.2, -0.1], [-0.2, 0.15], [0.9, 0.2], [2.0, 0.55], [3.1, 0.9]]
        self.play(FadeIn(dish), FadeIn(medium), FadeIn(dish_lbl), FadeIn(soma), run_time=0.6)
        fibre = smooth(f_pts, GREEN, 6)
        tip = blob(f_pts[-1], 0.18, GREEN, 0.9)
        eye = chip("watch one fibre while it is alive", GREEN, 30).move_to([0, 2.3, 0])
        self.play(FadeIn(eye), Create(fibre, run_time=1.6, rate_func=linear), run_time=1.6)
        self.add(tip)

        self.at("Inside a living animal")
        left = RoundedRectangle(corner_radius=0.3, width=6.0, height=5.2, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.08).move_to([-3.4, -0.2, 0])
        rng = np.random.RandomState(4)
        tang = VGroup(*[neurites([-3.4 + rng.uniform(-2.2, 2.2), -0.2 + rng.uniform(-1.7, 1.7)], 4, 1.5, rng, GREY, 3) for _ in range(9)])
        a_lbl = lab("inside a living animal", 28, GREY, weight=BOLD).move_to([-3.4, 2.75, 0])
        shrink = VGroup(dish, medium, dish_lbl, soma, fibre, tip, eye)
        self.play(FadeOut(eye), FadeOut(medium), FadeOut(dish_lbl),
                  VGroup(dish, soma, fibre, tip).animate.scale(0.45).move_to([3.4, -0.3, 0]), run_time=0.8)
        self.play(FadeIn(left), FadeIn(tang), FadeIn(a_lbl), run_time=0.7)
        hard = lab("hard to watch", 28, RED).move_to([-3.4, -3.1, 0])
        self.at("that is hard")
        self.play(FadeIn(hard), run_time=0.4)
        self.at("changing one thing")
        hard2 = lab("hard to change one thing at a time", 26, RED).move_to([-3.4, -3.1, 0])
        d_lbl = lab("a dish", 28, BLUE, weight=BOLD).move_to([3.4, 2.75, 0])
        dropper = chip("one thing changed", YELLOW, 26).move_to([3.4, 1.6, 0])
        dd = arr([3.4, 1.25, 0], [3.4, 0.55, 0], YELLOW, w=5, tip=0.2)
        self.play(ReplacementTransform(hard, hard2), FadeIn(d_lbl), FadeIn(dropper), GrowArrow(dd), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Explant(SpokenScene):
    """embryo -> neural tube piece -> drop of lymph on coverslip -> flip over hollow slide -> seal -> clot -> explant."""

    def construct(self):
        rng = np.random.RandomState(2)
        emb = Ellipse(width=10.0, height=2.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([0, 0.9, 0])
        tube = RoundedRectangle(corner_radius=0.2, width=7.4, height=0.62, stroke_color=GREEN, stroke_width=3,
                                fill_color=GREEN, fill_opacity=0.25).move_to([0, 1.3, 0])
        e_lbl = lab("frog embryo", 28, GREY).move_to([-4.6, -0.8, 0])
        t_lbl = lab("neural tube", 28, GREEN).move_to([4.2, 2.6, 0])
        cut = DashedVMobject(Rectangle(width=1.7, height=0.9, stroke_color=YELLOW, stroke_width=3).move_to([0, 1.3, 0]))
        piece = VGroup(RoundedRectangle(corner_radius=0.12, width=1.5, height=0.7, stroke_color=GREEN, stroke_width=3,
                                        fill_color=GREEN, fill_opacity=0.4),
                       *[Dot([dx, dy, 0], radius=0.05, color=GREEN) for dx, dy in [(-0.5, 0.12), (0, -0.12), (0.5, 0.1), (0.25, 0.15), (-0.2, 0.0)]]).move_to([0, 1.3, 0])
        stage = lab("stage: no nerve fibres yet", 32, YELLOW).move_to([0, -1.0, 0])

        C = np.array([0.0, 0.5, 0.0])
        cover = Rectangle(width=8.4, height=0.18, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to(C)
        drop = Polygon(*[[2.5 * np.cos(t), 0.59 + 1.3 * np.sin(t), 0] for t in np.linspace(0, np.pi, 40)],
                       stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.22)
        tissue = piece.copy().scale(1.5).move_to([0, 1.25, 0])
        cl = lab("coverslip", 28, BLUE).move_to([-5.2, 1.3, 0])
        dr = lab("drop of fresh adult frog lymph", 28, TEAL).move_to([0, 2.7, 0])

        self.at("Take a piece")
        self.play(FadeIn(emb), FadeIn(tube), FadeIn(e_lbl), FadeIn(t_lbl), run_time=0.7)
        self.play(Create(cut), run_time=0.5)
        self.at("Harrison removed")
        self.play(FadeOut(cut), piece.animate.shift(DOWN * 0.0), FadeIn(stage), run_time=0.4)
        self.at("any nerve")
        self.play(Indicate(stage, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("He set it in a drop")
        self.play(FadeOut(VGroup(emb, tube, e_lbl, t_lbl, stage)), FadeIn(cover), FadeIn(cl), run_time=0.5)
        self.play(FadeIn(drop), Transform(piece, tissue), FadeIn(dr), run_time=1.0)
        self.at("on a cover slip")
        self.play(Indicate(cover, color=BLUE), run_time=0.4)
        self.at("The lymph clotted")
        m = mesh(-1.9, 1.9, 0.75, 1.45, 24, rng)
        clot = lab("clots into a soft mesh", 30, TEAL).move_to([0, -0.5, 0])
        self.play(FadeOut(dr), Create(m, lag_ratio=0.05), FadeIn(clot), run_time=1.6)
        self.at("that held the tissue")
        self.play(Indicate(piece, color=GREEN, scale_factor=1.25), run_time=0.9)
        self.at("Then he inverted")
        flip = VGroup(cover, drop, piece, m)
        self.play(FadeOut(cl), FadeOut(clot), Rotate(flip, PI, about_point=C), run_time=1.0)
        self.at("over a hollow slide")
        slide = Polygon([-6.2, 0.41, 0], [-3.1, 0.41, 0], [-3.1, -1.25, 0], [3.1, -1.25, 0], [3.1, 0.41, 0], [6.2, 0.41, 0],
                        [6.2, -2.4, 0], [-6.2, -2.4, 0], stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18)
        sl = lab("hollow slide", 30, BLUE).move_to([-4.6, -1.3, 0])
        self.play(FadeIn(slide, shift=UP * 0.3), FadeIn(sl), run_time=0.8)
        self.at("and sealed it")
        seal = VGroup(*[Rectangle(width=0.7, height=0.26, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to([s_ * 3.9, 0.54, 0]) for s_ in (-1, 1)])
        sealt = lab("sealed", 30, ORANGE).move_to([5.0, 1.3, 0])
        self.play(FadeIn(seal), FadeIn(sealt), run_time=0.6)
        self.at("Tissue kept alive")
        ex = chip("explant", GREEN, 40).move_to([0, 2.7, 0])
        ex2 = lab("tissue kept alive outside the body", 28, TEXT).move_to([-3.5, 1.7, 0])
        ar = arr([0, 2.25, 0], [0, 0.15, 0], GREEN, w=5, tip=0.22)
        self.play(FadeIn(ex, shift=DOWN * 0.15), FadeIn(ex2), GrowArrow(ar), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Primary(SpokenScene):
    """cells wander on web threads; tissue broken into single cells plated thinly on a polylysine coverslip -> primary culture."""

    def construct(self):
        rng = np.random.RandomState(8)
        web = VGroup()
        cx0, cy0, ax, ay = 0.0, -0.1, 5.4, 2.5
        angs = [k * np.pi / 4 + 0.2 for k in range(8)]
        for a in angs:
            web.add(Line([cx0, cy0, 0], [cx0 + ax * np.cos(a), cy0 + ay * np.sin(a), 0], color=GREY, stroke_width=3))
        for f in (0.35, 0.65, 1.0):
            web.add(poly([[cx0 + f * ax * np.cos(a), cy0 + f * ay * np.sin(a)] for a in angs + [angs[0]]], GREY, 2))
        solid = lab("cells need a solid to move on", 34, TEXT, weight=BOLD).move_to([0, 3.2, 0])
        cpos = [(0, 0.45), (2, 0.7), (3, 0.5), (5, 0.8), (6, 0.35), (4, 0.9)]
        cells = VGroup(*[blob([cx0 + d * ax * np.cos(angs[k]), cy0 + d * ay * np.sin(angs[k])], 0.26, GREEN, 0.6) for k, d in cpos])
        cells.set_opacity(0.0)
        self.at("Cells need a solid")
        self.play(FadeIn(solid), run_time=0.5)
        self.at("Harrison saw frog cells")
        self.play(Create(web, lag_ratio=0.08), run_time=1.5)
        cells.set_opacity(1.0)
        self.play(FadeIn(cells, lag_ratio=0.2), run_time=0.8)
        wl = lab("frog cells wander along spider-web threads", 28, GREEN).move_to([0, -3.1, 0])
        self.at("threads")
        self.play(FadeIn(wl), cells.animate.shift(RIGHT * 0.4), run_time=0.7)

        self.at("To watch single neurons")
        self.play(FadeOut(VGroup(web, cells, solid, wl)), run_time=0.4)
        cover = RoundedRectangle(corner_radius=0.25, width=12.4, height=5.0, stroke_color=BLUE, stroke_width=4,
                                 fill_color=TEAL, fill_opacity=0.10).move_to([0, -0.7, 0])
        coat = lab("coverslip with polylysine coating", 26, TEAL).move_to([-3.4, -2.7, 0])
        block = VGroup(RoundedRectangle(corner_radius=0.2, width=2.6, height=1.4, stroke_color=GREEN, stroke_width=4,
                                        fill_color=GREEN, fill_opacity=0.3),
                       *[Dot([rng.uniform(-1.1, 1.1), rng.uniform(-0.55, 0.55), 0], radius=0.08, color=GREEN) for _ in range(14)]).move_to([-3.4, 0.9, 0])
        tl = lab("tissue", 30, GREEN).move_to([-3.4, 2.5, 0])
        self.play(FadeIn(block), FadeIn(tl), FadeIn(cover), FadeIn(coat), run_time=0.8)
        self.at("break tissue into single cells")
        singles = VGroup(*[blob([-3.4 + rng.uniform(-1.1, 1.1) + 6.2 * (k / 9.0), 0.9 + rng.uniform(-0.45, 0.45)], 0.2, GREEN, 0.6) for k in range(10)])
        bk = lab("single cells", 30, GREEN).move_to([3.4, 2.5, 0])
        self.play(FadeOut(block), FadeOut(tl), FadeIn(singles), FadeIn(bk), run_time=0.9)
        self.at("plate them thinly")
        spots = [(-5.1, 0.2), (-3.1, -1.4), (-1.5, 0.4), (0.3, -1.4), (1.9, 0.3), (3.6, -1.3), (5.2, 0.3), (-0.8, -0.7)]
        spots = [(-5.0, 0.0), (-3.0, -1.4), (-1.3, 0.3), (0.4, -1.4), (2.0, 0.2), (3.8, -1.3), (5.2, 0.1), (1.0, -0.6)]
        plated = VGroup(*[neuron(s, 0.26, 4, 1.0, seed=i) for i, s in enumerate(spots)])
        dn = lab("low density: each neuron can be followed", 30, TEXT).move_to([0, 3.15, 0])
        self.play(ReplacementTransform(singles, VGroup(*[blob(s, 0.26, GREEN, 0.5) for s in spots])), FadeOut(bk), FadeIn(dn), run_time=1.2)
        self.add(plated)
        self.at("Banker and Cowan")
        bc = lab("Banker and Cowan: fetal rat hippocampus", 28, GOLD).move_to([0, 2.45, 0])
        self.play(FadeIn(bc), run_time=0.5)
        self.at("coverslips")
        self.play(Indicate(coat, color=TEAL, scale_factor=1.1), run_time=0.8)
        self.at("Cells plated straight from tissue")
        pc = chip("primary culture", GREEN, 40).move_to([3.5, -2.55, 0])
        self.play(FadeIn(pc, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Medium(SpokenScene):
    """medium is an experiment variable: 12 compounds for HeLa; a line divides on; neurons alone fade, with explant last two weeks."""

    def construct(self):
        dish = tubeless_dish([0, -0.2], 12.4, 5.6)
        dname = lab("culture dish with medium", 26, TEAL).move_to([-3.6, -2.55, 0])
        self.at("The medium is part")
        self.play(FadeIn(dish), FadeIn(dname), run_time=0.6)
        chips = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.8, height=0.8, stroke_color=TEAL, stroke_width=2.5,
                                          fill_color=TEAL, fill_opacity=0.5) for _ in range(12)]).arrange_in_grid(3, 4, buff=0.2).move_to([-3.6, 0.1, 0])
        self.at("amino acid compounds")
        cl = lab("12 amino acid compounds", 28, TEAL).move_to([-3.6, 1.95, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in chips], lag_ratio=0.1), FadeIn(cl), run_time=1.4)
        self.at("necessary for growth")
        hela = VGroup(*[blob([3.0 + dx, 0.1 + dy], 0.42, GREEN, 0.5) for dx, dy in [(-0.4, 0.0), (0.4, 0.1)]])
        self.play(FadeIn(hela), run_time=0.5)
        hl = lab("HeLa cells: a cell line", 30, GREEN, weight=BOLD).move_to([3.0, 1.95, 0])
        self.at("a cell line")
        self.play(FadeIn(hl), run_time=0.4)
        more = VGroup(*[blob([3.0 + dx, 0.1 + dy], 0.42, GREEN, 0.5) for dx, dy in
                        [(-1.5, -0.5), (-0.9, 0.9), (0.0, -1.0), (1.3, 0.8), (1.5, -0.6), (-0.6, -0.1), (0.5, 0.2), (0.1, 1.1), (-1.7, 0.7)]])
        self.at("A continuous line")
        self.play(FadeIn(more, lag_ratio=0.15), run_time=1.0)
        ind = lab("a continuous line can divide indefinitely", 28, TEXT).move_to([2.2, -2.0, 0])
        loop = CurvedArrow([5.6, 1.3, 0], [5.6, -0.9, 0], angle=-2.4, color=YELLOW, stroke_width=5)
        self.at("can divide indefinitely")
        self.play(FadeIn(ind), Create(loop), run_time=0.8)

        self.at("Partners can be added")
        self.play(FadeOut(VGroup(dish, dname, chips, cl, hela, hl, more, ind, loop)), run_time=0.5)
        dA = tubeless_dish([-3.2, -0.2], 6.0, 5.2)
        dB = tubeless_dish([3.2, -0.2], 6.0, 5.2)
        tA = lab("neurons alone", 30, TEXT, weight=BOLD).move_to([-3.2, 3.1, 0])
        tB = lab("neurons with an explant alongside", 30, TEXT, weight=BOLD).move_to([3.2, 3.1, 0])
        nA = VGroup(*[neuron(p, 0.24, 4, 0.8, seed=i) for i, p in enumerate([(-4.8, 0.9), (-2.6, 1.3), (-4.0, -0.6), (-1.9, -0.8), (-3.2, 0.3)])])
        nB = VGroup(*[neuron(p, 0.24, 4, 0.8, seed=i + 10) for i, p in enumerate([(4.8, 1.3), (4.7, -0.7), (1.9, -0.8), (3.3, -1.3), (1.6, 1.0)])])
        ex = VGroup(RoundedRectangle(corner_radius=0.15, width=1.5, height=0.9, stroke_color=PURPLE, stroke_width=3,
                                     fill_color=PURPLE, fill_opacity=0.4).move_to([3.2, 0.5, 0]))
        exl = lab("explant", 26, PURPLE).move_to([3.2, 1.3, 0])
        self.at("Isolated hippocampal neurons")
        self.play(FadeIn(dA), FadeIn(dB), FadeIn(tA), FadeIn(tB), FadeIn(nA), FadeIn(nB), FadeIn(ex), FadeIn(exl), run_time=0.9)
        self.at("only a few days")
        la = lab("only a few days", 30, RED).move_to([-3.2, -2.35, 0])
        self.play(FadeIn(la), nA.animate.set_opacity(0.12), run_time=1.8)
        self.at("about two weeks")
        lb = lab("about two weeks", 30, GREEN).move_to([3.2, -2.35, 0])
        self.play(FadeIn(lb), Indicate(nB, color=GREEN, scale_factor=1.04), run_time=1.0)
        self.at("That is a")
        cc = chip("coculture", PURPLE, 36).move_to([3.2, 2.1, 0])
        self.play(FadeIn(cc, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """halo bioassay: five wells with a ganglion each, sample diluted along the row; bars of fibre density; highest dilution with a halo = activity."""

    def construct(self):
        rng = np.random.RandomState(7)
        xs = np.linspace(-4.9, 4.9, 5)
        cy = 1.45
        wells = VGroup(*[Circle(radius=1.15, stroke_color=BLUE, stroke_width=4, fill_color=TEAL, fill_opacity=0.10).move_to([x, cy, 0]) for x in xs])
        gang = VGroup(*[blob([x, cy], 0.3, GREEN, 0.6) for x in xs])
        dil = VGroup(*[lab(t, 26, GREY).move_to([x, cy - 1.55, 0]) for x, t in zip(xs, ["least diluted", "", "", "", "most diluted"])])
        dil[2].become(lab("sample, more and more diluted", 26, YELLOW).move_to([xs[2], cy - 1.55, 0]))
        sarr = arr([xs[0] - 0.9, cy - 2.05, 0], [xs[-1] + 0.9, cy - 2.05, 0], YELLOW, w=5, tip=0.22)
        ex = lab("idealised example", 28, GREY).move_to([-4.4, 3.25, 0])
        self.at("To read a halo")
        self.play(FadeIn(wells), FadeIn(gang), FadeIn(ex), FadeIn(dil), GrowArrow(sarr), run_time=1.0)
        counts = [30, 22, 12, 5, 0]
        lens = [(0.5, 0.72), (0.4, 0.62), (0.3, 0.5), (0.15, 0.28), (0, 0)]
        halos = [radial([x, cy], n, a, b, rng, GREEN, 3, 0.34) if n else VGroup() for x, n, (a, b) in zip(xs, counts, lens)]
        self.at("look at the")
        self.play(*[Create(h, lag_ratio=0.02) for h in halos], run_time=1.8)
        t_day = lab("after about a day", 30, TEXT, weight=BOLD).move_to([0.5, 3.25, 0])
        self.play(FadeIn(t_day), run_time=0.4)
        self.at("Their density shows")
        base_y = -3.0
        base = Line([xs[0] - 0.9, base_y, 0], [xs[-1] + 0.9, base_y, 0], color=GREY, stroke_width=3)
        bars = VGroup(*[Rectangle(width=1.2, height=max(c, 0.001) * 0.06, stroke_color=GREEN, stroke_width=3,
                                  fill_color=GREEN, fill_opacity=0.45).move_to([x, base_y + max(c, 0.001) * 0.06 / 2, 0]) for x, c in zip(xs, counts)])
        dens = lab("fibre density shows how much factor the sample holds", 28, TEXT).move_to([0, -0.6, 0])
        self.play(FadeOut(sarr), FadeIn(dens), FadeIn(base), *[GrowFromEdge(b, DOWN) for b in bars[:4]], run_time=1.0)
        self.at("The highest dilution")
        box = SurroundingRectangle(wells[3], color=YELLOW, buff=0.1, stroke_width=5, corner_radius=0.2)
        box2 = SurroundingRectangle(bars[3], color=YELLOW, buff=0.1, stroke_width=5, corner_radius=0.1)
        act = lab("highest dilution with a halo = the activity", 30, YELLOW, weight=BOLD).move_to([1.7, 3.25, 0])
        self.play(FadeOut(t_day), Create(box), Create(box2), FadeIn(act), run_time=0.8)
        self.at("most dilute dish gives none")
        no = lab("no halo", 28, RED).move_to([xs[4], base_y + 0.4, 0])
        self.play(FadeIn(no), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """mycoplasma that looks like nothing; wrong identity; a line that differs from tissue."""

    def construct(self):
        rng = np.random.RandomState(3)

        def vial(cx, cy, specks):
            body = RoundedRectangle(corner_radius=0.3, width=3.0, height=4.0, stroke_color=BLUE, stroke_width=4,
                                    fill_color=TEAL, fill_opacity=0.14).move_to([cx, cy, 0])
            g = VGroup(body)
            for _ in range(specks):
                g.add(Dot([cx + rng.uniform(-1.2, 1.2), cy + rng.uniform(-1.7, 1.7), 0], radius=0.06, color=RED))
            return g
        vA = vial(-4.4, 0.35, 0)
        vB = vial(-0.9, 0.35, 30)
        for d in vB[1:]:
            d.set_opacity(0.0)
        nA = lines("mycoplasma-free", "line", size=26, color=GREEN, buff=0.04, align=ORIGIN).move_to([-4.4, -2.15, 0])
        nB = lines("contaminated", "line", size=26, color=RED, buff=0.04, align=ORIGIN).move_to([-0.9, -2.15, 0])
        same = lab("both look clear", 32, TEXT, weight=BOLD).move_to([-2.65, 3.1, 0])
        self.at("Culture can mislead")
        self.play(FadeIn(vA), FadeIn(vB), FadeIn(nA), FadeIn(nB), FadeIn(same), run_time=0.8)
        self.at("Mycoplasma escapes detection")
        ch1 = lines("turbidity:", "nothing seen", size=28, color=GREY, buff=0.05, align=ORIGIN).move_to([4.4, 2.1, 0])
        ch2 = lines("ordinary microscopy:", "nothing seen", size=28, color=GREY, buff=0.05, align=ORIGIN).move_to([4.4, 0.55, 0])
        self.play(FadeIn(ch1), FadeIn(ch2), run_time=0.8)
        self.play(*[d.animate.set_opacity(0.22) for d in vB[1:]], run_time=0.8)
        self.at("and resists common antibiotics")
        ab = chip("common antibiotics", ORANGE, 30).move_to([4.4, -1.0, 0])
        xx = T("✕", 70, RED, weight=BOLD).move_to([4.4, -2.0, 0])
        self.play(FadeIn(ab), FadeIn(xx), run_time=0.7)
        self.at("Compare with")
        ctl = chip("control: compare with mycoplasma-free lines", GREEN, 26).move_to([0, -3.1, 0])
        self.play(Create(SurroundingRectangle(vA, color=GREEN, buff=0.12, stroke_width=5, corner_radius=0.3)), FadeIn(ctl), run_time=0.8)

        # ---- phase B: identity
        self.at("Identity can be wrong")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        xs3 = [-4.2, 0.0, 4.2]
        names = ["labelled line A", "labelled line B", "labelled line C"]
        cards = VGroup(*[RoundedRectangle(corner_radius=0.2, width=3.7, height=1.9, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.1).move_to([x, 1.5, 0]) for x in xs3])
        cl = VGroup(*[lab(t, 28, GREY).move_to([x, 1.5, 0]) for x, t in zip(xs3, names)])
        head = lab("other human lines", 32, TEXT, weight=BOLD).move_to([-3.5, 3.0, 0])
        self.play(FadeIn(cards), FadeIn(cl), FadeIn(head), run_time=0.7)
        self.at("Gartler reported")
        hl = VGroup(*[lab("apparently HeLa", 28, RED, weight=BOLD).move_to([x, 1.5, 0]) for x in xs3[:2]])
        gt = lab("Gartler, 1968", 30, GOLD).move_to([4.4, 3.0, 0])
        self.play(*[ReplacementTransform(cl[i], hl[i]) for i in range(2)], *[cards[i].animate.set_stroke(RED) for i in range(2)], FadeIn(gt), run_time=1.0)
        self.at("profiling was reproducible")

        def peaks(cx, cy, col, hs):
            base = Line([cx - 2.2, cy, 0], [cx + 2.2, cy, 0], color=GREY, stroke_width=2)
            bars = VGroup(*[Line([cx - 1.8 + i * 0.6, cy, 0], [cx - 1.8 + i * 0.6, cy + h, 0], color=col, stroke_width=10) for i, h in enumerate(hs)])
            return VGroup(base, bars)
        hs_ = [0.9, 1.6, 0.7, 1.4, 1.0, 0.5, 1.2]
        pa = peaks(-3.4, -2.05, YELLOW, hs_)
        pb = peaks(3.4, -2.05, YELLOW, hs_)
        la_ = lab("laboratory 1", 26, GREY).move_to([-3.4, -2.5, 0])
        lb_ = lab("laboratory 2", 26, GREY).move_to([3.4, -2.5, 0])
        eq = T("=", 80, GREEN, weight=BOLD).move_to([0, -1.4, 0])
        sh = lab("STR profile, idealised example", 28, GREY).move_to([0, -0.05, 0])
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(la_), FadeIn(lb_), FadeIn(sh), FadeIn(eq), run_time=0.9)
        self.at("across")
        n253 = lab("tested on 253 human lines: same profile in different laboratories", 28, GREEN).move_to([0, -3.2, 0])
        self.play(FadeIn(n253), run_time=0.5)

        # ---- phase C: line vs tissue
        self.at("And a line differs")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        tis = lab("normal tissue", 34, GREEN, weight=BOLD).move_to([-3.4, 2.9, 0])
        lin = lab("HeLa Kyoto line", 34, RED, weight=BOLD).move_to([3.4, 2.9, 0])
        y0 = 0.3
        flat = poly([[-5.9, y0], [-0.9, y0]], GREEN, 7)
        lv_ = [1.2, 1.2, -0.8, -0.8, 0.3, 1.4, 1.4, -1.3]
        pts = []
        for i in range(8):
            xa = 0.9 + i * 0.625
            pts += [[xa, y0 + lv_[i]], [xa + 0.625, y0 + lv_[i]]]
        uneven = poly(pts, RED, 7)
        base1 = DashedLine([-5.9, y0, 0], [-0.9, y0, 0], color=GREY, stroke_width=2)
        base2 = DashedLine([0.9, y0, 0], [5.9, y0, 0], color=GREY, stroke_width=2)
        cap = lab("copy number along the genome, idealised example", 28, GREY).move_to([0, -2.9, 0])
        self.play(FadeIn(tis), FadeIn(lin), FadeIn(base1), FadeIn(base2), FadeIn(cap), run_time=0.7)
        self.at("genome shows")
        self.play(Create(flat, rate_func=linear), Create(uneven, rate_func=linear), run_time=1.2)
        an = lab("extensive aneuploidy", 34, RED, weight=BOLD).move_to([3.4, -1.9, 0])
        self.at("extensive aneuploidy")
        self.play(FadeIn(an), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Unlocked1(SpokenScene):
    """Harrison: fibres grow from an explant into the clot, one from an isolated cell; Levi-Montalcini: halo near tumour fragment."""

    def construct(self):
        rng = np.random.RandomState(12)
        clot = RoundedRectangle(corner_radius=0.35, width=12.4, height=5.0, stroke_color=TEAL, stroke_width=3,
                                fill_color=TEAL, fill_opacity=0.08).move_to([0, -0.3, 0])
        m = mesh(-6.0, 6.0, -2.7, 2.1, 30, rng, TEAL, 1.4, 0.3)
        exp = VGroup(RoundedRectangle(corner_radius=0.2, width=2.2, height=1.6, stroke_color=GREEN, stroke_width=4,
                                      fill_color=GREEN, fill_opacity=0.4)).move_to([-4.7, -0.3, 0])
        el = lab("explant", 28, GREEN).move_to([-4.7, -1.5, 0])
        hd = lab("Harrison, early 1900s", 30, GOLD, weight=BOLD).move_to([-4.2, 3.1, 0])
        self.at("In the early")
        self.play(FadeIn(clot), FadeIn(m), FadeIn(exp), FadeIn(el), FadeIn(hd), run_time=0.9)
        self.at("watched")
        paths = [[[-3.6, 0.2], [-2.4, 0.7], [-1.0, 0.9], [0.4, 1.3], [1.8, 1.3]],
                 [[-3.6, -0.2], [-2.3, -0.1], [-0.8, -0.3], [0.6, -0.6], [2.2, -0.5]],
                 [[-3.7, -0.7], [-2.4, -1.2], [-1.0, -1.5], [0.4, -1.7], [1.8, -2.0]]]
        fibs = [smooth(p, GREEN, 6) for p in paths]
        tips = [blob(p[-1], 0.16, GREEN, 0.9) for p in paths]
        self.play(*[Create(f, run_time=2.0, rate_func=linear) for f in fibs], run_time=2.0)
        self.add(*tips)
        self.at("The clot held no chain")
        nochain = lab("no chain of cells in the clot", 28, TEAL).move_to([-0.8, -2.5, 0])
        self.play(FadeIn(nochain), run_time=0.5)
        self.at("a single isolated cell")
        iso = blob([3.7, 0.7], 0.34, GREEN, 0.55)
        ifib = smooth([[3.7, 0.7], [4.3, 0.3], [4.9, -0.2], [5.5, -0.8]], GREEN, 6)
        itip = blob([5.5, -0.8], 0.16, GREEN, 0.9)
        il = lab("one isolated cell", 28, YELLOW).move_to([4.2, 1.5, 0])
        self.play(FadeIn(iso), FadeIn(il), Create(ifib, run_time=1.2), run_time=1.2)
        self.add(itip)
        self.at("drawn out from one cell")
        cc = chip("an axon is drawn out from one cell", YELLOW, 28).move_to([2.6, 3.1, 0])
        self.play(FadeIn(cc, shift=DOWN * 0.15), run_time=0.7)

        # ---- Levi-Montalcini
        self.at("Rio de Janeiro")
        self.play(*[FadeOut(m_) for m_ in list(self.mobjects)], run_time=0.5)
        dish = tubeless_dish([0, -0.1], 12.4, 4.9)
        gan = VGroup(RoundedRectangle(corner_radius=0.3, width=1.5, height=1.1, stroke_color=GREEN, stroke_width=4,
                                      fill_color=GREEN, fill_opacity=0.5)).move_to([-2.8, 0.2, 0])
        tum = VGroup(RoundedRectangle(corner_radius=0.3, width=1.5, height=1.1, stroke_color=PURPLE, stroke_width=4,
                                      fill_color=PURPLE, fill_opacity=0.45)).move_to([4.4, 0.2, 0])
        gl = lab("chick ganglion", 28, GREEN).move_to([-4.4, -1.9, 0])
        tl = lab("tumour fragments", 28, PURPLE).move_to([4.4, -0.8, 0])
        hd2 = lab("Levi-Montalcini, Rio de Janeiro, early 1950s", 30, GOLD, weight=BOLD).move_to([0, 3.1, 0])
        self.play(FadeIn(dish), FadeIn(gan), FadeIn(tum), FadeIn(gl), FadeIn(tl), FadeIn(hd2), run_time=0.8)
        self.at("saw a halo")
        hr = np.random.RandomState(3)
        halo = VGroup()
        while len(halo) < 52:
            ang = hr.uniform(-np.pi, np.pi)
            if hr.rand() > 0.18 + 0.82 * (1 + np.cos(ang)) / 2:
                continue
            w_ = ((1 + np.cos(ang)) / 2) ** 1.3
            ln = 0.35 + 2.4 * (w_ ** 1.25) * hr.uniform(0.8, 1.0)
            d_ = np.array([np.cos(ang), np.sin(ang)])
            p0 = np.array([-2.8, 0.2]) + d_ * 0.66
            nrm = np.array([-d_[1], d_[0]])
            halo.add(smooth([p0, p0 + d_ * ln * 0.5 + nrm * hr.randn() * 0.08, p0 + d_ * ln], GREEN, 3.5))
        self.play(Create(halo, lag_ratio=0.02), run_time=1.6)
        hl = lab("a halo of fibres within a day", 30, YELLOW, weight=BOLD).move_to([3.2, 1.75, 0])
        self.at("within a day")
        self.play(FadeIn(hl), run_time=0.5)
        self.at("That halo became")
        bio = chip("the halo became the assay used to purify nerve growth factor", YELLOW, 28).move_to([0, -3.05, 0])
        self.play(FadeIn(bio, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Unlocked2(SpokenScene):
    """Scheiffele 2000: neuroligin on a non-neuronal cell with neuroligin triggers a terminal in a dish; the knockout animal still has synapses; the rule."""

    def construct(self):
        dish = tubeless_dish([0, -0.1], 12.4, 4.9)
        hd = lab("Scheiffele and colleagues, 2000", 30, GOLD, weight=BOLD).move_to([0, 3.1, 0])
        axon_cell = blob([-5.0, -0.1], 0.55, GREEN, 0.5)
        axl = lab("axon", 28, GREEN).move_to([-5.0, -1.1, 0])
        bare = blob([3.6, -0.1], 1.2, PURPLE, 0.35)
        nl = VGroup(*[Line([3.6 + 1.2 * np.cos(a), -0.1 + 1.2 * np.sin(a), 0], [3.6 + 1.65 * np.cos(a), -0.1 + 1.65 * np.sin(a), 0],
                           color=YELLOW, stroke_width=6) for a in np.linspace(2.2, 4.1, 5)])
        bl = lines("non-neuronal cell", "with neuroligin", size=28, color=PURPLE, buff=0.05, align=ORIGIN).move_to([3.6, -2.05, 0])
        self.at("colleagues found that")
        self.play(FadeIn(dish), FadeIn(hd), FadeIn(axon_cell), FadeIn(axl), FadeIn(bare), run_time=0.8)
        self.at("neuroligin on a")
        self.play(FadeIn(nl), FadeIn(bl), run_time=0.6)
        self.at("triggers")
        ax = smooth([[-4.5, -0.1], [-3.0, 0.2], [-1.2, 0.0], [0.4, 0.4], [1.4, 0.2], [2.35, -0.1]], GREEN, 7)
        self.play(Create(ax, run_time=2.4, rate_func=linear), run_time=2.4)
        self.at("contacting axons")
        term = VGroup(blob([2.25, -0.1], 0.3, YELLOW, 0.7), *[Dot([1.75 + 0.12 * i, -0.1 + 0.22 * ((-1) ** i), 0], radius=0.06, color=YELLOW) for i in range(5)])
        tl = lab("terminal forms: presynaptic differentiation", 28, YELLOW).move_to([-0.6, 1.5, 0])
        self.play(FadeIn(term, scale=0.5), FadeIn(tl), run_time=0.7)
        self.at("A partner cell")
        pc = lines("a partner with no other", "synaptic machinery", size=28, color=TEXT, buff=0.05, align=ORIGIN).move_to([-1.2, -1.75, 0])
        self.play(FadeIn(pc), run_time=0.6)

        # ---- animal
        self.at("Yet mice lacking")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        ttl = lab("mice lacking neuroligins 1 to 3: brainstem", 32, TEXT, weight=BOLD).move_to([0, 3.1, 0])
        base = Line([-6.0, -2.2, 0], [6.0, -2.2, 0], color=GREY, stroke_width=3)

        def bar(x, h, col):
            return Rectangle(width=1.4, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.45).move_to([x, -2.2 + h / 2, 0])
        b1 = bar(-4.7, 3.0, GREEN); b2 = bar(-3.0, 3.0, GREEN)
        b3 = bar(3.0, 3.0, GREEN); b4 = bar(4.7, 1.2, RED)
        wt1 = lab("normal", 24, GREY).move_to([-4.7, -2.6, 0]); ko1 = lab("lacking", 24, GREY).move_to([-3.0, -2.6, 0])
        wt2 = lab("normal", 24, GREY).move_to([3.0, -2.6, 0]); ko2 = lab("lacking", 24, GREY).move_to([4.7, -2.6, 0])
        g1 = lab("synapse number", 30, GREEN).move_to([-3.85, 1.4, 0])
        g2 = lab("transmission", 30, RED).move_to([3.85, 1.2, 0])
        ex = lab("illustration, not data", 28, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(ttl), FadeIn(base), run_time=0.5)
        self.at("synapses in normal number")
        self.play(FadeIn(b1), FadeIn(wt1), FadeIn(g1), run_time=0.5)
        self.play(FadeIn(b2), FadeIn(ko1), FadeIn(ex), run_time=0.5)
        self.at("with impaired transmission")
        self.play(FadeIn(b3), FadeIn(wt2), FadeIn(g2), run_time=0.4)
        self.play(FadeIn(b4), FadeIn(ko2), run_time=0.6)
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        rule = lines("Sufficient in a dish", "does not mean required in the animal.", size=46, color=TEXT, buff=0.25, align=ORIGIN)
        box = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.5, corner_radius=0.2)
        head = lab("KEEP THIS RULE", 26, GOLD, weight=BOLD).next_to(box, UP, buff=0.25)
        VGroup(rule, box, head).move_to([0, 0, 0])
        self.play(FadeIn(head), Create(box), run_time=0.5)
        self.at("sufficient in a dish")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Sufficient in a dish does not mean required in the animal."
