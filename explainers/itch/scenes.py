"""Which Line Carries the Itch?  (chapter 1, Biochemistrypedia explainer)

One world: chips and droplets at left, a teal sensory cell or population in the middle,
schematic gauges at right. Colour map: histamine gold, chloroquine blue, itch-route neurons teal,
pain-related output red, inhibition purple, neutral tissue white.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

HIST = "#F2B632"
CHLQ = BLUE
PURP = "#B58CD9"
PAIN = RED
NEUT = TEXT


def lab(text, size=28, color=TEXT, **kw):
    return T(text, size=size, color=color, weight=BOLD, **kw)


def sub(text, size=26, color=TEXT, **kw):
    return T(text, size=size, color=color, **kw)


class Flow(VGroup):
    """Drifting droplets along a line; limit cuts the stream, level fades it."""

    def __init__(self, p0, p1, color, n=4, speed=0.2, r=0.08, wob=0.1, seed=0, level=1.0):
        super().__init__()
        self.p0 = np.array(p0, float)
        self.p1 = np.array(p1, float)
        self.limit = 1.0
        self.level = level
        self.t = 0.0
        self.speed = speed
        self.wob = wob
        rng = np.random.RandomState(seed)
        self.ph = [(i + rng.rand() * 0.5) / n for i in range(n)]
        self.off = rng.rand(n) * 6.28
        for _ in range(n):
            self.add(Dot(radius=r, color=color, stroke_width=0))
        self.add_updater(Flow._upd)
        Flow._upd(self, 0)

    def _upd(self, dt=0):
        self.t += dt
        d = self.p1 - self.p0
        perp = np.array([-d[1], d[0], 0.0])
        perp = perp / (np.linalg.norm(perp) + 1e-9)
        for i, m in enumerate(self.submobjects):
            u = (self.ph[i] + self.t * self.speed) % 1.0
            m.move_to(self.p0 + d * u + perp * self.wob * np.sin(self.off[i] + self.t * 2.0))
            op = (np.sin(np.pi * u) ** 0.5) * (1.0 if u <= self.limit else 0.0) * self.level
            m.set_opacity(float(op))


def fl_to(fl, level, rt=1.0):
    l0 = fl.level
    return UpdateFromAlphaFunc(fl, lambda m, a: setattr(m, "level", l0 + (level - l0) * a), run_time=rt)


def fl_limit(fl, lim, rt=1.0):
    l0 = fl.limit
    return UpdateFromAlphaFunc(fl, lambda m, a: setattr(m, "limit", l0 + (lim - l0) * a), run_time=rt)


class Gauge(VGroup):
    def __init__(self, color, w=2.6, h=0.5, v=0.8):
        super().__init__()
        self.tr = ValueTracker(v)
        self.box = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_opacity=0)
        self.fill = Rectangle(width=w * max(v, 0.012), height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        self.fill.align_to(self.box, LEFT)
        self.add(self.box, self.fill)
        self.add_updater(Gauge._upd)

    def _upd(self):
        v = max(self.tr.get_value(), 0.012)
        self.fill.stretch_to_fit_width(self.box.width * v)
        self.fill.align_to(self.box, LEFT)


def blk(color, at, w=0.45, h=0.95):
    b = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=TEXT, stroke_width=2,
                         fill_color=color, fill_opacity=0.95).move_to([at[0], at[1], 0])
    b.set_z_index(5)
    return b


def xmark(mob, color=RED, w=7):
    r = 0.5 * min(mob.width, mob.height) + 0.1
    c = mob.get_center()
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]), color=color, stroke_width=w)).set_z_index(8)


def dashed(mob, n=36, **kw):
    return DashedVMobject(mob, num_dashes=n, **kw)


# ---------------------------------------------------------------- shared pictures
NY = [1.5, 0.0, -1.5]


def neuron(y):
    fork = VGroup(*[Line([-2.7, y, 0], [-3.5, y + dy, 0], color=TEAL, stroke_width=4) for dy in (0.32, 0.0, -0.32)])
    axon = Line([-2.7, y, 0], [-0.42, y, 0], color=TEAL, stroke_width=4)
    soma = Circle(radius=0.42, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.35).move_to([0, y, 0])
    cen = Line([0.42, y, 0], [4.2, y, 0], color=TEAL, stroke_width=4)
    return VGroup(fork, axon, cen, soma)


def skin_world():
    skin = Rectangle(width=4.35, height=7.0, stroke_color=GREY, stroke_width=3, fill_color=TEXT, fill_opacity=0.08)
    skin.move_to([-4.575, 0, 0])
    epi = Rectangle(width=0.9, height=7.0, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([-6.3, 0, 0])
    skin_l = sub("skin", 28, TEXT).rotate(PI / 2).move_to([-6.3, 0, 0])
    cord = RoundedRectangle(corner_radius=0.25, width=2.4, height=6.0, stroke_color=GREY, stroke_width=3,
                            fill_color=TEXT, fill_opacity=0.08).move_to([5.4, 0, 0])
    cord_l = VGroup(sub("spinal", 28), sub("cord", 28)).arrange(DOWN, buff=0.05).move_to([5.4, 2.35, 0])
    ns = VGroup(*[neuron(y) for y in NY])
    return skin, epi, skin_l, cord, cord_l, ns


def skin_flows(gold=True, blue=True, level=1.0):
    gs, bs = VGroup(), VGroup()
    for i, y in enumerate(NY):
        if gold:
            gs.add(Flow([-5.6, y + 0.5, 0], [-3.5, y + 0.12, 0], HIST, seed=i, level=level))
        if blue:
            bs.add(Flow([-5.6, y - 0.5, 0], [-3.5, y - 0.12, 0], CHLQ, seed=10 + i, level=level))
    return gs, bs


CELL = dict(c=[0.7, 0, 0], w=4.0, h=5.8)


def cell_body():
    return RoundedRectangle(corner_radius=0.7, width=4.0, height=5.8, stroke_color=TEAL, stroke_width=5,
                            fill_color=TEAL, fill_opacity=0.18).move_to([0.7, 0, 0])


def gauge_pair(c1, c2, v1, v2, head="scratching", names=("", "")):
    g1 = Gauge(c1, 2.6, 0.5, v1).move_to([5.2, 1.4, 0])
    g2 = Gauge(c2, 2.6, 0.5, v2).move_to([5.2, -1.4, 0])
    h = VGroup(lab(head, 28), sub("schematic", 22, GREY)).arrange(DOWN, buff=0.08).move_to([5.2, 2.7, 0])
    n1 = sub(names[0], 26, c1).move_to([5.2, 0.85, 0]) if names[0] else VGroup()
    n2 = sub(names[1], 26, c2).move_to([5.2, -1.95, 0]) if names[1] else VGroup()
    return g1, g2, h, n1, n2


def chip_at(text, color, at):
    c = chip(text, color, size=28)
    c.move_to(at)
    return c


# population view
CYS = [2.55, 0.85, -0.85, -2.55]


def pop_cells(teal=3):
    cs = VGroup()
    for i, y in enumerate(CYS):
        col = TEAL if i < teal else GREY
        cs.add(Circle(radius=0.78, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.25).move_to([0.6, y, 0]))
    return cs


def pop_box():
    return dashed(RoundedRectangle(corner_radius=0.3, width=2.1, height=5.2, color=TEAL, stroke_width=4).move_to([0.6, 0.85, 0]), 44)


def pop_label():
    return VGroup(lab("MrgprA3", 30, TEAL), sub("neurons", 28, TEAL)).arrange(DOWN, buff=0.05).move_to([2.85, 0.0, 0])


class Pop:
    """the population world shared by s02 to s04"""

    def __init__(self, scene, question=True, level=1.0):
        self.cells = pop_cells()
        self.box = pop_box()
        self.lbl = pop_label()
        self.ch = chip_at("histamine", HIST, [-5.2, 1.4, 0])
        self.cc = chip_at("chloroquine", CHLQ, [-5.2, -1.4, 0])
        self.fa = Flow([-4.0, 1.4, 0], [-0.55, 1.4, 0], HIST, n=5, seed=1, level=level)
        self.fb = Flow([-4.0, -1.4, 0], [-0.55, -1.4, 0], CHLQ, n=5, seed=2, level=level)
        self.oa = Flow([1.45, 1.4, 0], [3.7, 1.4, 0], HIST, n=3, seed=3, level=level)
        self.ob = Flow([1.45, -1.4, 0], [3.7, -1.4, 0], CHLQ, n=3, seed=4, level=level)
        self.g1, self.g2, self.head, self.n1, self.n2 = gauge_pair(HIST, CHLQ, 0.8, 0.8, names=("histamine", "chloroquine"))
        self.all = VGroup(self.cells, self.box, self.lbl, self.ch, self.cc, self.fa, self.fb, self.oa, self.ob,
                          self.g1, self.g2, self.head, self.n1, self.n2)
        scene.add(self.g1.tr, self.g2.tr)


def question_card():
    q = VGroup(lab("Will histamine", 40, HIST), lab("scratching remain?", 40, HIST)).arrange(DOWN, buff=0.1)
    return q.move_to([-3.4, 3.0, 0])


def paw(color, s=1.0):
    pad = Ellipse(width=0.9, height=0.75, stroke_width=0, fill_color=color, fill_opacity=0.95)
    toes = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([dx, dy, 0])
                    for dx, dy in [(-0.45, 0.55), (-0.15, 0.72), (0.15, 0.72), (0.45, 0.55)]])
    return VGroup(pad, toes).scale(s)


def scratch_icon(color=TEAL, s=1.0):
    p = paw(color, s)
    lines = VGroup(*[Line([-0.55 + k * 0.55, 1.1, 0], [-0.35 + k * 0.55, 1.6, 0], color=color, stroke_width=5) for k in range(3)]).scale(s)
    return VGroup(p, lines)


def wipe_icon(color=PAIN, s=1.0):
    p = paw(color, s)
    arc = Arc(radius=1.05 * s, start_angle=PI * 0.85, angle=-PI * 0.7, color=color, stroke_width=5).shift(DOWN * 0.1 * s)
    arc.add_tip(tip_length=0.22)
    return VGroup(p, arc)


# ================================================================ s00
class S00Hook(SpokenScene):
    def construct(self):
        skin, epi, skin_l, cord, cord_l, ns = skin_world()
        gs, bs = skin_flows()
        for f in bs:
            f.level = 0.0
        self.add(gs, bs)
        self.play(FadeIn(skin), FadeIn(epi), FadeIn(skin_l), FadeIn(cord), FadeIn(cord_l), FadeIn(ns), run_time=1.4)
        gl = VGroup(lab("histamine", 30, HIST), sub("scratching normal", 28, HIST)).arrange(DOWN, buff=0.08).move_to([-4.5, 3.0, 0])
        self.at("histamine")
        self.play(FadeIn(gl, shift=DOWN * 0.15), run_time=0.7)
        self.at("yet")
        self.play(*[fl_to(f, 1.0, 1.2) for f in bs], run_time=1.2)
        bl = VGroup(sub("scratching much less", 28, CHLQ), lab("chloroquine", 30, CHLQ)).arrange(DOWN, buff=0.08).move_to([-4.5, -3.0, 0])
        self.at("chloroquine")
        self.play(FadeIn(bl, shift=UP * 0.15), run_time=0.7)
        # question beat
        q = lab("Two neurons, or two inputs?", 34, TEXT).move_to([1.7, 3.4, 0])
        self.at("did one experiment")
        self.play(FadeIn(q), run_time=0.6)
        self.at("separate two neurons")
        self.play(Indicate(ns[0][3], color=TEAL, scale_factor=1.35), Indicate(ns[1][3], color=TEAL, scale_factor=1.35), run_time=1.6)
        self.at("only two inputs")
        self.play(Indicate(gl[0], color=HIST, scale_factor=1.2), Indicate(bl[1], color=CHLQ, scale_factor=1.2), run_time=1.6)
        # pathway beat
        title = T("Which Line Carries the Itch?", 32, TEXT, font=TITLE_FONT).move_to([1.7, 3.4, 0])
        self.at("watch one skin")
        self.play(FadeOut(q, run_time=0.4))
        self.play(FadeIn(title), ShowPassingFlash(ns[1].copy().set_stroke(TEAL, 10), time_width=0.5, run_time=2.0), run_time=1.0)
        self.at("gold histamine and blue")
        self.play(Indicate(gl[0], color=HIST, scale_factor=1.2), run_time=0.8)
        self.play(Indicate(bl[1], color=CHLQ, scale_factor=1.2), run_time=0.8)
        pl = lab("sensory neurons", 30, TEAL).move_to([0.2, 2.55, 0])
        self.at("approach the same")
        self.play(FadeIn(pl, shift=DOWN * 0.1), *[Indicate(ns[i][3], color=TEAL, scale_factor=1.3) for i in range(3)], run_time=1.8)
        self.finish()


# ================================================================ s01
class S01ReceptorRoute(SpokenScene):
    def construct(self):
        skin, epi, skin_l, cord, cord_l, ns = skin_world()
        gs, bs = skin_flows()
        old = VGroup(skin, epi, skin_l, cord, cord_l, ns[0], ns[2], ns[1][0], ns[1][1], ns[1][2])
        self.add(old, ns[1][3], gs, bs)
        # build the cell view
        cell = cell_body()
        ch = chip_at("histamine", HIST, [-5.2, 1.4, 0])
        cc = chip_at("chloroquine", CHLQ, [-5.2, -1.4, 0])
        fa = Flow([-4.0, 1.4, 0], [-1.7, 1.4, 0], HIST, n=4, seed=1, level=0)
        fb = Flow([-4.0, -1.4, 0], [-1.7, -1.4, 0], CHLQ, n=4, seed=2, level=0)
        oa = Flow([-0.9, 1.4, 0], [3.7, 1.4, 0], HIST, n=5, seed=3, level=0)
        ob = Flow([-0.9, -1.4, 0], [3.7, -1.4, 0], CHLQ, n=5, seed=4, level=0)
        ba = blk(HIST, [-1.3, 1.4])
        bb = blk(CHLQ, [-1.3, -1.4])
        g1, g2, head, n1, n2 = gauge_pair(HIST, CHLQ, 0.8, 0.8, names=("histamine", "chloroquine"))
        self.add(g1.tr, g2.tr)
        self.play(FadeOut(old), FadeOut(gs), FadeOut(bs), ReplacementTransform(ns[1][3], cell), run_time=1.3)
        self.add(fa, fb, oa, ob)
        self.play(FadeIn(ch), FadeIn(cc), FadeIn(ba), FadeIn(bb), FadeIn(g1), FadeIn(g2), FadeIn(head), FadeIn(n1), FadeIn(n2),
                  *[fl_to(f, 1.0, 1.0) for f in (fa, fb, oa, ob)], run_time=1.2)
        lb = lab("Mrgpr", 28, CHLQ).move_to([-0.1, -0.7, 0])
        lg = lab("receptor", 28, HIST).move_to([-0.1, 2.05, 0])
        self.at("mrgpr")
        self.play(FadeIn(lb), FadeIn(lg), run_time=0.6)
        self.at("receptor genes")
        self.play(FadeOut(bb, scale=0.6), FadeIn(xmark(bb)), run_time=1.0)
        self.at("blue chloroquine")
        self.play(fl_limit(ob, 0.0, 1.4), run_time=1.4)
        self.at("so scratching")
        self.play(g2.tr.animate.set_value(0.15), run_time=1.6)
        self.at("gold histamine scratching")
        self.play(Indicate(g1, color=HIST, scale_factor=1.08), run_time=1.5)
        t1 = lab("two routes separated", 32, TEXT).move_to([0.7, 3.4, 0])
        self.at("the intervention separated")
        self.play(FadeIn(t1), Indicate(ba, color=HIST), run_time=1.5)
        t2 = lab("neurons: not yet separated", 32, TEAL).move_to([0.7, 3.4, 0])
        self.at("it did not yet")
        self.play(FadeOut(t1), FadeIn(t2), Indicate(cell, color=TEAL, scale_factor=1.04), run_time=1.6)
        self.finish()


# ================================================================ s01b
class S01bChannels(SpokenScene):
    def construct(self):
        cell = cell_body()
        ch = chip_at("histamine", HIST, [-5.2, 1.4, 0])
        cc = chip_at("chloroquine", CHLQ, [-5.2, -1.4, 0])
        fa = Flow([-4.0, 1.4, 0], [-1.7, 1.4, 0], HIST, n=4, seed=1)
        fb = Flow([-4.0, -1.4, 0], [-1.7, -1.4, 0], CHLQ, n=4, seed=2)
        oa = Flow([-0.9, 1.4, 0], [1.2, 1.4, 0], HIST, n=3, seed=3)
        oa2 = Flow([2.0, 1.4, 0], [3.7, 1.4, 0], HIST, n=2, seed=5)
        ob = Flow([-0.9, -1.4, 0], [1.2, -1.4, 0], CHLQ, n=3, seed=4)
        ob2 = Flow([2.0, -1.4, 0], [3.7, -1.4, 0], CHLQ, n=2, seed=6)
        ba = blk(HIST, [-1.3, 1.4])
        bb = blk(CHLQ, [-1.3, -1.4])
        g2 = Gauge(CHLQ, 2.6, 0.5, 0.8).move_to([5.2, -1.4, 0])
        head = VGroup(lab("scratching", 28), sub("schematic", 22, GREY)).arrange(DOWN, buff=0.08).move_to([5.2, -0.45, 0])
        self.add(g2.tr)
        self.add(cell, ch, cc, fa, fb, oa, oa2, ob, ob2, ba, bb, g2, head)
        # channel machinery appears unlabelled
        cog = Star(n=8, outer_radius=0.45, inner_radius=0.33, stroke_color=TEXT, stroke_width=2, fill_color=GREY, fill_opacity=0.9).move_to([0.0, 1.4, 0]).set_z_index(5)
        cog_spin = lambda m, dt: m.rotate(0.9 * dt)
        trpv = blk(GREY, [1.6, 1.4], 0.45, 1.0)
        trpa = blk(GREY, [1.6, -1.4], 0.45, 1.0)
        self.at("channel machinery")
        self.play(FadeIn(cog), FadeIn(trpv), FadeIn(trpa), run_time=1.2)
        cog.add_updater(cog_spin)
        self.at("histamine itch")
        self.play(Indicate(ch, color=HIST), run_time=1.2)
        l_cog = lab("PLC-β3", 26, HIST).move_to([0.0, 0.75, 0])
        self.at("plc beta 3")
        self.play(FadeIn(l_cog), cog.animate.set_fill(HIST, 0.95), run_time=0.8)
        l_v = lab("TRPV1", 28, HIST).move_to([1.6, 2.1, 0])
        self.at("trpv1")
        self.play(FadeIn(l_v), trpv.animate.set_fill(HIST, 0.95), run_time=0.8)
        self.at("chloroquine and")
        self.play(Indicate(cc, color=CHLQ), run_time=1.0)
        bam = chip_at("BAM8-22", CHLQ, [-2.4, -3.4, 0])
        self.at("b")
        self.play(FadeIn(bam, shift=UP * 0.2), run_time=0.6)
        arr = Arrow([-1.3, -3.3, 0], [1.3, -2.15, 0], buff=0, color=CHLQ, stroke_width=5, tip_length=0.18)
        self.play(GrowArrow(arr), trpa.animate.set_fill(CHLQ, 0.95), run_time=0.8)
        self.at("scratching instead")
        self.play(Indicate(g2, color=CHLQ, scale_factor=1.06), run_time=1.2)
        l_a = lab("TRPA1", 28, CHLQ).move_to([1.6, -0.7, 0])
        self.at("falls markedly")
        self.play(FadeIn(l_a), g2.tr.animate.set_value(0.2), run_time=0.9)
        self.at("without")
        self.play(FadeOut(trpa, scale=0.6), FadeIn(xmark(trpa)), fl_limit(ob2, 0.0, 1.0), run_time=1.0)
        self.finish()


# ================================================================ s02 / s03
class S02Predict(SpokenScene):
    def construct(self):
        P = Pop(self)
        cell = cell_body()
        ch = chip_at("histamine", HIST, [-5.2, 1.4, 0])
        self.add(cell)
        # transition: cell view -> population
        self.play(FadeOut(cell, scale=0.5), FadeIn(P.cells), FadeIn(P.ch), FadeIn(P.cc), FadeIn(P.g1), FadeIn(P.g2),
                  FadeIn(P.head), FadeIn(P.n1), FadeIn(P.n2), run_time=1.3)
        self.add(P.fa, P.fb, P.oa, P.ob)
        self.at("marked by")
        self.play(FadeIn(P.box), FadeIn(P.lbl), run_time=1.0)
        q = question_card()
        self.at("what should happen")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.8)
        self.at("predict before")
        self.play(*[Indicate(c, color=TEAL, scale_factor=1.18) for c in P.cells[:3]], run_time=1.8)
        self.at("does the gold")
        self.play(Indicate(P.ch, color=HIST, scale_factor=1.15), Indicate(P.g1, color=HIST, scale_factor=1.08), run_time=2.0)
        self.finish()


class S03Pause(NarratedScene):
    def construct(self):
        P = Pop(self)
        self.add(P.all, question_card())
        self.finish()


# ================================================================ s04
class S04Ablation(SpokenScene):
    def construct(self):
        P = Pop(self)
        q = question_card()
        self.add(P.all, q)
        self.play(FadeOut(q), FadeOut(P.cells[:3]), FadeOut(P.box), FadeOut(P.lbl), fl_to(P.fa, 0, 1.4), fl_to(P.fb, 0, 1.4),
                  fl_to(P.oa, 0, 1.4), fl_to(P.ob, 0, 1.4), run_time=1.5)
        self.at("also")
        self.play(P.g1.tr.animate.set_value(0.15), P.g2.tr.animate.set_value(0.15), run_time=1.6)
        cA = VGroup(lab("Receptor deletion", 30, TEXT), sub("one input lost", 28, CHLQ)).arrange(DOWN, buff=0.1).move_to([-0.1, 1.2, 0])
        cB = VGroup(lab("Cell ablation", 30, TEXT), sub("every input lost", 28, TEAL)).arrange(DOWN, buff=0.1).move_to([-0.1, -1.2, 0])
        self.at("removing a receptor")
        self.play(FadeIn(cA, shift=UP * 0.15), run_time=0.8)
        self.at("removing its whole")
        self.play(FadeIn(cB, shift=UP * 0.15), run_time=0.8)
        self.at("are different")
        self.play(Indicate(cA, color=CHLQ, scale_factor=1.1), Indicate(cB, color=TEAL, scale_factor=1.1), run_time=1.6)
        # several inputs
        ghost = dashed(Circle(radius=1.3, color=TEAL, stroke_width=4).move_to([0.4, 0, 0]), 32)
        ins = VGroup()
        fls = VGroup()
        for y, col, sd in [(1.4, HIST, 1), (0.45, TEXT, 2), (-0.45, TEXT, 3), (-1.4, CHLQ, 4)]:
            ins.add(Arrow([-3.4, y, 0], [-0.95, y * 0.6, 0], buff=0, color=col, stroke_width=5, tip_length=0.2))
            fls.add(Flow([-3.4, y, 0], [-1.0, y * 0.6, 0], col, n=3, seed=int(sd) + 20, level=0.0))
        sev = lab("several inputs", 30, TEXT).move_to([0.4, 1.95, 0])
        self.at("the neurons receive")
        self.play(FadeOut(cA), FadeOut(cB), FadeIn(ghost), FadeIn(ins), FadeIn(sev), run_time=1.0)
        self.add(fls)
        self.play(*[fl_to(f, 1.0, 0.8) for f in fls], run_time=0.8)
        need = lab("needed for much scratching", 30, TEAL).move_to([-3.6, -3.3, 0])
        self.at("ablation shows")
        self.play(FadeOut(ins), FadeOut(sev), FadeOut(fls), FadeIn(xmark(ghost)), run_time=1.0)
        self.play(FadeIn(need), Indicate(P.g1, color=HIST, scale_factor=1.08), Indicate(P.g2, color=CHLQ, scale_factor=1.08), run_time=1.8)
        self.finish()


# ================================================================ s05
def rescue_cells():
    cs = pop_cells()
    slots, chans = VGroup(), VGroup()
    for i, y in enumerate(CYS):
        s = dashed(Rectangle(width=0.32, height=0.6, color=GREY, stroke_width=3).move_to([-0.18, y, 0]), 16)
        c = Rectangle(width=0.32, height=0.6, stroke_color=TEXT, stroke_width=2, fill_color=GREY, fill_opacity=0.9).move_to([1.38, y, 0])
        slots.add(s)
        chans.add(c)
    return cs, slots, chans


class S05Rescue(SpokenScene):
    def construct(self):
        cells, slots, chans = rescue_cells()
        c0 = pop_cells()
        self.add(c0)
        self.play(FadeOut(c0), FadeIn(cells), run_time=1.0)
        self.play(FadeIn(slots), FadeIn(chans), run_time=0.8)
        l1 = lab("TRPV1 absent", 28, TEXT).move_to([-2.8, 3.0, 0])
        self.at("lacking working")
        self.play(FadeIn(l1), run_time=0.8)
        self.at("restored that channel")
        new = VGroup()
        for i in range(3):
            b = blk(TEAL, [-1.6, CYS[i]], 0.32, 0.6)
            new.add(b)
        self.play(FadeIn(new, shift=LEFT * 0.0), run_time=0.6)
        self.play(*[new[i].animate.move_to([-0.18, CYS[i], 0]) for i in range(3)], run_time=1.4)
        l2 = lab("TRPV1 in teal only", 28, TEAL).move_to([-2.8, 3.0, 0])
        self.at("teal neurons")
        self.play(ReplacementTransform(l1, l2), Indicate(cells[3], color=GREY, scale_factor=1.1), run_time=1.2)
        cap = chip_at("capsaicin", TEXT, [-5.2, 0.0, 0])
        fans = VGroup()
        for i, y in enumerate(CYS):
            f = Flow([-3.9, 0, 0], [-0.55, y, 0], TEXT, n=3, seed=30 + i, level=0.0)
            if i == 3:
                f.limit = 0.7
            fans.add(f)
        self.at("capsaicin could now")
        self.add(fans)
        self.play(FadeIn(cap), *[fl_to(f, 1.0, 1.0) for f in fans], run_time=1.2)
        self.at("only that population")
        self.play(*[cells[i].animate.set_fill(TEAL, 0.6) for i in range(3)], run_time=1.5)
        wipe = wipe_icon(PAIN, 1.0).move_to([5.0, 1.2, 0])
        self.at("the mouse produced")
        self.play(FadeIn(wipe), run_time=0.8)
        sc = scratch_icon(TEAL, 1.0).move_to([5.0, 1.2, 0])
        lt = VGroup(lab("itch-related", 28, TEAL), lab("scratching", 28, TEAL)).arrange(DOWN, buff=0.06).move_to([5.0, -0.5, 0])
        self.at("itch related behavior")
        self.play(ReplacementTransform(wipe, sc), FadeIn(lt), run_time=1.2)
        sc[0].add_updater(lambda m, dt: None)
        sc.t = 0.0

        def jig(m, dt):
            m.t += dt
            m.move_to([5.0 + 0.1 * np.sin(m.t * 9), 1.2 + 0.1 * np.sin(m.t * 5), 0])
        sc.add_updater(jig)
        wl = lab("pain-related wiping", 28, PAIN).move_to([5.0, -1.8, 0])
        self.at("pain related wiping")
        strike = Line(wl.get_left(), wl.get_right(), color=PAIN, stroke_width=5)
        self.play(FadeIn(wl), Create(strike), run_time=1.0)
        self.finish()


# ================================================================ s06
class S06Scope(SpokenScene):
    def construct(self):
        cell = cell_body()
        g1 = Gauge(PAIN, 2.6, 0.5, 0.1).move_to([5.2, 1.4, 0])
        g2 = Gauge(TEAL, 2.6, 0.5, 0.1).move_to([5.2, -1.4, 0])
        head = VGroup(lab("schematic", 26, GREY)).move_to([5.2, 2.7, 0])
        n1 = VGroup(sub("pain-related", 24, PAIN), sub("defense", 24, PAIN)).arrange(DOWN, buff=0.03).move_to([5.2, 0.8, 0])
        n2 = sub("scratching", 26, TEAL).move_to([5.2, -1.95, 0])
        self.add(g1.tr, g2.tr)
        nl = lab("teal neuron", 30, TEAL).move_to([0.7, 0.0, 0])
        amb = Flow([0.7, -2.2, 0], [0.7, 2.2, 0], TEAL, n=6, seed=9, speed=0.08, wob=0.8)
        self.add(amb, nl)
        o1 = Flow([2.0, 1.4, 0], [3.7, 1.4, 0], PAIN, n=3, seed=1, level=0.0)
        o2 = Flow([2.0, -1.4, 0], [3.7, -1.4, 0], TEAL, n=3, seed=2, level=0.0)
        self.play(FadeIn(cell), FadeIn(g1), FadeIn(g2), FadeIn(head), FadeIn(n1), FadeIn(n2), run_time=1.2)
        self.add(o1, o2)
        self.at("these neurons")
        self.play(Indicate(cell, color=TEAL, scale_factor=1.03), run_time=1.2)
        cap = chip_at("capsaicin", TEXT, [-4.6, 0.0, 0])
        fc = Flow([-3.5, 0, 0], [-1.0, 0, 0], TEXT, n=5, seed=3, level=0.0)
        self.add(fc)
        self.at("capsaicin")
        self.play(FadeIn(cap), fl_to(fc, 1.0, 0.8), fl_to(o2, 1.0, 1.0), g2.tr.animate.set_value(0.8), run_time=2.0)
        stamp = VGroup(RoundedRectangle(corner_radius=0.12, width=4.6, height=1.3, stroke_color=TEXT, stroke_width=7, fill_color=BG, fill_opacity=0.9),
                       lab("ITCH ONLY", 52, TEXT)).rotate(-0.14).move_to([0.7, 0, 0]).set_z_index(10)
        self.at("it does not prove")
        self.play(FadeIn(stamp, scale=1.5), run_time=0.5)
        crack = VMobject(color=PAIN, stroke_width=8).set_points_as_corners(
            [[2.85, 0.8, 0], [3.0, 0.3, 0], [2.78, -0.1, 0], [3.05, -0.45, 0], [2.9, -0.9, 0]]).set_z_index(11)
        self.at("means itch")
        self.play(Create(crack), run_time=0.7)
        self.play(stamp.animate.rotate(0.1).shift(DOWN * 0.2).set_opacity(0), FadeOut(crack), run_time=1.0)
        # fast ionotropic
        self.at("later")
        self.play(FadeOut(cap), fl_to(fc, 0, 0.6), g2.tr.animate.set_value(0.1), fl_to(o2, 0, 0.6), run_time=1.0)
        sw = VGroup(RoundedRectangle(corner_radius=0.25, width=1.2, height=0.5, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.5),
                    Circle(radius=0.2, stroke_width=0, fill_color=PAIN, fill_opacity=1)).move_to([-4.6, 1.4, 0])
        sw.t = 0.0

        def tog(m, dt):
            m.t += dt
            m[1].move_to(m[0].get_center() + RIGHT * 0.3 * np.sign(np.sin(m.t * 10)))
        sw.add_updater(tog)
        swl = lab("fast ionotropic", 28, PAIN).move_to([-4.2, 2.3, 0])
        f1 = Flow([-3.7, 1.4, 0], [-1.0, 0.8, 0], PAIN, n=5, seed=5, level=0.0, speed=0.5)
        self.add(f1)
        self.at("fast")
        self.play(FadeIn(sw), FadeIn(swl), fl_to(f1, 1.0, 0.8), run_time=1.0)
        self.at("mostly evoked")
        self.play(g1.tr.animate.set_value(0.8), fl_to(o1, 1.0, 1.0), run_time=2.4)
        dial = VGroup(Circle(radius=0.55, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.15),
                      Line(ORIGIN, UP * 0.5, color=TEAL, stroke_width=6)).move_to([-4.6, -1.4, 0])
        dial[1].set_z_index(6)
        dial.add_updater(lambda m, dt: m[1].rotate(-0.8 * dt, about_point=m[0].get_center()))
        dl = lab("Gq-linked", 28, TEAL).move_to([-4.4, -2.45, 0])
        f2 = Flow([-3.8, -1.4, 0], [-1.0, -0.8, 0], TEAL, n=3, seed=6, level=0.0, speed=0.12)
        self.add(f2)
        self.at("gq")
        self.play(FadeOut(sw), FadeOut(swl), fl_to(f1, 0, 0.6), g1.tr.animate.set_value(0.1), fl_to(o1, 0, 0.6),
                  FadeIn(dial), FadeIn(dl), fl_to(f2, 1.0, 0.8), run_time=1.2)
        self.at("evoked itch")
        self.play(g2.tr.animate.set_value(0.8), fl_to(o2, 1.0, 1.0), run_time=2.0)
        self.finish()


# ================================================================ s07
def mouse_head(H):
    ears = VGroup(*[Circle(radius=0.7, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.10).move_to(H + np.array(p))
                    for p in [(-1.0, 1.55, 0), (0.1, 1.75, 0)]])
    head = Ellipse(width=4.4, height=3.4, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.10).move_to(H)
    eye = Dot(H + np.array([0.7, 0.45, 0]), radius=0.11, color=TEXT)
    nose = Dot(H + np.array([2.15, -0.1, 0]), radius=0.15, color=TEXT)
    wh = VGroup(*[Line(H + np.array([1.9, -0.15, 0]), H + np.array([2.7, -0.15 + k * 0.3, 0]), color=GREY, stroke_width=3) for k in (-1, 0, 1)])
    return VGroup(ears, head, eye, nose, wh)


class S07Assay(SpokenScene):
    def construct(self):
        H = np.array([-3.0, 0.3, 0.0])
        mouse = mouse_head(H)
        cheek = dashed(Circle(radius=0.55, color=TEXT, stroke_width=4).move_to(H + np.array([0.5, -0.6, 0])), 16)
        fore_rest = H + np.array([-0.2, -2.3, 0])
        hind_rest = H + np.array([-1.9, -1.9, 0])
        cheek_c = H + np.array([0.5, -0.6, 0])
        hind = paw(TEAL, 0.7).move_to(hind_rest)
        fore = paw(PAIN, 0.7).move_to(fore_rest)
        hind.act = ValueTracker(0)
        fore.act = ValueTracker(0)
        hind.t = 0.0
        fore.t = 0.0

        def hu(m, dt):
            m.t += dt
            a = m.act.get_value()
            m.move_to(hind_rest + (cheek_c + np.array([0.3 * np.sin(m.t * 13), 0.12 * np.sin(m.t * 7), 0]) - hind_rest) * a)

        def fu(m, dt):
            m.t += dt
            a = m.act.get_value()
            m.move_to(fore_rest + (cheek_c + np.array([0.15, 0.1 * np.sin(m.t * 3), 0]) + np.array([0.55 * np.sin(m.t * 3), 0, 0]) - fore_rest) * a)
        hind.add_updater(hu)
        fore.add_updater(fu)
        self.add(hind.act, fore.act)
        tag = lab("MrgprA3", 30, TEAL).move_to([-3.0, -3.45, 0])
        self.play(Create(mouse), run_time=1.6)
        self.add(hind, fore)
        self.play(FadeIn(tag), run_time=0.8)
        self.at("cheek assay")
        self.play(Create(cheek), run_time=1.0)
        laneA = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.3, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.08).move_to([3.7, 1.5, 0])
        laneB = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.3, stroke_color=PAIN, stroke_width=4, fill_color=PAIN, fill_opacity=0.08).move_to([3.7, -1.5, 0])
        tA = VGroup(lab("hindpaw scratching", 28, TEAL), lab("itch-related output", 28, TEAL)).arrange(DOWN, buff=0.08).move_to([4.3, 1.5, 0])
        tB = VGroup(lab("forelimb wiping", 28, PAIN), lab("pain-related output", 28, PAIN)).arrange(DOWN, buff=0.08).move_to([4.3, -1.5, 0])
        iA = scratch_icon(TEAL, 0.5).move_to([1.6, 1.4, 0])
        iB = wipe_icon(PAIN, 0.5).move_to([1.6, -1.5, 0])
        self.at("hind")
        self.play(FadeIn(laneA), FadeIn(tA), FadeIn(iA), hind.act.animate.set_value(1.0), run_time=1.4)
        self.at("forlim")
        self.play(FadeIn(laneB), FadeIn(tB), FadeIn(iB), fore.act.animate.set_value(1.0), hind.act.animate.set_value(0.0), run_time=1.4)
        self.at("those readouts")
        self.play(Indicate(tA, color=TEAL, scale_factor=1.06), Indicate(tB, color=PAIN, scale_factor=1.06), run_time=1.8)
        bub = VGroup(Ellipse(width=2.8, height=1.1, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1), sub("sensation?", 28, TEXT)).move_to([-0.7, 3.15, 0])
        self.at("not a")
        self.play(FadeIn(bub), run_time=1.0)
        self.play(Indicate(bub, color=GREY, scale_factor=1.08), run_time=1.2)
        # gene row
        hum = lab("MRGPRX1", 54, TEXT)
        neq = lab("≠", 60, TEXT)
        row_t = lab("MrgprA3", 54, TEAL)
        row = VGroup(row_t, neq, hum).arrange(RIGHT, buff=0.55).move_to([0, 0.5, 0])
        sm = sub("mouse gene", 28, TEAL).next_to(row_t, DOWN, buff=0.25)
        sh = sub("human gene", 28, TEXT).next_to(hum, DOWN, buff=0.25)
        self.at("human")
        self.play(FadeOut(mouse), FadeOut(cheek), FadeOut(hind), FadeOut(fore), FadeOut(laneA), FadeOut(laneB),
                  FadeOut(tA), FadeOut(tB), FadeOut(iA), FadeOut(iB), FadeOut(bub),
                  ReplacementTransform(tag, row_t), run_time=1.3)
        self.at("mrgprx1")
        self.play(FadeIn(neq), FadeIn(hum), run_time=0.9)
        self.at("also a different")
        self.play(FadeIn(sm), FadeIn(sh), Indicate(neq, color=PAIN, scale_factor=1.4), run_time=1.4)
        self.finish()


# ================================================================ s07b
class S07bSpecies(SpokenScene):
    def construct(self):
        EC_M, EC_H = 27.55, 297.68
        R = lambda c, ec: c / (ec + c)
        ax = Axes(x_range=[0, 3.5, 0.5], y_range=[0, 1, 0.5], x_length=9.0, y_length=5.0,
                  axis_config=dict(color=GREY, stroke_width=3, include_ticks=False, include_tip=False)).move_to([-1.2, 0.0, 0])
        ticks = VGroup()
        for k, s in enumerate(["1", "10", "100", "1000"]):
            ticks.add(sub(s, 24, TEXT).move_to(ax.c2p(k, 0) + DOWN * 0.3))
        xl = sub("chloroquine, µM (log scale)", 28, TEXT).move_to([-1.2, -3.45, 0])
        yl = sub("response (model)", 28, TEXT).rotate(PI / 2).move_to([-6.45, 0, 0])
        curve_m = ax.plot(lambda x: R(10 ** x, EC_M), x_range=[0, 3.5], color=TEAL, stroke_width=6)
        curve_h = ax.plot(lambda x: R(10 ** x, EC_H), x_range=[0, 3.5], color=TEXT, stroke_width=6)
        # carried gene row
        row_t = lab("MrgprA3", 54, TEAL)
        neq = lab("≠", 60, TEXT)
        hum = lab("MRGPRX1", 54, TEXT)
        row = VGroup(row_t, neq, hum).arrange(RIGHT, buff=0.55).move_to([0, 0.5, 0])
        sm = sub("mouse gene", 28, TEAL).next_to(row_t, DOWN, buff=0.25)
        sh = sub("human gene", 28, TEXT).next_to(hum, DOWN, buff=0.25)
        self.add(row, sm, sh)
        lm = VGroup(lab("mouse", 28, TEAL), lab("MrgprA3", 28, TEAL)).arrange(DOWN, buff=0.04)
        lh = VGroup(lab("human", 28, TEXT), lab("MRGPRX1", 28, TEXT)).arrange(DOWN, buff=0.04)
        lm.move_to([5.4, 2.3, 0])
        lh.move_to([5.4, 1.3, 0])
        self.play(FadeOut(sm), FadeOut(sh), FadeOut(neq), ReplacementTransform(row_t, lm), ReplacementTransform(hum, lh),
                  Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), run_time=1.6)
        cap = VGroup(sub("transfected cells,", 26, GREY), sub("computed model", 26, GREY)).arrange(DOWN, buff=0.05).move_to([5.1, -1.6, 0])
        self.at("respond to chloroquine")
        self.play(Create(curve_m), FadeIn(cap), run_time=2.0)
        self.at("transfected")
        self.play(Create(curve_h), run_time=2.0)
        self.at("but not equally")
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(np.log10(EC_H), 0.5), color=GREY, stroke_width=3)
        dm = DashedLine(ax.c2p(np.log10(EC_M), 0.5), ax.c2p(np.log10(EC_M), 0), color=TEAL, stroke_width=4)
        dh = DashedLine(ax.c2p(np.log10(EC_H), 0.5), ax.c2p(np.log10(EC_H), 0), color=TEXT, stroke_width=4)
        self.play(Create(half), run_time=0.8)
        self.play(Create(dm), Create(dh), run_time=1.2)
        tm = sub("27.55 µM", 24, TEAL).move_to(ax.c2p(np.log10(EC_M) - 0.05, 0.6), aligned_edge=RIGHT)
        th = sub("297.68 µM", 24, TEXT).move_to(ax.c2p(np.log10(EC_H) + 0.08, 0.38), aligned_edge=LEFT)
        self.at("functional potency")
        self.play(FadeIn(tm), FadeIn(th), run_time=1.0)
        self.play(Indicate(lh, color=TEXT, scale_factor=1.1), run_time=1.6)
        # cursor
        tr = ValueTracker(np.log10(4.0))
        cur = always_redraw(lambda: DashedLine(ax.c2p(tr.get_value(), 0), ax.c2p(tr.get_value(), 1), color=YELLOW, stroke_width=4))
        dotm = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), R(10 ** tr.get_value(), EC_M)), radius=0.12, color=TEAL).set_z_index(6))
        doth = always_redraw(lambda: Dot(ax.c2p(tr.get_value(), R(10 ** tr.get_value(), EC_H)), radius=0.12, color=TEXT).set_z_index(6))
        rm = always_redraw(lambda: M(f"mouse {R(10 ** tr.get_value(), EC_M):.2f}", 26, TEAL).move_to([5.4, 0.4, 0]))
        rh = always_redraw(lambda: M(f"human {R(10 ** tr.get_value(), EC_H):.2f}", 26, TEXT).move_to([5.4, -0.4, 0]))
        ct = always_redraw(lambda: M(f"{10 ** tr.get_value():.0f} µM", 24, YELLOW).move_to(ax.c2p(tr.get_value(), 1.0) + UP * 0.25))
        self.at("shared ligand")
        self.add(tr)
        self.play(FadeIn(cur), FadeIn(dotm), FadeIn(doth), FadeIn(rm), FadeIn(rh), FadeIn(ct), FadeOut(tm), run_time=0.8)
        self.play(tr.animate.set_value(np.log10(12.0)), run_time=0.9)
        nt = lab("not equivalent:", 30, TEXT)
        c1 = chip("genes", GREY, 28)
        c2 = chip("neurons", GREY, 28)
        c3 = chip("sensations", GREY, 28)
        rowc = VGroup(nt, c1, c2, c3).arrange(RIGHT, buff=0.3).move_to([-0.5, 3.45, 0])
        self.at("do not make")
        self.play(FadeIn(nt), tr.animate.set_value(np.log10(18.0)), run_time=0.7)
        self.at("genes")
        self.play(FadeIn(c1), tr.animate.set_value(np.log10(24.0)), run_time=0.6)
        self.at("neurons")
        self.play(FadeIn(c2), tr.animate.set_value(np.log10(28.0)), run_time=0.6)
        self.at("sensations")
        self.play(FadeIn(c3), tr.animate.set_value(np.log10(30.0)), run_time=0.8)
        self.play(FadeIn(tm), Indicate(rm, color=TEAL, scale_factor=1.3), Indicate(rh, color=TEXT, scale_factor=1.3), run_time=1.6)
        self.finish()


# ================================================================ s08
class S08Rule(SpokenScene):
    def construct(self):
        xs = [-4.95, -1.65, 1.65, 4.95]
        cols = [HIST, TEAL, GREY, PURP]
        names = [["Trigger"], ["Recruited", "population"], ["Spinal", "route"], ["Inhibition"]]
        panels, labels = [], []
        for x, c, nm in zip(xs, cols, names):
            r = RoundedRectangle(corner_radius=0.25, width=2.5, height=5.0, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.0).move_to([x, 0.0, 0])
            panels.append(r)
            labels.append(VGroup(*[lab(s, 28, c if c != GREY else TEXT) for s in nm]).arrange(DOWN, buff=0.05).move_to([x, 1.8, 0]))
        # carried world fades into the four regions
        self.play(*[Create(p) for p in panels[:2]], run_time=1.6)
        self.at("trigger")
        self.play(FadeIn(labels[0]), panels[0].animate.set_fill(HIST, 0.10), run_time=0.7)
        fl_g = Flow([-5.7, 0.5, 0], [-4.2, 0.2, 0], HIST, n=4, seed=1)
        fl_b = Flow([-5.7, -0.5, 0], [-4.2, -0.2, 0], CHLQ, n=4, seed=2)
        self.add(fl_g, fl_b)
        self.at("recruited population")
        cells = VGroup(*[Circle(radius=0.38, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.35).move_to([-1.65, y, 0]) for y in (0.6, -0.2, -1.0)])
        self.play(FadeIn(labels[1]), panels[1].animate.set_fill(TEAL, 0.10), FadeIn(cells), run_time=0.8)
        d3 = dashed(panels[2].copy().set_stroke(GREY, 4), 40)
        d4 = dashed(panels[3].copy().set_stroke(PURP, 4), 40)
        self.at("spinal")
        self.play(FadeOut(panels[2]), FadeIn(d3), FadeIn(labels[2]), run_time=0.8)
        self.at("and inhibition")
        self.play(FadeOut(panels[3]), FadeIn(d4), FadeIn(labels[3]), run_time=0.8)
        links = VGroup(*[Arrow([x + 1.3, 0.4, 0], [x + 2.0, 0.4, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.2)
                         for x in (-4.95, -1.65, 1.65)])
        self.at("together")
        self.play(FadeIn(links), run_time=0.8)
        rule = lab("Each perturbation supports only the link it tests", 30, TEXT).move_to([0, -3.2, 0])
        br = RoundedRectangle(corner_radius=0.15, width=1.6, height=1.3, stroke_color=YELLOW, stroke_width=6).move_to([-3.3, 0.4, 0])
        self.at("each perturbation")
        self.play(FadeIn(rule), Create(br), run_time=1.0)
        self.at("link it")
        self.play(br.animate.move_to([0.0, 0.4, 0]), run_time=2.2)
        self.at("chapter")
        brace = Brace(VGroup(d3, d4), UP, color=YELLOW)
        ch2 = lab("chapter 2", 30, YELLOW).next_to(brace, UP, buff=0.1)
        self.play(FadeOut(br), FadeIn(brace), FadeIn(ch2), run_time=1.0)
        self.at("this pathway")
        inner = Flow([-0.6, 0.4, 0], [1.6, 0.4, 0], TEAL, n=4, seed=7, level=0.0)
        self.add(inner)
        self.play(fl_to(inner, 1.0, 1.0), run_time=1.0)
        self.finish()


class S09End(EndCard):
    LINE = "Each perturbation supports only the link it tests."
