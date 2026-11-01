"""Motivation and reward: dopamine neurons signal a prediction error  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the reward (juice), received reward r
  BLUE   = the cue (the sound)
  GREEN  = a burst of firing / a positive prediction error (delta above zero)
  RED    = a dip below baseline / a negative prediction error / the reward left out
  TEAL   = the cue's learned value V, "the reward predicted"
  ORANGE = alpha, the learning rate
  PURPLE = the dopamine neuron
  GREY   = axes, baselines, frames, tags, and every unanswered thing (dashed)
  TEXT   = the firing trace itself

Scenes 1 to 3 draw firing-rate sketches ("in this sketch": relative units, the lesson gives no
recording). Scenes 4 to 6 use the lesson's model numbers only: alpha 0.30, r 1, V 0 at the start,
V = 1 - 0.7^n, and V near 0.95 for the omission.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# ---------------------------------------------------------------------------------------------
# firing-rate sketch geometry (scenes 1 to 3)
# ---------------------------------------------------------------------------------------------
X0, X1 = -5.4, 5.6
YB, U = -0.4, 2.2            # baseline y, units of y per unit of rate
YAX, YEV = -2.25, -2.95      # time axis, event-chip row
T_SOUND, T_JUICE, T_LATE = 1.5, 5.5, 8.0
TS = np.linspace(0, 10, 240)


def tx(t):
    return X0 + (X1 - X0) * t / 10.0


def trace(specs):
    """always_redraw builder: a firing-rate curve from bumps (centre, width, tracker)."""
    def build():
        e = sum(tr.get_value() * np.exp(-((TS - c) / w) ** 2) for c, w, tr in specs)
        pts = [np.array([tx(t), YB + U * v, 0]) for t, v in zip(TS, e)]
        out = [VMobject(stroke_color=TEXT, stroke_width=4).set_points_as_corners(pts)]
        for sign, col in ((1, GREEN), (-1, RED)):
            ev = np.maximum(sign * e, 0)
            if ev.max() > 0.03:
                top = [np.array([tx(t), YB + U * sign * v, 0]) for t, v in zip(TS, ev)]
                base = [np.array([tx(t), YB, 0]) for t in TS[::-1]]
                out.append(Polygon(*top, *base, stroke_width=0, fill_color=col, fill_opacity=0.55))
        return VGroup(*out)
    return build


def neuron_icon():
    """A simple dopamine neuron: soma, dendrites, axon."""
    c = np.array([0.0, 0.0, 0])
    soma = Circle(radius=0.26, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to(c)
    dend = VGroup(*[Line(c + 0.26 * np.array([np.cos(a), np.sin(a), 0]),
                         c + 0.8 * np.array([np.cos(a), np.sin(a), 0]), color=PURPLE, stroke_width=3)
                    for a in (2.4, 3.14, 3.9)])
    ax = Line(c + [0.26, 0, 0], c + [1.1, 0, 0], color=PURPLE, stroke_width=3)
    bulb = Circle(radius=0.09, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.6).move_to(c + [1.15, 0, 0])
    return VGroup(dend, ax, soma, bulb)


def plot_frame(show_tag=True):
    """Axes, labels, baseline and the neuron header. Returns (group, parts)."""
    yax = Line([X0 - 0.12, YAX, 0], [X0 - 0.12, 2.1, 0], color=GREY, stroke_width=3)
    xax = Arrow([X0 - 0.12, YAX, 0], [X1 + 0.35, YAX, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    xl = T("time", 22, GREY).next_to(xax, DOWN, buff=0.04).align_to([X1 - 0.3, 0, 0], RIGHT)
    xl.move_to([X1 - 0.1, YAX + 0.28, 0])
    yl = T("firing rate, relative units", 22, GREY).move_to([X0 + 1.95, 2.4, 0])
    base = DashedLine([X0 - 0.12, YB, 0], [X1, YB, 0], color=GREY, stroke_width=2, dash_length=0.12)
    bl = T("baseline", 22, GREY).move_to([X1 - 0.65, YB + 0.28, 0])
    nr = neuron_icon().move_to([-5.0, 3.05, 0])
    nl = T("dopamine neuron, monkey", 24, TEXT).next_to(nr, RIGHT, buff=0.35)
    tag = T("in this sketch", 22, GREY).move_to([5.0, 3.05, 0])
    axes = VGroup(yax, xax, base)
    labels = VGroup(xl, yl, bl, tag)
    head = VGroup(nr, nl)
    return axes, labels, head


def evchip(text, color, t):
    return chip(text, color, size=24, pad=0.16).move_to([tx(t), YEV, 0])


def evline(t, color):
    return DashedLine([tx(t), YAX, 0], [tx(t), 2.0, 0], color=color, stroke_width=2, dash_length=0.1).set_opacity(0.55)


def ghost(text, t):
    lab = T(text, 24, GREY)
    w, h = lab.width + 0.32, lab.height + 0.32
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=GREY, stroke_width=3), num_dashes=30)
    return VGroup(box, lab).move_to([tx(t), YEV, 0])


def eqrow(parts, size=40, buff=0.16):
    return VGroup(*[M(s, size, c) for s, c in parts]).arrange(RIGHT, buff=buff, aligned_edge=DOWN)


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Feeding, Motivation and Reward"
    TITLE = "Dopamine Neurons Signal Prediction Errors"


class S01Juice(SpokenScene):
    def construct(self):
        axes, labels, head = plot_frame()
        juice, jl = evchip("juice", YELLOW, T_JUICE), evline(T_JUICE, YELLOW)
        amp = ValueTracker(0)
        tr = always_redraw(trace([(T_JUICE, 0.35, amp)]))
        self.at("A monkey receives")
        self.play(Create(axes), FadeIn(labels), run_time=0.8)
        self.play(FadeIn(juice, shift=DOWN * 0.3), Create(jl), run_time=0.6)
        self.add(tr)
        nw = T("no warning", 22, GREY).next_to(juice, RIGHT, buff=0.3)
        self.at("with no warning")
        self.play(FadeIn(nw), run_time=0.4)
        self.at("recorded single dopamine neurons")
        self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
        def ticks(ts):
            return VGroup(*[Line([tx(t), YB + 0.12, 0], [tx(t), YB + 0.5, 0], color=TEXT, stroke_width=3) for t in ts])
        base_ticks = ticks([0.4, 1.1, 1.9, 2.6, 3.5, 4.3, 6.9, 7.6, 8.3])
        sp_lab = T("spikes", 22, GREY).move_to([tx(2.2), YB + 0.85, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in base_ticks], lag_ratio=0.5), FadeIn(sp_lab),
                  run_time=max(1.0, self.t_of("three quarters") - 0.3 - self.elapsed()))
        self.at("-quarters")
        bar_o = Rectangle(width=3.0, height=0.3, stroke_color=GREY, stroke_width=3)
        bar_f = Rectangle(width=2.25, height=0.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.8)
        bar_o.move_to([4.3, 1.45, 0]); bar_f.align_to(bar_o, LEFT).align_to(bar_o, UP)
        cap = VGroup(T("about three quarters of", 22, TEXT), T("recorded neurons, two monkeys", 22, TEXT)).arrange(DOWN, buff=0.06)
        cap.next_to(bar_o, UP, buff=0.18)
        self.play(FadeIn(cap), Create(bar_o), GrowFromEdge(bar_f, LEFT), run_time=0.8)
        self.at("fired a brief burst")
        burst_ticks = ticks([5.15, 5.3, 5.4, 5.5, 5.6, 5.7, 5.85])
        self.play(amp.animate.set_value(1.0), LaggedStart(*[FadeIn(t) for t in burst_ticks], lag_ratio=0.15), run_time=0.9)
        self.at("What is that burst")
        self.play(FadeOut(base_ticks), FadeOut(burst_ticks), FadeOut(sp_lab), run_time=0.4)
        q = T("?", 72, TEXT).move_to([tx(T_JUICE) - 1.2, 1.2, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.finish()


class S02Cue(SpokenScene):
    def construct(self):
        axes, labels, head = plot_frame()
        juice, jl = evchip("juice", YELLOW, T_JUICE), evline(T_JUICE, YELLOW)
        a_s, a_j = ValueTracker(0), ValueTracker(1.0)
        tr = always_redraw(trace([(T_SOUND, 0.35, a_s), (T_JUICE, 0.35, a_j)]))
        self.add(axes, labels, head, juice, jl, tr)
        sound, sl = evchip("sound", BLUE, T_SOUND), evline(T_SOUND, BLUE)
        pred = Arrow(sound.get_right() + [0.05, 0, 0], juice.get_left() - [0.05, 0, 0], buff=0, color=BLUE, stroke_width=4, tip_length=0.2)
        pl = T("predicts", 22, BLUE).move_to([(tx(T_SOUND) + tx(T_JUICE)) / 2, YEV + 0.3, 0])
        self.at("Now suppose a sound")
        self.play(FadeIn(sound, shift=DOWN * 0.3), Create(sl), run_time=0.6)
        self.play(GrowArrow(pred), FadeIn(pl), run_time=0.6)
        self.at("the burst came at the sound")
        self.play(a_s.animate.set_value(1.0), a_j.animate.set_value(0.0), run_time=1.3)
        self.at("rather than at the juice")
        nb = T("no burst", 24, GREY).move_to([tx(T_JUICE) + 0.9, YB + 0.5, 0])
        self.play(FadeIn(nb), Indicate(juice, color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("The response moved")
        arc = CurvedArrow([tx(T_JUICE) - 0.2, 1.2, 0], [tx(T_SOUND) + 0.2, 1.2, 0], angle=TAU / 6, color=GREEN, stroke_width=5)
        self.play(Create(arc), run_time=0.8)
        self.finish()


class S03Error(SpokenScene):
    def construct(self):
        axes, labels, head = plot_frame()
        juice, jl = evchip("juice", YELLOW, T_JUICE), evline(T_JUICE, YELLOW)
        sound, sl = evchip("sound", BLUE, T_SOUND), evline(T_SOUND, BLUE)
        pred = Arrow(sound.get_right() + [0.05, 0, 0], juice.get_left() - [0.05, 0, 0], buff=0, color=BLUE, stroke_width=4, tip_length=0.2)
        pl = T("predicts", 22, BLUE).move_to([(tx(T_SOUND) + tx(T_JUICE)) / 2, YEV + 0.3, 0])
        a_s, a_j, a_l = ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.0)
        tr = always_redraw(trace([(T_SOUND, 0.35, a_s), (T_JUICE, 0.45, a_j), (T_LATE, 0.35, a_l)]))
        self.add(axes, labels, head, juice, jl, sound, sl, pred, pl, tr)
        c1 = T("expected juice left out", 26, TEXT).move_to([2.6, 2.4, 0])
        c2 = T("juice at an unexpected time", 26, TEXT).move_to([2.6, 2.4, 0])
        gh = ghost("juice", T_JUICE)
        self.at("an expected reward was left out")
        self.play(FadeIn(c1), FadeOut(juice), FadeIn(gh), run_time=0.7)
        self.at("dipped below baseline")
        self.play(a_j.animate.set_value(-0.6), run_time=0.8)
        self.at("A reward at an unexpected time")
        late, ll = evchip("juice", YELLOW, T_LATE), evline(T_LATE, YELLOW)
        self.play(FadeOut(c1), FadeOut(gh), FadeOut(sound), FadeOut(sl), FadeOut(pred), FadeOut(pl), FadeOut(jl),
                  a_j.animate.set_value(0.0), a_s.animate.set_value(0.0),
                  FadeIn(late, shift=DOWN * 0.3), Create(ll), run_time=0.9)
        self.play(FadeIn(c2), run_time=0.3)
        self.at("evoked a burst")
        self.play(a_l.animate.set_value(1.0), run_time=0.6)
        self.at("So the firing follows")
        self.play(*[FadeOut(m) for m in (axes, labels, head, tr, late, ll, c2)], run_time=0.7)
        self.remove(tr)
        rec = chip("reward received", YELLOW, size=34, pad=0.26).move_to([-3.5, 1.1, 0])
        prd = chip("reward predicted", TEAL, size=34, pad=0.26).move_to([3.5, 1.1, 0])
        minus = M("−", 56, TEXT).move_to([0, 1.1, 0])
        self.at("the reward received")
        self.play(FadeIn(rec, shift=UP * 0.2), run_time=0.5)
        self.at("the reward predicted")
        self.play(FadeIn(minus), FadeIn(prd, shift=UP * 0.2), run_time=0.5)
        self.at("reward prediction error")
        res = chip("reward prediction error", GREEN, size=44, pad=0.3).move_to([0, -1.5, 0])
        ar = Arrow([0, 0.35, 0], [0, -0.7, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.28)
        self.play(GrowArrow(ar), FadeIn(res, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ---- bar charts for the model numbers (scenes 4 to 6) ---------------------------------------
def bargroup(x, delta, v, base, scale, bw, off, labels=True, size=28):
    d = Rectangle(width=bw, height=max(delta * scale, 0.02), stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
    d.move_to([x - off, base + max(delta * scale, 0.02) / 2, 0])
    vv = Rectangle(width=bw, height=max(v * scale, 0.02), stroke_width=0, fill_color=TEAL, fill_opacity=0.85)
    vv.move_to([x + off, base + max(v * scale, 0.02) / 2, 0])
    parts = [d, vv]
    labs = VGroup()
    if labels:
        labs.add(M(f"{delta:.2f}", size, GREEN).next_to(d, UP, buff=0.1))
        labs.add(M(f"{v:.2f}", size, TEAL).next_to(vv, UP, buff=0.1))
    return VGroup(d, vv), labs


def model_series(n=9, alpha=0.3):
    out, v = [], 0.0
    for _ in range(n):
        dl = 1.0 - v
        v = v + alpha * dl
        out.append((dl, v))
    return out


SER = model_series()
S4_BASE, S4_SCALE = -2.5, 3.0


def s4_chart(upto):
    groups, labs, tl = [], [], []
    for i, x in enumerate((-2.2, 2.2)[:upto]):
        g, lb = bargroup(x, SER[i][0], SER[i][1], S4_BASE, S4_SCALE, 0.9, 0.55)
        groups.append(g); labs.append(lb)
        tl.append(T(f"trial {i + 1}", 26, GREY).move_to([x, S4_BASE - 0.4, 0]))
    return groups, labs, tl


def legend_left():
    a = chip("δ  error", GREEN, size=24, pad=0.16).move_to([-4.9, 0.1, 0])
    b = chip("V  cue value", TEAL, size=24, pad=0.16).move_to([-4.9, -0.7, 0])
    return VGroup(a, b)


class S04Rule(SpokenScene):
    def construct(self):
        base_line = Line([-6.0, S4_BASE, 0], [6.0, S4_BASE, 0], color=GREY, stroke_width=3)
        e1 = eqrow([("δ", GREEN), (" = ", TEXT), ("r", YELLOW), (" − ", TEXT), ("V", TEAL)]).move_to([0, 3.0, 0])
        e2 = eqrow([("new V", TEAL), (" = ", TEXT), ("V", TEAL), (" + ", TEXT), ("α", ORANGE), (" × ", TEXT), ("δ", GREEN)]).move_to([0, 2.25, 0])
        par = eqrow([("α = 0.30", ORANGE), ("r = 1", YELLOW), ("V starts at 0", TEAL)], size=26, buff=0.6).move_to([0, 1.6, 0])
        gs, ls, ts = s4_chart(2)
        lg = legend_left()
        self.add(base_line)
        self.remove(base_line)
        rname = chip("Rescorla-Wagner rule", ORANGE, size=40, pad=0.3).move_to([0, 2.6, 0])
        self.at("simplest rule")
        self.play(FadeIn(rname, shift=UP * 0.2), run_time=0.6)
        e1.move_to([0, 1.1, 0]).scale(1.4); e2.scale(1.4).move_to([0, 0.0, 0])
        par.move_to([0, -1.2, 0])
        self.at("Delta is the reward")
        self.play(FadeIn(e1, shift=UP * 0.15), run_time=0.6)
        self.at("and the new")
        self.play(FadeIn(e2, shift=UP * 0.15), run_time=0.6)
        self.at("With alpha at")
        self.play(FadeIn(par, shift=UP * 0.1), run_time=0.6)
        self.at("gives delta", nth=0)
        self.play(FadeOut(rname), e1.animate.scale(1 / 1.4).move_to([0, 3.0, 0]), e2.animate.scale(1 / 1.4).move_to([0, 2.25, 0]),
                  par.animate.move_to([0, 1.6, 0]), Create(base_line), FadeIn(lg), run_time=0.7)
        self.play(FadeIn(ts[0]), GrowFromEdge(gs[0][0], DOWN), run_time=0.6)
        self.play(FadeIn(ls[0][0]), run_time=0.3)
        self.at("and V of", nth=0)
        self.play(GrowFromEdge(gs[0][1], DOWN), run_time=0.6)
        self.play(FadeIn(ls[0][1]), run_time=0.3)
        self.at("gives delta", nth=1)
        self.play(FadeIn(ts[1]), GrowFromEdge(gs[1][0], DOWN), run_time=0.6)
        self.play(FadeIn(ls[1][0]), run_time=0.3)
        self.at("and V of", nth=1)
        self.play(GrowFromEdge(gs[1][1], DOWN), run_time=0.6)
        self.play(FadeIn(ls[1][1]), run_time=0.3)
        self.finish()


S5_BASE, S5_SCALE = -2.0, 3.2
S5_XS = [-4.9 + 1.2 * i for i in range(9)]


class S05Shift(SpokenScene):
    def construct(self):
        base_line = Line([-6.0, S4_BASE, 0], [6.0, S4_BASE, 0], color=GREY, stroke_width=3)
        gs, ls, ts = s4_chart(2)
        lg = legend_left()
        self.add(base_line, *gs, *ls, *ts, lg)
        # the same two trials, moved into a nine-trial row
        new_base = Line([-6.0, S5_BASE, 0], [6.0, S5_BASE, 0], color=GREY, stroke_width=3)
        ng, nl_, nt = [], [], []
        for i, x in enumerate(S5_XS):
            g, _ = bargroup(x, SER[i][0], SER[i][1], S5_BASE, S5_SCALE, 0.42, 0.22, labels=False)
            ng.append(g)
            nt.append(T(str(i + 1), 24, GREY).move_to([x, S5_BASE - 0.38, 0]))
        lg2 = VGroup(chip("δ  error at the reward", GREEN, size=24, pad=0.16), chip("V  cue value", TEAL, size=24, pad=0.16)).arrange(RIGHT, buff=0.6).move_to([0, 2.6, 0])
        trial_lab = T("trial", 22, GREY).move_to([0, S5_BASE - 0.85, 0])
        self.at("The error at the reward")
        self.play(FadeOut(VGroup(*ls)), FadeOut(VGroup(*ts)), FadeOut(lg),
                  ReplacementTransform(base_line, new_base),
                  ReplacementTransform(gs[0], ng[0]), ReplacementTransform(gs[1], ng[1]),
                  FadeIn(VGroup(nt[0], nt[1])), FadeIn(lg2), run_time=1.0)
        self.play(FadeIn(trial_lab), run_time=0.2)
        rest = VGroup(*ng[2:])
        t_end = self.t_of("After nine trials") - 0.35
        self.play(LaggedStart(*[GrowFromEdge(g, DOWN) for g in ng[2:]], lag_ratio=0.35), FadeIn(VGroup(*nt[2:])),
                  run_time=max(0.8, t_end - self.elapsed()))
        self.at("trials")
        v9 = M("0.96", 26, TEAL).next_to(ng[8][1], UP, buff=0.1)
        ring = SurroundingRectangle(ng[8], color=TEAL, buff=0.1, stroke_width=3)
        self.play(Create(ring), FadeIn(v9), run_time=0.6)
        self.at("itself arrives")
        # panels: first trial and after nine trials
        cxl, cxr, yb = -3.2, 3.2, -1.2
        sc = 3.0
        def panel(cx, title, cue_h, rew_h, cue_lab, rew_lab):
            bl = Line([cx - 2.6, yb, 0], [cx + 2.6, yb, 0], color=GREY, stroke_width=3)
            ti = T(title, 28, TEXT).move_to([cx, 3.0, 0])
            cch = chip("cue", BLUE, size=24, pad=0.16).move_to([cx - 1.4, yb - 0.75, 0])
            rch = chip("reward", YELLOW, size=24, pad=0.16).move_to([cx + 1.4, yb - 0.75, 0])
            cb = Rectangle(width=0.8, height=max(cue_h * sc, 0.02), stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
            cb.move_to([cx - 1.4, yb + max(cue_h * sc, 0.02) / 2, 0])
            rb = Rectangle(width=0.8, height=max(rew_h * sc, 0.02), stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
            rb.move_to([cx + 1.4, yb + max(rew_h * sc, 0.02) / 2, 0])
            rl = M(rew_lab, 26, GREEN).next_to(rb, UP, buff=0.1)
            return VGroup(bl, ti, cch, rch), cb, rb, rl
        pl_s, cb1, rb1, rl1 = panel(cxl, "trial 1", 0.0, 1.0, "", "1.00")
        pl_e, cb2, rb2, rl2 = panel(cxr, "after nine trials", 0.96, 0.04, "", "0.04")
        tdr = T("in the temporal-difference reading", 24, TEAL).move_to([cxr, -2.85, 0])
        self.play(FadeOut(VGroup(new_base, *ng, *nt, lg2, trial_lab, ring, v9)), run_time=0.6)
        self.play(FadeIn(pl_s), FadeIn(pl_e), GrowFromEdge(rb1, DOWN), FadeIn(rl1), FadeIn(tdr), run_time=0.7)
        self.at("grows toward")
        tow = T("toward V", 24, TEAL).move_to([cxr - 0.1, 1.0, 0])
        self.play(GrowFromEdge(cb2, DOWN), run_time=0.7)
        self.play(GrowFromEdge(rb2, DOWN), FadeIn(rl2), FadeIn(tow), run_time=0.5)
        self.at("The burst moves from")
        arc = CurvedArrow([cxl + 1.4, 2.55, 0], [cxr - 1.4, 2.0, 0], angle=-TAU / 8, color=GREEN, stroke_width=5)
        self.play(Create(arc), run_time=0.8)
        self.at("These are model units")
        tagm = T("model units, not spikes per second", 24, GREY).move_to([0, -3.35, 0])
        self.play(FadeIn(tagm), run_time=0.5)
        self.finish()


class S06Keep(SpokenScene):
    def construct(self):
        zy, sc = 0.3, 1.8
        xa, xb = -3.0, 3.0
        zero = Line([-6.0, zy, 0], [6.0, zy, 0], color=GREY, stroke_width=3)
        za = M("0", 24, GREY).move_to([-6.1, zy, 0])
        tagm = T("model units, not spikes per second", 22, GREY).move_to([0, -3.3, 0])
        la = VGroup(T("reward left out", 26, TEXT), M("V near 0.95", 24, TEAL)).arrange(DOWN, buff=0.08).move_to([xa, 3.05, 0])
        lb = VGroup(T("unpredicted reward", 26, TEXT), M("V = 0", 24, TEAL)).arrange(DOWN, buff=0.08).move_to([xb, 3.05, 0])
        cue_a = chip("cue", BLUE, size=24, pad=0.16).move_to([xa - 1.5, -2.6, 0])
        gh_a = VGroup(*ghost("reward", 0)).move_to([xa + 0.4, -2.6, 0]) if False else ghost("reward", 0).move_to([xa + 0.5, -2.6, 0])
        rew_b = chip("reward", YELLOW, size=24, pad=0.16).move_to([xb, -2.6, 0])
        bar_a = Rectangle(width=1.1, height=0.95 * sc, stroke_width=0, fill_color=RED, fill_opacity=0.85)
        bar_a.move_to([xa + 0.5, zy - 0.95 * sc / 2, 0])
        lab_a = M("−0.95", 28, RED).next_to(bar_a, DOWN, buff=0.1)
        bar_b = Rectangle(width=1.1, height=1.0 * sc, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        bar_b.move_to([xb, zy + sc / 2, 0])
        lab_b = M("+1.00", 28, GREEN).next_to(bar_b, UP, buff=0.1)
        self.at("Now leave the reward out")
        self.play(Create(zero), FadeIn(za), FadeIn(tagm), FadeIn(la), FadeIn(cue_a), FadeIn(gh_a), run_time=0.8)
        self.at("Delta is minus")
        self.play(GrowFromEdge(bar_a, UP), run_time=0.7)
        self.play(FadeIn(lab_a), run_time=0.3)
        self.at("An unpredicted reward")
        self.play(FadeIn(lb), FadeIn(rew_b), run_time=0.6)
        self.at("gives plus")
        self.play(GrowFromEdge(bar_b, DOWN), run_time=0.6)
        self.play(FadeIn(lab_b), run_time=0.3)
        self.at("A recording shows")
        self.play(*[FadeOut(m) for m in (zero, za, tagm, la, lb, cue_a, gh_a, rew_b, bar_a, bar_b, lab_a, lab_b)], run_time=0.6)
        r1 = chip("recording", TEXT, size=28, pad=0.2).move_to([-4.6, 2.3, 0])
        r2 = chip("firing goes with error", GREEN, size=28, pad=0.2).move_to([0.0, 2.3, 0])
        a1 = Arrow(r1.get_right() + [0.05, 0, 0], r2.get_left() - [0.05, 0, 0], buff=0, color=GREEN, stroke_width=5, tip_length=0.22)
        r3 = chip("burst teaches?", GREY, size=28, pad=0.2).move_to([4.7, 2.3, 0])
        a2 = DashedLine(r2.get_right() + [0.05, 0, 0], r3.get_left() - [0.3, 0, 0], color=GREY, stroke_width=4, dash_length=0.12)
        a2h = Triangle(fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.12).rotate(-PI / 2).move_to(r3.get_left() - [0.2, 0, 0])
        self.play(FadeIn(r1), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(r2), run_time=0.5)
        self.play(Create(a2), FadeIn(a2h), FadeIn(r3), run_time=0.6)
        self.at("Keep the rule")
        self.play(VGroup(r1, r2, r3, a1, a2, a2h).animate.set_opacity(0.35), run_time=0.5)
        note = T("in these monkeys", 26, GREY).move_to([0, 0.0, 0])
        f1 = chip("reward received", YELLOW, size=34, pad=0.24).move_to([-4.2, -1.5, 0])
        f2 = M("−", 52, TEXT).move_to([-1.8, -1.5, 0])
        f3 = chip("reward predicted", TEAL, size=34, pad=0.24).move_to([0.75, -1.5, 0])
        f4 = chip("firing", GREEN, size=34, pad=0.24).move_to([4.9, -1.5, 0])
        ar = Arrow([3.95, -1.2, 0], [4.3, -1.2, 0], buff=0, color=GREEN, stroke_width=5, tip_length=0.22) if False else M("→", 46, GREEN).move_to([3.4, -1.5, 0])
        self.play(FadeIn(note), FadeIn(f1, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(f2), FadeIn(f3, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(ar), FadeIn(f4, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "In these monkeys, firing follows reward received minus predicted."
