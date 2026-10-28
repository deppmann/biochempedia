"""A survival factor has a ceiling  (Developmental Neuroscience, neurotrophic hypothesis)

COLOR MAP (one color per concept, whole video)
  BLUE   = a neuron (made, status not yet decided)
  GREEN  = a neuron that survives / the survival curve
  RED    = a neuron that dies or is lost / blocked / antiserum
  YELLOW = nerve growth factor (NGF) and "what the factor can support"
  TEAL   = the number of neurons made (the ceiling)
  PURPLE = the receptor TrkA (the knockout)
  GREY   = target tissue, axes, structure, empty slots
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
GA = 2.399963


# ---------------------------------------------------------------------------------------------
def disk_pts(n, sp, center):
    """phyllotaxis points: the first k are the same for any n."""
    return [np.array([center[0] + sp * np.sqrt(k + 0.5) * np.cos(k * GA),
                      center[1] + sp * np.sqrt(k + 0.5) * np.sin(k * GA), 0]) for k in range(n)]


def dot(p, color=BLUE, r=0.16, op=0.95):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).move_to(p)


def slot(p, r=0.16):
    return DashedVMobject(Circle(radius=r, stroke_color=GREY, stroke_width=2, stroke_opacity=0.7).move_to(p), num_dashes=10)


def to_state(d, color, op):
    return d.animate.set_stroke(color, opacity=op).set_fill(color, opacity=op * 0.95)


def status(text, color=GREY, y=-3.3, x=0.0):
    return T(text, 26, color).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def cross(center, s=0.4, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7))


class S00Title(TitleCard):
    LESSON = "The neurotrophic hypothesis tested"
    TITLE = "A survival factor has a ceiling"


# ---------------------------------------------------------------------------------------------
class S01Swell(SpokenScene):
    """a ganglion of dots swells with NGF, wastes with antiserum, then waits under a question."""

    def construct(self):
        C = np.array([0.6, 0.0, 0])
        P = disk_pts(30, 0.46, C)
        base = VGroup(*[dot(p) for p in P[:14]])
        extra = VGroup(*[dot(p) for p in P[14:]])
        lbl = T("sympathetic ganglion", 28, GREY).move_to([C[0], -3.1, 0])
        self.at("Give a young mammal")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in base], lag_ratio=0.06), FadeIn(lbl), run_time=1.2)

        ngf = chip("NGF", YELLOW, 34).move_to([-4.6, 0.0, 0])
        a1 = arr([-3.5, 0, 0], [-2.3, 0, 0], YELLOW)
        self.at("extra nerve growth factor")
        self.play(FadeIn(ngf, shift=RIGHT * 0.3), GrowArrow(a1), run_time=0.8)
        self.at("swell")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in extra], lag_ratio=0.04), run_time=1.3)

        anti = chip("antiserum", RED, 32).move_to([-4.6, 0.0, 0])
        self.at("newborn mouse")
        self.play(FadeOut(extra), FadeOut(ngf), FadeOut(a1), run_time=0.5)
        a2 = a1.copy().set_color(RED)
        self.play(FadeIn(anti, shift=RIGHT * 0.3), GrowArrow(a2), run_time=0.7)
        self.at("waste away")
        self.play(*[to_state(d, RED, 0.18) for d in base[4:]], *[to_state(d, RED, 0.9) for d in base[:4]], run_time=0.9)

        q = T("?", 150, GOLD, weight=BOLD).move_to([-4.4, 0.0, 0])
        self.at("Call the protein")
        self.play(FadeOut(anti), FadeOut(a2), *[to_state(d, BLUE, 0.95) for d in base], run_time=0.9)
        ngf2 = chip("NGF", YELLOW, 40).move_to([-4.6, 0.0, 0])
        self.play(FadeIn(ngf2), run_time=0.5)
        self.at("how many neurons")
        self.play(FadeOut(ngf2), FadeIn(q, scale=0.6), Indicate(base, color=BLUE, scale_factor=1.06), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def grid_pts(center, cols=4, rows=3, sp=0.95):
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(np.array([center[0] + (c - (cols - 1) / 2) * sp, center[1] + ((rows - 1) / 2 - r) * sp, 0]))
    return out


class S02Two(SpokenScene):
    """one small ganglion, two stories; then chick: many formed with fibres, dying cells later."""

    def construct(self):
        small = VGroup(*[dot(p, r=0.22) for p in disk_pts(6, 0.62, [0, 0.3, 0])])
        sl = T("a small ganglion", 32, GREY).move_to([0, -1.9, 0])
        self.at("A small ganglion")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in small], lag_ratio=0.1), FadeIn(sl), run_time=1.0)

        L, R = np.array([-3.4, 0.2, 0]), np.array([3.4, 0.2, 0])
        PL, PR = disk_pts(12, 0.42, L), disk_pts(12, 0.42, R)
        slotsL = VGroup(*[slot(p, 0.18) for p in PL])
        slotsR = VGroup(*[slot(p, 0.18) for p in PR])
        dL = VGroup(*[dot(p, r=0.18) for p in PL[:6]])
        dR = VGroup(*[dot(p, r=0.18) for p in PR])
        tL = T("too few were made", 30, TEAL).move_to([-3.4, 2.7, 0])
        tR = T("made, then some lost", 30, RED).move_to([3.4, 2.7, 0])
        self.at("two things")
        self.play(FadeOut(small), FadeOut(sl), run_time=0.5)
        self.at("Either too few")
        self.play(FadeIn(slotsL), FadeIn(tL), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dL], lag_ratio=0.08), run_time=0.8)
        self.at("normal number")
        self.play(FadeIn(slotsR), FadeIn(tR), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dR], lag_ratio=0.05), run_time=0.9)
        self.at("some were lost")
        self.play(*[to_state(d, RED, 0.0) for d in dR[6:]], run_time=1.4)

        # ---- chick timeline -------------------------------------------------------------
        head = chip("chick spinal ganglia", GREY, 28).move_to([0, 3.0, 0])
        cA, cB = np.array([-3.7, 0.0, 0]), np.array([3.7, 0.0, 0])
        gA, gB = grid_pts(cA), grid_pts(cB)
        nA = VGroup(*[dot(p, r=0.24) for p in gA])
        fA = VGroup(*[Line(p + [0.24, 0, 0], p + [0.62, 0, 0], color=BLUE, stroke_width=3) for p in gA])
        nB = VGroup(*[dot(p, r=0.24) for p in gB])
        fB = VGroup(*[Line(p + [0.24, 0, 0], p + [0.62, 0, 0], color=BLUE, stroke_width=3) for p in gB])
        early = T("early", 30, GREY).move_to([-3.7, -2.1, 0])
        late = T("later", 30, GREY).move_to([3.7, -2.1, 0])
        tl = arr([-1.3, 0, 0], [1.3, 0, 0], GREY)
        self.at("In chick spinal ganglia")
        self.play(FadeOut(VGroup(slotsL, slotsR, dL, dR, tL, tR)), FadeIn(head), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in nA], lag_ratio=0.05), FadeIn(early), run_time=1.0)
        self.at("formed and grew")
        self.play(LaggedStart(*[Create(f) for f in fA], lag_ratio=0.03), run_time=0.6)
        self.at("first")
        self.play(GrowArrow(tl), FadeIn(nB), FadeIn(fB), FadeIn(late), run_time=0.6)
        self.at("Dying cells")
        dying = [0, 3, 5, 6, 9]
        self.play(*[to_state(nB[i], RED, 0.25) for i in dying], *[fB[i].animate.set_stroke(RED, opacity=0.25) for i in dying],
                  run_time=1.2)
        op = T("Neurons are overproduced", 32, TEAL).move_to([0, -3.1, 0])
        self.at("overproduced")
        self.play(FadeIn(op, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
NY = [2.3 - 0.42 * i for i in range(12)]
NX = -5.3
TX0 = 1.8   # target left edge
WIN = [0, 2, 3, 6, 8, 10]


def build_race():
    neu = VGroup(*[dot([NX, y, 0], BLUE, r=0.17) for y in NY])
    axs = VGroup(*[Line([NX + 0.17, y, 0], [TX0, y, 0], color=BLUE, stroke_width=2.5, stroke_opacity=0.8) for y in NY])
    tgt = RoundedRectangle(corner_radius=0.25, width=3.4, height=5.5, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.15).move_to([TX0 + 1.7, -0.05, 0])
    tlbl = T("target", 28, GREY).move_to([TX0 + 1.7, 2.95, 0])
    return neu, axs, tgt, tlbl


FACT_PTS = [np.array([TX0 + 1.1 + (i % 3) * 0.55, 0.7 - (i // 3) * 0.55, 0]) for i in range(6)]


class S03Limit(SpokenScene):
    """twelve neurons reach a target with a few factor dots; those that take one live, the rest die."""

    def construct(self):
        neu, axs, tgt, tlbl = build_race()
        self.at("The target is the tissue")
        self.play(FadeIn(tgt), FadeIn(tlbl), run_time=0.7)
        self.at("axon grows to")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in neu], lag_ratio=0.04), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in axs], lag_ratio=0.05), run_time=1.4)
        fd = VGroup(*[dot(p, YELLOW, r=0.17) for p in FACT_PTS])
        fchip = chip("limited factor", YELLOW, 24).move_to([TX0 + 1.7, -1.5, 0])
        self.at("supplies the factor")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in fd], lag_ratio=0.1), run_time=0.9)
        self.at("amount is limited")
        self.play(FadeIn(fchip), run_time=0.5)
        st = status("axons take up the factor", YELLOW)
        self.at("take it up")
        self.play(FadeIn(st), run_time=0.3)
        moves = []
        for k, i in enumerate(WIN):
            moves.append(fd[k].animate.move_to([NX + 0.5, NY[i], 0]))
        self.play(*moves, run_time=1.6)
        self.play(*[to_state(neu[i], GREEN, 0.95) for i in WIN], *[axs[i].animate.set_stroke(GREEN, opacity=0.9) for i in WIN],
                  *[FadeOut(fd[k], scale=0.3) for k in range(6)], run_time=0.6)
        lose = [i for i in range(12) if i not in WIN]
        st2 = status("too little factor: they die by apoptosis", RED)
        self.at("die by apoptosis")
        self.play(FadeOut(st), FadeIn(st2), *[to_state(neu[i], RED, 0.25) for i in lose],
                  *[axs[i].animate.set_stroke(RED, opacity=0.25) for i in lose], run_time=1.4)
        st3 = status("the idea: neurons compete for a limiting amount", TEXT)
        self.at("the idea is")
        self.play(FadeOut(st2), FadeIn(st3), FadeOut(fchip), run_time=0.5)
        self.at("not before")
        self.play(Indicate(tgt, color=GREY, scale_factor=1.03), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def axes_at(origin, w, h, xlabel, ylabel):
    o = np.array(origin, float)
    xa = Arrow(o, o + [w, 0, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    ya = Arrow(o, o + [0, h, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    xl = T(xlabel, 26, GREY).move_to(o + [w - (1.6 if len(xlabel) < 20 else 2.8), -0.5, 0])
    yl = T(ylabel, 26, GREY).rotate(PI / 2).move_to(o + [-0.55, h / 2, 0])
    return VGroup(xa, ya, xl, yl)


class S04Trka(SpokenScene):
    """antiserum doubt -> knockout; schematic ganglion count rises, then falls after E15.5."""

    def construct(self):
        anti = chip("antiserum: binds something else?", RED, 26).move_to([0, 3.0, 0])
        O0 = [-5.4, -2.7, 0]
        ax0 = axes_at(O0, 11.0, 4.6, "embryonic age", "neurons in the ganglion")
        self.at("carries a doubt")
        self.play(FadeIn(anti, shift=DOWN * 0.2), FadeIn(ax0), run_time=0.7)
        ko = chip("TrkA knockout mouse (no TrkA)", PURPLE, 28).move_to([0, 3.0, 0])
        O = [-5.4, -2.7, 0]
        W, H = 11.0, 4.6
        ax = ax0
        o = np.array(O)
        plateau = 3.1
        xs = np.linspace(0, 6.4, 60)
        rise = [o + [x, plateau / (1 + np.exp(-(x - 2.6) * 1.5)) - plateau / (1 + np.exp(2.6 * 1.5)), 0] for x in xs]
        rise_m = VMobject(color=BLUE, stroke_width=7).set_points_smoothly(rise)
        sch = T("schematic", 24, GREY).move_to([o[0] + 9.8, o[1] + 4.2, 0])
        self.at("knockout mouse")
        self.play(FadeOut(anti, shift=UP * 0.2), FadeIn(ko, shift=UP * 0.2), FadeIn(sch), run_time=0.7)
        span = self.t_of("Neurons are made") - 0.4 - self.elapsed()
        self.play(Create(rise_m), run_time=max(1.6, span), rate_func=linear)
        end = rise[-1]
        self.at("Neurons are made")
        self.play(Indicate(rise_m, color=BLUE, scale_factor=1.0), run_time=0.8)
        tick = Line([end[0], o[1] - 0.12, 0], [end[0], o[1] + 0.12, 0], color=TEXT, stroke_width=4)
        tl = M("E15.5", 26, TEXT).move_to([end[0], o[1] - 0.45, 0])
        self.at("lost after embryonic day")
        self.play(FadeIn(tick), FadeIn(tl), run_time=0.5)
        fall_pts = [end + [x, -(1 - np.exp(-x * 0.9)) * 2.0, 0] for x in np.linspace(0, 3.2, 48)]
        fall = VGroup()
        for k in range(6):
            seg = VMobject(color=RED, stroke_width=7, stroke_opacity=1.0 - 0.14 * k)
            seg.set_points_smoothly(fall_pts[k * 8: k * 8 + 9] if k < 5 else fall_pts[40:48])
            fall.add(seg)
        self.play(Create(fall), run_time=1.6)
        self.at("What failed")
        sv = T("survival fails", 30, RED, weight=BOLD).move_to([end[0] + 2.1, end[1] - 0.85, 0])
        self.play(FadeIn(sv, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Excess(SpokenScene):
    """the race again, with excess factor: ghosts return to life; no new neuron is made."""

    def construct(self):
        neu, axs, tgt, tlbl = build_race()
        lose = [i for i in range(12) if i not in WIN]
        for i in WIN:
            neu[i].set_stroke(GREEN, opacity=0.95).set_fill(GREEN, opacity=0.9)
            axs[i].set_stroke(GREEN, opacity=0.9)
        for i in lose:
            neu[i].set_stroke(RED, opacity=0.25).set_fill(RED, opacity=0.24)
            axs[i].set_stroke(RED, opacity=0.25)
        self.add(tgt, tlbl, neu, axs)
        pts = [np.array([TX0 + 0.6 + (i % 5) * 0.55, 1.7 - (i // 5) * 0.55, 0]) for i in range(20)]
        fd = VGroup(*[dot(p, YELLOW, r=0.17) for p in pts])
        fchip = chip("excess NGF", YELLOW, 26).move_to([TX0 + 1.7, -1.7, 0])
        self.at("developing chick embryo")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in fd], lag_ratio=0.04), FadeIn(fchip), run_time=1.4)
        self.at("get larger")
        self.play(*[to_state(neu[i], GREEN, 0.95) for i in lose], *[axs[i].animate.set_stroke(GREEN, opacity=0.9) for i in lose],
                  run_time=1.2)
        st = status("more of the neurons that were made survive", GREEN)
        self.at("escape the normal death")
        self.play(FadeIn(st), Indicate(VGroup(*[neu[i] for i in lose]), color=GREEN, scale_factor=1.3), run_time=0.9)
        c1 = chip("count neurons and dying cells", TEAL, 24)
        c2 = chip("mark dividing cells", TEAL, 24)
        row = VGroup(c1, c2).arrange(RIGHT, buff=0.4).move_to([0, -3.3, 0])
        self.at("count neurons")
        self.play(FadeOut(st), FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("mark dividing cells")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        sl13 = slot([NX, 2.85, 0], 0.17)
        nn = T("survival adds none", 26, GREY).move_to([NX + 2.1, 2.85, 0])
        self.at("No new neurons")
        self.play(FadeOut(row), FadeIn(sl13), FadeIn(nn), run_time=0.7)
        same = T("same type of neuron", 26, GREY).move_to([0, -3.3, 0])
        self.at("what kind of neuron")
        self.play(FadeIn(same), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Ceiling(SpokenScene):
    """survivors = smaller of (made) and (factor supports): rises, then flat at the ceiling."""

    def construct(self):
        O = np.array([-4.8, -2.55, 0])
        W, H = 10.4, 4.0
        ax = axes_at(O, W, H, "factor the target can support", "neurons surviving")
        N = 2.9
        s = 0.5
        kx = N / s
        ceil = DashedLine(O + [0, N, 0], O + [W - 0.2, N, 0], color=TEAL, stroke_width=4)
        cl = T("neurons made", 28, TEAL).move_to(O + [2.0, N + 0.42, 0])
        self.at("a ceiling")
        self.play(FadeIn(ax), Create(ceil), FadeIn(cl), run_time=1.0)

        head = T("neurons surviving = the smaller of", 28, TEXT).move_to([0, 3.2, 0])
        ca = chip("neurons made", TEAL, 26)
        cb = chip("factor can support", YELLOW, 26)
        andt = T("and", 26, GREY)
        row = VGroup(ca, andt, cb).arrange(RIGHT, buff=0.4).move_to([0, 2.45, 0])
        self.at("smaller of two")
        self.play(FadeIn(head), FadeIn(row, shift=DOWN * 0.1), run_time=0.8)

        rise = Line(O, O + [kx, N, 0], color=GREEN, stroke_width=8)
        flat = Line(O + [kx, N, 0], O + [W - 0.2, N, 0], color=GREEN, stroke_width=8)
        mk = Dot(O, radius=0.17, color=YELLOW)
        self.at("Extra factor")
        self.play(FadeIn(mk), run_time=0.3)
        self.play(Create(rise), mk.animate.move_to(O + [kx, N, 0]), run_time=2.0, rate_func=linear)
        self.play(Indicate(cb, color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("raises the first")
        self.play(Indicate(ca, color=TEAL, scale_factor=1.12), Indicate(ceil, color=TEAL), run_time=0.8)
        up = inhib(O + [W - 1.0, N + 0.12, 0], O + [W - 1.0, N + 0.95, 0])
        self.play(Create(flat), mk.animate.move_to(O + [W - 1.0, N, 0]), run_time=1.4, rate_func=linear)
        self.play(FadeIn(up), run_time=0.4)
        note = T("one population, its own factor", 26, GREY).move_to(O + [7.4, 0.7, 0])
        self.at("population you measured")
        self.play(FadeIn(note), run_time=0.6)
        self.at("can decide how many")
        self.play(Indicate(rise, color=GREEN, scale_factor=1.0), run_time=0.9)
        self.at("cannot add")
        self.play(Indicate(up, color=RED, scale_factor=1.3), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Survival alone cannot add neurons never made."
