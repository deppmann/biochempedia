"""From Transcript to Message — RNA processing.

COLOR MAP
  BLUE = retained exons and the processed message
  RED  = introns that leave
  GOLD = added end marks and the reacting free exon edge
  TEAL = recognition signals and spliceosome guides
  GREY = DNA, polymerase, helpers, and neutral structure
"""
from bp_parts import *  # noqa: F401,F403


Y_RNA = 0.45
EXON_X = (-4.85, -1.65, 1.65, 4.85)


class LivingScene:
    """Faint ambient drift keeps narrated holds alive without adding a biological claim."""
    def setup(self):
        super().setup()
        motes = VGroup()
        for i in range(24):
            x = -6.15 + (i % 12) * 1.1
            y = -3.35 if i < 12 else 0.0
            if x > 5.1 and y > 2.5:
                x -= 1.0
            d = Dot([x, y, 0], radius=0.29, color=TEXT).set_opacity(0.12)
            d.v = np.array([0.34 + 0.035 * (i % 4), 0.0, 0])

            def drift(mob, dt):
                mob.shift(mob.v * dt)
                if mob.get_x() > 6.5:
                    mob.shift(LEFT * 13.0)
                if mob.get_y() > 3.5:
                    mob.shift(DOWN * 7.0)
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)


def wave(a, b, y=Y_RNA, amp=0.22, color=RED, width=8):
    """A schematic intron ribbon, computed as a sine wave between two endpoints."""
    xs = np.linspace(a, b, 60)
    pts = [np.array([x, y + amp * np.sin(2 * PI * (x - a) / (b - a)), 0]) for x in xs]
    m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
    m.set_points_as_corners(pts)
    return m


def whole_transcript(with_polymerase=True, with_ends=False):
    """The carried whole-transcript picture; all whole-RNA scenes call this builder."""
    exons = VGroup(*[
        RoundedRectangle(width=1.55, height=1.15, corner_radius=0.12,
                         stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                         fill_opacity=0.42).move_to([x, Y_RNA, 0])
        for x in EXON_X
    ])
    introns = VGroup(
        wave(-4.08, -2.42), wave(-0.88, 0.88), wave(2.42, 4.08)
    )
    g = VGroup(introns, exons)
    g.exons, g.introns = exons, introns
    if with_polymerase:
        pol = boxed_label("RNA polymerase", GREY, size=26, pad=0.18).move_to([4.85, 1.55, 0])
        guide = Line([-6.0, 1.98, 0], [5.65, 1.98, 0], color=GREY, stroke_width=3).set_opacity(0.55)
        g.add(guide, pol)
        g.polymerase, g.guide = pol, guide
    if with_ends:
        cap = boxed_label("m7G cap", GOLD, size=26, pad=0.18).move_to([-5.75, 1.55, 0])
        tail = VGroup(*[
            RoundedRectangle(width=0.34, height=0.58, corner_radius=0.08,
                             stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD,
                             fill_opacity=0.34).move_to([5.78 + 0.36 * i, Y_RNA, 0])
            for i in range(3)
        ])
        g.add(cap, tail)
        g.cap, g.tail = cap, tail
    return g


def splice_world(lariat=False, joined=False):
    """The carried one-intron picture used unchanged through the splice sequence."""
    left = RoundedRectangle(width=2.15, height=1.35, corner_radius=0.12,
                            stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                            fill_opacity=0.42).move_to([-4.65 if not joined else -1.08, 0.65, 0])
    right = RoundedRectangle(width=2.15, height=1.35, corner_radius=0.12,
                             stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                             fill_opacity=0.42).move_to([4.65 if not joined else 1.08, 0.65, 0])
    if joined:
        seam = Line([0, 0.0, 0], [0, 1.3, 0], color=TEXT, stroke_width=2).set_opacity(0.6)
        g = VGroup(left, right, seam)
        g.left, g.right, g.seam = left, right, seam
        return g
    if not lariat:
        intron = wave(-3.55, 3.55, y=0.65, amp=0.32, width=9)
    else:
        loop = Circle(radius=1.2, color=RED, stroke_width=9).move_to([0.65, 0.72, 0])
        tail = CubicBezier([1.72, 1.27, 0], [2.4, 1.72, 0], [2.7, 0.76, 0], [3.55, 0.65, 0])
        tail.set_stroke(RED, 9)
        intron = VGroup(loop, tail)
    g = VGroup(intron, left, right)
    g.intron, g.left, g.right = intron, left, right
    g.exons, g.introns = VGroup(left, right), VGroup(intron)
    return g


def finished_message(y=0.5):
    """The carried processed message used by both closing spoken scenes."""
    widths = (1.35, 1.6, 1.45, 1.75)
    xs, x = [], -3.55
    for w in widths:
        xs.append(x + w / 2)
        x += w
    exons = VGroup(*[
        RoundedRectangle(width=w, height=1.8, corner_radius=0.09,
                         stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                         fill_opacity=0.48).move_to([cx, y, 0])
        for w, cx in zip(widths, xs)
    ])
    cap = boxed_label("m7G cap", GOLD, size=26, pad=0.18).next_to(exons, LEFT, buff=0.16)
    tail = VGroup(*[
        RoundedRectangle(width=0.38, height=0.62, corner_radius=0.08,
                         stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD,
                         fill_opacity=0.36)
        for _ in range(5)
    ]).arrange(RIGHT, buff=0.08).next_to(exons, RIGHT, buff=0.16)
    g = VGroup(cap, exons, tail)
    g.cap, g.exons, g.tail = cap, exons, tail
    return g


def add_breathing(world):
    """Slow, visible ambient motion without moving any landmark sideways."""
    targets = getattr(world, "exons", VGroup())
    for i, mob in enumerate(targets):
        bob(mob, amp=0.11, speed=1.45, seed=i)
    for i, mob in enumerate(getattr(world, "introns", VGroup())):
        pulse(mob, base=8.0, amp=1.1, speed=1.8 + i * 0.15)
    return world


class S00Hook(LivingScene, SpokenScene):
    def construct(self):
        world = whole_transcript()
        # Show the puzzle before naming the transcript.
        message = DashedVMobject(RoundedRectangle(width=6.6, height=1.05, corner_radius=0.12,
                                                   color=BLUE, stroke_width=3)).move_to([0, -2.0, 0])
        qs = VGroup(*[T("?", 46, GOLD, weight=BOLD).move_to([x, -2.0, 0]) for x in (-2.2, 0, 2.2)])
        self.play(FadeIn(message), LaggedStart(*[FadeIn(q, scale=1.25) for q in qs], lag_ratio=0.18), run_time=0.8)
        self.at("Watch one new transcript")
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.18) for m in world.introns],
                              *[FadeIn(m, shift=LEFT * 0.18) for m in world.exons], lag_ratio=0.08), run_time=1.2)
        self.play(FadeIn(world.guide), FadeIn(world.polymerase), run_time=0.5)
        add_breathing(world)
        self.at("Some parts will stay")
        self.play(LaggedStart(*[Indicate(e, color=BLUE, scale_factor=1.04) for e in world.exons], lag_ratio=0.14), run_time=1.1)
        self.at("some will leave")
        self.play(LaggedStart(*[Indicate(i, color=RED, scale_factor=1.03) for i in world.introns], lag_ratio=0.18), run_time=0.9)
        self.at("two new end marks")
        marks = VGroup(Dot([-6.0, Y_RNA, 0], radius=0.17, color=GOLD),
                       Dot([6.0, Y_RNA, 0], radius=0.17, color=GOLD))
        self.play(FadeIn(marks, scale=0.3), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(LivingScene, NarratedScene):
    def construct(self):
        world = add_breathing(whole_transcript())
        title_text = T("From Transcript to Message", 52, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        title_back = BackgroundRectangle(title_text, color=BG, fill_opacity=0.96, buff=0.16, stroke_width=0)
        title = VGroup(title_back, title_text)
        rule = Line([-1.4, 2.5, 0], [1.4, 2.5, 0], color=GOLD, stroke_width=4)
        self.add(world, scope_tag("schematic"))
        self.play(FadeIn(title_back), Write(title_text), GrowFromCenter(rule), run_time=0.75)
        self.wait(0.65)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.6)
        self.finish()


class S02Parts(LivingScene, SpokenScene):
    def construct(self):
        world = add_breathing(whole_transcript())
        self.add(world, scope_tag("schematic"))
        bracket = BraceBetweenPoints([-5.65, 2.75, 0], [5.65, 2.75, 0], UP, color=TEXT)
        lab = T("primary transcript", 32, TEXT).next_to(bracket, UP, buff=0.12)
        self.play(GrowFromCenter(bracket), FadeIn(lab, shift=DOWN * 0.12), run_time=0.8)
        self.at("Blue exons")
        exon_lab = T("exon • retained", 30, BLUE).move_to([-4.85, -1.0, 0])
        self.play(Indicate(world.exons[0], color=BLUE, scale_factor=1.12), run_time=0.55)
        self.play(FadeIn(exon_lab), run_time=0.45)
        self.at("Red introns")
        intron_lab = T("intron • removed", 30, RED).move_to([-2.45, -1.75, 0])
        self.play(Indicate(world.introns[0], color=RED, scale_factor=1.12), run_time=0.55)
        self.play(FadeIn(intron_lab), run_time=0.45)
        self.at("Each decision")
        self.play(world.polymerase.animate.shift(RIGHT * 0.35), run_time=0.8)
        self.finish()


class S03Cap(LivingScene, SpokenScene):
    def construct(self):
        world = add_breathing(whole_transcript())
        self.add(world, scope_tag("schematic"))
        self.play(world.polymerase.animate.shift(RIGHT * 0.3), run_time=0.7)
        self.at("A methylated guanosine cap")
        cap = boxed_label("m7G cap", GOLD, size=28).move_to([-5.75, 1.55, 0])
        self.play(FadeIn(cap, scale=0.75), run_time=0.8)
        self.at("triphosphate bridge")
        dots = VGroup(*[Dot([-5.58, 1.08 - 0.18 * i, 0], radius=0.075, color=GOLD) for i in range(3)])
        bridge_text = T("triphosphate bridge", 28, GOLD).move_to([-3.8, -1.15, 0])
        bridge_back = BackgroundRectangle(bridge_text, color=BG, fill_opacity=0.96, buff=0.12, stroke_width=0)
        bridge_lab = VGroup(bridge_back, bridge_text)
        self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in dots], lag_ratio=0.2), FadeIn(bridge_lab), run_time=0.8)
        self.at("That bridge leaves")
        self.play(FadeOut(bridge_lab), run_time=0.25)
        wedge = Triangle(color=GREY, fill_color=GREY, fill_opacity=0.35).scale(0.45).rotate(-PI / 2).move_to([-4.0, -2.05, 0])
        exolab = T("exonuclease", 28, GREY).next_to(wedge, DOWN, buff=0.16)
        self.play(FadeIn(VGroup(wedge, exolab)), run_time=0.45)
        self.play(wedge.animate.move_to([-5.35, 0.3, 0]), run_time=0.65)
        self.play(wedge.animate.shift(RIGHT * 1.0 + DOWN * 0.7).rotate(PI), run_time=0.6)
        self.at("recruits proteins")
        export = T("export", 28, TEAL).move_to([-1.7, -1.55, 0])
        translation = T("translation", 28, TEAL).move_to([1.55, -1.55, 0])
        arrows = VGroup(Arrow(cap.get_bottom(), export.get_left(), buff=0.15, color=TEAL),
                        Arrow(cap.get_bottom(), translation.get_left(), buff=0.15, color=TEAL))
        self.play(Create(arrows), FadeIn(export), FadeIn(translation), run_time=1.0)
        self.finish()


class S04Tail(LivingScene, SpokenScene):
    def construct(self):
        world = whole_transcript(with_polymerase=False)
        self.add(world, scope_tag("schematic"))
        dna = Line([-6.0, -1.55, 0], [6.2, -1.55, 0], color=GREY, stroke_width=4).set_opacity(0.7)
        dna_text = T("DNA guide continues", 28, GREY).move_to([-2.8, -2.05, 0])
        dna_back = BackgroundRectangle(dna_text, color=BG, fill_opacity=0.96, buff=0.12, stroke_width=0)
        dna_lab = VGroup(dna_back, dna_text)
        self.add(dna, dna_lab)
        self.at("RNA signal guides a cut")
        flag = VGroup(Line([3.15, 1.25, 0], [3.15, 2.25, 0], color=TEAL, stroke_width=4),
                      T("RNA signal", 28, TEAL).move_to([4.25, 2.25, 0]))
        cut = DashedLine([4.0, -0.35, 0], [4.0, 1.3, 0], color=TEAL, stroke_width=4)
        self.play(FadeIn(flag, shift=UP * 0.15), Create(cut), run_time=0.8)
        scrap = world.exons[3]
        self.play(scrap.animate.shift(RIGHT * 1.0 + DOWN * 1.0).set_opacity(0.25), run_time=0.75)
        self.at("Polya polymerase")
        pol = boxed_label("poly(A) polymerase", GREY, size=26).move_to([3.6, 3.0, 0])
        self.play(FadeIn(pol, shift=DOWN * 0.2), run_time=0.55)
        tail = VGroup(*[RoundedRectangle(width=0.38, height=0.58, corner_radius=0.08,
                                        stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD,
                                        fill_opacity=0.34).move_to([4.18 + 0.42 * i, Y_RNA, 0]) for i in range(5)])
        self.play(LaggedStart(*[GrowFromCenter(a) for a in tail], lag_ratio=0.15), run_time=1.2)
        tail_lab = T("poly(A) tail", 30, GOLD).move_to([5.0, 1.58, 0])
        self.play(FadeIn(tail_lab), run_time=0.4)
        self.at("rather than copied")
        gap = T("no DNA template beneath tail", 28, GOLD).move_to([3.7, -2.45, 0])
        self.play(FadeIn(gap), Indicate(dna, color=GREY, scale_factor=1.0), run_time=0.75)
        self.at("binding proteins")
        binders = VGroup(*[RoundedRectangle(width=0.34, height=0.28, corner_radius=0.06,
                                           color=GOLD, fill_color=GOLD, fill_opacity=0.55).move_to([4.18 + 0.84 * i, 0.95, 0]) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in binders], lag_ratio=0.2), run_time=0.8)
        self.finish()


class S05Sites(LivingScene, SpokenScene):
    def construct(self):
        world = add_breathing(splice_world())
        self.play(FadeIn(world, scale=0.82), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.at("its ends usually carry")
        gu = chip("GU", TEAL, size=30).move_to([-3.55, 1.92, 0])
        ag = chip("AG", TEAL, size=30).move_to([3.55, 1.92, 0])
        self.play(FadeIn(gu, scale=0.85), FadeIn(ag, scale=0.85), run_time=0.8)
        self.at("A branch point")
        branch = Dot([1.25, 0.65, 0], radius=0.18, color=TEAL)
        branch_lab = T("branch A", 30, TEAL).move_to([1.25, 2.76, 0])
        stem = Line(branch, branch_lab.get_bottom() + DOWN * 0.1, color=TEAL, stroke_width=2.5)
        self.play(FadeIn(branch, scale=0.2), Create(stem), FadeIn(branch_lab), run_time=0.8)
        self.at("pyrimidine rich stretch")
        pyr = VGroup(*[Dot([2.0 + 0.28 * i, 0.28, 0], radius=0.07, color=TEAL) for i in range(4)])
        pyr_lab = T("pyrimidine-rich", 28, TEAL).move_to([2.4, -0.75, 0])
        self.play(LaggedStart(*[FadeIn(p) for p in pyr], lag_ratio=0.15), FadeIn(pyr_lab), run_time=0.8)
        pulse(world.intron, base=9, amp=1.2, speed=1.7)
        self.finish()


class S06Guides(LivingScene, SpokenScene):
    def construct(self):
        world = splice_world()
        gu = chip("GU", TEAL, size=28).move_to([-3.55, 1.75, 0])
        ag = chip("AG", TEAL, size=28).move_to([3.55, 1.75, 0])
        branch = VGroup(Dot([1.25, 0.65, 0], radius=0.18, color=TEAL), T("branch A", 28, TEAL).move_to([1.25, 2.6, 0]))
        self.add(world, gu, ag, branch, scope_tag("schematic"))
        pulse(world.intron, base=9, amp=1.1, speed=1.6)
        self.at("U1 recognizes")
        u1 = boxed_label("U1", TEAL, size=30).move_to([-5.0, -1.4, 0])
        self.play(FadeIn(u1), run_time=0.35)
        self.play(u1.animate.move_to([-3.55, -0.72, 0]), run_time=0.75)
        self.at("U2 holds")
        u2 = boxed_label("U2", TEAL, size=30).move_to([0.0, -1.5, 0])
        self.play(FadeIn(u2), run_time=0.35)
        self.play(u2.animate.move_to([0.55, 0.0, 0]), branch[0].animate.shift(UP * 0.55), run_time=0.8)
        self.at("Other particles join")
        others = VGroup(*[boxed_label(n, TEXT, size=26, pad=0.16) for n in ("U4", "U5", "U6")]).arrange(RIGHT, buff=0.35).move_to([0, -2.0, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.18) for x in others], lag_ratio=0.15), run_time=0.8)
        self.at("rearrange the assembly")
        self.play(others[0].animate.move_to([-1.4, -0.8, 0]), others[1].animate.move_to([0.0, -1.25, 0]),
                  others[2].animate.move_to([1.6, -0.75, 0]), run_time=1.1)
        self.at("form a spliceosome")
        ring = Ellipse(width=10.5, height=5.0, color=TEAL, stroke_width=4).move_to([0, 0.2, 0])
        lab = T("spliceosome", 32, TEAL).move_to([0, 3.0, 0])
        self.play(FadeOut(gu), FadeOut(ag), FadeOut(branch), run_time=0.3)
        self.play(Create(ring), FadeIn(lab), run_time=0.9)
        self.finish()


class S07Predict(LivingScene, SpokenScene):
    def construct(self):
        before = splice_world()
        branch = Dot([1.25, 0.65, 0], radius=0.18, color=TEAL)
        self.add(before, branch, scope_tag("schematic"))
        self.at("branch adenosine attacks")
        attack = CurvedArrow([1.25, 0.85, 0], [-3.5, 1.0, 0], angle=PI / 3, color=TEAL, stroke_width=5)
        self.play(Create(attack), branch.animate.move_to([-3.35, 1.05, 0]), run_time=1.1)
        self.at("upstream exon comes free")
        self.play(before.left.animate.shift(LEFT * 0.45), FadeOut(attack), run_time=0.7)
        self.at("intron bends into a lariat")
        after = splice_world(lariat=True)
        after.left.shift(LEFT * 0.45)
        self.play(ReplacementTransform(before.intron, after.intron), run_time=1.1)
        edge = Line(after.left.get_right() + UP * 0.55, after.left.get_right() + DOWN * 0.55,
                    color=GOLD, stroke_width=9)
        pulse(edge, base=8, amp=3, speed=2.2)
        self.at("free edge glowing gold")
        self.play(FadeIn(edge), run_time=0.45)
        self.at("Which exposed end")
        q = question_card("Which end joins the exons?", y=-2.75, size=34)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.65)
        self.finish()


def lariat_pause_backdrop():
    world = splice_world(lariat=True)
    world.left.shift(LEFT * 0.45)
    edge = Line(world.left.get_right() + UP * 0.55, world.left.get_right() + DOWN * 0.55,
                color=GOLD, stroke_width=9)
    pulse(edge, base=8, amp=3, speed=2.2)
    bob(world.intron, amp=0.035, speed=1.2)
    return VGroup(world, edge, scope_tag("schematic"))


class S08Pause(LivingScene, PredictPause):
    QUESTION = "Which end joins the exons?"
    SECONDS = 4.5
    CARD = {"y": -2.75, "size": 34}
    RING_AT = (5.9, -2.75, 0)

    def backdrop(self):
        return lariat_pause_backdrop()


class S09Join(LivingScene, SpokenScene):
    def construct(self):
        world = splice_world(lariat=True)
        world.left.shift(LEFT * 0.45)
        edge = Line(world.left.get_right() + UP * 0.55, world.left.get_right() + DOWN * 0.55,
                    color=GOLD, stroke_width=9)
        self.add(world, edge, scope_tag("schematic"))
        self.play(FadeOut(edge), run_time=0.25)
        self.at("attacks the second splice site")
        attack = CurvedArrow(world.left.get_right(), world.right.get_left(), angle=-PI / 3,
                             color=GOLD, stroke_width=5)
        self.play(Create(attack), run_time=1.0)
        self.at("Both exons join")
        joined = splice_world(joined=True)
        self.play(FadeOut(attack), Transform(world.left, joined.left), Transform(world.right, joined.right),
                  world.intron.animate.shift(DOWN * 2.2 + RIGHT * 2.8).set_opacity(0.2), run_time=1.2)
        ledger = Ledger([("step 1", "bond swapped", TEAL), ("step 2", "bond swapped", GOLD)],
                        top_left=(-5.6, -1.45), title="two attacks", key_w=1.7, width=5.1, size=26)
        self.at("Two attacks")
        self.play(FadeIn(ledger), run_time=0.45)
        self.play(ledger.reveal(0), run_time=0.55)
        self.at("two bond swaps")
        self.play(ledger.reveal(1), run_time=0.55)
        self.at("intron is gone")
        self.play(FadeOut(world.intron), Indicate(VGroup(world.left, world.right), color=BLUE, scale_factor=1.03), run_time=0.8)
        self.finish()


class S10Whole(LivingScene, SpokenScene):
    def construct(self):
        world = add_breathing(whole_transcript(with_polymerase=False, with_ends=True))
        self.play(FadeIn(world, scale=0.86), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.at("Introns leave as lariats")
        drops = VGroup(*[Circle(radius=0.48, color=RED, stroke_width=7).move_to([x, -1.4, 0]) for x in (-3.0, 0, 3.0)])
        self.play(LaggedStart(*[ReplacementTransform(i.copy(), d) for i, d in zip(world.introns, drops)], lag_ratio=0.18),
                  FadeOut(world.introns), run_time=1.25)
        self.at("exons meet in order")
        finish = finished_message(y=0.55)
        self.play(FadeOut(world.cap), run_time=0.25)
        for exon in world.exons:
            exon.clear_updaters()
        self.play(Transform(world.exons, finish.exons), Transform(world.tail, finish.tail),
                  drops.animate.shift(DOWN * 1.3).set_opacity(0.12), run_time=1.25)
        world.cap = finish.cap
        self.play(FadeIn(world.cap), run_time=0.3)
        self.at("transcript is shorter")
        self.play(Indicate(world.exons, color=BLUE, scale_factor=1.035), run_time=0.7)
        self.at("cap and tail remain")
        self.play(Indicate(world.cap, color=GOLD, scale_factor=1.08), Indicate(world.tail, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.at("ready for later steps")
        arrow = Arrow([4.7, 0.55, 0], [6.1, 0.55, 0], buff=0.05, color=GREY, stroke_width=4)
        export = T("export", 28, GREY).move_to([5.4, 1.75, 0])
        self.play(Create(arrow), FadeIn(export), run_time=0.7)
        self.finish()


class S11Rule(LivingScene, SpokenScene):
    def construct(self):
        msg = add_breathing(finished_message(y=0.55))
        self.add(msg, scope_tag("schematic"))
        self.at("Ends marked")
        self.play(Indicate(msg.cap, color=GOLD, scale_factor=1.1), Indicate(msg.tail, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.at("segments chosen")
        self.play(LaggedStart(*[Indicate(e, color=BLUE, scale_factor=1.04) for e in msg.exons], lag_ratio=0.15), run_time=1.2)
        self.at("one primary transcript becomes")
        primary = T("primary transcript", 30, GREY).move_to([0, 2.65, 0])
        messenger = T("messenger RNA", 32, BLUE).move_to([0, 2.65, 0])
        self.play(FadeIn(primary), run_time=0.45)
        self.play(swap(primary, messenger), run_time=0.8)
        self.at("protect and use")
        helpers = VGroup(T("protect", 28, GOLD), T("use", 28, GOLD)).arrange(RIGHT, buff=1.4).move_to([0, -1.25, 0])
        self.play(FadeIn(helpers), run_time=0.65)
        self.at("rule applies")
        scope = caption("protein-coding RNA polymerase II transcripts • eukaryotic nuclei", size=28, y=-2.55)
        self.play(FadeOut(helpers), FadeIn(scope), run_time=0.75)
        self.at("Processing marks transcript ends")
        legend = VGroup(chip("end marks", GOLD, size=26), chip("joined segments", BLUE, size=26)).arrange(RIGHT, buff=0.45).move_to([0, -1.4, 0])
        self.play(FadeOut(scope), FadeOut(messenger), FadeIn(legend), run_time=0.8)
        for e in msg.exons:
            pulse(e, base=3.0, amp=0.8, speed=1.4)
        self.finish()


class S12End(EndCard):
    LINE = "Processing marks transcript ends and\nchooses which segments join into messenger RNA."
