"""Enzymes at work: an enzyme works only while its active site keeps its shape (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the enzyme (catalase, bromelain)
  YELLOW = the substrate (hydrogen peroxide; the protein chains of gelatin)
  GREEN  = products, "works", the enzyme unchanged
  RED    = denatured enzyme, "does not fit"
  ORANGE = heat, temperature
  TEAL   = activation energy (the hill)
  PURPLE = pH and electric charge
  GOLD   = pineapple pieces
  GREY   = outlines, bowls, axes, weak attractions
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


# the enzyme: a labelled block with a pocket (the active site) cut into its top edge
ENZ_PTS = [(-1.8, -1.0), (1.8, -1.0), (1.8, 1.0), (0.65, 1.0), (0.45, 0.2), (-0.45, 0.2), (-0.65, 1.0), (-1.8, 1.0)]
# the same block after it has lost its shape: pocket closed up and slanted, body bulged
ENZ_BAD = [(-1.9, -1.1), (1.7, -0.8), (2.0, 0.7), (0.95, 0.9), (0.85, 0.55), (0.35, 0.5), (0.0, 0.95), (-1.6, 1.1)]


def enzyme(color=BLUE, s=1.0, pts=ENZ_PTS, fill=0.28):
    p = Polygon(*[np.array([x, y, 0.0]) for x, y in pts], stroke_color=color, stroke_width=4,
                fill_color=color, fill_opacity=fill).round_corners(0.12)
    return p.scale(s)


def piece(color=YELLOW, s=1.0):
    """substrate: a block shaped to fit the pocket (a schematic shape, not a molecule)."""
    pts = [(-0.6, 0.37), (0.6, 0.37), (0.4, -0.37), (-0.4, -0.37)]
    p = Polygon(*[np.array([x, y, 0.0]) for x, y in pts], stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.55).round_corners(0.06)
    return p.scale(s)


def pocket_at(enz_center, s=1.0):
    return np.array(enz_center) + np.array([0.0, 0.6 * s, 0.0])


def wavy(x0, x1, y, amp=0.12, freq=3.0, ph=0.0, tilt=0.0, color=YELLOW, w=4):
    xc = (x0 + x1) / 2
    return ParametricFunction(lambda t: np.array([t, y + amp * np.sin(freq * t + ph) + tilt * (t - xc), 0]),
                              t_range=[x0, x1], color=color, stroke_width=w, use_smoothing=False)


BOWL_Y = -0.2
BOWL_W, BOWL_H = 5.0, 3.0
BX = (-3.4, 3.4)


def bowl(cx):
    return RoundedRectangle(corner_radius=0.3, width=BOWL_W, height=BOWL_H, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.08).move_to([cx, BOWL_Y, 0])


def loose_chains(cx):
    """five loose chains (gelatin before it sets)."""
    g = VGroup()
    for k in range(5):
        y = BOWL_Y - 0.9 + 0.38 * k
        g.add(wavy(cx - 2.0, cx + 2.0, y, amp=0.09, freq=2.6 + 0.3 * k, ph=0.7 * k))
    return g


def net_chains(cx):
    """the same five chains tangled into a net (same point count, so they can transform)."""
    g = VGroup()
    for k in range(5):
        y = BOWL_Y - 0.55
        tilt = [0.22, -0.22, 0.12, -0.12, 0.0][k]
        g.add(wavy(cx - 2.0, cx + 2.0, y, amp=0.3, freq=3.0 + 0.9 * k, ph=1.1 * k, tilt=tilt))
    return g


def cut_chains(cx):
    """chains cut into short pieces: built from the loose ones, then broken into fragments."""
    g = VGroup()
    for k in range(5):
        y = BOWL_Y - 0.9 + 0.38 * k
        ph = 0.7 * k
        fr = 2.6 + 0.3 * k
        for a, b in [(-2.0, -1.45), (-1.15, -0.5), (-0.2, 0.55), (0.85, 1.4), (1.7, 2.0)]:
            g.add(wavy(cx + a + 0.04 * k, cx + b + 0.04 * k, y, amp=0.09, freq=fr, ph=ph, w=4))
    return g


def pine_bits(cx):
    return VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.42, height=0.42, stroke_color=GOLD, stroke_width=3,
                                     fill_color=GOLD, fill_opacity=0.7).move_to([cx - 1.0 + 1.0 * i, BOWL_Y + 1.05, 0])
                    for i in range(3)])


def label(text, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw)


def axes_lines(x0, x1, y0, y1):
    ax = Arrow([x0, y0, 0], [x1, y0, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    ay = Arrow([x0, y0, 0], [x0, y1, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    return VGroup(ax, ay)


def sstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


class S00Title(TitleCard):
    LESSON = "Enzymes at work"
    TITLE = "Enzymes only work in shape"


# ---------------------------------------------------------------------------------------------
class S01Pineapple(SpokenScene):
    """fresh pineapple: gelatin stays runny; canned: it sets as the chains tangle into a net; the question."""

    def construct(self):
        bl, br = bowl(BX[0]), bowl(BX[1])
        tl = label("fresh pineapple", 32, GOLD).move_to([BX[0], 2.4, 0])
        tr = label("canned pineapple", 32, GOLD).move_to([BX[1], 2.4, 0])
        bitsL, bitsR = pine_bits(BX[0]), pine_bits(BX[1])
        st_l = label("gelatin stays runny", 30).move_to([BX[0], -2.3, 0])
        st_r = label("gelatin sets", 30).move_to([BX[1], -2.3, 0])

        self.at("Stir fresh pineapple", lead=0.0)
        self.play(FadeIn(bl), FadeIn(tl), FadeIn(bitsL, shift=DOWN * 0.6), run_time=0.9)
        self.at("runny")
        self.play(FadeIn(st_l), run_time=0.5)
        self.at("canned pineapple")
        self.play(FadeIn(br), FadeIn(tr), FadeIn(bitsR, shift=DOWN * 0.6), run_time=0.9)
        self.at("it sets")
        self.play(FadeIn(st_r), run_time=0.5)

        chip_g = chip("gelatin is a protein", YELLOW, size=26).move_to([0, 3.15, 0])
        chL, chR = loose_chains(BX[0]), loose_chains(BX[1])
        self.at("Gelatin is a protein")
        self.play(FadeIn(chip_g, shift=DOWN * 0.1), Create(chL), Create(chR), run_time=1.2)
        self.at("tangle into a net")
        st_r2 = label("long chains tangle into a net", 28).move_to([BX[1], -2.3, 0])
        self.play(Transform(chR, net_chains(BX[1])), ReplacementTransform(st_r, st_r2), run_time=1.6)
        self.at("traps water")
        self.play(Indicate(chR, color=YELLOW, scale_factor=1.05), run_time=1.0)

        qL = chip("What is in it?", GOLD, size=30).move_to([BX[0], -3.1, 0])
        qR = chip("What did canning change?", ORANGE, size=30).move_to([BX[1], -3.1, 0])
        self.at("What is in fresh pineapple")
        self.play(FadeIn(qL, shift=UP * 0.1), run_time=0.6)
        self.at("what did canning change")
        self.play(FadeIn(qR, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Enzyme(SpokenScene):
    """metabolism = all the reactions; far too slow alone; an enzyme (a protein) speeds one up and is not used up."""

    def construct(self):
        cell = Ellipse(width=9.6, height=4.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06)
        cell.move_to([0, 0.4, 0])
        rng = np.random.RandomState(4)
        spots = [(-3.2, 1.2), (-1.0, 1.5), (1.4, 1.4), (3.1, 0.9), (-3.4, -0.5), (-0.9, -0.2), (1.5, -0.3), (3.2, -0.9),
                 (-2.0, -1.0), (0.2, 0.6)]
        mini = VGroup()
        for x, y in spots:
            a = Dot([x - 0.5, y, 0], radius=0.11, color=YELLOW)
            b = Dot([x + 0.5, y, 0], radius=0.11, color=GREEN)
            ar = arr([x - 0.32, y, 0], [x + 0.3, y, 0], GREY, w=3, tip=0.14)
            mini.add(VGroup(a, ar, b))
        title = label("Metabolism", 44, TEXT).move_to([0, 3.15, 0])
        sub = label("all the chemical reactions in a living thing", 30, GREY).move_to([0, -2.4, 0])
        self.at("Metabolism means", lead=0.0)
        self.play(FadeIn(title), Create(cell), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in mini], lag_ratio=0.06), run_time=0.9)
        self.at("all the chemical reactions")
        self.play(FadeIn(sub), run_time=0.6)

        # --- zoom to one reaction -----------------------------------------------------------------
        a0 = Dot([-4.0, 0.2, 0], radius=0.34, color=YELLOW)
        a0.set_fill(YELLOW, 0.9)
        b0 = Dot([4.0, 0.2, 0], radius=0.34, color=GREEN)
        b0.set_fill(GREEN, 0.25)
        rx = arr([-3.4, 0.2, 0], [3.4, 0.2, 0], GREY, w=6, tip=0.3)
        rxl = label("one reaction", 28, GREY).move_to([0, 0.8, 0])
        bar_o = RoundedRectangle(corner_radius=0.15, width=8.0, height=0.45, stroke_color=GREY, stroke_width=3)
        bar_o.move_to([0.4, -1.75, 0])
        bar_f = Rectangle(width=0.4, height=0.45, stroke_width=0, fill_color=RED, fill_opacity=0.9)
        bar_f.align_to(bar_o, LEFT).align_to(bar_o, DOWN).shift(RIGHT * 0.0)
        bar_lbl = label("speed", 28, GREY).next_to(bar_o, LEFT, buff=0.3)
        slow = label("body temperature, no help: far too slow", 28, RED).move_to([0, -2.6, 0])
        self.at("Many would be far too slow")
        self.play(FadeOut(cell), FadeOut(mini), FadeOut(title), FadeOut(sub),
                  FadeIn(a0), FadeIn(b0), GrowArrow(rx), FadeIn(rxl), Create(bar_o), FadeIn(bar_lbl), run_time=1.0)
        self.play(FadeIn(bar_f), FadeIn(slow), run_time=0.6)

        enz = chip("enzyme", BLUE, size=36).move_to([0, 1.7, 0])
        fast = label("with the enzyme: faster", 28, GREEN).move_to([0, -2.6, 0])
        self.at("comes from enzymes")
        self.play(FadeIn(enz, shift=DOWN * 0.2), run_time=0.6)
        self.play(bar_f.animate.stretch_to_fit_width(7.9).align_to(bar_o, LEFT).set_fill(GREEN),
                  ReplacementTransform(slow, fast), run_time=1.0)

        prot = label("almost all enzymes are proteins", 28, BLUE).move_to([0, 2.65, 0])
        self.at("almost all of them")
        self.play(FadeIn(prot), run_time=0.6)

        cat = label("catalyst", 44, BLUE, weight=BOLD).move_to([0, 3.15, 0])
        self.at("is a catalyst")
        self.play(FadeOut(prot), FadeIn(cat, scale=0.9), run_time=0.7)

        self.at("without being used up")
        prod = Dot([4.0, 0.2, 0], radius=0.34, color=GREEN)
        prod.set_fill(GREEN, 0.9)
        keep = label("the enzyme is not used up", 28, GREEN).move_to([0, 2.5, 0])
        self.play(ReplacementTransform(a0, prod), FadeOut(b0), FadeIn(keep), Indicate(enz, color=GREEN, scale_factor=1.12),
                  run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Site(SpokenScene):
    """catalase: substrate fits the active site, becomes products, they leave, the enzyme is unchanged."""

    def construct(self):
        K = 1.4
        ec = np.array([0.0, -0.8, 0.0])
        enz = enzyme(BLUE, K).move_to(ec)
        enz_lbl = label("catalase", 40, BLUE, weight=BOLD).move_to(ec + np.array([0, -1.0, 0]))
        sub_start = np.array([-4.6, 1.2, 0.0])
        pk = pocket_at(ec, K)

        self.at("Take catalase", lead=0.0)
        self.play(FadeIn(enz, shift=UP * 0.2), FadeIn(enz_lbl), run_time=0.9)

        sub = piece(YELLOW, 1.2).move_to(sub_start)
        sl1 = label("substrate", 32, YELLOW).move_to([-4.6, 2.2, 0])
        sl2 = label("hydrogen peroxide", 28, YELLOW).move_to([-4.6, 0.3, 0])
        self.at("The substrate is")
        self.play(FadeIn(sub, scale=0.8), FadeIn(sl1), run_time=0.7)
        self.at("hydrogen peroxide")
        self.play(FadeIn(sl2), run_time=0.5)

        self.at("fits into")
        self.play(sub.animate.move_to([0, 1.7, 0]), run_time=0.6)
        self.play(sub.animate.move_to(pk), run_time=0.6)
        asl = label("active site", 36, BLUE, weight=BOLD).move_to([4.2, 2.3, 0])
        asa = arr([3.1, 2.0, 0], [1.0, 0.35, 0], BLUE, w=5)
        self.at("active site")
        self.play(FadeIn(asl), GrowArrow(asa), run_time=0.6)
        self.at("small pocket")
        self.play(Indicate(enz, color=TEXT, scale_factor=1.03), run_time=0.9)

        w1 = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.46, stroke_color=GREEN, stroke_width=3,
                              fill_color=GREEN, fill_opacity=0.6).move_to(pk + LEFT * 0.3)
        o1 = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.46, stroke_color=GREEN, stroke_width=3,
                              fill_color=GREEN, fill_opacity=0.6).move_to(pk + RIGHT * 0.3)
        prods = VGroup(w1, o1)
        self.at("changes it into products")
        self.play(ReplacementTransform(sub, prods), run_time=0.9)

        pl = label("products", 32, GREEN).move_to([4.5, 0.2, 0])
        wl = label("water", 30, GREEN).move_to([3.7, -2.1, 0])
        ol = label("oxygen", 30, GREEN).move_to([5.3, -2.1, 0])
        self.at("water and oxygen")
        self.play(FadeIn(pl), run_time=0.5)
        self.at("The products leave")
        self.play(w1.animate.scale(1.8).move_to([3.7, -1.2, 0]), o1.animate.scale(1.8).move_to([5.3, -1.2, 0]),
                  FadeIn(wl), FadeIn(ol), run_time=1.3)

        un = label("enzyme unchanged", 32, GREEN).move_to([0, -3.1, 0])
        self.at("is unchanged")
        self.play(FadeIn(un), Indicate(enz, color=GREEN, scale_factor=1.04), run_time=0.9)
        sub2 = piece(YELLOW, 1.2).move_to(sub_start)
        self.at("another substrate molecule")
        self.play(FadeIn(sub2, scale=0.8), run_time=0.3)
        self.play(sub2.animate.move_to([0, 1.7, 0]), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def hill_fn(X, H):
    """energy along a reaction (relative, in this sketch): starts high, ends lower, with a hill between."""
    return 0.9 - 0.55 * sstep((X - 0.5) / 0.35 + 0.5) + H * np.exp(-((X - 0.45) / 0.13) ** 2)


HX0, HX1 = -5.0, 5.0
HY0, HSC = -2.1, 1.45


def hpt(X, H):
    return np.array([HX0 + (HX1 - HX0) * X, HY0 + HSC * hill_fn(X, H), 0.0])


def hill(H, color):
    return ParametricFunction(lambda t: hpt(t, H), t_range=[0, 1], color=color, stroke_width=6, use_smoothing=False)


class S04Hill(SpokenScene):
    """energy hill sketch: the ball must be pushed over it; the enzyme lowers it; more substrate reacts."""

    def construct(self):
        ax = axes_lines(-5.6, 5.6, -2.5, 3.0)
        yl = label("energy (relative)", 26, GREY).rotate(PI / 2).move_to([-6.1, 0.3, 0])
        xl = label("reaction progress", 26, GREY).move_to([0, -3.05, 0])
        note = label("a sketch, not measured data", 24, GREY).move_to([3.4, 3.1, 0])
        h_hi = hill(1.6, YELLOW)
        ball = Dot(hpt(0.04, 1.6), radius=0.26, color=YELLOW)
        ball.set_fill(YELLOW, 1)

        self.at("Picture a ball", lead=0.0)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(note), run_time=0.9)
        self.play(Create(h_hi), FadeIn(ball), run_time=1.2)

        self.at("pushed over a hill")
        push = arr([-5.2, -0.3, 0], [-4.35, -0.3, 0], YELLOW, w=6, tip=0.25)
        self.play(GrowArrow(push), run_time=0.3)
        up = ParametricFunction(lambda t: hpt(0.04 + 0.41 * t, 1.6), t_range=[0, 1])
        down = ParametricFunction(lambda t: hpt(0.45 + 0.5 * t, 1.6), t_range=[0, 1])
        self.play(MoveAlongPath(ball, up), FadeOut(push), run_time=1.0)
        self.play(MoveAlongPath(ball, down), run_time=0.6, rate_func=rush_into)

        pk = hpt(0.45, 1.6)
        base = hpt(0.04, 1.6)
        brk = DoubleArrow([pk[0] + 0.0, base[1], 0], [pk[0], pk[1] - 0.02, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
        brl = label("activation energy", 32, TEAL, weight=BOLD).move_to([pk[0] - 2.8, pk[1] + 0.75, 0])
        base_line = DashedLine([HX0 + 0.3, base[1], 0], [pk[0] + 0.4, base[1], 0], color=GREY, stroke_width=3)
        self.at("Activation energy")
        self.play(Create(base_line), GrowFromCenter(brk), FadeIn(brl), run_time=1.0)
        self.play(ball.animate.move_to(hpt(0.04, 1.6)), run_time=0.01)

        noadd = label("the enzyme adds no energy", 30, BLUE).move_to([3.4, 2.45, 0])
        self.at("does not add energy")
        self.play(FadeIn(noadd), run_time=0.6)

        # an enzyme cradles a substrate
        mini_e = enzyme(BLUE, 0.42).move_to([4.2, 2.15, 0])
        mini_s = piece(YELLOW, 0.42).move_to(pocket_at([4.2, 2.15, 0], 0.42))
        mini_l = label("enzyme holds the substrate", 26, BLUE).move_to([4.2, 1.45, 0])
        self.at("holds the substrate")
        self.play(FadeOut(noadd), FadeIn(mini_e), FadeIn(mini_s), FadeIn(mini_l), run_time=0.7)

        h_lo = hill(0.75, BLUE)
        ghost = hill(1.6, GREY)
        ghost.set_stroke(opacity=0.5)
        gl = label("without the enzyme", 26, GREY).move_to([1.5, 2.05, 0])
        pk2 = hpt(0.45, 0.75)
        brk2 = DoubleArrow([pk[0], base[1], 0], [pk[0], pk2[1] - 0.02, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
        self.at("lowers the hill")
        self.play(FadeIn(ghost), FadeIn(gl), ReplacementTransform(h_hi, h_lo), Transform(brk, brk2),
                  brl.animate.move_to([pk[0] - 2.8, pk2[1] + 0.75, 0]), run_time=1.6)

        balls = VGroup(*[Dot(hpt(0.04, 0.75), radius=0.2, color=YELLOW).set_fill(YELLOW, 1) for _ in range(4)])
        path = ParametricFunction(lambda t: hpt(0.04 + 0.92 * t, 0.75), t_range=[0, 1])
        self.at("more substrate reacts")
        self.play(FadeOut(ball), FadeIn(balls), run_time=0.2)
        self.play(LaggedStart(*[MoveAlongPath(b, path) for b in balls], lag_ratio=0.3), run_time=3.2,
                  rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
def rate_fn(u):
    """rate against temperature (relative, in this sketch): rises, peaks, then falls steeply. u in 0..1."""
    return np.exp(3.2 * u) / (1 + np.exp((u - 0.62) / 0.045))


_US = np.linspace(0, 1, 400)
_PK = float(_US[np.argmax([rate_fn(u) for u in _US])])
_RMAX = rate_fn(_PK)
PX0, PX1 = 0.2, 6.2
PY0, PY1 = -1.9, 2.4


def ppt(u):
    return np.array([PX0 + (PX1 - PX0) * u, PY0 + (PY1 - PY0) * 0.92 * rate_fn(u) / _RMAX, 0.0])


class S05Heat(SpokenScene):
    """rate rises with temperature, peaks at the optimum, then falls as the enzyme loses its shape."""

    def construct(self):
        ec = np.array([-4.2, 0.4, 0.0])
        s = 1.0
        enz = enzyme(BLUE, s).move_to(ec)
        sub = piece(YELLOW, s).move_to(pocket_at(ec, s))
        elbl = label("enzyme", 32, BLUE).move_to(ec + np.array([0, -1.45, 0]))
        ax = axes_lines(PX0, PX1 + 0.3, PY0, PY1 + 0.6)
        xl = label("temperature", 30, ORANGE).move_to([3.3, -3.3, 0])
        yl = label("rate (relative)", 26, GREY).rotate(PI / 2).move_to([-0.35, 0.3, 0])
        note = label("a sketch", 24, GREY).move_to([5.5, 3.0, 0])

        rise = ParametricFunction(lambda t: ppt(t * _PK), t_range=[0, 1], color=ORANGE, stroke_width=6, use_smoothing=False)
        fall = ParametricFunction(lambda t: ppt(_PK + t * (0.9 - _PK)), t_range=[0, 1], color=RED, stroke_width=6,
                                  use_smoothing=False)

        self.add(enz, sub, elbl)
        self.at("Warmer molecules", lead=0.0)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(note), Wiggle(sub, scale_value=1.15, rotation_angle=0.06 * TAU),
                  run_time=1.2)
        self.at("up to a point")
        self.play(Create(rise), run_time=2.2, rate_func=linear)

        # weak attractions hold the shape, then heat shakes them apart
        dashes = VGroup(*[DashedLine(ec + np.array([-1.3 * s, -0.2 - 0.3 * k, 0]), ec + np.array([1.3 * s, -0.2 - 0.3 * k, 0]),
                                     color=GREY, stroke_width=3, dash_length=0.12) for k in range(3)])
        dl = label("weak attractions", 26, GREY).move_to(ec + np.array([0, 1.6, 0]))
        self.at("too much heat")
        self.play(Create(fall), Wiggle(enz, scale_value=1.05, rotation_angle=0.03 * TAU), run_time=1.6, rate_func=linear)
        self.at("weak attractions")
        self.play(Create(dashes), FadeIn(dl), run_time=0.5)
        bad = enzyme(RED, s, pts=ENZ_BAD).move_to(ec)
        self.play(FadeOut(dashes, shift=DOWN * 0.1), FadeOut(dl), ReplacementTransform(enz, bad),
                  sub.animate.move_to(ec + np.array([-0.1, 1.5 * s + 0.15, 0])), elbl.animate.set_color(RED), run_time=1.4)

        den = label("denatured enzyme", 32, RED, weight=BOLD).move_to(ec + np.array([0, -1.45, 0]))
        self.at("To denature")
        self.play(ReplacementTransform(elbl, den), run_time=0.5)
        home = sub.get_center().copy()
        self.play(sub.animate.move_to(ec + np.array([0.3, 0.95, 0])), run_time=0.7)
        self.play(sub.animate.move_to(home + LEFT * 0.4 + UP * 0.2), run_time=0.7)
        self.at("is not dead")
        self.play(Indicate(bad, color=RED, scale_factor=1.03), run_time=0.8)
        self.play(sub.animate.move_to(ec + np.array([0.3, 0.95, 0])), run_time=0.7)
        self.play(sub.animate.move_to(home + LEFT * 0.4 + UP * 0.2), run_time=0.7)
        nf = label("active site no longer fits", 28, RED).move_to(ec + np.array([0, -2.15, 0]))
        self.at("no longer fits")
        self.play(FadeIn(nf), sub.animate.move_to(ec + np.array([0.3, 0.95, 0])), run_time=0.7)
        self.play(sub.animate.move_to(home + LEFT * 0.4 + UP * 0.2), run_time=0.7)

        pkp = ppt(_PK)
        mk = Dot(pkp, radius=0.14, color=TEXT)
        dline = DashedLine(pkp, [pkp[0], PY0, 0], color=GREY, stroke_width=3)
        opt = label("optimum", 32, TEXT, weight=BOLD).move_to([pkp[0] - 0.1, pkp[1] + 0.45, 0])
        self.at("The optimum")
        self.play(FadeIn(mk, scale=1.8), Create(dline), FadeIn(opt), run_time=0.9)
        t37 = label("37 °C", 30, TEXT).move_to([pkp[0], PY0 - 0.4, 0])
        t37b = label("most human enzymes", 26, TEXT).move_to([pkp[0], PY0 - 0.8, 0])
        self.at("Most human enzymes")
        self.play(FadeIn(t37), FadeIn(t37b), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """a best pH (charges); back to the pineapple: bromelain cuts the chains; canning denatures it; the rule."""

    def construct(self):
        # --- pH strip --------------------------------------------------------------------------
        strip = VGroup(*[Rectangle(width=0.62, height=0.5, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE,
                                   fill_opacity=0.12 + 0.05 * i).move_to([-4.65 + 0.62 * i + 0.31, 2.6, 0]) for i in range(15)])
        strip.move_to([0.6, 2.7, 0])
        ticks = VGroup(*[label(str(n), 26, PURPLE).next_to(strip[n], UP, buff=0.15) for n in (0, 7, 14)])
        phl = label("pH", 36, PURPLE, weight=BOLD).next_to(strip, LEFT, buff=0.35)
        marker = Triangle(color=PURPLE, fill_opacity=1, stroke_width=0).scale(0.18).move_to(strip[7].get_bottom() + DOWN * 0.22)
        best = label("each enzyme has a best pH", 30, PURPLE).move_to([0, 1.55, 0])
        self.at("Each enzyme also", lead=0.0)
        self.play(FadeIn(strip), FadeIn(ticks), FadeIn(phl), FadeIn(marker), run_time=0.9)
        self.at("a best")
        self.play(FadeIn(best), run_time=0.5)

        ec = np.array([0.0, -1.0, 0.0])
        enz = enzyme(BLUE, 1.0).move_to(ec)
        pkc = pocket_at(ec, 1.0)

        def badge(sign, pos, col=PURPLE):
            c = Circle(radius=0.18, stroke_width=0, fill_color=col, fill_opacity=1)
            return VGroup(c, T(sign, 24, BG, weight=BOLD).move_to(c)).move_to(pos)

        plus = VGroup(badge("+", pkc + np.array([-0.2, -0.1, 0])), badge("+", pkc + np.array([0.2, -0.1, 0])))
        sub = piece(YELLOW, 0.9).move_to(pkc + np.array([3.2, 1.2, 0]))
        minus = VGroup(badge("\u2212", sub.get_center() + np.array([-0.2, 0, 0])), badge("\u2212", sub.get_center() + np.array([0.2, 0, 0])))
        chg = label("electric charges", 30, PURPLE).move_to([0, -2.75, 0])
        self.at("changes electric charges")
        self.play(FadeIn(enz), FadeOut(best), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(plus), FadeIn(minus), FadeIn(chg), marker.animate.move_to(strip[3].get_bottom() + DOWN * 0.22), run_time=0.9)
        near = pkc + np.array([0.0, 1.15, 0])
        pull = arr(near + np.array([0, -0.15, 0]), pkc + np.array([0, 0.5, 0]), GREEN, w=4, tip=0.16)
        sub_grp = VGroup(sub, minus)
        self.play(sub_grp.animate.shift(near - sub.get_center()), run_time=0.8)
        self.play(GrowArrow(pull), run_time=0.3)
        self.at("may no longer attract")
        chg2 = label("charges change, so they may no longer attract", 28, PURPLE).move_to([0, -2.75, 0])
        sk = label("in this sketch", 24, GREY).move_to([0, -3.3, 0])
        self.play(plus.animate.set_opacity(0.55), pull.animate.set_color(GREY).set_opacity(0.6),
                  sub_grp.animate.shift(RIGHT * 0.5 + UP * 0.15), ReplacementTransform(chg, chg2), FadeIn(sk), run_time=1.0)

        # --- back to the pineapple -----------------------------------------------------------------
        self.at("Back to the pineapple")
        old = VGroup(strip, ticks, phl, marker, enz, sub, plus, minus, chg2, pull, sk)
        self.play(FadeOut(old), run_time=0.6)
        bl, br = bowl(BX[0]), bowl(BX[1])
        tl = label("fresh pineapple", 32, GOLD).move_to([BX[0], 2.75, 0])
        tr = label("canned pineapple", 32, GOLD).move_to([BX[1], 2.75, 0])
        bitsL, bitsR = pine_bits(BX[0]), pine_bits(BX[1])
        chL, chR = loose_chains(BX[0]), loose_chains(BX[1])
        self.play(FadeIn(bl), FadeIn(br), FadeIn(tl), FadeIn(tr), FadeIn(bitsL), FadeIn(bitsR), FadeIn(chL), FadeIn(chR),
                  run_time=0.8)

        brom = chip("bromelain", BLUE, size=28).move_to([BX[0], 1.95, 0])
        self.at("contains bromelain")
        self.play(FadeIn(brom, shift=DOWN * 0.15), run_time=0.6)
        cutl = cut_chains(BX[0])
        stl = label("chains cut: no net, runny", 28).move_to([BX[0], -2.3, 0])
        self.at("cuts the protein chains")
        self.play(ReplacementTransform(chL, cutl), FadeIn(stl), Indicate(brom, color=BLUE, scale_factor=1.1), run_time=1.4)

        heat = label("canning heat", 30, ORANGE, weight=BOLD).move_to([BX[1], 1.95, 0])
        self.at("Canning heats")
        self.play(FadeIn(heat, shift=DOWN * 0.15), run_time=0.6)
        brom2 = chip("denatured bromelain", RED, size=26).move_to([BX[1], 1.95, 0])
        self.at("denature bromelain")
        self.play(ReplacementTransform(heat, brom2), run_time=0.9)
        str_ = label("gelatin sets", 28).move_to([BX[1], -2.3, 0])
        self.at("canned gelatin sets")
        self.play(Transform(chR, net_chains(BX[1])), FadeIn(str_), run_time=1.5)
        self.finish()


class S07End(EndCard):
    LINE = "An enzyme works only while its active site keeps its shape."
