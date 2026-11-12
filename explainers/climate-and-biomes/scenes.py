"""Where the Rain Falls (climate-and-biomes film 1).  Timed to the spoken words via self.at().

COLOR MAP (one colour per concept, whole film)
  RED    = monthly temperature (line, thermometer)      BLUE  = monthly rain, moist air, rain
  GOLD   = a dry month, dry sinking air                 YELLOW = sunlight
  GREEN  = forest / the rain belt on the ground         TAN   = desert
  Globes, parcels, trees are schematic cartoons; sunlight bars and the climate-diagram
  lines are computed (sun-angle geometry, Walter-Lieth rule: dry when rain (mm) < 2 x temperature (C)).
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


# ---------------------------------------------------------------- climate-diagram data (schematic town)
def Tfun(u):
    return 26 - 2.0 * math.cos(2 * math.pi * (u - 7.0) / 12)


def Rfun(u):
    return 8 + 64 * math.exp(-((u - 7.0) / 2.4) ** 2)


WET_MONTHS = [Rfun(i + 0.5) > 2 * Tfun(i + 0.5) for i in range(12)]


class Chart:
    def __init__(self, cx, cy, w, h, tf=Tfun, rf=Rfun, tr=None):
        self.cx, self.cy, self.w, self.h, self.tf, self.rf = cx, cy, w, h, tf, rf
        self.tr = tr if tr is not None else ValueTracker(0)

    def X(self, u):
        return self.cx - self.w / 2 + u / 12 * self.w

    def YT(self, t):
        return self.cy - self.h / 2 + t / 40 * self.h

    def YR(self, r):
        return self.cy - self.h / 2 + r / 80 * self.h

    def pts(self, fn, ymap, n=56, add=0.0):
        return [[self.X(u), ymap(fn(u) + add), 0] for u in np.linspace(0.5, 11.5, n)]

    def red(self):
        return VMobject().set_points_as_corners(self.pts(self.tf, self.YT, add=self.tr.get_value())).set_stroke(RED, 7)

    def blue(self):
        return VMobject().set_points_as_corners(self.pts(self.rf, self.YR)).set_stroke(BLUE, 7)

    def fills(self):
        us = np.linspace(0.5, 11.5, 111)
        add = self.tr.get_value()
        out = VGroup()
        run = []
        def flush():
            if len(run) > 1:
                top = [[self.X(u), self.YT(self.tf(u) + add), 0] for u in run]
                bot = [[self.X(u), self.YR(self.rf(u)), 0] for u in run][::-1]
                out.add(Polygon(*(top + bot), stroke_width=0, fill_color=GOLD, fill_opacity=0.5))
        for u in us:
            if self.rf(u) < 2 * (self.tf(u) + add):
                run.append(u)
            else:
                flush()
                run.clear()
        flush()
        return out

    def axes(self):
        x0, x1 = self.X(0), self.X(12)
        y0, y1 = self.cy - self.h / 2, self.cy + self.h / 2
        return VGroup(Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3),
                      Line([x0, y0, 0], [x0, y1, 0], color=RED, stroke_width=3),
                      Line([x1, y0, 0], [x1, y1, 0], color=BLUE, stroke_width=3))

    def months(self, size=26):
        return VGroup(*[T(m, size, GREY).move_to([self.X(i + 0.5), self.cy - self.h / 2 - 0.38, 0]) for i, m in enumerate(MONTHS)])

    def ticks(self):
        g = VGroup()
        for t in range(0, 41, 10):
            g.add(T(str(t), 24, RED).move_to([self.X(0) - 0.45, self.YT(t), 0]))
        for r in range(0, 81, 20):
            g.add(T(str(r), 24, BLUE).move_to([self.X(12) + 0.45, self.YR(r), 0]))
        return g


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
class S00Title(TitleCard):
    LESSON = "Climate, Biomes and Environmental Variation"
    TITLE = "Where the Rain Falls"


class S01Question(AmbScene):
    def construct(self):
        pa, ps = panel_pair()
        self.play(FadeIn(pa[0]), FadeIn(ps[0]), FadeIn(pa[1], lag_ratio=0.05), FadeIn(ps[1], lag_ratio=0.1), run_time=self.beat(0.1))
        sway(pa[1], 0.04, 1.6)
        self.add(pa[1])
        self.at("Amazon")
        self.play(FadeIn(pa[2]), run_time=0.4)
        self.at("Sahara")
        self.play(FadeIn(ps[2]), run_time=0.4)
        th = therm_glyph([-3.75, 0.6, 0], 0.15, 1.6)
        self.play(FadeIn(th), run_time=0.4)
        self.at("hot")
        th2 = therm_glyph([-3.75, 0.6, 0], 0.9, 1.6)
        self.play(Transform(th, th2), run_time=0.9)
        th_r = th.copy()
        self.play(th_r.animate.move_to([3.75, 0.6, 0]), run_time=1.0)
        q = lab("?", 140, YELLOW, weight=BOLD).move_to([0, 0.2, 0])
        self.at("So why")
        self.play(GrowFromCenter(q), run_time=0.9)
        self.at("rainforest")
        self.play(pa[0].animate.set_stroke(GREEN, 8), run_time=0.5)
        self.at("desert")
        self.play(ps[0].animate.set_stroke(TAN, 8), run_time=0.5)
        self.play(q.animate.scale(1.15), run_time=0.8)
        self.finish()


class S02Biome(AmbScene):
    def construct(self):
        self.at("biome")
        word = lab("biome", 72, TEXT, font=TITLE_FONT).move_to([0, 2.7, 0])
        self.play(Write(word), run_time=0.9)
        self.at("a large region")
        d1 = lab("a large region with", 40).move_to([0, 1.5, 0])
        d2 = lab("similar climate and similar", 40).move_to([0, 0.9, 0])
        d3 = lab("plants and animals", 40).move_to([0, 0.35, 0])
        self.play(FadeIn(d1, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(d2, shift=UP * 0.1), run_time=0.6)
        self.at("plants and animals")
        self.play(FadeIn(d3, shift=UP * 0.1), run_time=0.6)
        names = ["Tropical\nforest", "Savanna", "Desert", "Temperate\ngrassland", "Boreal\nforest", "Tundra"]
        cols = [GREEN, "#B7C45A", TAN, "#9CCB6B", "#3E8E6B", "#9FC9D6"]
        icons = VGroup()
        for i, (nm, c) in enumerate(zip(names, cols)):
            x = -5.3 + i * 2.12
            box = RoundedRectangle(corner_radius=0.15, width=1.95, height=2.1, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.18)
            pic = tree(0, -0.55, 0.9, c) if i in (0, 4) else (Circle(radius=0.3, fill_color=c, fill_opacity=0.9, stroke_width=0).move_to([0, 0.0, 0]) if i == 5 else Line([-0.6, -0.3, 0], [0.6, -0.3, 0], color=c, stroke_width=8))
            if i == 1:
                pic = VGroup(tree(-0.35, -0.55, 0.7, c), Line([-0.7, -0.55, 0], [0.7, -0.55, 0], color=c, stroke_width=5))
            if i == 2:
                pic = VMobject().set_points_smoothly([[t, 0.25 * math.sin(2.2 * t) - 0.2, 0] for t in np.linspace(-0.7, 0.7, 12)]).set_stroke(c, 7)
            if i == 3:
                pic = VGroup(*[Line([-0.6 + k * 0.3, -0.5, 0], [-0.55 + k * 0.3, 0.1 + 0.1 * (k % 2), 0], color=c, stroke_width=5) for k in range(5)])
            pic.scale(1.5).move_to(box.get_center() + UP * 0.05)
            g = VGroup(box, pic)
            l = lab(nm, 24, c).next_to(g, DOWN, buff=0.12)
            icons.add(VGroup(g, l).move_to([x, -2.0, 0]))
        for ic in icons:
            self.play(FadeIn(ic, shift=UP * 0.2, scale=0.8), run_time=0.35)
        sway(VGroup(*[ic[0] for ic in icons]), 0.05, 1.5)
        self.add(*[ic[0] for ic in icons])
        self.at("To guess")
        self.wait(0.2)
        self.at("ask two things")
        self.play(FadeOut(d1), FadeOut(d2), FadeOut(d3), FadeOut(icons), word.animate.move_to([0, 3.0, 0]).scale(0.7), run_time=0.8)
        wbox = RoundedRectangle(corner_radius=0.2, width=4.8, height=4.0, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.06).move_to([-3.3, -0.1, 0])
        dbox = RoundedRectangle(corner_radius=0.2, width=4.8, height=4.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.06).move_to([3.3, -0.1, 0])
        th = therm_glyph([-3.3, 0.2, 0], 0.0, 2.4)
        dr = drop_icon(BLUE, 3.0).move_to([3.3, 0.2, 0])
        dr_out = drop_icon(BLUE, 3.0).set_fill(opacity=0).set_stroke(BLUE, 4).move_to(dr)
        self.at("of every month")
        self.play(Create(wbox), Create(dbox), FadeIn(th), FadeIn(dr_out), run_time=0.8)
        wl = lab("warmth", 34, RED).next_to(wbox, DOWN, buff=-0.7)
        dl = lab("water", 34, BLUE).next_to(dbox, DOWN, buff=-0.7)
        em = lab("each month", 30, GREY).move_to([0, -3.35, 0])
        self.play(FadeIn(wl), FadeIn(dl), FadeIn(em), run_time=0.5)
        self.at("How warm")
        self.play(Transform(th, therm_glyph([-3.3, 0.2, 0], 0.85, 2.4)), run_time=1.0)
        self.at("How wet")
        self.play(FadeIn(dr), run_time=0.8)
        self.play(dr.animate.scale(1.12), run_time=0.5)
        self.finish()


class S03Torch(AmbScene):
    def construct(self):
        piv = np.array([-2.5, 2.2, 0.0])
        table_y = -2.7
        ang = ValueTracker(0.0)
        HALF = math.radians(12)
        H = piv[1] - table_y

        def hit(a):
            return piv[0] + H * math.tan(a)

        table = Rectangle(width=13, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, table_y - 0.25, 0])
        tlab = lab("table", 28, GREY).move_to([5.6, table_y - 0.25, 0])
        def mk_torch():
            return VGroup(RoundedRectangle(corner_radius=0.15, width=1.0, height=1.9, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.55),
                          Rectangle(width=1.1, height=0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=1).shift(DOWN * 1.0))
        torch = mk_torch().move_to(piv + UP * 0.95)
        torch.add_updater(lambda m: m.become(mk_torch().rotate(-ang.get_value(), about_point=ORIGIN).move_to(piv + np.array([math.sin(ang.get_value()), math.cos(ang.get_value()), 0]) * 0.95)))
        self.play(FadeIn(table), FadeIn(torch), FadeIn(tlab), run_time=self.beat(0.07))
        self.add(torch)
        beam_on = ValueTracker(0)

        def beam():
            a = ang.get_value()
            x1, x2 = hit(a - HALF), hit(a + HALF)
            pts = [piv, [x1, table_y, 0], [x2, table_y, 0]]
            op = beam_on.get_value()
            return Polygon(*pts, stroke_width=0, fill_color=YELLOW, fill_opacity=0.18 * op)

        def spot():
            a = ang.get_value()
            x1, x2 = hit(a - HALF), hit(a + HALF)
            w = x2 - x1
            e = Ellipse(width=w, height=0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=min(1.0, 0.95 * 1.0 / (w / 1.05) ** 1.0) * beam_on.get_value())
            return e.move_to([(x1 + x2) / 2, table_y + 0.12, 0])

        offs = [-HALF * 0.8, -HALF * 0.4, 0, HALF * 0.4, HALF * 0.8]

        def rays():
            a = ang.get_value()
            g = VGroup()
            for o in offs:
                x = hit(a + o)
                g.add(Line(piv, [x, table_y, 0], color=YELLOW, stroke_width=2.5, stroke_opacity=0.7 * beam_on.get_value()))
                g.add(Dot([x, table_y + 0.05, 0], radius=0.07, color=YELLOW, fill_opacity=beam_on.get_value()))
            return g

        b, s, r = always_redraw(beam), always_redraw(spot), always_redraw(rays)
        self.add(b, s, r)
        # moving dots along the rays (light travelling)
        flow = VGroup(*[Dot(radius=0.06, color=YELLOW) for _ in range(15)])
        flow.t = 0.0

        def fupd(m, dt):
            m.t += dt
            a = ang.get_value()
            for i, d in enumerate(m):
                o = offs[i % 5]
                tgt = np.array([hit(a + o), table_y, 0])
                ph = ((i // 5) / 3 + m.t * 0.5) % 1
                d.move_to(piv + (tgt - piv) * ph)
                d.set_opacity(beam_on.get_value())
        flow.add_updater(fupd)
        self.add(flow)
        self.at("Shine a torch")
        self.play(beam_on.animate.set_value(1), run_time=1.0)
        self.at("small bright spot")
        l1 = lab("small, bright", 32, YELLOW, halo=True).move_to([0.6, -1.9, 0])
        self.play(FadeIn(l1), run_time=0.5)
        self.at("Tilt it")
        self.play(FadeOut(l1), run_time=0.3)
        self.play(ang.animate.set_value(math.radians(38)), run_time=0.9, rate_func=smooth)
        self.at("same light")
        l0 = lab("same five rays", 30, TEXT, halo=True).move_to([-3.6, 0.9, 0])
        self.play(FadeIn(l0), run_time=0.4)
        self.at("larger dimmer oval")
        l2 = lab("larger, dimmer", 32, YELLOW, halo=True).move_to([4.4, -1.9, 0])
        self.play(FadeIn(l2), run_time=0.5)
        self.play(ang.animate.set_value(math.radians(42)), run_time=1.5)
        self.finish()


class S04Globe(AmbScene):
    def construct(self):
        C = np.array([-2.7, 0.0, 0.0])
        R = 3.0
        globe = Circle(radius=R, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.18).move_to(C)
        axis = Line(C + UP * (R + 0.3), C + DOWN * (R + 0.3), color=GREY, stroke_width=2)
        schem = lab("schematic", 22, GREY).move_to(C + DOWN * (R + 0.45))
        ys = np.linspace(-2.7, 2.7, 10)
        rays = VGroup(*[Line([-6.7, y, 0], [C[0] - math.sqrt(R * R - y * y), y, 0], color=YELLOW, stroke_width=3, stroke_opacity=0.55) for y in ys])
        sun = lab("Sun", 26, YELLOW).move_to([-6.1, 3.35, 0])
        flow = VGroup(*[Dot(radius=0.06, color=YELLOW) for _ in range(30)])
        flow.t = 0.0

        def fup(m, dt):
            m.t += dt
            for i, d in enumerate(m):
                y = ys[i % 10]
                xe = C[0] - math.sqrt(R * R - y * y)
                ph = ((i // 10) / 3 + m.t * 0.35) % 1
                d.move_to([-6.7 + (xe + 6.7) * ph, y, 0])
        flow.add_updater(fup)
        self.at("Sunlight does the same")
        self.play(FadeIn(globe), FadeIn(axis), FadeIn(schem), run_time=0.8)
        self.play(FadeIn(rays), FadeIn(sun), run_time=0.8)
        self.add(flow)

        def patch(lat1, lat2, op, name_y):
            a1, a2 = math.radians(lat1), math.radians(lat2)
            return Arc(radius=R, start_angle=math.pi - a2, angle=a2 - a1, arc_center=C, color=YELLOW, stroke_width=12, stroke_opacity=op)
        # one band of rays (height 0.6) falling on three latitudes
        bands = [(0.0, 0.95), (1.5, 0.65), (2.6, 0.35)]
        p = []
        for yc, op in bands:
            y1, y2 = yc - 0.3, yc + 0.3
            p.append(patch(math.degrees(math.asin(y1 / R)), math.degrees(math.asin(y2 / R)), op, yc))
        pm = [patch(-math.degrees(math.asin(0.3 / R)), math.degrees(math.asin(0.3 / R)), 0.95, 0)]
        self.at("Averaged over a year")
        self.wait(0.3)
        self.at("strikes the equator")
        eq = Arc(radius=R, start_angle=math.pi - math.asin(0.3 / R), angle=2 * math.asin(0.3 / R), arc_center=C, color=YELLOW, stroke_width=14)
        eqb = Rectangle(width=C[0] - math.sqrt(R * R - 0.09) + 6.7, height=0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.35).move_to([(-6.7 + C[0] - math.sqrt(R * R - 0.09)) / 2, 0, 0])
        self.play(FadeIn(eqb), Create(eq), run_time=0.9)
        self.at("poles at a slant")
        y1, y2 = 2.3, 2.9
        a1, a2 = math.asin(y1 / R), math.asin(y2 / R)
        hi = Arc(radius=R, start_angle=math.pi - a2, angle=a2 - a1, arc_center=C, color=YELLOW, stroke_width=14, stroke_opacity=0.5)
        hib = Rectangle(width=C[0] - math.sqrt(R * R - 2.6 ** 2) + 6.7, height=0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.25).move_to([(-6.7 + C[0] - math.sqrt(R * R - 2.6 ** 2)) / 2, 2.6, 0])
        self.play(FadeIn(hib), Create(hi), run_time=0.9)
        # chart
        vals = [("Equator", 415), ("30°N", 365), ("60°N", 236), ("Pole", 172)]
        base_y = -2.5
        xs = [1.95, 3.2, 4.45, 5.7]
        title = lab("Sunlight, W per m²\n(yearly average, computed)", 24, TEXT).move_to([4.0, 2.55, 0])
        axis_l = Line([1.2, base_y, 0], [6.4, base_y, 0], color=GREY, stroke_width=3)
        self.at("So the tropics")
        self.play(FadeIn(title), Create(axis_l), run_time=0.5)

        def bar(i):
            nm, v = vals[i]
            h = 4.0 * v / 415
            b = Rectangle(width=0.85, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95 - 0.12 * i).move_to([xs[i], base_y + h / 2, 0])
            vl = M(str(v), 24, TEXT).next_to(b, UP, buff=0.08)
            nl = lab(nm, 22, TEXT).move_to([xs[i], base_y - 0.3, 0])
            return b, vl, nl
        b0 = bar(0)
        self.play(GrowFromEdge(b0[0], DOWN), FadeIn(b0[2]), run_time=1.0)
        self.play(FadeIn(b0[1]), run_time=0.3)
        self.at("square meter")
        b1 = bar(1)
        self.play(GrowFromEdge(b1[0], DOWN), FadeIn(b1[2]), run_time=0.8)
        self.play(FadeIn(b1[1]), run_time=0.3)
        self.at("the poles the least")
        b2, b3 = bar(2), bar(3)
        self.play(GrowFromEdge(b2[0], DOWN), GrowFromEdge(b3[0], DOWN), FadeIn(b2[2]), FadeIn(b3[2]), run_time=1.0)
        self.play(FadeIn(b2[1]), FadeIn(b3[1]), run_time=0.3)
        self.finish()


class S05Water(AmbScene):
    def construct(self):
        pa, ps = panel_pair()
        sway(pa[1], 0.04, 1.6)
        self.add(pa[0], ps[0], ps[1], pa[1], pa[2], ps[2])
        t1 = therm_glyph([-3.75, 0.6, 0], 0.9, 1.6)
        t2 = therm_glyph([3.75, 0.6, 0], 0.9, 1.6)
        self.at("But the Amazon")
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)
        eq = lab("similar\nwarmth", 30, RED, halo=True).move_to([0, 0.9, 0])
        self.play(FadeIn(eq), run_time=0.5)
        self.play(eq.animate.shift(UP * 0.1), run_time=2.0)
        self.at("What differs")
        d1 = drop_icon(BLUE, 2.6).move_to([-3.75, 0.6, 0])
        d2 = drop_icon(BLUE, 2.6).move_to([3.75, 0.6, 0])
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(eq), FadeIn(d1), FadeIn(d2), run_time=0.7)
        self.play(d1.animate.scale(1.2), run_time=0.4)
        self.play(d1.animate.scale(1 / 1.2), run_time=0.4)
        cross = VGroup(Line([3.2, 0.1, 0], [4.3, 1.1, 0], color=RED, stroke_width=10), Line([3.2, 1.1, 0], [4.3, 0.1, 0], color=RED, stroke_width=10))
        self.play(Create(cross), run_time=0.5)
        self.at("moving air")
        lp = loop_fn(1)
        dots = VGroup(*[Dot(radius=0.09, color=TEXT) for _ in range(12)])
        dots.t = 0.0

        def up(m, dt):
            m.t += dt
            for i, d in enumerate(m):
                ph = (i / 12 + m.t * 0.2) % 1
                p = lp(ph)
                d.move_to([p[0] * 0.55 - 0.9 + 0.9 * 0, p[1] * 0.9 + 0.0, 0])
        dots.add_updater(up)
        self.add(dots)
        self.play(FadeIn(dots), run_time=0.6)
        self.wait(1.5)
        self.finish()


def world_with_band(bx=0.0, tan=False, loops=False):
    base = base_world()
    band = Band(bx)
    return base, band


class S06Rise(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.0, ground_color=RED)
        band.ground.set_fill(opacity=0.45)
        self.at("Over the warm equator")
        self.play(FadeIn(base), FadeIn(band.ground), run_time=0.8)
        warm = lab("warm", 32, RED).move_to([2.3, -2.0, 0])
        self.play(FadeIn(warm), run_time=0.4)
        self.at("moist air")
        pc = make_parcel(BLUE, 0.45).move_to([0, -2.0, 0])
        self.play(GrowFromCenter(pc), run_time=0.7)
        self.at("rises")
        self.play(pc.animate.move_to([0, 0.2, 0]), run_time=1.9, rate_func=smooth)
        lv = ValueTracker(0.85)
        th = always_redraw(lambda: therm_glyph(pc[0].get_right() + RIGHT * 0.3, lv.get_value(), 0.9))
        self.at("As it rises")
        self.play(FadeIn(th), FadeOut(warm), run_time=0.6)
        self.at("expands")
        self.play(pc.animate.scale(1.6), run_time=1.3)
        self.at("cools")
        self.play(lv.animate.set_value(0.25), run_time=1.5)
        self.at("water vapor")
        self.play(Indicate(pc[1], color=TEXT, scale_factor=1.3), run_time=0.9)
        self.at("condenses")
        band.cloud.move_to([0, 1.6, 0])
        self.play(FadeOut(pc[1][1:]), GrowFromPoint(band.cloud, pc.get_top()), run_time=1.4)
        band.cloud.add_updater(lambda m: m.move_to([band.bx.get_value(), 1.6, 0]))
        self.add(band.cloud)
        self.at("and it rains")
        self.play(FadeIn(band.rain), FadeOut(th), run_time=0.7)
        self.at("This is the equatorial")
        self.play(band.ground.animate.set_fill(GREEN, opacity=0.85), run_time=1.0)
        self.at("rain belt")
        l = lab("equatorial rain belt", 32, GREEN, halo=True).move_to([-3.4, -1.9, 0])
        self.play(FadeIn(l, shift=RIGHT * 0.2), run_time=0.6)
        self.play(pc.animate.shift(UP * 0.2), run_time=1.2)
        self.finish()


class S07Sink(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.0)
        self.add(base, band.ground, band.cloud, band.rain)
        sink_lab = lab("equatorial rain belt", 28, GREEN, halo=True).move_to([-3.4, -1.9, 0])
        self.add(sink_lab)
        self.play(FadeIn(base), run_time=0.3)
        self.at("The air now dry")
        p0 = make_parcel(PALE, 0.4).move_to([0, 2.1, 0])
        p0[0].set_fill(PALE, 0.2)
        self.play(FadeIn(p0, scale=0.7), FadeOut(sink_lab), run_time=0.7)
        pl, pr = p0.copy(), p0.copy()
        self.at("flows toward the poles")
        self.play(pr.animate.move_to([LX(30), 2.1, 0]), pl.animate.move_to([-LX(30), 2.1, 0]), FadeOut(p0), run_time=1.8, rate_func=smooth)
        sway(VGroup(pl, pr), 0.04, 2.0)
        self.add(pl, pr)
        self.at("Near 30 degrees")
        d1 = DashedLine([LX(30), -2.6, 0], [LX(30), 2.8, 0], color=YELLOW, stroke_width=3)
        d2 = DashedLine([-LX(30), -2.6, 0], [-LX(30), 2.8, 0], color=YELLOW, stroke_width=3)
        l1 = lab("30°N", 30, YELLOW).move_to([LX(30) + 0.8, 3.3, 0])
        l2 = lab("30°S", 30, YELLOW).move_to([-LX(30) - 0.8, 3.3, 0])
        self.play(Create(d1), Create(d2), FadeIn(l1), FadeIn(l2), run_time=1.2)
        self.wait(0.8)
        self.at("it sinks back down")
        pl.clear_updaters(); pr.clear_updaters()
        self.play(pr.animate.move_to([LX(30), -0.6, 0]), pl.animate.move_to([-LX(30), -0.6, 0]), run_time=1.3)
        self.play(Create(loop_path(1)), Create(loop_path(-1)), run_time=0.9)
        self.finish()


class S08Dry(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.0)
        tan = VGroup(*[Rectangle(width=2.0, height=0.2, stroke_width=0, fill_color=TAN, fill_opacity=0.0).move_to([s * LX(30), -2.7, 0]) for s in (1, -1)])
        d1 = DashedLine([LX(30), -2.6, 0], [LX(30), 2.8, 0], color=YELLOW, stroke_width=2, stroke_opacity=0.5)
        d2 = DashedLine([-LX(30), -2.6, 0], [-LX(30), 2.8, 0], color=YELLOW, stroke_width=2, stroke_opacity=0.5)
        lp = VGroup(loop_path(1), loop_path(-1))
        pr = make_parcel(PALE, 0.4).move_to([LX(30), -0.6, 0])
        pl = make_parcel(PALE, 0.4).move_to([-LX(30), -0.6, 0])
        for p in (pr, pl):
            p[0].set_fill(PALE, 0.2)
        self.add(base, tan, band.ground, band.cloud, band.rain, d1, d2, lp, pr, pl)
        lv = ValueTracker(0.35)
        th = always_redraw(lambda: therm_glyph(pr[0].get_right() + RIGHT * 0.3, lv.get_value(), 0.9))
        self.at("Sinking air is squeezed")
        self.play(pr.animate.scale(0.65).move_to([LX(30), -1.9, 0]), pl.animate.scale(0.65).move_to([-LX(30), -1.9, 0]), run_time=1.4)
        self.add(th)
        self.at("and it warms")
        self.play(lv.animate.set_value(0.85), pr[0].animate.set_color(GOLD), pl[0].animate.set_color(GOLD), run_time=1.6)
        rh = ValueTracker(0.85)
        gbox = Rectangle(width=0.5, height=2.2, stroke_color=TEXT, stroke_width=3).move_to([5.9, 0.2, 0])
        gfill = always_redraw(lambda: Rectangle(width=0.4, height=max(0.02, 2.1 * rh.get_value()), stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([5.9, 0.2 - 1.05 + max(0.02, 2.1 * rh.get_value()) / 2, 0]))
        glab = lab("relative\nhumidity", 24, TEXT).move_to([5.7, 2.15, 0])
        self.at("Warming takes it")
        self.play(FadeIn(gbox), FadeIn(gfill), FadeIn(glab), run_time=0.6)
        self.at("further from the point")
        self.play(rh.animate.set_value(0.25), run_time=2.4)
        note = lab("same water", 26, TEXT, halo=True).move_to([LX(30) + 1.12, 0.5, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.wait(0.3)
        self.at("So sinking air stays clear")
        self.play(FadeOut(note), tan.animate.set_fill(TAN, 0.6), run_time=2.0)
        self.at("and rain is rare")
        dr = drop_icon(BLUE, 1.2).move_to([LX(30), 0.9, 0])
        cr = VGroup(Line([LX(30) - 0.4, 0.5, 0], [LX(30) + 0.4, 1.3, 0], color=RED, stroke_width=8), Line([LX(30) - 0.4, 1.3, 0], [LX(30) + 0.4, 0.5, 0], color=RED, stroke_width=8))
        self.play(FadeIn(dr), Create(cr), run_time=0.9)
        self.wait(0.8)
        self.at("Many great deserts")
        self.play(FadeOut(dr), FadeOut(cr), FadeOut(gbox), FadeOut(gfill), FadeOut(glab), FadeOut(th), FadeOut(pr), FadeOut(pl), FadeOut(lp),
                  tan.animate.set_fill(TAN, 0.95), run_time=1.2)
        dl = VGroup(lab("desert", 30, TAN, halo=True).move_to([LX(30), -1.8, 0]), lab("desert", 30, TAN, halo=True).move_to([-LX(30), -1.8, 0]))
        self.play(FadeIn(dl, shift=UP * 0.15), run_time=0.7)
        self.at("the Sahara")
        sa = lab("Sahara", 38, TAN, weight=BOLD, halo=True).move_to([LX(30), -0.9, 0])
        self.play(FadeIn(sa, shift=DOWN * 0.15), run_time=0.7)
        self.play(sa.animate.scale(1.12), run_time=0.8)
        self.finish()


class S09Rule1(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.0)
        tan = tan_patches(0.95)
        fl = [flow_dots(1), flow_dots(-1)]
        world = VGroup(base, band.ground, tan, band.cloud, band.rain, *fl)
        self.add(base, tan, band.ground, band.cloud, band.rain, *fl)
        # opacity reduced on updating groups would be reset by updaters; dim via overlay instead
        self.at("So here is")
        head = lab("The rule, first half", 38, YELLOW, weight=BOLD).move_to([0, 3.0, 0])
        veil = Rectangle(width=14.4, height=6.2, stroke_width=0, fill_color=BG, fill_opacity=0.72).move_to([0, 0.2, 0])
        self.play(FadeIn(veil), FadeIn(head), run_time=0.8)
        self.at("Rain falls where")
        a1 = Arrow([-5.7, -0.1, 0], [-5.7, 1.3, 0], color=BLUE, buff=0, stroke_width=10, tip_length=0.35)
        l1 = lab("Rain where moist air rises and cools", 38, TEXT).move_to([0.1, 0.6, 0])
        self.play(GrowArrow(a1), FadeIn(l1, shift=RIGHT * 0.3), run_time=1.0)
        self.at("It is scarce")
        a2 = Arrow([-5.7, -0.6, 0], [-5.7, -2.0, 0], color=GOLD, buff=0, stroke_width=10, tip_length=0.35)
        l2 = lab("Scarce where air sinks and warms", 38, TEXT).move_to([-0.35, -1.3, 0])
        self.play(GrowArrow(a2), FadeIn(l2, shift=RIGHT * 0.3), run_time=1.0)
        self.play(l1.animate.set_color(BLUE), run_time=0.6)
        self.play(l2.animate.set_color(GOLD), run_time=0.6)
        self.finish()


class S10Shift(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.0)
        day = ValueTracker(80)
        sx = lambda: LX(23.44 * math.sin(2 * math.pi * (day.get_value() - 80) / 365))
        sun = sun_glyph([0, 3.25, 0])
        sun.add_updater(lambda m: m.move_to([sx(), 3.25, 0]))
        ray = DashedLine([0, 2.8, 0], [0, -2.6, 0], color=YELLOW, stroke_width=2.5)
        ray.add_updater(lambda m: m.become(DashedLine([sx(), 2.8, 0], [sx(), -2.6, 0], color=YELLOW, stroke_width=2.5, stroke_opacity=0.6)))
        mon = always_redraw(lambda: lab(MONTH_NAMES[int(((day.get_value() - 1) % 365) / 30.42) % 12], 36, YELLOW).move_to([-5.7, 3.25, 0]))
        lag = Mobject()
        lag.add_updater(lambda m, dt: band.bx.set_value(band.bx.get_value() + (sx() - band.bx.get_value()) * (1 - math.exp(-dt / 0.45))))
        self.add(base, band.ground, band.cloud, band.rain, lag)
        self.at("The rain belt does not stay put")
        self.wait(0.2)
        self.play(FadeIn(sun), run_time=0.5)
        self.add(ray)
        self.play(FadeIn(mon), run_time=0.3)
        self.at("Through the year")
        self.play(day.animate.set_value(80 + 365), run_time=7.0, rate_func=linear)
        self.wait(0.3)
        self.finish()


class S11Predict(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.0)
        self.add(base, band.ground, band.cloud, band.rain)
        PINX = 2.9
        pin = VGroup(Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.4).rotate(PI),
                     Circle(radius=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=1).shift(UP * 0.5))
        pin.move_to([PINX, GROUND_TOP + 0.6, 0])
        self.at("Picture a town")
        self.play(band.bx.animate.set_value(2.3), run_time=2.4)
        self.play(FadeIn(pin, shift=DOWN * 0.5), run_time=0.01)
        tl = lab("town", 30, YELLOW, halo=True).move_to([PINX + 0.0, -1.3, 0])
        self.add(tl)
        self.at("near the edge")
        ghosts = VGroup(*[DashedVMobject(Rectangle(width=2.2, height=0.2, color=GREEN, stroke_width=3).move_to([s * 2.3, -2.7, 0])) for s in (1, -1)])
        arr = DoubleArrow([-2.3, 2.8, 0], [2.3, 2.8, 0], color=GREEN, buff=0, stroke_width=5, tip_length=0.25)
        sl = lab("the swing", 30, GREEN).move_to([0, 3.35, 0])
        self.play(Create(ghosts), GrowFromCenter(arr), FadeIn(sl), run_time=1.0)
        self.wait(0.8)
        self.at("Does it get rain")
        q = lab("Rain all year, or only part?", 44, YELLOW, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeOut(sl), FadeOut(arr), FadeIn(q), run_time=0.7)
        self.at("or only part of it")
        self.play(band.bx.animate.set_value(0.9), run_time=1.6)
        self.finish()


class S12Pause(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.9)
        PINX = 2.9
        pin = VGroup(Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.4).rotate(PI),
                     Circle(radius=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=1).shift(UP * 0.5)).move_to([PINX, GROUND_TOP + 0.6, 0])
        q = lab("Rain all year, or only part?", 44, YELLOW, weight=BOLD).move_to([0, 3.25, 0])
        tl = lab("town", 30, YELLOW, halo=True).move_to([PINX, -1.3, 0])
        ring_bg = Circle(radius=0.45, color=GREY, stroke_width=4).move_to([-5.9, 0.4, 0])
        self.add(base, band.ground, band.cloud, band.rain, pin, tl, q, ring_bg)
        ring = Arc(radius=0.45, start_angle=PI / 2, angle=0.001, color=YELLOW, stroke_width=7, arc_center=[-5.9, 0.4, 0])
        t = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=PI / 2, angle=-2 * PI * max(t.get_value(), 0.002), color=YELLOW, stroke_width=7, arc_center=[-5.9, 0.4, 0]))
        self.add(ring)
        self.play(t.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S13Reveal(AmbScene):
    def construct(self):
        base = base_world()
        band = Band(0.9)
        PINX = 2.9
        pin = VGroup(Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.4).rotate(PI),
                     Circle(radius=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=1).shift(UP * 0.5)).move_to([PINX, GROUND_TOP + 0.6, 0])
        tl = lab("town", 30, YELLOW, halo=True).move_to([PINX, -1.3, 0])
        self.add(base, band.ground, band.cloud, band.rain, pin, tl)
        self.at("Only part of it")
        self.play(band.bx.animate.set_value(1.3), run_time=1.5)
        self.at("The town is wet")
        self.play(band.bx.animate.set_value(2.3), run_time=1.3)
        self.at("belt is overhead")
        wl = lab("wet season", 38, BLUE, weight=BOLD, halo=True).move_to([5.0, 2.4, 0])
        self.play(FadeIn(wl, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.6)
        self.at("dry when the belt moves away")
        self.play(FadeOut(wl), band.bx.animate.set_value(-0.6), run_time=2.0)
        dl = lab("dry season", 38, GOLD, weight=BOLD, halo=True).move_to([5.0, 2.4, 0])
        self.play(FadeIn(dl, shift=LEFT * 0.2), run_time=0.6)
        self.at("A wet season")
        self.play(FadeOut(dl), band.bx.animate.set_value(0.2), run_time=0.6)
        sq = VGroup(*[Square(side_length=0.5, stroke_color=GREY, stroke_width=2).move_to([-2.75 + i * 0.5, 3.15, 0]) for i in range(12)])
        ltr = VGroup(*[T(m, 24, GREY).move_to(sq[i]) for i, m in enumerate(MONTHS)])
        self.play(Create(sq), FadeIn(ltr), run_time=0.4)
        self.play(*[sq[i].animate.set_fill(BLUE, 0.85) for i in range(12) if WET_MONTHS[i]], run_time=0.5)
        self.at("then a dry one")
        self.play(*[sq[i].animate.set_fill(GOLD, 0.85) for i in range(12) if not WET_MONTHS[i]], run_time=1.0)
        note = lab("schematic", 22, GREY).move_to([4.6, 3.15, 0])
        self.play(FadeIn(note), run_time=0.3)
        self.finish()


class S14Diagram(AmbScene):
    def construct(self):
        ch = Chart(0, 0.1, 10, 5.2)
        sq = VGroup(*[Square(side_length=0.8, stroke_color=BG, stroke_width=2).set_fill(BLUE if WET_MONTHS[i] else GOLD, 0.85).move_to([-4.4 + i * 0.8, 0.5, 0]) for i in range(12)])
        ltr = VGroup(*[T(m, 28, BG, weight=BOLD).move_to(sq[i]) for i, m in enumerate(MONTHS)])
        wl = lab("wet months", 32, BLUE).move_to([-3.0, -0.5, 0])
        dl = lab("dry months", 32, GOLD).move_to([3.0, -0.5, 0])
        self.at("Ecologists draw that")
        self.play(FadeIn(sq, lag_ratio=0.1), FadeIn(ltr, lag_ratio=0.1), run_time=1.2)
        self.play(FadeIn(wl), FadeIn(dl), run_time=0.5)
        self.wait(0.3)
        self.at("climate diagram")
        axes = ch.axes()
        flat = VGroup(*[Rectangle(width=0.8, height=0.14, stroke_width=0, fill_color=BLUE if WET_MONTHS[i] else GOLD, fill_opacity=0.85).move_to([ch.X(i + 0.5), ch.cy - ch.h / 2 - 0.12, 0]) for i in range(12)])
        self.play(Create(axes), Transform(sq, flat), FadeOut(ltr), FadeOut(wl), FadeOut(dl), run_time=1.8)
        self.at("Months run along")
        mo = ch.months()
        self.play(FadeIn(mo, lag_ratio=0.12), run_time=1.5)
        self.play(FadeOut(sq), run_time=0.4)
        self.at("A red line")
        red = ch.red()
        rl = lab("temperature", 32, RED, halo=True).move_to([-3.3, 1.45, 0])
        self.play(Create(red), FadeIn(rl), run_time=2.4, rate_func=linear)
        self.wait(0.3)
        self.at("A blue line")
        blue = ch.blue()
        bl = lab("rain", 32, BLUE, halo=True).move_to([-3.3, -1.35, 0])
        self.play(Create(blue), FadeIn(bl), run_time=2.4, rate_func=linear)
        sc = lab("schematic", 22, GREY).move_to([5.6, -3.55, 0])
        self.play(FadeIn(sc), run_time=0.3)
        self.finish()


class S15Rule2(AmbScene):
    def construct(self):
        ch = Chart(0, 0.1, 10, 5.2)
        axes, mo, red, blue = ch.axes(), ch.months(), ch.red(), ch.blue()
        self.add(axes, mo, red, blue)
        self.at("The scales are linked")
        tn = lab("Temperature (°C)", 26, RED).move_to([-4.3, 3.4, 0])
        rn = lab("Rain (mm)", 26, BLUE).move_to([4.7, 3.4, 0])
        tk = ch.ticks()
        self.play(FadeIn(tn), FadeIn(rn), FadeIn(tk), run_time=1.0)
        self.at("10 degrees sits level")
        yl = ch.YT(10)
        c1 = Circle(radius=0.3, color=YELLOW, stroke_width=5).move_to([ch.X(0) - 0.45, yl, 0])
        dash = DashedLine([ch.X(0), yl, 0], [ch.X(12), yl, 0], color=YELLOW, stroke_width=4)
        self.play(Create(c1), run_time=0.5)
        self.play(Create(dash), run_time=1.0)
        dot = Dot([ch.X(0), yl, 0], radius=0.1, color=YELLOW)
        self.at("20 millimeters")
        c2 = Circle(radius=0.3, color=YELLOW, stroke_width=5).move_to([ch.X(12) + 0.45, ch.YR(20), 0])
        self.play(Create(c2), run_time=0.5)
        self.add(dot)
        self.play(dot.animate.move_to([ch.X(12), yl, 0]), run_time=1.2)
        self.play(dot.animate.move_to([ch.X(0), yl, 0]), run_time=1.0)
        self.at("When the blue line")
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(dot), dash.animate.set_stroke(opacity=0.35), run_time=0.4)
        fills = ch.fills()
        self.play(FadeIn(fills), run_time=2.0)
        self.at("month is")
        lbl = lab("dry month: rain (mm) < 2 × temperature (°C)", 26, GOLD).move_to([0, -3.55, 0])
        self.play(FadeIn(lbl, shift=UP * 0.1), run_time=0.7)
        self.play(fills.animate.set_fill(GOLD, 0.7), run_time=0.7)
        self.play(fills.animate.set_fill(GOLD, 0.5), run_time=0.7)
        self.finish()


class S16Rule2b(AmbScene):
    def construct(self):
        tr = ValueTracker(0)
        ch = Chart(-2.7, 0.0, 7.2, 4.4, tr=tr)
        axes = ch.axes()
        sr = Rectangle(width=0.1, height=0.1)
        self.at("That is the second half")
        red_s, blue_s = ch.red(), ch.blue()
        self.play(Create(axes), Create(red_s), Create(blue_s), run_time=1.6)
        self.remove(red_s)
        red = always_redraw(ch.red)
        fills = always_redraw(ch.fills)
        self.add(red, fills)
        rl = lab("temperature", 28, RED, halo=True).move_to([-4.9, 2.55, 0])
        bl = lab("rain", 28, BLUE, halo=True).move_to([-0.4, 1.7, 0])
        self.play(FadeIn(rl), FadeIn(bl), run_time=0.4)

        def row(y, arrow, color, text):
            return VGroup(arrow, lab(text, 30, TEXT)).arrange(RIGHT, buff=0.3).move_to([4.1, y, 0]).set_x(4.1) if False else None
        def card_line(y, color, text, up):
            a = Arrow([0, -0.4 if up else 0.4, 0], [0, 0.4 if up else -0.4, 0], color=color, buff=0, stroke_width=9, tip_length=0.28).move_to([1.5, y, 0])
            t = lab(text, 30, TEXT).move_to([4.5, y, 0])
            t.align_to([1.95, 0, 0], LEFT)
            return VGroup(a, t)
        c1 = card_line(1.9, BLUE, "Rain where moist air\nrises and cools", True)
        c2 = card_line(0.3, GOLD, "Scarce where air\nsinks and warms", False)
        c3 = card_line(-1.3, RED, "Warmer months\nneed more rain", True)
        self.at("rule")
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.7)
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.7)
        self.at("The warmer a month")
        self.play(tr.animate.set_value(7.0), run_time=1.4, rate_func=smooth)
        self.at("more rain it needs")
        self.play(FadeIn(c3, shift=LEFT * 0.2), run_time=0.8)
        self.play(c3[1].animate.set_color(RED), run_time=0.5)
        self.play(tr.animate.set_value(8.0), run_time=1.2)
        self.finish()


class S17Close(AmbScene):
    def construct(self):
        def flat(c, rv, tv):
            return Chart(c, -0.2, 5.8, 3.4, tf=lambda u: tv, rf=lambda u: rv)
        fch, dch = flat(-3.4, 70, 26), flat(3.4, 6, 28)
        names = []
        for ch in (fch, dch):
            pass
        self.at("Read month by month")
        ax = [ch.axes() for ch in (fch, dch)]
        reds = [ch.red() for ch in (fch, dch)]
        blues = [ch.blue() for ch in (fch, dch)]
        self.play(*[Create(a) for a in ax], run_time=0.5)
        self.play(*[Create(m) for m in reds + blues], run_time=0.8)
        ff = fch.fills()
        # wet fill for forest: rain above red, drawn blue
        fwet = VGroup(Polygon(*([[fch.X(u), fch.YT(26), 0] for u in np.linspace(0.5, 11.5, 12)] + [[fch.X(u), fch.YR(70), 0] for u in np.linspace(0.5, 11.5, 12)][::-1]),
                              stroke_width=0, fill_color=BLUE, fill_opacity=0.3))
        df = dch.fills()
        self.play(FadeIn(fwet), FadeIn(df), run_time=0.4)
        self.at("Warmth and water")
        forest = VGroup(*[tree(-0.7 + 0.7 * i, -0.3, 1.5) for i in range(3)]).move_to([-3.4, 2.5, 0])
        desert = VGroup(*[VMobject().set_points_smoothly([[t, 0.22 * math.sin(2.2 * t + k) + k * 0.4, 0] for t in np.linspace(-1.2, 1.2, 14)]).set_stroke(TAN, 8) for k in range(3)]).move_to([3.4, 2.5, 0])
        self.play(FadeIn(forest, shift=DOWN * 0.2), FadeIn(desert, shift=DOWN * 0.2), run_time=0.8)
        sway(forest, 0.05, 1.8)
        self.add(forest)
        self.at("first guess")
        g1 = lab("first guess", 32, GREEN).move_to([-3.4, -2.35, 0])
        g2 = lab("first guess", 32, TAN).move_to([3.4, -2.35, 0])
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.7)
        self.at("A guess not a final answer")
        fn = lab("A guess, not a final answer.", 36, YELLOW).move_to([0, -3.3, 0])
        self.play(FadeIn(fn, shift=UP * 0.1), run_time=0.8)
        self.play(fn.animate.scale(1.05), run_time=0.8)
        self.finish()


class S18End(EndCard):
    LINE = "Rain follows rising moist air; warmer months need more of it."
