"""Stem cells: chance decides which stem cell wins  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a stem cell, unlabelled (plain)
  GREY   = crypt outline, differentiated / short-lived cells, structure
  GREEN  = the label: the tamoxifen-induced mark, a labelled clone, labelled cells in the model
  YELLOW = tamoxifen (the drug) and the highlighted dividing step
  PURPLE, ORANGE, PINK = the other reporter colours (clones of a different colour)
  RED    = lost / crossed out / not shown
  TEAL   = the arithmetic and the plotted curve
  GOLD   = the open question
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E87FB0"
CLONE = [GREEN, PURPLE, ORANGE, PINK]

CX = -3.3                 # crypt centre x
R = 2.0                   # crypt half width
CC = -1.3                 # y of the centre of the crypt's rounded bottom
TOP = CC + 3.6            # top of the crypt walls


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def crypt(cx=CX, k=1.0, h=3.6):
    r_ = R * k
    cc = -3.3 + r_
    left = Line([cx - r_, cc + h, 0], [cx - r_, cc, 0], color=GREY, stroke_width=5)
    arc = Arc(radius=r_, start_angle=PI, angle=PI, arc_center=[cx, cc, 0], color=GREY, stroke_width=5)
    right = Line([cx + r_, cc, 0], [cx + r_, cc + h, 0], color=GREY, stroke_width=5)
    return VGroup(left, arc, right)


def base_pos(cx=CX, k=1.0):
    cc = -3.3 + R * k
    return [np.array([cx + 1.45 * k * np.cos(np.radians(a)), cc + 1.45 * k * np.sin(np.radians(a)), 0]) for a in (190, 230, 270, 310, 350)]


def cell(color=BLUE, r=0.4, fill=0.35, sw=4):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)


def rise_pos(cx=CX):
    return [[np.array([cx + dx, CC + 1.05 + 0.75 * k, 0]) for dx in (-1.2, -0.4, 0.4, 1.2)] for k in range(4)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cross(mob, color=RED, w=7):
    d = 0.5 * mob.width
    h = 0.5 * mob.height
    c = mob.get_center()
    return VGroup(Line(c + [-d, h, 0], c + [d, -h, 0], color=color, stroke_width=w),
                  Line(c + [-d, -h, 0], c + [d, h, 0], color=color, stroke_width=w))


class S00Title(TitleCard):
    LESSON = "Stem cells and tissue renewal"
    TITLE = "Chance decides which stem cell wins"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a crypt: cells born at the base, move up, shed at the tip; the base is the open question."""

    def construct(self):
        cr = crypt()
        head = T("mouse small intestine", 26, GREY).move_to([3.4, 3.1, 0])
        t1 = T("lining replaced\nevery few days", 38, TEXT, font=TITLE_FONT, line_spacing=0.8).move_to([3.4, 1.7, 0])
        self.at("The lining")
        self.play(Create(cr), FadeIn(head), FadeIn(t1, shift=UP * 0.15), run_time=0.9)
        t2 = T("kept for life", 38, TEXT, font=TITLE_FONT).move_to([3.4, 0.35, 0])
        self.at("Yet the animal")
        self.play(FadeIn(t2, shift=UP * 0.15), run_time=0.6)

        base = [cell(BLUE).move_to(p) for p in base_pos()]
        born = bchip("born in the crypt", BLUE, 26).move_to([3.4, -2.6, 0])
        self.at("Cells are born")
        self.play(FadeOut(VGroup(t1, t2)), LaggedStart(*[FadeIn(c, scale=0.6) for c in base], lag_ratio=0.12),
                  FadeIn(born), run_time=0.9)

        pos = rise_pos()
        rows = [VGroup(*[cell(GREY, 0.3, 0.3, 3).move_to(p) for p in row]) for row in pos]
        up_lbl = bchip("move up", GREY, 26).move_to([3.4, -1.2, 0])
        up_arr = arr([3.4, -2.2, 0], [3.4, -1.6, 0], GREY)
        self.at("They move up")
        self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.2) for r_ in rows], lag_ratio=0.2), FadeIn(up_lbl), GrowArrow(up_arr), run_time=0.9)

        shed_arr = arr([CX, 2.4, 0], [CX, 3.0, 0], GREY)
        shed_lbl = bchip("shed at the tip", GREY, 26).move_to([3.4, 0.2, 0])
        up_arr2 = arr([3.4, -0.8, 0], [3.4, -0.2, 0], GREY)
        self.at("shed at the tip")
        self.play(GrowArrow(shed_arr), GrowArrow(up_arr2), FadeIn(shed_lbl), run_time=0.5)
        # the stream: everything shifts up one row, the top row is shed, a new row is born
        top = rows[-1]
        newrow = VGroup(*[cell(GREY, 0.3, 0.3, 3).move_to(p) for p in pos[0]])
        self.play(*[r_.animate.shift(UP * 0.75) for r_ in rows], run_time=0.6)
        self.play(FadeOut(top, shift=UP * 0.3), FadeIn(newrow, shift=UP * 0.2), run_time=0.4)
        rows = [newrow] + rows[:-1]
        self.at("Something at the bottom")
        ring = DashedVMobject(Circle(radius=0.5, color=GOLD, stroke_width=5), num_dashes=24).move_to([CX, -1.75, 0])
        q = T("?", 50, GOLD, weight=BOLD).move_to([CX, -1.75, 0])
        self.play(Create(ring), FadeIn(q, scale=0.6), *[c.animate.set_stroke(GOLD, 6) for c in base], run_time=0.8)
        self.play(FadeOut(VGroup(born, up_lbl, up_arr, up_arr2, shed_lbl, head)), run_time=0.5)
        ask = T("Which cells?\nHow would you\nprove it?", 44, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to([3.4, 0.2, 0])
        self.at("Which cells")
        self.play(FadeIn(ask, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Trace(SpokenScene):
    """tamoxifen marks one base cell; the mark is inherited and spreads up over 60 days."""

    def construct(self):
        cr = crypt()
        base = [cell(BLUE).move_to(p) for p in base_pos()]
        pos = rise_pos()
        rows = [VGroup(*[cell(GREY, 0.3, 0.3, 3).move_to(p) for p in row]) for row in pos]
        allrise = VGroup(*rows)
        self.add(cr, *base, allrise)

        note = T("a gene being on\nsays nothing about fate", 30, TEXT, line_spacing=0.85).move_to([3.4, 1.0, 0])
        self.at("Expressing a gene")
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.7)
        self.at("trace cells")
        self.play(FadeOut(note), Indicate(base[3], color=GREEN, scale_factor=1.15), run_time=0.7)

        tam = bchip("tamoxifen", YELLOW, 28).move_to([3.4, -2.6, 0])
        a_t = arr(tam.get_left() + [-0.05, 0, 0], base[3].get_right() + [0.08, 0, 0], YELLOW)
        self.at("tamoxifen")
        self.play(FadeIn(tam, shift=LEFT * 0.2), GrowArrow(a_t), run_time=0.7)
        mark = T("permanent mark", 26, GREEN).move_to([3.4, -1.55, 0])
        self.at("permanent mark")
        self.play(base[3].animate.set_stroke(GREEN).set_fill(GREEN, 0.7), FadeIn(mark), run_time=0.6)

        # the mark is inherited: a ribbon of daughters rises up the right-hand side
        self.at("Every daughter")
        sel = [rows[0][3], rows[1][3], rows[2][3], rows[3][3]]
        self.play(LaggedStart(*[c.animate.set_stroke(GREEN).set_fill(GREEN, 0.6) for c in sel], lag_ratio=0.25), run_time=1.0)

        # 60 days
        bar = Line([0.6, 2.6, 0], [6.2, 2.6, 0], color=GREY, stroke_width=4)
        d0 = T("day 0", 24, GREY).move_to([0.9, 3.05, 0])
        d60 = T("day 60", 24, GREY).move_to([5.7, 3.05, 0])
        t0 = Line([0.6, 2.4, 0], [0.6, 2.8, 0], color=GREY, stroke_width=4)
        dot = Dot([0.6, 2.6, 0], radius=0.14, color=GREEN)
        self.at("Over")
        self.play(Create(bar), FadeIn(d0), FadeIn(t0), FadeIn(d60), FadeIn(dot), run_time=0.6)
        rib2 = [rows[k][1] for k in range(4)] + [rows[1][2], rows[2][2]]
        self.at("the label filled")
        self.play(dot.animate.move_to([6.2, 2.6, 0]),
                  LaggedStart(*[c.animate.set_stroke(GREEN).set_fill(GREEN, 0.6) for c in rib2], lag_ratio=0.1), run_time=1.8)
        rl = T("ribbons of labelled epithelium", 24, GREEN).move_to([3.4, 1.9, 0])
        self.play(FadeIn(rl), run_time=0.4)
        every = bchip("every epithelial cell type\nwithin the ribbons", GREEN, 26).move_to([3.4, 0.7, 0])
        self.at("Those ribbons")
        self.play(FadeIn(every, shift=UP * 0.15), run_time=0.6)
        multi = bchip("multipotent: within the gut", GREEN, 26).move_to([3.4, -0.6, 0])
        self.at("That shows")
        self.play(FadeIn(multi, shift=UP * 0.15), run_time=0.5)
        plu = bchip("pluripotent", RED, 28).move_to([3.4, -1.55, 0])
        self.at("It does not show")
        self.play(FadeIn(plu, shift=UP * 0.15), run_time=0.5)
        x = cross(plu)
        self.at("pluripotency")
        self.play(Create(x[0]), Create(x[1]), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def division(cx, ytop, c_parent, c1, c2, r=0.6, dx=1.0, drop=2.3):
    p = cell(c_parent, r).move_to([cx, ytop, 0])
    d1 = cell(c1, r).move_to([cx - dx, ytop - drop, 0])
    d2 = cell(c2, r).move_to([cx + dx, ytop - drop, 0])
    a1 = arr(p.get_bottom(), d1.get_top(), GREY, w=4, tip=0.2)
    a2 = arr(p.get_bottom(), d2.get_top(), GREY, w=4, tip=0.2)
    return p, d1, d2, a1, a2


class S03Cartoon(SpokenScene):
    """the always-uneven cartoon, the colour reporter, and what was seen: symmetric divisions."""

    def construct(self):
        head_l = T("the cartoon:\nuneven, every time", 28, GREY, weight=BOLD, line_spacing=0.8).move_to([-3.4, 3.0, 0])
        self.at("How do the stem cells")
        self.play(FadeIn(head_l), run_time=0.4)
        p, d1, d2, a1, a2 = division(-3.4, 1.8, BLUE, BLUE, GREY)
        self.at("One cartoon")
        self.play(FadeIn(p, scale=0.8), run_time=0.4)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(d1, shift=DOWN * 0.1), FadeIn(d2, shift=DOWN * 0.1), run_time=0.7)
        l1 = T("stem cell", 24, BLUE).next_to(d1, DOWN, buff=0.15)
        l2 = T("short-lived\ncell", 24, GREY, line_spacing=0.8).next_to(d2, DOWN, buff=0.15)
        self.at("One stem cell")
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)

        self.at("Snippert")
        strip_cell = cell(BLUE, 0.35).move_to([-5.7, -3.2, 0])
        sa = arr([-5.2, -3.2, 0], [-4.6, -3.2, 0], GREY, w=4, tip=0.2)
        cols = [cell(c_, 0.3).move_to([-4.0 + 0.8 * i, -3.2, 0]) for i, c_ in enumerate(CLONE)]
        cap = T("random colour,\none of four", 24, TEXT, line_spacing=0.8).move_to([0.0, -3.2, 0])
        self.at("Their reporter")
        self.play(FadeIn(strip_cell), GrowArrow(sa), LaggedStart(*[FadeIn(c_, scale=0.5) for c_ in cols], lag_ratio=0.15),
                  FadeIn(cap), run_time=1.2)

        # clock: about once a day
        clock = VGroup(Circle(radius=0.36, stroke_color=GREY, stroke_width=4),
                       Line(ORIGIN, UP * 0.26, color=TEXT, stroke_width=4), Line(ORIGIN, RIGHT * 0.18, color=TEXT, stroke_width=4)
                       ).move_to([3.0, -3.2, 0])
        clock_t = T("divide about\nonce a day", 24, TEXT, line_spacing=0.8).move_to([4.9, -3.2, 0])
        self.at("These stem cells divide")
        self.play(FadeIn(clock), FadeIn(clock_t), run_time=0.6)
        self.play(Rotate(clock[1], angle=-TAU, about_point=clock[0].get_center(), rate_func=linear), run_time=0.8)

        head_r = T("what they saw", 28, GREEN, weight=BOLD).move_to([3.3, 3.0, 0])
        self.at("Most divisions")
        self.play(FadeIn(head_r), run_time=0.4)
        p2, e1, e2, b1, b2 = division(1.6, 1.8, BLUE, BLUE, BLUE, dx=0.9, r=0.5)
        self.at("two stem cells")
        self.play(FadeIn(p2, scale=0.8), run_time=0.3)
        self.play(GrowArrow(b1), GrowArrow(b2), FadeIn(e1), FadeIn(e2), run_time=0.7)
        m1 = T("two stem\ncells", 24, BLUE, line_spacing=0.8).move_to([1.6, -1.55, 0])
        self.play(FadeIn(m1), run_time=0.3)
        p3, f1, f2, g1, g2 = division(4.9, 1.8, BLUE, GREY, GREY, dx=0.9, r=0.5)
        self.at("or two")
        self.play(FadeIn(p3, scale=0.8), run_time=0.3)
        self.play(GrowArrow(g1), GrowArrow(g2), FadeIn(f1), FadeIn(f2), run_time=0.7)
        m2 = T("two non-stem\ncells", 24, GREY, line_spacing=0.8).move_to([4.9, -1.55, 0])
        self.play(FadeIn(m2), run_time=0.3)
        # the symmetric result replaces the cartoon's claim
        self.finish()


# ---------------------------------------------------------------------------------------------
def bars_for(colors_state, x0=1.4):
    """rows of horizontal bars: cells per clone colour (computed from the crypt's current state)."""
    order = [GREEN, PURPLE, ORANGE, PINK, BLUE]
    g = VGroup()
    for i, c_ in enumerate(order):
        n = sum(1 for s in colors_state if s == c_)
        w = max(0.001, 0.62 * n)
        b = Rectangle(width=w, height=0.38, stroke_width=0 if n == 0 else 2, stroke_color=c_, fill_color=c_, fill_opacity=0.55)
        b.move_to([x0 + w / 2, 1.05 - 0.62 * i, 0])
        g.add(b)
    return g


def swatches(x0=0.9):
    return VGroup(*[Circle(radius=0.17, stroke_color=c_, stroke_width=3, fill_color=c_, fill_opacity=0.35).move_to([x0, 1.05 - 0.62 * i, 0])
                    for i, c_ in enumerate([GREEN, PURPLE, ORANGE, PINK, BLUE])])


class S04Drift(SpokenScene):
    """a model crypt of five stem cells drifts to one colour; bars show clones growing and vanishing."""

    def construct(self):
        K = 1.3
        cr = crypt(-3.4, K, 2.6)
        state = [GREEN, PURPLE, ORANGE, PINK, BLUE]
        pos = base_pos(-3.4, K)
        cells = [cell(c_, 0.52).move_to(p) for c_, p in zip(state, pos)]
        cap = T("model crypt:\nfive equivalent stem cells", 26, GREY, line_spacing=0.85).move_to([3.4, 3.0, 0])
        self.add(cr, *cells)

        mlab = T("real crypts, over 1 to 6 months:\ndrifted toward a single colour", 24, GREY, line_spacing=0.85).move_to([3.4, -2.7, 0])
        self.at("Then they waited")
        self.play(FadeIn(cap), run_time=0.5)

        events = [(3, 4), (1, 0), (1, 2), (2, 3), (3, 4)]   # (source, target)
        stops = [0.2, 0.4, 0.6, 0.8, 1.0]
        bars = None

        def event(i):
            nonlocal cells
            s, t = events[i]
            state[t] = state[s]
            new = cells[s].copy().move_to(cells[t].get_center())
            self.play(Indicate(cells[s], scale_factor=1.15, color=state[s]), run_time=0.35)
            self.play(ReplacementTransform(cells[t], new), run_time=0.5)
            cells[t] = new

        self.at("Over")
        self.play(FadeIn(mlab), run_time=0.4)
        self.at("crypts drifted")
        event(0)
        event(1)
        title_b = T("cells per clone", 24, GREY).move_to([2.6, 1.85, 0])
        self.at("Surviving clones")
        bars = bars_for(state)
        sw_ = swatches()
        self.play(FadeIn(title_b), FadeIn(sw_), FadeIn(bars), run_time=0.6)
        self.at("while others vanished")
        for i in (2, 3):
            event(i)
            nb = bars_for(state)
            self.play(Transform(bars, nb), run_time=0.4)
        self.at("neutral drift")
        event(4)
        nb = bars_for(state)
        self.play(Transform(bars, nb), run_time=0.4)
        nd = bchip("neutral drift", TEAL, 30).move_to([3.4, -1.45, 0])
        self.play(FadeIn(nd, shift=UP * 0.1), run_time=0.5)
        self.at("Chance")
        ch = T("chance, not a fixed hierarchy", 26, TEXT).move_to([3.4, 3.1, 0])
        self.play(FadeOut(cap), FadeIn(ch, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
MINI_W, MINI_H = 0.68, 0.46
PITCH_X, PITCH_Y = 0.76, 0.58


def mini_crypt():
    box = RoundedRectangle(corner_radius=0.1, width=MINI_W, height=MINI_H, stroke_color=GREY, stroke_width=2)
    dots = VGroup(*[Dot([(i - 2) * 0.118, 0, 0], radius=0.05, color=BLUE) for i in range(5)])
    return VGroup(box, dots)


class S05Numbers(SpokenScene):
    """100 labelled crypts, N = 5: 1/5 take over = 20 fully labelled; 100 labelled cells conserved."""

    def construct(self):
        rng = np.random.default_rng(7)
        winners = set(rng.choice(100, 20, replace=False).tolist())
        gx, gy = -2.5, -0.05
        crypts = []
        for idx in range(100):
            r_, c_ = divmod(idx, 10)
            m = mini_crypt()
            m.move_to([gx + (c_ - 4.5) * PITCH_X, gy + (4.5 - r_) * PITCH_Y, 0])
            crypts.append(m)
        grid = VGroup(*crypts)

        title = T("a model, with round numbers", 26, GREY).move_to([4.0, 3.15, 0])
        self.at("Now the arithmetic")
        self.play(FadeIn(title), LaggedStart(*[FadeIn(m, scale=0.8) for m in crypts], lag_ratio=0.008), run_time=1.4)
        self.at("Label one stem cell")
        self.play(LaggedStart(*[m[1][2].animate.set_color(GREEN) for m in crypts], lag_ratio=0.01), run_time=1.0)
        l1 = T("100 labelled crypts,\n1 labelled cell each", 28, GREEN, line_spacing=0.85)
        l2 = T("5 equivalent stem cells\nin every crypt", 28, BLUE, line_spacing=0.85)
        l3 = M("P(takeover) = 1/5 = 0.2", 26, TEAL)
        l4 = VGroup(M("100 \u00d7 0.2 = 20", 28, GREEN), T("fully labelled crypts", 26, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        l5 = T("80 clones lost", 28, RED)
        l6 = M("start: 100 \u00d7 1 = 100", 26, TEXT)
        l7 = M("end:   20 \u00d7 5 = 100", 26, TEXT)
        panel = VGroup(l1, l2, l3, l4, l5, l6, l7).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(panel, max_w=4.5, max_h=5.9)
        panel.move_to([4.05, -0.1, 0])
        l1.align_to(panel, LEFT)
        # hide the pieces until their cue
        self.play(FadeIn(l1, shift=LEFT * 0.15), run_time=0.5)
        self.at("Say each crypt")
        self.play(FadeIn(l2, shift=LEFT * 0.15), Indicate(crypts[0][1], color=BLUE, scale_factor=1.3), run_time=0.7)
        self.at("probability")
        self.play(FadeIn(l3, shift=LEFT * 0.15), run_time=0.6)
        self.at("So expect")
        full = [crypts[i] for i in sorted(winners)]
        anims = []
        for m in full:
            for d in m[1]:
                anims.append(d.animate.set_color(GREEN))
            anims.append(m[0].animate.set_stroke(GREEN, 3))
        self.play(*anims, FadeIn(l4, shift=LEFT * 0.15), run_time=1.0)
        self.at("clones are lost")
        lost = [crypts[i] for i in range(100) if i not in winners]
        self.play(*[m[1][2].animate.set_color(BLUE) for m in lost], *[m[0].animate.set_stroke(GREY, 2, opacity=0.4) for m in lost],
                  FadeIn(l5, shift=LEFT * 0.15), run_time=1.0)
        self.at("Check the count")
        self.play(FadeIn(l6, shift=LEFT * 0.15), run_time=0.5)
        self.at("at the end")
        self.play(FadeIn(l7, shift=LEFT * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Estimate(SpokenScene):
    """expected fully labelled crypts = 100 / N: N 5 gives 20, N 14 gives about 7; read N back from the count."""

    def construct(self):
        axes = Axes(x_range=[3, 16, 1], y_range=[0, 30, 5], x_length=8.6, y_length=5.0,
                    axis_config={"color": GREY, "stroke_width": 4, "include_ticks": True, "include_numbers": False, "tick_size": 0.08},
                    tips=False)
        axes.move_to([-0.7, -0.2, 0])
        xl = T("stem cells competing per crypt, N", 24, GREY).next_to(axes, DOWN, buff=0.3)
        yl = T("fully labelled crypts (of 100)", 24, GREY).rotate(PI / 2).next_to(axes, LEFT, buff=0.75)
        curve = axes.plot(lambda n: 100 / n, x_range=[3.5, 16], color=TEAL, stroke_width=6)

        p5 = Dot(axes.c2p(5, 20), radius=0.13, color=GREEN)
        p14 = Dot(axes.c2p(14, 100 / 14), radius=0.13, color=YELLOW)

        def guide(n, y, color, ylabel, xlabel):
            h = DashedLine(axes.c2p(3, y), axes.c2p(n, y), color=color, stroke_width=3)
            v = DashedLine(axes.c2p(n, 0), axes.c2p(n, y), color=color, stroke_width=3)
            yt = T(ylabel, 24, color).next_to(axes.c2p(3, y), LEFT, buff=0.12)
            xt = T(xlabel, 24, color).next_to(axes.c2p(n, 0), DOWN, buff=0.12)
            return VGroup(h, v, yt, xt)

        g5 = guide(5, 20, GREEN, "20", "5")
        g14 = guide(14, 100 / 14, YELLOW, "7", "14")
        eq = M("100 / N", 32, TEAL).move_to([3.4, 2.4, 0])
        self.at("Change")
        self.play(Create(axes), FadeIn(xl), FadeIn(yl), run_time=0.6)
        self.play(Create(curve), FadeIn(eq), FadeIn(p5), Create(g5), run_time=1.0)
        self.at("expected count")
        self.play(FadeIn(p14), Create(g14), run_time=0.8)
        lab = T("about 7 crypts", 26, YELLOW).move_to(axes.c2p(12.0, 100 / 14) + DOWN * 0.45)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        note = T("roughly 14 Lgr5-high cells\ncounted per crypt", 24, YELLOW, line_spacing=0.85).move_to([3.4, 3.1, 0])
        self.at("roughly")
        self.play(FadeIn(note, shift=DOWN * 0.1), FadeOut(eq), run_time=0.6)
        eff = T("N = 5: an effective number,\nsmaller than the count", 24, GREEN, line_spacing=0.85).move_to([3.4, 1.3, 0])
        self.at("was an effective")
        self.play(FadeIn(eff, shift=UP * 0.1), run_time=0.5)
        # read N back from the count
        cnt = bchip("count the crypts", GREEN, 26).move_to(axes.c2p(7.9, 0) + UP * 0.62)
        self.at("So counting")
        self.play(FadeIn(cnt, shift=DOWN * 0.1), run_time=0.5)
        trav = Dot(axes.c2p(3, 100 / 14), radius=0.12, color=WHITE)
        self.at("estimates how many")
        self.play(FadeIn(trav), run_time=0.2)
        self.play(trav.animate.move_to(axes.c2p(14, 100 / 14)), run_time=0.9, rate_func=smooth)
        self.play(trav.animate.move_to(axes.c2p(14, 0)), Indicate(p14, color=YELLOW, scale_factor=1.6), run_time=0.7)
        est = bchip("read off N", YELLOW, 26).move_to(axes.c2p(14, 0) + UP * 1.3 + RIGHT * 0.1)
        est.move_to([5.2, -1.2, 0])
        self.play(FadeIn(est, shift=UP * 0.1), run_time=0.4)
        self.at("Balance is kept")
        self.play(Indicate(curve, color=TEAL, scale_factor=1.03), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Balance is kept by the population, not by each division."
