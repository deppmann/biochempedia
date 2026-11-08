"""Movement and spatial populations: a region outlasts its ponds  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREEN  = an occupied patch / the occupied fraction p
  GREY   = an empty patch, ground, structure, axes
  YELLOW = colonization (colonists, the rate c)
  RED    = local extinction (the rate e)
  BLUE   = the region / metapopulation (bracket) and the sketch curve of p
  GOLD   = the equilibrium line
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

N = 10               # 10 x 10 identical patches in the sketch
SP = 0.5
RNG = np.random.RandomState(7)
RANK = RNG.permutation(N * N)   # patch i is lit when RANK[i] < n_lit (monotone sketches)


def pond(x, y, w=1.8, h=1.35, on=True):
    return Ellipse(width=w, height=h, stroke_color=GREEN if on else GREY, stroke_width=4,
                   fill_color=GREEN if on else GREY, fill_opacity=0.55 if on else 0.12).move_to([x, y, 0])


def make_grid(center, sp=SP, r=0.2):
    dots = VGroup()
    for j in range(N):
        for i in range(N):
            d = Circle(radius=r, stroke_width=2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.12)
            d.move_to([center[0] + (i - (N - 1) / 2) * sp, center[1] + ((N - 1) / 2 - j) * sp, 0])
            dots.add(d)
    return dots


def set_state(d, on):
    c = GREEN if on else GREY
    d.set_stroke(c, 2).set_fill(c, 0.75 if on else 0.12)


def apply_mask(dots, mask):
    for d, m in zip(dots, mask):
        set_state(d, bool(m))


def mask_n(n):
    return [1 if RANK[i] < n else 0 for i in range(N * N)]


def anim_state(d, on):
    c = GREEN if on else GREY
    return d.animate.set_stroke(c, 2).set_fill(c, 0.75 if on else 0.12)


def levins(c, e, p0, T, steps=400):
    dt = T / steps
    p, out = p0, [p0]
    for _ in range(steps):
        p += dt * (c * p * (1 - p) - e * p)
        out.append(p)
    return np.array(out)


def p_at(arr, t, T):
    return float(arr[min(len(arr) - 1, int(round(t / T * (len(arr) - 1))))])


def make_axes(center, w=5.4, h=4.3):
    ax = Axes(x_range=[0, 20, 10], y_range=[0, 1, 0.5], x_length=w, y_length=h,
              axis_config={"color": GREY, "include_tip": False, "include_ticks": True, "stroke_width": 3},
              ).move_to([center[0], center[1], 0])
    labs = VGroup()
    for v in (0, 10, 20):
        labs.add(M(str(v), 22, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.12))
    for v, s in ((0, "0"), (0.5, "0.5"), (1, "1")):
        labs.add(M(s, 22, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.12))
    xl = T("years", 22, GREY).next_to(ax, DOWN, buff=0.5).align_to(ax, RIGHT)
    yl = T("occupied fraction p", 22, GREEN).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
    return ax, VGroup(labs, xl, yl)


def flash_swaps(scene, dots, mask, k, rt=0.35):
    """k lit patches go dark (red flash) and k dark patches are colonized (yellow flash)."""
    lit = [i for i, m in enumerate(mask) if m]
    dark = [i for i, m in enumerate(mask) if not m]
    out = list(RNG.choice(lit, size=min(k, len(lit)), replace=False))
    inn = list(RNG.choice(dark, size=min(k, len(dark)), replace=False))
    scene.play(*[dots[i].animate.set_stroke(RED, 3).set_fill(RED, 0.8) for i in out],
               *[dots[i].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.8) for i in inn], run_time=rt)
    scene.play(*[anim_state(dots[i], False) for i in out], *[anim_state(dots[i], True) for i in inn], run_time=rt)
    for i in out:
        mask[i] = 0
    for i in inn:
        mask[i] = 1


class S00Title(TitleCard):
    LESSON = "Movement and spatial populations"
    TITLE = "A region outlasts its ponds"


# ---------------------------------------------------------------------------------------------
class S01Ponds(SpokenScene):
    def construct(self):
        xs = [-5.25, -3.15, -1.05, 1.05, 3.15, 5.25]
        ys = [0.95, -0.55, 1.05, -0.45, 0.95, -0.55]
        field = Rectangle(width=12.6, height=4.3, stroke_width=0, fill_color=GREY, fill_opacity=0.10).move_to([0, 0.35, 0])
        ponds = [pond(x, y, on=False) for x, y in zip(xs, ys)]
        self.at("string of ponds")
        self.play(FadeIn(field), LaggedStart(*[GrowFromCenter(p) for p in ponds], lag_ratio=0.2), run_time=1.6)
        lbl = T("local population", 30, GREEN).move_to([-4.2, 3.0, 0])
        self.at("local population")
        self.play(ponds[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.55), FadeIn(lbl, shift=DOWN * 0.1), run_time=0.5)
        self.play(*[p.animate.set_stroke(GREEN).set_fill(GREEN, 0.55) for p in ponds[1:]], run_time=0.6)
        hostile = T("hostile ground", 30, GREY).move_to([0, -2.45, 0])
        self.at("hostile ground")
        self.play(FadeIn(hostile, shift=UP * 0.1), run_time=0.5)
        arcs = VGroup()
        for i in range(5):
            a = ArcBetweenPoints(ponds[i].get_top() + RIGHT * 0.35, ponds[i + 1].get_top() + LEFT * 0.35, angle=-0.9,
                                 color=YELLOW, stroke_width=4)
            arcs.add(a)
        self.at("linked by dispersal")
        self.play(FadeOut(lbl), FadeOut(hostile), LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2), run_time=1.0)
        y0 = -2.7
        br = VGroup(Line([-6.0, y0 + 0.25, 0], [-6.0, y0, 0]), Line([-6.0, y0, 0], [6.0, y0, 0]),
                    Line([6.0, y0, 0], [6.0, y0 + 0.25, 0])).set_color(BLUE).set_stroke(width=4)
        mp = T("metapopulation", 32, BLUE).move_to([0, y0 - 0.5, 0])
        self.at("metapopulation")
        self.play(Create(br), FadeIn(mp, shift=UP * 0.1), run_time=0.7)
        self.at("losing their populations")
        self.play(FadeOut(arcs), run_time=0.3)
        for i in (1, 4, 2):
            self.play(ponds[i].animate.set_stroke(GREY).set_fill(GREY, 0.12), run_time=0.4)
        q = T("?", 120, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        self.at("Can a region keep")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Occupied(SpokenScene):
    def construct(self):
        ctr = [0.0, 0.0]
        dots = make_grid(ctr, sp=0.6, r=0.24)
        mask = mask_n(60)
        apply_mask(dots, mask)
        self.at("Richard")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.008), run_time=1.6)
        # occupied fraction bar
        bx = 4.2
        frame = Rectangle(width=1.1, height=4.6, stroke_color=GREY, stroke_width=3).move_to([bx, 0, 0])
        bar = Rectangle(width=1.1, height=4.6 * 0.6, stroke_width=0, fill_color=GREEN, fill_opacity=0.6)
        bar.move_to(frame.get_bottom() + UP * bar.height / 2)
        plabel = T("p", 44, GREEN, weight=BOLD).next_to(frame, UP, buff=0.2)
        plab2 = T("fraction occupied", 24, GREY).next_to(frame, DOWN, buff=0.2)
        self.at("ignored how many animals")
        keyg = VGroup(Circle(radius=0.2, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.75), T("occupied", 26, GREEN),
                      Circle(radius=0.2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.12), T("empty", 26, GREY))
        keyg[1].next_to(keyg[0], RIGHT, buff=0.15)
        keyg[2].next_to(keyg[1], RIGHT, buff=0.5)
        keyg[3].next_to(keyg[2], RIGHT, buff=0.15)
        keyg.move_to([0.0, -3.45, 0])
        self.wait(0.1)
        self.at("either occupied or empty")
        self.play(FadeIn(keyg), run_time=0.5)
        self.at("fraction of patches")
        self.play(VGroup(dots, keyg).animate.shift(LEFT * 2.2), Create(frame), FadeIn(bar), FadeIn(plabel), FadeIn(plab2), run_time=0.9)
        # colonists
        lit = [i for i, m in enumerate(mask) if m]
        dark = [i for i, m in enumerate(mask) if not m]
        src = lit[5]
        # choose a dark target near the source
        sp = dots[src].get_center()
        tgt = min(dark, key=lambda i: abs(np.linalg.norm(dots[i].get_center() - sp) - 1.9))
        arrow = Arrow(sp, dots[tgt].get_center(), buff=0.3, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        self.at("send out colonists")
        self.play(GrowArrow(arrow), dots[src].animate.set_stroke(YELLOW, 4), run_time=0.7)
        self.at("in empty patches")
        self.play(dots[tgt].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.8), run_time=0.4)
        self.play(anim_state(dots[tgt], True), FadeOut(arrow), dots[src].animate.set_stroke(GREEN, 2), run_time=0.4)
        mask[tgt] = 1
        out = [i for i in lit if i not in (src, tgt)][12]
        self.at("losing its population")
        self.play(dots[out].animate.set_stroke(RED, 4).set_fill(RED, 0.8), run_time=0.4)
        self.play(anim_state(dots[out], False), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rates(SpokenScene):
    def construct(self):
        ctr = [-3.6, -0.3]
        dots = make_grid(ctr, sp=0.5, r=0.2)
        mask = mask_n(75)
        apply_mask(dots, mask)
        self.add(dots)
        eq_a = M("dp/dt  =", 32, TEXT)
        eq_c = M("c p (1 − p)", 32, YELLOW)
        eq_m = M("−", 32, TEXT)
        eq_e = M("e p", 32, RED)
        eq = VGroup(eq_a, eq_c, eq_m, eq_e).arrange(RIGHT, buff=0.2).move_to([3.1, 2.2, 0])
        fit(eq, max_w=6.4)
        tag = T("in this sketch of the Levins model", 24, GREY).move_to([3.1, 3.2, 0])
        self.at("Colonization has a rate")
        self.play(FadeIn(tag), Write(eq_a), run_time=0.5)
        self.play(FadeIn(eq_c, shift=DOWN * 0.1), run_time=0.5)
        cbox = VGroup(T("colonization", 30, YELLOW, weight=BOLD), T("rate c per year", 26, YELLOW),
                      T("needs colonists from occupied", 24, TEXT), T("patches, works on empty ones", 24, TEXT)).arrange(DOWN, buff=0.12)
        cbox.move_to([3.1, 0.35, 0])
        cframe = SurroundingRectangle(cbox, color=YELLOW, buff=0.2, corner_radius=0.14, stroke_width=3)
        self.at("It needs colonists")
        self.play(FadeIn(cbox), Create(cframe), run_time=0.7)
        # colonists: yellow flashes on dark patches
        dark = [i for i, m in enumerate(mask) if not m]
        pick = list(RNG.choice(dark, 5, replace=False))
        self.play(*[dots[i].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.8) for i in pick], run_time=0.4)
        self.play(*[anim_state(dots[i], True) for i in pick], run_time=0.4)
        for i in pick:
            mask[i] = 1
        ebox = VGroup(T("extinction", 30, RED, weight=BOLD), T("rate e per year", 26, RED),
                      T("each occupied patch loses", 24, TEXT), T("its population at this rate", 24, TEXT)).arrange(DOWN, buff=0.12)
        ebox.move_to([3.1, -2.1, 0])
        eframe = SurroundingRectangle(ebox, color=RED, buff=0.2, corner_radius=0.14, stroke_width=3)
        self.at("Extinction has a rate")
        self.play(Write(eq_m), FadeIn(eq_e, shift=DOWN * 0.1), FadeIn(ebox), Create(eframe), run_time=0.8)
        lit = [i for i, m in enumerate(mask) if m]
        pick = list(RNG.choice(lit, 5, replace=False))
        self.play(*[dots[i].animate.set_stroke(RED, 3).set_fill(RED, 0.8) for i in pick], run_time=0.4)
        self.play(*[anim_state(dots[i], False) for i in pick], run_time=0.4)
        for i in pick:
            mask[i] = 0
        self.at("row of lamps")
        flash_swaps(self, dots, mask, 5)
        self.at("get relit")
        flash_swaps(self, dots, mask, 5)
        self.at("partly lit")
        flash_swaps(self, dots, mask, 5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Balance(SpokenScene):
    def construct(self):
        ctr = [-3.7, -0.35]
        T_ = 20.0
        arr = levins(0.4, 0.1, 0.10, T_, 800)
        dots = make_grid(ctr, sp=0.5, r=0.2)
        mask = mask_n(10)
        apply_mask(dots, mask)
        self.add(dots)
        ax, labs = make_axes([3.7, -0.35], 5.4, 4.3)
        self.add(ax, labs)
        tag = T("in this sketch", 24, GREY).move_to([-3.7, -3.4, 0])
        self.add(tag)
        eq1 = M("p* = 1 − e/c", 40, GREEN)
        eq1.move_to([-1.5, 3.3, 0])
        self.at("Set the change to zero")
        self.play(Write(eq1), run_time=0.8)
        cond = M("positive only if  c > e", 26, TEXT).next_to(eq1, DOWN, buff=0.15).align_to(eq1, LEFT)
        self.at("positive only when")
        self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.5)
        nums = VGroup(M("c = 0.4", 30, YELLOW), M("e = 0.1", 30, RED), T("per year", 26, GREY)).arrange(RIGHT, buff=0.35)
        nums.move_to([-1.2, 3.25, 0])
        eqn = M("p* = 1 − 0.1/0.4 = 0.75", 32, GREEN).move_to([-1.2, 3.25, 0])
        self.at("Suppose c is")
        self.play(FadeOut(eq1), FadeOut(cond), FadeIn(nums), run_time=0.5)
        line = DashedLine(ax.c2p(0, 0.75), ax.c2p(20, 0.75), color=GOLD, stroke_width=4)
        lab75 = M("0.75", 26, GOLD).next_to(ax.c2p(20, 0.75), UP, buff=0.12).shift(LEFT * 0.35)
        curve = ax.plot(lambda t: p_at(arr, t, T_), x_range=[0, T_, 0.05], color=BLUE, stroke_width=5, use_smoothing=False)
        tr = ValueTracker(0)
        def upd(g):
            n = int(round(p_at(arr, tr.get_value(), T_) * 100))
            apply_mask(g, mask_n(n))
        dots.add_updater(upd)
        self.at("The fraction settles")
        self.play(Create(line), FadeIn(lab75), run_time=0.4)
        self.play(Create(curve, rate_func=linear), tr.animate.set_value(T_).set_rate_func(linear), run_time=1.3)
        dots.remove_updater(upd)
        mask[:] = mask_n(75)
        self.play(ReplacementTransform(nums, eqn), run_time=0.3)
        self.at("Three patches in four")
        self.wait(0.3)
        self.at("which ones keeps changing")
        flash_swaps(self, dots, mask, 8)
        flash_swaps(self, dots, mask, 8)
        flash_swaps(self, dots, mask, 8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Slow(SpokenScene):
    def construct(self):
        ctr = [-3.7, -0.35]
        T_ = 20.0
        dots = make_grid(ctr, sp=0.5, r=0.2)
        mask = mask_n(75)
        apply_mask(dots, mask)
        self.add(dots)
        ax, labs = make_axes([3.7, -0.35], 5.4, 4.3)
        self.add(ax, labs)
        tag = T("in this sketch", 24, GREY).move_to([-3.7, -3.4, 0])
        self.add(tag)
        ce = VGroup(M("c = 0.4", 30, YELLOW), M("e = 0.1", 30, RED), T("per year", 26, GREY)).arrange(RIGHT, buff=0.35).move_to([-1.2, 3.1, 0])
        self.add(ce)
        line = DashedLine(ax.c2p(0, 0.75), ax.c2p(20, 0.75), color=GOLD, stroke_width=4)
        lab = M("0.75", 26, GOLD).next_to(ax.c2p(20, 0.75), UP, buff=0.12).shift(LEFT * 0.35)
        pt0 = Dot(ax.c2p(0, 0.75), color=BLUE, radius=0.09)
        self.add(line, lab)
        self.at("Now let e rise")
        ce2 = VGroup(M("c = 0.4", 30, YELLOW), M("e = 0.4", 30, RED), T("per year", 26, GREY)).arrange(RIGHT, buff=0.35).move_to([-1.2, 3.1, 0])
        self.play(ReplacementTransform(ce, ce2), run_time=0.6)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(20, 0), color=GOLD, stroke_width=4)
        zlab = M("p* = 0", 26, GOLD).next_to(ax.c2p(20, 0), UP, buff=0.12).shift(LEFT * 0.7)
        self.at("equilibrium falls to zero")
        self.play(Transform(line, zero), ReplacementTransform(lab, zlab), run_time=0.8)
        lost = T("the network is lost", 32, RED, weight=BOLD).move_to([-3.7, 2.55, 0])
        self.at("the network is lost")
        self.play(FadeIn(lost, shift=UP * 0.1), run_time=0.4)
        slow = T("... but slowly", 32, RED, weight=BOLD).move_to([-3.7, 2.55, 0])
        self.at("lost slowly")
        self.play(ReplacementTransform(lost, slow), run_time=0.4)
        arr = np.array([1 / (1 / 0.75 + 0.4 * t) for t in np.linspace(0, T_, 801)])
        curve = ax.plot(lambda t: p_at(arr, t, T_), x_range=[0, 10, 0.05], color=BLUE, stroke_width=5, use_smoothing=False)
        self.at("Occupancy starts at")
        self.play(FadeIn(pt0), run_time=0.3)
        tr = ValueTracker(0)
        def upd(g):
            n = int(round(p_at(arr, tr.get_value(), T_) * 100))
            apply_mask(g, mask_n(n))
        dots.add_updater(upd)
        self.at("falls by")
        self.play(Create(curve, rate_func=linear), tr.animate.set_value(10).set_rate_func(linear), run_time=2.6)
        dots.remove_updater(upd)
        end = Dot(ax.c2p(10, 1 / (1 / 0.75 + 4)), color=BLUE, radius=0.1)
        tl = M("0.19 at 10 years", 26, BLUE).move_to(ax.c2p(10.5, 0.62))
        lead = Line(tl.get_bottom() + DOWN * 0.05, end.get_top(), color=BLUE, stroke_width=2)
        self.at("After 10 years")
        self.play(FadeIn(end), FadeIn(tl), Create(lead), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        ctr = [-3.9, -0.1]
        dots = make_grid(ctr, sp=0.58, r=0.23)
        mask = mask_n(19)
        apply_mask(dots, mask)
        head = M("c = e", 34, TEXT).move_to([-3.9, 3.2, 0])
        cap = T("ten years on, in this sketch", 24, GREY).move_to([-3.9, -3.4, 0])
        ax, labs = make_axes([3.9, -0.1], 5.0, 4.0)
        arr = np.array([1 / (1 / 0.75 + 0.4 * t) for t in np.linspace(0, 20, 801)])
        curve = ax.plot(lambda t: p_at(arr, t, 20.0), x_range=[0, 10, 0.05], color=BLUE, stroke_width=5, use_smoothing=False)
        end = Dot(ax.c2p(10, 1 / (1 / 0.75 + 4)), color=BLUE, radius=0.1)
        plot = VGroup(ax, labs, curve, end)
        self.at("past its threshold")
        self.play(FadeIn(dots), FadeIn(head), FadeIn(cap), FadeIn(plot), run_time=0.7)
        q = T("persisting?", 44, GOLD, weight=BOLD).move_to([3.9, 3.35, 0])
        lit = [dots[i] for i, m in enumerate(mask) if m]
        self.at("seeing animals")
        self.play(*[Indicate(d, color=GREEN, scale_factor=1.35) for d in lit], FadeIn(q, shift=LEFT * 0.2), run_time=0.9)
        chips = VGroup(chip("identical patches", GREY, 30), chip("all equally reachable", GREY, 30),
                       chip("constant rates", GREY, 30)).arrange(DOWN, buff=0.4).move_to([3.9, 0.0, 0])
        self.at("The model is simple")
        self.play(FadeOut(q), FadeOut(plot), run_time=0.4)
        self.at("identical patches")
        self.play(FadeIn(chips[0], shift=LEFT * 0.2), run_time=0.4)
        self.at("equally reachable")
        self.play(FadeIn(chips[1], shift=LEFT * 0.2), run_time=0.4)
        self.at("constant rates")
        self.play(FadeIn(chips[2], shift=LEFT * 0.2), run_time=0.4)
        rr = np.random.RandomState(3)
        sc = rr.choice([0.5, 0.75, 1.0, 1.2], size=N * N)
        self.at("big and small patches")
        self.play(*[d.animate.scale(float(s)) for d, s in zip(dots, sc)], FadeOut(chips), run_time=1.0)
        self.at("The rule to keep")
        self.play(FadeOut(dots), FadeOut(head), FadeOut(cap), run_time=0.5)
        col = VGroup(T("colonization", 54, YELLOW, weight=BOLD), M(">", 72, TEXT), T("extinction", 54, RED, weight=BOLD)).arrange(RIGHT, buff=0.6)
        col.move_to([0, 0.7, 0])
        res = T("the region persists", 56, GREEN, weight=BOLD).move_to([0, -1.0, 0])
        self.at("colonization outpaces")
        self.play(FadeIn(col, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "A region persists when colonization outpaces local extinction."
