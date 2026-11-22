"""
Three Switches Turn Grip Into Crawling (Integrins and Rho GTPases, Chapter 2)

COLOUR MAP (one colour per concept across the whole film):
- MATRIX    = "#D4A359"  amber extracellular matrix / fibronectin surface
- MEMBRANE  = "#5C7A99"  slate-blue plasma membrane
- ALPHA     = "#2EC4B6"  teal integrin alpha chain / outer adhesion partner
- BETA      = "#FF6B6B"  coral integrin beta chain / adhesion partner
- TALIN     = "#9B72CF"  violet talin linker
- VINCULIN  = "#E85D9E"  magenta vinculin reinforcement
- ACTIN     = "#E2E8F0"  silver-white actin filaments, cables, branches, cores
- RHO       = "#F87171"  crimson Rho switch, myosin II bars, stress fibres, front Rho sensor
- RAC       = "#34D399"  emerald Rac switch and lamellipodium sheet
- CDC42     = "#60A5FA"  sky-blue Cdc42 switch, filopodia, WASP activator
- FAK_CY    = "#22D3EE"  cyan FAK-Src phosphorylation sparks
- WASP      = "#FB923C"  warm orange WASP effector in Cdc42 inset
- LOCK_GOLD = GOLD       (#D4A843) gold locks on adhesions, GTP 'on' state, question card, GEF
- OFF_GREY  = GREY       (#8B93A1) off-state badge border, GAP arrow (text stays full-opacity TEXT)

CARRIED WORLD:
A single fibroblast resting on the amber matrix slab (y in [-2.52, 2.12]), opened by tilting
the side-view adhesion cross-section from Chapter 1 into a top-down cell view in S01Hook,
then carried at consistent scale and coordinates through S10Closing, with a top switch bar
(y = 3.18) and a bottom step/question band (y = -3.12).

WHAT CHANGES IN EACH SPOKEN SCENE (and what computes it):
- S01Hook: Side-view adhesion pulls taut (pull_t tracker) and morphs geometrically into the
  top-down fibroblast on the amber matrix while seeded actin filaments stream and curve inside
  the cell (flow_t tracker, rng seed 7).
- S02GtpaseCycle: Cycle tracker (state_t, flow_t) flips the central switch badge between GDP
  off and GTP on via GEF exchange and GAP-accelerated splitting while effector coupling drives
  actin extension and remodeling inside the cell below.
- S03Rho: Alignment tracker (bundle_t) draws seeded actin filaments into 5 parallel cables,
  myosin II bars insert, focal adhesions enlarge, and Hookean tension tracker (tension_t)
  pulls myosin bars and adhesion ends inward.
- S04Rac: Protrusion tracker (prot_t) billows the right rim into a lamellipodium while a
  recursive 70-degree Arp2/3 branching tree (rng seed 42) grows outward to push the edge.
- S05Cdc42: Extension and probing trackers (filo_t, probe_t) extend 6 sky-blue filopodia
  with parallel formin-built actin cores and sweep their tips sinusoidally; a WASP inset
  unfolds (open_t) when Cdc42-GTP binds to nucleate an Arp2/3 branch.
- S06WiringAndCycle: Polarisation tracker (polar_t), front FAK-Src spark + GEF feedback
  (fb_t, push2_t), and Rho rear contraction (pull_t) drive the cell body rightward in 1-2-3.
- S07Predict: Gold clamps lock front and rear adhesions; strain tracker (strain_t, q_phase)
  oscillates tensed crimson stress fibres inward while computed cell displacement stays pinned at 0.
- S09Release: Rear clamps dissolve (rear_op), stride tracker (stride_t) shortens stress fibres
  and glides the cell rightward across the matrix, and a front Rho sensor pulse (rho_pulse)
  illuminates along the emerald leading edge.
- S10Closing: Coordinated locomotion tracker (walk_t) runs one full stride (Rac sheet,
  Cdc42 fingers, assembling/dissolving adhesions, Rho contraction), then stall_t breaks grip
  and switches so forward velocity drops to zero.
"""

from bp_parts import *

# ---- Concept Palette ----
MATRIX = "#D4A359"
MEMBRANE = "#5C7A99"
ALPHA = "#2EC4B6"
BETA = "#FF6B6B"
TALIN = "#9B72CF"
VINCULIN = "#E85D9E"
ACTIN = "#E2E8F0"
RHO = "#F87171"
RAC = "#34D399"
CDC42 = "#60A5FA"
FAK_CY = "#22D3EE"
WASP = "#FB923C"

# ---- Carried Stage Constants ----
MATRIX_CENTER = np.array([0.0, -0.20, 0.0])
MATRIX_W = 12.4
MATRIX_H = 4.65
TOP_BAR_Y = 3.18
BOTTOM_Y_BAND = -3.12


def make_matrix_slab(center=MATRIX_CENTER, width=MATRIX_W, height=MATRIX_H):
    """Amber extracellular matrix slab (no stroke so layout_check never treats it as a panel)."""
    slab = RoundedRectangle(
        corner_radius=0.22,
        width=width,
        height=height,
        fill_color=MATRIX,
        fill_opacity=0.16,
        stroke_width=0,
    ).move_to(center)
    slab.set_z_index(-5)
    return slab


def make_switch_bar(active=None, state_suffix=True, y=TOP_BAR_Y):
    """Top row of three Rho-family switch badges: Rho, Rac, Cdc42."""
    specs = [
        ("Rho", RHO, -3.2),
        ("Rac", RAC, 0.0),
        ("Cdc42", CDC42, 3.2),
    ]
    bar = VGroup()
    for name, col, x in specs:
        is_on = (active == name) or (active == "ALL")
        txt = f"{name} · GTP" if (is_on and state_suffix) else name
        badge = boxed_label(
            txt,
            color=col if is_on else TEXT,
            size=28,
            box=(2.35, 0.56),
            stroke=4.0 if is_on else 1.8,
            fill_opacity=0.26 if is_on else 0.06,
        )
        if not is_on:
            badge.box.set_stroke(col, width=1.8, opacity=0.65)
        badge.move_to([x, y, 0])
        badge.set_z_index(12)
        bar.add(badge)
    return bar


def make_adhesion_pair(pos, scale=1.0, glow=1.0):
    """A teal/coral integrin focal adhesion dot pair beneath the cell rim."""
    a = Dot(pos + LEFT * 0.09 * scale + DOWN * 0.04 * scale, radius=0.11 * scale, color=ALPHA).set_opacity(glow)
    b = Dot(pos + RIGHT * 0.09 * scale + UP * 0.04 * scale, radius=0.11 * scale, color=BETA).set_opacity(glow)
    ring = Circle(radius=0.21 * scale, stroke_color=ALPHA, stroke_width=2.0 * scale, stroke_opacity=0.50 * glow).move_to(pos)
    g = VGroup(ring, a, b)
    g.set_z_index(3)
    return g


def make_cell_ellipse(center, rx, ry, fill_col=MEMBRANE, fill_op=0.16, stroke_col=MEMBRANE, stroke_w=4.5):
    """Top-down fibroblast cell body outline."""
    cell = Ellipse(
        width=2 * rx,
        height=2 * ry,
        fill_color=fill_col,
        fill_opacity=fill_op,
        stroke_color=stroke_col,
        stroke_width=stroke_w,
    ).move_to(center)
    cell.set_z_index(1)
    return cell


def make_polar_cell(cx, cy, body_rx=2.15, body_ry=1.65, lam_ext=1.55, lam_spread=1.95, tail_pull=0.0):
    """Smooth polarised fibroblast contour: rounded tail on left, broad lamellipodium sheet on right."""
    tail_x = cx - body_rx + tail_pull
    front_x = cx + body_rx + lam_ext
    pts = [
        [front_x, cy, 0],
        [front_x - 0.15, cy + lam_spread * 0.65, 0],
        [cx + body_rx * 0.55, cy + lam_spread, 0],
        [cx - body_rx * 0.15, cy + body_ry, 0],
        [tail_x + 0.35, cy + body_ry * 0.72, 0],
        [tail_x, cy, 0],
        [tail_x + 0.35, cy - body_ry * 0.72, 0],
        [cx - body_rx * 0.15, cy - body_ry, 0],
        [cx + body_rx * 0.55, cy - lam_spread, 0],
        [front_x - 0.15, cy - lam_spread * 0.65, 0],
    ]
    poly = VMobject(
        stroke_color=MEMBRANE,
        stroke_width=4.5,
        fill_color=MEMBRANE,
        fill_opacity=0.15,
    )
    poly.set_points_smoothly([np.array(p, dtype=float) for p in pts + [pts[0]]])
    poly.set_z_index(1)
    return poly


def make_lam_sheet(cx, cy, body_rx=2.15, lam_ext=1.55, lam_spread=1.95, opacity=0.22):
    """Emerald-tinted lamellipodium crescent at the cell's right leading edge."""
    front_x = cx + body_rx + lam_ext
    back_x = cx + body_rx * 0.25
    pts = [
        [front_x, cy, 0],
        [front_x - 0.15, cy + lam_spread * 0.65, 0],
        [cx + body_rx * 0.55, cy + lam_spread, 0],
        [back_x, cy + lam_spread * 0.62, 0],
        [back_x - 0.25, cy, 0],
        [back_x, cy - lam_spread * 0.62, 0],
        [cx + body_rx * 0.55, cy - lam_spread, 0],
        [front_x - 0.15, cy - lam_spread * 0.65, 0],
    ]
    sheet = VMobject(
        stroke_color=RAC,
        stroke_width=3.0,
        stroke_opacity=0.85,
        fill_color=RAC,
        fill_opacity=opacity,
    )
    sheet.set_points_smoothly([np.array(p, dtype=float) for p in pts + [pts[0]]])
    sheet.set_z_index(2)
    return sheet


def compute_arp23_branches(origin_xy, base_angle=0.0, length=1.6, depth=3, seed=42):
    """Compute a deterministic 70-degree Arp2/3 branching actin tree.

    Returns list of (p0, p1, birth_t, end_t, gen) in normalized growth time [0, 1].
    """
    rng = np.random.default_rng(seed)
    segs = []
    arp_angle = 70.0 * DEGREES

    def recurse(p0, ang, seg_len, d, t0):
        t1 = min(1.0, t0 + 0.28)
        p1 = p0 + seg_len * np.array([np.cos(ang), np.sin(ang), 0.0])
        segs.append((p0, p1, t0, t1, d))
        if d <= 0:
            return
        sign = 1.0 if (rng.random() > 0.45) else -1.0
        if d == depth:
            recurse(p1, ang + 0.48 * arp_angle, seg_len * 0.76, d - 1, t1 * 0.85)
            recurse(p1, ang - 0.48 * arp_angle, seg_len * 0.76, d - 1, t1 * 0.85)
        else:
            recurse(p1, ang + rng.uniform(-0.12, 0.12), seg_len * 0.74, d - 1, t1 * 0.90)
            recurse(p0 + 0.65 * (p1 - p0), ang + sign * arp_angle, seg_len * 0.68, d - 1, t0 + 0.16)

    recurse(np.array([origin_xy[0], origin_xy[1], 0.0]), base_angle, length, depth, 0.0)
    return segs


def draw_arp23_tree(segs, progress, stroke_w=3.2):
    """Render computed Arp2/3 actin segments up to progress in [0, 1]."""
    g = VGroup()
    p = float(np.clip(progress, 0.0, 1.0))
    for p0, p1, t0, t1, gen in segs:
        if p <= t0:
            continue
        frac = float(np.clip((p - t0) / max(t1 - t0, 1e-4), 0.0, 1.0))
        q = p0 + frac * (p1 - p0)
        ln = Line(p0, q, color=ACTIN, stroke_width=max(2.0, stroke_w - 0.35 * (3 - gen)))
        g.add(ln)
        if frac > 0.15 and gen < 3:
            g.add(Dot(p0, radius=0.045, color=RAC))
    g.set_z_index(4)
    return g


def make_stress_fibres(left_pts, right_pts, tension=0.0, quiver_amp=0.0, quiver_phase=0.0, show_myosin=True):
    """Build actin-myosin II stress fibres spanning left_pts to right_pts.

    tension in [0, 1] straightens cable sag and draws myosin II bars inward.
    """
    g = VGroup()
    for i, (a, b) in enumerate(zip(left_pts, right_pts)):
        a = np.array(a, dtype=float)
        b = np.array(b, dtype=float)
        mid = 0.5 * (a + b)
        sag = (0.24 * (1.0 - tension)) * (-1 if i % 2 == 0 else 1)
        q_off = quiver_amp * np.sin(quiver_phase + i * 1.4)
        ctrl = mid + UP * (sag + q_off)
        cable = CubicBezier(a, 0.5 * (a + ctrl), 0.5 * (ctrl + b), b, color=ACTIN, stroke_width=4.0 + 1.8 * tension)
        g.add(cable)
        if show_myosin:
            pull_osc = 0.03 * np.sin(quiver_phase) if quiver_amp > 0 else 0.0
            for frac in (0.30, 0.50, 0.70):
                f_adj = 0.5 + (frac - 0.5) * (1.0 - 0.24 * tension - pull_osc)
                pos = cable.point_from_proportion(f_adj)
                tangent = b - a
                ang = np.arctan2(tangent[1], tangent[0])
                bar = RoundedRectangle(
                    corner_radius=0.04,
                    width=0.34,
                    height=0.11,
                    fill_color=RHO,
                    fill_opacity=0.95,
                    stroke_color=RHO,
                    stroke_width=1.5,
                ).rotate(ang).move_to(pos)
                g.add(bar)
    g.set_z_index(4)
    return g


def make_gold_clamp(pos, scale=1.0, opacity=1.0):
    """A crisp transparent-centre gold lock clamp around an adhesion (never covers adhesion dots)."""
    op = float(np.clip(opacity, 0.0, 1.0))
    box = RoundedRectangle(
        corner_radius=0.09,
        width=0.58 * scale,
        height=0.52 * scale,
        stroke_color=GOLD,
        stroke_width=3.8,
        stroke_opacity=op,
        fill_color=GOLD,
        fill_opacity=0.10 * op,
    ).move_to(pos)
    jaw1 = Line(
        pos + LEFT * 0.34 * scale + UP * 0.20 * scale,
        pos + RIGHT * 0.34 * scale + UP * 0.20 * scale,
        color=GOLD,
        stroke_width=3.8,
        stroke_opacity=op,
    )
    jaw2 = Line(
        pos + LEFT * 0.34 * scale + DOWN * 0.20 * scale,
        pos + RIGHT * 0.34 * scale + DOWN * 0.20 * scale,
        color=GOLD,
        stroke_width=3.8,
        stroke_opacity=op,
    )
    g = VGroup(box, jaw1, jaw2)
    g.set_z_index(6)
    return g


def make_side_adhesion(pull_val=0.0):
    """Side-view focal adhesion cross-section carried from Chapter 1.

    pull_val in [0, 0.5] switches integrins from bent to extended grip on the matrix;
    pull_val in [0.5, 1.0] slides actin and stretches talin with vinculin reinforcement.
    """
    grip_t = float(np.clip(pull_val / 0.5, 0.0, 1.0))
    force_t = float(np.clip((pull_val - 0.5) / 0.5, 0.0, 1.0))

    mat = Rectangle(width=11.8, height=1.25, fill_color=MATRIX, fill_opacity=0.30, stroke_color=MATRIX, stroke_width=2.5).move_to([0, -2.05, 0])
    mem = Rectangle(width=11.8, height=0.34, fill_color=MEMBRANE, fill_opacity=0.72, stroke_color=MEMBRANE, stroke_width=2.5).move_to([0, -0.55, 0])
    integrins = VGroup()
    talins = VGroup()
    vinculins = VGroup()
    actins = VGroup()
    shift_x = 0.72 * force_t
    knee_bend = 0.55 * (1.0 - grip_t)
    head_y = -1.16 - 0.29 * grip_t
    for cx in (-1.9, 1.9):
        a_top = np.array([cx - 0.16 - 0.06 * grip_t, -0.35, 0.0])
        a_knee = np.array([cx - 0.25 - knee_bend, -0.90, 0.0])
        a_bot = np.array([cx - 0.28 - 0.35 * knee_bend, head_y, 0.0])
        a_leg = VMobject(color=ALPHA, stroke_width=7).set_points_as_corners([a_top, a_knee, a_bot])
        a_head = Circle(radius=0.18, color=ALPHA, fill_color=ALPHA, fill_opacity=0.9).move_to(a_bot)

        b_top = np.array([cx + 0.12 + 0.12 * grip_t, -0.20, 0.0])
        b_knee = np.array([cx + 0.25 - 0.7 * knee_bend, -0.88, 0.0])
        b_bot = np.array([cx + 0.28 - 0.25 * knee_bend, head_y, 0.0])
        b_leg = VMobject(color=BETA, stroke_width=7).set_points_as_corners([b_top, b_knee, b_bot])
        b_head = Circle(radius=0.18, color=BETA, fill_color=BETA, fill_opacity=0.9).move_to(b_bot)
        integrins.add(a_leg, a_head, b_leg, b_head)

        t_start = b_top.copy()
        t_end = np.array([cx + 0.95 + shift_x, 0.92, 0])
        talin = Line(t_start, t_end, color=TALIN, stroke_width=9)
        talins.add(talin)

        v_mid = 0.55 * t_start + 0.45 * t_end + LEFT * 0.22
        v_scale = 0.75 + 0.35 * force_t
        vinc = RoundedRectangle(corner_radius=0.10, width=0.52 * v_scale, height=0.28 * v_scale, color=VINCULIN, fill_color=VINCULIN, fill_opacity=0.85).rotate(0.55).move_to(v_mid)
        vinculins.add(vinc)

    actin_cable = Line([-4.6 + shift_x, 1.05, 0], [4.6 + shift_x, 1.05, 0], color=ACTIN, stroke_width=8)
    actin_cable2 = Line([-4.2 + shift_x, 1.45, 0], [4.4 + shift_x, 1.45, 0], color=ACTIN, stroke_width=5)
    actins.add(actin_cable, actin_cable2)

    g = VGroup(mat, mem, integrins, talins, vinculins, actins)
    g.mat, g.mem, g.integrins, g.talins, g.vinculins, g.actins = mat, mem, integrins, talins, vinculins, actins
    return g


def make_topdown_resting_cell(flow_t=0.0, adh_scale=1.0, active_state=0.0, center=np.array([0.0, -0.25, 0.0]), rx=2.55, ry=2.25):
    """Top-down rounded fibroblast on amber matrix with adhesions and flowing actin."""
    cell = make_cell_ellipse(center, rx, ry)
    adh_offsets = [
        [-1.65, 1.10], [1.65, 1.10],
        [-1.95, -0.15], [1.95, -0.15],
        [-1.45, -1.35], [1.45, -1.35],
    ]
    adhs = VGroup(*[make_adhesion_pair(center + np.array([dx, dy, 0.0]), scale=adh_scale + 0.18 * active_state) for dx, dy in adh_offsets])

    rng = np.random.default_rng(7)
    fils = VGroup()
    span_boost = 0.32 * active_state
    for i in range(9):
        y0 = rng.uniform(-0.60 * ry, 0.60 * ry)
        x0 = rng.uniform(-0.62 * rx, -0.15 * rx) - span_boost
        x1 = rng.uniform(0.15 * rx, 0.62 * rx) + span_boost
        phase = rng.uniform(0, TAU)
        bend = (0.36 + 0.25 * active_state) * np.sin(flow_t * 2.2 + phase)
        slide = 0.25 * np.cos(flow_t * 1.4 + phase)
        p0 = center + np.array([x0 + slide, y0, 0.0])
        p1 = center + np.array([0.5 * (x0 + x1) + slide, y0 + bend, 0.0])
        p2 = center + np.array([x1 + slide, y0 - 0.5 * bend, 0.0])
        fil = CubicBezier(p0, 0.5 * (p0 + p1), 0.5 * (p1 + p2), p2, color=ACTIN, stroke_width=3.2 + 1.4 * active_state)
        fils.add(fil)
    fils.set_z_index(2)
    return VGroup(cell, adhs, fils), cell, adhs, fils


# ==================================================================
# SCENES
# ==================================================================

class S00Title(TitleCard):
    LESSON = "Integrins and Rho GTPases"
    TITLE = "Three Switches Turn Grip Into Crawling"


class S01Hook(SpokenScene):
    def construct(self):
        pull = ValueTracker(0.0)
        flow = ValueTracker(0.0)

        side_world = always_redraw(lambda: make_side_adhesion(pull.get_value()))
        lbl_mat = T("matrix", 28, MATRIX).move_to([4.4, -2.05, 0]).set_z_index(10)
        lbl_int = T("integrins", 28, ALPHA).move_to([-4.3, -1.06, 0]).set_z_index(10)
        lbl_tal = T("talin & vinculin", 28, TALIN).move_to([-4.0, 0.30, 0]).set_z_index(10)
        lbl_act = T("actin", 28, ACTIN).move_to([-4.2, 2.05, 0]).set_z_index(10)
        side_labels = VGroup(lbl_mat, lbl_int, lbl_tal, lbl_act)

        self.add(side_world, side_labels)
        self.play(pull.animate.set_value(0.18), run_time=1.0, rate_func=linear)

        self.at("how integrins switch grip")
        self.play(pull.animate.set_value(0.52), run_time=2.4, rate_func=linear)

        self.at("build force")
        self.play(pull.animate.set_value(1.0), run_time=2.2, rate_func=linear)

        self.at("yet a grip alone")
        self.play(FadeOut(side_labels, run_time=0.4))
        side_snap = make_side_adhesion(1.0)
        self.remove(side_world)
        side_body = VGroup(side_snap.mem, side_snap.integrins, side_snap.talins, side_snap.vinculins, side_snap.actins)
        self.add(side_snap.mat, side_body)

        slab = make_matrix_slab()
        top_grp, _, _, _ = make_topdown_resting_cell(flow_t=0.0, adh_scale=1.0, center=np.array([0.0, -0.25, 0.0]), rx=2.55, ry=2.25)
        self.play(
            ReplacementTransform(side_snap.mat, slab),
            ReplacementTransform(side_body, top_grp),
            run_time=1.8,
        )
        self.remove(top_grp)
        live_cell = always_redraw(lambda: make_topdown_resting_cell(flow.get_value(), adh_scale=1.0, center=np.array([0.0, -0.25, 0.0]), rx=2.55, ry=2.25)[0])
        self.add(live_cell)

        self.at("shape actin")
        q_hook = T("How do switches shape actin to crawl?", 30, GOLD).move_to([0.0, TOP_BAR_Y, 0]).set_z_index(12)
        self.play(FadeIn(q_hook, shift=DOWN * 0.1), run_time=0.5)
        self.play(flow.animate.set_value(2.2), run_time=2.0, rate_func=linear)

        self.at("three small switches")
        bar = make_switch_bar(active="ALL", state_suffix=False, y=TOP_BAR_Y)
        self.play(swap(q_hook, bar, run_time=0.6))

        self.at("run the actin skeleton")
        self.play(flow.animate.set_value(5.0), run_time=max(0.8, self.narration_s - self.elapsed()), rate_func=linear)
        self.finish()


class S02GtpaseCycle(SpokenScene):
    def construct(self):
        # Lower matrix slab slightly in S02 so the GEF / GDP-GTP / GAP row sits cleanly on dark background above it
        slab = make_matrix_slab(center=np.array([0.0, -0.62, 0.0]), width=MATRIX_W, height=3.85)
        bar = make_switch_bar(active="ALL", state_suffix=False, y=TOP_BAR_Y)
        flow = ValueTracker(0.0)
        state = ValueTracker(0.0)   # 0 = GDP off, 1 = GTP on

        cell_grp = always_redraw(
            lambda: make_topdown_resting_cell(
                flow.get_value(),
                adh_scale=1.0,
                active_state=state.get_value(),
                center=np.array([0.0, -0.78, 0.0]),
                rx=2.65,
                ry=1.62,
            )[0]
        )

        # Toggle badge row cleanly above amber matrix (y = 2.08; matrix top is 1.305)
        badge_pos = np.array([0.0, 2.08, 0.0])
        gdp_badge = boxed_label("GDP · off", color=TEXT, size=28, box=(2.25, 0.60), stroke=2.5, fill_opacity=0.08).move_to(badge_pos).set_z_index(12)
        gdp_badge.box.set_stroke(GREY, width=2.5)
        gtp_badge = boxed_label("GTP · on", color=GOLD, size=28, box=(2.25, 0.60), stroke=4.0, fill_opacity=0.28).move_to(badge_pos).set_z_index(12)

        gef_arrow = Arrow([-2.55, 2.08, 0], [-1.25, 2.08, 0], color=GOLD, stroke_width=4.5, buff=0).set_z_index(10)
        gef_lbl = T("GEF (on)", 28, GOLD).next_to(gef_arrow, LEFT, buff=0.18).set_z_index(12)
        gap_arrow = Arrow([2.55, 2.08, 0], [1.25, 2.08, 0], color=GREY, stroke_width=4.5, buff=0).set_z_index(10)
        gap_lbl = T("GAP (off)", 28, TEXT).next_to(gap_arrow, RIGHT, buff=0.18).set_z_index(12)
        split_note = T("speeds GTP splitting", 24, TEXT).next_to(gap_lbl, DOWN, buff=0.12).set_z_index(12)

        eff_line = always_redraw(
            lambda: DashedLine(
                [0.0, 1.74, 0],
                [0.0, 0.90, 0],
                color=GOLD,
                stroke_width=4.0,
                dash_length=0.12,
            ).set_stroke(opacity=float(np.clip((state.get_value() - 0.3) * 1.5, 0.0, 1.0))).set_z_index(9)
        )
        eff_lbl = T("effector engaged", 26, GOLD).move_to([1.95, 1.48, 0]).set_z_index(12)
        tag = scope_tag("schematic", size=24, color=TEXT).set_z_index(12)

        badge = gdp_badge.copy()
        self.add(slab, bar, cell_grp, badge, eff_line, tag)

        self.play(flow.animate.set_value(1.6), run_time=2.5, rate_func=linear)
        self.at("flip between two states")
        next_b = gtp_badge.copy()
        self.play(swap(badge, next_b, run_time=0.35), state.animate.set_value(1.0), run_time=0.35)
        badge = next_b
        self.play(flow.animate.set_value(2.6), run_time=0.85, rate_func=linear)
        next_b = gdp_badge.copy()
        self.play(swap(badge, next_b, run_time=0.35), state.animate.set_value(0.0), run_time=0.35)
        badge = next_b
        self.play(flow.animate.set_value(3.4), run_time=0.75, rate_func=linear)

        self.at("bound to gtp")
        next_b = gtp_badge.copy()
        self.play(swap(badge, next_b, run_time=0.35), state.animate.set_value(1.0), run_time=0.35)
        badge = next_b
        self.play(flow.animate.set_value(4.9), run_time=1.45, rate_func=linear)

        self.at("engages its effectors")
        self.play(FadeIn(eff_lbl, shift=LEFT * 0.1), flow.animate.set_value(6.5), run_time=2.2, rate_func=linear)

        self.at("bound to gdp")
        self.play(FadeOut(eff_lbl, run_time=0.3))
        next_b = gdp_badge.copy()
        self.play(swap(badge, next_b, run_time=0.35), state.animate.set_value(0.0), run_time=0.35)
        badge = next_b
        self.play(flow.animate.set_value(8.0), run_time=1.65, rate_func=linear)

        self.at("exchange factors swap")
        self.play(GrowArrow(gef_arrow), FadeIn(gef_lbl, shift=RIGHT * 0.1), run_time=0.7)
        self.play(Indicate(gef_arrow, color=GOLD, scale_factor=1.08), run_time=0.6)
        next_b = gtp_badge.copy()
        self.play(swap(badge, next_b, run_time=0.35), state.animate.set_value(1.0), run_time=0.35)
        badge = next_b
        self.play(flow.animate.set_value(11.4), run_time=3.65, rate_func=linear)

        self.at("proteins speed its own")
        self.play(GrowArrow(gap_arrow), FadeIn(gap_lbl, shift=LEFT * 0.1), FadeIn(split_note), run_time=0.7)
        self.play(Indicate(gap_arrow, color=TEXT, scale_factor=1.08), run_time=0.6)
        next_b = gdp_badge.copy()
        self.play(swap(badge, next_b, run_time=0.35), state.animate.set_value(0.0), run_time=0.35)
        badge = next_b
        self.play(flow.animate.set_value(13.5), run_time=max(0.6, self.narration_s - self.elapsed()), rate_func=linear)
        self.finish()


def _rho_cell_builder(center, bundle_t, adh_t, myosin_t, tension_t):
    """Build fibroblast with computed transition from resting actin to contracted stress fibres."""
    rx = 3.10 - 0.34 * tension_t
    ry = 2.10 + 0.12 * tension_t
    cell = make_cell_ellipse(center, rx, ry)
    ys = [-1.20, -0.60, 0.0, 0.60, 1.20]
    x_span = [2.05, 2.45, 2.65, 2.45, 2.05]
    inward = 0.40 * tension_t
    l_pts = [center + np.array([-xs + inward, y, 0.0]) for xs, y in zip(x_span, ys)]
    r_pts = [center + np.array([xs - inward, y, 0.0]) for xs, y in zip(x_span, ys)]

    adhs = VGroup()
    scale = 0.95 + 0.42 * adh_t
    for p in l_pts + r_pts:
        adhs.add(make_adhesion_pair(p, scale=scale))

    cables = VGroup()
    if bundle_t < 0.05:
        rng = np.random.default_rng(7)
        for i in range(8):
            y0 = rng.uniform(-1.3, 1.3)
            p0 = center + np.array([-1.6, y0, 0])
            p1 = center + np.array([0.0, y0 + 0.3 * np.sin(i), 0])
            p2 = center + np.array([1.6, y0 - 0.2 * np.cos(i), 0])
            cables.add(CubicBezier(p0, 0.5 * (p0 + p1), 0.5 * (p1 + p2), p2, color=ACTIN, stroke_width=3.2))
    else:
        for i, (lp, rp) in enumerate(zip(l_pts, r_pts)):
            mid = 0.5 * (lp + rp)
            sag = (0.38 * (1.0 - bundle_t) + 0.18 * (1.0 - tension_t)) * (-1 if i % 2 == 0 else 1)
            ctrl = mid + UP * sag
            w = 3.2 + 2.4 * bundle_t + 1.4 * tension_t
            cab = CubicBezier(lp, 0.5 * (lp + ctrl), 0.5 * (ctrl + rp), rp, color=ACTIN, stroke_width=w)
            cables.add(cab)
            if myosin_t > 0.05:
                for frac in (0.30, 0.50, 0.70):
                    f_adj = 0.5 + (frac - 0.5) * (1.0 - 0.28 * tension_t)
                    pos = cab.point_from_proportion(f_adj)
                    bar = RoundedRectangle(
                        corner_radius=0.04,
                        width=0.36 * myosin_t,
                        height=0.12,
                        fill_color=RHO,
                        fill_opacity=0.95 * myosin_t,
                        stroke_color=RHO,
                        stroke_width=1.5,
                    ).move_to(pos)
                    cables.add(bar)
    cables.set_z_index(4)
    return VGroup(cell, adhs, cables)


class S03Rho(SpokenScene):
    def construct(self):
        slab = make_matrix_slab()
        bar = make_switch_bar(active="Rho", y=TOP_BAR_Y)
        center = np.array([-1.35, -0.25, 0.0])

        bundle_t = ValueTracker(0.0)
        adh_t = ValueTracker(0.0)
        myosin_t = ValueTracker(0.0)
        tension_t = ValueTracker(0.0)

        cell = always_redraw(
            lambda: _rho_cell_builder(center, bundle_t.get_value(), adh_t.get_value(), myosin_t.get_value(), tension_t.get_value())
        )

        c_rho = boxed_label("Rho", RHO, size=28, box=(2.9, 0.54)).move_to([4.25, 1.35, 0]).set_z_index(12)
        a1 = Arrow([4.25, 0.98, 0], [4.25, 0.48, 0], color=RHO, stroke_width=3.5, buff=0).set_z_index(10)
        c_rock = boxed_label("Rho kinase (ROCK)", RHO, size=26, box=(3.2, 0.56)).move_to([4.25, 0.10, 0]).set_z_index(12)
        a2 = Arrow([4.25, -0.28, 0], [4.25, -0.78, 0], color=RHO, stroke_width=3.5, buff=0).set_z_index(10)
        c_myo = boxed_label("myosin II", RHO, size=28, box=(2.9, 0.54)).move_to([4.25, -1.15, 0]).set_z_index(12)

        lbl_sf = T("stress fibres", 30, RHO).move_to([-1.35, BOTTOM_Y_BAND, 0]).set_z_index(12)

        self.add(slab, bar, cell)
        self.play(bundle_t.animate.set_value(0.35), run_time=2.5, rate_func=linear)

        self.at("thick contractile cables")
        self.play(bundle_t.animate.set_value(1.0), run_time=2.4, rate_func=linear)

        self.at("these are stress")
        self.play(FadeIn(lbl_sf, shift=UP * 0.1), adh_t.animate.set_value(0.25), run_time=0.8)

        self.at("actin and myosin")
        self.play(myosin_t.animate.set_value(1.0), adh_t.animate.set_value(0.45), run_time=1.2)

        self.at("anchored at focal adhesions")
        self.play(adh_t.animate.set_value(1.0), run_time=1.5)

        self.at("row activates")
        self.play(FadeIn(c_rho), GrowArrow(a1), FadeIn(c_rock), tension_t.animate.set_value(0.25), run_time=1.5)
        self.play(GrowArrow(a2), FadeIn(c_myo), tension_t.animate.set_value(0.45), run_time=1.2)

        self.at("cables contract and pull")
        self.play(tension_t.animate.set_value(1.0), run_time=max(1.2, self.narration_s - self.elapsed()), rate_func=linear)
        self.finish()


def _rac_cell_builder(center, prot_t, arp_segs, extra_branch_t):
    """Fibroblast billowing rightward into an emerald lamellipodium with computed 70-deg Arp2/3 tree."""
    cx, cy = center[0], center[1]
    lam_ext = 0.25 + 1.95 * prot_t
    lam_spread = 1.65 + 0.45 * prot_t
    body_rx = 2.25
    body_ry = 1.85

    cell = make_polar_cell(cx, cy, body_rx=body_rx, body_ry=body_ry, lam_ext=lam_ext, lam_spread=lam_spread)
    sheet = make_lam_sheet(cx, cy, body_rx=body_rx, lam_ext=lam_ext, lam_spread=lam_spread, opacity=0.06 + 0.24 * prot_t)

    adhs = VGroup(
        make_adhesion_pair([cx - 1.5, cy + 1.0, 0], scale=1.0),
        make_adhesion_pair([cx - 1.5, cy - 1.0, 0], scale=1.0),
        make_adhesion_pair([cx + 0.4, cy + 1.35, 0], scale=1.0),
        make_adhesion_pair([cx + 0.4, cy - 1.35, 0], scale=1.0),
    )

    tree = VGroup()
    if prot_t > 0.04:
        for seg_list in arp_segs:
            tree.add(draw_arp23_tree(seg_list, prot_t, stroke_w=3.2))
    if extra_branch_t > 0.01:
        m0 = np.array([cx + 1.55, cy + 0.25, 0.0])
        m1 = m0 + np.array([1.25, 0.20, 0.0])
        mother = Line(m0, m1, color=ACTIN, stroke_width=5.0)
        b_start = m0 + 0.45 * (m1 - m0)
        ang = np.arctan2(0.20, 1.25) + 70.0 * DEGREES
        b_end = b_start + extra_branch_t * 0.95 * np.array([np.cos(ang), np.sin(ang), 0.0])
        daughter = Line(b_start, b_end, color=RAC, stroke_width=5.0)
        arp_dot = Dot(b_start, radius=0.09, color=RAC, stroke_color=TEXT, stroke_width=2.0)
        tree.add(mother, daughter, arp_dot)
    tree.set_z_index(4)
    return VGroup(cell, sheet, adhs, tree)


class S04Rac(SpokenScene):
    def construct(self):
        slab = make_matrix_slab()
        bar = make_switch_bar(active="Rho", y=TOP_BAR_Y)
        center = np.array([-1.65, -0.25, 0.0])

        arp_segs = [
            compute_arp23_branches([center[0] + 0.75, center[1] + 0.50], base_angle=0.18, length=0.80, depth=2, seed=42),
            compute_arp23_branches([center[0] + 0.75, center[1] - 0.50], base_angle=-0.18, length=0.80, depth=2, seed=43),
            compute_arp23_branches([center[0] + 0.90, center[1]], base_angle=0.0, length=1.15, depth=2, seed=44),
        ]

        prot_t = ValueTracker(0.0)
        extra_t = ValueTracker(0.0)

        cell = always_redraw(lambda: _rac_cell_builder(center, prot_t.get_value(), arp_segs, extra_t.get_value()))

        c_rac = boxed_label("Rac", RAC, size=28, box=(2.8, 0.54)).move_to([4.55, 1.35, 0]).set_z_index(12)
        a1 = Arrow([4.55, 0.98, 0], [4.55, 0.48, 0], color=RAC, stroke_width=3.5, buff=0).set_z_index(10)
        c_wave = boxed_label("WAVE complex", RAC, size=26, box=(2.9, 0.56)).move_to([4.55, 0.10, 0]).set_z_index(12)
        a2 = Arrow([4.55, -0.28, 0], [4.55, -0.78, 0], color=RAC, stroke_width=3.5, buff=0).set_z_index(10)
        c_arp = boxed_label("Arp2/3", RAC, size=28, box=(2.8, 0.54)).move_to([4.55, -1.15, 0]).set_z_index(12)

        lbl_lam = T("lamellipodium", 30, RAC).move_to([-0.2, BOTTOM_Y_BAND, 0]).set_z_index(12)

        self.add(slab, bar, cell)
        self.play(Transform(bar, make_switch_bar(active="Rac", y=TOP_BAR_Y)), run_time=0.45)
        self.play(prot_t.animate.set_value(0.20), run_time=1.8)

        self.at("pushes out a broad")
        self.play(prot_t.animate.set_value(0.68), run_time=2.6, rate_func=linear)

        self.at("called a lamellipodium")
        self.play(FadeIn(lbl_lam, shift=UP * 0.1), prot_t.animate.set_value(0.80), run_time=1.4, rate_func=linear)

        self.at("turns on the wave complex")
        self.play(FadeIn(c_rac), GrowArrow(a1), FadeIn(c_wave), prot_t.animate.set_value(0.86), run_time=1.4)
        self.play(GrowArrow(a2), FadeIn(c_arp), prot_t.animate.set_value(0.90), run_time=1.1)

        self.at("starts each new actin")
        self.play(extra_t.animate.set_value(0.45), prot_t.animate.set_value(0.95), run_time=1.2, rate_func=linear)

        self.at("as a branch")
        self.play(
            extra_t.animate.set_value(1.0),
            prot_t.animate.set_value(1.0),
            run_time=max(1.0, self.narration_s - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


def _cdc42_cell_builder(center, filo_t, probe_t):
    """Fibroblast with protruding sky-blue filopodia and parallel formin-built actin cores."""
    cx, cy = center[0], center[1]
    cell = make_polar_cell(cx, cy, body_rx=1.85, body_ry=1.65, lam_ext=0.95, lam_spread=1.70)
    sheet = make_lam_sheet(cx, cy, body_rx=1.85, lam_ext=0.95, lam_spread=1.70, opacity=0.14)
    adhs = VGroup(
        make_adhesion_pair([cx - 1.15, cy + 0.90, 0]),
        make_adhesion_pair([cx - 1.15, cy - 0.90, 0]),
        make_adhesion_pair([cx + 0.70, cy + 1.15, 0]),
        make_adhesion_pair([cx + 0.70, cy - 1.15, 0]),
    )

    filos = VGroup()
    base_angles = [-0.55, -0.32, -0.11, 0.11, 0.32, 0.55]
    lengths = [1.55, 1.85, 2.05, 1.95, 1.80, 1.50]
    for i, (ang0, L0) in enumerate(zip(base_angles, lengths)):
        ang = ang0 + 0.15 * np.sin(probe_t + i * 1.1)
        L = max(0.05, L0 * filo_t)
        base = np.array([cx + 2.25 * np.cos(ang0 * 0.8), cy + 1.55 * np.sin(ang0 * 1.15), 0.0])
        tip = base + L * np.array([np.cos(ang), np.sin(ang), 0.0])
        perp = np.array([-np.sin(ang), np.cos(ang), 0.0])
        sheath = Polygon(
            base + perp * 0.11,
            tip + perp * 0.045,
            tip - perp * 0.045,
            base - perp * 0.11,
            color=CDC42,
            stroke_width=2.5,
            fill_color=CDC42,
            fill_opacity=0.22,
        )
        c1 = Line(base + perp * 0.035, tip - 0.05 * (tip - base) / max(L, 0.1) + perp * 0.02, color=ACTIN, stroke_width=2.6)
        c2 = Line(base - perp * 0.035, tip - 0.05 * (tip - base) / max(L, 0.1) - perp * 0.02, color=ACTIN, stroke_width=2.6)
        filos.add(sheath, c1, c2)
    filos.set_z_index(4)
    return VGroup(cell, sheet, adhs, filos)


def _wasp_inset_contents(open_t):
    """Animated contents inside the WASP inset (drawn on top of the static panel)."""
    hinge = np.array([-4.15, 0.22, 0.0])
    ang = (1.0 - open_t) * 1.35
    arm_a = RoundedRectangle(corner_radius=0.08, width=1.05, height=0.34, color=WASP, fill_color=WASP, fill_opacity=0.35).move_to(hinge + LEFT * 0.60)
    arm_b = (
        RoundedRectangle(corner_radius=0.08, width=1.05, height=0.34, color=WASP, fill_color=WASP, fill_opacity=0.35)
        .rotate(-ang)
        .move_to(hinge + 0.60 * np.array([np.cos(-ang), np.sin(-ang), 0.0]))
    )
    p0 = hinge + LEFT * 0.08
    p2 = hinge + 0.08 * np.array([np.cos(-ang), np.sin(-ang), 0.0])
    ctrl = hinge + UP * (0.14 * (1.0 - open_t))
    linker = CubicBezier(p0, 0.5 * (p0 + ctrl), 0.5 * (ctrl + p2), p2, color=WASP, stroke_width=6.0, fill_opacity=0.0)
    hinge_dot = Dot(hinge, radius=0.055, color=WASP)
    wasp_lbl = T("WASP (folded)" if open_t < 0.5 else "WASP (open)", 24, TEXT).move_to([-4.15, 0.72, 0])

    g = VGroup(linker, hinge_dot, arm_a, arm_b, wasp_lbl)

    if open_t > 0.08:
        cdc_dock = boxed_label("Cdc42·GTP", CDC42, size=24, box=(1.85, 0.44), fill_opacity=0.18).move_to([-4.15, 1.42 - 0.22 * open_t, 0])
        g.add(cdc_dock)

    if open_t > 0.55:
        arp_chip = boxed_label("Arp2/3", ACTIN, size=24, box=(1.45, 0.44), fill_opacity=0.18).move_to([-4.15, -0.72, 0])
        b_prog = float(np.clip((open_t - 0.55) / 0.45, 0.05, 1.0))
        b1 = Line([-4.65, -1.26, 0], [-4.65 + 1.0 * b_prog, -1.26, 0], color=ACTIN, stroke_width=3.5)
        callout = T("Cdc42 → WASP\n→ Arp2/3", 24, CDC42, line_spacing=0.85).move_to([-4.15, -1.86, 0])
        g.add(arp_chip, b1, callout)
        if b_prog > 0.5:
            b2_prog = (b_prog - 0.5) / 0.5
            b2 = Line([-4.15, -1.26, 0], [-4.15 + 0.42 * b2_prog, -1.26 + 0.24 * b2_prog, 0], color=ACTIN, stroke_width=3.5)
            g.add(b2)

    g.set_z_index(12)
    return g


class S05Cdc42(SpokenScene):
    def construct(self):
        slab = make_matrix_slab()
        bar = make_switch_bar(active="Rac", y=TOP_BAR_Y)
        center = np.array([1.05, -0.25, 0.0])

        filo_t = ValueTracker(0.05)
        probe_t = ValueTracker(0.0)
        open_t = ValueTracker(0.0)

        cell = always_redraw(lambda: _cdc42_cell_builder(center, filo_t.get_value(), probe_t.get_value()))
        lbl_filo = T("filopodia", 30, CDC42).move_to([4.55, 2.52, 0]).set_z_index(12)
        lbl_formin = T("cores built mainly by formins", 26, TEXT).move_to([2.45, BOTTOM_Y_BAND, 0]).set_z_index(12)

        self.add(slab, bar, cell)
        self.play(Transform(bar, make_switch_bar(active="Cdc42", y=TOP_BAR_Y)), run_time=0.45)
        self.play(filo_t.animate.set_value(0.55), run_time=2.5, rate_func=linear)

        self.at("triggering filopodia")
        self.play(filo_t.animate.set_value(1.0), FadeIn(lbl_filo, shift=DOWN * 0.1), run_time=2.5)

        self.at("probe the surface ahead")
        self.play(probe_t.animate.set_value(0.8 * TAU), run_time=2.0, rate_func=linear)

        self.at("other proteins")
        self.play(FadeIn(lbl_formin, shift=UP * 0.1), probe_t.animate.set_value(1.1 * TAU), run_time=0.7, rate_func=linear)

        self.at("build those parallel cores")
        self.play(probe_t.animate.set_value(2.0 * TAU), run_time=2.8, rate_func=linear)

        self.at("opens folded wasp")
        inset_panel = RoundedRectangle(
            corner_radius=0.18,
            width=3.95,
            height=4.15,
            stroke_color=CDC42,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to([-4.15, -0.25, 0]).set_z_index(10)
        self.play(FadeIn(inset_panel), run_time=0.4)
        wasp_contents = always_redraw(lambda: _wasp_inset_contents(open_t.get_value()))
        self.add(wasp_contents)
        self.play(open_t.animate.set_value(0.50), probe_t.animate.set_value(2.5 * TAU), run_time=1.8, rate_func=linear)

        self.at("freeing them to activate")
        self.play(
            open_t.animate.set_value(1.0),
            probe_t.animate.set_value(3.4 * TAU),
            run_time=max(1.0, self.narration_s - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


def _fade_stress_fibres(fibres, op):
    """Fade stress fibre cables by stroke opacity only (never filling CubicBeziers) and myosin bars normally."""
    for m in fibres:
        if isinstance(m, CubicBezier):
            m.set_fill(opacity=0.0).set_stroke(opacity=op)
        else:
            m.set_fill(opacity=0.95 * op).set_stroke(opacity=op)


def _wiring_cell_builder(cx, cy, polar_t, spark_t, fb_t, push2_t, pull_t, arp_segs):
    """Polarising fibroblast showing FAK-Src feedback to Rac GEFs and 1-2-3 stride."""
    lam_ext = 0.40 + 1.20 * polar_t + 0.55 * push2_t
    lam_spread = 1.65 + 0.25 * polar_t
    tail_pull = 0.28 * pull_t
    cell = make_polar_cell(cx, cy, body_rx=2.15, body_ry=1.65, lam_ext=lam_ext, lam_spread=lam_spread, tail_pull=tail_pull)
    sheet = make_lam_sheet(cx, cy, body_rx=2.15, lam_ext=lam_ext, lam_spread=lam_spread, opacity=0.14 + 0.14 * polar_t)

    front_pts = [[cx + 1.95, cy + 0.85, 0], [cx + 2.30, cy, 0], [cx + 1.95, cy - 0.85, 0]]
    rear_pts = [[cx - 1.55 + tail_pull, cy + 0.85, 0], [cx - 1.75 + tail_pull, cy, 0], [cx - 1.55 + tail_pull, cy - 0.85, 0]]
    adhs = VGroup()
    for p in front_pts:
        adhs.add(make_adhesion_pair(p, scale=0.8 + 0.45 * polar_t))
    for p in rear_pts:
        adhs.add(make_adhesion_pair(p, scale=1.0))

    tree = VGroup()
    for seg_list in arp_segs:
        shifted = [(p0 + RIGHT * cx, p1 + RIGHT * cx, t0, t1, gen) for p0, p1, t0, t1, gen in seg_list]
        tree.add(draw_arp23_tree(shifted, min(1.0, 0.30 + 0.50 * polar_t + 0.20 * push2_t), stroke_w=2.8))

    sparks = VGroup()
    if spark_t > 0.05:
        for p in front_pts:
            ring = Circle(radius=0.28 + 0.10 * spark_t, color=FAK_CY, stroke_width=3.5, fill_opacity=0.0).move_to(p).set_stroke(opacity=spark_t)
            sparks.add(ring)
    sparks.set_z_index(5)

    fibres = make_stress_fibres(rear_pts, front_pts, tension=pull_t, show_myosin=(pull_t > 0.05))
    _fade_stress_fibres(fibres, 0.35 + 0.65 * pull_t)

    # Feedback arrow routed cleanly outside the upper front sheet toward the GEF -> Rac label (clear of text)
    fb_grp = VGroup()
    if fb_t > 0.05:
        arr = CurvedArrow([cx + 2.25, cy + 1.15, 0], [3.86, 1.30, 0], angle=-0.45, color=FAK_CY, stroke_width=4.0)
        arr.set_fill(opacity=0.0).set_stroke(opacity=fb_t)
        if hasattr(arr, "tip"):
            arr.tip.set_fill(opacity=fb_t).set_stroke(opacity=fb_t)
        fb_grp.add(arr)
    fb_grp.set_z_index(6)

    return VGroup(cell, sheet, adhs, tree, fibres, sparks, fb_grp)


class S06WiringAndCycle(SpokenScene):
    def construct(self):
        slab = make_matrix_slab()
        bar = make_switch_bar(active="Rac", y=TOP_BAR_Y)

        cx_t = ValueTracker(-0.95)
        polar_t = ValueTracker(0.0)
        spark_t = ValueTracker(0.0)
        fb_t = ValueTracker(0.0)
        push2_t = ValueTracker(0.0)
        pull_t = ValueTracker(0.0)

        arp_segs = [
            compute_arp23_branches([0.85, 0.20], base_angle=0.14, length=0.72, depth=2, seed=45),
            compute_arp23_branches([0.85, -0.70], base_angle=-0.14, length=0.72, depth=2, seed=46),
        ]

        cell = always_redraw(
            lambda: _wiring_cell_builder(
                cx_t.get_value(), -0.25,
                polar_t.get_value(), spark_t.get_value(),
                fb_t.get_value(), push2_t.get_value(),
                pull_t.get_value(), arp_segs,
            )
        )

        # Labels placed strictly outside the cell's maximum outline and cleanly inside the matrix slab (top = 2.125)
        lbl_fak = T("FAK · Src", 28, FAK_CY).move_to([4.95, 1.82, 0]).set_z_index(12)
        lbl_gef = T("GEF → Rac", 28, RAC).move_to([4.95, 1.24, 0]).set_z_index(12)

        step1 = boxed_label("1 Push", RAC, size=28, box=(2.2, 0.56)).move_to([-3.6, BOTTOM_Y_BAND, 0]).set_z_index(12)
        step2 = boxed_label("2 Grip", ALPHA, size=28, box=(2.2, 0.56)).move_to([0.0, BOTTOM_Y_BAND, 0]).set_z_index(12)
        step3 = boxed_label("3 Pull", RHO, size=28, box=(2.2, 0.56)).move_to([3.6, BOTTOM_Y_BAND, 0]).set_z_index(12)
        arr12 = Arrow([-2.35, BOTTOM_Y_BAND, 0], [-1.25, BOTTOM_Y_BAND, 0], color=TEXT, stroke_width=3.0, buff=0).set_z_index(12)
        arr23 = Arrow([1.25, BOTTOM_Y_BAND, 0], [2.35, BOTTOM_Y_BAND, 0], color=TEXT, stroke_width=3.0, buff=0).set_z_index(12)

        self.add(slab, bar, cell)
        self.play(polar_t.animate.set_value(0.65), run_time=3.5, rate_func=linear)

        self.at("focal adhesion kinase and src")
        self.play(spark_t.animate.set_value(1.0), polar_t.animate.set_value(0.85), FadeIn(lbl_fak, shift=LEFT * 0.1), run_time=2.2, rate_func=linear)

        self.at("recruit exchange factors")
        self.play(fb_t.animate.set_value(1.0), polar_t.animate.set_value(1.0), FadeIn(lbl_gef, shift=LEFT * 0.1), run_time=2.4, rate_func=linear)

        self.at("a fresh grip at the front")
        self.play(push2_t.animate.set_value(0.55), cx_t.animate.set_value(-0.78), run_time=1.8, rate_func=linear)

        self.at("calls for more pushing")
        self.play(push2_t.animate.set_value(1.0), cx_t.animate.set_value(-0.62), run_time=2.2, rate_func=linear)

        self.at("put the steps in order")
        self.play(
            FadeOut(lbl_fak),
            FadeOut(lbl_gef),
            fb_t.animate.set_value(0.0),
            spark_t.animate.set_value(0.0),
            run_time=0.45,
        )

        self.at("push with")
        self.play(FadeIn(step1, shift=UP * 0.1), run_time=0.6)

        self.at("grip with integrins")
        self.play(GrowArrow(arr12), FadeIn(step2, shift=UP * 0.1), run_time=0.6)

        self.at("pull with")
        new_bar = make_switch_bar(active="Rho", y=TOP_BAR_Y)
        self.play(
            GrowArrow(arr23),
            FadeIn(step3, shift=UP * 0.1),
            FadeTransform(bar, new_bar),
            pull_t.animate.set_value(0.35),
            cx_t.animate.set_value(-0.56),
            run_time=0.35,
        )
        bar = new_bar
        self.play(
            pull_t.animate.set_value(1.0),
            cx_t.animate.set_value(-0.45),
            run_time=max(1.1, self.narration_s - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


def build_locked_cell(strain_t=0.0, quiver_phase=0.0, lock_op=1.0, cy=-0.30):
    """Shared world builder for S07Predict end state and S08Pause backdrop."""
    cx = -0.35
    pinch = 0.14 * strain_t + 0.07 * strain_t * np.sin(quiver_phase)
    tail_tug = 0.12 * strain_t * (0.5 + 0.5 * np.sin(quiver_phase))
    cell = make_polar_cell(cx, cy, body_rx=2.15, body_ry=1.60 - pinch, lam_ext=1.55, lam_spread=1.85, tail_pull=tail_tug)
    sheet = make_lam_sheet(cx, cy, body_rx=2.15, lam_ext=1.55, lam_spread=1.85, opacity=0.18)

    front_pts = [[cx + 2.25, cy + 0.85, 0], [cx + 2.55, cy, 0], [cx + 2.25, cy - 0.85, 0]]
    rear_pts = [[cx - 1.65, cy + 0.85, 0], [cx - 1.85, cy, 0], [cx - 1.65, cy - 0.85, 0]]
    adhs = VGroup(*[make_adhesion_pair(p, scale=1.1) for p in front_pts + rear_pts])

    clamps = VGroup()
    if lock_op > 0.02:
        for p in front_pts + rear_pts:
            clamps.add(make_gold_clamp(p, scale=1.0, opacity=lock_op))

    fibres = make_stress_fibres(
        rear_pts,
        front_pts,
        tension=0.35 + 0.65 * strain_t,
        quiver_amp=0.11 * strain_t,
        quiver_phase=quiver_phase,
        show_myosin=True,
    )
    return VGroup(cell, sheet, adhs, fibres, clamps)


class S07Predict(SpokenScene):
    QUESTION = "Front and back adhesions stay locked. What happens when Rho pulls?"

    def construct(self):
        slab = make_matrix_slab()
        lock_t = ValueTracker(0.0)
        strain_t = ValueTracker(0.0)
        q_phase = ValueTracker(0.0)

        cell = always_redraw(lambda: build_locked_cell(strain_t.get_value(), q_phase.get_value(), lock_t.get_value()))
        q_card = question_card(self.QUESTION, y=3.12, max_w=11.8)
        q_card.set_z_index(12)

        lbl_locked = T("adhesions locked", 28, GOLD).move_to([0.0, BOTTOM_Y_BAND, 0]).set_z_index(12)

        self.add(slab, cell)
        self.play(strain_t.animate.set_value(0.35), q_phase.animate.set_value(3.0), run_time=2.4, rate_func=linear)

        self.at("locks its integrins tightly")
        self.play(lock_t.animate.set_value(1.0), FadeIn(lbl_locked, shift=UP * 0.1), strain_t.animate.set_value(0.55), q_phase.animate.set_value(8.0), run_time=1.8, rate_func=linear)

        self.at("none of its old adhesions")
        self.play(strain_t.animate.set_value(0.75), q_phase.animate.set_value(18.0), run_time=3.2, rate_func=linear)

        self.at("contract the cell body")
        self.play(strain_t.animate.set_value(1.0), q_phase.animate.set_value(24.0), run_time=1.3, rate_func=linear)

        self.at("what happens")
        self.play(FadeOut(lbl_locked, run_time=0.25), FadeIn(q_card.question, shift=DOWN * 0.1), run_time=0.6)
        self.play(q_phase.animate.set_value(24.0), run_time=max(0.4, self.narration_s - self.elapsed()), rate_func=linear)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Front and back adhesions stay locked. What happens when Rho pulls?"
    CARD = {"y": 3.12, "max_w": 11.8}
    RING_AT = (6.0, -3.18, 0)
    SECONDS = 4.5

    def backdrop(self):
        slab = make_matrix_slab()
        t_phase = ValueTracker(0.0)
        t_phase.add_updater(lambda m, dt: m.increment_value(10.0 * dt))
        self.add(t_phase)
        cell = always_redraw(lambda: build_locked_cell(1.0, t_phase.get_value(), 1.0))
        return VGroup(slab, cell)


def _release_cell_builder(stride_t, rear_op, front_rho_op, rho_pulse=0.0):
    """Cell releasing rear adhesions, shortening stress fibres, and gliding rightward."""
    cx = -0.35 + 1.85 * stride_t
    cy = -0.30
    tail_pull = 0.65 * stride_t * (1.0 - 0.55 * stride_t)
    cell = make_polar_cell(cx, cy, body_rx=2.15, body_ry=1.60, lam_ext=1.55, lam_spread=1.85, tail_pull=tail_pull)
    sheet = make_lam_sheet(cx, cy, body_rx=2.15, lam_ext=1.55, lam_spread=1.85, opacity=0.20)

    front_pts = [[cx + 2.25, cy + 0.85, 0], [cx + 2.55, cy, 0], [cx + 2.25, cy - 0.85, 0]]
    old_rear = [[-0.35 - 1.65, cy + 0.85, 0], [-0.35 - 1.85, cy, 0], [-0.35 - 1.65, cy - 0.85, 0]]
    cur_rear = [[cx - 1.65 + tail_pull, cy + 0.85, 0], [cx - 1.85 + tail_pull, cy, 0], [cx - 1.65 + tail_pull, cy - 0.85, 0]]

    adhs = VGroup()
    for p in front_pts:
        adhs.add(make_adhesion_pair(p, scale=1.1))
    if rear_op > 0.03:
        for p in old_rear:
            adhs.add(make_adhesion_pair(p, scale=1.0, glow=rear_op))

    clamps = VGroup()
    if rear_op > 0.03:
        for p in old_rear:
            clamps.add(make_gold_clamp(p, scale=1.0, opacity=rear_op))
    front_lock_op = float(np.clip(1.0 - stride_t * 3.0, 0.0, 1.0))
    if front_lock_op > 0.03:
        for p in front_pts:
            clamps.add(make_gold_clamp(p, scale=1.0, opacity=front_lock_op))

    fibres = make_stress_fibres(cur_rear, front_pts, tension=0.6 + 0.4 * (1.0 - stride_t), show_myosin=True)

    front_rho = VGroup()
    if front_rho_op > 0.03:
        sw = 7.0 + 3.5 * np.sin(rho_pulse)
        arc = ArcBetweenPoints(
            [cx + 3.25, cy + 0.95, 0],
            [cx + 3.25, cy - 0.95, 0],
            angle=-0.95,
            color=RHO,
            stroke_width=sw,
        ).set_fill(opacity=0.0).set_stroke(opacity=0.90 * front_rho_op)
        front_rho.add(arc)
    front_rho.set_z_index(5)

    return VGroup(cell, sheet, adhs, fibres, clamps, front_rho)


class S09Release(SpokenScene):
    def construct(self):
        slab = make_matrix_slab()
        q_card = question_card(S07Predict.QUESTION, y=3.12, max_w=11.8).set_z_index(12)
        strain_phase = ValueTracker(0.0)
        locked = always_redraw(lambda: build_locked_cell(1.0, strain_phase.get_value(), 1.0))

        lbl_stall = T("stalls in place", 30, RHO).move_to([0.0, BOTTOM_Y_BAND, 0]).set_z_index(12)

        self.add(slab, locked, q_card)
        self.play(FadeOut(q_card.question, run_time=0.35), FadeIn(lbl_stall, shift=UP * 0.1), strain_phase.animate.set_value(8.0), run_time=1.8, rate_func=linear)

        stride_t = ValueTracker(0.0)
        rear_op = ValueTracker(1.0)
        front_rho_op = ValueTracker(0.0)
        rho_pulse = ValueTracker(0.0)
        live_cell = always_redraw(
            lambda: _release_cell_builder(stride_t.get_value(), rear_op.get_value(), front_rho_op.get_value(), rho_pulse.get_value())
        )

        self.at("old adhesions at the back")
        self.play(FadeOut(lbl_stall, run_time=0.25))
        self.remove(locked)
        self.add(live_cell)
        step4 = boxed_label("4 Let go", GOLD, size=28, box=(2.2, 0.56)).move_to([4.4, BOTTOM_Y_BAND, 0]).set_z_index(12)
        self.play(rear_op.animate.set_value(0.0), FadeIn(step4, shift=UP * 0.1), run_time=1.8)

        self.at("the tail draws in")
        self.play(stride_t.animate.set_value(0.55), run_time=2.0)

        self.at("push grip pull let go")
        s1 = boxed_label("1 Push", RAC, size=26, box=(1.85, 0.52)).move_to([-4.6, BOTTOM_Y_BAND, 0]).set_z_index(12)
        s2 = boxed_label("2 Grip", ALPHA, size=26, box=(1.85, 0.52)).move_to([-1.6, BOTTOM_Y_BAND, 0]).set_z_index(12)
        s3 = boxed_label("3 Pull", RHO, size=26, box=(1.85, 0.52)).move_to([1.4, BOTTOM_Y_BAND, 0]).set_z_index(12)
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(s3), stride_t.animate.set_value(0.85), run_time=2.8, rate_func=linear)

        self.at("in front and")
        bar = make_switch_bar(active="ALL", state_suffix=False, y=TOP_BAR_Y)
        self.play(FadeIn(bar), stride_t.animate.set_value(1.0), run_time=1.8, rate_func=linear)

        self.at("sensors of")
        self.play(front_rho_op.animate.set_value(1.0), rho_pulse.animate.set_value(PI), run_time=1.6, rate_func=linear)

        self.at("find some at the front too")
        lbl_front_rho = T("Rho also active at front", 28, RHO).move_to([3.5, 2.52, 0]).set_z_index(12)
        self.play(FadeIn(lbl_front_rho, shift=DOWN * 0.1), run_time=0.45)
        self.play(rho_pulse.animate.set_value(3.0 * PI), run_time=max(0.5, self.narration_s - self.elapsed()), rate_func=linear)
        self.finish()


def _closing_cell_builder(walk_t, stall_t, arp_segs):
    """Harmonised crawling stride with Rac sheet, Cdc42 fingers, dynamic adhesions, and Rho cables."""
    cx = -2.05 + 2.85 * walk_t
    cy = -0.25
    active_alpha = 1.0 - 0.72 * stall_t
    tail_pull = 0.28 * np.sin(walk_t * PI)

    cell = make_polar_cell(cx, cy, body_rx=2.0, body_ry=1.55, lam_ext=1.45, lam_spread=1.78, tail_pull=tail_pull)
    sheet = make_lam_sheet(cx, cy, body_rx=2.0, lam_ext=1.45, lam_spread=1.78, opacity=0.22 * active_alpha)

    filos = VGroup()
    for i, ang0 in enumerate((-0.42, -0.15, 0.15, 0.42)):
        ang = ang0 + 0.10 * np.sin(walk_t * 3 * TAU + i) * (1.0 - stall_t)
        base = np.array([cx + 3.15 * np.cos(ang0 * 0.65), cy + 1.35 * np.sin(ang0 * 1.1), 0.0])
        tip = base + 1.05 * np.array([np.cos(ang), np.sin(ang), 0.0])
        filos.add(Line(base, tip, color=CDC42, stroke_width=6.0).set_opacity(0.65 * active_alpha))
        filos.add(Line(base, tip, color=ACTIN, stroke_width=2.4))

    front_pts = [[cx + 2.0, cy + 0.82, 0], [cx + 2.25, cy, 0], [cx + 2.0, cy - 0.82, 0]]
    rear_pts = [[cx - 1.45 + tail_pull, cy + 0.82, 0], [cx - 1.65 + tail_pull, cy, 0], [cx - 1.45 + tail_pull, cy - 0.82, 0]]
    adhs = VGroup()
    for p in front_pts:
        adhs.add(make_adhesion_pair(p, scale=1.05, glow=active_alpha))
    for p in rear_pts:
        adhs.add(make_adhesion_pair(p, scale=0.85, glow=max(0.15, 0.85 * (1.0 - 0.6 * walk_t) * active_alpha)))

    tree = VGroup()
    for seg_list in arp_segs:
        shifted = [(p0 + RIGHT * (cx + 2.05), p1 + RIGHT * (cx + 2.05), t0, t1, gen) for p0, p1, t0, t1, gen in seg_list]
        tree.add(draw_arp23_tree(shifted, 1.0, stroke_w=2.6))

    fibres = make_stress_fibres(rear_pts, front_pts, tension=0.65 + 0.35 * np.sin(walk_t * PI), show_myosin=True)
    _fade_stress_fibres(fibres, 0.35 + 0.65 * active_alpha)

    return VGroup(cell, sheet, adhs, tree, filos, fibres)


class S10Closing(SpokenScene):
    def construct(self):
        slab = make_matrix_slab()
        bar = make_switch_bar(active="ALL", state_suffix=False, y=TOP_BAR_Y)

        walk_t = ValueTracker(0.0)
        stall_t = ValueTracker(0.0)

        arp_segs = [
            compute_arp23_branches([-1.05, 0.25], base_angle=0.22, length=0.85, depth=2, seed=47),
            compute_arp23_branches([-1.05, -0.75], base_angle=-0.22, length=0.85, depth=2, seed=48),
        ]

        cell = always_redraw(lambda: _closing_cell_builder(walk_t.get_value(), stall_t.get_value(), arp_segs))
        state_lbl = always_redraw(
            lambda: T(
                "crawling stalled" if stall_t.get_value() > 0.5 else "push · grip · pull · let go",
                28,
                RHO if stall_t.get_value() > 0.5 else TEXT,
            )
            .move_to([0.0, BOTTOM_Y_BAND, 0])
            .set_z_index(12)
        )

        self.add(slab, bar, cell, state_lbl)

        self.at("shape actin to turn grip")
        self.play(walk_t.animate.set_value(0.35), run_time=2.8, rate_func=linear)

        self.at("pushes broad sheets")
        self.play(Transform(bar, make_switch_bar(active="Rac", state_suffix=False, y=TOP_BAR_Y)), run_time=0.4)
        self.play(walk_t.animate.set_value(0.58), run_time=1.8, rate_func=linear)

        self.at("probes with fingers")
        self.play(Transform(bar, make_switch_bar(active="Cdc42", state_suffix=False, y=TOP_BAR_Y)), run_time=0.4)
        self.play(walk_t.animate.set_value(0.78), run_time=1.6, rate_func=linear)

        self.at("contracts cables against adhesions")
        self.play(Transform(bar, make_switch_bar(active="Rho", state_suffix=False, y=TOP_BAR_Y)), run_time=0.4)
        self.play(walk_t.animate.set_value(1.0), run_time=2.2, rate_func=linear)

        self.at("break the grip or the switches")
        self.play(Transform(bar, make_switch_bar(active=None, state_suffix=False, y=TOP_BAR_Y)), stall_t.animate.set_value(1.0), run_time=1.5)

        self.at("this kind of crawling stalls")
        self.finish()


class S11End(EndCard):
    LINE = "Rho, Rac and Cdc42 shape actin to turn grip into crawling."
