"""One Cross, Three Patterns.

COLOR MAP
  R_RED  = R allele, red flower/coat, A marker
  W_PALE = W allele, white flower/coat
  PINK   = incomplete-dominance RW phenotype
  BLUE   = B marker
  TEAL   = phenotype lens / conceptual separation
  GOLD   = prediction and active question
  GREY   = grid and supporting structure

The Punnett grid is always rebuilt by ``cross_world``.  That is the film's
carried picture, so every cell, header and allele tile keeps one location.
"""
from bp_parts import *


R_RED = "#E85D5D"
W_PALE = "#F4E7C5"
PINK = "#F29BB5"
MARKER_BLUE = "#58C4DD"
CELL = 1.82
GRID_C = np.array([0.45, 0.46, 0.0])
QUESTION = "Which pairing repeats, and which pairings sit at the corners?"


def allele_tile(letter, color, size=0.66):
    """One inherited copy; the fill colour never changes in the film."""
    box = RoundedRectangle(corner_radius=0.13, width=size, height=size,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.92)
    label = T(letter, 30 if size >= 0.6 else 28, BG, weight=BOLD).move_to(box)
    return VGroup(box, label)


def allele_pair(code, at, size=0.58):
    colors = {"R": R_RED, "W": W_PALE}
    pair = VGroup(*[allele_tile(c, colors[c], size) for c in code]).arrange(RIGHT, buff=0.13)
    return pair.move_to(at)


def snapdragon(color=PINK, height=2.7):
    """Large schematic flower: the lesson's own picture, not a molecule."""
    stem = Line(DOWN * 1.05, UP * 0.35, color=GREEN, stroke_width=8)
    leaf_l = Ellipse(width=0.52, height=0.24, color=GREEN, fill_color=GREEN,
                     fill_opacity=0.75).rotate(0.45).move_to([-0.28, -0.45, 0])
    leaf_r = leaf_l.copy().rotate(PI - 0.9).move_to([0.28, -0.15, 0])
    petals = VGroup(*[
        Circle(radius=0.31, color=color, fill_color=color, fill_opacity=0.92)
        .move_to(0.36 * np.array([np.cos(a), np.sin(a), 0]))
        for a in np.linspace(0, TAU, 6)[:-1]
    ]).shift(UP * 0.58)
    center = Circle(radius=0.23, color=color, fill_color=color, fill_opacity=1).move_to(UP * 0.58)
    g = VGroup(stem, leaf_l, leaf_r, petals, center)
    g.set_height(height)
    return g


def mini_flower(color, at):
    return snapdragon(color, 0.86).move_to(at)


def coat_patch(kind, at, size=0.86):
    if kind == "roan":
        colors = [R_RED, W_PALE] * 5
        bars = VGroup(*[
            Rectangle(width=size / len(colors), height=size * 0.86, stroke_width=0,
                      fill_color=c, fill_opacity=1) for c in colors
        ]).arrange(RIGHT, buff=0)
        frame = RoundedRectangle(corner_radius=0.12, width=size + 0.06, height=size,
                                 stroke_color=TEXT, stroke_width=3)
        bars.move_to(frame)
        return VGroup(bars, frame).move_to(at)
    color = R_RED if kind == "red" else W_PALE
    return RoundedRectangle(corner_radius=0.12, width=size, height=size,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.95).move_to(at)


def cross_world(revealed=False, phenotypes=None, title=None, lens=None):
    """The carried world.  Every continuing scene calls this builder."""
    cx, cy = GRID_C[:2]
    cells = VGroup()
    cell_map = {}
    for row in range(2):
        for col in range(2):
            p = np.array([cx + (col - 0.5) * CELL, cy + (0.5 - row) * CELL, 0])
            sq = Square(CELL, stroke_color=GREY, stroke_width=4).move_to(p)
            cells.add(sq)
            cell_map[(row, col)] = p
    top = VGroup(allele_tile("R", R_RED), allele_tile("W", W_PALE))
    top[0].move_to([cx - CELL / 2, cy + CELL + 0.52, 0])
    top[1].move_to([cx + CELL / 2, cy + CELL + 0.52, 0])
    left = VGroup(allele_tile("R", R_RED), allele_tile("W", W_PALE))
    left[0].move_to([cx - CELL - 0.52, cy + CELL / 2, 0])
    left[1].move_to([cx - CELL - 0.52, cy - CELL / 2, 0])
    targets = VGroup(*[Circle(radius=0.13, color=GREY, stroke_width=2).set_opacity(0.45).move_to(p)
                       for p in cell_map.values()])
    pairs = VGroup()
    codes = {(0, 0): "RR", (0, 1): "RW", (1, 0): "RW", (1, 1): "WW"}
    if revealed:
        for key in ((0, 0), (0, 1), (1, 0), (1, 1)):
            p = cell_map[key] + (UP * 0.36 if phenotypes else ORIGIN)
            pairs.add(allele_pair(codes[key], p))
    backplate = RoundedRectangle(corner_radius=0.28, width=5.72, height=5.66,
                                 stroke_color=GREY, stroke_width=2,
                                 fill_color="#29313D", fill_opacity=0.94).move_to([cx, 0.42, 0])
    backplate.set_z_index(-3)
    backplate.layout_ok = True  # deliberate dark stage behind all grid labels and tiles
    world = VGroup(backplate, cells, top, left, pairs if revealed else targets)
    world.backplate = backplate
    world.cells, world.cell_map, world.top_tiles, world.left_tiles = cells, cell_map, top, left
    world.targets, world.pairs = targets, pairs
    world.codes = codes
    if phenotypes == "flowers":
        vals = {(0, 0): R_RED, (0, 1): PINK, (1, 0): PINK, (1, 1): W_PALE}
        pics = VGroup(*[mini_flower(vals[k], cell_map[k] + DOWN * 0.47)
                        for k in ((0, 0), (0, 1), (1, 0), (1, 1))])
        world.add(pics)
        world.phenotypes = pics
    elif phenotypes == "coats":
        vals = {(0, 0): "red", (0, 1): "roan", (1, 0): "roan", (1, 1): "white"}
        pics = VGroup(*[coat_patch(vals[k], cell_map[k] + DOWN * 0.43)
                        for k in ((0, 0), (0, 1), (1, 0), (1, 1))])
        world.add(pics)
        world.phenotypes = pics
    if title:
        ttl = fit_text(title, max_w=5.2, size=30, color=TEXT).move_to([cx, 3.38, 0])
        world.add(ttl)
        world.title = ttl
    if lens:
        outline = RoundedRectangle(corner_radius=0.28, width=5.55, height=4.40,
                                   stroke_color=TEAL, stroke_width=5,
                                   fill_color=TEAL, fill_opacity=0.035).move_to([cx, 0.10, 0])
        lab = T(lens, 30, TEAL, weight=BOLD).move_to([cx, 3.56, 0])
        outline.set_z_index(-1)
        world.add(outline, lab)
        world.lens_outline, world.lens_label = outline, lab
    return world


def drifting_tiles(world):
    """Four copies circling empty landing targets; used before the answer."""
    tiles = VGroup(allele_tile("R", R_RED, 0.55), allele_tile("W", W_PALE, 0.55),
                   allele_tile("R", R_RED, 0.55), allele_tile("W", W_PALE, 0.55))
    starts = [world.cell_map[(0, 0)] + UL * 0.42, world.cell_map[(0, 1)] + UR * 0.42,
              world.cell_map[(1, 0)] + DL * 0.42, world.cell_map[(1, 1)] + DR * 0.42]
    for tile, p in zip(tiles, starts):
        tile.move_to(p)
    return tiles


def genotype_bar(label="genotypes stay fixed"):
    boxes = VGroup(*[allele_pair(c, ORIGIN, 0.43) for c in ("RR", "RW", "RW", "WW")])
    boxes.arrange(RIGHT, buff=0.45).move_to([0.45, -2.72, 0])
    lab = T(label, 28, TEAL, weight=BOLD).next_to(boxes, DOWN, buff=0.16)
    return VGroup(boxes, lab)


def phenotype_bar(kind):
    if kind == "flowers":
        pics = VGroup(*[snapdragon(c, 0.72) for c in (R_RED, PINK, PINK, W_PALE)])
    else:
        pics = VGroup(*[coat_patch(c, ORIGIN, 0.70) for c in ("red", "roan", "roan", "white")])
    pics.arrange(RIGHT, buff=0.55).move_to([0.45, -2.70, 0])
    lab = T("phenotypes", 28, TEAL, weight=BOLD).next_to(pics, DOWN, buff=0.13)
    return VGroup(pics, lab)


def predict_backdrop():
    world = cross_world(False)
    tiles = drifting_tiles(world)
    float_tiles(tiles)
    return VGroup(world, tiles)


def float_tiles(tiles):
    """Sustained calm motion while students trace paths; positions remain centred on their targets."""
    for i, tile in enumerate(tiles):
        tile._float_t = i * 0.8
        base = tile.get_center().copy()

        def drift(mob, dt, base=base, phase=i * 0.8):
            mob._float_t += dt
            mob.move_to(base + 0.10 * RIGHT * np.sin(0.9 * mob._float_t + phase)
                        + 0.08 * UP * np.cos(0.7 * mob._float_t + phase))
        tile.add_updater(drift)
    return tiles


def red_cell(at=(3.85, 0.0, 0), radius=1.75, markers=True):
    cell = Ellipse(width=2 * radius, height=1.35 * radius, color=R_RED, stroke_width=7,
                   fill_color=R_RED, fill_opacity=0.20).move_to(at)
    inner = Ellipse(width=1.20 * radius, height=0.55 * radius, color=R_RED,
                    stroke_width=3).move_to(at).set_opacity(0.6)
    cell.layout_ok = True  # marker blocks intentionally sit on the cell's outer edge
    g = VGroup(cell, inner)
    if markers:
        blocks = VGroup()
        specs = [("A", R_RED, 135), ("B", MARKER_BLUE, 45), ("A", R_RED, 225), ("B", MARKER_BLUE, 315)]
        for letter, color, deg in specs:
            a = deg * DEGREES
            p = np.array(at) + np.array([radius * np.cos(a), 0.68 * radius * np.sin(a), 0])
            b = chip(letter, color, 24, pad=0.12, fill_opacity=0.35).move_to(p)
            blocks.add(b)
        g.add(blocks)
        g.markers = blocks
    return g


class S01Hook(SpokenScene):
    def construct(self):
        left = snapdragon(height=4.1).move_to([-4.65, -0.05, 0])
        right = snapdragon(height=4.1).move_to([4.75, -0.05, 0])
        q = fit_text("Same genotypes — different-looking groups?", 9.2, 38, GOLD).move_to([0, 3.30, 0])
        self.play(FadeIn(left, scale=0.85), FadeIn(right, scale=0.85), FadeIn(q), run_time=1.1)
        bob(left, 0.05, 1.5, 1), bob(right, 0.05, 1.5, 4)
        self.at("Watch pink snapdragons")
        world = cross_world(False)
        self.play(left.animate.scale(0.52).move_to([-4.85, 0.05, 0]),
                  right.animate.scale(0.52).move_to([4.85, 0.05, 0]),
                  FadeOut(q), FadeIn(world.backplate), Create(world.cells), run_time=1.4)
        self.at("send their allele copies")
        lp = VGroup(allele_tile("R", R_RED), allele_tile("W", W_PALE)).arrange(DOWN, buff=0.24).move_to(left)
        lp.shift(RIGHT * 1.20)
        rp = VGroup(allele_tile("R", R_RED), allele_tile("W", W_PALE)).arrange(DOWN, buff=0.24).move_to(right)
        rp.shift(LEFT * 1.20)
        self.play(FadeIn(lp, scale=0.7), FadeIn(rp, scale=0.7), run_time=0.7)
        self.play(Transform(lp, world.left_tiles.copy()), Transform(rp, world.top_tiles.copy()), run_time=2.0)
        self.at("copies will stay fixed")
        ring = RoundedRectangle(corner_radius=0.25, width=5.65, height=5.35, color=TEAL,
                                stroke_width=4).move_to([GRID_C[0], 0.55, 0])
        self.play(Create(ring), run_time=1.2)
        self.at("phenotype rule changes")
        rule1 = chip("phenotype rule", TEAL, 28).move_to([0.45, -2.55, 0])
        rule2 = chip("new phenotype rule", GOLD, 28).move_to(rule1)
        self.play(FadeIn(rule1), run_time=0.7)
        self.play(swap(rule1, rule2), run_time=1.1)
        self.at("track inherited copies separately")
        sep = T("copies  ≠  visible traits", 32, TEXT, weight=BOLD).move_to([0.45, -3.25, 0])
        self.play(FadeOut(rule2), FadeIn(sep), ring.animate.set_color(GOLD), run_time=1.4)
        self.add(scope_tag("schematic", 24))
        self.finish()


class S02Title(TitleCard):
    LESSON = "Beyond Dominance"
    TITLE = "One Cross, Three Patterns"


class S03Setup(SpokenScene):
    def construct(self):
        world = cross_world(False)
        gene_box = RoundedRectangle(corner_radius=0.25, width=3.4, height=2.0,
                                    stroke_color=TEAL, stroke_width=4,
                                    fill_color=TEAL, fill_opacity=0.18).move_to([-4.55, 0.65, 0])
        gene = VGroup(gene_box, T("one gene", 34, TEAL, weight=BOLD).move_to(gene_box))
        self.play(FadeIn(gene), run_time=0.8)
        self.at("Each parent can pass")
        self.play(FadeIn(world.backplate), Create(world.cells), FadeIn(world.targets), run_time=0.9)
        self.play(FadeIn(world.top_tiles, shift=DOWN * 0.25),
                  FadeIn(world.left_tiles, shift=RIGHT * 0.25), run_time=1.3)
        self.at("grid tracks every pairing")
        path_h = VGroup(*[Arrow(t.get_center(), world.cell_map[(0, i)], buff=0.25,
                                     color=GREY, stroke_width=3) for i, t in enumerate(world.top_tiles)])
        path_v = VGroup(*[Arrow(t.get_center(), world.cell_map[(i, 0)], buff=0.25,
                                     color=GREY, stroke_width=3) for i, t in enumerate(world.left_tiles)])
        self.play(LaggedStart(*[GrowArrow(a) for a in [*path_h, *path_v]], lag_ratio=0.15), run_time=1.6)
        lab = T("allele pairings", 30, GOLD, weight=BOLD).move_to([0.45, -2.05, 0])
        self.play(FadeIn(lab), FadeOut(VGroup(path_h, path_v)), run_time=0.8)
        self.at("does not decide")
        unknowns = VGroup(*[T("?", 42, GREY).move_to(p) for p in world.cell_map.values()])
        self.play(FadeOut(world.targets), FadeIn(unknowns), run_time=0.7)
        self.play(Rotate(unknowns, angle=0.08, rate_func=there_and_back), run_time=1.3)
        self.at("Keeping those jobs separate")
        divider = DashedLine([-2.65, -2.55, 0], [3.55, -2.55, 0], color=TEAL, stroke_width=4)
        jobs = T("pair first  •  interpret second", 30, TEAL, weight=BOLD).move_to([0.45, -3.05, 0])
        self.play(FadeOut(gene), Create(divider), FadeIn(jobs), run_time=1.1)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = cross_world(False)
        tiles = drifting_tiles(world)
        self.add(world)
        self.at("predict the combinations")
        self.play(FadeIn(tiles), run_time=0.8)
        float_tiles(tiles)
        q = question_card(QUESTION, y=-3.25, size=30, max_w=10.7)
        self.play(FadeIn(q.question), run_time=0.8)
        self.at("Which pairing repeats")
        d1 = DashedLine(world.top_tiles[0].get_bottom() + DOWN * 0.08, world.cell_map[(0, 0)], color=GOLD, stroke_width=5)
        d2 = DashedLine(world.left_tiles[1].get_right() + RIGHT * 0.08, world.cell_map[(1, 1)], color=GOLD, stroke_width=5)
        self.play(Create(d1), run_time=1.1)
        self.play(ReplacementTransform(d1, d2), run_time=1.1)
        self.at("tiles keep moving")
        shifts = [RIGHT * 0.42, DOWN * 0.42, UP * 0.42, LEFT * 0.42]
        self.play(*[t.animate.shift(s) for t, s in zip(tiles, shifts)], FadeOut(d2), run_time=2.0,
                  rate_func=there_and_back)
        self.at("Look for repeated paths")
        paths = VGroup(DashedLine(world.top_tiles[1].get_bottom() + DOWN * 0.08, world.cell_map[(0, 1)], color=GOLD),
                       DashedLine(world.left_tiles[0].get_right() + RIGHT * 0.08, world.cell_map[(1, 0)], color=GOLD))
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.3), run_time=1.8)
        self.play(FadeOut(paths), *[t.animate.rotate(PI / 2) for t in tiles], run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5
    CARD = {"y": -3.25, "size": 30, "max_w": 10.7}
    RING_AT = (6.0, -3.15, 0)

    def backdrop(self):
        return predict_backdrop()


class S06Reveal(SpokenScene):
    def construct(self):
        empty = cross_world(False)
        self.add(empty.backplate, empty.cells, empty.top_tiles, empty.left_tiles, empty.targets)
        pulse(empty.cells, base=4.0, amp=1.3, speed=1.8)
        order = [((0, 0), "RR"), ((0, 1), "RW"), ((1, 0), "RW"), ((1, 1), "WW")]
        landed = VGroup()
        self.at("tiles land")
        for i, (key, code) in enumerate(order):
            p = allele_pair(code, empty.cell_map[key])
            landed.add(p)
            self.play(FadeIn(p, shift=UP * 0.18), run_time=0.55 if i < 3 else 0.7)
        self.play(FadeOut(empty.targets), run_time=0.3)
        self.at("mixed pairing appears twice")
        self.play(Indicate(landed[1], color=GOLD, scale_factor=1.16),
                  Indicate(landed[2], color=GOLD, scale_factor=1.16), run_time=1.4)
        self.at("genotype pattern comes")
        bar = genotype_bar()
        self.play(FadeIn(bar[0], shift=UP * 0.2), run_time=1.0)
        self.at("changing the phenotype rule")
        self.play(FadeIn(bar[1]), run_time=0.7)
        lens = RoundedRectangle(corner_radius=0.25, width=5.65, height=5.25, color=TEAL, stroke_width=4).move_to([0.45, 0.5, 0])
        self.play(Create(lens), Rotate(lens, angle=0.05, rate_func=there_and_back), run_time=1.6)
        self.at("pink phenotype never")
        parent = snapdragon(PINK, 1.35).move_to([-4.55, -1.7, 0])
        inside = allele_pair("RW", parent.get_center(), 0.48)
        inside[0].shift(LEFT * 0.35)
        inside[1].shift(RIGHT * 0.31)
        self.play(FadeIn(parent), run_time=0.7)
        self.play(FadeIn(inside), parent.animate.set_opacity(0.28), run_time=1.1)
        self.finish()


class S07Incomplete(SpokenScene):
    def construct(self):
        base = cross_world(True)
        self.add(base)
        self.at("lens over the grid")
        outline = RoundedRectangle(corner_radius=0.28, width=5.55, height=4.40,
                                   stroke_color=TEAL, stroke_width=5,
                                   fill_color=TEAL, fill_opacity=0.035).move_to([0.45, 0.10, 0])
        outline.set_z_index(-1)
        pulse(outline, base=5.0, amp=1.5, speed=1.7)
        label = T("incomplete dominance", 30, TEAL, weight=BOLD).move_to([0.45, 3.56, 0])
        self.play(Create(outline), run_time=1.0)
        self.play(FadeIn(label), run_time=0.7)
        vals = [R_RED, W_PALE, PINK]
        keys = [(0, 0), (1, 1), (0, 1)]
        pics = VGroup()
        self.at("Red -red becomes red")
        f = mini_flower(vals[0], base.cell_map[keys[0]] + DOWN * 0.47); pics.add(f)
        self.play(base.pairs[0].animate.shift(UP * 0.36), FadeIn(f, shift=UP * 0.15), run_time=0.9)
        self.at("white -white becomes white")
        f = mini_flower(vals[1], base.cell_map[keys[1]] + DOWN * 0.47); pics.add(f)
        self.play(base.pairs[3].animate.shift(UP * 0.36), FadeIn(f, shift=UP * 0.15), run_time=0.9)
        self.at("red -white becomes pink")
        f1 = mini_flower(vals[2], base.cell_map[(0, 1)] + DOWN * 0.47)
        f2 = mini_flower(vals[2], base.cell_map[(1, 0)] + DOWN * 0.47)
        pics.add(f1, f2)
        self.play(base.pairs[1].animate.shift(UP * 0.36), base.pairs[2].animate.shift(UP * 0.36),
                  FadeIn(f1, shift=UP * 0.15), FadeIn(f2, shift=UP * 0.15), run_time=1.2)
        self.at("Every genotype has")
        self.play(LaggedStart(*[Indicate(p, color=TEAL, scale_factor=1.10) for p in pics], lag_ratio=0.18), run_time=2.0)
        self.at("phenotype pattern matches")
        bar = phenotype_bar("flowers")
        self.play(FadeIn(bar, shift=UP * 0.15), run_time=1.2)
        self.at("color looks blended")
        self.play(Indicate(VGroup(f1, f2), color=PINK, scale_factor=1.12), run_time=1.0)
        self.at("copies remain distinct")
        self.play(Indicate(VGroup(base.pairs[1], base.pairs[2]), color=GOLD, scale_factor=1.16), run_time=1.6)
        self.finish()


class S08Codom(SpokenScene):
    def construct(self):
        flowers = cross_world(True, "flowers", lens="incomplete dominance")
        self.add(flowers)
        self.at("switch to short horn cattle")
        coats = cross_world(True, "coats", title="Shorthorn coat color", lens="codominance")
        coats.title.move_to([-4.65, 3.30, 0])
        self.play(ReplacementTransform(flowers, coats), run_time=1.5)
        self.at("same three pairings")
        self.play(LaggedStart(*[Indicate(p, color=GOLD, scale_factor=1.10) for p in coats.pairs], lag_ratio=0.18), run_time=1.6)
        self.at("give red")
        self.play(LaggedStart(*[FadeIn(p, scale=0.92) for p in coats.phenotypes], lag_ratio=0.18), run_time=1.3)
        self.at("roan red -white calf")
        zoom = coat_patch("roan", [-4.55, -0.2, 0], 2.35)
        zoom_label = T("red hairs + white hairs", 28, TEXT, weight=BOLD).next_to(zoom, DOWN, buff=0.22)
        zoom_label.shift(RIGHT * 0.05)
        self.play(FadeIn(zoom, scale=0.7), run_time=1.0)
        self.at("red hairs and white hairs")
        self.play(FadeIn(zoom_label), run_time=0.8)
        self.play(zoom.animate.scale(1.07), run_time=1.2, rate_func=there_and_back)
        self.at("shows both effects")
        both = VGroup(chip("RED", R_RED, 28), chip("WHITE", W_PALE, 28)).arrange(RIGHT, buff=0.20).move_to([-4.55, 2.1, 0])
        self.play(FadeIn(both), Indicate(zoom, color=GOLD, scale_factor=1.06), run_time=1.3)
        self.at("pairings still do not move")
        self.play(FadeOut(VGroup(zoom, zoom_label, both)),
                  Indicate(coats.pairs, color=TEAL, scale_factor=1.04), run_time=1.5)
        self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        lanes = VGroup(*[
            RoundedRectangle(corner_radius=0.22, width=12.45, height=1.72,
                             stroke_width=0, fill_color="#29313D", fill_opacity=0.94)
            .move_to([0, y, 0]).set_z_index(-3)
            for y in (2.35, 0.15, -2.20)
        ])
        allele_layer = VGroup(allele_pair("RR", [-3.4, 2.35, 0]), allele_pair("RW", [-1.15, 2.35, 0]),
                              allele_pair("RW", [1.15, 2.35, 0]), allele_pair("WW", [3.4, 2.35, 0]))
        grid = VGroup(*[Square(1.42, color=GREY, stroke_width=4) for _ in range(4)]).arrange(RIGHT, buff=0.22).move_to([0, 0.15, 0])
        coats = VGroup(*[coat_patch(k, ORIGIN, 1.02) for k in ("red", "roan", "roan", "white")])
        coats.arrange(RIGHT, buff=0.62).move_to([0, -2.20, 0])
        bracket = VGroup(Line([-6.35, 3.0, 0], [-6.35, -2.85, 0], color=TEAL, stroke_width=5),
                         Line([-6.35, 3.0, 0], [-6.05, 3.0, 0], color=TEAL, stroke_width=5),
                         Line([-6.35, -2.85, 0], [-6.05, -2.85, 0], color=TEAL, stroke_width=5))
        labels = VGroup(T("alleles", 30, R_RED, weight=BOLD).move_to([-5.25, 2.35, 0]),
                        T("genotypes", 30, GOLD, weight=BOLD).move_to([-5.10, 0.15, 0]),
                        T("phenotypes", 30, TEAL, weight=BOLD).move_to([-5.00, -2.20, 0]))
        self.play(FadeIn(lanes), FadeIn(allele_layer), Create(bracket), FadeIn(labels[0]), run_time=1.2)
        self.at("different scale")
        self.play(FadeIn(grid), FadeIn(labels[1]), run_time=1.0)
        self.at("grid reveals allele combinations")
        self.play(LaggedStart(*[TransformFromCopy(a, g) for a, g in zip(allele_layer, grid)], lag_ratio=0.15), run_time=1.8)
        self.at("phenotype key reveals")
        arrows = VGroup(*[Arrow(g.get_bottom(), c.get_top(), buff=0.15, color=TEAL, stroke_width=4)
                          for g, c in zip(grid, coats)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(coats), FadeIn(labels[2]), run_time=1.0)
        self.at("Confusing those views")
        pink = RoundedRectangle(corner_radius=0.16, width=2.55, height=1.28, color=PINK,
                                fill_color=PINK, fill_opacity=0.35).move_to([0, -2.2, 0])
        self.play(FadeIn(pink), run_time=0.8)
        self.play(FadeOut(pink), Indicate(allele_layer[1:3], color=GOLD), run_time=1.2)
        self.at("tool must match")
        rule = T("match the tool to the question", 34, GOLD, weight=BOLD).move_to([0, -3.35, 0])
        self.play(FadeOut(arrows), FadeIn(rule), run_time=1.1)
        self.finish()


class S10Abo(SpokenScene):
    def construct(self):
        panels = VGroup(
            RoundedRectangle(corner_radius=0.25, width=3.45, height=4.25, stroke_width=0,
                             fill_color="#29313D", fill_opacity=0.94).move_to([-4.25, 0.25, 0]),
            RoundedRectangle(corner_radius=0.25, width=6.15, height=6.55, stroke_width=0,
                             fill_color="#29313D", fill_opacity=0.94).move_to([3.55, 0.0, 0]),
        )
        panels.set_z_index(-3)
        cells = VGroup(*[Square(1.32, color=GREY, stroke_width=4) for _ in range(4)]).arrange_in_grid(2, 2, buff=0)
        cells.move_to([-4.25, 0.25, 0])
        codes = ("RR", "RW", "RW", "WW")
        pairs = VGroup(*[allele_pair(code, cell.get_center(), 0.44) for code, cell in zip(codes, cells)])
        grid = VGroup(cells, pairs)
        self.play(FadeIn(panels), FadeIn(grid), run_time=0.9)
        pulse(cells, base=4.0, amp=1.2, speed=1.7)
        bob(grid, amp=0.075, speed=1.15, seed=3)
        self.at("helps with blood type")
        heading = T("ABO blood type", 34, TEXT, weight=BOLD).move_to([3.55, 3.15, 0])
        self.play(FadeIn(heading), run_time=0.7)
        self.at("three common abo alleles")
        population = VGroup(chip("A", R_RED, 28), chip("B", MARKER_BLUE, 28), chip("O", GREY, 28))
        population.arrange(RIGHT, buff=0.25).move_to([3.55, 2.30, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in population], lag_ratio=0.22), run_time=1.1)
        self.at("each person carries a pair")
        pair = VGroup(population[0].copy(), population[1].copy()).arrange(RIGHT, buff=0.25).move_to([3.55, 1.45, 0])
        self.play(TransformFromCopy(population[0], pair[0]), TransformFromCopy(population[1], pair[1]), run_time=1.0)
        self.at("red blood cells display")
        cell = red_cell([3.55, -0.55, 0], 1.65, False)
        self.play(FadeIn(cell, scale=0.8), run_time=1.0)
        self.at("both A and B markers")
        marked = red_cell([3.55, -0.55, 0], 1.65, True)
        self.play(ReplacementTransform(cell, marked), run_time=1.1)
        label = T("type AB: both marker types", 30, TEAL, weight=BOLD).move_to([3.55, -2.55, 0])
        self.play(FadeIn(label), run_time=0.8)
        self.at("Type O cells")
        o_cell = red_cell([3.55, -0.55, 0], 1.65, False)
        bob(o_cell, amp=0.06, speed=1.2, seed=2)
        o_lab = T("O: neither", 28, GREY, weight=BOLD).move_to([3.55, -2.55, 0])
        self.play(ReplacementTransform(marked, o_cell), swap(label, o_lab), run_time=1.0)
        self.at("type A or B")
        self.play(Rotate(o_cell, angle=0.10, rate_func=there_and_back), run_time=1.3)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        cell = red_cell([5.0, 2.35, 0], 0.78, True)
        cell_box = RoundedRectangle(corner_radius=0.18, width=2.25, height=1.95, color=GREY).move_to([5.0, 2.25, 0])
        example = T("AB example", 24, GREY).move_to([5.0, 1.48, 0])
        world = cross_world(True, "flowers", lens="phenotype pattern")
        self.add(cell_box, cell, example, world)
        old = T("Which allele won?", 34, GREY, weight=BOLD).move_to([-4.55, 2.65, 0])
        strike = Line(old.get_left(), old.get_right(), color=R_RED, stroke_width=6)
        strike.layout_ok = True
        self.play(FadeIn(old), Create(strike), run_time=1.0)
        self.at("Ask which alleles")
        q1 = chip("1  Which alleles?", GOLD, 30).move_to([-4.65, 0.75, 0])
        a1 = Arrow(q1.get_right(), world.left_tiles[0].get_left(), buff=0.15, color=GOLD, stroke_width=5)
        self.play(FadeOut(VGroup(old, strike)), FadeIn(q1), GrowArrow(a1), run_time=1.2)
        self.at("then ask what that pair")
        q2 = chip("2  Which phenotype?", TEAL, 30).move_to([-4.55, -1.30, 0])
        a2 = Arrow(q2.get_right(), world.lens_outline.get_left(), buff=0.15, color=TEAL, stroke_width=5)
        self.play(FadeIn(q2), GrowArrow(a2), run_time=1.2)
        self.at("first answer comes")
        self.play(Indicate(VGroup(world.top_tiles, world.left_tiles, world.pairs), color=GOLD, scale_factor=1.04), run_time=1.3)
        self.at("second comes")
        self.play(Indicate(world.phenotypes, color=TEAL, scale_factor=1.07), run_time=1.3)
        self.at("That order keeps")
        rule = T("inherit first  →  interpret second", 34, TEXT, weight=BOLD).move_to([0, -3.35, 0])
        self.play(FadeOut(VGroup(q1, q2, a1, a2)), FadeIn(rule), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "Alleles remain separate; the pattern sets only how each pair shows."
