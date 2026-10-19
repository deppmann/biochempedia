"""Synapse elimination: the less active input is removed  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = motor axon A and its terminals
  ORANGE = motor axon B and its terminals
  TEAL   = acetylcholine receptor sites on the muscle
  YELLOW = activity (impulses, stimulation, an active site)
  RED    = blocked, lost, removed, stop
  GREEN  = kept / nothing lost
  GREY   = muscle fiber, outlines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ----------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------
def bead(x, y, color, w):
    return RoundedRectangle(corner_radius=0.12, width=w, height=0.8, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.55).move_to([x, y, 0])


def build_ep(cx, n, sp, ry, kA, ytop, mh=1.5, label=True):
    """A junction: muscle band, n receptor sites, axon A on sites [0,kA), axon B on [kA,n)."""
    xs = [cx + (i - (n - 1) / 2) * sp for i in range(n)]
    yt = ry + 0.65
    d = {"xs": xs, "yt": yt, "ry": ry, "ytop": ytop, "sp": sp, "n": n}
    d["muscle"] = RoundedRectangle(corner_radius=0.2, width=n * sp + 0.6, height=mh, stroke_color=GREY,
                                   stroke_width=3, fill_color=GREY, fill_opacity=0.22).move_to([cx, ry + 0.2 - mh / 2, 0])
    d["mlabel"] = T("muscle fiber", 24, GREY).move_to([cx, ry + 0.2 - mh / 2 - 0.1, 0]) if label else VGroup()
    d["rec"] = [RoundedRectangle(corner_radius=0.08, width=sp * 0.8, height=0.4, stroke_color=TEAL, stroke_width=3,
                                 fill_color=TEAL, fill_opacity=0.55).move_to([x, ry, 0]) for x in xs]
    d["lineA"] = Line([xs[0], yt, 0], [xs[kA - 1], yt, 0], color=BLUE, stroke_width=10) if kA > 1 else VGroup()
    d["lineB"] = Line([xs[n - 1], yt, 0], [xs[kA], yt, 0], color=ORANGE, stroke_width=10) if n - kA > 1 else VGroup()
    d["shA"] = Line([xs[0], ytop, 0], [xs[0], yt, 0], color=BLUE, stroke_width=10)
    d["shB"] = Line([xs[n - 1], ytop, 0], [xs[n - 1], yt, 0], color=ORANGE, stroke_width=10)
    d["bead"] = [bead(xs[i], yt, BLUE if i < kA else ORANGE, sp * 0.84) for i in range(n)]
    return d


def ep_group(d, with_labels=False):
    g = VGroup(d["muscle"], d["mlabel"], *d["rec"], d["lineA"], d["lineB"], d["shA"], d["shB"], *d["bead"])
    return g


def axon_labels(d, size=26):
    a = T("axon", size, BLUE).next_to(d["shA"].get_start(), UP, buff=0.12)
    b = T("axon", size, ORANGE).next_to(d["shB"].get_start(), UP, buff=0.12)
    return a, b


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def pdot(x, y=None):
    return Dot(radius=0.14, color=YELLOW).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Synapse elimination"
    TITLE = "The less active input is removed"


# ----------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        d = build_ep(0, 6, 1.9, -0.9, 3, 2.55, mh=1.8)
        la, lb = axon_labels(d)
        tag = T("newborn rat", 32, TEXT).move_to([0, -3.2, 0])
        self.play(FadeIn(d["muscle"]), FadeIn(d["mlabel"]), *[FadeIn(r) for r in d["rec"]], FadeIn(tag), run_time=0.5)
        self.at("two or more motor neurons")
        self.play(Create(d["shA"]), FadeIn(la), run_time=0.5)
        self.play(Create(d["lineA"]), *[FadeIn(d["bead"][i]) for i in range(3)], run_time=0.6)
        self.play(Create(d["shB"]), FadeIn(lb), run_time=0.5)
        self.play(Create(d["lineB"]), *[FadeIn(d["bead"][i]) for i in range(3, 6)], run_time=0.6)
        # pulses + receptors respond
        self.at("Nothing is wrong")
        dA, dB = pdot(d["xs"][0], d["ytop"]), pdot(d["xs"][5], d["ytop"])
        self.add(dA, dB)
        self.play(dA.animate.move_to([d["xs"][0], d["yt"], 0]), dB.animate.move_to([d["xs"][5], d["yt"], 0]), run_time=0.7,
                  rate_func=linear)
        self.play(dA.animate.move_to([d["xs"][2], d["yt"], 0]), dB.animate.move_to([d["xs"][3], d["yt"], 0]), run_time=0.5,
                  rate_func=linear)
        self.play(FadeOut(dA), FadeOut(dB), run_time=0.15)
        self.at("makes the fiber respond")
        self.play(*[Indicate(r, color=YELLOW, scale_factor=1.15) for r in d["rec"]], run_time=0.9)
        bgrp = [d["lineB"], d["shB"], lb] + [d["bead"][i] for i in range(3, 6)]
        self.at("In the adult")
        adult = T("adult", 32, TEXT).move_to([0, -3.2, 0])
        xs, yt = d["xs"], d["yt"]
        shortA = d["lineA"].copy()
        fullA = Line([xs[0], yt, 0], [xs[5], yt, 0], color=BLUE, stroke_width=10)
        extra = [bead(xs[i], yt, BLUE, d["sp"] * 0.84) for i in (3, 4, 5)]
        self.play(*[FadeOut(m, shift=RIGHT * 0.3) for m in bgrp], ReplacementTransform(tag, adult),
                  Transform(d["lineA"], fullA), *[FadeIn(e) for e in extra], run_time=1.0)
        n2 = chip("two weeks later: one input", TEXT, size=26).move_to([0, -3.2, 0])
        self.at("Two weeks later")
        self.play(ReplacementTransform(adult, n2), run_time=0.5)
        q1 = T("?", 80, YELLOW, weight=BOLD).move_to([d["xs"][1], 1.4, 0])
        q2 = T("?", 80, YELLOW, weight=BOLD).move_to([d["xs"][4], 1.4, 0])
        self.at("Where do the extra inputs go")
        for m in bgrp:
            m.set_opacity(0.0)
        self.play(*[m.animate.set_opacity(0.35) for m in bgrp], FadeIn(q2, scale=0.6), FadeOut(n2),
                  Transform(d["lineA"], shortA), *[FadeOut(e) for e in extra], run_time=0.8)
        self.at("who decides")
        self.play(FadeIn(q1, scale=0.6), Indicate(q2, color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Branches(SpokenScene):
    def construct(self):
        nA = Circle(radius=0.55, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to([-4.8, 1.2, 0])
        nB = Circle(radius=0.55, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.35).move_to([-4.8, -1.2, 0])
        lA = T("motor neuron", 24, BLUE).next_to(nA, UP, buff=0.12)
        lB = T("motor neuron", 24, ORANGE).next_to(nB, DOWN, buff=0.12)
        fy = [2.55, 0.85, -0.85, -2.55]
        fibers = [RoundedRectangle(corner_radius=0.25, width=4.2, height=0.7, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.25).move_to([2.2, y, 0]) for y in fy]
        tallies = [M("2", 30, TEXT).move_to([5.7, y, 0]) for y in fy]
        head = T("inputs", 24, GREY).move_to([5.7, 3.25, 0])
        count = T("motor neurons: 2", 28, TEXT).move_to([0, -3.35, 0])
        endsA = [np.array([0.05, y, 0]) for y in fy]
        brA = [Line(nA.get_right(), e, color=BLUE, stroke_width=5) for e in endsA]
        brB = [Line(nB.get_right(), e, color=ORANGE, stroke_width=5) for e in endsA]
        self.play(FadeIn(VGroup(*fibers)), FadeIn(head), FadeIn(nA), FadeIn(nB), FadeIn(lA), FadeIn(lB),
                  *[Create(b) for b in brA + brB], FadeIn(VGroup(*tallies)), FadeIn(count), run_time=0.6)
        # the death hypothesis
        q = chip("neurons die?", RED, size=28).move_to([-3.0, 3.1, 0])
        self.at("did the extra neurons die")
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.5)
        self.at("did not change significantly")
        x = Cross(q, stroke_color=RED, stroke_width=6)
        self.play(Create(x), Indicate(count, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.play(FadeOut(q), FadeOut(x), run_time=0.4)
        self.at("nearly every fiber had one input")
        # branches retract: A keeps fibers 0,1 ; B keeps fibers 2,3
        lose = [brA[2], brA[3], brB[0], brB[1]]
        short = [Line(nA.get_right(), nA.get_right() + (e.get_end() - e.get_start()) * 0.02, color=RED, stroke_width=5)
                 for e in lose[:2]] + \
                [Line(nB.get_right(), nB.get_right() + (e.get_end() - e.get_start()) * 0.02, color=RED, stroke_width=5)
                 for e in lose[2:]]
        self.play(*[b.animate.set_color(RED) for b in lose], run_time=0.5)
        self.at("pulled back some")
        self.play(*[ReplacementTransform(b, s) for b, s in zip(lose, short)],
                  *[ReplacementTransform(t, M("1", 30, GREEN).move_to(t)) for t in tallies], run_time=1.6)
        self.play(*[FadeOut(s) for s in short], run_time=0.3)
        end = T("branch loss, not cell loss", 32, TEXT).move_to([0, -3.35, 0])
        self.at("Losing an input")
        self.play(ReplacementTransform(count, end), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Takeover(SpokenScene):
    def construct(self):
        d = build_ep(0, 6, 1.9, -0.9, 3, 2.55, mh=1.8)
        la, lb = axon_labels(d)
        self.add(ep_group(d), la, lb)
        xs, yt = d["xs"], d["yt"]
        lab = T("first image", 32, TEXT).move_to([0, 3.15, 0])
        self.at("Now watch one junction")
        self.play(FadeIn(lab), run_time=0.4)
        self.at("receptor sites are labeled")
        self.play(*[Indicate(r, color=TEAL, scale_factor=1.15) for r in d["rec"]], run_time=0.8)

        state = {"lineA": d["lineA"], "lineB": d["lineB"]}

        def take(i, final=False):
            nb = bead(xs[i], yt, ORANGE, d["sp"] * 0.84)
            start = nb.copy().move_to([xs[i + 1], yt, 0])
            self.add(start)
            newB = Line([xs[5], yt, 0], [xs[i], yt, 0], color=ORANGE, stroke_width=10)
            anims = [FadeOut(d["bead"][i], scale=0.3), ReplacementTransform(start, nb),
                     Transform(state["lineB"], newB)]
            if i >= 2:
                newA = Line([xs[0], yt, 0], [xs[i - 1], yt, 0], color=BLUE, stroke_width=10)
                anims.append(Transform(state["lineA"], newA))
            else:
                anims.append(FadeOut(state["lineA"]))
            if i == 0:
                anims += [FadeOut(d["shA"]), FadeOut(la)]
            self.play(*anims, run_time=1.0)

        self.at("one axon withdraws")
        lab2 = T("days later", 32, TEXT).move_to([0, 3.15, 0])
        self.play(ReplacementTransform(lab, lab2), run_time=0.4)
        self.play(Indicate(d["bead"][2], color=RED, scale_factor=1.1), run_time=0.6)
        self.at("extends into the sites")
        take(2)
        self.at("takeover")
        take(1)
        take(0)
        # prediction
        c1 = chip("territory at the start", TEXT, size=26).move_to([-3.4, -3.2, 0])
        c2 = chip("winner", TEXT, size=26).move_to([3.4, -3.2, 0])
        ar = Arrow(c1.get_right(), c2.get_left(), buff=0.12, color=GREY, stroke_width=5)
        x = Cross(VGroup(ar), stroke_color=RED, stroke_width=7).scale(0.8)
        self.at("could not be reliably")
        self.play(FadeIn(c1), run_time=0.4)
        self.play(FadeIn(c2), GrowArrow(ar), run_time=0.5)
        self.play(Create(x), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S04Activity(SpokenScene):
    def construct(self):
        d = build_ep(0, 6, 1.9, -0.9, 3, 2.55, mh=1.8)
        la, lb = axon_labels(d)
        self.add(ep_group(d), la, lb)
        xs, yt = d["xs"], d["yt"]
        act = chip("activity", YELLOW, size=30).move_to([0, 3.1, 0])
        self.at("Activity")
        self.play(FadeIn(act, scale=0.8), run_time=0.5)

        def volley(k, rt):
            for _ in range(k):
                a, b = pdot(xs[0], d["ytop"]), pdot(xs[5], d["ytop"])
                self.add(a, b)
                self.play(a.animate.move_to([xs[0], yt, 0]), b.animate.move_to([xs[5], yt, 0]), run_time=rt,
                          rate_func=linear)
                self.play(FadeOut(a), FadeOut(b), run_time=0.08)

        blocks = VGroup(inhib([xs[0] - 0.4, 1.55, 0], [xs[0] + 0.4, 1.55, 0]),
                        inhib([xs[5] - 0.4, 1.55, 0], [xs[5] + 0.4, 1.55, 0]))
        slow = chip("elimination: slower", RED, size=30).move_to([0, -3.2, 0])
        fast = chip("elimination: faster", GREEN, size=30).move_to([0, -3.2, 0])
        self.at("blocking nerve impulses")
        a, b = pdot(xs[0], d["ytop"]), pdot(xs[5], d["ytop"])
        self.add(a, b)
        self.play(a.animate.move_to([xs[0], 1.8, 0]), b.animate.move_to([xs[5], 1.8, 0]), run_time=0.5, rate_func=linear)
        self.play(Create(blocks[0]), Create(blocks[1]), FadeOut(a), FadeOut(b), run_time=0.4)
        self.at("slows elimination")
        self.play(FadeIn(slow, shift=UP * 0.2), run_time=0.5)
        self.at("Stimulating the muscle")
        self.play(FadeOut(blocks), ReplacementTransform(slow, fast), d["muscle"].animate.set_stroke(YELLOW),
                  run_time=0.5)
        volley(4, 0.3)
        self.at("everywhere at once")
        box = DashedVMobject(SurroundingRectangle(VGroup(d["muscle"], *d["bead"]), buff=0.15, color=YELLOW,
                                                  stroke_width=4, corner_radius=0.15))
        self.play(FadeOut(fast), d["muscle"].animate.set_stroke(GREY), Create(box), run_time=0.7)
        self.at("whether the loser is silent")
        c1 = chip("silent?", GREY, size=28).move_to([-3.4, -3.2, 0])
        c2 = chip("less active than its neighbor?", YELLOW, size=28).move_to([2.6, -3.2, 0])
        self.play(FadeOut(box), FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.at("only less active")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
def panels():
    L = build_ep(-3.35, 4, 1.3, -0.35, 2, 2.3, mh=1.8, label=False)
    R = build_ep(3.35, 4, 1.3, -0.35, 2, 2.3, mh=1.8, label=False)
    return L, R


def red_rec(d, i):
    r = d["rec"][i]
    return r.animate.set_stroke(RED).set_fill(RED, 0.7)


class S05Test(SpokenScene):
    def construct(self):
        L, R = panels()
        self.add(ep_group(L), ep_group(R))
        for d in (L, R):
            for lbl in axon_labels(d, 22):
                self.add(lbl)
        tl = T("one patch blocked", 28, TEXT).move_to([-3.35, 3.3, 0])
        tr = T("whole junction blocked", 28, TEXT).move_to([3.35, 3.3, 0])
        tox = chip("α-bungarotoxin: blocks receptors", RED, size=26).move_to([0, -3.2, 0])
        self.at("A toxin")
        self.play(FadeIn(tox, shift=UP * 0.2), run_time=0.5)
        self.at("Block one patch")
        self.play(FadeIn(tl), red_rec(L, 1), run_time=0.7)
        self.at("The receptors there are lost")
        rl = L["rec"][1]
        self.play(FadeOut(rl, scale=0.3), run_time=0.7)
        self.at("withdraws from that patch")
        newA = Line([L["xs"][0], L["yt"], 0], [L["xs"][0] + 0.001, L["yt"], 0], color=BLUE, stroke_width=10)
        self.play(FadeOut(L["bead"][1], scale=0.3), FadeOut(L["lineA"]), run_time=0.8)
        resl = T("lost at the blocked patch", 26, RED).move_to([-3.35, -2.45, 0])
        self.play(FadeIn(resl), run_time=0.4)
        self.at("Now block the whole junction")
        self.play(FadeIn(tr), *[red_rec(R, i) for i in range(4)], run_time=0.8)
        self.at("Nothing is eliminated")
        resr = T("nothing lost", 26, GREEN).move_to([3.35, -2.45, 0])
        self.play(FadeIn(resr), Indicate(VGroup(*R["bead"]), color=GREEN, scale_factor=1.05), run_time=0.9)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        L, R = panels()
        # start from the blocked state, before anything is lost
        grp = VGroup(ep_group(L), ep_group(R))
        self.add(grp)
        labs = []
        for d in (L, R):
            for lbl in axon_labels(d, 22):
                labs.append(lbl)
                self.add(lbl)
        tl = T("one patch blocked", 28, TEXT).move_to([-3.35, 3.3, 0])
        tr = T("whole junction blocked", 28, TEXT).move_to([3.35, 3.3, 0])
        self.add(tl, tr)
        self.play(red_rec(L, 1), *[red_rec(R, i) for i in range(4)], run_time=0.5)
        everything = VGroup(grp, *labs, tl, tr)
        self.at("partial block")
        yd = L["ry"] - 0.0
        dots = [Dot(radius=0.13, color=YELLOW).move_to([L["xs"][i], L["ry"] - 0.8, 0]) for i in (0, 2, 3)]
        act = [T("active", 22, YELLOW).move_to([L["xs"][i], -2.45, 0]) for i in (0, 2, 3)]
        sil = T("silent", 22, RED).move_to([L["xs"][1], -2.45, 0])
        self.at("silent patch")
        self.play(*[FadeIn(x, scale=0.5) for x in dots], FadeIn(VGroup(*act)), FadeIn(sil), run_time=0.7)
        self.play(*[Indicate(x, color=YELLOW, scale_factor=1.6) for x in dots], run_time=0.8)
        self.at("full block")
        sil_r = T("silent", 22, RED).move_to([3.35, -2.45, 0])
        self.play(Indicate(VGroup(*R["rec"]), color=RED, scale_factor=1.08), run_time=0.5)
        self.at("equally silent")
        self.play(FadeIn(sil_r), run_time=0.5)
        self.at("Nothing is less active")
        self.wait(0.6)
        # arrows from active neighbours to the silent site
        ar1 = inhib([L["xs"][0] + 0.25, L["ry"] - 0.8, 0], [L["xs"][1] - 0.25, L["ry"] - 0.8, 0], RED)
        ar2 = inhib([L["xs"][2] - 0.25, L["ry"] - 0.8, 0], [L["xs"][1] + 0.25, L["ry"] - 0.8, 0], RED)
        self.at("Active sites can destabilize")
        self.play(Create(ar1), Create(ar2), run_time=0.8)
        self.at("one junction")
        self.play(Indicate(VGroup(ar1, ar2), color=RED, scale_factor=1.1), run_time=0.8)
        rule = Text("A synapse is lost when it is\nless active than its neighbor.", font=TITLE_FONT, font_size=40,
                    color=TEXT, line_spacing=0.9)
        rule.move_to([0, 0.2, 0])
        self.at("Keep this rule")
        self.play(everything.animate.set_opacity(0.0), *[FadeOut(x) for x in dots + act + [sil, sil_r, ar1, ar2]],
                  run_time=0.6)
        self.play(FadeIn(rule, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A synapse is lost when it is less active than its neighbor."
