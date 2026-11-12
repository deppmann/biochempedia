"""Selection Has an Agent (film 1 of 2, Ecology and Evolution), re-authored 2026-11-11.

THE WORLD (kept for both films): trunk at the left (x -5.6..0.4), a right-hand panel (x 1..6.6) that holds
the dial, the survivors bars and the labels.
COLOR MAP
  CREAM  = the pale morph (typica)      CHAR = the dark morph (carbonaria, thin white outline)
  BLUE   = birds (the agent)            YELLOW = the dial, ratio and highlights
  GREEN  = environment / deep beaks     TEAL = inheritance
  RED    = "not this" readings, drought
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

CREAM = "#F1E6C8"
CHAR = "#2B2B2E"
SOOT = "#1E1C22"
BARK = "#7A7262"
LICH = "#A9B79B"
TX = -2.6     # trunk centre x
PX = 3.9      # right panel centre x
HOME = np.array([0.5, 2.65, 0.0])   # where the bird hovers

# resting places of the moths on the trunk (idx: colour, x, y)
MP = {0: (CREAM, -4.4, 2.1), 1: (CHAR, -1.6, 2.4), 2: (CREAM, -1.7, -0.3), 3: (CHAR, -3.9, 0.2),
      4: (CREAM, -3.7, -2.5), 5: (CHAR, -1.3, -2.6), 6: (CHAR, -2.9, 1.2), 7: (CHAR, -4.6, -1.4),
      8: (CREAM, -2.9, -1.3), 9: (CREAM, -4.5, 0.9)}


def moth(color, s=1.0):
    edge = TEXT if color == CHAR else "#B8AC88"
    kw = dict(fill_color=color, fill_opacity=0.97, stroke_color=edge, stroke_width=1.6)
    w1 = Ellipse(width=0.62, height=0.34, **kw).shift(LEFT * 0.3 + UP * 0.05).rotate(0.25)
    w2 = Ellipse(width=0.62, height=0.34, **kw).shift(RIGHT * 0.3 + UP * 0.05).rotate(-0.25)
    b = Ellipse(width=0.16, height=0.5, **kw).shift(DOWN * 0.03)
    return VGroup(w1, w2, b).scale(s)


def make_moths(ids, s=1.3):
    return {i: moth(MP[i][0], s).move_to([MP[i][1], MP[i][2], 0]) for i in ids}


def bird(s=1.5):
    body = Ellipse(width=0.65, height=0.42, color=BLUE, fill_opacity=1)
    head = Circle(radius=0.17, color=BLUE, fill_opacity=1).shift(RIGHT * 0.32 + UP * 0.19)
    beak = Polygon([0.45, 0.23, 0], [0.72, 0.13, 0], [0.45, 0.06, 0], color=BLUE, fill_opacity=1)
    tail = VGroup(*[Line([-0.23 + d, -0.1, 0], [-0.48 + d, -0.7, 0], color=BLUE, stroke_width=7) for d in (-0.08, 0.08)])
    return VGroup(body, head, beak, tail).scale(s).flip(RIGHT * 0) if False else VGroup(body, head, beak, tail).scale(s)


def hover(b):
    b.base = b.get_center().copy()
    b.tt = 0.0

    def u(m, dt):
        m.tt += dt
        m.move_to(m.base + np.array([0.12 * np.sin(m.tt * 1.7), 0.1 * np.sin(m.tt * 2.3), 0]))
    b.add_updater(u)


def make_trunk(L=1.0):
    base = RoundedRectangle(width=6.0, height=7.4, corner_radius=0.25, stroke_color=GREY, stroke_width=2,
                            fill_opacity=1, fill_color=BARK).move_to([TX, 0, 0])
    rng = random.Random(4)
    patches = VGroup(*[Ellipse(width=rng.uniform(.5, 1.1), height=rng.uniform(.3, .6), fill_color=LICH,
                               fill_opacity=.8, stroke_width=0).move_to([TX + rng.uniform(-2.6, 2.6), rng.uniform(-3.3, 3.3), 0])
                       for _ in range(24)])
    g = VGroup(base, patches)
    g.L = ValueTracker(L)
    g.t = 0.0

    def upd(m, dt):
        m.t += dt
        l = m.L.get_value()
        base.set_fill(interpolate_color(ManimColor(SOOT), ManimColor(BARK), l))
        for i, p in enumerate(patches):
            p.set_fill(opacity=l * (0.7 + 0.15 * np.sin(m.t * 1.3 + i)))
    g.add_updater(upd, call_updater=True)
    return g


def make_smoke():
    rng = random.Random(7)
    g = VGroup()
    for _ in range(8):
        e = Ellipse(width=rng.uniform(1.6, 2.6), height=rng.uniform(.8, 1.3), fill_color="#8C8C97",
                    fill_opacity=0, stroke_width=0).move_to([rng.uniform(-4.2, 0.6), rng.uniform(-3.2, 3.2), 0])
        e.v = rng.uniform(.5, .9)
        g.add(e)
    g.a = ValueTracker(0.0)

    def u(m, dt):
        for e in m:
            e.shift(RIGHT * e.v * dt)
            if e.get_x() > 1.0:
                e.shift(LEFT * 5.4)
            e.set_fill(opacity=m.a.get_value() * 0.4)
    g.add_updater(u)
    return g


class Gauge:
    """Dial + survivors bars, both driven by the same two trackers (survival of pale and dark)."""

    def __init__(self, sp, sd, wob=0.0):
        C = np.array([PX, 0.6, 0.0])
        Rr = 1.6
        self.sp, self.sd, self.wob = ValueTracker(sp), ValueTracker(sd), ValueTracker(wob)
        arc = Arc(radius=Rr, start_angle=0, angle=PI, arc_center=C, color=GREY, stroke_width=6)
        tick = Line(C + UP * (Rr - .3), C + UP * (Rr + .12), color=YELLOW, stroke_width=6)
        one = T("1", 30, YELLOW).move_to(C + UP * (Rr + .42))
        cap = T("dark ÷ pale survival", 26).move_to(C + DOWN * .45)
        tag = T("schematic", 22, GREY).move_to(C + DOWN * .85)
        needle = Line(C, C + UP * 1.4, color=YELLOW, stroke_width=8)
        needle.tt = 0.0
        pivot = Dot(C, radius=.1, color=YELLOW)

        def nu(m, dt):
            m.tt += dt
            r = max(self.sd.get_value() / max(self.sp.get_value(), 1e-3), 0.26)
            a = PI / 2 - np.log2(min(r, 3.9)) * PI / 4 + self.wob.get_value() * np.sin(m.tt * 9)
            m.put_start_and_end_on(C, C + 1.4 * np.array([np.cos(a), np.sin(a), 0]))
        needle.add_updater(nu, call_updater=True)
        self.dial = VGroup(arc, tick, one, needle, pivot, cap, tag)
        bp = Rectangle(width=1.2, height=1, fill_color=CREAM, fill_opacity=.95, stroke_color=TEXT, stroke_width=2)
        bd = Rectangle(width=1.2, height=1, fill_color=CHAR, fill_opacity=.95, stroke_color=TEXT, stroke_width=2)

        def bu(tr, x):
            def f(m):
                h = max(2.3 * tr.get_value(), 0.03)
                m.stretch_to_fit_height(h)
                m.move_to([x, -3.0 + h / 2, 0])
            return f
        bp.add_updater(bu(self.sp, PX - 1.1), call_updater=True)
        bd.add_updater(bu(self.sd, PX + 1.1), call_updater=True)
        lp = T("pale", 28).move_to([PX - 1.1, -3.45, 0])
        ld = T("dark", 28).move_to([PX + 1.1, -3.45, 0])
        self.bars = VGroup(bp, bd, lp, ld)
        self.bp, self.bd = bp, bd

    def set(self, sp, sd, rt=1.6):
        return AnimationGroup(self.sp.animate.set_value(sp), self.sd.animate.set_value(sd), run_time=rt)


def swoop(sc, b, m, extra=(), rt=0.6, start=None):
    b.clear_updaters()
    if start is not None:
        b.move_to(start)
        sc.add(b)
    sc.play(b.animate.move_to(m.get_center() + UP * 0.55 + RIGHT * 0.5), run_time=rt)
    sc.play(FadeOut(m, scale=0.3), *[FadeOut(e) for e in extra], b.animate.move_to(HOME), run_time=rt)
    hover(b)


def cross(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=6),
                  Line(mob.get_corner(UR), mob.get_corner(DL), color=color, stroke_width=6))


def sun():
    return VGroup(Circle(radius=.3, color=RED, fill_opacity=.5),
                  *[Line(.42 * np.array([np.cos(a), np.sin(a), 0]), .63 * np.array([np.cos(a), np.sin(a), 0]), color=RED)
                    for a in np.arange(0, TAU, TAU / 8)])


def chunk(lines, size, color=TEXT, gap=.15):
    return VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=gap)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Natural Selection in Ecological Context"
    TITLE = "Selection Has an Agent"


class S01Question(SpokenScene):
    def construct(self):
        tr = make_trunk(1.0)
        M_ = make_moths([0, 1, 2, 3, 4, 5])
        b = bird()
        self.play(FadeIn(tr), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in M_.values()], lag_ratio=0.15), run_time=0.9)
        self.at("dark moths")
        swoop(self, b, M_[1], rt=0.9, start=[7.5, 3.4, 0])
        eh = T("eaten by birds", 32, BLUE).move_to([PX, 2.3, 0])
        er1 = VGroup(*[moth(CHAR, .9).move_to([2.6 + 1.2 * i, 1.4, 0]) for i in range(3)])
        er2 = VGroup(moth(CREAM, .9).move_to([2.6, .5, 0]))
        self.at("than pale ones")
        self.play(FadeIn(eh), LaggedStart(*[FadeIn(m, scale=.5) for m in er1], lag_ratio=.25), FadeIn(er2, scale=.5), run_time=1.2)
        q = T("Is that evolution?", 44).move_to([PX, -1.0, 0])
        self.at("Is that evolution")
        self.play(Write(q), run_time=1.0)
        n = T("Not yet.", 52, YELLOW).move_to([PX, -2.3, 0])
        self.at("Not yet")
        self.play(FadeIn(n, scale=1.2), run_time=0.6)
        self.at("This film builds")
        self.play(FadeOut(q), FadeOut(n), FadeOut(eh), FadeOut(er1), FadeOut(er2), run_time=0.6)
        boxes = VGroup(*[RoundedRectangle(corner_radius=.12, width=1.1, height=1.1, stroke_color=GOLD, stroke_width=4,
                                          fill_color=GOLD, fill_opacity=.12).move_to([1.9 + 1.4 * i, 0.4, 0]) for i in range(4)])
        self.at("the answer")
        self.play(LaggedStart(*[FadeIn(x, scale=.6) for x in boxes], lag_ratio=.6), run_time=1.8)
        self.finish()


class S02Morphs(SpokenScene):
    def construct(self):
        tr = make_trunk(1.0)
        M_ = make_moths([0, 1, 2, 3, 4, 5])
        self.add(tr, *M_.values())
        bigP = moth(CREAM, 2.1).move_to([2.5, 0.9, 0])
        bigD = moth(CHAR, 2.1).move_to([5.3, 0.9, 0])
        self.at("Meet the peppered")
        self.play(TransformFromCopy(M_[0], bigP), TransformFromCopy(M_[1], bigD), run_time=1.3)
        self.at("two main")
        self.play(Indicate(bigP, scale_factor=1.12), Indicate(bigD, scale_factor=1.12), run_time=1.0)
        d = chunk(["morph = one distinct form", "within a species"], 28, YELLOW).move_to([PX, 3.0, 0])
        self.at("A morph is one distinct form")
        self.play(FadeIn(d), run_time=0.8)
        labP = chunk(["typica", "pale morph"], 32, CREAM, .1).move_to([2.5, -0.85, 0])
        self.at("The pale morph is called")
        self.play(FadeIn(labP, shift=UP * .15), run_time=0.7)
        labD = chunk(["carbonaria", "dark morph"], 32, TEXT, .1).move_to([5.3, -0.85, 0])
        self.at("The dark morph is called")
        self.play(FadeIn(labD, shift=UP * .15), run_time=0.7)
        mid = moth("#8A8474", 1.2).move_to([PX, -2.35, 0])
        tg = T("intermediates exist", 28).move_to([PX, -3.2, 0])
        self.at("Intermediate moths exist")
        self.play(FadeIn(mid, scale=.6), FadeIn(tg), run_time=0.8)
        self.at("Both rest by day")
        self.play(LaggedStart(*[Indicate(m, color=YELLOW, scale_factor=1.25) for m in M_.values()], lag_ratio=.18), run_time=1.8)
        self.finish()


class S03Agent(SpokenScene):
    def construct(self):
        tr = make_trunk(1.0)
        M_ = make_moths([0, 1, 2, 3, 4, 5])
        b = bird()
        b.move_to([7.5, 3.4, 0])
        self.add(tr, *M_.values(), b)
        self.at("Birds hunt")
        self.play(b.animate.move_to(HOME), run_time=1.2)
        hover(b)
        rings = {i: Circle(radius=.75, color=YELLOW, stroke_width=4).move_to(M_[i]) for i in (1, 3, 5)}
        self.at("the dark morph stands")
        self.play(*[Create(r) for r in rings.values()], *[m.animate.set_opacity(.55) for i, m in M_.items() if i % 2 == 0], run_time=1.0)
        self.play(*[Indicate(M_[i], scale_factor=1.2, color=YELLOW) for i in (1, 3, 5)], run_time=1.0)
        self.at("So birds find")
        swoop(self, b, M_[1], extra=[rings[1]], rt=0.7)
        self.at("than pale ones")
        swoop(self, b, M_[3], extra=[rings[3]], rt=0.7)
        ca = chip("agent: birds", BLUE, 28).move_to([4.6, 3.1, 0])
        ar = Arrow([3.0, 3.1, 0], [1.6, 3.05, 0], color=BLUE, buff=0)
        self.at("The bird is the agent")
        self.play(FadeIn(ca), GrowArrow(ar), run_time=0.8)
        ce = chip("environment:\nlichen bark", GREEN, 28).move_to([4.3, -0.4, 0])
        ar2 = Arrow([2.7, -0.4, 0], [0.5, -0.4, 0], color=GREEN, buff=0)
        self.at("The lichen")
        self.play(FadeIn(ce), GrowArrow(ar2), run_time=0.9)
        self.play(Indicate(tr[0], color=GREEN, scale_factor=1.01), run_time=1.2)
        self.finish()


class S04Ratio(SpokenScene):
    def construct(self):
        tr = make_trunk(1.0)
        M_ = make_moths([0, 1, 2, 3, 4, 5])
        b = bird()
        b.move_to(HOME)
        hover(b)
        self.add(tr, *M_.values(), b)
        G = Gauge(.7, .7)
        f1 = T("Fitness", 48, YELLOW)
        f2 = T("reproductive success", 32)
        f3 = chunk(["compared with", "other variants"], 32)
        F = VGroup(f1, f2, f3).arrange(DOWN, buff=.3).move_to([PX, 0.5, 0])
        self.at("Fitness is reproductive")
        self.play(Write(f1), run_time=0.7)
        self.at("reproductive success")
        self.play(FadeIn(f2, shift=UP * .1), run_time=0.7)
        self.at("compared with other")
        self.play(FadeIn(f3, shift=UP * .1), run_time=0.8)
        self.at("Here we measure")
        self.play(FadeOut(F), run_time=0.6)
        s = chunk(["survival", "through a day"], 44, GREEN).move_to([PX, 0.6, 0])
        self.at("survival through a day")
        self.play(FadeIn(s, scale=.9), run_time=0.8)
        self.at("A dial shows")
        self.play(FadeOut(s), run_time=0.4)
        self.play(FadeIn(G.dial), run_time=1.4)
        self.at("dark survival divided")
        self.play(FadeIn(G.bars), run_time=1.2)
        self.at("On lichen")
        swoop(self, b, M_[1], rt=0.6)
        self.play(G.set(.85, .5, 1.6))
        fd = chip("fitness difference", YELLOW, 28).move_to([PX, 3.2, 0])
        self.at("Fitness is relative")
        self.play(FadeIn(fd), run_time=0.7)
        self.at("What matters is how one morph")
        self.play(Indicate(G.bp, scale_factor=1.06), Indicate(G.bd, scale_factor=1.06), run_time=1.4)
        box = SurroundingRectangle(tr[0], color=GOLD, buff=0.04, stroke_width=5)
        self.at("in the same place")
        self.play(Create(box), run_time=1.0)
        self.finish()


class S05Soot(SpokenScene):
    def construct(self):
        tr = make_trunk(1.0)
        M_ = make_moths([0, 1, 2, 3, 4, 5])
        b = bird()
        b.move_to(HOME)
        hover(b)
        G = Gauge(.85, .5)
        self.add(tr, *M_.values(), b, G.dial, G.bars)
        smoke = make_smoke()
        self.at("not the moths")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.2) for m in M_.values()], lag_ratio=.12), run_time=1.2)
        tag = chip("19th century,\nindustrial Britain", YELLOW, 24, pad=.12).move_to([PX, 3.25, 0])
        self.at("In the 19th century")
        self.play(FadeIn(tag), run_time=0.8)
        self.add(smoke)
        self.at("air pollution killed")
        self.play(smoke.a.animate.set_value(1.0), run_time=1.0)
        self.at("the lichens")
        self.play(tr.L.animate.set_value(0.0), run_time=4.6, rate_func=linear)
        self.at("On dark bark")
        swoop(self, b, M_[0], rt=0.6)
        self.at("stands out instead")
        swoop(self, b, M_[2], rt=0.6)
        self.at("The dial swings above")
        self.play(G.set(.5, .85, 1.8))
        n6, n7 = make_moths([6, 7])[6], make_moths([6, 7])[7]
        self.at("the dark morph became common")
        self.play(FadeIn(n6, scale=.5), FadeIn(n7, scale=.5), smoke.a.animate.set_value(0.0), run_time=1.2)
        self.finish()


def soot_state(sc, L, ratio, wob=0.0, q=None):
    tr = make_trunk(L)
    M_ = make_moths([1, 3, 4, 5, 6, 7])
    b = bird()
    b.move_to(HOME)
    hover(b)
    G = Gauge(ratio[0], ratio[1], wob)
    sc.add(tr, *M_.values(), b, G.dial, G.bars)
    return tr, M_, b, G


class S06Predict(SpokenScene):
    def construct(self):
        tr, M_, b, G = soot_state(self, 0.0, (.5, .85))
        tag = chip("19th century,\nindustrial Britain", YELLOW, 24, pad=.12).move_to([PX, 3.25, 0])
        self.add(tag)
        tag2 = chip("late 20th century", YELLOW, 24, pad=.12).move_to([PX, 3.25, 0])
        self.at("Then, in the late")
        self.play(Transform(tag, tag2), run_time=0.8)
        self.at("air pollution fell")
        self.play(G.set(.7, .7, 2.2))
        self.at("lichens grew back")
        self.play(tr.L.animate.set_value(1.0), run_time=2.4, rate_func=linear)
        q = T("Which morph now?", 36, YELLOW).move_to([4.2, 3.3, 0])
        self.at("Which morph")
        self.play(FadeOut(tag), G.wob.animate.set_value(.12), run_time=0.4)
        self.play(FadeIn(q), run_time=0.4)
        self.finish()


class S07Pause(SpokenScene):
    def construct(self):
        tr, M_, b, G = soot_state(self, 1.0, (.7, .7), wob=.12)
        q = T("Which morph now?", 36, YELLOW).move_to([4.2, 3.3, 0])
        prog = ValueTracker(0.0)
        C = np.array([6.3, 2.2, 0])
        back = Circle(radius=.28, color=GREY, stroke_width=3).move_to(C)
        ring = always_redraw(lambda: Arc(radius=.28, start_angle=PI / 2, angle=-max(TAU * (1 - prog.get_value()), 0.01),
                                         arc_center=C, color=YELLOW, stroke_width=6))
        self.add(q, back, ring)
        self.play(prog.animate.set_value(1.0), run_time=4.9, rate_func=linear)
        self.finish()


class S08Reveal(SpokenScene):
    def construct(self):
        tr, M_, b, G = soot_state(self, 1.0, (.7, .7), wob=.12)
        q = T("Which morph now?", 36, YELLOW).move_to([4.2, 3.3, 0])
        self.add(q)
        self.at("The dark morph again")
        self.play(FadeOut(q), run_time=0.4)
        swoop(self, b, M_[1], rt=0.6)
        self.at("It stands out on lichen")
        swoop(self, b, M_[3], rt=0.6)
        self.at("so the dial swings back")
        self.play(G.wob.animate.set_value(0.0), G.set(.85, .5, 1.8))
        self.at("carbonaria declined")
        self.play(*[FadeOut(M_[i], scale=.3) for i in (5, 6, 7)], run_time=1.0)
        t1 = T("Same moth, same birds", 30, YELLOW).move_to([4.2, 3.5, 0])
        self.at("Same moth")
        self.play(FadeIn(t1), run_time=0.7)
        t2 = T("different environment", 30, GREEN).move_to([4.2, 3.0, 0])
        self.at("A different environment")
        self.play(FadeIn(t2), run_time=0.7)
        newc = make_moths([8, 9])
        self.at("a different color")
        self.play(FadeIn(newc[8], scale=.5), FadeIn(newc[9], scale=.5), run_time=0.9)
        t3 = T("fitness: moth + place", 32, YELLOW).move_to([4.2, 3.3, 0])
        box = SurroundingRectangle(tr[0], color=GOLD, buff=0.04, stroke_width=5)
        self.at("Fitness belongs to the moth")
        self.play(FadeOut(t1), FadeOut(t2), FadeIn(t3), Create(box), run_time=1.0)
        self.finish()


class S09Sieve(SpokenScene):
    def construct(self):
        tr = make_trunk(1.0)
        M_ = make_moths([2, 4, 8, 9, 5])
        b = bird()
        b.move_to(HOME)
        hover(b)
        self.add(tr, *M_.values(), b)
        self.at("Notice what the birds")
        self.play(Indicate(b, scale_factor=1.25), run_time=1.2)
        o1 = moth(CREAM, 1.2).set_opacity(.4).move_to([3.0, 0.7, 0])
        o2 = moth(CHAR, 1.2).set_opacity(.5).move_to([4.8, 0.7, 0])
        x1, x2 = cross(o1), cross(o2)
        nt = T("no new moths made", 34, RED).move_to([PX, -0.6, 0])
        self.at("They did not make")
        self.play(FadeIn(o1), FadeIn(o2), run_time=0.6)
        self.play(Create(x1), Create(x2), FadeIn(nt), run_time=0.8)
        # the sieve
        sx, sy = PX, 0.0
        frame = Rectangle(width=5.4, height=1.2, stroke_color=GREY, stroke_width=6).move_to([sx, sy, 0])
        mesh = VGroup(*[Line([sx - 2.7 + .45 * k, sy - .6, 0], [sx - 2.7 + .45 * k, sy + .6, 0], stroke_color=GREY, stroke_width=2) for k in range(1, 12)],
                      Line([sx - 2.7, sy, 0], [sx + 2.7, sy, 0], stroke_color=GREY, stroke_width=2))
        sieve = VGroup(frame, mesh)
        self.at("Like a sieve")
        self.play(FadeOut(o1), FadeOut(o2), FadeOut(x1), FadeOut(x2), FadeOut(nt), run_time=0.6)
        self.play(Create(frame), Create(mesh), run_time=1.2)
        cols = [CREAM, CHAR, CREAM, CHAR, CREAM]
        ms = [moth(c, .85).move_to([sx - 2.1 + 1.05 * i, 3.4, 0]) for i, c in enumerate(cols)]
        rest = [sy + .6 + .4]
        self.at("sorted moths that already existed")
        self.play(LaggedStart(*[m.animate.move_to([m.get_x(), rest[0], 0]) for m in ms], lag_ratio=.12), run_time=2.0)
        fall = [ms[1], ms[3]]
        self.play(*[m.animate.shift(DOWN * 2.4).set_opacity(0) for m in fall], run_time=1.4)
        sel = chunk(["selection = sorting", "within one generation"], 32, YELLOW).move_to([PX, -2.4, 0])
        self.at("That sorting within one generation")
        self.play(FadeIn(sel), run_time=0.9)
        sun_ = sun().scale(1.0).move_to([6.2, 3.0, 0])
        self.at("A drought does not create")
        keep = [m for m in ms if m not in fall]
        self.play(*[FadeOut(m) for m in keep], FadeOut(sel), FadeIn(sun_), run_time=0.8)
        beaks = []
        for i in range(6):
            deep = i < 3
            h = .42 if deep else .15
            bk = Polygon([-.4, h, 0], [.5, 0, 0], [-.4, -h, 0], color=GREEN if deep else BLUE, fill_opacity=.85).scale(1.0)
            bk.move_to([1.5 + .9 * i + .1, sy + .6 + .5, 0])
            beaks.append(bk)
        ld = T("deep", 30, GREEN).move_to([2.6, 2.2, 0])
        ls = T("shallow", 30, BLUE).move_to([5.1, 2.2, 0])
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * .3) for k in beaks], lag_ratio=.1), FadeIn(ld), FadeIn(ls), run_time=1.2)
        self.at("It removes more of the shallow")
        self.play(*[beaks[i].animate.shift(DOWN * 2.4).set_opacity(0) for i in (3, 5)], Indicate(ls, color=BLUE), run_time=1.4)
        self.finish()


def surv_row(y, col, qcol):
    xs = [-5.6, -4.0, -2.4]
    cs = [CREAM, CREAM, CHAR]
    surv = VGroup(*[moth(c, 1.3).move_to([x, y, 0]) for x, c in zip(xs, cs)])
    arrow = Arrow([-1.5, y, 0], [-0.1, y, 0], color=col, buff=0, stroke_width=8)
    slots = VGroup(*[VGroup(Square(side_length=1.0, stroke_color=qcol, stroke_width=4, fill_opacity=0),
                            T("?", 40, qcol)).move_to([0.9 + 1.25 * i, y, 0]) for i in range(3)])
    return VGroup(surv, arrow, slots)


class S10Inherit(SpokenScene):
    def construct(self):
        tr = make_trunk(1.0)
        M_ = make_moths([2, 4, 8, 9, 5])
        self.add(tr, *M_.values())
        q = T("Is it evolution yet?", 40, YELLOW).move_to([PX, 3.3, 0])
        self.at("Is it evolution yet")
        self.play(Write(q), run_time=1.2)
        rowA = surv_row(0.4, GREY, GREY)
        cap = T("offspring resemble parents?", 32).move_to([0, -0.8, 0])
        self.at("Only if offspring")
        self.play(TransformFromCopy(VGroup(M_[2], M_[4], M_[5]), rowA[0]), FadeOut(tr), *[FadeOut(M_[i]) for i in (8, 9, 2, 4, 5)],
                  run_time=1.2)
        self.play(GrowArrow(rowA[1]), FadeIn(rowA[2]), FadeIn(cap), run_time=1.0)
        q2 = T("Two futures", 44, YELLOW).move_to([0, 3.3, 0])
        self.at("Picture two futures")
        top = surv_row(1.5, TEAL, TEAL)
        bot = surv_row(-1.7, GREY, GREY)
        self.play(FadeOut(cap), run_time=0.3)
        self.play(Transform(q, q2), Transform(rowA, top), TransformFromCopy(rowA, bot), run_time=1.1)
        tag1 = T("colour inherited", 32, TEAL).move_to([-4.7, 2.5, 0])
        cap1 = T("response depends on genotypes, mating and inheritance", 24).move_to([0, 0.65, 0])
        self.at("In one")
        self.play(FadeIn(tag1), FadeIn(cap1), run_time=0.9)
        self.at("and the young of the survivors")
        self.play(Indicate(rowA[1], color=TEAL, scale_factor=1.15), Indicate(rowA[2], color=TEAL), run_time=1.4)
        tag2 = T("schematic: if colour were not inherited", 28).move_to([-2.9, -0.45, 0])
        self.at("In the other")
        self.play(FadeIn(tag2), run_time=0.9)
        stamp = chip("no inherited\nresponse", GREY, 26).move_to([5.4, -1.7, 0])
        x = Line([-2.4, -1.5, 0], [-1.0, -1.9, 0], color=RED, stroke_width=0)
        self.at("so the shift need not")
        self.play(FadeIn(stamp, scale=1.5), run_time=0.7)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        ys = [2.4, 1.3, 0.2, -0.9]
        slots = VGroup(*[RoundedRectangle(corner_radius=.12, width=6.0, height=.85, stroke_color=GREY, stroke_width=3).move_to([-3.0, y, 0]) for y in ys])
        names = [("variation", GOLD), ("inheritance", TEAL), ("fitness difference", YELLOW), ("agent in an environment", BLUE)]
        chips = [chip(n, c, 30).move_to([-3.0, y, 0]) for (n, c), y in zip(names, ys)]
        self.at("four parts")
        self.play(LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=.2), run_time=1.2)
        self.at("Variation")
        self.play(FadeIn(chips[0], shift=LEFT * 3), run_time=0.8)
        self.at("inheritance")
        self.play(FadeIn(chips[1], shift=LEFT * 3), run_time=0.8)
        self.at("fitness difference")
        self.play(FadeIn(chips[2], shift=LEFT * 3), run_time=0.8)
        self.at("agent in an")
        self.play(FadeIn(chips[3], shift=LEFT * 3), run_time=0.8)
        c1 = chip("agent sorts\nvariants by fitness", BLUE, 30).move_to([3.9, 1.5, 0])
        self.at("An agent sorts")
        self.play(FadeIn(c1, shift=UP * .2), Indicate(chips[3], scale_factor=1.06), run_time=1.0)
        ar = Arrow([3.9, 0.7, 0], [3.9, -0.2, 0], color=TEAL, buff=0, stroke_width=8)
        c2 = chip("inheritance carries\nthe sorting forward", TEAL, 30).move_to([3.9, -1.2, 0])
        self.at("Inheritance carries")
        self.play(GrowArrow(ar), FadeIn(c2, shift=UP * .2), Indicate(chips[1], scale_factor=1.06), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "An agent sorts variants by fitness;\ninheritance carries the sorting forward."
