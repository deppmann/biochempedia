"""Evidence reweights possibilities without changing the person.

COLOR MAP (identical to chapter 1): inheritance routes GOLD; affected
phenotypes RED; compatible possibilities TEAL; excluded/downweighted
possibilities VIOLET; unaffected symbols WHITE.

The carried world is built by ``evidence_world``.  Every continuing scene
uses the same pedigree, filter and probability-bar coordinates.
"""
from bp_parts import *


VIOLET = "#B48EDE"
WHITE = TEXT
BAR_X0, BAR_X1, BAR_Y, BAR_H = 0.25, 6.15, -0.15, 1.42


def breathe_fill(mob, dark="#17353A", light="#2A6970", speed=1.7, opacity=0.78):
    """Gentle, visible motion for a carried subject during spoken holds."""
    mob._breath_t = 0.0
    lo, hi = ManimColor(dark), ManimColor(light)

    def update(m, dt):
        m._breath_t += dt
        mix = 0.5 + 0.5 * np.sin(speed * m._breath_t)
        m.set_fill(interpolate_color(lo, hi, mix), opacity=opacity)
    return mob.add_updater(update)


def person(kind="female", affected=False, side=0.66):
    shape = Square(side_length=side) if kind == "male" else Circle(radius=side / 2)
    shape.set_stroke(WHITE, 4)
    shape.set_fill(RED if affected else BG, 0.94 if affected else 1.0)
    return shape


def small_pedigree(at=(-3.55, -0.1, 0), scale=1.0):
    """The same compact family picture used throughout this chapter."""
    stage = RoundedRectangle(corner_radius=0.24, width=5.5, height=5.35,
                             stroke_color=GREY, stroke_width=2.5,
                             fill_color="#273247", fill_opacity=0.72)
    p1 = person("male").move_to([-0.9, 1.45, 0])
    p2 = person("female", True).move_to([0.9, 1.45, 0])
    c1 = person("female").move_to([-1.25, -1.05, 0])
    c2 = person("male", True).move_to([0.25, -1.05, 0])
    c3 = person("female").move_to([1.55, -1.05, 0])
    lines = VGroup(
        Line([-0.57, 1.45, 0], [0.57, 1.45, 0]),
        Line([0, 1.45, 0], [0, 0.42, 0]),
        Line([-1.25, 0.42, 0], [1.55, 0.42, 0]),
        Line([-1.25, 0.42, 0], [-1.25, -0.72, 0]),
        Line([0.25, 0.42, 0], [0.25, -0.72, 0]),
        Line([1.55, 0.42, 0], [1.55, -0.72, 0]),
    ).set_stroke(WHITE, 4)
    pulse(lines, base=4, amp=1.25, speed=2.7)
    people = VGroup(p1, p2, c1, c2, c3)
    g = VGroup(stage, lines, people).scale(scale).move_to(at)
    g.stage, g.lines, g.people = stage, lines, people
    g.parents, g.children = VGroup(p1, p2), VGroup(c1, c2, c3)
    return g


def genotype_tile(label, width, color=TEAL, height=BAR_H, breathe=False):
    rect = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.24)
    if breathe:
        breathe_fill(rect)
    lab = M(label, 34, color, weight=BOLD).move_to(rect)
    return VGroup(rect, lab)


def probability_bar(labels=("AA", "Aa", "aa"), widths=None, colors=None,
                    x0=BAR_X0, x1=BAR_X1, y=BAR_Y, height=BAR_H, gap=0.10, breathe=False):
    """A fixed-coordinate bar; widths encode schematic probability weights."""
    n = len(labels)
    total = x1 - x0
    widths = widths or [(total - gap * (n - 1)) / n] * n
    colors = colors or [TEAL] * n
    tiles = VGroup(*[genotype_tile(l, w, c, height, breathe=breathe and c == TEAL)
                     for l, w, c in zip(labels, widths, colors)])
    x = x0
    for tile, width in zip(tiles, widths):
        tile.move_to([x + width / 2, y, 0])
        x += width + gap
    bracket = VGroup(
        Line([x0, y + height / 2 + 0.35, 0], [x1, y + height / 2 + 0.35, 0], color=GOLD, stroke_width=3),
        Line([x0, y + height / 2 + 0.22, 0], [x0, y + height / 2 + 0.48, 0], color=GOLD, stroke_width=3),
        Line([x1, y + height / 2 + 0.22, 0], [x1, y + height / 2 + 0.48, 0], color=GOLD, stroke_width=3),
    )
    g = VGroup(bracket, tiles)
    g.bracket, g.tiles = bracket, tiles
    return g


def observation_card(text="unaffected", at=(3.2, 2.35, 0), color=WHITE):
    card = boxed_label(text, color=color, size=30, pad=0.28, fill_opacity=0.13)
    card.move_to(at)
    return card


def evidence_world(bar_breathe=False):
    pedigree = small_pedigree()
    bar = probability_bar(breathe=bar_breathe)
    obs = observation_card()
    g = VGroup(pedigree, bar, obs)
    g.pedigree, g.bar, g.obs = pedigree, bar, obs
    return g


def gold_allele(at, label="A"):
    bar = RoundedRectangle(corner_radius=0.1, width=0.38, height=0.95,
                           stroke_color=GOLD, stroke_width=3,
                           fill_color=GOLD, fill_opacity=0.28)
    return VGroup(bar, M(label, 26, GOLD, weight=BOLD).move_to(bar)).move_to(at)


def allele_marker(at):
    """An unlabelled inherited-copy marker; avoids implying an extra genotype."""
    return RoundedRectangle(corner_radius=0.08, width=0.24, height=0.66,
                            stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=0.45).move_to(at)


def lock_icon(at, scale=1.0):
    c = np.array(at)
    shackle = Arc(radius=0.30 * scale, start_angle=0, angle=PI, color=GOLD,
                  stroke_width=5, arc_center=c + UP * 0.16 * scale)
    body = RoundedRectangle(corner_radius=0.08, width=0.75 * scale, height=0.55 * scale,
                            stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                            fill_opacity=0.22).move_to(c + DOWN * 0.18 * scale)
    return VGroup(shackle, body)


def chromosomes(at=(-3.55, -0.15, 0)):
    bars = VGroup(gold_allele(LEFT * 0.42, "A"), gold_allele(RIGHT * 0.42, "a"))
    bars.scale(1.5).move_to(at)
    return bars


def predict_backdrop():
    bar = probability_bar(labels=("AA", "Aa", "aa", "A?"),
                          colors=(TEAL, TEAL, VIOLET, TEAL), breathe=True)
    obs = observation_card("new evidence", at=(3.2, 2.25, 0), color=VIOLET)
    arrow = Arrow(obs.get_bottom(), bar.tiles[2].get_top() + UP * 0.08, color=VIOLET,
                  stroke_width=5, buff=0.08, max_tip_length_to_length_ratio=0.12)
    q = question_card("Remove it—then what?", y=-2.55, max_w=9.8)
    return VGroup(bar, obs, arrow, q)


class S00Hook(SpokenScene):
    def construct(self):
        world = evidence_world(bar_breathe=True)
        world.pedigree.shift(LEFT * 2.2)
        self.play(world.pedigree.animate.shift(RIGHT * 2.2), run_time=2.2)
        self.at("tested inheritance models")
        self.play(FadeIn(world.bar, shift=LEFT * 0.25), run_time=1.4)
        self.at("How can learning")
        self.play(FadeIn(world.obs, shift=DOWN * 0.2), run_time=0.8)
        self.at("raise their carrier probability")
        carrier = world.bar.tiles[1]
        self.play(Indicate(carrier, color=TEAL, scale_factor=1.05), run_time=1.0)
        self.at("The surprise comes")
        self.play(world.obs.animate.shift(DOWN * 0.55), run_time=1.0)
        self.at("still compatible")
        self.play(Indicate(VGroup(world.bar.tiles[0], world.bar.tiles[1]), color=TEAL,
                           scale_factor=1.04), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Reading Pedigrees: Human Inheritance"
    TITLE = "Evidence Reweights the Possibilities"

    def construct(self):
        bar = probability_bar(labels=("", "", ""))
        filter_band = RoundedRectangle(corner_radius=0.1, width=0.46, height=1.25,
                                       stroke_color=WHITE, stroke_width=3,
                                       fill_color=WHITE, fill_opacity=0.13).move_to([0.7, BAR_Y, 0])
        obs = observation_card(at=(3.2, 2.35, 0))
        self.add(bar, obs, filter_band)
        self.play(filter_band.animate.move_to([3.2, BAR_Y, 0]), FadeOut(obs), run_time=0.55)
        title = fit_text(self.TITLE, max_w=11.8, size=48, font=TITLE_FONT).move_to([0, 2.45, 0])
        self.play(FadeIn(title, shift=UP * 0.12), run_time=0.55)
        small = T(self.TITLE, 28, GOLD).move_to([3.2, 2.55, 0])
        self.play(Transform(title, small), FadeOut(filter_band), run_time=0.55)
        self.play(FadeOut(VGroup(bar, title)), run_time=0.35)
        self.finish()


class S02Possibilities(SpokenScene):
    def construct(self):
        ped = small_pedigree()
        bar = probability_bar(labels=("AA", "Aa", "aa"), colors=(GOLD, GOLD, GOLD))
        self.play(FadeIn(ped), Create(bar.bracket), run_time=1.2)
        self.at("every genotype")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in bar.tiles], lag_ratio=0.2), run_time=1.5)
        for t in bar.tiles: breathe_fill(t[0], speed=1.9, dark="#3A3112", light="#6B5A1E", opacity=0.6)
        self.at("starting weight")
        weights = VGroup(*[M("1/3", 28, GOLD).next_to(t, DOWN, buff=0.22) for t in bar.tiles])
        self.play(LaggedStart(*[FadeIn(w) for w in weights], lag_ratio=0.2), run_time=1.2)
        self.at("transmission rules")
        alleles = VGroup(allele_marker(ped.parents[0].get_top() + UP * 0.32),
                         allele_marker(ped.parents[1].get_top() + UP * 0.32))
        self.play(FadeIn(alleles), run_time=0.7)
        self.at("population assumptions")
        moving = VGroup(*[a.copy() for a in alleles])
        self.add(moving)
        self.play(moving[0].animate.move_to(bar.tiles[0].get_top() + UP * 0.22),
                  moving[1].animate.move_to(bar.tiles[2].get_top() + UP * 0.22), run_time=1.5)
        self.play(FadeOut(moving), run_time=0.3)
        self.at("Write them down")
        note = caption("Starting weights come before phenotype evidence.", color=GOLD)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S03Condition(SpokenScene):
    def construct(self):
        world = evidence_world(bar_breathe=False)
        world.bar.tiles[2][0].set_stroke(VIOLET).set_fill(VIOLET, 0.24)
        world.bar.tiles[2][1].set_color(VIOLET)
        self.add(world.pedigree, world.bar)
        self.at("condition on")
        self.play(FadeIn(world.obs), run_time=0.6)
        self.play(world.obs.animate.move_to([3.2, 1.55, 0]), run_time=1.0)
        self.at("incompatible")
        bad = world.bar.tiles[2]
        self.play(bad.animate.set_color(VIOLET), run_time=0.6)
        self.at("loses its weight")
        self.play(bad.animate.scale(0.01, about_point=bad.get_bottom()), FadeOut(bad), run_time=1.3)
        self.at("Compatible possibilities remain")
        self.play(Indicate(VGroup(world.bar.tiles[0], world.bar.tiles[1]), color=TEAL,
                           scale_factor=1.04), run_time=1.0)
        self.at("not a change")
        self.play(Indicate(world.pedigree.people, color=WHITE, scale_factor=1.03), run_time=1.0)
        self.at("original proportions")
        ratio = M("1 : 1", 34, TEAL).move_to([3.2, -2.0, 0])
        self.play(FadeIn(ratio), run_time=0.8)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        bg = predict_backdrop()
        bar, obs, arrow, q = bg
        self.play(FadeIn(bar), run_time=0.9)
        breathe_fill(bar.tiles[2][0], dark="#2B2347", light="#5A4A9A", speed=1.9, opacity=0.7)
        self.at("new observation")
        self.play(FadeIn(obs), GrowArrow(arrow), run_time=1.0)
        self.at("Which tiles")
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.7)
        self.at("what must happen next")
        self.play(Indicate(bar.bracket, color=GOLD, scale_factor=1.0), run_time=1.0)
        self.at("Watch the total bar")
        pulse(bar.bracket, base=3, amp=1.5, speed=2.4)
        self.play(Indicate(bar.bracket, color=GOLD, scale_factor=1.02), run_time=1.2)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Remove it—then what?"
    SECONDS = 4.5
    CARD = {"y": -2.55, "max_w": 9.8}
    RING_AT = (6.0, -3.1, 0)

    def backdrop(self):
        bg = predict_backdrop()
        return VGroup(*bg[:-1])


class S06Renormalize(SpokenScene):
    def construct(self):
        bar = probability_bar(labels=("AA", "Aa", "aa", "A?"),
                              colors=(TEAL, TEAL, VIOLET, TEAL), breathe=True)
        self.add(bar)
        bad = bar.tiles[2]
        self.at("Remove the incompatible")
        self.play(bad.animate.rotate(PI / 2).scale(0.01), FadeOut(bad), run_time=1.4)
        self.at("stretch the survivors")
        target = probability_bar(labels=("AA", "Aa", "A?"), widths=(1.85, 2.45, 1.40), breathe=True)
        self.play(Transform(bar.tiles[0], target.tiles[0]), Transform(bar.tiles[1], target.tiles[1]),
                  Transform(bar.tiles[3], target.tiles[2]), run_time=2.2)
        self.at("renormalizing")
        lab = caption("renormalize: total probability stays whole", color=GOLD)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.8)
        self.at("divide all the probability")
        self.play(ShowPassingFlash(bar.bracket.copy().set_stroke(TEAL, 7), time_width=0.6), run_time=1.5)
        self.finish()


class S07Rise(SpokenScene):
    def construct(self):
        panels = TwoPanel("before evidence", "after evidence", colors=(GREY, TEAL), top=3.0, bottom=-2.25)
        before = VGroup(genotype_tile("AA", 1.2, TEAL), genotype_tile("Aa", 1.2, TEAL),
                        genotype_tile("aa", 1.2, RED)).arrange(RIGHT, buff=0.10)
        after = VGroup(genotype_tile("AA", 1.45, TEAL), genotype_tile("Aa", 2.25, TEAL, breathe=True)).arrange(RIGHT, buff=0.10)
        panels.put(before, "left"); panels.put(after, "right")
        before.scale(0.84); after.scale(0.84)
        self.play(FadeIn(panels), FadeIn(before), run_time=1.0)
        self.at("occupy more")
        self.play(FadeIn(after), Indicate(after[1], color=TEAL, scale_factor=1.04), run_time=1.1)
        self.at("person is unaffected")
        icon = person("female").scale(1.5).move_to([0, -2.75, 0])
        self.play(FadeIn(icon), run_time=0.7)
        self.at("comparison set")
        removed = VGroup(before[2], after[1])
        self.play(Indicate(removed, color=VIOLET, scale_factor=1.02), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S08NotChange(SpokenScene):
    def construct(self):
        chrom = chromosomes()
        lock = lock_icon([-3.55, 1.35, 0])
        bar1 = probability_bar(labels=("", "", ""), widths=(1.75, 1.75, 2.20), breathe=True)
        self.play(FadeIn(chrom), FadeIn(lock), run_time=0.9)
        self.at("person's DNA")
        self.play(Indicate(chrom, color=GOLD, scale_factor=1.03), run_time=0.9)
        self.at("Evidence changes")
        self.play(FadeIn(bar1), run_time=0.7)
        bar2 = probability_bar(labels=("", ""), widths=(2.15, 3.65), breathe=True)
        self.play(Transform(bar1, bar2), run_time=1.8)
        self.at("not genotypes")
        self.play(Indicate(lock, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.at("uncertainty changed")
        glass = VGroup(Circle(radius=0.48, color=TEAL, stroke_width=5),
                       Line([0.34, -0.34, 0], [0.92, -0.92, 0], color=TEAL, stroke_width=6))
        glass.move_to([1.25, 1.75, 0])
        self.play(FadeIn(glass), glass.animate.move_to([5.15, 1.75, 0]), run_time=1.6)
        self.finish()


class S09Bayes(SpokenScene):
    def construct(self):
        start = probability_bar(labels=("H1", "H2"), widths=(2.85, 2.85), colors=(GOLD, GOLD))
        self.play(FadeIn(start), run_time=0.8)
        self.at("does not eliminate")
        columns = VGroup(*[RoundedRectangle(corner_radius=0.12, width=2.1, height=3.2,
                                            stroke_color=GOLD, stroke_width=3,
                                            fill_color=GOLD, fill_opacity=0.16)
                           for _ in range(2)]).arrange(RIGHT, buff=1.5).move_to([1.4, -0.2, 0])
        labels = VGroup(M("H1", 34, GOLD), M("H2", 34, GOLD))
        for lab, col in zip(labels, columns): lab.next_to(col, DOWN, buff=0.22)
        self.play(ReplacementTransform(start.tiles, columns), FadeIn(labels), FadeOut(start.bracket), run_time=1.4)
        for c in columns: breathe_fill(c, speed=1.9, dark="#3A3112", light="#6B5A1E", opacity=0.6)
        self.at("more likely under")
        evidence = observation_card("evidence", at=(-3.6, 2.1, 0), color=WHITE)
        self.play(FadeIn(evidence), run_time=0.6)
        self.at("Bayes' rule")
        thick = Arrow(evidence.get_right(), columns[0].get_left(), color=TEAL, stroke_width=14, buff=0.12)
        thin = Arrow(evidence.get_right(), columns[1].get_left(), color=TEAL, stroke_width=5, buff=0.12)
        self.play(GrowArrow(thick), GrowArrow(thin), run_time=1.7)
        self.at("without making either")
        self.play(Indicate(columns, color=GOLD, scale_factor=1.02), run_time=1.0)
        self.at("Likelihood measures")
        lab = caption("likelihood — schematic", color=TEAL)
        self.play(FadeIn(lab), run_time=0.7)
        pulse(VGroup(thick, thin), base=8, amp=2, speed=2.0)
        self.finish()


class S10Prior(SpokenScene):
    def construct(self):
        cards = VGroup()
        for x, name in [(-2.0, "H1"), (2.0, "H2")]:
            prior = boxed_label("prior", GOLD, 28, box=(2.2, 0.95)).move_to([x, -0.9, 0])
            like = boxed_label("likelihood", TEAL, 28, box=(2.2, 0.95)).move_to([x, 0.8, 0])
            name_t = M(name, 32, WHITE).move_to([x, 2.2, 0])
            cards.add(VGroup(prior, like, name_t))
        self.play(FadeIn(VGroup(cards[0][0], cards[1][0])), run_time=0.8)
        self.at("prior weight")
        self.play(Indicate(VGroup(cards[0][0], cards[1][0]), color=GOLD, scale_factor=1.04), run_time=0.8)
        self.at("Multiply that weight")
        signs = VGroup(M("×", 38, WHITE).move_to([-2, -0.05, 0]), M("×", 38, WHITE).move_to([2, -0.05, 0]))
        self.play(FadeIn(VGroup(cards[0][1], cards[1][1])), FadeIn(signs), run_time=1.0)
        self.at("better prediction")
        weights = VGroup(genotype_tile("H1", 3.3, TEAL), genotype_tile("H2", 1.8, TEAL))
        weights.arrange(RIGHT, buff=0.8).move_to([0, -2.15, 0])
        self.play(FadeOut(VGroup(cards[0][0], cards[0][1], signs[0])), FadeIn(weights[0]), run_time=1.2)
        self.at("weak prediction")
        self.play(FadeOut(VGroup(cards[1][0], cards[1][1], signs[1])), FadeIn(weights[1]), run_time=1.2)
        self.finish()


class S11Posterior(SpokenScene):
    def construct(self):
        prior = probability_bar(labels=("H1", "H2"), widths=(2.15, 2.15), colors=(GOLD, GOLD),
                                x0=-6.0, x1=-1.5, y=1.8)
        evidence = observation_card("evidence", at=(-0.35, 1.8, 0))
        weighted = VGroup(genotype_tile("H1", 3.3, TEAL), genotype_tile("H2", 1.8, TEAL))
        weighted.arrange(RIGHT, buff=0.3).move_to([4.0, 1.8, 0])
        self.add(prior, evidence, weighted)
        arrows = VGroup(Arrow(prior.get_right(), evidence.get_left(), color=GOLD, buff=0.12),
                        Arrow(evidence.get_right(), weighted.get_left(), color=TEAL, buff=0.12))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.0)
        self.at("renormalize")
        post = probability_bar(labels=("H1", "H2"), widths=(3.75, 1.95),
                               x0=-2.85, x1=2.95, y=-1.35, breathe=True)
        self.play(FadeOut(weighted), FadeIn(post.tiles), Create(post.bracket), run_time=1.7)
        self.at("form the posterior")
        label = T("posterior", 34, TEAL, weight=BOLD).next_to(post, DOWN, buff=0.28)
        self.play(FadeIn(label), run_time=0.7)
        self.at("after accounting")
        self.play(ShowPassingFlash(post.bracket.copy().set_stroke(GOLD, 7), time_width=0.6), run_time=1.2)
        self.at("complete probability bar")
        self.play(Indicate(post, color=TEAL, scale_factor=1.02), run_time=1.0)
        self.finish()


class S12Repeat(SpokenScene):
    def construct(self):
        ped = small_pedigree(at=(0, 0, 0), scale=0.72)
        self.add(ped)
        steps = [("current\nweights", UP * 2.75), ("prediction", RIGHT * 4.55),
                 ("evidence", DOWN * 2.75), ("renormalize", LEFT * 4.55)]
        cards = VGroup(*[boxed_label(t, GOLD if i == 0 else TEAL, 28, pad=0.22).move_to(p)
                         for i, (t, p) in enumerate(steps)])
        self.at("current weights")
        self.play(FadeIn(cards[0]), run_time=0.6)
        self.at("what each hypothesis predicts")
        self.play(FadeIn(cards[1]), run_time=0.6)
        self.at("apply the evidence")
        self.play(FadeIn(cards[2]), run_time=0.6)
        self.at("then renormalize")
        self.play(FadeIn(cards[3]), run_time=0.6)
        paths = VGroup(
            ArcBetweenPoints(cards[0].get_right() + RIGHT * 0.12, cards[1].get_top() + UP * 0.12, angle=-0.55, color=GREY),
            ArcBetweenPoints(cards[1].get_bottom() + DOWN * 0.12, cards[2].get_right() + RIGHT * 0.12, angle=-0.55, color=GREY),
            ArcBetweenPoints(cards[2].get_left() + LEFT * 0.12, cards[3].get_bottom() + DOWN * 0.12, angle=-0.55, color=GREY),
            ArcBetweenPoints(cards[3].get_top() + UP * 0.12, cards[0].get_left() + LEFT * 0.12, angle=-0.55, color=GREY),
        ).set_stroke(width=3)
        marker = Dot(paths[0].get_start(), radius=0.16, color=GOLD)
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.18), FadeIn(marker), run_time=0.8)
        self.at("Each new fact")
        self.play(Succession(*[MoveAlongPath(marker, p, run_time=0.9, rate_func=linear) for p in paths]))
        self.at("method remains")
        self.play(Indicate(cards, color=TEAL, scale_factor=1.02), run_time=1.0)
        self.finish()


class S13Scope(SpokenScene):
    def construct(self):
        bar = probability_bar(y=1.25, breathe=True)
        foundations = VGroup(*[boxed_label(t, GOLD, 26, box=(2.75, 0.72)) for t in
                               ("penetrance", "new mutation", "relationships", "population")])
        foundations.arrange(RIGHT, buff=0.18).move_to([0, -0.55, 0])
        self.play(FadeIn(bar), run_time=0.8)
        self.at("depends on the model")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in foundations], lag_ratio=0.18), run_time=1.8)
        self.at("all shape")
        self.play(Indicate(foundations, color=GOLD, scale_factor=1.02), run_time=1.0)
        self.at("assumption changes")
        removed = foundations[1]
        self.play(removed.animate.shift(DOWN * 1.4).set_opacity(0.25),
                  bar.animate.rotate(0.035), run_time=1.0)
        self.at("recompute")
        self.play(bar.animate.rotate(-0.07), run_time=0.7)
        self.play(bar.animate.rotate(0.035), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S14Apply(SpokenScene):
    def construct(self):
        world = evidence_world(bar_breathe=True)
        worksheet = RoundedRectangle(corner_radius=0.2, width=12.0, height=6.1,
                                     stroke_color=WHITE, stroke_width=3,
                                     fill_color="#182131", fill_opacity=0.68)
        self.play(FadeIn(world), run_time=0.8)
        self.at("calculate exact")
        mini_ped = small_pedigree(at=(-4.55, 1.55, 0), scale=0.38)
        mini_tiles = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.62, height=0.48,
                                              stroke_color=TEAL, stroke_width=2.5,
                                              fill_color=TEAL, fill_opacity=0.25) for _ in range(3)])
        mini_tiles.arrange(RIGHT, buff=0.08).move_to([-4.55, -0.15, 0])
        mini = VGroup(mini_ped, mini_tiles)
        self.play(FadeIn(worksheet), FadeOut(world), FadeIn(mini), run_time=1.4)
        slots = VGroup(*[RoundedRectangle(corner_radius=0.1, width=3.1, height=0.8,
                                         stroke_color=GREY, stroke_width=2.5).move_to([2.0, y, 0])
                         for y in (1.35, 0.05, -1.25)])
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.25), run_time=1.5)
        self.at("Keep the filter")
        keep = VGroup(*[boxed_label(t, c, 28) for t, c in
                        (("filter", WHITE), ("weights", TEAL), ("assumptions", GOLD))])
        keep.arrange(RIGHT, buff=0.45).move_to([0, -2.65, 0])
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.12) for k in keep], lag_ratio=0.2), run_time=1.2)
        self.at("worked examples")
        self.play(Indicate(slots, color=TEAL, scale_factor=1.02), run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "Evidence changes genotype probabilities, not genotypes."
