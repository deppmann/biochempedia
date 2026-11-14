"""Why a White Coat Can Help—and Hurt.

COLOR MAP (kept for the whole film)
  GREEN  matched condition / helps
  RED    mismatch / cost
  BLUE   inherited variation
  YELLOW population and time
  WHITE  snow and winter coat
  BROWN  bare ground and summer coat

All animals and settings are explicitly tagged schematic.  The hillside, hare, and eye are
rebuilt only through the builders below, at the same scale and coordinates in every scene.
"""
from bp_parts import *

BROWN = "#7A5237"
DARK_BROWN = "#443126"
SNOW = "#E8F1F7"
SKY = "#172638"
INK = "#18212D"
ORANGE = "#F29E4C"


def hare(coat=WHITE, at=(0, -1.28, 0), scale=1.0, edge=GREY):
    """Large, simple snowshoe-hare cartoon; feet land at local y=0."""
    body = Ellipse(2.65, 1.42, fill_color=coat, fill_opacity=1, stroke_color=edge, stroke_width=4)
    body.move_to([-0.25, 0.93, 0])
    chest = Circle(0.62, fill_color=coat, fill_opacity=1, stroke_color=edge, stroke_width=4).move_to([1.05, 1.35, 0])
    head = Circle(0.50, fill_color=coat, fill_opacity=1, stroke_color=edge, stroke_width=4).move_to([1.42, 1.82, 0])
    ears = VGroup(
        Ellipse(0.25, 1.05, fill_color=coat, fill_opacity=1, stroke_color=edge, stroke_width=4).rotate(-0.16).move_to([1.25, 2.58, 0]),
        Ellipse(0.25, 1.00, fill_color=coat, fill_opacity=1, stroke_color=edge, stroke_width=4).rotate(0.13).move_to([1.57, 2.55, 0]),
    )
    back_foot = RoundedRectangle(0.18, width=1.35, height=0.34, fill_color=coat, fill_opacity=1,
                                 stroke_color=edge, stroke_width=4).move_to([-0.88, 0.18, 0])
    front_foot = RoundedRectangle(0.14, width=0.58, height=0.28, fill_color=coat, fill_opacity=1,
                                  stroke_color=edge, stroke_width=4).move_to([0.88, 0.14, 0])
    tail = Circle(0.31, fill_color=coat, fill_opacity=1, stroke_color=edge, stroke_width=4).move_to([-1.58, 1.20, 0])
    eye = Dot([1.60, 1.92, 0], radius=0.065, color=INK)
    g = VGroup(tail, body, chest, ears, back_foot, front_foot, head, eye).scale(scale)
    g.move_to(np.array(at) + UP * g.height / 2)
    g.coat_parts = VGroup(tail, body, chest, ears, back_foot, front_foot, head)
    g.back_foot = back_foot
    return g


def predator_eye(at=(4.9, 1.65, 0), scale=1.0):
    outline = Intersection(Circle(0.72), Circle(0.72).shift(RIGHT * 0.78)).set_fill(BG, 1).set_stroke(RED, 5)
    outline.rotate(PI / 2).scale(scale).move_to(at)
    pupil = Dot(at, radius=0.15 * scale, color=RED)
    sight = DashedLine(np.array(at) + DOWN * 0.55, [0.9, -0.25, 0], color=RED, stroke_width=3,
                       dash_length=0.14).set_opacity(0.55)
    return VGroup(sight, outline, pupil)


def hillside(snow_fraction=0.5):
    """The carried landscape. snow_fraction is the fraction of the ground covered from the left."""
    sky = Rectangle(width=13.4, height=5.6, fill_color=SKY, fill_opacity=1, stroke_width=0).move_to([0, 0.85, 0])
    ground = Rectangle(width=13.4, height=2.35, fill_color=BROWN, fill_opacity=1, stroke_width=0).move_to([0, -2.52, 0])
    ridge = VMobject(stroke_color=DARK_BROWN, stroke_width=6).set_points_as_corners([
        [-6.7, -1.55, 0], [-4.7, -1.15, 0], [-2.5, -1.52, 0], [-0.3, -1.18, 0],
        [2.0, -1.52, 0], [4.4, -1.12, 0], [6.7, -1.48, 0]])
    world = VGroup(sky, ground, ridge)
    if snow_fraction > 0:
        width = 13.4 * snow_fraction
        snow = Rectangle(width=width, height=2.35, fill_color=SNOW, fill_opacity=1, stroke_width=0)
        snow.move_to([-6.7 + width / 2, -2.52, 0])
        world.add(snow)
        snowy_ridge = Line([-6.7, -1.55, 0], [-6.7 + width, -1.28, 0], color=SNOW, stroke_width=9)
        world.add(snowy_ridge)
    return world


def world_with_hare(snow_fraction=0.5, coat=WHITE, x=0, eye=True, hare_scale=1.0):
    w = hillside(snow_fraction)
    h = hare(coat, at=(x, -1.55, 0), scale=hare_scale)
    parts = VGroup(w, h)
    parts.world, parts.hare = w, h
    if eye:
        e = predator_eye()
        parts.add(e)
        parts.eye = e
    return parts


def match_ring(h, color=GREEN):
    return Ellipse(h.width + 0.30, h.height + 0.24, color=color, stroke_width=8).move_to(h)


def cloud(x, y, s=1):
    return VGroup(Circle(.25), Circle(.34).shift(RIGHT*.30), Circle(.24).shift(RIGHT*.62)).set_fill(GREY, .55).set_stroke(width=0).scale(s).move_to([x, y, 0])


def leaf(x, y, color=ORANGE):
    return Ellipse(.20, .42, fill_color=color, fill_opacity=1, stroke_width=0).rotate(.55).move_to([x, y, 0])


def butterfly(color=ORANGE, scale=.55):
    wings = VGroup(Ellipse(.55, .34), Ellipse(.55, .34)).arrange(RIGHT, buff=-.06).set_fill(color, .85).set_stroke(color, 2)
    body = Line(DOWN*.25, UP*.25, color=INK, stroke_width=5)
    return VGroup(wings, body).scale(scale)


def turtle(scale=1.0):
    shell = ArcBetweenPoints(LEFT*1.25, RIGHT*1.25, angle=-PI).set_stroke(GREEN, 9)
    base = Line(LEFT*1.22, RIGHT*1.22, color=GREEN, stroke_width=9)
    head = Circle(.24, color=GREEN, fill_color=GREEN, fill_opacity=.3).move_to([1.45, .03, 0])
    feet = VGroup(*[Line([x, -.05, 0], [x-.08, -.40, 0], color=GREEN, stroke_width=7) for x in (-.72, .68)])
    return VGroup(shell, base, head, feet).scale(scale)


def balance(center=(0, .2, 0), color=YELLOW):
    c = np.array(center)
    beam = Line(c + LEFT*2.2, c + RIGHT*2.2, color=color, stroke_width=8)
    stem = Line(c + DOWN*1.25, c, color=color, stroke_width=7)
    foot = Line(c + DOWN*1.25 + LEFT*.7, c + DOWN*1.25 + RIGHT*.7, color=color, stroke_width=7)
    pans = VGroup(ArcBetweenPoints(c+LEFT*2.5+DOWN*.7, c+LEFT*1.9+DOWN*.7, angle=PI),
                  ArcBetweenPoints(c+RIGHT*1.9+DOWN*.7, c+RIGHT*2.5+DOWN*.7, angle=PI)).set_stroke(color, 5)
    strings = VGroup(*[Line(c+[x, 0, 0], c+[x + (.30 if x < 0 else -.30), -.7, 0], color=color, stroke_width=3)
                       for x in (-2.2, 2.2)])
    return VGroup(stem, foot, beam, strings, pans)


def schematic_tag():
    return scope_tag("schematic")


class S00Hook(SpokenScene):
    def construct(self):
        w = world_with_hare(.5, WHITE, 0, True, 1.12)
        q = fit_text("How can one white coat help—and hurt?", 10.8, 42, YELLOW).move_to([0, 3.15, 0])
        self.play(FadeIn(w.world), FadeIn(w.hare, shift=UP*.15), run_time=.8)
        bob(w.hare, .06, 1.5)
        self.at("same white coat")
        self.play(FadeIn(w.eye), Write(q), run_time=.8)
        self.at("put it in danger")
        self.play(w.hare.animate.shift(RIGHT*1.6), run_time=1.2)
        self.at("Montana hillside")
        self.play(w.hare.animate.shift(LEFT*3.2), w.eye.animate.shift(LEFT*.5), run_time=1.4)
        self.add(schematic_tag())
        self.at("around one")
        self.play(w.hare.animate.shift(RIGHT*1.6), run_time=.9)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = world_with_hare(.5, WHITE, 0, False, .92)
        veil = Rectangle(width=13.4, height=7.0, fill_color=BG, fill_opacity=.34, stroke_width=0)
        title = fit_text("Why a White Coat Can Help—and Hurt", 11.4, 48, TEXT, font=TITLE_FONT).move_to([0, 2.55, 0])
        rule = Line(LEFT*1.4, RIGHT*1.4, color=GOLD, stroke_width=5).next_to(title, DOWN, .22)
        leaves = VGroup(*[leaf(-5.6+i*1.8, 2.1+(i%2)*.5) for i in range(7)])
        self.add(w, veil)
        self.play(Write(title), GrowFromCenter(rule), leaves.animate.shift(DOWN*2.2+RIGHT*.7), run_time=1.5)
        self.finish()


class S02Fall(SpokenScene):
    def construct(self):
        w = world_with_hare(0, BROWN, 0, False, 1.12)
        leaves = VGroup(*[leaf(-5.5+i*1.35, -1.55+(i%3)*.14, ORANGE if i%2 else GOLD) for i in range(9)])
        shadows = VGroup(*[Line([x, -1.5, 0], [x+.7, -3.6, 0], color=DARK_BROWN, stroke_width=15).set_opacity(.48) for x in (-4,-1,2,5)])
        self.at("Begin in fall")
        self.play(FadeIn(w.world), FadeIn(leaves), run_time=.7)
        self.at("ground is brown")
        self.play(FadeIn(w.hare, shift=RIGHT*.2), FadeIn(shadows), run_time=.8)
        ring = match_ring(w.hare)
        self.at("hare is brown")
        self.play(Create(ring), w.hare.animate.shift(RIGHT*.65), run_time=1.0)
        tag = chip("match", GREEN, 30).move_to([-4.7, 1.7, 0])
        self.at("outline blends")
        self.play(FadeIn(tag), FadeOut(ring), shadows.animate.shift(RIGHT*.4), run_time=1.3)
        scene_tag = schematic_tag().shift(LEFT*.75)
        self.add(scene_tag)
        self.at("tree shadows")
        self.play(w.hare.animate.shift(LEFT*.65), leaves.animate.shift(RIGHT*.8), run_time=1.0)
        self.finish()


class S03Feet(SpokenScene):
    def construct(self):
        base = hillside(0)
        snow = hillside(1)
        h = hare(BROWN, at=(0, -1.55, 0), scale=1.08)
        self.add(base, h)
        self.at("snow covers")
        self.play(ReplacementTransform(base, snow), h.coat_parts.animate.set_fill(WHITE), run_time=1.3)
        self.at("large back feet")
        foot = RoundedRectangle(.22, width=4.3, height=1.05, fill_color=WHITE, fill_opacity=1, stroke_color=BLUE, stroke_width=6).move_to([0, .4, 0])
        print1 = Ellipse(4.1, .55, color=BLUE, stroke_width=5).move_to([0, -1.55, 0])
        lab = T("large feet", 34, BLUE).move_to([0, 2.05, 0])
        self.play(FadeOut(h), FadeIn(foot, shift=DOWN*.2), Create(print1), FadeIn(lab), run_time=1.1)
        self.at("spread its weight")
        self.play(foot.animate.shift(DOWN*.35).scale(1.05), print1.animate.scale(1.10), run_time=1.3)
        fur = VGroup(*[Line([x,-.05,0],[x+.10,-.50,0],color=GOLD,stroke_width=4) for x in np.linspace(-1.6,1.6,11)]).move_to(foot)
        fur_lab = T("fur underneath", 32, GOLD).move_to([3.9, .35, 0])
        arrow = Arrow(fur_lab.get_left(), [1.7,.0,0], buff=.15, color=GOLD, stroke_width=5)
        self.at("Fur underneath")
        self.play(FadeIn(fur), GrowArrow(arrow), FadeIn(fur_lab), run_time=1.0)
        self.add(schematic_tag())
        self.at("feet warm")
        self.play(foot.animate.shift(UP*.25), fur.animate.shift(UP*.25), run_time=.9)
        self.finish()


class S04Coat(SpokenScene):
    def construct(self):
        w = world_with_hare(1, BROWN, 0, True, 1.12)
        self.add(w.world, w.hare)
        self.at("grows white")
        self.play(w.hare.coat_parts.animate.set_fill(WHITE), run_time=1.8)
        ring = match_ring(w.hare)
        self.at("This coloring")
        self.play(Create(ring), run_time=.7)
        cam = chip("camouflage", GREEN, 34).move_to([-4.7, 1.9, 0])
        self.at("is camouflage")
        self.play(FadeIn(cam), FadeOut(ring), run_time=.8)
        self.at("blend into")
        self.play(w.hare.animate.shift(LEFT*.8), run_time=1.2)
        self.at("never makes")
        self.play(FadeIn(w.eye), w.eye.animate.shift(LEFT*.55), run_time=.9)
        self.add(schematic_tag())
        self.at("invisible")
        self.play(Indicate(w.hare, color=RED, scale_factor=1.04), run_time=.8)
        self.finish()


def predict_backdrop():
    w = world_with_hare(.5, WHITE, 0, False, .96)
    clouds = VGroup(cloud(-4.7, 2.25), cloud(-2.8, 2.55, .8))
    return VGroup(w, clouds, schematic_tag())


class S05Predict(SpokenScene):
    QUESTION = "When snow disappears, is the hare harder or easier to spot?"
    OPTIONS = ["harder", "easier"]

    def construct(self):
        full = world_with_hare(1, WHITE, 0, False, .96)
        self.add(full, schematic_tag())
        self.at("Spring comes early")
        warm = VGroup(*[Arrow([-6+i*.8,2.2,0],[-4.9+i*.8,2.2,0],color=GOLD,stroke_width=4,tip_length=.18) for i in range(5)])
        self.play(FadeIn(warm), run_time=.5)
        self.at("snow disappears")
        half = predict_backdrop()
        self.play(FadeOut(warm), ReplacementTransform(full, half[0]), FadeIn(half[1]), run_time=1.2)
        q = question_card(self.QUESTION, self.OPTIONS, color=YELLOW, chips_at=[4.7, .25, 0], y=3.2)
        q.chips[0][0].set_stroke(GREEN); q.chips[0][1].set_color(GREEN)
        q.chips[1][0].set_stroke(RED); q.chips[1][1].set_color(RED)
        self.at("harder or easier")
        self.play(FadeIn(q.chips), FadeIn(q.question), run_time=.9)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = S05Predict.QUESTION
    OPTIONS = S05Predict.OPTIONS
    CHIPS_AT = [4.7, .25, 0]
    CARD = {"y": 3.2}
    RING_AT = (6.0, -2.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop()


class S07Reveal(SpokenScene):
    def construct(self):
        w = world_with_hare(.5, WHITE, 0, True, 1.04)
        self.add(w, schematic_tag())
        self.at("bare ground returns")
        bare = hillside(0)
        self.play(ReplacementTransform(w.world, bare), run_time=1.3)
        ring = match_ring(w.hare, RED)
        self.at("stands out")
        self.play(Create(ring), run_time=.6)
        self.at("predator can notice")
        self.play(w.eye.animate.shift(LEFT*.8), run_time=.9)
        good = chip("helps on snow", GREEN, 30).move_to([-4.5, 1.8, 0])
        cost = chip("costs on bare ground", RED, 30).move_to([-4.1, 1.8, 0])
        self.at("helpful winter coat")
        self.play(FadeIn(good), w.hare.animate.shift(RIGHT*.35), run_time=.8)
        self.at("carries a cost")
        self.play(swap(good, cost), ring.animate.set_stroke(width=11), run_time=1.0)
        self.finish()


class S08Define(SpokenScene):
    def construct(self):
        adult = hare(WHITE, at=(-3.8,-1.55,0), scale=.9, edge=BLUE)
        young = VGroup(hare(WHITE, at=(.1,-1.55,0), scale=.55, edge=BLUE), hare(BROWN, at=(2.2,-1.55,0), scale=.55, edge=BLUE))
        self.add(hillside(.55), adult, schematic_tag())
        self.at("inherited trait")
        arrows = VGroup(Arrow([-2.3,.0,0],[-.6,.0,0],color=BLUE,stroke_width=6), Arrow([-2.3,-.4,0],[1.5,-.4,0],color=BLUE,stroke_width=6))
        inherited = chip("inherited", BLUE, 32).move_to([0, 2.15, 0])
        self.play(FadeIn(inherited), GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(young), run_time=1.2)
        helps = chip("helps survival + reproduction", GREEN, 30).move_to([2.9, 1.25, 0])
        self.at("helps survival")
        self.play(FadeIn(helps), young.animate.shift(RIGHT*.25), run_time=.9)
        bracket = Brace(adult, DOWN, color=TEAL)
        physical = T("physical: body feature", 32, TEAL).next_to(bracket, DOWN, .18)
        self.at("coat and feet")
        self.play(GrowFromCenter(bracket), FadeIn(physical), Indicate(adult, color=TEAL), run_time=1.0)
        self.at("physical adaptations")
        self.play(adult.animate.shift(UP*.12), young.animate.shift(UP*.12), run_time=.8)
        self.finish()


class S09Behaviour(SpokenScene):
    def construct(self):
        tp = TwoPanel("physical: body feature", "behavioral: action", colors=(TEAL, ORANGE))
        h = hare(WHITE, scale=.62)
        tp.put(h, "left")
        self.add(tp, h, schematic_tag())
        self.at("action or pattern")
        path = CubicBezier([-1.0,1.4,0],[.6,2.0,0],[2.5,-.1,0],[5.2,-1.4,0]).set_stroke(YELLOW, 6)
        self.play(Create(path), run_time=1.2)
        bugs = VGroup(*[butterfly(scale=.75).move_to(path.point_from_proportion(p)) for p in (.05,.2,.35)])
        self.at("Migration is")
        self.play(FadeIn(bugs), run_time=.5)
        self.at("regular journey")
        self.play(bugs.animate.shift(path.get_end()-path.get_start()), run_time=2.5, rate_func=linear)
        season1 = T("fall", 30, YELLOW).move_to([1.4,2.0,0])
        season2 = T("winter", 30, YELLOW).move_to([5.0,-1.7,0])
        self.at("different seasons")
        self.play(FadeIn(season1), FadeIn(season2), run_time=.7)
        action = chip("does something", ORANGE, 30).move_to([4.65, .85, 0])
        self.at("animal does something")
        self.play(FadeIn(action), FadeOut(bugs), FadeOut(path), FadeOut(season1), FadeOut(season2), run_time=.8)
        self.at("rather than")
        self.play(Indicate(h, color=TEAL), Indicate(path, color=ORANGE), run_time=1.0)
        self.finish()


class S09bPhysical(SpokenScene):
    def construct(self):
        tp = TwoPanel("heron: long legs", "turtle: shell", colors=(TEAL, GREEN))
        self.add(tp, schematic_tag())
        heron = VGroup(Line(DOWN*1.65, UP*.7, color=TEAL, stroke_width=10), Line([.35,-1.65,0],[.35,.7,0],color=TEAL,stroke_width=10),
                       Ellipse(.9,1.1,color=TEAL,fill_color=TEAL,fill_opacity=.25).move_to([.15,1.0,0]),
                       Line([.15,1.55,0],[.15,2.05,0],color=TEAL,stroke_width=8),
                       Arrow([.15,2.05,0],[1.2,1.85,0],color=TEAL,stroke_width=6,tip_length=.2))
        tp.put(heron,"left")
        tur = turtle(1.25); tp.put(tur,"right")
        self.at("different jobs")
        self.play(FadeIn(heron), FadeIn(tur), run_time=.8)
        water = Rectangle(width=5.5,height=1.0,fill_color=BLUE,fill_opacity=.28,stroke_width=0).move_to([-3.25,-1.85,0])
        fish = VGroup(Triangle(fill_color=BLUE,fill_opacity=.7,stroke_width=0).scale(.2), Line([.1,0,0],[.6,0,0],color=BLUE,stroke_width=7)).move_to([-4.2,-1.6,0])
        self.at("deeper water")
        self.play(FadeIn(water,shift=UP*.7), fish.animate.shift(RIGHT*1.4), run_time=1.5)
        soft = Ellipse(1.5,.65,fill_color=RED,fill_opacity=.4,stroke_color=RED,stroke_width=3).move_to([3.25,-.2,0])
        self.at("soft body")
        self.play(FadeIn(soft), tur.animate.shift(UP*.28), run_time=.8)
        self.at("from predators")
        self.play(tur.animate.shift(DOWN*.28), FadeOut(soft), run_time=1.0)
        self.finish()


class S09cHibernation(SpokenScene):
    def construct(self):
        world = hillside(1)
        burrow = ArcBetweenPoints([-3.3,-2.0,0],[3.3,-2.0,0],angle=-PI).set_stroke(BROWN,12)
        groundhog = VGroup(Ellipse(2.5,1.35,fill_color=BROWN,fill_opacity=1,stroke_color=TEXT,stroke_width=4), Circle(.46,fill_color=BROWN,fill_opacity=1,stroke_color=TEXT,stroke_width=4).shift(RIGHT*1.0+UP*.3))
        groundhog.move_to([0,-2.35,0])
        self.add(world, burrow, groundhog, schematic_tag())
        self.at("deeply inactive")
        bob(groundhog,.05,.65)
        self.play(groundhog.animate.scale(.86), run_time=1.2)
        heart = T("♥", 62, RED).move_to([-4.55,1.55,0])
        rate = ValueTracker(72)
        beat_read = counter("heart {:.0f}", rate, [-4.55,.9,0], 30, RED)
        temp = ValueTracker(37)
        temp_read = counter("body {:.0f}°", temp, [3.9,-.1,0], 30, BLUE)
        self.at("heart slows")
        self.add(beat_read); self.play(FadeIn(heart), rate.animate.set_value(8), run_time=1.6)
        self.at("body cools")
        self.add(temp_read); self.play(temp.animate.set_value(12), run_time=1.5)
        both = VGroup(chip("behavior", ORANGE, 30), chip("body function", BLUE, 30)).arrange(RIGHT,.4).move_to([0,2.3,0])
        self.at("behavior plus")
        self.play(FadeIn(both), groundhog.animate.scale(1.07), run_time=.9)
        self.at("inside the body")
        self.play(heart.animate.scale(.82), run_time=.8)
        self.finish()


class S10Tradeoff(SpokenScene):
    def construct(self):
        w = world_with_hare(.5, WHITE, -3.0, False, .92)
        bal = balance((0,2.2,0)).scale(.55)
        title = T("trade-off", 38, YELLOW).move_to([0,3.2,0])
        good = chip("helps", GREEN, 30).move_to([-4.2,.45,0])
        cost = chip("costs", RED, 30).move_to([4.8,2.05,0])
        self.add(w, bal, title, schematic_tag())
        self.at("helps in one way")
        self.play(FadeIn(good), w.hare.animate.shift(LEFT*.5), bal.animate.rotate(.12), run_time=1.1)
        self.at("costs in another")
        self.play(FadeIn(cost), w.hare.animate.shift(RIGHT*6.9), bal.animate.rotate(-.24), run_time=1.4)
        self.at("white coat works")
        self.play(w.hare.animate.shift(LEFT*6.9), bal.animate.rotate(.24), run_time=1.2)
        self.at("background fits")
        ring = match_ring(w.hare,GREEN)
        self.play(Create(ring), run_time=.7)
        self.finish()


class S10bCosts(SpokenScene):
    def construct(self):
        w = hillside(.65)
        bal = balance((0,.9,0)).scale(1.15)
        shell = turtle(.72).move_to([-2.55,.7,0])
        weight = VGroup(Rectangle(width=1.3,height=.9,fill_color=RED,fill_opacity=.35,stroke_color=RED,stroke_width=5), T("heavy",28,RED)).move_to([2.55,-.9,0])
        self.add(w, bal, schematic_tag())
        self.at("protective shell")
        self.play(FadeIn(shell), bal.animate.rotate(.10), run_time=1.0)
        self.at("heavy to carry")
        self.play(FadeIn(weight), bal.animate.rotate(-.22), run_time=1.2)
        nofit = chip("no perfect fit", YELLOW, 36).move_to([0,2.75,0])
        self.at("perfectly adapted")
        self.play(FadeIn(nofit), bal.animate.rotate(.14), run_time=.9)
        bare = hillside(0)
        self.at("Conditions change")
        self.play(ReplacementTransform(w,bare), bal.animate.rotate(-.08), run_time=1.3)
        self.at("bring a cost")
        self.play(weight.animate.shift(RIGHT*.3), shell.animate.shift(UP*.15), run_time=.9)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        h = hare(WHITE, at=(-4.0,-1.55,0), scale=.9)
        world = hillside(0)
        rule = fit_text("Adaptations help in particular settings", 7.3, 36, GREEN).move_to([1.7,2.35,0])
        self.add(world,h,schematic_tag())
        self.at("particular settings")
        self.play(FadeIn(rule), h.animate.shift(RIGHT*.2), run_time=1.0)
        line = Arrow([-2.5,-.35,0],[5.3,-.35,0],color=YELLOW,stroke_width=7,tip_length=.25)
        generations = T("generations",32,YELLOW).next_to(line,UP,.2)
        self.at("populations change")
        self.play(GrowArrow(line), FadeIn(generations), run_time=1.2)
        group = VGroup(*[hare(WHITE if i%2 else BROWN, scale=.34) for i in range(5)]).arrange(RIGHT,.2).move_to([2.8,-1.3,0])
        self.at("over generations")
        self.play(FadeIn(group,shift=RIGHT*.3), run_time=1.0)
        one = chip("one hare", BLUE, 30).move_to([-4.5,1.0,0])
        self.at("One hare")
        self.play(FadeIn(one), Indicate(h,color=BLUE), run_time=.8)
        no = T("cannot choose a new coat",32,RED).move_to([1.3,1.35,0])
        self.at("cannot choose")
        self.play(FadeIn(no), h.animate.shift(LEFT*.2), run_time=1.0)
        self.at("snow vanished")
        self.play(group.animate.shift(RIGHT*.35), line.animate.set_stroke(width=10), run_time=1.0)
        self.finish()


def timeline_world():
    world = hillside(.25)
    line = Arrow([-5.6,-.2,0],[5.7,-.2,0],color=YELLOW,stroke_width=7,tip_length=.25)
    spring = Line([0,-1.0,0],[0,1.1,0],color=GOLD,stroke_width=7)
    spring_lab = T("spring",30,GOLD).next_to(spring,UP,.14)
    return VGroup(world,line,spring,spring_lab)


class S12Variation(SpokenScene):
    def construct(self):
        tw = timeline_world()
        hs = VGroup(*[hare(BROWN,scale=.42) for _ in range(4)])
        for h,x in zip(hs,(-4.3,-1.6,1.1,3.8)): h.move_to([x,-1.45,0])
        self.add(tw,schematic_tag())
        self.at("not identical")
        self.play(FadeIn(hs,shift=UP*.2), run_time=.9)
        ticks = VGroup(*[Line([x,-.55,0],[x,.15,0],color=BLUE,stroke_width=7) for x in (-2.8,-1.0,.7,2.5)])
        self.at("changing color earlier")
        self.play(Create(ticks), hs[0].coat_parts.animate.set_fill(WHITE), run_time=1.2)
        self.at("others")
        self.play(hs[1].coat_parts.animate.set_fill(WHITE), hs.animate.shift(RIGHT*.35), run_time=1.1)
        tag = chip("variation",BLUE,36).move_to([0,2.25,0])
        self.at("are variation")
        self.play(FadeIn(tag), hs[2].coat_parts.animate.set_fill(WHITE), run_time=.9)
        self.at("seasons shift")
        self.play(hs.animate.shift(LEFT*.7), ticks.animate.shift(LEFT*.7), run_time=1.5, rate_func=linear)
        self.finish()


class S12bPlaces(SpokenScene):
    def construct(self):
        tp = TwoPanel("snowy hillside", "low-snow hillside", colors=(BLUE,BROWN))
        left_ground = Rectangle(width=5.6,height=2.0,fill_color=SNOW,fill_opacity=1,stroke_width=0)
        right_ground = Rectangle(width=5.6,height=2.0,fill_color=BROWN,fill_opacity=1,stroke_width=0)
        tp.put(left_ground,"left"); tp.put(right_ground,"right")
        lh = hare(WHITE,scale=.65); rh = hare(BROWN,scale=.65)
        tp.put(lh,"left"); lh.shift(DOWN*.65)
        tp.put(rh,"right"); rh.shift(DOWN*.65)
        self.add(tp,left_ground,right_ground,schematic_tag())
        self.at("across places")
        self.play(FadeIn(lh), FadeIn(rh), run_time=.8)
        self.at("little snow")
        self.play(rh.animate.shift(RIGHT*.35), run_time=1.0)
        self.at("stay brown")
        rr = match_ring(rh,GREEN)
        self.play(Create(rr), run_time=.7)
        self.at("winter")
        lr = match_ring(lh,GREEN)
        self.play(Create(lr), lh.animate.shift(LEFT*.35), run_time=.8)
        lab = chip("different places",BLUE,32).move_to([0,-3.15,0])
        self.at("depends on the setting")
        self.play(FadeIn(lab), lr.animate.set_stroke(width=10), rr.animate.set_stroke(width=10), run_time=1.0)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        world = hillside(0)
        coats = (WHITE,"#D9D5CF","#B9A58F",BROWN)
        hs = VGroup(*[hare(c,scale=.53) for c in coats]).arrange(RIGHT,.42).move_to([-1.3,-1.25,0])
        self.add(world,hs,schematic_tag())
        self.at("hide or expose")
        rings = VGroup(*[match_ring(h,RED if i<2 else GREEN) for i,h in enumerate(hs)])
        self.play(Create(rings), hs.animate.shift(RIGHT*.25), run_time=1.2)
        collar = Circle(.30,color=BLUE,stroke_width=7).move_to(hs[1].get_center()+DOWN*.1)
        self.at("field evidence")
        self.play(Create(collar), run_time=.6)
        signal = VGroup(*[Arc(radius=r,start_angle=-.5,angle=1.0,arc_center=collar.get_center()+RIGHT*.15,color=BLUE,stroke_width=5) for r in (.55,.9,1.25)])
        data = RoundedRectangle(.18,width=3.4,height=2.2,stroke_color=YELLOW,stroke_width=4,fill_color=BG,fill_opacity=.86).move_to([4.5,1.25,0])
        data_lab = T("field data",32,YELLOW).move_to(data.get_center()+UP*.55)
        blanks = VGroup(*[Line([3.55,y,0],[5.45,y,0],color=GREY,stroke_width=4) for y in (1.25,.75)])
        self.at("mismatch changes survival")
        self.play(Create(signal), FadeIn(data), FadeIn(data_lab), Create(blanks), run_time=1.3)
        pop = T("population",32,YELLOW).move_to([0,2.5,0])
        self.at("across the population")
        self.play(FadeIn(pop), rings.animate.set_stroke(width=9), run_time=.8)
        unknown = fit_text("one death: cause unknown",2.8,28,GREY,max_lines=2).move_to([4.5,.75,0])
        self.at("cannot tell us")
        self.play(FadeIn(unknown), FadeOut(signal), FadeOut(data_lab), FadeOut(blanks), run_time=1.0)
        self.at("any one death")
        self.play(Indicate(unknown,color=GREY), hs.animate.shift(LEFT*.25), run_time=.8)
        self.finish()


class S14End(EndCard):
    LINE = "Adaptations help in particular settings;\npopulations change over generations, not individuals."
