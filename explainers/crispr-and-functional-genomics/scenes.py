"""Which Way Do You Run Genetics?

COLOR MAP (one colour per concept, whole film)
  GREEN  = phenotype / assay readout
  PURPLE = chosen gene
  BLUE   = guide / RNA interference
  GOLD   = Cas9
  ORANGE = PAM (reserved; not needed in this film's pictures)
  GREY   = uncertain, hidden, mixed, or neutral outcomes
"""
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arrow(a, b, color=GREY, width=7, tip=0.25):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def larva_world(missing=True, unknown=True):
    """The opening larva, rebuilt identically wherever it is carried."""
    body = VGroup(*[
        RoundedRectangle(corner_radius=0.32, width=1.05, height=1.35,
                         stroke_color=TEXT, stroke_width=3,
                         fill_color=TEXT, fill_opacity=0.12)
        for _ in range(8)
    ]).arrange(RIGHT, buff=-0.18).move_to([0, -0.15, 0])
    bands = VGroup()
    for i, segment in enumerate(body):
        if not (missing and i == 4):
            bands.add(Line(segment.get_left() + RIGHT * 0.17,
                           segment.get_right() + LEFT * 0.17,
                           color=GREEN, stroke_width=11).move_to(segment))
    eye = Dot(body[0].get_center() + UL * 0.2, radius=0.07, color=TEXT)
    larva = VGroup(body, bands, eye)
    gap = body[4]
    qm = T("?", 78, GREY, weight=BOLD).next_to(gap, UP, buff=0.32)
    gene = RoundedRectangle(corner_radius=0.14, width=2.0, height=0.75,
                            stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.16).move_to([4.8, 1.8, 0])
    frost = RoundedRectangle(corner_radius=0.18, width=2.55, height=1.45,
                             stroke_color=GREY, stroke_width=2,
                             fill_color=BG, fill_opacity=0.78).move_to(gene)
    unk = T("unknown", 28, GREY).next_to(frost, DOWN, buff=0.14)
    world = VGroup(larva, qm)
    world.larva, world.question, world.gap = larva, qm, gap
    if unknown:
        world.add(gene, frost, unk)
        world.gene = VGroup(gene, frost, unk)
    return world


def organism(trait="ordinary", hidden=None, scale=1.0):
    """Neutral organism cartoon with an outward phenotype badge."""
    body = RoundedRectangle(corner_radius=0.34, width=3.15 if hidden else 1.45, height=1.55 if hidden else 1.0,
                            stroke_color=TEXT, stroke_width=3,
                            fill_color=TEXT, fill_opacity=0.10)
    badge = Circle(radius=0.19, stroke_color=GREEN, stroke_width=3,
                   fill_color=GREEN, fill_opacity=0.55).move_to(
                       body.get_center() + RIGHT * 0.38 + (UP * 0.32 if hidden else ORIGIN))
    eye = Dot(body.get_center() + LEFT * 0.35 + UP * 0.16, radius=0.055, color=TEXT)
    g = VGroup(body, badge, eye)
    g.badge = badge
    if hidden:
        h = T(hidden, 24, GREY).move_to(body.get_center() + DOWN * 0.50)
        g.add(h)
        g.hidden = h
    return g.scale(scale)


def assay_gate(center=(0, 0, 0), symbol="trait", color=GREEN):
    x, y, _ = center
    posts = VGroup(Line([x - 0.75, y - 1.15, 0], [x - 0.75, y + 1.15, 0], color=color, stroke_width=9),
                   Line([x + 0.75, y - 1.15, 0], [x + 0.75, y + 1.15, 0], color=color, stroke_width=9),
                   Line([x - 0.75, y + 1.15, 0], [x + 0.75, y + 1.15, 0], color=color, stroke_width=9))
    lab = T(symbol, 28, color).next_to(posts, UP, buff=0.30)
    g = VGroup(posts, lab)
    g.posts, g.label = posts, lab
    return g


def bench_base():
    bench = RoundedRectangle(corner_radius=0.18, width=12.8, height=4.9,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.18).move_to([0, -0.05, 0])
    rule = Line([-6.1, -1.9, 0], [6.1, -1.9, 0], color=GREY, stroke_width=4)
    return VGroup(bench, rule)


def two_lane_world():
    base = bench_base()
    split = DashedLine([0, -2.3, 0], [0, 2.35, 0], color=GREY, stroke_width=2)
    lh = T("phenotype first", 32, GREEN).move_to([-3.25, 2.72, 0])
    rh = T("gene first", 32, PURPLE).move_to([3.25, 2.72, 0])
    gate = assay_gate(center=(-1.05, -0.15, 0), symbol="assay")
    gate.label.move_to([-1.05, -1.62, 0])
    orgs = VGroup(*[organism(scale=0.67) for _ in range(3)]).arrange(RIGHT, buff=0.28).move_to([-4.25, -0.2, 0])
    gene = boxed_label("named gene", PURPLE, size=29).move_to([4.7, -0.2, 0])
    cell = Circle(radius=0.76, stroke_color=GREY, stroke_width=3,
                  fill_color=GREY, fill_opacity=0.09).move_to([1.45, -0.2, 0])
    cell_lab = T("cell", 27, GREY).move_to(cell)
    arrows = VGroup(arrow([-5.5, 1.65, 0], [-1.0, 1.65, 0], GREEN),
                    arrow([5.5, 1.65, 0], [1.0, 1.65, 0], PURPLE))
    return VGroup(base, split, lh, rh, gate, orgs, gene, VGroup(cell, cell_lab), arrows)


def predict_world(with_question=True):
    base = bench_base()
    gate = assay_gate(center=(-1.0, -0.1, 0), symbol="visible trait")
    org = organism(hidden="meiotic change", scale=1.18).move_to([2.0, -0.15, 0])
    exit_arrow = arrow([2.9, -0.15, 0], [5.4, -0.15, 0], GREY)
    unselected = T("unselected exit", 28, GREY).move_to([4.2, 1.45, 0])
    tag = T("schematic", 24, GREY).move_to([-5.7, -3.15, 0])
    g = VGroup(base, gate, org, exit_arrow, unselected, tag)
    g.organism, g.gate = org, gate
    if with_question:
        q = fit_text("Can the assay select what it never sees?", max_w=11.3,
                     size=38, color=GOLD).move_to([0, 3.15, 0])
        g.add(q)
        g.question = q
    return g


def candidate(text="candidate gene?"):
    return boxed_label(text, PURPLE, size=29, pad=0.34)


class S00Hook(TitleCard, SpokenScene):
    LESSON = "CRISPR AND FUNCTIONAL GENOMICS"
    TITLE = "Which Way Do You Run Genetics?"

    def construct(self):
        world = larva_world()
        larva, qm = world.larva, world.question
        bob(larva, amp=0.07, speed=1.5)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.12) for s in larva[0]], lag_ratio=0.08),
                  FadeIn(larva[1]), FadeIn(larva[2]), run_time=1.6)
        self.add(larva)
        self.at("lost part")
        self.play(FadeIn(qm, shift=DOWN * 0.2), run_time=0.7)
        self.at("nobody knows")
        self.play(FadeIn(world.gene, shift=LEFT * 0.2), run_time=0.8)
        self.at("Which end")
        left = arrow(world.gap.get_center() + LEFT * 0.2, [-5.7, -2.25, 0], GREEN)
        right = arrow(world.gap.get_center() + RIGHT * 0.2, [5.7, -2.25, 0], PURPLE)
        self.play(GrowArrow(left), GrowArrow(right), run_time=1.2)
        self.at("visible phenotype")
        pl = T("phenotype", 29, GREEN).next_to(left.get_end(), UP, buff=0.30).shift(LEFT * 0.2)
        gl = T("gene", 29, PURPLE).next_to(right.get_end(), UP, buff=0.30).shift(RIGHT * 0.2)
        self.play(FadeIn(pl), run_time=0.55)
        self.at("chosen gene")
        self.play(FadeIn(gl), run_time=0.55)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "CRISPR AND FUNCTIONAL GENOMICS"
    TITLE = "Which Way Do You Run Genetics?"


class S02TwoLanes(SpokenScene):
    def construct(self):
        world = two_lane_world()
        base, split, lh, rh, gate, orgs, gene, cell, arrows = world
        self.play(FadeIn(base), Create(split), run_time=1.0)
        self.at("On its left")
        self.play(FadeIn(lh), LaggedStart(*[FadeIn(o) for o in orgs], lag_ratio=0.15), run_time=1.2)
        self.play(orgs.animate.shift(RIGHT * 1.0), Create(gate), run_time=1.3)
        for i, o in enumerate(orgs):
            bob(o, amp=0.16, speed=4.0, seed=i)
        self.at("On its right")
        self.play(FadeIn(rh), FadeIn(gene), FadeIn(cell), run_time=0.8)
        self.play(gene.animate.shift(LEFT * 1.0), run_time=1.1)
        bob(gene, amp=0.16, speed=3.7, seed=3)
        self.at("not different toolkits")
        same = T("same bench", 30, TEXT).move_to([0, -2.75, 0])
        self.play(FadeIn(same), run_time=0.6)
        self.at("different directions")
        self.play(Create(arrows), Indicate(VGroup(lh, rh), color=GOLD, scale_factor=1.03), run_time=1.4)
        pulse(arrows[0], base=7, amp=1.2, speed=2.0)
        pulse(arrows[1], base=7, amp=1.2, speed=2.0)
        self.finish()


class S03Forward(SpokenScene):
    def construct(self):
        base = bench_base()
        lane = T("phenotype first", 36, GREEN).move_to([0, 3.15, 0])
        gate = assay_gate(center=(-0.8, 0.15, 0), symbol="assay")
        orgs = VGroup(*[organism(scale=0.72) for _ in range(3)]).arrange(DOWN, buff=0.22).move_to([-4.6, 0.15, 0])
        self.add(base, lane)
        self.at("random mutations")
        muts = VGroup(*[Dot(radius=0.13, color=GREY) for _ in range(3)])
        mut_lab = T("random mutations", 28, GREY).move_to([-4.6, 2.15, 0])
        for m, o in zip(muts, orgs): m.move_to(o)
        self.play(FadeIn(mut_lab), LaggedStart(*[FadeIn(m, shift=DOWN * 0.5) for m in muts], lag_ratio=0.18),
                  FadeIn(orgs), run_time=1.3)
        self.play(VGroup(orgs, muts).animate.shift(RIGHT * 2.2), FadeIn(gate), run_time=1.5)
        self.at("gate keeps")
        self.play(orgs[1].animate.set_color(GREEN).shift(RIGHT * 2.0),
                  FadeOut(orgs[0]), FadeOut(orgs[2]), FadeOut(muts), run_time=1.1)
        tray = boxed_label("recover lines", GREEN, size=30, box=(2.8, 0.8)).move_to([3.3, 1.35, 0])
        self.at("recover lines")
        self.play(FadeIn(tray), orgs[1].animate.move_to(tray.get_center() + DOWN * 1.0), run_time=0.9)
        chrom = RoundedRectangle(corner_radius=0.16, width=4.0, height=0.55,
                                 stroke_color=PURPLE, stroke_width=3,
                                 fill_color=PURPLE, fill_opacity=0.2).move_to([2.6, -1.05, 0])
        lesions = VGroup(*[Dot(chrom.get_left() + RIGHT * x, radius=0.11, color=GREY) for x in (0.8, 1.8, 3.0)])
        self.at("map each lesion")
        self.play(ReplacementTransform(tray, chrom), FadeIn(lesions), run_time=1.0)
        cand = candidate().move_to([2.6, -1.25, 0])
        loop = CurvedArrow([3.5, -0.65, 0], [4.25, 0.0, 0],
                           angle=-0.8, color=GREY, stroke_width=4)
        self.at("test a candidate")
        self.play(ReplacementTransform(VGroup(chrom, lesions), cand), Create(loop), run_time=1.0)
        pulse(cand[0], base=2.5, amp=2.0, speed=2.2)
        self.at("nobody expected")
        self.play(Indicate(cand, color=GOLD, scale_factor=1.06), run_time=1.0)
        self.at("only visible outcomes")
        cone = Polygon(gate.get_left(), [-5.8, 1.65, 0], [-5.8, -1.35, 0],
                       stroke_width=0, fill_color=GREEN, fill_opacity=0.12)
        self.play(FadeIn(cone), gate.animate.set_color(GREEN), run_time=1.0)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = predict_world(with_question=False)
        base, gate, org, exit_arrow, exit_lab, tag = world
        self.add(base, gate, tag)
        self.at("mutation that changes")
        self.play(FadeIn(org, shift=LEFT * 0.4), run_time=0.8)
        pulse(org[0], base=3.0, amp=1.8, speed=2.0)
        bob(org.badge, amp=0.16, speed=4.0)
        pulse(org.hidden, base=2.5, amp=1.0, speed=2.4)
        self.at("never changes the trait")
        self.play(Indicate(org.badge, color=GREEN, scale_factor=1.3), run_time=1.0)
        self.at("Will this forward screen")
        q = fit_text("Can the assay select what it never sees?", max_w=11.3,
                     size=38, color=GOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.8)
        self.at("unaffected looking")
        org.badge.clear_updaters()
        self.play(org.animate.shift(RIGHT * 2.0), GrowArrow(exit_arrow), FadeIn(exit_lab), run_time=1.5)
        bob(org.badge, amp=0.16, speed=4.0, seed=2)
        self.at("hidden mutation")
        self.play(Indicate(org.hidden, color=GREY, scale_factor=1.08), run_time=1.0)
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = "Can the assay select what it never sees?"
    SECONDS = 4.5
    CARD = {"y": 3.15, "size": 38, "max_w": 11.3}
    RING_AT = (6.0, -3.05, 0)

    def backdrop(self):
        w = predict_world(with_question=False)
        pulse(w.organism.hidden, base=2.5, amp=1.0, speed=2.4)
        bob(w.organism.badge, amp=0.035, speed=1.7)
        return w


class S06BlindSpot(SpokenScene):
    def construct(self):
        w = predict_world(with_question=False)
        base, gate, org, exit_arrow, exit_lab, tag = w
        org.shift(RIGHT * 2.0)
        self.add(base, gate, org, exit_arrow, exit_lab, tag)
        bob(gate.label, amp=0.16, speed=4.0)
        no = T("NO", 62, RED, weight=BOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(no, scale=0.7), run_time=0.5)
        self.at("cannot select")
        blind = boxed_label("assay blind spot", GREY, size=34).move_to([0, 3.05, 0])
        self.play(swap(no, blind), run_time=0.8)
        cone = Polygon(gate.get_left(), [-5.9, 1.45, 0], [-5.9, -1.45, 0],
                       stroke_width=0, fill_color=GREEN, fill_opacity=0.15)
        self.at("assay never records")
        self.play(FadeIn(cone), run_time=0.9)
        probe = Dot(radius=0.2, color=GREEN).set_opacity(0.85)
        probe._ft = 0.0
        def _flow(m, dt):
            m._ft += dt
            f = (m._ft * 0.35) % 1.0
            m.move_to([-0.9 - f * 4.6, 0.9 * np.sin(m._ft * 2.2) * (1 - f) * 0.9, 0])
        probe.add_updater(_flow)
        cone._pt = 0.0
        def _cp(m, dt):
            m._pt += dt
            m.set_fill(GREEN, opacity=0.15 + 0.09 * np.sin(m._pt * 3.0))
        cone.add_updater(_cp)
        self.add(probe)
        for post in gate.posts:
            pulse(post, base=9.0, amp=2.5, speed=1.8)
        self.at("bounded by phenotype")
        self.play(Indicate(gate, color=GREEN, scale_factor=1.03), run_time=1.0)
        gate2 = assay_gate(center=(1.2, 0.0, 0), symbol="meiosis assay")
        cone2 = Polygon(gate2.get_right(), [5.9, 1.25, 0], [5.9, -1.25, 0],
                        stroke_width=0, fill_color=GREEN, fill_opacity=0.13)
        self.at("different assay")
        probe.clear_updaters(); self.remove(probe); cone.clear_updaters()
        self.play(FadeOut(exit_arrow), FadeOut(exit_lab), org.animate.move_to([4.35, 0, 0]),
                  FadeIn(gate2, shift=LEFT * 0.3), FadeIn(cone2), run_time=1.4)
        self.at("reveal the same mutation")
        self.play(Indicate(org.hidden, color=GREEN, scale_factor=1.12), run_time=1.0)
        self.at("belongs to the measurement")
        probe2 = Dot(radius=0.2, color=GREEN).set_opacity(0.85)
        probe2._ft = 0.0
        def _flow2(m, dt):
            m._ft += dt
            f = (m._ft * 0.4) % 1.0
            m.move_to([2.0 + f * 3.4, 0.8 * np.sin(m._ft * 2.6) * (1 - f), 0])
        probe2.add_updater(_flow2)
        self.add(probe2)
        self.play(gate.animate.set_opacity(0.35), cone.animate.set_opacity(0.05),
                  Indicate(gate2.label, color=GOLD, scale_factor=1.05), run_time=1.2)
        self.finish()


class S07Reverse(SpokenScene):
    def construct(self):
        base = bench_base()
        title = T("gene first", 38, PURPLE).move_to([0, 3.15, 0])
        gene = boxed_label("named gene", PURPLE, size=34).move_to([-4.8, 0.65, 0])
        cell = Circle(radius=1.0, stroke_color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.08).move_to([-2.2, 0.65, 0])
        self.add(base, title)
        self.play(FadeIn(gene, shift=RIGHT * 0.2), FadeIn(cell), run_time=0.8)
        self.at("Lower its output")
        rnai = boxed_label("RNA interference", BLUE, size=28, pad=0.40).move_to([0.8, 1.7, 0])
        out = ValueTracker(0.9)
        gauge = dial(out, center=[4.0, 1.15, 0], radius=1.0, label="protein output", color=BLUE, size=30)
        self.play(GrowArrow(arrow(gene.get_right() + RIGHT * 0.28, rnai.get_left() + LEFT * 0.28, BLUE)),
                  FadeIn(rnai), FadeIn(gauge), run_time=1.0)
        self.play(out.animate.set_value(0.2), run_time=1.3)
        bob(gene, amp=0.07, speed=3.0); bob(cell, amp=0.07, speed=3.0, seed=1)
        self.at("alter its DNA")
        cas = boxed_label("Cas9", GOLD, size=31).move_to([0.25, -1.05, 0])
        dna = RoundedRectangle(corner_radius=0.12, width=2.4, height=0.48,
                               stroke_color=PURPLE, stroke_width=3,
                               fill_color=PURPLE, fill_opacity=0.2).move_to([3.05, -1.05, 0])
        self.play(FadeIn(cas), GrowArrow(arrow(cas.get_right(), dna.get_left(), GOLD)), FadeIn(dna), run_time=1.0)
        bob(cas, amp=0.07, speed=3.2, seed=2); bob(dna, amp=0.07, speed=2.8, seed=3); bob(rnai, amp=0.06, speed=3.0, seed=4)
        self.at("measure what changes")
        meters = VGroup(*[RoundedRectangle(corner_radius=0.12, width=0.55, height=h,
                                           stroke_color=GREEN, stroke_width=2,
                                           fill_color=GREEN, fill_opacity=0.55)
                         for h in (0.75, 1.35, 1.0)]).arrange(RIGHT, buff=0.22, aligned_edge=DOWN).move_to([5.35, -0.6, 0])
        self.play(FadeOut(gauge), LaggedStart(*[GrowFromEdge(m, DOWN) for m in meters], lag_ratio=0.2), run_time=1.2)
        for i, meter in enumerate(meters):
            bob(meter, amp=0.18, speed=4.0, seed=i)
        self.at("focused question")
        self.play(Indicate(gene, color=GOLD, scale_factor=1.05), run_time=0.9)
        cabinet = RoundedRectangle(corner_radius=0.15, width=3.3, height=1.45,
                                   stroke_color=GREY, stroke_width=3).move_to([-4.5, -1.15, 0])
        others = T("other genes\nnot chosen", 27, GREY, line_spacing=0.75).move_to(cabinet)
        self.at("nobody chose")
        self.play(FadeIn(VGroup(cabinet, others)), run_time=0.8)
        bob(cabinet, amp=0.06, speed=3.0, seed=5); bob(others, amp=0.06, speed=3.0, seed=5)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        panels = TwoPanel("forward: assay boundary", "reverse: chosen list", colors=(GREEN, PURPLE), size=30)
        self.play(FadeIn(panels), run_time=0.8)
        bob(panels.left_head, amp=0.14, speed=4.0)
        bob(panels.right_head, amp=0.14, speed=3.7, seed=2)
        left_gate = VGroup(
            VGroup(Line([-0.58, -0.85, 0], [-0.58, 0.72, 0], color=GREEN, stroke_width=7),
                   Line([0.58, -0.85, 0], [0.58, 0.72, 0], color=GREEN, stroke_width=7),
                   Line([-0.58, 0.72, 0], [0.58, 0.72, 0], color=GREEN, stroke_width=7)),
            T("assay", 24, GREEN).move_to([0, 1.03, 0]))
        left_traits = VGroup(*[Circle(radius=0.2, color=c, fill_color=c, fill_opacity=0.5)
                              for c in (GREEN, GREEN, GREY, GREY)]).arrange(DOWN, buff=0.3)
        left = VGroup(left_gate, left_traits).arrange(RIGHT, buff=0.55)
        panels.put(left, "left")
        right_gene = boxed_label("chosen gene", PURPLE, size=27)
        shelf = VGroup(*[boxed_label("gene", GREY, size=24, pad=0.12) for _ in range(3)]).arrange(DOWN, buff=0.3)
        right = VGroup(right_gene, shelf).arrange(RIGHT, buff=0.45)
        panels.put(right, "right")
        self.at("Forward screens miss")
        self.play(FadeIn(left_gate), LaggedStart(*[FadeIn(t) for t in left_traits], lag_ratio=0.15), run_time=1.1)
        for i, trait in enumerate(left_traits):
            bob(trait, amp=0.16, speed=4.0, seed=i)
        self.play(left_traits[2:].animate.set_opacity(0.22), run_time=0.7)
        self.at("Reverse experiments miss")
        self.play(FadeIn(right_gene), FadeIn(shelf), run_time=0.9)
        self.play(shelf.animate.set_opacity(0.25), run_time=0.7)
        self.at("complete mechanism")
        c1, c2 = candidate(), candidate()
        c1.move_to([-3.2, -1.75, 0]); c2.move_to([3.2, -1.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.9)
        pulse(c1[0], base=2.5, amp=1.8, speed=2.0)
        pulse(c2[0], base=2.5, amp=1.8, speed=2.2)
        self.at("separate causal test")
        loops = VGroup(CurvedArrow([-2.4, -0.75, 0], [-1.7, -0.75, 0], angle=-1.0, color=GREY),
                       CurvedArrow([1.7, -0.75, 0], [2.4, -0.75, 0], angle=-1.0, color=GREY))
        self.play(Create(loops), run_time=1.2)
        self.finish()


def guide_cell(gene_name):
    cell = Circle(radius=0.75, stroke_color=GREY, stroke_width=3,
                  fill_color=GREY, fill_opacity=0.08)
    card = RoundedRectangle(corner_radius=0.08, width=0.72, height=0.52,
                            stroke_color=BLUE, stroke_width=2,
                            fill_color=BLUE, fill_opacity=0.18).move_to(cell)
    guide = T(gene_name, 24, BLUE, weight=BOLD).move_to(card)
    return VGroup(cell, card, guide)


class S09Pooled(SpokenScene):
    def construct(self):
        base = bench_base()
        title = T("pooled Cas9 screen", 38, GOLD).move_to([0, 3.15, 0])
        self.add(base)
        self.play(FadeIn(title), run_time=0.6)
        self.at("choose many guides")
        guides = VGroup(*[boxed_label(f"guide {c}", BLUE, size=25, pad=0.14) for c in "ABCD"])
        guides.arrange(DOWN, buff=0.18).move_to([-5.0, 0.3, 0])
        genes = VGroup(*[T(f"gene {c}", 24, PURPLE).next_to(g, RIGHT, buff=0.18) for c, g in zip("ABCD", guides)])
        self.play(LaggedStart(*[FadeIn(VGroup(g, n), shift=RIGHT * 0.15) for g, n in zip(guides, genes)], lag_ratio=0.12), run_time=1.2)
        self.at("each cell a single guide")
        cells = VGroup(*[guide_cell(c) for c in "ABCD"]).arrange_in_grid(2, 2, buff=0.35).move_to([-1.7, 0.2, 0])
        self.play(ReplacementTransform(VGroup(guides, genes), cells), run_time=1.3)
        gate = VGroup(
            VGroup(Line([0.0, -0.8, 0], [0.0, 0.75, 0], color=GREEN, stroke_width=7),
                   Line([1.1, -0.8, 0], [1.1, 0.75, 0], color=GREEN, stroke_width=7),
                   Line([0.0, 0.75, 0], [1.1, 0.75, 0], color=GREEN, stroke_width=7)),
            T("selection", 24, GREEN).move_to([-1.3, 2.1, 0]))
        self.at("selection keeps cells")
        self.play(FadeIn(gate), cells.animate.shift(RIGHT * 1.2), run_time=1.1)
        bob(gate[1], amp=0.12, speed=4.0)
        kept = VGroup(cells[0].copy(), cells[3].copy()).arrange(DOWN, buff=0.25).move_to([2.35, 0.25, 0])
        self.play(ReplacementTransform(cells, kept), run_time=0.9)
        self.at("Sequencing identifies")
        bars_e = VGroup(*[Rectangle(width=0.5, height=h, color=GREEN, fill_color=GREEN, fill_opacity=0.65)
                          for h in (0.8, 1.55)]).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        bars_d = VGroup(*[Rectangle(width=0.5, height=h, color=GREY, fill_color=GREY, fill_opacity=0.55)
                          for h in (1.35, 0.5)]).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        charts = VGroup(VGroup(bars_e, T("enriched", 27, GREEN).next_to(bars_e, DOWN, buff=0.18)),
                        VGroup(bars_d, T("depleted", 27, GREY).next_to(bars_d, DOWN, buff=0.18)))
        charts.arrange(RIGHT, buff=0.6).move_to([4.55, 0.15, 0])
        self.play(FadeOut(kept), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_e], lag_ratio=0.2),
                  FadeIn(charts[0][1]), run_time=1.0)
        self.at("depleted")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_d], lag_ratio=0.2), FadeIn(charts[1][1]), run_time=1.0)
        self.at("nominate candidates")
        cand = candidate("candidates?").move_to([4.55, -0.55, 0])
        self.play(ReplacementTransform(charts, cand), run_time=1.0)
        self.finish()


def route(start_text, end_text, start_color, end_color, y):
    start = boxed_label(start_text, start_color, size=27).move_to([-4.8, y, 0])
    end = candidate(end_text).move_to([4.8, y, 0])
    path = arrow(start.get_right() + RIGHT * 0.22, end.get_left() + LEFT * 0.22, start_color, width=6)
    return VGroup(start, path, end)


class S10Compare(SpokenScene):
    def construct(self):
        base = bench_base()
        self.add(base)
        r1 = route("phenotype", "gene?", GREEN, PURPLE, 1.55)
        r1.shift(UP * 0.15)
        r2 = route("chosen gene", "phenotype?", PURPLE, GREEN, 0.0)
        r2.shift(UP * 0.3)
        guides = boxed_label("many guides", BLUE, size=27).move_to([-4.8, -1.55, 0])
        gate_posts = VGroup(Line([-0.45, -2.1, 0], [-0.45, -1.15, 0], color=GREEN, stroke_width=7),
                            Line([0.45, -2.1, 0], [0.45, -1.15, 0], color=GREEN, stroke_width=7),
                            Line([-0.45, -1.15, 0], [0.45, -1.15, 0], color=GREEN, stroke_width=7))
        gate = VGroup(gate_posts, T("selection", 24, GREEN).move_to([0, -0.88, 0]))
        c3 = candidate("candidates?").move_to([4.8, -1.55, 0])
        r3 = VGroup(guides, arrow(guides.get_right() + RIGHT * 0.22, gate.get_left() + LEFT * 0.22, BLUE, 6), gate,
                    arrow(gate.get_right() + RIGHT * 0.22, c3.get_left() + LEFT * 0.22, GREEN, 6), c3)
        r3.shift(UP * 0.55)
        self.at("phenotype first screen")
        self.play(FadeIn(r1[0]), GrowArrow(r1[1]), FadeIn(r1[2]), run_time=1.4)
        bob(r1[2], amp=0.10, speed=4.0)
        self.at("gene first experiment")
        self.play(FadeIn(r2[0]), GrowArrow(r2[1]), FadeIn(r2[2]), run_time=1.4)
        bob(r2[2], amp=0.10, speed=3.8, seed=2)
        self.at("pooled screen")
        self.play(FadeIn(guides), GrowArrow(r3[1]), FadeIn(gate), GrowArrow(r3[3]), FadeIn(c3), run_time=1.5)
        bob(c3, amp=0.15, speed=4.0, seed=4)
        self.at("assay defines")
        spot = Circle(radius=0.75, stroke_width=0, fill_color=GREEN, fill_opacity=0.19).move_to(r1[0])
        self.play(FadeIn(spot), spot.animate.move_to(r1[2]), run_time=1.0)
        self.play(spot.animate.move_to(r2[2]), run_time=1.0)
        self.play(spot.animate.move_to(gate), run_time=1.0)
        bob(spot, amp=0.11, speed=1.7)
        self.finish()


class S11Land(SpokenScene):
    def construct(self):
        a1 = arrow([-5.5, 1.15, 0], [5.5, 1.15, 0], GREEN, width=10, tip=0.35)
        a2 = arrow([5.5, -1.15, 0], [-5.5, -1.15, 0], PURPLE, width=10, tip=0.35)
        p = boxed_label("phenotype first", GREEN, size=32).move_to([-4.5, 2.25, 0])
        g = boxed_label("gene first", PURPLE, size=32).move_to([4.5, -2.25, 0])
        gene = boxed_label("gene?", PURPLE, size=30).move_to([4.8, 2.25, 0])
        pheno = boxed_label("phenotype?", GREEN, size=30).move_to([-4.8, -2.25, 0])
        self.play(FadeIn(VGroup(p, g, gene, pheno)), GrowArrow(a1), GrowArrow(a2), run_time=1.4)
        pulse(a1, base=10.0, amp=2.0, speed=1.7)
        pulse(a2, base=10.0, amp=2.0, speed=1.9)
        self.at("What did the experiment")
        q1 = T("What did the experiment choose first?", 36, GOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(q1, shift=DOWN * 0.15), run_time=0.8)
        s1 = Circle(radius=0.62, stroke_width=0, fill_color=GREEN, fill_opacity=0.18).move_to(p)
        self.play(FadeIn(s1), s1.animate.move_to(gene), run_time=1.5)
        self.at("What could its assay")
        q2 = T("What could its assay actually detect?", 36, GOLD).move_to([0, 3.2, 0])
        self.play(swap(q1, q2), run_time=0.8)
        shadow = VGroup(Rectangle(width=4.0, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=0.12).move_to([0, 0.2, 0]),
                        Rectangle(width=4.0, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=0.12).move_to([0, -2.1, 0]))
        self.play(FadeIn(shadow), s1.animate.move_to(pheno), run_time=1.4)
        self.at("reach and its blind spot")
        self.play(Indicate(VGroup(a1, a2), color=GOLD, scale_factor=1.02), run_time=1.0)
        self.at("direction is part")
        rule = T("The direction is part of the evidence.", 38, TEXT).move_to([0, 3.2, 0])
        self.play(swap(q2, rule), FadeOut(shadow), run_time=1.0)
        self.play(a1.animate.set_color(PURPLE), a2.animate.set_color(GREEN), run_time=1.0)
        self.finish()


class S12End(EndCard):
    LINE = "What you choose first determines what a genetic experiment can find."
