"""Same Warmth, Two Answers (climate-and-biomes film 2).  Timed to the spoken words via self.at().

COLOR MAP (identical to film 1)
  RED = monthly temperature   BLUE = monthly rain, moist air   GOLD = a dry month, dry sinking air
  GREEN = forest              TAN = savanna / dry grass         ORANGE = fire (new here, one use)
Cartoons are schematic. Climate-diagram lines are computed from the made-up station numbers in the
lesson (dry month when rain (mm) < 2 x temperature (C)); the rain axis shrinks above 100 mm.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

TAN = "#C9A66B"
PALE = "#BFD9E8"
MONTHS = "JFMAMJJASOND"
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
GROUND_TOP = -2.6


def LX(lat):
    return lat * 0.11


def lab(text, size=30, color=TEXT, halo=False, **kw):
    t = T(text, size, color, **kw)
    if halo:
        t.set_stroke(BG, 8, background=True)
    return t

# ---------------------------------------------------------------- small cartoons
def therm_glyph(center, level, h=0.9):
    outline = RoundedRectangle(corner_radius=0.07, width=0.16, height=h, stroke_color=TEXT, stroke_width=2.5, fill_opacity=0)
    fh = max(0.03, (h - 0.1) * level)
    fill = Rectangle(width=0.09, height=fh, stroke_width=0, fill_color=RED, fill_opacity=1)
    fill.move_to(outline.get_bottom() + UP * (0.05 + fh / 2))
    bulb = Dot(outline.get_bottom() + UP * 0.02, radius=0.12, color=RED)
    return VGroup(outline, fill, bulb).move_to(center)


def tree(x, y, s=1.0, color=GREEN):
    trunk = Line([x, y, 0], [x, y + 0.35 * s, 0], color=GREY, stroke_width=4)
    crown = Circle(radius=0.3 * s, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x, y + 0.6 * s, 0])
    return VGroup(trunk, crown)


def sun_glyph(pos, r=0.32):
    g = VGroup(Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1))
    for k in range(8):
        a = k * math.pi / 4
        g.add(Line([r * 1.35 * math.cos(a), r * 1.35 * math.sin(a), 0], [r * 1.85 * math.cos(a), r * 1.85 * math.sin(a), 0], color=YELLOW, stroke_width=4))
    return g.move_to(pos)


def cloud_shape(color=TEXT):
    g = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.92).move_to([x, y, 0])
                 for x, y, r in [(-0.55, 0, 0.38), (-0.1, 0.18, 0.5), (0.45, 0.02, 0.4), (0.0, -0.08, 0.42)]])
    return g


def drop_icon(color=BLUE, s=1.0):
    d = VGroup(Triangle(stroke_width=0, fill_color=color, fill_opacity=1).scale(0.3 * s).shift(UP * 0.2 * s),
               Circle(radius=0.26 * s, stroke_width=0, fill_color=color, fill_opacity=1).shift(DOWN * 0.06 * s))
    return d


def make_parcel(color=BLUE, r=0.45, ndots=5):
    c = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
    pos = [(-0.18, 0.12), (0.1, 0.22), (0.2, -0.05), (-0.08, -0.16), (0.04, 0.02)][:ndots]
    dots = VGroup(*[Dot([x * r / 0.45, y * r / 0.45, 0], radius=0.06 * r / 0.45, color=TEXT) for x, y in pos])
    return VGroup(c, dots)


def sway(group, amp=0.05, speed=1.4):
    group.t = 0.0
    group.base = [m.get_center().copy() for m in group]

    def upd(g, dt):
        g.t += dt
        for i, m in enumerate(g):
            m.move_to(g.base[i] + UP * amp * math.sin(g.t * speed + i * 0.9))
    group.add_updater(upd)
    return group


def make_rain(cx_fn, halfw=0.95, ytop=1.2, ybot=-2.5, n=8):
    g = VGroup(*[Line(ORIGIN, DOWN * 0.35, color=BLUE, stroke_width=4) for _ in range(n)])
    g.t = 0.0
    g.offs = [(-halfw + 2 * halfw * i / (n - 1), (i * 0.37) % 1) for i in range(n)]

    def upd(m, dt):
        m.t += dt
        cx = cx_fn()
        for line, (ox, ph) in zip(m, m.offs):
            y = ytop - ((ph + m.t * 0.7) % 1) * (ytop - ybot)
            line.put_start_and_end_on([cx + ox, y, 0], [cx + ox - 0.08, y - 0.35, 0])
    g.add_updater(upd)
    upd(g, 0)
    return g


class Band:
    """The rain belt: green ground, cloud and falling rain, all following one tracker (schematic)."""
    def __init__(self, x=0.0, ground_color=GREEN):
        self.bx = ValueTracker(x)
        self.ground = Rectangle(width=2.2, height=0.2, stroke_width=0, fill_color=ground_color, fill_opacity=0.85)
        self.ground.add_updater(lambda m: m.move_to([self.bx.get_value(), -2.7, 0]))
        self.cloud = cloud_shape().scale(1.7)
        self.cloud.add_updater(lambda m: m.move_to([self.bx.get_value(), 1.6, 0]))
        self.rain = make_rain(lambda: self.bx.get_value())
        for m in (self.ground, self.cloud):
            m.update()


def base_world(labels=True):
    ground = Rectangle(width=13.2, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to([0, -3.0, 0])
    sky = Rectangle(width=13.2, height=5.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.13).move_to([0, 0.15, 0])
    g = VGroup(sky, ground)
    if labels:
        g.add(lab("Equator", 24, TEXT).move_to([0, -3.12, 0]),
              lab("30°N", 24, TEXT).move_to([LX(30), -3.12, 0]),
              lab("30°S", 24, TEXT).move_to([-LX(30), -3.12, 0]))
    return g


def loop_fn(side):
    cx, cy, a, b, p = LX(30) / 2, -0.1, LX(30) / 2, 2.2, 0.4

    def f(ph):
        t = -2 * math.pi * ph + math.pi
        c, s = math.cos(t), math.sin(t)
        x = cx + a * math.copysign(abs(c) ** p, c)
        y = cy + b * math.copysign(abs(s) ** p, s)
        return np.array([side * x, y, 0.0])
    return f


def loop_path(side, opacity=0.4):
    f = loop_fn(side)
    return VMobject().set_points_smoothly([f(i / 80) for i in range(81)]).set_stroke(TEXT, 3, opacity)


def flow_dots(side, n=9, speed=0.09, opacity=0.8):
    f = loop_fn(side)
    g = VGroup(*[Dot(radius=0.07, color=BLUE) for _ in range(n)])
    g.t = 0.0

    def upd(m, dt):
        m.t += dt
        for i, d in enumerate(m):
            ph = (i / n + m.t * speed) % 1
            d.move_to(f(ph))
            d.set_color(BLUE if ph < 0.25 else (PALE if ph < 0.5 else GOLD)).set_opacity(opacity)
    g.add_updater(upd)
    upd(g, 0)
    return g


def tan_patches(op=0.55):
    return VGroup(*[Rectangle(width=2.0, height=0.2, stroke_width=0, fill_color=TAN, fill_opacity=op).move_to([s * LX(30), -2.7, 0]) for s in (1, -1)])


# ---------------------------------------------------------------- Amazon / Sahara panels (s01, s05)
def panel_pair():
    def panel(x, kind):
        frame = RoundedRectangle(corner_radius=0.2, width=5.7, height=6.2, stroke_color=GREEN if kind == "a" else TAN, stroke_width=3,
                                 fill_color=GREEN if kind == "a" else TAN, fill_opacity=0.08).move_to([x, -0.1, 0])
        scene = VGroup()
        if kind == "a":
            for i in range(7):
                for j in range(2):
                    scene.add(tree(x - 2.3 + i * 0.77 + 0.3 * (j % 2), -2.9 + j * 0.62, 1.25))
        else:
            for k in range(3):
                dune = FunctionGraph(lambda t, k=k: 0.3 * math.sin(1.3 * t + k) + 0.15 * math.sin(3 * t), x_range=[-2.6, 2.6], color=TAN, stroke_width=0)
                dune = VMobject().set_points_smoothly([[x + t, -2.6 + k * 0.5 + 0.3 * math.sin(1.3 * t + k * 1.7) , 0] for t in np.linspace(-2.6, 2.6, 24)])
                dune.set_stroke(TAN, 6, 0.95)
                scene.add(dune)
        name = lab("Amazon" if kind == "a" else "Sahara", 36, GREEN if kind == "a" else TAN, weight=BOLD).move_to([x, 2.5, 0])
        return VGroup(frame, scene, name)
    return panel(-3.75, "a"), panel(3.75, "s")


class AmbScene(SpokenScene):
    """SpokenScene plus a slow field of larger drifting motes, so a held frame is never a dead frame."""
    def setup(self):
        super().setup()
        import random
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        motes = VGroup()
        for _ in range(34):
            d = Dot(radius=rng.uniform(0.07, 0.16), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.18, 0.4))
            d.move_to([rng.uniform(-7, 7), rng.uniform(-4, 4), 0])
            d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.45))
            def drift(m):
                pass
            motes.add(d)
        motes.t = 0.0
        def upd(g, dt):
            for m in g:
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 4.1:
                    m.shift(DOWN * 8.2)
                if abs(m.get_x()) > 7.1:
                    m.shift(LEFT * 14.2 * (1 if m.get_x() > 0 else -1))
        motes.add_updater(upd)
        motes.set_z_index(-10)
        self.add(motes)


# ================================================================ scenes

ORANGE = "#FF862F"
CEN = [i + 0.5 for i in range(12)]
A_T = [26.0] * 12
A_R = [140, 120, 150, 180, 200, 160, 140, 110, 90, 100, 130, 160]
B_T = [25, 26, 28, 30, 29, 27, 26, 25, 25, 25, 24, 24]
B_R = [5, 10, 30, 80, 150, 180, 200, 220, 160, 60, 15, 5]
DRY_B = [10, 11, 0, 1, 2]          # Nov, Dec, Jan, Feb, Mar
assert sum(A_R) == 1680 and sum(B_R) == 1115


def G(mm):
    return mm if mm <= 100 else 100 + (mm - 100) / 5.0


class Chart2:
    """Climate diagram; temperature drawn at the 2 x T rain level, rain axis shrinks above 100 mm."""
    def __init__(self, cx, cy, w, h, T_, R_):
        self.cx, self.cy, self.w, self.h, self.T, self.R = cx, cy, w, h, T_, R_

    def X(self, u):
        return self.cx - self.w / 2 + u / 12 * self.w

    def Y(self, g):
        return self.cy - self.h / 2 + g / 130 * self.h

    def tv(self, u, T_=None):
        return float(np.interp(u, CEN, T_ if T_ is not None else self.T))

    def rv(self, u):
        return float(np.interp(u, CEN, self.R))

    def red(self, T_=None, n=97):
        return VMobject().set_points_as_corners([[self.X(u), self.Y(G(2 * self.tv(u, T_))), 0] for u in np.linspace(0, 12, n)]).set_stroke(RED, 7).set_fill(opacity=0)

    def blue(self, n=97):
        return VMobject().set_points_as_corners([[self.X(u), self.Y(G(self.rv(u))), 0] for u in np.linspace(0, 12, n)]).set_stroke(BLUE, 7).set_fill(opacity=0)

    def fill(self, i):
        us = np.linspace(i, i + 1, 13)
        top = [[self.X(u), self.Y(G(2 * self.tv(u))), 0] for u in us]
        bot = [[self.X(u), self.Y(G(self.rv(u))), 0] for u in us][::-1]
        assert all(self.rv(u) <= 2 * self.tv(u) + 1e-6 for u in us), i
        return Polygon(*(top + bot), stroke_width=0, fill_color=GOLD, fill_opacity=0.55)

    def axes(self):
        x0, x1 = self.X(0), self.X(12)
        y0, y1 = self.cy - self.h / 2, self.cy + self.h / 2
        return VGroup(Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3),
                      Line([x0, y0, 0], [x0, y1, 0], color=RED, stroke_width=3),
                      Line([x1, y0, 0], [x1, y1, 0], color=BLUE, stroke_width=3))

    def months(self, size=22):
        return VGroup(*[T(m, size, GREY).move_to([self.X(i + 0.5), self.cy - self.h / 2 - 0.3, 0]) for i, m in enumerate(MONTHS)])

    def ticks(self):
        g = VGroup()
        for t in range(0, 51, 10):
            g.add(T(str(t), 22, RED).move_to([self.X(0) - 0.32, self.Y(2 * t), 0]))
        for r in (0, 50, 100, 200):
            g.add(T(str(r), 22, BLUE).move_to([self.X(12) + 0.38, self.Y(G(r)), 0]))
        return g


CA = Chart2(-3.5, -0.75, 5.2, 3.3, A_T, A_R)
CB = Chart2(3.5, -0.75, 5.2, 3.3, B_T, B_R)
CB_FLAT = [26.0] * 12
NAME_Y, BADGE_Y, SLOT_Y, ROW_Y, NOTE_Y = 2.9, 2.2, 1.45, -3.55, -3.05


def pin_icon(s=0.5):
    return VGroup(Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.4 * s).rotate(PI),
                  Circle(radius=0.4 * s, stroke_width=0, fill_color=YELLOW, fill_opacity=1).shift(UP * 0.5 * s))


def name_tag(ch, text):
    t = lab(text, 28, YELLOW)
    p = pin_icon()
    g = VGroup(p, t).arrange(RIGHT, buff=0.2)
    return g.move_to([ch.cx, NAME_Y, 0])


def rule_line(i, size):
    col, up, txt = [(BLUE, True, "Moist air rises: rain"), (GOLD, False, "Dry air sinks: scarce"), (RED, True, "Warmer: more rain")][i]
    a = Arrow([0, -0.3 if up else 0.3, 0], [0, 0.3 if up else -0.3, 0], color=col, buff=0, stroke_width=size / 4, tip_length=0.22 * size / 22).scale(size / 30)
    return VGroup(a, lab(txt, size, TEXT)).arrange(RIGHT, buff=0.15)


def rule_strip():
    g = VGroup(*[rule_line(i, 22) for i in range(3)]).arrange(RIGHT, buff=0.55)
    return g.move_to([0, 3.45, 0])


def letter_box(ch_txt, x, y, col=TEXT):
    b = RoundedRectangle(corner_radius=0.1, width=0.75, height=0.75, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.12)
    return VGroup(b, lab(ch_txt, 44, col, weight=BOLD).move_to(b)).move_to([x, y, 0])


def badge(text, col=TEXT, size=26):
    return chip(text, col, size=size, pad=0.15)


def canopy(cx, cy, n=6, sc=0.8):
    g = VGroup()
    for i in range(n):
        g.add(tree(cx - 1.1 + i * 0.44, cy - 0.35 + 0.1 * (i % 2), sc))
    return g


def savanna(cx, cy, sc=0.8):
    ln = Line([cx - 1.2, cy - 0.35, 0], [cx + 1.2, cy - 0.35, 0], color=TAN, stroke_width=10)
    g = VGroup(ln)
    for dx in (-0.8, 0.1, 0.9):
        g.add(tree(cx + dx, cy - 0.35, sc * 0.8))
    return g


def full_frame(ch, with_ticks=False):
    g = VGroup(ch.axes(), ch.months())
    if with_ticks:
        g.add(ch.ticks())
    return g


def _dimmed(grp, o):
    t = grp.copy()
    for m in t.family_members_with_points():
        m.set_fill(opacity=m.get_fill_opacity() * o)
        m.set_stroke(opacity=m.get_stroke_opacity() * o)
    return t


def dim_now(grp, o):
    for m in grp.family_members_with_points():
        m.set_fill(opacity=m.get_fill_opacity() * o)
        m.set_stroke(opacity=m.get_stroke_opacity() * o)


def dim_play(scene, grp, o, **kw):
    scene.play(Transform(grp, _dimmed(grp, o)), **kw)


class S00Title(TitleCard):
    LESSON = "Climate, Biomes and Environmental Variation"
    TITLE = "Same Warmth, Two Answers"


class S01Link(AmbScene):
    def construct(self):
        base = base_world(labels=False)
        base.set_opacity(0.6)
        lp = VGroup(loop_path(1), loop_path(-1))
        fd = VGroup(flow_dots(1), flow_dots(-1))
        self.play(FadeIn(base), Create(lp), FadeIn(fd), run_time=1.4)
        self.add(fd)
        self.at("Rain falls")
        band = Band(0.0)
        par = make_parcel(BLUE, 0.4).move_to([0, -2.0, 0])
        gp = [make_parcel(GOLD, 0.35).move_to([s * LX(30), 0.6, 0]) for s in (1, -1)]
        self.add(band.ground, band.cloud, band.rain)
        self.play(FadeIn(par), *[FadeIn(g) for g in gp], run_time=0.5)
        big = [rule_line(i, 36) for i in range(3)]
        card = VGroup(*big).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, 0.2, 0])
        panel = RoundedRectangle(corner_radius=0.2, width=card.width + 0.8, height=card.height + 0.7, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.92).move_to(card)
        self.play(par.animate.move_to([0, 0.9, 0]), *[g.animate.move_to([g.get_center()[0], -1.8, 0]) for g in gp], FadeIn(panel), FadeIn(card[0], shift=RIGHT * 0.2), run_time=1.4)
        self.play(FadeIn(card[1], shift=RIGHT * 0.2), run_time=0.4)
        self.at("and warmer")
        self.play(FadeIn(card[2], shift=RIGHT * 0.2), run_time=0.8)
        self.wait(0.6)
        self.at("humid")
        strip = rule_strip()
        self.play(FadeOut(panel), FadeOut(base), FadeOut(lp), FadeOut(fd), FadeOut(band.cloud), FadeOut(band.rain), FadeOut(band.ground),
                  FadeOut(par), *[FadeOut(g) for g in gp], *[ReplacementTransform(card[i], strip[i]) for i in range(3)], run_time=0.9)
        self.finish()


class S02Question(AmbScene):
    def construct(self):
        strip = rule_strip()
        self.add(strip)
        fa, fb = full_frame(CA), full_frame(CB)
        self.play(Create(fa), Create(fb), run_time=1.3)
        self.at("stations")
        na, nb = name_tag(CA, "station A"), name_tag(CB, "station B (made-up)")
        self.play(FadeIn(na, shift=DOWN * 0.3), FadeIn(nb, shift=DOWN * 0.3), run_time=0.8)
        self.at("Both")
        ra, rb = CA.red(), CB.red(CB_FLAT)
        self.play(Create(ra), Create(rb), run_time=1.6, rate_func=linear)
        la = lab("average about 26 °C", 28, RED).move_to([CA.cx, ROW_Y, 0])
        lb = lab("average about 26 °C", 28, RED).move_to([CB.cx, ROW_Y, 0])
        self.play(FadeIn(la), FadeIn(lb), run_time=0.7)
        self.at("What grows")
        qa = lab("?", 90, YELLOW, weight=BOLD).move_to([CA.cx, SLOT_Y + 0.2, 0])
        qb = lab("?", 90, YELLOW, weight=BOLD).move_to([CB.cx, SLOT_Y + 0.2, 0])
        self.play(GrowFromCenter(qa), GrowFromCenter(qb), run_time=0.8)
        self.play(qa.animate.scale(1.15), qb.animate.scale(1.15), run_time=1.0)
        self.finish()


def carry(scene, upto):
    """Rebuild the film's carried world exactly where it was (frames, names, lines)."""
    strip = rule_strip()
    items = {"strip": strip, "fa": full_frame(CA), "fb": full_frame(CB), "na": name_tag(CA, "station A"), "nb": name_tag(CB, "station B (made-up)")}
    items["ra"], items["rb"] = CA.red(), CB.red(CB_FLAT)
    return items


class S03StationA(AmbScene):
    def construct(self):
        w = carry(self, 3)
        la = lab("average about 26 °C", 28, RED).move_to([CA.cx, ROW_Y, 0])
        lb = lab("average about 26 °C", 28, RED).move_to([CB.cx, ROW_Y, 0])
        qa = lab("?", 90, YELLOW, weight=BOLD).move_to([CA.cx, SLOT_Y + 0.2, 0]).scale(1.15)
        qb = lab("?", 90, YELLOW, weight=BOLD).move_to([CB.cx, SLOT_Y + 0.2, 0]).scale(1.15)
        self.add(*w.values(), la, lb, qa, qb)
        bgrp = VGroup(w["fb"], w["nb"], w["rb"], lb, qb)
        dim_play(self, bgrp, 0.35, run_time=0.9)
        self.play(FadeOut(la), FadeOut(qa), w["na"].animate.scale(1.15), run_time=0.5)
        tk = CA.ticks()
        self.play(FadeIn(tk), run_time=0.8)
        box = SurroundingRectangle(VGroup(w["fa"], tk), color=YELLOW, buff=0.1, stroke_width=3)
        self.play(Create(box), run_time=1.0)
        self.at("blue")
        blue = CA.blue()
        self.play(Create(blue), run_time=3.0, rate_func=linear)
        self.play(w["ra"].animate.set_stroke(width=11), run_time=0.4)
        tot = lab("1,680 mm a year", 28, BLUE).move_to([CA.cx, ROW_Y, 0])
        note = lab("rain axis shrinks above 100", 24, GREY).move_to([CA.cx, NOTE_Y, 0])
        self.play(FadeIn(tot), FadeIn(note), w["ra"].animate.set_stroke(width=7), run_time=0.6)
        self.finish()


class S04Af(AmbScene):
    def construct(self):
        w = carry(self, 4)
        for k in ("ra",):
            w[k].become(CA.red())
        ra = CA.red(); blue = CA.blue(); tk = CA.ticks()
        tot = lab("1,680 mm a year", 28, BLUE).move_to([CA.cx, ROW_Y, 0])
        note = lab("rain axis shrinks above 100", 24, GREY).move_to([CA.cx, NOTE_Y, 0])
        qb = lab("?", 90, YELLOW, weight=BOLD).move_to([CB.cx, SLOT_Y + 0.2, 0]).scale(1.15)
        lb = lab("average about 26 °C", 28, RED).move_to([CB.cx, ROW_Y, 0])
        bgrp = VGroup(w["fb"], w["nb"], w["rb"], lb, qb)
        dim_now(bgrp, 0.35)
        self.add(w["strip"], w["fa"], w["na"], ra, blue, tk, tot, note, bgrp)
        tick = VGroup(Line([-0.35, 0, 0], [-0.1, -0.3, 0], color=GREEN, stroke_width=12), Line([-0.1, -0.3, 0], [0.4, 0.4, 0], color=GREEN, stroke_width=12)).move_to([CA.cx - 1.5, SLOT_Y, 0])
        nd = lab("no dry month", 30, GREEN).move_to([CA.cx + 0.6, SLOT_Y, 0])
        self.play(Create(tick), FadeIn(nd), run_time=1.0)
        self.wait(0.6)
        self.at("class letters")
        self.play(FadeOut(tick), FadeOut(nd), run_time=0.5)
        self.at("A and")
        bA = letter_box("A", CA.cx - 0.5, BADGE_Y)
        self.play(GrowFromCenter(bA), run_time=0.5)
        self.at("F")
        bF = letter_box("f", CA.cx + 0.5, BADGE_Y)
        self.play(GrowFromCenter(bF), run_time=0.5)
        self.at("tropical")
        tA = lab("tropical", 26, TEXT).next_to(bA, DOWN, buff=0.12).shift(LEFT * 0.6)
        self.play(FadeIn(tA), run_time=0.5)
        self.at("no dry")
        tF = lab("no dry month", 26, GOLD).next_to(bF, DOWN, buff=0.12).shift(RIGHT * 0.6 + DOWN * 0.38)
        self.play(FadeIn(tF), run_time=0.6)
        self.wait(0.4)
        self.at("rainforest")
        bd = badge("Af: tropical rainforest", TEXT, 26).move_to([CA.cx, BADGE_Y, 0])
        cano = canopy(CA.cx, SLOT_Y - 0.15, 6, 0.8)
        self.play(ReplacementTransform(VGroup(bA, bF, tA, tF), bd), FadeIn(cano, lag_ratio=0.15), run_time=1.6)
        sway(cano, 0.04, 1.6)
        self.add(cano)
        self.wait(1.0)
        self.finish()


def a_done():
    """Station A, finished, same place (frame, lines, ticks, total, note, badge, canopy)."""
    fa, ra, blue, tk = full_frame(CA), CA.red(), CA.blue(), CA.ticks()
    tot = lab("1,680 mm a year", 28, BLUE).move_to([CA.cx, ROW_Y, 0])
    note = lab("rain axis shrinks above 100", 24, GREY).move_to([CA.cx, NOTE_Y, 0])
    na = name_tag(CA, "station A")
    bd = badge("Af: tropical rainforest", TEXT, 26).move_to([CA.cx, BADGE_Y, 0])
    cano = canopy(CA.cx, SLOT_Y - 0.15, 6, 0.8)
    sway(cano, 0.04, 1.6)
    return VGroup(fa, ra, blue, tk, tot, note, na, bd), cano


class S05StationB(AmbScene):
    def construct(self):
        strip = rule_strip()
        agrp, cano = a_done()
        fb, nb, rb = full_frame(CB), name_tag(CB, "station B (made-up)"), CB.red(CB_FLAT)
        lb = lab("average about 26 °C", 28, RED).move_to([CB.cx, ROW_Y, 0])
        qb = lab("?", 90, YELLOW, weight=BOLD).move_to([CB.cx, SLOT_Y + 0.2, 0]).scale(1.15)
        tot_a = agrp[4]
        self.add(strip, agrp, cano, fb, nb, rb, lb, qb)
        dim = VGroup(*[m for m in agrp if m is not tot_a], cano)
        dim_play(self, dim, 0.4, run_time=0.8)
        self.at("same")
        ra2 = CA.red()
        self.play(Indicate(agrp[1], color=RED, scale_factor=1.0), Indicate(rb, color=RED, scale_factor=1.0), run_time=1.0)
        tkb = CB.ticks()
        self.play(FadeIn(tkb), run_time=0.8)
        self.at("though its months")
        rb2 = CB.red()
        lb2 = lab("24 to 30 °C", 28, RED).move_to([CB.cx, ROW_Y, 0])
        self.play(Transform(rb, rb2), Transform(lb, lb2), run_time=2.6)
        self.wait(0.5)
        self.at("But it gets")
        blue = CB.blue()
        self.play(FadeOut(qb), Create(blue), run_time=2.6, rate_func=linear)
        tot = lab("1,115 mm a year", 28, BLUE).move_to([CB.cx, ROW_Y, 0])
        self.play(ReplacementTransform(lb, tot), run_time=0.6)
        self.play(tot_a.animate.scale(1.08), tot.animate.scale(1.08), run_time=0.5)
        self.at("April")
        x0, x1 = CB.X(3), CB.X(10)
        br = Brace(Line([x0, CB.cy - CB.h / 2 - 0.62, 0], [x1, CB.cy - CB.h / 2 - 0.62, 0]), direction=DOWN, color=BLUE, buff=0.0)
        mshade = Rectangle(width=x1 - x0, height=CB.h, stroke_width=0, fill_color=BLUE, fill_opacity=0.12).move_to([(x0 + x1) / 2, CB.cy, 0])
        self.play(FadeIn(mshade), run_time=0.6)
        self.at("October")
        self.play(Indicate(blue, color=BLUE, scale_factor=1.0), run_time=1.0)
        self.finish()


def b_done(dry=True):
    fb, rb, blue, tk = full_frame(CB), CB.red(), CB.blue(), CB.ticks()
    tot = lab("1,115 mm a year", 28, BLUE).move_to([CB.cx, ROW_Y, 0])
    note = lab("rain axis shrinks above 100", 24, GREY).move_to([CB.cx, NOTE_Y, 0])
    nb = name_tag(CB, "station B (made-up)")
    fills = VGroup(*[CB.fill(i) for i in DRY_B]) if dry else VGroup()
    return VGroup(fb, rb, blue, tk, tot, note, nb), fills


class S06Dry(AmbScene):
    def construct(self):
        strip = rule_strip()
        agrp, cano = a_done()
        bgrp, _ = b_done(False)
        dim = VGroup(*[m for m in agrp if m is not agrp[4]], cano)
        dim_now(dim, 0.4)
        self.add(strip, agrp, cano, bgrp)
        mo = bgrp[0][1]
        self.at("From")
        marks = VGroup()
        for i in [10, 11, 0, 1, 2]:
            r = Rectangle(width=CB.w / 12, height=0.4, stroke_width=0, fill_color=GOLD, fill_opacity=0.6).move_to([CB.X(i + 0.5), CB.cy - CB.h / 2 - 0.3, 0])
            marks.add(r)
            self.play(FadeIn(r), run_time=0.3)
        self.at("drops below")
        cr = [Circle(radius=0.32, color=YELLOW, stroke_width=5).move_to([CB.X(u), CB.Y(G(CB.rv(u))), 0]) for u in (9.72,)]
        self.play(Create(cr[0]), run_time=0.6)
        self.play(FadeOut(cr[0]), run_time=0.3)
        self.at("Those")
        self.play(FadeOut(marks), run_time=0.3)
        cnt = lab("0 dry months", 36, GOLD).move_to([CB.cx, SLOT_Y, 0])
        self.play(FadeIn(cnt), run_time=0.3)
        for k, i in enumerate(DRY_B):
            f = CB.fill(i)
            nt = lab(f"{k+1} dry month" + ("s" if k else ""), 36, GOLD).move_to([CB.cx, SLOT_Y, 0])
            self.play(FadeIn(f), Transform(cnt, nt), run_time=0.45)
            if k == 0:
                fills = VGroup(f)
            else:
                fills.add(f)
        self.at("dry season")
        self.play(Transform(cnt, lab("the dry season", 36, GOLD).move_to([CB.cx, SLOT_Y, 0])), fills.animate.set_fill(GOLD, 0.8), run_time=0.8)
        self.play(fills.animate.set_fill(GOLD, 0.55), run_time=0.8)
        self.finish()


class S07Aw(AmbScene):
    def construct(self):
        strip = rule_strip()
        agrp, cano = a_done()
        bgrp, fills = b_done(True)
        dim_now(VGroup(*[m for m in agrp if m is not agrp[4]], cano), 0.4)
        cnt = lab("the dry season", 36, GOLD).move_to([CB.cx, SLOT_Y, 0])
        self.add(strip, agrp, cano, bgrp, fills, cnt)
        self.at("class letters")
        self.play(FadeOut(cnt), run_time=0.4)
        self.at("A and")
        bA = letter_box("A", CB.cx - 0.5, BADGE_Y)
        self.play(GrowFromCenter(bA), run_time=0.5)
        self.at("W")
        bW = letter_box("w", CB.cx + 0.5, BADGE_Y)
        self.play(GrowFromCenter(bW), run_time=0.5)
        self.at("tropical")
        tA = lab("tropical", 26, TEXT).next_to(bA, DOWN, buff=0.12).shift(LEFT * 0.6)
        self.play(FadeIn(tA), run_time=0.5)
        self.at("marked")
        tW = lab("marked dry season", 26, GOLD).next_to(bW, DOWN, buff=0.12).shift(RIGHT * 0.2 + DOWN * 0.38)
        self.play(FadeIn(tW), run_time=0.6)
        self.wait(0.5)
        self.at("savannah")
        bd = badge("Aw: tropical savanna", TEXT, 26).move_to([CB.cx, BADGE_Y, 0])
        self.play(ReplacementTransform(VGroup(bA, bW, tA, tW), bd), run_time=1.0)
        self.wait(1.0)
        self.at("first guess")
        sv = savanna(CB.cx - 0.5, SLOT_Y - 0.15)
        self.play(FadeIn(sv, lag_ratio=0.2), run_time=1.5)
        sway(VGroup(*sv[1:]), 0.03, 1.4)
        self.add(sv)
        fg = lab("first guess", 24, TAN).move_to([CB.cx + 2.1, SLOT_Y, 0])
        self.play(FadeIn(fg), run_time=0.6)
        self.wait(1.2)
        self.finish()


def both_done():
    strip = rule_strip()
    agrp, cano = a_done()
    bgrp, fills = b_done(True)
    sv = savanna(CB.cx - 0.5, SLOT_Y - 0.15)
    sway(VGroup(*sv[1:]), 0.03, 1.4)
    return strip, agrp, cano, bgrp, fills, sv


class S08Works(AmbScene):
    def construct(self):
        strip, agrp, cano, bgrp, fills, sv = both_done()
        ba = badge("Af: tropical rainforest", TEXT, 26).move_to([CA.cx, BADGE_Y, 0])
        bb = badge("Aw: tropical savanna", TEXT, 26).move_to([CB.cx, BADGE_Y, 0])
        agrp.remove(agrp[7])
        self.add(strip, agrp, cano, bgrp, fills, sv, ba, bb)
        self.at("first guesses")
        ba2 = badge("Af: first guess forest", GREEN, 26).move_to([CA.cx, BADGE_Y, 0])
        bb2 = badge("Aw: first guess savanna", TAN, 26).move_to([CB.cx, BADGE_Y, 0])
        self.play(Transform(ba, ba2), Transform(bb, bb2), run_time=1.0)
        self.at("Similar warmth")
        self.play(Indicate(agrp[1], color=RED, scale_factor=1.0), Indicate(bgrp[1], color=RED, scale_factor=1.0), run_time=1.0)
        self.at("different rain")
        self.play(Indicate(agrp[2], color=BLUE, scale_factor=1.0), Indicate(bgrp[2], color=BLUE, scale_factor=1.0), run_time=1.0)
        self.at("different climate")
        self.play(Indicate(ba, scale_factor=1.15), Indicate(bb, scale_factor=1.15), run_time=1.2)
        self.wait(0.8)
        self.at("station B's")
        dimm = VGroup(agrp, cano, ba, strip)
        dim_play(self, dimm, 0.35, run_time=0.8)
        halo = RoundedRectangle(corner_radius=0.15, width=4.2, height=0.6, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.12).move_to([CB.cx, ROW_Y, 0])
        self.play(bgrp[4].animate.scale(1.3), FadeIn(halo), bgrp[2].animate.set_stroke(width=11), run_time=1.0)
        self.play(halo.animate.set_stroke(opacity=0.4), run_time=0.6)
        self.finish()


def rain_x(mm):
    return -6.0 + mm / 3000.0 * 12.0


AX_Y = -2.6


def rain_axis(skip=()):
    ax = Line([-6, AX_Y, 0], [6, AX_Y, 0], color=BLUE, stroke_width=4)
    g = VGroup(ax)
    for mm in (0, 1000, 2000, 3000):
        g.add(Line([rain_x(mm), AX_Y, 0], [rain_x(mm), AX_Y - 0.12, 0], color=BLUE, stroke_width=3))
        if mm in skip:
            continue
        g.add(lab(f"{mm:,}", 22, BLUE).move_to([rain_x(mm), AX_Y - 0.35, 0]))
    g.add(lab("mm of rain a year", 22, BLUE).move_to([0, AX_Y - 0.8, 0]))
    return g


def window(h=2.0):
    return Rectangle(width=rain_x(2500) - rain_x(1000), height=h, stroke_width=3, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.14).move_to([(rain_x(2500) + rain_x(1000)) / 2, AX_Y + h / 2, 0])


def patches(seed=3):
    import random
    rng = random.Random(seed)
    g = VGroup()
    for i in range(14):
        col = TAN if i in (0, 1, 3, 4, 6, 9, 11) else GREEN
        g.add(Square(side_length=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-4.55 + i * 0.7, 1.7, 0]))
    return g


class S09Staver(AmbScene):
    def construct(self):
        self.at("Staver")
        nm = lab("Staver, Archibald and Levin, 2011", 34, TEXT, font=TITLE_FONT).move_to([0, 3.5, 0])
        self.play(Write(nm), run_time=1.6)
        self.at("tree cover")
        pt = patches()
        self.play(FadeIn(pt, lag_ratio=0.12), run_time=1.6)
        tl = lab("tropics (schematic)", 24, GREY).move_to([0, 0.95, 0])
        self.play(FadeIn(tl), run_time=0.5)
        self.at("They looked")
        ax = rain_axis(skip=(1000,))
        self.play(Create(ax), run_time=1.4)
        self.at("about")
        win = window()
        l1 = lab("1,000", 26, YELLOW, weight=BOLD).move_to([rain_x(1000), AX_Y - 0.35, 0])
        self.add(l1)
        self.play(GrowFromEdge(win, LEFT), run_time=1.9, rate_func=linear)
        self.at("half")
        l2 = lab("2,500", 26, YELLOW, weight=BOLD).move_to([rain_x(2500), AX_Y - 0.35, 0])
        self.play(FadeIn(l2), run_time=0.5)
        self.wait(1.0)
        self.finish()


def hist_bars():
    tan_h = [1.2, 2.2, 2.6, 1.6, 0.6]
    gr_h = [0.6, 1.5, 2.4, 2.6, 1.4]
    g = VGroup()
    base = 0.1
    xs = np.linspace(-4.8, 4.8, 10)
    for i, h in enumerate(tan_h + gr_h):
        col = TAN if i < 5 else GREEN
        g.add(Rectangle(width=0.8, height=max(h, 0.05) * 0.8, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([xs[i], base + h * 0.8 / 2, 0]))
    return g


class S10Bimodal(AmbScene):
    def construct(self):
        nm = lab("Staver, Archibald and Levin, 2011", 34, TEXT, font=TITLE_FONT).move_to([0, 3.5, 0])
        pt = patches()
        tl = lab("tropics (schematic)", 24, GREY).move_to([0, 0.95, 0])
        ax, win = rain_axis(skip=(1000,)), window()
        l1 = lab("1,000", 26, YELLOW, weight=BOLD).move_to([rain_x(1000), AX_Y - 0.35, 0])
        l2 = lab("2,500", 26, YELLOW, weight=BOLD).move_to([rain_x(2500), AX_Y - 0.35, 0])
        self.add(nm, pt, tl, ax, win, l1, l2)
        wx = (rain_x(1000) + rain_x(2500)) / 2
        self.at("dry season")
        d1 = lab("dry season", 28, GOLD).move_to([wx, AX_Y + 1.5, 0])
        self.play(FadeIn(d1), run_time=0.5)
        self.at("seven")
        d2 = lab("shorter than 7 months", 28, GOLD).move_to([wx, AX_Y + 1.05, 0])
        self.play(FadeIn(d2), run_time=0.6)
        self.at("study's")
        d3 = lab("measured the study's way", 22, GREY).move_to([wx, AX_Y + 0.55, 0])
        self.play(FadeIn(d3), run_time=0.6)
        self.wait(0.8)
        self.at("There")
        bars = hist_bars()
        axl = lab("tree cover, low to high", 24, TEXT).move_to([0, -0.2, 0])
        base = Line([-5.4, 0.1, 0], [5.4, 0.1, 0], color=GREY, stroke_width=3)
        sch = lab("schematic of the reported pattern", 22, GREY).move_to([0, 3.05, 0])
        self.play(FadeOut(pt), FadeOut(tl), Create(base), FadeIn(axl), FadeIn(sch), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=1.4)
        self.at("between")
        gap = DashedLine([0, 0.3, 0], [0, 2.1, 0], color=YELLOW, stroke_width=4)
        gl = lab("rarely in between", 28, YELLOW).move_to([0, 2.45, 0])
        self.play(Create(gap), FadeIn(gl), run_time=1.0)
        self.wait(0.8)
        self.at("mostly savannah")
        sl = lab("savanna", 32, TAN, weight=BOLD).move_to([-3.4, 2.6, 0])
        self.play(FadeOut(gl), FadeOut(gap), FadeIn(sl), *[b.animate.set_fill(TAN, 1.0) for b in bars[:5]], run_time=0.9)
        self.at("mostly forest")
        fl = lab("forest", 32, GREEN, weight=BOLD).move_to([3.4, 2.6, 0])
        self.play(FadeIn(fl), *[b.animate.set_fill(GREEN, 1.0) for b in bars[5:]], run_time=0.9)
        self.wait(0.6)
        self.finish()


def b_mini():
    """Station B's diagram, small, for the prediction frame."""
    c = Chart2(-3.9, 1.7, 4.4, 2.2, B_T, B_R)
    g = VGroup(c.axes(), c.months(22), c.red(), c.blue(), *[c.fill(i) for i in DRY_B])
    return c, g


def question_outline():
    o = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=5.0, height=2.6, color=GREY, stroke_width=4)).move_to([3.6, 1.6, 0])
    q = lab("?", 100, YELLOW, weight=BOLD).move_to([3.6, 1.6, 0])
    t = lab("always savanna?", 34, YELLOW).move_to([3.6, 3.3, 0])
    return o, q, t


class S11Predict(AmbScene):
    def construct(self):
        ax, win = rain_axis(), window()
        wx = (rain_x(1000) + rain_x(2500)) / 2 + 0.4
        d1 = lab("dry season", 28, GOLD).move_to([wx, AX_Y + 1.5, 0])
        d2 = lab("shorter than 7 months", 28, GOLD).move_to([wx, AX_Y + 1.05, 0])
        d3 = lab("measured the study's way", 22, GREY).move_to([wx, AX_Y + 0.55, 0])
        bars = hist_bars()
        base = Line([-5.4, 0.1, 0], [5.4, 0.1, 0], color=GREY, stroke_width=3)
        self.add(ax, win, d1, d2, d3, base, bars)
        self.at("Station")
        self.play(FadeOut(bars), FadeOut(base), run_time=0.5)
        pin = pin_icon(0.8).move_to([rain_x(1115), 0.2, 0])
        self.add(pin)
        self.play(pin.animate.move_to([rain_x(1115), AX_Y + 0.55, 0]), run_time=1.2, rate_func=rush_into)
        pl = lab("B: 1,115 mm", 28, YELLOW).move_to([rain_x(1115) - 0.3, AX_Y + 2.35, 0])
        self.play(FadeIn(pl), run_time=0.5)
        self.at("diagram")
        c, g = b_mini()
        bd = badge("Aw: savanna", TAN, 26).move_to([-3.9, 3.3, 0])
        self.play(FadeIn(g, lag_ratio=0.05), run_time=1.5)
        self.play(FadeIn(bd), run_time=0.5)
        self.at("Would")
        o, q, t = question_outline()
        self.play(Create(o), GrowFromCenter(q), FadeIn(t), run_time=1.2)
        self.play(q.animate.scale(1.15), run_time=1.0)
        self.finish()


class S12Pause(AmbScene):
    def construct(self):
        ax, win = rain_axis(), window()
        wx = (rain_x(1000) + rain_x(2500)) / 2 + 0.4
        d1 = lab("dry season", 28, GOLD).move_to([wx, AX_Y + 1.5, 0])
        d2 = lab("shorter than 7 months", 28, GOLD).move_to([wx, AX_Y + 1.05, 0])
        d3 = lab("measured the study's way", 22, GREY).move_to([wx, AX_Y + 0.55, 0])
        pin = pin_icon(0.8).move_to([rain_x(1115), AX_Y + 0.55, 0])
        pl = lab("B: 1,115 mm", 28, YELLOW).move_to([rain_x(1115) - 0.3, AX_Y + 2.35, 0])
        c, g = b_mini()
        bd = badge("Aw: savanna", TAN, 26).move_to([-3.9, 3.3, 0])
        o, q, t = question_outline()
        q.scale(1.15)
        self.add(ax, win, d1, d2, d3, pin, pl, g, bd, o, q, t)
        ring_bg = Circle(radius=0.45, color=GREY, stroke_width=4).move_to([-0.25, 1.6, 0])
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=PI / 2, angle=-2 * PI * max(tr.get_value(), 0.002), color=YELLOW, stroke_width=7, arc_center=[-0.25, 1.6, 0]))
        self.add(ring_bg, ring)
        self.play(tr.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


PL_X, PR_X, PY = -3.4, 3.4, 0.2


def patch_frames():
    fl = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.4, stroke_color=TAN, stroke_width=3, fill_color=TAN, fill_opacity=0.08).move_to([PL_X, PY, 0])
    fr = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.4, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.08).move_to([PR_X, PY, 0])
    return fl, fr


def big_savanna():
    g = VGroup(Line([PL_X - 2.4, PY - 1.0, 0], [PL_X + 2.4, PY - 1.0, 0], color=TAN, stroke_width=14))
    for k in range(10):
        g.add(Line([PL_X - 2.2 + k * 0.48, PY - 0.95, 0], [PL_X - 2.1 + k * 0.48, PY - 0.55, 0], color=TAN, stroke_width=4))
    for dx in (-1.6, 0.2, 1.7):
        g.add(tree(PL_X + dx, PY - 0.95, 1.3))
    return g


def big_canopy():
    g = VGroup()
    for j in range(2):
        for i in range(8):
            g.add(tree(PR_X - 2.3 + i * 0.66 + 0.3 * j, PY - 1.0 + j * 0.5, 1.2))
    return g


def summary_card():
    return chip("similar rain total and season", TEXT, 30).move_to([0, 3.25, 0])


class S13Reveal(AmbScene):
    def construct(self):
        ax, win = rain_axis(), window()
        wx = (rain_x(1000) + rain_x(2500)) / 2 + 0.4
        d1 = lab("dry season", 28, GOLD).move_to([wx, AX_Y + 1.5, 0])
        d2 = lab("shorter than 7 months", 28, GOLD).move_to([wx, AX_Y + 1.05, 0])
        d3 = lab("measured the study's way", 22, GREY).move_to([wx, AX_Y + 0.55, 0])
        pin = pin_icon(0.8).move_to([rain_x(1115), AX_Y + 0.55, 0])
        pl = lab("B: 1,115 mm", 28, YELLOW).move_to([rain_x(1115) - 0.3, AX_Y + 2.35, 0])
        c, g = b_mini()
        bd = badge("Aw: savanna", TAN, 26).move_to([-3.9, 3.3, 0])
        o, q, t = question_outline()
        q.scale(1.15)
        self.add(ax, win, d1, d2, d3, pin, pl, g, bd, o, q, t)
        self.at("Now")
        fl, fr = patch_frames()
        self.play(FadeOut(VGroup(ax, win, d1, d2, d3, pin, pl, g, bd, q, t)), ReplacementTransform(o, VGroup(fl, fr)), run_time=1.6)
        self.at("window")
        sc = summary_card()
        self.play(FadeIn(sc, shift=DOWN * 0.2), run_time=0.8)
        self.at("savannah")
        sv = big_savanna()
        names = [lab("savanna", 30, TAN, weight=BOLD).move_to([PL_X, 2.35, 0]), lab("forest", 30, GREEN, weight=BOLD).move_to([PR_X, 2.35, 0])]
        self.play(FadeIn(sv, lag_ratio=0.1), FadeIn(names[0]), run_time=1.0)
        sway(VGroup(*sv[11:]), 0.04, 1.4)
        self.add(sv)
        self.at("forest")
        cn = big_canopy()
        self.play(FadeIn(cn, lag_ratio=0.05), FadeIn(names[1]), run_time=1.0)
        sway(cn, 0.04, 1.6)
        self.add(cn)
        self.at("similar climates")
        lb = lab("similar climates, two states", 32, YELLOW).move_to([0, -2.2, 0])
        lb2 = lab("(observed across the tropics)", 22, GREY).move_to([0, -2.75, 0])
        self.play(FadeIn(lb), FadeIn(lb2), run_time=0.8)
        self.at("fire was")
        fi = drop_icon(ORANGE, 1.4).move_to([PL_X - 1.8, PY - 0.2, 0])
        fl_ = lab("fire", 32, ORANGE, weight=BOLD).move_to([fi.get_x(), PY + 1.2, 0])
        self.play(FadeIn(fi, shift=UP * 0.2), FadeIn(fl_), run_time=0.8)
        self.at("open")
        self.play(Indicate(sv[0], color=ORANGE, scale_factor=1.0), run_time=1.2)
        self.finish()


def static_patches():
    fl, fr = patch_frames()
    sv, cn = big_savanna(), big_canopy()
    sway(VGroup(*sv[11:]), 0.04, 1.4)
    sway(cn, 0.04, 1.6)
    names = VGroup(lab("savanna", 30, TAN, weight=BOLD).move_to([PL_X, 2.35, 0]), lab("forest", 30, GREEN, weight=BOLD).move_to([PR_X, 2.35, 0]))
    return fl, fr, sv, cn, names


def fire_line(x, n=5):
    return VGroup(*[drop_icon(ORANGE, 1.1).move_to([x, PY - 1.1 + i * 0.55, 0]) for i in range(n)])


class S14Fire(AmbScene):
    def construct(self):
        fl, fr, sv, cn, names = static_patches()
        sc = summary_card()
        self.add(fl, fr, sv, cn, names, sc)
        self.at("Where")
        dm = lab("dry month", 26, GOLD).move_to([PL_X + 1.8, 2.35, 0])
        self.play(FadeIn(dm), run_time=0.5)
        self.at("fire can")
        f1 = fire_line(PL_X - 2.6)
        t1 = lab("fire can keep open areas open", 24, ORANGE).move_to([PL_X, -2.2, 0])
        self.play(FadeIn(f1), FadeIn(t1), run_time=0.5)
        self.play(f1.animate.shift(RIGHT * 5.2), run_time=1.8, rate_func=linear)
        self.play(FadeOut(f1), run_time=0.3)
        self.at("A closed")
        f2 = fire_line(PR_X - 2.9)
        t2 = lab("a closed canopy can hold fire back", 24, GREEN).move_to([PR_X, -2.2, 0])
        self.play(FadeIn(f2), FadeIn(t2), run_time=0.5)
        self.play(f2.animate.shift(RIGHT * 0.9).set_opacity(0.0), run_time=1.5, rate_func=linear)
        self.wait(0.4)
        sch = lab("schematic; strength varies from place to place", 22, GREY).move_to([0, -2.85, 0])
        self.play(FadeIn(sch), run_time=0.5)
        self.at("each state")
        ca = Arc(radius=0.5, start_angle=PI * 0.3, angle=PI * 1.6, color=TAN, stroke_width=6).move_to([PL_X, 1.1, 0]).add_tip(tip_length=0.2)
        cb = Arc(radius=0.5, start_angle=PI * 0.3, angle=PI * 1.6, color=GREEN, stroke_width=6).move_to([PR_X, 1.1, 0]).add_tip(tip_length=0.2)
        self.play(Create(ca), Create(cb), run_time=1.4)
        self.play(Rotate(ca, -PI, about_point=ca.get_center()), Rotate(cb, -PI, about_point=cb.get_center()), run_time=2.5, rate_func=linear)
        self.finish()


def well(x):
    return -1.1 + 1.6 * ((x / 3.3) ** 2 - 1) ** 2


class S15Hedge(AmbScene):
    def construct(self):
        fl, fr, sv, cn, names = static_patches()
        sc = summary_card()
        self.add(fl, fr, sv, cn, names, sc)
        self.at("This")
        cap = lab("association, not proven cause", 36, YELLOW, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeOut(sc), FadeIn(cap), run_time=0.8)
        self.wait(1.2)
        self.at("Savannah")
        sv_s, cn_s = sv.copy(), cn.copy()
        sv_s.clear_updaters(); cn_s.clear_updaters()
        for m in list(sv_s) + list(cn_s):
            m.clear_updaters()
        self.remove(sv, cn)
        self.add(sv_s, cn_s)
        curve = VMobject().set_points_smoothly([[x, well(x), 0] for x in np.linspace(-4.8, 4.8, 41)]).set_stroke(TEXT, 6)
        self.play(FadeOut(fl), FadeOut(fr), FadeOut(names),
                  sv_s.animate.scale(0.45).move_to([-3.3, -2.35, 0]), cn_s.animate.scale(0.45).move_to([3.3, -2.35, 0]), run_time=1.4)
        self.play(Create(curve), run_time=1.6)
        balls = [Dot([s * 3.3, well(3.3) + 0.2, 0], radius=0.2, color=c) for s, c in ((-1, TAN), (1, GREEN))]
        for b in balls:
            b.shift(UP * 1.5)
        self.play(*[b.animate.shift(DOWN * 1.5) for b in balls], run_time=0.9, rate_func=rush_into)
        nl = [lab("savanna", 28, TAN).move_to([-3.3, -1.35, 0]), lab("forest", 28, GREEN).move_to([3.3, -1.35, 0])]
        self.play(*[FadeIn(n) for n in nl], run_time=0.5)
        self.at("Whether")
        qh = lab("?", 70, YELLOW, weight=BOLD).move_to([0, 1.1, 0])
        st = lab("stable? still debated", 30, YELLOW).move_to([0, 2.15, 0])
        self.play(GrowFromCenter(qh), FadeIn(st), run_time=0.8)
        for _ in range(2):
            self.play(balls[0].animate.shift(LEFT * 0.25 + UP * 0.06), balls[1].animate.shift(RIGHT * 0.25 + UP * 0.06), run_time=0.5, rate_func=there_and_back)
        self.wait(0.6)
        self.finish()


class S16Close(AmbScene):
    def construct(self):
        strip = rule_strip()
        self.add(strip)
        self.at("So climate")
        agrp, cano = a_done()
        bgrp, fills = b_done(True)
        sv = savanna(CB.cx - 0.5, SLOT_Y - 0.15)
        sway(VGroup(*sv[1:]), 0.03, 1.4)
        agrp.remove(agrp[7]); agrp.remove(agrp[6]); bgrp.remove(bgrp[6])
        self.play(FadeIn(agrp), FadeIn(bgrp), FadeIn(fills), FadeIn(cano), FadeIn(sv), run_time=1.4)
        self.add(cano, sv)
        fa = lab("first guess: forest", 26, GREEN).move_to([CA.cx, BADGE_Y, 0])
        fb = lab("first guess: savanna", 26, TAN).move_to([CB.cx, BADGE_Y, 0])
        self.play(FadeIn(fa), FadeIn(fb), run_time=0.8)
        self.at("Fire")
        tags = [chip("fire", ORANGE, 28), chip("soils", TAN, 28), chip("rain timing", BLUE, 28), chip("microclimate", GREEN, 28)]
        row = VGroup(*tags).arrange(RIGHT, buff=0.35).move_to([0, 2.65, 0])
        self.play(FadeOut(fa), FadeOut(fb), run_time=0.3)
        self.at("Fire")
        self.play(FadeIn(tags[0], shift=DOWN * 0.2), run_time=0.5)
        self.at("soils")
        self.play(FadeIn(tags[1], shift=DOWN * 0.2), run_time=0.5)
        self.at("timing")
        self.play(FadeIn(tags[2], shift=DOWN * 0.2), run_time=0.5)
        self.at("microclimate")
        self.play(FadeIn(tags[3], shift=DOWN * 0.2), run_time=0.5)
        self.wait(0.8)
        self.at("savannah climate")
        cn2 = canopy(CB.cx + 1.1, SLOT_Y - 0.15, 3, 0.8)
        self.play(sv.animate.scale(0.6).move_to([CB.cx - 1.2, SLOT_Y + 0.05, 0]), FadeIn(cn2, lag_ratio=0.2), run_time=1.4)
        sway(cn2, 0.04, 1.6)
        self.add(cn2)
        q = lab("?", 60, YELLOW, weight=BOLD).move_to([CB.cx, SLOT_Y + 0.05, 0])
        self.play(GrowFromCenter(q), run_time=0.6)
        self.play(q.animate.scale(1.15), run_time=1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Climate gives a first guess at a biome, not the answer."
