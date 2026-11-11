"""Why One Photon Is Not Enough — Biochemistrypedia explainer.

COLOR MAP
  YELLOW = photons, excitation, and the tracked electron
  BLUE   = water and Photosystem II
  TEAL   = cytochrome b6f and membrane electron transport
  GREEN  = Photosystem I, NADP+/NADPH, and ATP
  RED    = lumen protons and the proton gradient
  GREY   = membrane, axes, carriers, and schematic structure

All diagrams are schematic.  The potential gap and photon-energy comparison use the
values stated in the narration: 0.82 - (-0.32) = 1.14 V and about 1.8 eV.
"""
from bp_style import *  # noqa: F401,F403
import numpy as np


def P(x, y):
    return np.array([x, y, 0.0])


def wave(a, b, color=YELLOW, amp=0.13, cycles=5, width=5):
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    u = d / np.linalg.norm(d)
    n = np.array([-u[1], u[0], 0.0])
    return ParametricFunction(
        lambda t: a + t * d + n * amp * np.sin(TAU * cycles * t),
        t_range=[0, 1, 0.02], color=color, stroke_width=width
    )


def electron(pos, r=0.16):
    halo = Circle(r * 2.2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.16)
    bead = Dot(radius=r, color=YELLOW)
    return VGroup(halo, bead).move_to(pos)


def hplus(pos, edge=RED):
    ring = Circle(0.20, color=edge, stroke_width=2.5, fill_color=edge, fill_opacity=0.18)
    plus = VGroup(Line(LEFT * .08, RIGHT * .08, color=edge, stroke_width=2.5),
                  Line(DOWN * .08, UP * .08, color=edge, stroke_width=2.5))
    return VGroup(ring, plus.move_to(ring)).move_to(pos)


def solid_chip(text, color=BLUE, size=28, pad=0.22):
    """A chip whose opaque centre keeps carried paths from crossing its label."""
    label = T(text, size=size, color=color, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad,
                           height=label.height + 2 * pad, stroke_color=color,
                           stroke_width=2.5, fill_color=BG, fill_opacity=.96)
    return VGroup(box, label.move_to(box))


def protein(label, x, color, width=1.75, height=1.35, size=28):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                           stroke_color=color, stroke_width=3,
                           fill_color=BG, fill_opacity=.96).move_to(P(x, 0))
    # The carried electron route runs through the lower half of each complex.
    # Keeping the label high makes the route readable without touching the words.
    text = T(label, size, color, weight=BOLD).move_to(box).shift(UP * .25)
    return VGroup(box, text)


def membrane(labels=True):
    band = Rectangle(width=12.6, height=0.72, stroke_width=0,
                     fill_color=GREY, fill_opacity=0.22).move_to(P(0, 0))
    rails = VGroup(Line(P(-6.3, .36), P(6.3, .36), color=GREY, stroke_width=3),
                   Line(P(-6.3, -.36), P(6.3, -.36), color=GREY, stroke_width=3))
    g = VGroup(band, rails)
    if labels:
        g.add(T("STROMA", 28, GREY).move_to(P(-5.35, 3.35)),
              T("LUMEN", 28, GREY).move_to(P(-5.45, -3.28)))
    return g


def complexes(include_atp=False):
    ps2 = protein("Photosystem II", -4.35, BLUE, 2.35)
    b6f = protein("cytochrome b6f", -1.25, TEAL, 2.65)
    ps1 = protein("Photosystem I", 2.0, GREEN, 2.25)
    items = [ps2, b6f, ps1]
    if include_atp:
        items.append(protein("ATP synthase", 5.0, YELLOW, 2.1, 1.65))
    return VGroup(*items)


def potential_track(with_labels=True):
    x, y0, y1 = -4.75, -2.75, 2.55
    axis = Arrow(P(x, y0), P(x, y1 + .45), buff=0, color=GREY,
                 stroke_width=5, max_tip_length_to_length_ratio=.06)
    ticks = VGroup(*[Line(P(x - .16, y), P(x + .16, y), color=GREY, stroke_width=3)
                     for y in np.linspace(y0, y1, 7)])
    low = Line(P(x - .5, y0), P(x + .55, y0), color=BLUE, stroke_width=6)
    high = Line(P(x - .5, y1), P(x + .55, y1), color=GREEN, stroke_width=6)
    g = VGroup(axis, ticks, low, high)
    if with_labels:
        g.add(T("water   about +0.82 V", 29, BLUE).move_to(P(-1.75, y0 + .38)),
              T("NADP+   about -0.32 V", 29, GREEN).move_to(P(-1.75, y1 - .38)),
              T("more negative = uphill", 28, TEXT).move_to(P(-4.25, 3.48)),
              T("schematic", 28, GREY).move_to(P(5.55, -3.32)))
    return g


def bracket_gap(x=-5.75):
    return VGroup(Line(P(x, -2.67), P(x, 2.47), color=YELLOW, stroke_width=4),
                  Line(P(x, -2.67), P(x + .35, -2.67), color=YELLOW, stroke_width=4),
                  Line(P(x, 2.47), P(x + .35, 2.47), color=YELLOW, stroke_width=4))


def photon_to(target):
    return wave(target + UP * 2.35 + LEFT * .8, target + UP * .65, YELLOW)


def lift_path():
    pts = [P(-5.7, -2.3), P(-4.35, 1.55), P(-1.25, -.3), P(2.0, 1.75), P(4.95, 2.45)]
    return pts


def z_lines(width=6, opacity=1):
    p = lift_path()
    return VGroup(*[Line(p[i], p[i + 1], color=YELLOW if i in (0, 2) else TEAL,
                              stroke_width=width, stroke_opacity=opacity)
                    for i in range(4)]).set_z_index(-2)


# A quiet, consistent diagram ground keeps the world alive between narrated beats.  The two
# translucent fields read as the two sides of the energy landscape; the motes are a schematic
# current, not additional molecules or a quantitative claim.
_BaseSpokenScene = SpokenScene


class SpokenScene(_BaseSpokenScene):
    def setup(self):
        super().setup()
        left = RoundedRectangle(corner_radius=.35, width=6.15, height=6.75,
                                stroke_width=0, fill_color=BLUE, fill_opacity=.14).move_to(P(-3.25, -.05))
        right = RoundedRectangle(corner_radius=.35, width=6.15, height=6.75,
                                 stroke_width=0, fill_color=GREEN, fill_opacity=.11).move_to(P(3.25, -.05))
        landscape = Rectangle(width=13.5, height=3.0, stroke_width=0,
                              fill_color=TEAL, fill_opacity=.16).move_to(P(0, -.45))
        fields = VGroup(left, right, landscape).set_z_index(-20)
        motes = VGroup(*[Dot(P(-6.2 + i * .66, -3.68 + .06 * np.sin(i)), radius=.10,
                                  color=YELLOW if i % 2 else TEAL).set_opacity(.46)
                         for i in range(20)]).set_z_index(-15)

        def drift(group, dt):
            group.shift(RIGHT * 1.15 * dt)
            for d in group:
                if d.get_x() > 6.45:
                    d.shift(LEFT * 13.3)

        motes.add_updater(drift)
        self.add(fields, motes)


class S00Hook(SpokenScene):
    def construct(self):
        track = potential_track()
        e = electron(P(-4.75, -2.57), .19)
        self.play(LaggedStart(Create(track[0]), Create(track[1]), Create(track[2]), Create(track[3]),
                              lag_ratio=.16), FadeIn(e, scale=.5), run_time=.9)
        self.play(FadeIn(VGroup(*track[4:])), run_time=.55)
        self.at("one red photon")
        ph = wave(P(.2, 2.9), P(1.4, 1.85), color="#F6A33B", amp=.16, cycles=6)
        energy = Arrow(P(1.6, -2.5), P(1.6, 3.15), buff=0, color=YELLOW,
                       stroke_width=9, max_tip_length_to_length_ratio=.08).set_opacity(.78)
        elab = T("about 1.8 eV", 32, YELLOW, weight=BOLD).next_to(energy, RIGHT, buff=.25)
        self.play(Create(ph), run_time=.65)
        self.play(GrowArrow(energy), FadeIn(elab), e.animate.shift(UP * .12), run_time=1.15)
        self.at("climb from water")
        br = bracket_gap()
        gap = T("1.14 V uphill", 32, YELLOW, weight=BOLD).rotate(PI / 2).move_to(P(-6.38, -.1))
        self.play(Create(br), FadeIn(gap), run_time=.85)
        self.at("so why")
        left = Arrow(P(.75, -2.25), P(.75, .2), buff=0, color=YELLOW, stroke_width=7)
        right = Arrow(P(2.45, .2), P(2.45, 2.65), buff=0, color=YELLOW, stroke_width=7)
        q = T("?", 64, TEXT, weight=BOLD).move_to(P(1.6, .2))
        self.play(FadeOut(energy), Transform(elab, T("two photons?", 34, YELLOW, weight=BOLD).move_to(P(1.6, -3.15))),
                  GrowArrow(left), GrowArrow(right), FadeIn(q), run_time=1.0)
        self.at("two photons")
        self.play(Indicate(VGroup(left, right), color=YELLOW, scale_factor=1.04),
                  e.animate.shift(UP * .18), run_time=.7)
        self.play(e.animate.shift(DOWN * .18), run_time=.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Photosynthesis: the light reactions"
    TITLE = "Why One Photon Is Not Enough"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 28, TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), 30, GREY)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        group = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=.3)
        self.play(FadeIn(brand, shift=UP*.1), FadeIn(lesson, shift=UP*.1),
                  run_time=self.beat(.25))
        self.play(Write(title), GrowFromCenter(rule), run_time=self.beat(.35))
        self.wait(self.beat(.2))
        self.play(FadeOut(group), run_time=self.beat(.2))
        self.finish()


class S02Map(SpokenScene):
    def construct(self):
        track = potential_track(False)
        e = electron(P(-4.75, -2.57), .18)
        mem = Rectangle(width=7.2, height=.72, stroke_width=0, fill_color=GREY,
                        fill_opacity=.24).move_to(P(2.6, -.35))
        rails = VGroup(Line(P(-1, .01), P(6.2, .01), color=GREY, stroke_width=3),
                       Line(P(-1, -.71), P(6.2, -.71), color=GREY, stroke_width=3))
        regions = VGroup(T("STROMA", 28, GREY).move_to(P(5.25, 2.95)),
                         T("LUMEN", 28, GREY).move_to(P(5.35, -3.1)))
        self.play(FadeIn(track), FadeIn(e), FadeIn(mem), Create(rails), FadeIn(regions), run_time=.9)
        self.at("more negative potential")
        uphill = Arrow(P(-3.8, -1.8), P(-3.8, 2.2), color=TEXT, stroke_width=5)
        ulab = T("UPHILL", 28, TEXT, weight=BOLD).rotate(PI / 2).next_to(uphill, RIGHT, buff=.15)
        self.play(LaggedStart(*[Indicate(t, color=TEXT, scale_factor=1.5) for t in track[1]], lag_ratio=.08),
                  GrowArrow(uphill), FadeIn(ulab), run_time=1.15)
        self.at("water starts")
        water = solid_chip("water", BLUE, 30).move_to(P(.05, -.35))
        lowlab = T("about +0.82 V", 28, BLUE).move_to(P(-2.75, -2.38))
        self.play(FadeIn(water, shift=UP * .2), FadeIn(lowlab), e.animate.scale(1.12), run_time=.85)
        self.at("dP plus", lead=.15)
        nadp = solid_chip("NADP+", GREEN, 30).move_to(P(4.85, 2.2))
        highlab = T("about -0.32 V", 28, GREEN).move_to(P(-2.7, 2.18))
        self.play(FadeIn(nadp, shift=DOWN * .2), FadeIn(highlab), run_time=.85)
        motes = VGroup(*[hplus(P(x, -2.0 + .22 * np.sin(x)), RED).scale(.7) for x in (0, 1.3, 2.6, 3.9, 5.2)])
        self.play(LaggedStart(*[FadeIn(m) for m in motes], lag_ratio=.08), run_time=.6)
        self.play(motes.animate.shift(RIGHT * .45), run_time=1.0, rate_func=linear)
        self.finish()


class S03Gap(SpokenScene):
    def construct(self):
        track = potential_track()
        e = electron(P(-4.75, -2.57), .18)
        self.add(track, e)
        self.at("the gap")
        br = bracket_gap()
        count = ValueTracker(0)
        read = always_redraw(lambda: M(f"{count.get_value():.2f} V", 34, YELLOW)
                             .rotate(PI / 2).move_to(P(-6.38, 0)))
        self.play(Create(br), FadeIn(read), count.animate.set_value(1.14), run_time=1.3)
        self.at("a red photon")
        ph = wave(P(-.5, 2.8), P(.8, 1.7), color="#F6A33B", amp=.15, cycles=6)
        barbox = RoundedRectangle(corner_radius=.14, width=1.1, height=5.2, color=GREY).move_to(P(3.2, -.05))
        fill = Rectangle(width=.72, height=.01, stroke_width=0, fill_color=YELLOW, fill_opacity=.72).move_to(P(3.2, -2.53))
        lab = T("about 1.8 eV", 30, YELLOW, weight=BOLD).move_to(P(4.75, 2.2))
        schem = T("energy comparison — schematic", 28, GREY).move_to(P(3.55, -3.25))
        self.play(Create(ph), Create(barbox), FadeIn(fill), run_time=.65)
        self.play(fill.animate.stretch_to_fit_height(5.0).move_to(P(3.2, -.05)),
                  FadeIn(lab), Transform(track[-1], schem), run_time=1.3)
        self.at("on paper")
        attempt = Arrow(P(-3.5, -2.55), P(-3.5, 2.85), buff=0, color=YELLOW, stroke_width=8)
        self.play(GrowArrow(attempt), e.animate.move_to(P(-4.75, 2.76)), run_time=1.25)
        self.at("looks sufficient")
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.08), e.animate.shift(UP * .12), run_time=.65)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        track = potential_track()
        e = electron(P(-4.75, -2.57), .18)
        tall = Arrow(P(-3.5, -2.55), P(-3.5, 2.85), buff=0, color=YELLOW, stroke_width=8)
        self.add(track, e, tall)
        self.at("arrive somewhere stable")
        self.play(e.animate.move_to(P(-4.75, 2.72)), tall.animate.set_opacity(.25), run_time=.8)
        self.play(e.animate.move_to(P(-4.75, -2.45)), run_time=1.15, rate_func=rush_into)
        self.at("not merely visit")
        unstable = T("excited ≠ stable", 33, RED, weight=BOLD).move_to(P(2.1, 2.3))
        self.play(FadeIn(unstable), Flash(e, color=YELLOW, line_length=.35), run_time=.65)
        self.at("Predict")
        one = Arrow(P(-.2, -1.6), P(-.2, 1.25), color=GREY, stroke_width=7)
        two = VGroup(Arrow(P(2.0, -1.6), P(2.0, -.05), color=YELLOW, stroke_width=7),
                     Arrow(P(4.25, -.05), P(4.25, 1.5), color=YELLOW, stroke_width=7))
        q = T("One photon or two?", 46, TEXT, font=TITLE_FONT).move_to(P(1.9, 3.15))
        self.play(FadeOut(unstable), FadeOut(tall), FadeIn(q), GrowArrow(one),
                  LaggedStart(*[GrowArrow(a) for a in two], lag_ratio=.25), run_time=1.0)
        self.at("one or two")
        traveler = electron(P(-.2, -1.65), .16)
        self.play(TransformFromCopy(e, traveler), run_time=.3)
        self.play(traveler.animate.move_to(P(2.0, -.2)), run_time=.75)
        self.play(traveler.animate.move_to(P(4.25, 1.55)), run_time=.75)
        self.finish()


class S05Think(Scene):
    def construct(self):
        config.background_color = BG
        q = T("One photon or two?", 50, TEXT, font=TITLE_FONT).move_to(P(0, 2.8))
        one = Arrow(P(-2.1, -1.65), P(-2.1, 1.0), color=GREY, stroke_width=8)
        two = VGroup(Arrow(P(1.0, -1.65), P(1.0, -.15), color=YELLOW, stroke_width=8),
                     Arrow(P(3.35, -.15), P(3.35, 1.35), color=YELLOW, stroke_width=8))
        e = electron(P(0, -2.65), .22)
        t = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=.55, start_angle=PI / 2,
                                         angle=-TAU * max(.002, t.get_value()), color=YELLOW,
                                         stroke_width=7).move_to(e))
        self.add(q, one, two, e, ring)
        self.play(t.animate.set_value(1), two.animate.set_opacity(.62), run_time=2.25, rate_func=linear)
        self.play(two.animate.set_opacity(1), one.animate.set_opacity(.55), run_time=2.25, rate_func=there_and_back)


class S06Answer(SpokenScene):
    def construct(self):
        q = T("One photon or two?", 44, TEXT, font=TITLE_FONT).move_to(P(0, 3.2))
        one = Arrow(P(-2.2, -1.9), P(-2.2, 1.45), color=GREY, stroke_width=7)
        p = [P(.2, -2.2), P(.2, .9), P(1.5, .35), P(2.6, -.2), P(4.1, 2.3)]
        segs = VGroup(*[Arrow(p[i], p[i + 1], buff=.05,
                                  color=YELLOW if i in (0, 3) else TEAL, stroke_width=7)
                        for i in range(4)])
        self.add(q, one)
        self.at("2")
        answer = T("TWO", 58, YELLOW, weight=BOLD).move_to(P(-4.65, .2))
        self.play(FadeOut(one), FadeOut(q), FadeIn(answer, scale=.7), FadeIn(segs), run_time=.9)
        self.at("fast downhill steps")
        plus = solid_chip("+", RED, 30).move_to(P(.1, 1.65))
        minus = electron(P(.25, .9), .17)
        self.play(FadeIn(plus), FadeIn(minus), run_time=.35)
        self.play(minus.animate.move_to(p[2]), run_time=.35)
        self.play(minus.animate.move_to(p[3]), run_time=.35)
        self.at("before they recombine")
        ret = CurvedArrow(p[3], plus.get_right(), angle=-TAU / 5, color=RED, stroke_width=3).set_opacity(.5)
        self.play(Create(ret), run_time=.35)
        self.play(ret.animate.scale(.15).set_opacity(0), run_time=.7)
        self.at("those steps spend")
        bar = Rectangle(width=.85, height=4.7, color=GREY).move_to(P(5.55, -.05))
        fill = Rectangle(width=.6, height=4.4, stroke_width=0, fill_color=YELLOW, fill_opacity=.8).move_to(P(5.55, -.05))
        bits = VGroup(*[Dot(P(x, y), radius=.07, color=TEAL) for x, y in ((1.2,.55),(1.8,.1),(2.4,-.25))])
        self.play(Create(bar), FadeIn(fill), run_time=.4)
        self.play(fill.animate.stretch_to_fit_height(1.85).align_to(bar, DOWN).shift(UP * .16),
                  LaggedStart(*[FadeIn(b, shift=DOWN * .25) for b in bits], lag_ratio=.15), run_time=1.0)
        self.at("each stable lift")
        kept = VGroup(Line(P(-.65, -2.18), P(-.65, .86), color=YELLOW, stroke_width=4),
                      T("kept: about 0.7–0.8 V", 30, YELLOW, weight=BOLD).rotate(PI/2).move_to(P(-1.15, -.65)))
        self.play(Create(kept[0]), FadeIn(kept[1]), run_time=.8)
        self.play(minus.animate.move_to(p[4]), bits.animate.shift(RIGHT * .25 + DOWN * .12), run_time=1.15)
        self.finish()


class S07FirstLift(SpokenScene):
    def construct(self):
        mem = membrane()
        route = z_lines(5, .25)
        self.play(FadeIn(mem), Create(route), run_time=.9)
        self.at("Photosystem II")
        ps2 = protein("Photosystem II", -4.35, BLUE, 2.35)
        self.play(FadeIn(ps2, shift=UP * .6), run_time=.75)
        self.at("first photon")
        ph = photon_to(P(-4.35, 0))
        e = electron(P(-5.65, -2.22), .17)
        self.play(Create(ph), FadeIn(e), run_time=.45)
        self.play(FadeOut(ph), e.animate.move_to(P(-4.35, 1.55)), run_time=.95)
        self.at("downhill chain")
        stones = VGroup(*[RoundedRectangle(corner_radius=.1, width=.85, height=.42, color=TEAL,
                                           fill_color=TEAL, fill_opacity=.15).move_to(p)
                          for p in (P(-3.2,1.05), P(-2.25,.45), P(-1.25,-.25))])
        self.play(LaggedStart(*[FadeIn(s) for s in stones], lag_ratio=.18), run_time=.55)
        for s in stones:
            self.play(e.animate.move_to(s), run_time=.32)
        self.at("from water")
        water = solid_chip("water", BLUE, 28).move_to(P(-5.55, -1.45))
        replacement = electron(water.get_right() + RIGHT * .1, .13)
        self.play(FadeIn(water), FadeIn(replacement), run_time=.4)
        self.play(replacement.animate.move_to(P(-4.35, .95)), run_time=.7)
        queue = VGroup(*[electron(P(-4.9 + i*.42, 1.0 + i*.25), .08).set_opacity(.45) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(x) for x in queue], lag_ratio=.15), run_time=.5)
        self.play(queue.animate.shift(RIGHT * .75 + UP * .35), e.animate.shift(RIGHT * .25), run_time=1.0)
        self.finish()


class S08WaterBridge(SpokenScene):
    def construct(self):
        mem = membrane()
        ps2 = protein("Photosystem II", -4.35, BLUE, 2.35)
        b6f = protein("cytochrome b6f", -1.25, TEAL, 2.65)
        water = solid_chip("water", BLUE, 28).move_to(P(-5.55, -1.45))
        self.add(mem, ps2, water)
        self.at("splitting water")
        cycles = VGroup(*[electron(P(-5.2 + i*.25, -1.0 + i*.18), .08) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(e, shift=UP*.3) for e in cycles], lag_ratio=.12), run_time=.65)
        oxy = VGroup(Circle(.38, color=BLUE, fill_color=BG, fill_opacity=.96),
                     T("O2", 28, BLUE, weight=BOLD)).move_to(P(-5.6, -2.35))
        protons = VGroup(*[hplus(P(-4.6+i*.48, -2.05-.22*(i%2)), BLUE) for i in range(4)])
        self.play(FadeIn(oxy, scale=.5), LaggedStart(*[FadeIn(h, shift=DOWN*.25) for h in protons], lag_ratio=.12), run_time=.85)
        self.at("Cytochrome B6F")
        self.play(FadeIn(b6f, shift=UP*.5), run_time=.6)
        self.at("downhill bridge")
        e = electron(P(-4.35, 1.35), .16)
        bridge = Arrow(P(-3.65, 1.15), P(-1.3, .55), color=TEAL, stroke_width=6)
        self.play(FadeIn(e), GrowArrow(bridge), run_time=.4)
        self.play(e.animate.move_to(P(-1.25, .95)), run_time=.8)
        more = VGroup(*[hplus(P(-1.7+i*.55, -2.45+.22*(i%2)), TEAL) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN*.5) for h in more], lag_ratio=.12), run_time=.75)
        self.at("build a gradient")
        gauge = RoundedRectangle(corner_radius=.15, width=.72, height=4.5, color=RED).move_to(P(5.55, -1.0))
        fill = Rectangle(width=.45, height=.05, stroke_width=0, fill_color=RED, fill_opacity=.72).move_to(P(5.55, -3.18))
        glab = T("H+ gradient", 28, RED, weight=BOLD).rotate(PI/2).move_to(P(6.15, -1.0))
        self.play(Create(gauge), FadeIn(fill), FadeIn(glab), run_time=.45)
        self.play(fill.animate.stretch_to_fit_height(4.15).move_to(P(5.55, -1.0)),
                  protons.animate.shift(RIGHT*.7), more.animate.shift(RIGHT*.7), run_time=1.25)
        self.finish()


class S09SecondLift(SpokenScene):
    def construct(self):
        mem = membrane()
        cs = complexes()
        e = electron(P(-1.25, .95), .17)
        self.add(mem, cs[0], cs[1], e)
        self.at("photosystem I")
        self.play(FadeIn(cs[2], shift=UP*.5), e.animate.move_to(P(2, .95)), run_time=.85)
        self.at("second photon")
        ph = photon_to(P(2, 0))
        self.play(Create(ph), run_time=.5)
        self.play(FadeOut(ph), e.animate.move_to(P(2, 2.0)), run_time=.9)
        self.at("downhill steps")
        fd = solid_chip("ferredoxin", GREEN, 28).move_to(P(3.45, 2.25))
        fnr = solid_chip("FNR", GREEN, 28).move_to(P(4.75, 1.25))
        self.play(FadeIn(fd), run_time=.35)
        self.play(e.animate.move_to(fd), FadeIn(fnr), run_time=.55)
        self.play(e.animate.move_to(fnr), run_time=.55)
        self.at("Faradoxin and FNR", lead=.15)
        nadp = solid_chip("NADP+", GREEN, 29).move_to(P(5.55, 2.65))
        self.play(FadeIn(nadp), Indicate(VGroup(fd, fnr), color=GREEN, scale_factor=1.04), run_time=.65)
        self.at("making")
        e2 = electron(P(4.15, 1.65), .12)
        self.play(FadeIn(e2), e.animate.move_to(nadp), e2.animate.move_to(nadp), run_time=.75)
        nadph = solid_chip("NADPH", GREEN, 30).move_to(nadp)
        self.play(ReplacementTransform(nadp, nadph), FadeOut(VGroup(e, e2, fd, fnr)), run_time=.65)
        follower = electron(P(-1.25, .95), .08).set_opacity(.5)
        self.play(FadeIn(follower), follower.animate.move_to(P(2, 1.6)), run_time=1.0)
        self.finish()


class S10ZRule(SpokenScene):
    def construct(self):
        mem = membrane()
        cs = complexes()
        water = solid_chip("water", BLUE, 28).move_to(P(-5.7, -1.35))
        nadph = solid_chip("NADPH", GREEN, 28).move_to(P(5.45, 2.45))
        track = z_lines(7, .18)
        self.play(FadeIn(mem), FadeIn(cs), FadeIn(water), FadeIn(nadph), Create(track), run_time=.95)
        self.at("Z scheme's logic")
        title = T("Z-SCHEME — SCHEMATIC", 34, YELLOW, weight=BOLD).move_to(P(0, 3.35))
        self.play(FadeIn(title), track.animate.set_opacity(1), run_time=.7)
        self.at("two light driven lifts")
        lifts = VGroup(track[0], track[2])
        self.play(Indicate(lifts, color=YELLOW, scale_factor=1.025), run_time=.85)
        self.at("span a gap")
        span = DoubleArrow(P(-5.8, -2.25), P(-5.8, 2.5), color=TEXT, stroke_width=4, tip_length=.16)
        self.play(GrowFromCenter(span), run_time=.65)
        self.at("the electron climbs")
        e = electron(lift_path()[0], .16)
        self.play(FadeIn(e), run_time=.2)
        self.play(e.animate.move_to(lift_path()[1]), run_time=.55)
        self.play(e.animate.move_to(lift_path()[2]), run_time=.45)
        self.at("then climbs")
        self.play(e.animate.move_to(lift_path()[3]), run_time=.55)
        self.play(e.animate.move_to(lift_path()[4]), run_time=.45)
        self.finish()


class S11Tally(SpokenScene):
    def construct(self):
        mem = membrane()
        cs = complexes()
        route = z_lines(5, .45)
        self.add(mem, cs, route)
        self.at("repeat the root", lead=.15)
        counters = VGroup(T("PSII photons: 0", 28, YELLOW).move_to(P(-4.25, 2.85)),
                          T("PSI photons: 0", 28, YELLOW).move_to(P(1.9, 2.85)))
        self.play(FadeIn(counters), run_time=.35)
        for i in range(4):
            bead = electron(lift_path()[0], .18)
            num = M(str(i + 1), 28, BG).move_to(bead[1])
            self.play(FadeIn(bead), FadeIn(num), run_time=.12)
            self.play(bead.animate.move_to(lift_path()[2]), num.animate.move_to(lift_path()[2]), run_time=.23)
            self.play(bead.animate.move_to(lift_path()[4]), num.animate.move_to(lift_path()[4]), run_time=.23)
            newc = VGroup(T(f"PSII photons: {i + 1}", 28, YELLOW).move_to(counters[0]),
                          T(f"PSI photons: {i + 1}", 28, YELLOW).move_to(counters[1]))
            self.play(ReplacementTransform(counters, newc), FadeOut(bead), FadeOut(num), run_time=.12)
            counters = newc
        oxy = T("O2: 1", 30, BLUE, weight=BOLD).move_to(P(-4.8, -2.6))
        self.play(FadeIn(oxy), run_time=.4)
        self.at("linear flow")
        total = solid_chip("8 photons", YELLOW, 30).move_to(P(-.9, 2.75))
        nadph = solid_chip("2 NADPH", GREEN, 29).move_to(P(5.25, 2.45))
        self.play(FadeIn(total), FadeIn(nadph), run_time=.75)
        self.at("water and cytochrome")
        hs_blue = VGroup(*[hplus(P(-4.6+i*.48, -2.1), BLUE).scale(.72) for i in range(4)])
        hs_teal = VGroup(*[hplus(P(-1.9+(i%4)*.48, -2.55-(i//4)*.48), TEAL).scale(.72) for i in range(8)])
        self.play(LaggedStart(*[FadeIn(h) for h in hs_blue], lag_ratio=.08), run_time=.45)
        self.play(LaggedStart(*[FadeIn(h) for h in hs_teal], lag_ratio=.06), run_time=.65)
        self.at("about 12")
        tally = T("H+ in lumen: about 12", 31, RED, weight=BOLD).move_to(P(3.65, -2.75))
        self.play(FadeIn(tally), VGroup(hs_blue, hs_teal).animate.shift(RIGHT*.35), run_time=.75)
        self.finish()


class S12AtpScope(SpokenScene):
    def construct(self):
        mem = membrane()
        cs = complexes()
        route = z_lines(4, .32)
        protons = VGroup(*[hplus(P(3.7+(i%4)*.5, -2.5-(i//4)*.45)).scale(.75) for i in range(8)])
        self.add(mem, cs[:3], route, protons)
        self.at("protons flow back")
        atp_box = RoundedRectangle(corner_radius=.18, width=2.25, height=1.9,
                                   stroke_color=YELLOW, stroke_width=3,
                                   fill_color=BG, fill_opacity=.96).move_to(P(5, 0))
        atp_label = T("ATP synthase", 28, YELLOW, weight=BOLD).move_to(P(5, .55))
        atp_unit = VGroup(atp_box, atp_label)
        self.play(FadeIn(atp_unit, shift=UP*.5), run_time=.5)
        rotor = Circle(.43, color=YELLOW, stroke_width=5).move_to(P(5, -.35))
        spokes = VGroup(*[Line(rotor.get_center(), rotor.point_at_angle(a), color=YELLOW, stroke_width=3)
                          for a in np.linspace(0, TAU, 6, endpoint=False)])
        self.play(Create(rotor), Create(spokes), run_time=.4)
        self.play(protons.animate.arrange(DOWN, buff=.08).move_to(P(5, -1.55)),
                  Rotate(spokes, PI), run_time=.9)
        self.at("TP synthase", lead=.15)
        adp = solid_chip("ADP", GREY, 28).move_to(P(3.8, 2.35))
        atp = solid_chip("ATP", GREEN, 30).move_to(P(4.8, 2.55))
        self.play(FadeIn(adp), Rotate(spokes, PI), run_time=.55)
        self.play(ReplacementTransform(adp, atp),
                  protons.animate.shift(UP*2.65).set_opacity(0), run_time=.75)
        self.at("this is linear flow")
        outline = SurroundingRectangle(VGroup(route, cs[:3]), color=YELLOW, buff=.15, stroke_width=3)
        linear = T("LINEAR FLOW", 29, YELLOW, weight=BOLD).move_to(P(-1.1, 3.15))
        self.play(Create(outline), FadeIn(linear), run_time=.7)
        self.at("cycle electrons")
        loop = CurvedArrow(P(3.2, 1.7), P(-1.2, .75), angle=TAU/5, color=TEAL, stroke_width=4)
        loop.set_stroke(opacity=.8)
        cyc = T("cyclic flow: ATP adjustment", 28, TEAL, weight=BOLD).move_to(P(.7, 2.25))
        self.play(FadeOut(outline), FadeOut(linear), Create(loop), FadeIn(cyc), run_time=.85)
        self.play(Indicate(atp, color=GREEN, scale_factor=1.1), Rotate(spokes, PI), run_time=.75)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        track = potential_track()
        self.play(LaggedStart(*[FadeIn(x) for x in track], lag_ratio=.08), run_time=.9)
        self.at("opening puzzle")
        q = T("Why two photons?", 40, TEXT, font=TITLE_FONT).move_to(P(2.3, 3.1))
        self.play(FadeIn(q), run_time=.5)
        self.at("a photon has enough")
        bar = RoundedRectangle(corner_radius=.14, width=.9, height=4.9, color=GREY).move_to(P(5.55, -.1))
        fill = Rectangle(width=.58, height=4.55, stroke_width=0, fill_color=YELLOW, fill_opacity=.78).move_to(P(5.55, -.1))
        blab = T("1.8 eV raw", 28, YELLOW, weight=BOLD).rotate(PI / 2).move_to(P(6.3, .75))
        self.play(Create(bar), FadeIn(fill), FadeIn(blab), run_time=.8)
        self.at("reaction center cannot")
        p = [P(-3.45,-2.55), P(-3.45,-.05), P(-1.0,-.8), P(1.35,1.7), P(3.5,1.15), P(4.5,2.5)]
        arrows = VGroup(*[Arrow(p[i], p[i+1], buff=.04, color=YELLOW if i in (0,2) else TEAL, stroke_width=6)
                          for i in range(5)]).set_z_index(-2)
        ps2 = solid_chip("PSII", BLUE, 28).move_to(P(-3.45, -.95))
        ps1 = solid_chip("PSI", GREEN, 28).move_to(P(1.35, .75))
        self.play(FadeIn(ps2), FadeIn(ps1), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.12),
                  fill.animate.stretch_to_fit_height(1.7).align_to(bar, DOWN).shift(UP*.16), run_time=1.25)
        self.at("two stable lifts")
        ans = T("2 STABLE LIFTS", 40, YELLOW, weight=BOLD).move_to(q)
        e = electron(p[0], .17)
        gauge = RoundedRectangle(corner_radius=.12, width=.6, height=2.2, color=RED).move_to(P(5.55, -2.0))
        gf = Rectangle(width=.36, height=.12, stroke_width=0, fill_color=RED, fill_opacity=.7).align_to(gauge, DOWN).shift(UP*.1)
        self.play(ReplacementTransform(q, ans), FadeIn(e), Create(gauge), FadeIn(gf), run_time=.55)
        self.play(e.animate.move_to(p[2]), run_time=.55)
        self.play(e.animate.move_to(p[4]), gf.animate.stretch_to_fit_height(1.85).move_to(gauge), run_time=.7)
        self.play(e.animate.move_to(p[5]), Indicate(ans, color=YELLOW, scale_factor=1.04), run_time=.6)
        self.finish()


class S14End(EndCard):
    LINE = "Stable transfer from water to NADPH needs two light-driven lifts."

    def construct(self):
        arrows = VGroup(Arrow(P(-5.7, -2.5), P(-5.0, 1.5), color=YELLOW, stroke_width=8),
                        Arrow(P(4.25, -2.5), P(4.85, 1.5), color=YELLOW, stroke_width=8)).set_opacity(.28)
        hexm = hex_mascot(1.45).move_to(P(0, 2.25))
        line = T("Stable transfer from water to NADPH\nneeds two light-driven lifts.",
                 38, TEXT, font=TITLE_FONT, line_spacing=.9)
        line.move_to(P(0, .35))
        sub = T("biochemistrypedia.com", 28, TEAL).move_to(P(0, -1.15))
        gauge = RoundedRectangle(corner_radius=.12, width=.65, height=2.3, color=RED).move_to(P(5.65, -1.8))
        fill = Rectangle(width=.38, height=.12, stroke_width=0, fill_color=RED, fill_opacity=.72).align_to(gauge, DOWN).shift(UP*.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.25), FadeIn(hexm), run_time=.75)
        self.play(FadeIn(line), FadeIn(sub), Create(gauge), FadeIn(fill), run_time=.55)
        shoulder = hexm.arm.get_start()
        self.play(Rotate(hexm.arm, -.5, about_point=shoulder),
                  fill.animate.stretch_to_fit_height(1.85).move_to(gauge),
                  rate_func=there_and_back, run_time=.75)
        self.play(Rotate(hexm.arm, -.5, about_point=shoulder), rate_func=there_and_back, run_time=.55)
        self.finish()
