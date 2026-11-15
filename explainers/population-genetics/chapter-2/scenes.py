"""Population genetics, chapter 2: what moves allele frequencies?

Every carried picture is rebuilt by a builder below, so landmarks do not drift between scenes.

COLOR MAP (continued exactly from chapter 1's new script)
  BLUE = allele A
  GOLD = allele a
  GREY = people, containers, and de-emphasized structure
  RED  = forces acting on a population / unresolved causes
  TEXT = expectations and fixed reference marks
  TEAL = chance motion and drift paths
"""
import numpy as np

from bp_parts import *  # noqa: F401,F403


# --------------------------------------------------------------------------- shared geometry
BAR_W, BAR_H = 10.4, 0.82


def living_copy_field(scene, seed=1):
    """A quiet raster field of drifting allele copies behind the main picture.

    Rasterising the distant copies keeps them out of label collision accounting while their slow,
    continuous drift prevents a spoken hold from becoming a frozen frame.
    """
    rng = np.random.default_rng(seed)
    h, w = 108, 192
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    palette = ((88, 196, 221, 82), (212, 168, 67, 82))
    for i in range(52):
        x = int(rng.integers(3, w - 8))
        y = int(rng.integers(3, h - 8))
        s = int(rng.integers(4, 7))
        rgba[y:y + s, x:x + s] = palette[i % 2]
    field = ImageMobject(rgba).set_width(14.5).set_z_index(-20)
    field._living_t = seed * 0.41
    base = field.get_center().copy()

    def drift(mob, dt):
        mob._living_t += dt
        mob.move_to(base + RIGHT * 0.34 * np.sin(0.9 * mob._living_t)
                    + UP * 0.22 * np.sin(1.17 * mob._living_t + 0.8))

    field.add_updater(drift)
    scene.add(field)
    return field


def allele_block(kind="A", size=0.42):
    """One allele copy: a plain block, never a molecular picture."""
    color = BLUE if kind == "A" else GOLD
    box = RoundedRectangle(corner_radius=0.08, width=size, height=size,
                           stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.72)
    return box


def allele_bar(frac=0.55, width=BAR_W, height=BAR_H, labels=True):
    """A computed split bar.  frac is p, the blue share."""
    wb = width * frac
    wg = width - wb
    blue = Rectangle(width=wb, height=height, stroke_color=BLUE, stroke_width=3,
                     fill_color=BLUE, fill_opacity=0.38)
    gold = Rectangle(width=wg, height=height, stroke_color=GOLD, stroke_width=3,
                     fill_color=GOLD, fill_opacity=0.38)
    blue.move_to([-width / 2 + wb / 2, 0, 0])
    gold.move_to([width / 2 - wg / 2, 0, 0])
    parts = [blue, gold]
    if labels:
        parts += [M("A", 30, BLUE, weight=BOLD).move_to(blue),
                  M("a", 30, GOLD, weight=BOLD).move_to(gold)]
    g = VGroup(*parts)
    g.blue, g.gold = blue, gold
    g.boundary_x = -width / 2 + wb
    return g


def split_bar_at(frac, y, width=BAR_W, height=BAR_H, labels=True):
    return allele_bar(frac, width, height, labels).move_to([0, y, 0])


def opening_world(with_question=True):
    """The unchanged before/after bars carried from chapter 1."""
    before = split_bar_at(0.55, 0.8)
    after = split_bar_at(0.55, -0.8)
    left = VGroup(T("before mating", 28, GREY).move_to([-5.15, 1.55, 0]),
                  T("after mating", 28, GREY).move_to([-5.15, -1.55, 0]))
    xb = before.boundary_x
    glow = Line([xb, -1.26, 0], [xb, 1.26, 0], color=TEXT, stroke_width=7)
    pulse(glow, base=5, amp=2, speed=2.4)
    g = VGroup(before, after, left, glow)
    if with_question:
        q = T("What moves p?", 48, TEXT, font=TITLE_FONT).move_to([0, 2.85, 0])
        g.add(q)
        g.question = q
    g.before, g.after, g.glow = before, after, glow
    return g


def pool_of_blocks(frac=0.55, cols=8, rows=4, size=0.34, center=ORIGIN, seed=4):
    """Deterministic inventory of allele copies in a rounded pool."""
    n = cols * rows
    n_blue = int(round(n * frac))
    kinds = ["A"] * n_blue + ["a"] * (n - n_blue)
    rng = np.random.default_rng(seed)
    rng.shuffle(kinds)
    blocks = VGroup(*[allele_block(k, size) for k in kinds]).arrange_in_grid(rows, cols, buff=0.11)
    rim = RoundedRectangle(corner_radius=0.28, width=blocks.width + 0.55,
                           height=blocks.height + 0.55, stroke_color=GREY,
                           stroke_width=3, fill_color=BG, fill_opacity=0.75)
    g = VGroup(rim, blocks).move_to(center)
    g.rim, g.blocks = rim, blocks
    return g


def sampling_cup(color=TEAL):
    """Opaque schematic sampling cup."""
    body = Polygon([-0.95, 0.72, 0], [0.95, 0.72, 0], [0.66, -0.72, 0],
                   [-0.66, -0.72, 0], stroke_color=color, stroke_width=4,
                   fill_color=BG, fill_opacity=0.96)
    lip = Line([-1.02, 0.72, 0], [1.02, 0.72, 0], color=color, stroke_width=6)
    return VGroup(body, lip)


def drift_start_world(question=True):
    """Exact carried frame for s05 and s06."""
    left = pool_of_blocks(0.5, cols=4, rows=3, size=0.38, center=[-3.4, 0.65, 0], seed=11)
    right = pool_of_blocks(0.5, cols=4, rows=3, size=0.38, center=[3.4, 0.65, 0], seed=11)
    cups = VGroup(sampling_cup().move_to([-3.4, 2.15, 0]),
                  sampling_cup().move_to([3.4, 2.15, 0]))
    bars = VGroup(allele_bar(0.5, 4.7, 0.62).move_to([-3.4, -1.25, 0]),
                  allele_bar(0.5, 4.7, 0.62).move_to([3.4, -1.25, 0]))
    # Faint possible future boundaries: schematic, symmetric around the identical start.
    fans = VGroup()
    for x0 in (-3.4, 3.4):
        for dx in (-0.8, -0.4, 0.4, 0.8):
            fans.add(Line([x0, -1.76, 0], [x0 + dx, -2.32, 0],
                          color=TEAL, stroke_width=3, stroke_opacity=0.22))
    g = VGroup(fans, left, right, cups, bars)
    if question:
        q = T("Same start: same path?", 46, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        g.add(q)
        g.question = q
    g.left_pool, g.right_pool, g.cups, g.bars = left, right, cups, bars
    return g


def genotype_card(a, b, color=GREY, width=1.65):
    blocks = VGroup(allele_block(a, 0.46), allele_block(b, 0.46)).arrange(RIGHT, buff=0.16)
    frame = RoundedRectangle(corner_radius=0.15, width=width, height=1.0,
                             stroke_color=color, stroke_width=2.5)
    return VGroup(frame, blocks.move_to(frame))


def genotype_histogram(values=(3.1, 1.35, 3.1), center=(-3.5, -0.3, 0)):
    """A genotype histogram used unchanged in s08 and s09."""
    x0, y0 = -5.75, -2.45
    colors = (BLUE, GREY, GOLD)
    names = ("AA", "Aa", "aa")
    bars, labels = VGroup(), VGroup()
    for i, (h, col, name) in enumerate(zip(values, colors, names)):
        x = x0 + 2.25 * i
        b = Rectangle(width=1.28, height=h, stroke_color=col, stroke_width=3,
                      fill_color=col, fill_opacity=0.38).move_to([x, y0 + h / 2, 0])
        bars.add(b)
        labels.add(T(name, 28, col).move_to([x, y0 - 0.38, 0]))
    base = Line([-6.55, y0, 0], [-0.35, y0, 0], color=GREY, stroke_width=3)
    title = T("genotype counts", 28, TEXT).move_to([-3.45, 2.85, 0])
    g = VGroup(base, bars, labels, title)
    g.bars = bars
    return g


def action_icon(kind, color=RED):
    """Five large action shapes for the comparison and rule scenes."""
    if kind == "contribution":
        shape = Polygon([-0.85, 0.55, 0], [0.85, 0.55, 0], [0.38, -0.55, 0],
                        [-0.38, -0.55, 0], color=color, stroke_width=4)
    elif kind == "membership":
        shape = VGroup(Arrow([-0.9, 0, 0], [0.45, 0, 0], color=color, stroke_width=6, buff=0),
                       Arc(radius=0.55, start_angle=-PI / 2, angle=PI, color=GREY, stroke_width=4).shift(RIGHT * 0.45))
    elif kind == "identity":
        shape = VGroup(allele_block("A", 0.55).shift(LEFT * 0.5),
                       CurvedArrow([-0.15, 0.45, 0], [0.52, 0.05, 0], angle=-1.2,
                                   color=color, stroke_width=4),
                       allele_block("a", 0.55).shift(RIGHT * 0.62))
    elif kind == "sample":
        shape = sampling_cup(TEAL).scale(0.72)
    else:
        shape = VGroup(genotype_card("A", "A", GREY, 1.25).scale(0.72),
                       genotype_card("a", "a", GREY, 1.25).scale(0.72)).arrange(RIGHT, buff=0.18)
    label = T(kind, 26, TEAL if kind == "sample" else color)
    return VGroup(shape, label).arrange(DOWN, buff=0.16)


def action_world():
    """The one pool with the five process shapes, shared by s10 and s11."""
    bar = allele_bar(0.55, 6.0, 0.9).move_to([0, 0.2, 0])
    specs = [("contribution", [-4.8, 2.2, 0]), ("membership", [0, 2.25, 0]),
             ("identity", [4.8, 2.2, 0]), ("sample", [-3.5, -2.25, 0]),
             ("pairing", [3.5, -2.25, 0])]
    icons = VGroup()
    for kind, pos in specs:
        icon = action_icon(kind, GREY if kind == "pairing" else RED).move_to(pos)
        icons.add(icon)
    g = VGroup(bar, icons)
    g.bar, g.icons = bar, icons
    return g


# --------------------------------------------------------------------------- scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        living_copy_field(self, 0)
        world = opening_world(False)
        self.play(FadeIn(world.before), run_time=1.0)
        self.at("unchanged after mating")
        self.play(FadeIn(world.after, shift=DOWN * 0.18), FadeIn(world[2]), run_time=1.3)
        self.at("move that boundary")
        self.play(FadeIn(world.glow), run_time=0.7)
        q = T("What moves p?", 48, TEXT, font=TITLE_FONT).move_to([0, 2.85, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.7)
        self.at("Keep following copies")
        movers = VGroup(*[allele_block("A" if i % 2 == 0 else "a", 0.34)
                          for i in range(8)]).arrange(RIGHT, buff=0.25).move_to([0, -2.75, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in movers], lag_ratio=0.08), run_time=1.2)
        bob(movers, amp=0.06, speed=1.7)
        self.at("depends on what touches")
        touch = VGroup(*[Arrow([x, -3.55, 0], [x, -3.02, 0], color=RED,
                               stroke_width=4, buff=0.02) for x in (-3, -1, 1, 3)])
        self.play(LaggedStart(*[GrowArrow(a) for a in touch], lag_ratio=0.12), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Population genetics"
    TITLE = "What Moves Allele Frequencies?"

    def construct(self):
        world = opening_world(False).scale(0.84).shift(DOWN * 0.55)
        world.before.remove(world.before[2], world.before[3])
        world.after.remove(world.after[2], world.after[3])
        world.set_opacity(0.72)
        lesson = T(self.LESSON.upper(), 22, GREY).move_to([0, 2.7, 0])
        title = fit_text(self.TITLE, max_w=10.8, size=50, color=TEXT,
                         font=TITLE_FONT, min_size=40).move_to([0, 1.9, 0])
        # Four unlabelled process shapes circle the unchanged bar; their names come later.
        icons = VGroup(action_icon("contribution")[0], action_icon("membership")[0],
                       action_icon("identity")[0], action_icon("sample")[0])
        for icon, pos in zip(icons, ([-5.75, 1.75, 0], [5.75, 1.75, 0],
                                     [-5.75, -2.75, 0], [5.75, -2.75, 0])):
            icon.scale(0.48).move_to(pos).set_opacity(0.7)
        self.add(world)
        self.play(FadeIn(lesson), FadeIn(title, shift=UP * 0.1), FadeIn(icons), run_time=0.8)
        self.play(Rotate(icons, angle=0.10, about_point=ORIGIN), run_time=0.8, rate_func=linear)
        self.finish()


class S02Selection(SpokenScene):
    def construct(self):
        living_copy_field(self, 2)
        title = T("selection: unequal contribution", 40, RED, font=TITLE_FONT).move_to([0, 3.25, 0])
        cards = VGroup(genotype_card("A", "A", BLUE), genotype_card("A", "a", GREY),
                       genotype_card("a", "a", GOLD)).arrange(RIGHT, buff=2.0).move_to([0, 1.55, 0])
        lanes = VGroup(*[Line([x, 0.98, 0], [x, -0.35, 0], color=GREY, stroke_width=12)
                         for x in (-3.65, 0, 3.65)])
        self.play(FadeIn(cards, shift=UP * 0.15), run_time=1.1)
        self.at("different numbers")
        self.play(FadeIn(title), Create(lanes), run_time=1.1)
        self.at("contributes fewer copies")
        narrow = Polygon([-0.55, 0.95, 0], [0.55, 0.95, 0], [0.20, -0.35, 0],
                         [-0.20, -0.35, 0], stroke_color=RED, stroke_width=4,
                         fill_color=BG, fill_opacity=1)
        fewer = T("fewer surviving offspring", 28, RED).move_to([0, 2.62, 0])
        self.play(FadeOut(lanes[1]), FadeIn(narrow), FadeIn(fewer), run_time=1.0)
        self.at("bar moves predictably")
        start = allele_bar(0.50, 8.8, 0.75).move_to([0, -1.45, 0])
        finish = allele_bar(0.62, 8.8, 0.75).move_to([0, -1.45, 0])
        copies = VGroup(*[allele_block(k, 0.32) for k in "AAAaaaAA"])
        copies.arrange(RIGHT, buff=0.22).move_to([0, -0.65, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.55) for b in copies], lag_ratio=0.07),
                  FadeIn(start), run_time=1.3)
        self.play(ReplacementTransform(start, finish), run_time=1.2)
        self.at("depends on the environment")
        env = boxed_label("environment sets the advantage", RED, size=28).move_to([0, -2.65, 0])
        self.play(swap(fewer, env), FadeOut(copies), run_time=0.9)
        self.at("direction can change")
        reverse = allele_bar(0.40, 8.8, 0.75).move_to([0, -1.45, 0])
        self.play(ReplacementTransform(finish, reverse), Indicate(env, color=RED), run_time=1.4)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Migration(SpokenScene):
    def construct(self):
        living_copy_field(self, 3)
        title = T("migration: mix populations", 40, RED, font=TITLE_FONT).move_to([0, 3.25, 0])
        resident = pool_of_blocks(0.68, 6, 4, 0.33, [-3.6, 0.65, 0], seed=3)
        migrant = pool_of_blocks(0.25, 4, 3, 0.33, [3.9, 1.05, 0], seed=8)
        labs = VGroup(T("residents", 30, BLUE).next_to(resident, UP, buff=0.2),
                      T("migrants", 30, GOLD).next_to(migrant, UP, buff=0.2))
        self.play(FadeIn(title), FadeIn(resident), run_time=1.1)
        self.at("between populations")
        self.play(FadeIn(migrant), FadeIn(labs), run_time=1.0)
        self.at("Pour a small stream")
        stream = CurvedArrow(migrant.get_left() + LEFT * 0.05,
                             resident.get_right() + RIGHT * 0.05, angle=0.42,
                             color=RED, stroke_width=7)
        moving = VGroup(*[allele_block("a", 0.30) for _ in range(4)]).arrange(RIGHT, buff=0.12)
        moving.move_to([0.5, 0.55, 0])
        self.play(Create(stream), LaggedStart(*[FadeIn(b, shift=LEFT * 1.2) for b in moving], lag_ratio=0.1), run_time=1.4)
        self.at("weighted average")
        b0 = allele_bar(0.68, 8.8, 0.78).move_to([0, -1.5, 0])
        migrant_mark = Line([-2.2, -2.08, 0], [-2.2, -0.95, 0], color=GOLD, stroke_width=4)
        self.play(FadeIn(b0), FadeIn(migrant_mark), run_time=0.9)
        self.at("toward the migrants' mix")
        b1 = allele_bar(0.58, 8.8, 0.78).move_to([0, -1.5, 0])
        self.play(ReplacementTransform(b0, b1), run_time=1.3)
        self.at("migrants' share")
        share = boxed_label("larger migrant share → larger shift", RED, size=28).move_to([0, -2.75, 0])
        self.play(FadeIn(share, shift=UP * 0.1), Indicate(stream, color=RED), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Mutation(SpokenScene):
    def construct(self):
        living_copy_field(self, 4)
        title = T("mutation: change identity", 40, RED, font=TITLE_FONT).move_to([0, 3.25, 0])
        blue = allele_block("A", 1.15).move_to([-4.5, 0.65, 0])
        door = RoundedRectangle(corner_radius=0.12, width=1.5, height=2.7,
                                stroke_color=RED, stroke_width=5).move_to([0, 0.65, 0])
        dlab = T("mutation", 28, RED).next_to(door, UP, buff=0.18)
        self.play(FadeIn(blue, scale=0.7), FadeIn(title), run_time=1.0)
        self.at("identity of a copy")
        self.play(FadeIn(door), FadeIn(dlab), blue.animate.move_to([-1.25, 0.65, 0]), run_time=1.1)
        self.at("flips to gold")
        gold = allele_block("a", 1.15).move_to([1.25, 0.65, 0])
        self.play(Rotate(blue, PI / 2), run_time=0.55)
        self.play(ReplacementTransform(blue, gold), run_time=0.65)
        self.at("new route")
        route = VGroup(Arrow([-4.1, -1.05, 0], [4.1, -1.05, 0], color=RED, stroke_width=5, buff=0),
                       Arrow([4.1, -1.48, 0], [-4.1, -1.48, 0], color=GREY,
                             stroke_width=3, stroke_opacity=0.45, buff=0),
                       M("A", 34, BLUE).move_to([-4.55, -1.05, 0]),
                       M("a", 34, GOLD).move_to([4.55, -1.05, 0]))
        self.play(FadeIn(route), gold.animate.move_to([4.55, 0.65, 0]), run_time=1.1)
        self.at("usually weak")
        b0 = allele_bar(0.550, 9.2, 0.72).move_to([0, -2.15, 0])
        b1 = allele_bar(0.545, 9.2, 0.72).move_to([0, -2.15, 0])
        self.play(FadeIn(b0), run_time=0.7)
        self.play(ReplacementTransform(b0, b1), run_time=1.2)
        self.at("supplies variation")
        varied = VGroup(*[allele_block(k, 0.34) for k in "AAAaAAaA"]).arrange(RIGHT, buff=0.18)
        varied.move_to([0, -3.05, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in varied], lag_ratio=0.08), run_time=1.0)
        self.finish()


class S05PredictDrift(SpokenScene):
    def construct(self):
        living_copy_field(self, 5)
        world = drift_start_world(False)
        self.play(FadeIn(world.left_pool), run_time=0.9)
        self.at("population twice")
        self.play(TransformFromCopy(world.left_pool, world.right_pool), run_time=1.0)
        self.at("samples its next generation")
        self.play(FadeIn(world.cups, shift=DOWN * 0.15), run_time=1.0)
        bob(world.cups[0], amp=0.07, speed=3.0)
        bob(world.cups[1], amp=0.07, speed=3.4, seed=2)
        self.at("same copy inventory")
        self.play(FadeIn(world.bars), FadeIn(world[0]), run_time=1.0)
        self.at("Predict the result")
        q = T("Same start: same path?", 46, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.8)
        self.at("move together")
        prompt = question_card("Must both bars move together — or can they separate?",
                               y=-3.18, size=30, max_w=11.2)
        self.play(FadeIn(prompt.question), run_time=0.9)
        self.at("without selection")
        self.play(Indicate(world.bars, color=TEAL, scale_factor=1.025), run_time=1.0)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "Must both bars move together — or can they separate?"
    CARD = {"y": -3.18, "size": 30, "max_w": 11.2}
    RING_AT = (6.05, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = drift_start_world(True)
        bob(w.cups[0], amp=0.07, speed=3.0)
        bob(w.cups[1], amp=0.07, speed=3.4, seed=2)
        for i, b in enumerate(w.left_pool.blocks):
            bob(b, amp=0.025, speed=2.0 + 0.1 * i, seed=i)
        for i, b in enumerate(w.right_pool.blocks):
            bob(b, amp=0.025, speed=2.1 + 0.1 * i, seed=i + 2)
        return w


class S07Drift(SpokenScene):
    def construct(self):
        living_copy_field(self, 7)
        world = drift_start_world(True)
        self.add(world)
        self.at("They can separate")
        self.play(FadeOut(world.question), run_time=0.4)
        left_new = allele_bar(0.72, 4.7, 0.62).move_to([-3.4, -1.25, 0])
        right_new = allele_bar(0.28, 4.7, 0.62).move_to([3.4, -1.25, 0])
        pours = VGroup(*[allele_block("A", 0.3).move_to([-3.4 + 0.15 * i, 1.65 - 0.15 * i, 0]) for i in range(4)],
                       *[allele_block("a", 0.3).move_to([3.4 + 0.15 * i, 1.65 - 0.15 * i, 0]) for i in range(4)])
        self.play(FadeIn(pours, shift=DOWN * 0.7),
                  ReplacementTransform(world.bars[0], left_new),
                  ReplacementTransform(world.bars[1], right_new), run_time=1.4)
        self.at("random sampling")
        label = T("drift: no preferred direction", 38, TEAL, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(FadeIn(label), FadeOut(pours), run_time=0.8)
        self.at("more blue")
        self.play(Indicate(left_new, color=BLUE, scale_factor=1.025), run_time=0.8)
        self.at("more gold")
        self.play(Indicate(right_new, color=GOLD, scale_factor=1.025), run_time=0.8)
        self.at("Across many repeats")
        self.play(FadeOut(VGroup(world.left_pool, world.right_pool, world.cups, world[0], left_new, right_new)), run_time=0.7)
        xs = np.linspace(-4.8, 4.8, 9)
        starts = np.full(9, 0.5)
        ends = np.array([0.10, 0.24, 0.34, 0.43, 0.50, 0.58, 0.67, 0.78, 0.91])
        paths, bars = VGroup(), VGroup()
        for x, p0, p1 in zip(xs, starts, ends):
            paths.add(Line([x, 1.45, 0], [x + (p1 - p0) * 1.1, -0.75, 0],
                           color=TEAL, stroke_width=4))
            bars.add(allele_bar(p1, 0.82, 2.8, labels=False).move_to([x + (p1 - p0) * 1.1, -2.2, 0]))
        mean = DashedLine([0, 1.75, 0], [0, -3.45, 0], color=TEXT, stroke_width=4)
        mean_lab = T("mean near start", 28, TEXT).move_to([1.35, 1.75, 0])
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.06), run_time=1.5)
        self.at("small populations spread widely")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in bars], lag_ratio=0.05),
                  FadeIn(mean), FadeIn(mean_lab), run_time=1.2)
        self.add(T("schematic", 24, GREY).move_to([5.75, 2.72, 0]))
        self.finish()


class S08Nonrandom(SpokenScene):
    def construct(self):
        living_copy_field(self, 8)
        title = T("same copies, different pairs", 42, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        random_cards = VGroup(genotype_card("A", "A", BLUE), genotype_card("A", "a"),
                              genotype_card("A", "a"), genotype_card("a", "a", GOLD))
        random_cards.arrange(RIGHT, buff=0.38).move_to([0, 1.75, 0])
        self.play(FadeIn(title), FadeIn(random_cards), run_time=1.2)
        self.at("pair more often")
        same_cards = VGroup(genotype_card("A", "A", BLUE), genotype_card("A", "A", BLUE),
                            genotype_card("a", "a", GOLD), genotype_card("a", "a", GOLD))
        same_cards.arrange(RIGHT, buff=0.38).move_to([0, 1.75, 0])
        self.play(ReplacementTransform(random_cards, same_cards), run_time=1.3)
        self.at("homozygotes can increase")
        hist0 = genotype_histogram((1.8, 3.25, 1.8))
        hist1 = genotype_histogram((3.1, 1.35, 3.1))
        self.play(FadeIn(hist0), run_time=0.8)
        self.at("heterozygotes decrease")
        self.play(ReplacementTransform(hist0, hist1), run_time=1.2)
        self.at("every blue and gold copy remains")
        fixed_bar = allele_bar(0.5, 5.1, 0.72).move_to([3.7, -0.75, 0])
        count = Readout([("blue", lambda: 4, "{:.0f} copies", BLUE),
                         ("gold", lambda: 4, "{:.0f} copies", GOLD)],
                        at=[3.7, -2.0, 0], widest=[4, 4], title="allele inventory")
        self.play(FadeIn(fixed_bar), FadeIn(count), run_time=1.0)
        self.at("stays in the same place")
        marker = Line([3.7, -1.32, 0], [3.7, -0.18, 0], color=TEXT, stroke_width=5)
        self.play(FadeIn(marker), Indicate(fixed_bar, color=TEXT), run_time=1.0)
        self.at("changes genotype frequencies")
        self.play(hist1.bars.animate.set_fill(opacity=0.68), run_time=0.5)
        self.play(hist1.bars.animate.set_fill(opacity=0.38), run_time=0.5)
        self.at("not allele frequencies")
        self.play(Indicate(VGroup(fixed_bar, marker), color=TEXT), run_time=1.0)
        self.finish()


class S09Signatures(SpokenScene):
    def construct(self):
        living_copy_field(self, 9)
        hist = genotype_histogram((3.1, 1.35, 3.1))
        deficit = boxed_label("heterozygote deficit", RED, size=30).move_to([3.75, 2.72, 0])
        self.add(hist)
        self.play(FadeIn(deficit), run_time=0.7)
        self.at("rarely names a cause")
        causes = VGroup(boxed_label("non-random mating", RED, size=26),
                        boxed_label("population mixture", RED, size=26),
                        boxed_label("typing error", RED, size=26))
        causes.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([3.85, 0.55, 0])
        spine = Line([1.55, 2.72, 0], [1.55, -1.45, 0], color=RED, stroke_width=4)
        trunk = Line(deficit.get_left() + LEFT * 0.08, [1.55, 2.72, 0], color=RED, stroke_width=4)
        branches = VGroup(*[Arrow([1.55, c.get_center()[1], 0], c.get_left() + LEFT * 0.08,
                                  color=RED, stroke_width=4, buff=0.02) for c in causes])
        self.play(Create(trunk), Create(spine),
                  LaggedStart(*[GrowArrow(a) for a in branches], lag_ratio=0.12), run_time=1.1)
        self.at("might reflect")
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.12) for c in causes], lag_ratio=0.14), run_time=1.2)
        self.at("several explanations")
        marks = VGroup(*[M("?", 38, RED, weight=BOLD).next_to(c, RIGHT, buff=0.18) for c in causes])
        self.play(LaggedStart(*[FadeIn(m, scale=1.2) for m in marks], lag_ratio=0.12), run_time=0.9)
        self.at("compares predictions with patterns")
        glass = VGroup(Circle(radius=0.62, color=TEXT, stroke_width=6),
                       Line([0.44, -0.44, 0], [1.05, -1.05, 0], color=TEXT, stroke_width=7)).move_to([-5.2, 0.4, 0])
        self.play(FadeIn(glass, scale=0.7), glass.animate.move_to([-2.0, 0.4, 0]), run_time=1.3)
        self.at("independent evidence")
        panels = VGroup(*[boxed_label("evidence ?", TEXT, size=26) for _ in range(3)])
        panels.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([3.85, 0.55, 0])
        self.play(Succession(
            FadeOut(VGroup(causes, marks, branches, spine, trunk, glass), run_time=0.42),
            LaggedStart(*[FadeIn(p, shift=LEFT * 0.12) for p in panels], lag_ratio=0.12, run_time=0.58)
        ))
        self.finish()


class S10Compare(SpokenScene):
    def construct(self):
        living_copy_field(self, 10)
        world = action_world()
        self.play(FadeIn(world.bar), run_time=0.8)
        self.at("what each process touches")
        self.play(LaggedStart(*[FadeIn(i, scale=0.8) for i in world.icons], lag_ratio=0.08), run_time=1.3)
        cues = [("Selection changes contribution", 0), ("Migration changes membership", 1),
                ("Mutation changes identity", 2), ("Drift changes the sample", 3),
                ("Non-random mating changes pairing", 4)]
        for phrase, i in cues:
            self.at(phrase)
            col = TEAL if i == 3 else (GREY if i == 4 else RED)
            self.play(Indicate(world.icons[i], color=col, scale_factor=1.08), run_time=0.85)
            if i < 4:
                moved = allele_bar([0.62, 0.45, 0.57, 0.48][i], 6.0, 0.9).move_to(world.bar)
                self.play(ReplacementTransform(world.bar, moved), run_time=0.55)
                world.bar = moved
        fixed = Line([0, -0.38, 0], [0, 0.78, 0], color=TEXT, stroke_width=5)
        self.play(FadeIn(fixed), run_time=0.5)
        self.at("evidence to explain")
        cap = caption("A moving bar is evidence — not a label for one cause.", size=30, color=TEXT, y=-3.43)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        living_copy_field(self, 11)
        world = action_world()
        self.add(world)
        bar_targets = ([-2.7, 0.78, 0], [1.5, 0.78, 0], [2.7, 0.78, 0], [-2.7, -0.38, 0])
        starts = (world.icons[0][0].get_right(), world.icons[1][0].get_right() + RIGHT * 0.18,
                  world.icons[2][0].get_left(), world.icons[3][0].get_right())
        paths = VGroup(*[Line(a, b, color=TEAL if i == 3 else RED, stroke_width=4)
                         for i, (a, b) in enumerate(zip(starts, bar_targets))])
        pairing_path = Line(world.icons[4][0].get_left(), [4.25, -0.75, 0],
                            color=GREY, stroke_width=4)
        cards = VGroup(genotype_card("A", "A", BLUE, 1.3),
                       genotype_card("a", "a", GOLD, 1.3)).arrange(RIGHT, buff=0.25).scale(0.72)
        cards.move_to([3.5, -0.75, 0])
        self.at("distinct, testable ways")
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.09),
                  Create(pairing_path), FadeIn(cards), run_time=1.4)
        self.at("Follow the copies")
        self.play(FadeOut(VGroup(world, paths, pairing_path, cards)), run_time=0.7)
        checks = [("copies", BLUE), ("prediction", TEXT), ("data", GOLD), ("alternatives", RED)]
        rows = VGroup()
        for word, col in checks:
            box = Square(side_length=0.46, color=col, stroke_width=3)
            tick = T("✓", 30, col)
            lab = T(word, 38, col)
            rows.add(VGroup(box, tick.move_to(box), lab).arrange(RIGHT, buff=0.28))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.15, 0])
        for phrase, row in zip(("Follow the copies", "expected signature", "with the data", "alternative causes"), rows):
            self.at(phrase)
            self.play(FadeIn(row, shift=RIGHT * 0.18), run_time=0.75)
        self.finish()


class S12End(EndCard):
    LINE = "Forces change allele frequencies in distinct, testable ways."
