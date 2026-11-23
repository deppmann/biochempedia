"""A parent's listening walk, drawn as one warm, cut-paper backyard."""
from bp_parts import *

# COLOR MAP: GREEN for living sources, BLUE/TEAL for sound and the test,
# GOLD for questions and circles, RED for safety, GREY for road and hardware.
SKY = "#202A38"
LAWN = "#486657"
LAWN_LIGHT = "#66826A"
WOOD = "#906950"
LEAF = "#518552"
PAPER = "#FAE7BD"
INK = "#2B303B"
SKIN = "#DBA678"
SHIRT = "#3C8C98"
CHILD = "#C26947"
MAT = "#B57050"
SOUND = "#9ED7E0"


def point(x, y):
    return np.array([x, y, 0.0])


def slab(w, h, x, y, color, radius=0.12):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            stroke_width=0, fill_color=color, fill_opacity=1).move_to(point(x, y))


def oval(w, h, x, y, color):
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=color,
                   fill_opacity=1).move_to(point(x, y))


def shape(vertices, color):
    return Polygon(*(point(*xy) for xy in vertices), stroke_width=0,
                   fill_color=color, fill_opacity=1)


def line(x1, y1, x2, y2, color, width=4):
    return Line(point(x1, y1), point(x2, y2), color=color, stroke_width=width)


def place(drawing, x, y, width=None):
    if width is not None:
        drawing.set_width(width)
    return drawing.move_to(point(x, y))


def yard(sway=False):
    sky = slab(13.5, 7.5, 0, 0, SKY, 0.25)
    hills = shape([(-6.72, -0.7), (-6.72, 0.15), (-4.5, 0.38),
                   (-2, 0.18), (1.2, 0.53), (4.1, 0.72), (6.72, 0.51),
                   (6.72, -0.7)], "#394F4D")
    road = shape([(3.3, 0.26), (6.72, 0.55), (6.72, -0.32), (0.2, -0.61)], "#666E78")
    fence = VGroup(slab(7.4, 0.12, 3.0, -0.22, WOOD),
                   slab(7.4, 0.12, 3.0, -0.66, WOOD),
                   *(slab(0.16, 0.86, x, -0.41, "#AA7C5B") for x in np.linspace(-0.6, 6.6, 11)))
    grass = slab(13.5, 3.14, 0, -2.16, LAWN, 0.22)
    foreground = shape([(-6.69, -3.42), (-3.7, -2.91), (-0.8, -3.05), (3.5, -2.6),
                        (6.69, -2.78), (6.69, -3.64), (-6.69, -3.64)], LAWN_LIGHT)
    tree = shape([(-5.15, -2.38), (-4.78, 0.15), (-5.42, 0.96), (-5.23, 1.13),
                  (-4.66, 0.65), (-4.35, 1.86), (-4.03, 1.98), (-4.24, 0.27),
                  (-2.83, 0.83), (-2.65, 0.72), (-4.18, -0.18), (-4.09, -2.38)], WOOD)
    canopy = VGroup(oval(2.5, 1.53, -5.25, 1.82, LEAF),
                    oval(2.4, 1.72, -4.45, 2.51, "#61955F"),
                    oval(2.16, 1.49, -3.62, 1.76, "#48754C"),
                    oval(1.58, 0.81, -4.8, 1.34, "#578757"))
    if sway:
        for i, crown in enumerate(canopy):
            bob(crown, amp=.18, speed=2.1, seed=i)
    return VGroup(sky, hills, road, fence, grass, foreground, tree, canopy)


def bird():
    return VGroup(shape([(-.59, -.12), (-.17, .12), (-.08, -.12)], TEAL),
                  oval(.66, .43, .01, -.06, TEAL), oval(.36, .34, .27, .13, BLUE),
                  shape([(.42, .17), (.64, .08), (.42, .04)], GOLD),
                  Dot(point(.34, .16), radius=.033, color=INK),
                  oval(.35, .16, -.08, -.06, "#377B87").rotate(.3),
                  line(.02, -.24, -.02, -.37, WOOD), line(.15, -.24, .12, -.37, WOOD))


def car():
    return VGroup(slab(1.34, .38, 0, -.04, BLUE), shape([(-.51, .12), (-.25, .42),
                  (.28, .42), (.53, .12)], BLUE),
                  shape([(-.36, .16), (-.2, .34), (.22, .34), (.38, .16)], SKY),
                  oval(.26, .26, -.42, -.23, INK), oval(.26, .26, .43, -.23, INK),
                  slab(.14, .09, .58, -.04, PAPER, .04))


def dog():
    return VGroup(oval(.77, .4, -.13, -.03, "#BD815B"), oval(.43, .42, .32, .18, "#BD815B"),
                  oval(.23, .22, .54, .1, SKIN), oval(.16, .31, .21, .26, WOOD).rotate(-.37),
                  line(-.39, -.06, -.64, .24, WOOD, 6), line(-.32, -.12, -.32, -.34, WOOD, 6),
                  line(.13, -.12, .13, -.34, WOOD, 6), Dot(point(.43, .24), radius=.035, color=INK))


def leaves():
    return VGroup(line(-.62, -.19, .58, .22, WOOD), oval(.56, .28, -.27, .11, LEAF).rotate(.64),
                  oval(.59, .28, .12, -.13, "#78A265").rotate(-.27),
                  oval(.53, .26, .38, .3, LEAF).rotate(.42))


def insect():
    return VGroup(oval(.68, .42, 0, 0, CHILD), oval(.23, .28, .33, 0, INK),
                  line(-.25, 0, .23, 0, INK), *(Dot(point(x, y), radius=.049, color=INK)
                  for x in [-.14, .09] for y in [-.10, .10]))


def arrivals():
    return VGroup(place(bird(), -3.04, 1.14, 1.1),
                  place(car(), 5.29, .50, 1.1), place(dog(), 3.84, -.17, 1.05))


def wave():
    return VGroup(*(Arc(radius=r, start_angle=-.61, angle=1.22, color=SOUND, stroke_width=5)
                    for r in [.31, .56, .82])).center()


def traveling_wave(start, end, offset=0, speed=.48, emphasis=1, opacity=1):
    origin, target = point(*start), point(*end)
    delta = target - origin
    mark = wave().scale(emphasis).rotate(np.arctan2(delta[1], delta[0]))
    mark.set_stroke(width=5 * emphasis ** 1.6)
    clock = 0

    def travel(mob, dt):
        nonlocal clock
        clock += dt
        phase = (offset + clock * speed) % 1
        mob.move_to(origin + phase * delta)
        mob.set_stroke(opacity=opacity * (.16 + .77 * np.sin(np.pi * phase) ** 1.1))

    travel(mark, 0)
    mark.add_updater(travel)
    return mark


def yard_waves(dog_sound=True):
    routes = [((-2.43, 1.0), (-.55, -.69), .06), ((-4.1, 1.32), (-2.0, -.66), .43),
              ((5.15, .28), (2.62, -1.04), .33)]
    if dog_sound:
        routes.append(((3.74, -.45), (1.62, -1.49), .74))
    return VGroup(*(traveling_wave(*route, emphasis=1.46) for route in routes))


def towel():
    mat = shape([(-2.55, -3.19), (2.85, -3.19), (1.98, -1.51), (-1.77, -1.51)], MAT)
    stripes = VGroup(*(line(-2.42 + d, -3.07 + d * .3, 2.69 - d, -3.07 + d * .3,
                             "#E0A179", 3) for d in [0, .27, .54]))
    return VGroup(mat, stripes)


def clipboard():
    return VGroup(slab(2.1, 2.6, 0, 0, WOOD), slab(1.85, 2.28, 0, -.04, PAPER),
                  slab(.79, .24, 0, 1.14, "#B8B4AA", .08))


def crayons():
    return VGroup(*(VGroup(slab(.91, .14, -.07, 0, color, .04),
                           shape([(.36, .07), (.55, 0), (.36, -.07)], color),
                           slab(.53, .15, -.1, 0, PAPER, .04)).rotate(a).shift(UP * y)
                    for color, a, y in [(TEAL, .22, -.22), (BLUE, -.13, .07), (GOLD, .13, .33)]))


def supplies():
    return VGroup(place(clipboard(), 1.51, -2.40, .87).rotate(-.16),
                  place(crayons(), 2.28, -2.65, .54))


def phone():
    return VGroup(slab(1.32, 2.24, 0, 0, INK), slab(1.12, 1.88, 0, .02, "#345263"),
                  slab(.36, .05, 0, -.99, GREY, .02))


def clock_face():
    return VGroup(Circle(radius=.24, stroke_color=GOLD, stroke_width=4),
                  line(0, 0, 0, .15, GOLD), line(0, 0, .10, -.04, GOLD))


def seat(color, facing=0, cupped=False, one_lap_hand=False):
    """Seated cut-paper person, with a profile nose and hands when viewed from the side."""
    legs = VGroup(oval(1.5, .34, 0, -.76, INK), oval(.86, .44, -.32, -.58, color),
                  oval(.86, .44, .32, -.58, color))
    torso = oval(1.17, 1.16, 0, -.22, color)
    head = oval(.83, .92, 0, .65, SKIN)
    hair = oval(.84 if not facing else .46, .83, -.17 if facing else -.025, .74, INK)
    if not facing:
        hands = VGroup(oval(.22, .24, -.61, -.53, SKIN), oval(.22, .24, .61, -.53, SKIN))
        return VGroup(legs, torso, head, hair, hands)
    nose = shape([(.35, .72), (.52, .57), (.34, .53)], SKIN)
    eye = line(.22, .69, .31, .69, INK, 2.5)
    ear_mark = oval(.18, .27, -.08, .59, "#B57357")
    if cupped:
        hands = VGroup(line(.12, -.32, -.32, .19, color, 15),
                       line(.25, -.28, .02, .22, color, 13),
                       oval(.23, .45, .02, .41, "#C58F68").rotate(.25),
                       oval(.24, .47, -.29, .48, SKIN).rotate(.25))
    else:
        hands = VGroup(line(.12, -.32, .45, -.4, color, 15), oval(.23, .27, .45, -.4, SKIN))
        if not one_lap_hand:
            hands.add(line(.25, -.28, .64, -.46, color, 13), oval(.21, .24, .64, -.46, SKIN))
    figure = VGroup(legs, torso, head, hair, nose, eye, ear_mark, hands)
    return figure if facing == 1 else figure.flip(UP)


def backyard_child(listening=False):
    return place(seat(CHILD, facing=int(listening), one_lap_hand=listening), .15, -1.85, 1.33)


def backyard_people(listening=False):
    return VGroup(place(seat(SHIRT), -1.43, -1.60, 1.72), backyard_child(listening))


def hand(fingers=1):
    palm = oval(.77, .86, 0, -.23, SKIN)
    thumb = oval(.23, .44, -.36, -.16, SKIN).rotate(.45)
    digits = VGroup(*(slab(.14, .55 - .047 * i, -.24 + i * .195, .39 - .023 * i, SKIN, .07)
                       for i in range(fingers)))
    return VGroup(palm, thumb, digits)


def listening_arm():
    return VGroup(line(.46, -1.86, .93, -1.48, CHILD, 16),
                  line(.93, -1.48, 1.25, -.86, SKIN, 13))


def raised_hand(fingers):
    return place(hand(fingers), 1.31, -.61, .64)


def fixed_text(words, x, y, size=36, color=TEXT):
    return T(words, size, color, weight=BOLD).move_to(point(x, y))


def prompt(words, y=2.64):
    return question_card(words, y=y, size=50, color=PAPER, max_w=10.3).shift(RIGHT * 1.3)


def timer_arc(tracker):
    x, y, radius = 4.33, 1.86, .85
    center = point(x, y)
    ring = Circle(radius=radius, color=GREY, stroke_width=7).move_to(center)
    progress = always_redraw(lambda: Arc(radius=radius, start_angle=PI / 2,
                                        angle=-TAU * max(.001, tracker.get_value()),
                                        arc_center=center, color=SOUND, stroke_width=12))
    number = fixed_text("2 min", x, y, 36)
    return VGroup(ring, progress, number)


def tally_sheet(show_count=False):
    pad = VGroup(slab(2.7, 1.72, 0, 0, PAPER), slab(.77, .13, 0, .77, WOOD, .05))
    if show_count:
        pad.add(fixed_text("Guess", -.65, .31, 28, INK), fixed_text("Heard", .66, .31, 28, INK),
                fixed_text("4", -.65, -.32, 42, INK),
                *(line(x, -.56, x, -.10, INK, 5) for x in [.43, .65, .87]))
    else:
        pad.add(fixed_text("Guess", 0, .33, 31, INK), fixed_text("4", 0, -.31, 46, INK))
    return pad.move_to(point(4.57, -1.83))


class S01Hook(SpokenScene):
    def construct(self):
        self.add(yard(), arrivals())
        waves = yard_waves()
        question = prompt("How many sounds?")
        self.at("How many sounds")
        self.add(waves)
        self.play(FadeIn(question, shift=DOWN * .12), run_time=.65)
        self.at("Most of the time")
        self.play(waves[0].animate.set_stroke(width=7), run_time=.75)
        self.at("Two still minutes")
        sheet = place(clipboard(), .7, -2.68, .83).rotate(-.15)
        self.play(FadeOut(question), FadeIn(sheet, shift=UP * .22), run_time=.9)
        self.finish()


class S02Title(TitleCard):
    TITLE = "The Listening Walk: Parent Guide"
    LESSON = "The Listening Walk"

    def construct(self):
        self.add(yard(), arrivals(), yard_waves())
        title = fit_text(self.TITLE, size=44, min_size=38, max_w=9.0,
                         font=TITLE_FONT, color=PAPER).move_to(point(1.42, 2.68))
        self.play(FadeIn(title, shift=DOWN * .1), run_time=.47)
        self.wait(self.narration_s - self.elapsed())


class S03Payoff(SpokenScene):
    def construct(self):
        self.add(yard(), arrivals(), yard_waves())
        gear = VGroup(towel(), supplies())
        duration = VGroup(clock_face(), T("30 minutes", 34, PAPER)).arrange(RIGHT, buff=.2)
        duration.move_to(point(1.6, 2.68))
        self.at("In about 30 minutes")
        self.play(FadeIn(gear, shift=UP * .38), run_time=1.05)
        self.play(FadeIn(duration), run_time=.55)
        self.at("counts sounds")
        self.play(Indicate(gear[1][0], color=PAPER, scale_factor=1.13), run_time=1.5)
        self.at("test their own ears")
        self.play(FadeOut(duration), run_time=.5)
        label = prompt("Listen closely")
        self.at("listening closely")
        self.play(FadeIn(label), run_time=.45)
        for cue, words in [("sorting what", "Sort sounds"), ("checking a guess", "Guess, then check")]:
            self.at(cue)
            new = prompt(words)
            self.play(swap(label, new), run_time=.55)
            self.remove(label)
            self.add(new)
            label = new
        self.finish()


def warning_mark(drawing, center=None):
    disc = Circle(radius=.82, color=RED, stroke_width=7)
    slash = line(-.57, .57, .57, -.57, RED, 8)
    return VGroup(disc, slash).move_to(drawing.get_center() if center is None else center)


class S04Gather(SpokenScene):
    def construct(self):
        self.add(yard(sway=True), arrivals(), towel())
        mat_items = supplies()
        paper = place(clipboard(), -.25, -1.88, 1.35)
        markers = place(crayons(), 1.53, -2.28, 1.13)
        timer = place(phone(), 2.95, -1.84, .77)
        timer.add(place(clock_face(), 2.95, -1.84, .36))
        self.at("Gather paper")
        self.play(FadeIn(paper, shift=DOWN * .25), run_time=.65)
        self.at("crayons a clipboard")
        self.play(FadeIn(markers, shift=UP * .24), run_time=.75)
        self.at("timer and a mat")
        self.play(FadeIn(timer, shift=DOWN * .2), run_time=.75)
        self.at("Pick a spot")
        check = VGroup(line(-.26, .01, -.07, -.21, GREEN, 9),
                       line(-.07, -.21, .35, .29, GREEN, 9)).move_to(point(.13, -.83))
        pond = oval(2.12, .74, 4.92, -1.51, "#628E9D")
        road_x = warning_mark(pond, point(5.47, .40)).scale(.85)
        pond_x = warning_mark(pond).scale(.83)
        pin = Circle(radius=.38, stroke_width=0, fill_color="#284B39", fill_opacity=1)
        pin.move_to(check)
        self.play(GrowFromCenter(pin), FadeIn(pond), run_time=.58)
        self.play(Create(check), run_time=.55)
        self.at("away from roads")
        self.play(Create(road_x), run_time=.65)
        self.at("ponds and streams")
        self.play(Create(pond_x), run_time=.65)
        self.at("Stay close enough")
        self.play(FadeOut(VGroup(paper, markers, timer, pin, check, pond, road_x, pond_x)),
                  run_time=.4)
        self.play(FadeIn(mat_items), FadeIn(backyard_people(), shift=UP * .28), run_time=.6)
        self.finish()


class S05PredictListen(SpokenScene):
    def construct(self):
        people = backyard_people()
        self.add(yard(), arrivals(), towel(), supplies(), people)
        question = prompt("How many sounds?")
        self.at("Ask first")
        self.play(FadeIn(question), run_time=.5)
        self.at("write the number")
        pad = tally_sheet()
        self.play(FadeIn(pad, shift=LEFT * .4), FadeOut(question), run_time=.85)
        self.at("set the timer")
        progress = ValueTracker(.01)
        ring = timer_arc(progress)
        self.play(FadeIn(ring), run_time=.55)
        self.at("closes their eyes")
        profile = backyard_child(listening=True)
        self.play(Transform(people[1], profile), progress.animate.set_value(.16), run_time=.64)
        raised = raised_hand(1)
        self.at("holds up one finger")
        waves = yard_waves(False)
        self.add(waves[0])
        self.play(FadeIn(raised, shift=UP * .24), FadeIn(listening_arm(), shift=UP * .18),
                  progress.animate.set_value(.35), run_time=.55)
        for count, fraction in [(2, .53), (3, .87)]:
            self.add(waves[count - 1])
            self.play(Transform(raised, raised_hand(count)),
                      progress.animate.set_value(fraction), run_time=.55)
        self.finish()


class S06Check(SpokenScene):
    def construct(self):
        progress = ValueTracker(.87)
        sounds = yard_waves(False)
        people = backyard_people(listening=True)
        self.add(yard(), arrivals(), towel(), supplies(), people, sounds, listening_arm(),
                 raised_hand(3))
        ring = timer_arc(progress)
        guess = tally_sheet()
        self.add(ring, guess)
        self.at("When the timer ends")
        self.play(progress.animate.set_value(1), run_time=1.12)
        self.at("more or fewer")
        self.play(FadeOut(guess), run_time=.24)
        self.play(FadeIn(tally_sheet(True), shift=LEFT * .4),
                  FadeIn(prompt("More or fewer?")), run_time=.7)
        self.at("Expect anything")
        for mark in sounds:
            mark.suspend_updating()
            self.play(Indicate(mark, color=PAPER, scale_factor=1.45), run_time=.85)
        for mark in sounds:
            mark.resume_updating()
        self.at("depending on the place")
        self.play(FadeOut(ring), run_time=.65)
        self.finish()


def map_board():
    return VGroup(slab(11.88, 6.56, 0, -.05, WOOD, .24),
                  slab(11.50, 6.13, 0, -.16, PAPER, .12),
                  slab(1.77, .29, 0, 3.09, "#C4B496", .09))


MAP_POS = {"bird": (-1.77, .90), "car": (4.20, -.14), "dog": (4.17, 1.48),
           "insect": (-.94, -1.32), "leaves": (-4.07, .64)}


def map_marks(car_large=False, dog_small=False):
    return {
        "bird": place(bird(), *MAP_POS["bird"], 1.40),
        "car": place(car(), *MAP_POS["car"], 2.38 if car_large else 1.32),
        "dog": place(dog(), *MAP_POS["dog"], .75 if dog_small else 1.23),
        "insect": place(insect(), *MAP_POS["insect"], .97),
        "leaves": place(VGroup(shape([(-.19, -.52), (.15, -.52), (.07, .38), (-.10, .38)], WOOD),
                                oval(1.08, .67, -.30, .21, LEAF),
                                oval(1.0, .78, .23, .35, "#78A265"),
                                place(leaves(), .39, .14, .67)), *MAP_POS["leaves"], 1.55),
    }


def map_me():
    return VGroup(Dot(point(0, 0), radius=.12, color=INK),
                  fixed_text("me", 0, -.43, 33, INK))


def pitch_arrows():
    return VGroup(Arrow(point(-.82, .53), point(-.82, 1.32), buff=0, color=INK, stroke_width=5),
                  Arrow(point(4.2, -.84), point(4.2, -1.62), buff=0, color=INK, stroke_width=5))


def map_rings():
    locations = [("bird", .81), ("insect", .61), ("dog", .52)]
    return VGroup(*(Circle(radius=r, stroke_color="#A47610", stroke_width=5).move_to(point(*MAP_POS[key]))
                    for key, r in locations))


def tricky_ring():
    return DashedVMobject(Circle(radius=.94, stroke_color="#A47610", stroke_width=5),
                         num_dashes=19).move_to(point(*MAP_POS["leaves"]))


def drawing_crayon(tip_x, tip_y):
    crayon = VGroup(slab(1.87, .35, 1.14, 0, "#327785", .06),
                    shape([(0, 0), (.31, -.18), (.31, .18)], "#327785"),
                    slab(1.05, .36, 1.12, 0, "#25485A", .045))
    return crayon.rotate(.24, about_point=ORIGIN).shift(point(tip_x, tip_y))


def map_rule(words):
    return caption(words, size=39, color=INK, y=-2.66).set_x(0)


class S07Map(SpokenScene):
    def construct(self):
        self.add(yard())
        self.at("Now the sound map")
        self.play(FadeIn(map_board(), shift=UP * .52), run_time=1.2)
        me = map_me()
        self.at("Put a dot")
        stylus = drawing_crayon(0, 0)
        drawing_hand = VGroup(slab(1.20, .79, 2.23, .89, SHIRT).rotate(.26),
                              oval(1.72, 1.03, 1.53, .67, SKIN).rotate(.26),
                              oval(.69, .31, .82, .23, "#C88D65").rotate(.28))
        pencil_grip = VGroup(stylus, drawing_hand)
        self.play(FadeIn(pencil_grip, shift=RIGHT * 2.0), run_time=.70)
        self.play(GrowFromCenter(me[0]), pencil_grip.animate.shift(RIGHT * .53), run_time=.55)
        self.at("label it me")
        self.play(FadeIn(me[1]), FadeOut(pencil_grip, shift=RIGHT * 1.2), run_time=.65)
        marks = map_marks()
        self.at("draws each sound")
        stylus = drawing_crayon(-1.72, .56)
        self.play(FadeIn(stylus, shift=LEFT * 2.1), run_time=.63)
        self.play(DrawBorderThenFill(marks["bird"]), stylus.animate.shift(RIGHT * .88), run_time=.89)
        self.play(stylus.animate.shift(RIGHT * 4.28 + DOWN * .82), run_time=.92)
        self.play(DrawBorderThenFill(marks["car"]), FadeOut(stylus, shift=DOWN * .70), run_time=.71)
        self.at("Near sounds go")
        near = map_rule("Near: close to dot")
        guide = line(-.23, .12, -1.22, .62, "#AC7B33", 12)
        self.play(FadeIn(near), GrowFromPoint(guide, guide.get_start()), run_time=.92)
        self.at("far sounds near")
        long_guide = line(.25, .03, 3.43, -.12, "#AC7B33", 12)
        self.play(swap(near, map_rule("Far: near edge")), FadeOut(guide),
                  GrowFromPoint(long_guide, long_guide.get_start()), run_time=1.1)
        self.play(FadeOut(long_guide), run_time=.45)
        self.finish()


class S08MapRules(SpokenScene):
    def construct(self):
        marks = map_marks()
        updated = map_marks(True, True)
        self.add(yard(), map_board(), map_me(), marks["bird"], marks["car"])
        self.at("Add one rule")
        stylus = drawing_crayon(4.18, 1.13)
        self.play(FadeIn(stylus, shift=LEFT * 1.5), run_time=.78)
        self.play(DrawBorderThenFill(marks["dog"]), FadeOut(stylus, shift=DOWN * .45), run_time=.72)
        self.at("Loud sounds are drawn")
        self.play(Transform(marks["car"], updated["car"]), run_time=1)
        self.at("soft sounds small")
        self.play(Transform(marks["dog"], updated["dog"]), run_time=.75)
        loud = map_rule("Loud: big, soft: small")
        self.play(FadeIn(loud), run_time=.45)
        self.at("High and low")
        pitch = map_rule("Pitch")
        self.play(swap(loud, pitch), run_time=.65)
        self.at("called pitch")
        stylus = drawing_crayon(-.82, .53)
        self.play(FadeIn(stylus, shift=LEFT * 1.85), run_time=1.05)
        self.at("an arrow up")
        up, down = pitch_arrows()
        self.play(GrowArrow(up), stylus.animate.shift(UP * .79),
                  swap(pitch, map_rule("High: up, low: down")), run_time=.78)
        self.play(stylus.animate.shift(RIGHT * 5.02 + DOWN * 2.16), run_time=.76)
        self.at("down for a low")
        self.play(GrowArrow(down), stylus.animate.shift(DOWN * .78), run_time=.48)
        self.play(FadeOut(stylus, shift=RIGHT * .24), run_time=.33)
        self.finish()


class S09Living(SpokenScene):
    def construct(self):
        marks = map_marks(True, True)
        rings = map_rings()
        self.add(yard(), map_board(), map_me(), pitch_arrows(),
                 *(marks[key] for key in ["bird", "car", "dog"]))
        tip = point(-1.77, 1.71)
        stylus = drawing_crayon(*tip[:2]).rotate(PI, about_point=tip)
        self.at("circle the sounds")
        self.play(FadeIn(stylus, shift=LEFT * 1.2), run_time=.57)
        orbit = Arc(radius=.81, start_angle=PI / 2, angle=TAU,
                    arc_center=stylus.get_center() + DOWN * .81)
        self.play(Create(rings[0]), MoveAlongPath(stylus, orbit), run_time=1.14)
        self.at("birds insects")
        self.play(DrawBorderThenFill(marks["insect"]),
                  stylus.animate.shift(RIGHT * .76 + DOWN * 2.48), run_time=.67)
        orbit = Arc(radius=.53, start_angle=PI / 2, angle=TAU,
                    arc_center=stylus.get_center() + DOWN * .53)
        self.play(Create(rings[1]), MoveAlongPath(stylus, orbit), run_time=.70)
        self.at("dogs and people")
        self.play(FadeOut(stylus, shift=LEFT * .82), run_time=.30)
        stylus = drawing_crayon(4.17, 2.0)
        self.play(FadeIn(stylus, shift=DOWN * .55), run_time=.55)
        self.play(Create(rings[2]), FadeOut(stylus, shift=UP * .44), run_time=.78)
        self.at("Talk about the tricky")
        stylus = drawing_crayon(-4.07, 1.58)
        self.play(DrawBorderThenFill(marks["leaves"]), FadeIn(stylus, shift=UP * .75), run_time=.86)
        self.play(Create(tricky_ring()), Rotate(stylus, TAU, about_point=point(*MAP_POS["leaves"])),
                  run_time=1.13)
        self.play(FadeOut(stylus), run_time=.35)
        self.at("Rustling leaves come")
        mark = traveling_wave((-5.2, 1.37), (-3.10, 1.49), .2, .55, emphasis=1.3)
        self.add(mark)
        self.at("the wind makes")
        self.play(FadeIn(map_rule("Tricky: tree or wind?")),
                  FadeIn(fixed_text("?", -4.18, 2.62, 40, INK)), run_time=.6)
        self.finish()


def fan_table():
    return VGroup(slab(3.35, .22, 3.98, -.61, WOOD), slab(.18, 1.88, 2.62, -1.58, WOOD),
                  slab(.18, 1.88, 5.37, -1.58, WOOD))


def fan():
    center = point(4.14, 1.15)
    blades = VGroup(*(oval(.29, 1.01, 4.06, 1.67, "#669DB1").rotate(-.32, about_point=center)
                      .rotate(a, about_point=center) for a in np.linspace(0, TAU, 4, endpoint=False)))
    grille = VGroup(*(Circle(radius=r, color="#9DABAF", stroke_width=2.3).move_to(center)
                      for r in [.37, .60, .83, 1.07]),
                    *(Line(center, center + 1.07 * point(np.cos(a), np.sin(a)),
                           color="#9DABAF", stroke_width=2) for a in np.linspace(0, TAU, 16, endpoint=False)))
    return VGroup(slab(.26, .80, 4.14, -.16, GREY), slab(1.89, .19, 4.14, -.42, GREY),
                  oval(2.37, 2.37, *center[:2], INK), blades, grille,
                  oval(.28, .28, *center[:2], BLUE))


def spinning(f):
    f[3].add_updater(lambda blades, dt: blades.rotate(2.8 * dt, about_point=point(4.14, 1.15)))
    return f


def tucked_cord():
    cord = VMobject(color=INK, stroke_width=7)
    cord.set_points_smoothly([point(4.64, -.43), point(5.12, -.72), point(5.29, -1.11),
                              point(5.28, -1.62), point(5.37, -2.46)])
    return VGroup(cord, slab(.16, .07, 5.32, -1.07, GREY, .025),
                  slab(.16, .07, 5.34, -1.58, GREY, .025))


def fan_adult():
    return place(seat(SHIRT, 1), -3.26, -.91, 2.64)


def fan_child(direction=1, cupped=True):
    return place(seat(CHILD, direction, cupped), -.46, -.93, 2.20)


def fan_waves():
    return VGroup(*(traveling_wave((2.79, 1.13), (.74, .69), offset, .54)
                    for offset in [.03, .54]))


def fan_question():
    return question_card("Louder, fainter, or the same?", y=-3.06, size=43, color=PAPER).shift(RIGHT * .5)


def test_backdrop():
    return VGroup(yard(), fan_table(), tucked_cord(), spinning(fan()), fan_adult(), fan_child(), fan_waves())


class S10CupSetup(SpokenScene):
    def construct(self):
        self.add(yard(), fan_table())
        source = fan().shift(UP * .34)
        grownup = place(seat(SHIRT, 1), 1.23, -.91, 2.64)
        self.at("Choose a quiet")
        self.play(FadeIn(source, shift=DOWN * .18), FadeIn(grownup, shift=LEFT * .45), run_time=1.25)
        self.at("Use a guarded fan")
        self.play(source.animate.shift(DOWN * .34), run_time=1.05)
        spinning(source)
        self.at("its cord tucked")
        for item in tucked_cord():
            self.play(Create(item), run_time=.29)
        self.at("Sit your child")
        learner = fan_child(cupped=False)
        self.play(Transform(grownup, fan_adult()), run_time=.65)
        self.play(FadeIn(learner, shift=LEFT * .25), run_time=.65)
        self.at("arm's length back")
        span = DoubleArrow(point(.66, -2.70), point(3.62, -2.70), color=PAPER, buff=0, stroke_width=3)
        measure = fixed_text("At least an arm’s length", 2.15, -3.29, 31, PAPER)
        self.play(GrowFromCenter(span), run_time=.55)
        self.play(FadeIn(measure), run_time=.35)
        self.at("face the sound")
        self.play(FadeOut(VGroup(span, measure)), run_time=.5)
        self.add(fan_waves())
        self.at("cup their hands")
        self.play(Transform(learner, fan_child()), run_time=1.25)
        self.finish()


class S11PredictQ(SpokenScene):
    def construct(self):
        picture = test_backdrop()
        self.add(picture)
        self.at("A question for you")
        self.at("hands cupped")
        self.play(Indicate(picture[5][7], color=PAPER, scale_factor=1.12), run_time=1.45)
        self.at("Will the sound get")
        self.play(FadeIn(fan_question(), shift=UP * .15), run_time=.75)
        self.finish()


class S12Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(test_backdrop(), fan_question())
        self.wait(float(os.environ["KX_DURATION"]))


def ear_inset(facing):
    """Cup openings point with the profile, while the source stays on the right."""
    panel = slab(4.0, 1.85, -2.63, 2.30, "#283D48", .19)
    head = VGroup(oval(1.1, 1.36, 0, 0, SKIN),
                  shape([(.47, .19), (.71, -.03), (.46, -.18)], SKIN),
                  oval(.24, .45, -.10, .04, "#AD6C54"),
                  ArcBetweenPoints(point(-.08, .47), point(-.1, -.34), angle=1.45,
                                   color=PAPER, stroke_width=12))
    if facing == -1:
        head.flip(UP)
    head.move_to(point(-3.56, 2.26))
    if facing == 1:
        stream = VGroup(*(traveling_wave((-1.12, y), (-3.5, y), i * .31, .78)
                          for i, y in enumerate([1.90, 2.26, 2.62])))
    else:
        stream = VGroup(traveling_wave((-1.12, 2.26), (-3.5, 2.26), .31, .78,
                                       emphasis=.80, opacity=.55))
    for mark in stream:
        mark.scale(.50)
    return VGroup(panel, head, stream)


class S13Reveal(SpokenScene):
    def construct(self):
        picture = test_backdrop()
        learner = picture[5]
        self.add(picture)
        before = ear_inset(1)
        after = ear_inset(-1)
        self.at("Most children hear")
        self.play(FadeIn(before), run_time=.8)
        self.at("turn around with")
        self.play(Transform(learner, fan_child(-1)), run_time=1.15)
        self.play(FadeOut(before[1:]), run_time=.32)
        self.add(after[1:])
        self.at("usually sounds fainter")
        self.play(FadeIn(prompt("Usually fainter", y=-3.07)), run_time=.56)
        self.at("bigger funnels now")
        self.play(Indicate(after[1][-1], scale_factor=1.14, color=GOLD), run_time=1.45)
        self.finish()


def cat():
    fur = "#CF905F"
    tail = ArcBetweenPoints(point(-.63, -.54), point(-1.65, -.10),
                            angle=-1.9, color=fur, stroke_width=18)
    body = oval(2.04, 1.31, -.21, -.43, fur)
    head = oval(1.35, 1.10, .47, .39, fur)
    ears = VGroup(VGroup(shape([(-.13, .58), (-.08, 1.5), (.47, .82)], fur),
                         shape([(-.055, .79), (-.02, 1.28), (.27, .86)], WOOD)),
                  VGroup(shape([(.48, .87), (1.1, 1.48), (1.06, .58)], fur),
                         shape([(.74, .87), (1.01, 1.26), (1.01, .76)], WOOD)))
    face = VGroup(oval(.14, .13, .42, .5, INK), oval(.14, .13, .84, .5, INK),
                  oval(.15, .09, .66, .32, WOOD), oval(.57, .23, .68, -.9, fur))
    return VGroup(tail, body, ears, head, face)


def horse():
    return VGroup(oval(1.68, .84, -.33, -.18, WOOD), oval(.53, 1.01, .43, .29, WOOD).rotate(-.34),
                  oval(.82, .47, .79, .68, "#BE906F"), oval(.16, .43, .63, 1.01, WOOD).rotate(.22),
                  oval(.16, .39, .90, 1.01, WOOD).rotate(-.22),
                  *(line(x, -.33, x - .11, -.88, WOOD, 7) for x in [-.88, -.59, .14, .34]),
                  line(-.97, -.13, -1.28, -.59, INK, 7),
                  Dot(point(.96, .75), radius=.045, color=INK))


def horse_yard():
    inset = slab(4.25, 3.11, 4.20, .88, "#394F4D", .2)
    rail = VGroup(*(slab(3.85, .12, 4.21, y, "#AC805C", .04) for y in [.29, .01]),
                  *(slab(.13, .64, x, .15, "#AC805C", .04) for x in [2.38, 4.25, 6.09]))
    return VGroup(inset, place(horse(), 5.03, 1.09, 1.93), place(seat(SHIRT, 1), 3.37, .86, .73),
                  rail, place(seat(SHIRT), 3.07, -.25, .70),
                  place(seat(CHILD), 3.71, -.28, .53))


class S14Cats(SpokenScene):
    def construct(self):
        pet = place(cat(), -3.10, -.07, 3.48)
        cabinet = VGroup(slab(2.26, 2.72, .10, -.24, WOOD),
                         slab(1.92, 2.40, .10, -.24, INK),
                         slab(1.88, 2.32, .10, -.24, "#AC805C"),
                         oval(.11, .17, .89, -.24, PAPER))
        watchers = place(backyard_people(), -4.51, -2.18, 2.53)
        self.add(yard(), cabinet, pet)
        self.at("Cats and horses")
        self.play(FadeIn(horse_yard(), shift=LEFT * .26), run_time=.88)
        self.at("turn toward a sound")
        self.play(VGroup(*cabinet[2:]).animate.stretch(.33, 0, about_point=cabinet[1].get_left()),
                  run_time=.8)
        self.add(traveling_wave((-.58, 1.29), (-1.83, 1.10), .08, .51))
        turns = []
        for cat_ear in pet[2]:
            base_left, _, base_right = cat_ear[0].get_vertices()
            turns.append(Rotate(cat_ear, -.29, about_point=(base_left + base_right) / 2))
        self.play(*turns, run_time=1.2)
        self.at("what do you think")
        self.play(FadeIn(question_card("What do big ears help it do?", y=2.93, size=45, color=PAPER).shift(RIGHT * 1.54)), run_time=.7)
        self.at("a pet your child knows")
        self.play(FadeIn(watchers, shift=RIGHT * .40), run_time=1)
        self.finish()


def ear():
    return VGroup(oval(1.03, 1.66, 0, 0, SKIN).rotate(-.22),
                  ArcBetweenPoints(point(-.16, .38), point(.14, -.12), angle=-2.8,
                                   color="#A25D46", stroke_width=8),
                  oval(.23, .33, -.12, -.22, "#A25D46"))


def mower():
    return VGroup(slab(1.47, .3, 0, -.31, CHILD), slab(.60, .4, -.1, -.06, INK),
                  oval(.32, .32, -.46, -.46, INK), oval(.32, .32, .48, -.46, INK),
                  line(.48, -.19, 1.12, .69, INK, 8), line(1.08, .68, 1.38, .68, INK, 8))


def safety_caption(words):
    return fixed_text(words, .55, 2.72, 43, PAPER)


class S15Safety(SpokenScene):
    def construct(self):
        self.add(yard(sway=True), arrivals())
        adults = VGroup(place(seat(SHIRT), -1.56, -.71, 2.85),
                        place(seat(CHILD, -1), .94, -.71, 2.35))
        self.at("Stay close enough")
        self.play(FadeIn(adults, shift=UP * .23), run_time=.85)
        words = safety_caption("Close enough to touch")
        self.play(FadeIn(words), run_time=.56)
        self.at("Cup hands only")
        child_cupping = place(seat(CHILD, -1, True), .94, -.71, 2.35)
        quiet = safety_caption("Quiet sounds only")
        self.play(Transform(adults[1], child_cupping), swap(words, quiet), run_time=1.0)
        bird_wave = traveling_wave((-2.63, 1.18), (.24, .16), .02, .48, emphasis=1.48)
        self.add(bird_wave)
        self.at("never toward a road")
        self.remove(bird_wave)
        road_cross = warning_mark(adults, point(4.83, .31))
        road_caption = safety_caption("Never toward a road")
        self.play(Create(road_cross), swap(quiet, road_caption), run_time=.8)
        self.at("something loud starts")
        noisy = place(mower(), 4.55, -1.3, 2.65)
        move = safety_caption("Loud? Move away")
        self.play(FadeOut(road_cross), FadeIn(noisy, shift=LEFT * .24),
                  swap(road_caption, move), run_time=.55)
        self.at("move away")
        arrow = Arrow(point(3.34, -2.8), point(-1.82, -2.8), color=PAPER, stroke_width=6, buff=0)
        self.play(adults.animate.scale(.86).shift(LEFT * .70 + DOWN * .25),
                  GrowArrow(arrow), run_time=.85)
        self.at("Nothing goes into", lead=.45)
        self.play(FadeOut(VGroup(adults, noisy, arrow, move)), run_time=.25)
        closeup = place(ear(), .2, -.36, 1.8)
        swab = VGroup(line(1.2, -.37, 2.49, .04, PAPER, 7),
                      oval(.51, .18, 1.14, -.39, TEXT).rotate(.32))
        self.play(FadeIn(closeup), FadeIn(swab), FadeIn(safety_caption("Nothing in ears")),
                  Create(warning_mark(swab, point(1.94, -.17))), run_time=.35)
        self.finish()


def pebble_and_acorn():
    pebble = shape([(-1.85, -.78), (-1.97, -.31), (-1.52, .35), (-.87, .53), (-.37, .11),
                    (-.28, -.51), (-.72, -.86), (-1.49, -.92)], GREY)
    acorn = VGroup(oval(1.11, 1.50, .76, -.39, "#C28355"),
                   oval(1.31, .63, .76, .15, WOOD), line(.77, .33, .88, .64, WOOD, 8)).rotate(-.28)
    drawing = VGroup(pebble, acorn)
    return VGroup(drawing, warning_mark(drawing).scale(2.35))


def berry_and_mouth():
    face = VGroup(oval(2.49, 2.8, 1.85, .01, SKIN),
                  shape([(.77, .46), (.29, -.01), (.82, -.15)], SKIN),
                  oval(.46, .15, .91, -.47, INK), oval(.19, .13, .99, .36, INK))
    wrist = VGroup(oval(2.55, .73, -1.23, -.70, SKIN).rotate(.19),
                   oval(.69, .48, -.24, -.45, SKIN))
    berry = VGroup(oval(.30, .30, .05, -.31, RED), oval(.29, .29, .21, -.18, RED),
                   oval(.26, .18, .24, .01, LEAF).rotate(.53))
    return VGroup(face, wrist, berry)


def wash_hands():
    basin = VGroup(slab(4.15, .27, 0, -1.49, "#C3D8D8"),
                   slab(.23, 1.24, -1.68, .54, GREY), slab(1.48, .23, -1.02, 1.06, GREY),
                   slab(.23, .38, -.37, .95, GREY))
    palms = VGroup(oval(2.35, .65, -.40, -.81, SKIN).rotate(.20),
                   oval(2.17, .58, .45, -.52, "#E2B58D").rotate(-.25))
    bubbles = VGroup(*(Circle(radius=r, stroke_color=PAPER, stroke_width=3).move_to(point(x, y))
                       for r, x, y in [(.13, -.46, -.48), (.17, -.17, -.64), (.11, .21, -.38), (.14, -.81, -.68)]))
    water = VGroup(*(slab(.07, .21, x, y, BLUE, .035) for x, y in
                     [(-.38, .54), (-.42, .18), (-.34, -.17), (-.53, .38)]))
    for i, drop in enumerate(water):
        bob(drop, amp=.15, speed=5.2, seed=i)
    return VGroup(basin, palms, bubbles, water)


def tick_check():
    pants = VGroup(slab(1.64, 2.50, 1.16, .13, SHIRT),
                   slab(.12, 2.22, .56, .11, "#326877"), slab(1.58, .18, 1.18, -.96, "#326877"),
                   oval(2.08, .55, .99, -1.21, INK))
    tick = VGroup(oval(.20, .29, .98, -.21, INK),
                  *(line(.98, y, x, y + .13, INK, 2.5) for y in [-.31, -.24, -.17, -.10] for x in [.79, 1.17]))
    finger = VGroup(oval(1.55, .58, -1.06, -.42, SKIN).rotate(.22),
                    oval(.93, .24, -.37, -.20, SKIN).rotate(.11))
    return VGroup(pants, tick, finger)


class S16Safety2(SpokenScene):
    def construct(self):
        self.add(yard())
        objects = pebble_and_acorn().move_to(point(.2, -.43))
        self.at("Nothing from the ground")
        self.play(FadeIn(objects[0], shift=UP * .34), run_time=.85)
        self.play(Create(objects[1]), run_time=.65)
        self.at("can choke children")
        label = safety_caption("Under 4: choking risk")
        self.play(FadeIn(label), Indicate(objects[0], scale_factor=1.07), run_time=.75)
        self.at("Call 911")
        self.play(FadeOut(VGroup(objects, label)), run_time=.4)
        call = VGroup(place(phone(), .2, -.39, 2.08), fixed_text("911", .2, -.24, 45))
        emergency = safety_caption("Choking: call 911")
        self.play(FadeIn(call, shift=UP * .3), FadeIn(emergency), run_time=.7)
        self.at("Never taste wild plants")
        self.play(FadeOut(VGroup(call, emergency)), run_time=.4)
        berry = berry_and_mouth()
        berry_x = warning_mark(berry, point(.2, -.24)).scale(1.30)
        self.play(FadeIn(berry, shift=LEFT * .25), run_time=.72)
        self.play(Create(berry_x), run_time=.72)
        self.at("Wash hands after")
        self.play(FadeOut(VGroup(berry, berry_x)), run_time=.33)
        sink = wash_hands()
        self.play(FadeIn(sink, shift=UP * .33), run_time=.72)
        self.at("Check for ticks")
        self.play(FadeOut(sink), run_time=.36)
        check = tick_check()
        self.play(FadeIn(check, shift=RIGHT * .30), run_time=.6)
        self.play(check[2].animate.shift(RIGHT * .58), run_time=.60)
        self.finish()


def finished_map():
    marks = map_marks(True, True)
    return VGroup(map_board(), Dot(radius=.12, color=INK), *marks.values(), pitch_arrows(),
                  map_rings(), tricky_ring())


class S17Return(SpokenScene):
    def construct(self):
        self.add(yard(), arrivals(), towel())
        board = place(finished_map(), .55, -2.33, 2.61).rotate(-.13)
        self.add(board)
        self.at("Ask what your child")
        pair = place(VGroup(seat(SHIRT, 1), seat(CHILD, -1, True).shift(RIGHT * 1.27)),
                     .1, -.82, 2.78)
        self.play(FadeIn(pair), run_time=.8)
        self.at("Look back at the map")
        self.play(FadeOut(pair), run_time=.62)
        self.at("trace where the sounds")
        self.add(yard_waves(False))
        self.play(Indicate(board, scale_factor=1.12), run_time=.92)
        self.finish()


class S18End(EndCard):
    LINE = "Our ears are funnels that catch sound."
