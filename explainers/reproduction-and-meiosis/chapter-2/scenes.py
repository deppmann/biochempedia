"""How chromosome pairs make different mixes — chapter 2.

COLOR MAP (kept for the whole two-chapter lesson)
  BLUE  = first member of each chromosome pair
  GOLD  = second member of each chromosome pair
  GREEN = sex cells
  TEXT  = fertilized cells and body cells
  GREY  = neutral cell outlines and guides

The opening is deliberately the scripted hook rather than a title card.  The title is the
following two-second scene, as required by this chapter's scene order and visual notes.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


PAIR_BLUE = BLUE
PAIR_GOLD = GOLD
SEX_GREEN = GREEN
BAR_W = 0.28
PAIR_HEIGHTS = (1.55, 1.16, 0.78)
PAIR_YS = (1.55, 0.0, -1.45)


def chrom_bar(height, color, at=ORIGIN, width=BAR_W):
    """One whole chromosome in the same rounded-bar language as chapter 1."""
    return RoundedRectangle(
        corner_radius=width / 2,
        width=width,
        height=height,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    ).move_to(at)


def pair_group(y, center_x=0, separation=0.72, height=1.1):
    blue = chrom_bar(height, PAIR_BLUE, [center_x - separation / 2, y, 0])
    gold = chrom_bar(height, PAIR_GOLD, [center_x + separation / 2, y, 0])
    return VGroup(blue, gold)


def parent_cell(center=(0, 0, 0), width=7.2, height=6.1, rocking=False):
    """The carried parent-cell picture. Every continuing scene calls this builder."""
    c = np.array(center, dtype=float)
    outline = Ellipse(
        width=width,
        height=height,
        stroke_color=GREY,
        stroke_width=4,
        fill_color=GREY,
        fill_opacity=0.20,
    ).move_to(c)
    pairs = VGroup(*[
        pair_group(c[1] + y, c[0], height=h)
        for y, h in zip(PAIR_YS, PAIR_HEIGHTS)
    ])
    g = VGroup(outline, pairs)
    g.outline, g.pairs = outline, pairs
    if rocking:
        for i, p in enumerate(pairs):
            p._rock_t = i * 0.8
            base = p.get_center().copy()
            def rock(m, dt, base=base):
                m._rock_t += dt
                m.rotate(0.18 * np.sin(1.2 * m._rock_t) * dt, about_point=base)
            p.add_updater(rock)
    return g


def sex_cell(at, pattern=(), radius=1.25, bar_scale=0.72):
    """A green sex cell with one chromosome from each represented pair."""
    at = np.array(at, dtype=float)
    ring = Circle(
        radius=radius,
        stroke_color=SEX_GREEN,
        stroke_width=5,
        fill_color=SEX_GREEN,
        fill_opacity=0.20,
    ).move_to(at)
    bars = VGroup()
    if pattern:
        xs = np.linspace(-0.55, 0.55, len(pattern))
        for x, col, h in zip(xs, pattern, PAIR_HEIGHTS):
            bars.add(chrom_bar(h * bar_scale, col, at + RIGHT * x, width=BAR_W * bar_scale))
    g = VGroup(ring, bars)
    g.ring, g.bars = ring, bars
    return g


def hook_world():
    parent = parent_cell((0, 0, 0), width=6.9, height=6.0)
    orbits = VGroup(*[sex_cell(p, radius=0.55) for p in [(-4.9, 1.8, 0), (4.9, 1.8, 0), (-4.9, -1.8, 0), (4.9, -1.8, 0)]])
    return VGroup(parent, orbits)


def prediction_world(rocking=True):
    old = sex_cell((-4.65, 0.25, 0), (PAIR_BLUE, PAIR_GOLD, PAIR_BLUE), radius=1.5, bar_scale=0.9)
    parent = parent_cell((3.0, 0.25, 0), width=5.6, height=5.5, rocking=rocking)
    parent.scale(0.82, about_point=np.array([3.0, 0.25, 0]))
    qmark = T("?", 82, GOLD, weight=BOLD).move_to([-0.7, 0.25, 0])
    return VGroup(old, parent, qmark)


def pattern_strip(pattern, at, width=2.7):
    segs = VGroup(*[
        Rectangle(width=width / len(pattern), height=0.28, stroke_width=0, fill_color=c, fill_opacity=1)
        for c in pattern
    ]).arrange(RIGHT, buff=0).move_to(at)
    return segs


def simple_person(at, color=TEXT):
    """A simple body-cell descendant silhouette, not an anatomical claim."""
    at = np.array(at, dtype=float)
    head = Circle(radius=0.43, color=color, stroke_width=4, fill_color=color, fill_opacity=0.12).move_to(at + UP * 1.15)
    body = RoundedRectangle(corner_radius=0.28, width=1.45, height=2.0, color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.10).move_to(at + DOWN * 0.35)
    return VGroup(head, body)


class S00Question(SpokenScene):
    def construct(self):
        world = hook_world()
        parent, orbiters = world
        self.at("The first film")
        self.play(FadeIn(parent.outline), LaggedStart(*[FadeIn(p) for p in parent.pairs], lag_ratio=0.14), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(c, scale=0.75) for c in orbiters], lag_ratio=0.12), run_time=1.2)
        for i, c in enumerate(orbiters):
            bob(c, amp=0.07, speed=0.8 + i * 0.08, seed=i)
        self.at("why are those halves different")
        q = fit_text("Why are the halves different?", max_w=6.1, size=36, color=GOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.8)
        self.at("Return to the blue")
        ring = Circle(radius=0.9, color=TEAL, stroke_width=6).move_to(parent.pairs[0])
        self.play(Create(ring), run_time=0.5)
        self.play(ring.animate.move_to(parent.pairs[1]), run_time=0.8)
        self.at("follow which member")
        self.play(ring.animate.move_to(parent.pairs[2]), run_time=0.8)
        self.play(Indicate(orbiters, color=SEX_GREEN, scale_factor=1.05), run_time=1.2)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = hook_world().set_opacity(0.10)
        # Deliberate title overlay on the carried cell picture; recorded in film_author.json.
        world.layout_ok = True
        for i, p in enumerate(world[0].pairs):
            bob(p, amp=0.025, speed=1.0, seed=i)
        title = fit_text("How Chromosome Pairs Make Different Mixes", max_w=11.4, size=48,
                         color=TEXT, font=TITLE_FONT).move_to([0, 0.2, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.35)
        self.add(world)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.1)
        self.wait(0.45)
        self.play(FadeOut(VGroup(title, rule)), run_time=0.35)
        self.finish()


class S02Alleles(SpokenScene):
    def construct(self):
        zoom_cell = Ellipse(width=8.2, height=6.3, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.20)
        blue = chrom_bar(4.6, PAIR_BLUE, [-1.1, 0, 0], width=0.5)
        gold = chrom_bar(4.6, PAIR_GOLD, [1.1, 0, 0], width=0.5)
        gene_y = 0.55
        self.at("A gene can have")
        self.play(FadeIn(zoom_cell), FadeIn(blue), FadeIn(gold), run_time=1.0)
        loci = VGroup(Dot([-1.1, gene_y, 0], radius=0.17, color=TEXT), Dot([1.1, gene_y, 0], radius=0.17, color=TEXT))
        self.play(FadeIn(loci, scale=1.6), run_time=0.7)
        tracker = RoundedRectangle(corner_radius=0.14, width=3.25, height=0.34, color=TEAL,
                                   fill_color=TEAL, fill_opacity=0.55, stroke_width=5).move_to([0, gene_y, 0])
        tracker.layout_ok = True  # deliberate scanning highlight across the chromosome bars
        tracker._t = 0.0
        def scan(m, dt):
            m._t += dt
            m.move_to([0, gene_y + 1.55 * np.sin(1.45 * m._t), 0])
        tracker.add_updater(scan)
        self.add(tracker)
        self.at("Each version is an allele")
        allele = T("alleles", 32, TEXT).move_to([0, 3.43, 0])
        self.play(FadeIn(allele), run_time=0.55)
        self.at("Put capital B")
        B = chip("B", PAIR_BLUE, size=34).move_to([-2.0, gene_y, 0])
        self.play(FadeIn(B), B.animate.next_to(blue, LEFT, buff=0.25), run_time=0.75)
        self.at("lowercase b")
        b = chip("b", PAIR_GOLD, size=34).move_to([2.0, gene_y, 0])
        self.play(FadeIn(b), b.animate.next_to(gold, RIGHT, buff=0.25), run_time=0.75)
        self.at("receives only one member")
        left_cell = sex_cell((-4.7, -0.15, 0), radius=1.35)
        right_cell = sex_cell((4.7, -0.15, 0), radius=1.35)
        tracker.clear_updaters()
        self.play(FadeOut(VGroup(allele, tracker, zoom_cell)), FadeIn(left_cell.ring), FadeIn(right_cell.ring), run_time=0.7)
        b1 = chrom_bar(2.05, PAIR_BLUE, left_cell.get_center(), width=0.34)
        b2 = chrom_bar(2.05, PAIR_GOLD, right_cell.get_center(), width=0.34)
        self.play(TransformFromCopy(blue, b1), TransformFromCopy(gold, b2), run_time=1.15)
        for i, routed in enumerate((b1, b2)):
            routed._t = i * PI
            base = routed.get_center().copy()
            def route_motion(m, dt, base=base):
                m._t += dt
                m.move_to(base + RIGHT * 0.38 * np.sin(2.8 * m._t))
            routed.add_updater(route_motion)
        self.at("equal chance")
        p1 = M("50%", 38, PAIR_BLUE).move_to([-4.7, -2.0, 0])
        p2 = M("50%", 38, PAIR_GOLD).move_to([4.7, -2.0, 0])
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.65)
        self.at("Across many sex cells")
        route1 = CurvedArrow([-0.8, -2.1, 0], [4.2, 0.3, 0], angle=0.28, color=PAIR_BLUE, stroke_width=4)
        route2 = CurvedArrow([0.8, -2.1, 0], [-4.2, 0.3, 0], angle=0.28, color=PAIR_GOLD, stroke_width=4)
        b1.clear_updaters()
        b2.clear_updaters()
        self.play(FadeOut(VGroup(b1, b2)), Create(route1), Create(route2), run_time=0.9)
        self.play(TransformFromCopy(blue, chrom_bar(2.05, PAIR_BLUE, right_cell.get_center(), width=0.34)),
                  TransformFromCopy(gold, chrom_bar(2.05, PAIR_GOLD, left_cell.get_center(), width=0.34)), run_time=1.0)
        self.play(FadeOut(VGroup(route1, route2, p1, p2)), run_time=0.5)
        self.finish()


class S03Independent(SpokenScene):
    def construct(self):
        parent = parent_cell((0, 0.15, 0), width=8.0, height=6.2)
        self.at("Now restore three pairs")
        self.play(FadeIn(parent.outline), LaggedStart(*[FadeIn(p) for p in parent.pairs], lag_ratio=0.15), run_time=1.2)
        selector = RoundedRectangle(corner_radius=0.22, width=2.0, height=1.75, color=TEAL,
                                    fill_color=TEAL, fill_opacity=0.10, stroke_width=7).move_to(parent.pairs[0])
        self.play(FadeIn(selector), selector.animate.move_to(parent.pairs[1]), run_time=1.0)
        selector._t = 0.0
        def scan_pairs(m, dt):
            m._t += dt
            m.move_to([0, 0.15 + 1.6 * np.sin(1.35 * m._t), 0])
        selector.add_updater(scan_pairs)
        lanes = VGroup(DashedLine([-2.2, 2.4, 0], [-2.2, -2.4, 0], color=GREY),
                       DashedLine([2.2, 2.4, 0], [2.2, -2.4, 0], color=GREY)).set_opacity(0.5)
        self.at("each pair sorts by chance")
        self.play(FadeIn(lanes), run_time=0.5)
        self.play(Rotate(parent.pairs[0], 0.18), Rotate(parent.pairs[1], -0.22), Rotate(parent.pairs[2], 0.14), run_time=1.25)
        self.at("independently of the other pairs")
        self.play(Rotate(parent.pairs[0], -0.33), run_time=0.7)
        self.play(Rotate(parent.pairs[1], 0.42), run_time=0.7)
        self.play(Rotate(parent.pairs[2], -0.28), run_time=0.7)
        left_targets = [np.array([-2.2, y + 0.15, 0]) for y in PAIR_YS]
        right_targets = [np.array([2.2, y + 0.15, 0]) for y in PAIR_YS]
        self.at("blue member may move left")
        selector.clear_updaters()
        self.play(FadeOut(selector), parent.pairs[0][0].animate.move_to(left_targets[0]),
                  parent.pairs[0][1].animate.move_to(right_targets[0]), run_time=1.0)
        self.at("gold member may move left")
        self.play(parent.pairs[1][1].animate.move_to(left_targets[1]), parent.pairs[1][0].animate.move_to(right_targets[1]), run_time=1.0)
        self.at("Each choice changes")
        self.play(parent.pairs[2][0].animate.move_to(left_targets[2]), parent.pairs[2][1].animate.move_to(right_targets[2]), run_time=1.0)
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), Indicate(VGroup(*[p[0] if i != 1 else p[1] for i, p in enumerate(parent.pairs)]), color=SEX_GREEN), run_time=1.0)
        self.finish()


class S04Predict(SpokenScene):
    QUESTION = "Must the next sex cell match?"
    def construct(self):
        old = sex_cell((-4.65, 0.25, 0), (PAIR_BLUE, PAIR_GOLD, PAIR_BLUE), radius=1.5, bar_scale=0.9)
        self.at("One green sex cell")
        self.play(FadeIn(old.ring), LaggedStart(*[FadeIn(b) for b in old.bars], lag_ratio=0.18), run_time=1.2)
        parent = parent_cell((3.0, 0.25, 0), width=5.6, height=5.5, rocking=True)
        parent.scale(0.82, about_point=np.array([3.0, 0.25, 0]))
        self.at("Reset the parent cell")
        self.play(FadeIn(parent), run_time=1.0)
        self.at("Must the next sex cell match")
        qm = T("?", 82, GOLD, weight=BOLD).move_to([-0.7, 0.25, 0])
        self.play(FadeIn(qm, scale=0.45), run_time=0.7)
        self.at("Predict what")
        q = question_card(self.QUESTION, y=-3.12, size=32)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.7)
        self.play(Indicate(old, color=SEX_GREEN), Indicate(parent.pairs, color=GOLD), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Must the next sex cell match?"
    OPTIONS = ()
    SECONDS = 4.5
    def backdrop(self):
        return prediction_world(rocking=True)


class S06Reveal(SpokenScene):
    def construct(self):
        old = sex_cell((-3.0, 0.25, 0), (PAIR_BLUE, PAIR_GOLD, PAIR_BLUE), radius=1.55, bar_scale=0.9)
        new = sex_cell((3.0, 0.25, 0), radius=1.55)
        self.add(old)
        self.at("The next cell need not match")
        self.play(FadeIn(new.ring), run_time=0.75)
        self.at("gold blue gold pattern")
        incoming = sex_cell((3.0, 0.25, 0), (PAIR_GOLD, PAIR_BLUE, PAIR_GOLD), radius=1.55, bar_scale=0.9).bars
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in incoming], lag_ratio=0.2), run_time=1.15)
        selectors = VGroup(
            RoundedRectangle(corner_radius=0.12, width=0.62, height=1.75, color=TEAL, stroke_width=7).move_to(old.bars[1]),
            RoundedRectangle(corner_radius=0.12, width=0.62, height=1.75, color=TEAL, stroke_width=7).move_to(incoming[1]),
        )
        for i, sel in enumerate(selectors):
            sel._t = i * 1.4
            base = sel.get_center().copy()
            def follow_members(m, dt, base=base):
                m._t += dt
                m.move_to(base + RIGHT * 0.52 * np.sin(1.7 * m._t))
            sel.add_updater(follow_members)
        self.play(FadeIn(selectors), run_time=0.35)
        self.at("Each pair still contributes one chromosome")
        brackets = VGroup(Brace(old.bars, DOWN, color=GREY), Brace(incoming, DOWN, color=GREY))
        self.play(GrowFromCenter(brackets[0]), GrowFromCenter(brackets[1]), run_time=0.7)
        self.at("every sex cell has half")
        same = T("same chromosome number", 30, TEXT).move_to([0, 2.75, 0])
        top_brace = Brace(VGroup(old, new), UP, color=TEXT)
        self.play(GrowFromCenter(top_brace), FadeIn(same), run_time=0.75)
        self.at("What changes is which member")
        s1 = pattern_strip((PAIR_BLUE, PAIR_GOLD, PAIR_BLUE), [-3.0, -2.05, 0])
        s2 = pattern_strip((PAIR_GOLD, PAIR_BLUE, PAIR_GOLD), [3.0, -2.05, 0])
        mix = T("different mix", 32, GOLD).move_to([0, -2.75, 0])
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.65)
        self.play(FadeIn(mix), run_time=0.55)
        self.at("Different eggs and sperm")
        self.play(Indicate(VGroup(s1, s2), color=SEX_GREEN, scale_factor=1.05), run_time=1.4)
        self.finish()


class S07Chance(SpokenScene):
    def construct(self):
        # A fixed, reproducible Bernoulli(0.5) model. The early run is uneven; cumulative shares converge.
        rng = np.random.RandomState(23)
        trials = rng.randint(0, 2, 80)
        trials[:8] = np.array([0, 0, 1, 0, 0, 1, 0, 1])
        n = ValueTracker(1)
        frame = RoundedRectangle(corner_radius=0.18, width=10.6, height=5.4, color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.22).move_to([0, 0.2, 0])
        base_y, scale = -2.0, 0.055
        def counts():
            k = max(1, min(len(trials), int(round(n.get_value()))))
            blue_n = int(np.sum(trials[:k] == 0))
            return blue_n, k - blue_n
        def bars():
            a, b = counts()
            return VGroup(
                Rectangle(width=2.2, height=max(0.08, a * scale), stroke_width=0, fill_color=PAIR_BLUE, fill_opacity=1).move_to([-2.0, base_y + a * scale / 2, 0]),
                Rectangle(width=2.2, height=max(0.08, b * scale), stroke_width=0, fill_color=PAIR_GOLD, fill_opacity=1).move_to([2.0, base_y + b * scale / 2, 0]),
            )
        live_bars = always_redraw(bars)
        labels = VGroup(T("B", 34, PAIR_BLUE, weight=BOLD).move_to([-2, -2.92, 0]),
                        T("b", 34, PAIR_GOLD, weight=BOLD).move_to([2, -2.92, 0]))
        run_label = T("trials accumulate", 28, TEXT).move_to([4.45, 2.35, 0])
        model = T("computed chance model", 28, GREY).move_to([0, 3.15, 0])
        self.at("Chance does not promise")
        self.play(FadeIn(frame), FadeIn(labels), FadeIn(model), FadeIn(live_bars), FadeIn(run_label), run_time=1.0)
        self.at("A short run")
        self.play(n.animate.set_value(8), run_time=2.6, rate_func=linear)
        token_row = VGroup(*[
            VGroup(Circle(radius=0.16, color=SEX_GREEN, stroke_width=3),
                   Dot(radius=0.07, color=PAIR_BLUE if v == 0 else PAIR_GOLD))
            for v in trials[:8]
        ]).arrange(RIGHT, buff=0.16).move_to([0, 2.35, 0])
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in token_row], lag_ratio=0.08), run_time=0.9)
        self.at("Across many model sex cells")
        self.play(FadeOut(token_row), n.animate.set_value(80), run_time=4.3, rate_func=linear)
        self.at("approach equal shares")
        half = DashedLine([-3.4, 0.2, 0], [3.4, 0.2, 0], color=TEXT, stroke_width=3).set_opacity(0.65)
        self.play(Create(half), run_time=0.65)
        self.at("An allele is not stronger")
        equal = T("frequency ≠ strength", 34, TEXT).move_to([0, 2.35, 0])
        self.play(FadeIn(equal), Indicate(labels, color=TEXT), run_time=1.0)
        self.play(n.animate.set_value(72), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S07bModelLimit(SpokenScene):
    def construct(self):
        blue = chrom_bar(4.2, PAIR_BLUE, [-1.1, 0.2, 0], width=0.55)
        gold = chrom_bar(4.2, PAIR_GOLD, [1.1, 0.2, 0], width=0.55)
        self.at("Blue and gold mark")
        self.play(FadeIn(blue), FadeIn(gold), run_time=0.9)
        member = T("colour tracks pair member", 32, TEXT).move_to([0, 3.0, 0])
        self.play(FadeIn(member), run_time=0.65)
        self.at("not stronger and weaker")
        eq = T("equal size • equal brightness", 32, GREY).move_to([0, -2.55, 0])
        self.play(FadeIn(eq), Indicate(VGroup(blue, gold), color=TEXT, scale_factor=1.02), run_time=1.0)
        self.at("This model follows whole chromosomes")
        today_frame = RoundedRectangle(corner_radius=0.2, width=5.4, height=5.8, color=TEXT, stroke_width=3).move_to([-3.5, 0, 0])
        today = T("today: whole bars", 30, TEXT).move_to([-3.5, 3.15, 0])
        pair = VGroup(blue, gold, member, eq)
        self.play(pair.animate.scale(0.72).move_to([-3.5, 0, 0]), Create(today_frame), FadeIn(today), run_time=1.1)
        self.at("you will add crossing over")
        later = T("later: crossing over", 30, GOLD).move_to([3.5, 3.15, 0])
        rb = chrom_bar(4.0, PAIR_BLUE, [3.0, 0, 0], width=0.6)
        rg = chrom_bar(4.0, PAIR_GOLD, [4.0, 0, 0], width=0.6)
        self.play(FadeIn(later), FadeIn(rb), FadeIn(rg), run_time=0.9)
        self.at("exchange matching pieces")
        blue_piece = Rectangle(width=0.6, height=1.05, stroke_width=0, fill_color=PAIR_BLUE, fill_opacity=1).move_to([3.0, 0.45, 0])
        gold_piece = Rectangle(width=0.6, height=1.05, stroke_width=0, fill_color=PAIR_GOLD, fill_opacity=1).move_to([4.0, 0.45, 0])
        self.add(blue_piece, gold_piece)
        self.play(blue_piece.animate.move_to([4.0, 0.45, 0]), gold_piece.animate.move_to([3.0, 0.45, 0]), run_time=1.3)
        self.at("creating still more")
        combo = VGroup(pattern_strip((PAIR_BLUE, PAIR_GOLD), [3.5, -2.5, 0], width=2.5),
                       T("more combinations", 28, GOLD).move_to([3.5, -3.0, 0]))
        self.play(FadeIn(combo), run_time=0.8)
        self.at("does not change today's sorting rule")
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), Indicate(today_frame, color=TEXT, scale_factor=1.01), run_time=1.2)
        self.finish()


class S08Mitosis(SpokenScene):
    def construct(self):
        panels = TwoPanel("mitosis: copy", "meiosis: sort", colors=(TEXT, SEX_GREEN), top=3.2, bottom=-2.55)
        panels.left_frame.set_fill(TEXT, opacity=0.11)
        panels.right_frame.set_fill(SEX_GREEN, opacity=0.14)
        source = parent_cell((0, 0, 0), width=3.2, height=3.3)
        source.scale(0.48)
        source.move_to([0, 0.3, 0])
        self.at("Mitosis does a different job")
        self.play(FadeIn(panels), FadeIn(source), run_time=1.0)
        self.at("keeps the chromosome number")
        body1 = parent_cell((-4.7, 0.1, 0), width=2.3, height=2.6); body1.scale(0.42, about_point=np.array([-4.7, 0.1, 0]))
        body2 = parent_cell((-2.0, 0.1, 0), width=2.3, height=2.6); body2.scale(0.42, about_point=np.array([-2.0, 0.1, 0]))
        self.play(TransformFromCopy(source, body1), TransformFromCopy(source, body2), run_time=1.4)
        match = T("matching body cells", 28, TEXT).move_to([-3.35, -1.65, 0])
        self.play(FadeIn(match), run_time=0.55)
        self.at("Meiosis makes sex cells")
        sex1 = sex_cell((2.1, 0.15, 0), (PAIR_BLUE, PAIR_GOLD, PAIR_BLUE), radius=0.9, bar_scale=0.52)
        sex2 = sex_cell((4.9, 0.15, 0), (PAIR_GOLD, PAIR_BLUE, PAIR_GOLD), radius=0.9, bar_scale=0.52)
        self.play(TransformFromCopy(source, sex1), TransformFromCopy(source, sex2), run_time=1.4)
        half = T("half • different mixes", 28, SEX_GREEN).move_to([3.5, -1.65, 0])
        self.play(FadeIn(half), run_time=0.55)
        self.at("Most asexual reproduction")
        asexual = T("asexual", 30, TEXT).move_to([-3.35, -2.95, 0])
        self.play(FadeIn(asexual), Indicate(VGroup(body1, body2), color=TEXT), run_time=0.9)
        self.at("Sexual reproduction uses")
        sexual = T("sexual", 30, SEX_GREEN).move_to([3.5, -2.95, 0])
        self.play(FadeIn(sexual), Indicate(VGroup(sex1, sex2), color=SEX_GREEN), run_time=1.0)
        self.finish()


class S09Answer(SpokenScene):
    def construct(self):
        sibling_panels = VGroup(
            RoundedRectangle(corner_radius=0.24, width=6.1, height=6.15, color=GREY, stroke_width=3,
                             fill_color=TEXT, fill_opacity=0.11).move_to([-3.35, 0.15, 0]),
            RoundedRectangle(corner_radius=0.24, width=6.1, height=6.15, color=GREY, stroke_width=3,
                             fill_color=TEXT, fill_opacity=0.11).move_to([3.35, 0.15, 0]),
        )
        for i, panel in enumerate(sibling_panels):
            panel._t = i * PI
            base = panel.get_center().copy()
            def breathe(m, dt, base=base):
                m._t += dt
                m.move_to(base + RIGHT * 0.22 * np.sin(2.4 * m._t))
            panel.add_updater(breathe)
        egg1 = sex_cell((-5.2, 1.7, 0), (PAIR_BLUE, PAIR_GOLD, PAIR_BLUE), radius=0.9, bar_scale=0.5)
        sperm1 = sex_cell((-2.8, 1.7, 0), (PAIR_GOLD, PAIR_BLUE, PAIR_GOLD), radius=0.9, bar_scale=0.5)
        egg2 = sex_cell((2.8, 1.7, 0), (PAIR_GOLD, PAIR_GOLD, PAIR_BLUE), radius=0.9, bar_scale=0.5)
        sperm2 = sex_cell((5.2, 1.7, 0), (PAIR_BLUE, PAIR_BLUE, PAIR_GOLD), radius=0.9, bar_scale=0.5)
        self.at("Now the sibling puzzle")
        self.play(FadeIn(sibling_panels), LaggedStart(*[FadeIn(x) for x in (egg1, sperm1, egg2, sperm2)], lag_ratio=0.12), run_time=1.2)
        self.at("Each child begins")
        z1 = Circle(radius=1.0, color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.20).move_to([-4.0, -0.55, 0])
        z2 = Circle(radius=1.0, color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.20).move_to([4.0, -0.55, 0])
        self.play(ReplacementTransform(VGroup(egg1, sperm1), z1), ReplacementTransform(VGroup(egg2, sperm2), z2), run_time=1.4)
        self.at("different allele mixes")
        p1 = pattern_strip((PAIR_BLUE, PAIR_GOLD, PAIR_BLUE, PAIR_GOLD), [-4, -0.55, 0], width=1.45)
        p2 = pattern_strip((PAIR_GOLD, PAIR_BLUE, PAIR_GOLD, PAIR_BLUE), [4, -0.55, 0], width=1.45)
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.7)
        self.at("alleles stay separate")
        self.play(p1.animate.set_y(-0.25), p2.animate.set_y(-0.25), run_time=0.8)
        self.at("Sexual reproduction")
        kid1, kid2 = simple_person((-4, -0.3, 0)), simple_person((4, -0.3, 0))
        sibling_panels.clear_updaters()
        self.play(FadeOut(sibling_panels), ReplacementTransform(z1, kid1), ReplacementTransform(z2, kid2),
                  p1.animate.move_to([-4, -0.45, 0]), p2.animate.move_to([4, -0.45, 0]), run_time=1.25)
        bob(kid1, amp=0.20, speed=3.0, seed=0)
        bob(kid2, amp=0.20, speed=3.0, seed=2)
        self.at("Meiosis has chromosome number")  # transcript's rendering of "halves"
        rule1 = T("meiosis: half + mixes", 30, SEX_GREEN).move_to([0, -2.45, 0])
        self.play(FadeIn(rule1), run_time=0.65)
        self.at("Fertilization restores pairs")
        rule2 = T("fertilization: pairs restored", 30, TEXT).move_to([0, -3.05, 0])
        self.play(FadeIn(rule2), Indicate(VGroup(p1, p2), color=GOLD), run_time=1.0)
        self.finish()


class S10End(EndCard):
    LINE = "Sexual reproduction:\nmeiosis halves chromosome number and makes mixes;\nfertilization restores pairs."
