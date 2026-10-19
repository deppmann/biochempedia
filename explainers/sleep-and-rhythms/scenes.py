"""Circadian rhythms and sleep: a clock that runs near 24 hours is reset by light every day.
(Biochemistrypedia neuroscience explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = CLOCK-BMAL1, the activating pair
  ORANGE = PER and CRY, the brake
  WHITE  = DNA elements (E-box, Per and Cry genes)
  TEAL   = the light pathway (melanopsin ganglion cell, tract, SCN)
  PURPLE = the clock's own time (internal day, its marker, its lag)
  YELLOW = light, and the light-driven shift of the clock
  PINK   = rods and cones
  GREEN  = on / switched on / the 24.00 h target
  RED    = inhibition (T-bar), blocked input
  GREY   = the external 24-hour day, membranes, outlines, de-emphasised text
Arrow types: solid arrow = drives / activates; T-bar = inhibits.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E879A8"
DNA = TEXT
LIGHT = YELLOW


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tbar(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def lamp(center, on=0.25, scale=1.0):
    core = Circle(radius=0.28 * scale, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=on)
    rays = VGroup(*[Line(UP * 0.4 * scale, UP * 0.6 * scale, color=YELLOW, stroke_width=3).rotate(k * PI / 4, about_point=ORIGIN)
                    for k in range(8)])
    return VGroup(core, rays).move_to(center)


class S00Title(TitleCard):
    LESSON = "Circadian rhythms and sleep"
    TITLE = "Light resets a slow clock"


# ---------------------------------------------------------------------------------------------
class S01Slow(SpokenScene):
    """28 h schedule bar, the internal-day bar a little shorter, near-coincident 24 h tick, the question."""

    def construct(self):
        X0, U = -5.8, 0.4  # left edge, units per hour
        lp = lamp([-5.6, 3.1, 0], on=0.15)
        lp_lbl = T("dim light", 26, YELLOW).next_to(lp, RIGHT, buff=0.3)

        # scheduled 28 h day
        sched = RoundedRectangle(corner_radius=0.12, width=28 * U, height=0.75, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.3).move_to([X0 + 14 * U, 1.1, 0])
        sched_lbl = T("scheduled day: 28 h", 28, GREY).next_to(sched, UP, buff=0.2).align_to(sched, LEFT)
        # internal day 24.18 h
        internal = RoundedRectangle(corner_radius=0.12, width=24.18 * U, height=0.75, stroke_color=PURPLE, stroke_width=3,
                                    fill_color=PURPLE, fill_opacity=0.35).move_to([X0 + 12.09 * U, -0.7, 0])
        int_lbl = T("internal day: 24.18 h on average", 28, PURPLE).next_to(internal, UP, buff=0.2).align_to(internal, LEFT)
        mean_note = T("a study mean; individuals vary", 24, GREY).next_to(internal, DOWN, buff=0.25).align_to(internal, LEFT)

        self.at("dim light")
        self.play(FadeIn(lp, scale=0.8), FadeIn(lp_lbl), lp[0].animate.set_fill(YELLOW, 0.3), run_time=0.6)
        self.at("scheduled")
        self.play(GrowFromEdge(sched, LEFT), FadeIn(sched_lbl), run_time=1.2)
        self.at("internal day")
        self.play(GrowFromEdge(internal, LEFT), FadeIn(int_lbl), run_time=1.4)
        self.at("study mean")
        self.play(FadeIn(mean_note, shift=UP * 0.1), run_time=0.5)

        # the near-coincident 24 h tick
        x24 = X0 + 24 * U
        tick = Line([x24, -1.3, 0], [x24, 0.15, 0], color=GREEN, stroke_width=6)
        t24 = T("24 h", 28, GREEN).move_to([x24, -1.65, 0])
        q = T("?", 64, YELLOW, weight=BOLD).move_to([x24 + 0.95, -0.7, 0])
        ask = T("what brings it back to 24 h, every day?", 30, TEXT).move_to([0, -2.9, 0])
        self.at("brings the clock back")
        self.play(Create(tick), FadeIn(t24), FadeIn(q, scale=1.4), run_time=0.8)
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Loop(SpokenScene):
    """mouse cell, nucleus: CLOCK-BMAL1 on the E-box, Per/Cry on, PER and CRY build, pair, enter, switch the pair off."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=1.2, width=12.6, height=6.9, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.06).move_to([0, 0, 0])
        nuc = Ellipse(width=9.2, height=3.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([0, 1.3, 0])
        cell_lbl = T("mouse cell", 26, GREY).move_to([-4.9, -3.0, 0])
        nuc_lbl = T("nucleus", 24, GREY).move_to([-5.3, 0.4, 0])

        dna = Line([-3.9, 0.55, 0], [3.9, 0.55, 0], color=GREY, stroke_width=4)
        ebox = bchip("E-box", DNA, size=24).move_to([-2.3, 0.55, 0])
        gene = bchip("Per, Cry genes", DNA, size=24).move_to([2.2, 0.55, 0])

        clock = bchip("CLOCK", BLUE, size=26)
        bmal = bchip("BMAL1", BLUE, size=26)
        pair = VGroup(clock, bmal).arrange(RIGHT, buff=0.08)
        clock.move_to([-5.0, 1.9, 0]); bmal.move_to([-5.0, 1.0, 0])

        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(cell_lbl), FadeIn(nuc_lbl), run_time=0.8)
        self.play(Create(dna), FadeIn(ebox), FadeIn(gene), run_time=0.7)
        gene[1].set_stroke(opacity=0.35); gene[1].set_fill(opacity=0.04); gene[2].set_opacity(0.4)

        self.at("pair of proteins")
        self.play(FadeIn(clock, shift=RIGHT * 0.3), FadeIn(bmal, shift=RIGHT * 0.3), run_time=0.6)
        # join as a pair
        pair_target = VGroup(clock.copy(), bmal.copy()).arrange(RIGHT, buff=0.08).move_to([-2.3, 1.55, 0])
        self.at("binds short")
        self.play(clock.animate.move_to(pair_target[0]), bmal.animate.move_to(pair_target[1]), run_time=1.0)
        # on the E-box
        on_lbl = T("bound to the E-box", 22, BLUE).move_to([-2.3, 2.45, 0])
        self.play(FadeIn(on_lbl), run_time=0.4)

        self.at("switches on")
        a1 = arr([-1.2, 0.55, 0], [1.2, 0.55, 0], GREEN)
        self.play(GrowArrow(a1), gene[1].animate.set_stroke(opacity=1).set_fill(opacity=0.16), gene[2].animate.set_opacity(1), run_time=0.8)
        # PER and CRY made, leave the nucleus into the cytoplasm
        out = arr([2.2, 0.0, 0], [2.2, -1.5, 0], GREEN)
        self.play(GrowArrow(out), run_time=0.5)

        self.at("build up")
        per_cry = []
        slots = [(0.4, -1.9), (1.8, -2.3), (2.9, -1.9), (4.2, -2.3)]
        for i, (x, y) in enumerate(slots):
            c = bchip("PER" if i % 2 == 0 else "CRY", ORANGE, size=24).move_to([x, y, 0])
            per_cry.append(c)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in per_cry], lag_ratio=0.18), run_time=1.6)

        self.at("bind each other")
        # three PER-CRY pairs: PER+CRY side by side
        pairs = [(0, 1), (2, 3)]
        centres = [(0.8, -2.2), (3.4, -2.2)]
        anims = []
        for (i, j), (cx, cy) in zip(pairs, centres):
            anims += [per_cry[i].animate.move_to([cx - 0.5, cy, 0]), per_cry[j].animate.move_to([cx + 0.5, cy, 0])]
        self.play(*anims, FadeOut(out), run_time=1.0)

        self.at("enter the nucleus")
        tgt = [(1.3, 1.55), (3.2, 1.55)]
        # move in: pairs rise into the nucleus above the DNA line on the right
        mv = []
        for (i, j), (tx, ty) in zip(pairs, tgt):
            mv += [per_cry[i].animate.move_to([tx - 0.5 + 0.05, ty, 0]).scale(0.85),
                   per_cry[j].animate.move_to([tx + 0.5 - 0.05, ty, 0]).scale(0.85)]
        self.play(*mv, run_time=1.6)

        self.at("reporter assays")
        rep = T("in reporter assays", 24, GREY).move_to([4.9, -1.6, 0])
        pr_all = VGroup(*per_cry)
        c1 = bchip("CRY1", ORANGE, size=24).move_to([1.0, 1.55, 0])
        orr = T("or", 24, GREY).move_to([2.0, 1.55, 0])
        c2 = bchip("CRY2", ORANGE, size=24).move_to([3.0, 1.55, 0])
        self.play(FadeOut(pr_all), FadeOut(cell_lbl), FadeIn(rep), run_time=0.5)
        self.play(FadeIn(c1), FadeIn(orr), FadeIn(c2), run_time=0.6)
        self.at("abolished")
        bar = tbar([0.2, 1.55, 0], [-0.8, 1.55, 0], RED)
        gone = T("transcription abolished", 22, RED).move_to([1.0, -0.02, 0])
        self.play(Create(bar), FadeOut(a1), FadeIn(gone),
                  gene[1].animate.set_stroke(opacity=0.35).set_fill(opacity=0.04), gene[2].animate.set_opacity(0.4),
                  clock[1].animate.set_stroke(opacity=0.4), bmal[1].animate.set_stroke(opacity=0.4),
                  clock[2].animate.set_opacity(0.5), bmal[2].animate.set_opacity(0.5), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def delayed_feedback(a=1.0, K=0.5, n=6, d=0.35, tau=3.0, T_end=24.0, dt=0.01):
    N = int(T_end / dt); lag = int(tau / dt)
    x = np.zeros(N); x[0] = 0.05
    for i in range(1, N):
        xd = x[i - 1 - lag] if i - 1 - lag >= 0 else 0.05
        x[i] = x[i - 1] + dt * (a / (1 + (xd / K) ** n) - d * x[i - 1])
    return np.arange(N) * dt, x


class S03Delay(SpokenScene):
    """The feedback loop with its delay steps, and a computed delayed-negative-feedback trace (in this sketch)."""

    def construct(self):
        # --- loop, left -------------------------------------------------------------------
        A = bchip("CLOCK-BMAL1", BLUE, size=26).move_to([-3.2, 3.0, 0])
        B = bchip("PER and CRY", ORANGE, size=26).move_to([-3.2, -3.0, 0])
        steps_txt = ["transcription", "translation", "modification", "nuclear entry", "timed degradation"]
        steps = VGroup(*[bchip(s, GREY, size=22, pad=0.14) for s in steps_txt]).arrange(DOWN, buff=0.26).move_to([-3.2, 0.0, 0])
        br = VGroup(Line([-1.7, 2.2, 0], [-1.5, 2.2, 0], color=GREY, stroke_width=3), Line([-1.5, 2.2, 0], [-1.5, -1.6, 0], color=GREY, stroke_width=3),
                    Line([-1.5, -1.6, 0], [-1.7, -1.6, 0], color=GREY, stroke_width=3))
        delay_lbl = T("hours of delay", 24, YELLOW).rotate(-PI / 2).move_to([-1.05, 0.3, 0])
        fb = VGroup(Line([-4.6, -3.0, 0], [-5.8, -3.0, 0], color=RED, stroke_width=5), Line([-5.8, -3.0, 0], [-5.8, 3.0, 0], color=RED, stroke_width=5),
                    tbar([-5.8, 3.0, 0], [-4.6, 3.0, 0], RED))
        brake = T("brake", 26, RED).rotate(PI / 2).move_to([-6.2, 0.0, 0])

        self.play(FadeIn(A), FadeIn(B), FadeIn(steps[0:0]), run_time=0.6)
        self.play(Create(fb), FadeIn(brake), run_time=0.8)
        self.at("comes off")
        # the brake comes off: PER and CRY degraded -> brake line goes grey/dashed
        self.play(B[1].animate.set_stroke(opacity=0.3).set_fill(opacity=0.05), B[2].animate.set_opacity(0.3), fb.animate.set_stroke(opacity=0.15), brake.animate.set_opacity(0.2), run_time=0.8)
        self.at("new cycle")
        self.play(Indicate(VGroup(*A[1:]), color=BLUE, scale_factor=1.12), run_time=0.9)
        self.play(B[1].animate.set_stroke(opacity=1).set_fill(opacity=0.16), B[2].animate.set_opacity(1), fb.animate.set_stroke(opacity=1), brake.animate.set_opacity(1), run_time=0.5)

        # --- plot, right ------------------------------------------------------------------
        ox, oy = 0.9, -2.4
        W, H = 3.4, 4.5
        xs, ys = delayed_feedback()
        xmax, ymax = xs[-1], 2.0
        axes = VGroup(Line([ox, oy, 0], [ox + W, oy, 0], color=GREY, stroke_width=3),
                      Line([ox, oy, 0], [ox, oy + H, 0], color=GREY, stroke_width=3))
        xl = T("time (relative units)", 22, GREY).move_to([ox + W / 2, oy - 0.45, 0])
        yl = T("PER and CRY level", 22, GREY).rotate(PI / 2).move_to([ox - 0.45, oy + H / 2, 0])
        sk = T("in this sketch", 26, YELLOW).move_to([ox + W / 2, oy + H + 0.35, 0])
        pts = [[ox + W * xs[i] / xmax, oy + H * min(ys[i], ymax) / ymax, 0] for i in range(0, len(xs), 4)]
        trace = VMobject(color=ORANGE, stroke_width=5).set_points_smoothly([np.array(p) for p in pts])
        mean_y = oy + H * (np.mean(ys[600:]) / ymax)
        steady = DashedLine([ox, mean_y, 0], [ox + W + 0.1, mean_y, 0], color=GREY, stroke_width=3)
        st_lbl = T("steady level", 22, GREY).move_to([ox + W + 0.8, mean_y, 0])

        self.at("oscillate")
        self.play(Create(axes), FadeIn(xl), FadeIn(yl), FadeIn(sk), run_time=0.9)
        self.play(Create(steady), FadeIn(st_lbl), run_time=0.5)
        self.at("Think of a shower")
        self.play(Create(trace, rate_func=linear), run_time=max(1.5, self.t_of("transcription") - 0.4 - self.elapsed()))
        # delay steps appear one by one as named
        self.at("transcription")
        self.play(FadeIn(steps[0], shift=DOWN * 0.15), run_time=0.3)
        self.at("translation")
        self.play(FadeIn(steps[1], shift=DOWN * 0.15), run_time=0.3)
        self.at("modification")
        self.play(FadeIn(steps[2], shift=DOWN * 0.15), run_time=0.3)
        self.at("nuclear entry")
        self.play(FadeIn(steps[3], shift=DOWN * 0.15), run_time=0.3)
        self.at("timed degradation")
        self.play(FadeIn(steps[4], shift=DOWN * 0.15), run_time=0.3)
        self.at("hours of delay")
        self.play(Create(br), FadeIn(delay_lbl), run_time=0.5)
        self.play(Indicate(VGroup(*[VGroup(*c[1:]) for c in steps]), color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Drift(SpokenScene):
    """24.18 - 24.00 = 0.18 h = 10.8 min per cycle; seven cycles of growing lag, the last 75.6 min."""

    def construct(self):
        head = T("an idealized clock: no time cues, starts in phase with the day", 26, GREY).to_edge(UP, buff=0.4)
        l1 = VGroup(M("24.18 h", 34, PURPLE), M("−", 34, TEXT), M("24.00 h", 34, GREY)).arrange(RIGHT, buff=0.25)
        l2 = M("= 0.18 h per cycle", 34, TEXT)
        l3 = M("0.18 × 60 = 10.8 min", 34, YELLOW)
        eq = VGroup(l1, l2, l3).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([-3.4, 0.5, 0])

        # lag chart (right)
        ox, oy, bw, gap, hmax = 0.9, -2.2, 0.5, 0.22, 4.3
        lag = [10.8 * k for k in range(1, 8)]
        axes = VGroup(Line([ox - 0.2, oy, 0], [ox + 7 * (bw + gap) + 0.1, oy, 0], color=GREY, stroke_width=3),
                      Line([ox - 0.2, oy, 0], [ox - 0.2, oy + hmax + 0.3, 0], color=GREY, stroke_width=3))
        xl = T("cycle", 22, GREY).move_to([ox + 3.5 * (bw + gap), oy - 0.75, 0])
        yl = T("marker lag (min)", 22, GREY).rotate(PI / 2).move_to([ox - 0.6, oy + 2.4, 0])
        bars = []
        for k, v in enumerate(lag):
            h = hmax * v / 75.6
            b = Rectangle(width=bw, height=h, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.5)
            b.move_to([ox + 0.3 + k * (bw + gap), oy + h / 2, 0])
            bars.append(b)
        nums = [T(str(k + 1), 22, GREY).move_to([bars[k].get_center()[0], oy - 0.2, 0]) for k in range(7)]
        first = M("10.8", 24, YELLOW).next_to(bars[0], UP, buff=0.1)
        last = M("75.6 min", 26, YELLOW).next_to(bars[6], UP, buff=0.1)
        last.shift(LEFT * 0.45)

        self.play(FadeIn(head), run_time=0.6)
        self.at("idealized clock")
        self.play(FadeIn(l1[0], shift=RIGHT * 0.2), FadeIn(l1[1]), FadeIn(l1[2]), run_time=0.8)
        self.at("starts in phase")
        self.wait(0.2)
        self.at("Each cycle runs")
        self.play(FadeIn(l2, shift=UP * 0.1), Create(axes), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.play(FadeIn(l3, shift=UP * 0.1), FadeIn(nums[0]), GrowFromEdge(bars[0], DOWN), FadeIn(first), run_time=0.9)
        self.at("After seven cycles")
        self.play(*[FadeIn(nums[k]) for k in range(1, 7)],
                  LaggedStart(*[GrowFromEdge(bars[k], DOWN) for k in range(1, 7)], lag_ratio=0.25), run_time=2.6)
        self.at("marker falls")
        self.play(FadeIn(last, shift=UP * 0.1), bars[6].animate.set_fill(YELLOW, 0.45).set_stroke(YELLOW), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Light(SpokenScene):
    """Light -> melanopsin ganglion cell -> retinohypothalamic tract -> SCN; rods and cones blocked, then contributing; Per1."""

    def construct(self):
        retina = RoundedRectangle(corner_radius=0.3, width=5.0, height=5.6, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.08).move_to([-3.7, -0.4, 0])
        ret_lbl = T("retina", 24, GREY).move_to([-3.7, 2.2, 0])
        iso_lbl = T("isolated rat retina", 24, GREY).move_to([-3.7, -3.5, 0])
        iso_lbl.shift(UP * 0.0)

        light_arrows = VGroup(*[arr([-5.2 + 1.3 * k, 3.45, 0], [-5.2 + 1.3 * k, 2.55, 0], YELLOW, w=5, tip=0.2) for k in range(3)])
        light_lbl = T("light", 26, YELLOW).move_to([-0.9, 3.1, 0])

        rods = bchip("rods", PINK, size=24).move_to([-5.2, 0.7, 0])
        cones = bchip("cones", PINK, size=24).move_to([-5.2, -0.7, 0])
        soma = Circle(radius=0.6, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.2).move_to([-3.0, 0.0, 0])
        gc_lbl = T("ganglion cell", 24, TEAL).next_to(soma, UP, buff=0.15)
        mel = bchip("melanopsin", TEAL, size=22, pad=0.12).move_to([-3.0, -1.35, 0])

        scn = bchip("SCN", TEAL, size=36, pad=0.3).move_to([4.4, -0.4, 0])
        scn_full = T("suprachiasmatic nucleus", 24, TEAL).next_to(scn, UP, buff=0.3)
        axon = VGroup(*[Line([-2.4, dy - 0.0, 0], [3.5, -0.4 + dy * 0.2, 0], color=TEAL, stroke_width=4) for dy in (0.12, 0.0, -0.12)])
        axon.set_z_index(0)
        tract_lbl = T("retinohypothalamic tract", 24, TEAL).move_to([1.2, -1.2, 0])
        tract_note = T("a bundle of axons", 22, GREY).move_to([0.9, 0.55, 0])

        self.play(FadeIn(retina), FadeIn(ret_lbl), FadeIn(rods), FadeIn(cones), FadeIn(soma), FadeIn(gc_lbl), run_time=0.8)
        self.at("Light must")
        self.play(LaggedStart(*[GrowArrow(a) for a in light_arrows], lag_ratio=0.2), FadeIn(light_lbl), run_time=0.8)
        self.at("suprachiasmatic nucleus")
        self.play(FadeIn(scn, scale=0.8), FadeIn(scn_full), run_time=0.7)
        self.at("hypothalamic tract")
        self.play(Create(axon), FadeIn(tract_lbl), run_time=1.0)
        self.at("bundle of axons")
        self.play(FadeIn(tract_note, shift=DOWN * 0.1), run_time=0.5)

        # isolated rat retina; rod and cone input blocked
        self.at("isolated rat retina")
        self.play(FadeIn(iso_lbl), run_time=0.5)
        a_r = arr([-4.65, 0.7, 0], [-3.55, 0.25, 0], PINK, w=4, tip=0.18)
        a_c = arr([-4.65, -0.7, 0], [-3.55, -0.25, 0], PINK, w=4, tip=0.18)
        self.play(GrowArrow(a_r), GrowArrow(a_c), run_time=0.5)
        self.at("ganglion cells that project")
        x1 = VGroup(Cross(stroke_color=RED, stroke_width=6).scale(0.22).move_to([-4.1, 0.48, 0]))
        x2 = VGroup(Cross(stroke_color=RED, stroke_width=6).scale(0.22).move_to([-4.1, -0.48, 0]))
        blk = T("blocked", 24, RED).move_to([-5.0, -1.5, 0])
        self.play(Create(x1), Create(x2), FadeIn(blk), a_r.animate.set_opacity(0.3), a_c.animate.set_opacity(0.3), run_time=0.6)
        self.at("still depolarize")
        dep = T("still depolarizes to light", 24, TEAL).move_to([-1.2, 2.05, 0])
        dep.move_to([-3.7, -2.45, 0])
        self.play(soma.animate.set_fill(TEAL, 0.6), Indicate(soma, color=YELLOW, scale_factor=1.15), FadeIn(dep, shift=DOWN * 0.1), run_time=0.9)

        self.at("melanopsin")
        self.play(FadeIn(mel, shift=UP * 0.1), run_time=0.5)
        self.at("rods and cones contribute")
        self.play(FadeOut(x1), FadeOut(x2), FadeOut(blk), a_r.animate.set_opacity(1), a_c.animate.set_opacity(1), run_time=0.7)

        self.at("In the mouse")
        self.play(FadeOut(dep), FadeOut(tract_note), run_time=0.4)
        per1 = bchip("Per1 transcripts up", GREEN, size=24).move_to([4.4, -2.3, 0])
        ar = arr([4.4, -0.95, 0], [4.4, -1.8, 0], GREEN, w=4, tip=0.18)
        mouse_lbl = T("mouse SCN: a light pulse", 22, YELLOW).move_to([3.6, 1.75, 0])
        self.play(FadeIn(mouse_lbl), run_time=0.4)
        self.at("quickly induced")
        self.play(GrowArrow(ar), FadeIn(per1, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Timing(SpokenScene):
    """Light before the temperature minimum delays, after it advances; a daily advance cancels the 10.8 min drift."""

    def construct(self):
        X0, X1, AY = -5.8, 5.8, -0.2
        axis = Arrow([X0, AY, 0], [X1, AY, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        later = T("later", 24, GREY).move_to([X1 - 0.4, AY - 0.4, 0])
        cbt = DashedLine([0, AY - 0.5, 0], [0, 2.1, 0], color=RED, stroke_width=4)
        cbt_lbl = T("core body temperature minimum", 26, RED).move_to([0, 2.6, 0])
        cbt_sub = T("usually early morning", 22, GREY).move_to([0, 2.15 - 0.0, 0])
        cbt_sub.move_to([0, AY - 0.85, 0])

        def marker(x):
            m = VGroup(Line([x, AY, 0], [x, AY + 0.9, 0], color=PURPLE, stroke_width=5),
                       Polygon([x, AY + 0.9, 0], [x + 0.55, AY + 0.7, 0], [x, AY + 0.5, 0], stroke_color=PURPLE, stroke_width=3,
                               fill_color=PURPLE, fill_opacity=0.8))
            return m
        mk = marker(-2.0)
        clk_lbl = T("clock marker", 22, PURPLE)
        lab = clk_lbl.next_to(mk, LEFT, buff=0.2).shift(UP * 0.35)

        def lightbar(x, w=1.6):
            r = RoundedRectangle(corner_radius=0.1, width=w, height=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45)
            return r.move_to([x, AY - 1.5, 0])

        self.play(Create(axis), FadeIn(later), Create(cbt), FadeIn(cbt_lbl), FadeIn(cbt_sub), run_time=0.7)
        self.at("In healthy people")
        self.play(FadeIn(mk), FadeIn(lab), run_time=0.6)

        # --- light before the minimum: delay (marker moves later = right)
        lb = lightbar(-3.4)
        lb_lbl = T("bright light before", 24, YELLOW).next_to(lb, DOWN, buff=0.15)
        self.at("bright light before")
        self.play(FadeIn(lb), FadeIn(lb_lbl), run_time=0.5)
        self.at("delayed the clock")
        d_arr = arr([-2.0, 1.55, 0], [-0.9, 1.55, 0], YELLOW, w=5)
        d_lbl = T("delays", 26, YELLOW).next_to(d_arr, UP, buff=0.1)
        shift = RIGHT * 1.1
        self.play(mk.animate.shift(shift), lab.animate.shift(shift), GrowArrow(d_arr), FadeIn(d_lbl), run_time=1.0)

        # --- light after the minimum: advance (marker moves earlier = left)
        self.at("Light after it")
        self.play(FadeOut(lb), FadeOut(lb_lbl), FadeOut(d_arr), FadeOut(d_lbl),
                  mk.animate.shift(-shift), lab.animate.shift(-shift), run_time=0.7)
        la = lightbar(3.4)
        la_lbl = T("bright light after", 24, YELLOW).next_to(la, DOWN, buff=0.15)
        self.play(FadeIn(la), FadeIn(la_lbl), run_time=0.5)
        self.at("advanced the clock")
        a_arr = arr([-0.9, 1.55, 0], [-2.0, 1.55, 0], YELLOW, w=5)
        a_lbl = T("advances", 26, YELLOW).next_to(a_arr, UP, buff=0.1)
        self.play(mk.animate.shift(-shift), lab.animate.shift(-shift), GrowArrow(a_arr), FadeIn(a_lbl), run_time=1.0)
        self.wait(0.3)

        # --- the daily budget: drift vs net advance
        self.at("To stay at")
        stage = [axis, later, cbt, cbt_lbl, cbt_sub, mk, lab, la, la_lbl, a_arr, a_lbl]
        self.play(*[FadeOut(m) for m in stage], run_time=0.6)
        drift_a = arr([-5.6, 0.4, 0], [-0.2, 0.4, 0], PURPLE, w=10, tip=0.35)
        drift_l = VGroup(T("the clock drifts later", 28, PURPLE), T("10.8 min per cycle", 28, PURPLE)).arrange(DOWN, buff=0.12).move_to([-2.9, 1.7, 0])
        adv_a = arr([5.6, 0.4, 0], [0.2, 0.4, 0], YELLOW, w=10, tip=0.35)
        adv_l = VGroup(T("light advances it", 28, YELLOW), T("10.8 min per day, on average", 28, YELLOW)).arrange(DOWN, buff=0.12).move_to([2.9, 1.7, 0])
        self.play(GrowArrow(drift_a), FadeIn(drift_l), run_time=0.8)
        self.at("average net advance")
        self.play(GrowArrow(adv_a), FadeIn(adv_l), run_time=0.9)
        eq = VGroup(T("stays at", 30, GREY), M("24.00 h", 48, GREEN)).arrange(RIGHT, buff=0.4).move_to([0, -1.6, 0])
        self.at("Keep this")
        self.play(FadeIn(eq, scale=1.2), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "The clock runs near a day; light resets it daily."
