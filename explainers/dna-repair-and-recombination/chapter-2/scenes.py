"""
COLOUR MAP (one colour per concept for the entire film):
- BLUE (#58C4DD) : Broken / original chromosome DNA (two thick block-patterned rows)
- RED  (#FC6255) : Double-strand break flash, ragged damaged ends, missing-template alert
- GOLD (#D4A843) : Trusted intact template (brief partner highlight in s01; sister chromatid DNA)
- GREEN (#83C167): Newly synthesized / restored DNA and ligated repair joints
- TEAL (#3FB8C0) : Repair machinery (Ku cuffs, bridging partners, trim/fill tools, recombinase, selector/brackets)
- TEXT (#E8EAF0) : Primary labels, headings, and questions
- GREY (#8B93A1) : Schematic scope tags, cell envelopes, cell-cycle strip borders

ONE CARRIED WORLD:
Two thick horizontal DNA rows built from sequence-block segments, broken across both strands
into left and right ends, carried through zoomed repair views, side-by-side before/after
replication cells, and the forked decision path between joining ends and copying a sister.

SCENE-BY-SCENE CHANGES (WHAT CHANGES & COMPUTED FROM WHAT):
- s01_hook    : Gold partner highlight glides along intact lower strand; red flash cuts both rows; left/right ends separate by computed drift; red '?' expands in gap; curved end-joining arrow and outward search arrow grow.
- s02_title   : Standard TitleCard ("DNA Repair and Recombination" / "Two Ways to Mend a Broken Chromosome").
- s03_choice  : Carried broken chromosome forks into two branches; left ends curve inward under "join ends"; gold sister track glides behind right gap under "copy a template"; teal selector travels between branches.
- s04_join    : Zoomed left branch; teal Ku cuffs slide onto both blue ends; bridging partners pull compatible block edges into a green joint; resets to ragged red tips where teal tools trim one tip and add one plain block before forming a green joint.
- s05_cycle   : ValueTracker drives broken blue chromosome + Ku cuffs across a two-zone cell-cycle strip while teal end-joining track spans the full strip and gold sister track emerges and brightens after the replication boundary.
- s06_predict : Two side-by-side cells ("before replication", "after replication") receive broken blue chromosomes and empty dashed gold outlines while a '?' pointer sweeps above them and the predict question appears.
- s07_pause   : PredictPause holds both cells and question for 4.5 s while empty gold outlines pulse gently and the countdown ring empties.
- s08_reveal  : Right cell's empty outline fills into a solid gold sister that slides up to align matching blocks across the blue break; left cell's outline collapses into "no sister yet"; teal Ku cuffs remain visible on ends in both cells.
- s09_copy    : Zoomed right cell; broken blue ends taper into single-stranded tails; teal recombinase beads coat one tail; tail scans along gold sister, pauses at matching blocks, invades; ValueTracker grows new green DNA while a gold guide highlight advances underneath.
- s10_finish  : Copied green-extended duplex splits into two simultaneous routes: upper strand lifts off gold and pairs with its other blue end; lower blue and gold tracks form two crossed junctions ("crossed junctions, schematic").
- s11_compare : Returns to forked path; left branch animates three "possible" outcomes (exact green joint, short deletion, short addition); right branch shows green restoration only while gold sister is present; headers swap to "ends joinable?" and "template available?".
- s12_close   : Forked paths merge into one repaired chromosome over the gold sister; teal bracket wraps the joined ends, gold bracket wraps the sister, and both transform into "What information remains?" as the repaired chromosome glides smoothly beneath.
- s13_end     : Standard EndCard with exact take-home line.
"""

from bp_parts import *

# Distinctive block-width rhythm so matching sequence blocks are visibly recognizable
# across the break and between the blue chromosome and gold sister chromatid.
HALF_WIDTHS_L = [0.68, 0.96, 0.58, 0.88, 0.72]
HALF_WIDTHS_R = [0.74, 0.62, 0.98, 0.66, 0.82]
ALL_WIDTHS = HALF_WIDTHS_L + HALF_WIDTHS_R


def make_duplex_segment(
    widths,
    block_h=0.46,
    row_gap=0.16,
    block_gap=0.06,
    color=BLUE,
    fill_opacity=0.55,
    stroke_width=2.5,
    ragged_side=None,
    dashed=False,
):
    """Build two thick parallel DNA rows made of rectangular sequence blocks."""
    top_row = VGroup()
    bot_row = VGroup()
    x = 0.0
    for idx, w in enumerate(widths):
        is_left_tip = idx == 0 and ragged_side == "left"
        is_right_tip = idx == len(widths) - 1 and ragged_side == "right"
        for row_idx, row in enumerate((top_row, bot_row)):
            if is_left_tip or is_right_tip:
                # Ragged red damaged tip on the cut end
                tip_col = RED
                if is_right_tip:
                    pts = [
                        [x, 0, 0],
                        [x + w, 0, 0],
                        [x + w + (0.14 if row_idx == 0 else -0.10), block_h * 0.35, 0],
                        [x + w - 0.06, block_h * 0.70, 0],
                        [x + w + (0.08 if row_idx == 1 else -0.12), block_h, 0],
                        [x, block_h, 0],
                    ]
                else:
                    pts = [
                        [x + w, 0, 0],
                        [x, 0, 0],
                        [x - (0.12 if row_idx == 0 else -0.08), block_h * 0.35, 0],
                        [x + 0.06, block_h * 0.70, 0],
                        [x - (0.08 if row_idx == 1 else -0.12), block_h, 0],
                        [x + w, block_h, 0],
                    ]
                blk = Polygon(
                    *pts,
                    stroke_color=tip_col,
                    stroke_width=stroke_width + 0.5,
                    fill_color=tip_col,
                    fill_opacity=0.65,
                )
            else:
                rect = RoundedRectangle(
                    corner_radius=0.06,
                    width=w,
                    height=block_h,
                    stroke_color=color,
                    stroke_width=stroke_width,
                    fill_color=color,
                    fill_opacity=0.0 if dashed else fill_opacity,
                )
                if dashed:
                    blk = DashedVMobject(rect, num_dashes=max(6, int(w * 10)), dashed_ratio=0.55)
                else:
                    blk = rect
                blk.move_to([x + w / 2, block_h / 2, 0])
            row.add(blk)
        x += w + block_gap

    top_row.move_to([0, (block_h + row_gap) / 2, 0])
    bot_row.move_to([0, -(block_h + row_gap) / 2, 0])
    g = VGroup(top_row, bot_row)
    g.top_row = top_row
    g.bot_row = bot_row
    return g


def make_broken_pair(
    gap=1.6,
    scale_x=1.0,
    block_h=0.46,
    row_gap=0.16,
    color=BLUE,
    fill_opacity=0.55,
    ragged=False,
    center=(0, 0, 0),
):
    """Build matching left and right broken chromosome halves separated by `gap`."""
    wl = [w * scale_x for w in HALF_WIDTHS_L]
    wr = [w * scale_x for w in HALF_WIDTHS_R]
    left = make_duplex_segment(
        wl, block_h=block_h, row_gap=row_gap, color=color, fill_opacity=fill_opacity,
        ragged_side="right" if ragged else None,
    )
    right = make_duplex_segment(
        wr, block_h=block_h, row_gap=row_gap, color=color, fill_opacity=fill_opacity,
        ragged_side="left" if ragged else None,
    )
    cx, cy, cz = center
    left.move_to([cx - gap / 2 - left.width / 2, cy, cz])
    right.move_to([cx + gap / 2 + right.width / 2, cy, cz])
    pair = VGroup(left, right)
    pair.left = left
    pair.right = right
    return pair


def make_ku_cuff(side="left", height=1.55, depth=0.55, color=TEAL, label_text=None):
    """Build a thick C-shaped teal Ku cuff that slides onto a broken chromosome end."""
    t = 0.18
    if side == "left":
        # Open toward left, solid bar on right (facing the end)
        pts = [
            [-depth, height / 2, 0],
            [0.0, height / 2, 0],
            [0.0, -height / 2, 0],
            [-depth, -height / 2, 0],
            [-depth, -height / 2 + t, 0],
            [-t, -height / 2 + t, 0],
            [-t, height / 2 - t, 0],
            [-depth, height / 2 - t, 0],
        ]
    else:
        pts = [
            [depth, height / 2, 0],
            [0.0, height / 2, 0],
            [0.0, -height / 2, 0],
            [depth, -height / 2, 0],
            [depth, -height / 2 + t, 0],
            [t, -height / 2 + t, 0],
            [t, height / 2 - t, 0],
            [depth, height / 2 - t, 0],
        ]
    cuff = Polygon(*pts, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.65)
    g = VGroup(cuff)
    g.cuff = cuff
    if label_text:
        shift_dir = LEFT * 0.62 if side == "left" else RIGHT * 0.62
        lab = T(label_text, size=28, color=color, weight=BOLD).next_to(cuff, UP, buff=0.18).shift(shift_dir)
        g.add(lab)
        g.label = lab
    return g


def make_cell_box(center, width=5.6, height=4.5, title="", color=GREY):
    """A large rounded cell boundary with a clear top heading inside."""
    box = RoundedRectangle(
        corner_radius=0.55,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=3.0,
        fill_color=color,
        fill_opacity=0.06,
    ).move_to(center)
    g = VGroup(box)
    g.box = box
    if title:
        head = T(title, size=28, color=TEXT, weight=BOLD).move_to(
            [center[0], box.get_top()[1] - 0.42, 0]
        )
        g.add(head)
        g.head = head
    return g


def make_bracket(target, side=UP, color=TEAL, buff=0.14, tick=0.18, stroke_width=4.0):
    """A crisp rectangular bracket around the horizontal span of `target`."""
    x0, x1 = target.get_left()[0] - 0.1, target.get_right()[0] + 0.1
    if np.array_equal(side, UP):
        y = target.get_top()[1] + buff
        pts = [[x0, y - tick, 0], [x0, y, 0], [x1, y, 0], [x1, y - tick, 0]]
    else:
        y = target.get_bottom()[1] - buff
        pts = [[x0, y + tick, 0], [x0, y, 0], [x1, y, 0], [x1, y + tick, 0]]
    m = VMobject(stroke_color=color, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


# ------------------------------------------------------------------ s01_hook
class S01Hook(SpokenScene):
    def construct(self):
        # Two thick blue rows already filling most of the frame width
        left = make_duplex_segment(
            [w * 1.15 for w in HALF_WIDTHS_L], block_h=0.62, row_gap=0.22, color=BLUE, fill_opacity=0.58
        )
        right = make_duplex_segment(
            [w * 1.15 for w in HALF_WIDTHS_R], block_h=0.62, row_gap=0.22, color=BLUE, fill_opacity=0.58
        )
        left.move_to([-left.width / 2 - 0.04, 0.2, 0])
        right.move_to([right.width / 2 + 0.04, 0.2, 0])
        chrom = VGroup(left, right)
        tag = scope_tag("schematic")

        # Gold highlight strip on the bottom strand ("one strand still held a usable partner")
        gold_bar = RoundedRectangle(
            corner_radius=0.08,
            width=chrom.width,
            height=0.72,
            stroke_color=GOLD,
            stroke_width=4.0,
            fill_color=GOLD,
            fill_opacity=0.22,
        ).move_to([0, left.bot_row.get_center()[1], 0])

        self.add(chrom, tag)
        # Begin highlighting the intact lower partner strand right as the narration recalls the first film
        self.play(Create(gold_bar), run_time=2.0)
        self.at("while one strand")
        self.play(gold_bar.animate.set_fill(opacity=0.30), run_time=2.2)

        # Red flash cuts across both rows
        self.at("when a break")
        flash = Line([0, 1.85, 0], [0, -1.45, 0], color=RED, stroke_width=10)
        flash_glow = Line([0, 1.85, 0], [0, -1.45, 0], color=RED, stroke_width=24).set_opacity(0.35)
        self.play(FadeIn(flash_glow, run_time=0.2), Create(flash, run_time=0.5))
        # Crack begins opening along the flash as the intact gold partner loses continuity
        self.play(
            left.animate.shift(LEFT * 0.25),
            right.animate.shift(RIGHT * 0.25),
            gold_bar.animate.shift(LEFT * 0.25).set_opacity(0.45),
            run_time=2.6,
        )

        # Left and right pieces drift apart; gold partner stops at the gap
        self.at("separates into")
        gold_left = RoundedRectangle(
            corner_radius=0.08,
            width=left.width,
            height=0.72,
            stroke_color=GOLD,
            stroke_width=4.0,
            fill_color=GOLD,
            fill_opacity=0.22,
        ).move_to([left.get_center()[0] - 1.10, left.bot_row.get_center()[1], 0])
        self.play(
            FadeOut(flash),
            FadeOut(flash_glow),
            left.animate.shift(LEFT * 1.10),
            right.animate.shift(RIGHT * 1.10),
            Transform(gold_bar, gold_left),
            run_time=2.2,
        )

        # Red question mark expands between the ends as the gap widens
        self.at("no continuous")
        q_mark = T("?", size=72, color=RED, weight=BOLD).move_to([0, 0.2, 0])
        self.play(
            FadeOut(gold_bar, run_time=0.5),
            GrowFromCenter(q_mark, run_time=1.8),
            left.animate.shift(LEFT * 0.32),
            right.animate.shift(RIGHT * 0.32),
            run_time=2.2,
        )

        # Two moving arrows: one curves ends together, one searches outward
        self.at("work with those ends")
        arc_join = CurvedArrow(
            [-1.35, 1.2, 0], [1.35, 1.2, 0], angle=-0.75, color=TEAL, stroke_width=7, tip_length=0.26
        )
        arc_join_rev = CurvedArrow(
            [1.35, 1.2, 0], [-1.35, 1.2, 0], angle=0.75, color=TEAL, stroke_width=7, tip_length=0.26
        )
        self.play(
            Create(arc_join),
            Create(arc_join_rev),
            left.animate.shift(RIGHT * 0.36),
            right.animate.shift(LEFT * 0.36),
            run_time=1.6,
        )

        self.at("search for matching")
        search_arrow = Arrow(
            [0.35, -0.85, 0], [3.8, -2.55, 0], color=GOLD, stroke_width=7.5, buff=0.0, max_tip_length_to_length_ratio=0.10
        )
        self.play(
            GrowArrow(search_arrow),
            right.animate.shift(RIGHT * 0.32),
            run_time=2.0,
        )
        self.finish()


# ------------------------------------------------------------------ s02_title
class S02Title(TitleCard):
    LESSON = "DNA Repair and Recombination"
    TITLE = "Two Ways to Mend a Broken Chromosome"


# ------------------------------------------------------------------ s03_choice
def build_fork_stage():
    """Shared forked-path backdrop for s03_choice and s11_compare."""
    top_break = make_broken_pair(gap=1.1, scale_x=0.75, block_h=0.34, row_gap=0.12, center=(0, 2.55, 0))
    left_box = RoundedRectangle(
        corner_radius=0.22, width=5.9, height=3.8, stroke_color=TEAL, stroke_width=2.5,
        fill_color=TEAL, fill_opacity=0.05,
    ).move_to([-3.2, -0.75, 0])
    right_box = RoundedRectangle(
        corner_radius=0.22, width=5.9, height=3.8, stroke_color=GOLD, stroke_width=2.5,
        fill_color=GOLD, fill_opacity=0.05,
    ).move_to([3.2, -0.75, 0])
    arr_l = Arrow([top_break.get_bottom()[0] - 0.5, 1.85, 0], [-3.2, 1.25, 0], color=TEAL, stroke_width=4, buff=0.05)
    arr_r = Arrow([top_break.get_bottom()[0] + 0.5, 1.85, 0], [3.2, 1.25, 0], color=GOLD, stroke_width=4, buff=0.05)
    return top_break, left_box, right_box, arr_l, arr_r


class S03Choice(SpokenScene):
    def construct(self):
        top_break, left_box, right_box, arr_l, arr_r = build_fork_stage()
        tag = scope_tag("schematic")
        h_left = T("join ends", size=32, color=TEAL, weight=BOLD).move_to([-3.2, 0.72, 0])
        h_right = T("copy a template", size=32, color=GOLD, weight=BOLD).move_to([3.2, 0.72, 0])

        # Left branch broken ends
        l_ends = make_broken_pair(gap=1.35, scale_x=0.52, block_h=0.34, row_gap=0.12, center=(-3.2, -0.7, 0))
        # Right branch broken ends + gold track behind gap
        r_ends = make_broken_pair(gap=1.35, scale_x=0.52, block_h=0.34, row_gap=0.12, center=(3.2, -0.35, 0))
        r_gold = make_duplex_segment(
            [w * 0.52 for w in ALL_WIDTHS], block_h=0.32, row_gap=0.12, color=GOLD, fill_opacity=0.55
        ).move_to([3.2, -1.55, 0])
        r_gold_lab = T("sister chromatid", size=26, color=GOLD).move_to([3.2, -2.35, 0])

        selector = RoundedRectangle(
            corner_radius=0.06, width=5.5, height=0.18, stroke_color=TEAL, stroke_width=2,
            fill_color=TEAL, fill_opacity=0.92,
        ).move_to([-3.2, 1.16, 0])

        self.add(top_break, tag)
        # Open the left fork arrow as the narrator introduces the two choices
        self.play(GrowArrow(arr_l), run_time=1.3)
        self.at("join its ends")
        self.play(
            FadeIn(left_box), FadeIn(h_left), FadeIn(l_ends),
            run_time=1.0,
        )

        self.at("copy a matching")
        self.play(
            GrowArrow(arr_r), FadeIn(right_box), FadeIn(h_right), FadeIn(r_ends),
            run_time=1.0,
        )
        r_gold_start = r_gold.copy().shift(RIGHT * 2.2).set_opacity(0.0)
        self.play(Transform(r_gold_start, r_gold), run_time=1.1)
        self.remove(r_gold_start)
        self.add(r_gold)

        # Non-homologous end joining: selector highlights left, ends curve toward each other
        self.at("end joining")
        self.play(Create(selector), run_time=0.6)
        self.play(
            l_ends.left.animate.rotate(-0.18).shift(RIGHT * 0.38 + DOWN * 0.1),
            l_ends.right.animate.rotate(0.18).shift(LEFT * 0.38 + DOWN * 0.1),
            run_time=1.8,
        )

        # Homologous recombination: selector slides to right, sister chromatid shifts into view and label appears
        self.at("Homologous recombination")
        self.play(
            selector.animate.move_to([3.2, 1.16, 0]),
            r_gold.animate.shift(LEFT * 0.35),
            run_time=1.2,
        )
        self.at("sister chromatid")
        self.play(
            FadeIn(r_gold_lab, shift=UP * 0.1),
            r_gold.animate.shift(RIGHT * 0.35),
            run_time=1.0,
        )

        # Neither name guarantees one outcome
        self.at("Neither name")
        q_l = T("?", size=38, color=TEXT, weight=BOLD).move_to([-3.2, -2.15, 0])
        q_r = T("?", size=38, color=TEXT, weight=BOLD).move_to([3.2, 0.18, 0])
        self.play(
            FadeIn(q_l),
            FadeIn(q_r),
            selector.animate.move_to([-3.2, 1.16, 0]),
            l_ends.left.animate.shift(LEFT * 0.25),
            l_ends.right.animate.shift(RIGHT * 0.25),
            run_time=1.8,
        )

        # Ends' condition and available template shape what happens next
        self.at("condition")
        self.play(
            l_ends.left.animate.shift(RIGHT * 0.35),
            l_ends.right.animate.shift(LEFT * 0.35),
            r_gold.animate.shift(UP * 0.34),
            selector.animate.move_to([3.2, 1.16, 0]),
            run_time=2.2,
        )
        self.play(
            l_ends.left.animate.shift(LEFT * 0.35),
            l_ends.right.animate.shift(RIGHT * 0.35),
            r_gold.animate.shift(DOWN * 0.34),
            FadeOut(selector),
            run_time=1.8,
        )
        self.finish()


# ------------------------------------------------------------------ s04_join
class S04Join(SpokenScene):
    def construct(self):
        heading = T("end joining", size=34, color=TEAL, weight=BOLD).move_to([0, 3.25, 0])
        tag = scope_tag("schematic")
        status = T("compatible ends", size=28, color=TEXT).move_to([0, 2.30, 0])

        ends = make_broken_pair(gap=2.2, scale_x=0.95, block_h=0.56, row_gap=0.20, center=(0, -0.1, 0))
        ku_l = make_ku_cuff("left", height=1.75, depth=0.65, color=TEAL, label_text="Ku")
        ku_r = make_ku_cuff("right", height=1.75, depth=0.65, color=TEAL, label_text="Ku")
        ku_l.move_to([-6.1, 0.28, 0])
        ku_r.move_to([6.1, 0.28, 0])

        self.add(heading, ends, ku_l, ku_r, tag)
        # Bring Ku cuffs inward from the frame edges toward the broken ends
        self.play(
            ku_l.animate.move_to([-4.6, 0.28, 0]),
            ku_r.animate.move_to([4.6, 0.28, 0]),
            run_time=2.2,
        )

        # Ku rings grip both blue ends
        self.at("rings grip")
        self.play(
            ku_l.animate.move_to([ends.left.get_right()[0] - 0.50, 0.28, 0]),
            ku_r.animate.move_to([ends.right.get_left()[0] + 0.50, 0.28, 0]),
            ends.left.animate.shift(RIGHT * 0.12),
            ends.right.animate.shift(LEFT * 0.12),
            run_time=2.0,
        )

        # Recruit partner shapes bridging the two cuffs
        self.at("recruit partners")
        p_top = RoundedRectangle(
            corner_radius=0.14, width=2.2, height=0.34, stroke_color=TEAL, stroke_width=2.5,
            fill_color=TEAL, fill_opacity=0.6,
        ).move_to([0, 1.30, 0])
        p_bot = RoundedRectangle(
            corner_radius=0.14, width=2.2, height=0.34, stroke_color=TEAL, stroke_width=2.5,
            fill_color=TEAL, fill_opacity=0.6,
        ).move_to([0, -1.55, 0])
        self.play(FadeIn(p_top, shift=DOWN * 0.45), FadeIn(p_bot, shift=UP * 0.45), run_time=1.0)

        # Bring compatible block edges together -> clean join turns green
        self.at("Clean")
        self.play(FadeIn(status, shift=UP * 0.1), run_time=0.45)
        shift_x = 1.05
        self.play(
            ends.left.animate.shift(RIGHT * shift_x),
            ku_l.animate.shift(RIGHT * shift_x),
            ends.right.animate.shift(LEFT * shift_x),
            ku_r.animate.shift(LEFT * shift_x),
            p_top.animate.stretch_to_fit_width(0.65).move_to([0, 1.20, 0]),
            p_bot.animate.stretch_to_fit_width(0.65).move_to([0, -1.35, 0]),
            run_time=1.8,
        )
        green_joint = VGroup(
            RoundedRectangle(
                corner_radius=0.05, width=0.24, height=0.56, stroke_color=GREEN, stroke_width=3,
                fill_color=GREEN, fill_opacity=0.85,
            ).move_to([0, 0.28, 0]),
            RoundedRectangle(
                corner_radius=0.05, width=0.24, height=0.56, stroke_color=GREEN, stroke_width=3,
                fill_color=GREEN, fill_opacity=0.85,
            ).move_to([0, -0.48, 0]),
        )
        exact_lab = T("same sequence", size=28, color=GREEN, weight=BOLD).move_to([0, -2.35, 0])
        self.play(FadeIn(green_joint, run_time=0.7), FadeIn(exact_lab, shift=UP * 0.1, run_time=0.7))

        # Reset to ragged red tips
        self.at("Ends that do")
        rag_ends = make_broken_pair(
            gap=2.2, scale_x=0.95, block_h=0.56, row_gap=0.20, ragged=True, center=(0, -0.1, 0)
        )
        ku_l_back = make_ku_cuff("left", height=1.75, depth=0.65, color=TEAL, label_text="Ku").move_to(
            [rag_ends.left.get_right()[0] - 0.65, 0.28, 0]
        )
        ku_r_back = make_ku_cuff("right", height=1.75, depth=0.65, color=TEAL, label_text="Ku").move_to(
            [rag_ends.right.get_left()[0] + 0.65, 0.28, 0]
        )
        bad_status = T("ragged ends do not fit", size=28, color=RED).move_to([0, 2.30, 0])
        self.play(FadeOut(green_joint), FadeOut(exact_lab), FadeOut(status), run_time=0.20)
        self.play(
            ReplacementTransform(ends, rag_ends),
            Transform(ku_l, ku_l_back),
            Transform(ku_r, ku_r_back),
            p_top.animate.stretch_to_fit_width(2.2).move_to([0, 1.30, 0]),
            p_bot.animate.stretch_to_fit_width(2.2).move_to([0, -1.55, 0]),
            FadeIn(bad_status),
            run_time=0.40,
        )
        self.wait(0.35)

        # Teal tools trim one tip and add one plain block to the other
        self.at("trimming or filling")
        trim_tool = Triangle(stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.8).scale(0.28).rotate(-PI / 2)
        trim_tool.move_to([rag_ends.left.get_right()[0] + 0.15, 0.85, 0])
        fill_tool = Square(side_length=0.42, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.8)
        fill_tool.move_to([rag_ends.right.get_left()[0] - 0.15, -1.05, 0])
        self.play(FadeIn(trim_tool, shift=DOWN * 0.2), FadeIn(fill_tool, shift=UP * 0.2), run_time=0.35)

        # Left ragged tip trimmed off; right gets one plain block added
        red_l_top, red_l_bot = rag_ends.left.top_row[-1], rag_ends.left.bot_row[-1]
        rag_ends.left.top_row.remove(red_l_top)
        rag_ends.left.bot_row.remove(red_l_bot)
        self.add(red_l_top, red_l_bot)

        red_r_top, red_r_bot = rag_ends.right.top_row[0], rag_ends.right.bot_row[0]
        rag_ends.right.top_row.remove(red_r_top)
        rag_ends.right.bot_row.remove(red_r_bot)
        self.add(red_r_top, red_r_bot)
        right_red_tip = VGroup(red_r_top, red_r_bot)

        added_block_x = rag_ends.right.get_left()[0] - 0.06 - 0.30
        added_block = VGroup(
            RoundedRectangle(
                corner_radius=0.06, width=0.60, height=0.56, stroke_color=GREEN, stroke_width=2.5,
                fill_color=GREEN, fill_opacity=0.65,
            ).move_to([added_block_x, 0.28, 0]),
            RoundedRectangle(
                corner_radius=0.06, width=0.60, height=0.56, stroke_color=GREEN, stroke_width=2.5,
                fill_color=GREEN, fill_opacity=0.65,
            ).move_to([added_block_x, -0.48, 0]),
        )
        self.play(
            trim_tool.animate.move_to([rag_ends.left.get_right()[0] - 0.35, -0.1, 0]),
            FadeOut(VGroup(red_l_top, red_l_bot), shift=DOWN * 0.5),
            fill_tool.animate.move_to([added_block_x - 0.25, -0.1, 0]),
            ReplacementTransform(right_red_tip, added_block),
            run_time=0.80,
        )

        # Pull together before ligation -> green joint forms
        self.at("before ligation")
        self.play(FadeOut(trim_tool), FadeOut(fill_tool), run_time=0.25)
        lig_status = T("trimmed and filled before ligation", size=28, color=GREEN).move_to([0, 2.30, 0])
        self.play(
            rag_ends.left.animate.shift(RIGHT * 1.62),
            ku_l.animate.shift(RIGHT * 1.08),
            rag_ends.right.animate.shift(LEFT * 1.04),
            added_block.animate.shift(LEFT * 1.04),
            ku_r.animate.shift(LEFT * 1.04),
            p_top.animate.stretch_to_fit_width(0.65).move_to([0, 1.20, 0]),
            p_bot.animate.stretch_to_fit_width(0.65).move_to([0, -1.35, 0]),
            swap(bad_status, lig_status, run_time=0.30),
            run_time=1.0,
        )
        joint_x = (rag_ends.left.get_right()[0] + added_block.get_left()[0]) / 2
        proc_joint = VGroup(
            RoundedRectangle(
                corner_radius=0.05, width=0.28, height=0.56, stroke_color=GREEN, stroke_width=3,
                fill_color=GREEN, fill_opacity=0.9,
            ).move_to([joint_x, 0.28, 0]),
            RoundedRectangle(
                corner_radius=0.05, width=0.28, height=0.56, stroke_color=GREEN, stroke_width=3,
                fill_color=GREEN, fill_opacity=0.9,
            ).move_to([joint_x, -0.48, 0]),
        )
        proc_lab = T("bases removed or added: sequence can change", size=28, color=TEXT).move_to([0, -2.35, 0])
        self.play(FadeIn(proc_joint, run_time=0.35), FadeIn(proc_lab, shift=UP * 0.1, run_time=0.35))
        self.at("remove or add")
        # Release Ku cuffs and partner bridges after ligation completes
        self.play(
            FadeOut(p_top), FadeOut(p_bot),
            ku_l.animate.shift(LEFT * 1.4),
            ku_r.animate.shift(RIGHT * 1.4),
            run_time=2.4,
        )
        self.finish()


# ------------------------------------------------------------------ s05_cycle
class S05Cycle(SpokenScene):
    def construct(self):
        # Horizontal cell-cycle strip divided at replication boundary x = -0.2
        strip = RoundedRectangle(
            corner_radius=0.18, width=11.8, height=3.6, stroke_color=GREY, stroke_width=2.5,
            fill_color=GREY, fill_opacity=0.05,
        ).move_to([0, 0.25, 0])
        bound_x = -0.2
        boundary = DashedLine([bound_x, 2.05, 0], [bound_x, -1.55, 0], color=GOLD, stroke_width=3.5, dash_length=0.16)
        h_before = T("before replication", size=30, color=TEXT, weight=BOLD).move_to([-3.05, 2.55, 0])
        h_after = T("during and after replication", size=30, color=GOLD, weight=BOLD).move_to([2.85, 2.55, 0])
        tag = scope_tag("schematic")

        # ValueTracker for chromosome progress along the strip [0 -> 1]
        prog = ValueTracker(0.0)
        x_start, x_end = -3.65, 3.65

        def moving_chrom():
            p = prog.get_value()
            cx = x_start + (x_end - x_start) * p
            ch = make_broken_pair(gap=0.50, scale_x=0.34, block_h=0.26, row_gap=0.09, center=(cx, 0.70, 0))
            kl = make_ku_cuff("left", height=0.80, depth=0.26, color=TEAL).move_to([cx - 0.30, 0.70, 0])
            kr = make_ku_cuff("right", height=0.80, depth=0.26, color=TEAL).move_to([cx + 0.30, 0.70, 0])
            return VGroup(ch, kl, kr)

        chrom_mob = always_redraw(moving_chrom)

        # Teal Ku end-joining bar extending beneath the entire strip
        ku_track_bg = Line([-5.5, -1.0, 0], [5.5, -1.0, 0], color=GREY, stroke_width=6).set_opacity(0.35)
        ku_track = always_redraw(
            lambda: Line(
                [-5.5, -1.0, 0],
                [-5.5 + 11.0 * max(0.02, prog.get_value()), -1.0, 0],
                color=TEAL,
                stroke_width=10,
            )
        )
        ku_lab = T("end joining (Ku) active", size=26, color=TEAL).move_to([-2.9, -2.05, 0])

        # Gold sister track that only begins AFTER the replication boundary (never enters left half)
        def sister_track():
            p = prog.get_value()
            cx = x_start + (x_end - x_start) * p
            if cx <= bound_x + 0.15:
                return VGroup()
            frac = float(np.clip((cx - bound_x) / (x_end - bound_x), 0.08, 1.0))
            op = 0.25 + 0.60 * frac
            sis = make_duplex_segment(
                [w * 0.34 for w in ALL_WIDTHS], block_h=0.24, row_gap=0.08, color=GOLD, fill_opacity=op
            )
            sis.set_stroke(opacity=0.35 + 0.65 * frac)
            sis.move_to([max(bound_x + 0.18 + sis.width / 2, cx), -0.25, 0])
            return sis

        sis_mob = always_redraw(sister_track)

        self.add(strip, boundary, h_before, h_after, ku_track_bg, ku_track, chrom_mob, sis_mob, tag)
        self.play(prog.animate.set_value(0.08), run_time=1.2, rate_func=linear)
        self.at("no matching")
        self.play(prog.animate.set_value(0.22), run_time=1.8, rate_func=linear)
        self.at("operate throughout")
        self.play(FadeIn(ku_lab, shift=UP * 0.1), run_time=0.4)
        self.play(prog.animate.set_value(0.36), run_time=2.2, rate_func=linear)

        self.at("Before DNA")
        no_sis_lab = T("no sister chromatid", size=26, color=RED).move_to([-3.05, -0.25, 0])
        self.play(FadeIn(no_sis_lab, shift=UP * 0.1), run_time=0.4)
        self.play(prog.animate.set_value(0.50), run_time=3.5, rate_func=linear)

        self.at("After replication")
        sis_lab = T("sister chromatid available", size=26, color=GOLD).move_to([2.9, -2.05, 0])
        self.play(FadeIn(sis_lab, shift=UP * 0.1), run_time=0.4)
        self.play(prog.animate.set_value(1.0), run_time=3.2, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ s06_predict & s07_pause
def build_two_cells_predict(show_ku=False):
    """Shared builder for s06_predict, s07_pause, and start of s08_reveal."""
    left_cell = make_cell_box([-3.2, 0.3, 0], width=5.6, height=4.4, title="before replication", color=GREY)
    right_cell = make_cell_box([3.2, 0.3, 0], width=5.6, height=4.4, title="after replication", color=GREY)

    l_chrom = make_broken_pair(gap=1.15, scale_x=0.48, block_h=0.34, row_gap=0.12, center=(-3.2, 0.8, 0))
    r_chrom = make_broken_pair(gap=1.15, scale_x=0.48, block_h=0.34, row_gap=0.12, center=(3.2, 0.8, 0))

    l_outline = make_duplex_segment(
        [w * 0.48 for w in ALL_WIDTHS], block_h=0.32, row_gap=0.12, color=GOLD, dashed=True
    ).move_to([-3.2, -0.75, 0])
    r_outline = make_duplex_segment(
        [w * 0.48 for w in ALL_WIDTHS], block_h=0.32, row_gap=0.12, color=GOLD, dashed=True
    ).move_to([3.2, -0.75, 0])

    g = VGroup(left_cell, right_cell, l_chrom, r_chrom, l_outline, r_outline)
    g.left_cell, g.right_cell = left_cell, right_cell
    g.l_chrom, g.r_chrom = l_chrom, r_chrom
    g.l_outline, g.r_outline = l_outline, r_outline

    if show_ku:
        l_ku_l = make_ku_cuff("left", height=1.05, depth=0.36, color=TEAL).move_to([l_chrom.left.get_right()[0] - 0.12, 0.70, 0])
        l_ku_r = make_ku_cuff("right", height=1.05, depth=0.36, color=TEAL).move_to([l_chrom.right.get_left()[0] + 0.12, 0.70, 0])
        r_ku_l = make_ku_cuff("left", height=1.05, depth=0.36, color=TEAL).move_to([r_chrom.left.get_right()[0] - 0.12, 0.70, 0])
        r_ku_r = make_ku_cuff("right", height=1.05, depth=0.36, color=TEAL).move_to([r_chrom.right.get_left()[0] + 0.12, 0.70, 0])
        l_chrom.move_to([-3.2, 0.70, 0])
        r_chrom.move_to([3.2, 0.70, 0])
        ku_all = VGroup(l_ku_l, l_ku_r, r_ku_l, r_ku_r)
        g.add(ku_all)
        g.ku_all = ku_all
    return g


class S06Predict(SpokenScene):
    def construct(self):
        cells = build_two_cells_predict(show_ku=False)
        # Put schematic tag top-center/top-right clear of bottom predict ring
        tag = T("schematic", size=24, color=GREY).move_to([5.45, 3.25, 0])
        q_float = T("?", size=54, color=GOLD, weight=BOLD).move_to([-3.2, 3.05, 0])
        q_card = question_card("Where is a sister available?", y=-3.0, color=GOLD, size=32)

        self.add(tag)
        self.play(FadeIn(cells.left_cell), FadeIn(cells.right_cell), run_time=1.4)
        self.at("one before")
        self.play(FadeIn(cells.l_chrom, lag_ratio=0.15), FadeIn(cells.r_chrom, lag_ratio=0.15), run_time=1.6)

        self.at("Which cell")
        self.play(FadeIn(cells.l_outline), FadeIn(cells.r_outline), FadeIn(q_float), run_time=1.4)
        self.play(q_float.animate.move_to([3.2, 3.05, 0]), run_time=2.0)

        self.at("Watch where")
        self.play(
            FadeIn(q_card, shift=UP * 0.15),
            q_float.animate.move_to([0.0, 3.05, 0]),
            run_time=1.4,
        )
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Where is a sister available?"
    CARD = {"y": -3.0, "color": GOLD, "size": 32}
    RING_AT = (5.8, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        cells = build_two_cells_predict(show_ku=False)
        tag = T("schematic", size=24, color=GREY).move_to([5.45, 3.25, 0])
        q_float = T("?", size=54, color=GOLD, weight=BOLD).move_to([0.0, 3.05, 0])
        pulse(cells.l_outline, base=3.0, amp=1.8, speed=3.5)
        pulse(cells.r_outline, base=3.0, amp=1.8, speed=3.5)
        return VGroup(cells, tag, q_float)


# ------------------------------------------------------------------ s08_reveal
class S08Reveal(SpokenScene):
    def construct(self):
        cells = build_two_cells_predict(show_ku=True)
        tag = T("schematic", size=24, color=GREY).move_to([5.45, 3.25, 0])
        solid_gold = make_duplex_segment(
            [w * 0.48 for w in ALL_WIDTHS], block_h=0.34, row_gap=0.12, color=GOLD, fill_opacity=0.65
        ).move_to([3.2, -0.75, 0])

        self.add(cells.left_cell, cells.right_cell, cells.l_chrom, cells.r_chrom, cells.l_outline, cells.r_outline, cells.ku_all, tag)

        # Reveal solid gold sister only in the right cell
        self.at("each chromosome")
        self.play(ReplacementTransform(cells.r_outline, solid_gold), run_time=1.6)
        self.play(solid_gold.animate.shift(UP * 0.24), run_time=2.4)

        # Homologous recombination useful during/after replication
        self.at("homologous recombination")
        hr_lab = T("homologous recombination", size=28, color=GOLD, weight=BOLD).move_to([3.2, -1.48, 0])
        ku_lab = T("Ku: end joining active", size=26, color=TEAL).move_to([-3.2, 1.54, 0])
        ku_lab_r = T("Ku: end joining active", size=26, color=TEAL).move_to([3.2, 1.54, 0])
        self.play(
            FadeIn(hr_lab, shift=UP * 0.1),
            FadeIn(ku_lab),
            FadeIn(ku_lab_r),
            cells.right_cell.animate.set_stroke(GOLD, width=3.5),
            run_time=0.5,
        )
        # Slide the newly revealed gold sister template up closer behind the broken chromosome
        self.play(solid_gold.animate.shift(UP * 0.24), run_time=1.8)
        self.play(solid_gold.animate.move_to([3.2, -0.30, 0]), run_time=1.6)

        # Broken blue chromosome aligns beside the gold sister
        self.at("aligns beside")
        align_ticks = VGroup(
            DashedLine([3.2 - 0.6, 0.25, 0], [3.2 - 0.6, -0.35, 0], color=GOLD, stroke_width=3.0),
            DashedLine([3.2 + 0.6, 0.25, 0], [3.2 + 0.6, -0.35, 0], color=GOLD, stroke_width=3.0),
        )
        self.play(
            solid_gold.animate.move_to([3.2, -0.25, 0]),
            cells.r_chrom.animate.shift(DOWN * 0.22),
            run_time=1.4,
        )
        self.play(Create(align_ticks), run_time=1.0)

        # Before replication, sister is absent -> collapse empty gold outline into 'no sister yet'
        self.at("sister is absent")
        no_sis = T("no sister yet", size=30, color=RED, weight=BOLD).move_to([-3.2, -0.75, 0])
        self.play(ReplacementTransform(cells.l_outline, no_sis), run_time=1.2)
        unavail = T("sister route unavailable", size=26, color=RED).move_to([-3.2, -1.45, 0])
        self.play(FadeIn(unavail, shift=UP * 0.1), run_time=0.45)
        self.play(
            cells.ku_all[0].animate.shift(RIGHT * 0.08),
            cells.ku_all[1].animate.shift(LEFT * 0.08),
            cells.ku_all[2].animate.shift(RIGHT * 0.08),
            cells.ku_all[3].animate.shift(LEFT * 0.08),
            run_time=1.8,
        )
        self.finish()


# ------------------------------------------------------------------ s09_copy
class S09Copy(SpokenScene):
    def construct(self):
        heading = T("homologous recombination", size=34, color=GOLD, weight=BOLD).move_to([0, 3.25, 0])
        tag = scope_tag("schematic")

        # Broken blue chromosome above; intact gold sister below with identical block widths
        broken = make_broken_pair(gap=2.0, scale_x=0.92, block_h=0.46, row_gap=0.16, center=(0, 1.55, 0))
        sister = make_duplex_segment(
            [w * 0.92 for w in ALL_WIDTHS], block_h=0.46, row_gap=0.16, color=GOLD, fill_opacity=0.58
        ).move_to([0, -1.55, 0])

        self.add(heading, broken, sister, tag)
        self.play(
            broken.animate.move_to([0, 1.35, 0]),
            sister.animate.move_to([0, -1.35, 0]),
            run_time=1.8,
        )

        # Reshape break into single-stranded tails (retract top-left and bottom-right inner blocks)
        self.at("reshapes the break")
        # Create protruding single-stranded blue tails extending inward from the break without overlapping blocks
        tail_l = RoundedRectangle(
            corner_radius=0.06, width=1.05, height=0.32, stroke_color=BLUE, stroke_width=2.5,
            fill_color=BLUE, fill_opacity=0.82,
        ).move_to([-1.0 + 1.05 / 2, broken.left.bot_row.get_center()[1], 0])
        tail_r = RoundedRectangle(
            corner_radius=0.06, width=1.05, height=0.32, stroke_color=BLUE, stroke_width=2.5,
            fill_color=BLUE, fill_opacity=0.82,
        ).move_to([1.0 - 1.05 / 2, broken.right.top_row.get_center()[1], 0])
        self.play(
            FadeOut(broken.left.top_row[-1], shift=LEFT * 0.25),
            FadeOut(broken.right.bot_row[0], shift=RIGHT * 0.25),
            GrowFromEdge(tail_l, LEFT),
            GrowFromEdge(tail_r, RIGHT),
            sister.animate.shift(UP * 0.10),
            run_time=2.2,
        )

        # Teal beads labeled 'recombinase' coat one tail
        self.at("coats a tail")
        beads = VGroup(
            *[
                Circle(radius=0.11, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.90).move_to(
                    [tail_l.get_left()[0] + 0.16 + i * 0.24, tail_l.get_center()[1], 0]
                )
                for i in range(4)
            ]
        )
        recomb_lab = T("recombinase", size=28, color=TEAL, weight=BOLD).next_to(beads, DOWN, buff=0.18)
        coated_tail = VGroup(tail_l, beads, recomb_lab)
        self.play(
            FadeIn(beads, lag_ratio=0.15),
            FadeIn(recomb_lab, shift=UP * 0.1),
            coated_tail.animate.shift(RIGHT * 0.22),
            run_time=1.4,
        )

        # Search along the gold sister, pause at matching block pattern
        self.at("search the gold")
        self.play(coated_tail.animate.move_to([-1.8, -0.25, 0]), run_time=0.9)
        self.play(coated_tail.animate.move_to([1.2, -0.25, 0]), run_time=1.0)

        self.at("matching")
        self.play(coated_tail.animate.move_to([-0.55, -0.25, 0]), run_time=0.9)

        # Tail invades: tucks beside the gold sister (displacing top gold blocks locally)
        self.at("tail invades")
        self.play(FadeOut(recomb_lab), FadeOut(beads, lag_ratio=0.1), run_time=0.3)
        self.play(
            tail_l.animate.move_to([-0.90, sister.top_row.get_center()[1] + 0.26, 0]),
            sister.top_row[4:7].animate.shift(UP * 0.35),
            run_time=0.95,
        )

        # Primes new green DNA while a gold template highlight bracket tracks across the sister
        self.at("primes new green")
        synth = ValueTracker(0.0)
        start_x = tail_l.get_right()[0]
        end_x = start_x + 1.96
        y_green = tail_l.get_center()[1]
        y_sister = sister.get_center()[1]

        green_track = always_redraw(
            lambda: RoundedRectangle(
                corner_radius=0.05,
                width=max(0.06, (end_x - start_x) * synth.get_value()),
                height=0.34,
                stroke_color=GREEN,
                stroke_width=2.5,
                fill_color=GREEN,
                fill_opacity=0.88,
            ).move_to([start_x + max(0.06, (end_x - start_x) * synth.get_value()) / 2, y_green, 0])
        )
        guide_frame = always_redraw(
            lambda: RoundedRectangle(
                corner_radius=0.08,
                width=0.95,
                height=1.18,
                stroke_color=GOLD,
                stroke_width=5.0,
                fill_color=GOLD,
                fill_opacity=0.35,
            ).move_to([start_x + (end_x - start_x) * synth.get_value(), y_sister, 0])
        )
        copy_lab = T("copied from sister template", size=28, color=GREEN, weight=BOLD).move_to([0, -2.55, 0])
        self.add(green_track, guide_frame)
        self.play(FadeIn(copy_lab, shift=UP * 0.1), run_time=0.3)
        self.play(synth.animate.set_value(1.0), run_time=4.8, rate_func=linear)

        # Replace live-redrawn mobjects with static mobjects before moving copied green DNA up to the broken chromosome
        fixed_green = RoundedRectangle(
            corner_radius=0.05, width=1.96, height=0.34, stroke_color=GREEN, stroke_width=2.5,
            fill_color=GREEN, fill_opacity=0.88,
        ).move_to([start_x + 1.96 / 2, y_green, 0])
        self.remove(green_track, guide_frame)
        self.add(fixed_green)

        # Keeps the sister's sequence across the gap
        self.at("keeps the sister")
        self.play(FadeOut(tail_l), FadeOut(tail_r), run_time=0.25)
        repaired_top = RoundedRectangle(
            corner_radius=0.05, width=1.96, height=0.32, stroke_color=GREEN, stroke_width=2.5,
            fill_color=GREEN, fill_opacity=0.88,
        ).move_to([0.0, broken.left.top_row.get_center()[1], 0])
        self.play(
            fixed_green.animate.move_to([0.0, broken.left.bot_row.get_center()[1], 0]),
            GrowFromEdge(repaired_top, LEFT),
            sister.top_row[4:7].animate.shift(DOWN * 0.35),
            run_time=1.1,
        )
        self.finish()


# ------------------------------------------------------------------ s10_finish
class S10Finish(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")

        def make_extended_state(y_off=0.0):
            left_b = make_duplex_segment(
                [w * 0.56 for w in HALF_WIDTHS_L], block_h=0.26, row_gap=0.08, color=BLUE, fill_opacity=0.55
            ).move_to([-2.4, y_off + 0.55, 0])
            right_b = make_duplex_segment(
                [w * 0.56 for w in HALF_WIDTHS_R], block_h=0.26, row_gap=0.08, color=BLUE, fill_opacity=0.55
            ).move_to([2.4, y_off + 0.55, 0])
            gold_s = make_duplex_segment(
                [w * 0.56 for w in ALL_WIDTHS], block_h=0.26, row_gap=0.08, color=GOLD, fill_opacity=0.52
            ).move_to([0, y_off - 0.55, 0])
            ext_green = RoundedRectangle(
                corner_radius=0.04, width=1.6, height=0.20, stroke_color=GREEN, stroke_width=2.5,
                fill_color=GREEN, fill_opacity=0.85,
            ).move_to([0.0, y_off - 0.12, 0])
            tether = Line(
                [left_b.get_right()[0], left_b.bot_row.get_center()[1], 0],
                ext_green.get_left(),
                color=BLUE, stroke_width=5,
            )
            g = VGroup(left_b, right_b, gold_s, ext_green, tether)
            g.left_b, g.right_b, g.gold_s, g.ext_green, g.tether = left_b, right_b, gold_s, ext_green, tether
            return g

        center_state = make_extended_state(0.0)
        self.add(center_state, tag)
        self.play(center_state.animate.shift(UP * 0.55), run_time=3.2)

        # Split into upper route (strand lifts away and pairs) and lower route (crossed junctions)
        self.at("Often the")
        upper = make_extended_state(1.85)
        lower = make_extended_state(-1.60)
        h_upper = T("strand leaves donor and pairs", size=28, color=GREEN, weight=BOLD).move_to([0, 3.22, 0])
        self.play(
            ReplacementTransform(center_state, upper),
            FadeIn(lower, shift=DOWN * 0.4),
            FadeIn(h_upper, run_time=0.45),
            run_time=1.3,
        )

        # Upper route: extended blue-green strand lifts away from gold and pairs with other blue end
        self.at("pairs with")
        lifted_green = RoundedRectangle(
            corner_radius=0.04, width=1.8, height=0.22, stroke_color=GREEN, stroke_width=2.5,
            fill_color=GREEN, fill_opacity=0.85,
        ).move_to([0.0, 1.85 + 0.35, 0])
        new_tether = Line(
            [upper.left_b.get_right()[0], upper.left_b.bot_row.get_center()[1], 0],
            lifted_green.get_left(),
            color=BLUE, stroke_width=5,
        )
        pair_bridge = RoundedRectangle(
            corner_radius=0.04, width=1.8, height=0.22, stroke_color=GREEN, stroke_width=2.5,
            fill_color=GREEN, fill_opacity=0.75,
        ).move_to([0.0, 1.85 + 0.72, 0])
        self.play(
            Transform(upper.ext_green, lifted_green),
            Transform(upper.tether, new_tether),
            FadeIn(pair_bridge, shift=LEFT * 0.2),
            run_time=1.5,
        )

        # Lower route: form two simple crossed junction icons labeled 'crossed junctions, schematic'
        self.at("Another branch")
        j1 = VGroup(
            Line([-0.85, -0.97, 0], [-0.45, -2.03, 0], color=BLUE, stroke_width=5),
            Line([-0.45, -0.97, 0], [-0.85, -2.03, 0], color=GOLD, stroke_width=5),
        )
        j2 = VGroup(
            Line([0.45, -0.97, 0], [0.85, -2.03, 0], color=GOLD, stroke_width=5),
            Line([0.85, -0.97, 0], [0.45, -2.03, 0], color=BLUE, stroke_width=5),
        )
        j_lab = T("crossed junctions, schematic", size=28, color=GOLD, weight=BOLD).move_to([0, -3.02, 0])
        self.play(Create(j1), Create(j2), run_time=1.1)
        self.play(FadeIn(j_lab, shift=UP * 0.1), run_time=0.35)

        # Both begin by using matching DNA as information
        self.at("Both begin")
        info_lab = T("both copy matching DNA", size=26, color=GREEN, weight=BOLD).move_to([0, 0.05, 0])
        self.play(FadeIn(info_lab, shift=UP * 0.1), run_time=0.3)
        self.play(
            upper.ext_green.animate.stretch_to_fit_width(2.02, about_edge=LEFT),
            pair_bridge.animate.stretch_to_fit_width(2.02, about_edge=LEFT),
            lower.ext_green.animate.stretch_to_fit_width(1.82, about_edge=LEFT),
            rate_func=there_and_back,
            run_time=2.5,
        )
        self.finish()


# ------------------------------------------------------------------ s11_compare
class S11Compare(SpokenScene):
    def construct(self):
        top_break, left_box, right_box, arr_l, arr_r = build_fork_stage()
        tag = scope_tag("schematic")
        h_left = T("end joining", size=30, color=TEAL, weight=BOLD).move_to([-3.2, 0.75, 0])
        h_right = T("homologous recombination", size=30, color=GOLD, weight=BOLD).move_to([3.2, 0.75, 0])

        self.add(top_break, tag)
        self.play(
            GrowArrow(arr_l), GrowArrow(arr_r),
            FadeIn(left_box), FadeIn(right_box),
            FadeIn(h_left), FadeIn(h_right),
            run_time=1.6,
        )

        # Three end-joining outcomes: exact green joint, short deletion, short addition (all 'possible')
        def ej_row(y, kind):
            lb = make_duplex_segment([0.52], block_h=0.22, row_gap=0.05, color=BLUE, fill_opacity=0.55)
            rb = make_duplex_segment([0.52], block_h=0.22, row_gap=0.05, color=BLUE, fill_opacity=0.55)
            if kind == "exact":
                mid = VGroup(
                    RoundedRectangle(corner_radius=0.04, width=0.18, height=0.22, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.85).move_to([0, 0.135, 0]),
                    RoundedRectangle(corner_radius=0.04, width=0.18, height=0.22, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.85).move_to([0, -0.135, 0]),
                )
                lb.next_to(mid, LEFT, buff=0.03)
                rb.next_to(mid, RIGHT, buff=0.03)
                txt = fit_text("exact joint (possible)", max_w=3.35, size=24, color=GREEN, max_lines=1)
            elif kind == "del":
                lb = make_duplex_segment([0.34], block_h=0.22, row_gap=0.05, color=BLUE, fill_opacity=0.55)
                mid = VGroup(
                    RoundedRectangle(corner_radius=0.04, width=0.14, height=0.22, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.75).move_to([0, 0.135, 0]),
                    RoundedRectangle(corner_radius=0.04, width=0.14, height=0.22, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.75).move_to([0, -0.135, 0]),
                )
                lb.next_to(mid, LEFT, buff=0.03)
                rb.next_to(mid, RIGHT, buff=0.03)
                txt = fit_text("short deletion (possible)", max_w=3.35, size=24, color=TEXT, max_lines=1)
            else:
                mid = VGroup(
                    RoundedRectangle(corner_radius=0.04, width=0.38, height=0.22, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.85).move_to([0, 0.135, 0]),
                    RoundedRectangle(corner_radius=0.04, width=0.38, height=0.22, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.85).move_to([0, -0.135, 0]),
                )
                lb.next_to(mid, LEFT, buff=0.03)
                rb.next_to(mid, RIGHT, buff=0.03)
                txt = fit_text("short addition (possible)", max_w=3.35, size=24, color=TEXT, max_lines=1)
            bar = VGroup(lb, mid, rb).move_to([-5.08, y, 0])
            txt.move_to([-4.15, y, 0], aligned_edge=LEFT)
            return VGroup(bar, txt)

        r1 = ej_row(0.05, "exact")
        r2 = ej_row(-0.95, "del")
        r3 = ej_row(-1.95, "add")

        self.at("End joining")
        self.play(FadeIn(r1, shift=RIGHT * 0.15), run_time=0.25)
        self.at("processing may")
        self.play(FadeIn(r2, shift=RIGHT * 0.15), FadeIn(r3, shift=RIGHT * 0.15), run_time=0.25)

        # Homologous side: green restoration only while gold sister is present
        self.at("Homologous recombination")
        hr_broken = make_broken_pair(gap=1.1, scale_x=0.46, block_h=0.30, row_gap=0.10, center=(3.2, -0.15, 0))
        hr_gold = make_duplex_segment(
            [w * 0.46 for w in ALL_WIDTHS], block_h=0.28, row_gap=0.10, color=GOLD, fill_opacity=0.6
        ).move_to([3.2, -1.25, 0])
        hr_green = VGroup(
            RoundedRectangle(corner_radius=0.04, width=1.06, height=0.30, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.85).move_to([3.2, 0.05, 0]),
            RoundedRectangle(corner_radius=0.04, width=1.06, height=0.30, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.85).move_to([3.2, -0.35, 0]),
        )
        hr_lab = T("restored from sister", size=26, color=GREEN).move_to([3.2, -2.05, 0])
        self.play(FadeIn(hr_broken), FadeIn(hr_gold), run_time=0.8)
        self.play(FadeIn(hr_green), FadeIn(hr_lab), run_time=0.9)

        self.at("only when that")
        hr_no_sis = T("no template: cannot restore", size=26, color=RED).move_to([3.2, -2.05, 0])
        hr_empty = make_duplex_segment(
            [w * 0.46 for w in ALL_WIDTHS], block_h=0.28, row_gap=0.10, color=GOLD, dashed=True
        ).move_to([3.2, -1.25, 0])
        self.play(
            FadeOut(hr_green),
            ReplacementTransform(hr_gold, hr_empty),
            swap(hr_lab, hr_no_sis, run_time=0.7),
            run_time=1.0,
        )

        # Replace headers with the two questions: 'ends joinable?' and 'template available?'
        self.at("not a contest")
        q_left = T("ends joinable?", size=30, color=TEAL, weight=BOLD).move_to([-3.2, 0.75, 0])
        q_right = T("template available?", size=30, color=GOLD, weight=BOLD).move_to([3.2, 0.75, 0])
        self.play(swap(h_left, q_left, run_time=0.6), swap(h_right, q_right, run_time=0.6), run_time=0.65)
        check_frame = SurroundingRectangle(left_box, color=TEAL, stroke_width=5, buff=0.06, corner_radius=0.25)
        right_frame = SurroundingRectangle(right_box, color=GOLD, stroke_width=5, buff=0.06, corner_radius=0.25)
        self.play(Create(check_frame), run_time=0.8)
        self.play(FadeOut(check_frame), Create(right_frame), run_time=1.6)

        self.at("available information")
        self.play(
            hr_empty.animate.shift(UP * 0.40),
            FadeOut(right_frame),
            run_time=1.5,
        )
        self.play(hr_empty.animate.shift(DOWN * 0.40), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------ s12_close
class S12Close(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")

        # Start with converging tracks from left & right that merge into one repaired blue chromosome
        l_arm = make_duplex_segment([w * 0.78 for w in HALF_WIDTHS_L], block_h=0.44, row_gap=0.14, color=BLUE, fill_opacity=0.58)
        r_arm = make_duplex_segment([w * 0.78 for w in HALF_WIDTHS_R], block_h=0.44, row_gap=0.14, color=BLUE, fill_opacity=0.58)
        joint = VGroup(
            RoundedRectangle(corner_radius=0.05, width=0.52, height=0.44, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.85).move_to([0, 0.29, 0]),
            RoundedRectangle(corner_radius=0.05, width=0.52, height=0.44, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.85).move_to([0, -0.29, 0]),
        )
        l_arm.next_to(joint, LEFT, buff=0.05)
        r_arm.next_to(joint, RIGHT, buff=0.05)
        repaired = VGroup(l_arm, joint, r_arm).move_to([0, -0.35, 0])

        gold_sis = make_duplex_segment(
            [w * 0.78 for w in ALL_WIDTHS], block_h=0.40, row_gap=0.12, color=GOLD, fill_opacity=0.52
        ).move_to([0, -2.05, 0])

        # Initial split positions that merge together
        l_start = l_arm.copy().shift(LEFT * 1.4 + UP * 1.3)
        r_start = r_arm.copy().shift(RIGHT * 1.4 + UP * 1.3)
        self.add(l_start, r_start, gold_sis, tag)

        self.at("ask what remains")
        self.play(
            Transform(l_start, l_arm),
            Transform(r_start, r_arm),
            FadeIn(joint),
            run_time=2.1,
        )
        self.remove(l_start, r_start)
        self.add(repaired)

        # Teal bracket surrounds joined ends
        self.at("joinable ends")
        teal_br = make_bracket(joint, side=UP, color=TEAL, buff=0.18, tick=0.22, stroke_width=5)
        teal_q = T("two joinable ends?", size=28, color=TEAL, weight=BOLD).next_to(teal_br, UP, buff=0.16)
        self.play(Create(teal_br), FadeIn(teal_q, shift=UP * 0.1), run_time=0.3)
        self.play(
            l_arm.animate.shift(RIGHT * 0.14),
            r_arm.animate.shift(LEFT * 0.14),
            rate_func=there_and_back,
            run_time=1.6,
        )

        # Gold bracket surrounds intact sister template
        self.at("intact sister")
        gold_br = make_bracket(gold_sis, side=DOWN, color=GOLD, buff=0.14, tick=0.18, stroke_width=5)
        gold_q = T("intact sister nearby?", size=28, color=GOLD, weight=BOLD).next_to(gold_br, DOWN, buff=0.16)
        self.play(
            Create(gold_br),
            FadeIn(gold_q, shift=UP * 0.1),
            gold_sis.animate.shift(UP * 0.22),
            run_time=1.0,
        )
        self.play(gold_sis.animate.shift(DOWN * 0.22), run_time=0.8)

        # Both brackets transform into centered prompt 'What information remains?' while repaired moves beneath
        self.at("Those questions")
        prompt = T("What information remains?", size=42, color=GOLD, weight=BOLD).move_to([0, 1.85, 0])
        self.play(FadeOut(teal_q), FadeOut(gold_q), run_time=0.35)
        self.play(
            ReplacementTransform(VGroup(teal_br, gold_br), prompt),
            run_time=1.0,
        )
        # Slow continuous glide of the repaired chromosome + sister beneath the centered prompt
        both_chroms = VGroup(repaired, gold_sis)
        self.play(both_chroms.animate.shift(RIGHT * 0.8), run_time=3.1, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ s13_end
class S13End(EndCard):
    LINE = "A broken chromosome can join its ends or copy a matching template."
