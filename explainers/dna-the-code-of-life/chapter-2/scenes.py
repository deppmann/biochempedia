"""Chapter 2: DNA amount, built in the visual language of chapter 1.

COLOR MAP (shared by both chapters)
DNA sides BLUE; A/T YELLOW; C/G GREEN; gene TEAL; protein RED;
trait GOLD; counts, chart furniture and axes GREY/WHITE.
"""
from bp_parts import *


DATA = [
    ("E. coli", "bacterium", 4.6, False),
    ("Baker's yeast", "fungus", 12.1, False),
    ("Thale cress", "plant", 157, True),
    ("Fruit fly", "animal", 175, True),
    ("Strawberry", "plant", 240, True),
    ("Rice", "plant", 389, True),
    ("Human", "animal", 3055, False),
    ("Onion", "plant", 16400, True),
]


def dna_ladder(height=4.8, center=ORIGIN, sequence="ATCGTA", rung_w=2.5):
    """The carried chapter-1 block ladder, always rebuilt at the same proportions."""
    n = len(sequence)
    ys = np.linspace(height / 2 - 0.32, -height / 2 + 0.32, n)
    rails = VGroup(
        Line([-rung_w / 2, height / 2, 0], [-rung_w / 2, -height / 2, 0], color=BLUE, stroke_width=10),
        Line([rung_w / 2, height / 2, 0], [rung_w / 2, -height / 2, 0], color=BLUE, stroke_width=10),
    )
    partners = {"A": "T", "T": "A", "C": "G", "G": "C"}
    blocks = VGroup()
    for y, base in zip(ys, sequence):
        partner = partners[base]
        col = YELLOW if base in "AT" else GREEN
        left = RoundedRectangle(width=0.92, height=0.48, corner_radius=0.08,
                                stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.2)
        right = left.copy()
        left.move_to([-0.48, y, 0]); right.move_to([0.48, y, 0])
        lt = T(base, 28, col).move_to(left); rt = T(partner, 28, col).move_to(right)
        # Deliberate: each letter is printed inside its own base block.
        lt.layout_ok = True; rt.layout_ok = True
        blocks.add(VGroup(left, lt, right, rt))
    g = VGroup(rails, blocks).move_to(center)
    g.rails, g.blocks = rails, blocks
    return g


def gene_path(scale=1.0, center=(0, 0.7, 0)):
    """The chapter-1 gene → protein → trait path at one fixed scale and place."""
    gene = chip("gene sequence", TEAL, 28)
    protein = chip("protein", RED, 28)
    trait = chip("trait", GOLD, 28)
    VGroup(gene, protein, trait).arrange(RIGHT, buff=1.05)
    a1 = Arrow(gene.get_right(), protein.get_left(), color=TEXT, stroke_width=4, buff=0.18)
    a2 = Arrow(protein.get_right(), trait.get_left(), color=TEXT, stroke_width=4, buff=0.18)
    g = VGroup(gene, a1, protein, a2, trait).scale(scale).move_to(center)
    return g


def organism_icon(kind, height=1.25):
    """Simple labelled silhouettes—lesson pictures, not biological structures."""
    if kind == "human":
        head = Circle(0.22, color=TEXT, fill_color=TEXT, fill_opacity=0.12)
        body = RoundedRectangle(width=0.72, height=1.05, corner_radius=0.28,
                                color=TEXT, fill_color=TEXT, fill_opacity=0.1).next_to(head, DOWN, buff=0.06)
        g = VGroup(head, body)
    elif kind == "onion":
        bulb = Ellipse(width=1.0, height=1.05, color=GOLD, fill_color=GOLD, fill_opacity=0.13)
        roots = VGroup(*[Line([x, -0.48, 0], [x * 1.4, -0.75, 0], color=GOLD, stroke_width=3)
                         for x in (-0.22, 0, 0.22)])
        shoot = VGroup(ArcBetweenPoints([-0.08, 0.48, 0], [-0.2, 1.0, 0], angle=0.5),
                       ArcBetweenPoints([0.08, 0.48, 0], [0.25, 1.0, 0], angle=-0.5)).set_color(GREEN)
        g = VGroup(bulb, roots, shoot)
    elif kind == "strawberry":
        fruit = Polygon([-0.7, 0.45, 0], [0.7, 0.45, 0], [0, -0.75, 0], color=RED,
                        fill_color=RED, fill_opacity=0.2)
        leaves = VGroup(*[Line([0, 0.42, 0], [x, 0.75, 0], color=GREEN, stroke_width=5)
                          for x in (-0.45, 0, 0.45)])
        g = VGroup(fruit, leaves)
    else:
        g = Circle(0.55, color=GREY, fill_color=GREY, fill_opacity=0.12)
    g.set_height(height)
    return g


def amount_chart(max_value=16400, show_bars=True, rows=DATA, bar_color=WHITE,
                 box=(-2.0, 5.8, -2.35, 2.55), estimates=True):
    """Computed horizontal bars on the one shared linear scale."""
    x0, x1, y0, y1 = box
    axis = Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3)
    ticks = VGroup()
    tick_values = [0, max_value / 2, max_value]
    for value in tick_values:
        x = x0 + (x1 - x0) * value / max_value
        ticks.add(Line([x, y0, 0], [x, y0 - 0.11, 0], color=GREY, stroke_width=3))
        label = f"{value:,.0f}" if value >= 10 else f"{value:g}"
        ticks.add(M(label, 22, GREY).next_to([x, y0 - 0.11, 0], DOWN, buff=0.08))
    title = T("base pairs in one set (millions)", 26, GREY).move_to([(x0 + x1) / 2, y0 - 0.65, 0])
    labels, tracks, bars, badges = VGroup(), VGroup(), VGroup(), VGroup()
    ys = np.linspace(y1, y0 + 0.42, len(rows))
    for (name, _group, value, estimated), y in zip(rows, ys):
        labels.add(fit_text(name, max_w=2.4, size=26, min_size=22, max_lines=1).move_to([x0 - 0.25, y, 0], aligned_edge=RIGHT))
        row_h = 0.56 if len(rows) <= 2 else 0.30
        tracks.add(RoundedRectangle(width=x1 - x0, height=row_h, corner_radius=0.08,
                                    stroke_color=GREY, stroke_width=1.5, fill_color=GREY,
                                    fill_opacity=0.52).move_to([(x0 + x1) / 2, y, 0]))
        end = x0 + (x1 - x0) * min(value, max_value) / max_value
        width = max(0.035, end - x0)
        bar = Rectangle(width=width, height=row_h - 0.02, stroke_width=0, fill_color=bar_color, fill_opacity=0.9)
        bar.move_to([x0 + width / 2, y, 0])
        bars.add(bar)
        if estimates and estimated:
            badges.add(T("est.", 22, GOLD).move_to([x0 - 2.72, y, 0]))
    g = VGroup(axis, ticks, title, labels, tracks)
    if show_bars:
        g.add(bars)
    if estimates:
        g.add(badges)
    g.axis, g.ticks, g.title = axis, ticks, title
    g.labels, g.tracks, g.bars, g.badges = labels, tracks, bars, badges
    return g


def predict_backdrop():
    """Exact frame shared by the predict scene and silent pause."""
    q = question_card("Where should the human bar end compared with onion?", y=3.23, size=30, max_w=11.4)
    rows = [("Human", "animal", 3055, False), ("Onion", "plant", 16400, True)]
    chart = amount_chart(rows=rows, show_bars=False, box=(-1.2, 5.75, -1.55, 1.45), estimates=True)
    chart.title.shift(DOWN * 0.05)
    human = organism_icon("human", 1.05).move_to([-4.9, 1.15, 0])
    onion = organism_icon("onion", 1.05).move_to([-4.9, -0.75, 0])
    scopes = VGroup(T("one set", 25, TEAL).move_to([-3.25, 1.88, 0]),
                    T("one set", 25, TEAL).move_to([-3.25, -1.72, 0]))
    return VGroup(q, chart, human, onion, scopes)


def moving_row_highlight():
    """A soft prediction cursor that travels between the two unrevealed rows."""
    cursor = RoundedRectangle(width=7.15, height=0.72, corner_radius=0.12,
                              stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([2.28, 1.45, 0])
    cursor._t = 0.0
    def travel(mob, dt):
        mob._t += dt
        f = (1 - np.cos(0.55 * mob._t)) / 2
        mob.set_y(1.45 * (1 - f) + (-1.13) * f)
    cursor.add_updater(travel)
    return cursor


class S00Hook(SpokenScene, TitleCard):
    LESSON = "DNA: The Code of Life"
    TITLE = "Does More DNA Mean More Complex?"

    def construct(self):
        path = gene_path(scale=1.03, center=(0, 0.55, 0))
        self.play(FadeIn(path[0], shift=RIGHT * 0.2), run_time=1.0)
        self.at("proteins and traits")
        self.play(LaggedStart(FadeIn(path[1]), FadeIn(path[2]), FadeIn(path[3]), FadeIn(path[4]), lag_ratio=0.22), run_time=2.3)
        ladder = dna_ladder(height=4.1, center=(-3.8, -0.35, 0), sequence="ATCGTA", rung_w=2.0)
        human = organism_icon("human", 1.6).move_to([2.6, -0.4, 0])
        onion = organism_icon("onion", 1.6).move_to([4.7, -0.4, 0])
        self.at("Does more")
        self.play(ReplacementTransform(path, ladder), FadeIn(human), FadeIn(onion), run_time=2.5)
        question = fit_text("Does more DNA mean more complexity?", max_w=11.8, size=38, color=GOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(question, shift=DOWN * 0.15), run_time=1.0)
        chart = amount_chart(show_bars=False, rows=[DATA[-2], DATA[-1]], box=(-1.1, 5.7, -1.65, 1.25), estimates=True)
        self.at("counts from real")
        self.play(ReplacementTransform(ladder, chart), human.animate.move_to([-4.8, 0.75, 0]).scale(0.7),
                  onion.animate.move_to([-4.8, -0.75, 0]).scale(0.7), run_time=3.2)
        bob(human, amp=0.035); bob(onion, amp=0.035, seed=2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "DNA: The Code of Life"
    TITLE = "Does More DNA Mean More Complex?"


class S02Measure(SpokenScene):
    def construct(self):
        ladder = dna_ladder(height=5.2, center=(0, -0.1, 0), sequence="ATCGTAC", rung_w=3.2)
        scope = scope_tag("schematic")
        self.play(FadeIn(ladder.rails), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ladder.blocks], lag_ratio=0.12), run_time=2.4)
        chroms = VGroup(RoundedRectangle(width=1.0, height=2.0, corner_radius=0.35, color=BLUE),
                        RoundedRectangle(width=1.0, height=2.0, corner_radius=0.35, color=BLUE)).arrange(RIGHT, buff=0.45).move_to([4.6, 1.25, 0])
        self.at("full chromosome set")
        self.play(FadeIn(chroms), run_time=1.2)
        set_label = fit_text("one full chromosome set", max_w=3.2, size=28, color=TEAL, max_lines=2).next_to(chroms, DOWN, buff=0.2)
        self.play(FadeIn(set_label), run_time=0.8)
        rung_box = SurroundingRectangle(ladder.blocks[3], color=GOLD, buff=0.08, stroke_width=4)
        self.at("base pair is")
        self.play(Create(rung_box), run_time=1.2)
        bp = T("one base pair", 28, GOLD).move_to([-4.6, 0.0, 0])
        self.play(FadeIn(bp), run_time=0.7)
        count = ValueTracker(0)
        read = counter("{:.0f} rungs counted", count, at=[-4.4, -1.0, 0], size=28, color=TEXT)
        self.add(read, scope)
        self.play(count.animate.set_value(7), run_time=2.0, rate_func=linear)
        seq = chip("sequenced", TEAL, 28).move_to([3.85, -1.2, 0])
        est = chip("estimated", GOLD, 28).move_to([3.85, -2.15, 0])
        self.at("sequenced some")
        self.play(FadeIn(seq), run_time=0.9)
        self.at("estimated others")
        self.play(FadeIn(est), run_time=0.9)
        bar = Rectangle(width=6.2, height=0.48, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).move_to([0, 0, 0])
        self.at("methods count")
        self.play(FadeOut(VGroup(bp, rung_box, read, chroms, set_label, seq, est, scope)), ReplacementTransform(ladder, bar), run_time=2.0)
        no_score = caption("A count is not a complexity score.", color=GOLD)
        self.at("do not score")
        self.play(FadeIn(no_score), run_time=1.0)
        self.finish()


class S03Chart(SpokenScene):
    def construct(self):
        ladders = VGroup(*[dna_ladder(height=1.2, center=(-4.9, y, 0), sequence=s, rung_w=0.8)
                           for y, s in zip((1.7, 0.1, -1.5), ("ATC", "CGA", "TGC"))])
        self.play(LaggedStart(*[FadeIn(x) for x in ladders], lag_ratio=0.25), run_time=1.5)
        nums = VGroup(*[M(v, 28, TEXT).move_to([-2.8, y, 0]) for v, y in zip(("157", "3,055", "16,400"), (1.7, 0.1, -1.5))])
        self.at("become a counter")
        self.play(LaggedStart(*[ReplacementTransform(l, n) for l, n in zip(ladders, nums)], lag_ratio=0.2), run_time=2.0)
        bars = VGroup(*[Rectangle(width=w, height=0.42, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).move_to([-1.7 + w / 2, y, 0])
                        for w, y in zip((0.35, 1.5, 6.2), (1.7, 0.1, -1.5))])
        self.at("then a bar")
        self.play(LaggedStart(*[ReplacementTransform(n, b) for n, b in zip(nums, bars)], lag_ratio=0.2), run_time=2.1)
        chart = amount_chart(show_bars=False)
        note = scope_tag("computed from lesson table")
        self.at("published data")
        self.play(FadeOut(bars), FadeIn(chart), FadeIn(note), run_time=2.0)
        self.at("Every estimated")
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in chart.badges], lag_ratio=0.16), run_time=2.5)
        self.finish()


class S04Groups(SpokenScene):
    def construct(self):
        chart = amount_chart(show_bars=False, estimates=False)
        self.add(chart.axis, chart.ticks, chart.title)
        groups = [("bacterium", BLUE), ("fungus", GREEN), ("plants", TEAL), ("animals", GOLD)]
        icons = VGroup(*[T(name, 25, col) for name, col in groups])
        for icon, y in zip(icons, (2.55, 1.86, 0.47, -0.23)):
            icon.move_to([-5.5, y, 0])
        self.play(FadeIn(icons[0]), FadeIn(icons[1]), run_time=1.5)
        self.at("then plant")
        self.play(FadeIn(icons[2]), FadeIn(icons[3]), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in chart.labels], lag_ratio=0.1), run_time=2.8)
        bracket = Brace(chart.labels, LEFT, color=TEAL)
        bracket_label = fit_text("groups represented in this table", max_w=4.0, size=24, color=TEAL).move_to([-4.4, 3.3, 0])
        self.at("Every group represented")
        self.play(GrowFromCenter(bracket), FadeIn(bracket_label), run_time=1.8)
        claim = fit_text("This claim belongs to this table.", max_w=7.0, size=28, color=TEXT).move_to([1.4, 3.35, 0])
        self.at("careful claim")
        self.play(FadeIn(claim), run_time=1.0)
        boundary = SurroundingRectangle(VGroup(icons, chart.labels), color=GREY, buff=0.12, stroke_width=2)
        limit = T("8 living things", 24, GREY).move_to([4.9, 2.85, 0])
        self.at("small set")
        self.play(Create(boundary), FadeIn(limit), run_time=1.5)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        backdrop = predict_backdrop()
        q, chart, human, onion, scopes = backdrop
        bob(human, amp=0.08, speed=1.4); bob(onion, amp=0.08, speed=1.4, seed=3)
        row_cursor = moving_row_highlight()
        self.add(row_cursor)
        self.play(FadeIn(human), FadeIn(onion), run_time=1.2)
        self.play(FadeIn(chart.labels), FadeIn(chart.tracks), FadeIn(chart.axis), FadeIn(chart.ticks), FadeIn(chart.title), FadeIn(chart.badges), run_time=1.5)
        self.at("where should the human")
        self.play(FadeIn(q), run_time=1.0)
        cursor = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=0.8).scale(0.16).rotate(-PI / 2).move_to([-1.55, 1.45, 0])
        self.at("Make your prediction")
        self.play(FadeIn(cursor), cursor.animate.shift(DOWN * 3.0), run_time=2.4, rate_func=there_and_back)
        self.at("full chromosome set")
        self.play(LaggedStart(*[FadeIn(s) for s in scopes], lag_ratio=0.35), run_time=1.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Where should the human bar end compared with onion?"
    CARD = {"y": 3.23, "size": 30, "max_w": 11.4}
    SECONDS = 4.5

    def backdrop(self):
        g = predict_backdrop()
        return VGroup(*g[1:])

    def construct(self):
        self.add(self.backdrop())
        self.add(question_card(self.QUESTION, y=3.23, size=30, max_w=11.4))
        self.add(moving_row_highlight())
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        backdrop = predict_backdrop()
        q, chart, human, onion, scopes = backdrop
        self.add(q, chart, human, onion, scopes)
        x0, x1 = -1.2, 5.75
        hw, ow = (x1 - x0) * 3055 / 16400, x1 - x0
        human_bar = Rectangle(width=hw, height=0.54, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([x0 + hw / 2, 1.45, 0])
        onion_bar = Rectangle(width=ow, height=0.54, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to([x0 + ow / 2, -1.13, 0])
        human_number = M("3,055", 26, TEXT).next_to(human_bar, UP, buff=0.12).align_to(human_bar, RIGHT)
        onion_number = M("16,400", 26, GOLD).move_to([5.15, -0.62, 0])
        self.play(GrowFromEdge(human_bar, LEFT), FadeIn(human_number), run_time=2.0)
        self.at("onion bar continues")
        self.play(GrowFromEdge(onion_bar, LEFT), FadeIn(onion_number), run_time=3.0)
        division = M("16,400 ÷ 3,055 = 5.37 ≈ 5 times", 28, GOLD).move_to([0, -2.65, 0])
        self.at("division appears")
        self.play(FadeIn(division, shift=UP * 0.1), run_time=1.3)
        self.at("several times")
        self.play(Circumscribe(chart.tracks[1], color=GOLD, buff=0.08),
                  Circumscribe(chart.tracks[0], color=WHITE, buff=0.08), run_time=2.0)
        rule = caption("DNA amount does not rank organism complexity.", color=GOLD)
        self.at("larger D")
        self.play(FadeOut(division), FadeIn(rule), run_time=1.2)
        self.finish()


class S08Order(SpokenScene):
    def construct(self):
        chart = amount_chart(show_bars=False)
        self.add(chart)
        self.at("reveal every bar")
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in chart.bars], lag_ratio=0.12), run_time=3.2)
        self.add(chart.bars)
        fly_i, rice_i, human_i, onion_i = 3, 5, 6, 7
        self.at("Rice extends")
        self.play(Indicate(chart.labels[fly_i], color=GOLD), Indicate(chart.bars[fly_i], color=GOLD), run_time=1.0)
        self.play(Indicate(chart.labels[rice_i], color=GOLD), Indicate(chart.bars[rice_i], color=GOLD), run_time=1.0)
        self.play(Indicate(chart.labels[human_i], color=GOLD), Indicate(chart.bars[human_i], color=GOLD), run_time=0.8)
        self.play(Indicate(chart.labels[onion_i], color=GOLD), Indicate(chart.bars[onion_i], color=GOLD), run_time=0.8)
        zoom_rows = DATA[:6]
        zoom = amount_chart(max_value=500, show_bars=True, rows=zoom_rows, box=(-2.0, 5.8, -2.35, 2.55))
        zoom_tag = scope_tag("zoom: 0–500 million")
        self.at("pattern does not march")
        self.play(FadeOut(chart), FadeIn(zoom), FadeIn(zoom_tag), run_time=2.2)
        self.play(LaggedStart(*[Indicate(b, color=GOLD, scale_factor=1.02) for b in zoom.bars], lag_ratio=0.15), run_time=2.6)
        rule = fit_text("Base count and complexity are different questions.", max_w=10.5, size=30, color=GOLD).move_to([0, 3.35, 0])
        self.at("different questions")
        self.play(FadeOut(zoom_tag), FadeIn(rule), run_time=1.0)
        self.finish()


def information_strip(center=(0, 1.4, 0)):
    blocks = VGroup(*[Rectangle(width=0.58, height=0.75, stroke_color=(TEAL if i in (2, 3, 9) else BLUE),
                                     stroke_width=3, fill_color=(TEAL if i in (2, 3, 9) else BLUE), fill_opacity=0.14)
                      for i in range(14)]).arrange(RIGHT, buff=0.04).move_to(center)
    return blocks


class S09Information(SpokenScene):
    def construct(self):
        bar = Rectangle(width=10.5, height=0.72, fill_color=WHITE, fill_opacity=0.85, stroke_width=0).move_to([0, 1.5, 0])
        self.play(GrowFromEdge(bar, LEFT), run_time=1.5)
        strip = information_strip()
        self.at("not only genes")
        self.play(ReplacementTransform(bar, strip), run_time=2.0)
        gene_bracket = Brace(VGroup(strip[2], strip[3]), DOWN, color=TEAL)
        gene_label = T("a gene", 28, TEAL).next_to(gene_bracket, DOWN, buff=0.12)
        self.play(GrowFromCenter(gene_bracket), FadeIn(gene_label), FadeIn(scope_tag("schematic—not to scale")), run_time=1.2)
        skin = RoundedRectangle(width=5.3, height=2.2, corner_radius=0.3, color=BLUE).move_to([-3.1, -1.3, 0])
        muscle = RoundedRectangle(width=5.3, height=2.2, corner_radius=0.3, color=RED).move_to([3.1, -1.3, 0])
        labels = VGroup(T("skin cell", 28, BLUE).move_to([-3.1, -0.65, 0]), T("muscle cell", 28, RED).move_to([3.1, -0.65, 0]))
        strips = VGroup(information_strip((-3.1, -1.45, 0)).scale(0.43), information_strip((3.1, -1.45, 0)).scale(0.43))
        self.at("which genes a cell uses")
        self.play(FadeIn(skin), FadeIn(muscle), FadeIn(labels), FadeIn(strips), run_time=2.0)
        glows = VGroup(SurroundingRectangle(strips[0][2:4], color=TEAL, buff=0.05),
                       SurroundingRectangle(strips[1][8:10], color=TEAL, buff=0.05))
        self.play(Create(glows), run_time=1.5)
        self.at("Sequence and gene use")
        self.play(glows[0].animate.set_stroke(width=8), glows[1].animate.set_stroke(width=8), run_time=2.0, rate_func=there_and_back)
        summary = caption("Length cannot replace sequence and gene-use information.", color=GOLD)
        self.at("total length")
        self.play(FadeOut(VGroup(skin, muscle, labels, strips, glows)), FadeIn(summary), run_time=1.4)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        path = gene_path(scale=0.8, center=(0, 2.55, 0))
        chart = amount_chart(show_bars=True, box=(-0.5, 5.7, -2.45, 0.6))
        self.play(FadeIn(path), run_time=1.4)
        self.at("both halves meet")
        self.play(FadeIn(chart), run_time=1.5)
        rule = fit_text("DNA sequence helps shape traits; DNA amount does not rank complexity.", max_w=12.0, size=32, color=GOLD).move_to([0, 1.2, 0])
        self.at("sequence helps shape")
        self.play(FadeIn(rule), run_time=1.2)
        self.at("amount does not rank")
        self.play(Indicate(chart, color=GOLD, scale_factor=1.01), run_time=1.6)
        scope = chip("amount = base pairs in one chromosome set", TEAL, 25).move_to([0, -3.4, 0])
        self.at("rule has scope")
        self.play(FadeOut(chart.title), FadeIn(scope), run_time=1.2)
        sun = VGroup(Circle(0.24, color=GOLD), *[Line(0.34 * np.array([np.cos(a), np.sin(a), 0]),
                                                     0.55 * np.array([np.cos(a), np.sin(a), 0]), color=GOLD)
                                                for a in np.linspace(0, TAU, 8, endpoint=False)]).move_to([5.8, 2.2, 0])
        self.at("genes proteins")
        self.play(LaggedStart(*[Indicate(m, color=TEAL if i == 0 else RED if i == 2 else GOLD) for i, m in enumerate((path[0], path[2], path[4]))], lag_ratio=0.25), run_time=2.6)
        self.at("depend on the surroundings")
        self.play(FadeIn(sun), path[4].animate.shift(RIGHT * 0.15), run_time=1.4)
        self.finish()


class S11Limits(SpokenScene):
    def construct(self):
        chart = amount_chart(show_bars=True, box=(-2.0, 3.7, -2.35, 2.55))
        chart.shift(LEFT * 1.0)
        self.add(chart)
        cursor = RoundedRectangle(width=5.0, height=0.42, corner_radius=0.08,
                                  stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([-0.3, 2.55, 0])
        cursor._t = 0.0
        def scan(mob, dt):
            mob._t += dt
            mob.set_y(0.31 + 2.24 * np.sin(0.55 * mob._t))
        cursor.add_updater(scan)
        self.add(cursor)
        tags = VGroup()
        def tag(text, y, color=GREY):
            return chip(text, color, 22).move_to([5.0, y, 0])
        row_y = np.linspace(2.55, -1.93, 8)
        lab = tag("lab study", row_y[0] + 0.29)
        sample = tag("one strain/sample", row_y[1] + 0.11)
        estimated = tag("estimated", row_y[2], GOLD)
        human = tag("22 chr. + X; rounded", row_y[6] + 0.05, TEAL).shift(LEFT * 0.25)
        onion = tag("earlier estimate", row_y[7] - 0.12, GOLD)
        self.at("published lab studies")
        self.play(FadeIn(lab, shift=LEFT * 0.15), run_time=1.2); tags.add(lab)
        self.at("one strain or sample")
        self.play(FadeIn(sample, shift=LEFT * 0.15), run_time=1.2); tags.add(sample)
        self.at("values are estimates")
        self.play(FadeIn(estimated, shift=LEFT * 0.15), run_time=1.2); tags.add(estimated)
        self.at("human row")
        self.play(FadeIn(human, shift=LEFT * 0.15), run_time=1.2); tags.add(human)
        self.at("onion uses")
        self.play(FadeIn(onion, shift=LEFT * 0.15), run_time=1.2); tags.add(onion)
        for t, idx in zip(tags, (0, 1, 2, 6, 7)):
            self.play(FadeIn(Dot([2.85, row_y[idx], 0], radius=0.055,
                                 color=t[1].get_color())), run_time=0.25)
        self.at("limits attached")
        self.play(LaggedStart(*[Indicate(t, scale_factor=1.02) for t in tags], lag_ratio=0.12), run_time=2.0)
        self.finish()


class S13Answer(SpokenScene):
    def construct(self):
        strawberry = organism_icon("strawberry", 2.0).move_to([-4.7, 0.9, 0])
        person = organism_icon("human", 2.0).move_to([4.7, 0.9, 0])
        ladder = dna_ladder(height=4.7, center=(0, 0.55, 0), sequence="ATCGTA", rung_w=2.4)
        self.play(FadeIn(strawberry), FadeIn(person), FadeIn(ladder), FadeIn(scope_tag("schematic")), run_time=2.0)
        self.at("answer is not")
        cross = Cross(ladder, stroke_color=GOLD, stroke_width=6)
        cross.layout_ok = True
        self.play(Create(cross), run_time=1.4)
        changed = dna_ladder(height=4.7, center=(0, 0.55, 0), sequence="CGTACG", rung_w=2.4)
        self.at("Different base orders")
        self.play(FadeOut(cross), Transform(ladder, changed), run_time=2.2)
        genes = VGroup(SurroundingRectangle(ladder.blocks[1:3], color=TEAL, buff=0.08),
                       SurroundingRectangle(ladder.blocks[4:6], color=TEAL, buff=0.08))
        self.at("different gene use")
        self.play(LaggedStart(*[Create(g) for g in genes], lag_ratio=0.3), run_time=1.8)
        proteins = VGroup(chip("protein A", RED, 26).move_to([-3.6, -1.65, 0]),
                          chip("protein B", RED, 26).move_to([3.6, -1.65, 0]))
        self.play(FadeIn(proteins[0], shift=DOWN * 0.15), FadeIn(proteins[1], shift=DOWN * 0.15), run_time=1.8)
        bars = VGroup(Rectangle(width=2.5, height=0.34, fill_color=WHITE, fill_opacity=0.9, stroke_width=0),
                      Rectangle(width=5.2, height=0.34, fill_color=WHITE, fill_opacity=0.9, stroke_width=0)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -2.65, 0])
        schematic = T("amount bars: schematic", 24, GREY).next_to(bars, LEFT, buff=0.25)
        self.at("amount does not rank")
        self.play(FadeOut(VGroup(strawberry, person, ladder, genes, proteins)), FadeIn(bars), FadeIn(schematic), run_time=1.6)
        ideas = VGroup(T("base order + gene use → different proteins", 30, TEAL),
                       T("DNA amount ≠ complexity rank", 32, GOLD)).arrange(DOWN, buff=0.45).move_to([0, 0.5, 0])
        self.play(FadeIn(ideas), run_time=1.3)
        self.finish()


class S14End(EndCard):
    LINE = "DNA sequence helps shape traits; DNA amount does not rank organism complexity."
