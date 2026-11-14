"""What the Hare Data Show — chapter 2 of Adaptations for Survival.

COLOR MAP (carried exactly from chapter 1 where the concept occurs)
  GREEN  matched condition / timing that fits
  RED    mismatch / cost
  BLUE   inherited variation and estimated links
  YELLOW population and time
  WHITE_C snowshoe hare winter coat
  BROWN_C snowshoe hare summer coat
  SNOW_C snow; GROUND_C bare ground

The Montana plot contains only the three rounded values printed in the lesson.  Straight
segments join those observations; they are not presented as a fitted biological curve.
"""
from bp_parts import *  # noqa: F401,F403


WHITE_C = "#F4F6FA"
BROWN_C = "#8A6240"
SNOW_C = "#D5E1EE"
GROUND_C = "#5B4331"
EDGE = "#9AA3B2"
INK = "#1B2433"
SAND_C = "#CDB98A"
SOIL_C = "#49372B"


def ambient_field():
    """A quiet, moving snow/ground motif behind spoken scenes.

    It keeps held explanations alive without adding a scientific claim.  The two low arcs also
    preserve chapter 1's landscape language in the data scenes.
    """
    left = Circle(radius=3.2, stroke_width=0, fill_color=SNOW_C, fill_opacity=.18).move_to([-5.4, -5.35, 0])
    right = Circle(radius=3.3, stroke_width=0, fill_color=BLUE, fill_opacity=.16).move_to([5.3, -5.45, 0])
    contours = VGroup(
        Arc(radius=2.8, start_angle=.1, angle=2.2, arc_center=[-5.4, -5.35, 0],
            color=TEXT, stroke_width=5, stroke_opacity=.28),
        Arc(radius=2.45, start_angle=.7, angle=1.8, arc_center=[5.3, -5.45, 0],
            color=BLUE, stroke_width=6, stroke_opacity=.32))
    contours[0].add_updater(lambda m, dt: m.rotate(.34*dt, about_point=[-5.4, -5.35, 0]))
    contours[1].add_updater(lambda m, dt: m.rotate(-.38*dt, about_point=[5.3, -5.45, 0]))
    motes = VGroup()
    for i in range(48):
        x = -6.2 + (i % 12) * 1.12
        y = -3.0 + (i // 12) * 1.95
        d = Dot([x, y, 0], radius=.05 + .012*(i % 3), color=TEXT).set_opacity(.30)
        d.v = np.array([.05*((i % 3)-1), .24 + .045*(i % 4), 0])
        def drift(m, dt):
            m.shift(m.v*dt)
            if m.get_y() > 3.65:
                m.shift(DOWN*6.4)
        d.add_updater(drift)
        motes.add(d)
    field = VGroup(left, right, contours, motes).set_z_index(-20)
    field.layout_ok = True
    return field


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(ambient_field())


def band(x, y_top, y_bottom, width, color):
    return Rectangle(width=width, height=y_top-y_bottom, stroke_width=0,
                     fill_color=color, fill_opacity=1).move_to([x, (y_top+y_bottom)/2, 0])


def hare(coat=WHITE_C, scale=1.0, edge=EDGE):
    """Chapter 1's block-silhouette snowshoe hare, with feet at local y=0."""
    def rr(w, h, x, y, r):
        return RoundedRectangle(corner_radius=r, width=w, height=h).move_to([x, y, 0])
    parts = [rr(2.5, 1.25, 0, .95, .6), rr(.95, .8, 1.45, 1.55, .35),
             rr(.26, .95, 1.3, 2.3, .13).rotate(-.12),
             rr(.26, .95, 1.62, 2.25, .13).rotate(.1),
             rr(1.1, .3, -.75, .15, .15), rr(.32, .45, .85, .22, .12)]
    body = Union(*parts, stroke_color=edge, stroke_width=3, fill_color=coat, fill_opacity=1)
    eye = Dot([1.66, 1.65, 0], radius=.06, color=BG)
    g = VGroup(body, eye).scale(scale)
    g.body = body
    return g


def stand(mob, x, feet_y):
    return mob.move_to([x, feet_y + mob.height/2, 0])


def collar(h, color=BLUE):
    c = h.get_center() + np.array([.62*h.width/2, .12*h.height, 0])
    ring = Circle(radius=.17, color=color, stroke_width=5).move_to(c)
    tag = Dot(c + DOWN*.22, radius=.08, color=color)
    return VGroup(ring, tag)


def signal(center, color=BLUE, max_r=1.15):
    return VGroup(*[Arc(radius=r, start_angle=-PI/3, angle=2*PI/3,
                        arc_center=center, color=color, stroke_width=4).set_opacity(.8-i*.18)
                    for i, r in enumerate(np.linspace(.4, max_r, 3))])


def eye_icon(at, color=RED, scale=.8):
    outline = Ellipse(width=1.8, height=.85, color=color, stroke_width=5)
    pupil = VGroup(Circle(radius=.25, color=color, fill_color=color, fill_opacity=.18),
                   Dot(radius=.09, color=color))
    return VGroup(outline, pupil).scale(scale).move_to(at)


def hillside(split=True):
    """The carried Montana hillside used by every hillside scene."""
    sky = Rectangle(width=13.2, height=6.4, stroke_width=0, fill_color=BG,
                    fill_opacity=1).move_to([0, .3, 0])
    if split:
        ground = VGroup(band(-3.15, -.9, -3.5, 6.3, SNOW_C),
                        band(3.15, -.9, -3.5, 6.3, GROUND_C))
    else:
        ground = band(0, -.9, -3.5, 12.6, GROUND_C)
    ridge = VMobject(color=EDGE, stroke_width=4).set_points_as_corners(
        [np.array([-6.3, -.9, 0]), np.array([-3.8, .15, 0]), np.array([-1.1, -.55, 0]),
         np.array([1.8, .3, 0]), np.array([4.0, -.35, 0]), np.array([6.3, -.9, 0])])
    return VGroup(sky, ground, ridge)


def radio_hare(x=0, coat=WHITE_C, scale=1.15, feet_y=-.9):
    h = stand(hare(coat, scale), x, feet_y)
    return VGroup(h, collar(h))


def survival_plot():
    p = Plot(box=(-5.55, 5.55, -2.15, 2.35), xr=(0, 100), yr=(87, 98),
             xticks=[(0, "0"), (60, "60"), (100, "100")],
             yticks=[(89, "89%"), (92, "92%"), (96, "96%")],
             xlabel="coat–ground contrast", ylabel="estimated weekly survival", label_size=28)
    return p


def reported_points(p, include_lines=True):
    pts = [Dot(p.pt(x, y), radius=.16, color=c, stroke_color=TEXT, stroke_width=3)
           for x, y, c in [(0, 96, GREEN), (60, 92, YELLOW), (100, 89, RED)]]
    lines = VGroup(Line(p.pt(0, 96), p.pt(60, 92), color=TEXT, stroke_width=5),
                   Line(p.pt(60, 92), p.pt(100, 89), color=TEXT, stroke_width=5))
    return VGroup(lines, *pts) if include_lines else VGroup(*pts)


def choice_arrows(p):
    x0, x1 = p.pt(12, 91), p.pt(47, 91)
    rise = Arrow(x0+UP*.55, x1+UP*1.25, buff=0, color=GREEN, stroke_opacity=.48, tip_length=.2)
    level = Arrow(x0, x1, buff=0, color=YELLOW, stroke_opacity=.48, tip_length=.2)
    fall = Arrow(x0+DOWN*.55, x1+DOWN*1.25, buff=0, color=RED, stroke_opacity=.7, tip_length=.2)
    return VGroup(rise, level, fall)


def clay_mouse(color=WHITE_C, edge=EDGE, scale=.7):
    body = Ellipse(width=2.0, height=1.0, stroke_color=edge, stroke_width=4,
                   fill_color=color, fill_opacity=1)
    head = Circle(radius=.42, stroke_color=edge, stroke_width=4,
                  fill_color=color, fill_opacity=1).next_to(body, RIGHT, buff=-.24).shift(UP*.05)
    ears = VGroup(*[Circle(radius=.16, stroke_color=edge, stroke_width=3,
                           fill_color=color, fill_opacity=1).move_to(head.get_center()+v)
                    for v in (UL*.28, UR*.22)])
    tail = Arc(radius=.6, start_angle=PI*.6, angle=PI*.65, color=edge, stroke_width=4)
    tail.next_to(body, LEFT, buff=-.12)
    eye = Dot(head.get_center()+RIGHT*.16+UP*.05, radius=.045, color=INK)
    return VGroup(tail, body, head, ears, eye).scale(scale)


def timing_world():
    """Four carried hares and their season/timing track, reused without drift."""
    line = Arrow([-5.7, -1.8, 0], [5.8, -1.8, 0], buff=0, color=YELLOW,
                 stroke_width=6, tip_length=.25)
    xs = [-4.4, -1.5, 1.5, 4.4]
    hs = VGroup(*[stand(hare(c, .57), x, -.45)
                  for x, c in zip(xs, [WHITE_C, WHITE_C, BROWN_C, BROWN_C])])
    ticks = VGroup(*[Line([x, -2.1, 0], [x, -1.5, 0], color=BLUE, stroke_width=8)
                     for x in [-3.8, -1.1, 1.0, 3.6]])
    melt = Line([.2, -2.35, 0], [.2, .25, 0], color=YELLOW, stroke_width=6)
    return VGroup(line, hs, ticks, melt)


def generations_track():
    frames = VGroup(*[RoundedRectangle(corner_radius=.18, width=3.65, height=4.7,
                                       stroke_color=YELLOW, stroke_width=3).move_to([x, .15, 0])
                      for x in [-4.25, 0, 4.25]])
    labels = VGroup(*[T(f"generation {i}", 28, YELLOW).move_to([x, 2.1, 0])
                      for i, x in enumerate([-4.25, 0, 4.25], 1)])
    return VGroup(frames, labels)


class S00Hook(FilmScene):
    def construct(self):
        world = hillside(True)
        h = radio_hare(-3.2)
        self.play(FadeIn(world), FadeIn(h, shift=UP*.2), run_time=.8)
        self.at("helping on snow")
        self.play(h.animate.shift(RIGHT*6.25), run_time=2.2)
        self.at("standing out")
        ring = SurroundingRectangle(h, color=RED, buff=.12, corner_radius=.2)
        self.play(Create(ring), run_time=.6)
        self.at("change a hair's survival")
        q = T("survival?", 48, YELLOW, weight=BOLD).move_to([3.0, 2.7, 0])
        sig = signal(h[1][1].get_center(), max_r=1.0)
        pulse(sig, base=4, amp=2, speed=2)
        self.play(FadeIn(q, shift=UP*.2), FadeIn(sig), run_time=.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "Adaptations for Survival"
    TITLE = "What the Hare Data Show"


class S02Follow(FilmScene):
    def construct(self):
        world = hillside(False)
        rh = radio_hare(-1.0, BROWN_C, 1.25)
        self.play(FadeIn(world), FadeIn(rh), run_time=.7)
        self.at("radio collars")
        self.play(Indicate(rh[1], color=BLUE, scale_factor=1.35), run_time=.8)
        sig = signal(rh[1][1].get_center(), max_r=1.4)
        pulse(sig, base=4, amp=2, speed=2)
        self.add(sig)
        self.at("Each week")
        weekly = counter("weekly check  {:.0f}", ValueTracker(1), [3.9, 2.8, 0], 30, YELLOW)
        researcher = VGroup(Circle(radius=.28, color=TEXT), Line(DOWN*.25, DOWN*1.25, color=TEXT, stroke_width=6),
                            Line(DOWN*.55, LEFT*.55+DOWN*1.55, color=TEXT, stroke_width=5),
                            Line(DOWN*.55, RIGHT*.55+DOWN*1.55, color=TEXT, stroke_width=5)).move_to([4.2, -.1, 0])
        self.play(FadeIn(weekly), FadeIn(researcher, shift=LEFT*.3), run_time=.8)
        self.at("checked signals")
        self.play(researcher.animate.shift(LEFT*2), run_time=2.0)
        self.at("find each animal again")
        self.play(Indicate(rh, color=BLUE, scale_factor=1.04), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Score(FilmScene):
    def construct(self):
        h = stand(hare(WHITE_C, 1.15), -4.5, -1.5)
        coat = ValueTracker(.82)
        snow = ValueTracker(.35)
        d1 = dial(coat, [-1.5, .9, 0], 1.35, "coat whiteness", BLUE)
        self.play(FadeIn(h), FadeIn(d1), run_time=.7)
        self.at("scored nearby snow")
        d2 = dial(snow, [2.1, .9, 0], 1.35, "site weekly snow cover", YELLOW)
        self.play(FadeIn(d2), run_time=.7)
        self.at("averaged it")
        self.play(snow.animate.set_value(.47), run_time=1.8)
        self.at("Contrast was the gap")
        contrast = ValueTracker(abs(coat.get_value()-snow.get_value()))
        gauge = dial(contrast, [5.0, .8, 0], 1.15, "contrast", RED)
        self.play(FadeIn(gauge), run_time=.7)
        self.at("coat whiteness")
        self.play(coat.animate.set_value(.65), contrast.animate.set_value(.18), run_time=1.7)
        self.at("weekly snow cover")
        self.play(snow.animate.set_value(.60), contrast.animate.set_value(.05), run_time=1.7)
        match = T("match", 30, GREEN).move_to([5, -1.35, 0])
        self.play(FadeIn(match), run_time=.5)
        self.finish()


class S04Model(FilmScene):
    def construct(self):
        p = survival_plot()
        self.play(Create(p), run_time=1.4)
        self.at("estimated weekly survival")
        places = reported_points(p, include_lines=False).set_opacity(.18)
        self.play(FadeIn(places), run_time=.8)
        self.at("different mismatch levels")
        self.play(LaggedStart(*[Indicate(x, color=x.get_color(), scale_factor=1.5) for x in places], lag_ratio=.25), run_time=1.5)
        self.at("estimates for groups")
        tag = scope_tag("model estimates")
        self.play(FadeIn(tag), run_time=.6)
        self.at("not guarantees")
        cap = caption("groups, not guarantees for one hare", 30, YELLOW, y=-3.45)
        self.play(FadeIn(cap), run_time=.7)
        pulse(places, base=4, amp=1.2, speed=2)
        self.finish()


class S04bMissing(FilmScene):
    def construct(self):
        weeks = [-4.8, -2.4, 0, 2.4, 4.8]
        line = Arrow([-5.7, -2.2, 0], [5.8, -2.2, 0], buff=0, color=YELLOW, stroke_width=5)
        hs = VGroup(*[stand(hare(c, .48), x, -.6) for x, c in zip(weeks, [BROWN_C, BROWN_C, WHITE_C, WHITE_C, WHITE_C])])
        self.play(GrowArrow(line), FadeIn(hs), run_time=.8)
        self.at("was missed")
        missing = hs[2]
        cloud = Circle(radius=.72, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=.10).move_to(missing)
        self.play(FadeOut(missing), FadeIn(cloud), run_time=.7)
        self.at("between observations")
        bridge = DashedLine(hs[1].get_top(), hs[3].get_top(), color=BLUE, stroke_width=6)
        label = T("estimated between observations", 28, BLUE).move_to([0, 2.25, 0])
        self.play(Create(bridge), FadeIn(label), run_time=1.2)
        self.at("adds uncertainty")
        pulse(cloud, base=3, amp=2, speed=2)
        self.play(cloud.animate.scale(1.35), run_time=1.0)
        self.at("rounded estimates")
        rounded = chip("rounded estimates", YELLOW, 30).move_to([0, 3.05, 0])
        self.play(swap(label, rounded), run_time=.8)
        self.finish()


class S05Predict(FilmScene):
    QUESTION = "Should estimated survival rise, stay level, or fall?"
    OPTIONS = ("rise", "stay level", "fall")

    def construct(self):
        p = survival_plot()
        choices = choice_arrows(p)
        self.add(p)
        self.at("predict the direction")
        self.play(LaggedStart(*[GrowArrow(a) for a in choices], lag_ratio=.25), run_time=1.5)
        self.at("coat and ground differ more")
        end = Dot(p.pt(100, 87.4), radius=.22, color=RED)
        pulse(end, base=6, amp=3, speed=2)
        self.play(FadeIn(end), run_time=.5)
        self.at("survival rise")
        q = question_card(self.QUESTION, self.OPTIONS, chips_at=[4.55, .75, 0],
                          y=-3.42, left=-6.35, max_w=9.6, size=28)
        self.play(FadeIn(q.chips), FadeIn(q.question), run_time=.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = S05Predict.QUESTION
    OPTIONS = S05Predict.OPTIONS
    CHIPS_AT = [4.55, .75, 0]
    CARD = {"y": -3.42, "left": -6.35, "max_w": 9.6, "size": 28}
    SECONDS = 4.5

    def backdrop(self):
        p = survival_plot()
        return VGroup(p, choice_arrows(p), Dot(p.pt(100, 87.4), radius=.22, color=RED))


class S07Reveal(FilmScene):
    def construct(self):
        p = survival_plot()
        self.add(p)
        self.at("fell as mismatch grew")
        data = reported_points(p)
        self.play(Create(data[0]), FadeIn(data[1]), run_time=1.2)
        self.at("fully mismatched estimate")
        self.play(FadeIn(data[3]), run_time=.7)
        l0 = T("0 contrast, 96%", 28, GREEN).next_to(data[1], UR, buff=.16)
        l2 = T("100 contrast, 89%", 28, RED).move_to([4.65, 1.25, 0])
        self.play(FadeIn(l0), FadeIn(l2), run_time=.8)
        self.at("partial mismatch")
        self.play(FadeIn(data[2]), run_time=.6)
        l1 = T("60 contrast, 92%", 28, YELLOW).next_to(data[2], UR, buff=.16)
        self.play(FadeIn(l1), run_time=.6)
        tag = scope_tag("rounded reported estimates")
        self.play(FadeIn(tag), run_time=.5)
        pulse(data[0], base=5, amp=1.4, speed=2)
        self.finish()


class S08Meaning(FilmScene):
    def construct(self):
        world = hillside(True)
        matched = radio_hare(-3.25, WHITE_C, 1.0)
        mismatched = radio_hare(3.25, WHITE_C, 1.0)
        self.play(FadeIn(world), FadeIn(matched), FadeIn(mismatched), run_time=.8)
        self.at("not a shield")
        eyes = VGroup(eye_icon([-3.2, 2.3, 0], RED, .65), eye_icon([3.2, 2.3, 0], RED, .65))
        self.play(FadeIn(eyes), run_time=.6)
        self.at("matched hair may die")
        c1 = Circle(radius=1.55, color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=.08).move_to(matched)
        self.play(Create(c1), matched.animate.shift(RIGHT*.35), run_time=1.0)
        self.at("mismatched hair may survive")
        c2 = Circle(radius=1.55, color=RED, stroke_width=4, fill_color=RED, fill_opacity=.08).move_to(mismatched)
        self.play(Create(c2), mismatched.animate.shift(LEFT*.35), run_time=1.0)
        self.at("change the chance")
        chance = T("chance", 46, YELLOW, weight=BOLD).move_to([0, 2.9, 0])
        self.play(FadeIn(chance), run_time=.6)
        self.at("do not decide")
        self.play(c1.animate.scale(1.08), c2.animate.scale(.92), rate_func=there_and_back, run_time=1.4)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Clay(FilmScene):
    def construct(self):
        panels = TwoPanel("light sand", "dark soil", colors=(YELLOW, GREY))
        sand = band(-3.3, 1.95, -2.2, 5.7, SAND_C)
        soil = band(3.3, 1.95, -2.2, 5.7, SOIL_C)
        self.play(FadeIn(panels), FadeIn(sand), FadeIn(soil), run_time=.8)
        self.at("clay mice")
        mice = VGroup(clay_mouse(WHITE_C).move_to([-4.35, .35, 0]), clay_mouse(BROWN_C).move_to([-2.25, .35, 0]),
                       clay_mouse(WHITE_C).move_to([2.25, .35, 0]), clay_mouse(BROWN_C).move_to([4.35, .35, 0]))
        self.play(FadeIn(mice, shift=UP*.25), run_time=.8)
        clay = T("clay models", 30, BLUE).move_to([0, 3.42, 0])
        self.play(FadeIn(clay), run_time=.4)
        self.at("light and dark models")
        eye = eye_icon([-5.1, 1.5, 0], RED, .6)
        self.play(FadeIn(eye), eye.animate.shift(RIGHT*10.2), run_time=2.2)
        self.add(scope_tag("schematic"))
        self.finish()


class S10Attacks(FilmScene):
    def construct(self):
        p = Plot(box=(-5.6, 5.5, -1.85, 2.5), xr=(0, 4), yr=(0, 18), xticks=[],
                 yticks=[0, 5, 10, 15], ylabel="attacks recorded")
        self.play(Create(p), run_time=.9)
        self.at("recorded attacks")
        xs, vals = [.55, 1.45, 2.55, 3.45], [5, 2, 16, 5]
        cols = [RED, GREEN, RED, GREEN]
        names = ["dark / sand", "light / sand", "light / soil", "dark / soil"]
        bars = VGroup(*[Rectangle(width=.72, height=(v/18)*4.65, stroke_width=0, fill_color=c, fill_opacity=.9)
                        .move_to(p.pt(x, v/2)) for x, v, c in zip(xs, vals, cols)])
        labels = VGroup(*[T(n, 24, c).move_to([p.pt(x, 0)[0], -2.35, 0]) for x, n, c in zip(xs, names, cols)])
        nums = VGroup(*[M(str(v), 30, c).next_to(b, UP, buff=.12) for v, c, b in zip(vals, cols, bars)])
        marks = VGroup()
        for b in bars:
            c = b.get_center()
            marks.add(Line(c+LEFT*.18+DOWN*.15, c+RIGHT*.18+UP*.15, color=TEXT, stroke_width=5),
                      Line(c+LEFT*.18+UP*.15, c+RIGHT*.18+DOWN*.15, color=TEXT, stroke_width=5))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=.18), FadeIn(labels), run_time=2.0)
        self.play(FadeIn(nums), FadeIn(marks), run_time=.7)
        self.at("mismatched received more")
        self.play(Indicate(bars[0], color=RED), Indicate(bars[2], color=RED), run_time=1.0)
        self.at("matching mattered")
        cap = caption("mismatch: more attacks on both grounds", 30, RED)
        self.play(FadeIn(cap), run_time=.6)
        self.finish()


class S10bTotal(FilmScene):
    def construct(self):
        source = VGroup(*[Rectangle(width=.75, height=h, fill_color=c, fill_opacity=.9, stroke_width=0)
                          for h, c in zip([1.0, .4, 3.2, 1.0], [RED, GREEN, RED, GREEN])])
        source.arrange(RIGHT, buff=.35).move_to([0, 1.9, 0])
        self.play(FadeIn(source), run_time=.5)
        self.at("Add the attack bars")
        red_bin = RoundedRectangle(corner_radius=.2, width=4.4, height=3.5, color=RED, stroke_width=5).move_to([-3.0, -.5, 0])
        green_bin = RoundedRectangle(corner_radius=.2, width=4.4, height=3.5, color=GREEN, stroke_width=5).move_to([3.0, -.5, 0])
        fills = VGroup(Rectangle(width=4.05, height=2.6, stroke_width=0, fill_color=RED, fill_opacity=.55).align_to(red_bin, DOWN).shift(UP*.18),
                       Rectangle(width=4.05, height=.9, stroke_width=0, fill_color=GREEN, fill_opacity=.55).align_to(green_bin, DOWN).shift(UP*.18))
        self.play(FadeIn(red_bin), FadeIn(green_bin), Transform(source, fills), run_time=1.8)
        self.at("Most marks landed")
        labs = VGroup(T("mismatched", 34, RED).move_to([-3, 1.65, 0]),
                      T("matched", 34, GREEN).move_to([3, 1.65, 0]))
        self.play(FadeIn(labs), run_time=.6)
        self.at("across both habitats")
        grounds = VGroup(T("light sand", 28, YELLOW).move_to([-3, -2.8, 0]),
                         T("dark soil", 28, GREY).move_to([3, -2.8, 0]))
        self.play(FadeIn(grounds), run_time=.6)
        self.at("matching, not one color")
        rule = caption("The pattern follows matching—not one color.", 32, YELLOW)
        self.play(FadeOut(grounds), FadeIn(rule), run_time=.8)
        pulse(red_bin, base=5, amp=1.5, speed=2)
        self.finish()


class S11Limit(FilmScene):
    def construct(self):
        tp = TwoPanel("Montana hare estimates", "Florida clay attacks", colors=(BLUE, GREEN))
        axes = VGroup(Line([-5.55, -.9, 0], [-1.1, -.9, 0], color=GREY, stroke_width=4),
                      Line([-5.55, -.9, 0], [-5.55, 1.5, 0], color=GREY, stroke_width=4))
        data = VGroup(Line([-5.15, 1.15, 0], [-3.45, .45, 0], color=TEXT, stroke_width=5),
                      Line([-3.45, .45, 0], [-1.55, -.35, 0], color=TEXT, stroke_width=5),
                      Dot([-5.15, 1.15, 0], radius=.14, color=GREEN),
                      Dot([-3.45, .45, 0], radius=.14, color=YELLOW),
                      Dot([-1.55, -.35, 0], radius=.14, color=RED))
        mini_plot = VGroup(axes, data)
        bars = VGroup(*[Rectangle(width=.45, height=h, stroke_width=0, fill_color=c, fill_opacity=.9)
                        for h, c in zip([1.0, .4, 2.6, 1.0], [RED, GREEN, RED, GREEN])]).arrange(RIGHT, buff=.22)
        tp.put(mini_plot, "left"); tp.put(bars, "right")
        self.play(FadeIn(tp), FadeIn(mini_plot), FadeIn(bars), run_time=.9)
        self.at("neither proves")
        frame = SurroundingRectangle(VGroup(tp, mini_plot, bars), color=YELLOW, buff=.12, corner_radius=.2)
        label = T("evidence, not certainty", 34, YELLOW).move_to([0, -3.05, 0])
        self.play(Create(frame), FadeIn(label), run_time=.8)
        self.at("movement, sound")
        icons = VGroup(chip("movement", TEXT, 26), chip("sound", TEXT, 26),
                       chip("smell", TEXT, 26), chip("cover", TEXT, 26)).arrange(RIGHT, buff=.25).move_to([0, 1.55, 0])
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN*.15) for i in icons], lag_ratio=.2), run_time=1.4)
        pulse(frame, base=4, amp=1.2, speed=2)
        self.finish()


class S12Variation(FilmScene):
    def construct(self):
        world = timing_world()
        self.play(FadeIn(world[0]), FadeIn(world[1]), run_time=.8)
        self.at("different times")
        self.play(LaggedStart(*[Create(t) for t in world[2]], lag_ratio=.2), run_time=1.2)
        self.at("changing snow season")
        self.play(Create(world[3]), world[3].animate.shift(LEFT*1.4), run_time=1.5)
        states = VGroup(*[T(t, 28, c).move_to([x, 2.1, 0]) for x, t, c in
                          [(-4.4, "match", GREEN), (-1.5, "match", GREEN), (1.5, "mismatch", RED), (4.4, "mismatch", RED)]])
        self.play(LaggedStart(*[FadeIn(s) for s in states], lag_ratio=.2), run_time=1.0)
        self.add(scope_tag("schematic"))
        bob(world[1][0], amp=.035, speed=2)
        self.finish()


class S12bFlexibility(FilmScene):
    def construct(self):
        world = timing_world()
        self.add(world)
        self.at("shift spring molt timing")
        self.play(world[2][0].animate.shift(LEFT*.35), world[2][1].animate.shift(LEFT*.25), run_time=1.3)
        self.at("not enough")
        gaps = VGroup(*[Line([x, -2.35, 0], [x+.65, -2.35, 0], color=RED, stroke_width=8)
                        for x in [1.0, 3.6]])
        self.play(Create(gaps), run_time=.8)
        # Kokoro's aligned transcript spells the spoken "snowier" as two tokens.
        self.at("snow your resting spots")
        spots = VGroup(band(-3.2, 3.0, 2.3, 5.5, SNOW_C), band(3.2, 3.0, 2.3, 5.5, GROUND_C))
        labels = VGroup(T("snowy spot", 28, INK).move_to([-3.2, 2.65, 0]), T("bare spot", 28, TEXT).move_to([3.2, 2.65, 0]))
        self.play(FadeIn(spots), FadeIn(labels), run_time=.7)
        self.at("did not move")
        self.play(Indicate(world[1], color=RED, scale_factor=1.03), run_time=1.0)
        tag = chip("limited flexibility", BLUE, 30).move_to([0, 3.35, 0])
        self.play(FadeIn(tag), run_time=.5)
        self.finish()


class S13Population(FilmScene):
    def construct(self):
        track = generations_track()
        self.play(FadeIn(track), run_time=.7)
        groups = []
        counts = [(2, 2), (3, 2), (4, 2)]
        for x, (early, late) in zip([-4.25, 0, 4.25], counts):
            a = VGroup(*[stand(hare(BROWN_C, .32, BLUE), 0, 0) for _ in range(early)]).arrange_in_grid(2, buff=.2)
            b = VGroup(*[stand(hare(WHITE_C, .32), 0, 0) for _ in range(late)]).arrange_in_grid(2, buff=.2)
            g = VGroup(a, b).arrange(DOWN, buff=.28).move_to([x, -.15, 0]); groups.append(g)
        self.at("inherited")
        self.play(FadeIn(groups[0]), run_time=.6)
        arrows = VGroup(Arrow([-2.55, 0, 0], [-1.7, 0, 0], color=BLUE, buff=0),
                        Arrow([1.7, 0, 0], [2.55, 0, 0], color=BLUE, buff=0))
        self.at("survive and leave more young")
        self.play(GrowArrow(arrows[0]), FadeIn(groups[1]), run_time=1.1)
        self.at("many generations")
        self.play(GrowArrow(arrows[1]), FadeIn(groups[2]), run_time=1.1)
        self.at("may become more common")
        cap = caption("earlier timing may become more common", 32, BLUE)
        self.play(FadeIn(cap), run_time=.6)
        bob(groups[2], amp=.03, speed=2)
        self.add(scope_tag("schematic"))
        self.finish()


class S14Rule(FilmScene):
    def construct(self):
        track = generations_track().set_opacity(.45)
        h = stand(hare(WHITE_C, 1.15), -3.9, -1.4)
        self.play(FadeIn(track), FadeIn(h), run_time=.7)
        self.at("populations change")
        bars = VGroup(*[Rectangle(width=.65, height=hgt, stroke_width=0, fill_color=BLUE, fill_opacity=.75)
                        .move_to([x, -1.0+hgt/2, 0]) for x, hgt in zip([-.7, 0, .7], [.8, 1.5, 2.2])])
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=.2), run_time=1.3)
        self.at("One hair molts")
        self.play(h.body.animate.set_fill(BROWN_C, 1), run_time=1.6)
        self.at("does not choose")
        no = chip("not a choice", RED, 30).move_to([-3.8, 1.45, 0])
        self.play(FadeIn(no), run_time=.6)
        rule = fit_text("Adaptations help in particular settings; populations change over generations, not individuals.",
                        max_w=11.8, size=34, color=YELLOW, max_lines=2).move_to([0, 3.15, 0])
        self.play(FadeIn(rule), run_time=.8)
        pulse(bars, base=1, amp=.5, speed=2)
        self.finish()


class S15Close(FilmScene):
    def construct(self):
        p = Plot(box=(-6.0, -.65, -1.35, 1.65), xr=(0, 100), yr=(87, 98),
                 xticks=[(0, "0"), (100, "100")], yticks=[(89, "89%"), (96, "96%")],
                 size=22, label_size=24)
        d = reported_points(p)
        track = Arrow([.2, -.2, 0], [5.8, -.2, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=.25)
        self.play(FadeIn(p), Create(d), GrowArrow(track), run_time=1.0)
        self.at("lower estimated survival")
        self.play(Indicate(d[-1], color=RED, scale_factor=1.5), run_time=.8)
        self.at("Variation gives selection")
        paths = VGroup(Arrow([.8, .45, 0], [5.4, 1.4, 0], color=GREEN, stroke_width=5),
                       Arrow([.8, -.85, 0], [4.6, -1.5, 0], color=RED, stroke_width=5))
        clouds = VGroup(Ellipse(width=5.0, height=1.25, color=GREEN, fill_color=GREEN, fill_opacity=.08).move_to([3.1, 1.0, 0]),
                        Ellipse(width=4.2, height=1.25, color=RED, fill_color=RED, fill_opacity=.08).move_to([2.8, -1.2, 0]))
        self.play(FadeIn(clouds), GrowArrow(paths[0]), GrowArrow(paths[1]), run_time=1.4)
        self.at("if timing is inherited")
        condition = chip("if timing is inherited", BLUE, 30).move_to([3.15, 2.45, 0])
        may = chip("may", YELLOW, 30).move_to([5.25, -2.05, 0])
        self.play(FadeIn(condition), FadeIn(may), run_time=.7)
        self.at("field setting")
        place = caption("The field setting still matters.", 32, YELLOW)
        self.play(FadeIn(place), run_time=.6)
        pulse(clouds, base=3, amp=1, speed=2)
        self.finish()


class S16End(EndCard):
    LINE = "Adaptations help in particular settings;\npopulations change over generations, not individuals."
