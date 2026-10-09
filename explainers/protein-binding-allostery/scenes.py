"""How hemoglobin talks to itself  (Biochemistrypedia: Protein binding & allostery)

COLOR MAP (one color per concept, whole video)
  BLUE   = protein / hemoglobin in the tense (T) state / receptor sites
  GREEN  = relaxed (R) state, high affinity, "tighter" binding
  YELLOW = O2, the ligand, and the half-saturation marker
  RED    = carbon monoxide (CO) and CO-hemoglobin
  TEAL   = 2,3-BPG (the allosteric regulator)
  GOLD   = cooperativity / the Hill coefficient n / call-outs
  TEXT   = equations, neutral labels, emphasis;  GREY = axes, secondary labels, "without regulator"
NO molecular structures are drawn: only labelled blocks, arrows and curves computed from
   Y = L/(Kd+L)   and   Y = x^n / (P50^n + x^n).
"""
import json
import os
import re

import numpy as np

from bp_style import *


# ---------------------------------------------------------------- helpers
def starts(scene_id):
    """Fraction of the narration at which each sentence begins (by character count)."""
    sc = json.load(open(os.environ["KX_SCRIPT"]))["scenes"]
    text = next(s["narration"] for s in sc if s["id"] == scene_id)
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
    tot = sum(len(s) for s in sents)
    out, acc = [], 0
    for s in sents:
        out.append(acc / tot)
        acc += len(s)
    return out + [1.0]


class Sc(NarratedScene):
    SID = ""

    def setup(self):
        super().setup()
        self.st = starts(self.SID)

    def at(self, i, lead=0.0):
        """Wait until sentence i begins (minus `lead` fraction)."""
        r = (self.st[i] - lead) * self.narration_s - self.elapsed()
        if os.environ.get("KX_DEBUG"):
            print(f"[at] {self.SID} sentence {i}: target {(self.st[i]-lead)*self.narration_s:.1f}s, elapsed {self.elapsed():.1f}s", flush=True)
        if r > 0.02:
            self.wait(r)

    def at_s(self, t):
        """Wait until absolute second t of the narration (sentence starts measured from the audio)."""
        r = t - self.elapsed()
        if os.environ.get("KX_DEBUG"):
            print(f"[at_s] {self.SID}: target {t:.1f}s, elapsed {self.elapsed():.1f}s", flush=True)
        if r > 0.02:
            self.wait(r)

    def span(self, i, frac=1.0):
        """Seconds of sentence i (scaled)."""
        return max(0.4, (self.st[i + 1] - self.st[i]) * self.narration_s * frac)


def hill(x, p50, n):
    return x ** n / (p50 ** n + x ** n)


def mk_axes(xmax, w, h, xlab, ylab, xt, yt, center, ymax=1.0, ysize=24):
    ax = Axes(x_range=[0, xmax, xmax], y_range=[0, ymax, ymax], x_length=w, y_length=h, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3})
    ax.move_to(center)
    deco = VGroup()
    for v, lab in xt:
        deco.add(M(lab, 24, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
    for v, lab in yt:
        deco.add(M(lab, 24, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15))
    xl = T(xlab, 26, GREY).next_to(ax.x_axis, DOWN, buff=0.62)
    yl = T(ylab, 26, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.55)
    deco.add(xl, yl)
    return ax, deco


def o2(r=0.3):
    c = Circle(radius=r, color=YELLOW, fill_opacity=1, stroke_width=0)
    return VGroup(c, T("O₂", 24, BG, weight=BOLD).move_to(c))


def co(r=0.3):
    c = Circle(radius=r, color=RED, fill_opacity=1, stroke_width=0)
    return VGroup(c, T("CO", 24, BG, weight=BOLD).move_to(c))


def sub(label, color, size=1.25, op=0.18):
    r = RoundedRectangle(corner_radius=0.16, width=size, height=size, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=op)
    return VGroup(r, T(label, 34, color).move_to(r))


def hb(gap=0.55, color=BLUE, size=1.25, op=0.18, labels=("α", "β", "β", "α")):
    """Schematic 4-subunit protein: four labelled blocks (beta chains on the diagonal)."""
    d = (size + gap) / 2
    pos = [(-d, d), (d, d), (-d, -d), (d, -d)]
    g = VGroup()
    for (x, y), lab in zip(pos, labels):
        s = sub(lab, color, size, op)
        s.move_to([x, y, 0])
        g.add(s)
    return g


def socket_of(s):
    """Where O2 docks on a subunit block (its upper-right corner, just inside)."""
    return s[0].get_corner(UR) + np.array([-0.05, -0.05, 0])


# ---------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "Protein binding & allostery"
    TITLE = "How hemoglobin talks to itself"


class S06End(EndCard):
    LINE = "Four subunits, one conversation: that is cooperativity."


# ---------------------------------------------------------------- s01: Kd = half-saturation
class S01Kd(Sc):
    SID = "s01_kd"

    def construct(self):
        # --- sentence 1: the reaction, written in the direction it comes apart
        R = chip("R", BLUE, 40)
        L = chip("L", YELLOW, 40)
        cx = VGroup(R.copy(), L.copy()).arrange(RIGHT, buff=0.06)
        cbox = SurroundingRectangle(cx, color=GREY, buff=0.15, corner_radius=0.2, stroke_width=2)
        complex_ = VGroup(cx, cbox).move_to(LEFT * 4.2 + UP * 0.7)
        arr = Arrow(LEFT * 2.3 + UP * 0.7, LEFT * 0.4 + UP * 0.7, color=TEXT, buff=0, stroke_width=6)
        free_R = chip("R", BLUE, 40).move_to(RIGHT * 1.2 + UP * 0.7)
        plus = T("+", 40).move_to(RIGHT * 2.55 + UP * 0.7)
        free_L = chip("L", YELLOW, 40).move_to(RIGHT * 3.9 + UP * 0.7)
        lab_b = T("bound", 26, GREY).next_to(complex_, DOWN, buff=0.3)
        lab_f = T("free", 26, GREY).next_to(VGroup(free_R, free_L), DOWN, buff=0.3)
        self.play(FadeIn(complex_, shift=UP * 0.15), FadeIn(lab_b), run_time=self.beat(0.06))
        self.wait(self.beat(0.05))
        self.play(GrowArrow(arr), run_time=self.beat(0.05))
        self.play(TransformFromCopy(cx[0], free_R), TransformFromCopy(cx[1], free_L), FadeIn(plus),
                  FadeIn(lab_f), run_time=self.beat(0.10))
        # --- sentence 2: the ratio of loose to bound
        self.at(1)
        num = VGroup(M("[R]", 38, BLUE), M("[L]", 38, YELLOW)).arrange(RIGHT, buff=0.14)
        den = M("[RL]", 38, TEXT)
        bar = Line(LEFT, RIGHT, color=TEXT, stroke_width=3).set_width(num.width + 0.4)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.14)
        eq = VGroup(M("Kd =", 38, GOLD), frac).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.9)
        loose = T("loose", 26, GREY).next_to(num, RIGHT, buff=0.35)
        tight = T("bound", 26, GREY).next_to(den, RIGHT, buff=0.35)
        units = T("units: concentration", 28, GOLD).next_to(eq, LEFT, buff=0.9)
        self.play(Write(eq), run_time=self.beat(0.10))
        self.play(FadeIn(loose, shift=LEFT * 0.1), FadeIn(tight, shift=LEFT * 0.1), run_time=self.beat(0.05))
        self.play(FadeIn(units, shift=RIGHT * 0.1), run_time=self.beat(0.05))
        # --- sentence 3: Kd is the half-occupied concentration
        self.at(2)
        self.play(FadeOut(VGroup(complex_, lab_b, arr, free_R, plus, free_L, lab_f, loose, tight, units)),
                  eq.animate.scale(0.8).to_edge(UP, buff=0.3), run_time=self.beat(0.04))
        KD = 2.0
        ax, deco = mk_axes(10, 6.4, 3.6, "free ligand [L]  (µM)", "fraction of receptor bound",
                           [(5, "5"), (10, "10")], [(1, "1")], LEFT * 2.35 + DOWN * 0.55)
        curve = ax.plot(lambda x: x / (KD + x), x_range=[0, 10, 0.02], color=BLUE, stroke_width=5)
        t = ValueTracker(0.0)
        fy = lambda: t.get_value() / (KD + t.get_value())
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), fy()), color=YELLOW, radius=0.11))
        vline = always_redraw(lambda: DashedLine(ax.c2p(t.get_value(), 0), ax.c2p(t.get_value(), fy()),
                                                 color=YELLOW, stroke_width=3))
        hline = always_redraw(lambda: DashedLine(ax.c2p(0, fy()), ax.c2p(t.get_value(), fy()),
                                                 color=YELLOW, stroke_width=3))

        def recep():
            y = fy()
            cells = VGroup()
            for i in range(10):
                box = RoundedRectangle(corner_radius=0.1, width=0.6, height=0.6, stroke_color=BLUE,
                                       stroke_width=2.5, fill_color=BLUE, fill_opacity=0.14)
                lig = Circle(radius=0.17, stroke_width=0, fill_color=YELLOW,
                             fill_opacity=float(np.clip(10 * y - i, 0, 1))).move_to(box)
                cells.add(VGroup(box, lig))
            return cells.arrange_in_grid(2, 5, buff=0.18).move_to(RIGHT * 4.1 + UP * 0.5)

        rec = always_redraw(recep)
        rec_t = T("receptor sites", 26, GREY).move_to(RIGHT * 4.1 + UP * 1.75)
        occ = always_redraw(lambda: M(f"{100 * fy():.0f}% occupied", 28, YELLOW).move_to(RIGHT * 4.1 + DOWN * 0.95))
        self.play(Create(ax), FadeIn(deco), run_time=self.beat(0.04))
        self.play(Create(curve), FadeIn(rec), FadeIn(rec_t), FadeIn(occ), FadeIn(dot), run_time=self.beat(0.06))
        self.play(t.animate.set_value(KD), run_time=self.beat(0.09), rate_func=smooth)
        kd_lab = M("Kd", 28, GOLD).next_to(ax.c2p(KD, 0), DOWN, buff=0.15)
        half = M("½", 28, GOLD).next_to(ax.c2p(0, 0.5), LEFT, buff=0.15)
        callout = T("half the sites are full", 26, YELLOW).next_to(ax.c2p(KD, 0.5), DR, buff=0.5)
        self.play(FadeIn(kd_lab), FadeIn(half), FadeIn(callout), run_time=self.beat(0.03))
        # --- sentence 4: smaller Kd = tighter (curve moves left)
        self.at(3)
        [m.clear_updaters() for m in (rec, occ, vline, hline, dot)]
        self.play(*[FadeOut(m) for m in (rec, rec_t, occ, callout, vline, hline, dot)], run_time=self.beat(0.02))
        KD2 = 0.6
        curve2 = ax.plot(lambda x: x / (KD2 + x), x_range=[0, 10, 0.02], color=GREEN, stroke_width=5)
        kd2 = M("Kd", 28, GREEN).next_to(ax.c2p(KD2, 0), DOWN, buff=0.15).shift(DOWN * 0.0)
        d2 = Dot(ax.c2p(KD2, 0.5), color=GREEN, radius=0.11)
        l2 = DashedLine(ax.c2p(KD2, 0), ax.c2p(KD2, 0.5), color=GREEN, stroke_width=3)
        l2h = DashedLine(ax.c2p(0, 0.5), ax.c2p(KD2, 0.5), color=GREEN, stroke_width=3)
        d1 = Dot(ax.c2p(KD, 0.5), color=BLUE, radius=0.11)
        rt1 = VGroup(T("smaller Kd", 36, GREEN), T("tighter binding", 36, GREEN)).arrange(DOWN, buff=0.25)
        rt1.move_to(RIGHT * 4.1 + UP * 0.4)
        down = Arrow(rt1[0].get_bottom(), rt1[1].get_top(), color=GREEN, buff=0.06, stroke_width=5)
        self.play(Create(curve2), FadeIn(d2), Create(l2), Create(l2h), FadeIn(d1), run_time=self.beat(0.05))
        self.play(FadeIn(kd2), FadeIn(rt1[0]), run_time=self.beat(0.02))
        self.play(GrowArrow(down), FadeIn(rt1[1]), run_time=self.beat(0.02))
        # --- sentence 5: the classic error
        warn = T("Kd is not Ka", 34, GOLD)
        under = T("lower Kd = tighter", 34, GREEN)
        wb = VGroup(warn, under).arrange(DOWN, buff=0.35).move_to(RIGHT * 4.1 + DOWN * 2.1)
        self.at_s(31.5)
        self.play(FadeIn(warn, shift=UP * 0.1), run_time=0.8)
        self.at_s(33.5)
        self.play(FadeIn(under, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- s02: hyperbola -> sigmoid
class S02Sigmoid(Sc):
    SID = "s02_sigmoid"

    def construct(self):
        P50 = 26
        ax, deco = mk_axes(100, 6.2, 3.7, "oxygen pressure pO₂  (torr)", "fraction of sites bound",
                           [(50, "50"), (100, "100")], [(1, "1")], LEFT * 2.65 + DOWN * 0.4)
        hyper = ax.plot(lambda x: x / (P50 + x), x_range=[0, 100, 0.5], color=BLUE, stroke_width=5)
        sig = ax.plot(lambda x: hill(x, P50, 2.8), x_range=[0, 100], color=GOLD, stroke_width=5)
        # sentence 1: one site, one ligand -> hyperbola
        site = sub("site", BLUE, 1.5)
        site.move_to(RIGHT * 3.9 + DOWN * 0.3)
        cap1 = T("one site, one ligand", 30, BLUE).move_to(RIGHT * 3.9 + UP * 1.7)
        lig = o2().move_to(RIGHT * 6.0 + DOWN * 0.3 + UP * 1.2)
        self.play(Create(ax), FadeIn(deco), run_time=self.beat(0.04))
        self.play(FadeIn(site), FadeIn(cap1), FadeIn(lig), run_time=self.beat(0.03))
        self.play(lig.animate.move_to(socket_of(site) + np.array([-0.05, 0.0, 0])).scale(1.0),
                  Create(hyper), run_time=self.beat(0.11))
        # sentence 2: several sites that sense each other -> curve changes shape
        self.at(1)
        H = hb(0.28, BLUE).scale(0.92).move_to(RIGHT * 3.9 + UP * 0.45)
        cap2 = T("four sites that sense each other", 28, GOLD).move_to(RIGHT * 3.9 + UP * 2.65)
        self.play(FadeOut(lig), FadeOut(cap1), FadeOut(site, scale=0.8), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in H], lag_ratio=0.25), FadeIn(cap2, shift=DOWN * 0.1),
                  run_time=1.6)
        self.play(Transform(hyper, sig), run_time=self.beat(0.1))
        # sentence 3: binding at one site raises affinity at the others
        self.at(2)
        names = T("hemoglobin", 28, TEXT).next_to(H, DOWN, buff=0.35)
        self.play(FadeIn(names), run_time=self.beat(0.03))
        o_a = o2(0.3).move_to(H.get_center() + RIGHT * 4.5 + UP * 1.2)
        o_b = o2(0.3).move_to(H.get_center() + RIGHT * 4.5 + DOWN * 1.2)
        self.play(FadeIn(o_a), run_time=self.beat(0.02))
        self.play(o_a.animate.move_to(socket_of(H[0]) + np.array([-0.05, 0, 0])),
                  run_time=self.beat(0.05))
        # the other three brighten ("affinity up")
        self.play(*[H[i][0].animate.set_fill(GOLD, 0.45).set_stroke(GOLD) for i in (1, 2, 3)],
                  *[H[i][1].animate.set_color(GOLD) for i in (1, 2, 3)],
                  run_time=self.beat(0.06))
        up = T("affinity ↑", 30, GOLD).next_to(names, DOWN, buff=0.25)
        self.play(FadeIn(up, shift=UP * 0.1), run_time=self.beat(0.03))
        self.play(FadeIn(o_b), run_time=self.beat(0.01))
        self.play(o_b.animate.move_to(socket_of(H[3]) + np.array([-0.05, 0, 0])),
                  run_time=self.beat(0.05))
        coop = T("= cooperativity", 30, GOLD).next_to(up, DOWN, buff=0.15)
        self.play(FadeIn(coop), run_time=self.beat(0.03))
        # sentence 4: the sigmoid
        self.at(3)
        steep = ax.plot(lambda x: hill(x, P50, 2.8), x_range=[15, 40], color=TEXT, stroke_width=9)
        s_lab = T("S-shaped: a sigmoid", 30, GOLD).next_to(ax.c2p(52, 0.34), RIGHT, buff=0.0).shift(RIGHT * 0.05)
        self.play(Create(steep), run_time=self.beat(0.1))
        self.play(FadeIn(s_lab, shift=UP * 0.1), run_time=self.beat(0.06))
        self.finish()


# ---------------------------------------------------------------- s03: the Hill coefficient
class S03Hill(Sc):
    SID = "s03_hill"

    def construct(self):
        ax, deco = mk_axes(3, 6.0, 3.7, "ligand  (× the half-saturation value)", "fraction bound",
                           [(1, "1"), (2, "2"), (3, "3")], [(0.5, "½"), (1, "1")], LEFT * 2.55 + DOWN * 0.4)
        n = ValueTracker(1.0)
        curve = always_redraw(lambda: ax.plot(lambda x: hill(x, 1.0, n.get_value()), x_range=[0.001, 3],
                                              color=BLUE, stroke_width=5))
        mid = Dot(ax.c2p(1, 0.5), color=YELLOW, radius=0.11)

        def tangent():
            s = n.get_value() / 4
            dx = 0.42
            return Line(ax.c2p(1 - dx, 0.5 - s * dx), ax.c2p(1 + dx, 0.5 + s * dx), color=GOLD, stroke_width=6)

        tan = always_redraw(tangent)
        # right-hand gauge for n
        GX = 4.1
        n_read = always_redraw(lambda: M(f"n = {n.get_value():.1f}", 54, GOLD).move_to(RIGHT * GX + UP * 1.7))
        bar = Line(RIGHT * (GX - 2.0), RIGHT * (GX + 2.0), color=GREY, stroke_width=5).move_to(RIGHT * GX + UP * 0.6)

        def nx(v):
            return bar.get_start() + (bar.get_end() - bar.get_start()) * ((v - 1) / 3)

        ticks = VGroup(*[Line(nx(v) + UP * 0.12, nx(v) + DOWN * 0.12, color=GREY, stroke_width=4) for v in (1, 4)])
        tl = VGroup(M("1", 26, GREY).next_to(nx(1), DOWN, buff=0.22), M("4", 26, GREY).next_to(nx(4), DOWN, buff=0.22))
        marker = always_redraw(lambda: Triangle(color=GOLD, fill_opacity=1, stroke_width=0).scale(0.16)
                               .rotate(PI).move_to(nx(n.get_value()) + UP * 0.28))
        gauge_title = T("teamwork, as one number", 28, GREY).move_to(RIGHT * GX + UP * 2.65)
        # sentence 1: the number for teamwork
        self.play(FadeIn(gauge_title), FadeIn(n_read), run_time=self.beat(0.03))
        self.play(Create(bar), FadeIn(ticks), FadeIn(tl), FadeIn(marker), run_time=self.beat(0.05))
        # sentence 2: plot, fit, slope
        self.at_s(3.2)
        self.play(Create(ax), FadeIn(deco), run_time=1.0)
        self.add(curve)
        self.play(FadeIn(mid), run_time=0.6)
        self.add(tan)
        slope_lab = T("slope", 28, GOLD).next_to(ax.c2p(1.5, 0.5), DOWN, buff=0.35).shift(RIGHT * 0.2)
        self.play(FadeIn(slope_lab), run_time=0.6)
        self.play(n.animate.set_value(2.8), run_time=2.4, rate_func=smooth)
        self.play(n.animate.set_value(1.0), run_time=1.6, rate_func=smooth)
        # sentence 3: n = 1 -> every site alone, myoglobin
        self.at_s(10.2)
        lab1 = T("n = 1: every site alone", 28, BLUE).move_to(RIGHT * GX + DOWN * 0.6)
        lab1b = T("myoglobin's hyperbola", 28, BLUE).next_to(lab1, DOWN, buff=0.18)
        self.play(FadeIn(lab1), FadeIn(lab1b), FadeOut(slope_lab), run_time=self.beat(0.05))
        # sentence 4: n > 1 -> positive cooperativity
        self.at_s(15.9)
        lab2 = T("n > 1: positive cooperativity", 28, GOLD).move_to(RIGHT * GX + DOWN * 2.1)
        self.play(FadeIn(lab2, shift=UP * 0.1), n.animate.set_value(2.0), run_time=self.beat(0.08), rate_func=smooth)
        # sentence 5: hemoglobin 2.8, max 4
        self.at_s(19.1)
        ghost = ax.plot(lambda x: hill(x, 1.0, 4.0), x_range=[0.001, 3], color=GREY, stroke_width=3)
        ghost = DashedVMobject(ghost, num_dashes=40)
        ghost_lab = T("max 4", 26, GREY).next_to(ax.c2p(2.35, 1.0), UP, buff=0.08)
        hb_lab = T("hemoglobin", 32, GOLD).move_to(RIGHT * GX + DOWN * 0.55)
        self.play(FadeOut(lab1), FadeOut(lab1b), FadeOut(lab2), run_time=0.4)
        self.play(FadeIn(hb_lab), run_time=0.4)
        self.play(n.animate.set_value(2.8), Create(ghost), FadeIn(ghost_lab), run_time=self.beat(0.1), rate_func=smooth)
        hb_pos = T("strong, but not perfect", 28, GOLD).move_to(RIGHT * GX + DOWN * 1.35)
        self.play(FadeIn(hb_pos, shift=UP * 0.1), run_time=self.beat(0.04))
        # sentence 6: black box
        self.at_s(26.3)
        self.play(FadeOut(hb_pos), run_time=self.beat(0.02))
        score = T("scores how loudly", 30, TEXT).move_to(RIGHT * GX + DOWN * 1.5)
        score2 = T("the subunits talk", 30, TEXT).next_to(score, DOWN, buff=0.15)
        self.play(FadeIn(score), FadeIn(score2), run_time=self.beat(0.05))
        for _ in range(2):
            self.play(Indicate(marker, color=GOLD, scale_factor=1.8), Indicate(tan, color=GOLD, scale_factor=1.15),
                      run_time=1.1)
        self.finish()


# ---------------------------------------------------------------- s04: 2,3-BPG
class S04Bpg(Sc):
    SID = "s04_bpg"

    def construct(self):
        # sentence 1: a dial for oxygen unloading
        face = Circle(radius=1.25, color=GREY, stroke_width=4).move_to(UP * 0.3)
        marks = VGroup(*[Line(face.get_center() + 1.0 * np.array([np.cos(a), np.sin(a), 0]),
                              face.get_center() + 1.2 * np.array([np.cos(a), np.sin(a), 0]), color=GREY,
                              stroke_width=3) for a in np.linspace(PI * 0.85, PI * 0.15, 7)])
        needle = Line(face.get_center(), face.get_center() + 0.95 * np.array([np.cos(PI * 0.8), np.sin(PI * 0.8), 0]),
                      color=TEAL, stroke_width=7)
        hub = Dot(face.get_center(), color=TEAL, radius=0.1)
        dial_lab = T("O₂ unloading", 32, TEXT).next_to(face, DOWN, buff=0.4)
        dial_t = T("2,3-BPG: the body's dial", 34, TEAL).next_to(face, UP, buff=0.45)
        self.play(FadeIn(face), FadeIn(marks), FadeIn(needle), FadeIn(hub), FadeIn(dial_lab),
                  FadeIn(dial_t), run_time=self.beat(0.03))
        self.play(Rotate(needle, angle=-PI * 0.6, about_point=face.get_center()), run_time=self.beat(0.05))
        # sentence 2: small, charged, ~1:1, wedges into the cavity between the beta chains
        self.at(1)
        T_ = hb(0.9, BLUE).move_to(DOWN * 0.1)
        self.play(FadeOut(VGroup(face, marks, needle, hub, dial_lab, dial_t)), run_time=0.6)
        self.play(FadeIn(T_), run_time=0.7)
        t_lab = T("hemoglobin, tense (T) state", 28, BLUE).move_to(UP * 2.55)
        self.play(FadeIn(t_lab), run_time=self.beat(0.02))
        bpg = VGroup(Circle(radius=0.5, color=TEAL, fill_opacity=0.95, stroke_width=0),
                     T("BPG", 24, BG, weight=BOLD))
        bpg[1].move_to(bpg[0])
        bpg.move_to(RIGHT * 4.6 + UP * 0.8)
        charge_l = T("small, highly charged", 26, TEAL).next_to(bpg, UP, buff=0.3)
        self.play(FadeIn(bpg), FadeIn(charge_l), run_time=self.beat(0.07))
        ratio = M("1 BPG : 1 Hb", 30, TEXT).move_to(RIGHT * 4.6 + DOWN * 1.2)
        self.play(FadeIn(ratio), run_time=self.beat(0.03))
        cy = T_.get_center()[1]
        cav = T("cavity between β chains", 26, TEAL).move_to(LEFT * 4.5 + UP * cy)
        cav_arr = Arrow(cav.get_right() + RIGHT * 0.1, np.array([-0.3, cy, 0]), color=TEAL, buff=0.05, stroke_width=4)
        self.play(FadeIn(cav), GrowArrow(cav_arr), run_time=self.beat(0.04))
        self.play(bpg.animate.move_to(T_.get_center()), FadeOut(VGroup(charge_l, ratio)),
                  run_time=self.beat(0.12), rate_func=smooth)
        # sentence 3: doorstop, stabilizes T, right-shifts the curve
        self.at_s(17.4)
        ax, deco = mk_axes(100, 5.4, 3.5, "pO₂  (torr)", "fraction bound", [(50, "50"), (100, "100")], [(1, "1")],
                           RIGHT * 3.4 + DOWN * 0.7)
        no_bpg = ax.plot(lambda x: hill(x, 12, 2.7), x_range=[0, 100, 0.5], color=GREY, stroke_width=5)
        with_bpg = ax.plot(lambda x: hill(x, 26, 2.8), x_range=[0, 100, 0.5], color=TEAL, stroke_width=5)

        def leg(y, color, text):
            ln = Line(ax.c2p(27, y), ax.c2p(34, y), color=color, stroke_width=6)
            tx = T(text, 24, color).next_to(ln, RIGHT, buff=0.15)
            return VGroup(ln, tx)

        leg_no, leg_with, leg_fet = leg(0.38, GREY, "without BPG"), leg(0.25, TEAL, "with BPG"), leg(0.12, GREEN, "fetal Hb (higher affinity)")
        grp_hb = VGroup(T_, bpg)
        door = T("doorstop: holds T", 28, TEAL).move_to(LEFT * 3.8 + DOWN * 2.5)
        self.play(FadeOut(VGroup(cav, cav_arr)), grp_hb.animate.scale(0.82).move_to(LEFT * 3.8 + UP * 0.2), t_lab.animate.move_to(LEFT * 3.8 + UP * 2.4),
                  Create(ax), FadeIn(deco), run_time=self.beat(0.05))
        self.play(FadeIn(door), Create(no_bpg), FadeIn(leg_no), run_time=self.beat(0.04))
        self.play(TransformFromCopy(no_bpg, with_bpg), FadeIn(leg_with), run_time=self.beat(0.07))
        shift_arr = Arrow(ax.c2p(14, 0.5), ax.c2p(24, 0.5), color=TEAL, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.5)
        r_lab = T("right shift: more O₂ dumped", 28, TEAL).next_to(ax, UP, buff=0.2)
        self.play(GrowArrow(shift_arr), FadeIn(r_lab), run_time=self.beat(0.04))
        # sentence 4: to reach R, BPG must be expelled
        self.at_s(25.1)
        R_ = hb(0.3, GREEN).scale(0.82).move_to(grp_hb[0].get_center())
        r_state = T("relaxed (R) state", 28, GREEN).move_to(t_lab)
        self.play(Transform(grp_hb[0], R_), Transform(t_lab, r_state),
                  bpg.animate.move_to(grp_hb[0].get_center() + UP * 2.0 + LEFT * 1.6).set_opacity(0),
                  FadeOut(door), run_time=self.beat(0.06))
        expel = T("BPG expelled", 28, TEAL).next_to(R_, DOWN, buff=0.45)
        self.play(FadeIn(expel), run_time=self.beat(0.03))
        # sentence 5: fetal Hb binds BPG weakly -> higher affinity
        self.at_s(29.0)
        self.play(FadeOut(expel), FadeOut(shift_arr), FadeOut(r_lab), run_time=0.5)
        fetal = ax.plot(lambda x: hill(x, 19, 2.6), x_range=[0, 100, 0.5], color=GREEN, stroke_width=5)
        f_hb = hb(0.9, GREEN).scale(0.7).move_to(LEFT * 3.8 + UP * 0.35)
        weak = VGroup(Circle(radius=0.36, color=TEAL, stroke_width=3, fill_opacity=0.0),
                      T("BPG", 24, TEAL)).move_to(f_hb.get_center())
        weak_lab = T("binds BPG weakly", 28, TEAL).move_to(LEFT * 3.8 + DOWN * 2.45)
        f_title = T("fetal hemoglobin", 28, GREEN).move_to(LEFT * 3.8 + UP * 2.35)
        # "Fetal hemoglobin binds it weakly..." (~29.3 s)
        self.play(ReplacementTransform(grp_hb[0], f_hb), ReplacementTransform(t_lab, f_title), run_time=0.6)
        self.play(FadeIn(weak, scale=0.6), run_time=0.5)
        self.play(weak.animate.move_to(LEFT * 3.8 + DOWN * 1.65), FadeIn(weak_lab), run_time=1.0)
        # "...which is why the fetus runs at higher affinity" (~32 s)
        self.at_s(31.7)
        self.play(Create(fetal), FadeIn(leg_fet), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s05: carbon monoxide
class S05Co(Sc):
    SID = "s05_co"

    def construct(self):
        # sentence 1: CO is the R-state lock
        H = hb(0.5, BLUE).scale(1.25).move_to(DOWN * 0.1)
        t_lab = T("hemoglobin", 30, BLUE).move_to(UP * 2.9)
        self.play(FadeIn(H), FadeIn(t_lab), run_time=self.beat(0.02))
        c = co(0.3).move_to(RIGHT * 4.3 + UP * 1.5)
        oxs = []
        for i in (0, 2):
            o = o2(0.3).move_to(socket_of(H[i]) + np.array([-0.05, 0, 0]))
            oxs.append(o)
        self.play(*[FadeIn(o, scale=0.5) for o in oxs], run_time=self.beat(0.02))
        self.play(FadeIn(c), run_time=self.beat(0.01))
        self.play(c.animate.move_to(socket_of(H[1]) + np.array([-0.05, 0, 0])), run_time=self.beat(0.02))
        lock_lab = T("R-state lock", 36, GREEN).move_to(UP * 2.9)
        self.play(*[H[i][0].animate.set_stroke(GREEN).set_fill(GREEN, 0.22) for i in range(4)],
                  *[H[i][1].animate.set_color(GREEN) for i in range(4)],
                  Transform(t_lab, lock_lab), run_time=self.beat(0.025))
        # sentence 2 (measured: starts 2.5 s; "so the oxygen still aboard" ~9.5 s; "a left-shifted curve" ~13 s;
        # "slashed carrying capacity" ~14.9 s; sentence 3 at 17.6 s)
        self.at_s(2.6)
        tight = T("CO binds far tighter than O₂", 28, RED).next_to(H, DOWN, buff=0.45)
        self.play(FadeIn(tight, shift=UP * 0.1), run_time=0.8)
        # "...and holds hemoglobin in the high-affinity relaxed state": keep the green lock, bring in the curve
        ax, deco = mk_axes(100, 5.4, 3.4, "pO₂  (torr)", "O₂ bound (fraction of all Hb)", [(50, "50"), (100, "100")],
                           [(1, "1")], RIGHT * 3.5 + DOWN * 0.15)
        grp = VGroup(H, *oxs, c)
        normal = ax.plot(lambda x: hill(x, 26, 2.8), x_range=[0, 100], color=BLUE, stroke_width=5)
        cohb = ax.plot(lambda x: 0.5 * hill(x, 13, 1.6), x_range=[0, 100], color=RED, stroke_width=5)
        self.at_s(5.6)
        self.play(FadeOut(tight), grp.animate.scale(0.62).move_to(LEFT * 3.9 + UP * 0.0),
                  t_lab.animate.scale(0.85).move_to(LEFT * 3.9 + UP * 1.9), run_time=1.0)
        self.play(Create(ax), FadeIn(deco), run_time=0.9)
        self.play(Create(normal), run_time=1.2)
        l_n = T("normal blood", 26, BLUE).next_to(ax.c2p(60, 1.0), UP, buff=0.1)
        self.play(FadeIn(l_n), run_time=0.4)
        # "...so the oxygen still aboard refuses to release"
        self.at_s(9.4)
        for o in oxs:       # O2 tries to leave and cannot
            self.play(o.animate.shift(LEFT * 0.5 + UP * 0.15), run_time=0.6, rate_func=there_and_back)
        refuse = T("O₂ refuses to release", 26, YELLOW).move_to(LEFT * 3.9 + DOWN * 1.7)
        self.play(FadeIn(refuse, shift=UP * 0.1), run_time=0.6)
        l_c = T("with CO", 26, RED).next_to(ax.c2p(60, 0.5), UP, buff=0.1)
        d_n = Dot(ax.c2p(26, 0.5), color=BLUE, radius=0.09)
        d_c = Dot(ax.c2p(13, 0.25), color=RED, radius=0.09)
        drop_n = DashedLine(ax.c2p(26, 0.5), ax.c2p(26, 0), color=BLUE, stroke_width=3)
        drop_c = DashedLine(ax.c2p(13, 0.25), ax.c2p(13, 0), color=RED, stroke_width=3)
        lshift = Arrow(ax.c2p(26, 0.1), ax.c2p(13, 0.1), color=RED, buff=0, stroke_width=5,
                       max_tip_length_to_length_ratio=0.6)
        shift_l = T("left shift", 28, RED).next_to(ax.c2p(30, 0.1), RIGHT, buff=0.15)
        cap = DoubleArrow(ax.c2p(90, 0.5), ax.c2p(90, 1.0), color=GOLD, buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.25)
        cap_lab = T("capacity ↓", 26, GOLD).move_to(ax.c2p(72, 0.74))
        # "...a left-shifted curve"
        self.at_s(12.6)
        self.play(Create(cohb), FadeIn(l_c), run_time=1.2)
        self.play(FadeIn(d_n), FadeIn(d_c), Create(drop_n), Create(drop_c), GrowArrow(lshift), FadeIn(shift_l),
                  run_time=1.0)
        # "...and slashed carrying capacity at once"
        self.at_s(14.8)
        self.play(GrowArrow(cap), FadeIn(cap_lab), run_time=0.9)
        # sentence 3: cherry-red blood; pulse oximeter fooled; tissues suffocate
        self.at_s(17.5)
        everything = VGroup(grp, t_lab, refuse, ax, deco, normal, cohb, l_n, l_c, shift_l, lshift, cap, cap_lab, d_n, d_c, drop_n, drop_c)
        self.play(FadeOut(everything), run_time=self.beat(0.03))
        vial = RoundedRectangle(corner_radius=0.3, width=1.5, height=2.8, stroke_color=RED, stroke_width=4,
                                fill_color=RED, fill_opacity=0.35)
        vial.move_to(LEFT * 4.4 + UP * 0.2)
        v_lab = T("cherry-red blood", 28, RED).next_to(vial, DOWN, buff=0.3)
        self.play(FadeIn(vial, scale=0.9), FadeIn(v_lab), run_time=self.beat(0.05))
        ox_body = RoundedRectangle(corner_radius=0.25, width=2.7, height=1.7, stroke_color=GREY, stroke_width=4,
                                   fill_color=GREY, fill_opacity=0.12)
        ox_body.move_to(UP * 0.2)
        scr = VGroup(T("SpO₂", 32, TEXT), M("98%", 36, TEXT)).arrange(RIGHT, buff=0.25).move_to(ox_body)
        ox_lab = T("pulse oximeter", 28, GREY).next_to(ox_body, DOWN, buff=0.3)
        self.play(FadeIn(ox_body), FadeIn(scr), FadeIn(ox_lab), run_time=self.beat(0.05))
        cant = T("can't tell CO-Hb from O₂-Hb", 26, GOLD).next_to(ox_lab, DOWN, buff=0.3)
        self.play(FadeIn(cant, shift=UP * 0.1), run_time=self.beat(0.04))
        self.at_s(24.9)
        # tissue O2 bar falls
        frame = Rectangle(width=1.0, height=2.8, color=YELLOW, stroke_width=3).move_to(RIGHT * 4.4 + UP * 0.2)
        fill_t = ValueTracker(1.0)

        def fillbar():
            h = 2.8 * fill_t.get_value()
            r = Rectangle(width=1.0, height=max(h, 0.01), stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
            r.move_to(frame.get_bottom() + UP * (max(h, 0.01) / 2))
            return r

        bar = always_redraw(fillbar)
        t_lab2 = T("tissue O₂ supply", 28, YELLOW).next_to(frame, DOWN, buff=0.3)
        self.play(FadeIn(frame), FadeIn(bar), FadeIn(t_lab2), run_time=self.beat(0.03))
        self.play(fill_t.animate.set_value(0.2), run_time=self.beat(0.06), rate_func=smooth)
        # sentence 4: flood with O2 and compete CO off
        self.at_s(27.8)
        bar.clear_updaters()
        H2 = hb(0.5, GREEN).move_to(DOWN * 0.2)
        c2 = co().move_to(socket_of(H2[1]) + np.array([-0.05, 0, 0]))
        self.play(*[FadeOut(m) for m in (vial, v_lab, ox_body, scr, ox_lab, cant, frame, bar, t_lab2)], run_time=0.5)
        self.play(FadeIn(H2), FadeIn(c2), run_time=0.5)
        flood = VGroup(*[o2(0.28).move_to(LEFT * 6.0 + UP * y) for y in (1.8, 0.6, -0.6, -1.8)])
        fl_lab = T("flood with oxygen", 32, YELLOW).move_to(UP * 2.9)
        self.play(FadeIn(fl_lab), FadeIn(flood), run_time=0.5)
        docks = [socket_of(H2[k]) + np.array([-0.05, 0, 0]) for k in (0, 2, 3, 1)]
        self.play(c2.animate.shift(RIGHT * 2.4 + UP * 1.0).set_opacity(0.0),
                  *[o.animate.move_to(p) for o, p in zip(flood, docks)], run_time=1.5, rate_func=smooth)
        self.remove(c2)
        comp = T("O₂ competes the CO back off", 30, YELLOW).move_to(DOWN * 3.1)
        self.play(FadeIn(comp, shift=UP * 0.1), run_time=0.6)
        self.finish()
