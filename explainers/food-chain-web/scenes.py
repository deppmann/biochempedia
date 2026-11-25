from bp_parts import *
from bp_style import EndCard

# COLOR MAP: house GOLD/YELLOW = sunlight and energy, GREEN = producers,
# BLUE/TEAL = Bay and water, RED = yarn and safety, GREY = neutral equipment.
# Dark pencil versions keep the house hues readable on cream paper.
INK = "#292A23"
CREAM = "#EAD6AC"
PAPER = "#FFF5D9"
EDGE = "#99794E"
SHADE = "#C7A775"
LEAF = "#477346"
LIGHT_LEAF = "#8EAA56"
HONEY = "#B47A22"
YARN = "#A23A38"
FIBER = "#7B5A80"
WATER = "#477F8E"
SKIN = "#BC7957"
PEACH = "#E9AB7E"
WOOD = "#77533B"
QUESTION = "If we take out the grass, who loses a food link first?"
QUESTION_STYLE = dict(y=-3.27, size=32, color=INK, max_w=10.1)


def xy(x, y):
    return np.array((x, y, 0.0))


def oval(x, y, w, h, color, tilt=0):
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=color,
                   fill_opacity=1).rotate(tilt).move_to(xy(x, y))


def cut(color, *points):
    return Polygon(*(xy(*p) for p in points), stroke_width=0, fill_color=color, fill_opacity=1)


def pencil(color, *points, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly([xy(*p) for p in points])


def round_box(w, h, color, stroke=None, radius=.12):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            fill_color=color, fill_opacity=1,
                            stroke_color=stroke or color, stroke_width=2 if stroke else 0)


def mat():
    board = round_box(12.95, 7.32, CREAM, radius=.27)
    binding = round_box(12.76, 7.13, CREAM, EDGE, radius=.22)
    return VGroup(board, binding).set_z_index(-5)


def sun():
    rays = VGroup(*[oval(.74 * np.cos(a), .74 * np.sin(a), .24, .075, HONEY, a)
                    for a in np.linspace(0, TAU, 12, endpoint=False)])
    rays.add(oval(0, 0, 1.12, 1.12, GOLD), oval(-.13, .12, .53, .49, YELLOW))
    return rays


def grass():
    return VGroup(
        oval(0, -.52, 1.83, .27, LIGHT_LEAF),
        cut(LEAF, (-.68, -.52), (-.96, .28), (-.60, .10), (-.36, -.47)),
        cut(LIGHT_LEAF, (-.42, -.51), (-.59, .71), (-.25, .40), (-.10, -.48)),
        cut(LEAF, (-.18, -.50), (.03, .82), (.24, .51), (.13, -.50)),
        cut(LIGHT_LEAF, (.10, -.51), (.52, .74), (.62, .47), (.39, -.51)),
        cut(LEAF, (.40, -.52), (.68, .12), (.99, .40), (.78, -.50)),
    )


def grasshopper():
    return VGroup(
        pencil(LEAF, (-.75, -.40), (-.63, -.02), (-.10, -.55), (.07, -.53)),
        pencil(LEAF, (.19, -.12), (.31, -.48), (.52, -.50)),
        pencil(INK, (.64, .29), (.79, .65), (.98, .69), width=2.4),
        pencil(INK, (.58, .31), (.63, .69), (.76, .80), width=2.4),
        oval(-.24, -.04, 1.43, .44, LEAF, .21),
        oval(-.35, .02, 1.13, .24, LIGHT_LEAF, .22),
        oval(.56, .20, .48, .48, LIGHT_LEAF),
        oval(.65, .28, .10, .10, INK),
        pencil(HONEY, (-.73, -.23), (-.38, .22), (.06, -.43), (.30, -.44), width=4.3),
    )


def frog():
    return VGroup(
        oval(-.58, -.26, .78, .51, LEAF, -.17), oval(.58, -.26, .78, .51, LEAF, .17),
        oval(0, -.38, 1.36, .43, LIGHT_LEAF), oval(0, .04, 1.66, .94, LEAF),
        oval(0, -.12, 1.41, .41, LIGHT_LEAF),
        oval(-.48, .37, .55, .54, LEAF), oval(.48, .37, .55, .54, LEAF),
        oval(-.49, .38, .30, .30, PAPER), oval(.49, .38, .30, .30, PAPER),
        oval(-.43, .38, .13, .17, INK), oval(.43, .38, .13, .17, INK),
        pencil(INK, (-.45, -.07), (0, -.22), (.45, -.07), width=2.4),
    )


def snake():
    points = [(-.95, -.49), (-.44, -.28), (.58, -.39), (.83, -.16),
              (.40, .04), (-.47, .03), (-.63, .29), (-.27, .48), (.26, .46)]
    return VGroup(pencil(LEAF, *points, width=15), pencil(LIGHT_LEAF, *points, width=6),
                  oval(.39, .46, .63, .37, LEAF), oval(.55, .53, .10, .1, INK))


def bird(osprey=False):
    coat = "#4F4940" if osprey else WOOD
    return VGroup(
        cut(coat, (-.18, -.11), (-1.03, .24), (-1.53, .61), (-1.19, -.02),
            (-.84, -.39), (-.39, -.57), (0, -.30), (.41, -.57), (.85, -.40),
            (1.22, -.02), (1.53, .61), (1.03, .24), (.19, -.11)),
        cut(EDGE, (-.89, -.11), (-.42, -.23), (-.22, -.40), (-.62, -.36)),
        cut(EDGE, (.89, -.11), (.42, -.23), (.22, -.40), (.62, -.36)),
        cut(coat, (-.21, -.26), (-.37, -.71), (.20, -.74), (.45, -.65), (.23, -.21)),
        oval(.02, -.08, .67, 1.05, coat, -.23),
        oval(.20, .32, .61, .48, PAPER if osprey else SHADE, -.18),
        cut(HONEY, (.40, .36), (.72, .29), (.55, .04), (.48, .17), (.39, .16)),
        oval(.29, .38, .11, .11, INK),
    )


def rabbit():
    return VGroup(
        oval(-.80, -.06, .38, .37, PAPER), oval(-.31, -.16, 1.19, .78, SHADE),
        oval(.39, .04, .82, .64, SHADE), oval(.26, .48, .25, .94, WOOD, .22),
        oval(.56, .48, .24, 1.00, SHADE, -.21), oval(.56, .53, .10, .67, PEACH, -.21),
        oval(.52, -.08, .67, .32, PAPER), oval(.61, .15, .10, .10, INK),
        oval(.88, -.03, .13, .11, WOOD), oval(.25, -.50, .77, .23, WOOD),
    )


def mouse():
    return VGroup(
        pencil(WOOD, (-.50, -.25), (-.94, -.25), (-1.13, .03), (-1.27, -.11), width=3),
        oval(-.27, -.14, 1.24, .70, GREY),
        cut(GREY, (.05, -.34), (-.01, .27), (.51, .24), (.95, -.06), (.76, -.23)),
        oval(.25, .26, .52, .51, GREY), oval(.26, .28, .33, .32, PEACH),
        oval(.61, .01, .12, .12, INK), oval(.93, -.06, .16, .12, INK),
        oval(.26, -.43, .52, .13, PEACH),
    )


def fox():
    ochre = "#AF5230"
    return VGroup(
        oval(-.56, -.12, 1.35, .51, ochre, -.26), oval(-1.00, .01, .51, .45, PAPER, -.26),
        oval(.06, -.33, 1.15, .54, ochre),
        cut(ochre, (.07, -.24), (.09, .69), (.40, .35), (.83, .68), (.81, .22), (1.15, -.18), (.75, -.44)),
        cut(PAPER, (.16, .04), (.63, -.05), (.92, -.11), (1.15, -.18), (.75, -.44), (.33, -.27)),
        oval(.69, .12, .12, .10, INK), oval(1.10, -.18, .19, .13, INK),
    )


def mushroom():
    return VGroup(
        oval(0, -.28, .49, .89, SHADE), oval(0, -.05, 1.61, .40, WOOD),
        cut(YARN, (-.81, -.05), (-.67, .37), (-.39, .65), (0, .78),
            (.39, .68), (.66, .39), (.81, -.05)),
        oval(-.34, .33, .29, .16, PAPER, .36), oval(.22, .47, .24, .16, PAPER, -.24),
        oval(.43, .17, .24, .15, PAPER, -.20),
    )


def worm():
    body = [(-1, -.25), (-.68, -.39), (-.32, -.12), (0, .34), (.31, .33), (.62, -.05), (.86, .13), (.96, .45)]
    return VGroup(pencil(WOOD, *body, width=15), pencil(PEACH, *body, width=10),
                  oval(.97, .48, .28, .34, SKIN, -.2), oval(.99, .52, .07, .07, INK))


def fish(striped=False):
    color = WATER if striped else TEAL
    body = VGroup(
        cut(color, (-.50, .04), (-1.15, .48), (-1.01, .03), (-1.17, -.43), (-.56, -.14)),
        cut(WATER, (-.36, .27), (-.18, .62), (.35, .30)),
        oval(.13, 0, 1.61, .64 if striped else .8, color),
        oval(.17, -.13, 1.36, .37, "#A6C4BC"), oval(.69, .10, .12, .12, INK),
    )
    if striped:
        body.add(*[pencil(INK, (-.45, y), (0, y + .04), (.48, y), width=2.1)
                   for y in (-.11, .04, .19)])
    else:
        body.add(oval(.39, .12, .12, .12, WATER))
    return body


def plankton(animal=False):
    if animal:
        return VGroup(
            pencil(WATER, (-.26, .06), (-.64, .54), (-1.01, .51), width=3),
            pencil(WATER, (.05, .18), (.27, .64), (.68, .65), width=3),
            cut(WATER, (-.19, -.29), (-.05, -.73), (.19, -.75), (.22, -.31)),
            oval(0, -.12, .66, .99, TEAL, .17), oval(-.05, .19, .13, .13, INK),
            *[pencil(WATER, (.21, y + .10), (.59, y), (.75, y + .11), width=2.6)
              for y in (-.48, -.27, -.05)])
    return VGroup(
        oval(-.52, .19, .40, 1.01, LEAF, .63), oval(-.50, .20, .11, .72, LIGHT_LEAF, .63),
        oval(.56, -.20, .45, .92, LEAF, -.81), oval(.55, -.18, .14, .68, LIGHT_LEAF, -.81),
        *[oval(-.20 + i * .21, -.47 + i * .24, .24, .23, LIGHT_LEAF) for i in range(5)],
    )


def tadpole():
    return VGroup(cut(WATER, (-.24, -.16), (-.69, -.01), (-1.16, .43), (-.80, .36),
                      (-.47, .15), (-.10, .17)),
                  oval(.22, -.02, 1.04, .66, WATER), oval(.49, .09, .14, .14, INK))


def dead_leaf():
    return VGroup(oval(0, 0, 1.68, .82, WOOD, .4),
                  pencil(SHADE, (-.87, -.36), (-.32, -.07), (.33, .09), (.65, .25), width=3))


ART = {
    "Sun": sun, "Grass": grass, "Grasshopper": grasshopper, "Frog": frog,
    "Snake": snake, "Hawk": bird, "Rabbit": rabbit, "Mouse": mouse, "Fox": fox,
    "Mushroom": mushroom, "Earthworm": worm, "Phytoplankton": plankton,
    "Zooplankton": lambda: plankton(True), "Menhaden": fish,
    "Striped bass": lambda: fish(True), "Osprey": lambda: bird(True),
    "Algae": plankton, "Tadpole": tadpole,
}
LAND = ("Sun", "Grass", "Grasshopper", "Frog", "Snake", "Hawk")
LAND_SPOTS = ((-4.55, 1.68), (0, 1.68), (4.55, 1.68),
              (4.55, -1.51), (0, -1.51), (-4.55, -1.51))
BAY = ("Sun", "Phytoplankton", "Zooplankton", "Menhaden", "Striped bass", "Osprey")
BAY_SPOTS = ((-4.74, 1.68), (-.69, 1.68), (3.43, 1.68),
             (0, -1.51), (-4.60, -1.51), (4.60, -1.51))
WEB_SPOTS = {
    "Sun": (-5.10, 2.50), "Grass": (-5.10, .30),
    "Grasshopper": (-2.27, 2.50), "Rabbit": (-2.27, .30), "Mouse": (-2.27, -1.77),
    "Frog": (.63, 2.50), "Snake": (.79, -1.06), "Hawk": (3.63, 2.50),
    "Fox": (4.97, .30), "Mushroom": (4.97, -1.88), "Earthworm": (1.25, -2.37),
}
WEB_SIZE = (2.34, 1.13)
DIRECT = [("Grass", n) for n in ("Grasshopper", "Rabbit", "Mouse")]
ONWARD = [
    ("Grasshopper", "Frog"), ("Frog", "Snake"), ("Frog", "Hawk"),
    ("Mouse", "Snake"), ("Mouse", "Fox"), ("Mouse", "Hawk"),
    ("Rabbit", "Fox"), ("Rabbit", "Hawk"), ("Snake", "Hawk"),
]
DEAD = [("Frog", "Mushroom"), ("Fox", "Mushroom"), ("Mouse", "Earthworm")]
WEB_LINKS = [("Sun", "Grass"), *DIRECT, *ONWARD, *DEAD]


def picture_card(name, point, w=3.04, h=2.44, size=30):
    """A single piece of illustrated paper. Artwork and writing can appear separately."""
    shadow = round_box(w, h, SHADE).shift(xy(.075, -.075)).set_z_index(2)
    paper = round_box(w, h, PAPER, EDGE).set_z_index(3)
    print_art = ART[name]()
    print_art.scale(min((w - .48) / print_art.width, (h - .73) / print_art.height))
    print_art.move_to(UP * .25).set_z_index(4)
    label = fit_text(name, max_w=w - .22, size=size, min_size=28,
                     color=INK, weight=BOLD)
    label.move_to(DOWN * (h / 2 - .125 - label.height / 2)).set_z_index(5)
    group = VGroup(shadow, paper, print_art, label).move_to(xy(*point))
    group.paper, group.art, group.label = paper, print_art, label
    return group


def land_cards():
    return {name: picture_card(name, point, w=3.18 if name == "Grasshopper" else 3.04)
            for name, point in zip(LAND, LAND_SPOTS)}


def bay_cards():
    return {name: picture_card(name, point, w=3.12 if name == "Phytoplankton" else 2.68)
            for name, point in zip(BAY, BAY_SPOTS)}


def paper_arrow(a, b, color=YARN):
    return Arrow(a, b, buff=0, color=color, stroke_width=9,
                 max_tip_length_to_length_ratio=.27, max_stroke_width_to_length_ratio=14).set_z_index(1)


def card_boundary(card, toward, pad=.12):
    box = card.paper
    diff = toward - box.get_center()
    factors = [(half + pad) / abs(d) for d, half in
               zip(diff[:2], (box.width / 2, box.height / 2)) if abs(d) > 1e-6]
    return box.get_center() + min(factors) * diff


def between(cards, a, b, color=YARN):
    start, end = cards[a], cards[b]
    return paper_arrow(card_boundary(start, end.paper.get_center()),
                       card_boundary(end, start.paper.get_center()), color)


def yarn_link(cards, a, b):
    start, end = cards[a], cards[b]
    # The long crossings thread through the open interior of the tabletop.
    guides = {
        ("Rabbit", "Hawk"): [(1.55, 1.33)],
        ("Mouse", "Hawk"): [(-.89, -.76), (-.39, -.15), (1.82, -.05), (2.70, 1.36)],
        ("Rabbit", "Fox"): [(1.51, .70), (3.28, .63)],
        ("Mouse", "Fox"): [(-.62, -.92), (-.45, -.36), (.35, -.31), (2.10, -.32), (3.30, -.13)],
        ("Frog", "Mushroom"): [(3.10, 1.25), (3.52, -.56)],
        ("Snake", "Hawk"): [(2.26, .24), (3.19, 1.72)],
        ("Mouse", "Earthworm"): [(-.82, -2.36), (-.11, -2.56)],
    }.get((a, b), [])
    mids = [xy(*point) for point in guides]
    first = card_boundary(start, mids[0] if mids else end.paper.get_center(), pad=.03)
    last = card_boundary(end, mids[-1] if mids else start.paper.get_center(), pad=.03)
    color = HONEY if a == "Sun" else FIBER if (a, b) in DEAD else YARN
    if not mids:
        middle = (first + last) / 2
        mids = [middle + DOWN * min(.17, .10 * np.linalg.norm(last - first))]
    return pencil(color, *[tuple(p[:2]) for p in [first, *mids, last]], width=4.5).set_z_index(1)


def web():
    cards = {name: picture_card(name, point, 2.71 if name == "Grasshopper" else WEB_SIZE[0],
                                WEB_SIZE[1], size=28)
             for name, point in WEB_SPOTS.items()}
    links = {edge: yarn_link(cards, *edge) for edge in WEB_LINKS}
    return cards, links


def halo(card, color=HONEY):
    outline = SurroundingRectangle(card.paper, buff=.085, corner_radius=.16,
                                   stroke_color=color, stroke_width=5).set_z_index(6)
    return outline


def trace(link, color=YELLOW, width=9):
    return ShowPassingFlash(link.copy().set_stroke(color, width=width).set_z_index(2),
                            time_width=.40)


def light_card(card, color="#ECCD82"):
    return card.paper.animate(rate_func=there_and_back).set_fill(color)


def fan(cards, links):
    return VGroup(*links.values(), *cards.values())


def yarn_ball():
    body = VGroup(oval(0, 0, 1.67, 1.59, YARN))
    for y in (-.48, -.23, .03, .28, .49):
        reach = .76 * np.sqrt(1 - (y / .82) ** 2)
        body.add(pencil(PEACH, (-reach, y - .02), (-reach / 2, y + .14),
                        (reach / 2, y - .12), (reach, y), width=2.5))
    body.add(pencil(YARN, (.53, -.54), (.99, -.72), (1.32, -.48), (1.72, -.60), width=5))
    return body


def blank_cards(count=3):
    return VGroup(*[round_box(1.82, 1.32, PAPER, EDGE).rotate(.24 - .034 * i)
                    .shift(xy(.068 * i, -.051 * i)) for i in range(count)])


def crayon(color=YARN):
    return VGroup(cut(color, (-.80, -.15), (.48, -.15), (.84, 0), (.48, .15), (-.80, .15)),
                  round_box(.88, .28, PAPER, radius=.03).shift(LEFT * .11))


def supplies_crayons():
    return VGroup(crayon(YARN).rotate(.57).shift(LEFT * .53 + UP * .31),
                  crayon(LEAF).rotate(.17).shift(DOWN * .19),
                  crayon(WATER).rotate(-.41).shift(RIGHT * .50 + DOWN * .42))


def tape():
    return VGroup(oval(.06, -.10, 1.34, 1.17, EDGE), oval(0, 0, 1.36, 1.20, GOLD),
                  oval(0, 0, .77, .67, CREAM),
                  cut(GOLD, (.46, .39), (1.10, .21), (1.02, -.11), (.66, -.06)))


def clips():
    clip = pencil(WATER, (-.41, .06), (-.39, -.43), (.15, -.47), (.31, -.22),
                  (.31, .46), (.05, .63), (-.11, .46), (-.11, -.20), (.11, -.21),
                  (.12, .29), width=4.5)
    return VGroup(clip.copy().rotate(.55).shift(LEFT * .38),
                  clip.rotate(-.49).shift(RIGHT * .44))


def scissors():
    return VGroup(
        cut(GREY, (-.10, -.08), (.99, .62), (1.32, .65), (1.04, .28), (.16, -.28)),
        cut("#606B72", (-.12, .10), (1.08, -.42), (1.36, -.69), (.89, -.65), (.01, -.11)),
        Circle(radius=.30, stroke_color=YARN, stroke_width=11).move_to(xy(-.53, .34)),
        Circle(radius=.30, stroke_color=YARN, stroke_width=11).move_to(xy(-.56, -.34)),
        pencil(YARN, (-.33, .26), (-.17, .17), (0, 0), width=8),
        pencil(YARN, (-.33, -.23), (-.17, -.16), (0, 0), width=8),
        oval(.04, -.01, .18, .18, WOOD),
    )


def hand(color=PEACH, sleeve=WATER):
    """Open hand viewed from above, wrist below the palm."""
    return VGroup(
        round_box(.75, .81, sleeve).shift(DOWN * .85),
        oval(0, -.23, .82, 1.08, color), oval(-.44, -.14, .36, .74, color, .62),
        oval(-.29, .48, .24, .93, color, .15), oval(-.03, .58, .23, 1.04, color, .03),
        oval(.21, .50, .23, .92, color, -.12), oval(.41, .30, .21, .68, color, -.21),
    )


def crayon_hand(color=PEACH, sleeve=WATER):
    return VGroup(hand(color, sleeve), crayon(LEAF).rotate(.65).shift(UP * .40))


class TableScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(mat())

    def show_card(self, card, seconds=.44):
        self.play(FadeIn(VGroup(card[0], card.paper, card.art), shift=DOWN * .09),
                  run_time=seconds * .65)
        self.play(FadeIn(card.label), run_time=seconds * .35)
        self.remove(*card)
        self.add(card)


def hook_cards():
    return (picture_card("Grass", (-3.8, -.73), 3.47, 3.32, 36),
            picture_card("Hawk", (3.8, -.73), 3.47, 3.32, 36),
            picture_card("Sun", (0, 2.10), 2.27, 1.94, 30))


class S01Hook(TableScene):
    def construct(self):
        grass_card, hawk_card, sun_card = hook_cards()
        dots = VGroup(*[Dot(xy(x, .93 - .095 * x * x), radius=.047, color=EDGE)
                        for x in np.linspace(-1.92, 1.92, 17)])
        mark = T("?", 50, HONEY, font=TITLE_FONT).move_to(xy(0, .34))
        self.add(grass_card, hawk_card, sun_card)
        bob(grass_card.art, amp=.095, speed=2.1)
        bob(sun_card.art, amp=.074, speed=1.8)
        self.at("why does a hawk")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=.075),
                  FadeIn(mark), run_time=1.15)
        ball = yarn_ball().move_to(xy(0, -1.40))
        self.at("picture cards and yarn")
        self.play(FadeIn(ball, shift=RIGHT * .18), run_time=.65)
        bob(ball, amp=.13, speed=1.7)
        self.at("looking closely")
        self.play(Indicate(grass_card.paper, color=HONEY, scale_factor=1.035), run_time=1.05)
        self.at("sorting living things")
        self.play(Indicate(hawk_card.paper, color=HONEY, scale_factor=1.035), run_time=.95)
        self.at("testing a guess")
        self.play(Indicate(mark, color=YARN, scale_factor=1.23), run_time=1.2)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Who Eats Whom?"
    TITLE = "Who Eats Whom?: Parent Guide"

    def construct(self):
        grass_card, hawk_card, sun_card = hook_cards()
        self.add(mat(), grass_card, hawk_card, sun_card)
        main, subtitle = self.TITLE.split(": ", 1)
        title = T(main, 59, INK, font=TITLE_FONT).move_to(UP * .21).set_z_index(5)
        sub = T(subtitle, 33, HONEY, weight=BOLD).move_to(DOWN * .69).set_z_index(5)
        banner = round_box(7.50, 2.25, PAPER, EDGE, radius=.19).set_z_index(4)
        glints = VGroup(*[Dot(xy(x, y), radius=.033, color=HONEY)
                          for x, y in [(-2.1, 2.45), (-1.8, 2.05), (1.65, 2.18), (2.03, 2.62)]])
        for i, dot in enumerate(glints):
            bob(dot, amp=.14, speed=2.1, seed=i)
        self.add(glints)
        self.play(grass_card.animate.shift(LEFT * .86), hawk_card.animate.shift(RIGHT * .86),
                  FadeIn(banner), run_time=.60)
        self.play(FadeIn(title, shift=UP * .10), FadeIn(sub), run_time=.49)
        self.wait(max(.1, self.narration_s - self.elapsed()))


class S03Materials(TableScene):
    def construct(self):
        layout = [
            ("12 to 18 index cards", blank_cards(12), (-4.31, 1.56)),
            ("Crayons or markers", supplies_crayons(), (0, 1.56)),
            ("Ball of yarn", yarn_ball(), (4.28, 1.56)),
            ("Tape or paper clips", VGroup(tape(), clips()).arrange(RIGHT, buff=.24), (-3.95, -1.79)),
            ("Adult scissors", scissors(), (3.95, -1.79)),
        ]
        items = []
        for label, drawing, point in layout:
            fit(drawing.scale(1.18), max_w=3.03, max_h=1.65).move_to(xy(*point))
            items.append((drawing, T(label, 29, INK, weight=BOLD).next_to(drawing, DOWN, buff=.24)))
        first, *rest = items
        self.add(first[0])
        self.at("gather")
        self.play(Wiggle(first[0], scale_value=1.06, rotation_angle=.08), run_time=.75)
        self.at("index cards")
        self.play(FadeIn(first[1]), run_time=.40)
        for cue, (drawing, label) in zip(("crayons or markers", "ball of yarn", "tape or paper clips"), rest):
            self.at(cue, lead=.55)
            self.play(FadeIn(drawing, shift=DOWN * .23), run_time=.48)
            self.play(FadeIn(label), run_time=.33)
        self.at("clear floor or table")
        space = DashedVMobject(round_box(2.5, 1.68, CREAM).set_fill(opacity=0).set_stroke(EDGE, 3)
                              .move_to(xy(0, -1.59)), num_dashes=28)
        self.play(Create(space), run_time=.73)
        self.at("and scissors", lead=.25)
        self.play(FadeIn(rest[-1][0], shift=DOWN * .19), run_time=.48)
        self.play(FadeIn(rest[-1][1]), run_time=.30)
        self.at("review the yarn")
        ball = rest[1][0]
        self.play(Rotate(ball, angle=-.48, rate_func=there_and_back),
                  rest[1][1].animate(rate_func=there_and_back).set_color(YARN),
                  run_time=1.48)
        self.finish()


class S04LandChain(TableScene):
    def construct(self):
        cards = land_cards()
        adult = crayon_hand(SKIN).scale(.79).rotate(-.8).move_to(xy(-2.34, .07)).set_z_index(5)
        child = crayon_hand(PEACH, LEAF).scale(.65).rotate(.75).move_to(xy(2.26, .06)).set_z_index(5)
        self.add(adult, child)
        for name, cue in zip(LAND, ("cards for sun", "sun grass", "grasshopper frog", "frog snake",
                                    "snake and hawk", "and hawk")):
            self.at(cue)
            self.show_card(cards[name], .40 if name != "Snake" else .32)
        self.at("line them up")
        self.play(FadeOut(adult, shift=LEFT * .66), FadeOut(child, shift=RIGHT * .66),
                  LaggedStart(*[Indicate(c.paper, color=HONEY, scale_factor=1.03)
                                for c in cards.values()], lag_ratio=.17), run_time=1.7)
        links = [between(cards, a, b, HONEY if a == "Sun" else YARN) for a, b in zip(LAND, LAND[1:])]
        self.play(GrowArrow(links[0]), run_time=.55)
        self.at("where does the grass")
        focus = VGroup(halo(cards["Grass"]), halo(cards["Grasshopper"]))
        self.play(Create(focus), run_time=.48)
        for ring in focus:
            pulse(ring, base=5, amp=2.8, speed=2.9)
        self.at("point the arrow")
        # The paper arrow occupies the open gap, enlarged as it lands toward the eater.
        self.play(GrowArrow(links[1]), run_time=.85)
        self.play(Indicate(links[1], color=YARN, scale_factor=1.20), run_time=.95)
        for ring in focus:
            ring.clear_updaters()
        self.play(FadeOut(focus), run_time=.23)
        self.at("first arrow shows")
        self.play(trace(links[0]), run_time=1.05)
        self.play(LaggedStart(*[GrowArrow(line) for line in links[2:]], lag_ratio=.45),
                  run_time=2.02)
        self.finish()


class S05RolesAndBay(TableScene):
    def construct(self):
        land = land_cards()
        arrows = [between(land, a, b, HONEY if a == "Sun" else YARN) for a, b in zip(LAND, LAND[1:])]
        old = VGroup(*arrows, *land.values())
        self.add(old)
        self.at("grass makes food")
        producer = T("Producer", 32, LEAF, weight=BOLD).move_to(xy(-.88, .08)).set_z_index(5)
        glow = halo(land["Grass"], LEAF)
        self.play(Create(glow), trace(arrows[0]), run_time=.98)
        self.play(FadeIn(producer), run_time=.39)
        self.at("animals are consumers")
        rings = VGroup(*[halo(land[n], YARN) for n in LAND[2:]])
        consumers = T("Consumers", 32, YARN, weight=BOLD).move_to(xy(-.88, .08)).set_z_index(5)
        self.play(FadeOut(glow), swap(producer, consumers), Create(rings), run_time=.85)
        self.at("mushrooms break down", lead=.40)
        self.play(FadeOut(old), FadeOut(rings), FadeOut(consumers), run_time=.34)
        mush = picture_card("Mushroom", (2.52, .05), 3.68, 3.97, 35)
        debris = dead_leaf().scale(1.52).move_to(xy(-2.51, .04))
        self.play(FadeIn(debris, shift=DOWN * .16), run_time=.42)
        self.show_card(mush, .57)
        self.play(Wiggle(debris, scale_value=1.09, rotation_angle=.11), run_time=1.2)
        self.at("for the bay chain")
        self.play(FadeOut(debris), FadeOut(mush), run_time=.48)
        cards = bay_cards()
        for i, cue in enumerate(("draw sun", "phytoplankton", "zooplankton", "menhaden in that")):
            self.at(cue, lead=.34)
            self.show_card(cards[BAY[i]], .42)
            if i:
                self.play(GrowArrow(between(cards, BAY[i-1], BAY[i], HONEY if i == 1 else WATER)),
                          run_time=.40)
        self.at("from menhaden")
        self.play(Create(halo(cards["Menhaden"], WATER), remover=True), run_time=.74)
        self.at("to striped bass", lead=.53)
        self.show_card(cards["Striped bass"], .44)
        self.play(GrowArrow(between(cards, "Menhaden", "Striped bass", WATER)), run_time=.52)
        self.at("another to osprey", lead=.27)
        self.show_card(cards["Osprey"], .44)
        self.play(GrowArrow(between(cards, "Menhaden", "Osprey", WATER)), run_time=.58)
        self.finish()


class S06YarnWeb(TableScene):
    def construct(self):
        cards, links = web()
        land = land_cards()
        self.add(*land.values())
        self.at("add rabbit")
        # Slide the same land drawings from the line into their places in the web.
        self.play(*[FadeOut(card.label) for card in land.values()], run_time=.18)
        source = [VGroup(*land[n][:3]) for n in LAND]
        target = [VGroup(*cards[n][:3]) for n in LAND]
        self.remove(*land.values(), *[part for card in land.values() for part in card])
        self.add(*source)
        self.play(*[ReplacementTransform(a, b, path_arc=.15 if i % 2 else -.15)
                    for i, (a, b) in enumerate(zip(source, target))], run_time=.47)
        self.play(*[FadeIn(cards[n].label) for n in LAND], run_time=.18)
        self.remove(*target, *[cards[n].label for n in LAND])
        self.add(*[cards[n] for n in LAND])
        for name, cue in zip(("Rabbit", "Mouse", "Fox", "Mushroom", "Earthworm"),
                             ("rabbit", "mouse", "fox", "mushroom", "and earthworm")):
            self.at(cue, lead=.18)
            self.show_card(cards[name], .38)
        first_hand = hand(SKIN).scale(.72).rotate(-1.3).move_to(xy(-4.25, -1.39))
        other_hand = hand(PEACH, LEAF).scale(.68).rotate(1.9).move_to(xy(2.40, .66))
        loose = pencil(YARN, (-4.83, -1.48), (-4.28, -1.40), (-3.99, -1.59),
                       (-3.51, -1.52), width=5).set_z_index(2)
        self.at("each person holds")
        self.play(FadeIn(first_hand, shift=LEFT * .30), FadeIn(other_hand, shift=RIGHT * .35),
                  Create(loose), run_time=.75)
        self.play(Indicate(cards["Grass"].paper, color=LEAF, scale_factor=1.03), run_time=.83)
        self.at("start at grass")
        self.play(FadeOut(first_hand), FadeOut(other_hand), FadeOut(loose),
                  Create(links[("Sun", "Grass")]), run_time=.39)
        self.play(LaggedStart(*[Create(links[key]) for key in DIRECT], lag_ratio=.37),
                  run_time=1.30)
        self.play(LaggedStart(*[Create(links[key]) for key in ONWARD], lag_ratio=.23),
                  run_time=2.45)
        self.at("link living cards", lead=0)
        self.play(LaggedStart(*[Create(links[key]) for key in DEAD], lag_ratio=.45),
                  run_time=1.95)
        dead = T("Dead material", 28, FIBER, weight=BOLD).move_to(xy(4.26, -3.10))
        self.play(FadeIn(dead), run_time=.48)
        self.at("overlapping chains")
        self.play(FadeOut(dead), run_time=.33)
        for key in (DIRECT[0], ONWARD[0], ONWARD[2]):
            self.play(trace(links[key], color=HONEY, width=13), light_card(cards[key[1]]),
                      run_time=.74)
        self.finish()


class S07TugAndPredict(TableScene):
    def construct(self):
        cards, links = web()
        self.add(fan(cards, links))
        frog_strand = links[("Frog", "Snake")]
        mouse_strand = links[("Mouse", "Snake")]
        grip = frog_strand.point_from_proportion(.68)
        snake_hand = hand(SKIN).scale(.52).rotate(PI / 2).set_z_index(6)
        middle_fingertip = snake_hand[4].get_left()
        snake_hand.shift(grip - middle_fingertip + LEFT * .08)
        raise_hand = hand(PEACH, LEAF).scale(.91).rotate(-.20).move_to(xy(-4.67, -1.98))
        self.at("snake holder give")
        self.play(FadeIn(snake_hand, shift=UP * .19), run_time=.48)
        tug = LEFT * .25
        pair = [(frog_strand, grip), (mouse_strand, mouse_strand.point_from_proportion(.52))]
        slack = [pencil(YARN, *[tuple(p[:2]) for p in [strand.get_start(), hold + tug, strand.get_end()]],
                        width=4.5).set_z_index(1) for strand, hold in pair]
        self.at("one gentle tug")
        self.play(snake_hand.animate.shift(tug),
                  cards["Snake"].paper.animate.set_fill("#D9A35A"),
                  *[Transform(strand, bent) for (strand, _), bent in zip(pair, slack)],
                  rate_func=there_and_back, run_time=1.40)
        self.at("anyone who feels")
        self.play(FadeOut(snake_hand), FadeIn(raise_hand, shift=DOWN * .42), run_time=.75)
        self.play(raise_hand.animate.shift(UP * .45), run_time=.95)
        self.at("now look at")
        focus = halo(cards["Grass"], LEAF)
        self.play(FadeOut(raise_hand, shift=DOWN * .34), Create(focus), run_time=.67)
        self.play(Indicate(cards["Grass"].art, color=LEAF, scale_factor=1.15),
                  light_card(cards["Grass"], "#A9BE74"), run_time=1.05)
        self.at("if we take")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=.50)
        pulse(focus, base=5, amp=3.1, speed=3.3)
        self.at("food link first", lead=0)
        self.play(cards["Grass"].paper.animate.set_fill("#A9BE74"), run_time=1.25)
        focus.clear_updaters().set_stroke(width=5)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5
    RING_AT = (5.72, -3.04, 0)

    def backdrop(self):
        cards, links = web()
        return VGroup(mat(), fan(cards, links), halo(cards["Grass"], LEAF))

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, fill = countdown(self.SECONDS, center=self.RING_AT, color=HONEY)
        ring[0].set_fill(opacity=0)
        self.add(ring)
        self.play(fill, rate_func=lambda progress: 1 - progress)


class S09RevealAndTadpole(TableScene):
    def construct(self):
        cards, links = web()
        focus = halo(cards["Grass"], LEAF)
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(fan(cards, links), focus, question)
        self.at("take out the grass")
        self.play(FadeOut(question), FadeOut(focus),
                  FadeOut(cards["Grass"], shift=UP * .50),
                  FadeOut(links[("Sun", "Grass")]), run_time=.83)
        self.at("trace the links")
        direct = VGroup(*[links[key] for key in DIRECT])
        for a, b in DIRECT:
            self.play(trace(links[(a, b)], color=HONEY),
                      Indicate(cards[b].paper, color=HONEY, scale_factor=1.045), run_time=1.04)
        self.at("then follow their")
        self.play(FadeOut(direct), run_time=.38)
        for names in (("Frog",), ("Snake", "Fox"), ("Hawk",)):
            paths = [trace(links[key], color=HONEY, width=13) for key in ONWARD if key[1] in names]
            self.play(*paths, *[light_card(cards[name]) for name in names], run_time=.91)
        self.at("the yarn shows")
        self.play(trace(links[ONWARD[0]], color=HONEY, width=13), light_card(cards["Frog"]),
                  run_time=.98)
        self.play(trace(links[ONWARD[1]], color=HONEY, width=13), light_card(cards["Snake"]),
                  run_time=.98)
        self.at("place a tadpole", lead=.48)
        stays = VGroup(*[card for name, card in cards.items() if name != "Grass"],
                       *[link for key, link in links.items() if key not in DIRECT and key[0] != "Sun"])
        self.play(FadeOut(stays), run_time=.44)
        algae = picture_card("Algae", (-4.23, .12), 3.36, 3.85, 36)
        young = picture_card("Tadpole", (0, .12), 3.36, 3.85, 36)
        self.add(algae)
        self.show_card(young, .52)
        self.at("most tadpoles eat")
        meal = between({"Algae": algae, "Tadpole": young}, "Algae", "Tadpole", LEAF)
        bits = VGroup(dead_leaf().scale(.38), dead_leaf().scale(.24)).arrange(RIGHT, buff=.08)
        bits.move_to(xy(-4.25, -2.52))
        self.play(GrowArrow(meal), light_card(algae, "#D1DC99"), run_time=.73)
        self.at("and plant bits")
        self.play(FadeIn(bits, shift=UP * .19), light_card(young, "#C3DCDC"), run_time=.95)
        bob(young.art, amp=.16, speed=2.6)
        self.at("adult frogs eat", lead=.53)
        adult = picture_card("Frog", (4.24, .12), 3.36, 3.85, 36)
        self.show_card(adult, .57)
        insect = grasshopper().scale(.58).move_to(xy(4.23, -2.71))
        up = paper_arrow(xy(4.23, -2.37), xy(4.23, -1.96), HONEY)
        self.play(FadeIn(insect), GrowArrow(up), run_time=.65)
        self.finish()


def small_supplies():
    caps = VGroup(round_box(.33, .66, WATER).rotate(.49),
                  round_box(.33, .66, LEAF).rotate(-.30).shift(RIGHT * .52))
    scraps = VGroup(cut(HONEY, (-.39, -.17), (.07, -.24), (.08, .11), (-.35, .23)),
                    cut(YARN, (.18, -.27), (.60, -.10), (.50, .23), (.14, .11)))
    string = pencil(FIBER, (-.94, -.20), (-.52, -.33), (-.43, .39),
                    (.29, .49), (.45, -.12), (.07, -.24), (.73, -.33), width=5)
    return [yarn_ball(), string, tape(), clips(), caps, scraps]


def sink():
    basin = round_box(6.3, 4.72, "#ADBFC0", WATER, radius=.75)
    inset = round_box(5.73, 4.15, "#BBD4CF", radius=.63)
    faucet = VGroup(oval(0, 2.22, 1.33, .62, "#77888C"),
                    round_box(.61, 1.13, "#546F78", radius=.23).move_to(UP * 1.82),
                    oval(0, 1.37, .64, .34, WATER))
    return VGroup(faucet[0], basin, inset, faucet[1], faucet[2]).move_to(xy(.50, .05))


def safety_label(words):
    return T(words, 34, INK, weight=BOLD).move_to(DOWN * 2.90).set_z_index(5)


class S10Safety(TableScene):
    def construct(self):
        adult = hand(SKIN).scale(1.45).rotate(-.84).move_to(xy(-3.39, -.28))
        child = hand(PEACH, LEAF).scale(.99).rotate(.72).move_to(xy(4.41, -.29))
        shears = scissors().scale(1.27).move_to(xy(-1.90, .57))
        paper = round_box(2.50, 2.60, PAPER, EDGE).rotate(-.08).move_to(xy(.83, .36))
        cap = safety_label("Adults do the cutting")
        self.add(adult, child, paper, shears)
        self.at("stay with your child")
        self.play(child.animate.shift(LEFT * .37), run_time=1.30)
        self.at("do all the cutting")
        self.play(shears.animate.shift(RIGHT * .65), FadeIn(cap), run_time=.92)
        self.play(Indicate(shears, color=YARN, scale_factor=1.06), run_time=.75)
        self.at("hold yarn loosely", lead=.48)
        cutting = VGroup(adult, child, paper, shears)
        open_hand = hand(SKIN).scale(1.62).rotate(-.16).move_to(xy(-.4, .20))
        strand = pencil(YARN, (-4.57, .82), (-2.89, .22), (-1.69, .37),
                        (-.27, .82), (1.17, .64), (2.32, .04), (4.16, .49), width=8)
        open_label = safety_label("Hold yarn loosely")
        self.play(FadeOut(cutting, shift=LEFT * .18), FadeIn(open_hand), Create(strand),
                  swap(cap, open_label), run_time=.77)
        self.at("keep it off necks")
        neck = safety_label("Keep yarn off necks")
        self.play(swap(open_label, neck), run_time=.65)
        self.play(Indicate(strand, color=YARN, scale_factor=1.04), run_time=.84)
        self.at("never wrap it tightly")
        fingers = safety_label("Keep fingers and wrists free")
        self.play(swap(neck, fingers),
                  open_hand.animate.rotate(.30), run_time=.73)
        self.play(trace(strand, PEACH, 11), run_time=1.30)
        self.at("hand the ball over", lead=.35)
        self.play(FadeOut(VGroup(open_hand, strand, fingers)), run_time=.33)
        hands = VGroup(hand(SKIN).scale(1.23).rotate(-1.08).move_to(xy(-3.24, -.18)),
                       hand(PEACH, LEAF).scale(1.08).rotate(1.14).move_to(xy(3.18, -.17)))
        ball = yarn_ball().scale(1.09).move_to(xy(-2.10, .49))
        self.play(FadeIn(hands), FadeIn(ball), run_time=.43)
        self.play(ball.animate.move_to(xy(1.66, .43)), run_time=1.22)
        self.at("stay still while")
        still = safety_label("Stay still with yarn")
        self.play(FadeIn(still), run_time=.41)
        self.at("clear yarn and")
        pile = blank_cards().move_to(xy(0, 1.73))
        self.play(FadeOut(still), FadeIn(pile), run_time=.45)
        self.play(VGroup(ball, pile, hands[0]).animate.shift(LEFT * 1.47),
                  FadeOut(hands[1]), run_time=1.48)
        self.at("if you work outside")
        self.play(FadeOut(VGroup(*hands, pile, ball)), run_time=.52)
        tap = sink()
        wash = VGroup(hand(SKIN).scale(.94).rotate(-1.05).move_to(xy(-.12, -.45)),
                      hand(PEACH).scale(.89).rotate(.94).move_to(xy(1.09, -.49)))
        self.play(FadeIn(tap), run_time=.55)
        self.at("wash hands with")
        spray = VGroup(*[pencil(WATER, (.50 + dx, 1.49), (.50 + dx, .91),
                                (.57 + dx, .43), width=3.3) for dx in (-.13, 0, .13)])
        bar = round_box(.74, .42, "#F7E3A3").rotate(-.16).move_to(xy(2.43, .88))
        lather = VGroup(*[oval(x, y, d, d, PAPER) for x, y, d in
                         [(.18, .19, .31), (.40, .12, .42), (.65, .21, .30),
                          (.61, -.14, .34), (.30, -.14, .31), (.81, .37, .17)]])
        self.play(FadeIn(wash), Create(spray), FadeIn(bar), run_time=.63)
        self.play(FadeIn(lather), wash.animate.shift(UP * .13), run_time=.55)
        bob(lather, amp=.15, speed=4)
        self.finish()


class S10Choking(TableScene):
    def construct(self):
        supplies = small_supplies()
        points = ((-4.34, 1.63), (0, 1.63), (4.27, 1.63),
                  (-4.34, -.90), (0, -.90), (4.27, -.90))
        for item, point in zip(supplies, points):
            item.scale_to_fit_width(1.85).move_to(xy(*point))
        self.add(supplies[0])
        self.at("yarn string")
        self.play(FadeIn(supplies[1]), run_time=.79)
        for cue, item in zip(("tape paper clips", "paper clips marker",
                              "marker caps", "small crayon pieces"), supplies[2:]):
            self.at(cue)
            self.play(FadeIn(item, shift=DOWN * .15), run_time=.43)
        self.at("choking hazards")
        warning = safety_label("Choking hazard: under four.")
        self.play(FadeIn(warning), run_time=.51)
        self.at("keep them away")
        grown = hand(SKIN).rotate(-PI / 2).scale(1.1).move_to(xy(-4.93, .91))
        self.play(FadeIn(grown, shift=LEFT * .24), run_time=.52)
        tray = VGroup(*supplies)
        self.play(tray.animate.scale(.65).move_to(xy(2.74, 1.32)),
                  grown.animate.shift(RIGHT * 3.25 + UP * .26), run_time=1.58)
        self.at("call 911")
        emergency = safety_label("Call 911 if choking")
        self.play(swap(warning, emergency), FadeOut(grown), run_time=.77)
        self.finish()


class S11Takeaway(TableScene):
    def construct(self):
        cards, links = web()
        self.add(fan(cards, links))
        self.at("through this game")
        grass_focus = halo(cards["Grass"], LEAF)
        self.play(Create(grass_focus), run_time=.65)
        self.at("asking what happens")
        self.play(*[light_card(cards[key[1]], "#D6DCA9") for key in DIRECT],
                  *[trace(links[key], color=HONEY, width=12) for key in DIRECT], run_time=1.64)
        self.at("checking a guess")
        for names in (("Frog", "Snake"), ("Fox", "Hawk")):
            paths = [trace(links[key], color=HONEY, width=13) for key in ONWARD if key[1] in names]
            self.play(*paths, *[light_card(cards[name]) for name in names], run_time=1.33)
        self.at("one gentle tug", lead=.50)
        self.play(trace(links[("Sun", "Grass")], color=YELLOW, width=12),
                  light_card(cards["Sun"]), light_card(cards["Grass"]), run_time=.80)
        self.play(*[trace(links[key], color=YELLOW, width=13) for key in DIRECT],
                  *[light_card(cards[key[1]]) for key in DIRECT], run_time=.85)
        self.play(*[trace(links[key], color=YELLOW, width=13) for key in [*ONWARD, *DEAD]],
                  light_card(cards["Frog"]), light_card(cards["Fox"]), run_time=1.12)
        self.at("and grass", lead=.22)
        self.play(Create(halo(cards["Hawk"], HONEY)), light_card(cards["Hawk"]),
                  light_card(cards["Grass"]), run_time=1.27)
        self.finish()


class S12End(EndCard):
    LINE = "Food webs show how energy moves through overlapping food chains."
