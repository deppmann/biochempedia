"""Seeing Inside Without Cutting, paced to the supplied microCT narration.

Color map: BLUE apparatus and water-filled conduits, GREY structural outlines,
YELLOW X-rays and active marks, GREEN plant tissue, RED cut, GOLD study credits,
TEAL bath, PURPLE insect body, TEXT air spaces and readable neutral labels.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
NIGHT = "#25364C"
SCREEN = "#253F55"
PLANT = "#457F59"
AIR = TEXT
STEM_X = -1.05
WIN_X = 4.32
AFTER = (0, 2, 5)
QUESTION = "Already there, or made by the cut?"


def pos(x, y):
    return np.array([x, y, 0.0])


def shape(w, h, x, y, fill, edge=GREY, alpha=1, radius=0.14):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            stroke_color=edge, stroke_width=2, fill_color=fill,
                            fill_opacity=alpha).move_to(pos(x, y))


def oval(w, h, x, y, fill, edge=GREY, ink=2):
    return Ellipse(width=w, height=h, stroke_color=edge, stroke_width=ink,
                   fill_color=fill, fill_opacity=1).move_to(pos(x, y))


def label(words, x=WIN_X, y=2.61, color=TEXT):
    return T(words, 30, color).move_to(pos(x, y))


def credit(words):
    return caption(words, size=29, color=GOLD)


def scanner():
    """The source, specimen mount, and reconstruction screen never move."""
    source = VGroup(
        shape(1.85, 2.5, -5.45, 0.36, NIGHT, BLUE, radius=0.25),
        shape(0.93, 1.54, -4.52, 0.36, SCREEN, BLUE),
        oval(0.19, 0.95, -4.06, 0.36, YELLOW, YELLOW),
        *[Line(pos(-6.05, y), pos(-5.35, y), color=BLUE, stroke_width=3)
          for y in (0.85, 0.60, 0.35, 0.10, -0.15)],
    )
    holder = VGroup(shape(3.35, 0.4, STEM_X, -2.5, NIGHT, BLUE),
                    oval(3.38, 0.48, STEM_X, -2.30, SCREEN, BLUE))
    screen = shape(4.65, 5.75, WIN_X, 0.30, SCREEN, BLUE, radius=0.22)
    return VGroup(screen, holder, source)


def ray(alpha=0.3, active=False):
    beam = Polygon(pos(-4.04, 0.26), pos(1.96, -1.12),
                   pos(1.96, 1.84), pos(-4.04, 0.46),
                   stroke_color=YELLOW, stroke_width=1.6,
                   fill_color=YELLOW, fill_opacity=alpha)
    if active:
        def exposure(m, dt):
            m.phase += dt * 2.35
            m.set_fill(opacity=alpha + .19*np.sin(m.phase))
        beam.phase = 0
        beam.add_updater(exposure)
    return beam


def scanning_band(x=STEM_X, y=0.32, w=2.40, swing=1.38):
    """Sweep the detector's illuminated section across the specimen."""
    band = VGroup(Rectangle(width=w, height=0.46, stroke_width=0,
                            fill_color=YELLOW, fill_opacity=0.39),
                  Line(LEFT * w / 2, RIGHT * w / 2, color=YELLOW, stroke_width=2))
    return bob(band.move_to(pos(x, y)), amp=swing, speed=1.75)


def cylinder(x, bottom, top, width=2.38):
    body = Rectangle(width=width, height=top-bottom, stroke_color=GREEN,
                     stroke_width=0, fill_color=PLANT, fill_opacity=1)
    body.move_to(pos(x, (bottom+top)/2))
    rims = [Line(pos(x+dx,bottom), pos(x+dx,top), color=GREEN, stroke_width=2)
            for dx in (-width/2,width/2)]
    return VGroup(oval(width, 0.52, x, bottom, PLANT, GREEN), body,
                  *rims, oval(width, 0.52, x, top, GREEN, GREEN))


def stem(turn=False, cut=False, ribs=True, cut_edge=-.66):
    if cut:
        return VGroup(cylinder(STEM_X, -2.12, -1.12),
                      cylinder(STEM_X, cut_edge, 2.46))
    plant = cylinder(STEM_X, -2.12, 2.46)
    if not ribs:
        return plant
    ribs = VGroup(*[Line(UP*2.12, DOWN*2.12, color=GREEN, stroke_width=3)
                    .move_to(pos(STEM_X+dx, 0.13))
                    for dx in (-0.79, -0.4, 0.15, 0.65)])
    plant.add(ribs)
    if turn:
        def roll(m, dt):
            m.angle += dt * 0.84
            for i, rib in enumerate(m):
                angle = m.angle + i * 0.74 - 0.9
                rib.set_x(STEM_X + np.sin(angle) * 1.02)
                rib.set_stroke(opacity=0.25 + 0.70 * (1 + np.cos(angle))/2)
        ribs.angle = 0
        ribs.add_updater(roll)
    return plant


VESSELS = ((-.49, .51), (.22, .63), (.56, .08), (-.65, -.15),
           (-.17, .06), (.33, -.58), (-.34, -.64))


def stem_slice(empty=(), height=3.18):
    disc = oval(2, 1.94, 0, 0, PLANT, GREEN, ink=3)
    cells = VGroup(*[Circle(radius=0.185, color=TEXT if i in empty else BLUE,
                            fill_opacity=1, stroke_width=2).move_to(pos(x, y))
                     for i, (x, y) in enumerate(VESSELS)])
    g = VGroup(disc, cells).scale_to_fit_height(height)
    g.cells = cells
    return g


def projection(angle, x, y):
    """Orthographic view of the schematic vessel centers at one scan angle."""
    card = shape(1.24, 2.28, x, y, NIGHT, BLUE)
    profiles = VGroup()
    for vx, vy in VESSELS:
        offset = .64*(vx*np.cos(angle)+vy*np.sin(angle))
        profile = shape(.19, 1.85, x+offset, y, BLUE, BLUE, .36, radius=.08)
        profile.set_stroke(width=0)
        profiles.add(profile)
    return VGroup(card, profiles)


def reconstruction(air=True):
    """Oblique cutaway: matched vertical channels end on the same top section."""
    y_top, y_base = 1.59, -1.87
    x = WIN_X
    body = VGroup(oval(3.18, 0.77, x, y_base, PLANT, GREEN),
                  Rectangle(width=3.18, height=y_top-y_base, stroke_width=2,
                            stroke_color=GREEN, fill_color=PLANT, fill_opacity=1)
                  .move_to(pos(x, (y_top+y_base)/2)))
    tubes = VGroup(*[shape(.47, 2.95, x+dx, -0.10, BLUE, BLUE, radius=.13)
                     for dx in (-.98, -.32, .33, .98)])
    bubble = shape(.47, 1.05, x+.33, -0.04, AIR, AIR, radius=.18)
    lid = oval(3.18, 0.80, x, y_top, GREEN, GREEN)
    for dx, dy in ((-.98,.02),(-.32,.13),(.33,.13),(.98,.02)):
        lid = VGroup(lid, oval(.44, .16, x+dx, y_top+dy, BLUE, BLUE))
    return VGroup(body, tubes, lid, *([bubble] if air else [])), bubble


def bath():
    return VGroup(shape(3.70, 2.09, STEM_X, -1.50, TEAL, BLUE, .32),
                  Line(pos(-2.81, -.51), pos(.71, -.51), color=BLUE, stroke_width=3))


def blade():
    return Polygon(pos(-3.7,-.66), pos(-2.30,-.66), pos(-2.56,-1.02),
                   pos(-3.7,-1.02), fill_color=GREY, fill_opacity=1,
                   stroke_color=RED, stroke_width=3)


def pull():
    return VGroup(*[Arrow(pos(x, -1.14), pos(x, 1.60), buff=0, color=BLUE,
                          stroke_width=6, max_tip_length_to_length_ratio=.16)
                    for x in (STEM_X-.55, STEM_X, STEM_X+.55)])


def comparison(left, right, first=(), second=()):
    panels = TwoPanel(left, right, top=2.88, bottom=-2.21, gap=.15,
                      width=4.28, size=28, colors=(BLUE, TEXT)).shift(RIGHT * WIN_X)
    # TwoPanel's coordinates are local to its paired frames.
    a = stem_slice(first, 1.71).move_to(pos(WIN_X-1.1075, .27))
    b = stem_slice(second, 1.71).move_to(pos(WIN_X+1.1075, .27))
    return panels, a, b


def cut_world(active=False):
    panels, before, after = comparison("Before cut", "After cut", second=AFTER)
    return VGroup(scanner(), ray(.25, active=active), stem(cut=True), bath(), panels, before, after)


def question():
    return question_card(QUESTION, y=-3.07, size=34)


def beetle(x=STEM_X, y=-.03, scale=1, pupa=False, pump=None):
    outline = VGroup()
    if not pupa:
        for side in (-1, 1):
            for py, ey in ((.68, 1.29), (.24, .24), (-.22, -1.02)):
                outline.add(VMobject(stroke_color=GREY, stroke_width=5)
                            .set_points_as_corners([pos(side*.59, py), pos(side*1.38, ey+.28),
                                                    pos(side*1.60, ey)]))
            outline.add(ArcBetweenPoints(pos(.30*side, 1.64), pos(.86*side, 2.15),
                                         angle=-side*.65, color=GREY, stroke_width=4))
    shell = oval(2.04, 2.64, 0, -.60, "#563E73", PURPLE)
    abdomen = VGroup(shell)
    if pupa:
        for py in (-1.41, -1.02, -.61, -.21):
            abdomen.add(ArcBetweenPoints(pos(-.75, py), pos(.75, py), angle=.42,
                                         color=PURPLE, stroke_width=2))
    else:
        abdomen.add(Line(pos(0,.41),pos(0,-1.83),color=PURPLE,stroke_width=2))
    outline.add(abdomen, oval(1.64, 1.21, 0, .84, "#674A88", PURPLE),
                oval(1.09, .78, 0, 1.54, "#674A88", PURPLE))
    outline.scale(scale).move_to(pos(x, y))
    if pupa:
        outline.shift(DOWN*.19)
    if pump is not None:
        base = abdomen.copy()
        abdomen.add_updater(lambda m: m.become(base.copy().stretch(1-.26*pump(), 0)))
    return outline


def tracheae(x=WIN_X, y=.24, scale=1, contraction=None):
    branches = []
    for side in (-1, 1):
        branches.append([pos(side*.46,-1.88), pos(side*.73,-.83),
                         pos(side*.65,.09), pos(side*.49,1.03), pos(side*.26,1.68)])
        for by, ex, ey in ((-1.04, 1.38, -1.49),(-.44, 1.56, -.62),
                           (.27, 1.53, .51),(.91, 1.15, 1.37)):
            branches.append([pos(side*.58, by), pos(side*(ex-.25), ey-.18), pos(side*ex, ey)])
    lines = VGroup(*[VMobject(stroke_color=AIR, stroke_width=(16 if i%5==0 else 8)*scale)
                     .set_points_smoothly(points) for i, points in enumerate(branches)])
    lines.scale(scale).move_to(pos(x,y))
    if contraction is not None:
        widths = [m.get_stroke_width() for m in lines]
        for line, w in zip(lines, widths):
            line.add_updater(lambda m, w=w: m.set_stroke(width=w*(1-.69*contraction())))
    return lines


def cycle(scene, period=2.55):
    start = scene.elapsed()
    return lambda: (1-np.cos(TAU*(scene.elapsed()-start)/period))/2


def clock_face(center):
    ring = Circle(radius=.48, color=BLUE, stroke_width=3).move_to(center)
    hand = Line(center, center+.34*UP, color=TEXT, stroke_width=4)
    hand.add_updater(lambda m, dt: m.rotate(-dt*2.1, about_point=center))
    return VGroup(ring, hand)


def bar_track(width, center, fraction, color=BLUE):
    full = shape(width, .47, *center[:2], NIGHT, GREY, radius=.09)
    fill = Rectangle(width=(width-.14)*fraction, height=.33, stroke_width=0,
                     fill_color=color, fill_opacity=1)
    fill.next_to(full.get_left()+RIGHT*.07, RIGHT, buff=0)
    return full, fill


def mesophyll():
    """A cutaway with connected dark air spaces between schematic cells."""
    block = shape(3.82, 3.18, WIN_X, .12, BG, GREEN, radius=.22)
    cells = VGroup()
    for row, widths in enumerate(((.78,.92,.77,.63),(.81,.66,.72),(.72,.68,.84,.79))):
        xs = ((-1.32,-.38,.58,1.40),(-1.05,.10,1.12),(-1.35,-.48,.50,1.37))[row]
        for i, (x,w) in enumerate(zip(xs,widths)):
            y = 1.08-row*.98+.11*((i+row)%2)
            cell = oval(w,.76 if row!=1 else .62,WIN_X+x,y,PLANT,GREEN)
            cell.rotate((i%3-1)*.35)
            cells.add(cell)
    return VGroup(block, cells), cells


def leaf_disc():
    leaf = VGroup(oval(3.13, .83, STEM_X,-.15, PLANT,GREEN),
                  oval(3.13, .83, STEM_X,.06, GREEN,GREEN))
    for dx in (-.93, -.50, 0, .49, .91):
        leaf.add(Line(pos(STEM_X+dx,-.12),pos(STEM_X+dx+.24,.23),
                      color=PLANT,stroke_width=3))
    rest = VGroup(shape(.24, 1.77, STEM_X, -1.24, NIGHT, BLUE, radius=.08),
                  oval(1.17, .22, STEM_X, -.36, NIGHT, BLUE))
    return VGroup(rest, leaf)


class S01Hook(SpokenScene):
    def construct(self):
        world, specimen = scanner(), stem(ribs=False)
        mark = VGroup(oval(1.22,1.30,STEM_X,.37,BG,GOLD,ink=3),
                      T("?", 94, GOLD).move_to(pos(STEM_X,.37)))
        self.add(world, ray(.24, active=True), specimen)
        self.at("how do you")
        self.play(FadeIn(mark), run_time=.6)
        self.at("living stem or")
        self.play(FadeIn(scanning_band(y=1.78, swing=.38)), run_time=.8)
        self.at("hidden tubes carry")
        self.play(FadeOut(mark), run_time=.35)
        preview, _ = reconstruction(air=False)
        self.play(FadeIn(preview), run_time=1.2)
        self.at("air in insects")
        insect = tracheae(y=.16, scale=.46)
        beetle_scan = VGroup(beetle(x=WIN_X, y=.24, scale=.95),
                            insect)
        self.play(FadeOut(preview), run_time=.35)
        self.play(FadeIn(beetle_scan), run_time=.65)
        self.at("cutting can change")
        self.play(FadeOut(beetle_scan), FadeIn(mark), run_time=.7)
        self.at("rays look inside")
        self.play(FadeOut(mark), FadeIn(reconstruction(air=False)[0]), run_time=1.3)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Seeing Inside Without Cutting"
    LESSON = "X-ray Microtomography and Synchrotron Imaging"

    def construct(self):
        world = VGroup(scanner(), ray(.25, active=True), stem()).set_opacity(.38)
        title = fit_text(self.TITLE, max_w=12.5, size=53, font=TITLE_FONT)
        title.move_to(pos(0,1.13))
        lesson = label(self.LESSON, 0, .24, TEXT)
        # A solid card gives the heading contrast over the carried stage.
        card = shape(12.7, 2.5, 0, .64, BG, BLUE, radius=.24)
        self.add(world, card, title)
        self.play(FadeIn(lesson), run_time=.48)
        self.wait(self.narration_s-self.elapsed())


class S03Microct(SpokenScene):
    def construct(self):
        self.add(scanner(), ray(active=True), stem(turn=True), scanning_band())
        self.at("micro ct")
        method = label("MicroCT")
        self.play(FadeIn(method), run_time=.46)
        self.at("imaged from many angles")
        views = VGroup(*[projection(angle, WIN_X+dx, y)
                         for angle, dx, y in ((0,-1.39,-.46),(PI/3,0,.08),(2*PI/3,1.39,.62))])
        self.play(LaggedStart(*[FadeIn(v, shift=RIGHT*.27) for v in views],
                              lag_ratio=.62), run_time=2.15)
        self.at("the images combine")
        volume, bubble = reconstruction(air=False)
        self.play(FadeOut(views, shift=UP*.45), run_time=.85)
        self.play(FadeIn(volume, shift=UP*.35), run_time=1.4)
        self.at("air filled and")
        self.play(GrowFromCenter(bubble), run_time=.65)
        key = label("Blue = water   ·   Pale = air", 3.98, -3.10)
        self.play(FadeIn(key), run_time=.5)
        self.at("you can spot")
        highlight = SurroundingRectangle(bubble, buff=.12, color=GOLD,
                                         stroke_width=4, corner_radius=.17)
        self.play(Create(highlight), run_time=.52)
        self.play(swap(key, label("Embolism", WIN_X, -3.10, GOLD)), run_time=.76)
        self.finish()


class S04Synchrotron(SpokenScene):
    def construct(self):
        specimen = stem(turn=True)
        volume, _ = reconstruction()
        self.add(scanner(), ray(), specimen, scanning_band(), volume)
        self.at("inside is moving")
        self.play(FadeOut(volume), run_time=.85)
        self.at("a synchrotron")
        beam = ray(.46, active=True)
        self.bring_to_back(beam)
        self.play(FadeIn(beam), run_time=1.18)
        self.at("very bright")
        self.play(FadeIn(label("Synchrotron beam", -4.52, -1.53, YELLOW)),
                  run_time=.72)
        self.at("film small")
        insect = beetle()
        self.play(ReplacementTransform(specimen, insect), run_time=1.45)
        self.at("it films an")
        scan = tracheae(contraction=cycle(self))
        self.play(FadeIn(scan), run_time=.65)
        self.at("called trachea")
        self.play(FadeIn(label("Tracheae")), run_time=.5)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        specimen, band = stem(turn=True), scanning_band()
        self.add(scanner(), ray(.25, active=True), specimen, band)
        panels, before, after = comparison("Before cut", "After cut", second=AFTER)
        self.at("an intact stem")
        self.play(FadeIn(VGroup(panels.left_frame, panels.left_head, before)),
                  run_time=1.15)
        self.at("that water is pulled")
        arrows = pull()
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.25),
                  run_time=1.7)
        self.at("drought raises")
        self.play(arrows.animate.stretch(1.38, 1), run_time=1.12)
        tension = label("Tension", -4.35, 2.35, BLUE)
        self.play(FadeIn(tension), run_time=.48)
        self.at("cut the stem")
        water, knife = bath(), blade()
        self.play(FadeIn(water), FadeOut(band), run_time=.55)
        self.play(knife.animate.shift(RIGHT*2.56), run_time=.83)
        separated = stem(cut=True, cut_edge=-1.12)
        self.replace(specimen, separated)
        self.play(Transform(separated[1], stem(cut=True)[1]),
                  FadeOut(arrows), FadeOut(tension), run_time=.58)
        self.play(FadeOut(knife), run_time=.33)
        self.at("scan again")
        self.play(FadeIn(VGroup(panels.right_frame, panels.right_head)),
                  run_time=.83)
        self.at("several conduits now")
        self.play(FadeIn(after), run_time=1.12)
        self.at("already there")
        self.play(FadeIn(question()), run_time=.65)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5

    def backdrop(self):
        return cut_world()

    def construct(self):
        picture = self.backdrop()
        self.add(picture, question())
        cells = picture[-1].cells
        halos = VGroup(*[Circle(radius=cells[i].width/2+.063, color=GOLD,
                                stroke_width=3).move_to(cells[i]) for i in AFTER])
        self.play(FadeIn(halos), run_time=.75)
        self.wait(self.SECONDS-1.5)
        self.play(FadeOut(halos), run_time=.75)


class S07Control(SpokenScene):
    def construct(self):
        world = cut_world(active=True)
        self.add(world)
        self.at("empty after")
        cells = world[-1].cells
        marks = VGroup(*[Circle(radius=cells[i].width/2+.062, color=GOLD,
                                 stroke_width=3).move_to(cells[i]) for i in AFTER])
        self.play(Create(marks), run_time=.55)
        cause = caption("Emptied by cut", size=32, color=GOLD)
        self.play(FadeIn(cause), run_time=.5)
        self.at("did tension cause")
        probe = caption("Did tension cause it?", size=32, color=GOLD)
        self.play(swap(cause, probe), FadeOut(marks), run_time=.75)
        self.at("rehydrate the plant")
        self.play(FadeOut(probe), FadeOut(VGroup(*world[4:])), run_time=.7)
        water = world[3][0]
        self.play(water.animate.set_fill(TEAL,.56), run_time=.7)
        level = ValueTracker(.13)
        gauge = dial(level, pos(WIN_X, .33), radius=1.48, label="Water potential",
                     color=BLUE, size=32)
        gauge.remove(gauge[3])
        self.play(FadeIn(gauge), run_time=.49)
        self.at("water potential")
        self.play(level.animate.set_value(.77), run_time=4.46, rate_func=smooth)
        self.at("aim for about")
        target = label("−0.2 to −0.4 MPa", WIN_X, -1.48)
        self.play(level.animate(run_time=1.2).set_value(.9), FadeIn(target, run_time=.5))
        check = stem_slice(AFTER, 3.25).move_to(pos(WIN_X,.2))
        self.at("rescan to check")
        self.add(scanning_band())
        self.play(FadeOut(gauge), FadeOut(target), run_time=.52)
        self.play(FadeIn(check), run_time=.69)
        verified = label("Nothing refilled")
        self.play(FadeIn(verified), run_time=.54)
        self.at("compare matched cuts")
        panels, low, high = comparison("Low tension", "High tension")
        test = label("If", WIN_X, -3.10, GOLD)
        self.play(FadeOut(check), FadeOut(verified), run_time=.4)
        self.play(FadeIn(VGroup(panels, low, high, test)), run_time=1.09)
        self.at("few new embolisms")
        self.play(low.cells[0].animate.set_fill(AIR).set_stroke(AIR), run_time=.95)
        self.at("many at high")
        self.play(LaggedStart(*[high.cells[i].animate.set_fill(AIR).set_stroke(AIR)
                                for i in (0, 1, 2, 4, 5)], lag_ratio=.27), run_time=1.45)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        specimen = stem(cut=True)
        tank = bath()
        band = scanning_band()
        self.add(scanner(), ray(active=True), specimen, tank, band)
        panels, before, after = comparison("Before cut", "After cut", second=AFTER)
        self.at("cuts can create")
        cuts = VGroup(panels, before, after)
        self.play(FadeIn(cuts), run_time=.85)
        self.at("intact stems never")
        intact = stem(turn=True)
        self.play(FadeOut(cuts), FadeOut(tank), FadeOut(specimen), run_time=.58)
        self.play(FadeIn(intact), run_time=.65)
        self.at("needs repeated scans")
        divider = Line(pos(2.26,.64),pos(6.38,.64),color=BLUE,stroke_width=2)
        test = label("Test refilling uncut", WIN_X,2.62)
        sample = stem_slice(empty=AFTER, height=1.38).move_to(pos(3.45,1.60))
        clock = clock_face(pos(5.42,1.63))
        inset_scan = scanning_band(x=3.45, y=1.59, w=1.28, swing=.43)
        self.play(FadeIn(VGroup(divider, sample, clock, inset_scan)), run_time=.7)
        self.play(FadeIn(test), run_time=.5)
        self.at("insects x rays")
        clock[1].clear_updaters()
        self.play(FadeOut(VGroup(sample, clock, test, divider, inset_scan, band)), run_time=.32)
        insect = beetle(pupa=True, pump=cycle(self))
        self.play(ReplacementTransform(intact, insect), run_time=.94)
        scan = tracheae(y=.30, scale=.55, contraction=cycle(self))
        self.play(FadeIn(scan), run_time=.76)
        self.at("not how much air")
        airflow = caption("Airflow remains unmeasured", size=31)
        self.play(FadeIn(airflow), run_time=.52)
        self.at("in 2015")
        study = credit("Pendar, Kenny and Socha, 2015").shift(RIGHT*.30)
        self.play(swap(airflow, study), run_time=.75)
        self.at("beetle pupae")
        # The pressure trace is explicitly schematic and shares the pump's period.
        axes = Plot((-6.06,-3.35,-2.0,-1.03), (0,5.1), (0,1.08), size=28)
        time = ValueTracker(0)
        pressure = lambda t: .09+.86*((1-np.cos(TAU*t/2.55))/2)**3
        trace = axes.live_curve(pressure, time, color=YELLOW, width=4)
        title = label("Fluid pressure", -4.70, -2.39, YELLOW)
        schematic = label("Schematic", -4.86, -2.90)
        self.play(FadeIn(axes), FadeIn(title), FadeIn(schematic), run_time=.45)
        self.add(trace)
        self.at("recording abdominal pumps")
        start = self.elapsed()
        pumping = cycle(self)
        fresh = beetle(pupa=True, pump=pumping)
        synchronous = tracheae(y=.30, scale=.55, contraction=pumping)
        self.remove(insect, scan)
        self.add(fresh, synchronous)
        time.add_updater(lambda m: m.set_value((self.elapsed()-start)%5.1))
        self.add(time)
        self.at("every tracheal collapse")
        paired = label("Collapse with pump", WIN_X,-2.14)
        self.play(FadeIn(paired), run_time=.62)
        self.at("yet in their recordings")
        still = tracheae(y=.30, scale=.55)
        self.remove(synchronous)
        self.add(still)
        self.play(FadeOut(paired), still.animate.set_y(-.58), run_time=.78)
        self.at("63 .7")
        track, fraction = bar_track(3.72,pos(WIN_X,1.53),.637, GOLD)
        stat = label("63.7% of pumps", WIN_X,2.44,GOLD)
        note = label("No compression", WIN_X,.96)
        self.play(FadeIn(track), FadeIn(stat), GrowFromEdge(fraction, LEFT), run_time=.8)
        self.at("no compression")
        self.play(FadeIn(note), run_time=.51)
        self.finish()


class S09Unlocked1(SpokenScene):
    def construct(self):
        body = beetle()
        branches = tracheae(contraction=cycle(self))
        band = scanning_band(w=3.05, swing=1.22)
        self.add(scanner(), ray(.45, active=True), body, band)
        self.at("imaging unlocked")
        self.play(FadeIn(branches), run_time=1.32)
        self.at("in 2003")
        study = credit("Westneat et al., 2003")
        self.play(FadeIn(study), run_time=.63)
        self.at("synchrotron x rays")
        scan_label = label("Tracheae")
        self.play(FadeIn(scan_label), run_time=.64)
        self.at("their trachea compressed")
        self.at("in 2015")
        intact = stem(turn=True)
        self.play(FadeOut(branches), FadeOut(scan_label), FadeOut(band),
                  ReplacementTransform(body,intact),
                  swap(study,credit("Torres-Ruiz et al., 2015")), run_time=1.35)
        self.at("scanned stems at")
        panels, before, after = comparison("Before cut", "After cut", second=AFTER)
        self.play(FadeIn(VGroup(panels.left_frame,panels.left_head,before)), run_time=.92)
        arrows = pull()
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.2),run_time=.92)
        self.at("cutting underwater")
        tank, knife = bath(), blade()
        self.play(FadeIn(tank),run_time=.48)
        self.play(knife.animate.shift(RIGHT*2.56),run_time=.9)
        separated = stem(cut=True, cut_edge=-1.12)
        self.replace(intact, separated)
        self.play(Transform(separated[1], stem(cut=True)[1]),
                  FadeOut(arrows), run_time=.48)
        self.play(FadeOut(knife), FadeIn(VGroup(panels.right_frame, panels.right_head)),
                  run_time=.5)
        self.at("created embolisms")
        self.play(FadeIn(after), run_time=1.15)
        self.finish()


class S10Unlocked2(SpokenScene):
    def construct(self):
        specimen = leaf_disc()
        world = scanner()
        beam = ray(active=True)
        self.add(world, beam, specimen)
        self.at("in 2018")
        study = credit("Mathers et al., 2018")
        self.play(FadeIn(study),run_time=.65)
        self.at("scanned leaf disks")
        band = scanning_band(y=.02,w=3.1,swing=.29)
        self.play(FadeIn(band),run_time=.58)
        tissue, cells = mesophyll()
        self.play(FadeIn(tissue,shift=UP*.28),run_time=1.45)
        self.at("surface of mesophyll")
        self.play(LaggedStart(*[c.animate.set_stroke(GREEN, width=6) for c in cells],
                              lag_ratio=.14),run_time=2.26)
        meso = label("Mesophyll surface",WIN_X,2.57,GREEN)
        self.play(FadeIn(meso),run_time=.55)
        self.at("internal airspaces")
        spaces = label("Internal air spaces",WIN_X,-2.12)
        self.play(FadeIn(spaces),run_time=.54)
        self.at("divide that surface")
        numerator = label("Mesophyll surface",WIN_X,1.69,GREEN)
        rule = Line(pos(2.78,1.27),pos(5.86,1.27),color=TEXT,stroke_width=2)
        denom = label("Leaf area",WIN_X,.85)
        units = label("mm² / mm²",WIN_X,-.37)
        self.play(FadeOut(tissue), FadeOut(meso), FadeOut(spaces), run_time=.25)
        self.play(FadeIn(numerator), Create(rule), FadeIn(denom), FadeIn(units), run_time=.35)
        self.at("the units cancel")
        unitless = label("No units",WIN_X,-.37)
        self.play(swap(units,unitless),run_time=.75)
        self.at("barley gave")
        ratio = label("Surface ÷ leaf area",WIN_X,2.59)
        self.play(FadeOut(VGroup(numerator, rule, denom, unitless)), FadeIn(ratio), run_time=.35)
        max_ratio = 24
        barley, rice = 21.3, 15.5
        results = VGroup(ratio)
        for name,value,y,phrase,times in (
            ("Barley",barley,1.18,None,"About 21 times"),
            ("Rice",rice,-.76,"rice gave","About 15 times"),
        ):
            if phrase:
                self.at(phrase)
            track,fill = bar_track(3.67,pos(WIN_X,y),value/max_ratio,GREEN)
            row = label(f"{name}   {value:.1f}",WIN_X,y+.59)
            self.play(FadeIn(track), FadeIn(row), GrowFromEdge(fill, LEFT), run_time=.7)
            self.at("about 21 times" if name=="Barley" else "about 15 times")
            multiple = label(times,WIN_X,y-.50,GREEN)
            self.play(FadeIn(multiple),run_time=.58)
            results.add(track, row, fill, multiple)
        self.at("each time x rays")
        self.play(FadeOut(study), FadeOut(results), run_time=.52)
        self.play(FadeIn(tissue), run_time=.78)
        band.clear_updaters()
        self.play(VGroup(world, beam, specimen, band, tissue).animate.scale(.91, about_point=ORIGIN),
                  run_time=2.7)
        self.finish()


class S11End(EndCard):
    LINE = "X-ray scans see hidden air and water without slicing specimens open."
