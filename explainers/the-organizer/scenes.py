"""The organizer: a graft changes its neighbours' fate  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = ectoderm that is on its way to skin
  PURPLE = neural fate (neural plate, neural tube)
  GREEN  = mesoderm
  CREAM  = donor tissue / the organizer (the pale graft, cells with no pigment)
  AMBER dots = pigment granules (marks host cells)
  YELLOW = the signal / what moves or is highlighted
  GREY   = endoderm, outlines, labels
  RED    = the open question
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CREAM = "#F2EBD3"
AMBER = "#E39A3C"
R = 0.3


def X(i):
    return -5.04 + 0.72 * i


def cell(x, y, color=BLUE, dots=False, r=R):
    fo = 0.85 if color == CREAM else 0.5
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fo)
    g = VGroup(c)
    if dots:
        for dx, dy in ((-0.15, 0.04), (-0.04, 0.15), (0.12, 0.08), (0.14, -0.1), (-0.07, -0.11), (0.02, -0.01)):
            g.add(Dot([dx * r / 0.3, dy * r / 0.3, 0], radius=0.04 * r / 0.3, color=AMBER))
    g.move_to([x, y, 0])
    g.base, g.dots_on = c, dots
    return g


def paint(g, color):
    fo = 0.85 if color == CREAM else 0.5
    return g.base.animate.set_stroke(color).set_fill(color, fo)


def row(idx, y, color, dots=False, k=1.0):
    return [cell(X(i) * k, y, color, dots, r=R * k) for i in idx]


def ring(cells_colors, center, rad):
    """positions for n cells around a circle, first cell at the bottom (the floor)."""
    n = len(cells_colors)
    out = []
    for k in range(n):
        a = -PI / 2 + TAU * k / n
        out.append(np.array([center[0] + rad * np.cos(a), center[1] + rad * np.sin(a), 0]))
    return out


def lab(text, color=GREY, size=24):
    return T(text, size, color)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "The organizer: Spemann and Mangold"
    TITLE = "A graft changes its neighbours' fate"


# ---------------------------------------------------------------------------------------------
def backed(c):
    """put an opaque disc behind a cell so background dots do not show through."""
    back = Circle(radius=c.base.radius, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    return VGroup(back, c)


class S01Question(SpokenScene):
    def construct(self):
        donor = Ellipse(width=5.4, height=3.6, stroke_color=CREAM, stroke_width=4,
                        fill_color=CREAM, fill_opacity=0.14).move_to([-3.4, 0.2, 0])
        host = Ellipse(width=5.6, height=3.8, stroke_color=BLUE, stroke_width=4,
                       fill_color=BLUE, fill_opacity=0.14).move_to([3.4, 0.2, 0])
        rng = np.random.RandomState(4)
        dots = VGroup()
        while len(dots) < 30:
            p = rng.uniform(-1, 1, 2) * [2.6, 1.7]
            if (p[0] / 2.6) ** 2 + (p[1] / 1.7) ** 2 < 0.9:
                dots.add(Dot([3.4 + p[0], 0.2 + p[1], 0], radius=0.06, color=AMBER))
        dl = lab("one newt embryo", GREY, 26).move_to([-3.4, 2.7, 0])
        hl = lab("another", GREY, 26).move_to([3.4, 2.7, 0])
        self.add(donor, host, dots, dl, hl)

        patch = RoundedRectangle(corner_radius=0.08, width=1.1, height=0.65, stroke_color=YELLOW, stroke_width=4,
                                 fill_color=CREAM, fill_opacity=0.9).move_to([-3.4, 1.1, 0])
        self.at("small piece of tissue")
        self.play(FadeIn(patch, scale=0.6), run_time=0.4)
        self.at("Place it")
        self.play(patch.animate.move_to([3.4, -1.1, 0]), run_time=1.6)
        self.play(patch.animate.set_stroke(CREAM), run_time=0.3)

        tube = VGroup(*[backed(cell(1.8 + 0.8 * k, 0.5, PURPLE, r=0.34)) for k in range(5)])
        self.at("second neural tube")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in tube], lag_ratio=0.15), run_time=1.0)
        tl = lab("second neural tube", PURPLE, 26)
        tl_back = Rectangle(width=tl.width + 0.2, height=tl.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=0.9)
        tl = VGroup(tl_back, tl).move_to([3.4, 1.35, 0])
        self.play(FadeIn(tl), run_time=0.4)
        qs = VGroup(*[T("?", 32, TEXT, weight=BOLD).move_to(c) for c in tube])
        self.at("Where do the cells")
        self.play(FadeIn(qs, lag_ratio=0.1), run_time=0.6)

        c1 = chip("graft cells?", CREAM, 28).move_to([-1.0, -2.9, 0])
        c2 = chip("host cells?", AMBER, 28).move_to([3.4, -2.9, 0])
        self.at("come from")
        self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2), run_time=0.7)
        self.play(Indicate(c1, color=CREAM, scale_factor=1.1), run_time=0.5)
        self.play(Indicate(c2, color=AMBER, scale_factor=1.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Layers(SpokenScene):
    def construct(self):
        ecto = row(range(15), 1.0, GREY)
        meso = row(range(7), -0.1, GREY)
        endo = row(range(15), -1.2, GREY)
        self.at("three layers")
        self.play(LaggedStart(*[FadeIn(c) for c in ecto], lag_ratio=0.02),
                  LaggedStart(*[FadeIn(c) for c in meso], lag_ratio=0.03),
                  LaggedStart(*[FadeIn(c) for c in endo], lag_ratio=0.02), run_time=0.9)
        l_endo = lab("endoderm", GREY, 26).move_to([0.0, -1.9, 0])
        self.play(FadeIn(l_endo), run_time=0.3)
        l_ecto = lab("ectoderm", BLUE, 26).move_to([0.0, 1.85, 0])
        self.at("The outer layer")
        self.play(*[paint(c, BLUE) for c in ecto], FadeIn(l_ecto), run_time=0.8)
        self.at("makes outer skin")
        self.play(Indicate(VGroup(*ecto), color=BLUE, scale_factor=1.05), run_time=0.8)

        l_plate = lab("neural plate", PURPLE, 26).move_to([X(3), 1.85, 0])
        l_belly = lab("belly: skin", BLUE, 26).move_to([2.52, 1.85, 0])
        self.at("A strip of ectoderm along the back")
        self.play(*[paint(c, PURPLE) for c in ecto[:7]], ReplacementTransform(l_ecto, l_plate), run_time=0.8)
        ring_cols = [PURPLE] * 7
        pos = ring(ring_cols, [X(3), 2.5], 0.72)
        self.at("rolls up")
        l_tube = lab("neural tube", PURPLE, 26).move_to([-0.35, 2.5, 0])
        self.play(*[ecto[k].animate.move_to(pos[k]) for k in range(7)], FadeOut(l_plate), run_time=0.9)
        self.play(FadeIn(l_tube), run_time=0.3)
        self.at("Ectoderm on the belly")
        self.play(FadeIn(l_belly), run_time=0.4)
        self.at("becomes skin")
        self.play(Indicate(VGroup(*ecto[7:]), color=BLUE, scale_factor=1.08), run_time=0.7)
        self.at("Both start as the same kind")
        self.play(Indicate(VGroup(*ecto[7:]), color=TEXT, scale_factor=1.04), Indicate(VGroup(*ecto[:7]), color=TEXT, scale_factor=1.04), run_time=1.0)
        q = T("?", 64, YELLOW, weight=BOLD).move_to([1.3, 2.9, 0])
        self.at("So what is different")
        self.play(FadeIn(q, scale=0.5), run_time=0.5)

        lip = ArcBetweenPoints([-5.5, 1.0, 0], [-5.5, -0.1, 0], angle=-PI * 0.9, color=YELLOW, stroke_width=5)
        lip.add_tip(tip_length=0.22)
        l_lip = lab("dorsal lip", YELLOW, 26).move_to([-5.15, 1.95, 0])
        l_meso = lab("mesoderm", GREEN, 26).move_to([1.45, -0.1, 0])
        la = arr([0.55, -0.1, 0], [-0.4, -0.1, 0], GREEN)
        self.at("Underneath the back")
        self.play(FadeOut(q), run_time=0.3)
        self.play(Create(lip), FadeIn(l_lip), run_time=0.9)
        self.at("form the mesoderm")
        self.play(*[paint(c, GREEN) for c in meso], FadeIn(l_meso), GrowArrow(la), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def host_strip(y):
    return row(range(15), y, BLUE, dots=True)


class S03Graft(SpokenScene):
    def construct(self):
        donor = row(range(15), 2.4, CREAM)
        l_don = lab("pale embryo: little pigment", CREAM, 26).move_to([0, 3.2, 0])
        host = host_strip(-0.4)
        l_host = lab("pigmented embryo", AMBER, 26).move_to([0, 0.5, 0])
        self.at("Cells of one")
        self.play(LaggedStart(*[FadeIn(c) for c in donor], lag_ratio=0.03), FadeIn(l_don), run_time=0.9)
        self.at("Cells of the other")
        self.play(LaggedStart(*[FadeIn(c) for c in host], lag_ratio=0.03), FadeIn(l_host), run_time=0.9)
        self.at("stay visible in thin sections")
        self.play(*[Indicate(c[1:], color=AMBER, scale_factor=1.4) for c in host[3:12]], run_time=1.2)

        lip = VGroup(*[SurroundingRectangle(donor[i], color=YELLOW, buff=0.03, stroke_width=3, corner_radius=0.1) for i in (6, 7, 8)])
        l_lip = lab("dorsal lip", YELLOW, 26).move_to([X(7), 1.65, 0])
        self.at("a small piece of dorsal lip")
        self.play(Create(lip), FadeIn(l_lip), run_time=0.8)
        patch = VGroup(*[donor[i] for i in (6, 7, 8)])
        self.at("She placed it")
        self.play(FadeOut(l_lip), FadeOut(l_don), FadeOut(lip), run_time=0.3)
        self.play(patch.animate.shift(DOWN * 3.9), run_time=1.3)
        l_belly = lab("belly ectoderm: would become skin", BLUE, 26).move_to([0, 0.5, 0])
        self.at("tissue that would become belly skin")
        self.play(ReplacementTransform(l_host, l_belly), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Result(SpokenScene):
    def construct(self):
        host = host_strip(-0.4)
        graft = row((6, 7, 8), -1.5, CREAM)
        self.add(*host, *graft)
        l_g = lab("pale graft", CREAM, 24).move_to([3.0, -1.5, 0])
        self.add(l_g)
        plate_idx = list(range(4, 11))
        l_plate = lab("second neural plate", PURPLE, 26).move_to([0, 0.75, 0])
        self.play(*[paint(host[i], PURPLE) for i in plate_idx], FadeIn(l_plate), FadeOut(l_g), run_time=0.8)
        self.play(*[host[i].animate.shift(UP * 0.25) for i in plate_idx], run_time=0.5)
        pos = ring([0] * 7, [0.0, 1.5], 0.78)
        self.at("It folded")
        self.play(*[host[i].animate.move_to(pos[k]) for k, i in enumerate(plate_idx)], FadeOut(l_plate), run_time=0.9)
        l_tube = lab("second neural tube", PURPLE, 26).move_to([3.4, 1.5, 0])
        self.at("closed into a second")
        self.play(FadeIn(l_tube), run_time=0.4)

        self.at("In thin sections")
        keep = {id(host[i]) for i in plate_idx}
        rest = [c for c in host if id(c) not in keep]
        self.play(FadeOut(VGroup(*rest, *graft, l_tube)), *[FadeOut(host[i]) for i in plate_idx], run_time=0.4)
        ctr = [-1.0, 0.7]
        n, RR = 10, 1.75
        pos = []
        for k in range(n):
            a = -PI / 2 + TAU * (k - 0.5) / n
            pos.append(np.array([ctr[0] + RR * np.cos(a), ctr[1] + RR * np.sin(a), 0]))
        sec = VGroup(*[cell(p[0], p[1], PURPLE, dots=True, r=0.42) for p in pos])
        l_sec = lab("section through the second neural tube", GREY, 26).move_to([0, -3.2, 0])
        self.play(FadeIn(sec, lag_ratio=0.05), FadeIn(l_sec), run_time=0.6)
        self.at("most of that tube was pigmented")
        self.play(*[Indicate(d, color=AMBER, scale_factor=1.8) for c in sec[2:] for d in c[1:]], run_time=0.8)
        la = lab("pigmented: host cells", AMBER, 28).move_to([4.2, 1.9, 0])
        self.at("made of host cells")
        self.play(FadeIn(la), run_time=0.4)
        self.at("A narrow pale strip")
        floor = [sec[0], sec[1]]
        self.play(*[paint(c, CREAM) for c in floor], *[FadeOut(d) for c in floor for d in c[1:]], run_time=0.7)
        lb = lab("pale: from the graft", CREAM, 28).move_to([4.7, -1.3, 0])
        lbA = arr([2.9, -1.3, 0], [-0.2, -1.05, 0], CREAM)
        self.play(FadeIn(lb), GrowArrow(lbA), run_time=0.5)
        self.at("In another embryo")
        newd = []
        for c in floor:
            for o in ((-0.15, 0.04), (-0.04, 0.15), (0.12, 0.08), (0.14, -0.1), (-0.07, -0.11), (0.02, -0.01)):
                newd.append(Dot(c.get_center() + np.array([o[0] * 0.42 / 0.3, o[1] * 0.42 / 0.3, 0]), radius=0.04 * 0.42 / 0.3, color=AMBER))
        self.play(*[paint(c, PURPLE) for c in floor], *[FadeIn(d) for d in newd], FadeOut(lb), FadeOut(lbA), run_time=0.8)
        self.at("the whole tube was host tissue")
        self.play(*[Indicate(d, color=AMBER, scale_factor=1.8) for d in [d for c in sec[2:] for d in c[1:]] + newd], run_time=0.8)
        nb = VGroup(*[cell(ctr[0] - 0.8 + 0.8 * k, -2.55, CREAM, r=0.34) for k in range(3)])
        l_nb = lab("second notochord", CREAM, 28).move_to([3.4, -2.55, 0])
        self.at("The pale graft lay beneath it")
        self.play(FadeOut(l_sec), FadeIn(nb, lag_ratio=0.2), run_time=0.8)
        self.at("as a second notochord")
        self.play(FadeIn(l_nb), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
K = 1.2


class S05Induction(SpokenScene):
    def construct(self):
        ecto = row(range(15), 1.5, BLUE, k=K)
        sig_t = row(range(5, 10), -0.9, CREAM, k=K)
        l_e = lab("ectoderm", BLUE, 28).move_to([-4.6, 2.4, 0])
        l_s = lab("signaling tissue", CREAM, 28).move_to([0, -1.85, 0])
        self.play(LaggedStart(*[FadeIn(c) for c in ecto], lag_ratio=0.03), FadeIn(l_e), run_time=0.7)
        l_skin = lab("on its way to skin", BLUE, 28).move_to([4.2, 2.4, 0])
        self.at("that would have made skin")
        self.play(FadeIn(l_skin), run_time=0.4)
        self.play(FadeIn(VGroup(*sig_t)), FadeIn(l_s), run_time=0.5)
        arrows = VGroup(*[arr([X(i) * K, -0.4, 0], [X(i) * K, 0.9, 0], YELLOW, w=5) for i in range(5, 10)])
        self.at("had made nervous system")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), run_time=0.6)
        self.play(*[paint(ecto[i], PURPLE) for i in range(3, 12)], FadeOut(l_skin), run_time=0.7)
        l_n = lab("nervous system", PURPLE, 28).move_to([4.2, 2.4, 0])
        self.play(FadeIn(l_n), run_time=0.3)
        self.at("This is induction")
        l_ind = T("induction", 46, YELLOW, weight=BOLD, font=TITLE_FONT).move_to([-4.0, -3.0, 0])
        self.play(FadeIn(l_ind, shift=UP * 0.2), run_time=0.5)
        self.at("a change in the fate of one tissue")
        self.play(Indicate(VGroup(*ecto[3:12]), color=PURPLE, scale_factor=1.06), run_time=0.9)
        self.at("caused by a signal")
        self.play(Indicate(arrows, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("must be able to answer")
        brace = Brace(VGroup(*ecto[3:12]), UP, color=BLUE, buff=0.12)
        self.play(FadeOut(l_n), FadeOut(l_e), FadeIn(brace), run_time=0.5)
        l_c = T("competence", 42, BLUE, weight=BOLD, font=TITLE_FONT).next_to(brace, UP, buff=0.12)
        self.at("That ability is called competence")
        self.play(FadeIn(l_c, shift=UP * 0.1), run_time=0.5)
        self.at("It does not last")
        self.play(FadeOut(VGroup(*ecto, *sig_t, arrows, l_s, l_ind, brace, l_c)), run_time=0.6)

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=9.0, y_length=4.6,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False, "include_tip": True},
                  ).move_to([0.3, 0.0, 0])
        xl = lab("age of the ectoderm  (older embryos)", GREY, 28).next_to(ax, DOWN, buff=0.3)
        yl = lab("neural response", PURPLE, 28).rotate(PI / 2).next_to(ax, LEFT, buff=0.3)
        f = lambda x: 9.2 / (1 + np.exp(1.1 * (x - 6.2)))
        curve = ax.plot(f, x_range=[0.2, 9.8], color=PURPLE, stroke_width=6)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.7)
        dot = Dot(ax.c2p(0.2, f(0.2)), radius=0.14, color=YELLOW)
        self.at("In amphibians")
        self.play(FadeIn(dot), run_time=0.3)
        t = ValueTracker(0.2)
        dot.add_updater(lambda d: d.move_to(ax.c2p(t.get_value(), f(t.get_value()))))
        self.at("older embryos responds less")
        self.play(Create(curve), t.animate.set_value(9.8), run_time=3.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Organizer(SpokenScene):
    def construct(self):
        yE, yM = 1.8, -1.0
        org = row((6, 7, 8), yM, CREAM, k=K)
        meso = row([i for i in range(15) if i not in (6, 7, 8)], yM, GREEN, k=K)
        ecto = row(range(15), yE, BLUE, k=K)
        self.add(*org)
        l_org = T("organizer", 42, CREAM, weight=BOLD, font=TITLE_FONT).move_to([0, -2.3, 0])
        self.at("The dorsal lip is called")
        self.play(FadeIn(l_org, shift=UP * 0.15), *[Indicate(c, color=YELLOW) for c in org], run_time=0.9)
        self.play(LaggedStart(*[FadeIn(c) for c in ecto], lag_ratio=0.02),
                  LaggedStart(*[FadeIn(c) for c in meso], lag_ratio=0.02), run_time=0.8)
        l_m = lab("mesoderm", GREEN, 26).move_to([-4.9, yM - 0.85, 0])
        l_e = lab("ectoderm", BLUE, 26).move_to([-4.9, yE + 0.85, 0])
        self.play(FadeIn(l_m), FadeIn(l_e), run_time=0.4)
        nb = chip("notochord", CREAM, 30).move_to([5.0, 0.4, 0])
        a_nb = arr([X(8) * K + 0.3, yM + 0.4, 0], [4.1, 0.2, 0], CREAM)
        self.at("Its own cells become notochord")
        self.play(GrowArrow(a_nb), FadeIn(nb), run_time=0.8)
        sides = [meso[i] for i in (3, 4, 5, 9, 10, 11)]
        a_l = arr([X(6) * K - 0.45, yM, 0], [X(3) * K - 0.1, yM, 0], YELLOW)
        a_r = arr([X(8) * K + 0.45, yM, 0], [X(11) * K + 0.1, yM, 0], YELLOW)
        l_d = lab("dorsal fates", GREEN, 28).move_to([X(4) * K, yM + 0.85, 0])
        l_d2 = lab("dorsal fates", GREEN, 28).move_to([X(10) * K, yM + 0.85, 0])
        self.at("mesoderm into dorsal fates")
        self.play(GrowArrow(a_l), GrowArrow(a_r), FadeOut(a_nb), FadeOut(nb), run_time=0.7)
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.2) for c in sides], FadeIn(l_d), FadeIn(l_d2), run_time=0.9)
        ups = VGroup(*[arr([X(i) * K, yM + 0.45, 0], [X(i) * K, yE - 0.5, 0], YELLOW, w=4) for i in (6, 7, 8)])
        self.at("it induces the ectoderm")
        self.play(FadeOut(a_l), FadeOut(a_r), FadeOut(l_d), FadeOut(l_d2), run_time=0.3)
        self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.1), run_time=0.5)
        self.play(*[paint(ecto[i], PURPLE) for i in range(4, 11)], run_time=0.6)
        q = T("?", 110, RED, weight=BOLD).move_to([X(7) * K, 0.4, 0])
        l_q = T("what is the signal?", 42, RED, font=TITLE_FONT).move_to([0, -2.9, 0])
        self.at("one question open")
        self.play(FadeOut(ups), FadeOut(l_org), FadeOut(l_m), FadeOut(l_e), run_time=0.3)
        self.play(FadeIn(q, scale=0.4), FadeIn(l_q), run_time=0.6)
        self.at("Keep the rule")
        rule = T("A cell's fate depends, in part,\non the signals it receives", 46, TEXT, font=TITLE_FONT, line_spacing=0.9)
        rule.move_to([0, 0, 0])
        self.play(FadeOut(VGroup(*ecto, *org, *meso, q, l_q)), run_time=0.5)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A cell's fate depends, in part, on the signals it receives."
