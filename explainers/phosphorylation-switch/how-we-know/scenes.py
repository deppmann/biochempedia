"""Section film: How a Phosphate Was Found (phosphorylation-switch, "How we know").

COLOR MAP (one color per concept, whole film)
  BLUE   = glycogen phosphorylase (both chains, forms a and b)
  GREEN  = ACTIVE lamp
  GREY   = inactive lamp, labels, outlines
  YELLOW = AMP
  ORANGE = ATP
  TEAL   = calcium
  PURPLE = the converting enzyme (later shown to act)
  RED    = phosphatase, crossed-out assumption
  GOLD   = a phosphate (P badge)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B48EE0"
ORANGE = "#F29B4B"


def pbadge(size=0.24):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def lamp(on, scale=1.0):
    return chip("ACTIVE", GREEN, 26) if on else chip("inactive", GREY, 26)


def enz(name, pos, k=1.0):
    """Two chains side by side; returns VGroup(chains, label) with .c1 .c2 .lbl."""
    c1 = RoundedRectangle(corner_radius=0.3, width=1.5 * k, height=2.2 * k, stroke_color=BLUE, stroke_width=4,
                          fill_color=BLUE, fill_opacity=0.25)
    c2 = c1.copy()
    chains = VGroup(c1, c2).arrange(RIGHT, buff=0.15 * k).move_to(pos)
    lbl = T(name, 26, BLUE).next_to(chains, DOWN, buff=0.2)
    g = VGroup(chains, lbl)
    g.c1, g.c2, g.chains, g.lbl = c1, c2, chains, lbl
    return g


class S00Title(TitleCard):
    LESSON = "Phosphorylation: Kinases and Phosphatases"
    TITLE = "How a Phosphate Was Found"


# ---------------------------------------------------------------------------------------------
class S01Forms(SpokenScene):
    def construct(self):
        head = T("1943 · St. Louis", 30, GREY).to_edge(UP, buff=0.45)
        self.at("In 1943")
        self.play(FadeIn(head), run_time=0.5)
        names = T("Carl Cori · Gerty Cori · Arda Green", 30, TEXT).next_to(head, DOWN, buff=0.2)
        self.at("Carl and")
        self.play(FadeIn(names, shift=UP * 0.1), run_time=0.6)
        base = enz("glycogen phosphorylase", [0, -0.3, 0], 1.3)
        self.at("crystallized")
        self.play(FadeIn(base, scale=0.9), run_time=0.7)
        self.at("two forms")
        ea = enz("phosphorylase a", [-3.0, -0.3, 0], 1.3)
        eb = enz("phosphorylase b", [2.6, -0.3, 0], 1.3)
        self.play(ReplacementTransform(base, ea), ReplacementTransform(base.copy(), eb), run_time=1.0)
        la = lamp(False).next_to(ea, UP, buff=0.25)
        lb = lamp(False).next_to(eb, UP, buff=0.25)
        self.play(FadeIn(la), FadeIn(lb), run_time=0.4)
        self.at("active alone")
        la2 = lamp(True).move_to(la)
        self.play(ReplacementTransform(la, la2), ea.chains.animate.set_fill(GREEN, 0.0).set_fill(BLUE, 0.4), run_time=0.6)
        self.at("only when")
        amp = chip("AMP", YELLOW, 26).move_to([5.4, -3.0, 0])
        self.play(FadeIn(amp), run_time=0.4)
        self.play(amp.animate.next_to(eb.chains, RIGHT, buff=0.05), run_time=0.8)
        lb2 = lamp(True).move_to(lb)
        self.play(ReplacementTransform(lb, lb2), eb.chains.animate.set_fill(BLUE, 0.4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Assumed(SpokenScene):
    def construct(self):
        head = T("The Coris' enzyme: a into b", 30, GREY).to_edge(UP, buff=0.45)
        ea = enz("phosphorylase a", [-3.9, 0.3, 0], 1.2)
        eb = enz("phosphorylase b", [3.9, 0.3, 0], 1.2)
        la = lamp(True).next_to(ea, UP, buff=0.25)
        lb = lamp(False).next_to(eb, UP, buff=0.25)
        for e in (ea,):
            e.chains.set_fill(BLUE, 0.4)
        self.add(head, ea, eb, la, lb)
        arrow = arr = Arrow([-1.6, 0.3, 0], [1.6, 0.3, 0], buff=0, color=GREY, stroke_width=6)
        conv = chip("enzyme", PURPLE, 28).move_to([0, 1.2, 0])
        self.at("also had an enzyme")
        self.play(GrowArrow(arrow), FadeIn(conv, shift=DOWN * 0.2), run_time=0.8)
        self.at("assumed")
        amp = chip("AMP", YELLOW, 26).next_to(ea.chains, RIGHT, buff=0.05)
        assume = T("their assumption: it clips off a bound AMP", 26, GREY).move_to([0, -2.4, 0])
        self.play(FadeIn(amp), FadeIn(assume), run_time=0.5)
        self.play(amp.animate.move_to([0, -0.5, 0]), run_time=0.7)
        self.play(amp.animate.move_to([0, -1.3, 0]).set_opacity(0.0), run_time=0.7)
        self.at("not so")
        cross = Cross(assume, stroke_color=RED, stroke_width=6).scale(1.0)
        self.play(Create(cross), assume.animate.set_color(RED), run_time=0.6)
        self.at("in fact a phosphatase")
        pho = chip("phosphatase", RED, 28).move_to(conv)
        self.play(ReplacementTransform(conv, pho), FadeOut(cross), FadeOut(assume), run_time=0.8)
        q = T("So what did separate a from b?", 32, YELLOW).move_to([0, -3.2, 0])
        self.at("what did separate")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Paper(SpokenScene):
    def construct(self):
        head = T("1955 · Seattle", 30, GREY).to_edge(UP, buff=0.45)
        names = T("Edmond Fischer · Edwin Krebs", 30, TEXT).next_to(head, DOWN, buff=0.2)
        self.at("In 1955")
        self.play(FadeIn(head), run_time=0.4)
        self.at("Edwin Krebs")
        self.play(FadeIn(names, shift=UP * 0.1), run_time=0.5)
        ext = chip("extract", GREY, 30).move_to([-5.3, 0.3, 0])
        goal = T("goal: phosphorylase a", 26, GREEN).move_to([4.6, 1.5, 0])
        flow = Arrow([-4.2, 0.3, 0], [3.4, 0.3, 0], buff=0, color=GREY, stroke_width=6)
        recipe = T("the Cori recipe", 26, GREY).move_to([-2.3, 0.85, 0])
        res = chip("b", BLUE, 48).move_to([4.7, 0.3, 0])
        self.at("recipe")
        self.play(FadeIn(ext), FadeIn(goal), GrowArrow(flow), FadeIn(recipe), run_time=0.8)
        self.at("kept getting")
        self.play(FadeIn(res, scale=0.8), run_time=0.5)
        # paper in the path
        paper = VGroup(Rectangle(width=0.18, height=1.5, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.35)
                       ).move_to([1.0, 0.3, 0])
        plbl = T("paper", 26, TEXT).next_to(paper, DOWN, buff=0.15)
        self.at("unless they filtered")
        self.play(FadeIn(paper, shift=DOWN * 0.2), FadeIn(plbl), run_time=0.6)
        resa = chip("a", GREEN, 48).move_to(res)
        self.play(ReplacementTransform(res, resa), run_time=0.6)
        self.at("leaching calcium")
        drops = VGroup(*[chip("Ca²⁺", TEAL, 24).move_to([0.0 + 1.0 * i, -1.4, 0]) for i in range(3)])
        dl = T("the paper leaches calcium", 24, TEAL).move_to([1.0, -2.2, 0])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in drops], lag_ratio=0.25), FadeIn(dl), run_time=0.9)
        self.at("left standing")
        self.play(FadeOut(VGroup(drops, dl, plbl)), run_time=0.4)
        stand = VGroup(chip("extract", GREY, 26), ).move_to([-2.0, -1.6, 0])
        atp = chip("ATP", ORANGE, 24).next_to(stand, RIGHT, buff=0.25)
        sl = T("left standing", 24, GREY).next_to(stand, DOWN, buff=0.2)
        self.play(FadeIn(stand), FadeIn(atp), FadeIn(sl), run_time=0.5)
        self.at("ran out")
        self.play(atp.animate.scale(0.3).set_opacity(0), run_time=0.8)
        out = T("ATP runs out", 24, ORANGE).next_to(sl, DOWN, buff=0.15)
        self.play(FadeIn(out), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Serine(SpokenScene):
    def construct(self):
        head = T("Over the next few years", 30, GREY).to_edge(UP, buff=0.45)
        eb = enz("phosphorylase b", [-0.4, -0.3, 0], 1.4)
        lb = lamp(False).next_to(eb, UP, buff=0.25)
        self.add(head, eb, lb)
        self.at("conversion of b to a")
        conv = chip("enzyme", PURPLE, 28).move_to([-5.2, 1.4, 0])
        atp = chip("ATP", ORANGE, 28).move_to([-5.2, 0.0, 0])
        atp2 = chip("ATP", ORANGE, 28).move_to([-5.2, -1.2, 0])
        self.play(FadeIn(conv), FadeIn(atp), FadeIn(atp2), run_time=0.6)
        self.at("one phosphate")
        p1, p2 = pbadge(), pbadge()
        p1.move_to(atp.get_right() + RIGHT * 0.35)
        p2.move_to(atp2.get_right() + RIGHT * 0.35)
        s1 = T("serine", 24, GREY).move_to(eb.c1.get_center() + UP * 0.2)
        s2 = T("serine", 24, GREY).move_to(eb.c2.get_center() + UP * 0.2)
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.4)
        self.at("one serine")
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.5)
        t1 = s1.get_center() + DOWN * 0.55
        t2 = s2.get_center() + DOWN * 0.55
        self.at("each chain")
        self.play(p1.animate.move_to(t1), p2.animate.move_to(t2), atp.animate.set_opacity(0.35), atp2.animate.set_opacity(0.35), run_time=1.0)
        la = lamp(True).move_to(lb)
        ea_lbl = T("phosphorylase a", 26, BLUE).move_to(eb.lbl)
        self.at("carries the phosphate")
        self.play(ReplacementTransform(lb, la), ReplacementTransform(eb.lbl, ea_lbl), run_time=0.7)
        lbl_p = T("phosphate on each chain", 24, GOLD).move_to([-0.4, -3.1, 0])
        self.play(FadeIn(lbl_p), run_time=0.4)
        self.at("added by one enzyme")
        self.play(FadeOut(lbl_p), run_time=0.3)
        fwd = T("added by\nan enzyme", 28, PURPLE).move_to([4.5, 0.9, 0])
        back = T("removed by\na phosphatase", 28, RED).move_to([4.5, -1.0, 0])
        self.play(FadeIn(fwd, shift=LEFT * 0.2), run_time=0.5)
        self.at("removed by another")
        self.play(FadeIn(back, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "A phosphate, added by one enzyme and removed by another."
