"""The Blubber Glove: shared cutaways and word-cued tabletop animation."""

from bp_parts import *
from bp_style import EndCard

# COLOR MAP: blue = ice and cold water, cream = shortening and blubber,
# gold = body warmth, slate = plastic/skin, red = stop and safety.
WATER = "#245675"
DEEP = "#183953"
PALE = "#FFE7B4"
WARM = "#F4AA57"
PLASTIC = "#A3C9DA"
SEAL = "#7893A7"
TABLE = "#583D38"
TABLE_EDGE = "#AB7560"
QUESTION = "Which way does heat move?"
QUESTION_STYLE = dict(y=3.14, size=43, color=TEXT, max_w=10.4)


def p(x, y):
    return np.array([x, y, 0.0])


def path(start, segments, fill, stroke=None, width=3, opacity=1):
    shape = VMobject()
    shape.start_new_path(p(*start))
    for c1, c2, end in segments:
        shape.add_cubic_bezier_curve_to(p(*c1), p(*c2), p(*end))
    shape.set_fill(fill, opacity).set_stroke(stroke or fill, width)
    return shape


def ice(x=0, y=0, size=0.65):
    base = Polygon(p(-.48, -.27), p(.24, -.43), p(.52, -.08), p(.38, .36), p(-.31, .44),
                   fill_color=BLUE, fill_opacity=1, stroke_color=PLASTIC, stroke_width=2)
    face = Polygon(p(-.48, -.27), p(.24, -.43), p(.34, .08), p(-.31, .44),
                   fill_color=WATER, fill_opacity=.5, stroke_width=0)
    gleam = Line(p(-.21, .32), p(.23, .22), color=TEXT, stroke_width=3)
    return VGroup(base, face, gleam).scale(size).move_to(p(x, y))


def ripple(x, y, length):
    return path((x-length/2, y), [((x-length/6, y+.16), (x+length/6, y-.16), (x+length/2, y))],
                BLUE, BLUE, 3, 0).set_stroke(opacity=.56)


def ocean(surface=True, moving=True):
    top = 2.35 if surface else 2.61
    field = RoundedRectangle(width=13.16, height=top+3.52, corner_radius=.32,
                             fill_color=DEEP, fill_opacity=1, stroke_width=0).move_to(p(0, (top-3.52)/2))
    layers = VGroup(field)
    for j, (y, x, color) in enumerate([(1.60, -.25, WATER), (.54, .24, "#204B68"), (-.72, -.21, "#21465F"),
                                       (-1.86, .22, "#1B415B"), (-2.88, -.12, "#1C3D56")]):
        slab = RoundedRectangle(width=11.9, height=.64, corner_radius=.29, fill_color=color,
                                fill_opacity=1, stroke_width=0).move_to(p(x, y))
        if moving and not surface:
            bob(slab, amp=.17, speed=1.9+.16*j, seed=2*j)
        layers.add(slab)
        for k, dx in enumerate((-3.85, 0, 3.85)):
            wave = ripple(dx+x, y+.07*(-1)**k, 1.36+.34*((j+k)%3))
            if moving:
                bob(wave, amp=.13, speed=1.7, seed=3*j+k)
            layers.add(wave)
    if surface:
        for j, (x, y, s) in enumerate([(-5.35, 2.05, 1.05), (-2.76, 2.21, .71), (2.50, 2.14, .86), (5.31, 2.05, 1.12)]):
            cube = ice(x, y, s).rotate(.16*(-1)**j)
            layers.add(bob(cube, amp=.14, speed=1.8, seed=j) if moving else cube)
    else:
        for j, (x, y, size) in enumerate([(-4.79,1.33,.94), (4.68,.38,.89), (-3.82,-1.91,.82), (4.15,-2.17,1.09)]):
            cube = ice(x, y, size).rotate(.19*(-1)**j)
            layers.add(bob(cube, amp=.20, speed=1.72+.21*j, seed=j) if moving else cube)
    return layers.set_z_index(-8)


def seal(cut=False):
    tail = path((-3.55, -.56), [((-4.67, -.15), (-5, .37), (-5.13, 1.13)),
                ((-4.5, 1.17), (-4.04, .73), (-3.91, .48)),
                ((-4, 1.07), (-3.77, 1.44), (-3.4, 1.59)),
                ((-3.07, .85), (-3.17, .3), (-3.55, -.56))], SEAL, PLASTIC)
    flipper = path((1.33, -.99), [((1.1, -2.11), (-.16, -2.65), (-1.03, -2.13)),
                   ((-.6, -1.94), (-.27, -1.19), (.19, -.64)),
                   ((.59, -.47), (1.21, -.61), (1.33, -.99))], "#56738C", PLASTIC)
    body = path((-4.08, -.43), [((-3.28, .89), (-1.23, 1.75), (1.02, 1.12)),
                 ((1.97, .83), (2.29, 1.22), (2.81, 1.47)),
                 ((3.69, 1.96), (4.41, 1.41), (4.5, .73)),
                 ((5.24, .7), (5.44, .11), (4.88, -.21)),
                 ((4.19, -.74), (3.09, -.58), (2.38, -1.12)),
                 ((.77, -2.04), (-2.41, -1.75), (-4.08, -.43))], SEAL, PLASTIC, 4)
    belly = path((-3.23, -.56), [((-1.48, -.81), (1.09, -1.04), (2.62, -.66)),
                  ((1.14, -1.83), (-1.69, -1.64), (-3.23, -.56))], "#55738C", width=0)
    eye = VGroup(Dot(p(3.87, .92), radius=.14, color=BG),
                 Dot(p(3.91, .97), radius=.042, color=TEXT))
    nose = Ellipse(width=.31, height=.2, color=BG, fill_opacity=1).move_to(p(5.02, .37))
    smile = ArcBetweenPoints(p(4.16, .08), p(4.95, .25), angle=.51, color=BG, stroke_width=3)
    whiskers = VGroup(*[Line(p(4.62, .18), p(5.40, y), color=PLASTIC, stroke_width=2) for y in (.34, .08, -.16)])
    pattern = VGroup(*[Ellipse(width=w, height=.11, fill_color=DEEP, fill_opacity=.37, stroke_width=0)
                       .rotate(-.17).move_to(p(x, y)) for x, y, w in
                       [(-2.38,.28,.29),(-1.84,.64,.19),(-1.42,.78,.33),(-.86,.79,.18),(-.35,.66,.32),
                        (.17,.76,.20),(.6,.57,.28),(1.09,.5,.19),(-2.82,-.03,.3),(-2.15,-.12,.20)]])
    patch = Ellipse(width=4.72, height=1.98, stroke_color=PLASTIC, stroke_width=5,
                    fill_color=PALE, fill_opacity=1).move_to(p(-.45, -.27))
    core = Ellipse(width=3.94, height=1.26, stroke_width=0, fill_color=WARM, fill_opacity=1).move_to(p(-.45, -.27))
    animal = VGroup(tail, flipper, body, belly, pattern, eye, nose, smile, whiskers)
    animal.cutaway = VGroup(patch, core)
    if cut:
        animal.add(animal.cutaway)
    return animal


def swim(animal):
    base = animal.get_center().copy()
    def glide(mob, dt):
        mob.phase += dt
        mob.move_to(base + RIGHT*.61*np.sin(1.08*mob.phase) + UP*.18*np.sin(1.65*mob.phase))
    animal.phase = 0
    return animal.add_updater(glide)


def tabletop():
    slab = RoundedRectangle(width=13.15, height=4.58, corner_radius=.33, stroke_width=0,
                             fill_color=TABLE, fill_opacity=1).move_to(p(0, -1.20))
    edge = Line(p(-6.25, 1.055), p(6.25, 1.055), color=TABLE_EDGE, stroke_width=5)
    grain = VGroup(*[Line(p(x, y), p(x+w, y), color=TABLE_EDGE, stroke_width=2).set_opacity(.34)
                     for x, y, w in [(-5.9,.42,3.3),(3.9,.48,2.1),(-6.03,-1.5,4.2),
                                     (3.5,-2.14,2.4),(-4.6,-2.83,3.8),(.63,-3.12,4.9)]])
    return VGroup(slab, edge, grain).set_z_index(-8)


def bag_outline(width=2.54, height=3.67, edge=PLASTIC, fill=DEEP, opacity=1, rim=BLUE, front_rim=False):
    w, h = width/2, height
    sack = path((-w, 0), [((-w*.92,-h*.18),(-w*1.07,-h*.77),(-w*.86,-h*.91)),
                           ((-w*.62,-h*1.03),(w*.62,-h*1.03),(w*.86,-h*.91)),
                           ((w*1.07,-h*.77),(w*.92,-h*.18),(w,0)),
                           ((w*.32,-.17),(-w*.32,-.17),(-w,0))], fill, edge, 3, opacity)
    opening = Ellipse(width=width, height=.35, color=rim, stroke_width=3,
                      fill_color=BG, fill_opacity=.97)
    bag = VGroup(sack, opening)
    if front_rim:
        opening.set_z_index(7)
        lip = Arc(start_angle=PI, angle=PI, color=rim, stroke_width=3, fill_opacity=0)
        lip.stretch_to_fit_width(width).stretch_to_fit_height(.175).move_to(p(0,-.0875))
        bag.add(lip.set_z_index(10))
    return bag


def tape_tabs():
    return VGroup(*[RoundedRectangle(width=.48, height=.41, corner_radius=.065, stroke_width=0,
                                     fill_color=GOLD, fill_opacity=1).rotate(.16*side)
                    .move_to(p(side*1.12,-.035)) for side in (-1, 1)])


def mitten(x, top, fat=True, scale=1, flat=False, taped=True):
    outer = bag_outline(fill=PALE if fat else WATER, edge=PLASTIC, front_rim=True)
    inner = bag_outline(1.78 if fat else 2.31, 3.04 if fat else 3.44,
                        edge=TEXT, fill=DEEP, front_rim=True).shift(DOWN*.13)
    tabs = tape_tabs().set_z_index(11)
    item = VGroup(outer, inner, tabs) if taped else VGroup(outer, inner)
    if flat:
        item.stretch(.86, 0, about_point=ORIGIN)
    return item.scale(scale, about_point=ORIGIN).shift(p(x, top))


def hand(color=WARM):
    return path((-.57,1.08), [((-.59,.54),(-.52,.22),(-.58,-.06)),
                ((-.89,.18),(-1.13,-.06),(-.98,-.35)),
                ((-.93,-.50),(-.72,-.77),(-.69,-1.06)),
                ((-.58,-1.76),(-.29,-2.27),(.06,-2.16)),
                ((.39,-2.32),(.70,-1.87),(.68,-1.51)),
                ((.79,-.97),(.64,-.34),(.56,-.09)),
                ((.49,.3),(.52,.76),(.53,1.08)),
                ((.32,1.27),(-.38,1.27),(-.57,1.08))], color, PALE, 2.5)


def hand_in_bag(x, top, scale=.8):
    return hand().scale(.81*scale, about_point=ORIGIN).shift(p(x, top+.08)).set_z_index(8)


def bowl(cx=.55, cy=-1.0, scale=1, level=2/3, iced=True, moving=True):
    shadow = Ellipse(width=9.45, height=.69, fill_color="#2D2429", fill_opacity=1,
                     stroke_width=0).shift(DOWN*1.30)
    shell = path((-4.54,.55), [((-4.43,-.33),(-3.23,-1.24),(-2.66,-1.32)),
                  ((-1.13,-1.61),(1.13,-1.61),(2.66,-1.32)),
                  ((3.23,-1.24),(4.43,-.33),(4.54,.55)),
                  ((3.16,1.75),(-3.16,1.75),(-4.54,.55))], "#4E829A", PLASTIC, 4)
    rim = Ellipse(width=9.08, height=2.12, stroke_color=PLASTIC, stroke_width=4,
                  fill_color=DEEP, fill_opacity=1).move_to(p(0,.56))
    surface = Ellipse(width=8.16, height=1.49, fill_color=WATER, fill_opacity=1,
                      stroke_color=BLUE, stroke_width=3).move_to(p(0,.43))
    surface.stretch(.66+.34*level/(2/3), 0).shift(DOWN*(2/3-level)*.38)
    waves = VGroup(*[ripple(x,y,l) for x,y,l in [(-1.9,.76,2.24),(1.28,.76,2.15),(-2.58,.16,1.69),(.14,-.06,1.43),(2.66,.18,1.38)]])
    cubes = VGroup(*[ice(x,y,s).rotate(a) for x,y,s,a in
                     [(-3.4,.63,.71,.15),(-.35,1.00,.56,-.15),(.2,.10,.61,.16),(.48,.89,.61,.3),(3.36,.45,.72,-.22)]])
    band = ArcBetweenPoints(p(-3.65,-.53), p(3.65,-.53), angle=.43, color=PLASTIC, stroke_width=2)
    model = VGroup(shadow, shell, rim, band)
    if level:
        model.add(surface, waves)
    if iced:
        model.add(cubes)
    model.scale(scale, about_point=ORIGIN).shift(p(cx, cy))
    for i, wave in enumerate(waves):
        if moving and level:
            bob(wave, amp=.105, speed=2.2, seed=i)
    for i, cube in enumerate(cubes):
        if moving and iced:
            bob(cube, amp=.085, speed=1.9, seed=i)
    model.water = VGroup(surface, waves)
    model.cubes = cubes
    return model.set_z_index(-3)


def pair(fat_left=True, top=1.85, scale=.8, hands=False):
    bags = VGroup(mitten(-1.43, top, fat_left, scale), mitten(2.45, top, not fat_left, scale))
    if hands:
        bags.add(hand_in_bag(-1.43, top, scale), hand_in_bag(2.45, top, scale))
    return bags


def ready_table():
    return tabletop(), bowl(), pair()


def dipped(fat_left=True):
    return pair(fat_left, top=.51, hands=True)


def water_in_front():
    """Transparent bowl wall below the waterline, over the submerged tips."""
    lens = path((-3.55,-.53), [((-2.63,.24),(3.63,.24),(4.64,-.53)),
                 ((4.36,-1.39),(3.52,-2.09),(3.18,-2.18)),
                 ((1.60,-2.48),(-.45,-2.48),(-2.08,-2.18)),
                 ((-2.62,-1.97),(-3.28,-1.27),(-3.55,-.53))], BLUE, BLUE, 0, .26)
    line = path((-3.55,-.53), [((-2.63,.24),(3.63,.24),(4.64,-.53))], BLUE, BLUE, 4, 0)
    return VGroup(lens,line).set_z_index(9)


def heading(value, color=TEXT, size=36, y=3.2, x=0):
    return fit_text(value, max_w=10.45, size=size, min_size=28, color=color, weight=BOLD).move_to(p(x,y))


def press_arrow(start, end, color=TEXT):
    return Arrow(p(*start), p(*end), buff=0, color=color, stroke_width=5, max_tip_length_to_length_ratio=.23)


def clock(tracker, x, y, scale=1, duration=60, numeric=True, progress=False):
    center = p(x,y)
    circle = Circle(radius=1.06*scale, stroke_color=PLASTIC, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(center)
    ticks = VGroup(*[Line(center + .82*scale*rotate_vector(UP, k*TAU/12),
                          center + .96*scale*rotate_vector(UP, k*TAU/12), color=PLASTIC, stroke_width=2)
                     for k in range(12)])
    needle = Line(center, center+UP*.72*scale, color=GOLD, stroke_width=5)
    def set_needle(line):
        tip = rotate_vector(UP, -TAU*tracker.get_value()/duration)*.72*scale
        dial_center = circle.get_center()
        line.put_start_and_end_on(dial_center, dial_center+tip)
    needle.add_updater(set_needle)
    face = VGroup(circle, ticks, needle, Dot(center, radius=.07*scale, color=GOLD))
    if progress:
        face.add(always_redraw(lambda: Arc(radius=1.15*scale, start_angle=PI/2,
                 angle=-TAU*max(.002, tracker.get_value()/duration), arc_center=center,
                 stroke_color=GOLD, stroke_width=11)))
    if numeric:
        face.add(counter("{:02.0f} s", tracker, center+DOWN*(1.39*scale+.11), color=TEXT, size=29))
    return face


def timer_icon():
    t = clock(ValueTracker(0), 0, 0, .68, numeric=False)
    crown = RoundedRectangle(width=.43,height=.19,corner_radius=.055,fill_color=PLASTIC,fill_opacity=1,stroke_width=0)
    return VGroup(t, crown.move_to(p(0,.77)))


def plain_bag(x, y, scale=1):
    return bag_outline(2.1, 3.1, fill=WATER, opacity=.93).scale(scale, about_point=ORIGIN).shift(p(x,y))


def tub(x, y):
    body = RoundedRectangle(width=2.62,height=1.74,corner_radius=.28,stroke_color=PLASTIC,stroke_width=3,
                            fill_color=DEEP,fill_opacity=1).move_to(p(x,y))
    lid = RoundedRectangle(width=2.8,height=.32,corner_radius=.12,stroke_width=0,
                           fill_color=PALE,fill_opacity=1).move_to(p(x,y+.82))
    return VGroup(body,lid,T("Shortening", 30, PALE).move_to(p(x,y)))


def roll(x, y):
    body = Ellipse(width=1.53,height=1.07,fill_color=GOLD,fill_opacity=1,stroke_width=0).move_to(p(x,y))
    hole = Ellipse(width=.89,height=.53,fill_color=TABLE,fill_opacity=1,stroke_width=0).move_to(p(x,y+.05))
    tab = Polygon(p(x+.49,y-.34),p(x+1.08,y-.69),p(x+1.36,y-.48),p(x+.69,y-.15),
                  stroke_width=0,fill_color=PALE,fill_opacity=1)
    return VGroup(body, tab, hole)


def towel(x, y, scale=1):
    cloth = RoundedRectangle(width=2.77,height=1.25,corner_radius=.18,stroke_color=PLASTIC,stroke_width=3,
                             fill_color=TEAL,fill_opacity=1)
    fold = Line(p(-1.21,-.37),p(1.21,-.37),color=DEEP,stroke_width=4)
    hem = Line(p(.98,-.38),p(.98,.49),color=TEXT,stroke_width=3)
    return VGroup(cloth,fold,hem).scale(scale).move_to(p(x,y))


def tray():
    base = RoundedRectangle(width=1.76,height=.82,corner_radius=.17,stroke_color=PLASTIC,
                            stroke_width=3,fill_color=DEEP,fill_opacity=1)
    return VGroup(base,*[ice(x, y, .34) for x in (-.55,0,.55) for y in (-.19,.19)])


def sea_question(moving=True):
    sea = ocean(surface=False, moving=moving)
    glove = mitten(-.2, 2.03, scale=1.25)
    palm = hand().scale(.92, about_point=ORIGIN).shift(p(-.2,.79)).set_z_index(8)
    if moving:
        pulse(palm, base=3, amp=1.3, speed=2.4)
    return sea, glove, palm


def predict_text():
    return question_card(QUESTION, **QUESTION_STYLE)


def heat_flow(start, end, seconds, direction, width=4):
    start, end = p(*start), p(*end)
    vec = end-start
    arrow = Arrow(ORIGIN, RIGHT*.56, buff=0, color=GOLD, stroke_width=width,
                  max_tip_length_to_length_ratio=.4).rotate(angle_of_vector(direction))
    phase = ValueTracker(0)
    def travel(mob, dt):
        phase.increment_value(dt/seconds)
        t = phase.get_value() % 1
        mob.move_to(start + vec*t).set_opacity(min(1, 8*t, 8*(1-t)))
    arrow.add_updater(travel)
    return arrow


class S01Hook(SpokenScene):
    def construct(self):
        sea, animal = ocean(), seal()
        self.at("picture a seal")
        self.add(sea, swim(animal))
        self.at("how does it stay", lead=.45)
        animal.cutaway.shift(RIGHT*.61*np.sin(1.08*animal.phase) + UP*.18*np.sin(1.65*animal.phase))
        animal.add(animal.cutaway)
        self.play(FadeIn(animal.cutaway), run_time=.48)
        question = heading("How does it stay warm?", size=44)
        self.play(Write(question), run_time=.68)
        self.at("with four zip bags", lead=.44)
        table, basin, bags = ready_table()
        animal.clear_updaters()
        self.play(FadeOut(question), FadeOut(sea), FadeIn(table), FadeIn(basin),
                  ReplacementTransform(animal, bags), run_time=1.10)
        self.at("vegetable shortening")
        self.play(bags[0].animate(rate_func=there_and_back).shift(UP*.27), run_time=2.0)
        self.finish()


class S02Title(TitleCard):
    TITLE = "The Blubber Glove: Parent Guide"
    LESSON = "The Blubber Glove"

    def construct(self):
        self.add(*ready_table())
        title = T(self.LESSON, 55, font=TITLE_FONT).move_to(p(0,3.18))
        self.play(FadeIn(title, shift=UP*.13), run_time=.55)
        self.wait(self.narration_s - .55)


class S03WhatChildGets(SpokenScene):
    def construct(self):
        table, basin, bags = ready_table()
        self.add(table, basin, bags)
        self.at("30 minute activity")
        intro = heading("30-minute activity", y=3.17)
        self.play(FadeIn(intro), run_time=.5)
        self.at("making a guess", lead=.55)
        guess = boxed_label("Make a guess", color=TEXT, size=32, fill_opacity=.07).move_to(p(0,3.29))
        self.play(swap(intro, guess, .62))
        self.at("checking it right away")
        hands = VGroup(hand_in_bag(-1.43, 1.85), hand_in_bag(2.45, 1.85))
        self.play(FadeIn(hands), run_time=1.12)
        self.at("compare how their hands", lead=.5)
        compare = boxed_label("Compare both hands", color=TEXT, size=32, fill_opacity=.07).move_to(p(0,3.32))
        self.play(swap(guess, compare, .7))
        self.play(ShowPassingFlash(bags[0][0][0].copy().set_fill(opacity=0).set_stroke(PALE,7), time_width=.55),
                  run_time=2.0)
        self.at("switching mittens", lead=.8)
        arrows = VGroup(CurvedArrow(p(-.25,1.44),p(1.3,1.44),angle=-.8,color=GOLD),
                        CurvedArrow(p(1.3,.70),p(-.25,.70),angle=-.8,color=GOLD))
        repeat = boxed_label("Swap and repeat", color=TEXT, size=32, fill_opacity=.07).move_to(p(0,3.32))
        self.play(swap(compare, repeat, .7), Create(arrows), run_time=.85)
        self.at("stay with your child", lead=.42)
        stay = heading("Stay with your child", color=PALE, y=3.22)
        self.play(swap(repeat, stay, .68), FadeOut(arrows), FadeOut(hands), run_time=.75)
        self.finish()


class S04MaterialsAndBuild(SpokenScene):
    def construct(self):
        self.add(tabletop())
        self.at("set out four matching")
        bags = VGroup(*[plain_bag(-4.99+i*1.39, 1.31, .85) for i in range(4)])
        title = heading("4 matching gallon-size zip bags")
        self.play(LaggedStart(*[FadeIn(bag, shift=UP*.34) for bag in bags], lag_ratio=.27), run_time=1.55)
        self.play(FadeIn(title), run_time=.56)
        tape, cloth, timepiece = roll(1.3,-.45), towel(4.12,-.77,.78), VGroup(timer_icon()).move_to(p(1.35,1.54))
        basin = bowl(3.52,-2.22,.51,level=0,iced=False)
        self.at("tape towels", lead=.30)
        self.play(FadeIn(tape,shift=UP*.22), run_time=.47)
        self.at("towels a timer")
        self.play(FadeIn(cloth,shift=UP*.22), run_time=.51)
        self.at("timer and a bowl")
        self.play(FadeIn(timepiece,shift=UP*.18), run_time=.56)
        self.at("a bowl", lead=.15)
        self.play(FadeIn(basin,shift=UP*.25), run_time=.75)
        self.at("the vegetable shortening", lead=.52)
        shortening = tub(4.52,1.48)
        check = heading("Check the label for allergies", color=PALE)
        self.play(FadeIn(shortening, shift=UP*.2), swap(title, check), run_time=.86)
        self.at("put about two cups", lead=.62)
        outer = bag_outline().shift(p(-1.43,1.86))
        inner = bag_outline(1.78,3.04,edge=TEXT).shift(p(1.83,1.73)).set_z_index(1)
        self.play(ReplacementTransform(bags[0], outer), ReplacementTransform(bags[1], inner),
                  FadeOut(bags[2]), FadeOut(bags[3]), FadeOut(check),
                  FadeOut(cloth), FadeOut(tape), FadeOut(timepiece), FadeOut(basin), run_time=.91)
        portion = RoundedRectangle(width=1.93,height=.82,corner_radius=.38,stroke_width=0,fill_color=PALE,
                                   fill_opacity=1).move_to(p(4.52,2.68))
        amount = heading("About 2 cups", color=PALE, x=-.4)
        self.play(FadeIn(portion), FadeIn(amount), run_time=.41)
        self.play(portion.animate.move_to(p(-1.43,-1.08)), path_arc=-.65, run_time=1.30)
        self.at("slip a second bag", lead=.37)
        self.play(inner.animate.shift(LEFT*3.26), FadeOut(amount), FadeOut(shortening), run_time=1.65)
        self.at("tape the folded rims", lead=.27)
        tabs = tape_tabs().shift(p(-1.43,1.85))
        self.play(LaggedStart(*[FadeIn(tab,shift=DOWN*.45) for tab in tabs],lag_ratio=.44),run_time=1.30)
        open_label = heading("Leave the inner bag open", y=2.92)
        self.at("leave the inner bag")
        self.play(FadeIn(open_label), run_time=.52)
        self.at("spread the shortening", lead=.34)
        small = mitten(-1.43,1.85,True,.8)
        width = heading("About a finger’s width", color=PALE, y=2.92)
        lining = small[0][0].copy()
        self.play(Transform(portion, lining), Transform(outer, small[0]), Transform(inner,small[1]),
                  Transform(tabs,small[2]), swap(open_label,width),run_time=1.22)
        self.remove(portion,outer,inner,tabs)
        self.add(small)
        self.finish()


class S05FairTestAndChill(SpokenScene):
    def construct(self):
        lined = mitten(-1.43,1.85,True,.8)
        self.add(tabletop(), lined)
        self.at("make a plain mitten")
        flat = mitten(2.45,1.85,False,.8,flat=True)
        empty = mitten(2.45,1.85,False,.8)
        b1, b2 = plain_bag(2.45,1.98,.9), plain_bag(4.23,2.49,.86)
        self.play(FadeIn(b1,shift=LEFT*.37), run_time=.59)
        self.play(FadeIn(b2,shift=LEFT*.45), run_time=.71)
        self.at("the other two bags")
        self.play(ReplacementTransform(VGroup(b1,b2),empty),run_time=1.34)
        self.at("squeeze out extra air", lead=.4)
        press = VGroup(press_arrow((.58,.65),(1.32,.65),BLUE), press_arrow((4.4,.65),(3.53,.65),BLUE))
        title = heading("Squeeze out extra air")
        self.play(GrowArrow(press[0]), GrowArrow(press[1]),FadeIn(title),run_time=.66)
        self.play(Transform(empty,flat), press[0].animate.shift(RIGHT*.14), press[1].animate.shift(LEFT*.14),run_time=1.11)
        self.at("the only difference")
        difference = heading("Same bags. Only one has fat.", PALE)
        self.play(swap(title,difference),FadeOut(press),run_time=.73)
        self.at("fill the bowl",lead=.59)
        basin = bowl(level=0,iced=False)
        full = bowl(moving=False)
        fill_label = heading("Two-thirds full", PALE)
        self.play(swap(difference,fill_label,.67),FadeIn(basin,shift=UP*.22),run_time=.67)
        water = full.water.copy().set_z_index(-2.5)
        self.play(GrowFromCenter(water),run_time=1.12)
        self.at("add two trays",lead=.34)
        trays = VGroup(tray().move_to(p(-4.55,.55)),tray().move_to(p(4.87,.59)))
        self.play(FadeOut(fill_label),FadeIn(trays,shift=DOWN*.38),run_time=.38)
        full.cubes.set_z_index(-2)
        self.play(ReplacementTransform(trays, full.cubes),run_time=.77)
        self.add(full.cubes)
        for i, cube in enumerate(full.cubes):
            bob(cube,amp=.085,speed=1.9,seed=i)
        self.at("wait five minutes",lead=.17)
        t = ValueTracker(0)
        watch = clock(t,-4.78,1.27,.82,duration=5,numeric=False)
        wait = heading("Wait 5 minutes",PALE)
        self.play(FadeIn(watch),FadeIn(wait),run_time=.45)
        self.play(t.animate.set_value(4.99),rate_func=linear,run_time=1.22)
        self.finish()


class S06PhrasesAndDip(SpokenScene):
    def construct(self):
        self.add(tabletop(),bowl())
        bags = pair()
        self.add(bags)
        self.at("feel the shortening",lead=.64)
        touch = hand().scale(.68).rotate(PI/2).move_to(p(-4.43,.47))
        self.play(FadeIn(touch,shift=RIGHT*.6),run_time=.64)
        self.play(touch.animate.shift(RIGHT*.77),run_time=.68)
        echo = ArcBetweenPoints(p(-2.4,-.24),p(-2.40,1.26),angle=-.85,color=TEXT,stroke_width=5)
        self.play(ShowPassingFlash(echo,time_width=.73),run_time=1.10)
        self.at("does it feel warm",lead=.49)
        feel = question_card("Does it feel warm or cool?",**QUESTION_STYLE)
        self.play(FadeIn(feel),FadeOut(touch,shift=LEFT*.57),run_time=.53)
        self.at("which hand will feel",lead=.47)
        predict = question_card("Which hand will feel cold first?",**QUESTION_STYLE)
        self.play(swap(feel,predict,.68))
        self.at("write down the guess",lead=.28)
        paper = RoundedRectangle(width=1.61,height=1.92,corner_radius=.13,fill_color=TEXT,fill_opacity=1,stroke_width=0).move_to(p(5.1,1.47))
        lines = VGroup(*[Line(p(4.59,y),p(5.57,y),color=DEEP,stroke_width=3) for y in (1.91,1.57,1.23)])
        self.play(FadeIn(paper,shift=UP*.32),run_time=.36)
        self.play(LaggedStart(*[Create(line) for line in lines],lag_ratio=.65),run_time=.87)
        self.at("dip both mittens",lead=.64)
        hands = VGroup(hand_in_bag(-1.43,1.85),hand_in_bag(2.45,1.85))
        self.play(FadeOut(predict), FadeOut(VGroup(paper,lines)), FadeIn(hands,shift=DOWN*.3),run_time=.58)
        wet = water_in_front()
        self.play(VGroup(bags,hands).animate.shift(DOWN*1.34),
                  Succession(Wait(.75), FadeIn(wet,run_time=.57)),run_time=1.32)
        self.at("the openings above",lead=.43)
        tip = heading("Openings above water",TEXT)
        self.play(FadeIn(tip),run_time=.47)
        self.at("start the timer",lead=.48)
        t = ValueTracker(0)
        watch = clock(t,-4.74,1.32,.82,numeric=False)
        self.play(FadeIn(watch),FadeOut(tip),run_time=.70)
        self.finish()


class S07NoticeAndSwap(SpokenScene):
    def construct(self):
        self.add(tabletop(),bowl())
        bags = dipped()
        t = ValueTracker(0)
        watch = clock(t,-4.74,1.32,.82,numeric=False)
        wet = water_in_front()
        self.add(bags,watch,wet)
        self.at("hand feels cold",lead=.61)
        cold = boxed_label("Cold!",color=BLUE,size=35).move_to(p(2.57,2.44))
        shiver = VGroup(bags[1],bags[3])
        self.play(FadeIn(cold), t.animate.set_value(2),run_time=.58)
        self.play(Wiggle(shiver,scale_value=1.025,rotation_angle=.047,n_wiggles=5),
                  t.animate.set_value(5),run_time=2.43,rate_func=linear)
        self.at("record the time",lead=.23)
        record = Ledger([("Plain", "Time first felt cold", BLUE), ("Lined", "Time first felt cold", PALE)],
                        top_left=(-.8,2.95),key_w=1.42,width=6.60,row_h=.56,size=28)
        self.play(FadeOut(cold),run_time=.24)
        self.play(record.reveal(0),t.animate.set_value(7),run_time=.93)
        self.play(record.reveal(1),t.animate.set_value(8),run_time=.82)
        self.at("stop at one minute",lead=.35)
        limit = heading("Stop by 1 minute",PALE,y=3.24)
        self.play(FadeOut(record.everything()),run_time=.3)
        self.play(FadeIn(limit),run_time=.43)
        self.play(bags.animate.shift(UP*1.34), FadeOut(watch),
                  FadeOut(wet,run_time=.5),run_time=1.50)
        self.at("the first sign",lead=.48)
        sooner = heading("Stop sooner for discomfort",PALE,y=3.24)
        self.play(swap(limit,sooner),run_time=.77)
        self.at("dry and gently warm",lead=.54)
        mittens = VGroup(bags[0], bags[1])
        hands = VGroup(bags[2], bags[3])
        cloth = towel(.50,1.07,1.36).set_z_index(12)
        self.play(FadeOut(sooner),mittens.animate.shift(DOWN*1.2),
                  hands.animate.shift(DOWN*.15),run_time=.55)
        self.play(FadeIn(cloth,shift=UP*.45),run_time=.32)
        self.play(cloth.animate.shift(LEFT*1.88+UP*.16),run_time=.64)
        self.play(cloth.animate.shift(RIGHT*3.74),run_time=.79)
        self.at("wait about five minutes",lead=.32)
        wait = heading("Wait until both hands feel normal",PALE,y=3.38)
        pause = ValueTracker(0)
        dial_face = clock(pause,-4.74,1.32,.82,duration=5,numeric=False)
        self.play(FadeOut(cloth),FadeIn(wait),FadeIn(dial_face),run_time=.64)
        self.play(pause.animate.set_value(4.99),run_time=3.0,rate_func=linear)
        self.at("then swap mittens",lead=.36)
        crossing = VGroup(CurvedArrow(p(-.65,1.49),p(1.59,1.49),angle=-.84,color=GOLD),
                          CurvedArrow(p(1.59,-.5),p(-.65,-.5),angle=-.84,color=GOLD))
        self.play(FadeOut(wait),FadeOut(dial_face),Create(crossing),run_time=.41)
        self.play(bags[0].animate(path_arc=-.60).shift(RIGHT*3.88+UP*.60),
                  bags[1].animate(path_arc=-.60).shift(LEFT*3.88+UP*.60),run_time=.93)
        self.play(FadeOut(crossing),mittens.animate.shift(DOWN*.74),hands.animate.shift(DOWN*1.19),
                  Succession(Wait(.48),FadeIn(wet,run_time=.42)),run_time=.90)
        self.finish()


class S08PredictQuestion(SpokenScene):
    def construct(self):
        table, basin = tabletop(), bowl()
        last = dipped(False)
        wet = water_in_front()
        self.add(table,basin,last,wet)
        self.at("after the test")
        sea, glove, palm = sea_question()
        self.play(FadeOut(table),FadeOut(basin),FadeOut(wet),FadeIn(sea),
                  ReplacementTransform(last[1],glove),ReplacementTransform(last[3],palm),
                  FadeOut(last[0]),FadeOut(last[2]),run_time=1.65)
        self.at("where did that warmth",lead=.43)
        source = question_card("Where did that warmth come from?",**QUESTION_STYLE)
        self.play(FadeIn(source),run_time=.56)
        self.at("shortening made heat",lead=.32)
        rim = glove[0][0].copy().set_fill(opacity=0).set_stroke(PALE,7)
        self.play(ShowPassingFlash(rim,time_width=.55),run_time=2.85)
        self.at("pause for a moment",lead=.33)
        self.play(FadeOut(source),run_time=.58)
        self.at("which way is heat",lead=.49)
        self.play(FadeIn(predict_text()),run_time=.57)
        self.finish()


class S09PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(*sea_question(moving=False),predict_text())
        self.wait(float(os.environ["KX_DURATION"]))


class S10RevealAndGuidingIdea(SpokenScene):
    def construct(self):
        sea, glove, palm = sea_question()
        question = predict_text()
        self.add(sea,glove,palm,question)
        self.at("heat always flows")
        self.play(FadeOut(question),run_time=.4)
        lined = VGroup(glove,palm)
        self.play(lined.animate.shift(LEFT*2.7),run_time=.65)
        plain = mitten(2.93,2.03,False,1.25)
        other = hand().scale(.92,about_point=ORIGIN).shift(p(2.93,.79)).set_z_index(8)
        self.play(FadeIn(plain),FadeIn(other),run_time=.63)
        flows = VGroup()
        for x, period in [(-2.9,3.3),(2.93,1.24)]:
            for side in (-1,1):
                for y in (-.73,.32):
                    arrow = heat_flow((x+side*.28,y),(x+side*2.62,y-.25),period,RIGHT*side).set_z_index(13)
                    arrow.update(.17 if y>0 else .56)
                    flows.add(arrow)
        self.add(flows)
        rule = heading("Heat moves from warm to cold",PALE)
        self.play(FadeIn(rule),run_time=.62)
        self.at("your child's hand made",lead=.38)
        warmth = heading("The hand supplies the heat",PALE)
        self.play(swap(rule,warmth),run_time=.71)
        self.at("the fat slowed",lead=.37)
        slower = heading("Fat slows heat loss",PALE)
        self.play(swap(warmth,slower),run_time=.67)
        self.at("a seal has a thick",lead=.61)
        animal = seal(cut=True)
        open_sea = ocean()
        self.play(FadeOut(slower),FadeOut(plain),FadeOut(other),FadeOut(sea),FadeOut(flows),
                  FadeIn(open_sea),ReplacementTransform(lined,animal),run_time=1.4)
        heat = VGroup(*[heat_flow((x,-.48),(x+.11,-2.34),2.9,DOWN).set_z_index(14)
                        for x in (-1.72,-.58,.61)])
        for index,a in enumerate(heat):
            a.update(.42+.64*index)
        self.add(heat)
        self.at("called blubber",lead=.44)
        self.play(FadeIn(heading("Blubber",PALE,size=44)),run_time=.51)
        self.finish()


class S11Safety(SpokenScene):
    def construct(self):
        self.add(tabletop())
        t = ValueTracker(1)
        watch = clock(t,0,.44,2.04,progress=True)
        self.at("stop for stinging")
        self.add(watch)
        stop = heading("Stop at any discomfort",RED)
        self.play(FadeIn(stop),run_time=.50)
        self.play(t.animate.set_value(60),run_time=2.7,rate_func=linear)
        self.at("unusual skin color", lead=0)
        self.play(Flash(watch[3],color=RED,line_length=.20,flash_radius=.30),run_time=.55)
        self.at("never leave a child",lead=.48)
        basin = bowl(cx=0,cy=-.69,moving=False)
        near = heading("Stay with your child",PALE)
        self.play(FadeOut(watch),run_time=.40)
        self.play(FadeIn(basin,shift=UP*.4),swap(stop,near,.76),run_time=.76)
        self.at("empty it right afterward",lead=.57)
        self.remove(basin)
        shadow = basin[0]
        basin_body = basin[1:4]
        water, cubes = basin.water, basin.cubes
        shadow.set_z_index(-3)
        basin_body.set_z_index(-3)
        water.set_z_index(-2)
        cubes.set_z_index(-1)
        self.add(shadow, basin_body, water, cubes)
        pivot = p(0,-.69)
        self.play(Rotate(VGroup(basin_body, water, cubes),-.24,about_point=pivot),
                  FadeOut(near),run_time=.72)
        drop = VGroup(*[Line(p(4.18+i*.16,-1.9+i*.21),p(4.49+i*.15,-3.17+i*.09),
                             color=BLUE,stroke_width=10) for i in range(3)])
        self.play(Rotate(basin_body,-.22,about_point=pivot),
                  FadeOut(water,shift=DOWN*.22+RIGHT*.29),FadeOut(cubes,shift=DOWN*.22+RIGHT*.29),
                  ShowPassingFlash(drop,time_width=.74),run_time=.84)
        self.at("keep bags and ice",lead=.50)
        bag = plain_bag(-1.9,1.81,1.24)
        cube = ice(2.30,-.10,2.36)
        keep = boxed_label("Keep away from children under 4",color=PALE,size=34).move_to(p(0,3.14))
        self.play(FadeOut(VGroup(shadow, basin_body)),FadeIn(bag,shift=UP*.45),
                  FadeIn(cube,shift=UP*.45),FadeIn(keep),run_time=.73)
        bob(cube,amp=.115,speed=1.83)
        self.at("call 911 if choking",lead=.49)
        call = heading("Call 911 if choking",RED,size=43)
        self.play(swap(keep,call),run_time=.72)
        self.at("never use dry ice",lead=.52)
        cube.clear_updaters()
        stop_ring = Circle(radius=1.78,color=RED,stroke_width=8).move_to(p(0,-.17))
        slash = Line(stop_ring.get_center()+1.17*UL,stop_ring.get_center()+1.17*DR,color=RED,stroke_width=9)
        dry = heading("Never use dry ice",RED,size=42)
        block = RoundedRectangle(width=2.42,height=1.51,corner_radius=.14,fill_color=PLASTIC,
                                 fill_opacity=1,stroke_color=TEXT,stroke_width=3).move_to(p(0,-.17))
        self.play(FadeOut(bag),ReplacementTransform(cube,block),swap(call,dry),run_time=.76)
        self.play(Create(stop_ring),Create(slash),run_time=.73)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        self.at("if your child skips")
        sea, glove, _ = sea_question()
        self.add(sea,glove)
        pouch = bag_outline(1.72,2.02,edge=PALE,fill=WARM,rim=PALE).move_to(p(-.2,-.48)).set_z_index(7)
        self.play(FadeIn(pouch,shift=DOWN*.45),run_time=.85)
        probe = Line(p(1.45,1.88),p(.08,-1.00),color=TEXT,stroke_width=6)
        reader = RoundedRectangle(width=1.04,height=.65,corner_radius=.13,fill_color=PLASTIC,fill_opacity=1,
                                  stroke_width=0).rotate(.43).move_to(p(1.57,2.08))
        window = RoundedRectangle(width=.53,height=.26,corner_radius=.045,fill_color=DEEP,fill_opacity=1,
                                  stroke_width=0).rotate(.43).move_to(reader)
        thermometer = VGroup(probe,reader,window).set_z_index(12)
        self.at("guide's thermometer version",lead=.86)
        self.play(FadeIn(thermometer,shift=DOWN*.75),run_time=1.24)
        self.at("then look at a seal",lead=.52)
        animal, open_sea = seal(cut=True), ocean()
        self.play(FadeOut(thermometer),FadeOut(sea),FadeIn(open_sea),FadeOut(pouch),
                  ReplacementTransform(glove,animal),run_time=1.44)
        swim(animal)
        self.at("ask where its mitten is",lead=.34)
        prompt = heading("Where is its “mitten”?",size=41)
        self.play(FadeIn(prompt),run_time=.57)
        self.at("ask what they noticed",lead=.38)
        self.play(FadeOut(prompt),run_time=.52)
        pulse(animal.cutaway[0],base=5,amp=2.1,speed=2.3)
        self.finish()


class S13End(EndCard):
    LINE = "Blubber makes no heat. It slows warmth from leaving the body."
