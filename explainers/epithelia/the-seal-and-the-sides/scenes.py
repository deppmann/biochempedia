"""The Seal and the Sides -- chapter two in one continuous epithelial world.

COLOR MAP (fixed across both chapters)
  GOLD       glucose
  BLUE       sodium / ions
  RED        sodium pumps
  GREEN      tight-junction seal
  TEXT       apical membrane
  SLATE      basolateral membrane / cell structure
  ORANGE     adherens junction
  PURPLE     desmosome
  CYAN       gap junction / water
  RED_BROWN  hemidesmosome
"""
from bp_style import *  # noqa: F401,F403


GOLD_GLUCOSE = GOLD
SLATE = "#667080"
CELL_FILL = "#C8CED8"
ORANGE = "#E89B4B"
PURPLE = "#A77BE8"
CYAN = "#55D6CF"
MAGENTA = "#E06AA8"
RED_BROWN = "#B86B52"
TAN = "#C9A66B"
CELL_X = (-4.45, -1.45, 1.55)
CELL_W = 2.78
TOP, BASE = 1.75, -1.80
GAPS = (-2.95, 0.05)
GUT_Y, BLOOD_Y = 2.75, -2.75


def glucose(x, y, r=0.105):
    return Dot([x, y, 0], radius=r, color=GOLD_GLUCOSE)


def sodium(x, y, r=0.09):
    return Dot([x, y, 0], radius=r, color=BLUE)


def cell_shape(cx, height=TOP - BASE):
    return Rectangle(width=CELL_W, height=height, stroke_color=SLATE, stroke_width=4,
                     fill_color=CELL_FILL, fill_opacity=0.20).move_to([cx, (TOP + BASE) / 2, 0])


def membranes(cx):
    top = Line([cx - CELL_W / 2, TOP, 0], [cx + CELL_W / 2, TOP, 0], color=TEXT, stroke_width=8)
    side = VMobject(color=SLATE, stroke_width=8).set_points_as_corners([
        [cx - CELL_W / 2, TOP - .05, 0], [cx - CELL_W / 2, BASE, 0],
        [cx + CELL_W / 2, BASE, 0], [cx + CELL_W / 2, TOP - .05, 0]])
    return top, side


def seal(x, narrow=False):
    width = .11 if narrow else .22
    return RoundedRectangle(width=width, height=.62, corner_radius=.04, stroke_width=0,
                            fill_color=GREEN, fill_opacity=1).move_to([x, 1.27, 0])


def turnstile(cx, y=TOP):
    ring = Circle(radius=.30, color=BLUE, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([cx, y, 0])
    bars = VGroup(Line(LEFT*.25, RIGHT*.25), Line(DOWN*.25, UP*.25)).set_stroke(BLUE, 5).move_to(ring)
    return VGroup(ring, bars)


def exit_door(cx, y=BASE):
    jamb = VGroup(Line([cx-.28, y, 0], [cx-.28, y+.52, 0]),
                  Line([cx+.28, y, 0], [cx+.28, y+.52, 0])).set_stroke(GOLD_GLUCOSE, 5)
    door = Line([cx-.26, y+.02, 0], [cx+.16, y+.42, 0], color=GOLD_GLUCOSE, stroke_width=5)
    return VGroup(jamb, door)


def pump(cx, y=BASE):
    body = RoundedRectangle(width=.66, height=.48, corner_radius=.12, color=RED, stroke_width=4,
                            fill_color=RED, fill_opacity=.22).move_to([cx, y, 0])
    arrow = VGroup(Line([-.14, -.10, 0], [.08, 0, 0]), Line([.08, 0, 0], [-.14, .10, 0]))
    arrow.set_stroke(RED, 5).move_to(body)
    return VGroup(body, arrow)


def schematic_tag():
    return T("schematic", 28, TEXT).move_to([5.55, -3.35, 0])


def add_wrap_motion(group, dx=.6, lo=-5.0, hi=3.7):
    def drift(mob, dt):
        for d in mob:
            d.shift(RIGHT * dx * dt)
            if d.get_x() > hi:
                d.shift(LEFT * (hi - lo))
    group.add_updater(drift)
    return group


def gut_world(proteins=True, particles=True, junction_stack=False):
    gut = Rectangle(width=12.2, height=1.15, stroke_width=0, fill_color=BLUE,
                    fill_opacity=.10).move_to([0, GUT_Y, 0])
    blood = Rectangle(width=12.2, height=1.15, stroke_width=0, fill_color=BLUE,
                      fill_opacity=.14).move_to([0, BLOOD_Y, 0])
    cells = VGroup(*[cell_shape(x) for x in CELL_X])
    mems = VGroup(*[m for x in CELL_X for m in membranes(x)])
    seals = VGroup(*[seal(x) for x in GAPS])
    labels = VGroup(T("gut", 30, TEXT).move_to([-5.75, GUT_Y, 0]),
                    T("blood", 30, TEXT).move_to([-5.55, BLOOD_Y, 0]))
    flow = VGroup(*[Dot([x, BLOOD_Y + .14*((i % 5)-2), 0], radius=.065, color=TEXT).set_opacity(.48)
                    for i, x in enumerate(np.linspace(-4.9, 3.55, 40))])
    add_wrap_motion(flow, .85)
    dots = VGroup()
    if particles:
        dots.add(*[glucose(x, GUT_Y + .22*((i % 3)-1)) for i, x in enumerate(np.linspace(-4.8, 3.5, 11))])
        add_wrap_motion(dots, .18)
    pro = VGroup()
    if proteins:
        for x in CELL_X:
            pro.add(VGroup(turnstile(x-.28), exit_door(x+.30), pump(x-.48)))
    stack = VGroup()
    if junction_stack:
        stack = junction_marks(GAPS[1])
    return VGroup(gut, blood, cells, mems, seals, labels, flow, dots, pro, stack, schematic_tag())


def move_glucose(scene, x, run_time=1.4):
    d = glucose(x, GUT_Y)
    scene.add(d)
    path = VMobject().set_points_as_corners([[x, GUT_Y, 0], [x, TOP+.2, 0], [x, .2, 0],
                                             [x+.25, BASE-.15, 0], [x+.65, BLOOD_Y, 0]])
    scene.play(MoveAlongPath(d, path), run_time=run_time, rate_func=linear)
    return d


def gate_icon(x=0, y=0, width=3.4, openings=.28):
    bars = VGroup()
    left, right = x-width/2, x+width/2
    for xx in np.arange(left, right+.01, openings+.22):
        bars.add(RoundedRectangle(width=.22, height=1.05, corner_radius=.05, stroke_width=0,
                                  fill_color=GREEN, fill_opacity=1).move_to([xx, y, 0]))
    return bars


def water_drop(x, y):
    return VGroup(Dot([x, y-.06, 0], radius=.10, color=CYAN),
                  Triangle(fill_color=CYAN, fill_opacity=1, stroke_width=0).scale(.12).move_to([x, y+.08, 0]))


def meter(label="resistance", low=False):
    box = RoundedRectangle(width=2.35, height=2.45, corner_radius=.18, color=TEXT, stroke_width=4,
                           fill_color=BG, fill_opacity=.9).move_to([4.75, .10, 0])
    arc = Arc(radius=.72, start_angle=PI, angle=-PI, color=GREY, stroke_width=5).move_to([4.75, .35, 0])
    angle = .25 if low else 2.35
    needle = Line([4.75, .35, 0], [4.75+.62*np.cos(angle), .35+.62*np.sin(angle), 0],
                  color=GOLD, stroke_width=7)
    lab = T(label, 28, TEXT).move_to([4.75, -.72, 0])
    return VGroup(box, arc, needle, lab)


def lab_insert(low=False, meter_label="resistance"):
    top_ch = Rectangle(width=8.7, height=2.0, stroke_color=BLUE, stroke_width=3,
                       fill_color=BLUE, fill_opacity=.11).move_to([-.8, 2.15, 0])
    bot_ch = top_ch.copy().move_to([-.8, -2.25, 0])
    cells = VGroup(*[Rectangle(width=2.35, height=1.65, stroke_color=SLATE, stroke_width=4,
                              fill_color=CELL_FILL, fill_opacity=.21).move_to([x, .25, 0])
                     for x in (-3.15, -.65, 1.85)])
    tops = VGroup(*[Line([x-1.17, 1.07, 0], [x+1.17, 1.07, 0], color=TEXT, stroke_width=7)
                    for x in (-3.15, -.65, 1.85)])
    seals = VGroup(seal(-1.90).move_to([-1.90, .80, 0]), seal(.60).move_to([.60, .80, 0]))
    filt = RoundedRectangle(width=7.55, height=.45, corner_radius=.08, color=TAN, stroke_width=3,
                            fill_color=TAN, fill_opacity=.28).move_to([-.65, -.82, 0])
    pores = VGroup(*[Circle(radius=.07, color=BG, fill_color=BG, fill_opacity=1).move_to([x, -.82, 0])
                     for x in np.linspace(-4.0, 2.7, 12)])
    ions = VGroup(*[sodium(-4.0+.58*i, 2.0+.22*((i%3)-1), .075) for i in range(12)])
    def bob(mob, dt):
        for i, d in enumerate(mob):
            d.shift(DOWN * (.30 + .04*(i%3)) * dt)
            if d.get_y() < -2.8:
                d.move_to([d.get_x(), 2.7, 0])
    ions.add_updater(bob)
    return VGroup(top_ch, bot_ch, cells, tops, seals, filt, pores, ions, meter(meter_label, low), schematic_tag())


def electrode(x, y, flip=False):
    stem = Line([x, y + (.95 if not flip else -.95), 0], [x, y, 0], color=TEXT, stroke_width=8)
    plate = RoundedRectangle(width=.70, height=.22, corner_radius=.06, color=GOLD, stroke_width=4,
                             fill_color=GOLD, fill_opacity=.25).move_to([x, y, 0])
    return VGroup(stem, plate)


def junction_marks(x=0):
    adherens = RoundedRectangle(width=.34, height=.28, corner_radius=.06, color=ORANGE, stroke_width=0,
                                fill_color=ORANGE, fill_opacity=1).move_to([x, .62, 0])
    desmo = Circle(radius=.20, color=PURPLE, fill_color=PURPLE, fill_opacity=1).move_to([x, -.18, 0])
    gap = RoundedRectangle(width=.42, height=.18, corner_radius=.07, color=CYAN, stroke_width=0,
                           fill_color=CYAN, fill_opacity=1).move_to([x, -.92, 0])
    anchors = VGroup(*[Triangle(color=RED_BROWN, fill_color=RED_BROWN, fill_opacity=1).scale(.16).rotate(PI)
                       .move_to([x+d, BASE+.05, 0]) for d in (-.22, .22)])
    return VGroup(adherens, desmo, gap, anchors)


def two_cell_closeup():
    left = Rectangle(width=5.2, height=5.8, stroke_color=SLATE, stroke_width=5,
                     fill_color=CELL_FILL, fill_opacity=.20).move_to([-2.7, -.15, 0])
    right = left.copy().move_to([2.7, -.15, 0])
    tops = VGroup(Line([-5.3, 2.75, 0], [-.1, 2.75, 0], color=TEXT, stroke_width=10),
                  Line([.1, 2.75, 0], [5.3, 2.75, 0], color=TEXT, stroke_width=10))
    s = RoundedRectangle(width=.30, height=1.05, corner_radius=.06, stroke_width=0,
                         fill_color=GREEN, fill_opacity=1).move_to([0, 2.18, 0])
    return VGroup(left, right, tops, s, schematic_tag())


class S00LinkAndQuestion(SpokenScene, TitleCard):
    LESSON = "Epithelia and tissue organization"
    TITLE = "The Seal and the Sides"

    def construct(self):
        w = gut_world(True, True)
        self.add(w)
        q = T("What makes a selective sheet?", 42, TEXT, weight=BOLD).move_to([0, 3.30, 0])
        panel = RoundedRectangle(width=q.width+.5, height=q.height+.20, corner_radius=.1,
                                 stroke_width=0, fill_color=BG, fill_opacity=.92).move_to(q)
        focus = VGroup(w[2][1], w[2][2], w[3][2], w[3][3], w[4][1])
        self.play(focus.animate.scale(1.10, about_point=[GAPS[1], 1.15, 0]),
                  Indicate(w[4][1], color=GREEN, scale_factor=1.45), run_time=1.15)
        self.at("what keeps each")
        self.play(Indicate(w[3][2], color=TEXT), Indicate(w[3][3], color=SLATE),
                  FadeIn(panel), FadeIn(q, shift=DOWN*.1), run_time=1.1)
        self.at("in chapter 1")
        self.play(focus.animate.scale(1/1.10, about_point=[GAPS[1], 1.15, 0]), run_time=.8)
        self.at("carrier placement")
        for p in w[8]:
            self.play(Indicate(p[0], color=BLUE), Indicate(p[1], color=GOLD),
                      Indicate(p[2], color=RED), run_time=.38)
        self.at("glucose toward blood")
        move_glucose(self, CELL_X[1], 1.15)
        self.at("seal decided")
        self.play(LaggedStart(*[Indicate(s, color=GREEN, scale_factor=1.45) for s in w[4]], lag_ratio=.2), run_time=.8)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Epithelia and tissue organization"
    TITLE = "The Seal and the Sides"

    def construct(self):
        w = gut_world(True, True)
        self.add(w)
        title = T(self.TITLE, 50, TEXT, font=TITLE_FONT).move_to([0, 3.22, 0])
        panel = RoundedRectangle(width=title.width+.65, height=title.height+.25, corner_radius=.12,
                                 stroke_width=0, fill_color=BG, fill_opacity=.93).move_to(title)
        self.play(FadeIn(panel), FadeIn(title, shift=UP*.12), run_time=.55)
        self.play(Indicate(w[4], color=GREEN), w[7].animate.shift(RIGHT*.35), run_time=.9)
        self.finish()


class S02TightJunction(SpokenScene):
    def construct(self):
        pair = two_cell_closeup()
        self.play(FadeIn(pair[0]), FadeIn(pair[1]), FadeIn(pair[2]), run_time=.8)
        self.at("tight junction")
        belt_back = Ellipse(width=1.8, height=.75, color=GREEN, stroke_width=8).move_to([0, 2.18, 0]).set_opacity(.45)
        self.play(Create(belt_back), FadeIn(pair[3]), run_time=.8)
        lab = T("tight junction", 34, GREEN).move_to([2.65, 2.12, 0])
        self.play(Rotate(VGroup(pair[0], pair[1], pair[2], pair[3], belt_back), angle=.12, axis=UP),
                  FadeIn(lab), run_time=1.25)
        self.at("not solid caulk")
        plug = RoundedRectangle(width=3.7, height=1.10, corner_radius=.10, stroke_width=0,
                                fill_color=GREEN, fill_opacity=1).move_to([0, -.65, 0])
        cross = VGroup(Line(LEFT*.35+UP*.35, RIGHT*.35+DOWN*.35),
                       Line(LEFT*.35+DOWN*.35, RIGHT*.35+UP*.35)).set_stroke(TEXT, 8).move_to(plug)
        self.play(FadeIn(plug), Create(cross), run_time=.75)
        self.at("selective gate")
        gate = gate_icon(0, -.65)
        ions = VGroup(*[sodium(-2.5+i*.35, -.65+.14*((i%2)*2-1)) for i in range(4)])
        big = glucose(-2.95, -.65, .22)
        bug = Ellipse(width=.90, height=.42, color=GREY, fill_color=GREY, fill_opacity=.45).move_to([-4.1, -.65, 0])
        self.play(FadeOut(cross), ReplacementTransform(plug, gate), FadeIn(ions), FadeIn(big), FadeIn(bug), run_time=.9)
        self.play(ions.animate.shift(RIGHT*5), big.animate.shift(RIGHT*.35), bug.animate.shift(RIGHT*.25),
                  run_time=1.25, rate_func=linear)
        self.play(big.animate.shift(LEFT*.35), bug.animate.shift(LEFT*.25), run_time=.45)
        self.add(pair[4])
        self.finish()


class S03ClaudinStrands(SpokenScene):
    def construct(self):
        tag = schematic_tag()
        strands = VGroup()
        ys = (1.65, .55, -.55, -1.65)
        for j, y in enumerate(ys):
            pts = [[-5.6, y, 0], [-3.2, y+.25*((j%2)*2-1), 0], [-.55, y, 0],
                   [1.0, y+.30*((j%2)*2-1), 0], [5.5, y, 0]]
            strands.add(VMobject(color=GREEN, stroke_width=10).set_points_as_corners(pts))
        self.play(LaggedStart(*[Create(s) for s in strands], lag_ratio=.16), run_time=1.35)
        self.at("around each cell")
        blocks = VGroup(*[chip("claudin", GREEN, 28).move_to([x, y, 0])
                          for x, y in [(-4.2,1.5),(-1.7,.75),(.5,-.45),(3.3,-1.5)]])
        # Opaque backs keep the strand from running through the readable label.
        for block in blocks:
            block[0].set_fill(BG, opacity=1)
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=.15), run_time=.8)
        self.play(strands.animate.shift(UP*.16), blocks.animate.shift(UP*.16), run_time=1.1)
        self.play(strands.animate.shift(DOWN*.16), blocks.animate.shift(DOWN*.16), run_time=1.1)
        self.at("narrow routes")
        opening = RoundedRectangle(width=.36, height=.82, corner_radius=.08, color=BG, stroke_width=0,
                                   fill_color=BG, fill_opacity=1).move_to([-.55, .55, 0])
        self.add(opening)
        ions = VGroup(*[sodium(-2.4-.35*i, .55) for i in range(3)])
        self.add(ions)
        self.play(ions.animate.shift(RIGHT*5.0), run_time=1.5, rate_func=linear)
        # Keep the large subject alive while the sentence about the route lands.
        drift_time = max(.4, self.t_of("strongly restricts") - .2 - self.elapsed())
        self.play(strands.animate.shift(UP*.12), blocks.animate.shift(UP*.12),
                  run_time=drift_time/2, rate_func=smooth)
        self.play(strands.animate.shift(DOWN*.12), blocks.animate.shift(DOWN*.12),
                  run_time=drift_time/2, rate_func=smooth)
        self.at("strongly restricts")
        disc = glucose(-3.9, -1.65, .24)
        bug = Ellipse(width=1.05, height=.48, color=GREY, fill_color=GREY, fill_opacity=.5).move_to([3.8, 1.65, 0])
        self.add(disc, bug)
        self.play(disc.animate.shift(RIGHT*1.15), bug.animate.shift(LEFT*1.15), run_time=.8)
        self.play(disc.animate.shift(LEFT*.55), bug.animate.shift(RIGHT*.55), run_time=.6)
        self.add(tag)
        self.finish()


class S04TunedBarriers(SpokenScene):
    def construct(self):
        w = gut_world(False, False)
        self.add(w)
        title = T("small intestine", 36, TEXT).move_to([0, 3.25, 0])
        slider_line = Line([-2.5, 2.25, 0], [2.5, 2.25, 0], color=GREY, stroke_width=5)
        ends = VGroup(T("relatively leaky", 28, TEXT).move_to([-3.9, 2.25, 0]),
                      T("tighter", 28, TEXT).move_to([3.3, 2.25, 0]))
        knob = Dot([-2.1, 2.25, 0], radius=.16, color=GREEN)
        self.play(FadeIn(title), Create(slider_line), FadeIn(ends), FadeIn(knob), run_time=.9)
        self.at("sodium and water")
        particles = VGroup(*[sodium(GAPS[1]+.11*((i%2)*2-1), 1.7+.3*i) for i in range(4)],
                           *[water_drop(GAPS[0]+.10*((i%2)*2-1), 1.8+.36*i) for i in range(3)])
        self.add(particles)
        self.play(particles.animate.shift(DOWN*3.6), run_time=1.65, rate_func=linear)
        self.at("bladder needs")
        bladder = T("bladder", 36, TEXT).move_to(title)
        narrow = VGroup(*[seal(x, True) for x in GAPS])
        self.play(ReplacementTransform(title, bladder), Transform(w[4], narrow), knob.animate.move_to([2.1, 2.25, 0]), run_time=1.0)
        turned = VGroup(*[sodium(GAPS[1]-.12, 2.45+.22*i) for i in range(4)])
        self.add(turned)
        self.play(turned.animate.shift(LEFT*1.25), run_time=.8)
        self.at("different epithelia")
        self.play(Indicate(slider_line, color=GREEN), Indicate(w[4], color=GREEN), run_time=1.0)
        self.finish()


class S05PredictTeer(SpokenScene):
    def construct(self):
        lab = lab_insert(False)
        self.play(FadeIn(lab[0]), FadeIn(lab[1]), run_time=.7)
        self.at("grow cells")
        self.play(LaggedStart(*[FadeIn(c, shift=UP*.15) for c in lab[2]], lag_ratio=.14),
                  FadeIn(lab[3]), FadeIn(lab[4]), FadeIn(lab[5]), FadeIn(lab[6]), run_time=1.2)
        self.at("one electrode above")
        e1, e2 = electrode(-4.45, 2.0), electrode(2.85, -2.1, True)
        self.play(FadeIn(e1, shift=DOWN*.4), FadeIn(e2, shift=UP*.4), run_time=.9)
        self.at("pass current")
        self.add(lab[7])
        current = Arrow([-3.8, 2.45, 0], [2.45, -2.45, 0], color=BLUE, stroke_width=7, buff=.1)
        self.play(GrowArrow(current), lab[7].animate.shift(DOWN*.25), run_time=1.0)
        self.play(FadeOut(current), FadeIn(lab[8]), run_time=.6)
        self.at("if resistance falls")
        q = T("Lower resistance = glucose leak?", 38, TEXT, weight=BOLD).move_to([0, 3.33, 0])
        panel = RoundedRectangle(width=q.width+.5, height=q.height+.18, corner_radius=.1,
                                 stroke_width=0, fill_color=BG, fill_opacity=.94).move_to(q)
        g = glucose(4.1, -1.65, .21)
        qm = T("?", 46, GOLD).next_to(g, RIGHT, buff=.18)
        self.play(FadeIn(panel), FadeIn(q), FadeIn(g), FadeIn(qm), run_time=.8)
        self.add(lab[9])
        self.finish()


class S06PredictPause(Scene):
    def construct(self):
        lab = lab_insert(False)
        self.add(lab)
        q = T("Lower resistance = glucose leak?", 38, TEXT, weight=BOLD).move_to([0, 3.33, 0])
        panel = RoundedRectangle(width=q.width+.5, height=q.height+.18, corner_radius=.1,
                                 stroke_width=0, fill_color=BG, fill_opacity=.94).move_to(q)
        g = glucose(4.1, -1.65, .21)
        qm = T("?", 46, GOLD).next_to(g, RIGHT, buff=.18)
        self.add(panel, q, g, qm)
        self.play(Rotate(lab[8][2], angle=.10, about_point=[4.75, .35, 0]), run_time=2.2, rate_func=there_and_back)
        self.play(Indicate(lab[4], color=GREEN, scale_factor=1.15), run_time=2.3)


class S07TeerAnswer(SpokenScene):
    def construct(self):
        lab = lab_insert(False)
        self.add(lab)
        q = T("Lower resistance = glucose leak?", 38, TEXT, weight=BOLD).move_to([0, 3.33, 0])
        panel = RoundedRectangle(width=q.width+.5, height=q.height+.18, corner_radius=.1,
                                 stroke_width=0, fill_color=BG, fill_opacity=.94).move_to(q)
        g = glucose(4.1, -1.65, .21)
        qm = T("?", 46, GOLD).next_to(g, RIGHT, buff=.18)
        self.add(panel, q, g, qm)
        no = T("No", 50, RED, weight=BOLD).move_to(qm)
        self.play(ReplacementTransform(qm, no), g.animate.shift(LEFT*1.1).set_opacity(.15), run_time=.7)
        self.at("transepithelial electrical resistance")
        teer = T("TEER:\nionic\nresistance", 28, TEXT, line_spacing=.35).move_to([4.75, -.45, 0])
        self.play(FadeOut(lab[8][3]), FadeIn(teer), FadeOut(VGroup(panel, q, g, no)), run_time=.9)
        self.play(Rotate(lab[8][2], angle=-.48, about_point=[4.75, .35, 0]),
                  lab[2].animate.set_fill(CELL_FILL, .34), run_time=1.5)
        self.play(Rotate(lab[8][2], angle=.48, about_point=[4.75, .35, 0]),
                  lab[2].animate.set_fill(CELL_FILL, .21), Indicate(lab[4], color=GREEN, scale_factor=1.12),
                  run_time=1.5)
        self.at("ions cross")
        between = VGroup(*[sodium(-1.9, 2.3+.20*i, .075) for i in range(4)])
        through = VGroup(*[sodium(-.65, 2.3+.20*i, .075) for i in range(4)])
        self.add(between, through)
        p1 = Line([-1.9, 2.3, 0], [-1.9, -2.4, 0])
        p2 = ArcBetweenPoints([-.65, 2.3, 0], [-.65, -2.4, 0], angle=.7)
        self.play(MoveAlongPath(between, p1), MoveAlongPath(through, p2), run_time=1.8, rate_func=linear)
        self.at("cannot name")
        tags = VGroup(chip("which ion?", BLUE, 28).move_to([-3.5, -.1, 0]),
                      chip("which route?", GREEN, 28).move_to([-.65, -.1, 0]),
                      chip("larger molecules?", GOLD, 28).move_to([2.0, -1.75, 0]))
        self.play(LaggedStart(*[FadeIn(t, shift=UP*.1) for t in tags], lag_ratio=.28), run_time=1.3)
        self.finish()


class S08TeerLimits(SpokenScene):
    def construct(self):
        lab = lab_insert(True, "TEER: low")
        self.add(lab)
        self.at("pass through them")
        a = Arrow([-1.9, 2.4, 0], [-1.9, -2.25, 0], color=BLUE, stroke_width=6)
        b = CurvedArrow([-.65, 2.4, 0], [-.65, -2.25, 0], angle=.65, color=BLUE, stroke_width=6)
        self.play(GrowArrow(a), Create(b), run_time=1.0)
        self.at("selective ion pours")
        token = chip("pore ?", GREEN, 30).move_to([-3.45, -2.6, 0])
        self.play(FadeOut(a), FadeOut(b), FadeIn(token), Indicate(lab[4], color=GREEN), run_time=.8)
        self.at("broader leaks")
        leak = chip("broader leak ?", GREEN, 30).move_to([-.45, -2.6, 0])
        self.play(lab[4].animate.scale(1.45), FadeIn(leak), run_time=.8)
        self.at("or breaks")
        brk = chip("break ?", GREEN, 30).move_to([2.2, -2.6, 0])
        gap = Rectangle(width=.55, height=1.7, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([.60, .25, 0])
        self.play(FadeIn(gap), FadeIn(brk), run_time=.8)
        self.at("design problem below")
        design = chip("design problem below", TEXT, 28).move_to([3.2, 2.8, 0])
        self.play(FadeIn(design), LaggedStart(*[Indicate(t, color=TEXT) for t in (token, leak, brk)], lag_ratio=.2), run_time=1.1)
        self.finish()


class S09FenceQualified(SpokenScene):
    def construct(self):
        w = gut_world(False, True)
        self.play(FadeIn(w), run_time=.9)
        self.at("called a fence")
        fence = VGroup(*[Line([-.18+i*.12, 1.1, 0], [-.18+i*.12, 1.62, 0], color=GREEN, stroke_width=4)
                         for i in range(4)],
                       Line([-.25,1.25,0],[.25,1.25,0],color=GREEN,stroke_width=4),
                       Line([-.25,1.48,0],[.25,1.48,0],color=GREEN,stroke_width=4))
        self.play(FadeIn(fence), run_time=.7)
        self.at("tested in the text below")
        test = T("tested below ?", 28, TEXT).move_to([2.05, 2.20, 0])
        self.play(FadeIn(test), run_time=.65)
        self.at("mark territories")
        self.play(Indicate(w[3][2], color=TEXT), Indicate(w[3][3], color=SLATE), run_time=.9)
        self.at("traffic delivers")
        topv = Dot([CELL_X[1], .0, 0], radius=.20, color=TEXT)
        botv = Dot([CELL_X[1]+.55, .1, 0], radius=.20, color=SLATE)
        self.add(topv, botv)
        self.play(MoveAlongPath(topv, ArcBetweenPoints(topv.get_center(), [CELL_X[1]-.3, TOP,0], angle=.7)),
                  MoveAlongPath(botv, ArcBetweenPoints(botv.get_center(), [CELL_X[1]+.35, BASE,0], angle=-.7)),
                  run_time=1.55)
        self.finish()


class S10PolarityTerritories(SpokenScene):
    def construct(self):
        w = gut_world(False, True)
        self.add(w)
        cx = CELL_X[1]
        crumbs = RoundedRectangle(width=2.35, height=.56, corner_radius=.08, color=TEXT, stroke_width=3,
                                  fill_color=TEXT, fill_opacity=.22).move_to([cx, 1.48, 0])
        crlab = T("Crumbs", 30, TEXT).move_to(crumbs)
        self.play(GrowFromCenter(crumbs), FadeIn(crlab), run_time=.75)
        self.at("scribble marks")
        scribble = RoundedRectangle(width=.65, height=2.55, corner_radius=.08, color=SLATE, stroke_width=3,
                                    fill_color=SLATE, fill_opacity=.3).move_to([cx+1.05, -.35, 0])
        slab = T("Scribble", 28, TEXT).rotate(PI/2).move_to(scribble)
        self.play(GrowFromCenter(scribble), FadeIn(slab), run_time=.85)
        self.at("par complex")
        bracket = BraceBetweenPoints([cx+.72, 1.0, 0], [cx+1.38, 1.0, 0], color=MAGENTA)
        plab = T("Par", 30, MAGENTA).move_to([cx-.05, .82, 0])
        self.play(GrowFromCenter(bracket), FadeIn(plab), run_time=.7)
        self.at("restrain one another")
        self.play(crumbs.animate.scale(1.08), scribble.animate.scale(1.05), run_time=.45, rate_func=there_and_back)
        self.play(bracket.animate.scale(1.15), run_time=.45, rate_func=there_and_back)
        self.at("polarized traffic")
        v1, v2 = Dot([cx-.4, 0, 0], radius=.18, color=BLUE), Dot([cx+.35, 0, 0], radius=.18, color=RED)
        self.add(v1, v2)
        self.play(v1.animate.move_to([cx-.28, TOP,0]), v2.animate.move_to([cx-.48, BASE,0]), run_time=1.2)
        self.play(ReplacementTransform(v1, turnstile(cx-.28)), ReplacementTransform(v2, pump(cx-.48)), run_time=.7)
        self.finish()


class S11JunctionStack(SpokenScene):
    def construct(self):
        pair = two_cell_closeup()
        self.add(pair)
        self.play(VGroup(pair[0],pair[1],pair[2],pair[3]).animate.shift(UP*.65), run_time=.65)
        self.at("adherence junction")
        adh = RoundedRectangle(width=.38, height=.32, corner_radius=.06, stroke_width=0,
                               fill_color=ORANGE, fill_opacity=1).move_to([0, 1.25, 0])
        ropes = VGroup(Line([-3.6,1.25,0],[-.2,1.25,0],color=ORANGE,stroke_width=8),
                       Line([.2,1.25,0],[3.6,1.25,0],color=ORANGE,stroke_width=8))
        alab = T("adherens", 28, ORANGE).move_to([1.15, 1.65, 0])
        self.play(Create(ropes), FadeIn(adh), FadeIn(alab), run_time=.9)
        self.play(ropes.animate.stretch(1.05, 0), run_time=.45, rate_func=there_and_back)
        self.at("desmosomes link")
        des = Circle(radius=.23, color=PURPLE, fill_color=PURPLE, fill_opacity=1).move_to([0, -.1, 0])
        cables = VGroup(ArcBetweenPoints([-3.7,-1.2,0],[-.2,-.1,0],angle=-.5,color=PURPLE,stroke_width=8),
                        ArcBetweenPoints([.2,-.1,0],[3.7,-1.2,0],angle=-.5,color=PURPLE,stroke_width=8))
        dlab = T("desmosome", 28, PURPLE).move_to([1.25, .25, 0])
        self.play(Create(cables), FadeIn(des), FadeIn(dlab), run_time=.9)
        self.play(pair[0].animate.shift(LEFT*.12), pair[1].animate.shift(RIGHT*.12), run_time=.55, rate_func=there_and_back)
        self.at("gap junctions")
        gap = RoundedRectangle(width=.48, height=.22, corner_radius=.08, stroke_width=0,
                               fill_color=CYAN, fill_opacity=1).move_to([0, -1.55, 0])
        glab = T("gap junction", 28, CYAN).move_to([1.45, -1.55, 0])
        dots = VGroup(sodium(-2.0,-1.55,.065), glucose(-2.35,-1.55,.065))
        self.play(FadeIn(gap), FadeIn(glab), FadeIn(dots), run_time=.6)
        self.play(dots.animate.shift(RIGHT*4.5), pair[0].animate.set_fill(CELL_FILL, .29),
                  pair[1].animate.set_fill(CELL_FILL, .29), run_time=1.25, rate_func=linear)
        self.play(pair[0].animate.set_fill(CELL_FILL, .20), pair[1].animate.set_fill(CELL_FILL, .20), run_time=.75)
        self.finish()


class S12BaseAnchor(SpokenScene):
    def construct(self):
        pair = two_cell_closeup()
        pair[0].stretch(.90,1).shift(UP*.25); pair[1].stretch(.90,1).shift(UP*.25)
        self.add(pair)
        mat = RoundedRectangle(width=11.0, height=.55, corner_radius=.12, color=TAN, stroke_width=3,
                               fill_color=TAN, fill_opacity=.35).move_to([0,-2.72,0])
        self.play(FadeIn(mat, shift=UP*.15), VGroup(pair[0], pair[1], pair[2], pair[3]).animate.shift(UP*.18), run_time=.9)
        self.at("hemidesmosomes connect")
        anchors = VGroup(*[Triangle(color=RED_BROWN, fill_color=RED_BROWN, fill_opacity=1).scale(.25).rotate(PI)
                           .move_to([x,-2.42,0]) for x in (-2.7,2.7)])
        cables = VGroup(*[ArcBetweenPoints([x-.8,-.2,0],[x,-2.35,0],angle=.35,color=PURPLE,stroke_width=8)
                          for x in (-2.7,2.7)])
        mlab = T("basement membrane", 30, TAN).move_to([0,-3.35,0])
        self.play(Create(cables), FadeIn(anchors), FadeIn(mlab),
                  pair[0].animate.set_fill(CELL_FILL, .30), pair[1].animate.set_fill(CELL_FILL, .30), run_time=1.2)
        self.play(pair[0].animate.set_fill(CELL_FILL, .20), pair[1].animate.set_fill(CELL_FILL, .20), run_time=.8)
        self.at("different job")
        stack = VGroup(pair[3],
                       RoundedRectangle(width=.34,height=.28,corner_radius=.05,stroke_width=0,fill_color=ORANGE,fill_opacity=1).move_to([0,1.15,0]),
                       Circle(radius=.2,color=PURPLE,fill_color=PURPLE,fill_opacity=1).move_to([0,.15,0]),
                       RoundedRectangle(width=.42,height=.18,corner_radius=.05,stroke_width=0,fill_color=CYAN,fill_opacity=1).move_to([0,-.85,0]),
                       anchors)
        labels = VGroup(*[T(x,28,c) for x,c in zip(("select","grip","resist","connect","anchor"),(GREEN,ORANGE,PURPLE,CYAN,RED_BROWN))])
        for i, (lab, mark, y) in enumerate(zip(labels, stack, (2.2,1.15,.15,-.85,-2.0))):
            lab.move_to([1.25,y,0])
            fill = .22 if i % 2 == 0 else .27
            self.play(Indicate(mark,color=lab.get_color()), FadeIn(lab),
                      pair[0].animate.set_fill(CELL_FILL, fill),
                      pair[1].animate.set_fill(CELL_FILL, fill), run_time=.34)
        drift_time = max(.4, self.t_of("stay selective") - .2 - self.elapsed())
        self.play(pair[0].animate.set_fill(CELL_FILL, .31),
                  pair[1].animate.set_fill(CELL_FILL, .31), run_time=drift_time/2)
        self.play(pair[0].animate.set_fill(CELL_FILL, .23),
                  pair[1].animate.set_fill(CELL_FILL, .23), run_time=drift_time/2)
        self.at("stay selective")
        self.play(VGroup(pair[0],pair[1],pair[2],pair[3],cables,anchors).animate.rotate(.06,about_point=[0,-2.7,0]),
                  run_time=.8, rate_func=there_and_back)
        self.play(LaggedStart(*[Indicate(m,color=c) for m,c in zip(stack,(GREEN,ORANGE,PURPLE,CYAN,RED_BROWN))],lag_ratio=.12),
                  pair[0].animate.set_fill(CELL_FILL, .20), pair[1].animate.set_fill(CELL_FILL, .20), run_time=1.1)
        self.finish()


class S13ReturnToGut(SpokenScene):
    def construct(self):
        w = gut_world(True, True, True)
        self.add(w)
        self.play(LaggedStart(*[FadeIn(p) for p in w[8]], lag_ratio=.1), run_time=.7)
        self.at("pump stays")
        self.play(LaggedStart(*[Indicate(p[0],color=BLUE) for p in w[8]],lag_ratio=.12),
                  LaggedStart(*[Indicate(p[2],color=RED) for p in w[8]],lag_ratio=.12),run_time=.9)
        self.at("selective seal")
        ions = VGroup(*[sodium(GAPS[1],2.4+.2*i,.075) for i in range(3)])
        self.add(ions)
        self.play(ions.animate.shift(DOWN*2.2), Indicate(w[4][1],color=GREEN), run_time=1.0)
        self.at("deeper junctions")
        self.play(LaggedStart(*[Indicate(m,color=c) for m,c in zip(w[9],(ORANGE,PURPLE,CYAN,RED_BROWN))],lag_ratio=.16),run_time=1.0)
        arrow = Arrow([CELL_X[1],1.25,0],[CELL_X[1],-1.25,0],color=GOLD,stroke_width=10,buff=0)
        self.play(GrowArrow(arrow), run_time=.8)
        move_glucose(self,CELL_X[1],1.1)
        self.finish()


class S14OrganizingRule(SpokenScene):
    def construct(self):
        w = gut_world(True, True, True)
        self.add(w)
        rule = T("Division of labour", 42, TEXT, weight=BOLD).move_to([0,3.30,0])
        panel = RoundedRectangle(width=rule.width+.5,height=rule.height+.18,corner_radius=.1,
                                 stroke_width=0,fill_color=BG,fill_opacity=.93).move_to(rule)
        self.play(FadeIn(panel),FadeIn(rule),run_time=.7)
        self.at("a gate")
        icons = VGroup(chip("selective gate",GREEN,28).move_to([1.55,1.30,0]),
                       chip("distinct faces",TEXT,28).move_to([-1.45,-.25,0]),
                       chip("grip",ORANGE,28).move_to([1.55,.55,0]),
                       chip("anchor",RED_BROWN,28).move_to([1.55,-1.05,0]),
                       chip("channel",CYAN,28).move_to([1.55,-.25,0]))
        self.play(FadeOut(w[8]), LaggedStart(*[FadeIn(i,shift=UP*.1) for i in icons],lag_ratio=.18),run_time=1.3)
        self.at("work together")
        for icon in icons:
            self.play(Indicate(icon,color=icon[0].get_stroke_color(),scale_factor=1.08),run_time=.25)
        self.at("not interchangeable")
        frame = RoundedRectangle(width=10.2,height=4.3,corner_radius=.25,color=TEXT,stroke_width=4).move_to([-.6,-.25,0])
        self.play(Create(frame), LaggedStart(*[Indicate(i,color=i[0].get_stroke_color()) for i in icons],lag_ratio=.12), run_time=.9)
        self.finish()


class S15End(EndCard):
    LINE = "Selective gates, distinct faces, and strong junctions divide the work."

    def construct(self):
        w = gut_world(True, True, True)
        w.set_opacity(.25)
        self.add(w)
        line = T(self.LINE, 38, TEXT, font=TITLE_FONT).move_to([0,.20,0])
        fit(line,max_w=11.4)
        panel = RoundedRectangle(width=line.width+.7,height=line.height+.45,corner_radius=.15,
                                 stroke_width=0,fill_color=BG,fill_opacity=.86).move_to(line)
        self.play(FadeIn(panel),FadeIn(line,shift=UP*.1),run_time=.7)
        self.play(LaggedStart(Indicate(w[4],color=GREEN),
                              *[Indicate(m,color=c) for m,c in zip(w[9],(ORANGE,PURPLE,CYAN,RED_BROWN))],
                              lag_ratio=.15),run_time=1.6)
        self.finish()
