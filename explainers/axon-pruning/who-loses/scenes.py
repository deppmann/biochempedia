"""Pruning Without Dying, chapter 3: Who Loses, and When It Commits

COLOR MAP (one color per concept; the first seven are the lesson's shared map from scenes.old.py)
  BLUE   = the neuron (cell body and axon)
  YELLOW = NGF (the dots) and TrkA, its receptor
  RED    = degeneration, loss, the loser
  GREEN  = survival, the winner, protected
  GREY   = structure, targets, time axis, labels
  VIOLET = caspases (not used in this chapter)   ORANGE = Apaf-1 (not used in this chapter)
  PINK   = BDNF (the dots) and p75, its receptor (new in this chapter)
  TEAL   = spheroids and the calcium inside them (calcium dots a lighter teal), and the transition stretch
  GOLD   = the laboratory's model (the gate)
  WHITE  = DR6 and the unnamed neurotrophins (plain text colour)
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#EE8CCB"
CALCIUM = "#A8E6EA"


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# shared building blocks
def line_segs(x0, y0, x1, y1, n, width=8.0, color=BLUE):
    xs = np.linspace(x0, x1, n + 1)
    ys = np.linspace(y0, y1, n + 1)
    return VGroup(*[Line(P(xs[i], ys[i]), P(xs[i + 1], ys[i + 1]), color=color, stroke_width=width,
                         cap_style=CapStyleType.ROUND) for i in range(n)])


def smooth_segs(x0, y0, x1, y1, n, width=8.0, color=BLUE):
    def f(t):
        return P(x0 + (x1 - x0) * t, y0 + (y1 - y0) * (t * t * (3 - 2 * t)))
    return VGroup(*[Line(f(i / n), f((i + 1) / n), color=color, stroke_width=width,
                         cap_style=CapStyleType.ROUND) for i in range(n)])


def body(x, y, r=0.38):
    return Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to(P(x, y))


def ndot(pos, color=YELLOW, r=0.11):
    return Dot(P(pos[0], pos[1]), radius=r, color=color)


def leader(a, b, color=GREY, w=2.5):
    return Line(a, b, color=color, stroke_width=w).set_opacity(0.85)


def receptor(base, ang, color, s=1.0):
    """A receptor as a cartoon: a short stalk from the membrane ending in an open cup facing outward."""
    d = P(np.cos(ang), np.sin(ang))
    r, st = 0.17 * s, 0.28 * s
    end = base + d * st
    c = end + d * r
    w = 5 * min(s, 1.5)
    stalk = Line(base, end, color=color, stroke_width=w)
    cup = Arc(radius=r, start_angle=ang + PI / 2, angle=PI, arc_center=c, color=color, stroke_width=w + 1)
    return VGroup(stalk, cup), c


class Tip:
    """An axon tip: a bulb with receptor cups on its outer face. slots = [(name, angle in degrees)]."""

    def __init__(self, center, s=1.0, slots=()):
        self.center, self.s = center, s
        self.rb = 0.42 * s
        self.bulb = Circle(radius=self.rb, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                           fill_opacity=0.35).move_to(center)
        self.rec, self.cup = {}, {}
        for name, deg in slots:
            col = PINK if name.startswith("p75") else YELLOW
            a = np.radians(deg)
            base = center + P(np.cos(a), np.sin(a)) * self.rb
            g, c = receptor(base, a, col, s)
            self.rec[name], self.cup[name] = g, c

    def receptors(self):
        return VGroup(*self.rec.values())


def frag_offsets(n, seed, amp=0.32):
    rng = random.Random(seed)
    return [(rng.uniform(-0.12, 0.12), rng.uniform(-amp, amp), rng.uniform(-0.6, 0.6)) for _ in range(n)]


def frag_anim(segs, offs, color=RED, opacity=None):
    out = []
    for s, (dx, dy, rot) in zip(segs, offs):
        a = s.animate.shift(P(dx, dy)).rotate(rot).scale(0.75).set_color(color)
        if opacity is not None:
            a = a.set_opacity(opacity)
        out.append(a)
    return out


def frag_now(segs, offs, color=RED, opacity=None):
    for s, (dx, dy, rot) in zip(segs, offs):
        s.shift(P(dx, dy)).rotate(rot).scale(0.75).set_color(color)
        if opacity is not None:
            s.set_opacity(opacity)


# ---------------------------------------------------------------------------------------------
# scenes 1 to 3: branches compete for a target's NGF
ROWS = [(2.6, 1.5), (1.0, 0.5), (-1.0, -0.5), (-2.6, -1.5)]   # (body y, tip y)
BODY_X, AX0, AX1 = -5.65, -5.25, 2.9
DOTS4 = [(3.5, 0.8), (3.5, 0.2), (3.5, -0.3), (3.5, -0.9)]


def target_block(h=4.6):
    return RoundedRectangle(corner_radius=0.3, width=1.9, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.16).move_to(P(5.15, 0))


def axon_row(by, ty, width=11):
    b = body(BODY_X, by, 0.4)
    segs = smooth_segs(AX0 - 0.04, by, AX1, ty, 16, width)
    tip = Dot(P(AX1, ty), radius=0.22, color=BLUE)
    return b, segs, tip


def axon_set(i):
    by, ty = ROWS[i]
    return axon_row(by, ty)


class S00Title(TitleCard):
    LESSON = "Pruning Without Dying: Axons That Cut Themselves Back"
    TITLE = "Who Loses, and When It Commits"


class S01Q(SpokenScene):
    def construct(self):
        tg = target_block(4.2)
        top, bot = axon_row(1.5, 1.0), axon_row(-1.5, -1.0)
        dish = RoundedRectangle(corner_radius=0.4, width=12.6, height=6.5, stroke_color=GREY, stroke_width=3)
        dish = DashedVMobject(dish, num_dashes=70).set_opacity(0.8)
        dlab = T("in a dish", 30, GREY).move_to(P(-4.7, 2.75))
        dt = VGroup(ndot((3.45, 1.3), YELLOW, 0.16), ndot((3.45, 0.75), YELLOW, 0.16))
        db = VGroup(ndot((3.45, -0.75), YELLOW, 0.16), ndot((3.45, -1.3), YELLOW, 0.16))
        self.play(Create(dish), FadeIn(dlab), FadeIn(tg), FadeIn(top[0], scale=0.7), FadeIn(bot[0], scale=0.7),
                  Create(top[1], lag_ratio=1.0), Create(bot[1], lag_ratio=1.0), GrowFromCenter(top[2]),
                  GrowFromCenter(bot[2]), FadeIn(dt, scale=0.5), FadeIn(db, scale=0.5), run_time=1.0)
        self.at("experimenter decides")
        exp = chip("experimenter", GREY, size=30, pad=0.16).move_to(P(0.4, 0.0))
        arr = Arrow(exp.get_right() + RIGHT * 0.05, P(3.0, -0.95), buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(exp, shift=DOWN * 0.1), GrowArrow(arr), run_time=0.7)
        self.at("where support is lost")
        self.play(*[d.animate.shift(DOWN * 0.5).set_opacity(0) for d in db],
                  *[s.animate.set_stroke(width=6).set_opacity(0.6) for s in bot[1]], run_time=0.9)
        self.at("In the animal")
        self.play(FadeOut(VGroup(dish, dlab, exp, arr)), *[d.animate.shift(UP * 0.5).set_opacity(1) for d in db],
                  *[s.animate.set_stroke(width=11).set_opacity(1) for s in bot[1]], run_time=0.5)
        self.at("who decides", lead=0.5)
        q = T("?", 110, TEXT, weight=BOLD).move_to(P(0.2, 0.0))
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.play(Indicate(VGroup(top[1], bot[1]), color=TEXT, scale_factor=1.0), run_time=0.9)
        self.finish()


class S02Compete(SpokenScene):
    def construct(self):
        tg = target_block()
        parts = [axon_set(i) for i in range(4)]
        dots = VGroup(*[ndot(p, YELLOW, 0.16) for p in DOTS4])
        old = [parts[1], parts[2]]
        self.add(tg, *[p[0] for p in old], *[p[1] for p in old], *[p[2] for p in old], dots)
        self.at("Many sympathetic", lead=0.0)
        new = [parts[0], parts[3]]
        self.play(*[FadeIn(p[0], scale=0.7) for p in new], run_time=0.5)
        self.at("send branches")
        self.play(*[Create(p[1], lag_ratio=1.0) for p in new], *[GrowFromCenter(p[2]) for p in new], run_time=0.9)
        self.at("toward targets")
        tlab = T("target", 32, GREY).move_to(P(5.15, 0))
        self.play(FadeIn(tlab, scale=0.8), Indicate(tg, color=TEXT, scale_factor=1.03), run_time=0.7)
        self.at("that make")
        leg = VGroup(Dot(P(3.9, 3.15), radius=0.14, color=YELLOW), T("NGF", 32, YELLOW).move_to(P(4.5, 3.15)))
        self.play(FadeIn(leg, shift=DOWN * 0.1), Indicate(dots, color=YELLOW, scale_factor=1.6), run_time=0.9)
        self.at("The branches compete")
        tips = VGroup(*[p[2] for p in parts])
        self.play(Indicate(tips, color=TEXT, scale_factor=2.0), run_time=1.0)
        self.finish()


class S03Zero(SpokenScene):
    def construct(self):
        tg = target_block()
        parts = [axon_set(i) for i in range(4)]
        dots = VGroup(*[ndot(p, YELLOW, 0.16) for p in DOTS4])
        tlab = T("target", 32, GREY).move_to(P(5.15, 0))
        leg = VGroup(Dot(P(3.9, 3.15), radius=0.14, color=YELLOW), T("NGF", 32, YELLOW).move_to(P(4.5, 3.15)))
        for p in parts:
            self.add(p[0], p[1], p[2])
        self.add(tg, tlab, dots, leg)
        win, lose = parts[1], parts[2]
        self.at("limited", lead=0.3)
        cap = T("only enough for some", 30, GREY).move_to(P(-0.6, 3.15))
        self.play(*[FadeOut(parts[i][j]) for i in (0, 3) for j in range(3)], FadeOut(dots[2]), FadeOut(dots[3]),
                  FadeIn(cap, shift=DOWN * 0.1), Indicate(leg, color=YELLOW, scale_factor=1.2), run_time=0.9)
        self.at("wins enough")
        self.play(dots[0].animate.move_to(P(AX1 + 0.1, 0.55)).set_opacity(0),
                  dots[1].animate.move_to(P(AX1 + 0.1, 0.45)).set_opacity(0),
                  *[s.animate.set_stroke(width=20) for s in win[1]], win[2].animate.scale(1.9),
                  FadeOut(cap), run_time=0.9)
        self.at("stabilized")
        c1 = chip("stabilized", GREEN, size=30, pad=0.16).move_to(P(0.6, 1.9))
        self.play(FadeIn(c1, shift=UP * 0.1), Indicate(win[1], color=GREEN, scale_factor=1.0), run_time=0.7)
        self.at("One left with")
        self.play(Indicate(lose[2], color=RED, scale_factor=1.8), run_time=1.0)
        self.at("weakened")
        self.play(*[s.animate.set_stroke(width=3).set_opacity(0.6) for s in lose[1]], lose[2].animate.scale(0.6),
                  run_time=0.9)
        self.at("removed")
        offs = frag_offsets(16, 7)
        self.play(*frag_anim(lose[1], offs), lose[2].animate.set_color(RED), run_time=0.6)
        c2 = chip("removed", RED, size=30, pad=0.16).move_to(P(0.6, -1.9))
        self.play(*[FadeOut(s) for s in lose[1]], FadeOut(lose[2]), FadeIn(c2, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scenes 4 to 9: the two receptors, the question, the answer
class S04Recept(SpokenScene):
    def construct(self):
        s = 4.2
        tip = Tip(P(-3.0, 0), s, [("p75", -35), ("trkA", 35)])
        shaft = line_segs(-6.2, 0, -3.0 - tip.rb + 0.1, 0, 8, 16)
        self.play(Create(shaft, lag_ratio=1.0), FadeIn(tip.bulb, scale=0.6), run_time=0.7)
        self.at("matter")
        self.play(*[Create(g) for g in tip.rec.values()], run_time=0.7)
        self.wait(0.4)
        self.at("is the")
        cA, cP = tip.cup["trkA"], tip.cup["p75"]
        l1 = T("TrkA", 52, YELLOW, weight=BOLD).move_to(P(2.4, 2.45)).align_to(P(2.4, 0), LEFT)
        ld1 = leader(cA + P(0.85, 0.15), P(2.25, 2.4), YELLOW)
        self.play(FadeIn(l1, shift=RIGHT * 0.15), Create(ld1), run_time=0.5)
        self.at("NGF receptor")
        l1b = T("the NGF receptor", 30, TEXT).next_to(l1, DOWN, buff=0.15, aligned_edge=LEFT)
        ngf = ndot((1.7, 1.25), YELLOW, 0.28)
        self.play(FadeIn(l1b, shift=RIGHT * 0.15), FadeIn(ngf), run_time=0.5)
        self.play(ngf.animate.move_to(cA), run_time=0.7)
        self.at("binds all", lead=0.9)
        l2 = T("p75", 52, PINK, weight=BOLD).move_to(P(2.4, -1.45)).align_to(P(2.4, 0), LEFT)
        ld2 = leader(cP + P(0.85, -0.15), P(2.25, -1.55), PINK)
        self.play(FadeIn(l2, shift=RIGHT * 0.15), Create(ld2), run_time=0.5)
        l2a = T("binds all", 30, TEXT).next_to(l2, DOWN, buff=0.15, aligned_edge=LEFT)
        l2a2 = T("neurotrophins,", 30, TEXT).next_to(l2a, DOWN, buff=0.08, aligned_edge=LEFT)
        self.play(FadeIn(l2a, shift=RIGHT * 0.15), FadeIn(l2a2, shift=RIGHT * 0.15), run_time=0.5)
        self.at("neurotrophins")
        for col in (YELLOW, TEXT):
            d = ndot((1.7, -1.25), col, 0.28)
            self.add(d)
            self.play(d.animate.move_to(cP), run_time=0.3)
            self.play(d.animate.move_to(P(1.7, -1.25)).set_opacity(0), run_time=0.25)
        self.at("including BDNF")
        l2b = T("including BDNF", 30, PINK).next_to(l2a2, DOWN, buff=0.08, aligned_edge=LEFT)
        d3 = ndot((1.7, -1.25), PINK, 0.28)
        self.play(FadeIn(l2b, shift=RIGHT * 0.15), FadeIn(d3), run_time=0.4)
        self.play(d3.animate.move_to(cP), run_time=0.6)
        self.play(Indicate(tip.rec["p75"], color=PINK, scale_factor=1.1), run_time=0.8)
        self.finish()


TY, BY, TIPX, BODX = 1.8, -1.8, 0.6, -5.7
TS = 1.7   # scale of the tips
TAG_OFF = (1.3, 0.45)
BD_BASE = [P(4.5, 0.35), P(5.3, 0.15), P(4.7, -0.3), P(5.4, -0.35)]
S05_DRIFT_END = 4.1    # seconds of drift already elapsed when s05 ends
S06_LEN = 5.4


def drift(i, t):
    return P(0.28 * np.sin(0.9 * t + 1.7 * i) - 0.28 * np.sin(1.7 * i),
             0.2 * np.cos(1.1 * t + 2.1 * i) - 0.2 * np.cos(2.1 * i))


def start_drift(scene, dots, t0):
    ts = scene.elapsed()
    for i, d in enumerate(dots):
        d.add_updater(lambda m, dt, i=i: m.move_to(BD_BASE[i] + drift(i, t0 + scene.elapsed() - ts)))


def stop_drift(dots):
    for d in dots:
        d.clear_updaters()


def tag_follow(tag, dots, off=(0.0, 0.95)):
    g = VGroup(*dots)
    tag.add_updater(lambda m, dt: m.move_to(g.get_center() + P(off[0], off[1])))


class Pair:
    """The strong-TrkA axon (top) and the weak-TrkA axon (bottom), in the same place in every scene."""

    def __init__(self):
        self.body_t, self.body_b = body(BODX, TY, 0.45), body(BODX, BY, 0.45)
        self.tip_t = Tip(P(TIPX, TY), TS, [("p75", 38), ("trkA", 0), ("trkB", -38)])
        self.tip_b = Tip(P(TIPX, BY), TS, [("p75", 38), ("trkA", 0)])
        xe = TIPX - self.tip_t.rb + 0.08
        self.sh_t = line_segs(-5.25, TY, xe, TY, 12, 12)
        self.sh_b = line_segs(-5.25, BY, xe, BY, 12, 12)
        self.nd = [ndot(self.tip_t.cup["trkA"], YELLOW, 0.17), ndot(self.tip_t.cup["trkB"], YELLOW, 0.17)]

        def cl(text, color, cup):
            return T(text, 26, color).next_to(cup, RIGHT, buff=0.42)
        t, b = self.tip_t, self.tip_b
        self.cl_t = VGroup(cl("p75", PINK, t.cup["p75"]), cl("TrkA", YELLOW, t.cup["trkA"]),
                           cl("TrkA", YELLOW, t.cup["trkB"]))
        self.cl_b = VGroup(cl("p75", PINK, b.cup["p75"]), cl("TrkA", YELLOW, b.cup["trkA"]))
        self.lab_t = T("strong TrkA", 34, YELLOW).move_to(P(-2.8, TY + 0.85))
        self.lab_b = T("weak TrkA", 34, YELLOW).move_to(P(-2.8, BY + 0.85))
        self.bd = [ndot(BD_BASE[i], PINK, 0.15) for i in range(4)]
        self.bd_tag = T("BDNF", 30, PINK)

    def add_top(self, scene, labels=True):
        scene.add(self.body_t, self.sh_t, self.tip_t.bulb, self.tip_t.receptors(), *self.nd)
        if labels:
            scene.add(self.lab_t, self.cl_t)

    def add_bottom(self, scene, labels=True):
        scene.add(self.body_b, self.sh_b, self.tip_b.bulb, self.tip_b.receptors())
        if labels:
            scene.add(self.lab_b, self.cl_b)

    def spots(self):
        cup = self.tip_b.cup["p75"]
        return [cup, cup + P(0.1, 0.55), cup + P(0.55, 0.5), cup + P(-0.3, 0.5)]

    def thin_weak(self):
        for s in self.sh_b:
            s.set_stroke(width=5)
        self.tip_b.bulb.set_fill(BLUE, 0.2)


def qmarks():
    return VGroup(T("?", 80, TEXT, weight=BOLD).move_to(P(5.4, TY)), T("?", 80, TEXT, weight=BOLD).move_to(P(5.4, BY)))


class S05Q1(SpokenScene):
    def construct(self):
        p = Pair()
        self.play(FadeIn(p.body_t, scale=0.7), FadeIn(p.body_b, scale=0.7), Create(p.sh_t, lag_ratio=1.0),
                  Create(p.sh_b, lag_ratio=1.0), FadeIn(p.tip_t.bulb), FadeIn(p.tip_b.bulb), run_time=0.9)
        self.at("strong")
        self.play(*[Create(g) for g in p.tip_t.rec.values()], run_time=0.5)
        self.play(*[FadeIn(d, scale=0.3) for d in p.nd], FadeIn(p.lab_t, shift=RIGHT * 0.1), FadeIn(p.cl_t),
                  run_time=0.6)
        self.at("the other")
        self.play(*[Create(g) for g in p.tip_b.rec.values()], FadeIn(p.lab_b, shift=RIGHT * 0.1), FadeIn(p.cl_b),
                  run_time=0.7)
        self.at("BDNF is")
        for d in p.bd:
            d.set_opacity(0)
            self.add(d)
        p.bd_tag.set_opacity(0)
        self.add(p.bd_tag)
        tag_follow(p.bd_tag, p.bd)
        start_drift(self, p.bd, 0.0)
        self.play(LaggedStart(*[d.animate.set_opacity(1) for d in p.bd], lag_ratio=0.15),
                  p.bd_tag.animate.set_opacity(1), run_time=1.0)
        self.at("Which axon")
        q = qmarks()
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        p = Pair()
        p.add_top(self)
        p.add_bottom(self)
        self.add(*p.bd, p.bd_tag, qmarks())
        tag_follow(p.bd_tag, p.bd)
        start_drift(self, p.bd, S05_DRIFT_END)
        cx, cy, r = -2.8, 0.3, 0.52
        ring = Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(P(cx, cy))
        ring.set_stroke(opacity=0.5)
        think = T("think", 26, GREY).move_to(P(cx, cy))
        dur = 5.0

        def arc():
            f = min(self.elapsed() / dur, 1.0)
            return Arc(radius=r, start_angle=PI / 2, angle=-2 * PI * max(1 - f, 0.001), arc_center=P(cx, cy),
                       color=TEXT, stroke_width=7, fill_opacity=0)
        self.add(ring, think, always_redraw(arc))
        self.finish()


class S07R1(SpokenScene):
    def construct(self):
        p = Pair()
        q = qmarks()
        p.add_top(self)
        p.add_bottom(self)
        self.add(*p.bd, p.bd_tag, q)
        tag_follow(p.bd_tag, p.bd)
        start_drift(self, p.bd, S05_DRIFT_END + S06_LEN)
        self.play(FadeOut(q), Indicate(VGroup(p.sh_b, p.tip_b.bulb), color=TEXT, scale_factor=1.0), run_time=0.9)
        self.at("On axons with weak")
        self.play(Indicate(p.lab_b, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("BDNF acting")
        stop_drift(p.bd)
        p.bd_tag.clear_updaters()
        tag_follow(p.bd_tag, p.bd, off=TAG_OFF)
        self.play(*[d.animate.move_to(s) for d, s in zip(p.bd, p.spots())], run_time=1.3)
        self.at("through")
        self.play(Indicate(p.tip_b.rec["p75"], color=PINK, scale_factor=1.3),
                  Indicate(p.cl_b[0], color=PINK, scale_factor=1.3), run_time=0.9)
        self.at("caused degeneration")
        gone = VGroup(*p.sh_b[6:])
        offs = frag_offsets(6, 11)
        self.play(*[s.animate.set_stroke(width=4) for s in p.sh_b], p.tip_b.bulb.animate.scale(0.6),
                  run_time=0.6)
        self.play(*frag_anim(gone, offs, RED, 0.45),
                  p.tip_b.bulb.animate.shift(P(0.1, -0.3)).set_color(RED).set_opacity(0.45),
                  FadeOut(p.tip_b.receptors()), FadeOut(p.cl_b), *[FadeOut(d) for d in p.bd], FadeOut(p.bd_tag),
                  run_time=0.8)
        credit = T("Singh, Kaplan, Miller and colleagues, 2008", 26, GREY).move_to(P(0, -3.3))
        self.play(FadeIn(credit, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S08R1b(SpokenScene):
    def construct(self):
        p = Pair()
        p.thin_weak()
        p.add_top(self)
        p.add_bottom(self, labels=False)
        self.add(p.lab_b, p.cl_b[0])
        self.at("protected")
        prot = chip("protected", GREEN, size=30, pad=0.16).move_to(P(5.2, TY))
        self.play(FadeIn(prot, shift=LEFT * 0.1), Indicate(p.sh_t, color=GREEN, scale_factor=1.0), run_time=0.8)
        self.at("And the winning")
        wtag = T("winner", 30, GREEN).move_to(P(BODX, 2.8))
        self.play(FadeIn(wtag, shift=DOWN * 0.1), Indicate(p.body_t, color=GREEN, scale_factor=1.25), run_time=0.8)
        self.at("made the")
        dots = [ndot((3.9 + 0.2 * i, 0.3 - 0.1 * i), PINK, 0.15).set_opacity(0) for i in range(4)]
        self.add(*dots)
        p.bd_tag.set_opacity(0)
        self.add(p.bd_tag)
        tag_follow(p.bd_tag, dots, off=TAG_OFF)
        self.play(LaggedStart(*[d.animate.set_opacity(1).move_to(s) for d, s in zip(dots, p.spots())],
                              lag_ratio=0.2), p.bd_tag.animate.set_opacity(1), run_time=1.5)
        lab = T("in one model, released by the winner", 28, PINK).move_to(P(0.0, -3.25))
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.6)
        self.finish()


def line_parts():
    a1 = T("the winner", 30, TEXT)
    a2 = T("takes the NGF", 30, TEXT)
    VGroup(a1, a2).arrange(RIGHT, buff=0.18).move_to(P(0.5, -2.85))
    b = T("and signals", 30, TEXT)
    c = T("the loser’s removal", 30, TEXT)
    VGroup(b, c).arrange(RIGHT, buff=0.18).move_to(P(0.5, -3.38))
    return a1, a2, b, c


class S09R1c(SpokenScene):
    def construct(self):
        p = Pair()
        p.thin_weak()
        wtag = T("winner", 30, GREEN).move_to(P(BODX, 2.8))
        p.add_top(self, labels=False)
        p.add_bottom(self, labels=False)
        self.add(wtag)
        a1, a2, b, c = line_parts()
        cA, cB = p.tip_t.cup["trkA"], p.tip_t.cup["trkB"]
        self.wait(0.3)

        def wave(extra, run=0.8):
            ds = [ndot((5.2, cA[1] + 0.25), YELLOW, 0.17), ndot((5.2, cB[1] - 0.25), YELLOW, 0.17)]
            self.add(*ds)
            self.play(ds[0].animate.move_to(cA), ds[1].animate.move_to(cB), *extra, run_time=run)
            self.play(*[FadeOut(d) for d in ds], run_time=0.1)
        wave([FadeIn(a1, shift=UP * 0.1)])
        wave([FadeIn(a2, shift=UP * 0.1), *[s_.animate.set_stroke(width=18) for s_ in p.sh_t]])
        wave([Indicate(p.body_t, color=GREEN, scale_factor=1.25)])
        self.at("sends a signal", lead=0.3)
        dots = [ndot((3.9 + 0.2 * i, 0.3 - 0.1 * i), PINK, 0.15).set_opacity(0) for i in range(4)]
        self.add(*dots)
        p.bd_tag.set_opacity(0)
        self.add(p.bd_tag)
        tag_follow(p.bd_tag, dots, off=TAG_OFF)
        self.play(LaggedStart(*[d.animate.set_opacity(1).move_to(s) for d, s in zip(dots, p.spots())],
                              lag_ratio=0.15), p.bd_tag.animate.set_opacity(1), FadeIn(b, shift=UP * 0.1),
                  run_time=1.2)
        self.at("removes the loser", lead=0.3)
        ltag = T("loser", 30, RED).move_to(P(BODX, -1.05))
        gone = VGroup(p.sh_b, p.tip_b.bulb, p.tip_b.receptors(), *dots, p.bd_tag)
        self.play(FadeOut(gone), FadeIn(ltag, shift=UP * 0.1), FadeIn(c, shift=UP * 0.1), run_time=1.0)
        self.finish()


class S10Beat(NarratedScene):
    def construct(self):
        p = Pair()
        p.add_top(self, labels=False)
        for s in p.sh_t:
            s.set_stroke(width=18)
        wtag = T("winner", 30, GREEN).move_to(P(BODX, 2.8))
        ltag = T("loser", 30, RED).move_to(P(BODX, -1.05))
        a1, a2, b, c = line_parts()
        pair_group = VGroup(p.body_t, p.sh_t, p.tip_t.bulb, p.tip_t.receptors(), *p.nd, p.body_b, wtag, ltag,
                            a1, a2, b, c)
        self.add(pair_group)
        self.wait(2.2)
        panels = panel_group()
        self.play(FadeOut(pair_group), FadeIn(panels), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scene 11: the same idea at two scales
PY1, PY2 = 0.95, -1.15


def mini_panel(cx):
    frame = RoundedRectangle(corner_radius=0.2, width=6.1, height=5.5, stroke_color=GREY, stroke_width=2.5)
    frame.move_to(P(cx, 0))
    tgt = RoundedRectangle(corner_radius=0.2, width=0.8, height=4.0, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.16).move_to(P(cx + 2.4, -0.1))
    b1, b2 = body(cx - 2.35, PY1, 0.55), body(cx - 2.35, PY2, 0.55)
    a1 = line_segs(cx - 1.75, PY1, cx + 1.25, PY1, 8, 14)
    a2 = line_segs(cx - 1.75, PY2, cx + 1.25, PY2, 8, 14)
    t1, t2 = Dot(P(cx + 1.3, PY1), radius=0.26, color=BLUE), Dot(P(cx + 1.3, PY2), radius=0.26, color=BLUE)
    d = VGroup(ndot((cx + 1.85, PY1 + 0.3), YELLOW, 0.16), ndot((cx + 1.85, PY1 - 0.3), YELLOW, 0.16))
    return dict(frame=frame, tgt=tgt, b1=b1, b2=b2, a1=a1, a2=a2, t1=t1, t2=t2, d=d)




def panel_group():
    return VGroup(*[v for P_ in (mini_panel(-3.25), mini_panel(3.25)) for v in P_.values()])


class S11Scale(SpokenScene):
    def construct(self):
        L, R = mini_panel(-3.25), mini_panel(3.25)
        self.add(*L.values(), *R.values())
        lesson = chip("the neurotrophic hypothesis lesson", TEAL, size=28, pad=0.16).move_to(P(0, 3.25))
        self.at("neurotrophic hypothesis")
        self.play(FadeIn(lesson, shift=DOWN * 0.1), run_time=0.5)
        self.at("showed the same", lead=0.3)
        self.play(Indicate(L["frame"], color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("winner removes loser")
        lab = T("winner removes loser", 36, TEXT).move_to(P(0, -3.25))
        self.play(FadeIn(lab, shift=UP * 0.1), L["b1"].animate.set_stroke(GREEN), Indicate(L["d"], color=YELLOW, scale_factor=1.6),
                  run_time=0.9)
        self.at("whole neurons", lead=0.3)
        lt = T("whole neurons", 30, GREY).move_to(P(-3.25, 2.3))
        wl = T("winner", 26, GREEN).move_to(P(-5.6, PY1 + 0.85))
        ll = T("loser", 26, RED).move_to(P(-5.6, PY2 + 0.85))
        self.play(FadeIn(lt, shift=DOWN * 0.1), FadeIn(wl), FadeIn(ll),
                  L["b2"].animate.set_stroke(RED).set_fill(RED, 0.3).scale(0.8),
                  *[s.animate.set_color(RED).set_opacity(0.3) for s in L["a2"]],
                  L["t2"].animate.set_color(RED).set_opacity(0.3), run_time=1.0)
        self.at("Here it works", lead=0.65)
        rt = T("axons", 30, TEXT).move_to(P(3.25, 2.3))
        offs = frag_offsets(8, 5, 0.25)
        wl2 = T("winner", 26, GREEN).move_to(P(0.9, PY1 + 0.85))
        ll2 = T("loser", 26, RED).move_to(P(0.9, PY2 + 0.85))
        self.play(FadeIn(rt, shift=DOWN * 0.1), R["b1"].animate.set_stroke(GREEN),
                  *frag_anim(R["a2"], offs, RED, 0.5), R["t2"].animate.set_color(RED).set_opacity(0.5),
                  FadeIn(wl2), FadeIn(ll2), run_time=0.65)
        full = T("winner removes loser, at two scales", 36, TEXT).move_to(P(0, -3.25))
        self.play(Transform(lab, full), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scenes 12 to 19: one axon coming apart, and the time strip beneath it.
# The axon and the strip share one x axis: the swellings sit over the transition stretch.
CY, HW0 = 1.05, 0.28
AXA, AXB = -5.05, 5.15
BODY_CX = -5.6
SY, BAR_H = -2.3, 0.5
SX0, SXL, SXT, SX1 = -5.05, -0.3, 3.1, 5.2
PH_Y = SY - 0.52
BUMPS = [(0.4, 0.55, 0.36), (1.5, 0.72, 0.40), (2.6, 0.48, 0.34)]   # (x, extra half-height, width)
NGF_TIP = [(5.9, 1.45), (6.1, 1.05), (5.9, 0.65)]
CA_OFF = [(-0.08, 0.15), (0.10, -0.12), (-0.05, -0.22), (0.12, 0.2)]


def ribbon(bumps, color=BLUE, op=0.8, n=170):
    xs = np.linspace(AXA, AXB, n)
    hw = np.full(n, HW0)
    for (x0, amp, w) in bumps:
        hw = hw + amp * np.exp(-((xs - x0) / w) ** 2)
    top = [P(x, CY + h) for x, h in zip(xs, hw)]
    bot = [P(x, CY - h) for x, h in zip(xs[::-1], hw[::-1])]
    m = VMobject()
    m.set_points_as_corners(top + bot + [top[0]])
    m.set_fill(color, op).set_stroke(color, 0, opacity=0)
    return m


def axon_body():
    return body(BODY_CX, CY, 0.62)


def axon_tip():
    return Dot(P(5.3, CY), radius=0.3, color=BLUE)


def axon_group(ks, gop):
    rb = ribbon([(x, a * k, w) for (x, a, w), k in zip(BUMPS, ks)])
    gl = VGroup()
    for (x, a, w), k in zip(BUMPS, ks):
        if k > 0.03:
            e = Ellipse(width=2.5 * w * (0.4 + 0.6 * k), height=2 * (HW0 + a * k) * 0.8)
            e.move_to(P(x, CY)).set_fill(TEAL, gop).set_stroke(TEAL, 3, opacity=min(1.0, gop + 0.3))
            gl.add(e)
    return VGroup(rb, gl)


def axon_pieces(n=40):
    xs = np.linspace(AXA, AXB, n + 1)
    return VGroup(*[Polygon(P(xs[i], CY + HW0), P(xs[i + 1] + 0.02, CY + HW0), P(xs[i + 1] + 0.02, CY - HW0),
                            P(xs[i], CY - HW0), fill_color=BLUE, fill_opacity=0.8, stroke_width=0)
                    for i in range(n)])


class Strip:
    """The time strip under the axon: an arrow, three bars (filled as time passes), labels and a playhead."""

    def __init__(self, ph_x=SX0):
        self.arrow = Arrow(P(-5.3, SY), P(5.95, SY), buff=0, stroke_width=3, color=GREY, tip_length=0.22,
                           max_tip_length_to_length_ratio=0.5)
        self.time = T("time, not to scale", 26, GREY).move_to(P(-1.9, SY + 0.78))
        self.tick = Line(P(SX0, SY - 0.3), P(SX0, SY + 1.0), color=GREY, stroke_width=3)
        self.ngf = T("NGF withdrawn", 26, GREY).move_to(P(SX0 - 0.1, SY + 1.35)).align_to(P(SX0 - 0.1, 0), LEFT)
        self.lab1 = T("latent", 28, GREY).move_to(P((SX0 + SXL) / 2, SY - 0.95))
        self.lab2 = T("transition", 28, TEAL).move_to(P((SXL + SXT) / 2, SY - 0.95))
        self.lab3 = T("catastrophic", 28, RED).move_to(P((SXT + SX1) / 2, SY - 0.95))
        self.ph = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.22).move_to(P(ph_x, PH_Y))

    def bar(self, x0, x1, color):
        return Rectangle(width=max(x1 - x0, 0.01), height=BAR_H, stroke_width=0, fill_color=color,
                         fill_opacity=0.9).move_to(P((x0 + x1) / 2, SY))

    def full_bars(self, upto):
        out = [self.bar(SX0, SXL, GREY)]
        if upto >= 2:
            out.append(self.bar(SXL, SXT, TEAL))
        if upto >= 3:
            out.append(self.bar(SXT, SX1, RED))
        return out

    def base(self, scene):
        scene.add(self.arrow, self.time, self.tick, self.ngf)


def drive_ph(scene, ph, x0, x1, t0, t1):
    def up(m, dt):
        u = min(max((scene.elapsed() - t0) / (t1 - t0), 0.0), 1.0)
        m.move_to(P(x0 + (x1 - x0) * u, PH_Y))
    ph.add_updater(up)


def trail(ph, xa, xb, color):
    def mk():
        x = min(max(ph.get_center()[0], xa), xb)
        return Rectangle(width=max(x - xa, 0.01), height=BAR_H, stroke_width=0, fill_color=color,
                         fill_opacity=0.9).move_to(P((xa + x) / 2, SY))
    return always_redraw(mk)


def long_bracket():
    y = SY + 1.9
    ln = Line(P(SX0, y), P(SXL, y), color=GREY, stroke_width=3)
    e1 = Line(P(SX0, y - 0.12), P(SX0, y + 0.12), color=GREY, stroke_width=3)
    e2 = Line(P(SXL, y - 0.12), P(SXL, y + 0.12), color=GREY, stroke_width=3)
    lab = T("long", 26, GREY).move_to(P((SX0 + SXL) / 2, y + 0.3))
    return VGroup(ln, e1, e2, lab)


class S12Q2(SpokenScene):
    def construct(self):
        bd, rb, tip = axon_body(), ribbon([]), axon_tip()
        st = Strip()
        dots = VGroup(*[ndot(p, YELLOW, 0.15) for p in NGF_TIP])
        self.play(FadeIn(bd, scale=0.7), run_time=0.3)
        self.play(GrowFromEdge(rb, LEFT), run_time=0.9)
        self.play(GrowFromCenter(tip), FadeIn(dots, scale=0.4), run_time=0.4)
        self.at("after NGF")
        self.play(GrowArrow(st.arrow), FadeIn(st.time), run_time=0.8)
        self.at("withdrawn")
        self.play(*[d.animate.shift(UP * 0.45).set_opacity(0) for d in dots], FadeIn(st.tick),
                  FadeIn(st.ngf, shift=DOWN * 0.1), FadeIn(st.ph, scale=0.5), run_time=1.0)
        self.at("Not all at once")
        ghosts = [Rectangle(width=x1 - x0, height=BAR_H, stroke_color=c, stroke_width=5, fill_color=c,
                            fill_opacity=0.22).move_to(P((x0 + x1) / 2, SY))
                  for (x0, x1, c) in ((SX0, SXL, GREY), (SXL, SXT, TEAL), (SXT, SX1, RED))]
        self.play(LaggedStart(*[FadeIn(g, scale=1.0) for g in ghosts], lag_ratio=0.45), run_time=1.2)
        self.finish()


class S13Latent(SpokenScene):
    def construct(self):
        bd, rb, tip = axon_body(), ribbon([]), axon_tip()
        st = Strip()
        self.add(bd, rb, tip)
        st.base(self)
        self.add(st.ph)
        drive_ph(self, st.ph, SX0, SXL, 0.0, 4.9)
        self.add(trail(st.ph, SX0, SXL, GREY))
        self.at("long latent", lead=0.3)
        br = long_bracket()
        self.play(FadeIn(st.lab1, shift=UP * 0.1), FadeIn(br), run_time=0.6)
        self.at("looks nearly normal")
        self.play(Indicate(rb, color=TEXT, scale_factor=1.0), run_time=1.0)
        self.finish()


def ca_dests():
    return [[P(x + dx, CY + dy) for dx, dy in CA_OFF] for (x, a, w) in BUMPS]


class S14Trans(SpokenScene):
    def construct(self):
        bd, tip = axon_body(), axon_tip()
        st = Strip(SXL)
        ks = [ValueTracker(0) for _ in BUMPS]
        gop = ValueTracker(0.18)
        ax = always_redraw(lambda: axon_group([k.get_value() for k in ks], gop.get_value()))
        self.add(bd, tip, ax)
        st.base(self)
        self.add(st.bar(SX0, SXL, GREY), st.lab1, st.ph)
        drive_ph(self, st.ph, SXL, SXT, 0.0, 5.6)
        self.add(trail(st.ph, SXL, SXT, TEAL))
        self.at("Late in latency")
        self.play(FadeIn(st.lab2, shift=UP * 0.1), run_time=0.6)
        self.at("swellings called")
        self.play(LaggedStart(*[k.animate.set_value(1) for k in ks], lag_ratio=0.3), run_time=0.9)
        self.at("spheroids", lead=0.1)
        sl = T("spheroids", 30, TEAL).move_to(P(1.5, 2.7))
        ln = leader(P(1.5, 2.12), P(1.5, 2.42), TEAL)
        self.play(FadeIn(sl, shift=DOWN * 0.1), Create(ln), run_time=0.6)
        self.at("Calcium gathers", lead=0.3)
        cdots, anims = VGroup(), []
        for (x, a, w), dests in zip(BUMPS, ca_dests()):
            for j, dpos in enumerate(dests):
                d = Dot(P(x + (1.3 if j % 2 else -1.3), CY), radius=0.075, color=CALCIUM).set_opacity(0)
                cdots.add(d)
                anims.append(d.animate.move_to(dpos).set_opacity(1))
        self.add(cdots)
        cl = T("calcium", 30, TEAL).move_to(P(0.4, -0.55))
        cln = leader(P(0.4, 0.12), P(0.4, -0.25), TEAL)
        self.play(LaggedStart(*anims, lag_ratio=0.05), gop.animate.set_value(0.7), FadeIn(cl, shift=UP * 0.1),
                  Create(cln), run_time=1.4)
        self.finish()


class S15Rupt(SpokenScene):
    def construct(self):
        bd, tip = axon_body(), axon_tip()
        st = Strip(SXT)
        ks = [ValueTracker(1) for _ in BUMPS]
        gop = ValueTracker(0.7)
        ax = always_redraw(lambda: axon_group([k.get_value() for k in ks], gop.get_value()))
        sl = T("spheroids", 30, TEAL).move_to(P(1.5, 2.7))
        ln = leader(P(1.5, 2.12), P(1.5, 2.42), TEAL)
        cl = T("calcium", 30, TEAL).move_to(P(0.4, -0.55))
        cln = leader(P(0.4, 0.12), P(0.4, -0.25), TEAL)
        cdots = VGroup(*[Dot(p, radius=0.075, color=CALCIUM) for ds in ca_dests() for p in ds])
        self.add(bd, tip, ax)
        st.base(self)
        self.add(st.bar(SX0, SXL, GREY), st.bar(SXL, SXT, TEAL), st.lab1, st.lab2, st.ph, sl, ln, cl, cln, cdots)
        self.at("rupture", lead=0.65)
        rng = random.Random(3)
        spray, moves = VGroup(), []
        for (x, a, w) in BUMPS:
            for j in range(9):
                ang = j * 2 * PI / 9 + rng.uniform(-0.2, 0.2)
                dist = rng.uniform(0.8, 1.5)
                dd = Dot(P(x, CY), radius=0.09, color=TEAL)
                spray.add(dd)
                moves.append(dd.animate.move_to(P(x + dist * np.cos(ang), CY + dist * np.sin(ang))).set_opacity(0.9))
        self.add(spray)
        rl = T("ruptured", 30, TEAL).move_to(P(4.55, 2.7))
        self.play(FadeIn(rl), *moves, LaggedStart(*[k.animate.set_value(0) for k in ks], lag_ratio=0.15),
                  gop.animate.set_value(0.0), FadeOut(sl), FadeOut(ln), FadeOut(cl), FadeOut(cln), FadeOut(cdots),
                  run_time=1.3)
        self.play(FadeOut(spray), run_time=0.35)
        self.wait(1.2)
        self.finish()


CAT_OFFS = frag_offsets(40, 21, 0.4)


class S16Cat(SpokenScene):
    def construct(self):
        bd, tip = axon_body(), axon_tip()
        pieces = axon_pieces()
        st = Strip(SXT)
        self.add(bd, tip, pieces)
        st.base(self)
        self.add(st.bar(SX0, SXL, GREY), st.bar(SXL, SXT, TEAL), st.lab1, st.lab2, st.ph)
        drive_ph(self, st.ph, SXT, SX1, 0.5, 3.7)
        self.add(trail(st.ph, SXT, SX1, RED))
        self.at("axon fragments", lead=0.3)
        self.play(*frag_anim(pieces, CAT_OFFS, RED), tip.animate.shift(P(0.1, -0.3)).set_color(RED), run_time=1.4)
        self.at("catastrophic phase", lead=0.3)
        self.play(FadeIn(st.lab3, shift=UP * 0.1), run_time=0.6)
        self.finish()


def cat_final():
    bd, tip = axon_body(), axon_tip()
    pieces = axon_pieces()
    st = Strip(SX1)
    frag_now(pieces, CAT_OFFS, RED)
    tip.shift(P(0.1, -0.3)).set_color(RED)
    return bd, pieces, tip, st


class S16Beat(NarratedScene):
    def construct(self):
        bd, pieces, tip, st = cat_final()
        self.add(bd, pieces, tip)
        st.base(self)
        self.add(*st.full_bars(3), st.lab1, st.lab2, st.lab3, st.ph)
        self.finish()


def strip_group(st):
    return VGroup(st.arrow, st.time, st.tick, st.ngf, *st.full_bars(3), st.lab1, st.lab2, st.lab3, st.ph)


def column(x0, x1, color):
    top, bot = CY + 1.1, SY - 0.4
    return Rectangle(width=x1 - x0, height=top - bot, stroke_color=color, stroke_width=2.5, fill_color=color,
                     fill_opacity=0.07).move_to(P((x0 + x1) / 2, (top + bot) / 2))


def p75_block():
    t = T("p75", 44, PINK, weight=BOLD)
    s = T("needed for spheroid formation", 28, TEXT)
    return VGroup(t, s).arrange(DOWN, buff=0.1).move_to(P(1.4, 2.85))


def dr6_block():
    # Keep the whole DR6 explanation inside the catastrophic column, below the axon.
    t = T("DR6", 38, TEXT, weight=BOLD)
    s1 = T("needed for", 22, TEXT)
    s2 = T("catastrophic\ndegeneration", 22, TEXT, line_spacing=0.8)
    return VGroup(t, s1, s2).arrange(DOWN, buff=0.12).move_to(P(4.15, -0.65))


def static_axon(ks=(1, 1, 1), gop=0.35):
    return axon_group(list(ks), gop)


class S17P75(SpokenScene):
    def construct(self):
        bd, pieces, tip, st = cat_final()
        self.add(bd, pieces, tip)
        st.base(self)
        self.add(*st.full_bars(3), st.lab1, st.lab2, st.lab3, st.ph)
        ks = [ValueTracker(0) for _ in BUMPS]
        gop = ValueTracker(0.35)
        ax = always_redraw(lambda: axon_group([k.get_value() for k in ks], gop.get_value()))
        new_tip = axon_tip()
        self.play(FadeOut(pieces), FadeOut(tip), FadeIn(ax), FadeIn(new_tip), run_time=0.8)
        self.at("split the work")
        ct, cr = column(SXL, SXT, TEAL), column(SXT, SX1, RED)
        self.play(FadeIn(ct), FadeIn(cr), Indicate(st.lab2, color=TEAL, scale_factor=1.2),
                  Indicate(st.lab3, color=RED, scale_factor=1.2), run_time=1.0)
        self.at("p75 is", lead=0.1)
        blk = p75_block()
        self.play(FadeIn(blk[0], shift=DOWN * 0.1), run_time=0.5)
        self.at("needed for", lead=0.2)
        self.play(FadeIn(blk[1], shift=DOWN * 0.1), run_time=0.5)
        self.at("spheroid")
        self.play(LaggedStart(*[k.animate.set_value(1) for k in ks], lag_ratio=0.25), run_time=1.0)
        self.finish()


def s17_state(scene):
    """Everything on screen at the end of s17."""
    bd, tip, st = axon_body(), axon_tip(), Strip(SX1)
    ax = static_axon()
    ct, cr = column(SXL, SXT, TEAL), column(SXT, SX1, RED)
    blk = p75_block()
    sg = strip_group(st)
    scene.add(ct, cr, bd, ax, tip, sg, blk)
    return dict(bd=bd, tip=tip, st=st, ax=ax, ct=ct, cr=cr, blk=blk, sg=sg)


def s18_extras():
    dr = dr6_block()
    dar = Arrow(P(4.15, -1.45), P(4.15, SY + 0.3), buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
    med = chip("medium from\ndeprived axons", GREY, size=28, pad=0.14).move_to(P(-4.0, 2.85))
    hl = Line(med.get_right() + RIGHT * 0.05, P(4.15, 2.85), color=RED, stroke_width=5)
    va = Arrow(P(4.15, 2.85), P(4.15, 1.5), buff=0, color=RED, stroke_width=5, tip_length=0.22)
    sp = T("speeds up the breakdown", 28, RED).move_to(P(0.8, 3.22))
    return dr, dar, med, hl, va, sp


class S18Dr6(SpokenScene):
    def construct(self):
        S = s17_state(self)
        dr, dar, med, hl, va, sp = s18_extras()
        self.play(FadeOut(S["blk"][1]), S["blk"][0].animate.scale(0.7).move_to(P(1.4, 2.45)).set_opacity(1),
                  S["ct"].animate.set_fill(TEAL, 0.03).set_stroke(TEAL, 2.5, opacity=0.35),
                  S["cr"].animate.set_fill(RED, 0.18), FadeIn(dr[0], shift=UP * 0.1), run_time=0.8)
        self.at("needed for the")
        self.play(FadeIn(dr[1], shift=UP * 0.1), FadeIn(dr[2], shift=UP * 0.1), GrowArrow(dar),
                  Indicate(S["st"].lab3, color=RED, scale_factor=1.2), run_time=0.9)
        self.at("medium from")
        self.play(FadeIn(med, shift=DOWN * 0.1), run_time=0.6)
        self.at("speeds up")
        self.play(Create(hl), FadeIn(sp, shift=RIGHT * 0.1), run_time=0.6)
        self.play(GrowArrow(va), run_time=0.3)
        self.finish()


class S19Gate(SpokenScene):
    def construct(self):
        S = s17_state(self)
        dr, dar, med, hl, va, sp = s18_extras()
        S["blk"][0].scale(0.7).move_to(P(1.4, 2.45)).set_opacity(1)
        S["blk"][1].set_opacity(0)
        S["ct"].set_fill(TEAL, 0.03).set_stroke(TEAL, 2.5, opacity=0.35)
        S["cr"].set_fill(RED, 0.18)
        old = VGroup(S["blk"][0], dr, dar, med, hl, va, sp, S["ct"], S["cr"])
        self.add(dr, dar, med, hl, va, sp)
        self.play(FadeOut(old), run_time=0.6)
        self.at("model is that")
        mod = T("the laboratory's model", 38, GOLD).move_to(P(0, 3.2))
        self.play(FadeIn(mod, shift=DOWN * 0.1), run_time=0.6)
        self.at("gate the step", lead=0.7)
        sl = T("spheroids", 30, TEAL).move_to(P(1.5, 2.58))
        ln = leader(P(1.5, 2.12), P(1.5, 2.33), TEAL)
        self.play(FadeIn(sl, shift=DOWN * 0.1), Create(ln), Indicate(S["ax"], color=TEAL, scale_factor=1.0),
                  run_time=0.5)
        self.at("gate the step")
        door = Rectangle(width=0.36, height=2.0, stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                         fill_opacity=0.85).move_to(P(SXT, CY))
        dash = DashedLine(P(SXT, CY - 1.0), P(SXT, SY + 0.3), color=GOLD, stroke_width=4)
        hinge = Dot(P(SXT, CY + 1.0), radius=0.12, color=GOLD)
        gl = T("gate", 32, GOLD).move_to(P(SXT + 0.75, 2.25))
        self.play(GrowFromEdge(door, DOWN), FadeIn(hinge), Create(dash), FadeIn(gl, shift=DOWN * 0.1), run_time=0.5)
        self.at("from waiting")
        self.play(Indicate(S["st"].lab1, color=TEXT, scale_factor=1.25), run_time=0.4)
        self.at("to catastrophe")
        self.play(Rotate(door, angle=PI / 2, about_point=hinge.get_center()), FadeOut(gl),
                  Indicate(S["st"].lab3, color=RED, scale_factor=1.25), run_time=0.8)
        self.at("not yet a settled", lead=0.3)
        ns = T("not yet a settled mechanism", 30, GREY).move_to(P(0.2, -0.45))
        self.play(FadeIn(ns, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Take(SpokenScene):
    def construct(self):
        # row 1: where support is lost picks the branch (the lost branch holds zero NGF)
        y1 = 1.75
        trunk = Line(P(-6.2, y1), P(-4.9, y1), color=BLUE, stroke_width=16)
        bt = Line(P(-4.9, y1), P(-1.9, y1 + 0.95), color=BLUE, stroke_width=16)
        bb = Line(P(-4.9, y1), P(-1.9, y1 - 0.95), color=BLUE, stroke_width=16)
        dts = VGroup(ndot((-1.35, y1 + 1.2), YELLOW, 0.17), ndot((-1.25, y1 + 0.75), YELLOW, 0.17),
                     ndot((-1.4, y1 + 0.3), YELLOW, 0.17))
        zero = T("0 NGF", 28, GREY).move_to(P(-1.35, y1 - 1.45))
        ic1 = VGroup(trunk, bt, bb)
        t1 = T("Where support is lost", 42, TEXT, font=TITLE_FONT).move_to(P(0, y1 + 0.3)).align_to(P(0.2, 0), LEFT)
        t1b = T("decides what is lost.", 42, TEXT, font=TITLE_FONT).next_to(t1, DOWN, buff=0.25, aligned_edge=LEFT)
        # row 2: in a contest the winner helps decide
        y2 = -1.8
        w = Circle(radius=0.75, stroke_color=GREEN, stroke_width=6, fill_color=GREEN, fill_opacity=0.35).move_to(P(-5.2, y2))
        l = Circle(radius=0.75, stroke_color=BLUE, stroke_width=6, fill_color=BLUE, fill_opacity=0.35).move_to(P(-1.9, y2))
        arr = Arrow(w.get_right() + RIGHT * 0.1, l.get_left() - RIGHT * 0.1, buff=0, color=PINK, stroke_width=7, tip_length=0.28)
        alab = T("BDNF", 28, PINK).next_to(arr, UP, buff=0.15)
        t2 = T("In a contest, the winner", 42, TEXT, font=TITLE_FONT).move_to(P(0, y2 + 0.3)).align_to(P(0.2, 0), LEFT)
        t2b = T("helps decide too.", 42, TEXT, font=TITLE_FONT).next_to(t2, DOWN, buff=0.25, aligned_edge=LEFT)
        VGroup(ic1, dts, zero).scale(1.08).move_to(P(-3.65, 1.6))
        VGroup(w, l, arr, alab).scale(1.12).move_to(P(-3.65, -1.85))
        self.play(Create(ic1), FadeIn(dts, scale=0.4), FadeIn(t1, shift=RIGHT * 0.15), run_time=0.4)
        self.at("support is lost", lead=0.1)
        self.play(FadeIn(zero, shift=UP * 0.1), run_time=0.5)
        self.at("decides what")
        self.play(FadeIn(t1b, shift=RIGHT * 0.15), run_time=0.4)
        self.at("what is lost")
        self.play(bb.animate.set_color(RED).set_opacity(0.5), zero.animate.set_color(RED), run_time=0.8)
        self.at("In a contest")
        self.play(FadeIn(w, scale=0.6), FadeIn(l, scale=0.6), FadeIn(t2, shift=RIGHT * 0.15), run_time=0.8)
        self.at("the winner helps")
        self.play(GrowArrow(arr), FadeIn(alab), FadeIn(t2b, shift=RIGHT * 0.15), run_time=0.8)
        self.play(l.animate.set_stroke(RED).set_fill(RED, 0.45), run_time=0.7)
        self.finish()


class S21End(EndCard):
    LINE = "Where support is lost decides what is lost.\nIn a contest, the winner helps decide too."

    def construct(self):
        a, b = self.LINE.split("\n")
        l1, l2 = T(a, 40, TEXT, font=TITLE_FONT), T(b, 40, TEXT, font=TITLE_FONT)
        g = VGroup(l1, l2).arrange(DOWN, buff=0.5)
        fit(g, max_w=11.8)
        sub = T("biochemistrypedia.com", 26, TEAL)
        VGroup(g, sub).arrange(DOWN, buff=0.6)
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=self.beat(0.25))
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=self.beat(0.25))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
