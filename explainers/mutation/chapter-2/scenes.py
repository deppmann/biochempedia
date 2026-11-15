"""
COLOUR MAP (used consistently across the whole film):
- BLUE   (#58C4DD): Unchanged DNA sequence blocks, original strand, ancestor cell
- YELLOW (#F5D547): Changed DNA sequence / wrong block / inherited mutant block and variant lineage
- RED    (#FC6255): Chemical damage / lesion mark, outside mutagens, phage particles
- GREEN  (#83C167): Accurate DNA repair, repair gate, restored original block
- TEXT   (#E8EAF0): Neutral labels, brackets, headings, "heritable change" criterion, neutral outlines
- GOLD   (#D4A843): Predict question highlight and title rule
- GREY   (#8B93A1): Structural conveyor rails and dimmed background tracks only (never text)

ONE WORLD CARRIED ACROSS THE FILM:
A bacterial cell lineage (from Film 1) zooms into a double-stranded DNA sequence strip built from
paired labelled blocks riding a left-to-right copying conveyor into a Y-shaped fork: one branch
leads through a GREEN repair gate back to an all-BLUE strip, and the other enters an open copying
station that splits into daughter sequences.

WHAT CHANGES ON SCREEN (per spoken scene) AND WHAT IT IS COMPUTED FROM:
- s00_link_and_question: Lineage tree grows then rewinds to the pre-branch blue ancestor, zooms
  into its paired BLUE block strip on the moving conveyor, a RED lesion lands on block 4 when
  damage is named, and 'Mutation yet?' appears above the single damaged strip before any daughter forms.
- s02_definition: Conveyor rollers turn continuously under the carried strip, the RED lesion
  flickers while blue block letters stay fixed, 'damage' and 'sequence' labels point to each,
  a scan bar confirms unchanged letters, and the WHITE 'heritable change' bracket stays empty.
- s03_two_entries: Upper and lower BLUE strips ride animated conveyor lanes through an open-sided
  copying station; the upper strip gains one YELLOW block inside the station while a RED damage
  badge lands on the lower strip ahead of the station.
- s04_fork: Damaged strip sits at the fork entrance while three computed cubic-Bezier fork branches
  extend through open repair and copying gates to an all-BLUE repair outcome, an all-BLUE copied
  outcome, and a YELLOW changed outcome, then a tight ring highlights the lesion.
- s05_predict: Damaged strip rewinds along the entry rail to the fork entrance while a tracer
  sweeps each dimmed Bezier branch toward two neutral daughter outlines under the predict question.
- s07_repair: Damaged strip glides along the brightened GREEN branch into the open repair gate,
  the RED mark lifts off, a BLUE replacement block slides into the vacated slot, and copying yields
  two all-BLUE daughter strips while the 'heritable change' bracket stays empty.
- s08_fixed_change: Brightened copying path leads into Copy 1 where a YELLOW wrong block pairs
  opposite the RED lesion, then Copy 2 separates the strands so the YELLOW strand templates a full
  YELLOW base-pair change while the RED parental strand exits to a 'repair or bypass' branch and
  the 'heritable change' bracket closes on the stable YELLOW position.
- s09_sources: Carried conveyor sits beneath 'copying error' and 'DNA damage' as tokens stream
  along computed arrows from 'spontaneous' (left) and 'induced' (right) cards into both entrances,
  then converge through one shared 'heritable sequence change?' gate to output a YELLOW block.
- s10_consequences: A YELLOW-marked strip sits beside the neutral outcomes board as three branches
  grow (the occasional branch drawn thinner), then fold back into a single YELLOW sequence block
  between strip and board.
- s11_selection_link: The YELLOW strip transforms into a single YELLOW cell inside the culture
  tube, divides into a 4-cell yellow family, and only then do RED phage icons arrive outside the
  closed gate above an 'origin first, sorting later' arrow.
- s12_rule: Two copies of the damaged strip travel simultaneously down the GREEN repair path
  (erased into an all-BLUE strip) and the copying path (transformed into a YELLOW block shared by
  descendants), ending centered on the YELLOW block labelled 'inherited sequence change'.
- s13_text_bridge: Unlabelled blank source cards flow continuously under 'spontaneous sources' and
  'induced sources' into the fork while an unlabelled bacterial plate outline with '?' forms on the right.
"""

from bp_parts import *

# Canonical 7-base-pair sequence used across the DNA strip scenes
BASE_PAIRS = [("A", "T"), ("C", "G"), ("G", "C"), ("G", "C"), ("T", "A"), ("A", "T"), ("C", "G")]
MINI_PAIRS = [("A", "T"), ("C", "G"), ("G", "C"), ("T", "A"), ("C", "G")]
CHANGED_MINI = [("A", "T"), ("C", "G"), ("A", "T"), ("T", "A"), ("C", "G")]


def dna_block(letter, color=BLUE, w=0.66, h=0.52, size=26, fill_opacity=0.40, stroke_opacity=1.0):
    """One DNA base block with crisp full-opacity letter inside."""
    rect = RoundedRectangle(
        corner_radius=0.10, width=w, height=h,
        stroke_color=color, stroke_width=3.5, stroke_opacity=stroke_opacity,
        fill_color=color, fill_opacity=fill_opacity,
    )
    txt = M(letter, size=size, color=TEXT if color != YELLOW else YELLOW, weight=BOLD).move_to(rect)
    return VGroup(rect, txt)


def dna_strip(pairs=BASE_PAIRS, block_w=0.66, block_h=0.50, gap_x=0.10, gap_y=0.10,
              top_colors=None, bot_colors=None, size=26, damage_idx=None, label=None,
              fill_opacity=0.40, stroke_opacity=1.0):
    """Paired two-strand DNA strip of labelled blocks; optional red damage badge above block damage_idx."""
    n = len(pairs)
    top_colors = top_colors or [BLUE] * n
    bot_colors = bot_colors or [BLUE] * n
    cols = VGroup()
    top_blocks = VGroup()
    bot_blocks = VGroup()
    for i, (t_let, b_let) in enumerate(pairs):
        tb = dna_block(t_let, top_colors[i], w=block_w, h=block_h, size=size,
                       fill_opacity=fill_opacity, stroke_opacity=stroke_opacity)
        bb = dna_block(b_let, bot_colors[i], w=block_w, h=block_h, size=size,
                       fill_opacity=fill_opacity, stroke_opacity=stroke_opacity)
        col = VGroup(tb, bb).arrange(DOWN, buff=gap_y)
        cols.add(col)
        top_blocks.add(tb)
        bot_blocks.add(bb)
    cols.arrange(RIGHT, buff=gap_x)
    g = VGroup(cols)
    g.cols = cols
    g.top_blocks = top_blocks
    g.bot_blocks = bot_blocks
    g.badge = None
    if damage_idx is not None:
        badge = damage_badge(width=block_w * 0.78).next_to(top_blocks[damage_idx], UP, buff=0.08)
        g.add(badge)
        g.badge = badge
    if label:
        lab = T(label, size=26, color=TEXT).next_to(cols, DOWN, buff=0.18)
        g.add(lab)
        g.label = lab
    return g


def damage_badge(width=0.52):
    """A jagged RED crack/lesion badge clearly separate from block text."""
    h = width * 0.52
    tri = Polygon(
        [-width / 2, -h * 0.35, 0],
        [0, h * 0.65, 0],
        [width / 2, -h * 0.35, 0],
        stroke_color=RED, stroke_width=3.0, fill_color=RED, fill_opacity=0.35,
    )
    bolt = VMobject(stroke_color=RED, stroke_width=4.0).set_points_as_corners([
        [-width * 0.16, h * 0.25, 0],
        [width * 0.05, h * 0.05, 0],
        [-width * 0.08, -h * 0.05, 0],
        [width * 0.16, -h * 0.25, 0],
    ])
    return VGroup(tri, bolt)


def set_badge_opacity(badge, op):
    """Adjust lesion triangle/bolt opacity while keeping translucent triangle fill so bolt stays visible."""
    badge[0].set_stroke(opacity=op)
    badge[0].set_fill(opacity=0.35 * op)
    badge[1].set_stroke(opacity=op)


def animated_conveyor(phase_tracker, x0=-5.8, x1=5.8, y=-1.35, spacing=0.9, rail_color=GREY, tick_color=BLUE):
    """Conveyor whose belt ticks glide smoothly with phase_tracker."""
    rail_top = Line([x0, y + 0.14, 0], [x1, y + 0.14, 0], color=rail_color, stroke_width=4.0)
    rail_bot = Line([x0, y - 0.14, 0], [x1, y - 0.14, 0], color=rail_color, stroke_width=4.0)

    def mk_ticks():
        p = phase_tracker.get_value() % spacing
        xs = np.arange(x0 + 0.2 + p, x1 - 0.2, spacing)
        return VGroup(*[
            Line([x, y - 0.11, 0], [x, y + 0.11, 0], color=tick_color, stroke_width=4.5)
            for x in xs
        ])

    ticks = always_redraw(mk_ticks)
    return VGroup(rail_top, rail_bot, ticks)


def open_station(label, center, width=2.8, height=1.25, color=TEXT, label_pos="top",
                 size=28, opacity=1.0, fill_opacity=0.20):
    """Open-sided gate/station with top and bottom jaws so DNA strips pass through with no crossing border."""
    cx, cy = center[0], center[1]
    hw, hh = width / 2, height / 2
    jaw_drop = 0.20
    bg = RoundedRectangle(
        corner_radius=0.14, width=width, height=height,
        stroke_width=0, fill_color=color, fill_opacity=fill_opacity * opacity,
    ).move_to([cx, cy, 0])
    top_jaw = VMobject(stroke_color=color, stroke_width=3.5, stroke_opacity=opacity).set_points_as_corners([
        [cx - hw, cy + hh - jaw_drop, 0],
        [cx - hw, cy + hh, 0],
        [cx + hw, cy + hh, 0],
        [cx + hw, cy + hh - jaw_drop, 0],
    ])
    bot_jaw = VMobject(stroke_color=color, stroke_width=3.5, stroke_opacity=opacity).set_points_as_corners([
        [cx - hw, cy - hh + jaw_drop, 0],
        [cx - hw, cy - hh, 0],
        [cx + hw, cy - hh, 0],
        [cx + hw, cy - hh + jaw_drop, 0],
    ])
    lbl = T(label, size=size, color=color, weight=BOLD)
    if label_pos == "top":
        lbl.next_to(top_jaw, UP, buff=0.12)
    else:
        lbl.next_to(bot_jaw, DOWN, buff=0.12)
    g = VGroup(bg, top_jaw, bot_jaw, lbl)
    g.bg = bg
    g.top_jaw = top_jaw
    g.bot_jaw = bot_jaw
    g.lbl = lbl
    g.left_port = np.array([cx - hw, cy, 0.0])
    g.right_port = np.array([cx + hw, cy, 0.0])
    return g


def criterion_bracket(width=4.1, height=0.95, status="empty", center=(0.0, -2.35, 0)):
    """The carried WHITE 'heritable change' bracket: empty dashed slot or closed YELLOW slot."""
    c = np.array(center, dtype=float)
    left_b = VMobject(stroke_color=TEXT, stroke_width=4.0).set_points_as_corners([
        c + [-width / 2 + 0.2, height / 2, 0],
        c + [-width / 2, height / 2, 0],
        c + [-width / 2, -height / 2, 0],
        c + [-width / 2 + 0.2, -height / 2, 0],
    ])
    right_b = VMobject(stroke_color=TEXT, stroke_width=4.0).set_points_as_corners([
        c + [width / 2 - 0.2, height / 2, 0],
        c + [width / 2, height / 2, 0],
        c + [width / 2, -height / 2, 0],
        c + [width / 2 - 0.2, -height / 2, 0],
    ])
    lab = T("heritable change", size=28, color=TEXT).move_to(c + UP * 0.16)
    if status == "empty":
        slot = DashedVMobject(
            RoundedRectangle(corner_radius=0.08, width=1.5, height=0.34, stroke_color=TEXT, stroke_width=2.2),
            num_dashes=10,
        ).move_to(c + DOWN * 0.22)
    else:
        slot = RoundedRectangle(
            corner_radius=0.08, width=1.5, height=0.34,
            stroke_color=YELLOW, stroke_width=3.0, fill_color=YELLOW, fill_opacity=0.30,
        ).move_to(c + DOWN * 0.22)
    g = VGroup(left_b, right_b, lab, slot)
    g.slot = slot
    g.brackets = VGroup(left_b, right_b)
    return g


def smooth_branch(p0, p1, color=GREY, width=5.5, opacity=1.0):
    """Smooth S-curve path connecting p0 -> p1 with horizontal tangents."""
    p0, p1 = np.array(p0, dtype=float), np.array(p1, dtype=float)
    dx = (p1[0] - p0[0]) * 0.48
    return CubicBezier(
        p0, p0 + RIGHT * dx, p1 - RIGHT * dx, p1,
        stroke_color=color, stroke_width=width, stroke_opacity=opacity,
    )


def build_fork_world(dim_paths=False, show_outcomes=True, show_neutral_outlines=False, gate_label_size=28):
    """Carried Y-fork geometry used across s04, s05, s06, s07, s12, s13.

    Entry conveyor rail sits below the parked strip at y = -0.68 so no line ever crosses DNA text.
    A short stem connects [-2.85, 0.0] to junction [-2.35, 0.0]:
      - Upper repair branch: [-2.35, 0.0] -> [-1.15, 1.80] -> open repair gate [0.25, 1.80] -> [1.65, 1.80] -> [2.70, 1.80]
      - Lower copying branch: [-2.35, 0.0] -> [-1.15, -1.00] -> open copying gate [0.25, -1.00] -> [1.65, -1.00] -> splits:
          * Original blue daughter: [1.65, -1.00] -> [2.70, -0.10]
          * Changed yellow daughter: [1.65, -1.00] -> [2.70, -2.05]
    """
    path_op = 0.35 if dim_paths else 1.0
    entry_rail = Line([-5.85, -0.68, 0], [-2.35, -0.68, 0], color=TEXT, stroke_width=4.0, stroke_opacity=path_op)
    entry_stem = Line([-2.80, 0.0, 0], [-2.35, 0.0, 0], color=TEXT, stroke_width=5.0, stroke_opacity=path_op)
    entry = VGroup(entry_rail, entry_stem)
    junc = Dot([-2.35, 0.0, 0], radius=0.10, color=TEXT).set_opacity(path_op)

    up_in = smooth_branch([-2.35, 0.0, 0], [-1.15, 1.80, 0], color=GREEN, width=7.0, opacity=path_op)
    repair_gate = open_station("repair", center=[0.25, 1.80, 0], width=2.8, height=1.45,
                               color=GREEN, label_pos="top", size=gate_label_size, opacity=1.0 if not dim_paths else 0.75)
    up_out = Line([1.65, 1.80, 0], [2.70, 1.80, 0], color=GREEN, stroke_width=7.0, stroke_opacity=path_op)

    dn_in = smooth_branch([-2.35, 0.0, 0], [-1.15, -1.00, 0], color=TEXT, width=7.0, opacity=path_op)
    copy_gate = open_station("copying", center=[0.25, -1.00, 0], width=2.8, height=1.30,
                             color=TEXT, label_pos="bottom", size=gate_label_size, opacity=1.0 if not dim_paths else 0.75)
    mid_out = smooth_branch([1.65, -1.00, 0], [2.70, -0.10, 0], color=BLUE, width=7.0, opacity=path_op)
    bot_out = smooth_branch([1.65, -1.00, 0], [2.70, -2.05, 0], color=YELLOW, width=7.0, opacity=path_op)

    all_blue = [BLUE] * 5
    yel_pair = [BLUE, BLUE, YELLOW, BLUE, BLUE]

    outcomes = VGroup()
    if show_outcomes:
        s_rep = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                          top_colors=all_blue, bot_colors=all_blue, size=24).move_to([4.35, 1.80, 0])
        l_rep = T("restored original", size=26, color=GREEN).next_to(s_rep, UP, buff=0.14)
        s_orig = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                           top_colors=all_blue, bot_colors=all_blue, size=24).move_to([4.35, -0.10, 0])
        l_orig = T("original sequence", size=26, color=BLUE).next_to(s_orig, UP, buff=0.14)
        s_mut = dna_strip(CHANGED_MINI, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                          top_colors=yel_pair, bot_colors=yel_pair, size=24).move_to([4.35, -2.05, 0])
        l_mut = T("changed sequence", size=26, color=YELLOW).next_to(s_mut, UP, buff=0.14)
        outcomes.add(VGroup(s_rep, l_rep), VGroup(s_orig, l_orig), VGroup(s_mut, l_mut))

    neutral_outlines = VGroup()
    if show_neutral_outlines:
        for y in (1.05, -0.95):
            box = DashedVMobject(
                RoundedRectangle(corner_radius=0.12, width=2.8, height=0.95, stroke_color=TEXT, stroke_width=3.0),
                num_dashes=22,
            ).move_to([4.35, y, 0])
            q = T("?", size=34, color=TEXT).move_to(box)
            neutral_outlines.add(VGroup(box, q))

    world = VGroup(entry, junc, up_in, up_out, repair_gate, dn_in, copy_gate, mid_out, bot_out, outcomes, neutral_outlines)
    world.entry = entry
    world.entry_rail = entry_rail
    world.entry_stem = entry_stem
    world.junc = junc
    world.up_in = up_in
    world.up_out = up_out
    world.repair_gate = repair_gate
    world.dn_in = dn_in
    world.copy_gate = copy_gate
    world.mid_out = mid_out
    world.bot_out = bot_out
    world.outcomes = outcomes
    world.neutral_outlines = neutral_outlines
    return world


def make_phage_icon(scale=1.0):
    """Simple geometric schematic phage icon (no molecular detail)."""
    head = RegularPolygon(n=6, radius=0.22 * scale, color=RED, stroke_width=3.0, fill_color=RED, fill_opacity=0.30)
    tail = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.28 * scale, color=RED, stroke_width=3.5)
    leg_l = Line(tail.get_end(), tail.get_end() + DL * 0.16 * scale, color=RED, stroke_width=2.5)
    leg_r = Line(tail.get_end(), tail.get_end() + DR * 0.16 * scale, color=RED, stroke_width=2.5)
    return VGroup(head, tail, leg_l, leg_r)


# ------------------------------------------------------------------ Scenes

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        # Part 1: Film 1's lineage tree (blue ancestors + early yellow branch) -> rewind to pre-branch blue cell
        trunk = Line([-5.5, 0.0, 0], [-3.2, 0.0, 0], color=BLUE, stroke_width=6.0)
        b_up = smooth_branch([-3.2, 0.0, 0], [0.0, 1.75, 0], color=BLUE, width=5.5)
        b_up2 = smooth_branch([0.0, 1.75, 0], [4.9, 2.35, 0], color=BLUE, width=5.0)
        b_mid = smooth_branch([-3.2, 0.0, 0], [4.9, 0.25, 0], color=BLUE, width=5.5)
        b_dn = smooth_branch([-3.2, 0.0, 0], [-0.9, -1.45, 0], color=BLUE, width=5.5)
        y_branch = smooth_branch([-0.9, -1.45, 0], [4.9, -1.85, 0], color=YELLOW, width=6.5)

        origin_dot = Dot([-0.9, -1.45, 0], radius=0.14, color=BLUE, stroke_color=TEXT, stroke_width=3.0)
        origin_lbl = T("origin", size=28, color=BLUE).next_to(origin_dot, DOWN, buff=0.22)
        sel_zone = DashedLine([2.1, -2.5, 0], [2.1, 2.6, 0], color=TEXT, stroke_width=3.0)
        sel_lbl = T("selection", size=28, color=TEXT).next_to(sel_zone, UP, buff=0.18)
        var_lbl = T("variant branch", size=28, color=YELLOW).next_to(y_branch.get_end(), DOWN, buff=0.32).align_to(y_branch.get_end(), RIGHT)

        tree = VGroup(trunk, b_up, b_up2, b_mid, b_dn, y_branch, origin_dot, origin_lbl, sel_zone, sel_lbl, var_lbl)
        self.play(Create(trunk), Create(b_up), Create(b_mid), Create(b_dn), run_time=1.2)
        self.play(Create(b_up2), Create(y_branch), FadeIn(sel_zone), FadeIn(sel_lbl), FadeIn(var_lbl), run_time=1.4)
        self.play(FadeIn(origin_dot), FadeIn(origin_lbl), run_time=0.5)

        # Rewind marker sliding backward along the yellow branch to the blue ancestor cell
        rew_dot = Dot([4.9, -1.85, 0], radius=0.18, color=YELLOW, stroke_color=TEXT, stroke_width=3.0)
        self.play(FadeIn(rew_dot), run_time=0.3)
        self.play(MoveAlongPath(rew_dot, y_branch.copy().reverse_points()), run_time=1.0)

        # Zoom into the blue ancestor cell -> its large DNA strip of labelled BLUE blocks
        self.at("Now")
        cell_ring = RoundedRectangle(corner_radius=1.2, width=10.8, height=4.5, stroke_color=BLUE,
                                     stroke_width=4.0, fill_color=BLUE, fill_opacity=0.08).move_to([0, -0.25, 0])
        strip = dna_strip(BASE_PAIRS, block_w=0.88, block_h=0.66, gap_x=0.14, gap_y=0.14, size=28).move_to([0, -0.10, 0])
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.45))
        conv = animated_conveyor(phase, x0=-5.4, x1=5.4, y=-1.45, spacing=0.95)
        self.add(phase)

        self.play(
            FadeOut(tree), FadeOut(rew_dot),
            FadeIn(cell_ring), FadeIn(strip), FadeIn(conv),
            run_time=0.95,
        )

        # Red mark lands when "is damaged" is spoken (before "is the cell mutated yet?")
        self.at("is damaged")
        badge = damage_badge(width=0.72).next_to(strip.top_blocks[3], UP, buff=0.10)
        badge_start = badge.get_center() + UP * 1.15
        badge.move_to(badge_start)
        self.play(
            badge.animate.move_to(strip.top_blocks[3].get_top() + UP * (0.10 + badge.height / 2)),
            strip.top_blocks[3][0].animate.set_stroke(RED, width=4.0),
            run_time=0.75,
        )

        self.at("is the cell mutated yet")
        q_text = T("Mutation yet?", size=42, color=GOLD, weight=BOLD).move_to([0, 2.75, 0])
        self.play(FadeIn(q_text, shift=DOWN * 0.15), run_time=0.9)

        self.at("Follow how that variant")
        hl = SurroundingRectangle(strip.cols, color=BLUE, stroke_width=3.5, buff=0.14)
        self.play(Create(hl), run_time=1.0)
        self.play(FadeOut(hl), run_time=0.7)

        self.at("The red mark appears")
        badge_ring = SurroundingRectangle(badge, color=RED, stroke_width=3.5, buff=0.08)
        self.play(Create(badge_ring), run_time=1.0)
        self.play(badge_ring.animate.set_stroke(GOLD, width=4.0), run_time=1.0)
        self.play(FadeOut(badge_ring), run_time=0.7)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        cell_ring = RoundedRectangle(corner_radius=1.2, width=10.8, height=4.0, stroke_color=BLUE,
                                     stroke_width=4.0, fill_color=BLUE, fill_opacity=0.08).move_to([0, -1.15, 0])
        strip = dna_strip(BASE_PAIRS, block_w=0.84, block_h=0.58, gap_x=0.13, gap_y=0.12,
                          size=28, damage_idx=3).move_to([0, -0.85, 0])
        strip.top_blocks[3][0].set_stroke(RED, width=4.0)
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.55))
        conv = animated_conveyor(phase, x0=-5.4, x1=5.4, y=-2.20, spacing=0.95)
        t_pulse = ValueTracker(0.0)
        t_pulse.add_updater(lambda m, dt: m.increment_value(dt))
        strip.badge.add_updater(lambda m: m.set_stroke(width=3.0 + 2.0 * np.sin(7.0 * t_pulse.get_value())))

        self.add(tag, cell_ring, strip, conv, phase, t_pulse)

        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD)
        brand.layout_ok = True
        lesson = T("MUTATION: WHERE VARIATION COMES FROM", size=22, color=TEXT)
        title = T("When Damage Becomes Mutation", size=48, font=TITLE_FONT, color=TEXT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.18).move_to([0, 2.20, 0])

        self.play(FadeIn(g, shift=UP * 0.1), run_time=self.beat(0.28))
        self.wait(self.beat(0.54))
        self.play(FadeOut(g), run_time=self.beat(0.18))
        self.finish()


class S02Definition(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        strip = dna_strip(BASE_PAIRS, block_w=0.94, block_h=0.68, gap_x=0.14, gap_y=0.14,
                          size=30, damage_idx=3).move_to([-1.15, 0.25, 0])
        strip.top_blocks[3][0].set_stroke(RED, width=4.0)
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.85))
        conv = animated_conveyor(phase, x0=-5.5, x1=5.5, y=-1.02, spacing=0.85)
        self.add(tag, strip, conv, phase)

        # Red damage mark flickers continuously while preserving triangle transparency over the bolt
        t_flick = ValueTracker(0.0)
        t_flick.add_updater(lambda m, dt: m.increment_value(dt))
        strip.badge.add_updater(
            lambda m: set_badge_opacity(m, 0.35 + 0.65 * abs(np.sin(6.5 * t_flick.get_value())))
        )
        self.add(t_flick)

        self.at("heritable change")
        crit = criterion_bracket(width=4.3, height=1.05, status="empty", center=(-1.45, -2.35, 0))
        self.play(
            FadeIn(crit, run_time=1.1),
            strip.animate(run_time=3.5, rate_func=linear).move_to([-0.35, 0.25, 0]),
        )

        self.at("Heritable matters here")
        self.play(
            strip.animate(rate_func=linear).move_to([0.0, 0.25, 0]),
            crit.brackets.animate(rate_func=there_and_back).set_color(GOLD),
            run_time=2.0,
        )

        self.at("chemical lesion is damage")
        dmg_lbl = T("damage", size=34, color=RED, weight=BOLD).move_to([2.5, 2.55, 0])
        dmg_arr = Arrow(
            dmg_lbl.get_bottom() + DOWN * 0.10,
            strip.badge.get_top() + UR * 0.14,
            color=RED, stroke_width=4.5, buff=0.0, max_tip_length_to_length_ratio=0.18,
        )
        seq_lbl = T("sequence", size=34, color=BLUE, weight=BOLD).move_to([-2.5, 2.55, 0])
        seq_brace = Line(
            [strip.cols[0].get_left()[0], 1.78, 0],
            [strip.cols[2].get_right()[0], 1.78, 0],
            color=BLUE, stroke_width=4.5,
        )
        self.play(FadeIn(dmg_lbl), Create(dmg_arr), FadeIn(seq_lbl), Create(seq_brace), run_time=1.3)

        self.at("not automatically a changed sequence")
        scan = Rectangle(
            width=0.96, height=1.80,
            stroke_width=0, fill_color=BLUE, fill_opacity=0.26,
        ).move_to([strip.cols[0].get_center()[0], 0.25, 0])
        self.play(FadeIn(scan), run_time=0.2)
        self.play(scan.animate.move_to([strip.cols[-1].get_center()[0], 0.25, 0]), run_time=2.6, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.25)

        self.at("must change and persist")
        div_lbl = T("cell divides", size=28, color=TEXT).move_to([2.55, -2.35, 0])
        div_arr = Arrow(crit.get_right() + RIGHT * 0.14, div_lbl.get_left() + LEFT * 0.14,
                        color=TEXT, stroke_width=4.0, buff=0.0)
        self.play(FadeIn(div_lbl), Create(div_arr), run_time=1.0)

        self.at("when the cell divides")
        d_top = RoundedRectangle(corner_radius=0.26, width=0.95, height=0.52, stroke_color=BLUE,
                                 stroke_width=3.5, fill_color=BLUE, fill_opacity=0.18).move_to([4.95, -1.88, 0])
        d_bot = RoundedRectangle(corner_radius=0.26, width=0.95, height=0.52, stroke_color=BLUE,
                                 stroke_width=3.5, fill_color=BLUE, fill_opacity=0.18).move_to([4.95, -2.82, 0])
        arr_d1 = Arrow(div_lbl.get_right() + RIGHT * 0.12, d_top.get_left() + LEFT * 0.10, color=BLUE, stroke_width=3.5, buff=0.0)
        arr_d2 = Arrow(div_lbl.get_right() + RIGHT * 0.12, d_bot.get_left() + LEFT * 0.10, color=BLUE, stroke_width=3.5, buff=0.0)
        self.play(
            crit.slot.animate.set_stroke(GOLD),
            Create(arr_d1), Create(arr_d2),
            FadeIn(d_top), FadeIn(d_bot),
            run_time=1.3,
        )
        self.finish()


class S03TwoEntries(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        # Open-sided copying station spanning both lanes (no vertical walls crossing the DNA strips)
        st_bg = RoundedRectangle(
            corner_radius=0.18, width=2.4, height=4.6,
            stroke_width=0, fill_color=BLUE, fill_opacity=0.14,
        ).move_to([0.9, 0.15, 0])
        top_jaw = VMobject(stroke_color=TEXT, stroke_width=3.5).set_points_as_corners([
            [-0.3, 2.15, 0], [-0.3, 2.45, 0], [2.1, 2.45, 0], [2.1, 2.15, 0],
        ])
        bot_jaw = VMobject(stroke_color=TEXT, stroke_width=3.5).set_points_as_corners([
            [-0.3, -1.85, 0], [-0.3, -2.15, 0], [2.1, -2.15, 0], [2.1, -1.85, 0],
        ])
        st_lbl = T("copying station", size=30, color=TEXT, weight=BOLD).next_to(top_jaw, UP, buff=0.16)

        # Upper lane: copying error; Lower lane: damage (animated conveyor rails below both)
        up_y, dn_y = 1.38, -1.02
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.85))
        up_conv = animated_conveyor(phase, x0=-5.9, x1=5.9, y=up_y - 0.82, spacing=0.85, rail_color=GREY, tick_color=BLUE)
        dn_conv = animated_conveyor(phase, x0=-5.9, x1=5.9, y=dn_y - 0.82, spacing=0.85, rail_color=GREY, tick_color=BLUE)
        self.add(phase)

        up_lbl = T("copying error", size=28, color=YELLOW, weight=BOLD).move_to([-4.2, up_y + 0.90, 0])
        dn_lbl = T("damage", size=28, color=RED, weight=BOLD).move_to([-4.2, dn_y + 0.90, 0])

        s_up = dna_strip(MINI_PAIRS, block_w=0.56, block_h=0.44, gap_x=0.08, gap_y=0.08, size=25).move_to([-3.8, up_y, 0])
        s_dn = dna_strip(MINI_PAIRS, block_w=0.56, block_h=0.44, gap_x=0.08, gap_y=0.08, size=25).move_to([-3.8, dn_y, 0])

        self.play(
            FadeIn(st_bg), Create(top_jaw), Create(bot_jaw), FadeIn(st_lbl),
            FadeIn(up_conv), FadeIn(dn_conv),
            FadeIn(up_lbl), FadeIn(dn_lbl),
            FadeIn(s_up), FadeIn(s_dn),
            run_time=0.9,
        )

        self.play(s_up.animate.shift(RIGHT * 1.6), s_dn.animate.shift(RIGHT * 0.9), run_time=1.8, rate_func=linear)

        self.at("Copying can place")
        self.play(s_up.animate.move_to([0.9, up_y, 0]), s_dn.animate.shift(RIGHT * 0.4), run_time=0.95, rate_func=linear)
        wrong_b = dna_block("T", YELLOW, w=0.56, h=0.44, size=25).move_to(s_up.bot_blocks[2])
        self.play(FadeOut(s_up.bot_blocks[2], run_time=0.18))
        s_up.bot_blocks[2].become(wrong_b)
        self.play(FadeIn(s_up.bot_blocks[2], run_time=0.25))
        self.play(s_up.animate.move_to([3.95, up_y, 0]), run_time=0.90, rate_func=linear)

        self.at("Or chemistry can damage")
        badge = damage_badge(width=0.50).next_to(s_dn.top_blocks[2], UP, buff=0.08)
        badge_hi = badge.copy().shift(UP * 0.78)
        self.play(FadeIn(badge_hi), run_time=0.3)
        self.play(
            badge_hi.animate.move_to(badge),
            s_dn.top_blocks[2][0].animate.set_stroke(RED, width=3.5),
            run_time=0.9,
        )
        s_dn.add(badge_hi)
        self.play(s_dn.animate.move_to([-1.60, dn_y, 0]), run_time=1.6, rate_func=linear)

        self.at("Either route can end")
        up_no = T("no mutation?", size=26, color=TEXT).move_to([4.35, up_y + 0.90, 0])
        dn_no = T("no mutation?", size=26, color=TEXT).move_to([4.35, dn_y + 0.90, 0])
        self.play(
            FadeIn(up_no), FadeIn(dn_no),
            s_dn.animate(rate_func=linear).move_to([-1.10, dn_y, 0]),
            run_time=1.8,
        )
        self.finish()


class S04Fork(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        world = build_fork_world(dim_paths=False, show_outcomes=True)
        strip = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                          size=24, damage_idx=2).move_to([-4.6, 0.0, 0])
        strip.top_blocks[2][0].set_stroke(RED, width=3.5)

        self.play(Create(world.entry), FadeIn(world.junc), FadeIn(strip), run_time=1.0)
        self.play(strip.animate.move_to([-4.2, 0.0, 0]), run_time=1.6, rate_func=linear)

        self.at("Repair may restore")
        self.play(
            Create(world.up_in), FadeIn(world.repair_gate), Create(world.up_out),
            FadeIn(world.outcomes[0]),
            run_time=1.8,
        )

        self.at("If repair misses it")
        self.play(Create(world.dn_in), FadeIn(world.copy_gate), run_time=1.4)

        self.at("preserve the original sequence")
        self.play(Create(world.mid_out), FadeIn(world.outcomes[1]), run_time=1.2)

        self.at("or produce a different one")
        self.play(Create(world.bot_out), FadeIn(world.outcomes[2]), run_time=1.2)

        self.at("lesion's presence")
        ring = SurroundingRectangle(strip.badge, color=RED, stroke_width=4.0, buff=0.07)
        self.play(Create(ring), run_time=0.8)
        self.play(ring.animate.set_stroke(GOLD, width=4.0), run_time=1.0, rate_func=there_and_back)
        self.play(FadeOut(ring), run_time=0.5)
        self.finish()


def predict_backdrop(pulse_badge=False):
    """Exact shared backdrop between end of s05_predict and s06_predict_pause."""
    tag = scope_tag("schematic", size=24, color=TEXT)
    world = build_fork_world(dim_paths=True, show_outcomes=False, show_neutral_outlines=True)
    strip = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                      size=24, damage_idx=2).move_to([-4.35, 0.0, 0])
    strip.top_blocks[2][0].set_stroke(RED, width=3.5)
    if pulse_badge:
        strip.badge._t = 0.0
        def _pulse(m, dt):
            m._t += dt
            set_badge_opacity(m, 0.35 + 0.65 * abs(np.sin(5.0 * m._t)))
        strip.badge.add_updater(_pulse)

        world.neutral_outlines._t = 0.0
        def _pulse_outlines(m, dt):
            m._t += dt
            op = 0.45 + 0.55 * abs(np.sin(3.5 * m._t))
            for item in m:
                item[0].set_stroke(opacity=op)
                item[1].set_opacity(op)
        world.neutral_outlines.add_updater(_pulse_outlines)
    return VGroup(tag, world, strip)


class S05Predict(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        world_bright = build_fork_world(dim_paths=False, show_outcomes=True)
        world_dim = build_fork_world(dim_paths=True, show_outcomes=False, show_neutral_outlines=True)

        strip = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                          size=24, damage_idx=2).move_to([-4.15, 0.0, 0])
        strip.top_blocks[2][0].set_stroke(RED, width=3.5)

        self.add(tag, world_bright, strip)
        outcomes_out = world_bright.outcomes
        world_bright.remove(outcomes_out)
        self.play(
            strip.animate.move_to([-4.35, 0.0, 0]),
            FadeOut(outcomes_out),
            ReplacementTransform(world_bright, world_dim),
            run_time=2.3,
        )

        self.at("must a red damage mark")
        q = question_card("Must the damage become a mutation?", y=-2.95, color=GOLD, size=34, max_w=10.2)
        hl_badge = SurroundingRectangle(strip.badge, color=RED, stroke_width=4.0, buff=0.08)
        self.play(FadeIn(q.question, shift=UP * 0.1), Create(hl_badge), run_time=1.3)
        self.play(FadeOut(hl_badge), run_time=0.7)

        self.at("Trace every possible path")
        tr = Dot([-2.35, 0.0, 0], radius=0.16, color=GOLD, stroke_color=TEXT, stroke_width=3.0)
        self.play(FadeIn(tr), run_time=0.2)
        self.play(MoveAlongPath(tr, world_dim.up_in), run_time=0.60)
        tr.move_to(world_dim.up_out.get_start())
        self.play(MoveAlongPath(tr, world_dim.up_out), run_time=0.45)
        tr.move_to([-2.35, 0.0, 0])
        self.play(MoveAlongPath(tr, world_dim.dn_in), run_time=0.55)
        tr.move_to(world_dim.mid_out.get_start())
        self.play(MoveAlongPath(tr, world_dim.mid_out), run_time=0.45)
        tr.move_to(world_dim.bot_out.get_start())
        self.play(MoveAlongPath(tr, world_dim.bot_out), run_time=0.50)
        self.play(FadeOut(tr), run_time=0.2)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "Must the damage become a mutation?"
    CARD = {"y": -2.95, "size": 34, "max_w": 10.2}
    RING_AT = (6.0, -2.42, 0)
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop(pulse_badge=True)


class S07Repair(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        world = build_fork_world(dim_paths=True, show_outcomes=False)
        strip = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                          size=24, damage_idx=2).move_to([-4.35, 0.0, 0])
        strip.top_blocks[2][0].set_stroke(RED, width=3.5)

        no_lbl = T("No.", size=42, color=GREEN, weight=BOLD).move_to([-4.6, 2.55, 0])
        self.add(tag, world, strip)
        self.play(FadeIn(no_lbl, shift=DOWN * 0.1), run_time=0.55)

        self.at("On one path")
        bright_up_in = smooth_branch([-2.35, 0.0, 0], [-1.15, 1.80, 0], color=GREEN, width=7.0, opacity=1.0)
        bright_up_out = Line([1.65, 1.80, 0], [2.70, 1.80, 0], color=GREEN, stroke_width=7.0, stroke_opacity=1.0)
        self.play(Create(bright_up_in), Create(bright_up_out), run_time=0.75)

        self.at("repair removes the lesion")
        self.play(strip.animate.move_to([0.25, 1.80, 0]), run_time=0.70)
        self.play(FadeOut(strip.badge, shift=UP * 0.25), run_time=0.45)
        strip.remove(strip.badge)

        self.at("restores the blue block")
        fresh_g = dna_block("G", BLUE, w=0.50, h=0.40, size=24).move_to(strip.top_blocks[2])
        old_blk = strip.top_blocks[2]
        self.play(FadeOut(old_blk, run_time=0.25))
        fresh_start = fresh_g.copy().shift(UP * 0.22)
        self.play(FadeIn(fresh_start, run_time=0.2))
        self.play(fresh_start.animate.move_to(old_blk.get_center()), run_time=0.60)
        self.remove(fresh_start)
        strip.top_blocks[2].become(fresh_g)
        self.add(strip.top_blocks[2])

        self.at("After copying")
        self.play(strip.animate.move_to([2.40, 1.80, 0]), run_time=1.1)

        self.at("both daughter strips")
        d1 = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07, size=24).move_to([4.65, 2.15, 0])
        d2 = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07, size=24).move_to([4.65, 0.30, 0])
        l_d1 = T("daughter 1 (original)", size=24, color=BLUE).next_to(d1, UP, buff=0.18)
        l_d2 = T("daughter 2 (original)", size=24, color=BLUE).next_to(d2, DOWN, buff=0.18)
        arr1 = Arrow([2.70, 1.80, 0], d1.get_left() + LEFT * 0.12, color=BLUE, stroke_width=4.0, buff=0.0)
        arr2 = Arrow([2.70, 1.80, 0], d2.get_left() + LEFT * 0.12, color=BLUE, stroke_width=4.0, buff=0.0)
        self.play(
            Create(arr1), Create(arr2),
            ReplacementTransform(strip, d1),
            FadeIn(d2, shift=DOWN * 0.2),
            FadeIn(l_d1), FadeIn(l_d2),
            run_time=1.55,
        )

        self.at("yet no mutation remains")
        crit = criterion_bracket(width=4.2, height=1.00, status="empty", center=(-4.0, -2.35, 0))
        self.play(FadeIn(crit), run_time=1.2)
        self.finish()


class S08FixedChange(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        # Open-sided Copy 1 and Copy 2 stations with real arrows and strands entering them
        s0 = dna_strip(MINI_PAIRS, block_w=0.44, block_h=0.38, gap_x=0.06, gap_y=0.06,
                       size=24, damage_idx=2).move_to([-4.85, 0.45, 0])
        s0.top_blocks[2][0].set_stroke(RED, width=3.5)

        c1_st = open_station("copy 1", center=[-1.75, 0.45, 0], width=2.55, height=1.65, color=TEXT, label_pos="top", size=26)
        arr_in = Arrow([-3.55, 0.45, 0], c1_st.left_port + LEFT * 0.06, color=TEXT, stroke_width=4.5, buff=0.0)

        self.play(FadeIn(s0), Create(arr_in), FadeIn(c1_st), run_time=1.0)

        self.at("copying places a wrong block")
        s1 = dna_strip(MINI_PAIRS, block_w=0.44, block_h=0.38, gap_x=0.06, gap_y=0.06,
                       top_colors=[BLUE]*5, bot_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                       size=24, damage_idx=2).move_to([-1.75, 0.45, 0])
        s1.top_blocks[2][0].set_stroke(RED, width=3.5)
        s1.bot_blocks[2][1].become(M("T", size=24, color=YELLOW, weight=BOLD).move_to(s1.bot_blocks[2]))
        tok_in = Dot([-3.55, 0.45, 0], radius=0.14, color=BLUE, stroke_color=RED, stroke_width=3.0)
        self.play(tok_in.animate.move_to([-1.75, 0.45, 0]), run_time=0.75)
        mismatch_lbl = T("lesion + mismatch", size=26, color=YELLOW).next_to(c1_st.bot_jaw, DOWN, buff=0.20)
        self.play(FadeOut(tok_in, run_time=0.15), FadeIn(s1), FadeIn(mismatch_lbl), run_time=0.75)

        self.at("At the next copy")
        c2_st = open_station("copy 2", center=[1.45, 0.45, 0], width=2.55, height=1.65, color=TEXT, label_pos="top", size=26)
        arr_12 = Arrow(c1_st.right_port + RIGHT * 0.06, c2_st.left_port + LEFT * 0.06, color=TEXT, stroke_width=4.5, buff=0.0)
        split_top = smooth_branch([0.35, 0.55, 0], [2.73, 0.80, 0], color=RED, width=4.5, opacity=0.80)
        split_bot = smooth_branch([0.35, 0.35, 0], [2.73, 0.10, 0], color=YELLOW, width=5.5, opacity=1.0)
        up_branch = smooth_branch([2.73, 0.80, 0], [3.55, 1.95, 0], color=RED, width=4.5, opacity=0.70)
        dn_branch = smooth_branch([2.73, 0.10, 0], [3.50, -0.95, 0], color=YELLOW, width=5.5, opacity=1.0)
        unzip_dot = Dot([0.35, 0.45, 0], radius=0.11, color=GOLD)
        self.play(Create(arr_12), FadeIn(c2_st), FadeIn(unzip_dot), run_time=0.60)
        self.play(Create(split_top), Create(split_bot), unzip_dot.animate.move_to([2.73, 0.45, 0]), run_time=0.70)
        self.play(FadeOut(unzip_dot, run_time=0.15), Create(up_branch), Create(dn_branch), run_time=0.60)

        self.at("templates a full")
        s_yel = dna_strip(CHANGED_MINI, block_w=0.44, block_h=0.38, gap_x=0.06, gap_y=0.06,
                          top_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                          bot_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                          size=24).move_to([4.85, -0.95, 0])
        l_yel = fit_text("stable base-pair change", max_w=2.45, size=24, color=YELLOW, max_lines=2).next_to(s_yel, UP, buff=0.20)
        tok_y = Dot([2.73, 0.10, 0], radius=0.14, color=YELLOW, stroke_color=TEXT, stroke_width=2.5)
        self.play(MoveAlongPath(tok_y, dn_branch), run_time=0.7)
        self.play(FadeOut(tok_y, run_time=0.2), FadeIn(s_yel), FadeIn(l_yel), run_time=0.9)

        self.at("The damaged strand")
        # Dim block borders/fill only; keep letters at full opacity for crisp contrast
        s_dmg = dna_strip(MINI_PAIRS, block_w=0.44, block_h=0.38, gap_x=0.06, gap_y=0.06,
                          size=24, damage_idx=2, fill_opacity=0.10, stroke_opacity=0.55).move_to([4.85, 1.95, 0])
        s_dmg.top_blocks[2][0].set_stroke(RED, width=3.0, opacity=0.65)
        tok_r = Dot([2.73, 0.80, 0], radius=0.14, color=RED, stroke_color=TEXT, stroke_width=2.5)
        self.play(MoveAlongPath(tok_r, up_branch), run_time=0.7)
        self.play(FadeOut(tok_r, run_time=0.2), FadeIn(s_dmg), run_time=0.8)

        self.at("repair or bypass")
        l_rep = T("repair or bypass", size=26, color=TEXT).next_to(s_dmg, UP, buff=0.18)
        self.play(FadeIn(l_rep), run_time=1.0)

        self.at("In the changed lineage")
        crit = criterion_bracket(width=4.2, height=1.00, status="closed", center=(3.15, -2.55, 0))
        box_y = SurroundingRectangle(s_yel.cols[2], color=YELLOW, stroke_width=3.5, buff=0.08)
        self.play(Create(box_y), FadeIn(crit), run_time=1.5)
        self.finish()


class S09Sources(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        # Carried conveyor below the two entrances
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.85))
        conv = animated_conveyor(phase, x0=-5.8, x1=5.8, y=-1.10, spacing=0.85)
        self.add(phase, conv)

        spont_tag = T("spontaneous", size=30, color=TEXT, weight=BOLD).move_to([-4.1, 2.85, 0])
        spont_card = boxed_label("cell chemistry + copying", color=TEXT, size=28, pad=0.24, fill_opacity=0.22).move_to([-4.1, 1.95, 0])

        ind_tag = T("induced", size=30, color=RED, weight=BOLD).move_to([4.1, 2.85, 0])
        ind_card = boxed_label("outside agents", color=RED, size=28, pad=0.24, fill_opacity=0.28).move_to([4.1, 1.95, 0])
        # Non-overlapping L-shaped shadow edge behind ind_card to indicate multiple outside agents
        c_ur = ind_card.get_corner(UR)
        c_dr = ind_card.get_corner(DR)
        c_ul = ind_card.get_corner(UL)
        ind_stack = VMobject(stroke_color=RED, stroke_width=3.0).set_points_as_corners([
            c_ul + [0.14, 0.14, 0], c_ur + [0.14, 0.14, 0], c_dr + [0.14, 0.14, 0],
        ])

        ent_copy = boxed_label("copying error", color=YELLOW, size=28, pad=0.24, fill_opacity=0.24).move_to([-2.4, -0.25, 0])
        ent_dmg = boxed_label("DNA damage", color=RED, size=28, pad=0.24, fill_opacity=0.24).move_to([2.4, -0.25, 0])

        gate = boxed_label("heritable sequence change?", color=TEXT, size=28, pad=0.26, fill_opacity=0.22).move_to([-0.2, -2.35, 0])

        a_sc = Arrow(spont_card.get_bottom() + DOWN * 0.08, ent_copy.get_top() + UP * 0.08 + LEFT * 0.4,
                     color=TEXT, stroke_width=5.5, buff=0.0)
        a_sd = Arrow(spont_card.get_bottom() + DOWN * 0.08 + RIGHT * 0.6, ent_dmg.get_top() + UP * 0.08 + LEFT * 0.5,
                     color=TEXT, stroke_width=5.5, buff=0.0)
        a_ic = Arrow(ind_card.get_bottom() + DOWN * 0.08 + LEFT * 0.6, ent_copy.get_top() + UP * 0.08 + RIGHT * 0.5,
                     color=RED, stroke_width=5.5, buff=0.0)
        a_id = Arrow(ind_card.get_bottom() + DOWN * 0.08, ent_dmg.get_top() + UP * 0.08 + RIGHT * 0.4,
                     color=RED, stroke_width=5.5, buff=0.0)
        a_cg = Arrow(ent_copy.get_bottom() + DOWN * 0.08, gate.get_top() + UP * 0.08 + LEFT * 0.8,
                     color=YELLOW, stroke_width=6.0, buff=0.0)
        a_dg = Arrow(ent_dmg.get_bottom() + DOWN * 0.08, gate.get_top() + UP * 0.08 + RIGHT * 0.8,
                     color=RED, stroke_width=6.0, buff=0.0)

        def _pill(color):
            return RoundedRectangle(corner_radius=0.10, width=0.50, height=0.28,
                                    stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.65)

        self.play(FadeIn(ent_copy), FadeIn(ent_dmg), run_time=1.0)
        self.play(FadeIn(spont_card), Create(a_sc), Create(a_sd), run_time=1.8)

        self.at("spontaneous mutations")
        self.play(FadeIn(spont_tag), run_time=0.6)
        for _ in range(2):
            d1 = _pill(TEXT).move_to(a_sc.point_from_proportion(0.18))
            d2 = _pill(TEXT).move_to(a_sd.point_from_proportion(0.18))
            self.play(d1.animate.move_to(a_sc.point_from_proportion(0.80)), d2.animate.move_to(a_sd.point_from_proportion(0.80)), run_time=1.4, rate_func=linear)
            self.play(FadeOut(d1), FadeOut(d2), run_time=0.2)

        self.at("Outside agents")
        self.play(Create(ind_stack), FadeIn(ind_card), FadeIn(ind_tag), Create(a_ic), Create(a_id), run_time=1.15)
        for _ in range(2):
            r1 = _pill(RED).move_to(a_ic.point_from_proportion(0.18))
            r2 = _pill(RED).move_to(a_id.point_from_proportion(0.18))
            self.play(r1.animate.move_to(a_ic.point_from_proportion(0.80)), r2.animate.move_to(a_id.point_from_proportion(0.80)), run_time=1.3, rate_func=linear)
            self.play(FadeOut(r1), FadeOut(r2), run_time=0.2)

        self.at("Both routes end")
        self.play(FadeIn(gate), Create(a_cg), Create(a_dg), run_time=1.4)

        self.at("A change becomes a mutation")
        for _ in range(2):
            t_c = _pill(YELLOW).move_to(a_cg.point_from_proportion(0.20))
            t_d = _pill(RED).move_to(a_dg.point_from_proportion(0.20))
            self.play(t_c.animate.move_to(a_cg.point_from_proportion(0.78)), t_d.animate.move_to(a_dg.point_from_proportion(0.78)), run_time=1.3, rate_func=linear)
            self.play(FadeOut(t_c), FadeOut(t_d), run_time=0.2)

        self.at("leaves a heritable")
        out_blk = dna_block("A", YELLOW, w=0.68, h=0.52, size=26).move_to([4.6, -2.35, 0])
        out_arr = Arrow(gate.get_right() + RIGHT * 0.10, out_blk.get_left() + LEFT * 0.10,
                        color=YELLOW, stroke_width=5.5, buff=0.0)
        self.play(gate.box.animate.set_stroke(YELLOW, width=4.5), Create(out_arr), FadeIn(out_blk), run_time=1.3)
        self.finish()


class S10Consequences(SpokenScene):
    def construct(self):
        tag = scope_tag("possible outcomes, schematic", size=24, color=TEXT)
        self.add(tag)

        strip = dna_strip(CHANGED_MINI, block_w=0.52, block_h=0.42, gap_x=0.07, gap_y=0.07,
                          top_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                          bot_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                          size=25).move_to([-4.6, 0.15, 0])
        seq_lbl = fit_text("inherited sequence change", max_w=3.2, size=26, color=YELLOW, max_lines=2).next_to(strip, DOWN, buff=0.22)

        board = RoundedRectangle(
            corner_radius=0.18, width=7.3, height=5.0,
            stroke_color=TEXT, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.16,
        ).move_to([2.35, 0.15, 0])
        board_lbl = T("effect on protein", size=30, color=TEXT, weight=BOLD).next_to(board, UP, buff=0.16)

        self.play(FadeIn(strip), FadeIn(seq_lbl), FadeIn(board), FadeIn(board_lbl), run_time=0.95)
        self.play(strip.animate.shift(RIGHT * 0.35), seq_lbl.animate.shift(RIGHT * 0.35), run_time=0.75)

        anch = [-0.65, 0.15, 0]
        b1 = smooth_branch(anch, [1.05, 1.65, 0], color=TEXT, width=7.0)
        b2 = smooth_branch(anch, [1.05, 0.15, 0], color=TEXT, width=7.0)
        b3 = smooth_branch(anch, [1.05, -1.35, 0], color=TEXT, width=2.6)  # noticeably thinner

        l1 = T("no effect", size=28, color=TEXT).move_to([1.30, 1.65, 0], aligned_edge=LEFT)
        l2 = T("reduced or lost function", size=28, color=TEXT).move_to([1.30, 0.15, 0], aligned_edge=LEFT)
        l3 = fit_text("changed or gained function (occasional)", max_w=4.2, size=26, color=TEXT, max_lines=2).move_to([1.30, -1.35, 0], aligned_edge=LEFT)

        self.at("from none")
        self.play(Create(b1), FadeIn(l1), run_time=0.55)

        self.at("loss of function")
        self.play(Create(b2), FadeIn(l2), run_time=0.80)

        self.at("and occasionally")
        self.play(Create(b3), FadeIn(l3), run_time=1.8)
        dots = VGroup(*[Dot(anch, radius=0.09, color=YELLOW) for _ in (b1, b2, b3)])
        self.play(
            MoveAlongPath(dots[0], b1),
            MoveAlongPath(dots[1], b2),
            MoveAlongPath(dots[2], b3),
            run_time=1.8,
        )
        self.play(FadeOut(dots), run_time=0.25)

        self.at("Those consequences")
        # Fold the branches back into the single YELLOW sequence block, separating consequence from origin
        yel_block = dna_block("A", YELLOW, w=0.86, h=0.68, size=30).move_to([1.45, 0.15, 0])
        self.play(
            FadeOut(l1), FadeOut(l2), FadeOut(l3),
            FadeOut(board), FadeOut(board_lbl),
            strip.animate.shift(RIGHT * 2.8),
            seq_lbl.animate.shift(RIGHT * 2.8),
            ReplacementTransform(VGroup(b1, b2, b3), yel_block),
            run_time=1.55,
        )

        self.at("inherited sequence change")
        hl = SurroundingRectangle(strip.cols[2], color=YELLOW, stroke_width=3.5, buff=0.08)
        self.play(Create(hl), run_time=1.1)
        self.finish()


class S11SelectionLink(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        tube = RoundedRectangle(
            corner_radius=0.55, width=6.8, height=4.0,
            stroke_color=TEXT, stroke_width=4.0, fill_color=BLUE, fill_opacity=0.11,
        ).move_to([-1.6, 0.25, 0])
        tube_lbl = T("culture tube", size=28, color=TEXT).next_to(tube, UP, buff=0.16)
        gate = Line([2.15, -1.65, 0], [2.15, 2.15, 0], color=TEXT, stroke_width=8.0)
        gate_lbl = T("closed gate", size=26, color=TEXT).next_to(gate, UP, buff=0.16)

        blue_cells = VGroup(*[
            RoundedRectangle(corner_radius=0.15, width=0.62, height=0.30, stroke_color=BLUE,
                             stroke_width=3.0, fill_color=BLUE, fill_opacity=0.38).move_to(p)
            for p in [[-4.1, 1.35, 0], [-3.8, -0.95, 0], [-2.4, 1.45, 0], [-1.8, -1.10, 0],
                      [-0.2, 1.35, 0], [0.5, -0.95, 0], [0.8, 0.35, 0], [1.1, 1.40, 0]]
        ])

        y_strip = dna_strip(CHANGED_MINI, block_w=0.46, block_h=0.38, gap_x=0.07, gap_y=0.07,
                            top_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                            bot_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                            size=24).move_to([-3.3, 0.25, 0])
        y0 = RoundedRectangle(corner_radius=0.18, width=0.68, height=0.32, stroke_color=YELLOW,
                              stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.52).move_to([-3.3, 0.25, 0])

        self.play(FadeIn(tube), FadeIn(tube_lbl), FadeIn(gate), FadeIn(gate_lbl), FadeIn(blue_cells), FadeIn(y_strip), run_time=0.70)
        self.play(ReplacementTransform(y_strip, y0), run_time=0.50)

        self.at("variant exists")
        y1 = y0.copy().move_to([-2.3, 0.65, 0])
        y2 = y0.copy().move_to([-2.3, -0.25, 0])
        y3 = y0.copy().move_to([-0.8, 0.85, 0])
        y4 = y0.copy().move_to([-0.8, -0.45, 0])
        fam_lines = VGroup(
            Line(y0.get_right(), y1.get_left(), color=YELLOW, stroke_width=3.5),
            Line(y0.get_right(), y2.get_left(), color=YELLOW, stroke_width=3.5),
            Line(y1.get_right(), y3.get_left(), color=YELLOW, stroke_width=3.5),
            Line(y2.get_right(), y4.get_left(), color=YELLOW, stroke_width=3.5),
        )
        self.play(Create(fam_lines[:2]), TransformFromCopy(y0, y1), TransformFromCopy(y0, y2), run_time=1.6)
        self.play(Create(fam_lines[2:]), TransformFromCopy(y1, y3), TransformFromCopy(y2, y4), run_time=1.6)

        self.at("The first film followed")
        phages = VGroup(*[
            make_phage_icon(scale=1.0).move_to(pos)
            for pos in [[3.4, 1.35, 0], [4.5, 0.65, 0], [3.6, -0.20, 0], [4.8, -1.05, 0]]
        ])
        phage_lbl = T("phages", size=28, color=RED, weight=BOLD).move_to([4.1, 2.25, 0])
        self.play(FadeIn(phages, shift=LEFT * 0.3), FadeIn(phage_lbl), run_time=1.5)

        self.at("with phage resistance")
        self.play(phages.animate.shift(LEFT * 0.80), run_time=1.4)
        self.play(phages.animate.shift(RIGHT * 0.25), run_time=0.9)

        self.at("Selection cannot reach backward")
        order_arr = Arrow([-4.8, -2.55, 0], [4.8, -2.55, 0], color=TEXT, stroke_width=5.0, buff=0.0)
        order_lbl = T("origin first, sorting later", size=30, color=TEXT, weight=BOLD).next_to(order_arr, DOWN, buff=0.14)
        self.play(Create(order_arr), run_time=2.0)
        self.play(FadeIn(order_lbl), run_time=0.8)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        world = build_fork_world(dim_paths=False, show_outcomes=False)
        strip = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                          size=24, damage_idx=2).move_to([-4.35, 0.0, 0])
        strip.top_blocks[2][0].set_stroke(RED, width=3.5)

        self.play(FadeIn(world), FadeIn(strip), run_time=1.1)

        self.at("when repair or copying")
        # Two copies of the RED lesion travel simultaneously down the upper and lower Bezier paths
        b_top = strip.badge.copy()
        b_bot = strip.badge.copy()
        self.add(b_top, b_bot)
        self.play(
            b_top.animate.move_to(world.junc.get_center()),
            b_bot.animate.move_to(world.junc.get_center()),
            run_time=0.6,
        )
        self.play(
            MoveAlongPath(b_top, world.up_in),
            MoveAlongPath(b_bot, world.dn_in),
            run_time=1.5,
        )
        s_rep_in = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07, size=24).move_to([0.25, 1.80, 0])
        s_copy_in = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07, size=24).move_to([0.25, -1.00, 0])
        self.play(
            FadeIn(s_rep_in), FadeIn(s_copy_in),
            b_top.animate.next_to(s_rep_in.top_blocks[2], UP, buff=0.08),
            b_bot.animate.next_to(s_copy_in.top_blocks[2], UP, buff=0.08),
            run_time=0.6,
        )

        self.at("Repair can erase")
        self.play(FadeOut(b_top, shift=UP * 0.25), run_time=0.5)
        s_blue = dna_strip(MINI_PAIRS, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07, size=24).move_to([4.35, 1.80, 0])
        arr_r = Arrow([1.65, 1.80, 0], s_blue.get_left() + LEFT * 0.12, color=GREEN, stroke_width=4.5, buff=0.0)
        self.play(Create(arr_r), FadeIn(s_blue), run_time=1.0)

        self.at("The inherited sequence")
        self.play(FadeOut(b_bot, shift=UP * 0.20), run_time=0.4)
        d_y1 = dna_strip(CHANGED_MINI, block_w=0.50, block_h=0.40, gap_x=0.07, gap_y=0.07,
                         top_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                         bot_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE], size=24).move_to([4.35, -0.25, 0])
        d_y2 = d_y1.copy().move_to([4.35, -2.05, 0])
        arr_y1 = Arrow([1.65, -0.95, 0], d_y1.get_left() + LEFT * 0.12, color=YELLOW, stroke_width=4.5, buff=0.0)
        arr_y2 = Arrow([1.65, -1.05, 0], d_y2.get_left() + LEFT * 0.12, color=YELLOW, stroke_width=4.5, buff=0.0)
        self.play(Create(arr_y1), Create(arr_y2), FadeIn(d_y1), FadeIn(d_y2), run_time=2.2)

        self.at("A red mark alone")
        hero = dna_strip(CHANGED_MINI, block_w=0.82, block_h=0.62, gap_x=0.14, gap_y=0.14,
                         top_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                         bot_colors=[BLUE, BLUE, YELLOW, BLUE, BLUE],
                         size=28).move_to([0, 0.35, 0])
        hero_box = SurroundingRectangle(hero.cols[2], color=YELLOW, stroke_width=4.5, buff=0.12)
        hero_lbl = T("inherited sequence change", size=34, color=YELLOW, weight=BOLD).next_to(hero, DOWN, buff=0.35)
        self.play(
            FadeOut(world), FadeOut(strip), FadeOut(s_rep_in), FadeOut(s_copy_in),
            FadeOut(arr_r), FadeOut(arr_y1), FadeOut(arr_y2),
            FadeOut(s_blue), FadeOut(d_y2),
            run_time=0.6,
        )
        self.play(ReplacementTransform(d_y1.cols, hero.cols), run_time=1.4)
        self.play(Create(hero_box), FadeIn(hero_lbl), run_time=1.2)
        self.finish()


class S13TextBridge(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)

        world = build_fork_world(dim_paths=False, show_outcomes=False, gate_label_size=32).scale(0.75).move_to([-0.85, 0.0, 0])
        world.entry_rail.set_opacity(0.0)
        h_spont = T("spontaneous sources", size=28, color=TEXT, weight=BOLD).move_to([-4.6, 2.50, 0])
        h_ind = T("induced sources", size=28, color=RED, weight=BOLD).move_to([-4.6, -2.50, 0])

        self.play(FadeIn(world), FadeIn(h_spont), FadeIn(h_ind), run_time=0.95)

        self.at("names the specific sources")
        j_pt = world.junc.get_center()
        sp0 = RoundedRectangle(corner_radius=0.08, width=0.66, height=0.38, stroke_color=TEXT, stroke_width=3.0,
                               fill_color=TEXT, fill_opacity=0.28).move_to([-4.2, 1.55, 0])
        sp1 = sp0.copy().move_to([-5.1, 1.55, 0])
        in0 = RoundedRectangle(corner_radius=0.08, width=0.66, height=0.38, stroke_color=RED, stroke_width=3.0,
                               fill_color=RED, fill_opacity=0.38).move_to([-4.2, -1.55, 0])
        in1 = in0.copy().move_to([-5.1, -1.55, 0])

        self.play(FadeIn(sp0), FadeIn(sp1), FadeIn(in0), FadeIn(in1), run_time=0.40)
        # Stagger arrival cleanly so spontaneous and induced tokens never collide at the junction
        self.play(
            sp0.animate.move_to(world.up_in.get_start()),
            sp1.animate.move_to([-4.2, 1.55, 0]),
            in0.animate.move_to([-3.2, -1.00, 0]),
            in1.animate.move_to([-4.2, -1.55, 0]),
            run_time=0.80,
        )
        self.play(
            MoveAlongPath(sp0, world.up_in),
            in0.animate.move_to(world.dn_in.get_start()),
            run_time=1.05,
        )
        self.play(
            sp0.animate.set_color(GREEN).move_to(world.up_out.get_end()),
            MoveAlongPath(in0, world.dn_in),
            run_time=0.90,
        )

        self.at("Then the Ames test")
        plate_outer = Circle(radius=1.60, color=TEXT, stroke_width=4.0, fill_color=BLUE, fill_opacity=0.15).move_to([4.55, 0.0, 0])
        plate_inner = Circle(radius=1.45, color=TEXT, stroke_width=2.0).move_to([4.55, 0.0, 0])
        plate_lbl = T("bacteria on plates", size=26, color=TEXT).next_to(plate_outer, UP, buff=0.18)
        rods = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.38, height=0.18, stroke_color=BLUE,
                             stroke_width=2.5, fill_color=BLUE, fill_opacity=0.42).move_to(plate_outer.get_center() + p)
            for p in [[-0.85, 0.65, 0], [0.85, 0.65, 0], [-0.95, -0.45, 0], [0.85, -0.55, 0], [0.0, 0.95, 0]]
        ])
        plate_q = T("?", size=58, color=GOLD, weight=BOLD).move_to(plate_outer)
        flow_plate = Arrow(world.bot_out.get_end() + RIGHT * 0.08, [3.00, -0.70, 0],
                           color=YELLOW, stroke_width=5.0, buff=0.0)
        mut_rod_0 = RoundedRectangle(corner_radius=0.09, width=0.38, height=0.18, stroke_color=YELLOW,
                                     stroke_width=3.0, fill_color=YELLOW, fill_opacity=0.55).move_to(plate_outer.get_center() + [-0.40, -0.85, 0])
        mut_rod_1 = mut_rod_0.copy().move_to(plate_outer.get_center() + [0.40, -0.85, 0])
        self.play(
            FadeIn(plate_outer), FadeIn(plate_inner), FadeIn(plate_lbl), FadeIn(rods), FadeIn(plate_q),
            Create(flow_plate),
            FadeOut(sp0),
            in0.animate.set_color(YELLOW).move_to(world.bot_out.get_end()),
            sp1.animate.move_to(world.up_in.get_start()),
            run_time=1.6,
        )
        self.play(
            ReplacementTransform(in0, mut_rod_0),
            MoveAlongPath(sp1, world.up_in),
            in1.animate.move_to(world.dn_in.get_start()),
            run_time=1.6,
        )
        self.play(
            sp1.animate.set_color(GREEN).move_to(world.up_out.get_end()),
            MoveAlongPath(in1, world.dn_in),
            plate_q.animate.scale(1.15),
            run_time=1.6,
        )

        self.at("Those details belong")
        self.play(
            FadeOut(sp1),
            in1.animate.set_color(YELLOW).move_to(world.bot_out.get_end()),
            run_time=1.1,
        )
        self.play(
            ReplacementTransform(in1, mut_rod_1),
            plate_q.animate.scale(1.0 / 1.15),
            run_time=1.1,
        )
        self.finish()


class S14End(EndCard):
    LINE = "Damage becomes mutation when repair or copying leaves a heritable sequence change."
