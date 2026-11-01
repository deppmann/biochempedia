"""Synaptic plasticity: one synapse, turned up or down  (Biochemistrypedia Neuroscience explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = glutamate (the transmitter)
  BLUE   = AMPA receptor
  PURPLE = NMDA receptor
  ORANGE = Mg2+ plug in the NMDA pore
  TEAL   = Ca2+
  PINK   = the postsynaptic membrane depolarized
  GREEN  = increase: LTP, CaMKII, receptors added
  RED    = decrease: LTD, phosphatases, receptors removed
  TEXT   = stimulus trains, the blocker APV
  GOLD   = the open question
  GREY   = membranes, outlines, before-bars, de-emphasized
All response bars are "in this sketch": relative heights, no values.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FC0"

CX0 = -2.1          # normal view: synapse centre x
MEM_Y = 1.5         # normal view: postsynaptic membrane y
# channel layout, x relative to the synapse centre: kind, rx
LAYOUT = [("A1", "A", -2.5), ("N1", "N", -1.55), ("A2", "A", -0.65), ("N2", "N", 0.35), ("A3", "A", 1.25)]
NEWSLOTS = [("A4", 2.05), ("A5", 2.75)]


def ampa(x, y, k=1.0, fill=0.4):
    w, gap, h = 0.2 * k, 0.1 * k, 0.62 * k
    return VGroup(*[RoundedRectangle(corner_radius=0.05 * k, width=w, height=h, stroke_color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=fill).move_to([x + s * (gap / 2 + w / 2), y, 0])
                    for s in (-1, 1)])


def nmda(x, y, k=1.0, fill=0.4):
    w, gap, h = 0.3 * k, 0.24 * k, 0.72 * k
    return VGroup(*[RoundedRectangle(corner_radius=0.05 * k, width=w, height=h, stroke_color=PURPLE, stroke_width=3,
                                     fill_color=PURPLE, fill_opacity=fill).move_to([x + s * (gap / 2 + w / 2), y, 0])
                    for s in (-1, 1)])


class Syn:
    """The one synapse: terminal on top, cleft, postsynaptic spine below. self.k is the cumulative zoom."""

    def __init__(self, cx=CX0, mg=True, depol=False, ampa_set=("A1", "A2", "A3"), vesicles=True):
        self.cx, self.k = cx, 1.0
        col = PINK if depol else GREY
        self.term = RoundedRectangle(corner_radius=0.55, width=6.2, height=1.3, stroke_color=GREY, stroke_width=3,
                                     fill_color=GREY, fill_opacity=0.12).move_to([cx, 2.65, 0])
        self.spine = RoundedRectangle(corner_radius=1.1, width=6.6, height=2.8, stroke_color=col, stroke_width=4,
                                      fill_color=col, fill_opacity=0.07).move_to([cx, 0.1, 0])
        self.mem = RoundedRectangle(corner_radius=0.08, width=6.0, height=0.2, stroke_width=0,
                                    fill_color=col, fill_opacity=0.55).move_to([cx, MEM_Y, 0])
        self.ch = {}
        for name, kind, rx in LAYOUT:
            if kind == "A" and name not in ampa_set:
                continue
            f = ampa if kind == "A" else nmda
            self.ch[name] = f(cx + rx, MEM_Y)
        self.mg = {}
        if mg:
            for name in ("N1", "N2"):
                rx = [r for n, kd, r in LAYOUT if n == name][0]
                self.mg[name] = Circle(radius=0.15, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                                       fill_opacity=0.95).move_to([cx + rx, MEM_Y + 0.22, 0])
        self.ves = VGroup()
        self.glu = VGroup()
        if vesicles:
            for rx in (-2.0, 0.0, 2.0):
                v = Circle(radius=0.22, stroke_color=GREY, stroke_width=2).move_to([cx + rx, 2.3, 0])
                d = Dot(radius=0.09, color=YELLOW).move_to(v)
                self.ves.add(v)
                self.glu.add(d)
        self.all = VGroup(self.term, self.spine, self.mem, *self.ch.values(), *self.mg.values(), self.ves, self.glu)

    # --- geometry that survives zooming ----------------------------------------------------------
    def p(self, rx, ry=0.0):
        """screen point at rx (x, relative to the synapse centre) and ry (relative to the membrane)."""
        c = self.mem.get_center()
        return c + np.array([rx * self.k, ry * self.k, 0])

    def zoom_to(self, k, to):
        """immediate zoom about the membrane centre, which lands on `to`."""
        c = self.mem.get_center()
        self.all.scale(k, about_point=c).shift(np.array(to, float) - c)
        self.k *= k

    def zoom_anim(self, k, to):
        c = self.mem.get_center()
        self.k *= k
        return self.all.animate.scale(k, about_point=c).shift(np.array(to, float) - c)

    def dot(self, kind_color, rx, ry, r=0.1):
        return Dot(radius=r * self.k, color=kind_color).move_to(self.p(rx, ry))


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def bar(x, base, h, color, w=0.6, op=0.85):
    return Rectangle(width=w, height=max(h, 0.02), stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=op).move_to([x, base + max(h, 0.02) / 2, 0])


def baseline(x0, x1, y):
    return Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=3)


def ticks(cx, y, n, gap, color=TEXT):
    xs = (np.arange(n) - (n - 1) / 2) * gap + cx
    return VGroup(*[Line([x, y - 0.14, 0], [x, y + 0.14, 0], color=color, stroke_width=4) for x in xs])


def tag(text, color, size=24, **kw):
    return chip(text, color, size=size, **kw)


class S00Title(TitleCard):
    LESSON = "Synaptic Plasticity"
    TITLE = "One Synapse, Turned Up or Down"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        syn = Syn()
        lab_t = T("Schaffer collateral terminal", 24, GREY).move_to([CX0, 2.95, 0])
        lab_s = T("CA1 pyramidal cell spine", 24, GREY).move_to([CX0, -0.75, 0])
        lab_p = T("rat hippocampal slice", 24, GREY).move_to([CX0, -2.2, 0])
        self.play(FadeIn(syn.all), FadeIn(lab_t), FadeIn(lab_s), FadeIn(lab_p), run_time=0.7)
        self.at("turned up")
        up = Arrow([CX0 - 1.1, -0.2, 0], [CX0 - 1.1, 0.95, 0], buff=0, color=GREEN, stroke_width=10, tip_length=0.4)
        self.play(GrowArrow(up), run_time=0.6)
        self.at("turned down")
        dn = Arrow([CX0 + 1.1, 0.95, 0], [CX0 + 1.1, -0.2, 0], buff=0, color=RED, stroke_width=10, tip_length=0.4)
        self.play(GrowArrow(dn), run_time=0.6)
        self.at("rat hippocampus")
        self.play(FadeOut(up), FadeOut(dn), Indicate(lab_p, color=TEXT, scale_factor=1.15), run_time=0.9)

        # row A: fast train -> increase
        chipA = tag("100 pulses per second", TEXT).move_to([4.0, 3.0, 0])
        tkA = ticks(4.0, 2.42, 15, 0.22)
        baseA = 1.0
        blA = baseline(2.3, 4.7, baseA)
        b0A = bar(2.95, baseA, 0.6, GREY)
        lbA = VGroup(T("before", 22, GREY).move_to([2.95, 0.68, 0]), T("after", 22, GREY).move_to([3.95, 0.68, 0]))
        # row B: slow train -> decrease
        chipB = tag("900 pulses, 1 to 3 Hz", TEXT).move_to([4.0, -0.35, 0])
        tkB = ticks(4.0, -0.9, 5, 0.62)
        baseB = -2.45
        blB = baseline(2.3, 4.7, baseB)
        b0B = bar(2.95, baseB, 0.6, GREY)
        lbB = VGroup(T("before", 22, GREY).move_to([2.95, -2.77, 0]), T("after", 22, GREY).move_to([3.95, -2.77, 0]))

        skn = T("in this sketch", 22, GREY).move_to([4.0, 0.2, 0])
        self.at("fast train")
        self.play(FadeIn(skn), FadeIn(chipA, shift=DOWN * 0.1), run_time=0.4)
        self.play(LaggedStart(*[Create(t) for t in tkA], lag_ratio=0.08), FadeIn(blA), FadeIn(b0A), FadeIn(lbA), run_time=1.0)
        self.at("lasting increase")
        a1 = bar(3.95, baseA, 1.05, GREEN)
        txA = T("lasting\nincrease", 24, GREEN).move_to([5.55, baseA + 0.52, 0])
        self.play(GrowFromEdge(a1, DOWN), FadeIn(txA), run_time=0.7)
        self.at("slow train")
        self.play(FadeIn(chipB, shift=DOWN * 0.1), run_time=0.4)
        self.play(LaggedStart(*[Create(t) for t in tkB], lag_ratio=0.25), FadeIn(blB), FadeIn(b0B), FadeIn(lbB), run_time=1.1)
        self.at("lasting decrease")
        a2 = bar(3.95, baseB, 0.22, RED)
        txB = T("lasting\ndecrease", 24, RED).move_to([5.55, baseB + 0.55, 0])
        self.play(GrowFromEdge(a2, DOWN), FadeIn(txB), run_time=0.7)
        self.at("Same synapse")
        self.play(Indicate(syn.spine, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("What tells")
        q = T("?", 110, GOLD, weight=BOLD).move_to([CX0, 0.45, 0])
        self.play(FadeOut(lab_s), FadeIn(q, scale=1.4), run_time=0.6)
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Gate(SpokenScene):
    def construct(self):
        syn = Syn()
        lab_t = T("Schaffer collateral terminal", 24, GREY).move_to([CX0, 2.95, 0])
        lab_s = T("CA1 pyramidal cell spine", 24, GREY).move_to([CX0, -0.5, 0])
        self.add(syn.all, lab_t, lab_s)
        self.wait(0.3)
        self.at("releases glutamate")
        # glutamate leaves the vesicles and crosses the cleft to the channels
        dests = ["N1", "A2", "N2", "A3", "A1"]
        starts = [syn.glu[0], syn.glu[1], syn.glu[1], syn.glu[2], syn.glu[0]]
        dots = []
        for dn, st in zip(dests, starts):
            d = Dot(radius=0.1, color=YELLOW).move_to(st.get_center())
            dots.append(d)
        syn.all.add(*dots)
        self.add(*dots)
        moves = []
        for d, dn in zip(dots, dests):
            x = syn.ch[dn].get_center()[0]
            moves.append(d.animate.move_to([x, 1.97, 0]))
        glu_tag = T("glutamate", 24, YELLOW).move_to([3.4, 1.97, 0])
        glu_ln = Line([glu_tag.get_left()[0] - 0.1, 1.97, 0], [dots[3].get_center()[0] + 1.0, 1.97, 0], color=YELLOW, stroke_width=2)
        self.play(*moves, FadeIn(glu_tag), Create(glu_ln), FadeOut(lab_t), FadeOut(syn.glu), run_time=1.3)
        self.at("Two kinds of receptor")
        # zoom to the membrane
        self.play(FadeOut(glu_tag), FadeOut(glu_ln), FadeOut(lab_s),
                  syn.zoom_anim(1.25, [0.0, 1.0, 0]), run_time=1.3)
        self.play(Indicate(VGroup(*syn.ch.values()), color=TEXT, scale_factor=1.06), run_time=0.8)

        la = T("AMPA\nreceptor", 24, BLUE).move_to(syn.p(1.25, -1.05))
        ln_a = Line(la.get_top() + UP * 0.05, syn.p(1.25, -0.4), color=BLUE, stroke_width=2)
        self.at("AMPA receptors carry")
        self.play(FadeIn(la), Create(ln_a),
                  *[syn.ch[n].animate.set_fill(BLUE, 0.85) for n in ("A1", "A2", "A3")], run_time=0.8)
        ln_ = T("NMDA\nreceptor", 24, PURPLE).move_to(syn.p(-1.55, -1.05))
        ln_n = Line(ln_.get_top() + UP * 0.05, syn.p(-1.55, -0.45), color=PURPLE, stroke_width=2)
        self.at("sit beside them")
        self.play(FadeIn(ln_), Create(ln_n), run_time=0.8)
        self.at("magnesium ion")
        lm = T("Mg²⁺", 26, ORANGE).move_to(syn.p(0.35, -1.85))
        ln_m = Line(lm.get_top() + UP * 0.05, syn.mg["N2"].get_bottom() + DOWN * 0.02, color=ORANGE, stroke_width=2)
        self.play(FadeIn(lm), Create(ln_m), Indicate(VGroup(*syn.mg.values()), color=ORANGE, scale_factor=1.5), run_time=1.0)
        self.at("pore stays plugged")
        blk = T("pore plugged", 24, ORANGE).move_to(syn.p(0.35, -2.4))
        self.play(FadeIn(blk), Indicate(VGroup(*syn.mg.values()), color=ORANGE, scale_factor=1.5), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Coincidence(SpokenScene):
    def construct(self):
        syn = Syn()
        dots = [Dot(radius=0.1, color=YELLOW).move_to([syn.ch[n].get_center()[0], 1.97, 0])
                for n in ("N1", "A2", "N2", "A3", "A1")]
        syn.all.add(*dots)
        for n in ("A1", "A2", "A3"):
            syn.ch[n].set_fill(BLUE, 0.85)
        syn.glu.set_opacity(0)
        syn.zoom_to(1.25, [0.0, 1.0, 0])
        self.add(syn.all)
        # carry the labels from the last scene
        la = T("AMPA\nreceptor", 24, BLUE).move_to(syn.p(1.25, -1.05))
        ln_a = Line(la.get_top() + UP * 0.05, syn.p(1.25, -0.4), color=BLUE, stroke_width=2)
        lb = T("NMDA\nreceptor", 24, PURPLE).move_to(syn.p(-1.55, -1.05))
        ln_n = Line(lb.get_top() + UP * 0.05, syn.p(-1.55, -0.45), color=PURPLE, stroke_width=2)
        lm = T("Mg²⁺", 26, ORANGE).move_to(syn.p(0.35, -1.85))
        ln_m = Line(lm.get_top() + UP * 0.05, syn.mg["N2"].get_bottom() + DOWN * 0.02, color=ORANGE, stroke_width=2)
        blk = T("pore plugged", 24, ORANGE).move_to(syn.p(0.35, -2.4))
        olds = VGroup(la, ln_a, lb, ln_n, lm, ln_m, blk)
        self.add(olds)

        # equation strip along the bottom
        c1 = tag("agonists bound", YELLOW, 22)
        plus = T("+", 30, TEXT)
        c2 = tag("depolarized", PINK, 22)
        eq = T("=", 30, TEXT)
        c3 = tag("NMDA receptor passes current", PURPLE, 22)
        row = VGroup(c1, plus, c2, eq, c3).arrange(RIGHT, buff=0.25).move_to([0, -3.1, 0])
        fit(row, max_w=12.2)

        self.at("depolarize the cell")
        self.play(FadeOut(blk), run_time=0.3)
        self.play(syn.spine.animate.set_stroke(PINK).set_fill(PINK, 0.1), syn.mem.animate.set_fill(PINK, 0.6),
                  FadeIn(c2, shift=UP * 0.1), FadeIn(plus), run_time=0.9)
        self.at("while glutamate is bound")
        self.play(FadeIn(c1, shift=UP * 0.1), Indicate(VGroup(*dots), color=YELLOW, scale_factor=1.6), run_time=0.8)
        self.at("driven out")
        outs = [m.animate.move_to(m.get_center() + UP * 0.55 * syn.k + RIGHT * (0.5 if i else -0.5) * syn.k)
                for i, m in enumerate(syn.mg.values())]
        self.play(FadeOut(VGroup(la, ln_a, lb, ln_n, lm, ln_m)), *outs, *[syn.ch[n].animate.set_fill(PURPLE, 0.85) for n in ("N1", "N2")], run_time=1.1)
        self.play(*[m.animate.set_opacity(0.0) for m in syn.mg.values()], run_time=0.5)
        self.at("passes sodium")
        ions = T("Na⁺  K⁺  Ca²⁺", 26, TEXT, t2c={"Ca²⁺": TEAL}).move_to(syn.p(0.35, -2.0))
        ca = []
        rng = np.random.RandomState(3)
        for j in range(8):
            n = "N1" if j % 2 == 0 else "N2"
            rx = -1.55 if n == "N1" else 0.35
            d = syn.dot(TEAL, rx, 0.35, r=0.1)
            ca.append((d, rx, j))
        self.add(*[d for d, _, _ in ca])
        anims = []
        for d, rx, j in ca:
            tx = rx + rng.uniform(-0.5, 0.5)
            ty = -rng.uniform(0.7, 1.6)
            anims.append(Succession(Wait(0.12 * j), d.animate(run_time=1.1).move_to(syn.p(tx, ty))))
        self.play(*anims, FadeIn(ions), run_time=2.2)
        self.at("coincidence detector")
        self.play(FadeIn(eq), FadeIn(c3, shift=UP * 0.1), run_time=0.8)
        self.play(Indicate(row, color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("the blocker")
        apv = tag("APV", TEXT, 24).move_to(syn.p(-0.6, -1.9))
        l1 = inhib(apv.get_top() + UP * 0.02 + LEFT * 0.3, syn.p(-1.55, -0.45), TEXT, 4)
        l2 = inhib(apv.get_top() + UP * 0.02 + RIGHT * 0.3, syn.p(0.35, -0.45), TEXT, 4)
        self.play(FadeOut(row), FadeOut(ions), *[FadeOut(d) for d, _, _ in ca], run_time=0.6)
        self.play(FadeIn(apv, shift=UP * 0.2), Create(l1), Create(l2), run_time=0.9)
        self.at("ordinary response alone")
        t1 = T("ordinary response: unchanged", 24, BLUE).move_to([0, -3.1, 0])
        self.play(FadeIn(t1), Indicate(VGroup(*[syn.ch[n] for n in ("A1", "A2", "A3")]), color=BLUE, scale_factor=1.15), run_time=0.9)
        self.at("fails to produce")
        t2 = T("high-frequency train: no LTP", 24, RED)
        self.play(t1.animate.move_to([0, -2.8, 0]), FadeIn(t2.move_to([0, -3.3, 0])), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pre_open_syn(ampa_set=("A1", "A2", "A3"), depol=True):
    s = Syn(mg=False, depol=depol, ampa_set=ampa_set, vesicles=False)
    for n in ("N1", "N2"):
        s.ch[n].set_fill(PURPLE, 0.85)
    return s


def scatter(syn, n, seed, y0=-0.35, y1=-1.35, span=2.9):
    rng = np.random.RandomState(seed)
    return [(rng.uniform(-span, span - 0.3), -rng.uniform(-y0, -y1)) for _ in range(n)]


class S04Up(SpokenScene):
    def construct(self):
        syn = pre_open_syn()
        self.add(syn.all)

        capCa = tag("large Ca²⁺ rise", TEAL, 24).move_to([4.0, 3.0, 0])
        self.at("large rise of calcium")
        self.play(FadeIn(capCa, shift=DOWN * 0.1), run_time=0.4)
        pos = [(-2.4 + 0.5 * i % 3, 0) for i in range(0)]
        rng = np.random.RandomState(5)
        dots = []
        for j in range(14):
            rx = -1.55 if j % 2 == 0 else 0.35
            d = Dot(radius=0.1, color=TEAL).move_to(syn.p(rx, 0.3))
            dots.append((d, rng.uniform(-2.7, 2.2), -rng.uniform(0.6, 2.3)))
        self.add(*[d for d, _, _ in dots])
        self.play(*[Succession(Wait(0.07 * i), d.animate(run_time=0.9).move_to(syn.p(tx, ty)))
                    for i, (d, tx, ty) in enumerate(dots)], run_time=2.0)
        self.at("trigger for")
        capL = tag("LTP", GREEN, 26).move_to([4.0, 2.25, 0])
        arr1 = Arrow(capCa.get_bottom(), capL.get_top(), buff=0.08, color=GREEN, stroke_width=4, tip_length=0.2)
        self.play(GrowArrow(arr1), FadeIn(capL), run_time=0.7)
        self.at("recruits")
        kin = tag("CaMKII", GREEN, 28).move_to(syn.p(-0.3, -1.4))
        # kinase sits in the middle of the cloud
        self.play(FadeIn(kin, scale=0.8), run_time=0.7)
        self.play(Indicate(kin, color=GREEN, scale_factor=1.12), run_time=0.6)
        self.at("stay active")
        self.play(Indicate(kin, color=GREEN, scale_factor=1.12), run_time=0.7)
        self.at("after calcium falls")
        self.play(*[FadeOut(d) for d, _, _ in dots], FadeOut(capCa), FadeOut(arr1),
                  kin[1].animate.set_fill(GREEN, 0.4), run_time=1.2)
        self.at("Expression includes")
        news = []
        for nm, rx in NEWSLOTS:
            a = ampa(syn.p(rx)[0], syn.p(rx)[1], 1.0, 0.85)
            a.set_color(GREEN)
            a.set_fill(GREEN, 0.9)
            news.append(a)
        self.play(*[GrowFromCenter(a) for a in news], run_time=0.9)
        lab = T("more AMPA\nreceptors", 24, GREEN).move_to(syn.p(1.7, -1.0))
        self.play(FadeIn(lab), *[a.animate.set_color(BLUE).set_fill(BLUE, 0.85) for a in news], run_time=0.9)
        self.at("same test pulse")
        base = -1.45
        bl = baseline(2.3, 5.8, base)
        b0 = bar(3.1, base, 1.0, GREY, w=0.8)
        lb = VGroup(T("before", 22, GREY).move_to([3.1, base - 0.3, 0]), T("after", 22, GREY).move_to([4.5, base - 0.3, 0]))
        ttl = T("same test pulse:\nresponse", 24, TEXT).move_to([4.0, 1.25, 0])
        note = T("relative heights, in this sketch", 22, GREY).move_to([4.0, base - 0.85, 0])
        self.play(FadeIn(bl), FadeIn(b0), FadeIn(lb), FadeIn(ttl), FadeIn(note), run_time=0.7)
        self.at("bigger response")
        a1 = bar(4.5, base, 2.0, GREEN, w=0.8)
        self.play(GrowFromEdge(a1, DOWN), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Down(SpokenScene):
    def construct(self):
        syn = pre_open_syn(depol=False)
        self.add(syn.all)
        self.wait(0.2)
        self.at("the slow train")
        chipB = tag("900 pulses, 1 to 3 Hz", TEXT).move_to([4.0, 3.0, 0])
        tkB = ticks(4.0, 2.42, 5, 0.62)
        self.play(FadeIn(chipB, shift=DOWN * 0.1), LaggedStart(*[Create(t) for t in tkB], lag_ratio=0.25), run_time=1.2)
        self.at("modest, prolonged")
        capCa = tag("modest, prolonged\nCa²⁺ rise", TEAL, 24).move_to([4.0, 1.5, 0])
        self.play(FadeIn(capCa, shift=DOWN * 0.1), run_time=0.4)
        rng = np.random.RandomState(9)
        dots = []
        for j in range(4):
            rx = -1.55 if j % 2 == 0 else 0.35
            d = Dot(radius=0.1, color=TEAL).move_to(syn.p(rx, 0.3))
            dots.append((d, rng.uniform(-2.2, 1.6), -rng.uniform(0.7, 1.9)))
        self.add(*[d for d, _, _ in dots])
        self.play(*[Succession(Wait(0.55 * i), d.animate(run_time=1.0).move_to(syn.p(tx, ty)))
                    for i, (d, tx, ty) in enumerate(dots)], run_time=3.0)
        self.at("protein phosphatases")
        pho = tag("phosphatases", RED, 28).move_to(syn.p(-0.3, -1.4))
        self.play(FadeIn(pho, scale=0.8), run_time=0.7)
        self.at("rather than")
        ghost = tag("less CaMKII", GREY, 24).move_to(syn.p(1.95, -1.75))
        ghost.set_opacity(0.55)
        self.play(FadeIn(ghost), run_time=0.7)
        self.at("removing")
        outs = []
        for n in ("A1", "A3"):
            c = syn.ch[n].get_center()
            outs.append(syn.ch[n].animate.set_color(RED).set_fill(RED, 0.4))
        self.play(*outs, FadeOut(VGroup(*[d for d, _, _ in dots])), run_time=0.6)
        pinch = []
        for n in ("A1", "A3"):
            c = syn.ch[n].get_center()
            pinch.append(syn.ch[n].animate.scale(0.45).move_to(c + DOWN * 0.95))
        lab = T("AMPA receptors removed", 24, RED).move_to(syn.p(-0.2, -2.4))
        self.play(*pinch, FadeIn(lab), run_time=1.2)
        self.at("same test pulse")
        base = -1.2
        bl = baseline(1.8, 6.1, base)
        b0 = bar(2.2, base, 1.0, GREY, w=0.7)
        b0o = bar(4.6, base, 1.0, GREY, w=0.7)
        lb = VGroup(T("before", 22, GREY).move_to([2.2, base - 0.28, 0]), T("after", 22, GREY).move_to([3.2, base - 0.28, 0]),
                    T("before", 22, GREY).move_to([4.6, base - 0.28, 0]), T("after", 22, GREY).move_to([5.6, base - 0.28, 0]))
        names = VGroup(T("conditioned\ninput", 22, TEXT).move_to([2.7, base - 1.0, 0]),
                       T("other\ninput", 22, TEXT).move_to([5.1, base - 1.0, 0]))
        note = T("relative heights, in this sketch", 22, GREY).move_to([4.0, 0.55, 0])
        self.play(FadeOut(chipB), FadeOut(tkB), FadeOut(capCa), FadeIn(bl), FadeIn(b0), FadeIn(b0o), FadeIn(lb), FadeIn(note), run_time=0.8)
        self.at("smaller response")
        a1 = bar(3.2, base, 0.4, RED, w=0.7)
        self.play(GrowFromEdge(a1, DOWN), FadeIn(names[0]), run_time=0.6)
        self.at("only at")
        a2 = bar(5.6, base, 1.0, GREY, w=0.7)
        self.play(GrowFromEdge(a2, DOWN), FadeIn(names[1]), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        N = 48
        W, H, Y = 11.0, 0.6, 0.55
        segs = VGroup(*[Rectangle(width=W / N, height=H, stroke_width=0, fill_opacity=0.85,
                                  fill_color=interpolate_color(ManimColor(RED), ManimColor(GREEN), i / (N - 1)))
                        for i in range(N)]).arrange(RIGHT, buff=0).move_to([0, Y, 0])
        rim = RoundedRectangle(corner_radius=0.12, width=W + 0.1, height=H + 0.1, stroke_color=GREY, stroke_width=3).move_to(segs)
        wire = Line([-W / 2 - 1.1, Y, 0], [-W / 2, Y, 0], color=GREY, stroke_width=6)
        wire_l = T("one input", 22, GREY).move_to([-W / 2 - 0.1, Y + 0.7, 0])
        wire_l.shift(RIGHT * 0.1)
        knob = Circle(radius=0.42, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([0, Y, 0])
        self.at("dimmer switch")
        self.play(FadeIn(segs), Create(rim), Create(wire), FadeIn(wire_l), FadeIn(knob, scale=0.7), run_time=1.2)
        top = T("Ca²⁺ through the NMDA receptor", 32, TEAL).move_to([0, 2.7, 0])
        left = VGroup(T("LTD", 40, RED, weight=BOLD), T("AMPA receptors removed", 24, RED)).arrange(DOWN, buff=0.12)
        right = VGroup(T("LTP", 40, GREEN, weight=BOLD), T("AMPA receptors added", 24, GREEN)).arrange(DOWN, buff=0.12)
        left.move_to([-3.4, -0.45, 0]).align_to([-W / 2, 0, 0], LEFT)
        right.move_to([3.4, -0.45, 0]).align_to([W / 2, 0, 0], RIGHT)
        self.at("How much calcium")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.5)
        self.at("decides the direction")
        self.play(knob.animate.move_to([-W / 2 + 0.7, Y, 0]), FadeIn(left), run_time=1.0)
        self.play(knob.animate.move_to([W / 2 - 0.7, Y, 0]), FadeIn(right), run_time=1.4)
        self.at("is a model")
        mod = tag("a model: canonical", GREY, 24).move_to([0, 1.75, 0])
        self.play(FadeIn(mod, shift=DOWN * 0.1), knob.animate.move_to([0, Y, 0]), run_time=0.9)
        self.at("No single calcium threshold")
        q = T("?", 56, GOLD, weight=BOLD).move_to([0, Y, 0])
        nt = T("no single threshold established", 26, GOLD).move_to([0, -1.5, 0])
        self.play(FadeOut(knob), FadeIn(q, scale=1.3), FadeIn(nt), run_time=0.8)
        self.at("a family")
        fam = VGroup(T("LTP is a family of changes", 26, TEXT),
                     T("mossy-fibre LTP, guinea-pig CA3: NMDA-receptor independent", 24, TEXT)).arrange(DOWN, buff=0.15)
        fit(fam, max_w=11.8)
        fam.move_to([0, -2.7, 0])
        self.play(FadeIn(fam, shift=UP * 0.1), run_time=0.9)
        self.at("The same synapse")
        knob2 = Circle(radius=0.42, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([0, Y, 0])
        self.play(FadeOut(q), FadeIn(knob2), run_time=0.4)
        self.at("with its pattern")
        self.play(knob2.animate.move_to([-W / 2 + 0.7, Y, 0]), run_time=0.8)
        self.play(knob2.animate.move_to([W / 2 - 0.7, Y, 0]), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "The same synapse turns up or down with its pattern of activity."
