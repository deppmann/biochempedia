"""Oncogenes: gain acts alone, loss needs both  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the growth signal
  BLUE   = a normal Ras protein
  GOLD   = GTP (the badge Ras holds while it is on)
  TEAL   = the off-step: a GAP (neurofibromin) and the gene that makes it
  PURPLE = a normal gene copy (the DNA block)
  RED    = what is altered, lost or stuck: the changed gene copy, the altered Ras, a lost copy, "oncogene"
  GREEN  = on: the switch on, the cell divides
  GREY   = off / waiting / labels / a lost or empty slot

No molecular structures: proteins are chips, genes are blocks on a line, GTP is a badge, the
switch is a track with a knob.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


# ------------------------------------------------------------------ helpers
def toggle(on, pos=(0, 0), k=1.0, stuck=False):
    w, h = 3.0 * k, 1.4 * k
    col = GREEN if on else GREY
    track = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=RED if stuck else col,
                             stroke_width=5, fill_color=col, fill_opacity=0.3 if on else 0.15)
    x = (w / 2 - h / 2) if on else -(w / 2 - h / 2)
    knob = Circle(radius=h / 2 - 0.14 * k, stroke_width=0, fill_color=col if on else TEXT, fill_opacity=1)
    knob.move_to(track.get_center() + RIGHT * x)
    return VGroup(track, knob).move_to([pos[0], pos[1], 0])


def lamp(state, pos=(0, 0), size=30):
    """state: 'on' (cell divides), 'off' (cell waits), 'none' (not yet shown)."""
    if state == "on":
        c = Circle(radius=0.5, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.9)
        t = T("cell divides", size, GREEN)
    elif state == "off":
        c = Circle(radius=0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.18)
        t = T("cell waits", size, GREY)
    else:
        c = Circle(radius=0.5, stroke_color=GREY, stroke_width=3, fill_opacity=0)
        c = DashedVMobject(c, num_dashes=14).set_color(GREY)
        t = T("cell?", size, GREY)
    c2 = Circle(radius=0.5, stroke_width=0, fill_opacity=0)  # keeps the circle a fixed size
    g = VGroup(VGroup(c, c2), t).arrange(DOWN, buff=0.18)
    return g.move_to([pos[0], pos[1], 0])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def strike(m, color=RED, w=7):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=w)


def cross_at(p, r=0.3, color=RED, w=7):
    p = np.array(p, float)
    return VGroup(Line(p + [-r, -r, 0], p + [r, r, 0], color=color, stroke_width=w),
                  Line(p + [-r, r, 0], p + [r, -r, 0], color=color, stroke_width=w))


def gtp_badge(pos, size=26):
    c = chip("GTP", GOLD, size=size, pad=0.14, fill_opacity=0.9)
    c[1].set_color(BG)
    return c.move_to([pos[0], pos[1], 0])


def gene(label, color, pos, state="ok", w=2.6):
    """a gene copy: a block on a short DNA line. state: ok / altered / lost."""
    line = Line(LEFT * (w / 2 + 0.4), RIGHT * (w / 2 + 0.4), color=GREY, stroke_width=5)
    if state == "lost":
        blk = RoundedRectangle(corner_radius=0.08, width=w, height=0.62, stroke_color=GREY, stroke_width=3,
                               fill_opacity=0)
        blk = DashedVMobject(blk, num_dashes=30).set_color(GREY)
        txt = T("lost copy", 24, GREY)
        back = RoundedRectangle(corner_radius=0.08, width=w, height=0.62, stroke_width=0, fill_color=BG, fill_opacity=1)
        g = VGroup(line, back, blk, txt)
    else:
        col = RED if state == "altered" else color
        back = RoundedRectangle(corner_radius=0.08, width=w, height=0.62, stroke_width=0, fill_color=BG, fill_opacity=1)
        blk = RoundedRectangle(corner_radius=0.08, width=w, height=0.62, stroke_color=col, stroke_width=3,
                               fill_color=col, fill_opacity=0.45)
        txt = T(label, 24, TEXT)
        g = VGroup(line, back, blk, txt)
    return g.move_to([pos[0], pos[1], 0])


class Slot:
    """holds one mobject that is swapped by a cross-fade (never morphed: morphs of text glitch)."""
    def __init__(self, m):
        self.m = m

    def to(self, new):
        old, self.m = self.m, new
        return [FadeOut(old), FadeIn(new)]

    def __getattr__(self, k):
        return getattr(self.m, k)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Oncogenes: When the Switch Sticks"
    TITLE = "Gain Acts Alone, Loss Needs Both"


class S01Stuck(SpokenScene):
    def construct(self):
        SIG, TG, LP = (-4.8, 0.3), (0, 0.3), (5.0, 0.3)
        tg = toggle(False, TG, 2.0)
        lp = Slot(lamp("off", LP))
        sig_chip = chip("growth signal", YELLOW, 28).move_to([SIG[0], SIG[1], 0])
        a1 = arr([-3.5, 0.3, 0], [-1.85, 0.3, 0], YELLOW)
        a2 = arr([1.85, 0.3, 0], [3.75, 0.3, 0], GREY)
        self.at("divide only when")
        self.play(FadeIn(tg), FadeIn(lp.m), run_time=0.6)
        self.wait(0.2)
        self.at("signaling pathway")
        on_arrow = arr([-1.4, 1.85, 0], [1.4, 1.85, 0], GREEN)
        on_lbl = T("on-step", 28, GREEN).next_to(on_arrow, UP, buff=0.15)
        off_arrow = arr([1.4, -1.25, 0], [-1.4, -1.25, 0], TEAL)
        off_lbl = T("off-step", 28, TEAL).next_to(off_arrow, DOWN, buff=0.15)
        self.play(GrowArrow(on_arrow), FadeIn(on_lbl), GrowArrow(off_arrow), FadeIn(off_lbl), run_time=0.7)
        self.at("flips a switch")
        self.play(FadeIn(sig_chip), GrowArrow(a1), run_time=0.5)
        self.play(Transform(tg, toggle(True, TG, 2.0)), run_time=0.5)
        self.play(GrowArrow(a2), *lp.to(lamp("on", LP)), run_time=0.5)
        self.at("flips it back")
        self.play(FadeOut(sig_chip), FadeOut(a1), run_time=0.4)
        self.play(Indicate(off_arrow, color=TEAL, scale_factor=1.1), Indicate(off_lbl, color=TEAL), run_time=0.5)
        self.play(Transform(tg, toggle(False, TG, 2.0)), *lp.to(lamp("off", LP)), run_time=0.5)
        self.at("switch sticks")
        stuck = T("stuck on", 28, RED).move_to([-0.6, 0.3, 0])
        nosig = VGroup(DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.9, height=0.8), num_dashes=36).set_color(GREY),
                       T("no signal", 26, GREY)).move_to([SIG[0], SIG[1], 0])
        self.play(Transform(tg, toggle(True, TG, 2.0, stuck=True)), *lp.to(lamp("none", LP)),
                  FadeIn(nosig), FadeIn(stuck), run_time=0.6)
        self.at("divides on its own")
        self.play(*lp.to(lamp("on", LP)), run_time=0.4)
        self.wait(0.3)
        self.at("jam an")
        jam = chip("jam the on-step", RED, 26).move_to([0, 3.15, 0])
        self.play(FadeIn(jam), on_arrow.animate.set_color(RED), on_lbl.animate.set_color(RED), run_time=0.5)
        self.at("remove an")
        rem = chip("remove the off-step", RED, 26).move_to([0, -3.0, 0])
        self.play(FadeIn(rem), FadeIn(strike(off_arrow)), run_time=0.5)
        self.finish()


class _Ras(SpokenScene):
    RAS = (-2.8, 0.2)
    LAMP = (3.6, 0.2)
    GAPX = (3.6, 0.2)

    def ras(self, color=BLUE, text="Ras"):
        return chip(text, color, 40, pad=0.35).move_to([self.RAS[0], self.RAS[1], 0])

    def gtp(self):
        return gtp_badge([self.RAS[0], self.RAS[1] + 1.35, 0], 30)

    def lamp(self, st):
        return lamp(st, [self.LAMP[0], self.LAMP[1] - 0.2, 0])


class S02Jam(_Ras):
    def construct(self):
        ras = Slot(self.ras())
        gtp = self.gtp()
        arrow = arr([-1.0, 0.2, 0], [2.2, 0.2, 0], GREY)
        lp = Slot(self.lamp("none"))
        case = Slot(T("normal Ras", 34, BLUE).move_to([0, 3.0, 0]))
        gap = chip("GAP", TEAL, 36, pad=0.3)
        gap.move_to([self.RAS[0], self.RAS[1] - 1.7, 0]).shift(RIGHT * 5.2)
        step = chip("jam the on-step", RED, 28).move_to([4.2, 3.1, 0])
        self.play(FadeIn(step), run_time=0.5)
        self.at("Ras is on")
        self.play(FadeIn(case.m), FadeIn(ras.m), FadeIn(gtp, shift=DOWN * 0.3), FadeIn(lp.m), run_time=0.6)
        self.play(FadeIn(arrow), *lp.to(self.lamp("on")), run_time=0.4)
        self.at("helper called")
        self.play(FadeIn(gap, shift=LEFT * 0.3), run_time=0.4)
        gap_goal = [self.RAS[0], self.RAS[1] - 2.2, 0]
        up = arr([self.RAS[0], gap_goal[1] + 0.55, 0], [self.RAS[0], self.RAS[1] - 0.5, 0], TEAL)
        self.play(gap.animate.move_to(gap_goal), run_time=0.7)
        self.play(GrowArrow(up), run_time=0.3)
        self.at("break down")
        self.play(gtp.animate.shift(UP * 0.6).set_opacity(0), run_time=0.6)
        self.at("switch turns off")
        self.play(*lp.to(self.lamp("off")), run_time=0.5)
        self.at("changed amino acid")
        # reset to a neutral state for the new case
        case2 = T("Ras G12V", 34, RED).move_to(case.m)
        ras2 = self.ras(RED, "Ras G12V")
        gtp2 = self.gtp()
        self.play(*case.to(case2), *ras.to(ras2), gap.animate.shift(RIGHT * 5.2), FadeOut(up),
                  FadeIn(gtp2, shift=DOWN * 0.3), *lp.to(self.lamp("none")), run_time=0.8)
        self.wait(0.2)
        self.at("stops this")
        up2 = arr([self.RAS[0], gap_goal[1] + 0.55, 0], [self.RAS[0], self.RAS[1] - 0.5, 0], TEAL)
        self.play(gap.animate.move_to(gap_goal), GrowArrow(up2), run_time=0.7)
        self.at("cannot break down")
        x = cross_at([self.RAS[0], self.RAS[1] - 1.2, 0], 0.3)
        self.play(FadeIn(x), Indicate(gtp2, color=GOLD, scale_factor=1.15), run_time=0.5)
        self.at("even with")
        self.play(*lp.to(self.lamp("on")), run_time=0.4)
        self.at("oncogene")
        onc = chip("oncogene", RED, 30).move_to([self.RAS[0], 2.75, 0])
        self.play(FadeIn(onc, shift=DOWN * 0.2), run_time=0.5)
        self.finish()


class S03Remove(_Ras):
    def construct(self):
        ras = Slot(self.ras())
        gtp = self.gtp()
        arrow = arr([-1.0, 0.2, 0], [2.2, 0.2, 0], GREY)
        lp = Slot(self.lamp("none"))
        case = Slot(T("normal Ras", 34, BLUE).move_to([0, 3.0, 0]))
        step = chip("remove the off-step", RED, 28).move_to([4.2, 3.1, 0])
        self.play(FadeIn(step), run_time=0.5)
        self.play(FadeIn(ras.m), FadeIn(gtp), FadeIn(arrow), FadeIn(lp.m), run_time=0.6)
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=3.8, height=0.9), num_dashes=40).set_color(GREY)
        slot.move_to([self.RAS[0], self.RAS[1] - 2.2, 0])
        gap = chip("neurofibromin", TEAL, 30, pad=0.25).move_to(slot)
        self.at("Neurofibromin is")
        self.play(FadeIn(gap, shift=UP * 0.3), run_time=0.5)
        gl = T("a GAP for Ras", 26, TEAL).next_to(gap, DOWN, buff=0.25)
        self.play(FadeIn(gl), run_time=0.4)
        self.at("It is the")
        self.play(Indicate(gap, color=TEAL, scale_factor=1.1), run_time=0.5)
        self.at("Lose neurofibromin")
        sk = strike(gap)
        self.play(FadeIn(sk), run_time=0.3)
        self.play(FadeOut(gap), FadeOut(gl), FadeOut(sk), FadeIn(slot), run_time=0.6)
        self.at("not cleared")
        self.play(Indicate(gtp, color=GOLD, scale_factor=1.15), *lp.to(self.lamp("on")), run_time=0.6)
        self.at("jammed here")
        self.play(FadeIn(case.m), run_time=0.4)
        self.at("is missing")
        miss = T("off-step missing", 28, RED).next_to(slot, DOWN, buff=0.25)
        self.play(Indicate(slot, color=RED, scale_factor=1.08), FadeIn(miss), run_time=0.5)
        self.at("suppressor")
        ts = chip("tumour suppressor", RED, 30).move_to([self.LAMP[0] - 0.4, -2.2, 0])
        self.play(FadeIn(ts, shift=UP * 0.2), run_time=0.5)
        self.finish()


class S04Gain(SpokenScene):
    def construct(self):
        LX, RX = -3.4, 3.4
        Y_G, Y_P, Y_L = 2.4, 0.2, -2.5
        g1 = Slot(gene("Ras gene", PURPLE, [LX, Y_G, 0]))
        g2 = Slot(gene("Ras gene", PURPLE, [RX, Y_G, 0]))
        self.at("count the copies")
        self.play(FadeIn(g1.m), FadeIn(g2.m), run_time=0.6)
        self.at("one from each parent")
        p1 = T("from one parent", 26, GREY).next_to(g1.m, UP, buff=0.3)
        p2 = T("from the other parent", 26, GREY).next_to(g2.m, UP, buff=0.3)
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.5)
        self.at("one copy of the")
        self.play(*g1.to(gene("changed Ras gene", PURPLE, [LX, Y_G, 0], "altered", w=3.3)), run_time=0.6)
        self.at("altered protein")
        alt = chip("altered Ras", RED, 32).move_to([LX, Y_P, 0])
        d1 = arr([LX, Y_G - 0.5, 0], [LX, Y_P + 0.6, 0], RED)
        self.play(GrowArrow(d1), FadeIn(alt), run_time=0.6)
        lp = Slot(lamp("none", [0, Y_L, 0]))
        sig = arr([LX + 0.3, Y_P - 0.6, 0], [-0.9, Y_L + 0.3, 0], RED)
        self.at("without being told")
        told = T("no signal needed", 26, YELLOW).move_to([-3.4, -1.55, 0]).shift(LEFT * 0.5)
        self.play(GrowArrow(sig), FadeIn(lp.m), FadeIn(told), run_time=0.6)
        self.at("normal protein")
        norm = chip("normal Ras", BLUE, 32).move_to([RX, Y_P, 0])
        d2 = arr([RX, Y_G - 0.5, 0], [RX, Y_P + 0.6, 0], BLUE)
        self.play(GrowArrow(d2), FadeIn(norm), run_time=0.6)
        self.at("cannot stop it")
        inh = Line([RX - 1.3, Y_P, 0], [LX + 1.3, Y_P, 0], color=RED, stroke_width=5)
        bar = Line([LX + 1.3, Y_P - 0.25, 0], [LX + 1.3, Y_P + 0.25, 0], color=RED, stroke_width=6)
        mid = (inh.get_center())
        self.play(Create(inh), FadeIn(bar), run_time=0.5)
        x = cross_at(mid, 0.28)
        self.play(FadeIn(x), run_time=0.3)
        self.at("So the cell divides")
        self.play(*lp.to(lamp("on", [0, Y_L, 0])), run_time=0.4)
        self.at("gain of function")
        gof = chip("gain of function", GREEN, 28).move_to([-4.0, Y_L, 0])
        self.play(FadeIn(gof, shift=UP * 0.2), run_time=0.4)
        self.at("it is dominant")
        dom = chip("dominant", GREEN, 28).move_to([4.0, Y_L, 0])
        self.play(FadeIn(dom, shift=UP * 0.2), run_time=0.4)
        self.at("even when")
        self.play(Indicate(norm, color=BLUE, scale_factor=1.1), run_time=0.5)
        self.finish()


class S05Loss(SpokenScene):
    def construct(self):
        LX, RX = -3.4, 3.4
        Y_G, Y_P, Y_L = 2.4, 0.2, -2.4
        g1 = Slot(gene("GAP gene", TEAL, [LX, Y_G, 0]))
        g2 = Slot(gene("GAP gene", TEAL, [RX, Y_G, 0]))
        c1 = chip("GAP", TEAL, 32).move_to([LX, Y_P, 0])
        c2 = chip("GAP", TEAL, 32).move_to([RX, Y_P, 0])
        d1 = arr([LX, Y_G - 0.5, 0], [LX, Y_P + 0.6, 0], TEAL)
        d2 = arr([RX, Y_G - 0.5, 0], [RX, Y_P + 0.6, 0], TEAL)
        lp = Slot(lamp("off", [0, Y_L, 0]))
        case = Slot(T("both copies present", 32, GREY).move_to([0, 3.3, 0]))
        self.at("is different")
        self.play(FadeIn(g1.m), FadeIn(g2.m), run_time=0.5)
        self.play(GrowArrow(d1), GrowArrow(d2), FadeIn(c1), FadeIn(c2), FadeIn(case.m), FadeIn(lp.m), run_time=0.7)
        self.at("One good copy")
        self.play(Indicate(c2, color=TEAL, scale_factor=1.12), run_time=0.5)
        self.at("Lose one copy")
        case2 = T("one copy lost", 32, RED).move_to(case.m)
        hit1 = T("hit 1", 28, RED).next_to(g1.m, UP, buff=0.3)
        self.play(*case.to(case2), *g1.to(gene("GAP gene", TEAL, [LX, Y_G, 0], "lost")),
                  FadeOut(c1), FadeOut(d1), *lp.to(lamp("none", [0, Y_L, 0])), run_time=0.7)
        self.at("still works")
        self.play(*lp.to(lamp("off", [0, Y_L, 0])), Indicate(c2, color=TEAL, scale_factor=1.1), run_time=0.5)
        self.at("Both copies must go")
        case3 = T("both copies lost", 32, RED).move_to(case.m)
        self.play(*case.to(case3), *g2.to(gene("GAP gene", TEAL, [RX, Y_G, 0], "lost")),
                  FadeOut(c2), FadeOut(d2), *lp.to(lamp("none", [0, Y_L, 0])), run_time=0.7)
        self.at("before the")
        self.play(*lp.to(lamp("on", [0, Y_L, 0])), run_time=0.5)
        self.at("takes two hits")
        h1 = T("hit 1", 30, RED).next_to(g1.m, UP, buff=0.3)
        h2 = T("hit 2", 30, RED).next_to(g2.m, UP, buff=0.3)
        self.play(FadeIn(h1, shift=DOWN * 0.2), run_time=0.4)
        self.play(FadeIn(h2, shift=DOWN * 0.2), run_time=0.4)
        self.at("two copies of one gene")
        self.play(Indicate(g1.m, color=RED, scale_factor=1.06), Indicate(g2.m, color=RED, scale_factor=1.06), run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    def pair(self, states, pos, labels=None):
        """two small copy blocks; state: ok / altered / lost"""
        out = VGroup()
        for i, s in enumerate(states):
            col = {"ok": PURPLE, "altered": RED, "lost": GREY}[s]
            if s == "lost":
                b = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=0.95, height=0.6), num_dashes=24).set_color(GREY)
                b = VGroup(b, cross_at([0, 0, 0], 0.22, w=5))
            else:
                b = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.6, stroke_color=col, stroke_width=3,
                                     fill_color=col, fill_opacity=0.5)
            out.add(b)
        out.arrange(RIGHT, buff=0.25).move_to([pos[0], pos[1], 0])
        return out

    def res(self, state, pos):
        col, txt = (GREEN, "cell divides") if state == "on" else (GREY, "cell waits")
        c = Circle(radius=0.32, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.9 if state == "on" else 0.18)
        return VGroup(c, T(txt, 30, col)).arrange(RIGHT, buff=0.3).move_to([pos[0], pos[1], 0])

    def construct(self):
        R1, R2, R3 = 1.75, 0.0, -1.5
        PX, AX, RX = 0.1, 2.35, 4.6
        def row(states, y, cap, state):
            p = self.pair(states, [PX, y])
            c = T(cap, 24, GREY).next_to(p, DOWN, buff=0.12)
            a = arr([AX - 0.6, y, 0], [AX + 0.6, y, 0], GREY)
            r = self.res(state, [RX, y])
            return p, c, a, r
        lab1 = T("jammed on-step", 32, RED).move_to([-4.3, R1, 0])
        lab2 = T("lost off-step", 32, RED).move_to([-4.3, (R2 + R3) / 2, 0])
        hd = T("copies of the gene", 26, GREY).move_to([PX, 2.95, 0])
        self.play(FadeIn(hd), run_time=0.4)
        self.at("A jammed")
        p, c, a, r = row(["altered", "ok"], R1, "one copy altered", "on")
        self.play(FadeIn(lab1, shift=RIGHT * 0.2), FadeIn(p), FadeIn(c), run_time=0.5)
        self.at("one copy is altered")
        self.play(GrowArrow(a), FadeIn(r), run_time=0.5)
        self.at("A lost")
        p2, c2, a2, r2 = row(["lost", "ok"], R2, "one copy lost", "off")
        self.play(FadeIn(lab2, shift=RIGHT * 0.2), FadeIn(p2), FadeIn(c2), run_time=0.5)
        self.at("usually needs")
        self.play(GrowArrow(a2), FadeIn(r2), run_time=0.5)
        self.at("both copies gone")
        p3, c3, a3, r3 = row(["lost", "lost"], R3, "both copies lost", "on")
        self.play(FadeIn(p3), FadeIn(c3), run_time=0.5)
        self.play(GrowArrow(a3), FadeIn(r3), run_time=0.4)
        self.at("Gain acts alone")
        g = T("Gain acts alone.", 44, GREEN, font=TITLE_FONT).move_to([-3.2, -3.0, 0])
        self.play(FadeIn(g, shift=UP * 0.2), run_time=0.5)
        self.at("Loss needs both")
        l = T("Loss needs both.", 44, RED, font=TITLE_FONT).move_to([3.2, -3.0, 0])
        self.play(FadeIn(l, shift=UP * 0.2), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Gain acts alone. Loss needs both."
