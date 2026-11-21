"""Timing, Context, and Jammed Relays (ras-to-mapk__chapter-2)

COLOUR MAP (one colour per concept for the whole film):
    COL_EGF      = "#F5C542"   # Gold: Receptor, EGF ligand, ATP/GTP, phosphate badges (P)
    COL_NGF      = "#F58A2E"   # Amber: NGF ligand and sustained differentiation readout
    COL_SOS      = "#3FB8C0"   # Teal: SOS exchange factor
    COL_RAS      = "#FF7B59"   # Coral: Ras GTPase switch
    COL_RAF      = "#38D399"   # Emerald: Raf kinase (normal and B-Raf V600E)
    COL_MEK      = "#4CC9F0"   # Electric blue: MEK kinase (and always-on MEK)
    COL_ERK      = "#B882FF"   # Vivid violet: ERK kinase and ERK activity readout
    COL_INHIB    = "#F43F6E"   # Crimson: Negative feedback, phosphatases, GAP/neurofibromin, drugs (Vemurafenib, Trametinib)
    COL_MEMBRANE = "#5A6B8C"   # Slate blue: Cell membrane, cytoplasm compartment, fibroblasts
    COL_NUCLEUS  = "#7B88FF"   # Indigo: Nucleus and nuclear genes
    COL_FOCI     = "#F472B6"   # Rose: Mouse fibroblasts / transformed foci
    TEXT         = "#E8EAF0"   # Crisp off-white: Primary labels, axes, outlines
    AXIS_COL     = "#C4CBD6"   # Bright silver: Plot axes, ticks, and scope tags (never dim grey)

THE ONE WORLD CARRIED THROUGH THE FILM:
    A dark-navy cell cross-section (gold receptor at top membrane -> SOS -> coral Ras -> emerald Raf ->
    electric-blue MEK -> vivid violet ERK -> indigo nucleus at bottom) paired with a schematic ERK
    activity trace / gauge on the right. Scenes zoom into the relevant tier or cell-outcome comparison
    while preserving exact protein identities and colours.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s01_hook:              Signal pulse propagates tier-by-tier along the connecting arrows down the cell
                           cross-section while lighting each tier; on the right, top PC12 cell elongates and
                           splits parametrically into two daughter cells under EGF, while bottom PC12 cell
                           grows computed branching neurite trees under NGF.
    s02_feedback_duration: Active ERK drives a fast solid crimson feedback arc back to SOS and Raf (weakening
                           their border glow) and a slow dashed arc into the nucleus; transcription spawns
                           filled crimson dual-specificity phosphatase crescents that drift up to strip
                           both Thr-P and Tyr-P badges off ERK while the schematic ERK trace (Plot) drops.
    s03_pc12_clock:        A time tracker t (0 -> 3.7 h) drives two computed ERK curves on Plot: a gamma-like
                           EGF pulse ((t/0.25)**1.5 * exp(1.5*(1 - t/0.25))) peaking and fading within 1 h,
                           and an exponential-plateau NGF curve (0.88 * (1 - exp(-t/0.25))) holding high for
                           hours, synchronized with receptor persistence bars on the left.
    s04_cell_context:      An identical Always-on MEK block is placed into two resting cells without growth
                           factor; left PC12 cell grows branching neurites while right fibroblast monolayer
                           divides and stacks upward into a seeded-RNG (seed=7) disordered mound (Foci).
    s05_cancer_jams:       Left panel shows normal Ras GTP -> GDP off-timer sped by GAPs, then swaps to
                           Ras G12V, crosses out the GTP hydrolysis cut, and jams the off-timer dial to
                           drive Raf pairs, MEK, and ERK; right panel shows inactive Ras-GDP beside
                           glowing B-Raf V600E ('Partner needed? debated') pulsing MEK and ERK.
    s06_predict_q:         Left panel slides crimson Vemurafenib wedge into B-Raf V600E's ATP notch and dims
                           MEK and ERK; right panel shows Active Ras holding a pair of normal Raf blocks as
                           the wedge enters one Raf's ATP notch, raising the question banner and ERK '?'.
    s07_predict_pause:     PredictPause holds the final frame of s06_predict_q while a 4.5 s countdown ring
                           sweeps smoothly in the bottom-right corner.
    s08_drug_reveal:       Schematic ERK gauge needle and fill shoot upward as Active Ras pulls normal Raf
                           into a side-to-side pair and drug-bound Raf transfers activation by contact (not
                           catalysis) to its drug-free partner; then crimson Trametinib locks into MEK's
                           allosteric side pocket beside ATP and the ERK gauge drops.
    s09_rasopathies_close: Schematic body outline highlights pulsing face, heart, and growth zones; beside it,
                           losing neurofibromin (a Ras GAP off-timer) stalls the dial and leaves Ras-GTP
                           active too long; then the view transitions into three summary cards (Duration,
                           Context, Pathway state).
"""

import numpy as np
from bp_parts import *

# ------------------------------------------------------------------ Colour map
COL_EGF = "#F5C542"
COL_NGF = "#F58A2E"
COL_SOS = "#3FB8C0"
COL_RAS = "#FF7B59"
COL_RAF = "#38D399"
COL_MEK = "#4CC9F0"
COL_ERK = "#B882FF"
COL_INHIB = "#F43F6E"
COL_MEMBRANE = "#5A6B8C"
COL_NUCLEUS = "#7B88FF"
COL_FOCI = "#F472B6"
AXIS_COL = "#C4CBD6"
CYTO_FILL = "#242D3F"


# ------------------------------------------------------------------ Shared geometry helpers
def _arrow_between(src, dst, color=TEXT, stroke_width=3.5, tip_len=0.14, gap=0.07):
    """Straight arrow starting outside src and ending outside dst so it never straddles a box."""
    p0 = src.get_bottom() + DOWN * gap
    p1 = dst.get_top() + UP * gap
    if np.linalg.norm(p1 - p0) < 0.10:
        p0 = src.get_center()
        p1 = dst.get_center()
    return Arrow(p0, p1, buff=0, color=color, stroke_width=stroke_width,
                 max_tip_length_to_length_ratio=0.45, tip_length=tip_len)


def build_cell_stage(x_center=-3.4, width=5.4, include_sos=False, y_top=2.22, y_bot=-3.05, node_offset=0.0):
    """Build the carried cell cross-section: membrane, receptor, cascade tiers, nucleus + genes."""
    half_w = width / 2.0
    nx = x_center + node_offset
    mem_top = Line([x_center - half_w, y_top + 0.09, 0], [x_center + half_w, y_top + 0.09, 0],
                   color=COL_MEMBRANE, stroke_width=4)
    mem_bot = Line([x_center - half_w, y_top - 0.09, 0], [x_center + half_w, y_top - 0.09, 0],
                   color=COL_MEMBRANE, stroke_width=4)
    mem_fill = Polygon(
        [x_center - half_w, y_top + 0.09, 0],
        [x_center + half_w, y_top + 0.09, 0],
        [x_center + half_w, y_top - 0.09, 0],
        [x_center - half_w, y_top - 0.09, 0],
        stroke_width=0, fill_color=COL_MEMBRANE, fill_opacity=0.45,
    )
    cyto = Polygon(
        [x_center - half_w + 0.04, y_top - 0.09, 0],
        [x_center + half_w - 0.04, y_top - 0.09, 0],
        [x_center + half_w - 0.04, y_bot, 0],
        [x_center - half_w + 0.04, y_bot, 0],
        stroke_width=0, fill_color=CYTO_FILL, fill_opacity=0.85,
    )
    mem_tag = T("membrane", 22, AXIS_COL).move_to([x_center + half_w - 0.85, y_top + 0.34, 0])

    rec_x = nx - 0.55 if include_sos else nx
    rec_stem = RoundedRectangle(corner_radius=0.08, width=0.54, height=0.72,
                                stroke_color=COL_EGF, stroke_width=3,
                                fill_color=COL_EGF, fill_opacity=0.30).move_to([rec_x, y_top, 0])
    rec_arm_l = Line([rec_x - 0.14, y_top + 0.36, 0], [rec_x - 0.36, y_top + 0.62, 0],
                     color=COL_EGF, stroke_width=4)
    rec_arm_r = Line([rec_x + 0.14, y_top + 0.36, 0], [rec_x + 0.36, y_top + 0.62, 0],
                     color=COL_EGF, stroke_width=4)
    rec_lbl = T("Receptor", 24, COL_EGF).move_to([rec_x, y_top + 0.90, 0])
    receptor = VGroup(rec_stem, rec_arm_l, rec_arm_r, rec_lbl)

    if include_sos:
        ys = {"SOS": 1.48, "Ras": 0.74, "Raf": 0.00, "MEK": -0.74, "ERK": -1.48}
        sz, pad = 24, 0.14
    else:
        ys = {"Ras": 1.32, "Raf": 0.44, "MEK": -0.44, "ERK": -1.32}
        sz, pad = 26, 0.16

    nodes = {}
    if include_sos:
        nodes["SOS"] = boxed_label("SOS", COL_SOS, size=sz, box=(1.60, 0.46), pad=pad, fill_opacity=0.20).move_to([nx, ys["SOS"], 0])
    nodes["Ras"] = boxed_label("Ras", COL_RAS, size=sz, box=(1.60, 0.46), pad=pad, fill_opacity=0.20).move_to([nx, ys["Ras"], 0])
    nodes["Raf"] = boxed_label("Raf", COL_RAF, size=sz, box=(1.60, 0.46), pad=pad, fill_opacity=0.20).move_to([nx, ys["Raf"], 0])
    nodes["MEK"] = boxed_label("MEK", COL_MEK, size=sz, box=(1.60, 0.46), pad=pad, fill_opacity=0.20).move_to([nx, ys["MEK"], 0])
    nodes["ERK"] = boxed_label("ERK", COL_ERK, size=sz, box=(1.60, 0.46), pad=pad, fill_opacity=0.20).move_to([nx, ys["ERK"], 0])

    nuc_pts = []
    for a in np.linspace(0, PI, 32):
        nuc_pts.append([x_center + (half_w - 0.30) * np.cos(a), y_bot + 1.12 * np.sin(a), 0])
    nuc_poly = Polygon(*nuc_pts, stroke_color=COL_NUCLEUS, stroke_width=3,
                       fill_color=COL_NUCLEUS, fill_opacity=0.26)
    genes_lbl = T("Genes", 24, TEXT).move_to([x_center, y_bot + 0.56, 0])
    genes_bar = Line([x_center - 1.15, y_bot + 0.22, 0], [x_center + 1.15, y_bot + 0.22, 0],
                     color=COL_NUCLEUS, stroke_width=6)
    nucleus = VGroup(nuc_poly, genes_bar, genes_lbl)

    arrows = []
    order = (["SOS", "Ras", "Raf", "MEK", "ERK"] if include_sos else ["Ras", "Raf", "MEK", "ERK"])
    p_rec = rec_stem.get_bottom() + DOWN * 0.05
    p_top = nodes[order[0]].get_top() + UP * 0.05
    arrows.append(Arrow(p_rec, p_top, buff=0, color=AXIS_COL, stroke_width=3, tip_length=0.12))
    for a, b in zip(order[:-1], order[1:]):
        arrows.append(_arrow_between(nodes[a], nodes[b], color=AXIS_COL, stroke_width=3, tip_len=0.12, gap=0.05))
    p_erk = nodes["ERK"].get_bottom() + DOWN * 0.05
    p_nuc = np.array([nx, y_bot + 1.13, 0])
    arrows.append(Arrow(p_erk, p_nuc, buff=0, color=COL_ERK, stroke_width=3.5, tip_length=0.13))

    parts = {
        "cyto": cyto,
        "membrane": VGroup(mem_fill, mem_top, mem_bot, mem_tag),
        "receptor": receptor,
        "rec_stem": rec_stem,
        "nodes": nodes,
        "arrows": VGroup(*arrows),
        "nucleus": nucleus,
        "nuc_poly": nuc_poly,
        "genes_bar": genes_bar,
        "genes_lbl": genes_lbl,
        "x_center": x_center,
        "y_top": y_top,
        "y_bot": y_bot,
    }
    parts["group"] = VGroup(cyto, parts["membrane"], receptor, *nodes.values(), parts["arrows"], nucleus)
    return parts


def make_pocket_kinase(label_text, color, pocket_side="left", width=2.3, height=1.05,
                       pocket_depth=0.42, pocket_h=0.44, font_size=24):
    """Build a kinase block with an ATP notch cut into its left or right edge."""
    hw, hh = width / 2.0, height / 2.0
    ph = pocket_h / 2.0
    if pocket_side == "left":
        pts = [
            [-hw, hh, 0], [hw, hh, 0], [hw, -hh, 0], [-hw, -hh, 0],
            [-hw, -ph, 0], [-hw + pocket_depth, -ph, 0],
            [-hw + pocket_depth, ph, 0], [-hw, ph, 0],
        ]
        lbl_x = pocket_depth * 0.42
        p_center = np.array([-hw + pocket_depth * 0.5, 0.0, 0.0])
    else:
        pts = [
            [-hw, hh, 0], [hw, hh, 0],
            [hw, ph, 0], [hw - pocket_depth, ph, 0],
            [hw - pocket_depth, -ph, 0], [hw, -ph, 0],
            [hw, -hh, 0], [-hw, -hh, 0],
        ]
        lbl_x = -pocket_depth * 0.42
        p_center = np.array([hw - pocket_depth * 0.5, 0.0, 0.0])
    body = Polygon(*pts, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    lbl = T(label_text, font_size, color).move_to([lbl_x, 0, 0])
    g = VGroup(body, lbl)
    g.body = body
    g.label = lbl
    g._pocket_offset = p_center
    return g


def make_wedge(color=COL_INHIB, width=0.44, height=0.40):
    """A drug wedge sized to plug cleanly into a kinase ATP pocket."""
    hw, hh = width / 2.0, height / 2.0
    return Polygon(
        [-hw, hh, 0], [hw, hh * 0.72, 0], [hw, -hh * 0.72, 0], [-hw, -hh, 0],
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.92,
    )


def make_erk_gauge(tracker, center, radius=1.25, label="Schematic ERK"):
    """Qualitative half-circle ERK gauge (low -> high) driven by a ValueTracker in [0, 1]."""
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=AXIS_COL, stroke_width=10)
    v = lambda: float(np.clip(tracker.get_value(), 0.01, 1.0))
    fill_arc = always_redraw(
        lambda: Arc(radius=radius, start_angle=PI, angle=-PI * v(), arc_center=c,
                    stroke_color=COL_ERK, stroke_width=10)
    )
    needle = always_redraw(
        lambda: Line(c, c + 0.80 * radius * np.array([np.cos(PI - PI * v()), np.sin(PI - PI * v()), 0]),
                     color=TEXT, stroke_width=5)
    )
    pivot = Dot(c, radius=0.08, color=TEXT)
    low_t = T("low", 22, AXIS_COL).move_to(c + LEFT * (radius + 0.36) + DOWN * 0.14)
    high_t = T("high", 22, AXIS_COL).move_to(c + RIGHT * (radius + 0.38) + DOWN * 0.14)
    lbl_t = T(label, 26, COL_ERK).move_to(c + DOWN * 0.65)
    return VGroup(track, fill_arc, needle, pivot, low_t, high_t, lbl_t)


def build_neurite_tree(origin, direction=RIGHT, seed=7, scale=1.0,
                       angles=(-0.45, -0.10, 0.25, 0.55), step_len=0.36):
    """Compute a deterministic branching neurite tree as a VGroup of VMobjects."""
    rng = np.random.default_rng(seed)
    base_dir = direction / np.linalg.norm(direction)
    branches = VGroup()
    for a in angles:
        d0 = np.array([base_dir[0] * np.cos(a) - base_dir[1] * np.sin(a),
                       base_dir[0] * np.sin(a) + base_dir[1] * np.cos(a), 0.0])
        pts = [np.array(origin, dtype=float)]
        cur = pts[0].copy()
        ang = np.arctan2(d0[1], d0[0])
        for _ in range(4):
            ang += rng.uniform(-0.16, 0.16)
            cur = cur + step_len * scale * np.array([np.cos(ang), np.sin(ang), 0.0])
            pts.append(cur.copy())
        main = VMobject(stroke_color=COL_NGF, stroke_width=3.8 * scale)
        main.set_points_as_corners(pts)
        branches.add(main)
        for idx, twig_a in ((2, 0.32), (3, -0.30)):
            t_ang = ang + twig_a + rng.uniform(-0.08, 0.08)
            p_start = pts[idx]
            p_mid = p_start + 0.22 * scale * np.array([np.cos(t_ang), np.sin(t_ang), 0.0])
            p_end = p_mid + 0.20 * scale * np.array([np.cos(t_ang + 0.14), np.sin(t_ang + 0.14), 0.0])
            tw = VMobject(stroke_color=COL_NGF, stroke_width=2.6 * scale)
            tw.set_points_as_corners([p_start, p_mid, p_end])
            branches.add(tw)
    return branches


def build_pc12_cell(center, radius=0.62, color=TEXT):
    """Simple schematic rounded PC12 cell with inner nucleus dot."""
    body = Circle(radius=radius, stroke_color=color, stroke_width=3.5,
                  fill_color=COL_MEMBRANE, fill_opacity=0.38).move_to(center)
    nuc = Circle(radius=radius * 0.34, stroke_color=COL_NUCLEUS, stroke_width=2.5,
                 fill_color=COL_NUCLEUS, fill_opacity=0.45).move_to(center)
    return VGroup(body, nuc)


def _segment_pulse(segments, phase_tracker, color=COL_EGF, radius=0.07):
    """Return an always_redraw Dot inset strictly inside arrow gaps so it never straddles box borders."""
    segs = []
    for a, b in segments:
        pa, pb = np.array(a, dtype=float), np.array(b, dtype=float)
        d = pb - pa
        dist = np.linalg.norm(d)
        if dist > 0.32:
            u = d / dist
            segs.append((pa + u * 0.13, pb - u * 0.13))
        else:
            mid = (pa + pb) / 2.0
            segs.append((mid, mid))
    n = len(segs)

    def mk():
        u = (phase_tracker.get_value() % 1.0) * n
        idx = min(n - 1, int(u))
        f = u - idx
        p = segs[idx][0] + f * (segs[idx][1] - segs[idx][0])
        return Dot(p, radius=radius, color=color)

    return always_redraw(mk)


def _tier_glow(boxes, phase_tracker, base_width=2.5, amp=2.8):
    """Return an updater tying cascade box stroke widths to the travelling phase (active tier wave)."""
    n = len(boxes)

    def u(mob, dt=0):
        ph = (phase_tracker.get_value() % 1.0) * n
        for i, bx in enumerate(boxes):
            d = min(abs(ph - i), abs(ph - i - n), abs(ph - i + n))
            w = base_width + amp * max(0.0, 1.0 - d * 1.4)
            bx.box.set_stroke(width=w)

    return u


def _panel_bg(panel_frame):
    """Subtle cytoplasm tint inside a TwoPanel frame (Polygon so layout_check never flags outside)."""
    c = panel_frame.get_center()
    hw = panel_frame.width / 2.0 - 0.08
    hh = panel_frame.height / 2.0 - 0.08
    return Polygon(
        [c[0] - hw, c[1] + hh, 0],
        [c[0] + hw, c[1] + hh, 0],
        [c[0] + hw, c[1] - hh, 0],
        [c[0] - hw, c[1] - hh, 0],
        stroke_width=0, fill_color=CYTO_FILL, fill_opacity=0.75,
    ).set_z_index(-2)


def _predict_world():
    """Shared backdrop for s06_predict_q end state and s07_predict_pause."""
    tp = TwoPanel("B-Raf V600E + Vemurafenib", "Active Ras + normal B-Raf",
                  colors=(COL_RAF, COL_RAS), top=2.75, bottom=-2.45, gap=0.45, width=12.6, size=28)
    bg_l, bg_r = _panel_bg(tp.left_frame), _panel_bg(tp.right_frame)

    lc = tp.area("left")[0]
    braf_v = make_pocket_kinase("B-Raf V600E", COL_RAF, pocket_side="left", width=2.55, height=0.85,
                                pocket_depth=0.38, pocket_h=0.40, font_size=24).move_to([lc[0] + 0.72, 0.85, 0])
    vem_l = make_wedge(COL_INHIB, width=0.34, height=0.36).move_to(braf_v.body.get_center() + braf_v._pocket_offset)
    vem_l_lbl = T("Vemurafenib", 22, COL_INHIB).next_to(vem_l, LEFT, buff=0.18)
    mek_l = boxed_label("MEK", COL_MEK, size=24, box=(1.6, 0.50), fill_opacity=0.14).move_to([lc[0], -0.45, 0])
    erk_l = boxed_label("ERK (off)", COL_ERK, size=24, box=(1.8, 0.50), fill_opacity=0.14).move_to([lc[0], -1.65, 0])
    arr_l1 = Arrow(braf_v.get_bottom() + DOWN * 0.06, mek_l.get_top() + UP * 0.06, buff=0, color=COL_INHIB, stroke_width=3, tip_length=0.13)
    cross_l = VGroup(
        Line([-0.14, -0.14, 0], [0.14, 0.14, 0], color=COL_INHIB, stroke_width=4),
        Line([-0.14, 0.14, 0], [0.14, -0.14, 0], color=COL_INHIB, stroke_width=4),
    ).move_to(arr_l1.get_center())
    arr_l2 = Arrow(mek_l.get_bottom() + DOWN * 0.06, erk_l.get_top() + UP * 0.06, buff=0, color=COL_MEMBRANE, stroke_width=2.5, tip_length=0.12)
    left_g = VGroup(braf_v, vem_l, vem_l_lbl, mek_l, erk_l, arr_l1, cross_l, arr_l2)

    rc = tp.area("right")[0]
    ras_r = boxed_label("Active Ras", COL_RAS, size=24, box=(2.2, 0.46), fill_opacity=0.22).move_to([rc[0] + 0.58, 1.35, 0])
    raf_l = make_pocket_kinase("Raf", COL_RAF, pocket_side="left", width=1.42, height=0.80,
                               pocket_depth=0.32, pocket_h=0.36, font_size=24).move_to([rc[0] - 0.15, 0.30, 0])
    raf_r = make_pocket_kinase("Raf", COL_RAF, pocket_side="right", width=1.42, height=0.80,
                               pocket_depth=0.32, pocket_h=0.36, font_size=24).move_to([rc[0] + 1.36, 0.30, 0])
    vem_r = make_wedge(COL_INHIB, width=0.30, height=0.32).move_to(raf_l.body.get_center() + raf_l._pocket_offset)
    vem_r_lbl = T("Vemurafenib", 22, COL_INHIB).next_to(vem_r, LEFT, buff=0.18)
    tether_l = Line(ras_r.get_bottom() + LEFT * 0.40 + DOWN * 0.04, raf_l.get_top() + UP * 0.04, color=COL_RAS, stroke_width=3)
    tether_r = Line(ras_r.get_bottom() + RIGHT * 0.40 + DOWN * 0.04, raf_r.get_top() + UP * 0.04, color=COL_RAS, stroke_width=3)
    mek_r = boxed_label("MEK", COL_MEK, size=24, box=(1.55, 0.46), fill_opacity=0.22).move_to([rc[0] - 1.15, -0.95, 0])
    arr_rm = Arrow(raf_r.get_bottom() + DOWN * 0.06, mek_r.get_top() + UP * 0.06, buff=0, color=COL_RAF, stroke_width=3, tip_length=0.13)

    g_center = np.array([rc[0] + 1.35, -1.42, 0.0])
    g_rad = 0.85
    g_track = Arc(radius=g_rad, start_angle=PI, angle=-PI, arc_center=g_center, stroke_color=AXIS_COL, stroke_width=8)
    g_q = T("?", 38, COL_ERK, weight=BOLD).move_to(g_center + UP * 0.30)
    g_lbl = T("ERK ?", 24, COL_ERK).move_to(g_center + DOWN * 0.36)
    gauge_q = VGroup(g_track, g_q, g_lbl)
    arr_mg = Arrow(mek_r.get_right() + RIGHT * 0.06, [g_center[0] - g_rad - 0.12, mek_r.get_center()[1], 0],
                   buff=0, color=COL_MEK, stroke_width=3, tip_length=0.12)

    right_g = VGroup(ras_r, raf_l, raf_r, vem_r, vem_r_lbl, tether_l, tether_r, mek_r, arr_rm, gauge_q, arr_mg)
    tag = scope_tag("schematic", color=AXIS_COL).move_to([4.15, -3.12, 0])
    return VGroup(bg_l, bg_r, tp, left_g, right_g, tag)


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Ras to MAPK: The Kinase Cascade"
    TITLE = "Timing, Context, and Jammed Relays"


class S01Hook(SpokenScene):
    def construct(self):
        cell = build_cell_stage(x_center=-3.4, width=5.3, include_sos=False)
        nodes = cell["nodes"]
        gap_segs = [
            (cell["rec_stem"].get_bottom() + DOWN * 0.04, nodes["Ras"].get_top() + UP * 0.04),
            (nodes["Ras"].get_bottom() + DOWN * 0.04, nodes["Raf"].get_top() + UP * 0.04),
            (nodes["Raf"].get_bottom() + DOWN * 0.04, nodes["MEK"].get_top() + UP * 0.04),
            (nodes["MEK"].get_bottom() + DOWN * 0.04, nodes["ERK"].get_top() + UP * 0.04),
            (nodes["ERK"].get_bottom() + DOWN * 0.04, np.array([cell["x_center"], cell["y_bot"] + 1.15, 0])),
        ]
        pkt = Dot(gap_segs[0][0], radius=0.09, color=COL_EGF)

        self.at("the first film")
        self.play(FadeIn(cell["group"]), FadeIn(pkt), run_time=0.9)

        self.at("ross")
        self.play(MoveAlongPath(pkt, Line(*gap_segs[0])), nodes["Ras"].box.animate.set_stroke(width=5), run_time=0.7)
        pkt.set_color(COL_RAS)

        self.at("raff")
        self.play(MoveAlongPath(pkt, Line(*gap_segs[1])), nodes["Raf"].box.animate.set_stroke(width=5), run_time=0.5)
        pkt.set_color(COL_RAF)

        self.at("mech")
        self.play(MoveAlongPath(pkt, Line(*gap_segs[2])), nodes["MEK"].box.animate.set_stroke(width=5), run_time=0.5)
        pkt.set_color(COL_MEK)

        self.at("irk")
        self.play(MoveAlongPath(pkt, Line(*gap_segs[3])), nodes["ERK"].box.animate.set_stroke(width=5), run_time=0.7)
        pkt.set_color(COL_ERK)

        self.at("membrane signal to genes")
        self.play(MoveAlongPath(pkt, Line(*gap_segs[4])), cell["genes_bar"].animate.set_stroke(COL_ERK, width=10), run_time=1.8)
        self.play(FadeOut(pkt), run_time=0.4)

        pc12_hdr = T("PC12 cells", 30, TEXT, weight=BOLD).move_to([3.2, 3.10, 0])
        div_line = Line([0.2, 0.0, 0], [6.1, 0.0, 0], color=COL_MEMBRANE, stroke_width=2.5).set_opacity(0.80)

        top_c = np.array([2.5, 1.48, 0.0])
        top_cell = build_pc12_cell(top_c, radius=0.64, color=TEXT)
        q_fork = VGroup(
            Arrow(nodes["ERK"].get_right() + RIGHT * 0.12, [0.85, 1.48, 0], buff=0, color=COL_ERK, stroke_width=3.5, tip_length=0.14),
            Arrow(nodes["ERK"].get_right() + RIGHT * 0.12, [0.85, -1.55, 0], buff=0, color=COL_ERK, stroke_width=3.5, tip_length=0.14),
        )
        bot_c = np.array([2.2, -1.58, 0.0])
        bot_cell = build_pc12_cell(bot_c, radius=0.64, color=TEXT)

        self.at("how can that same relay")
        self.play(FadeIn(div_line), Create(q_fork), run_time=1.2)

        self.at("one cell to divide")
        div_tag = T("Divide?", 26, COL_EGF).move_to([4.85, 1.48, 0])
        self.play(FadeIn(top_cell), FadeIn(div_tag), run_time=1.4)

        self.at("another to stop dividing")
        stop_tag = T("Stop dividing?", 26, COL_NGF).move_to([4.85, -1.58, 0])
        self.play(FadeIn(bot_cell), FadeIn(stop_tag), run_time=1.8)

        self.at("in pc 12 cells")
        self.play(FadeIn(pc12_hdr), run_time=1.3)

        self.at("egf drives division")
        egf_chip = boxed_label("EGF", COL_EGF, size=24, box=(1.05, 0.44), fill_opacity=0.22).move_to([1.25, 2.55, 0])
        egf_arr = Arrow(egf_chip.get_bottom() + DOWN * 0.08, top_cell.get_top() + LEFT * 0.25 + UP * 0.08,
                        buff=0, color=COL_EGF, stroke_width=3, tip_length=0.12)
        self.play(FadeIn(egf_chip), Create(egf_arr), FadeOut(div_tag), run_time=0.45)

        split_t = ValueTracker(0.0)
        def _dividing():
            s = split_t.get_value()
            dx = 0.72 * s
            r = 0.64 * (1.0 - 0.22 * s)
            c1 = build_pc12_cell(top_c + LEFT * dx + RIGHT * 0.5, radius=r, color=COL_EGF if s > 0.7 else TEXT)
            c2 = build_pc12_cell(top_c + RIGHT * dx + RIGHT * 0.5, radius=r, color=COL_EGF if s > 0.7 else TEXT)
            return VGroup(c1, c2)

        live_div = always_redraw(_dividing)
        self.remove(top_cell)
        self.add(live_div)
        div_lbl = T("Divide", 26, COL_EGF, weight=BOLD).move_to([5.25, 1.48, 0])
        self.play(split_t.animate.set_value(1.0), FadeIn(div_lbl), run_time=1.35)

        self.at("while ngf grows")
        ngf_chip = boxed_label("NGF", COL_NGF, size=24, box=(1.05, 0.44), fill_opacity=0.22).move_to([1.25, -0.58, 0])
        ngf_arr = Arrow(ngf_chip.get_bottom() + DOWN * 0.08, bot_cell.get_top() + LEFT * 0.20 + UP * 0.08,
                        buff=0, color=COL_NGF, stroke_width=3, tip_length=0.12)
        neurites = build_neurite_tree(bot_cell.get_right() + LEFT * 0.04, direction=RIGHT, seed=7, scale=1.20)
        neu_lbl = T("Neurites", 26, COL_NGF, weight=BOLD).move_to([4.9, -2.75, 0])
        self.play(FadeIn(ngf_chip), Create(ngf_arr), FadeOut(stop_tag), run_time=0.45)
        self.play(Create(neurites, lag_ratio=0.15), FadeIn(neu_lbl), run_time=2.3)
        self.finish()


class S02FeedbackDuration(SpokenScene):
    def construct(self):
        cell = build_cell_stage(x_center=-3.45, width=5.6, include_sos=True, node_offset=0.55)
        nodes = cell["nodes"]
        erk_box = nodes["ERK"]
        sos_box = nodes["SOS"]
        raf_box = nodes["Raf"]

        p1 = boxed_label("Thr-P", COL_EGF, size=22, box=(1.08, 0.42), pad=0.07, fill_opacity=0.22).next_to(erk_box, LEFT, buff=0.12).shift(UP * 0.30)
        p2 = boxed_label("Tyr-P", COL_EGF, size=22, box=(1.08, 0.42), pad=0.07, fill_opacity=0.22).next_to(erk_box, LEFT, buff=0.12).shift(DOWN * 0.18)
        p_badges = VGroup(p1, p2)

        P = Plot(box=(1.35, 6.05, -1.65, 2.05), xr=(0, 3.0), yr=(0, 1.15),
                 xticks=[(0, "0"), (1, "1"), (2, "2"), (3, "3 h")],
                 yticks=[(0, "0"), (1, "high")],
                 xlabel="time", ylabel="ERK activity (schematic)", color=AXIS_COL, size=22, label_size=24)
        t_val = ValueTracker(0.06)

        def erk_fn(t):
            if t < 0.55:
                return 0.96 * (t / 0.55) ** 0.8
            if t < 1.35:
                return 0.96 - 0.30 * (t - 0.55) / 0.80  # fast feedback weakens upstream (0.96 -> 0.66)
            return max(0.06, 0.66 * np.exp(-((t - 1.35) / 0.60) ** 2))  # slow phosphatases strip ERK down

        live_c = P.live_curve(erk_fn, t_val, color=COL_ERK, width=7)
        live_d = P.dot(lambda: t_val.get_value(), lambda: erk_fn(t_val.get_value()), color=TEXT, ring=COL_ERK, radius=0.13)
        self.add(cell["group"], P, scope_tag("schematic", color=AXIS_COL))

        self.at("duration")
        self.add(live_c, live_d)
        dur_arr = DoubleArrow(P.pt(0.75, 0.26), P.pt(2.30, 0.26), buff=0, color=COL_ERK, stroke_width=3.5, tip_length=0.14)
        dur_lbl = T("duration", 24, COL_ERK).next_to(dur_arr, DOWN, buff=0.10)
        str_arr = DoubleArrow(P.pt(0.55, 0.04), P.pt(0.55, 0.96), buff=0, color=COL_EGF, stroke_width=3.5, tip_length=0.14)
        str_lbl = T("strength", 24, COL_EGF).next_to(str_arr, RIGHT, buff=0.12).shift(UP * 0.24)
        self.play(t_val.animate.set_value(0.56), FadeIn(p_badges), run_time=0.7)
        self.play(Create(dur_arr), FadeIn(dur_lbl), run_time=0.5)

        self.at("strength")
        self.play(Create(str_arr), FadeIn(str_lbl), run_time=0.7)

        self.at("erk helps set")
        clk_lbl = T("ERK sets its clock", 26, COL_ERK, weight=BOLD).move_to([3.4, 3.12, 0])
        self.play(
            FadeIn(clk_lbl), FadeOut(dur_arr), FadeOut(dur_lbl), FadeOut(str_arr), FadeOut(str_lbl),
            t_val.animate.set_value(0.85), run_time=2.2,
        )

        self.at("active erk sends fast")
        fb_arc_raf = CurvedArrow(
            erk_box.get_right() + RIGHT * 0.06,
            raf_box.get_right() + RIGHT * 0.06,
            angle=1.10, color=COL_INHIB, stroke_width=5, tip_length=0.16,
        )
        fb_arc_sos = CurvedArrow(
            erk_box.get_right() + RIGHT * 0.06 + UP * 0.06,
            sos_box.get_right() + RIGHT * 0.06,
            angle=0.92, color=COL_INHIB, stroke_width=5, tip_length=0.16,
        )
        fast_lbl = T("Fast\nfeedback", 22, COL_INHIB, weight=BOLD, line_spacing=0.80).next_to(cell["cyto"], RIGHT, buff=0.12).set_y(0.55)
        self.play(Create(fb_arc_raf), Create(fb_arc_sos), FadeIn(fast_lbl), t_val.animate.set_value(1.10), run_time=3.0)

        self.at("phosphorylating sos")
        p_sos = boxed_label("P", COL_INHIB, size=22, box=(0.44, 0.44), pad=0.06, fill_opacity=0.24).next_to(sos_box, LEFT, buff=0.12)
        self.play(FadeIn(p_sos), sos_box.box.animate.set_stroke(COL_MEMBRANE, width=2), t_val.animate.set_value(1.24), run_time=1.3)

        self.at("and raf to weaken them")
        p_raf = boxed_label("P", COL_INHIB, size=22, box=(0.44, 0.44), pad=0.06, fill_opacity=0.24).next_to(raf_box, LEFT, buff=0.12).shift(UP * 0.28)
        self.play(FadeIn(p_raf), raf_box.box.animate.set_stroke(COL_MEMBRANE, width=2), t_val.animate.set_value(1.38), run_time=1.8)

        self.at("erk also induces")
        slow_arc = DashedVMobject(
            CurvedArrow(erk_box.get_left() + LEFT * 0.05 + DOWN * 0.40,
                        cell["genes_bar"].get_left() + LEFT * 0.05 + UP * 0.08,
                        angle=0.80, color=COL_INHIB, stroke_width=5, tip_length=0.15),
            num_dashes=10,
        )
        self.play(Create(slow_arc), cell["genes_bar"].animate.set_stroke(COL_INHIB, width=10),
                  cell["nuc_poly"].animate.set_fill(COL_INHIB, opacity=0.22),
                  t_val.animate.set_value(1.65), run_time=1.1)

        self.at("phosphatases")
        def _crescent(pos):
            return AnnularSector(inner_radius=0.10, outer_radius=0.22, angle=PI * 1.25, start_angle=-0.2,
                                 arc_center=pos, color=COL_INHIB, fill_opacity=0.90)

        phos = VGroup(_crescent([-5.70, -2.32, 0]), _crescent([-5.15, -2.52, 0]))
        phos_lbl = T("Dual-specificity\nphosphatase\n(slow: new protein)", 22, COL_INHIB, line_spacing=0.65).move_to([-5.14, -0.36, 0])
        self.play(FadeIn(phos), FadeIn(phos_lbl), t_val.animate.set_value(1.95), run_time=1.2)

        self.at("strip both")
        self.play(
            phos[0].animate.move_to(p1.get_left() + LEFT * 0.28),
            phos[1].animate.move_to(p2.get_left() + LEFT * 0.28),
            t_val.animate.set_value(2.35),
            run_time=1.0,
        )
        self.play(
            FadeOut(p1), FadeOut(p2),
            erk_box.box.animate.set_stroke(COL_MEMBRANE, width=2),
            t_val.animate.set_value(2.55),
            run_time=0.6,
        )

        self.at("they act slowly")
        self.play(
            Indicate(phos_lbl, color=COL_INHIB, scale_factor=1.06),
            Indicate(cell["genes_bar"], color=COL_INHIB, scale_factor=1.05),
            t_val.animate.set_value(2.85),
            run_time=2.2,
        )
        self.finish()


class S03Pc12Clock(SpokenScene):
    def construct(self):
        hdr_l = T("Receptor + feedback", 28, TEXT, weight=BOLD).move_to([-4.15, 2.95, 0])
        egf_rec = boxed_label("EGF receptor: brief", COL_EGF, size=24, box=(3.3, 0.55), fill_opacity=0.22).move_to([-4.15, 1.55, 0])
        egf_bar_bg = RoundedRectangle(corner_radius=0.08, width=3.2, height=0.38, stroke_color=COL_EGF, stroke_width=2.5).move_to([-4.15, 0.90, 0])
        ngf_rec = boxed_label("NGF receptor: persists", COL_NGF, size=24, box=(3.3, 0.55), fill_opacity=0.22).move_to([-4.15, -0.20, 0])
        ngf_bar_bg = RoundedRectangle(corner_radius=0.08, width=3.2, height=0.38, stroke_color=COL_NGF, stroke_width=2.5).move_to([-4.15, -0.85, 0])

        egf_lvl = ValueTracker(0.95)
        ngf_lvl = ValueTracker(0.95)
        egf_fill = always_redraw(lambda: Rectangle(
            width=max(0.06, 3.12 * egf_lvl.get_value()), height=0.30, stroke_width=0,
            fill_color=COL_EGF, fill_opacity=0.88,
        ).align_to(egf_bar_bg.get_left() + RIGHT * 0.04, LEFT).move_to([0, egf_bar_bg.get_center()[1], 0], coor_mask=np.array([0, 1, 0])))
        ngf_fill = always_redraw(lambda: Rectangle(
            width=max(0.06, 3.12 * ngf_lvl.get_value()), height=0.30, stroke_width=0,
            fill_color=COL_NGF, fill_opacity=0.88,
        ).align_to(ngf_bar_bg.get_left() + RIGHT * 0.04, LEFT).move_to([0, ngf_bar_bg.get_center()[1], 0], coor_mask=np.array([0, 1, 0])))

        fb_badge = boxed_label("Fast + slow feedback", COL_INHIB, size=24, box=(3.3, 0.52), fill_opacity=0.22).move_to([-4.15, -1.90, 0])

        plot_title = T("Schematic ERK activity (PC12 cells)", 30, TEXT, weight=BOLD).move_to([2.25, 2.95, 0])
        P = Plot(box=(-1.35, 6.0, -1.65, 2.15), xr=(0, 4), yr=(0, 1.15),
                 xticks=[(0, "0"), (1, "1 h"), (2, "2 h"), (3, "3 h"), (4, "4 h")],
                 yticks=[(0, "0"), (1, "high")],
                 xlabel="time (hours)", ylabel="", color=AXIS_COL, size=22, label_size=24)

        egf_fn = lambda t: 0.0 if t <= 0 else (t / 0.25) ** 1.5 * np.exp(1.5 * (1.0 - t / 0.25))
        ngf_fn = lambda t: 0.0 if t <= 0 else 0.88 * (1.0 - np.exp(-t / 0.28))

        t_egf = ValueTracker(0.10)
        t_ngf = ValueTracker(0.10)
        egf_curve = P.live_curve(egf_fn, t_egf, color=COL_EGF, width=6, x0=0.0)
        egf_dot = P.dot(lambda: t_egf.get_value(), lambda: egf_fn(t_egf.get_value()), color=TEXT, ring=COL_EGF)
        ngf_curve = P.live_curve(ngf_fn, t_ngf, color=COL_NGF, width=6, x0=0.0)
        ngf_dot = P.dot(lambda: t_ngf.get_value(), lambda: max(0.06, ngf_fn(t_ngf.get_value())), color=TEXT, ring=COL_NGF)

        self.at("how long the receptor")
        self.play(FadeIn(hdr_l), FadeIn(egf_rec), FadeIn(egf_bar_bg), FadeIn(ngf_rec), FadeIn(ngf_bar_bg),
                  FadeIn(egf_fill), FadeIn(ngf_fill), Create(P), FadeIn(plot_title), run_time=2.2)

        self.at("plus this feedback")
        self.play(FadeIn(fb_badge), run_time=2.5)

        self.at("pc 12 cells")
        self.play(Indicate(plot_title, color=COL_ERK, scale_factor=1.05), run_time=1.3)

        self.at("egf sparks a brief")
        self.add(egf_curve, egf_dot)
        egf_lbl = T("EGF", 26, COL_EGF, weight=BOLD).move_to(P.pt(0.75, 0.92))
        div_badge = boxed_label("Divide", COL_EGF, size=24, box=(1.45, 0.46), fill_opacity=0.22).move_to(P.pt(1.55, 0.40))
        self.play(FadeIn(egf_lbl), run_time=0.2)
        self.play(t_egf.animate.set_value(3.65), egf_lvl.animate.set_value(0.06), run_time=3.4, rate_func=linear)

        self.at("ngf holds erk high")
        self.add(ngf_curve, ngf_dot)
        ngf_lbl = T("NGF", 26, COL_NGF, weight=BOLD).move_to(P.pt(2.3, 1.03))
        neu_badge = boxed_label("Neurites", COL_NGF, size=24, box=(1.65, 0.46), fill_opacity=0.22).move_to(P.pt(3.10, 0.65))
        self.play(FadeIn(ngf_lbl), run_time=0.2)
        self.play(t_ngf.animate.set_value(2.10), ngf_lvl.animate.set_value(0.90), run_time=2.6, rate_func=linear)

        self.at("brief erk goes with division")
        self.play(FadeIn(div_badge), t_ngf.animate.set_value(2.75), run_time=1.4)

        self.at("and sustained erk")
        self.play(FadeIn(neu_badge), t_ngf.animate.set_value(3.65), run_time=2.8, rate_func=linear)

        self.at("how widely other cells")
        caveat = caption("One cell line; generality open", size=26, color=COL_EGF, y=-3.05)
        self.play(FadeIn(caveat), FadeIn(scope_tag("schematic", color=AXIS_COL)), run_time=1.8)
        self.finish()


class S04CellContext(SpokenScene):
    def construct(self):
        tp = TwoPanel("PC12 cell", "Mouse fibroblasts", colors=(COL_NGF, COL_FOCI),
                      top=2.65, bottom=-2.45, gap=0.45, width=12.6, size=30)
        bg_l, bg_r = _panel_bg(tp.left_frame), _panel_bg(tp.right_frame)
        lc = tp.area("left")[0]
        rc = tp.area("right")[0]

        no_gf_l = T("No growth factor", 22, AXIS_COL).move_to([lc[0], 1.68, 0])
        pc12 = build_pc12_cell([lc[0] - 1.55, -1.14, 0], radius=0.52, color=TEXT)
        pc12_lbl = T("PC12", 24, TEXT).next_to(pc12, DOWN, buff=0.14)

        no_gf_r = T("No growth factor", 22, AXIS_COL).move_to([rc[0], 1.68, 0])
        dish_line = Line([rc[0] - 2.6, -1.92, 0], [rc[0] + 2.6, -1.92, 0], color=AXIS_COL, stroke_width=3)
        flat_cells = VGroup(*[
            RoundedRectangle(corner_radius=0.12, width=1.15, height=0.28,
                             stroke_color=COL_MEMBRANE, stroke_width=2.5,
                             fill_color=COL_MEMBRANE, fill_opacity=0.45).move_to([rc[0] - 1.9 + i * 1.25, -1.75, 0])
            for i in range(4)
        ])

        self.at("cell context matters")
        self.play(FadeIn(bg_l), FadeIn(bg_r), FadeIn(tp), FadeIn(pc12), FadeIn(pc12_lbl),
                  FadeIn(dish_line), FadeIn(flat_cells), run_time=2.6)

        self.at("researchers placed the same")
        mek_master = boxed_label("Always-on MEK", COL_MEK, size=24, box=(2.55, 0.48), fill_opacity=0.22).move_to([0, 3.22, 0])
        self.play(FadeIn(mek_master), FadeIn(no_gf_l), FadeIn(no_gf_r), run_time=2.0)

        mek_l = boxed_label("Always-on MEK", COL_MEK, size=24, box=(2.55, 0.46), fill_opacity=0.22).move_to([lc[0], 1.00, 0])
        mek_r = boxed_label("Always-on MEK", COL_MEK, size=24, box=(2.55, 0.46), fill_opacity=0.22).move_to([rc[0], 1.00, 0])
        erk_l = boxed_label("Sustained ERK", COL_ERK, size=24, box=(2.45, 0.46), fill_opacity=0.22).move_to([lc[0], 0.16, 0])
        erk_r = boxed_label("Sustained ERK", COL_ERK, size=24, box=(2.45, 0.46), fill_opacity=0.22).move_to([rc[0], 0.16, 0])
        arr_l = _arrow_between(mek_l, erk_l, color=COL_MEK, stroke_width=3.5, tip_len=0.12, gap=0.05)
        arr_r = _arrow_between(mek_r, erk_r, color=COL_MEK, stroke_width=3.5, tip_len=0.12, gap=0.05)

        self.at("into two cell types")
        self.play(FadeOut(mek_master, shift=DOWN * 0.15), FadeIn(mek_l), FadeIn(mek_r), run_time=0.8)
        self.play(Create(arr_l), Create(arr_r), FadeIn(erk_l), FadeIn(erk_r), run_time=2.2)

        self.at("pc 12 cells grew neurites")
        neurites = build_neurite_tree(pc12.get_right() + LEFT * 0.04, direction=RIGHT, seed=11, scale=1.22,
                                      angles=(-0.20, -0.04, 0.10, 0.22), step_len=0.35)
        neu_lbl = T("Neurites", 26, COL_NGF, weight=BOLD).move_to([lc[0] + 1.15, -2.14, 0])
        self.play(Create(neurites, lag_ratio=0.15), run_time=1.8)
        self.play(FadeIn(neu_lbl), run_time=0.35)

        self.at("no growth factor")
        self.play(Indicate(no_gf_l, color=COL_EGF, scale_factor=1.1), run_time=1.8)

        self.at("mouse fibroblasts instead piled")
        rng = np.random.default_rng(7)
        foci_cells = VGroup()
        for layer, count in ((1, 5), (2, 4), (3, 3), (4, 2)):
            for k in range(count):
                x_off = (k - (count - 1) / 2.0) * 0.62 + rng.uniform(-0.14, 0.14)
                y_pos = -1.75 + layer * 0.24 + rng.uniform(-0.04, 0.05)
                ang = rng.uniform(-0.35, 0.35)
                c = RoundedRectangle(
                    corner_radius=0.10, width=0.78, height=0.26,
                    stroke_color=COL_FOCI, stroke_width=2.2,
                    fill_color=COL_FOCI, fill_opacity=0.50,
                ).rotate(ang).move_to([rc[0] + x_off, y_pos, 0])
                foci_cells.add(c)

        self.play(FadeIn(foci_cells, lag_ratio=0.14), run_time=1.8)

        self.at("into disordered foci")
        foci_lbl = T("Foci (transformation)", 26, COL_FOCI, weight=BOLD).move_to([rc[0], -2.95, 0])
        self.play(FadeIn(foci_lbl), run_time=1.8)
        self.finish()


class S05CancerJams(SpokenScene):
    def construct(self):
        tp = TwoPanel("Normal Ras (off-timer)", "B-Raf V600E (melanoma)",
                      colors=(COL_RAS, COL_RAF), top=2.95, bottom=-2.65, gap=0.45, width=12.6, size=28)
        tp.remove(tp.left_head, tp.right_head)
        w_panel = (12.6 - 0.45) / 2
        left_head_jammed = fit_text("Ras G12V (jammed on)", max_w=w_panel - 0.5, size=28, color=COL_RAS).move_to(tp.left_head.get_center())
        bg_l, bg_r = _panel_bg(tp.left_frame), _panel_bg(tp.right_frame)
        lc = tp.area("left")[0]
        rc = tp.area("right")[0]

        mem_l = Line([lc[0] - 2.55, 1.92, 0], [lc[0] + 2.55, 1.92, 0], color=COL_MEMBRANE, stroke_width=4)
        ras_norm = boxed_label("Ras", COL_RAS, size=24, box=(1.15, 0.48), pad=0.16, fill_opacity=0.22).move_to([lc[0] - 1.95, 1.38, 0])
        ras_l = boxed_label("Ras G12V", COL_RAS, size=24, box=(1.88, 0.48), pad=0.16, fill_opacity=0.22).move_to([lc[0] - 1.90, 1.38, 0])
        gtp_l = boxed_label("GTP", COL_EGF, size=22, box=(0.82, 0.42), pad=0.12, fill_opacity=0.22).move_to([lc[0] - 0.28, 1.38, 0])
        cut_arr = Arrow([lc[0] + 0.18, 1.38, 0], [lc[0] + 0.90, 1.38, 0], buff=0, color=COL_EGF, stroke_width=3.5, tip_length=0.13)
        gdp_l = boxed_label("GDP", AXIS_COL, size=22, box=(0.82, 0.42), pad=0.12, fill_opacity=0.14).move_to([lc[0] + 1.36, 1.38, 0])
        cross_cut = VGroup(
            Line([-0.16, -0.16, 0], [0.16, 0.16, 0], color=COL_INHIB, stroke_width=5),
            Line([-0.16, 0.16, 0], [0.16, -0.16, 0], color=COL_INHIB, stroke_width=5),
        ).move_to(cut_arr.get_center())

        dial_c = np.array([lc[0] + 2.18, 1.38, 0.0])
        timer_ring = Circle(radius=0.24, stroke_color=AXIS_COL, stroke_width=3).move_to(dial_c)
        timer_ang = ValueTracker(0.15)
        timer_arc = always_redraw(
            lambda: Arc(radius=0.24, start_angle=PI / 2, angle=-TAU * timer_ang.get_value(),
                        arc_center=dial_c, stroke_color=COL_INHIB, stroke_width=4.5)
        )
        timer_hand = always_redraw(
            lambda: Line(dial_c, dial_c + 0.18 * np.array([np.cos(PI / 2 - TAU * timer_ang.get_value()),
                                                           np.sin(PI / 2 - TAU * timer_ang.get_value()), 0]),
                         color=TEXT, stroke_width=3.5)
        )
        timer_dial = VGroup(timer_ring, timer_arc, timer_hand)
        off_lbl_1 = T("Off-timer: GTP hydrolysis,", 22, COL_EGF).move_to([lc[0] + 0.44, 0.86, 0])
        off_lbl_2 = T("sped by GAPs", 22, COL_INHIB, weight=BOLD).next_to(off_lbl_1, DOWN, buff=0.16)

        raf_l1 = boxed_label("Raf", COL_RAF, size=24, box=(1.10, 0.44), fill_opacity=0.22).move_to([lc[0] - 0.65, -0.22, 0])
        raf_l2 = boxed_label("Raf", COL_RAF, size=24, box=(1.10, 0.44), fill_opacity=0.22).move_to([lc[0] + 0.65, -0.22, 0])
        mek_l = boxed_label("MEK", COL_MEK, size=24, box=(1.50, 0.44), fill_opacity=0.22).move_to([lc[0], -1.04, 0])
        erk_l = boxed_label("ERK", COL_ERK, size=24, box=(1.50, 0.44), fill_opacity=0.22).move_to([lc[0], -1.86, 0])

        arr_l = VGroup(
            Arrow(ras_l.get_bottom() + DOWN * 0.05, raf_l1.get_top() + UP * 0.05, buff=0, color=COL_RAS, stroke_width=3.5, tip_length=0.12),
            Arrow(raf_l1.get_bottom() + DOWN * 0.05, mek_l.get_top() + UP * 0.05, buff=0, color=COL_RAF, stroke_width=3.5, tip_length=0.12),
            Arrow(raf_l2.get_bottom() + DOWN * 0.05, mek_l.get_top() + UP * 0.05, buff=0, color=COL_RAF, stroke_width=3.5, tip_length=0.12),
            _arrow_between(mek_l, erk_l, color=COL_MEK, stroke_width=3.5, tip_len=0.12, gap=0.05),
        )

        mem_r = Line([rc[0] - 2.55, 1.92, 0], [rc[0] + 2.55, 1.92, 0], color=COL_MEMBRANE, stroke_width=4)
        ras_r_box = RoundedRectangle(corner_radius=0.14, width=1.75, height=0.44, stroke_color=COL_MEMBRANE,
                                     stroke_width=2.5, fill_color=COL_MEMBRANE, fill_opacity=0.18).move_to([rc[0] - 1.55, 1.38, 0])
        ras_r_lbl = T("Ras (GDP)", 22, AXIS_COL).move_to(ras_r_box)
        ras_r = VGroup(ras_r_box, ras_r_lbl)
        braf_r = boxed_label("B-Raf V600E", COL_RAF, size=24, box=(2.15, 0.48), fill_opacity=0.22).move_to([rc[0] - 0.85, -0.22, 0])
        deb_lbl = T("Partner needed?\ndebated", 22, COL_EGF, line_spacing=0.80).next_to(braf_r, RIGHT, buff=0.22)
        mek_r = boxed_label("MEK", COL_MEK, size=24, box=(1.50, 0.44), fill_opacity=0.22).move_to([rc[0] - 0.85, -1.04, 0])
        erk_r = boxed_label("ERK", COL_ERK, size=24, box=(1.50, 0.44), fill_opacity=0.22).move_to([rc[0] - 0.85, -1.86, 0])
        arr_r = VGroup(
            _arrow_between(braf_r, mek_r, color=COL_RAF, stroke_width=3.5, tip_len=0.12, gap=0.05),
            _arrow_between(mek_r, erk_r, color=COL_MEK, stroke_width=3.5, tip_len=0.12, gap=0.05),
        )

        ph_l = ValueTracker(0.0)
        ph_r = ValueTracker(0.0)
        pulse_l = _segment_pulse([
            (ras_l.get_bottom() + DOWN * 0.05, raf_l1.get_top() + UP * 0.05),
            (raf_l1.get_bottom() + DOWN * 0.05, mek_l.get_top() + UP * 0.05),
            (mek_l.get_bottom() + DOWN * 0.05, erk_l.get_top() + UP * 0.05),
        ], ph_l, color=COL_EGF, radius=0.07)
        pulse_r = _segment_pulse([
            (braf_r.get_bottom() + DOWN * 0.05, mek_r.get_top() + UP * 0.05),
            (mek_r.get_bottom() + DOWN * 0.05, erk_r.get_top() + UP * 0.05),
        ], ph_r, color=COL_RAF, radius=0.07)

        # Tier border wave driven directly by the same signal phase tracker (never crosses text!)
        left_wave = VGroup(ras_l, raf_l1, mek_l, erk_l)
        right_wave = VGroup(braf_r, mek_r, erk_r)

        self.at("human tumors jam")
        self.play(FadeIn(bg_l), FadeIn(bg_r), FadeIn(tp), FadeIn(tp.left_head), FadeIn(mem_l), FadeIn(ras_norm), FadeIn(gtp_l),
                  FadeIn(raf_l1), FadeIn(raf_l2), FadeIn(mek_l), FadeIn(erk_l), FadeIn(arr_l), run_time=1.8)

        self.at("normally shuts itself off")
        self.play(FadeIn(cut_arr), FadeIn(gdp_l), FadeIn(timer_dial), timer_ang.animate.set_value(0.55), run_time=1.3)

        self.at("cutting gtp to gdp")
        self.play(FadeIn(off_lbl_1), timer_ang.animate.set_value(0.85), run_time=1.6)

        self.at("helped by gap proteins")
        self.play(FadeIn(off_lbl_2), timer_ang.animate.set_value(1.0), run_time=1.8)

        self.at("a single base change")
        mut_note = T("Gly 12 -> Val", 24, COL_RAS, weight=BOLD).move_to([lc[0], -2.38, 0])
        self.play(FadeIn(mut_note), run_time=1.0)

        self.at("glycine 12 to valine")
        self.play(FadeOut(ras_norm), FadeOut(tp.left_head), run_time=0.25)
        self.play(FadeIn(ras_l), FadeIn(left_head_jammed), run_time=0.35)
        self.play(Indicate(ras_l, color=COL_RAS, scale_factor=1.08), run_time=0.45)

        self.at("blunts that cut")
        jam_x = T("JAMMED", 22, COL_INHIB, weight=BOLD).move_to([dial_c[0] + 0.08, 0.46, 0])
        self.play(FadeIn(cross_cut), FadeIn(jam_x), gdp_l.animate.set_opacity(0.35), run_time=1.0)

        self.at("stays on")
        left_wave.add_updater(_tier_glow([ras_l, raf_l1, mek_l, erk_l], ph_l, base_width=2.5, amp=3.5))
        self.add(pulse_l)
        self.play(ph_l.animate.set_value(1.5), run_time=1.4, rate_func=linear)

        self.at("one tier down")
        self.play(FadeIn(mem_r), FadeIn(ras_r), FadeIn(mek_r), FadeIn(erk_r),
                  ph_l.animate.set_value(3.0), run_time=1.8, rate_func=linear)

        self.at("mutant b raf")
        self.play(FadeIn(tp.right_head), FadeIn(braf_r), FadeIn(arr_r), ph_l.animate.set_value(5.0), run_time=2.2, rate_func=linear)

        self.at("signals without")
        right_wave.add_updater(_tier_glow([braf_r, mek_r, erk_r], ph_r, base_width=2.5, amp=3.5))
        self.add(pulse_r)
        self.play(ph_l.animate.set_value(7.0), ph_r.animate.set_value(2.0), run_time=2.0, rate_func=linear)

        self.at("possibly even without")
        self.play(FadeIn(deb_lbl), ph_l.animate.set_value(9.0), ph_r.animate.set_value(4.0), run_time=2.0, rate_func=linear)
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        tp = TwoPanel("B-Raf V600E + Vemurafenib", "Active Ras + normal B-Raf",
                      colors=(COL_RAF, COL_RAS), top=2.75, bottom=-2.45, gap=0.45, width=12.6, size=28)
        bg_l, bg_r = _panel_bg(tp.left_frame), _panel_bg(tp.right_frame)
        lc = tp.area("left")[0]
        rc = tp.area("right")[0]

        braf_v = make_pocket_kinase("B-Raf V600E", COL_RAF, pocket_side="left", width=2.55, height=0.85,
                                    pocket_depth=0.38, pocket_h=0.40, font_size=24).move_to([lc[0] + 0.72, 0.85, 0])
        target_l = braf_v.body.get_center() + braf_v._pocket_offset
        vem_l = make_wedge(COL_INHIB, width=0.34, height=0.36).move_to(target_l + LEFT * 0.75)
        vem_l_docked = vem_l.copy().move_to(target_l)
        vem_l_lbl = T("Vemurafenib", 22, COL_INHIB).next_to(vem_l_docked, LEFT, buff=0.18)
        mek_l = boxed_label("MEK", COL_MEK, size=24, box=(1.6, 0.50), fill_opacity=0.22).move_to([lc[0], -0.45, 0])
        erk_l = boxed_label("ERK", COL_ERK, size=24, box=(1.8, 0.50), fill_opacity=0.22).move_to([lc[0], -1.65, 0])
        arr_l1 = Arrow(braf_v.get_bottom() + DOWN * 0.06, mek_l.get_top() + UP * 0.06, buff=0, color=COL_RAF, stroke_width=3.5, tip_length=0.13)
        arr_l2 = Arrow(mek_l.get_bottom() + DOWN * 0.06, erk_l.get_top() + UP * 0.06, buff=0, color=COL_MEK, stroke_width=3.5, tip_length=0.12)

        ras_r = boxed_label("Active Ras", COL_RAS, size=24, box=(2.2, 0.46), fill_opacity=0.22).move_to([rc[0] + 0.58, 1.35, 0])
        raf_l = make_pocket_kinase("Raf", COL_RAF, pocket_side="left", width=1.42, height=0.80,
                                   pocket_depth=0.32, pocket_h=0.36, font_size=24).move_to([rc[0] - 0.15, 0.30, 0])
        raf_r = make_pocket_kinase("Raf", COL_RAF, pocket_side="right", width=1.42, height=0.80,
                                   pocket_depth=0.32, pocket_h=0.36, font_size=24).move_to([rc[0] + 1.36, 0.30, 0])
        target_r = raf_l.body.get_center() + raf_l._pocket_offset
        vem_r = make_wedge(COL_INHIB, width=0.30, height=0.32).move_to(target_r + LEFT * 0.65)
        vem_r_docked = vem_r.copy().move_to(target_r)
        vem_r_lbl = T("Vemurafenib", 22, COL_INHIB).next_to(vem_r_docked, LEFT, buff=0.18)
        tether_l = Line(ras_r.get_bottom() + LEFT * 0.40 + DOWN * 0.04, raf_l.get_top() + UP * 0.04, color=COL_RAS, stroke_width=3)
        tether_r = Line(ras_r.get_bottom() + RIGHT * 0.40 + DOWN * 0.04, raf_r.get_top() + UP * 0.04, color=COL_RAS, stroke_width=3)
        mek_r = boxed_label("MEK", COL_MEK, size=24, box=(1.55, 0.46), fill_opacity=0.22).move_to([rc[0] - 1.15, -0.95, 0])
        arr_rm = Arrow(raf_r.get_bottom() + DOWN * 0.06, mek_r.get_top() + UP * 0.06, buff=0, color=COL_RAF, stroke_width=3.5, tip_length=0.13)

        g_center = np.array([rc[0] + 1.35, -1.42, 0.0])
        g_rad = 0.85
        g_track = Arc(radius=g_rad, start_angle=PI, angle=-PI, arc_center=g_center, stroke_color=AXIS_COL, stroke_width=8)
        g_q = T("?", 38, COL_ERK, weight=BOLD).move_to(g_center + UP * 0.30)
        g_lbl = T("ERK ?", 24, COL_ERK).move_to(g_center + DOWN * 0.36)
        gauge_q = VGroup(g_track, g_q, g_lbl)
        arr_mg = Arrow(mek_r.get_right() + RIGHT * 0.06, [g_center[0] - g_rad - 0.12, mek_r.get_center()[1], 0],
                       buff=0, color=COL_MEK, stroke_width=3, tip_length=0.12)

        tag = scope_tag("schematic", color=AXIS_COL).move_to([4.15, -3.12, 0])
        ph_l = ValueTracker(0.0)
        pkt_l = _segment_pulse([
            (braf_v.get_bottom() + DOWN * 0.07, mek_l.get_top() + UP * 0.07),
            (mek_l.get_bottom() + DOWN * 0.07, erk_l.get_top() + UP * 0.07),
        ], ph_l, color=COL_RAF, radius=0.07)

        self.at("now test how pathway")
        self.play(FadeIn(bg_l), FadeIn(bg_r), FadeIn(tp), FadeIn(braf_v), FadeIn(mek_l), FadeIn(erk_l),
                  Create(arr_l1), Create(arr_l2), FadeIn(tag), run_time=1.2)
        self.add(pkt_l)
        self.play(ph_l.animate.set_value(2.0), run_time=2.3, rate_func=linear)

        self.at("vemurafenib plugs the atp")
        self.play(FadeIn(vem_l), FadeOut(pkt_l), run_time=0.4)
        self.play(vem_l.animate.move_to(target_l), run_time=1.35)
        self.play(FadeIn(vem_l_lbl), run_time=0.45)

        self.at("shuts down braf")
        erk_off = boxed_label("ERK (off)", COL_ERK, size=24, box=(1.8, 0.50), fill_opacity=0.14).move_to(erk_l.get_center())
        cross_l = VGroup(
            Line([-0.14, -0.14, 0], [0.14, 0.14, 0], color=COL_INHIB, stroke_width=4),
            Line([-0.14, 0.14, 0], [0.14, -0.14, 0], color=COL_INHIB, stroke_width=4),
        ).move_to(arr_l1.get_center())
        self.play(
            arr_l1.animate.set_color(COL_INHIB),
            arr_l2.animate.set_color(COL_MEMBRANE),
            mek_l.box.animate.set_stroke(COL_MEMBRANE, width=2),
            swap(erk_l, erk_off, run_time=0.5),
            FadeIn(cross_l),
            run_time=2.2,
        )

        self.at("add that same drug")
        self.play(FadeIn(ras_r), FadeIn(raf_l), FadeIn(raf_r), Create(tether_l), Create(tether_r),
                  FadeIn(mek_r), Create(arr_rm), FadeIn(gauge_q), Create(arr_mg), run_time=1.5)

        self.at("active ras and normal braf")
        self.play(FadeIn(vem_r), run_time=0.4)
        self.play(vem_r.animate.move_to(target_r), run_time=1.7)
        self.play(FadeIn(vem_r_lbl), run_time=0.5)

        q = question_card("Active Ras + normal B-Raf + Raf drug: ERK falls, stays flat, or rises?",
                          y=-3.08, color=COL_EGF, size=27, left=-6.2, max_w=6.8)
        self.at("does erk fall")
        self.play(FadeIn(q.question), run_time=0.7)
        self.at("stay flat")
        self.play(Indicate(g_q, color=COL_EGF, scale_factor=1.12), run_time=0.5)
        self.at("or rise")
        self.play(Indicate(g_q, color=COL_ERK, scale_factor=1.12), run_time=0.5)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = "Active Ras + normal B-Raf + Raf drug: ERK falls, stays flat, or rises?"
    OPTIONS = ()
    CARD = {"y": -3.08, "color": COL_EGF, "size": 27, "left": -6.2, "max_w": 6.8}
    RING_AT = (5.85, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _predict_world()


class S08DrugReveal(SpokenScene):
    def construct(self):
        hdr = T("Active Ras + normal Raf pairs", 30, COL_RAS, weight=BOLD).move_to([-2.3, 3.22, 0])
        ras = boxed_label("Active Ras", COL_RAS, size=26, box=(2.4, 0.52), fill_opacity=0.22).move_to([-2.3, 2.50, 0])
        raf_l = make_pocket_kinase("Raf", COL_RAF, pocket_side="left", width=2.05, height=0.92,
                                   pocket_depth=0.40, pocket_h=0.42, font_size=26).move_to([-3.65, 1.42, 0])
        raf_r = make_pocket_kinase("Raf", COL_RAF, pocket_side="right", width=2.05, height=0.92,
                                   pocket_depth=0.40, pocket_h=0.42, font_size=26).move_to([-0.95, 1.42, 0])
        vem = make_wedge(COL_INHIB, width=0.38, height=0.38).move_to(raf_l.body.get_center() + raf_l._pocket_offset)
        vem_lbl = T("Vemurafenib", 22, COL_INHIB).next_to(vem, LEFT, buff=0.16)
        teth_l = always_redraw(lambda: Line(ras.get_bottom() + LEFT * 0.5 + DOWN * 0.04, raf_l.get_top() + UP * 0.04, color=COL_RAS, stroke_width=3.5))
        teth_r = always_redraw(lambda: Line(ras.get_bottom() + RIGHT * 0.5 + DOWN * 0.04, raf_r.get_top() + UP * 0.04, color=COL_RAS, stroke_width=3.5))

        mek_w, mek_h = 3.85, 1.18
        mek_c = np.array([-2.3, -1.62, 0.0])
        hw, hh = mek_w / 2.0, mek_h / 2.0
        mek_pts = [
            [-hw, hh, 0], [-1.32, hh, 0], [-1.32, hh - 0.42, 0], [-0.46, hh - 0.42, 0], [-0.46, hh, 0],
            [-0.08, hh, 0], [-0.08, hh - 0.42, 0], [0.78, hh - 0.42, 0], [0.78, hh, 0],
            [hw, hh, 0], [hw, -hh, 0], [-hw, -hh, 0],
        ]
        mek_body = Polygon(*mek_pts, stroke_color=COL_MEK, stroke_width=3, fill_color=COL_MEK, fill_opacity=0.25).move_to(mek_c)
        mek_lbl = T("MEK", 26, COL_MEK, weight=BOLD).move_to(mek_c + DOWN * 0.25)
        atp_blk = RoundedRectangle(corner_radius=0.06, width=0.78, height=0.38, stroke_color=COL_EGF, stroke_width=2,
                                   fill_color=COL_EGF, fill_opacity=0.90).move_to(mek_c + np.array([-0.89, hh - 0.21, 0]))
        atp_lbl = T("ATP", 22, BG, weight=BOLD).move_to(atp_blk)
        side_lbl = T("side pocket", 22, COL_INHIB).move_to(mek_c + np.array([0.35, hh + 0.26, 0]))
        mek_g = VGroup(mek_body, mek_lbl, atp_blk, atp_lbl)

        arr_raf_mek = always_redraw(lambda: Arrow(
            raf_r.get_bottom() + RIGHT * 0.45 + DOWN * 0.06,
            mek_body.get_top() + RIGHT * 1.45 + UP * 0.06,
            buff=0, color=COL_RAF, stroke_width=4, tip_length=0.14,
        ))

        erk_val = ValueTracker(0.25)
        gauge = make_erk_gauge(erk_val, center=[3.6, 0.35, 0], radius=1.55, label="Schematic ERK")
        status_rises = T("ERK RISES", 30, COL_ERK, weight=BOLD).move_to([3.6, -1.35, 0])
        status_falls = T("ERK FALLS", 30, COL_INHIB, weight=BOLD).move_to([3.6, -1.35, 0])
        arr_mek_erk = Arrow(mek_body.get_right() + RIGHT * 0.10, [1.55, mek_c[1], 0],
                            buff=0, color=COL_MEK, stroke_width=4, tip_length=0.15)

        ph = ValueTracker(0.0)

        def _pkt_dot():
            segs = [
                (raf_r.get_bottom() + RIGHT * 0.45 + DOWN * 0.06, mek_body.get_top() + RIGHT * 1.45 + UP * 0.06),
                (mek_body.get_right() + RIGHT * 0.12, np.array([1.50, mek_c[1], 0])),
            ]
            u = (ph.get_value() % 1.0) * len(segs)
            idx = min(len(segs) - 1, int(u))
            f = u - idx
            pa, pb = segs[idx]
            d = pb - pa
            dist = np.linalg.norm(d)
            if dist > 0.32:
                unit = d / dist
                pa, pb = pa + unit * 0.13, pb - unit * 0.13
            else:
                mid = (pa + pb) / 2.0
                pa, pb = mid, mid
            return Dot(pa + f * (pb - pa), radius=0.08, color=COL_RAF)

        pkt = always_redraw(_pkt_dot)

        self.add(hdr, ras, raf_l, raf_r, vem, vem_lbl, teth_l, teth_r, mek_g, arr_raf_mek, gauge, arr_mek_erk,
                 scope_tag("schematic", color=AXIS_COL))

        self.at("surprisingly")
        self.play(Indicate(gauge, color=COL_ERK, scale_factor=1.04), run_time=0.9)

        self.at("erk rises")
        self.add(pkt)
        self.play(erk_val.animate.set_value(0.86), FadeIn(status_rises), ph.animate.set_value(1.2), run_time=1.6)

        self.at("active ras brings normal")
        self.play(Indicate(ras, color=COL_RAS, scale_factor=1.08), ph.animate.set_value(2.4), run_time=2.2, rate_func=linear)

        self.at("into pairs at the membrane")
        self.play(
            raf_l.animate.move_to([-3.34, 1.42, 0]),
            vem.animate.shift(RIGHT * 0.31),
            vem_lbl.animate.shift(RIGHT * 0.31),
            raf_r.animate.move_to([-1.26, 1.42, 0]),
            ph.animate.set_value(3.8),
            run_time=2.4, rate_func=linear,
        )

        self.at("cannot work itself")
        blk_x = T("blocked", 22, COL_INHIB, weight=BOLD).next_to(vem_lbl, DOWN, buff=0.14)
        self.play(FadeIn(blk_x), ph.animate.set_value(4.8), run_time=1.2, rate_func=linear)

        self.at("yet its contact")
        contact_glow = Arrow(
            raf_l.get_right() + LEFT * 0.12,
            raf_r.get_left() + RIGHT * 0.25,
            buff=0, color=COL_EGF, stroke_width=6, tip_length=0.16,
        )
        contact_lbl = T("Activation by contact,\nnot catalysis", 22, COL_EGF, weight=BOLD, line_spacing=0.80).move_to([-2.78, 0.42, 0])
        self.play(Create(contact_glow), FadeIn(contact_lbl), raf_r.body.animate.set_fill(COL_RAF, opacity=0.45),
                  erk_val.animate.set_value(0.95), ph.animate.set_value(7.0), run_time=3.2, rate_func=linear)

        self.at("trametinib binds a separate")
        tram = RoundedRectangle(corner_radius=0.06, width=0.76, height=0.36, stroke_color=COL_INHIB, stroke_width=2.5,
                                fill_color=COL_INHIB, fill_opacity=0.92).move_to(mek_c + np.array([0.35, hh + 0.56, 0]))
        tram_lbl = T("Trametinib", 22, COL_INHIB, weight=BOLD).next_to(tram, UP, buff=0.10)
        self.play(FadeIn(side_lbl), ph.animate.set_value(7.3), run_time=0.45, rate_func=linear)
        self.play(FadeOut(side_lbl), ph.animate.set_value(7.6), run_time=0.35, rate_func=linear)
        self.play(FadeIn(tram), FadeIn(tram_lbl), ph.animate.set_value(8.4), run_time=1.25)
        self.play(
            tram.animate.move_to(mek_c + np.array([0.35, hh - 0.20, 0])),
            tram_lbl.animate.move_to(mek_c + np.array([0.35, hh + 0.28, 0])),
            ph.animate.set_value(9.6),
            run_time=1.85,
        )

        self.at("blocking mec below")
        cross_m = VGroup(
            Line([-0.15, -0.15, 0], [0.15, 0.15, 0], color=COL_INHIB, stroke_width=5),
            Line([-0.15, 0.15, 0], [0.15, -0.15, 0], color=COL_INHIB, stroke_width=5),
        ).move_to(arr_mek_erk.get_center())
        self.play(
            FadeOut(pkt),
            FadeIn(cross_m),
            arr_mek_erk.animate.set_color(COL_INHIB),
            mek_body.animate.set_fill(COL_MEMBRANE, opacity=0.22).set_stroke(COL_INHIB),
            erk_val.animate.set_value(0.10),
            swap(status_rises, status_falls, run_time=0.45),
            run_time=2.0,
        )

        self.at("so both drugs are often combined")
        combo = caption("Vemurafenib + Trametinib closes the escape", size=28, color=COL_EGF, y=-3.05)
        self.play(FadeIn(combo), run_time=1.4)
        self.finish()


class S09RasopathiesClose(SpokenScene):
    def construct(self):
        head = Circle(radius=0.58, stroke_color=TEXT, stroke_width=3, fill_color=CYTO_FILL, fill_opacity=0.85).move_to([-3.6, 1.95, 0])
        torso = RoundedRectangle(corner_radius=0.35, width=1.65, height=2.25, stroke_color=TEXT, stroke_width=3,
                                 fill_color=CYTO_FILL, fill_opacity=0.85).move_to([-3.6, 0.15, 0])
        leg_l = RoundedRectangle(corner_radius=0.16, width=0.52, height=1.85, stroke_color=TEXT, stroke_width=3,
                                 fill_color=CYTO_FILL, fill_opacity=0.85).move_to([-4.05, -1.95, 0])
        leg_r = RoundedRectangle(corner_radius=0.16, width=0.52, height=1.85, stroke_color=TEXT, stroke_width=3,
                                 fill_color=CYTO_FILL, fill_opacity=0.85).move_to([-3.15, -1.95, 0])
        body = VGroup(head, torso, leg_l, leg_r)

        z_face = Circle(radius=0.34, stroke_color=COL_RAS, stroke_width=3, fill_color=COL_ERK, fill_opacity=0.45).move_to(head.get_center() + DOWN * 0.08)
        z_heart = Circle(radius=0.34, stroke_color=COL_INHIB, stroke_width=3, fill_color=COL_RAS, fill_opacity=0.50).move_to([-3.45, 0.55, 0])
        z_growth = RoundedRectangle(corner_radius=0.12, width=0.32, height=1.35, stroke_color=COL_ERK, stroke_width=3,
                                    fill_color=COL_ERK, fill_opacity=0.45).move_to([-3.15, -1.90, 0])
        zones = VGroup(z_face, z_heart, z_growth)

        title_r = T("RASopathies (germline)", 30, COL_RAS, weight=BOLD).move_to([2.3, 2.85, 0])
        syn_noonan = T("Noonan syndrome", 26, TEXT).move_to([2.3, 2.15, 0])
        syn_nf1 = T("Neurofibromatosis type 1 (NF1)", 26, TEXT).move_to([2.3, 1.60, 0])

        ras_b = boxed_label("Ras", COL_RAS, size=26, box=(1.45, 0.52), fill_opacity=0.22).move_to([1.0, -0.35, 0])
        gtp_b = boxed_label("GTP", COL_EGF, size=24, box=(0.95, 0.46), fill_opacity=0.22).next_to(ras_b, RIGHT, buff=0.16)
        dial_c = gtp_b.get_right() + RIGHT * 0.52
        timer_bg = Circle(radius=0.30, stroke_color=AXIS_COL, stroke_width=3).move_to(dial_c)
        timer_ang = ValueTracker(0.15)
        timer_arc = always_redraw(
            lambda: Arc(radius=0.30, start_angle=PI / 2, angle=-TAU * max(0.05, timer_ang.get_value()),
                        arc_center=dial_c, stroke_color=COL_INHIB, stroke_width=4.5)
        )
        timer_hand = always_redraw(
            lambda: Line(dial_c, dial_c + 0.22 * np.array([np.cos(PI / 2 - TAU * timer_ang.get_value()),
                                                           np.sin(PI / 2 - TAU * timer_ang.get_value()), 0]),
                         color=TEXT, stroke_width=3)
        )
        gap_b = boxed_label("Neurofibromin", COL_INHIB, size=24, box=(2.5, 0.50), fill_opacity=0.22).move_to([2.2, -1.12, 0])
        gap_sub = T("a Ras GAP (off-timer)", 22, COL_INHIB, weight=BOLD).next_to(gap_b, DOWN, buff=0.10)
        nf1_note = T("No neurofibromin: Ras stays active", 24, COL_INHIB, weight=BOLD).move_to([2.3, -2.15, 0])

        tag = scope_tag("schematic", color=AXIS_COL)

        self.at("milder germline")
        self.play(FadeIn(body), FadeIn(title_r), FadeIn(tag), run_time=2.3)

        self.at("causes developmental syndromes")
        self.play(FadeIn(zones), run_time=1.0)
        self.play(
            z_face.animate.set_fill(opacity=0.75),
            z_heart.animate.set_fill(opacity=0.75),
            z_growth.animate.set_fill(opacity=0.75),
            run_time=2.0,
        )

        self.at("including noonan syndrome")
        self.play(FadeIn(syn_noonan), FadeIn(syn_nf1), run_time=2.2)

        self.at("in neurofibromatosis type 1")
        self.play(FadeIn(ras_b), FadeIn(gtp_b), FadeIn(timer_bg), FadeIn(timer_arc), FadeIn(timer_hand),
                  FadeIn(gap_b), FadeIn(gap_sub), run_time=1.4)
        self.play(timer_ang.animate.set_value(0.55), run_time=1.0)

        self.at("losing neurofibromin")
        self.play(gap_b.animate.set_opacity(0.45), Indicate(gap_sub, color=COL_INHIB, scale_factor=1.06), run_time=1.3)

        self.at("one of")
        self.play(Indicate(gap_b, color=COL_INHIB, scale_factor=1.05), timer_ang.animate.set_value(0.72), run_time=1.2)

        self.at("leaves")
        self.play(FadeOut(VGroup(gap_b, gap_sub)), run_time=0.45)
        self.play(FadeIn(nf1_note), gtp_b.animate.scale(1.08), timer_ang.animate.set_value(0.95), run_time=2.0)

        self.at("every cell carries")
        cell_dots = VGroup(
            Dot(head.get_center() + UP * 0.25, radius=0.07, color=COL_RAS),
            Dot(torso.get_center() + LEFT * 0.45, radius=0.07, color=COL_RAS),
            Dot(leg_l.get_center(), radius=0.07, color=COL_RAS),
        )
        same_lbl = T("Same variant in every cell", 24, COL_RAS).move_to([-3.6, -3.12, 0])
        self.play(FadeIn(cell_dots), FadeIn(same_lbl), run_time=1.5)

        self.at("yet tissues differ")
        diff_lbl = T("Yet tissues differ", 24, COL_ERK, weight=BOLD).move_to([2.3, 0.75, 0])
        self.play(FadeIn(diff_lbl, run_time=0.45), Indicate(zones, color=COL_EGF, scale_factor=1.06, run_time=1.8))

        cards = [
            (-4.2, "Duration", COL_EGF),
            (0.0, "Context", COL_NGF),
            (4.2, "Pathway state", COL_INHIB),
        ]
        card_w, card_h = 3.7, 3.8
        c_frames = VGroup(*[
            RoundedRectangle(corner_radius=0.18, width=card_w, height=card_h,
                             stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.16).move_to([x, 0.1, 0])
            for x, _, col in cards
        ])
        c_titles = VGroup(*[
            T(lbl, 28, col, weight=BOLD).move_to([x, 1.55, 0])
            for x, lbl, col in cards
        ])

        clk_c = np.array([-4.2, -0.25, 0.0])
        clk_ring = Circle(radius=0.95, stroke_color=COL_EGF, stroke_width=4, fill_color=COL_EGF, fill_opacity=0.14).move_to(clk_c)
        hand_ang = ValueTracker(PI / 2)
        clk_hand = always_redraw(lambda: Line(
            clk_c, clk_c + 0.72 * np.array([np.cos(hand_ang.get_value()), np.sin(hand_ang.get_value()), 0]),
            color=TEXT, stroke_width=4,
        ))
        icon_dur = VGroup(clk_ring, clk_hand, Dot(clk_c, radius=0.07, color=COL_EGF))

        c2_a = build_pc12_cell([-0.85, -0.15, 0], radius=0.35, color=COL_NGF)
        c2_n = build_neurite_tree([-0.50, -0.15, 0], direction=RIGHT, seed=3, scale=0.45)
        c2_b = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.58, height=0.20, stroke_color=COL_FOCI, stroke_width=2,
                             fill_color=COL_FOCI, fill_opacity=0.58).move_to([0.75 + dx, -0.65 + dy, 0])
            for dx, dy in [(-0.25, 0), (0.25, 0), (0.0, 0.24)]
        ])
        icon_ctx = VGroup(c2_a, c2_n, c2_b)

        p_l = boxed_label("Raf", COL_RAF, size=22, box=(1.1, 0.48), fill_opacity=0.22).move_to([3.55, 0.30, 0])
        p_r = boxed_label("Raf", COL_RAF, size=22, box=(1.1, 0.48), fill_opacity=0.22).move_to([4.85, 0.30, 0])
        p_mek = boxed_label("MEK", COL_MEK, size=22, box=(1.2, 0.44), fill_opacity=0.22).move_to([4.20, -0.85, 0])
        p_arr = Arrow(p_r.get_bottom() + DOWN * 0.05, p_mek.get_top() + UP * 0.05, buff=0, color=COL_RAF, stroke_width=3, tip_length=0.12)
        p_blk = make_wedge(COL_INHIB, width=0.32, height=0.30).move_to([4.98, -0.85, 0])
        icon_state = VGroup(p_l, p_r, p_mek, p_arr, p_blk)

        old_all = VGroup(body, zones, title_r, syn_noonan, syn_nf1, ras_b, gtp_b, timer_bg, timer_arc, timer_hand,
                         nf1_note, cell_dots, same_lbl, diff_lbl)

        self.at("across health and disease")
        self.play(FadeOut(old_all, run_time=0.45), FadeIn(c_frames, run_time=0.7), FadeIn(c_titles, run_time=0.7))

        self.at("duration")
        self.play(FadeIn(icon_dur), run_time=0.4)
        self.play(hand_ang.animate.set_value(PI / 2 - TAU * 0.45), run_time=0.8)

        self.at("cell context")
        self.play(FadeIn(icon_ctx), run_time=0.7)

        self.at("pathway state")
        self.play(FadeIn(icon_state), hand_ang.animate.set_value(PI / 2 - TAU * 0.85), run_time=1.8)
        self.finish()


class S10End(EndCard):
    LINE = "Duration, cell context, and pathway state shape what the cascade does."
