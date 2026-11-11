"""A Path Is Not a Pump — membrane transport as one carried world.

COLOR MAP
  BLUE   water, hydration, concentration
  GOLD   oily membrane core
  TEAL   transport-protein outlines / polar pathway
  YELLOW charged solute and sodium
  RED    energetic cost, voltage, uphill
  GREEN  electrochemical downhill and coupled energy
  GREY   neutral structure and secondary labels
  TEXT   primary labels

All mechanisms are schematic cartoons.  No molecular structures are drawn.
"""
from bp_style import *


MEM_Y = -0.45
CORE_H = 1.45


def solute(label="+", r=0.27, color=YELLOW):
    body = Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.95)
    mark = T(label, size=24, color=BG, weight=BOLD).move_to(body)
    return VGroup(body, mark)


def membrane_world(motes=True):
    """The carried water/oil cross-section, at identical coordinates in every scene."""
    upper = Rectangle(width=13.2, height=2.65, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.09).move_to([0, 2.05, 0])
    lower = Rectangle(width=13.2, height=2.65, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.09).move_to([0, -2.95, 0])
    # A slow optical shimmer keeps long explanatory holds alive without changing the diagram.
    for i, band in enumerate((upper, lower)):
        band._phase = i * PI
        def shimmer(m, dt):
            m._phase += dt
            m.set_fill(BLUE, opacity=0.09 + 0.035 * np.sin(1.7 * m._phase))
        band.add_updater(shimmer)
    core = RoundedRectangle(width=13.2, height=CORE_H, corner_radius=0.18,
                            stroke_color=GOLD, stroke_width=2,
                            fill_color=GOLD, fill_opacity=0.28).move_to([0, MEM_Y, 0])
    faces = VGroup(
        Line([-6.55, MEM_Y + CORE_H / 2, 0], [6.55, MEM_Y + CORE_H / 2, 0], color=GOLD, stroke_width=5),
        Line([-6.55, MEM_Y - CORE_H / 2, 0], [6.55, MEM_Y - CORE_H / 2, 0], color=GOLD, stroke_width=5),
    )
    world = VGroup(upper, lower, core, faces)
    if not motes:
        return world, VGroup()
    dots = VGroup()
    coords = [(-6.0, 3.15), (-5.2, 2.2), (-4.3, 3.0), (-3.4, 1.45),
              (-2.5, 2.55), (-1.5, 3.25), (-0.4, 1.65), (0.7, 2.7),
              (1.8, 1.45), (2.8, 3.15), (3.8, 2.2), (4.8, 3.0), (5.8, 1.6),
              (-5.8, -3.25), (-4.8, -2.15), (-3.7, -3.35), (-2.7, -2.0),
              (-1.6, -3.05), (-0.5, -2.2), (0.6, -3.35), (1.7, -2.05),
              (2.8, -3.1), (3.9, -2.15), (5.0, -3.35), (6.0, -2.2)]
    for i, (x, y) in enumerate(coords):
        d = Dot([x, y, 0], radius=0.055 + 0.012 * (i % 3), color=BLUE).set_opacity(0.42)
        vx = 0.10 + 0.025 * (i % 4)
        vy = (0.025 if i % 2 else -0.025)
        region = 1 if y > MEM_Y else -1
        def drift(m, dt, vx=vx, vy=vy, region=region):
            m.shift([vx * dt, vy * dt, 0])
            if m.get_x() > 6.65:
                m.set_x(-6.65)
            lo, hi = ((0.45, 3.55) if region > 0 else (-3.55, -1.35))
            if m.get_y() < lo:
                m.set_y(hi)
            elif m.get_y() > hi:
                m.set_y(lo)
        d.add_updater(drift)
        dots.add(d)
    return world, dots


def pore(x=0, open_amount=0.95):
    left = RoundedRectangle(width=0.42, height=2.15, corner_radius=0.18,
                            stroke_color=TEAL, stroke_width=5, fill_color=TEAL,
                            fill_opacity=0.23).move_to([x - open_amount / 2, MEM_Y, 0])
    right = left.copy().move_to([x + open_amount / 2, MEM_Y, 0])
    return VGroup(left, right)


def carrier(x=0, opening=UP, color=TEAL, scale=1.0):
    body = RoundedRectangle(width=1.65, height=2.1, corner_radius=0.38,
                            stroke_color=color, stroke_width=5,
                            fill_color=color, fill_opacity=0.24).move_to([x, MEM_Y, 0])
    pocket = Circle(radius=0.42, stroke_width=0, fill_color=BG, fill_opacity=1)
    pocket.move_to([x, MEM_Y + (0.85 if np.allclose(opening, UP) else -0.85), 0])
    return VGroup(body, pocket).scale(scale, about_point=[x, MEM_Y, 0])


def side_labels(top="outside", bottom="inside"):
    return VGroup(T(top, 28, TEXT).move_to([-5.0, 2.95, 0]),
                  T(bottom, 28, TEXT).move_to([-4.9, -3.25, 0]))


def charge_row(sign, y, color, n=7):
    return VGroup(*[T(sign, 30, color, weight=BOLD).move_to([x, y, 0])
                    for x in np.linspace(-4.5, 4.5, n)])


def crowd(y, xs=(-3.6, -2.6, -1.6, -0.6, 0.6, 1.6, 2.6, 3.6)):
    return VGroup(*[solute().scale(0.82).move_to([x, y + 0.18 * ((i % 3) - 1), 0])
                    for i, x in enumerate(xs)])


def add_world(scene):
    world, motes = membrane_world()
    scene.add(world, motes)
    return world, motes


def stream(scene, x, y0, y1, count=3, color=YELLOW, run_time=1.8):
    beads = [solute(color=color).scale(0.72).move_to([x, y0 + 0.22 * i, 0]) for i in range(count)]
    scene.add(*beads)
    scene.play(LaggedStart(*[b.animate.move_to([x, y1 - 0.18 * i, 0]) for i, b in enumerate(beads)],
                           lag_ratio=0.28), run_time=run_time, rate_func=linear)
    scene.play(*[FadeOut(b) for b in beads], run_time=0.18)


class S00Hook(SpokenScene):
    def construct(self):
        add_world(self)
        ion = solute().move_to([-2.6, 2.35, 0])
        self.play(FadeIn(ion), ion.animate.shift(RIGHT * 0.45 + UP * 0.12), run_time=0.8)
        self.at("opens a path")
        gate = pore(0, 0.20)
        self.play(GrowFromCenter(gate), gate[0].animate.shift(LEFT * 0.38),
                  gate[1].animate.shift(RIGHT * 0.38), ion.animate.move_to([-0.9, 1.35, 0]), run_time=1.1)
        self.at("travel uphill")
        uphill = Arrow([1.65, -2.6, 0], [1.65, 2.45, 0], color=RED,
                       stroke_width=10, max_tip_length_to_length_ratio=0.12).set_opacity(0.25)
        self.play(GrowArrow(uphill), ion.animate.shift(RIGHT * 0.18), run_time=0.9)
        self.at("doorway")
        self.play(Indicate(gate, color=TEAL, scale_factor=1.08), run_time=0.55)
        self.at("pump")
        pump = carrier(0, UP, TEAL)
        energy = chip("energy", GREEN, 28).move_to([2.9, 0.75, 0])
        self.play(ReplacementTransform(gate, pump), FadeIn(energy, shift=LEFT * 0.15), run_time=0.75)
        self.at("Follow one charged")
        self.play(ion.animate.move_to([0, 1.05, 0]), pump.animate.rotate(0.13), run_time=0.75)
        self.play(pump.animate.rotate(-0.13), ion.animate.shift(DOWN * 0.35), run_time=0.6)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Membrane structure & function"
    TITLE = "A Path Is Not a Pump"
    def construct(self):
        world, motes = membrane_world()
        ion = solute().scale(0.85).move_to([-2.8, 2.15, 0])
        shade = Rectangle(width=11.8, height=2.0, stroke_width=0,
                          fill_color=BG, fill_opacity=0.72).move_to([0, 0.65, 0])
        title = T(self.TITLE, 54, TEXT, font=TITLE_FONT)
        rule = Line([-1.5, -0.05, 0], [1.5, -0.05, 0], color=GOLD, stroke_width=5)
        self.add(world, motes, ion)
        self.play(FadeIn(shade), Write(title), GrowFromCenter(rule),
                  ion.animate.shift(RIGHT * 0.35 + UP * 0.08), run_time=0.8)
        self.play(ion.animate.shift(RIGHT * 0.25 + DOWN * 0.10), run_time=0.45)
        self.play(FadeOut(VGroup(shade, title, rule)), ion.animate.shift(RIGHT * 0.2), run_time=0.65)
        self.finish()


class S02Toll(SpokenScene):
    def construct(self):
        add_world(self)
        ion = solute().move_to([-1.0, 2.15, 0])
        drops = VGroup(*[Dot(radius=0.13, color=BLUE).move_to(
            ion.get_center() + 0.68 * np.array([np.cos(a), np.sin(a), 0])) for a in np.linspace(0, TAU, 7)[:-1]])
        self.play(FadeIn(ion), LaggedStart(*[FadeIn(d) for d in drops], lag_ratio=0.12), run_time=0.8)
        self.at("water shell")
        shell_l = T("water shell", 30, BLUE).move_to([2.4, 2.35, 0])
        self.play(FadeIn(shell_l), Rotate(drops, angle=0.7, about_point=ion.get_center()), run_time=0.8)
        self.at("enter the oily")
        self.play(VGroup(ion, drops).animate.shift(DOWN * 1.25), Rotate(drops, angle=0.7, about_point=ion.get_center()), run_time=0.9)
        self.at("must lose")
        bar_box = RoundedRectangle(width=0.75, height=4.2, corner_radius=0.14,
                                   stroke_color=GREY, stroke_width=3).move_to([4.8, 0.35, 0])
        fill = Rectangle(width=0.58, height=0.08, stroke_width=0,
                         fill_color=RED, fill_opacity=0.85).move_to([4.8, -1.67, 0])
        schematic = T("schematic", 28, GREY).move_to([4.8, -2.2, 0])
        targets = [d.get_center() + 0.85 * (d.get_center() - ion.get_center()) for d in drops]
        self.play(FadeIn(bar_box), FadeIn(schematic), FadeOut(shell_l),
                  *[d.animate.move_to(p).set_opacity(0.15) for d, p in zip(drops, targets)],
                  fill.animate.stretch_to_fit_height(3.75).move_to([4.8, 0.17, 0]), run_time=1.2)
        self.at("nothing in return")
        self.play(ion.animate.move_to([-1.0, 1.65, 0]), FadeIn(fill), run_time=0.8, rate_func=rush_from)
        self.at("toll for leaving water")
        toll = T("toll for leaving water", 30, RED).move_to([3.55, 3.15, 0])
        self.play(FadeIn(toll), Indicate(fill, color=RED, scale_factor=1.06), run_time=0.8)
        self.finish()


class S03Channel(SpokenScene):
    def construct(self):
        add_world(self)
        toll = Rectangle(width=0.6, height=3.8, stroke_width=0,
                         fill_color=RED, fill_opacity=0.8).move_to([0, 0.15, 0])
        self.add(toll)
        self.at("channel offers")
        ch = pore(0)
        grips = VGroup(*[Dot([sx * 0.50, y, 0], radius=0.10, color=BLUE)
                         for sx in (-1, 1) for y in (-0.85, -0.05)])
        self.play(ReplacementTransform(toll, ch), FadeIn(grips), run_time=0.9)
        self.at("polar pathway")
        labels = VGroup(T("polar pathway", 30, TEAL), T("schematic", 28, GREY)).arrange(DOWN, buff=0.1).move_to([3.25, 2.35, 0])
        self.play(FadeIn(labels), grips.animate.shift(UP * 0.12), run_time=0.65)
        self.at("replace some help")
        ion = solute().move_to([0, 2.2, 0])
        shell = VGroup(*[Dot(radius=0.11, color=BLUE).move_to(ion.get_center() +
                 0.55 * np.array([np.cos(a), np.sin(a), 0])) for a in np.linspace(0, TAU, 7)[:-1]])
        self.play(FadeIn(ion), FadeIn(shell), ion.animate.move_to([0, 0.45, 0]),
                  shell.animate.move_to([0, 1.25, 0]).set_opacity(0.2), run_time=1.0)
        self.at("lowering the toll")
        self.play(grips.animate.set_color(GREEN), ion.animate.move_to([0, -1.3, 0]), run_time=0.8)
        self.at("crosses much faster")
        self.play(FadeOut(VGroup(ion, shell, labels)), run_time=0.2)
        stream(self, 0, 2.2, -2.4, count=3, run_time=1.7)
        self.at("no directional energy")
        two_way = DoubleArrow([1.9, -1.8, 0], [1.9, 1.2, 0], color=GREY, stroke_width=5, buff=0.05).set_opacity(0.6)
        self.play(FadeIn(two_way), grips.animate.set_color(BLUE), run_time=0.65)
        self.finish()


class S04Gradient(SpokenScene):
    def construct(self):
        add_world(self)
        ch = pore(0)
        top = crowd(2.15)
        bottom = crowd(-2.35, xs=(-1.0, 1.0))
        self.add(ch, top, bottom)
        self.play(top.animate.shift(RIGHT * 0.12), bottom.animate.shift(LEFT * 0.12), run_time=0.6)
        self.at("electrochemical gradient")
        heading = T("electrochemical gradient", 34, TEXT, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(heading), top.animate.shift(LEFT * 0.12), run_time=0.6)
        self.at("Concentration pushes")
        ca = Arrow([-2.2, 1.55, 0], [-2.2, -1.65, 0], color=BLUE, stroke_width=8, buff=0)
        cl = T("concentration", 28, BLUE).next_to(ca, LEFT, buff=0.18)
        self.play(GrowArrow(ca), FadeIn(cl), run_time=0.8)
        self.at("Voltage pulls")
        minus = charge_row("−", -2.0, RED)
        plus = charge_row("+", 0.85, RED)
        va = Arrow([2.2, 1.55, 0], [2.2, -1.65, 0], color=RED, stroke_width=8, buff=0)
        vl = T("voltage", 28, RED).next_to(va, RIGHT, buff=0.18)
        self.play(FadeIn(minus), FadeIn(plus), GrowArrow(va), FadeIn(vl), run_time=0.95)
        self.at("Together")
        down = Arrow([0, 1.65, 0], [0, -2.15, 0], color=GREEN, stroke_width=13, buff=0)
        dl = T("electrochemical downhill", 30, GREEN).move_to([3.7, -3.15, 0])
        self.play(ReplacementTransform(VGroup(ca, va), down), FadeOut(VGroup(cl, vl, heading)), FadeIn(dl), run_time=0.8)
        stream(self, 0, 1.8, -2.35, count=2, run_time=1.25)
        self.finish()


def prediction_layout(question=False):
    ch = pore(0, 0.18)
    top = crowd(2.05)
    bottom = crowd(-2.45, xs=(-1.1, 1.1))
    labels = side_labels("outside: high sodium", "inside: negative")
    minus = charge_row("−", -1.75, RED, 6)
    outlines = VGroup(
        DashedLine([-2.0, 1.2, 0], [-2.0, -1.45, 0], color=BLUE, stroke_width=6),
        DashedLine([2.0, 1.2, 0], [2.0, -1.45, 0], color=RED, stroke_width=6),
        T("concentration", 28, BLUE).move_to([-3.35, 0.75, 0]),
        T("voltage", 28, RED).move_to([3.0, 0.75, 0]),
    ).set_opacity(0.45)
    q = T("?", 64, TEXT, weight=BOLD).move_to([0, 0.55, 0])
    fullq = T("Which way will sodium move?", 36, TEXT, weight=BOLD).move_to([0, 3.35, 0])
    return ch, top, bottom, labels, minus, outlines, q, fullq


class S05Predict(SpokenScene):
    def construct(self):
        add_world(self)
        ch, top, bottom, labels, minus, outlines, q, fullq = prediction_layout()
        self.play(FadeIn(top), FadeIn(bottom), FadeIn(labels[0]), run_time=0.7)
        self.at("interior is negative")
        self.play(FadeIn(labels[1]), FadeIn(minus), run_time=0.7)
        self.at("channel opens")
        self.play(FadeIn(ch), ch[0].animate.shift(LEFT * 0.38), ch[1].animate.shift(RIGHT * 0.38), run_time=0.75)
        self.at("which way")
        self.play(FadeIn(outlines), GrowFromCenter(q), run_time=0.7)
        self.at("Follow both pushes")
        self.play(outlines[:2].animate.set_opacity(0.85), top.animate.shift(RIGHT * 0.10),
                  minus.animate.set_opacity(0.65), run_time=0.8)
        self.finish()


class S06PredictHold(Scene):
    def construct(self):
        add_world(self)
        ch, top, bottom, labels, minus, outlines, q, fullq = prediction_layout(True)
        ch[0].shift(LEFT * 0.38); ch[1].shift(RIGHT * 0.38)
        self.add(ch, top, bottom, labels, minus, outlines, q, fullq)
        ring = Arc(radius=0.72, start_angle=PI / 2, angle=0.01, color=GOLD, stroke_width=5).move_to(q)
        self.add(ring)
        self.play(outlines[0].animate.set_opacity(1), minus.animate.set_opacity(0.55),
                  Create(Arc(radius=0.72, start_angle=PI / 2, angle=-PI, color=GOLD, stroke_width=5).move_to(q)), run_time=2.15)
        self.play(outlines[1].animate.set_opacity(1), minus.animate.set_opacity(1),
                  Create(Arc(radius=0.72, start_angle=-PI / 2, angle=-PI, color=GOLD, stroke_width=5).move_to(q)), run_time=2.15)
        self.wait(0.2)


class S07Answer(SpokenScene):
    def construct(self):
        add_world(self)
        ch, top, bottom, labels, minus, outlines, q, fullq = prediction_layout()
        ch[0].shift(LEFT * 0.38); ch[1].shift(RIGHT * 0.38)
        self.add(ch, top, bottom, labels, minus, outlines, q)
        self.at("Concentration pushes")
        a1 = Arrow([-1.6, 1.35, 0], [-1.6, -1.55, 0], color=BLUE, stroke_width=8, buff=0)
        self.play(ReplacementTransform(outlines[0], a1), outlines[2].animate.set_opacity(1), run_time=0.8)
        self.at("negative interior")
        a2 = Arrow([1.6, 1.35, 0], [1.6, -1.55, 0], color=RED, stroke_width=8, buff=0)
        self.play(ReplacementTransform(outlines[1], a2), outlines[3].animate.set_opacity(1),
                  minus.animate.set_opacity(0.65), run_time=0.8)
        self.at("Both pushes agree")
        down = Arrow([0, 1.65, 0], [0, -2.05, 0], color=GREEN, stroke_width=13, buff=0)
        check = T("✓", 58, GREEN, weight=BOLD).move_to(q)
        self.play(ReplacementTransform(VGroup(a1, a2), down), ReplacementTransform(q, check),
                  FadeOut(outlines[2:]), run_time=0.75)
        self.at("speeds sodium downhill")
        stream(self, 0, 2.2, -2.45, count=4, run_time=1.35)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        add_world(self)
        ch = pore(0)
        outside = crowd(2.1, xs=(-1.0, 1.0))
        inside = crowd(-2.35)
        labels = side_labels("outside: low sodium", "inside: positive")
        signs = charge_row("+", -1.78, RED, 6)
        down = Arrow([0, 1.45, 0], [0, -2.0, 0], color=GREEN, stroke_width=12, buff=0)
        self.add(ch, down, outside, inside)
        self.at("reverse the combined")
        up = Arrow([0, -2.0, 0], [0, 1.45, 0], color=GREEN, stroke_width=12, buff=0)
        self.play(ReplacementTransform(down, up), FadeIn(labels), FadeIn(signs),
                  inside.animate.shift(RIGHT * 0.1), run_time=1.0)
        self.at("opposite way")
        stream(self, 0, -2.35, 2.15, count=3, run_time=1.5)
        self.at("changes speed")
        gauge = RoundedRectangle(width=2.2, height=1.15, corner_radius=0.18,
                                 stroke_color=GREY, stroke_width=3).move_to([4.65, 1.8, 0])
        gauge_l = VGroup(T("speed", 28, TEXT), T("schematic", 28, GREY)).arrange(DOWN, buff=0.06).move_to([4.65, 2.0, 0])
        needle = Line([4.65, 1.5, 0], [5.25, 1.78, 0], color=TEAL, stroke_width=7)
        self.play(FadeIn(gauge), FadeIn(gauge_l), GrowFromPoint(needle, [4.65, 1.5, 0]), run_time=0.75)
        self.at("not the downhill")
        self.play(Rotate(needle, -0.65, about_point=[4.65, 1.5, 0]),
                  Indicate(up, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("uphill transport requires")
        bad = Arrow([-2.1, 1.1, 0], [-2.1, -1.45, 0], color=RED, stroke_width=8, buff=0)
        cross = Cross(bad, stroke_color=RED, stroke_width=7)
        self.play(GrowArrow(bad), Create(cross), Rotate(needle, 0.45, about_point=[4.65, 1.5, 0]), run_time=0.8)
        self.at("energy coupling")
        self.play(Indicate(VGroup(bad, cross), color=RED, scale_factor=1.07),
                  Rotate(needle, -0.35, about_point=[4.65, 1.5, 0]), run_time=0.7)
        self.finish()


class S09Mechanisms(SpokenScene):
    def construct(self):
        add_world(self)
        ch = pore(-3.1)
        car = carrier(3.1, UP)
        labs = VGroup(T("channel: pore", 30, TEAL).move_to([-3.1, 2.95, 0]),
                      T("carrier: alternating access", 30, TEAL).move_to([3.1, 2.95, 0]))
        self.play(FadeIn(ch), FadeIn(labs[0]), run_time=0.7)
        self.at("open to both sides")
        stream(self, -3.1, 2.0, -2.25, count=3, run_time=1.35)
        self.at("Carriers instead bind")
        cargo = solute().move_to([3.1, 2.0, 0])
        self.play(FadeIn(car), FadeIn(labs[1]), FadeIn(cargo), cargo.animate.move_to([3.1, 0.28, 0]), run_time=0.85)
        self.at("change shape")
        closed = RoundedRectangle(width=1.65, height=2.1, corner_radius=0.38,
                                  stroke_color=TEAL, stroke_width=5, fill_color=TEAL,
                                  fill_opacity=0.24).move_to([3.1, MEM_Y, 0])
        self.play(ReplacementTransform(car, closed), Rotate(VGroup(closed, cargo), PI, about_point=[3.1, MEM_Y, 0]), run_time=1.0)
        self.at("release it")
        car2 = carrier(3.1, DOWN)
        self.play(ReplacementTransform(closed, car2), cargo.animate.move_to([3.1, -2.25, 0]), run_time=0.9)
        self.at("Either mechanism")
        downhill = Arrow([-5.0, 1.45, 0], [5.0, -2.15, 0], color=GREEN, stroke_width=9, buff=0)
        self.play(GrowArrow(downhill), Indicate(VGroup(ch, car2), color=TEAL, scale_factor=1.04), run_time=1.0)
        self.finish()


def battery(x=4.8, y=1.95, fill=0.0):
    shell = RoundedRectangle(width=1.25, height=2.25, corner_radius=0.16,
                             stroke_color=GREEN, stroke_width=4).move_to([x, y, 0])
    nub = Rectangle(width=0.42, height=0.18, stroke_color=GREEN, stroke_width=3).next_to(shell, UP, buff=0)
    h = max(0.06, 1.85 * fill)
    liquid = Rectangle(width=0.92, height=h, stroke_width=0, fill_color=GREEN,
                       fill_opacity=0.75).move_to([x, y - 0.92 + h / 2, 0])
    return VGroup(shell, nub, liquid)


class S10Pump(SpokenScene):
    def construct(self):
        add_world(self)
        pump = carrier(0, DOWN, TEAL, 1.18)
        grad = Arrow([2.4, 1.4, 0], [2.4, -1.7, 0], color=GREEN, stroke_width=9, buff=0)
        self.play(FadeIn(pump), FadeIn(grad), run_time=0.7)
        self.at("energy source")
        atp = chip("ATP", GREEN, 30).move_to([-3.1, -2.25, 0])
        self.play(FadeIn(atp), atp.animate.move_to([-1.25, -1.0, 0]), run_time=0.8)
        self.at("only sodium")
        lab = VGroup(T("sodium-potassium pump", 30, TEAL, weight=BOLD),
                     T("sodium side only", 28, GREY)).arrange(DOWN, buff=0.1).move_to([0, 3.0, 0])
        na = solute("+").move_to([0, -2.35, 0])
        self.play(FadeIn(lab), FadeIn(na), run_time=0.65)
        self.at("A TP drives")
        self.play(Indicate(atp, color=GREEN, scale_factor=1.08),
                  na.animate.move_to([0, -0.75, 0]), run_time=0.8)
        self.at("shape change")
        self.play(Rotate(VGroup(pump, na), PI, about_point=[0, MEM_Y, 0]),
                  FadeOut(atp), run_time=1.0)
        self.at("sodium uphill")
        self.play(na.animate.move_to([0, 2.25, 0]), run_time=0.85)
        self.at("charging the gradient battery")
        bat0 = battery(fill=0.05); bat1 = battery(fill=1.0)
        extra = crowd(2.15, xs=(-1.8, -0.9, 0.9, 1.8))
        self.play(FadeIn(bat0), FadeIn(extra), run_time=0.35)
        self.play(ReplacementTransform(bat0, bat1), extra.animate.shift(RIGHT * 0.12),
                  pump.animate.rotate(0.16), run_time=1.0)
        self.finish()


class S11Coupling(SpokenScene):
    def construct(self):
        add_world(self)
        pump = carrier(-4.35, UP, TEAL, 0.72)
        bat = battery(-5.7, 2.0, 1.0)
        crowd_top = crowd(2.25, xs=(-3.2, -2.4, -1.6, -0.8))
        coupled = carrier(2.0, UP, TEAL, 1.15)
        self.add(pump, bat, crowd_top)
        self.at("coupled carrier")
        label = T("sodium-glucose carrier", 30, TEAL, weight=BOLD).move_to([2.1, 3.15, 0])
        self.play(FadeIn(coupled), FadeIn(label), pump.animate.rotate(0.12), run_time=0.8)
        self.at("Sodium runs downhill")
        ramp1 = Arrow([0.2, 2.0, 0], [1.55, 0.25, 0], color=GREEN, stroke_width=9, buff=0)
        nas = VGroup(solute().scale(0.72).move_to([0.1, 2.35, 0]),
                     solute().scale(0.72).move_to([-0.35, 2.7, 0]))
        self.play(GrowArrow(ramp1), FadeIn(nas), nas.animate.shift(RIGHT * 1.55 + DOWN * 1.8), run_time=1.0)
        self.at("Glucose travels uphill")
        gear = Circle(radius=0.48, stroke_color=GOLD, stroke_width=6).move_to([2.0, MEM_Y, 0])
        gear.add(*[Line(gear.point_at_angle(a), gear.point_at_angle(a) * 0 + gear.get_center() +
                        0.68 * np.array([np.cos(a), np.sin(a), 0]), color=GOLD, stroke_width=5)
                   for a in np.linspace(0, TAU, 8, endpoint=False)])
        glucose = chip("glucose", BLUE, 28).move_to([3.7, 2.25, 0])
        ramp2 = Arrow([4.85, 1.55, 0], [4.85, -1.55, 0], color=RED, stroke_width=8, buff=0)
        self.play(FadeIn(gear), GrowArrow(ramp2), FadeIn(glucose), Rotate(gear, -1.5),
                  glucose.animate.move_to([2.45, -1.65, 0]), run_time=1.15)
        self.at("No ATP")
        no_atp = T("no ATP here", 28, TEXT).move_to([4.8, -2.9, 0])
        self.play(FadeIn(no_atp), FadeOut(glucose), Rotate(gear, -0.8), run_time=0.7)
        self.at("ultimately depends")
        link = CurvedArrow([1.15, -1.7, 0], [-4.4, -1.25, 0], angle=-0.25,
                           color=GREEN, stroke_width=5)
        self.play(Create(link), Indicate(bat, color=GREEN, scale_factor=1.06),
                  pump.animate.rotate(-0.22), run_time=1.0)
        self.finish()


class S12Classify(SpokenScene):
    def construct(self):
        add_world(self)
        ch = pore(-3.2)
        car = carrier(3.2, UP)
        self.play(FadeIn(ch), FadeIn(car), run_time=0.7)
        self.at("three questions")
        nums = VGroup(*[T(str(i), 32, GOLD, weight=BOLD).move_to([-5.7, y, 0]) for i, y in enumerate((2.8, 0.75, -2.75), 1)])
        self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.2), run_time=0.7)
        self.at("route a poor")
        # Transcript says "poor" for pore; the on-screen scientific term remains correct.
        routes = VGroup(T("pore", 30, TEAL).move_to([-3.2, 2.9, 0]),
                        T("alternating access", 30, TEAL).move_to([3.2, 2.9, 0]))
        self.play(FadeIn(routes), Indicate(VGroup(ch, car), color=TEAL, scale_factor=1.04), run_time=0.85)
        self.at("downhill or uphill")
        test = solute().move_to([-1.0, 1.45, 0])
        down = Arrow([-1.0, 1.1, 0], [-1.0, -1.65, 0], color=GREEN, stroke_width=8, buff=0)
        up = Arrow([1.0, -1.65, 0], [1.0, 1.1, 0], color=RED, stroke_width=8, buff=0)
        self.play(FadeIn(test), GrowArrow(down), test.animate.move_to([-1.0, -2.1, 0]), run_time=0.8)
        self.play(test.animate.move_to([1.0, -2.1, 0]), GrowArrow(up), run_time=0.55)
        self.at("what supplies energy")
        atp = chip("ATP", GREEN, 28).move_to([4.9, -2.55, 0])
        partner = VGroup(solute().scale(0.7), T("downhill flow", 28, GREEN)).arrange(RIGHT, buff=0.15).move_to([-3.5, -2.65, 0])
        self.play(FadeIn(atp), FadeIn(partner), run_time=0.65)
        self.at("another downhill flow")
        self.play(atp.animate.shift(LEFT * 0.45), partner.animate.shift(RIGHT * 0.45),
                  car.animate.rotate(0.18), run_time=0.8)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        add_world(self)
        gate = pore(0)
        ion = solute().move_to([0, -2.2, 0])
        uphill = Arrow([2.0, -2.35, 0], [2.0, 2.25, 0], color=RED,
                       stroke_width=11, buff=0).set_opacity(0.28)
        self.add(gate, ion, uphill)
        self.at("cannot push")
        self.play(ion.animate.move_to([0, -0.1, 0]), run_time=0.7)
        self.play(ion.animate.move_to([0, -1.75, 0]), run_time=0.65, rate_func=rush_from)
        self.at("Look for energy coupling")
        car = carrier(0, DOWN)
        atp = chip("ATP", GREEN, 28).move_to([-3.2, -1.65, 0])
        partner = VGroup(solute().scale(0.68), T("downhill partner", 28, GREEN)).arrange(RIGHT, buff=0.12).move_to([-3.2, 1.65, 0])
        self.play(ReplacementTransform(gate, car), FadeIn(atp), run_time=0.75)
        self.play(atp.animate.move_to([-1.25, -0.9, 0]), car.animate.rotate(0.16),
                  ion.animate.move_to([0, 0.65, 0]), run_time=0.75)
        self.at("calling transport uphill")
        self.play(FadeIn(partner), partner.animate.shift(RIGHT * 0.35),
                  ion.animate.move_to([0, 1.55, 0]), run_time=0.8)
        self.at("Only coupled energy")
        bat = battery(4.8, 1.5, 0.85)
        solid = Arrow([2.0, -2.35, 0], [2.0, 2.25, 0], color=GREEN, stroke_width=12, buff=0)
        self.play(ReplacementTransform(uphill, solid), FadeIn(bat),
                  Indicate(VGroup(atp, partner), color=GREEN, scale_factor=1.06), run_time=0.9)
        self.at("drive transport uphill")
        self.play(ion.animate.move_to([0, 2.45, 0]), Indicate(bat, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "Only coupled energy can drive transport uphill."
    def construct(self):
        world, motes = membrane_world()
        arrow = Arrow([3.9, -2.2, 0], [3.9, 2.1, 0], color=GREEN, stroke_width=10, buff=0)
        atp = chip("ATP", GREEN, 28).move_to([5.2, -1.7, 0])
        ion = solute().scale(0.78).move_to([3.9, -1.8, 0])
        shade = RoundedRectangle(width=8.2, height=1.75, corner_radius=0.2,
                                 stroke_width=0, fill_color=BG, fill_opacity=0.78).move_to([-1.25, 0.25, 0])
        line = VGroup(T("Only coupled energy can", 42, TEXT, font=TITLE_FONT),
                      T("drive transport uphill.", 42, TEXT, font=TITLE_FONT))
        line.arrange(DOWN, buff=0.15).move_to([-1.25, 0.25, 0])
        self.add(world, motes, arrow, atp, ion)
        self.play(FadeIn(shade), FadeIn(line, shift=UP * 0.12),
                  ion.animate.move_to([3.9, 0.2, 0]), run_time=1.25)
        self.play(ion.animate.move_to([3.9, 2.0, 0]), Indicate(atp, color=GREEN, scale_factor=1.05), run_time=1.55)
        self.wait(0.7)

