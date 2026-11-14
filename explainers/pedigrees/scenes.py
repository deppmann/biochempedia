"""The pedigree as a model test.

The family chart is the film's one world.  Every scene that uses it calls
``pedigree()`` (or the fixed-position ``x_focus()`` crop), so symbols and
relationships never drift between cuts.
"""
from bp_parts import *


VIOLET = "#B48EDE"
WHITE = TEXT


def breathe_stage(stage, speed=1.65):
    """A slow blue color breath across the family's stage during spoken holds."""
    stage._breath_t = 0.0
    dark, light = ManimColor("#1B2840"), ManimColor("#476D9A")

    def update(mob, dt):
        mob._breath_t += dt
        mix = 0.5 + 0.5 * np.sin(speed * mob._breath_t)
        mob.set_fill(interpolate_color(dark, light, mix), opacity=0.72)
    return stage.add_updater(update)


def person(kind, affected=False, side=0.72, color=WHITE):
    """A conventional pedigree symbol; the chart key gives the meaning."""
    if kind == "male":
        shape = Square(side_length=side)
    else:
        shape = Circle(radius=side / 2)
    shape.set_stroke(color, 4)
    shape.set_fill(RED if affected else BG, 0.92 if affected else 1.0)
    return shape


def check(at, scale=0.32):
    a = np.array(at) + np.array([-0.28, 0.00, 0]) * scale / 0.32
    b = np.array(at) + np.array([-0.06, -0.22, 0]) * scale / 0.32
    c = np.array(at) + np.array([0.32, 0.25, 0]) * scale / 0.32
    return VMobject(color=TEAL, stroke_width=7).set_points_as_corners([a, b, c])


def cross_mark(at, width=0.62, color=VIOLET):
    c = np.array(at)
    d = width / 2
    return VGroup(Line(c + [-d, -d, 0], c + [d, d, 0], color=color, stroke_width=7),
                  Line(c + [-d, d, 0], c + [d, -d, 0], color=color, stroke_width=7))


def pedigree(shift=ORIGIN, opacity=1.0):
    """The carried three-generation family, always rebuilt at one scale."""
    stage = RoundedRectangle(corner_radius=0.28, width=12.1, height=6.35, stroke_width=0,
                             fill_color="#273247", fill_opacity=0.72).set_z_index(-6)
    breathe_stage(stage)
    p = {}
    p["f0"] = person("male").move_to([-1.45, 2.38, 0])
    p["m0"] = person("female", affected=True).move_to([1.45, 2.38, 0])
    p["d1"] = person("female", affected=True).move_to([-3.85, 0.35, 0])
    p["s1"] = person("male").move_to([-2.55, 0.35, 0])
    p["s2"] = person("male", affected=True).move_to([0.0, 0.35, 0])
    p["d2"] = person("female").move_to([3.45, 0.35, 0])
    p["s3"] = person("male", affected=True).move_to([4.75, 0.35, 0])
    p["g1"] = person("female").move_to([-0.95, -2.05, 0])
    p["g2"] = person("male", affected=True).move_to([0.95, -2.05, 0])

    lines = VGroup(
        Line([-1.09, 2.38, 0], [1.09, 2.38, 0]),
        Line([0, 2.38, 0], [0, 1.55, 0]),
        Line([-3.85, 1.55, 0], [3.45, 1.55, 0]),
        Line([-3.85, 1.55, 0], [-3.85, 0.71, 0]),
        Line([0, 1.55, 0], [0, 0.71, 0]),
        Line([3.45, 1.55, 0], [3.45, 0.71, 0]),
        Line([-3.49, 0.35, 0], [-2.91, 0.35, 0]),
        Line([3.81, 0.35, 0], [4.39, 0.35, 0]),
        Line([0, -0.01, 0], [0, -0.92, 0]),
        Line([-0.95, -0.92, 0], [0.95, -0.92, 0]),
        Line([-0.95, -0.92, 0], [-0.95, -1.69, 0]),
        Line([0.95, -0.92, 0], [0.95, -1.69, 0]),
    ).set_stroke(WHITE, 4)
    pulse(lines, base=4.0, amp=1.35, speed=3.2)
    people = VGroup(*p.values())
    world = VGroup(stage, lines, people)
    world.stage, world.lines, world.people, world.p = stage, lines, people, p
    world.shift(shift).set_opacity(opacity)
    return world


def model_card(text, color=GOLD, at=(0, 0, 0), width=11.8, height=5.55):
    frame = RoundedRectangle(corner_radius=0.22, width=width, height=height,
                             stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.10).move_to(at)
    label = fit_text(text, max_w=width - 0.7, size=28, color=color).move_to(frame.get_top() + UP * 0.35)
    return VGroup(frame, label)


def route(points, color=GOLD, dashed=False, width=7):
    cls = DashedVMobject if dashed else None
    path = VMobject(color=color, stroke_width=width).set_points_as_corners([np.array(p) for p in points])
    return cls(path, num_dashes=18) if dashed else path


def pedigree_key():
    male = person("male", side=0.42)
    female = person("female", side=0.42)
    affected = person("male", True, side=0.42)
    rows = VGroup(VGroup(male, T("person", 28)).arrange(RIGHT, buff=0.18),
                  VGroup(female, T("person", 28)).arrange(RIGHT, buff=0.18),
                  VGroup(affected, T("affected", 28, RED)).arrange(RIGHT, buff=0.18))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    box = RoundedRectangle(corner_radius=0.16, width=2.6, height=2.0,
                           stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.92)
    rows.move_to(box)
    return VGroup(box, rows).move_to([-5.25, -2.15, 0])


def x_focus(show_question=False):
    """Fixed father/mother/daughter/son crop used unchanged in s06--s09."""
    stage = RoundedRectangle(corner_radius=0.28, width=11.5, height=5.65, stroke_width=0,
                             fill_color="#273247", fill_opacity=0.72).set_z_index(-6)
    breathe_stage(stage)
    father = person("male", True, side=1.12).move_to([-2.25, 1.45, 0])
    mother = person("female", False, side=1.12).move_to([2.25, 1.45, 0])
    daughter = person("female", False, side=1.12).move_to([-2.25, -1.55, 0])
    son = person("male", True, side=1.12).move_to([2.25, -1.55, 0])
    lines = VGroup(Line([-1.69, 1.45, 0], [1.69, 1.45, 0]),
                   Line([0, 1.45, 0], [0, 0.25, 0]),
                   Line([-2.25, 0.25, 0], [2.25, 0.25, 0]),
                   Line([-2.25, 0.25, 0], [-2.25, -0.99, 0]),
                   Line([2.25, 0.25, 0], [2.25, -0.99, 0])).set_stroke(WHITE, 5)
    pulse(lines, base=5.0, amp=1.5, speed=3.2)
    g = VGroup(stage, lines, father, mother, daughter, son)
    g.stage, g.father, g.mother, g.daughter, g.son, g.lines = stage, father, mother, daughter, son, lines
    if show_question:
        qpath = route([[-2.25, 0.89, 0], [-2.25, 0.25, 0], [2.25, 0.25, 0], [2.25, -0.99, 0]], dashed=True)
        pulse(qpath, base=5.5, amp=1.8, speed=2.2)
        g.add(qpath)
        g.qpath = qpath
    return g


def chromosome(label, color, at):
    bar = RoundedRectangle(corner_radius=0.12, width=0.52, height=1.2,
                           stroke_color=color, stroke_width=3, fill_color="#10141F", fill_opacity=0.93)
    txt = M(label, 34, color, weight=BOLD).move_to(bar)
    return VGroup(bar, txt).move_to(at)


class S00Hook(SpokenScene):
    def construct(self):
        world = pedigree()
        question = T("?", 84, GOLD, weight=BOLD).move_to([5.8, 2.35, 0])
        self.play(LaggedStart(Create(world.lines), FadeIn(world.people), lag_ratio=0.28), run_time=2.7)
        self.play(FadeIn(question, shift=LEFT * 0.2), run_time=0.55)
        self.at("Watch this pedigree")
        trace = route([[-1.45, 2.38, 0], [0, 2.38, 0], [0, 1.55, 0], [0, 0.71, 0], [0, 0.35, 0]], width=8)
        self.play(Create(trace), question.animate.move_to([5.5, 0.2, 0]), run_time=1.5)
        self.at("The answer depends")
        card = model_card("what does the model allow?", at=[0, 0, 0])
        card[0].set_z_index(-1)
        self.play(FadeIn(card[0]), FadeIn(card[1], shift=DOWN * 0.1), run_time=1.0)
        self.at("This is why")
        pulse(trace, base=7, amp=2, speed=2.2)
        self.play(Indicate(card[1], color=GOLD, scale_factor=1.05), run_time=0.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Reading Pedigrees: Human Inheritance"
    TITLE = "The Pedigree as a Model Test"


class S02Code(SpokenScene):
    def construct(self):
        world = pedigree()
        self.play(FadeIn(world), run_time=0.8)
        self.at("Shapes identify")
        samples = VGroup(world.p["f0"].copy(), world.p["m0"].copy(), world.p["s2"].copy())
        samples.arrange(RIGHT, buff=0.48).scale(1.45).move_to([4.8, 2.45, 0])
        self.play(TransformFromCopy(VGroup(world.p["f0"], world.p["m0"], world.p["s2"]), samples), run_time=1.0)
        self.at("connecting lines")
        self.play(ShowPassingFlash(world.lines.copy().set_stroke(GOLD, 9), time_width=0.45), run_time=1.5)
        self.at("fill marks")
        self.play(Indicate(VGroup(world.p["m0"], world.p["s2"], world.p["s3"], world.p["g2"]),
                           color=RED, scale_factor=1.08), run_time=0.9)
        self.at("Always read its key")
        key = pedigree_key()
        self.play(FadeIn(key, shift=RIGHT * 0.15), FadeOut(samples), run_time=0.8)
        self.at("The same symbol")
        tag = caption("The key names the phenotype.", color=GOLD)
        self.play(FadeIn(tag), run_time=0.7)
        self.finish()


class S03Models(SpokenScene):
    def construct(self):
        world = pedigree()
        card = model_card("inheritance model", at=[0, 0, 0])
        card[0].set_z_index(-2)
        self.add(world)
        self.play(FadeIn(card, shift=RIGHT * 0.25), run_time=0.9)
        self.at("Each inheritance model")
        r1 = route([[-1.45, 2.38, 0], [0, 2.38, 0], [0, 1.55, 0], [0, 0.35, 0]])
        r2 = route([[1.45, 2.38, 0], [0, 2.38, 0], [0, 1.55, 0], [3.45, 1.55, 0], [3.45, 0.35, 0]])
        self.play(Create(r1), Create(r2), run_time=2.2)
        self.at("which relatives")
        marks = VGroup(check([0.55, 0.35, 0]), check([4.0, 0.35, 0]))
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in marks], lag_ratio=0.5), run_time=1.1)
        self.at("The chart becomes evidence")
        pulse(VGroup(r1, r2), base=7, amp=1.5, speed=2.0)
        self.play(Indicate(world.lines, color=TEAL, scale_factor=1.01), run_time=1.0)
        self.finish()


class S04Autosomal(SpokenScene):
    def construct(self):
        world = pedigree()
        card = model_card("autosomal dominant — schematic")
        card[0].set_z_index(-2)
        self.add(card, world)
        self.at("either parent")
        left = route([[-1.45, 2.38, 0], [0, 2.38, 0], [0, 1.55, 0], [-3.85, 1.55, 0], [-3.85, 0.35, 0]])
        right = route([[1.45, 2.38, 0], [0, 2.38, 0], [0, 1.55, 0], [3.45, 1.55, 0], [3.45, 0.35, 0]])
        self.play(Create(left), Create(right), run_time=1.4)
        self.at("A dominant model")
        pulse(right, base=7, amp=2, speed=2.4)
        self.play(Indicate(world.p["m0"], color=RED, scale_factor=1.12), run_time=0.8)
        self.at("children of either sex")
        self.play(Indicate(VGroup(world.p["d1"], world.p["s2"]), color=GOLD, scale_factor=1.1), run_time=1.0)
        self.at("An affected child")
        contradiction = cross_mark(world.p["g2"].get_center(), width=0.95)
        note = caption("unaffected parents → affected child", color=VIOLET)
        self.play(Create(contradiction), FadeIn(note), run_time=1.0)
        self.finish()


class S05Recessive(SpokenScene):
    def construct(self):
        world = pedigree()
        card = model_card("autosomal recessive — schematic")
        card[0].set_z_index(-2)
        self.add(card, world)
        carrier_l = Arc(radius=0.25, start_angle=PI / 2, angle=PI, color=GOLD, stroke_width=8).next_to(world.p["s2"], LEFT, buff=0.18)
        carrier_r = Arc(radius=0.25, start_angle=-PI / 2, angle=PI, color=GOLD, stroke_width=8).next_to(world.p["d2"], RIGHT, buff=0.18)
        self.at("hide in unaffected carriers")
        lab = T("carrier", 30, GOLD).move_to([4.95, 2.35, 0])
        self.play(Create(carrier_l), Create(carrier_r), FadeIn(lab), run_time=1.0)
        self.at("when each parent contributes")
        lroute = route([[0, 0.35, 0], [0, -0.92, 0], [0.95, -0.92, 0], [0.95, -1.69, 0]])
        rroute = route([[3.45, 0.35, 0], [2.7, -0.35, 0], [0.95, -0.92, 0], [0.95, -1.69, 0]])
        self.play(Create(lroute), Create(rroute), run_time=1.8)
        self.at("Here unaffected parents")
        pulse(VGroup(carrier_l, carrier_r), base=7, amp=2, speed=2.0)
        self.play(Indicate(VGroup(world.p["s2"], world.p["d2"]), color=GOLD, scale_factor=1.08), run_time=0.9)
        self.finish()


class S06Xroute(SpokenScene):
    def construct(self):
        dim = pedigree(opacity=0.16)
        focus = x_focus()
        self.add(dim)
        self.play(FadeIn(focus), run_time=0.8)
        self.at("A father gives")
        xb = chromosome("X", GOLD, [-4.0, 2.35, 0])
        yb = chromosome("Y", GREY, [-3.15, 2.35, 0])
        self.play(FadeIn(xb), FadeIn(yb), run_time=0.6)
        self.at("to daughters")
        xpath = route([[-4.0, 1.75, 0], [-4.0, 0.25, 0], [-2.25, 0.25, 0], [-2.25, -0.99, 0]])
        self.play(Create(xpath), xb.animate.move_to([-3.15, -1.55, 0]), run_time=1.3)
        self.at("Y chromosome")
        ypath = route([[-3.15, 1.75, 0], [-3.15, 0.25, 0], [2.25, 0.25, 0], [2.25, -0.99, 0]], color=GREY)
        self.play(Create(ypath), yb.animate.move_to([3.15, -1.55, 0]), run_time=1.3)
        self.at("sex and parental origin")
        pulse(VGroup(xpath, ypath), base=7, amp=1.5, speed=2.0)
        self.play(Indicate(VGroup(focus.daughter, focus.son), color=GOLD, scale_factor=1.08), run_time=0.9)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        focus = x_focus()
        self.add(focus)
        self.play(Indicate(VGroup(focus.father, focus.son), color=RED, scale_factor=1.1), run_time=0.8)
        self.at("Could an X")
        qpath = route([[-2.25, 0.89, 0], [-2.25, 0.25, 0], [2.25, 0.25, 0], [2.25, -0.99, 0]], dashed=True)
        pulse(qpath, base=5.5, amp=1.8, speed=2.2)
        self.play(Create(qpath), run_time=1.6)
        self.at("Follow the chromosome route")
        q = question_card("Direct X-linked transmission?", y=-3.15, max_w=9.8)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.6)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Direct X-linked transmission?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "max_w": 9.8}

    def backdrop(self):
        return x_focus(show_question=True)


class S09Reveal(SpokenScene):
    def construct(self):
        focus = x_focus(show_question=True)
        q = question_card("Direct X-linked transmission?", y=-3.15, max_w=9.8)
        self.add(focus, q)
        no = T("No.", 58, VIOLET, weight=BOLD).move_to([5.4, 2.35, 0])
        self.play(FadeIn(no), FadeOut(focus.qpath), run_time=0.7)
        self.at("the son's X chromosome")
        xb = chromosome("X", GOLD, [2.25, 1.45, 0])
        maternal = route([[2.25, 0.89, 0], [2.25, -0.99, 0]])
        self.play(FadeIn(xb), Create(maternal), xb.animate.move_to([2.25, -1.55, 0]), run_time=1.6)
        self.at("therefore contradicts")
        frame = RoundedRectangle(corner_radius=0.2, width=9.4, height=4.45, stroke_color=GREY,
                                 stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([0, 0.0, 0])
        models = VGroup(T("X-linked dominant", 24, GREY), T("X-linked recessive", 24, GREY))
        models.arrange(RIGHT, buff=1.0).move_to([0, 2.65, 0])
        card = VGroup(frame, models).set_z_index(-1)
        bar = Line([-4.5, -0.2, 0], [4.5, 0.8, 0], color=VIOLET, stroke_width=14)
        label = caption("father-to-son transmission", color=VIOLET)
        self.play(FadeIn(card), Create(bar), FadeIn(label), FadeOut(q), run_time=1.1)
        self.at("An affected pair alone")
        pulse(maternal, base=7, amp=1.8, speed=2.0)
        caveat = T("only if mother carries no copy", 28, GREY).move_to([0, -3.0, 0])
        self.play(swap(label, caveat), run_time=0.8)
        self.finish()


class S10Mito(SpokenScene):
    def construct(self):
        world = pedigree()
        card = model_card("mitochondrial — simple model")
        card[0].set_z_index(-2)
        self.add(card, world)
        dots = VGroup(*[Dot(radius=0.09, color=GOLD).move_to(world.p["m0"].get_center() + [dx, dy, 0])
                        for dx, dy in [(-.16, .12), (.14, .13), (-.02, -.15)]])
        self.play(FadeIn(dots), run_time=0.6)
        self.at("Mothers can transmit")
        routes = [route([[1.45, 2.38, 0], [0, 2.38, 0], [0, 1.55, 0], [x, 1.55, 0], [x, 0.71, 0]])
                  for x in (-3.85, 0, 3.45)]
        self.play(LaggedStart(*[Create(r) for r in routes], lag_ratio=0.3), run_time=2.1)
        self.at("while fathers")
        father_dots = dots.copy().move_to(world.p["s3"])
        halo = Circle(radius=0.5, color=GOLD, stroke_width=4).move_to(world.p["s3"])
        self.play(FadeIn(father_dots), Rotate(father_dots, angle=TAU, about_point=world.p["s3"].get_center()),
                  Create(halo), run_time=1.2)
        self.at("This maternal route differs")
        pulse(VGroup(*routes), base=7, amp=1.6, speed=2.0)
        note = caption("not every mitochondrial disease", color=GREY)
        self.play(FadeIn(note), run_time=0.7)
        self.finish()


class S11Compare(SpokenScene):
    def construct(self):
        world = pedigree(shift=LEFT * 2.2)
        world.scale(0.78, about_point=LEFT * 2.2)
        self.add(world)
        cards = VGroup(*[chip(t, c, 26) for t, c in [("dominant", GOLD), ("recessive", GOLD),
                                                       ("X-linked", GOLD), ("mitochondrial", GOLD)]])
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.55, 0.55, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in cards], lag_ratio=0.2), run_time=1.1)
        self.at("One contradiction")
        marks = VGroup(check([3.05, 1.62, 0]), cross_mark([3.05, 0.55, 0], width=0.42),
                       check([3.05, -0.52, 0]), check([3.05, -1.58, 0]))
        self.play(LaggedStart(*[FadeIn(m, scale=0.7) for m in marks], lag_ratio=0.25), run_time=1.3)
        self.at("Compatibility adds support")
        glass = VGroup(Circle(radius=0.48, color=TEAL, stroke_width=5),
                       Line([0.34, -0.34, 0], [0.92, -0.92, 0], color=TEAL, stroke_width=6)).move_to([-3.8, 1.8, 0])
        self.play(FadeIn(glass), glass.animate.move_to([2.35, 1.7, 0]), run_time=2.0)
        self.at("The model earns confidence")
        self.play(glass.animate.move_to([2.35, -1.45, 0]), run_time=1.6)
        self.at("guiding rule")
        rule = caption("Fitting predictions support; contradictions can rule out.", color=GOLD)
        self.play(FadeIn(rule), run_time=0.7)
        self.finish()


class S12Scope(SpokenScene):
    def construct(self):
        world = pedigree(shift=LEFT * 2.25)
        world.scale(0.76, about_point=LEFT * 2.25)
        frame = RoundedRectangle(corner_radius=0.22, width=5.0, height=5.2, stroke_color=GOLD,
                                 stroke_width=3, fill_color=GOLD, fill_opacity=0.05).move_to([3.65, 0.15, 0])
        route_line = route([[-2.0, 2.0, 0], [-2.0, 0.2, 0], [-1.4, -1.3, 0]])
        pulse(route_line, base=7, amp=1.5, speed=2.0)
        self.add(world, route_line, frame)
        self.at("It assumes")
        labels = [T("full penetrance", 26, GREY), T("no new mutation", 26, GREY),
                  T("correct relationships", 26, GREY), T("simple model", 26, GREY)]
        positions = [[3.65, 1.65, 0], [3.65, 0.55, 0], [3.65, -0.55, 0], [3.65, -1.65, 0]]
        for lab, pos in zip(labels, positions):
            lab.move_to(pos)
        self.play(LaggedStart(*[FadeIn(l, scale=0.85) for l in labels], lag_ratio=0.25), run_time=2.2)
        self.at("Change an assumption")
        gap = Line([3.05, 2.75, 0], [4.25, 2.75, 0], color=BG, stroke_width=10)
        soft = cross_mark([5.55, 0.1, 0], width=0.8).set_opacity(0.35)
        self.play(Create(gap), FadeIn(soft), frame.animate.set_stroke(opacity=0.45), run_time=1.2)
        self.at("another explanation")
        self.play(soft.animate.set_opacity(0.12), run_time=0.8)
        self.finish()


class S13Support(SpokenScene):
    def construct(self):
        world = pedigree(shift=LEFT * 3.0)
        world.scale(0.67, about_point=LEFT * 3.0)
        self.add(world)
        c1 = model_card("model A", at=[3.6, 1.55, 0], width=5.0, height=2.1)
        c2 = model_card("model B", at=[3.6, -1.2, 0], width=5.0, height=2.1)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.8)
        self.at("Other models")
        r1 = route([[1.45, 1.55, 0], [3.6, 1.55, 0], [5.6, 1.55, 0]], width=6)
        r2 = route([[1.45, -1.2, 0], [3.6, -1.2, 0], [5.6, -1.2, 0]], width=6)
        self.play(Create(r1), Create(r2), run_time=1.5)
        self.at("same small family")
        marks = VGroup(check([5.55, 1.0, 0]), check([5.55, -1.75, 0]))
        word = T("supports", 40, TEAL, weight=BOLD).move_to([3.6, -2.9, 0])
        self.play(FadeIn(marks), FadeIn(word), run_time=0.8)
        self.at("Small families")
        pulse(VGroup(r1, r2), base=6, amp=1.4, speed=2.0)
        missing = VGroup(person("female", side=0.58, color=GREY), T("?", 30, GREY)).arrange(RIGHT, buff=0.2)
        missing.move_to([0.4, -3.0, 0])
        self.play(FadeIn(missing), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "Fitting predictions support a model; one contradiction can rule it out."
