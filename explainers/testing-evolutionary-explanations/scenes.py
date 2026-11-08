"""Testing evolutionary explanations: survival is not yet evolution  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the population before the drought (and its mean)
  YELLOW = survivors that breed, and S, the selection differential
  GREEN  = offspring, and R, the response
  TEAL   = heritability, h squared
  RED    = the supposed later drought (S and R below zero)
  GREY   = axes, the birds that died, labels
All beak-depth numbers are the lesson's made-up worked example (mm).
"""
import numpy as np
from statistics import NormalDist
from bp_style import *  # noqa: F401,F403

POP, SURV, OFF, HER, LATER, DEAD = BLUE, YELLOW, GREEN, TEAL, RED, GREY

def X(mm):
    return (mm - 9.5) * 7.5 + 0.8

BASE = [1.3, -0.45, -2.1]
AXY = -2.9
N = 40
Z = [NormalDist().inv_cdf((i + 0.5) / N) for i in range(N)]
SIG = 0.40 / float(np.mean(Z[-6:]))
VALS = [9.40 + SIG * z for z in Z]          # mean 9.40; the top six average 9.80
NSURV = 6


def dot(x, y, color, r=0.12, op=0.9):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def stack(vals, base, color):
    cnt, out = {}, []
    for v in vals:
        b = round(v / 0.05)
        k = cnt.get(b, 0)
        cnt[b] = k + 1
        out.append(dot(X(b * 0.05), base + 0.13 + 0.25 * k, color))
    return out


def axis():
    line = Line([X(8.8), AXY, 0], [X(10.2), AXY, 0], color=GREY, stroke_width=3)
    g = VGroup(line)
    for mm in (9.0, 9.5, 10.0):
        g.add(Line([X(mm), AXY, 0], [X(mm), AXY - 0.12, 0], color=GREY, stroke_width=3))
        g.add(M(f"{mm:.1f}", 22, GREY).move_to([X(mm), AXY - 0.38, 0]))
    g.add(T("beak depth, mm", 22, GREY).move_to([-4.9, AXY - 0.38, 0]))
    return g


def rowlabel(text, color, i):
    t = T(text, 24, color)
    return t.move_to([-6.2 + t.width / 2, BASE[i] + 1.3, 0])


def marker(mm, i, color, label=None):
    ln = Line([X(mm), BASE[i] - 0.1, 0], [X(mm), BASE[i] + 0.95, 0], color=color, stroke_width=5)
    lb = M(label or f"{mm:.2f} mm", 22, color).move_to([X(mm), BASE[i] + 1.2, 0])
    return VGroup(ln, lb)


def guide():
    return DashedLine([X(9.40), BASE[0] + 1.0, 0], [X(9.40), AXY, 0], color=POP, stroke_width=3, dash_length=0.15).set_opacity(0.4)


def gap(a, b, i, color, text, right=False):
    y = BASE[i] + 0.8
    ar = Arrow([X(a), y, 0], [X(b), y, 0], buff=0, color=color, stroke_width=6, tip_length=0.2,
               max_tip_length_to_length_ratio=0.5)
    lb = M(text, 24, color)
    lb.move_to([(0.45 + lb.width / 2) if right else (-0.4 - lb.width / 2), y, 0])
    return VGroup(ar, lb)


def tag():
    return T("made-up numbers", 22, GREY).move_to([5.0, 3.2, 0])


def pretty(s):
    return s.replace("h2", "h²")


class W:
    """The shared stage: rows of dots, markers, arrows. Built once, reused by scenes 2 to 6."""
    def __init__(self):
        self.axis = axis()
        self.tag = tag()
        self.pop = VGroup(*stack(VALS, BASE[0], POP))
        self.l1 = rowlabel("before the drought", POP, 0)
        self.m1 = marker(9.40, 0, POP)
        self.guide = guide()
        self.surv_src = VGroup(*[self.pop[i] for i in range(N - NSURV, N)])
        self.surv = VGroup(*stack(VALS[-NSURV:], BASE[1], SURV))
        self.l2 = rowlabel("survivors that breed", SURV, 1)
        self.m2 = marker(9.80, 1, SURV)
        self.S = gap(9.40, 9.80, 1, SURV, "S = 0.40 mm")
        self.l3 = rowlabel("offspring, predicted", OFF, 2)
        self.m3 = marker(9.64, 2, OFF, "9.64 mm")
        self.R = gap(9.40, 9.64, 2, OFF, "R = 0.24 mm")


class S00Title(TitleCard):
    LESSON = "How to test an evolutionary explanation"
    TITLE = "Survival Is Not Yet Evolution"


# ---------------------------------------------------------------------------------------------
class S01Drought(SpokenScene):
    def construct(self):
        head = T("Daphne Major, Galápagos", 34, font=TITLE_FONT).to_edge(UP, buff=0.45)
        pts = []
        for i in range(N):
            r = 0.44 * np.sqrt(i + 0.5)
            a = i * 2.39996
            pts.append([-3.4 + r * np.cos(a), -0.15 + r * np.sin(a), 0])
        dots = VGroup(*[dot(p[0], p[1], POP, r=0.17, op=0.95) for p in pts])
        keep = [3, 11, 17, 24, 31, 38]
        lab = T("medium ground finches", 26, POP).next_to(dots, DOWN, buff=0.25)
        self.at("a drought hit")
        self.play(Write(head), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), FadeIn(lab), run_time=1.6)
        self.at("medium ground finches")
        note = T("about 85 percent died", 30, TEXT).move_to([3.4, 1.4, 0])
        dead = [dots[i] for i in range(N) if i not in keep]
        self.play(*[d.animate.set_fill(DEAD, 0.28) for d in dead], FadeIn(note), run_time=1.4)
        self.at("were not a random sample")
        sv = T("the survivors", 28, SURV).move_to([3.4, 0.55, 0])
        self.play(*[dots[i].animate.set_fill(SURV, 1).scale(1.25) for i in keep], FadeIn(sv), run_time=0.9)
        self.at("will their children be different")
        box = RoundedRectangle(corner_radius=0.2, width=4.4, height=1.7, stroke_color=OFF, stroke_width=3,
                               fill_opacity=0).move_to([3.4, -1.4, 0])
        box = DashedVMobject(box, num_dashes=40)
        q = T("their children?", 28, OFF).move_to([3.4, -1.4, 0])
        self.play(Create(box), FadeIn(q), run_time=0.9)
        self.at("Survival is only")
        half = T("survival: only half", 28, SURV).move_to([3.4, 0.55, 0])
        self.play(ReplacementTransform(sv, half), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Selection(SpokenScene):
    def construct(self):
        w = W()
        self.at("Here is a")
        self.play(FadeIn(w.axis), FadeIn(w.tag), FadeIn(w.l1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in w.pop], lag_ratio=0.04), run_time=1.6)
        self.at("mean beak depth")
        self.play(Create(w.m1[0]), FadeIn(w.m1[1]), FadeIn(w.guide), run_time=0.7)
        self.at("survive and breed")
        self.play(FadeIn(w.l2), *[d.animate.set_fill(SURV, 1) for d in w.surv_src], run_time=0.4)
        self.play(*[TransformFromCopy(a, b) for a, b in zip(w.surv_src, w.surv)], run_time=0.6)
        self.at("average")
        self.play(Create(w.m2[0]), FadeIn(w.m2[1]), run_time=0.7)
        self.at("Subtract")
        self.play(GrowArrow(w.S[0]), run_time=0.7)
        self.at("selection differential")
        self.play(FadeIn(w.S[1]), run_time=0.5)
        self.at("within one generation")
        self.play(Indicate(w.S, color=SURV, scale_factor=1.12), run_time=0.8)
        self.finish()


def static_world(scene, w, upto):
    """Put the end state of scene 2 (and optionally 3, 4) on screen without animation."""
    for p in (w.axis, w.tag, w.pop, w.l1, w.m1, w.guide, w.l2, w.surv, w.m2, w.S):
        scene.add(p)
    w.surv_src.set_fill(SURV, 1)
    if upto >= 3:
        scene.add(w.l3)


class S03Children(SpokenScene):
    def construct(self):
        w = W()
        static_world(self, w, 2)
        self.at("children are the next")
        q = T("not yet measured", 26, OFF).move_to([0.8, BASE[2] + 0.5, 0])
        self.play(FadeIn(w.l3), FadeIn(q), run_time=0.9)
        self.at("who lived")
        self.play(Indicate(w.surv, color=SURV, scale_factor=1.25), run_time=0.8)
        self.at("what those children look like")
        self.play(Indicate(q, color=OFF, scale_factor=1.15), run_time=0.8)
        self.at("heritability")
        h2 = chip("h²", HER, size=34).move_to([5.0, -1.45, 0])
        hl = T("heritability", 24, HER).next_to(h2, DOWN, buff=0.12)
        self.play(FadeIn(h2, scale=0.8), FadeIn(hl), run_time=0.7)
        self.at("resemble their parents")
        a1 = Arrow([X(9.8), BASE[1] - 0.2, 0], [X(9.8), BASE[2] + 0.6, 0], buff=0.05, color=HER, stroke_width=5,
                   tip_length=0.22)
        self.play(GrowArrow(a1), run_time=0.8)
        self.at("one population in one environment")
        cc = T("h² belongs to one population in one environment", 24, HER).move_to([-1.0, 3.15, 0])
        self.play(FadeIn(cc, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S04Breeder(SpokenScene):
    def construct(self):
        w = W()
        static_world(self, w, 3)
        self.at("equation joins")
        eq = M("R = h² × S", 36, TEXT).move_to([-1.0, 3.15, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.7)
        self.at("Assume")
        h2 = chip("h² = 0.60", HER, size=28).move_to([4.9, -1.45, 0])
        self.play(FadeIn(h2, scale=0.8), run_time=0.6)
        self.at("Then R is")
        eq2 = M("R = 0.60 × 0.40", 36, TEXT).move_to([-1.0, 3.15, 0])
        self.play(ReplacementTransform(eq, eq2), run_time=0.7)
        self.at("That is")
        eq3 = M("R = 0.60 × 0.40 = 0.24 mm", 36, OFF).move_to([-1.0, 3.15, 0])
        self.play(ReplacementTransform(eq2, eq3), GrowArrow(w.R[0]), FadeIn(w.R[1]), run_time=0.9)
        self.at("predicted offspring mean")
        self.play(Create(w.m3[0]), FadeIn(w.m3[1]), run_time=0.8)
        self.finish()


class S05Limits(SpokenScene):
    def construct(self):
        w = W()
        static_world(self, w, 3)
        for p in (w.R, w.m3):
            self.add(p)
        eq = M("R = 0.60 × 0.40 = 0.24 mm", 36, OFF).move_to([-1.0, 3.15, 0])
        h2 = chip("h² = 0.60", HER, size=28).move_to([4.9, -1.45, 0])
        self.add(eq, h2)
        self.at("heritability were zero")
        h0 = chip("h² = 0", HER, size=28).move_to([4.9, -1.45, 0])
        r0 = Arrow([X(9.40), BASE[2] + 0.45, 0], [X(9.40) + 0.01, BASE[2] + 0.45, 0], buff=0, color=OFF)
        m0 = marker(9.40, 2, OFF, "9.40 mm")
        eq0 = M("R = 0 × 0.40 = 0", 36, OFF).move_to([-1.0, 3.15, 0])
        self.play(ReplacementTransform(h2, h0), ReplacementTransform(eq, eq0),
                  FadeOut(w.R), Transform(w.m3, m0), run_time=1.2)
        self.at("would look like the population")
        self.play(Indicate(w.m3, color=OFF, scale_factor=1.08), Indicate(w.m1, color=POP, scale_factor=1.08), run_time=0.9)
        self.at("also flip")
        h6 = chip("h² = 0.60", HER, size=28).move_to([4.9, -1.45, 0])
        self.play(ReplacementTransform(h0, h6), FadeOut(eq0), FadeOut(w.m3), FadeOut(w.surv), FadeOut(w.m2),
                  FadeOut(w.S), run_time=0.9)
        for d in w.surv_src:
            d.set_fill(POP, 0.9)
        self.at("Suppose a later drought")
        l2b = rowlabel("a later drought", LATER, 1)
        m2 = marker(9.20, 1, LATER, "9.20 mm")
        self.play(ReplacementTransform(w.l2, l2b), Create(m2[0]), FadeIn(m2[1]), run_time=0.9)
        self.at("Then S is minus")
        S2 = gap(9.40, 9.20, 1, LATER, "S = -0.20 mm", right=True)
        self.play(GrowArrow(S2[0]), FadeIn(S2[1]), run_time=0.8)
        self.at("R is minus")
        eqr = M("R = 0.60 × (-0.20) = -0.12 mm", 34, LATER).move_to([-1.0, 3.15, 0])
        R2 = gap(9.40, 9.28, 2, LATER, "R = -0.12 mm", right=True)
        self.play(FadeIn(eqr), GrowArrow(R2[0]), FadeIn(R2[1]), run_time=0.9)
        self.at("predicted offspring mean is")
        m3 = marker(9.28, 2, LATER, "9.28 mm")
        self.play(Create(m3[0]), FadeIn(m3[1]), run_time=0.8)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        w = W()
        static_world(self, w, 3)
        for p in (w.R, w.m3):
            self.add(p)
        h2 = chip("h² = 0.60", HER, size=28).move_to([4.9, -1.45, 0])
        eq = M("R = 0.60 × 0.40 = 0.24 mm", 36, OFF).move_to([-1.0, 3.15, 0])
        self.add(h2, eq)
        everything = VGroup(w.axis, w.tag, w.pop, w.l1, w.m1, w.guide, w.l2, w.surv, w.m2, w.S, w.l3, w.R, w.m3,
                            h2, eq)
        self.at("S happens within a generation")
        sl = T("S: within one generation", 24, SURV)
        sl.move_to([-0.4 - sl.width / 2, BASE[1] + 0.8, 0])
        self.play(Transform(w.S[1], sl), Indicate(w.S[0], color=SURV, scale_factor=1.1), run_time=0.8)
        self.at("R happens across generations")
        rl = T("R: across generations", 24, OFF)
        rl.move_to([-0.4 - rl.width / 2, BASE[2] + 0.8, 0])
        self.play(Transform(w.R[1], rl), Indicate(w.R[0], color=OFF, scale_factor=1.1), run_time=0.8)
        self.at("Only R is evolution")
        ev = T("only R is evolution", 24, OFF).move_to([4.7, -2.1, 0])
        self.play(FadeIn(ev), Indicate(w.m3, color=OFF, scale_factor=1.1), run_time=0.7)
        self.at("this R is a prediction")
        pr = T("this R is a prediction", 24, OFF).move_to([4.5, -2.1, 0])
        self.play(ReplacementTransform(ev, pr), run_time=0.6)
        self.at("Only real offspring")
        self.play(w.m3.animate.set_opacity(0.45), run_time=0.5)
        self.at("one more question")
        ask = chip("Were the offspring measured?", OFF, size=36).move_to([0.8, 0.0, 0])
        self.play(everything.animate.set_opacity(0.07), pr.animate.set_opacity(0.07), run_time=0.5)
        self.play(FadeIn(ask, scale=0.9), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Only R is evolution: measure the offspring."
