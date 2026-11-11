"""Sealed or Torn — cell death and clearance.

COLOR MAP (fixed throughout)
  BLUE   plasma membrane
  TEAL   caspases
  YELLOW phosphatidylserine / eat-me signal
  GREEN  phagocyte
  RED    leaked contents, alarms, inflammation
  GREY   nuclei, outlines, other cells
"""
from bp_style import *  # noqa: F401,F403


CELL_C = np.array([-2.35, -0.15, 0.0])
CELL_R = 2.18


def breathe(ring, color=BLUE, base=0.17, swing=0.035):
    """A slow, continuous readout of an intact living boundary."""
    ring._breath_t = 0.0
    ring._breath_scale = 1.0

    def update(m, dt):
        m._breath_t += dt
        m.set_fill(color, opacity=base + swing * np.sin(1.35 * m._breath_t))
        target_scale = 1.0 + 0.012 * np.sin(1.35 * m._breath_t)
        m.scale(target_scale / m._breath_scale)
        m._breath_scale = target_scale

    ring.add_updater(update)
    return ring


def membrane_cell(center=CELL_C, radius=CELL_R, nucleus=True, fill=0.17):
    ring = Circle(radius=radius, color=BLUE, stroke_width=9,
                  fill_color=BLUE, fill_opacity=fill).move_to(center)
    breathe(ring, BLUE, fill)
    parts = [ring]
    if nucleus:
        nuc = Circle(radius=radius * 0.34, color=GREY, stroke_width=4,
                     fill_color=GREY, fill_opacity=0.22).move_to(center + 0.12 * UR)
        parts.append(nuc)
    return VGroup(*parts)


def scissors(scale=1.0):
    """A labelled-cartoon action mark, not a molecular structure."""
    a = Line(0.28 * DL, 0.38 * UR, color=TEAL, stroke_width=5)
    b = Line(0.28 * UL, 0.38 * DR, color=TEAL, stroke_width=5)
    h1 = Circle(radius=0.12, color=TEAL, stroke_width=4).move_to(0.39 * DL)
    h2 = Circle(radius=0.12, color=TEAL, stroke_width=4).move_to(0.39 * UL)
    return VGroup(a, b, h1, h2).scale(scale)


def caspase_group(center=CELL_C):
    return VGroup(
        scissors(0.72).move_to(center + [-0.46, 0.34, 0]),
        scissors(0.64).move_to(center + [0.50, -0.26, 0]),
    )


def surface_heads(center=CELL_C, radius=CELL_R, n=10):
    return VGroup(*[
        Dot(center + (radius + 0.06) * np.array([np.cos(a), np.sin(a), 0]),
            radius=0.075, color=YELLOW)
        for a in np.linspace(0, TAU, n, endpoint=False)
    ])


def blebs(center=CELL_C, radius=CELL_R):
    return VGroup(
        Circle(radius=0.31, color=BLUE, stroke_width=6,
               fill_color=BLUE, fill_opacity=0.04).move_to(center + [radius + 0.23, 0.42, 0]),
        Circle(radius=0.23, color=BLUE, stroke_width=6,
               fill_color=BLUE, fill_opacity=0.04).move_to(center + [-0.52, radius + 0.13, 0]),
    )


def apoptotic_world(with_heads=False, with_blebs=True):
    cell = membrane_cell()
    # Four nucleus fragments are rebuilt in the same place in every continuation.
    cell.remove(cell[1])
    frags = VGroup(*[
        Circle(radius=0.18, color=GREY, stroke_width=3,
               fill_color=GREY, fill_opacity=0.38).move_to(CELL_C + d)
        for d in ([-0.35, 0.26, 0], [0.22, 0.32, 0], [-0.18, -0.27, 0], [0.34, -0.22, 0])
    ])
    g = VGroup(cell[0], frags, caspase_group())
    if with_blebs:
        g.add(blebs())
    if with_heads:
        g.add(surface_heads())
    return g


def phagocyte(center=(4.7, -0.2, 0), radius=1.78):
    edge = Circle(radius=radius, color=GREEN, stroke_width=8,
                  fill_color=GREEN, fill_opacity=0.18).move_to(center)
    breathe(edge, GREEN, 0.18, 0.025)
    nuc = Circle(radius=0.42, color=GREEN, stroke_width=3,
                 fill_color=GREEN, fill_opacity=0.20).move_to(np.array(center) + [0.35, 0.28, 0])
    return VGroup(edge, nuc)


def find_cloud():
    return VGroup(*[
        Dot([x, y, 0], radius=0.055 + 0.012 * (i % 2), color=TEXT).set_opacity(0.85 - 0.05 * i)
        for i, (x, y) in enumerate([
            (-0.72, 0.25), (-0.22, 0.45), (0.25, 0.18), (0.75, 0.48),
            (1.18, 0.10), (1.62, 0.34), (2.02, 0.02), (2.42, 0.28),
        ])
    ])


def worm_outline(x=0, scale=1.0):
    """A simple tapered C. elegans outline in side view."""
    pts = [
        [-0.95, -2.25], [-1.18, -1.45], [-1.02, -0.45], [-1.15, 0.55],
        [-0.88, 1.48], [-0.28, 2.23], [0.28, 2.30], [0.92, 1.53],
        [1.12, 0.56], [1.00, -0.42], [1.13, -1.35], [0.92, -2.18],
    ]
    path = VMobject(color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)
    path.set_points_smoothly([np.array([x + scale * a, scale * b, 0]) for a, b in pts] +
                             [np.array([x + scale * pts[0][0], scale * pts[0][1], 0])])
    breathe(path, GREY, 0.14, 0.025)
    return path


def worm_cells(x=0, scale=1.0, color=GREY):
    # Exactly 131 repeated positions: an 11 x 12 field plus the central cell.
    pos = []
    for j in range(12):
        yy = -1.80 + j * 0.33
        width = 0.66 + 0.22 * (1 - abs(yy) / 2.0)
        for i in range(11):
            xx = -width + (2 * width * i / 10)
            pos.append((xx, yy))
    pos = pos[:130] + [(0, 0)]
    return VGroup(*[
        Dot([x + scale * xx, scale * yy, 0], radius=0.025 * scale + 0.008, color=color)
        for xx, yy in pos
    ])


def clock(center=(4.75, -2.15, 0), radius=0.53):
    face = Circle(radius=radius, color=TEXT, stroke_width=3).move_to(center)
    hand = Line(center, np.array(center) + radius * 0.72 * UP, color=TEXT, stroke_width=4)
    return VGroup(face, hand)


def dish_world(question=True):
    dish = Circle(radius=3.18, color=GREY, stroke_width=5,
                  fill_color=GREY, fill_opacity=0.18).move_to([-0.65, -0.28, 0])
    cell = apoptotic_world(with_heads=True).scale(0.84).move_to([-1.20, -0.25, 0])
    clk = clock()
    lab = T("time (schematic)", 28, TEXT).next_to(clk, DOWN, buff=0.14)
    items = [dish, cell, clk, lab]
    if question:
        items.append(T("What happens to the ring?", 38, TEXT, weight=BOLD).move_to([0, 3.25, 0]))
    return VGroup(*items)


def broken_ring(center, radius, color=BLUE, width=8):
    return VGroup(
        Arc(radius=radius, start_angle=0.48, angle=2.44, color=color,
            stroke_width=width).move_arc_center_to(center),
        Arc(radius=radius, start_angle=3.35, angle=2.55, color=color,
            stroke_width=width).move_arc_center_to(center),
    )


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Cell death"
    TITLE = "Sealed or Torn"

    def construct(self):
        xs = (-4.35, 0, 4.35)
        worms = VGroup(*[worm_outline(x, 0.78) for x in xs])
        cells = [worm_cells(x, 0.78) for x in xs]
        all_cells = VGroup(*cells)
        label = T("C. elegans hermaphrodites", 34, TEXT, weight=BOLD).move_to([0, 3.28, 0])
        self.play(Create(worms), FadeIn(all_cells), run_time=1.0)
        self.play(FadeIn(label), worms.animate.shift(UP * 0.04), run_time=0.8)

        self.at("the same")
        blue = VGroup(*[
            Circle(radius=0.055, color=BLUE, stroke_width=2).move_to(d)
            for group in cells for d in group
        ])
        self.play(FadeIn(blue), run_time=0.45)
        count = ValueTracker(0)
        counter = always_redraw(
            lambda: T(f"{int(count.get_value())} of 1,090 cells", 30, TEXT).move_to([5.05, 3.25, 0])
        )
        self.play(FadeOut(label), FadeIn(counter), run_time=0.3)
        gone = [VGroup(cells[0][i], cells[1][i], cells[2][i],
                       blue[i], blue[131 + i], blue[262 + i]) for i in range(131)]
        self.play(AnimationGroup(*[FadeOut(g, scale=0.5) for g in gone], lag_ratio=0.015),
                  count.animate.set_value(131),
                  run_time=2.5)
        new_counter = T("131 of 1,090 cells", 30, TEXT).move_to(counter)
        self.remove(counter)
        self.add(new_counter)
        self.play(worms.animate.shift(DOWN * 0.04), run_time=0.45)

        self.at("without leaving a mess")
        question = T("Die without a mess?", 44, TEXT, weight=BOLD).move_to([0, 3.18, 0])
        self.play(FadeIn(question, shift=DOWN * 0.12), run_time=0.55)
        self.play(worms.animate.shift(UP * 0.05), run_time=1.0, rate_func=there_and_back)

        self.at("rarely see a corpse")
        close = membrane_cell(center=ORIGIN, radius=2.55)
        self.play(FadeOut(VGroup(worms, new_counter, question)), FadeIn(close, scale=0.15), run_time=1.1)
        self.play(close[0].animate.scale(1.025), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        cell = membrane_cell(center=[0, -0.35, 0], radius=2.55)
        title = T("Sealed or Torn", 56, TEXT, font=TITLE_FONT).move_to([0, 2.95, 0])
        self.add(cell)
        self.play(FadeIn(title, shift=DOWN * 0.12), cell[0].animate.scale(1.025),
                  run_time=0.7)
        self.play(cell[0].animate.scale(1 / 1.025), run_time=0.65)
        self.wait(0.65)


class S02Apart(SpokenScene):
    def construct(self):
        big = membrane_cell(center=[-1.15, -0.15, 0], radius=3.05)
        self.play(FadeIn(big, scale=0.7), run_time=0.8)
        self.at("own enzymes")
        shears = VGroup(scissors(1.0).move_to([-2.0, 0.65, 0]),
                        scissors(0.9).move_to([-0.25, -0.45, 0])).set_opacity(0.28)
        rods = VGroup(*[
            RoundedRectangle(width=1.0, height=0.22, corner_radius=0.08,
                             color=GREY, fill_color=GREY, fill_opacity=0.25).move_to(p)
            for p in ([-1.2, 1.15, 0], [-1.75, -0.65, 0], [-0.25, 0.45, 0])
        ])
        self.play(FadeIn(shears), FadeIn(rods), run_time=0.7)
        self.at("switch on")
        self.play(shears.animate.set_opacity(1), run_time=0.45)
        caslab = T("caspases", 32, TEAL, weight=BOLD).move_to([3.55, 1.65, 0])
        self.play(FadeIn(caslab), shears[0].animate.rotate(0.35), run_time=0.55)
        self.at("cut other proteins")
        pieces = VGroup(*[
            RoundedRectangle(width=0.42, height=0.22, corner_radius=0.06,
                             color=GREY, fill_color=GREY, fill_opacity=0.30).move_to(p)
            for p in ([-1.45, 1.15, 0], [-0.92, 1.15, 0], [-1.95, -0.65, 0],
                      [-1.45, -0.65, 0], [-0.48, 0.45, 0], [0.02, 0.45, 0])
        ])
        self.play(ReplacementTransform(rods, pieces), shears.animate.rotate(-0.25), run_time=0.65)

        self.at("cell shrinks")
        final_ring = membrane_cell()[0]
        self.play(ReplacementTransform(big[0], final_ring), FadeOut(pieces),
                  shears.animate.scale(0.72).move_to(CELL_C), run_time=0.85)
        self.at("chromatin packs down")
        packed = VGroup(*[
            Arc(radius=0.46, start_angle=a, angle=0.85, color=GREY, stroke_width=11).move_arc_center_to(CELL_C)
            for a in (0.15, 1.75, 3.35, 4.9)
        ])
        self.play(ReplacementTransform(big[1], packed), run_time=0.65)
        self.at("nucleus breaks into pieces")
        fragments = apoptotic_world()[1]
        self.play(ReplacementTransform(packed, fragments), run_time=0.7)
        self.at("surface bubbles")
        bs = blebs()
        self.play(FadeIn(bs, scale=0.15), run_time=0.75)
        self.play(bs.animate.shift(0.06 * UR), run_time=0.45, rate_func=there_and_back)
        self.at("watch the membrane")
        self.play(Indicate(final_ring, color=BLUE, scale_factor=1.04),
                  *[Indicate(b, color=BLUE, scale_factor=1.06) for b in bs], run_time=0.9)
        self.finish()


class S03Sealed(SpokenScene):
    def construct(self):
        world = apoptotic_world()
        self.add(world)
        check = T("✓", 34, BLUE, weight=BOLD).move_to(CELL_C + CELL_R * RIGHT)
        path = Circle(radius=CELL_R, color=BLUE).move_to(CELL_C)
        self.play(FadeIn(check), MoveAlongPath(check, path),
                  world[2].animate.rotate(0.35), run_time=2.2, rate_func=linear)
        self.at("taking itself apart")
        self.play(world[2].animate.rotate(-0.7), run_time=0.8, rate_func=there_and_back)
        self.at("every piece stays wrapped")
        self.play(MoveAlongPath(check, Circle(radius=0.31).move_to(world[3][0])), run_time=1.0)
        self.play(MoveAlongPath(check, Circle(radius=0.23).move_to(world[3][1])), run_time=0.8)
        self.at("closed membrane")
        self.play(Indicate(VGroup(world[0], world[3]), color=BLUE, scale_factor=1.025), run_time=0.8)
        self.at("called apoptosis")
        lab = T("apoptosis", 42, TEXT, weight=BOLD).move_to([-2.35, 2.82, 0])
        self.play(FadeOut(check), FadeIn(lab, shift=DOWN * 0.12), run_time=0.65)
        self.play(world[2].animate.rotate(0.35), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S04Findme(SpokenScene):
    def construct(self):
        world = apoptotic_world()
        apop = T("apoptosis", 42, TEXT, weight=BOLD).move_to([-2.35, 2.82, 0])
        self.add(world, apop)
        self.at("send two signals")
        badge = T("1", 30, TEXT, weight=BOLD)
        badge.add_background_rectangle(color=BLUE, opacity=0.8, buff=0.15)
        badge.move_to([-0.40, 1.45, 0])
        self.play(FadeIn(badge), run_time=0.45)
        self.at("channel in its membrane opens")
        channel = VGroup(
            Line([-0.52, -0.05, 0], [-0.16, -0.05, 0], color=BLUE, stroke_width=8),
            Line([-0.52, 0.27, 0], [-0.16, 0.27, 0], color=BLUE, stroke_width=8),
        )
        self.play(Create(channel), run_time=0.65)
        self.at("small molecules puff out")
        cloud = find_cloud()
        self.play(AnimationGroup(*[FadeIn(d, shift=0.35 * RIGHT) for d in cloud], lag_ratio=0.13),
                  run_time=1.25)
        self.at("find me signal")
        find = T("find-me", 32, TEXT, weight=BOLD).move_to([1.20, 1.12, 0])
        self.play(FadeIn(find), cloud.animate.shift(0.10 * RIGHT), run_time=0.55)
        self.at("call a phagocyte")
        eater = phagocyte(center=[7.0, -0.15, 0])
        plab = T("phagocyte", 32, GREEN, weight=BOLD).move_to([4.45, -2.35, 0])
        self.play(FadeOut(badge), eater.animate.move_to([4.45, -0.15, 0]), FadeIn(plab),
                  cloud.animate.shift(0.18 * RIGHT), run_time=1.45)
        self.play(eater.animate.shift(0.18 * LEFT), run_time=0.6)
        self.finish()


class S05Eatme(SpokenScene):
    def construct(self):
        outer = Line([-5.4, 0.48, 0], [3.0, 0.48, 0], color=BLUE, stroke_width=6)
        inner = Line([-5.4, -0.48, 0], [3.0, -0.48, 0], color=BLUE, stroke_width=6)
        faces = VGroup(T("outside", 30, TEXT).move_to([-4.55, 1.40, 0]),
                       T("inside", 30, TEXT).move_to([-4.70, -1.40, 0]))
        proteins = VGroup(*[
            RoundedRectangle(width=0.62, height=1.28, corner_radius=0.10,
                             color=GREY, fill_color=GREY, fill_opacity=0.32).move_to([x, 0, 0])
            for x in (0.10, 1.45)
        ])
        heads = VGroup(*[
            Dot([x, y, 0], radius=0.12, color=YELLOW)
            for x, y in zip(np.linspace(-4.6, 2.5, 11), [-0.78] * 9 + [0.80, 0.80])
        ])
        self.play(Create(VGroup(outer, inner)), FadeIn(faces), run_time=0.8)
        self.at("lipid called phosphatidylserine")
        self.play(AnimationGroup(*[FadeIn(h, scale=0.4) for h in heads], lag_ratio=0.08), run_time=1.0)
        ps = T("phosphatidylserine", 34, YELLOW, weight=BOLD).move_to([-0.9, 2.75, 0])
        self.play(FadeIn(ps), run_time=0.5)
        self.at("mostly on the membrane's inner face")
        self.play(Indicate(VGroup(*heads[:9]), color=YELLOW), run_time=0.65)
        self.at("cut the membrane proteins")
        self.play(FadeIn(proteins), run_time=0.35)
        shears = VGroup(scissors(0.8).move_to(proteins[0]), scissors(0.8).move_to(proteins[1]))
        self.play(FadeIn(shears), proteins.animate.set_opacity(0.35), run_time=0.65)
        cuts = VGroup(*[
            VGroup(Line([-0.32, 0, 0], [-0.05, 0, 0], color=GREY, stroke_width=8),
                   Line([0.05, 0, 0], [0.32, 0, 0], color=GREY, stroke_width=8)).move_to(p)
            for p in proteins
        ])
        self.play(ReplacementTransform(proteins, cuts), shears.animate.rotate(0.45), run_time=0.7)
        # The lipids continue to shimmer while the cut proteins change state.
        self.play(heads.animate.shift(0.09 * UP), shears.animate.rotate(-0.28),
                  run_time=1.05, rate_func=there_and_back)
        self.at("appears on the outer face")
        self.play(*[heads[i].animate.move_to([heads[i].get_x(), 0.80, 0]) for i in range(9)],
                  run_time=1.25)
        self.play(Indicate(heads, color=YELLOW), run_time=0.55)
        self.at("eat me flag")
        full = apoptotic_world(with_heads=True)
        eater = phagocyte(center=[4.45, -0.15, 0])
        # Keep the label above the cell: at the old right-edge position it sat behind a bleb
        # and the membrane crossed the text during its fade-in.
        eat = T("eat-me", 34, YELLOW, weight=BOLD).move_to([-2.35, 2.82, 0])
        self.play(FadeOut(VGroup(outer, inner, faces, ps, cuts, shears, heads)),
                  FadeIn(full, scale=1.3), FadeIn(eater), run_time=0.85)
        self.play(FadeIn(eat), eater.animate.shift(0.22 * LEFT), run_time=0.65)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        world = apoptotic_world(with_heads=True)
        cloud = find_cloud()
        eater = phagocyte(center=[4.05, -0.15, 0])
        self.add(world, cloud, eater)
        idea = T("Holds while taken apart", 42, TEXT, weight=BOLD).move_to([0, 3.18, 0])
        self.play(Write(idea), eater.animate.shift(0.10 * LEFT), run_time=1.0)
        self.at("membrane holds")
        self.play(Indicate(world[0], color=BLUE, scale_factor=1.035), run_time=0.8)
        self.at("takes itself apart")
        self.play(world[2].animate.rotate(0.55), run_time=0.75, rate_func=there_and_back)
        self.at("buys time")
        timer = Arc(radius=1.78, start_angle=PI / 2, angle=0.01, color=TEXT,
                    stroke_width=5).move_arc_center_to(CELL_C)
        full_timer = Arc(radius=1.78, start_angle=PI / 2, angle=-TAU + 0.08,
                         color=TEXT, stroke_width=5).move_arc_center_to(CELL_C)
        self.play(Transform(timer, full_timer), eater.animate.shift(0.20 * LEFT), run_time=1.15)
        self.at("before anything leaks")
        self.play(FadeOut(timer), eater.animate.shift(0.26 * LEFT), run_time=0.8)
        self.play(world[2].animate.rotate(-0.4), run_time=0.6, rate_func=there_and_back)
        self.finish()


class S07Eaten(SpokenScene):
    def construct(self):
        world = apoptotic_world(with_heads=True)
        eater = phagocyte(center=[3.65, -0.15, 0])
        self.add(world, eater)
        self.at("recognizes the flag")
        self.play(eater.animate.shift(2.30 * LEFT), Indicate(world[-1], color=YELLOW), run_time=1.0)
        self.at("wraps around the whole cell")
        wrap = Circle(radius=2.58, color=GREEN, stroke_width=11,
                      fill_color=GREEN, fill_opacity=0.19).move_to(CELL_C)
        breathe(wrap, GREEN, 0.19, 0.025)
        self.play(ReplacementTransform(eater[0], wrap), FadeOut(eater[1]), run_time=1.15)
        self.at("swallows it")
        swallowed = VGroup(world, wrap)
        self.play(swallowed.animate.scale(0.76), run_time=0.8)
        self.at("lysosome digests it")
        lyso_sphere = Circle(radius=0.43, color=GREY, fill_color=GREY, fill_opacity=0.25).move_to([2.35, 1.42, 0])
        lyso_label = T("lysosome", 28, TEXT).next_to(lyso_sphere, DOWN, buff=0.16)
        self.play(FadeIn(lyso_sphere), FadeIn(lyso_label), run_time=0.55)
        # The name has finished its job before the organelle merges; do not leave faint text
        # trapped under the shrinking cell.
        self.play(lyso_sphere.animate.move_to(swallowed), FadeOut(lyso_label),
                  swallowed.animate.scale(0.35).set_opacity(0.12), run_time=1.0)
        self.at("Nothing spills")
        clean_cell = VGroup(
            Circle(radius=1.95, color=GREEN, stroke_width=9,
                   fill_color=GREEN, fill_opacity=0.18),
            Circle(radius=0.46, color=BLUE, stroke_width=5,
                   fill_color=BLUE, fill_opacity=0.12),
        ).move_to([0, 0.42, 0])
        clean = T("nothing spills", 36, TEXT, weight=BOLD).move_to([0, -2.35, 0])
        self.play(FadeOut(VGroup(lyso_sphere, swallowed)), FadeIn(clean_cell), FadeIn(clean), run_time=0.65)
        self.at("rarely see a corpse")
        worm = worm_outline(0, 1.35)
        dots = worm_cells(0, 1.35)
        marked = Circle(radius=0.14, color=BLUE, stroke_width=4).move_to(dots[-1])
        self.play(FadeOut(VGroup(clean_cell, clean)), Create(worm), FadeIn(dots), FadeIn(marked), run_time=0.9)
        self.play(FadeOut(VGroup(dots[-1], marked), scale=0.2), worm.animate.shift(0.05 * UP),
                  run_time=0.75, rate_func=smooth)
        self.finish()


class S08Ask(SpokenScene):
    def construct(self):
        world = dish_world(question=False)
        self.play(Create(world[0]), FadeIn(world[1]), run_time=0.9)
        self.at("no phagocyte will come")
        self.play(FadeIn(world[2]), FadeIn(world[3]), run_time=0.55)
        self.at("Time passes")
        self.play(Rotate(world[2][1], angle=-1.7, about_point=world[2][0].get_center()),
                  world[1][2].animate.rotate(0.45), run_time=1.2, rate_func=linear)
        self.at("What happens to its membrane")
        q = T("What happens to the ring?", 38, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), Indicate(world[1][0], color=BLUE), run_time=0.8)
        self.play(world[1][0].animate.scale(1.025), run_time=0.55, rate_func=there_and_back)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        world = dish_world(question=True)
        self.add(world)
        self.play(Rotate(world[2][1], angle=-TAU * 0.65, about_point=world[2][0].get_center()),
                  world[1][0].animate.scale(1.025), world[1][-1].animate.set_opacity(0.72),
                  run_time=2.25, rate_func=linear)
        self.play(Rotate(world[2][1], angle=-TAU * 0.65, about_point=world[2][0].get_center()),
                  world[1][0].animate.scale(1 / 1.025), world[1][-1].animate.set_opacity(1),
                  run_time=2.25, rate_func=linear)


class S10Leak(SpokenScene):
    def construct(self):
        world = dish_world(question=True)
        self.add(world)
        self.play(FadeOut(world[-1]), run_time=0.35)
        self.at("Often it fails")
        c = world[1][0].get_center()
        r = 0.84 * CELL_R
        broken = broken_ring(c, r, width=7)
        self.play(ReplacementTransform(world[1][0], broken), run_time=0.75)
        # Once failed, the two membrane edges keep opening and relaxing slightly.
        breathe(broken, BLUE, 0.0, 0.0)
        breathe(world[0], GREY, 0.18, 0.025)
        self.at("now leaks")
        seep = VGroup(*[
            Dot(c + d, radius=rr, color=RED).set_opacity(op)
            for d, rr, op in [([1.05, 0.42, 0], .11, .9), ([1.42, .58, 0], .13, .8),
                              ([1.78, .35, 0], .15, .7), ([-1.08, -.48, 0], .10, .9),
                              ([-1.48, -.72, 0], .14, .7), ([-1.88, -.92, 0], .18, .55)]
        ])
        self.play(AnimationGroup(*[FadeIn(d, shift=0.25 * RIGHT) for d in seep], lag_ratio=0.15),
                  run_time=1.2)
        self.at("contents spill")
        self.play(seep.animate.scale(1.18), Rotate(world[2][1], angle=-1.3,
                  about_point=world[2][0].get_center()), run_time=0.75)
        self.at("secondary necrosis")
        # Keep the label inside the dish with clear air above its lower boundary.
        lab = T("secondary necrosis", 34, RED, weight=BOLD).move_to([-0.65, -2.65, 0])
        self.play(FadeIn(lab), run_time=0.6)
        self.at("In a tissue")
        inset = RoundedRectangle(width=3.15, height=2.20, corner_radius=0.15,
                                 color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.92).move_to([4.75, 1.75, 0])
        mini_blue = Circle(radius=0.45, color=BLUE, stroke_width=5).move_to([4.48, 1.78, 0])
        mini_green = Circle(radius=0.78, color=GREEN, stroke_width=6,
                            fill_color=GREEN, fill_opacity=0.12).move_to([5.12, 1.78, 0])
        tissue = T("tissue", 28, TEXT).next_to(inset, DOWN, buff=0.10)
        dish = T("dish", 28, TEXT).move_to([-1.1, 2.45, 0])
        self.play(FadeIn(inset), FadeIn(mini_blue), FadeIn(mini_green), FadeIn(tissue), FadeIn(dish), run_time=0.8)
        self.play(mini_green.animate.move_to(mini_blue).scale(1.05), mini_blue.animate.scale(0.65), run_time=0.9)
        self.finish()


class S11Torn(SpokenScene):
    def construct(self):
        center = np.array([1.25, -0.15, 0])
        cell = membrane_cell(center=center, radius=1.48)
        organelles = VGroup(*[
            Circle(radius=0.16, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to(center + d)
            for d in ([-0.65, 0.55, 0], [0.62, 0.48, 0], [-0.55, -0.57, 0], [0.62, -0.55, 0])
        ])
        self.play(FadeIn(cell), FadeIn(organelles), run_time=0.8)
        self.at("This one swells")
        self.play(VGroup(cell, organelles).animate.scale(1.38), run_time=1.05)
        self.at("membrane tears early")
        r = 1.48 * 1.38
        broken = broken_ring(center, r, width=9)
        self.play(ReplacementTransform(cell[0], broken), run_time=0.75)
        self.at("contents spill at once")
        spill = VGroup(*[
            Dot(center + d, radius=rr, color=RED)
            for d, rr in [([2.0, .75, 0], .13), ([2.5, .4, 0], .18), ([2.75, -.2, 0], .14),
                          ([-2.0, -.7, 0], .15), ([-2.55, -1.0, 0], .18), ([2.25, -1.1, 0], .12)]
        ])
        self.play(AnimationGroup(*[FadeIn(d, shift=0.5 * normalize(d.get_center() - center)) for d in spill],
                                 lag_ratio=0.12), run_time=1.0)
        self.at("alarm signals")
        alarms = VGroup(*[Dot(center + d, radius=0.23, color=RED) for d in ([2.7, 1.25, 0], [3.1, .75, 0])])
        al = T("alarm signals", 30, RED, weight=BOLD).move_to([4.35, 2.55, 0])
        self.play(FadeIn(alarms), FadeIn(al), run_time=0.65)
        self.at("immune system")
        immune = VGroup(*[
            Circle(radius=0.48, color=GREY, stroke_width=5,
                   fill_color=GREY, fill_opacity=0.10).move_to(p)
            for p in ([-6.6, 1.95, 0], [-6.5, -2.05, 0])
        ])
        self.play(immune[0].animate.move_to([-3.5, 1.45, 0]),
                  immune[1].animate.move_to([-3.4, -1.45, 0]), run_time=1.2)
        self.at("cause inflammation")
        glow = Circle(radius=2.75, color=RED, stroke_width=5,
                      fill_color=RED, fill_opacity=0.18).move_to(center)
        infl = T("inflammation", 30, RED, weight=BOLD).move_to([-3.55, 0, 0])
        self.play(FadeIn(glow), FadeIn(infl), run_time=0.65)
        self.at("called necrosis")
        label = T("necrosis", 42, TEXT, weight=BOLD).move_to([1.25, 3.10, 0])
        self.play(FadeIn(label), glow.animate.scale(1.05), run_time=0.7)
        self.finish()


class S12Programs(SpokenScene):
    def construct(self):
        left_c = np.array([-3.35, 0.50, 0])
        right_c = np.array([3.35, 0.50, 0])
        intact = membrane_cell(left_c, 1.45)
        heads = surface_heads(left_c, 1.45, 8)
        eater = phagocyte(center=[-5.5, 0.5, 0], radius=0.85)
        torn_body = Circle(radius=1.75, stroke_opacity=0, fill_color=GREY,
                           fill_opacity=0.17).move_to(right_c)
        torn = broken_ring(right_c, 1.75, width=8)
        spill = VGroup(*[Dot(right_c + d, radius=.12, color=RED) for d in ([1.6,.4,0],[1.9,0,0],[1.5,-.65,0])])
        labs = VGroup(T("apoptosis", 34, TEXT, weight=BOLD).move_to([-3.35, 2.70, 0]),
                      T("necrosis", 34, TEXT, weight=BOLD).move_to([3.35, 2.70, 0]))
        self.play(FadeIn(VGroup(intact, heads, eater, torn_body, torn, spill, labs)), run_time=0.85)
        self.at("genetic programs too")
        genes = VGroup(*[chip("gene", TEXT, 28).move_to([2.05 + i * 1.30, -1.18, 0]) for i in range(3)])
        self.play(AnimationGroup(*[FadeIn(g, shift=UP * 0.15) for g in genes], lag_ratio=0.2), run_time=0.75)
        self.play(FadeOut(genes), spill.animate.shift(0.08 * RIGHT), run_time=0.55)
        self.at("difference is timing")
        line = Arrow([-5.5, -2.35, 0], [5.5, -2.35, 0], buff=0, color=TEXT,
                     stroke_width=4, tip_length=0.22)
        early = T("early", 30, TEXT).next_to(line.get_start(), UP, buff=0.15)
        schematic = T("time (schematic)", 28, TEXT).next_to(line, DOWN, buff=0.15)
        self.play(GrowArrow(line), FadeIn(early), FadeIn(schematic), run_time=0.85)
        self.at("membrane intact early")
        blue_tick = VGroup(Circle(radius=.24, color=BLUE, stroke_width=5), T("✓", 28, BLUE)).move_to([-3.35, -2.35, 0])
        self.play(FadeIn(blue_tick), Indicate(intact[0], color=BLUE), run_time=0.7)
        self.at("open it early")
        red_tick = VGroup(VGroup(Line(.22 * UL, .22 * DR, color=RED, stroke_width=5),
                                 Line(.22 * UR, .22 * DL, color=RED, stroke_width=5))).move_to([3.35, -2.35, 0])
        self.play(FadeIn(red_tick), Indicate(torn, color=RED), run_time=0.75)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        # Start on the same comparison, then pull back into the hook's three-worm world.
        left = membrane_cell([-3.35, 0.4, 0], 1.2)
        right_body = Circle(radius=1.5, stroke_opacity=0, fill_color=GREY,
                            fill_opacity=0.17).move_to([3.35, 0.4, 0])
        right = broken_ring([3.35, 0.4, 0], 1.5, width=8)
        spill = VGroup(*[Dot(np.array([3.35, .4, 0]) + d, radius=.12, color=RED)
                         for d in ([1.6,.5,0],[1.9,0,0],[1.5,-.6,0])])
        self.add(left, right_body, right, spill)
        self.at("back to the worm")
        xs = (-4.35, 0, 4.35)
        worms = VGroup(*[worm_outline(x, 0.78) for x in xs])
        dots = VGroup(*[worm_cells(x, 0.78) for x in xs])
        counter = T("131 of 1,090 cells", 30, TEXT).move_to([4.95, 3.25, 0])
        self.play(FadeOut(VGroup(left, right_body, right, spill)), FadeIn(worms, scale=1.2), FadeIn(dots),
                  FadeIn(counter), run_time=1.0)
        self.at("usually eaten by neighboring cells")
        doomed = Circle(radius=.16, color=BLUE, stroke_width=4).move_to([0, 0, 0])
        neighbor = Circle(radius=.34, color=GREY, stroke_width=5,
                          fill_color=GREEN, fill_opacity=.12).move_to([0.55, 0.05, 0])
        self.play(FadeIn(doomed), FadeIn(neighbor), run_time=0.45)
        self.play(neighbor.animate.move_to(doomed).scale(1.35), doomed.animate.scale(.5), run_time=0.85)
        self.at("before they spill")
        self.play(FadeOut(doomed), neighbor.animate.set_stroke(GREEN), worms.animate.shift(0.04 * UP),
                  run_time=0.65)
        self.at("membrane that holds")
        self.play(Indicate(neighbor, color=BLUE), run_time=0.65)
        self.at("quieter death")
        sealed = VGroup(Circle(radius=.42, color=BLUE, stroke_width=5),
                        Circle(radius=.62, color=GREEN, stroke_width=5)).move_to([-2.5, -2.75, 0])
        torn = broken_ring([2.35, -2.75, 0], .48, width=5)
        red = VGroup(*[Dot([2.95 + .25*i, -2.75 + .12*(-1)**i, 0], radius=.07, color=RED) for i in range(3)])
        labels = VGroup(T("sealed and eaten", 28, TEXT).move_to([-2.5, -3.45, 0]),
                        T("torn and spilled", 28, TEXT).move_to([2.55, -3.45, 0]))
        self.play(FadeIn(VGroup(sealed, torn, red, labels)), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "Apoptosis keeps the membrane intact early, often until the cell is eaten."

    def construct(self):
        line = VGroup(
            T("Apoptosis keeps the membrane intact early,", 40, TEXT, font=TITLE_FONT),
            T("often until the cell is eaten.", 40, TEXT, font=TITLE_FONT),
        ).arrange(DOWN, buff=0.24).move_to([0, 0.35, 0])
        # A wider ellipse leaves visible clearance around both ends of the sentence.
        ring = Circle(radius=2.30, color=BLUE, stroke_width=7).stretch(2.60, 0).move_to([0, 0.35, 0])
        site = T("biochemistrypedia.com", 28, GREY).move_to([0, -2.75, 0])
        self.play(FadeIn(line, shift=UP * 0.12), run_time=0.65)
        self.play(Create(ring), run_time=1.55)
        self.play(FadeIn(site), run_time=0.4)
        self.finish()
