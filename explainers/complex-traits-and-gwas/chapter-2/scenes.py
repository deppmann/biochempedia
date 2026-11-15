"""A GWAS Hit Is a Starting Point.

COLOR MAP (kept from chapter 1 and the approved script)
  BLUE  = measured genetic differences and tag SNPs
  GREY  = environment, context, and neutral structure
  GOLD  = questions and candidate causes
  GREEN = converging functional evidence
  RED   = confounding and reduced portability
"""
from bp_parts import *  # noqa: F401,F403
import math


LESSON = "Complex traits and GWAS"
TITLE = "A GWAS Hit Is a Starting Point"


# A quiet, common visual ground: a broad study field and slow data motes.  The motion is
# continuous (not a one-second pulse), so spoken holds remain alive without adding claims.
_PipelineSpokenScene = SpokenScene


class SpokenScene(_PipelineSpokenScene):
    def setup(self):
        super().setup()
        field = Rectangle(width=12.4, height=5.75, stroke_width=0,
                          fill_color=GREY, fill_opacity=0.035).move_to([0, 0.15, 0])
        field.set_z_index(-20)
        self.add(field)
        scanner = Rectangle(width=1.72, height=6.65, stroke_width=0,
                            fill_color=TEAL, fill_opacity=0.18).move_to([-5.65, 0.15, 0])
        scanner.set_z_index(-18)
        def sweep(m, dt):
            m.shift(RIGHT*1.33*dt)
            if m.get_x() > 5.65:
                m.move_to([-5.65, 0.15, 0])
        scanner.add_updater(sweep)
        self.add(scanner)
        motes = VGroup()
        for i in range(24):
            d = Dot(radius=0.035 + 0.012*(i % 3), color=BLUE if i % 4 == 0 else GREY)
            d.set_opacity(0.18).move_to([-5.8 + (i*1.71) % 11.6, -2.5 + (i*0.83) % 5.0, 0])
            d.v = 0.10 + 0.018*(i % 5)
            def drift(m, dt):
                m.shift(RIGHT*m.v*dt)
                if m.get_x() > 6.15:
                    m.shift(LEFT*12.3)
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-15)
        self.add(motes)


def person(x=0, y=-1.8, color=GREY, scale=1.0):
    body = RoundedRectangle(corner_radius=0.14, width=0.52, height=1.05,
                            stroke_color=color, stroke_width=3, fill_color=color,
                            fill_opacity=0.18).move_to([x, y + 0.48, 0])
    head = Circle(radius=0.19, color=color, stroke_width=3, fill_color=color,
                  fill_opacity=0.18).move_to([x, y + 1.23, 0])
    return VGroup(body, head).scale(scale)


def crowd_picture(y=-1.9, scale=1.0, color=GREY):
    xs = np.linspace(-4.7, 4.7, 9)
    hs = [0.88, 1.08, 0.94, 1.18, 1.02, 0.91, 1.14, 0.97, 1.09]
    return VGroup(*[person(x, y, color, h * scale) for x, h in zip(xs, hs)])


def chromosomes(y=1.35):
    bars = VGroup()
    for i, x in enumerate(np.linspace(-4.9, 4.9, 6)):
        bar = RoundedRectangle(corner_radius=0.2, width=1.35, height=0.46,
                               stroke_color=GREY, stroke_width=3, fill_color=GREY,
                               fill_opacity=0.12).move_to([x, y, 0])
        for j in range(3):
            bar.add(Rectangle(width=0.18, height=0.38, stroke_width=0,
                              fill_color=BLUE, fill_opacity=0.75).move_to([x - 0.38 + 0.38*j, y, 0]))
        bars.add(bar)
    return bars


def association_data(adjusted=False):
    """Deterministic synthetic dosage/trait tests; plotted values are computed, never sketched."""
    n, m = 80, 60
    people = np.arange(n)
    ancestry = (people >= n // 2).astype(float)
    dosages = np.zeros((n, m))
    for j in range(m):
        phase = (j * 7) % 19
        base = ((people * (j % 5 + 2) + phase) % 11 > (4 + j % 3)).astype(float)
        extra = ((people + 3*j) % 13 > 9).astype(float)
        dosages[:, j] = base + extra
    # A local linked cluster plus ancestry-correlated markers.
    causal = ((people * 3 + 2) % 10 > 4).astype(float) + ((people + 1) % 9 > 6)
    for j, noise_every in zip(range(39, 44), [17, 13, 11, 9, 7]):
        flip = ((people + j) % noise_every == 0)
        dosages[:, j] = np.clip(causal + flip.astype(float) - ((people + 2*j) % (noise_every+3) == 0), 0, 2)
    for j in [6, 18, 31, 53]:
        dosages[:, j] = np.clip(dosages[:, j] + ancestry, 0, 2)
    trait = 1.65 * causal + 1.5 * ancestry + 0.35*np.sin(people*1.7) + 0.18*np.cos(people*0.31)
    if adjusted:
        trait = trait - np.array([trait[ancestry == g].mean() for g in ancestry])
        dosages = dosages - np.vstack([dosages[ancestry == g].mean(axis=0) for g in ancestry])
    vals = []
    for j in range(m):
        x = dosages[:, j]
        if np.std(x) < 1e-8:
            vals.append(0.0)
            continue
        r = float(np.corrcoef(x, trait)[0, 1])
        z = abs(r) * math.sqrt(n - 2) / math.sqrt(max(1e-6, 1-r*r))
        p = max(math.erfc(z / math.sqrt(2)), 1e-14)
        vals.append(-math.log10(p))
    return np.arange(m), np.array(vals)


def skyline(adjusted=False, dots=60):
    P = Plot(box=(-5.75, 5.75, -1.95, 2.45), xr=(0, 60), yr=(0, 14),
             xticks=[0, 12, 24, 36, 48, 60], yticks=[0, 4, 8, 12],
             xlabel="markers across chromosomes", ylabel="evidence")
    xs, ys = association_data(adjusted)
    points = VGroup(*[Dot(P.pt(float(x), float(y)), radius=0.055,
                          color=(GOLD if 39 <= x <= 43 else BLUE))
                      for x, y in zip(xs[:dots], ys[:dots])])
    return P, points


def ld_world(question=False):
    blocks = VGroup()
    widths = [1.45, 1.75, 2.2, 1.65, 1.35, 1.45]
    x = -5.0
    colors = [GREY, BLUE, BLUE, BLUE, GREY, GREY]
    for w, col in zip(widths, colors):
        blocks.add(RoundedRectangle(corner_radius=0.12, width=w, height=1.15,
                                    stroke_color=col, stroke_width=3, fill_color=col,
                                    fill_opacity=0.16).move_to([x + w/2, -0.65, 0]))
        x += w + 0.08
    xs = [-2.7, -1.65, -0.55, 0.55, 1.45]
    heights = [2.2, 2.75, 3.35, 2.65, 2.15]
    markers = VGroup(*[Line([xx, -0.05, 0], [xx, -0.05+h, 0], color=BLUE,
                                stroke_width=9) for xx, h in zip(xs, heights)])
    candidate = Square(side_length=0.34, color=GOLD, stroke_width=4,
                       fill_color=GOLD, fill_opacity=0.45).rotate(PI/4).move_to([-0.15, -0.65, 0])
    world = VGroup(blocks, markers, candidate)
    if question:
        world.add(question_card("Must the tallest point be the causal variant?"))
    return world


def variant_cards():
    vals = [0.30, 0.26, 0.20, 0.15, 0.09]
    cards = VGroup(*[boxed_label(f"variant {c}", BLUE, 28, box=(1.75, 0.72),
                                fill_opacity=0.08 + v*0.65)
                     for c, v in zip("ABCDE", vals)]).arrange(RIGHT, buff=0.28).move_to([0, 0.45, 0])
    brace = RoundedRectangle(corner_radius=0.22, width=cards.width+0.45, height=cards.height+0.48,
                             color=GOLD, stroke_width=4).move_to(cards)
    label = T("credible set", 30, GOLD).next_to(brace, UP, buff=0.2)
    return VGroup(brace, cards, label)


def gene_blocks(y=-0.35):
    genes = VGroup(*[boxed_label(name, GREEN if name == "neighbor gene" else GREY, 28,
                                 box=(2.7, 0.8), fill_opacity=0.10)
                     for name in ["containing gene", "neighbor gene", "third gene"]])
    genes.arrange(RIGHT, buff=0.55).move_to([0, y, 0])
    return genes


class S01Hook(SpokenScene):
    def construct(self):
        people = crowd_picture()
        bars = chromosomes()
        bob(people, amp=0.035, speed=1.2)
        self.at("The first film")
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.2) for p in people], lag_ratio=0.08), run_time=1.8)
        self.at("which DNA differences")
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.35) for b in bars], lag_ratio=0.12), run_time=1.6)
        q = fit_text("Which DNA differences are involved?", max_w=11.0, size=42, color=GOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN*0.2), run_time=0.7)
        self.at("searches without choosing")
        scan = Line([-5.4, 1.8, 0], [5.4, 1.8, 0], color=BLUE, stroke_width=6)
        self.play(Create(scan), run_time=2.0)
        self.at("study population and setting")
        self.play(people.animate.set_color(GREY), bars.animate.set_opacity(0.72), run_time=1.5)
        self.add(scope_tag("chromosomes: schematic"))
        self.finish()


class S02Title(TitleCard):
    LESSON = LESSON
    TITLE = TITLE


class S03Scan(SpokenScene):
    def construct(self):
        people = crowd_picture(y=-2.25, scale=0.72)
        P, pts = skyline()
        trait = boxed_label("trait value", GREY, 28).move_to([-3.0, 2.95, 0])
        allele = boxed_label("allele count", BLUE, 28).move_to([0.2, 2.95, 0])
        self.at("Each person contributes")
        self.play(FadeIn(people), FadeIn(trait), FadeIn(allele), run_time=1.4)
        self.at("At every marker")
        self.play(FadeOut(people), FadeOut(trait), FadeOut(allele), run_time=0.4)
        self.play(Create(P), run_time=1.1)
        self.at("tests whether allele dosage")
        self.play(LaggedStart(*[FadeIn(d, shift=UP*0.2) for d in pts[:20]], lag_ratio=0.05), run_time=2.0)
        self.at("The skyline")
        self.play(LaggedStart(*[FadeIn(d, shift=UP*0.2) for d in pts[20:]], lag_ratio=0.025), run_time=3.0)
        tag = T("simulated, computed", 24, GREY).move_to([2.7, 2.95, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.at("Each point represents")
        cap = caption("Each point is a statistical test — not gene importance.", color=GOLD)
        self.play(FadeIn(cap), pts.animate.set_opacity(0.78), run_time=1.2)
        self.finish()


class S04Threshold(SpokenScene):
    def construct(self):
        P, raw = skyline(False)
        _, adj = skyline(True)
        self.add(P, raw)
        pulse(raw, base=2.0, amp=0.5, speed=1.5)
        self.at("Testing many markers")
        self.play(raw.animate.set_opacity(0.65), run_time=1.5)
        line = P.hline(-math.log10(5e-8), "P = 5 × 10⁻⁸", GOLD)
        self.at("stringent genome")
        self.play(Create(line), run_time=1.3)
        self.at("Ancestry differences")
        red = VGroup(*[raw[i].copy().set_color(RED).scale(1.8) for i in [6, 18, 31, 53]])
        self.play(LaggedStart(*[FadeIn(x) for x in red], lag_ratio=0.2), run_time=1.5)
        slider = boxed_label("PC adjustment", RED, 28).move_to([3.9, 2.95, 0])
        self.at("principal components")
        self.play(FadeIn(slider), Transform(raw, adj), FadeOut(red), run_time=2.2)
        self.at("A threshold controls")
        cap = caption("Threshold ≠ confounding control", color=RED)
        self.play(FadeIn(cap), Indicate(line, color=GOLD), run_time=1.3)
        self.add(scope_tag("simulated"))
        self.finish()


class S05Ld(SpokenScene):
    def construct(self):
        world = ld_world()
        blocks, markers, candidate = world
        self.at("A peak rarely")
        self.play(FadeIn(blocks, shift=RIGHT*0.4), run_time=1.4)
        self.at("Nearby alleles")
        self.play(LaggedStart(*[GrowFromEdge(m, DOWN) for m in markers], lag_ratio=0.12), FadeIn(candidate), run_time=1.8)
        gen = ValueTracker(1)
        count = counter("generation {:.0f} …", gen, at=[4.65, 2.55, 0], size=30, color=GREY)
        self.add(count)
        self.at("for generations")
        self.play(gen.animate.set_value(80), world.animate.shift(RIGHT*0.25), run_time=2.3, rate_func=linear)
        cut = DashedLine([3.15, -1.45, 0], [3.15, 0.25, 0], color=RED, stroke_width=5)
        self.at("recombination separates")
        self.play(Create(cut), blocks[-1].animate.shift(RIGHT*0.65), run_time=1.5)
        ld = T("linkage disequilibrium", 36, BLUE).move_to([0, -2.1, 0])
        self.at("That correlation")
        self.play(FadeOut(count), FadeIn(ld), run_time=0.8)
        self.at("A harmless marker")
        arrow = CurvedArrow(markers[2].get_top()+UP*0.1, candidate.get_top()+UP*0.15,
                            angle=-0.55, color=GOLD, stroke_width=5)
        lab = T("tag", 28, BLUE).next_to(markers[2], LEFT, buff=0.18)
        self.play(Create(arrow), FadeIn(lab), run_time=1.3)
        self.add(scope_tag("inheritance: schematic"))
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world = ld_world()
        blocks, markers, candidate = world
        self.add(world)
        pulse(markers[2], base=9, amp=3, speed=2)
        bob(VGroup(markers, candidate), amp=0.035, speed=1.2)
        self.at("The tallest marker")
        self.play(Indicate(markers[2], color=BLUE), run_time=1.3)
        self.at("Must that tallest")
        q = question_card("Must the tallest point be the causal variant?")
        self.play(FadeIn(q.question), run_time=0.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Must the tallest point be the causal variant?"
    SECONDS = 4.5

    def backdrop(self):
        world = ld_world()
        pulse(world[1][2], base=9, amp=3, speed=2)
        bob(VGroup(world[1], world[2]), amp=0.035, speed=1.2)
        return world


class S08Reveal(SpokenScene):
    def construct(self):
        world = ld_world()
        self.add(world)
        self.at("Now")
        no = T("No.", 54, GOLD).move_to([3.5, 2.75, 0])
        self.play(FadeIn(no, scale=1.2), run_time=0.6)
        self.at("several variants")
        self.play(*[Indicate(m, color=BLUE, scale_factor=1.04) for m in world[1]], run_time=1.8)
        cards = variant_cards()
        self.at("Fine mapping")
        self.play(FadeOut(no), ReplacementTransform(world, cards), run_time=2.0)
        self.at("rank variants")
        self.play(LaggedStart(*[Indicate(c, color=GOLD, scale_factor=1.03) for c in cards[1]], lag_ratio=0.16), run_time=2.0)
        self.at("credible set")
        self.play(Indicate(cards[0], color=GOLD), run_time=1.1)
        self.at("still expresses uncertainty")
        cap = caption("Ranked candidates, not a proven cause", color=GOLD)
        self.play(FadeIn(cap), run_time=0.8)
        self.add(scope_tag("values simulated"))
        self.finish()


class S09Expression(SpokenScene):
    def construct(self):
        mini_cards = VGroup(*[boxed_label(f"variant {c}", BLUE, 24, box=(1.6, 0.58)) for c in "ABC"])
        mini_cards.arrange(RIGHT, buff=0.25).move_to([0, 2.45, 0])
        mini_brace = RoundedRectangle(corner_radius=0.18, width=mini_cards.width+0.35,
                                      height=mini_cards.height+0.3, color=GOLD, stroke_width=3).move_to(mini_cards)
        mini_label = T("credible set", 24, GOLD).next_to(mini_brace, UP, buff=0.12)
        cards = VGroup(mini_brace, mini_cards, mini_label)
        genes = gene_blocks()
        variant = Square(side_length=0.38, color=GOLD, fill_color=GOLD,
                         fill_opacity=0.5).rotate(PI/4).move_to([0, 1.35, 0])
        self.add(cards)
        self.at("ask which gene")
        self.play(FadeIn(variant), FadeIn(genes), run_time=1.4)
        paths = VGroup(*[DashedVMobject(CurvedArrow(variant.get_bottom(), g.get_top(), angle=a,
                                                    color=GOLD, stroke_width=4), num_dashes=12)
                         for g, a in zip(genes, [-0.35, 0, 0.35])])
        self.at("Colocalization tests")
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.2), run_time=1.8)
        trace = VMobject(color=GREEN, stroke_width=6).set_points_as_corners([
            np.array([0.0, -1.05, 0]), np.array([0.35, -0.65, 0]), np.array([0.7, -1.1, 0]),
            np.array([1.05, -0.45, 0]), np.array([1.4, -0.9, 0])])
        trace.next_to(genes[1], DOWN, buff=0.35)
        self.at("expression signals")
        self.play(Create(trace), genes[1].animate.set_color(GREEN), run_time=1.5)
        self.at("neighboring gene")
        lab = T("candidate path", 28, GREEN).next_to(trace, DOWN, buff=0.18)
        self.play(FadeIn(lab), genes[0].animate.set_opacity(0.45), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


def cell(label, x):
    shell = Circle(radius=1.45, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to([x, 0.25, 0])
    nucleus = Circle(radius=0.5, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.12).move_to([x, 0.25, 0])
    lab = T(label, 30, GREY).move_to([x, 2.2, 0])
    return VGroup(shell, nucleus, lab)


class S10Edit(SpokenScene):
    def construct(self):
        left, right = cell("control", -3.2), cell("edited", 0.4)
        self.at("Editing")
        self.play(FadeIn(left), FadeIn(right), run_time=1.4)
        old = Square(0.34, color=BLUE, fill_color=BLUE, fill_opacity=0.5).move_to(right[1])
        new = Square(side_length=0.34, color=GOLD, fill_color=GOLD,
                     fill_opacity=0.55).rotate(PI/4).move_to(right[1])
        self.add(old)
        self.at("changes a candidate allele")
        self.play(ReplacementTransform(old, new), run_time=1.2)
        expr = ValueTracker(0.25)
        phen = ValueTracker(0.30)
        bars = Readout([("expression", lambda: expr.get_value(), "{:4.0%}", GREEN),
                        ("cell readout", lambda: phen.get_value(), "{:4.0%}", GREEN)],
                       at=[4.25, 1.35, 0], widest=[1, 1], title="schematic")
        self.at("gene expression")
        self.play(FadeIn(bars), expr.animate.set_value(0.82), phen.animate.set_value(0.76), run_time=2.4)
        self.at("gains support")
        self.play(Indicate(new, color=GREEN), run_time=1.0)
        boundary = DashedLine([2.55, -2.5, 0], [2.55, 0.2, 0], color=GREY, stroke_width=4)
        human = person(4.9, -1.85, GREY, 1.15)
        note = T("not yet established", 28, GREY).move_to([4.55, -2.75, 0])
        self.at("does not prove")
        self.play(Create(boundary), FadeIn(human), FadeIn(note), run_time=1.4)
        self.finish()


class S11Score(SpokenScene):
    def construct(self):
        tiles = VGroup(*[boxed_label(f"allele {i+1}", BLUE, 26, box=(1.55, 0.68)) for i in range(4)])
        tiles.arrange(RIGHT, buff=0.35).move_to([0, 1.75, 0])
        self.at("Association estimates")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN*0.2) for t in tiles], lag_ratio=0.15), run_time=1.5)
        weights = VGroup(*[T("× weight", 26, GOLD).next_to(t, DOWN, buff=0.18) for t in tiles])
        self.at("weighted by")
        self.play(LaggedStart(*[FadeIn(w) for w in weights], lag_ratio=0.15), run_time=1.4)
        total = boxed_label("polygenic score", BLUE, 34, box=(3.5, 1.0)).move_to([0, -0.35, 0])
        arrows = VGroup(*[Arrow(t.get_bottom(), total.get_top(), buff=0.14, color=GREY, stroke_width=3) for t in tiles])
        self.at("terms are summed")
        self.play(FadeOut(weights), run_time=0.3)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(total), run_time=1.2)
        divider = DashedLine([0, -3.0, 0], [0, -1.0, 0], color=GREY, stroke_width=3)
        discover = crowd_picture(y=-2.75, scale=0.4).scale(0.65).shift(LEFT*3.25)
        test = crowd_picture(y=-2.75, scale=0.4).scale(0.65).shift(RIGHT*3.25)
        dl = T("discovery", 28, GREY).move_to([-3.25, -1.35, 0])
        tl = T("separate test", 28, GOLD).move_to([3.25, -1.35, 0])
        self.at("tested in people")
        self.play(FadeIn(divider), FadeIn(discover), FadeIn(test), FadeIn(dl), FadeIn(tl),
                  total.animate.move_to([3.25, -0.35, 0]).scale(0.78), run_time=2.0)
        self.add(scope_tag("construction: schematic"))
        self.finish()


def population_map(x, boundaries, label):
    base = RoundedRectangle(corner_radius=0.18, width=5.1, height=1.15, color=GREY,
                            stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([x, 0.45, 0])
    cuts = VGroup(*[Line([x-2.55+b, -0.1, 0], [x-2.55+b, 1.0, 0], color=GREY, stroke_width=3)
                    for b in boundaries])
    genes = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.62, height=0.45, color=GREEN,
                                      fill_color=GREEN, fill_opacity=0.3).move_to([x+d, 0.45, 0])
                     for d in [-1.45, 1.3]])
    title = T(label, 28, GREY).move_to([x, 1.55, 0])
    return VGroup(base, cuts, genes, title)


class S12Portability(SpokenScene):
    def construct(self):
        top = population_map(0, [1.4, 3.2], "discovery population")
        bottom = population_map(0, [0.9, 2.1, 4.0], "different population").shift(DOWN*2.85)
        bottom[3].move_to([0, -3.3, 0])
        tags = VGroup(*[Square(0.34, color=BLUE, fill_color=BLUE, fill_opacity=0.6).move_to([x, 0.45, 0])
                        for x in [-1.8, -0.7, 0.6, 1.75]])
        self.add(top, tags)
        self.at("carry those weights")
        self.play(FadeIn(bottom), tags.copy().animate.shift(DOWN*2.85), run_time=2.3)
        lower_tags = tags.copy().shift(DOWN*2.85)
        self.add(lower_tags)
        self.at("same tag markers")
        self.play(lower_tags[0].animate.shift(LEFT*0.55), lower_tags[2].animate.shift(RIGHT*0.65), run_time=1.8)
        accuracy = ValueTracker(0.82)
        gauge = dial(accuracy, center=[4.6, 2.1, 0], radius=1.0, label="prediction", color=RED, size=30)
        self.add(gauge)
        self.at("Prediction can weaken")
        self.play(accuracy.animate.set_value(0.46), run_time=2.2)
        self.at("underlying biology")
        self.play(*[Indicate(g, color=GREEN) for g in list(top[2])+list(bottom[2])], run_time=1.2)
        self.add(scope_tag("maps: schematic"))
        self.finish()


class S13Ethics(SpokenScene):
    def construct(self):
        left = VGroup(*[person(x, -1.65, GREY, 0.62) for x in [-5.35, -4.45, -3.55]])
        right = VGroup(*[person(x, -1.65, GREY, 0.62) for x in [3.55, 4.45, 5.35]])
        tool = RoundedRectangle(corner_radius=0.25, width=2.5, height=3.3, color=RED,
                                stroke_width=4, fill_color=RED, fill_opacity=0.08)
        g1 = Rectangle(width=1.6, height=0.55, color=BLUE, fill_color=BLUE, fill_opacity=0.45).move_to([0, 0.5, 0])
        g2 = Rectangle(width=0.85, height=0.55, color=RED, fill_color=RED, fill_opacity=0.45).move_to([0, -0.5, 0])
        self.at("before clinical use")
        self.play(FadeIn(left), FadeIn(right), FadeIn(tool), FadeIn(g1), FadeIn(g2), run_time=1.5)
        self.at("Training data shape")
        self.play(g1.animate.set_width(2.0), g2.animate.set_width(0.65), run_time=1.4)
        qs = ["Who was studied?", "Who benefits?", "Who controls data?"]
        cards = VGroup(*[boxed_label(q, GOLD, 30) for q in qs]).arrange(DOWN, buff=0.28).move_to([0, 0, 0])
        self.at("Ask who is studied")
        self.play(FadeOut(VGroup(tool, g1, g2)), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.2) for c in cards], lag_ratio=0.25), run_time=1.7)
        bob(left, amp=0.03, speed=1.1)
        bob(right, amp=0.03, speed=1.3)
        lab = T("questions for use", 28, GREY).move_to([0, 2.65, 0])
        self.play(FadeIn(lab), run_time=0.5)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        axes = VGroup(Line([-5.9, -0.5, 0], [-3.8, -0.5, 0], color=GREY, stroke_width=3),
                      Line([-5.9, -0.5, 0], [-5.9, 1.5, 0], color=GREY, stroke_width=3))
        dots = VGroup(*[Dot([-5.75+0.18*i, -0.35+0.10*((i*7)%8), 0], radius=0.045, color=BLUE)
                        for i in range(11)],
                      Dot([-4.35, 1.25, 0], radius=0.09, color=GOLD))
        plot_icon = VGroup(axes, dots)
        block = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.72, height=1.15,
                                          color=BLUE, fill_color=BLUE, fill_opacity=0.15)
                         for _ in range(3)]).arrange(RIGHT, buff=0.08).move_to([-2.35, 0.45, 0])
        mini = VGroup(*[Square(0.42, color=BLUE, fill_color=BLUE, fill_opacity=o)
                        for o in [0.55, 0.35, 0.2]]).arrange(RIGHT, buff=0.22).move_to([0.25, 0.45, 0])
        brace = RoundedRectangle(corner_radius=0.16, width=mini.width+0.35, height=mini.height+0.35,
                                 color=GOLD, stroke_width=3).move_to(mini)
        cards = VGroup(brace, mini)
        shell = Circle(radius=0.82, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([2.85, 0.45, 0])
        nucleus = Circle(radius=0.28, color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.2).move_to(shell)
        cells = VGroup(shell, nucleus)
        human = person(5.4, -0.7, GREY, 1.05)
        stages = VGroup(plot_icon, block, cards, cells, human)
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i+1].get_left(), buff=0.12,
                                color=[BLUE, GOLD, GOLD, GREEN][i], stroke_width=4)
                          for i in range(4)])
        self.at("Association narrows")
        self.play(FadeIn(stages[0]), run_time=1.0)
        self.play(GrowArrow(arrows[0]), FadeIn(block), run_time=1.0)
        self.at("Functional evidence")
        self.play(GrowArrow(arrows[1]), FadeIn(cards), run_time=1.0)
        self.play(GrowArrow(arrows[2]), FadeIn(cells), run_time=1.0)
        self.at("Establishing a cause")
        boundary = DashedLine([4.85, -1.7, 0], [4.85, 2.0, 0], color=GREY, stroke_width=3)
        self.play(GrowArrow(arrows[3]), Create(boundary), FadeIn(human), run_time=1.2)
        cap = caption("Association → candidates → functional evidence → cause", color=GOLD)
        self.play(FadeIn(cap), LaggedStart(*[Indicate(s, scale_factor=1.04) for s in stages], lag_ratio=0.16), run_time=2.2)
        self.finish()


class S15End(EndCard):
    LINE = "A GWAS peak marks an associated region, not a proven cause."
