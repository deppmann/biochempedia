"""One tree, from a fixed fence-post view and a close view of its twigs."""

from bp_parts import *
from bp_style import EndCard

# COLOR MAP: blue = sky and observation, gold = fall and highlighted buds,
# green = growth, red = safety, brown = wood, cream = field notes.
INK = "#183B45"
WOOD = "#684637"
BARK = "#98715A"
PAPER = "#FFF5DC"
SHADOW = "#B6C4AE"
ALERT = "#A1372C"
AMBER = "#AD690E"
LEAF_GREEN = "#387552"
TREE_AT = np.array([3.5, -3.02, 0])
POST_AT = np.array([-5.83, -2.87, 0])
LEFT_AT = -3.35
SAFETY_AT = -2.80
QUESTION = "What will you see\non a bare winter twig?"
SEASONS = {
    "Winter": ("#D5E6EA", "#B9D1D5", "#7C9A91", "#ACC4AF", ()),
    "Spring": ("#DDEDEA", "#BDDAD1", "#759D6F", "#A9C792", ("#689D62", "#9AB965", "#B8C771")),
    "Summer": ("#D5E9EB", "#B4D6D2", "#648969", "#9EBE84", ("#32765C", "#4B9067", "#77A65E")),
    "Fall": ("#F3E6CE", "#DED4AD", "#888C64", "#B4BA83", ("#AA5E35", "#CC8539", "#DEAA4E", "#5B885B")),
}

# Each path starts on a parent limb. The same paths are reused in the photos.
LIMBS = [
    (0.63, [(0, 0), (-.10, .9), (.04, 2.0), (.27, 3.12), (.10, 4.05), (.34, 5.15), (.29, 5.80)]),
    (.36, [(0, 1.45), (-.54, 2.36), (-1.17, 3.12), (-1.88, 3.57), (-2.39, 4.05)]),
    (.28, [(.12, 2.33), (.80, 2.94), (1.48, 3.20), (2.16, 3.89), (2.63, 4.04)]),
    (.24, [(.26, 3.05), (-.48, 3.77), (-.72, 4.38), (-1.25, 5.17), (-1.77, 5.50)]),
    (.20, [(.11, 3.77), (.84, 4.16), (1.16, 4.71), (1.95, 5.22)]),
    (.15, [(-1.11, 3.07), (-1.54, 3.82), (-1.48, 4.39), (-1.81, 4.85)]),
    (.13, [(-1.58, 3.36), (-2.07, 3.35), (-2.63, 3.57)]),
    (.14, [(-.49, 3.79), (-.96, 4.04), (-1.30, 4.65), (-1.26, 5.06)]),
    (.11, [(-.83, 4.57), (-.69, 5.09), (-.80, 5.66)]),
    (.10, [(.28, 5.04), (-.03, 5.39), (-.17, 5.75)]),
    (.15, [(.19, 4.48), (.68, 4.92), (.81, 5.50), (1.18, 5.79)]),
    (.12, [(1.10, 4.62), (1.68, 4.70), (2.24, 5.02)]),
    (.11, [(1.64, 5.04), (1.73, 5.54), (1.98, 5.72)]),
    (.13, [(1.45, 3.21), (1.68, 3.75), (1.53, 4.29)]),
    (.11, [(1.84, 3.58), (2.37, 3.52), (2.78, 3.73)]),
    (.08, [(-2.29, 3.95), (-2.48, 4.38), (-2.39, 4.65)]),
    (.08, [(2.10, 3.83), (2.31, 4.28), (2.54, 4.55)]),
    (.09, [(-1.36, 5.23), (-1.39, 5.68), (-1.28, 5.84)]),
]
CROWN = [(-2.26, 3.9), (-1.86, 4.56), (-1.48, 5.25), (-.89, 5.54), (-.30, 5.65),
         (.31, 5.67), (.92, 5.65), (1.64, 5.46), (2.11, 5.05), (2.46, 4.45),
         (2.36, 3.86), (1.71, 3.79), (1.06, 4.28), (.50, 4.82), (-.17, 4.63),
         (-.92, 4.44), (-1.60, 3.77), (-.65, 3.77), (.53, 3.81), (1.20, 3.53)]


def p(x, y):
    return np.array([x, y, 0.0])


def patch(points, color, smooth=False):
    corners = [p(*xy) for xy in (*points, points[0])]
    shape = VMobject(stroke_width=0, fill_color=color, fill_opacity=1)
    if smooth:
        shape.set_points_smoothly(corners)
    else:
        shape.set_points_as_corners(corners)
    return shape


def path(points, color, width=3):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly([p(*xy) for xy in points])


def slab(w, h, color, x=0, y=0, radius=.13):
    return RoundedRectangle(width=w, height=h, corner_radius=radius, stroke_width=0,
                            fill_color=color, fill_opacity=1).move_to(p(x, y))


def oval(w, h, color, x=0, y=0, angle=0):
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=color,
                   fill_opacity=1).rotate(angle).move_to(p(x, y))


def edge(x0, y0, x1, y1, color, width=3):
    return Line(p(x0, y0), p(x1, y1), stroke_color=color, stroke_width=width)


def leaf(color, length=.30, width=.15, angle=0):
    shape = patch([(-.5, 0), (-.09, -.48), (.29, -.37), (.5, 0), (.16, .43), (-.19, .43)], color, True)
    return shape.stretch_to_fit_width(length).stretch_to_fit_height(width).rotate(angle)


def limb(points, width, color=WOOD):
    xy = np.asarray(points, dtype=float)
    tangent = np.gradient(xy, axis=0)
    normal = tangent[:, ::-1] * np.array([-1, 1])
    normal /= np.linalg.norm(normal, axis=1)[:, None]
    radii = (width / 2 * np.linspace(1, .035, len(xy))**.86)[:, None]
    return patch([*map(tuple, xy + radii * normal), *map(tuple, (xy - radii * normal)[::-1])], color, True)


def tree(season):
    colors = SEASONS[season][-1]
    wood = VGroup(*[limb(points, width) for width, points in LIMBS])
    wood.add(
        patch([(-.65, .02), (-.28, .25), (-.17, .68), (.16, .68), (.28, .22), (.63, .04)], WOOD, True),
        path([(-.12, .13), (-.16, .68), (-.02, 1.23), (.05, 1.64)], BARK, 2.8),
        path([(.14, .25), (.15, .85), (.10, 1.24)], BARK, 1.8),
        path([(-.16, 1.52), (-.50, 2.13), (-.97, 2.80)], BARK, 1.8),
    )
    crown = VGroup()
    rng = np.random.default_rng(1125)
    if colors:
        for i, (x, y) in enumerate(CROWN):
            if season == "Fall" and i in (2, 6, 11, 13, 17):
                continue
            if season == "Spring":
                for j in range(3):
                    crown.add(leaf(colors[(i + j) % len(colors)], .25, .13, rng.uniform(-1.2, 1.2))
                              .move_to(p(x + .18 * (j - 1), y + rng.uniform(-.15, .15))))
                continue
            for j in range(3):
                dx, dy = rng.uniform(-.35, .35, 2)
                crown.add(leaf(colors[(i + j) % len(colors)], rng.uniform(.65, 1.17),
                               rng.uniform(.40, .69), rng.uniform(-1, 1)).move_to(p(x + dx, y + dy)))
    return VGroup(wood, crown)


def post():
    return VGroup(
        patch([(-.19, 0), (-.18, 1.34), (.01, 1.49), (.23, 1.34), (.22, 0)], WOOD),
        patch([(-.18, 0), (-.18, 1.34), (.01, 1.49), (.02, 0)], BARK),
        edge(-.08, .22, -.08, 1.12, WOOD, 1.8),
    )


def scenery(season):
    sky, distant, land, grass, colors = SEASONS[season]
    backdrop = Rectangle(width=config.frame_width, height=config.frame_height, stroke_width=0,
                         fill_opacity=1, fill_color=sky)
    hills = patch([(-7.11, -3.73), (-7.11, -1.81), (-4.8, -1.24), (-2.6, -1.81),
                   (-.9, -1.54), (.7, -1.07), (3.2, -1.18), (5.56, -1.64), (7.11, -1.26), (7.11, -3.73)], distant)
    lawn = patch([(-7.11, -4), (-7.11, -2.52), (-4.7, -2.61), (-2.37, -2.37), (0, -2.62),
                  (2.5, -2.42), (5.0, -2.38), (7.11, -2.62), (7.11, -4)], land)
    shadow = oval(4.6, .35, grass, 3.45, -3.05)
    tufts = VGroup()
    for x, y in [(-6.5, -3.57), (-5.1, -3.42), (-3.63, -3.69), (-1.5, -2.96),
                 (.22, -3.54), (1.5, -3.11), (5.5, -3.49), (6.55, -2.89)]:
        tufts.add(VGroup(*[path([(x + .08 * i, y), (x + .12 * i, y + .12),
                                (x + .18 * i, y + .21 - .025 * abs(i))], grass, 2.4) for i in [-1, 0, 1]]))
    litter = VGroup()
    if season == "Fall":
        for i, (x, y) in enumerate([(1.2, -3.3), (2.2, -3.46), (2.85, -3.12), (3.72, -3.41), (4.6, -3.23), (5.52, -3.02)]):
            litter.add(leaf(colors[i % 3], .34, .12, i * .72).move_to(p(x, y)))
    return VGroup(backdrop, hills, lawn, shadow, tufts, litter)


def sway(mob, pivot, amplitude=.045, speed=1.45):
    phase = 0.0
    previous = 0.0

    def bend(obj, dt):
        nonlocal phase, previous
        phase += dt * speed
        angle = amplitude * np.sin(phase)
        obj.rotate(angle - previous, about_point=pivot)
        previous = angle
        obj.bend_angle = angle

    mob.bend_angle = 0.0
    return mob.add_updater(bend)


def landscape(season, moving=False):
    land = scenery(season)
    main = tree(season).shift(TREE_AT)
    fence = post().shift(POST_AT)
    if moving:
        sway(main, TREE_AT)
        for tuft in land[4]:
            sway(tuft, tuft.get_bottom(), .21, 2.2)
    return VGroup(land, fence, main)


def change_season(scene, world, season, seconds=1.4):
    old_land, _, main = world
    _, crown = main
    new_land = scenery(season)
    new_crown = tree(season)[1].shift(TREE_AT)
    main.clear_updaters()
    main.rotate(-main.bend_angle, about_point=TREE_AT)
    if len(crown) and not len(new_crown):
        leaves = VGroup(*[leaf(SEASONS["Fall"][-1][i % 3], .28, .15, i * .8)
                          .move_to(p(1.7 + i % 6 * .75, .65 + (i * 3 % 7) * .30)) for i in range(12)])
        # Keep the crown in the landscape while fading so Manim preserves its parent groups.
        scene.play(FadeIn(leaves), crown.animate.set_opacity(0), Transform(old_land, new_land), run_time=.75)
        scene.play(LaggedStart(*[FadeOut(obj, shift=p(.28 + i * .025, -1.7 - i % 4 * .23))
                                 for i, obj in enumerate(leaves)], lag_ratio=.07), run_time=seconds)
        main.remove(crown)
        main.add(new_crown)
    else:
        main.remove(crown)
        main.add(new_crown)
        scene.play(Transform(old_land, new_land), FadeIn(new_crown, scale=.83), run_time=seconds)
    sway(main, TREE_AT)


def title_text(text, x=LEFT_AT, y=1.65, size=50, color=INK):
    return T(text, size, color, font=TITLE_FONT, line_spacing=.84).move_to(p(x, y))


def label(text, x=LEFT_AT, y=2.54, size=32, color=INK):
    return T(text, size, color, weight=SEMIBOLD, line_spacing=.83).move_to(p(x, y))


def twig(show_buds=True):
    body = VGroup(
        limb([(-1.88, -1.19), (-1.13, -.64), (-.35, -.16), (.44, .27), (1.09, .64), (1.51, .90)], .42),
        limb([(-.56, -.28), (-.55, .14), (-.74, .58), (-1.03, .92)], .19),
        limb([(.33, .20), (.75, .06), (1.08, .05)], .15),
        path([(-1.77, -1.13), (-1.15, -.69), (-.33, -.20), (.51, .27), (1.41, .82)], BARK, 3.1),
        edge(.31, .15, .43, .19, "#C6A081", 3),
        edge(-.44, -.29, -.33, -.24, "#C6A081", 3),
    )
    specimen = VGroup(body)
    if show_buds:
        specimen.add(bud(.70, .34).rotate(.58).move_to(p(1.52, .94)),
                     bud(.49, .26).rotate(1.10).move_to(p(.32, .37)))
    return specimen


def bud(length, width):
    base = leaf("#9D5835", length, width)
    seam = path([(-.34, -.10), (.02, .05), (.33, .14)], "#D69C64", 2)
    seam.stretch_to_fit_width(length * .64).stretch_to_fit_height(width * .38).move_to(base)
    return VGroup(base, seam)


def twig_view(show_buds=True):
    # An opaque paper-colored inset keeps the branch and its silhouette distinct.
    rim = oval(5.54, 5.54, "#EFF6ED", 3.54, .05)
    interior = oval(5.30, 5.30, "#BCCFD0", 3.54, .05)
    specimen = twig(show_buds=show_buds).scale(1.05, about_point=ORIGIN).shift(p(3.54, .05))
    return VGroup(rim, interior, specimen)


def predict_card():
    card = question_card(QUESTION, y=1.33, color=INK, size=39, max_w=5.6)
    card.move_to(p(LEFT_AT, 1.33))
    return card


def notebook(kind="sketch"):
    cover = slab(3.75, 2.55, "#93724C", 0, -.06)
    page = slab(3.65, 2.50, PAPER)
    ruling = VGroup(*[edge(-1.02, y, 1.35, y, "#D2C7A7", 2) for y in [.61, .25, -.11, -.47, -.83]])
    spine = edge(-1.36, -.99, -1.36, .99, "#D8AB8D", 2)
    if kind == "sketch":
        mark = twig().scale(.65).move_to(p(.21, .03))
    else:
        mark = VGroup(*[slab(.47, .42, "#D0DBC4", (i % 4 - 1.5) * .58 + .18, .51 - .56 * (i // 4), .035)
                        for i in range(12)])
        for i in range(8):
            mark.add(oval(.12, .12, GREEN, (i % 4 - 1.5) * .58 + .18, .51 - .56 * (i // 4)))
    return VGroup(cover, page, ruling, spine, mark)


def pencil():
    return VGroup(slab(1.34, .16, "#D4A843", .1, 0, .05),
                  patch([(-.55, -.08), (-.85, 0), (-.55, .08)], BARK),
                  patch([(-.74, -.03), (-.85, 0), (-.74, .03)], INK)).rotate(.43)


def photo(season, width=2.85):
    ground = SEASONS[season][2]
    backdrop = slab(3.05, 3.44, PAPER)
    field = slab(2.76, 2.89, SEASONS[season][0], 0, .13, .06)
    grass = slab(2.76, .46, ground, 0, -1.10, .06)
    t = tree(season).scale(.39, about_point=ORIGIN).shift(p(.26, -1.14))
    fence = post().scale(.39, about_point=ORIGIN).shift(p(-1.02, -1.14))
    g = VGroup(backdrop, field, grass, fence, t)
    if season == "Fall":
        g.add(VGroup(*[leaf("#CC8539", .18, .075, i).move_to(p(x, y))
                       for i, (x, y) in enumerate([(-.39, -1.14), (.16, -1.22), (.78, -1.16), (1.03, -1.25)])]))
    return g.scale(width / 3.05)


def pine():
    return VGroup(slab(.23, 2.5, WOOD, 0, -1.05),
                  *[patch([(-w, y - .93), (0, y + .9), (w, y - .93)], c)
                    for w, y, c in [(1.08, -.27, "#56765C"), (.88, .35, "#5B8163"), (.64, .94, "#6A8C6B")]])


def cross(center, size=.85):
    x, y = center[:2]
    return VGroup(edge(x-size, y-size, x+size, y+size, ALERT, 7),
                  edge(x-size, y+size, x+size, y-size, ALERT, 7))


def phone():
    body = slab(2.86, 1.75, INK)
    view = photo("Fall", 1.13)
    view.move_to(ORIGIN)
    hand = oval(.58, .94, "#CD946F", -1.34, -.60, -.5)
    thumb = oval(.28, .70, "#E1AC87", -1.15, -.32, -.16)
    shutter = oval(.19, .19, PAPER, 1.13, 0)
    return VGroup(hand, body, slab(2.29, 1.46, "#C7DADD", -.10, 0), view, shutter, thumb)


def viewfinder():
    corners = VGroup()
    for x, sx in [(.50, 1), (6.53, -1)]:
        for y, sy in [(-3.37, 1), (3.13, -1)]:
            corners.add(edge(x, y, x + sx * .36, y, INK, 4),
                        edge(x, y, x, y + sy * .36, INK, 4))
    return corners


def sun(x=0, y=0):
    rays = VGroup()
    for a in np.arange(8) * TAU / 8:
        ray = p(np.cos(a), np.sin(a))
        rays.add(Line(ray * .49, ray * .71, color="#BA791A", stroke_width=3.5))
    return VGroup(oval(.75, .75, "#D9A547"), rays).shift(p(x, y))


def cloud(color="#849CA6"):
    return VGroup(oval(1.10, .54, color, -.33, -.08),
                  oval(.77, .75, color, .11, .08), oval(.81, .52, color, .50, -.12))


def bird():
    return VGroup(oval(.77, .49, INK, 0, 0, .39), oval(.41, .40, INK, .28, .22),
                  patch([(.42, .27), (.70, .20), (.45, .14)], AMBER),
                  patch([(-.19, .05), (-.66, -.16), (-.30, -.22)], INK),
                  oval(.38, .23, "#446672", -.06, -.02, .37), oval(.065, .065, PAPER, .34, .26),
                  edge(.04, -.19, .11, -.40, WOOD), edge(-.09, -.20, -.12, -.40, WOOD))


def sectioned_bud():
    shell = leaf("#734732", 4.3, 2.2, .54)
    inside = leaf("#E0B183", 3.88, 1.85, .54)
    foliage = VGroup(leaf("#315C40", 2.67, .48, .57).shift(p(-.17, .07)),
                     leaf("#467746", 2.53, .45, .31).shift(p(-.05, -.26)),
                     leaf("#6B9552", 2.27, .42, .80).shift(p(-.10, .33)),
                     path([(-1.31, -.61), (-.53, -.24), (.38, .10), (1.06, .48)], "#B9C477", 3.2))
    return VGroup(shell, inside, foliage).move_to(p(3.52, .03))


def walk_pair():
    people = VGroup()
    for x, scale, coat in [(-.50, 1, "#3F7C85"), (.57, .68, "#D59951")]:
        body = VGroup(oval(.51, .57, "#BE8868", 0, 1.81),
                      slab(.75, 1.03, coat, 0, 1.01, .18),
                      path([(-.20, .69), (-.24, .22), (-.28, 0)], INK, 9),
                      path([(.19, .68), (.23, .26), (.28, 0)], INK, 9),
                      edge(-.36, 1.34, -.48, .80, coat, 9),
                      edge(.36, 1.32, .56, .93, coat, 9))
        people.add(body.scale(scale, about_point=ORIGIN).shift(p(x, 0)))
    return people


def no_sign(icon):
    rim = Circle(radius=1.07, stroke_width=5, color=ALERT)
    return VGroup(icon, rim, edge(-.74, -.74, .74, .74, ALERT, 6))


def acorn():
    return VGroup(oval(.68, .85, "#B47143", 0, -.13),
                  oval(.84, .35, WOOD, 0, .17), edge(-.02, .28, .12, .42, WOOD, 4))


def ivy():
    stem = path([(-.43, -1.38), (-.54, -.78), (-.04, -.38), (.02, .19), (.27, .85)], WOOD, 5)
    cluster = VGroup()
    for x, y, a in [(-.44, .47, 2.70), (.26, .39, .31), (.17, 1.06, 1.45)]:
        cluster.add(leaf("#497851", .85, .57, a).move_to(p(x, y)))
    cluster.add(edge(-.03, .13, -.41, .47, "#30583D", 3),
                edge(-.03, .13, .24, .37, "#30583D", 3),
                edge(-.03, .13, .17, .99, "#30583D", 3))
    return VGroup(stem, cluster)


def caterpillar():
    g = VGroup()
    for i in range(6):
        x, y = -.71 + i * .28, .05 + .18 * np.sin(i * .66)
        g.add(oval(.42, .37, "#719551" if i % 2 else "#557D45", x, y))
        for j in [-1, 0, 1]:
            g.add(edge(x + j * .08, y + .10, x + j * .11, y + .27, WOOD, 1.5))
    g.add(oval(.085, .085, INK, .79, .20))
    eye = path([(-1.16, .0), (-.58, .59), (.05, .70), (.66, .54), (1.16, 0),
                (.58, -.51), (-.06, -.62), (-.70, -.46), (-1.16, 0)], INK, 3)
    return VGroup(eye, g)


def lens():
    return VGroup(Circle(radius=.53, color=INK, stroke_width=8, fill_color=TEAL, fill_opacity=.20),
                  slab(.23, .90, INK, .60, -.64, .07).rotate(.7),
                  Arc(radius=.34, start_angle=1.42, angle=1.1, color=PAPER, stroke_width=5))


def hands():
    a = oval(.91, .39, "#CB8E6A", -.32, -.28, .34)
    b = oval(.91, .39, "#DFAB85", .27, -.12, -.24)
    bubbles = VGroup(*[Circle(radius=r, color="#407B88", stroke_width=2.6).move_to(p(x, y))
                       for x, y, r in [(-.48, .33, .17), (-.10, .17, .12), (.29, .51, .22), (.58, .19, .13)]])
    check = path([(.81, .02), (.96, -.12), (1.24, .24)], "#39784F", 5)
    return VGroup(a, b, bubbles, check)


def safety_picture(icon, message):
    backing = slab(5.34, 4.16, PAPER, SAFETY_AT, .69, .23)
    icon.move_to(p(SAFETY_AT, .87))
    title = label(message, x=SAFETY_AT, y=-.81, size=32)
    return VGroup(backing, icon, title)


class S01Hook(SpokenScene):
    def construct(self):
        world = landscape("Winter", moving=True)
        self.add(world)
        self.at("looks dead")
        hook = title_text("Bare in winter.\nDead?", y=1.53, size=58)
        self.play(FadeIn(hook, shift=UP * .10), run_time=.77)
        self.at("walk past the same")
        self.play(Indicate(world[1], color="#815441", scale_factor=1.06), run_time=1.35)
        self.at("visited through the year")
        self.play(FadeOut(hook, shift=UP*.13), run_time=1.3)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Adopt a Tree"
    TITLE = "Adopt a Tree: Parent Guide"

    def construct(self):
        self.add(landscape("Winter", moving=True))
        heading = title_text(self.LESSON, y=1.57, size=55)
        sub = label(self.TITLE.split(": ", 1)[1], y=.65, size=32)
        rule = edge(-4.19, .08, -2.51, .08, AMBER, 4)
        orbit = Arc(radius=3.40, start_angle=2.67, angle=.46, stroke_width=5,
                    color="#B98948", arc_center=p(3.50, .15))
        self.play(FadeIn(heading, shift=UP*.14), FadeIn(sub), GrowFromCenter(rule), Create(orbit), run_time=.68)
        self.play(Rotate(orbit, -.48, about_point=p(3.50, .15)), run_time=.83)
        self.play(FadeOut(orbit), run_time=.35)
        self.wait(.14)


class S03Payoff(SpokenScene):
    def construct(self):
        world = landscape("Winter", moving=True)
        self.add(world)
        self.at("adopting one tree")
        change_season(self, world, "Fall", 1.9)
        self.at("your child practices")
        folio = notebook().move_to(p(LEFT_AT, -.18))
        cover = slab(3.85, 2.63, "#AB834F", LEFT_AT, -.18)
        self.play(FadeIn(cover, shift=UP*.37), run_time=.55)
        self.play(FadeIn(folio), cover.animate.stretch(.045, 0, about_edge=LEFT), run_time=.82)
        self.remove(cover)
        current = label("Look closely", y=1.77)
        self.play(FadeIn(current), run_time=.5)
        self.at("make a guess")
        calendar = notebook("calendar").move_to(folio)
        next_label = label("Predict and check", y=1.77)
        self.play(swap(current, next_label), swap(folio[4], calendar[4], 1.12), run_time=1.12)
        self.at("check it against")
        entry = calendar[4][-1]
        self.play(Indicate(entry, color="#55874A", scale_factor=1.7), run_time=1.27)
        self.at("30 minutes to start")
        time = label("30 minutes to start", y=1.77)
        self.play(swap(next_label, time), run_time=.82)
        self.finish()


class S04Setup(SpokenScene):
    def construct(self):
        world = landscape("Fall", moving=True)
        evergreen = pine().scale(.79).move_to(p(LEFT_AT, -.80))
        self.add(world, evergreen)
        self.at("drops its leaves")
        rejection = cross(evergreen.get_center(), .82)
        self.play(Create(rejection), run_time=.7)
        self.play(FadeOut(evergreen), FadeOut(rejection), run_time=1.05)
        self.at("ask permission")
        ask = label("Ask permission", y=1.75)
        self.play(FadeIn(ask), run_time=.55)
        self.at("bring a phone")
        device = phone().move_to(p(-4.86, .40))
        page = notebook().scale(.53).move_to(p(-2.02, .35))
        pen = pencil().scale(.80).move_to(p(-1.43, -.29))
        self.play(FadeOut(ask), FadeIn(device, shift=UP*.12), run_time=.55)
        self.play(FadeIn(page), FadeIn(pen, shift=LEFT*.17), run_time=.86)
        self.at("stand 10 to 20")
        marks = VGroup()
        for i in range(12):
            marks.add(oval(.19, .11, PAPER, 2.78 - .72 * i, -2.67 + .13 * (i % 2), -.24))
        bracket = VGroup(edge(-5.43, -3.20, 2.63, -3.20, INK, 2.8),
                         edge(-5.43, -3.07, -5.43, -3.33, INK, 2.8),
                         edge(2.63, -3.07, 2.63, -3.33, INK, 2.8))
        distance = label("10 to 20 steps", x=-1.74, y=-3.54)
        self.play(FadeOut(page), FadeOut(pen), LaggedStart(*[FadeIn(mark, shift=LEFT*.13) for mark in marks],
                                                         lag_ratio=.10), run_time=1.2)
        self.play(Create(bracket), FadeIn(distance), run_time=.67)
        self.at("take every photo")
        self.play(device.animate.move_to(p(-4.05, -.08)).scale(1.14), run_time=1.28)
        self.at("keep the whole tree")
        self.play(FadeOut(marks), FadeOut(bracket), FadeOut(distance), run_time=.28)
        finder = viewfinder()
        self.play(Create(finder), run_time=.6)
        self.finish()


class S05VisitAndPhrases(SpokenScene):
    def construct(self):
        world = landscape("Fall", moving=True)
        self.add(world)
        zoom = twig_view()
        self.at("before looking closely")
        self.play(FadeIn(zoom, scale=.34, shift=DOWN*.44), run_time=2.3)
        self.at("what do you think")
        prompt = question_card("What will it look like\nnext month?", y=1.6, color=INK, size=38, max_w=5.7)
        prompt.move_to(p(LEFT_AT, 1.6))
        self.play(FadeIn(prompt), run_time=.65)
        self.at("save the guess")
        book = notebook().move_to(p(LEFT_AT, -.57))
        sketch = book[4]
        self.play(FadeIn(VGroup(*book[:4]), shift=UP*.18), run_time=.67)
        self.at("spend about 10")
        timer = label("About 10 minutes", y=1.70)
        self.play(swap(prompt, timer), run_time=.74)
        self.at("looking at bark")
        bark_sample = limb([(-.25, -.81), (-.23, -.26), (-.32, .40), (-.18, .93)], .74, BARK)
        grain = VGroup(*[path([(-.47 + i*.10, -.58), (-.42 + i*.10, -.29), (-.50+i*.10, .13)], WOOD, 2.3)
                         for i in range(5)])
        bark = VGroup(bark_sample, grain).scale(.59).move_to(p(1.94, 1.22))
        self.play(FadeIn(bark, scale=.78), run_time=.45)
        self.at("a low twig")
        self.play(Indicate(zoom[2], color="#B07A47", scale_factor=1.03), run_time=.68)
        self.at("the weather")
        weather = VGroup(sun(-.36, .32), cloud().shift(RIGHT*.32)).scale(.53).move_to(p(3.63, 1.92))
        self.play(FadeIn(weather, shift=UP*.13), run_time=.49)
        self.at("any animals")
        animal = bird().scale(.81).move_to(p(4.57, -.85))
        self.play(FadeIn(animal, shift=p(-.52, -.32)), run_time=1.05)
        self.at("your child draws")
        pen = pencil().move_to(p(-4.19, -.74))
        self.play(FadeIn(pen), FadeOut(timer), run_time=.46)
        self.play(DrawBorderThenFill(sketch), pen.animate.shift(p(1.6, .83)), run_time=1.50)
        self.play(FadeOut(pen), run_time=.49)
        self.finish()


class S06MonthlyPattern(SpokenScene):
    def construct(self):
        self.add(landscape("Fall", moving=True))
        summer = photo("Summer", 2.66).move_to(p(-4.61, .30))
        fall = photo("Fall", 2.66).move_to(p(-1.69, .30))
        schedule = label("15 min monthly\n(or once each season)", x=-3.15, y=2.59, size=34)
        self.at("come back about")
        self.play(FadeIn(schedule), run_time=.65)
        self.play(FadeIn(summer, shift=RIGHT*.56), run_time=1.35)
        self.at("repeat the photo")
        drawing = notebook().scale(.67).move_to(fall)
        self.play(FadeIn(drawing, shift=UP*.22), run_time=.88)
        self.at("record what you saw")
        pen = pencil().scale(.68).move_to(p(-2.32, 0))
        self.play(FadeIn(pen), run_time=.34)
        self.play(pen.animate.shift(p(1.14, .42)), run_time=1.1)
        self.at("check the last guess")
        saved = oval(.30, .30, "#5B8654", -2.60, -.19)
        self.play(FadeIn(saved, scale=.62), run_time=.47)
        self.at("then compare photos")
        self.play(FadeOut(VGroup(pen, saved)), swap(drawing, fall, .83), run_time=.94)
        self.at("ask can you")
        ask = question_card("Find three differences?", color=INK, y=2.59, size=36, max_w=5.70)
        ask.move_to(p(-3.15, 2.59))
        self.play(swap(schedule, ask), run_time=.55)
        marks = [(fall.get_center() + p(-.34, .89), .30),
                 (fall.get_center() + p(.49, .79), .29),
                 (fall[2].get_center() + RIGHT*.68, .16)]
        rings = [Circle(radius=radius, color=INK, stroke_width=5.5).move_to(center) for center, radius in marks]
        self.play(LaggedStart(*[Create(ring) for ring in rings], lag_ratio=.28), run_time=.70)
        for ring in rings:
            pulse(ring, 5.5, .8, 3)
        self.finish()


class S07PredictQuestion(SpokenScene):
    def construct(self):
        world = landscape("Winter", moving=True)
        self.add(world)
        self.at("the branches are")
        thought = label("“Our tree died.”", y=1.43, size=43)
        self.play(FadeIn(thought, shift=UP*.15), run_time=.74)
        self.at("before you explain")
        zoom = twig_view(show_buds=False)
        self.play(FadeOut(thought), FadeIn(zoom, scale=.26), run_time=2.18)
        self.at("what do you predict")
        self.play(FadeIn(predict_card(), shift=UP*.10), run_time=.72)
        world[2].clear_updaters()
        specimen = zoom[2]
        self.play(Transform(world[2], landscape("Winter")[2]),
                  Rotate(specimen, .19, about_point=specimen.get_corner(DL)),
                  rate_func=there_and_back, run_time=2.5)
        world[2].become(landscape("Winter")[2])
        self.finish()


class S08PredictPause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5
    RING_AT = (-3.35, -.33, 0)

    def construct(self):
        self.add(landscape("Winter"), twig_view(show_buds=False), predict_card())
        ring, draw = countdown(self.SECONDS, center=self.RING_AT, radius=.63, color="#407B88")
        self.add(ring)
        self.play(draw)


class S09RevealBuds(SpokenScene):
    def construct(self):
        self.add(landscape("Winter", moving=True))
        zoom = twig_view()
        specimen = zoom[2]
        body, tip_bud, side_bud = specimen
        focus = specimen.get_center()
        inset_center = zoom[1].get_center()
        specimen.remove(tip_bud, side_bud)
        self.add(zoom)
        self.at("look closely at")
        buds = VGroup(tip_bud, side_bud)
        buds.scale(1.04, about_point=focus).rotate(-.32, about_point=inset_center)
        self.play(body.animate.scale(1.04, about_point=focus).rotate(-.32, about_point=inset_center), run_time=1.45)
        self.at("plump buds wait")
        tip = Circle(radius=.42, color=AMBER, stroke_width=4.5).move_to(tip_bud)
        side = Circle(radius=.35, color=AMBER, stroke_width=4.5).move_to(side_bud)
        self.play(FadeIn(tip_bud), FadeIn(side_bud), run_time=.40)
        self.play(Create(tip), run_time=.44)
        self.at("where each leaf")
        self.play(Create(side), run_time=.63)
        highlighted = VGroup(body, tip_bud, side_bud, tip, side)
        self.play(Rotate(highlighted, .32, about_point=inset_center), run_time=1.09)
        self.at("ask i wonder")
        intact = bud(4.09, 1.95).rotate(.54).move_to(p(3.52, .03))
        self.play(FadeOut(highlighted), FadeIn(intact, scale=.48), run_time=.85)
        self.at("what is inside")
        ask = question_card("What is inside this bud?", color=INK, size=36, max_w=5.75, y=1.35)
        ask.move_to(p(LEFT_AT, 1.35))
        self.play(FadeIn(ask), run_time=.70)
        self.at("do you think will")
        self.play(intact.animate.scale(1.09), run_time=1.12, rate_func=there_and_back)
        self.at("the tree is dormant")
        dormancy = label("Dormant = alive, resting", y=1.34, size=35)
        self.play(swap(ask, dormancy), run_time=.72)
        self.at("next spring's leaves")
        interior = sectioned_bud()
        self.play(FadeOut(intact), FadeIn(interior, scale=.88), run_time=.97)
        self.play(FadeIn(label("Buds hold spring leaves", y=.41, size=31)), run_time=.57)
        self.finish()


class S10WhySeasons(SpokenScene):
    def construct(self):
        world = landscape("Fall", moving=True)
        self.add(world)
        arc = path([(-5.46, 1.68), (-3.54, 2.67), (-1.52, 1.68)], "#BB883D", 3.1)
        short = path([(-5.03, 1.56), (-3.54, 2.03), (-2.07, 1.56)], "#BB883D", 3.1)
        big_sun = sun(-4.62, 1.59).scale(.80)
        temp = slab(.53, 2.02, "#F5ECD7", -3.54, -.44, .15)
        warm = slab(.21, 1.46, "#AF5143", -3.54, -.53, .08)
        bulb = oval(.45, .45, "#AF5143", -3.54, -1.41)
        self.at("shorter days and")
        self.add(arc, big_sun)
        self.play(Transform(arc, short), big_sun.animate.move_to(p(-3.54, 1.33)), run_time=1.18)
        self.at("cooler weather")
        self.play(FadeIn(temp), FadeIn(warm), FadeIn(bulb), run_time=.45)
        self.play(warm.animate.stretch(.39, 1, about_edge=DOWN), run_time=1.24)
        self.at("drop its leaves")
        change_season(self, world, "Winter", 1.8)
        self.at("warmer spring days")
        self.play(Transform(arc, path([(-5.46, 1.68), (-3.54, 2.67), (-1.52, 1.68)], "#BB883D", 3.1)),
                  big_sun.animate.move_to(p(-3.54, 1.96)),
                  warm.animate.stretch(1/.39, 1, about_edge=DOWN), run_time=.95)
        change_season(self, world, "Spring", 1.30)
        self.at("all four seasons")
        self.play(FadeOut(VGroup(arc, big_sun, temp, warm, bulb)), run_time=.41)
        seasons = list(("Spring", "Summer", "Fall", "Winter"))
        cards = VGroup()
        for season, x in zip(seasons, [-4.68, -1.56, 1.56, 4.68]):
            card = photo(season, 2.86).move_to(p(x, .22))
            cards.add(VGroup(card, label(season, x=x, y=-1.76, size=33)))
        self.play(FadeOut(world[2]), FadeOut(world[1]), FadeOut(world[0][3]),
                  LaggedStart(*[FadeIn(card, shift=UP*.39) for card in cards], lag_ratio=.31), run_time=2.43)
        self.at("look at the order")
        cycle = CurvedArrow(p(4.69, -2.35), p(-4.67, -2.35), angle=-.34, color=INK,
                            stroke_width=4, tip_length=.20)
        self.play(Create(cycle), run_time=1.53)
        self.play(cards[0][0].animate.shift(UP*.22), rate_func=there_and_back, run_time=1.50)
        self.finish()


class S11SafetyGround(SpokenScene):
    def construct(self):
        self.add(landscape("Summer", moving=True))
        self.at("stay with your child")
        pair = walk_pair().scale(.94).move_to(p(LEFT_AT, -1.56))
        self.play(FadeIn(pair, shift=RIGHT*.44), run_time=.82)
        self.at("avoid busy road")
        road = VGroup(slab(1.23, .46, "#526471", -.10, -.42, .05),
                      edge(-.57, -.42, -.30, -.42, PAPER, 3), edge(-.14, -.42, .14, -.42, PAPER, 3))
        storm = cloud("#637985").scale(.68).move_to(p(.12, .37))
        bolt = patch([(.12, .24), (-.14, -.14), (.04, -.13), (-.12, -.39), (.36, -.02), (.14, -.01)], AMBER)
        danger = safety_picture(no_sign(VGroup(road, storm, bolt)), "Avoid roads and storms")
        self.play(swap(pair, danger, .94), run_time=.94)
        self.at("storms and strong wind")
        self.play(Indicate(danger[1][0], scale_factor=1.08, color="#647989"), run_time=1.15)
        self.at("feet stay on the ground")
        ground = VGroup(edge(-1.02, -.14, 1.03, -.14, LEAF_GREEN, 4), walk_pair())
        safe = safety_picture(ground, "Feet on ground")
        self.play(swap(danger, safe, .93), run_time=.93)
        self.at("nothing goes in a mouth")
        objects = VGroup(acorn().shift(LEFT*.43), oval(.55, .39, "#657884", .41, -.27, .14),
                         oval(.37, .43, "#BB824A", .41, .28))
        risk = safety_picture(no_sign(objects), "Nothing in mouths")
        risk[0].stretch_to_fit_height(4.58).shift(DOWN*.34)
        self.play(swap(safe, risk, .95), run_time=.95)
        self.at("can choke children")
        label_risk = label("Under 4 • Choking risk", x=SAFETY_AT, y=-.81, size=32)
        self.play(swap(risk[2], label_risk), run_time=.83)
        self.at("call 911 if choking")
        help_line = label("Call 911 if choking", x=SAFETY_AT, y=-1.54, size=33, color=ALERT)
        self.play(FadeIn(help_line, shift=UP*.13), run_time=.57)
        self.finish()


class S12SafetyNature(SpokenScene):
    def construct(self):
        self.add(landscape("Summer", moving=True))
        self.at("check the trunk")
        vine = ivy().scale(.64).move_to(p(3.17, -1.69))
        first = safety_picture(ivy().scale(.73), "Leaves of three, let it be")
        self.play(FadeIn(vine), FadeIn(first[0]), FadeIn(first[1]), run_time=.72)
        self.at("for poison ivy")
        self.play(FadeIn(first[2]), run_time=.48)
        self.at("leave fallen nuts")
        nut = safety_picture(no_sign(acorn()), "Leave fallen nuts alone")
        self.play(FadeOut(vine), swap(first, nut), run_time=.86)
        self.at("with a nut allergy")
        self.play(Indicate(nut[1][0], color="#BE8150", scale_factor=1.13), run_time=1.40)
        self.at("never taste wild")
        berry = VGroup(oval(.31, .31, "#834B5B", -.70, -.01),
                       oval(.31, .31, "#834B5B", -.45, -.14),
                       leaf(LEAF_GREEN, .53, .22, .8).move_to(p(-.50, .24)))
        mushroom = VGroup(slab(.23, .65, BARK, .44, -.20, .06),
                          oval(1.01, .53, "#B4664B", .44, .23))
        wild = safety_picture(no_sign(VGroup(berry, mushroom)), "Never taste wild plants,\nberries, or mushrooms")
        self.play(swap(nut, wild), run_time=.86)
        self.at("look at insects")
        observe = safety_picture(caterpillar(), "Look, don't touch")
        self.play(swap(wild, observe), run_time=.90)
        self.play(observe[1][1].animate.scale(.94).shift(RIGHT*.10), run_time=1.46, rate_func=there_and_back)
        self.at("adults handle glass")
        glass = safety_picture(lens().scale(1.15), "Adults handle lenses")
        self.play(swap(observe, glass), run_time=.86)
        self.at("keep lenses from focusing")
        solar = sun(-4.51, 1.43).scale(.72)
        self.play(FadeIn(solar), glass[1].animate.rotate(PI / 7).shift(RIGHT*.50), run_time=1.10)
        solar_rule = label("Keep sunlight unfocused", x=SAFETY_AT, y=-.81)
        self.play(swap(glass[2], solar_rule), run_time=.74)
        self.at("never look at the sun")
        sun_rule = label("Never view the sun\nthrough a lens", x=SAFETY_AT, y=-.81)
        self.play(swap(solar_rule, sun_rule), run_time=.79)
        self.at("wash hands and check")
        clean = safety_picture(hands().scale(1.25), "Wash hands, tick check")
        self.play(FadeOut(solar), FadeOut(sun_rule), run_time=.24)
        self.play(swap(VGroup(glass[0], glass[1]), clean), run_time=.85)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        world = landscape("Fall", moving=True)
        self.add(world)
        folder = VGroup(*notebook("calendar")[:4]).move_to(p(LEFT_AT, -.5))
        mini = VGroup(*[photo(season, .71) for season in ("Spring", "Summer", "Fall", "Winter")])
        mini.arrange(RIGHT, buff=.10).move_to(p(LEFT_AT, -.42))
        self.at("by year's end")
        self.play(FadeIn(folder, shift=UP*.34), run_time=.90)
        self.play(LaggedStart(*[FadeIn(card, shift=UP*.16) for card in mini], lag_ratio=.27), run_time=1.86)
        self.at("next winter", lead=.80)
        change_season(self, world, "Winter", 1.04)
        self.at("look for buds together")
        tint = "#B57723"
        landmarks = VGroup(*[oval(.23, .23, tint, *points[-1]).shift(TREE_AT)
                             for _, points in (LIMBS[8], LIMBS[9], LIMBS[10], LIMBS[12])])
        main = world[2]
        start_angle = main.bend_angle
        landmarks.rotate(start_angle, about_point=TREE_AT)
        self.play(FadeIn(landmarks, scale=.77), run_time=.47)
        current_angle = main.bend_angle
        landmarks.rotate(current_angle - start_angle, about_point=TREE_AT)
        self.remove(landmarks)
        main.add(landmarks)
        self.at("those tiny buds")
        cover = slab(3.83, 2.64, "#AD8655", LEFT_AT, -.50)
        narrow = cover.copy().stretch(.04, 0, about_edge=LEFT)
        self.add(narrow)
        self.play(Transform(narrow, cover), run_time=.94)
        self.remove(folder, *mini)
        self.play(landmarks.animate.set_fill("#DB9A39"), run_time=.69)
        self.finish()


class S14End(EndCard):
    LINE = "Winter buds hold next spring's leaves while the tree rests."
