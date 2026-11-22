"""Cell adhesion, mechanics and migration in a single schematic live-cell chamber.

Color map from the patch-clamp film: blue marks cells and the apparatus, grey
marks structure, purple marks receptors, yellow marks force and actin motion,
green marks attachment, red marks a stalled step, pink marks adaptors and
linkers, orange marks added dye and dyed cells,
teal marks tissue, and gold marks study dates and the prediction.
"""
from bp_parts import *  # noqa: F403

PURPLE = "#B58CD9"
PINK = "#F195C5"
ORANGE = "#F29E4C"
CHAMBER = "#1D2E3D"
GEL = "#3A566A"
QUESTION = "Stronger adhesion: faster crawling, or slower?"
QUESTION_STYLE = dict(y=3.18, size=34)

COMPACT = [(-1.06, -0.78), (0.49, -0.83), (-0.35, 0.56), (1.14, 0.57)]
SINGLE = [(-4.5, -0.72), (3.85, -0.78), (-2.45, 1.3), (2.05, 1.38)]
HOOK_OPEN = [(-5.05, -0.85), (-3.55, -0.94), (-4.75, 0.86)]
HOOK_CLOSED = [(-4.83, -0.72), (-3.48, -0.67), (-4.14, 0.48)]


def p(x, y):
    return np.array([x, y, 0.0])


def curve(points, color, width=3, fill=None, opacity=1):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_smoothly([p(*xy) for xy in points])
    if fill:
        m.close_path()
        m.set_fill(fill, opacity)
    return m


def arr(a, b, color=YELLOW, width=5):
    return Arrow(p(*a), p(*b), buff=0, color=color, stroke_width=width, tip_length=0.19,
                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=12)


def heading(text, color=TEXT, size=34, x=0):
    return T(text, size, color).move_to(p(x, 3.16))


def plaque(text, color=TEXT, x=0, y=-3.15):
    return T(text, 30, color).move_to(p(x, y))


def chamber():
    return RoundedRectangle(width=13, height=5.5, corner_radius=0.26, stroke_color=GEL,
                            stroke_width=2, fill_color=CHAMBER, fill_opacity=1).set_z_index(-4)


def substrate(pull=0, center=0):
    """Gel cross-section with fiducial lines bent inwards by opposing traction."""
    top, bottom = -1.51, -2.56
    base = RoundedRectangle(width=12.5, height=top - bottom, corner_radius=0.11,
                            stroke_width=2, stroke_color=GREY, fill_color=GEL,
                            fill_opacity=1).move_to(p(0, (top + bottom) / 2))
    grid = VGroup(base)
    for x in np.linspace(-6, 6, 29):
        local = x - center
        bend = pull * local * np.exp(-((abs(local) - 1.65) / 1.12) ** 2)
        grid.add(curve([(x, bottom + 0.02), (x - 0.11 * bend, -2.23),
                        (x - 0.55 * bend, -1.89), (x - bend, top - 0.02)], GREY, 1.25))
    for y in (-2.22, -1.88):
        grid.add(Line(p(-6.23, y), p(6.23, y), color=GREY, stroke_width=1.2))
    return grid


def cell(x, y, r=0.76, dye=False):
    membrane = ORANGE if dye else BLUE
    angle = np.linspace(0, TAU, 25)
    rim = [(x + r * (1 + 0.055 * np.cos(3 * a + 0.5)) * np.cos(a),
            y + r * (1 + 0.055 * np.cos(3 * a + 0.5)) * np.sin(a)) for a in angle]
    return VGroup(
        curve(rim, membrane, 4.0, interpolate_color(ManimColor(BG), ManimColor(membrane), 0.36)),
        curve([(x + r * a, y + r * b) for a, b in [(-.63, .25), (-.49, .53), (-.2, .68)]],
              membrane, 2.5).set_stroke(opacity=.66),
        Circle(radius=.28 * r, stroke_color=membrane, stroke_width=2,
               fill_color=membrane, fill_opacity=.44).move_to(p(x + .1 * r, y - .04 * r)),
    )


def colony(points, r=.76):
    return VGroup(*(cell(x, y, r) for x, y in points))


def breathe(col, amp=.095):
    for i, c in enumerate(col):
        bob(c, amp=amp, speed=2.8, seed=i + 1)


def crawler(front=0, rear=0, grip=.65, flow=0, phase=0, stretch=False):
    """One side-on cell. Pad coordinates stay fixed when the leading edge extends."""
    pad_y = -1.39
    outlines = [(-3.28 + rear, -1.04), (-2.55 + rear, -0.34),
                (-1.89 + rear * .6, 1.16), (-.94 + rear * .45, 1.91),
                (.1, 2.00), (1.42 + front * .45, 1.24),
                (2.72 + front, -.3), (3.02 + front, -1.21),
                (2.41 + front * .3, -1.37), (0.37, -1.27),
                (-1.7 + rear * .8, -1.31), (-3.28 + rear, -1.04)]
    body = curve(outlines, BLUE, 5, "#234850")
    nucleus = Ellipse(width=1.28, height=.94, stroke_color=BLUE, stroke_width=3,
                      fill_color=BLUE, fill_opacity=.32).move_to(p(-.79 + rear * .45, .68))
    fibers = VGroup()
    for i in range(4):
        y = -.42 + i * .31
        line = curve([(-2 + rear * .78 + i * .18, -.89 + i * .16),
                      (-.56, y), (.55, y + .07), (1.67 + front * .52 - i * .16, y + .07)],
                     YELLOW, 2.6).set_stroke(opacity=.66)
        fibers.add(line)
        for j in range(4):
            q = (j / 4 - flow + .11 * i) % 1
            d = Dot(line.point_from_proportion(q), radius=.055, color=YELLOW)
            d.set_opacity(min(1, 8 * q, 8 * (1 - q)))
            fibers.add(d)
    pads = VGroup()
    for i, x in enumerate((-2.61, -1.74, 1.43, 2.29)):
        strength = grip if i >= 2 or stretch else grip * np.exp(-rear * 5)
        pads.add(RoundedRectangle(width=.30 + .43 * strength, height=.16 + .09 * strength,
                                  corner_radius=.07, stroke_color=GREEN, stroke_width=2,
                                  fill_color=GREEN, fill_opacity=.72).set_opacity(min(strength, 1))
                 .move_to(p(x, pad_y)))
    return VGroup(body, nucleus, fibers, pads)


def live_crawler(scene, front, rear, grip, speed, *, pinned=False):
    """Tie flow speckles and the schematic gauge to the same speed control."""
    clock = ValueTracker(0)
    clock.add_updater(lambda m, dt: m.increment_value(dt * (.17 + .74 * speed.get_value())))
    scene.add(clock)
    body = always_redraw(lambda: crawler(front.get_value(), rear.get_value(), grip.get_value(),
                                         clock.get_value(), stretch=pinned))
    return body


def hook_picture(clumped=False, tug=0, travel=0):
    trio = colony(HOOK_CLOSED if clumped else HOOK_OPEN, .70)
    center = crawler(.13, 0, .72, .15).scale(.51)
    traveller = crawler(.25, .13, .58, .25).scale(.43)
    for mob, x in ((center, .05), (traveller, 3.58 + travel)):
        mob.move_to(p(x, -1.51 + mob.height / 2))
    return VGroup(chamber(), substrate(tug), trio, center, traveller)


def link_view(offset=0, installed=True, receptor_color=PURPLE):
    """Enlarged two-cell contact with four geometric links on each side."""
    pair = VGroup()
    for side in (-1, 1):
        wall = side * (.91 + offset)
        body_x = side * (3.62 + offset * .4)
        rim = curve([(wall, -.1), (wall + side * .24, 1.02), (body_x, 1.82),
                     (side * 6.06, .84), (side * 6.06, -1.1), (body_x, -1.83),
                     (wall + side * .24, -1.13), (wall, -.1)], BLUE, 4, "#234850")
        partner = RoundedRectangle(width=.72, height=.38, corner_radius=.13, stroke_color=GREEN,
                                   fill_color=GREEN, fill_opacity=.65).move_to(p(side * (.36 + offset), 0))
        receptor = RoundedRectangle(width=.52, height=.72, corner_radius=.11,
                                    stroke_color=receptor_color, fill_color=receptor_color,
                                    fill_opacity=.78).move_to(p(wall, 0))
        adaptor = RoundedRectangle(width=.92, height=.48, corner_radius=.12, stroke_color=PINK,
                                   fill_color=PINK, fill_opacity=.85).move_to(p(wall + side * .72, 0))
        if not installed:
            adaptor.shift(UP * 1.22).set_opacity(0)
        cable = VGroup(*(curve([(wall + side * 1.17, y * .2),
                                (wall + side * 1.75, y * .63),
                                (wall + side * 2.29, y), (wall + side * 2.83, y * .72)],
                               YELLOW, 3.4) for y in (-.43, 0, .43)))
        pair.add(VGroup(rim, partner, receptor, adaptor, cable))
    return pair


def forebrain():
    """A ventral-to-cortical slice, carried without rescaling between studies."""
    rim = [(-6.02, -1.6), (-5.62, -.52), (-4.56, -.77), (-3.82, -.02),
           (-2.84, -.80), (-1.53, -.33), (-.52, .76), (1.24, 1.85),
           (3.25, 2.3), (5.44, 1.69), (6.11, .41), (5.92, -.63),
           (4.2, -.85), (2.35, -1.28), (.25, -2.26), (-3.5, -2.41),
           (-6.02, -1.6)]
    tissue = curve(rim, TEAL, 4, "#244D55")
    preplate = curve([(-.12, .6), (1.24, 1.63), (3.24, 2.06), (5.35, 1.48), (5.9, .51)],
                     BLUE, 8)
    eminences = VGroup(
        curve([(-5.76, -1.54), (-5.44, -.68), (-4.52, -.99), (-4.23, -1.58)], TEAL, 2.4),
        curve([(-4.26, -1.5), (-3.82, -.29), (-3.18, -.69), (-2.78, -1.63)], TEAL, 2.4),
    )
    return VGroup(tissue, preplate, eminences).set_z_index(-2)


def track_cells(source, routes, travel, r=.19):
    """Let cells leave one labelled site at offsets along different tissue paths."""
    paths = [curve([source, *route], ORANGE) for route in routes]
    return VGroup(*(cell(*path.point_from_proportion(
        np.clip((travel - i * .073) / .68, 0, 1))[:2], r, dye=True)
        for i, path in enumerate(paths)))


LGE = (-3.76, -.65)
MGE = (-5.22, -1.03)
LONG_ROUTES = [
    [(-2.7, -1.25), (-1.8, -1.12), (-.24, .40), (2.18, 1.76), (4.48, 1.63)],
    [(-2.7, -1.25), (-1.48, -1.06), (.25, .76), (2.1, 1.70), (3.62, 1.91)],
    [(-2.7, -1.25), (-1.3, -.89), (.51, -.21), (2.87, .91), (5.20, 1.16)],
]
SHORT_ROUTES = [
    [(-2.92, -.82), (-2.40, -.86), (-2.05, -.98)],
    [(-2.76, -.82), (-1.94, -.80), (-1.51, -.66)],
    [(-2.73, -.85), (-1.90, -.71), (-1.00, -.49)],
    [(-2.92, -.90), (-2.13, -1.07), (-1.48, -1.12)],
    [(-2.79, -.94), (-2.06, -.92), (-.88, -.95)],
]


def neuron(x, y, size=.65):
    soma = cell(x, y, size * .27, dye=True)
    branches = VGroup()
    for angles in [(20, 48, -12), (106, 65, 133), (178, 146, 204), (254, 219, 291), (322, 302, 356)]:
        a, b, c = (np.radians(i) for i in angles)
        root = p(x, y)
        joint = root + size * .65 * p(np.cos(a), np.sin(a))
        branches.add(Line(root, joint, color=ORANGE, stroke_width=3))
        for d in (b, c):
            tip = joint + size * .52 * p(np.cos(d), np.sin(d))
            branches.add(Line(joint, tip, color=ORANGE, stroke_width=2.6))
    return VGroup(branches, soma)


def graft_inset():
    ring = Circle(radius=1.04, stroke_color=BLUE, stroke_width=3,
                  fill_color=CHAMBER, fill_opacity=1).move_to(p(4.65, -1.19))
    graft = VGroup(cell(4.31, -1.05, .22, True), cell(4.98, -1.35, .20, True))
    neurons = VGroup(neuron(4.31, -1.05, .56), neuron(4.98, -1.35, .49))
    return ring, graft, neurons


def prediction():
    return question_card(QUESTION, **QUESTION_STYLE)


def pinned_world(front=1.48, phase=.45):
    return VGroup(chamber(), substrate(.42), crawler(front, 0, 1, phase, stretch=True))


class S01Hook(SpokenScene):
    def construct(self):
        world = hook_picture()
        border, gel, trio, puller, traveller = world
        self.add(world, scope_tag(size=28, color=TEXT))
        self.at("how do you")
        self.wait(.30)
        self.play(Transform(trio, colony(HOOK_CLOSED, .70)), run_time=.95)
        self.at("cell sticks")
        stick = heading("Stick", GREEN, x=-4.15)
        self.play(FadeIn(stick), Transform(gel, substrate(.38)), run_time=.65)
        self.at("pulls or")
        pull = heading("Pull", YELLOW)
        self.play(FadeIn(pull), puller.animate.stretch(1.08, 0), run_time=.54)
        self.at("or travels")
        travel = heading("Travel", ORANGE, x=4.12)
        self.play(traveller.animate.shift(RIGHT * .94), FadeIn(travel), run_time=1.41)
        self.at("a still picture")
        self.wait(2.12)
        self.at("living cell assays")
        self.play(Transform(gel, substrate(.12)), trio.animate.shift(UP * .2),
                  traveller.animate.stretch(1.14, 0), run_time=1.30)
        self.at("invisible grip")
        self.play(trio.animate.shift(DOWN * .2), Transform(gel, substrate(.38)), run_time=1.45)
        self.at("travel into direct")
        self.play(traveller.animate.stretch(1 / 1.14, 0), run_time=1.06)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Cell Adhesion, Migration, and Mechanics Assays"
    TITLE = "Measuring How Cells Stick, Pull, and Travel"

    def construct(self):
        world = hook_picture(True, .38, .94)
        breathe(world[2], .08)
        bob(world[4], amp=.07, speed=3)
        title = fit_text(self.TITLE, size=42, min_size=36, max_w=12.2, font=TITLE_FONT)
        title.move_to(p(0, 3.22))
        self.add(world)
        self.play(FadeIn(title), run_time=.32)
        self.wait(1.10)
        self.play(FadeOut(title), run_time=.38)


class S03Adhesion(SpokenScene):
    def construct(self):
        world = hook_picture(True, .38, .94)
        border, gel, trio, puller, traveller = world
        self.add(world, scope_tag(size=28, color=TEXT))
        self.at("start with sticking")
        cluster = colony(COMPACT[:3])
        self.play(FadeOut(puller), FadeOut(traveller), Transform(trio, cluster),
                  Transform(gel, substrate(0)), run_time=1.01)
        self.at("separate cells")
        self.play(Transform(trio, colony(SINGLE[:3])), run_time=1.34)
        self.at("clump back together")
        self.play(Transform(trio, colony(COMPACT[:3])), run_time=.74)
        reaggregation = heading("Reaggregation", GREEN)
        self.play(FadeIn(reaggregation), run_time=.34)
        breathe(trio, .105)
        self.at("every anchoring grip")
        trio.clear_updaters()
        for c in trio:
            c.clear_updaters()
        zoom = Circle(radius=.42, color=GOLD, stroke_width=4).move_to(p(-.37, -.76))
        self.play(Create(zoom), FadeOut(reaggregation), run_time=.36)
        pair = link_view()
        self.play(zoom.animate.scale(4.1), FadeOut(trio), FadeIn(pair), run_time=.71)
        self.play(FadeOut(zoom), run_time=.24)
        labels = [
            T("Partner", 30, GREEN).move_to(p(.26, 2.16)),
            T("Receptor", 30, PURPLE).move_to(p(-1.64, -3.17)),
            T("Adaptor", 30, PINK).move_to(p(1.87, -3.17)),
            T("Cable", 30, YELLOW).move_to(p(3.56, 2.16)),
        ]
        def show_link(index, side, link, color):
            part = pair[side][link]
            outline = SurroundingRectangle(part, color=color, corner_radius=.11,
                                           buff=.12, stroke_width=5)
            other = 1 - side
            self.play(FadeIn(labels[index]), Create(outline),
                      pair[side][0].animate.set_fill("#356371"),
                      pair[other][0].animate.set_fill("#234850"), run_time=.49)
            return outline

        self.at("outer partner")
        focus = show_link(0, 1, 1, GREEN)
        self.at("receptor", lead=.08)
        self.remove(focus)
        focus = show_link(1, 0, 2, PURPLE)
        self.at("internal adapters")
        self.remove(focus)
        focus = show_link(2, 1, 3, PINK)
        self.at("inner cable")
        self.remove(focus)
        focus = show_link(3, 1, 4, YELLOW)
        self.at("remove or block")
        self.play(*(FadeOut(t) for t in labels), FadeOut(focus),
                  Transform(pair, link_view(.36, False)), run_time=.96)
        self.at("watch clumping change")
        self.play(Transform(pair, link_view(.57, False)), run_time=.74)
        self.at("then restore it")
        self.play(Transform(pair, link_view()), run_time=.85)
        self.finish()


class S04Mechanics(SpokenScene):
    def construct(self):
        self.add(chamber(), scope_tag(size=28, color=TEXT))
        gel = substrate()
        pair = link_view()
        self.add(gel, pair)
        f, r, grip, speed, stress = (ValueTracker(v) for v in (0, 0, .24, .36, 0))
        gel.add_updater(lambda m: m.become(substrate(stress.get_value())))
        motile = live_crawler(self, f, r, grip, speed)
        self.at("sticking also powers")
        zoom = Circle(radius=.82, color=GOLD, stroke_width=4).move_to(p(0, -.22))
        self.play(Create(zoom), run_time=.36)
        self.play(FadeOut(pair), FadeIn(motile), zoom.animate.scale(2), run_time=.79)
        self.play(FadeOut(zoom), run_time=.23)
        self.at("protrusion")
        protrusion = heading("Protrusion", BLUE)
        self.play(f.animate.set_value(.50), FadeIn(protrusion), run_time=.55)
        self.at("grip", lead=.06)
        adhesion = heading("Focal adhesion", GREEN)
        self.play(grip.animate.set_value(.89), swap(protrusion, adhesion, run_time=.46), run_time=.46)
        self.at("contraction")
        contraction = heading("Contraction", YELLOW)
        self.play(stress.animate.set_value(.42), speed.animate.set_value(.63),
                  swap(adhesion, contraction, run_time=.54), run_time=.54)
        self.at("and release")
        release = heading("Release", GREEN)
        self.play(r.animate.set_value(.73), stress.animate.set_value(.10),
                  swap(contraction, release), run_time=.91)
        self.at("integrin receptors")
        self.play(FadeOut(release), r.animate.set_value(.25), run_time=.80)
        receptor = RoundedRectangle(width=.37, height=.42, corner_radius=.08, color=PURPLE,
                                    fill_opacity=.92).move_to(p(2.29, -1.12))
        linker = RoundedRectangle(width=.42, height=.27, corner_radius=.08, color=PINK,
                                  fill_opacity=.95).move_to(p(2.21, -.83))
        bridge = curve([(1.85, -.35), (1.99, -.43), (2.11, -.57), (2.19, -.75)],
                       YELLOW, 2.6).set_stroke(opacity=.66)
        receptor_label = plaque("Integrin", PURPLE, x=-3.3)
        linker_label = plaque("Linker", PINK, x=-.7)
        self.play(FadeIn(receptor), FadeIn(receptor_label), run_time=.42)
        self.at("linker proteins")
        self.play(FadeIn(bridge), FadeIn(linker), FadeIn(linker_label), run_time=.53)
        self.at("form focal adhesions")
        self.play(FadeIn(adhesion), stress.animate.set_value(.30), run_time=1.38)
        self.at("anchoring cells")
        self.play(f.animate.set_value(.72), run_time=1.88)
        self.at("filament growth")
        engine = heading("Filament growth", YELLOW)
        self.play(swap(adhesion, engine), FadeOut(receptor_label), FadeOut(linker_label),
                  f.animate.set_value(1.05), speed.animate.set_value(.77), run_time=1.63)
        self.at("adhesion is the clutch")
        clutch = heading("Adhesion is the clutch", GREEN)
        self.play(swap(engine, clutch), stress.animate.set_value(.43),
                  speed.animate.set_value(.47), run_time=1.58)
        self.at("mechanics assays measure")
        forces = VGroup(arr((-2.65, -1.84), (-1.35, -1.84)), arr((2.47, -1.84), (1.21, -1.84)))
        tr = heading("Traction stress", YELLOW)
        self.play(FadeOut(receptor), FadeOut(bridge), FadeOut(linker), swap(clutch, tr),
                  LaggedStart(*(GrowArrow(a) for a in forces), lag_ratio=.26), run_time=.95)
        self.at("force per area")
        self.play(FadeIn(plaque("Force per area", YELLOW, x=-2.12)),
                  stress.animate.set_value(.56), run_time=1.52)
        self.at("local actin speed")
        gauge = dial(speed, center=p(4.85, .24), radius=.94, color=YELLOW, label="Actin speed")
        gauge.remove(gauge[3])
        gauge[-1].move_to(p(4.84, 1.58))
        self.play(FadeIn(gauge), speed.animate.set_value(.66), run_time=1.23)
        self.finish()


class S05Migration(SpokenScene):
    def construct(self):
        schematic = scope_tag(size=28, color=TEXT)
        self.add(chamber(), schematic)
        floor = substrate(.56)
        motile = crawler(1.05, .25, .89, .36)
        self.add(floor, motile)
        self.at("inside developing tissue")
        tissue = forebrain()
        self.play(ReplacementTransform(floor, tissue), FadeOut(motile), run_time=1.35)
        cells = VGroup(*(cell(x, y, .30) for x, y in
                         [(-5.2, -1.22), (-3.76, -.65), (-2.75, -1.98), (-1.1, -1.58),
                          (.18, .21), (1.57, 1.00), (3.2, 1.52), (4.43, .78)]))
        self.play(LaggedStart(*(FadeIn(c, shift=UP * .16) for c in cells), lag_ratio=.14), run_time=1.85)
        breathe(cells, .12)
        self.at("a dye like")
        dye = heading("DiI / DiA", ORANGE)
        drop = curve([(-3.76, .83), (-3.51, .42), (-3.76, .15), (-4.01, .42), (-3.76, .83)],
                     ORANGE, 3, ORANGE)
        self.play(FadeIn(drop, shift=DOWN * .38), FadeIn(dye), run_time=.68)
        self.at("dissolves into cell membranes")
        donor = cell(*LGE, .34, True)
        cells[1].clear_updaters()
        self.play(FadeOut(cells[1]), FadeOut(drop, shift=DOWN * .34), FadeIn(donor), run_time=.73)
        pulse(donor[0], base=5, amp=2, speed=4)
        self.at("cells leaving that spot")
        progress = ValueTracker(.025)
        travellers = always_redraw(lambda: track_cells(LGE, LONG_ROUTES, progress.get_value(), .22))
        self.add(travellers)
        self.play(FadeOut(dye), progress.animate.set_value(.48), run_time=2.58)
        self.at("slices let you watch")
        slice_label = plaque("Slice", BLUE, x=-3.98)
        glass = Polygon(p(-5.65, 1.15), p(-4.91, 2.20), p(-2.66, 2.20), p(-3.40, 1.15),
                        stroke_color=BLUE, stroke_width=2.5, fill_color=GEL, fill_opacity=.75)
        carried = VGroup(cell(-5.01, 1.51, .14, True), cell(-4.67, 1.79, .14, True))
        self.play(FadeIn(glass), FadeIn(carried), FadeIn(slice_label), run_time=.54)
        self.play(carried.animate.shift(RIGHT * .70), progress.animate.set_value(.74), run_time=1.30)
        self.at("grafts show what")
        ring, graft, neurons = graft_inset()
        graft_label = plaque("Graft", ORANGE, x=3.58)
        self.play(FadeIn(ring), FadeIn(graft), FadeIn(graft_label), run_time=.62)
        self.play(Transform(graft, neurons), progress.animate.set_value(.86), run_time=1.22)
        self.at("each assay measures")
        self.play(FadeOut(ring), FadeOut(graft), FadeOut(graft_label),
                  FadeOut(slice_label), FadeOut(glass), FadeOut(carried), run_time=.42)
        trio = VGroup(
            VGroup(cell(-3.8, -3.23, .13), cell(-3.51, -3.23, .13), plaque("Grip", GREEN, -2.72, -3.23)),
            VGroup(arr((-.98, -3.23), (-.49, -3.23)), plaque("Pull", YELLOW, .02, -3.23)),
            VGroup(cell(2.03, -3.23, .13, True), arr((2.22, -3.23), (2.58, -3.23), ORANGE),
                   plaque("Travel", ORANGE, 3.28, -3.23)),
        )
        # The three readouts occupy their own bottom band during the recap.
        self.play(FadeOut(schematic), FadeIn(trio.set_opacity(.48)), run_time=.40)
        self.at("grip pull", lead=.20)
        self.play(trio[0].animate.set_opacity(1), run_time=.33)
        self.at("pull or travel")
        self.play(trio[0].animate.set_opacity(.48), trio[1].animate.set_opacity(1), run_time=.38)
        self.at("or travel", lead=-.08)
        self.play(trio[1].animate.set_opacity(.48), trio[2].animate.set_opacity(1), run_time=.58)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        tissue = forebrain()
        tracers = track_cells(LGE, LONG_ROUTES, .86, .22)
        self.add(chamber(), tissue, tracers, scope_tag(size=28, color=TEXT))
        f, r, grip, speed, stress = (ValueTracker(v) for v in (.08, 0, .39, .47, .07))
        gel = substrate(.07)
        motile = live_crawler(self, f, r, grip, speed, pinned=True)
        self.at("back to the crawling")
        self.play(ReplacementTransform(tissue, gel), FadeOut(tracers), FadeIn(motile), run_time=1.22)
        gel.add_updater(lambda m: m.become(substrate(stress.get_value())))
        self.at("focal adhesions anchor")
        label = heading("Focal adhesions", GREEN)
        self.play(grip.animate.set_value(.68), stress.animate.set_value(.22),
                  f.animate.set_value(.31), FadeIn(label), run_time=1.55)
        self.at("suppose you make")
        self.play(grip.animate.set_value(1), stress.animate.set_value(.42),
                  f.animate.set_value(.58), FadeOut(label), run_time=2.36)
        self.at("will the cell always")
        self.play(FadeIn(prediction()), f.animate.set_value(.71), speed.animate.set_value(.25), run_time=1.50)
        self.at("stronger adhesions slow", lead=.2)
        self.play(f.animate.set_value(1.48), run_time=3.44, rate_func=lambda t: t**2)
        self.remove(motile)
        gel.clear_updaters()
        self.add(crawler(1.48, 0, 1, .45, stretch=True))
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(pinned_world(), prediction(), scope_tag(size=28, color=TEXT))
        self.wait(4.5)


# Gardel et al. (2008), doi:10.1083/jcb.200810060, Fig. 5 and Results.
# Approximate control means read from Fig. 5E–G. Slopes in kPa·s/µm are
# numerically equal to Pa per (nm/s). The two lines meet at about 8.7 nm/s.
# The magnitudes are normalized for the schematic teaching plot.
SLOW_SLOPE, FAST_SLOPE = 11, -3
SLOW_INTERCEPT = 65 - SLOW_SLOPE * 6
FAST_INTERCEPT = 88 - FAST_SLOPE * 11
TURN_SPEED = (FAST_INTERCEPT - SLOW_INTERCEPT) / (SLOW_SLOPE - FAST_SLOPE)


def traction_schematic(speed):
    return min(SLOW_SLOPE * speed + SLOW_INTERCEPT,
               FAST_SLOPE * speed + FAST_INTERCEPT) / 105


def trace_area(plot, endpoint):
    speeds = np.linspace(1, endpoint, 42)
    points = [plot.pt(x, traction_schematic(x)) for x in speeds]
    return Polygon(plot.pt(1, 0), *points, plot.pt(endpoint, 0),
                   stroke_width=0, fill_color=YELLOW, fill_opacity=.23).set_z_index(-1)


class S08AnswerMechanics(SpokenScene):
    def construct(self):
        border, gel, stalled = pinned_world()
        q = prediction()
        self.add(border, gel, stalled, q, scope_tag(size=28, color=TEXT))
        self.at("stronger adhesion can")
        retracted = crawler(.55, 0, 1, .62, stretch=True)
        retracted[0].set_fill("#346371")
        self.play(FadeOut(q, run_time=.25), Transform(stalled, retracted, run_time=1.02),
                  Transform(gel, substrate(.23), run_time=1.02), rate_func=linear)
        self.at("the rear must")
        release = heading("Rear must release", RED)
        rear = Circle(radius=.46, color=RED, stroke_width=4).move_to(p(-2.61, -1.32))
        self.play(Create(rear), FadeIn(release), run_time=.49)
        self.at("stronger grip resists")
        self.play(Transform(stalled, crawler(1.08, 0, 1, .91, stretch=True)),
                  Transform(gel, substrate(.50)), run_time=2.63)
        self.at("in ptk1")
        left_cell = crawler(1.08, 0, 1, .91, stretch=True).scale(.60).move_to(p(-3.94, -.29))
        self.play(FadeOut(rear), FadeOut(release), FadeOut(gel),
                  Transform(stalled, left_cell), run_time=.53)
        plot = Plot(box=(-.90, 6.17, -1.78, 2.15), xr=(0, 24), yr=(0, 1),
                    xlabel="Local actin speed", ylabel="Traction stress", color=TEXT, label_size=30)
        plot.xlabel.move_to(p(2.65, -3.12))
        plot.ylabel.move_to(p(.7, 2.48))
        # Keep the source at the same size as the other study headings.
        title = heading("PtK1 cells", GOLD, x=1.70)
        self.play(FadeIn(plot), FadeIn(title), run_time=.40)
        self.at("had a two")
        point = ValueTracker(1.01)
        trace = plot.live_curve(traction_schematic, point, color=YELLOW, x0=1)
        marker = plot.dot(point.get_value, lambda: traction_schematic(point.get_value()), color=TEXT, ring=YELLOW)
        self.add(always_redraw(lambda: trace_area(plot, point.get_value())), trace, marker)
        self.play(point.animate.set_value(TURN_SPEED), run_time=2.69, rate_func=linear)
        self.at("changed near")
        a, b = plot.pt(8, 0)[0], plot.pt(10, 0)[0]
        band = Rectangle(width=b - a, height=3.83, stroke_width=0, fill_color=BLUE, fill_opacity=.19)
        band.move_to(p((a + b) / 2, .17)).set_z_index(-1)
        threshold = T("8–10 nm/s", 29, BLUE).move_to(p((a + b) / 2, -2.20))
        self.play(FadeIn(band), FadeIn(threshold), run_time=.56)
        self.play(point.animate.set_value(14), run_time=2.10, rate_func=linear)
        self.at("faster flow does")
        self.play(point.animate.set_value(24), run_time=2.85, rate_func=linear)
        self.at("the clutch is")
        self.play(FadeIn(heading("Clutch model", GREEN, x=-3.93)),
                  Transform(stalled, crawler(.88, 0, 1, 1.24, stretch=True).scale(.60).move_to(p(-3.94, -.29))),
                  run_time=1.48)
        self.finish()


class S09Controls(SpokenScene):
    def construct(self):
        clump = colony(COMPACT)
        gel = substrate()
        self.add(chamber(), gel, clump, scope_tag(size=28, color=TEXT))
        breathe(clump, .12)
        self.at("every assay has")
        self.play(FadeIn(heading("Assay limits", GOLD)), run_time=.51)
        self.at("reaggregation tests clumping")
        target = Circle(radius=.34, color=GOLD, stroke_width=4).move_to(p(-.31, -.78))
        self.play(Create(target), run_time=.72)
        self.at("not force on")
        unknown = T("?", 39, GOLD).move_to(p(-.35, 1.94))
        force = plaque("No single-contact force", YELLOW, x=-1.1)
        self.play(FadeIn(unknown), FadeIn(force), run_time=.45)
        self.at("tracking follows moving")
        # Remove the old label and contact before bringing up the next claim.
        self.play(FadeOut(unknown), FadeOut(force), FadeOut(target), run_time=.35)
        tissue = forebrain()
        self.play(ReplacementTransform(gel, tissue), FadeOut(clump), run_time=.67)
        motion = ValueTracker(.13)
        cells = always_redraw(lambda: track_cells(LGE, LONG_ROUTES, motion.get_value(), .24))
        self.add(cells)
        self.play(motion.animate.set_value(.48), run_time=1.03)
        self.at("does not show")
        identity = plaque("Identity unproven", ORANGE, x=-.9)
        fate = T("?", 39, GOLD).move_to(p(4.93, 1.12))
        self.play(FadeIn(identity), FadeIn(fate), motion.animate.set_value(.75),
                  tissue[0].animate.set_fill("#366370"), run_time=2.18)
        self.at("losing a gene")
        stopped = cell(.29, .30, .40, True)
        self.play(FadeOut(identity), FadeOut(fate), FadeOut(cells), FadeIn(stopped, shift=RIGHT * .42),
                  tissue[0].animate.set_fill("#244D55"), run_time=.86)
        self.at("two ideas compete")
        halt = Circle(radius=.55, color=RED, stroke_width=4).move_to(stopped)
        self.play(Create(halt), tissue[0].animate.set_fill("#203843"), run_time=.81)
        self.at("it may be")
        traveller = plaque("In traveller?", ORANGE, x=-2.2)
        substrate_label = plaque("In tissue?", TEAL, x=2.2)
        self.play(FadeIn(traveller, run_time=.40),
                  Indicate(stopped, color=ORANGE, scale_factor=1.18, run_time=1.18))
        self.at("or in the tissue")
        self.play(FadeIn(substrate_label, run_time=.40), FadeOut(halt),
                  tissue[0].animate.set_fill("#346A71"), run_time=1.45)
        self.finish()


class S10UnlockedAdhesion(SpokenScene):
    def construct(self):
        tissue = forebrain()
        tissue[0].set_fill("#346A71")
        stopped = cell(.29, .30, .40, True)
        self.add(chamber(), tissue, stopped, scope_tag(size=28, color=TEXT))
        self.at("these assays unlocked")
        clump = colony(SINGLE)
        self.play(ReplacementTransform(tissue, substrate()), FadeOut(stopped),
                  LaggedStart(*(FadeIn(c) for c in clump), lag_ratio=.12), run_time=1.28)
        breathe(clump, .12)
        self.at("in 1992")
        study = heading("Hirano et al., 1992", GOLD)
        self.play(FadeIn(study), run_time=.52)
        self.at("colleagues studied")
        label = plaque("PC9 cells", BLUE, x=-3.65)
        self.play(FadeIn(label), run_time=.45)
        self.at("carrying the receptor")
        pair = link_view(.06, False)
        self.play(FadeOut(clump), FadeIn(pair), run_time=.70)
        receptor_label = plaque("E-cadherin", PURPLE, x=-1.04)
        self.play(FadeIn(receptor_label), run_time=.37)
        self.at("aggregation was greatly")
        self.play(Transform(pair, link_view(0, False)), run_time=.76)
        self.play(Transform(pair, link_view(.43, False)), run_time=1.06)
        self.at("grew mostly singly")
        self.play(FadeOut(pair), FadeOut(receptor_label), FadeIn(clump), run_time=.72)
        self.at("putting the adapter")
        for c in clump:
            c.clear_updaters()
        self.play(FadeOut(clump), FadeIn(pair), run_time=.35)
        adaptor = plaque("α-catenin", PINK, x=-.50)
        self.play(FadeIn(adaptor), Transform(pair, link_view(0, True)), run_time=.85)
        self.at("restored firm")
        self.play(FadeOut(label), run_time=.30)
        self.at("compact")
        result = plaque("Compact aggregates", GREEN, x=-2.25)
        self.play(FadeOut(pair), FadeOut(adaptor), FadeIn(clump), run_time=.35)
        self.play(Transform(clump, colony(COMPACT), run_time=1.10), FadeIn(result, run_time=.38))
        breathe(clump, .065)
        self.finish()


class S11UnlockedMigration(SpokenScene):
    def construct(self):
        gel = substrate()
        cluster = colony(COMPACT)
        self.add(chamber(), gel, cluster, scope_tag(size=28, color=TEXT))
        self.at("in 1996")
        tissue = forebrain()
        self.play(ReplacementTransform(gel, tissue), FadeOut(cluster), run_time=1.28)
        study = heading("de Carlos et al., 1996", GOLD)
        self.play(FadeIn(study), run_time=.46)
        self.at("lateral ganglionic eminence")
        donor = cell(*LGE, .34, True)
        label = plaque("Lateral ganglionic eminence", ORANGE, x=-3.05)
        self.play(FadeIn(donor, scale=1.8), FadeIn(label), run_time=.80)
        pulse(donor[0], base=5, amp=3, speed=3.5)
        self.at("a ventral forebrain")
        self.play(Indicate(tissue[2][1], scale_factor=1.13, color=ORANGE), run_time=1.19)
        self.at("cultured rat embryos")
        self.play(FadeOut(label), tissue[0].animate.set_fill("#2A545D"), run_time=1.43)
        self.at("most labeled cells")
        radial = ValueTracker(.07)
        nearby = always_redraw(lambda: track_cells(LGE, SHORT_ROUTES, radial.get_value(), .19))
        self.add(nearby)
        target = curve([(-2.47, -1.01), (-1.72, -.52), (-.92, -.23), (-.56, -.68),
                        (-.74, -1.20), (-1.52, -1.40), (-2.47, -1.01)],
                       TEAL, 0, TEAL, .46).set_z_index(-1)
        self.play(radial.animate.set_value(.89), FadeIn(target), run_time=2.80)
        self.at("ventralateral cortex")
        near_label = plaque("Ventrolateral cortex", ORANGE, x=-2.50)
        self.play(FadeIn(near_label), radial.animate.set_value(1), run_time=1.04)
        self.at("others ran sideways")
        sideways = ValueTracker(.05)
        distant = always_redraw(lambda: track_cells(LGE, LONG_ROUTES[:2], sideways.get_value(), .21))
        self.add(distant)
        cortex = curve([(-.53, .14), (.57, 1.03), (2.87, 1.94), (4.50, 1.78),
                        (5.66, 1.06), (5.48, .40), (4.00, .81), (2.82, .91),
                        (1.47, .52), (.43, -.19), (-.53, .14)], TEAL, 0, TEAL, .52).set_z_index(-1)
        self.play(FadeOut(near_label), FadeOut(target), FadeIn(cortex),
                  sideways.animate.set_value(.66), run_time=2.44)
        self.at("the plate")
        preplate = plaque("Preplate", BLUE, x=-.1)
        self.play(FadeIn(preplate), FadeOut(cortex), sideways.animate.set_value(.86), run_time=1.33)
        self.at("first layer of")
        self.play(tissue[1].animate.set_stroke(width=12), sideways.animate.set_value(1), run_time=1.71)
        self.finish()


class S12UnlockedSlices(SpokenScene):
    def construct(self):
        tissue = forebrain()
        distal = track_cells(LGE, LONG_ROUTES[:2], 1, .21)
        nearby = track_cells(LGE, SHORT_ROUTES, 1)
        lge_donor = cell(*LGE, .34, True)
        self.add(chamber(), tissue, distal, nearby, lge_donor, scope_tag(size=28, color=TEXT))
        self.at("in 1999")
        study = heading("Wichterle et al., 1999", GOLD)
        self.play(FadeOut(distal), FadeOut(nearby), FadeOut(lge_donor),
                  FadeIn(study), tissue[1].animate.set_stroke(width=8), run_time=.74)
        self.at("tracked cells from")
        donor = cell(*MGE, .35, True)
        mge_label = plaque("MGE", ORANGE, x=-4.87)
        self.play(FadeIn(donor, scale=1.7), tissue[0].animate.set_fill("#34565E"), run_time=.95)
        pulse(donor[0], base=6, amp=3, speed=3)
        self.at("the mge")
        focus = curve([(-5.76, -1.47), (-5.48, -.76), (-4.94, -.94),
                       (-4.59, -1.47), (-5.14, -1.77), (-5.76, -1.47)],
                      ORANGE, 0, ORANGE, .34).set_z_index(-1)
        self.play(FadeIn(mge_label), FadeIn(focus, scale=.55), run_time=.78)
        self.at("in embryonic slices")
        slice_label = plaque("Embryonic slice", BLUE, x=-1.65)
        self.play(FadeIn(slice_label), tissue[0].animate.set_fill("#315E67"), run_time=.98)
        travel = ValueTracker(.065)
        routes = [[(-3.8, -1.35), *route] for route in LONG_ROUTES]
        routes.append([(-3.8, -1.35), (-2.7, -1.25), (-1.45, -1.00),
                       (-.26, .17), (2.5, .74), (4.2, 1.01)])
        travelling = always_redraw(lambda: track_cells(MGE, routes, travel.get_value(), .22))
        self.add(travelling)
        self.at("those cells migrated")
        self.play(travel.animate.set_value(.76), FadeOut(focus),
                  tissue[0].animate.set_fill("#244D55"), run_time=3.58)
        self.at("grafted cells became")
        ring, graft, neurons = graft_inset()
        self.play(FadeOut(slice_label), FadeIn(ring), FadeIn(graft), run_time=.52)
        self.play(Transform(graft, neurons), travel.animate.set_value(1), run_time=1.16)
        graft_label = plaque("Grafted cells → neurons", ORANGE, x=1.18)
        self.play(FadeIn(graft_label), run_time=.36)
        self.at("each assay captures")
        self.play(FadeOut(study), FadeOut(mge_label), FadeOut(graft_label),
                  FadeOut(ring), FadeOut(graft), tissue[0].animate.set_fill("#27454E"), run_time=1.13)
        self.at("shows what still")
        self.play(FadeOut(donor), FadeOut(travelling), tissue[0].animate.set_fill(CHAMBER), run_time=1.89)
        self.finish()


class S13End(EndCard):
    LINE = "Measure grip, pull, or travel directly; no assay proves every step."
