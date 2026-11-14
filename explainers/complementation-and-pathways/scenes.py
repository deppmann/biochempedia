"""When Two Mutants Rescue Each Other.

COLOR MAP
  BLUE   gene A and its function
  GOLD   gene B and its function
  GREEN  observed rescue / working result
  RED    a tested break or failure
  GREY   inactive context, chromosomes, and position marks
  EYE_RED the ordinary red-eye phenotype

The chromosome/cell picture is rebuilt through shared builder functions so every
carried landmark stays at exactly the same scale and position.
"""
from bp_parts import *


EYE_RED = "#B5304A"
PALE = "#F2F2F2"
CELL_CENTER = np.array([0.0, 0.15, 0.0])
CHR_Y = (1.15, -0.35)
GENE_X = {"A": -2.45, "B": 2.45}


def eye(kind="white", radius=0.72):
    """A schematic fly eye/readout, not an anatomical drawing."""
    fill = EYE_RED if kind == "red" else PALE
    outer = Ellipse(width=2.0 * radius, height=1.45 * radius, color=GREY,
                    stroke_width=4, fill_color=fill, fill_opacity=1)
    pupil = Circle(radius=0.23 * radius, stroke_width=0, fill_color=BG,
                   fill_opacity=1).move_to(outer)
    shine = Dot(radius=0.07 * radius, color=PALE).move_to(
        outer.get_center() + LEFT * 0.18 * radius + UP * 0.14 * radius)
    return VGroup(outer, pupil, shine)


def eye_fill(e, kind):
    return e[0].animate.set_fill(EYE_RED if kind == "red" else PALE, 1)


def xmark(center, size=0.27, color=RED, width=6):
    c = np.array(center)
    return VGroup(
        Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=width),
        Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=width),
    )


def gene_block(gene, state="working", center=ORIGIN, allele=None):
    """Gene label on the left; a break mark gets its own clear bay on the right."""
    col = BLUE if gene == "A" else GOLD
    box = RoundedRectangle(corner_radius=0.14, width=2.8, height=1.02,
                           stroke_color=col, stroke_width=4, fill_color=BG,
                           fill_opacity=0.96)
    label = T(allele or f"gene {gene}", 36, col, weight=BOLD).move_to(box).shift(LEFT * 0.38)
    mark = xmark(box.get_center() + RIGHT * 1.0, 0.20).set_opacity(1 if state == "broken" else 0)
    glow = SurroundingRectangle(box, color=GREEN, buff=0.08, stroke_width=4,
                                fill_opacity=0).set_stroke(opacity=0)
    g = VGroup(box, label, mark, glow).move_to(center)
    g.box, g.label, g.mark, g.glow = box, label, mark, glow
    return g


def chromosome(y, a="working", b="working", allele_a=None, allele_b=None):
    # Three rail segments meet the gene blocks without running behind their labels.
    bar = VGroup(
        Line([-5.25, y, 0], [-4.05, y, 0], color=GREY, stroke_width=14),
        Line([-0.85, y, 0], [0.85, y, 0], color=GREY, stroke_width=14),
        Line([4.05, y, 0], [5.25, y, 0], color=GREY, stroke_width=14),
    )
    ga = gene_block("A", a, [GENE_X["A"], y, 0], allele_a)
    gb = gene_block("B", b, [GENE_X["B"], y, 0], allele_b)
    return VGroup(bar, ga, gb)


def diploid_world(states=(("broken", "working"), ("working", "broken")),
                  eye_kind="white", eye_y=-2.82, show_scope=True):
    """The carried trans-test world used from s04 through s07."""
    cell = RoundedRectangle(corner_radius=0.42, width=12.2, height=4.65,
                            stroke_color=GREY, stroke_width=3, fill_color=GREY,
                            fill_opacity=0.20).move_to([0, 0.25, 0])
    top = chromosome(CHR_Y[0], *states[0])
    bottom = chromosome(CHR_Y[1], *states[1])
    readout = eye(eye_kind, 0.78).move_to([0, eye_y, 0])
    g = VGroup(cell, top, bottom, readout)
    if show_scope:
        g.add(scope_tag("schematic"))
    g.cell, g.top, g.bottom, g.eye = cell, top, bottom, readout
    return g


def unresolved_world(question=True):
    w = diploid_world()
    q = T("Recover or stay white?", 36, GOLD, weight=BOLD).move_to([0, 3.25, 0])
    if question:
        w.add(q)
    w.question = q
    return w


def pathway_block(text, center, color=GREY, active=False, width=2.55):
    box = RoundedRectangle(corner_radius=0.15, width=width, height=0.98,
                           stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.28 if active else 0.08)
    lab = fit_text(text, max_w=width - 0.35, size=28, color=color,
                   min_size=24, max_lines=2).move_to(box)
    return VGroup(box, lab).move_to(center)


def pathway_world(a_active=False, b_active=False, eye_kind="white", fail_a=False,
                  same_gene=False):
    """Carried functional pathway for the reveal and same-gene reset."""
    cell = RoundedRectangle(corner_radius=0.42, width=12.2, height=5.55,
                            stroke_color=GREY, stroke_width=3, fill_color=GREY,
                            fill_opacity=0.20).move_to([0, 0.1, 0])
    a = pathway_block("A function", [-3.75, 0.35, 0], BLUE, a_active)
    b = pathway_block("B function", [0, 0.35, 0], GOLD, b_active)
    out = pathway_block("red pigment", [3.75, 0.35, 0], GREEN,
                        a_active and b_active)
    ar1 = Arrow(a.get_right() + RIGHT * 0.08, b.get_left() + LEFT * 0.08,
                buff=0, color=GREEN if a_active else GREY, stroke_width=7, tip_length=0.22)
    ar2 = Arrow(b.get_right() + RIGHT * 0.08, out.get_left() + LEFT * 0.08,
                buff=0, color=GREEN if a_active and b_active else GREY,
                stroke_width=7, tip_length=0.22)
    if fail_a:
        stop = xmark([-2.26, 0.35, 0], 0.23)
    else:
        stop = VGroup()
    e = eye(eye_kind, 0.8).move_to([0, -2.0, 0])
    chr_pair = (VGroup(
        chromosome(2.18, "broken", "working"),
        chromosome(1.18, "broken", "working"),
    ) if same_gene else VGroup(
        chromosome(2.18, "broken", "working"),
        chromosome(1.18, "working", "broken"),
    )).scale(0.62).move_to([0, 2.02, 0])
    g = VGroup(cell, chr_pair, a, b, out, ar1, ar2, stop, e, scope_tag("schematic"))
    g.cell, g.chromosomes, g.a, g.b, g.out = cell, chr_pair, a, b, out
    g.ar1, g.ar2, g.stop, g.eye = ar1, ar2, stop, e
    return g


def function_token(letter, color, at):
    return chip(f"{letter} function", color, size=26, pad=0.18).move_to(at)


def exception_card(text, at):
    label = T(f"EXCEPTION\n{text}", 24, RED, weight=BOLD,
              line_spacing=0.8)
    box = RoundedRectangle(corner_radius=0.18, width=4.1, height=1.35,
                           stroke_color=RED, stroke_width=3, fill_color=BG,
                           fill_opacity=0.92)
    label.move_to(box)
    return VGroup(box, label).move_to(at)


class S01Hook(SpokenScene):
    def construct(self):
        left = eye("white", 1.05).move_to([-4.6, 2.25, 0])
        right = eye("white", 1.05).move_to([4.6, 2.25, 0])
        child = eye("white", 0.88).move_to([0, 2.35, 0])
        cross = T("?", 48, GOLD, weight=BOLD).move_to([0, 3.37, 0])
        cell = RoundedRectangle(corner_radius=0.42, width=9.8, height=3.45,
                                stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                fill_opacity=0.20).move_to([0, -0.75, 0])
        top = chromosome(-0.25, "broken", "working").scale(0.72).shift(LEFT * 1.0)
        bottom = chromosome(-1.35, "working", "broken").scale(0.72).shift(RIGHT * 1.0)
        motes = VGroup(*[Dot(radius=0.035, color=GREY).set_opacity(0.35).move_to(
            [-3.8 + 0.7 * i, -2.0 + 0.28 * (i % 4), 0]) for i in range(12)])
        bob(motes, amp=0.06, speed=1.1)
        bob(child, amp=0.055, speed=1.35, seed=2)
        self.add(motes)
        self.play(FadeIn(left, scale=0.85), FadeIn(right, scale=0.85),
                  FadeIn(child), FadeIn(cross), run_time=1.5)
        self.play(Indicate(left, color=TEXT, scale_factor=1.08),
                  Indicate(right, color=TEXT, scale_factor=1.08), run_time=1.3)
        self.at("Watch their chromosome")
        self.play(Create(cell), run_time=0.8)
        self.play(top.animate.shift(RIGHT * 1.0), bottom.animate.shift(LEFT * 1.0), run_time=2.0)
        self.at("Each parent carries")
        self.play(Indicate(top[1], color=RED, scale_factor=1.08),
                  Indicate(bottom[2], color=RED, scale_factor=1.08), run_time=1.6)
        self.at("The offspring eye")
        self.play(Indicate(child, color=PALE, scale_factor=1.08), run_time=1.3)
        self.at("normal function returns")
        self.play(Flash(child, color=GOLD, flash_radius=1.15, line_length=0.18), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S02ManyCauses(SpokenScene):
    def construct(self):
        heading = T("One white eye, several possible breaks", 36, TEXT).move_to([0, 3.3, 0])
        redp = pathway_block("red pigment", [-4.7, 1.3, 0], GREY)
        brownp = pathway_block("brown pigment", [-4.7, -0.45, 0], GREY)
        transport = pathway_block("shared transporter", [-0.7, 0.45, 0], GREY, width=3.2)
        granule = Circle(radius=0.82, color=GREY, stroke_width=4,
                         fill_color=EYE_RED, fill_opacity=0.85).move_to([2.55, 0.45, 0])
        glab = T("granule", 28, TEXT).move_to(granule)
        e = eye("red", 0.78).move_to([5.15, 0.45, 0])
        bob(e, amp=0.055, speed=1.3, seed=1)
        a1 = Arrow(redp.get_right(), transport.get_left() + UP * 0.18, buff=0.14,
                   color=GREY, stroke_width=5, tip_length=0.2)
        a2 = Arrow(brownp.get_right(), transport.get_left() + DOWN * 0.18, buff=0.14,
                   color=GREY, stroke_width=5, tip_length=0.2)
        a3 = Arrow(transport.get_right(), granule.get_left(), buff=0.12,
                   color=GREY, stroke_width=5, tip_length=0.2)
        a4 = Arrow(granule.get_right(), e.get_left(), buff=0.12,
                   color=GREY, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(heading), run_time=0.7)
        self.play(LaggedStart(FadeIn(redp), FadeIn(brownp), FadeIn(transport),
                              FadeIn(granule), FadeIn(glab), FadeIn(e),
                              lag_ratio=0.16), run_time=2.7)
        self.at("Some genes make pigments")
        self.play(Create(a1), Create(a2),
                  Indicate(VGroup(redp, brownp), color=TEXT, scale_factor=1.04), run_time=1.2)
        self.at("Others move pigments")
        self.play(Create(a3), Create(a4),
                  Indicate(VGroup(transport, granule, glab, e), color=TEXT,
                           scale_factor=1.035), run_time=1.5)
        self.at("A missing shared transporter")
        tx = Line(transport.get_right() + RIGHT * 0.12 + UP * 0.42,
                  transport.get_right() + RIGHT * 0.12 + DOWN * 0.42,
                  color=RED, stroke_width=9)
        self.play(Create(tx), transport[0].animate.set_stroke(RED),
                  granule.animate.set_fill(GREY, 0.12), eye_fill(e, "white"), run_time=1.7)
        self.at("So does blocking")
        self.play(FadeOut(tx), transport[0].animate.set_stroke(GREY), run_time=0.45)
        x1 = Line(redp.get_right() + RIGHT * 0.12 + UP * 0.42,
                  redp.get_right() + RIGHT * 0.12 + DOWN * 0.42,
                  color=RED, stroke_width=9)
        x2 = Line(brownp.get_right() + RIGHT * 0.12 + UP * 0.42,
                  brownp.get_right() + RIGHT * 0.12 + DOWN * 0.42,
                  color=RED, stroke_width=9)
        self.play(Create(x1), Create(x2),
                  Indicate(VGroup(redp, brownp), color=RED, scale_factor=1.045),
                  run_time=1.25)
        self.at("Appearance alone")
        note = caption("The phenotype does not identify the broken gene.", color=GOLD)
        self.play(FadeIn(note), Indicate(e, color=PALE, scale_factor=1.08), run_time=1.4)
        self.add(scope_tag("schematic"))
        self.finish()


class S02Terms(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.42, width=12.1, height=5.55,
                                stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                fill_opacity=0.20).move_to([0, 0.05, 0])
        c1 = chromosome(1.35, "working", "working", allele_a="A¹")
        c2 = chromosome(-0.15, "broken", "working", allele_a="a²")
        allele_labs = VGroup(T("allele", 30, BLUE), T("allele", 30, BLUE))
        allele_labs[0].next_to(c1[1], UP, buff=0.2)
        allele_labs[1].next_to(c2[1], DOWN, buff=0.2)
        site = RoundedRectangle(corner_radius=0.18, width=2.8, height=1.05,
                                stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                                fill_opacity=0.12).move_to([3.75, -2.05, 0])
        site_lab = T("normal site", 28, BLUE).move_to(site)
        token = function_token("A", BLUE, [-4.45, -1.55, 0])
        bob(c1[1], amp=0.05, speed=1.2, seed=1)
        enough = T("enough from one copy", 30, GREEN).next_to(site, LEFT, buff=0.45)
        self.play(Create(cell), run_time=0.7)
        self.play(FadeIn(c1[1]), FadeIn(c2[1]), run_time=1.1)
        self.at("An allele is")
        self.play(FadeIn(allele_labs), run_time=1.2)
        self.at("A diploid cell")
        self.play(FadeIn(c1[0]), FadeIn(c1[2]), FadeIn(c2[0]), FadeIn(c2[2]), run_time=1.8)
        self.at("For a recessive loss")
        self.play(Indicate(c1[1], color=BLUE, scale_factor=1.055), run_time=1.25)
        self.at("one working allele")
        self.play(FadeIn(token, scale=0.8), run_time=0.8)
        self.play(FadeIn(site), FadeIn(site_lab),
                  token.animate.move_to(site.get_center() + UP * 1.0), run_time=2.0)
        self.at("That product works")
        self.play(FadeIn(enough), Indicate(site, color=BLUE, scale_factor=1.06), run_time=1.5)
        self.add(scope_tag("schematic"))
        self.finish()


class S03CheckRecessive(SpokenScene):
    def construct(self):
        w = diploid_world(states=(("broken", "working"), ("working", "working")))
        bob(w.eye, amp=0.055, speed=1.25, seed=2)
        working = SurroundingRectangle(w.bottom[1], color=GREEN, buff=0.10, stroke_width=5)
        self.play(FadeIn(w.cell), FadeIn(w.top), FadeIn(w.bottom), FadeIn(w.eye), run_time=1.6)
        self.at("If a working copy")
        self.play(Create(working), eye_fill(w.eye, "red"), run_time=1.7)
        rec = chip("recessive", GREEN, size=30).move_to([3.85, -2.55, 0])
        self.play(FadeIn(rec, scale=0.85), run_time=0.8)
        self.at("That check matters")
        self.play(Indicate(VGroup(working, w.eye), color=GREEN, scale_factor=1.04), run_time=1.5)
        self.at("A dominant mutation")
        dom = pathway_block("dominant effect", w.top[1].get_center(), RED, width=2.55)
        self.play(FadeOut(working), FadeOut(rec), FadeOut(w.top[1]), FadeIn(dom),
                  eye_fill(w.eye, "white"), run_time=1.4)
        unin = chip("test uninformative", RED, size=28).move_to([3.7, -2.55, 0])
        self.play(FadeIn(unin), run_time=1.0)
        self.finish()


class S04Trans(SpokenScene):
    def construct(self):
        w = diploid_world()
        bob(w.eye, amp=0.055, speed=1.25, seed=3)
        self.play(FadeIn(w.cell), run_time=0.6)
        self.play(FadeIn(w.top[0]), FadeIn(w.bottom[0]), run_time=1.0)
        self.at("opposite chromosome copies")
        self.play(LaggedStart(FadeIn(w.top[1]), FadeIn(w.top[2]),
                              FadeIn(w.bottom[1]), FadeIn(w.bottom[2]), lag_ratio=0.18), run_time=2.0)
        self.at("This arrangement is trans")
        trans = chip("trans", TEXT, size=32).move_to([0, 3.25, 0])
        self.play(FadeIn(trans, scale=0.8), run_time=1.1)
        self.at("One chromosome has")
        self.play(Indicate(w.top, color=GOLD, scale_factor=1.035), run_time=1.5)
        self.at("The other has")
        self.play(Indicate(w.bottom, color=BLUE, scale_factor=1.035), run_time=1.5)
        self.play(FadeIn(w.eye), run_time=0.7)
        unresolved = T("unresolved", 28, GREY).next_to(w.eye, RIGHT, buff=0.35)
        self.play(FadeIn(unresolved), run_time=0.7)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        w = unresolved_world(question=False)
        bob(w.eye, amp=0.055, speed=1.25, seed=4)
        self.add(w)
        self.play(FadeIn(w.question, shift=DOWN * 0.12), run_time=1.0)
        self.play(Indicate(w.eye, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.at("Follow the working copies")
        pulse(w.top[2], base=4.5, amp=1.8, speed=2.0)
        pulse(w.bottom[1], base=4.5, amp=1.8, speed=2.0)
        self.play(Indicate(w.top[2], color=GOLD, scale_factor=1.06),
                  Indicate(w.bottom[1], color=BLUE, scale_factor=1.06), run_time=1.7)
        self.at("Decide whether")
        self.play(Circumscribe(VGroup(w.top[2], w.bottom[1]), color=GREEN,
                               fade_out=True), run_time=1.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Recover or stay white?"
    SECONDS = 4.5
    CARD = {"y": 3.30, "size": 36, "max_w": 8.5}
    RING_AT = (5.85, -3.05, 0)

    def backdrop(self):
        w = diploid_world(show_scope=False)
        bob(w.eye, amp=0.055, speed=1.25, seed=4)
        pulse(w.top[2], base=4.5, amp=1.8, speed=2.0)
        pulse(w.bottom[1], base=4.5, amp=1.8, speed=2.0)
        return w


class S06Reveal(SpokenScene):
    def construct(self):
        w = pathway_world(False, False, "white")
        bob(w.eye, amp=0.055, speed=1.25, seed=5)
        self.add(w)
        ta = function_token("A", BLUE, [-5.0, -1.3, 0])
        tb = function_token("B", GOLD, [2.0, -1.3, 0])
        self.play(FadeIn(ta, scale=0.8), run_time=0.7)
        self.play(ta.animate.move_to([-3.75, -0.9, 0]),
                  w.a[0].animate.set_fill(BLUE, 0.28), run_time=1.5)
        self.at("The working B copy")
        self.play(FadeIn(tb, scale=0.8), run_time=0.7)
        self.play(tb.animate.move_to([0, -0.9, 0]),
                  w.b[0].animate.set_fill(GOLD, 0.28), run_time=1.5)
        self.at("With both functions")
        self.play(FadeOut(ta), FadeOut(tb), w.ar1.animate.set_color(GREEN),
                  w.ar2.animate.set_color(GREEN), w.out[0].animate.set_fill(GREEN, 0.28),
                  run_time=2.0)
        self.play(eye_fill(w.eye, "red"), run_time=1.0)
        self.at("Normal function returns")
        comp = chip("complement", GREEN, size=34).move_to([3.9, -2.2, 0])
        self.play(FadeIn(comp, scale=0.75), Indicate(w.eye, color=GREEN, scale_factor=1.08), run_time=1.5)
        self.finish()


class S07SameGene(SpokenScene):
    def construct(self):
        old = pathway_world(True, True, "red")
        bob(old.eye, amp=0.055, speed=1.25, seed=6)
        answer = chip("complement", GREEN, size=34).move_to([3.9, -2.2, 0])
        self.add(old, answer)
        self.play(FadeOut(answer), FadeOut(old), run_time=0.7)
        w = pathway_world(False, True, "white", fail_a=True, same_gene=True)
        bob(w.eye, amp=0.055, speed=1.25, seed=7)
        bob(w.chromosomes, amp=0.045, speed=1.1, seed=3)
        self.play(FadeIn(w), run_time=1.3)
        self.at("Now both chromosomes")
        self.play(Indicate(w.chromosomes[0][1], color=RED, scale_factor=1.06),
                  Indicate(w.chromosomes[1][1], color=RED, scale_factor=1.06), run_time=1.7)
        self.at("No working A product")
        gold = function_token("B", GOLD, [2.0, -1.3, 0])
        self.play(FadeIn(gold), gold.animate.move_to([0, -0.9, 0]),
                  w.b[0].animate.set_fill(GOLD, 0.28), run_time=1.8)
        self.play(Indicate(w.a, color=RED, scale_factor=1.06), run_time=0.8)
        self.at("The eye stays white")
        fail = chip("fail to complement", RED, size=32).move_to([3.8, -2.2, 0])
        self.play(FadeOut(gold), FadeIn(fail, scale=0.8),
                  Indicate(w.eye, color=RED, scale_factor=1.06), run_time=1.5)
        self.finish()


class S08Groups(SpokenScene):
    def construct(self):
        pts = [np.array([-4.8, 1.7, 0]), np.array([-3.3, 0.15, 0]), np.array([-4.8, -1.4, 0]),
               np.array([1.7, 1.7, 0]), np.array([3.3, 0.15, 0]), np.array([1.7, -1.4, 0])]
        dots = VGroup(*[Circle(radius=0.34, color=GREY, stroke_width=4,
                              fill_color=GREY, fill_opacity=0.20).move_to(p) for p in pts])
        bob(dots, amp=0.05, speed=1.15, seed=2)
        self.play(LaggedStart(*[FadeIn(d, scale=0.7) for d in dots], lag_ratio=0.15), run_time=1.8)
        self.at("form a complementation group")
        left_links = VGroup(Line(pts[0], pts[1], color=RED, stroke_width=5),
                            Line(pts[1], pts[2], color=RED, stroke_width=5))
        right_links = VGroup(Line(pts[3], pts[4], color=RED, stroke_width=5),
                             Line(pts[4], pts[5], color=RED, stroke_width=5))
        self.play(Create(left_links), Create(right_links), run_time=1.6)
        self.at("In the simple model")
        left_group = RoundedRectangle(corner_radius=0.35, width=3.0, height=4.15,
                                      color=BLUE, stroke_width=5, fill_color=BLUE,
                                      fill_opacity=0.12).move_to([-4.05, 0.15, 0])
        right_group = RoundedRectangle(corner_radius=0.35, width=3.0, height=4.15,
                                       color=GOLD, stroke_width=5, fill_color=GOLD,
                                       fill_opacity=0.12).move_to([2.5, 0.15, 0])
        self.play(Create(left_group), Create(right_group), run_time=1.8)
        self.at("Testing many pairs")
        sweep = Line([-5.8, 2.55, 0], [4.3, 2.55, 0], color=GREEN, stroke_width=5)
        self.play(sweep.animate.shift(DOWN * 4.8), run_time=2.7, rate_func=linear)
        self.play(FadeOut(sweep), FadeOut(left_links), FadeOut(right_links), run_time=0.5)
        self.at("revealing how many functions")
        cap = caption("at least this many genes", color=GREEN)
        self.play(FadeIn(cap), Indicate(VGroup(left_group, right_group), color=GREEN,
                                        scale_factor=1.025), run_time=1.5)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Scope(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.35, width=8.0, height=4.15,
                                stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                fill_opacity=0.20).move_to([0, 0.05, 0])
        bars = VGroup(*[
            VGroup(Line([-3.4, y, 0], [-3.12, y, 0], color=GREY, stroke_width=14),
                   Line([-0.15, y, 0], [0.15, y, 0], color=GREY, stroke_width=14),
                   Line([3.12, y, 0], [3.4, y, 0], color=GREY, stroke_width=14))
            for y in (0.9, -0.35)
        ])
        genes = VGroup(gene_block("A", "broken", [-1.65, 0.9, 0]),
                       gene_block("B", "working", [1.65, 0.9, 0]),
                       gene_block("A", "working", [-1.65, -0.35, 0]),
                       gene_block("B", "broken", [1.65, -0.35, 0]))
        center_eye = eye("red", 0.64).move_to([0, -1.45, 0])
        bob(center_eye, amp=0.055, speed=1.25, seed=8)
        center = VGroup(cell, bars, genes, center_eye)
        usual = chip("usual simple result", GREEN, size=30).move_to([4.15, -2.75, 0])
        self.play(FadeIn(center), FadeIn(usual), run_time=1.5)
        self.at("Introgenic complementation")
        left = exception_card("same gene may rescue", [-4.5, 3.0, 0])
        self.play(FadeIn(left, shift=RIGHT * 0.15), run_time=1.5)
        self.at("Mutations in different genes")
        right = exception_card("different genes may fail", [4.5, 3.0, 0])
        self.play(FadeIn(right, shift=LEFT * 0.15), run_time=1.5)
        self.at("Those exceptions refine")
        self.play(Indicate(VGroup(left, right), color=RED, scale_factor=1.025), run_time=1.5)
        self.at("They do not change")
        self.play(Indicate(usual, color=GREEN, scale_factor=1.08), run_time=1.8)
        self.finish()


class S09Readout(SpokenScene):
    def construct(self):
        panels = TwoPanel("function", "position", colors=(GREEN, GREY), top=3.0, bottom=-2.5)
        self.play(FadeIn(panels), run_time=1.2)
        e = eye("red", 1.15)
        rescue = chip("observed rescue", GREEN, size=30)
        left = VGroup(e, rescue).arrange(DOWN, buff=0.45)
        panels.put(left, "left")
        bob(left, amp=0.05, speed=1.15, seed=9)
        ticks = VGroup(
            Line([-2.2, 0, 0], [2.2, 0, 0], color=GREY, stroke_width=7),
            *[Line([x, -0.35, 0], [x, 0.35, 0], color=GREY, stroke_width=4)
              for x in (-1.45, -0.55, 0.35, 1.25)],
            T("chromosome positions", 28, GREY).move_to([0, -0.8, 0]),
        )
        panels.put(ticks, "right")
        self.at("A red eye is")
        self.play(FadeIn(left), run_time=1.4)
        self.play(Indicate(rescue, color=GREEN, scale_factor=1.08), run_time=1.0)
        self.at("Mapping asks")
        self.play(FadeIn(ticks, scale=0.90), run_time=1.3)
        divider = Line([0, 2.55, 0], [0, -2.05, 0], color=TEAL, stroke_width=5)
        self.play(Create(divider), run_time=0.7)
        self.at("Complimentation asks")
        focus = SurroundingRectangle(left, color=GREEN, buff=0.25, stroke_width=5)
        self.play(Create(focus), ticks.animate.set_opacity(0.35),
                  Indicate(left, color=GREEN, scale_factor=1.035), run_time=1.6)
        self.finish()


class S10End(EndCard):
    LINE = "For recessive mutants, rescue in trans usually means different genes."
