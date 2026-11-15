"""Heritability Is About Variation.

COLOR MAP
  BLUE = measured genetic differences / additive effects
  GREY = environment, context, and neutral structure
  GOLD = questions, scope, and candidate causes
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


BASE_Y = -1.45
PERSON_X = np.linspace(-4.8, 4.8, 9)
TILE_COUNTS = [1, 2, 3, 4, 5, 4, 3, 2, 1]


class FilmScene(SpokenScene):
    """Spoken scene with the film's quiet, continuously moving population texture."""
    def setup(self):
        super().setup()
        motes = VGroup()
        for i in range(180):
            x = -6.35 + (i % 30) * .44
            y = -3.38 + (i // 30) * 1.24 + (i % 3) * .08
            d = Dot([x, y, 0], radius=.066 + .008 * (i % 2), color=GREY).set_opacity(.22)
            d.v = 1.05 + .045 * (i % 5)
            def drift(m, dt):
                m.shift(RIGHT * m.v * dt)
                if m.get_x() > 6.55:
                    m.shift(LEFT * 13.0)
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-20)
        self.add(motes)


def person(x=0, base=BASE_Y, height=2.15, color=TEXT, opacity=0.32):
    """The one carried person drawing, rebuilt at the same scale everywhere."""
    head = Circle(radius=0.23, color=color, stroke_width=3, fill_color=color, fill_opacity=opacity)
    body = RoundedRectangle(width=0.62, height=height - 0.48, corner_radius=0.16,
                            color=color, stroke_width=3, fill_color=color, fill_opacity=opacity)
    body.move_to([x, base + (height - 0.48) / 2, 0])
    head.move_to([x, base + height - 0.23, 0])
    return VGroup(body, head)


def crowd(base=BASE_Y, scale=1.0, opacity=0.22):
    heights = [1.65, 2.05, 2.35, 2.65, 2.9, 2.65, 2.35, 2.05, 1.65]
    return VGroup(*[person(x, base, h * scale, opacity=opacity) for x, h in zip(PERSON_X, heights)])


def tile_stack(x, n, y=-2.45):
    return VGroup(*[RoundedRectangle(width=0.46, height=0.20, corner_radius=0.04,
                                     color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.55)
                    .move_to([x, y + i * 0.23, 0]) for i in range(n)])


def genetic_tiles():
    return VGroup(*[tile_stack(x, n) for x, n in zip(PERSON_X, TILE_COUNTS)])


def normal_pdf(x, sigma=1.0):
    return np.exp(-0.5 * (x / sigma) ** 2)


def distribution_area(p, sigma=1.0, color=BLUE, opacity=.19):
    xs = np.linspace(-4, 4, 90)
    pts = [p.pt(-4, 0), *[p.pt(x, normal_pdf(x, sigma)) for x in xs], p.pt(4, 0)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def distribution_plot():
    return Plot(box=(-5.65, 5.15, -2.25, 2.25), xr=(-4, 4), yr=(0, 1.05),
                xticks=[-4, -2, 0, 2, 4], yticks=(), xlabel="trait value", ylabel="people")


def curve_world(sigma=1.35, include_thin=True, dots=False):
    p = distribution_plot()
    wide = p.curve(lambda x: normal_pdf(x, sigma), color=GREY, width=8)
    out = VGroup(p, wide, distribution_area(p, sigma, GREY, .19))
    if include_thin:
        out.add(p.curve(lambda x: normal_pdf(x, 0.92), color=BLUE, width=5),
                distribution_area(p, .92, BLUE, .15))
    if dots:
        beads = VGroup(*[Dot(p.pt(x, normal_pdf(x, sigma)), radius=0.065, color=TEXT)
                         for x in np.linspace(-3.1, 3.1, 19)])
        out.add(beads)
    return out


def variance_containers():
    specs = [("additive", BLUE, 0.46), ("dominance", BLUE, 0.20),
             ("interaction", BLUE, 0.14), ("environment", GREY, 0.38)]
    xs = [-4.65, -1.55, 1.55, 4.65]
    groups = VGroup()
    for (name, col, fill), x in zip(specs, xs):
        box = RoundedRectangle(width=2.55, height=2.75, corner_radius=0.16, color=col,
                               stroke_width=3, fill_color=col, fill_opacity=0.12).move_to([x, -0.35, 0])
        level = Rectangle(width=2.18, height=1.65 * fill + 0.28, stroke_width=0,
                          fill_color=col, fill_opacity=0.55).set_x(x).align_to(box, DOWN).shift(UP * 0.18)
        label = T(name, 28, col).next_to(box, DOWN, buff=0.24)
        groups.add(VGroup(box, level, label))
    return groups


def hbracket(y, x0, x1, color=GOLD, down=True):
    tick = -0.20 if down else 0.20
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=5),
                  Line([x0, y, 0], [x0, y + tick, 0], color=color, stroke_width=5),
                  Line([x1, y, 0], [x1, y + tick, 0], color=color, stroke_width=5))


def predict_backdrop(wide=False):
    """Exact shared frame for the spoken question, pause, and reveal."""
    p = Plot(box=(-5.7, 3.65, -1.65, 2.10), xr=(-4, 4), yr=(0, 1.05),
             xticks=[-4, 0, 4], yticks=(), xlabel="trait value", ylabel="people")
    genetic = p.curve(lambda x: normal_pdf(x, 0.92), color=BLUE, width=6)
    env_sigma = 1.55 if wide else 1.28
    env = p.curve(lambda x: normal_pdf(x, env_sigma), color=GREY, width=8)
    arrows = VGroup(*[DoubleArrow(p.pt(x - (0.34 if wide else 0.2), 0.08),
                                  p.pt(x + (0.34 if wide else 0.2), 0.08),
                                  color=GREY, stroke_width=3, buff=0, tip_length=0.12)
                      for x in (-2.3, -1.15, 0, 1.15, 2.3)])
    tiles = VGroup(*[RoundedRectangle(width=0.34, height=0.17, corner_radius=0.03,
                                      color=BLUE, fill_color=BLUE, fill_opacity=0.55, stroke_width=2)
                     .move_to([x, 2.72, 0]) for x in np.linspace(-4.7, 2.7, 9)])
    areas = VGroup(distribution_area(p, env_sigma, GREY, .19), distribution_area(p, .92, BLUE, .14))
    return VGroup(p, env, genetic, arrows, tiles, areas)


def twin_pair(x, identical=True):
    a = person(x - 0.43, -1.15, 2.15, BLUE if identical else TEXT, 0.18)
    b = person(x + 0.43, -1.15, 2.15, BLUE if identical else TEXT, 0.18)
    band = DoubleArrow([x - 0.75, 1.35, 0], [x + 0.75, 1.35, 0], color=BLUE if identical else GREY,
                       stroke_width=6, buff=0, tip_length=0.18)
    return VGroup(a, b, band)


class S01Hook(FilmScene):
    def construct(self):
        lone = person(0, -2.35, 5.35, TEXT, 0.18)
        q = question_card("How much of your height came from genes?", y=-3.15, size=34)
        self.play(FadeIn(lone, shift=UP * 0.2), run_time=0.8)
        self.at("does that tell you")
        self.play(FadeIn(q.question, shift=UP * 0.15), run_time=0.7)
        self.at("Now")
        no = boxed_label("No.", GOLD, 48, box=(1.8, .95)).move_to([-4.8, 2.75, 0])
        self.play(FadeIn(no, scale=0.8), FadeOut(q.question), run_time=0.6)
        self.at("describes differences")
        many = crowd()
        self.play(Transform(lone, many[4]), FadeOut(no),
                  LaggedStart(*[FadeIn(m, shift=(LEFT if i < 4 else RIGHT) * 0.25)
                                for i, m in enumerate(many) if i != 4], lag_ratio=0.06), run_time=1.4)
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), run_time=0.4)
        bob(lone, amp=0.025, speed=1.6)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        people = crowd(opacity=0.13)
        title = T("Heritability Is About Variation", 52, font=TITLE_FONT).move_to([0, 2.8, 0])
        rule = Line([-5.2, 2.15, 0], [5.2, 2.15, 0], color=GOLD, stroke_width=4)
        self.add(people)
        self.play(Write(title), Create(rule), run_time=0.8)
        baseline = Line([-5.2, -1.45, 0], [5.2, -1.45, 0], color=GREY, stroke_width=4)
        self.play(ReplacementTransform(rule, baseline), FadeOut(title, shift=DOWN * 0.25), run_time=0.7)
        self.finish()


class S03Tiles(FilmScene):
    def construct(self):
        people = crowd(base=-0.65, scale=0.82)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in people], lag_ratio=0.05), run_time=1.0)
        self.at("Give each small effect")
        tiles = genetic_tiles().shift(UP * 0.45)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.7) for s in tiles], lag_ratio=0.07), run_time=1.8)
        self.at("Few people collect")
        self.play(Indicate(VGroup(tiles[0], tiles[-1]), color=GOLD, scale_factor=1.06), run_time=0.8)
        self.at("Most gather combinations")
        self.play(Indicate(VGroup(*tiles[2:7]), color=BLUE, scale_factor=1.04), run_time=1.0)
        self.at("With more loci")
        copies = VGroup(*[s.copy().scale(0.72) for s in tiles]).arrange(RIGHT, buff=0.22).move_to([0, -2.65, 0])
        self.play(Transform(tiles, copies), run_time=1.5)
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), run_time=0.35)
        for s in tiles:
            pulse(s, base=2.0, amp=0.5, speed=2.0)
        self.finish()


class S04Curve(FilmScene):
    def construct(self):
        p = distribution_plot()
        bars = VGroup(*[Rectangle(width=0.7, height=h, color=BLUE, stroke_width=2,
                                  fill_color=BLUE, fill_opacity=0.35)
                        .move_to(p.pt(x, 0) + UP * h / 2)
                        for x, h in zip(np.linspace(-3.4, 3.4, 9), [0.25, .42, .62, .82, 1.0, .82, .62, .42, .25])])
        self.add(p, bars)
        self.at("environmental differences")
        arrows = VGroup(*[Arrow(p.pt(x, .12), p.pt(x + d, .12), color=GREY, buff=0, tip_length=.16)
                          for x, d in zip(np.linspace(-3, 3, 7), [-.35,.25,-.2,.3,-.3,.2,.35])])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.08), run_time=1.2)
        thin = p.curve(lambda x: normal_pdf(x, .92), color=BLUE, width=6)
        self.at("columns blur")
        self.play(ReplacementTransform(bars, thin), FadeOut(arrows), run_time=1.5)
        wide = p.curve(lambda x: normal_pdf(x, 1.35), color=GREY, width=8)
        area = distribution_area(p, 1.35, GREY, .20)
        self.at("then widened")
        self.play(Create(wide), FadeIn(area), run_time=1.7)
        dots = VGroup(*[Dot(p.pt(x, normal_pdf(x, 1.35)), radius=.065, color=TEXT)
                        for x in np.linspace(-3, 3, 17)])
        self.play(FadeIn(dots), run_time=.5)
        tag = scope_tag("computed simulation")
        self.at("picture is a model")
        self.play(FadeIn(tag), run_time=.5)
        bob(dots, amp=.025, speed=1.4)
        self.finish()


class S05Variance(FilmScene):
    def construct(self):
        curve = curve_world(1.35, include_thin=False)[1].scale(.55).move_to([0, 2.75, 0])
        self.play(Create(curve), run_time=.8)
        self.at("partition that spread")
        boxes = variance_containers()
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN*.2) for g in boxes], lag_ratio=.13), run_time=1.7)
        total = hbracket(1.45, -5.95, 5.95)
        lab = T("total spread", 30, GOLD).next_to(total, UP, buff=.18)
        self.play(Create(total), FadeIn(lab), FadeOut(curve), run_time=.8)
        self.at("additive part")
        self.play(Indicate(boxes[0], color=BLUE, scale_factor=1.03), run_time=1.0)
        self.at("helps predict resemblance")
        parent = person(-5.05, 1.68, 1.35, BLUE, .18)
        child = person(-4.15, 1.68, 1.0, BLUE, .18)
        self.play(FadeIn(VGroup(parent, child), shift=DOWN*.15), run_time=.8)
        self.at("only under")
        tag = scope_tag("simplified model")
        self.play(FadeIn(tag), run_time=.4)
        for g in boxes:
            bob(g[1], amp=.025, speed=1.3)
        self.finish()


class S06Ratios(FilmScene):
    def construct(self):
        boxes = variance_containers()
        total = hbracket(1.45, -5.95, 5.95)
        den = T("total phenotypic variance", 28, GREY).next_to(total, UP, buff=.18)
        self.add(boxes, total, den)
        self.at("additive variance")
        num1 = hbracket(-2.62, -5.9, -3.4, BLUE, down=False)
        f1 = M("h² = V_A / V_P", 38, BLUE).move_to([0, 2.45, 0])
        self.play(Create(num1), FadeIn(f1), run_time=.8)
        self.at("Broad sense")
        num2 = hbracket(-2.62, -5.9, 2.8, BLUE, down=False)
        f2 = M("H² = V_G / V_P", 38, BLUE).move_to([0, 2.45, 0])
        self.play(ReplacementTransform(num1, num2), swap(f1, f2), run_time=1.0)
        self.at("no units")
        units = T("ratios • no units", 30, GOLD).move_to([0, -3.25, 0])
        self.play(FadeIn(units), run_time=.5)
        self.at("belong to the population")
        scope = T("population + environment", 30, GOLD).move_to([0, 3.25, 0])
        self.play(swap(f2, scope), FadeOut(units), run_time=.8)
        self.at("alter the denominator")
        self.play(Indicate(total, color=GREY, scale_factor=1.02), boxes[3][1].animate.stretch(1.35, 1), run_time=1.2)
        self.finish()


class S07Predict(FilmScene):
    def construct(self):
        world = predict_backdrop(False)
        self.add(world)
        self.at("Now make")
        wider = predict_backdrop(True)
        self.play(Transform(world[1], wider[1]), Transform(world[3], wider[3]), run_time=1.5)
        self.at("Will heritability")
        q = question_card("Will heritability rise, fall, or stay the same?", y=-3.12, size=32)
        q.question.add_background_rectangle(color=BG, opacity=.96, buff=.12)
        self.play(FadeIn(q.question, shift=UP*.12), run_time=.6)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Will heritability rise, fall, or stay the same?"
    SECONDS = 4.5
    CARD = {"y": -3.12, "size": 32}
    def backdrop(self):
        w = predict_backdrop(True)
        pulse(w[3], base=3.0, amp=1.2, speed=1.8)
        return w


class S09Reveal(FilmScene):
    def construct(self):
        world = predict_backdrop(True)
        h = ValueTracker(.68)
        gauge = dial(h, [5.05, .4, 0], radius=1.15, label="heritability", color=BLUE)
        tag = scope_tag("computed simulation")
        self.add(world, gauge, tag)
        self.at("so heritability falls")
        self.play(h.animate.set_value(.36), world[1].animate.set_stroke(width=10), run_time=1.5)
        self.at("Reverse the change")
        narrow = predict_backdrop(False)
        self.play(Transform(world[1], narrow[1]), Transform(world[3], narrow[3]),
                  h.animate.set_value(.68), run_time=1.6)
        self.at("A ratio changes")
        rule = caption("A ratio changes when one part changes.", color=GOLD, y=-3.1)
        self.play(FadeIn(rule), run_time=.6)
        self.finish()


class S10Person(FilmScene):
    def construct(self):
        people = crowd(opacity=.12)
        label = T("heritability", 30, BLUE).move_to([0, 2.85, 0])
        self.add(people, label)
        self.at("one person's height")
        lone = person(0, -2.25, 4.55, TEXT, .22)
        self.play(FadeOut(VGroup(*[p for i,p in enumerate(people) if i != 4])),
                  Transform(people[4], lone), run_time=1.2)
        split = VGroup(Rectangle(width=1.25, height=1.25, color=BLUE, fill_color=BLUE, fill_opacity=.35),
                       Rectangle(width=1.25, height=1.25, color=GREY, fill_color=GREY, fill_opacity=.35))
        split.arrange(RIGHT, buff=.08).move_to([3.5, .3, 0])
        self.play(FadeIn(split), run_time=.5)
        self.at("no population variance")
        self.play(FadeOut(split, scale=.6), label.animate.set_opacity(.22), run_time=.8)
        self.at("trait cannot change")
        env = Arrow([-2.8,-.5,0], [-2.8,1.0,0], color=GREY, stroke_width=7)
        self.play(GrowArrow(env), people[4].animate.shift(UP*.7), run_time=1.2)
        self.finish()


class S11Groups(FilmScene):
    def construct(self):
        panels = TwoPanel("group A", "group B", colors=(BLUE, BLUE), top=3.0, bottom=-2.15)
        self.play(FadeIn(panels), run_time=.7)
        def mini_curve(cx):
            ax = Line([cx-2.35,-1.35,0],[cx+2.35,-1.35,0],color=GREY,stroke_width=3)
            pts = [[cx+x, -1.35+2.4*normal_pdf(x,1.05), 0] for x in np.linspace(-2.2,2.2,70)]
            cv = VMobject(color=BLUE, stroke_width=7).set_points_smoothly(pts)
            fill = Polygon([cx-2.2,-1.35,0], *pts, [cx+2.2,-1.35,0], stroke_width=0,
                           fill_color=BLUE, fill_opacity=.20)
            return VGroup(ax,cv,fill)
        a, b = mini_curve(-3.3), mini_curve(3.3)
        self.play(Create(a), Create(b), run_time=1.2)
        self.at("does not explain")
        q = T("?", 64, GOLD, weight=BOLD).move_to([0,3.35,0])
        self.play(FadeIn(q, scale=.7), run_time=.5)
        self.at("Different environments")
        arr = Arrow([1.2,-2.55,0],[5.3,-2.55,0],color=GREY,stroke_width=7)
        self.play(GrowArrow(arr), b.animate.shift(RIGHT*.65), run_time=1.5)
        tag = scope_tag("schematic analogy")
        self.play(FadeIn(tag), run_time=.4)
        pulse(VGroup(a[1],b[1]), base=7, amp=1, speed=1.5)
        self.finish()


class S12Twins(FilmScene):
    def construct(self):
        xs = np.linspace(-5.7, 5.7, 90)
        pts = [[x, -1.45 + 2.55 * normal_pdf(x / 1.4, 1.45), 0] for x in xs]
        population = Polygon([-5.7,-1.45,0], *pts, [5.7,-1.45,0], stroke_color=GREY,
                             stroke_width=5, fill_color=GREY, fill_opacity=.16)
        self.add(population)
        idp, frp = twin_pair(-3.15, True), twin_pair(1.1, False)
        li = T("identical", 30, BLUE).move_to([-3.15,-2.0,0])
        lf = T("fraternal", 30, GREY).move_to([1.1,-2.0,0])
        self.play(FadeIn(idp, shift=RIGHT*.2), FadeIn(frp, shift=LEFT*.2), FadeIn(li), FadeIn(lf), run_time=1.1)
        self.at("Under their assumptions")
        assumptions = boxed_label("equal environments • additive effects • random mating", GOLD, 28,
                                  box=(-.8, 1.35), min_size=24).move_to([0,2.75,0])
        self.play(FadeIn(assumptions), run_time=.6)
        self.at("extra similarity")
        gap = DoubleArrow(idp[2].get_right()+RIGHT*.15, frp[2].get_left()+LEFT*.15,
                          color=GOLD, stroke_width=5, buff=0, tip_length=.16)
        self.play(Create(gap), run_time=.8)
        self.at("Doubling that gap")
        cbox = RoundedRectangle(width=2.25, height=2.45, corner_radius=.15, color=BLUE,
                                fill_color=BLUE, fill_opacity=.12, stroke_width=3).move_to([5.15,-.25,0])
        clevel = Rectangle(width=1.9, height=.95, stroke_width=0, fill_color=BLUE,
                           fill_opacity=.42).set_x(5.15).align_to(cbox, DOWN).shift(UP*.18)
        clabel = T("additive", 28, BLUE).next_to(cbox, DOWN, buff=.2)
        container = VGroup(cbox, clevel, clabel)
        self.play(gap.animate.scale(1.5), FadeIn(container, shift=LEFT*.2), run_time=1.0)
        self.at("sampled population")
        scope = T("sampled population + environment", 28, GOLD).move_to([0,-3.05,0])
        self.play(FadeIn(scope), run_time=.5)
        self.finish()


class S13Rule(FilmScene):
    def construct(self):
        twins = VGroup(twin_pair(-2.1,True), twin_pair(2.1,False)).scale(.85)
        self.add(twins)
        self.at("create smooth variation")
        people = crowd(base=-1.4, scale=.85)
        self.play(ReplacementTransform(twins, people), run_time=1.1)
        pworld = curve_world(1.35, include_thin=True, dots=True)
        self.play(ReplacementTransform(people, pworld), run_time=1.2)
        self.at("variation is partitioned")
        boxes = variance_containers().scale(.83).shift(DOWN*.15)
        curve = VGroup(pworld[1].copy(), pworld[2].copy()).scale(.45).move_to([0,2.45,0])
        self.play(FadeOut(pworld), FadeIn(boxes), Create(curve), run_time=1.2)
        self.at("Keep the scope")
        scope = boxed_label("population + environment", GOLD, 34, box=(5.8,1.0)).move_to([0,2.75,0])
        self.play(ReplacementTransform(curve, scope), run_time=.8)
        for g in boxes:
            bob(g[1], amp=.02, speed=1.25)
        self.finish()


class S14End(EndCard):
    LINE = "Heritability describes variation in a population and environment, never a person."
