"""When Ecosystems Change Course — chapter 2.

COLOR MAP (continued exactly from chapter 1)
  BLUE   = Bay water, rain
  YELLOW = nutrients
  GREEN  = plants and habitat
  GREY   = inactive matter, structure, small notes
  ORANGE = bacteria / warm conditions
  TEAL   = dissolved oxygen
  RED    = disturbances and harmful pressure
  BROWN  = land
  TEXT   = animals and plain labels
  GOLD   = one guiding idea / emphasis
"""
from bp_parts import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BROWN = "#A8825A"


def arrow(a, b, color=GREY, width=5, tip=0.18):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=width, tip_length=tip)


def pine(x, y, height=1.15, color=GREEN):
    trunk = Line([x, y, 0], [x, y + height * 0.58, 0], color=BROWN, stroke_width=5)
    crown = Polygon([x, y + height, 0], [x - height * 0.32, y + height * 0.35, 0],
                    [x + height * 0.32, y + height * 0.35, 0], stroke_color=color,
                    fill_color=color, fill_opacity=0.72, stroke_width=2)
    return VGroup(trunk, crown)


def animal(x, y, scale=1.0, color=TEXT):
    body = Ellipse(width=0.48 * scale, height=0.25 * scale, color=color,
                   fill_color=color, fill_opacity=0.68, stroke_width=2).move_to([x, y, 0])
    head = Dot([x + 0.28 * scale, y + 0.08 * scale, 0], radius=0.1 * scale, color=color)
    return VGroup(body, head)


def seed(x, y, scale=1.0):
    return Ellipse(width=0.18 * scale, height=0.34 * scale, color=GREY,
                   fill_color=GREY, fill_opacity=0.72, stroke_width=2).rotate(-0.5).move_to([x, y, 0])


def flame(x, y, scale=1.0):
    return Polygon([x, y, 0], [x - 0.22 * scale, y + 0.42 * scale, 0],
                   [x - 0.05 * scale, y + 0.34 * scale, 0], [x + 0.05 * scale, y + 0.72 * scale, 0],
                   [x + 0.24 * scale, y + 0.3 * scale, 0], color=RED,
                   fill_color=RED, fill_opacity=0.78, stroke_width=2)


def add_drift(mob, vx=0.035, lo=-6.2, hi=6.2):
    def drift(m, dt):
        m.shift(RIGHT * vx * dt)
        if m.get_left()[0] > hi:
            m.shift(LEFT * (hi - lo + m.width))
    mob.add_updater(drift)
    return mob


def add_sway(mob, amp=0.035, speed=1.7, phase=0.0):
    mob._sway_t = phase
    base = mob.get_center().copy()
    def sway(m, dt):
        m._sway_t += dt
        m.move_to(base + RIGHT * amp * np.sin(speed * m._sway_t))
    mob.add_updater(sway)
    return mob


def landscape(opacity=1.0, labels=True):
    """The carried world; every continuing scene calls this at identical scale and position."""
    ground = VMobject(color=BROWN, stroke_width=5, fill_color=BROWN, fill_opacity=0.25)
    ground.set_points_as_corners([[-6.5, -1.4, 0], [-4.4, -1.0, 0], [-2.8, -0.55, 0],
                                  [-1.3, -0.2, 0], [0.1, 0.35, 0], [1.8, -0.05, 0],
                                  [3.4, -0.8, 0], [6.5, -1.25, 0], [6.5, -2.65, 0],
                                  [-6.5, -2.65, 0], [-6.5, -1.4, 0]])
    sea = Polygon([-6.5, -1.4, 0], [-4.4, -1.0, 0], [-3.0, -0.56, 0],
                  [-3.0, -2.65, 0], [-6.5, -2.65, 0], color=BLUE,
                  fill_color=BLUE, fill_opacity=0.28, stroke_width=3)
    sea._shimmer_t = 0.0
    def shimmer(m, dt):
        m._shimmer_t += dt
        m.set_fill(BLUE, opacity=.25 + .09 * (1 + np.sin(1.8 * m._shimmer_t)) / 2)
    sea.add_updater(shimmer)
    stream = VMobject(color=BLUE, stroke_width=12)
    stream.set_points_smoothly([[6.3, -0.92, 0], [5.4, -1.1, 0], [4.6, -1.35, 0], [3.6, -1.85, 0]])
    trees = VGroup(*[pine(x, -0.42 + 0.15 * np.cos(x), 1.0 + 0.12 * (i % 2))
                     for i, x in enumerate((-0.9, -0.15, 0.65, 1.45, 2.2))])
    cloud1 = VGroup(*[Dot([x, 2.36, 0], radius=r, color=TEXT).set_opacity(0.23)
                      for x, r in ((-4.7, .28), (-4.4, .38), (-4.05, .25))])
    cloud2 = VGroup(*[Dot([x, 2.63, 0], radius=r, color=TEXT).set_opacity(0.18)
                      for x, r in ((3.3, .22), (3.58, .31), (3.87, .2))])
    add_drift(cloud1, 0.045)
    add_drift(cloud2, 0.025)
    for i, tr in enumerate(trees):
        add_sway(tr, amp=0.018, speed=1.35 + 0.08 * i, phase=i)
    waves = VGroup(*[ArcBetweenPoints([-6.15 + i * .82, -1.65, 0], [-5.55 + i * .82, -1.65, 0],
                                     angle=-0.28, color=TEAL, stroke_width=3).set_opacity(.65)
                     for i in range(4)])
    g = VGroup(ground, sea, stream, trees, waves, cloud1, cloud2)
    if labels:
        labs = VGroup(T("coast", 28, BLUE).move_to([-4.9, -2.16, 0]),
                      T("forest", 28, GREEN).move_to([0.6, -2.16, 0]),
                      T("stream", 28, BLUE).move_to([4.9, -2.16, 0]))
        g.add(labs)
        g.labels = labs
    g.ground, g.sea, g.stream, g.trees, g.waves = ground, sea, stream, trees, waves
    g.set_opacity(opacity)
    return g


def young_forest(question=False):
    ground = Line([-5.7, -1.85, 0], [5.7, -1.85, 0], color=BROWN, stroke_width=8)
    pines = VGroup(*[pine(x, -1.82, 1.15 + 0.12 * (i % 3))
                     for i, x in enumerate(np.linspace(-4.7, 3.6, 9))])
    for i, p in enumerate(pines):
        add_sway(p, amp=.025, speed=1.5, phase=i * .6)
    seeds = VGroup(seed(-2.4, -1.45), seed(.25, -1.45), seed(2.55, -1.45))
    fire = VGroup(flame(4.65, -1.83, .9), flame(5.08, -1.83, .72), flame(5.42, -1.83, .55))
    pulse(fire, base=2.5, amp=1.0, speed=3.2)
    g = VGroup(ground, pines, seeds, fire)
    g.ground, g.pines, g.seeds, g.fire = ground, pines, seeds, fire
    return g


FIRE_QUESTION = "What may happen if it burns again before young trees make many seeds?"


class S00Hook(SpokenScene):
    def construct(self):
        bay = landscape(labels=False)
        self.play(FadeIn(VGroup(bay.sea, bay.waves)), run_time=.7)
        self.at("Why do some ecosystems")
        self.play(FadeIn(VGroup(bay.ground, bay.stream, bay.trees, bay[-2], bay[-1])), run_time=1.2)
        q = fit_text("Why recover — or stay changed?", max_w=10.5, size=44, color=GOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN * .15), run_time=.7)
        self.at("Follow what happens")
        coast = T("coast", 28, BLUE).move_to([-4.9, -2.16, 0])
        forest = T("forest", 28, GREEN).move_to([0.6, -2.16, 0])
        stream = T("stream", 28, BLUE).move_to([4.9, -2.16, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * .1) for x in (coast, forest, stream)], lag_ratio=.25), run_time=1.3)
        self.at("answer is not simply")
        no = chip("not every change is permanent", RED, size=30).move_to([0, -3.1, 0])
        self.play(FadeIn(no, shift=UP * .12), run_time=.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "Big Changes: Dead Zones, Storms and Climate"
    TITLE = "When Ecosystems Change Course"

    def construct(self):
        w = landscape()
        title = fit_text(self.TITLE, max_w=11.5, size=52, color=TEXT, font=TITLE_FONT).move_to([0, 1.85, 0])
        veil = RoundedRectangle(width=12.2, height=1.2, corner_radius=.2, stroke_width=0,
                                fill_color=BG, fill_opacity=.82).move_to(title)
        self.add(w)
        self.play(FadeIn(veil), Write(title), run_time=self.beat(.5))
        timeline = Arrow([-5.4, 3.0, 0], [5.4, 3.0, 0], buff=0, color=GREY,
                         stroke_width=5, tip_length=.2)
        self.play(FadeOut(veil), ReplacementTransform(title, timeline), run_time=self.beat(.35))
        self.finish()


class S02SlowChange(SpokenScene):
    def construct(self):
        w = landscape()
        self.add(w, scope_tag())
        line = Arrow([-5.7, 3.0, 0], [5.7, 3.0, 0], buff=0, color=GREY, stroke_width=5, tip_length=.2)
        marker = Dot([-5.3, 3.0, 0], radius=.14, color=ORANGE)
        years = T("many years", 30, ORANGE).next_to(marker, DOWN, buff=.18)
        self.play(GrowArrow(line), FadeIn(marker), run_time=.8)
        self.at("lasting shift")
        self.play(FadeIn(years), run_time=.5)
        self.at("temperature rain or weather")
        warm = Polygon([-2.8, -.55, 0], [-1.3, -.2, 0], [.1, .35, 0], [1.8, -.05, 0],
                       [1.8, .22, 0], [.1, .62, 0], [-1.3, .07, 0], [-2.8, -.28, 0],
                       color=ORANGE, fill_color=ORANGE, fill_opacity=.2, stroke_width=0)
        self.play(FadeIn(warm), w.sea.animate.shift(RIGHT * .35), run_time=1.4)
        self.at("builds over many years")
        self.play(marker.animate.move_to([5.1, 3.0, 0]), years.animate.move_to([4.35, 2.55, 0]),
                  warm.animate.shift(UP * .28), run_time=2.0, rate_func=linear)
        self.finish()


class S03Habitat(SpokenScene):
    def construct(self):
        w = landscape()
        self.add(w, scope_tag())
        patches = VGroup(*[Ellipse(width=1.4, height=.62, color=GREEN, fill_color=GREEN,
                                  fill_opacity=.35).move_to(p) for p in ((-3.8, -.4, 0), (-.8, .62, 0), (2.1, .3, 0))])
        groups = VGroup(animal(-3.9, -.38), animal(-.9, .65), animal(2.05, .32))
        self.play(FadeIn(patches), run_time=.7)
        self.at("move or shrink")
        self.play(patches[0].animate.shift(RIGHT * .55 + UP * .3).scale(.72),
                  patches[1].animate.shift(RIGHT * .55 + UP * .45),
                  patches[2].animate.shift(LEFT * .25 + UP * .25).scale(.72), run_time=1.7)
        self.at("Some species may follow")
        self.play(FadeIn(groups), run_time=.5)
        self.play(groups[0].animate.shift(RIGHT * .55 + UP * .3),
                  groups[1].animate.shift(RIGHT * .55 + UP * .45), run_time=1.2)
        self.at("others may lose space")
        lost = T("may lose space", 30, TEXT).move_to([3.8, 1.45, 0])
        self.play(groups[2].animate.scale(.55).set_opacity(.45), FadeIn(lost), run_time=1.0)
        self.finish()


class S04Sudden(SpokenScene):
    def construct(self):
        w = landscape()
        self.add(w, scope_tag())
        line = Arrow([-5.7, 3.0, 0], [5.7, 3.0, 0], buff=0, color=GREY, stroke_width=5, tip_length=.2)
        pulse_dot = Dot([-5.4, 3, 0], radius=.18, color=RED)
        self.play(GrowArrow(line), FadeIn(pulse_dot), run_time=.6)
        self.at("arrives suddenly")
        self.play(pulse_dot.animate.move_to([5.3, 3, 0]), run_time=.65, rate_func=linear)
        self.at("Hurricanes tear branches")
        wind = VGroup(*[Arrow([-2.8, y, 0], [-.7, y-.15, 0], color=RED, stroke_width=4,
                             tip_length=.16) for y in (.7, 1.25, 1.8)])
        branch = Line([.55, .25, 0], [1.25, -.45, 0], color=BROWN, stroke_width=7)
        self.play(FadeIn(wind), w.trees.animate.rotate(-.09, about_point=[.5, -.3, 0]), FadeIn(branch), run_time=1.1)
        self.at("Floods spread")
        flood = Rectangle(width=3.1, height=1.35, color=BLUE, fill_color=BLUE, fill_opacity=.35).move_to([4.7, -1.35, 0])
        self.play(FadeOut(wind), FadeOut(branch), w.trees.animate.rotate(.09, about_point=[.5, -.3, 0]),
                  GrowFromEdge(flood, RIGHT), run_time=1.0)
        self.at("Forest fires burn")
        fires = VGroup(*[flame(x, -.45, .75) for x in (-.4, .25, .9, 1.55)])
        self.play(FadeOut(flood), LaggedStart(*[FadeIn(f) for f in fires], lag_ratio=.15), run_time=1.1)
        self.at("event is brief")
        after = VGroup(*[Line([x, -.4, 0], [x, .45, 0], color=GREY, stroke_width=7) for x in (-.4, .25, .9, 1.55)])
        self.play(FadeOut(fires), FadeIn(after), run_time=.8)
        self.at("effects can last")
        self.play(Indicate(after, color=RED, scale_factor=1.05), run_time=1.0)
        self.finish()


class S05Biodiversity(SpokenScene):
    def construct(self):
        patch = RoundedRectangle(width=11.4, height=5.4, corner_radius=.3, color=GREEN,
                                 fill_color=GREEN, fill_opacity=.1).move_to([0, .1, 0])
        patch._breath_t = 0.0
        def habitat_breath(m, dt):
            m._breath_t += dt
            m.set_fill(GREEN, opacity=.07 + .08 * (1 + np.sin(1.5 * m._breath_t)) / 2)
        patch.add_updater(habitat_breath)
        self.play(FadeIn(patch), run_time=.6)
        self.at("Biodiversity means")
        title = T("biodiversity = variety of living things", 36, GREEN).move_to([0, 3.1, 0])
        self.play(FadeIn(title), run_time=.6)
        groups = VGroup(VGroup(*[animal(-4.2+i*.52, .7) for i in range(4)]),
                        VGroup(*[pine(-1.7+i*.55, -.25, .72) for i in range(4)]),
                        VGroup(*[Circle(radius=.18, color=BLUE, fill_color=BLUE, fill_opacity=.6).move_to([1.2+i*.5, .6, 0]) for i in range(4)]),
                        VGroup(*[Dot([3.45+i*.42, -.15, 0], radius=.15, color=YELLOW) for i in range(4)]))
        self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=.2), run_time=1.4)
        self.at("Some populations fall")
        may = T("may", 30, GOLD).move_to([0, -2.25, 0])
        self.play(groups[0].animate.scale(.55), groups[1].animate.scale(.6), FadeIn(may), run_time=1.2)
        self.at("others may find new space")
        self.play(groups[3].animate.scale(1.45), groups[3].animate.shift(RIGHT * .25), run_time=1.0)
        self.at("different groups in different directions")
        dirs = VGroup(arrow([-4.2, -1.05, 0], [-4.2, -1.65, 0], RED),
                      arrow([-1.0, -1.05, 0], [-1.0, -1.65, 0], RED),
                      arrow([1.9, -1.55, 0], [1.9, -1.05, 0], GREY),
                      arrow([4.1, -1.15, 0], [4.1, -.45, 0], GREEN))
        self.play(LaggedStart(*[GrowArrow(a) for a in dirs], lag_ratio=.15), run_time=1.3)
        self.add(scope_tag())
        self.finish()


class S06FirePredict(SpokenScene):
    def construct(self):
        f = young_forest()
        self.play(FadeIn(f.ground), run_time=.4)
        self.at("young pine forest")
        self.play(LaggedStart(*[GrowFromEdge(p, DOWN) for p in f.pines], lag_ratio=.08), run_time=1.5)
        self.at("first fire removed older trees")
        old = VGroup(*[Line([x, -1.8, 0], [x, .75, 0], color=GREY, stroke_width=8) for x in (-5.1, -3.2, 4.1)])
        self.play(FadeIn(old), run_time=.5)
        self.play(FadeOut(old), run_time=.5)
        self.at("young trees started returning")
        self.play(Indicate(f.pines, color=GREEN, scale_factor=1.03), run_time=.8)
        self.at("before the young trees make many seeds")
        self.play(FadeIn(f.seeds), FadeIn(f.fire), run_time=.8)
        q = question_card(FIRE_QUESTION, y=-3.1, size=28, max_w=11.2)
        self.play(FadeIn(q.question), run_time=.6)
        self.add(scope_tag())
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = FIRE_QUESTION
    SECONDS = 4.5
    CARD = {"y": -3.1, "size": 28, "max_w": 11.2}
    def backdrop(self):
        return young_forest()


class S08FireReveal(SpokenScene):
    def construct(self):
        f = young_forest()
        self.add(f, scope_tag())
        self.at("second fire")
        self.play(f.fire.animate.shift(LEFT * 9.0), run_time=1.8, rate_func=linear)
        self.play(FadeOut(f.fire), FadeOut(f.pines), run_time=.6)
        seedlings = VGroup(*[pine(x, -1.82, .68) for x in (-3.7, -.9, 2.4)])
        self.at("few seeds were ready")
        self.play(FadeOut(f.seeds), LaggedStart(*[GrowFromEdge(p, DOWN) for p in seedlings], lag_ratio=.25), run_time=1.3)
        for i, p in enumerate(seedlings):
            add_sway(p, amp=.035, speed=1.45 + .08 * i, phase=i)
        label = chip("fewer may return", GREEN, size=32).move_to([0, 2.45, 0])
        self.play(FadeIn(label), run_time=.6)
        self.at("In Yellowstone")
        data = fit_text("Yellowstone: about 1/6 as many young trees", max_w=10.8, size=32,
                        color=TEXT).move_to([0, 1.55, 0])
        scan = RoundedRectangle(width=1.7, height=1.75, corner_radius=.12, color=TEXT,
                                stroke_width=3, fill_color=TEXT, fill_opacity=.12).move_to([-4.7, -1.0, 0])
        scan.layout_ok = True  # intentional translucent counting window passes behind later labels
        scan._vx = .9
        def count_scan(m, dt):
            m.shift(RIGHT * m._vx * dt)
            if m.get_x() > 5.1:
                m.shift(LEFT * 10.2)
        scan.add_updater(count_scan)
        self.play(FadeIn(data), FadeIn(scan), run_time=.7)
        self.at("counted only the first year")
        limit = T("first year only", 30, GOLD).move_to([0, .8, 0])
        self.play(FadeIn(limit), run_time=.6)
        self.at("long term result is not known")
        unknown = T("long-term result: not known", 32, GREY).move_to([0, -.05, 0])
        self.play(FadeIn(unknown), run_time=.7)
        self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        w = landscape()
        self.add(w, scope_tag())
        source = Dot([-5.25, -.65, 0], radius=.2, color=RED)
        self.play(FadeIn(source), run_time=.4)
        self.at("effects can spread")
        a1 = arrow([-5.0, -.65, 0], [-1.55, .12, 0], RED)
        a2 = arrow([-1.3, .15, 0], [3.65, -1.28, 0], GOLD)
        a3 = arrow([-1.15, .25, 0], [1.1, 1.2, 0], GREEN)
        self.play(GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), run_time=1.4)
        self.at("connections timing")
        nodes = VGroup(chip("habitat", GREEN, size=28).move_to([-1.05, 1.65, 0]),
                       chip("organisms", TEXT, size=28).move_to([2.1, 1.95, 0]),
                       chip("water", BLUE, size=28).move_to([4.45, -.35, 0]))
        self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=.18), run_time=1.1)
        self.at("weaken strengthen or stop")
        stop = Line([.55, .8, 0], [1.25, 1.5, 0], color=RED, stroke_width=7)
        self.play(a1.animate.set_stroke(width=3, opacity=.45), a2.animate.set_stroke(width=9), Create(stop), run_time=1.2)
        self.at("before reaching every part")
        self.play(nodes[1].animate.set_opacity(.4), run_time=.7)
        self.finish()


def recovery_tracks():
    base = VGroup(*[Line([-4.45, y, 0], [5.6, y, 0], color=GREY, stroke_width=3) for y in (1.65, 0, -1.65)])
    labs = VGroup(T("mild", 28, TEXT).move_to([-5.7, 1.65, 0]),
                  T("longer", 28, TEXT).move_to([-5.7, 0, 0]),
                  T("close pulses", 28, TEXT).move_to([-5.7, -1.65, 0]))
    return VGroup(base, labs)


class S10Recovery(SpokenScene):
    def construct(self):
        tracks = recovery_tracks()
        self.play(FadeIn(tracks), run_time=.6)
        self.at("how severe")
        pulses = VGroup(Rectangle(width=.35, height=.8, color=RED, fill_color=RED, fill_opacity=.7).move_to([-3.7, 1.65, 0]),
                        Rectangle(width=1.45, height=.8, color=RED, fill_color=RED, fill_opacity=.7).move_to([-3.15, 0, 0]),
                        Rectangle(width=.35, height=.8, color=RED, fill_color=RED, fill_opacity=.7).move_to([-3.7, -1.65, 0]),
                        Rectangle(width=.35, height=.8, color=RED, fill_color=RED, fill_opacity=.7).move_to([-2.8, -1.65, 0]))
        self.play(FadeIn(pulses[0]), run_time=.4)
        self.at("how long it lasts")
        self.play(FadeIn(pulses[1]), run_time=.6)
        self.at("conditions already there")
        self.play(FadeIn(pulses[2]), FadeIn(pulses[3]), run_time=.6)
        self.at("Timing matters")
        returns = VGroup(arrow([-3.3, 1.65, 0], [4.8, 1.65, 0], GREEN, 7),
                         arrow([-2.35, 0, 0], [3.1, 0, 0], GREEN, 5),
                         arrow([-2.4, -1.65, 0], [1.25, -1.65, 0], GREEN, 4))
        self.play(LaggedStart(*[GrowArrow(a) for a in returns], lag_ratio=.25), run_time=1.7)
        for a in returns:
            pulse(a, base=5.5, amp=2.0, speed=2.4)
        earlier = VGroup(*[Dot([5.0+i*.25, 1.65, 0], radius=.09, color=GREEN) for i in range(4)])
        partial = VGroup(*[Dot([3.35+i*.25, 0, 0], radius=.09, color=GREEN) for i in range(2)],
                         Dot([1.55, -1.65, 0], radius=.09, color=GREEN))
        self.play(FadeIn(earlier), FadeIn(partial), run_time=.7)
        self.add(scope_tag())
        self.finish()


class S11RecoveryExamples(SpokenScene):
    def construct(self):
        tp = TwoPanel("Bay in fall", "forest after fire", colors=(BLUE, GREEN))
        self.play(FadeIn(tp), run_time=.5)
        layers = VGroup(Rectangle(width=4.7, height=1.3, color=BLUE, fill_color=BLUE, fill_opacity=.18),
                        Rectangle(width=4.7, height=1.3, color=BLUE, fill_color=BLUE, fill_opacity=.34)).arrange(DOWN, buff=.06)
        tp.put(layers, "left")
        forest = VGroup(Line([-2.1, -1.2, 0], [2.1, -1.2, 0], color=BROWN, stroke_width=6),
                        *[pine(x, -1.18, .8) for x in (-1.5, -.5, .5, 1.5)])
        tp.put(forest, "right")
        self.play(FadeIn(layers), FadeIn(forest), run_time=.7)
        self.at("winds can remix")
        mix = VGroup(*[CurvedArrow([-4.7+i*.6, 1.25, 0], [-4.7+i*.6, -.95, 0], angle=.45,
                                  color=TEAL, stroke_width=4, tip_length=.15) for i in range(3)])
        self.play(LaggedStart(*[Create(a) for a in mix], lag_ratio=.18), run_time=1.2)
        self.at("Repeated damage")
        fires = VGroup(flame(1.7, -.75, .6), flame(2.55, -.75, .6))
        self.play(FadeIn(fires[0]), run_time=.4)
        self.play(FadeIn(fires[1]), forest.animate.set_opacity(.45), run_time=.7)
        self.at("supply of seeds")
        seeds = VGroup(*[seed(x, y) for x, y in ((.5, 1.0), (1.1, .7), (1.6, .95), (2.1, .6))])
        self.play(FadeIn(seeds), run_time=.5)
        self.play(seeds.animate.shift(DOWN * 1.35), run_time=1.1)
        new = VGroup(pine(.75, -.8, .55), pine(1.55, -.8, .55))
        self.play(FadeOut(seeds), FadeIn(new), run_time=.7)
        self.finish()


class S12NotIdentical(SpokenScene):
    def construct(self):
        tp = TwoPanel("earlier", "later", colors=(GREEN, GOLD))
        self.play(FadeIn(tp), run_time=.5)
        left = VGroup(*[pine(x, -1.3, 1.0) for x in (-1.8, -.7, .4, 1.5)],
                      animal(0, -.1, 1.2))
        right = VGroup(pine(-1.4, -1.3, .8), pine(.2, -1.3, 1.25),
                       *[animal(x, y, s) for x, y, s in ((-1.0, .1, .8), (.6, -.25, 1.0), (1.4, .25, .65))])
        tp.put(left, "left"); tp.put(right, "right")
        for i, organism in enumerate((left[-1], right[2], right[3], right[4])):
            bob(organism, amp=.075, speed=1.55 + .12 * i, seed=i)
        self.play(FadeIn(left), run_time=.6)
        self.at("does not always mean")
        self.play(FadeIn(right), run_time=.7)
        self.at("still work")
        work1 = T("working ecosystem", 28, GREEN).move_to([-3.2, -2.1, 0])
        work2 = T("working ecosystem", 28, GOLD).move_to([3.2, -2.1, 0])
        self.play(FadeIn(work1), FadeIn(work2), run_time=.6)
        self.at("different way")
        mix = chip("different mix", GOLD, size=30).move_to([3.2, 1.7, 0])
        self.play(FadeIn(mix), run_time=.6)
        self.at("Different groups")
        links = VGroup(arrow([-4.0, -.3, 0], [-2.7, .6, 0], GREEN, 4),
                       arrow([2.2, -.4, 0], [3.25, .55, 0], GREEN, 4),
                       arrow([3.5, .55, 0], [4.3, -.2, 0], GREEN, 4))
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=.15), run_time=1.1)
        self.at("fast slow partial")
        cap = caption("Return may be fast, slow, partial, or hard to see.", size=28)
        self.play(FadeIn(cap), run_time=.7)
        self.finish()


def observation_loop(words=("change", "measure", "revise"), center=ORIGIN):
    pts = [center + LEFT * 2.8 + UP * .75, center + RIGHT * 2.8 + UP * .75, center + DOWN * 1.6]
    nodes = VGroup(*[chip(t, c, size=30).move_to(p) for t, c, p in zip(words, (RED, BLUE, GREEN), pts)])
    arrows = VGroup(CurvedArrow(nodes[0].get_right(), nodes[1].get_left(), angle=-.25, color=GREY, tip_length=.18),
                    CurvedArrow(nodes[1].get_bottom(), nodes[2].get_right(), angle=-.25, color=GREY, tip_length=.18),
                    CurvedArrow(nodes[2].get_left(), nodes[0].get_bottom(), angle=-.25, color=GREY, tip_length=.18))
    g = VGroup(nodes, arrows); g.nodes, g.arrows = nodes, arrows
    return g


class S13People(SpokenScene):
    def construct(self):
        w = landscape()
        self.add(w, scope_tag())
        pressure = arrow([-1.0, 2.0, 0], [-.1, .5, 0], RED, 9)
        self.at("People cause")
        self.play(GrowArrow(pressure), run_time=.7)
        self.at("people can also help")
        restoration = VGroup(*[pine(x, -.35, .65) for x in (-1.0, -.4, .2)])
        self.play(FadeOut(pressure), LaggedStart(*[GrowFromEdge(p, DOWN) for p in restoration], lag_ratio=.2), run_time=1.1)
        self.at("good plan traces")
        self.play(FadeOut(w), FadeOut(restoration), run_time=.5)
        loop = observation_loop()
        self.play(FadeIn(loop.nodes[0]), Create(loop.arrows[0]), run_time=.6)
        self.at("measures results")
        self.play(FadeIn(loop.nodes[1]), Create(loop.arrows[1]), run_time=.6)
        self.at("changes course")
        self.play(FadeIn(loop.nodes[2]), Create(loop.arrows[2]), run_time=.7)
        for a in loop.arrows:
            pulse(a, base=3.5, amp=1.5, speed=2.6)
        self.at("Actions on land")
        small = landscape(opacity=.35)
        self.play(FadeOut(loop), FadeIn(small), run_time=.6)
        helpful = arrow([-.4, .1, 0], [4.6, -1.35, 0], GREEN, 7)
        self.play(GrowArrow(helpful), run_time=1.2)
        self.finish()


class S14Questions(SpokenScene):
    def construct(self):
        w = landscape()
        self.add(w, scope_tag())
        light = Dot([-5.3, -.7, 0], radius=.22, color=GOLD)
        trail = TracedPath(light.get_center, stroke_color=GOLD, stroke_width=5, dissipating_time=2.0)
        self.add(trail, light)
        self.at("where the change began")
        where = chip("where?", RED, size=32).move_to([-4.3, 3.0, 0])
        self.play(FadeIn(where), light.animate.move_to([-1.0, .25, 0]), run_time=1.1)
        self.at("which connections")
        which = chip("which connections?", GOLD, size=32).move_to([0, 3.0, 0])
        self.play(FadeIn(which), light.animate.move_to([4.4, -1.2, 0]), run_time=1.1)
        self.at("what might help")
        helps = chip("what helps?", GREEN, size=32).move_to([4.35, 3.0, 0])
        self.play(FadeIn(helps), light.animate.move_to([-.2, .25, 0]), run_time=1.1)
        self.finish()


class S15Evidence(SpokenScene):
    def construct(self):
        w = landscape(opacity=.22)
        self.add(w)
        questions = VGroup(chip("where?", RED, size=30), chip("which connections?", GOLD, size=30),
                           chip("what helps?", GREEN, size=30)).arrange(RIGHT, buff=.45).move_to([0, 3.0, 0])
        self.play(FadeIn(questions), run_time=.6)
        self.at("testable model")
        loop = observation_loop(("model", "measure", "revise"), center=DOWN * .15)
        self.play(ReplacementTransform(questions[0], loop.nodes[0]),
                  ReplacementTransform(questions[1], loop.nodes[1]),
                  ReplacementTransform(questions[2], loop.nodes[2]), run_time=1.1)
        self.play(LaggedStart(*[Create(a) for a in loop.arrows], lag_ratio=.2), run_time=1.0)
        for a in loop.arrows:
            pulse(a, base=3.5, amp=1.5, speed=2.6)
        self.at("measurements that could support")
        self.play(Indicate(loop.nodes[1], color=BLUE, scale_factor=1.1), run_time=.8)
        self.at("show its limits")
        limit = T("evidence can revise the model", 32, GOLD).move_to([0, -2.65, 0])
        self.play(FadeIn(limit), Indicate(loop.nodes[2], color=GREEN, scale_factor=1.1), run_time=.8)
        self.finish()


class S16End(EndCard):
    LINE = "Change one ecosystem part, and effects can spread through the system."
