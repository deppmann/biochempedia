"""
===============================================================================
PLAN — "Many Mutations, One Weak Point" (oncogenes__chapter-2)
===============================================================================

COLOUR MAP (one colour per concept, high-contrast on BG = #0f1117):
- Stuck ON growth switch / oncogene signal : ONCO_AMBER   = "#F59E0B"
- Checkpoint / p53 / alarm / death signal  : CHECK_CORAL  = "#F43F5E"
- Survival signal                          : SURV_EMERALD = "#10B981"
- Targeted drug / blocker                  : DRUG_CYAN    = "#38BDF8"
- Parallel backup route                    : BACKUP_BLUE  = "#60A5FA"
- Lost off-switch / tumour suppressor loss : LOSS_CRIMSON = "#EF4444" (with SLATE_LINE = "#94A3B8" dashed shell)
- Schematic cell structure & primary text  : TEXT (#E8EAF0), CELL_MEMBRANE = "#CBD5E1", CELL_FILL = "#1E2B45", NUCLEUS_FILL = "#283A5E"

THE ONE CARRIED WORLD:
A schematic cell (membrane ring, central nucleus with 2-copy chromosome bar,
an amber membrane growth switch sending pulses inward along a signaling track,
and a coral-red checkpoint gate guarding the exit toward cell division) that
zooms out from the stuck switch in s01, clamps division at the checkpoint in
s02-s03, accumulates four cooperating faults to divide into a non-overlapping
tumour cluster in s04, is challenged by a targeted cyan drug in s05-s06,
collapses in s07, has its two competing mechanisms dissected in s08, and
returns as a three-stage cell-to-tumour-to-collapse arc in s09.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook: Amber signal pulses stream continuously along the switch track
  (position u(t) = (phase + i/N) % 1 from a linear ValueTracker), while a
  smooth zoom-out transformation shrinks the close-up switch + 2-copy gene
  rack into the whole schematic cell at its carried position.
- s02_alarm: A computed signal-intensity trace rises from a brief normal pulse
  to a sustained nonstop amber beam along the track, triggering computed
  expanding coral-red warning rings (r(t) = r0 + ((t+k) % 1) * dr) and driving
  a gate-closure ValueTracker (1 -> 0) that clamps the division arrow shut.
- s03_checkpoints: The checkpoint barrier opens to reveal p53; a rotating
  cell-cycle ring (angle from ValueTracker) locks dead still for Arrest, while
  a duplicate cell breaks into 8 radially separating fragments (computed from
  polar angle + progress tracker) for Apoptosis, and a live emerald survival
  pulse stream flows into a cell that slips past.
- s04_multistep: Four cooperating fault badges lock onto the carried cell in
  sequence while nonstop signal waves pulse from switch to checkpoint; once all
  four are present, a growth ValueTracker spawns and expands 1 -> 13
  non-overlapping tumour cells along a relaxed Vogel-spiral cluster seeded
  with np.random.default_rng(7).
- s05_addiction_predict: On the carried pulsing tumour cluster (membrane pulse
  amplitude driven by switch power tracker), each named fault badge highlights
  in sync, then a cyan Targeted drug wedge glides into the amber switch;
  switch-power drops 1 -> 0, stopping pulses and pulsing while leaving all
  other mutation badges intact.
- s07_reveal_addiction: A continuous contraction ValueTracker (0 -> 1) shrinks
  the cluster radially and fades outer cells layer-by-layer by their computed
  distance r_i from cluster center across the scene while the silenced switch
  stays attached to the core cell and the untouched mutation badges stay clear.
- s08_debated_mechanisms: Left panel drives a feedback-brake bar tracker
  (0.15 -> 0.90) that proportionally dims/suppresses the parallel backup route
  signal; right panel plots two live computed exponential decay curves
  S(t) = exp(-t/2.0) and D(t) = exp(-t/7.5) via Plot.live_curve and drives a
  balance beam angle proportional to D(t) - S(t) from the same time tracker.
- s09_closing: Builds the 3-stage arc left-to-right: Stage 1 pulses hit the p53
  brake; Stage 2 expands a multi-fault cell cluster via a growth tracker; Stage 3
  glides in the cyan blocker and contracts the cluster via a collapse tracker.
===============================================================================
"""

from bp_parts import *

# ---------------------------------------------------------------------------
# Film Colour Map
# ---------------------------------------------------------------------------
ONCO_AMBER = "#F59E0B"
CHECK_CORAL = "#F43F5E"
SURV_EMERALD = "#10B981"
DRUG_CYAN = "#38BDF8"
BACKUP_BLUE = "#60A5FA"
LOSS_CRIMSON = "#EF4444"
SLATE_LINE = "#94A3B8"
CELL_MEMBRANE = "#CBD5E1"
CELL_FILL = "#1E2B45"
NUCLEUS_FILL = "#283A5E"

# Standard carried cell geometry (leaves right side clear for division / branches)
CELL_C = np.array([-1.95, -0.05, 0.0])
CELL_R = 2.52
NUC_R = 0.92
SW_ANGLE = 3 * PI / 4
SW_POS = CELL_C + CELL_R * np.array([np.cos(SW_ANGLE), np.sin(SW_ANGLE), 0.0])
GATE_POS = CELL_C + RIGHT * CELL_R
# Tumour cluster center & scale for s04 (end), s05, s06, s07 (clear of top question & right badges)
CLUSTER_C = np.array([-0.80, -0.35, 0.0])
CLUSTER_S = 0.88


# ---------------------------------------------------------------------------
# Computed Geometry & Simulation Helpers
# ---------------------------------------------------------------------------
def cluster_layout(n=13, seed=7):
    """Deterministic packed non-overlapping tumour-cluster cell offsets and radii."""
    rng = np.random.default_rng(seed)
    coords = [(0.0, 0.0, 0.50)]
    golden = PI * (3 - np.sqrt(5))
    for k in range(1, n):
        r = 0.95 * np.sqrt(k) + rng.uniform(-0.02, 0.02)
        ang = (5 * PI / 4 if k == 1 else k * golden) + rng.uniform(-0.08, 0.08)
        rad = rng.uniform(0.39, 0.45)
        coords.append([r * np.cos(ang), r * np.sin(ang), rad])
    pts = [list(coords[0])] + coords[1:]
    for _ in range(40):
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                d = np.hypot(dx, dy) + 1e-6
                min_d = pts[i][2] + pts[j][2] + 0.14
                if d < min_d:
                    push = (min_d - d) * 0.52
                    ux, uy = dx / d, dy / d
                    if i > 0:
                        pts[i][0] -= ux * push
                        pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
    return [(x, y, r) for x, y, r in pts]


def make_switch_icon(pos, scale=1.0, active=True, angle=0.0):
    """Membrane growth switch with an active receptor pocket."""
    col = ONCO_AMBER if active else SLATE_LINE
    base = RoundedRectangle(
        corner_radius=0.10 * scale,
        width=0.58 * scale,
        height=0.82 * scale,
        stroke_color=col,
        stroke_width=3.5,
        fill_color=col,
        fill_opacity=0.28 if active else 0.12,
    )
    notch = Polygon(
        [-0.22 * scale, 0.42 * scale, 0],
        [-0.08 * scale, 0.08 * scale, 0],
        [0.08 * scale, 0.08 * scale, 0],
        [0.22 * scale, 0.42 * scale, 0],
        [0.34 * scale, 0.42 * scale, 0],
        [0.14 * scale, -0.04 * scale, 0],
        [-0.14 * scale, -0.04 * scale, 0],
        [-0.34 * scale, 0.42 * scale, 0],
        stroke_color=col,
        stroke_width=2.5,
        fill_color=col,
        fill_opacity=0.55 if active else 0.20,
    )
    core = Dot(radius=0.14 * scale, color=col).shift(DOWN * 0.16 * scale)
    g = VGroup(base, notch, core)
    g.rotate(angle)
    g.move_to(pos)
    return g


def make_drug_wedge(scale=1.0, angle=0.0):
    """Crisp cyan wedge that docks cleanly into the growth switch pocket."""
    wedge = Polygon(
        [-0.26 * scale, 0.34 * scale, 0],
        [0.26 * scale, 0.34 * scale, 0],
        [0.11 * scale, -0.14 * scale, 0],
        [-0.11 * scale, -0.14 * scale, 0],
        stroke_color=DRUG_CYAN,
        stroke_width=3.0,
        fill_color=DRUG_CYAN,
        fill_opacity=0.92,
    )
    wedge.rotate(angle)
    return wedge


def make_gene_rack(center, scale=1.0, altered=True):
    """Two-copy chromosome rack inside nucleus: 1 normal copy, 1 altered copy."""
    c1 = RoundedRectangle(
        corner_radius=0.06 * scale, width=0.95 * scale, height=0.22 * scale,
        stroke_color=CELL_MEMBRANE, stroke_width=2.5, fill_color=CELL_MEMBRANE, fill_opacity=0.25,
    )
    c2_col = ONCO_AMBER if altered else CELL_MEMBRANE
    c2 = RoundedRectangle(
        corner_radius=0.06 * scale, width=0.95 * scale, height=0.22 * scale,
        stroke_color=c2_col, stroke_width=3.0, fill_color=c2_col, fill_opacity=0.38 if altered else 0.25,
    )
    return VGroup(c1, c2).arrange(DOWN, buff=0.12 * scale).move_to(center)


def make_checkpoint_barrier(pos, height=1.2, closed=True):
    """Coral-red checkpoint barrier gate standing across the division track."""
    col = CHECK_CORAL
    top_post = Dot(pos + UP * (height * 0.55), radius=0.09, color=col)
    bot_post = Dot(pos + DOWN * (height * 0.55), radius=0.09, color=col)
    if closed:
        bar = Line(pos + UP * (height * 0.52), pos + DOWN * (height * 0.52), color=col, stroke_width=8)
    else:
        bar = Line(
            pos + UP * (height * 0.52),
            pos + UP * (height * 0.52) + LEFT * 0.65 + UP * 0.25,
            color=col, stroke_width=8,
        )
    return VGroup(top_post, bot_post, bar)


def make_carried_cell(center=CELL_C, radius=CELL_R, nuc_r=NUC_R, show_rack=True):
    """Standard schematic cell carried across s01-s04."""
    membrane = Circle(
        radius=radius, stroke_color=CELL_MEMBRANE, stroke_width=4.5,
        fill_color=CELL_FILL, fill_opacity=0.95,
    ).move_to(center)
    nucleus = Circle(
        radius=nuc_r, stroke_color=BACKUP_BLUE, stroke_width=3.0,
        fill_color=NUCLEUS_FILL, fill_opacity=0.96,
    ).move_to(center)
    sw_pos = center + radius * np.array([np.cos(SW_ANGLE), np.sin(SW_ANGLE), 0.0])
    switch = make_switch_icon(sw_pos, scale=0.85, active=True, angle=PI / 4)
    track_pts = [
        sw_pos + np.array([0.28, -0.28, 0.0]),
        center + np.array([-0.55, 0.55, 0.0]),
        center + np.array([0.0, 0.0, 0.0]),
        center + RIGHT * (radius - 0.16),
    ]
    track = VMobject(stroke_color=SLATE_LINE, stroke_width=3.5, stroke_opacity=0.75)
    track.set_points_as_corners(track_pts)
    rack = make_gene_rack(center, scale=0.95, altered=True) if show_rack else VGroup()
    g = VGroup(membrane, nucleus, track, rack, switch)
    g.membrane = membrane
    g.nucleus = nucleus
    g.track = track
    g.track_pts = track_pts
    g.rack = rack
    g.switch = switch
    g.sw_pos = sw_pos
    g.gate_pos = center + RIGHT * radius
    return g


def signal_stream(track_pts, phase_tracker, power_tracker=None, n_pulses=6, color=ONCO_AMBER, radius=0.14):
    """Computed pulse dots moving along track_pts driven by phase_tracker (0..1 loop)."""
    pts = [np.array(p, dtype=float) for p in track_pts]
    segs = [pts[i + 1] - pts[i] for i in range(len(pts) - 1)]
    lens = [float(np.linalg.norm(s)) for s in segs]
    tot = sum(lens)

    def eval_pt(u):
        d = (u % 1.0) * tot
        for s, ln, p0 in zip(segs, lens, pts[:-1]):
            if d <= ln + 1e-9:
                return p0 + s * (d / max(ln, 1e-6))
            d -= ln
        return pts[-1]

    def mk():
        pwr = power_tracker.get_value() if power_tracker is not None else 1.0
        if pwr <= 0.03:
            return VGroup()
        ph = phase_tracker.get_value()
        dots = VGroup()
        for k in range(n_pulses):
            u = (ph + k / n_pulses) % 1.0
            pos = eval_pt(u)
            d = Dot(pos, radius=radius * (0.65 + 0.35 * pwr), color=color)
            d.set_opacity(min(1.0, pwr))
            dots.add(d)
        return dots

    return always_redraw(mk)


def fault_badge(kind, width=3.15):
    """Crisp schematic fault badge (full-opacity bright colours, never grey text)."""
    if kind == "on":
        icon = Dot(radius=0.11, color=ONCO_AMBER)
        txt = T("Stuck on-switch", size=24, color=ONCO_AMBER)
        col, dashed = ONCO_AMBER, False
    elif kind == "switched_off":
        icon = Dot(radius=0.11, color=DRUG_CYAN)
        txt = T("Switch blocked", size=24, color=DRUG_CYAN)
        col, dashed = DRUG_CYAN, False
    elif kind == "off":
        c = Circle(radius=0.12, stroke_color=SLATE_LINE, stroke_width=2.5)
        x1 = Line([-0.09, -0.09, 0], [0.09, 0.09, 0], color=LOSS_CRIMSON, stroke_width=3.5)
        x2 = Line([-0.09, 0.09, 0], [0.09, -0.09, 0], color=LOSS_CRIMSON, stroke_width=3.5)
        icon = VGroup(c, x1, x2)
        txt = T("Lost off-switch", size=24, color=LOSS_CRIMSON)
        col, dashed = LOSS_CRIMSON, True
    elif kind == "p53":
        sh = Polygon(
            [-0.11, 0.11, 0], [0.11, 0.11, 0], [0.11, -0.03, 0], [0, -0.14, 0], [-0.11, -0.03, 0],
            stroke_color=CHECK_CORAL, stroke_width=2.8, fill_color=CHECK_CORAL, fill_opacity=0.25,
        )
        crack = Line([-0.06, 0.12, 0], [0.06, -0.12, 0], color=TEXT, stroke_width=2.5)
        icon = VGroup(sh, crack)
        txt = T("p53 lost", size=24, color=CHECK_CORAL)
        col, dashed = CHECK_CORAL, False
    else:  # death blocked
        bar = Line([-0.12, 0, 0], [0.12, 0, 0], color=CHECK_CORAL, stroke_width=4)
        ring = Circle(radius=0.12, stroke_color=CHECK_CORAL, stroke_width=2.5)
        icon = VGroup(ring, bar)
        txt = T("Death blocked", size=24, color=CHECK_CORAL)
        col, dashed = CHECK_CORAL, False

    inner = VGroup(icon, txt).arrange(RIGHT, buff=0.14)
    h = max(0.56, inner.height + 0.22)
    w = max(width, inner.width + 0.34)
    base_rect = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        stroke_color=SLATE_LINE if dashed else col, stroke_width=2.5,
        fill_color=CELL_FILL, fill_opacity=0.95,
    )
    rect = DashedVMobject(base_rect, num_dashes=26, dashed_ratio=0.55) if dashed else base_rect
    inner.move_to(base_rect)
    g = VGroup(rect, inner)
    g.box = base_rect
    return g


UL_UNIT = np.array([-1.0, 1.0, 0.0]) / np.sqrt(2.0)


def cluster_switch_pos(center, scale, shrink):
    """Switch anchor stays docked directly onto the upper-left membrane of the core cell."""
    core_r = 0.50 * scale * max(0.58, 1.0 - 0.42 * shrink)
    return center + (core_r + 0.40 * scale) * UL_UNIT


def build_tumour_cluster(center=CLUSTER_C, scale=CLUSTER_S, active_switch=True, shrink=0.0, pulse_phase=None):
    """Non-overlapping multi-cell tumour cluster (seed=7) with contraction shrink and optional growth pulse."""
    layout = cluster_layout(13, seed=7)
    max_r = max(np.hypot(x, y) for x, y, _ in layout) + 1e-6
    cells = VGroup()
    for idx, (ox, oy, rad) in enumerate(layout):
        dist_frac = np.hypot(ox, oy) / max_r
        if idx == 0:
            cell_scale = max(0.58, 1.0 - 0.42 * shrink)
            op = max(0.55, 1.0 - 0.40 * shrink)
        else:
            fade_start = max(0.0, (1.0 - dist_frac) * 0.55)
            local = np.clip((shrink - fade_start) / 0.40, 0.0, 1.0)
            cell_scale = max(0.05, 1.0 - local)
            op = max(0.0, 1.0 - local)
        if op <= 0.04:
            continue
        pulse_mul = 1.0 + (0.09 * np.sin(pulse_phase * TAU + idx * 0.6) if (pulse_phase is not None and active_switch) else 0.0)
        pos = center + np.array([ox, oy, 0.0]) * scale * (1.0 - 0.42 * shrink)
        r_now = rad * scale * cell_scale * pulse_mul
        mem_col = ONCO_AMBER if (active_switch and idx == 0) else CELL_MEMBRANE
        c = Circle(
            radius=r_now,
            stroke_color=mem_col,
            stroke_width=3.2 if idx == 0 else 2.3,
            fill_color=CELL_FILL,
            fill_opacity=0.95 * op,
        ).set_stroke(opacity=op).move_to(pos)
        nuc = Circle(
            radius=r_now * 0.44,
            stroke_color=BACKUP_BLUE,
            stroke_width=1.8,
            fill_color=NUCLEUS_FILL,
            fill_opacity=0.94 * op,
        ).set_stroke(opacity=op).move_to(pos)
        d1 = Dot(pos + UL * (r_now * 0.25), radius=0.055 * scale * cell_scale, color=ONCO_AMBER if active_switch else SLATE_LINE).set_opacity(op)
        d2 = Dot(pos + UR * (r_now * 0.25), radius=0.055 * scale * cell_scale, color=LOSS_CRIMSON).set_opacity(op)
        d3 = Dot(pos + DOWN * (r_now * 0.26), radius=0.055 * scale * cell_scale, color=CHECK_CORAL).set_opacity(op)
        cells.add(VGroup(c, nuc, d1, d2, d3))

    sw_anchor = cluster_switch_pos(center, scale, shrink)
    sw = make_switch_icon(sw_anchor, scale=1.05 * scale, active=active_switch, angle=PI / 4)
    g = VGroup(cells, sw)
    g.cells = cells
    g.switch = sw
    g.sw_anchor = sw_anchor
    return g


def build_drug_on_cluster(cluster, scale=CLUSTER_S):
    """Cyan Targeted drug wedge docked into cluster's amber switch pocket."""
    w = make_drug_wedge(scale=1.05 * scale, angle=PI / 4)
    w.move_to(cluster.sw_anchor + UL * (0.28 * scale))
    return w


def build_s05_end_backdrop(show_badges=True):
    """Exact state shared between end of s05_addiction_predict and s06_pause."""
    cluster = build_tumour_cluster(CLUSTER_C, scale=CLUSTER_S, active_switch=False, shrink=0.0)
    wedge = build_drug_on_cluster(cluster, scale=CLUSTER_S)
    drug_lbl = T("Targeted drug", size=26, color=DRUG_CYAN).move_to([-4.65, 2.25, 0.0])
    drug_arr = Arrow(drug_lbl.get_right() + RIGHT * 0.12, wedge.get_corner(UL) + UL * 0.06, color=DRUG_CYAN, stroke_width=4, buff=0.04)
    g = VGroup(cluster, wedge, drug_lbl, drug_arr)
    if show_badges:
        b1 = fault_badge("switched_off", width=3.15)
        b2 = fault_badge("off", width=3.15)
        b3 = fault_badge("p53", width=3.15)
        b4 = fault_badge("death", width=3.15)
        col = VGroup(b1, b2, b3, b4).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.55, -0.25, 0.0])
        g.add(col)
    return g


# ---------------------------------------------------------------------------
# Scene 00: Title Card
# ---------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Oncogenes: When the Switch Sticks"
    TITLE = "Many Mutations, One Weak Point"


# ---------------------------------------------------------------------------
# Scene 01: Hook — Zoom out from stuck switch & 2-copy rack to whole cell
# ---------------------------------------------------------------------------
class S01Hook(SpokenScene):
    def construct(self):
        # Smooth large cell quadrant clearly clear of right-side puzzle boxes (x >= 1.8)
        zoom_center = np.array([-2.8, -3.6, 0.0])
        zoom_r = 4.65
        zoom_fill = Circle(radius=zoom_r, stroke_width=0, fill_color=CELL_FILL, fill_opacity=0.92).move_to(zoom_center)
        zoom_mem = Circle(radius=zoom_r, stroke_color=CELL_MEMBRANE, stroke_width=6).move_to(zoom_center)
        zoom_sw_pos = zoom_center + zoom_r * np.array([np.cos(PI * 0.34), np.sin(PI * 0.34), 0.0])
        zoom_sw = make_switch_icon(zoom_sw_pos, scale=1.20, active=True, angle=PI / 4)
        zoom_track_pts = [
            zoom_sw_pos + np.array([0.32, -0.42, 0.0]),
            np.array([-1.7, -0.8, 0.0]),
            np.array([0.2, -1.0, 0.0]),
        ]
        zoom_track = VMobject(stroke_color=SLATE_LINE, stroke_width=4).set_points_as_corners(zoom_track_pts)

        rack = make_gene_rack(np.array([-4.0, -1.85, 0.0]), scale=1.20, altered=True)
        rack_lbl1 = T("Normal copy", size=24, color=TEXT).next_to(rack[0], RIGHT, buff=0.25)
        rack_lbl2 = T("Altered copy", size=24, color=ONCO_AMBER).next_to(rack[1], RIGHT, buff=0.25)
        sw_lbl = T("Growth switch: STUCK ON", size=28, color=ONCO_AMBER).move_to([-2.0, 2.35, 0.0])

        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.65))
        self.add(phase)

        pulses = signal_stream(zoom_track_pts, phase, n_pulses=6, color=ONCO_AMBER, radius=0.14)

        self.add(zoom_fill, zoom_mem, zoom_track, zoom_sw, rack, rack_lbl1, rack_lbl2, sw_lbl, pulses)
        self.add(scope_tag("schematic", color=TEXT))

        self.at("one altered gene copy")
        self.play(
            Circumscribe(rack[1], color=ONCO_AMBER, fade_out=True),
            Circumscribe(zoom_sw, color=ONCO_AMBER, fade_out=True),
            run_time=1.2,
        )

        self.at("Why does one stuck switch")
        q1_box = RoundedRectangle(
            corner_radius=0.16, width=4.6, height=1.55,
            stroke_color=CHECK_CORAL, stroke_width=3.5, fill_color=CELL_FILL, fill_opacity=0.96,
        ).move_to([4.05, 1.45, 0.0])
        q1_t = fit_text("1 stuck switch\n→ rarely a tumour?", max_w=4.2, size=28, color=CHECK_CORAL).move_to(q1_box)
        self.play(FadeIn(q1_box, shift=LEFT * 0.2), FadeIn(q1_t), run_time=0.8)

        self.at("blocking just one switch")
        q2_box = RoundedRectangle(
            corner_radius=0.16, width=4.6, height=1.55,
            stroke_color=DRUG_CYAN, stroke_width=3.5, fill_color=CELL_FILL, fill_opacity=0.96,
        ).move_to([4.05, -0.55, 0.0])
        q2_t = fit_text("Block 1 switch\n→ shrinks many-fault tumour?", max_w=4.2, size=26, color=DRUG_CYAN).move_to(q2_box)
        self.play(FadeIn(q2_box, shift=LEFT * 0.2), FadeIn(q2_t), run_time=0.8)

        self.at("Let us zoom out")
        cell = make_carried_cell()
        cell.membrane.set_z_index(0)
        cell.nucleus.set_z_index(1)
        cell.track.set_z_index(2)
        cell.rack.set_z_index(3)
        rack.set_z_index(3)
        cell.switch.set_z_index(4)
        zoom_sw.set_z_index(4)
        barrier = make_checkpoint_barrier(cell.gate_pos, height=1.35, closed=True)
        barrier.set_z_index(4)
        cell_lbl = T("Whole cell", size=28, color=TEXT).next_to(cell.membrane, UP, buff=0.22).set_z_index(5)
        nuc_lbl = T("Nucleus", size=24, color=BACKUP_BLUE).next_to(cell.nucleus, DOWN, buff=0.18).set_z_index(5)
        nuc_lbl.layout_ok = "covered"
        chk_lbl = T("Checkpoint", size=28, color=CHECK_CORAL).next_to(barrier, RIGHT, buff=0.28).set_z_index(5)
        sw_small_lbl = T("Stuck switch", size=26, color=ONCO_AMBER).next_to(cell.switch, UL, buff=0.18).set_z_index(5)

        self.remove(pulses)
        cell_pulses = signal_stream(cell.track_pts, phase, n_pulses=6, color=ONCO_AMBER, radius=0.13)
        cell_pulses.set_z_index(4)

        self.play(
            FadeOut(q1_box), FadeOut(q1_t), FadeOut(q2_box), FadeOut(q2_t),
            FadeOut(rack_lbl1), FadeOut(rack_lbl2), FadeOut(sw_lbl),
            run_time=0.35,
        )
        self.play(
            FadeOut(zoom_fill), FadeOut(zoom_mem), FadeOut(zoom_track),
            ReplacementTransform(zoom_sw, cell.switch),
            ReplacementTransform(rack, cell.rack),
            FadeIn(cell.membrane), FadeIn(cell.nucleus), FadeIn(cell.track),
            FadeIn(barrier),
            run_time=1.8,
        )
        self.add(cell_pulses)
        self.play(
            FadeIn(cell_lbl), FadeIn(nuc_lbl), FadeIn(chk_lbl), FadeIn(sw_small_lbl),
            run_time=0.7,
        )
        self.finish()


# ---------------------------------------------------------------------------
# Scene 02: Alarm — Brief normal pulse -> nonstop beam -> checkpoint clamps
# ---------------------------------------------------------------------------
class S02Alarm(SpokenScene):
    def construct(self):
        cell = make_carried_cell()
        sw_lbl = T("Growth switch", size=26, color=ONCO_AMBER).next_to(cell.switch, UL, buff=0.18)
        nuc_lbl = T("Nucleus", size=24, color=BACKUP_BLUE).next_to(cell.nucleus, DOWN, buff=0.18)
        nuc_lbl.layout_ok = "covered"

        gate_open = ValueTracker(1.0)
        barrier = always_redraw(lambda: make_checkpoint_barrier(
            cell.gate_pos, height=1.35, closed=gate_open.get_value() < 0.5
        ))

        div_start = cell.gate_pos + RIGHT * 0.35
        div_end = cell.gate_pos + RIGHT * 2.55
        div_arrow = Arrow(div_start, div_end, color=CELL_MEMBRANE, stroke_width=5, buff=0)
        div_cell = Circle(
            radius=0.55, stroke_color=CELL_MEMBRANE, stroke_width=3.5,
            fill_color=CELL_FILL, fill_opacity=0.90,
        ).move_to(div_end + RIGHT * 0.78)
        div_lbl = T("Divide", size=26, color=TEXT).next_to(div_cell, UP, buff=0.18)

        sig_plot = Plot(
            box=(1.8, 5.9, -2.75, -1.10), xr=(0, 10), yr=(0, 1.25),
            xticks=[], yticks=[(0, "0"), (1, "ON")],
            xlabel="time", ylabel="Signal", color=TEXT, size=22, label_size=24,
        )
        t_sig = ValueTracker(0.0)
        sig_fn = lambda x: (0.95 * np.exp(-((x - 1.5) / 0.65) ** 2)) if x < 3.4 else (1.0 - 0.85 * np.exp(-(x - 3.4) * 2.2))
        sig_curve = sig_plot.live_curve(sig_fn, t_sig, color=ONCO_AMBER, width=5)
        sig_dot = sig_plot.dot(lambda: t_sig.get_value(), lambda: sig_fn(t_sig.get_value()), color=ONCO_AMBER, ring=TEXT, radius=0.09)

        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.65))
        pwr = ValueTracker(0.0)
        pulses = signal_stream(cell.track_pts, phase, power_tracker=pwr, n_pulses=6, color=ONCO_AMBER, radius=0.13)

        self.add(phase, cell, sw_lbl, nuc_lbl, barrier, div_arrow, div_cell, div_lbl, sig_plot, sig_curve, sig_dot, pulses)
        self.add(scope_tag("schematic", color=TEXT))

        normal_dot = Dot(cell.track_pts[0], radius=0.14, color=ONCO_AMBER)
        self.play(
            MoveAlongPath(normal_dot, cell.track),
            t_sig.animate.set_value(3.2),
            run_time=1.3, rate_func=linear,
        )
        self.play(FadeOut(normal_dot, run_time=0.25))

        self.at("stuck growth switch")
        stuck_lbl = T("Stuck ON", size=26, color=ONCO_AMBER).next_to(cell.switch, UL, buff=0.18)
        self.play(
            swap(sw_lbl, stuck_lbl, run_time=0.5),
            cell.track.animate.set_stroke(ONCO_AMBER, width=6, opacity=0.9),
            pwr.animate.set_value(1.0),
            t_sig.animate.set_value(5.6),
            run_time=2.5, rate_func=linear,
        )

        self.at("Surprisingly")
        ring_t = ValueTracker(0.0)

        def mk_rings():
            g = VGroup()
            t_val = ring_t.get_value()
            for k in range(3):
                u = (t_val + k / 3.0) % 1.0
                r = 0.25 + u * 1.05
                op = (1.0 - u) * 0.90
                g.add(Circle(radius=r, stroke_color=CHECK_CORAL, stroke_width=4.5).set_stroke(opacity=op).move_to(cell.gate_pos))
            return g

        rings = always_redraw(mk_rings)
        rings.layout_ok = True
        ring_t.add_updater(lambda m, dt: m.increment_value(dt * 0.75))
        self.add(ring_t, rings)

        stop_x = VGroup(
            Line([-0.24, -0.24, 0], [0.24, 0.24, 0], color=CHECK_CORAL, stroke_width=6),
            Line([-0.24, 0.24, 0], [0.24, -0.24, 0], color=CHECK_CORAL, stroke_width=6),
        ).move_to(div_arrow.get_center())
        stopped_lbl = T("Stopped", size=28, color=CHECK_CORAL).next_to(div_cell, UP, buff=0.18)

        self.play(
            gate_open.animate.set_value(0.0),
            Create(stop_x),
            swap(div_lbl, stopped_lbl, run_time=0.5),
            div_cell.animate.set_stroke(CHECK_CORAL, opacity=0.45),
            t_sig.animate.set_value(7.6),
            run_time=2.2, rate_func=linear,
        )

        self.at("A healthy cell")
        fault_tag = boxed_label("Fault alarm!", color=CHECK_CORAL, size=26).move_to([4.15, 2.55, 0.0])
        self.play(FadeIn(fault_tag, shift=DOWN * 0.15), t_sig.animate.set_value(9.0), run_time=2.5, rate_func=linear)

        self.at("called checkpoints")
        chk_lbl = T("Checkpoint (schematic)", size=26, color=CHECK_CORAL).move_to([2.05, 1.65, 0.0])
        chk_leader = Arrow(
            chk_lbl.get_bottom() + DOWN * 0.06 + LEFT * 0.70,
            cell.gate_pos + UP * 0.72,
            color=CHECK_CORAL, stroke_width=3.5, buff=0.04, max_tip_length_to_length_ratio=0.18,
        )
        self.play(FadeIn(chk_lbl, shift=UP * 0.1), GrowArrow(chk_leader), t_sig.animate.set_value(10.0), run_time=1.8, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 03: Checkpoints — p53 badge, Arrest ring, Apoptosis fragments, Survival cue
# ---------------------------------------------------------------------------
class S03Checkpoints(SpokenScene):
    def construct(self):
        cell = make_carried_cell()
        stuck_lbl = T("Stuck ON", size=26, color=ONCO_AMBER).next_to(cell.switch, UL, buff=0.18)
        nuc_lbl = T("Nucleus", size=24, color=BACKUP_BLUE).next_to(cell.nucleus, DOWN, buff=0.18)
        nuc_lbl.layout_ok = "covered"

        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.65))
        pulses = signal_stream(cell.track_pts, phase, n_pulses=6, color=ONCO_AMBER, radius=0.13)
        barrier = make_checkpoint_barrier(cell.gate_pos, height=1.35, closed=True)

        self.add(phase, cell, stuck_lbl, nuc_lbl, barrier, pulses)
        self.add(scope_tag("schematic", color=TEXT))

        self.at("One major guard")
        p53_badge = boxed_label("p53", color=CHECK_CORAL, size=32, box=(1.25, 0.78)).move_to(cell.gate_pos + RIGHT * 0.85)
        self.play(ReplacementTransform(barrier, p53_badge), run_time=0.85)

        self.at("A nonstop growth signal")
        dna_lbl = T("DNA damage", size=24, color=CHECK_CORAL).move_to([p53_badge.get_x(), 2.35, 0.0])
        dna_arr = Arrow(dna_lbl.get_bottom() + DOWN * 0.08, p53_badge.get_top() + UP * 0.08, color=CHECK_CORAL, stroke_width=3.5, buff=0.04)
        ring_c = np.array([3.95, 1.75, 0.0])
        cycle_ring = Circle(radius=0.64, stroke_color=BACKUP_BLUE, stroke_width=5).move_to(ring_c)
        cycle_angle = ValueTracker(0.0)
        cycle_speed = ValueTracker(2.6)
        cycle_angle.add_updater(lambda m, dt: m.increment_value(dt * cycle_speed.get_value()))
        cycle_dot = always_redraw(lambda: Dot(
            ring_c + 0.64 * np.array([np.cos(cycle_angle.get_value()), np.sin(cycle_angle.get_value()), 0.0]),
            radius=0.12, color=TEXT,
        ))
        self.add(cycle_angle, cycle_speed)
        self.play(
            FadeIn(dna_lbl), GrowArrow(dna_arr),
            FadeIn(cycle_ring), FadeIn(cycle_dot),
            Circumscribe(p53_badge, color=CHECK_CORAL, fade_out=True),
            run_time=1.3,
        )

        self.at("It halts cell division")
        arr_top = Arrow(p53_badge.get_right() + RIGHT * 0.1, ring_c + LEFT * 0.84, color=CHECK_CORAL, stroke_width=4, buff=0.05)
        arrest_lbl = T("Arrest", size=28, color=CHECK_CORAL).next_to(cycle_ring, RIGHT, buff=0.28)
        clamp = Line(ring_c + LEFT * 0.42 + UP * 0.42, ring_c + RIGHT * 0.42 + DOWN * 0.42, color=CHECK_CORAL, stroke_width=6)
        self.play(GrowArrow(arr_top), cycle_speed.animate.set_value(0.0), Create(clamp), FadeIn(arrest_lbl), run_time=1.0)

        self.at("or triggers apoptosis")
        apop_c = np.array([3.85, -0.25, 0.0])
        arr_bot = Arrow(p53_badge.get_right() + RIGHT * 0.1, apop_c + LEFT * 0.84, color=CHECK_CORAL, stroke_width=4, buff=0.05)
        frag_t = ValueTracker(0.0)
        rng = np.random.default_rng(7)
        frag_dirs = [(k * TAU / 8 + rng.uniform(-0.12, 0.12), rng.uniform(0.15, 0.20)) for k in range(8)]

        def mk_frags():
            t = frag_t.get_value()
            g = VGroup()
            if t < 0.05:
                g.add(Circle(radius=0.52, stroke_color=CELL_MEMBRANE, stroke_width=3.5, fill_color=CELL_FILL, fill_opacity=0.92).move_to(apop_c))
                return g
            op = max(0.55, 1.0 - 0.42 * t)
            for ang, r0 in frag_dirs:
                pos = apop_c + (0.18 + 0.50 * t) * np.array([np.cos(ang), np.sin(ang), 0.0])
                g.add(Dot(pos, radius=r0 * (1.0 - 0.30 * t), color=CHECK_CORAL).set_opacity(op))
            return g

        frags = always_redraw(mk_frags)
        apop_lbl = T("Apoptosis", size=28, color=CHECK_CORAL).move_to(apop_c + RIGHT * 1.85)
        self.play(GrowArrow(arr_bot), FadeIn(frags), run_time=0.5)
        self.play(frag_t.animate.set_value(1.0), FadeIn(apop_lbl), run_time=2.6, rate_func=smooth)

        self.at("Even cells that slip past")
        slip_c = np.array([3.20, -2.35, 0.0])
        slip_cell = Circle(radius=0.45, stroke_color=CELL_MEMBRANE, stroke_width=3.5, fill_color=CELL_FILL, fill_opacity=0.92).move_to(slip_c)
        surv_src = np.array([5.85, -2.35, 0.0])
        surv_lbl = T("Survival signal", size=24, color=SURV_EMERALD).move_to([4.65, -1.60, 0.0])
        surv_arr = Arrow(surv_src, slip_c + RIGHT * 0.56, color=SURV_EMERALD, stroke_width=4, buff=0.04)
        surv_ph = ValueTracker(0.0)
        surv_ph.add_updater(lambda m, dt: m.increment_value(dt * 0.8))
        surv_stream = signal_stream([surv_src, slip_c + RIGHT * 0.52], surv_ph, n_pulses=3, color=SURV_EMERALD, radius=0.09)

        self.add(surv_ph)
        self.play(FadeIn(slip_cell, shift=RIGHT * 0.4), run_time=0.8)
        self.play(
            GrowArrow(surv_arr),
            FadeIn(surv_lbl),
            slip_cell.animate.set_stroke(SURV_EMERALD, width=4.5),
            run_time=1.2,
        )
        self.add(surv_stream)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 04: Multistep — Four cooperating faults snap on -> tumour cluster grows
# ---------------------------------------------------------------------------
class S04Multistep(SpokenScene):
    def construct(self):
        cell = make_carried_cell()
        nuc_lbl = T("Nucleus", size=24, color=BACKUP_BLUE).next_to(cell.nucleus, DOWN, buff=0.18)
        nuc_lbl.layout_ok = "covered"
        p53_gate = boxed_label("p53", color=CHECK_CORAL, size=30, box=(1.20, 0.72)).move_to(cell.gate_pos + RIGHT * 0.85)

        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.65))
        pulses = signal_stream(cell.track_pts, phase, n_pulses=6, color=ONCO_AMBER, radius=0.14)

        # Computed signal ripple expanding from p53 gate while switch is firing so active alarm stays visible
        alarm_wave = always_redraw(lambda: Circle(
            radius=0.35 + (phase.get_value() % 1.0) * 0.65,
            stroke_color=ONCO_AMBER, stroke_width=3.5,
        ).set_stroke(opacity=(1.0 - (phase.get_value() % 1.0)) * 0.85).move_to(cell.sw_pos))
        alarm_wave.layout_ok = True

        b_on = fault_badge("on", width=3.15)
        b_off = fault_badge("off", width=3.15)
        b_p53 = fault_badge("p53", width=3.15)
        b_death = fault_badge("death", width=3.15)
        badge_col = VGroup(b_on, b_off, b_p53, b_death).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.55, -0.25, 0.0])

        self.add(phase, cell, nuc_lbl, p53_gate, pulses, alarm_wave, b_on)
        self.add(scope_tag("schematic", color=TEXT))

        self.at("one stuck switch")
        self.play(Circumscribe(b_on, color=ONCO_AMBER, fade_out=True), run_time=1.0)

        self.at("To become a")
        title_badge = T("Cooperating changes (schematic)", size=26, color=TEXT).move_to([3.85, 2.35, 0.0])
        self.play(FadeIn(title_badge, shift=DOWN * 0.1), run_time=0.8)

        # Show time/step progression clearly while collecting changes
        step_lbl = T("Collecting changes...", size=24, color=ONCO_AMBER).move_to([3.85, 1.75, 0.0])
        self.play(FadeIn(step_lbl), Circumscribe(cell.rack[1], color=ONCO_AMBER, fade_out=True), run_time=1.8)

        self.at("It may pair")
        self.play(FadeOut(step_lbl, run_time=0.25), Circumscribe(cell.switch, color=ONCO_AMBER, fade_out=True), run_time=0.9)

        self.at("with a")
        off_mark = Circle(radius=0.18, stroke_color=LOSS_CRIMSON, stroke_width=3.5).move_to(cell.switch.get_center() + DOWN * 0.55 + RIGHT * 0.35)
        off_x = VGroup(
            Line([-0.12, -0.12, 0], [0.12, 0.12, 0], color=LOSS_CRIMSON, stroke_width=3.5),
            Line([-0.12, 0.12, 0], [0.12, -0.12, 0], color=LOSS_CRIMSON, stroke_width=3.5),
        ).move_to(off_mark)
        self.play(FadeIn(b_off, shift=LEFT * 0.25), FadeIn(off_mark), FadeIn(off_x), run_time=0.9)

        self.at("a broken checkpoint")
        p53_broken = DashedVMobject(
            RoundedRectangle(corner_radius=0.12, width=1.20, height=0.72, stroke_color=CHECK_CORAL, stroke_width=2.5),
            num_dashes=18, dashed_ratio=0.45,
        ).move_to(p53_gate.get_center())
        p53_x = T("p53 ×", size=26, color=CHECK_CORAL).move_to(p53_gate.get_center())
        self.play(FadeOut(p53_gate, run_time=0.22))
        self.play(FadeIn(b_p53, shift=LEFT * 0.25), FadeIn(p53_broken), FadeIn(p53_x), run_time=0.7)

        self.at("and blocked cell death")
        death_bar = Line(
            p53_broken.get_bottom() + DOWN * 0.32 + LEFT * 0.42,
            p53_broken.get_bottom() + DOWN * 0.32 + RIGHT * 0.42,
            color=CHECK_CORAL, stroke_width=6,
        )
        self.play(FadeIn(b_death, shift=LEFT * 0.25), Create(death_bar), run_time=0.9)

        self.at("Step by step")
        self.remove(pulses, alarm_wave)
        growth = ValueTracker(0.08)
        layout = cluster_layout(13, seed=7)

        def mk_growing_cluster():
            g_val = growth.get_value()
            n_vis = max(1, int(np.ceil(g_val * len(layout))))
            cells = VGroup()
            for idx in range(n_vis):
                ox, oy, rad = layout[idx]
                local = np.clip((g_val * len(layout) - idx), 0.0, 1.0)
                pos = CLUSTER_C + np.array([ox, oy, 0.0]) * CLUSTER_S * local
                r_now = rad * CLUSTER_S * (0.45 + 0.55 * local)
                c = Circle(
                    radius=r_now,
                    stroke_color=ONCO_AMBER if idx == 0 else CELL_MEMBRANE,
                    stroke_width=3.2 if idx == 0 else 2.3,
                    fill_color=CELL_FILL, fill_opacity=0.95,
                ).move_to(pos)
                nuc = Circle(
                    radius=r_now * 0.44, stroke_color=BACKUP_BLUE, stroke_width=1.8,
                    fill_color=NUCLEUS_FILL, fill_opacity=0.94,
                ).move_to(pos)
                d1 = Dot(pos + UL * (r_now * 0.25), radius=0.055 * CLUSTER_S, color=ONCO_AMBER)
                d2 = Dot(pos + UR * (r_now * 0.25), radius=0.055 * CLUSTER_S, color=LOSS_CRIMSON)
                d3 = Dot(pos + DOWN * (r_now * 0.26), radius=0.055 * CLUSTER_S, color=CHECK_CORAL)
                cells.add(VGroup(c, nuc, d1, d2, d3))
            core_local = np.clip(g_val * len(layout), 0.0, 1.0)
            core_r = layout[0][2] * CLUSTER_S * (0.45 + 0.55 * core_local)
            sw_pos = CLUSTER_C + (core_r + 0.40 * CLUSTER_S) * UL_UNIT
            sw = make_switch_icon(sw_pos, scale=1.05 * CLUSTER_S, active=True, angle=PI / 4)
            return VGroup(cells, sw)

        growing = always_redraw(mk_growing_cluster)
        self.play(
            FadeOut(cell), FadeOut(nuc_lbl), FadeOut(p53_broken), FadeOut(p53_x),
            FadeOut(off_mark), FadeOut(off_x), FadeOut(death_bar), FadeOut(title_badge),
            FadeIn(growing),
            run_time=0.7,
        )
        self.play(growth.animate.set_value(1.0), run_time=3.8, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 05: Predict — Targeted drug blocks ONLY the stuck switch
# ---------------------------------------------------------------------------
class S05AddictionPredict(SpokenScene):
    def construct(self):
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.70))
        pwr = ValueTracker(1.0)

        cluster = always_redraw(lambda: build_tumour_cluster(
            CLUSTER_C, scale=CLUSTER_S,
            active_switch=pwr.get_value() > 0.3,
            shrink=0.0,
            pulse_phase=phase.get_value() if pwr.get_value() > 0.3 else None,
        ))
        b_on = fault_badge("on", width=3.15)
        b_off = fault_badge("off", width=3.15)
        b_p53 = fault_badge("p53", width=3.15)
        b_death = fault_badge("death", width=3.15)
        badge_col = VGroup(b_on, b_off, b_p53, b_death).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.55, -0.25, 0.0])

        sw_a = cluster_switch_pos(CLUSTER_C, CLUSTER_S, 0.0)
        sig_pts = [sw_a + np.array([0.22, -0.22, 0.0]), CLUSTER_C, CLUSTER_C + np.array([0.68, -0.40, 0.0])]
        pulses = signal_stream(sig_pts, phase, power_tracker=pwr, n_pulses=6, color=ONCO_AMBER, radius=0.12)

        self.add(phase, pwr, cluster, badge_col, pulses)
        self.add(scope_tag("schematic", color=TEXT))

        self.at("Its checkpoint is gone")
        self.play(Circumscribe(b_p53, color=CHECK_CORAL, fade_out=True), run_time=0.9)

        self.at("its off switch is missing")
        self.play(Circumscribe(b_off, color=LOSS_CRIMSON, fade_out=True), run_time=0.9)

        self.at("one growth switch is jammed on")
        self.play(Circumscribe(b_on, color=ONCO_AMBER, fade_out=True), run_time=1.0)

        self.at("Suppose a targeted drug")
        wedge_target = make_drug_wedge(scale=1.05 * CLUSTER_S, angle=PI / 4).move_to(sw_a + UL * (0.28 * CLUSTER_S))
        wedge_start = wedge_target.copy().shift(UP * 1.45 + LEFT * 0.45)
        drug_lbl = T("Targeted drug", size=26, color=DRUG_CYAN).move_to([-4.65, 2.25, 0.0])
        drug_arr = Arrow(drug_lbl.get_right() + RIGHT * 0.12, wedge_target.get_corner(UL) + UL * 0.06, color=DRUG_CYAN, stroke_width=4, buff=0.04)
        self.play(FadeIn(wedge_start), FadeIn(drug_lbl), run_time=0.7)
        self.play(Transform(wedge_start, wedge_target), GrowArrow(drug_arr), run_time=1.1)

        self.at("shuts off")
        b_blocked = fault_badge("switched_off", width=3.15).move_to(b_on.get_center())
        self.play(
            pwr.animate.set_value(0.0),
            swap(b_on, b_blocked, run_time=0.6),
            run_time=1.5,
        )

        self.at("every other mutation untouched")
        self.play(Circumscribe(b_off, color=LOSS_CRIMSON, fade_out=True), run_time=1.1)
        self.play(Circumscribe(b_p53, color=CHECK_CORAL, fade_out=True), run_time=1.1)
        self.play(Circumscribe(b_death, color=CHECK_CORAL, fade_out=True), run_time=1.1)

        self.at("Will the tumor keep growing")
        q = question_card("Block only one stuck switch: keep growing or shrink?", y=3.25, max_w=12.0)
        q.question.set_x(0.0)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 06: Predict Pause (4.5 s)
# ---------------------------------------------------------------------------
class S06Pause(PredictPause):
    QUESTION = "Block only one stuck switch: keep growing or shrink?"
    CARD = {"y": 3.25, "max_w": 12.0}
    SECONDS = 4.5
    RING_AT = (6.0, -3.0, 0)

    def backdrop(self):
        return build_s05_end_backdrop(show_badges=True)

    def construct(self):
        backdrop = self.backdrop()
        self.add(backdrop)
        qc = question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD)
        qc.question.set_x(0.0)
        self.add(qc)

        # Gentle pulsing on the untouched broken badges (matches script.json visual note)
        badges = backdrop[-1]
        broken_badges = VGroup(badges[1], badges[2], badges[3])
        pt = ValueTracker(0.0)
        broken_badges.add_updater(lambda m, dt: None)
        pulse_ring = always_redraw(lambda: VGroup(*[
            RoundedRectangle(
                corner_radius=0.14, width=b.box.width + 0.08 + 0.05 * np.sin(pt.get_value() * TAU),
                height=b.box.height + 0.08 + 0.05 * np.sin(pt.get_value() * TAU),
                stroke_color=CHECK_CORAL, stroke_width=2.5,
            ).set_stroke(opacity=0.35 + 0.35 * np.sin(pt.get_value() * TAU)).move_to(b.get_center())
            for b in broken_badges
        ]))
        pulse_ring.layout_ok = True

        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        bar_bg = Line([-5.4, -3.32, 0], [4.9, -3.32, 0], color=SLATE_LINE, stroke_width=8).set_opacity(0.35)
        bar_fg = always_redraw(lambda: Line(
            [-5.4, -3.32, 0],
            [-5.4 + max(0.08, 10.3 * pt.get_value() / 2.0), -3.32, 0],
            color=DRUG_CYAN, stroke_width=10,
        ))
        self.add(ring, bar_bg, bar_fg, pulse_ring)
        self.play(run, pt.animate(run_time=self.SECONDS, rate_func=linear).set_value(2.0))
        self.finish()


# ---------------------------------------------------------------------------
# Scene 07: Reveal — Cluster contracts smoothly across the whole scene
# ---------------------------------------------------------------------------
class S07RevealAddiction(SpokenScene):
    def construct(self):
        qc = question_card("Block only one stuck switch: keep growing or shrink?", y=3.25, max_w=12.0)
        qc.question.set_x(0.0)
        b_blocked = fault_badge("switched_off", width=3.15)
        b_off = fault_badge("off", width=3.15)
        b_p53 = fault_badge("p53", width=3.15)
        b_death = fault_badge("death", width=3.15)
        badge_col = VGroup(b_blocked, b_off, b_p53, b_death).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.55, -0.25, 0.0])

        shrink_t = ValueTracker(0.0)

        def mk_contracting():
            s = shrink_t.get_value()
            cl = build_tumour_cluster(CLUSTER_C, scale=CLUSTER_S, active_switch=False, shrink=s)
            wd = build_drug_on_cluster(cl, scale=CLUSTER_S)
            return VGroup(cl, wd)

        cluster_grp = always_redraw(mk_contracting)
        drug_lbl = T("Targeted drug", size=26, color=DRUG_CYAN).move_to([-4.65, 2.25, 0.0])
        drug_arr = always_redraw(lambda: Arrow(
            drug_lbl.get_right() + RIGHT * 0.12,
            cluster_switch_pos(CLUSTER_C, CLUSTER_S, shrink_t.get_value()) + UL * (0.58 * CLUSTER_S) + LEFT * 0.08,
            color=DRUG_CYAN, stroke_width=4, buff=0.04,
        ))

        self.add(qc, badge_col, cluster_grp, drug_lbl, drug_arr)
        self.add(scope_tag("schematic", color=TEXT))

        self.play(FadeOut(qc, run_time=0.25))
        self.at("the tumor shrinks")
        self.play(shrink_t.animate.set_value(0.45), run_time=4.8, rate_func=linear)

        self.at("Their other mutations")
        self.play(shrink_t.animate.set_value(0.54), Circumscribe(b_off, color=LOSS_CRIMSON, fade_out=True), run_time=1.8, rate_func=linear)
        self.play(shrink_t.animate.set_value(0.62), Circumscribe(b_p53, color=CHECK_CORAL, fade_out=True), run_time=1.6, rate_func=linear)

        self.at("stop dividing or die")
        self.play(shrink_t.animate.set_value(0.70), Circumscribe(b_death, color=CHECK_CORAL, fade_out=True), run_time=2.5, rate_func=linear)

        self.at("Scientists call this dependence")
        addict_box = boxed_label("Oncogene addiction", color=ONCO_AMBER, size=32).move_to([0.0, 2.95, 0.0])
        self.play(FadeIn(addict_box, shift=DOWN * 0.15), shrink_t.animate.set_value(0.78), run_time=2.6, rate_func=linear)

        self.at("That is why one targeted drug")
        self.play(shrink_t.animate.set_value(0.88), run_time=5.6, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 08: Debated Mechanisms — TwoPanel: feedback vs differential decay
# ---------------------------------------------------------------------------
class S08DebatedMechanisms(SpokenScene):
    def construct(self):
        header = T("Debated mechanisms (schematic)", size=34, color=TEXT).move_to([0, 3.30, 0])
        tp = TwoPanel(
            "1. Feedback quiets backups",
            "2. Survival fades faster",
            colors=(ONCO_AMBER, SURV_EMERALD),
            top=2.82, bottom=-2.95, gap=0.45, width=12.8, size=28,
        )
        self.add(scope_tag("schematic", color=TEXT))

        sw_box = boxed_label("Stuck switch", color=ONCO_AMBER, size=24).move_to([-4.68, 1.35, 0.0])
        main_arr = Arrow([-4.68, 0.96, 0.0], [-4.68, -0.45, 0.0], color=ONCO_AMBER, stroke_width=5, buff=0)
        main_lbl = T("Main path", size=24, color=ONCO_AMBER).move_to([-4.68, -0.82, 0.0])

        backup_level = ValueTracker(1.0)
        bk_box = boxed_label("Backup route", color=BACKUP_BLUE, size=24).move_to([-1.85, 1.35, 0.0])
        bk_arr = always_redraw(lambda: Arrow(
            [-1.85, 0.96, 0.0], [-1.85, -0.45, 0.0],
            color=BACKUP_BLUE, stroke_width=2 + 4 * backup_level.get_value(), buff=0,
        ).set_opacity(0.25 + 0.75 * backup_level.get_value()))
        bk_state = T("Active", size=24, color=BACKUP_BLUE).move_to([-1.85, -0.82, 0.0])
        bk_quiet = T("Quieted", size=24, color=LOSS_CRIMSON).move_to([-1.85, -0.82, 0.0])

        fb = ValueTracker(0.15)
        fb_lbl = T("Feedback brake", size=24, color=ONCO_AMBER).move_to([-3.31, -1.65, 0.0])
        fb_track = RoundedRectangle(corner_radius=0.08, width=4.2, height=0.34, stroke_color=SLATE_LINE, stroke_width=2.5).move_to([-3.31, -2.22, 0.0])
        fb_fill = always_redraw(lambda: Rectangle(
            width=max(0.08, 4.12 * fb.get_value()), height=0.26,
            stroke_width=0, fill_color=ONCO_AMBER, fill_opacity=0.88,
        ).move_to([-3.31 - 2.06 + max(0.08, 4.12 * fb.get_value()) / 2, -2.22, 0.0]))
        inh_line = Line([-3.75, 0.25, 0.0], [-2.25, 0.25, 0.0], color=CHECK_CORAL, stroke_width=4)
        inh_cap = Line([-2.25, 0.05, 0.0], [-2.25, 0.45, 0.0], color=CHECK_CORAL, stroke_width=5)
        inhib = VGroup(inh_line, inh_cap)

        P = Plot(
            box=(1.45, 5.75, -0.25, 1.48), xr=(0, 10), yr=(0, 1.15),
            xticks=[], yticks=[(0, "0"), (1, "High")],
            xlabel="time after drug", ylabel="Signal", color=TEXT, size=22, label_size=24,
        )
        t_dec = ValueTracker(0.0)
        surv_fn = lambda x: np.exp(-x / 2.0)
        death_fn = lambda x: np.exp(-x / 7.5)
        surv_curve = P.live_curve(surv_fn, t_dec, color=SURV_EMERALD, width=5)
        death_curve = P.live_curve(death_fn, t_dec, color=CHECK_CORAL, width=5)
        surv_dot = P.dot(lambda: t_dec.get_value(), lambda: surv_fn(t_dec.get_value()), color=SURV_EMERALD, ring=TEXT, radius=0.08)
        death_dot = P.dot(lambda: t_dec.get_value(), lambda: death_fn(t_dec.get_value()), color=CHECK_CORAL, ring=TEXT, radius=0.08)
        leg_d = T("Death", size=24, color=CHECK_CORAL).move_to([4.85, 1.32, 0.0])
        leg_s = T("Survival", size=24, color=SURV_EMERALD).move_to([4.85, 0.92, 0.0])

        fulc_pos = np.array([3.31, -2.35, 0.0])
        fulc = Polygon(
            fulc_pos + LEFT * 0.26 + DOWN * 0.35,
            fulc_pos + RIGHT * 0.26 + DOWN * 0.35,
            fulc_pos,
            stroke_color=TEXT, stroke_width=2.5, fill_color=CELL_FILL, fill_opacity=0.95,
        )

        def beam_angle():
            t = t_dec.get_value()
            return float(np.clip(-0.30 * (death_fn(t) - surv_fn(t)) / (death_fn(t) + surv_fn(t) + 1e-6), -0.32, 0.0))

        beam = always_redraw(lambda: Line(
            fulc_pos + 1.55 * np.array([-np.cos(beam_angle()), -np.sin(beam_angle()), 0.0]),
            fulc_pos + 1.55 * np.array([np.cos(beam_angle()), np.sin(beam_angle()), 0.0]),
            color=TEXT, stroke_width=5,
        ))
        left_pan = always_redraw(lambda: T("Survival", size=24, color=SURV_EMERALD).move_to(
            fulc_pos + 1.55 * np.array([-np.cos(beam_angle()), -np.sin(beam_angle()), 0.0]) + UP * 0.34
        ))
        right_pan = always_redraw(lambda: T("Death", size=24, color=CHECK_CORAL).move_to(
            fulc_pos + 1.55 * np.array([np.cos(beam_angle()), np.sin(beam_angle()), 0.0]) + UP * 0.34
        ))

        self.play(
            FadeIn(header, shift=DOWN * 0.1),
            Create(tp.left_frame),
            Create(tp.right_frame),
            run_time=1.6,
        )
        self.play(
            FadeIn(sw_box), FadeIn(main_arr), FadeIn(main_lbl),
            run_time=1.5,
        )

        self.at("The exact cause is still debated")
        self.play(
            FadeIn(tp.left_head, shift=DOWN * 0.1),
            FadeIn(tp.right_head, shift=DOWN * 0.1),
            FadeIn(bk_box), FadeIn(bk_arr), FadeIn(bk_state),
            FadeIn(fb_lbl), FadeIn(fb_track), FadeIn(fb_fill),
            run_time=1.8,
        )

        self.at("two ideas lead")
        self.play(
            Create(P),
            FadeIn(fulc), FadeIn(beam), FadeIn(left_pan), FadeIn(right_pan),
            run_time=1.8,
        )

        self.at("First")
        self.play(Circumscribe(tp.left_head, color=ONCO_AMBER, fade_out=True), run_time=1.0)

        self.at("keeps feedback")
        self.play(fb.animate.set_value(0.92), Create(inhib), run_time=2.0, rate_func=smooth)

        self.at("quiet nearby backup routes")
        self.play(backup_level.animate.set_value(0.15), swap(bk_state, bk_quiet, run_time=0.6), run_time=1.6)

        self.at("Second")
        self.play(
            Circumscribe(tp.right_head, color=SURV_EMERALD, fade_out=True),
            FadeIn(leg_d), FadeIn(leg_s),
            run_time=1.2,
        )
        self.add(surv_curve, death_curve, surv_dot, death_dot)

        self.at("survival signals may fade")
        self.play(t_dec.animate.set_value(7.2), run_time=3.6, rate_func=linear)

        self.at("Either way")
        self.play(t_dec.animate.set_value(10.0), run_time=1.8, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 09: Closing — Three-stage cell -> tumour -> collapse arc + takeaway
# ---------------------------------------------------------------------------
class S09Closing(SpokenScene):
    def construct(self):
        c1 = np.array([-4.65, 0.48, 0.0])
        cell1 = Circle(radius=1.22, stroke_color=CELL_MEMBRANE, stroke_width=4, fill_color=CELL_FILL, fill_opacity=0.95).move_to(c1)
        nuc1 = Circle(radius=0.46, stroke_color=BACKUP_BLUE, stroke_width=2.5, fill_color=NUCLEUS_FILL, fill_opacity=0.96).move_to(c1)
        sw1 = make_switch_icon(c1 + np.array([-0.86, 0.86, 0.0]), scale=0.60, active=True, angle=PI / 4)
        p53_1 = boxed_label("p53", color=CHECK_CORAL, size=24, box=(0.82, 0.50)).move_to(c1 + RIGHT * 1.82)
        t1_pts = [c1 + np.array([-0.68, 0.68, 0.0]), c1, c1 + RIGHT * 1.06]
        ph1 = ValueTracker(0.0)
        ph1.add_updater(lambda m, dt: m.increment_value(dt * 0.65))
        pulses1 = signal_stream(t1_pts, ph1, n_pulses=4, color=ONCO_AMBER, radius=0.09)
        lbl1 = T("1 switch → halted", size=26, color=CHECK_CORAL).move_to([-4.35, -1.85, 0.0])
        stage1 = VGroup(cell1, nuc1, sw1, p53_1)

        c2 = np.array([0.05, 0.48, 0.0])
        g2 = ValueTracker(0.15)
        layout = cluster_layout(11, seed=7)

        def mk_stage2():
            gv = g2.get_value()
            n_vis = max(1, int(np.ceil(gv * len(layout))))
            cells = VGroup()
            for idx in range(n_vis):
                ox, oy, rad = layout[idx]
                local = np.clip((gv * len(layout) - idx), 0.0, 1.0)
                pos = c2 + np.array([ox, oy, 0.0]) * 0.58 * local
                r_now = rad * 0.58 * (0.45 + 0.55 * local)
                cells.add(Circle(
                    radius=r_now, stroke_color=ONCO_AMBER if idx == 0 else CELL_MEMBRANE,
                    stroke_width=2.4, fill_color=CELL_FILL, fill_opacity=0.95,
                ).move_to(pos))
                cells.add(Dot(pos + UR * (r_now * 0.25), radius=0.04, color=LOSS_CRIMSON))
                cells.add(Dot(pos + DOWN * (r_now * 0.25), radius=0.04, color=CHECK_CORAL))
            return cells

        cluster2 = always_redraw(mk_stage2)
        lbl2 = T("Several faults → tumour", size=26, color=ONCO_AMBER).move_to([0.05, -1.85, 0.0])

        c3 = np.array([4.50, 0.48, 0.0])
        s3 = ValueTracker(0.0)

        def mk_stage3():
            sv = s3.get_value()
            cl = build_tumour_cluster(c3, scale=0.56, active_switch=False, shrink=sv)
            wd = build_drug_on_cluster(cl, scale=0.56)
            return VGroup(cl, wd)

        cluster3 = always_redraw(mk_stage3)
        lbl3 = T("Block 1 switch → shrinks", size=26, color=DRUG_CYAN).move_to([4.45, -1.85, 0.0])

        arr12 = Arrow([p53_1.get_right()[0] + 0.18, 0.48, 0.0], [-1.52, 0.48, 0.0], color=TEXT, stroke_width=4, buff=0)
        arr23 = Arrow([1.85, 0.48, 0.0], [2.55, 0.48, 0.0], color=TEXT, stroke_width=4, buff=0)

        self.add(ph1, stage1, pulses1, lbl1, scope_tag("schematic", color=TEXT))

        self.at("so cancer usually requires")
        self.play(GrowArrow(arr12), FadeIn(cluster2), FadeIn(lbl2), run_time=0.9)
        self.play(g2.animate.set_value(1.0), run_time=4.2, rate_func=smooth)

        self.at("Yet a tumor")
        self.play(GrowArrow(arr23), FadeIn(cluster3), FadeIn(lbl3), run_time=1.0)
        self.play(s3.animate.set_value(0.86), run_time=4.6, rate_func=smooth)

        self.at("Put both halves together")
        top_tag = T("Many mutations, one weak point (schematic)", size=30, color=TEXT).move_to([0.0, 2.85, 0.0])
        self.play(FadeIn(top_tag, shift=DOWN * 0.1), run_time=0.8)

        self.at("Tumors usually need")
        cap = caption("Tumours usually need several changes, yet often depend on one stuck switch.", size=28, color=TEXT, y=-2.85)
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 10: Standard End Card
# ---------------------------------------------------------------------------
class S10End(EndCard):
    LINE = "Tumours usually need several changes, yet often depend on one stuck switch."
