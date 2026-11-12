"""Emptying Islands  (island biogeography, film 2 of 2; Biochemistrypedia explainer)

COLOUR MAP (same as film 1)
  BLUE = immigration / arrivals      RED = local extinction / losses     GOLD = the crossing, S*
  Species tokens: small multicoloured dots (schematic).
  Mites: GREEN = Bdella (before and after), GREY = Amblyseius (before only), PURPLE = Carpoglyphus (after only).
All animals, islands and tents are cartoons (schematic). Curves in the recap are computed from
I(S) = 10(1 - S/100) and E(S) = 0.1 S. The recovery plot is labelled schematic, shape only.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PAL = ["#E07BE0", "#9B7BFF", "#4ED6A4", "#FF9F43", "#B8E04A", "#F78FB3", "#C69C6D", "#DDE6F0", "#2EC4B6", "#FFB4A2"]
PURPLE = "#9B7BFF"
SEA = "#2A8C99"
RIP = "#6FD0DA"
LAND = "#2E6B45"
LANDS = "#7FBF8A"
BROWN = "#8B5A2B"
ORDER = list(range(100))
random.Random(11).shuffle(ORDER)


# ---------------------------------------------------------------------------------------------
# shared world pieces (copied from film 1 so the look matches)
# ---------------------------------------------------------------------------------------------
def sea(x0, x1, y0, y1, n=14, seed=1):
    rng = random.Random(seed)
    rect = Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0, fill_color=SEA, fill_opacity=0.14).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    rip = VGroup()
    for _ in range(n):
        a = Arc(radius=0.2, start_angle=PI * 1.2, angle=PI * 0.6, stroke_color=RIP, stroke_width=3, stroke_opacity=0.55)
        a.move_to([rng.uniform(x0 + 0.3, x1 - 0.3), rng.uniform(y0 + 0.3, y1 - 0.3), 0])
        a.v = rng.uniform(0.15, 0.3)

        def u(m, dt, x0=x0, x1=x1):
            m.shift(RIGHT * m.v * dt)
            if m.get_x() > x1 - 0.15:
                m.shift(LEFT * (x1 - x0 - 0.3))
        a.add_updater(u)
        rip.add(a)
    g = VGroup(rect, rip)
    g.set_z_index(-5)
    return g


def tok(k, r, pos):
    return Circle(radius=r, stroke_color=PAL[(k // 10) % 10], stroke_width=2, fill_color=PAL[k % 10], fill_opacity=1).move_to(pos)


def sunflower(n, a, b, c):
    out = []
    for i in range(n):
        r = np.sqrt((i + 0.5) / n)
        th = i * 2.39996
        out.append(np.array([c[0] + a * r * np.cos(th), c[1] + b * r * np.sin(th), 0.0]))
    return out


class Isl(VGroup):
    def __init__(self, cx, cy, w, h, r, seed=3):
        super().__init__()
        self.body = Ellipse(width=w, height=h, stroke_color=LANDS, stroke_width=4, fill_color=LAND, fill_opacity=0.9).move_to([cx, cy, 0])
        pos = sunflower(100, w * 0.43, h * 0.43, [cx, cy])
        self.slots = VGroup(*[tok(k, r, pos[k]) for k in range(100)])
        self.slots.set_opacity(0)
        self.add(self.body, self.slots)
        self.present = set()
        self.alpha = [0.0] * 100
        self.lastop = [-1.0] * 100
        self.clock = 0.0
        self.blink_rate = 0.0
        self.blink_until = [0.0] * 100
        self.follow = None
        self.rng = random.Random(seed)
        self.add_updater(lambda m, dt: m._tick(dt))

    def _tick(self, dt):
        self.clock += dt
        if self.follow is not None:
            n = max(0, min(100, int(round(self.follow.get_value()))))
            self.present = set(ORDER[:n])
        for k in range(100):
            tgt = 1.0 if k in self.present else 0.0
            if self.blink_rate and tgt and self.rng.random() < self.blink_rate * dt:
                self.blink_until[k] = self.clock + 0.7
            if self.blink_until[k] > self.clock:
                tgt = 0.0
            a = self.alpha[k]
            a = min(tgt, a + 6 * dt) if tgt > a else max(tgt, a - 6 * dt)
            self.alpha[k] = a
            op = a * (0.88 + 0.12 * np.sin(self.clock * 2.2 + k * 0.9))
            if abs(op - self.lastop[k]) > 0.02:
                self.lastop[k] = op
                s = self.slots[k]
                s.set_fill(opacity=op)
                s.set_stroke(opacity=op)


def tide(sc):
    r = Rectangle(width=16, height=9, stroke_width=0, fill_color="#3A9AA8", fill_opacity=0.07).set_z_index(-20)
    r.t = 0.0

    def u(m, dt):
        m.t += dt
        m.set_fill(opacity=0.07 + 0.06 * np.sin(m.t * TAU / 3.0))
    r.add_updater(u)
    sc.add(r)


def bob(m, amp=0.06, sp=1.6, ph=0.0):
    m.bob_t = ph
    m.bob_off = np.zeros(3)

    def u(mm, dt):
        mm.bob_t += dt
        off = np.array([amp * 0.5 * np.cos(mm.bob_t * sp * 0.8 + ph), amp * np.sin(mm.bob_t * sp + ph), 0.0])
        mm.shift(off - mm.bob_off)
        mm.bob_off = off
    m.add_updater(u)
    return m


def ring_at(sc, pos, color=TEXT, r=0.1):
    ring = Circle(radius=r, stroke_color=color, stroke_width=3).move_to(pos)
    ring.age = 0.0

    def u(m, dt):
        m.age += dt
        m.scale(1 + 3.0 * dt)
        m.set_stroke(opacity=max(0.0, 1 - m.age / 0.5))
    ring.add_updater(u)
    sc.add(ring)


# ---------------------------------------------------------------------------------------------
# cartoon animals (schematic)
# ---------------------------------------------------------------------------------------------
def mite(color, s=1.0):
    body = Ellipse(width=0.62, height=0.5, stroke_color=TEXT, stroke_width=2, fill_color=color, fill_opacity=1)
    legs = VGroup()
    for i in (-1, 0, 1):
        legs.add(Line([-0.28, i * 0.14, 0], [-0.5, i * 0.24, 0]), Line([0.28, i * 0.14, 0], [0.5, i * 0.24, 0]))
    legs.set_stroke(color, 4)
    eyes = VGroup(Dot([-0.1, 0.08, 0], radius=0.04, color=BG), Dot([0.1, 0.08, 0], radius=0.04, color=BG))
    return VGroup(legs, body, eyes).scale(s)


def beetle(s=1.0):
    col = "#FF9F43"
    body = Ellipse(width=0.8, height=0.56, stroke_color=TEXT, stroke_width=2, fill_color=col, fill_opacity=1)
    mid = Line([0, 0.28, 0], [0, -0.28, 0]).set_stroke(TEXT, 2)
    head = Circle(radius=0.13, stroke_color=TEXT, stroke_width=2, fill_color=col, fill_opacity=1).move_to([0.5, 0, 0])
    legs = VGroup(*[Line([x, 0.2 * sg, 0], [x - 0.08, 0.42 * sg, 0]) for x in (-0.2, 0, 0.2) for sg in (1, -1)]).set_stroke(col, 4)
    return VGroup(legs, body, mid, head).scale(s)


def spider(s=1.0):
    col = "#E07BE0"
    legs = VGroup()
    for sg in (-1, 1):
        for y in (0.3, 0.1, -0.1, -0.3):
            legs.add(Line([0, 0, 0], [sg * 0.5, y * 1.4, 0]))
    legs.set_stroke(col, 3)
    body = Circle(radius=0.2, stroke_color=TEXT, stroke_width=2, fill_color=col, fill_opacity=1)
    head = Circle(radius=0.12, stroke_color=TEXT, stroke_width=2, fill_color=col, fill_opacity=1).move_to([0, 0.24, 0])
    return VGroup(legs, body, head).scale(s)


def moth(s=1.0):
    col = "#F78FB3"
    w1 = Polygon([0, 0, 0], [-0.5, 0.3, 0], [-0.4, -0.25, 0], stroke_color=TEXT, stroke_width=2, fill_color=col, fill_opacity=0.9)
    w2 = Polygon([0, 0, 0], [0.5, 0.3, 0], [0.4, -0.25, 0], stroke_color=TEXT, stroke_width=2, fill_color=col, fill_opacity=0.9)
    body = Line([0, 0.2, 0], [0, -0.25, 0]).set_stroke(TEXT, 5)
    return VGroup(w1, w2, body).scale(s)


def mangrove(cx, cy, w, h):
    """Film 1's island ellipse plus a canopy and prop roots (cartoon)."""
    land = Ellipse(width=w, height=h, stroke_color=LANDS, stroke_width=4, fill_color=LAND, fill_opacity=0.9).move_to([cx, cy, 0])
    roots = VGroup()
    for i in range(8):
        x0 = cx + (i - 3.5) * w * 0.11
        y0 = cy - h * 0.5 * np.sqrt(max(0.0, 1 - ((x0 - cx) / (w / 2)) ** 2)) + 0.05
        roots.add(ArcBetweenPoints([x0, y0, 0], [x0 + (i - 3.5) * 0.07, cy - h * 0.5 - 0.42, 0], angle=0.5 if i % 2 else -0.5))
    roots.set_stroke(BROWN, 5).set_z_index(-1)
    canopy = VGroup(*[Circle(radius=h * r, stroke_width=0, fill_color=LANDS, fill_opacity=0.28).move_to([cx + dx * w, cy + h * dy, 0])
                      for r, dx, dy in ((0.28, -0.22, 0.12), (0.32, 0.0, 0.2), (0.27, 0.22, 0.1))])
    g = VGroup(roots, land, canopy)
    g.land = land
    return g


# ---------------------------------------------------------------------------------------------
# recap graph of film 1 (computed from the two rate lines)
# ---------------------------------------------------------------------------------------------
def recap(center, xl, yl, w=7, small=False):
    ax = Axes(x_range=[0, 100, 50], y_range=[0, 11, 5], x_length=xl, y_length=yl, tips=False,
              axis_config={"color": TEXT, "stroke_width": 3 if not small else 2, "include_ticks": False}).move_to([center[0], center[1], 0])
    I = ax.plot(lambda s: 10 * (1 - s / 100.0), x_range=[0, 100, 2], color=BLUE, stroke_width=w, use_smoothing=False)
    E = ax.plot(lambda s: 0.1 * s, x_range=[0, 100, 2], color=RED, stroke_width=w, use_smoothing=False)
    dot = Dot(ax.c2p(50, 5), radius=0.17 if not small else 0.09, color=GOLD).set_z_index(5)
    g = VGroup(ax, I, E, dot)
    g.ax = ax
    return g


def osc_dots(sc, ax, amp=18.0, sp=2.4):
    clock = ValueTracker(0)
    clock.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(clock)
    S = lambda: 50 + amp * np.sin(clock.get_value() * sp)
    b = always_redraw(lambda: Dot(ax.c2p(S(), 10 * (1 - S() / 100.0)), radius=0.16, color=BLUE).set_z_index(6))
    r = always_redraw(lambda: Dot(ax.c2p(S(), 0.1 * S()), radius=0.16, color=RED).set_z_index(6))
    sc.add(b, r)
    return clock, b, r


# ---------------------------------------------------------------------------------------------
# notebooks (s06 - s09)
# ---------------------------------------------------------------------------------------------
NBX = 3.5


def notebook(cx, title, w=4.6, h=4.7, cy=-0.35, ty=2.55):
    body = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.06).move_to([cx, cy, 0])
    spine = Line([cx - w / 2 + 0.45, cy - h / 2 + 0.12, 0], [cx - w / 2 + 0.45, cy + h / 2 - 0.12, 0]).set_stroke(TEXT, 2, 0.35)
    ttl = T(title, 34).move_to([cx, ty, 0])
    return VGroup(body, spine, ttl)


def tok_slots(cx):
    return [[cx + dx, y, 0] for y in (1.3, 0.35, -0.6, -1.55) for dx in (-0.9, 0.9)]


class C2(SpokenScene):
    def setup(self):
        super().setup()
        tide(self)

    def span(self, phrase, lead=0.2, nth=0, minimum=0.1):
        return max(minimum, self.t_of(phrase, nth) - lead - self.elapsed())


def mites_in_notebooks(sc):
    """The three mites placed in the two notebooks, as at the end of s08 (names stay on screen)."""
    pass


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Island Biogeography"
    TITLE = "Emptying Islands"


# ---------------------------------------------------------------------------------------------
class S01Link(C2):
    def construct(self):
        self.add(sea(-6.8, 6.8, -3.8, 3.8, 16, 2))
        big = recap((-0.5, 0.2), 8.6, 5.0, 7)
        ax = big.ax
        lb = T("arrivals", 30, BLUE).move_to(ax.c2p(24, 10.0))
        lr = T("losses", 30, RED).move_to(ax.c2p(76, 9.9))
        self.play(Create(ax), run_time=0.7)
        self.play(Create(big[1]), Create(big[2]), FadeIn(lb), FadeIn(lr), run_time=1.6)
        self.at("steady count")
        gl = T("S*", 34, GOLD).next_to(ax.c2p(50, 5), UP, 0.3)
        self.play(GrowFromCenter(big[3]), FadeIn(gl), run_time=0.6)
        self.at("kept coming")
        clock, b, r = osc_dots(self, ax)
        self.wait(self.span("So empty", 1.2))
        self.remove(b, r, clock)
        small = big.copy().scale(0.42).move_to([-4.6, 2.2, 0])
        small[1].set_stroke(width=4)
        small[2].set_stroke(width=4)
        isl = Isl(2.2, -0.5, 6.6, 4.6, 0.13)
        n = ValueTracker(0)
        isl.follow = n
        isl.blink_rate = 0.4
        self.add(isl)
        self.play(Transform(big, small), FadeOut(lb), FadeOut(gl), FadeOut(lr), FadeIn(isl.body), run_time=1.0)
        self.at("So empty")
        self.play(n.animate.set_value(45), run_time=1.5, rate_func=linear)
        self.at("of every insect", lead=0.4)
        self.play(n.animate.set_value(0), run_time=self.span("spider.", 0.0, minimum=1.2) + 0.9, rate_func=linear)
        self.at("How many")
        q1 = T("how many?", 38, TEXT).move_to([-4.9, -0.2, 0])
        self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.7)
        bob(q1)
        self.at("are they the same")
        q2 = T("which ones?", 38, TEXT).move_to([-4.9, -1.3, 0])
        self.play(FadeIn(q2, shift=UP * 0.2), run_time=0.7)
        bob(q2, ph=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
KEY_PTS = [(3.4, 1.3), (4.6, 0.5), (5.5, -0.5), (5.5, -1.6), (4.6, -2.4), (3.5, -2.9)]


def keys_map():
    fl = RoundedRectangle(corner_radius=0.3, width=4.4, height=1.1, stroke_color=LANDS, stroke_width=4, fill_color=LAND, fill_opacity=0.9).move_to([2.2, 2.9, 0])
    fl_t = T("Florida", 28).move_to(fl)
    rng = random.Random(7)
    blobs = VGroup()
    for i in range(10):
        t = i / 9.0
        x = 2.9 + 3.2 * np.sin(t * 2.4)
        y = 2.0 - 4.9 * t
        blobs.add(Ellipse(width=0.4, height=0.18, stroke_width=0, fill_color=LAND, fill_opacity=0.7).move_to([x + rng.uniform(-0.2, 0.2), y, 0]))
    dots = VGroup(*[Dot([x, y, 0], radius=0.2, color=LANDS) for x, y in KEY_PTS]).set_opacity(0.3)
    lab = T("Florida Keys", 30).move_to([1.9, -0.8, 0])
    sch = T("schematic", 24).move_to([5.7, -3.5, 0])
    return VGroup(fl, fl_t, blobs, lab, sch), dots


class S02Why(C2):
    def construct(self):
        self.add(sea(-6.8, 6.8, -3.8, 3.8, 16, 4))
        old = Isl(-3.5, 0.3, 5.4, 3.8, 0.12)
        n = ValueTracker(60)
        old.follow = n
        old.blink_rate = 0.25
        self.play(FadeIn(old.body), run_time=1.0)
        self.add(old)
        self.at("long ago")
        l1 = T("colonised long ago:", 32).move_to([-3.5, -2.4, 0])
        self.play(FadeIn(l1), run_time=0.6)
        self.at("rates")
        l2 = T("rates unseen", 32, GREY).move_to([-3.5, -3.0, 0])
        self.play(FadeIn(l2), run_time=0.6)
        self.wait(self.span("Daniel", 1.0))
        mp, dots = keys_map()
        self.at("Daniel", lead=0.3)
        self.play(FadeOut(old), FadeOut(l1), FadeOut(l2), FadeIn(mp), FadeIn(dots), run_time=0.9)
        c1 = chip("Daniel Simberloff", TEXT, 32)
        c2 = chip("Edward O. Wilson", TEXT, 32)
        c1.move_to([-3.6, 0.9, 0])
        c2.move_to([-3.6, -0.5, 0])
        self.play(FadeIn(c1, shift=RIGHT * 1.5), run_time=0.8)
        self.at("Edward")
        self.play(FadeIn(c2, shift=RIGHT * 1.5), run_time=0.8)
        self.at("chose islands")
        self.play(LaggedStart(*[d.animate.set_opacity(1) for d in dots], lag_ratio=0.3), run_time=self.span("small enough", 0.0, minimum=1.2) + 0.8)
        for d in dots:
            ring_at(self, d.get_center(), TEXT, 0.2)
        self.at("then watched")
        for i, d in enumerate(dots):
            bob(d, 0.08, 2.0, i)
        self.play(Indicate(dots, color=TEXT, scale_factor=1.4), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def critters_on(cx_off=0.0):
    b = beetle(1.2).move_to([-2.3 + cx_off, 0.5, 0])
    m = moth(1.2).move_to([2.3 + cx_off, 1.0, 0])
    s = spider(1.2).move_to([-0.3 + cx_off, -0.8, 0])
    t = mite(PAL[6], 1.2).move_to([2.4 + cx_off, -0.6, 0])
    return b, m, s, t


class S03Islands(C2):
    def construct(self):
        self.add(sea(-6.8, 6.8, -3.8, 3.8, 16, 4))
        mp, dots = keys_map()
        for d in dots:
            d.set_opacity(0.6)
        lab6 = T("six small islands", 34).move_to([-3.0, 0.3, 0])
        self.add(mp, dots)
        self.at("six small", lead=0.4)
        self.play(FadeIn(lab6), Indicate(dots, color=TEXT, scale_factor=1.4), run_time=1.2)
        self.wait(self.span("red mangrove", 0.5))
        isl = mangrove(0.2, -0.1, 7.2, 4.6)
        self.at("red mangrove", lead=0.4)
        others = VGroup(mp, *[d for i, d in enumerate(dots) if i != 3])
        self.play(FadeOut(others), FadeOut(lab6), ReplacementTransform(dots[3], isl.land), run_time=1.2)
        self.play(FadeIn(isl[0]), FadeIn(isl[2]), run_time=0.6)
        nm = VGroup(T("red mangrove, ", 32), T("Rhizophora mangle", 32, slant=ITALIC)).arrange(RIGHT, buff=0.18).move_to([0, 3.3, 0])
        self.play(FadeIn(nm), run_time=0.6)
        self.at("Each carried")
        b, m, s, t = critters_on()
        for i, c in enumerate((b, m, s, t)):
            bob(c, 0.07, 1.8, i)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in (b, m, s, t)], lag_ratio=0.25), run_time=1.4)
        self.at("terrestrial")
        ta = T("terrestrial arthropods", 34).move_to([0, -3.4, 0])
        self.play(FadeIn(ta), run_time=0.8)
        self.at("insects,")
        la = T("insects", 28, TEXT).next_to(b, DOWN, 0.15)
        lb = T("insects", 28, TEXT).next_to(m, DOWN, 0.15)
        self.play(FadeIn(la), FadeIn(lb), Indicate(b), Indicate(m), run_time=0.9)
        self.at("spiders,")
        ls = T("spiders", 28, TEXT).next_to(s, DOWN, 0.15)
        self.play(FadeIn(ls), Indicate(s), run_time=0.9)
        self.at("mites,")
        lm = T("mites", 28, TEXT).next_to(t, DOWN, 0.15)
        self.play(FadeIn(lm), Indicate(t), run_time=0.9)
        self.at("their relatives")
        self.play(Indicate(VGroup(b, m, s, t), color=TEXT, scale_factor=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tent_shape(cx, cy):
    t = Polygon([cx - 3.4, cy - 1.7, 0], [cx - 2.9, cy + 0.6, 0], [cx, cy + 2.2, 0], [cx + 2.9, cy + 0.6, 0], [cx + 3.4, cy - 1.7, 0],
                stroke_color=TEXT, stroke_width=5, fill_color="#DDE6F0", fill_opacity=0.18)
    t.add(Line([cx, cy + 2.2, 0], [cx, cy - 1.7, 0]).set_stroke(TEXT, 3, 0.5))
    return t


def tag(n, text, color=TEXT):
    c = VGroup(Circle(radius=0.32, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.2), M(str(n), 32, GOLD))
    c[1].move_to(c[0])
    lab = T(text, 34, color)
    return VGroup(c, lab).arrange(RIGHT, buff=0.3)


class S04Method(C2):
    def construct(self):
        self.add(sea(-6.8, 6.8, -3.8, 3.8, 16, 5))
        isl = Isl(2.0, 0.3, 5.6, 3.6, 0.12)
        n = ValueTracker(0)
        isl.follow = n
        isl.blink_rate = 0.15
        nb = notebook(-4.6, "", 3.0, 3.8, 0.3, 2.0)
        t1 = tag(1, "census before").move_to([0, 3.3, 0])
        self.play(FadeIn(isl.body), FadeIn(nb), FadeIn(t1), run_time=0.8)
        self.add(isl)
        self.at("recorded every")
        self.play(n.animate.set_value(45), run_time=1.6, rate_func=linear)
        sw = VGroup(*[Circle(radius=0.14, stroke_width=0, fill_color=PAL[ORDER[k] % 10], fill_opacity=1).move_to([-5.4 + (k % 5) * 0.45 + 0.3, 1.7 - (k // 5) * 0.42, 0]) for k in range(30)])
        self.play(LaggedStart(*[FadeIn(s, scale=2) for s in sw], lag_ratio=0.05), run_time=self.span("Then they covered", 0.3, minimum=1.0))
        self.at("Then they covered")
        t2 = tag(2, "tent and fumigation").move_to([0, 3.3, 0])
        tent = tent_shape(2.0, 0.5).shift(UP * 4)
        self.play(ReplacementTransform(t1, t2), tent.animate.shift(DOWN * 4), run_time=1.0)
        self.at("fumigated")
        rng = random.Random(3)
        cloud = VGroup(*[Circle(radius=rng.uniform(0.35, 0.7), stroke_width=0, fill_color="#DDE6F0", fill_opacity=0.3).move_to([2.0 + rng.uniform(-2.3, 2.3), 0.3 + rng.uniform(-1.3, 1.3), 0]) for _ in range(9)])
        for c in cloud:
            c.v = np.array([rng.uniform(-0.2, 0.2), rng.uniform(-0.1, 0.1), 0])
            c.add_updater(lambda m, dt: m.shift(m.v * dt))
        self.play(FadeIn(cloud), n.animate.set_value(0), run_time=1.6, rate_func=linear)
        self.wait(self.span("Afterwards", 0.3, minimum=0.1))
        self.at("Afterwards")
        t3 = tag(3, "census again, for a year").move_to([0, 3.3, 0])
        self.play(ReplacementTransform(t2, t3), FadeOut(cloud), tent.animate.shift(UP * 4).set_opacity(0), run_time=1.2)
        self.remove(tent)
        strip = Line([-5.8, -2.9, 0], [5.8, -2.9, 0]).set_stroke(TEXT, 4)
        d0 = T("day 0", 28).move_to([-5.2, -3.45, 0])
        d1 = T("day 365", 28).move_to([5.0, -3.45, 0])
        self.play(Create(strip), FadeIn(d0), FadeIn(d1), run_time=self.span("again and again", 0.3, minimum=0.6))
        self.at("again and again")
        ticks = VGroup(*[Line([x, -2.65, 0], [x, -3.15, 0]).set_stroke(GOLD, 5) for x in np.linspace(-4.6, 5.0, 9)])
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2), run_time=1.8)
        n.set_value(0)
        self.play(n.animate.set_value(18), run_time=1.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Return(C2):
    def construct(self):
        ax = Axes(x_range=[0, 365, 365], y_range=[0, 1.1, 1], x_length=10.8, y_length=5.2, tips=False,
                  axis_config={"color": TEXT, "stroke_width": 3, "include_ticks": False}).move_to([-0.4, -0.2, 0])
        self.add(ax)
        ytxt = T("species number", 30).move_to([-4.2, 3.0, 0])
        xtxt = T("days since fumigation", 28).move_to([-3.2, -3.55, 0])
        sch = T("schematic, shape only", 24, GREY).move_to([3.8, -2.2, 0])
        z = T("0", 26).next_to(ax.c2p(0, 0), DOWN, 0.2)
        self.play(FadeIn(ytxt), FadeIn(xtxt), FadeIn(z), FadeIn(sch), run_time=0.8)
        T_ = ValueTracker(0.01)
        A = [0.95, 0.9, 1.0, 0.88, 0.93]
        TAU = [55, 70, 85, 95, 62]
        curves = []
        for a, tau in zip(A, TAU):
            curves.append(always_redraw(lambda a=a, tau=tau: ax.plot(lambda t: a * (1 - np.exp(-t / tau)), x_range=[0, max(1.0, T_.get_value()), 5],
                                                                       color=TEXT, stroke_width=5, use_smoothing=False)))
        e1 = always_redraw(lambda: ax.plot(lambda t: 0.62 * (1 - np.exp(-t / 140.0)), x_range=[0, max(1.0, T_.get_value()), 5],
                                           color=PAL[3], stroke_width=5, use_smoothing=False))
        for c in curves:
            self.add(c)
        self.add(e1)
        self.play(T_.animate.set_value(250), run_time=self.span("day 250", 0.0, minimum=1.0), rate_func=linear)
        self.at("day 250", lead=0.2)
        mark = DashedLine(ax.c2p(250, 0), ax.c2p(250, 1.1), color=TEXT, stroke_width=3)
        ml = T("day 250", 30).next_to(ax.c2p(250, 0), DOWN, 0.2)
        self.play(Create(mark), FadeIn(ml), run_time=0.6)
        self.play(T_.animate.set_value(365), run_time=self.span("most islands", 0.3, minimum=0.8), rate_func=linear)
        self.at("most islands")
        band = Rectangle(width=ax.c2p(365, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 1.0)[1] - ax.c2p(0, 0.8)[1], stroke_width=0, fill_color=GOLD, fill_opacity=0.0).move_to(
            [(ax.c2p(365, 0)[0] + ax.c2p(0, 0)[0]) / 2, (ax.c2p(0, 1.0)[1] + ax.c2p(0, 0.8)[1]) / 2, 0]).set_z_index(-1)
        band.set_fill(TEXT, 0.16)
        self.play(FadeIn(band), run_time=1.0)
        self.at("untreated")
        bl = T("untreated islands", 32).move_to([3.0, 2.95, 0])
        self.play(FadeIn(bl), run_time=0.6)
        self.at("exception")
        self.play(Indicate(e1, color=PAL[3], scale_factor=1.0), run_time=1.0)
        self.at("most distant", lead=0.3)
        el = T("E1, most distant", 32, PAL[3]).move_to(ax.c2p(335, 0.36))
        self.play(FadeIn(el), run_time=0.7)
        self.wait(self.span("Population", 0.7))
        isl = mangrove(0.2, -0.1, 7.2, 4.6)
        cr = critters_on()
        ghosts = VGroup(*[Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.45).move_to(p) for p in
                          [(-1.2, 1.2, 0), (0.6, 0.6, 0), (-2.8, -0.5, 0), (-1.6, -1.4, 0), (1.0, -1.3, 0), (3.4, 0.2, 0), (0.4, 1.5, 0), (3.0, -1.3, 0)]])
        ghosts = DashedVMobject(ghosts, num_dashes=8) if False else ghosts
        plot = VGroup(ax, ytxt, xtxt, z, sch, mark, ml, band, bl, el)
        for c in curves:
            self.remove(c)
        self.remove(e1)
        self.play(FadeOut(plot), FadeIn(isl), run_time=0.9)
        for i, c in enumerate(cr):
            bob(c, 0.07, 1.8, i)
        self.at("Population", lead=0.3)
        self.play(FadeIn(ghosts), LaggedStart(*[GrowFromCenter(c) for c in cr], lag_ratio=0.2), run_time=1.2)
        self.at("abnormally", lead=0.3)
        lab = T("densities still low", 38).move_to([0, -3.4, 0])
        self.play(FadeIn(lab), run_time=0.7)
        self.play(Indicate(ghosts, color=TEXT, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def covers_for(cx, color=GREY):
    return VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.8, height=0.8, stroke_width=2, stroke_color=TEXT, fill_color=color, fill_opacity=0.95).move_to(p) for p in tok_slots(cx)])


def hidden_tokens(cx, shift):
    return VGroup(*[tok((i + shift) % 10, 0.3, p) for i, p in enumerate(tok_slots(cx))])


class S06Predict(C2):
    def construct(self):
        nl, nr = notebook(-NBX, "before"), notebook(NBX, "day 364")
        self.play(FadeIn(nl), FadeIn(nr), run_time=1.2)
        self.at("the count", lead=0.5)
        tl = hidden_tokens(-NBX, 0)
        self.play(LaggedStart(*[GrowFromCenter(t) for t in tl], lag_ratio=0.12), run_time=self.span("came back", 0.2, minimum=1.0))
        self.at("came back")
        tr = hidden_tokens(NBX, 3)
        self.play(LaggedStart(*[GrowFromCenter(t) for t in tr], lag_ratio=0.1), run_time=self.span("how much", 0.5, minimum=0.8))
        self.at("how much", lead=0.6)
        cl, cr = covers_for(-NBX), covers_for(NBX)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in list(cl) + list(cr)], lag_ratio=0.04), run_time=1.2)
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, -0.35, 0])
        self.add(q)
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        q.add_updater(lambda m, dt: m.set_opacity(0.8 + 0.2 * np.sin(self.renderer.time * 5)))
        self.at("old species")
        self.play(Indicate(nl[0], color=TEXT, scale_factor=1.04), run_time=1.0)
        self.at("new list")
        self.play(Indicate(nr[0], color=TEXT, scale_factor=1.04), run_time=1.0)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        tide(self)
        nl, nr = notebook(-NBX, "before"), notebook(NBX, "day 364")
        cl, cr = covers_for(-NBX), covers_for(NBX)
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, -0.35, 0])
        self.add(nl, nr, cl, cr, q)
        q.add_updater(lambda m, dt: m.set_opacity(0.8 + 0.2 * np.sin(self.renderer.time * 5)))
        T_ = ValueTracker(0)
        r0 = Circle(radius=0.95, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.4).move_to([0, -0.35, 0])
        ring = always_redraw(lambda: Arc(radius=0.95, start_angle=PI / 2, angle=-TAU * max(0.001, T_.get_value()), stroke_color=GOLD, stroke_width=8).move_to([0, -0.35, 0]))
        self.add(r0, ring)
        self.play(T_.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
SLOT_A, SLOT_B = 0.85, -0.95   # y of the two mite slots in a notebook


def slot_pos(cx, row):
    return [cx, SLOT_A if row == 0 else SLOT_B, 0]


class S08Mites(C2):
    def construct(self):
        nl, nr = notebook(-NBX, "before"), notebook(NBX, "day 364")
        tl, tr = hidden_tokens(-NBX, 0), hidden_tokens(NBX, 3)
        cl, cr = covers_for(-NBX), covers_for(NBX)
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, -0.35, 0])
        self.add(nl, nr, tl, tr, cl, cr, q)
        self.play(FadeOut(q), FadeOut(cl), FadeOut(cr), FadeOut(tl), FadeOut(tr), run_time=1.2)
        self.at("three mite", lead=0.3)
        centre = [mite(TEXT, 1.0).move_to([0, y, 0]) for y in (1.3, 0.0, -1.3)]
        for i, c in enumerate(centre):
            bob(c, 0.05, 1.7, i)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in centre], lag_ratio=0.25), run_time=1.5)
        self.at("chosen because")
        ll = T("island E9, three chosen mite taxa", 30).move_to([0, -3.35, 0])
        self.play(FadeIn(ll), run_time=0.8)
        self.at("One was there before and after")
        names = {}

        def place(row, side, color, name, src):
            cx = -NBX if side < 0 else NBX
            pos = slot_pos(cx, row)
            m = mite(color, 1.2).move_to(src.get_center())
            lab = T(name, 28, color)
            lab.move_to([cx, pos[1] - 0.6, 0])
            return m, pos, lab

        # green, both notebooks
        self.play(centre[0].animate.set_color(GREEN), run_time=0.6)
        centre[0].become(mite(GREEN, 1.0).move_to(centre[0].get_center()))
        m1, p1, l1 = place(0, -1, GREEN, "Bdella", centre[0])
        m2, p2, l2 = place(0, 1, GREEN, "Bdella", centre[0])
        self.add(m1, m2)
        self.play(m1.animate.move_to(p1), m2.animate.move_to(p2), run_time=1.2)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        bob(m1, 0.05, 1.7, 0.3)
        bob(m2, 0.05, 1.7, 1.1)
        self.at("One was there only before")
        centre[1].become(mite(GREY, 1.0).move_to(centre[1].get_center()))
        m3, p3, l3 = place(1, -1, GREY, "Amblyseius", centre[1])
        self.add(m3)
        self.play(m3.animate.move_to(p3), run_time=1.2)
        self.play(FadeIn(l3), run_time=0.6)
        bob(m3, 0.05, 1.7, 2.1)
        self.at("One was there only after")
        centre[2].become(mite(PURPLE, 1.0).move_to(centre[2].get_center()))
        m4, p4, l4 = place(1, 1, PURPLE, "Carpoglyphus lactis", centre[2])
        self.add(m4)
        self.play(m4.animate.move_to(p4), run_time=1.2)
        self.play(FadeIn(l4), run_time=0.6)
        bob(m4, 0.05, 1.7, 3.1)
        self.play(FadeOut(VGroup(*centre)), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
V1, V2, VY, VR = (-1.35, 0.55, 0.0), (1.35, 0.55, 0.0), 0.55, 2.0


class S09Jaccard(C2):
    def construct(self):
        nl, nr = notebook(-NBX, "before"), notebook(NBX, "day 364")
        a_l = mite(GREEN, 1.2).move_to(slot_pos(-NBX, 0))
        b_l = mite(GREY, 1.2).move_to(slot_pos(-NBX, 1))
        a_r = mite(GREEN, 1.2).move_to(slot_pos(NBX, 0))
        b_r = mite(PURPLE, 1.2).move_to(slot_pos(NBX, 1))
        mites = [a_l, b_l, a_r, b_r]
        self.add(nl, nr, *mites)
        for i, m in enumerate(mites):
            bob(m, 0.05, 1.7, i)
        n1 = M("2", 60).move_to([-0.6, -0.35, 0])
        n2 = M("2", 60).move_to([0.6, -0.35, 0])
        eq = M("=", 60).move_to([0, -0.35, 0])
        self.play(FadeIn(n1, scale=0.5), Indicate(a_l), Indicate(b_l), run_time=1.0)
        self.at("and two kinds after", lead=0.1)
        self.play(FadeIn(n2, scale=0.5), Indicate(a_r), Indicate(b_r), run_time=1.0)
        self.at("unchanged", lead=0.4)
        self.play(FadeIn(eq, scale=0.5), run_time=0.6)
        self.wait(self.span("But only", 0.2))
        self.at("But only", lead=0.3)
        # Venn
        c1 = Circle(radius=VR, stroke_color=TEXT, stroke_width=4).move_to(V1)
        c2 = Circle(radius=VR, stroke_color=TEXT, stroke_width=4).move_to(V2)
        lb = T("before", 32).move_to([V1[0] - 0.3, 3.1, 0])
        la = T("day 364", 32).move_to([V2[0] + 0.3, 3.1, 0])
        self.remove(a_l, a_r, b_l, b_r)
        gm1 = mite(GREEN, 1.0).move_to(a_l.get_center())
        gm2 = mite(GREEN, 1.0).move_to(a_r.get_center())
        grey = mite(GREY, 1.0).move_to(b_l.get_center())
        pur = mite(PURPLE, 1.0).move_to(b_r.get_center())
        self.add(gm1, gm2, grey, pur)
        self.play(FadeOut(nl), FadeOut(nr), FadeOut(n1), FadeOut(n2), FadeOut(eq), Create(c1), Create(c2), FadeIn(lb), FadeIn(la),
                  grey.animate.move_to([-2.4, VY, 0]), pur.animate.move_to([2.4, VY, 0]),
                  gm1.animate.move_to([0, VY, 0]), gm2.animate.move_to([0, VY, 0]), run_time=1.5)
        self.remove(gm2)
        for i, m in enumerate((grey, gm1, pur)):
            bob(m, 0.05, 1.7, i)
        self.at("is shared")
        try:
            lens = Intersection(c1, c2, stroke_width=0, fill_color=GREEN, fill_opacity=0.35)
        except Exception:
            lens = Circle(radius=0.1, stroke_width=0)
        self.play(FadeIn(lens), run_time=0.8)
        self.at("divided", lead=0.7)
        f1 = T("Jaccard = shared / in either list", 32).move_to([0, -2.5, 0])
        self.play(FadeIn(f1), run_time=1.0)
        self.at("shared species", lead=0.2)
        self.play(Indicate(lens, color=GREEN, scale_factor=1.1), run_time=1.2)
        self.at("in either list", lead=0.3)
        union = VGroup(c1.copy().set_stroke(width=0).set_fill(TEXT, 0.18), c2.copy().set_stroke(width=0).set_fill(TEXT, 0.18))
        self.play(FadeIn(union), run_time=0.8)
        self.play(FadeOut(union), run_time=0.8)
        self.at("Here it is")
        f2 = M("= 1 / 3", 52, TEXT, weight=BOLD).move_to([0, -3.3, 0])
        self.play(FadeIn(f2, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(lens, color=GREEN, scale_factor=1.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10Caution(C2):
    def construct(self):
        c1 = Circle(radius=VR, stroke_color=TEXT, stroke_width=4).move_to(V1)
        c2 = Circle(radius=VR, stroke_color=TEXT, stroke_width=4).move_to(V2)
        lb = T("before", 32).move_to([V1[0] - 0.3, 3.1, 0])
        la = T("day 364", 32).move_to([V2[0] + 0.3, 3.1, 0])
        try:
            lens = Intersection(c1, c2, stroke_width=0, fill_color=GREEN, fill_opacity=0.35)
        except Exception:
            lens = Circle(radius=0.1, stroke_width=0)
        grey, gm, pur = mite(GREY, 1.0).move_to([-2.4, VY, 0]), mite(GREEN, 1.0).move_to([0, VY, 0]), mite(PURPLE, 1.0).move_to([2.4, VY, 0])
        f1 = T("Jaccard = shared / in either list", 32).move_to([0, -2.5, 0])
        f2 = M("= 1 / 3", 52, TEXT, weight=BOLD).move_to([0, -3.3, 0])
        self.add(c1, c2, lb, la, lens, grey, gm, pur, f1, f2)
        for i, m in enumerate((grey, gm, pur)):
            bob(m, 0.05, 1.7, i)
        # big notebook page, a corner kept clear for the three mites
        page = RoundedRectangle(corner_radius=0.25, width=9.4, height=5.0, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.06).move_to([0.5, 0.35, 0])
        rng = random.Random(5)
        toks = VGroup()
        for r in range(5):
            for c in range(10):
                x, y = -3.7 + c * 0.9 + 0.5, 2.4 - r * 0.9
                if r == 0 and c < 3:
                    continue
                toks.add(tok(rng.randrange(100), 0.17, [x, y, 0]))
        corner_c = np.array([-2.55, 2.4, 0.0])
        box = RoundedRectangle(corner_radius=0.12, width=3.0, height=1.05, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.08).move_to(corner_c)
        self.play(FadeOut(VGroup(c1, c2, lb, la, lens, f1, f2)), FadeIn(page), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in toks], lag_ratio=0.02), FadeIn(box),
                  grey.animate.scale(0.75).move_to(corner_c + LEFT * 0.95), gm.animate.scale(0.75).move_to(corner_c),
                  pur.animate.scale(0.75).move_to(corner_c + RIGHT * 0.95), run_time=1.8)
        for t in toks:
            t.ph = rng.uniform(0, 6)
            t.t0 = 0.0
            t.add_updater(lambda m, dt: (setattr(m, "t0", m.t0 + dt), m.set_opacity(0.75 + 0.25 * np.sin(m.t0 * 2 + m.ph))))
        self.at("chosen subset", lead=0.3)
        self.play(Indicate(box, color=TEXT, scale_factor=1.1), run_time=1.0)
        self.at("not the whole")
        sel = T("a selection, not the whole community", 32).move_to([0.5, -3.3, 0])
        self.play(FadeIn(sel), run_time=0.8)
        self.wait(self.span("And finding", 0.4))
        # second half: the shared mite across the tent
        self.at("And finding", lead=0.4)
        self.remove(toks)
        strip = Line([-5.8, -1.2, 0], [5.8, -1.2, 0]).set_stroke(TEXT, 4)
        tx = [-4.6, -1.6, 1.8, 3.0, 4.2]
        ticks = VGroup(*[Line([x, -0.95, 0], [x, -1.45, 0]).set_stroke(GOLD, 5) for x in tx])
        lcb = T("census before", 28).move_to([-4.6, -2.0, 0])
        ltent = T("tent", 28).move_to([-1.6, -2.0, 0])
        lc2 = T("census, day 364", 28).move_to([4.2, -2.0, 0])
        tent = tent_shape(-1.6, 0.1).scale(0.35).move_to([-1.6, -0.2, 0])
        self.play(FadeOut(VGroup(page, toks, box, grey, pur, sel)), Create(strip), Create(ticks), FadeIn(lcb), FadeIn(ltent), FadeIn(lc2), FadeIn(tent),
                  gm.animate.scale(1.5).move_to([-4.6, 0.7, 0]), run_time=1.2)
        self.at("does not")
        self.play(gm.animate.move_to([-1.6, 0.7, 0]).set_opacity(0), run_time=1.6)
        self.at("It was recorded", lead=0.3)
        gm.move_to([4.2, 0.7, 0])
        self.play(gm.animate.set_opacity(1), run_time=1.0)
        rl = T("recorded again, not necessarily survived", 32).move_to([0, 2.8, 0])
        self.play(FadeIn(rl), run_time=0.8)
        self.at("after recolonization", lead=0.1)
        self.play(Indicate(gm, color=GREEN), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11Year2(C2):
    def construct(self):
        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=6.9, y_length=3.0, tips=False,
                  axis_config={"color": TEXT, "stroke_width": 3, "include_ticks": False}).move_to([-2.3, -1.55, 0])
        yt = T("species", 28).next_to(ax.c2p(0, 1), UP, 0.1).shift(RIGHT * 0.5)
        self.play(Create(ax), FadeIn(yt), run_time=0.8)
        cols = [PAL[0], PAL[3], PAL[4], PAL[5]]
        y1 = [0.82, 0.64, 0.46, 0.28]
        y2 = [0.80, 0.66, 0.43, 0.31]
        xs = [0.3, 0.75]
        isl = VGroup(*[Ellipse(width=1.9, height=1.1, stroke_color=c, stroke_width=5, fill_color=LAND, fill_opacity=0.9).move_to([x, 2.3, 0])
                       for c, x in zip(cols, (-4.65, -1.55, 1.55, 4.65))])
        self.at("followed four")
        self.play(FadeIn(isl), run_time=0.8)
        p1 = VGroup(*[Dot(ax.c2p(xs[0], y), radius=0.14, color=c) for c, y in zip(cols, y1)])
        l1 = T("year 1", 28).next_to(ax.c2p(xs[0], 0), DOWN, 0.2)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in p1], lag_ratio=0.2), FadeIn(l1), run_time=1.4)
        self.at("second year", lead=0.3)
        p2 = VGroup(*[Dot(ax.c2p(xs[1], y), radius=0.14, color=c) for c, y in zip(cols, y2)])
        l2 = T("year 2", 28).next_to(ax.c2p(xs[1], 0), DOWN, 0.2)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in p2], lag_ratio=0.2), FadeIn(l2), run_time=1.4)
        self.at("changed little", lead=0.3)
        lines = VGroup(*[DashedLine(ax.c2p(xs[0], a), ax.c2p(xs[1], b), color=c, stroke_width=4) for c, a, b in zip(cols, y1, y2)])
        self.play(Create(lines), run_time=1.2)
        lab = VGroup(T("little net change", 28), T("between annual censuses;", 28), T("path between them unknown", 28)).arrange(DOWN, buff=0.12).move_to([4.0, -1.5, 0])
        self.play(FadeIn(lab), run_time=0.8)
        self.at("immigrations")
        lb = T("immigrations and extinctions continued at high rates", 28).move_to([0, 0.85, 0])
        self.play(FadeIn(lb), run_time=0.8)
        # arrows firing at irregular intervals
        rng = random.Random(9)
        arrows = VGroup()
        for x in (-4.65, -1.55, 1.55, 4.65):
            ai = Arrow([x - 1.0, 3.55, 0], [x - 0.4, 2.7, 0], color=BLUE, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.35)
            ao = Arrow([x + 0.4, 2.7, 0], [x + 1.0, 3.55, 0], color=RED, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.35)
            for a in (ai, ao):
                a.t0 = rng.uniform(0, 3)
                a.per = rng.uniform(1.0, 2.0)
                a.add_updater(lambda m, dt: (setattr(m, "t0", m.t0 + dt), m.set_opacity(max(0.0, np.sin((m.t0 % m.per) / m.per * PI)) ** 2)))
                arrows.add(a)
        self.add(arrows)
        self.wait(self.span("rates.", 0.0, minimum=0.5))
        self.play(Indicate(lb, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Dynamic(C2):
    def construct(self):
        self.add(sea(-6.8, 6.8, -3.8, 3.8, 14, 6))
        big = recap((-2.4, 0.2), 7.4, 4.6, 7)
        small = big.copy().scale(0.42).move_to([-4.6, 2.2, 0])
        small[1].set_stroke(width=4)
        small[2].set_stroke(width=4)
        sm = small.copy()
        self.add(sm)
        self.wait(0.8)
        self.play(Transform(sm, big), run_time=1.5)
        ax = big.ax
        gl = T("S*", 34, GOLD).next_to(ax.c2p(50, 5), UP, 0.3)
        self.play(FadeIn(gl), run_time=0.5)
        clock, b, r = osc_dots(self, ax)
        sm.add_updater(lambda m, dt: m[3].set_width(0.34 * (1 + 0.15 * np.sin(clock.get_value() * 4))))
        self.at("dynamic")
        dl = VGroup(T("dynamic", 40), T("equilibrium", 40)).arrange(DOWN, buff=0.1).move_to([4.3, 1.4, 0])
        self.play(FadeIn(dl, shift=LEFT * 0.3), run_time=0.8)
        self.at("fits the model")
        st1 = T("fits the model,", 36, GOLD)
        st2 = T("does not prove it", 36, GOLD)
        stamp = VGroup(st1, st2).arrange(DOWN, buff=0.12)
        box = RoundedRectangle(corner_radius=0.15, width=stamp.width + 0.5, height=stamp.height + 0.4, stroke_color=GOLD, stroke_width=4).move_to(stamp)
        sg = VGroup(box, stamp).move_to([3.7, -1.4, 0]).rotate(0.06)
        self.play(FadeIn(sg, scale=1.4), run_time=0.8)
        self.wait(self.span("mechanism", 0.0, minimum=0.5))
        self.play(Indicate(sg, color=GOLD, scale_factor=1.06), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def leaf(cx, cy):
    lf = Ellipse(width=1.3, height=0.7, stroke_color=LANDS, stroke_width=3, fill_color=LAND, fill_opacity=1).move_to([cx, cy, 0]).rotate(0.3)
    rib = Line([cx - 0.55, cy - 0.15, 0], [cx + 0.55, cy + 0.15, 0]).set_stroke(LANDS, 3)
    return VGroup(lf, rib)


class S13Rough(C2):
    def construct(self):
        self.add(sea(-6.8, 6.8, -3.8, 3.8, 14, 8))
        isl = Isl(0.0, 1.0, 9.0, 2.2, 0.1)
        nn = ValueTracker(35)
        isl.follow = nn
        isl.blink_rate = 0.3
        self.add(isl)
        self.play(FadeIn(isl.body), run_time=0.8)
        SY = -1.2
        TX = [-5.2, -2.6, 0.0, 2.6, 5.2]
        strip = Line([-6.2, SY, 0], [6.2, SY, 0]).set_stroke(TEXT, 4)
        ticks = VGroup(*[Line([x, SY + 0.3, 0], [x, SY - 0.3, 0]).set_stroke(GOLD, 6) for x in TX])
        self.play(Create(strip), run_time=1.0)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.3), run_time=1.5)
        self.at("Censuses came")
        cl = T("census", 30, GOLD).move_to([TX[0], SY - 0.75, 0])
        self.play(FadeIn(cl), run_time=0.6)
        self.at("intervals")
        self.play(LaggedStart(*[Indicate(t, color=GOLD, scale_factor=1.4) for t in ticks], lag_ratio=0.25), run_time=1.6)
        self.at("some arrivals", lead=0.3)
        pm = mite(PURPLE, 1.1).move_to([-4.0, 1.2, 0])
        ai = Arrow([-4.6, 3.4, 0], [-4.1, 1.9, 0], color=BLUE, buff=0, stroke_width=8)
        self.play(FadeIn(ai), FadeIn(pm, scale=0.5), run_time=0.8)
        bob(pm, 0.08, 2.0)
        self.at("losses")
        ao = Arrow([-3.5, 1.9, 0], [-3.0, 3.4, 0], color=RED, buff=0, stroke_width=8)
        self.play(FadeIn(ao), run_time=0.6)
        self.at("between visits")
        self.play(pm.animate.set_opacity(0.35), run_time=0.8)
        ghost = DashedVMobject(Circle(radius=0.5, stroke_color=PURPLE, stroke_width=3).move_to(pm.get_center()), num_dashes=16)
        self.add(ghost)
        self.at("never seen", lead=0.1)
        ml = T("missed between visits", 30).move_to([-3.9, -0.5, 0])
        self.play(FadeIn(ml), run_time=0.7)
        self.wait(self.span("And a resident", 0.3))
        self.at("And a resident", lead=0.2)
        gm = mite(GREEN, 1.3).move_to([TX[2] - 1.0, 1.2, 0])
        bob(gm, 0.06, 2.0)
        rec = VGroup(*[Circle(radius=0.18, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.5).move_to([x, -2.4, 0]) for x in TX[2:]])
        rl = T("what each census sees", 28, TEXT).move_to([-3.0, -2.4, 0])
        self.play(FadeOut(VGroup(ai, ao, pm, ghost, ml, cl)), FadeIn(gm), FadeIn(rec), FadeIn(rl), gm.animate.move_to([TX[2], 1.2, 0]), run_time=0.7)
        d3 = Dot([TX[2], -2.4, 0], radius=0.2, color=GREEN)
        self.play(GrowFromCenter(d3), run_time=0.3)
        self.at("at one", lead=0.2)
        lf = leaf(TX[3], 1.2)
        self.play(gm.animate.move_to([TX[3], 1.2, 0]), FadeIn(lf, scale=0.5), run_time=0.7)
        self.at("looked like")
        ol = T("overlooked: looks like a loss and a return", 30).move_to([0.8, 3.0, 0])
        self.play(FadeIn(ol), run_time=0.8)
        self.at("a loss", lead=0.3)
        loss = Arrow([TX[3], -2.0, 0], [TX[3], -2.9, 0], color=RED, buff=0, stroke_width=8)
        self.play(FadeIn(loss), run_time=0.6)
        self.play(FadeOut(lf), gm.animate.move_to([TX[4], 1.2, 0]), run_time=0.8)
        self.at("a return", lead=0.2)
        d5 = Dot([TX[4], -2.4, 0], radius=0.2, color=GREEN)
        up = Arrow([TX[4], -2.9, 0], [TX[4], -2.0, 0], color=BLUE, buff=0, stroke_width=8)
        self.play(GrowFromCenter(d5), FadeIn(up), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14End(EndCard):
    LINE = "A steady species count can hide a changing list of species."
