"""
Glycolysis: Where the Profit Comes From — scenes.py

COLOUR MAP (one colour per concept for the entire film):
- BLUE    (#58C4DD) : carbon (the sugar and its three-carbon halves)
- YELLOW  (#F5D547) : ATP and any phosphate that came from ATP
- RED     (#FC6255) : ATP spent / blocked uphill transfer
- GREEN   (#83C167) : ATP earned / gain / favorable downhill transfer
- TEAL    (#3FB8C0) : NAD+
- PURPLE  (#B189F5) : NADH
- MAGENTA (#F264B6) : new phosphate captured from inorganic phosphate (Pi)
- GREY    (#8B93A1) : structure (phosphoryl-transfer ladder, enzyme clamp, empty ADP slots, axes)
- TEXT    (#E8EAF0) : primary text, electron dots, questions

ONE WORLD CARRIED FROM SCENE TO SCENE:
- Left 40% (x in [-5.8, -1.65], y in [-2.85, +2.55]): standard phosphoryl-transfer ladder to scale
  from ΔG°′ = −65 kJ/mol (top) to −10 kJ/mol (bottom).
- Top-right strip (y = +3.32): compact ATP ledger (spent 2 | earned 4 | net +2).
- Right side (x in [-0.5, +6.1]): the BLUE 3-carbon sugar half, step 6 GREY clamp, phosphate tokens,
  two GREY ADP slots, and (from s04 onward) the drifting MAGENTA inorganic phosphate pool at bottom.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question : Recap ledger coins slide out/in (2 spent, 4 earned, net +2), swap to top
                          strip while the 3C sugar half with 1 YELLOW phosphate and 2 empty ADP slots
                          rise with oscillating carbon dots and ghost arrows + "?" (arithmetic balance).
- s02_ladder            : Ladder built to scale from lesson ΔG°′ values (−10 to −65 kJ/mol); "more
                          negative = higher rung" up-arrow cue appears at top of axis; rungs light at
                          −30.5 and −13.8; GREEN downhill arrow enters ADP, RED uphill arrow
                          bounces at ATP; YELLOW token links to −13.8 and bobs.
- s03_step6_oxidation   : Step 6 GREY clamp closes on C1; TEAL NAD+ receives 2 hopping electron dots
                          to become PURPLE NADH; ghost heat lines rise & rewind; clamp link glows as
                          activated bond while −49.3 rung begins to glow.
- s04_new_rung          : MAGENTA Pi token rises from bottom pool, breaks activated bond and releases
                          1,3-BPG; −49.3 rung lights in MAGENTA above ATP while "more negative =
                          higher rung" pulses; at step 7 MAGENTA token slides down past ATP into
                          slot 1 -> MAGENTA-rimmed ATP coin (+1).
- s05_guiding_idea      : New MAGENTA-rimmed ATP coin glides to ledger under net +2 ("new") while NADH
                          pulses; remaining YELLOW token on sugar half pulses ("paid back").
- s06_predict           : Sugar half becomes 3-phosphoglycerate with YELLOW token tethered to −13.8
                          below ATP; slot 2 waits empty; faint −61.9 rung pulses; question card opens.
- s08_rearrange         : Carbon dots number 1-2-3; YELLOW token slides from C3 to C2; water droplet
                          leaves as bar tenses into PEP; schematic ΔG gauge twitches slightly; dotted
                          tether leaps from −13.8 up to PEP rung at −61.9.
- s09_why_pep           : Ghost preview lifts phosphate, wobbles unstable enol and settles to pyruvate,
                          then rewinds; real step 10 slides YELLOW token down from −61.9 to slot 2
                          ("paid back") leaving calm pyruvate.
- s10_ledger            : Second identical 3C half slides in; both halves show 4 ATP coins; 2 YELLOW
                          coins slide under 2 RED spent coins to repay them, 2 MAGENTA-rimmed coins bank
                          under net +2 beside 2 PURPLE NADH.
- s11_close             : Full world: spent/repaid coins fade to "0" ("break even"); MAGENTA trace links
                          net +2 coins back to −49.3 and step 6; 2 NADH pulse beside NAD+ regeneration
                          while Pi pool keeps drifting.
"""
import numpy as np
from bp_parts import *

# Additional concept colours (continuing film 1's map)
PURPLE = "#B189F5"       # NADH
MAGENTA = "#F264B6"      # new phosphate captured from inorganic phosphate
HEAT_ORANGE = "#FF8C42"  # heat-loss ghost lines in s03
WATER_BLUE = "#A8E0F0"   # water droplet in s08

# Shared world coordinates (safe frame x in [-6.3, 6.3], y in [-3.5, 3.5])
LAD_X0 = -5.25
LAD_X1 = -1.65
LAD_Y0 = -2.85
LAD_Y1 = 2.55
DG_BOT = -10.0
DG_TOP = -65.0

RUNGS = {
    "pep": (-61.9, "PEP −61.9", YELLOW, 24),
    "bpg": (-49.3, "1,3-BPG −49.3", MAGENTA, 24),
    "atp": (-30.5, "ATP −30.5", YELLOW, 24),
    "est": (-13.8, "ordinary ester −13.8", TEXT, 22),
}

BAR_CENTER = np.array([1.30, 0.10, 0.0])
BAR_W = 3.00
BAR_H = 1.05
SLOT1_POS = np.array([5.25, 0.65, 0.0])
SLOT2_POS = np.array([5.25, -0.85, 0.0])
NADH_CORNER = np.array([5.25, 1.85, 0.0])
LEDGER_POS = np.array([3.05, 3.32, 0.0])


def dg_to_y(dg):
    """Linear scale mapping standard hydrolysis ΔG°′ (kJ/mol) in [-10, -65] to scene y."""
    frac = (DG_BOT - dg) / (DG_BOT - DG_TOP)
    return LAD_Y0 + frac * (LAD_Y1 - LAD_Y0)


def make_phosphate_token(color=YELLOW, radius=0.34, label="P", text_color=TEXT):
    """Round phosphate token with ample border clearance around P."""
    c = Circle(radius=radius, stroke_color=color, stroke_width=4.0,
               fill_color=color, fill_opacity=0.24)
    t = T(label, size=24, color=text_color, weight=BOLD).move_to(c)
    g = VGroup(c, t)
    g.ring = c
    g.txt = t
    return g


def make_coin(label="ATP", rim_color=YELLOW, text_color=TEXT, radius=0.46, font_size=22):
    """ATP coin with ample clearance so text never touches or overflows the rim."""
    c = Circle(radius=radius, stroke_color=rim_color, stroke_width=4.5,
               fill_color=YELLOW if rim_color != GREY else BG,
               fill_opacity=0.22 if rim_color != GREY else 0.65)
    t = T(label, size=font_size, color=text_color, weight=BOLD).move_to(c)
    g = VGroup(c, t)
    g.ring = c
    g.txt = t
    return g


def make_nad_pill(label="NAD+", color=TEAL):
    """Rounded pill for NAD+ / NADH with generous padding."""
    box = RoundedRectangle(corner_radius=0.22, width=1.55, height=0.76,
                           stroke_color=color, stroke_width=3.5,
                           fill_color=color, fill_opacity=0.24)
    txt = T(label, size=24, color=color, weight=BOLD).move_to(box)
    g = VGroup(box, txt)
    g.box = box
    g.txt = txt
    return g


def make_adp_slot(pos, label="ADP"):
    """Empty GREY ADP slot waiting for a phosphate."""
    box = RoundedRectangle(corner_radius=0.20, width=1.50, height=0.86,
                           stroke_color=GREY, stroke_width=3.0,
                           fill_color=GREY, fill_opacity=0.14).move_to(pos)
    txt = T(label, size=24, color=TEXT).move_to(box)
    g = VGroup(box, txt)
    g.box = box
    g.txt = txt
    return g


def make_sugar_half(center=BAR_CENTER, width=BAR_W, height=BAR_H,
                    corner_radius=0.26, numbered=False, tense=False):
    """BLUE rounded bar with three BLUE carbon dots (no molecular structure)."""
    cr = 0.10 if tense else corner_radius
    bar = RoundedRectangle(corner_radius=cr, width=width, height=height,
                           stroke_color=BLUE, stroke_width=4.5 if tense else 3.8,
                           fill_color=BLUE, fill_opacity=0.22).move_to(center)
    xs = [center[0] - width * 0.30, center[0], center[0] + width * 0.30]
    dot_y = center[1] + (0.14 if numbered else 0.0)
    dots = VGroup()
    nums = VGroup()
    for idx, x in enumerate(xs, start=1):
        d = Dot([x, dot_y, 0], radius=0.16, color=BLUE)
        dots.add(d)
        if numbered:
            n = T(str(idx), size=22, color=TEXT, weight=BOLD).move_to([x, center[1] - 0.22, 0])
            nums.add(n)
    g = VGroup(bar, dots)
    if numbered:
        g.add(nums)
    g.bar = bar
    g.dots = dots
    g.nums = nums
    return g


def attach_carbon_jiggle(dots, amp=0.04, speed=2.6):
    """Gentle computed thermal motion on the three carbon dots inside the bar."""
    bases = [d.get_center().copy() for d in dots]
    for i, d in enumerate(dots):
        d._jt = i * 1.4
        base = bases[i]

        def u(mob, dt, b=base, s=speed + 0.3 * i):
            mob._jt += dt
            mob.move_to(b + UP * amp * np.sin(s * mob._jt) + RIGHT * (amp * 0.6) * np.cos(0.8 * s * mob._jt))
        d.add_updater(u)


def make_ladder(lit=("atp", "est"), faint=("bpg", "pep"), show_more_neg=True):
    """Build the phosphoryl-transfer ladder to scale from ΔG°′ = −10 to −65 kJ/mol."""
    left_rail = Line([LAD_X0, LAD_Y0, 0], [LAD_X0, LAD_Y1, 0], color=GREY, stroke_width=4.0)
    right_rail = Line([LAD_X1, LAD_Y0, 0], [LAD_X1, LAD_Y1, 0], color=GREY, stroke_width=3.0)
    ticks = VGroup()
    tlabels = VGroup()
    for dg in (-10, -20, -30, -40, -50, -60):
        y = dg_to_y(dg)
        tk = Line([LAD_X0 - 0.14, y, 0], [LAD_X0, y, 0], color=GREY, stroke_width=3.0)
        tl = M(f"−{abs(dg)}", size=22, color=TEXT).next_to(tk, LEFT, buff=0.10)
        ticks.add(tk)
        tlabels.add(tl)

    axis_title = T("ΔG°′ of hydrolysis (kJ/mol)", size=24, color=TEXT).move_to([-3.55, 3.22, 0])
    up_arr = Arrow([0, -0.16, 0], [0, 0.16, 0], color=TEXT, stroke_width=4.0, buff=0, max_tip_length_to_length_ratio=0.45)
    more_neg_txt = T("more negative = higher rung", size=22, color=TEXT, weight=BOLD)
    more_neg_tag = VGroup(up_arr, more_neg_txt).arrange(RIGHT, buff=0.12).move_to([-3.80, 2.82, 0])

    rungs = {}
    rung_group = VGroup()
    for key, (dg, label, col, fsz) in RUNGS.items():
        y = dg_to_y(dg)
        if key in lit:
            bar = Line([LAD_X0, y, 0], [LAD_X1, y, 0], color=col, stroke_width=6.0)
            lab = T(label, size=fsz, color=col, weight=BOLD).next_to(bar, UP, buff=0.10)
            rg = VGroup(bar, lab)
            rg.bar = bar
            rg.lab = lab
            rungs[key] = rg
            rung_group.add(rg)
        elif key in faint:
            bar = DashedLine([LAD_X0, y, 0], [LAD_X1, y, 0], color=GREY, stroke_width=3.0, dash_length=0.16)
            rg = VGroup(bar)
            rg.bar = bar
            rg.lab = None
            rungs[key] = rg
            rung_group.add(rg)

    g = VGroup(left_rail, right_rail, ticks, tlabels, axis_title)
    if show_more_neg:
        g.add(more_neg_tag)
    g.add(rung_group)
    g.rungs = rungs
    g.axis_title = axis_title
    g.more_neg_tag = more_neg_tag
    return g


def make_elbow_tether(start_fn, target_y, color=YELLOW, mid_x=-0.95):
    """Orthogonal dashed tether routed strictly clear of the sugar bar and all labels."""
    def mk():
        p0 = start_fn()
        p2 = np.array([LAD_X1 + 0.05, target_y, 0.0])
        bar_top = BAR_CENTER[1] + BAR_H / 2 + 0.05
        if p0[0] < 0.0:
            # Left-side token linking to upper rung: left to mid_x, then up/down to target_y
            pts = [p0, [mid_x, p0[1], 0.0], [mid_x, target_y, 0.0], p2]
        elif p0[1] > bar_top and target_y < BAR_CENTER[1]:
            # Token sits above the bar linking to low rung: go LEFT past bar first, then down in open corridor
            pts = [p0, [mid_x, p0[1], 0.0], [mid_x, target_y, 0.0], p2]
        elif target_y > p0[1]:
            # Token linking to top rung: go UP clear of bar, then left to rung
            clear_y = max(p0[1] + 0.55, target_y)
            pts = [p0, [p0[0], clear_y, 0.0], [mid_x, clear_y, 0.0], [mid_x, target_y, 0.0], p2]
        else:
            # Right-side token beside bar linking to low rung: straight down below bar & labels, then left
            pts = [p0, [p0[0], target_y, 0.0], p2]
        path = VMobject(stroke_color=color, stroke_width=3.0)
        path.set_points_as_corners([np.array(q, dtype=float) for q in pts])
        return DashedVMobject(path, num_dashes=max(8, int(path.get_arc_length() * 4)))
    return always_redraw(mk)


def make_compact_ledger(pos=LEDGER_POS):
    """Compact top-edge ledger strip carried across scenes."""
    frame = RoundedRectangle(corner_radius=0.14, width=6.10, height=0.58,
                             stroke_color=GREY, stroke_width=2.5,
                             fill_color=BG, fill_opacity=0.92).move_to(pos)
    s_txt = T("spent 2", size=24, color=RED, weight=BOLD)
    e_txt = T("earned 4", size=24, color=GREEN, weight=BOLD)
    n_txt = T("net +2", size=24, color=GREEN, weight=BOLD)
    row = VGroup(s_txt, T("|", 24, GREY), e_txt, T("|", 24, GREY), n_txt).arrange(RIGHT, buff=0.22).move_to(frame)
    g = VGroup(frame, row)
    g.frame = frame
    g.spent = s_txt
    g.earned = e_txt
    g.net = n_txt
    return g


def make_enzyme_clamp(center):
    """Simple rounded C-clamp representing the step 6 enzyme (no molecular structure)."""
    top_jaw = RoundedRectangle(corner_radius=0.12, width=0.95, height=0.34,
                               stroke_color=GREY, stroke_width=3.5,
                               fill_color=GREY, fill_opacity=0.28).move_to(center + UP * 0.44 + RIGHT * 0.15)
    bot_jaw = RoundedRectangle(corner_radius=0.12, width=0.95, height=0.34,
                               stroke_color=GREY, stroke_width=3.5,
                               fill_color=GREY, fill_opacity=0.28).move_to(center + DOWN * 0.44 + RIGHT * 0.15)
    spine = RoundedRectangle(corner_radius=0.12, width=0.40, height=1.22,
                             stroke_color=GREY, stroke_width=3.5,
                             fill_color=GREY, fill_opacity=0.28).move_to(center + LEFT * 0.25)
    g = VGroup(spine, top_jaw, bot_jaw)
    g.spine, g.top_jaw, g.bot_jaw = spine, top_jaw, bot_jaw
    return g


def make_pi_pool(seed=7, x_range=(0.0, 4.4), y_range=(-3.42, -2.72), n=10):
    """Pool of drifting MAGENTA inorganic phosphate dots strictly below the -13.8 tether."""
    rng = np.random.default_rng(seed)
    pool = VGroup()
    for i in range(n):
        x0 = rng.uniform(x_range[0] + 0.15, x_range[1] - 0.15)
        y0 = rng.uniform(y_range[0] + 0.12, y_range[1] - 0.12)
        vx = rng.uniform(0.20, 0.36) * (1 if i % 2 == 0 else -1)
        vy = rng.uniform(0.08, 0.18) * (1 if (i // 2) % 2 == 0 else -1)
        d = Dot([x0, y0, 0], radius=0.10, color=MAGENTA)
        d._vx, d._vy = vx, vy

        def drift(m, dt, xr=x_range, yr=y_range):
            p = m.get_center() + np.array([m._vx * dt, m._vy * dt, 0.0])
            if p[0] < xr[0] + 0.12 or p[0] > xr[1] - 0.12:
                m._vx *= -1
                p[0] = np.clip(p[0], xr[0] + 0.12, xr[1] - 0.12)
            if p[1] < yr[0] + 0.12 or p[1] > yr[1] - 0.12:
                m._vy *= -1
                p[1] = np.clip(p[1], yr[0] + 0.12, yr[1] - 0.12)
            m.move_to(p)
        d.add_updater(drift)
        pool.add(d)
    return pool


def make_transfer_arrow(start_pt, end_pt, via_x=3.95, via_y=1.35, color=GREEN):
    """Clean elbow arrow from a ladder rung into an ADP slot without crossing bar, NADH, or slots."""
    pts = [
        np.array(start_pt, dtype=float),
        np.array([via_x, start_pt[1], 0.0]) if abs(start_pt[1] - via_y) < 0.5 else np.array([-0.85, start_pt[1], 0.0]),
        np.array([-0.85, via_y, 0.0]) if abs(start_pt[1] - via_y) >= 0.5 else np.array([via_x, start_pt[1], 0.0]),
        np.array([via_x, via_y, 0.0]),
        np.array([via_x, end_pt[1], 0.0]),
        np.array(end_pt, dtype=float),
    ]
    # Simplify straight corridor for high rungs
    if start_pt[1] > 1.8:
        pts = [
            np.array(start_pt, dtype=float),
            np.array([via_x, start_pt[1], 0.0]),
            np.array([via_x, end_pt[1], 0.0]),
            np.array(end_pt, dtype=float),
        ]
    else:
        pts = [
            np.array(start_pt, dtype=float),
            np.array([-0.85, start_pt[1], 0.0]),
            np.array([-0.85, via_y, 0.0]),
            np.array([via_x, via_y, 0.0]),
            np.array([via_x, end_pt[1], 0.0]),
            np.array(end_pt, dtype=float),
        ]
    vm = VMobject(stroke_color=color, stroke_width=4.5)
    vm.set_points_as_corners(pts)
    tip = Triangle(color=color, fill_color=color, fill_opacity=1.0).scale(0.14)
    d = pts[-1] - pts[-2]
    ang = np.arctan2(d[1], d[0])
    tip.rotate(ang - PI / 2).move_to(pts[-1])
    return VGroup(vm, tip)


# ==============================================================================
# SCENES
# ==============================================================================

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        spent_coins = VGroup(*[make_coin("ATP", RED, TEXT, radius=0.44, font_size=22) for _ in range(2)]).arrange(RIGHT, buff=0.16)
        spent_lab = T("spent 2", size=28, color=RED, weight=BOLD).next_to(spent_coins, DOWN, buff=0.18)
        spent_grp = VGroup(spent_coins, spent_lab)

        earned_coins = VGroup(*[make_coin("ATP", GREEN, TEXT, radius=0.44, font_size=22) for _ in range(4)]).arrange(RIGHT, buff=0.14)
        earned_lab = T("earned 4", size=28, color=GREEN, weight=BOLD).next_to(earned_coins, DOWN, buff=0.18)
        earned_grp = VGroup(earned_coins, earned_lab)

        net_box = RoundedRectangle(corner_radius=0.16, width=2.2, height=0.88,
                                   stroke_color=GREEN, stroke_width=3.5,
                                   fill_color=GREEN, fill_opacity=0.22)
        net_lab = T("net +2", size=30, color=GREEN, weight=BOLD).move_to(net_box)
        net_grp = VGroup(net_box, net_lab)

        recap = VGroup(spent_grp, earned_grp, net_grp).arrange(RIGHT, buff=0.65).move_to([0, 1.95, 0])

        self.at("the arithmetic")
        self.play(FadeIn(spent_coins, shift=LEFT * 0.3), FadeIn(spent_lab), run_time=self.beat(0.08))

        self.at("earn four")
        self.play(FadeIn(earned_coins, shift=RIGHT * 0.3), FadeIn(earned_lab), run_time=self.beat(0.08))

        self.at("keep two")
        self.play(FadeIn(net_grp, scale=0.92), run_time=self.beat(0.07))

        compact = make_compact_ledger(pos=[3.05, 3.28, 0])
        sugar = make_sugar_half(center=[-1.55, -0.75, 0], width=4.8, height=1.75, corner_radius=0.35)
        attach_carbon_jiggle(sugar.dots, amp=0.05, speed=2.8)
        p_tok = make_phosphate_token(YELLOW, radius=0.36).move_to([1.35, -0.75, 0])
        p_lab = T("one ordinary phosphate", size=28, color=YELLOW).next_to(sugar, DOWN, buff=0.35)
        slot_a = make_adp_slot([4.35, 0.25, 0])
        slot_b = make_adp_slot([4.35, -1.75, 0])

        self.at("each half")
        self.play(FadeOut(recap, run_time=0.25))
        self.play(
            FadeIn(compact),
            FadeIn(sugar, shift=UP * 0.2),
            FadeIn(slot_a), FadeIn(slot_b),
            run_time=self.beat(0.11),
        )

        self.at("one ordinary phosphate")
        self.play(FadeIn(p_tok, scale=0.85), FadeIn(p_lab), run_time=self.beat(0.09))

        q_title = T("One phosphate in, two out?", size=40, color=TEXT, weight=BOLD).move_to([-2.0, 2.05, 0])
        arr_a = DashedVMobject(
            Line(p_tok.get_right() + RIGHT * 0.08 + UP * 0.10, slot_a.get_left() + LEFT * 0.10,
                 color=TEXT, stroke_width=3.5), num_dashes=10
        )
        arr_b = DashedVMobject(
            Line(p_tok.get_right() + RIGHT * 0.08 + DOWN * 0.10, [3.05, -1.55, 0],
                 color=RED, stroke_width=3.5), num_dashes=7
        )
        q_mark = T("?", size=54, color=TEXT, weight=BOLD).move_to([3.0, -0.75, 0])

        self.at("how does each half")
        self.play(
            FadeIn(q_title, shift=DOWN * 0.12),
            Create(arr_a), Create(arr_b),
            FadeIn(q_mark, scale=0.85),
            run_time=self.beat(0.13),
        )
        self.finish()


class S01Title(TitleCard):
    LESSON = "Glycolysis: The Investment-and-Payoff Pathway"
    TITLE = "Where the Profit Comes From"


class S02Ladder(SpokenScene):
    def construct(self):
        ledger = make_compact_ledger()
        ladder = make_ladder(lit=(), faint=(), show_more_neg=False)
        sugar = make_sugar_half()
        attach_carbon_jiggle(sugar.dots)
        p_tok = make_phosphate_token(YELLOW).move_to([BAR_CENTER[0] + BAR_W / 2 + 0.45, BAR_CENTER[1], 0])
        slot1 = make_adp_slot(SLOT1_POS)
        slot2 = make_adp_slot(SLOT2_POS)

        self.play(
            FadeIn(ledger),
            Create(ladder),
            FadeIn(sugar), FadeIn(p_tok),
            FadeIn(slot1), FadeIn(slot2),
            run_time=self.beat(0.07),
        )

        self.at("ranked by")
        bpg_faint = DashedLine([LAD_X0, dg_to_y(-49.3), 0], [LAD_X1, dg_to_y(-49.3), 0], color=GREY, stroke_width=3.0, dash_length=0.16)
        pep_faint = DashedLine([LAD_X0, dg_to_y(-61.9), 0], [LAD_X1, dg_to_y(-61.9), 0], color=GREY, stroke_width=3.0, dash_length=0.16)
        self.play(Create(bpg_faint), Create(pep_faint), run_time=self.beat(0.06))

        self.at("more negative means higher")
        self.play(FadeIn(ladder.more_neg_tag, shift=UP * 0.10), run_time=self.beat(0.05))

        self.at("leaves more eagerly")
        self.play(ladder.more_neg_tag.animate.scale(1.06), rate_func=there_and_back, run_time=0.6)

        self.at("sits at")
        atp_bar = Line([LAD_X0, dg_to_y(-30.5), 0], [LAD_X1, dg_to_y(-30.5), 0], color=YELLOW, stroke_width=6.0)
        self.play(Create(atp_bar), run_time=0.55)

        self.at("minus 30", lead=0.1)
        atp_lab = T("ATP −30.5", size=24, color=YELLOW, weight=BOLD).next_to(atp_bar, UP, buff=0.10)
        self.play(FadeIn(atp_lab), run_time=0.65)

        self.at("a kinase")
        est_bar = Line([LAD_X0, dg_to_y(-13.8), 0], [LAD_X1, dg_to_y(-13.8), 0], color=TEXT, stroke_width=5.5)
        est_lab = T("ordinary ester −13.8", size=22, color=TEXT, weight=BOLD).next_to(est_bar, UP, buff=0.10)
        self.play(Create(est_bar), FadeIn(est_lab), run_time=0.75)

        self.at("only from a higher rung")
        g_start = np.array([LAD_X1 + 0.12, dg_to_y(-45.0), 0])
        g_end = SLOT1_POS + UP * 0.50
        g_path = VMobject(stroke_color=GREEN, stroke_width=4.5)
        g_path.set_points_as_corners([g_start, [-0.85, g_start[1], 0], [-0.85, 1.45, 0], [SLOT1_POS[0], 1.45, 0], g_end])
        g_tip = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1.0).scale(0.14).rotate(PI).move_to(g_end)
        r_start = np.array([LAD_X1 + 0.25, dg_to_y(-13.8), 0])
        r_top = np.array([LAD_X1 + 0.25, dg_to_y(-28.0), 0])
        r_arr = Arrow(r_start, r_top, color=RED, stroke_width=5.0, buff=0)
        cross = VGroup(
            Line([-0.16, -0.16, 0], [0.16, 0.16, 0], color=RED, stroke_width=5.0),
            Line([-0.16, 0.16, 0], [0.16, -0.16, 0], color=RED, stroke_width=5.0),
        ).move_to([LAD_X1 + 0.65, dg_to_y(-22.0), 0])
        self.play(Create(g_path), FadeIn(g_tip), Create(r_arr), run_time=self.beat(0.08))
        self.play(r_arr.animate.shift(DOWN * 0.35), FadeIn(cross), run_time=self.beat(0.05))

        self.at("is an ordinary")
        tether = make_elbow_tether(lambda: p_tok.get_bottom() + DOWN * 0.05, dg_to_y(-13.8), color=YELLOW)
        g6p_tag = T("like glucose-6-phosphate", size=24, color=YELLOW).move_to([0.95, -0.95, 0])
        self.add(tether)
        self.play(FadeIn(g6p_tag), run_time=0.7)
        bob(p_tok, amp=0.06, speed=2.6)

        self.at("far below", lead=0.1)
        self.play(g6p_tag.animate.scale(1.05), rate_func=there_and_back, run_time=0.6)
        self.finish()


class S03Step6Oxidation(SpokenScene):
    def construct(self):
        ledger = make_compact_ledger()
        ladder = make_ladder(lit=("atp", "est"), faint=("bpg", "pep"))
        sugar = make_sugar_half()
        attach_carbon_jiggle(sugar.dots)
        p_tok = make_phosphate_token(YELLOW).move_to([BAR_CENTER[0] + BAR_W / 2 + 0.45, BAR_CENTER[1], 0])
        bob(p_tok, amp=0.05, speed=2.5)
        tether = make_elbow_tether(lambda: p_tok.get_bottom() + DOWN * 0.05, dg_to_y(-13.8), color=YELLOW)
        slot1 = make_adp_slot(SLOT1_POS)
        slot2 = make_adp_slot(SLOT2_POS)
        self.add(ledger, ladder, sugar, p_tok, tether, slot1, slot2)

        self.at("builds a higher rung")
        bpg_bar = ladder.rungs["bpg"].bar
        self.play(bpg_bar.animate.set_stroke(color=MAGENTA, opacity=0.75), run_time=self.beat(0.08))

        self.at("at step 6")
        clamp = make_enzyme_clamp(np.array([BAR_CENTER[0] - BAR_W / 2 - 0.15, BAR_CENTER[1], 0]))
        clamp_lab = T("step 6 enzyme", size=24, color=TEXT).next_to(clamp, DOWN, buff=0.22)
        self.play(FadeIn(clamp, shift=LEFT * 0.3), FadeIn(clamp_lab), run_time=self.beat(0.08))

        self.at("nad plus")
        nad = make_nad_pill("NAD+", TEAL).move_to([1.1, 1.95, 0])
        self.play(FadeIn(nad, shift=DOWN * 0.25), run_time=self.beat(0.07))

        self.at("takes the electrons")
        e1 = Dot([BAR_CENTER[0] - 0.85, BAR_CENTER[1] + 0.30, 0], radius=0.09, color=TEXT)
        e2 = Dot([BAR_CENTER[0] - 0.55, BAR_CENTER[1] + 0.30, 0], radius=0.09, color=TEXT)
        self.play(FadeIn(e1), FadeIn(e2), run_time=self.beat(0.03))
        nadh_txt = T("NADH", size=24, color=PURPLE, weight=BOLD).move_to(nad.box)
        self.play(
            e1.animate.move_to(nad.box.get_left() + LEFT * 0.15 + UP * 0.12),
            e2.animate.move_to(nad.box.get_left() + LEFT * 0.15 + DOWN * 0.12),
            run_time=self.beat(0.07),
        )
        self.play(
            FadeOut(e1), FadeOut(e2),
            nad.box.animate.set_stroke(color=PURPLE).set_fill(color=PURPLE, opacity=0.24),
            swap(nad.txt, nadh_txt, run_time=self.beat(0.05)),
            run_time=self.beat(0.06),
        )
        nadh = VGroup(nad.box, nadh_txt)
        self.play(nadh.animate.move_to(NADH_CORNER), run_time=self.beat(0.08))

        self.at("lost as heat")
        waves = VGroup()
        for k in range(3):
            xs = np.linspace(0, 0.35, 16)
            pts = [[BAR_CENTER[0] - 0.6 + k * 0.45 + 0.12 * np.sin(14 * t), BAR_CENTER[1] + 0.65 + t * 2.4, 0] for t in xs]
            w = VMobject(stroke_color=HEAT_ORANGE, stroke_width=4.0).set_points_as_corners(pts)
            waves.add(w)
        heat_tag = T("one go: heat", size=24, color=HEAT_ORANGE, weight=BOLD).next_to(waves, UP, buff=0.14)
        self.play(Create(waves), FadeIn(heat_tag), run_time=self.beat(0.04))
        self.play(FadeOut(waves, shift=UP * 0.3), FadeOut(heat_tag), run_time=self.beat(0.04))

        self.at("instead")
        bond = Line([BAR_CENTER[0] - BAR_W / 2 - 0.12, BAR_CENTER[1], 0],
                    [BAR_CENTER[0] - BAR_W / 2 + 0.18, BAR_CENTER[1], 0],
                    color=YELLOW, stroke_width=10.0)
        bond_lab = T("activated bond", size=24, color=YELLOW, weight=BOLD).move_to([BAR_CENTER[0] - 1.15, 1.35, 0])
        self.play(FadeIn(bond), FadeIn(bond_lab), run_time=self.beat(0.07))

        self.at("activated bond")
        pulse(bond, base=9.0, amp=3.5, speed=5.0)
        bpg_glow = Line([LAD_X0, dg_to_y(-49.3), 0], [LAD_X1, dg_to_y(-49.3), 0], color=MAGENTA, stroke_width=5.5)
        pulse(bpg_glow, base=5.5, amp=2.5, speed=4.0)
        self.play(Create(bpg_glow), run_time=self.beat(0.06))
        self.finish()


class S04NewRung(SpokenScene):
    def construct(self):
        ledger = make_compact_ledger()
        ladder = make_ladder(lit=("atp", "est"), faint=("bpg", "pep"))
        bpg_glow = Line([LAD_X0, dg_to_y(-49.3), 0], [LAD_X1, dg_to_y(-49.3), 0], color=MAGENTA, stroke_width=5.0)
        sugar = make_sugar_half()
        attach_carbon_jiggle(sugar.dots)
        p_old = make_phosphate_token(YELLOW).move_to([BAR_CENTER[0] + BAR_W / 2 + 0.45, BAR_CENTER[1], 0])
        bob(p_old, amp=0.05, speed=2.5)
        tether_old = make_elbow_tether(lambda: p_old.get_bottom() + DOWN * 0.05, dg_to_y(-13.8), color=YELLOW)
        slot1 = make_adp_slot(SLOT1_POS)
        slot2 = make_adp_slot(SLOT2_POS)
        clamp = make_enzyme_clamp(np.array([BAR_CENTER[0] - BAR_W / 2 - 0.15, BAR_CENTER[1], 0]))
        clamp_lab = T("step 6 enzyme", size=24, color=TEXT).next_to(clamp, DOWN, buff=0.22)
        bond = Line([BAR_CENTER[0] - BAR_W / 2 - 0.12, BAR_CENTER[1], 0],
                    [BAR_CENTER[0] - BAR_W / 2 + 0.18, BAR_CENTER[1], 0],
                    color=YELLOW, stroke_width=10.0)
        pulse(bond, base=9.0, amp=3.5, speed=5.0)
        bond_lab = T("activated bond", size=24, color=YELLOW, weight=BOLD).move_to([BAR_CENTER[0] - 1.15, 1.35, 0])
        nadh = make_nad_pill("NADH", PURPLE).move_to(NADH_CORNER)

        pi_pool = make_pi_pool(seed=7)
        pool_lab = T("Pi pool", size=24, color=MAGENTA).move_to([5.25, -3.05, 0])
        self.add(ledger, ladder, bpg_glow, sugar, p_old, tether_old, slot1, slot2,
                 clamp, clamp_lab, bond, bond_lab, nadh, pi_pool, pool_lab)

        self.at("inorganic phosphate")
        pi_tok = make_phosphate_token(MAGENTA).move_to([0.35, -2.95, 0])
        self.play(FadeIn(pi_tok), run_time=0.4)
        pi_target = np.array([-0.85, -1.75, 0])
        pi_lab = T("inorganic phosphate", size=22, color=MAGENTA, weight=BOLD).move_to([1.15, -1.75, 0])
        self.play(pi_tok.animate.move_to(pi_target), FadeIn(pi_lab), run_time=0.9)

        self.at("the cell's pool")
        self.play(pool_lab.animate.scale(1.08), rate_func=there_and_back, run_time=0.6)

        self.at("attacks that bond")
        bpg_name = T("1,3-BPG", size=26, color=BLUE, weight=BOLD).move_to([BAR_CENTER[0], -0.85, 0])
        left_end = np.array([BAR_CENTER[0] - BAR_W / 2 - 0.45, BAR_CENTER[1], 0])
        self.play(FadeOut(clamp, shift=LEFT * 0.3), FadeOut(clamp_lab), FadeOut(bond), FadeOut(bond_lab), run_time=0.25)
        self.play(
            pi_tok.animate.move_to(left_end),
            FadeOut(pi_lab),
            FadeIn(bpg_name),
            run_time=self.beat(0.08),
        )

        self.at("new phosphate")
        bpg_glow.clear_updaters()
        bpg_glow.set_stroke(width=6.0)
        tether_new = make_elbow_tether(lambda: pi_tok.get_left() + LEFT * 0.05, dg_to_y(-49.3), color=MAGENTA, mid_x=-1.15)
        self.add(tether_new)
        bpg_short = T("1,3-BPG", size=24, color=MAGENTA, weight=BOLD).next_to(bpg_glow, UP, buff=0.10)
        self.play(FadeIn(bpg_short), run_time=0.6)

        self.at("minus 49", lead=0.1)
        bpg_lab = T("1,3-BPG −49.3", size=24, color=MAGENTA, weight=BOLD).next_to(bpg_glow, UP, buff=0.10)
        self.play(swap(bpg_short, bpg_lab, run_time=0.7))

        self.at("more negative")
        self.play(ladder.more_neg_tag.animate.scale(1.10), rate_func=there_and_back, run_time=0.8)

        self.at("at step 7")
        arr_7 = make_transfer_arrow([LAD_X1 + 0.08, dg_to_y(-49.3), 0], slot1.get_left() + LEFT * 0.08, via_x=3.95, via_y=1.35, color=GREEN)
        self.play(Create(arr_7), run_time=0.8)

        self.at("a kinase hands")
        self.remove(tether_new)
        new_atp = make_coin("ATP", rim_color=MAGENTA, text_color=TEXT, radius=0.46, font_size=22).move_to(SLOT1_POS)
        plus1 = T("+1", size=28, color=GREEN, weight=BOLD).move_to([SLOT1_POS[0] - 1.10, SLOT1_POS[1], 0])
        pg_name = T("3-phosphoglycerate", size=24, color=BLUE, weight=BOLD).move_to(bpg_name)
        self.play(FadeOut(arr_7), run_time=0.20)
        self.play(
            pi_tok.animate.move_to(slot1.get_left() + LEFT * 0.42),
            swap(bpg_name, pg_name, run_time=0.65),
            run_time=0.75,
        )
        self.play(
            FadeOut(pi_tok), FadeOut(slot1),
            FadeIn(new_atp), FadeIn(plus1, shift=UP * 0.15),
            run_time=0.60,
        )
        self.finish()


class S05GuidingIdea(SpokenScene):
    def construct(self):
        ledger = make_compact_ledger()
        ladder = make_ladder(lit=("bpg", "atp", "est"), faint=("pep",))
        sugar = make_sugar_half()
        attach_carbon_jiggle(sugar.dots)
        p_old = make_phosphate_token(YELLOW).move_to([BAR_CENTER[0] + BAR_W / 2 + 0.45, BAR_CENTER[1], 0])
        bob(p_old, amp=0.05, speed=2.5)
        tether_old = make_elbow_tether(lambda: p_old.get_bottom() + DOWN * 0.05, dg_to_y(-13.8), color=YELLOW)
        pg_name = T("3-phosphoglycerate", size=24, color=BLUE, weight=BOLD).move_to([BAR_CENTER[0], -0.85, 0])
        new_atp = make_coin("ATP", rim_color=MAGENTA, text_color=TEXT, radius=0.46, font_size=22).move_to(SLOT1_POS)
        slot2 = make_adp_slot(SLOT2_POS)
        nadh = make_nad_pill("NADH", PURPLE).move_to(NADH_CORNER)
        pi_pool = make_pi_pool(seed=7)
        pool_lab = T("Pi pool", size=24, color=MAGENTA).move_to([5.25, -3.05, 0])
        self.add(ledger, ladder, sugar, p_old, tether_old, pg_name, new_atp, slot2, nadh, pi_pool, pool_lab)

        self.at("idea to hold")
        idea_txt = T("Net gain = new phosphate", size=24, color=TEXT, weight=BOLD).move_to([1.05, 2.20, 0])
        self.play(FadeIn(idea_txt, shift=DOWN * 0.12), run_time=self.beat(0.11))

        self.at("the net gain")
        new_tag = T("new", size=22, color=MAGENTA, weight=BOLD).move_to([3.95, 1.72, 0])
        self.play(
            new_atp.animate.move_to([3.95, 0.65, 0]),
            run_time=self.beat(0.05),
        )
        self.play(
            new_atp.animate.move_to([3.95, 2.45, 0]),
            run_time=self.beat(0.07),
        )
        self.play(FadeIn(new_tag), run_time=self.beat(0.03))

        self.at("this oxidation captures")
        self.play(
            nadh.box.animate.set_stroke(width=7.5),
            rate_func=there_and_back, run_time=self.beat(0.14),
        )

        self.at("everything else")
        paid_tag = T("paid back", size=24, color=YELLOW, weight=BOLD).move_to([3.25, 1.05, 0])
        halo = Circle(radius=0.44, stroke_color=TEXT, stroke_width=4.5).move_to(p_old.get_center())
        self.play(FadeIn(paid_tag), FadeIn(halo), run_time=self.beat(0.10))
        self.at("only paid back")
        self.play(FadeOut(halo), run_time=self.beat(0.08))
        self.finish()


def world_after_s06(with_pi=True):
    """Shared builder for end of S06Predict and S07PredictPause."""
    ledger = make_compact_ledger()
    ladder = make_ladder(lit=("bpg", "atp", "est"), faint=("pep",))
    sugar = make_sugar_half()
    attach_carbon_jiggle(sugar.dots)
    p_old = make_phosphate_token(YELLOW).move_to([BAR_CENTER[0] + BAR_W / 2 + 0.45, BAR_CENTER[1], 0])
    bob(p_old, amp=0.05, speed=2.4)
    tether_old = make_elbow_tether(lambda: p_old.get_bottom() + DOWN * 0.05, dg_to_y(-13.8), color=YELLOW)
    pg_name = T("3-phosphoglycerate", size=24, color=BLUE, weight=BOLD).move_to([BAR_CENTER[0], -0.85, 0])
    new_atp = make_coin("ATP", rim_color=MAGENTA, text_color=TEXT, radius=0.46, font_size=22).move_to(SLOT1_POS)
    slot2 = make_adp_slot(SLOT2_POS)
    nadh = make_nad_pill("NADH", PURPLE).move_to(NADH_CORNER)
    g = VGroup(ledger, ladder, sugar, p_old, tether_old, pg_name, new_atp, slot2, nadh)
    if with_pi:
        pi_pool = make_pi_pool(seed=7)
        pool_lab = T("Pi pool", size=24, color=MAGENTA).move_to([5.25, -3.05, 0])
        g.add(pi_pool, pool_lab)
    g.ladder = ladder
    g.slot2 = slot2
    g.p_old = p_old
    return g


PREDICT_Q = "Old phosphate, no oxidation: how?"
PREDICT_CARD = {"y": 2.15, "left": -1.0, "max_w": 5.8, "size": 28, "color": TEXT}


class S06Predict(SpokenScene):
    def construct(self):
        w = world_after_s06()
        idea_txt = T("Net gain = new phosphate", size=24, color=TEXT, weight=BOLD).move_to([1.05, 2.20, 0])
        self.add(w, idea_txt)

        self.at("old phosphate")
        self.play(FadeOut(idea_txt), run_time=self.beat(0.10))

        self.at("below")
        gap_bar = DoubleArrow([LAD_X1 + 0.35, dg_to_y(-13.8), 0], [LAD_X1 + 0.35, dg_to_y(-30.5), 0],
                              color=RED, stroke_width=3.5, buff=0.05)
        self.play(Create(gap_bar), run_time=self.beat(0.14))

        self.at("no second oxidation")
        pep_bar = w.ladder.rungs["pep"].bar
        self.play(
            FadeOut(gap_bar),
            pep_bar.animate.set_stroke(color=TEXT, opacity=0.85),
            rate_func=there_and_back, run_time=self.beat(0.16),
        )

        self.at("so how can")
        qc = question_card(PREDICT_Q, **PREDICT_CARD)
        self.play(FadeIn(qc, shift=DOWN * 0.1), run_time=self.beat(0.14))
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = PREDICT_Q
    CARD = PREDICT_CARD
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = world_after_s06(with_pi=False)
        pulse(w.slot2.box, base=3.0, amp=1.5, speed=3.0)
        pulse(w.ladder.rungs["pep"].bar, base=3.0, amp=1.8, speed=3.5)
        return w


class S08Rearrange(SpokenScene):
    def construct(self):
        ledger = make_compact_ledger()
        ladder = make_ladder(lit=("bpg", "atp", "est"), faint=("pep",))
        sugar = make_sugar_half(numbered=True)
        attach_carbon_jiggle(sugar.dots)
        p_old = make_phosphate_token(YELLOW).move_to([sugar.dots[2].get_center()[0], BAR_CENTER[1] + 1.00, 0])
        tether_old = make_elbow_tether(lambda: p_old.get_left() + LEFT * 0.05, dg_to_y(-13.8), color=YELLOW, mid_x=-0.95)
        pg_name = T("3-phosphoglycerate", size=24, color=BLUE, weight=BOLD).move_to([BAR_CENTER[0], -0.85, 0])
        new_atp = make_coin("ATP", rim_color=MAGENTA, text_color=TEXT, radius=0.46, font_size=22).move_to(SLOT1_POS)
        slot2 = make_adp_slot(SLOT2_POS)
        nadh = make_nad_pill("NADH", PURPLE).move_to(NADH_CORNER)
        pi_pool = make_pi_pool(seed=7)
        pool_lab = T("Pi pool", size=24, color=MAGENTA).move_to([3.85, -2.42, 0])
        qc = question_card(PREDICT_Q, **PREDICT_CARD)
        self.add(ledger, ladder, sugar, p_old, tether_old, pg_name, new_atp, slot2, nadh, pi_pool, pool_lab, qc)

        self.at("rearrange")
        self.play(FadeOut(qc), run_time=self.beat(0.08))

        self.at("step 8")
        pg2_name = T("2-phosphoglycerate", size=24, color=BLUE, weight=BOLD).move_to(pg_name)
        self.play(
            p_old.animate.move_to([sugar.dots[1].get_center()[0], BAR_CENTER[1] + 1.00, 0]),
            swap(pg_name, pg2_name, run_time=self.beat(0.08)),
            run_time=self.beat(0.12),
        )

        self.at("step 9")
        water_drop = VGroup(
            Circle(radius=0.18, stroke_color=WATER_BLUE, stroke_width=3.0, fill_color=WATER_BLUE, fill_opacity=0.35),
            T("H₂O", size=22, color=TEXT),
        )
        water_drop[1].next_to(water_drop[0], RIGHT, buff=0.10)
        water_drop.move_to([BAR_CENTER[0] + 1.15, BAR_CENTER[1] + 1.00, 0])
        tense_bar = RoundedRectangle(corner_radius=0.08, width=BAR_W, height=BAR_H * 0.90,
                                     stroke_color=BLUE, stroke_width=4.8,
                                     fill_color=BLUE, fill_opacity=0.26).move_to(BAR_CENTER)
        pep_name = T("PEP", size=28, color=BLUE, weight=BOLD).move_to(pg2_name)
        self.play(FadeIn(water_drop, scale=0.7), run_time=self.beat(0.05))
        self.play(
            water_drop.animate.shift(UP * 1.10 + RIGHT * 0.35).set_opacity(0.0),
            Transform(sugar.bar, tense_bar),
            swap(pg2_name, pep_name, run_time=self.beat(0.07)),
            run_time=self.beat(0.11),
        )
        self.remove(water_drop)

        self.at("barely changes")
        g_bg = Arc(radius=0.52, start_angle=PI, angle=-PI, arc_center=[3.45, 1.55, 0], stroke_color=GREY, stroke_width=7.0)
        g_needle = Line([3.45, 1.55, 0], [3.45, 2.00, 0], color=TEXT, stroke_width=4.0)
        g_lab = T("free-energy change: small", size=24, color=TEXT).move_to([2.35, 2.52, 0])
        g_tag = scope_tag("schematic")
        gauge = VGroup(g_bg, g_needle, g_lab)
        self.play(FadeIn(gauge), FadeIn(g_tag), run_time=self.beat(0.06))
        self.play(Rotate(g_needle, angle=-0.16, about_point=[3.45, 1.55, 0]), rate_func=there_and_back, run_time=self.beat(0.09))

        self.at("top of the ladder")
        self.remove(tether_old)
        tether_pep = make_elbow_tether(lambda: p_old.get_top() + UP * 0.05, dg_to_y(-61.9), color=YELLOW, mid_x=-0.95)
        pep_rung = Line([LAD_X0, dg_to_y(-61.9), 0], [LAD_X1, dg_to_y(-61.9), 0], color=YELLOW, stroke_width=6.5)
        pep_rung_lab = T("PEP −61.9", size=24, color=YELLOW, weight=BOLD).next_to(pep_rung, UP, buff=0.10)
        self.add(tether_pep)
        self.play(
            FadeOut(gauge), FadeOut(g_tag),
            Create(pep_rung), FadeIn(pep_rung_lab),
            p_old.ring.animate.set_stroke(width=6.0),
            run_time=self.beat(0.10),
        )
        bob(p_old, amp=0.05, speed=2.8)
        self.finish()


class S09WhyPep(SpokenScene):
    def construct(self):
        ledger = make_compact_ledger()
        ladder = make_ladder(lit=("pep", "bpg", "atp", "est"), faint=())
        sugar = make_sugar_half(numbered=True, tense=True)
        attach_carbon_jiggle(sugar.dots)
        p_pos = np.array([sugar.dots[1].get_center()[0], BAR_CENTER[1] + 1.00, 0])
        p_old = make_phosphate_token(YELLOW).move_to(p_pos)
        tether_pep = make_elbow_tether(lambda: p_old.get_top() + UP * 0.05, dg_to_y(-61.9), color=YELLOW, mid_x=-0.95)
        pep_name = T("PEP", size=28, color=BLUE, weight=BOLD).move_to([BAR_CENTER[0], -0.85, 0])
        new_atp = make_coin("ATP", rim_color=MAGENTA, text_color=TEXT, radius=0.46, font_size=22).move_to(SLOT1_POS)
        slot2 = make_adp_slot(SLOT2_POS)
        nadh = make_nad_pill("NADH", PURPLE).move_to(NADH_CORNER)
        pi_pool = make_pi_pool(seed=7)
        pool_lab = T("Pi pool", size=24, color=MAGENTA).move_to([5.25, -3.05, 0])
        self.add(ledger, ladder, sugar, p_old, tether_pep, pep_name, new_atp, slot2, nadh, pi_pool, pool_lab)

        self.at("what stays behind")
        self.play(sugar.bar.animate.set_stroke(color=TEXT), rate_func=there_and_back, run_time=self.beat(0.08))

        self.at("phosphate leaves")
        ghost_p = p_old.copy().set_opacity(0.45)
        tether_pep.clear_updaters()
        self.play(
            ghost_p.animate.move_to([2.90, 1.95, 0]),
            FadeOut(p_old), FadeOut(tether_pep),
            run_time=self.beat(0.08),
        )

        self.at("unstable form")
        unst_tag = T("unstable form", size=24, color=TEXT, weight=BOLD).move_to([2.90, 1.25, 0])
        self.play(FadeIn(unst_tag), Wiggle(sugar.bar, scale_value=1.08, rotation_angle=0.06), run_time=self.beat(0.11))

        self.at("settles into pyruvate")
        calm_bar = RoundedRectangle(corner_radius=0.45, width=BAR_W, height=BAR_H,
                                    stroke_color=BLUE, stroke_width=3.8,
                                    fill_color=BLUE, fill_opacity=0.22).move_to(BAR_CENTER)
        pyr_name = T("pyruvate", size=26, color=BLUE, weight=BOLD).move_to(pep_name)
        tense_bar = sugar.bar.copy()
        self.play(
            FadeOut(unst_tag),
            Transform(sugar.bar, calm_bar),
            swap(pep_name, pyr_name, run_time=self.beat(0.07)),
            run_time=self.beat(0.11),
        )

        self.at("leaves very readily")
        pep_name2 = T("PEP", size=28, color=BLUE, weight=BOLD).move_to(pyr_name)
        p_old = make_phosphate_token(YELLOW).move_to(p_pos)
        tether_pep = make_elbow_tether(lambda: p_old.get_top() + UP * 0.05, dg_to_y(-61.9), color=YELLOW, mid_x=-0.95)
        tether_pep.clear_updaters()
        self.play(
            FadeOut(ghost_p),
            FadeIn(p_old), FadeIn(tether_pep),
            Transform(sugar.bar, tense_bar),
            swap(pyr_name, pep_name2, run_time=self.beat(0.07)),
            run_time=self.beat(0.10),
        )

        self.at("at step 10")
        arr_10 = make_transfer_arrow([LAD_X1 + 0.08, dg_to_y(-61.9), 0], slot2.get_left() + LEFT * 0.08, via_x=3.85, via_y=dg_to_y(-61.9), color=GREEN)
        self.play(Create(arr_10), run_time=self.beat(0.06))

        self.at("a kinase hands")
        self.remove(tether_pep)
        repaid_atp = make_coin("ATP", rim_color=YELLOW, text_color=TEXT, radius=0.46, font_size=22).move_to(SLOT2_POS)
        paid_tag = T("paid back", size=24, color=YELLOW, weight=BOLD).next_to(repaid_atp, DOWN, buff=0.18)
        pyr_final = T("pyruvate", size=26, color=BLUE, weight=BOLD).move_to(pep_name2)
        self.play(FadeOut(arr_10), run_time=0.20)
        self.play(
            p_old.animate.move_to(slot2.get_left() + LEFT * 0.42),
            Transform(sugar.bar, calm_bar),
            swap(pep_name2, pyr_final, run_time=self.beat(0.07)),
            run_time=self.beat(0.09),
        )
        self.play(
            FadeOut(p_old), FadeOut(slot2),
            FadeIn(repaid_atp), FadeIn(paid_tag),
            run_time=self.beat(0.07),
        )
        self.finish()


def make_full_ledger_shell():
    """Shared top-right full ledger box for S10Ledger and S11Close."""
    l_box = RoundedRectangle(corner_radius=0.16, width=7.55, height=2.36,
                             stroke_color=GREY, stroke_width=2.5,
                             fill_color=BG, fill_opacity=0.92).move_to([2.42, 2.40, 0])
    sp_head = T("spent 2", size=24, color=RED, weight=BOLD).move_to([-0.15, 3.32, 0])
    sp_coins = VGroup(*[make_coin("ATP", RED, TEXT, radius=0.42, font_size=22) for _ in range(2)]).arrange(RIGHT, buff=0.12).move_to([-0.15, 2.66, 0])
    net_head = T("net +2", size=24, color=GREEN, weight=BOLD).move_to([2.85, 3.32, 0])
    nadh_pair = VGroup(*[
        VGroup(
            RoundedRectangle(corner_radius=0.18, width=1.42, height=0.66, stroke_color=PURPLE, stroke_width=3.0, fill_color=PURPLE, fill_opacity=0.24),
            T("NADH", 22, PURPLE, weight=BOLD),
        ) for _ in range(2)
    ])
    for n in nadh_pair:
        n[1].move_to(n[0])
    nadh_pair.arrange(DOWN, buff=0.14).move_to([5.30, 2.40, 0])
    return l_box, sp_head, sp_coins, net_head, nadh_pair


class S10Ledger(SpokenScene):
    def construct(self):
        ladder = make_ladder(lit=("pep", "bpg", "atp", "est"), faint=())
        half1 = make_sugar_half(center=[0.45, -0.05, 0], width=2.45, height=0.80, corner_radius=0.36)
        attach_carbon_jiggle(half1.dots, amp=0.03)
        half2 = make_sugar_half(center=[0.45, -1.25, 0], width=2.45, height=0.80, corner_radius=0.36)
        attach_carbon_jiggle(half2.dots, amp=0.03, speed=2.4)
        halves_lab = T("two halves, same steps", size=24, color=BLUE, weight=BOLD).move_to([0.45, -2.02, 0])

        c_new1 = make_coin("ATP", rim_color=MAGENTA, radius=0.42, font_size=22).move_to([3.30, -0.05, 0])
        c_new2 = make_coin("ATP", rim_color=MAGENTA, radius=0.42, font_size=22).move_to([3.30, -1.25, 0])
        c_rep1 = make_coin("ATP", rim_color=YELLOW, radius=0.42, font_size=22).move_to([4.60, -0.05, 0])
        c_rep2 = make_coin("ATP", rim_color=YELLOW, radius=0.42, font_size=22).move_to([4.60, -1.25, 0])

        l_box, sp_head, sp_coins, net_head, nadh_pair = make_full_ledger_shell()
        pi_pool = make_pi_pool(seed=7, x_range=(3.0, 5.9), y_range=(-3.35, -2.45), n=8)
        count_note = T("counting groups, not atoms", size=24, color=TEXT).move_to([0.35, -3.15, 0])

        self.add(ladder, half1, l_box, sp_head, sp_coins, net_head, pi_pool)

        self.at("count phosphate groups")
        self.play(FadeIn(half2, shift=LEFT * 0.4), FadeIn(halves_lab), run_time=self.beat(0.11))

        self.at("four leave")
        self.play(
            FadeIn(c_new1, shift=RIGHT * 0.25), FadeIn(c_new2, shift=RIGHT * 0.25),
            FadeIn(c_rep1, shift=RIGHT * 0.25), FadeIn(c_rep2, shift=RIGHT * 0.25),
            run_time=self.beat(0.12),
        )

        self.at("only repay")
        repay_tag = T("repay steps 1, 3", size=22, color=YELLOW, weight=BOLD).move_to([-0.15, 0.96, 0])
        self.play(
            c_rep1.animate.move_to([sp_coins[0].get_center()[0], 1.72, 0]),
            c_rep2.animate.move_to([sp_coins[1].get_center()[0], 1.72, 0]),
            FadeIn(repay_tag),
            run_time=self.beat(0.14),
        )
        eq_bar = Line([-0.90, 2.19, 0], [0.60, 2.19, 0], color=RED, stroke_width=3.5)
        self.play(Create(eq_bar), run_time=self.beat(0.05))

        self.at("two are new")
        new_tag = T("new, from step 6", size=22, color=MAGENTA, weight=BOLD).move_to([2.85, 1.56, 0])
        self.play(
            c_new1.animate.move_to([2.36, 2.46, 0]),
            c_new2.animate.move_to([3.34, 2.46, 0]),
            FadeIn(new_tag),
            run_time=self.beat(0.14),
        )

        self.at("oxidation paid")
        self.play(FadeIn(nadh_pair, shift=LEFT * 0.2), FadeIn(count_note), run_time=self.beat(0.12))
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        ladder = make_ladder(lit=("pep", "bpg", "atp", "est"), faint=())
        half1 = make_sugar_half(center=[0.45, -0.05, 0], width=2.45, height=0.80, corner_radius=0.38)
        attach_carbon_jiggle(half1.dots, amp=0.03)
        half2 = make_sugar_half(center=[0.45, -1.25, 0], width=2.45, height=0.80, corner_radius=0.38)
        attach_carbon_jiggle(half2.dots, amp=0.03, speed=2.4)
        pyr_lab = T("2 pyruvate", size=26, color=BLUE, weight=BOLD).move_to([0.45, -2.02, 0])

        l_box, sp_head, sp_coins, net_head, nadh_pair = make_full_ledger_shell()
        c_rep1 = make_coin("ATP", YELLOW, TEXT, radius=0.42, font_size=22).move_to([sp_coins[0].get_center()[0], 1.72, 0])
        c_rep2 = make_coin("ATP", YELLOW, TEXT, radius=0.42, font_size=22).move_to([sp_coins[1].get_center()[0], 1.72, 0])
        eq_bar = Line([-0.90, 2.19, 0], [0.60, 2.19, 0], color=RED, stroke_width=3.5)
        repay_coins = VGroup(sp_coins, c_rep1, c_rep2, eq_bar)

        c_new1 = make_coin("ATP", MAGENTA, TEXT, radius=0.42, font_size=22).move_to([2.36, 2.46, 0])
        c_new2 = make_coin("ATP", MAGENTA, TEXT, radius=0.42, font_size=22).move_to([3.34, 2.46, 0])

        pi_pool = make_pi_pool(seed=7, x_range=(2.2, 5.9), y_range=(-3.35, -2.45), n=10)
        pool_lab = T("Pi pool", size=24, color=MAGENTA).move_to([4.05, -2.15, 0])

        self.add(ladder, half1, half2, pyr_lab, l_box, sp_head, repay_coins,
                 net_head, c_new1, c_new2, nadh_pair, pi_pool, pool_lab)

        self.at("only break even")
        zero_txt = T("0", size=44, color=TEXT, weight=BOLD).move_to([-0.15, 2.20, 0])
        self.play(repay_coins.animate.scale(1.06), rate_func=there_and_back, run_time=self.beat(0.08))
        self.play(swap(repay_coins, zero_txt, run_time=self.beat(0.10)))

        self.at("paid for by")
        trace_pts = [
            c_new1.get_bottom() + DOWN * 0.06,
            [2.36, 1.01, 0],
            [LAD_X1 + 0.12, 1.01, 0],
        ]
        trace = VMobject(stroke_color=MAGENTA, stroke_width=4.5).set_points_as_corners(trace_pts)
        step6_badge = chip("step 6 oxidation", MAGENTA, size=24).move_to([3.85, 0.35, 0])
        self.play(
            Create(trace),
            FadeIn(step6_badge),
            c_new1.ring.animate.set_stroke(width=6.5),
            c_new2.ring.animate.set_stroke(width=6.5),
            run_time=self.beat(0.16),
        )

        self.at("which needs")
        nad_need = chip("needs NAD+", TEAL, size=26).move_to([4.35, -0.95, 0])
        self.play(FadeIn(nad_need, shift=UP * 0.15), run_time=self.beat(0.08))
        self.play(nadh_pair.animate.scale(1.10), rate_func=there_and_back, run_time=self.beat(0.10))
        self.finish()


class S12End(EndCard):
    LINE = "From glucose, net ATP equals the new phosphates an oxidation pays for."
