"""Before the Phage Arrives — Mutation: Where Variation Comes From.

COLOUR MAP (one colour per concept across the whole film):
  BLUE   (#58C4DD) : unchanged DNA and susceptible bacterial cells
  YELLOW (#F5D547) : changed DNA (heritable variant), resistant cells, colonies, growth-model scatter
  RED    (#FC6255) : phage (bacterial virus), the gate, and contact-induced model scatter
  GREEN  (#83C167) : accurate repair (reserved in two-film palette; not drawn here)
  TEXT   (#E8EAF0) : neutral labels, counts, brackets, axes, schematic/illustrative tags
  GREY   (#8B93A1) : glass tube outlines, plate rims, and axis lines only (never for text)

CARRIED WORLD:
  10 glass culture tubes at TUBE_XS (x = -5.65 .. +3.53, y = -0.45 .. +2.65),
  a closed/open RED gate at x = 4.25, and RED phage icons on the far right (x = 4.9 .. 6.1).
  Illustrative counts from the lesson: [0, 0, 1, 0, 3, 0, 0, 52, 2, 2] (mean 6, sample variance ~262),
  compared with bulk samples [4, 8, 6, 3, 9, 5, 7, 6, 8, 4] (mean 6, sample variance 4).

WHAT CHANGES IN EACH SPOKEN SCENE (computed from lesson parameters / fixed rng seed 7):
  s00_hook            : 10 BLUE family trees grow upward inside tubes; RED phages move to closed gate; 3 yellow outcome bars rise over blank plates.
  s02_same_start      : 10 identical food pills drop into tubes; 10 BLUE trees branch together at steady rhythm; lineage trace climbs one tree.
  s03_sequence_change : 6-base BLUE DNA strip replicates into two strips; one block mutates to YELLOW; zoom pulls back to a growing YELLOW subtree among BLUE branches.
  s04_timing          : Shared time sweep drives 10 trees from 0 to 1; early node (tube 7) builds large YELLOW branch, late tips (tubes 2,4,8,9) build few tips, 5 stay BLUE.
  s05_two_models      : Left overlay preserves YELLOW growth branches (tubes 0..4); right overlay rewinds tubes 5..9 to BLUE, opens gate, and phages touch isolated tips YELLOW.
  s06_predict         : Pre-exposure trees complete growth; question card and two neutral choice cards ("similar counts", "jackpots + empty plates") appear; trees highlight.
  s08_exposure        : Gate opens; RED phages sweep left across all 10 tubes, fading BLUE branches while YELLOW cells drop to plates and expand into colonies.
  s09_pattern         : 10 plates slide onto shared count axis (0..55); schematic RED contact band and YELLOW growth band expand around mean = 6.
  s10_evidence        : Independent tubes (top) vs 1 bulk flask pouring 10 equal drops (bottom); dots fly onto shared 0..55 axis as computed variances tick to 262 vs 4.
  s11_scope           : Framed phage-resistance tubes filter through RED phage wave; mutation-rate gauge needle shifts modestly across neutral condition cards A, B, C.
  s12_rule            : Large family tree grows, YELLOW sequence-change node triggers "origin" branch growth, then RED phage wave performs "sorting" removing BLUE branches.
"""
from bp_parts import *

# ------------------------------------------------------------------ shared geometry & lesson data
TUBE_XS = [-5.65 + i * 1.02 for i in range(10)]
TUBE_W = 0.86
TUBE_Y0 = -0.45
TUBE_Y1 = 2.65
TUBE_YC = (TUBE_Y0 + TUBE_Y1) / 2
TUBE_H = TUBE_Y1 - TUBE_Y0
GATE_X = 4.25

IND_COUNTS = [0, 0, 1, 0, 3, 0, 0, 52, 2, 2]
BULK_COUNTS = [4, 8, 6, 3, 9, 5, 7, 6, 8, 4]

# Mutation schedule per tube (generation level 1..4, branch index within level, normalized time)
# Matches IND_COUNTS: 0, 0, 1, 0, 3, 0, 0, 52(early), 2, 2
TUBE_MUTATIONS = {
    2: (4, 10, 0.84),   # 1 late tip
    4: (3, 5, 0.64),    # 3-tip small late cluster
    7: (1, 1, 0.24),    # early event -> half tree yellow (jackpot = 52)
    8: (3, 2, 0.72),    # 2 late tips
    9: (3, 6, 0.74),    # 2 late tips
}


def make_phage(scale=1.0, color=RED):
    """Schematic virus icon (geometric polygon head + tail + two legs, never a molecular structure)."""
    head = RegularPolygon(6, radius=0.13 * scale, color=color, stroke_width=2.6, fill_color=color, fill_opacity=0.28)
    head.rotate(PI / 6)
    tail = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.14 * scale, color=color, stroke_width=2.6)
    tip = tail.get_end()
    leg_l = Line(tip, tip + np.array([-0.10, -0.09, 0.0]) * scale, color=color, stroke_width=2.4)
    leg_r = Line(tip, tip + np.array([0.10, -0.09, 0.0]) * scale, color=color, stroke_width=2.4)
    return VGroup(head, tail, leg_l, leg_r)


def make_gate(y0=TUBE_Y0, y1=TUBE_Y1, x=GATE_X):
    """Closed red gate barrier."""
    post = Line([x, y0, 0], [x, y1, 0], color=RED, stroke_width=6)
    bars = VGroup(*[
        Line([x - 0.14, y, 0], [x + 0.14, y, 0], color=RED, stroke_width=3.5)
        for y in np.linspace(y0 + 0.25, y1 - 0.25, 6)
    ])
    return VGroup(post, bars)


def make_phage_swarm(xs=(4.95, 5.55, 6.05, 5.15, 5.75, 6.20), ys=(2.2, 1.75, 1.25, 0.75, 0.25, 2.35), scale=0.95):
    """Phage icons waiting behind the gate on the right."""
    return VGroup(*[make_phage(scale=scale).move_to([x, y, 0]) for x, y in zip(xs, ys)])


def make_tube_glass(cx, y0=TUBE_Y0, y1=TUBE_Y1, w=TUBE_W):
    """Glass culture tube outline inside safe bounds."""
    h = y1 - y0
    glass = RoundedRectangle(
        corner_radius=0.18, width=w, height=h,
        stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.45
    ).move_to([cx, (y0 + y1) / 2, 0])
    rim = Line([cx - w * 0.42, y1, 0], [cx + w * 0.42, y1, 0], color=TEXT, stroke_width=2.4).set_opacity(0.45)
    return VGroup(glass, rim)


def _tree_segments(cx, y0, y1, width, tube_idx, mut_info=None, depth=4):
    """Build deterministic binary tree segments [(p0, p1, gen, is_yellow), ...] strictly inside tube."""
    rng = np.random.default_rng(7 + tube_idx * 13)
    pad_y0 = y0 + 0.22
    pad_y1 = y1 - 0.20
    ys = np.linspace(pad_y0, pad_y1, depth + 1)
    segs = []
    stem_top = pad_y0 + (ys[1] - pad_y0) * 0.55
    segs.append((np.array([cx, pad_y0, 0.0]), np.array([cx, stem_top, 0.0]), 0, False))

    mut_gen, mut_idx = (mut_info[0], mut_info[1]) if mut_info else (None, None)
    nodes = [(cx, stem_top, False)]
    for g in range(1, depth + 1):
        n_branches = 2 ** g
        half_span = width * 0.35
        xs_g = np.linspace(cx - half_span, cx + half_span, n_branches)
        next_nodes = []
        for idx, (px, py, par_y) in enumerate(nodes):
            for child_side in (0, 1):
                c_idx = idx * 2 + child_side
                jx = float(rng.uniform(-0.012, 0.012))
                tx = float(np.clip(xs_g[c_idx] + jx, cx - half_span, cx + half_span))
                ty = float(ys[g])
                is_y = par_y or (mut_gen == g and c_idx == mut_idx)
                segs.append((np.array([px, py, 0.0]), np.array([tx, ty, 0.0]), g, is_y))
                next_nodes.append((tx, ty, is_y))
        nodes = next_nodes
    # Extra third tip inside tube 4 at the exact same canopy height pad_y1
    if tube_idx == 4 and mut_info:
        for p0, p1, g, iy in segs:
            if g == depth and iy:
                segs.append((p0, np.array([min(cx + width * 0.35, p1[0] + 0.042), pad_y1, 0.0]), depth, True))
                break
    return segs


def draw_tree_at(cx, y0, y1, width, tube_idx, progress, mut_info=None, blue_opacity=1.0, yellow_opacity=1.0,
                 stroke_w=4.2, tip_r=0.052, depth=4, force_all_blue=False):
    """Render a deterministic growing family tree at normalized progress in [0, 1]."""
    segs = _tree_segments(cx, y0, y1, width, tube_idx, mut_info=mut_info, depth=depth)
    g = VGroup()
    p = float(np.clip(progress, 0.0, 1.0))
    span = depth + 1
    g.add(Dot([cx, y0 + 0.22, 0], radius=tip_r * 1.45, color=BLUE).set_opacity(max(blue_opacity, 0.15)))
    for p0, p1, gen, is_y in segs:
        t0 = gen / span
        t1 = (gen + 1) / span
        if p <= t0:
            continue
        frac = min(1.0, (p - t0) / (t1 - t0))
        end = p0 + frac * (p1 - p0)
        use_yellow = is_y and not force_all_blue
        col = YELLOW if use_yellow else BLUE
        op = yellow_opacity if use_yellow else blue_opacity
        g.add(Line(p0, end, color=col, stroke_width=stroke_w).set_opacity(op))
        if frac >= 0.99 and gen == depth:
            g.add(Dot(end, radius=tip_r, color=col).set_opacity(op))
    return g


def build_world(progress=1.0, include_mutations=True, blue_opacity=1.0, yellow_opacity=1.0, gate_open=False):
    """Build the carried 10-tube world at identical coordinates across scenes."""
    tubes = VGroup(*[make_tube_glass(cx) for cx in TUBE_XS])
    trees = VGroup(*[
        draw_tree_at(
            cx, TUBE_Y0, TUBE_Y1, TUBE_W, i, progress,
            mut_info=TUBE_MUTATIONS.get(i) if include_mutations else None,
            blue_opacity=blue_opacity, yellow_opacity=yellow_opacity
        )
        for i, cx in enumerate(TUBE_XS)
    ])
    gate = make_gate()
    if gate_open:
        gate.shift(UP * 1.5 + RIGHT * 0.25).rotate(0.45)
    phages = make_phage_swarm()
    return tubes, trees, gate, phages


def make_plate_colonies(cx, cy, count, radius=0.40, seed=7):
    """Petri plate circle + deterministic yellow colony dots matching `count`."""
    rim = Circle(radius=radius, color=GREY, stroke_width=3.0, fill_color=BG, fill_opacity=0.85).move_to([cx, cy, 0])
    rng = np.random.default_rng(seed + count * 31)
    dots = VGroup()
    n_draw = count if count <= 10 else 28
    dot_r = 0.045 if count <= 10 else 0.030
    for _ in range(n_draw):
        ang = rng.uniform(0, TAU)
        rr = (radius - 0.09) * np.sqrt(rng.uniform(0, 1))
        dots.add(Dot([cx + rr * np.cos(ang), cy + rr * np.sin(ang), 0], radius=dot_r, color=YELLOW))
    return VGroup(rim, dots)


# ------------------------------------------------------------------ Scene 0: Hook
class S00Hook(SpokenScene):
    def construct(self):
        tubes = VGroup(*[make_tube_glass(cx) for cx in TUBE_XS])
        growth = ValueTracker(0.05)
        trees = always_redraw(lambda: VGroup(*[
            draw_tree_at(cx, TUBE_Y0, TUBE_Y1, TUBE_W, i, growth.get_value(), mut_info=None)
            for i, cx in enumerate(TUBE_XS)
        ]))
        gate = make_gate()
        phages = make_phage_swarm(xs=(5.65, 6.15, 6.45, 5.85, 6.25, 6.50))
        tag = scope_tag("schematic", color=TEXT)

        self.play(FadeIn(tubes), FadeIn(tag), run_time=0.5)
        self.add(trees)
        rt1 = max(0.5, self.t_of("then meet") - 0.2 - self.elapsed())
        self.play(growth.animate.set_value(0.82), run_time=rt1, rate_func=linear)

        self.at("then meet")
        self.play(FadeIn(gate), FadeIn(phages), run_time=0.7)
        rt2 = max(0.5, self.t_of("Why do some") - 0.25 - self.elapsed())
        self.play(
            phages.animate.shift(LEFT * 0.55),
            growth.animate.set_value(1.0),
            run_time=rt2,
            rate_func=linear
        )

        self.at("Why do some")
        plate_xs = [-3.6, -0.7, 2.2]
        plate_y = -2.65
        plates = VGroup(*[
            Circle(radius=0.45, color=GREY, stroke_width=2.6, fill_color=BG, fill_opacity=0.8).move_to([px, plate_y, 0])
            for px in plate_xs
        ])
        bar_targets = [0.02, 0.35, 1.35]
        bar_trackers = [ValueTracker(0.01) for _ in range(3)]
        bars = always_redraw(lambda: VGroup(*[
            Rectangle(
                width=0.52,
                height=max(0.03, bt.get_value()),
                color=YELLOW if bt.get_value() > 0.04 else GREY,
                stroke_width=2.4,
                fill_color=YELLOW if bt.get_value() > 0.04 else GREY,
                fill_opacity=0.78 if bt.get_value() > 0.04 else 0.35
            ).move_to([px, plate_y + 0.56 + max(0.03, bt.get_value()) / 2, 0])
            for px, bt in zip(plate_xs, bar_trackers)
        ]))
        self.play(FadeIn(plates), run_time=0.5)
        self.add(bars)
        rt3 = max(0.5, self.t_of("Each tube began") - 0.25 - self.elapsed())
        self.play(*[bt.animate.set_value(tgt) for bt, tgt in zip(bar_trackers, bar_targets)], run_time=rt3)

        self.at("Each tube began")
        start_rings = VGroup(*[
            Circle(radius=0.14, color=BLUE, stroke_width=3).move_to([cx, TUBE_Y0 + 0.22, 0])
            for cx in TUBE_XS
        ])
        rt4 = max(0.4, self.t_of("every plate receives") - 0.25 - self.elapsed())
        self.play(Create(start_rings), run_time=rt4)

        self.at("every plate receives")
        plate_phages = VGroup(*[
            make_phage(scale=0.85).move_to([GATE_X + 0.65, plate_y + 0.15, 0])
            for _ in plate_xs
        ])
        self.play(
            *[p.animate.move_to([px + 0.72, plate_y, 0]) for p, px in zip(plate_phages, plate_xs)],
            FadeOut(start_rings),
            run_time=1.8
        )
        self.finish()


# ------------------------------------------------------------------ Scene 1: Title Card
class S01Title(TitleCard):
    LESSON = "Mutation: Where Variation Comes From"
    TITLE = "Before the Phage Arrives"


# ------------------------------------------------------------------ Scene 2: Same Start
class S02SameStart(SpokenScene):
    def construct(self):
        tubes = VGroup(*[make_tube_glass(cx) for cx in TUBE_XS])
        gate = make_gate()
        phages = make_phage_swarm()
        tag = scope_tag("schematic", color=TEXT)
        growth = ValueTracker(0.0)
        trees = always_redraw(lambda: VGroup(*[
            draw_tree_at(cx, TUBE_Y0, TUBE_Y1, TUBE_W, i, growth.get_value(), mut_info=None)
            for i, cx in enumerate(TUBE_XS)
        ]))

        self.add(tubes, trees, gate, phages, tag)
        starters = VGroup(*[Dot([cx, TUBE_Y0 + 0.22, 0], radius=0.09, color=BLUE) for cx in TUBE_XS])
        self.add(starters)
        start_line = Line([TUBE_XS[0] - 0.35, TUBE_Y0 - 0.32, 0], [TUBE_XS[-1] + 0.35, TUBE_Y0 - 0.32, 0],
                          color=TEXT, stroke_width=2.5)
        start_ticks = VGroup(
            Line([TUBE_XS[0] - 0.35, TUBE_Y0 - 0.20, 0], [TUBE_XS[0] - 0.35, TUBE_Y0 - 0.32, 0], color=TEXT, stroke_width=2.5),
            Line([TUBE_XS[-1] + 0.35, TUBE_Y0 - 0.20, 0], [TUBE_XS[-1] + 0.35, TUBE_Y0 - 0.32, 0], color=TEXT, stroke_width=2.5),
        )
        start_lbl = T("same start", size=28, color=TEXT).next_to(start_line, DOWN, buff=0.18)
        self.play(
            *[s.animate.scale(1.35) for s in starters],
            Create(start_line), Create(start_ticks), FadeIn(start_lbl),
            run_time=1.8
        )
        rt1 = max(0.5, self.t_of("They receive") - 0.25 - self.elapsed())
        self.play(*[s.animate.scale(1 / 1.35) for s in starters], run_time=rt1)

        self.at("They receive")
        foods = VGroup(*[
            boxed_label("food", color=TEXT, size=22, pad=0.12, stroke=1.8, fill_opacity=0.12).move_to([cx, TUBE_Y1 + 0.54, 0])
            for cx in TUBE_XS
        ])
        self.play(FadeIn(foods), run_time=0.4)
        self.play(*[f.animate.shift(DOWN * 0.14).set_opacity(0.0) for f in foods], run_time=0.65)
        self.remove(foods)

        self.at("and grow")
        rt2 = max(0.8, self.t_of("The selecting phage") - 0.9 - self.elapsed())
        self.play(growth.animate.set_value(0.84), run_time=rt2, rate_func=linear)
        end_line = Line([TUBE_XS[0] - 0.35, TUBE_Y1 + 0.28, 0], [TUBE_XS[-1] + 0.35, TUBE_Y1 + 0.28, 0],
                        color=TEXT, stroke_width=2.5)
        end_ticks = VGroup(
            Line([TUBE_XS[0] - 0.35, TUBE_Y1 + 0.16, 0], [TUBE_XS[0] - 0.35, TUBE_Y1 + 0.28, 0], color=TEXT, stroke_width=2.5),
            Line([TUBE_XS[-1] + 0.35, TUBE_Y1 + 0.16, 0], [TUBE_XS[-1] + 0.35, TUBE_Y1 + 0.28, 0], color=TEXT, stroke_width=2.5),
        )
        end_lbl = T("similar final size", size=28, color=TEXT).next_to(end_line, UP, buff=0.12)
        self.play(Create(end_line), Create(end_ticks), FadeIn(end_lbl), run_time=0.7)

        self.at("The selecting phage")
        gate_hl = SurroundingRectangle(gate, color=RED, buff=0.10, stroke_width=3)
        shut_lbl = T("gate shut", size=28, color=RED).move_to([GATE_X + 1.15, TUBE_Y1 + 0.42, 0])
        self.play(Create(gate_hl), FadeIn(shut_lbl), run_time=0.8)
        rt3 = max(0.6, self.t_of("The growing branches") - 0.25 - self.elapsed())
        self.play(phages.animate.shift(LEFT * 0.14), run_time=rt3 * 0.5)
        self.play(phages.animate.shift(RIGHT * 0.14), FadeOut(gate_hl), run_time=rt3 * 0.5)

        self.at("The growing branches")
        self.play(growth.animate.set_value(1.0), run_time=1.2, rate_func=linear)
        segs = _tree_segments(TUBE_XS[4], TUBE_Y0, TUBE_Y1, TUBE_W, 4, depth=4)
        lineage_pts = [segs[0][0], segs[0][1]]
        cur_p = segs[0][1]
        for p0, p1, g, _ in segs[1:]:
            if np.allclose(p0, cur_p, atol=1e-3):
                lineage_pts.append(p1)
                cur_p = p1
        lineage = VMobject(color=TEXT, stroke_width=5).set_points_as_corners(lineage_pts)
        self.play(Create(lineage), run_time=2.2)
        self.finish()


# ------------------------------------------------------------------ Scene 3: Sequence Change
class S03SequenceChange(SpokenScene):
    def _base_strip(self, bases, changed_idx=None):
        tiles = VGroup()
        for i, b in enumerate(bases):
            col = YELLOW if i == changed_idx else BLUE
            rect = RoundedRectangle(
                corner_radius=0.08, width=0.92, height=0.82,
                stroke_color=col, stroke_width=3.2, fill_color=col, fill_opacity=0.22
            )
            lbl = M(b, size=34, color=col)
            tiles.add(VGroup(rect, lbl))
        tiles.arrange(RIGHT, buff=0.04)
        return tiles

    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        self.add(tag)

        parent_strip = self._base_strip(["A", "T", "G", "C", "A", "G"]).move_to([0, 0.8, 0])
        cell_box = RoundedRectangle(
            corner_radius=0.5, width=7.2, height=3.8,
            stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.06
        ).move_to([0, 0.2, 0])
        cell_box.layout_ok = True
        cell_lbl = T("dividing cell", size=28, color=BLUE).next_to(cell_box, UP, buff=0.18)

        self.play(FadeIn(cell_box), FadeIn(cell_lbl), FadeIn(parent_strip), run_time=0.6)
        copy_bot = self._base_strip(["A", "T", "G", "C", "A", "G"]).move_to([0, -0.65, 0])
        self.play(
            parent_strip.animate.move_to([0, 1.08, 0]),
            FadeIn(copy_bot, shift=DOWN * 0.35),
            run_time=1.3
        )

        self.at("sequence change")
        mut_tile = self._base_strip(["A", "T", "G", "T", "A", "G"], changed_idx=3).move_to([0, -0.65, 0])
        change_lbl = T("heritable sequence change", size=30, color=YELLOW).next_to(cell_box, DOWN, buff=0.25)
        rt1 = max(0.8, self.t_of("That cell") - 0.3 - self.elapsed())
        self.play(Transform(copy_bot[3], mut_tile[3]), FadeIn(change_lbl), run_time=min(1.2, rt1))
        if self.t_of("That cell") - 0.25 - self.elapsed() > 0.3:
            self.play(Indicate(copy_bot[3], color=YELLOW), run_time=self.t_of("That cell") - 0.25 - self.elapsed())

        self.at("That cell")
        tree_p = ValueTracker(0.32)
        tree_cx, tree_y0, tree_y1, tree_w = -0.8, -2.6, 2.7, 8.6
        tree = always_redraw(lambda: draw_tree_at(
            tree_cx, tree_y0, tree_y1, tree_w, 7, tree_p.get_value(),
            mut_info=(1, 1), stroke_w=6.2, tip_r=0.08, depth=4
        ))
        gate = make_gate(y0=-2.6, y1=2.7, x=4.6)
        phages = make_phage_swarm(xs=(5.3, 5.9, 5.4, 6.0), ys=(1.8, 0.9, -0.2, -1.2), scale=1.0)

        self.play(
            FadeOut(cell_box), FadeOut(cell_lbl), FadeOut(parent_strip), FadeOut(copy_bot), FadeOut(change_lbl),
            FadeIn(gate), FadeIn(phages),
            run_time=0.8
        )
        self.add(tree)
        segs = _tree_segments(tree_cx, tree_y0, tree_y1, tree_w, 7, mut_info=(1, 1), depth=4)
        mut_node_pos = segs[2][1]
        mut_ring = Circle(radius=0.22, color=YELLOW, stroke_width=4).move_to(mut_node_pos)
        self.play(Create(mut_ring), run_time=0.6)

        self.at("as the tree")
        rt2 = max(1.0, self.t_of("The changed cell") - 0.25 - self.elapsed())
        self.play(tree_p.animate.set_value(0.74), FadeOut(mut_ring), run_time=rt2, rate_func=linear)

        self.at("The changed cell")
        lbl_var = T("variant branch", size=28, color=YELLOW).move_to([2.2, 3.05, 0])
        lbl_unc = T("unchanged branch", size=28, color=BLUE).move_to([-3.2, 3.05, 0])
        rt3 = max(1.0, self.t_of("The change merely") - 0.25 - self.elapsed())
        self.play(
            tree_p.animate.set_value(0.90),
            FadeIn(lbl_var), FadeIn(lbl_unc),
            run_time=rt3, rate_func=linear
        )

        self.at("The change merely")
        self.play(tree_p.animate.set_value(1.0), run_time=2.4, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ Scene 4: Timing
class S04Timing(SpokenScene):
    def construct(self):
        tubes = VGroup(*[make_tube_glass(cx) for cx in TUBE_XS])
        gate = make_gate()
        phages = make_phage_swarm()
        tag = scope_tag("schematic", color=TEXT)
        t_val = ValueTracker(0.05)

        trees = always_redraw(lambda: VGroup(*[
            draw_tree_at(cx, TUBE_Y0, TUBE_Y1, TUBE_W, i, t_val.get_value(), mut_info=TUBE_MUTATIONS.get(i))
            for i, cx in enumerate(TUBE_XS)
        ]))

        bar_x0, bar_x1, bar_y = TUBE_XS[0] - 0.35, TUBE_XS[-1] + 0.35, -1.55
        track = Line([bar_x0, bar_y, 0], [bar_x1, bar_y, 0], color=GREY, stroke_width=5)
        fill_bar = always_redraw(lambda: Line(
            [bar_x0, bar_y, 0],
            [bar_x0 + t_val.get_value() * (bar_x1 - bar_x0), bar_y, 0],
            color=YELLOW, stroke_width=7
        ))
        knob = always_redraw(lambda: Dot(
            [bar_x0 + t_val.get_value() * (bar_x1 - bar_x0), bar_y, 0],
            radius=0.11, color=TEXT
        ))
        time_lbl = T("growth time", size=26, color=TEXT).next_to(track, DOWN, buff=0.22)

        self.add(tubes, trees, gate, phages, tag, track, fill_bar, knob, time_lbl)
        rt0 = max(0.8, self.t_of("An early event") - 0.25 - self.elapsed())
        self.play(t_val.animate.set_value(0.28), run_time=rt0, rate_func=linear)

        self.at("An early event")
        early_lbl = T("early", size=28, color=YELLOW).move_to([TUBE_XS[7], TUBE_Y1 + 0.38, 0])
        early_ring = Circle(radius=0.18, color=YELLOW, stroke_width=3.5).move_to([TUBE_XS[7], TUBE_Y0 + 0.80, 0])
        self.play(FadeIn(early_lbl), Create(early_ring), run_time=0.6)

        self.at("leaves a large")
        rt1 = max(1.0, self.t_of("A late event") - 0.25 - self.elapsed())
        self.play(t_val.animate.set_value(0.70), FadeOut(early_ring), run_time=rt1, rate_func=linear)

        self.at("A late event")
        late_lbl = T("late", size=28, color=YELLOW).move_to([TUBE_XS[4], TUBE_Y1 + 0.38, 0])
        late_ring = Circle(radius=0.16, color=YELLOW, stroke_width=3.5).move_to([TUBE_XS[4], TUBE_Y0 + 1.85, 0])
        self.play(FadeIn(late_lbl), Create(late_ring), run_time=0.6)
        rt2 = max(1.0, self.t_of("Some cultures") - 0.25 - self.elapsed())
        self.play(t_val.animate.set_value(0.90), FadeOut(late_ring), run_time=rt2, rate_func=linear)

        self.at("Some cultures")
        none_lbl = T("no event", size=28, color=BLUE).move_to([TUBE_XS[1], TUBE_Y1 + 0.38, 0])
        rt3 = max(1.0, self.t_of("Outcomes depend") - 0.25 - self.elapsed())
        self.play(FadeIn(none_lbl), t_val.animate.set_value(1.0), run_time=rt3, rate_func=linear)

        self.at("Outcomes depend")
        hl_early = SurroundingRectangle(tubes[7], color=YELLOW, buff=0.05, stroke_width=3)
        hl_late = SurroundingRectangle(tubes[4], color=YELLOW, buff=0.05, stroke_width=3)
        hl_none = SurroundingRectangle(tubes[1], color=BLUE, buff=0.05, stroke_width=3)
        rt4 = max(1.0, self.t_of("and if so") - 0.25 - self.elapsed())
        self.play(Create(hl_none), Create(hl_late), Create(hl_early), run_time=rt4)

        self.at("and if so")
        self.play(FadeOut(hl_none), FadeOut(hl_late), FadeOut(hl_early), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ Scene 5: Two Models
class S05TwoModels(SpokenScene):
    def construct(self):
        tubes = VGroup(*[make_tube_glass(cx) for cx in TUBE_XS])
        left_trees = VGroup(*[
            draw_tree_at(TUBE_XS[i], TUBE_Y0, TUBE_Y1, TUBE_W, i, 1.0, mut_info=TUBE_MUTATIONS.get(i))
            for i in range(5)
        ])
        right_p = ValueTracker(1.0)
        right_blue = ValueTracker(0.0)
        right_trees = always_redraw(lambda: VGroup(*[
            draw_tree_at(
                TUBE_XS[i], TUBE_Y0, TUBE_Y1, TUBE_W, i, right_p.get_value(),
                mut_info=TUBE_MUTATIONS.get(i),
                force_all_blue=(right_blue.get_value() > 0.5)
            )
            for i in range(5, 10)
        ]))
        gate = make_gate()
        phages = make_phage_swarm()
        tag = scope_tag("schematic", color=TEXT)

        left_frame = RoundedRectangle(
            corner_radius=0.18, width=5.10, height=TUBE_H + 0.44,
            stroke_color=YELLOW, stroke_width=3.2, fill_color=YELLOW, fill_opacity=0.07
        ).move_to([(TUBE_XS[0] + TUBE_XS[4]) / 2, TUBE_YC, 0])
        right_frame = RoundedRectangle(
            corner_radius=0.18, width=5.10, height=TUBE_H + 0.44,
            stroke_color=RED, stroke_width=3.2, fill_color=RED, fill_opacity=0.07
        ).move_to([(TUBE_XS[5] + TUBE_XS[9]) / 2, TUBE_YC, 0])
        left_frame.layout_ok = "outside"
        right_frame.layout_ok = "outside"

        left_lbl = T("variant during growth  ?", size=28, color=YELLOW).next_to(left_frame, UP, buff=0.18)
        right_lbl = T("induced after contact  ?", size=28, color=RED).next_to(right_frame, UP, buff=0.18)

        self.add(tubes, left_trees, right_trees, gate, phages, tag)
        rt0 = max(0.8, self.t_of("Perhaps the phage") - 0.25 - self.elapsed())
        self.play(
            FadeIn(left_frame), FadeIn(left_lbl),
            FadeIn(right_frame), FadeIn(right_lbl),
            run_time=rt0
        )

        self.at("Perhaps the phage")
        self.play(
            right_p.animate.set_value(0.10),
            gate.animate.shift(UP * 1.35 + RIGHT * 0.2).rotate(0.45),
            run_time=0.9, rate_func=linear
        )
        right_blue.set_value(1.0)
        rt1 = max(1.0, self.t_of("Then each exposed") - 0.25 - self.elapsed())
        self.play(
            right_p.animate.set_value(1.0),
            *[phages[k].animate.move_to([TUBE_XS[5 + k], 2.40, 0]) for k in range(5)],
            run_time=rt1, rate_func=linear
        )

        self.at("Then each exposed")
        targets = [
            (5, 0.18, 2.02),
            (6, -0.16, 2.02),
            (7, 0.08, 2.02),
            (8, -0.12, 2.02),
            (9, 0.14, 2.02),
        ]
        self.play(
            *[phages[k].animate.move_to([TUBE_XS[ti] + dx, ty + 0.24, 0]) for k, (ti, dx, ty) in enumerate(targets)],
            run_time=1.3
        )
        chosen = [targets[0], targets[2], targets[4]]
        contact_marks = VGroup()
        for ti, dx, ty in chosen:
            p0 = np.array([TUBE_XS[ti] + dx, ty - 0.18, 0.0])
            pL = np.array([TUBE_XS[ti] + dx - 0.09, TUBE_Y1 - 0.20, 0.0])
            pR = np.array([TUBE_XS[ti] + dx + 0.09, TUBE_Y1 - 0.20, 0.0])
            ring = Circle(radius=0.14, color=YELLOW, stroke_width=3.2, fill_color=YELLOW, fill_opacity=0.35).move_to([TUBE_XS[ti] + dx, ty, 0])
            twig = VGroup(
                Line(p0, pL, color=YELLOW, stroke_width=4.2),
                Line(p0, pR, color=YELLOW, stroke_width=4.2),
                Dot(pL, radius=0.052, color=YELLOW),
                Dot(pR, radius=0.052, color=YELLOW),
            )
            contact_marks.add(ring, twig)
        self.play(Create(contact_marks), run_time=1.8)
        rt2 = max(0.8, self.t_of("The competing models") - 0.25 - self.elapsed())
        contact_hl = VGroup(*[SurroundingRectangle(tubes[ti], color=RED, buff=0.03, stroke_width=2.5) for ti, _, _ in chosen])
        self.play(Create(contact_hl), run_time=rt2 * 0.55)
        self.play(FadeOut(contact_hl), run_time=rt2 * 0.45)

        self.at("The competing models")
        q_left = T("?", size=42, color=YELLOW).next_to(left_frame, DOWN, buff=0.30)
        q_right = T("?", size=42, color=RED).next_to(right_frame, DOWN, buff=0.30)
        self.play(FadeIn(q_left), FadeIn(q_right), run_time=0.8)
        self.play(Indicate(left_frame, color=YELLOW, scale_factor=1.018), run_time=1.5)
        self.play(Indicate(right_frame, color=RED, scale_factor=1.018), run_time=1.5)
        self.finish()


# ------------------------------------------------------------------ Helper for S06 & S07 Predict
def _predict_backdrop():
    tubes, trees, gate, phages = build_world(progress=1.0, include_mutations=True, gate_open=False)
    c1 = boxed_label("similar counts", color=TEXT, size=28).move_to([-3.2, 3.24, 0])
    c2 = boxed_label("jackpots + empty plates", color=TEXT, size=28).move_to([2.0, 3.24, 0])
    return VGroup(tubes, trees, gate, phages, c1, c2, scope_tag("schematic", color=TEXT))


# ------------------------------------------------------------------ Scene 6: Predict
class S06Predict(SpokenScene):
    def construct(self):
        tubes = VGroup(*[make_tube_glass(cx) for cx in TUBE_XS])
        growth = ValueTracker(0.55)
        trees = always_redraw(lambda: VGroup(*[
            draw_tree_at(cx, TUBE_Y0, TUBE_Y1, TUBE_W, i, growth.get_value(), mut_info=TUBE_MUTATIONS.get(i))
            for i, cx in enumerate(TUBE_XS)
        ]))
        gate = make_gate()
        phages = make_phage_swarm()
        tag = scope_tag("schematic", color=TEXT)
        self.add(tubes, trees, gate, phages, tag)

        rt0 = max(1.0, self.t_of("what pattern") - 0.25 - self.elapsed())
        self.play(growth.animate.set_value(1.0), run_time=rt0, rate_func=linear)

        self.at("what pattern")
        q = question_card("What pattern should appear after exposure?", y=-2.95, size=32, color=GOLD)
        rt1 = max(0.8, self.t_of("Similar survivor") - 0.25 - self.elapsed())
        self.play(FadeIn(q.question), run_time=min(1.2, rt1))
        if self.t_of("Similar survivor") - 0.25 - self.elapsed() > 0.3:
            self.play(Indicate(q.question, color=GOLD, scale_factor=1.01),
                      run_time=self.t_of("Similar survivor") - 0.25 - self.elapsed())

        self.at("Similar survivor")
        c1 = boxed_label("similar counts", color=TEXT, size=28).move_to([-3.2, 3.24, 0])
        rt2 = max(0.5, self.t_of("or uneven counts") - 0.25 - self.elapsed())
        self.play(FadeIn(c1), run_time=rt2)

        self.at("or uneven counts")
        c2 = boxed_label("jackpots + empty plates", color=TEXT, size=28).move_to([2.0, 3.24, 0])
        rt3 = max(0.7, self.t_of("Use the family") - 0.25 - self.elapsed())
        self.play(FadeIn(c2), run_time=min(1.0, rt3))
        if self.t_of("Use the family") - 0.25 - self.elapsed() > 0.3:
            self.play(Indicate(c2, color=TEXT, scale_factor=1.02),
                      run_time=self.t_of("Use the family") - 0.25 - self.elapsed())

        self.at("Use the family")
        hl_tubes = VGroup(*[
            SurroundingRectangle(tubes[i], color=YELLOW, buff=0.03, stroke_width=2.8)
            for i in (2, 4, 7, 8, 9)
        ])
        self.play(Create(hl_tubes), run_time=2.0)
        self.play(FadeOut(hl_tubes), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ Scene 7: Predict Pause
class S07PredictPause(PredictPause):
    QUESTION = "What pattern should appear after exposure?"
    CARD = {"y": -2.95, "size": 32}
    RING_AT = (5.8, -2.55, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _predict_backdrop()


# ------------------------------------------------------------------ Scene 8: Exposure
class S08Exposure(SpokenScene):
    def construct(self):
        tubes = VGroup(*[make_tube_glass(cx) for cx in TUBE_XS])
        blue_op = ValueTracker(1.0)
        trees = always_redraw(lambda: VGroup(*[
            draw_tree_at(cx, TUBE_Y0, TUBE_Y1, TUBE_W, i, 1.0, mut_info=TUBE_MUTATIONS.get(i),
                         blue_opacity=blue_op.get_value(), yellow_opacity=1.0)
            for i, cx in enumerate(TUBE_XS)
        ]))
        gate = make_gate()
        phages = make_phage_swarm()
        tag = scope_tag("schematic", color=TEXT)

        plate_y = -2.10
        empty_plates = VGroup(*[make_plate_colonies(cx, plate_y, 0, radius=0.40) for cx in TUBE_XS])
        guides = VGroup(*[
            DashedLine([cx, TUBE_Y0 - 0.05, 0], [cx, plate_y + 0.44, 0], color=GREY, stroke_width=1.8)
            for cx in TUBE_XS
        ])

        self.add(tubes, trees, gate, phages, empty_plates, guides, tag)

        self.at("open the gate")
        self.play(gate.animate.shift(UP * 1.45 + RIGHT * 0.25).rotate(0.45), run_time=0.8)
        sweep_xs = [TUBE_XS[9], TUBE_XS[7], TUBE_XS[5], TUBE_XS[3], TUBE_XS[1], TUBE_XS[0]]
        sweep_ys = [2.1, 1.4, 0.8, 1.9, 1.1, 0.4]
        rt1 = max(0.8, self.t_of("Phage removes") - 0.25 - self.elapsed())
        self.play(
            *[p.animate.move_to([sx, sy, 0]) for p, sx, sy in zip(phages, sweep_xs, sweep_ys)],
            run_time=rt1
        )

        self.at("Phage removes")
        rt2 = max(1.0, self.t_of("Resistant yellow") - 0.25 - self.elapsed())
        self.play(
            blue_op.animate.set_value(0.14),
            phages.animate.shift(LEFT * 1.15),
            run_time=rt2
        )

        self.at("Resistant yellow")
        full_plates = VGroup(*[make_plate_colonies(cx, plate_y, cnt, radius=0.40) for cx, cnt in zip(TUBE_XS, IND_COUNTS)])
        res_indices = [i for i, c in enumerate(IND_COUNTS) if c > 0]
        drops = VGroup(*[
            Dot([TUBE_XS[i], TUBE_Y0 + 0.4, 0], radius=0.105, color=YELLOW)
            for i in res_indices
        ])
        res_glow = VGroup(*[
            SurroundingRectangle(tubes[i], color=YELLOW, buff=0.04, stroke_width=2.8, fill_color=YELLOW, fill_opacity=0.16)
            for i in res_indices
        ])
        self.play(FadeIn(drops), FadeIn(res_glow), run_time=0.35)
        rt3 = max(1.0, self.t_of("Exposure changes") - 0.25 - self.elapsed())
        self.play(
            *[d.animate.move_to([TUBE_XS[i], plate_y, 0]) for d, i in zip(drops, res_indices)],
            run_time=rt3 * 0.45
        )
        self.play(
            FadeOut(drops),
            FadeOut(res_glow),
            Transform(empty_plates, full_plates),
            run_time=rt3 * 0.55
        )

        self.at("Exposure changes")
        link_7 = SurroundingRectangle(VGroup(tubes[7], empty_plates[7]), color=YELLOW, buff=0.08, stroke_width=3.6, fill_color=YELLOW, fill_opacity=0.18)
        link_0 = SurroundingRectangle(VGroup(tubes[0], empty_plates[0]), color=BLUE, buff=0.08, stroke_width=3.6, fill_color=BLUE, fill_opacity=0.18)
        rt4 = max(1.5, self.t_of("The phage acts") - 0.25 - self.elapsed())
        self.play(FadeIn(link_7), FadeIn(link_0), phages.animate.shift(LEFT * 1.35), run_time=rt4 * 0.45)
        self.play(Indicate(tubes[7], color=YELLOW, scale_factor=1.04), phages.animate.shift(RIGHT * 0.85), run_time=rt4 * 0.30)
        self.play(FadeOut(link_7), FadeOut(link_0), run_time=rt4 * 0.25)

        self.at("The phage acts")
        filter_line = Line([-6.1, -1.05, 0], [4.0, -1.05, 0], color=RED, stroke_width=5.5)
        filter_lbl = T("filter after growth", size=28, color=RED).move_to([-1.05, -3.05, 0])
        surv_rings = VGroup(*[
            SurroundingRectangle(empty_plates[i], color=YELLOW, buff=0.05, stroke_width=2.5)
            for i in (2, 4, 7, 8, 9)
        ])
        self.play(Create(filter_line), FadeIn(filter_lbl), run_time=1.8)
        self.play(Create(surv_rings), phages.animate.shift(RIGHT * 0.25), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ Scene 9: Pattern
class S09Pattern(SpokenScene):
    def construct(self):
        plate_y = 2.15
        plates = VGroup(*[
            make_plate_colonies(TUBE_XS[i] + 0.55, plate_y, cnt, radius=0.35)
            for i, cnt in enumerate(IND_COUNTS)
        ])
        num_lbls = VGroup(*[
            M(str(cnt), size=26, color=TEXT).move_to([TUBE_XS[i] + 0.55, 2.84, 0])
            for i, cnt in enumerate(IND_COUNTS)
        ])
        illus_tag = T("illustrative", size=24, color=TEXT).move_to([-5.55, 3.45, 0])
        tag = scope_tag("schematic", color=TEXT)

        ax_x0, ax_x1, ax_y = -5.6, 5.8, 0.20
        to_x = lambda v: ax_x0 + (v / 55.0) * (ax_x1 - ax_x0)
        axis = Line([ax_x0, ax_y, 0], [ax_x1, ax_y, 0], color=GREY, stroke_width=3.2)
        ticks = VGroup()
        tick_lbls = VGroup()
        for tv in (0, 10, 20, 30, 40, 50):
            tx = to_x(tv)
            ticks.add(Line([tx, ax_y, 0], [tx, ax_y - 0.12, 0], color=GREY, stroke_width=2.6))
            tick_lbls.add(M(str(tv), size=24, color=TEXT).next_to([tx, ax_y - 0.12, 0], DOWN, buff=0.10))
        ax_title = T("resistant colonies per culture", size=26, color=TEXT).next_to(tick_lbls, DOWN, buff=0.16)

        self.add(plates, num_lbls, illus_tag, tag, axis, ticks, tick_lbls, ax_title)

        seen = {}
        dot_targets = []
        for cnt in IND_COUNTS:
            k = seen.get(cnt, 0)
            seen[cnt] = k + 1
            dot_targets.append([to_x(cnt), ax_y + 0.22 + k * 0.25, 0])

        dots = VGroup(*[
            Dot([TUBE_XS[i] + 0.55, plate_y, 0], radius=0.115, color=YELLOW)
            for i in range(10)
        ])
        drop_traces = VGroup(*[
            DashedLine([TUBE_XS[i] + 0.55, plate_y - 0.36, 0], dot_targets[i], color=GREY, stroke_width=1.6)
            for i in range(10)
        ])
        rt0 = max(1.0, self.t_of("several empty") - 0.25 - self.elapsed())
        self.play(
            LaggedStart(*[d.animate.move_to(pos) for d, pos in zip(dots, dot_targets)], lag_ratio=0.06),
            FadeIn(drop_traces),
            run_time=rt0
        )

        self.at("several empty")
        zeros = VGroup(*[dots[i] for i, c in enumerate(IND_COUNTS) if c == 0])
        z_plates = VGroup(*[
            SurroundingRectangle(plates[i], color=TEXT, buff=0.06, stroke_width=2.8, fill_color=TEXT, fill_opacity=0.12)
            for i, c in enumerate(IND_COUNTS) if c == 0
        ])
        z_ring = SurroundingRectangle(zeros, color=TEXT, buff=0.09, stroke_width=3.0, fill_color=TEXT, fill_opacity=0.14)
        rt1 = max(0.5, self.t_of("some small") - 0.25 - self.elapsed())
        self.play(FadeOut(drop_traces), Create(z_ring), Create(z_plates), run_time=rt1)

        self.at("some small")
        smalls = VGroup(*[dots[i] for i, c in enumerate(IND_COUNTS) if 0 < c < 10])
        s_plates = VGroup(*[
            SurroundingRectangle(plates[i], color=YELLOW, buff=0.06, stroke_width=2.8, fill_color=YELLOW, fill_opacity=0.14)
            for i, c in enumerate(IND_COUNTS) if 0 < c < 10
        ])
        s_ring = SurroundingRectangle(smalls, color=YELLOW, buff=0.09, stroke_width=3.0, fill_color=YELLOW, fill_opacity=0.16)
        rt2 = max(0.5, self.t_of("an occasional jackpot") - 0.25 - self.elapsed())
        self.play(FadeOut(z_ring), FadeOut(z_plates), Create(s_ring), Create(s_plates), run_time=rt2)

        self.at("an occasional jackpot")
        jackpot_dot = dots[7]
        j_plate = SurroundingRectangle(plates[7], color=YELLOW, buff=0.07, stroke_width=3.2, fill_color=YELLOW, fill_opacity=0.18)
        j_ring = Circle(radius=0.25, color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.16).move_to(jackpot_dot)
        j_link = DashedLine(plates[7].get_bottom(), j_ring.get_top(), color=YELLOW, stroke_width=2.4)
        j_lbl = T("52 (jackpot)", size=26, color=YELLOW).next_to(j_ring, LEFT, buff=0.16)
        rt3 = max(0.8, self.t_of("resistance predicts") - 0.25 - self.elapsed())
        self.play(
            FadeOut(s_ring), FadeOut(s_plates),
            Create(j_plate), Create(j_link), Create(j_ring), FadeIn(j_lbl),
            run_time=rt3
        )

        self.at("resistance predicts")
        red_w_t = ValueTracker(0.08)
        yel_w_t = ValueTracker(0.08)
        red_y, yel_y = -1.32, -2.48
        mean_x = to_x(6.0)
        red_band = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.10, width=max(0.10, red_w_t.get_value()), height=0.44,
            stroke_color=RED, stroke_width=2.8, fill_color=RED, fill_opacity=0.34
        ).move_to([mean_x, red_y, 0]))
        red_lbl = T("contact model (schematic)", size=26, color=RED).move_to([to_x(27.0), red_y, 0])

        yel_band = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.10, width=max(0.10, yel_w_t.get_value()), height=0.44,
            stroke_color=YELLOW, stroke_width=2.8, fill_color=YELLOW, fill_opacity=0.28
        ).move_to([to_x(26.0 * (yel_w_t.get_value() / (to_x(52) - to_x(0))) + 6.0 * (1 - yel_w_t.get_value() / (to_x(52) - to_x(0)))), yel_y, 0]))
        yel_lbl = T("growth model (schematic)", size=26, color=YELLOW).move_to([to_x(27.0), -1.90, 0])

        self.add(red_band, yel_band)
        rt4 = max(1.2, self.t_of("Averages alone") - 0.25 - self.elapsed())
        self.play(
            FadeOut(j_ring), FadeOut(j_plate), FadeOut(j_link),
            red_w_t.animate.set_value(to_x(10) - to_x(2)),
            yel_w_t.animate.set_value(to_x(52) - to_x(0)),
            FadeIn(red_lbl), FadeIn(yel_lbl),
            run_time=rt4
        )

        self.at("Averages alone")
        mean_line = DashedLine([mean_x, ax_y + 0.25, 0], [mean_x, yel_y - 0.32, 0], color=TEXT, stroke_width=3.2)
        mean_lbl = T("mean = 6", size=26, color=TEXT).next_to(mean_line, DOWN, buff=0.10)
        self.play(Create(mean_line), FadeIn(mean_lbl), run_time=2.0)
        self.play(Indicate(mean_lbl, color=TEXT, scale_factor=1.04), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ Scene 10: Evidence
class S10Evidence(SpokenScene):
    def construct(self):
        tag = scope_tag("illustrative", color=TEXT)
        self.add(tag)

        top_title = T("independent cultures", size=28, color=YELLOW).move_to([-3.3, 3.22, 0])
        top_tubes = VGroup()
        for i in range(10):
            tx = -5.85 + i * 0.56
            glass = RoundedRectangle(corner_radius=0.08, width=0.44, height=1.35, stroke_color=GREY, stroke_width=2.4,
                                     fill_color=BG, fill_opacity=0.4).move_to([tx, 2.08, 0])
            tree = draw_tree_at(tx, 1.40, 2.75, 0.44, i, 1.0, mut_info=TUBE_MUTATIONS.get(i),
                                stroke_w=2.5, tip_r=0.032, depth=3)
            top_tubes.add(VGroup(glass, tree))

        ax_x0, ax_x1 = 0.2, 6.2
        to_x = lambda v: ax_x0 + (v / 55.0) * (ax_x1 - ax_x0)
        top_y, bot_y = 1.65, -1.35

        ax_top = Line([ax_x0, top_y, 0], [ax_x1, top_y, 0], color=GREY, stroke_width=2.8)
        ax_bot = Line([ax_x0, bot_y, 0], [ax_x1, bot_y, 0], color=GREY, stroke_width=2.8)
        ticks_b = VGroup()
        tlbls_b = VGroup()
        for tv in (0, 10, 20, 30, 40, 50):
            tx = to_x(tv)
            ticks_b.add(Line([tx, bot_y, 0], [tx, bot_y - 0.11, 0], color=GREY, stroke_width=2.4))
            tlbls_b.add(M(str(tv), size=22, color=TEXT).next_to([tx, bot_y - 0.11, 0], DOWN, buff=0.08))
        ax_lbl = T("resistant colonies", size=24, color=TEXT).next_to(tlbls_b, DOWN, buff=0.14)

        rt0 = max(1.0, self.t_of("with repeated samples") - 0.25 - self.elapsed())
        self.play(FadeIn(top_title), FadeIn(top_tubes), run_time=min(1.4, rt0 * 0.5))
        self.play(
            FadeIn(ax_top), FadeIn(ax_bot), FadeIn(ticks_b), FadeIn(tlbls_b), FadeIn(ax_lbl),
            run_time=max(0.6, self.t_of("with repeated samples") - 0.25 - self.elapsed())
        )

        self.at("with repeated samples")
        bot_title = T("one bulk culture", size=28, color=BLUE).move_to([-3.3, 0.25, 0])
        flask = RoundedRectangle(corner_radius=0.22, width=1.8, height=1.35, stroke_color=BLUE, stroke_width=3.0,
                                 fill_color=BLUE, fill_opacity=0.20).move_to([-5.3, -1.0, 0])
        rng = np.random.default_rng(7)
        specks = VGroup(*[
            Dot([-5.3 + rng.uniform(-0.62, 0.62), -1.0 + rng.uniform(-0.44, 0.44), 0], radius=0.045, color=YELLOW)
            for _ in range(12)
        ])
        bulk_plates = VGroup(*[
            make_plate_colonies(-3.8 + i * 0.42, -2.35, cnt, radius=0.19, seed=100 + i)
            for i, cnt in enumerate(BULK_COUNTS)
        ])
        pour_drops = VGroup(*[Dot([-4.35, -1.0, 0], radius=0.058, color=BLUE) for _ in range(10)])
        self.play(FadeIn(bot_title), FadeIn(flask), FadeIn(specks), run_time=0.6)
        self.add(pour_drops)
        rt1 = max(1.0, self.t_of("Independent cultures scattered") - 0.25 - self.elapsed())
        self.play(*[d.animate.move_to([-3.8 + i * 0.42, -2.35, 0]) for i, d in enumerate(pour_drops)], run_time=rt1 * 0.6)
        self.play(FadeOut(pour_drops), FadeIn(bulk_plates), run_time=rt1 * 0.4)

        self.at("Independent cultures scattered")
        seen_i = {}
        ind_targets = []
        for c in IND_COUNTS:
            k = seen_i.get(c, 0)
            seen_i[c] = k + 1
            ind_targets.append([to_x(c), top_y + 0.16 + k * 0.21, 0])

        ind_spread = ValueTracker(0.0)
        mean_x = to_x(6.0)
        ind_launch = VGroup(*[
            Dot([top_tubes[i].get_center()[0], top_y + 0.16, 0], radius=0.092, color=YELLOW)
            for i in range(10)
        ])
        self.play(
            LaggedStart(*[d.animate.move_to([mean_x, top_y + 0.16, 0]) for d in ind_launch], lag_ratio=0.04),
            run_time=1.0
        )
        self.remove(ind_launch)

        ind_var_full = float(np.var(IND_COUNTS, ddof=1))  # ~262.0
        ind_dots = always_redraw(lambda: VGroup(*[
            Dot([
                to_x(6.0 + ind_spread.get_value() * (c - 6.0)),
                (top_y + 0.16) * (1.0 - ind_spread.get_value()) + ind_targets[i][1] * ind_spread.get_value(),
                0
            ], radius=0.092, color=YELLOW)
            for i, c in enumerate(IND_COUNTS)
        ]))
        ind_band = always_redraw(lambda: Rectangle(
            width=max(0.08, to_x(6.0 + ind_spread.get_value() * 46.0) - to_x(6.0 + ind_spread.get_value() * (-6.0))),
            height=0.14, color=YELLOW, stroke_width=2.0, fill_color=YELLOW, fill_opacity=0.28
        ).move_to([
            0.5 * (to_x(6.0 + ind_spread.get_value() * (-6.0)) + to_x(6.0 + ind_spread.get_value() * 46.0)),
            top_y + 0.08,
            0
        ]))
        ind_stat = always_redraw(lambda: VGroup(
            M("mean = 6", size=26, color=TEXT),
            M(f"variance ≈ {ind_var_full * (ind_spread.get_value() ** 2):.0f}", size=26, color=YELLOW),
        ).arrange(RIGHT, buff=0.35).move_to([3.85, 2.95, 0]))
        self.add(ind_band, ind_dots)
        self.play(FadeIn(ind_stat), run_time=0.4)
        rt2 = max(1.5, self.t_of("Repeated bulk") - 0.25 - self.elapsed())
        self.play(ind_spread.animate.set_value(1.0), run_time=rt2 * 0.65, rate_func=linear)
        self.play(Indicate(ind_band, color=YELLOW, scale_factor=1.04), run_time=rt2 * 0.35)

        self.at("Repeated bulk")
        self.play(LaggedStart(*[Indicate(p, color=BLUE, scale_factor=1.18) for p in bulk_plates], lag_ratio=0.10), run_time=1.5)
        seen_b = {}
        bulk_targets = []
        for c in BULK_COUNTS:
            k = seen_b.get(c, 0)
            seen_b[c] = k + 1
            bulk_targets.append([to_x(c), bot_y + 0.16 + k * 0.21, 0])

        bulk_spread = ValueTracker(0.0)
        bulk_launch = VGroup(*[
            Dot([bulk_plates[i].get_center()[0], -2.35, 0], radius=0.092, color=BLUE)
            for i in range(10)
        ])
        self.play(
            LaggedStart(*[d.animate.move_to([mean_x, bot_y + 0.16, 0]) for d in bulk_launch], lag_ratio=0.04),
            run_time=0.9
        )
        self.remove(bulk_launch)

        bulk_var_full = float(np.var(BULK_COUNTS, ddof=1))  # 4.0
        bulk_dots = always_redraw(lambda: VGroup(*[
            Dot([
                to_x(6.0 + bulk_spread.get_value() * (c - 6.0)),
                (bot_y + 0.16) * (1.0 - bulk_spread.get_value()) + bulk_targets[i][1] * bulk_spread.get_value(),
                0
            ], radius=0.092, color=BLUE)
            for i, c in enumerate(BULK_COUNTS)
        ]))
        bulk_band = always_redraw(lambda: Rectangle(
            width=max(0.08, to_x(6.0 + bulk_spread.get_value() * 3.0) - to_x(6.0 + bulk_spread.get_value() * (-3.0))),
            height=0.14, color=BLUE, stroke_width=2.0, fill_color=BLUE, fill_opacity=0.35
        ).move_to([mean_x, bot_y + 0.08, 0]))
        bulk_stat = always_redraw(lambda: VGroup(
            M("mean = 6", size=26, color=TEXT),
            M(f"variance = {bulk_var_full * (bulk_spread.get_value() ** 2):.0f}", size=26, color=BLUE),
        ).arrange(RIGHT, buff=0.35).move_to([3.85, -0.15, 0]))
        self.add(bulk_band, bulk_dots)
        self.play(FadeIn(bulk_stat), run_time=0.4)
        rt3 = max(1.0, self.t_of("contrast tests") - 0.25 - self.elapsed())
        self.play(bulk_spread.animate.set_value(1.0), run_time=rt3 * 0.60, rate_func=linear)
        self.play(Indicate(bulk_band, color=BLUE, scale_factor=1.10), run_time=rt3 * 0.40)

        self.at("contrast tests")
        mean_line = DashedLine([mean_x, top_y + 0.9, 0], [mean_x, bot_y - 0.05, 0], color=TEXT, stroke_width=2.8)
        self.play(Create(mean_line), run_time=1.0)
        self.play(Indicate(ind_stat[1], color=YELLOW, scale_factor=1.06), Indicate(bulk_stat[1], color=BLUE, scale_factor=1.06), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ Scene 11: Scope
class S11Scope(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        self.add(tag)

        rep_indices = [0, 4, 7, 8]
        rep_xs = [-5.0, -3.5, -2.0, -0.5]
        tubes = VGroup(*[make_tube_glass(rx, y0=-1.6, y1=1.8, w=0.95) for rx in rep_xs])
        blue_op = ValueTracker(1.0)
        trees = always_redraw(lambda: VGroup(*[
            draw_tree_at(rx, -1.6, 1.8, 0.95, idx, 1.0, mut_info=TUBE_MUTATIONS.get(idx),
                         blue_opacity=blue_op.get_value(), yellow_opacity=1.0)
            for rx, idx in zip(rep_xs, rep_indices)
        ]))
        gate = make_gate(y0=-1.6, y1=1.8, x=0.35)
        phages = make_phage_swarm(xs=(0.95, 1.15, 0.90), ys=(1.2, 0.3, -0.7), scale=0.9)

        scope_box = RoundedRectangle(
            corner_radius=0.18, width=7.5, height=4.4,
            stroke_color=TEXT, stroke_width=3.2, fill_opacity=0
        ).move_to([-2.3, 0.1, 0])
        scope_box.layout_ok = True
        scope_lbl = T("this phage-resistance system", size=28, color=TEXT).next_to(scope_box, UP, buff=0.20)

        rt0 = max(1.0, self.t_of("phage resistance arose") - 0.25 - self.elapsed())
        self.play(FadeIn(scope_box), FadeIn(scope_lbl), FadeIn(tubes), FadeIn(gate), FadeIn(phages), run_time=min(1.2, rt0))
        self.add(trees)
        if self.t_of("phage resistance arose") - 0.25 - self.elapsed() > 0.3:
            self.play(Indicate(tubes[2], color=YELLOW), run_time=self.t_of("phage resistance arose") - 0.25 - self.elapsed())

        self.at("phage resistance arose")
        self.play(gate.animate.shift(RIGHT * 0.55 + DOWN * 0.15).scale(0.82).rotate(-0.28), run_time=0.8)
        rt1 = max(1.5, self.t_of("Mutation rates") - 0.25 - self.elapsed())
        self.play(
            *[p.animate.move_to([rx, ry, 0]) for p, rx, ry in zip(phages, [-0.5, -2.0, -3.5], [0.8, 0.1, -0.4])],
            blue_op.animate.set_value(0.18),
            run_time=rt1
        )

        self.at("Mutation rates")
        c = np.array([4.05, 1.30, 0.0])
        r = 1.38
        rate_t = ValueTracker(0.28)
        track = Arc(radius=r, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=13)
        sector = always_redraw(lambda: Sector(
            radius=r * 0.94, start_angle=PI,
            angle=-PI * float(np.clip(rate_t.get_value(), 0.02, 0.98)),
            arc_center=c, color=YELLOW, fill_opacity=0.18, stroke_width=0
        ))
        val_arc = always_redraw(lambda: Arc(
            radius=r, start_angle=PI, angle=-PI * float(np.clip(rate_t.get_value(), 0.02, 0.98)),
            arc_center=c, stroke_color=YELLOW, stroke_width=13
        ))
        needle = always_redraw(lambda: Line(
            c,
            c + 0.85 * r * np.array([np.cos(PI - PI * rate_t.get_value()), np.sin(PI - PI * rate_t.get_value()), 0]),
            color=TEXT, stroke_width=5.5
        ))
        hub = Dot(c, radius=0.09, color=TEXT)
        gauge_lbl = T("mutation rate", size=28, color=YELLOW).move_to(c + DOWN * 0.48)

        conds = VGroup(
            boxed_label("condition A", color=TEXT, size=24),
            boxed_label("condition B", color=TEXT, size=24),
            boxed_label("condition C", color=TEXT, size=24),
        ).arrange(DOWN, buff=0.18).move_to([4.05, -1.00, 0])

        self.play(FadeIn(track), FadeIn(gauge_lbl), FadeIn(conds), FadeIn(hub), run_time=0.6)
        self.add(sector, val_arc, needle)
        rt2 = max(1.5, self.t_of("Changing a rate") - 0.25 - self.elapsed())
        self.play(
            conds[0][0].animate.set_stroke(YELLOW, width=3.5).set_fill(YELLOW, opacity=0.22),
            rate_t.animate.set_value(0.28),
            run_time=rt2 * 0.2
        )
        self.play(
            conds[0][0].animate.set_stroke(TEXT, width=2.5).set_fill(TEXT, opacity=0.08),
            conds[1][0].animate.set_stroke(YELLOW, width=3.5).set_fill(YELLOW, opacity=0.22),
            rate_t.animate.set_value(0.58),
            run_time=rt2 * 0.4
        )
        self.play(
            conds[1][0].animate.set_stroke(TEXT, width=2.5).set_fill(TEXT, opacity=0.08),
            conds[2][0].animate.set_stroke(YELLOW, width=3.5).set_fill(YELLOW, opacity=0.22),
            rate_t.animate.set_value(0.36),
            run_time=rt2 * 0.4
        )

        self.at("Changing a rate")
        not_dir = boxed_label("not directed", color=RED, size=26, pad=0.12, fill_opacity=0.16).move_to([4.05, -2.62, 0])
        pre_hl = VGroup(*[
            SurroundingRectangle(tubes[k], color=YELLOW, buff=0.05, stroke_width=2.8, fill_color=YELLOW, fill_opacity=0.12)
            for k in (1, 2, 3)
        ])
        self.play(
            conds[2][0].animate.set_stroke(TEXT, width=2.5).set_fill(TEXT, opacity=0.08),
            rate_t.animate.set_value(0.50),
            FadeIn(not_dir),
            FadeIn(pre_hl),
            run_time=1.8
        )
        self.play(FadeOut(pre_hl), Indicate(not_dir, color=RED, scale_factor=1.05), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------ Scene 12: Rule
class S12Rule(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        self.add(tag)

        tree_cx, tree_y0, tree_y1, tree_w = -0.7, -2.5, 2.7, 9.2
        p = ValueTracker(0.15)
        blue_op = ValueTracker(1.0)
        tree = always_redraw(lambda: draw_tree_at(
            tree_cx, tree_y0, tree_y1, tree_w, 7, p.get_value(),
            mut_info=(1, 1), blue_opacity=blue_op.get_value(), yellow_opacity=1.0,
            stroke_w=6.2, tip_r=0.08, depth=4
        ))
        self.add(tree)
        rt0 = max(0.6, self.t_of("heritable") - 0.2 - self.elapsed())
        self.play(p.animate.set_value(0.42), run_time=rt0, rate_func=linear)

        self.at("heritable")
        segs = _tree_segments(tree_cx, tree_y0, tree_y1, tree_w, 7, mut_info=(1, 1), depth=4)
        node_pos = segs[2][1]
        seq_badge = boxed_label("sequence change", color=YELLOW, size=26).next_to(node_pos, DR, buff=0.22)
        node_ring = Circle(radius=0.20, color=YELLOW, stroke_width=4).move_to(node_pos)
        self.play(Create(node_ring), FadeIn(seq_badge), run_time=0.8)

        self.at("Selection changes")
        rt1 = max(1.0, self.t_of("The sequence change") - 0.25 - self.elapsed())
        self.play(p.animate.set_value(0.75), FadeOut(node_ring), run_time=rt1, rate_func=linear)

        self.at("The sequence change")
        self.play(FadeOut(seq_badge), run_time=0.35)
        origin_lbl = T("origin", size=32, color=YELLOW).next_to(node_pos, DOWN, buff=0.52).shift(LEFT * 0.55)
        rt2 = max(1.0, self.t_of("The environment") - 0.25 - self.elapsed())
        self.play(
            FadeIn(origin_lbl),
            p.animate.set_value(1.0),
            run_time=rt2, rate_func=linear
        )

        self.at("The environment")
        wave = VGroup(*[make_phage(scale=1.1).move_to([5.6, y, 0]) for y in np.linspace(-0.7, 2.2, 6)])
        self.play(FadeIn(wave), run_time=0.5)
        rt3 = max(1.5, self.t_of("Keep origin") - 0.9 - self.elapsed())
        self.play(
            wave.animate.shift(LEFT * 10.2),
            blue_op.animate.set_value(0.10),
            run_time=rt3
        )
        sorting_lbl = T("sorting", size=32, color=RED).move_to([4.35, 1.35, 0])
        self.play(FadeIn(sorting_lbl), run_time=0.6)

        self.at("Keep origin")
        self.play(Indicate(origin_lbl, color=YELLOW), run_time=1.8)
        self.play(Indicate(sorting_lbl, color=RED), run_time=1.8)
        self.finish()


# ------------------------------------------------------------------ Scene 13: End Card
class S13End(EndCard):
    LINE = "Mutation creates heritable DNA variants;\nselection changes how common they become."
