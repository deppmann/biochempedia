"""What Followed the Trait? — animated explainer.

COLOR MAP
  BLUE  DNA and phosphorus-rich tracer
  GOLD  protein and sulfur-containing tracer
  TEAL  living rough recipient cells and bacterial outlines
  GREEN donor-type capsule and transformation activity
  GREY  apparatus, limits, and neutral structure
"""
from bp_parts import *  # noqa: F401,F403


def bench_stage():
    """The film's single landscape: a softly lit laboratory bench."""
    panel = RoundedRectangle(corner_radius=0.28, width=13.0, height=6.25,
                             stroke_width=0, fill_color=GREY,
                             fill_opacity=0.16).set_z_index(-20)
    glow = Line([-6.1, -2.75, 0], [-6.1, 2.75, 0], color=TEAL,
                stroke_width=54, stroke_opacity=0.20).set_z_index(-19)
    glow._travel = 0.0

    def travel(mob, dt):
        mob._travel = (mob._travel + dt) % 6.0
        mob.set_x(-6.1 + 12.2 * mob._travel / 6.0)
    glow.add_updater(travel)
    return VGroup(panel, glow)


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(bench_stage())


def arrow(a, b, color=GREY, width=5):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=width, tip_length=0.22)


def bacterium(capsule=False, scale=1.0, color=TEAL):
    body = RoundedRectangle(corner_radius=0.42, width=1.65, height=0.78,
                            stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.18)
    core = VGroup(Dot(LEFT * 0.33, radius=0.07, color=color),
                  Dot(RIGHT * 0.33, radius=0.07, color=color))
    parts = VGroup(body, core)
    if capsule:
        halo = RoundedRectangle(corner_radius=0.54, width=1.92, height=1.05,
                                stroke_color=GREEN, stroke_width=7,
                                fill_color=GREEN, fill_opacity=0.07)
        parts = VGroup(halo, body, core)
    return parts.scale(scale)


def bench_world(descendants=True):
    """Carried hook picture, rebuilt at identical positions."""
    rough = VGroup(*[bacterium().move_to([-4.65, y, 0]) for y in (1.3, 0.0, -1.3)])
    donors = VGroup(*[bacterium(True, color=GREY).set_opacity(0.55).move_to([0, y, 0])
                      for y in (1.15, -0.15)])
    question = T("?", 82, GOLD, weight=BOLD).move_to([0, -1.65, 0])
    desc = VGroup(*[bacterium(True).move_to([4.55, y, 0]) for y in (1.45, 0.15, -1.15)])
    labels = VGroup(T("living rough", 28, TEAL).move_to([-4.65, 2.55, 0]),
                    T("heat-killed donor", 28, GREEN).move_to([0, 2.55, 0]))
    g = VGroup(rough, donors, question, labels)
    if descendants:
        g.add(desc, T("living donor type", 28, GREEN).move_to([4.55, 2.55, 0]))
    g.rough, g.donors, g.question, g.desc, g.labels = rough, donors, question, desc, labels
    return g


def tray_world(count=5, lamp=True):
    tray = RoundedRectangle(corner_radius=0.2, width=4.15, height=3.6,
                            stroke_color=GREY, stroke_width=3).move_to([4.15, -0.15, 0])
    pts = [(-1.35, 0.8), (0, 0.85), (1.25, 0.65), (-0.8, -0.45), (0.75, -0.6)]
    colonies = VGroup(*[bacterium(i < count, 0.48).move_to([4.15 + x, -0.2 + y, 0])
                        for i, (x, y) in enumerate(pts)])
    light = Circle(radius=0.25, stroke_color=GREEN if lamp else GREY, stroke_width=4,
                   fill_color=GREEN if lamp else GREY, fill_opacity=0.7 if lamp else 0.1).move_to([5.75, 1.15, 0])
    lab = T("recipient culture", 28, TEAL).move_to([4.15, 2.45, 0])
    g = VGroup(tray, colonies, light, lab)
    g.colonies, g.light = colonies, light
    return g


def enzyme_world(question=False):
    gates = VGroup()
    for x, name, col in [(-3.9, "protein", GOLD), (0, "RNA", TEAL), (3.9, "DNA", BLUE)]:
        box = RoundedRectangle(corner_radius=0.18, width=3.15, height=2.2,
                               stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.1).move_to([x, 0.65, 0])
        name_t = T(name, 32, col, weight=BOLD).move_to([x, 1.25, 0])
        check = chip("target checked", GREEN, size=24).move_to([x, 0.25, 0])
        lamp = Circle(radius=0.22, color=GREEN if name != "DNA" or not question else GREY,
                      fill_opacity=0.75 if name != "DNA" or not question else 0.1).move_to([x, -0.95, 0])
        gates.add(VGroup(box, name_t, check, lamp))
    stream = chip("active fraction", BLUE, size=30).move_to([0, 2.8, 0])
    paths = VGroup(*[arrow(stream.get_bottom(), g[0].get_top(), BLUE, 4) for g in gates])
    return VGroup(stream, paths, gates)


def phage_cartoon(scale=1.0):
    coat = VGroup(RegularPolygon(6, radius=0.9, color=GOLD, stroke_width=6,
                                 fill_color=GOLD, fill_opacity=0.13).rotate(PI / 6),
                  Line([0, -0.78, 0], [0, -1.62, 0], color=GOLD, stroke_width=6),
                  Line([0, -1.62, 0], [-0.5, -2.0, 0], color=GOLD, stroke_width=5),
                  Line([0, -1.62, 0], [0.5, -2.0, 0], color=GOLD, stroke_width=5))
    dna = (chip("DNA", BLUE, size=30, pad=0.13) if scale >= 0.8 else
           RoundedRectangle(corner_radius=0.12, width=0.95, height=0.48,
                            color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35))
    dna.move_to([0, 0, 0])
    g = VGroup(coat, dna).scale(scale)
    g.coat, g.dna = coat, dna
    return g


def tube_world():
    tube = RoundedRectangle(corner_radius=0.5, width=3.3, height=5.25,
                            stroke_color=TEAL, stroke_width=5).move_to([0.2, 0.05, 0])
    fluid = Rectangle(width=2.85, height=2.65, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.08).move_to([0.2, 0.7, 0])
    surface = Line([-1.2, 2.02, 0], [1.6, 2.02, 0], color=TEAL, stroke_width=4)
    pellet = Ellipse(width=2.1, height=0.55, color=TEAL, fill_color=TEAL,
                     fill_opacity=0.35).move_to([0.2, -2.1, 0])
    labels = VGroup(T("fluid", 28, TEAL).move_to([0.2, 1.55, 0]),
                    T("cell pellet", 28, TEAL).move_to([0.2, -1.55, 0]))
    return VGroup(tube, fluid, surface, pellet, labels)


class S01Hook(FilmScene):
    def construct(self):
        world = bench_world()
        self.at("Dead bacteria")
        self.play(FadeIn(world.donors, shift=DOWN * 0.2), run_time=0.8)
        self.at("living bacteria")
        self.play(FadeIn(world.rough, shift=RIGHT * 0.3), run_time=0.8)
        self.at("What crossed")
        self.play(FadeIn(world.question, scale=0.6), run_time=0.7)
        self.at("Living rough cells")
        self.play(FadeIn(world.labels[0]), LaggedStart(*[Indicate(c, color=TEAL) for c in world.rough], lag_ratio=0.2), run_time=1.0)
        self.at("Heat killed smooth cells")
        self.play(FadeIn(world.labels[1]), world.donors.animate.set_opacity(0.35), run_time=0.9)
        self.at("Yet mixing them")
        self.play(world.rough.animate.shift(RIGHT * 1.25), world.donors.animate.shift(LEFT * 1.0), run_time=1.2)
        self.at("living capsule bearing cells")
        self.play(FadeIn(world.desc, shift=RIGHT * 0.35), FadeIn(T("living donor type", 28, GREEN).move_to([4.55, 2.55, 0])), run_time=1.0)
        self.at("Their descendants")
        daughters = VGroup(*[bacterium(True, 0.7).move_to([3.6 + i * 0.95, -2.3, 0]) for i in range(3)])
        self.play(TransformFromCopy(world.desc[1], daughters), run_time=1.1)
        self.at("Neither ingredient alone")
        self.play(Indicate(VGroup(world.rough, world.donors), color=GOLD, scale_factor=1.03), run_time=1.0)
        self.add(scope_tag("schematic"))
        bob(daughters, amp=0.035, speed=1.2)
        self.finish()


class S02Title(TitleCard):
    LESSON = "DNA: The Genetic Material"
    TITLE = "What Followed the Trait?"


class S03Assay(FilmScene):
    def construct(self):
        mouse = VGroup(Ellipse(width=1.5, height=0.8, color=GREY, fill_opacity=0.18),
                       Circle(radius=0.25, color=GREY).move_to([0.75, 0.18, 0]),
                       Arc(radius=0.65, start_angle=PI, angle=PI, color=GREY).move_to([-0.8, 0, 0])).move_to([-4.6, 0.6, 0])
        self.at("Griffith's mouse experiment")
        self.play(FadeIn(mouse), FadeIn(T("transformation", 34, GREEN).move_to([-4.4, 2.4, 0])), run_time=0.9)
        unknown = chip("unknown substance", GOLD, size=30).move_to([-1.0, 0.6, 0])
        self.at("did not name")
        self.play(FadeIn(unknown), run_time=0.7)
        self.at("pointed to an assay")
        self.play(FadeOut(mouse), unknown.animate.move_to([-4.0, 0.8, 0]), run_time=0.8)
        culture = T("later laboratories: culture", 28, TEAL).move_to([-0.8, 1.85, 0])
        self.at("Later laboratories")
        self.play(FadeIn(culture), run_time=0.7)
        drop = chip("donor extract", GREEN, size=30).move_to([-4.0, 0.8, 0])
        self.at("Add a donor extract")
        self.play(ReplacementTransform(unknown, drop), run_time=0.7)
        funnels = VGroup(*[Triangle(color=GREY, stroke_width=4).scale(0.42).rotate(PI).move_to([x, 0.8, 0]) for x in (-1.6, -0.2, 1.2)])
        pipe = VGroup(arrow(drop.get_right(), funnels[0].get_left(), BLUE, 4),
                      arrow(funnels[0].get_right(), funnels[1].get_left(), BLUE, 4),
                      arrow(funnels[1].get_right(), funnels[2].get_left(), BLUE, 4))
        self.play(LaggedStart(*[FadeIn(f) for f in funnels], lag_ratio=0.2), Create(pipe), run_time=1.1)
        tray = tray_world(0, lamp=False)
        self.at("rough recipients")
        self.play(FadeIn(tray), run_time=0.8)
        n = ValueTracker(0)
        read = counter("donor-type colonies  {:.0f}", n, [3.2, -2.75, 0], size=28, color=GREEN)
        self.add(read)
        self.at("count colonies")
        transformed = tray_world(5, lamp=True)
        self.play(ReplacementTransform(tray, transformed), n.animate.set_value(5), run_time=1.7)
        self.at("followed through purification")
        self.play(LaggedStart(*[Indicate(f, color=BLUE) for f in funnels], lag_ratio=0.18), run_time=1.1)
        self.at("scored phenotype")
        self.play(Indicate(transformed.colonies, color=GREEN), run_time=1.0)
        self.finish()


class S04Predict(FilmScene):
    def construct(self):
        world = enzyme_world(question=True)
        self.at("purified the active fraction")
        self.play(FadeIn(world[0], shift=DOWN * 0.2), run_time=0.8)
        self.at("challenged separate samples")
        self.play(Create(world[1]), LaggedStart(*[FadeIn(g[0:2]) for g in world[2]], lag_ratio=0.2), run_time=1.2)
        self.at("Protein digesting enzymes")
        self.play(FadeIn(world[2][0][2:]), Indicate(world[2][0][3], color=GREEN), run_time=0.9)
        self.at("RNA digesting enzyme")
        self.play(FadeIn(world[2][1][2:]), Indicate(world[2][1][3], color=GREEN), run_time=0.9)
        self.at("Each enzyme was first checked")
        self.play(FadeIn(world[2][2][2]), LaggedStart(*[Indicate(g[2], color=GREEN) for g in world[2]], lag_ratio=0.2), run_time=1.2)
        self.at("Now predict")
        self.play(FadeOut(world[2][0]), FadeOut(world[2][1]), world[2][2].animate.scale(1.35).move_to([0, 0.45, 0]), FadeOut(world[1]), run_time=1.0)
        q = question_card("If intact DNA is required, what happens here?", y=-3.1, size=30)
        self.at("If intact DNA")
        self.play(FadeIn(q.question), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "If intact DNA is required, what happens here?"
    SECONDS = 4.5

    def backdrop(self):
        gate = enzyme_world(question=True)[2][2]
        gate.scale(1.35).move_to([0, 0.45, 0])
        blocks = VGroup(*[chip("DNA", BLUE, size=24).move_to([-5.4 + i * 1.15, 2.15, 0]) for i in range(3)])
        bob(blocks, amp=0.05, speed=1.1)
        return VGroup(bench_stage(), gate, blocks)


class S06Reveal(FilmScene):
    def construct(self):
        gate = enzyme_world(question=True)[2][2].scale(1.25).move_to([-3.8, 0.55, 0])
        blocks = VGroup(*[chip("DNA", BLUE, size=24).move_to([-6.0 + i * 1.2, 3.05, 0]) for i in range(3)])
        self.add(gate, blocks)
        self.at("removed activity")
        fragments = VGroup(*[Rectangle(width=0.32, height=0.16, color=BLUE, fill_opacity=0.7).move_to([-2.9 + i * 0.42, 1.6 - (i % 2) * 0.35, 0]) for i in range(5)])
        self.play(ReplacementTransform(blocks, fragments), gate[3].animate.set_fill(GREY, opacity=0.05), run_time=1.2)
        ledger = Ledger([("chemistry", "matched nucleic acid", BLUE),
                         ("selective destruction", "activity removed", BLUE),
                         ("heredity", "donor type persisted", GREEN)],
                        top_left=(-0.8, 2.1), title="evidence", width=6.8, key_w=3.1, row_h=0.75, size=26)
        self.at("Chemistry also matched")
        self.play(FadeIn(ledger), ledger.reveal(0), run_time=0.9)
        self.at("transformed cells passed")
        self.play(ledger.reveal(2), run_time=0.8)
        self.at("concluded that the fraction")
        self.play(ledger.reveal(1), run_time=0.8)
        conclusion = caption("principally, if not solely, DNA", color=BLUE, y=-2.75)
        self.at("principally")
        self.play(FadeIn(conclusion), run_time=0.8)
        limit = DashedLine([-0.5, -1.45, 0], [5.7, -1.45, 0], color=GOLD, stroke_width=3)
        q = chip("?", GOLD, size=28).move_to([4.9, -2.05, 0])
        lab = T("detection limit", 26, GOLD).move_to([2.2, -1.15, 0])
        self.at("protein below detection")
        self.play(Create(limit), FadeIn(q), FadeIn(lab), run_time=0.9)
        self.at("hedge preserved")
        self.play(Indicate(VGroup(limit, q), color=GOLD), run_time=1.0)
        self.finish()


class S07PhageSetup(FilmScene):
    def construct(self):
        bact = Ellipse(width=5.2, height=2.3, color=TEAL, stroke_width=6,
                       fill_color=TEAL, fill_opacity=0.12).move_to([3.2, -0.25, 0])
        self.at("One system was not enough")
        self.play(FadeIn(bact), run_time=0.7)
        p1, p2 = phage_cartoon(1.0).move_to([-4.2, 1.3, 0]), phage_cartoon(1.0).move_to([-4.2, -1.25, 0])
        self.at("Hershey and Chase")
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.9)
        coat_lab = chip("protein coat", GOLD, size=28).move_to([-1.3, 2.55, 0])
        dna_lab = chip("DNA", BLUE, size=28).move_to([-1.3, 1.75, 0])
        self.at("protein coat around DNA")
        self.play(FadeIn(coat_lab), FadeIn(dna_lab), run_time=0.8)
        sulfur = chip("sulfur tracer", GOLD, size=26).move_to([-1.35, -1.6, 0])
        phosph = chip("phosphorus tracer", BLUE, size=26).move_to([-1.35, -2.65, 0])
        self.at("sulfur containing protein")
        self.play(FadeIn(sulfur), Indicate(p1.coat, color=GOLD), run_time=0.9)
        self.at("phosphorus rich")
        self.play(FadeIn(phosph), Indicate(p2.dna, color=BLUE), run_time=0.9)
        self.at("protein gold and DNA blue")
        self.play(FadeOut(VGroup(coat_lab, dna_lab, sulfur, phosph)),
                  p1.animate.shift(RIGHT * 2.3), p2.animate.shift(RIGHT * 2.3), run_time=1.4)
        self.at("Where each color travelled")
        self.play(p1.animate.shift(RIGHT * 1.9), p2.animate.shift(RIGHT * 1.9), run_time=1.2)
        self.at("independent physical test")
        self.play(Indicate(VGroup(p1, p2, bact), color=TEAL), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S08Blend(FilmScene):
    def construct(self):
        bact = Ellipse(width=5.2, height=2.3, color=TEAL, stroke_width=6,
                       fill_color=TEAL, fill_opacity=0.12)
        coats = VGroup(*[phage_cartoon(0.6).move_to([-2.0 + i * 2.0, 1.65, 0]) for i in range(3)])
        self.at("Both phage batches")
        self.play(FadeIn(bact), FadeIn(coats), run_time=0.9)
        blue_in = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.8, height=0.42,
                                           color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to([-1.6 + i * 1.6, 0, 0]) for i in range(3)])
        self.play(FadeIn(blue_in, shift=DOWN * 0.5), run_time=0.8)
        vortex = Arc(radius=2.1, start_angle=0, angle=TAU * 0.85, color=TEAL, stroke_width=7)
        self.at("Blending removed")
        self.play(Create(vortex), coats.animate.shift(RIGHT * 0.6).rotate(0.5), run_time=1.2)
        tube = tube_world()
        self.at("centrifugation separated")
        self.play(FadeOut(VGroup(bact, vortex, coats, blue_in)), FadeIn(tube), run_time=1.0)
        gold = ValueTracker(0)
        blue = ValueTracker(0)
        ro = Readout([("fluid S", lambda: gold.get_value(), "{:4.0f}%", GOLD),
                      ("fluid P", lambda: blue.get_value(), "{:4.0f}%", BLUE)],
                     at=[4.15, 1.2, 0], widest=[100, 100], title="in fluid")
        self.at("Most gold sulfur")
        self.add(ro)
        self.play(gold.animate.set_value(75), run_time=1.3)
        self.at("Much less blue")
        self.play(blue.animate.set_value(15), run_time=1.1)
        progeny = VGroup(*[phage_cartoon(0.32).move_to([3.0 + i * 1.05, -2.25, 0]) for i in range(4)])
        self.at("stripped cells still produced")
        self.play(FadeIn(progeny, shift=RIGHT * 0.3), run_time=1.2)
        prog = VGroup(chip("S <1%", GOLD, size=28), chip("P 30% or more", BLUE, size=28)).arrange(DOWN, buff=0.25).move_to([4.35, -0.8, 0])
        self.at("progeny carried")
        self.play(FadeIn(prog), run_time=1.0)
        self.at("Exact percentages")
        self.play(Indicate(VGroup(ro, prog), color=TEXT), run_time=1.0)
        self.finish()


class S09Limits(FilmScene):
    def construct(self):
        tube = tube_world().move_to([-2.8, 0, 0])
        self.add(tube)
        title = T("Tracer limits", 36, GOLD, weight=BOLD).move_to([2.9, 2.75, 0])
        self.at("tracers set limits")
        self.play(FadeIn(title), run_time=0.7)
        bracket = Brace(Line([1.0, 1.4, 0], [5.8, 1.4, 0]), UP, color=GREY)
        unmeasured = fit_text("unmeasured sulfur-free material?", max_w=5.3, size=28, color=GREY).move_to([3.4, 2.0, 0])
        self.at("Sulfur could not report")
        self.play(FadeIn(bracket), FadeIn(unmeasured), run_time=0.9)
        no_claim = chip("not: no protein entered", GOLD, size=27).move_to([3.4, 0.6, 0])
        self.at("did not show")
        self.play(FadeIn(no_claim), run_time=0.8)
        remainder = Dot([-1.75, -2.1, 0], radius=0.16, color=GOLD)
        self.at("Some sulfur stayed")
        self.play(FadeIn(remainder, scale=0.3), run_time=0.8)
        self.at("distinction matters")
        self.play(Indicate(VGroup(no_claim, remainder), color=GOLD), run_time=0.9)
        most = VGroup(chip("most DNA entered", BLUE, size=30), chip("most coat stayed out", GOLD, size=30)).arrange(DOWN, buff=0.35).move_to([3.45, -1.25, 0])
        self.at("result was narrower")
        self.play(FadeOut(no_claim), FadeIn(most), run_time=0.9)
        path = Arrow([-1.6, -1.7, 0], [1.3, -1.7, 0], color=BLUE, stroke_width=10, buff=0.2)
        self.at("Inheritance travelled")
        self.play(GrowArrow(path), Indicate(most[0], color=BLUE), run_time=1.2)
        self.finish()


class S10Converge(FilmScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.2, width=12.4, height=5.7, color=GREY, stroke_width=3).move_to([0, 0.15, 0])
        tray = tray_world(4, True)
        tray.remove(tray[3])
        tray.scale(0.72).move_to([-4.25, 0.1, 0])
        tube = tube_world()
        tube.remove(tube[4])
        tube.scale(0.72).move_to([4.25, 0.1, 0])
        center = chip("inherited information", BLUE, size=34, pad=0.3).move_to([0, 0.15, 0])
        self.at("Across two independent systems")
        self.play(FadeIn(frame), FadeIn(tray), FadeIn(tube), run_time=1.0)
        p1 = Arrow([-2.8, 0.35, 0], center.get_left(), color=BLUE, stroke_width=9, buff=0.15)
        self.at("heritable change followed DNA")
        self.play(GrowArrow(p1), FadeIn(center), run_time=1.0)
        intact = T("intact DNA required", 28, BLUE).move_to([-3.9, -2.35, 0])
        self.at("Transformation required")
        self.play(FadeIn(intact), Indicate(tray, color=GREEN), run_time=1.0)
        p2 = Arrow([2.8, 0.35, 0], center.get_right(), color=BLUE, stroke_width=9, buff=0.15)
        phage = T("DNA label → cells → progeny", 28, BLUE).move_to([3.35, 2.45, 0])
        self.at("Phage reproduction")
        self.play(GrowArrow(p2), FadeIn(phage), run_time=1.0)
        limits = VGroup(T("bounded claims", 28, GOLD), T("measured evidence", 28, GOLD)).arrange(DOWN, buff=0.2).move_to([-1.7, 2.25, 0])
        self.at("Neither experiment")
        self.play(FadeIn(limits), run_time=0.9)
        self.at("Convergence")
        pulse(p1, base=9, amp=2, speed=2.5); pulse(p2, base=9, amp=2, speed=2.5)
        self.play(Indicate(center, color=BLUE), run_time=1.2)
        bounded = chip("these systems", GREY, size=28).move_to([0, -2.1, 0])
        self.at("Together")
        self.play(FadeIn(bounded), run_time=0.8)
        self.at("strongest candidate")
        self.play(Indicate(center, color=BLUE, scale_factor=1.05), run_time=1.1)
        self.finish()


class S11End(EndCard):
    LINE = "Heritable information follows DNA across independent experiments."
