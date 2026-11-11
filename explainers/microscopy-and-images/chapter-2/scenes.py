"""What an Overlap Can Claim (chapter 2) — microscopy-and-images teaching film.

COLOR MAP (same as chapter 1)
  GREEN  fluorescent sources / green channel / the resolution scale
  BLUE   objective and optical elements, antibodies
  YELLOW distances, controls, questions, the overlap patch
  RED    red channel, warnings, things that cannot be claimed
  TEXT   detector sums and conclusions
  GREY   cell, detector, de-emphasised structure

The bench is schematic. The intensity trace in the record scene is a seeded Poisson
simulation, marked "simulated". The ellipsoid is an order-of-magnitude cartoon.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

LENS_X = -0.8
CELL_X = -5.15
DET_X, DET_Y = 3.8, -0.55
ELL_X, ELL_Y, ELL_W, ELL_H = -1.6, -0.5, 2.2, 5.2
CHIP_Y = 3.3
CHIP_XS = (-5.15, 0.45, 3.8)


# ---------------------------------------------------------------- helpers
def bracket(a, b, label, color=YELLOW, vertical=False, size=28):
    line = Line(a, b, color=color, stroke_width=4)
    if vertical:
        ticks = VGroup(Line(a + LEFT * .13, a + RIGHT * .13, color=color, stroke_width=4),
                       Line(b + LEFT * .13, b + RIGHT * .13, color=color, stroke_width=4))
        text = M(label, size, color).next_to(line, LEFT, buff=.18)
    else:
        ticks = VGroup(Line(a + DOWN * .13, a + UP * .13, color=color, stroke_width=4),
                       Line(b + DOWN * .13, b + UP * .13, color=color, stroke_width=4))
        text = M(label, size, color).next_to(line, UP, buff=.16)
    return VGroup(line, ticks, text)


def light_packets(ys, colors, start=-4.6, end=-1.35):
    group = VGroup()
    for row, (y, col) in enumerate(zip(ys, colors)):
        for i in range(4):
            d = Dot([start + i * (end - start) / 4, y, 0], radius=.055, color=col).set_opacity(.7)

            def drift(m, dt, lo=start, hi=end, v=.38 + .035 * row):
                m.shift(RIGHT * v * dt)
                if m.get_x() > hi:
                    m.set_x(lo)
            d.add_updater(drift)
            group.add(d)
        xs = np.linspace(start, end, 90)
        ripple = VMobject(stroke_color=col, stroke_width=9, stroke_opacity=.7)
        ripple.phase = row * np.pi / 2

        def motion(m, dt, xs=xs, y=y):
            m.phase += 14.0 * dt
            m.set_points_as_corners([[x, y + .2 * np.sin(7.2 * x - m.phase), 0] for x in xs])
        ripple.add_updater(motion)
        motion(ripple, 0)
        group.add(ripple)
    return group


class World:
    """The carried bench: cell with a green mitochondrion outline and red dots, objective, detector."""

    def __init__(self, sep=.9, show_images=True, vis=1.0):
        self.cell = Ellipse(width=2.35, height=5.45, color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=.16).move_to([CELL_X, -.25, 0])
        mito = RoundedRectangle(corner_radius=.31, width=.62, height=2.0, color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=.12).move_to([CELL_X, .45, 0])
        cristae = VGroup(*[Line([CELL_X - .17, y, 0], [CELL_X + .17, y, 0], color=GREEN, stroke_width=3)
                           for y in (-.15, .45, 1.05)])
        reds = VGroup(*[Dot([CELL_X + dx, y, 0], radius=.07, color=RED) for dx, y in
                        ((-.75, 1.5), (.7, 1.1), (-.8, -.3), (.65, -.1), (-.4, -1.3), (.5, -1.6),
                         (-.45, 2.0), (.45, 2.0), (-.7, -1.9))])
        self.mito = VGroup(mito, cristae)
        self.reds = reds
        self.lens = Ellipse(width=.78, height=4.65, color=BLUE, stroke_width=5,
                            fill_color=BLUE, fill_opacity=.16).move_to([LENS_X, -.15, 0])
        self.lens_label = T("objective", 28, BLUE).next_to(self.lens, DOWN, buff=.18)
        self.det = RoundedRectangle(corner_radius=.16, width=5.15, height=4.35, color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=.17).move_to([DET_X, DET_Y, 0])
        self.det_label = T("detector", 28, GREY).move_to([DET_X, 1.9, 0])
        self.tag = T("SCHEMATIC", 22, TEXT).move_to([CELL_X, -3.4, 0])
        self.static = VGroup(self.cell, self.mito, self.reds, self.lens, self.lens_label,
                             self.det, self.det_label, self.tag)
        self.light = light_packets((.45, -1.0), (GREEN, RED))
        self.g = Circle(.95, stroke_width=0, fill_color=GREEN, fill_opacity=.38).move_to([DET_X - sep / 2, DET_Y, 0])
        self.r = Circle(.95, stroke_width=0, fill_color=RED, fill_opacity=.38).move_to([DET_X + sep / 2, DET_Y, 0])
        self.vis = ValueTracker(vis)
        self.patch = Ellipse(width=1, height=1, stroke_width=0, fill_color=YELLOW, fill_opacity=.6)
        self.patch.tt = 0

        def upd(m, dt):
            m.tt += dt
            s = self.r.get_x() - self.g.get_x()
            ov = max(1.9 - s, .02)
            hh = 2 * np.sqrt(max(.95 ** 2 - (s / 2) ** 2, 1e-4))
            m.become(Ellipse(width=ov, height=hh, stroke_width=0, fill_color=YELLOW,
                             fill_opacity=self.vis.get_value() * (.62 + .16 * np.sin(2.2 * m.tt))))
            m.move_to([(self.g.get_x() + self.r.get_x()) / 2, DET_Y, 0])
        self.patch.add_updater(upd)
        upd(self.patch, 0)
        self.images = VGroup(self.g, self.r, self.patch)
        self.all = VGroup(self.static, self.light, self.images)

    def add_to(self, scene):
        scene.add(self.all)
        return self

    def calm(self):
        self.patch.clear_updaters()


def chain_chips(active=None, labels=("label", "channels", "record")):
    chips = VGroup()
    for x, lab in zip(CHIP_XS, labels):
        c = chip(lab, YELLOW, 30).move_to([x, CHIP_Y, 0])
        chips.add(c)
    links = VGroup(Line(chips[0].get_right(), chips[1].get_left(), color=YELLOW, stroke_width=4),
                   Line(chips[1].get_right(), chips[2].get_left(), color=YELLOW, stroke_width=4))
    g = VGroup(chips, links)
    g.chips, g.links = chips, links
    if active is not None:
        for i, c in enumerate(chips):
            c.set_opacity(1 if i == active else .35)
        links.set_opacity(.35)
    return g


def filter_block():
    top = Rectangle(width=.5, height=1.1, color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=.4)
    bot = Rectangle(width=.5, height=1.1, color=RED, stroke_width=3, fill_color=RED, fill_opacity=.4)
    return VGroup(top, bot).arrange(DOWN, buff=0).move_to([CHIP_XS[1], -.15, 0])


def ellipsoid(cx=ELL_X, cy=ELL_Y, w=ELL_W, h=ELL_H, color=GREEN, op=.12):
    layers = VGroup(*[Ellipse(width=w * s, height=h * s, stroke_width=0, fill_color=color, fill_opacity=op)
                      for s in (1.0, .82, .64, .46, .28)])
    rim = Ellipse(width=w, height=h, color=color, stroke_width=3, stroke_opacity=.75)
    ring = Ellipse(width=w, height=w * .28, color=color, stroke_width=2, stroke_opacity=.4)
    g = VGroup(layers, rim, ring).move_to([cx, cy, 0])
    g.layers = layers
    return g


def drifters(n_g=4, n_r=3, cx=ELL_X, cy=ELL_Y, amp=1.0, seed=1):
    rng = np.random.RandomState(seed)
    out = VGroup()
    for i in range(n_g + n_r):
        d = Dot(radius=.11, color=GREEN if i < n_g else RED)
        ph = rng.uniform(0, 6.28, 2)
        fr = rng.uniform(.5, 1.1, 2) * .7
        bx, by = rng.uniform(-.3, .3), rng.uniform(-.6, .6)
        d.t = rng.uniform(0, 5)

        def upd(m, dt, ph=ph, fr=fr, bx=bx, by=by):
            m.t += dt
            m.move_to([cx + bx + .33 * amp * np.sin(fr[0] * m.t + ph[0]),
                       cy + by + .9 * amp * np.sin(fr[1] * m.t + ph[1]), 0])
        upd(d, 0)
        d.add_updater(upd)
        out.add(d)
    return out


def volume_picture(brackets=True, labels=True):
    """Ellipsoid scene state carried through chapter 2 (same place every time)."""
    ell = ellipsoid()
    dots = drifters()
    out = VGroup(ell, dots)
    out.ell, out.dots = ell, dots
    if brackets:
        top = ELL_Y + ELL_H / 2
        hb = bracket(np.array([ELL_X - ELL_W / 2, top + .5, 0]), np.array([ELL_X + ELL_W / 2, top + .5, 0]),
                     "about 230 nm")
        vb = bracket(np.array([ELL_X - ELL_W / 2 - .5, ELL_Y - ELL_H / 2, 0]),
                     np.array([ELL_X - ELL_W / 2 - .5, top, 0]), "about 800 nm", vertical=True)
        dep = VGroup(Arrow([ELL_X + 1.5, ELL_Y - 1.9, 0], [ELL_X + 1.5, ELL_Y + 1.9, 0], buff=0, color=YELLOW,
                           stroke_width=5, tip_length=.25),
                     T("depth", 30, YELLOW).move_to([ELL_X + 2.5, ELL_Y, 0]))
        out.hb, out.vb, out.dep = hb, vb, dep
    if labels:
        out.rs = T("resolution scale", 34, GREEN, weight=BOLD).move_to([4.0, 1.5, 0])
        out.sch = T("schematic, not a boundary", 24, TEXT).move_to([4.0, .85, 0])
    return out


# ---------------------------------------------------------------- scenes
class S01Hook(SpokenScene, TitleCard):
    LESSON = "Microscopy and Images"
    TITLE = "What an Overlap Can Claim"

    def construct(self):
        w = World(sep=3.4, vis=0)
        w.g.set_x(DET_X - 1.9)
        w.r.set_x(DET_X + 1.9)
        self.add(w.static, w.light, w.images)
        self.play(w.g.animate.set_x(DET_X - .45), w.r.animate.set_x(DET_X + .45), run_time=1.9)
        self.play(w.vis.animate.set_value(1), run_time=.5)
        self.at("does the yellow patch")
        q = T("Do they bind?", 46, YELLOW, weight=BOLD).move_to([DET_X + .6, 2.9, 0])
        self.play(FadeIn(q, shift=UP * .6), run_time=1.1)
        self.play(Indicate(w.patch, color=YELLOW, scale_factor=1.2), run_time=1.2)
        self.at("chapter one")
        self.play(w.g.animate.set_x(DET_X - .8), w.r.animate.set_x(DET_X + .8), run_time=1.4)
        self.play(w.g.animate.set_x(DET_X - .1), w.r.animate.set_x(DET_X + .1), run_time=1.4)
        self.play(w.g.animate.set_x(DET_X - .45), w.r.animate.set_x(DET_X + .45), run_time=1.2)
        self.at("now follow")
        self.play(FadeOut(q), run_time=.5)
        arrow = Arrow([-4.3, 2.55, 0], [2.2, 2.55, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=.26)
        lab = T("label", 32, YELLOW, weight=BOLD).move_to([-5.3, 2.55, 0])
        self.play(FadeIn(lab), GrowArrow(arrow), run_time=1.2)
        clm = T("claim", 32, YELLOW, weight=BOLD).move_to([3.2, 2.55, 0])
        self.play(FadeIn(clm), run_time=.9)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        w = World()
        w.add_to(self)
        veil = Rectangle(width=14.3, height=8.2, stroke_width=0, fill_color=BG, fill_opacity=.45)
        title = T("What an Overlap Can Claim", 52, TEXT, font=TITLE_FONT).move_to([0, 2.55, 0])
        fit(title, max_w=12)
        rule = Line([-2.0, 2.0, 0], [2.0, 2.0, 0], color=GOLD, stroke_width=4)
        self.play(FadeIn(veil), FadeIn(title, shift=UP * .15), GrowFromCenter(rule), run_time=.45)
        self.wait(.95)
        self.play(FadeOut(title), FadeOut(rule), FadeOut(veil), run_time=.45)
        self.finish()


class S03Volume(SpokenScene):
    def construct(self):
        w = World()
        w.add_to(self)
        pix = Square(.3, color=YELLOW, stroke_width=4).move_to([DET_X, DET_Y, 0])
        self.play(Create(pix), run_time=.8)
        vp = volume_picture()
        ell = vp.ell
        ell.scale(.04).move_to([DET_X, DET_Y, 0])
        self.at("from chapter one")
        w.calm()
        self.add(ell)
        self.play(FadeOut(w.all), FadeOut(pix),
                  ell.animate.scale(25).move_to([ELL_X, ELL_Y, 0]), run_time=2.2)
        self.play(FadeIn(vp.dots), run_time=.8)
        self.at("across the image")
        self.play(Create(vp.hb), run_time=1.0)
        self.at("about 230")
        self.play(Indicate(vp.hb[2], color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.at("along the depth direction")
        self.play(Create(vp.vb), GrowArrow(vp.dep[0]), FadeIn(vp.dep[1]), run_time=1.5)
        self.at("about 800")
        self.play(Indicate(vp.vb[2], color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.at("a yellow pixel alone")
        self.play(FadeIn(vp.rs), FadeIn(vp.sch), run_time=1.0)
        px = Square(.32, stroke_width=0, fill_color=YELLOW, fill_opacity=.9).move_to([ELL_X, ELL_Y, 0])
        self.play(FadeIn(px, scale=.5), run_time=.8)
        self.at("closer than this scale")
        self.play(Indicate(ell, color=YELLOW, scale_factor=1.06), run_time=1.3)
        self.finish()


class S03ChannelScale(SpokenScene):
    def construct(self):
        vp = volume_picture()
        px = Square(.32, stroke_width=0, fill_color=YELLOW, fill_opacity=.9).move_to([ELL_X, ELL_Y, 0])
        self.add(vp, vp.hb, vp.vb, vp.dep, vp.rs, vp.sch, px)
        self.play(Indicate(vp.ell, color=GREEN, scale_factor=1.05), run_time=1.0)
        gl = T("green light", 30, GREEN).move_to([4.0, .2, 0])
        self.play(FadeIn(gl), run_time=.7)
        self.at("a red channel")
        red = ellipsoid(color=RED, op=.05)
        red.set_z_index(-1)
        self.play(FadeIn(red), run_time=.5)
        self.at("longer emission wavelength")
        lw = T("longer wavelength", 30, RED).move_to([4.0, -.6, 0])
        self.play(red.animate.scale(1.12), FadeIn(lw), run_time=1.6)
        self.at("larger blur")
        self.play(Indicate(red, color=RED, scale_factor=1.04), run_time=1.2)
        self.at("two color claim")
        badge = chip("measure each channel", YELLOW, 42, pad=.35).move_to([0.5, 0, 0])
        badge.set_z_index(5)
        self.play(FadeOut(VGroup(vp, vp.hb, vp.vb, vp.dep, vp.rs, vp.sch, px, red, gl, lw)),
                  FadeIn(badge, scale=.8), run_time=1.2)
        self.at("use the measured resolution")
        self.play(badge.animate.scale(1.12), run_time=1.5)
        self.play(Indicate(badge, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.finish()


def cards():
    cs = VGroup(chip("a handful", YELLOW, 34), chip("a few hundred", YELLOW, 34),
                chip("tens of thousands", YELLOW, 34))
    for c, y in zip(cs, (1.0, -.3, -1.6)):
        c.move_to([4.0, y, 0])
    return cs


class S04Predict(SpokenScene):
    def construct(self):
        vp = volume_picture(brackets=False, labels=False)
        self.add(vp)
        q = T("HOW MANY INSIDE?", 48, TEXT, weight=BOLD).move_to([1.8, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN * .2), Indicate(vp.ell, color=YELLOW, scale_factor=1.04), run_time=1.4)
        self.at("at typical cellular")
        dens = chip("typical cellular density", TEAL, 28).move_to([4.0, 2.0, 0])
        self.play(FadeIn(dens, shift=LEFT * .2), run_time=.9)
        self.at("this volume")
        self.play(Indicate(vp.ell, color=YELLOW, scale_factor=1.06), run_time=1.4)
        cs = cards()
        self.at("a handful")
        self.play(FadeIn(cs[0], shift=LEFT * .6), run_time=.7)
        self.at("a few hundred")
        self.play(FadeIn(cs[1], shift=LEFT * .6), run_time=.7)
        self.at("tens of thousands")
        self.play(FadeIn(cs[2], shift=LEFT * .6), run_time=.7)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        vp = volume_picture(brackets=False, labels=False)
        q = T("HOW MANY INSIDE?", 48, TEXT, weight=BOLD).move_to([1.8, 3.05, 0])
        dens = chip("typical cellular density", TEAL, 28).move_to([4.0, 2.0, 0])
        self.add(vp, q, dens, cards())
        self.play(Indicate(q, color=YELLOW, scale_factor=1.04), run_time=1.5)
        self.finish()


class S06Count(SpokenScene):
    def construct(self):
        vp = volume_picture(brackets=False, labels=False)
        q = T("HOW MANY INSIDE?", 48, TEXT, weight=BOLD).move_to([1.8, 3.05, 0])
        dens = chip("typical cellular density", TEAL, 28).move_to([4.0, 2.0, 0])
        cs = cards()
        self.add(vp, q, dens, cs)
        self.play(FadeOut(q), run_time=.6)
        self.at("ellipsoid")
        self.play(Indicate(vp.ell, color=YELLOW, scale_factor=1.06), run_time=1.3)
        self.at("its volume")
        badge1 = chip("about 0.02\ncubic micrometres", YELLOW, 32).move_to([4.0, 1.0, 0])
        self.play(FadeOut(cs[0]), FadeOut(cs[1]), FadeOut(dens),
                  cs[2].animate.move_to([4.0, -1.2, 0]).set_opacity(.35), FadeIn(badge1, shift=DOWN * .2),
                  run_time=1.2)
        self.at("roughly")
        est = T("order-of-magnitude estimate", 26, TEXT).move_to([3.4, -2.9, 0])
        sch = T("schematic", 24, TEXT).move_to([-1.6, -3.4, 0])
        self.play(FadeIn(est), FadeIn(sch), run_time=.8)
        self.at("at typical cellular")
        dens2 = chip("typical cellular density", TEAL, 28).move_to([4.0, -0.2, 0])
        self.play(FadeIn(dens2, shift=LEFT * .2), run_time=.8)
        self.at("tens of thousands")
        badge2 = chip("tens of thousands,\ncellular density", TEXT, 34).move_to([4.0, -1.5, 0])
        self.play(FadeOut(cs[2]), FadeOut(dens2), FadeIn(badge2, scale=.9),
                  *[l.animate.set_fill(opacity=.2) for l in vp.ell.layers], run_time=1.6)
        self.play(Indicate(badge2, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.finish()


class S06Reveal(SpokenScene):
    def construct(self):
        ell = ellipsoid()
        for l in ell.layers:
            l.set_fill(opacity=.2)
        g = Dot(radius=.13, color=GREEN).move_to([ELL_X - .35, ELL_Y + 1.3, 0])
        r = Dot(radius=.13, color=RED).move_to([ELL_X + .35, ELL_Y - 1.3, 0])
        for d, ph in ((g, 0), (r, 2)):
            d.base = d.get_center().copy()
            d.t = ph

            def upd(m, dt):
                m.t += dt
                m.move_to(m.base + np.array([.08 * np.sin(m.t), .12 * np.cos(.8 * m.t), 0]))
            d.add_updater(upd)
        self.add(ell, g, r)
        badge = chip("in-focus", YELLOW, 38).move_to([4.2, 2.3, 0])
        pix = Square(1.2, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=.55).move_to([4.2, -.6, 0])
        pixl = T("yellow pixel", 28, YELLOW).next_to(pix, DOWN, buff=.2)
        self.play(FadeIn(badge), FadeIn(pix), FadeIn(pixl), run_time=1.2)
        self.at("in focus overlap")
        self.play(Indicate(pix, color=YELLOW, scale_factor=1.1), run_time=1.5)
        self.at("within about this volume")
        self.play(Indicate(ell, color=YELLOW, scale_factor=1.06), run_time=1.6)
        self.at("it does not say")
        line = DashedLine(g.get_center(), r.get_center(), color=TEXT, stroke_width=4)
        line.add_updater(lambda m: m.become(DashedLine(g.get_center(), r.get_center(), color=TEXT, stroke_width=4)))
        nt = T("not touching", 32, TEXT, weight=BOLD).move_to([1.4, ELL_Y, 0])
        self.add(line)
        self.play(FadeIn(nt, shift=LEFT * .2), run_time=1.0)
        self.at("in widefield")
        haze = VGroup(*[Circle(.42, stroke_width=0, fill_color=GREEN, fill_opacity=.28)
                        .move_to([ELL_X + dx, y, 0]) for dx, y in ((-.3, 3.5), (.4, 3.1), (0, -3.5), (.5, -3.3))])
        wf = chip("widefield haze", GREEN, 38).move_to([4.2, 2.3, 0])
        self.play(FadeOut(nt), ReplacementTransform(badge, wf),
                  *[h.animate.move_to([ELL_X, ELL_Y + (.2 if h.get_y() > 0 else -.2), 0]) for h in haze],
                  FadeIn(haze), run_time=2.2)
        self.at("out of focus haze")
        self.play(pix.animate.set_fill(opacity=.95).scale(1.12), haze.animate.set_opacity(.1), run_time=1.6)
        self.at("apparent overlap")
        self.play(Indicate(pix, color=YELLOW, scale_factor=1.15), run_time=1.5)
        self.finish()


class S07Chain(SpokenScene):
    def construct(self):
        ell = ellipsoid()
        for l in ell.layers:
            l.set_fill(opacity=.2)
        w = World(vis=0)
        self.add(ell)
        self.wait(.3)
        self.add(w.images)
        self.play(ell.animate.scale(.04).move_to([DET_X, DET_Y, 0]).set_opacity(0),
                  FadeIn(w.static), FadeIn(w.light), w.vis.animate.set_value(1), run_time=1.8)
        self.at("color overlap is a claim")
        claim = chip("claim", YELLOW, 30).move_to([DET_X, -3.3, 0])
        cl = Line([DET_X, DET_Y - .85, 0], claim.get_top(), color=YELLOW, stroke_width=4)
        self.play(FadeIn(claim, shift=UP * .2), Create(cl), run_time=1.0)
        self.at("each link")
        ch = chain_chips()
        fb = filter_block()
        drops = VGroup(Line([CHIP_XS[0], CHIP_Y - .4, 0], [CHIP_XS[0], 2.5, 0], color=YELLOW, stroke_width=3),
                       Line([CHIP_XS[1], CHIP_Y - .4, 0], [CHIP_XS[1], fb.get_top()[1], 0], color=YELLOW, stroke_width=3),
                       Line([CHIP_XS[2], CHIP_Y - .4, 0], [CHIP_XS[2], 2.2, 0], color=YELLOW, stroke_width=3))
        self.play(FadeIn(fb), LaggedStart(*[FadeIn(c, shift=DOWN * .2) for c in ch.chips], lag_ratio=.4),
                  Create(drops), Create(ch.links), run_time=2.2)
        self.at("check three links")
        pulse = Dot(radius=.16, color=YELLOW).move_to([CHIP_XS[0], CHIP_Y, 0])
        pulse.set_z_index(10)
        path = VMobject().set_points_as_corners([[CHIP_XS[0], CHIP_Y, 0], [CHIP_XS[2], CHIP_Y, 0],
                                                 [CHIP_XS[2], -3.3, 0]])
        self.play(MoveAlongPath(pulse, path), run_time=2.6)
        self.play(Indicate(claim, color=YELLOW, scale_factor=1.12), run_time=.8)
        self.finish()


def tracker(active):
    ch = chain_chips(active)
    return ch


def blank_panel(w, h, color=GREY):
    return RoundedRectangle(corner_radius=.15, width=w, height=h, color=color, stroke_width=3,
                            fill_color=GREY, fill_opacity=.25)


class S08Label(SpokenScene):
    def construct(self):
        w = World()
        ch = chain_chips()
        fb = filter_block()
        w.add_to(self)
        self.add(ch, fb)
        self.play(*[c.animate.set_opacity(.35) for c in ch.chips[1:]], ch.links.animate.set_opacity(.35),
                  FadeOut(w.all), FadeOut(fb), run_time=1.2)
        w.calm()
        tgt = VGroup(Rectangle(width=2.8, height=.9, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.4),
                     T("target", 28, TEXT)).move_to([-3.0, -1.7, 0])
        tgt[1].move_to(tgt[0])
        self.play(FadeIn(tgt, shift=UP * .2), run_time=.8)
        self.at("an antibody")
        p1 = VGroup(RoundedRectangle(corner_radius=.35, width=2.2, height=.8, color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=.35), T("primary", 28, TEXT))
        p1[1].move_to(p1[0])
        p1.move_to([-3.0, 1.3, 0])
        self.play(FadeIn(p1), run_time=.4)
        self.play(p1.animate.move_to([-3.0, -.8, 0]), run_time=1.0)
        self.at("wrong protein")
        wr = VGroup(Rectangle(width=3.0, height=.9, color=RED, stroke_width=3, fill_color=RED, fill_opacity=.25),
                    T("wrong protein", 28, TEXT)).move_to([2.8, -1.7, 0])
        wr[1].move_to(wr[0])
        p2 = p1.copy()
        self.play(FadeIn(wr, shift=UP * .2), run_time=.6)
        self.add(p2)
        self.play(p2.animate.move_to([2.8, -.8, 0]), run_time=1.5)
        sec = VGroup(RoundedRectangle(corner_radius=.35, width=2.4, height=.8, color=GREEN, stroke_width=3,
                                      fill_color=GREEN, fill_opacity=.4), T("secondary", 28, TEXT))
        sec[1].move_to(sec[0])
        sec.move_to([-3.0, .1, 0])
        glow = Circle(1.1, stroke_width=0, fill_color=GREEN, fill_opacity=.12).move_to(sec)
        self.play(FadeIn(sec, shift=DOWN * .3), FadeIn(glow), run_time=1.0)
        self.at("signal loss after knockout")
        diag = VGroup(tgt, p1, wr, p2, sec, glow)
        pl = blank_panel(5.6, 3.8).move_to([-3.4, .1, 0])
        pr = blank_panel(5.6, 3.8).move_to([3.4, .1, 0])
        ql = T("?", 120, TEXT, weight=BOLD).move_to(pl)
        qr = T("?", 120, TEXT, weight=BOLD).move_to(pr)
        for qq in (ql, qr):
            qq.tt = 0

            def br(m, dt):
                m.tt += dt
                m.set_opacity(.45 + .35 * np.sin(2 * m.tt) ** 2)
            qq.add_updater(br)
        tl = T("target knockout", 34, YELLOW, weight=BOLD).move_to([-3.4, 2.5, 0])
        tr = T("secondary only", 34, YELLOW, weight=BOLD).move_to([3.4, 2.5, 0])
        sk = T("schematic", 24, TEXT).move_to([0, -3.3, 0])
        self.play(FadeOut(diag), FadeIn(pl), FadeIn(pr), FadeIn(ql), FadeIn(qr), FadeIn(tl), FadeIn(sk), run_time=1.2)
        self.play(FadeIn(tr), run_time=.6)
        self.at("with knockdown")
        kd = chip("knockdown", YELLOW, 30).move_to([-3.4, -2.3, 0])
        self.play(FadeIn(kd, shift=UP * .2), run_time=.8)
        self.at("verified target reduction")
        kd2 = chip("verified target reduction", YELLOW, 28).move_to([-3.4, -2.3, 0])
        self.play(ReplacementTransform(kd, kd2), Indicate(pl, color=YELLOW, scale_factor=1.03), run_time=1.3)
        self.at("a secondary only sample")
        self.play(Indicate(pr, color=GREEN, scale_factor=1.04), Indicate(tr, color=GREEN), run_time=1.4)
        sb = VGroup(RoundedRectangle(corner_radius=.3, width=2.6, height=.7, color=GREEN, stroke_width=3,
                                     fill_color=GREEN, fill_opacity=.4), T("secondary", 28, TEXT))
        sb[1].move_to(sb[0])
        sb.move_to([3.4, -2.3, 0])
        self.play(FadeIn(sb, shift=UP * .2), run_time=.9)
        self.at("nonspecific signal")
        self.play(Indicate(sb, color=GREEN, scale_factor=1.12), run_time=1.5)
        self.at("fluorescent secondary")
        self.play(Indicate(sb, color=GREEN, scale_factor=1.15), run_time=1.5)
        self.finish()


class S09Channels(SpokenScene):
    def construct(self):
        w = World()
        ch = chain_chips()
        fb = filter_block()
        w.add_to(self)
        self.add(ch, fb)
        self.play(*[c.animate.set_opacity(.35) for c in (ch.chips[0], ch.chips[2])],
                  ch.links.animate.set_opacity(.35), FadeOut(w.all), fb.animate.move_to([-4.4, 0, 0]), run_time=.8)
        w.calm()
        inc = Arrow([-6.6, 0, 0], [-4.7, 0, 0], buff=0, color=TEXT, stroke_width=6, tip_length=.22)
        gb = Line([-4.15, .3, 0], [-1.8, 1.55, 0], color=GREEN, stroke_width=5)
        rb = Line([-4.15, -.3, 0], [-1.8, -1.65, 0], color=RED, stroke_width=5)
        gp = RoundedRectangle(corner_radius=.12, width=4.0, height=2.0, color=GREEN, stroke_width=3,
                              fill_color=GREEN, fill_opacity=.18).move_to([.2, 1.55, 0])
        rp = RoundedRectangle(corner_radius=.12, width=4.0, height=2.5, color=RED, stroke_width=3,
                              fill_color=RED, fill_opacity=.18).move_to([.2, -1.65, 0])
        gt = T("green channel", 30, GREEN).move_to([4.5, 1.55, 0])
        rt = T("red channel", 30, RED).move_to([4.5, -1.65, 0])
        self.play(FadeIn(inc), Create(gb), Create(rb), FadeIn(gp), FadeIn(rp), FadeIn(gt), FadeIn(rt), run_time=1.6)
        self.at("a dye's light")
        leak = Arrow([.2, .55, 0], [.2, -1.0, 0], buff=0, color=GREEN, stroke_width=7, tip_length=.22)
        self.play(GrowArrow(leak), run_time=1.4)
        self.play(ShowPassingFlash(leak.copy().set_stroke(TEXT, 10), time_width=.5), run_time=1.2)
        self.at("that leak is called")
        bt = T("bleed-through", 32, GREEN, weight=BOLD).move_to([4.5, 0, 0])
        self.play(FadeIn(bt, shift=LEFT * .2), Indicate(leak, color=GREEN), run_time=1.3)
        self.at("single label samples")
        samp = VGroup(Ellipse(width=1.2, height=1.6, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.2),
                      Dot(radius=.16, color=GREEN)).move_to([-5.7, 0, 0])
        sl = T("single\nlabel", 26, TEXT).move_to([-5.7, -1.3, 0])
        ghost = Circle(.7, stroke_width=0, fill_color=RED, fill_opacity=.2).move_to([.2, -1.65, 0])
        ml = T("measured leak", 32, GREEN, weight=BOLD).move_to([4.5, 0, 0])
        self.play(FadeOut(inc), ReplacementTransform(leak, ghost), FadeIn(samp), FadeIn(sl),
                  ReplacementTransform(bt, ml), run_time=1.5)
        self.at("multicolor beads")
        offs = [(-1.0, .45), (.3, -.35), (1.2, .4)]
        gbeads = VGroup(*[Dot([.2 + dx, 1.55 + dy, 0], radius=.13, color=GREEN) for dx, dy in offs])
        rbeads = VGroup(*[Dot([.2 + dx, -1.65 + dy, 0], radius=.13, color=RED) for dx, dy in offs])
        redp = VGroup(rp, rbeads, ghost)
        self.play(FadeOut(samp), FadeOut(sl), FadeOut(ml), FadeIn(gbeads), FadeIn(rbeads),
                  FadeOut(ghost), redp.animate.shift(RIGHT * .6), run_time=1.5)
        self.at("whether the channels line up")
        reg = T("registered", 32, YELLOW, weight=BOLD).move_to([4.5, 0, 0])
        self.play(redp.animate.shift(LEFT * .6), FadeIn(reg), run_time=1.5)
        self.at("misregistration")
        off = T("offset", 32, RED, weight=BOLD).move_to([4.5, 0, 0])
        self.play(redp.animate.shift(RIGHT * .6), ReplacementTransform(reg, off), run_time=1.6)
        self.at("or superimpose")
        self.play(redp.animate.shift(LEFT * .3), run_time=1.5)
        self.play(Indicate(rbeads, color=RED), run_time=1.0)
        self.finish()


class S10Record(SpokenScene):
    def construct(self):
        w = World()
        ch = chain_chips()
        fb = filter_block()
        w.add_to(self)
        self.add(ch, fb)
        self.play(*[c.animate.set_opacity(.35) for c in ch.chips[:2]], ch.links.animate.set_opacity(.35),
                  FadeOut(w.all), FadeOut(fb), run_time=1.2)
        w.calm()
        pc = blank_panel(3.8, 3.0).move_to([-3.9, .3, 0])
        pt = blank_panel(3.8, 3.0).move_to([3.9, .3, 0])
        bc = Circle(.75, stroke_width=0, fill_color=GREEN, fill_opacity=.4).move_to(pc)
        bt = Circle(.75, stroke_width=0, fill_color=GREEN, fill_opacity=.4).move_to(pt)
        lc = T("control", 34, TEXT, weight=BOLD).move_to([-3.9, 2.25, 0])
        lt = T("treated", 34, TEXT, weight=BOLD).move_to([3.9, 2.25, 0])
        self.play(FadeIn(VGroup(pc, bc, lc)), FadeIn(VGroup(pt, bt, lt)), run_time=1.0)
        self.at("image every condition")
        dial = Circle(1.0, color=YELLOW, stroke_width=4).move_to([0, .3, 0])
        ticks = VGroup(*[Line(dial.get_center() + .85 * np.array([np.cos(a), np.sin(a), 0]),
                              dial.get_center() + 1.0 * np.array([np.cos(a), np.sin(a), 0]),
                              color=YELLOW, stroke_width=3) for a in np.linspace(3.5, -.35, 9)])
        needle = Line(dial.get_center(), dial.get_center() + .8 * np.array([np.cos(2.4), np.sin(2.4), 0]),
                      color=YELLOW, stroke_width=6)
        con = VGroup(Line([-1.0, .3, 0], [-2.0, .3, 0], color=YELLOW, stroke_width=3),
                     Line([1.0, .3, 0], [2.0, .3, 0], color=YELLOW, stroke_width=3))
        self.play(Create(dial), Create(ticks), Create(con), FadeIn(needle), run_time=.9)
        self.play(Rotate(needle, angle=-.9, about_point=dial.get_center()), run_time=.7)
        self.at("identical settings")
        idl = T("identical settings", 30, YELLOW, weight=BOLD).move_to([0, -1.5, 0])
        self.play(FadeIn(idl), Indicate(needle, color=YELLOW), run_time=1.5)
        self.at("keep the relevant pixels")
        self.play(FadeOut(VGroup(pc, bc, lc, pt, bt, lt, dial, ticks, needle, con, idl)), run_time=.5)
        box = Rectangle(width=2.4, height=4.4, color=GREY, stroke_width=3).move_to([-2.0, -.3, 0])
        maxline = Line([-3.4, 1.9, 0], [-.6, 1.9, 0], color=RED, stroke_width=6)
        mxl = T("detector maximum", 30, RED, weight=BOLD).move_to([2.3, 1.9, 0])
        level = ValueTracker(0.0)
        fill = Rectangle(width=2.4, height=.01, stroke_width=0, fill_color=GREEN, fill_opacity=.85)

        def fu(m):
            h = max(4.4 * level.get_value(), .01)
            m.become(Rectangle(width=2.4, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=.85))
            m.move_to([-2.0, -2.5 + h / 2, 0])
        fill.add_updater(fu)
        pv = T("pixel value", 28, TEXT).move_to([2.3, -.3, 0])
        self.add(fill)
        self.play(Create(box), Create(maxline), FadeIn(mxl), FadeIn(pv), run_time=.6)
        self.play(level.animate.set_value(.75), run_time=1.4)
        self.at("detector maximum")
        self.play(Indicate(mxl, color=RED, scale_factor=1.1), run_time=1.2)
        self.at("background subtraction")
        fill.clear_updaters()
        self.play(FadeOut(VGroup(box, maxline, mxl, pv, fill)), run_time=.4)
        n = 140
        rng = np.random.RandomState(7)
        xs = np.linspace(-5.5, 5.5, n)
        mean = 40 + 170 * np.exp(-((np.arange(n) - 70) / 20.0) ** 2)
        counts = rng.poisson(mean).astype(float)
        y0, sc = -1.6, 4.0 / 250
        pts = lambda c: [[x, y0 + sc * v, 0] for x, v in zip(xs, c)]
        axl = VGroup(Line([-5.7, y0, 0], [5.7, y0, 0], color=GREY, stroke_width=2),
                     Line([-5.7, y0, 0], [-5.7, 2.5, 0], color=GREY, stroke_width=2))
        tr = VMobject().set_points_as_corners(pts(counts)).set_stroke(TEXT, 4)
        sim = T("simulated counts", 24, TEXT).move_to([-3.6, 2.55, 0])
        sub = chip("subtract background", YELLOW, 28).move_to([-3.6, 1.8, 0])
        bgl = DashedLine([-5.7, y0 + sc * 40, 0], [5.7, y0 + sc * 40, 0], color=YELLOW, stroke_width=4)
        self.play(Create(axl), Create(tr), FadeIn(sim), Create(bgl), FadeIn(sub), run_time=1.0)
        self.at("removes the average")
        tr2 = VMobject().set_points_as_corners(pts(counts - 40)).set_stroke(TEXT, 4)
        bg2 = DashedLine([-5.7, y0, 0], [5.7, y0, 0], color=YELLOW, stroke_width=4)
        self.play(Transform(tr, tr2), Transform(bgl, bg2), run_time=1.6)
        self.at("photon noise")
        pn = T("photon noise remains", 32, RED, weight=BOLD).move_to([3.3, 1.5, 0])
        self.play(FadeIn(pn, shift=DOWN * .2), ShowPassingFlash(tr.copy().set_stroke(RED, 9), time_width=.3),
                  run_time=1.8)
        self.finish()


class S11Claim(SpokenScene):
    def construct(self):
        w = World()
        ch = chain_chips()
        fb = filter_block()
        claim = chip("claim", YELLOW, 30).move_to([DET_X, -3.3, 0])
        cl = Line([DET_X, DET_Y - .85, 0], claim.get_top(), color=YELLOW, stroke_width=4)
        drops = VGroup(Line([CHIP_XS[0], CHIP_Y - .4, 0], [CHIP_XS[0], 2.5, 0], color=YELLOW, stroke_width=3),
                       Line([CHIP_XS[1], CHIP_Y - .4, 0], [CHIP_XS[1], fb.get_top()[1], 0], color=YELLOW, stroke_width=3),
                       Line([CHIP_XS[2], CHIP_Y - .4, 0], [CHIP_XS[2], 2.2, 0], color=YELLOW, stroke_width=3))
        w.add_to(self)
        self.add(ch, fb, claim, cl, drops)
        self.at("if every link holds")
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.15) for c in ch.chips[:1]], run_time=.7)
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.15) for c in ch.chips[1:2]], run_time=.7)
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.15) for c in ch.chips[2:]], run_time=.7)
        self.at("infocus overlap")
        halo = Ellipse(width=1.4, height=2.2, color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=.1)
        halo.move_to([DET_X, DET_Y, 0])
        self.play(FadeIn(halo, scale=.5), run_time=1.0)
        self.at("proximity at roughly")
        px = T("proximity at\nresolution scale", 26, GREEN, weight=BOLD).move_to([1.5, -3.4, 0])
        self.play(FadeIn(px, shift=UP * .2), run_time=1.0)
        self.play(Indicate(halo, color=GREEN, scale_factor=1.1), run_time=1.4)
        self.at("binding is a separate")
        w.calm()
        old = VGroup(w.all, fb, claim, cl, drops, ch.links, halo, px)
        prox_ell = ellipsoid(cx=-5.1, cy=-.1, w=1.2, h=3.0)
        prox_dot = Square(.25, stroke_width=0, fill_color=YELLOW, fill_opacity=.9).move_to([-5.1, -.1, 0])
        prox_lab = T("proximity at\nresolution scale", 28, GREEN, weight=BOLD).move_to([-5.0, -2.3, 0])
        box = RoundedRectangle(corner_radius=.2, width=3.6, height=4.0, color=TEXT, stroke_width=4)
        box.move_to([4.9, .0, 0])
        bl = T("binding", 40, TEXT, weight=BOLD).move_to([4.9, 1.2, 0])
        sch = T("schematic", 24, TEXT).move_to([4.9, -1.5, 0])
        self.play(FadeOut(old), FadeIn(prox_ell), FadeIn(prox_dot), FadeIn(prox_lab), Create(box), FadeIn(bl),
                  *[c.animate.set_opacity(.5) for c in ch.chips], run_time=2.0)
        self.add(sch)
        self.at("co immunoprecipitation")
        bead = Circle(.38, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.5).move_to([-1.3, .9, 0])
        self.play(FadeIn(bead, scale=.6), run_time=.8)
        self.at("supports membership")
        b1 = RoundedRectangle(corner_radius=.1, width=.7, height=.5, color=BLUE, stroke_width=3,
                              fill_color=BLUE, fill_opacity=.4).move_to([-.4, 1.4, 0])
        b2 = RoundedRectangle(corner_radius=.1, width=.7, height=.5, color=RED, stroke_width=3,
                              fill_color=RED, fill_opacity=.4).move_to([-.4, .4, 0])
        t1, t2 = Line(bead.get_right(), b1.get_left(), color=GREY, stroke_width=3), Line(bead.get_right(), b2.get_left(), color=GREY, stroke_width=3)
        coi = T("co-IP: same complex", 28, TEXT).move_to([0.2, 2.2, 0])
        self.play(FadeIn(b1), FadeIn(b2), Create(t1), Create(t2), FadeIn(coi), run_time=1.4)
        self.at("but not direct")
        arr1 = DashedLine([.9, .9, 0], [3.0, .5, 0], color=TEXT, stroke_width=4)
        arr1.add_tip(tip_length=.2)
        self.play(Create(arr1), run_time=1.3)
        self.at("a test with purified")
        tube = VGroup(RoundedRectangle(corner_radius=.3, width=.8, height=1.6, color=TEXT, stroke_width=3,
                                       fill_color=BLUE, fill_opacity=.15),
                      Dot([0, -.2, 0], radius=.1, color=BLUE), Dot([.15, -.45, 0], radius=.1, color=RED)
                      ).move_to([-1.3, -1.9, 0])
        pur = T("purified proteins:\ndirect binding", 28, TEXT).move_to([.9, -1.9, 0])
        self.play(FadeIn(tube, shift=UP * .2), FadeIn(pur), run_time=1.2)
        self.at("addresses direct interaction")
        arr2 = DashedLine([2.5, -1.9, 0], [3.1, -.9, 0], color=TEXT, stroke_width=4)
        arr2.add_tip(tip_length=.2)
        self.play(Create(arr2), run_time=1.2)
        self.play(Indicate(box, color=TEXT, scale_factor=1.03), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "Overlap supports proximity within one resolution volume, not binding."
