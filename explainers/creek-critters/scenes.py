"""A creek cutaway and a close view of its sampling tray."""
from bp_parts import *

# Colour map: blue/teal water and observation, green bank, gold questions
# and leaf litter, red caution, grey rock and equipment, white tray.
SKY = "#1C2E3C"
BANK = "#456349"
MOSS = "#648550"
DEEP = "#194C62"
SHALLOW = "#28677A"
FOAM = "#76D0DA"
STONE = "#797B77"
BED = "#51483D"
RIM = "#F0F4EA"
TRAY_WATER = "#A4D9DE"
INK = "#233C44"
MAYFLY = "#5F4B2B"
STONEFLY = "#34493D"
QUESTION = "What might this mix suggest?"
QUESTION_STYLE = {"y": 2.91, "size": 38}


def point(x, y):
    return np.array([x, y, 0.0])


def shape(points, fill, stroke=None, width=2):
    return Polygon(*(point(*p) for p in points), color=stroke or fill,
                   stroke_width=width, fill_color=fill, fill_opacity=1)


def oval(w, h, x, y, fill, stroke=None, width=2):
    return Ellipse(width=w, height=h, color=stroke or fill, stroke_width=width,
                   fill_color=fill, fill_opacity=1).move_to(point(x, y))


def rounded(w, h, x, y, fill, stroke=None, width=2, radius=0.16):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            color=stroke or fill, stroke_width=width,
                            fill_color=fill, fill_opacity=1).move_to(point(x, y))


def line(a, b, color, width=4):
    return Line(point(*a), point(*b), color=color, stroke_width=width)


def path(points, color, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(
        [point(*p) for p in points])


def rock(x, y, w, h, color=STONE):
    base = shape([(-0.50, -0.20), (-0.37, 0.31), (-0.04, 0.50),
                  (0.33, 0.33), (0.50, -0.13), (0.32, -0.46),
                  (-0.27, -0.50)], color, "#B2AB94")
    face = shape([(-0.50, -0.20), (-0.04, -0.03), (0.50, -0.13),
                  (0.32, -0.46), (-0.27, -0.50)], "#575A54")
    return VGroup(base, face).stretch(w, 0).stretch(h, 1).move_to(point(x, y))


def current():
    """Moving water strokes stay within the cutaway's wetted area."""
    ripples = VGroup()
    for i in range(24):
        row, col = divmod(i, 6)
        x = -5.83 + col * 1.63 + (row % 2) * 0.24
        y = 0.43 - row * 0.66
        w = 0.75 + 0.13 * ((i * 5) % 4)
        wave = path([(-w/2, 0), (-w/5, 0.045), (w/5, 0.044), (w/2, 0)],
                    FOAM if row < 2 else BLUE, 3.3 if row < 2 else 2.4)
        wave.set_stroke(opacity=0.75 if row < 2 else 0.54)
        origin = point(x, y)
        wave.move_to(origin)

        def drift(mob, dt, origin=origin, phase=i * 1.57):
            mob.clock += dt
            t = mob.clock
            mob.move_to(origin + point(0.33 * np.sin(1.9*t + phase),
                                       0.087 * np.sin(2.2*t + phase)))

        wave.clock = 0.0
        wave.add_updater(drift)
        ripples.add(wave)
    return ripples


def creek():
    """Rebuild the same bank, waterline, and landmarks in every cutaway."""
    horizon = rounded(13.48, 6.93, 0, -0.05, SKY, radius=0.30)
    far = shape([(-6.65, 0.84), (-6.65, 1.36), (-5.21, 1.68), (-3.83, 1.49),
                 (-2.22, 1.79), (-0.62, 1.48), (1.17, 1.65), (2.51, 1.20),
                 (3.47, 0.84)], "#364D43")
    bed = shape([(-6.65, -1.66), (-5.4, -1.45), (-3.9, -1.75), (-2.1, -1.49),
                 (-0.1, -1.79), (1.8, -1.54), (3.35, -1.12), (6.64, -0.35),
                 (6.64, -3.38), (-6.65, -3.38)], BED)
    water = shape([(-6.65, 0.85), (3.62, 0.85), (4.72, 0.40), (3.35, -1.12),
                   (1.8, -1.54), (-0.1, -1.79), (-2.1, -1.49), (-3.9, -1.75),
                   (-5.4, -1.45), (-6.65, -1.66)], DEEP)
    surface = shape([(-6.65, 0.85), (3.62, 0.85), (4.72, 0.4), (3.64, 0.02),
                     (0.37, -0.03), (-2.3, 0.12), (-4.22, -0.06),
                     (-6.65, 0.06)], SHALLOW)
    bank = shape([(3.52, 0.84), (4.01, 1.34), (4.61, 1.66), (5.63, 1.65),
                  (6.65, 2.03), (6.65, -0.36), (5.03, -0.66), (3.35, -1.12),
                  (4.17, -0.10)], BANK)
    moss = VGroup(
        shape([(3.52, 0.84), (4.01, 1.34), (4.61, 1.66), (5.63, 1.65),
               (6.65, 2.03), (6.65, 1.49), (5.60, 1.19), (4.65, 1.14),
               (4.09, 0.89)], MOSS),
        *[oval(0.42, 0.11, x, y, MOSS) for x, y in
          [(4.59, 0.72), (5.24, 0.95), (5.75, 0.69), (6.23, 0.94), (5.58, 0.23)]],
    )
    stones = VGroup(*[rock(*r) for r in [
        (-5.83, -1.69, 1.50, 0.79), (-4.08, -1.89, 1.69, 0.65),
        (-2.25, -1.68, 1.80, 1.02), (-0.31, -1.88, 1.94, 0.66),
        (1.70, -1.63, 1.83, 0.95), (3.37, -1.34, 1.27, 0.69),
        (-5.48, -2.50, 0.95, 0.42), (-3.49, -2.80, 1.28, 0.48),
        (-0.50, -2.65, 1.18, 0.49), (2.73, -2.60, 0.99, 0.49),
        (4.93, -1.63, 1.36, 0.70), (5.86, -2.71, 1.00, 0.49),
    ]])
    waterline = line((-6.63, 0.85), (3.50, 0.85), FOAM, 3)
    return VGroup(horizon, far, bed, water, surface, bank, moss, stones,
                  waterline, current())


def gravel_shoal():
    """Foreground shallows give the waders a visible waterline at their ankles."""
    sand = shape([(-5.05, -1.40), (-5.05, -0.45), (-4.51, 0.36),
                  (-3.56, 0.99), (-2.37, 1.16), (-0.75, 1.10),
                  (1.02, 1.24), (2.61, 1.10), (3.66, 0.98), (4.32, 0.52),
                  (3.68, -0.61), (3.08, -1.30), (1.78, -1.56),
                  (-1.11, -1.60), (-3.23, -1.58)], "#526758")
    edge = path([(-4.88, -1.27), (-3.27, -1.20), (-1.24, -1.14),
                 (0.82, -1.09), (2.26, -1.10), (3.18, -1.16)], FOAM, 3.8)
    shallows = shape([(-4.93, -1.21), (-3.27, -1.18), (-1.24, -1.13),
                      (0.82, -1.08), (2.26, -1.09), (3.21, -1.15),
                      (3.08, -1.30), (1.78, -1.56), (-1.11, -1.60),
                      (-3.23, -1.58)], SHALLOW)
    stones = VGroup(*[rock(x, y, w, h) for x, y, w, h in [
        (-4.15, -0.59, 0.63, 0.24), (-1.26, -0.54, 0.58, 0.24),
        (2.90, -0.63, 0.58, 0.23), (3.34, 0.11, 0.64, 0.29),
    ]])
    ripples = VGroup()
    for i, x in enumerate((-3.65, -2.10, -0.52, 1.72)):
        ripple = path([(x-0.48, -1.41), (x-0.01, -1.36), (x+0.48, -1.40)],
                      FOAM, 3.6)
        motion(ripple, dx=0.19, dy=0.05, speed=2.65+i*0.26)
        ripples.add(ripple)
    return VGroup(sand, shallows, stones, edge, ripples)


def nymph(kind="mayfly", x=0, y=0, scale=1, angle=0):
    """Distinguish the schematic young by tail count, silhouette, and gills."""
    mayfly = kind.startswith("mayfly")
    broad = kind.endswith("wide")
    color = MAYFLY if mayfly else STONEFLY
    gills = VGroup()
    if mayfly:
        for z in (-0.37, -0.17, 0.03):
            for sign in (-1, 1):
                gills.add(oval(0.23, 0.14, z, sign * 0.23, "#AD894B", color)
                          .rotate(sign * 0.48))
    legs = VGroup()
    for z, reach in [(-0.06, -0.39), (0.19, 0.04), (0.42, 0.51)]:
        for sign in (-1, 1):
            legs.add(path([(z, sign*0.12), (reach, sign*0.36),
                           (reach-0.14, sign*0.52)], color, 4))
    tail_directions = (-0.32, 0, 0.32) if mayfly else (-0.31, 0.31)
    tails = VGroup(*[path([(-0.53, d*0.25), (-0.84, d*0.67), (-1.21, d)], color, 3)
                     for d in tail_directions])
    body = VGroup(oval(1.13, 0.36 if mayfly else 0.45, -0.03, 0, color),
                  oval(0.33, 0.34, 0.55, 0, color))
    segments = VGroup(*[line((z, -0.12), (z, 0.12), "#C4A876", 2)
                        for z in (-0.39, -0.21, -0.03, 0.15)])
    antennae = VGroup(*[path([(0.58, s*0.07), (0.81, s*0.18),
                              (1.05, s*0.20)], color, 2.5) for s in (-1, 1)])
    insect = VGroup(tails, legs, gills, body, segments, antennae)
    if broad:
        insect.stretch(1.28, 1)
    insect.scale(scale).rotate(angle).move_to(point(x, y))
    insect.gills = gills
    return insect


def motion(mob, dx=0.16, dy=0.12, speed=2.0, phase=0):
    """Give a creature room to crawl or swim around its starting position."""
    origin = mob.get_center().copy()

    def travel(m, dt):
        m.clock += dt
        t = m.clock
        m.move_to(origin + point(dx * (np.sin(speed*t + phase) - np.sin(phase)),
                                 dy * np.sin(0.81*speed*t)))

    mob.clock = 0.0
    return mob.add_updater(travel)


def tray_side(x, y, width=2.5, wet=True):
    tub = shape([(-1.3, 0.24), (1.3, 0.24), (1.05, -0.37), (-1.05, -0.37)],
                RIM, GREY, 3)
    inside = shape([(-1.13, 0.13), (1.13, 0.13), (0.91, -0.22), (-0.91, -0.22)],
                   TRAY_WATER if wet else "#CFD9D8")
    rim = line((-1.31, 0.24), (1.31, 0.24), WHITE, 5)
    return VGroup(tub, inside, rim).scale(width/2.6).move_to(point(x, y))


def tray_view():
    """Close view of the same white tray, set on the bank beside the water."""
    world = creek()
    shadow = rounded(9.52, 4.98, 0.61, -0.53, "#203839", radius=0.50)
    rim = rounded(9.35, 4.86, 0.57, -0.39, RIM, radius=0.50, width=3)
    inner = rounded(8.76, 4.33, 0.57, -0.39, TRAY_WATER, "#6E9DA4", radius=0.40)
    reflections = VGroup(
        path([(-3.47, 1.35), (-2.84, 1.47), (-2.20, 1.35)], WHITE, 3),
        path([(3.40, -2.19), (4.00, -2.10), (4.53, -1.91)], WHITE, 3),
    ).set_stroke(opacity=0.62)
    edge_ripples = VGroup()
    for i, y in enumerate((0.49, 0.14, -0.22, -0.57, -0.93, -1.22)):
        ripple = path([(-6.48, y), (-5.62, y+0.10), (-4.66, y+0.03),
                       (-4.28, y+0.12)], FOAM, 4.8)
        motion(ripple, dx=0.13, dy=0.16, speed=2.6+i*0.21)
        edge_ripples.add(ripple)
    return VGroup(world, edge_ripples, shadow, rim, inner, reflections)


def creek_label(words, color=TEXT, x=0, y=2.92, size=36):
    return fit_text(words, max_w=12.0, size=size, min_size=28, color=color,
                    weight=BOLD).move_to(point(x, y))


def top_question(words):
    return question_card(words, **QUESTION_STYLE)


def strainer(x, y, scale=1):
    mesh = VGroup(*[line((i, -0.30), (i+0.16, 0.30), GREY, 1.5)
                    for i in [-0.48, -0.25, -0.02, 0.21, 0.44]])
    rim = oval(1.38, 0.76, 0, 0, "#B9D1CB", TEXT, 4)
    edge = path([(-0.64, -0.09), (-0.39, -0.52), (0.36, -0.52), (0.64, -0.09)],
                GREY, 4)
    handle = line((0.63, 0.03), (1.45, 0.34), TEXT, 9)
    return VGroup(handle, edge, rim, mesh).scale(scale).move_to(point(x, y))


def spoon(x, y, scale=1):
    return VGroup(line((-0.59, 0), (0.50, 0), "#F2E6CD", 11),
                  oval(0.60, 0.42, -0.75, 0, "#FAEFDA", GREY, 2)).scale(scale).move_to(point(x, y))


def cup(x, y, wet=True):
    wall = shape([(-0.43, 0.47), (0.43, 0.47), (0.33, -0.48), (-0.33, -0.48)],
                 "#395E68", TEXT, 3)
    water = shape([(-0.38, -0.08), (0.38, -0.08), (0.33, -0.47), (-0.33, -0.47)], TEAL)
    opening = oval(0.86, 0.19, 0, 0.47, "#395E68", TEXT)
    return VGroup(wall, water, opening).move_to(point(x, y)) if wet else VGroup(wall, opening).move_to(point(x, y))


def shoe(x, y, color=GREY):
    upper = shape([(-0.58, -0.18), (-0.55, 0.14), (-0.29, 0.33), (0.06, 0.16),
                   (0.43, 0.08), (0.64, -0.10), (0.58, -0.25), (-0.53, -0.25)],
                  color, TEXT)
    return VGroup(upper, line((-0.52, -0.17), (0.55, -0.17), INK, 3)).move_to(point(x, y))


def bottle(x, y, fill, height=1.0):
    return VGroup(rounded(0.60, height, 0, 0, fill, TEXT),
                  rounded(0.35, 0.18, 0, height/2+0.05, RIM)).move_to(point(x, y))


def lens(x, y, scale=1):
    return VGroup(line((0.32, -0.34), (0.68, -0.72), TEXT, 10),
                  Circle(radius=0.48, color=TEXT, stroke_width=5,
                         fill_color=BLUE, fill_opacity=0.20)).scale(scale).move_to(point(x, y))


def person(x, foot, height, color, reach=False):
    """Faceless profile with visible shoes, anchored at the soles."""
    arm = [(0.08, 1.53), (0.45, 1.30), (0.91, 1.27)] if reach else [
        (0.08, 1.53), (0.35, 1.32), (0.26, 1.04)]
    figure = VGroup(
        path([(-0.06, 0.88), (-0.21, 0.50), (-0.24, 0.13)], TEXT, 8),
        path([(0.11, 0.88), (0.26, 0.54), (0.29, 0.13)], TEXT, 8),
        oval(0.58, 0.91, 0, 1.21, color, TEXT),
        oval(0.49, 0.51, 0.13, 1.92, SKY, TEXT, 4),
        path(arm, TEXT, 6),
        shoe(-0.16, 0.10, color).scale(0.35),
        shoe(0.37, 0.10, color).scale(0.35),
    )
    figure.set_height(height).move_to(point(x, foot), aligned_edge=DOWN)
    return figure


def reaching_arm(figure, x, y):
    shoulder = figure[4].get_start()
    elbow = (shoulder + point(x, y)) / 2 + RIGHT*0.12
    return path([tuple(shoulder[:2]), tuple(elbow[:2]), (x, y)], TEXT, 6)


def warning(icon, x=-3.65, y=-0.12):
    icon.scale(min(1.48/icon.width, 1.31/icon.height)).move_to(point(x, y))
    ring = Circle(radius=0.94, color=RED, stroke_width=7,
                  fill_color=BG, fill_opacity=1).move_to(point(x, y))
    slash = line((x-0.64, y+0.64), (x+0.64, y-0.64), RED, 7)
    return VGroup(ring, icon, slash)


def crayfish(x, y):
    body = VGroup(oval(1.04, 0.41, -0.07, 0, "#B26D51"),
                  oval(0.39, 0.50, -0.62, 0, "#B26D51"))
    for s in (-1, 1):
        body.add(path([(0.17, s*0.08), (0.41, s*0.32), (0.64, s*0.34)], "#CB8B6C", 6),
                 shape([(0.53, s*0.27), (0.68, s*0.51), (0.95, s*0.45),
                        (0.76, s*0.34), (0.94, s*0.27), (0.76, s*0.19)], "#CB8B6C"))
    return body.move_to(point(x, y))


def clue_icon(kind, x, y):
    if kind == "look":
        return lens(x, y)
    if kind == "sort":
        return VGroup(*[cup(x+i*0.47, y, wet=False).scale(0.45) for i in (-1, 0, 1)])
    check = path([(-0.05, -0.11), (0.10, -0.28), (0.43, 0.22)], GREEN, 7)
    return VGroup(T("?", size=42, color=GOLD).move_to(LEFT * 0.75),
                  Arrow(LEFT*0.47, RIGHT*0.02, buff=0.04, color=TEXT),
                  check.shift(RIGHT*0.30)).move_to(point(x, y))


def notebook(x, y):
    cover = rounded(2.35, 1.54, x, y, "#D3CBAD", "#A08A5F", radius=0.10)
    marks = VGroup(*[line((x-0.8, y+dy), (x+0.74, y+dy), "#796C59", 2)
                     for dy in (0.37, 0.11, -0.15, -0.41)])
    return VGroup(cover, marks)


def hook_animals():
    return VGroup(nymph("mayfly", -2.24, -1.82, 0.35, 0.35),
                  nymph("stonefly", -2.30, -1.83, 0.30, 2.65),
                  nymph("mayfly_wide", -2.38, -1.89, 0.26, 3.43))


class S01Hook(TitleCard, SpokenScene):
    LESSON = "Creek Critters"
    TITLE = "Creek Critters: Parent Guide"

    def construct(self):
        world = creek()
        central = world[7][2]
        self.add(world)
        self.at("what lives under")
        banner = creek_label(self.LESSON, x=-3.95, size=50)
        self.play(FadeIn(banner), run_time=0.32)
        self.wait(1.42)
        self.play(FadeOut(banner), run_time=0.32)
        self.at("lift one", lead=0.38)
        insects = hook_animals()
        for insect in insects:
            insect.set_color(GOLD)
        self.play(central.animate.shift(UP*1.12+LEFT*0.2).rotate(0.42), run_time=0.90)
        self.at("tiny animals scramble", lead=0.25)
        self.add(*insects)
        goals = [(-0.68, -0.27), (-3.67, -0.56), (-3.81, -2.31)]
        self.play(*(m.animate.move_to(point(*xy)) for m, xy in zip(insects, goals)),
                  run_time=1.45)
        for i, insect in enumerate(insects):
            motion(insect, dx=0.28, dy=0.14, speed=2.1+i*0.35, phase=i)
        self.at("you and your child")
        spotlight = Circle(radius=0.65, color=FOAM, stroke_width=4).move_to(insects[0])
        self.play(Create(spotlight), run_time=0.68)
        self.at("sort what you find")
        self.play(spotlight.animate.move_to(insects[1]), run_time=0.70)
        self.at("check a guess")
        self.play(FadeOut(spotlight), run_time=0.45)
        self.finish()


class S02WhatTheyGet(SpokenScene):
    def construct(self):
        world = creek()
        world[7][2].shift(UP*1.12+LEFT*0.2).rotate(0.42)
        self.add(world)
        setup = VGroup(tray_side(4.58, 0.89, 2.85), notebook(4.86, -0.55))
        self.at("lead this trip", lead=1.4)
        self.play(FadeIn(setup, shift=LEFT*0.30), run_time=1.10)
        self.at("slowing down")
        plate = rounded(6.22, 5.55, -3.43, 0.30, SKY, "#66818B", radius=0.27)
        self.play(FadeIn(plate), run_time=0.40)
        group = VGroup()
        for phrase, label, kind, y in [
            ("looking closely", "Look closely", "look", 2.17),
            ("and sorting", "Sort what you find", "sort", 0.20),
            ("making a guess", "Guess, then check", "guess", -1.71),
        ]:
            self.at(phrase, lead=0.48)
            icon = clue_icon(kind, -5.45, y)
            text = creek_label(label, x=-2.56, y=y, size=32)
            self.play(FadeIn(icon, shift=RIGHT*0.20), run_time=0.42)
            self.play(FadeIn(text), run_time=0.35)
            group.add(icon, text)
        self.at("against real evidence")
        self.play(Indicate(group[-1], color=GOLD, scale_factor=1.04), run_time=0.68)
        self.finish()


def weather_card():
    sheet = rounded(4.25, 1.84, 3.69, -0.19, SKY, TEXT, 3, 0.18)
    bar = line((1.69, 0.29), (5.69, 0.29), TEXT, 3)
    cloud = VGroup(*[oval(0.39, 0.27, x, -0.15+y, GREY)
                     for x, y in [(2.18, 0), (2.38, 0.10), (2.57, 0)]],
                   *[line((x, -0.31), (x-0.10, -0.58), BLUE, 3)
                     for x in (2.27, 2.43, 2.60)])
    suns = VGroup()
    for x in (3.22, 4.20, 5.17):
        sun = oval(0.31, 0.31, x, -0.25, GOLD)
        rays = VGroup(*[Line(point(x, -0.25)+0.22*d, point(x, -0.25)+0.31*d,
                             color=GOLD, stroke_width=3)
                        for d in (RIGHT, UR, UP, UL, LEFT, DL, DOWN, DR)])
        suns.add(VGroup(sun, rays))
    return VGroup(sheet, bar, cloud), suns


class S03GearSpot(SpokenScene):
    def construct(self):
        self.add(creek())
        mat = rounded(7.28, 4.11, 2.64, 0.82, "#344D42", "#729072", radius=0.24)
        self.add(mat)
        gear = [
            ("kitchen strainer", strainer(0.43, 1.85, 1.24)),
            ("white plastic tray", tray_side(3.11, 1.85, 2.71, wet=False)),
            ("plastic spoon", spoon(5.23, 0.64, 1.10)),
            ("closed toe water", VGroup(shoe(3.55, -0.13), shoe(4.66, -0.35))),
            ("bring soap", bottle(0.62, -0.15, TEAL, 0.72)),
            ("clean water", VGroup(
                rounded(0.38, 0.40, 1.94, 0.14, SKY, TEXT).set_fill(opacity=0),
                bottle(1.59, -0.08, BLUE, 1.10))),
            ("sunscreen", bottle(2.53, -0.17, GOLD, 0.80)),
            ("insect repellent", bottle(5.77, -0.60, GREEN, 0.89)),
            ("clear plastic cup", cup(5.42, 1.90, wet=False)),
        ]
        for phrase, tool in gear:
            self.at(phrase, lead=0.48)
            self.play(FadeIn(tool, shift=DOWN*0.24), run_time=0.43)
        self.at("choose a shallow", lead=0.50)
        riffle = VGroup(*[path([(-5.7, y), (-4.42, y+0.13), (-3.26, y),
                               (-2.02, y+0.09), (-0.86, y)], FOAM, 4)
                          for y in (0.40, -0.13, -0.70)])
        self.play(*(FadeOut(tool) for _, tool in gear), FadeOut(mat), Create(riffle), run_time=0.85)
        public = creek_label("Public park · Collecting allowed", GREEN)
        self.at("in a public park")
        self.play(FadeIn(public), run_time=0.45)
        advisory = creek_label("Check posted water advisories", GOLD)
        self.at("check posted water")
        self.play(swap(public, advisory), run_time=0.70)
        self.at("when water is low", lead=0.65)
        clear = creek_label("Low and clear", BLUE)
        calendar, suns = weather_card()
        self.play(swap(advisory, clear), FadeIn(calendar), FadeOut(riffle), run_time=0.78)
        self.at("three days after")
        self.play(LaggedStart(*(GrowFromCenter(sun) for sun in suns), lag_ratio=0.42),
                  run_time=1.10)
        self.finish()


def alert_scene_icon(kind):
    if kind == "fast":
        return VGroup(*[path([(-0.62, y), (-0.28, y+0.15), (0.19, y-0.11), (0.65, y)],
                             "#B58361", 8) for y in (-0.28, 0, 0.28)])
    if kind == "glass":
        return shape([(-0.57, -0.32), (0.42, -0.44), (0.16, 0.59)], TRAY_WATER, WHITE, 3)
    if kind == "berries":
        return VGroup(path([(0, -0.55), (0.06, -0.07), (-0.36, 0.46)], GREEN, 5),
                      oval(0.54, 0.23, -0.28, 0.32, GREEN).rotate(0.52),
                      oval(0.51, 0.24, 0.28, 0.12, GREEN).rotate(-0.40),
                      *[oval(0.34, 0.34, x, y, "#C27162")
                        for x, y in [(-0.22, -0.06), (0.06, -0.26), (0.34, -0.14)]])
    if kind == "cup":
        return cup(0, 0)
    return nymph("mayfly", scale=0.65)


class S04Safety(SpokenScene):
    def construct(self):
        self.add(creek(), gravel_shoal())
        adult = person(0.33, -1.36, 3.05, TEAL, reach=True)
        child = person(1.98, -1.31, 1.98, GOLD)
        reach = DashedVMobject(path([(0.91, 0.60), (1.25, 0.91),
                                     (1.60, 0.85), (1.88, 0.56)], GOLD, 5),
                               num_dashes=9)
        self.at("stay within arms")
        self.add(adult, child)
        label = creek_label("Arm’s reach", GOLD)
        self.play(Create(reach), FadeIn(label), run_time=0.80)
        small_child = person(4.14, 0.31, 1.29, GOLD)
        second_adult = person(5.50, 0.44, 2.62, TEAL, reach=True).flip(UP)
        self.at("children under five", lead=0.45)
        new_label = creek_label("Under five · Stay on the bank", GOLD, x=-1.45)
        self.play(FadeOut(reach), FadeIn(small_child), FadeIn(second_adult),
                  swap(label, new_label), run_time=0.82)
        self.at("wade only in", lead=0.50)
        depth = line((-0.37, -1.06), (2.65, -1.06), FOAM, 5)
        depth_mark = line((2.65, -1.34), (2.65, -1.06), FOAM, 5)
        label = creek_label("Ankle-deep, slow", BLUE)
        bad = warning(alert_scene_icon("fast"))
        self.play(FadeOut(small_child), FadeOut(second_adult), Create(depth), Create(depth_mark),
                  FadeIn(bad), swap(new_label, label), run_time=0.89)
        self.at("wear closed toe")
        new_label = creek_label("Closed-toe shoes")
        glass = warning(alert_scene_icon("glass"))
        self.play(swap(label, new_label), swap(bad, glass), run_time=0.78)
        self.at("never drink creek", lead=0.45)
        no_drink = warning(alert_scene_icon("cup"))
        label = creek_label("Never drink creek water", RED)
        self.play(swap(glass, no_drink), swap(new_label, label), FadeOut(depth), FadeOut(depth_mark),
                  run_time=0.78)
        self.at("taste wild plants", lead=0.25)
        no_berries = warning(alert_scene_icon("berries"))
        new_label = creek_label("Never taste wild plants", RED)
        self.play(swap(no_drink, no_berries), swap(label, new_label), run_time=0.70)
        self.at("keep tiny animals", lead=0.45)
        away = warning(alert_scene_icon("animals"))
        label = creek_label("Keep small objects away", RED)
        self.play(swap(no_berries, away), swap(new_label, label), run_time=0.90)
        self.at("call 911", lead=0.30)
        self.play(swap(label, creek_label("Choking · Call 911", RED)), FadeOut(away),
                  run_time=0.79)
        self.finish()


def catch_people():
    return (person(-3.40, -1.36, 3.24, TEAL, reach=True),
            person(-0.55, -1.35, 1.92, GOLD, reach=True))


class S05Catch(SpokenScene):
    def construct(self):
        world = creek()
        risky, safe = world[7][2], world[7][4]
        tray = tray_side(3.85, 0.83, 2.50)
        dry_tray = tray_side(3.85, 0.83, 2.50, wet=False)
        shoal = gravel_shoal()
        self.add(world, shoal, dry_tray)
        self.add(risky, safe)
        self.at("fill the shaded")
        fill_cup = cup(3.70, 1.82).rotate(-1.12)
        pour = VGroup(*[line((4.01+i*0.12, 1.61), (4.10+i*0.12, 1.08), FOAM, 5)
                        for i in range(3)])
        self.play(FadeIn(fill_cup, shift=DOWN*0.36), Create(pour), run_time=0.63)
        self.play(Transform(dry_tray[1], tray[1]), run_time=0.94)
        self.at("two to three", lead=0.10)
        depth = creek_label("2 to 3 cm", BLUE, x=3.85, y=2.55, size=32)
        self.play(FadeOut(pour), FadeOut(fill_cup, shift=LEFT*0.40),
                  FadeIn(depth), run_time=0.58)
        adult, child = catch_people()
        self.at("creek water", lead=0.12)
        self.play(FadeIn(adult, shift=RIGHT*0.50), run_time=0.81)
        self.at("ask your child")
        on_bank = person(5.95, 0.95, 1.50, GOLD)
        self.play(FadeOut(depth), FadeIn(on_bank), run_time=0.50)
        self.at("what do you think", lead=0.38)
        bubble = boxed_label("What lives under this rock?", color=GOLD,
                             size=36, fill_opacity=0.08).move_to(point(0, 2.91))
        self.play(FadeIn(bubble), run_time=0.43)
        self.at("look for snakes", lead=0.43)
        scan = DashedVMobject(path([(-3.23, 1.42), (-2.98, 0.48),
                                    (-2.38, -0.80)], GOLD, 4), num_dashes=12)
        self.play(FadeOut(bubble), Create(scan), run_time=1.0)
        self.at("lift the rock", lead=0.49)
        danger = crayfish(-1.99, -1.58).scale(0.69)
        self.play(FadeOut(scan), risky.animate.shift(UP*1.36+LEFT*0.40).rotate(0.32),
                  Transform(adult[4], reaching_arm(adult, -2.62, 0.19)),
                  run_time=1.32)
        self.play(FadeIn(danger, shift=RIGHT*0.30), run_time=0.68)
        motion(danger, dx=0.24, dy=0.07, speed=2.4)
        self.at("gently put the rock")
        prompt = creek_label("Set the rock back gently", GOLD)
        self.play(FadeIn(prompt), run_time=0.55)
        self.at("see a crayfish", lead=0.0)
        self.play(FadeOut(danger), risky.animate.rotate(-0.32).shift(DOWN*1.36+RIGHT*0.40),
                  Transform(adult[4], reaching_arm(adult, -2.48, -0.25)),
                  run_time=2.50)
        self.at("at a safe rock", lead=0.65)
        adult_next = person(0.53, -1.39, 3.24, TEAL, reach=True)
        self.play(FadeOut(prompt), Transform(adult, adult_next), run_time=0.70)
        self.play(safe.animate.shift(UP*1.04+LEFT*0.16).rotate(0.30),
                  Transform(adult[4], reaching_arm(adult, 1.39, -0.13)), run_time=0.90)
        checked = DashedVMobject(path([(0.65, 1.40), (0.96, 0.50), (1.67, -0.83)], GOLD, 4),
                                 num_dashes=12)
        self.play(Create(checked), run_time=0.58)
        self.at("hold the strainer", lead=0.58)
        child.move_to(point(2.65, -1.30), aligned_edge=DOWN)
        sieve = strainer(2.97, -1.15, 0.66)
        child[4].become(reaching_arm(child, 3.51, -0.88))
        self.play(FadeOut(checked), Transform(on_bank, child), FadeIn(sieve), run_time=0.82)
        downstream = creek_label("Strainer flat, just downstream", BLUE)
        self.play(FadeIn(downstream), run_time=0.40)
        self.at("gently rub the underside", lead=0.75)
        palm = oval(0.38, 0.23, 1.63, -0.97, TEXT, GREY)
        shoulder = tuple(adult[4].get_start()[:2])

        def rub_arm():
            hand = tuple(palm.get_center()[:2])
            return path([shoulder, (0.93, -0.52), (1.10, -1.01), hand], TEXT, 6)

        rub = rub_arm()
        self.play(FadeOut(downstream), FadeIn(rub), FadeIn(palm), run_time=0.45)
        motion(palm, dx=0.34, dy=0.06, speed=5.1)
        palm.add_updater(lambda _: rub.become(rub_arm()))
        flecks = VGroup(*[Dot(point(1.65+0.15*i, -1.02-i*0.019), radius=0.039,
                              color=GOLD) for i in range(5)])
        self.add(flecks)
        self.play(flecks.animate.shift(RIGHT*0.92+DOWN*0.11), run_time=1.45)
        self.at("about 30 seconds")
        self.play(FadeIn(creek_label("Rub gently for about 30 seconds", GOLD)), run_time=0.52)
        self.finish()


SORTED_X = (-2.28, 0.58, 3.44)
SORTED_LABELS = ("Crawlers", "Swimmers", "Stay still")


def sort_headers():
    return VGroup(*(T(word, size=31, color=INK, weight=BOLD).move_to(point(x, 1.13))
                    for x, word in zip(SORTED_X, SORTED_LABELS)))


def animals_to_sort():
    return VGroup(
        nymph("mayfly", -1.70, -0.58, 0.31, 0.35),
        nymph("mayfly_wide", 0.08, -1.43, 0.31, 2.55),
        nymph("stonefly", 1.09, -0.34, 0.32, -0.51),
        nymph("stonefly_wide", 2.05, -1.41, 0.27, 1.04),
        nymph("mayfly", 3.45, -0.49, 0.28, 2.41),
        nymph("stonefly", 3.88, -1.66, 0.27, 0.32),
    )


def sorted_positions():
    return [point(x+offset, y) for x in SORTED_X
            for offset, y in [(-0.24, -0.22), (0.23, -1.33)]]


def mixed_nymphs():
    return VGroup(
        nymph("mayfly", -1.96, 0.43, 0.69, 0.24),
        nymph("mayfly_wide", -0.65, -1.32, 0.68, -0.38),
        nymph("stonefly", 1.35, 0.46, 0.67, -0.38),
        nymph("stonefly_wide", 3.15, -1.16, 0.65, 0.25),
    )


class S06LookSort(SpokenScene):
    def construct(self):
        self.add(tray_view())
        sieve = strainer(-3.86, 0.95, 1.12)
        specks = VGroup(*[Dot(point(-3.49+i*0.16, 0.66-i*0.05), radius=0.048,
                              color=MAYFLY) for i in range(6)])
        self.add(sieve)
        self.at("tip the strainer")
        self.play(sieve.animate.rotate(-0.74).shift(DOWN*0.36), run_time=0.78)
        self.add(specks)
        self.play(specks.animate.shift(DOWN*0.90+RIGHT*1.38), run_time=0.70)
        self.at("try three or four")
        samples = VGroup(*[rock(-5.44+(i%2)*0.55, -0.35-i*0.59, 0.65, 0.42)
                           for i in range(4)])
        self.play(FadeOut(sieve), LaggedStart(*(GrowFromCenter(r) for r in samples), lag_ratio=0.30),
                  run_time=1.00)
        self.at("give the mud")
        silt = VGroup(*[oval(1.54, 0.63, -1.80+i*0.59, -0.70+0.26*np.sin(i), "#9F9078")
                        for i in range(7)]).set_opacity(0.34)
        self.play(FadeIn(silt), FadeOut(specks), run_time=0.45)
        self.play(FadeOut(silt, shift=DOWN*0.50), run_time=1.80)
        self.at("watch for specks", lead=0.45)
        animals = animals_to_sort()
        self.play(FadeIn(animals), FadeOut(samples), run_time=0.50)
        for i, animal in enumerate(animals[:4]):
            motion(animal, dx=0.18 if i < 2 else 0.41, dy=0.12 if i < 2 else 0.26,
                   speed=1.7 if i < 2 else 3.5, phase=i*0.8)
        self.at("why do you think")
        ask = top_question("Why do you think they hide under rocks?")
        self.play(FadeIn(ask), run_time=0.45)
        self.at("use the spoon", lead=0.42)
        tool = spoon(-4.20, -0.72, 1.03).rotate(-0.29)
        self.play(FadeOut(ask), FadeIn(tool), run_time=0.43)
        labels = sort_headers()
        targets = sorted_positions()
        for i, phrase in enumerate(("sort crawlers", "swimmers", "animals that stay still")):
            lead = (0.30, 0.32, 0.18)[i]
            self.at(phrase, lead=lead)
            for animal in animals[i*2:i*2+2]:
                animal.clear_updaters()
            self.play(tool.animate.move_to(point(SORTED_X[i]-0.69, -0.78)),
                      animals[i*2].animate.move_to(targets[i*2]),
                      animals[i*2+1].animate.move_to(targets[i*2+1]), run_time=0.60)
            self.play(FadeIn(labels[i]), run_time=0.20)
        self.play(FadeOut(tool), run_time=0.32)
        self.finish()


class S07PredictQ(SpokenScene):
    def construct(self):
        animals = animals_to_sort()
        for m, target in zip(animals, sorted_positions()):
            m.move_to(target)
        labels = sort_headers()
        self.add(tray_view(), animals, labels)
        self.at("you have sorted")
        for i, animal in enumerate(animals[:4]):
            motion(animal, dx=0.19 if i < 2 else 0.33, dy=0.10, speed=1.9+i*0.41, phase=i)
        self.at("now look at", lead=0.45)
        new_mix = mixed_nymphs()
        self.play(FadeOut(labels), FadeOut(animals), run_time=0.47)
        self.play(FadeIn(new_mix), run_time=0.64)
        self.at("several kinds of", lead=0.35)
        examples = VGroup()
        for i, animal in enumerate(new_mix):
            ring = Ellipse(width=animal.width+0.30, height=animal.height+0.30, color=INK,
                           stroke_width=2.5).move_to(animal)
            examples.add(ring)
        self.play(LaggedStart(*(Create(ring) for ring in examples), lag_ratio=0.64),
                  run_time=2.35)
        self.at("what might that", lead=0.30)
        self.play(FadeOut(examples), FadeIn(top_question(QUESTION)), run_time=0.54)
        self.play(
            *(animal.animate.shift(0.25*d)
              for animal, d in zip(new_mix, (RIGHT, LEFT, DR, UL))),
            rate_func=there_and_back, run_time=1.65,
        )
        self.finish()


class S08PredictPause(NarratedScene):
    def construct(self):
        # Only the creek moves in this 4.5-second thinking pause.
        self.add(tray_view(), mixed_nymphs(), top_question(QUESTION))
        self.wait(self.narration_s)


def caddisfly_case(x, y):
    case = shape([(-1.31, -0.34), (-1.16, 0.36), (0.38, 0.40),
                  (0.71, 0.20), (0.67, -0.34)], "#967657", "#5B4838", 3)
    bits = VGroup(*[line((x0, y0), (x0+0.41, y0+0.12), color, 7)
                    for x0, y0, color in [
                        (-1.14, -0.20, "#C2A374"), (-0.63, -0.15, "#5F4731"),
                        (-0.13, -0.25, "#B08C59"), (-0.95, 0.11, "#745234"),
                        (-0.45, 0.12, "#C2A374"), (0.10, 0.14, "#654932"),
                        (-1.00, 0.30, "#9F7849"), (0.13, -0.028, "#A17F54")]])
    head = oval(0.52, 0.47, 0.72, 0, "#584738")
    legs = VGroup(*[path([(0.69, s*0.11), (0.96, s*0.34), (1.14, s*0.35)],
                         "#584738", 4) for s in (-1, 1)])
    sand = VGroup(*[oval(0.14, 0.11, x0, y0, "#C3A988")
                    for x0, y0 in [(-0.77, 0.02), (-0.31, -0.08), (-0.21, 0.24), (0.27, -0.15)]])
    return VGroup(legs, head, case, bits, sand).move_to(point(x, y))


def water_clues():
    return VGroup(
        path([(-2.93, -0.22), (-2.59, 0.02), (-2.24, -0.37),
              (-1.86, -0.55), (-1.53, -0.29)], "#80605E", 13),
        oval(1.03, 0.38, 0.49, -0.25, "#61564E").rotate(-0.46),
        path([(2.55, -0.48), (2.79, -0.04), (3.05, 0.17),
              (3.31, -0.06), (3.43, -0.38)], "#B44947", 12),
    )


class S09RevealIdea(SpokenScene):
    def construct(self):
        self.add(tray_view())
        mixture = mixed_nymphs()
        old = top_question(QUESTION)
        self.add(mixture, old)
        self.at("several kinds can")
        good = creek_label("Several kinds can be a good sign", GREEN)
        self.play(swap(old, good), run_time=0.73)
        for i, animal in enumerate(mixture):
            motion(animal, dx=0.14, dy=0.13, speed=1.4+0.23*i, phase=i)
        self.at("need cool clean", lead=0.43)
        conditions = creek_label("Cool, clean, oxygen-rich water", BLUE)
        self.play(swap(good, conditions), run_time=0.80)
        self.at("mayfly young usually", lead=0.94)
        may = nymph("mayfly", 0.57, -0.36, 1.93)
        name = T("Mayfly young", size=32, color=INK, weight=BOLD).move_to(point(0.57, 1.34))
        self.play(FadeOut(mixture), FadeOut(conditions), run_time=0.40)
        self.play(FadeIn(may, scale=0.87), FadeIn(name), run_time=0.53)
        self.at("usually have three tails", lead=0.45)
        tails = creek_label("Usually three tails", GOLD)
        self.play(FadeIn(tails), run_time=0.42)
        self.at("side gills", lead=0.45)
        gills = T("Side gills", size=30, color=INK, weight=BOLD)
        target = may.gills.get_top()
        pointer = Arrow(point(2.45, 0.92), target+UP*0.10, color=INK,
                        buff=0.08, stroke_width=5, max_tip_length_to_length_ratio=0.22)
        gills.next_to(pointer.get_start(), RIGHT, buff=0.20)
        self.play(FadeIn(gills), GrowArrow(pointer), run_time=0.40)
        self.at("stonefly young have", lead=0.62)
        stone = nymph("stonefly", 0.57, -0.36, 1.93)
        stone_name = T("Stonefly young", size=32, color=INK, weight=BOLD).move_to(name)
        self.play(FadeOut(may), FadeOut(pointer), FadeOut(gills), FadeOut(name),
                  FadeOut(tails), run_time=0.35)
        self.play(FadeIn(stone, scale=0.88), FadeIn(stone_name), run_time=0.43)
        self.at("two tails", lead=0.45)
        two = creek_label("Two tails", GOLD)
        self.play(FadeIn(two), run_time=0.25)
        self.at("caddisfly young", lead=0.49)
        caddis = caddisfly_case(0.57, -0.36).scale(1.78)
        caddis_name = T("Caddisfly young", size=32, color=INK, weight=BOLD).move_to(name)
        self.play(FadeOut(stone), FadeOut(two), FadeOut(stone_name), run_time=0.41)
        self.play(FadeIn(caddis, scale=0.86), FadeIn(caddis_name), run_time=0.55)
        self.at("in sand or stick")
        cases = creek_label("Often sand or sticks", GOLD)
        self.play(FadeIn(cases), run_time=0.45)
        self.at("mostly worms", lead=0.44)
        clues = water_clues()
        self.play(FadeOut(caddis), FadeOut(cases), FadeOut(caddis_name), run_time=0.38)
        self.play(FadeIn(clues[0]), run_time=0.38)
        self.at("leeches")
        self.play(FadeIn(clues[1]), run_time=0.39)
        self.at("tiny red larvae")
        self.play(FadeIn(clues[2]), run_time=0.40)
        for i, creature in enumerate(clues):
            motion(creature, dx=0.16, dy=0.12, speed=1.5+i*0.4, phase=i)
        self.at("suggest less healthy")
        self.play(FadeIn(creek_label("Look at the mix", GOLD)), run_time=0.50)
        self.finish()


def food_web():
    leaf_bits = VGroup(*[
        shape([(-0.52, 0.14), (-0.04, 0.41), (0.50, 0.06), (0.18, -0.32), (-0.24, -0.17)],
              "#C9974B", "#ECCB82", 2).scale(scale).rotate(angle).move_to(point(x, y))
        for x, y, scale, angle in [(-5.26, -0.46, 1, 0.25), (-4.73, -0.91, 0.63, -0.40),
                                   (-5.42, -1.06, 0.49, 0.61)]])
    insects = VGroup(nymph("mayfly", -1.97, -0.52, 0.47, 0.20),
                     nymph("stonefly", -0.93, -1.00, 0.40, -0.28))
    insects[0].set_color(GOLD)
    insects[1].set_color("#D5C59C")
    fish = VGroup(
        shape([(4.05, -0.52), (4.75, 0.04), (4.58, -0.59), (4.71, -1.00)],
              "#81B7A0", "#C9DFBB", 3),
        oval(2.26, 0.91, 3.17, -0.53, "#81B7A0", "#C9DFBB", 3),
        shape([(3.07, -0.51), (3.72, -0.49), (3.54, -0.90)], "#558680"),
        Dot(point(2.48, -0.41), radius=0.065, color=INK),
    )
    return leaf_bits, insects, fish


def web_arrows():
    return (Arrow(point(-4.45, -0.51), point(-2.74, -0.51), buff=0.10, color=GOLD,
                  stroke_width=7),
            Arrow(point(-0.27, -0.65), point(1.95, -0.63), buff=0.12, color=GOLD,
                  stroke_width=7))


class S10FoodWeb(SpokenScene):
    def construct(self):
        self.add(creek())
        leaves, insects, fish = food_web()
        first, second = web_arrows()
        self.at("a creek is")
        self.play(FadeIn(leaves), run_time=0.63)
        self.at("connected food web")
        self.play(FadeIn(insects), run_time=0.70)
        for i, insect in enumerate(insects):
            motion(insect, dx=0.22, dy=0.13, speed=1.4+i*0.62, phase=i)
        self.at("its hidden animals")
        self.play(FadeIn(fish, shift=LEFT*0.55), run_time=0.90)
        motion(fish, dx=0.19, dy=0.10, speed=1.56)
        self.at("what do you think")
        q = top_question("What eats what?")
        self.play(FadeIn(q), run_time=0.49)
        self.at("many eat leaf bits", lead=0.42)
        self.play(GrowArrow(first), run_time=0.72)
        self.at("fish eat them", lead=0.34)
        self.play(GrowArrow(second), run_time=0.73)
        self.at("one visit is a clue")
        self.play(swap(q, creek_label("One visit gives a clue", TEAL)), run_time=0.68)
        self.finish()


def wash_hands():
    stream = VGroup(*[path([(4.98+i*0.12, 1.44), (4.97+i*0.12, 1.19),
                            (4.89+i*0.12, 0.98)], BLUE, 4) for i in range(3)])
    hands = VGroup(path([(4.01, 0.70), (4.36, 0.68), (4.72, 0.86), (5.10, 0.85)], TEXT, 12),
                   path([(5.83, 0.46), (5.40, 0.46), (5.07, 0.62), (4.64, 0.62)], TEXT, 12))
    suds = VGroup(*[Circle(radius=r, color=TEXT, stroke_width=2).move_to(point(x, y))
                     for x, y, r in [(4.66, 1.03, 0.11), (4.88, 0.93, 0.08),
                                     (5.15, 1.14, 0.11), (5.28, 0.95, 0.07)]])
    for i, bubble in enumerate(suds):
        bob(bubble, amp=0.08, speed=3, seed=i)
    return VGroup(stream, hands, suds)


class S11ReturnClose(SpokenScene):
    def construct(self):
        world = creek()
        lifted = world[7][4].shift(UP*1.04+LEFT*0.16).rotate(0.30)
        tray = tray_side(4.08, 0.67, 2.62)
        self.add(world, tray)
        self.at("pour the tray back")
        stream = VGroup(*[path([(2.91+i*0.08, 0.50), (2.66+i*0.08, 0.08),
                               (2.52+i*0.08, -0.44)], FOAM, 4) for i in range(3)])
        self.play(tray.animate.rotate(0.45).shift(LEFT*0.39), Create(stream), run_time=1.35)
        returned = VGroup(nymph("mayfly", 2.73, -0.02, 0.23, 2.9),
                          nymph("stonefly", 2.84, 0.21, 0.22, 3.6)).set_color(GOLD)
        self.play(FadeIn(returned), run_time=0.39)
        self.play(returned[0].animate.move_to(point(0.56, -0.71)),
                  returned[1].animate.move_to(point(1.11, -1.05)), run_time=2.15)
        self.at("set each rock back")
        self.play(lifted.animate.rotate(-0.30).shift(DOWN*1.04+RIGHT*0.16),
                  FadeOut(stream), FadeOut(returned), FadeOut(tray), run_time=1.54)
        self.at("empty any containers")
        other_cup = cup(4.98, 0.81)
        self.play(FadeIn(other_cup), run_time=0.46)
        self.play(other_cup.animate.rotate(0.92).shift(LEFT*0.27), run_time=0.69)
        self.play(FadeOut(other_cup), run_time=0.61)
        self.at("wash hands with", lead=0.40)
        hands = wash_hands()
        self.play(FadeIn(hands), run_time=0.55)
        self.at("wash the gear", lead=0.45)
        rinse, palms, suds = hands
        clean = strainer(5.47, 0.83, 0.85)
        runoff = VGroup(*[line((x, 0.55), (x-0.04, 0.40), FOAM, 3)
                          for x in (4.93, 5.06, 5.19)])
        self.remove(hands)
        self.add(rinse, palms, suds)
        self.play(FadeOut(palms), FadeOut(suds), FadeIn(clean), FadeIn(runoff),
                  run_time=0.25)
        for i, drop in enumerate(runoff):
            bob(drop, amp=0.07, speed=5, seed=i)
        self.at("check everyone for ticks", lead=0)
        tick_check = lens(5.12, 0.78, 0.90)
        self.play(FadeOut(rinse), FadeOut(clean), FadeOut(runoff), run_time=0.35)
        self.play(FadeIn(tick_check), FadeIn(creek_label("Check for ticks", TEAL)), run_time=0.46)
        self.at("the mix you found", lead=0.45)
        self.play(*(FadeOut(m) for m in list(self.mobjects)[1:]), run_time=0.45)
        leaves, insects, fish = food_web()
        first, second = web_arrows()
        self.play(FadeIn(leaves), FadeIn(insects), FadeIn(fish), run_time=0.65)
        self.play(GrowArrow(first), GrowArrow(second), run_time=0.80)
        self.finish()


class S12End(EndCard):
    LINE = "Tiny creek animals share a food web and signal water health."
