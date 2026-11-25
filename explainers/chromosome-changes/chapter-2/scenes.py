"""Break, Rejoin, Segregate — Chromosome Number and Structure (Chapter 2)

COLOUR MAP (identical to Chapter 1):
- BLUE  (#58C4DD): one homologue (normal chromosome blocks A-E)
- GOLD  (#D4A843): the other homologue (normal partner blocks A-E)
- TEAL  (#3FB8C0): a segment or division currently moving (translocated end D-E, active path token)
- GREEN (#83C167): balanced chromosome dose, alternate segregation, balanced gamete ledgers
- RED   (#FC6255): extra or missing dose, failed/adjacent segregation, unbalanced gamete ledgers
- GREY  (#8B93A1): nonhomologous chromosome (blocks 1-5), spindle fibres, carrier cell context
- TEXT  (#E8EAF0): block letters, labels, brackets, titles

CARRIED WORLD:
Block chromosomes (blue A-E, gold A-E, grey 1-5) paired with a live ValueTracker-driven
DoseGauge (MISSING - BALANCED - EXTRA) and breakpoint/spindle attachments, carried from the
opening break through deletion/duplication, inversion loop, reciprocal translocation, gene
context, four-way cross segregation, carrier paradox, and the three-part causal path.

SCENE CHANGES (what changes and what computes it):
- s00_hook:      Whole blue/gold homologues split into blocks A-E; blue breaks at C|D while DoseGauge stays at v=0 (BALANCED); fragments hold aligned with subtle 0.03 drift.
- s01_title:     Standard TitleCard for "Break, Rejoin, Segregate".
- s02_questions: Blue chromosome A-E enlarges to fill frame; gene ticks appear; checklist (DOSE, CONTEXT, MEIOSIS) lights up as DoseGauge, breakpoint bracket, and spindle fibres grow directly from the chromosome.
- s03_dose_changes: Block C lifts out and gap closes (A-B-D-E), DoseGauge ValueTracker moves smoothly from 0 to -1 (MISSING, RED); restores to 0, then C duplicates and inserts (A-B-C-C-D-E) as tracker moves from 0 to +1 (EXTRA, RED).
- s04_inversion: Blocks B-C-D lift, invert to D-C-B with upright letters, and reinsert; DoseGauge stays at 0 (GREEN); gold homologue enters and both bend along computed parametric loop curves so A-E align face-to-face.
- s05_exchange:  Chromosomes stand vertically beside grey 1-5; both break at matching height; blue D-E turns TEAL and swaps onto grey while grey 4-5 moves onto blue; DoseGauge stays level at 0; white brackets pulse at the two new junctions.
- s06_context:   Zooms into breakpoint on a generic GENE block splitting it ("can"), then shows half GENE A beside half GENE B ("can"), with DoseGauge at 0 (GREEN) and chromosome count held at 2.
- s07_pairing:   Zooms out to 4-chromosome cross (NW blue, NE t(B;G), SE grey, SW t(G;B)) with zero crossings, opening 2 large gamete zones (left and right) and thin grey spindle fibres from opposite poles.
- s08_predict:   Overlays green opposite dashed arrows and red neighbouring dashed arrows on the cross, puts ? in each gamete zone, and shows empty ledger frames + question card.
- s09_pause:     PredictPause (4.5s) holding cross, both arrow choices, question card, subtle spindle motion, and 4.5s countdown ring.
- s10_reveal:    Green opposite arrows animate NW+SE stacked in left gamete zone and NE+SW stacked in right gamete zone with green balanced ledgers (1 copy each); resets cross completely; red neighbouring arrows animate NW+SW stacked left and NE+SE stacked right with red unbalanced ledgers (D-E x2 / 4-5 x0 and reverse).
- s11_carrier:   Returns balanced carrier set to top centre with green balanced ledger and "outcomes can differ" beside breakpoint; fans out alternate (green) and adjacent (red) gamete ledgers below.
- s12_rule:      Transforms DoseGauge, breakpoint bracket, and cross into a horizontal causal path (BREAK -> DNA DOSE -> GENE CONTEXT -> MEIOTIC BALANCE) under the carrier ledger; teal segment travels step by step through each stage.
- s13_end:       Standard EndCard with the exact take-home line.
"""

from bp_parts import *


# ------------------------------------------------------------------ shared builders
def make_block(label, color, w=1.08, h=0.86, font_size=30, stroke_w=4.0):
    """One chromosome segment block with high-contrast upright label."""
    rect = RoundedRectangle(
        corner_radius=0.1,
        width=w,
        height=h,
        stroke_color=color,
        stroke_width=stroke_w,
        fill_color=color,
        fill_opacity=0.34,
    )
    txt = T(label, size=font_size, color=TEXT, weight=BOLD).move_to(rect)
    g = VGroup(rect, txt)
    g.box = rect
    g.label = txt
    g.seg_color = color
    return g


def make_chrom(labels, colors, horizontal=True, w=1.08, h=0.86, gap=0.06, font_size=30, centromere_after=None):
    """Build a linear block chromosome from parallel lists of labels and colours."""
    if isinstance(colors, str):
        colors = [colors] * len(labels)
    blocks = VGroup(*[make_block(lb, col, w=w, h=h, font_size=font_size) for lb, col in zip(labels, colors)])
    direction = RIGHT if horizontal else DOWN
    blocks.arrange(direction, buff=gap)
    g = VGroup(blocks)
    g.blocks = blocks
    g.centromere = None
    if centromere_after is not None and 0 <= centromere_after < len(blocks) - 1:
        a, b = blocks[centromere_after], blocks[centromere_after + 1]
        mid = (a.get_center() + b.get_center()) / 2
        c_dot = Circle(radius=0.11, color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(mid)
        c_dot.set_z_index(3)
        g.add(c_dot)
        g.centromere = c_dot
    return g


class DoseGauge(VGroup):
    """Computed dose gauge driven by a ValueTracker in [-1, +1] (0 = BALANCED, -1 = MISSING, +1 = EXTRA)."""

    def __init__(self, tracker, center=(0, -1.8, 0), width=4.0, title="TOTAL DOSE"):
        super().__init__()
        self.tracker = tracker
        width = max(width, 4.0)
        cx, cy = center[0], center[1]
        half = width / 2.0

        track = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=0.22,
            stroke_color=GREY,
            stroke_width=2.2,
            fill_color=GREY,
            fill_opacity=0.18,
        ).move_to([cx, cy, 0])
        mid_tick = Line([cx, cy - 0.18, 0], [cx, cy + 0.18, 0], color=TEXT, stroke_width=2.5)

        def _col():
            return GREEN if abs(tracker.get_value()) < 0.15 else RED

        def _fill():
            v = float(np.clip(tracker.get_value(), -1.0, 1.0))
            if abs(v) < 0.03:
                return RoundedRectangle(
                    corner_radius=0.06, width=0.26, height=0.18,
                    stroke_width=0, fill_color=GREEN, fill_opacity=0.85
                ).move_to([cx, cy, 0])
            w_bar = max(0.08, abs(v) * half)
            x_bar = cx + (w_bar / 2.0 if v > 0 else -w_bar / 2.0)
            return RoundedRectangle(
                corner_radius=0.06, width=w_bar, height=0.18,
                stroke_width=0, fill_color=_col(), fill_opacity=0.85
            ).move_to([x_bar, cy, 0])

        def _needle():
            v = float(np.clip(tracker.get_value(), -1.0, 1.0))
            x_n = cx + v * half
            return Dot([x_n, cy, 0], radius=0.15, color=TEXT, stroke_color=_col(), stroke_width=4)

        def _status():
            v = tracker.get_value()
            if abs(v) < 0.15:
                word, col = "BALANCED", GREEN
            elif v < 0:
                word, col = "MISSING", RED
            else:
                word, col = "EXTRA", RED
            return T(f"{title}: {word}", size=26, color=col, weight=BOLD).move_to([cx, cy + 0.56, 0])

        lab_l = T("MISSING", size=24, color=GREY).move_to([cx - half, cy - 0.45, 0], aligned_edge=LEFT)
        lab_c = T("LEVEL", size=24, color=GREY).move_to([cx, cy - 0.45, 0])
        lab_r = T("EXTRA", size=24, color=GREY).move_to([cx + half, cy - 0.45, 0], aligned_edge=RIGHT)

        self.fill_bar = always_redraw(_fill)
        self.needle = always_redraw(_needle)
        self.status = always_redraw(_status)
        self.add(track, mid_tick, self.fill_bar, self.needle, self.status, lab_l, lab_c, lab_r)


def make_cross_arm(labels, colors, coords, block_size=(0.56, 0.50), font_size=24):
    """Build a bent or straight chromosome along explicit (x, y) block centres with edge-only connectors."""
    if isinstance(colors, str):
        colors = [colors] * len(labels)
    bw, bh = block_size
    blocks = VGroup()
    for lb, col, (x, y) in zip(labels, colors, coords):
        b = make_block(lb, col, w=bw, h=bh, font_size=font_size, stroke_w=3.0).move_to([x, y, 0])
        blocks.add(b)
    # Connect adjacent blocks strictly from edge to edge (never across letters or boxes)
    connectors = VGroup()
    for i in range(len(blocks) - 1):
        p1 = blocks[i].get_center()
        p2 = blocks[i + 1].get_center()
        dv = p2 - p1
        dx, dy = abs(dv[0]), abs(dv[1])
        if dx < 0.05:
            # Vertical neighbours
            sgn = 1.0 if p2[1] > p1[1] else -1.0
            a = p1 + UP * sgn * (bh / 2.0 + 0.01)
            b_pt = p2 - UP * sgn * (bh / 2.0 + 0.01)
            connectors.add(Line(a, b_pt, color=colors[i], stroke_width=3.5))
        elif dy < 0.05:
            # Horizontal neighbours
            sgn = 1.0 if p2[0] > p1[0] else -1.0
            a = p1 + RIGHT * sgn * (bw / 2.0 + 0.01)
            b_pt = p2 - RIGHT * sgn * (bw / 2.0 + 0.01)
            connectors.add(Line(a, b_pt, color=colors[i], stroke_width=3.5))
        else:
            # Corner between block 2 and block 3
            sx = 1.0 if p2[0] > p1[0] else -1.0
            sy = 1.0 if p2[1] > p1[1] else -1.0
            a = p1 + RIGHT * sx * (bw / 2.0 + 0.01)
            if abs(p2[1] - p1[1]) <= bh / 2.0 + 0.06:
                b_pt = p2 - RIGHT * sx * (bw / 2.0 + 0.01)
                connectors.add(Line(a, b_pt, color=colors[i], stroke_width=3.5))
            else:
                b_pt = p2 - UP * sy * (bh / 2.0 + 0.01)
                corner = np.array([b_pt[0], a[1], 0.0])
                elbow = VMobject(stroke_color=colors[i], stroke_width=3.5)
                elbow.set_points_as_corners([a, corner, b_pt])
                connectors.add(elbow)
    g = VGroup(connectors, blocks)
    g.connectors = connectors
    g.blocks = blocks
    return g


def build_translocation_cross(center=(0.0, 0.45), step=0.65, arm_gap=0.56, block_size=(0.56, 0.50), font_size=24):
    """Build the 4-chromosome translocation cross with zero crossings.

    Quadrants:
      NW: Normal Blue  (A-B-C down North-left, D-E left West-top)
      NE: t(B;G)       (A-B-C down North-right, 4-5 right East-top)
      SE: Normal Grey  (4-5 right East-bottom, 1-2-3 down South-right)
      SW: t(G;B)       (1-2-3 down South-left, D-E teal left West-bottom)
    Returns (group, dict_of_4_chroms).
    """
    cx, cy = center
    d = arm_gap

    nw_coords = [
        (cx - d, cy + 3 * step),  # A
        (cx - d, cy + 2 * step),  # B
        (cx - d, cy + 1 * step),  # C
        (cx - d - step, cy + d),  # D
        (cx - d - 2 * step, cy + d),  # E
    ]
    nw = make_cross_arm(["A", "B", "C", "D", "E"], BLUE, nw_coords, block_size=block_size, font_size=font_size)

    ne_coords = [
        (cx + d, cy + 3 * step),  # A
        (cx + d, cy + 2 * step),  # B
        (cx + d, cy + 1 * step),  # C
        (cx + d + step, cy + d),  # 4
        (cx + d + 2 * step, cy + d),  # 5
    ]
    ne = make_cross_arm(["A", "B", "C", "4", "5"], [BLUE, BLUE, BLUE, GREY, GREY], ne_coords, block_size=block_size, font_size=font_size)

    se_coords = [
        (cx + d, cy - 3 * step),  # 1
        (cx + d, cy - 2 * step),  # 2
        (cx + d, cy - 1 * step),  # 3
        (cx + d + step, cy - d),  # 4
        (cx + d + 2 * step, cy - d),  # 5
    ]
    se = make_cross_arm(["1", "2", "3", "4", "5"], GREY, se_coords, block_size=block_size, font_size=font_size)

    sw_coords = [
        (cx - d, cy - 3 * step),  # 1
        (cx - d, cy - 2 * step),  # 2
        (cx - d, cy - 1 * step),  # 3
        (cx - d - step, cy - d),  # D
        (cx - d - 2 * step, cy - d),  # E
    ]
    sw = make_cross_arm(["1", "2", "3", "D", "E"], [GREY, GREY, GREY, TEAL, TEAL], sw_coords, block_size=block_size, font_size=font_size)

    g = VGroup(nw, ne, se, sw)
    return g, {"NW": nw, "NE": ne, "SE": se, "SW": sw}


def build_gamete_zones(left_x=-4.6, right_x=4.6, y=0.60, r=1.40):
    """Two large dashed gamete zone circles (left gamete, right gamete), sized to hold both co-segregating chromosomes."""
    zones = {}
    specs = [
        ("L", left_x, y),
        ("R", right_x, y),
    ]
    g = VGroup()
    for key, x, cy in specs:
        c = DashedVMobject(
            Circle(radius=r, color=GREY, stroke_width=2.5),
            num_dashes=24,
            dashed_ratio=0.55,
        ).move_to([x, cy, 0])
        zones[key] = c
        g.add(c)
    return g, zones


def build_spindle_fibres(cross_dict, left_pole=(-5.95, 0.38, 0), right_pole=(5.95, 0.38, 0)):
    """Thin grey curved spindle fibres from opposite poles arcing cleanly around arms to centromeres."""
    lp = np.array(left_pole, dtype=float)
    rp = np.array(right_pole, dtype=float)
    f_nw = ArcBetweenPoints(lp, cross_dict["NW"].blocks[1].get_left() + LEFT * 0.06, angle=-0.35, color=GREY, stroke_width=2.4).set_stroke(opacity=0.8).set_fill(opacity=0)
    f_sw = ArcBetweenPoints(lp, cross_dict["SW"].blocks[1].get_left() + LEFT * 0.06, angle=0.35, color=GREY, stroke_width=2.4).set_stroke(opacity=0.8).set_fill(opacity=0)
    f_ne = ArcBetweenPoints(rp, cross_dict["NE"].blocks[1].get_right() + RIGHT * 0.06, angle=0.35, color=GREY, stroke_width=2.4).set_stroke(opacity=0.8).set_fill(opacity=0)
    f_se = ArcBetweenPoints(rp, cross_dict["SE"].blocks[1].get_right() + RIGHT * 0.06, angle=-0.35, color=GREY, stroke_width=2.4).set_stroke(opacity=0.8).set_fill(opacity=0)
    pole_l = Dot(lp, radius=0.09, color=GREY)
    pole_r = Dot(rp, radius=0.09, color=GREY)
    return VGroup(pole_l, pole_r, f_nw, f_sw, f_ne, f_se)


def _dashed_double_arrow(p1, p2, color, stroke_width=4.0, arc=0.0):
    """A clean dashed line or arc between p1 and p2 with arrowheads at both ends."""
    d = p2 - p1
    u = d / max(np.linalg.norm(d), 1e-6)
    if abs(arc) < 1e-4:
        shaft = DashedLine(p1 + u * 0.08, p2 - u * 0.08, color=color, stroke_width=stroke_width, dash_length=0.09)
        u1, u2 = -u, u
    else:
        base_arc = ArcBetweenPoints(p1, p2, angle=arc, color=color, stroke_width=stroke_width).set_fill(opacity=0)
        shaft = DashedVMobject(base_arc, num_dashes=10, dashed_ratio=0.55)
        u1 = (base_arc.points[0] - base_arc.points[1])
        u1 = u1 / max(np.linalg.norm(u1), 1e-6)
        u2 = (base_arc.points[-1] - base_arc.points[-2])
        u2 = u2 / max(np.linalg.norm(u2), 1e-6)
    tip1 = Triangle(color=color, fill_color=color, fill_opacity=1.0, stroke_width=0).scale(0.068)
    tip1.rotate(np.arctan2(u1[1], u1[0]) - PI / 2).move_to(p1)
    tip2 = Triangle(color=color, fill_color=color, fill_opacity=1.0, stroke_width=0).scale(0.068)
    tip2.rotate(np.arctan2(u2[1], u2[0]) - PI / 2).move_to(p2)
    return VGroup(shaft, tip1, tip2)


def build_segregation_arrows(cross_dict, opp_color=GREEN, adj_color=RED):
    """Opposite arrows (NW<->SE, NE<->SW) and neighbouring arrows (NW<->SW, NE<->SE)."""
    cx = (cross_dict["NW"].blocks[2].get_center()[0] + cross_dict["NE"].blocks[2].get_center()[0]) / 2.0
    cy = (cross_dict["NW"].blocks[2].get_center()[1] + cross_dict["SW"].blocks[2].get_center()[1]) / 2.0

    # Clean diagonal dashed arrows across the widened open central gap of the cross
    g1 = _dashed_double_arrow(
        np.array([cx - 0.16, cy + 0.28, 0]),
        np.array([cx + 0.16, cy - 0.28, 0]),
        opp_color,
        stroke_width=3.8,
    )
    g2 = _dashed_double_arrow(
        np.array([cx + 0.16, cy + 0.28, 0]),
        np.array([cx - 0.16, cy - 0.28, 0]),
        opp_color,
        stroke_width=3.8,
    )
    green_arrows = VGroup(g1, g2)

    # Curved dashed arrows connect neighbouring outer arms cleanly outside the blocks
    r1 = _dashed_double_arrow(
        cross_dict["NW"].blocks[4].get_left() + LEFT * 0.14,
        cross_dict["SW"].blocks[4].get_left() + LEFT * 0.14,
        adj_color, stroke_width=3.8, arc=0.85,
    )
    r2 = _dashed_double_arrow(
        cross_dict["NE"].blocks[4].get_right() + RIGHT * 0.14,
        cross_dict["SE"].blocks[4].get_right() + RIGHT * 0.14,
        adj_color, stroke_width=3.8, arc=-0.85,
    )
    red_arrows = VGroup(r1, r2)
    return green_arrows, red_arrows


def make_block_ledger(title, rows, color, min_width=3.4, center=(0, 0, 0)):
    """High-contrast Ledger-style card (strokeless dark backing + rule + non-overlapping columns)."""
    head = T(title, size=25, color=color, weight=BOLD)
    row_pairs = [(T(k, size=24, color=TEXT), M(v, size=24, color=vcol)) for k, v, vcol in rows]
    max_k = max(kt.width for kt, _ in row_pairs)
    max_v = max(vt.width for _, vt in row_pairs)
    inner_w = max(min_width - 0.5, head.width + 0.1, max_k + max_v + 0.45)

    row_mobs = VGroup()
    for kt, vt in row_pairs:
        kt.move_to([-inner_w / 2 + kt.width / 2, 0, 0])
        vt.move_to([inner_w / 2 - vt.width / 2, 0, 0])
        row_mobs.add(VGroup(kt, vt))
    row_mobs.arrange(DOWN, buff=0.20)

    rule = Line(LEFT * (inner_w / 2), RIGHT * (inner_w / 2), color=color, stroke_width=2.5)
    content = VGroup(head, rule, row_mobs).arrange(DOWN, buff=0.16)

    # Strokeless backing panel (stroke_width=0 -> never treated as a label's personal box)
    pad_w, pad_h = inner_w + 0.48, content.height + 0.36
    back = RoundedRectangle(
        corner_radius=0.14,
        width=pad_w,
        height=pad_h,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.22,
    )
    content.move_to(back)
    card = VGroup(back, content).move_to(center)
    card.box = back
    return card


# ------------------------------------------------------------------ scenes
class S00Hook(SpokenScene):
    def construct(self):
        self.at("The first film")
        blue_whole = RoundedRectangle(
            corner_radius=0.22, width=5.2, height=0.84, stroke_color=BLUE, stroke_width=4,
            fill_color=BLUE, fill_opacity=0.22,
        ).move_to([-1.9, 1.0, 0])
        gold_whole = RoundedRectangle(
            corner_radius=0.22, width=5.2, height=0.84, stroke_color=GOLD, stroke_width=4,
            fill_color=GOLD, fill_opacity=0.22,
        ).move_to([-1.9, -0.8, 0])
        blue_tag = T("homologue 1", size=26, color=BLUE).next_to(blue_whole, LEFT, buff=0.42)
        gold_tag = T("homologue 2", size=26, color=GOLD).next_to(gold_whole, LEFT, buff=0.42)
        pair_init = VGroup(blue_whole, gold_whole, blue_tag, gold_tag)
        if pair_init.get_left()[0] < -6.2:
            pair_init.shift(RIGHT * (-6.2 - pair_init.get_left()[0]))

        dose_v = ValueTracker(0.0)
        gauge = DoseGauge(dose_v, center=(4.15, 0.1, 0), width=4.0)

        self.play(FadeIn(blue_whole), FadeIn(gold_whole), FadeIn(blue_tag), FadeIn(gold_tag), run_time=0.8)

        blue_blocks = make_chrom(["A", "B", "C", "D", "E"], BLUE, w=0.96, h=0.84, gap=0.06, centromere_after=1)
        blue_blocks.move_to(blue_whole)
        gold_blocks = make_chrom(["A", "B", "C", "D", "E"], GOLD, w=0.96, h=0.84, gap=0.06, centromere_after=1)
        gold_blocks.move_to(gold_whole)

        self.play(
            ReplacementTransform(blue_whole, blue_blocks),
            ReplacementTransform(gold_whole, gold_blocks),
            FadeIn(gauge),
            run_time=1.3,
        )

        self.at("Can a chromosome rearrangement")
        left_frag = VGroup(blue_blocks.blocks[0], blue_blocks.blocks[1], blue_blocks.blocks[2], blue_blocks.centromere)
        right_frag = VGroup(blue_blocks.blocks[3], blue_blocks.blocks[4])

        break_x = (blue_blocks.blocks[2].get_right()[0] + blue_blocks.blocks[3].get_left()[0]) / 2
        break_y = blue_blocks.get_center()[1]
        cut_line = DashedLine([break_x, break_y - 0.62, 0], [break_x, break_y + 0.62, 0], color=TEXT, stroke_width=3.5)

        self.play(Create(cut_line), run_time=0.6)
        self.play(
            left_frag.animate.shift(LEFT * 0.24),
            right_frag.animate.shift(RIGHT * 0.24),
            FadeOut(cut_line),
            run_time=1.1,
        )
        question = fit_text("Can this matter if no DNA is missing?", max_w=7.4, size=30, color=GOLD).move_to(
            [blue_blocks.get_center()[0], 2.55, 0]
        )
        self.play(FadeIn(question, shift=DOWN * 0.12), run_time=0.9)

        bob(left_frag, amp=0.03, speed=2.0, seed=0)
        bob(right_frag, amp=0.03, speed=2.0, seed=1.8)

        self.at("Follow the same colored blocks")
        self.play(
            Indicate(blue_blocks.blocks[3], color=TEAL, scale_factor=1.08),
            Indicate(blue_blocks.blocks[4], color=TEAL, scale_factor=1.08),
            run_time=1.5,
        )
        self.finish()


class S01Title(TitleCard):
    LESSON = "Chromosome Number and Structure: Aneuploidy and Rearrangements"
    TITLE = "Break, Rejoin, Segregate"


class S02Questions(SpokenScene):
    def construct(self):
        self.at("A chromosome is more")
        chrom = make_chrom(["A", "B", "C", "D", "E"], BLUE, w=1.42, h=1.15, gap=0.08, font_size=34, centromere_after=1)
        chrom.move_to([-1.6, 1.35, 0])
        count_chip = boxed_label("count: 1 chromosome", BLUE, size=26).move_to([-1.6, 2.75, 0])

        c_dose = T("dose", size=24, color=GREEN)
        c_ctx = T("context", size=24, color=GOLD)
        c_mei = T("meiosis", size=24, color=TEAL)
        corner_tags = VGroup(c_dose, c_ctx, c_mei).arrange(RIGHT, buff=0.4).move_to([-3.6, -2.95, 0])

        self.play(FadeIn(chrom), FadeIn(count_chip), FadeIn(corner_tags), run_time=1.0)

        self.at("Its blocks carry genes")
        gene_ticks = VGroup()
        for b in chrom.blocks:
            x0 = b.get_center()[0]
            y_bot = b.get_bottom()[1] + 0.12
            for dx in (-0.36, -0.18, 0.18, 0.36):
                gene_ticks.add(Line([x0 + dx, y_bot, 0], [x0 + dx, y_bot + 0.18, 0], color=TEXT, stroke_width=2.2).set_opacity(0.65))
        genes_lab = T("blocks carry genes", size=26, color=TEXT).next_to(chrom, DOWN, buff=0.22)
        self.play(Create(gene_ticks), FadeIn(genes_lab), run_time=1.0)

        self.at("their order provides context")
        order_lab = T("order = context", size=26, color=GOLD).next_to(chrom, DOWN, buff=0.22)
        order_arrow = Arrow(chrom.blocks[0].get_top() + UP * 0.18, chrom.blocks[4].get_top() + UP * 0.18,
                            color=GOLD, stroke_width=3, buff=0.1, tip_length=0.18)
        self.play(swap(genes_lab, order_lab, run_time=0.6), FadeOut(count_chip, run_time=0.35), Create(order_arrow), run_time=1.0)

        self.at("For any rearrangement")
        chk_dose = boxed_label("1. DOSE", GREY, size=26, box=(2.5, 0.58))
        chk_ctx = boxed_label("2. CONTEXT", GREY, size=26, box=(2.5, 0.58))
        chk_mei = boxed_label("3. MEIOSIS", GREY, size=26, box=(2.5, 0.58))
        checklist = VGroup(chk_dose, chk_ctx, chk_mei).arrange(DOWN, buff=0.28).move_to([4.5, 0.1, 0])
        self.play(
            ReplacementTransform(c_dose, chk_dose),
            ReplacementTransform(c_ctx, chk_ctx),
            ReplacementTransform(c_mei, chk_mei),
            FadeOut(order_arrow),
            FadeOut(order_lab),
            run_time=1.0,
        )

        self.at("what material changed dose")
        dose_v = ValueTracker(0.0)
        gauge = DoseGauge(dose_v, center=(-3.8, -1.75, 0), width=3.6)
        link_dose = Line(chrom.blocks[1].get_bottom() + DOWN * 0.08, gauge.status.get_top() + UP * 0.12, color=GREEN, stroke_width=3)
        chk_dose_on = boxed_label("1. DOSE", GREEN, size=26, box=(2.5, 0.58)).move_to(chk_dose)
        self.play(
            ReplacementTransform(chk_dose, chk_dose_on),
            Create(link_dose),
            FadeIn(gauge, shift=DOWN * 0.2),
            run_time=1.1,
        )

        self.at("what breakpoint changed context")
        bx = (chrom.blocks[2].get_right()[0] + chrom.blocks[3].get_left()[0]) / 2
        by = chrom.get_center()[1]
        bp_line = DashedLine([bx, by - 0.72, 0], [bx, by + 0.72, 0], color=GOLD, stroke_width=4)
        bp_tag = T("breakpoint", size=24, color=GOLD).next_to(bp_line, UP, buff=0.16)
        chk_ctx_on = boxed_label("2. CONTEXT", GOLD, size=26, box=(2.5, 0.58)).move_to(chk_ctx)
        self.play(
            ReplacementTransform(chk_ctx, chk_ctx_on),
            Create(bp_line),
            FadeIn(bp_tag),
            run_time=1.1,
        )

        self.at("what products meiosis")
        c_pos = chrom.centromere.get_center()
        spindle = VGroup(
            Line([c_pos[0] - 0.08, chrom.blocks[1].get_bottom()[1] - 0.06, 0], [-0.4, -2.5, 0], color=GREY, stroke_width=2.4),
            Line([c_pos[0] + 0.08, chrom.blocks[1].get_bottom()[1] - 0.06, 0], [1.2, -2.5, 0], color=GREY, stroke_width=2.4),
        )
        spindle_lab = T("meiosis", size=24, color=TEAL).move_to([0.4, -2.9, 0])
        chk_mei_on = boxed_label("3. MEIOSIS", TEAL, size=26, box=(2.5, 0.58)).move_to(chk_mei)
        self.play(
            ReplacementTransform(chk_mei, chk_mei_on),
            Create(spindle),
            FadeIn(spindle_lab),
            run_time=1.2,
        )
        self.finish()


class S03DoseChanges(SpokenScene):
    def construct(self):
        self.at("Remove one block")
        chrom = make_chrom(["A", "B", "C", "D", "E"], BLUE, w=1.22, h=0.98, gap=0.07, font_size=32, centromere_after=1)
        chrom.move_to([0.0, 0.85, 0])
        dose_v = ValueTracker(0.0)
        gauge = DoseGauge(dose_v, center=(0.0, -1.75, 0), width=4.4)
        stag = scope_tag("schematic")

        blocks_cnt = ValueTracker(5.0)
        cnt_readout = counter("blocks: {:.0f}", blocks_cnt, at=(-4.4, -1.75, 0), size=28, color=TEXT)

        self.play(FadeIn(chrom), FadeIn(gauge), FadeIn(cnt_readout), FadeIn(stag), run_time=1.4)

        blk_a, blk_b, blk_c, blk_d, blk_e = chrom.blocks
        slot = DashedVMobject(
            RoundedRectangle(corner_radius=0.1, width=1.22, height=0.98, stroke_color=RED, stroke_width=2.5),
            num_dashes=16,
        ).move_to(blk_c)
        del_lab = T("DELETION", size=30, color=RED, weight=BOLD).move_to([0.0, 3.05, 0])

        self.play(
            FadeIn(slot),
            blk_c.animate.shift(UP * 1.15),
            FadeIn(del_lab),
            run_time=1.8,
        )
        shift_dx = (1.22 + 0.07) / 2.0
        self.play(
            FadeOut(blk_c),
            FadeOut(slot),
            VGroup(blk_a, blk_b, chrom.centromere).animate.shift(RIGHT * shift_dx),
            VGroup(blk_d, blk_e).animate.shift(LEFT * shift_dx),
            blocks_cnt.animate.set_value(4.0),
            dose_v.animate.set_value(-1.0),
            run_time=1.8,
        )

        self.at("lower dose")
        self.play(Indicate(gauge.status, color=RED, scale_factor=1.06), Indicate(gauge.needle, color=RED, scale_factor=1.2), run_time=1.2)

        self.at("A missing segment")
        miss_note = T("C missing: lower gene dose", size=26, color=RED).move_to([0.0, -0.35, 0])
        self.play(FadeIn(miss_note), Indicate(blk_b, color=TEXT, scale_factor=1.05), Indicate(blk_d, color=TEXT, scale_factor=1.05), run_time=2.2)

        self.at("Copy one block")
        restored = make_chrom(["A", "B", "C", "D", "E"], BLUE, w=1.22, h=0.98, gap=0.07, font_size=32, centromere_after=1)
        restored.move_to([0.0, 0.85, 0])
        old_group = VGroup(blk_a, blk_b, chrom.centromere, blk_d, blk_e)
        self.play(
            FadeOut(miss_note, run_time=0.4),
            FadeOut(del_lab, run_time=0.4),
            ReplacementTransform(old_group, restored),
            dose_v.animate.set_value(0.0),
            blocks_cnt.animate.set_value(5.0),
            run_time=1.6,
        )

        ra, rb, rc, rd, re_b = restored.blocks
        c_copy = make_block("C", TEAL, w=1.22, h=0.98, font_size=32).move_to(rc.get_center() + UP * 1.15)
        dup_lab = T("DUPLICATION", size=30, color=RED, weight=BOLD).move_to([0.0, 3.05, 0])
        self.play(FadeIn(c_copy, shift=UP * 0.2), FadeIn(dup_lab), run_time=1.1)

        self.play(
            VGroup(ra, rb, restored.centromere, rc).animate.shift(LEFT * shift_dx),
            VGroup(rd, re_b).animate.shift(RIGHT * shift_dx),
            run_time=1.1,
        )
        insert_pos = [rc.get_center()[0] + 1.22 + 0.07, rc.get_center()[1], 0]
        self.play(c_copy.animate.move_to(insert_pos), blocks_cnt.animate.set_value(6.0), dose_v.animate.set_value(1.0), run_time=1.2)

        self.at("higher dose")
        self.play(Indicate(gauge.status, color=RED, scale_factor=1.06), Indicate(gauge.needle, color=RED, scale_factor=1.2), run_time=1.2)

        self.at("An extra segment")
        extra_note = T("extra C: higher gene dose", size=26, color=RED).move_to([0.0, -0.35, 0])
        self.play(FadeIn(extra_note), Indicate(rc.box, color=TEXT, scale_factor=1.06), Indicate(c_copy.box, color=TEXT, scale_factor=1.06), run_time=2.0)

        self.at("The red gauge tracks")
        self.play(Indicate(gauge.needle, color=RED, scale_factor=1.35), Indicate(gauge.status, color=RED, scale_factor=1.06), run_time=2.2)
        self.finish()


class S04Inversion(SpokenScene):
    def construct(self):
        self.at("cut out several blocks")
        chrom = make_chrom(["A", "B", "C", "D", "E"], BLUE, w=1.12, h=0.72, gap=0.06, font_size=28, centromere_after=1)
        chrom.move_to([0.0, 0.75, 0])
        dose_v = ValueTracker(0.0)
        gauge = DoseGauge(dose_v, center=(0.0, -2.0, 0), width=4.0)
        cnt_lab = boxed_label("chromosome count: 1", TEXT, size=24).move_to([-4.3, -2.0, 0])
        self.play(FadeIn(chrom), FadeIn(gauge), FadeIn(cnt_lab), run_time=0.8)

        b_a, b_b, b_c, b_d, b_e = chrom.blocks
        p_b, p_c, p_d = b_b.get_center().copy(), b_c.get_center().copy(), b_d.get_center().copy()
        c_pos = chrom.centromere.get_center().copy()
        c_new = (p_c + p_d) / 2.0
        self.play(
            b_b.box.animate.set_stroke(TEAL),
            b_c.box.animate.set_stroke(TEAL),
            b_d.box.animate.set_stroke(TEAL),
            run_time=0.45,
        )
        # Lift B-C-D (with centromere at B|C) high enough (UP * 1.45 -> y=2.20) so B arcs over C and D arcs cleanly under C
        self.play(VGroup(b_b, b_c, b_d, chrom.centromere).animate.shift(UP * 1.45), run_time=0.9)
        arc_up = ArcBetweenPoints(p_b + UP * 1.45, p_d + UP * 1.45, angle=2.4)
        arc_dn = ArcBetweenPoints(p_d + UP * 1.45, p_b + UP * 1.45, angle=2.4)
        arc_cent = ArcBetweenPoints(c_pos + UP * 1.45, c_new + UP * 1.45, angle=2.4)
        self.play(
            MoveAlongPath(b_b, arc_up),
            MoveAlongPath(b_d, arc_dn),
            MoveAlongPath(chrom.centromere, arc_cent),
            run_time=1.3,
        )
        self.play(
            b_d.animate.move_to(p_b),
            b_c.animate.move_to(p_c),
            b_b.animate.move_to(p_d),
            chrom.centromere.animate.move_to(c_new),
            run_time=0.9,
        )

        self.at("That is an inversion")
        inv_lab = T("INVERSION (A-D-C-B-E)", size=28, color=TEAL, weight=BOLD).move_to([0.0, 2.35, 0])
        self.play(FadeIn(inv_lab), run_time=1.2)

        self.at("No block is lost")
        # Scan each block sequentially to verify all 5 remain present and dose stays green
        self.play(
            LaggedStart(*[Indicate(b, color=GREEN, scale_factor=1.08) for b in (b_a, b_d, b_c, b_b, b_e)], lag_ratio=0.35),
            Indicate(gauge.status, color=GREEN, scale_factor=1.06),
            run_time=2.8,
        )

        self.at("The chromosome count")
        self.play(Indicate(cnt_lab, color=GREEN, scale_factor=1.06), Indicate(gauge.needle, color=GREEN, scale_factor=1.2), run_time=2.2)

        self.at("During meiosis")
        gold = make_chrom(["A", "B", "C", "D", "E"], GOLD, w=1.12, h=0.72, gap=0.06, font_size=28, centromere_after=1)
        gold.move_to([0.0, -0.75, 0])
        self.play(
            FadeOut(gauge),
            FadeOut(cnt_lab),
            FadeOut(inv_lab),
            FadeOut(chrom.centromere),
            FadeIn(gold, shift=UP * 0.3),
            run_time=0.6,
        )
        self.remove(gold.centromere)

        blue_mobs = [b_a, b_d, b_c, b_b, b_e]
        gold_mobs = [gold.blocks[0], gold.blocks[1], gold.blocks[2], gold.blocks[3], gold.blocks[4]]
        blue_start = [m.get_center().copy() for m in blue_mobs]
        gold_start = [m.get_center().copy() for m in gold_mobs]

        blue_end = [
            np.array([-4.1, 0.55, 0]),   # A
            np.array([-1.7, 0.85, 0]),   # D
            np.array([0.0, 2.35, 0]),    # C
            np.array([1.7, 0.85, 0]),    # B
            np.array([4.1, 0.55, 0]),    # E
        ]
        gold_end = [
            np.array([-4.1, -0.60, 0]),  # A
            np.array([1.7, -0.35, 0]),   # B
            np.array([0.0, 1.15, 0]),    # C
            np.array([-1.7, -0.35, 0]),  # D
            np.array([4.1, -0.60, 0]),   # E
        ]

        loop_u = ValueTracker(0.0)

        def _update_blocks():
            u = loop_u.get_value()
            for m, s, e in zip(blue_mobs, blue_start, blue_end):
                m.move_to((1 - u) * s + u * e)
            for m, s, e in zip(gold_mobs, gold_start, gold_end):
                m.move_to((1 - u) * s + u * e)

        def _connectors():
            _update_blocks()
            u = loop_u.get_value()
            g = VGroup()
            # Blue connectors (short lines between adjacent block edges)
            for i in range(len(blue_mobs) - 1):
                p1, p2 = blue_mobs[i].get_center(), blue_mobs[i + 1].get_center()
                d = p2 - p1
                n = np.linalg.norm(d)
                if n > 1.25:
                    uvec = d / n
                    g.add(Line(p1 + uvec * 0.62, p2 - uvec * 0.62, color=BLUE, stroke_width=3.5))
            # Gold connectors: A->B and D->E sweep BELOW the loop when u > 0.1 so they never cross D or B!
            for i in range(len(gold_mobs) - 1):
                p1, p2 = gold_mobs[i].get_center(), gold_mobs[i + 1].get_center()
                d = p2 - p1
                n = np.linalg.norm(d)
                if i in (0, 3) and u > 0.12:
                    a = p1 + DOWN * 0.38
                    b_pt = p2 + DOWN * 0.38
                    ang = 0.55 * u if i == 0 else 0.55 * u
                    g.add(ArcBetweenPoints(a, b_pt, angle=ang, color=GOLD, stroke_width=3.5))
                elif n > 1.25:
                    uvec = d / n
                    g.add(Line(p1 + uvec * 0.62, p2 - uvec * 0.62, color=GOLD, stroke_width=3.5))
            return g

        conn = always_redraw(_connectors)
        self.add(conn)

        loop_cap = T("inversion loop aligns matching blocks", size=26, color=TEXT).move_to([0.0, -2.65, 0])
        self.play(loop_u.animate.set_value(1.0), FadeIn(loop_cap), run_time=2.0)
        self.finish()


class S05Exchange(SpokenScene):
    def construct(self):
        self.at("A reciprocal translocation")
        blue_v = make_chrom(["A", "B", "C", "D", "E"], BLUE, horizontal=False, w=1.0, h=0.78, gap=0.06, font_size=28, centromere_after=1)
        grey_v = make_chrom(["1", "2", "3", "4", "5"], GREY, horizontal=False, w=1.0, h=0.78, gap=0.06, font_size=28, centromere_after=1)
        blue_v.move_to([-4.0, 0.40, 0])
        grey_v.move_to([-1.2, 0.40, 0])

        lbl_b = T("blue", size=26, color=BLUE).next_to(blue_v, UP, buff=0.22)
        lbl_g = T("grey", size=26, color=GREY).next_to(grey_v, UP, buff=0.22)

        dose_v = ValueTracker(0.0)
        gauge = DoseGauge(dose_v, center=(3.5, 0.25, 0), width=3.8)
        cnt_lab = T("chromosomes: 2", size=24, color=TEXT).move_to([3.5, -1.25, 0])

        self.play(FadeIn(blue_v), FadeIn(grey_v), FadeIn(lbl_b), FadeIn(lbl_g), FadeIn(gauge), FadeIn(cnt_lab), run_time=2.2)

        break_y = (blue_v.blocks[2].get_bottom()[1] + blue_v.blocks[3].get_top()[1]) / 2
        cut_line = DashedLine([-4.8, break_y, 0], [-0.4, break_y, 0], color=TEXT, stroke_width=3.5)
        self.play(Create(cut_line), run_time=1.4)

        self.at("Move a teal end segment")
        b_de = VGroup(blue_v.blocks[3], blue_v.blocks[4])
        g_45 = VGroup(grey_v.blocks[3], grey_v.blocks[4])
        p_b_de = b_de.get_center().copy()
        p_g_45 = g_45.get_center().copy()

        self.play(
            blue_v.blocks[3].box.animate.set_stroke(TEAL).set_fill(TEAL, opacity=0.25),
            blue_v.blocks[4].box.animate.set_stroke(TEAL).set_fill(TEAL, opacity=0.25),
            run_time=0.6,
        )
        self.play(b_de.animate.shift(DOWN * 1.65 + RIGHT * 1.4), run_time=1.4)

        self.at("return a gray segment")
        self.play(
            LaggedStart(
                g_45.animate.move_to(p_b_de),
                b_de.animate(path_arc=0.6).move_to(p_g_45),
                lag_ratio=0.75,
            ),
            FadeOut(cut_line),
            run_time=2.0,
        )

        self.at("Total dose may stay balanced")
        brk_l = VGroup(
            Line([-4.62, break_y + 0.16, 0], [-4.72, break_y + 0.16, 0], color=TEXT, stroke_width=4),
            Line([-4.72, break_y + 0.16, 0], [-4.72, break_y - 0.16, 0], color=TEXT, stroke_width=4),
            Line([-4.72, break_y - 0.16, 0], [-4.62, break_y - 0.16, 0], color=TEXT, stroke_width=4),
        )
        brk_r = VGroup(
            Line([-0.58, break_y + 0.16, 0], [-0.48, break_y + 0.16, 0], color=TEXT, stroke_width=4),
            Line([-0.48, break_y + 0.16, 0], [-0.48, break_y - 0.16, 0], color=TEXT, stroke_width=4),
            Line([-0.48, break_y - 0.16, 0], [-0.58, break_y - 0.16, 0], color=TEXT, stroke_width=4),
        )
        new_lab = T("new neighbours", size=26, color=TEAL).move_to([-2.6, -2.65, 0])
        self.play(Create(brk_l), Create(brk_r), FadeIn(new_lab), Indicate(gauge.status, color=GREEN), run_time=1.2)
        pulse(brk_l, base=4.5, amp=2.2, speed=4.0)
        pulse(brk_r, base=4.5, amp=2.2, speed=4.0)
        self.finish()


class S06Context(SpokenScene):
    def construct(self):
        self.at("Balanced dose")
        dose_v = ValueTracker(0.0)
        gauge = DoseGauge(dose_v, center=(3.8, -2.05, 0), width=3.6)
        cnt_box = boxed_label("chromosome count: 2 (unchanged)", TEXT, size=24).move_to([-3.2, -2.05, 0])
        stag = scope_tag("schematic")
        self.play(FadeIn(gauge), FadeIn(cnt_box), FadeIn(stag), run_time=2.0)

        self.at("A breakpoint can interrupt")
        gene_left = make_block("GE", BLUE, w=1.45, h=0.95, font_size=30)
        gene_right = make_block("NE", BLUE, w=1.45, h=0.95, font_size=30)
        gene_whole = VGroup(gene_left, gene_right).arrange(RIGHT, buff=0.0).move_to([-1.2, 1.55, 0])
        gene_full_lab = boxed_label("GENE", BLUE, size=30, box=(2.9, 0.95)).move_to(gene_whole)
        bp = DashedLine([-1.2, 2.3, 0], [-1.2, 0.8, 0], color=GOLD, stroke_width=4)

        self.play(FadeIn(gene_full_lab), run_time=0.7)
        self.play(Create(bp), ReplacementTransform(gene_full_lab, gene_whole), run_time=0.8)
        can1 = T("can interrupt a gene", size=28, color=GOLD).move_to([3.5, 1.55, 0])
        self.play(
            gene_left.animate.shift(LEFT * 0.45),
            gene_right.animate.shift(RIGHT * 0.45),
            FadeIn(can1),
            run_time=1.2,
        )

        self.at("place pieces from different genes")
        ga_half = make_block("GENE A (1/2)", BLUE, w=2.55, h=0.95, font_size=26).move_to([-3.2, -0.15, 0])
        gb_half = make_block("GENE B (1/2)", TEAL, w=2.55, h=0.95, font_size=26).move_to([0.8, -0.15, 0])
        can2 = T("can join different genes", size=28, color=TEAL).move_to([2.05, -0.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(ga_half, shift=RIGHT * 0.2), FadeIn(gb_half, shift=LEFT * 0.2), run_time=0.9)
        self.play(
            ga_half.animate.move_to([-1.2 - 0.14 - ga_half.width / 2, -0.15, 0]),
            gb_half.animate.move_to([-1.2 + 0.14 + gb_half.width / 2, -0.15, 0]),
            FadeIn(can2),
            run_time=1.2,
        )

        self.at("The result depends")
        j_line = Line([-1.2, 0.48, 0], [-1.2, -0.78, 0], color=TEXT, stroke_width=4.5)
        self.play(Create(j_line), Indicate(bp, color=GOLD), run_time=1.3)

        self.at("changes in gene context")
        ctx_head = T("GENE CONTEXT CHANGED", size=28, color=GOLD, weight=BOLD).move_to([0.0, 2.95, 0])
        self.play(FadeIn(ctx_head), Indicate(gauge.status, color=GREEN), Indicate(cnt_box, color=TEXT), run_time=1.6)
        self.finish()


class S07Pairing(SpokenScene):
    def construct(self):
        self.at("The carrier still faces")
        cross, cdict = build_translocation_cross(center=(0.0, 0.45), step=0.65, arm_gap=0.56)
        nw, ne, se, sw = cdict["NW"], cdict["NE"], cdict["SE"], cdict["SW"]

        self.play(FadeIn(ne), FadeIn(sw), run_time=1.2)

        self.at("Normal and translocated partners")
        nw_start = nw.copy().shift(LEFT * 2.2)
        se_start = se.copy().shift(RIGHT * 2.2)
        self.play(FadeIn(nw_start, shift=RIGHT * 0.4), FadeIn(se_start, shift=LEFT * 0.4), run_time=2.0)

        self.at("All four chromosomes")
        self.play(
            ReplacementTransform(nw_start, nw),
            ReplacementTransform(se_start, se),
            run_time=2.5,
        )

        self.at("The way this cross separates")
        zones, zdict = build_gamete_zones(left_x=-4.6, right_x=4.6, y=0.60, r=1.40)
        spindles = build_spindle_fibres(cdict, left_pole=(-6.15, 0.45, 0), right_pole=(6.15, 0.45, 0))
        z_lab_l = T("gamete zone", size=24, color=GREY).move_to([-4.6, -1.15, 0])
        z_lab_r = T("gamete zone", size=24, color=GREY).move_to([4.6, -1.15, 0])

        self.play(FadeIn(zones), FadeIn(z_lab_l), FadeIn(z_lab_r), run_time=1.8)
        self.play(Create(spindles), run_time=3.4)
        bob(spindles, amp=0.035, speed=1.8, seed=0)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        self.at("which separation preserves")
        cross, cdict = build_translocation_cross(center=(0.0, 0.45), step=0.65, arm_gap=0.56)
        zones, zdict = build_gamete_zones(left_x=-4.6, right_x=4.6, y=0.60, r=1.40)
        spindles = build_spindle_fibres(cdict, left_pole=(-6.15, 0.45, 0), right_pole=(6.15, 0.45, 0))
        qmarks = VGroup(*[T("?", size=48, color=GOLD, weight=BOLD).move_to(zdict[k]) for k in ("L", "R")])

        self.add(cross, zones, spindles)
        bob(spindles, amp=0.035, speed=1.8, seed=0)
        self.play(LaggedStart(*[FadeIn(q, scale=1.2) for q in qmarks], lag_ratio=0.35), run_time=2.4)

        opp_arrows, adj_arrows = build_segregation_arrows(cdict, opp_color=GOLD, adj_color=TEAL)

        self.at("opposite chromosomes moving")
        opp_tag = T("opposite", size=24, color=GOLD).move_to([-2.4, 2.85, 0])
        self.play(Create(opp_arrows), FadeIn(opp_tag), run_time=1.6)

        self.at("neighboring chromosomes moving")
        adj_tag = T("neighbouring", size=24, color=TEAL).move_to([2.4, 2.85, 0])
        self.play(Create(adj_arrows), FadeIn(adj_tag), run_time=1.6)

        self.at("Look at the block ledgers")
        l_blank = make_block_ledger("LEFT GAMETE", [("blue A-E", "?", GOLD), ("grey 1-5", "?", GOLD)], GREY, min_width=2.9, center=(-4.2, -2.80, 0))
        r_blank = make_block_ledger("RIGHT GAMETE", [("blue A-E", "?", GOLD), ("grey 1-5", "?", GOLD)], GREY, min_width=2.9, center=(3.8, -2.80, 0))
        qcard = question_card("Which keeps 1 copy\nof every block?", y=-3.05, size=24, max_w=4.6)
        qcard.move_to([-0.2, -3.05, 0])
        self.play(FadeIn(l_blank), FadeIn(r_blank), FadeIn(qcard), run_time=1.3)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Which keeps 1 copy\nof every block?"
    OPTIONS = ()
    CARD = {"y": -3.05, "size": 24, "max_w": 4.6}
    RING_AT = (6.15, -3.1, 0)
    SECONDS = 4.5

    def backdrop(self):
        cross, cdict = build_translocation_cross(center=(0.0, 0.45), step=0.65, arm_gap=0.56)
        zones, zdict = build_gamete_zones(left_x=-4.6, right_x=4.6, y=0.60, r=1.40)
        spindles = build_spindle_fibres(cdict, left_pole=(-6.15, 0.45, 0), right_pole=(6.15, 0.45, 0))
        bob(spindles, amp=0.035, speed=1.8, seed=0)
        qmarks = VGroup(*[T("?", size=48, color=GOLD, weight=BOLD).move_to(zdict[k]) for k in ("L", "R")])
        opp_arrows, adj_arrows = build_segregation_arrows(cdict, opp_color=GOLD, adj_color=TEAL)
        opp_tag = T("opposite", size=24, color=GOLD).move_to([-2.4, 2.85, 0])
        adj_tag = T("neighbouring", size=24, color=TEAL).move_to([2.4, 2.85, 0])
        l_blank = make_block_ledger("LEFT GAMETE", [("blue A-E", "?", GOLD), ("grey 1-5", "?", GOLD)], GREY, min_width=2.9, center=(-4.2, -2.80, 0))
        r_blank = make_block_ledger("RIGHT GAMETE", [("blue A-E", "?", GOLD), ("grey 1-5", "?", GOLD)], GREY, min_width=2.9, center=(3.8, -2.80, 0))
        return VGroup(cross, zones, spindles, qmarks, opp_arrows, adj_arrows, opp_tag, adj_tag, l_blank, r_blank)

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, self.OPTIONS, **self.CARD)
        q.move_to([-0.2, -3.05, 0])
        self.add(q)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        self.at("Opposite partners preserve")
        cross, cdict = build_translocation_cross(center=(0.0, 0.45), step=0.65, arm_gap=0.56)
        zones, zdict = build_gamete_zones(left_x=-4.6, right_x=4.6, y=0.60, r=1.40)
        green_arrows, red_arrows = build_segregation_arrows(cdict)
        qmarks = VGroup(*[T("?", size=48, color=GOLD, weight=BOLD).move_to(zdict[k]) for k in ("L", "R")])
        self.add(cross, zones, green_arrows, red_arrows, qmarks)

        def _zone_chrom(labels, colors, pos):
            return make_chrom(labels, colors, horizontal=True, w=0.42, h=0.46, gap=0.02, font_size=22).move_to(pos)

        lc = zdict["L"].get_center()
        rc = zdict["R"].get_center()
        dy = 0.36

        self.play(FadeOut(red_arrows), FadeOut(qmarks), Indicate(green_arrows, color=GREEN), run_time=0.8)
        nw_alt = _zone_chrom(["A", "B", "C", "D", "E"], BLUE, lc + UP * dy)
        se_alt = _zone_chrom(["1", "2", "3", "4", "5"], GREY, lc + DOWN * dy)
        ne_alt = _zone_chrom(["A", "B", "C", "4", "5"], [BLUE, BLUE, BLUE, GREY, GREY], rc + UP * dy)
        sw_alt = _zone_chrom(["1", "2", "3", "D", "E"], [GREY, GREY, GREY, TEAL, TEAL], rc + DOWN * dy)
        self.play(
            FadeOut(green_arrows),
            FadeOut(cross),
            FadeIn(nw_alt, shift=LEFT * 1.2),
            FadeIn(se_alt, shift=LEFT * 1.2),
            FadeIn(ne_alt, shift=RIGHT * 1.2),
            FadeIn(sw_alt, shift=RIGHT * 1.2),
            run_time=1.8,
        )

        self.at("alternate segregation")
        alt_head = T("ALTERNATE SEGREGATION: BALANCED", size=28, color=GREEN, weight=BOLD).move_to([0.0, 2.95, 0])
        l_alt = make_block_ledger(
            "NORMAL GAMETE",
            [("A-E (blue)", "1 copy each", GREEN), ("1-5 (grey)", "1 copy each", GREEN)],
            GREEN,
            center=(-3.8, -2.72, 0),
        )
        r_alt = make_block_ledger(
            "BALANCED CARRIER",
            [("A-E (blue+teal)", "1 copy each", GREEN), ("1-5 (grey)", "1 copy each", GREEN)],
            GREEN,
            center=(3.8, -2.72, 0),
        )
        self.play(FadeIn(alt_head), FadeIn(l_alt), FadeIn(r_alt), run_time=1.4)

        self.at("Neighboring partners give")
        # Reset the cross completely cleanly before animating red neighbouring arrows
        cross2, cdict2 = build_translocation_cross(center=(0.0, 0.45), step=0.65, arm_gap=0.56)
        _, red_arrows2 = build_segregation_arrows(cdict2)
        self.play(
            FadeOut(alt_head),
            FadeOut(l_alt),
            FadeOut(r_alt),
            FadeOut(nw_alt),
            FadeOut(se_alt),
            FadeOut(ne_alt),
            FadeOut(sw_alt),
            FadeIn(cross2),
            run_time=1.2,
        )
        self.play(Create(red_arrows2), run_time=0.8)
        nw_adj = _zone_chrom(["A", "B", "C", "D", "E"], BLUE, lc + UP * dy)
        sw_adj = _zone_chrom(["1", "2", "3", "D", "E"], [GREY, GREY, GREY, TEAL, TEAL], lc + DOWN * dy)
        ne_adj = _zone_chrom(["A", "B", "C", "4", "5"], [BLUE, BLUE, BLUE, GREY, GREY], rc + UP * dy)
        se_adj = _zone_chrom(["1", "2", "3", "4", "5"], GREY, rc + DOWN * dy)
        self.play(
            FadeOut(red_arrows2),
            FadeOut(cross2),
            FadeIn(nw_adj, shift=LEFT * 1.2),
            FadeIn(sw_adj, shift=LEFT * 1.2),
            FadeIn(ne_adj, shift=RIGHT * 1.2),
            FadeIn(se_adj, shift=RIGHT * 1.2),
            run_time=1.8,
        )

        self.at("adjacent segregation")
        adj_head = T("ADJACENT SEGREGATION: UNBALANCED", size=28, color=RED, weight=BOLD).move_to([0.0, 2.95, 0])
        l_adj = make_block_ledger(
            "UNBALANCED GAMETE",
            [("D-E (teal)", "2 copies (extra)", RED), ("4-5 (grey end)", "0 copies (missing)", RED)],
            RED,
            center=(-3.5, -2.72, 0),
        )
        r_adj = make_block_ledger(
            "UNBALANCED GAMETE",
            [("4-5 (grey end)", "2 copies (extra)", RED), ("D-E (teal)", "0 copies (missing)", RED)],
            RED,
            center=(3.5, -2.72, 0),
        )
        self.play(FadeIn(adj_head), FadeIn(l_adj), FadeIn(r_adj), run_time=1.4)
        self.finish()


class S11Carrier(SpokenScene):
    def construct(self):
        self.at("That explains a common puzzle")
        cell_box = RoundedRectangle(
            corner_radius=0.35, width=5.4, height=2.55,
            stroke_color=GREY, stroke_width=2.8, fill_color=GREY, fill_opacity=0.08
        ).move_to([-2.9, 1.55, 0])
        cell_lbl = T("carrier cell", size=24, color=GREY).next_to(cell_box, UP, buff=0.14)

        c1 = make_chrom(["A", "B", "C", "D", "E"], BLUE, w=0.62, h=0.42, gap=0.03, font_size=24)
        c2 = make_chrom(["A", "B", "C", "4", "5"], [BLUE, BLUE, BLUE, GREY, GREY], w=0.62, h=0.42, gap=0.03, font_size=24)
        c3 = make_chrom(["1", "2", "3", "4", "5"], GREY, w=0.62, h=0.42, gap=0.03, font_size=24)
        c4 = make_chrom(["1", "2", "3", "D", "E"], [GREY, GREY, GREY, TEAL, TEAL], w=0.62, h=0.42, gap=0.03, font_size=24)
        chroms = VGroup(c1, c2, c3, c4).arrange(DOWN, buff=0.14).move_to(cell_box)

        carrier_ledger = make_block_ledger(
            "CARRIER SET: BALANCED",
            [("A-E (blue+teal)", "2 copies each", GREEN), ("1-5 (grey)", "2 copies each", GREEN)],
            GREEN,
            center=(3.1, 1.55, 0),
        )

        self.play(FadeIn(cell_box), FadeIn(cell_lbl), FadeIn(chroms), FadeIn(carrier_ledger), run_time=1.2)

        self.at("A carrier can be healthy")
        bp_x = (c2.blocks[2].get_right()[0] + c2.blocks[3].get_left()[0]) / 2
        bp_y = c2.get_center()[1]
        bp_mark = Line([bp_x, bp_y - 0.25, 0], [bp_x, bp_y + 0.25, 0], color=GOLD, stroke_width=3.5)
        bp_mark2 = Line([bp_x, c4.get_center()[1] - 0.25, 0], [bp_x, c4.get_center()[1] + 0.25, 0], color=GOLD, stroke_width=3.5)
        diff_lbl = T("outcomes can differ", size=24, color=GOLD).move_to([-4.6, -0.25, 0])
        diff_ptr = Arrow(diff_lbl.get_right() + RIGHT * 0.04, bp_mark2.get_bottom(), color=GOLD, stroke_width=2.5, buff=0.08, tip_length=0.15)
        self.play(Indicate(carrier_ledger, color=GREEN), Create(bp_mark), Create(bp_mark2), FadeIn(diff_lbl), Create(diff_ptr), run_time=1.3)

        self.at("Yet meiosis can produce")
        g_alt = make_block_ledger(
            "ALTERNATE GAMETES",
            [("all blocks", "1 copy each (balanced)", GREEN)],
            GREEN,
            center=(-3.25, -2.15, 0),
        )
        g_adj = make_block_ledger(
            "ADJACENT GAMETES",
            [("D-E / 4-5", "extra + missing", RED)],
            RED,
            center=(3.25, -2.15, 0),
        )
        arr_l = Arrow([-2.0, cell_box.get_bottom()[1] - 0.06, 0], [-2.5, g_alt.get_top()[1] + 0.08, 0], color=GREEN, stroke_width=3, tip_length=0.16)
        arr_r = Arrow([-0.9, cell_box.get_bottom()[1] - 0.06, 0], g_adj.get_top() + UP * 0.08, color=RED, stroke_width=3, tip_length=0.16)
        self.play(Create(arr_l), Create(arr_r), FadeIn(g_alt), FadeIn(g_adj), run_time=1.6)

        self.at("Balance must therefore")
        # Highlight Level 1 (carrier set) then Level 2 (meiotic gametes) sequentially across the beat
        self.play(Indicate(carrier_ledger, color=GREEN, scale_factor=1.05), Indicate(cell_box, color=GREEN, scale_factor=1.02), run_time=2.2)
        self.play(Indicate(g_alt, color=GREEN, scale_factor=1.05), Indicate(g_adj, color=RED, scale_factor=1.05), run_time=2.4)

        self.at("context and segregation")
        self.play(Indicate(diff_lbl, color=GOLD, scale_factor=1.06), Indicate(g_adj, color=RED, scale_factor=1.04), run_time=1.3)

        self.at("not chromosome count alone")
        cnt_note = T("not chromosome count alone", size=24, color=TEXT).move_to([3.1, 0.05, 0])
        self.play(FadeIn(cnt_note), run_time=1.0)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        self.at("Trace three things")
        carrier_top = make_block_ledger(
            "CARRIER SET: BALANCED",
            [("DNA blocks", "A-E and 1-5: 2 copies each", GREEN)],
            GREEN,
            center=(0.0, 2.35, 0),
        )

        dose_v = ValueTracker(0.0)
        mini_gauge = DoseGauge(dose_v, center=(-4.0, -0.75, 0), width=4.0, title="DOSE")
        mini_bp = VGroup(
            make_block("A", BLUE, w=0.72, h=0.65, font_size=24),
            DashedLine([0, 0.5, 0], [0, -0.5, 0], color=GOLD, stroke_width=3.5),
            make_block("B", TEAL, w=0.72, h=0.65, font_size=24),
        ).arrange(RIGHT, buff=0.14).move_to([0.0, -0.75, 0])
        mini_cross, _ = build_translocation_cross(
            center=(4.45, -0.75), step=0.52, arm_gap=0.28, block_size=(0.46, 0.44), font_size=24
        )

        self.play(FadeIn(carrier_top), FadeIn(mini_gauge), FadeIn(mini_bp), FadeIn(mini_cross), run_time=1.8)

        n_break = boxed_label("BREAK", TEXT, size=25, box=(1.70, 0.85)).move_to([-5.25, -0.75, 0])
        n_dose = boxed_label("DNA DOSE", GREEN, size=25, box=(2.30, 0.85)).move_to([-2.45, -0.75, 0])
        n_ctx = boxed_label("GENE CONTEXT", GOLD, size=25, box=(2.70, 0.85)).move_to([0.85, -0.75, 0])
        n_mei = boxed_label("MEIOSIS", TEAL, size=25, box=(2.15, 0.85)).move_to([4.55, -0.75, 0])

        a1 = Arrow(n_break.get_right() + RIGHT * 0.06, n_dose.get_left() + LEFT * 0.06, color=GREY, stroke_width=3, buff=0, tip_length=0.16)
        a2 = Arrow(n_dose.get_right() + RIGHT * 0.06, n_ctx.get_left() + LEFT * 0.06, color=GREY, stroke_width=3, buff=0, tip_length=0.16)
        a3 = Arrow(n_ctx.get_right() + RIGHT * 0.06, n_mei.get_left() + LEFT * 0.06, color=GREY, stroke_width=3, buff=0, tip_length=0.16)

        self.at("what material was gained")
        q_dose = T("gained or lost?", size=24, color=GREEN).next_to(n_dose, DOWN, buff=0.22)
        self.play(FadeOut(mini_gauge), run_time=0.45)
        self.play(
            FadeIn(n_break),
            Create(a1),
            FadeIn(n_dose),
            FadeIn(q_dose),
            run_time=1.0,
        )

        self.at("which genes were interrupted")
        q_ctx = T("interrupted or joined?", size=24, color=GOLD).next_to(n_ctx, DOWN, buff=0.22)
        self.play(
            swap(mini_bp, n_ctx, run_time=0.9),
            Create(a2),
            FadeIn(q_ctx),
            run_time=1.3,
        )

        self.at("which chromosome combinations")
        q_mei = T("balanced gametes?", size=24, color=TEAL).next_to(n_mei, DOWN, buff=0.22)
        self.play(
            swap(mini_cross, n_mei, run_time=0.9),
            Create(a3),
            FadeIn(q_mei),
            run_time=1.3,
        )

        seg = make_block("D-E", TEAL, w=1.05, h=0.62, font_size=24).move_to(n_break.get_top() + UP * 0.55)
        self.play(FadeIn(seg, shift=DOWN * 0.15), run_time=0.7)

        self.at("through DNA dose")
        self.play(seg.animate.move_to(n_dose.get_top() + UP * 0.55), Indicate(n_dose, color=GREEN), run_time=1.1)

        self.at("gene context")
        self.play(seg.animate.move_to(n_ctx.get_top() + UP * 0.55), Indicate(n_ctx, color=GOLD), run_time=1.0)

        self.at("and meiotic balance")
        self.play(seg.animate.move_to(n_mei.get_top() + UP * 0.55), Indicate(n_mei, color=TEAL), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Rearrangements matter through DNA dose, gene context, and meiotic balance."
