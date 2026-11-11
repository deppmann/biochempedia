"""Two Faces and a Seal -- one continuous epithelial teaching world.

COLOR MAP (fixed for the whole film)
  GOLD   glucose
  BLUE   sodium
  RED    sodium pump and ATP
  GREEN  seal between cells
  TEXT   apical face
  GREY   basolateral face and cell structure
"""
from bp_style import *  # noqa: F401,F403


GOLD_GLUCOSE = GOLD
SLATE = "#667080"
CELL_FILL = "#C8CED8"
CELL_X = (-4.45, -1.45, 1.55)
CELL_W = 2.78
TOP, BASE = 1.75, -1.80
GAPS = (-2.95, 0.05)
GUT_Y, BLOOD_Y = 2.75, -2.75
GAUGE_X = (4.75, 5.85)


def glucose(x, y, r=0.105):
    return Dot([x, y, 0], radius=r, color=GOLD_GLUCOSE)


def sodium(x, y, r=0.09):
    return Dot([x, y, 0], radius=r, color=BLUE)


def cell_shape(cx, bright=False):
    c = Rectangle(width=CELL_W, height=TOP - BASE, stroke_color=SLATE, stroke_width=4,
                  fill_color=CELL_FILL, fill_opacity=0.10).move_to([cx, (TOP + BASE) / 2, 0])
    if bright:
        c.set_fill(CELL_FILL, 0.18)
    return c


def membranes(cx):
    top = Line([cx - CELL_W / 2, TOP, 0], [cx + CELL_W / 2, TOP, 0], color=TEXT, stroke_width=8)
    lower = VMobject(color=SLATE, stroke_width=8).set_points_as_corners([
        [cx - CELL_W / 2, TOP - 0.05, 0], [cx - CELL_W / 2, BASE, 0],
        [cx + CELL_W / 2, BASE, 0], [cx + CELL_W / 2, TOP - 0.05, 0]])
    return top, lower


def seal(x, open_gap=False):
    if open_gap:
        return VGroup(
            RoundedRectangle(width=0.16, height=0.22, corner_radius=0.04, stroke_width=0,
                             fill_color=GREEN, fill_opacity=1).move_to([x, 1.47, 0]),
            RoundedRectangle(width=0.16, height=0.22, corner_radius=0.04, stroke_width=0,
                             fill_color=GREEN, fill_opacity=1).move_to([x, 1.05, 0]))
    return RoundedRectangle(width=0.22, height=0.62, corner_radius=0.05, stroke_width=0,
                            fill_color=GREEN, fill_opacity=1).move_to([x, 1.27, 0])


def turnstile(cx, y=TOP):
    ring = Circle(radius=0.30, color=BLUE, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([cx, y, 0])
    bars = VGroup(Line(LEFT * 0.25, RIGHT * 0.25), Line(DOWN * 0.25, UP * 0.25)).set_stroke(BLUE, 5).move_to(ring)
    return VGroup(ring, bars)


def exit_door(cx, y=BASE):
    jamb = VGroup(Line([cx - 0.28, y, 0], [cx - 0.28, y + 0.52, 0]),
                  Line([cx + 0.28, y, 0], [cx + 0.28, y + 0.52, 0])).set_stroke(GOLD_GLUCOSE, 5)
    door = Line([cx - 0.26, y + 0.02, 0], [cx + 0.16, y + 0.42, 0], color=GOLD_GLUCOSE, stroke_width=5)
    return VGroup(jamb, door)


def pump(cx, y=BASE):
    body = RoundedRectangle(width=0.66, height=0.48, corner_radius=0.12, color=RED, stroke_width=4,
                            fill_color=RED, fill_opacity=0.22).move_to([cx, y, 0])
    chevron = VGroup(Line([-0.14, -0.10, 0], [0.08, 0, 0]), Line([0.08, 0, 0], [-0.14, 0.10, 0]))
    chevron.set_stroke(RED, 5).move_to(body)
    return VGroup(body, chevron)


def slot(cx, y):
    return RoundedRectangle(width=0.56, height=0.24, corner_radius=0.10, color=GREY,
                            stroke_width=3, fill_color=GREY, fill_opacity=0.10).move_to([cx, y, 0])


def gauge(x, label, level=0.75):
    bottom, height = -0.75, 2.30
    outline = RoundedRectangle(width=0.62, height=height, corner_radius=0.12, color=GREY, stroke_width=3)
    outline.move_to([x, bottom + height / 2, 0])
    fill_h = max(0.08, height * level)
    fill = Rectangle(width=0.45, height=fill_h, stroke_width=0, fill_color=GOLD_GLUCOSE,
                     fill_opacity=0.78).move_to([x, bottom + fill_h / 2, 0])
    lab = T(label, 28, GOLD_GLUCOSE).rotate(PI / 2).next_to(outline, DOWN, buff=0.18)
    return VGroup(outline, fill, lab)


def gauges(gut_level=0.85, blood_level=0.48, dashed=True):
    gg = gauge(GAUGE_X[0], "gut", gut_level)
    bg = gauge(GAUGE_X[1], "blood", blood_level)
    line_y = -0.75 + 2.30 * blood_level
    line = DashedLine([4.30, line_y, 0], [6.30, line_y, 0], dash_length=0.10,
                      color=GOLD_GLUCOSE, stroke_width=3).set_opacity(0.65)
    tag = T("schematic", 28, TEXT).move_to([5.30, -1.88, 0])
    return VGroup(gg, bg, line if dashed else VGroup(), tag)


def world(gut_level=0.85, blood_level=0.48, proteins=False, open_seal=False,
          particles=True, labels=True):
    cells = VGroup(*[cell_shape(x, i == 1) for i, x in enumerate(CELL_X)])
    mems = VGroup(*[m for x in CELL_X for m in membranes(x)])
    seals = VGroup(*[seal(x, open_seal) for x in GAPS])
    gut_band = Rectangle(width=9.70, height=1.10, stroke_width=0, fill_color=BLUE, fill_opacity=0.05).move_to([-1.05, GUT_Y, 0])
    blood_band = Rectangle(width=9.70, height=1.10, stroke_width=0, fill_color=BLUE, fill_opacity=0.08).move_to([-1.05, BLOOD_Y, 0])
    labs = VGroup(T("gut", 30, TEXT).move_to([-5.65, GUT_Y, 0]),
                  T("blood", 30, TEXT).move_to([-5.45, BLOOD_Y, 0])) if labels else VGroup()
    flow = VGroup(*[Dot([x, BLOOD_Y + 0.15 * ((i % 5) - 2), 0], radius=0.08, color=TEXT).set_opacity(0.52)
                    for i, x in enumerate(np.linspace(-4.9, 3.6, 50))])

    def stream(mob, dt):
        for d in mob:
            d.shift(RIGHT * 0.90 * dt)
            if d.get_x() > 3.75:
                d.shift(LEFT * 8.75)
    flow.add_updater(stream)
    dots = VGroup()
    if particles:
        dots.add(*[glucose(x, GUT_Y + (i % 2) * 0.25 - 0.12) for i, x in enumerate(np.linspace(-4.7, 3.0, 10))])
    pro = VGroup()
    if proteins:
        for x in CELL_X:
            pro.add(VGroup(turnstile(x - 0.28), exit_door(x + 0.30), pump(x - 0.48)))
    return VGroup(gut_band, blood_band, cells, mems, seals, labs, flow, dots, pro, gauges(gut_level, blood_level))


def move_glucose(scene, x, run_time=1.5):
    d = glucose(x, GUT_Y)
    scene.add(d)
    scene.play(MoveAlongPath(d, VMobject().set_points_as_corners([
        [x, GUT_Y, 0], [x, TOP + 0.2, 0], [x, 0.1, 0], [x + 0.25, BASE - 0.2, 0], [x + 0.75, BLOOD_Y, 0]])),
        run_time=run_time, rate_func=linear)
    return d


def bob(scene, group, run_time=1.0):
    scene.play(group.animate.shift(UP * 0.08), run_time=run_time / 2, rate_func=smooth)
    scene.play(group.animate.shift(DOWN * 0.08), run_time=run_time / 2, rate_func=smooth)


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Epithelia and tissue organization"
    TITLE = "Two Faces and a Seal"

    def construct(self):
        w = world(gut_level=0.82, particles=True)
        self.play(FadeIn(w[0]), FadeIn(w[1]), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in w[2]], lag_ratio=0.18),
                  run_time=1.25)
        self.at("sheet just one cell")
        self.play(FadeIn(VGroup(w[3], w[4], w[5], w[6], w[7], w[9])), run_time=0.75)
        self.at("How does it keep")
        move_glucose(self, CELL_X[1], 1.6)
        self.at("even when the gut")
        low = gauges(0.38, 0.48)
        self.play(Transform(w[9], low), run_time=1.15)
        q = T("Uphill?", 48, TEXT, weight=BOLD).move_to([-1.1, 3.25, 0])
        q_panel = RoundedRectangle(width=q.width + .45, height=q.height + .18, corner_radius=.10,
                                   stroke_width=0, fill_color=BG, fill_opacity=.94).move_to(q)
        self.play(FadeIn(q_panel), FadeIn(q, shift=DOWN * 0.10), run_time=0.45)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Epithelia and tissue organization"
    TITLE = "Two Faces and a Seal"

    def construct(self):
        w = world(gut_level=0.38, particles=True)
        self.add(w)
        title = T(self.TITLE, 48, TEXT, font=TITLE_FONT).move_to([-1.1, 3.15, 0])
        title_panel = RoundedRectangle(width=title.width + .55, height=title.height + .18, corner_radius=.10,
                                       stroke_width=0, fill_color=BG, fill_opacity=.94).move_to(title)
        self.play(FadeIn(title_panel), FadeIn(title), Transform(w[9], gauges(0.85, 0.48)), run_time=0.75)
        mover = glucose(CELL_X[1], GUT_Y)
        self.add(mover)
        self.play(mover.animate.move_to([CELL_X[1], BLOOD_Y, 0]), run_time=0.8, rate_func=linear)
        self.play(FadeOut(title), FadeOut(title_panel), run_time=0.25)
        self.finish()


class S02Faces(SpokenScene):
    def construct(self):
        w = world(particles=False)
        self.add(w)
        mid = w[2][1]
        self.play(mid.animate.set_fill(CELL_FILL, 0.26).scale(1.05), run_time=0.75)
        self.at("the apical face")
        top, lower = membranes(CELL_X[1])
        top.set_stroke(width=13)
        ap = T("apical", 32, TEXT).move_to([CELL_X[1], 2.25, 0])
        self.play(Create(top), FadeIn(ap, shift=DOWN * 0.1), run_time=0.85)
        self.at("the basolateral face")
        lower.set_stroke(width=12)
        bl = T("basolateral", 30, GREY).move_to([CELL_X[1], -0.95, 0])
        self.play(Create(lower), FadeIn(bl), run_time=1.2)
        self.at("look toward its neighbors")
        self.play(Indicate(w[2][0], color=GREY), Indicate(w[2][2], color=GREY), run_time=1.0)
        self.at("Each face carries")
        slots = VGroup(slot(CELL_X[1] - 0.28, TOP), slot(CELL_X[1] - 0.48, BASE), slot(CELL_X[1] + 0.30, BASE))
        self.play(LaggedStart(*[GrowFromCenter(s) for s in slots], lag_ratio=0.25), run_time=1.45)
        self.play(LaggedStart(*[Indicate(s, color=TEXT, scale_factor=1.12) for s in slots], lag_ratio=0.2), run_time=1.0)
        self.finish()


class S03Turnstile(SpokenScene):
    def construct(self):
        w = world(particles=False)
        self.add(w)
        x = CELL_X[1] - 0.28
        empty = slot(x, TOP)
        self.add(empty)
        self.at("On the apical face")
        ts = turnstile(x)
        self.play(ReplacementTransform(empty, ts), run_time=0.8)
        self.at("called")
        lab = T("SGLT1", 30, BLUE).move_to([CELL_X[2], 1.02, 0])
        self.play(FadeIn(lab), run_time=0.55)
        self.at("sodium glucose carrier")
        crowded = VGroup(*[sodium(x + dx, GUT_Y + dy) for dx, dy in [(-.8,0),(-.55,.25),(-.3,-.15),(0,.2),(.25,-.1),(.55,.2),(.8,-.15)]])
        self.play(LaggedStart(*[FadeIn(d) for d in crowded], lag_ratio=0.10), run_time=0.9)
        self.at("Think of it as")
        turn = T("turnstile", 30, BLUE).move_to([CELL_X[2], .50, 0])
        self.play(Rotate(ts[1], PI / 2), FadeIn(turn), run_time=1.0)
        self.at("Two sodium ions")
        pair = VGroup(sodium(x - 0.22, 2.25), glucose(x, 2.40), sodium(x + 0.22, 2.25))
        self.play(FadeIn(pair), run_time=0.35)
        self.play(Rotate(ts[1], PI / 2), pair.animate.move_to([x, 0.55, 0]), run_time=1.45)
        self.play(pair.animate.shift(DOWN * 0.20), run_time=0.5)
        self.finish()


class S04Fare(SpokenScene):
    def construct(self):
        w = world(particles=False)
        self.add(w)
        x = CELL_X[1] - 0.28
        ts = turnstile(x)
        self.add(ts)
        slope = Polygon([-2.72, 2.75, 0], [-0.20, 2.75, 0], [-0.20, -0.25, 0],
                        color=BLUE, fill_color=BLUE, fill_opacity=0.10, stroke_width=3)
        outdots = VGroup(*[sodium(-2.5 + .35*(i%4), 2.25 + .25*(i//4)) for i in range(8)])
        indot = VGroup(sodium(-1.8, .4), sodium(-1.1, -.1))
        self.play(FadeIn(slope), LaggedStart(*[FadeIn(d) for d in outdots], lag_ratio=.06), FadeIn(indot), run_time=1.25)
        self.at("sparse inside")
        minus = T("−", 52, BLUE, weight=BOLD).move_to([-1.45, 0.75, 0])
        self.play(FadeIn(minus), run_time=0.5)
        self.at("sodium falls inward")
        downhill = Arrow([-2.45, 2.25, 0], [-1.55, 0.45, 0], color=BLUE, stroke_width=9, buff=0.05)
        dl = T("sodium: downhill", 28, BLUE).move_to([-3.95, 0.60, 0])
        pair = VGroup(sodium(-2.2, 2.35), sodium(-1.9, 2.35))
        self.add(pair)
        self.play(GrowArrow(downhill), FadeIn(dl), pair.animate.move_to([-1.55, 0.15, 0]), run_time=1.35)
        self.at("That fall")
        step = VGroup(Line([0.10, 0.25, 0], [0.75, 0.25, 0]), Line([0.75, 0.25, 0], [0.75, 1.05, 0]),
                      Line([0.75, 1.05, 0], [1.35, 1.05, 0])).set_stroke(GOLD_GLUCOSE, 6)
        gl = glucose(0.25, 0.45, .14)
        self.play(Create(step), FadeIn(gl), run_time=0.65)
        self.at("pays the fare")
        coin = Circle(radius=.20, color=BLUE, fill_color=BLUE, fill_opacity=.25).move_to([-1.55, .65, 0])
        coin.add(T("Na", 28, BLUE).scale(.78).move_to(coin))
        up = T("glucose: uphill", 28, GOLD_GLUCOSE).move_to([1.55, 2.35, 0])
        self.play(coin.animate.move_to(ts), gl.animate.move_to([1.10, 1.25, 0]), FadeIn(up), run_time=1.2)
        self.play(Rotate(ts[1], PI / 2), run_time=0.55)
        self.finish()


class S05Exit(SpokenScene):
    def construct(self):
        w = world(particles=False)
        self.add(w)
        x = CELL_X[1]
        pile = VGroup(*[glucose(x + dx, y) for dx, y in [(-.55,.35),(-.18,.15),(.2,.42),(.48,.05),(-.35,-.35)]])
        self.play(LaggedStart(*[FadeIn(d) for d in pile], lag_ratio=.12), run_time=1.1)
        self.at("free exit door")
        door = exit_door(x + .30)
        self.play(GrowFromCenter(door), run_time=.75)
        label = T("GLUT2", 30, GOLD_GLUCOSE).move_to([0.65, -1.32, 0])
        self.play(FadeIn(label), run_time=.45)
        self.at("passive carrier")
        passive = T("free exit", 28, TEXT).move_to([0.70, -0.75, 0])
        self.play(FadeIn(passive), door[1].animate.rotate(-0.35, about_point=door[1].get_start()), run_time=.75)
        self.at("spends no energy")
        no_atp = T("no ATP", 30, TEXT).move_to([-3.95, -0.25, 0])
        self.play(FadeIn(no_atp), run_time=.5)
        self.at("glucose runs out")
        for i, d in enumerate(pile[:3]):
            self.play(d.animate.move_to([x + .30 + .18*i, BLOOD_Y, 0]), run_time=.65, rate_func=linear)
        flow_arrow = Arrow([-.55, BLOOD_Y, 0], [2.4, BLOOD_Y, 0], color=GOLD_GLUCOSE, buff=0, stroke_width=6)
        self.play(GrowArrow(flow_arrow), run_time=.65)
        self.at("standard account")
        std = T("GLUT2 • standard account", 28, GOLD_GLUCOSE).move_to([1.55, -.78, 0])
        self.play(FadeOut(VGroup(label, passive, no_atp)), FadeIn(std), run_time=.8)
        self.finish()


class S06Pump(SpokenScene):
    def construct(self):
        w = world(particles=False)
        self.add(w)
        x = CELL_X[1]
        blue = VGroup(*[sodium(x + dx, y) for dx, y in [(-.65,.65),(-.2,.45),(.25,.6),(-.5,.05),(.15,-.15),(.55,.15)]])
        gold = glucose(x+.4,.85,.13)
        self.play(FadeIn(blue), FadeIn(gold), run_time=.75)
        self.at("brought two sodium")
        self.play(LaggedStart(*[d.animate.shift(DOWN*.18) for d in blue], lag_ratio=.08), run_time=.8)
        self.at("The sodium pump")
        p = pump(x-.48)
        pl = T("sodium pump", 28, RED).move_to([-3.75, -1.15, 0])
        self.play(GrowFromCenter(p), FadeIn(pl), run_time=.8)
        self.at("spends a TP")
        atp = chip("ATP", RED, size=28).move_to([x-.48, -.95, 0])
        self.play(atp.animate.move_to(p), run_time=.7)
        self.at("throw sodium back")
        self.play(LaggedStart(*[d.animate.move_to([x-.48 + .16*(i%3), BLOOD_Y, 0]) for i,d in enumerate(blue)], lag_ratio=.10),
                  Rotate(p[1], PI), run_time=1.35)
        self.at("keeps the slopes")
        steep = Arrow([-2.55, 2.55, 0], [-1.55, .30, 0], color=BLUE, stroke_width=10, buff=.05)
        self.play(GrowArrow(steep), FadeOut(atp), run_time=.85)
        self.play(Indicate(steep, color=BLUE), run_time=.7)
        self.finish()


class S07Uphill(SpokenScene):
    def construct(self):
        w = world(gut_level=.85, proteins=True)
        self.add(w)
        clock = Circle(radius=.36, color=TEXT, stroke_width=4).move_to([-4.45, .15, 0])
        hand = Line(clock.get_center(), clock.get_center()+UP*.27, color=TEXT, stroke_width=4)
        self.at("run the clock")
        self.play(Create(clock), Create(hand), Rotate(hand, 2*PI, about_point=clock.get_center()), run_time=1.2, rate_func=linear)
        self.at("gauge falls")
        self.play(Transform(w[9], gauges(.48,.48)), Rotate(w[8][1][0][1], PI/2), run_time=1.45)
        move_glucose(self, CELL_X[1], 1.1)
        self.at("keeps falling below")
        self.play(Transform(w[9], gauges(.23,.48)), Rotate(hand, 2*PI, about_point=clock.get_center()), run_time=1.2, rate_func=linear)
        self.at("moving uphill")
        arrow = Arrow([6.45,-.20,0],[6.45,.55,0],color=GOLD_GLUCOSE,stroke_width=8,buff=0)
        lab = T("uphill", 28, GOLD_GLUCOSE).rotate(PI/2).next_to(arrow, LEFT, buff=.10)
        self.play(GrowArrow(arrow), FadeIn(lab), run_time=.7)
        self.finish()


class S08Watch(Scene):
    def construct(self):
        w = world(gut_level=.23, proteins=True)
        self.add(w)
        d1, d2 = glucose(CELL_X[0],GUT_Y), glucose(CELL_X[2],GUT_Y)
        self.add(d1,d2)
        self.play(d1.animate.move_to([CELL_X[0],BLOOD_Y,0]), d2.animate.move_to([CELL_X[2],BLOOD_Y,0]),
                  Rotate(w[8][1][0][1], PI/2), Rotate(w[8][2][0][1], PI/2),
                  Transform(w[9],gauges(.12,.48)), run_time=2.5, rate_func=linear)
        self.wait(.5)


class S09Direction(SpokenScene):
    def construct(self):
        w = world(gut_level=.20, proteins=True)
        self.add(w)
        title = T("Where carriers sit sets the direction", 34, TEXT).move_to([-1.0,3.25,0])
        title_panel = RoundedRectangle(width=title.width + .5, height=title.height + .16, corner_radius=.10,
                                       stroke_width=0, fill_color=BG, fill_opacity=.94).move_to(title)
        self.play(FadeIn(title_panel), FadeIn(title), run_time=.65)
        self.at("Under these gut gradients")
        soft = VGroup(*[glucose(x,y) for x,y in [(-4.7,2.65),(-.9,2.75),(1.7,2.65),(-3.9,-2.7),(.8,-2.8)]])
        self.play(FadeIn(soft), run_time=.55)
        bob(self,soft,1.0)
        self.at("carrier's place")
        self.play(Indicate(w[2][1], color=TEXT, scale_factor=1.03), run_time=.8)
        self.at("turnstile on top")
        self.play(Indicate(w[8][1][0], color=BLUE, scale_factor=1.25), run_time=.8)
        self.at("exit door underneath")
        self.play(Indicate(w[8][1][1], color=GOLD_GLUCOSE, scale_factor=1.25), run_time=.8)
        self.at("from gut to blood")
        ar = Arrow([CELL_X[1],1.15,0],[CELL_X[1],-1.15,0],color=GOLD_GLUCOSE,stroke_width=12,buff=0)
        lab = T("gut to blood",32,GOLD_GLUCOSE).next_to(ar,RIGHT,buff=.18)
        self.play(GrowArrow(ar),FadeIn(lab),run_time=1.0)
        bob(self,soft,1.0)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        w = world(gut_level=.82, particles=False)
        self.add(w)
        self.at("look between the cells")
        focus = SurroundingRectangle(w[4][1],color=GREEN,buff=.20,stroke_width=4)
        self.play(Create(focus),run_time=.75)
        self.at("joined near the top")
        lab=T("seal",30,GREEN).move_to([.65,1.20,0])
        self.play(FadeIn(lab),Indicate(w[4][1],color=GREEN),run_time=.8)
        self.at("thought experiment")
        tag=chip("thought experiment",TEXT,size=28).move_to([1.75,2.35,0])
        self.play(FadeIn(tag),run_time=.55)
        self.at("Loosen that seal")
        opened=seal(GAPS[1],True)
        self.play(ReplacementTransform(w[4][1],opened),FadeOut(focus),run_time=1.05)
        self.at("let glucose slip")
        g=glucose(GAPS[1],2.25,.14)
        self.add(g)
        self.play(g.animate.move_to([GAPS[1],.85,0]),run_time=.75)
        self.at("Would the gut")
        q=T("Open the seal: does the gut still take up glucose?",34,TEXT).move_to([-1.0,3.30,0])
        fit(q,max_w=9.9)
        self.play(FadeOut(tag), FadeIn(q,shift=DOWN*.10),run_time=.6)
        bob(self,g,1.0)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        w=world(gut_level=.82,particles=False,open_seal=True)
        q=T("Open the seal: does the gut still take up glucose?",34,TEXT).move_to([-1.0,3.30,0])
        fit(q,max_w=9.9)
        dots=VGroup(glucose(-.15,2.3,.13),glucose(.22,2.6,.13),glucose(-.05,-2.65,.13))
        self.add(w,q,dots)
        for _ in range(3):
            self.play(dots.animate.shift(UP*.07),w[4][1].animate.set_opacity(.55),run_time=.7)
            self.play(dots.animate.shift(DOWN*.07),w[4][1].animate.set_opacity(1),run_time=.7)
        self.wait(.3)


class S12Early(SpokenScene):
    def construct(self):
        w=world(gut_level=.82,particles=False,open_seal=True)
        q=T("Open the seal: does the gut still take up glucose?",34,TEXT).move_to([-1.0,3.30,0])
        fit(q,max_w=9.9)
        self.add(w,q)
        self.play(FadeOut(q),run_time=.5)
        self.at("Between the cells")
        leak=Arrow([GAPS[1],1.0,0],[GAPS[1],-1.2,0],color=GOLD_GLUCOSE,stroke_width=8,buff=0)
        leaklab=T("leak",28,GOLD_GLUCOSE).next_to(leak,RIGHT,buff=.15)
        self.play(GrowArrow(leak),FadeIn(leaklab),run_time=.85)
        self.at("follows its own gradient")
        dots=VGroup(*[glucose(GAPS[1]+dx,2.4+.2*i,.12) for i,dx in enumerate((-.15,.12,-.08))])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.shift(DOWN*4.8) for d in dots],lag_ratio=.18),run_time=1.5,rate_func=linear)
        self.at("Early in a meal")
        early=T("early: gut > blood",30,GOLD_GLUCOSE).move_to([-2.9,3.28,0])
        self.play(FadeIn(early),Transform(w[9],gauges(.68,.48)),run_time=.85)
        self.at("open seal adds")
        through=glucose(CELL_X[1],GUT_Y)
        para=glucose(GAPS[1],GUT_Y)
        self.add(through,para)
        self.play(through.animate.move_to([CELL_X[1],BLOOD_Y,0]),para.animate.move_to([GAPS[1],BLOOD_Y,0]),
                  Transform(w[9],gauges(.42,.48)),run_time=1.55,rate_func=linear)
        self.play(Indicate(leak,color=GOLD_GLUCOSE),run_time=.6)
        self.finish()


class S13Late(SpokenScene):
    def construct(self):
        w=world(gut_level=.42,particles=False,open_seal=True,proteins=True)
        self.add(w)
        late=T("late: gut < blood",30,GOLD_GLUCOSE).move_to([-2.9,3.28,0])
        self.play(FadeIn(late),Transform(w[9],gauges(.36,.48)),run_time=.9)
        self.at("leak runs backwards")
        leak=Arrow([GAPS[1],-1.15,0],[GAPS[1],1.05,0],color=GOLD_GLUCOSE,stroke_width=8,buff=0)
        leaklab=T("leak",28,GOLD_GLUCOSE).next_to(leak,RIGHT,buff=.15)
        self.play(GrowArrow(leak),FadeIn(leaklab),run_time=.9)
        self.at("Glucose slides back")
        dots=VGroup(*[glucose(GAPS[1]+dx,-2.55-.12*i,.12) for i,dx in enumerate((-.14,.12,-.05))])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.shift(UP*4.6) for d in dots],lag_ratio=.18),run_time=1.6,rate_func=linear)
        self.at("gut level stalls")
        self.play(Transform(w[9],gauges(.31,.48)),run_time=.9)
        floor_y=-.75+2.30*.31
        tick=Line([4.35,floor_y,0],[5.15,floor_y,0],color=GOLD_GLUCOSE,stroke_width=6)
        floor=T("floor",28,GOLD_GLUCOSE).next_to(tick,LEFT,buff=.12)
        self.play(Create(tick),FadeIn(floor),run_time=.7)
        self.at("cannot sink below")
        self.play(Indicate(tick,color=GOLD_GLUCOSE),bob(VGroup(),VGroup()) if False else Rotate(w[8][1][0][1],PI/2),run_time=.85)
        self.finish()


class S14Net(SpokenScene):
    def construct(self):
        w=world(gut_level=.31,particles=False,open_seal=True,proteins=True)
        self.add(w)
        self.at("Tighten the seal")
        self.play(Transform(w[4],VGroup(*[seal(x,False) for x in GAPS])),run_time=.85)
        self.at("floor drops")
        self.play(Transform(w[9],gauges(.14,.48)),run_time=1.05)
        self.at("what the sheet absorbs")
        carried=Arrow([CELL_X[1],1.25,0],[CELL_X[1],-1.25,0],color=GOLD_GLUCOSE,stroke_width=9,buff=0)
        self.play(GrowArrow(carried),run_time=.8)
        self.at("carries through the cells")
        d=glucose(CELL_X[1],2.4,.13)
        self.add(d)
        self.play(d.animate.move_to([CELL_X[1],-2.4,0]),run_time=1.05)
        self.at("minus what leaks back")
        cap=T("net = carried through − leaked back",34,TEXT).move_to([-1.0,2.78,0])
        cap_panel=RoundedRectangle(width=cap.width+.45,height=cap.height+.16,corner_radius=.10,
                                   stroke_width=0,fill_color=BG,fill_opacity=.92).move_to(cap)
        self.play(FadeIn(cap_panel),FadeIn(cap,shift=UP*.1),run_time=.7)
        self.play(Indicate(w[4],color=GREEN),run_time=.75)
        self.finish()


class S15Idea(SpokenScene):
    def construct(self):
        w=world(gut_level=.18,particles=False,proteins=True)
        self.add(w)
        idea=T("ONE IDEA",30,TEXT,weight=BOLD).move_to([-1.2,3.25,0])
        self.play(FadeIn(idea),run_time=.55)
        self.at("usual gut gradients")
        self.play(Transform(w[9],gauges(.28,.48)),run_time=.8)
        self.at("where the carrier sit")
        tops=VGroup(*[w[8][i][0] for i in range(3)])
        bases=VGroup(*[w[8][i][1] for i in range(3)],*[w[8][i][2] for i in range(3)])
        self.play(LaggedStart(*[Indicate(m,color=BLUE,scale_factor=1.18) for m in tops],lag_ratio=.15),run_time=.9)
        self.play(LaggedStart(*[Indicate(m,color=GOLD_GLUCOSE,scale_factor=1.15) for m in bases],lag_ratio=.10),run_time=.9)
        self.at("flow from gut to blood")
        ar=Arrow([CELL_X[1],1.15,0],[CELL_X[1],-1.15,0],color=GOLD_GLUCOSE,stroke_width=11,buff=0)
        lab=T("gut to blood",30,GOLD_GLUCOSE).next_to(ar,LEFT,buff=.15)
        self.play(GrowArrow(ar),FadeIn(lab),run_time=.9)
        self.at("The seal does not")
        self.play(LaggedStart(*[Indicate(s,color=GREEN,scale_factor=1.25) for s in w[4]],lag_ratio=.2),run_time=.85)
        self.at("what can slip between")
        jig=VGroup(glucose(GAPS[1]-.10,.65),sodium(GAPS[1]+.10,.35))
        self.add(jig)
        self.play(jig.animate.shift(UP*.18),run_time=.35)
        self.play(jig.animate.shift(DOWN*.18),run_time=.35)
        two=DoubleArrow([GAPS[1],-.30,0],[GAPS[1],.40,0],color=GREEN,stroke_width=6,buff=0)
        can=T("what can pass",28,GREEN).move_to([2.05,.72,0])
        self.play(GrowFromCenter(two),FadeIn(can),run_time=.8)
        self.at("what can leak back")
        self.play(Indicate(two,color=GREEN),jig.animate.shift(UP*.12),run_time=.8)
        self.finish()


class S16Handoff(SpokenScene):
    def construct(self):
        left=Rectangle(width=5.8,height=6.5,stroke_color=SLATE,stroke_width=5,fill_color=CELL_FILL,fill_opacity=.10).move_to([-3.1,-.1,0])
        right=left.copy().move_to([3.1,-.1,0])
        s=seal(0,False).scale(1.35)
        tag=chip("thought experiment",TEXT,size=28).move_to([2.0,2.5,0])
        self.add(left,right,s,tag)
        pan = VGroup(left, right, s)
        for m in (left, right, s):
            m.add_updater(lambda mob, dt: mob.shift(UP * .16 * dt))
        self.play(FadeOut(tag),run_time=.55)
        self.at("real seal lets through")
        self.play(Indicate(s,color=GREEN,scale_factor=1.25),run_time=.8)
        blocks=VGroup(*[Rectangle(width=.55,height=.22,stroke_width=0,fill_color=GREY,fill_opacity=.7).move_to([0,y,0])
                        for y in (.15,-.65,-1.45,-2.35)])
        for b in blocks:
            b.add_updater(lambda mob, dt: mob.shift(UP * .16 * dt))
        self.play(LaggedStart(*[FadeIn(b,shift=DOWN*.15) for b in blocks],lag_ratio=.20),run_time=.75)
        self.at("how it is measured")
        self.play(VGroup(left,right,s,blocks).animate.shift(UP*.45),run_time=.8)
        self.at("text below")
        line=T("The real seal: in the text below",36,TEXT).move_to([0,3.12,0]).set_z_index(20)
        line_panel=RoundedRectangle(width=line.width+.55,height=line.height+.22,corner_radius=.10,
                                    stroke_width=0,fill_color=BG,fill_opacity=.94).move_to(line).set_z_index(19)
        self.play(FadeIn(line_panel),FadeIn(line,shift=DOWN*.1),run_time=.65)
        self.play(blocks.animate.shift(DOWN*.15),run_time=.55)
        self.finish()


class S17End(EndCard):
    LINE = "Usual gut gradients: carrier placement biases glucose flow toward blood."

    def construct(self):
        w = world(gut_level=.16, particles=False, proteins=True)
        w.set_opacity(.24)
        self.add(w)
        line = T("Usual gut gradients:\ncarrier placement biases glucose flow toward blood.", 40, TEXT,
                 font=TITLE_FONT, line_spacing=.85)
        fit(line, max_w=11.3)
        panel = RoundedRectangle(width=line.width + .8, height=line.height + .65, corner_radius=.16,
                                 stroke_width=0, fill_color=BG, fill_opacity=.82).move_to(line)
        self.play(FadeIn(panel), FadeIn(line, shift=UP*.10), run_time=.75)
        drift = VGroup(*[glucose(x, y, .09) for x, y in [(-4.2,2.7),(-2.8,2.9),(-1.2,2.65),(.3,2.85),(1.9,2.65)]])
        drift.set_opacity(.55)
        self.add(drift)
        self.play(drift.animate.shift(DOWN*.35), run_time=1.6, rate_func=linear)
        self.finish()

