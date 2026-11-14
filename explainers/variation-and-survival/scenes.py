"""How Populations Change — animated explainer.

COLOR MAP
  TEAL = inherited teal (tuskless) variant
  GOLD = inherited gold (tusked) variant
  BLUE = a newly made or arriving allele
  GREEN = successful passage / offspring
  RED = environmental limits or a blocked route
  GREY = neutral structure and scope labels

All animals and allele pools are explicitly schematic.  Counts illustrate shares; they are
not measurements.  The same builders are used whenever a picture carries into a later scene.
"""
from bp_parts import *


# --------------------------------------------------------------------------- carried world
HERD_POS = [(-4.8, 1.7), (-2.9, 1.8), (-1.0, 1.65), (1.0, 1.75), (2.9, 1.62), (4.8, 1.78),
            (-4.7, -0.65), (-2.8, -0.55), (-0.95, -0.72), (1.0, -0.58), (2.9, -0.7), (4.75, -0.55)]


def diagram_stage():
    """The film's consistent non-semantic drawing surface."""
    stage = RoundedRectangle(width=13.25, height=6.65, corner_radius=0.24,
                             stroke_width=0, fill_color="#2A303C", fill_opacity=1.0)
    stage.set_z_index(-100)
    stage.layout_ok = True  # deliberate background surface; it sits behind every label and shape
    return stage


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(diagram_stage())


def elephant(colour, tusked=False, scale=1.0):
    """A simple elephant silhouette; tusks are short pale arcs, never molecular geometry."""
    body = Ellipse(width=1.34, height=0.86, stroke_color=colour, stroke_width=4,
                   fill_color=colour, fill_opacity=0.42)
    head = Circle(radius=0.35, stroke_color=colour, stroke_width=4,
                  fill_color=colour, fill_opacity=0.42).move_to([0.72, -0.02, 0])
    ear = Circle(radius=0.17, color=colour, fill_opacity=0.18).move_to([0.57, 0.02, 0])
    trunk = ArcBetweenPoints([0.94, -0.16, 0], [0.86, -0.64, 0], angle=-0.45,
                             color=colour, stroke_width=7)
    legs = VGroup(*[Line([x, -0.30, 0], [x, -0.62, 0], color=colour, stroke_width=8)
                    for x in (-0.42, 0.22)])
    eye = Dot([0.82, 0.04, 0], radius=0.035, color=TEXT)
    parts = [body, legs, head, ear, trunk, eye]
    if tusked:
        parts.append(ArcBetweenPoints([0.94, -0.13, 0], [1.19, -0.30, 0], angle=0.35,
                                      color=TEXT, stroke_width=4))
    return VGroup(*parts).scale(scale)


def herd(teal_n=5, y_shift=0.0, scale=0.92, moving=True):
    """The canonical herd: fixed landmarks ensure every carried view matches."""
    animals = VGroup()
    for i, (x, y) in enumerate(HERD_POS):
        is_teal = i < teal_n
        a = elephant(TEAL if is_teal else GOLD, tusked=not is_teal, scale=scale)
        a.move_to([x, y + y_shift, 0])
        if moving:
            bob(a, amp=0.055, speed=1.25 + 0.06 * i, seed=i)
        animals.add(a)
    return animals


def herd_legend(y=-2.35):
    t = VGroup(elephant(TEAL, False, 0.55), T("teal inherited variant", 28, TEAL)).arrange(RIGHT, buff=0.18)
    g = VGroup(elephant(GOLD, True, 0.55), T("gold inherited variant", 28, GOLD)).arrange(RIGHT, buff=0.18)
    return VGroup(t, g).arrange(RIGHT, buff=0.75).move_to([0, y, 0])


def pool(beads=(TEAL, GOLD, TEAL, GOLD, GOLD, TEAL, GOLD, GOLD), moving=True):
    ring = Circle(radius=2.35, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=0.25)
    dots = VGroup()
    pts = [(-1.15, 0.9), (0, 1.35), (1.15, 0.85), (-1.35, -0.2), (0, 0.2),
           (1.35, -0.2), (-0.75, -1.15), (0.75, -1.1)]
    for i, (p, c) in enumerate(zip(pts, beads)):
        d = Dot([p[0], p[1], 0], radius=0.24, color=c)
        if moving:
            bob(d, amp=0.07, speed=1.2 + i * 0.08, seed=i)
        dots.add(d)
    lab = T("gene pool", 36, TEXT, weight=BOLD).move_to([0, 2.75, 0])
    return VGroup(ring, dots, lab), dots


def filter_frame(question=False, equal=True):
    """Canonical survival-and-reproduction filter used by predict, pause, and reveals."""
    left = RoundedRectangle(width=3.25, height=3.7, corner_radius=0.18,
                            stroke_color=GREY, stroke_width=3).move_to([-4.4, 0.35, 0])
    gate = Polygon([-2.6, 1.8, 0], [0.2, 0.85, 0], [0.2, -0.15, 0], [-2.6, -1.1, 0],
                   stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08)
    out = RoundedRectangle(width=4.2, height=3.7, corner_radius=0.18,
                           stroke_color=GREEN, stroke_width=3).move_to([3.55, 0.35, 0])
    labels = VGroup(T("parents", 30, TEXT).move_to([-4.4, 2.65, 0]),
                    T("survival + reproduction", 28, GREY).move_to([-1.05, 2.65, 0]),
                    T("next generation", 30, GREEN).move_to([3.55, 2.65, 0]))
    streams = VGroup()
    cols = [TEAL, GOLD] * 4 if equal else [TEAL, TEAL, GOLD, TEAL, TEAL, GOLD, TEAL, TEAL]
    for i, c in enumerate(cols):
        d = Dot([-5.3 + (i % 4) * 0.58, 1.05 - (i // 4) * 1.35, 0], radius=0.18, color=c)
        bob(d, amp=0.05, speed=1.2 + i * 0.1, seed=i)
        streams.add(d)
    world = VGroup(left, gate, out, labels, streams)
    if question:
        q = question_card("Will one color take over, or will the shares wobble?", y=-3.12, size=29)
        return world, streams, q
    return world, streams


def generation_row(teal_n, y, label):
    dots = VGroup(*[Dot(radius=0.21, color=TEAL if i < teal_n else GOLD) for i in range(10)])
    dots.arrange(RIGHT, buff=0.24).move_to([0.55, y, 0])
    txt = T(label, 28, GREY).next_to(dots, LEFT, buff=0.38)
    return VGroup(txt, dots), dots


# --------------------------------------------------------------------------- scenes
class S00Hook(FilmScene):
    def construct(self):
        q = fit_text("How can a population change when no individual changes?", max_w=12.0,
                     size=38, color=TEXT).move_to([0, 3.2, 0])
        h = herd(teal_n=5, y_shift=-0.2, scale=0.9)
        leg = herd_legend(-2.45)
        tag = scope_tag("schematic")
        self.at("How can a population change")
        self.play(FadeIn(h, scale=0.92), run_time=1.5)
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.7)
        self.at("Watch this schematic")
        self.play(FadeIn(leg), FadeIn(tag), run_time=0.8)
        outlines = herd(teal_n=7, y_shift=-0.2, scale=0.9, moving=False).set_opacity(0.16)
        outlines.shift(RIGHT * 0.45)
        self.at("Each animal keeps")
        self.play(FadeIn(outlines), run_time=0.7)
        self.at("colored shares can change")
        self.play(h.animate.shift(RIGHT * 0.45), run_time=2.0, rate_func=linear)
        self.play(FadeOut(outlines), run_time=0.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Variation and survival"
    TITLE = "How Populations Change"

    def construct(self):
        teal = Dot([-4.9, 0, 0], radius=0.32, color=TEAL)
        gold = Dot([4.9, 0, 0], radius=0.32, color=GOLD)
        brand = T("VARIATION AND SURVIVAL", 22, GREY)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, title, rule).arrange(DOWN, buff=0.35)
        self.add(teal, gold)
        self.play(teal.animate.shift(RIGHT * 2.0), gold.animate.shift(LEFT * 2.0),
                  FadeIn(brand), Write(title), GrowFromCenter(rule), run_time=1.35)
        self.play(teal.animate.shift(RIGHT * 0.5), gold.animate.shift(LEFT * 0.5),
                  FadeOut(g), run_time=0.55)
        self.finish()


class S02Variation(FilmScene):
    def construct(self):
        h = herd(teal_n=5, y_shift=-0.15)
        head = T("one population — different individuals", 36, TEXT).move_to([0, 3.25, 0])
        self.at("Individuals in one population")
        self.play(LaggedStart(*[FadeIn(a, scale=0.8) for a in h], lag_ratio=0.05), run_time=1.5)
        self.play(FadeIn(head), run_time=0.5)
        glow = SurroundingRectangle(h[8], color=GREY, buff=0.16, corner_radius=0.15)
        food = T("food or experience", 28, GREY).next_to(glow, DOWN, buff=0.16)
        self.at("Some differences come")
        self.play(Create(glow), FadeIn(food), run_time=0.7)
        self.play(FadeOut(glow), FadeOut(food), h[8].animate.set_opacity(0.18), run_time=1.1)
        inherited = VGroup(T("inherited", 32, TEAL), T("inherited", 32, GOLD)).arrange(RIGHT, buff=2.4).move_to([0, -2.5, 0])
        self.at("Others are inherited")
        self.play(FadeIn(inherited), Indicate(h[1], color=TEAL), Indicate(h[7], color=GOLD), run_time=1.0)
        young = VGroup(elephant(TEAL, False, 0.52), elephant(GOLD, True, 0.52)).arrange(RIGHT, buff=3.0).move_to([0, -1.6, 0])
        self.at("pass from parents")
        self.play(TransformFromCopy(VGroup(h[1], h[7]), young), run_time=1.4)
        self.at("shape later generations")
        self.play(young.animate.shift(UP * 0.16), run_time=1.2, rate_func=there_and_back)
        self.finish()


class S03GenePool(FilmScene):
    def construct(self):
        p, dots = pool()
        tag = scope_tag("schematic")
        self.at("Zoom into the population's gene pool")
        self.play(FadeIn(p, scale=0.55), FadeIn(tag), run_time=1.5)
        meaning = T("all its alleles — versions of genes", 30, GREY).move_to([0, -2.9, 0])
        self.at("all its alleles")
        self.play(FadeIn(meaning), run_time=0.7)
        for bead in dots:
            bead.clear_updaters()
        dots.add_updater(lambda mob, dt: mob.rotate(0.18 * dt, about_point=ORIGIN))
        self.play(Rotate(dots, angle=0.35), run_time=2.4, rate_func=linear)
        new = Dot([0.05, 0.2, 0], radius=0.25, color=BLUE)
        mut = T("mutation", 30, BLUE).move_to([-4.3, 1.0, 0])
        arrow1 = Arrow(mut.get_right(), new.get_left(), color=BLUE, buff=0.2)
        self.at("A mutation can make")
        self.play(FadeIn(mut), GrowArrow(arrow1), FadeIn(new, scale=0.1), run_time=1.1)
        neighbour = Circle(radius=0.9, color=GREY).move_to([4.5, -0.3, 0])
        incoming = Dot(neighbour.get_center(), radius=0.24, color=BLUE)
        flow = T("gene flow", 30, BLUE).move_to([4.5, 1.25, 0])
        self.at("Gene flow can bring")
        self.play(Create(neighbour), FadeIn(incoming), FadeIn(flow), run_time=0.7)
        self.play(incoming.animate.move_to([1.15, -0.2, 0]), run_time=1.4)
        self.at("Both can change")
        self.play(Indicate(VGroup(new, incoming), color=BLUE), run_time=1.0)
        self.finish()


class S04Shuffle(FilmScene):
    def construct(self):
        p, dots = pool()
        p[2].set_opacity(0.0)
        head = T("existing alleles", 36, TEXT).move_to([0, 3.15, 0])
        self.at("Sexual reproduction")
        self.play(FadeIn(p), FadeIn(head), run_time=1.0)
        pairs = VGroup()
        targets = [(-3.6, 0.8), (0, 0.8), (3.6, 0.8), (-3.6, -1.1), (0, -1.1), (3.6, -1.1)]
        copies = VGroup(*[d.copy().clear_updaters() for d in dots])
        self.add(copies)
        self.play(FadeOut(p), run_time=0.5)
        self.at("Myosis and fertilization")
        for i, (x, y) in enumerate(targets):
            a = copies[(2 * i) % len(copies)]
            b = copies[(2 * i + 3) % len(copies)].copy()
            self.add(b)
            box = RoundedRectangle(width=1.35, height=0.8, corner_radius=0.14, color=GREY).move_to([x, y, 0])
            pairs.add(box)
            self.play(a.animate.move_to([x - 0.25, y, 0]), b.animate.move_to([x + 0.25, y, 0]), Create(box), run_time=0.38)
        combos = T("new combinations", 34, GREEN).move_to([0, -2.45, 0])
        self.at("new combinations")
        self.play(FadeIn(combos), run_time=0.7)
        n = ValueTracker(0)
        reads = VGroup(counter("new alleles  {:.0f}", n, [-3.4, 2.55, 0], 30, BLUE),
                       T("new combinations  6", 30, GREEN).move_to([3.3, 2.55, 0]))
        self.at("without a new allele")
        self.play(FadeOut(head), FadeIn(reads), run_time=0.8)
        self.play(pairs.animate.shift(UP * 0.08), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S05Predict(FilmScene):
    def construct(self):
        world, streams, q = filter_frame(question=True, equal=True)
        self.at("Now suppose teal and gold")
        self.play(FadeIn(world), run_time=1.2)
        for marker in streams:
            marker.clear_updaters()
        self.play(streams.animate.shift(RIGHT * 0.3), run_time=1.8, rate_func=linear)
        equal = T("equal offspring left", 32, TEXT).move_to([-4.4, -2.05, 0])
        self.at("offspring equally often")
        self.play(FadeIn(equal), streams.animate.shift(RIGHT * 0.3), run_time=1.5, rate_func=linear)
        self.at("Predict the next generation")
        self.play(FadeIn(q.question), run_time=0.8)
        self.at("Will one color steadily")
        self.play(streams.animate.shift(RIGHT * 0.4), run_time=2.2, rate_func=linear)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Will one color take over, or will the shares wobble?"
    SECONDS = 4.5

    def backdrop(self):
        world, streams = filter_frame(question=False, equal=True)
        streams.shift(RIGHT * 1.0)
        return VGroup(diagram_stage(), world)


class S07EqualReveal(FilmScene):
    def construct(self):
        r1, d1 = generation_row(5, 1.75, "generation 1")
        r2, d2 = generation_row(6, 0.55, "generation 2")
        r3, d3 = generation_row(4, -0.65, "generation 3")
        r4, d4 = generation_row(5, -1.85, "generation 4")
        head = T("equal reproductive success", 38, TEXT).move_to([0, 3.2, 0])
        self.at("With equal reproductive success")
        self.play(FadeIn(head), FadeIn(r1), run_time=1.0)
        self.at("neither color")
        self.play(FadeIn(r2), run_time=0.8)
        self.at("Chance can still")
        self.play(FadeIn(r3), FadeIn(r4), run_time=1.5)
        arrow = DoubleArrow([-4.6, -2.75, 0], [4.6, -2.75, 0], color=GREY, stroke_width=5)
        lab = T("no consistent direction", 34, TEXT).move_to([0, -3.25, 0])
        self.at("no directional push")
        self.play(GrowFromCenter(arrow), FadeIn(lab), run_time=1.2)
        self.play(d4.animate.shift(RIGHT * 0.12), run_time=1.2, rate_func=there_and_back)
        self.finish()


class S08Surplus(FilmScene):
    def construct(self):
        head = T("more young than the environment supports", 36, TEXT).move_to([0, 3.2, 0])
        parents = VGroup(elephant(TEAL, False, 0.85), elephant(GOLD, True, 0.85)).arrange(RIGHT, buff=1.1).move_to([-4.4, 0.4, 0])
        young = VGroup(*[Dot(radius=0.15, color=TEAL if i % 3 else GOLD) for i in range(24)])
        young.arrange_in_grid(4, 6, buff=0.22).move_to([-0.5, 0.35, 0])
        self.at("Real populations usually produce")
        self.play(FadeIn(parents), FadeIn(head), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in young], lag_ratio=0.025), run_time=1.8)
        gate = Polygon([1.8, 2.0, 0], [3.2, 0.8, 0], [3.2, -0.1, 0], [1.8, -1.35, 0],
                       color=RED, fill_color=RED, fill_opacity=0.08, stroke_width=4)
        limits = VGroup(*[chip(x, RED, 26) for x in ("food", "space", "predators", "disease")]).arrange(DOWN, buff=0.16).move_to([5.0, 0.45, 0])
        self.at("Food, space, predators")
        self.play(Create(gate), LaggedStart(*[FadeIn(x) for x in limits], lag_ratio=0.1), run_time=1.2)
        passers = VGroup(*[young[i] for i in (2, 5, 8, 11, 14, 17)])
        others = VGroup(*[d for d in young if d not in passers])
        self.at("many never reproduce")
        self.play(FadeOut(others, scale=0.5), passers.animate.move_to([3.7, -1.6, 0]), run_time=1.4)
        nests = VGroup(*[Circle(radius=0.28, color=GREEN) for _ in range(3)]).arrange(RIGHT, buff=0.55).move_to([4.5, -2.25, 0])
        self.at("surviving adults")
        self.play(FadeOut(limits), FadeIn(nests), run_time=0.7)
        self.at("Reproduction matters")
        self.play(passers.animate.move_to(nests.get_center() + UP * 0.55), run_time=1.1)
        self.finish()


class S09UnequalFilter(FilmScene):
    def construct(self):
        world, streams = filter_frame(equal=False)
        banner = chip("changed conditions", RED, 34).move_to([0, 3.3, 0])
        self.at("Now change the conditions")
        self.play(FadeIn(world), FadeIn(banner), run_time=1.1)
        fitlab = T("teal fits these conditions better", 30, TEAL).move_to([-3.75, -2.05, 0])
        self.at("teal individuals leave more offspring")
        for marker in streams:
            marker.clear_updaters()
        self.play(FadeIn(fitlab), Indicate(VGroup(*[d for d in streams if d.get_color() == ManimColor(TEAL)]), color=TEAL), run_time=1.3)
        self.play(streams.animate.shift(RIGHT * 0.8), run_time=5.2, rate_func=linear)
        self.at("More teal markers pass")
        self.play(streams.animate.shift(RIGHT * 5.1), run_time=2.4, rate_func=linear)
        nextrow, dots = generation_row(7, -1.65, "new mix")
        dots.arrange_in_grid(2, 5, buff=0.24).move_to([3.55, 0.75, 0])  # inside the next-generation box
        nextrow[0].next_to(dots, DOWN, buff=0.35)
        self.at("The next generation starts")
        self.play(FadeOut(streams), FadeIn(nextrow), run_time=1.2)
        self.play(dots.animate.shift(UP * 0.08), run_time=1.2, rate_func=there_and_back)
        self.finish()


class S10Rule(FilmScene):
    def construct(self):
        tp = TwoPanel("inherited variation", "unequal offspring left", colors=(TEAL, GREEN), width=8.4)
        tp.shift(LEFT * 2.0)
        leftpic = VGroup(elephant(TEAL, False, 0.75), elephant(GOLD, True, 0.75)).arrange(DOWN, buff=0.55)
        rightpic = VGroup(*[Dot(radius=0.22, color=c) for c in (TEAL, TEAL, TEAL, GOLD, TEAL, GOLD)]).arrange_in_grid(2, 3, buff=0.35)
        tp.put(leftpic, "left"); tp.put(rightpic, "right")
        rdots = VGroup(*[Dot(radius=0.19, color=TEAL if i < 7 else GOLD) for i in range(10)])
        rdots.arrange_in_grid(2, 5, buff=0.24)
        result = VGroup(T("changed generation", 28, GREY), rdots).arrange(DOWN, buff=0.38).move_to([4.75, 0.2, 0])
        arr = Arrow([2.3, -0.85, 0], [3.35, -0.85, 0], color=GOLD, stroke_width=6)
        self.at("When inherited variations")
        self.play(FadeIn(tp), FadeIn(leftpic), run_time=1.0)
        self.at("affect reproductive success")
        self.play(FadeIn(rightpic), run_time=0.8)
        self.at("populations change")
        self.play(GrowArrow(arr), FadeIn(result), run_time=1.2)
        self.play(rdots.animate.shift(UP * 0.12), run_time=1.4, rate_func=there_and_back)
        rule = caption("Natural selection", size=42, color=GOLD)
        self.at("That process is natural selection")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.play(rdots.animate.shift(RIGHT * 0.14), run_time=1.7, rate_func=there_and_back)
        self.at("It needs inherited variation")
        self.play(Indicate(leftpic, color=TEAL), run_time=0.8)
        self.at("unequal reproductive success")
        self.play(Indicate(rightpic, color=GREEN), run_time=0.8)
        self.play(rdots.animate.shift(UP * 0.08), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S11NoTransform(FilmScene):
    def construct(self):
        gold = elephant(GOLD, True, 1.7).move_to([-3.5, 0.65, 0])
        teal = elephant(TEAL, False, 1.7).move_to([3.5, 0.65, 0])
        gl = T("gold through life", 32, GOLD).move_to([-3.5, -1.05, 0])
        tl = T("teal through life", 32, TEAL).move_to([3.5, -1.05, 0])
        self.at("Follow one gold individual")
        self.play(FadeIn(gold), FadeIn(gl), run_time=0.9)
        pathg = Line([-5.2, 1.8, 0], [-1.9, 1.8, 0], color=GOLD, stroke_width=4)
        self.at("never turns teal")
        self.play(gold.animate.shift(UP * 1.15), Create(pathg), run_time=1.2)
        self.at("Follow one teal individual")
        self.play(FadeIn(teal), FadeIn(tl), run_time=0.9)
        patht = Line([1.9, 1.8, 0], [5.2, 1.8, 0], color=TEAL, stroke_width=4)
        self.at("never turns gold")
        self.play(teal.animate.shift(UP * 1.15), Create(patht), run_time=1.2)
        before, _ = generation_row(4, -2.0, "old")
        after, _ = generation_row(7, -2.85, "new")
        self.at("compare the population")
        self.play(FadeOut(VGroup(pathg, patht, gl, tl)), FadeIn(before), FadeIn(after), run_time=1.3)
        self.finish()


class S12MissingVariation(FilmScene):
    def construct(self):
        all_gold = herd(teal_n=0, y_shift=-0.3, scale=0.83)
        head = T("selection uses variation already present", 36, TEXT).move_to([0, 3.2, 0])
        self.at("Selection can work only")
        self.play(FadeIn(all_gold), FadeIn(head), run_time=1.3)
        opening = RoundedRectangle(width=2.0, height=1.15, corner_radius=0.18, color=TEAL,
                                   fill_color=TEAL, fill_opacity=0.08).move_to([0, -2.25, 0])
        absent = T("teal variant absent", 32, TEAL).move_to([0, -3.15, 0])
        self.at("every marker begins gold")
        self.play(Create(opening), run_time=0.8)
        mut = chip("mutation closed", RED, 27).move_to([-4.55, -2.65, 0])
        flow = chip("gene flow closed", RED, 27).move_to([4.55, -2.65, 0])
        self.at("no new teal allele")
        self.play(FadeIn(mut), FadeIn(flow), FadeIn(absent), run_time=1.0)
        self.at("teal advantage cannot change")
        self.play(Indicate(opening, color=TEAL), run_time=1.1)
        self.at("variant that is absent")
        self.play(all_gold.animate.shift(RIGHT * 0.12), run_time=1.3, rate_func=there_and_back)
        self.finish()


class S13Conditions(FilmScene):
    def construct(self):
        panels = TwoPanel("environment A", "environment B", colors=(GREEN, RED))
        a1 = VGroup(elephant(TEAL, False, 0.9), elephant(GOLD, True, 0.9)).arrange(DOWN, buff=0.65)
        a2 = a1.copy()
        panels.put(a1, "left"); panels.put(a2, "right")
        gate1 = Rectangle(width=2.5, height=0.7, color=TEAL).move_to([-3.2, -1.55, 0])
        gate2 = Rectangle(width=1.2, height=0.7, color=TEAL).move_to([3.2, -1.55, 0])
        self.at("Whether a variation helps")
        self.play(FadeIn(panels), FadeIn(a1), FadeIn(a2), run_time=1.1)
        self.play(a1.animate.shift(UP * 0.12), a2.animate.shift(DOWN * 0.12),
                  run_time=2.3, rate_func=there_and_back)
        self.at("depends on the environment")
        self.play(Create(gate1), Create(gate2), run_time=1.0)
        self.play(a1.animate.shift(RIGHT * 0.14), a2.animate.shift(LEFT * 0.14),
                  run_time=1.2, rate_func=there_and_back)
        planning = Arrow([-2.4, -2.65, 0], [2.4, -2.65, 0], color=GOLD, stroke_width=6)
        no = T("no planning", 36, RED).move_to([0, -3.2, 0])
        self.at("Selection does not plan ahead")
        self.play(GrowArrow(planning), run_time=0.7)
        self.play(FadeOut(planning), FadeIn(no), run_time=0.7)
        self.at("do not change inherited traits")
        self.play(a1.animate.shift(UP * 0.09), a2.animate.shift(DOWN * 0.09), run_time=1.5, rate_func=there_and_back)
        self.finish()


class S14Return(FilmScene):
    def construct(self):
        panels = TwoPanel("starting generation", "next generation", colors=(GREY, GREEN))
        old = herd(teal_n=4, moving=False, scale=0.48)
        new = herd(teal_n=8, moving=False, scale=0.48)
        panels.put(old, "left"); panels.put(new, "right")
        self.at("Return to the whole field")
        self.play(FadeIn(panels), FadeIn(old), run_time=1.0)
        paths = VGroup(*[CurvedArrow(old[i].get_right(), new[(i + 2) % 12].get_left(), angle=-0.18,
                                           color=old[i][0].get_color(), stroke_width=2.5)
                         for i in (0, 2, 5, 7, 9)])
        self.at("Different individuals entered")
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.12), run_time=1.3)
        self.at("next generation has a different mix")
        self.play(FadeIn(new), run_time=1.2)
        rule = caption("Population shares changed; individual colors did not.", size=32, color=GOLD)
        self.at("The population changed")
        self.play(FadeOut(paths), FadeIn(rule), run_time=0.8)
        self.at("not because individuals transformed")
        self.play(Indicate(VGroup(old, new), color=TEXT), run_time=1.3)
        self.finish()


class S15End(EndCard):
    LINE = "When inherited variations affect reproductive success,\npopulations change across generations."
