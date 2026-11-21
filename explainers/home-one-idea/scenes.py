# COLOUR MAP:
#   TEAL   (#3FB8C0): STEMhop interactive cues (Simpler/Deeper, active rung outline, STEMhop host)
#   GOLD   (#D4A843): current rung marker, Hex's bonds/feet, rung level labels, selection arrow
#   BLUE   (#58C4DD): quantitative biology data (moth bars, Gorongosa tuskless fill, breeder's equation chip)
#   GREEN  (#83C167 / lawn #2D5A27 / worm #4FA845): grass lawn and camouflaged green yarn worms
#   BROWN  (#7A5638): camouflaged brown yarn worms
#   RED    (#FC6255): conspicuous red yarn worms
#   YELLOW (#F5D547): conspicuous yellow yarn worms and "chicks?" target
#   TEXT   (#E8EAF0): headings, ladder rails/rungs, labels, axes, beak outlines, bar outlines
#
# SCENE PLAN:
#   s01_ladder:    Heading "Natural selection", empty 4-rung HopLadder with Hex on High school fade in; nothing moves.
#   s02_hunt:      Outline rung 0 + fill title/note; lawn with 4 corner sticks, cup, 20 worms; 10 red+yellow worms move to cup; "green and brown: often left" + "schematic".
#   s03_moths:     Outline moves to rung 1 + fill; cross-fade lawn to 0..15 moth chart + Cambridge/light-trap notes; 2001 bar grows to 12, 2007 bar grows to 1.
#   s04_elephants: Outline moves to rung 2 + fill; cross-fade moth chart to Gorongosa heading + key; before-war bar (18.5%, n=54) grows, survivors bar (50.9%, n=108) grows; "already tuskless" pointer added.
#   s05_finches:   Outline moves to rung 3 + fill; elephant picture fades out; two beak outlines + "schematic" appear, "selection" arrow, "chicks?" arrow, then "R = h² × S" chip + S/R explanations.
#   s06_hop:       Outline fades out; cross-fade finches to stacked compact Gorongosa + moth bars; Hex hops down to Grade 7, then back up to High school.
#   s07_rule:      Ladder holds with Hex on High school; cross-fade compact charts to large title-font rule sentence; everything holds still.
#   s08_end:       Standard EndCard with LINE = "A level is a place to start, not a rank."

from bp_parts import *
from bp_ladder import HopLadder

HEAD_POS = np.array([3.95, 3.05, 0.0])
LAWN_GREEN = "#2D5A27"
LAWN_BORDER = "#427D3B"
WORM_GREEN = "#3C7F35"
WORM_GREEN_EDGE = "#132910"
WORM_BROWN = "#7A5638"
STICK_COL = "#C4A484"
CUP_COL = "#D0D4DE"

RUNGS = [
    {
        "level": "Ages 5 to 10",
        "title": "The Camouflage Hunt",
        "adds": "Be the hungry bird: which yarn worms get eaten last?",
    },
    {
        "level": "Grade 7",
        "title": "Natural Selection in Action",
        "adds": "Hunt moths on clean and sooty bark, then read the real counts.",
    },
    {
        "level": "High school",
        "title": "Variation and Survival",
        "adds": "Poaching in Gorongosa raised tuskless females from 18.5 to 50.9 percent.",
    },
    {
        "level": "College, the core",
        "title": "How to Test an Evolutionary Explanation",
        "adds": "Daphne Major's 1977 drought shows selection; the breeder's equation predicts the offspring shift.",
    },
]


def _nudge_rung2_note(lad):
    """Add tiny vertical clearance (0.015) between rung 2's wrapped lines so descenders/ascenders stay >= 0.05 apart."""
    if len(lad.texts) > 2 and lad.texts[2] is not None:
        title_mob = lad.texts[2][0]
        note_mob = lad.texts[2][1] if len(lad.texts[2]) > 1 else None
        if note_mob is not None and len(note_mob) >= 2:
            note_mob[0].shift(UP * 0.015)
            title_mob.shift(UP * 0.015)
            lad.levels[2].shift(UP * 0.015)


def build_ladder(filled_up_to=-1, here=2):
    """Build HopLadder identically across scenes, filling rungs 0..filled_up_to."""
    specs = []
    for i, r in enumerate(RUNGS):
        if i <= filled_up_to:
            specs.append(dict(r))
        else:
            specs.append({"level": r["level"]})
    lad = HopLadder(specs, here=here)
    _nudge_rung2_note(lad)
    return lad


def build_heading():
    return T("Natural selection", size=40, color=TEXT, font=TITLE_FONT).move_to(HEAD_POS)


def make_scope_tag():
    t = T("schematic", size=22, color=TEXT)
    return t.move_to([6.25 - t.width / 2, -3.38 + t.height / 2, 0])


def animate_fill_and_outline(scene, lad, idx, old_outline=None, step1_anims=(), step2_anims=(), run_time=0.5):
    """Move outline to rung idx and reveal rung idx's title/note without jumping the level label."""
    old_y = lad.levels[idx].get_y()
    filled = lad.fill(idx, RUNGS[idx]["title"], RUNGS[idx]["adds"])
    if idx == 2:
        _nudge_rung2_note(lad)
    new_y = lad.levels[idx].get_y()
    new_outline = lad.outline(idx)
    lad.levels[idx].set_y(old_y)

    step1 = [lad.levels[idx].animate.set_y(new_y)]
    if old_outline is not None:
        step1.append(ReplacementTransform(old_outline, new_outline))
    else:
        step1.append(Create(new_outline))
    step1.extend(step1_anims)
    scene.play(*step1, run_time=run_time * 0.48)
    scene.play(FadeIn(filled), *step2_anims, run_time=run_time * 0.52)
    return new_outline


def cross_fade_right(scene, old_mob, new_mob, run_time=0.45):
    """Fade out old right-column picture then fade in new one with zero text overlap."""
    scene.play(FadeOut(old_mob, run_time=run_time * 0.45))
    scene.play(FadeIn(new_mob, run_time=run_time * 0.55))


# ------------------------------------------------------------------ Picture builders

def _make_worm(center, angle, wavy, fill_col, edge_col=None):
    """Build a short yarn worm (~0.34 long) centered at origin then rotated/moved."""
    pts = []
    n = 7
    for k in range(n):
        t = k / (n - 1) - 0.5
        x = t * 0.34
        y = 0.045 * np.sin(t * TAU * 1.4) if wavy else 0.015 * np.sin(t * PI)
        pts.append([x, y, 0.0])
    g = VGroup()
    if edge_col is not None:
        bg = VMobject(stroke_color=edge_col, stroke_width=10.5, fill_opacity=0)
        bg.set_points_smoothly(pts)
        bg.set_cap_style(CapStyleType.ROUND)
        g.add(bg)
    fg = VMobject(stroke_color=fill_col, stroke_width=6.0, fill_opacity=0)
    fg.set_points_smoothly(pts)
    fg.set_cap_style(CapStyleType.ROUND)
    g.add(fg)
    g.rotate(angle)
    g.move_to(center)
    return g


def build_hunt_picture(eaten=False, show_note=False):
    """Build the lawn, 4 corner sticks, cup, 20 yarn worms, optional eaten state and note."""
    rng = np.random.default_rng(7)
    lawn_center = np.array([3.70, 0.45, 0.0])
    lawn_size = 3.40
    lawn = RoundedRectangle(
        corner_radius=0.16,
        width=lawn_size,
        height=lawn_size,
        fill_color=LAWN_GREEN,
        fill_opacity=1.0,
        stroke_color=LAWN_BORDER,
        stroke_width=3.0,
    ).move_to(lawn_center)

    # 4 corner sticks
    half = lawn_size / 2 - 0.16
    sticks = VGroup()
    stick_centers = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = lawn_center + np.array([sx * half, sy * half, 0.0])
            stick_centers.append(c)
            d = np.array([sx * 0.09, sy * 0.09, 0.0])
            st = Line(c - d, c + d, color=STICK_COL, stroke_width=5.5)
            st.set_cap_style(CapStyleType.ROUND)
            sticks.add(st)

    # Small cup just outside lower-right edge of the lawn
    cup_center = np.array([5.82, -0.92, 0.0])
    cup_body = Polygon(
        cup_center + np.array([-0.34, 0.30, 0.0]),
        cup_center + np.array([0.34, 0.30, 0.0]),
        cup_center + np.array([0.24, -0.34, 0.0]),
        cup_center + np.array([-0.24, -0.34, 0.0]),
        stroke_color=CUP_COL,
        stroke_width=3.0,
        fill_color=BG,
        fill_opacity=0.95,
    )
    cup_rim = Ellipse(
        width=0.68,
        height=0.16,
        stroke_color=CUP_COL,
        stroke_width=2.5,
        fill_color="#1D2230",
        fill_opacity=1.0,
    ).move_to(cup_center + UP * 0.30)
    cup_back = VGroup(cup_body, cup_rim)

    # Generate 20 non-overlapping worm positions on the lawn
    worm_specs = (
        [(WORM_GREEN, WORM_GREEN_EDGE)] * 5
        + [(WORM_BROWN, None)] * 5
        + [(RED, None)] * 5
        + [(YELLOW, None)] * 5
    )
    # Shuffle order deterministically so colors are mixed across the lawn
    order = rng.permutation(len(worm_specs))
    worm_specs = [worm_specs[i] for i in order]

    positions = []
    for _ in range(len(worm_specs)):
        for _attempt in range(600):
            cand = lawn_center + np.array([rng.uniform(-1.32, 1.32), rng.uniform(-1.32, 1.32), 0.0])
            ok_sticks = all(np.linalg.norm(cand - sc) >= 0.48 for sc in stick_centers)
            ok_others = all(np.linalg.norm(cand - p) >= 0.50 for p in positions)
            if ok_sticks and ok_others:
                positions.append(cand)
                break
        else:
            positions.append(lawn_center + np.array([rng.uniform(-1.25, 1.25), rng.uniform(-1.25, 1.25), 0.0]))

    stay_worms = VGroup()
    move_worms = VGroup()
    cup_targets = []
    for idx, ((fcol, ecol), pos) in enumerate(zip(worm_specs, positions)):
        ang = rng.uniform(0, PI)
        wavy = bool(idx % 2 == 0)
        w = _make_worm(pos, ang, wavy, fcol, ecol)
        if fcol in (RED, YELLOW):
            target = cup_center + np.array([rng.uniform(-0.14, 0.14), rng.uniform(-0.14, 0.14), 0.0])
            t_ang = rng.uniform(0, PI)
            if eaten:
                w.rotate(t_ang - ang)
                w.move_to(target)
            move_worms.add(w)
            cup_targets.append((target, t_ang - ang))
        else:
            stay_worms.add(w)

    tag = make_scope_tag()
    all_parts = VGroup(lawn, sticks, cup_back, stay_worms, move_worms, tag)
    note = None
    if show_note:
        note = T("green and brown: often left", size=24, color=TEXT).move_to([3.70, -1.78, 0.0])
        all_parts.add(note)

    return all_parts, move_worms, cup_targets, note


def build_moth_chart(show_2001=False, show_2007=False):
    """Build the Grade 7 moth bar chart and Cambridge notes."""
    P = Plot(
        box=(2.40, 5.75, -0.75, 1.45),
        xr=(0, 3),
        yr=(0, 15),
        xticks=(),
        yticks=[(0, "0"), (5, "5"), (10, "10"), (15, "15")],
        color=TEXT,
        size=22,
        stroke=2.5,
    )
    y_title = T("dark moths,\npercent of moths caught", size=24, color=TEXT, line_spacing=0.9)
    y_title.next_to([2.40, 1.45, 0.0], UP, buff=0.28)
    y_title.align_to([1.80, 0.0, 0.0], LEFT)

    n1 = T("Madingley, near Cambridge,\nEngland; light-trap samples", size=22, color=TEXT, line_spacing=0.9)
    n3 = T("values read from a graph,\nso rounded", size=22, color=TEXT, line_spacing=0.9)
    notes = VGroup(n1, n3).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    notes.move_to([1.60, -1.68, 0.0], aligned_edge=UL)

    def _bar_group(x_center, val, year_str, top_str):
        y0 = P.pt(0, 0)[1]
        y_top = P.pt(0, val)[1]
        h = max(0.04, y_top - y0)
        bar = Rectangle(
            width=0.82,
            height=h,
            fill_color=BLUE,
            fill_opacity=0.88,
            stroke_color=BLUE,
            stroke_width=2.0,
        ).move_to([x_center, y0 + h / 2, 0.0])
        yr_lbl = T(year_str, size=24, color=TEXT).next_to([x_center, y0, 0.0], DOWN, buff=0.16)
        top_lbl = T(top_str, size=24, color=TEXT).next_to(bar, UP, buff=0.14)
        return bar, yr_lbl, top_lbl

    b1, y1, t1 = _bar_group(3.35, 12, "2001", "about 12%")
    b2, y2, t2 = _bar_group(4.90, 1, "2007", "about 1%")

    base = VGroup(P, y_title, notes)
    if show_2001:
        base.add(b1, y1, t1)
    if show_2007:
        base.add(b2, y2, t2)
    return base, (b1, y1, t1), (b2, y2, t2)


def build_elephant_picture(show_war=False, show_surv=False, show_pointer=False):
    """Build the High school Gorongosa tuskless horizontal bar comparison."""
    head = fit_text("Gorongosa: sampled female elephants", max_w=4.4, size=24, color=TEXT, min_size=24)
    head.move_to([3.95, 2.08, 0.0])

    bar_w = 4.50
    bar_h = 0.54
    x_left = 1.70
    x_right = x_left + bar_w

    def _hbar(y_c, title_str, n_str, pct, pct_str):
        outline = Rectangle(
            width=bar_w,
            height=bar_h,
            stroke_color=TEXT,
            stroke_width=2.5,
            fill_opacity=0.0,
        ).move_to([x_left + bar_w / 2, y_c, 0.0])
        fw = bar_w * (pct / 100.0)
        fill = Rectangle(
            width=fw,
            height=bar_h - 0.04,
            fill_color=BLUE,
            fill_opacity=0.88,
            stroke_width=0.0,
        ).move_to([x_left + fw / 2, y_c, 0.0])
        lbl_l = T(title_str, size=24, color=TEXT).move_to([x_left, y_c + bar_h / 2 + 0.16, 0.0], aligned_edge=DL)
        lbl_n = T(n_str, size=22, color=TEXT).move_to([x_right, y_c + bar_h / 2 + 0.16, 0.0], aligned_edge=DR)
        pct_lbl = T(pct_str, size=24, color=TEXT).move_to([x_left + fw + 0.14, y_c, 0.0], aligned_edge=LEFT)
        return outline, fill, lbl_l, lbl_n, pct_lbl

    war = _hbar(0.85, "before the war", "n = 54 females", 18.5, "18.5%")
    surv = _hbar(-1.05, "survivors", "n = 108 females", 50.9, "50.9%")

    key_sq = Square(side_length=0.26, fill_color=BLUE, fill_opacity=0.88, stroke_width=0.0)
    key_txt = T("no tusks", size=24, color=TEXT)
    key = VGroup(key_sq, key_txt).arrange(RIGHT, buff=0.14)
    key.move_to([x_left, -2.05, 0.0], aligned_edge=LEFT)

    # Tag "already tuskless" pointing up to the filled portion of the upper bar
    war_fill = war[1]
    tag_lbl = T("already tuskless", size=22, color=TEXT).move_to([2.68, -0.05, 0.0])
    target_pt = np.array([war_fill.get_center()[0], war[0].get_bottom()[1] - 0.04, 0.0])
    start_pt = np.array([war_fill.get_center()[0], tag_lbl.get_top()[1] + 0.06, 0.0])
    ptr = Arrow(start_pt, target_pt, buff=0.0, stroke_width=2.5, tip_length=0.16, color=TEXT)
    pointer_grp = VGroup(tag_lbl, ptr)

    group = VGroup(head)
    if show_war:
        group.add(*war, key)
    if show_surv:
        group.add(*surv)
    if show_pointer:
        group.add(pointer_grp)
    return group, war, surv, key, pointer_grp


def _beak_outline(x_left, y_center, length, depth):
    """Simple closed side-view wedge beak pointing right with slightly curved upper edge."""
    p_top = np.array([x_left, y_center + depth / 2, 0.0])
    p_bot = np.array([x_left, y_center - depth / 2, 0.0])
    p_tip = np.array([x_left + length, y_center - depth * 0.08, 0.0])

    # Build smooth curved upper edge from p_top to p_tip, then straight edges to p_bot and p_top
    ts = np.linspace(0.0, 1.0, 14)
    ctrl = np.array([x_left + length * 0.58, y_center + depth * 0.42, 0.0])
    upper_pts = [((1 - t) ** 2) * p_top + 2 * (1 - t) * t * ctrl + (t ** 2) * p_tip for t in ts]
    all_pts = upper_pts + [p_bot, p_top]

    m = VMobject(stroke_color=TEXT, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.12)
    m.set_points_as_corners(all_pts)
    m.close_path()
    return m


def build_finches_picture(show_beaks=False, show_selection=False, show_chicks=False, show_eq=False):
    """Build College level Daphne Major beak schematic + breeder's equation."""
    beak_len = 1.24
    d1 = 0.66
    d2 = d1 * 1.35

    b1 = _beak_outline(1.72, 1.55, beak_len, d1)
    b2 = _beak_outline(4.78, 1.55, beak_len, d2)

    lbl1 = T("before the\ndrought", size=24, color=TEXT, line_spacing=0.88).next_to(b1, DOWN, buff=0.18)
    lbl2 = T("survivors", size=24, color=TEXT).next_to(b2, DOWN, buff=0.18)
    lbl2.set_y(lbl1.get_top()[1] - lbl2.height / 2)

    sel_arrow = Arrow(
        [b1.get_right()[0] + 0.14, 1.55, 0.0],
        [b2.get_left()[0] - 0.14, 1.55, 0.0],
        buff=0.0,
        stroke_width=3.0,
        tip_length=0.18,
        color=GOLD,
    )
    sel_lbl = T("selection", size=24, color=GOLD).next_to(sel_arrow, UP, buff=0.14)

    chicks_lbl = T("chicks?", size=24, color=YELLOW).move_to([b2.get_center()[0], -0.25, 0.0])
    chicks_arrow = Arrow(
        [b2.get_center()[0], lbl2.get_bottom()[1] - 0.08, 0.0],
        [b2.get_center()[0], chicks_lbl.get_top()[1] + 0.08, 0.0],
        buff=0.0,
        stroke_width=3.0,
        tip_length=0.16,
        color=YELLOW,
    )

    eq_txt = M("R = h² × S", size=26, color=BLUE)
    eq_box = RoundedRectangle(
        corner_radius=0.14,
        width=eq_txt.width + 0.44,
        height=eq_txt.height + 0.36,
        stroke_color=BLUE,
        stroke_width=2.5,
        fill_color=BLUE,
        fill_opacity=0.16,
    )
    eq_chip = VGroup(eq_box, eq_txt.move_to(eq_box)).move_to([3.95, -0.95, 0.0])

    s_line = fit_text(
        "S: how far the parents' average sits from the population's",
        max_w=4.45,
        size=22,
        color=TEXT,
        min_size=22,
        max_lines=2,
    )
    r_line = fit_text(
        "R: how far the chicks' average moves",
        max_w=4.45,
        size=22,
        color=TEXT,
        min_size=22,
        max_lines=2,
    )
    sr_group = VGroup(s_line, r_line).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    sr_group.move_to([1.72, -1.48, 0.0], aligned_edge=UL)

    tag = make_scope_tag()

    beak1_grp = VGroup(b1, lbl1, tag)
    beak2_grp = VGroup(b2, lbl2)
    sel_grp = VGroup(sel_arrow, sel_lbl)
    chicks_grp = VGroup(chicks_arrow, chicks_lbl)
    eq_grp = VGroup(eq_chip, sr_group)

    full = VGroup()
    if show_beaks:
        full.add(beak1_grp, beak2_grp)
    if show_selection:
        full.add(sel_grp)
    if show_chicks:
        full.add(chicks_grp)
    if show_eq:
        full.add(eq_grp)
    return full, beak1_grp, beak2_grp, sel_grp, chicks_grp, eq_grp


def build_compact_pair():
    """Stacked Gorongosa bars (top) and moth bars (bottom) for s06_hop."""
    bar_w = 3.85
    bar_h = 0.38
    x_left = 2.02

    def _compact_hbar(y_c, label_str, pct, pct_str):
        outline = Rectangle(
            width=bar_w,
            height=bar_h,
            stroke_color=TEXT,
            stroke_width=2.2,
            fill_opacity=0.0,
        ).move_to([x_left + bar_w / 2, y_c, 0.0])
        fw = bar_w * (pct / 100.0)
        fill = Rectangle(
            width=fw,
            height=bar_h - 0.04,
            fill_color=BLUE,
            fill_opacity=0.88,
            stroke_width=0.0,
        ).move_to([x_left + fw / 2, y_c, 0.0])
        lbl = T(label_str, size=22, color=TEXT).move_to([x_left, y_c + bar_h / 2 + 0.10, 0.0], aligned_edge=DL)
        plbl = T(pct_str, size=22, color=TEXT).move_to([x_left + fw + 0.12, y_c, 0.0], aligned_edge=LEFT)
        return VGroup(outline, fill, lbl, plbl)

    g_top = _compact_hbar(1.88, "before the war", 18.5, "18.5%")
    g_bot = _compact_hbar(0.95, "survivors", 50.9, "50.9%")

    P = Plot(
        box=(2.45, 5.65, -2.55, -0.55),
        xr=(0, 3),
        yr=(0, 15),
        xticks=(),
        yticks=[(0, "0"), (5, "5"), (10, "10"), (15, "15")],
        color=TEXT,
        size=22,
        stroke=2.2,
    )

    def _mbar(xc, val, yr_s, top_s):
        y0 = P.pt(0, 0)[1]
        yt = P.pt(0, val)[1]
        h = max(0.04, yt - y0)
        b = Rectangle(
            width=0.76,
            height=h,
            fill_color=BLUE,
            fill_opacity=0.88,
            stroke_color=BLUE,
            stroke_width=2.0,
        ).move_to([xc, y0 + h / 2, 0.0])
        yl = T(yr_s, size=22, color=TEXT).next_to([xc, y0, 0.0], DOWN, buff=0.14)
        tl = T(top_s, size=22, color=TEXT).next_to(b, UP, buff=0.12)
        return VGroup(b, yl, tl)

    m1 = _mbar(3.40, 12, "2001", "about 12%")
    m2 = _mbar(4.90, 1, "2007", "about 1%")

    return VGroup(g_top, g_bot, P, m1, m2)


def build_rule_sentence():
    t = T(
        "A level is\na place to start,\nnot a rank.",
        size=40,
        color=TEXT,
        font=TITLE_FONT,
        line_spacing=1.05,
    )
    fit(t, max_w=4.4)
    return t.move_to([3.95, 0.0, 0.0])


# ------------------------------------------------------------------ Scenes

class S01Ladder(SpokenScene):
    def construct(self):
        lad = build_ladder(filled_up_to=-1, here=2)
        head = build_heading()
        self.play(FadeIn(lad), FadeIn(head), run_time=0.5)
        self.finish()


class S02Hunt(SpokenScene):
    def construct(self):
        lad = build_ladder(filled_up_to=-1, here=2)
        head = build_heading()
        self.add(lad, head)

        hunt_pic, move_worms, cup_targets, _ = build_hunt_picture(eaten=False, show_note=False)
        old_y = lad.levels[0].get_y()
        filled0 = lad.fill(0, RUNGS[0]["title"], RUNGS[0]["adds"])
        new_y = lad.levels[0].get_y()
        outline0 = lad.outline(0)
        lad.levels[0].set_y(old_y)

        self.play(
            lad.levels[0].animate.set_y(new_y),
            Create(outline0),
            FadeIn(hunt_pic),
            run_time=0.45,
        )
        self.play(FadeIn(filled0), run_time=0.25)

        self.at("hunts yarn worms")
        anims = []
        for w, (tgt, d_ang) in zip(move_worms, cup_targets):
            anims.append(w.animate(path_arc=-0.4).rotate(d_ang).move_to(tgt))
        self.play(LaggedStart(*anims, lag_ratio=0.22, run_time=2.45))

        self.at("green and brown")
        note = T("green and brown: often left", size=24, color=TEXT).move_to([3.70, -1.78, 0.0])
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


class S03Moths(SpokenScene):
    def construct(self):
        lad = build_ladder(filled_up_to=0, here=2)
        head = build_heading()
        outline = lad.outline(0)
        old_pic, _, _, _ = build_hunt_picture(eaten=True, show_note=True)
        self.add(lad, head, outline, old_pic)

        moth_base, (b1, y1, t1), (b2, y2, t2) = build_moth_chart(show_2001=False, show_2007=False)
        outline = animate_fill_and_outline(
            self,
            lad,
            1,
            old_outline=outline,
            step1_anims=(FadeOut(old_pic),),
            step2_anims=(FadeIn(moth_base),),
            run_time=0.55,
        )

        self.at("were about")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(y1), run_time=0.4)
        self.play(FadeIn(t1), run_time=0.25)

        self.at("and about")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(y2), run_time=0.35)
        self.play(FadeIn(t2), run_time=0.25)
        self.finish()


class S04Elephants(SpokenScene):
    def construct(self):
        lad = build_ladder(filled_up_to=1, here=2)
        head = build_heading()
        outline = lad.outline(1)
        old_pic, _, _ = build_moth_chart(show_2001=True, show_2007=True)
        self.add(lad, head, outline, old_pic)

        ele_base, war, surv, key, ptr = build_elephant_picture(
            show_war=False, show_surv=False, show_pointer=False
        )
        outline = animate_fill_and_outline(
            self,
            lad,
            2,
            old_outline=outline,
            step1_anims=(FadeOut(old_pic),),
            step2_anims=(FadeIn(ele_base),),
            run_time=0.55,
        )

        self.at("before the war")
        w_out, w_fill, w_lbl, w_n, w_pct = war
        self.play(FadeIn(w_out), FadeIn(w_lbl), FadeIn(w_n), FadeIn(key), run_time=0.35)
        self.play(GrowFromEdge(w_fill, LEFT), FadeIn(w_pct), run_time=0.8)

        self.at("among survivors")
        s_out, s_fill, s_lbl, s_n, s_pct = surv
        self.play(FadeIn(s_out), FadeIn(s_lbl), FadeIn(s_n), run_time=0.35)
        self.play(GrowFromEdge(s_fill, LEFT), FadeIn(s_pct), run_time=0.8)

        self.at("no elephant had")
        self.play(FadeIn(ptr), run_time=0.4)
        self.finish()


class S05Finches(SpokenScene):
    def construct(self):
        lad = build_ladder(filled_up_to=2, here=2)
        head = build_heading()
        outline = lad.outline(2)
        old_pic, _, _, _, _ = build_elephant_picture(
            show_war=True, show_surv=True, show_pointer=True
        )
        self.add(lad, head, outline, old_pic)

        _, beak1_grp, beak2_grp, sel_grp, chicks_grp, eq_grp = build_finches_picture()
        outline = animate_fill_and_outline(
            self,
            lad,
            3,
            old_outline=outline,
            step1_anims=(FadeOut(old_pic),),
            step2_anims=(FadeIn(beak1_grp),),
            run_time=0.55,
        )

        self.at("survivors of the")
        self.play(FadeIn(beak2_grp), run_time=0.45)

        self.at("that is selection")
        self.play(FadeIn(sel_grp), run_time=0.4)

        self.at("not yet evolution")
        self.play(FadeIn(chicks_grp), run_time=0.4)

        self.at("a breeder's equation")
        self.play(FadeIn(eq_grp), run_time=0.45)
        self.finish()


class S06Hop(SpokenScene):
    def construct(self):
        lad = build_ladder(filled_up_to=3, here=2)
        head = build_heading()
        outline = lad.outline(3)
        old_pic, _, _, _, _, _ = build_finches_picture(
            show_beaks=True, show_selection=True, show_chicks=True, show_eq=True
        )
        self.add(lad, head, outline, old_pic)

        compact = build_compact_pair()
        self.play(FadeOut(outline), FadeOut(old_pic), run_time=0.25)
        self.play(FadeIn(compact), run_time=0.3)

        self.at("hop down")
        lad.hop(self, 1, run_time=0.6)

        self.at("then back up")
        lad.hop(self, 2, run_time=0.6)
        self.finish()


class S07Rule(SpokenScene):
    def construct(self):
        lad = build_ladder(filled_up_to=3, here=2)
        head = build_heading()
        old_pic = build_compact_pair()
        self.add(lad, head, old_pic)

        rule = build_rule_sentence()
        cross_fade_right(self, old_pic, rule, run_time=0.45)
        self.finish()


class S08End(EndCard):
    LINE = "A level is a place to start, not a rank."
