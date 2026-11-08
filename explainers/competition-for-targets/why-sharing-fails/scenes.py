"""Why Sharing Fails  (Developmental Neuroscience, competition for targets, chapter 2)

COLOR MAP (one color per concept, whole series; taken from scenes.old.py)
  BLUE   = a neuron whose fate is not yet decided (A and B; A is the solid wedge, B the faint wedge)
  GREEN  = a winner / a neuron that survives
  RED    = a loser / a neuron that dies
  YELLOW = nerve growth factor (NGF), what a neuron catches
  PURPLE = the receptor TrkA (its level)
  ORANGE = the punishment signal (BDNF and NT-4)
  TEAL   = the receptor p75, and links to other lessons
  ROSE   = the length of a signal (new in this chapter)
  TEXT   = plain labels
  GOLD   = the question, a number to watch, one highlight
  GREY   = target, axons, axes, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
ROSE = "#E58FA8"


def P(x, y):
    return np.array([x, y, 0.0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ngf_dot(p, r=0.09):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=1.5, fill_color=YELLOW, fill_opacity=1).move_to(p)


def lt(text, size, color, x, y, weight=NORMAL):
    """Text whose left edge sits at x."""
    return T(text, size, color, weight=weight).move_to(P(x, y), aligned_edge=LEFT)


# ---------------------------------------------------------------- the two-neuron stage
NX = -6.1                  # soma x
AY, BY = 2.1, -2.1         # row heights of neuron A and B
PADL, PADR = -4.8, -0.3    # axon-tip pad (receptors, later the TrkA bars)
PADH = 1.8
RX0, DX = -4.4, 0.6        # first receptor x, spacing
RS = 0.4                   # receptor side
BX0 = -4.5                 # left end of the TrkA bars
BH = 0.7                   # bar height
U = 0.115                  # bar length per unit of TrkA
G = 1.25                   # growth per round in the toy round
NA, NB = 13, 12            # receptors (and NGF molecules caught): 13 / 25 = 52 percent
TGX, TGY = 4.4, 0.2        # target centre in the opening scenes
GAPX = -2.4                # centre of the gap between the two pads


def val(k, who):
    return (NA if who == "A" else NB) * G ** k


def vtxt(v):
    return f"{v:.4g}"


def soma(y, letter):
    c = Circle(radius=0.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3).move_to(P(NX, y))
    return VGroup(c, T(letter, 34, TEXT, weight=BOLD).move_to(c))


def axon(y):
    return Line(P(NX + 0.5, y), P(PADL, y), color=GREY, stroke_width=5)


def pad(y):
    return RoundedRectangle(corner_radius=0.15, width=PADR - PADL, height=PADH, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.08).move_to(P((PADL + PADR) / 2, y))


def rec_pos(y, n, i):
    per = 7 if n == NA else 6
    if i < per:
        return P(RX0 + DX * i, y + 0.4)
    return P(RX0 + DX * (i - per), y - 0.4)


def receptors(y, n):
    return VGroup(*[Square(side_length=RS, stroke_color=PURPLE, stroke_width=1.5, fill_color=PURPLE,
                           fill_opacity=0.95).move_to(rec_pos(y, n, i)) for i in range(n)])


def mark_extra(rA):
    rA[6].set_stroke(GOLD, 5)
    return rA


def bound_dots(y, n):
    return VGroup(*[ngf_dot(rec_pos(y, n, i), 0.12) for i in range(n)])


def bar(y, L, color=PURPLE, h=BH, op=0.85, x0=BX0):
    L = max(L, 0.05)
    return Rectangle(width=L, height=h, stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=op).move_to(P(x0 + L / 2, y))


def seg(y, L0, L1, color=PURPLE, h=BH, x0=BX0, op=0.3):
    return Rectangle(width=L1 - L0, height=h, stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=op).move_to(P(x0 + (L0 + L1) / 2, y))


def vlab(y, L, v):
    return M(vtxt(v), 26, TEXT, weight=BOLD).move_to(P(BX0 + L / 2, y))


def blab():
    """'TrkA level, A' and 'TrkA level, B' tags sitting in the pads above the bars."""
    return VGroup(lt("TrkA level, A", 26, PURPLE, BX0, AY + 0.62, BOLD), lt("TrkA level, B", 26, PURPLE, BX0, BY + 0.62, BOLD))


def level_bars(k):
    """bars, numbers for round k (k = 0 is the receptor count)."""
    LA, LB = val(k, "A") * U, val(k, "B") * U
    return (bar(AY, LA), bar(BY, LB), vlab(AY, LA, val(k, "A")), vlab(BY, LB, val(k, "B")))


def target_parts():
    box = RoundedRectangle(corner_radius=0.2, width=2.2, height=4.6, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.12).move_to(P(TGX, TGY))
    lab = T("target", 26, GREY).move_to(P(TGX, -2.55))
    nchip = chip("NGF", YELLOW, 28).move_to(P(TGX, 3.0))
    return box, lab, nchip


def target_dots():
    ds = []
    for r in range(5):
        for c in range(5):
            ds.append(ngf_dot(P(TGX + (c - 2) * 0.5, TGY + (2 - r) * 0.5), 0.13))
    return ds  # row 0 is the top row


# ---------------------------------------------------------------- the pie
PC = P(3.8, 0.2)
PR = 2.7


def pie_wedges(p, c=PC, R=PR):
    a = Sector(radius=R, angle=TAU * p, start_angle=0, arc_center=c, fill_color=BLUE, fill_opacity=0.6,
               stroke_color=BLUE, stroke_width=3)
    b = Sector(radius=R, angle=TAU * (1 - p), start_angle=TAU * p, arc_center=c, fill_color=BLUE,
               fill_opacity=0.12, stroke_color=BLUE, stroke_width=3)
    return VGroup(a, b)


def pie_labels(p, c=PC, R=PR, dec=0, size=28, qA=False):
    mA = TAU * p / 2
    mB = TAU * p + TAU * (1 - p) / 2

    def spot(m, big):
        f = 0.58 if big else 1.0 + 0.55 / R
        return c + f * R * np.array([np.cos(m), np.sin(m), 0.0])

    def place(t, m, big):
        if big:
            t.move_to(spot(m, True))
        else:
            c_ = np.cos(m)
            pt = c + (R + 0.12) * np.array([c_, np.sin(m), 0.0])
            t.move_to(pt, aligned_edge=LEFT if c_ > 0.25 else (RIGHT if c_ < -0.25 else ORIGIN))
        return t

    out = VGroup()
    if qA:
        la = T("A ?", size, GOLD, weight=BOLD)
    else:
        la = T(f"A {p * 100:.{dec}f}%", size, TEXT, weight=BOLD)
    out.add(place(la, mA, p > 0.2))
    lb = T("B" if qA else f"B {(1 - p) * 100:.{dec}f}%", size, TEXT, weight=BOLD)
    out.add(place(lb, mB, (1 - p) > 0.2))
    return out


def pie_header(c=PC, R=PR, text="share of the NGF caught", y=None):
    return T(text, 26, GREY).move_to(P(c[0], (c[1] + R + 0.5) if y is None else y))


def tracked_pie(tr, c=PC, R=PR, dec=0, size=28):
    return always_redraw(lambda: VGroup(pie_wedges(tr.get_value(), c, R), pie_labels(tr.get_value(), c, R, dec, size)))


def pie_static(p=0.52, qA=False, **kw):
    return pie_wedges(p), pie_labels(p, qA=qA, **kw), pie_header()


def neutral_pie(c=PC, R=PR):
    circ = Circle(radius=R, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2).move_to(c)
    q = T("?", 110, GOLD, weight=BOLD).move_to(c)
    return circ, q, pie_header()


def stage(recs=False, dots=False, tpad=True):
    """soma, axon, pad for A and B, in the same place in every scene."""
    parts = [soma(AY, "A"), axon(AY), soma(BY, "B"), axon(BY)]
    if tpad:
        parts += [pad(AY), pad(BY)]
    g = VGroup(*parts)
    out = [g]
    if recs:
        out += [mark_extra(receptors(AY, NA)), receptors(BY, NB)]
    if dots:
        out += [bound_dots(AY, NA), bound_dots(BY, NB)]
    return out


def count_labels(a, b, ca=PURPLE, cb=PURPLE):
    return (T(a, 28, ca, weight=BOLD).move_to(P(GAPX, 0.62)), T(b, 28, cb, weight=BOLD).move_to(P(GAPX, -0.62)))


def question_head():
    return T("After many rounds, what is A's share?", 32, TEXT).move_to(P(-2.4, 3.45))


def option_chips():
    return (chip("grow", GREEN, 28).move_to(P(-4.7, 0.0)), chip("shrink", RED, 28).move_to(P(-2.7, 0.0)),
            chip("stay put", GREY, 28).move_to(P(-0.6, 0.0)))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Competition: How Neurons Win a Target"
    TITLE = "Why Sharing Fails"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    def construct(self):
        sA, aA, sB, aB, pA_, pB_ = soma(AY, "A"), axon(AY), soma(BY, "B"), axon(BY), pad(AY), pad(BY)
        box, lab, _ = target_parts()
        self.at("two neurons")
        self.play(FadeIn(sA, scale=0.6), FadeIn(sB, scale=0.6), Create(aA), Create(aB), FadeIn(pA_), FadeIn(pB_),
                  run_time=0.7)
        self.at("share one target")
        self.play(FadeIn(box), FadeIn(lab), run_time=0.9)
        self.at("one starts with")
        lead = T("tiny lead", 30, GOLD).move_to(P(GAPX, -0.1))
        la = arr(P(GAPX, 0.3), P(GAPX, 1.1), GOLD, 6, 0.22)
        self.play(FadeIn(lead), GrowArrow(la), run_time=0.8)
        c1 = chip("grow", GREEN, 30).move_to(P(1.5, 1.1))
        c2 = chip("shrink", RED, 30).move_to(P(1.5, 0.0))
        c3 = chip("stay put", GREY, 30).move_to(P(1.5, -1.1))
        self.at("grow")
        self.play(FadeIn(c1, scale=0.8), run_time=0.5)
        self.at("shrink")
        self.play(FadeIn(c2, scale=0.8), run_time=0.5)
        self.at("stay put")
        self.play(FadeIn(c3, scale=0.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(SpokenScene):
    def construct(self):
        g, = stage()
        box, lab, nchip = target_parts()
        self.add(g, box, lab)
        rA, rB = receptors(AY, NA), receptors(BY, NB)
        self.at("neuron a")
        self.play(Indicate(g[0], color=BLUE, scale_factor=1.25), run_time=0.9)
        self.at("a little more")
        self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in list(rA) + list(rB)], lag_ratio=0.04), run_time=0.7)
        ca, cb = count_labels("A: 13 TrkA", "B: 12 TrkA")
        self.at("track a")
        self.play(FadeIn(ca, shift=UP * 0.1), FadeIn(cb, shift=DOWN * 0.1),
                  Indicate(rA[6], color=GOLD, scale_factor=2.2), run_time=0.9)
        extra = T("one extra", 26, GOLD).move_to(P(1.15, AY + 0.4))
        self.play(rA[6].animate.set_stroke(GOLD, 5), FadeIn(extra, shift=LEFT * 0.1), run_time=0.4)
        self.at("binds ngf")
        dots = VGroup(*target_dots())
        self.play(FadeIn(nchip, shift=DOWN * 0.2), LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.04),
                  run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    def construct(self):
        g, = stage()
        box, lab, nchip = target_parts()
        rA, rB = mark_extra(receptors(AY, NA)), receptors(BY, NB)
        ca, cb = count_labels("A: 13 TrkA", "B: 12 TrkA")
        extra = T("one extra", 26, GOLD).move_to(P(1.15, AY + 0.4))
        dl = target_dots()
        dots = VGroup(*dl)
        self.add(g, box, lab, nchip, rA, rB, ca, cb, extra, dots)
        tk = T("TrkA, a receptor tyrosine kinase", 26, PURPLE, weight=BOLD).move_to(P(GAPX, 0.0))
        self.at("receptor tyrosine kinase")
        self.play(FadeIn(tk), FadeOut(extra), Indicate(VGroup(rA, rB), color=PURPLE, scale_factor=1.04), run_time=1.2)
        self.at("more receptor means")
        anims = []
        for i, d in enumerate(dl[:NA]):
            anims.append(d.animate.move_to(rec_pos(AY, NA, i)).scale(0.9))
        for i, d in enumerate(dl[NA:]):
            anims.append(d.animate.move_to(rec_pos(BY, NB, i)).scale(0.9))
        self.play(FadeOut(tk), run_time=0.3)
        self.play(LaggedStart(*anims, lag_ratio=0.06), run_time=2.4)
        na, nb = count_labels("A caught 13", "B caught 12", YELLOW, YELLOW)
        self.play(Transform(ca, na), Transform(cb, nb), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(SpokenScene):
    def construct(self):
        g, rA, rB, dA, dB = stage(recs=True, dots=True)
        box, lab, nchip = target_parts()
        ca, cb = count_labels("A caught 13", "B caught 12", YELLOW, YELLOW)
        self.add(g, rA, rB, dA, dB, box, lab, nchip, ca, cb)
        wedges = pie_wedges(0.52)
        labs = pie_labels(0.52)
        hdr = pie_header()
        self.at("by chance")
        self.play(FadeOut(box), FadeOut(lab), FadeOut(nchip), run_time=0.6)
        self.at("52")
        self.play(FadeIn(hdr), GrowFromCenter(wedges), run_time=1.0)
        self.play(FadeIn(labs[0]), run_time=0.4)
        self.at("neuron b catches")
        self.play(Indicate(wedges[1], color=BLUE, scale_factor=1.04), FadeIn(labs[1]), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    def construct(self):
        g, rA, rB, dA, dB = stage(recs=True, dots=True)
        w, l, h = pie_static()
        ca, cb = count_labels("A caught 13", "B caught 12", YELLOW, YELLOW)
        self.add(g, rA, rB, dA, dB, w, l, h, ca, cb)
        YA, YB = 0.68, -0.68
        cNa = chip("NGF caught", YELLOW, 26, pad=0.15).move_to(P(-3.95, YA))
        cNb = chip("NGF caught", YELLOW, 26, pad=0.15).move_to(P(-3.95, YB))
        cTa = chip("TrkA made", PURPLE, 26, pad=0.15).move_to(P(-1.4, YA))
        cTb = chip("TrkA made", PURPLE, 26, pad=0.15).move_to(P(-1.4, YB))
        dnA = arr(P(-3.8, 1.5), P(-3.8, YA + 0.36), GOLD, 5, 0.2)
        dnB = arr(P(-3.8, -1.5), P(-3.8, YB - 0.36), GOLD, 5, 0.2)
        rgA = arr(P(-2.83, YA), P(-2.45, YA), GOLD, 5, 0.18)
        rgB = arr(P(-2.83, YB), P(-2.45, YB), GOLD, 5, 0.18)
        upA = arr(P(-1.4, YA + 0.36), P(-1.4, 1.5), GOLD, 5, 0.2)
        upB = arr(P(-1.4, YB - 0.36), P(-1.4, -1.5), GOLD, 5, 0.2)
        self.at("feedback")
        self.play(FadeOut(ca), FadeOut(cb), run_time=0.3)
        self.play(GrowArrow(dnA), FadeIn(cNa, shift=DOWN * 0.1), run_time=0.7)
        self.play(GrowArrow(dnB), FadeIn(cNb, shift=UP * 0.1), run_time=0.7)
        self.at("makes track a")
        self.play(GrowArrow(rgA), FadeIn(cTa, shift=RIGHT * 0.1), GrowArrow(rgB), FadeIn(cTb, shift=RIGHT * 0.1),
                  run_time=0.5)
        self.play(GrowArrow(upA), GrowArrow(upB), Indicate(rA, color=WHITE, scale_factor=1.0),
                  Indicate(rB, color=WHITE, scale_factor=1.0), run_time=0.6)
        lab = T("made in proportion to caught", 26, TEXT).move_to(P(GAPX, 0.0))
        self.at("in proportion")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06(SpokenScene):
    def construct(self):
        g, rA, rB, dA, dB = stage(recs=True, dots=True)
        w, l, h = pie_static()
        self.add(g, rA, rB, dA, dB, w, l, h)
        self.at("each neuron's catch")
        self.play(Indicate(dA, color=YELLOW, scale_factor=1.3), Indicate(dB, color=YELLOW, scale_factor=1.3), run_time=0.9)
        aA = arr(P(-0.2, 1.5), P(2.0, 1.1), GREY, 6, 0.24)
        aB = arr(P(-0.2, -1.5), P(2.0, -1.0), GREY, 6, 0.24)
        sh = T("share follows TrkA", 30, PURPLE, weight=BOLD).move_to(P(-2.0, 0.0))
        self.at("proportional to")
        self.play(GrowArrow(aA), GrowArrow(aB), FadeIn(sh, shift=RIGHT * 0.1), run_time=0.7)
        self.at("its track a")
        self.play(Indicate(rA, color=WHITE, scale_factor=1.0), Indicate(rB, color=WHITE, scale_factor=1.0),
                  Indicate(sh, color=WHITE, scale_factor=1.05), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07(SpokenScene):
    def construct(self):
        g, rA, rB, dA, dB = stage(recs=True, dots=True)
        w, l, h = pie_static()
        self.add(g, rA, rB, dA, dB, w, l, h)
        bA, bB, tA, tB = level_bars(0)
        lab = blab()
        note = T("illustrative numbers", 26, GREY).move_to(P(GAPX, -3.5))
        self.at("both neurons")
        self.play(FadeOut(rA), FadeOut(rB), FadeOut(dA), FadeOut(dB), run_time=0.45)
        self.play(FadeIn(bA), FadeIn(bB), FadeIn(tA), FadeIn(tB), FadeIn(lab), run_time=0.55)
        nA, nB, uA, uB = level_bars(1)
        gA = T("+25%", 28, PURPLE, weight=BOLD).move_to(P(BX0 + val(1, "A") * U + 0.8, AY))
        gB = T("+25%", 28, PURPLE, weight=BOLD).move_to(P(BX0 + val(1, "B") * U + 0.8, BY))
        self.at("make more receptor")
        self.play(Transform(bA, nA), Transform(bB, nB), FadeOut(tA), FadeOut(tB), FadeIn(uA), FadeIn(uB),
                  FadeIn(note), run_time=1.0)
        self.play(FadeIn(gA, shift=RIGHT * 0.1), FadeIn(gB, shift=RIGHT * 0.1), run_time=0.4)
        self.at("b grows")
        self.play(Indicate(bB, color=PURPLE, scale_factor=1.05), run_time=0.8)
        self.at("same fraction")
        self.play(Indicate(gA, color=GOLD, scale_factor=1.3), Indicate(gB, color=GOLD, scale_factor=1.3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def level_scene_base(sc, k, qA=False):
    g, = stage()
    bA, bB, tA, tB = level_bars(k)
    sc.add(g, bA, bB, tA, tB, blab())
    return g, bA, bB, tA, tB


class S08(SpokenScene):
    def construct(self):
        g, bA, bB, tA, tB = level_scene_base(self, 1)
        w, l, h = neutral_pie()
        self.add(w, l, h)
        head = question_head()
        c1, c2, c3 = option_chips()
        self.at("after many rounds")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.8)
        self.at("what share")
        self.play(LaggedStart(FadeIn(c1, scale=0.8), FadeIn(c2, scale=0.8), FadeIn(c3, scale=0.8), lag_ratio=0.3),
                  Indicate(l, color=GOLD, scale_factor=1.2), run_time=1.0)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        g, bA, bB, tA, tB = level_scene_base(self, 1)
        w, l, h = neutral_pie()
        head = question_head()
        c1, c2, c3 = option_chips()
        self.add(w, l, h, head, c1, c2, c3)
        self.wait(5.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10(SpokenScene):
    def construct(self):
        g, bA, bB, tA, tB = level_scene_base(self, 1)
        w0, q0, h = neutral_pie()
        head = question_head()
        c1, c2, c3 = option_chips()
        self.add(w0, q0, h, head, c1, c2, c3)
        w, l = pie_wedges(0.52), pie_labels(0.52)
        self.at("still")
        self.play(FadeOut(w0), FadeOut(q0), FadeIn(w), FadeIn(l), FadeOut(head), c1.animate.set_opacity(0.25), c2.animate.set_opacity(0.25),
                  c3[0].animate.set_stroke(GOLD, 6).set_fill(GOLD, 0.3), run_time=0.7)
        pc2, pr2 = P(3.8, 0.75), 2.15
        w2 = pie_wedges(0.52, pc2, pr2)
        l2b = pie_labels(0.52, pc2, pr2, size=28)
        xs = [1.9 + 0.9 * i for i in range(6)]
        rl = T("round", 26, GREY).move_to(P(0.5, -2.05))
        rn = VGroup(*[M(str(i + 1), 26, GREY).move_to(P(xs[i], -2.05)) for i in range(6)])
        nums = VGroup(*[M("52%", 26, BLUE, weight=BOLD).move_to(P(xs[i], -2.7)) for i in range(6)])
        cap = T("A's share after each round", 26, GREY).move_to(P(3.8, -3.4))
        self.at("proportional sharing")
        self.play(ReplacementTransform(w, w2), ReplacementTransform(l, l2b), FadeIn(rl), FadeIn(cap), run_time=0.6)
        for i in range(6):
            self.play(Indicate(w2, color=WHITE, scale_factor=1.04), FadeIn(rn[i], shift=UP * 0.1),
                      FadeIn(nums[i], shift=UP * 0.1), run_time=0.38)
        self.at("round after round")
        self.play(Indicate(nums, color=GOLD, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11(SpokenScene):
    def construct(self):
        g, bA, bB, tA, tB = level_scene_base(self, 1)
        w, l, h = pie_static()
        self.add(w, l, h)

        def end(k, who):
            return BX0 + val(k, who) * U

        gh = [seg(AY, val(1, "A") * U, val(2, "A") * U), seg(BY, val(1, "B") * U, val(2, "B") * U)]
        gA = T("gain", 28, PURPLE, weight=BOLD).move_to(P(end(2, "A") + 0.7, AY))
        gB = T("gain", 28, PURPLE, weight=BOLD).move_to(P(end(2, "B") + 0.7, BY))
        self.at("gain")
        self.play(FadeIn(gh[0], shift=RIGHT * 0.2), FadeIn(gh[1], shift=RIGHT * 0.2), FadeIn(gA), FadeIn(gB), run_time=0.8)
        pA = T("+25%", 28, PURPLE, weight=BOLD).move_to(gA)
        pB = T("+25%", 28, PURPLE, weight=BOLD).move_to(gB)
        b2A, b2B, t2A, t2B = level_bars(2)
        self.at("fixed fraction")
        self.play(FadeOut(gA), FadeOut(gB), FadeIn(pA), FadeIn(pB), run_time=0.3)
        self.play(Transform(bA, b2A), Transform(bB, b2B), FadeOut(tA), FadeOut(tB), FadeIn(t2A), FadeIn(t2B),
                  FadeOut(gh[0]), FadeOut(gh[1]), run_time=0.5)
        gh2 = [seg(AY, val(2, "A") * U, val(3, "A") * U), seg(BY, val(2, "B") * U, val(3, "B") * U)]
        b3A, b3B, t3A, t3B = level_bars(3)
        self.at("of what it already")
        self.play(FadeIn(gh2[0], shift=RIGHT * 0.2), FadeIn(gh2[1], shift=RIGHT * 0.2),
                  pA.animate.move_to(P(end(3, "A") + 0.8, AY)), pB.animate.move_to(P(end(3, "B") + 0.8, BY)), run_time=0.6)
        self.play(Transform(bA, b3A), Transform(bB, b3B), FadeOut(t2A), FadeOut(t2B), FadeIn(t3A), FadeIn(t3B),
                  FadeOut(gh2[0]), FadeOut(gh2[1]), run_time=0.6)
        ratio = T("ratio stays 13 : 12", 30, GOLD, weight=BOLD).move_to(P(GAPX, 0.0))
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12(SpokenScene):
    def construct(self):
        g, bA, bB, tA, tB = level_scene_base(self, 3)
        tr = ValueTracker(0.52)
        pie = tracked_pie(tr)
        h = pie_header()
        self.add(pie, h)
        LA3, LB3 = val(3, "A") * U, val(3, "B") * U
        c = 10.0                      # same absolute top-up for both neurons, in the same units as the bars
        topL = c * U
        chp = chip("basal TrkA", PURPLE, 28).move_to(P(-4.0, 0.0))
        self.at("basal synthesis")
        self.play(FadeIn(chp, scale=0.8), run_time=0.6)
        aA = arr(P(-3.3, 0.45), P(BX0 + LA3 + topL / 2, AY - 0.4), PURPLE, 5, 0.2)
        aB = arr(P(-3.3, -0.45), P(BX0 + LB3 + topL / 2, BY + 0.4), PURPLE, 5, 0.2)
        self.at("both neurons get")
        self.play(GrowArrow(aA), GrowArrow(aB), run_time=0.7)
        sA, sB = seg(AY, LA3, LA3 + topL, op=0.5), seg(BY, LB3, LB3 + topL, op=0.5)
        pa = M("+10", 26, TEXT, weight=BOLD).move_to(sA)
        pb = M("+10", 26, TEXT, weight=BOLD).move_to(sB)
        same = T("same top-up", 26, PURPLE, weight=BOLD).move_to(P(-0.9, 0.0))
        nA, nB = vlab(AY, LA3 + topL, val(3, "A") + c), vlab(BY, LB3 + topL, val(3, "B") + c)
        nA.move_to(P(BX0 + (LA3) / 2, AY))
        nB.move_to(P(BX0 + (LB3) / 2, BY))
        self.at("same top up")
        self.play(FadeIn(sA, shift=RIGHT * 0.2), FadeIn(sB, shift=RIGHT * 0.2), FadeIn(pa), FadeIn(pb), FadeIn(same),
                  FadeOut(tA), FadeOut(tB), FadeIn(nA), FadeIn(nB), run_time=0.8)
        shareA = (val(3, "A") + c) / (val(3, "A") + val(3, "B") + 2 * c)
        even = DashedLine(PC + P(-PR - 0.25, 0), PC + P(PR + 0.25, 0), color=GOLD, stroke_width=4)
        elab = T("dashed line: even split", 26, GOLD).move_to(P(3.8, -3.3))
        self.at("shares drift")
        self.play(tr.animate.set_value(shareA), Create(even), FadeIn(elab), run_time=1.2)
        self.at("toward even")
        self.play(Indicate(even, color=WHITE, scale_factor=1.0), Indicate(elab, color=WHITE, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.3, width=11.6, height=5.6, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.06).move_to(P(0, 0))
        l1 = T("In this setup,", 46, TEXT).move_to(P(0, 1.5))
        l2 = T("feedback on receptor level alone", 46, PURPLE).move_to(P(0, 0.2))
        l3 = T("does not make a winner.", 46, TEXT, weight=BOLD).move_to(P(0, -1.2))
        self.add(card, l1)
        self.at("feedback on receptor level")
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.8)
        self.at("does not make")
        self.play(FadeIn(l3, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
BXL, BXR = -1.5, 6.5
TOPY, BOTY, BOXH = 1.75, -1.75, 2.7
CAUGHT_X = -3.95


def box_at(y, color):
    return RoundedRectangle(corner_radius=0.15, width=BXR - BXL, height=BOXH, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.06).move_to(P((BXL + BXR) / 2, y))


def caught_dots(n, hi=0):
    ds = []
    for i in range(n):
        d = ngf_dot(P(-5.0 + 0.4 * (i % 5), -0.85 - 0.4 * (i // 5)), 0.12)
        if i >= n - hi:
            d.set_stroke(WHITE, 3)
        ds.append(d)
    return VGroup(*ds)


def left_col():
    s = soma(0.0, "A")
    s.move_to(P(-6.1, 0.0))
    ch = chip("NGF caught", YELLOW, 28).move_to(P(CAUGHT_X, 0.0))
    return s, ch


def top_box_final():
    box = box_at(TOPY, PURPLE)
    title = lt("neuron A: TrkA level", 28, PURPLE, BXL + 0.25, TOPY + 0.97, BOLD)
    b0 = bar(TOPY + 0.15, 5.4, x0=BXL + 0.25)
    mk = DashedLine(P(BXL + 0.25 + 1.8, TOPY + 0.15 - 0.4), P(BXL + 0.25 + 1.8, TOPY - 0.7), color=GREY, stroke_width=3)
    tb = T("before", 26, GREY).move_to(P(BXL + 0.25 + 1.8, TOPY - 0.98))
    ta = T("after", 26, PURPLE).move_to(P(BXL + 0.25 + 5.4, TOPY - 0.98))
    return box, title, b0, mk, tb, ta


class S14(SpokenScene):
    def construct(self):
        s, ch = left_col()
        self.add(s, ch)
        dots = caught_dots(5)
        self.play(FadeIn(dots), run_time=0.5)
        self.at("two things")
        t1 = chip("more TrkA", PURPLE, 28).move_to(P(1.0, TOPY))
        t2 = chip("longer signal", ROSE, 28).move_to(P(1.0, BOTY))
        a1 = arr(P(CAUGHT_X + 1.25, 0.25), P(-0.2, TOPY - 0.15), PURPLE, 5, 0.22)
        a2 = arr(P(CAUGHT_X + 1.25, -0.25), P(-0.2, BOTY + 0.15), ROSE, 5, 0.22)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(t1), FadeIn(t2), run_time=1.0)
        box, title, bfull, mk, tb, ta = top_box_final()
        bshort = bar(TOPY + 0.15, 1.8, x0=BXL + 0.25)
        a1n = arr(P(CAUGHT_X + 1.25, 0.25), P(BXL - 0.05, TOPY - 0.15), PURPLE, 7, 0.24)
        self.at("it raises track a")
        self.play(ReplacementTransform(t1, box), Transform(a1, a1n), FadeIn(title), FadeIn(bshort), run_time=0.6)
        self.play(FadeIn(mk), FadeIn(tb), run_time=0.3)
        self.play(Transform(bshort, bfull), run_time=0.8)
        self.play(FadeIn(ta), run_time=0.2)
        more = caught_dots(10, hi=5)
        cm = T("catches more", 28, GOLD, weight=BOLD).move_to(P(CAUGHT_X, -2.0))
        self.at("catches more")
        self.play(Transform(dots, more), FadeIn(cm, shift=UP * 0.1), Indicate(ch, color=YELLOW, scale_factor=1.06),
                  run_time=1.0)
        self.finish()


def pulses(widths, gap, x0, base, h=0.7, color=ROSE):
    out = []
    x = x0
    for wd in widths:
        out.append(Rectangle(width=wd, height=h, stroke_color=color, stroke_width=2, fill_color=color,
                             fill_opacity=0.85).move_to(P(x + wd / 2, base + h / 2)))
        x += wd + gap
    return VGroup(*out)


class S15(SpokenScene):
    def construct(self):
        s, ch = left_col()
        dots = caught_dots(10, hi=5)
        cm = T("catches more", 28, GOLD, weight=BOLD).move_to(P(CAUGHT_X, -2.0))
        box, title, bfull, mk, tb, ta = top_box_final()
        a1 = arr(P(CAUGHT_X + 1.25, 0.25), P(BXL - 0.05, TOPY - 0.15), PURPLE, 7, 0.24)
        t2 = chip("longer signal", ROSE, 28).move_to(P(1.0, BOTY))
        a2 = arr(P(CAUGHT_X + 1.25, -0.25), P(-0.2, BOTY + 0.15), ROSE, 5, 0.22)
        self.add(s, ch, dots, cm, box, title, bfull, mk, tb, ta, a1, t2, a2)
        box2 = box_at(BOTY, ROSE)
        title2 = lt("neuron A: signal length", 28, ROSE, BXL + 0.25, BOTY + 0.97, BOLD)
        y1, y2 = BOTY - 0.05, BOTY - 0.85
        PX = 0.7
        base1 = Line(P(PX - 0.2, y1), P(BXR - 0.3, y1), color=GREY, stroke_width=2)
        base2 = Arrow(P(PX - 0.2, y2), P(BXR - 0.2, y2), buff=0, color=GREY, stroke_width=3, tip_length=0.18)
        tl = T("time", 26, GREY).move_to(P(BXR - 0.75, y2 - 0.24))
        lb = lt("before", 26, GREY, BXL + 0.25, y1 + 0.28)
        la = lt("after", 26, ROSE, BXL + 0.25, y2 + 0.28, BOLD)
        p0 = pulses([0.5, 0.5, 0.5], 0.6, PX, y1, h=0.5)
        p1 = pulses([1.3, 1.3, 1.3], 0.5, PX, y2, h=0.5)
        a2n = arr(P(CAUGHT_X + 1.25, -0.25), P(BXL - 0.05, BOTY + 0.15), ROSE, 7, 0.24)
        self.at("lengthens each signal")
        self.play(ReplacementTransform(t2, box2), Transform(a2, a2n), FadeIn(title2), FadeIn(base1), FadeIn(lb),
                  FadeIn(p0), run_time=0.8)
        p0c = p0.copy()
        self.add(p0c)
        self.play(FadeIn(base2), FadeIn(tl), FadeIn(la), Transform(p0c, p1), run_time=1.1)
        self.at("molecule counts")
        self.play(Indicate(dots, color=YELLOW, scale_factor=1.12), Indicate(p0c, color=WHITE, scale_factor=1.04),
                  run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16(SpokenScene):
    def construct(self):
        note = T("assumed toy update, not measured biology", 28, GOLD).move_to(P(0, 3.4))
        self.at("simple arithmetic")
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.7)
        c_sig = chip("signal", ROSE, 40)
        eq = T("=", 44, TEXT)
        c_catch = chip("catch", YELLOW, 40)
        tm = T("×", 48, TEXT)
        c_dur = chip("duration", ROSE, 40)
        row1 = VGroup(c_sig, eq, c_catch, tm, c_dur).arrange(RIGHT, buff=0.45).move_to(P(0, 2.3))
        self.at("each signal lasts")
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in row1], lag_ratio=0.25), run_time=1.2)
        sub = T("duration in proportion to catch", 32, TEXT).move_to(P(0, 1.2))
        self.at("proportion to the catch")
        self.play(FadeIn(sub, shift=UP * 0.1), Indicate(c_dur, color=ROSE, scale_factor=1.1), run_time=0.9)
        r2a = chip("TrkA made", PURPLE, 40)
        r2t = T("in proportion to", 32, TEXT)
        r2b = chip("signal", ROSE, 40)
        row2 = VGroup(r2a, r2t, r2b).arrange(RIGHT, buff=0.5).move_to(P(0, -0.05))
        self.at("and track a")
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in row2], lag_ratio=0.3), run_time=1.4)
        r3a = chip("ratio of A to B", BLUE, 38).move_to(P(-3.9, -1.5))
        self.at("then each round")
        self.play(FadeIn(r3a, shift=UP * 0.1), run_time=0.6)
        ar = arr(P(-1.1, -1.5), P(1.1, -1.5), GOLD, 7, 0.28)
        r3b = chip("ratio × ratio", BLUE, 38).move_to(P(3.9, -1.5))
        sq = T("squared", 34, GOLD, weight=BOLD).move_to(P(0, -0.95))
        self.at("squares the ratio")
        self.play(GrowArrow(ar), FadeIn(r3b, shift=RIGHT * 0.2), FadeIn(sq, shift=UP * 0.1), run_time=0.7)
        rs = [0.52 / 0.48]
        for _ in range(3):
            rs.append(rs[-1] ** 2)
        nums = [M(f"{r:.2f}", 44, BLUE, weight=BOLD) for r in rs]
        row = VGroup(nums[0], T("→", 40, GREY), nums[1], T("→", 40, GREY), nums[2], T("→", 40, GREY),
                     nums[3]).arrange(RIGHT, buff=0.35).move_to(P(0, -2.7))
        cap = T("ratio of A to B, round by round (toy arithmetic)", 28, GREY).move_to(P(0, -3.5))
        self.at("ratio of a to b")
        self.play(FadeIn(cap), LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in row], lag_ratio=0.35), run_time=1.6)
        self.wait(1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17(SpokenScene):
    def construct(self):
        r = 0.52 / 0.48
        shares = []
        for _ in range(6):
            shares.append(r / (1 + r))
            r = r * r
        c17, R17 = P(2.7, 0.0), 2.5
        tr = ValueTracker(shares[0])
        pie = tracked_pie(tr, c=c17, R=R17)
        base, sc = -2.55, 0.05
        ax = VGroup(Line(P(-5.8, base), P(-0.4, base), color=GREY, stroke_width=3),
                    Line(P(-5.8, base), P(-5.8, base + 100 * sc), color=GREY, stroke_width=3))
        ticks = VGroup(*[M(str(v), 26, GREY).move_to(P(-6.3, base + v * sc)) for v in (0, 50, 100)])
        half = DashedLine(P(-5.8, base + 50 * sc), P(-0.4, base + 50 * sc), color=GREY, stroke_width=2)
        ytitle = lt("A's share of NGF (%)", 26, TEXT, -6.5, 3.3)
        note = T("assumed toy update, not measured biology", 26, GOLD).move_to(P(2.8, 3.3))
        xt = T("teaching round (not time)", 26, GREY).move_to(P(-2.6, -3.45))
        BXs = [-5.2 + 0.85 * i for i in range(6)]
        bars, vals, nums = [], [], []
        for i, s in enumerate(shares):
            h = s * 100 * sc
            bars.append(Rectangle(width=0.65, height=h, stroke_color=BLUE, stroke_width=2, fill_color=BLUE,
                                  fill_opacity=0.7).move_to(P(BXs[i], base + h / 2)))
            vals.append(M(f"{round(s * 100)}%", 26, TEXT, weight=BOLD).move_to(P(BXs[i], base + h + 0.3)))
            nums.append(M(str(i + 1), 26, GREY).move_to(P(BXs[i], base - 0.35)))
        rtag = T("round 1", 38, GOLD, weight=BOLD).move_to(P(2.7, -3.2))
        self.add(ax, ticks, half, ytitle, note, xt)
        self.play(FadeIn(pie), GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]), FadeIn(nums[0]), FadeIn(rtag), run_time=0.8)
        self.at("climb")
        for k in range(1, 6):
            nt = T(f"round {k + 1}", 38, GOLD, weight=BOLD).move_to(P(2.7, -3.2))
            self.play(tr.animate.set_value(shares[k]), GrowFromEdge(bars[k], DOWN), FadeIn(vals[k]), FadeIn(nums[k]),
                      FadeOut(rtag), FadeIn(nt), run_time=0.9)
            rtag = nt
            self.wait(0.7)
        self.wait(1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18(SpokenScene):
    def construct(self):
        c_lead = chip("lead", BLUE, 40).move_to(P(0, 2.7))
        c_catch = chip("more catch", YELLOW, 34).move_to(P(4.6, -1.5))
        c_trk = chip("more TrkA, longer signal", PURPLE, 34).move_to(P(-3.3, -1.5))
        a1 = arr(P(1.0, 2.35), P(4.3, -0.95), GREY, 6, 0.26)
        a2 = arr(P(3.1, -1.5), P(-0.35, -1.5), GREY, 6, 0.26)
        a3 = arr(P(-3.3, -0.95), P(-0.9, 2.3), GREY, 6, 0.26)
        self.add(c_lead)
        self.play(GrowArrow(a1), FadeIn(c_catch, shift=RIGHT * 0.2), run_time=0.4)
        self.play(GrowArrow(a2), FadeIn(c_trk, shift=LEFT * 0.2), run_time=0.4)
        self.play(GrowArrow(a3), run_time=0.3)
        pf = T("positive feedback", 40, GOLD, weight=BOLD).move_to(P(0.4, -0.15))
        self.at("positive feedback")
        self.play(FadeIn(pf, scale=0.9), Indicate(VGroup(a1, a2, a3), color=GOLD, scale_factor=1.0), run_time=1.0)
        link = chip("signaling circuits lesson", TEAL, 34, pad=0.25, fill_opacity=0.3).move_to(P(0, -3.1))
        ul = Line(link.get_corner(DL) + P(0.25, 0.14), link.get_corner(DR) + P(-0.25, 0.14), color=TEAL, stroke_width=2)
        self.at("signaling circuits")
        self.play(FadeIn(VGroup(link, ul), shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.3, width=11.8, height=3.9, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.06).move_to(P(0, 1.45))
        l0 = T("Here is the condition it needs", 32, GOLD).move_to(P(0, 2.85))
        l1 = T("A lead can grow only when", 44, TEXT).move_to(P(0, 1.9))
        l2 = T("the reward rises", 44, YELLOW).move_to(P(0, 1.0))
        l3 = T("faster than the lead.", 44, BLUE, weight=BOLD).move_to(P(0, 0.1))
        self.add(card, l0)
        self.at("a lead can grow")
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.7)
        X0 = -6.4
        lr = lt("reward (signal)", 26, YELLOW, X0, -1.15)
        ll = lt("lead (A's share above even)", 26, BLUE, X0, -2.45)
        tr = ValueTracker(0.0)

        def lenR():
            return 0.5 + 11.0 * tr.get_value()

        def lenL():
            return 0.5 + 4.0 * tr.get_value()

        ar = always_redraw(lambda: arr(P(X0, -1.75), P(X0 + lenR(), -1.75), YELLOW, 9, 0.35))
        al = always_redraw(lambda: arr(P(X0, -3.05), P(X0 + lenL(), -3.05), BLUE, 9, 0.35))
        self.at("the reward")
        self.add(ar, al)
        self.play(FadeIn(l2, shift=UP * 0.15), FadeIn(lr), FadeIn(ll), tr.animate.set_value(0.3), run_time=0.8,
                  rate_func=linear)
        self.at("faster than")
        self.play(FadeIn(l3, shift=UP * 0.1, run_time=0.3), tr.animate(run_time=1.6, rate_func=linear).set_value(1.0))
        self.wait(1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
SY_A, SY_B = 1.4, -1.4
TIPA, TIPB = 3.7, 2.7
TGT20X, TGT20Y = 5.6, 0.2


def s20_parts():
    box = RoundedRectangle(corner_radius=0.2, width=1.5, height=5.0, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.12).move_to(P(TGT20X, TGT20Y))
    lab = T("target", 26, GREY).move_to(P(TGT20X, 3.15))

    def sm(y, letter):
        return VGroup(Circle(radius=0.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3).move_to(P(NX, y)),
                      T(letter, 34, TEXT, weight=BOLD).move_to(P(NX, y)))

    sA, sB = sm(SY_A, "A"), sm(SY_B, "B")
    aA = Line(P(NX + 0.5, SY_A), P(TIPA, SY_A), color=GREY, stroke_width=10)
    aB = Line(P(NX + 0.5, SY_B), P(TIPB, SY_B), color=GREY, stroke_width=10)
    cA = Circle(radius=0.26, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).move_to(P(TIPA, SY_A))
    cB = Circle(radius=0.26, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).move_to(P(TIPB, SY_B))
    return box, lab, sA, sB, aA, aB, cA, cB


def s20_gap():
    dA = DashedLine(P(TIPA, SY_A - 0.3), P(TIPA, 0.0), color=GOLD, stroke_width=4)
    dB = DashedLine(P(TIPB, SY_B + 0.3), P(TIPB, 0.0), color=GOLD, stroke_width=4)
    dbl = DoubleArrow(P(TIPB, 0.0), P(TIPA, 0.0), buff=0.0, color=GOLD, stroke_width=5, tip_length=0.18)
    return VGroup(dA, dB, dbl)


class S20(SpokenScene):
    def construct(self):
        box, lab, sA, sB, aA, aB, cA, cB = s20_parts()
        self.add(box, lab, sA, sB)
        self.at("arriving first")
        mA = cA.copy().move_to(P(NX + 0.5, SY_A))
        mB = cB.copy().move_to(P(NX + 0.5, SY_B))
        self.add(mA, mB)
        self.play(Create(aA, run_time=1.6, rate_func=linear), Create(aB, run_time=2.0, rate_func=linear),
                  mA.animate(run_time=1.6, rate_func=linear).move_to(P(TIPA, SY_A)),
                  mB.animate(run_time=2.0, rate_func=linear).move_to(P(TIPB, SY_B)))
        gap = s20_gap()
        lab2 = T("may give the lead", 32, GOLD, weight=BOLD).move_to(P(-0.9, 0.0))
        self.at("may well give")
        self.play(Create(gap), FadeIn(lab2), run_time=1.0)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        box, lab, sA, sB, aA, aB, cA, cB = s20_parts()
        gap = s20_gap()
        self.add(box, lab, sA, sB, aA, aB, cA, cB, gap)
        self.at("arrival order alone")
        self.play(Indicate(gap, color=GOLD, scale_factor=1.1), run_time=0.9)
        q = T("grows?", 32, GOLD, weight=BOLD).move_to(P(-0.9, 0.0))
        sx0, sx1, sy = -5.5, 5.5, -3.3
        shA = Rectangle(width=(sx1 - sx0) * 0.52, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                        fill_opacity=0.6).move_to(P(sx0 + (sx1 - sx0) * 0.26, sy))
        shB = Rectangle(width=(sx1 - sx0) * 0.48, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                        fill_opacity=0.12).move_to(P(sx1 - (sx1 - sx0) * 0.24, sy))
        ta = T("A 52%", 28, TEXT, weight=BOLD).move_to(shA)
        tb = T("B 48%", 28, TEXT, weight=BOLD).move_to(shB)
        cap = T("share of the NGF caught", 26, GREY).move_to(P(-2.6, -2.7))
        self.at("small lead grows")
        self.play(FadeIn(q), FadeIn(VGroup(shA, shB, ta, tb, cap)), run_time=0.8)
        stay = T("lead stays small", 32, GOLD, weight=BOLD).move_to(P(-0.9, 0.0))
        self.at("supply keeps coming")
        self.play(FadeOut(q), FadeIn(stay), run_time=0.4)
        for wave in range(2):
            ds, anims = [], []
            for who, ty, tx, n in (("A", SY_A, TIPA, 13), ("B", SY_B, TIPB, 12)):
                for i in range(n):
                    y = ty + (i / (n - 1) - 0.5) * 0.9
                    d = ngf_dot(P(TGT20X - 0.2 + 0.25 * (i % 3), y), 0.09)
                    ds.append(d)
                    anims.append(d.animate.move_to(P(tx + 0.4 + 0.22 * ((i * 2) % 3), y)))
            self.add(*ds)
            self.play(LaggedStart(*anims, lag_ratio=0.05), run_time=1.5, rate_func=linear)
            self.play(*[FadeOut(d) for d in ds], run_time=0.2)
        self.wait(0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S22(SpokenScene):
    def construct(self):
        TX = -5.7
        box = RoundedRectangle(corner_radius=0.2, width=1.4, height=4.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to(P(TX, 0.5))
        lab = T("target", 26, GREY).move_to(P(TX, 3.05))
        self.add(box, lab)
        self.at("target keeps releasing")
        rng = np.random.default_rng(7)
        X_START, X_END = TX + 0.8, 6.4
        LEN = X_END - X_START
        SPD = 3.4
        N = 70
        dots = VGroup()
        for j in range(N):
            d = ngf_dot(P(X_START, 0.0), 0.13)
            d.y0 = float(rng.uniform(-1.9, 2.7))
            d.birth = float(rng.uniform(0.0, LEN / SPD))
            d.set_opacity(0.0)
            dots.add(d)
        state = {"t": 0.0}

        def upd(m, dt):
            state["t"] += dt
            for d in m:
                age = state["t"] - d.birth
                if age < 0:
                    continue
                run = (age * SPD) % LEN
                d.move_to(P(X_START + run, d.y0))
                d.set_opacity(min(1.0, run / 0.5, (LEN - run) / 0.8))

        dots.add_updater(upd)
        self.add(dots)
        y0 = -3.0
        barL = Line(P(-6.2, y0), P(6.3, y0), color=GREY, stroke_width=6)
        t0 = Line(P(-5.3, y0 - 0.2), P(-5.3, y0 + 0.2), color=GREY, stroke_width=5)
        t1 = Line(P(6.0, y0 - 0.2), P(6.0, y0 + 0.2), color=GREY, stroke_width=5)
        marker = Triangle(color=GOLD, fill_opacity=1, stroke_width=0).scale(0.22).rotate(PI).move_to(P(-5.3, y0 + 0.4))
        fl = T("first arrival", 26, GREY).move_to(P(-4.9, y0 - 0.5))
        el = T("end of death period", 26, GREY).move_to(P(4.6, y0 - 0.5))
        dlab = T("death period", 28, TEXT, weight=BOLD).move_to(P(0.2, y0 - 0.5))
        nowl = always_redraw(lambda: T("now", 26, GOLD, weight=BOLD).move_to(marker.get_center() + P(0, 0.5)))
        self.at("throughout")
        self.add(nowl)
        self.play(Create(barL), FadeIn(t0), FadeIn(t1), FadeIn(marker), FadeIn(fl), FadeIn(el), run_time=0.6)
        self.play(marker.animate.move_to(P(6.0, y0 + 0.4)), FadeIn(dlab), run_time=1.1, rate_func=linear)
        self.at("not just")
        self.play(Indicate(fl, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.wait(1.2)
        dots.clear_updaters()
        nowl.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------------------------
def sim12(n=12, steps=400, seed=3, rate=1.6, sd=0.03, T_=2.2):
    rng = np.random.default_rng(seed)
    x = 1 + sd * rng.standard_normal(n)
    x0 = x.copy()
    dt = T_ / steps
    for _ in range(steps):
        rel = x / x.mean()
        h = rel ** 8 / (1 + rel ** 8)
        x = np.maximum(x + dt * (0.1 + 3.0 * h - 1.5 * x) * rate, 0.05)
    return x0, x


class S23(SpokenScene):
    def construct(self):
        x0, x1 = sim12()
        base = -2.5
        sc = 2.1
        BXs = [-6.4 + 0.5 * i for i in range(12)]

        def vb(i, v, color=BLUE):
            h = max(v * sc, 0.05)
            return Rectangle(width=0.38, height=h, stroke_color=color, stroke_width=2, fill_color=color,
                             fill_opacity=0.75).move_to(P(BXs[i], base + h / 2))

        bars = VGroup(*[vb(i, x0[i]) for i in range(12)])
        floor = Line(P(-6.7, base), P(-0.3, base), color=GREY, stroke_width=3)
        cap = T("TrkA level, 12 neurons", 26, PURPLE, weight=BOLD).move_to(P(-3.5, -3.0))
        note = T("the lesson's simulation (a sketch)", 26, GREY).move_to(P(-3.5, -3.5))
        gain = chip("gain", GREEN, 28).move_to(P(-5.3, 3.3))
        lose = chip("lose", RED, 28).move_to(P(-3.4, 3.3))
        self.at("the simulation")
        self.play(FadeIn(bars, shift=UP * 0.2), FadeIn(floor), FadeIn(cap), FadeIn(note), run_time=1.0)
        ax0, ax1, ay0, ay1 = 1.8, 6.5, -2.5, 2.6
        axes = VGroup(Line(P(ax0, ay0), P(ax1, ay0), color=GREY, stroke_width=3),
                      Line(P(ax0, ay0), P(ax0, ay1), color=GREY, stroke_width=3))
        xl = T("neuron's share", 26, GREY).move_to(P((ax0 + ax1) / 2, ay0 - 0.5))
        yl = T("TrkA response", 26, GREY).rotate(PI / 2).move_to(P(ax0 - 0.45, (ay0 + ay1) / 2))
        rel = np.linspace(0, 2.0, 120)
        hh = rel ** 8 / (1 + rel ** 8)
        pts = [P(ax0 + (ax1 - ax0) * r / 2.0, ay0 + 0.15 + h_ * (ay1 - ay0 - 0.3)) for r, h_ in zip(rel, hh)]
        curve = VMobject(stroke_color=PURPLE, stroke_width=7).set_points_smoothly(pts)
        self.at("splits its neurons")
        self.play(FadeIn(axes), FadeIn(xl), FadeIn(yl), FadeIn(gain), FadeIn(lose), run_time=0.5)
        self.play(*[Transform(bars[i], vb(i, x1[i], GREEN if x1[i] > 1 else RED)) for i in range(12)],
                  Create(curve, rate_func=linear), run_time=1.7)
        self.at("response to each")
        self.play(Indicate(curve, color=GOLD, scale_factor=1.0), Indicate(yl, color=GOLD, scale_factor=1.1), run_time=1.0)
        sw = T("switch-like", 34, GOLD, weight=BOLD).move_to(P(3.3, 1.9))
        self.at("switch like")
        self.play(FadeIn(sw), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S24(SpokenScene):
    def construct(self):
        hd = T("Takeaway", 42, GOLD, weight=BOLD, font=TITLE_FONT).move_to(P(0, 3.3))
        self.at("take away")
        self.play(FadeIn(hd, shift=DOWN * 0.1), run_time=0.6)
        c1 = chip("identical neurons", BLUE, 36).move_to(P(-3.7, 2.0))
        c2 = chip("proportional sharing", YELLOW, 36).move_to(P(-3.7, 0.55))
        c3 = chip("no basal synthesis", PURPLE, 36).move_to(P(-3.7, -0.9))
        p1 = T("+", 36, GREY).move_to(P(-3.7, 1.28))
        p2 = T("+", 36, GREY).move_to(P(-3.7, -0.17))
        self.at("identical neurons")
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("proportional sharing")
        self.play(FadeIn(p1), FadeIn(c2, shift=RIGHT * 0.2), run_time=0.5)
        self.at("no basal synthesis")
        self.play(FadeIn(p2), FadeIn(c3, shift=RIGHT * 0.2), run_time=0.5)
        pc = P(4.2, 0.55)
        w = pie_wedges(0.52, c=pc, R=2.3)
        l = pie_labels(0.52, c=pc, R=2.3, size=30)
        eq = T("=", 60, GOLD).move_to(P(0.35, 0.55))
        fz = T("a lead stays frozen", 36, GOLD, weight=BOLD).move_to(P(4.2, -2.1))
        self.at("a lead stays frozen")
        self.play(FadeIn(eq), GrowFromCenter(w), FadeIn(l), FadeIn(fz, shift=UP * 0.1), run_time=1.0)
        bar_ = RoundedRectangle(corner_radius=0.2, width=12.2, height=0.95, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.08).move_to(P(0, -3.2))
        rule = T("To grow, the reward has to rise faster than the lead.", 34, TEXT)
        fit(rule, 11.6)
        rule.move_to(bar_)
        self.at("to grow")
        self.play(FadeIn(bar_), FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.at("faster than the lead")
        self.play(Indicate(rule, color=GOLD, scale_factor=1.04), run_time=0.9)
        self.finish()


class S25End(EndCard):
    LINE = "For identical neurons with proportional sharing, a lead stays frozen; to grow, the reward must rise faster than the lead."

    def construct(self):
        l1 = T("For identical neurons with proportional sharing,", 40, TEXT, font=TITLE_FONT)
        l2 = T("a lead stays frozen;", 40, GOLD, font=TITLE_FONT, weight=BOLD)
        l3 = T("to grow, the reward must rise faster than the lead.", 40, TEXT, font=TITLE_FONT)
        g = VGroup(l1, l2, l3).arrange(DOWN, buff=0.35)
        fit(g, 12.2)
        sub = T("biochemistrypedia.com", 26, TEAL)
        g2 = VGroup(g, sub).arrange(DOWN, buff=0.6)
        self.play(FadeIn(g, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
