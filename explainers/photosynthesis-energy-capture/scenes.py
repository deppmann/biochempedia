"""A Tree Made of Air: where a plant's mass comes from (chapter-1 film, Capturing Sunlight).

COLOUR MAP (whole film): carbon dioxide BLUE, water TEAL, light YELLOW, glucose AMBER, oxygen RED,
the plant GREEN (dry plant grey-brown), soil brown, structure GREY.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F2A93B"
SOIL = "#8B6B4A"
DRYC = "#A08C6E"
POTC = "#B07A55"
WOODC = "#8A6A45"
LX, RX, PY = -3.4, 4.9, -2.3          # left scale x, right (soil) scale x, platform top
QC = np.array([6.3, 3.25, 0])         # corner of the question mark
PIE_C = np.array([LX, 0.5, 0])
PIE_R = 2.4
EPI_Y, SX = 2.25, -3.6                # leaf surface and the stoma
CELL = (-6.2, 2.6, -2.95, 1.9)        # x0, x1, y0, y1 of the big cell
CH_C = np.array([-1.8, -0.55, 0])     # chloroplast centre
VX = 4.6                              # vein x


def P(x, y):
    return np.array([x, y, 0.0])


def setop(ch, o):
    ch[0].set_stroke(opacity=o)
    ch[0].set_fill(opacity=0.16 * o)
    ch[1].set_opacity(o)


def world_start(sc, ambient=True):
    """A clock every moving thing reads, and faint drifting motes so a held frame is never dead."""
    sc.clock = ValueTracker(0)
    sc.clock.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(sc.clock)
    if not ambient:
        return
    rng = random.Random(type(sc).__name__)
    W, H = config.frame_width, config.frame_height
    motes = VGroup()
    for _ in range(22):
        d = Dot(radius=rng.uniform(0.025, 0.06), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.12, 0.3))
        d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
        d.v = (rng.uniform(-0.2, 0.2), rng.uniform(0.15, 0.4))

        def drift(m, dt, W=W, H=H):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > H / 2 + 0.1:
                m.shift(DOWN * (H + 0.2))
            if abs(m.get_x()) > W / 2 + 0.1:
                m.shift(LEFT * (W + 0.2) * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-10)
    sc.add(motes)


# ----------------------------------------------------------------------------- the willow
LEAVES = [(-0.75, -0.05, 0.55), (0.75, -0.05, 0.55), (0, 0.45, 0.62), (-0.45, 0.35, 0.5), (0.45, 0.35, 0.5),
          (0, -0.05, 0.7), (-1.0, -0.4, 0.38), (1.0, -0.4, 0.38)]


class Plant:
    """Pot + willow. Trackers: g (growth 0..1), dry (0..1 grey-brown), wet (0..1 teal tint), bx (x of the pot)."""

    def __init__(self, sc, g=1.0, dry=0.0, wet=0.0, bx=LX, by=PY):
        self.sc = sc
        self.g, self.dry, self.wet = ValueTracker(g), ValueTracker(dry), ValueTracker(wet)
        self.bx, self.by = ValueTracker(bx), ValueTracker(by)
        self.mob = always_redraw(self.build)

    def build(self):
        g, dry, wet = self.g.get_value(), self.dry.get_value(), self.wet.get_value()
        x, y, t = self.bx.get_value(), self.by.get_value(), self.sc.clock.get_value()
        leaf = interpolate_color(interpolate_color(ManimColor(GREEN), ManimColor(DRYC), dry), ManimColor(TEAL), 0.65 * wet)
        wood = interpolate_color(interpolate_color(ManimColor(WOODC), ManimColor("#7D6D5A"), dry), ManimColor(TEAL), 0.6 * wet)
        pot = Polygon(P(x - 1.15, y + 0.9), P(x + 1.15, y + 0.9), P(x + 0.85, y), P(x - 0.85, y),
                      stroke_color=POTC, stroke_width=3, fill_color=POTC, fill_opacity=0.55)
        soil = Polygon(P(x - 1.1, y + 0.9), P(x + 1.1, y + 0.9), P(x + 1.08, y + 0.74), P(x - 1.08, y + 0.74),
                       stroke_width=0, fill_color=SOIL, fill_opacity=1)
        y0 = y + 0.9
        h = 0.5 + 2.4 * g ** 0.85
        w = 0.05 + 0.14 * g
        trunk = Polygon(P(x - w, y0), P(x + w, y0), P(x + w * 0.55, y0 + h), P(x - w * 0.55, y0 + h),
                        stroke_color=wood, stroke_width=2, fill_color=wood, fill_opacity=1)
        r = 0.12 + 1.0 * g
        parts = [pot, soil, trunk]
        for i, (dx, dy, rel) in enumerate(LEAVES):
            sw = 0.05 * np.sin(1.3 * t + i * 1.7) * (0.3 + g)
            sy = 0.03 * np.cos(1.1 * t + i) * (0.3 + g)
            c = Circle(radius=max(0.06, rel * r * 0.92), stroke_color=leaf, stroke_width=2,
                       fill_color=leaf, fill_opacity=0.6)
            c.move_to(P(x + dx * r * 1.45 + sw, y0 + h + dy * r * 1.45 + sy))
            parts.append(c)
        return VGroup(*parts)

    def snapshot(self):
        return self.build()

    def canopy_centre(self):
        return P(self.bx.get_value(), self.by.get_value() + 0.9 + 0.5 + 2.4 * self.g.get_value() ** 0.85 + 0.4)


# ----------------------------------------------------------------------------- scales
def scale_static(cx, w=3.4):
    plat = RoundedRectangle(corner_radius=0.08, width=w, height=0.2, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to(P(cx, PY - 0.1))
    base = RoundedRectangle(corner_radius=0.18, width=w * 0.88, height=1.1, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.18).move_to(P(cx, PY - 0.75))
    face = Circle(radius=0.46, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(cx, -3.15))
    ticks = VGroup(*[Line(P(cx + 0.46 * np.sin(np.radians(a)), -3.15 + 0.46 * np.cos(np.radians(a))),
                          P(cx + 0.37 * np.sin(np.radians(a)), -3.15 + 0.37 * np.cos(np.radians(a))),
                          stroke_color=GREY, stroke_width=3) for a in range(-135, 136, 45)])
    return VGroup(plat, base, face, ticks)


def needle(cx, val_fn):
    def mk():
        a = np.radians(-135 + 270 * float(np.clip(val_fn() / 400.0, 0, 1)))
        return Line(P(cx, -3.15), P(cx + 0.36 * np.sin(a), -3.15 + 0.36 * np.cos(a)), stroke_color=YELLOW, stroke_width=5)
    return always_redraw(mk)


def mound(cx):
    pts = [P(cx + 1.0 * np.cos(a), PY + 0.8 * np.sin(a)) for a in np.linspace(0, np.pi, 24)]
    m = VMobject(stroke_color=SOIL, stroke_width=2, fill_color=SOIL, fill_opacity=0.95)
    m.set_points_as_corners(pts + [pts[0]])
    return m


def tag(text, color=TEXT, size=32, **kw):
    return T(text, size, color, **kw)


def schematic_tag():
    return T("scale: schematic", 22, GREY).move_to(P(0.9, -3.55))


def corner_q():
    return T("?", 52, GOLD, weight=BOLD).move_to(QC)


def left_world(sc, plant, with_needle=True, right=True):
    """The scales of the willow story. Returns (static group, plant, right-needle) already added."""
    ls = scale_static(LX)
    sc.add(ls)
    objs = [ls]
    if with_needle:
        sc.add(needle(LX, lambda: 205 + 164 * plant.g.get_value() - 70 * plant.dry.get_value() * plant.g.get_value()))
    if right:
        rs = scale_static(RX, 2.2)
        mo = mound(RX)
        sc.add(rs, mo, needle(RX, lambda: 200 - 0.125 * plant.g.get_value()))
        objs += [rs, mo]
    sc.add(plant.mob)
    return objs


def pie_ring():
    return DashedVMobject(Circle(radius=PIE_R, stroke_color=GREY, stroke_width=4).move_to(PIE_C), num_dashes=40)


def cards():
    cs = [chip(t, TEXT, 32) for t in ("most", "about half", "almost none")]
    for c, y in zip(cs, (1.3, 0.2, -0.9)):
        c.move_to(P(1.3, y))
    return cs


def timeline():
    line = Line(P(-4.4, 3.35), P(3.9, 3.35), stroke_color=GREY, stroke_width=4)
    ticks = VGroup(*[Line(P(x, 3.2), P(x, 3.5), stroke_color=GREY, stroke_width=3) for x in np.linspace(-4.4, 3.9, 6)])
    lab = T("1600s", 30, GOLD, weight=BOLD).move_to(P(-5.5, 3.35))
    return VGroup(line, ticks, lab)


def qmark_pop(sc, mob):
    mob.add_updater(lambda m, dt: None)


# ----------------------------------------------------------------------------- leaf world
def epidermis(sc):
    xl, xr = SX - 1.25, SX + 1.25
    a = Line(P(-6.75, EPI_Y), P(xl, EPI_Y), stroke_color=GREEN, stroke_width=14).set_opacity(0.7)
    b = Line(P(xr, EPI_Y), P(6.75, EPI_Y), stroke_color=GREEN, stroke_width=14).set_opacity(0.7)

    def guards():
        op = 0.5 + 0.5 * np.sin(1.1 * sc.clock.get_value())
        d = 0.14 * op
        g1 = Ellipse(width=0.62, height=0.46, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.85, stroke_width=2).move_to(P(SX - 1.05 - d, EPI_Y))
        g2 = Ellipse(width=0.62, height=0.46, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.85, stroke_width=2).move_to(P(SX + 1.05 + d, EPI_Y))
        return VGroup(g1, g2)
    return VGroup(a, b, always_redraw(guards))


def vein():
    return RoundedRectangle(corner_radius=0.35, width=1.5, height=4.7, stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.1).move_to(P(VX, -1.35))


def big_cell():
    x0, x1, y0, y1 = CELL
    return RoundedRectangle(corner_radius=0.5, width=x1 - x0, height=y1 - y0, stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.06).move_to(P((x0 + x1) / 2, (y0 + y1) / 2))


def chloroplast():
    return Ellipse(width=7.4, height=3.5, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.22).move_to(CH_C)


def cell_grid():
    x0, x1, y0, y1 = CELL
    cols, rows = 6, 4
    w, h = (x1 - x0) / cols, (y1 - y0) / rows
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            cells.add(RoundedRectangle(corner_radius=0.2, width=w - 0.14, height=h - 0.14, stroke_color=GREEN, stroke_width=2,
                                       fill_color=GREEN, fill_opacity=0.05).move_to(P(x0 + w * (c + 0.5), y0 + h * (r + 0.5))).set_stroke(opacity=0.55))
    return cells


# ============================================================================ scenes
class S00Title(TitleCard):
    LESSON = "Capturing Sunlight"
    TITLE = "A Tree Made of Air"


class S01Question(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0, bx=0.6)
        floor = Line(P(-6.6, PY), P(6.6, PY), stroke_color=GREY, stroke_width=3).set_opacity(0.6)
        self.add(floor)
        q = T("?", 190, GOLD, weight=BOLD).move_to(P(3.3, 0.9))
        q.add_updater(lambda m: m.move_to(P(3.3, 0.9 + 0.1 * np.sin(2.0 * self.clock.get_value()))) if m.get_height() > 1 else None)
        self.play(FadeIn(pl.mob, shift=UP * 0.2), FadeIn(q, scale=0.6), run_time=0.9)
        self.at("a willow in a pot")
        ring = SurroundingRectangle(VGroup(Rectangle(width=2.4, height=0.9).move_to(P(0.6, PY + 0.45))), color=GOLD, buff=0.15, stroke_width=5)
        self.play(Create(ring), run_time=0.4)
        self.play(FadeOut(ring), run_time=0.3)
        self.at("weighed long ago")
        ls = scale_static(LX)
        nd = needle(LX, lambda: (205 + 164 * pl.g.get_value()) * float(np.clip((0.6 - pl.bx.get_value()) / (0.6 - LX), 0, 1)) ** 2)
        self.play(FadeIn(ls, shift=UP * 0.2), FadeOut(floor), run_time=0.7)
        self.add(nd)
        self.play(pl.bx.animate.set_value(LX), run_time=1.2, rate_func=smooth)
        self.at("turns that into a puzzle")
        q.clear_updaters()
        self.play(q.animate.scale(0.28).move_to(QC), run_time=1.2)
        self.at("here is what the man")
        rs = scale_static(RX, 2.2)
        mo = mound(RX)
        self.add(needle(RX, lambda: 200))
        tl = timeline()
        self.play(FadeIn(rs), FadeIn(mo), Create(tl[0]), FadeIn(tl[1]), FadeIn(tl[2], shift=RIGHT * 0.2), run_time=1.0)
        self.finish()


class S02Willow(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0)
        left_world(self, pl)
        tl = timeline()
        q = corner_q()
        self.add(tl, q, schematic_tag())
        self.play(pl.g.animate.set_value(0.0), run_time=1.6, rate_func=smooth)
        self.at("five pound willow stem")
        t1 = tag("stem: 5 lb", GREEN).move_to(P(-0.6, 1.2), aligned_edge=LEFT)
        self.play(FadeIn(t1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("200 pounds")
        t2 = tag("dried soil: 200 lb", "#C9A27A").move_to(P(RX, -0.35))
        self.play(FadeIn(t2, shift=UP * 0.15), run_time=0.6)
        self.at("five years later")
        yr = ValueTracker(0)
        cnt = always_redraw(lambda: T(f"year {int(round(yr.get_value()))}", 30, TEXT, weight=BOLD).move_to(P(5.1, 3.35)))
        dot = always_redraw(lambda: Dot(P(-4.4 + 8.3 * yr.get_value() / 5, 3.35), radius=0.13, color=YELLOW))
        self.add(cnt, dot)
        self.play(yr.animate.set_value(5), pl.g.animate.set_value(1.0), run_time=2.8, rate_func=linear)
        self.at("about 169")
        t3 = tag("tree: about 169 lb", GREEN).move_to(P(-0.6, 1.2), aligned_edge=LEFT)
        self.play(ReplacementTransform(t1, t3), run_time=0.6)
        self.at("the soil was only")
        t4 = tag("soil: about\n2 oz lighter", "#C9A27A").move_to(P(RX, -0.5))
        ring = Circle(radius=0.62, stroke_color=GOLD, stroke_width=5).move_to(P(RX, -3.15))
        self.play(ReplacementTransform(t2, t4), Create(ring), run_time=0.8)
        self.play(ring.animate.scale(1.25).set_stroke(opacity=0.3), run_time=1.0)
        self.finish()


def dry_world(sc, wet=0.0, dry=1.0, needle_ok=True):
    pl = Plant(sc, g=1.0, dry=dry, wet=wet)
    left_world(sc, pl)
    sc.add(corner_q(), schematic_tag())
    return pl


class S03Dry(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0)
        left_world(self, pl)
        self.add(corner_q(), schematic_tag())
        stamp_t = T("soil loss:\nfar too small", 28, TEXT, weight=BOLD, line_spacing=0.9)
        box = SurroundingRectangle(stamp_t, color=GOLD, buff=0.18, stroke_width=4, corner_radius=0.1)
        stamp = VGroup(box, stamp_t).move_to(P(RX, 0.2)).rotate(-0.08)
        self.at("so soil loss")
        self.play(FadeIn(stamp, scale=1.5), run_time=0.5)
        self.at("alive")
        wl = tag("water in a\nliving tree", TEAL).move_to(P(-0.6, 1.4), aligned_edge=LEFT)
        self.play(pl.wet.animate.set_value(1.0), FadeIn(wl, shift=RIGHT * 0.2), run_time=1.6)
        self.at("but dry the tree")
        dl = tag("dried", GREY).move_to(P(-0.6, 1.4), aligned_edge=LEFT)
        self.play(FadeOut(wl), pl.wet.animate.set_value(0.0), run_time=0.9)
        self.play(pl.dry.animate.set_value(1.0), FadeIn(dl), run_time=0.9)
        self.at("plenty of solid matter")
        dm = tag("dry mass: the\nmass left after\ndrying", TEXT).move_to(P(-0.6, 1.4), aligned_edge=LEFT)
        self.play(ReplacementTransform(dl, dm), run_time=0.6)
        self.finish()


def predict_frame(sc, pl, lit=None):
    q = T("How much of the dry\nmass came from soil?", 30, TEXT, line_spacing=0.9).move_to(P(1.3, 2.7))
    ring = pie_ring()
    cs = cards()
    sc.add(q, ring, *cs)
    return q, ring, cs


class S04Predict(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0, dry=1.0)
        left_world(self, pl)
        self.add(corner_q(), schematic_tag())
        self.at("if you dried this tree")
        q = T("How much of the dry\nmass came from soil?", 30, TEXT, line_spacing=0.9).move_to(P(1.3, 2.7))
        ring = pie_ring()
        self.play(Create(ring), FadeIn(q, shift=DOWN * 0.15), run_time=1.2)
        self.at("most of it")
        cs = cards()
        self.play(FadeIn(cs[0], shift=LEFT * 0.5), run_time=0.5)
        self.at("about half")
        self.play(FadeIn(cs[1], shift=LEFT * 0.5), run_time=0.5)
        self.at("almost none")
        self.play(FadeIn(cs[2], shift=LEFT * 0.5), run_time=0.5)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0, dry=1.0)
        left_world(self, pl)
        self.add(corner_q(), schematic_tag())
        q = T("How much of the dry\nmass came from soil?", 30, TEXT, line_spacing=0.9).move_to(P(1.3, 2.7))
        ring = pie_ring()
        cs = cards()
        self.add(q, ring, *cs)
        k = ValueTracker(0)
        c0 = P(-6.0, 3.25)
        back = Circle(radius=0.36, stroke_color=GREY, stroke_width=4).move_to(c0)
        fill = always_redraw(lambda: Sector(radius=0.34, angle=max(0.01, TAU * k.get_value()), start_angle=PI / 2,
                                            fill_color=GOLD, fill_opacity=0.9, stroke_width=0, arc_center=c0))
        self.add(back, fill)

        def pulse(m, dt, i=[0]):
            pass
        for i, c in enumerate(cs):
            c.base = c.get_center().copy()
            c.add_updater(lambda m, dt, i=i: m.move_to(m.base + UP * 0.07 * np.sin(2.2 * self.clock.get_value() + i * 1.3)))
        self.play(k.animate.set_value(1.0), run_time=self.narration_s, rate_func=linear)
        self.finish()


class S06Reveal(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0, dry=1.0)
        left_world(self, pl)
        self.add(corner_q(), schematic_tag())
        q = T("How much of the dry\nmass came from soil?", 30, TEXT, line_spacing=0.9).move_to(P(1.3, 2.7))
        ring = pie_ring()
        cs = cards()
        self.add(q, ring, *cs)
        self.play(cs[2][0].animate.set_stroke(GREEN, 5).set_fill(GREEN, 0.35), cs[2][1].animate.set_color(GREEN),
                  cs[0].animate.set_opacity(0.25), cs[1].animate.set_opacity(0.25), run_time=0.8)
        self.at("soil gives a plant")
        pie = Circle(radius=PIE_R, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to(PIE_C)
        qm = T("?", 110, GREY, weight=BOLD).move_to(PIE_C + UP * 0.2)
        qm.add_updater(lambda m: m.move_to(PIE_C + UP * (0.2 + 0.08 * np.sin(2.0 * self.clock.get_value()))))
        self.play(FadeOut(VGroup(q, *cs)), FadeIn(pie), FadeIn(qm, scale=0.7), run_time=1.0)
        self.at("a small share of minerals")
        wedge = Sector(radius=PIE_R, angle=0.38, start_angle=-0.1, fill_color=SOIL, fill_opacity=1, stroke_width=0, arc_center=PIE_C)
        lab = tag("soil minerals\n(small share)", "#C9A27A").move_to(P(0.7, 0.6), aligned_edge=LEFT)
        lead = Line(P(0.55, 0.45), PIE_C + P(PIE_R * 0.93, 0.0), stroke_color="#C9A27A", stroke_width=3)
        self.play(GrowFromCenter(wedge) if False else FadeIn(wedge, scale=1.3), run_time=0.8)
        self.play(FadeIn(lab, shift=LEFT * 0.2), Create(lead), run_time=0.7)
        self.at("something you cannot see")
        self.play(Indicate(qm, color=GOLD, scale_factor=1.25), run_time=1.0)
        self.at("it comes from the air")
        wisps = VGroup()
        rng = random.Random(3)
        for i in range(14):
            w = Circle(radius=rng.uniform(0.18, 0.34), stroke_width=0, fill_color=BLUE, fill_opacity=0.3)
            w.sx, w.sy = rng.uniform(-1.5, 1.5), rng.uniform(3.4, 4.2)
            w.ph = rng.random()
            w.tx, w.ty = LX + rng.uniform(-1.2, 1.2), 1.5 + rng.uniform(-0.6, 0.8)
            wisps.add(w)
        t0 = self.clock.get_value()

        def flow(m, dt):
            k = ((self.clock.get_value() - t0) * 0.45 + m.ph) % 1.0
            m.move_to(P(m.sx + (m.tx - m.sx) * k, m.sy + (m.ty - m.sy) * k))
            m.set_fill(opacity=0.35 * np.sin(np.pi * k))
        for w in wisps:
            w.add_updater(flow)
        self.add(wisps)
        self.finish()


# ----------------------------------------------------------------------------- the leaf
class S07Leaf(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0)
        ls = scale_static(LX)
        self.add(ls, pl.mob)
        self.wait(1.0)
        snap = pl.snapshot()
        self.remove(pl.mob)
        self.add(snap)
        epi, vn = epidermis(self), vein()
        grid = cell_grid()
        centre = pl.canopy_centre()
        self.play(snap.animate.scale(4.5, about_point=centre).set_opacity(0), ls.animate.scale(4.5, about_point=centre).set_opacity(0),
                  FadeIn(epi), FadeIn(grid), run_time=2.0, rate_func=smooth)
        self.remove(snap, ls)
        self.at("carbon dioxide")
        co2 = []
        for i in range(5):
            c = chip("CO2", BLUE, 26)
            c.ph, c.dx = i / 5, (0.28 if i % 2 else -0.28)
            co2.append(c)
        on = ValueTracker(0)

        def fall(m, dt):
            k = (self.clock.get_value() * 0.22 + m.ph) % 1.0
            m.move_to(P(SX + m.dx, 3.3 - 4.0 * k))
            setop(m, float(on.get_value() * np.clip(min(k * 8, (1 - k) * 6), 0, 1)))
        for c in co2:
            c.add_updater(fall)
        self.add(*co2)
        self.play(on.animate.set_value(1), run_time=0.8)
        self.at("tiny pores called stomata")
        sl = tag("stoma (pores: stomata)", TEXT).move_to(P(-2.6, 3.2), aligned_edge=LEFT)
        self.play(FadeIn(sl, shift=RIGHT * 0.2), run_time=0.6)
        self.at("water climbs up")
        h2o = []
        for i in range(4):
            c = chip("H2O", TEAL, 26)
            c.ph = i / 4
            h2o.append(c)
        won = ValueTracker(0)

        def rise(m, dt):
            k = (self.clock.get_value() * 0.2 + m.ph) % 1.0
            m.move_to(P(VX, -3.5 + 3.9 * k))
            setop(m, float(won.get_value() * np.clip(min(k * 8, (1 - k) * 6), 0, 1)))
        for c in h2o:
            c.add_updater(rise)
        self.add(vn, *h2o)
        self.play(FadeIn(vn), won.animate.set_value(1), FadeOut(sl), run_time=0.9)
        self.at("from the roots")
        rl = tag("from the roots", TEAL).move_to(P(VX - 0.3, -3.55), aligned_edge=ORIGIN)
        rl.move_to(P(2.0, -3.4))
        self.play(FadeIn(rl, shift=UP * 0.1), run_time=0.5)
        self.at("inside a leaf cell")
        x0, x1, y0, y1 = CELL
        w, h = (x1 - x0) / 6, (y1 - y0) / 4
        sel = RoundedRectangle(corner_radius=0.2, width=w - 0.14, height=h - 0.14, stroke_color=GREEN, stroke_width=5).move_to(P(x0 + w * 2.5, y0 + h * 2.5))
        self.play(Create(sel), FadeOut(rl), run_time=0.6)
        bc = big_cell()
        on.set_value(0)
        self.play(ReplacementTransform(sel, bc), FadeOut(grid), FadeOut(VGroup(*co2)), FadeOut(VGroup(*h2o)), run_time=1.3)
        for c in co2 + h2o:
            c.clear_updaters()
        self.at("a green chloroplast")
        chl = chloroplast()
        cl = tag("chloroplast", GREEN, weight=BOLD).move_to(CH_C + DOWN * 0.1)
        self.play(GrowFromCenter(chl), run_time=0.8)
        self.play(FadeIn(cl), run_time=0.4)
        self.at("catches light")
        rays = VGroup(*[Line(P(-5.4 + 1.5 * i + 0.8, 3.7), P(-5.4 + 1.5 * i - 0.4, 0.9), stroke_color=YELLOW, stroke_width=7) for i in range(5)])
        for r in rays:
            r.set_cap_style(CapStyleType.ROUND)
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.15), chl.animate.set_stroke(YELLOW, 7).set_fill(GREEN, 0.4), run_time=1.2)
        self.finish()


def cell_world(sc, vein_on=True, label=True, rays=False):
    epi = epidermis(sc)
    bc = big_cell()
    chl = chloroplast()
    objs = [epi, bc, chl]
    sc.add(*objs)
    if vein_on:
        v = vein()
        sc.add(v)
        objs.append(v)
    return objs


def grana():
    stacks = VGroup()
    dots = VGroup()
    for cx in (-4.8, -3.7, -2.6):
        for k in range(4):
            stacks.add(RoundedRectangle(corner_radius=0.05, width=0.95, height=0.15, stroke_color=GREEN, stroke_width=2,
                                        fill_color=GREEN, fill_opacity=0.85).move_to(P(cx, -0.1 - 0.28 * k + 0.4)))
            dots.add(Dot(radius=0.05, color="#D6F2A8").move_to(P(cx - 0.3 + 0.2 * (k % 4), -0.1 - 0.28 * k + 0.4)))
    return stacks, dots


class S08Pigment(SpokenScene):
    def construct(self):
        world_start(self)
        objs = cell_world(self)
        self.at("its green pigment")
        stacks, dots = grana()
        sl = tag("stacked membranes", GREEN).move_to(P(-1.8, 0.75))
        self.play(FadeIn(stacks, shift=UP * 0.2), FadeIn(sl), run_time=0.9)
        self.play(FadeIn(dots), run_time=0.4)
        self.at("chlorophyll")
        cl = tag("chlorophyll", "#D6F2A8").move_to(P(-3.7, -1.15))
        self.play(FadeIn(cl, shift=UP * 0.1), Indicate(dots, color="#D6F2A8", scale_factor=1.4), run_time=0.8)
        self.at("absorbs mostly red")
        self.play(FadeOut(sl), run_time=0.3)
        cols = ["#FF4D4D", "#FF9F43", "#F5D547", "#83C167", "#4DD0E1", "#5B7BFF", "#9B6BE8"]
        beams = VGroup(*[Rectangle(width=0.4, height=1.1, stroke_width=0, fill_color=c, fill_opacity=0.95).move_to(P(-5.1 + 0.45 * i, 2.7)) for i, c in enumerate(cols)])
        self.add(beams)
        self.play(beams.animate.shift(DOWN * 2.45), run_time=1.3, rate_func=linear)
        absorbed = [0, 1, 5, 6]
        anims = []
        for i, b in enumerate(beams):
            if i in absorbed:
                anims.append(b.animate.scale(0.15).set_opacity(0))
            else:
                anims.append(b.animate.shift(UP * 2.0).set_opacity(0))
        self.play(*anims, run_time=1.0)
        self.remove(beams)
        # work area
        self.at("that captured light")
        wa = RoundedRectangle(corner_radius=0.2, width=2.5, height=2.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to(P(0.3, -0.45))
        wsc = T("schematic", 22, GREY).move_to(P(0.1, -1.3))
        self.play(FadeIn(wa), FadeIn(wsc), run_time=0.5)
        self.at("photosynthesis")
        flow = VGroup(*[Dot(radius=0.1, color=YELLOW) for _ in range(6)])
        for i, d in enumerate(flow):
            d.ph = i / 6

        def move(m, dt):
            k = (self.clock.get_value() * 0.5 + m.ph) % 1.0
            m.move_to(P(-2.2 + 2.0 * k, -0.2 + 0.15 * np.sin(6 * k + m.ph * 9)))
            m.set_opacity(float(np.clip(min(k * 6, (1 - k) * 6), 0, 1)))
        for d in flow:
            d.add_updater(move)
        self.add(flow)
        self.wait(0.2)
        self.at("water is split")
        h2o = chip("H2O", TEAL, 30).move_to(P(0.3, 0.15))
        wl = tag("water is split", TEAL).move_to(P(0.3, 1.55))
        self.play(FadeIn(h2o, shift=DOWN * 0.3), FadeIn(wl, shift=UP * 0.1), FadeOut(wsc), run_time=0.7)
        crack = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_as_corners([P(0.3, 0.55), P(0.18, 0.28), P(0.42, 0.1), P(0.2, -0.1), P(0.3, -0.25)])
        spark = VGroup(*[Line(P(0.3, 0.15) + 0.25 * np.array([np.cos(a), np.sin(a), 0]), P(0.3, 0.15) + 0.6 * np.array([np.cos(a), np.sin(a), 0]), stroke_color=YELLOW, stroke_width=5) for a in np.linspace(0, TAU, 8, endpoint=False)])
        self.play(Create(crack), FadeIn(spark), run_time=0.4)
        l_half, r_half = h2o.copy(), h2o.copy()
        self.remove(h2o)
        self.add(l_half, r_half)
        self.play(l_half.animate.shift(LEFT * 0.7).set_opacity(0), r_half.animate.shift(RIGHT * 0.7).set_opacity(0), FadeOut(crack), FadeOut(spark), run_time=0.8)
        self.at("carbon from carbon dioxide")
        co2 = chip("CO2", BLUE, 30).move_to(P(0.3, 0.5))
        self.play(FadeIn(co2, shift=DOWN * 0.3), FadeOut(wl), run_time=0.6)
        chain = VGroup()
        self.play(co2.animate.move_to(P(0.3, -1.0)), run_time=1.0)
        self.at("is built into sugar")
        for i in range(5):
            hx = RegularPolygon(6, radius=0.2, stroke_color=AMBER, stroke_width=3, fill_color=AMBER, fill_opacity=0.6).move_to(P(-0.4 + 0.35 * i, -1.35 + 0.0))
            chain.add(hx)
        self.play(FadeOut(co2), LaggedStart(*[GrowFromCenter(h) for h in chain], lag_ratio=0.25), run_time=1.4)
        self.finish()


def eq_line():
    parts = [("6CO2", BLUE), ("+", TEXT), ("6H2O", TEAL), ("+", TEXT), ("light energy", YELLOW), ("→", TEXT), ("C6H12O6", AMBER), ("+", TEXT), ("6O2", RED)]
    ms = [T(t, 28, c, weight=BOLD if c != TEXT else NORMAL) for t, c in parts]
    g = VGroup(*ms).arrange(RIGHT, buff=0.2).move_to(P(0, -3.3))
    return g


class S09Products(SpokenScene):
    def construct(self):
        world_start(self)
        objs = cell_world(self, vein_on=False)
        chl = objs[2]
        self.play(chl.animate.set_fill(GREEN, 0.05).set_stroke(opacity=0.4), run_time=0.4)
        eq = eq_line()
        a = VGroup(RoundedRectangle(corner_radius=0.18, width=3.0, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1),
                   VGroup(T("6CO2", 30, BLUE, weight=BOLD), T("+", 30), T("6H2O", 30, TEAL, weight=BOLD)).arrange(RIGHT, buff=0.15)).move_to(P(-4.4, -0.7))
        a[1].move_to(a[0])
        arrow = Arrow(P(-2.8, -0.7), P(-1.6, -0.7), buff=0, color=TEXT, stroke_width=6)
        self.at("the atoms are rearranged")
        self.play(FadeIn(a, shift=RIGHT * 0.3), FadeIn(eq[0:3]), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(eq[3:6]), run_time=0.6)
        self.at("glucose")
        hexa = RegularPolygon(6, radius=0.85, stroke_color=AMBER, stroke_width=5, fill_color=AMBER, fill_opacity=0.4).move_to(P(-0.4, -0.7))
        hl = T("glucose", 24, AMBER, weight=BOLD).move_to(hexa)
        sub = T("C6H12O6", 24, AMBER).move_to(P(-0.4, -1.95))
        self.play(GrowFromCenter(hexa), FadeIn(hl), run_time=0.8)
        self.play(FadeIn(sub), FadeIn(eq[6]), run_time=0.5)
        self.at("a sugar with six carbon atoms")
        self.play(Indicate(VGroup(hexa, hl), color=AMBER, scale_factor=1.08), run_time=1.2)
        tg = T("net count only: the net equation is not an atom map", 22, GREY).move_to(P(0, -3.65))
        self.add(tg)
        self.at("six molecules of oxygen gas")
        o2 = []
        for i in range(6):
            c = chip("O2", RED, 28).move_to(P(1.0 + 1.1 * (i % 3), -0.3 - 0.9 * (i // 3) + 0.0))
            o2.append(c)
        self.play(FadeIn(eq[7:9]), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in o2], lag_ratio=0.2), run_time=1.5)
        self.at("released through the stomata")
        for i, c in enumerate(o2):
            c.t0 = self.clock.get_value() + 0.3 * i
            c.p0 = c.get_center().copy()

        def rise(m, dt):
            k = float(np.clip((self.clock.get_value() - m.t0) / 1.6, 0, 1))
            if k < 0.5:
                u = k / 0.5
                tgt = P(SX, 1.2)
                m.move_to(m.p0 + (tgt - m.p0) * u)
            else:
                u = (k - 0.5) / 0.5
                m.move_to(P(SX, 1.2 + 2.4 * u))
            setop(m, 0.0 if k >= 1 else 1.0)
        for c in o2:
            c.add_updater(rise)
        self.wait(3.0)
        self.finish()


# ----------------------------------------------------------------------------- the stage of the ledger
def group_a(y=0.45):
    box = RoundedRectangle(corner_radius=0.18, width=3.0, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1)
    tx = VGroup(T("6CO2", 30, BLUE, weight=BOLD), T("+", 30), T("6H2O", 30, TEAL, weight=BOLD)).arrange(RIGHT, buff=0.15).move_to(box)
    g = VGroup(box, tx)
    return g.move_to(P(-4.8, y))


def group_b(y_off=0.0):
    hexa = RegularPolygon(6, radius=0.85, stroke_color=AMBER, stroke_width=5, fill_color=AMBER, fill_opacity=0.4).move_to(P(3.4, 0.45))
    hl = T("glucose", 24, AMBER, weight=BOLD).move_to(hexa)
    sub = T("C6H12O6", 24, AMBER).move_to(P(3.4, -0.65))
    o2 = VGroup(*[chip("O2", RED, 28).move_to(P(4.95 + 1.05 * (i % 2), 1.6 - 1.0 * (i // 2))) for i in range(6)])
    g = VGroup(hexa, hl, sub, o2)
    return g.shift(UP * y_off)


class Panel:
    def __init__(self, sc):
        self.v = [ValueTracker(0) for _ in range(6)]   # C in, H in, O in, C out, H out, O out
        self.lock = ValueTracker(0)
        self.sc = sc
        rect = RoundedRectangle(corner_radius=0.2, width=3.5, height=4.1, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(0, 0.9))
        title = T("ATOM TALLY", 26, GOLD, weight=BOLD).move_to(P(0, 2.6))
        hin, hout = T("in", 28, TEXT).move_to(P(-0.1, 2.0)), T("out", 28, TEXT).move_to(P(1.0, 2.0))
        rows = VGroup(*[T(s, 34, TEXT, weight=BOLD).move_to(P(-1.2, y)) for s, y in zip("CHO", (1.2, 0.4, -0.4))])
        self.static = VGroup(rect, title, hin, hout, rows)
        ys = (1.2, 0.4, -0.4)
        self.counters = VGroup()
        for i in range(6):
            x = -0.1 if i < 3 else 1.0
            self.counters.add(always_redraw(lambda i=i, x=x: M(str(int(round(self.v[i].get_value()))), 38,
                              interpolate_color(ManimColor(TEXT), ManimColor(GREEN), self.lock.get_value())).move_to(P(x, ys[i % 3]))))

    def add_all(self):
        self.sc.add(self.static, self.counters)

    def finish_state(self):
        for v, n in zip(self.v, (6, 12, 18, 6, 12, 18)):
            v.set_value(n)
        self.lock.set_value(1)


def check():
    return VMobject(stroke_color=GREEN, stroke_width=9).set_points_as_corners([P(-0.3, -0.85), P(-0.1, -1.05), P(0.3, -0.6)])


class S10Tally(SpokenScene):
    def construct(self):
        world_start(self)
        objs = cell_world(self, vein_on=False)
        chl = objs[2]
        chl.set_fill(GREEN, 0.05).set_stroke(opacity=0.4)
        eq = eq_line()
        tg = T("net count only: the net equation is not an atom map", 22, GREY).move_to(P(0, -3.65))
        a = VGroup(RoundedRectangle(corner_radius=0.18, width=3.0, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1),
                   VGroup(T("6CO2", 30, BLUE, weight=BOLD), T("+", 30), T("6H2O", 30, TEAL, weight=BOLD)).arrange(RIGHT, buff=0.15)).move_to(P(-4.4, -0.7))
        a[1].move_to(a[0])
        hexa = RegularPolygon(6, radius=0.85, stroke_color=AMBER, stroke_width=5, fill_color=AMBER, fill_opacity=0.4).move_to(P(-0.4, -0.7))
        hl = T("glucose", 24, AMBER, weight=BOLD).move_to(hexa)
        sub = T("C6H12O6", 24, AMBER).move_to(P(-0.4, -1.95))
        o2 = VGroup(*[chip("O2", RED, 28).move_to(P(1.0 + 1.1 * (i % 3), -0.3 - 0.9 * (i // 3))) for i in range(6)])
        arrow = Arrow(P(-2.8, -0.7), P(-1.6, -0.7), buff=0, color=TEXT, stroke_width=6)
        self.add(eq, tg, a, hexa, hl, sub, o2, arrow)
        # now count: the cell world gives way to the ledger
        ga, gb = group_a(), group_b()
        self.play(FadeOut(VGroup(*objs)), FadeOut(arrow),
                  a.animate.move_to(ga.get_center()),
                  VGroup(hexa, hl).animate.move_to(P(3.4, 0.45)), sub.animate.move_to(P(3.4, -0.65)),
                  *[o2[i].animate.move_to(gb[3][i].get_center()) for i in range(6)], run_time=1.2)
        pn = Panel(self)
        self.play(FadeIn(pn.static, scale=0.95), run_time=0.7)
        pn.add_all()
        bobs = [a, VGroup(hexa, hl, sub, o2)]
        for k, b in enumerate(bobs):
            b.base = b.get_center().copy()
            b.add_updater(lambda m, dt, k=k: m.move_to(m.base + UP * 0.05 * np.sin(1.6 * self.clock.get_value() + k)))
        self.at("going in")
        ringa = SurroundingRectangle(a, color=GOLD, buff=0.15, stroke_width=4)
        self.play(Create(ringa), run_time=0.5)
        self.at("six carbon")
        self.play(pn.v[0].animate.set_value(6), run_time=0.9, rate_func=linear)
        self.at("twelve hydrogen")
        self.play(pn.v[1].animate.set_value(12), run_time=0.9, rate_func=linear)
        self.at("eighteen oxygen")
        self.play(pn.v[2].animate.set_value(18), run_time=1.0, rate_func=linear)
        self.at("coming out")
        ringb = SurroundingRectangle(bobs[1], color=GOLD, buff=0.2, stroke_width=4)
        self.play(ReplacementTransform(ringa, ringb), run_time=0.5)
        self.play(pn.v[3].animate.set_value(6), pn.v[4].animate.set_value(12), pn.v[5].animate.set_value(18), run_time=0.9, rate_func=linear)
        self.at("exactly the same")
        self.play(pn.lock.animate.set_value(1), run_time=0.6)
        self.at("no atom is made")
        self.play(Indicate(pn.counters[0:3], color=GREEN, scale_factor=1.25), run_time=1.0)
        self.at("none is destroyed")
        self.play(Indicate(pn.counters[3:6], color=GREEN, scale_factor=1.25), run_time=1.0)
        self.at("conservation of matter")
        ck = check()
        cl = T("conservation of matter:", 28, GREEN, weight=BOLD).move_to(P(0, -1.6))
        cl2 = T("atoms are rearranged,\nnot made or destroyed", 28, TEXT, line_spacing=0.9).move_to(P(0, -2.45))
        self.play(Create(ck), FadeOut(ringb), run_time=0.6)
        self.play(FadeIn(cl, shift=UP * 0.1), FadeIn(cl2, shift=UP * 0.1), run_time=0.8)
        self.finish()


def ledger_base(sc, locked=True, with_check=True):
    pn = Panel(sc)
    pn.finish_state()
    pn.add_all()
    ga = group_a()
    gb = group_b()
    sc.add(ga, gb)
    sc.ck = check()
    if with_check:
        sc.add(sc.ck)
    return pn, ga, gb


def bracket_b(gb):
    return RoundedRectangle(corner_radius=0.25, width=4.35, height=3.15, stroke_color=GREY, stroke_width=4, fill_opacity=0).set_stroke(opacity=0.9).move_to(P(4.48, 0.55))


def spring(x0, x1, y, amp=0.3, coils=9):
    pts = [P(x0, y)]
    n = coils * 2
    for i in range(1, n):
        pts.append(P(x0 + (x1 - x0) * i / n, y + (amp if i % 2 else -amp)))
    pts.append(P(x1, y))
    m = VMobject(stroke_color=GOLD, stroke_width=6)
    m.set_points_as_corners(pts)
    return m


class S11Light(SpokenScene):
    def construct(self):
        world_start(self)
        pn, ga, gb = ledger_base(self)
        P0, P1, P2, PM = P(-6.3, -2.2), P(-2.4, -1.45), P(2.1, -1.75), P(1.0, -3.9)
        u = ValueTracker(0)

        def ray_mk(i):
            miss = i in (1, 3)

            def mk():
                lag = 0.12 * i
                uu = u.get_value() - lag
                if uu < 0:
                    return VMobject()
                if uu <= 1:
                    h, d = P0 + (P1 - P0) * uu, P1 - P0
                else:
                    tgt = PM if miss else P2
                    k = min(uu - 1, 1)
                    h, d = P1 + (tgt - P1) * k, tgt - P1
                d = d / np.linalg.norm(d)
                op = 1.0
                if uu > 1 and miss:
                    op = max(0, 1 - 1.2 * (uu - 1))
                if uu > 1.0 and not miss:
                    op = 1.0 if uu < 1.95 else max(0, 1 - 6 * (uu - 1.95))
                ln = Line(h - d * 0.8, h, stroke_color=YELLOW, stroke_width=7, stroke_opacity=op)
                ln.shift(UP * 0.0)
                return ln
            return always_redraw(mk)
        rays = VGroup(*[ray_mk(i) for i in range(4)])
        self.add(rays)
        self.play(u.animate.set_value(0.95), run_time=2.0, rate_func=linear)
        self.at("not a single atom")
        st = T("0 atoms", 36, YELLOW, weight=BOLD)
        stamp = VGroup(SurroundingRectangle(st, color=YELLOW, buff=0.15, stroke_width=4, corner_radius=0.1), st).move_to(P(-3.0, -2.55)).rotate(0.06)
        self.play(FadeIn(stamp, scale=1.6), run_time=0.5)
        self.at("light adds energy")
        br = bracket_b(gb)
        bl = T("glucose + oxygen\ntogether", 28, TEXT, line_spacing=0.9).move_to(P(4.45, 2.95))
        sp = spring(2.45, 3.4, -1.75, 0.28, 3)
        self.play(FadeOut(stamp), u.animate.set_value(2.0), run_time=2.4, rate_func=linear)
        self.at("part of that energy")
        nl = tag("not all stored", GREY).move_to(P(-1.0, -3.3))
        self.add(sp)
        sp2 = spring(2.45, 6.6, -1.75, 0.28, 9)
        self.play(FadeIn(nl), Create(br), FadeIn(bl), Transform(sp, sp2), run_time=1.2)
        self.at("stored as chemical energy")
        cl = tag("chemical energy", GOLD, weight=BOLD).move_to(P(4.45, -2.4))
        self.play(FadeIn(cl, shift=UP * 0.1), FadeOut(nl), run_time=0.6)
        self.at("in the new arrangement")
        sub = T("energy held in the\narrangement of atoms", 24, TEXT, line_spacing=0.9).move_to(P(4.45, -3.15))
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S12Spring(SpokenScene):
    def construct(self):
        world_start(self)
        pn, ga, gb = ledger_base(self)
        br = bracket_b(gb)
        bl = T("glucose + oxygen\ntogether", 28, TEXT, line_spacing=0.9).move_to(P(4.45, 2.95))
        sp = spring(2.45, 6.6, -1.75, 0.28, 9)
        cl = tag("chemical energy", GOLD, weight=BOLD).move_to(P(4.45, -2.4))
        sub = T("energy held in the\narrangement of atoms", 24, TEXT, line_spacing=0.9).move_to(P(4.45, -3.15))
        self.add(br, bl, sp, cl, sub)
        FL = -2.7
        # the ledger gives way to two energy bars
        self.at("glucose and oxygen together")
        lb = Rectangle(width=2.6, height=0.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to(P(-4.8, FL + 0.2))
        rb = Rectangle(width=4.4, height=1.55, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to(P(4.45, FL + 0.775))
        sc_tag = T("schematic", 22, GREY).move_to(P(0, -3.5))
        lb_lab = T("carbon dioxide\n+ water", 26, TEXT, line_spacing=0.9).move_to(P(-4.8, -3.2))
        rb_lab = T("glucose + oxygen", 28, TEXT).move_to(P(4.45, -3.2))
        gb_all = VGroup(gb, br, sp)
        for c_ in pn.counters:
            c_.clear_updaters()
        self.play(FadeOut(pn.static), FadeOut(pn.counters), FadeOut(self.ck), FadeOut(bl), FadeOut(cl), FadeOut(sub), run_time=0.8)
        self.play(ga.animate.move_to(P(-4.8, -1.85)), gb_all.animate.shift(UP * 0.9), GrowFromEdge(lb, DOWN), GrowFromEdge(rb, DOWN), run_time=1.3)
        self.play(FadeIn(lb_lab), FadeIn(rb_lab), FadeIn(sc_tag), run_time=0.6)
        self.at("hold more chemical energy")
        self.play(Indicate(rb, color=GOLD, scale_factor=1.05), run_time=1.2)
        self.at("than the carbon dioxide and water")
        arr = Arrow(P(-0.1, FL + 0.4), P(-0.1, FL + 1.55), buff=0, color=YELLOW, stroke_width=8)
        al = tag("light\nenergy", YELLOW, weight=BOLD).move_to(P(1.2, FL + 1.1))
        self.play(GrowArrow(arr), FadeIn(al), run_time=1.4)
        self.at("think of a stretch spring")
        self.play(Indicate(sp, color=GOLD, scale_factor=1.12), run_time=1.5)
        sp3 = spring(2.45, 6.6, -0.85, 0.28, 11)
        self.play(Transform(sp, sp3), run_time=1.5, rate_func=there_and_back)
        self.finish()


# ----------------------------------------------------------------------------- wood and pie
class S13Wood(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0)
        ls = scale_static(LX)
        self.add(ls, needle(LX, lambda: 369), pl.mob)
        win = RoundedRectangle(corner_radius=0.3, width=6.8, height=6.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to(P(3.2, 0.1))
        ring = Circle(radius=0.28, stroke_color=GOLD, stroke_width=4).move_to(P(LX, -0.1))
        con = DashedLine(P(LX + 0.28, -0.1), P(-0.2, 0.1), stroke_color=GOLD, stroke_width=3)
        self.at("back to the willow")
        self.play(Create(ring), Create(con), FadeIn(win), run_time=1.0)
        self.at("the plant links glucose")
        hexes = VGroup(*[RegularPolygon(6, radius=0.36, stroke_color=AMBER, stroke_width=3, fill_color=AMBER, fill_opacity=0.5).move_to(P(1.0 + 1.0 * i, 2.1)) for i in range(6)])
        gl = tag("glucose", AMBER).move_to(P(3.2, 2.85))
        self.play(LaggedStart(*[GrowFromCenter(h) for h in hexes], lag_ratio=0.3), FadeIn(gl), run_time=1.6)
        self.at("long chains of cellulose")
        links = VGroup(*[Line(hexes[i].get_right(), hexes[i + 1].get_left(), stroke_color=AMBER, stroke_width=6) for i in range(5)])
        cl = tag("cellulose", AMBER, weight=BOLD).move_to(P(3.2, 1.3))
        self.play(Create(links), Transform(gl, cl), run_time=1.4)
        self.at("the tough fiber of cell walls")
        fibres = VGroup()
        for y in (0.7, 0.2, -0.3, -0.8):
            f = VGroup(Line(P(1.0, y), P(6.0, y), stroke_color=AMBER, stroke_width=6), *[Dot(P(1.0 + i, y), radius=0.08, color=AMBER) for i in range(6)])
            fibres.add(f)
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.3) for f in fibres], lag_ratio=0.25), run_time=1.2)
        band = RoundedRectangle(corner_radius=0.15, width=5.4, height=2.1, stroke_color=AMBER, stroke_width=4).move_to(P(3.5, -0.05))
        wl = tag("cell wall", AMBER, weight=BOLD).move_to(P(3.5, -1.5))
        self.play(Create(band), FadeIn(wl), run_time=0.8)
        self.at("wood is mostly cell walls")
        grid = VGroup()
        for r in range(4):
            for c in range(3):
                grid.add(RoundedRectangle(corner_radius=0.12, width=1.9, height=1.0, stroke_color=AMBER, stroke_width=6, fill_color=BLUE, fill_opacity=0.0).move_to(P(1.45 + 2.0 * c, 1.7 - 1.2 * r)))
        wd = tag("wood: mostly cell walls", WOODC if False else "#D8B07A", size=28, weight=BOLD).move_to(P(3.2, -2.68))
        self.play(FadeOut(VGroup(hexes, links, gl, fibres, band, wl)), FadeIn(grid), FadeIn(wd), run_time=1.4)
        self.at("so most of the trunk's")
        self.play(Indicate(grid, color=AMBER, scale_factor=1.03), run_time=1.5)
        self.at("built from carbon dioxide")
        threads = VGroup()
        for c in grid:
            cx, cy = c.get_center()[0], c.get_center()[1]
            threads.add(Line(P(cx - 0.7, cy - 0.35), P(cx + 0.7, cy + 0.35), stroke_color=TEAL, stroke_width=2.5))
            threads.add(Line(P(cx - 0.7, cy + 0.1), P(cx + 0.7, cy + 0.7 - 0.3), stroke_color=TEAL, stroke_width=2.5))
        bl = tag("carbon from CO2", BLUE, size=28, weight=BOLD).move_to(P(3.2, 2.72))
        self.play(*[c.animate.set_fill(BLUE, 0.5) for c in grid], FadeOut(wd), FadeIn(bl), run_time=1.6)
        self.at("and water")
        tl = tag("hydrogen from water", TEAL, size=28, weight=BOLD).move_to(P(3.2, -2.68))
        self.play(LaggedStart(*[Create(t) for t in threads], lag_ratio=0.02), FadeIn(tl), run_time=1.3)
        self.finish()


class S14Pie(SpokenScene):
    def construct(self):
        world_start(self)
        pl = Plant(self, g=1.0, dry=1.0)
        left_world(self, pl)
        q = corner_q()
        self.add(q, schematic_tag())
        ring = pie_ring()
        self.add(ring)
        self.at("most of its dry mass")
        blue = Circle(radius=PIE_R, stroke_width=0, fill_color=BLUE, fill_opacity=0.0).move_to(PIE_C)
        self.add(blue)
        bl = tag("from carbon dioxide\nin the air", BLUE, weight=BOLD).move_to(P(0.7, 1.7), aligned_edge=LEFT)
        lb = Line(P(0.55, 1.5), PIE_C + P(PIE_R * 0.75, PIE_R * 0.55), stroke_color=BLUE, stroke_width=3)
        self.play(blue.animate.set_fill(BLUE, 0.5), FadeIn(bl, shift=LEFT * 0.2), Create(lb), run_time=1.6)
        self.at("water supplied the hydrogen")
        thr = VGroup()
        for i in range(14):
            yy = PIE_C[1] - 2.0 + i * 0.3
            hw = np.sqrt(max(PIE_R ** 2 - (yy - PIE_C[1]) ** 2, 0.01)) * 0.92
            thr.add(Line(P(PIE_C[0] - hw, yy), P(PIE_C[0] + hw, yy + 0.12), stroke_color=TEAL, stroke_width=2.5))
        hl = tag("hydrogen from water", TEAL, weight=BOLD).move_to(P(0.7, 0.2), aligned_edge=LEFT)
        lh = Line(P(0.55, 0.2), PIE_C + P(PIE_R * 0.9, -0.2), stroke_color=TEAL, stroke_width=3)
        self.play(LaggedStart(*[Create(t) for t in thr], lag_ratio=0.05), FadeIn(hl, shift=LEFT * 0.2), Create(lh), run_time=1.6)
        self.at("only a small essential share")
        wedge = Sector(radius=PIE_R, angle=0.38, start_angle=-0.55, fill_color=SOIL, fill_opacity=1, stroke_width=0, arc_center=PIE_C)
        sl = tag("soil minerals", "#C9A27A", weight=BOLD).move_to(P(0.7, -1.4), aligned_edge=LEFT)
        ls_ = Line(P(0.55, -1.4), PIE_C + P(PIE_R * 0.92 * np.cos(-0.36), PIE_R * 0.92 * np.sin(-0.36)), stroke_color="#C9A27A", stroke_width=3)
        self.play(FadeIn(wedge, scale=1.3), FadeIn(sl, shift=LEFT * 0.2), Create(ls_), run_time=1.0)
        pt = T("schematic, not to scale", 22, GREY).move_to(P(1.5, -2.3))
        self.add(pt)
        self.at("the soil")
        self.play(FadeOut(q), run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "A plant is built mostly from air and water, powered by light."
