"""
How DNA Chooses a Repair Route — Animation for biochemistrypedia.com

COLOUR MAP (one colour per concept, held across all 11 scenes):
- BLUE   (#58C4DD): Intact DNA base blocks, pairing rungs, and undamaged strands
- RED    (#FC6255): Damage/lesions (warped base, chemical mark, linked pair, mismatch ?, sequence changed)
- GOLD   (#D4A843): Intact partner, trustworthy template, and source pointers
- TEAL   (#3FB8C0): Repair machinery (scanner, eraser tool, clamps, cut markers) and new-strand signal
- GREEN  (#83C167): Newly synthesized replacement base(s) and restored sequence
- TEXT   (#E8EAF0): Primary headings, pathway labels, and questions
- GREY   (#8B93A1): Structural DNA backbone rails and 'schematic' scope tag

CARRIED PICTURE OF THE WORLD:
Two horizontal rows of large paired DNA base blocks (upper and lower rows) linked by vertical
pairing rungs and framed by horizontal backbone rails. Every scene transforms this same duplex.

WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
- s01_hook: 11 paired columns scroll continuously left via phase tracker x_i(t) with smooth edge taper;
  a scanning teal beam sweeps to center, one upper block warps red, and its lower partner gains a gold frame.
- s03_rule: Full-height paired rows restore; a red 'chemical mark' badge sits on an intact blue block inside a
  gold bracket while a teal eraser tool glides across, lifts the badge off, and an intact-backbone pulse runs.
- s04_small: Neighboring columns oscillate in a continuous vertical sine wave dy(i, t); one red block lifts
  out, a gold guide line projects from the intact partner, a green block rises in, and teal clamps seal the rail.
- s05_bulky: Two adjacent upper blocks link red and the upper row bows via a computed Gaussian bump dy(x);
  teal cuts excise a 4-block patch, gold guides project upward, 4 green blocks fill and straighten the row, then turn blue.
- s06_predict: Straightened blue rows hold one mismatched normal pair with a rocking red '?' and two balanced
  'replace?' arrows while a soft white highlight alternates cleanly between upper and lower block.
- s08_reveal: A moving teal ribbon ('new strand') and gold ribbon ('template') stream along the upper/lower
  backbones; the teal stretch peels away past the mismatch, green blocks copy up from gold and turn blue.
- s09_sort: One continuous 14-column duplex runs four left-to-right transformations (reverse, one base,
  short patch, new strand) while gold pointers mark the repaired base (reversal) or intact lower partner (excision).
- s10_consequence: Repaired rows glide continuously along an upper green 'sequence restored' lane while an
  unrepaired red block passes through a schematic replication fork into a paired red 'sequence changed' lane;
  both outcomes keep gliding as the center question 'What information remains?' appears.
"""

from bp_parts import *


# ------------------------------------------------------------------ shared geometry
N_COLS = 11
DX = 1.12
BW = 0.86
BH = 1.18
Y_UP = 1.06
Y_DN = -1.06
Y_RAIL_UP = 1.78
Y_RAIL_DN = -1.78


def make_block(color=BLUE, w=BW, h=BH, fill_op=0.30, stroke_w=3.5, radius=0.14):
    """One DNA letter/base block."""
    return RoundedRectangle(
        corner_radius=radius,
        width=w,
        height=h,
        stroke_color=color,
        stroke_width=stroke_w,
        fill_color=color,
        fill_opacity=fill_op,
    )


def make_warped_block(color=RED, w=BW, h=BH, fill_op=0.36, stroke_w=4.0):
    """A pinched/skewed block representing base distortion/damage."""
    pts = [
        [-w * 0.44, h * 0.48, 0],
        [w * 0.48, h * 0.36, 0],
        [w * 0.36, -h * 0.48, 0],
        [-w * 0.48, -h * 0.34, 0],
    ]
    return Polygon(
        *pts,
        stroke_color=color,
        stroke_width=stroke_w,
        fill_color=color,
        fill_opacity=fill_op,
    ).round_corners(0.10)


def col_x(i, n_cols=N_COLS, dx=DX):
    return (i - (n_cols - 1) / 2.0) * dx


def build_duplex(
    n_cols=N_COLS,
    dx=DX,
    bw=BW,
    bh=BH,
    y_up=Y_UP,
    y_dn=Y_DN,
    rail_up=Y_RAIL_UP,
    rail_dn=Y_RAIL_DN,
):
    """Build the carried two-row DNA duplex centered at ORIGIN."""
    x_left = col_x(0, n_cols, dx) - bw * 0.58
    x_right = col_x(n_cols - 1, n_cols, dx) + bw * 0.58
    top_rail = Line([x_left, rail_up, 0], [x_right, rail_up, 0], color=GREY, stroke_width=5)
    bot_rail = Line([x_left, rail_dn, 0], [x_right, rail_dn, 0], color=GREY, stroke_width=5)
    upper = VGroup()
    lower = VGroup()
    rungs = VGroup()
    for i in range(n_cols):
        x = col_x(i, n_cols, dx)
        ub = make_block(BLUE, bw, bh).move_to([x, y_up, 0])
        lb = make_block(BLUE, bw, bh).move_to([x, y_dn, 0])
        rg = Line(
            [x, y_dn + bh / 2 + 0.04, 0],
            [x, y_up - bh / 2 - 0.04, 0],
            color=BLUE,
            stroke_width=3.0,
            stroke_opacity=0.45,
        )
        upper.add(ub)
        lower.add(lb)
        rungs.add(rg)
    g = VGroup(top_rail, bot_rail, rungs, upper, lower)
    g.top_rail = top_rail
    g.bot_rail = bot_rail
    g.rungs = rungs
    g.upper = upper
    g.lower = lower
    return g


def gold_bracket_around(mob, pad=0.14, color=GOLD, stroke_w=4.5):
    """Two clean corner brackets around a block (without crossing its interior)."""
    l = mob.get_left()[0] - pad
    r = mob.get_right()[0] + pad
    t = mob.get_top()[1] + pad * 0.6
    b = mob.get_bottom()[1] - pad * 0.6
    arm = 0.20
    left_b = VMobject(color=color, stroke_width=stroke_w)
    left_b.set_points_as_corners([[l + arm, t, 0], [l, t, 0], [l, b, 0], [l + arm, b, 0]])
    right_b = VMobject(color=color, stroke_width=stroke_w)
    right_b.set_points_as_corners([[r - arm, t, 0], [r, t, 0], [r, b, 0], [r - arm, b, 0]])
    return VGroup(left_b, right_b)


def make_eraser_tool():
    """Teal schematic repair tool with a sloped eraser edge."""
    body = RoundedRectangle(
        corner_radius=0.18,
        width=1.45,
        height=0.72,
        stroke_color=TEAL,
        stroke_width=4,
        fill_color=TEAL,
        fill_opacity=0.25,
    )
    tip = Polygon(
        [-0.72, -0.36, 0],
        [-0.25, -0.36, 0],
        [-0.42, -0.56, 0],
        [-0.72, -0.56, 0],
        stroke_color=TEAL,
        stroke_width=3.5,
        fill_color=TEAL,
        fill_opacity=0.45,
    )
    return VGroup(body, tip)


def make_cut_marker(x, y):
    """Small teal wedge cut marker pointing down onto the backbone."""
    w = Polygon(
        [x - 0.16, y + 0.34, 0],
        [x + 0.16, y + 0.34, 0],
        [x, y + 0.04, 0],
        stroke_color=TEAL,
        stroke_width=3,
        fill_color=TEAL,
        fill_opacity=0.65,
    )
    return w


def make_gold_pointer(x, y, point_up=True):
    """Small gold triangle pointer."""
    dy = 0.26 if point_up else -0.26
    return Polygon(
        [x - 0.15, y - dy * 0.5, 0],
        [x + 0.15, y - dy * 0.5, 0],
        [x, y + dy * 0.5, 0],
        stroke_color=GOLD,
        stroke_width=2.5,
        fill_color=GOLD,
        fill_opacity=0.85,
    )


def moving_ribbon_ticks(x0, x1, y, color, tracker, n_ticks=14, stroke_w=7):
    """A ribbon bar plus bold moving chevron ticks driven by a phase ValueTracker."""
    bar = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=stroke_w)
    span = x1 - x0

    def mk():
        g = VGroup()
        ph = tracker.get_value()
        step = span / n_ticks
        for k in range(n_ticks):
            tx = x0 + ((k * step + ph) % span)
            vis = 0.95 if (x0 + 0.16 < tx < x1 - 0.16) else 0.0
            tk = VMobject(color=TEXT, stroke_width=3.5, stroke_opacity=vis)
            tk.set_points_as_corners([
                [tx - 0.13, y - 0.10, 0],
                [tx + 0.07, y, 0],
                [tx - 0.13, y + 0.10, 0],
            ])
            g.add(tk)
        return g

    ticks = always_redraw(mk)
    return bar, ticks


def mismatch_backdrop(rock_t=None, alt_t=None, show_arrows=True):
    """Shared mismatch picture for S06Predict end and S07Pause."""
    dup = build_duplex()
    mid = 5
    dup.rungs[mid].set_stroke(opacity=0.0)
    qmark = T("?", size=50, color=RED, weight=BOLD).move_to([0, 0, 0])

    if rock_t is not None:
        qmark.add_updater(lambda m, dt: m.rotate_to(0.18 * np.sin(2.4 * rock_t.get_value())) if False else None)

    g = VGroup(dup, qmark)
    g.dup = dup
    g.qmark = qmark
    if show_arrows:
        arr_up = Arrow([0, 2.35, 0], [0, 1.86, 0], buff=0, color=TEXT, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        arr_dn = Arrow([0, -2.35, 0], [0, -1.86, 0], buff=0, color=TEXT, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        lab_up = T("replace?", size=28, color=TEXT).next_to(arr_up, UP, buff=0.14)
        lab_dn = T("replace?", size=28, color=TEXT).next_to(arr_dn, DOWN, buff=0.14)
        g.add(arr_up, arr_dn, lab_up, lab_dn)
        g.arrows = VGroup(arr_up, arr_dn, lab_up, lab_dn)
    return g


# ------------------------------------------------------------------ S01
class S01Hook(SpokenScene):
    def construct(self):
        # Continuous conveyor of 11 visible paired columns scrolling left inside [-6.0, 6.0].
        scroll = ValueTracker(0.0)
        span = N_COLS * DX
        half_span = span / 2.0
        target_id = 14  # enters from the right and settles at x = 0 at scene end

        top_rail = Line([-5.95, Y_RAIL_UP, 0], [5.95, Y_RAIL_UP, 0], color=GREY, stroke_width=5)
        bot_rail = Line([-5.95, Y_RAIL_DN, 0], [5.95, Y_RAIL_DN, 0], color=GREY, stroke_width=5)
        self.add(top_rail, bot_rail, scope_tag("schematic"))

        # Track whether the target column has warped red and partner gained gold
        warp_t = ValueTracker(0.0)
        rung_boost = ValueTracker(0.0)
        scan_x = ValueTracker(-5.2)
        scan_alpha = ValueTracker(0.0)

        def draw_conveyor():
            ph = scroll.get_value()
            wt = warp_t.get_value()
            rb = rung_boost.get_value()
            g = VGroup()
            # Draw 17 logical columns wrapping cleanly inside [-half_span, half_span]
            for cid in range(int(np.floor(ph / DX)) - 6, int(np.floor(ph / DX)) + 8):
                x = cid * DX - ph
                if abs(x) > 5.75:
                    continue
                edge_fade = float(np.clip((5.75 - abs(x)) / 0.85, 0.0, 1.0))
                is_target = (cid == target_id)

                # Rung
                rop = (0.45 + 0.45 * rb) * edge_fade
                rcol = TEAL if rb > 0.5 else BLUE
                rung = Line(
                    [x, Y_DN + BH / 2 + 0.04, 0],
                    [x, Y_UP - BH / 2 - 0.04, 0],
                    color=rcol,
                    stroke_width=3.0 + 1.5 * rb,
                    stroke_opacity=rop,
                )
                g.add(rung)

                # Upper block
                if is_target and wt > 0.01:
                    col = interpolate_color(ManimColor(BLUE), ManimColor(RED), wt)
                    ub = make_warped_block(col, BW, BH, fill_op=0.34 * edge_fade, stroke_w=3.8)
                    ub.set_stroke(opacity=edge_fade)
                    ub.move_to([x, Y_UP, 0])
                else:
                    ub = make_block(BLUE, BW, BH, fill_op=0.30 * edge_fade).set_stroke(opacity=edge_fade)
                    ub.move_to([x, Y_UP, 0])
                g.add(ub)

                # Lower block
                if is_target and wt > 0.01:
                    lb = make_block(BLUE, BW, BH, fill_op=0.30 * edge_fade, stroke_w=3.5 + 2.5 * wt)
                    lb.set_stroke(color=interpolate_color(ManimColor(BLUE), ManimColor(GOLD), wt), opacity=edge_fade)
                    lb.move_to([x, Y_DN, 0])
                else:
                    lb = make_block(BLUE, BW, BH, fill_op=0.30 * edge_fade).set_stroke(opacity=edge_fade)
                    lb.move_to([x, Y_DN, 0])
                g.add(lb)
            return g

        conveyor = always_redraw(draw_conveyor)
        self.add(conveyor)

        def draw_scanner():
            a = scan_alpha.get_value()
            if a <= 0.02:
                return VGroup()
            sx = scan_x.get_value()
            beam = RoundedRectangle(
                corner_radius=0.16,
                width=1.12,
                height=3.92,
                stroke_color=TEAL,
                stroke_width=4.0,
                stroke_opacity=a,
                fill_color=TEAL,
                fill_opacity=0.10 * a,
            ).move_to([sx, 0, 0])
            beam.layout_ok = True
            return beam

        scanner = always_redraw(draw_scanner)
        self.add(scanner)

        # Beat 1 (0.00 -> 3.96): continuous leftward drift of blue DNA rows
        self.play(scroll.animate.set_value(4.5), run_time=3.7, rate_func=linear)

        # Beat 2 (3.96): "How can a cell..." — scanning teal spotlight enters and sweeps
        self.at("How can a cell")
        self.play(
            scroll.animate.set_value(9.5),
            scan_alpha.animate.set_value(0.95),
            scan_x.animate.set_value(3.8),
            run_time=4.6,
            rate_func=linear,
        )

        # Beat 3 (8.88): "Watch these two blue rows" — sweep across to highlight both rows
        self.at("Watch these two blue rows")
        self.play(
            scroll.animate.set_value(12.2),
            scan_x.animate.set_value(-2.8),
            run_time=2.3,
            rate_func=linear,
        )

        # Beat 4 (11.46): "They carry paired information" — highlight pairing rungs
        self.at("They carry paired information")
        self.play(
            scroll.animate.set_value(14.3),
            rung_boost.animate.set_value(1.0),
            scan_x.animate.set_value(-4.5),
            run_time=2.3,
            rate_func=linear,
        )

        # Beat 5 (14.08): "A red mark changes..." — target_id=14 enters center, warps red, scanner locks onto it
        self.at("A red mark changes")
        target_x = lambda: target_id * DX - scroll.get_value()
        lbl_damage = always_redraw(
            lambda: T("damage", size=30, color=RED).move_to([target_x(), 2.38, 0])
        )
        lbl_partner = always_redraw(
            lambda: T("intact partner", size=30, color=GOLD).move_to([target_x(), -2.38, 0])
        )

        self.play(
            scroll.animate.set_value(target_id * DX - 0.7),
            warp_t.animate.set_value(1.0),
            rung_boost.animate.set_value(0.0),
            scan_x.animate.set_value(0.7),
            run_time=2.6,
            rate_func=smooth,
        )
        self.add(lbl_damage)
        self.play(FadeIn(lbl_damage, shift=DOWN * 0.1), run_time=0.4)

        # Beat 6 (16.94): "while the lower row" — label 'intact partner' appears below gold-outlined block
        self.at("while the lower row")
        self.add(lbl_partner)
        self.play(
            FadeIn(lbl_partner, shift=UP * 0.1),
            scroll.animate.set_value(target_id * DX - 0.35),
            scan_x.animate.set_value(0.35),
            run_time=2.5,
            rate_func=linear,
        )

        # Beat 7 (20.80): "shape determines" — gentle final drift to x = 0 at rest
        self.at("shape determines")
        self.play(
            scroll.animate.set_value(target_id * DX),
            scan_x.animate.set_value(0.0),
            run_time=1.8,
            rate_func=smooth,
        )
        self.finish()


# ------------------------------------------------------------------ S02
class S02Title(NarratedScene):
    def construct(self):
        # Start from the carried end state of S01Hook (target column centered at x=0)
        dup = build_duplex()
        mid = 5
        warped = make_warped_block(RED, BW, BH).move_to(dup.upper[mid].get_center())
        dup.upper[mid].become(warped)
        dup.lower[mid].set_stroke(GOLD, width=5.5)
        self.add(dup)

        # Compact focal 3-column motif (cols 4, 5, 6) and move it beside the title on the left
        focal = VGroup(
            dup.upper[4], dup.upper[5], dup.upper[6],
            dup.lower[4], dup.lower[5], dup.lower[6],
            dup.rungs[4], dup.rungs[5], dup.rungs[6],
        )
        outer = VGroup(
            dup.top_rail, dup.bot_rail,
            *[dup.upper[i] for i in range(N_COLS) if i not in (4, 5, 6)],
            *[dup.lower[i] for i in range(N_COLS) if i not in (4, 5, 6)],
            *[dup.rungs[i] for i in range(N_COLS) if i not in (4, 5, 6)],
        )

        lesson = T("DNA REPAIR AND RECOMBINATION", size=22, color=TEAL, weight=BOLD)
        title = fit_text("How DNA Chooses a Repair Route", max_w=7.2, size=44, font=TITLE_FONT, max_lines=2)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        lockup = VGroup(lesson, title, rule).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([1.85, 0, 0])

        self.play(
            FadeOut(outer, run_time=0.5),
            focal.animate.scale(0.85).move_to([-4.2, 0, 0]),
            FadeIn(lockup, shift=LEFT * 0.25),
            run_time=0.95,
        )
        # Red block and gold-outlined partner pulse once
        self.play(
            Indicate(dup.upper[5], color=RED, scale_factor=1.12),
            Indicate(dup.lower[5], color=GOLD, scale_factor=1.12),
            run_time=0.75,
        )
        self.finish()


# ------------------------------------------------------------------ S03
class S03Rule(SpokenScene):
    def construct(self):
        # Return full-height carried blue rows
        dup = build_duplex()
        self.play(FadeIn(dup), run_time=0.8)

        # Beat 1 (0.00 -> 6.44): full-duplex inspection bracket glides left-to-right checking pairs
        inspect_box = RoundedRectangle(
            corner_radius=0.14,
            width=1.22,
            height=3.65,
            stroke_color=TEAL,
            stroke_width=4.5,
            fill_color=TEAL,
            fill_opacity=0.11,
        ).move_to([col_x(0), 0, 0])
        inspect_box.layout_ok = True
        self.play(FadeIn(inspect_box), run_time=0.45)

        for idx in (1, 4, 7, 9):
            self.play(
                inspect_box.animate.move_to([col_x(idx), 0, 0]),
                dup.rungs[idx].animate.set_stroke(GOLD, width=6, opacity=0.95),
                dup.upper[idx].animate.set_fill(GOLD, opacity=0.45).set_stroke(GOLD, width=4.5),
                dup.lower[idx].animate.set_fill(GOLD, opacity=0.45).set_stroke(GOLD, width=4.5),
                run_time=0.62,
            )
            self.play(
                dup.rungs[idx].animate.set_stroke(BLUE, width=3, opacity=0.45),
                dup.upper[idx].animate.set_fill(BLUE, opacity=0.30).set_stroke(BLUE, width=3.5),
                dup.lower[idx].animate.set_fill(BLUE, opacity=0.30).set_stroke(BLUE, width=3.5),
                run_time=0.38,
            )
        self.play(inspect_box.animate.move_to([col_x(5), 0, 0]), run_time=0.85)

        # Beat 2 (6.44): "Sometimes the original base..."
        self.at("Sometimes the original base")
        mid = 5
        upper_target = dup.upper[mid]
        bracket = RoundedRectangle(
            corner_radius=0.14,
            width=BW + 0.28,
            height=BH + 0.28,
            stroke_color=GOLD,
            stroke_width=4.5,
            fill_color=GOLD,
            fill_opacity=0.14,
        ).move_to(upper_target.get_center())
        bracket.layout_ok = True
        badge = RoundedRectangle(
            corner_radius=0.09,
            width=0.44,
            height=0.24,
            stroke_color=RED,
            stroke_width=3,
            fill_color=RED,
            fill_opacity=0.88,
        ).move_to(upper_target.get_top() + DOWN * 0.06)
        chem_lbl = T("chemical mark", size=28, color=RED).move_to([0, 2.55, 0])
        chem_arr = Arrow(
            chem_lbl.get_bottom() + DOWN * 0.06,
            badge.get_top() + UP * 0.08,
            buff=0,
            color=RED,
            stroke_width=3.5,
            max_tip_length_to_length_ratio=0.35,
        )
        self.play(ReplacementTransform(inspect_box, bracket), FadeIn(badge, scale=0.8), run_time=1.0)
        self.play(FadeIn(chem_lbl, shift=DOWN * 0.12), GrowArrow(chem_arr), run_time=0.9)

        # Clear fill + scale pulse on the marked base and focus bracket while line finishes
        self.play(
            bracket.animate.scale(1.16).set_stroke(GOLD, width=6.5),
            upper_target.animate.set_fill(RED, opacity=0.48).scale(1.09),
            badge.animate.scale(1.22),
            run_time=1.25,
        )
        self.play(
            bracket.animate.scale(1.0 / 1.16).set_stroke(GOLD, width=4.5),
            upper_target.animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.09),
            badge.animate.scale(1.0 / 1.22),
            run_time=1.25,
        )
        self.play(
            bracket.animate.scale(1.12),
            upper_target.animate.set_fill(RED, opacity=0.45),
            run_time=0.85,
        )
        self.play(
            bracket.animate.scale(1.0 / 1.12),
            upper_target.animate.set_fill(BLUE, opacity=0.30),
            run_time=0.85,
        )

        # Beat 3 (12.92): "Direct reversal removes"
        self.at("Direct reversal removes")
        heading = T("direct reversal", size=34, color=TEAL, weight=BOLD).move_to([0, HEAD_Y, 0])
        tool = make_eraser_tool().move_to([3.8, 2.35, 0])
        self.play(
            FadeIn(heading, shift=DOWN * 0.1),
            FadeOut(chem_lbl),
            FadeOut(chem_arr),
            FadeIn(tool, shift=LEFT * 0.3),
            run_time=0.9,
        )
        # Slide tool over the badge, attach badge, carry it off to the right
        self.play(tool.animate.move_to([0.2, 2.15, 0]), run_time=0.85)
        carried = VGroup(tool, badge)
        self.play(carried.animate.shift(RIGHT * 4.4), run_time=1.0)
        self.play(FadeOut(carried), run_time=0.4)

        # Beat 4 (16.52): "The backbone stays uncut"
        self.at("The backbone stays uncut")
        # Full-height teal integrity band glides smoothly end-to-end over the continuous uncut upper backbone
        x_l = dup.top_rail.get_left()[0]
        x_r = dup.top_rail.get_right()[0]
        scanner = RoundedRectangle(
            corner_radius=0.14,
            width=1.35,
            height=3.75,
            stroke_color=TEAL,
            stroke_width=4.5,
            fill_color=TEAL,
            fill_opacity=0.14,
        ).move_to([x_l + 0.72, 0, 0])
        scanner.layout_ok = True
        self.play(
            FadeIn(scanner),
            dup.top_rail.animate.set_stroke(TEAL, width=7),
            run_time=0.55,
        )
        self.play(
            scanner.animate.move_to([x_r - 0.72, 0, 0]),
            run_time=2.8,
            rate_func=linear,
        )
        self.play(
            scanner.animate.move_to([0.0, 0, 0]),
            run_time=1.8,
            rate_func=smooth,
        )
        self.play(
            FadeOut(scanner),
            dup.top_rail.animate.set_stroke(GREY, width=5),
            run_time=0.55,
        )

        # Beat 5 (22.70): "fits only damage" — enzyme checks neighbors briefly, locks onto the repaired base
        self.at("fits only damage")
        self.play(
            bracket.animate.scale(1.16).set_stroke(GOLD, width=6.5),
            upper_target.animate.set_fill(GOLD, opacity=0.55).scale(1.10),
            dup.rungs[mid].animate.set_stroke(GOLD, width=5.5, opacity=0.95),
            run_time=1.15,
        )
        self.play(
            bracket.animate.scale(1.0 / 1.16).set_stroke(TEAL, width=4.5),
            upper_target.animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.10),
            dup.rungs[mid].animate.set_stroke(BLUE, width=3.0, opacity=0.45),
            run_time=1.15,
        )
        self.play(
            bracket.animate.scale(1.14).set_stroke(GOLD, width=6.0),
            upper_target.animate.set_fill(GOLD, opacity=0.50).scale(1.08),
            run_time=1.15,
        )
        self.play(
            bracket.animate.scale(1.0 / 1.14).set_stroke(GOLD, width=4.5),
            upper_target.animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.08),
            run_time=1.05,
        )
        self.finish()


# ------------------------------------------------------------------ S04
class S04Small(SpokenScene):
    def construct(self):
        dup = build_duplex()
        self.add(dup)

        mid = 5
        wave_t = ValueTracker(0.0)
        wave_on = ValueTracker(1.0)
        # Track active upper block vertical offset so it lifts cleanly without fighting the wave
        repair_active = set([mid])

        for i in range(N_COLS):
            if i == mid:
                continue
            bx = col_x(i)
            ub = dup.upper[i]
            lb = dup.lower[i]
            rg = dup.rungs[i]
            ub.add_updater(
                lambda m, dt, x=bx, idx=i: m.move_to(
                    [x, Y_UP + wave_on.get_value() * 0.075 * np.sin(2.6 * wave_t.get_value() - 0.55 * idx), 0]
                )
            )
            lb.add_updater(
                lambda m, dt, x=bx, idx=i: m.move_to(
                    [x, Y_DN + wave_on.get_value() * 0.075 * np.sin(2.6 * wave_t.get_value() - 0.55 * idx), 0]
                )
            )
            rg.add_updater(
                lambda m, dt, x=bx, idx=i: m.put_start_and_end_on(
                    [x, Y_DN + BH / 2 + 0.04 + wave_on.get_value() * 0.075 * np.sin(2.6 * wave_t.get_value() - 0.55 * idx), 0],
                    [x, Y_UP - BH / 2 - 0.04 + wave_on.get_value() * 0.075 * np.sin(2.6 * wave_t.get_value() - 0.55 * idx), 0],
                )
            )

        # Drive wave_t continuously across the scene via a lightweight dummy updater
        clock = ValueTracker(0.0)
        clock.add_updater(lambda m, dt: wave_t.increment_value(dt))
        self.add(clock)

        # Beat 1 (0.00 -> 4.10): "A small damaged base needs a different move"
        small_red = make_warped_block(RED, BW * 0.86, BH * 0.86).move_to([0, Y_UP, 0])
        self.play(Transform(dup.upper[mid], small_red), run_time=1.8)
        self.wait(1.6)

        # Beat 2 (4.10): "Base excision repair" — lift out single red block, leaving empty slot
        self.at("Base excision repair")
        heading = T("base excision repair", size=34, color=TEAL, weight=BOLD).move_to([0, HEAD_Y, 0])
        # Open a small break in upper backbone above mid
        left_rail = Line([dup.top_rail.get_left()[0], Y_RAIL_UP, 0], [-0.48, Y_RAIL_UP, 0], color=GREY, stroke_width=5)
        right_rail = Line([0.48, Y_RAIL_UP, 0], [dup.top_rail.get_right()[0], Y_RAIL_UP, 0], color=GREY, stroke_width=5)
        self.remove(dup.top_rail)
        self.add(left_rail, right_rail)
        self.play(
            FadeIn(heading, shift=DOWN * 0.1),
            FadeOut(dup.rungs[mid]),
            dup.upper[mid].animate.shift(UP * 1.45),
            run_time=1.8,
        )
        self.play(FadeOut(dup.upper[mid], shift=UP * 0.3), run_time=0.8)

        # Beat 3 (8.72): "The lower row guides" — gold partner sends guide line up; green block rises in
        self.at("The lower row guides")
        guide = DashedLine([0, Y_DN + BH / 2 + 0.04, 0], [0, Y_UP - BH / 2 - 0.04, 0], color=GOLD, stroke_width=4, dash_length=0.10)
        green_blk = (
            make_block(GREEN, BW, BH)
            .move_to([0, Y_DN + 0.85, 0])
            .set_fill(GREEN, opacity=0.0)
            .set_stroke(GREEN, opacity=0.0)
        )
        self.play(dup.lower[mid].animate.set_stroke(GOLD, width=5.5), Create(guide), run_time=1.1)
        self.add(green_blk)
        self.play(
            green_blk.animate.set_fill(GREEN, opacity=0.30).set_stroke(GREEN, opacity=1.0).move_to([0, Y_UP, 0]),
            run_time=1.6,
        )

        # Beat 4 (12.06): "the strand is sealed" — two teal clamps close the backbone gap
        self.at("the strand is sealed")
        clamp_l = RoundedRectangle(corner_radius=0.08, width=0.30, height=0.44, color=TEAL, fill_opacity=0.65).move_to([-0.85, Y_RAIL_UP, 0])
        clamp_r = RoundedRectangle(corner_radius=0.08, width=0.30, height=0.44, color=TEAL, fill_opacity=0.65).move_to([0.85, Y_RAIL_UP, 0])
        seal_seg = Line([-0.50, Y_RAIL_UP, 0], [0.50, Y_RAIL_UP, 0], color=TEAL, stroke_width=5)
        self.play(FadeIn(clamp_l), FadeIn(clamp_r), run_time=0.4)
        self.play(
            clamp_l.animate.move_to([-0.16, Y_RAIL_UP, 0]),
            clamp_r.animate.move_to([0.16, Y_RAIL_UP, 0]),
            Create(seal_seg),
            run_time=1.1,
        )
        self.play(FadeOut(clamp_l), FadeOut(clamp_r), seal_seg.animate.set_stroke(GREY), run_time=0.5)

        # Beat 5 (14.42): "One damaged block" — emphasize the restored green block
        self.at("One damaged block")
        self.play(Indicate(green_blk, color=GREEN, scale_factor=1.10), run_time=1.5)

        # Beat 6 (18.76): "Most surrounding DNA" — green becomes blue; sweep focus over untouched neighbors
        self.at("Most surrounding DNA")
        restored_blue = make_block(BLUE, BW, BH).move_to([0, Y_UP, 0])
        restored_rung = Line([0, Y_DN + BH / 2 + 0.04, 0], [0, Y_UP - BH / 2 - 0.04, 0], color=BLUE, stroke_width=3, stroke_opacity=0.45)
        self.play(
            Transform(green_blk, restored_blue),
            FadeOut(guide),
            FadeIn(restored_rung),
            dup.lower[mid].animate.set_stroke(BLUE, width=3.5),
            run_time=1.8,
        )

        # Beat 7 (22.68): "Repair machinery works" — clean preservation sweep over untouched neighbors
        self.at("Repair machinery works")
        self.play(
            LaggedStart(
                *[Indicate(dup.upper[i], color=BLUE, scale_factor=1.07) for i in range(N_COLS) if i != mid],
                lag_ratio=0.09,
            ),
            run_time=2.5,
        )
        self.finish()


# ------------------------------------------------------------------ S05
class S05Bulky(SpokenScene):
    def construct(self):
        dup = build_duplex()
        self.add(dup, scope_tag("schematic"))

        # Compute Gaussian bow on upper row around cols 4..7 (centered at x_mid = col 5.5)
        patch_cols = [4, 5, 6, 7]
        x_mid = (col_x(5) + col_x(6)) / 2.0

        def bow_dy(x, amp):
            return amp * float(np.exp(-((x - x_mid) / 1.85) ** 2))

        bow_amp = ValueTracker(0.0)
        # Store initial rail points to deform rail smoothly
        x_l, x_r = dup.top_rail.get_left()[0], dup.top_rail.get_right()[0]
        xs_rail = np.linspace(x_l, x_r, 60)

        def make_bowed_rail(amp, color=GREY, width=5):
            m = VMobject(color=color, stroke_width=width)
            m.set_points_as_corners([[x, Y_RAIL_UP + bow_dy(x, amp), 0] for x in xs_rail])
            return m

        bow_rail = always_redraw(lambda: make_bowed_rail(bow_amp.get_value()))
        self.remove(dup.top_rail)
        self.add(bow_rail)

        # Linked red pair at cols 5 & 6
        c5, c6 = col_x(5), col_x(6)
        link_bar = Line([c5, Y_UP, 0], [c6, Y_UP, 0], color=RED, stroke_width=10)

        # Beat 1 (0.00 -> 5.54): Transform cols 5 & 6 into a red linked pair and bow the upper row
        linked_5 = make_warped_block(RED, BW, BH).move_to([c5, Y_UP, 0])
        linked_6 = make_warped_block(RED, BW, BH).move_to([c6, Y_UP, 0])

        def update_bow_blocks(amp_val):
            anims = []
            for i in range(N_COLS):
                x = col_x(i)
                dy = bow_dy(x, amp_val)
                anims.append(dup.upper[i].animate.move_to([x, Y_UP + dy, 0]))
                anims.append(
                    dup.rungs[i].animate.put_start_and_end_on(
                        [x, Y_DN + BH / 2 + 0.04, 0],
                        [x, Y_UP + dy - BH / 2 - 0.04, 0],
                    )
                )
            return anims

        self.play(
            Transform(dup.upper[5], linked_5),
            Transform(dup.upper[6], linked_6),
            Create(link_bar),
            run_time=1.3,
        )
        # Bow upper blocks + link bar + rail upward
        self.play(
            bow_amp.animate.set_value(0.46),
            *[
                dup.upper[i].animate.move_to([col_x(i), Y_UP + bow_dy(col_x(i), 0.46), 0])
                for i in range(N_COLS)
            ],
            *[
                dup.rungs[i].animate.put_start_and_end_on(
                    [col_x(i), Y_DN + BH / 2 + 0.04, 0],
                    [col_x(i), Y_UP + bow_dy(col_x(i), 0.46) - BH / 2 - 0.04, 0],
                )
                for i in range(N_COLS)
            ],
            link_bar.animate.put_start_and_end_on(
                [c5, Y_UP + bow_dy(c5, 0.46), 0],
                [c6, Y_UP + bow_dy(c6, 0.46), 0],
            ),
            run_time=2.3,
        )

        # Beat 2 (5.54): "Nucleotide excision repair" — label + wide scanning box sweeping distorted zone
        self.at("Nucleotide excision repair")
        heading = T("nucleotide excision repair", size=34, color=TEAL, weight=BOLD).move_to([0, 3.38, 0])
        scan_box = RoundedRectangle(
            corner_radius=0.18,
            width=4.4,
            height=2.15,
            stroke_color=TEAL,
            stroke_width=4.5,
            fill_color=TEAL,
            fill_opacity=0.13,
        ).move_to([x_mid - 1.1, Y_UP + 0.25, 0])
        scan_box.layout_ok = True
        self.play(
            FadeIn(heading, shift=DOWN * 0.1),
            FadeIn(scan_box),
            run_time=1.2,
        )
        self.play(scan_box.animate.move_to([x_mid + 1.1, Y_UP + 0.25, 0]), run_time=1.6)
        self.play(scan_box.animate.move_to([x_mid, Y_UP + 0.25, 0]), run_time=1.3)

        # Beat 3 (10.42): "Two cuts lift" — teal cut markers land on both sides, short red patch rises out
        self.at("Two cuts lift")
        cut_l_x = (col_x(3) + col_x(4)) / 2.0
        cut_r_x = (col_x(7) + col_x(8)) / 2.0
        cut_l = make_cut_marker(cut_l_x, Y_RAIL_UP + bow_dy(cut_l_x, 0.46))
        cut_r = make_cut_marker(cut_r_x, Y_RAIL_UP + bow_dy(cut_r_x, 0.46))
        self.play(FadeOut(scan_box), FadeIn(cut_l, shift=DOWN * 0.15), FadeIn(cut_r, shift=DOWN * 0.15), run_time=0.9)

        # Split bowed rail into left, excised center, and right
        xs_c = np.linspace(cut_l_x, cut_r_x, 24)
        xs_ll = np.linspace(x_l, cut_l_x, 20)
        xs_rr = np.linspace(cut_r_x, x_r, 20)
        rail_l = VMobject(color=GREY, stroke_width=5).set_points_as_corners([[x, Y_RAIL_UP + bow_dy(x, 0.46), 0] for x in xs_ll])
        rail_r = VMobject(color=GREY, stroke_width=5).set_points_as_corners([[x, Y_RAIL_UP + bow_dy(x, 0.46), 0] for x in xs_rr])
        rail_c = VMobject(color=RED, stroke_width=5).set_points_as_corners([[x, Y_RAIL_UP + bow_dy(x, 0.46), 0] for x in xs_c])
        self.remove(bow_rail)
        self.add(rail_l, rail_r, rail_c)

        excised_patch = VGroup(
            rail_c, link_bar,
            *[dup.upper[i] for i in patch_cols],
        )
        self.play(
            *[FadeOut(dup.rungs[i]) for i in patch_cols],
            FadeOut(cut_l),
            FadeOut(cut_r),
            excised_patch.animate.shift(UP * 0.62),
            run_time=1.5,
        )
        self.play(FadeOut(excised_patch, shift=UP * 0.12), run_time=0.6)

        # Beat 4 (14.66): "The intact row guides" — gold outlines + guides + green blocks sweep in
        self.at("The intact row guides")
        guides = VGroup(*[
            DashedLine([col_x(i), Y_DN + BH / 2 + 0.04, 0], [col_x(i), Y_UP - BH / 2 - 0.04, 0],
                       color=GOLD, stroke_width=4, dash_length=0.10)
            for i in patch_cols
        ])
        self.play(
            *[dup.lower[i].animate.set_stroke(GOLD, width=5.5) for i in patch_cols],
            Create(guides),
            run_time=1.0,
        )
        greens = VGroup(*[
            make_block(GREEN, BW, BH)
            .move_to([col_x(i), Y_DN + 0.7, 0])
            .set_fill(GREEN, opacity=0.0)
            .set_stroke(GREEN, opacity=0.0)
            for i in patch_cols
        ])
        self.add(greens)
        # Straighten outer rows back to flat Y_UP while green blocks sweep in
        straight_l = Line([x_l, Y_RAIL_UP, 0], [cut_l_x, Y_RAIL_UP, 0], color=GREY, stroke_width=5)
        straight_r = Line([cut_r_x, Y_RAIL_UP, 0], [x_r, Y_RAIL_UP, 0], color=GREY, stroke_width=5)
        seal_mid = Line([cut_l_x, Y_RAIL_UP, 0], [cut_r_x, Y_RAIL_UP, 0], color=GREEN, stroke_width=5)
        self.play(
            LaggedStart(
                *[g.animate.set_fill(GREEN, opacity=0.30).set_stroke(GREEN, opacity=1.0).move_to([col_x(i), Y_UP, 0]) for g, i in zip(greens, patch_cols)],
                lag_ratio=0.15,
            ),
            Transform(rail_l, straight_l),
            Transform(rail_r, straight_r),
            *[dup.upper[i].animate.move_to([col_x(i), Y_UP, 0]) for i in range(N_COLS) if i not in patch_cols],
            *[
                dup.rungs[i].animate.put_start_and_end_on([col_x(i), Y_DN + BH / 2 + 0.04, 0], [col_x(i), Y_UP - BH / 2 - 0.04, 0])
                for i in range(N_COLS) if i not in patch_cols
            ],
            run_time=2.2,
        )
        self.play(Create(seal_mid), run_time=0.6)

        # Beat 5 (19.12): "The same partner" — sweep a gold template band & pulse lower partner bases smoothly
        self.at("The same partner")
        partner_box = RoundedRectangle(
            corner_radius=0.14,
            width=4.2,
            height=1.36,
            stroke_color=GOLD,
            stroke_width=4.5,
            fill_color=GOLD,
            fill_opacity=0.14,
        ).move_to([x_mid, Y_DN, 0])
        partner_box.layout_ok = True
        self.play(
            FadeIn(partner_box),
            *[dup.lower[i].animate.set_fill(GOLD, opacity=0.50).scale(1.07) for i in patch_cols],
            run_time=1.1,
        )
        self.play(
            partner_box.animate.shift(RIGHT * 0.55),
            *[dup.lower[i].animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.07) for i in patch_cols],
            run_time=1.1,
        )
        self.play(
            partner_box.animate.shift(LEFT * 0.55),
            *[dup.lower[i].animate.set_fill(GOLD, opacity=0.45).scale(1.06) for i in patch_cols],
            run_time=1.1,
        )

        # Beat 6 (23.02): "chemistry and distortion" — green patch becomes blue sequentially, verifying restored duplex
        self.at("chemistry and distortion")
        new_rungs = VGroup(*[
            Line([col_x(i), Y_DN + BH / 2 + 0.04, 0], [col_x(i), Y_UP - BH / 2 - 0.04, 0],
                 color=BLUE, stroke_width=3, stroke_opacity=0.45)
            for i in patch_cols
        ])
        verify_band = RoundedRectangle(
            corner_radius=0.16,
            width=4.3,
            height=3.65,
            stroke_color=BLUE,
            stroke_width=4.5,
            fill_color=BLUE,
            fill_opacity=0.12,
        ).move_to([x_mid, 0, 0])
        verify_band.layout_ok = True
        self.play(
            LaggedStart(
                *[g.animate.set_color(BLUE).set_fill(BLUE, opacity=0.35).set_stroke(BLUE, width=3.5) for g in greens],
                lag_ratio=0.18,
            ),
            *[dup.lower[i].animate.set_fill(BLUE, opacity=0.30).set_stroke(BLUE, width=3.5).scale(1.0 / 1.06) for i in patch_cols],
            ReplacementTransform(partner_box, verify_band),
            FadeOut(guides),
            FadeIn(new_rungs),
            seal_mid.animate.set_stroke(GREY, width=5),
            run_time=2.2,
        )
        self.play(
            verify_band.animate.scale(1.08),
            *[g.animate.set_fill(BLUE, opacity=0.52) for g in greens],
            seal_mid.animate.set_stroke(TEAL, width=6),
            run_time=1.1,
        )
        self.play(
            FadeOut(verify_band),
            *[g.animate.set_fill(BLUE, opacity=0.30) for g in greens],
            seal_mid.animate.set_stroke(GREY, width=5),
            run_time=0.9,
        )
        self.finish()


# ------------------------------------------------------------------ S06
class S06Predict(SpokenScene):
    def construct(self):
        dup = build_duplex()
        mid = 5
        dup.rungs[mid].set_stroke(opacity=0.0)
        qmark = T("?", size=38, color=RED, weight=BOLD).move_to([0, 0, 0])
        self.add(dup, qmark)

        # Beat 1 (0.00 -> 5.04): two normal blue blocks, mismatch wiggle + '?' rock showing unresolved choice
        self.play(
            dup.upper[mid].animate.shift(RIGHT * 0.09),
            dup.lower[mid].animate.shift(LEFT * 0.09),
            Rotate(qmark, angle=0.16),
            run_time=1.4,
        )
        self.play(
            dup.upper[mid].animate.shift(LEFT * 0.18),
            dup.lower[mid].animate.shift(RIGHT * 0.18),
            Rotate(qmark, angle=-0.32),
            run_time=1.5,
        )
        self.play(
            dup.upper[mid].animate.move_to([0, Y_UP, 0]),
            dup.lower[mid].animate.move_to([0, Y_DN, 0]),
            Rotate(qmark, angle=0.16),
            run_time=1.3,
        )

        # Beat 2 (5.04): "Neither looks damaged" — highlight both blue blocks clearly while '?' keeps rocking
        self.at("Neither looks damaged")
        self.play(
            dup.upper[mid].animate.set_fill(WHITE, opacity=0.48).scale(1.10),
            dup.lower[mid].animate.set_fill(WHITE, opacity=0.48).scale(1.10),
            Rotate(qmark, angle=0.22),
            run_time=1.0,
        )
        self.play(
            dup.upper[mid].animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.10),
            dup.lower[mid].animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.10),
            Rotate(qmark, angle=-0.22),
            run_time=1.0,
        )

        # Beat 3 (7.28): "If the strands carry" — glide a crisp white choice halo smoothly between upper and lower block
        self.at("If the strands carry")
        arr_up = Arrow([0, 2.35, 0], [0, 1.86, 0], buff=0, color=TEXT, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        arr_dn = Arrow([0, -2.35, 0], [0, -1.86, 0], buff=0, color=TEXT, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        lab_up = T("replace?", size=28, color=TEXT).next_to(arr_up, UP, buff=0.14)
        lab_dn = T("replace?", size=28, color=TEXT).next_to(arr_dn, DOWN, buff=0.14)
        self.play(
            FadeIn(arr_up), FadeIn(lab_up),
            FadeIn(arr_dn), FadeIn(lab_dn),
            run_time=1.0,
        )

        choice_halo = RoundedRectangle(
            corner_radius=0.14,
            width=1.04,
            height=1.34,
            stroke_color=WHITE,
            stroke_width=4.0,
            fill_color=WHITE,
            fill_opacity=0.22,
        ).move_to([0, Y_UP, 0])

        self.play(FadeIn(choice_halo), Rotate(qmark, angle=-0.20), run_time=0.65)
        self.play(
            choice_halo.animate.move_to([0, Y_DN, 0]),
            dup.lower[mid].animate.set_fill(WHITE, opacity=0.45),
            dup.upper[mid].animate.set_fill(BLUE, opacity=0.30),
            Rotate(qmark, angle=0.40),
            run_time=1.05,
        )
        self.play(
            choice_halo.animate.move_to([0, Y_UP, 0]),
            dup.upper[mid].animate.set_fill(WHITE, opacity=0.45),
            dup.lower[mid].animate.set_fill(BLUE, opacity=0.30),
            Rotate(qmark, angle=-0.40),
            run_time=1.05,
        )
        self.play(
            choice_halo.animate.move_to([0, Y_DN, 0]),
            dup.lower[mid].animate.set_fill(WHITE, opacity=0.45),
            dup.upper[mid].animate.set_fill(BLUE, opacity=0.30),
            Rotate(qmark, angle=0.20),
            run_time=1.05,
        )

        # Beat 4 (12.34): "Choose the upper block" — keep gliding between both choices through pause handoff
        self.at("Choose the upper block")
        self.play(
            choice_halo.animate.move_to([0, Y_UP, 0]),
            dup.upper[mid].animate.set_fill(WHITE, opacity=0.45),
            dup.lower[mid].animate.set_fill(BLUE, opacity=0.30),
            Rotate(qmark, angle=-0.18),
            run_time=1.1,
        )
        self.play(
            choice_halo.animate.move_to([0, Y_DN, 0]),
            dup.lower[mid].animate.set_fill(WHITE, opacity=0.45),
            dup.upper[mid].animate.set_fill(BLUE, opacity=0.30),
            Rotate(qmark, angle=0.36),
            run_time=1.1,
        )
        self.finish()


# ------------------------------------------------------------------ S07
class S07Pause(PredictPause):
    QUESTION = "Which strand is new?"
    OPTIONS = ()
    CARD = {"y": -3.15}
    RING_AT = (6.0, -3.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        bg = mismatch_backdrop(show_arrows=True)
        # Keep the red '?' gently rocking and white highlight alternating between upper and lower block
        q_state = {"t": 0.0, "prev": 0.0}
        qmark = bg.qmark

        def rock_q(m, dt):
            q_state["t"] += dt
            ang = 0.22 * np.sin(2.8 * q_state["t"])
            m.rotate(ang - q_state["prev"])
            q_state["prev"] = ang

        qmark.add_updater(rock_q)

        hi_up = make_block(WHITE, BW + 0.08, BH + 0.08, fill_op=0.16, stroke_w=4.0).move_to([0, Y_UP, 0])
        hi_dn = make_block(WHITE, BW + 0.08, BH + 0.08, fill_op=0.16, stroke_w=4.0).move_to([0, Y_DN, 0])
        hi_up.layout_ok = True
        hi_dn.layout_ok = True
        hi_t = {"up": 0.0, "dn": 0.0}

        def alt_up(m, dt):
            hi_t["up"] += dt
            s = 0.5 + 0.5 * np.sin(3.2 * hi_t["up"])
            m.set_fill(opacity=0.18 * s)
            m.set_stroke(opacity=0.85 * s)

        def alt_dn(m, dt):
            hi_t["dn"] += dt
            s = 0.5 - 0.5 * np.sin(3.2 * hi_t["dn"])
            m.set_fill(opacity=0.18 * s)
            m.set_stroke(opacity=0.85 * s)

        hi_up.add_updater(alt_up)
        hi_dn.add_updater(alt_dn)

        return VGroup(bg, hi_up, hi_dn)


# ------------------------------------------------------------------ S08
class S08Reveal(SpokenScene):
    def construct(self):
        bg = mismatch_backdrop(show_arrows=True)
        dup = bg.dup
        qmark = bg.qmark
        self.add(bg)

        # Beat 1 (0.00 -> 3.52): "The mismatch alone cannot answer" — clear pause arrows, wiggle unresolved pair & '?'
        self.play(FadeOut(bg.arrows), run_time=0.45)
        self.play(
            dup.upper[5].animate.shift(RIGHT * 0.10),
            dup.lower[5].animate.shift(LEFT * 0.10),
            Rotate(qmark, angle=0.22),
            run_time=1.0,
        )
        self.play(
            dup.upper[5].animate.shift(LEFT * 0.20),
            dup.lower[5].animate.shift(RIGHT * 0.20),
            Rotate(qmark, angle=-0.44),
            run_time=1.0,
        )
        self.play(
            dup.upper[5].animate.move_to([0, Y_UP, 0]),
            dup.lower[5].animate.move_to([0, Y_DN, 0]),
            Rotate(qmark, angle=0.22),
            run_time=0.95,
        )

        # Beat 2 (3.52): "Repair needs another clue" — moving teal ribbon 'new strand' along upper row
        self.at("Repair needs another clue")
        rib_phase = ValueTracker(0.0)
        rib_phase.add_updater(lambda m, dt: m.increment_value(1.15 * dt))
        self.add(rib_phase)

        x_l, x_r = dup.top_rail.get_left()[0], dup.top_rail.get_right()[0]
        new_bar, new_ticks = moving_ribbon_ticks(x_l, x_r, Y_RAIL_UP + 0.14, TEAL, rib_phase, n_ticks=14)
        new_lbl = T("new strand", size=30, color=TEAL, weight=BOLD).move_to([-4.2, 2.48, 0])
        self.add(new_ticks)
        self.play(FadeIn(new_bar), FadeIn(new_lbl, shift=DOWN * 0.08), run_time=0.85)
        self.play(
            LaggedStart(*[Indicate(dup.upper[i], color=TEAL, scale_factor=1.05) for i in range(N_COLS)], lag_ratio=0.06),
            run_time=2.5,
        )

        # Beat 3 (8.28): "During replication" — gold ribbon 'template' along lower row
        self.at("During replication")
        tmpl_bar, tmpl_ticks = moving_ribbon_ticks(x_l, x_r, Y_RAIL_DN - 0.14, GOLD, rib_phase, n_ticks=14)
        tmpl_lbl = T("template", size=30, color=GOLD, weight=BOLD).move_to([-4.2, -2.48, 0])
        patch = [4, 5, 6, 7]
        self.add(tmpl_ticks)
        self.play(
            FadeIn(tmpl_bar),
            FadeIn(tmpl_lbl, shift=UP * 0.1),
            *[dup.lower[i].animate.set_stroke(GOLD, width=5.5) for i in patch],
            run_time=1.8,
        )
        self.play(
            LaggedStart(*[Indicate(dup.lower[i], color=GOLD, scale_factor=1.07) for i in patch], lag_ratio=0.14),
            run_time=2.0,
        )

        # Beat 4 (13.08): "Signals that tell new" — teal upper stretch containing mismatch peels away
        self.at("Signals that tell new")
        peel_grp = VGroup(*[dup.upper[i] for i in patch])
        self.play(
            FadeOut(qmark),
            *[FadeOut(dup.rungs[i]) for i in patch if i != 5],
            *[dup.upper[i].animate.set_stroke(TEAL, width=4.5).set_fill(TEAL, opacity=0.30) for i in patch],
            run_time=1.0,
        )
        self.play(peel_grp.animate.shift(UP * 1.15 + RIGHT * 0.25), run_time=1.4)
        self.play(FadeOut(peel_grp, shift=UP * 0.3), run_time=0.7)

        # Beat 5 (18.44): "The template then guides" — green blocks copy upward from gold template
        self.at("The template then guides")
        guides = VGroup(*[
            DashedLine([col_x(i), Y_DN + BH / 2 + 0.04, 0], [col_x(i), Y_UP - BH / 2 - 0.04, 0],
                       color=GOLD, stroke_width=4, dash_length=0.10)
            for i in patch
        ])
        greens = VGroup(*[
            make_block(GREEN, BW, BH)
            .move_to([col_x(i), Y_DN + 0.7, 0])
            .set_fill(GREEN, opacity=0.0)
            .set_stroke(GREEN, opacity=0.0)
            for i in patch
        ])
        self.add(greens)
        self.play(Create(guides), run_time=0.7)
        self.play(
            LaggedStart(
                *[g.animate.set_fill(GREEN, opacity=0.30).set_stroke(GREEN, opacity=1.0).move_to([col_x(i), Y_UP, 0]) for g, i in zip(greens, patch)],
                lag_ratio=0.15,
            ),
            run_time=1.9,
        )

        # Beat 6 (22.80): "trustworthy information includes" — turn corrected patch blue sequentially & verify pairing
        self.at("trustworthy information includes")
        restored_rungs = VGroup(*[
            Line([col_x(i), Y_DN + BH / 2 + 0.04, 0], [col_x(i), Y_UP - BH / 2 - 0.04, 0],
                 color=BLUE, stroke_width=3, stroke_opacity=0.45)
            for i in patch
        ])
        self.play(
            LaggedStart(
                *[g.animate.set_color(BLUE).set_fill(BLUE, opacity=0.30).set_stroke(BLUE, width=3.5) for g in greens],
                lag_ratio=0.18,
            ),
            FadeOut(guides),
            LaggedStart(*[FadeIn(r) for r in restored_rungs], lag_ratio=0.18),
            run_time=2.6,
        )
        self.play(
            LaggedStart(*[Indicate(g, color=BLUE, scale_factor=1.08) for g in greens], lag_ratio=0.15),
            LaggedStart(*[Indicate(dup.lower[i], color=GOLD, scale_factor=1.08) for i in patch], lag_ratio=0.15),
            run_time=2.3,
        )

        # Beat 7 (28.74): "extra label solves" — emphasize the two identity labels cleanly
        self.at("extra label solves")
        self.play(
            Indicate(new_lbl, color=TEAL, scale_factor=1.10),
            Indicate(tmpl_lbl, color=GOLD, scale_factor=1.10),
            run_time=1.3,
        )
        self.play(
            Indicate(new_lbl, color=TEAL, scale_factor=1.08),
            Indicate(tmpl_lbl, color=GOLD, scale_factor=1.08),
            run_time=1.1,
        )
        self.finish()


# ------------------------------------------------------------------ S09
class S09Sort(SpokenScene):
    def construct(self):
        # Continuous 14-column duplex showing all four repair routes left-to-right
        n14 = 14
        dx14 = 0.88
        bw14 = 0.68
        bh14 = 1.04
        y_u, y_d = 1.02, -1.02
        ru, rd = 1.68, -1.68

        dup = build_duplex(n_cols=n14, dx=dx14, bw=bw14, bh=bh14, y_up=y_u, y_dn=y_d, rail_up=ru, rail_dn=rd)

        # Zone column assignments:
        # Zone 1 ('reverse'): col 1
        # Zone 2 ('one base'): col 3
        # Zone 3 ('short patch'): cols 5, 6, 7 (with linked red pair at 5, 6)
        # Zone 4 ('new strand'): cols 10, 11, 12 (with teal ribbon & mismatch ? at 11)
        z1 = 1
        z2 = 3
        z3 = [5, 6, 7]
        z4 = [10, 11, 12]

        # Set initial damage visuals along the continuous row
        # Zone 1: red badge on intact blue block
        badge = RoundedRectangle(
            corner_radius=0.07, width=0.34, height=0.18,
            stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.90,
        ).move_to(dup.upper[z1].get_top() + DOWN * 0.05)

        # Zone 2: single red warped block
        dup.upper[z2].become(make_warped_block(RED, bw14, bh14).move_to(dup.upper[z2].get_center()))

        # Zone 3: linked red pair (5, 6) + slight upward bow on cols 5, 6, 7 and local top rail arch
        bow = {5: 0.12, 6: 0.16, 7: 0.12}
        for c, dy in bow.items():
            dup.upper[c].shift(UP * dy)
            x = dup.upper[c].get_center()[0]
            dup.rungs[c].put_start_and_end_on([x, y_d + bh14 / 2 + 0.04, 0], [x, y_u + dy - bh14 / 2 - 0.04, 0])
        dup.upper[5].become(make_warped_block(RED, bw14, bh14).move_to(dup.upper[5].get_center()))
        dup.upper[6].become(make_warped_block(RED, bw14, bh14).move_to(dup.upper[6].get_center()))
        link3 = Line(dup.upper[5].get_center(), dup.upper[6].get_center(), color=RED, stroke_width=8)

        # Replace flat top rail with a locally bowed top rail clearing Zone 3 blocks
        rail_xl = dup.top_rail.get_left()[0]
        rail_xr = dup.top_rail.get_right()[0]
        x_b_mid = col_x(6, n14, dx14)
        xs_bow = np.linspace(rail_xl, rail_xr, 90)
        bowed_top_rail = VMobject(color=GREY, stroke_width=5).set_points_as_corners([
            [x, ru + 0.30 * np.exp(-((x - x_b_mid) / 1.15) ** 2), 0] for x in xs_bow
        ])
        flat_top_rail = Line([rail_xl, ru, 0], [rail_xr, ru, 0], color=GREY, stroke_width=5)
        dup.top_rail.become(bowed_top_rail)

        # Zone 4: teal new-strand segment over cols 10..12 + mismatch ? at col 11
        x10 = dup.upper[10].get_left()[0] - 0.06
        x12 = dup.upper[12].get_right()[0] + 0.06
        teal_seg = Line([x10, ru + 0.13, 0], [x12, ru + 0.13, 0], color=TEAL, stroke_width=6)
        for c in z4:
            dup.upper[c].set_stroke(TEAL, width=4.0)
        dup.rungs[11].set_stroke(opacity=0.0)
        q11 = T("?", size=38, color=RED, weight=BOLD).move_to([col_x(11, n14, dx14), 0, 0])

        focus_box = RoundedRectangle(
            corner_radius=0.14,
            width=1.05,
            height=3.65,
            stroke_color=TEAL,
            stroke_width=4.0,
            fill_color=TEAL,
            fill_opacity=0.11,
        ).move_to([col_x(z1, n14, dx14), 0, 0])
        focus_box.layout_ok = True
        self.play(FadeIn(dup), FadeIn(badge), FadeIn(link3), FadeIn(teal_seg), FadeIn(q11), run_time=1.2)
        self.play(FadeIn(focus_box, shift=RIGHT * 0.4), run_time=1.0)
        self.play(
            dup.upper[z2].animate.set_fill(RED, opacity=0.45),
            dup.upper[5].animate.set_fill(RED, opacity=0.45),
            dup.upper[6].animate.set_fill(RED, opacity=0.45),
            run_time=0.9,
        )

        # Beat 1 (3.62): "reversibly damaged base" -> Zone 1 transformation + gold pointer under upper block itself
        self.at("reversibly damaged base")
        lbl1 = T("reverse", size=28, color=TEAL, weight=BOLD).move_to([col_x(z1, n14, dx14), 2.85, 0])
        dup.rungs[z1].set_stroke(opacity=0.0)
        ptr1 = make_gold_pointer(col_x(z1, n14, dx14), 0.16, point_up=True)
        eraser = make_eraser_tool().scale(0.55).move_to([col_x(z1, n14, dx14) - 0.65, 1.95, 0])
        self.play(FadeIn(lbl1), FadeIn(ptr1), FadeIn(eraser), run_time=0.6)
        self.play(eraser.animate.move_to([col_x(z1, n14, dx14) + 0.05, 1.85, 0]), run_time=0.7)
        carried1 = VGroup(eraser, badge)
        self.play(carried1.animate.shift(DOWN * 0.12 + LEFT * 0.35).set_opacity(0), run_time=0.55)
        self.remove(carried1)
        self.play(
            dup.upper[z1].animate.set_fill(BLUE, opacity=0.55).scale(1.08),
            run_time=0.75,
        )
        self.play(
            dup.upper[z1].animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.08),
            focus_box.animate.move_to([col_x(z2, n14, dx14), 0, 0]),
            run_time=0.85,
        )

        # Beat 2 (7.62): "small lesion loses" -> Zone 2 one red block exchanged + gold pointer under lower partner
        self.at("small lesion loses")
        lbl2 = T("one base", size=28, color=TEAL, weight=BOLD).move_to([col_x(z2, n14, dx14), 2.85, 0])
        ptr2 = make_gold_pointer(col_x(z2, n14, dx14), -2.05, point_up=True)
        self.play(
            FadeIn(lbl2), FadeIn(ptr2),
            dup.lower[z2].animate.set_fill(GOLD, opacity=0.45).set_stroke(GOLD, width=5.0),
            FadeOut(dup.rungs[z2]),
            dup.upper[z2].animate.shift(UP * 0.55).set_opacity(0),
            run_time=0.95,
        )
        g2 = (
            make_block(GREEN, bw14, bh14)
            .move_to([col_x(z2, n14, dx14), y_d + 0.6, 0])
            .set_fill(GREEN, opacity=0.0)
            .set_stroke(GREEN, opacity=0.0)
        )
        self.add(g2)
        self.play(
            g2.animate.set_fill(GREEN, opacity=0.35).set_stroke(GREEN, opacity=1.0).move_to([col_x(z2, n14, dx14), y_u, 0]),
            run_time=0.85,
        )
        z3_focus = RoundedRectangle(
            corner_radius=0.14,
            width=2.80,
            height=3.65,
            stroke_color=TEAL,
            stroke_width=4.0,
            fill_color=TEAL,
            fill_opacity=0.11,
        ).move_to([col_x(6, n14, dx14), 0, 0])
        z3_focus.layout_ok = True
        self.play(
            ReplacementTransform(focus_box, z3_focus),
            dup.lower[z2].animate.set_fill(BLUE, opacity=0.30),
            run_time=0.95,
        )

        # Beat 3 (10.64): "bulky distortion loses" -> Zone 3 short patch exchanged + gold pointer under lower partner
        self.at("bulky distortion loses")
        lbl3 = T("short patch", size=28, color=TEAL, weight=BOLD).move_to([col_x(6, n14, dx14), 2.85, 0])
        ptr3 = make_gold_pointer(col_x(6, n14, dx14), -2.05, point_up=True)
        patch3_grp = VGroup(link3, *[dup.upper[c] for c in z3])
        self.play(
            FadeIn(lbl3), FadeIn(ptr3),
            *[dup.lower[c].animate.set_fill(GOLD, opacity=0.45).set_stroke(GOLD, width=5.0) for c in z3],
            *[FadeOut(dup.rungs[c]) for c in z3],
            patch3_grp.animate.shift(UP * 0.55).set_opacity(0),
            run_time=1.0,
        )
        g3 = VGroup(*[
            make_block(GREEN, bw14, bh14)
            .move_to([col_x(c, n14, dx14), y_d + 0.6, 0])
            .set_fill(GREEN, opacity=0.0)
            .set_stroke(GREEN, opacity=0.0)
            for c in z3
        ])
        self.add(g3)
        self.play(
            *[blk.animate.set_fill(GREEN, opacity=0.35).set_stroke(GREEN, opacity=1.0).move_to([col_x(c, n14, dx14), y_u, 0]) for blk, c in zip(g3, z3)],
            Transform(dup.top_rail, flat_top_rail),
            run_time=0.95,
        )
        self.play(
            z3_focus.animate.move_to([col_x(11, n14, dx14), 0, 0]),
            *[dup.lower[c].animate.set_fill(BLUE, opacity=0.30) for c in z3],
            run_time=1.0,
        )

        # Beat 4 (13.86): "mismatch loses part" -> Zone 4 teal new-strand segment exchanged + gold pointer under lower partner
        self.at("mismatch loses part")
        lbl4 = T("new strand", size=28, color=TEAL, weight=BOLD).move_to([col_x(11, n14, dx14), 2.85, 0])
        ptr4 = make_gold_pointer(col_x(11, n14, dx14), -2.05, point_up=True)
        patch4_grp = VGroup(teal_seg, *[dup.upper[c] for c in z4])
        self.play(
            FadeIn(lbl4), FadeIn(ptr4),
            FadeOut(q11),
            *[dup.lower[c].animate.set_fill(GOLD, opacity=0.45).set_stroke(GOLD, width=5.0) for c in z4],
            *[FadeOut(dup.rungs[c]) for c in z4 if c != 11],
            patch4_grp.animate.shift(UP * 0.55).set_opacity(0),
            run_time=1.1,
        )
        g4 = VGroup(*[
            make_block(GREEN, bw14, bh14)
            .move_to([col_x(c, n14, dx14), y_d + 0.6, 0])
            .set_fill(GREEN, opacity=0.0)
            .set_stroke(GREEN, opacity=0.0)
            for c in z4
        ])
        self.add(g4)
        self.play(
            *[blk.animate.set_fill(GREEN, opacity=0.35).set_stroke(GREEN, opacity=1.0).move_to([col_x(c, n14, dx14), y_u, 0]) for blk, c in zip(g4, z4)],
            run_time=1.1,
        )
        self.play(
            *[dup.lower[c].animate.set_fill(BLUE, opacity=0.30) for c in z4],
            z3_focus.animate.move_to([col_x(z1, n14, dx14), 0, 0]).stretch_to_fit_width(1.65),
            run_time=1.5,
        )

        # Beat 5 (19.10): "limits its work" — turn all replaced green blocks blue, sweep focus scanner across all 4 zones
        self.at("limits its work")
        self.play(
            *[blk.animate.set_color(BLUE).set_fill(BLUE, opacity=0.30).set_stroke(BLUE, width=3.5) for blk in [g2, *g3, *g4]],
            z3_focus.animate.move_to([col_x(6, n14, dx14), 0, 0]),
            run_time=1.8,
        )
        self.play(
            z3_focus.animate.move_to([col_x(11, n14, dx14), 0, 0]),
            LaggedStart(
                Indicate(lbl1, color=TEAL),
                Indicate(lbl2, color=TEAL),
                Indicate(lbl3, color=TEAL),
                Indicate(lbl4, color=TEAL),
                lag_ratio=0.28,
            ),
            run_time=2.2,
        )
        self.play(FadeOut(z3_focus), run_time=0.4)

        # Beat 6 (23.80): "copy the intact partner" — upward gold copy guides + visible gold partner wave
        self.at("copy the intact partner")
        copy_cols = [z2] + z3 + z4
        copy_guides = VGroup(*[
            DashedLine(
                [col_x(c, n14, dx14), y_d + bh14 / 2 + 0.04, 0],
                [col_x(c, n14, dx14), y_u - bh14 / 2 - 0.04, 0],
                color=GOLD,
                stroke_width=4.5,
                dash_length=0.08,
            )
            for c in copy_cols
        ])
        self.play(
            Create(copy_guides),
            *[dup.lower[c].animate.set_fill(GOLD, opacity=0.52).scale(1.07) for c in copy_cols],
            ptr2.animate.shift(UP * 0.14),
            ptr3.animate.shift(UP * 0.14),
            ptr4.animate.shift(UP * 0.14),
            run_time=1.35,
        )
        self.play(
            *[dup.lower[c].animate.set_fill(BLUE, opacity=0.30).scale(1.0 / 1.07) for c in copy_cols],
            ptr2.animate.shift(DOWN * 0.14),
            ptr3.animate.shift(DOWN * 0.14),
            ptr4.animate.shift(DOWN * 0.14),
            FadeOut(copy_guides),
            run_time=1.35,
        )
        self.finish()


# ------------------------------------------------------------------ S10
class S10Consequence(SpokenScene):
    def construct(self):
        # Compact mini-duplex builder for the two moving outcome lanes
        def mini_pair(col_up=BLUE, col_dn=BLUE, w=0.52, h=0.60, alpha=1.0):
            u = make_block(col_up, w, h, fill_op=0.34 * alpha, stroke_w=3.0).set_stroke(opacity=alpha).move_to([0, 0.42, 0])
            d = make_block(col_dn, w, h, fill_op=0.34 * alpha, stroke_w=3.0).set_stroke(opacity=alpha).move_to([0, -0.42, 0])
            r = Line([0, -0.10, 0], [0, 0.10, 0], color=col_up, stroke_width=2.5, stroke_opacity=0.65 * alpha)
            return VGroup(r, u, d)

        def mini_strip(cols_up, cols_dn, spacing=0.64, alpha=1.0):
            g = VGroup()
            for idx, (cu, cd) in enumerate(zip(cols_up, cols_dn)):
                x = (idx - (len(cols_up) - 1) / 2.0) * spacing
                g.add(mini_pair(cu, cd, alpha=alpha).move_to([x, 0, 0]))
            return g

        # Top lane (y = +2.15): repaired strip moving smoothly rightward
        top_lane_bg = RoundedRectangle(
            corner_radius=0.16, width=11.8, height=1.85,
            stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.06,
        ).move_to([0, 2.05, 0])
        top_lane_bg.layout_ok = True
        lbl_restored = T("sequence restored", size=28, color=GREEN, weight=BOLD).move_to([-3.6, 3.25, 0])

        # Bottom lane (y = -1.90): unrepaired red block passes through schematic replication fork -> stable red pair
        bot_lane_bg = RoundedRectangle(
            corner_radius=0.16, width=11.8, height=2.05,
            stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.06,
        ).move_to([0, -1.85, 0])
        bot_lane_bg.layout_ok = True
        lbl_changed = T("sequence changed", size=28, color=RED, weight=BOLD).move_to([2.4, -3.15, 0])

        # Schematic Y-shaped replication fork centered around x = -1.0, y = -1.85
        fork = VGroup(
            Line([-2.2, -1.85, 0], [-0.9, -1.85, 0], color=GREY, stroke_width=4),
            Line([-0.9, -1.85, 0], [0.4, -1.35, 0], color=GREY, stroke_width=4),
            Line([-0.9, -1.85, 0], [0.4, -2.35, 0], color=GREY, stroke_width=4),
        )
        fork_tag = scope_tag("schematic")

        # Moving strips driven by continuous trackers (starting clear of fork tips x=0.40)
        top_x = ValueTracker(-4.2)
        bot_in_x = ValueTracker(-4.6)
        bot_in_op = ValueTracker(0.0)
        bot_out_x = ValueTracker(1.38)
        show_out = ValueTracker(0.0)

        top_strip = always_redraw(
            lambda: mini_strip([BLUE, GREEN, BLUE, BLUE], [BLUE, BLUE, BLUE, BLUE], alpha=1.0).move_to([top_x.get_value(), 2.05, 0])
        )
        bot_in_strip = always_redraw(
            lambda: mini_strip([BLUE, RED, BLUE], [BLUE, BLUE, BLUE], alpha=bot_in_op.get_value()).move_to([bot_in_x.get_value(), -1.85, 0])
        )
        bot_out_strip = always_redraw(
            lambda: mini_strip([BLUE, RED, BLUE], [BLUE, RED, BLUE], alpha=show_out.get_value()).move_to([bot_out_x.get_value(), -1.85, 0])
        )

        self.add(top_lane_bg, lbl_restored, top_strip, fork_tag, bot_in_strip)
        self.play(FadeIn(bot_lane_bg), Create(fork), bot_in_op.animate.set_value(1.0), run_time=1.0)

        # Beat 1 (2.26): "replication may turn" — red lesion enters fork, fades into fork, emerges as stable RED paired block
        self.at("replication may turn")
        self.add(bot_out_strip)
        self.play(
            top_x.animate.set_value(-2.8),
            bot_in_x.animate.set_value(-2.95),
            run_time=1.3,
            rate_func=linear,
        )
        self.play(
            top_x.animate.set_value(-2.2),
            bot_in_x.animate.set_value(-2.2),
            bot_in_op.animate.set_value(0.0),
            run_time=0.65,
            rate_func=linear,
        )
        self.remove(bot_in_strip)
        self.play(
            top_x.animate.set_value(-1.0),
            show_out.animate.set_value(1.0),
            bot_out_x.animate.set_value(2.05),
            FadeIn(lbl_changed, shift=UP * 0.1),
            run_time=1.9,
            rate_func=linear,
        )

        # Beat 2 (7.10): "Repair can also change" — highlight the stable red paired block & keep both lanes moving
        self.at("Repair can also change")
        self.play(
            top_x.animate.set_value(0.45),
            bot_out_x.animate.set_value(2.75),
            Indicate(lbl_changed, color=RED, scale_factor=1.06),
            run_time=2.8,
            rate_func=linear,
        )

        # Beat 3 (11.36): "That is why finding" — keep gliding while transitioning focus
        self.at("That is why finding")
        self.play(
            top_x.animate.set_value(1.75),
            bot_out_x.animate.set_value(3.35),
            run_time=2.6,
            rate_func=linear,
        )

        # Beat 4 (15.64): "The cell must also know" — keep labels crisp 1.0, dim lane borders only, reveal question cleanly
        self.at("The cell must also know")
        question = T("What information remains?", size=46, color=GOLD, weight=BOLD).move_to([0, 0.12, 0])
        self.play(
            top_lane_bg.animate.set_stroke(opacity=0.55).set_fill(opacity=0.03),
            bot_lane_bg.animate.set_stroke(opacity=0.55).set_fill(opacity=0.03),
            fork.animate.set_stroke(opacity=0.45),
            FadeIn(question, scale=0.96),
            top_x.animate.set_value(2.15),
            bot_out_x.animate.set_value(3.55),
            run_time=0.7,
            rate_func=linear,
        )
        self.play(
            top_x.animate.set_value(3.15),
            bot_out_x.animate.set_value(4.05),
            run_time=2.2,
            rate_func=linear,
        )

        # Beat 5 (20.54): "Follow that question" — keep both outcomes moving steadily through scene end
        self.at("Follow that question")
        self.play(
            top_x.animate.set_value(4.58),
            bot_out_x.animate.set_value(4.90),
            run_time=3.7,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ S11
class S11End(EndCard):
    LINE = "Repair outcomes depend on what is damaged and what intact information remains."
