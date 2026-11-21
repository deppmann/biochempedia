"""The Frame Sets the Message — genetic code and translation explainer.

COLOR MAP (one meaning throughout)
  BLUE  message ribbon / RNA bases
  TEAL  reading window and correctly aligned triplets
  GOLD  selected start and inserted/deleted bases
  GREEN amino-acid outcomes / restored alignment
  RED   too little capacity or translation stop
  GREY  inactive, uncertain, or displaced evidence
"""
from bp_parts import *


SEQ = "CAUGGCUUGGAAACCUGACUA"
TILE_W = 0.60
TILE_H = 1.0
RIBBON_X = -6.15


def tile_x(i, x0=RIBBON_X):
    return x0 + i * TILE_W


def message_ribbon(y=0.35, seq=SEQ, x0=RIBBON_X, start=1, brackets=True,
                   tile_color=BLUE, letter_color=TEXT):
    """The one carried picture: all ribbon scenes call this at identical scale and coordinates."""
    tiles = VGroup()
    for i, base in enumerate(seq):
        box = RoundedRectangle(
            corner_radius=0.08, width=TILE_W - 0.12, height=TILE_H,
            stroke_color=tile_color, stroke_width=2.2,
            fill_color=tile_color, fill_opacity=0.16,
        ).move_to([tile_x(i, x0), y, 0])
        letter = M(base, 28, letter_color).move_to(box)
        tiles.add(VGroup(box, letter))

    groups = VGroup()
    if brackets:
        for first in range(start, len(seq) - 2, 3):
            groups.add(
                RoundedRectangle(
                    corner_radius=0.1, width=3 * TILE_W - 0.04, height=TILE_H + 0.22,
                    stroke_color=TEAL, stroke_width=3.2,
                    fill_color=TEAL, fill_opacity=0.035,
                ).move_to([tile_x(first + 1, x0), y, 0])
            )

    flag_x = tile_x(start, x0)
    pole = Line([flag_x, y + 0.48, 0], [flag_x, y + 1.25, 0], color=GOLD, stroke_width=5)
    pennant = Polygon(
        [flag_x, y + 1.23, 0], [flag_x + 0.48, y + 1.04, 0], [flag_x, y + 0.86, 0],
        color=GOLD, fill_color=GOLD, fill_opacity=0.9, stroke_width=2,
    )
    flag = VGroup(pole, pennant)
    world = VGroup(tiles, groups, flag)
    world.tiles, world.brackets, world.flag = tiles, groups, flag
    world.y, world.x0, world.start = y, x0, start
    return world


def reading_window(first, y=0.35, x0=RIBBON_X, color=TEAL):
    """A three-slot reading window whose dividers fall only in tile gaps."""
    cx = tile_x(first + 1, x0)
    outer = RoundedRectangle(
        corner_radius=0.13, width=3 * TILE_W + 0.12, height=TILE_H + 0.34,
        stroke_color=color, stroke_width=6, fill_color=color, fill_opacity=0.08,
    ).move_to([cx, y, 0])
    dividers = VGroup(*[
        Line([tile_x(first + j, x0) + TILE_W / 2, y - 0.52, 0],
             [tile_x(first + j, x0) + TILE_W / 2, y + 0.52, 0],
             color=color, stroke_width=3)
        for j in (0, 1)
    ])
    return VGroup(outer, dividers)


def shimmer_ribbon(world, speed=1.15, depth=0.62):
    """A slow wave of colour along the message, keeping long spoken holds alive."""
    tiles = world.tiles
    tiles._shimmer_t = 0.0

    def update(mob, dt):
        mob._shimmer_t += dt
        for i, tile in enumerate(mob):
            tile[0].set_fill(opacity=0.12 + depth * (0.5 + 0.5 * np.sin(speed * mob._shimmer_t - i * 0.55)))
    tiles.add_updater(update)
    return world


def shimmer_marks(group, speed=1.1, low=0.48):
    """Gentle opacity wave for capacity dots and evidence rows."""
    group._shimmer_t = 0.0

    def update(mob, dt):
        mob._shimmer_t += dt
        for i, mark in enumerate(mob):
            mark.set_opacity(low + (1 - low) * (0.5 + 0.5 * np.sin(speed * mob._shimmer_t - i * 0.35)))
    group.add_updater(update)
    return group


def amino_blocks(y=-1.35, labels=("Met", "Ala", "Trp", "Lys", "Pro", "Asp"),
                 start=1, color=GREEN):
    blocks = VGroup()
    for k, name in enumerate(labels):
        blocks.add(boxed_label(name, color, size=26, box=(1.55, 0.68), pad=0.14).move_to(
            [tile_x(start + 1 + 3 * k), y, 0]))
    return blocks


def predict_backdrop():
    world = message_ribbon(y=0.65)
    insert = VGroup(
        RoundedRectangle(corner_radius=0.08, width=TILE_W - 0.035, height=TILE_H,
                         stroke_color=GOLD, stroke_width=3, fill_color=BLUE, fill_opacity=0.2),
        M("?", 31, GOLD),
    ).move_to([tile_x(4) + TILE_W / 2, 2.05, 0])
    near = boxed_label("nearby only", TEXT, size=27).move_to([-2.55, -1.25, 0])
    all_down = boxed_label("all downstream codons", TEXT, size=27).move_to([2.25, -1.25, 0])
    return VGroup(world, insert, near, all_down)


def trial_row(y, mode="opposite"):
    """A compact copy of the same ribbon for the three experimental shift trials."""
    seq = SEQ[:18]
    row = message_ribbon(y=y, seq=seq, x0=-4.8, start=1, brackets=True)
    shimmer_ribbon(row, speed=0.9)
    row.flag.set_opacity(0)
    if mode == "opposite":
        marks = VGroup(T("+", 30, GOLD).move_to([-1.7, y + 1.15, 0]),
                       T("−", 30, GOLD).move_to([0.0, y + 1.15, 0]))
        tail = Line([0.1, y - 0.58, 0], [4.9, y - 0.58, 0], color=TEAL, stroke_width=5)
    elif mode == "same":
        marks = VGroup(T("+", 30, GOLD).move_to([-1.7, y + 1.15, 0]),
                       T("+", 30, GOLD).move_to([0.0, y + 1.15, 0]))
        tail = Line([0.1, y - 0.58, 0], [4.9, y - 0.58, 0], color=GREY, stroke_width=5)
    else:
        marks = VGroup(*[T("+", 30, GOLD).move_to([-1.7 + 1.35 * i, y + 1.15, 0]) for i in range(3)])
        tail = Line([0.1, y - 0.58, 0], [4.9, y - 0.58, 0], color=TEAL, stroke_width=5)
    return VGroup(row, marks, tail)


class S00Hook(TitleCard, SpokenScene):
    LESSON = "The Genetic Code and Translation"
    TITLE = "The Frame Sets the Message"

    def construct(self):
        world = message_ribbon(y=-0.15, brackets=False)
        shimmer_ribbon(world)
        window = reading_window(1, y=-0.15).shift(UP * 1.2)
        q = T("Which groups will the cell read?", 38, GOLD).move_to([-0.5, 2.85, 0])
        tag = scope_tag("schematic")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in world.tiles], lag_ratio=0.03),
                  run_time=1.4)
        self.at("regroup every downstream")
        self.play(FadeIn(q), FadeIn(world.flag, shift=DOWN * 0.2), run_time=0.7)
        self.at("answer lies")
        self.play(FadeIn(window, shift=DOWN * 0.2), FadeIn(tag), run_time=0.7)
        self.at("continuous message")
        self.play(window.animate.shift(RIGHT * 2.1), run_time=2.1, rate_func=there_and_back)
        self.at("same ribbon")
        self.play(Indicate(world.tiles, color=BLUE, scale_factor=1.03), run_time=1.2)
        self.at("letters will stay fixed")
        pulse(window[0], base=6, amp=2, speed=3)
        self.wait(1.4)
        self.at("deliberately change")
        self.play(window.animate.shift(RIGHT * 1.2), run_time=1.1, rate_func=there_and_back)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = message_ribbon(y=-1.25, brackets=False)
        shimmer_ribbon(world)
        window = reading_window(4, y=-1.25)
        title = T("The Frame Sets the Message", 50, TEXT, font=TITLE_FONT).move_to([-0.5, 1.35, 0])
        self.add(world, window, scope_tag("schematic"))
        pulse(window[0], base=6, amp=2, speed=3)
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.55)
        self.wait(0.8)
        self.play(FadeOut(title), run_time=0.35)
        self.finish()


class S02Window(SpokenScene):
    def construct(self):
        world = message_ribbon(y=0.15, brackets=False)
        shimmer_ribbon(world)
        window = reading_window(1, y=0.15).shift(UP * 1.35)
        self.add(world.tiles)
        self.at("starting place")
        self.play(FadeIn(world.flag, shift=DOWN * 0.2), run_time=0.7)
        self.at("initiation selects")
        self.play(Indicate(world.flag, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.at("reading window locks")
        target = reading_window(1, y=0.15)
        self.play(FadeIn(window), run_time=0.35)
        self.play(FadeOut(window), FadeIn(target), run_time=0.65)
        window = target
        codon = T("codon", 30, TEAL).next_to(target, DOWN, buff=0.3)
        self.at("covers a triplet")
        self.play(FadeIn(codon), world.tiles[1:4].animate.shift(UP * 0.08), run_time=0.7)
        self.at("advances to the next")
        next_window = reading_window(4, y=0.15)
        self.play(swap(window, next_window), world.tiles[1:4].animate.shift(DOWN * 0.08),
                  world.tiles[4:7].animate.shift(UP * 0.08), run_time=1.0)
        window = next_window
        codon2 = T("codon", 30, TEAL).move_to(codon).shift(RIGHT * 3 * TILE_W)
        self.play(swap(codon, codon2), run_time=0.45)
        self.at("Each window position")
        last_window = reading_window(7, y=0.15)
        self.play(swap(window, last_window),
                  world.tiles[4:7].animate.shift(DOWN * 0.08),
                  world.tiles[7:10].animate.shift(UP * 0.08),
                  codon2.animate.shift(RIGHT * 3 * TILE_W), run_time=1.25)
        self.finish()


class S03Frame(SpokenScene):
    def construct(self):
        upper = message_ribbon(y=1.25, start=1, brackets=False)
        lower = message_ribbon(y=-1.25, start=2, brackets=False)
        shimmer_ribbon(upper)
        shimmer_ribbon(lower, speed=0.95)
        wu = reading_window(1, y=1.25)
        wl = reading_window(2, y=-1.25)
        self.add(upper.tiles, lower.tiles)
        self.at("alignment between")
        self.play(FadeIn(upper.flag), FadeIn(wu), run_time=0.75)
        self.at("different base")
        self.play(FadeIn(lower.flag), FadeIn(wl), run_time=0.75)
        self.at("every box contains")
        wu2, wl2 = reading_window(4, y=1.25), reading_window(5, y=-1.25)
        self.play(swap(wu, wu2), swap(wl, wl2), run_time=0.9)
        wu, wl = wu2, wl2
        wu3, wl3 = reading_window(7, y=1.25), reading_window(8, y=-1.25)
        self.play(swap(wu, wu3), swap(wl, wl3), run_time=0.9)
        wu, wl = wu3, wl3
        self.at("same base")
        fresh = reading_window(1, y=0.15)
        self.play(FadeOut(wl), FadeOut(wu), FadeIn(fresh), lower.animate.set_opacity(0.22),
                  upper.animate.shift(DOWN * 1.1), run_time=1.0)
        wu = fresh
        self.at("boxes remain fixed")
        fixed = message_ribbon(y=0.15, start=1, brackets=True).brackets
        self.play(LaggedStart(*[Create(b) for b in fixed], lag_ratio=0.18), run_time=1.5)
        self.at("window moves")
        last = reading_window(7, y=0.15)
        self.play(swap(wu, last), run_time=1.0)
        self.at("fixed start makes")
        rule = caption("A fixed start makes each next triplet a codon.", color=TEAL)
        self.play(FadeIn(rule), run_time=0.65)
        self.finish()


class S04Capacity(SpokenScene):
    def construct(self):
        carried = message_ribbon(y=0.15, brackets=False)
        shimmer_ribbon(carried)
        self.add(carried.tiles)

        # Top row of the 4 distinct RNA bases transformed from the carried ribbon.
        base_idx = (0, 1, 2, 4)  # A, U, G, C in SEQ
        base_xs = (-2.1, -1.4, -0.7, 0.0)
        base_tiles = VGroup()
        for letter, bx in zip(("A", "U", "G", "C"), base_xs):
            box = RoundedRectangle(
                corner_radius=0.07, width=0.52, height=0.68,
                stroke_color=BLUE, stroke_width=2.2,
                fill_color=BLUE, fill_opacity=0.18,
            ).move_to([bx, 2.88, 0])
            base_tiles.add(VGroup(box, M(letter, 26, TEXT).move_to(box)))
        bases_lbl = T("4 bases", 28, BLUE).next_to(base_tiles, LEFT, buff=0.28)

        # Three grid panels on the left/center, leaving x = 3.05..6.25 for the 20 amino acids comparison bar.
        panel_xs = (-4.85, -1.80, 1.25)
        panels = VGroup(*[
            RoundedRectangle(
                corner_radius=0.16, width=2.85, height=3.50, stroke_color=GREY,
                stroke_width=2, fill_color=GREY, fill_opacity=0.04,
            ).move_to([x, 0.40, 0])
            for x in panel_xs
        ]).set_z_index(-2)
        panels._shimmer_t = 0.0

        def breathe_panels(mob, dt):
            mob._shimmer_t += dt
            for i, panel in enumerate(mob):
                panel.set_fill(opacity=0.04 + 0.11 * (0.5 + 0.5 * np.sin(0.9 * mob._shimmer_t - i * 1.2)))
        panels.add_updater(breathe_panels)

        heads = VGroup(
            T("single", 28, TEXT).move_to([panel_xs[0], 1.85, 0]),
            T("pairs", 28, TEXT).move_to([panel_xs[1], 1.85, 0]),
            T("triplets", 28, TEAL).move_to([panel_xs[2], 1.85, 0]),
        )

        def dot_grid(n, center, color):
            dots = VGroup(*[Dot(radius=0.068 if n > 16 else (0.095 if n == 16 else 0.125), color=color) for _ in range(n)])
            cols = 8 if n == 64 else (4 if n == 16 else 2)
            rows = n // cols
            dots.arrange_in_grid(rows, cols, buff=0.085 if n == 64 else (0.14 if n == 16 else 0.22)).move_to(center)
            return dots

        grids = [
            dot_grid(4, [panel_xs[0], 0.62, 0], RED),
            dot_grid(16, [panel_xs[1], 0.62, 0], RED),
            dot_grid(64, [panel_xs[2], 0.62, 0], TEAL),
        ]
        for i, grid in enumerate(grids):
            shimmer_marks(grid, speed=0.9 + 0.12 * i)

        # Formulas & capacity digits positioned beneath each grid inside its panel.
        f0 = M("4", 34, RED).move_to([panel_xs[0], -0.82, 0])
        f1_parts = VGroup(M("4", 28, RED), M("×4", 28, RED), M("= 16", 28, RED)).arrange(RIGHT, buff=0.08)
        f1_parts.move_to([panel_xs[1], -0.82, 0])
        f2_parts = VGroup(M("4", 26, TEAL), M("×4", 26, TEAL), M("×4", 26, TEAL), M("= 64", 26, TEAL)).arrange(RIGHT, buff=0.06)
        f2_parts.move_to([panel_xs[2], -0.82, 0])

        # Comparison bar chart on the right (computed heights proportional to capacity / 64).
        bar_y0, bar_h = -1.05, 2.80
        bar_xs = (3.85, 4.70, 5.55)
        bar_axis = VGroup(
            Line([3.25, bar_y0, 0], [6.05, bar_y0, 0], color=GREY, stroke_width=2.5),
            Line([3.25, bar_y0, 0], [3.25, bar_y0 + bar_h + 0.12, 0], color=GREY, stroke_width=2.5),
        )

        def make_bar(val, x, color):
            h = (val / 64.0) * bar_h
            rect = Rectangle(width=0.46, height=h, stroke_color=color, stroke_width=2.5,
                             fill_color=color, fill_opacity=0.65)
            rect.move_to([x, bar_y0 + h / 2, 0])
            lbl = M(str(val), 24, color).move_to([x, bar_y0 - 0.30, 0])
            return VGroup(rect, lbl)

        bar4 = make_bar(4, bar_xs[0], RED)
        bar16 = make_bar(16, bar_xs[1], RED)
        bar64 = make_bar(64, bar_xs[2], TEAL).set_z_index(1)

        y20 = bar_y0 + (20.0 / 64.0) * bar_h
        line20 = DashedLine([3.25, y20, 0], [6.05, y20, 0], color=GREEN, stroke_width=4, dash_length=0.12)
        line20.set_z_index(-1)
        lbl20 = T("20 amino\nacids", 24, GREEN, line_spacing=0.85).move_to([4.18, y20 + 0.50, 0])

        # 1. "With 4 bases," (4 at 0.44)
        self.at("4 bases", lead=0.0)
        extra_tiles = VGroup(*[carried.tiles[i] for i in range(len(carried.tiles)) if i not in base_idx])
        self.play(
            *[Transform(carried.tiles[idx], base_tiles[k]) for k, idx in enumerate(base_idx)],
            FadeOut(extra_tiles),
            FadeIn(bases_lbl),
            run_time=0.80,
        )

        # 2. "singles give 4 words," (singles at 1.70, 4 at 2.20)
        self.at("singles give")
        base_boxes = VGroup(*[b[0] for b in base_tiles])
        self.play(
            FadeIn(panels[0]), FadeIn(heads[0]),
            ReplacementTransform(base_boxes.copy(), grids[0]),
            run_time=0.65,
        )
        self.at("4 words", lead=0.0)
        self.play(FadeIn(f0, shift=UP * 0.1), FadeIn(bar_axis), FadeIn(bar4), run_time=0.45)
        self.play(Indicate(f0, color=GOLD, scale_factor=1.08), run_time=0.35)

        # 3. "and pairs give 4 times 4 or 16." (pairs at 3.34, 4 at 3.82, times 4 at 4.16, 16 at 5.02)
        self.at("pairs give")
        self.play(
            FadeIn(panels[1]), FadeIn(heads[1]),
            ReplacementTransform(base_boxes.copy(), grids[1]),
            run_time=0.60,
        )
        self.at("4 times", lead=0.0)
        self.play(FadeIn(f1_parts[0]), run_time=0.30)
        self.at("times 4", lead=0.0)
        self.play(FadeIn(f1_parts[1]), run_time=0.40)
        self.at("16", lead=0.0)
        self.play(FadeIn(f1_parts[2], shift=UP * 0.1), FadeIn(bar16), run_time=0.45)
        self.play(Indicate(f1_parts, color=GOLD, scale_factor=1.06), run_time=0.55)

        # 4. "Both are fewer than 20 amino acids." (Both at 6.84, 20 at 7.76)
        self.at("Both are fewer")
        few0 = T("too few", 28, RED).move_to([panel_xs[0], -1.78, 0])
        few1 = T("too few", 28, RED).move_to([panel_xs[1], -1.78, 0])
        self.play(
            FadeIn(few0), FadeIn(few1),
            Indicate(VGroup(grids[0], grids[1]), color=RED, scale_factor=1.03),
            run_time=0.75,
        )
        self.at("20 amino", lead=0.0)
        self.play(Create(line20), FadeIn(lbl20), run_time=0.75)

        # 5. "Triplets give 4 times 4 times 4, or 64, which is enough."
        self.at("Triplets give")
        self.play(
            FadeIn(panels[2]), FadeIn(heads[2]),
            ReplacementTransform(base_boxes.copy(), grids[2]),
            run_time=0.60,
        )
        self.at("4 times", lead=0.0, nth=1)
        self.play(FadeIn(f2_parts[0]), run_time=0.28)
        self.at("times 4", lead=0.0, nth=1)
        self.play(FadeIn(f2_parts[1]), run_time=0.35)
        self.at("times 4", lead=0.0, nth=2)
        self.play(FadeIn(f2_parts[2]), run_time=0.38)
        self.at("64", lead=0.0)
        self.play(
            FadeIn(f2_parts[3], shift=UP * 0.1),
            GrowFromEdge(bar64[0], DOWN), FadeIn(bar64[1]),
            run_time=0.55,
        )
        self.at("which is enough")
        enough = T("enough", 28, TEAL).move_to([panel_xs[2], -1.78, 0])
        self.play(FadeIn(enough), Indicate(VGroup(f2_parts, bar64[0]), color=GOLD, scale_factor=1.05), run_time=0.65)

        # 6. "So fixed-length words must be at least triplets."
        self.at("at least triplets")
        self.play(Indicate(VGroup(heads[2], grids[2], f2_parts), color=TEAL, scale_factor=1.04), run_time=0.95)

        # 7. "Only experiments could test the real reading unit."
        self.at("Only experiments")
        actual = VGroup(T("?", 40, GREY), T("actual unit?", 28, GREY)).arrange(DOWN, buff=0.08).move_to([0, -2.75, 0])
        self.play(FadeIn(actual), run_time=0.75)
        self.finish()


class S05Substitution(SpokenScene):
    def construct(self):
        world = message_ribbon(y=1.0)
        shimmer_ribbon(world)
        blocks = amino_blocks(y=-0.75)
        self.add(world, blocks)
        changed = 8
        replacement = VGroup(world.tiles[changed][0].copy().set_stroke(GOLD).set_fill(BLUE, 0.2),
                             M("C", 28, TEXT).move_to(world.tiles[changed])).move_to(world.tiles[changed])
        self.at("replace a base")
        self.play(Transform(world.tiles[changed], replacement), run_time=0.75)
        self.at("boundaries do not move")
        self.play(Indicate(world.brackets, color=TEAL, scale_factor=1.02), run_time=1.0)
        outcome = boxed_label("same", GREEN, size=28, box=(1.55, 0.68)).move_to(blocks[2])
        self.at("keep the same")
        self.play(swap(blocks[2], outcome), run_time=0.65)
        current = outcome
        outcome2 = boxed_label("different", GOLD, size=28, box=(1.55, 0.68)).move_to(blocks[2])
        self.at("another amino acid")
        self.play(swap(current, outcome2), run_time=0.65)
        current = outcome2
        stop = boxed_label("stop", RED, size=28, box=(1.55, 0.68)).move_to(blocks[2])
        self.at("become a stop")
        self.play(swap(current, stop), run_time=0.65)
        self.at("Later codons")
        bob(blocks[3], amp=0.05, seed=1)
        bob(blocks[4], amp=0.05, seed=2)
        bob(blocks[5], amp=0.05, seed=3)
        self.play(Indicate(VGroup(*world.brackets[3:]), color=TEAL, scale_factor=1.03), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        world, insert, near, all_down = back
        shimmer_ribbon(world)
        self.add(world)
        self.at("base is inserted")
        self.play(FadeIn(insert, shift=DOWN * 0.25), run_time=0.7)
        pulse(insert[0], base=3, amp=2, speed=3)
        self.at("only the nearest")
        self.play(FadeIn(near), run_time=0.6)
        self.at("every downstream")
        self.play(FadeIn(all_down), run_time=0.6)
        self.at("Hold the reading")
        q = question_card("Which codons will be regrouped?", y=-2.85, max_w=8.8)
        self.play(FadeIn(q.question), run_time=0.6)
        self.at("follow the ribbon")
        self.play(Indicate(world.tiles[4:], color=BLUE, scale_factor=1.025), run_time=1.0)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which codons will be regrouped?"
    OPTIONS = ()
    CARD = {"y": -2.85, "max_w": 8.8}
    SECONDS = 4.5

    def backdrop(self):
        back = predict_backdrop()
        shimmer_ribbon(back[0])
        return back


class S08Insert(SpokenScene):
    def construct(self):
        world = message_ribbon(y=1.15)
        shimmer_ribbon(world)
        blocks = amino_blocks(y=-0.6)
        inserted = VGroup(
            RoundedRectangle(corner_radius=0.08, width=TILE_W - 0.035, height=TILE_H,
                             stroke_color=GOLD, stroke_width=3, fill_color=BLUE, fill_opacity=0.2),
            M("G", 28, GOLD),
        ).move_to([tile_x(4) + TILE_W / 2, 2.65, 0])
        self.add(world, blocks)
        self.at("new base joins")
        shifted_tiles = world.tiles[4:].copy().shift(RIGHT * TILE_W)
        self.play(FadeIn(inserted), inserted.animate.move_to([tile_x(4), 1.15, 0]),
                  FadeOut(world.tiles[4:]), run_time=0.48)
        self.play(FadeIn(shifted_tiles), run_time=0.52)
        self.at("Every downstream letter slides")
        self.play(Indicate(VGroup(inserted, shifted_tiles), color=GOLD, scale_factor=1.025), run_time=1.0)
        self.at("New triplets appear")
        questions = VGroup(*[boxed_label("?", GREY, size=28, box=(1.55, 0.68)).move_to(b) for b in blocks[1:]])
        self.play(*[swap(blocks[i + 1], questions[i]) for i in range(len(questions))], run_time=0.8)
        current = list(questions)
        names = ("Gly", "Leu", "Glu", "Thr")
        for i, name in enumerate(names):
            new = boxed_label(name, GREEN, size=27, box=(1.55, 0.68)).move_to(blocks[i + 1])
            self.play(swap(current[i], new), run_time=0.42)
            current[i] = new
        self.at("until a stop")
        stop = boxed_label("stop", RED, size=28, box=(1.55, 0.68)).move_to(blocks[5])
        self.play(swap(current[4], stop), world.brackets[5].animate.set_color(RED), run_time=0.7)
        self.at("This is a frame shift")
        lab = caption("frameshift: the grouping changed", color=GOLD)
        self.play(FadeIn(lab), run_time=0.65)
        self.at("not merely a letter")
        self.play(Indicate(world.brackets[1:], color=TEAL, scale_factor=1.025), run_time=1.0)
        self.finish()


class S09PlusMinus(SpokenScene):
    def construct(self):
        labels = VGroup(T("opposite shifts", 28, TEXT).move_to([-4.85, 2.65, 0]),
                        T("same-sign shifts", 28, TEXT).move_to([-4.7, 0.25, 0]),
                        T("three same-sign", 28, TEXT).move_to([-4.65, -2.15, 0]))
        r1, r2, r3 = trial_row(1.75, "opposite"), trial_row(-0.65, "same"), trial_row(-3.05, "triple")
        self.at("plus and minus")
        self.play(FadeIn(labels[0]), FadeIn(r1[0]), FadeIn(r1[1]), run_time=0.9)
        self.at("often restored function")
        note = T("often restored function\nin tested combinations", 26, GREEN).move_to([3.9, 2.88, 0])
        self.play(Create(r1[2]), FadeIn(note), run_time=0.8)
        self.at("Same sign shifts")
        self.play(FadeIn(labels[1]), FadeIn(r2[0]), FadeIn(r2[1]), run_time=0.85)
        self.at("did not restore")
        self.play(Create(r2[2]), run_time=0.7)
        self.at("complete triplet")
        self.play(FadeIn(labels[2]), FadeIn(r3[0]), LaggedStart(*[FadeIn(m) for m in r3[1]], lag_ratio=0.2), run_time=1.0)
        self.at("later message")
        self.play(Create(r3[2]), run_time=0.8)
        self.at("earlier grouping")
        self.play(Indicate(VGroup(r1[2], r3[2]), color=TEAL, scale_factor=1.02), run_time=0.8)
        self.finish()


class S10Restoration(SpokenScene):
    def construct(self):
        board = RoundedRectangle(corner_radius=0.18, width=7.0, height=5.3, stroke_color=GREY,
                                 stroke_width=2.5, fill_color=GREY, fill_opacity=0.04).move_to([-2.6, 0, 0])
        start = Line([-5.2, -2.0, 0], [-5.2, 2.0, 0], color=GOLD, stroke_width=6)
        rows = VGroup(*[Line([-4.8, y, 0], [0.3, y, 0], color=c, stroke_width=7)
                        for y, c in ((1.35, TEAL), (0, GREY), (-1.35, TEAL))])
        shimmer_marks(rows, speed=0.8, low=0.55)
        board._shimmer_t = 0.0
        board.add_updater(lambda m, dt: (setattr(m, "_shimmer_t", m._shimmer_t + dt),
                                         m.set_fill(opacity=0.05 + 0.06 * (0.5 + 0.5 * np.sin(m._shimmer_t))))[-1])
        self.add(board, start, rows)
        self.at("often restored gene function")
        self.play(Indicate(VGroup(rows[0], rows[2]), color=GREEN, scale_factor=1.03), run_time=0.9)
        supported = T("supported", 32, GOLD).move_to([3.5, 2.0, 0])
        self.at("They supported")
        self.play(FadeIn(supported), run_time=0.5)
        fixed = boxed_label("fixed reading point", TEAL, size=29).move_to([3.5, 0.65, 0])
        self.at("fixed reading point")
        self.play(FadeIn(fixed, shift=UP * 0.15), run_time=0.7)
        trip = boxed_label("triplet or multiple", GREEN, size=29).move_to([3.5, -0.75, 0])
        self.at("triplet or a multiple")
        self.play(FadeIn(trip, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S11Dictionary(SpokenScene):
    def construct(self):
        board = RoundedRectangle(corner_radius=0.16, width=4.2, height=5.3, stroke_color=GREY,
                                 stroke_width=2.5).move_to([-4.25, 0.15, 0])
        board._shimmer_t = 0.0
        board.set_fill(GREY, 0.04)
        board.add_updater(lambda m, dt: (setattr(m, "_shimmer_t", m._shimmer_t + dt),
                                         m.set_fill(opacity=0.04 + 0.1 * (0.5 + 0.5 * np.sin(m._shimmer_t))))[-1])
        fixed = T("fixed frame", 29, TEAL).move_to([-4.25, 1.25, 0])
        unknown = T("dictionary ?", 31, GREY).move_to([-4.25, -0.25, 0])
        self.add(board, fixed, unknown)
        self.at("did not assign")
        self.play(Indicate(unknown, color=GREY, scale_factor=1.08), run_time=0.8)
        tube = RoundedRectangle(corner_radius=0.35, width=2.2, height=3.4, stroke_color=TEXT,
                                stroke_width=4, fill_color=BLUE, fill_opacity=0.06).move_to([2.5, 0.5, 0])
        rna = boxed_label("RNA", BLUE, size=29).move_to([2.5, 1.15, 0])
        aas = VGroup(*[Dot(radius=0.14, color=GREEN) for _ in range(5)]).arrange(RIGHT, buff=0.18).move_to([2.5, -0.05, 0])
        self.at("Cell free translation")
        self.play(FadeIn(tube), FadeIn(rna, shift=DOWN * 0.2), FadeIn(aas), run_time=0.9)
        self.at("ribosome binding tests")
        filt = Line([1.0, -0.2, 0], [5.5, -0.2, 0], color=GREY, stroke_width=5)
        ribo = boxed_label("ribosome", TEAL, size=28).move_to([3.1, 0.35, 0])
        self.play(FadeOut(tube), FadeIn(filt), Transform(rna, ribo),
                  aas.animate.shift(DOWN * 1.15), run_time=1.0)
        self.at("linked defined")
        codon = boxed_label("codon", BLUE, size=28).move_to([-1.25, -1.6, 0])
        amino = boxed_label("amino acid", GREEN, size=28).move_to([2.25, -1.6, 0])
        link = Arrow(codon.get_right() + RIGHT * 0.12, amino.get_left() + LEFT * 0.12,
                     color=GOLD, stroke_width=4, buff=0.02)
        self.play(FadeIn(codon), Create(link), FadeIn(amino), run_time=0.9)
        self.at("codons with assignments")
        assigned = T("codon assignments", 30, GREEN).move_to(unknown)
        self.play(swap(unknown, assigned), run_time=0.7)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        world = message_ribbon(y=0.5)
        shimmer_ribbon(world)
        window = reading_window(1, y=0.5)
        self.add(world, window)
        changed = world.tiles[8].copy()
        changed[0].set_stroke(GOLD).set_fill(BLUE, 0.2)
        changed[1].become(M("C", 28, TEXT).move_to(changed[0]))
        self.at("substitution can alter")
        self.play(Transform(world.tiles[8], changed), run_time=0.75)
        self.at("without moving later")
        self.play(Indicate(world.brackets[3:], color=TEAL, scale_factor=1.02), run_time=0.9)
        insert = world.tiles[4].copy().set_color(GOLD)
        insert[1].set_color("#10141C")
        insert.move_to([tile_x(4) + TILE_W / 2, 2.2, 0])
        self.at("insertion or deletion")
        self.play(FadeIn(insert), run_time=0.55)
        self.at("moves the downstream frame")
        shifted = world.brackets[1:].copy().shift(RIGHT * TILE_W)
        self.play(insert.animate.move_to([tile_x(4), 0.5, 0]),
                  *[t.animate.shift(RIGHT * TILE_W) for t in world.tiles[4:]],
                  FadeOut(world.brackets[1:]), run_time=0.55)
        self.play(FadeIn(shifted), run_time=0.45)
        self.at("lasting lesson")
        original = message_ribbon(y=0.5)
        shimmer_ribbon(original)
        fresh_window = reading_window(1, y=0.5)
        self.play(FadeOut(VGroup(world, window, insert)), FadeIn(original), FadeIn(fresh_window), run_time=0.9)
        self.at("Keep the starting register")
        rule = caption("Keep the starting register, and every later codon keeps its place.", color=TEAL)
        self.play(FadeIn(rule), run_time=0.7)
        self.at("every later codon")
        for first in (4, 7, 10):
            nxt = reading_window(first, y=0.5)
            self.play(swap(fresh_window, nxt), run_time=0.82)
            fresh_window = nxt
        self.finish()


class S13End(EndCard):
    LINE = "A fixed start makes each next triplet a codon."
