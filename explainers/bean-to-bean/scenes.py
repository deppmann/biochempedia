"""From Bean to Bean. A shared windowsill and a five-stage paper wheel."""
from bp_parts import *
from bp_style import EndCard

# COLOR MAP: GREEN living plant and pods; YELLOW sunlight, pollen, ripening;
# BLUE water and glass; RED safety; GOLD seed, clay and paper; TEAL observations.
WALL = "#19262E"
SKY = "#43717D"
HILL = "#335F55"
FRAME = "#77989B"
WOOD = "#47363A"
WOOD_LIGHT = "#73534A"
CLAY = "#C77B58"
CLAY_LIGHT = "#E9A47B"
SOIL = "#684739"
SEED = "#EABE84"
SEED_LINE = "#AC714D"
LEAF_DARK = "#4D936E"
POD_GREEN = "#B0D975"
PAPER = "#F3E2B8"
INK = "#39382E"
SKIN = "#D39776"
SLEEVE = "#548496"
POT_AT = (-1.95, -2.32, 0)
POT_SCALE = 0.94
QUESTION = "No bees indoors:\npods or empty?"
QUESTION_STYLE = dict(y=1.62, left=2.48, max_w=3.95, size=34)
RING_AT = (5.64, -0.02, 0)


def pt(x, y):
    return np.array([x, y, 0.0])


def form(points, color, outline=None, width=2):
    return Polygon(*[pt(x, y) for x, y in points], fill_color=color, fill_opacity=1,
                   stroke_color=outline or color, stroke_width=width)


def oval(w, h, x, y, color, outline=None, width=0):
    return Ellipse(width=w, height=h, fill_color=color, fill_opacity=1,
                   stroke_color=outline or color, stroke_width=width).move_to(pt(x, y))


def tile(w, h, x, y, color, radius=0.16, outline=None, width=0):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            fill_color=color, fill_opacity=1,
                            stroke_color=outline or color, stroke_width=width).move_to(pt(x, y))


def stroke(points, color, width=3, smooth_path=False):
    path = VMobject(stroke_color=color, stroke_width=width)
    points = [pt(x, y) for x, y in points]
    if smooth_path:
        path.set_points_smoothly(points)
    else:
        path.set_points_as_corners(points)
    return path


def shape(start, segments, color, outline=None, width=2):
    path = VMobject(fill_color=color, fill_opacity=1,
                    stroke_color=outline or color, stroke_width=width)
    path.start_new_path(pt(*start))
    for a, b, c in segments:
        path.add_cubic_bezier_curve_to(pt(*a), pt(*b), pt(*c))
    return path.close_path()


def sunlight():
    """A slow pane-wide sweep and a few motes, visible only inside the window."""
    glint = form([(-5.86, 2.78), (-4.6, 2.78), (-2.95, -1.45),
                  (-5.1, -1.45)], "#E2C88A", width=0).set_fill(opacity=0.20)
    glow = form([(-4.4, 2.78), (-4.05, 2.78), (-2.5, -1.45),
                 (-2.95, -1.45)], "#E2C88A", width=0).set_fill(opacity=0.13)
    light = VGroup(glint, glow)
    start = light.get_center().copy()
    light.clock = 0.0

    def sweep(mob, dt):
        mob.clock += dt
        mob.move_to(start + RIGHT * (0.56 * np.sin(mob.clock * 0.95)))
        glint.set_fill(opacity=0.20 + 0.09 * np.sin(mob.clock * 1.4))
        glow.set_fill(opacity=0.13 + 0.06 * np.sin(mob.clock * 1.4))

    light.add_updater(sweep)
    motes = VGroup()
    for x, y, r, phase in [(-5.9, 2.19, .045, 0), (-4.9, 1.1, .055, 1),
                           (-3.7, 2.1, .045, 2), (-5.3, -.52, .035, 3),
                           (-2.6, .24, .046, 1), (-1.4, 2.55, .037, 0)]:
        mote = Dot(pt(x, y), radius=r, color=PAPER).set_opacity(.72)
        bob(mote, amp=.21, speed=1.4, seed=phase)
        motes.add(mote)
    return VGroup(light, motes)


def windowsill():
    wall = Rectangle(width=config.frame_width, height=config.frame_height,
                     stroke_width=0, fill_color=WALL, fill_opacity=1)
    surround = tile(8.68, 5.15, -2.32, .58, "#2F4145", radius=.17)
    glass = tile(8.44, 4.89, -2.32, .58, SKY, radius=.10)
    hills = form([(-6.49, -.23), (-5.59, .14), (-4.72, .23), (-3.81, -.16),
                  (-2.82, -.31), (-1.73, .51), (-.65, .26), (.65, .54),
                  (1.85, .16), (1.85, -1.63), (-6.49, -1.63)], HILL, width=0)
    garden = form([(-6.49, -.96), (-5.1, -.65), (-3.8, -.78), (-2.8, -.48),
                   (-1.65, -.74), (-.25, -.46), (1.85, -.62), (1.85, -1.62),
                   (-6.49, -1.62)], "#284D46", width=0)
    mullion = tile(.12, 4.88, -2.32, .58, FRAME, radius=.04)
    sill = tile(8.79, .25, -2.32, -1.76, FRAME, radius=.06)
    desktop = form([(-7.11, -2.13), (7.11, -2.13), (7.11, -3.19),
                    (-7.11, -3.19)], WOOD_LIGHT, width=0)
    apron = form([(-7.11, -3.19), (7.11, -3.19), (7.11, -4),
                  (-7.11, -4)], WOOD, width=0)
    return VGroup(wall, surround, glass, hills, garden, sunlight(), mullion, sill, desktop, apron)


def seed(color=SEED, hilum=True):
    body = shape((-.95, .1), [
        ((-.94, .72), (-.19, .94), (.45, .64)),
        ((1.05, .42), (1.04, -.42), (.33, -.57)),
        ((-.07, -.68), (-.17, -.29), (-.43, -.31)),
        ((-.68, -.49), (-.99, -.31), (-.95, .1)),
    ], color, SEED_LINE, 3)
    mark = stroke([(-.27, -.17), (-.12, -.12), (.07, -.22)], SEED_LINE, 4, True)
    return VGroup(body, mark) if hilum else body


def leaf(length=1.3, color=GREEN, angle=0):
    blade = shape((0, 0), [
        ((.22, .29), (.57, .36), (1, .10)),
        ((.73, -.32), (.30, -.34), (0, 0)),
    ], color, LEAF_DARK, 2)
    vein = stroke([(.1, .01), (.48, .01), (.79, .075)], LEAF_DARK, 2, True)
    return VGroup(blade, vein).scale(length, about_point=ORIGIN).rotate(angle, about_point=ORIGIN)


def bud():
    return VGroup(oval(.3, .55, 0, .18, TEXT, "#A9C1BF", 1.8).rotate(.25),
                  leaf(.24, LEAF_DARK, PI * .78), leaf(.23, LEAF_DARK, PI * .23))


def flower():
    petals = VGroup(*[oval(.31, .49, .0, .24, TEXT, "#C6D2D5", 1.5)
                      .rotate(a, about_point=ORIGIN) for a in np.arange(5) * TAU / 5])
    return VGroup(petals, Dot(radius=.11, color=YELLOW))


def pod(color=POD_GREEN, opened=False):
    edge = LEAF_DARK if color == POD_GREEN else SEED_LINE
    body = shape((-1.48, .09), [
        ((-.96, .48), (-.3, .32), (.22, .27)),
        ((.86, .2), (1.2, .05), (1.5, -.35)),
        ((.82, -.31), (.42, -.34), (-.26, -.34)),
        ((-.77, -.36), (-1.27, -.14), (-1.48, .09)),
    ], color, edge, 3)
    stem = stroke([(-1.46, .07), (-1.66, .13), (-1.77, .28)], edge, 4, True)
    if opened:
        inside = shape((-1.24, .1), [
            ((-.5, .27), (.8, .19), (1.22, -.23)),
            ((.35, -.15), (-.72, -.29), (-1.24, .1)),
        ], PAPER, edge, 2)
        beans = VGroup(*[seed().scale(.20).rotate(-.12).move_to(pt(x, y))
                         for x, y in [(-.77, .04), (-.27, .015), (.21, -.02), (.67, -.07)]])
        return VGroup(stem, body, inside, beans)
    seam = stroke([(-1.31, .09), (-.61, .04), (.37, -.05), (1.19, -.24)], edge, 2, True)
    return VGroup(stem, body, seam)


def pot(cut=False):
    saucer = VGroup(oval(3.22, .36, 0, -.37, CLAY_LIGHT),
                    oval(2.83, .22, 0, -.36, CLAY),
                    oval(2.20, .09, 0, -.4, SOIL))
    body = form([(-1.42, 1.45), (1.42, 1.45), (1.05, -.29), (-1.05, -.29)], CLAY, CLAY_LIGHT, 3)
    gloss = form([(-1.26, 1.37), (-.95, 1.37), (-.72, -.23), (-.92, -.23)], CLAY_LIGHT, width=0)
    rim = tile(3.05, .29, 0, 1.44, CLAY_LIGHT, radius=.10)
    mouth = oval(2.77, .39, 0, 1.59, SOIL, CLAY_LIGHT, 3)
    if cut:
        inset = form([(-1.15, 1.48), (1.15, 1.48), (.82, -.15), (-.82, -.15)], "#33292A", width=0)
        drain = oval(.36, .09, 0, -.23, WALL)
        return VGroup(saucer, body, rim, inset, drain)
    return VGroup(saucer, body, gloss, rim, mouth)


def place_pot(obj, at=POT_AT, scale=POT_SCALE):
    return obj.scale(scale, about_point=ORIGIN).shift(at)


def bush(stage="buds", dying=False):
    """Plant base is always at the pot's soil surface. Three flowering sites are shared."""
    stem_color = "#A59556" if dying else LEAF_DARK
    leaf_color = "#D3B86F" if dying else GREEN
    stems = VGroup(
        stroke([(0, 0), (-.08, .81), (.03, 1.63), (.04, 3.32)], stem_color, 10, True),
        stroke([(-.02, 1.21), (-.63, 1.7), (-1.13, 2.48)], stem_color, 6, True),
        stroke([(.02, 1.55), (.60, 1.94), (1.18, 2.75)], stem_color, 6, True),
    )
    leaves = VGroup()
    for x, y, length, angle in [(-.04, .7, 1.65, 2.82), (.0, 1.02, 1.73, .30),
                                (-.48, 1.62, 1.51, 3.0), (.58, 1.91, 1.5, .24),
                                (-.88, 2.10, 1.22, 2.44), (.85, 2.26, 1.12, .64),
                                (.04, 2.44, 1.35, 2.34), (.04, 2.71, 1.24, .63)]:
        leaves.add(leaf(length, leaf_color, -angle if dying else angle).shift(pt(x, y)))
    tops = VGroup()
    for (x, y), angle in zip([(-1.13, 2.48), (.04, 3.32), (1.18, 2.75)], [-2.23, -.78, -1.11]):
        if stage == "buds":
            item = bud().scale(1.34)
        elif stage == "flowers":
            item = flower().scale(1.12)
        elif stage in ("tiny", "green", "yellow", "dry"):
            color = {"tiny": POD_GREEN, "green": POD_GREEN, "yellow": "#DFBC65", "dry": SEED}[stage]
            item = pod(color).shift(RIGHT * 1.48).scale(.31 if stage == "tiny" else .64,
                                                       about_point=ORIGIN).rotate(angle, about_point=ORIGIN)
        else:
            continue
        tops.add(item.shift(pt(x, y)))
    if dying:
        stems.stretch(.73, 1, about_point=ORIGIN)
        leaves.stretch(.73, 1, about_point=ORIGIN)
    return VGroup(stems, leaves, tops)


def planted(stage="buds", dying=False):
    return place_pot(bush(stage, dying).shift(UP * 1.61))


def sprout(height=2.3, hooked=False):
    if hooked:
        return VGroup(stroke([(0, 0), (-.03, .86), (.25, 1), (.44, .72)], LEAF_DARK, 9, True),
                      seed().scale(.19).rotate(-.7).move_to(pt(.46, .61))).scale(
                          height, about_point=ORIGIN)
    stem = stroke([(0, 0), (-.08, .47), (.03, .77), (.10, 1)], LEAF_DARK, 9, True)
    return VGroup(stem, leaf(.55, GREEN, 2.76).shift(pt(.04, .74)),
                  leaf(.51, GREEN, .36).shift(pt(.06, .86))).scale(height, about_point=ORIGIN)


def hand(color=SKIN, sleeve=SLEEVE, direction=1):
    cuff = tile(1.20, .62, -.87, 0, sleeve, radius=.15)
    palm = shape((-1.0, -.28), [
        ((-.54, -.41), (-.20, -.42), (.13, -.32)),
        ((.53, -.28), (.79, -.14), (.78, -.03)),
        ((.76, .07), (.62, .09), (.30, .045)),
        ((.47, .25), (.29, .34), (.10, .28)),
        ((-.08, .22), (-.36, .28), (-1.0, .26)),
        ((-1.02, .11), (-1.01, -.11), (-1.0, -.28)),
    ], color, "#A36856", 2)
    crease = stroke([(-.2, -.12), (.03, -.06), (.30, .045)], "#A36856", 2, True)
    return VGroup(palm, cuff, crease).stretch(direction, 0, about_point=ORIGIN)


def packet():
    back = form([(-1.25, -1.82), (1.25, -1.82), (1.25, 1.63),
                 (1.07, 1.82), (-1.25, 1.82)], PAPER, SEED, 3)
    flap = form([(-1.23, 1.34), (1.23, 1.34), (1.23, 1.72), (-1.23, 1.72)], SEED, width=0)
    drawing = pod().scale(.58).rotate(-.30).move_to(pt(0, -.37))
    return VGroup(back, flap, drawing)


def bag():
    return VGroup(
        form([(-1.16, -1.58), (1.14, -1.58), (1.22, .97), (.93, 1.47),
              (-.85, 1.47), (-1.19, .98)], "#AA7353", CLAY_LIGHT, 3),
        form([(-1.09, -.69), (1.11, -.69), (1.14, .54), (-1.12, .54)], SOIL, width=0),
        stroke([(-.85, 1.26), (.91, 1.26)], SEED, 3),
        VGroup(*[oval(.18, .10, x, y, SEED_LINE) for x, y in
                 [(-.63, -.29), (-.24, -.42), (.19, -.14), (.64, -.26), (.46, .19), (-.38, .18)]]),
    )


def drop(x, y, scale=1):
    return shape((0, .25), [
        ((-.04, .09), (-.18, -.02), (-.17, -.13)),
        ((-.17, -.34), (.17, -.34), (.17, -.13)),
        ((.18, -.02), (.04, .09), (0, .25)),
    ], BLUE, "#B7ECF1", 1.4).scale(scale).move_to(pt(x, y))


def water_stream(x, y, distance, count=5):
    drops = VGroup()
    for i in range(count):
        droplet = drop(x, y, .37 + .06 * (i % 3))
        droplet.age = i / count
        spread = .18 * np.sin(i * 2.4)

        def fall(mob, dt, spread=spread):
            mob.age = (mob.age + dt * 1.3) % 1
            mob.move_to(pt(x + spread * (mob.age + .2), y - distance * mob.age))
            mob.set_opacity(min(1, mob.age * 9, (1 - mob.age) * 8))

        droplet.add_updater(fall, call_updater=True)
        drops.add(droplet)
    return drops


def pencil():
    return VGroup(tile(2.05, .15, 0, 0, YELLOW, radius=.06),
                  form([(1.01, -.075), (1.37, 0), (1.01, .075)], SEED, width=0),
                  form([(1.26, -.024), (1.37, 0), (1.26, .024)], INK, width=0),
                  tile(.17, .17, -1.03, 0, RED, radius=.06))


def notably(text, color=TEXT, y=1.1):
    return fit_text(text, size=36, color=color, weight=BOLD,
                    max_w=4.12, min_size=28, max_lines=2).move_to(pt(4.37, y))


def cycle_wheel(paper=False):
    center, radius = pt(-1.96, .11), 2.88
    face = Circle(radius=radius, color=SEED, stroke_width=4,
                  fill_color=PAPER if paper else "#243D3C", fill_opacity=1).move_to(center)
    edge = Circle(radius=radius - .14, color=SEED_LINE if paper else FRAME,
                  stroke_width=2).move_to(center)
    spokes = VGroup()
    icons = VGroup()
    drawings = [seed(), sprout(.9, hooked=True), bush("none").scale(.38),
                flower().scale(1.20), pod(opened=True).scale(.57)]
    for i, drawing in enumerate(drawings):
        angle = PI / 2 + PI / 5 - i * TAU / 5
        spokes.add(Line(center, center + radius * pt(np.cos(angle), np.sin(angle)),
                        color=SEED_LINE if paper else FRAME, stroke_width=2.8))
        angle -= PI / 5
        drawing.set_width(min(drawing.width, 1.62)).move_to(
            center + 1.80 * pt(np.cos(angle), np.sin(angle)))
        icons.add(drawing)
    return VGroup(face, edge), spokes, icons


def wheel_arrow():
    # Travel clockwise from the final pod wedge, around the rim to the seed wedge.
    path = Arc(radius=2.55, start_angle=2.62, angle=-1.07,
               arc_center=pt(-1.96, .11), color=SEED_LINE, stroke_width=7)
    end = path.get_end()
    tip = Triangle(color=SEED_LINE, fill_color=SEED_LINE, fill_opacity=1,
                   stroke_width=0).scale(.13).rotate(-PI / 2).move_to(end)
    return VGroup(path, tip)


class S01Hook(SpokenScene):
    def construct(self):
        self.add(windowsill())
        plate = VGroup(oval(3.76, 1.27, -4.43, -2.28, PAPER, SEED, 3),
                       oval(3.17, .89, -4.43, -2.28, "#E7CCA0", SEED, 1.5))
        green_pod = pod().scale(.96).rotate(.20).move_to(pt(-4.47, -2.24))
        dry_seed = seed().scale(.43).rotate(.18).move_to(pt(-2.58, -2.65))
        planter = place_pot(pot(), (.08, -2.35, 0), 1.07)
        question = question_card("Where do new\nbeans come from?", left=2.51, y=1.11,
                                 max_w=4.05, size=35).question
        self.add(plate, green_pod, dry_seed, planter)
        self.at("where do new")
        self.play(FadeIn(question, shift=UP * .1), run_time=.6)
        self.at("grow a bean")
        wheel, spokes, _ = cycle_wheel()
        self.play(FadeOut(VGroup(plate, green_pod)), dry_seed.animate.move_to(pt(-1.96, 1.91)),
                  planter.animate.shift(LEFT * 2.04 + UP * 1.52), run_time=1.22)
        self.add(wheel, spokes)
        self.bring_to_front(dry_seed, planter)
        self.play(FadeIn(wheel), LaggedStart(*[Create(s) for s in spokes], lag_ratio=.18), run_time=1.1)
        self.at("over about")
        months = notably("About 3 months", PAPER)
        self.play(swap(question, months), run_time=.68)
        pointer = Dot(radius=.105, color=YELLOW).move_to(pt(-1.96, 2.64))
        track = Arc(radius=2.53, start_angle=PI / 2, angle=-TAU * .92, arc_center=pt(-1.96, .11))
        self.add(pointer)
        self.play(MoveAlongPath(pointer, track, rate_func=linear), run_time=4.2)
        self.at("checking a guess")
        self.play(Indicate(dry_seed, color=YELLOW, scale_factor=1.10), run_time=.65)
        self.finish()


class S02Title(TitleCard):
    TITLE = "From Bean to Bean: Parent Guide"
    LESSON = "From Bean to Bean"

    def construct(self):
        self.add(windowsill())
        plate, spokes, _ = cycle_wheel()
        planter = place_pot(pot(), (-1.96, -.83, 0), 1.07)
        self.add(plate, spokes, planter, seed().scale(.43).rotate(.18).move_to(pt(-1.96, 1.91)))
        title = T(self.LESSON, 49, TEXT, font=TITLE_FONT).move_to(pt(1, .98))
        subtitle = T("Parent Activity Guide", 31, PAPER).move_to(pt(1, .25))
        panel = tile(9.65, 1.98, 1, .65, WALL, outline=GOLD, width=2.5)
        self.add(panel)
        self.play(FadeIn(VGroup(title, subtitle), shift=UP * .10), run_time=.46)
        self.wait(max(.1, self.narration_s - self.elapsed()))


class S04Safety(SpokenScene):
    def construct(self):
        self.add(windowsill())
        pack = packet().move_to(pt(-3.68, -.20))
        seeds = VGroup(*[seed().scale(.27).rotate(a).move_to(pt(x, y)) for x, y, a in
                         [(-.97, -2.38, .31), (-.41, -2.70, -.31), (.10, -2.31, .20)]])
        adult = hand().scale(1.47).rotate(-.19).move_to(pt(-5.11, -.27))
        self.add(pack, seeds, adult)
        self.at("untreated bush", lead=.45)
        label = notably("Untreated\nbush bean seeds", PAPER)
        self.play(FadeIn(label), adult.animate.shift(RIGHT * .48), run_time=.56)
        self.at("check for bean")
        allergy = notably("Check legume\nallergies", PAPER)
        self.play(swap(label, allergy), adult.animate.rotate(-.18).shift(UP * .20), run_time=.72)
        self.at("stay with your")
        child = hand("#E3B291", "#9C7481", -1).scale(.86).rotate(.14).move_to(pt(.90, -1.19))
        self.play(FadeOut(allergy), FadeIn(child, shift=LEFT * .50), run_time=.68)
        self.at("keep loose seeds")
        warning = notably("Under 4:\nchoking risk", RED)
        self.play(adult.animate.shift(RIGHT * 2.75 + DOWN * 1.49), FadeOut(child), run_time=.8)
        self.play(seeds.animate.shift(LEFT * 1.48 + UP * .49),
                  adult.animate.shift(LEFT * 1.45 + UP * .45), FadeIn(warning), run_time=1.05)
        self.at("call 911 if")
        call = notably("Call 911\nif choking", RED)
        self.play(swap(warning, call), run_time=.65)
        self.at("never taste the")
        plant = place_pot(VGroup(pot(), bush("none").shift(UP * 1.61)), (-2.03, -2.38, 0))
        no_taste = notably("No tasting", RED)
        self.play(FadeOut(VGroup(pack, adult, seeds)), swap(call, no_taste), run_time=.58)
        self.play(FadeIn(plant, shift=UP * .2), run_time=.55)
        self.at("wash hands after")
        self.play(FadeOut(VGroup(plant, no_taste)), run_time=.40)
        hands = VGroup(hand().scale(2.24).rotate(.22).move_to(pt(-2.94, -.15)),
                       hand(SKIN, SLEEVE, -1).scale(2.00).rotate(-.32).move_to(pt(-.60, -.43)))
        bubbles = VGroup()
        for i, (x, y, r) in enumerate([(-3.2, .38, .22), (-2.5, .81, .28), (-1.85, .29, .34),
                                       (-1.2, .81, .20), (-1.34, 1.43, .24), (-2.1, 1.58, .14),
                                       (-3.55, 1.10, .15), (-.65, 1.26, .12)]):
            b = Circle(radius=r, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=.18).move_to(pt(x, y))
            bubbles.add(bob(b, amp=.25, speed=2.2, seed=i))
        wash = notably("Wash hands", BLUE)
        self.play(FadeIn(hands), FadeIn(wash), run_time=.53)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bubbles], lag_ratio=.13),
                  hands[1].animate.shift(LEFT * .62 + UP * .12), run_time=1.24)
        self.finish()


class S03GatherPeek(SpokenScene):
    def construct(self):
        self.add(windowsill())
        mix = bag().scale(1.26).move_to(pt(-4.64, -.63))
        pots = VGroup(place_pot(pot(), (-1.71, -2.32, 0), .74),
                      place_pot(pot(cut=True), (1.02, -2.32, 0), .74))
        self.add(mix)
        self.at("two or three", lead=.37)
        self.play(LaggedStart(*[FadeIn(planter, shift=UP * .36) for planter in pots],
                              lag_ratio=.30), run_time=1.10)
        self.at("drainage holes")
        drain = pots[1][-1]
        self.play(Indicate(drain, color=BLUE, scale_factor=1.42), run_time=.82)
        self.at("soak one extra")
        bowl = VGroup(oval(4.8, 1.95, -2.02, -.88, "#355968", BLUE, 4),
                      oval(4.15, 1.47, -2.02, -.79, "#598A9D", BLUE, 2))
        wet_seed = seed().scale(1.53).move_to(pt(-2.02, -.60))
        overnight = notably("Soak one extra\nbean overnight", BLUE)
        self.play(FadeOut(VGroup(mix, pots)), FadeIn(bowl), FadeIn(wet_seed, shift=DOWN * .40),
                  FadeIn(overnight), run_time=.86)
        ripple = Ellipse(width=2.55, height=.76, color=BLUE, stroke_width=2.4).move_to(pt(-2.02, -.69))
        self.play(GrowFromCenter(ripple), run_time=.62)
        self.play(FadeOut(ripple, scale=1.54), run_time=.70)
        self.at("help your child")
        adult = hand().scale(1.53).rotate(-.20).move_to(pt(-4.41, -.28))
        child = hand("#E3B291", "#9C7481", -1).scale(1.34).rotate(.25).move_to(pt(.15, -.66))
        self.play(FadeOut(bowl), FadeOut(overnight), FadeIn(adult, shift=RIGHT * .42),
                  FadeIn(child, shift=LEFT * .42), run_time=.55)
        self.at("peel it")
        skin = wet_seed.copy()
        self.add(skin)
        inner = seed(PAPER, hilum=False).scale(1.49).move_to(wet_seed)
        self.remove(wet_seed)
        self.add(inner)
        self.bring_to_front(skin, adult, child)
        self.play(skin.animate.scale(.53).rotate(.77).shift(LEFT * 1.8 + UP * 1.20),
                  adult.animate.shift(LEFT * .32 + UP * .48), run_time=.78)
        self.at("split it open")
        left_half = seed(PAPER, hilum=False).scale(1.14).rotate(.39).move_to(pt(-3.43, -.77))
        right_half = seed("#F9EAC8", hilum=False).scale(1.14).rotate(-.34).move_to(pt(-.62, -.77))
        second_half = inner.copy()
        self.add(second_half)
        self.play(Transform(inner, left_half), Transform(second_half, right_half),
                  child.animate.shift(RIGHT * .35), FadeOut(skin), run_time=.71)
        self.at("tiny leaves")
        embryo = VGroup(stroke([(0, -.40), (-.10, -.19), (0, .01), (.13, .18)], LEAF_DARK, 5, True),
                        leaf(.55, GREEN, 2.68), leaf(.62, GREEN, .72)).move_to(pt(-.72, -.58))
        tiny = notably("Tiny leaves", GREEN)
        self.play(GrowFromCenter(embryo), FadeIn(tiny), run_time=.60)
        self.at("ask what do")
        question = question_card("What do you think\nthis will become?", y=1.1, left=2.48,
                                 max_w=3.92, size=32).question
        self.play(swap(tiny, question), run_time=.61)
        self.at("toss the soaked")
        bin_body = form([(-3.3, -.67), (-.63, -.67), (-.89, -2.53), (-3.01, -2.53)],
                        "#376572", BLUE, 3)
        rim = tile(2.89, .23, -1.96, -.63, "#6793A0")
        contents = VGroup(inner, second_half, embryo)
        self.play(FadeOut(VGroup(child, question)), FadeIn(bin_body), FadeIn(rim),
                  contents.animate.scale(.39).move_to(pt(-1.96, .18)),
                  adult.animate.shift(RIGHT * 1.08 + UP * .19), run_time=.58)
        self.play(FadeOut(contents, shift=DOWN * 1.55), run_time=.56)
        self.finish()


def soil_fill():
    cross_section = form([(-1.13, 1.08), (1.13, 1.08), (.82, -.15), (-.82, -.15)],
                         SOIL, width=0)
    details = VGroup(*[oval(r, .58 * r, x, y, SEED_LINE) for x, y, r in
                       [(-.74, .93, .13), (-.51, .36, .11), (-.22, .91, .10), (.15, .58, .14),
                        (.31, .24, .08), (.84, .79, .11), (.58, .40, .13), (-.61, .13, .09)]])
    surface = Line(pt(-1.13, 1.08), pt(1.13, 1.08), color=SEED_LINE, stroke_width=3)
    return VGroup(cross_section, details, surface)


def measure_bracket(x, top, bottom):
    return stroke([(x - .14, top), (x, top), (x, bottom),
                   (x - .14, bottom)], PAPER, 3)


def stake(at=POT_AT, scale=POT_SCALE, cut=False):
    stick = tile(.44, 1.15, .86, 2.16, SEED, radius=.12, outline=SEED_LINE, width=2)
    # Handwritten date strokes read as a dated marker without fixing a planting date.
    ticks = VGroup(*[stroke([(.74, y), (.96, y + .03)], SEED_LINE, 1.9) for y in (2.54, 2.39, 2.24)])
    marker = VGroup(stick, ticks).rotate(-.13, about_point=stick.get_center())
    if cut:
        marker.shift(DOWN * .51)
    return place_pot(marker, at, scale)


def notebook():
    back = tile(3.04, 2.26, 4.38, -1.65, "#528C88", outline=TEAL, width=3)
    page = form([(3.02, -.63), (5.77, -.63), (5.77, -2.55), (3.02, -2.55)], PAPER, width=0)
    binding = VGroup(*[Line(pt(2.85, y), pt(3.11, y), color=INK, stroke_width=3)
                       for y in np.linspace(-.83, -2.32, 6)])
    return VGroup(back, page, binding)


class S05PlantPredict(SpokenScene):
    def construct(self):
        self.add(windowsill())
        mix = bag().scale(1.23).move_to(pt(-4.88, -.45))
        pouring = water_stream(-4.89, 2.30, 1.26)
        scoop = VGroup(tile(1.06, .22, -.59, .14, FRAME),
                       form([(-.22, .29), (.83, .33), (.57, -.19), (-.12, -.19)], BLUE, FRAME, 2),
                       oval(.68, .22, .27, .26, SOIL))
        handle = scoop[0]
        scoop_load = scoop[2]
        adult = hand().scale(.72, about_point=ORIGIN).shift(handle.get_center() + LEFT * .17)
        held_scoop = VGroup(scoop, adult).shift(pt(-4.48, 1.10) - scoop_load.get_center())
        self.add(mix, pouring)
        self.at("before scooping")
        self.remove(pouring)
        self.play(FadeIn(held_scoop, shift=UP * .58), run_time=.85)
        self.at("fill each pot")
        enlarged_at = (-1.90, -2.0, 0)
        scale = 1.52
        planter = place_pot(pot(cut=True), enlarged_at, scale)
        soil = place_pot(soil_fill(), enlarged_at, scale)
        self.play(FadeIn(planter),
                  held_scoop.animate.shift(pt(-2.30, 1.37) - scoop_load.get_center()), run_time=.87)
        self.play(GrowFromEdge(soil, DOWN),
                  Rotate(held_scoop, -.62, about_point=handle.get_center()), run_time=.76)
        self.at("below the rim")
        top_y = enlarged_at[1] + scale * 1.48
        soil_y = enlarged_at[1] + scale * 1.08
        level_marker = measure_bracket(.65, top_y, soil_y)
        level = notably("About 2 cm\nbelow the rim", PAPER)
        self.play(FadeOut(VGroup(held_scoop, mix)), Create(level_marker), FadeIn(level), run_time=.66)
        self.at("plant two or")
        grains = VGroup(*[seed().scale(.32).rotate(a).move_to(pt(x, 1.32)) for x, a in
                          [(-2.89, .14), (-1.91, -.31), (-.99, .17)]])
        self.play(FadeOut(VGroup(level, level_marker)), FadeIn(grains, shift=DOWN * .22), run_time=.57)
        self.at("about 3 cm")
        depth_y = soil_y - .88
        depth_marker = measure_bracket(.65, soil_y, depth_y)
        depth = notably("About 3 cm deep", PAPER)
        self.play(grains.animate.set_y(depth_y), Create(depth_marker), FadeIn(depth), run_time=1.04)
        self.at("cover them")
        self.play(FadeOut(VGroup(depth, depth_marker)),
                  FadeOut(grains, shift=DOWN * .17), run_time=.57)
        self.at("water until it")
        falling = water_stream(-1.90, 2.18, 2.46)
        drip = water_stream(-1.90, -2.37, .24, count=2)
        self.add(falling)
        self.wait(.75)
        self.add(drip)
        self.at("date the label")
        self.remove(falling, drip)
        label = stake(enlarged_at, scale, cut=True)
        self.play(FadeIn(label, shift=DOWN * .58), run_time=.78)
        self.at("use your sunniest")
        sun = notably("Sunniest window", PAPER, 1.36)
        self.play(Transform(planter, place_pot(pot())), FadeOut(soil), FadeIn(sun),
                  Transform(label, stake()), run_time=1.48)
        frost = notably("Outdoors after\nlast spring frost", PAPER, 1.36)
        self.at("plant outside after")
        self.play(swap(sun, frost), run_time=.70)
        self.at("write down your")
        book = notebook()
        writing = pencil().rotate(-.28).move_to(pt(2.61, -1.09))
        guess = notably("Sprouting guess", TEAL)
        self.play(swap(frost, guess), FadeIn(book), FadeIn(writing), run_time=.60)
        mark = stroke([(3.35, -1.43), (3.58, -1.35), (3.82, -1.45), (4.03, -1.34),
                       (4.29, -1.44), (4.66, -1.38), (5.16, -1.42)], INK, 3, True)
        self.play(Create(mark), writing.animate.shift(RIGHT * 1.49), run_time=1.06)
        self.finish()


def calendar():
    back = tile(3.34, 2.74, 4.39, -.37, PAPER, outline=SEED, width=3)
    header = tile(3.34, .56, 4.39, .72, CLAY, radius=.16)
    squares = VGroup(*[tile(.28, .24, 3.31 + .43 * col, .15 - .40 * row, SEED,
                             radius=.035) for row in range(4) for col in range(6)])
    return VGroup(back, header, squares)


def ruler():
    x, y = .55, -.81
    face = tile(.56, 3.35, x, y + 1.66, SEED, radius=.07, outline=SEED_LINE, width=2)
    ticks = VGroup(*[Line(pt(x - .27, y + i * .32), pt(x + (.05 if i % 5 == 0 else -.12), y + i * .32),
                          color=INK, stroke_width=2.3) for i in range(11)])
    return VGroup(face, ticks)


def shears():
    blades = VGroup(form([(-.07, -.07), (1.27, .28), (.80, .06), (0, -.16)], "#B8CBCD"),
                    form([(-.07, .07), (1.27, -.28), (.80, -.06), (0, .16)], "#9BADB1"))
    handles = VGroup(*[Ellipse(width=.6, height=.31, color=RED, stroke_width=7).move_to(pt(-.38, y))
                       for y in (-.24, .24)])
    return VGroup(blades, handles, Dot(radius=.075, color=FRAME))


class S06WeeklyVisit(SpokenScene):
    def construct(self):
        self.add(windowsill(), place_pot(pot()), stake())
        weekly = calendar()
        lead_plant = sprout(2.84).shift(pt(-1.95, -.81))
        small = sprout(1.17).shift(pt(-2.79, -.81))
        medium = sprout(1.78).shift(pt(-1.45, -.81))
        self.add(weekly)
        self.at("visit together weekly")
        weeks = notably("About 10–15 weeks", PAPER, 2.01)
        self.play(FadeIn(weeks), LaggedStart(GrowFromEdge(small, DOWN), GrowFromEdge(medium, DOWN),
                                           GrowFromEdge(lead_plant, DOWN), lag_ratio=.36),
                  run_time=2.58)
        page = weekly[2].copy()
        self.play(FadeOut(page, shift=UP * .68, scale=.87), run_time=.45)
        self.at("measure the tallest")
        tool = ruler()
        guide = DashedLine(pt(-1.62, lead_plant.get_top()[1]), pt(.25, lead_plant.get_top()[1]),
                           color=PAPER, dash_length=.095, stroke_width=2.6)
        adult = hand(SKIN, SLEEVE, -1).scale(.80).rotate(.19).move_to(pt(1.34, -.86))
        self.play(FadeOut(VGroup(weekly, weeks)), FadeIn(tool, shift=DOWN * .33),
                  FadeIn(adult, shift=LEFT * .36), run_time=.70)
        self.play(Create(guide), run_time=.53)
        self.at("with string and")
        string = Line(pt(.52, -.81), pt(.52, lead_plant.get_top()[1]), stroke_width=6, color=PAPER)
        blocks = VGroup(*[tile(.67, .48, 1.17, -.57 + i * .48, col, radius=.055)
                         for i, col in enumerate([TEAL, CLAY, BLUE, GREEN, GOLD, "#957A9B"])])
        self.play(FadeOut(tool), FadeOut(adult), Create(string), run_time=.58)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * .17) for b in blocks], lag_ratio=.15), run_time=1.20)
        self.at("count leaves")
        book = notebook().shift(UP * 1.30)
        drawing = sprout(.95).move_to(pt(4.32, -.35))
        self.play(FadeOut(VGroup(string, blocks, guide)), FadeIn(book), run_time=.55)
        self.play(Create(drawing), Indicate(lead_plant[1], color=YELLOW, scale_factor=1.10),
                  Indicate(lead_plant[2], color=YELLOW, scale_factor=1.10), run_time=1.09)
        self.at("water when the")
        water = water_stream(-1.24, .80, 1.53, 4)
        self.play(FadeOut(VGroup(book, drawing)), run_time=.46)
        self.add(water)
        self.at("at about 5")
        self.remove(water)
        mark = notably("At about 5 cm", PAPER)
        self.play(FadeIn(mark), run_time=.51)
        self.at("snip all but")
        scissors = shears().rotate(.11).move_to(pt(-3.85, -.66))
        holding = hand().rotate(.04).move_to(pt(-4.72, -.65))
        self.play(FadeIn(holding, shift=RIGHT * .32), FadeIn(scissors, shift=RIGHT * .32), run_time=.62)
        self.play(scissors[0][0].animate.rotate(-.15, about_point=scissors.get_center()),
                  scissors[0][1].animate.rotate(.15, about_point=scissors.get_center()),
                  FadeOut(small, shift=LEFT * .41 + DOWN * .17), run_time=.65)
        self.play(FadeOut(VGroup(mark, scissors, holding)), run_time=.39)
        # One smaller plant stays alongside the strongest during the thinning beat.
        self.play(FadeOut(medium), Transform(lead_plant, planted()), run_time=.85)
        self.finish()


def bee():
    wings = VGroup(oval(.52, .67, -.19, .32, "#BCE3E7", BLUE, 2).rotate(.28),
                   oval(.45, .63, .29, .32, "#BCE3E7", BLUE, 2).rotate(-.4))
    body = oval(1.03, .59, 0, 0, YELLOW, INK, 2)
    stripes = VGroup(*[Line(pt(x, -.22), pt(x + .04, .23), color=INK, stroke_width=5)
                       for x in (-.15, .12)])
    head = oval(.34, .33, .48, .07, INK)
    return VGroup(wings, body, stripes, head)


def no_bee():
    center = pt(-4.67, 1.29)
    icon = bee().scale(.90).move_to(center)
    ring = DashedVMobject(Circle(radius=.88, color=PAPER, stroke_width=3).move_to(center),
                          num_dashes=14, dashed_ratio=.66)
    slash = Line(center + .62 * UL, center + .62 * DR, color=RED, stroke_width=5)
    return VGroup(icon, ring, slash)


def prediction_world():
    return VGroup(windowsill(), place_pot(pot()), stake(), planted(), no_bee())


def sway(plant, speed=1.4, angle=.053):
    base = pt(POT_AT[0], POT_AT[1] + POT_SCALE * 1.61)
    original = plant.copy()
    plant.phase = 0.0

    def lean(mob, dt):
        mob.phase += dt * speed
        mob.become(original.copy().rotate(angle * np.sin(mob.phase), about_point=base))

    return plant.add_updater(lean)


class S07PredictQ(SpokenScene):
    def construct(self):
        table, planter, label, plant, bee_mark = prediction_world()
        self.add(table, planter, label, sway(plant))
        self.at("before the flowers")
        self.wait(.42)
        self.at("suppose your beans")
        outdoor = bee().scale(.9).move_to(pt(-5.68, 1.63))
        self.play(FadeIn(outdoor, shift=RIGHT * 1.01 + DOWN * .34), run_time=1.17)
        self.at("no bees at")
        self.remove(outdoor)
        self.add(bee_mark[0])
        self.play(Create(bee_mark[1]), Create(bee_mark[2]), run_time=.74)
        self.at("will those flowers")
        q = question_card(QUESTION, **QUESTION_STYLE).question
        self.play(FadeIn(q, shift=UP * .10), run_time=.61)
        self.finish()


class S08PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    RING_AT = RING_AT
    SECONDS = 4.5

    def backdrop(self):
        table, planter, label, plant, bee_mark = prediction_world()
        return VGroup(table, planter, label, sway(plant), bee_mark)


def bud_section(opened=False):
    x, y = -2.05, .52
    stem = stroke([(x - .42, -2.31), (x - .20, -1.77), (x, y - 1.25)],
                  LEAF_DARK, 13, True)
    sepals = VGroup(leaf(1.06, LEAF_DARK, 2.52), leaf(1.11, LEAF_DARK, .61)).shift(pt(x, y - 1.11))
    petal = shape((0, -1.15), [
        ((-1.44, -.91), (-1.48, .92), (-.08, 1.57)),
        ((.91, 1.46), (1.48, -.14), (.70, -.94)),
        ((.45, -1.22), (.23, -1.23), (0, -1.15)),
    ], "#EDF1DF", "#A6C5B7", 4).shift(pt(x, y))
    interior = shape((0, -1.05), [
        ((-.91, -.45), (-.67, .73), (-.07, 1.27)),
        ((.78, .83), (.99, -.54), (.40, -.95)),
        ((.20, -1.08), (.11, -1.15), (0, -1.05)),
    ], "#ABC6B4", "#DCE8D5", 2).shift(pt(x, y))
    if opened:
        petal = flower().scale(3.48).shift(pt(x, y))
        interior = oval(.44, 1.14, x, y - .50, "#76A96E", LEAF_DARK, 3)
    center = VGroup(oval(.42, .61, x, y - .77, LEAF_DARK),
                    stroke([(x, y - .58), (x + .09, y - .09), (x, y + .45)],
                           LEAF_DARK, 7, True),
                    oval(.30, .15, x, y + .45, LEAF_DARK))
    return VGroup(stem, petal, interior, sepals, center)


def sprout_time():
    panels = TwoPanel("Sprouts in warm weather", "Flowers",
                      colors=(PAPER, PAPER), top=1.98, bottom=-2.06,
                      gap=.35, width=9.55, size=30).shift(LEFT * 1.93)
    for frame in (panels.left_frame, panels.right_frame):
        frame.set_fill("#263B3B", opacity=1).set_stroke(FRAME)
    left_x, right_x = panels.left_frame.get_x(), panels.right_frame.get_x()
    sprig = sprout(1.63, hooked=True).move_to(pt(left_x, .09))
    bloom = flower().scale(1.41).move_to(pt(right_x, .14))
    first = T("Usually 5–14 days", 31, TEXT).move_to(pt(left_x, -1.32))
    second = fit_text("Usually about 4–7 weeks", max_w=4.1, size=29).move_to(pt(right_x, -1.32))
    return (VGroup(panels.left_frame, panels.left_head), sprig, first,
            VGroup(panels.right_frame, panels.right_head), bloom, second)


class S09PredictReveal(SpokenScene):
    def construct(self):
        table, planter, label, plant, bee_mark = prediction_world()
        q = question_card(QUESTION, **QUESTION_STYLE).question
        self.add(table, planter, label, plant, bee_mark, q)
        self.at("they can make")
        section = bud_section()
        answer = notably("They can make pods", GREEN)
        self.play(FadeOut(VGroup(planter, label, plant, bee_mark)), swap(q, answer),
                  GrowFromPoint(section, pt(-1.91, 2.43)), run_time=1.13)
        self.at("bean flowers mostly")
        pollen = VGroup(*[Dot(pt(x, y), radius=.081, color=YELLOW) for x, y in
                          [(-2.54, .73), (-2.65, .62), (-2.57, .48), (-1.53, .53), (-1.61, .35)]])
        self.play(FadeIn(pollen), run_time=.35)
        self.at("pollinate themselves")
        selfing = notably("Mostly self-pollinate", GREEN)
        targets = VGroup(*[Dot(pt(-2.10 + i * .05, .98 - abs(i - 2) * .043),
                              radius=.072, color=YELLOW) for i in range(5)])
        self.play(Transform(pollen, targets), swap(answer, selfing), run_time=1.29)
        self.at("often before opening", lead=.48)
        open_flower = bud_section(opened=True)
        self.play(Transform(section, open_flower), run_time=.55)
        new_pod = pod().scale(1.17).rotate(-.97).move_to(pt(-1.58, -.32))
        self.play(FadeOut(pollen), ReplacementTransform(section, new_pod), run_time=.65)
        self.at("in warm weather", lead=.04)
        left_back, stem, germ, right_back, bloom, flowers_time = sprout_time()
        schematic = scope_tag(size=28, color=PAPER)
        self.play(FadeOut(VGroup(new_pod, selfing)), FadeIn(left_back),
                  FadeIn(schematic), run_time=.61)
        self.at("hooked stem usually")
        self.play(GrowFromEdge(stem, DOWN), run_time=.76)
        self.play(FadeIn(germ), run_time=.55)
        self.at("flowers usually open")
        self.play(FadeIn(right_back), GrowFromCenter(bloom), run_time=.80)
        self.play(FadeIn(flowers_time), run_time=.58)
        self.at("ask your child")
        q2 = question_card("What will grow\nwhere the\nflowers are?", left=2.58, y=.94,
                           max_w=3.85, size=31).question
        self.play(FadeOut(VGroup(left_back, stem, germ, right_back, bloom, flowers_time, schematic)),
                  run_time=.43)
        self.play(FadeIn(planter), FadeIn(label), FadeIn(q2), run_time=.53)
        self.play(GrowFromEdge(planted("flowers"), DOWN), run_time=1.06)
        self.finish()


def saucepan():
    body = form([(-1.62, .44), (1.59, .44), (1.22, -1.00), (-1.18, -1.00)],
                "#63828B", "#ACBCC0", 3)
    handle = tile(1.37, .27, 2.06, .08, "#89A2A7", radius=.11)
    lip = oval(3.27, .55, 0, .44, "#BCCDD0", FRAME, 3)
    water = oval(2.94, .40, 0, .45, "#527E91", BLUE, 2)
    beans = VGroup(*[pod().scale(.42).rotate(a).move_to(pt(x, y)) for x, y, a in
                     [(-.59, .45, .08), (.45, .43, -.22)]])
    return VGroup(handle, body, lip, water, beans)


def boil_bubbles():
    bubbles = VGroup()
    for i, (x, r) in enumerate([(3.10, .095), (3.44, .15), (3.89, .13), (4.16, .11),
                               (4.51, .13), (4.90, .10), (5.08, .075)]):
        bubble = Circle(radius=r, color=BLUE, stroke_width=2.8)
        bubble.age = i / 7

        def rise(mob, dt, x=x):
            mob.age = (mob.age + .87 * dt) % 1
            mob.move_to(pt(x + .09 * np.sin(4 * mob.age), -.86 + 1.12 * mob.age))
            mob.set_opacity(min(1, mob.age * 8, (1 - mob.age) * 7))

        bubbles.add(bubble.add_updater(rise, call_updater=True))
    return bubbles


class S10RipenCircle(SpokenScene):
    def construct(self):
        self.add(windowsill(), place_pot(pot()), stake())
        plant = planted("flowers")
        self.add(plant)
        self.at("tiny pods show")
        target = planted("tiny")[2]
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(plant[2], target)],
                              lag_ratio=.27), run_time=2.31)
        early = notably("Within 1–2 weeks\nof first flowers", PAPER)
        self.play(FadeIn(early), run_time=.58)
        self.at("green pods are")
        target = planted("green")[2]
        self.play(FadeOut(early), LaggedStart(*[Transform(a, b) for a, b in zip(plant[2], target)],
                                              lag_ratio=.20), run_time=1.28)
        self.at("pick about seven")
        picking = notably("Picking: about\n7–9 weeks", GREEN)
        self.play(FadeIn(picking), run_time=.62)
        self.at("for eating later")
        pan = saucepan().scale(.85, about_point=ORIGIN).shift(pt(4.12, -1.28))
        harvest = pod().scale(.46).rotate(-.20).move_to(pt(-.78, 1.19))
        adult = hand(SKIN, SLEEVE, -1).scale(.77).move_to(pt(.08, 1.22))
        self.play(FadeOut(picking), FadeIn(adult, shift=LEFT * .29),
                  GrowFromPoint(harvest, pt(-.85, 1.66)), FadeIn(pan), run_time=.62)
        self.at("adult boils picked")
        self.play(harvest.animate.move_to(pt(3.89, -.82)), adult.animate.shift(RIGHT * 3.71 + DOWN * 1.65),
                  run_time=.79)
        self.remove(harvest)
        bubbles = boil_bubbles()
        self.add(bubbles)
        boil = notably("Boil 30 minutes\nor more", BLUE, 1.18)
        self.play(FadeOut(adult), FadeIn(boil), run_time=.57)
        self.at("leave at least")
        # The harvest leaves three pods where they grew.
        self.play(FadeOut(pan), FadeOut(boil), run_time=.50)
        self.remove(bubbles)
        remaining = notably("Leave at least 3 pods", GREEN)
        self.play(FadeIn(remaining), LaggedStart(*[Indicate(p, color=YELLOW, scale_factor=1.12)
                                                 for p in plant[2]], lag_ratio=.34), run_time=1.35)
        self.finish()


class S10Compare(SpokenScene):
    def construct(self):
        planter, marker = place_pot(pot()), stake()
        self.add(windowsill(), planter, marker)
        plant = planted("green")
        self.add(plant)
        self.at("over the next")
        weeks = notably("Over the next\n3–6 weeks", PAPER)
        self.play(FadeIn(weeks), Transform(plant[2], planted("yellow")[2]), run_time=1.18)
        self.at("the pods dry")
        self.play(Transform(plant[2], planted("dry")[2]), run_time=.72)
        self.at("the seeds rattle")
        dry = pod(SEED).scale(1.18).rotate(.08).move_to(pt(-2.10, .32))
        self.play(FadeOut(VGroup(plant, planter, marker)), FadeOut(weeks),
                  GrowFromPoint(dry, pt(-1.1, 1.1)), run_time=.64)
        self.play(Wiggle(dry, scale_value=1.035, rotation_angle=.11, n_wiggles=4), run_time=1.0)
        self.at("ask will the")
        q = question_card("Will the new seeds\nlook like the one\nwe planted?", left=2.48, y=.88,
                          max_w=4.05, size=32).question
        self.play(FadeIn(q), run_time=.65)
        self.at("open a dry")
        adult = hand().scale(1.12).rotate(-.26).move_to(pt(-4.61, .30))
        child = hand("#E3B291", "#9C7481", -1).scale(.86).rotate(.27).move_to(pt(.23, .30))
        self.play(FadeIn(adult, shift=RIGHT * .37), FadeIn(child, shift=LEFT * .39),
                  FadeOut(q), run_time=.52)
        opened = pod(SEED, opened=True).scale(1.23).rotate(.08).move_to(pt(-2.10, .12))
        lid = dry.copy()
        self.add(lid)
        self.play(Transform(dry, opened), lid.animate.rotate(.20).shift(UP * .92),
                  adult.animate.shift(UP * .58), run_time=.76)
        self.at("compare its seeds")
        two = [seed().scale(.83).rotate(.15).move_to(pt(x, -.36)) for x in (3.19, 5.30)]
        label_new = T("New seed", 28, TEXT).move_to(pt(3.19, -1.24))
        label_old = T("Packet seed", 28, TEXT).move_to(pt(5.30, -1.24))
        label_box = tile(4.40, 2.75, 4.26, -.40, "#273641", outline=FRAME, width=2.4)
        self.play(FadeOut(VGroup(adult, child, lid)), FadeIn(label_box),
                  GrowFromPoint(two[0], pt(-1.95, .11)), GrowFromPoint(two[1], pt(5.3, 1.1)),
                  run_time=.85)
        self.play(FadeIn(label_new), FadeIn(label_old), run_time=.57)
        self.at("after the seeds")
        self.play(FadeOut(VGroup(dry, label_box, *two, label_new, label_old)),
                  FadeIn(VGroup(plant, planter, marker)), run_time=.74)
        self.at("the plant yellows")
        self.play(Transform(plant, planted("none", dying=True)), run_time=1.46)
        self.finish()


class S11WheelClose(SpokenScene):
    def construct(self):
        self.add(windowsill())
        ring, _, _ = cycle_wheel()
        plate, spokes, icons = cycle_wheel(paper=True)
        self.add(ring)
        self.at("divide a paper")
        self.play(Transform(ring, plate), run_time=.70)
        self.play(LaggedStart(*[Create(s) for s in spokes], lag_ratio=.22),
                  run_time=1.53)
        for phrase, illustration in zip(("draw a seed", "a sprout", "a leafy plant", "flowers and", "pod with seeds"), icons):
            self.at(phrase, lead=.16)
            self.play(DrawBorderThenFill(illustration), run_time=.53)
        self.at("draw an arrow")
        arc, tip = wheel_arrow()
        self.play(Create(arc), run_time=1.22)
        self.play(FadeIn(tip), run_time=.24)
        self.at("making a guess")
        guess = notably("Make a guess", TEAL, 1.08)
        self.play(FadeIn(guess), run_time=.59)
        self.at("checking it against")
        check = notably("Check what you saw", TEAL, 1.08)
        self.play(swap(guess, check), Indicate(icons[0], color=YELLOW, scale_factor=1.08), run_time=.81)
        pulse(arc, base=7, amp=1.8, speed=2.5)
        self.finish()


class S12End(EndCard):
    LINE = "One bean grows, flowers, makes new beans, and completes the circle."
