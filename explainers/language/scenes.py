"""Language and lateralization: same rates, different base rate  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every number is the lesson's own (Knecht and colleagues 2000, 326 healthy adults, functional
transcranial Doppler: right-hemisphere dominance in 4% of strong right-handers, 15% of ambidextrous
people, 27% of strong left-handers) and its worked problem (100 + 100 assumed people; then 90% / 10%).
"Right" and "left" here are the PERSON'S OWN handedness; no hemisphere or pathway is drawn.

COLOR MAP (one color per concept, whole video)
  BLUE   = strong right-handers (the group)
  YELLOW = strong left-handers (the group)
  GREY   = ambidextrous people, structure, axes, de-emphasized
  GREEN  = the computed probability (the answer to "how likely is it that this person is left-handed?")
  RED    = the wrong conclusion (crossed out)
  A filled dot = right-hemisphere language dominance; a hollow dim dot = not right-dominant
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def dot(color, lit, r=0.12):
    return Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=1.0 if lit else 0.0).set_stroke(opacity=1.0 if lit else 0.35)


def lit_idx(n_lit, seed, n=100):
    return sorted(np.random.RandomState(seed).choice(n, n_lit, replace=False).tolist())


def grid(color, lit, center, sp=0.4, r=0.13):
    """10 x 10 icon array; dots in `lit` are right-dominant. Row-major from the top left."""
    dots = VGroup()
    for k in range(100):
        row, col = divmod(k, 10)
        d = dot(color, k in lit, r)
        d.move_to([center[0] + (col - 4.5) * sp, center[1] + (4.5 - row) * sp, 0])
        dots.add(d)
    return dots


def light(d, color):
    return d.animate.set_fill(color, 1.0).set_stroke(color, opacity=1.0)


def bartxt(text, size=26, color=GREY):
    return T(text, size, color)


def pool_positions(n, cx, cy, sp=0.5, cols=6):
    rows = int(np.ceil(n / cols))
    pts = []
    for k in range(n):
        row, col = divmod(k, cols)
        pts.append([cx + (col - (cols - 1) / 2) * sp, cy + ((rows - 1) / 2 - row) * sp, 0])
    return pts


RIGHT_LIT = lit_idx(4, 3)     # 4 of 100 strong right-handers
LEFT_LIT = lit_idx(27, 7)     # 27 of 100 strong left-handers
GX = 3.7                      # grid centres in scenes 3 and 4
GY = 0.2


class S00Title(TitleCard):
    LESSON = "Language and lateralization"
    TITLE = "Same rates, different base rate"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """100 strong left-handers, 27 lit; the tempting conclusion is crossed out."""

    def construct(self):
        self.at("Language is left")
        g = grid(YELLOW, [], [-3.3, -0.1], sp=0.42, r=0.14)
        lab = T("per 100 strong left-handers", 28, YELLOW).next_to(g, UP, buff=0.4)
        self.play(FadeIn(g), FadeIn(lab), run_time=0.8)

        self.at("326 healthy adults")
        study = chip("study: 326 healthy adults", GREY, size=26).move_to([3.0, 2.5, 0])
        self.play(FadeIn(study, shift=DOWN * 0.15), run_time=0.6)

        self.at("appeared in about")
        self.play(LaggedStart(*[light(g[k], YELLOW) for k in LEFT_LIT], lag_ratio=0.12), run_time=3.0)
        count = M("27 of 100", 60, YELLOW).move_to([3.0, 0.9, 0])
        what = T("right-hemisphere dominance", 28, TEXT).next_to(count, DOWN, buff=0.3)
        self.play(FadeIn(count, scale=0.9), FadeIn(what), run_time=0.7)
        leg = VGroup(dot(YELLOW, True, 0.12), T("filled = right-hemisphere dominance", 22, GREY))
        leg[0].move_to([-5.1, -2.75, 0]); leg[1].next_to(leg[0], RIGHT, buff=0.2)

        self.at("Does that make")
        q = T("most left-handers are right-dominant?", 30, TEXT).move_to([3.0, -0.75, 0])
        fit(q, max_w=6.2)
        self.play(FadeIn(q, shift=UP * 0.1), FadeIn(leg), run_time=0.7)

        self.at("It does not")
        cross = Cross(q, stroke_color=RED, stroke_width=5).scale(1.0)
        no = T("No", 40, RED, weight=BOLD).next_to(q, DOWN, buff=0.3)
        self.play(Create(cross), FadeIn(no), run_time=0.7)

        self.at("base rate")
        br = T("the base rate", 40, GREEN, weight=BOLD).move_to([3.0, -2.5, 0])
        self.play(FadeIn(br, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Rates(SpokenScene):
    """scoring rule for fTCD (sketch), then the three measured rates."""

    def construct(self):
        self.at("How was dominance measured")
        head = T("How was dominance measured?", 34, font=TITLE_FONT).to_edge(UP, buff=0.45)
        self.play(Write(head), run_time=1.2)

        self.at("ultrasound over each temple")
        base_y = -2.3
        ax = Line([-4.4, base_y, 0], [4.4, base_y, 0], color=GREY, stroke_width=3)
        h0 = 1.4
        xl, xr = -3.0, 3.0
        bl = Rectangle(width=1.4, height=h0, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.35, stroke_width=3)
        br_ = Rectangle(width=1.4, height=h0, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.35, stroke_width=3)
        bl.move_to([xl, base_y + h0 / 2, 0]); br_.move_to([xr, base_y + h0 / 2, 0])
        ll = T("left middle cerebral artery", 24, TEXT).move_to([xl, base_y - 0.45, 0])
        lr = T("right middle cerebral artery", 24, TEXT).move_to([xr, base_y - 0.45, 0])
        note = T("blood-flow velocity; the person's own left and right; the scoring rule, in this sketch", 22, GREY).move_to([0, base_y - 0.95, 0])
        tl = VGroup()
        self.play(FadeIn(ax), FadeIn(bl), FadeIn(br_), FadeIn(ll), FadeIn(lr), FadeIn(tl), FadeIn(note), run_time=1.0)

        self.at("while people generated words")
        wg = chip("word generation", GOLD, size=26).move_to([0, -0.2, 0])
        self.play(FadeIn(wg, shift=DOWN * 0.1), run_time=0.5)
        self.at("functional transcranial Doppler")
        self.play(bl.animate.stretch_to_fit_height(3.2).move_to([xl, base_y + 1.6, 0]),
                  br_.animate.stretch_to_fit_height(2.2).move_to([xr, base_y + 1.1, 0]), run_time=1.4)
        self.at("scored as dominant")
        sc = T("rises more: scored dominant", 26, GREEN, weight=BOLD).next_to(bl, UP, buff=0.3)
        self.play(FadeIn(sc, scale=0.9), bl.animate.set_stroke(GREEN).set_fill(GREEN, 0.35), run_time=0.7)

        # --- measured rates -------------------------------------------------------------------
        self.at("dominance appeared")
        self.play(FadeOut(VGroup(ax, bl, br_, ll, lr, note, tl, wg, sc, head)), run_time=0.6)
        h2 = T("Right-hemisphere dominance, by handedness", 32, font=TITLE_FONT).to_edge(UP, buff=0.45)
        yb = -2.2; ys = 0.115     # units per percent
        axis = Line([-5.2, yb, 0], [5.2, yb, 0], color=GREY, stroke_width=3)
        ylab = T("% of each group", 24, GREY).move_to([-4.0, 2.55, 0])
        xs = [-4.0, 0.0, 4.0]
        vals = [4, 15, 27]
        cols = [BLUE, GREY, YELLOW]
        names = ["strong right-handers", "ambidextrous people", "strong left-handers"]
        bars, labs, nums = [], [], []
        for x, v, c, n in zip(xs, vals, cols, names):
            b = Rectangle(width=1.8, height=0.02, stroke_color=c, fill_color=c, fill_opacity=0.4, stroke_width=3)
            b.move_to([x, yb + 0.01, 0])
            b.target = Rectangle(width=1.8, height=v * ys, stroke_color=c, fill_color=c, fill_opacity=0.4,
                                 stroke_width=3).move_to([x, yb + v * ys / 2, 0])
            bars.append(b)
            labs.append(T(n, 24, c).move_to([x, yb - 0.45, 0]))
            nums.append(M(f"{v}%", 44, c).move_to([x, yb + v * ys + 0.5, 0]))
        self.play(Write(h2), FadeIn(axis), FadeIn(ylab), *[FadeIn(b) for b in bars], *[FadeIn(l) for l in labs], run_time=0.8)
        self.play(MoveToTarget(bars[0]), FadeIn(nums[0]), run_time=0.9)
        self.at("ambidextrous people")
        self.play(MoveToTarget(bars[1]), FadeIn(nums[1]), run_time=0.9)
        self.at("of strong left")
        self.play(MoveToTarget(bars[2]), FadeIn(nums[2]), run_time=0.9)

        self.at("raises the odds")
        txt = T("raises the odds; does not make it typical", 28, TEXT).move_to([-2.2, 1.6, 0])
        self.play(FadeIn(txt, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Hundred(SpokenScene):
    """100 + 100 assumed people; 4 and 27 right-dominant; 31 in all."""

    def construct(self):
        self.at("Now")
        foot = T("group sizes assumed for the exercise, not measured", 24, GREY).move_to([0, 3.15, 0])
        gr = grid(BLUE, [], [-GX, GY])
        gl = grid(YELLOW, [], [GX, GY])
        lr_ = T("100 strong right-handers", 28, BLUE).move_to([-GX, GY + 2.4, 0])
        ll_ = T("100 strong left-handers", 28, YELLOW).move_to([GX, GY + 2.4, 0])
        self.play(FadeIn(gr), FadeIn(gl), FadeIn(lr_), FadeIn(ll_), run_time=1.0)

        self.at("fixed probabilities")
        rates = VGroup(M("4%", 34, BLUE).move_to([-GX, GY - 2.4, 0]), M("27%", 34, YELLOW).move_to([GX, GY - 2.4, 0]))
        rtag = T("study rates", 24, GREY).move_to([0, GY - 2.4, 0])
        self.play(FadeIn(rates), FadeIn(rtag), run_time=0.6)

        self.at("one dot")
        self.play(Indicate(gr, color=BLUE, scale_factor=1.03), Indicate(gl, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.at("Take")
        self.play(FadeIn(foot), run_time=0.5)

        self.at("Expect four")
        self.play(LaggedStart(*[light(gr[k], BLUE) for k in RIGHT_LIT], lag_ratio=0.2), run_time=1.0)
        c4 = M("4 right-dominant", 28, BLUE).move_to([-GX, GY - 2.95, 0])
        self.play(FadeIn(c4), run_time=0.4)
        self.at("27 of the left")
        self.play(LaggedStart(*[light(gl[k], YELLOW) for k in LEFT_LIT], lag_ratio=0.08), run_time=2.2)
        c27 = M("27 right-dominant", 28, YELLOW).move_to([GX, GY - 2.95, 0])
        self.play(FadeIn(c27), run_time=0.4)

        self.at("in all")
        tot = VGroup(M("4 + 27", 40, GREEN), M("= 31", 60, GREEN)).arrange(DOWN, buff=0.15).move_to([0, GY + 0.1, 0])
        self.play(FadeIn(tot, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Pick(SpokenScene):
    """The 31 right-dominant people gather: 27 of 31 are left-handers, but 27 of 100 left-handers are right-dominant."""

    def construct(self):
        gr = grid(BLUE, RIGHT_LIT, [-GX, GY])
        gl = grid(YELLOW, LEFT_LIT, [GX, GY])
        lr_ = T("100 strong right-handers", 28, BLUE).move_to([-GX, GY + 2.4, 0])
        ll_ = T("100 strong left-handers", 28, YELLOW).move_to([GX, GY + 2.4, 0])
        self.add(gr, gl, lr_, ll_)
        self.at("Now pick one")
        # the 31 lit dots (27 yellow, 4 blue) gather in a pool on the left
        pts = pool_positions(31, -GX, GY + 0.15, sp=0.55)
        movers = []
        for i, k in enumerate(LEFT_LIT):
            movers.append((gl[k].copy(), pts[i]))
        for j, k in enumerate(RIGHT_LIT):
            movers.append((gr[k].copy(), pts[27 + j]))
        copies = VGroup(*[m for m, _ in movers])
        head = T("31 right-dominant people", 28, TEXT).move_to([-GX, GY + 2.4, 0])
        self.add(copies)
        self.play(FadeOut(gr, run_time=0.8), FadeOut(lr_),
                  *[m.animate.move_to(p).scale(1.35) for m, p in movers], FadeIn(head), run_time=1.8)
        # the yellow grid stays but its dots that moved are echoed; keep the grid for the reverse question
        q1 = T("how many are left-handers?", 26, GREY).move_to([-GX, GY - 2.35, 0])
        self.at("How likely is it")
        self.play(FadeIn(q1), run_time=0.5)

        self.at("of the")
        e1 = M("27 / 31 = 87.1%", 36, GREEN).move_to([-GX, GY - 3.0, 0])
        self.play(*[copies[i].animate.set_fill(YELLOW, 1.0) for i in range(27)],
                  Indicate(VGroup(*copies[:27]), color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("That is")
        self.play(FadeIn(e1, scale=0.9), run_time=0.6)

        self.at("Yet only")
        q2 = T("how many are right-dominant?", 26, GREY).move_to([GX, GY - 2.35, 0])
        e2 = M("27 / 100 = 27%", 36, GREEN).move_to([GX, GY - 3.0, 0])
        self.play(FadeIn(q2), run_time=0.5)
        self.play(Indicate(VGroup(*[gl[k] for k in LEFT_LIT]), color=YELLOW, scale_factor=1.15), FadeIn(e2, scale=0.9), run_time=0.9)

        self.at("two different questions")
        ne = M("≠", 64, RED, weight=BOLD).move_to([0, GY - 3.0, 0])
        self.play(FadeIn(ne, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# area chart shared by scenes 5 and 6: width = share of the population, height = rate
# ---------------------------------------------------------------------------------------------
X0, XW = -5.0, 10.0       # chart spans x -5 .. 5 for a total share of 1
Y0 = -2.4                 # baseline
YS = 4.1 / 0.27           # units per unit rate (0.27 -> 3.8)
R_RIGHT, R_LEFT = 0.04, 0.27


def chart(tr):
    """Returns (blue block, yellow block, group labels, value labels) driven by tracker tr = share of left-handers."""
    def sl():
        return tr.get_value()

    def blue():
        w = XW * (1 - sl())
        return Rectangle(width=max(w, 1e-3), height=R_RIGHT * YS, stroke_color=BLUE, stroke_width=3,
                         fill_color=BLUE, fill_opacity=0.45).move_to([X0 + w / 2, Y0 + R_RIGHT * YS / 2, 0])

    def yel():
        w = XW * sl()
        return Rectangle(width=max(w, 1e-3), height=R_LEFT * YS, stroke_color=YELLOW, stroke_width=3,
                         fill_color=YELLOW, fill_opacity=0.45).move_to([X0 + XW - w / 2, Y0 + R_LEFT * YS / 2, 0])

    def glabs():
        s = sl()
        b = T(f"strong right-handers {round((1 - s) * 100)}%", 24, BLUE)
        b.move_to([X0 + XW * (1 - s) / 2, Y0 - 0.35, 0])
        y = T(f"strong left-handers {round(s * 100)}%", 24, YELLOW)
        y.move_to([min(X0 + XW - XW * s / 2, 6.2 - y.width / 2), Y0 - 0.8, 0])
        return VGroup(b, y)

    return always_redraw(blue), always_redraw(yel), always_redraw(glabs)


def values(tr):
    def f():
        s = tr.get_value()
        b = M(f"{1 - s:.2f} × 0.04 = {(1 - s) * 0.04:.3f}", 26, BLUE)
        b.move_to([X0 + XW * (1 - s) / 2, Y0 + R_RIGHT * YS + 0.4, 0])
        y = M(f"{s:.2f} × 0.27 = {s * 0.27:.3f}", 26, YELLOW)
        top = Y0 + R_LEFT * YS + 0.4
        y.move_to([min(X0 + XW - XW * s / 2, 6.2 - y.width / 2), top, 0])
        return VGroup(b, y)
    return always_redraw(f)


def rate_tags():
    g = VGroup()
    for r, c in ((R_RIGHT, BLUE), (R_LEFT, YELLOW)):
        y = Y0 + r * YS
        ln = DashedLine([X0, y, 0], [X0 + XW, y, 0], color=c, stroke_width=2, dash_length=0.12).set_stroke(opacity=0.5)
        tg = M(f"{round(r * 100)}%", 24, c).move_to([X0 - 0.62, y, 0])
        g.add(VGroup(ln, tg))
    return g


class S05Population(SpokenScene):
    """width = share of population, height = rate; the shares slide from 50/50 to 90/10."""

    def construct(self):
        tr = ValueTracker(0.5)
        bl, yl, gl_ = chart(tr)
        base = Line([X0, Y0, 0], [X0 + XW, Y0, 0], color=GREY, stroke_width=3)
        tags = rate_tags()
        key = T("width: share of the population      height: rate of right-hemisphere dominance", 22, GREY).move_to([0, 3.4, 0])
        fit(key, max_w=12.2)
        self.at("Now change only")
        self.play(FadeIn(base), FadeIn(bl), FadeIn(yl), FadeIn(gl_), FadeIn(key), run_time=0.9)
        self.add(tags)
        self.play(FadeIn(tags), run_time=0.5)

        self.at("Make it")
        self.play(tr.animate.set_value(0.1), run_time=3.2, rate_func=smooth)

        self.at("The rates stay the same")
        self.play(*[Indicate(t, color=GOLD, scale_factor=1.15) for t in tags], run_time=1.0)

        vals = values(tr)
        self.at("share of the population times")
        self.play(FadeIn(vals), run_time=0.7)
        self.at("handers contribute")
        self.play(Indicate(bl, color=BLUE, scale_factor=1.04), run_time=1.0)
        self.at("handers contribute", nth=1)
        self.play(Indicate(yl, color=YELLOW, scale_factor=1.04), run_time=1.0)

        self.at("Together")
        tot = M("0.036 + 0.027 = 0.063 = 6.3%", 32, GREEN).move_to([-1.2, 2.85, 0])
        self.play(FadeIn(tot, scale=0.92), run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    """same chart at 90/10: left-handers are 42.9% of the right-dominant; 87% fell to 43%."""

    def construct(self):
        tr = ValueTracker(0.1)
        bl, yl, gl_ = chart(tr)
        base = Line([X0, Y0, 0], [X0 + XW, Y0, 0], color=GREY, stroke_width=3)
        tags = rate_tags()
        vals = values(tr)
        key = T("width: share of the population      height: rate of right-hemisphere dominance", 22, GREY).move_to([0, 3.4, 0])
        fit(key, max_w=12.2)
        tot = M("0.036 + 0.027 = 0.063 = 6.3%", 32, GREEN).move_to([-1.2, 2.85, 0])
        self.add(base, bl, yl, gl_, tags, vals, key, tot)

        self.at("Pick a right dominant person")
        wl = 10 * 0.429
        wr = 10 - wl
        by = 2.85
        sy = Rectangle(width=wl, height=0.55, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.45, stroke_width=3)
        sb = Rectangle(width=wr, height=0.55, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.45, stroke_width=3)
        sy.move_to([-5 + wl / 2, by, 0]); sb.move_to([-5 + wl + wr / 2, by, 0])
        ty = T("left-handers 42.9%", 26, YELLOW).move_to(sy)
        tb = T("right-handers 57.1%", 26, BLUE).move_to(sb)
        tit = T("who the right-dominant people are", 22, GREY).move_to([0, 3.4, 0])
        self.play(FadeOut(tot), FadeOut(key), run_time=0.4)
        self.play(FadeIn(sy), FadeIn(sb), FadeIn(ty), FadeIn(tb), FadeIn(tit), run_time=0.8)

        self.at("The chance of being")
        eq = M("0.027 / 0.063 = 42.9%", 36, GREEN).move_to([-2.3, 0.5, 0])
        self.play(Indicate(sy, color=YELLOW, scale_factor=1.04), FadeIn(eq, scale=0.92), run_time=1.0)

        self.at("The rates did not change")
        self.play(*[Indicate(t, color=GOLD, scale_factor=1.15) for t in tags], run_time=0.9)
        self.at("The base rate did")
        self.play(Indicate(gl_, color=GOLD, scale_factor=1.06), run_time=0.9)

        self.at("the answer fell")
        fell = M("87% → 43%", 48, GREEN).move_to([-2.3, 0.5, 0])
        fell2 = M("87%  >  43%", 48, GREEN).move_to([-2.3, 0.5, 0])
        self.play(ReplacementTransform(eq, fell), run_time=0.8)

        self.at("more often found")
        mo = T("more often a right-hander", 26, BLUE).move_to([-2.3, -0.5, 0])
        self.play(FadeIn(mo, shift=UP * 0.1), Indicate(sb, color=BLUE, scale_factor=1.03), run_time=0.8)

        self.at("handedness shifts")
        st = VGroup(T("left-handedness shifts the odds", 28, TEXT), T("it does not reverse them", 28, TEXT)).arrange(DOWN, buff=0.2)
        st.move_to([-2.3, 0.0, 0])
        self.play(FadeOut(fell), FadeOut(mo), run_time=0.4)
        self.play(FadeIn(st, shift=UP * 0.1), run_time=0.7)

        self.at("Same rates")
        self.play(*[Indicate(t, color=GOLD, scale_factor=1.15) for t in tags], run_time=0.8)
        self.at("different base rate")
        self.play(Indicate(gl_, color=GOLD, scale_factor=1.06), run_time=0.8)
        self.at("different answer")
        self.play(Indicate(VGroup(sy, ty), color=GREEN, scale_factor=1.05), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Same rates, different base rate, different answer."
