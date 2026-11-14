"""How do we know it worked? — chapter 2 of Genetic engineering.

COLOR MAP (kept for the whole chapter pair)
  BLUE   = plasmid / engineered change
  GREEN  = intended insulin gene, product, or intended effect
  YELLOW = test tools
  RED    = selection, risk, or unresolved unintended effect
  TEAL   = evidence and supported claims
  PURPLE = values
  GREY   = cells, controls, structure, and neutral labels

All biological drawings are schematic cartoons.  The adoption plot is computed from the
lesson data in script.json; gel positions are computed from the assigned schematic sizes.
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
BENCH_Y = -2.15


def arrow(a, b, color=GREY, width=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=0.22)


def plasmid(center=ORIGIN, radius=1.12, width=14):
    """The carried chapter-1 object: a blue plasmid with one green insert."""
    blue = Arc(radius=radius, start_angle=np.radians(48), angle=np.radians(306),
               arc_center=center, stroke_color=BLUE, stroke_width=width)
    gene = Arc(radius=radius, start_angle=np.radians(-6), angle=np.radians(54),
               arc_center=center, stroke_color=GREEN, stroke_width=width)
    return VGroup(blue, gene)


def bench():
    top = Line([-6.25, BENCH_Y, 0], [6.25, BENCH_Y, 0], color=TEAL, stroke_width=9)
    legs = VGroup(Line([-5.5, BENCH_Y, 0], [-5.5, -3.15, 0], color=TEAL, stroke_width=7),
                  Line([5.5, BENCH_Y, 0], [5.5, -3.15, 0], color=TEAL, stroke_width=7))
    return VGroup(top, legs).set_opacity(0.8)


def colony(center=(-3.9, -0.25, 0), scale=1.0):
    """One large schematic colony made from gently overlapping neutral cells."""
    offsets = [(-0.7, 0.25), (0.0, 0.55), (0.75, 0.2), (-0.45, -0.45),
               (0.35, -0.35), (0.95, -0.5), (-0.05, 0.0)]
    dots = VGroup(*[Circle(radius=0.54, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.18).move_to([center[0] + scale*x, center[1] + scale*y, 0])
                    for x, y in offsets])
    return dots.scale(scale)


CLAIMS = ("plasmid taken up", "insulin DNA present", "insulin protein made")


def claim_stack(status=("?", "?", "?"), x=3.55, top=2.25, width=5.35):
    """Three claim frames at the same coordinates in every bench scene."""
    groups = VGroup()
    for i, (label, mark) in enumerate(zip(CLAIMS, status)):
        y = top - i * 1.48
        frame = RoundedRectangle(corner_radius=0.16, width=width, height=1.12,
                                 stroke_color=GREY, stroke_width=3, fill_color=TEAL,
                                 fill_opacity=0.20).move_to([x, y, 0])
        lab = T(label, 28, TEXT).move_to([x - 0.45, y, 0])
        col = TEAL if mark == "✓" else RED
        symbol = T(mark, 38, col, weight=BOLD).move_to([x + width/2 - 0.42, y, 0])
        groups.add(VGroup(frame, lab, symbol))
    return groups


def antibiotic_world(with_question=False):
    """Carried picture shared by the predict scene and its deliberate pause."""
    plate = Circle(radius=2.28, stroke_color=RED, stroke_width=8,
                   fill_color=RED, fill_opacity=0.20).move_to([-1.25, -0.25, 0])
    cells = colony((-1.25, -0.3, 0), 0.72)
    p = plasmid((-1.25, -0.28, 0), 0.62, 10)
    product = DashedVMobject(RoundedRectangle(corner_radius=0.18, width=2.35, height=1.0,
                                              stroke_color=GREEN, stroke_width=5), num_dashes=20)
    product.move_to([3.5, -0.15, 0])
    prod_lab = T("insulin product?", 30, GREEN).next_to(product, DOWN, buff=0.25)
    plate_lab = T("antibiotic plate", 30, RED).move_to([-1.25, -2.95, 0])
    g = VGroup(plate, cells, p, product, prod_lab, plate_lab)
    if with_question:
        q = question_card("Does growth alone prove insulin is made?", y=3.2, size=34, max_w=11.2)
        g.add(q)
    return g


def use_card(title, color, x):
    frame = RoundedRectangle(corner_radius=0.2, width=3.65, height=4.3, stroke_color=color,
                             stroke_width=4, fill_color=color, fill_opacity=0.20).move_to([x, 0.35, 0])
    head = T(title, 30, color, weight=BOLD).move_to([x, 1.92, 0])
    change = plasmid([x, 0.55, 0], 0.72, 10)
    effect = T("effect", 28, GREEN).move_to([x, -0.72, 0])
    risk = T("?", 42, RED, weight=BOLD).move_to([x + 1.25, -1.35, 0])
    return VGroup(frame, head, change, effect, risk)


class S01Hook(SpokenScene):
    def construct(self):
        p = plasmid([-3.55, 0.45, 0], 1.65, 18)
        p_lab = T("plasmid", 32, BLUE).move_to([-3.55, 2.6, 0])
        gene_lab = T("insulin gene", 30, GREEN).move_to([-3.55, -1.8, 0])
        self.play(Create(p), run_time=1.15)
        p.add_updater(lambda mob, dt: mob.rotate(0.055 * dt))
        self.at("green insulin gene")
        self.play(FadeIn(p_lab), FadeIn(gene_lab), p.animate.rotate(0.35), run_time=0.8)
        self.at("how do we know")
        q = T("Did the change work?", 45, GOLD, font=TITLE_FONT).move_to([2.45, 2.4, 0])
        self.play(FadeIn(q, shift=UP * 0.12), p.animate.rotate(0.35), run_time=0.8)
        self.at("surviving bacterial colony")
        c = colony([2.25, -0.25, 0], 0.72)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in c], lag_ratio=0.08), run_time=1.0)
        self.at("evidence for which claim")
        empty = VGroup(*[RoundedRectangle(corner_radius=0.12, width=1.2, height=0.9,
                                          stroke_color=TEAL, stroke_width=3).move_to([4.8, y, 0])
                         for y in (0.8, -0.3, -1.4)])
        marks = VGroup(*[T("?", 30, TEAL).move_to(r) for r in empty])
        self.play(FadeIn(empty), FadeIn(marks), q.animate.set_color(TEAL), run_time=0.9)
        self.at("onto a testing bench")
        b = bench()
        self.play(FadeOut(VGroup(q, empty, marks, p_lab, gene_lab)), FadeIn(b),
                  p.animate.scale(0.6).move_to([-4.5, -1.15, 0]).rotate(0.5),
                  c.animate.scale(0.72).move_to([-1.75, -1.2, 0]), run_time=1.25)
        self.add(scope_tag("schematic"))
        self.finish()


class S00Title(TitleCard):
    LESSON = "Genetic engineering"
    TITLE = "How Do We Know It Worked?"


class S02Claims(SpokenScene):
    def construct(self):
        c = colony([-3.85, 0.0, 0], 1.05)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in c], lag_ratio=0.08), run_time=1.0)
        bob(c, amp=0.045, speed=1.3)
        self.at("several different claims")
        claims = claim_stack()
        self.play(FadeIn(claims[0], shift=LEFT * 0.2), run_time=0.75)
        self.at("contain the intended")
        self.play(FadeIn(claims[1], shift=LEFT * 0.2), c.animate.scale(1.03), run_time=0.75)
        self.at("make insulin protein")
        self.play(FadeIn(claims[2], shift=LEFT * 0.2), c.animate.scale(1.03), run_time=0.75)
        self.at("Each claim needs")
        tests = VGroup(*[T("test", 24, YELLOW).next_to(g, LEFT, buff=0.2) for g in claims])
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in tests], lag_ratio=0.18), run_time=1.0)
        self.at("checkmark belongs")
        rings = VGroup(*[Circle(radius=0.38, color=TEAL, stroke_width=5).move_to(g[2]) for g in claims])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.18), run_time=1.0)
        self.at("not to the whole organism")
        self.play(c.animate.set_opacity(0.35), claims.animate.set_opacity(1), run_time=0.9)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        world = antibiotic_world(False)
        plate, cells, p, product, prod_lab, plate_lab = world
        self.play(FadeIn(p), FadeIn(product), run_time=0.7)
        self.at("green product separate")
        self.play(p.animate.shift(LEFT * 0.15), product.animate.shift(RIGHT * 0.15),
                  FadeIn(prod_lab), run_time=0.75)
        bob(p, amp=0.035, speed=1.5)
        self.at("Predict before opening")
        q = question_card("Does growth alone prove insulin is made?", y=3.2, size=34, max_w=11.2)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.7)
        self.at("colony grows on antibiotic")
        self.play(FadeIn(plate), FadeIn(plate_lab),
                  LaggedStart(*[GrowFromCenter(d) for d in cells], lag_ratio=0.06), run_time=1.2)
        self.at("plasmid carries resistance")
        pulse(plate)
        self.play(Indicate(p, color=BLUE, scale_factor=1.25), run_time=0.8)
        self.at("growth alone prove")
        self.play(Indicate(product, color=GREEN, scale_factor=1.12),
                  cells.animate.scale(1.06), run_time=1.0)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Does growth alone prove insulin is made?"
    CARD = {"y": 3.2, "size": 34, "max_w": 11.2}
    SECONDS = 4.5

    def backdrop(self):
        g = antibiotic_world(False)
        pulse(g[0], base=8, amp=2, speed=2.2)
        bob(g[1], amp=0.035, speed=1.4)
        return g


class S05Selection(SpokenScene):
    def construct(self):
        world = antibiotic_world(True)
        self.add(world)
        no = T("NO", 50, RED, weight=BOLD).move_to([0, 2.2, 0])
        self.play(FadeIn(no, scale=1.25), run_time=0.65)
        self.at("antibiotic growth supports")
        claims = claim_stack(("✓", "?", "?"))
        self.play(FadeOut(world), FadeOut(no), FadeIn(bench()), FadeIn(claims), run_time=1.1)
        pulse(claims[0][0], base=3, amp=0.7, speed=1.4)
        self.at("resistance travels")
        p = plasmid([-4.55, -0.65, 0], 0.9, 12)
        resistance = chip("resistance", RED, 28).move_to([-4.55, 0.85, 0])
        self.play(Create(p), FadeIn(resistance), run_time=0.8)
        self.at("insert might still")
        uncertainties = VGroup(*[chip(s, RED, 25) for s in ("missing", "reversed", "unread")])
        uncertainties.arrange(DOWN, buff=0.18).move_to([-1.7, 0.45, 0])
        self.play(LaggedStart(*[FadeIn(u, shift=RIGHT * 0.12) for u in uncertainties], lag_ratio=0.16), run_time=1.1)
        self.at("Selection narrows")
        self.play(FadeOut(uncertainties), p.animate.scale(0.72).move_to([-5.0, -1.15, 0]),
                  resistance.animate.scale(0.82).move_to([-5.0, -0.05, 0]), run_time=0.9)
        self.at("does not replace")
        tool = chip("next test", YELLOW, 34).move_to([-1.6, -1.15, 0])
        wheels = VGroup(Circle(0.13, color=YELLOW).move_to([-2.15, -1.75, 0]),
                        Circle(0.13, color=YELLOW).move_to([-1.05, -1.75, 0]))
        cart = VGroup(tool, wheels).shift(RIGHT * 7)
        self.play(cart.animate.shift(LEFT * 7), run_time=1.2)
        self.finish()


class S06Dna(SpokenScene):
    def construct(self):
        tool = chip("DNA test", YELLOW, 36).move_to([-4.75, 1.8, 0])
        self.play(FadeIn(tool, shift=LEFT * 0.2), run_time=0.6)
        self.at("polymerase chain reaction")
        gate = RoundedRectangle(corner_radius=0.22, width=3.2, height=2.5, stroke_color=YELLOW,
                                stroke_width=5, fill_color=YELLOW, fill_opacity=0.08).move_to([-3.5, 0.15, 0])
        gate_lab = T("ideal PCR model", 28, YELLOW).move_to([-3.5, 1.75, 0])
        note = T("real copying is less than perfect", 24, GREY).move_to([-3.5, -1.55, 0])
        self.play(FadeOut(tool), FadeIn(gate), FadeIn(gate_lab), run_time=0.9)
        self.at("copies one chosen stretch")
        one = Rectangle(width=1.2, height=0.34, stroke_width=0, fill_color=GREEN,
                        fill_opacity=1).move_to([-4.7, 0.15, 0])
        two = VGroup(one.copy(), one.copy()).arrange(DOWN, buff=0.22).move_to([-2.3, 0.15, 0])
        four = VGroup(*[one.copy().scale(0.82) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.18).move_to([-0.35, 0.15, 0])
        self.play(FadeIn(one), run_time=0.4)
        self.play(TransformFromCopy(one, two), FadeIn(note), run_time=0.75)
        self.play(TransformFromCopy(two, four), run_time=0.75)
        self.at("gel sorts DNA")
        self.play(FadeOut(VGroup(gate, gate_lab, note, one, two)), four.animate.scale(0.6).move_to([-5.25, 2.2, 0]), run_time=0.8)
        gel = RoundedRectangle(corner_radius=0.12, width=7.1, height=5.6, stroke_color=GREY,
                               stroke_width=4, fill_color=GREY, fill_opacity=0.20).move_to([1.45, 0.0, 0])
        gel_lab = T("schematic sizes", 28, GREY).move_to([1.45, 3.18, 0])
        sizes = np.array([500.0, 1000.0, 2000.0])
        xs = np.array([-0.5, 1.45, 3.4])
        top_y, bottom_y = 2.3, -2.15
        # Migration is assigned from log(size): smaller pieces travel farther down this schematic gel.
        travel = (np.log(sizes.max()) - np.log(sizes)) / (np.log(sizes.max()) - np.log(sizes.min()))
        ys = top_y - (0.8 + 2.9 * travel)
        wells = VGroup(*[Rectangle(width=1.05, height=0.24, stroke_color=GREY, stroke_width=3).move_to([x, top_y, 0]) for x in xs])
        bands = VGroup(*[Rectangle(width=1.12, height=0.22, stroke_width=0, fill_color=GREEN,
                                  fill_opacity=1).move_to([x, top_y, 0]) for x in xs])
        self.play(FadeIn(gel), FadeIn(gel_lab), FadeIn(wells), FadeIn(bands), run_time=1.0)
        pulse(gel, base=4, amp=0.6, speed=1.2)
        self.at("shorter pieces traveling farther")
        self.play(*[band.animate.move_to([x, y, 0]) for band, x, y in zip(bands, xs, ys)], run_time=1.6)
        self.at("expected band supports")
        expected = SurroundingRectangle(bands[1], color=TEAL, buff=0.2, stroke_width=5)
        check = T("✓ insert", 32, TEAL, weight=BOLD).move_to([5.85, -1.5, 0])
        self.play(Create(expected), FadeIn(check), run_time=0.8)
        self.at("Sequencing can confirm")
        identity = chip("sequence identity", YELLOW, 28).move_to([-4.85, -1.3, 0])
        self.play(FadeOut(four), FadeIn(identity), expected.animate.set_color(YELLOW), run_time=0.9)
        self.finish()


class S07Protein(SpokenScene):
    def construct(self):
        band = Rectangle(width=2.0, height=0.3, stroke_width=0, fill_color=GREEN,
                         fill_opacity=1).move_to([-4.5, 1.5, 0])
        band_box = SurroundingRectangle(band, color=TEAL, buff=0.22)
        self.play(FadeIn(band), Create(band_box), run_time=0.65)
        self.at("does not show insulin")
        protein_box = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=3.1, height=1.0,
                                                      stroke_color=GREEN, stroke_width=4), num_dashes=28)
        protein_lab = T("insulin protein?", 30, GREEN).move_to(protein_box)
        protein = VGroup(protein_box, protein_lab).move_to([-4.5, -0.3, 0])
        not_shown = T("not shown", 28, RED, weight=BOLD).move_to([-4.5, -1.25, 0])
        self.play(FadeIn(protein), FadeIn(not_shown), run_time=0.8)
        self.at("Use a protein test")
        self.play(FadeOut(VGroup(band, band_box, protein, not_shown)), run_time=0.5)
        labels = ("engineered cells", "empty plasmid", "known insulin")
        xs = (-4.25, 0.0, 4.25)
        wells = VGroup()
        for x, lab in zip(xs, labels):
            w = RoundedRectangle(corner_radius=0.18, width=3.55, height=4.65, stroke_color=YELLOW,
                                 stroke_width=4, fill_color=YELLOW, fill_opacity=0.20).move_to([x, 0.15, 0])
            t = fit_text(lab, max_w=3.1, size=29, color=TEXT).move_to([x, 2.0, 0])
            wells.add(VGroup(w, t))
        self.play(FadeIn(wells[0]), run_time=0.55)
        self.at("empty plasmid control")
        self.play(FadeIn(wells[1]), run_time=0.55)
        self.at("known insulin sample")
        self.play(FadeIn(wells[2]), run_time=0.55)
        self.at("signal in the engineered")
        signals = VGroup()
        for x in (xs[0], xs[2]):
            bar = Rectangle(width=1.3, height=0.2, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([x, -1.55, 0])
            signals.add(bar)
        self.play(signals[0].animate.stretch_to_fit_height(2.5).move_to([xs[0], -0.4, 0]), run_time=1.0)
        self.at("controls behaving correctly")
        zero = T("no signal", 27, GREY).move_to([xs[1], -1.45, 0])
        self.play(FadeIn(zero), FadeIn(signals[1]),
                  signals[1].animate.stretch_to_fit_height(2.5).move_to([xs[2], -0.4, 0]), run_time=1.0)
        self.at("supports production")
        check = T("✓ protein made", 34, TEAL, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(check, shift=UP * 0.1), run_time=0.7)
        self.at("Purity and function")
        next_q = VGroup(chip("purity?", RED, 27), chip("function?", RED, 27)).arrange(RIGHT, buff=0.35).move_to([0, 3.25, 0])
        self.play(FadeOut(check), FadeIn(next_q), run_time=0.8)
        self.finish()


class S08Uses(SpokenScene):
    def construct(self):
        b = bench()
        start = VGroup(plasmid([0, 0.35, 0], 1.38, 16),
                       T("same testing logic", 38, TEAL, weight=BOLD).move_to([0, -1.55, 0]))
        self.play(FadeIn(b), FadeIn(start), run_time=0.6)
        self.at("A crop")
        cards = VGroup(use_card("crop", GREEN, -4.25),
                       use_card("blood stem cell", BLUE, 0.0),
                       use_card("research cell", YELLOW, 4.25))
        self.play(ReplacementTransform(start, cards[0]), run_time=0.7)
        self.at("edited blood stem cell")
        self.play(FadeIn(cards[1], shift=UP * 0.15), run_time=0.7)
        self.at("research cell")
        self.play(FadeIn(cards[2], shift=UP * 0.15), run_time=0.7)
        self.at("specific change")
        for c in cards:
            c[2].add_updater(lambda mob, dt: mob.rotate(0.045 * dt))
        self.play(*[Indicate(c[2], color=BLUE, scale_factor=1.15) for c in cards], run_time=0.9)
        self.at("Measure the intended")
        brackets = VGroup(*[Brace(c[3], DOWN, color=TEAL) for c in cards])
        self.play(LaggedStart(*[GrowFromCenter(br) for br in brackets], lag_ratio=0.15), run_time=1.0)
        self.at("possible unintended effects")
        self.play(*[Indicate(c[4], color=RED, scale_factor=1.3) for c in cards], run_time=0.9)
        self.at("and limits")
        limits = VGroup(*[T("limits?", 25, RED).move_to(c[4]) for c in cards])
        self.play(*[Transform(c[4], lim) for c, lim in zip(cards, limits)], run_time=0.7)
        self.at("not transfer one result")
        separators = VGroup(Line([-2.15, -1.9, 0], [-2.15, 2.55, 0], color=GREY, stroke_width=4),
                            Line([2.15, -1.9, 0], [2.15, 2.55, 0], color=GREY, stroke_width=4))
        self.play(Create(separators), cards[0].animate.shift(LEFT * 0.15), cards[2].animate.shift(RIGHT * 0.15), run_time=0.9)
        self.finish()


YEARS = np.array([2000, 2004, 2008, 2010, 2016, 2020, 2024, 2025], dtype=float)
CORN = np.array([25, 47, 80, 86, 92, 92, 94, 94], dtype=float)
SOY = np.array([54, 85, 92, 93, 94, 94, 96, 96], dtype=float)


def adoption_plot():
    p = Plot(box=(-5.75, 2.0, -2.25, 2.35), xr=(2000, 2025), yr=(0, 100),
             xticks=[(2000, "2000"), (2025, "2025")],
             yticks=[(0, "0%"), (100, "100%")], xlabel="year", ylabel="adoption")
    corn_fn = lambda year: float(np.interp(year, YEARS, CORN))
    soy_fn = lambda year: float(np.interp(year, YEARS, SOY))
    return p, corn_fn, soy_fn


class S09Data(SpokenScene):
    def construct(self):
        crop = use_card("crop survey", GREEN, -3.7).scale(0.9)
        self.play(FadeIn(crop), run_time=0.7)
        self.at("Its lines rise")
        self.play(FadeOut(crop), run_time=0.4)
        p, corn_fn, soy_fn = adoption_plot()
        year = ValueTracker(2000)
        corn_line = p.live_curve(corn_fn, year, color=GREEN, width=7)
        soy_line = p.live_curve(soy_fn, year, color=BLUE, width=7)
        corn_dot = p.dot(lambda: year.get_value(), lambda: corn_fn(year.get_value()), color=GREEN)
        soy_dot = p.dot(lambda: year.get_value(), lambda: soy_fn(year.get_value()), color=BLUE)
        title = T("adoption", 36, TEAL, weight=BOLD).move_to([-1.85, 3.2, 0])
        plot_back = RoundedRectangle(corner_radius=0.16, width=8.45, height=5.8, stroke_width=0,
                                     fill_color=GREY, fill_opacity=0.20).move_to([-1.85, 0.05, 0])
        self.play(FadeIn(plot_back), Create(p), FadeIn(title), run_time=0.9)
        self.add(corn_line, soy_line, corn_dot, soy_dot)
        self.at("planted with engineered varieties")
        self.play(year.animate.set_value(2025), run_time=2.2, rate_func=linear)
        endpoints = VGroup(T("corn 94%", 28, GREEN).move_to([3.65, 1.55, 0]),
                           T("soybean 96%", 28, BLUE).move_to([3.65, 2.65, 0]))
        self.play(FadeIn(endpoints), run_time=0.55)
        self.at("data show adoption")
        self.play(Indicate(title, color=TEAL, scale_factor=1.15), run_time=0.75)
        self.at("do not show safety")
        qs = VGroup(*[chip(s + " ?", RED, 25) for s in ("safety", "environment", "benefit", "fairness")])
        qs.arrange(DOWN, buff=0.18).move_to([5.05, -0.35, 0])
        self.play(FadeIn(qs[0], shift=LEFT * 0.1), run_time=0.45)
        self.at("environmental effect")
        self.play(FadeIn(qs[1], shift=LEFT * 0.1), run_time=0.45)
        self.at("farmer benefit")
        self.play(FadeIn(qs[2], shift=LEFT * 0.1), run_time=0.45)
        self.at("or fairness")
        self.play(FadeIn(qs[3], shift=LEFT * 0.1), run_time=0.45)
        self.at("require other evidence")
        self.play(qs.animate.set_stroke(TEAL), run_time=0.8)
        self.finish()


class S10Judge(SpokenScene):
    def construct(self):
        use = use_card("one use", GREEN, 0).scale(0.92)
        use[4].shift(LEFT * 0.45 + UP * 0.4)
        evidence_lens = Circle(radius=2.05, color=TEAL, stroke_width=7).move_to([-3.1, 0.2, 0])
        values_lens = Circle(radius=2.05, color=PURPLE, stroke_width=7).move_to([3.1, 0.2, 0])
        evidence_lens.set_fill(TEAL, opacity=0.16)
        values_lens.set_fill(PURPLE, opacity=0.16)
        ev_title = T("evidence", 34, TEAL, weight=BOLD).move_to([-3.1, 2.8, 0])
        va_title = T("values", 34, PURPLE, weight=BOLD).move_to([3.1, 2.8, 0])
        self.play(FadeIn(use), Create(evidence_lens), run_time=0.8)
        self.at("estimate benefits and risks")
        self.play(FadeIn(ev_title), evidence_lens.animate.move_to(use), run_time=0.9)
        self.at("cannot choose every value")
        self.play(Create(values_lens), FadeIn(va_title), run_time=0.5)
        self.play(values_lens.animate.move_to(use), run_time=0.55)
        self.at("who wrote the claim")
        ev_items = VGroup(T("source", 29, TEAL), T("support", 29, TEAL), T("review", 29, TEAL)).arrange(DOWN, buff=0.28)
        ev_items.move_to([-3.85, 0.1, 0])
        self.play(evidence_lens.animate.move_to([-3.85, 0.1, 0]), FadeIn(ev_items[0]), run_time=0.65)
        self.at("what evidence supports")
        self.play(FadeIn(ev_items[1]), run_time=0.55)
        self.at("other scientists checked")
        self.play(FadeIn(ev_items[2]), run_time=0.55)
        self.at("discuss access")
        val_items = VGroup(T("access", 29, PURPLE), T("safety", 29, PURPLE), T("limits", 29, PURPLE)).arrange(DOWN, buff=0.28)
        val_items.move_to([3.85, 0.1, 0])
        self.play(values_lens.animate.move_to([3.85, 0.1, 0]), FadeIn(val_items[0]), run_time=0.65)
        self.at("safety")
        self.play(FadeIn(val_items[1]), run_time=0.5)
        self.at("and limits")
        self.play(FadeIn(val_items[2]), run_time=0.5)
        self.at("particular use")
        self.play(Indicate(use, color=GREEN, scale_factor=1.06), run_time=0.7)
        self.at("Reasonable people may weigh")
        self.play(values_lens.animate.shift(UP * 0.2), evidence_lens.animate.shift(DOWN * 0.2), run_time=1.0)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        xs = (-5.1, -1.8, 1.6, 5.0)
        change = VGroup(plasmid([xs[0], 0.2, 0], 0.82, 11), T("change", 28, BLUE).move_to([xs[0], -1.35, 0]))
        test = VGroup(chip("test", YELLOW, 32).move_to([xs[1], 0.2, 0]), T("claim", 28, TEXT).move_to([xs[1], -1.35, 0]))
        effect = VGroup(T("✓", 62, TEAL, weight=BOLD).move_to([xs[2], 0.2, 0]), T("effect", 28, GREEN).move_to([xs[2], -1.35, 0]))
        judge = VGroup(Circle(0.78, color=TEAL, stroke_width=5).move_to([xs[3]-0.25, 0.2, 0]),
                       Circle(0.78, color=PURPLE, stroke_width=5).move_to([xs[3]+0.25, 0.2, 0]),
                       T("one use", 28, TEXT).move_to([xs[3], -1.35, 0]))
        links = VGroup(arrow([xs[0]+1.0, 0.2, 0], [xs[1]-1.0, 0.2, 0]),
                       arrow([xs[1]+1.0, 0.2, 0], [xs[2]-0.9, 0.2, 0]),
                       arrow([xs[2]+0.8, 0.2, 0], [xs[3]-1.0, 0.2, 0]))
        track = RoundedRectangle(corner_radius=0.3, width=12.75, height=4.15, stroke_width=0,
                                 fill_color=TEAL, fill_opacity=0.17).move_to([0, 0.25, 0])
        scan = Rectangle(width=1.3, height=3.8, stroke_width=0, fill_color=TEAL,
                         fill_opacity=0.13).move_to([-5.55, 0.25, 0])
        def move_scan(mob, dt):
            mob.shift(RIGHT * 1.7 * dt)
            if mob.get_x() > 5.75:
                mob.move_to([-5.75, 0.25, 0])
        scan.add_updater(move_scan)
        self.play(FadeIn(track), FadeIn(scan), Create(change[0]), FadeIn(change[1]), run_time=0.8)
        change[0].add_updater(lambda mob, dt: mob.rotate(0.05 * dt))
        self.at("start of an explanation")
        self.play(GrowArrow(links[0]), FadeIn(test), run_time=0.8)
        self.at("not the end")
        q = T("?", 50, RED, weight=BOLD).move_to([0, 2.6, 0])
        self.play(FadeIn(q), run_time=0.6)
        self.at("Match each claim")
        self.play(Indicate(test, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("keep uncertainty visible")
        q2 = q.copy().move_to([3.25, 2.6, 0])
        self.play(TransformFromCopy(q, q2), run_time=0.6)
        self.at("judge cases")
        self.play(GrowArrow(links[1]), FadeIn(effect), GrowArrow(links[2]), FadeIn(judge), run_time=1.1)
        self.at("Engineering changes")
        rule = caption("Engineering changes DNA; test effects and judge each use separately.", size=34, color=GOLD, y=-3.05)
        self.play(FadeIn(rule, shift=UP * 0.1), change[0].animate.rotate(0.4), run_time=0.8)
        self.at("test the effects")
        self.play(Indicate(effect, color=TEAL, scale_factor=1.12), run_time=0.65)
        self.at("judge each")
        self.play(Indicate(judge, color=PURPLE, scale_factor=1.12), run_time=0.65)
        self.finish()


class S12End(EndCard):
    LINE = "Engineering changes a cell's DNA; test the effects, judge each use separately."
