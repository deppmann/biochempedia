"""A Watershed in a Pan, a parent guide drawn as paper and ink.

Color map from the earlier film: blue is water, tan is high ground, green is
watershed land, orange is material water can carry, and gray is the built world.
The terrain is schematic. Its facets, creases and runoff all share one mesh.
"""
from bp_parts import *
from bp_style import EndCard


TAN = "#C9A27A"
ORANGE = "#F29E4C"
LAND = "#8B93A1"
INK = "#283342"
PAPER = "#F2EEE6"
STEEL = "#657385"
DARK_BLUE = "#1784AF"
DARK_GREEN = "#357B58"
PURPLE = "#8068B0"
LESSON_TITLE = "A Watershed in a Pan"
FILM_TITLE = "A Watershed in a Pan: Parent Guide"


def pt(x, y):
    return np.array([x, y, 0.0])


def shape(points, fill, edge=None, width=2, opacity=1):
    return Polygon(*points, fill_color=fill, fill_opacity=opacity,
                   stroke_color=edge or fill, stroke_width=width if edge else 0)


def linework(points, color, width=4):
    path = VMobject().set_points_as_corners(points)
    path.set_stroke(color, width).set_fill(opacity=0)
    path.set_cap_style(CapStyleType.ROUND)
    return path


def slab(w, h, color, x=0, y=0, radius=0.09, edge=None):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            fill_color=color, fill_opacity=1, stroke_color=edge or color,
                            stroke_width=2 if edge else 0).move_to(pt(x, y))


def oval(w, h, color, x=0, y=0):
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=color,
                   fill_opacity=1).move_to(pt(x, y))


def arrow(start, end, color=INK):
    return Arrow(start, end, buff=0.06, color=color, stroke_width=4,
                 tip_length=0.19, max_tip_length_to_length_ratio=0.32)


def dropshape(color=BLUE):
    points = [pt(0, .27), pt(-.14, .02), pt(-.13, -.12), pt(0, -.19),
              pt(.13, -.12), pt(.14, .02)]
    return VMobject(fill_color=color, fill_opacity=1, stroke_width=0).set_points_smoothly(
        [*points, points[0]])


def label(words, x, y, color=TEXT, size=32):
    return T(words, size, color, weight=BOLD).move_to(pt(x, y))


def heading(words, y=3.13, x=0, size=46):
    return T(words, size, TEXT, font=TITLE_FONT).move_to(pt(x, y))


def stream_marks(path, count=5, rate=.22, color=BLUE, size=.10):
    """Moving glints follow an existing drawn flow path."""
    marks = VGroup()
    for i in range(count):
        mark = oval(size * 4, size, color)

        def drift(mob, dt, phase=[i / count]):
            phase[0] = (phase[0] + dt * rate) % 1
            p = phase[0]
            here = path.point_from_proportion(p)
            ahead = path.point_from_proportion(min(1, p + .006))
            delta = ahead - here
            angle = np.arctan2(delta[1], delta[0])
            mob.rotate(angle - getattr(mob, "flow_angle", 0))
            mob.flow_angle = angle
            mob.move_to(here)
            mob.set_opacity(min(1, p * 14, (1 - p) * 14))

        mark.add_updater(drift, call_updater=True)
        marks.add(mark)
    return marks


# The paper tray is drawn in shallow perspective. Column 3 is the main divide.
HEIGHTS = np.array([
    [.20, .48, .73, 1.35, .82, .55, .27],
    [.56, .73, .45, 2.05, .54, .78, .36],
    [.47, .60, .15, 1.65, .36, .54, .21],
    [.30, .32, -.13, .92, .16, .21, .01],
    [.20, .10, .02, .52, .05, -.03, -.17],
])
FACES = ("#F6F1E8", "#DFDAD1", "#F0EBE3", "#D1D0CD", "#E7E3DC",
         "#C1C4C7", "#D9DBDB", "#F3EFE6")


def vertex(u, v, lift=1, tilt=0):
    return pt((u - 3) * 1.56 + (v - 2) * .24,
              1.06 - .84 * v + HEIGHTS[v, u] * .91 * lift + tilt * (3 - u) * .095)


def surface(u, v, tilt=1):
    """Interpolate coordinates on the same two triangles used to fold each cell."""
    i, j = min(int(u), 5), min(int(v), 3)
    a, b = u - i, v - j
    p, q, r, s = (vertex(i, j, tilt=tilt), vertex(i+1, j, tilt=tilt),
                  vertex(i+1, j+1, tilt=tilt), vertex(i, j+1, tilt=tilt))
    if b <= a:
        return p + a * (q - p) + b * (r - q)
    return p + a * (r - s) + b * (s - p)


def paper_mesh(lift=1, tilt=0, watersheds=False, flat=False):
    faces = VGroup()
    for v in range(4):
        for u in range(6):
            p, q, r, s = (vertex(u, v, lift, tilt), vertex(u+1, v, lift, tilt),
                          vertex(u+1, v+1, lift, tilt), vertex(u, v+1, lift, tilt))
            for tri, shade in (([p, q, r], (v * 6 + u * 3) % 8),
                               ([p, r, s], (v * 3 + u * 5 + 3) % 8)):
                color = PAPER if flat else FACES[shade]
                if watersheds:
                    tint = GREEN if u >= 3 else "#D2BA83"
                    color = interpolate_color(ManimColor(color), ManimColor(tint), .66)
                faces.add(shape(tri, color, color, width=.8))
    return faces


def tray_parts(tilt=0):
    back_l, back_r = pt(-5.53, 1.90 + .28 * tilt), pt(4.80, 1.90 - .28 * tilt)
    front_l, front_r = pt(-4.85, -2.51 + .28 * tilt), pt(5.51, -2.51 - .28 * tilt)
    lip_l, lip_r = front_l + pt(.18, -.36), front_r + pt(-.12, -.36)
    rim = shape([back_l, back_r, front_r, front_l], STEEL, "#A9B7C5", 2.5)
    bed = shape([back_l + pt(.23, -.20), back_r + pt(-.19, -.20),
                 front_r + pt(-.24, .18), front_l + pt(.19, .18)], "#435166")
    lip = shape([front_l, front_r, lip_r, lip_l], "#8596A9", "#ADBBCA", 2)
    return VGroup(rim, bed, lip)


def towel():
    top = shape([pt(-1.2, .19), pt(-.8, .55), pt(1.15, .55), pt(1.0, .19)], PAPER)
    edge = slab(2.2, .32, "#C3CDD5", -.10, .02)
    seam = linework([pt(-1.04, .02), pt(.80, .02)], "#94A5B5", 2)
    return VGroup(edge, top, seam)


def plate(tilt=0):
    stand = towel().scale(.76).move_to(pt(-3.72, -2.74))
    stand.set_opacity(float(tilt))
    return VGroup(stand, tray_parts(tilt))


def ridges(tilt=0):
    main = linework([vertex(3, v, tilt=tilt) for v in range(5)], TAN, 8)
    other = linework([vertex(u, v, tilt=tilt) for u, v in [(0, 1), (1, 1), (1, 0)]], TAN, 6)
    return VGroup(main, other)


def local_line(coords, color, width):
    return linework([surface(u, v) for u, v in coords], color, width)


def bay(tilt=1):
    corners = [(4.7, 3.9), (5.07, 3.53), (5.48, 3.63), (5.61, 3.34),
               (6, 3.38), (6, 4), (5.15, 4)]
    return shape([surface(u, v, tilt=tilt) for u, v in corners], DARK_BLUE)


def house():
    base = slab(.66, .46, DARK_GREEN, 0, -.13)
    roof = shape([pt(-.43, .06), pt(0, .39), pt(.43, .06)], "#478464")
    door = slab(.13, .24, PAPER, .09, -.22, .025)
    window = slab(.14, .13, "#BCDFA8", -.17, -.1, .02)
    return VGroup(base, roof, door, window)


def town():
    houses = VGroup(house().scale(.78).move_to(surface(1.10, 1.18)),
                    house().scale(.69).move_to(surface(2.12, 2.82)),
                    house().scale(.82).move_to(surface(4.92, 1.11)))
    rear_left, rear_right, front_right, front_left = [
        surface(u, v) for u, v in [(3.7, .64), (4.53, .64), (4.65, 1.35), (3.74, 1.35)]
    ]
    field = shape([rear_left, rear_right, front_right, front_left], "#9CC478")
    rows = VGroup()
    for fraction in np.linspace(.15, .85, 4):
        rear = interpolate(rear_left, rear_right, fraction)
        front = interpolate(front_left, front_right, fraction)
        rows.add(linework([interpolate(rear, front, .14),
                              interpolate(rear, front, .84)], DARK_GREEN, 3))
    farm = VGroup(field, rows)
    road_points = [(0, 2.26), (1, 2.06), (2, 2.10), (2.6, 2.28), (3, 2.18),
                   (3.58, 2.26), (4, 2.38), (5, 2.28), (6, 2.19)]
    road = VGroup(local_line(road_points, STEEL, 12),
                  DashedVMobject(local_line(road_points, PAPER, 2), num_dashes=28))
    return VGroup(houses, farm, road)


def landscape(tilt=1, marked=True, colored=True, built=True, watersheds=False):
    """Return layers in drawing order so a scene can reveal any one independently."""
    layers = VGroup(plate(tilt), paper_mesh(tilt=tilt, watersheds=watersheds))
    if marked:
        layers.add(ridges(tilt))
    if colored:
        layers.add(bay())
    if built:
        layers.add(town())
    return layers


def side_tray(with_paper=True):
    if with_paper:
        tray = landscape(tilt=0, marked=False, colored=False, built=False)
    else:
        tray = plate()
    return tray.scale(.66, about_point=ORIGIN).shift(pt(2.66, -.25))


# Water takes the lower creases on its own side of the main divide. These are
# schematic routes over the paper, with a local pool on the left and bay on the right.
ROUTES = (
    [(2.77, 1.45), (2.42, 1.68), (2.12, 1.92), (2, 2.26), (2, 2.74), (2, 3.21)],
    [(3.23, 1.48), (3.57, 1.75), (4, 2.10), (4.24, 2.49), (4.80, 3.02),
     (5.10, 3.40), (5.57, 3.76)],
    [(5.14, 1.39), (5.08, 1.85), (5.10, 2.37), (5.05, 2.89),
     (5.10, 3.40), (5.57, 3.76)],
)
GUESS_ENDS = [(2.18, 1.52), (3.93, 1.68), (5.78, 1.60)]


def rain_path(index, color=DARK_BLUE, width=8):
    return local_line(ROUTES[index], color, width)


def pencils():
    starts = [surface(*route[0]) for route in ROUTES]
    dots = VGroup(*[Dot(p, radius=.10, color=INK) for p in starts])
    arrows = VGroup(*[arrow(p, surface(*end), INK) for p, end in zip(starts, GUESS_ENDS)])
    return dots, arrows


def local_pool():
    return oval(.88, .22, DARK_BLUE).move_to(surface(2, 3.17))


def wet_details():
    return VGroup(*[rain_path(i) for i in range(3)], local_pool())


def wet_glints(paths):
    return VGroup(*[stream_marks(path, count=3, size=.10, rate=.34) for path in paths])


# Street and paper icons share a cut-paper silhouette style.
def street():
    sidewalk = shape([pt(-6, 1.62), pt(-4.52, 2.30), pt(6.15, -.73),
                      pt(5.98, -1.38)], "#AFB9C4")
    curb = shape([pt(-6, 1.62), pt(5.98, -1.38), pt(5.98, -1.68),
                  pt(-6, 1.38)], "#677685")
    asphalt = shape([pt(-6, 1.38), pt(5.98, -1.68), pt(5.98, -2.90),
                     pt(-6, -2.90)], "#3C4657")
    seam = linework([pt(-5.55, -1.50), pt(3.9, -2.76)], "#77899B", 2)
    puddle = oval(2.65, .46, DARK_BLUE, -4.54, .76).rotate(-.21)
    flow = linework([pt(-4.57, .74), pt(-3.38, .48), pt(-2.18, .13), pt(-.6, -.29),
                     pt(1.1, -.78), pt(2.9, -1.22), pt(4.78, -1.79)], DARK_BLUE, 10)
    drain = VGroup(slab(1.26, .49, "#202936", edge="#8192A6"),
                   *[slab(.075, .31, "#8192A6", x, 0, .018) for x in np.linspace(-.46, .46, 6)])
    drain.rotate(-.25).move_to(pt(4.86, -1.83))
    world = VGroup(asphalt, sidewalk, curb, seam, puddle, flow, drain)
    return world, flow


def sheet():
    return shape([pt(-3.55, -1.05), pt(2.70, -1.34), pt(3.34, 1.43),
                  pt(-2.98, 1.79)], PAPER, "#A9B7C5")


def paper_ball():
    # Keep every facet's vertex correspondence as the sheet is squeezed inward.
    mesh = paper_mesh(lift=.75).move_to(ORIGIN)

    def squeeze(p):
        x, y = p[0] / 5.20, p[1] / 2.42
        return pt(.98 * x * (1 - .26 * y * y), .92 * y * (1 - .27 * x * x))

    return mesh.apply_function(squeeze).rotate(.34).shift(DOWN * .25)


def spray_bottle(color=BLUE):
    bottle = slab(.86, 1.02, color, 0, -.30, .24, "#B5D1DB")
    stripe = slab(.63, .31, "#E4F0F0", 0, -.35, .07)
    neck = slab(.32, .32, "#A4B4C0", -.04, .35)
    handle = slab(.81, .26, "#8497A8", -.24, .62)
    nozzle = slab(.24, .21, "#D4DFE3", -.68, .62, .04)
    trigger = linework([pt(-.39, .50), pt(-.39, .27), pt(-.54, .18)], "#B8C9D5", 7)
    return VGroup(bottle, stripe, neck, handle, nozzle, trigger)


def marker(color):
    return VGroup(slab(1.52, .24, "#E2E8EC"), slab(.47, .28, color, .59),
                  slab(.20, .24, color, -.75, radius=.05))


def pin(color=ORANGE):
    head = Circle(radius=.26, stroke_width=0, fill_color=color, fill_opacity=1)
    tip = shape([pt(-.20, -.10), pt(0, -.54), pt(.20, -.10)], color)
    return VGroup(tip, head, Dot(radius=.086, color=INK))


def eye():
    shell = VMobject(fill_color=PAPER, fill_opacity=1, stroke_width=0)
    shell.set_points_smoothly([pt(-.54, 0), pt(0, .27), pt(.54, 0), pt(0, -.27), pt(-.54, 0)])
    return VGroup(shell, Dot(radius=.16, color=DARK_BLUE), Dot(pt(.04, .05), radius=.055, color=PAPER))


def cocoa_dish():
    mound = shape([pt(-.57, .09), pt(-.35, .30), pt(.01, .40), pt(.37, .29),
                   pt(.58, .08)], "#A86746")
    return VGroup(oval(1.65, .52, "#D5DCE2"), oval(1.42, .30, "#8F9EAC", 0, .07), mound)


def cross(target, scale=1):
    center = target.get_center()
    return VGroup(Line(pt(-.48, -.48), pt(.48, .48)),
                  Line(pt(-.48, .48), pt(.48, -.48))).set_stroke(RED, 8).scale(scale).move_to(center)


def person(shirt, skin="#E8BD9A"):
    head = Dot(pt(0, .68), radius=.34, color=skin)
    torso = slab(.95, .91, shirt, 0, -.04, .26)
    legs = VGroup(slab(.26, .58, "#99A6B6", -.24, -.64),
                  slab(.26, .58, "#99A6B6", .24, -.64))
    return VGroup(legs, torso, head)


def pet(kind):
    head = oval(1.17, .87, "#BE946F" if kind == "dog" else "#9DAFC3")
    if kind == "dog":
        ears = VGroup(oval(.28, .64, "#8F634C", -.52, .10).rotate(-.28),
                      oval(.28, .64, "#8F634C", .52, .10).rotate(.28))
    else:
        ears = VGroup(*[shape([pt(x-.22, .22), pt(x, .66), pt(x+.22, .22)], "#9DAFC3")
                        for x in (-.38, .38)])
    face = VGroup(Dot(pt(-.20, .08), radius=.063, color=INK), Dot(pt(.20, .08), radius=.063, color=INK),
                  oval(.20, .12, INK, 0, -.10))
    return VGroup(ears, head, face)


def trash_bin():
    body = shape([pt(-.48, .28), pt(.48, .28), pt(.36, -.70),
                  pt(-.36, -.70)], "#7393A4")
    slots = VGroup(*[slab(.058, .60, "#ABC6CB", x, -.20, .025) for x in (-.18, 0, .18)])
    lid = VGroup(slab(1.12, .17, "#AFC2CF", 0, .29), slab(.28, .15, "#AFC2CF", 0, .43))
    return VGroup(body, slots, lid)


def tap():
    pipe = linework([pt(-.58, .38), pt(.30, .38), pt(.54, .19), pt(.54, -.07)], "#9AB1C1", 24)
    valve = VGroup(slab(.15, .30, "#B6C6D3", -.24, .63),
                   slab(.65, .12, "#B6C6D3", -.24, .78))
    return VGroup(pipe, valve)


def hand():
    palm = slab(.77, .47, "#E8BD9A", 0, -.13, .20)
    fingers = VGroup(*[slab(.15, length, "#E8BD9A", x, .04 + length / 2, .065)
                      for x, length in zip((-.27, -.09, .09, .27), (.39, .51, .44, .32))])
    thumb = slab(.16, .40, "#E8BD9A", -.39, -.03, .070).rotate(.64)
    return VGroup(palm, fingers, thumb)


def badge(icon, x=-3.52, y=.12):
    pictogram = icon.scale_to_fit_width(3.0).scale_to_fit_height(
        min(2.18, icon.height)).move_to(pt(x, y))
    panel = slab(4.60, 3.12, "#263447", x, y, .28, "#53677F")
    return VGroup(panel, pictogram)


def spray_fan(origin, targets, period=1.10):
    """Short sprays start at a point or a moving point and vanish on contact."""
    source = origin.get_center if isinstance(origin, Mobject) else lambda: origin
    fan = VGroup()
    for i, target in enumerate(targets):
        for j in range(2):
            fleck = oval(.086, .22, BLUE)

            def fall(mob, dt, end=target, age=[0.015 * i + .14 * j]):
                age[0] = (age[0] + dt) % period
                fraction = min(1, age[0] / .42)
                mob.move_to(interpolate(source(), end, fraction))
                mob.set_opacity(0 if fraction >= 1 else min(.94, fraction * 12))

            fleck.add_updater(fall, call_updater=True)
            fan.add(fleck)
    return fan


class S01Hook(SpokenScene, TitleCard):
    LESSON = LESSON_TITLE
    TITLE = FILM_TITLE

    def construct(self):
        world, flow = street()
        question = heading("Where does the rain go?", size=53)
        self.add(world, stream_marks(flow, count=7, size=.235, rate=.19))
        self.at("where does rain go")
        self.play(FadeIn(question, shift=UP * .12), run_time=.55)
        self.at("it runs downhill")
        parcel = oval(1.53, .37, "#9AE0EA").rotate(-.26)
        self.play(MoveAlongPath(parcel, flow), run_time=2.05, rate_func=linear)
        self.remove(parcel)
        self.at("a paper landscape")
        self.play(FadeOut(question), run_time=.40)
        self.finish()


class S02Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = FILM_TITLE

    def construct(self):
        world, _ = street()
        tray = side_tray()
        title = heading(self.LESSON, y=3.00, size=56)
        guide = label("Parent Guide", 0, 2.28, BLUE)
        self.add(world)
        self.play(ReplacementTransform(world, tray), FadeIn(title), run_time=.66)
        self.play(FadeIn(guide), run_time=.26)
        self.wait(.83)
        self.play(FadeOut(title), FadeOut(guide), run_time=.25)


class S03Payoff(SpokenScene):
    def construct(self):
        self.add(side_tray())
        duration = label("About 25 minutes", -2.89, 2.88, BLUE, 33)
        rows = [
            (arrow(pt(-.44, 0), pt(.43, 0), BLUE), "Guess, then check", 1.64),
            (eye(), "Look closely", .21),
            (pin(), "Our watershed", -1.24),
        ]
        self.at("it takes about")
        self.play(FadeIn(duration, shift=UP * .12), run_time=.55)
        for cue, (icon, words, y) in zip(("practices guessing", "and checking", "a watershed map"), rows):
            icon.move_to(pt(-5.34, y))
            text = label(words, 0, y, size=34).align_to(pt(-4.48, y), LEFT)
            self.at(cue, lead=.45)
            self.play(FadeIn(icon, shift=RIGHT * .25), run_time=.43)
            self.play(FadeIn(text), run_time=.36)
            bob(icon, amp=.10, speed=2.1)
        self.at("also trace")
        self.play(FadeOut(duration), run_time=.45)
        self.finish()


class S04Gather(SpokenScene):
    def construct(self):
        tray = side_tray(with_paper=False)
        start_tray = side_tray()
        self.add(start_tray)
        page = sheet().scale(.32).move_to(pt(-4.64, .99))
        markers = VGroup(*[marker(c) for c in (BLUE, TAN, GREEN, PURPLE)]).arrange(DOWN, buff=.18)
        markers.rotate(-.19).move_to(pt(-2.35, .85))
        towels = VGroup(towel(), towel().shift(pt(.05, .24))).move_to(pt(-4.53, -1.16))
        cocoa = cocoa_dish().move_to(pt(-2.14, -1.2))
        supply = VGroup(page, markers, towels, cocoa)
        self.at("gather white")
        self.play(ReplacementTransform(start_tray, tray), FadeIn(page, shift=RIGHT * .60), run_time=.80)
        self.at("washable markers")
        self.play(FadeIn(markers, shift=UP * .44), run_time=.77)
        self.at("paper towels")
        self.play(FadeIn(towels, shift=RIGHT * .40), run_time=.69)
        self.at("a shallow metal tray")
        pan_name = caption("Shallow tray or tub", 30, y=-3.10).set_x(2.66)
        self.play(FadeIn(pan_name), run_time=.45)
        self.play(FadeIn(cocoa, shift=UP * .25), run_time=.56)

        self.at("use plain water", lead=.78)
        self.play(FadeOut(supply), FadeOut(pan_name), run_time=.42)
        clean = spray_bottle().scale(1.23).move_to(pt(-4.87, .73))
        old = spray_bottle("#88998C").scale(1.14).move_to(pt(-1.88, .73))
        water_only = label("Plain water only", -4.87, -.76, BLUE, 28)
        old_name = label("Old cleaner", -1.95, -.76, RED, 28)
        self.play(FadeIn(clean, shift=UP * .35), run_time=.47)
        self.play(FadeIn(water_only), run_time=.45)
        self.at("one that has only")
        old_cross = cross(old, 1.36)
        self.play(FadeIn(old), FadeIn(old_name), Create(old_cross), run_time=.54)
        self.at("if you use a hole", lead=.50)
        self.play(FadeOut(clean), FadeOut(water_only), FadeOut(old), FadeOut(old_cross),
                  FadeOut(old_name), run_time=.47)
        punch = VGroup(slab(1.55, .22, LAND, 0, -.40),
                       slab(1.64, .22, "#B7C2CF", 0, -.11).rotate(.28),
                       Dot(pt(-.61, -.26), radius=.19, color="#AFBCC9")).scale(1.39)
        punch.move_to(pt(-3.63, .86))
        small_dots = VGroup(*[Dot(pt(-4.06+i*.43, -.17), radius=.105, color=PAPER) for i in range(3)])
        self.play(FadeIn(punch, shift=DOWN * .25), run_time=.42)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .21) for d in small_dots], lag_ratio=.33), run_time=.62)
        self.at("handle it yourself")
        self.play(FadeIn(label("Adults handle the punch", -3.43, -1.40), shift=UP * .12), run_time=.42)
        self.finish()


class S14Safety(SpokenScene):
    def construct(self):
        self.add(side_tray())
        adult = person(BLUE).scale(1.04)
        child = person(GREEN).scale(.72).shift(pt(.94, -.12))
        adult.shift(LEFT * .66)
        current = badge(VGroup(adult, child))
        rule = label("Stay beside your child", -3.43, -2.03)
        self.at("stay beside your child")
        self.add(current)
        self.play(FadeIn(rule), run_time=.53)
        self.play(adult.animate.shift(RIGHT * .15), run_time=.79)

        self.at("spray only at", lead=.60)
        sprayer = spray_bottle().rotate(PI / 2.8).move_to(pt(-4.12, .51))
        target = slab(1.45, .17, PAPER, -4.02, -.64)
        face = Dot(pt(-2.65, .45), radius=.36, color="#E8BD9A")
        icon = VGroup(sprayer, target, face, cross(face, .68))
        next_badge = VGroup(current[0].copy(), icon)
        spray_rule = label("Aim at the paper", -3.43, -2.03, BLUE)
        self.play(FadeOut(current[1]), FadeOut(rule), run_time=.30)
        self.remove(current)
        self.add(next_badge[0])
        self.play(FadeIn(icon), run_time=.44)
        mist = spray_fan(pt(-4.35, .17), [pt(x, -.50) for x in np.linspace(-4.6, -3.52, 7)])
        self.add(mist)
        self.play(FadeIn(spray_rule), run_time=.42)

        self.at("keep paper dots", lead=.40)
        pieces = VGroup(*[Dot(pt(x, -.01), radius=.22, color=PAPER) for x in (-4.45, -3.80, -3.15)],
                        slab(.37, .66, GREEN, -2.52, -.04, .08).rotate(-.35))
        choke_rule = label("Under 4 • choking risk", -3.43, -2.03)
        self.play(FadeOut(icon), FadeOut(spray_rule), FadeOut(mist), run_time=.35)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * .24) for p in pieces], lag_ratio=.24), run_time=1.35)
        self.at("children under 4", lead=.30)
        self.play(FadeIn(choke_rule), run_time=.52)
        self.at("count the dots out", lead=.35)
        self.play(FadeOut(pieces[3]), run_time=.24)
        numbers = VGroup(*[label(str(i), x, .61, BLUE, 33)
                           for i, x in enumerate((-4.45, -3.80, -3.15), 1)])
        self.play(LaggedStart(*[FadeIn(n, shift=UP * .12) for n in numbers], lag_ratio=.36), run_time=.77)
        self.play(LaggedStart(*[d.animate.shift(DOWN * .40) for d in pieces[:3]], lag_ratio=.25), run_time=.80)
        self.at("child is choking", lead=.25)
        emergency = label("If choking, call 911", -3.43, -2.03, RED, 35)
        self.play(swap(choke_rule, emergency, run_time=.80))
        self.finish()


class S15SafetyMore(SpokenScene):
    def construct(self):
        self.add(side_tray())
        lips = oval(1.38, .35, "#D9A58D", 0, .51)
        mouth = VGroup(lips, oval(1.10, .13, INK, 0, .51), cross(lips, .85),
                       cocoa_dish().shift(DOWN * .50))
        current = badge(mouth)
        safety = label("Keep supplies out of mouths", -3.40, -2.05, size=29)
        self.at("keep all supplies")
        self.add(current)
        self.play(FadeIn(safety), run_time=.50)
        self.play(mouth[-1].animate.shift(DOWN * .18), run_time=1.13)
        panel = current[0]
        self.remove(current)
        self.add(panel, mouth)

        self.at("cocoa is toxic", lead=.50)
        pets = VGroup(pet("dog"), pet("cat")).arrange(RIGHT, buff=.38).scale(1.14).move_to(pt(-3.52, .14))
        keep_away = label("Keep pets away from cocoa", -3.40, -2.05, size=29)
        self.play(FadeOut(mouth), FadeOut(safety), run_time=.32)
        self.play(FadeIn(pets, shift=LEFT * .25), run_time=.62)
        self.play(FadeIn(keep_away), run_time=.49)
        self.at("keep pets away")
        self.play(pets.animate.shift(LEFT * .53), run_time=.93)

        self.at("wipe up cocoa", lead=.30)
        puddle = oval(1.27, .43, DARK_BLUE, -3.62, -.15)
        splash = VGroup(puddle, *[Dot(pt(x, y), radius=.093, color=ORANGE)
                                  for x, y in [(-3.84, -.08), (-3.08, -.27), (-3.59, -.36)]])
        cloth = towel().scale(.73).move_to(pt(-4.64, -.07))
        self.play(FadeOut(pets), FadeOut(keep_away), run_time=.29)
        self.play(FadeIn(splash), FadeIn(cloth, shift=RIGHT * .22), run_time=.65)
        self.play(cloth.animate.shift(RIGHT * 1.60), FadeOut(splash), run_time=1.23)

        self.at("cocoa -covered paper", lead=.60)
        bin_icon = trash_bin().scale(1.23).move_to(pt(-3.60, -.07))
        scrap = sheet().scale(.15).move_to(pt(-4.32, 1.04))
        scrap.add(oval(.33, .15, ORANGE).move_to(scrap))
        shut_bin = label("Use a pet-proof bin", -3.40, -2.05)
        self.play(FadeOut(cloth), FadeIn(bin_icon), run_time=.41)
        self.play(FadeIn(scrap), bin_icon[2].animate.shift(UP * .49), run_time=.48)
        self.play(scrap.animate.move_to(pt(-3.57, .25)), run_time=.60)
        self.remove(scrap)
        self.play(bin_icon[2].animate.shift(DOWN * .49), FadeIn(shut_bin), run_time=.51)

        self.at("wash everyone's hands", lead=.48)
        faucet = tap().scale(.83).move_to(pt(-3.70, .83))
        hands = VGroup(hand().rotate(.89), hand().rotate(-.77)).arrange(RIGHT, buff=-.10)
        hands.scale(.74).move_to(pt(-3.41, -.46))
        suds = VGroup(*[Dot(pt(x, y), radius=.074, color="#D4EFF0") for x, y in
                        [(-3.8, -.29), (-3.59, -.25), (-3.42, -.16), (-3.24, -.30)]])
        self.play(FadeOut(bin_icon), FadeOut(shut_bin), run_time=.30)
        self.play(FadeIn(faucet), FadeIn(hands), run_time=.44)
        water = linework([pt(-3.23, .48), pt(-3.34, -.39)], DARK_BLUE, 6)
        self.add(water, stream_marks(water, count=4, rate=1.18, size=.064))
        self.play(FadeIn(suds), run_time=.50)
        bob(hands, amp=.13, speed=3.2)
        bob(suds, amp=.13, speed=3.2)
        self.play(FadeIn(label("Wash with soap and water", -3.40, -2.05, BLUE, 30)), run_time=.55)
        self.finish()


class S05Crumple(SpokenScene):
    def construct(self):
        base = plate()
        mesh = paper_mesh(lift=0, flat=True).scale(.76).shift(UP * .45)
        self.add(base, mesh)
        self.at("crumple the paper")
        self.play(Transform(mesh, paper_ball()), run_time=2.34)
        self.at("open it gently")
        self.play(Transform(mesh, paper_mesh(lift=.56)), run_time=2.41)
        self.at("you want hills")
        self.play(Transform(mesh, paper_mesh()), run_time=1.45)
        self.at("ask your child")
        question = question_card("Where is the highest ground?", y=-3.37, size=37)
        self.play(FadeIn(question), run_time=.54)
        main, other = ridges()
        finger = hand().scale(.81).rotate(PI + .24)
        finger.move_to(main.get_start() + pt(.12, .49))
        self.at("the highest ground", lead=.32)
        self.play(FadeIn(finger, shift=LEFT * .72), run_time=.68)
        self.at("then trace each ridge", lead=.40)
        self.play(FadeOut(question), run_time=.31)
        route = main.copy().shift(pt(.12, .49))
        ridge_name = label("Ridge = high ground", 2.25, 3.06, TAN, 36)
        self.play(Create(main, rate_func=linear), MoveAlongPath(finger, route, rate_func=linear),
                  FadeIn(ridge_name, rate_func=squish_rate_func(smooth, .20, .62)), run_time=1.06)
        self.play(Create(other), FadeOut(finger), run_time=.47)
        self.finish()


class S06Town(SpokenScene):
    def construct(self):
        base, mesh, crest = landscape(tilt=0, colored=False, built=False)
        before_bay = bay(tilt=0)
        self.add(base, mesh, crest)
        self.at("color one low corner")
        self.play(FadeIn(before_bay, scale=.56), run_time=1.08)
        self.at("call it the bay")
        bay_name = label("The bay", 4.27, -3.43, BLUE, 33)
        self.play(FadeIn(bay_name), run_time=.50)

        self.at("tuck a folded towel")
        stand = towel().scale(.76).move_to(pt(-5.57, -2.81))
        self.play(FadeIn(stand, shift=RIGHT * .43), run_time=.65)
        self.play(stand.animate.move_to(pt(-3.72, -2.74)),
                  Transform(base[1], tray_parts(1)), Transform(mesh, paper_mesh(tilt=1)),
                  Transform(crest, ridges(1)), Transform(before_bay, bay()), run_time=1.73)
        self.remove(stand)
        self.bring_to_back(plate(1)[0])
        self.at("then draw houses", lead=.38)
        houses, farm, road = town()
        self.play(LaggedStart(*[DrawBorderThenFill(h) for h in houses], lag_ratio=.24), run_time=1.37)
        self.at("a farm and", lead=.12)
        self.play(DrawBorderThenFill(farm), run_time=.52)
        self.at("and a road", lead=.02)
        pencil = marker(PURPLE).scale(.79).rotate(.70)
        drawing = road[0].copy().shift(pt(.47, .31))
        pencil.move_to(drawing.get_start())
        self.add(pencil)
        self.play(Create(road), MoveAlongPath(pencil, drawing), run_time=1.69, rate_func=linear)
        self.play(FadeOut(bay_name), FadeOut(pencil), run_time=.50)
        self.finish()


class S07ChildGuess(SpokenScene):
    def construct(self):
        self.add(landscape())
        dots, guesses = pencils()
        pointer = hand().scale(1.12).rotate(PI)
        offsets = [d.get_center() + pt(.08, .76) for d in dots]
        halos = VGroup(*[Circle(radius=.60, color="#AA713E", stroke_width=8,
                                fill_color=ORANGE, fill_opacity=.52).move_to(d) for d in dots])
        pointer.move_to(offsets[0] + pt(-.84, .36))
        self.at("point to three spots")
        self.add(pointer)
        self.play(pointer.animate.move_to(offsets[0]), run_time=.72)
        self.play(FadeIn(halos[0], scale=.35), FadeIn(dots[0], scale=.35), run_time=.44)
        self.at("on each side")
        self.play(pointer.animate.move_to(offsets[1]), FadeOut(halos[0]), run_time=.69)
        self.play(FadeIn(halos[1], scale=.35), FadeIn(dots[1], scale=.35), run_time=.44)
        self.at("one by a house", lead=.32)
        self.play(pointer.animate.move_to(offsets[2]), FadeOut(halos[1]), run_time=.82)
        self.play(FadeIn(halos[2], scale=.35), FadeIn(dots[2], scale=.35), run_time=.55)
        self.play(FadeOut(pointer, shift=RIGHT * .48), FadeOut(halos[2]), run_time=.53)
        self.at("if rain lands here", lead=.31)
        question = question_card("If rain lands here, where will it go?", y=3.08, size=42)
        self.play(FadeIn(question), run_time=.58)
        self.at("draws a small arrow", lead=.34)
        nib = shape([pt(-1.18, 0), pt(-.78, .27), pt(-.78, -.27)], INK)
        pencil = VGroup(slab(1.70, .53, "#665597", .05, 0, .12),
                        slab(.24, .44, "#AD9ECC", .80, 0, .07), nib).rotate(.60)
        tip_offset = pencil.get_center() - nib.get_vertices()[0]
        for guess in guesses:
            cursor = linework([guess.get_start() + tip_offset, guess.get_end() + tip_offset], INK)
            pencil.move_to(cursor.get_start())
            self.add(pencil)
            self.play(GrowArrow(guess), MoveAlongPath(pencil, cursor), run_time=.63, rate_func=linear)
            self.remove(pencil)
        self.finish()


PREDICT = "Same place,\nor not?"
PREDICT_CARD = {"left": -6.07, "y": 1.25, "max_w": 3.36, "size": 42}


def ridge_closeup():
    # Crop around the same ridge using an inset made from the shared mesh.
    faces = VGroup()
    for v in range(3):
        for u in range(1, 5):
            p, q, r, s = (vertex(u, v, tilt=1), vertex(u+1, v, tilt=1),
                          vertex(u+1, v+1, tilt=1), vertex(u, v+1, tilt=1))
            for tri, i in (([p, q, r], (v*6+u*3) % 8),
                           ([p, r, s], (v*3+u*5+3) % 8)):
                faces.add(shape(tri, FACES[i], FACES[i], .8))
    crest = linework([vertex(3, v, tilt=1) for v in range(4)], TAN, 10)
    water = VGroup(*[dropshape(DARK_BLUE).scale(1.59).move_to(surface(*r[0]) + pt(dx, .71))
                     for r, dx in zip(ROUTES[:2], (-.45, .15))])
    group = VGroup(faces, crest, water).scale(1.22, about_point=ORIGIN).shift(pt(2.52, -.26))
    return group


class S08PredictQuestion(SpokenScene):
    def construct(self):
        top = ridge_closeup()
        self.add(*top[:2])
        card = question_card(PREDICT, **PREDICT_CARD)
        self.at("here is a question")
        self.play(FadeIn(card), run_time=.60)
        self.at("take two drops", lead=.32)
        drops = top[2]
        settled = [d.get_center().copy() for d in drops]
        for d, x in zip(drops, (-.59, .62)):
            d.shift(pt(x, .63))
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .29) for d in drops], lag_ratio=.38), run_time=1.14)
        self.play(*[d.animate.shift(DOWN * .44) for d in drops], run_time=1.54)
        self.at("opposite sides", lead=.36)
        divide = top[1].copy().set_stroke("#9D623D", 15)
        self.add(divide)
        self.bring_to_front(*drops)
        self.play(Create(divide), *[d.animate.move_to(p + UP * .53) for d, p in zip(drops, settled)],
                  run_time=1.91)
        self.at("will they end up")
        self.play(FadeOut(divide), *[d.animate.move_to(p) for d, p in zip(drops, settled)],
                  run_time=2.62)
        self.finish()


class S09PredictPause(PredictPause):
    QUESTION = PREDICT
    CARD = PREDICT_CARD
    RING_AT = (-4.66, -.34, 0)
    SECONDS = 4.5

    def backdrop(self):
        return ridge_closeup()

    def construct(self):
        # A larger ring is legible beside the ridge even in the low-resolution draft.
        ring, sweep = countdown(self.SECONDS, center=self.RING_AT, radius=.80)
        ring[1].add_updater(lambda arc: arc.set_stroke(width=17))
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD), ring)
        self.play(sweep)


class S10Rain(SpokenScene):
    def construct(self):
        world = landscape()
        dots, guesses = pencils()
        hover = VGroup(*[dropshape(DARK_BLUE).move_to(surface(*r[0]) + pt(0, .45)) for r in ROUTES[:2]])
        self.add(world, hover)
        bottle = spray_bottle()
        spray_from = VectorizedPoint(bottle[4].get_left())
        bottle.add(spray_from).flip(UP).scale(.72).rotate(-.58).move_to(pt(-3.21, 3.10))
        fan = spray_fan(spray_from, [surface(u, 1.96) for u in np.linspace(1.45, 5.4, 19)], period=.82)
        for fleck in fan:
            fleck.scale(1.35)
        self.at("the paper from", lead=.72)
        self.play(FadeIn(bottle, shift=UP * .12), run_time=.58)
        self.add(fan)
        measure = DashedLine(pt(-5.75, spray_from.get_y()), pt(-5.75, vertex(0, 0, tilt=1)[1]),
                             dash_length=.14, color=BLUE, stroke_width=4)
        distance = label("About 1 foot", -5.17, 3.52, BLUE, 30)
        self.at("about a foot", lead=.24)
        self.play(Create(measure), run_time=.38)
        self.play(FadeIn(distance), run_time=.38)
        self.at("10 to 20 squirts")
        sprays = caption("10–20 squirts", 33, BLUE, y=-3.45).set_x(0)
        self.play(FadeIn(sprays), run_time=.49)
        self.at("several squirts")
        self.play(FadeOut(sprays), bottle.animate.rotate(-.10).shift(DOWN * .08), run_time=.54)
        self.play(bottle.animate.rotate(.10).shift(UP * .08), run_time=1.22)
        fan.clear_updaters(recursive=True)
        self.play(FadeOut(fan), FadeOut(bottle), FadeOut(distance), FadeOut(measure), run_time=.43)

        paths = [rain_path(i) for i in range(3)]
        self.at("the marker bleeds", lead=.37)
        ink = VGroup(*[rain_path(i, "#85B5BC", 24) for i in range(3)])
        self.play(LaggedStart(*[Create(trail) for trail in ink], lag_ratio=.24), run_time=2.24)
        self.play(LaggedStart(*[Create(trail) for trail in paths], lag_ratio=.10), run_time=1.06)
        self.at("drops on each side", lead=.55)
        for d, route in zip(hover, paths[:2]):
            d.scale(1.77).move_to(route.get_start())
        self.bring_to_front(hover)
        self.play(*(MoveAlongPath(d, route) for d, route in zip(hover, paths)),
                  run_time=1.78, rate_func=linear)
        self.play(GrowFromCenter(local_pool()), FadeOut(hover), FadeOut(ink), run_time=.65)
        self.add(wet_glints(paths))
        self.finish()


class S11Check(SpokenScene):
    def construct(self):
        world = landscape()
        trails = wet_details()
        dots, guesses = pencils()
        self.add(world, trails, dots, guesses, wet_glints(trails[:3]))
        self.at("check the arrows")
        for a in guesses:
            self.play(a.animate.set_color(ORANGE), run_time=.39)
            self.play(a.animate.set_color(INK), run_time=.34)
        self.at("did the rain go")
        question = question_card("Did the rain go where you guessed?", y=3.11, size=37)
        self.play(FadeIn(question), run_time=.52)
        self.at("then name it")
        self.play(FadeOut(question), FadeOut(dots), FadeOut(guesses), run_time=.45)

        self.at("all the land", lead=.30)
        colored = paper_mesh(tilt=1, watersheds=True)
        old_mesh = world[1]
        for index in range(0, 48, 12):
            self.play(*[Transform(a, b) for a, b in zip(old_mesh[index:index+12], colored[index:index+12])],
                      run_time=.54)
        watershed = label("Watershed", 4.04, -3.47, GREEN, 37)
        self.at("one watershed", lead=.32)
        self.play(FadeIn(watershed), run_time=.61)
        self.at("the ridges split", lead=.20)
        ridge_glow = linework([vertex(3, v, tilt=1) for v in range(5)], "#9A633D", 14)
        # A second pass brightens the two catchments as their common edge is traced.
        sharp_washes = paper_mesh(tilt=1, watersheds=True)
        for face in sharp_washes[:]:
            face.set_fill(interpolate_color(face.get_fill_color(), ManimColor("#748A65"), .29))
        self.play(Create(ridge_glow), Transform(old_mesh, sharp_washes), run_time=1.78)
        self.finish()


def fertilizer_spot():
    where = surface(4.02, 1.51)
    return VGroup(*[Dot(where + pt(x, y), radius=.052, color=ORANGE) for x, y in
                    [(-.20, .04), (-.11, -.02), (-.08, .12), (.02, -.08),
                     (.09, .05), (.16, .11), (.19, -.02), (.27, .05)]])


class S12Pollution(SpokenScene):
    def construct(self):
        world = landscape()
        trails = wet_details()
        self.add(world, trails, wet_glints(trails[:3]))
        cocoa = fertilizer_spot()
        fertilizer = label("Pretend fertilizer", 3.33, 2.99, ORANGE, 34)
        self.at("a pinch of cocoa", lead=.35)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .35) for d in cocoa], lag_ratio=.16), run_time=1.52)
        self.play(FadeIn(fertilizer), run_time=.60)
        bob(cocoa, amp=.05, speed=2.0)
        self.at("if allergies or asthma")
        self.play(FadeOut(fertilizer), run_time=.46)
        option = label("Colored water, if suitable", 3.00, 2.98, BLUE, 32)
        sample = VGroup(*[dropshape(ORANGE).scale(.65).move_to(pt(1.63+i*.33, 2.25-.14*(i%2)))
                          for i in range(3)])
        self.at("use colored water", lead=.45)
        self.play(FadeIn(sample, shift=DOWN * .28), run_time=.64)
        self.play(FadeIn(option), run_time=.50)
        for i, d in enumerate(sample):
            bob(d, amp=.12, seed=i)
        self.at("you can skip both")
        self.play(FadeOut(sample), FadeOut(option), run_time=.51)
        litter = VGroup(*[Dot(surface(x, y), radius=.097, color=ORANGE) for x, y in
                          [(1.28, 2.08), (1.54, 2.11), (4.03, 2.38)]])
        self.at("put a few paper dots")
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .49) for d in litter], lag_ratio=.34), run_time=1.25)
        litter_name = label("Paper litter", -3.92, 2.93, ORANGE, 33)
        self.at("as litter")
        self.play(FadeIn(litter_name), run_time=.51)
        runoff = local_line([(4.02, 1.51), (4.07, 1.90), (4.24, 2.49), (4.80, 3.02),
                             (5.10, 3.40), (5.57, 3.76)], ORANGE, 10)
        source = pt(-.65, 2.82)
        self.at("spray again")
        fan = spray_fan(source, [surface(u, 2.13) for u in np.linspace(1, 5.4, 15)])
        self.add(fan)
        self.play(FadeOut(litter_name), run_time=.47)
        self.at("watch where everything", lead=.30)
        self.play(Create(runoff), litter[2].animate.shift(pt(.29, -.24)), run_time=1.65, rate_func=linear)
        self.add(stream_marks(runoff, count=3, color="#FFCA7B", rate=.48, size=.10))
        self.finish()


def map_picture():
    outline = shape([pt(-6, -.89), pt(-5.16, -.26), pt(-4.44, .05), pt(-3.95, .67),
                     pt(-3.14, .60), pt(-2.82, 1.25), pt(-2.33, 1.53), pt(-1.98, 2.09),
                     pt(-1.35, 2.39), pt(-1.08, 1.82), pt(-.60, 1.53), pt(-.23, 1.07),
                     pt(.31, .91), pt(.04, .63), pt(.72, .32), pt(.54, -.21),
                     pt(.85, -.66), pt(.94, -1.17), pt(-5.77, -1.17)],
                    "#CFDAB8", "#92B591", 3)
    river = linework([pt(-3.35, .14), pt(-2.68, -.05), pt(-2.25, .10), pt(-1.75, -.20),
                      pt(-1.26, .06), pt(-.80, -.24), pt(-.37, -.27), pt(.55, -.81)], DARK_BLUE, 9)
    mouth = oval(.55, .26, DARK_BLUE).move_to(river.get_end())
    return VGroup(outline, river, mouth)


def seedling():
    soil = oval(1.10, .24, "#AA7958", 0, -.45)
    trunk = linework([pt(0, -.43), pt(0, .42)], DARK_GREEN, 7)
    leaves = VGroup(oval(.58, .26, GREEN, -.19, .20).rotate(-.50),
                    oval(.61, .28, "#75B768", .25, .47).rotate(.53))
    return VGroup(soil, trunk, leaves)


class S13Home(SpokenScene):
    def construct(self):
        outline, river, mouth = map_picture()
        self.add(outline)
        title = heading("Virginia’s watersheds", x=-2.55, y=3.04, size=43)
        tag = scope_tag(size=29, color=TEXT).move_to(pt(-2.35, -2.08))
        self.at("a map of virginia's")
        self.play(FadeIn(title), FadeIn(tag), run_time=.57)
        self.at("find your town", lead=.41)
        town_pin = pin().scale(.75).move_to(river.get_start() + pt(0, .34))
        name = label("Our town", -4.24, 1.14, ORANGE, 33)
        self.play(FadeIn(town_pin, shift=DOWN * .30), run_time=.50)
        self.play(FadeIn(name), run_time=.23)
        self.at("follow the river", lead=.12)
        self.play(Create(river), run_time=1.52, rate_func=linear)
        self.play(FadeIn(mouth), run_time=.48)
        self.add(stream_marks(river, count=5, rate=.26))

        activities = [
            (trash_bin().scale(.97), 3.47, 1.54),
            (seedling().scale(1.14), 3.47, -.05),
            (tap().scale(.94), 3.47, -1.79),
        ]
        self.at("pick three things")
        action = label("Draw three family actions", 3.42, 2.83, size=29)
        self.play(FadeIn(action), run_time=.48)
        for icon, x, y in activities:
            icon.move_to(pt(x, y))
            self.play(DrawBorderThenFill(icon), run_time=.79)
        self.play(activities[1][0].animate.shift(DOWN * .28), run_time=.60)
        icon_bin, tree, faucet = (item[0] for item in activities)
        self.at("put trash in the bin", lead=.19)
        trash = shape([pt(-.17, -.13), pt(-.20, .06), pt(.07, .16),
                       pt(.19, .01), pt(.11, -.14)], ORANGE)
        trash.move_to(icon_bin.get_top() + pt(.62, .27))
        self.add(trash)
        self.play(icon_bin[2].animate.shift(UP * .21), run_time=.29)
        self.play(trash.animate.move_to(icon_bin[0].get_top()), run_time=.39)
        self.remove(trash)
        self.play(icon_bin[2].animate.shift(DOWN * .21), run_time=.26)
        self.at("turn off the tap", lead=.25)
        drip = dropshape().scale(.46).move_to(faucet[0].get_end() + pt(0, -.14))
        self.add(drip)
        self.play(faucet[1][1].animate.rotate(PI / 4), FadeOut(drip, shift=DOWN * .27), run_time=.74)
        self.finish()


class S16Return(SpokenScene):
    def construct(self):
        world, flow = street()
        self.add(world, stream_marks(flow, count=7, size=.235, rate=.19))
        litter = shape([pt(-.17, -.07), pt(-.11, .16), pt(.12, .13),
                        pt(.21, -.07), pt(.04, -.15)], ORANGE, "#FFD19E", 2)
        litter.move_to(flow.point_from_proportion(.19))
        path = flow.copy().pointwise_become_partial(flow, .19, 1)
        self.at("rain can carry", lead=.36)
        self.play(FadeIn(litter, shift=DOWN * .17), run_time=.46)
        surge = oval(1.58, .36, "#8DD7E7").rotate(-.27)
        litter.set_z_index(1)
        surge_path = path.copy().shift(UP * .05)
        self.play(MoveAlongPath(litter, path), MoveAlongPath(surge, surge_path),
                  run_time=2.57, rate_func=linear)
        self.remove(surge)
        self.play(FadeOut(litter, scale=.40), run_time=.29)
        drain_name = label("Storm drain", 4.62, .58, BLUE, 33)
        self.play(FadeIn(drain_name), run_time=.41)
        self.at("your pan shows", lead=.25)
        creek = linework([pt(4.86, -1.84), pt(4.16, -2.26), pt(3.23, -2.50),
                          pt(2.55, -2.74), pt(1.28, -2.93), pt(.38, -3.03)], BLUE, 9)
        creek_name = label("Creek", -1.10, -3.37, BLUE, 32)
        self.play(Create(creek), run_time=1.36)
        self.play(FadeIn(creek_name), run_time=.36)
        parcel = litter.copy().move_to(creek.get_start())
        self.add(parcel, stream_marks(creek, count=4, size=.18))
        self.at("carry them downstream", lead=.40)
        self.play(MoveAlongPath(parcel, creek), run_time=1.32, rate_func=linear)
        self.finish()


class S17End(EndCard):
    LINE = "Rain runs downhill and carries what it picks up downstream."
