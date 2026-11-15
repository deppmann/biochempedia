"""RNA processing, chapter 2: When the Joins Change.

COLOR MAP (continued from chapter 1)
  BLUE = exons and mature RNA; RED = introns or removed coding sequence
  GOLD = cap, tail, codon emphasis; TEAL = splice choices and junctions
  GREEN = preserved reading-frame alignment; GREY = guides and neutral limits
  TEXT = questions and neutral marks; WHITE = the invented-exon outline
"""
from bp_parts import *  # noqa: F401,F403


EXON_Y = 0.45
EXON_H = 1.4
LEFT_X = -5.45


def exon(width, x, y=EXON_Y, outline=BLUE, fill=BLUE, opacity=0.48):
    return RoundedRectangle(
        corner_radius=0.09, width=width, height=EXON_H,
        stroke_color=outline, stroke_width=3, fill_color=fill,
        fill_opacity=opacity,
    ).move_to([x, y, 0])


def intron(x1, x2, y=EXON_Y):
    return Line([x1, y, 0], [x2, y, 0], color=RED, stroke_width=9)


def join_arc(a, b, y=EXON_Y, color=TEAL, height=1.0):
    return ArcBetweenPoints([a, y + EXON_H / 2, 0], [b, y + EXON_H / 2, 0],
                            angle=-1.15, color=color, stroke_width=5)


def end_marks(y=EXON_Y, left=-5.8, right=5.55):
    cap = VGroup(Circle(radius=0.48, color=GOLD, stroke_width=3,
                        fill_color=GOLD, fill_opacity=0.25), T("cap", 32, GOLD)).move_to([left, y, 0])
    tail = M("AAAA", 32, GOLD).move_to([right, y, 0])
    return cap, tail


def finished_message(y=1.05, scale=1.0, with_arcs=True):
    """The carried capped-and-tailed message, always rebuilt at identical landmarks."""
    widths = [2.25, 1.85, 2.15, 2.0]
    gap = 0.05
    total = sum(widths) + gap * 3
    x = -total / 2
    blocks = VGroup()
    joins = VGroup()
    edges = []
    for i, w in enumerate(widths):
        b = exon(w, x + w / 2, y)
        blocks.add(b)
        edges.append((x, x + w))
        x += w + gap
    for i in range(3):
        joins.add(Line([edges[i][1], y, 0], [edges[i + 1][0], y, 0], color=TEAL, stroke_width=7))
    cap, tail = end_marks(y, left=edges[0][0] - 0.48, right=edges[-1][1] + 0.62)
    arcs = VGroup(*[join_arc(edges[i][1] - 0.2, edges[i + 1][0] + 0.2, y, height=0.6) for i in range(3)])
    g = VGroup(cap, blocks, joins, tail)
    if with_arcs:
        g.add(arcs)
    g.blocks, g.joins, g.arcs, g.cap, g.tail = blocks, joins, arcs, cap, tail
    if scale != 1:
        g.scale(scale)
    return g


def premrna(y=EXON_Y, scale=1.0):
    """One schematic copy: four equal exons separated by red introns."""
    centers = [-4.6, -1.55, 1.55, 4.6]
    blocks = VGroup(*[exon(1.55, x, y) for x in centers])
    ribbons = VGroup(*[intron(centers[i] + 0.775, centers[i + 1] - 0.775, y) for i in range(3)])
    g = VGroup(ribbons, blocks)
    g.blocks, g.ribbons = blocks, ribbons
    if scale != 1:
        g.scale(scale)
    return g


def triplet_ruler(y=-1.05, start=-5.55, count=12, cell=0.9, shift=0.0, color=GREY):
    """Computed triplet boundaries: every box spans exactly three base positions."""
    base = cell / 3
    boxes = VGroup()
    letters = VGroup()
    for codon in range(count):
        x0 = start + shift + codon * cell
        boxes.add(Rectangle(width=cell, height=0.76, stroke_color=color, stroke_width=2.3,
                            fill_color=color, fill_opacity=0.06).move_to([x0 + cell / 2, y, 0]))
        for k in range(3):
            letters.add(M("•", 24, TEXT).move_to([x0 + (k + 0.5) * base, y, 0]))
    g = VGroup(boxes, letters)
    g.boxes, g.letters = boxes, letters
    return g


def small_message(at):
    """A compact stack icon with no text that would become unreadably small."""
    bars = VGroup(*[RoundedRectangle(corner_radius=0.04, width=w, height=0.22,
                                     color=BLUE, fill_color=BLUE, fill_opacity=0.48,
                                     stroke_width=2) for w in (0.55, 0.48, 0.52, 0.5)])
    bars.arrange(RIGHT, buff=0.035).move_to(at)
    return bars


def reading_marker(x=-5.55, y=-1.05):
    marker = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=0.9, stroke_width=0).scale(0.16).rotate(PI)
    marker.move_to([x, y + 0.48, 0])
    return marker


def alive(mob, base=3.5, amp=1.8, speed=3.2):
    """Continuous, gentle outline activity on the subject during narrated holds."""
    return pulse(mob, base=base, amp=amp, speed=speed)


def sway(mob, amp=0.09, speed=3.6, seed=0.0):
    """Move a carried diagram continuously without fighting its cue-driven transforms."""
    mob._sway_t = seed
    mob._sway_last = amp * np.sin(speed * seed)

    def update(m, dt):
        m._sway_t += dt
        now = amp * np.sin(speed * m._sway_t)
        m.shift(UP * (now - m._sway_last))
        m._sway_last = now
    return mob.add_updater(update)


def sway_all(*mobs, seed=0.0):
    for mob in mobs:
        sway(mob, seed=seed)
    return VGroup(*mobs)


def predict_world(question=True):
    """Exact carried frame for s06 and its deliberate pause."""
    left = exon(2.65, -3.95, 0.75)
    chosen = exon(3.6, -0.55, 1.8, outline=WHITE, opacity=0.36)
    right = exon(3.25, 3.9, 0.75)
    ruler = triplet_ruler(y=-0.65, start=-5.25, count=12, cell=0.88)
    lab = boxed_label("12 coding nucleotides", WHITE, size=28).move_to([4.45, 2.85, 0])
    marker = reading_marker(-5.25, -0.65)
    gap = DashedLine([-2.05, 0.75, 0], [1.25, 0.75, 0], color=GREY, stroke_width=3, dash_length=0.18)
    world = VGroup(left, gap, right, chosen, ruler, lab, marker)
    world.marker, world.chosen, world.ruler = marker, chosen, ruler
    if question:
        world.add(question_card("Do downstream triplets stay aligned?", y=-3.15, max_w=10.2))
    return world


class S00Link(SpokenScene):
    def construct(self):
        done = finished_message(y=1.55, scale=1.05)
        self.play(FadeIn(done), run_time=0.8)
        alive(done.blocks)
        sway(done.blocks)
        self.at("marked both ends")
        self.play(Indicate(VGroup(done.cap, done.tail), color=GOLD), run_time=0.9)
        self.at("If those joins change")
        self.play(LaggedStart(*[Indicate(j, color=TEAL, scale_factor=1.25) for j in done.joins], lag_ratio=0.2), run_time=1.2)
        strip = VGroup(*[Rectangle(width=0.75, height=0.48, color=GREY, stroke_width=2) for _ in range(9)]).arrange(RIGHT, buff=0.06)
        strip.move_to([0, -2.25, 0])
        q = T("?", 54, TEXT, weight=BOLD).next_to(strip, RIGHT, buff=0.28)
        self.play(FadeIn(strip, shift=UP * 0.15), FadeIn(q), run_time=0.8)
        self.at("Follow different copies")
        self.play(done.animate.scale(0.72).move_to([0, 2.15, 0]), FadeOut(VGroup(strip, q)), run_time=0.9)
        fresh = premrna(y=-0.15, scale=0.82)
        fresh_label = fit_text("another copy of the same gene's transcript", max_w=6.0, size=28, color=TEXT).move_to([0, -1.35, 0])
        self.play(FadeIn(fresh, shift=DOWN * 0.15), FadeIn(fresh_label), run_time=0.9)
        alive(fresh.blocks)
        sway_all(fresh.blocks, fresh.ribbons, seed=0.5)
        self.at("regulatory signals")
        arcs = VGroup(join_arc(-3.85, -2.3, -0.15), join_arc(-0.8, 0.8, -0.15), join_arc(2.3, 3.85, -0.15))
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2), run_time=1.4)
        self.add(scope_tag("schematic"))
        pulse(arcs, base=5, amp=1.2, speed=2.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "RNA processing"
    TITLE = "When the Joins Change"


class S02Patterns(SpokenScene):
    def construct(self):
        world = premrna(y=0.35)
        label = T("one of many copies", 30, TEXT).move_to([0, 2.75, 0])
        self.play(FadeIn(world), FadeIn(label), run_time=0.8)
        alive(world.blocks)
        sway_all(world.blocks, world.ribbons)
        stack = VGroup()
        tag = T("skip", 30, TEAL).move_to([-4.9, -2.35, 0])
        self.at("skip an exon")
        self.play(world.blocks[1].animate.shift(UP * 1.45), FadeIn(tag), run_time=0.9)
        stack.add(small_message([5.25, -1.75, 0]))
        self.play(FadeIn(stack[-1]), world.blocks[1].animate.shift(DOWN * 1.45), run_time=0.65)
        self.at("shift a splice site")
        new_tag = T("shift", 30, TEAL).move_to(tag)
        flag = Triangle(color=TEAL, fill_color=TEAL, fill_opacity=1).scale(0.16).rotate(-PI / 2).move_to([-0.85, 1.05, 0])
        self.play(swap(tag, new_tag), FadeIn(flag), run_time=0.55)
        self.play(flag.animate.shift(RIGHT * 0.65), run_time=0.75)
        m2 = small_message([5.25, -2.25, 0])
        stack.add(m2); self.play(FadeIn(m2), FadeOut(flag), run_time=0.6)
        self.at("choose between exons")
        alt_tag = T("choose", 30, TEAL).move_to(tag)
        self.play(swap(new_tag, alt_tag), world.blocks[1].animate.shift(UP * 0.6), world.blocks[2].animate.shift(DOWN * 0.6), run_time=0.85)
        m3 = small_message([5.25, -2.75, 0])
        stack.add(m3); self.play(FadeIn(m3), world.blocks[1].animate.shift(DOWN * 0.6), world.blocks[2].animate.shift(UP * 0.6), run_time=0.7)
        self.at("retain an intron")
        retain_tag = T("retain", 30, TEAL).move_to(tag)
        self.play(swap(alt_tag, retain_tag), Indicate(world.ribbons[1], color=RED, scale_factor=1.15), run_time=0.9)
        m4 = small_message([5.25, -3.25, 0])
        stack.add(m4); self.play(FadeIn(m4), run_time=0.5)
        self.at("differ among tissues")
        self.play(LaggedStart(*[Indicate(m, color=TEAL, scale_factor=1.08) for m in stack], lag_ratio=0.16), run_time=1.2)
        self.finish()


class S03Variant(SpokenScene):
    def construct(self):
        left, right = exon(3.1, -3.55, 1.35), exon(3.1, 3.55, 1.35)
        bridge = intron(-2.0, 2.0, 1.35)
        normal = Triangle(color=TEAL, fill_color=TEAL, fill_opacity=1).scale(0.24).rotate(PI).move_to([2.0, 2.05, 0])
        nlab = T("normal site", 28, TEAL).move_to([4.2, 2.55, 0])
        self.play(FadeIn(VGroup(left, bridge, right, normal, nlab)), run_time=0.8)
        alive(VGroup(left, right))
        sway_all(left, bridge, right, normal)
        self.at("weaken a normal splice site")
        self.play(normal.animate.set_opacity(0.28), nlab.animate.set_opacity(0.45), run_time=0.9)
        self.at("Nearby sites")
        flags = VGroup(*[Triangle(color=TEAL, fill_color=TEAL, fill_opacity=0.9).scale(0.16).rotate(PI).move_to([x, 1.92, 0]) for x in (0.75, 1.35)])
        cryptic = T("possible cryptic sites", 28, TEAL).move_to([0.0, 3.15, 0])
        self.play(FadeIn(flags), FadeIn(cryptic), run_time=0.8)
        arcs = VGroup(join_arc(-2.0, 0.75, 1.35), join_arc(-2.0, 1.35, 1.35), join_arc(-2.0, 2.0, 1.35))
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2), run_time=1.2)
        self.at("most often causes exon skipping")
        self.play(FadeOut(VGroup(left, bridge, right, normal, nlab, flags, cryptic, arcs)), run_time=0.45)
        lanes = VGroup(
            boxed_label("skip (most often)", TEAL, size=30, box=(8.8, 1.1)),
            boxed_label("cryptic site", TEAL, size=28, box=(5.3, 0.95)),
            boxed_label("retain", RED, size=28, box=(5.3, 0.95)),
        ).arrange(DOWN, buff=0.32).move_to([0, 0.15, 0])
        alive(VGroup(*[lane[0] for lane in lanes]), base=2.5, amp=1.2)
        sway_all(*lanes)
        self.play(FadeIn(lanes[0], shift=RIGHT * 0.15), run_time=0.9)
        self.at("Less often")
        self.play(LaggedStart(FadeIn(lanes[1], shift=RIGHT * 0.15), FadeIn(lanes[2], shift=RIGHT * 0.15), lag_ratio=0.35), run_time=1.2)
        self.at("several products at once")
        self.play(LaggedStart(*[Indicate(l, scale_factor=1.03) for l in lanes], lag_ratio=0.15), run_time=1.2)
        self.add(scope_tag("lane widths are schematic"))
        self.finish()


class S04Evidence(SpokenScene):
    def construct(self):
        allele = boxed_label("studied beta-thalassemia allele", TEAL, size=30).move_to([0, 2.7, 0])
        stem = Arrow(allele.get_bottom() + DOWN * 0.08, [0, 1.65, 0], buff=0.08, color=TEAL, stroke_width=4)
        self.play(FadeIn(allele), GrowArrow(stem), run_time=0.9)
        self.at("two abnormal RNAs")
        main = VGroup(exon(2.5, -3.7, 0.55), Rectangle(width=1.35, height=0.55, color=RED, fill_color=RED, fill_opacity=0.5).move_to([-1.75, 0.55, 0]), exon(2.5, 0.2, 0.55))
        minor = VGroup(exon(2.4, -2.8, -1.75), exon(2.4, 0.05, -1.75), Line([-1.6, -1.75, 0], [-1.15, -1.75, 0], color=TEAL, stroke_width=7))
        alive(main); alive(minor)
        main_lab = T("main: part of intron retained", 30, TEXT).move_to([2.8, -0.68, 0])
        minor_lab = T("smaller: nonadjacent exons", 28, TEXT).move_to([2.9, -2.8, 0])
        sway_all(main, main_lab); sway_all(minor, minor_lab, seed=0.6)
        self.play(FadeIn(main, shift=LEFT * 0.2), run_time=0.9)
        self.at("main product")
        self.play(FadeIn(main_lab), Indicate(main[1], color=RED), run_time=0.9)
        self.at("smaller amount")
        self.play(FadeIn(minor, shift=LEFT * 0.2), FadeIn(minor_lab), run_time=0.9)
        self.at("more than one way")
        self.play(Indicate(main, scale_factor=1.03), Indicate(minor, scale_factor=1.03), run_time=1.1)
        self.finish()


class S05Ruler(SpokenScene):
    def construct(self):
        coding = VGroup(exon(4.1, -3.45, 1.2), exon(2.7, 0, 1.2), exon(4.1, 3.45, 1.2))
        ruler = triplet_ruler(y=-0.35, start=-5.4, count=12, cell=0.9)
        marker = reading_marker(-5.4, -0.35)
        self.play(GrowFromCenter(coding), run_time=0.8)
        alive(coding); alive(ruler.boxes, base=2.3, amp=1.0)
        sway(coding); sway_all(ruler.boxes, ruler.letters, marker, seed=0.4)
        self.at("groups called codons")
        self.play(LaggedStart(*[Create(b) for b in ruler.boxes], lag_ratio=0.05), FadeIn(ruler.letters), run_time=1.5)
        self.add(marker)
        self.play(marker.animate.shift(RIGHT * 3.55), run_time=2.0, rate_func=linear)
        self.at("Changing the length")
        self.play(coding[1].animate.shift(UP * 0.35).set_stroke(WHITE, width=4), run_time=0.8)
        self.at("every downstream group")
        downstream = VGroup(*ruler.boxes[6:])
        self.play(downstream.animate.set_stroke(GOLD, width=4).set_fill(GOLD, opacity=0.12), marker.animate.shift(RIGHT * 4.0), run_time=2.0)
        self.at("every later codon boundary")
        self.play(LaggedStart(*[Indicate(b, color=GOLD, scale_factor=1.03) for b in ruler.boxes[6:]], lag_ratio=0.08), run_time=1.4)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = predict_world(question=False)
        self.play(FadeIn(VGroup(w[0], w[1], w[2])), run_time=0.7)
        alive(VGroup(w[0], w[2])); alive(w.ruler.boxes, base=2.3, amp=1.0)
        sway_all(w[0], w[1], w[2], w[3], w[4], w[6])
        self.at("outlined exon")
        self.play(FadeIn(w.chosen, shift=UP * 0.15), FadeIn(w[5]), run_time=0.8)
        self.at("complete codon groups")
        self.play(FadeIn(w.ruler), FadeIn(w.marker), run_time=1.2)
        self.at("Imagine that splicing skips it")
        self.play(w.chosen.animate.shift(UP * 0.25), run_time=0.7)
        self.at("Will the downstream groups stay aligned")
        q = question_card("Do downstream triplets stay aligned?", y=-3.15, max_w=10.2)
        self.play(FadeIn(q), run_time=0.8)
        bob(w.marker, amp=0.06, speed=2.2)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Do downstream triplets stay aligned?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "max_w": 10.2}

    def backdrop(self):
        w = predict_world(question=False)
        bob(w.marker, amp=0.06, speed=2.2)
        alive(VGroup(w[0], w[2])); alive(w.ruler.boxes, base=2.3, amp=1.0)
        sway_all(w[0], w[1], w[2], w[3], w[4])
        return w


class S08Reveal(SpokenScene):
    def construct(self):
        w = predict_world(question=False)
        self.add(w)
        alive(VGroup(w[0], w[2])); alive(w.ruler.boxes, base=2.3, amp=1.0)
        sway_all(w[0], w[1], w[2], w[3], w[4], w[6])
        self.at("They stay aligned")
        self.play(FadeOut(VGroup(w.chosen, w[5]), shift=UP * 0.35), run_time=0.75)
        self.play(w[0].animate.shift(RIGHT * 1.35), w[2].animate.shift(LEFT * 1.35), FadeOut(w[1]), run_time=1.0)
        self.at("Whole triplets leave")
        bracket = BraceBetweenPoints([-5.25, -1.15, 0], [5.3, -1.15, 0], DOWN, color=GREEN)
        aligned = T("aligned", 32, GREEN).next_to(bracket, DOWN, buff=0.14)
        self.play(GrowFromCenter(bracket), FadeIn(aligned), w.marker.animate.shift(RIGHT * 4.0), run_time=1.5)
        self.at("next base begins a codon normally")
        self.play(w.marker.animate.shift(RIGHT * 3.5), run_time=1.6, rate_func=linear)
        self.at("new junction can still matter")
        junction = Dot([0, 0.75, 0], radius=0.14, color=TEAL)
        q = T("?  sequence still matters", 30, TEXT).move_to([0, 2.25, 0])
        self.play(FadeIn(junction, scale=1.5), FadeIn(q), run_time=0.8)
        pulse(junction, base=5, amp=2, speed=3)
        self.finish()


class S09Shift(SpokenScene):
    def construct(self):
        left = exon(2.6, -4.15, 0.9)
        chosen = exon(3.05, -1.15, 1.85, outline=WHITE, opacity=0.36)
        right = exon(5.2, 3.15, 0.9)
        ruler = triplet_ruler(y=-0.55, start=-5.4, count=12, cell=0.9)
        marker = reading_marker(-5.4, -0.55)
        lab = boxed_label("10 coding nucleotides", WHITE, size=28).move_to([-1.15, 3.18, 0])
        leftover = Rectangle(width=0.3, height=0.58, color=WHITE, stroke_width=3).move_to([0.85, 1.85, 0])
        self.play(FadeIn(VGroup(left, chosen, right, ruler, marker, lab)), run_time=0.9)
        alive(VGroup(left, chosen, right)); alive(ruler.boxes, base=2.3, amp=1.0)
        sway_all(left, chosen, right, ruler.boxes, ruler.letters, marker, leftover)
        self.at("one extra base")
        self.play(FadeIn(leftover), Indicate(leftover, color=WHITE), run_time=0.8)
        self.at("Every downstream boundary shifts")
        shifted = triplet_ruler(y=-0.55, start=-5.4, count=12, cell=0.9, shift=0.3, color=GOLD)
        self.play(FadeOut(VGroup(chosen, lab, leftover), shift=UP * 0.25), run_time=0.6)
        self.play(Transform(ruler, shifted), left.animate.shift(RIGHT * 1.1), right.animate.shift(LEFT * 1.1), run_time=1.3)
        self.at("different base groups")
        self.play(marker.animate.shift(RIGHT * 7.0), run_time=2.0, rate_func=linear)
        self.at("premature stop becomes likely")
        stop = RegularPolygon(n=8, color=RED, fill_color=RED, fill_opacity=0.22, stroke_width=3).scale(0.42).move_to([2.0, 2.35, 0])
        qm = T("?", 32, TEXT, weight=BOLD).move_to(stop)
        self.play(FadeIn(VGroup(stop, qm)), run_time=0.6)
        self.play(VGroup(stop, qm).animate.shift(RIGHT * 2.2), run_time=1.6, rate_func=there_and_back)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        left = exon(2.0, -5.15, 0.8, outline=GREY, fill=GREY, opacity=0.2)
        coding = exon(7.4, -0.15, 0.8)
        right = exon(1.6, 4.85, 0.8, outline=GREY, fill=GREY, opacity=0.2)
        self.play(FadeIn(VGroup(left, coding, right)), run_time=0.7)
        alive(VGroup(left, coding, right))
        sway_all(left, coding, right)
        coding_brace = Brace(coding, UP, color=BLUE)
        coding_lab = T("coding sequence", 30, BLUE).next_to(coding_brace, UP, buff=0.12)
        untranslated = VGroup(T("untranslated", 28, GREY).next_to(left, DOWN, buff=0.25), T("untranslated", 28, GREY).next_to(right, DOWN, buff=0.25))
        self.at("inside coding sequence")
        self.play(GrowFromCenter(coding_brace), FadeIn(coding_lab), FadeIn(untranslated), run_time=1.0)
        ruler = triplet_ruler(y=-0.55, start=-3.8, count=8, cell=0.9)
        alive(ruler.boxes, base=2.3, amp=1.0)
        sway_all(ruler.boxes, ruler.letters, seed=0.5)
        self.play(FadeIn(ruler), run_time=1.0)
        self.at("does not predict effects")
        self.play(Indicate(untranslated, color=GREY, scale_factor=1.05), run_time=0.8)
        self.at("cannot tell whether")
        tags = VGroup(*[boxed_label(t, GREY, size=28) for t in ("export?", "decay?", "translation?")]).arrange(RIGHT, buff=0.35).move_to([0, -2.35, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in tags], lag_ratio=0.25), run_time=1.3)
        self.at("evidence beyond")
        self.play(LaggedStart(*[Indicate(t, color=GREY, scale_factor=1.04) for t in tags], lag_ratio=0.2), run_time=1.1)
        self.finish()


class S11Rules(SpokenScene):
    def construct(self):
        msg = finished_message(y=1.35, scale=1.02)
        self.play(FadeIn(msg), run_time=0.8)
        alive(msg.blocks)
        sway_all(msg.cap, msg.blocks, msg.joins, msg.tail, msg.arcs)
        self.at("marks transcript ends")
        self.play(Indicate(VGroup(msg.cap, msg.tail), color=GOLD), run_time=0.9)
        self.at("segments join")
        self.play(LaggedStart(*[Indicate(j, color=TEAL, scale_factor=1.2) for j in msg.joins], lag_ratio=0.2), run_time=1.0)
        ruler = triplet_ruler(y=-0.25, start=-5.4, count=12, cell=0.9)
        alive(ruler.boxes, base=2.3, amp=1.0)
        sway_all(ruler.boxes, ruler.letters, seed=0.5)
        marker = reading_marker(-5.4, -0.25)
        self.at("keep a second rule")
        self.play(FadeIn(ruler), FadeIn(marker), run_time=1.0)
        rule1 = caption("Processing marks the ends and chooses the joins.", size=30, color=TEXT, y=-2.65)
        self.play(FadeIn(rule1), run_time=0.7)
        self.at("Coding length changes")
        rule2 = caption("Coding-length changes keep the downstream frame\nonly in multiples of three.", size=30, color=GREEN, y=-2.65)
        self.play(swap(rule1, rule2), marker.animate.shift(RIGHT * 4.0), run_time=1.4)
        self.at("only when the changed nucleotides are coding")
        coding = BraceBetweenPoints([-4.0, -0.85, 0], [4.0, -0.85, 0], DOWN, color=BLUE)
        self.play(GrowFromCenter(coding), marker.animate.shift(RIGHT * 3.8), run_time=1.4)
        self.at("Sequence decides")
        self.play(LaggedStart(*[Indicate(b, color=GOLD, scale_factor=1.03) for b in ruler.boxes], lag_ratio=0.04), run_time=1.3)
        self.at("scope of this rule")
        self.play(Indicate(rule2, color=GREEN, scale_factor=1.03), run_time=0.9)
        bob(msg.blocks, amp=0.035, speed=1.5)
        self.finish()


class S12End(EndCard):
    LINE = "Coding-length changes keep the downstream frame only in multiples of three."
