"""Thirsty Celery, a schematic kitchen demonstration."""
from bp_parts import *

# COLOR MAP: BLUE water and tubes, GREEN celery, RED safety and alternate dye,
# GOLD questions and timing, GREY glass and tools. Kitchen surfaces are warm slate.
PALE = "#C9DB98"
RIB = "#658B51"
DYE = "#1754A1"
GLASS = "#9EBBC5"
SLATE = "#334752"
WOOD = "#55474A"
LINEN = "#B1C2BD"
SKIN = "#D7A583"
HERO = 3.05
OTHER = -0.35
BASE = -2.55
SURFACE = -1.78
CUT_Y = -.35
BARE_DYE_FRACTION = .37
QUESTION = "What will the cut end\nlook like?"
QUESTION_STYLE = dict(y=2.06, left=-6.03, size=41, max_w=5.15)


def p(x, y):
    return np.array([x, y, 0.0])


def solid(points, fill, outline=None, width=2):
    return Polygon(*(p(*xy) for xy in points), fill_color=fill, fill_opacity=1,
                   stroke_color=outline or fill, stroke_width=width)


def path(points, color, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly([p(*xy) for xy in points])


def box(w, h, x, y, color, radius=0.15, edge=None):
    return RoundedRectangle(width=w, height=h, corner_radius=radius, fill_color=color,
                            fill_opacity=1, stroke_color=edge or color,
                            stroke_width=2 if edge else 0).move_to(p(x, y))


def kitchen(tray=True):
    counter_top = Polygon(p(-6.72, -1.82), p(6.72, -1.82), p(6.72, -3.72), p(-6.72, -3.72),
                          stroke_width=0, fill_color=WOOD, fill_opacity=1)
    stage = VGroup(counter_top, box(13.44, 0.19, 0, -3.59, "#43393E", 0.08))
    if tray:
        stage.add(box(10.9, 0.84, 0.55, -2.79, SLATE, edge=GLASS),
                  box(10.55, 0.46, 0.55, -2.82, "#435C65"))
    return stage


def leaf(angle=0, size=1):
    blade = VMobject(fill_color=GREEN, fill_opacity=1, stroke_color=PALE, stroke_width=2)
    blade.set_points_smoothly([p(0, 0), p(.26, .37), p(.66, .54), p(1.05, .44), p(1.4, .22),
                               p(1.62, .11), p(1.22, -.16), p(.82, -.29), p(.39, -.24), p(0, 0)])
    veins = VGroup(path([(0, 0), (.75, .09), (1.43, .13)], RIB, 3),
                   path([(.55, .07), (.76, .36)], RIB, 2),
                   path([(.83, .095), (1.07, -.12)], RIB, 2))
    return VGroup(blade, veins).scale(size, about_point=ORIGIN).rotate(angle, about_point=ORIGIN)


def celery(x, base=BASE, leafy=True, stature=1):
    """Ribs, crown and the geometry reused for the dye overlays."""
    top = 4.3 if leafy else 3.62
    stem = solid([(-.48, 0), (.49, 0), (.49, 1.35), (.42, 2.68), (.32, top),
                  (-.25, top + .06), (-.32, 2.89), (-.44, 1.38)], PALE, GREEN, 3)
    ribs = VGroup(*[path([(d, .04), (d * .87, 1.34), (d * .79, 2.59), (d * .62, top - .08)], RIB, 3)
                    for d in (-.30, -.11, .10, .31)])
    cut = Ellipse(width=.96 if leafy else .57, height=.16, color=GREEN, stroke_width=2,
                  fill_color="#DFE7AF", fill_opacity=1)
    cut.move_to(p(0, .03 if leafy else top))
    crown = VGroup()
    if leafy:
        specs = [(3.02, 2.77, 1.05), (3.31, .28, 1.19), (3.83, 2.22, 1.05),
                 (4.06, .90, .99), (4.27, 1.53, .77)]
        crown.add(*[leaf(a, s).shift(p(0, h)) for h, a, s in specs])
    plant = VGroup(stem, cut, ribs, crown)
    plant.scale(stature, about_point=ORIGIN).shift(p(x, base))
    plant.ribs, plant.crown = ribs, crown
    return plant


def glass(x, level=SURFACE, color=DYE, strength=1, ripple=True, base=-2.67):
    """A sturdy clear cup with a broad, slowly moving reflection on the dyed surface."""
    top = base + 1.94
    def half_width(y):
        return .73 + .24 * (y - base) / (top - base)

    water = VGroup()
    waves = VGroup()
    if level > base:
        w = half_width(level) - .055
        water.add(solid([(x-.67, base+.05), (x+.67, base+.05), (x+w, level), (x-w, level)], color))
        water.set_opacity(strength)
        waves.add(Ellipse(width=2*w, height=.21, color=BLUE, stroke_width=1.8,
                          fill_color=BLUE, fill_opacity=.44 * strength).move_to(p(x, level)))
        for i in range(3):
            gleam = Ellipse(width=1.07 - .12*i, height=.12, stroke_width=0, fill_color=BLUE,
                            fill_opacity=.70 * strength).move_to(p(x, level-.16-.20*i))
            if ripple:
                anchor = gleam.get_center().copy()
                gleam.phase = i * TAU / 3

                def reflect(mob, dt, anchor=anchor):
                    mob.phase += 2.45 * dt
                    mob.move_to(anchor + p(.19*np.sin(mob.phase), .072*np.cos(mob.phase)))
                gleam.add_updater(reflect)
            waves.add(gleam)
    outline = VGroup(
        path([(x-.97, top), (x-.88, top-.73), (x-.72, base+.05),
              (x, base-.05), (x+.72, base+.05), (x+.88, top-.73), (x+.97, top)], GLASS, 3),
        Ellipse(width=1.94, height=.25, color=GLASS, stroke_width=2.5).move_to(p(x, top)),
        Line(p(x-.80, top-.24), p(x-.72, top-.88), color=TEXT, stroke_width=2),
    )
    return VGroup(water, waves, outline)


def rig(pair=False, ripple=True, color=DYE):
    plants = [celery(HERO)] + ([celery(OTHER, leafy=False)] if pair else [])
    cups = [glass(HERO, ripple=ripple, color=color)] + ([glass(OTHER, ripple=ripple, color=color)] if pair else [])
    return VGroup(kitchen(), *plants, *cups)


def heading(text, x=-3.42, y=2.05, color=TEXT, size=40, width=5.6):
    return fit_text(text, max_w=width, size=size, min_size=28, color=color, max_lines=3).move_to(p(x, y))


def note(text, x=-3.42, y=1.75, color=GOLD, size=31):
    return boxed_label(text, color=color, size=size, pad=.19, fill_opacity=.12).move_to(p(x, y))


def bottle(x, y, color):
    body = box(.83, 1.23, x, y, color, edge=TEXT)
    shoulder = box(.57, .35, x, y+.55, color)
    cap = box(.38, .36, x, y+.85, GLASS, .09)
    mark = drop(x, y, .22, TEXT)
    return VGroup(shoulder, body, cap, mark)


def drop(x, y, size, color=BLUE):
    shape = solid([(0, .32), (.19, 0), (.14, -.16), (0, -.22), (-.14, -.16), (-.19, 0)], color)
    return shape.set_height(size).move_to(p(x, y))


def prohibition(mob, radius=.56):
    center = mob.get_center()
    circle = Circle(radius=radius, color=RED, stroke_width=6).move_to(center)
    slash = Line(center + radius*.71*UL, center + radius*.71*DR, color=RED, stroke_width=6)
    return VGroup(mob, circle, slash)


def clock(x, y, radius=.67, hour=0):
    face = Circle(radius=radius, color=GOLD, stroke_width=3, fill_color="#2E3540", fill_opacity=1)
    marks = VGroup(*[Line(UP*radius*.80, UP*radius*.91, color=GOLD, stroke_width=2).rotate(
        k*TAU/12, about_point=ORIGIN) for k in range(12)])
    hand = Line(ORIGIN, UP*radius*.55, color=TEXT, stroke_width=6).rotate(-hour*TAU/12, about_point=ORIGIN)
    minute = Line(ORIGIN, UP*radius*.73, color=GOLD, stroke_width=4)
    minute.add_updater(lambda m, dt: m.rotate(-1.5*dt, about_point=m.get_start()))
    dial_face = VGroup(face, marks, hand, minute, Dot(radius=.055, color=TEXT)).shift(p(x, y))
    dial_face.hand = hand
    return dial_face


def person(x, y, scale=1, child=False):
    body = box(.78, 1.04, 0, -.67, TEAL if child else SLATE, .26, GLASS)
    head = Circle(radius=.29, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to(p(0, .24))
    eye = Dot(p(.09, .27), radius=.028, color=BG)
    return VGroup(body, head, eye).scale(scale, about_point=ORIGIN).shift(p(x, y))


def hand(x, y, angle=0):
    palm = box(.92, .47, 0, 0, SKIN, .18)
    thumb = box(.42, .20, .24, .23, SKIN, .095).rotate(.44)
    cuff = box(.29, .50, -.42, 0, TEAL, .09)
    return VGroup(palm, thumb, cuff).rotate(angle, about_point=ORIGIN).shift(p(x, y))


def knife(x, y, angle=0):
    blade = solid([(0, -.14), (1.03, -.14), (1.4, .16), (0, .16)], GLASS, TEXT)
    grip = box(.66, .26, -.34, 0, SLATE, .10, GLASS)
    return VGroup(blade, grip, hand(-.43, .07)).rotate(angle, about_point=ORIGIN).shift(p(x, y))


def section(filled=False):
    cut = VMobject(stroke_color=PALE, stroke_width=4,
                   fill_color=PALE if filled else "#343139", fill_opacity=1)
    cut.set_points_smoothly([p(-1.38, .49), p(-.92, .95), p(0, 1.03), p(.92, .95), p(1.38, .49),
                              p(1.27, -.48), p(.7, -1.0), p(0, -1.14), p(-.7, -1), p(-1.27, -.48),
                              p(-1.38, .49)])
    return cut.shift(p(-3.55, -.40))


def section_dots():
    # Schematic positions along the outer arc of the cut stalk.
    return VGroup(*[Dot(p(-3.55 + 1.15*np.sin(a), -.19 - 1.10*np.cos(a)), radius=.095, color=DYE)
                    for a in np.linspace(-1.14, 1.14, 9)])


def rib_dye(plant, fraction=1, width=5):
    return VGroup(*[VMobject(stroke_color=DYE, stroke_width=width).pointwise_become_partial(r, 0, fraction)
                    for r in plant.ribs])


def leaf_dye(plant, edges=False):
    if edges:
        return VGroup(*[VMobject(stroke_color=BLUE, stroke_width=4).pointwise_become_partial(blade, .25, .82)
                        for blade, veins in plant.crown])
    return VGroup(*[vein.copy().set_stroke(DYE, width=4) for blade, veins in plant.crown for vein in veins])


def vapor(scene, x=HERO):
    motes = VGroup(*[Dot(radius=.061 + .009*(i % 3), color=BLUE) for i in range(11)])
    def rise(group, dt):
        group.age += dt
        for i, mote in enumerate(group):
            f = (group.age / 2.7 + i*.173) % 1
            mote.move_to(p(x+(i%5-2)*.40 + f*(.20 if i%2 else -.22),
                           2.37 + f*.94 + .055*(i%3))).set_opacity(.85*np.sin(PI*f))
    motes.age = 0
    rise(motes, 0)
    motes.add_updater(rise)
    scene.add(motes)
    return motes


class S01Hook(SpokenScene):
    def construct(self):
        world = rig()
        self.add(world)
        self.at("how does water")
        q = heading("How does water get\nto the top?", y=1.55, color=GOLD, size=52)
        self.play(FadeIn(q, shift=UP*.12), run_time=.65)
        self.at("a celery stalk")
        self.play(Indicate(world[1], color=PALE, scale_factor=1.09), run_time=1.10)
        self.at("blue water make")
        shimmer = Arc(angle=PI, radius=.58, stroke_width=5, color=BLUE).move_to(p(HERO, SURFACE+.08))
        self.play(Create(shimmer), run_time=.75)
        self.play(FadeOut(shimmer), run_time=.5)
        self.at("compare a stalk")
        other = celery(OTHER, leafy=False)
        self.play(FadeIn(other, shift=UP*.42), FadeIn(glass(OTHER)), q.animate.shift(LEFT*.38), run_time=1.65)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Thirsty Celery"
    TITLE = "Thirsty Celery: Parent Guide"

    def construct(self):
        self.add(rig())
        title = heading(self.TITLE.replace(": ", ":\n"), y=.96, size=52, width=6.05)
        title.set_color(TEXT)
        rule = Line(LEFT*1.45, RIGHT*1.45, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=.36)
        self.play(FadeIn(title, shift=UP*.15), GrowFromCenter(rule), run_time=.55)
        self.wait(self.narration_s - self.elapsed())


class S03Payoff(SpokenScene):
    def construct(self):
        world = rig()
        self.add(world)
        time = clock(-3.42, .23, radius=.88)
        times = heading("About 20 min setup\nChecks over a day", y=2.10, size=34)
        self.at("setting up takes")
        self.play(FadeIn(time), FadeIn(times), run_time=.58)
        self.play(Rotate(time.hand, -TAU*.85, about_point=p(-3.42, .23)), run_time=3.7)
        self.at("makes a guess")
        pencil = VGroup(box(.25, 1.35, 0, 0, GOLD, .08),
                        solid([(-.125, -.65), (.125, -.65), (0, -.94)], SKIN)).rotate(-.65).move_to(p(-3.42, .17))
        guess = heading("Guess, then check", y=2.10, size=37)
        self.play(FadeOut(time), FadeIn(pencil, shift=UP*.18), swap(times, guess), run_time=.7)
        self.play(pencil.animate.shift(RIGHT*.47 + DOWN*.35), run_time=1.4)
        self.at("looking closely")
        lens = VGroup(Circle(radius=.59, color=GLASS, stroke_width=7), Line(p(.43,-.43), p(.97,-.97),
                         stroke_width=11, color=GLASS)).move_to(p(-3.42, .2))
        close = heading("Look closely", y=2.10, size=37)
        self.play(FadeOut(pencil), FadeIn(lens), swap(guess, close), run_time=.50)
        self.play(lens.animate.shift(RIGHT*.46), run_time=.45)
        self.at("something slow")
        later = heading("Wait for it", y=2.10, size=37)
        time = clock(-3.42, .23, radius=.88)
        self.play(swap(close, later), FadeOut(lens), FadeIn(time), run_time=.65)
        self.play(Rotate(time.hand, -TAU*.55, about_point=p(-3.42, .23)), run_time=1.35)
        self.at("see a path")
        hidden = heading("See the hidden path", y=2.10, size=37)
        trace = VGroup(*[
            VMobject(stroke_color=DYE, stroke_width=6).pointwise_become_partial(rib, .21, 1)
            for rib in world[1].ribs
        ])
        self.play(swap(later, hidden, run_time=.50), FadeOut(time, run_time=.45),
                  Create(trace, run_time=1.55))
        self.finish()


class S03bAllergies(SpokenScene):
    def construct(self):
        stalk = celery(HERO)
        cup = glass(HERO, level=-2.11, color=GLASS, strength=.68).set_z_index(1)
        self.add(kitchen(), stalk, cup)
        self.at("if anyone is allergic")
        alert = note("Celery allergy", y=2.05, color=RED)
        self.play(FadeIn(alert), run_time=.55)
        self.at("leave it out")
        self.play(FadeOut(stalk, shift=RIGHT*.7), run_time=1.15)
        cabbage = leaf(1.32, 2.35).shift(p(HERO-.20, -2.50))
        cabbage[0].set_fill("#D7E1A9")
        napa = heading("Napa cabbage", y=2.05)
        self.at("use the guide's")
        self.play(FadeIn(cabbage, shift=UP*.28), swap(alert, napa), run_time=1.13)
        bob(cabbage, amp=.08, speed=1.8)
        self.at("keep all experiment")
        no_taste = note("No tasting", y=2.05, color=RED)
        mouth = prohibition(Arc(angle=PI, start_angle=PI, radius=.27, stroke_width=6, color=TEXT).move_to(p(-3.42,.24)))
        self.play(swap(napa, no_taste), FadeIn(mouth), run_time=.75)
        self.at("the setup that follows")
        self.play(FadeOut(no_taste), FadeOut(mouth), FadeOut(cabbage), FadeIn(stalk), run_time=1.02)
        self.at("choose food coloring")
        dye = VGroup(bottle(-4.42, .04, DYE), bottle(-2.58, .04, RED))
        safe = heading("Use a suitable color", y=2.05, size=36)
        self.play(FadeIn(dye, shift=UP*.4), FadeIn(safe), run_time=1.0)
        bob(dye, amp=.078)
        self.at("skip the activity")
        self.play(swap(safe, note("No suitable color? Skip", y=2.05, color=RED)), FadeOut(dye), run_time=.8)
        self.finish()


class S04Gather(SpokenScene):
    def construct(self):
        self.add(kitchen())
        stalks = VGroup(*[celery(x, base=-.7, stature=.59) for x in (-5.42, -3.62, -1.82)])
        cups = VGroup(*[glass(x, level=-3, base=-2.59).scale(.76, about_point=p(x,-2.59))
                        for x in (-.60, 1.13, 2.85)])
        self.at("you need three")
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN*.42) for s in stalks], lag_ratio=.46), run_time=2.15)
        self.at("three sturdy clear")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*.43) for c in cups], lag_ratio=.33), run_time=1.35)
        self.at("blue or red")
        colors = VGroup(bottle(.90, .86, DYE), bottle(2.05, .86, RED))
        self.play(FadeIn(colors, shift=DOWN*.44), run_time=1.15)
        self.at("yellow is hard")
        omit = prohibition(bottle(3.26, .86, YELLOW), .61)
        self.play(FadeIn(omit, shift=DOWN*.25), run_time=.65)
        self.at("add water")
        jug_body = box(1.25, 1.74, 4.95, -1.36, SLATE, edge=GLASS)
        jug = VGroup(Arc(radius=.48, angle=PI, start_angle=-PI/2, color=GLASS, stroke_width=5).move_to(p(5.75,-1.28)),
                     jug_body, box(1.04,.91,4.95,-1.65,GLASS), path([(4.33,-.71),(4.14,-.51),(4.55,-.48)],GLASS))
        self.play(FadeOut(omit), FadeIn(jug, shift=LEFT*.48), run_time=.78)
        self.at("paper towels")
        towels = VGroup(box(3.12,.52,-3.85,-1.95,LINEN), box(2.82,.36,-3.78,-1.80,TEXT))
        self.play(FadeIn(towels, shift=RIGHT*.34), run_time=.55)
        self.at("old clothes")
        shirt = solid([(-.64,.47),(-.34,.66),(-.18,.49),(.18,.49),(.34,.66),(.64,.47),
                       (.47,.14),(.31,.22),(.31,-.61),(-.31,-.61),(-.31,.22),(-.47,.14)], TEAL, GLASS)
        self.play(FadeIn(shirt.move_to(p(4.92,1.02)), shift=DOWN*.24), run_time=.6)
        self.at("coloring stains")
        self.play(FadeIn(caption("Coloring stains: use a tray", y=-3.49, size=29, color=GOLD)), run_time=.55)
        self.finish()


class S05Mix(SpokenScene):
    def construct(self):
        self.add(kitchen())
        xs = (-.35, 2.38, 5.11)
        level = ValueTracker(-2.65)
        counts = [ValueTracker(0) for _ in xs]
        cups = [always_redraw(lambda x=x, n=n: glass(x, level.get_value(),
                interpolate_color(ManimColor("#648795"), ManimColor(DYE), n.get_value()/15), ripple=False))
                for x, n in zip(xs, counts)]
        self.add(*cups)
        self.at("fill each glass")
        self.play(level.animate.set_value(SURFACE), run_time=2.1, rate_func=linear)
        line = DashedLine(p(-1.53, SURFACE), p(.78, SURFACE), color=GOLD, stroke_width=3)
        mark = place_label(T("5 cm", 32, GOLD), line, dirs=(LEFT,), buff=.35)
        self.play(Create(line), FadeIn(mark), run_time=.60)
        self.at("stir in")
        qty = heading("15 to 20 drops\nper glass", x=-3.8, y=.88, size=41)
        bot = bottle(-.35, .85, DYE).rotate(PI)
        self.play(FadeOut(line), FadeOut(mark), FadeIn(qty), FadeIn(bot, shift=DOWN*.23), run_time=.6)
        live = counter("{:.0f} added", counts[0], p(-3.8,-.53), size=31, color=GOLD)
        falling = VGroup(*[drop(-.35, .03, .19) for _ in range(15)])
        def falling_drops(group):
            for i, bead in enumerate(group):
                f = counts[0].get_value() - i
                bead.set_opacity(1 if 0 < f < 1.5 else 0)
                bead.set_y(.03 - min(1.5, max(0, f))*1.12)
        falling.add_updater(falling_drops)
        falling_drops(falling)
        self.add(live, falling)
        self.play(counts[0].animate.set_value(15), run_time=3.0, rate_func=linear)
        self.remove(falling)
        self.at("dark color")
        self.play(bot.animate.shift(RIGHT*2.73), counts[1].animate.set_value(15), run_time=.90)
        self.play(bot.animate.shift(RIGHT*2.73), counts[2].animate.set_value(15), run_time=.95)
        self.play(FadeOut(bot), FadeOut(live), run_time=.45)
        self.finish()


class S06Cut(SpokenScene):
    def construct(self):
        stage = kitchen(False)
        board = box(7.7, 3.58, .45, -1.18, "#756257", .28, "#B99879")
        stalk = celery(0, base=0, stature=.88).rotate(-PI/2, about_point=ORIGIN).shift(p(-2.58,-1.24))
        adult = knife(-2.55, -.55, -.8)
        child = person(4.86, .31, 1.35, child=True)
        self.add(stage, board, stalk, adult, child)
        self.at("you do all")
        label = heading("Adult does the cutting", x=-2.79, y=2.14, size=39)
        self.play(FadeIn(label), adult.animate.shift(DOWN*.18), run_time=.75)
        self.at("keep celery pieces")
        cap = box(.45,.40,1.6,.85,GLASS,.09)
        piece = box(.48,.53,2.25,.85,PALE,.10,GREEN)
        small = VGroup(cap,piece)
        away = heading("Keep small pieces and caps\naway from children under 4", x=-2.79, y=2.13, size=34)
        self.play(swap(label, away), FadeIn(small), run_time=.7)
        self.play(small.animate.shift(LEFT*1.19), run_time=2.6)
        self.at("call 911")
        call = note("Choking? Call 911", x=-2.79, y=2.13, color=RED, size=33)
        self.play(swap(away, call), FadeOut(small), run_time=.73)
        self.at("trim about two")
        trim = note("2 cm, fresh cut", x=-2.79, y=2.13)
        self.play(swap(call, trim), adult.animate.shift(DOWN*.50 + RIGHT*.18), run_time=1.05)
        sliver = box(.32,.78,-2.60,-1.23,PALE,.10,GREEN)
        self.play(FadeIn(sliver), adult.animate.shift(UP*.46), run_time=.55)
        self.play(sliver.animate.shift(LEFT*.66), run_time=.9)
        self.at("cut all the leaves")
        bare = celery(0, base=0, leafy=False, stature=.88).rotate(-PI/2, about_point=ORIGIN).shift(p(-2.58,-1.24))
        self.play(adult.animate.move_to(p(.35,-.61)), run_time=.45)
        self.play(adult.animate.shift(DOWN*.48), FadeOut(stalk.crown, shift=RIGHT*.42), run_time=.55)
        self.remove(stalk, *stalk)
        self.add(bare)
        self.play(swap(trim, note("No leaves", x=-2.79, y=2.13)), FadeOut(adult), run_time=.65)
        self.finish()


def prediction_stalks(lift=0):
    return celery(HERO, BASE+lift), celery(OTHER, BASE+lift, leafy=False)


def writing_pad():
    sheet = box(2.0, 1.38, -4.08, -1.36, LINEN, .13)
    rows = VGroup()
    for y in (-1.06, -1.62):
        rows.add(VGroup(box(.22, .22, -4.72, y, LINEN, .02, SLATE),
                        Line(p(-4.44, y-.025), p(-3.42, y-.025), color=SLATE, stroke_width=3)))
    return VGroup(sheet, rows)


class S07ChildGuess(SpokenScene):
    def construct(self):
        left, right = prediction_stalks()
        hands = VGroup(hand(HERO-.47, BASE+.63), hand(OTHER-.47, BASE+.63))
        self.add(kitchen(), left, right, hands)
        self.at("hold up both")
        self.play(*[m.animate.shift(UP*.32) for m in (left, right, hands)], run_time=1.38)
        bob(hands, amp=.06, speed=2)
        bob(left, amp=.045, speed=2)
        bob(right, amp=.045, speed=2)
        self.at("where do you think")
        first = heading("Where will\nthe blue go?", y=1.93, color=GOLD, size=40)
        self.play(FadeIn(first, shift=UP*.12), run_time=.66)
        self.at("will change first")
        second = heading("Which changes first?", y=1.93, color=GOLD, size=40)
        self.play(swap(first, second), run_time=.65)
        self.at("write down the guesses")
        pad = writing_pad()
        self.play(FadeIn(pad[0], shift=UP*.12), run_time=.31)
        self.play(LaggedStart(*[Create(row) for row in pad[1]], lag_ratio=.42), run_time=.75)
        self.finish()


def soft_window():
    pane = box(3.6, 3.36, -3.65, .71, "#3C5462", .18, GLASS)
    bars = VGroup(Line(p(-5.43,.71),p(-1.87,.71),color=GLASS,stroke_width=4),
                  Line(p(-3.65,-.94),p(-3.65,2.37),color=GLASS,stroke_width=4))
    sunlight = VGroup(Dot(p(-5.66,2.44),radius=.25,color=GOLD), *[
        Line(p(-5.66,2.44)+.34*rotate_vector(UP,a), p(-5.66,2.44)+.47*rotate_vector(UP,a),
             color=GOLD,stroke_width=3) for a in np.arange(8)*TAU/8])
    return VGroup(pane, bars, prohibition(sunlight, .56))


class S08Stand(SpokenScene):
    def construct(self):
        leafy, bare = prediction_stalks(.32)
        empty_space = kitchen()
        cups = [glass(HERO), glass(OTHER)]
        self.add(empty_space, leafy, bare, *cups)
        self.at("in two glasses")
        self.play(leafy.animate.shift(DOWN*.32), bare.animate.shift(DOWN*.32), run_time=1.33)
        self.at("keep the third")
        spare = celery(-4.63, base=-1.63, stature=.74)
        tag = heading("Spare stalk", x=-4.66, y=3.11, size=33, width=3.35)
        self.play(FadeIn(spare, shift=UP*.26), run_time=.70)
        self.play(FadeIn(tag), run_time=.45)
        self.at("find a bright spot")
        self.play(FadeOut(tag), FadeOut(spare, shift=LEFT*.26), run_time=.48)
        window = soft_window()
        self.play(FadeIn(window, shift=UP*.24), run_time=.79)
        self.at("stay nearby")
        adult = person(5.38,-.08,1.46)
        self.play(FadeIn(adult, shift=LEFT*.33), run_time=.84)
        bob(adult, amp=.073, speed=1.7)
        self.finish()


def prediction_question():
    return question_card(QUESTION, **QUESTION_STYLE)


class S09PredictQuestion(SpokenScene):
    def construct(self):
        self.add(rig())
        self.at("now a question")
        q = prediction_question()
        self.play(FadeIn(q, shift=UP*.12), run_time=.75)
        self.at("cut across the leafy")
        cut = DashedLine(p(HERO-.66, CUT_Y), p(HERO+.66, CUT_Y), color=GOLD, stroke_width=4)
        blank = section()
        self.play(Create(cut), run_time=.62)
        self.play(FadeIn(blank, shift=LEFT*1.02), run_time=1.13)
        self.at("what do you think")
        self.play(FadeOut(cut), run_time=.3)
        self.play(blank.animate.set_fill("#625951"), rate_func=there_and_back, run_time=1.26)
        self.at("blue all over")
        self.play(blank.animate.set_fill("#625951"), rate_func=there_and_back, run_time=2.65)
        self.finish()


class S10PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    RING_AT = (-3.55, -2.28, 0)
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(rig(), section())

    def construct(self):
        self.add(self.backdrop(), prediction_question())
        ring, turn = countdown(self.SECONDS, center=self.RING_AT, radius=.58)
        self.add(ring)
        self.play(turn)


def observation_clock(hour=0):
    return clock(-4.23, .05, radius=.97, hour=hour)


class S11Checks(SpokenScene):
    def construct(self):
        world = rig(pair=True)
        leafy, bare = world[1:3]
        self.add(world)
        self.at("check after about")
        watch = observation_clock()
        one = heading("About 1 hour", x=-4.23, y=1.86, size=38, width=3.5)
        self.play(FadeIn(watch), FadeIn(one), run_time=.55)
        self.play(Rotate(watch.hand, -TAU/12, about_point=p(-4.23,.05)), run_time=1.35)
        self.at("little may show")
        faint = heading("Little may show", x=-4.23, y=-1.38, size=29, width=3.45)
        self.play(FadeIn(faint), run_time=.60)
        self.at("after about four")
        four = heading("About 4 hours", x=-4.23, y=1.86, size=38, width=3.5)
        self.play(swap(one, four), FadeOut(faint),
                  Rotate(watch.hand, -TAU*.25, about_point=p(-4.23,.05)), run_time=1.30)
        self.at("blue lines most")
        possible = note("Possible result", x=-4.23, y=-1.38, size=29)
        self.play(FadeIn(possible), Create(rib_dye(leafy,.91)),
                  Create(rib_dye(bare, BARE_DYE_FRACTION)), run_time=2.35)
        self.at("leaf edges start")
        self.play(Create(leaf_dye(leafy, edges=True)), run_time=1.5)
        self.at("compare the two")
        markers = VGroup(Line(p(2.10, 1.21), p(2.63, 1.21), color=BLUE, stroke_width=5),
                         Line(p(-1.90, -1.06), p(-1.40, -1.06), color=BLUE, stroke_width=5))
        self.play(Create(markers), run_time=.62)
        self.at("was your guess")
        question = heading("Was your\nguess right?", x=-4.23, y=1.86, size=35, width=3.6, color=GOLD)
        self.play(swap(four, question), FadeOut(markers), run_time=.78)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        world = rig(pair=True)
        leafy, bare = world[1:3]
        old_edges = leaf_dye(leafy, edges=True)
        dyed_ribs = rib_dye(leafy,.91)
        self.add(world, dyed_ribs, rib_dye(bare, BARE_DYE_FRACTION), old_edges)
        self.at("the next day")
        day = heading("Next day", x=-4.23, y=1.86, size=38, width=3.5)
        watch = observation_clock(4)
        self.play(FadeIn(watch), FadeIn(day), run_time=.57)
        self.play(Rotate(watch.hand, -TAU*1.67, about_point=p(-4.23,.05)), run_time=2.16)
        self.at("blue veins in")
        self.play(Create(leaf_dye(leafy)), Transform(dyed_ribs,rib_dye(leafy)), run_time=1.8)
        self.at("cut across the stalk")
        tool = knife(1.62, CUT_Y)
        self.play(FadeOut(watch), FadeIn(tool, shift=RIGHT*.23), run_time=.78)
        self.play(tool.animate.shift(RIGHT*.55), run_time=.53)
        self.at("three centimeters above")
        measure = Line(p(4.27, SURFACE), p(4.27, CUT_Y), color=GOLD, stroke_width=3).add_tip(tip_length=.14)
        value = place_label(T("3 cm", 33, GOLD), measure, dirs=(RIGHT,), buff=.24)
        self.play(FadeOut(tool), Create(measure), FadeIn(value), run_time=.76)
        self.at("look for a curved")
        self.play(FadeOut(measure), FadeOut(value), FadeIn(section(filled=True)), run_time=.57)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in section_dots()], lag_ratio=.44), run_time=1.32)
        self.at("each dot marks")
        self.play(swap(day, heading("Each dot marks\na bundle of water tubes", x=-3.6, y=2.04, size=36)),
                  run_time=.83)
        self.finish()


def tube_arrows(plant, fractions):
    arrows = VGroup()
    for rib, (start, end) in zip(plant.ribs, fractions):
        a, b = rib.point_from_proportion(start), rib.point_from_proportion(end)
        arrows.add(Arrow(a, b, buff=0, color=BLUE, stroke_width=6, max_tip_length_to_length_ratio=.25))
    return arrows


class S13Why(SpokenScene):
    def construct(self):
        world = rig(pair=True)
        leafy, bare = world[1:3]
        veins = leaf_dye(leafy)
        self.add(world, veins)
        self.at("why the leaves")
        leaf_caption = heading("Water leaves\nthrough tiny pores", y=1.93, x=-3.78, size=37, width=4.65)
        self.play(Indicate(leafy.crown, color=PALE, scale_factor=1.04), run_time=1.4)
        self.at("water dries off")
        vapor(self)
        self.play(FadeIn(leaf_caption), run_time=.7)
        self.at("as it leaves")
        self.play(swap(leaf_caption, heading("More water is\npulled up the tubes", y=1.93, x=-3.78, size=37, width=4.65)),
                  Create(rib_dye(leafy)), run_time=2.85)
        arrows = tube_arrows(leafy, [(.24,.55),(.46,.77),(.18,.50),(.36,.69)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.25), run_time=1.05)
        self.at("the stalk with leaves")
        short = tube_arrows(bare, [(.22,.32),(.33,.43),(.19,.29),(.29,.39)])
        self.play(Create(rib_dye(bare,.4)), LaggedStart(*[GrowArrow(a) for a in short], lag_ratio=.32),
                  run_time=1.7)
        self.finish()


def pet(x, y):
    head = Circle(radius=.36, fill_color=SKIN, fill_opacity=1, stroke_width=0)
    ears = VGroup(box(.24,.52,-.29,.22,WOOD,.11), box(.24,.52,.29,.22,WOOD,.11))
    face = VGroup(*[Dot(p(a,b), radius=r, color=BG) for a,b,r in [(-.12,.06,.034),(.12,.06,.034),(0,-.10,.056)]])
    return VGroup(head, ears, face).shift(p(x,y))


def washing():
    tap = path([(-4.93,.62),(-4.93,1.07),(-4.54,1.29),(-3.82,1.29),(-3.49,1.06),(-3.49,.79)], GLASS, 11)
    hands = VGroup(hand(-3.48,-.97,.18), hand(-3.10,-.65,-.28))
    drops = VGroup(*[drop(-3.50+.13*(i%2),.61-i*.24,.15) for i in range(5)])
    suds = VGroup(*[Circle(radius=.09+.026*(i%3), color=TEXT, stroke_width=2)
                    .move_to(p(-3.92+.23*i,-.49+.17*np.sin(i))) for i in range(6)])
    return VGroup(tap, hands, drops, suds)


class S14Safety(SpokenScene):
    def construct(self):
        world = rig(pair=True)
        self.add(world)
        self.at("stay nearby")
        adult = person(-3.91,.27,1.58)
        first = heading("Stay nearby", x=-3.91, y=2.12, size=36)
        self.play(FadeIn(adult, shift=RIGHT*.34), FadeIn(first), run_time=.75)
        bob(adult, amp=.12, speed=1.9)
        self.at("use sturdy glasses")
        stable = heading("Use sturdy glasses", x=-3.91, y=2.12, size=35)
        sturdy = glass(-3.92, level=-.42, base=-1.30)
        self.play(swap(first, stable), FadeOut(adult), FadeIn(sturdy), run_time=.73)
        self.at("away from toddlers")
        small = VGroup(person(-4.45,.11,.71,child=True), pet(-3.47,-.35))
        barrier = Line(p(-2.89,-1.44), p(-2.89,.83), color=RED, stroke_width=6)
        away = heading("Away from toddlers\nand pets", x=-3.91, y=2.12, size=34)
        self.play(swap(stable, away), FadeOut(sturdy), FadeIn(small), Create(barrier), run_time=.65)
        self.play(small.animate.shift(LEFT*.43), run_time=1.38)
        self.at("nobody eats")
        mouth = Arc(angle=PI, start_angle=PI, radius=.49, color=TEXT, stroke_width=7).move_to(p(-3.85,-.09))
        no = prohibition(mouth, .86)
        keep = heading("Do not eat or drink", x=-3.91, y=2.12, size=35)
        self.play(swap(away,keep), FadeOut(small), FadeOut(barrier), FadeIn(no), run_time=.8)
        self.at("throw both away")
        self.play(FadeOut(no), FadeOut(world[1:], shift=DOWN*.33), run_time=.72)
        self.at("wash hands with")
        soap = heading("Wash with soap", x=-.10, y=2.12, size=35)
        wash = washing().shift(RIGHT*3.8).scale(1.15)
        self.play(swap(keep, soap), FadeIn(wash), run_time=.82)
        for i, bead in enumerate(wash[2]):
            bob(bead, amp=.09, speed=4, seed=i)
        self.finish()


class S15Debrief(SpokenScene):
    def construct(self):
        world = rig()
        plant = world[1]
        veins = leaf_dye(plant)
        ribs = rib_dye(plant)
        self.add(world, ribs, veins)
        vapor(self)
        self.at("to finish ask")
        ask = heading("Where did\nthe water go?", y=1.75, color=GOLD, size=48)
        self.play(FadeIn(ask, shift=UP*.18), run_time=.7)
        trace = VMobject(stroke_color=BLUE, stroke_width=7)
        trace.set_points_smoothly([p(HERO-.10,-2.48),p(HERO-.07,-.64),p(HERO,1.58),p(HERO+.84,2.36)])
        self.at("where did the water")
        self.play(ShowPassingFlash(trace, time_width=.32), run_time=2.65)
        self.at("the color only")
        visible = heading("Color shows the path", y=1.75, size=39)
        self.play(swap(ask, visible, run_time=.65), ShowPassingFlash(trace.copy(), time_width=.28, run_time=2.1))
        self.at("with clear water")
        clear = heading("Clear water\nstill climbs", y=1.75, size=43)
        self.play(swap(visible, clear), FadeOut(ribs), FadeOut(veins),
                  world[2][0][0].animate.set_fill("#647F8C").set_stroke("#647F8C"), run_time=1.16)
        self.finish()


class S16End(EndCard):
    LINE = "Water climbs a plant through tiny tubes, pulled up by the leaves."
