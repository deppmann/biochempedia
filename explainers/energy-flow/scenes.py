"""Three Doors: where the energy goes at each feeding step (Biochemistrypedia explainer, remake).

One world all film: producers at the bottom, herbivores above, predators on top, a detritus box at
the lower right. COLOUR MAP: GREEN producers / NPP; PURPLE production passed up; BROWN door, detritus;
GREY (HEAT) respiration leaving as heat; YELLOW sunlight and GPP. All numbers are the lesson's
made-up budget, kJ per m^2 per year. Boxes, pipes and cartoons are schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

_T, _M = T, M


def T(text, size=30, *a, **k):
    return _T(text, round(size * 1.25), *a, **k)


def M(text, size=30, *a, **k):
    return _M(text, round(size * 1.25), *a, **k)


PURPLE = "#B58CD9"
BROWN = "#B9825A"
HEAT = "#B4BBC8"
PALE = "#DDE3EA"

PROD_C = np.array([-4.1, -2.6, 0.0])
HERB_C = np.array([-4.1, 0.3, 0.0])
PRED_C = np.array([-4.1, 2.9, 0.0])
SOIL_C = np.array([3.4, -2.95, 0.0])
BW = 4.8


def rbox(w, h, color, pos, op=0.15, sw=3.5):
    return RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to(pos)


def grass(c, s=1.0):
    g = VGroup(*[Line(ORIGIN, [dx * 0.18 * s, 0.5 * s, 0]).set_stroke(GREEN, 4) for dx in (-2, -1, 0, 1, 2)])
    return g.move_to(c)


def hopper(c, s=1.0):
    body = Ellipse(width=0.9 * s, height=0.42 * s, color=PALE, stroke_width=3).move_to(c)
    head = Circle(radius=0.15 * s, color=PALE, stroke_width=3).move_to(c + np.array([0.52 * s, 0.1 * s, 0]))
    legs = VGroup(*[Line(c + np.array([x * s, -0.1 * s, 0]), c + np.array([(x - 0.15) * s, -0.4 * s, 0]), color=PALE, stroke_width=3)
                    for x in (-0.25, 0.0, 0.25)])
    return VGroup(body, head, legs)


def spider(c, s=1.0):
    b = Circle(radius=0.2 * s, color=PALE, stroke_width=3).move_to(c)
    h = Circle(radius=0.11 * s, color=PALE, stroke_width=3).move_to(c + np.array([0.28 * s, 0, 0]))
    legs = VGroup()
    for k, sg in enumerate((-1, 1)):
        for j in range(4):
            y = (j - 1.5) * 0.12 * s
            legs.add(Line(c + np.array([0, y, 0]), c + np.array([sg * 0.45 * s, y + (j - 1.5) * 0.12 * s, 0]), color=PALE, stroke_width=2.5))
    return VGroup(b, h, legs)


def door(pos, color, w=0.46, h=1.05):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.45).move_to(pos)
    k = Dot(radius=0.05, color=TEXT).move_to(pos + np.array([w * 0.2, 0, 0]))
    return VGroup(r, k)


def stream(a, b, color, n=7, speed=0.3, r=0.09, wave=0.0):
    """A looping stream of dots from a to b (a rate, drawn as motion)."""
    a = np.array(a, float)
    b = np.array(b, float)
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    g.t = 0.0
    d = b - a
    perp = np.array([-d[1], d[0], 0.0])
    perp = perp / (np.linalg.norm(perp) + 1e-9)

    def upd(m, dt):
        m.t += dt
        for i, dot in enumerate(m):
            ph = (i / n + m.t * speed) % 1
            dot.move_to(a + d * ph + perp * wave * np.sin(ph * 9 + i))
            dot.set_opacity(float(min(1, ph * 6, (1 - ph) * 6)))
    g.add_updater(upd)
    upd(g, 0)
    return g


def gauge(center, w, h, tr, color, op=0.5, maxh=None):
    """A fill inside a box, tied to a tracker (0..1)."""
    mh = maxh or h

    def mk():
        hh = max(tr.get_value() * mh, 0.01)
        return Rectangle(width=w, height=hh, stroke_width=0, fill_color=color, fill_opacity=op).move_to(
            center + np.array([0, -h / 2 + hh / 2, 0]))
    return always_redraw(mk)


def lbl(text, pos, color=TEXT, size=30, edge=None, mono=False):
    t = (M if mono else T)(text, size, color)
    if edge is None:
        return t.move_to(pos)
    return t.move_to(pos, aligned_edge=edge)


def two(a, b, pos, ca, cb, sa=30, sb=30, edge=LEFT, mono_a=True):
    g = VGroup((M if mono_a else T)(a, sa, ca, weight=BOLD) if False else (M if mono_a else T)(a, sa, ca),
               T(b, sb, cb)).arrange(DOWN, buff=0.06, aligned_edge=edge)
    return g.move_to(pos)


class World:
    """Builds the carried objects in fixed places."""

    def __init__(self, prod=True, herb=True, pred=True, soil=False, pf=1.0, hf=0.0):
        self.pf = ValueTracker(pf)
        self.hf = ValueTracker(hf)
        self.prod_box = rbox(BW, 1.6, GREEN, PROD_C)
        self.prod_fill = gauge(PROD_C, BW - 0.1, 1.5, self.pf, GREEN, 0.5, maxh=1.5)
        self.prod_lab = T("Producers", 30, TEXT).move_to(PROD_C + np.array([-0.8, 0, 0]))
        self.prod_art = grass(PROD_C + np.array([1.7, -0.3, 0]), 1.3)
        self.prod = VGroup(self.prod_fill, self.prod_box, self.prod_lab, self.prod_art)
        self.herb_box = rbox(BW, 1.7, PALE, HERB_C, op=0.08)
        self.herb_fill = gauge(HERB_C, BW - 0.1, 1.6, self.hf, GREEN, 0.4, maxh=1.6)
        self.herb_lab = T("Herbivores", 30, TEXT).move_to(HERB_C + np.array([-0.8, 0, 0]))
        self.herb_art = hopper(HERB_C + np.array([1.6, 0, 0]), 1.3)
        self.herb = VGroup(self.herb_fill, self.herb_box, self.herb_lab, self.herb_art)
        self.pred_box = rbox(BW, 1.3, PALE, PRED_C, op=0.08)
        self.pred_lab = T("Predators", 30, TEXT).move_to(PRED_C + np.array([-0.8, 0, 0]))
        self.pred_art = spider(PRED_C + np.array([1.6, 0, 0]), 1.3)
        self.pred = VGroup(self.pred_box, self.pred_lab, self.pred_art)
        self.soil_box = rbox(6.2, 1.4, BROWN, SOIL_C, op=0.22)
        self.soil_lab = T("Detritus", 30, BROWN).move_to(SOIL_C + np.array([-1.35, 0, 0]))
        self.soil = VGroup(self.soil_box, self.soil_lab)
        self.parts = []
        if prod:
            self.parts.append(self.prod)
        if herb:
            self.parts.append(self.herb)
        if pred:
            self.parts.append(self.pred)
        if soil:
            self.parts.append(self.soil)

    def add_to(self, scene):
        scene.add(*self.parts)


def critters():
    """bacterium, fungus, worm inside the detritus box (schematic)."""
    bac = RoundedRectangle(corner_radius=0.1, width=0.4, height=0.2, color=TEAL, stroke_width=3)
    fun = VGroup(Arc(radius=0.2, start_angle=0, angle=PI, color="#D9C6A0", stroke_width=4),
                 Line([0, 0, 0], [0, -0.22, 0], color="#D9C6A0", stroke_width=4)).move_to([0, 0, 0])
    worm = ParametricFunction(lambda t: np.array([t, 0.1 * np.sin(4 * t), 0]), t_range=[-0.35, 0.35], color="#E3A3A3", stroke_width=5)
    pos = [SOIL_C + np.array([0.5, 0.05, 0]), SOIL_C + np.array([1.5, 0.05, 0]), SOIL_C + np.array([2.4, 0.05, 0])]
    for m in (bac, fun, worm):
        m.scale(1.5)
    for m, p in zip((bac, fun, worm), pos):
        m.move_to(p)
    return bac, fun, worm


def wiggle(mob, amp=0.06, speed=2.0):
    mob.base = mob.get_center().copy()
    mob.tt = 0.0

    def u(m, dt):
        m.tt += dt
        m.move_to(m.base + np.array([0, amp * np.sin(m.tt * speed), 0]))
    mob.add_updater(u)


def pulse(mob, base=0.4, amp=0.2, speed=2.5):
    mob.tt = 0.0

    def u(m, dt):
        m.tt += dt
        m.set_fill(opacity=base + amp * np.sin(m.tt * speed))
    mob.add_updater(u)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Energy Flow and Productivity"
    TITLE = "Three Doors"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        patch = Square(side_length=3.4, stroke_color=TEXT, stroke_width=5, fill_color=GREEN, fill_opacity=0.22)
        blades = VGroup(*[grass([x, y, 0], 0.7) for x in (-1.0, 0, 1.0) for y in (-0.9, 0.2)])
        plab = T("1 m²", 40, TEXT).next_to(patch, UP, buff=0.2)
        pt = VGroup(patch, blades)
        self.play(FadeIn(pt), FadeIn(plab), run_time=self.beat(0.08))
        self.at("square meter")
        w = World()
        sun = Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([0.9, -1.3, 0])
        sun_s = stream([0.6, -1.5, 0], [-1.7, -2.4, 0], YELLOW, n=8, speed=0.35, r=0.1)
        self.play(ReplacementTransform(pt, w.prod), FadeOut(plab), FadeIn(w.herb), FadeIn(w.pred),
                  FadeIn(sun), FadeIn(sun_s), run_time=self.beat(0.16))
        w.pf.set_value(1.0)
        tr = ValueTracker(0)
        self.add(tr)
        count = always_redraw(lambda: M(f"{int(tr.get_value()):,}", 54, YELLOW).move_to([3.7, -0.1, 0]))
        cl = T("kJ fixed per year", 30, YELLOW).move_to([3.7, -0.85, 0])
        self.add(count)
        self.play(FadeIn(cl), tr.animate.set_value(12000), run_time=self.t_of("year") - self.elapsed() + 0.3,
                  rate_func=linear)
        self.at("Why does so little")
        q = T("?", 72, YELLOW, weight=BOLD).move_to(PRED_C + np.array([-0.2, 0.05, 0]))
        q.move_to(np.array([-1.1, 2.9, 0]))
        glow = w.pred_box.copy().set_stroke(YELLOW, 5).set_fill(YELLOW, 0.1)
        pulse(glow, 0.1, 0.1)
        self.play(FadeIn(q), FadeIn(glow), run_time=self.beat(0.06))
        self.at("animals at the top")
        self.play(Indicate(q, scale_factor=1.3, color=YELLOW), run_time=self.beat(0.1))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Rate(SpokenScene):
    def construct(self):
        w = World()
        w.add_to(self)
        sun = Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([0.9, -1.3, 0])
        sun_s = stream([0.6, -1.5, 0], [-1.7, -2.4, 0], YELLOW, n=8, speed=0.35, r=0.1)
        self.add(sun, sun_s)
        yr = ValueTracker(0)
        yr.add_updater(lambda m, dt: m.increment_value(dt * 2.2))
        self.add(yr)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        def cal():
            v = yr.get_value() % 12
            t = M(months[int(v)], 48, TEXT).move_to([3.4, 3.0, 0])
            frame = RoundedRectangle(corner_radius=0.12, width=2.2, height=1.0, stroke_color=GREY, stroke_width=3).move_to([3.4, 3.0, 0])
            bar = Rectangle(width=2.0 * (v / 12), height=0.08, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
            bar.move_to([2.4, 2.65, 0], aligned_edge=LEFT)
            return VGroup(frame, t, bar)
        cal_mob = always_redraw(cal)
        self.play(FadeIn(cal_mob), run_time=self.beat(0.05))
        self.at("Each one is a rate")
        u = M("kJ per m² per year", 26, YELLOW).move_to([3.7, 1.5, 0])
        self.play(FadeIn(u), run_time=self.beat(0.05))
        self.at("That is production")
        prod_tag = T("production = rate (flow)", 28, GREEN).move_to([0.9, -0.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(prod_tag, shift=RIGHT * 0.2), Indicate(sun_s, color=YELLOW, scale_factor=1.0), run_time=self.beat(0.06))
        self.at("not the balance")
        stock = T("biomass = stock (balance)", 28, GREEN).move_to([-1.2, -3.2, 0], aligned_edge=LEFT)
        arr = Arrow([-1.25, -3.2, 0], [-1.7, -3.2, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.2)
        self.play(FadeIn(stock), FadeIn(arr), Circumscribe(w.prod_box, color=GREEN, time_width=1.0), run_time=self.beat(0.08))
        self.finish()


# ---------------------------------------------------------------------------------------------
def heat_prod(rate=0.3, n=7):
    return stream([-1.7, -2.2, 0], [-0.6, 1.7, 0], HEAT, n=n, speed=rate, r=0.09, wave=0.18)


class S03Gross(SpokenScene):
    def construct(self):
        w = World(pred=False)
        w.add_to(self)
        gpp = two("12,000", "GPP", [2.0, -2.5, 0], YELLOW, YELLOW, 48, 30)
        self.add(gpp)
        sun = Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([0.9, -1.0, 0])
        sun_s = stream([0.6, -1.2, 0], [-1.7, -2.2, 0], YELLOW, n=8, speed=0.35, r=0.1)
        self.add(sun, sun_s)
        self.at("gross primary production")
        self.play(Indicate(gpp, color=YELLOW, scale_factor=1.15), run_time=self.beat(0.08))
        self.at("The plants respire")
        self.play(FadeOut(sun), FadeOut(sun_s), run_time=self.beat(0.04))
        hs = heat_prod()
        tag = VGroup(T("respired by producers", 30, HEAT), M("Ra: 6,000", 36, HEAT)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        tag.move_to([0.8, 2.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(hs), FadeIn(tag), run_time=self.beat(0.06))
        self.at("In this budget it is half")
        self.play(w.pf.animate.set_value(0.5), run_time=self.t_of("heat.") - self.elapsed() + 0.2, rate_func=smooth)
        self.finish()


class S04Net(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=0.5)
        w.add_to(self)
        gpp = two("12,000", "GPP", [2.0, -2.5, 0], YELLOW, YELLOW, 48, 30)
        hs = heat_prod(0.25, 5)
        tag = VGroup(T("respired by producers", 30, HEAT), M("Ra: 6,000", 36, HEAT)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        tag.move_to([0.8, 2.0, 0], aligned_edge=LEFT)
        self.add(gpp, hs, tag)
        self.at("net primary production")
        self.play(FadeOut(tag), FadeOut(gpp), run_time=self.beat(0.06))
        npp = two("NPP = 6,000", "net primary production", [2.0, -2.5, 0], GREEN, GREEN, 40, 28)
        glow = w.prod_box.copy().set_stroke(GREEN, 8).set_fill(GREEN, 0.0)
        pulse(glow, 0.0, 0.0)
        self.play(FadeIn(npp), Create(glow), run_time=self.beat(0.1))
        eq = M("NPP = GPP − Ra", 32, TEXT).move_to([0.4, -0.9, 0], aligned_edge=LEFT)
        self.play(FadeIn(eq), run_time=self.beat(0.06))
        self.at("all the energy left")
        up = stream([-4.1, -1.8, 0], [-4.1, -0.6, 0], GREEN, n=4, speed=0.3, r=0.1)
        hb = w.herb_box.copy().set_stroke(GREEN, 6)
        self.play(FadeIn(up), FadeIn(hb), run_time=self.beat(0.08))
        self.at("to eat or to store")
        self.play(Indicate(npp, color=GREEN, scale_factor=1.1), run_time=self.beat(0.1))
        self.finish()


# ---------------------------------------------------------------------------------------------
def doors_set():
    brown = door([-1.55, -2.6, 0], BROWN)
    grey = door([-1.55, 0.75, 0], HEAT)
    pipe = Rectangle(width=0.34, height=1.35, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.6).move_to([-4.1, -1.17, 0])
    return brown, grey, pipe


class S05Doors(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=0.5)
        w.add_to(self)
        npp = two("NPP = 6,000", "net primary production", [2.0, -2.5, 0], GREEN, GREEN, 40, 28)
        self.add(npp)
        self.at("follow it up")
        self.play(FadeOut(npp), Circumscribe(VGroup(w.prod_box, w.herb_box), color=GREEN), run_time=self.beat(0.1))
        brown, grey, pipe = doors_set()
        self.at("three ways out")
        self.play(FadeIn(brown, shift=LEFT * 0.2), run_time=self.beat(0.05))
        lb = T("detritus", 32, BROWN).move_to([-0.6, -2.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(lb), run_time=self.beat(0.03))
        self.play(FadeIn(grey, shift=LEFT * 0.2), run_time=self.beat(0.05))
        lg = T("heat", 32, HEAT).move_to([-1.1, 0.75, 0], aligned_edge=LEFT)
        hs = stream([-1.5, 0.95, 0], [-0.7, 2.6, 0], HEAT, n=4, speed=0.3, r=0.09, wave=0.15)
        self.play(FadeIn(lg), FadeIn(hs), run_time=self.beat(0.04))
        self.play(FadeIn(pipe, shift=UP * 0.2), run_time=self.beat(0.05))
        lp = T("passed up", 32, PURPLE).move_to([-3.2, -1.17, 0], aligned_edge=LEFT)
        up = stream([-4.1, -1.8, 0], [-4.1, -0.55, 0], PURPLE, n=3, speed=0.3, r=0.08)
        self.play(FadeIn(lp), FadeIn(up), run_time=self.beat(0.04))
        self.at("Call them doors")
        self.play(Wiggle(brown, scale_value=1.1), Wiggle(grey, scale_value=1.1), run_time=self.beat(0.12))
        self.finish()


def predict_group():
    t1 = T("most is eaten", 36, TEXT)
    b1 = RoundedRectangle(corner_radius=0.15, width=t1.width + 0.5, height=0.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12)
    o1 = VGroup(b1, t1.move_to(b1)).move_to([3.2, 0.3, 0])
    t2 = T("only a little is eaten", 36, TEXT)
    b2 = RoundedRectangle(corner_radius=0.15, width=t2.width + 0.5, height=0.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12)
    o2 = VGroup(b2, t2.move_to(b2)).move_to([3.2, -1.0, 0])
    return o1, o2


class S06Predict(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=0.5)
        w.add_to(self)
        wiggle(w.herb_art, 0.08, 3.0)
        blades = VGroup(*[grass([-5.0 + 0.55 * i, -1.65, 0], 0.5) for i in range(7)])
        self.play(FadeIn(blades), run_time=self.beat(0.08))
        o1, o2 = predict_group()
        self.at("could eat most")
        self.play(FadeIn(o1, shift=LEFT * 0.3), run_time=self.beat(0.08))
        self.at("or only a little")
        self.play(FadeIn(o2, shift=LEFT * 0.3), run_time=self.beat(0.08))
        self.at("Which do you expect")
        q = T("Which do you expect?", 40, YELLOW).move_to([3.2, 2.0, 0])
        self.play(FadeIn(q), run_time=self.beat(0.08))
        self.play(Indicate(o1, color=YELLOW), Indicate(o2, color=YELLOW), run_time=self.beat(0.15))
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        w = World(pred=False, pf=0.5)
        w.add_to(self)
        wiggle(w.herb_art, 0.08, 3.0)
        blades = VGroup(*[grass([-5.0 + 0.55 * i, -1.65, 0], 0.5) for i in range(7)])
        o1, o2 = predict_group()
        q = VGroup(T("Predict: how much of NPP", 36, YELLOW), T("do the herbivores eat?", 36, YELLOW)).arrange(DOWN, buff=0.1).move_to([2.8, 2.3, 0])
        self.add(blades, o1, o2, q)
        tr = ValueTracker(5.0)
        tr.add_updater(lambda m, dt: m.increment_value(-dt))
        self.add(tr)
        cd = always_redraw(lambda: M(str(max(1, int(np.ceil(tr.get_value())))), 60, TEXT).move_to([3.2, -2.4, 0]))
        self.add(cd)
        self.wait(5.0)


# ---------------------------------------------------------------------------------------------
class S08Reveal(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=0.5, soil=True)
        w.add_to(self)
        wiggle(w.herb_art, 0.08, 3.0)
        brown, grey, pipe = doors_set()
        self.add(brown, grey, pipe)
        o1, o2 = predict_group()
        self.add(o2)
        self.play(FadeOut(o2[1]) if False else Indicate(o2, color=YELLOW), run_time=self.beat(0.06))
        self.at("less than a third")
        ing = stream([-4.4, -1.85, 0], [-4.4, -0.5, 0], GREEN, n=3, speed=0.3, r=0.09)
        il = VGroup(M("ingested: 1,800", 26, GREEN), M("(30% of NPP)", 26, GREEN)).arrange(DOWN, buff=0.05, aligned_edge=LEFT).move_to([-3.7, -1.17, 0], aligned_edge=LEFT)
        self.play(FadeOut(o2), FadeIn(ing), FadeIn(il), run_time=self.beat(0.08))
        self.at("The rest is never eaten")
        ul = VGroup(M("uneaten → detritus:", 26, BROWN), M("4,200", 36, BROWN)).arrange(DOWN, buff=0.05).move_to([4.0, -1.5, 0])
        wide = stream([-1.4, -2.6, 0], [0.5, -2.9, 0], BROWN, n=18, speed=0.5, r=0.15)
        pulse(w.soil_box, 0.22, 0.12, 2.0)
        self.play(FadeIn(wide), FadeIn(ul), run_time=self.beat(0.07))
        self.at("drops through the brown door")
        self.play(Wiggle(brown, scale_value=1.15), run_time=self.beat(0.07))
        self.at("Detritus is dead matter")
        bac, fun, worm = critters()
        self.at("bacteria")
        self.play(FadeIn(bac, scale=1.5), run_time=self.beat(0.04))
        self.at("fungi")
        self.play(FadeIn(fun, scale=1.5), run_time=self.beat(0.04))
        self.at("animals that eat it")
        self.play(FadeIn(worm, scale=1.5), run_time=self.beat(0.04))
        for m in (bac, fun, worm):
            wiggle(m, 0.1, 3.0)
        self.finish()


def soil_stuff():
    bac, fun, worm = critters()
    for m in (bac, fun, worm):
        wiggle(m, 0.1, 3.0)
    return VGroup(bac, fun, worm)


class S09Feces(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=0.5, soil=True, hf=0.0)
        w.add_to(self)
        wiggle(w.herb_art, 0.15, 4.0)
        brown, grey, pipe = doors_set()
        self.add(brown, grey, pipe, soil_stuff())
        ing = stream([-4.4, -1.85, 0], [-4.4, -0.5, 0], GREEN, n=4, speed=0.5, r=0.11)
        self.add(ing)
        il = VGroup(M("ingested: 1,800", 26, GREEN)).move_to([-3.7, -1.17, 0], aligned_edge=LEFT)
        self.add(il)
        self.at("much passes straight through")
        self.play(FadeOut(il), run_time=self.beat(0.04))
        fe = stream([-1.7, -0.1, 0], [1.2, -2.3, 0], BROWN, n=8, speed=0.3, r=0.12)
        fl = VGroup(M("egested (feces):", 26, BROWN), M("1,080", 36, BROWN)).arrange(DOWN, buff=0.05).move_to([3.3, -0.3, 0])
        self.play(FadeIn(fe), FadeIn(fl), run_time=self.beat(0.08))
        w.hf.set_value(0.0)
        self.play(w.hf.animate.set_value(0.6), run_time=self.beat(0.15))
        al = VGroup(M("assimilated:", 26, GREEN), M("720", 36, GREEN)).arrange(DOWN, buff=0.05).move_to([3.3, 1.5, 0])
        self.play(FadeIn(al), run_time=self.beat(0.06))
        self.at("goes out the brown door")
        self.play(Wiggle(brown, scale_value=1.15), run_time=self.beat(0.1))
        self.at("into the same detritus")
        self.play(Indicate(w.soil_box, color=BROWN, scale_factor=1.03), run_time=self.beat(0.15))
        self.finish()


class S10Heat(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=0.5, soil=True, hf=0.6)
        w.add_to(self)
        wiggle(w.herb_art, 0.08, 3.0)
        brown, grey, pipe = doors_set()
        self.add(brown, grey, pipe, soil_stuff())
        al = VGroup(M("assimilated:", 26, GREEN), M("720", 36, GREEN)).arrange(DOWN, buff=0.05).move_to([3.3, 1.2, 0])
        self.add(al)
        self.at("a large part is respired")
        hs = stream([-1.5, 0.95, 0], [-0.2, 3.4, 0], HEAT, n=8, speed=0.3, r=0.1, wave=0.2)
        hl = VGroup(M("respired → heat:", 26, HEAT), M("360", 36, HEAT)).arrange(DOWN, buff=0.05).move_to([3.2, 3.0, 0])
        self.play(FadeIn(hs), FadeIn(hl), w.hf.animate.set_value(0.3), run_time=self.t_of("alive") - self.elapsed() + 0.4)
        self.at("leaves through the gray door")
        self.play(Wiggle(grey, scale_value=1.2), run_time=self.beat(0.12))
        self.finish()


class S11Up(SpokenScene):
    def construct(self):
        w = World(pred=True, pf=0.5, soil=True, hf=0.3)
        w.add_to(self)
        brown, grey, pipe = doors_set()
        self.add(brown, grey, pipe, soil_stuff())
        wide = stream([-1.4, -2.6, 0], [0.5, -2.9, 0], BROWN, n=14, speed=0.35, r=0.13)
        self.add(wide)
        self.at("new herbivore tissue")
        kids = VGroup(*[hopper(HERB_C + np.array([1.05 + 0.6 * i, -0.2 + 0.1 * (i % 2), 0]), 0.5) for i in range(3)])
        self.play(FadeOut(w.herb_art), FadeIn(kids, shift=UP * 0.2), w.hf.animate.set_value(0.0), run_time=self.beat(0.14))
        self.at("That is the herbivore's production")
        pl = VGroup(M("herbivore production:", 24, PURPLE), M("360", 36, PURPLE)).arrange(DOWN, buff=0.05).move_to([3.5, 1.5, 0])
        up = stream([-4.1, -1.8, 0], [-4.1, -0.55, 0], PURPLE, n=3, speed=0.3, r=0.07)
        self.play(FadeIn(pl), FadeIn(up), run_time=self.beat(0.08))
        self.at("Predators can eat it")
        q = T("?", 56, PURPLE, weight=BOLD).move_to(PRED_C + np.array([2.2, 0, 0]))
        self.play(Indicate(w.pred_box, color=PURPLE, scale_factor=1.05), run_time=self.beat(0.1))
        self.at("do not eat all")
        self.play(Indicate(pl, color=PURPLE), run_time=self.beat(0.1))
        self.finish()


# ---------------------------------------------------------------------------------------------
PX = 0.4  # x of the valve pipe


def valve_world(self_):
    w = World(pred=False, pf=0.5)
    w.add_to(self_)
    return w


VY = [-0.9, 0.7, 2.3]
VW = [0.8, 0.24, 0.1, 0.05]
VLAB = [("consumption efficiency", "0.30", "lost to detritus", BROWN),
        ("assimilation efficiency", "0.40", "lost to detritus", BROWN),
        ("net production efficiency", "0.50", "lost as heat", HEAT)]


def pipe_segs():
    segs = VGroup()
    ys = [-2.6, VY[0], VY[1], VY[2], 3.4]
    for i in range(4):
        y0, y1 = ys[i], ys[i + 1]
        segs.add(Rectangle(width=max(VW[i], 0.05), height=y1 - y0, stroke_width=0, fill_color=PURPLE,
                           fill_opacity=0.7).move_to([PX, (y0 + y1) / 2, 0]))
    feeder = Line([-1.7, -2.6, 0], [PX - 0.4, -2.6, 0], color=PURPLE, stroke_width=8)
    return segs, feeder


def valve(y, color):
    a = Polygon([-0.3, 0.25, 0], [0.3, 0.25, 0], [0, 0, 0], color=color, fill_color=color, fill_opacity=0.8, stroke_width=3)
    b = Polygon([-0.3, -0.25, 0], [0.3, -0.25, 0], [0, 0, 0], color=color, fill_color=color, fill_opacity=0.8, stroke_width=3)
    return VGroup(a, b).move_to([PX, y, 0])


def vlabel(i, with_loss=True):
    nm, num, loss, c = VLAB[i]
    g = VGroup(T(nm, 28, PURPLE), M(num, 32, TEXT)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    return g.move_to([1.1, VY[i], 0], aligned_edge=LEFT)


class S12Valves(SpokenScene):
    def construct(self):
        w = valve_world(self)
        hb = w.herb_box
        segs, feeder = pipe_segs()
        self.at("a fraction")
        self.play(FadeIn(feeder), FadeIn(segs[0]), run_time=self.beat(0.06))
        self.at("valve on the pipe")
        self.play(FadeIn(segs[1:]), run_time=self.beat(0.06))
        vals = [valve(VY[i], VLAB[i][3]) for i in range(3)]
        loss = []
        for i in range(3):
            loss.append(stream([PX - 0.3, VY[i], 0], [PX - 1.9, VY[i] + 0.05, 0], VLAB[i][3], n=4, speed=0.4, r=0.09))
        self.play(FadeIn(VGroup(*vals)), run_time=self.beat(0.06))
        self.at("share eaten")
        self.play(FadeIn(vlabel(0)), FadeIn(loss[0]), run_time=self.beat(0.06))
        self.at("share absorbed")
        self.play(FadeIn(vlabel(1)), FadeIn(loss[1]), run_time=self.beat(0.06))
        self.at("made into tissue")
        self.play(FadeIn(vlabel(2)), FadeIn(loss[2]), run_time=self.beat(0.06))
        self.finish()


class S13Product(SpokenScene):
    def construct(self):
        w = valve_world(self)
        segs, feeder = pipe_segs()
        vals = VGroup(*[valve(VY[i], VLAB[i][3]) for i in range(3)])
        labs = VGroup(*[vlabel(i) for i in range(3)])
        loss = [stream([PX - 0.3, VY[i], 0], [PX - 1.9, VY[i] + 0.05, 0], VLAB[i][3], n=4, speed=0.4, r=0.09) for i in range(3)]
        self.add(feeder, segs, vals, labs, *loss)
        self.at("three valves in a row")
        self.play(Indicate(vals, color=PURPLE), run_time=self.beat(0.1))
        self.at("product of the three fractions")
        nums = VGroup(*[labs[i][1].copy() for i in range(3)])
        eq = M("0.30 × 0.40 × 0.50 = 0.06", 24, TEXT).move_to([2.7, 0.9, 0])
        self.play(FadeOut(labs), FadeOut(vals), *[FadeOut(l) for l in loss], FadeOut(segs[1:]), FadeIn(nums), run_time=0.1)
        self.play(ReplacementTransform(nums, eq), run_time=self.beat(0.15))
        self.at("trophic transfer efficiency")
        tl = T("trophic transfer efficiency", 28, PURPLE).move_to([2.7, 2.1, 0])
        r6 = M("360 / 6,000 = 6%", 28, PURPLE).move_to([2.7, -0.4, 0])
        self.play(FadeIn(tl), FadeIn(r6), run_time=self.beat(0.1))
        self.play(Indicate(r6, color=PURPLE, scale_factor=1.12), Indicate(feeder, color=PURPLE), run_time=self.beat(0.1))
        self.finish()


class S14Ledger(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=0.5)
        w.add_to(self)
        brown, grey, pipe = doors_set()
        self.add(brown, grey, pipe)
        sc = 6.4 / 6000
        x = 2.5
        y0 = -3.3
        pieces = [(4200, BROWN, "4,200 uneaten"), (1080, BROWN, "1,080 feces"), (360, HEAT, "360 heat"), (360, PURPLE, "360 passed up")]
        label_y = [-1.0, 1.75, 2.4, 3.1]
        outline = Rectangle(width=1.2, height=6.4, stroke_color=GREY, stroke_width=2).move_to([x, y0 + 3.2, 0])
        self.add(outline)
        self.at("three doors together")
        yb = y0
        bars = []
        for i, (v, c, nm) in enumerate(pieces):
            h = v * sc
            r = Rectangle(width=1.2, height=h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.55).move_to([x, yb + h / 2, 0])
            lab = T(nm, 28, c).move_to([3.5, label_y[i], 0], aligned_edge=LEFT)
            cl = Line([x + 0.62, yb + h / 2, 0], [3.45, label_y[i], 0], color=c, stroke_width=2)
            self.play(FadeIn(r, shift=UP * 0.15), FadeIn(lab), FadeIn(cl), run_time=self.beat(0.09))
            yb += h
            bars.append(r)
        self.at("In this budget")
        br = Brace(Rectangle(width=1.2, height=6.4).move_to([x, y0 + 3.2, 0]), LEFT, color=TEXT)
        tl = M("= 6,000 NPP", 24, TEXT).move_to([0.0, y0 + 3.2, 0])
        self.play(FadeIn(br), FadeIn(tl), run_time=self.beat(0.08))
        ck = VMobject(color=GREEN, stroke_width=10).set_points_as_corners([[0, 0, 0], [0.3, -0.35, 0], [0.9, 0.5, 0]]).move_to([5.4, 0.3, 0])
        self.play(Create(ck), run_time=self.beat(0.08))
        self.finish()


class S15Multiply(SpokenScene):
    def construct(self):
        w = World(soil=True, pf=0.5)
        w.add_to(self)
        brown, grey, pipe = doors_set()
        self.add(brown, grey, pipe, soil_stuff())
        self.at("same three doors")
        up2 = Rectangle(width=0.2, height=1.2, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.6).move_to([-4.1, 1.7, 0])
        ing = stream([-4.1, 1.15, 0], [-4.1, 2.3, 0], PURPLE, n=3, speed=0.3, r=0.07)
        il = VGroup(T("ingested by predators", 28, PURPLE), M("200", 36, PURPLE)).arrange(DOWN, buff=0.04, aligned_edge=LEFT).move_to([-3.3, 1.7, 0], aligned_edge=LEFT)
        self.play(FadeIn(up2), FadeIn(ing), FadeIn(il), run_time=self.beat(0.1))
        b2 = door([-1.55, 2.55, 0], BROWN, 0.3, 0.55)
        g2 = door([-1.55, 3.25, 0], HEAT, 0.3, 0.4)
        fe = stream([-1.7, 0.6, 0], [1.2, -2.3, 0], BROWN, n=4, speed=0.3, r=0.11)
        fl = VGroup(M("uneaten → detritus:", 28, BROWN), M("160", 36, BROWN)).arrange(DOWN, buff=0.04).move_to([3.4, -0.5, 0])
        self.play(FadeIn(fe), FadeIn(fl), FadeIn(b2), FadeIn(g2), run_time=self.beat(0.1))
        self.at("So the fractions multiply")
        boxes = VGroup()
        pos = [(1.7, 3.0, 1.9, 0.9), (4.0, 3.0, 1.4, 0.7), (5.7, 3.0, 0.9, 0.5)]
        arrs = VGroup()
        for i, (x, y, bw, bh) in enumerate(pos):
            bx = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=bw, height=bh, stroke_color=PALE, stroke_width=2.5).move_to([x, y, 0]), num_dashes=24)
            boxes.add(bx)
        a0 = Arrow([-1.2, 2.9, 0], [0.7, 2.95, 0], buff=0, color=PURPLE, stroke_width=7, tip_length=0.2)
        a1 = Arrow([2.7, 3.0, 0], [3.3, 3.0, 0], buff=0, color=PURPLE, stroke_width=4, tip_length=0.15)
        a2 = Arrow([4.8, 3.0, 0], [5.2, 3.0, 0], buff=0, color=PURPLE, stroke_width=2.5, tip_length=0.1)
        self.play(FadeIn(boxes), FadeIn(a0), FadeIn(a1), FadeIn(a2), run_time=self.beat(0.15))
        self.at("production shrinks fast")
        sl = VGroup(T("schematic: each level a", 26, GREY), T("fraction of the one below", 26, GREY)).arrange(DOWN, buff=0.05).move_to([4.0, 0.9, 0])
        sl.set_color(HEAT)
        self.play(FadeIn(sl), run_time=self.beat(0.08))
        self.finish()


class S16Scope(SpokenScene):
    def construct(self):
        w = World(soil=True, pf=0.5)
        w.add_to(self)
        brown, grey, pipe = doors_set()
        self.add(brown, grey, pipe)
        sty = soil_stuff()
        self.add(sty)
        t1 = T("one period (usually a year)", 24, TEXT).move_to([0.6, 3.3, 0], aligned_edge=LEFT)
        t2 = T("one currency per area", 24, TEXT).move_to([0.6, 2.5, 0], aligned_edge=LEFT)
        t3 = VGroup(T("consumers eat no more than", 24, TEXT), T("the production below them", 24, TEXT)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([0.6, 1.5, 0], aligned_edge=LEFT)
        self.at("one period")
        self.play(FadeIn(t1, shift=LEFT * 0.2), run_time=self.beat(0.05))
        self.at("one currency")
        self.play(FadeIn(t2, shift=LEFT * 0.2), run_time=self.beat(0.05))
        self.at("consumers eat no more")
        self.play(FadeIn(t3, shift=LEFT * 0.2), run_time=self.beat(0.06))
        self.at("Energy never returns")
        arr = DashedVMobject(Arrow([0.3, -2.5, 0], [-1.7, -2.5, 0], buff=0, color=RED, stroke_width=6, tip_length=0.25), num_dashes=10)
        xx = VGroup(Line([-0.85, -2.3, 0], [-0.45, -2.7, 0]), Line([-0.85, -2.7, 0], [-0.45, -2.3, 0])).set_stroke(RED, 7)
        nl = VGroup(T("energy:", 22, RED), T("no return", 22, RED)).arrange(DOWN, buff=0.03).move_to([-0.5, -1.55, 0])
        self.play(FadeIn(arr), FadeIn(xx), FadeIn(nl), run_time=self.beat(0.08))
        self.at("stored for a while")
        tk = T("stored for a while", 26, BROWN).move_to([3.4, -1.9, 0])
        self.play(FadeIn(tk), run_time=self.beat(0.05))
        self.at("or leaves as heat")
        h1 = stream([-1.6, -2.2, 0], [-1.0, 3.7, 0], HEAT, n=4, speed=0.18, r=0.09, wave=0.15)
        h2 = stream([-1.6, 0.4, 0], [-0.55, 3.7, 0], HEAT, n=4, speed=0.18, r=0.09, wave=0.15)
        self.play(FadeIn(h1), FadeIn(h2), run_time=self.beat(0.06))
        self.finish()


class S17End(EndCard):
    LINE = "Three doors at every step; the shares passed up multiply."
