"""Section film: Pulses Work Where Steady Signals Fail (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = GnRH (and the GnRH agonist), the signal
  GREEN  = gonadotropin output
  RED    = off switches (the general possibility), and nothing else
  BLUE   = the receptor and the signalling chain
  TEAL   = the measurement
  GREY   = lesion, "no / not", axes, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

NOTE_Y = -3.5


def note(text="idealised, not to scale"):
    return T(text, 22, GREY).move_to([0, NOTE_Y, 0])


def spikes(x0, y, n, gap, h=1.0, w=0.14, color=YELLOW):
    return VGroup(*[Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.95)
                    .move_to([x0 + i * gap, y + h / 2, 0]) for i in range(n)])


class S00Title(TitleCard):
    LESSON = "Turning the Signal Off: Arrestins, RGS Proteins and Phosphodiesterases"
    TITLE = "Pulses Work Where Steady Signals Fail"


# ---------------------------------------------------------------------------------------------
class S01Monkeys(SpokenScene):
    def construct(self):
        n = note()
        # opening puzzle: steady vs pulses
        steady = Rectangle(width=4.2, height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([-4.3, 0.2, 0])
        ls = T("steady", 30).move_to([-4.3, 1.2, 0])
        pul = spikes(1.9, -0.3, 6, 0.8, h=1.0)
        lp = T("pulsing", 30).move_to([3.9, 1.2, 0])
        q = T("?", 90, GREY).move_to([-0.15, 0.2, 0])
        self.play(FadeIn(steady), FadeIn(ls), FadeIn(pul), FadeIn(lp), FadeIn(q), FadeIn(n), run_time=0.8)
        self.at("peptide")
        chips = VGroup(chip("hypothalamus", BLUE, 28), chip("pituitary", BLUE, 28),
                       chip("ovaries and testes", BLUE, 28)).arrange(RIGHT, buff=1.7).move_to([0, 0.0, 0])
        hyp, pit, ov = chips
        a1 = Arrow(hyp.get_right(), pit.get_left(), buff=0.08, color=YELLOW, stroke_width=6)
        l1 = T("GnRH", 26, YELLOW).next_to(a1, UP, buff=0.5)
        self.play(FadeOut(steady), FadeOut(ls), FadeOut(pul), FadeOut(lp), FadeOut(q), FadeIn(hyp), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.5)
        self.at("pituitary")
        self.play(FadeIn(pit), run_time=0.4)
        self.at("gonadotropins")
        a2 = Arrow(pit.get_right(), ov.get_left(), buff=0.08, color=GREEN, stroke_width=6)
        l2 = T("gonadotropins", 26, GREEN).next_to(a2, UP, buff=0.5)
        l2.set_x(a2.get_center()[0])
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.5)
        self.at("ovaries and testes")
        self.play(FadeIn(ov), run_time=0.4)
        self.at("and colleagues")
        who = T("Belchetz and colleagues, 1978", 32, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(who, shift=DOWN * 0.15), run_time=0.4)
        self.at("rhesus monkeys")
        mk = T("rhesus monkeys", 28).move_to([0, 2.3, 0])
        self.play(FadeIn(mk), run_time=0.4)
        self.at("lesions")
        ring = SurroundingRectangle(hyp, color=GREY, buff=0.12, stroke_width=3)
        ll = T("lesion", 26, GREY).next_to(hyp, DOWN, buff=0.35)
        d1 = DashedLine(hyp.get_right(), pit.get_left(), color=GREY, stroke_width=5, dash_length=0.18)
        self.play(Create(ring), FadeIn(ll), FadeOut(a1), FadeOut(l1), FadeIn(d1), run_time=0.5)
        self.at("abolished")
        d2 = DashedLine(pit.get_right(), ov.get_left(), color=GREY, stroke_width=5, dash_length=0.18)
        nr = T("no gonadotropin release", 26, GREY).move_to([d2.get_center()[0] + 0.4, -1.0, 0])
        self.play(FadeOut(a2), FadeOut(l2), FadeIn(d2), FadeIn(nr), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pulses(SpokenScene):
    def panel(self, y, label, kind):
        lab = T(label, 28, YELLOW).move_to([-5.2, y + 0.5, 0])
        axis = Line([-3.5, y - 0.2, 0], [1.9, y - 0.2, 0], color=GREY, stroke_width=3)
        if kind == "flat":
            sig = Rectangle(width=5.2, height=0.45, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95
                            ).move_to([-0.8, y - 0.2 + 0.225, 0])
        else:
            sig = spikes(-3.0, y - 0.2, 5, 1.0, h=1.0)
        return lab, axis, sig

    def construct(self):
        n = note()
        hd = T("GnRH given", 30, YELLOW, weight=BOLD).move_to([-1.0, 3.1, 0])
        hr = T("gonadotropin secretion", 28, GREEN, weight=BOLD).move_to([4.5, 3.1, 0])
        self.add(n)
        self.play(FadeIn(hd), FadeIn(hr), FadeIn(n), run_time=0.5)
        la, ax_a, sa = self.panel(1.3, "continuous", "flat")
        lb, ax_b, sb = self.panel(-1.6, "once an hour", "spikes")
        self.play(FadeIn(ax_a), FadeIn(ax_b), run_time=0.4)
        self.at("continuously")
        self.play(FadeIn(la), GrowFromEdge(sa, LEFT), run_time=0.7)
        self.at("once an hour")
        self.play(FadeIn(lb), LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in sb], lag_ratio=0.25), run_time=1.2)
        br = BraceBetweenPoints([sb[0].get_x(), -2.0, 0], [sb[1].get_x(), -2.0, 0], direction=DOWN, color=GREY)
        bl = T("1 hour", 22, GREY).next_to(br, DOWN, buff=0.08)
        self.play(FadeIn(br), FadeIn(bl), run_time=0.4)
        self.at("hourly pulses")
        rb = chip("restored", GREEN, 30).move_to([4.5, -1.2, 0])
        self.play(FadeIn(rb, shift=LEFT * 0.2), run_time=0.5)
        self.at("constant infusion")
        ra = chip("not restored", GREY, 30).move_to([4.5, 1.7, 0])
        self.play(Indicate(sa, color=YELLOW, scale_factor=1.05), FadeIn(ra, shift=LEFT * 0.2), run_time=0.6)
        self.at("clinics use")
        self.play(*[FadeOut(m) for m in (hd, hr, la, lb, ax_a, ax_b, sa, sb, br, bl, rb, ra)], run_time=0.5)
        ch = T("clinics use the same effect on purpose", 32, TEXT, weight=BOLD).move_to([0, 2.4, 0])
        self.play(FadeIn(ch, shift=DOWN * 0.15), run_time=0.4)
        self.at("keeping a")
        ag = chip("GnRH agonist,\nkept present", YELLOW, 32).move_to([-3.9, 0.3, 0])
        bar = Rectangle(width=4.2, height=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([-3.9, -1.3, 0])
        self.play(FadeIn(ag), GrowFromEdge(bar, LEFT), run_time=0.6)
        self.at("shut gonadotropin")
        arr = Arrow([-0.9, 0.3, 0], [0.7, 0.3, 0], buff=0, color=TEXT, stroke_width=6)
        out = chip("gonadotropin output\nshut down", GREY, 32).move_to([3.8, 0.3, 0])
        self.play(GrowArrow(arr), FadeIn(out, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def trace(kind, x0, w, y0, hgt, n_pulse=4):
    """Idealised off-switch level: rises while the signal is on, falls in the gaps."""
    pts = []
    L = 0.0
    steps = 240
    for i in range(steps + 1):
        t = i / steps
        if kind == "flat":
            on = True
        else:
            on = (int(t * n_pulse * 2) % 2 == 0) and t < 1.0
        dt = 1.0 / steps
        if on:
            L += (1 - L) * 2.6 * dt * (3 if kind != "flat" else 1.6)
        else:
            L -= L * 9 * dt
        pts.append([x0 + t * w, y0 + L * hgt, 0])
    m = VMobject(color=RED, stroke_width=6)
    m.set_points_as_corners(pts)
    return m


class S03Gap(SpokenScene):
    def construct(self):
        n = note("one general possibility, idealised")
        cx = [-3.4, 3.4]
        W = 5.4
        hdc = T("constant signal", 30, TEXT, weight=BOLD).move_to([cx[0], 3.1, 0])
        hdp = T("pulses", 30, TEXT, weight=BOLD).move_to([cx[1], 3.1, 0])
        sc = Rectangle(width=W, height=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([cx[0], 2.2, 0])
        sp = VGroup(*[Rectangle(width=W / 8, height=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95)
                      .move_to([cx[1] - W / 2 + W / 16 + i * W / 4, 2.2, 0]) for i in range(4)])
        tl = T("signal", 22, GREY).move_to([-6.3, 2.2, 0]) if False else None
        ax = [Line([c - W / 2, -2.2, 0], [c + W / 2, -2.2, 0], color=GREY, stroke_width=3) for c in cx]
        Y0, H = -2.2, 3.5
        tc = trace("flat", cx[0] - W / 2, W, Y0, H)
        tp = trace("pulse", cx[1] - W / 2, W, Y0, H)
        lab = VGroup(*[T("off switches", 26, RED).move_to([c, -2.7, 0]) for c in cx])
        self.play(FadeIn(hdc), FadeIn(hdp), FadeIn(sc), FadeIn(sp), *[FadeIn(a) for a in ax], FadeIn(n), run_time=0.7)
        self.at("off switches build up")
        self.play(Create(tc, run_time=2.4, rate_func=linear), Create(tp, run_time=2.4, rate_func=linear),
                  FadeIn(lab, run_time=0.6))
        self.at("need a gap")
        gaps = VGroup(*[Rectangle(width=W / 8, height=0.4, stroke_width=3, stroke_color=TEXT, fill_opacity=0)
                        .move_to([cx[1] - W / 2 + 3 * W / 16 + i * W / 4, 2.2, 0]) for i in range(3)])
        gl = T("gap", 26, TEXT).move_to([cx[1], 1.45, 0])
        self.play(Create(gaps), FadeIn(gl), run_time=0.7)
        self.at("pulses give")
        self.play(Indicate(tp, color=RED, scale_factor=1.0), run_time=0.8)
        self.at("kinase mark")
        phaseA = VGroup(hdc, hdp, sc, sp, *ax, tc, tp, lab, gaps, gl)
        self.play(FadeOut(phaseA), FadeOut(n), run_time=0.5)
        kc = chip("kinase mark", BLUE, 28)
        ar = chip("arrestin", BLUE, 28)
        ex = T("cannot be the whole explanation here", 26, GREY)
        row = VGroup(kc, ar, ex).arrange(RIGHT, buff=0.4).move_to([0, 3.0, 0])
        self.play(FadeIn(row, shift=DOWN * 0.15), run_time=0.5)
        self.at("whole explanation")
        # membrane and receptor
        mem = RoundedRectangle(corner_radius=0.1, width=6.2, height=0.5, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.3).move_to([-3.2, 0.3, 0])
        rec = RoundedRectangle(corner_radius=0.14, width=0.5, height=3.0, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.35).move_to([-3.2, 0.3, 0])
        who = T("Willars and colleagues, 1999", 30, GOLD, weight=BOLD).move_to([3.0, 2.0, 0])
        rl = T("mammalian GnRH receptor", 26, BLUE).move_to([-3.2, -2.9, 0])
        self.play(FadeIn(mem), FadeIn(rec), FadeIn(rl), run_time=0.6)
        self.at("showed")
        self.play(FadeIn(who), run_time=0.4)
        self.at("terminal tail")
        end = rec.get_bottom()
        al = T("no C-terminal tail", 28, TEXT).move_to([end[0] + 3.3, end[1] - 0.7, 0])
        ar2 = Arrow(al.get_left() + LEFT * 0.1, [end[0] + 0.1, end[1] - 0.12, 0], buff=0.0, color=TEXT, stroke_width=5)
        self.play(GrowArrow(ar2), FadeIn(al), run_time=0.6)
        self.at("resists phosphorylation")
        c1 = chip("resists phosphorylation by agonist", BLUE, 26).move_to([3.0, 0.7, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.5)
        self.at("rapid desensitization")
        c2 = chip("resists rapid desensitization", BLUE, 26).move_to([3.0, -0.7, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Measure(SpokenScene):
    def ptr(self, c, text, color=TEXT, size=30, reach=1.0):
        R = c.get_right()
        a = Arrow(R + RIGHT * (reach + 0.1), R + RIGHT * 0.1, buff=0.0, color=color, stroke_width=5, tip_length=0.2)
        t = T(text, size, color).next_to(a, RIGHT, buff=0.2)
        return VGroup(a, t)

    def construct(self):
        n = note("idealised chain; downstream steps not specified")
        names = ["GnRH receptor", "second messenger", "downstream steps", "hormone release"]
        cols = [BLUE, BLUE, GREY, GREEN]
        ch = [chip(t, c, 30) for t, c in zip(names, cols)]
        X = -4.0
        ys = [2.7, 0.9, -0.9, -2.7]
        for c, y in zip(ch, ys):
            c.move_to([X, y, 0])
        arrows = [Arrow([X, ys[i] - 0.45, 0], [X, ys[i + 1] + 0.45, 0], buff=0.02, color=GREY, stroke_width=5,
                        tip_length=0.2, max_tip_length_to_length_ratio=0.9) for i in range(3)]
        self.play(*[FadeIn(c) for c in ch], *[FadeIn(a) for a in arrows], FadeIn(n), run_time=0.3)
        self.at("failure at the receptor")
        pa = T("failure at the receptor", 34, TEXT, weight=BOLD).move_to([2.6, 1.8, 0])
        self.play(FadeIn(pa, shift=DOWN * 0.1), run_time=0.5)
        self.at("fewer receptors")
        fa = self.ptr(ch[0], "fewer on the surface")
        self.play(FadeIn(fa), run_time=0.5)
        self.at("less second messenger")
        la = self.ptr(ch[1], "less made per dose")
        self.play(FadeIn(la), run_time=0.5)
        self.at("failure downstream")
        pb = T("failure downstream", 34, TEXT, weight=BOLD).move_to([2.4, -0.2, 0])
        self.play(FadeOut(pa), FadeOut(fa), FadeOut(la), FadeIn(pb), run_time=0.5)
        self.at("output normal")
        nm = self.ptr(ch[1], "normal", GREEN)
        self.play(FadeIn(nm), run_time=0.5)
        self.at("release falls")
        fl = self.ptr(ch[3], "falls", TEXT)
        self.play(FadeIn(fl), run_time=0.5)
        self.at("second messenger output")
        self.play(FadeOut(pb), FadeOut(nm), FadeOut(fl), run_time=0.4)
        pr = self.ptr(ch[1], "measure here", TEAL, 34, reach=1.6)
        pr[0].set_stroke(width=7)
        self.play(FadeIn(pr), Indicate(ch[1], color=TEAL), run_time=0.7)
        self.at("tell the two apart")
        tt = T("receptor or downstream?", 34, TEXT).move_to([3.0, 1.9, 0])
        self.play(FadeIn(tt, shift=UP * 0.1), run_time=0.5)
        self.at("answers only part")
        pw = T("published work answers only part of this", 26, GREY).move_to([2.9, -2.0, 0])
        pw2 = T("question", 26, GREY).next_to(pw, DOWN, buff=0.1)
        self.play(FadeIn(pw), FadeIn(pw2), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "Measure second messenger output to tell receptor from downstream failure."
