"""Carried, or relayed?  (section film, Long-Distance Signaling in Neurons)

COLOR MAP (one color per concept, whole film)
  YELLOW = the courier and its parcel (the carried receptor)
  TEAL   = the relay: the message handed from stretch to stretch
  BLUE   = dynein, the motor
  GREEN  = survival, evidence, "settled"
  RED    = a block, "stopped", "proof" the title does not claim
  ORANGE = "not settled"
  GREY   = axon, cell body, labels, citations
  GOLD   = title rule only
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
YA, YB = 1.5, -1.5          # lane heights: courier lane, brigade lane
X0, X1 = -5.4, 3.7          # axon from tip to cell body
BODY_X = 4.7
NSEG = 4


def lane(y, label, color, segmented):
    bar = RoundedRectangle(corner_radius=0.2, width=X1 - X0, height=0.7, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.18).move_to([(X0 + X1) / 2, y, 0])
    body = Circle(radius=0.95, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([BODY_X, y, 0])
    bl = T("cell body", 22, GREY).move_to(body)
    tip = T("tip", 22, GREY).move_to([X0 - 0.5, y, 0])
    lab = T(label, 28, color, weight=BOLD)
    lab.move_to([X0, y + 0.8, 0]).align_to(bar, LEFT)
    segs, divs = [], []
    if segmented:
        w = (X1 - X0) / NSEG
        for k in range(NSEG):
            cx = X0 + w * (k + 0.5)
            segs.append(Rectangle(width=w - 0.12, height=0.58, stroke_width=0, fill_color=TEAL, fill_opacity=0).move_to([cx, y, 0]))
            if k:
                divs.append(Line([X0 + w * k, y - 0.35, 0], [X0 + w * k, y + 0.35, 0], color=GREY, stroke_width=2))
    g = VGroup(bar, body, bl, tip, lab, *divs, *segs)
    g.bar, g.body, g.lab, g.segs, g.divs, g.y = bar, body, lab, segs, divs, y
    return g


def dim(g, f=0.45):
    """scale every fill and stroke opacity by f (keeps the faint fills faint)."""
    for m in g.family_members_with_points():
        m.set_fill(opacity=m.get_fill_opacity() * f)
        m.set_stroke(opacity=m.get_stroke_opacity() * f)
    return g


def seg_cx(k):
    w = (X1 - X0) / NSEG
    return X0 + w * (k + 0.5)


def parcel(label=None):
    box = RoundedRectangle(corner_radius=0.12, width=0.9 if label else 0.7, height=0.46, stroke_color=YELLOW,
                           stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.95)
    g = VGroup(box)
    if label:
        g.add(T(label, 22, BG, weight=BOLD).move_to(box))
    return g


def motor(parcel_mob):
    m = chip("dynein", BLUE, size=22, pad=0.12).next_to(parcel_mob, DOWN, buff=0.22)
    link = Line(parcel_mob.get_bottom(), m.get_top(), color=BLUE, stroke_width=3)
    return VGroup(link, m)


def note():
    return T("idealised, not to scale", 22, GREY).move_to([4.4, 3.5, 0])


def hop(scene, A, upto=NSEG, rt=0.4):
    """light the stretches of lane A one after another, then the cell body."""
    for k in range(upto):
        anims = [A.segs[k].animate.set_fill(TEAL, 0.6)]
        if k:
            anims.append(A.segs[k - 1].animate.set_fill(TEAL, 0.0))
        scene.play(*anims, run_time=rt)
    scene.play(A.segs[upto - 1].animate.set_fill(TEAL, 0.0), A.body[0].animate.set_stroke(TEAL, 5), run_time=rt)


class S00Title(TitleCard):
    LESSON = "Long-distance signaling in neurons"
    TITLE = "Carried, or relayed?"


class S01TwoWays(SpokenScene):
    def construct(self):
        A = lane(YA, "courier", YELLOW, False)
        B = lane(YB, "bucket brigade", TEAL, True)
        n = note()
        pc = parcel().move_to([X0 + 0.45, YA, 0])
        self.play(FadeIn(A.bar), FadeIn(A.body), FadeIn(A[2]), FadeIn(A[3]),
                  FadeIn(B.bar), FadeIn(B.body), FadeIn(B[2]), FadeIn(B[3]), FadeIn(n), run_time=1.0)
        self.at("One answer is a courier")
        self.play(FadeIn(A.lab, shift=RIGHT * 0.2), FadeIn(pc, scale=0.8), run_time=0.6)
        self.at("the whole way")
        self.play(pc.animate.move_to([X1 - 0.5, YA, 0]), run_time=1.4, rate_func=linear)
        self.play(A.body[0].animate.set_stroke(YELLOW, 5), run_time=0.3)
        self.at("bucket brigade")
        self.play(FadeIn(B.lab, shift=RIGHT * 0.2), *[FadeIn(m) for m in B.divs], run_time=0.7)
        self.at("hands the message")
        hop(self, B, rt=0.45)
        self.finish()


class S02Block(SpokenScene):
    def construct(self):
        A = lane(YA, "courier", YELLOW, False)
        B = lane(YB, "bucket brigade", TEAL, True)
        dim(B)
        n = note()
        pc = parcel().move_to([X0 + 0.45, YA, 0])
        self.add(A, B, n, pc)
        mt = motor(pc)
        self.at("popular test")
        self.play(FadeIn(mt, shift=UP * 0.1), run_time=0.5)
        cross = Cross(mt[1], stroke_color=RED, stroke_width=6)
        lbl = T("the test: block dynein", 24, RED, weight=BOLD).next_to(mt[1], RIGHT, buff=0.3)
        self.at("block dynein")
        self.play(Create(cross), FadeIn(lbl), run_time=0.5)
        cite = T("Heerssen, Pazyra, Segal, 2004", 24, GREY).move_to([-1.0, -3.3, 0])
        self.at("In 2004")
        self.play(FadeOut(mt), FadeOut(cross), FadeOut(lbl), FadeIn(cite), run_time=0.5)
        mt2 = motor(pc)
        self.at("motors transport")
        self.play(FadeIn(mt2), run_time=0.3)
        grp = VGroup(pc, mt2)
        lab_trk = T("Trk", 22, BG, weight=BOLD).move_to(pc)
        lab_trk.add_updater(lambda m: m.move_to(pc))
        D = X1 - X0 - 0.95
        self.play(grp.animate.shift(RIGHT * D * 0.3), run_time=0.8, rate_func=linear)
        self.at("activated")
        self.play(grp.animate.shift(RIGHT * D * 0.7), FadeIn(lab_trk), run_time=2.4, rate_func=linear)
        lab_trk.clear_updaters()
        surv = T("survival needs this", 24, GREEN).move_to([4.2, -0.05, 0])
        self.at("needed for the survival")
        self.play(FadeIn(surv, shift=UP * 0.1), A.body[0].animate.set_stroke(GREEN, 5), run_time=0.6)
        ev = chip("evidence for a courier", GREEN, size=24, pad=0.14).move_to([-1.5, 0.3, 0])
        self.at("real evidence")
        self.play(FadeIn(ev, scale=0.9), run_time=0.5)
        self.finish()


class S03SameResult(SpokenScene):
    def construct(self):
        A = lane(YA, "courier", YELLOW, False)
        B = lane(YB, "bucket brigade", TEAL, True)
        n = note()
        pc = parcel().move_to([X0 + 0.45, YA, 0])
        mt = motor(pc)
        self.add(A, B, n, pc, mt)
        self.at("A brigade would fail")
        self.play(Indicate(B.lab, color=TEAL, scale_factor=1.15), run_time=0.7)
        self.at("Suppose each stretch")
        w = (X1 - X0) / NSEG
        dyn = VGroup(*[T("dynein", 22, BLUE).move_to([seg_cx(k), YB, 0]) for k in range(NSEG)])
        sup = T("suppose: every stretch needs dynein", 24, GREY).move_to([-1.0, YB - 1.15, 0])
        self.play(FadeIn(dyn, lag_ratio=0.2), FadeIn(sup), run_time=1.2)
        self.at("Then blocking")
        crosses = VGroup(*[Cross(dyn[k], stroke_color=RED, stroke_width=5) for k in range(NSEG)])
        # the courier lane lights up again so the same block is seen on both
        self.play(Create(crosses, lag_ratio=0.2), run_time=1.0)
        cr2 = Cross(mt[1], stroke_color=RED, stroke_width=6)
        self.at("stops the courier")
        self.play(Create(cr2), run_time=0.4)
        stA = T("stopped", 26, RED, weight=BOLD).move_to([BODY_X, 0.0, 0])
        stB = T("stopped", 26, RED, weight=BOLD).move_to([BODY_X, YB - 1.15, 0])
        self.play(FadeIn(stA), FadeIn(stB), run_time=0.4)
        same = chip("same result", GREY, size=26).move_to([-1.5, 0.15, 0])
        self.at("cannot tell them apart")
        self.play(FadeIn(same, scale=0.9), run_time=0.5)
        self.finish()


class S04Score(SpokenScene):
    def construct(self):
        # clear the lanes
        self.add(lane(YA, "courier", YELLOW, False), lane(YB, "bucket brigade", TEAL, True))
        self.clear()
        c1h = T("2002", 30, ORANGE, font=MONO)
        c1 = T("retrograde signals can support neuron survival\nwithout retrograde transport of NGF itself", 30, TEXT, line_spacing=0.9)
        card1 = VGroup(c1h, c1).arrange(DOWN, buff=0.15)
        c2h = T("2003", 30, ORANGE, font=MONO)
        c2 = T("“Evidence in support of signaling endosome-based\nretrograde survival of sympathetic neurons”", 26, TEXT, line_spacing=0.9)
        card2 = VGroup(c2h, c2).arrange(DOWN, buff=0.15)
        who1 = T("MacInnis and Campenot", 26, GREY)
        who2 = T("Ye, Kuruvilla, Zweifel and Ginty", 26, GREY)
        r1 = VGroup(VGroup(card1, who1).arrange(DOWN, buff=0.15)).move_to([0, 2.2, 0])
        r2 = VGroup(VGroup(card2, who2).arrange(DOWN, buff=0.15)).move_to([0, -0.1, 0])
        for r in (r1, r2):
            fit(r, max_w=11.5)
        sup = chip("claims support", GREEN, size=30).move_to([-2.4, -2.3, 0])
        prf = chip("claims proof", RED, size=28).move_to([2.4, -2.3, 0])
        strike = Line(prf.get_left() + LEFT * 0.1, prf.get_right() + RIGHT * 0.1, color=RED, stroke_width=5)
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.8)
        self.at("In 2003")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.8)
        self.at("claims support")
        self.play(FadeIn(sup, scale=0.9), run_time=0.4)
        self.at("does not claim")
        self.play(FadeIn(prf, scale=0.9), run_time=0.3)
        self.play(Create(strike), run_time=0.3)
        self.at("Settled")
        hs = T("Settled", 32, GREEN, weight=BOLD).move_to([-3.4, 2.7, 0])
        hn = T("Not settled", 32, ORANGE, weight=BOLD).move_to([3.4, 2.7, 0])
        s1 = T("NGF at the terminal\nis enough", 28, TEXT, line_spacing=0.9)
        s2 = T("a signal from the terminal\nreaches the nucleus", 28, TEXT, line_spacing=0.9)
        s3 = T("dynein carries activated receptors\nthat survival depends on", 28, TEXT, line_spacing=0.9)
        left = VGroup(s1, s2, s3).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([-3.4, 0.0, 0])
        n1 = T("whether the carried receptor\nis the only route", 28, TEXT, line_spacing=0.9).move_to([3.4, 1.0, 0])
        divl = Line([0, 3.2, 0], [0, -2.4, 0], color=GREY, stroke_width=2)
        self.play(FadeOut(r1), FadeOut(r2), FadeOut(sup), FadeOut(prf), FadeOut(strike), run_time=0.3)
        self.play(FadeIn(hs), FadeIn(hn), Create(divl), run_time=0.3)
        self.at("at the terminal")
        self.play(FadeIn(s1, shift=RIGHT * 0.15), run_time=0.4)
        self.at("signal from the terminal")
        self.play(FadeIn(s2, shift=RIGHT * 0.15), run_time=0.4)
        self.at("dynein carries activated")
        self.play(FadeIn(s3, shift=RIGHT * 0.15), run_time=0.4)
        self.at("Not settled")
        self.play(FadeIn(n1, shift=LEFT * 0.15), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "A motor block cannot tell a courier from a relay."
