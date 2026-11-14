"""Which Part of DNA Is the Code?

COLOR MAP
  BLUE   sugar-phosphate sides / DNA
  YELLOW A/T base blocks
  GREEN  C/G base blocks
  TEAL   genes
  RED    proteins
  GOLD   traits
  GREY   counts, frames, and supporting marks
"""
from bp_parts import *


PURPLE = "#B58CD9"
BASE_COLOR = {"A": YELLOW, "T": YELLOW, "C": GREEN, "G": GREEN}
PAIR = {"A": "T", "T": "A", "C": "G", "G": "C"}
SEQ_A = "ATCGTA"
SEQ_B = "CGATGC"


def arrow(a, b, color=GREY, width=5, tip=0.2):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=width, tip_length=tip)


def base_block(letter, center=ORIGIN, width=0.82, height=0.48, size=30):
    color = BASE_COLOR[letter]
    box = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.64)
    label = T(letter, size, color, weight=BOLD).move_to(box)
    return VGroup(box, label).move_to(center)


def dna_ladder(sequence=SEQ_A, center=ORIGIN, width=3.4, height=5.0,
               block_width=1.25, block_height=0.56, label=False,
               rail_opacity=1.0):
    """The shared flat DNA picture; every continuing scene calls this builder."""
    cx, cy = center[0], center[1]
    left_x, right_x = cx - width / 2, cx + width / 2
    rail_l = Line([left_x, cy - height / 2, 0], [left_x, cy + height / 2, 0],
                  color=BLUE, stroke_width=10).set_opacity(rail_opacity)
    rail_r = rail_l.copy().shift(RIGHT * width)
    rails = VGroup(rail_l, rail_r)
    ys = np.linspace(cy + height * 0.39, cy - height * 0.39, len(sequence))
    pairs = VGroup()
    for y, letter in zip(ys, sequence):
        mate = PAIR[letter]
        left = base_block(letter, [cx - block_width / 2, y, 0], block_width, block_height)
        right = base_block(mate, [cx + block_width / 2, y, 0], block_width, block_height)
        join = Line(left.get_right(), right.get_left(), color=GREY, stroke_width=3)
        pairs.add(VGroup(join, left, right))
    g = VGroup(rails, pairs)
    g.rails, g.pairs = rails, pairs
    if label:
        lab = T("DNA", 30, BLUE, weight=BOLD).next_to(g, UP, buff=0.14)
        g.add(lab)
        g.label = lab
    return g


def twisted_ladder(sequence=SEQ_A, center=ORIGIN, width=3.6, height=5.0, label=False):
    """A computed sine-wave ladder, used only to show the twist named in narration."""
    cx, cy = center[0], center[1]
    ys = np.linspace(cy - height / 2, cy + height / 2, 100)
    phase = (ys - cy) / height * 2 * PI
    spread = width * (0.34 + 0.07 * np.cos(phase))
    left_pts = [np.array([cx - s, y, 0]) for s, y in zip(spread, ys)]
    right_pts = [np.array([cx + s, y, 0]) for s, y in zip(spread, ys)]
    l = VMobject(color=BLUE, stroke_width=10).set_points_as_corners(left_pts)
    r = VMobject(color=BLUE, stroke_width=10).set_points_as_corners(right_pts)
    rails = VGroup(l, r)
    pairs = VGroup()
    rung_ys = np.linspace(cy + height * 0.39, cy - height * 0.39, len(sequence))
    for y, letter in zip(rung_ys, sequence):
        ph = (y - cy) / height * 2 * PI
        half = width * (0.34 + 0.07 * np.cos(ph))
        bw = half - 0.18
        left = base_block(letter, [cx - bw / 2, y, 0], bw, 0.52, 28)
        right = base_block(PAIR[letter], [cx + bw / 2, y, 0], bw, 0.52, 28)
        pairs.add(VGroup(Line(left.get_right(), right.get_left(), color=GREY, stroke_width=3), left, right))
    g = VGroup(rails, pairs)
    g.rails, g.pairs = rails, pairs
    if label:
        lab = T("DNA", 30, BLUE, weight=BOLD).next_to(g, UP, buff=0.14)
        g.add(lab)
        g.label = lab
    return g


def strawberry(height=3.6):
    body = Polygon([-1.25, 0.85, 0], [1.25, 0.85, 0], [0.95, -0.45, 0],
                   [0, -1.6, 0], [-0.95, -0.45, 0],
                   color=RED, fill_color=RED, fill_opacity=0.82, stroke_width=4)
    leaves = VGroup(*[Triangle(color=GREEN, fill_color=GREEN, fill_opacity=0.85, stroke_width=0)
                      .scale(0.38).rotate(a).shift(UP * 0.95) for a in (-0.65, 0, 0.65)])
    seeds = VGroup(*[Dot([x, y, 0], radius=0.045, color=YELLOW)
                     for x, y in [(-.55,.35),(0,.5),(.55,.35),(-.75,-.2),(-.25,-.15),(.3,-.2),(.72,-.15),(0,-.75)]])
    g = VGroup(body, leaves, seeds)
    return g.set_height(height)


def person(height=3.6):
    head = Circle(radius=0.42, color=TEXT, fill_color=TEXT, fill_opacity=0.25).shift(UP * 1.35)
    torso = RoundedRectangle(corner_radius=0.25, width=1.35, height=1.65,
                             color=TEXT, fill_color=TEXT, fill_opacity=0.18).shift(UP * 0.15)
    limbs = VGroup(Line([-.48,.45,0],[-1.0,-.45,0]), Line([.48,.45,0],[1.0,-.45,0]),
                   Line([-.32,-.65,0],[-.55,-1.6,0]), Line([.32,-.65,0],[.55,-1.6,0])).set_stroke(TEXT, 8)
    return VGroup(limbs, torso, head).set_height(height)


def cell(kind, center, color=TEXT, radius=1.25):
    outline = Circle(radius=radius, color=color, stroke_width=5,
                     fill_color=color, fill_opacity=0.18).move_to(center)
    nucleus = Circle(radius=radius * 0.28, color=BLUE, stroke_width=3,
                     fill_color=BLUE, fill_opacity=0.16).move_to(np.array(center) + [.18,.12,0])
    label = T(kind, 28, color).next_to(outline, DOWN, buff=0.16)
    return VGroup(outline, nucleus, label)


def organism_icons():
    berry = strawberry(0.8)
    mushroom = VGroup(ArcBetweenPoints([-0.5,0,0],[0.5,0,0], angle=-PI, color=GOLD, stroke_width=8),
                      RoundedRectangle(corner_radius=.08, width=.24, height=.55,
                                       color=TEXT, fill_color=TEXT, fill_opacity=.25).shift(DOWN*.25))
    bacterium = RoundedRectangle(corner_radius=.35, width=1.0, height=.52,
                                  color=GREEN, fill_color=GREEN, fill_opacity=.15)
    human = person(0.9)
    return VGroup(berry, mushroom, bacterium, human).arrange(DOWN, buff=0.35)


def pair_bracket(target):
    return Brace(target, RIGHT, color=TEXT).set_stroke(width=4)


def glow_fill(mob, low=.18, high=.55, speed=1.5, seed=0):
    """A visible, gentle base-block glow for held ladder frames."""
    mob._glow_t = seed * .45

    def update(m, dt):
        m._glow_t += dt
        alpha = low + (high - low) * (.5 + .5 * np.sin(speed * m._glow_t))
        m.set_fill(opacity=alpha)
    return mob.add_updater(update)


def two_ladders_world(with_question=False):
    left = dna_ladder(SEQ_A, [-2.3, 0.1, 0], width=2.25, height=4.9,
                      block_width=.78, block_height=.50)
    right = dna_ladder(SEQ_B, [2.3, 0.1, 0], width=2.25, height=4.9,
                       block_width=.78, block_height=.50)
    reader = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=0).scale(.16).rotate(-PI/2)
    reader.next_to(left.pairs[0], LEFT, buff=.15)
    g = VGroup(left, right, reader)
    g.left_ladder, g.right_ladder, g.reader = left, right, reader
    if with_question:
        q = fit_text("Which carries different instructions: shared sides or changing base order?",
                     max_w=12.2, size=30, color=GOLD, max_lines=2).move_to([0, 3.35, 0])
        g.add(q)
        g.question = q
    return g


def sequence_strip(sequence=SEQ_A, center=(0, 0, 0), width=.86):
    blocks = VGroup(*[base_block(x, width=width, height=.58, size=30) for x in sequence])
    blocks.arrange(RIGHT, buff=.10).move_to(center)
    return blocks


def gene_strip(center=(-4.25, 0.4, 0), sequence=SEQ_A, scale=.82):
    blocks = sequence_strip(sequence, center, .72).scale(scale)
    brace = Brace(blocks, UP, color=TEAL)
    label = T("gene", 28, TEAL, weight=BOLD).next_to(brace, UP, buff=.08)
    return VGroup(blocks, brace, label)


def protein_block(text="protein", center=ORIGIN):
    p = chip(text, RED, size=30, fill_opacity=.42).move_to(center)
    return p


def flower(center=(4.6, 0, 0), petal_color=PURPLE, scale=1.0):
    petals = VGroup(*[Ellipse(width=.72, height=1.2, color=petal_color,
                              fill_color=petal_color, fill_opacity=.72, stroke_width=3)
                      .rotate(k * TAU / 5).shift(UP * .62).rotate(k * TAU / 5, about_point=ORIGIN)
                      for k in range(5)])
    core = Circle(radius=.28, color=GOLD, fill_color=GOLD, fill_opacity=.9)
    stem = Line([0,-.2,0],[0,-1.45,0], color=GREEN, stroke_width=7)
    leaf = Ellipse(width=.65, height=.3, color=GREEN, fill_color=GREEN, fill_opacity=.6).rotate(.45).shift([.35,-.85,0])
    return VGroup(stem, leaf, petals, core).scale(scale).move_to(center)


def pea_path(mutated=False, y=0.15):
    seq = "ATCGTA" if not mutated else "ATGGTA"
    gene = gene_strip([-4.4, y, 0], seq, .75)
    protein = protein_block("working protein" if not mutated else "protein stops", [0, y, 0])
    bloom = flower([4.45, y, 0], PURPLE if not mutated else TEXT, .8)
    a1 = arrow(gene.get_right(), protein.get_left(), GREY)
    a2 = arrow(protein.get_right(), bloom.get_left(), GREY if not mutated else RED)
    g = VGroup(gene, a1, protein, a2, bloom)
    g.gene, g.protein, g.bloom, g.a1, g.a2 = gene, protein, bloom, a1, a2
    return g


class S00Hook(SpokenScene):
    def construct(self):
        berry, student = strawberry(3.6).move_to([-3.8, 0, 0]), person(3.6).move_to([3.8, 0, 0])
        bob(berry, amp=.035, speed=1.4)
        bob(student, amp=.025, speed=1.2, seed=2)
        self.play(FadeIn(berry, shift=RIGHT*.2), FadeIn(student, shift=LEFT*.2), run_time=.9)
        self.at("use the same kind")
        dna_tags = VGroup(chip("DNA", BLUE, 30), chip("DNA", BLUE, 30))
        dna_tags[0].next_to(berry, DOWN, buff=.25); dna_tags[1].next_to(student, DOWN, buff=.25)
        self.play(FadeIn(dna_tags), run_time=.7)
        self.at("What inside")
        question = T("What carries the difference?", 38, GOLD, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.play(FadeIn(question, shift=DOWN*.1), run_time=.7)
        self.at("Both lead into cells")
        cells = VGroup(cell("strawberry cell", [-3.5, 0, 0], RED, 1.25),
                       cell("person cell", [3.5, 0, 0], TEXT, 1.25))
        self.play(FadeOut(dna_tags), ReplacementTransform(berry, cells[0]),
                  ReplacementTransform(student, cells[1]), run_time=1.2)
        self.at("toward the same twisting ladder")
        dna = twisted_ladder(SEQ_A, [0, -.15, 0], width=2.8, height=4.7)
        dna_lab = T("DNA (schematic)", 28, BLUE).next_to(dna, DOWN, buff=.12)
        small_cells = VGroup(cell("strawberry cell", [-4.4,0,0], RED, .72),
                             cell("person cell", [4.4,0,0], TEXT, .72))
        self.play(ReplacementTransform(cells, small_cells), FadeIn(dna, scale=.8), FadeIn(dna_lab), run_time=1.1)
        self.at("where differences sit")
        glow = SurroundingRectangle(dna.pairs, color=GOLD, buff=.12, stroke_width=4)
        self.play(Create(glow), run_time=.7)
        pulse(glow, base=4, amp=1.2, speed=2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "DNA: The Code of Life"
    TITLE = "Which Part of DNA Is the Code?"

    def construct(self):
        dna = twisted_ladder(SEQ_A, [0, -.25, 0], width=2.8, height=4.8)
        dna.set_opacity(.32)
        title = fit_text(self.TITLE, max_w=9.5, size=48, color=TEXT,
                         font=TITLE_FONT, max_lines=2).move_to([0, 2.9, 0])
        self.add(dna)
        self.play(FadeIn(title, shift=DOWN*.12), Rotate(dna, .12), run_time=.7)
        mark = T("?", 64, GOLD, weight=BOLD).next_to(dna, RIGHT, buff=.5)
        self.play(ReplacementTransform(title, mark), Rotate(dna, -.18), run_time=.8)
        self.finish()


class S02SharedParts(SpokenScene):
    def construct(self):
        twist = twisted_ladder(SEQ_A, [0, -.05, 0], width=3.9, height=5.4)
        flat = dna_ladder(SEQ_A, [0, -.05, 0], width=3.9, height=5.4,
                          block_width=1.42, block_height=.62)
        self.add(twist, scope_tag("schematic"))
        self.at("like a ladder")
        self.play(ReplacementTransform(twist, flat), run_time=1.1)
        self.at("Sugar and phosphate")
        rails_label = T("sugar + phosphate", 30, BLUE, weight=BOLD).next_to(flat, LEFT, buff=.5)
        self.play(FadeIn(rails_label), *[Indicate(r, color=BLUE, scale_factor=1.03) for r in flat.rails], run_time=1.0)
        self.at("same kinds in every")
        icons = organism_icons().move_to([4.7, 0, 0])
        self.play(FadeIn(icons[0]), run_time=.35)
        self.play(FadeIn(icons[1]), run_time=.35)
        self.play(FadeIn(icons[2]), run_time=.35)
        self.play(FadeIn(icons[3]), run_time=.35)
        shared = T("shared sides", 32, BLUE).move_to([4.7, -2.65, 0])
        self.play(FadeIn(shared), run_time=.5)
        self.at("not the frame")
        rail_glow = VGroup(*[r.copy().set_stroke(BLUE, 16, opacity=.45) for r in flat.rails])
        self.add(rail_glow)
        self.play(rail_glow.animate.set_opacity(.08), run_time=1.0)
        self.play(ReplacementTransform(flat, twisted_ladder(SEQ_A, [0, -.05, 0], width=3.9, height=5.4)), run_time=.9)
        bob(icons, amp=.05, speed=1.25)
        self.finish()


class S03Pairs(SpokenScene):
    def construct(self):
        ladder = dna_ladder(SEQ_A, [0, -.1, 0], width=5.1, height=5.4,
                            block_width=1.92, block_height=.64)
        self.add(ladder, scope_tag("schematic"))
        self.at("rungs carry base pairs")
        self.play(LaggedStart(*[Indicate(p, scale_factor=1.03) for p in ladder.pairs], lag_ratio=.12), run_time=1.1)
        self.at("letter name")
        letters = VGroup(*[chip(x, BASE_COLOR[x], 34) for x in "ATCG"]).arrange(DOWN, buff=.28).move_to([4.7,.2,0])
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT*.1) for x in letters], lag_ratio=.15), run_time=1.1)
        self.at("A pairs with T")
        at = ladder.pairs[0]
        self.play(Indicate(at, color=YELLOW, scale_factor=1.08), run_time=.8)
        at_lab = T("A — T", 34, YELLOW, weight=BOLD).move_to([-4.6, 1.5, 0])
        self.play(FadeIn(at_lab), run_time=.45)
        self.at("C pairs with G")
        cg = ladder.pairs[2]
        self.play(Indicate(cg, color=GREEN, scale_factor=1.08), run_time=.8)
        cg_lab = T("C — G", 34, GREEN, weight=BOLD).move_to([-4.6, .5, 0])
        self.play(FadeIn(cg_lab), run_time=.45)
        self.at("either side tell us")
        bracket = pair_bracket(ladder.pairs[3])
        lab = T("base pair", 30, TEXT).next_to(bracket, RIGHT, buff=.28)
        self.play(FadeOut(letters), GrowFromCenter(bracket), FadeIn(lab), run_time=.7)
        lifted = VGroup(*[p[1] for p in ladder.pairs])
        self.play(lifted.animate.shift(UP*.18), run_time=.55)
        self.play(lifted.animate.shift(DOWN*.18), run_time=.55)
        self.at("across each rung")
        self.play(LaggedStart(*[Indicate(p[2], scale_factor=1.04) for p in ladder.pairs], lag_ratio=.12), run_time=1.0)
        for i, p in enumerate(ladder.pairs):
            glow_fill(p[1][0], seed=i)
            glow_fill(p[2][0], seed=i + 1)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = two_ladders_world(False)
        self.play(FadeIn(world.left_ladder.rails), FadeIn(world.right_ladder.rails), run_time=.7)
        self.at("rung letters appear")
        self.play(LaggedStart(*[FadeIn(p) for p in world.left_ladder.pairs], lag_ratio=.08),
                  LaggedStart(*[FadeIn(p) for p in world.right_ladder.pairs], lag_ratio=.08), run_time=1.2)
        self.at("Which part can carry")
        q = fit_text("Which carries different instructions: shared sides or changing base order?",
                     max_w=12.2, size=30, color=GOLD, max_lines=2).move_to([0, 3.35, 0])
        self.play(FadeIn(q, shift=DOWN*.1), run_time=.6)
        self.play(Indicate(VGroup(world.left_ladder.rails, world.right_ladder.rails), color=BLUE, scale_factor=1.02), run_time=.8)
        self.play(LaggedStart(*[Indicate(p, scale_factor=1.04) for p in VGroup(*world.left_ladder.pairs, *world.right_ladder.pairs)], lag_ratio=.05), run_time=1.0)
        self.at("Hold your answer")
        self.play(FadeIn(world.reader, shift=RIGHT*.15), run_time=.5)
        bob(world.reader, amp=.06, speed=1.6)
        for i, p in enumerate(VGroup(*world.left_ladder.pairs, *world.right_ladder.pairs)):
            glow_fill(p[1][0], seed=i)
            glow_fill(p[2][0], seed=i + 1)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which carries different instructions: shared sides or changing base order?"
    SECONDS = 4.5
    CARD = {"y": 3.35, "size": 30, "max_w": 12.2}
    RING_AT = (6.0, -3.0, 0)

    def backdrop(self):
        world = two_ladders_world(False)
        bob(world.reader, amp=.06, speed=1.6)
        for i, p in enumerate(VGroup(*world.left_ladder.pairs, *world.right_ladder.pairs)):
            glow_fill(p[1][0], seed=i)
            glow_fill(p[2][0], seed=i + 1)
        return world


class S06Sequence(SpokenScene):
    def construct(self):
        world = two_ladders_world(False)
        world.left_ladder.rails.set_opacity(.25); world.right_ladder.rails.set_opacity(.25)
        self.add(world.left_ladder, world.right_ladder)
        for i, p in enumerate(VGroup(*world.left_ladder.pairs, *world.right_ladder.pairs)):
            glow_fill(p[1][0], seed=i)
            glow_fill(p[2][0], seed=i + 1)
        self.at("changing order carries")
        self.play(LaggedStart(*[Indicate(p, scale_factor=1.05) for p in VGroup(*world.left_ladder.pairs, *world.right_ladder.pairs)], lag_ratio=.05), run_time=1.2)
        self.at("Sequence means")
        strip = sequence_strip(SEQ_A, [0, -2.75, 0], .78)
        strip_label = T("sequence = base order", 30, TEAL).move_to([0, 3.32, 0])
        reader = world.reader
        self.add(reader)
        copies = VGroup()
        for i, pair in enumerate(world.left_ladder.pairs):
            target = strip[i]
            self.play(reader.animate.next_to(pair, LEFT, buff=.14), TransformFromCopy(pair[1], target), run_time=.35)
            copies.add(target)
        self.play(FadeIn(strip_label), run_time=.45)
        self.at("Traits are features")
        trait = chip("trait = feature", GOLD, 32).move_to([4.65, -2.8, 0])
        self.play(FadeIn(trait, shift=LEFT*.15), run_time=.6)
        self.at("rule connecting both films")
        self.play(FadeOut(VGroup(world, reader, copies, strip_label, trait)), run_time=.6)
        rule = VGroup(T("DNA sequence helps shape traits.", 40, TEAL, weight=BOLD),
                      T("DNA amount does not rank organism complexity.", 34, TEXT))
        rule.arrange(DOWN, buff=.42).move_to([0,.2,0])
        self.play(FadeIn(rule[0], shift=UP*.1), run_time=.8)
        self.at("does not rank")
        self.play(FadeIn(rule[1], shift=UP*.1), run_time=.8)
        self.at("sequence half")
        self.play(rule[1].animate.set_opacity(.25), Indicate(rule[0], color=TEAL, scale_factor=1.03), run_time=1.0)
        underline = Line(rule[0].get_corner(DL)+DOWN*.12, rule[0].get_corner(DR)+DOWN*.12, color=TEAL, stroke_width=5)
        self.play(Create(underline), run_time=.6)
        pulse(underline, base=5, amp=2.0, speed=1.4)
        self.finish()


class S07Gene(SpokenScene):
    def construct(self):
        strip = sequence_strip(SEQ_A, [0, 1.65, 0], .78)
        self.add(strip)
        self.at("within a gene")
        gene_brace = Brace(strip, UP, color=TEAL)
        gene_label = T("gene = section of DNA", 30, TEAL).next_to(gene_brace, UP, buff=.1)
        self.play(GrowFromCenter(gene_brace), FadeIn(gene_label), run_time=.7)
        self.at("chromosome is packaged")
        ribbon = RoundedRectangle(corner_radius=.35, width=10.5, height=1.05, color=BLUE,
                                  fill_color=BLUE, fill_opacity=.16, stroke_width=7).move_to([0,.9,0])
        chromosome = VGroup(Line([-2.2,-1.5,0],[2.2,1.5,0], color=BLUE, stroke_width=28),
                            Line([-2.2,1.5,0],[2.2,-1.5,0], color=BLUE, stroke_width=28)).move_to([0,-.65,0])
        self.play(ReplacementTransform(VGroup(strip, gene_brace, gene_label), ribbon), run_time=.9)
        self.play(ReplacementTransform(ribbon, chromosome), run_time=.9)
        self.add(scope_tag("schematic"))
        self.at("carries many genes")
        genes = VGroup(*[Line([-1.2,0,0],[1.2,0,0], color=TEAL, stroke_width=12).scale(.35).rotate(a).move_to(p)
                         for p, a in [((-1.35,.65,0),-.6),((1.25,.65,0),.6),((-1.25,-.7,0),.6),((1.3,-.75,0),-.6)]])
        self.play(LaggedStart(*[Create(g) for g in genes], lag_ratio=.18), run_time=1.1)
        self.at("build proteins")
        protein = protein_block("protein", [4.7,-1.6,0])
        pa = arrow([2.2,-.6,0], protein.get_left(), RED)
        self.play(GrowArrow(pa), FadeIn(protein), run_time=.7)
        self.at("Other genes")
        other = chip("other cell use", GREY, 28).move_to([-4.7,-1.6,0])
        oa = arrow([-2.2,-.6,0], other.get_right(), GREY)
        self.play(GrowArrow(oa), FadeIn(other), run_time=.7)
        pulse(chromosome[0], base=28, amp=3, speed=1.2)
        pulse(chromosome[1], base=28, amp=3, speed=1.2)
        self.finish()


class S08Pea(SpokenScene):
    def construct(self):
        tag = T("one pea example", 30, TEXT).move_to([0, 3.25, 0])
        self.play(FadeIn(tag), run_time=.5)
        path = pea_path(False, .3)
        self.at("working protein")
        self.play(FadeIn(path.gene), GrowArrow(path.a1), FadeIn(path.protein), run_time=.9)
        self.at("purple flower colour")
        self.play(GrowArrow(path.a2), FadeIn(path.bloom, scale=.7), run_time=.8)
        path.bloom.scale(1.35)
        self.add(scope_tag("schematic"))
        self.at("change in its gene")
        mutant = pea_path(True, .3)
        changed = SurroundingRectangle(mutant.gene[0][2], color=RED, buff=.07, stroke_width=4)
        self.play(Transform(path.gene, mutant.gene), FadeIn(changed), run_time=.8)
        self.at("stop that protein working")
        stop = Cross(path.a1, stroke_color=RED, stroke_width=8)
        self.play(Create(stop), Transform(path.protein, mutant.protein), FadeOut(path.a2), run_time=.7)
        self.at("flower can then be white")
        mutant.bloom.scale(1.35)
        self.play(Transform(path.bloom, mutant.bloom), run_time=.9)
        self.at("connects gene sequence")
        labels = VGroup(T("gene sequence",28,TEAL), T("protein",28,RED), T("trait",28,GOLD))
        labels[0].next_to(path.gene, DOWN, buff=.45); labels[1].next_to(path.protein, DOWN, buff=.25); labels[2].next_to(path.bloom, DOWN, buff=.25)
        self.play(LaggedStart(*[FadeIn(x) for x in labels], lag_ratio=.18), run_time=.9)
        self.at("without making every trait simple")
        caution = T("one example ≠ every trait", 30, GOLD).move_to([0,-2.65,0])
        self.play(FadeIn(caution), run_time=.6)
        bob(path.bloom, amp=.055, speed=1.25)
        self.finish()


class S09Scope(SpokenScene):
    def construct(self):
        top_gene = chip("gene", TEAL, 28).move_to([-3.8, 1.72, 0])
        top_protein = protein_block("protein", [0, 1.72, 0])
        top_trait = chip("purple flower trait", GOLD, 28).move_to([3.9, 1.72, 0])
        path = VGroup(top_gene, arrow(top_gene.get_right(), top_protein.get_left()), top_protein,
                      arrow(top_protein.get_right(), top_trait.get_left()), top_trait)
        self.add(path)
        first = T("first model", 30, GOLD).move_to([0,3.15,0])
        self.at("first model")
        self.play(FadeIn(first), run_time=.5)
        self.add(scope_tag("schematic"))
        self.at("Many traits depend")
        genes = VGroup(sequence_strip("ATCG", [-4.8,-.25,0], .56),
                       sequence_strip("CGAT", [-4.8,-1.25,0], .56),
                       sequence_strip("TACG", [-4.8,-2.25,0], .56))
        genes_heading = T("several genes", 28, TEAL).move_to([-4.8,.45,0])
        trait = Circle(radius=.72, color=GOLD, fill_color=GOLD, fill_opacity=.14).move_to([4.55,-1.15,0])
        trait_lab = T("trait", 32, GOLD, weight=BOLD).move_to(trait)
        arrows = VGroup(*[arrow(g.get_right(), trait.get_left(), GREY, 3, .15) for g in genes])
        self.play(FadeIn(genes_heading), LaggedStart(*[FadeIn(g) for g in genes], lag_ratio=.15), run_time=.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.12), FadeIn(VGroup(trait,trait_lab)), run_time=.8)
        self.at("Surroundings can matter")
        sun = VGroup(Circle(radius=.3, color=YELLOW, fill_color=YELLOW, fill_opacity=.75),
                     *[Line(ORIGIN, RIGHT*.22, color=YELLOW, stroke_width=4).shift(RIGHT*.42).rotate(k*PI/4, about_point=ORIGIN) for k in range(8)])
        water = T("water", 28, BLUE)
        env = VGroup(sun, water).arrange(DOWN, buff=.25).move_to([.5,-1.2,0])
        ea = arrow(env.get_right(), trait.get_left(), GREY, 3, .15)
        self.play(FadeIn(env), GrowArrow(ea), run_time=.7)
        self.at("Some base changes")
        changed = SurroundingRectangle(genes[1][2], color=RED, buff=.05, stroke_width=4)
        changed.layout_ok = True  # deliberate highlight around the changed base
        self.play(Create(changed), run_time=.5)
        self.at("nothing you can see")
        q = T("?", 56, TEXT, weight=BOLD).move_to(trait)
        self.play(FadeOut(trait_lab), FadeIn(q), run_time=.5)
        self.at("scientists test changes")
        test = chip("test the change", TEXT, 28).move_to([2.15,-2.75,0])
        self.play(FadeIn(test), changed.animate.set_color(TEXT), run_time=.7)
        bob(VGroup(trait, q), amp=.05, speed=1.2)
        self.finish()


def chromosome_icon(center=ORIGIN, scale=.55):
    return VGroup(Line([-1,-1.5,0],[1,1.5,0], color=BLUE, stroke_width=18),
                  Line([-1,1.5,0],[1,-1.5,0], color=BLUE, stroke_width=18)).scale(scale).move_to(center)


class S10GeneUse(SpokenScene):
    def construct(self):
        skin = cell("skin cell", [-3.8,.15,0], GOLD, 2.0)
        muscle = cell("muscle cell", [3.8,.15,0], RED, 2.0)
        chrom = chromosome_icon([0,.15,0], .72)
        self.play(FadeIn(chrom), run_time=.5)
        self.at("same DNA")
        c1, c2 = chromosome_icon([-3.8,.35,0],.45), chromosome_icon([3.8,.35,0],.45)
        self.play(FadeIn(skin[0]), FadeIn(muscle[0]), TransformFromCopy(chrom,c1), TransformFromCopy(chrom,c2), FadeOut(chrom), run_time=1.0)
        self.play(FadeIn(VGroup(skin[1],skin[2],muscle[1],muscle[2])), run_time=.5)
        self.add(scope_tag("schematic"))
        self.at("uses different genes")
        g1 = SurroundingRectangle(c1[0], color=TEAL, buff=.08, stroke_width=5)
        g2 = SurroundingRectangle(c2[1], color=TEAL, buff=.08, stroke_width=5)
        self.play(Create(g1), run_time=.55)
        self.play(Create(g2), run_time=.55)
        self.at("Different proteins follow")
        p1 = protein_block("skin proteins",[-3.8,-2.55,0])
        p2 = protein_block("muscle proteins",[3.8,-2.55,0])
        a1 = arrow([-3.8,-1.4,0],p1.get_top(),RED); a2 = arrow([3.8,-1.4,0],p2.get_top(),RED)
        self.play(FadeOut(skin[2]), FadeOut(muscle[2]), GrowArrow(a1),FadeIn(p1),GrowArrow(a2),FadeIn(p2),run_time=.9)
        self.at("look and work differently")
        self.play(Indicate(VGroup(skin[0],p1),color=GOLD,scale_factor=1.02),
                  Indicate(VGroup(muscle[0],p2),color=RED,scale_factor=1.02),run_time=.9)
        self.at("how each cell uses it")
        use = T("same code • different gene use",32,TEAL,weight=BOLD).move_to([0,3.15,0])
        self.play(FadeIn(use,shift=DOWN*.1),run_time=.7)
        pulse(g1,base=5,amp=1.2,speed=2); pulse(g2,base=5,amp=1.2,speed=2)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        gene = chip("gene", TEAL, 30, fill_opacity=.38).move_to([-3.5,1.35,0])
        protein = protein_block("protein",[-3.5,-.1,0])
        trait = chip("trait", GOLD, 30, fill_opacity=.38).move_to([-3.5,-1.55,0])
        a1 = arrow(gene.get_bottom(), protein.get_top())
        a2 = arrow(protein.get_bottom(), trait.get_top())
        path = VGroup(gene,a1,protein,a2,trait)
        self.play(FadeIn(gene), run_time=.4)
        self.at("protein, and trait")
        self.play(GrowArrow(a1),FadeIn(protein),GrowArrow(a2),FadeIn(trait),run_time=1.0)
        self.add(scope_tag("schematic"))
        self.at("Shared parts can carry")
        ladder = dna_ladder("ATCG",[3.75,-.15,0],width=2.6,height=4.4,block_width=.95,block_height=.58)
        self.play(FadeIn(ladder),run_time=.7)
        self.at("cells can use genes differently")
        use = T("cells use genes differently",28,TEAL).move_to([-3.5,-2.65,0])
        self.play(FadeIn(use),run_time=.6)
        self.at("DNA sequence helps")
        rule = T("DNA sequence helps shape traits.",38,TEAL,weight=BOLD).move_to([0,3.1,0])
        self.play(FadeIn(rule,shift=DOWN*.1),run_time=.7)
        self.at("Counting whole chromosome sets")
        axes = VGroup(Line([1.7,-2.3,0],[6.0,-2.3,0],color=GREY,stroke_width=5),
                      Line([1.7,-2.3,0],[1.7,1.55,0],color=GREY,stroke_width=5))
        amount = T("DNA amount",30,GREY).next_to(axes[0],DOWN,buff=.18)
        nodata = T("question — no data yet",28,GOLD).move_to([4.15,-.3,0])
        self.play(ReplacementTransform(ladder, axes),FadeIn(amount),run_time=.7)
        self.at("different question")
        self.play(FadeIn(nodata),run_time=.6)
        self.at("second film")
        self.play(Indicate(VGroup(axes,nodata),color=GOLD,scale_factor=1.02),run_time=.7)
        bob(VGroup(axes, amount, nodata), amp=.045, speed=1.15)
        self.finish()


class S12End(EndCard):
    LINE = "DNA sequence helps shape traits."
