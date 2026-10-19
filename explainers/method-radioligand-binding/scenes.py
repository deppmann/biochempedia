"""Receptor binding and dose-response: counting receptors by what they hold  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = the labelled (radioactive) ligand, and the drug that is added
  PURPLE = receptors (cups on membranes)
  GREY   = membranes, tubes, axes, structure, de-emphasised text
  BLUE   = unlabelled competitor ligand
  YELLOW = specific binding: the curves we read, Kd, Bmax, bound complex
  RED    = nonspecific binding, and the pitfalls
  GREEN  = the response (EC50, full response) and a control
  TEAL   = the filter and the wash
  WHITE  = total binding
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
WHITE = TEXT
IDEAL = "idealised"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def dot(x, y, color=ORANGE, r=0.11):
    return Dot(point=[x, y, 0], radius=r, color=color)


class Rec(VGroup):
    """A receptor: a stem with a cup that opens upward. `base` is the top of the membrane."""

    def __init__(self, x, base, s=1.0, color=PURPLE):
        h, r = 0.26 * s, 0.2 * s
        stem = Line([x, base, 0], [x, base + h, 0], color=color, stroke_width=5)
        cup = Arc(radius=r, start_angle=PI, angle=PI, arc_center=[x, base + h + r, 0], color=color, stroke_width=5)
        self.site = np.array([x, base + h + r * 0.55, 0.0])
        super().__init__(stem, cup)


def frag(cx, y, w, n, s=1.0, bar_h=0.2):
    """A membrane fragment: grey bar centred at (cx, y) with n receptors on top."""
    bar = RoundedRectangle(corner_radius=0.08, width=w, height=bar_h, stroke_color=GREY, stroke_width=2.5,
                           fill_color=GREY, fill_opacity=0.4).move_to([cx, y, 0])
    top = y + bar_h / 2
    xs = [cx + (i - (n - 1) / 2) * (w / n) for i in range(n)]
    recs = [Rec(x, top, s) for x in xs]
    g = VGroup(bar, *recs)
    g.sites = [r.site for r in recs]
    g.top = top
    g.xs = xs
    return g


def axes(cx, cy, w, h, xr, yr):
    ax = Axes(x_range=list(xr), y_range=list(yr), x_length=w, y_length=h,
              axis_config={"include_tip": False, "include_ticks": False, "color": GREY, "stroke_width": 3})
    ax.move_to([cx, cy, 0])
    if xr[0] < 0:   # a log axis has no zero: draw the y axis at the left edge instead of at x = 0
        ya = Line(ax.c2p(xr[0], yr[0]), ax.c2p(xr[0], yr[1]), color=GREY, stroke_width=3)
        ax.y_axis.set_opacity(0)
        ax.add(ya)
    return ax


def curve(ax, f, x0, x1, color=YELLOW, w=5, n=140):
    xs = np.linspace(x0, x1, n)
    return poly([ax.c2p(x, f(x)) for x in xs], color, w)


def sat(x):          # specific binding fraction vs log10([L]/Kd)
    return 1.0 / (1.0 + 10.0 ** (-x))


def dash_h(ax, y, x0, x1, color=GREY):
    return DashedLine(ax.c2p(x0, y), ax.c2p(x1, y), color=color, stroke_width=3, dash_length=0.12)


def dash_v(ax, x, y0, y1, color=GREY):
    return DashedLine(ax.c2p(x, y0), ax.c2p(x, y1), color=color, stroke_width=3, dash_length=0.12)


def tagline(text, pos, size=22, color=GREY):
    return T(text, size, color, slant=ITALIC).move_to([pos[0], pos[1], 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Counting Receptors by What They Hold"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a drug acts on something nobody can isolate or count; a response is not occupancy; two questions."""

    def construct(self):
        cell = RoundedRectangle(width=12.2, height=1.8, corner_radius=0.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.12).move_to([0, 0.3, 0])
        cell_lbl = lab("muscle cell", 32).move_to([-4.6, 0.3, 0])
        box = DashedVMobject(Rectangle(width=4.8, height=2.0, stroke_color=PURPLE, stroke_width=4).move_to([2.6, 2.1, 0]))
        q = T("?", 64, PURPLE, weight=BOLD).move_to([2.6, 2.55, 0])
        sub = lab("receptive substance", 32, PURPLE).next_to(box, LEFT, buff=0.4)
        lang = T("Langley, 1905", 34, GOLD).move_to([-4.9, 3.15, 0])

        self.at("Langley argued")
        self.play(FadeIn(cell), FadeIn(cell_lbl), FadeIn(lang, shift=DOWN * 0.1), run_time=0.7)
        self.play(Create(box), FadeIn(q), FadeIn(sub), run_time=0.8)

        self.at("nicotine and curare")
        d1 = chip("nicotine", ORANGE, 28).move_to([1.4, 1.65, 0])
        d2 = chip("curare", ORANGE, 28).move_to([3.8, 1.65, 0])
        self.play(FadeIn(d1, shift=DOWN * 0.8), FadeIn(d2, shift=DOWN * 0.8), run_time=0.9)

        self.at("Nobody could isolate")
        n1 = chip("cannot isolate it", RED, 34).move_to([3.0, -1.2, 0])
        n2 = chip("cannot count it", RED, 34).move_to([3.0, -2.35, 0])
        self.play(FadeIn(n1, shift=UP * 0.15), run_time=0.5)
        self.at("or count it")
        self.play(FadeIn(n2, shift=UP * 0.15), run_time=0.5)

        self.at("inferred from a response")
        bath = Rectangle(width=6.4, height=2.5, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.14).move_to([-3.3, -2.25, 0])
        strip = RoundedRectangle(width=5.0, height=0.7, corner_radius=0.25, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.4).move_to([-3.3, -2.45, 0])
        bath_lbl = lab("organ bath", 28, TEAL).move_to([-3.3, -1.5, 0])
        self.play(FadeOut(n1), FadeOut(n2), FadeIn(bath), FadeIn(strip), FadeIn(bath_lbl), run_time=0.7)
        self.at("contraction in an organ")
        shr = strip.animate.stretch_to_fit_width(3.2).move_to([-3.3, -2.45, 0])
        resp = chip("response: contraction", GREEN, 34).move_to([3.0, -1.2, 0])
        self.play(shr, FadeIn(resp, shift=LEFT * 0.2), run_time=0.8)

        self.at("not the same as")
        neq = T("≠", 64, WHITE, weight=BOLD).move_to([3.0, -2.05, 0])
        occ = chip("occupancy", ORANGE, 34).move_to([3.0, -3.0, 0])
        self.play(FadeIn(neq), FadeIn(occ), run_time=0.6)

        self.at("So how many sites")
        old = Group(cell, cell_lbl, box, q, sub, lang, d1, d2, bath, strip, bath_lbl, resp, neq, occ)
        self.play(FadeOut(old), run_time=0.6)
        a = chip("How many sites does a tissue hold?", PURPLE, 44).move_to([0, 1.3, 0])
        self.play(FadeIn(a, shift=UP * 0.2), run_time=0.6)
        self.at("how tightly does")
        b = chip("How tightly does a ligand hold them?", ORANGE, 44).move_to([0, -1.3, 0])
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
TUBE_X = -3.4
REC_XS = [-5.05, -4.45, -3.65, -3.05, -2.25, -1.65]


def tube_items(cups_filled=0):
    tube = RoundedRectangle(width=5.8, height=6.3, corner_radius=0.35, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.05).move_to([TUBE_X, -0.1, 0])
    frags = [frag(-4.8, -2.55, 1.4, 2, 1.5), frag(-3.4, -2.55, 1.4, 2, 1.5), frag(-2.0, -2.55, 1.4, 2, 1.5)]
    return tube, frags


class S02Incubate(SpokenScene):
    """membranes + labelled ligand in a tube; incubate to equilibrium; Kd equation; tight binders take longer."""

    def construct(self):
        rng = np.random.RandomState(4)
        tube, frags = tube_items()
        sites = [s for f in frags for s in f.sites]
        mem_lbl = chip("membranes with receptors", PURPLE, 26).move_to([3.5, -2.1, 0])
        a_mem = arr([1.0, -2.1], [-1.0, -2.4], PURPLE, 4, 0.18)

        self.at("Take membranes")
        self.play(FadeIn(tube), *[FadeIn(f) for f in frags], run_time=0.7)
        self.play(FadeIn(mem_lbl, shift=LEFT * 0.2), GrowArrow(a_mem), run_time=0.5)

        self.at("Add a ligand")
        free_pos = [(-5.2, 1.9), (-4.4, 0.6), (-3.7, 2.3), (-2.9, 1.0), (-2.1, 2.0), (-1.6, 0.3), (-4.9, -0.7), (-3.3, -0.4), (-2.4, -1.1)]
        free = VGroup(*[dot(x, y + 1.6, ORANGE, 0.14) for x, y in free_pos])
        lig_lbl = chip("labelled ligand", ORANGE, 26).move_to([3.5, 0.2, 0])
        a_lig = arr([1.4, 0.2], [-0.9, 0.5], ORANGE, 4, 0.18)
        self.play(FadeIn(free, shift=DOWN * 0.3), run_time=0.5)
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(free, free_pos)], FadeIn(lig_lbl), GrowArrow(a_lig), run_time=0.8)

        self.at("biologically active")
        self.wait(0.6)

        self.at("Incubate until")
        self.play(FadeOut(mem_lbl), FadeOut(a_mem), FadeOut(lig_lbl), FadeOut(a_lig), run_time=0.4)
        bound_idx = [0, 2, 3, 5]
        moves = []
        for k, i in enumerate(bound_idx):
            moves.append(free[i].animate.move_to([sites[k][0], sites[k][1], 0]))
        self.play(*moves, run_time=1.4)
        bind = arr([0.6, 1.15], [3.0, 1.15], YELLOW, 7, 0.26)
        leave = arr([3.0, 0.4], [0.6, 0.4], ORANGE, 7, 0.26)
        bl = lab("binding", 32, YELLOW).move_to([4.8, 1.15, 0])
        ll = lab("release", 32, ORANGE).move_to([4.8, 0.4, 0])
        # a slight wobble of free dots
        self.play(GrowArrow(bind), GrowArrow(leave), FadeIn(bl), FadeIn(ll), run_time=0.6)

        self.at("That is equilibrium")
        # exchange: one leaves a cup, another enters an empty cup (equal rates)
        self.play(free[0].animate.move_to([-5.0, 0.2, 0]), free[1].animate.move_to([sites[4][0], sites[4][1], 0]), run_time=0.9)
        eqs = lab("binding = release", 28, WHITE).move_to([3.9, 0.0, 0])
        # equation
        num = VGroup(M("[L]", 40, ORANGE), M("[R]", 40, PURPLE)).arrange(RIGHT, buff=0.16)
        den = M("[LR]", 40, YELLOW)
        bar = Line(LEFT * 0.7, RIGHT * 0.7, color=WHITE, stroke_width=3)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.12)
        kd = M("Kd =", 42, WHITE)
        eq = VGroup(kd, frac).arrange(RIGHT, buff=0.3).move_to([3.4, 2.3, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.7)
        self.at("is ligand")
        self.play(Indicate(num[0], color=ORANGE, scale_factor=1.3), run_time=0.5)
        self.at("times receptor")
        self.play(Indicate(num[1], color=PURPLE, scale_factor=1.3), run_time=0.5)
        self.at("over the complex")
        self.play(Indicate(den, color=YELLOW, scale_factor=1.3), run_time=0.5)

        self.at("Tight binders take")
        self.play(FadeOut(bind), FadeOut(leave), FadeOut(bl), FadeOut(ll), run_time=0.3)
        ax = axes(3.6, -1.35, 5.2, 3.3, (0, 6, 1), (0, 1.25, 1))
        xl = lab("time", 24).next_to(ax, DOWN, buff=0.12)
        yl = lab("bound", 24).rotate(PI / 2).next_to(ax, LEFT, buff=0.12)
        fast = curve(ax, lambda t: 1 - np.exp(-2.2 * t), 0, 6, GREY, 5)
        slow = curve(ax, lambda t: 1 - np.exp(-0.7 * t), 0, 6, YELLOW, 5)
        plat = dash_h(ax, 1.0, 0, 6, GREY)
        fl = lab("loose binder", 26, GREY).move_to(ax.c2p(1.6, 1.13))
        sl = lab("tight binder", 26, YELLOW).move_to(ax.c2p(4.3, 0.62))
        ide = tagline(IDEAL, ax.c2p(4.3, 0.22))
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ide), run_time=0.5)
        self.play(Create(plat), Create(fast), FadeIn(fl), run_time=0.7)
        self.play(Create(slow, run_time=1.2, rate_func=linear), FadeIn(sl))
        self.finish()


# ---------------------------------------------------------------------------------------------
class Panel:
    """One filter panel in local coordinates around (cx, 0). Built from pieces so scenes can animate each."""

    def __init__(self, cx, title):
        self.cx = cx
        self.title_text = title
        self.slab = Rectangle(width=5.6, height=0.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                              fill_opacity=0.5).move_to([cx, 0.2, 0])
        self.slab_lbl = lab("filter", 26, TEAL).move_to([cx + 3.55, 0.2, 0])
        # membranes land on the slab; start 1.7 higher
        self.fr_final = [frag(cx - 1.5, 0.4, 2.3, 2, 1.5), frag(cx + 1.5, 0.4, 2.3, 2, 1.5)]
        top = self.fr_final[0].top
        self.sites = [s for f in self.fr_final for s in f.sites]
        self.ns_pos = [(cx - 1.5 + 0.95, top + 0.16), (cx + 1.5 - 0.95, top + 0.16)]
        self.title = lab(title, 28, WHITE).move_to([cx, -3.4, 0])
        self.base = -2.95
        self.cols = None


class S03Separate(SpokenScene):
    """filter, wash, count = total; excess unlabelled ligand takes the label off the sites = nonspecific; subtract."""

    def construct(self):
        rng = np.random.RandomState(7)
        UP_ = 1.9
        cxA = 0.0
        A = Panel(cxA, "total binding")
        # mixture (above the slab): membranes with specific dots + two nonspecific dots + free dots
        frA = VGroup(*[f.copy() for f in A.fr_final]).shift(UP * UP_)
        spec = VGroup(*[dot(s[0], s[1] + UP_, ORANGE, 0.15) for s in A.sites])
        ns = VGroup(*[dot(x, y + UP_, ORANGE, 0.15) for (x, y) in A.ns_pos])
        free_pos = [(-2.6, 2.9), (-1.7, 2.0), (-0.5, 3.0), (0.4, 2.2), (1.4, 3.0), (2.2, 2.1), (2.7, 2.9), (-2.3, 2.4)]
        free = VGroup(*[dot(x, y, ORANGE, 0.15) for x, y in free_pos])
        mixlbl = lab("labelled ligand\nand membranes", 26, GREY).move_to([-5.3, 2.4, 0])
        # the filter apparatus label
        self.at("pull the mixture")
        self.play(FadeIn(A.slab), FadeIn(A.slab_lbl), run_time=0.4)
        self.play(FadeIn(frA), FadeIn(spec), FadeIn(ns), FadeIn(free), FadeIn(mixlbl), run_time=0.6)
        self.at("traps the membranes")
        thru = [0, 1, 3, 4, 6]
        stay = [2, 5, 7]
        land = [frA.animate.shift(DOWN * UP_), spec.animate.shift(DOWN * UP_), ns.animate.shift(DOWN * UP_)]
        pass_dots = [free[i].animate.move_to([free_pos[i][0], -0.5 - 0.25 * k, 0]) for k, i in enumerate(thru)]
        stay_dots = [free[i].animate.move_to([free_pos[i][0], 1.0 + 0.2 * k, 0]) for k, i in enumerate(stay)]
        self.play(FadeOut(mixlbl), *land, *pass_dots, *stay_dots, FadeIn(waste_lbl := lab("passes through", 26, GREY).move_to([cxA + 4.3, -0.6, 0])), run_time=1.3)

        self.at("Wash it several")
        drops = VGroup(*[Dot(point=[-2.4 + 0.8 * i, 2.4 - 0.4 * (i % 2), 0], radius=0.07, color=TEAL) for i in range(7)])
        self.play(FadeIn(drops), run_time=0.3)
        self.play(*[d.animate.shift(DOWN * 3.4) for d in drops], *[free[i].animate.shift(DOWN * 2.2) for i in stay],
                  run_time=1.0)
        self.at("so unbound label goes")
        self.play(FadeOut(drops), FadeOut(VGroup(*[free[i] for i in range(8)])), FadeOut(waste_lbl), run_time=0.6)

        self.at("Count the radioactivity")
        u = 1.45 / 1.0
        nsh, sph = 0.45, 1.15
        axl = Line([cxA - 1.0, A.base, 0], [cxA + 1.0, A.base, 0], color=GREY, stroke_width=3)
        b_ns = Rectangle(width=0.9, height=nsh, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([cxA, A.base + nsh / 2, 0])
        b_sp = Rectangle(width=0.9, height=sph, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([cxA, A.base + nsh + sph / 2, 0])
        cnt = lab("counts", 26, GREY).move_to([cxA + 1.8, A.base + 0.5, 0])
        tot = Rectangle(width=0.9, height=nsh + sph, stroke_width=0, fill_color=WHITE, fill_opacity=0.9).move_to([cxA, A.base + (nsh + sph) / 2, 0])
        self.play(Create(axl), FadeIn(tot), FadeIn(cnt), run_time=0.9)
        self.at("That is total")
        br = Brace(tot, direction=LEFT, color=WHITE, buff=0.12)
        self.play(FadeIn(br), FadeIn(A.title), run_time=0.6)

        # ---------------- panel B: the same, with excess unlabelled ligand
        self.at("Repeat with a large")
        cxB, cxA2 = 3.4, -3.4
        grpA = Group(A.slab, A.slab_lbl, frA, spec, ns, axl, tot, cnt, br, A.title)
        b_ns.shift(LEFT * 3.4); b_sp.shift(LEFT * 3.4)
        A.slab_lbl.set_opacity(0)
        self.play(grpA.animate.shift(LEFT * 3.4), FadeOut(cnt), run_time=0.8)
        B = Panel(cxB, "with excess unlabelled ligand")
        frB = VGroup(*[f.copy() for f in B.fr_final])
        specB = VGroup(*[dot(s[0], s[1], ORANGE, 0.15) for s in B.sites])
        nsB = VGroup(*[dot(x, y, ORANGE, 0.15) for (x, y) in B.ns_pos], dot(cxB - 0.35, 0.4, ORANGE, 0.12), dot(cxB + 0.2, 0.4, ORANGE, 0.12))
        self.play(FadeIn(B.slab), FadeIn(frB), FadeIn(specB), FadeIn(nsB), FadeIn(B.title), run_time=0.7)
        cold_pos = [(cxB - 2.3, 2.3), (cxB - 1.4, 1.5), (cxB - 0.6, 2.4), (cxB + 0.3, 1.7), (cxB + 1.0, 2.5), (cxB + 1.8, 1.6), (cxB + 2.4, 2.3), (cxB - 0.9, 1.1)]
        cold = VGroup(*[dot(x, y, BLUE, 0.17) for x, y in cold_pos])
        cold_lbl = lab("unlabelled ligand, large excess", 26, BLUE).move_to([cxB + 0.2, 3.25 - 0.0, 0])
        cold_lbl.move_to([cxB, 3.2, 0])
        self.play(FadeIn(cold, shift=DOWN * 0.3), FadeIn(cold_lbl), run_time=0.7)

        self.at("which competes the label off")
        # blue dots take the cups, orange dots leave and pass through the filter
        mv = []
        for k, s in enumerate(B.sites):
            mv.append(cold[k].animate.move_to([s[0], s[1], 0]))
            mv.append(specB[k].animate.move_to([s[0] + (0.4 if k % 2 else -0.4), -0.7 - 0.2 * k, 0]))
        self.play(*mv, run_time=1.6)
        self.at("What still counts")
        axB = Line([cxB - 1.0, B.base, 0], [cxB + 1.0, B.base, 0], color=GREY, stroke_width=3)
        b_nsB = Rectangle(width=0.9, height=nsh, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([cxB, B.base + nsh / 2, 0])
        self.play(FadeOut(specB), FadeOut(cold_lbl), Create(axB), FadeIn(b_nsB), run_time=0.8)
        nsl = lab("nonspecific", 26, RED).move_to([cxB + 2.0, B.base + 0.3, 0])
        self.play(FadeIn(nsl), run_time=0.4)

        self.at("Total minus nonspecific")
        head = M("specific = total − nonspecific", 32, WHITE).move_to([0, 3.35, 0])
        self.play(FadeIn(head), FadeOut(tot), FadeIn(b_ns), FadeIn(b_sp), run_time=0.7)
        self.play(Indicate(b_ns, color=RED, scale_factor=1.3), run_time=0.4)
        self.at("is specific binding")
        self.play(Indicate(b_sp, color=YELLOW, scale_factor=1.15), head.animate.set_color(YELLOW), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Curves(SpokenScene):
    """saturation (Bmax, Kd) and competition (IC50 -> Ki) as curves from equations."""

    def construct(self):
        L = axes(-3.3, 0.15, 5.4, 4.3, (-3, 3, 1), (0, 1.12, 1))
        R = axes(3.3, 0.15, 5.4, 4.3, (-3, 3, 1), (0, 1.12, 1))
        tl = lab("saturation", 32, WHITE).move_to([-3.3, 2.85, 0])
        tr = lab("competition", 32, WHITE).move_to([3.3, 2.85, 0])
        xl = lab("labelled ligand added (log scale)", 24).move_to([-3.3, -2.85, 0])
        yl = lab("specific binding", 24).rotate(PI / 2).move_to([-6.55, 0.15, 0])
        xr = lab("unlabelled compound added (log scale)", 24).move_to([3.3, -2.85, 0])
        yr = lab("labelled ligand bound", 24).rotate(PI / 2).move_to([0.05, 0.15, 0])
        ide1 = tagline(IDEAL, L.c2p(1.9, 0.12))
        ide2 = tagline(IDEAL, R.c2p(1.9, 0.33))

        self.at("In saturation")
        self.play(Create(L), FadeIn(tl), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.play(FadeIn(ide1), run_time=0.2)
        self.at("raise the")
        s = curve(L, sat, -3, 3, YELLOW, 6)
        self.play(Create(s, run_time=1.6, rate_func=linear))
        self.at("levels off")
        bmax = dash_h(L, 1.0, -3, 3, YELLOW)
        bl = M("Bmax", 30, YELLOW).move_to(L.c2p(-2.3, 1.08))
        self.play(Create(bmax), FadeIn(bl), run_time=0.6)
        self.at("half maximal")
        hv = dash_v(L, 0, 0, 0.5, YELLOW)
        hh = dash_h(L, 0.5, -3, 0, YELLOW)
        kd = M("Kd", 28, YELLOW).move_to(L.c2p(0.0, -0.1) + DOWN * 0.0)
        kd.move_to(L.c2p(0.0, 0) + DOWN * 0.32)
        self.play(Create(hh), Create(hv), FadeIn(kd), run_time=0.7)

        self.at("In competition")
        self.play(Create(R), FadeIn(tr), FadeIn(xr), FadeIn(yr), FadeIn(ide2), run_time=0.8)
        self.at("hold the label fixed")
        fixed = chip("label fixed", ORANGE, 24).move_to(R.c2p(-1.9, 0.27))
        self.play(FadeIn(fixed, shift=DOWN * 0.1), run_time=0.5)
        self.at("add rising")
        c = curve(R, lambda x: 1.0 / (1.0 + 10.0 ** x), -3, 3, BLUE, 6)
        self.play(Create(c, run_time=1.6, rate_func=linear))
        self.at("is calculated")
        mv = dash_v(R, 0, 0, 0.5, BLUE)
        mh = dash_h(R, 0.5, -3, 0, BLUE)
        ic = M("IC50", 28, BLUE).move_to(R.c2p(0, 0) + DOWN * 0.32)
        self.play(Create(mh), Create(mv), FadeIn(ic), run_time=0.7)
        self.at("halves binding")
        hb = lab("halves binding", 24, BLUE).move_to(R.c2p(1.5, 0.62))
        self.play(FadeIn(hb), run_time=0.4)
        self.at("with the Cheng")
        f1 = M("Ki = IC50 / (1 + [L] / Kd)", 28, WHITE).move_to([3.3, -3.3, 0])
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """idealised worked example: bars 66, 18, 48 -> 60 fmol/mg; then total / nonspecific / specific vs concentration."""

    def construct(self):
        base = -2.2
        k = 0.052
        tag = tagline("idealised example", [-2.4, 3.2], 26)
        ground = Line([-6.2, base, 0], [1.2, base, 0], color=GREY, stroke_width=3)

        def bar(x, v, color, label, name):
            r = Rectangle(width=1.5, height=v * k, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, base + v * k / 2, 0])
            vl = M(label, 30, color).next_to(r, UP, buff=0.12)
            nl = lab(name, 24, color).move_to([x, base - 0.45, 0])
            return r, vl, nl

        t = bar(-5.1, 66, WHITE, "66 fmol", "total")
        n = bar(-2.7, 18, RED, "18 fmol", "nonspecific")
        s = bar(-0.3, 48, YELLOW, "48 fmol", "specific")
        n[2].become(lab("with excess\nunlabelled", 24, RED, line_spacing=0.6).move_to([-2.7, base - 0.55, 0]))

        self.at("idealized example")
        self.play(FadeIn(tag), Create(ground), run_time=0.5)
        self.at("of protein bind")
        info = VGroup(M("0.80 mg", 36, WHITE), lab("of protein", 28, GREY)).arrange(DOWN, buff=0.12).move_to([4.1, 1.7, 0])
        self.play(FadeIn(info, shift=LEFT * 0.2), run_time=0.5)
        self.at("in total")
        self.play(GrowFromEdge(t[0], DOWN), FadeIn(t[1]), FadeIn(t[2]), run_time=0.9)
        self.at("of unlabeled")
        self.play(GrowFromEdge(n[0], DOWN), FadeIn(n[1]), FadeIn(n[2]), run_time=0.9)
        self.at("Specific binding is")
        ghost = DashedVMobject(Rectangle(width=1.5, height=18 * k, stroke_color=RED, stroke_width=3).move_to([-0.3, base + 9 * k, 0]))
        self.play(GrowFromEdge(s[0], DOWN), FadeIn(s[1]), FadeIn(s[2]), run_time=0.9)
        self.at("receptor per milligram")
        res = VGroup(M("48 fmol ÷ 0.80 mg", 30, WHITE), M("= 60 fmol per mg", 34, YELLOW)).arrange(DOWN, buff=0.18).move_to([4.1, -0.3, 0])
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.7)

        # ------ plot phase
        self.at("Across concentrations")
        old = Group(tag, ground, *t, *n, *s, info, res)
        self.play(FadeOut(old), run_time=0.5)
        ax = axes(0.2, 0.3, 10.4, 5.1, (-2, 2, 1), (0, 1.95, 1))
        xl = lab("concentration of labelled ligand (log scale)", 26).move_to([0.2, -3.3, 0])
        yl = lab("counts", 26).rotate(PI / 2).move_to([-5.4, 0.3, 0])
        ide = tagline(IDEAL, [5.0, 3.2], 26)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ide), run_time=0.7)
        nsf = lambda x: 0.008 * 10.0 ** x
        spf = lambda x: sat(x)
        cn = curve(ax, nsf, -2, 2, RED, 5)
        cs = curve(ax, spf, -2, 2, YELLOW, 6)
        ct = curve(ax, lambda x: nsf(x) + spf(x), -2, 2, WHITE, 5)
        self.at("nonspecific binding usually")
        self.play(Create(cn, run_time=1.2, rate_func=linear))
        nlbl = lab("nonspecific", 26, RED).move_to(ax.c2p(1.2, 0.42))
        tlbl = lab("total", 26, WHITE).move_to(ax.c2p(1.0, 1.75))
        slbl = lab("specific", 26, YELLOW).move_to(ax.c2p(-1.35, 0.5))
        self.play(FadeIn(nlbl), run_time=0.3)
        self.at("while specific binding saturates")
        self.play(Create(cs, run_time=1.4, rate_func=linear), FadeIn(slbl))
        self.play(Create(ct, run_time=0.8, rate_func=linear), FadeIn(tlbl))

        self.at("percent occupancy takes")
        self.play(FadeOut(VGroup(cn, ct, nlbl, tlbl)), run_time=0.5)
        lo, hi = -np.log10(9), np.log10(9)
        p1 = dot(*ax.c2p(lo, sat(lo))[:2], WHITE, 0.14)
        p2 = dot(*ax.c2p(hi, sat(hi))[:2], WHITE, 0.14)
        l1 = M("10%", 28, WHITE).next_to(p1, UL, buff=0.12)
        l2 = M("90%", 28, WHITE).next_to(p2, DL, buff=0.12)
        v1 = dash_v(ax, lo, 0, sat(lo), WHITE)
        v2 = dash_v(ax, hi, 0, sat(hi), WHITE)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(l1), FadeIn(l2), Create(v1), Create(v2), run_time=0.8)
        span = DoubleArrow(ax.c2p(lo, 0.0) + DOWN * 0.3, ax.c2p(hi, 0.0) + DOWN * 0.3, buff=0, color=GOLD, stroke_width=4, tip_length=0.2)
        sp_l = M("81-fold", 28, GOLD).next_to(span, DOWN, buff=0.08)
        self.at("so the axis is logarithmic")
        self.play(GrowFromCenter(span), FadeIn(sp_l), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """binding is not response (spare receptors, EC50 below Kd; control: measure Kd by binding); depletion; too short."""

    def construct(self):
        # ---- phase 1: most receptors empty, full response
        mem = RoundedRectangle(width=12.2, height=0.4, corner_radius=0.14, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to([0, 0.5, 0])
        xs = np.linspace(-5.5, 5.5, 12)
        recs = VGroup(*[Rec(x, 0.7, 2.6) for x in xs])
        occupied = [2, 6, 9]
        dots = VGroup(*[dot(recs[i].site[0], recs[i].site[1], ORANGE, 0.26) for i in occupied])
        # response meter
        track = Rectangle(width=11.0, height=0.9, stroke_color=GREEN, stroke_width=3, fill_opacity=0).move_to([0, -2.4, 0])
        fillb = Rectangle(width=11.0, height=0.9, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([0, -2.4, 0])
        ml = lab("response", 34, GREEN).move_to([0, -1.5, 0])
        self.at("Binding is not response")
        self.play(FadeIn(mem), FadeIn(recs), run_time=0.7)
        self.play(FadeIn(dots), run_time=0.4)
        self.play(Create(track), FadeIn(ml), run_time=0.4)
        self.at("full response with")
        self.play(GrowFromEdge(fillb, LEFT), run_time=1.2)
        self.at("most receptors empty")
        emp = lab("most receptors empty", 40, PURPLE).move_to([0, 2.9, 0])
        self.play(FadeIn(emp, shift=DOWN * 0.1), run_time=0.5)

        # ---- phase 2: the two curves
        self.at("These spare receptors")
        self.play(FadeOut(Group(mem, recs, dots, track, fillb, ml, emp)), run_time=0.5)
        ax = axes(0.0, 0.25, 10.0, 5.0, (-3, 3, 1), (0, 1.12, 1))
        xl = lab("concentration of ligand (log scale)", 26).move_to([0, -3.3, 0])
        yl = lab("fraction of maximum", 26).rotate(PI / 2).move_to([-5.45, 0.25, 0])
        ide = tagline(IDEAL, [4.6, 3.1], 26)
        occ = curve(ax, sat, -3, 3, YELLOW, 6)
        rsp = curve(ax, lambda x: min(1.0, (sat(x)) / 0.05), -3, 3, GREEN, 6)
        occl = lab("binding", 28, YELLOW).move_to(ax.c2p(1.9, 0.78))
        rspl = lab("response", 28, GREEN).move_to(ax.c2p(-2.3, 0.8))
        ill = tagline("illustrative", ax.c2p(-2.3, 0.64), 24)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ide), run_time=0.6)
        self.play(Create(occ, run_time=0.7, rate_func=linear), FadeIn(occl))
        self.play(Create(rsp, run_time=0.7, rate_func=linear), FadeIn(rspl), FadeIn(ill))
        self.at("half the maximum response")
        e = np.log10(1.0 / 39.0)
        hh = dash_h(ax, 0.5, -3, 0, GREEN)
        ev = dash_v(ax, e, 0, 0.5, GREEN)
        el = M("EC50", 28, GREEN).move_to(ax.c2p(e, 0) + DOWN * 0.35)
        self.play(Create(hh), Create(ev), FadeIn(el), run_time=0.7)
        kv = dash_v(ax, 0, 0, 0.5, YELLOW)
        kl = M("Kd", 28, YELLOW).move_to(ax.c2p(0, 0) + DOWN * 0.35)
        self.at("below Kd")
        self.play(Create(kv), FadeIn(kl), run_time=0.6)
        gap = DoubleArrow(ax.c2p(e, 0.56), ax.c2p(0, 0.56), buff=0, color=WHITE, stroke_width=4, tip_length=0.2)
        self.play(GrowFromCenter(gap), run_time=0.5)
        self.at("measure Kd by binding")
        self.play(Indicate(kl, color=YELLOW, scale_factor=1.4), Indicate(occl, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.at("and compare")
        cmp_ = lab("compare", 28, WHITE).next_to(gap, UP, buff=0.08)
        self.play(FadeIn(cmp_), Indicate(el, color=GREEN, scale_factor=1.4), run_time=0.7)

        # ---- phase 3: depletion
        self.at("take up much of the label")
        self.play(FadeOut(Group(ax, xl, yl, occ, rsp, occl, rspl, ill, hh, ev, el, kv, kl, gap, cmp_)), run_time=0.5)
        # left: label bar; right: steepened curve
        x0 = -4.7
        bt = Rectangle(width=1.7, height=4.4, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.25).move_to([x0, -0.1, 0])
        taken = Rectangle(width=1.7, height=3.0, stroke_width=0, fill_color=PURPLE, fill_opacity=0.8).move_to([x0, -0.1 - 2.2 + 1.5, 0])
        bl = lab("label added", 26, ORANGE).move_to([x0, 2.55, 0])
        tl = lab("taken up by\nreceptors", 24, PURPLE, line_spacing=0.6).move_to([x0 + 2.5, -1.2, 0])
        ax2 = axes(2.6, 0.0, 6.2, 4.4, (-3, 3, 1), (0, 1.12, 1))
        x2 = lab("ligand (log scale)", 24).move_to([2.6, -2.6, 0])
        norm = curve(ax2, sat, -3, 3, YELLOW, 5)
        steep = curve(ax2, lambda x: 1 / (1 + 10 ** (-1.8 * x)), -3, 3, RED, 6)
        nl = lab("expected", 24, YELLOW).move_to(ax2.c2p(-2.0, 0.45))
        sl = lab("steeper", 24, RED).move_to(ax2.c2p(1.7, 0.2))
        ide2 = tagline(IDEAL, [2.6, -3.1], 24)
        self.play(FadeIn(bt), FadeIn(bl), FadeIn(taken, shift=UP * 0.2), FadeIn(tl), run_time=0.7)
        self.play(Create(ax2), FadeIn(x2), FadeIn(ide2), Create(norm), run_time=0.7)
        self.at("curves steepen")
        self.play(Create(steep, run_time=0.7, rate_func=linear), FadeIn(nl), FadeIn(sl))
        self.at("keep depletion under")
        self.play(FadeOut(Group(tl, taken)), run_time=0.4)
        small = Rectangle(width=1.7, height=0.44, stroke_width=0, fill_color=PURPLE, fill_opacity=0.8).move_to([x0, -0.1 - 2.2 + 0.22, 0])
        ok = lab("under about 10%\nof the label", 26, GREEN, line_spacing=0.6).move_to([x0 + 2.7, -1.5, 0])
        self.play(FadeIn(small), FadeIn(ok), FadeOut(steep), FadeOut(sl), run_time=0.6)

        # ---- phase 4: too short
        self.at("too short an incubation")
        self.play(FadeOut(Group(bt, bl, small, ok, ax2, x2, norm, nl, ide2)), run_time=0.5)
        ax3 = axes(0.0, 0.0, 10.0, 5.0, (0, 6, 1), (0, 1.2, 1))
        x3 = lab("incubation time", 26).move_to([0, -3.1, 0])
        y3 = lab("bound", 26).rotate(PI / 2).move_to([-5.45, 0, 0])
        full = curve(ax3, lambda t: 1 - np.exp(-0.8 * t), 0, 6, GREY, 5)
        plat = dash_h(ax3, 1.0, 0, 6, GREY)
        pl = lab("equilibrium", 26, GREY).move_to(ax3.c2p(5.0, 1.1))
        part = curve(ax3, lambda t: 1 - np.exp(-0.8 * t), 0, 1.6, YELLOW, 7)
        stop = dash_v(ax3, 1.6, 0, 1.2, RED)
        stl = lab("stopped here", 26, RED).move_to(ax3.c2p(2.35, 0.1))
        lvl = dash_h(ax3, 1 - np.exp(-0.8 * 1.6), 0, 1.6, RED)
        ide3 = tagline(IDEAL, [4.6, 3.1], 26)
        self.play(Create(ax3), FadeIn(x3), FadeIn(y3), FadeIn(ide3), run_time=0.5)
        self.play(Create(plat), Create(full), FadeIn(pl), run_time=0.8)
        self.play(Create(part, run_time=0.8, rate_func=linear), Create(stop), Create(lvl), FadeIn(stl))
        self.finish()


# ---------------------------------------------------------------------------------------------
def membrane_row(cx, y, w, n, s=1.0, cups=True):
    bar = RoundedRectangle(corner_radius=0.1, width=w, height=0.3, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.4).move_to([cx, y, 0])
    xs = [cx + (i - (n - 1) / 2) * (w / n) for i in range(n)]
    recs = [Rec(x, y + 0.15, s) for x in xs] if cups else []
    g = VGroup(bar, *recs)
    g.sites = [r.site for r in recs]
    return g


def head(year, who):
    y = T(year, 64, GOLD, weight=BOLD).move_to([-4.9, 3.0, 0])
    w = lab(who, 28, GOLD).move_to([-4.9 + 0.0, 2.25, 0])
    w.align_to([-6.3, 0, 0], LEFT)
    y.align_to([-6.3, 0, 0], LEFT)
    return VGroup(y, w)


class S07Origin(SpokenScene):
    """1970 ACTH labelled and bound, inhibition tracks activity; 1973 naloxone saturable, 30 pmol/g, Kd 20 nM, 15 compete."""

    def construct(self):
        SH = 3.2   # the left cluster starts centred and slides left when the plot comes in
        # ---------- 1970
        h1 = head("1970", "Lefkowitz et al.")
        mem1 = membrane_row(-3.2, -0.9, 5.8, 4, 2.6)
        chip1 = chip("radioactive ACTH", ORANGE, 34).move_to([-3.2, 1.3, 0])
        lbl1 = lab("adrenal extract", 32, GREY).move_to([-3.2, -1.6, 0])
        d1 = VGroup(*[dot(s[0], s[1], ORANGE, 0.26) for s in mem1.sites[:3]])
        left1 = Group(mem1, chip1, lbl1, d1).shift(RIGHT * SH)
        ax1 = axes(3.4, -0.25, 5.2, 4.0, (0, 6, 1), (0, 6, 1))
        pts = [(0.6, 0.7), (1.5, 1.7), (2.4, 2.4), (3.3, 3.5), (4.4, 4.2), (5.4, 5.3)]
        sc1 = VGroup(*[Dot(ax1.c2p(a, b), radius=0.13, color=BLUE) for a, b in pts])
        ln1 = DashedLine(ax1.c2p(0.2, 0.3), ax1.c2p(5.8, 5.6), color=GREY, stroke_width=3, dash_length=0.12)
        x1 = lab("biological activity", 26).move_to([3.4, -2.6, 0])
        yl1 = lab("inhibition of binding", 26).rotate(PI / 2).move_to([0.55, -0.25, 0])
        sch1 = tagline("schematic, not the paper's data", [3.4, -3.15], 24)
        tit1 = lab("unlabelled ACTH and five derivatives", 26, BLUE).move_to([3.4, 2.3, 0])

        self.at("Lefkowitz and colleagues")
        self.play(FadeIn(h1), FadeIn(mem1), FadeIn(lbl1), run_time=0.6)
        self.play(FadeIn(chip1, shift=DOWN * 0.1), run_time=0.5)
        self.at("Adrenal extracts bound")
        self.play(FadeIn(d1, shift=DOWN * 0.8), run_time=0.9)
        self.at("five derivatives")
        self.play(left1.animate.shift(LEFT * SH), FadeIn(ax1), FadeIn(x1), FadeIn(yl1), FadeIn(sch1), FadeIn(tit1), run_time=0.8)
        self.play(*[FadeIn(p, scale=1.6) for p in sc1], run_time=0.7)
        self.at("in proportion to")
        self.play(Create(ln1), run_time=0.7)

        # ---------- 1973
        self.at("In 1973 Pert")
        old = Group(h1, left1, ax1, sc1, ln1, x1, yl1, sch1, tit1)
        self.play(FadeOut(old), run_time=0.5)
        h2 = head("1973", "Pert and Snyder")
        mem2 = membrane_row(-3.2, -0.9, 5.8, 4, 2.6)
        chip2 = chip("tritiated naloxone", ORANGE, 34).move_to([-3.2, 1.3, 0])
        lbl2 = lab("rat brain", 32, GREY).move_to([-3.2, -1.6, 0])
        d2 = VGroup(*[dot(s[0], s[1], ORANGE, 0.26) for s in mem2.sites])
        left2 = Group(mem2, chip2, lbl2, d2).shift(RIGHT * SH)
        ax2 = axes(3.4, -0.25, 5.2, 4.0, (-3, 3, 1), (0, 1.12, 1))
        s2 = curve(ax2, sat, -3, 3, YELLOW, 6)
        bm = dash_h(ax2, 1.0, -3, 3, YELLOW)
        den = M("30 pmol/g", 28, YELLOW).move_to(ax2.c2p(-1.8, 1.0) + UP * 0.3)
        hv = dash_v(ax2, 0, 0, 0.5, YELLOW)
        hh = dash_h(ax2, 0.5, -3, 0, YELLOW)
        kd = M("Kd 20 nM", 28, YELLOW).move_to(ax2.c2p(1.35, 0.0) + UP * 0.45)
        x2 = lab("naloxone added (log scale)", 26).move_to([3.4, -2.6, 0])
        yl2 = lab("specific binding", 26).rotate(PI / 2).move_to([0.55, -0.25, 0])
        sch2 = tagline("schematic curve", ax2.c2p(-1.5, 0.72), 24)
        self.play(FadeIn(h2), FadeIn(mem2), FadeIn(lbl2), FadeIn(chip2), run_time=0.7)
        self.at("rat brain")
        self.play(FadeIn(d2, shift=DOWN * 0.8), run_time=0.7)
        self.at("Binding was saturable")
        self.play(left2.animate.shift(LEFT * SH), FadeIn(ax2), FadeIn(x2), FadeIn(yl2), FadeIn(sch2), Create(s2, run_time=1.2, rate_func=linear))
        self.at("nanomolar")
        self.play(Create(hh), Create(hv), FadeIn(kd), run_time=0.6)
        self.at("density of")
        self.play(Create(bm), FadeIn(den), run_time=0.6)
        self.at("Fifteen opiates")
        c15 = chip("15 opiates and antagonists\ncompete", BLUE, 28).move_to([-3.2, 1.3, 0])
        self.play(FadeOut(chip2), FadeIn(c15), run_time=0.6)
        self.finish()


class S08Unlocked(SpokenScene):
    """1975 enkephalins found by displacement; 1974 FH binding defect; the rule."""

    def construct(self):
        SH = 3.2
        # ---------- 1975
        mem1 = membrane_row(-3.2, -1.25, 5.8, 3, 2.8)
        site = mem1.sites[1]
        lbl1 = lab("brain membrane", 32, GREY).move_to([-3.2, -1.95, 0])
        plant = chip("plant drug", ORANGE, 34).move_to([-3.2, 1.6, 0])
        d1 = dot(site[0], site[1], ORANGE, 0.3)
        pep = chip("enkephalins: two pentapeptides", BLUE, 28).move_to([-3.2, 1.6, 0])
        site2 = mem1.sites[2]
        link = arr([-3.2 + 1.25, 1.2], [site2[0] + 0.0, site2[1] + 0.7], BLUE, 6, 0.24)
        left1 = Group(mem1, lbl1, d1, pep, link).shift(RIGHT * SH)
        site2 = site2 + np.array([SH, 0, 0])
        pdot = dot(site2[0], site2[1], BLUE, 0.3)
        nat = VGroup(lab("proposed natural ligands for", 36, BLUE), lab("opiate receptors", 36, BLUE),
                     lab("sequenced, then synthesised", 28, GREY)).arrange(DOWN, buff=0.25).move_to([3.4, 0.2, 0])

        self.at("A binding site for")
        self.play(FadeIn(mem1), FadeIn(lbl1), FadeIn(plant.shift(RIGHT * SH)), run_time=0.6)
        self.play(plant.animate.move_to([site[0] + SH, site[1] + 0.8, 0]).scale(0.8), run_time=0.5)
        self.play(FadeOut(plant), FadeIn(d1), run_time=0.4)
        self.at("In 1975 Hughes")
        h1 = head("1975", "Hughes, Kosterlitz et al.")
        self.play(FadeIn(h1), run_time=0.5)
        self.at("two pentapeptides")
        self.play(FadeIn(pep, shift=DOWN * 0.1), run_time=0.5)
        self.at("the enkephalins")
        self.play(GrowArrow(link), FadeIn(pdot), run_time=0.5)
        self.play(left1.animate.shift(LEFT * SH), pdot.animate.shift(LEFT * SH), FadeIn(nat), run_time=0.8)

        # ---------- 1974
        self.at("In 1974 Brown")
        old = Group(left1, pdot, nat, h1)
        self.play(FadeOut(old), run_time=0.5)
        h2 = head("1974", "Brown and Goldstein")
        nm = membrane_row(-3.2, 0.5, 5.0, 3, 2.0)
        nd = VGroup(*[dot(s[0], s[1], ORANGE, 0.23) for s in nm.sites])
        nl = lab("normal fibroblasts", 30, YELLOW).move_to([-3.2, -0.1, 0])
        fm = membrane_row(-3.2, -1.8, 5.0, 0, 1.0, cups=False)
        fd = VGroup(*[dot(-3.2 + dx, -1.8 + dy, ORANGE, 0.23) for dx, dy in [(-1.6, 0.6), (0.0, 0.9), (1.5, 0.5)]])
        fl = lab("five homozygous subjects", 30, RED).move_to([-3.2, -2.45, 0])
        ldl = chip("labelled LDL", ORANGE, 30).move_to([3.4, 2.5, 0])
        leftn = Group(nm, nd, nl).shift(RIGHT * SH)
        ax2 = axes(3.4, -0.25, 5.2, 3.9, (0, 6, 1), (0, 1.12, 1))
        cn = curve(ax2, lambda t: 1 - np.exp(-0.9 * t), 0, 6, YELLOW, 6)
        cf = poly([ax2.c2p(0, 0.04), ax2.c2p(6, 0.1)], RED, 6)
        x2 = lab("labelled LDL added", 24).move_to([3.4, -2.5, 0])
        yl2 = lab("high-affinity LDL binding", 22).rotate(PI / 2).move_to([0.55, -0.25, 0])
        sch2 = tagline("schematic", [5.0, -1.5], 24)
        self.play(FadeIn(h2), run_time=0.5)
        self.at("normal fibroblasts bound")
        self.play(FadeIn(nm), FadeIn(nl), FadeIn(nd, shift=DOWN * 0.5), FadeIn(ldl), run_time=0.8)
        self.play(leftn.animate.shift(LEFT * SH), FadeIn(ax2), FadeIn(x2), FadeIn(yl2), FadeIn(sch2), Create(cn, run_time=1.0, rate_func=linear))
        self.at("cells from five")
        self.play(FadeIn(fm), FadeIn(fl), FadeIn(fd, shift=DOWN * 0.4), run_time=0.7)
        self.play(Create(cf, run_time=0.8, rate_func=linear))
        self.at("binding defect")
        dfx = lab("binding defect may account for\nthe cells' cholesterol overproduction", 24, RED, line_spacing=0.6).move_to([3.4, -3.15, 0])
        self.play(FadeIn(dfx), run_time=0.5)

        # ---------- the rule
        self.at("Binding counts sites")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        r = Rec(-3.2, 0.2, 3.0)
        cupm = RoundedRectangle(width=2.0, height=0.4, corner_radius=0.12, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.4).move_to([-3.2, 0.0, 0])
        rd = dot(r.site[0], r.site[1], ORANGE, 0.32)
        ol = lab("occupancy", 36, ORANGE).move_to([-3.2, 2.9, 0])
        neq = T("≠", 100, WHITE, weight=BOLD).move_to([0, 1.0, 0])
        track = Rectangle(width=4.6, height=0.95, stroke_color=GREEN, stroke_width=3, fill_opacity=0).move_to([3.3, 1.0, 0])
        fillb = Rectangle(width=4.6, height=0.95, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([3.3, 1.0, 0])
        rl = lab("response", 36, GREEN).move_to([3.3, 2.2, 0])
        t1 = T("Binding counts sites and measures grip;", 46, GOLD).move_to([0, -1.9, 0])
        self.play(FadeIn(cupm), FadeIn(r), FadeIn(rd), FadeIn(ol), FadeIn(neq), Create(track), FadeIn(fillb), FadeIn(rl),
                  FadeIn(t1, shift=UP * 0.15), run_time=0.7)
        self.at("a response is not occupancy")
        t2 = T("a response is not occupancy.", 46, GOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(t2, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S09End(EndCard):
    LINE = "Binding counts sites and measures grip; a response is not occupancy."
