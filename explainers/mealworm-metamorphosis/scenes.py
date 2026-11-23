"""A continuous illustrated workbench for the Mealworms to Beetles parent guide."""

from bp_parts import *
from bp_style import EndCard

# COLOR MAP: TEAL for equipment and the workbench (as in the setup template),
# GOLD for actions, GREEN for observations, RED for safety. The insects and
# their surroundings use the natural colors of the lesson's illustrations.
CREAM = "#FFF0C8"
LARVA = "#F0BB68"
OAT = "#AC7448"
CORK = "#6E4938"
WOOD = "#45312F"
CARROT = "#F48A45"
SHELL = "#442A32"
GLASS = "#8ED3D2"
PAPER = "#F2DEB6"
INK = "#35282C"
SKIN = "#DA9670"
CHILD_SKIN = "#EEB48B"

QUESTION = "What comes out\nof the pupa?"
QUESTION_POSITION = dict(y=0.45, left=-5.57, max_w=4.76, size=39, color=CREAM)


def xy(x, y):
    return np.array([x, y, 0.0])


def rect(w, h, fill, stroke=None, r=0.15, opacity=1):
    return RoundedRectangle(
        width=w, height=h, corner_radius=r, stroke_color=stroke or fill,
        stroke_width=2.5 if stroke else 0, fill_color=fill, fill_opacity=opacity,
    )


def oval(w, h, fill, stroke=None, opacity=1):
    return Ellipse(
        width=w, height=h, stroke_color=stroke or fill,
        stroke_width=2.5 if stroke else 0, fill_color=fill, fill_opacity=opacity,
    )


def path(points, color, width=3):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(
        [xy(x, y) for x, y in points]
    )


def polygon(points, fill, stroke=None, opacity=1):
    return Polygon(
        *[xy(x, y) for x, y in points], fill_color=fill, fill_opacity=opacity,
        stroke_color=stroke or fill, stroke_width=2.5 if stroke else 0,
    )


def positioned(mob, x, y, width):
    return mob.scale_to_fit_width(width).move_to(xy(x, y))


def label(words, x, y, color=CREAM, size=32):
    return T(words, size, color, weight=BOLD).move_to(xy(x, y))


def floor():
    return rect(13.2, 2.30, WOOD, r=0.24).move_to(xy(0, -2.52)).set_z_index(-20)


def flakes(w, h, count, color=PAPER, seed=9):
    rng = np.random.default_rng(seed)
    grains = VGroup()
    for _ in range(count):
        x, y = rng.uniform(-1, 1, 2)
        if x*x + y*y <= 1:
            grain = oval(rng.uniform(0.09, 0.22), 0.05, color, opacity=0.64)
            grain.rotate(rng.uniform(-1, 1)).move_to(xy(x*w/2, y*h/2))
            grains.add(grain)
    return grains


def larva(width=3.3, legs=True, shed=False, motion=False, angle=0, phase=0):
    """Eleven articulated rings and three leg pairs at the head end."""
    n = 11
    direction = np.array([np.cos(angle), np.sin(angle), 0])
    normal = np.array([-np.sin(angle), np.cos(angle), 0])
    positions = np.linspace(-0.43, 0.43, n) * width
    rings = VGroup()
    feet = VGroup()
    sizes = (0.09, 0.12, 0.145, 0.16, 0.173, 0.18, 0.18, 0.175, 0.165, 0.148, 0.13)
    for i, size in enumerate(sizes):
        color = OAT if i == n - 1 else LARVA
        shell = oval(width*0.15, width*size, color, CORK)
        shine = oval(width*0.075, width*size*0.16, CREAM, opacity=0.65)
        shine.shift(UP * width*size*0.23)
        rings.add(VGroup(shell, shine).rotate(angle, about_point=ORIGIN))
    if legs:
        for i in range(n - 4, n - 1):
            for side in (-1, 1):
                foot = path([(0, 0), (0.04, side*0.095), (0.09, side*0.152),
                             (0.15, side*0.165)], OAT, 4)
                feet.add(foot.scale(width).rotate(angle, about_point=ORIGIN))
    animal = VGroup(feet, rings)

    def pose(time, center):
        offsets = [
            center + x*direction + width*0.074*np.sin(i*0.56 - time*3.6)*normal
            for i, x in enumerate(positions)
        ]
        for ring, offset in zip(rings, offsets):
            ring.move_to(offset)
        for k, foot in enumerate(feet):
            foot.shift(offsets[n - 4 + k//2] - foot.get_start())

    pose(phase, ORIGIN)
    if shed:
        rings.set_opacity(0.39)
        feet.set_stroke(opacity=0.39)
    if motion:
        animal.clock = phase

        def wriggle(mob, dt):
            old = mob.clock
            mob.clock += dt
            for i, ring in enumerate(rings):
                offset = width*0.074*(np.sin(i*0.56-mob.clock*3.6)-np.sin(i*0.56-old*3.6))
                ring.shift(offset*normal)
            for k, foot in enumerate(feet):
                foot.shift(rings[n-4+k//2].get_center() - foot.get_start())

        animal.add_updater(wriggle)
    return animal


def pupa(width=3.1):
    markings = VGroup()
    body = VGroup()
    for i in range(7):
        a = -0.82 + i*0.27
        ring = oval(0.73 - i*0.049, 1.10 - i*0.10, CREAM, OAT)
        x, y = -0.80 + i*0.30, 0.19 - 0.71*np.sin(i*0.22)
        body.add(ring.rotate(a).move_to(xy(x, y)))
    head = oval(0.90, 0.86, PAPER, OAT).rotate(-0.28).move_to(xy(-1.0, 0.53))
    wing = oval(0.91, 0.44, PAPER, OAT).rotate(-0.29).move_to(xy(-0.54, -0.13))
    for i in range(3):
        x = -0.89 + i*0.17
        markings.add(path([(x-0.12, 0.27), (x+0.05, 0.12),
                           (x+0.28, 0.17), (x+0.42, 0.07)], OAT, 2.4))
    return VGroup(body, head, wing, markings).scale_to_fit_width(width).move_to(ORIGIN)


def beetle(width=2.5, pale=False, shadow=False, motion=False):
    color = PAPER if pale else SHELL
    outline = OAT if pale else "#A87968"
    legs = VGroup()
    for i in range(3):
        for side in (-1, 1):
            y = 0.50 - i*0.47
            legs.add(path([(side*0.29, y), (side*0.80, y+0.18-i*0.12),
                           (side*1.06, y-0.06-i*0.12)], outline, 5))
    feelers = VGroup(*[
        path([(s*0.21, 0.96), (s*0.43, 1.23), (s*0.68, 1.31)], outline, 3)
        for s in (-1, 1)
    ])
    abdomen = oval(1.35, 1.82, color, outline).move_to(xy(0, -0.30))
    thorax = oval(1.08, 0.69, color, outline).move_to(xy(0, 0.59))
    head = oval(0.72, 0.55, color, outline).move_to(xy(0, 0.93))
    seam = Line(xy(0, 0.25), xy(0, -1.14), color=outline, stroke_width=2)
    detail = VGroup(*[
        path([(s*0.27, 0.26), (s*0.42, -0.25), (s*0.30, -0.88)], outline, 1.5)
        for s in (-1, 1)
    ])
    insect = VGroup(legs, feelers, abdomen, seam, detail, thorax, head)
    insect.scale_to_fit_width(width).move_to(ORIGIN)
    if shadow:
        insect.set_color("#A6856D").set_opacity(0.39)
    if motion:
        bases = [leg.copy() for leg in legs]
        insect.clock = 0.0

        def walk(mob, dt):
            mob.clock += dt
            for index, (leg, base) in enumerate(zip(legs, bases)):
                leg.become(base).rotate(0.27*np.sin(mob.clock*7 + index*np.pi/2),
                                        about_point=base.get_start())

        insect.add_updater(walk)
    return insect


def slice_carrot():
    base = oval(2.13, 0.83, "#BD582D", CORK)
    face = oval(2.13, 0.77, CARROT, "#FFD293").shift(UP*0.11)
    core = oval(1.53, 0.49, "#FCAC61", "#C86733").shift(UP*0.11)
    center = oval(0.74, 0.21, "#FFC082").shift(UP*0.11)
    return VGroup(base, face, core, center)


def lid(holes=True):
    rim = rect(8.87, 1.47, "#4B8082", GLASS, r=0.29)
    inside = rect(8.25, 1.06, "#346064", GLASS, r=0.23)
    vents = VGroup(*[
        oval(0.105, 0.055, BG).move_to(xy(-3.25 + i*0.9, y))
        for y in (-0.19, 0.19) for i in range(8)
    ])
    out = VGroup(rim, inside)
    out.vents = vents
    if holes:
        out.add(vents)
    return out


def bedding(width=8.0):
    soil = polygon([(-3.91, 0.21), (3.91, 0.21), (3.63, -0.76), (-3.61, -0.76)],
                   CORK, OAT)
    top = oval(7.85, 1.16, OAT, PAPER).shift(UP*0.24)
    grains = flakes(7.58, 1.04, 150).shift(UP*0.24)
    return VGroup(soil, top, grains).scale_to_fit_width(width)


def tub(x=0, y=-0.55, width=9.0, *, filled=True, carrots=2, worms=0, closed=False,
        adults=False, motion=False):
    """The same clear tub in all workbench and shelf views."""
    wall = polygon([(-4.5, 1.48), (4.5, 1.48), (3.99, -1.92), (-3.99, -1.92)],
                   "#23464E", GLASS)
    interior = oval(8.96, 1.34, "#17353D", GLASS).shift(UP*1.51)
    soil = bedding().move_to(xy(0, -0.94))
    crops = VGroup(*[
        positioned(slice_carrot(), cx, cy, w)
        for cx, cy, w in [(-2.02, -0.55, 2.61), (1.10, -0.88, 2.15)][:carrots]
    ])
    insects = VGroup()
    for i, (cx, cy, w, a) in enumerate([
        (-1.72, -0.35, 2.10, -0.17), (1.87, -0.36, 1.95, 0.30),
        (0.5, -1.03, 1.47, -0.20), (2.92, -0.98, 0.91, 0.22)
    ][:worms]):
        insects.add(larva(w, angle=a, phase=i*0.4).move_to(xy(cx, cy)))
    if adults:
        insects.add(beetle(1.35).rotate(-0.50).move_to(xy(2.46, -0.43)))
    lip = path([(-4.5, 1.48), (-3.0, 0.91), (0, 0.83), (3, 0.91), (4.5, 1.48)], GLASS, 4)
    highlights = VGroup(
        path([(-4.16, 0.94), (-4.01, -0.16), (-3.93, -1.20)], "#5D9297", 5),
        path([(4.14, 0.76), (4.00, -0.38), (3.85, -1.34)], "#5D9297", 4),
    )
    cover = positioned(lid(), 0, 1.61, 9.24).stretch(0.65, 1)
    scene = VGroup(interior, wall)
    if filled:
        scene.add(soil, crops, insects)
    scene.add(lip, highlights)
    if closed:
        scene.add(cover)
    scene.parts = VGroup(soil, crops, insects)
    scene.insects, scene.cover = insects, cover
    scene.scale(width/9.24, about_point=ORIGIN).shift(xy(x, y))
    if motion:
        for i, bug in enumerate(insects):
            bug.phase = i*1.2

            def drift(mob, dt, distance=0.16*width/9):
                old = mob.phase
                mob.phase += 4.2*dt
                mob.shift(xy(distance*(np.sin(mob.phase)-np.sin(old)),
                             distance*0.48*(np.cos(mob.phase)-np.cos(old))))

            bug.add_updater(drift)
    return scene


def dish(x=2.85, y=-0.42, width=6.5, *, bran=True):
    underside = oval(width, width*0.49, "#41656B", GLASS).shift(DOWN*0.20)
    rim = oval(width, width*0.47, "#6D9D98", GLASS)
    inner = oval(width*0.86, width*0.35, "#334F54", "#B3DED1").shift(UP*0.06)
    out = VGroup(underside, rim, inner)
    if bran:
        oat = oval(width*0.77, width*0.27, CORK, OAT)
        out.add(oat, flakes(width*0.71, width*0.24, 95, seed=7))
    return out.shift(xy(x, y))


def dish_pupa():
    return pupa(3.32).move_to(xy(2.85, -0.28))


def predict_card():
    card = question_card(QUESTION, **QUESTION_POSITION)
    plate = rect(5.65, 2.30, "#344A49", "#81B4AF", r=0.23).move_to(xy(-3.48,0.44))
    card.add_to_back(plate)
    card.plate = plate
    return card


def cat(width, color="#DBA27A"):
    tail = path([(0.54, -0.89), (1.12, -0.63), (1.28, -0.11), (1.45, 0.22)], color, 14)
    body = oval(1.47, 1.60, color, CORK).shift(DOWN*0.42)
    head = oval(1.32, 1.1, color, CORK).shift(UP*0.57)
    ears = VGroup(*[
        polygon([(s*0.68, 0.73), (s*0.62, 1.47), (s*0.08, 0.99)], color, CORK)
        for s in (-1, 1)
    ])
    paws = VGroup(*[oval(0.48, 0.25, color, CORK).move_to(xy(s*0.35, -1.09))
                    for s in (-1, 1)])
    eyes = VGroup(*[oval(0.13, 0.17, INK).move_to(xy(s*0.23, 0.57)) for s in (-1, 1)])
    muzzle = oval(0.49, 0.32, CREAM).move_to(xy(0, 0.36))
    nose = oval(0.13, 0.08, SHELL).move_to(xy(0, 0.42))
    return VGroup(tail, body, ears, head, paws, muzzle, eyes, nose).scale_to_fit_width(width)


def spoon(width=3.1):
    handle = rect(2.30, 0.25, TEAL, GLASS, r=0.11).shift(RIGHT*0.61)
    scoop = oval(1.34, 0.82, "#6CB8B7", GLASS).shift(LEFT*0.86)
    well = oval(0.94, 0.53, "#34666D", "#92C9C5").shift(LEFT*0.89)
    return VGroup(handle, scoop, well).scale_to_fit_width(width)


def brush(width=3.3):
    shaft = rect(2.34, 0.24, CORK, SKIN, r=0.11).shift(RIGHT*0.56)
    collar = rect(0.44, 0.32, "#879FAB", "#C7DFDE", r=0.07).shift(LEFT*0.68)
    bristles = polygon([(-0.89, 0.14), (-1.48, 0.24), (-1.62, 0.06),
                        (-1.61, -0.11), (-1.02, -0.18), (-0.89, -0.14)], PAPER, OAT)
    return VGroup(shaft, collar, bristles).scale_to_fit_width(width)


def grain_bag(color=OAT):
    bag = polygon([(-0.93, -1.10), (0.95, -1.10), (1.04, 0.64),
                   (0.65, 1.15), (-0.66, 1.15), (-1.02, 0.64)], color, PAPER)
    window = oval(1.35, 1.08, CORK, CREAM).shift(DOWN*0.22)
    fold = Line(xy(-0.69, 0.87), xy(0.69, 0.87), color=CREAM, stroke_width=3)
    return VGroup(bag, fold, window, flakes(1.15, 0.83, 35).shift(DOWN*0.22))


def carton():
    box = polygon([(-1.42,0.52),(1.42,0.52),(1.17,-0.80),(-1.17,-0.80)], CORK, SKIN)
    top = oval(2.84, 0.89, OAT, PAPER).shift(UP*0.52)
    return VGroup(box, top, larva(1.50, angle=0.15).move_to(xy(-0.37, 0.50)),
                  larva(1.38, angle=-0.25).move_to(xy(0.50, 0.31)))


def carrot():
    body = polygon([(-1.20, 0.04), (0.71, 0.57), (1.07, 0.40), (1.15, -0.29),
                    (0.74, -0.51)], CARROT, SKIN)
    leaves = VGroup(*[
        oval(0.92, 0.22, GREEN).rotate(a).move_to(xy(1.38, y))
        for a, y in [(0.57, 0.38), (0.0, 0.15), (-0.40, -0.09)]
    ])
    grooves = VGroup(*[
        Line(xy(x, y), xy(x+0.07, y-0.15), color=CORK, stroke_width=2)
        for x, y in [(-0.52, 0.20), (0.15, 0.37), (0.69, 0.49)]
    ])
    return VGroup(leaves, body, grooves)


def hand(color=SKIN):
    palm = rect(0.96, 1.12, color, CORK, r=0.31).shift(DOWN*0.16)
    fingers = VGroup(*[
        rect(0.23, h, color, CORK, r=0.105).move_to(xy(x, y))
        for x, y, h in [(-0.34, 0.54, 0.79), (-0.11, 0.65, 0.97),
                        (0.12, 0.61, 0.90), (0.35, 0.49, 0.67)]
    ])
    thumb = rect(0.29, 0.74, color, CORK, r=0.13).rotate(-0.61).move_to(xy(-0.56, -0.08))
    sleeve = rect(0.78, 0.54, "#477F86", GLASS, r=0.17).move_to(xy(0, -0.88))
    return VGroup(fingers, thumb, palm, sleeve)


def person(width=2.6, child=False):
    tone = CHILD_SKIN if child else SKIN
    shirt = "#578F88" if child else "#527485"
    shoulders = rect(2.13, 1.56, shirt, GLASS, r=0.52).shift(DOWN*0.68)
    neck = rect(0.47, 0.61, tone, r=0.21).move_to(xy(0, 0.17))
    hair = oval(1.53, 1.61, SHELL, OAT).shift(UP*1.00)
    face = oval(1.18, 1.32, tone, SHELL).shift(UP*0.87)
    fringe = oval(1.25, 0.40, SHELL).rotate(0.19).shift(UP*1.45)
    eyes = VGroup(*[
        oval(0.10, 0.14, INK).move_to(xy(s*0.24, 0.95)) for s in (-1, 1)
    ])
    smile = path([(-0.14, 0.67), (0, 0.60), (0.15, 0.69)], CORK, 2)
    return VGroup(shoulders, neck, hair, face, fringe, eyes, smile).scale_to_fit_width(width)


def shelf():
    plank = rect(12.6, 0.36, OAT, SKIN, r=0.13).move_to(xy(0, -1.95))
    brackets = VGroup(*[
        polygon([(x-0.37, -2.14), (x+0.60, -2.14), (x-0.37, -3.03)], WOOD, CORK)
        for x in (-4.8, 4.8)
    ])
    return VGroup(brackets, plank).set_z_index(-12)


def phone():
    frame = rect(2.16, 3.75, SHELL, RED, r=0.30)
    screen = rect(1.83, 3.02, "#663C42", "#C88981", r=0.18).shift(UP*0.12)
    receiver = path([(-0.42, 0.61), (-0.45, 0.15), (-0.20, -0.34),
                     (0.12, -0.64), (0.47, -0.68)], CREAM, 11)
    receiver.add(oval(0.35, 0.46, CREAM).rotate(0.25).move_to(xy(-0.42, 0.58)),
                 oval(0.42, 0.32, CREAM).rotate(-0.20).move_to(xy(0.50, -0.65)))
    return VGroup(frame, screen, receiver, oval(0.21, 0.12, RED).shift(DOWN*1.60))


def notebook(x, y, width=3.3, heading="Our guess"):
    page = rect(width, width*0.82, PAPER, OAT, r=0.19).move_to(xy(x, y))
    spine = Line(page.get_corner(UL)+xy(0.34, -0.11), page.get_corner(DL)+xy(0.34, 0.11),
                 color=CARROT, stroke_width=2)
    head = fit_text(heading, max_w=width-0.65, size=33, min_size=28,
                    color=INK, weight=BOLD).move_to(xy(x+0.17, y+width*0.24))
    rules = VGroup(*[
        Line(xy(x-width*0.32, y+v), xy(x+width*0.36, y+v), color=OAT, stroke_width=2)
        for v in (0.05, -0.33, -0.71)
    ])
    book = VGroup(page, spine, head, rules)
    book.writing_at = xy(x+0.1, y-0.14)
    return book


def pencil():
    stem = polygon([(-0.62, -0.09), (0.64, -0.09), (0.64, 0.09), (-0.62, 0.09)], GOLD, OAT)
    tip = polygon([(-0.62, -0.09), (-0.62, 0.09), (-0.93, 0)], PAPER, OAT)
    lead = polygon([(-0.82, 0.04), (-0.82, -0.04), (-0.93, 0)], INK)
    return VGroup(stem, tip, lead).rotate(0.43)


def metric_ruler(x, y, span=4.80):
    """A schematic 0–3 cm ruler with ten equal millimetre divisions per cm."""
    panel = rect(span+1.42, 0.83, PAPER, OAT, r=0.13).move_to(xy(x+0.36, y))
    left = x-span/2
    marks = VGroup(*[
        Line(xy(left+i*span/30, y+0.35), xy(left+i*span/30, y+0.35-(0.19 if i%10 == 0 else 0.09)),
             color=CORK, stroke_width=2)
        for i in range(31)
    ])
    numbers = VGroup(*[
        label(str(i), left+i*span/3, y-0.17, INK, 28) for i in range(4)
    ])
    units = label("cm", x+span/2+0.56, y-0.17, INK, 28)
    ruler = VGroup(panel, marks, numbers, units)
    ruler.zero = left
    ruler.unit = span/3
    return ruler


def arrow(a, b, color=GOLD):
    return Arrow(a, b, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.20)


def hook_world():
    return tub(-0.52, -0.48, 11.55, carrots=1, worms=3, closed=True, motion=True)


class S01Hook(SpokenScene, TitleCard):
    TITLE = "Mealworms to Beetles: Parent Guide"
    LESSON = "Mealworms to Beetles"

    def construct(self):
        world = hook_world()
        self.add(floor(), world)
        self.at("is a mealworm")
        question = label("A worm?", -4.65, 2.83, CREAM, 58)
        self.play(FadeIn(question, shift=UP*0.13), run_time=0.55)
        self.at("it looks like")
        self.play(world.insects.animate.shift(RIGHT*0.45), run_time=1.35, rate_func=there_and_back)
        self.at("but keep a")
        self.play(FadeOut(question), run_time=0.50)
        self.at("something else climbs", lead=0.48)
        shade = beetle(1.35, shadow=True).rotate(-0.24).move_to(xy(5.66, -0.02))
        self.play(FadeIn(shade, shift=UP*0.25), run_time=0.75)
        self.play(FadeOut(shade), run_time=0.55)
        self.finish()


class S02Title(TitleCard):
    TITLE = S01Hook.TITLE
    LESSON = S01Hook.LESSON

    def construct(self):
        self.add(floor(), hook_world())
        title = T(self.LESSON, 55, CREAM, font=TITLE_FONT).move_to(xy(0, 3.15))
        guide = label("Parent Guide", 0, 2.54, GOLD, 28)
        self.play(FadeIn(title, shift=UP*0.12), FadeIn(guide), run_time=0.56)
        self.wait(self.narration_s - self.elapsed())


class S03Payoff(SpokenScene):
    def construct(self):
        base = floor()
        panels = TwoPanel("Kitten to cat", "Mealworm to beetle", colors=(TEAL, GOLD),
                          top=2.80, bottom=-2.55, size=34)
        kitten = cat(1.51).move_to(xy(-5.01, -0.53))
        grown = cat(2.39).move_to(xy(-1.67, -0.22))
        left_arrow = arrow(xy(-4.19,-0.34), xy(-3.10,-0.34), TEAL)
        worm = larva(1.67, motion=True).move_to(xy(1.41, -0.29))
        adult = beetle(1.64).move_to(xy(4.80, -0.33))
        right_arrow = arrow(xy(2.42,-0.34), xy(3.78,-0.34))
        unknown = label("?", 3.10, 0.32, GOLD, 43)
        self.add(base, panels, kitten, worm)
        self.at("looks like a")
        self.play(Create(left_arrow), FadeIn(grown, shift=UP*0.18), run_time=0.92)
        self.at("a mealworm changes")
        self.play(Create(right_arrow), FadeIn(unknown), run_time=0.62)
        self.play(FadeIn(adult, shift=UP*0.25), run_time=0.65)
        self.at("at each visit")
        self.play(FadeOut(VGroup(panels, kitten, grown, left_arrow, worm, adult, right_arrow, unknown)),
                  run_time=0.37)
        tank = tub(0, -0.15, 9.6, worms=3, closed=True, motion=True)
        self.play(FadeIn(tank, shift=UP*0.18), run_time=0.45)
        count = chip("Count", TEAL, 32).move_to(xy(-4.16,-2.91))
        record = chip("Record", GREEN, 32).move_to(xy(0,-2.91))
        check = chip("Wait and check", GOLD, 32).move_to(xy(4.15,-2.91))
        self.at("child counts")
        self.play(FadeIn(count), run_time=0.31)
        self.at("and records what")
        self.play(FadeIn(record), run_time=0.36)
        self.at("over time")
        self.play(FadeIn(check), run_time=0.48)
        self.finish()


class S04Gather(SpokenScene):
    def construct(self):
        tank = tub(0, -0.45, 5.75, filled=False, closed=True)
        worms = positioned(carton(), 0, 0.44, 4.72)
        oats = positioned(grain_bag(), 4.59, 1.39, 2.03)
        root = positioned(carrot(), 4.53, -1.32, 2.50)
        ladle = spoon(2.10).rotate(-0.32).move_to(xy(-4.59, -1.26))
        paintbrush = brush(2.36).rotate(0.22).move_to(xy(0, 2.23))
        self.add(floor(), worms)
        self.at("you need 10")
        amount = label("10–20 ordinary mealworms", 0, -2.08, CREAM, 38)
        self.play(FadeIn(amount), worms.animate.rotate(-0.12), run_time=0.61)
        self.at("from a bait")
        self.play(worms.animate.rotate(0.26), run_time=1.35)
        self.at("not giant ones")
        self.play(worms.animate.rotate(-0.14), run_time=0.80)
        self.play(FadeOut(amount),
                  worms.animate.scale_to_fit_width(2.22).move_to(xy(-4.55, 1.67)),
                  run_time=0.85)
        self.at("clear plastic tub", lead=0.65)
        self.play(FadeIn(tank, shift=UP*0.3),
                  FadeIn(label("Ordinary\nmealworms", -4.64, 0.33, CREAM, 29)), run_time=0.56)
        self.play(FadeIn(label("Clear tub + lid", 0, -2.02)), run_time=0.53)
        self.at("rolled oats", lead=0.45)
        self.play(FadeIn(oats, shift=UP*0.18), run_time=0.47)
        self.play(FadeIn(label("Oats or bran", 4.59, 0.00)), run_time=0.39)
        self.at("and a carrot", lead=0.45)
        self.play(FadeIn(root, shift=LEFT*0.22), FadeIn(ladle), FadeIn(paintbrush),
                  run_time=0.45)
        self.play(FadeIn(label("Plastic spoon", -4.59, -2.34)),
                  FadeIn(label("Soft paintbrush", 0, 1.61)),
                  FadeIn(label("Carrot or potato", 4.53, -2.34)), run_time=0.38)
        self.finish()


class S14SafetyRules(SpokenScene):
    def construct(self):
        worktop = floor()
        tank = tub(1.65, -0.14, 7.75, worms=3, motion=True)
        lid_top = tub(1.65, -0.14, 7.75, closed=True).cover
        lid_top.shift(UP*1.25)
        adult = person(2.65).move_to(xy(-4.57, 0.23))
        kid = person(1.76, child=True).move_to(xy(-2.92, -0.74))
        self.add(worktop, adult, kid, tank, lid_top)
        self.at("stay with your")
        self.play(adult.animate.shift(RIGHT*0.19), kid.animate.shift(RIGHT*0.19), run_time=1.15)
        stay = label("Adult stays close", -4.25, 2.79, CREAM, 30)
        self.play(FadeIn(stay), run_time=0.49)
        self.at("keep the lid")
        self.play(lid_top.animate.shift(DOWN*1.25), FadeOut(stay), run_time=0.93)
        self.at("keep insects bedding")
        self.play(FadeOut(VGroup(adult, kid, worktop)), run_time=0.32)
        storage = shelf()
        self.play(FadeIn(storage, shift=UP*0.20),
                  VGroup(tank, lid_top).animate.shift(LEFT*1.65+UP*0.15), run_time=0.79)
        warning = chip("Under 4: choking risk", RED, 34).move_to(xy(0, 2.69))
        self.at("away from children")
        self.play(FadeIn(warning), run_time=0.48)
        self.at("call 911 if")
        self.play(FadeOut(warning), run_time=0.25)
        closed_tank = VGroup(tank, lid_top)
        seat = storage[1].get_top()[1] - closed_tank.get_bottom()[1]
        self.play(closed_tank.animate.scale(0.71, about_edge=DOWN).shift(LEFT*2.36+UP*seat),
                  run_time=0.48)
        mobile = phone().move_to(xy(3.74, 0.01))
        help_text = label("Choking? Call 911", 3.07, 2.50, CREAM, 33)
        self.play(FadeIn(mobile, shift=UP*0.25), run_time=0.44)
        self.play(FadeIn(help_text), run_time=0.40)
        self.at("keep everything out")
        self.play(FadeOut(VGroup(mobile, help_text)), run_time=0.45)
        mouth = chip("Keep out of mouths", RED, 32).move_to(xy(3.30, 0.62))
        self.play(FadeIn(mouth), run_time=0.30)
        self.at("wash hands with")
        self.play(FadeOut(mouth), run_time=0.30)
        hands = VGroup(hand().rotate(-0.66).move_to(xy(2.52, -0.28)),
                       hand().flip().rotate(0.66).move_to(xy(3.82, -0.22)))
        lather = VGroup(*[
            oval(s, s, GLASS, CREAM, 0.75).move_to(xy(3.15+x, y))
            for x,y,s in [(-0.36,0.3,0.43),(0.23,0.52,0.37),(-0.13,0.76,0.52),
                          (0.46,0.31,0.47),(0.24,1.03,0.25),(-0.55,0.62,0.20)]
        ])
        self.play(FadeIn(hands), LaggedStart(*[GrowFromCenter(b) for b in lather], lag_ratio=0.16),
                  run_time=1.26)
        self.play(FadeIn(label("Wash with soap", 3.18, 1.68)), run_time=0.38)
        self.finish()


class S13SafetyAllergy(SpokenScene):
    def construct(self):
        tank = tub(-2.02, -0.35, 7.10, worms=3, closed=True, motion=True)
        clinician = person(2.35).move_to(xy(3.40, 0.22))
        doctor = chip("Ask their doctor first", RED, 33).move_to(xy(3.36, -2.49))
        self.add(floor(), tank)
        self.at("your child has")
        self.play(FadeIn(clinician, shift=UP*0.25), run_time=0.84)
        medical = VGroup(rect(0.16,0.48,CREAM,r=0.06), rect(0.48,0.16,CREAM,r=0.06))
        medical.move_to(xy(3.08,-0.64))
        self.play(GrowFromCenter(medical), run_time=0.50)
        self.at("ask their doctor")
        self.play(FadeIn(doctor), run_time=0.52)
        self.at("for wheat allergy")
        self.play(FadeOut(VGroup(clinician, medical, doctor)), run_time=0.43)
        oats = positioned(grain_bag(), 2.55, 0.49, 1.52)
        bran = positioned(grain_bag("#875445"), 4.85, 0.49, 1.52)
        self.play(FadeIn(oats, shift=UP*0.22), FadeIn(bran, shift=UP*0.22), run_time=0.52)
        oat_text = label("Oats", 2.55, -0.77)
        bran_text = label("Bran", 4.85, -0.77)
        self.play(FadeIn(oat_text), FadeIn(bran_text), run_time=0.34)
        self.at("use only bedding")
        approved = chip("Allergist-approved bedding", RED, 30).move_to(xy(3.40, -2.49))
        self.play(FadeIn(approved), run_time=0.57)
        self.at("skip if in doubt")
        skip = chip("Skip if in doubt", RED, 33).move_to(approved)
        self.play(swap(approved, skip, run_time=0.64))
        self.at("open the tub")
        self.play(FadeOut(VGroup(oats, bran, oat_text, bran_text, skip)), run_time=0.37)
        adult = person(2.55).move_to(xy(3.85,0.26))
        cover = tank.cover
        grip = hand().rotate(-1.35).scale(0.47).move_to(cover.get_left()+LEFT*0.36+UP*0.12)
        self.play(FadeIn(adult), FadeIn(grip), run_time=0.43)
        lift = UP*0.97+RIGHT*0.25
        pivot = cover.get_center()
        self.play(cover.animate.rotate(-0.13, about_point=pivot).shift(lift),
                  grip.animate.rotate(-0.13, about_point=pivot).shift(lift), run_time=0.77)
        away = label("Open away from faces", -2.02, -2.29)
        self.play(FadeIn(away), run_time=0.37)
        self.at("if breathing is")
        self.play(FadeOut(VGroup(adult, grip, away)), run_time=0.30)
        mobile = phone().move_to(xy(3.95,0.03))
        self.play(FadeIn(mobile, shift=UP*0.20), run_time=0.48)
        self.at("call 911")
        self.play(FadeIn(label("Breathing hard?\nCall 911", 3.95, -2.66, CREAM, 33)),
                  run_time=0.65)
        self.finish()


class S05Setup(SpokenScene):
    def construct(self):
        top = positioned(lid(holes=False), -1.22, -0.42, 8.65).stretch(1.58, 1)
        vents = VGroup(*[
            oval(0.124, 0.070, BG).move_to(xy(-4.19 + i*0.83, y))
            for y in (-0.77, -0.19) for i in range(8)
        ])
        skewer = Line(xy(1.58, -0.20), xy(3.44, 1.84), color=PAPER, stroke_width=6)
        grip = hand().rotate(0.91).scale(0.82).move_to(xy(3.64, 1.51))
        tool = VGroup(skewer, grip)
        self.add(floor(), top, tool)
        self.at("with the lid flat")
        self.play(tool.animate.shift(LEFT*3.20+UP*0.07), run_time=0.63)
        self.at("poke 10 to 20")
        self.play(tool.animate.shift(DOWN*0.28), run_time=0.32)
        self.play(LaggedStart(*[GrowFromCenter(v) for v in vents], lag_ratio=0.085),
                  tool.animate.shift(RIGHT*3.42+UP*0.35), run_time=1.28)
        self.play(FadeIn(label("10–20 air holes", -1.21, 1.36)), run_time=0.41)
        holes = self.mobjects[-1]
        self.at("add oats")
        self.play(FadeOut(VGroup(top, vents, tool, holes)), run_time=0.36)
        tank = tub(-0.76, -0.35, 9.70, filled=False)
        content = tub(-0.76, -0.35, 9.70, carrots=2)
        soil, slices, _ = content.parts
        self.add(tank)
        self.play(GrowFromEdge(soil, DOWN), run_time=0.84)
        bracket = VGroup(
            Line(xy(4.37,-0.84), xy(4.37,-2.13), color=GOLD, stroke_width=4),
            *[Line(xy(4.37,y), xy(4.66,y), color=GOLD, stroke_width=4)
              for y in (-0.84,-2.13)],
        )
        self.at("centimeters deep")
        self.play(Create(bracket), FadeIn(label("3 to 5 cm", 5.40, -1.48, CREAM, 29)),
                  run_time=0.56)
        depth = self.mobjects[-1]
        self.at("cut two thin")
        left, right = slices
        left_start = positioned(slice_carrot(), -3.41, 1.94, 2.59)
        right_start = positioned(slice_carrot(), -0.17, 1.56, 2.21)
        self.play(FadeIn(left_start, shift=LEFT*0.46), FadeIn(right_start, shift=LEFT*0.46),
                  run_time=0.77)
        self.at("lay them on top")
        self.play(Transform(left_start,left), Transform(right_start,right), run_time=1.06)
        self.at("they provide water")
        droplet = polygon([(0,0.62), (0.38,0.02), (0.41,-0.25), (0.23,-0.47),
                           (-0.23,-0.47), (-0.41,-0.25), (-0.38,0.02)], BLUE, GLASS)
        droplet.move_to(xy(1.98,0.51))
        self.play(GrowFromCenter(droplet), FadeOut(VGroup(bracket, depth)), run_time=0.55)
        self.finish()


class S06Meet(SpokenScene):
    def construct(self):
        plate = VGroup(oval(8.31,4.69,"#BFA57D",PAPER),
                       oval(6.91,3.67,PAPER,CREAM)).move_to(xy(-1.54,-0.18))
        cup = carton().scale(0.68).rotate(-0.36).move_to(xy(-4.23, 2.18))
        subject = larva(4.82, phase=0.45, motion=True).move_to(xy(-1.76, 0.01))
        small = larva(2.38, angle=0.14, motion=True).move_to(xy(-2.12,-1.25))
        self.add(floor(), plate, cup)
        self.at("tip the mealworms")
        self.play(cup.animate.rotate(-0.66), FadeIn(subject, shift=DOWN*0.43),
                  FadeIn(small, shift=DOWN*0.43), run_time=1.12)
        self.play(FadeOut(cup), run_time=0.51)
        ring = Circle(radius=1.40, color=GLASS, stroke_width=9).move_to(xy(-0.43, 0.07))
        grip = rect(0.28,1.14,TEAL,GLASS,r=0.12).rotate(0.75).move_to(xy(1.0,-1.37))
        lens = VGroup(grip, ring)
        self.at("use a hand lens")
        self.play(FadeIn(lens, shift=RIGHT*0.34), run_time=0.71)
        self.at("count legs together")
        subject.clear_updaters()
        # The light at each bend traces one of the three pairs without hiding it.
        marks = VGroup(*[
            Circle(radius=0.11, color=RED, stroke_width=4).move_to(f.get_end())
            for f in subject[0]
        ])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.23), run_time=1.26)
        self.at("what do you think")
        self.play(FadeOut(VGroup(lens, marks)), run_time=0.36)
        book = notebook(4.19, 0.00)
        pen = pencil().move_to(xy(4.74,-0.02))
        self.play(FadeIn(book, shift=LEFT*0.27), run_time=0.66)
        self.at("record the guess")
        self.play(FadeIn(pen), pen.animate.shift(LEFT*0.83), run_time=0.69)
        ink = path([(3.53,-0.18),(3.66,-0.07),(3.73,-0.22),(3.89,-0.10),(4.14,-0.16)], INK, 3)
        self.play(Create(ink), pen.animate.shift(RIGHT*0.69), run_time=0.50)
        self.at("measure two or three")
        ruler = metric_ruler(-1.80, -2.88, span=5.75)
        self.play(FadeIn(ruler, shift=UP*0.29), run_time=0.54)
        self.play(subject.animate.move_to(xy(-2.20,-1.75)),
                  small.animate.move_to(xy(-2.75, 0.63)), run_time=0.75)
        self.at("then spoon all")
        self.play(FadeOut(VGroup(plate, book, pen, ink, ruler)), run_time=0.31)
        tank = tub(1.69,-0.24,7.52)
        ladle = spoon(3.55).flip(UP).move_to(xy(-4.20, 2.15))
        bowl = ladle[2].get_center()
        subject.set_z_index(2)
        small.set_z_index(2)
        self.play(FadeIn(tank), FadeIn(ladle),
                  subject.animate.scale(0.29).move_to(bowl+UP*0.12),
                  small.animate.scale(0.39).move_to(bowl+DOWN*0.10), run_time=0.54)
        reach = RIGHT*4.22
        self.play(VGroup(ladle, subject, small).animate.shift(reach), run_time=0.51)
        self.play(ladle.animate.rotate(-0.52, about_point=bowl+reach).shift(DOWN*0.80),
                  VGroup(subject, small).animate.shift(DOWN*0.80), run_time=0.49)
        self.play(subject.animate.move_to(xy(0.18,-0.96)),
                  small.animate.move_to(xy(-0.61,-1.17)),
                  FadeOut(ladle,shift=UP*0.65), run_time=0.54)
        self.finish()


def window():
    frame = rect(3.20, 2.63,"#394A55",GLASS,r=0.19)
    pane = rect(2.84,2.24,"#2E505E","#78B2B8",r=0.11)
    sun = Circle(radius=0.43, fill_color=GOLD, fill_opacity=1, stroke_width=0).move_to(xy(-0.68,0.35))
    bars = VGroup(Line(UP*1.05,DOWN*1.05,color=GLASS,stroke_width=4),
                  Line(LEFT*1.35,RIGHT*1.35,color=GLASS,stroke_width=4))
    return VGroup(frame,pane,sun,bars)


def week_strip():
    base = rect(8.48,1.09,"#29474A",GLASS,r=0.20)
    boxes = VGroup(*[
        rect(0.83,0.70,"#3E6261","#517E7F",r=0.13).move_to(xy(i*1.13,0))
        for i in range(-3,4)
    ])
    out = VGroup(base,boxes).move_to(xy(0.85,2.58))
    out.days = boxes
    return out


def tally():
    picture = VGroup(larva(1.06), pupa(0.82), beetle(0.70))
    marks = VGroup()
    marks.dashes = []
    for i, (icon, count) in enumerate(zip(picture, (4,2,1))):
        x = -0.68+i*2.40
        icon.move_to(xy(x,2.66))
        row = VGroup(*[
            Line(xy(x+(j-(count-1)/2)*0.19,1.96),
                 xy(x+(j-(count-1)/2)*0.19+0.04,2.18), color=GOLD,stroke_width=3)
            for j in range(count)
        ])
        marks.dashes.append(row)
        marks.add(row)
    return picture, marks


class S07Visits(SpokenScene):
    def construct(self):
        tank = tub(0.86,-0.34,8.65,worms=3,closed=True,motion=True)
        light = window().scale(0.90).move_to(xy(-4.85,1.36))
        self.add(shelf(), light, tank)
        self.at("keep the tub at")
        self.play(tank.animate.shift(RIGHT*0.43), run_time=0.92)
        temp = label("Room temperature", -4.84,-0.45, CREAM, 29)
        self.play(FadeIn(temp), run_time=0.47)
        self.at("out of direct sun")
        self.play(light[2].animate.shift(LEFT*0.29+UP*0.23), run_time=1.10)
        self.at("visit two or three")
        self.play(FadeOut(VGroup(light,temp)), run_time=0.32)
        calendar = week_strip()
        self.play(FadeIn(calendar, shift=DOWN*0.25), run_time=0.51)
        checks = VGroup(*[
            path([(x-0.24,2.53),(x-0.08,2.40),(x+0.22,2.76)], GREEN,5)
            for x in (calendar.days[j].get_x() for j in (0,3,5))
        ])
        self.play(LaggedStart(*[Create(m) for m in checks],lag_ratio=0.45),run_time=1.19)
        self.at("look for shed skins")
        skin = larva(2.25,shed=True,angle=-0.22).move_to(xy(-0.54,-1.41))
        self.play(FadeIn(skin,shift=RIGHT*0.36),run_time=0.59)
        glint = Line(xy(-1.38,-1.15), xy(0.12,-1.54),color=CREAM,stroke_width=3)
        self.play(ShowPassingFlash(glint,time_width=0.52),run_time=0.89)
        self.at("count and record")
        self.play(FadeOut(VGroup(calendar,checks)),run_time=0.29)
        icons, marks = tally()
        self.play(FadeIn(icons),run_time=0.47)
        self.play(LaggedStart(*[Create(row) for row in marks.dashes],lag_ratio=0.37),run_time=1.02)
        self.at("replace the carrot")
        self.play(FadeOut(VGroup(icons,marks)),tank.cover.animate.shift(UP*0.72),
                  run_time=0.46)
        old = tank.parts[1][0]
        fresh = old.copy().shift(LEFT*2.32+UP*1.24)
        self.play(FadeOut(old,shift=UP*1.30),run_time=0.53)
        tank.insects.set_z_index(2)
        self.add(fresh)
        self.play(fresh.animate.shift(RIGHT*2.32+DOWN*1.24),run_time=0.80)
        self.play(tank.cover.animate.shift(DOWN*0.72),run_time=0.50)
        self.finish()


class S08Pupa(SpokenScene):
    def construct(self):
        table = floor()
        soil = bedding(8.4).move_to(xy(-0.99,-0.97)).set_z_index(-2)
        insect = larva(4.73,motion=True).move_to(xy(-0.83,0.28))
        skin = larva(4.73,shed=True).move_to(xy(-0.83,0.28)).set_z_index(-1)
        self.add(table,soil,insect)
        self.at("the first pupae")
        tag = scope_tag("Schematic time lapse",size=28,color=CREAM)
        self.play(FadeIn(tag),run_time=0.44)
        self.at("often appear within")
        insect.clear_updaters()
        curled = pupa(3.32).move_to(xy(-0.49,0.20))
        self.add(skin)
        self.play(ReplacementTransform(insect,curled),skin.animate.shift(LEFT*2.49+DOWN*0.99),
                  run_time=1.52)
        self.at("a pupa is pale")
        name = label("Pupa", -0.50, 2.10, CREAM, 42)
        self.play(FadeIn(name),run_time=0.55)
        # Widen the view of the curled abdomen and folded legs while the animal remains still.
        self.play(VGroup(curled, soil, skin).animate.scale(1.10).shift(LEFT*0.33),
                  run_time=1.88)
        self.at("use a soft brush")
        self.play(FadeOut(VGroup(name,tag)),run_time=0.27)
        pusher = brush(3.48).rotate(-0.24).move_to(xy(1.17,1.15))
        grip = hand().rotate(1.15).scale(0.55).move_to(xy(2.61,1.03))
        self.play(FadeIn(pusher,shift=LEFT*0.35),FadeIn(grip,shift=LEFT*0.35),run_time=0.51)
        self.play(pusher.animate.shift(LEFT*0.55+DOWN*0.57),
                  grip.animate.shift(LEFT*0.55+DOWN*0.57),run_time=0.66)
        self.at("to a small dish")
        self.play(soil.animate.shift(LEFT*0.52),
                  VGroup(curled,pusher,grip).animate.shift(LEFT*1.04),run_time=0.53)
        tray = dish()
        self.play(FadeIn(tray,shift=LEFT*0.17),run_time=0.49)
        self.play(VGroup(curled,pusher,grip).animate.shift(UP*0.66),run_time=0.50)
        self.play(Transform(curled,dish_pupa()),
                  VGroup(pusher,grip).animate.shift(RIGHT*3.64),run_time=0.87)
        self.at("this keeps the other")
        other = larva(2.28,motion=True,angle=0.17).move_to(xy(-3.68,-0.88))
        self.play(FadeOut(VGroup(pusher,grip)),FadeIn(other),run_time=0.50)
        self.play(other.animate.shift(RIGHT*0.42),run_time=1.17)
        self.play(FadeOut(VGroup(other,skin,soil)),run_time=0.55)
        self.finish()


class S09PredictQ(SpokenScene):
    def construct(self):
        tray, curled = dish(), dish_pupa()
        self.add(floor(),tray,curled)
        self.at("picture the pale")
        self.play(tray[1].animate.set_fill("#9CB2A1"), run_time=1.75)
        self.at("your child sees")
        self.play(tray[1].animate.set_fill("#6D9D98"), run_time=1.28)
        self.at("wonders what will")
        question = predict_card()
        self.play(FadeIn(question.plate),run_time=0.57)
        self.at("what do you think")
        self.play(FadeIn(question.question,shift=UP*0.11),run_time=0.60)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_POSITION

    def construct(self):
        tray = dish()
        self.add(floor(),tray,dish_pupa(),predict_card())
        self.play(tray[1].animate.set_fill("#BCC0A6"), run_time=self.narration_s,
                  rate_func=there_and_back)


class S11Reveal(SpokenScene):
    def construct(self):
        tray, curled, question = dish(), dish_pupa(), predict_card()
        self.add(floor(),tray,curled,question)
        self.at("after about one")
        self.play(FadeOut(question),run_time=0.32)
        wait_label = label("About 1–3 weeks", -3.66, 0.48, CREAM, 38)
        tag = scope_tag("Schematic time lapse", size=28, color=CREAM)
        self.play(FadeIn(wait_label),FadeIn(tag),run_time=0.49)
        self.at("a pale beetle",lead=0.46)
        shell = pupa(3.20).set_opacity(0.46).move_to(xy(1.67,-0.67))
        adult = beetle(2.39,pale=True).rotate(-0.35).move_to(xy(3.51,0.21))
        self.add(shell)
        self.play(ReplacementTransform(curled,adult),FadeOut(wait_label),run_time=1.26)
        self.at("once it darkens")
        dark = beetle(2.39).rotate(-0.35).move_to(adult)
        self.play(Transform(adult,dark),run_time=1.25)
        self.at("move it back")
        tank = tub(-2.37,-0.42,7.11,worms=3,motion=True)
        self.play(FadeIn(tank,shift=UP*0.25),FadeOut(tag),run_time=0.49)
        ladle = spoon(3.80).move_to(xy(4.42,-0.13))
        adult.set_z_index(2)
        self.play(FadeIn(ladle,shift=LEFT*0.28),adult.animate.scale(0.60),run_time=0.37)
        self.play(VGroup(ladle,adult).animate.shift(LEFT*4.48+UP*0.36),run_time=0.75)
        self.play(FadeOut(ladle,shift=UP*0.40),adult.animate.shift(LEFT*0.81+DOWN*0.88),
                  run_time=0.46)
        self.at("check the first guess")
        self.play(FadeOut(VGroup(tray,shell)),run_time=0.28)
        book = notebook(3.95,0.09)
        previous = path([(3.29,-0.09),(3.42,0.02),(3.49,-0.13),
                         (3.65,-0.01),(3.90,-0.07)], INK,3)
        self.play(FadeIn(book,shift=LEFT*0.29),FadeIn(previous,shift=LEFT*0.29),run_time=0.67)
        self.at("measure the beetle")
        self.play(FadeOut(tank),run_time=0.30)
        ruler = metric_ruler(-2.60,-1.65)
        specimen = beetle(1.92).rotate(PI/2)
        specimen.scale_to_fit_width(1.50*ruler.unit)
        specimen.move_to(xy(ruler.zero+specimen.width/2,-0.10))
        self.play(FadeIn(ruler,shift=UP*0.25),Transform(adult,specimen),run_time=0.72)
        example = label("Example lengths", -2.56, 2.69, CREAM, 31)
        self.play(FadeIn(example),run_time=0.30)
        self.at("compare it with")
        worm = larva(2.50*ruler.unit,legs=False)
        worm.scale_to_fit_width(2.50*ruler.unit)
        worm.move_to(xy(ruler.zero+worm.width/2,1.48))
        self.play(FadeIn(worm,shift=DOWN*0.27),run_time=0.59)
        ledger = Ledger([("Mealworm","2.5 cm",LARVA),("Beetle","1.5 cm",CREAM)],
                        top_left=(2.05,-1.87),row_h=0.58,key_w=2.23,width=4.28,size=29)
        self.play(ledger.reveal(0),run_time=0.43)
        self.play(ledger.reveal(1),run_time=0.41)
        self.finish()


def eggs():
    return VGroup(*[
        oval(0.42,0.57,CREAM,OAT).rotate(a).move_to(xy(x,y))
        for x,y,a in [(-0.37,0.04,-0.34),(0.10,0.30,0.22),(0.36,-0.10,0.36),
                      (-0.10,-0.27,-0.27)]
    ])


def cycle_diagram(*, x=-2.60, y=0.0, scale=1.0, compact=False):
    origin = xy(x,y)
    coords = [xy(0,1.96),xy(2.12,0),xy(0,-1.91),xy(-2.12,0)]
    organisms = [eggs(),larva(2.15,angle=0.16),pupa(1.85),beetle(1.36)]
    names = ["Egg","Larva","Pupa","Beetle" if compact else "Adult beetle"]
    hues = [CREAM,LARVA,CREAM,CREAM]
    nodes = VGroup()
    for coordinate, organism, name, hue in zip(coords,organisms,names,hues):
        center = origin + scale*coordinate
        organism.scale(scale).move_to(center)
        i = len(nodes)
        dx, dy = [(0, 0.90), (0.43, -0.55), (0, -0.95), (-0.72, -1.09)][i]
        if compact and i == 3:
            dx, dy = -0.33, -1.05
        text = label(name, center[0]+dx, center[1]+dy*max(scale,0.80),
                     hue, 28 if compact or i == 3 else 32)
        nodes.add(VGroup(organism,text))
    arrows = VGroup(*[
        CurvedArrow(origin+scale*xy(*a),origin+scale*xy(*b),
                    angle=-0.52,color=GOLD,stroke_width=3.4,tip_length=0.14)
        for a,b in [
            ((0.93,1.92),(2.08,0.77)),((1.81,-0.94),(0.88,-1.77)),
            ((-0.96,-1.86),(-1.63,-0.86)),((-2.14,0.76),(-0.88,1.96))
        ]
    ])
    return nodes, arrows


class S12Cycle(SpokenScene):
    def construct(self):
        table = floor()
        tank = tub(-0.39,-0.52,11.15,worms=1,adults=True,motion=True)
        self.add(table,tank)
        self.at("look for tiny")
        babies = VGroup(*[
            larva(w,angle=angle,motion=True).move_to(xy(x,y))
            for x,y,w,angle in [(-0.77,-1.42,0.78,0.17),(-0.63,-1.77,0.63,-0.23),
                                (2.69,-1.80,0.69,0.28)]
        ])
        self.play(LaggedStart(*[FadeIn(m,shift=RIGHT*0.22) for m in babies],lag_ratio=0.27),
                  run_time=1.45)
        self.at("after a few weeks")
        self.play(babies.animate.shift(RIGHT*0.30),run_time=1.18)
        self.at("draw the four stages")
        self.play(FadeOut(VGroup(tank,babies)),run_time=0.43)
        nodes, arcs = cycle_diagram()
        self.play(GrowFromCenter(nodes[0][0]), run_time=0.48)
        self.at("egg larva",lead=0.34)
        self.play(FadeIn(nodes[0][1]),Create(arcs[0]),run_time=0.38)
        self.play(FadeIn(nodes[1],shift=DOWN*0.18),Create(arcs[1]),run_time=0.43)
        self.at("pupa and adult")
        self.play(FadeIn(nodes[2],shift=LEFT*0.18),Create(arcs[2]),run_time=0.45)
        self.play(FadeIn(nodes[3],shift=UP*0.18),Create(arcs[3]),run_time=0.54)
        self.at("looks like its parent")
        little = cat(1.54).move_to(xy(1.77,0.08))
        grown = cat(2.30).move_to(xy(5.03,0.20))
        self.play(FadeIn(little,shift=UP*0.21),run_time=0.39)
        self.play(Create(arrow(xy(2.69,0.10),xy(3.74,0.10),TEAL)),
                  FadeIn(grown,shift=UP*0.21),run_time=0.85)
        self.at("a kitten or")
        self.play(FadeIn(label("Kitten",1.77,-1.47),shift=UP*0.11),
                  FadeIn(label("Cat",5.03,-1.47),shift=UP*0.11),run_time=0.43)
        self.finish()


def gate():
    fence = VGroup()
    for x in (-1.88,-0.94,0,0.94,1.88):
        fence.add(polygon([(x-0.29,-1.31),(x+0.29,-1.31),(x+0.29,0.89),
                           (x,1.40),(x-0.29,0.89)],OAT,PAPER))
    rails = VGroup(*[rect(4.72,0.23,CORK,SKIN,r=0.07).shift(UP*y) for y in (0.62,-0.75)])
    uprights = VGroup(*[rect(0.39,3.30,CORK,SKIN,r=0.09).shift(RIGHT*x)
                        for x in (-2.51,2.51)])
    return VGroup(fence,rails,uprights)


def chicken():
    tail = VGroup(*[oval(0.87,0.30,c,SKIN).rotate(a).move_to(xy(-0.87,y))
                    for c,a,y in [(CORK,0.51,0.52),(OAT,-0.30,0.30),(CORK,-0.11,0.10)]])
    feet = VGroup(*[path([(x,-0.36),(x,-0.77),(x+0.30,-0.77)],CARROT,4)
                    for x in (-0.30,0.23)])
    body = oval(1.92,1.33,PAPER,OAT)
    wing = oval(1.06,0.66,"#D6B48C",OAT).rotate(0.28).move_to(xy(-0.39,0))
    head = oval(0.66,0.75,CREAM,OAT).move_to(xy(0.73,0.75))
    comb = VGroup(*[oval(0.19,0.35,RED).move_to(xy(0.58+i*0.15,1.14))
                    for i in range(3)])
    beak = polygon([(0.98,0.88),(1.28,0.76),(0.98,0.67)],CARROT,CORK)
    eye = oval(0.10,0.13,INK).move_to(xy(0.86,0.86))
    return VGroup(feet,tail,body,wing,comb,head,beak,eye)


def fridge():
    cabinet = rect(2.95,4.79,"#476371",GLASS,r=0.26)
    upper = rect(2.68,1.41,"#698A91",GLASS,r=0.17).shift(UP*1.53)
    lower = rect(2.68,2.90,"#4D767E",GLASS,r=0.17).shift(DOWN*0.68)
    grips = VGroup(*[rect(0.16,h,GLASS,r=0.07).move_to(xy(-0.94,y))
                     for y,h in [(1.53,0.68),(-0.28,1.25)]])
    unit = VGroup(cabinet,VGroup(upper,grips[0]),VGroup(lower,grips[1]))
    unit.freezer, unit.fridge = unit[1], unit[2]
    return unit


def freezer_bag():
    bag = polygon([(-1.43,1.02),(1.43,1.02),(1.26,-1.09),(-1.26,-1.09)],
                  "#427481",GLASS)
    seal = Line(xy(-1.39,0.83),xy(1.39,0.83),color=GLASS,stroke_width=5)
    bug = beetle(0.78).rotate(-0.45).move_to(xy(0,-0.13))
    return VGroup(bag,seal,bug)


class S15EndProject(SpokenScene):
    def construct(self):
        self.add(floor())
        tank = tub(-1.80,-0.40,7.42,worms=2,closed=True,adults=True,motion=True)
        plan = notebook(3.70,0.15,heading="End of project")
        self.add(tank,plan)
        self.at("make a plan")
        pen = pencil().move_to(xy(4.36,0.22))
        self.play(FadeIn(pen,shift=LEFT*0.30),run_time=0.48)
        self.play(pen.animate.shift(LEFT*0.78+DOWN*0.24),run_time=0.91)
        self.at("never release the")
        self.play(FadeOut(VGroup(tank,plan,pen)),run_time=0.35)
        fence = gate().move_to(xy(0,0.0))
        bug = beetle(1.82).move_to(xy(0,0.05))
        stop = VGroup(Circle(radius=1.39,color=RED,stroke_width=9),
                      Line(xy(-0.94,0.94),xy(0.94,-0.94),color=RED,stroke_width=9))
        self.play(FadeIn(fence),FadeIn(bug,shift=UP*0.39),run_time=0.50)
        self.play(Create(stop),FadeIn(label("Never release",0,-2.71,CREAM,35)),run_time=0.59)
        warning = self.mobjects[-1]
        self.at("offer them to")
        self.play(FadeOut(VGroup(fence,bug,stop,warning)),run_time=0.32)
        handoff = tub(-2.04,-0.18,4.91,worms=2,closed=True,adults=True)
        giver = hand().rotate(-0.93).move_to(xy(-4.28,-0.91))
        receiver = hand().flip().rotate(0.95).move_to(xy(2.22,-0.91))
        hen = chicken().scale(0.82).move_to(xy(4.70,0.48))
        self.play(FadeIn(giver),FadeIn(handoff),FadeIn(receiver),FadeIn(hen),run_time=0.52)
        home = label("Offer to an animal keeper",0,-2.67,CREAM,33)
        self.play(handoff.animate.shift(RIGHT*2.38),receiver.animate.shift(LEFT*0.31),
                  giver.animate.shift(RIGHT*0.63),
                  FadeIn(home,rate_func=squish_rate_func(smooth,0,0.36)),run_time=1.03)
        self.at("if nobody takes")
        self.play(FadeOut(VGroup(hen,receiver,giver,home)),
                  handoff.animate.shift(LEFT*1.02),run_time=0.54)
        appliance = fridge().move_to(xy(3.53,0.10))
        self.play(FadeIn(appliance,shift=UP*0.25),
                  handoff.animate.scale(0.67).shift(LEFT*1.98+DOWN*0.49),run_time=0.64)
        self.at("an adult chills")
        chill = label("Fridge · a few hours", -2.66, 1.62, CREAM, 32)
        self.play(FadeIn(chill),run_time=0.49)
        self.at("in the fridge")
        door = appliance.fridge
        door.save_state()
        self.play(door.animate.stretch(0.23,0,about_point=door.get_right()),
                  run_time=0.43)
        self.play(handoff.animate.shift(RIGHT*5.95+UP*0.22).scale(0.57),
                  run_time=0.92)
        self.play(FadeOut(handoff),Restore(door),run_time=0.48)
        self.at("the adult freezes")
        upper = appliance.freezer
        upper.save_state()
        self.play(FadeOut(chill),upper.animate.stretch(0.23,0,about_point=upper.get_right()),
                  run_time=0.38)
        bag = freezer_bag().move_to(xy(-2.90,0.24))
        self.play(FadeIn(bag,shift=UP*0.35),run_time=0.65)
        freeze = label("Freezer · at least 3 days", -2.90, -2.35, CREAM, 32)
        self.play(FadeIn(freeze),run_time=0.44)
        self.at("for at least three")
        self.play(bag.animate.scale(0.53).move_to(xy(3.65,1.62)),run_time=0.90)
        self.at("before disposal")
        self.play(FadeOut(bag),Restore(upper),run_time=0.40)
        self.finish()


class S16Return(SpokenScene):
    def construct(self):
        table = shelf()
        tank = tub(-2.41,-0.38,7.07,worms=1,closed=True,adults=True,motion=True)
        board = rect(4.80,4.30,"#343031",OAT,r=0.21).move_to(xy(3.68,0.38))
        stages, arcs = cycle_diagram(x=3.68,y=0.43,scale=0.53,compact=True)
        cycle = VGroup(board,arcs,stages)
        book = notebook(-4.32,2.62,width=2.86)
        self.add(table,tank,cycle)
        self.at("look back at")
        self.play(FadeIn(book),run_time=0.67)
        notes = path([(-4.90,2.59),(-4.68,2.66),(-4.52,2.52),(-4.34,2.61),
                      (-4.11,2.55)],INK,3)
        self.play(Create(notes),run_time=0.45)
        self.at("what changed before")
        glimmer = arcs[2].copy().set_color(CREAM).set_stroke(width=8)
        self.play(ShowPassingFlash(glimmer,time_width=0.70),
                  board.animate.set_fill("#635048"),run_time=1.75)
        self.at("your child can point")
        finger = polygon([(-0.41,-0.62),(0.23,-0.58),(0.39,-0.25),(0.25,0.03),
                          (-0.10,0.07),(0.17,0.61),(0.06,0.73),(-0.10,0.65),
                          (-0.55,-0.08),(-0.54,-0.41)], CHILD_SKIN, CORK)
        finger.rotate(-0.85).move_to(xy(0.22,-2.06))
        self.play(FadeIn(finger,shift=RIGHT*0.25+UP*0.30), run_time=0.64)
        self.play(finger.animate.shift(UP*0.53+RIGHT*0.26),run_time=0.70)
        self.finish()


class S17End(EndCard):
    LINE = "A mealworm becomes a pupa, then an adult beetle."
