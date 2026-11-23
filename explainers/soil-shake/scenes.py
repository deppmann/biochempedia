"""Soil Shake, a continuous view of one jar on a kitchen table."""

from bp_parts import *
from bp_style import EndCard, TitleCard

# Color map: teal plastic and water, gold sand and tape, ochre silt,
# terracotta clay, dark brown plant bits, red hazards, green approved materials.
PLASTIC = "#94D4D7"
WATER = "#468992"
MUD = "#89624E"
SAND = "#E9B471"
SILT = "#BA8050"
CLAY = "#AA6256"
PLANTS = "#3C2827"
PAPER = "#F1E6D2"
INK = "#273842"
TABLE = "#584435"
TOWEL = "#426568"
JAR_X = 3.25
BOTTOM, TOP, SURFACE = -2.46, 2.35, 1.62
HALF = 1.84
SAND_TOP, SILT_TOP, CLAY_TOP = -1.68, -1.02, -0.43
SOIL_TOP = BOTTOM + (TOP - BOTTOM) / 3


def p(x, y):
    return np.array([x, y, 0.0])


def rect(w, h, x, y, color, radius=0.08, opacity=1, edge=None, stroke=2):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            fill_color=color, fill_opacity=opacity,
                            stroke_color=edge or color, stroke_width=stroke).move_to(p(x, y))


def poly(points, color, edge=None, stroke=0):
    return Polygon(*(p(x, y) for x, y in points), fill_color=color,
                   fill_opacity=1, stroke_color=edge or color, stroke_width=stroke)


def line(x1, y1, x2, y2, color, width=3):
    return Line(p(x1, y1), p(x2, y2), color=color, stroke_width=width)


def label(words, y, color=TEXT, x=-3.4, size=34):
    return fit_text(words, max_w=5.7, size=size, min_size=28, color=color).move_to(p(x, y))


def layer_label(words, lo, hi, color, x):
    name = boxed_label(words, color, size=34, pad=0.10, stroke=0)
    name.box.set_fill(BG, opacity=1)
    return name.move_to(p(x, (lo + hi) / 2))


def tabletop():
    counter_top = poly([(-6.8, -1.38), (6.8, -1.38), (6.8, -3.78), (-6.8, -3.78)], TABLE)
    towel = poly([(0.48, -1.96), (5.54, -1.96), (6.53, -3.12), (-0.41, -3.12)],
                 TOWEL, PLASTIC, 1.5)
    hem = line(-0.15, -2.98, 6.27, -2.98, "#719194", 2)
    return VGroup(counter_top, towel, hem)


def jar_band(lo, hi, color, opacity=1):
    band = rect(2 * HALF - 0.12, hi - lo, JAR_X, (hi + lo) / 2, color,
                min(0.12, (hi - lo) / 3), opacity, stroke=0)
    return band


def lid():
    cap = rect(3.0, 0.58, JAR_X, 2.52, "#557D82", 0.13, edge=PLASTIC, stroke=3)
    ribs = VGroup(*(line(x, 2.39, x, 2.65, PLASTIC, 2)
                    for x in np.linspace(JAR_X - 1.32, JAR_X + 1.32, 15)))
    return VGroup(cap, ribs)


def particles(lo, hi, count, radius, color, seed, speed=0, side=1.60):
    """Seeded grains. The fixed seed preserves the same landmarks between cuts."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        x = rng.uniform(-side, side)
        y = rng.uniform(lo + radius, hi - radius)
        r = radius * rng.uniform(0.64, 1.08)
        phase = rng.uniform(0, 2 * np.pi)
        dot = Dot(p(JAR_X + x, y), radius=r, color=color, stroke_width=0)
        if speed:
            def drift(mob, dt, x=x, y=y, phase=phase):
                phase_now = mob.drift_time * speed
                mob.move_to(p(JAR_X + x + 0.11 * (np.sin(phase_now + phase) - np.sin(phase)),
                              y + 0.10 * (np.cos(phase_now + phase) - np.cos(phase))))
                mob.drift_time += dt

            dot.drift_time = 0
            dot.add_updater(drift)
        dots.add(dot)
    return dots


def water_sheen(lo, hi, speed):
    """Broad reflected light and suspended sediment move within the liquid."""
    streaks = VGroup()
    for i, (x, y, width, height) in enumerate([
        (2.86, lo + (hi - lo) * 0.32, 1.74, 0.43),
        (3.60, lo + (hi - lo) * 0.57, 1.85, 0.48),
        (2.95, lo + (hi - lo) * 0.80, 1.97, 0.37),
    ]):
        shape = Ellipse(width=width, height=height, fill_color="#F3DDBB",
                        fill_opacity=0.23, stroke_width=0).move_to(p(x, y))
        if speed:
            bob(shape, amp=0.13, speed=speed, seed=i)
            def glimmer(mob, x=x, i=i):
                mob.set_x(x + 0.42 * np.sin(mob._bob_t * speed + i))
                mob.set_fill(opacity=0.20 + 0.10 * np.cos(mob._bob_t * speed + i))
            shape.add_updater(glimmer)
        streaks.add(shape)
    return streaks


def flecks():
    pieces = VGroup()
    for i, (x, y) in enumerate(zip([1.92, 2.32, 2.94, 3.53, 4.16, 4.60],
                                  [1.57, 1.65, 1.59, 1.67, 1.58, 1.64])):
        leaf = poly([(-0.17, 0.02), (-0.06, -0.06), (0.13, -0.07),
                     (0.19, 0.06), (0.0, 0.09)], PLANTS)
        pieces.add(leaf.rotate((i - 2) * 0.16).move_to(p(x, y)))
    return pieces


def tape(y):
    return rect(0.65, 0.15, 4.98, y, "#F4D790", 0.035, edge="#FFE9B2")


def settled_layer(name):
    lo, hi, color, count, radius, seed = {
        "sand": (BOTTOM, SAND_TOP, SAND, 42, 0.066, 8),
        "silt": (SAND_TOP, SILT_TOP, SILT, 66, 0.037, 12),
        "clay": (SILT_TOP, CLAY_TOP, CLAY, 79, 0.022, 17),
    }[name]
    return VGroup(jar_band(lo, hi, color),
                  particles(lo + 0.05, hi - 0.04, count, radius, "#784B3A", seed))


def jar(state="empty", drift=0, capped=True):
    """Build the same jar at each stage, including the same boundaries and tape positions."""
    # The shoulders taper to the mouth above the straight-sided vessel.
    left, right = JAR_X - HALF, JAR_X + HALF
    back = VMobject(fill_color="#355359", fill_opacity=1, stroke_color=PLASTIC, stroke_width=3)
    back.start_new_path(p(JAR_X - 1.36, 2.33))
    back.add_line_to(p(JAR_X + 1.36, 2.33))
    back.add_cubic_bezier_curve_to(p(JAR_X + 1.68, 2.33), p(right, 2.12), p(right, 1.84))
    back.add_line_to(p(right, -2.19))
    back.add_cubic_bezier_curve_to(p(right, -2.43), p(right - 0.16, -2.53), p(right - 0.33, -2.53))
    back.add_line_to(p(left + 0.33, -2.53))
    back.add_cubic_bezier_curve_to(p(left + 0.16, -2.53), p(left, -2.43), p(left, -2.19))
    back.add_line_to(p(left, 1.84))
    back.add_cubic_bezier_curve_to(p(left, 2.12), p(JAR_X - 1.68, 2.33), p(JAR_X - 1.36, 2.33))
    back.close_path()
    shine = line(1.64, -1.98, 1.64, 1.97, "#A1CDCA", 2).set_opacity(0.66)
    neck = rect(2.77, 0.25, JAR_X, 2.32, "#52797C", 0.08, edge=PLASTIC)
    top = lid()
    liquid, grit, layers, marks = VGroup(), VGroup(), VGroup(), VGroup()
    floating = VGroup()
    if state in {"filled", "muddy", "hint", "sand", "silt", "settled"}:
        color = {"filled": WATER, "muddy": MUD, "hint": "#956E59",
                 "sand": "#A58C70", "silt": "#8F8F78", "settled": "#668D89"}[state]
        liquid.add(jar_band(BOTTOM + 0.06, SURFACE, color),
                   line(1.55, SURFACE, 4.95, SURFACE, "#D9BCA0" if state != "filled" else PLASTIC, 2))
    if state in {"filled", "dry"}:
        layers.add(jar_band(BOTTOM + 0.06, SOIL_TOP, MUD),
                   particles(BOTTOM + 0.10, SOIL_TOP - 0.07, 64, 0.053, SAND, 3))
    if state in {"muddy", "hint", "sand", "silt", "settled"}:
        floor = {"muddy": BOTTOM + 0.19, "hint": -2.06, "sand": SAND_TOP,
                 "silt": SILT_TOP, "settled": CLAY_TOP}[state]
        for count, radius, color, seed in [(24, 0.092, SAND, 2), (30, 0.055, "#CB9770", 4),
                                           (37, 0.030, "#E5AF94", 7)]:
            remaining = count if state in {"muddy", "hint"} else (0 if seed == 2 else count // 2)
            if state in {"silt", "settled"}:
                remaining = (count // 4 if seed == 7 else 0)
            grit.add(*particles(floor + 0.17, SURFACE - 0.15, remaining, radius, color, seed, drift))
    if drift and state in {"muddy", "hint", "sand", "silt", "settled"}:
        water_floor = {"muddy": -1.8, "hint": -1.8, "sand": -1.1, "silt": -0.5,
                       "settled": -0.28}[state]
        liquid.add(water_sheen(water_floor, SURFACE - 0.30, drift))
    if state == "hint":
        layers.add(jar_band(BOTTOM + 0.07, -2.06, "#AA7B55"),
                   jar_band(-2.06, -1.92, "#A97D65"))
    if state in {"sand", "silt", "settled"}:
        layers.add(settled_layer("sand"))
        marks.add(tape(SAND_TOP))
        floating = flecks()
    if state in {"silt", "settled"}:
        layers.add(settled_layer("silt"))
        marks.add(tape(SILT_TOP))
    if state == "settled":
        layers.add(settled_layer("clay"))
        marks.add(tape(CLAY_TOP))
    group = VGroup(back, liquid, grit, layers, floating, shine, neck, marks)
    if capped:
        group.add(top)
    group.liquid, group.grit, group.layers = liquid, grit, layers
    group.floating, group.marks, group.lid = floating, marks, top
    return group


def soil_bag():
    bag = poly([(-0.95, -1.11), (0.95, -1.11), (0.88, 0.67), (0.67, 1.10),
                (-0.67, 1.10), (-0.88, 0.67)], "#9A634B", "#E0A37E", 3)
    seal = line(-0.66, 0.90, 0.66, 0.90, "#E0A37E", 3)
    strip = rect(1.53, 0.71, 0, 0.06, "#E6BD8E", 0.08, stroke=0)
    mound = poly([(-0.60, -0.16), (-0.41, 0.00), (-0.21, 0.08), (0, 0.26),
                  (0.20, 0.17), (0.38, 0.02), (0.60, -0.16)], "#613C37")
    return VGroup(bag, seal, strip, mound)


def pitcher():
    handle = Circle(radius=0.44, color=PLASTIC, stroke_width=5).move_to(p(0.52, 0.07))
    jug = poly([(-0.62, 0.63), (-0.39, 0.41), (-0.35, -0.64), (0.55, -0.64),
                (0.57, 0.59)], WATER, PLASTIC, 3)
    level = line(-0.36, 0.16, 0.55, 0.16, PLASTIC, 2)
    return VGroup(handle, jug, level)


def ruler(vertical=False):
    block = rect(2.45, 0.38, 0, 0, "#E4C290", 0.04, stroke=0)
    ticks = VGroup(*(line(-1.09 + i * 0.155, 0.18, -1.09 + i * 0.155,
                          0.01 if i % 5 == 0 else 0.09, INK, 1.5) for i in range(15)))
    stick = VGroup(block, ticks)
    if vertical:
        stick.scale(1.54).rotate(PI / 2).move_to(p(5.85, -0.84))
    return stick


def marker():
    return VGroup(rect(1.33, 0.29, 0, 0, GOLD, 0.06),
                  rect(0.42, 0.33, 0.5, 0, INK, 0.05, edge=PLASTIC))


def tape_roll():
    return VGroup(Circle(radius=0.41, color="#F4D790", stroke_width=13),
                  Circle(radius=0.28, color="#C49A61", stroke_width=2))


def magnifier():
    return VGroup(Circle(radius=0.39, color=PLASTIC, stroke_width=5),
                  line(0.28, -0.28, 0.68, -0.68, PLASTIC, 8))


def pencil():
    return VGroup(rect(0.85, 0.15, 0, 0, GOLD, 0.03),
                  poly([(0.41, -0.08), (0.68, 0), (0.41, 0.08)], PAPER),
                  poly([(0.58, -0.025), (0.68, 0), (0.58, 0.025)], INK)).rotate(PI / 5)


def clock_face():
    return VGroup(Circle(radius=0.45, color=GOLD, stroke_width=4,
                         fill_color=BG, fill_opacity=1),
                  line(0, 0, 0, 0.29, GOLD, 3), line(0, 0, 0.25, -0.09, GOLD, 3))


def pebble():
    return poly([(-0.36, -0.14), (-0.28, 0.14), (-0.09, 0.29),
                 (0.19, 0.23), (0.37, 0.04), (0.24, -0.22), (-0.14, -0.24)], "#A9AAA3")


def leaf():
    return VGroup(poly([(-0.40, -0.15), (-0.24, 0.12), (0.12, 0.22),
                        (0.42, 0.10), (0.21, -0.15), (-0.09, -0.24)], "#9E573E"),
                  line(-0.40, -0.16, 0.29, 0.07, "#E0AA74", 2))


def root():
    return VGroup(line(-0.38, 0.32, -0.11, 0.07, MUD, 5),
                  line(-0.11, 0.07, 0.10, -0.15, MUD, 5),
                  line(0.10, -0.15, 0.37, -0.31, MUD, 5),
                  line(-0.04, 0.01, 0.26, 0.12, MUD, 3),
                  line(0.10, -0.15, -0.05, -0.41, MUD, 3))


def soil_sample():
    paper = rect(5.18, 2.88, -3.35, 0.05, PAPER, 0.12)
    rng = np.random.default_rng(34)
    grains = VGroup(*(Dot(p(-3.35 + x, 0.01 + y), radius=rng.uniform(0.023, 0.065),
                          color=rng.choice([MUD, SAND, SILT, PLANTS]))
                      for x, y in rng.uniform((-1.23, -0.42), (1.23, 0.42), (76, 2))))
    pieces = VGroup(pebble().scale(0.34).move_to(p(-4.65, 0.02)),
                    root().scale(0.41).move_to(p(-3.34, 0.03)),
                    leaf().scale(0.40).move_to(p(-2.03, -0.02)))
    return paper, grains, pieces


def drawing(x=-3.4, y=0.2):
    sheet = rect(3.47, 2.56, 0, 0, PAPER, 0.11)
    sketch = rect(1.62, 1.58, 0, -0.03, PAPER, 0.17, 0, edge="#537882", stroke=5)
    cap = rect(1.42, 0.20, 0, 0.82, "#537882", 0.05)
    scribble = VGroup(*(line(-0.69 + 0.23 * i, -0.63, -0.42 + 0.23 * i,
                              0.11 + 0.12 * (i % 3), "#A46E4E", 3) for i in range(6)))
    return VGroup(sheet, sketch, cap, scribble).move_to(p(x, y))


def folder():
    tab = rect(0.83, 0.31, -5.63, -2.38, "#CB955F", 0.08, stroke=0)
    cover = rect(2.22, 0.72, -5.03, -2.78, "#DDA569", 0.08, stroke=0)
    seam = line(-6.01, -2.58, -4.05, -2.58, "#F5C897", 2)
    return VGroup(tab, cover, seam)


def no_symbol(subject):
    center = subject.get_center()
    ring = Circle(radius=max(subject.width, subject.height) * 0.64,
                  color=RED, stroke_width=5).move_to(center)
    slash = Line(ring.point_at_angle(3 * PI / 4), ring.point_at_angle(-PI / 4),
                 color=RED, stroke_width=5)
    return VGroup(subject, ring, slash)


def hand(x=0, y=0, color="#E7AC86"):
    outline = dict(stroke_color="#9D654E", stroke_width=1.7)
    palm = Ellipse(width=0.68, height=0.61, fill_color=color, fill_opacity=1, **outline)
    fingers = VGroup(*(Ellipse(width=0.16, height=0.51 - 0.045 * abs(i - 1),
                               fill_color=color, fill_opacity=1, **outline)
                       .move_to(p(-0.23 + 0.15 * i, 0.27)) for i in range(4)))
    thumb = Ellipse(width=0.22, height=0.36, fill_color=color, fill_opacity=1, **outline)
    thumb.move_to(p(0.26, 0.06)).rotate(-0.55)
    return VGroup(palm, fingers, thumb).move_to(p(x, y))


def person(child=False, seated=False):
    skin = "#E7AC86" if child else "#BF856B"
    shirt = "#D6A36A" if child else "#61858A"
    head = Circle(radius=0.46, fill_color=skin, fill_opacity=1, stroke_width=0).move_to(UP * 1.28)
    eyes = VGroup(Dot(p(-0.14, 1.31), radius=0.038, color=INK),
                  Dot(p(0.17, 1.31), radius=0.038, color=INK))
    body = rect(1.05, 1.23, 0, 0.11, shirt, 0.26, stroke=0)
    legs = VGroup(line(-0.22, -0.36, -0.49 if seated else -0.30, -1.18, shirt, 18),
                  line(0.20, -0.36, 0.58 if seated else 0.31, -1.18, shirt, 18))
    arms = VGroup(line(-0.40, 0.44, -0.75, -0.02, skin, 13),
                  line(0.40, 0.44, 0.75, -0.02, skin, 13))
    return VGroup(legs, body, arms, head, eyes).scale(0.76 if child else 1)


def chips_for_prediction():
    options = VGroup()
    for name, radius, color, y in (("silt", 0.13, "#E4AA79", 0.72), ("clay", 0.074, "#EAA08D", 0.0),
                                    ("sand", 0.19, SAND, -0.72)):
        chip = boxed_label(name, color, size=30, box=(1.58, 0.54), pad=0.12).move_to(p(-3.08, y))
        grain = Dot(p(-4.37, y), radius=radius, color=color)
        options.add(VGroup(grain, chip))
    return options


def prediction_card():
    return question_card("Which settles first?\nWhich takes longest?", y=2.09,
                         left=-5.86, max_w=5.7, size=39)


def rise_from_bottom(mob):
    """Reveal a rising fill while its side walls stay in place."""
    full = mob.copy()
    mob.stretch(0.035, dim=1, about_edge=DOWN)
    return Transform(mob, full)


def light_on_layer(lo, hi):
    return jar_band(lo + 0.035, hi - 0.035, "#FFE0A0", 0.5)


class JarScene(SpokenScene):
    def table(self, saved=False):
        self.add(tabletop())
        if saved:
            self.add(folder())

    def put(self, mob, duration=0.55, shift=UP * 0.17):
        self.play(FadeIn(mob, shift=shift), run_time=duration)


class S01Hook(JarScene, TitleCard):
    LESSON = "Soil Shake"
    TITLE = "Soil Shake: Parent Guide"

    def construct(self):
        self.table()
        vessel = jar("muddy", drift=2.4)
        self.add(vessel)
        self.at("is dirt just dirt")
        self.put(label("Is dirt just dirt?", 1.62, GOLD, size=49))
        self.at("this cloudy jar holds")
        self.play(vessel.liquid.animate.set_opacity(0.92), run_time=1.65)
        self.at("after a shake")
        hint = jar("hint", drift=1.1).layers
        self.play(FadeIn(hint), run_time=2.45)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Soil Shake"
    TITLE = "Soil Shake: Parent Guide"

    def construct(self):
        self.add(tabletop(), jar("hint", drift=0.8))
        title = T(self.LESSON, 59, font=TITLE_FONT).move_to(p(-3.38, 0.95))
        rule = line(-4.55, 0.31, -2.21, 0.31, GOLD, 4)
        self.play(FadeIn(title), GrowFromCenter(rule), run_time=0.55)
        self.wait(1.40)


class S03Payoff(JarScene):
    def construct(self):
        self.table()
        self.add(jar("hint", drift=1.6))
        self.at("it takes about")
        timing = boxed_label("About 20 minutes", GOLD, size=33).move_to(p(-3.45, 1.95))
        self.put(timing)
        self.at("plus a few quick looks")
        timing_line = line(-5.22, 1.37, -1.68, 1.37, GOLD, 4)
        self.play(Create(timing_line), run_time=1.35)
        for cue, icon, name, y in [
            ("looking closely", magnifier(), "Look closely", 0.80),
            ("making a guess", pencil(), "Guess, then check", 0.00),
            ("waiting for", clock_face(), "Wait for it", -0.80),
        ]:
            self.at(cue)
            icon.scale(0.84).move_to(p(-5.47, y))
            text = label(name, y, x=-3.02)
            self.put(icon, 0.40)
            self.put(text, 0.38)
        self.at("and they find out")
        summary = label("Soil is a mix", 1.95, GOLD, size=42)
        self.play(swap(timing, summary, 0.9), FadeOut(timing_line), run_time=0.9)
        self.finish()


class S04Gather(JarScene):
    def construct(self):
        self.table()
        vessel = jar()
        self.add(vessel)
        self.at("you need a clear")
        self.play(vessel.lid.animate.shift(UP * 0.37), rate_func=there_and_back, run_time=3.6)
        self.at("never use glass")
        glass = VGroup(rect(1.0, 1.4, -5.29, 0.78, "#41505D", 0.18, edge=GREY),
                       rect(0.87, 0.12, -5.29, 1.46, GREY))
        self.put(glass, 0.32)
        cross = VGroup(line(-5.81, 0.17, -4.77, 1.38, RED, 6),
                       line(-5.81, 1.38, -4.77, 0.17, RED, 6))
        material = label("Plastic, never glass", 2.42, RED)
        self.play(Create(cross), FadeIn(material), run_time=0.6)
        self.play(FadeOut(glass), FadeOut(cross), run_time=0.43)
        self.at("bring about")
        bag = soil_bag().scale(0.88).move_to(p(-4.86, 0.77))
        cup = pitcher().scale(0.54).move_to(p(-3.86, 0.18))
        cup[1].set_fill(SILT)
        self.play(FadeOut(material), FadeIn(VGroup(bag, cup), shift=RIGHT * 0.35), run_time=0.68)
        self.put(label("1 to 1½ cups topsoil", 2.40, GOLD), 0.45)
        self.at("add water")
        self.put(pitcher().scale(0.91).move_to(p(-2.12, 0.63)), 0.5, RIGHT * 0.25)
        self.at("masking tape")
        self.put(tape_roll().move_to(p(-5.31, -1.68)), 0.40, RIGHT * 0.25)
        self.at("marker and a ruler")
        self.put(marker().move_to(p(-3.60, -1.69)), 0.45, RIGHT * 0.25)
        self.put(ruler().move_to(p(-1.65, -2.43)), 0.55, RIGHT * 0.25)
        self.finish()


class S05Look(JarScene):
    def construct(self):
        self.table()
        self.add(jar())
        paper, grains, pieces = soil_sample()
        self.at("stay with your child")
        grown = person().scale(0.73).move_to(p(-4.28, 0.61))
        child = person(child=True).scale(0.71).move_to(p(-2.75, 0.30))
        self.play(FadeIn(grown, shift=RIGHT * 0.25), FadeIn(child, shift=LEFT * 0.25), run_time=1.1)
        self.at("spread a spoonful")
        spoon = VGroup(Ellipse(width=0.64, height=0.36, color=GREY, fill_opacity=1),
                       line(0.22, 0, 1.23, 0.12, GREY, 8)).move_to(p(-4.43, 0.13))
        self.play(FadeOut(grown), FadeOut(child), FadeIn(paper), run_time=0.46)
        self.add(spoon)
        self.play(spoon.animate.shift(RIGHT * 1.93), FadeIn(grains), FadeIn(pieces), run_time=2.05)
        self.play(FadeOut(spoon), run_time=0.35)
        self.at("look for rock")
        zoom = VGroup()
        for icon, x in [(pebble(), -5.17), (root(), -3.35), (leaf(), -1.52)]:
            circle = Circle(radius=0.62, color=GOLD, stroke_width=2, fill_color=BG, fill_opacity=1)
            zoom.add(VGroup(circle, icon).move_to(p(x, 2.13)))
        self.play(LaggedStart(*(GrowFromCenter(m) for m in zoom), lag_ratio=0.45), run_time=2.18)
        self.play(zoom.animate.shift(UP * 0.22), run_time=0.85)
        self.at("ask does it feel")
        pinch = VGroup(hand(-3.95, 0.14).rotate(-PI / 2), hand(-2.75, 0.06).rotate(PI / 2))
        self.play(FadeOut(zoom), FadeIn(pinch), run_time=0.48)
        self.play(pinch[0].animate.shift(RIGHT * 0.19 + DOWN * 0.09),
                  pinch[1].animate.shift(LEFT * 0.19 + UP * 0.09),
                  rate_func=there_and_back, run_time=1.1)
        words = VGroup(*(boxed_label(word, GOLD, 28, pad=0.14)
                         for word in ["Gritty", "Smooth", "Sticky"])).arrange(RIGHT, buff=0.22)
        words.move_to(p(-3.35, -1.85))
        self.play(LaggedStart(*(FadeIn(m) for m in words), lag_ratio=0.3), run_time=0.8)
        self.finish()


class S06ChildGuess(JarScene):
    def construct(self):
        self.table()
        self.add(jar())
        paper, grains, pieces = soil_sample()
        sample = VGroup(paper, grains, pieces)
        self.add(sample)
        self.at("before any water")
        self.play(sample.animate.shift(DOWN * 0.17), run_time=1.1)
        self.at("if we shake soil")
        question = question_card("What will it look like?", y=2.16, left=-5.85, max_w=5.5, size=39)
        self.put(question, 0.6)
        self.at("what will it look like")
        card = drawing()
        self.play(sample.animate.scale(0.55).move_to(p(-4.85, -2.18)), run_time=0.75)
        self.play(FadeIn(card[0], shift=LEFT * 0.48), run_time=0.48)
        self.at("draw a guess")
        self.play(FadeOut(sample), Create(VGroup(*card[1:])), run_time=1.45)
        self.at("keep it to check")
        pocket = folder()
        self.add(pocket[0])
        self.play(card.animate.scale(0.37).move_to(p(-5.03, -2.53)), FadeOut(question),
                  run_time=0.78)
        self.play(FadeIn(VGroup(*pocket[1:])), FadeOut(card), run_time=0.42)
        self.finish()


class S07Fill(JarScene):
    def construct(self):
        self.table(saved=True)
        vessel = jar(capped=False)
        self.add(vessel)
        self.at("pick out sticks")
        rock = pebble().scale(0.74).move_to(p(-4.12, 0.72))
        stick = root().scale(0.68).move_to(p(-2.74, 0.64))
        debris = VGroup(rock, stick)
        self.put(debris, 0.65)
        self.play(FadeOut(debris, shift=LEFT * 0.65 + UP * 0.42), run_time=1.1)
        self.at("fill the jar")
        soil = jar("dry").layers
        soil_guide = DashedLine(p(0.58, SOIL_TOP), p(4.92, SOIL_TOP), color=SAND, stroke_width=2)
        soil_label = label("One-third", SOIL_TOP, SAND, x=-0.88, size=29)
        pour_soil = rise_from_bottom(soil)
        soil_stream = line(2.45, 2.88, 2.70, BOTTOM + 0.15, SILT, 14).set_opacity(0.85)
        self.play(FadeIn(soil_stream), Create(soil_guide), run_time=0.4)
        soil_stream.add_updater(lambda stream: stream.put_start_and_end_on(
            p(2.45, 2.88), p(2.70, soil[0].get_top()[1] - 0.03)))
        self.play(pour_soil, FadeIn(soil_label), run_time=1.6)
        soil_stream.clear_updaters()
        self.play(FadeOut(soil_stream), run_time=0.35)
        self.at("slowly add water")
        water = jar("filled").liquid
        self.remove(vessel, soil)
        back, _, _, _, _, shine, neck, _ = vessel
        self.add(back, water, soil, shine, neck)
        water_guide = DashedLine(p(0.62, SURFACE), p(4.92, SURFACE), color=PLASTIC, stroke_width=2)
        water_label = label("1 inch from top", SURFACE, PLASTIC, x=-1.34, size=29)
        stream = line(2.71, 2.74, 2.98, SOIL_TOP, PLASTIC, 11).set_opacity(0.80)
        stream.add_updater(lambda jet: jet.put_start_and_end_on(
            p(2.71, 2.74), p(2.98, max(SOIL_TOP, water[0].get_top()[1] - 0.03))))
        self.add(stream)
        self.play(rise_from_bottom(water), FadeOut(soil_guide), FadeOut(soil_label), run_time=1.55)
        stream.clear_updaters()
        self.play(FadeOut(stream), Create(water_guide), FadeIn(water_label), run_time=0.65)
        self.at("watch for bubbles")
        bubbles = VGroup()
        for i in range(9):
            bubble = Circle(radius=0.105 + 0.022 * (i % 4), color=PLASTIC, stroke_width=4,
                            fill_color=PLASTIC, fill_opacity=0.24)
            bubble.move_to(p(2.28 + 0.25 * i, SOIL_TOP + 0.11))
            bubbles.add(bubble)
        self.play(FadeOut(water_guide), FadeOut(water_label),
                  water[0].animate.set_fill("#5A9DA3", 1),
                  LaggedStart(*(FadeIn(b, shift=DOWN * 0.21) for b in bubbles), lag_ratio=0.11),
                  run_time=0.69)
        self.play(LaggedStart(*(b.animate.shift(UP * (0.88 + 0.095 * i))
                               for i, b in enumerate(bubbles)), lag_ratio=0.07), run_time=1.6)
        self.at("air that was")
        focus = Circle(radius=0.24, color=GOLD, stroke_width=3).move_to(bubbles[-1])
        air = label("Air from the soil", 0.55, PLASTIC, x=-1.43)
        self.play(Create(focus), FadeIn(air), run_time=0.5)
        self.play(VGroup(bubbles, focus).animate.shift(UP * 0.65),
                  water[0].animate.set_fill("#60A1A5", 1), run_time=2.17, rate_func=linear)
        self.finish()


class S08Shake(JarScene):
    def construct(self):
        self.table(saved=True)
        vessel = jar("filled", capped=False)
        self.add(vessel)
        cap = lid().shift(UP * 0.38)
        tightening_hand = hand(JAR_X + 1.73, cap.get_y()).rotate(PI / 2)
        self.at("tighten and check")
        self.play(FadeIn(cap), FadeIn(tightening_hand, shift=LEFT * 0.25), run_time=0.45)
        self.play(cap.animate.shift(DOWN * 0.38), tightening_hand.animate.shift(DOWN * 0.38),
                  run_time=0.7)
        self.play(tightening_hand.animate.shift(RIGHT * 0.15), rate_func=there_and_back, run_time=0.7)
        self.at("take turns shaking")
        adult = person().scale(1.04).move_to(p(-3.43, 0.25))
        grips = VGroup(hand(1.52, -0.09, "#BF856B").rotate(-PI / 2),
                       hand(4.99, -0.09, "#BF856B").rotate(PI / 2))
        self.play(FadeOut(tightening_hand), FadeIn(adult), FadeIn(grips), run_time=0.65)
        muddy = jar("muddy")
        self.remove(cap, vessel)
        self.add(muddy, grips)
        shake = VGroup(muddy, grips)

        def shake_jar(duration, cycles, amount):
            saved = shake.copy()

            def swing(group, t):
                travel = np.sin(2 * PI * cycles * t) * np.sin(PI * t) ** 0.28
                group.become(saved).rotate(travel * amount)
                group.shift(p(0.17 * travel, 0.12 * abs(travel)))

            self.play(UpdateFromAlphaFunc(shake, swing, rate_func=linear), run_time=duration)

        shake_jar(1.4, 3, 0.1)
        self.at("for two to three")
        timer = boxed_label("2 to 3 min", GOLD, 32).move_to(p(-3.36, 2.44))
        self.put(timer, 0.38)
        shake_jar(1.4, 3, 0.12)
        self.at("have your child")
        seat = rect(1.59, 0.16, -2.83, -0.91, "#906B51", 0.04)
        stool = VGroup(seat, line(-3.44, -0.93, -3.53, -1.43, "#906B51", 5),
                       line(-2.23, -0.93, -2.14, -1.43, "#906B51", 5))
        child = person(child=True, seated=True).move_to(p(-2.79, 0.03))
        self.play(FadeOut(adult), FadeIn(stool), FadeIn(child),
                  grips.animate.set_color("#E7AC86"), run_time=0.65)
        shake_jar(3.45, 5, 0.078)
        self.at("for ages five")
        ages = boxed_label("Ages 5–7", GOLD, 32).move_to(timer)
        self.play(FadeOut(child), FadeOut(stool), FadeIn(adult),
                  grips.animate.set_color("#BF856B"), swap(timer, ages, 0.75), run_time=0.75)
        shake_jar(2.65, 6, 0.12)
        self.at("set the jar on")
        self.play(shake.animate.shift(UP * 0.24), FadeOut(ages), run_time=0.48)
        self.play(shake.animate.shift(DOWN * 0.24), run_time=0.66)
        self.play(FadeOut(grips), FadeOut(adult), run_time=0.55)
        self.finish()


class S09PredictQuestion(JarScene):
    def construct(self):
        self.table(saved=True)
        self.add(jar("muddy", drift=1.7))
        question = prediction_card()
        silt, clay, sand = chips_for_prediction()
        self.at("here is a question")
        self.wait(0.65)
        self.at("big grains of sand")
        self.put(sand)
        self.at("finer silt")
        self.put(silt)
        self.at("tiny bits of clay")
        self.put(clay)
        self.at("which do you think")
        self.play(FadeIn(question), run_time=0.8)
        self.at("which takes the longest")
        self.finish()


class S10PredictPause(PredictPause):
    SECONDS = 4.5

    def construct(self):
        self.add(tabletop(), folder(), jar("muddy", drift=0.65),
                 prediction_card(), chips_for_prediction())
        ring, run = countdown(self.SECONDS, center=p(-3.67, -1.67))
        self.add(ring)
        self.play(run)


class S11Sand(JarScene):
    def construct(self):
        self.table(saved=True)
        vessel = jar("muddy", drift=1.45)
        self.add(vessel)
        self.at("the big bits sink")
        big = VGroup(*vessel.grit[:24])
        for grain in big:
            grain.clear_updaters()
        self.play(LaggedStart(*(d.animate.move_to(p(d.get_x(), BOTTOM + 0.16 + 0.11 * (i % 4)))
                                for i, d in enumerate(big)), lag_ratio=0.035), run_time=2.5)
        self.at("after about one minute")
        clock = clock_face().move_to(p(-5.26, 1.95))
        minute = label("1 minute", 1.95, GOLD, x=-3.58)
        sand = settled_layer("sand")
        self.play(FadeIn(clock), rise_from_bottom(sand), FadeOut(big), run_time=1.03)
        self.at("sand forms the bottom")
        name = label("Sand", -1.99, SAND, x=-0.85)
        self.play(FadeIn(minute), FadeIn(name), run_time=0.55)
        self.at("your child marks")
        self.play(FadeIn(tape(SAND_TOP), shift=RIGHT * 0.65),
                  vessel.liquid[0].animate.set_fill("#967760", 1), run_time=1.45)
        self.at("dark bits floating")
        floating = flecks()
        self.play(LaggedStart(*(FadeIn(f, shift=DOWN * 0.55) for f in floating), lag_ratio=0.13),
                  vessel.liquid[0].animate.set_fill("#A58C70", 1), run_time=1.8)
        self.at("old plant parts")
        plant_name = label("Old plant bits", SURFACE).move_to(p(0.91, SURFACE), aligned_edge=RIGHT)
        leader = Line(plant_name.get_right() + 0.12 * RIGHT, floating[0].get_left() + 0.04 * LEFT,
                      color=TEXT, stroke_width=2)
        self.play(FadeIn(plant_name), Create(leader), run_time=0.6)
        bob(floating, amp=0.055, speed=2 * PI / 2.3)
        self.finish()


class S12SiltClay(JarScene):
    def construct(self):
        self.table(saved=True)
        vessel = jar("sand", drift=1.75)
        self.add(vessel)
        self.at("after one hour")
        example = boxed_label("Example", GOLD, 31).move_to(p(-3.55, 2.63))
        hour = label("1 hour", 1.60, GOLD, x=-3.55, size=41)
        self.put(example, 0.41)
        self.put(hour, 0.48)
        silt = settled_layer("silt")
        self.play(rise_from_bottom(silt), run_time=0.79)
        self.at("silt above the sand")
        silt_name = layer_label("Silt", SAND_TOP, SILT_TOP, "#FFC394", x=-0.22)
        self.put(silt_name, 0.48)
        self.at("mark it with tape")
        self.play(FadeIn(tape(SILT_TOP), shift=LEFT * 0.42), run_time=0.72)
        self.at("one to two days")
        days = label("1 to 2 days", 1.60, GOLD, x=-3.55, size=41)
        clay = settled_layer("clay")
        self.play(swap(hour, days, 0.83), vessel.liquid[0].animate.set_fill("#668D89", 1),
                  run_time=0.83)
        self.play(rise_from_bottom(clay), run_time=0.86)
        self.at("clay above it")
        clay_name = layer_label("Clay", SILT_TOP, CLAY_TOP, "#FFC0B4", x=-0.22)
        self.put(clay_name, 0.45)
        self.at("measure any layers")
        scale = ruler(vertical=True)
        cm = label("cm", 1.50, PAPER, x=5.86, size=29)
        self.play(FadeIn(scale, shift=LEFT * 0.30), FadeIn(tape(CLAY_TOP), shift=LEFT * 0.4),
                  run_time=0.85)
        self.put(cm, 0.45)
        self.at("clay rich soil")
        suspended_clay = particles(CLAY_TOP + 0.15, SURFACE - 0.13, 110, 0.03,
                                   "#F1C4AC", seed=23, speed=1.1).set_opacity(0.78)
        self.play(vessel.liquid[0].animate.set_fill("#8F7668", 1),
                  FadeIn(suspended_clay), run_time=1.27)
        self.put(label("Layers can vary", 0.63, TEXT, x=-3.55), 0.55)
        self.finish()


class S13Debrief(JarScene):
    def construct(self):
        self.table(saved=True)
        vessel = jar("settled", drift=1.0)
        self.add(vessel)
        self.at("set the first drawing")
        card = drawing()
        final = card.copy()
        card.scale(0.34).move_to(p(-5.03, -2.55))
        self.play(Transform(card, final), run_time=1.55)
        self.at("what matched your guess")
        question = question_card("What matched your guess?", y=2.10, left=-6.00,
                                 max_w=6.1, size=37)
        self.put(question, 0.65)
        self.at("use the layers")
        light = light_on_layer(BOTTOM, SAND_TOP)
        self.play(FadeIn(light), run_time=0.65)
        self.play(FadeOut(light), run_time=1.38)
        self.at("what is still floating")
        self.play(vessel.floating.animate.set_color("#CC8D62"), rate_func=there_and_back, run_time=1.25)
        self.finish()


class S14Safety(JarScene):
    def construct(self):
        self.table(saved=True)
        self.add(jar("settled", drift=1.1))
        self.at("small stones can choke")
        rock = no_symbol(pebble().scale(1.38)).move_to(p(-4.80, 1.31))
        family = VGroup(person(), person(child=True).shift(RIGHT * 1.18 + DOWN * 0.36))
        family.scale(0.70).move_to(p(-2.40, 0.53))
        self.put(rock, 0.76)
        risk = boxed_label("Under 4: choking risk", RED, 30).move_to(p(-3.77, 2.61))
        self.put(risk, 0.55)
        self.at("keep them from babies")
        self.put(family, 1.40)
        self.at("if a child is choking")
        call = boxed_label("Choking? Call 911", RED, 33).move_to(risk)
        self.play(swap(risk, call, 0.75), run_time=0.75)
        self.at("nobody puts soil")
        mouth = VGroup(Ellipse(width=0.94, height=0.50, fill_color="#913F48",
                               fill_opacity=1, stroke_color="#E99290", stroke_width=4),
                       line(-0.39, 0.04, 0.39, 0.04, "#FFD7C0", 3))
        finger = rect(0.80, 0.23, 0.53, -0.21, "#E7AC86", 0.10)
        mud = Dot(p(0.17, -0.21), radius=0.105, color=MUD)
        crossed = no_symbol(VGroup(mouth, finger, mud)).move_to(p(-3.54, 0.64))
        self.play(FadeOut(family), FadeOut(rock), FadeOut(call), run_time=0.4)
        self.put(crossed, 0.73)
        self.at("wash hands with soap")
        tap = VGroup(line(-0.77, 1.09, 0.49, 1.09, PLASTIC, 10),
                     line(0.49, 1.09, 0.49, 0.73, PLASTIC, 10),
                     line(-0.57, 1.09, -0.57, 1.39, PLASTIC, 6),
                     line(-0.82, 1.39, -0.32, 1.39, PLASTIC, 5))
        hands = VGroup(hand(-0.08, -0.42).rotate(-0.48), hand(0.62, -0.59).rotate(0.63))
        suds = VGroup(*(Circle(radius=0.08 + (i % 3) * 0.03, color=PAPER, stroke_width=2)
                        .move_to(p(0.02 + 0.16 * i, -0.31 + 0.12 * (i % 2))) for i in range(5)))
        water = VGroup(*(line(0.35 + i * 0.13, 0.56, 0.31 + i * 0.13, 0.09, BLUE, 3)
                         for i in range(3)))
        wash = VGroup(tap, hands, suds, water).shift(LEFT * 3.55)
        self.play(FadeOut(crossed), FadeIn(wash), run_time=0.52)
        bob(water, amp=0.14, speed=2 * PI / 0.64)
        self.put(label("Wash with soap", 2.06, PLASTIC), 0.5)
        self.finish()


class S15SoilSource(JarScene):
    def construct(self):
        self.table(saved=True)
        self.add(jar("settled", drift=1.2))
        self.at("bag topsoil")
        bag = soil_bag().move_to(p(-3.58, 0.48))
        check = VGroup(line(-2.76, 1.63, -2.51, 1.39, GREEN, 7),
                       line(-2.51, 1.39, -2.02, 1.97, GREEN, 7))
        safest = boxed_label("Safest choice", GREEN, 31).move_to(p(-3.57, 2.47))
        self.put(bag, 0.63)
        self.play(Create(check), FadeIn(safest), run_time=0.80)
        self.at("if you plan to dig")
        base = poly([(-1.57, -0.39), (1.57, -0.39), (1.23, 0.58), (-1.22, 0.58)],
                    "#98674F", "#D4A076", 3)
        rows = VGroup(*(line(-1.22 + 0.55 * i, -0.26, -1.01 + 0.46 * i, 0.44, "#D4A076", 2)
                        for i in range(5)))
        shoots = VGroup(*(leaf().scale(0.54).set_color(GREEN).rotate((-1) ** i * 0.50)
                          .move_to(p(-0.96 + 0.46 * i, 0.19 + (i % 2) * 0.36)) for i in range(5)))
        bed = VGroup(base, rows, shoots).move_to(p(-3.55, 0.45))
        self.play(FadeOut(check), FadeOut(bag), FadeOut(safest), run_time=0.50)
        self.put(bed, 0.88)
        self.at("read the guide's soil")
        self.put(boxed_label("Check before digging", GOLD, 31).move_to(p(-3.56, 2.40)), 0.60)
        self.finish()


class S16Return(JarScene):
    def construct(self):
        self.table(saved=True)
        vessel = jar("settled", drift=1.4)
        self.add(vessel)
        self.at("that brown stuff")
        shoe = poly([(-1.60, -0.40), (1.57, -0.40), (1.43, 0.05), (0.81, 0.10),
                     (0.20, 0.29), (-0.16, 0.75), (-1.28, 0.75), (-1.36, 0.13)],
                    "#6D9C9D", PLASTIC, 3)
        sole = line(-1.56, -0.28, 1.49, -0.28, PAPER, 6)
        dirt = poly([(-1.32, -0.36), (-0.91, -0.37), (-0.68, -0.29), (-0.22, -0.24),
                     (0.10, -0.29), (0.65, -0.26), (1.27, -0.31), (1.36, -0.52),
                     (-1.34, -0.52)], MUD)
        boot = VGroup(shoe, sole, dirt).move_to(p(-3.38, 0.86))
        self.put(boot, 0.7, RIGHT * 0.45)
        self.at("is a mix")
        self.put(label("Soil is a mix", 2.14, GOLD, size=45), 0.6)
        sweep = jar_band(0.54, 1.03, PAPER, 0.25)
        self.play(FadeIn(sweep), run_time=0.38)
        self.play(sweep.animate.shift(DOWN * 2.17), run_time=1.41)
        self.at("the bigger grains")
        self.play(FadeOut(boot), FadeOut(sweep), run_time=0.40)
        names = VGroup(layer_label("Sand", BOTTOM, SAND_TOP, SAND, x=-0.48),
                       layer_label("Silt", SAND_TOP, SILT_TOP, "#FFC394", x=-0.48),
                       layer_label("Clay", SILT_TOP, CLAY_TOP, "#FFC0B4", x=-0.48))
        sand_glow = light_on_layer(BOTTOM, SAND_TOP)
        self.play(FadeIn(names[0]), FadeIn(sand_glow), run_time=0.63)
        self.play(FadeOut(sand_glow), run_time=0.53)
        self.at("the smaller bits")
        clay_glow = light_on_layer(SILT_TOP, CLAY_TOP)
        silt_glow = light_on_layer(SAND_TOP, SILT_TOP)
        self.play(FadeIn(names[1]), FadeIn(names[2]), FadeIn(clay_glow), run_time=0.49)
        self.play(FadeOut(clay_glow), FadeIn(silt_glow), run_time=0.48)
        self.play(FadeOut(silt_glow), run_time=0.38)
        self.finish()


class S17End(EndCard):
    LINE = "Soil is a mix: big bits sink first, tiny bits last."
