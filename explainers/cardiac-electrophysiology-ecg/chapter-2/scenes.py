"""
The Edges of the Wave — Cardiac Action Potentials and the ECG (Chapter 2)
=========================================================================

COLOUR MAP (one colour per concept for the whole film):
- Single-cell voltage trace (action potential): WHITE        (#FFFFFF)
- Excited cells on their plateau (~+10 mV):     PLATEAU_GOLD (#F5C542)
- Resting cells (~-90 mV):                      REST_BLUE    (#4EA8DE)
- Surface ECG tracing & pen:                    ECG_GREEN    (#39E58C)
- Moving boundary, current loops, battery:      EDGE_MAGENTA (#F249B3)
- Neutral labels, brackets, chest electrode:    TEXT         (#E8EAF0)
- ECG paper & fluid subtle backdrops:           PAPER_BG (#1F2E40), FLUID_BG (#1E3044)

ONE WORLD, CARRIED THROUGH THE FILM:
- Top half (y = +0.25 to +3.35): the cardiac tissue & skin electrode.
  In s00-s08 this is a horizontal strip of 10 ventricular muscle cells joined end-to-end
  inside a thin band of extracellular fluid under a neutral chest electrode (no +/- sign).
  In s09-s21 the strip morphs into a schematic four-chamber heart tiled with myocardial cells
  (atria, narrow AV node/bundle of His bridge, ventricles with Purkinje network).
- Bottom half (y = -2.55 to -0.32): a full-width dark ECG paper strip with a bright GREEN
  tracing drawn left-to-right by a live pen dot, plus a 'schematic' tag at bottom right all film.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Single-cell ventricular AP marker advances onto its computed plateau (+10 mV) while all 10 strip cells depolarize uniformly from -90 to +10 mV and the computed dipole ECG trace draws dead level.
- s02_guess: 10 computed single-cell AP curves lift from the cells and sum into one tall WHITE sum curve staying high on the plateau, then get crossed out as the level GREEN trace continues underneath.
- s03_electrode: View zooms onto the chest electrode, fluid band, and central cells; computed dipole streamlines in MAGENTA appear and circulate toward the electrode only when adjacent cells differ in voltage, vanishing when both match.
- s04_boundary: View pulls back to the full 10-cell strip; a computed wave front travels across cells 1-5 turning them GOLD while cells 6-10 stay BLUE, lighting the halfway boundary as the ECG pen records it.
- s05_battery: Positive charge markers cross the gap junction from cell 5 to 6, a computed MAGENTA circuit loop closes through the fluid and condenses into a MAGENTA battery that slides rightward turning cells GOLD while the computed GREEN deflection rises and returns level at the end.
- s07_idea: Three live side-by-side panels run simultaneously (all BLUE level, moving MAGENTA boundary deflecting, all GOLD level), each driven by the strip dipole computation.
- s09_p_wave: The 10-cell strip morphs into the tiled schematic heart; at rest the GREEN pen runs level, then a computed atrial wave front sweeps from the SA node turning atrial tiles GOLD as the pen draws the P wave.
- s11_predict: A small MAGENTA dot creeps down the narrow AV node / bundle of His bridge between GOLD atria and BLUE ventricles while the GREEN pen pauses just after P.
- s13_answer: The MAGENTA dot finishes crossing the narrow bridge as the GREEN pen draws the nearly level PR segment; beside the heart, tiny vs large MAGENTA batteries grow with proportional deflection bars driven by one size tracker.
- s14_qrs: Purkinje branches flash and a broad computed MAGENTA wave sweeps rapidly through the ventricular tiles turning them GOLD as the GREEN pen draws the tall narrow QRS complex, marked by its crossing-time bracket.
- s16_st: With every ventricular tile uniformly GOLD and zero MAGENTA, the single-cell inset dot glides along its computed plateau while the GREEN pen draws the nearly flat ST segment.
- s18_t_wave: Ventricular tiles repolarize at regionally distinct computed times from GOLD to BLUE, forming a broad soft MAGENTA recovery band (no direction arrow) while the GREEN pen draws the broad rounded T wave.
- s20_qt: The white QT bracket spans QRS-start to T-end with the computed single-cell AP aligned directly below; one plateau-duration ValueTracker stretches the cell plateau, slides the T wave rightward, and stretches the QT bracket together.
- s21_return: The tiled heart replays one complete computed beat synced to the narration — flat when all BLUE, flat when ventricles are all GOLD with atria back to BLUE, deflecting only while each MAGENTA boundary travels.
"""
import numpy as np
from bp_parts import *

# ------------------------------------------------------------------ Film Palette
CELL_WHITE = "#FFFFFF"
PLATEAU_GOLD = "#F5C542"
REST_BLUE = "#4EA8DE"
ECG_GREEN = "#39E58C"
EDGE_MAGENTA = "#F249B3"
PAPER_BG = "#1F2E40"
PAPER_BORDER = "#45607D"
PAPER_GRID = "#324963"
FLUID_BG = "#1E3044"
FLUID_BORDER = "#3E5C7E"
INSULATOR_COL = "#5E738E"

# ------------------------------------------------------------------ Shared Geometry Constants
STRIP_Y = 1.18
STRIP_N = 10
CELL_W = 1.04
CELL_H = 1.30
CELL_GAP = 0.08
STRIP_SPAN = STRIP_N * CELL_W + (STRIP_N - 1) * CELL_GAP  # 11.12

PAPER_BOX = (-6.1, 6.1, -2.55, -0.32)  # (x0, x1, y0, y1)
BASE_Y = -1.78
ECG_AMP = 1.15


# ------------------------------------------------------------------ Computed Biophysical Models
def ventricular_ap(t_ms, plateau_ms=200.0):
    """Computed human ventricular action potential V_m(t) in mV (lesson values: -90 mV rest,
    +30 mV peak, ~+10 mV plateau for ~200 ms, phase 3 return to -90 mV).
    t_ms = 0 is the phase 0 upstroke onset."""
    t = float(t_ms)
    if t < 0.0:
        return -90.0
    if t < 6.0:
        s = 0.5 * (1.0 - np.cos(np.pi * t / 6.0))
        return -90.0 + 120.0 * s
    if t < 22.0:
        s = 0.5 * (1.0 - np.cos(np.pi * (t - 6.0) / 16.0))
        return 30.0 - 18.0 * s
    p_end = 22.0 + plateau_ms
    if t < p_end:
        f = (t - 22.0) / max(plateau_ms, 1.0)
        return 12.0 - 16.0 * (f ** 1.35)
    r_dur = 85.0
    if t < p_end + r_dur:
        f = (t - p_end) / r_dur
        s = 0.5 * (1.0 - np.cos(np.pi * f))
        return -4.0 - 86.0 * s
    return -90.0


def ap_norm(t_ms, plateau_ms=200.0):
    """Normalized ventricular AP in [0, 1] (-90 mV -> 0, +30 mV -> 1)."""
    return (ventricular_ap(t_ms, plateau_ms) + 90.0) / 120.0


def strip_cell_states(front_pos, width=0.22):
    """Excitation level s_i in [0, 1] for 10 cells (indices 0..9) given wave front position
    in cell coordinates (-1.2 = all rest, 5.0 = halfway, 11.2 = all plateau)."""
    idx = np.arange(STRIP_N, dtype=float) + 0.5
    return 1.0 / (1.0 + np.exp((idx - front_pos) / width))


def strip_dipole_ecg(front_pos, width=0.22):
    """Computed schematic ECG deflection from the 10-cell strip dipole sum:
    sum_i (s_i - s_{i+1}) = s_0 - s_9. Zero when all rest or all plateau; >0 only while
    a boundary travels inside the strip."""
    s = strip_cell_states(front_pos, width)
    return float(s[0] - s[-1])


def beat_ecg_value(t_s, extra_plateau_s=0.0):
    """Computed schematic single-beat ECG waveform (normalized units, R peak ~ +1.0)
    matching the lesson's adult resting intervals (PR 0.16 s, QRS 0.08 s, QT ~0.39 s):
      0.00 - 0.08 s: baseline rest (flat)
      0.08 - 0.16 s: P wave (atrial depolarization)
      0.16 - 0.24 s: PR segment (AV node/His — tiny tissue -> nearly flat)
      0.24 - 0.32 s: QRS complex (ventricular depolarization, crossing time 0.08 s)
      0.32 - 0.48+extra: ST segment (all ventricles on plateau -> nearly flat)
      0.48+extra - 0.64+extra: T wave (broad regional ventricular repolarization)
      0.64+extra - 0.80+extra: baseline rest (flat)
    """
    t = float(t_s)
    p = 0.22 * np.exp(-0.5 * ((t - 0.120) / 0.017) ** 2)
    q = -0.14 * np.exp(-0.5 * ((t - 0.256) / 0.007) ** 2)
    r = 1.08 * np.exp(-0.5 * ((t - 0.278) / 0.0085) ** 2)
    s_dip = -0.22 * np.exp(-0.5 * ((t - 0.298) / 0.008) ** 2)
    t_center = 0.560 + extra_plateau_s
    sig_t = 0.036 if t < t_center else 0.028
    tw = 0.36 * np.exp(-0.5 * ((t - t_center) / sig_t) ** 2)
    return float(p + q + r + s_dip + tw)


# ------------------------------------------------------------------ Reusable Visual Builders
def tag_schematic():
    """Honest 'schematic' tag in the bottom-right safe zone, full opacity TEXT (never grey)."""
    return scope_tag("schematic", size=24, color=TEXT)


def label_plate(mob, pad_x=0.12, pad_y=0.06):
    """Dark opaque backing behind a label over paper/shapes so grid lines never cross letters."""
    bg = RoundedRectangle(
        corner_radius=0.08,
        width=mob.width + 2 * pad_x,
        height=mob.height + 2 * pad_y,
        fill_color=BG,
        fill_opacity=0.92,
        stroke_width=0,
    ).move_to(mob)
    return VGroup(bg, mob)


def build_ecg_paper(box=PAPER_BOX, base_y=BASE_Y, grid_nx=24, grid_ny=6):
    """Dark ECG paper panel with subtle grid lines (opacity < 0.25 so clean behind labels)."""
    x0, x1, y0, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    bg = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        fill_color=PAPER_BG, fill_opacity=0.95,
        stroke_color=PAPER_BORDER, stroke_width=2.4,
    ).move_to([cx, cy, 0])
    grid = VGroup()
    for i in range(1, grid_nx):
        gx = x0 + w * i / grid_nx
        is_maj = (i % 4 == 0)
        grid.add(Line(
            [gx, y0 + 0.03, 0], [gx, y1 - 0.03, 0],
            stroke_color=PAPER_GRID,
            stroke_width=1.5 if is_maj else 0.75,
            stroke_opacity=0.23 if is_maj else 0.15,
        ))
    for j in range(1, grid_ny):
        gy = y0 + h * j / grid_ny
        is_maj = (j % 2 == 0)
        grid.add(Line(
            [x0 + 0.03, gy, 0], [x1 - 0.03, gy, 0],
            stroke_color=PAPER_GRID,
            stroke_width=1.5 if is_maj else 0.75,
            stroke_opacity=0.23 if is_maj else 0.15,
        ))
    base_line = DashedLine(
        [x0 + 0.15, base_y, 0], [x1 - 0.15, base_y, 0],
        dash_length=0.14, stroke_color=PAPER_BORDER, stroke_width=1.3, stroke_opacity=0.23,
    )
    g = VGroup(bg, grid, base_line)
    g.box = box
    g.base_y = base_y
    return g


def build_electrode(center=(0.0, 2.78, 0.0), scale=1.0):
    """Neutral chest electrode icon above the tissue strip (NO plus or minus sign)."""
    c = np.array(center, dtype=float)
    skin = Arc(
        radius=2.4 * scale, start_angle=PI / 2 - 0.32, angle=0.64,
        arc_center=c + DOWN * (2.52 * scale),
        stroke_color=TEXT, stroke_width=2.5 * scale, stroke_opacity=0.75,
    )
    pad = RoundedRectangle(
        corner_radius=0.08 * scale, width=0.92 * scale, height=0.26 * scale,
        fill_color=TEXT, fill_opacity=0.94, stroke_color=TEXT, stroke_width=2.0 * scale,
    ).move_to(c)
    stud = Circle(
        radius=0.11 * scale, fill_color=ECG_GREEN, fill_opacity=1.0,
        stroke_color=TEXT, stroke_width=2.0 * scale,
    ).move_to(c + UP * (0.20 * scale))
    wire = CubicBezier(
        c + UP * (0.31 * scale),
        c + UP * (0.62 * scale) + RIGHT * (0.15 * scale),
        c + UP * (0.58 * scale) + RIGHT * (0.65 * scale),
        c + UP * (0.72 * scale) + RIGHT * (1.05 * scale),
        stroke_color=ECG_GREEN, stroke_width=3.2 * scale,
    )
    return VGroup(skin, pad, stud, wire)


def strip_cell_xs(n=STRIP_N, cell_w=CELL_W, gap=CELL_GAP, cx=0.0):
    total = n * cell_w + (n - 1) * gap
    x0 = cx - total / 2.0 + cell_w / 2.0
    return [x0 + i * (cell_w + gap) for i in range(n)]


def build_cell_strip(states=None, y=STRIP_Y, n=STRIP_N, cell_w=CELL_W, cell_h=CELL_H,
                     gap=CELL_GAP, cx=0.0, show_fluid=True):
    """10 ventricular muscle cells joined end-to-end by gap junctions inside extracellular fluid."""
    if states is None:
        states = np.zeros(n)
    xs = strip_cell_xs(n, cell_w, gap, cx)
    total_w = n * cell_w + (n - 1) * gap
    g = VGroup()
    if show_fluid:
        fluid = RoundedRectangle(
            corner_radius=0.24, width=total_w + 0.56, height=cell_h + 0.54,
            fill_color=FLUID_BG, fill_opacity=0.92,
            stroke_color=FLUID_BORDER, stroke_width=2.0, stroke_opacity=0.8,
        ).move_to([cx, y, 0])
        g.add(fluid)
        g.fluid = fluid
    cells = VGroup()
    junctions = VGroup()
    for i, x in enumerate(xs):
        s = float(np.clip(states[i], 0.0, 1.0))
        col = interpolate_color(ManimColor(REST_BLUE), ManimColor(PLATEAU_GOLD), s)
        cell = RoundedRectangle(
            corner_radius=0.14, width=cell_w, height=cell_h,
            fill_color=col, fill_opacity=0.88,
            stroke_color=col, stroke_width=3.0,
        ).move_to([x, y, 0])
        cells.add(cell)
        if i < n - 1:
            jx = x + (cell_w + gap) / 2.0
            for dy in (-0.22 * cell_h, 0.22 * cell_h):
                junctions.add(Line(
                    [jx - gap * 0.85, y + dy, 0], [jx + gap * 0.85, y + dy, 0],
                    stroke_color=TEXT, stroke_width=3.0, stroke_opacity=0.8,
                ))
    g.add(junctions, cells)
    g.cells = cells
    g.junctions = junctions
    g.xs = xs
    return g


def build_ap_inset(box=(-6.1, -3.15, 2.25, 3.48), t_dot_ms=None, plateau_ms=200.0,
                   draw_live=False, highlight_plateau_to=None):
    """Small inset showing the first film's computed WHITE ventricular action potential."""
    x0, x1, y0, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    frame = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        fill_color=PAPER_BG, fill_opacity=0.95,
        stroke_color=TEXT, stroke_width=2.2, stroke_opacity=0.85,
    ).move_to([cx, cy, 0])
    px0, px1 = x0 + 0.22, x1 - 0.18
    py0, py1 = y0 + 0.20, y1 - 0.38

    def pt_of(t):
        return np.array([
            px0 + (t + 40.0) / 400.0 * (px1 - px0),
            py0 + ap_norm(t, plateau_ms) * (py1 - py0),
            0.0,
        ])

    t_end = float(t_dot_ms) if (draw_live and t_dot_ms is not None) else 360.0
    t_end = max(-35.0, min(360.0, t_end))
    ts = np.linspace(-40.0, t_end, max(10, int(180 * (t_end + 40.0) / 400.0)))
    pts = [pt_of(t) for t in ts]
    curve = VMobject(stroke_color=CELL_WHITE, stroke_width=3.8, fill_opacity=0)
    curve.set_points_as_corners(pts)
    ttl = T("one cell", size=24, color=TEXT).move_to([cx, y1 - 0.18, 0])
    g = VGroup(frame, curve, ttl)

    if highlight_plateau_to is not None and highlight_plateau_to > 24.0:
        he = min(float(highlight_plateau_to), 22.0 + plateau_ms)
        hts = np.linspace(22.0, he, max(6, int(80 * (he - 22.0) / plateau_ms)))
        hcrv = VMobject(stroke_color=PLATEAU_GOLD, stroke_width=5.4, fill_opacity=0)
        hcrv.set_points_as_corners([pt_of(t) for t in hts])
        g.add(hcrv)

    if t_dot_ms is not None:
        dp = pt_of(float(t_dot_ms))
        dot = Dot(dp, radius=0.085, color=PLATEAU_GOLD, stroke_color=CELL_WHITE, stroke_width=2.2)
        g.add(dot)
        g.dot = dot
    g.px0, g.px1, g.py0, g.py1 = px0, px1, py0, py1
    return g


def build_plus_mark(center, size=0.11, color=CELL_WHITE, sw=3.4):
    """Geometric '+' sign (not a tiny font glyph, so clean at any size)."""
    c = np.array(center, dtype=float)
    return VGroup(
        Line(c + LEFT * size, c + RIGHT * size, stroke_color=color, stroke_width=sw),
        Line(c + DOWN * size, c + UP * size, stroke_color=color, stroke_width=sw),
    )


def build_battery_icon(center, scale=1.0, color=EDGE_MAGENTA):
    """Clean MAGENTA schematic battery glyph (long + short plates inside badge, NO +/- text)."""
    c = np.array(center, dtype=float)
    badge = RoundedRectangle(
        corner_radius=0.16 * scale, width=0.86 * scale, height=0.64 * scale,
        fill_color=BG, fill_opacity=0.94,
        stroke_color=color, stroke_width=3.6 * scale,
    ).move_to(c)
    lead_l = Line(c + LEFT * (0.34 * scale), c + LEFT * (0.11 * scale),
                  stroke_color=color, stroke_width=3.2 * scale)
    plate_l = Line(c + LEFT * (0.11 * scale) + DOWN * (0.12 * scale),
                   c + LEFT * (0.11 * scale) + UP * (0.12 * scale),
                   stroke_color=color, stroke_width=6.0 * scale)
    plate_r = Line(c + RIGHT * (0.11 * scale) + DOWN * (0.22 * scale),
                   c + RIGHT * (0.11 * scale) + UP * (0.22 * scale),
                   stroke_color=color, stroke_width=3.6 * scale)
    lead_r = Line(c + RIGHT * (0.11 * scale), c + RIGHT * (0.34 * scale),
                  stroke_color=color, stroke_width=3.2 * scale)
    return VGroup(badge, lead_l, plate_l, plate_r, lead_r)


def dipole_loop_points(origin, r_max, sign_y=1.0, n=48):
    """Exact dipole field line r = r_max * sin^2(theta) in the upper or lower half-plane."""
    thetas = np.linspace(0.08, np.pi - 0.08, n)
    ox, oy = origin[0], origin[1]
    pts = []
    for th in thetas:
        r = r_max * (np.sin(th) ** 2)
        pts.append(np.array([ox + r * np.cos(th), oy + sign_y * r * np.sin(th), 0.0]))
    return pts


def build_ecg_live_trace(fn, t_tracker, t_range=(0.0, 0.80), box=PAPER_BOX, base_y=BASE_Y,
                         amp=ECG_AMP, color=ECG_GREEN, sw=5.8, show_pen=True, show_cursor=True):
    """Live GREEN ECG trace drawing from t_range[0] to t_tracker with a bright pen dot and time cursor."""
    x0, x1, y0, y1 = box
    px0, px1 = x0 + 0.25, x1 - 0.25
    ta, tb = t_range

    def tx(t):
        return px0 + (t - ta) / max(tb - ta, 1e-6) * (px1 - px0)

    def ty(t):
        return base_y + amp * fn(t)

    def mk():
        tc = float(np.clip(t_tracker.get_value(), ta, tb))
        g = VGroup()
        cx = tx(tc)
        if show_cursor and show_pen:
            # Subtle oscilloscope/chart-recorder scan line moving strictly with the active ECG pen
            cursor = Line(
                [cx, y0 + 0.08, 0], [cx, y1 - 0.08, 0],
                stroke_color=color, stroke_width=2.6, stroke_opacity=0.24,
            )
            g.add(cursor)
        n = max(4, int(240 * (tc - ta) / max(tb - ta, 1e-6)) + 2)
        if tc > ta + 1e-5:
            ts = np.linspace(ta, tc, n)
            pts = [np.array([tx(u), ty(u), 0.0]) for u in ts]
            crv = VMobject(stroke_color=color, stroke_width=sw, fill_opacity=0)
            crv.set_points_as_corners(pts)
            g.add(crv)
        if show_pen:
            tip = np.array([cx, ty(tc), 0.0])
            glow = Dot(tip, radius=0.17, color=color, fill_opacity=0.40, stroke_width=0)
            pen = Dot(tip, radius=0.085, color=CELL_WHITE, stroke_color=color, stroke_width=3.2)
            g.add(glow, pen)
        return g

    return always_redraw(mk)


def ecg_pt(t, y_val, t_range=(0.0, 0.80), box=PAPER_BOX, base_y=BASE_Y, amp=ECG_AMP):
    x0, x1, _, _ = box
    px0, px1 = x0 + 0.25, x1 - 0.25
    ta, tb = t_range
    return np.array([
        px0 + (t - ta) / max(tb - ta, 1e-6) * (px1 - px0),
        base_y + amp * y_val,
        0.0,
    ])


# ------------------------------------------------------------------ Computed Tiled Heart Model
def _build_heart_spec():
    """Generate tiled myocardial cells for a clean schematic four-chamber heart centered at (0, 1.78).
    Each tile: (cx, cy, w, h, angle, t_act, t_rep_start, t_rep_dur)."""
    atrial = []
    sa = np.array([-1.42, 2.74])
    atrial_centers = [
        (-1.42, 2.74, 0.36, 0.30, 0.35),
        (-1.12, 2.98, 0.38, 0.28, 0.15),
        (-0.74, 3.06, 0.38, 0.28, -0.05),
        (-0.36, 2.98, 0.36, 0.28, -0.25),
        (-1.52, 2.40, 0.34, 0.32, 0.10),
        (-1.42, 2.10, 0.36, 0.28, -0.15),
        (-1.06, 2.04, 0.38, 0.26, 0.0),
        (-0.68, 2.05, 0.38, 0.26, 0.05),
        (-0.08, 2.74, 0.28, 0.34, 0.0),
        (0.08, 2.42, 0.28, 0.34, 0.0),
        (0.36, 2.98, 0.36, 0.28, 0.25),
        (0.74, 3.06, 0.38, 0.28, 0.05),
        (1.12, 2.98, 0.38, 0.28, -0.15),
        (1.42, 2.74, 0.36, 0.30, -0.35),
        (1.52, 2.40, 0.34, 0.32, -0.10),
        (1.42, 2.10, 0.36, 0.28, 0.15),
        (1.06, 2.04, 0.38, 0.26, 0.0),
        (0.68, 2.05, 0.38, 0.26, -0.05),
    ]
    dists = [np.linalg.norm(np.array([x, y]) - sa) for x, y, *_ in atrial_centers]
    d_max = max(dists)
    for (x, y, w, h, ang), d in zip(atrial_centers, dists):
        frac = d / max(d_max, 1e-6)
        t_act = 0.082 + 0.068 * frac
        t_rep = 0.245 + 0.055 * frac
        atrial.append((x, y, w, h, ang, t_act, t_rep, 0.035))

    # Ventricular myocardium: delayed t_rep (0.505..0.595) so EVERY ventricular tile is 100% pure GOLD during ST!
    vent = []
    septum_pts = [
        (0.0, 1.60, 0.34, 0.30, 0.0, 0.242, 0.560),
        (0.0, 1.30, 0.34, 0.30, 0.0, 0.248, 0.548),
        (0.0, 1.00, 0.36, 0.30, 0.0, 0.254, 0.536),
        (0.0, 0.70, 0.40, 0.30, 0.0, 0.260, 0.525),
        (0.0, 0.42, 0.46, 0.30, 0.0, 0.264, 0.512),
        (-0.42, 0.48, 0.42, 0.30, -0.25, 0.268, 0.506),
        (0.42, 0.48, 0.42, 0.30, 0.25, 0.268, 0.505),
    ]
    rv_pts = [
        (-0.82, 0.64, 0.42, 0.30, -0.45, 0.274, 0.514),
        (-1.18, 0.88, 0.42, 0.30, -0.68, 0.280, 0.528),
        (-1.44, 1.18, 0.38, 0.32, -0.95, 0.286, 0.545),
        (-1.60, 1.50, 0.36, 0.32, -1.25, 0.294, 0.568),
        (-1.58, 1.78, 0.36, 0.28, -1.45, 0.302, 0.588),
        (-0.66, 0.88, 0.36, 0.26, -0.55, 0.272, 0.544),
        (-1.02, 1.16, 0.36, 0.26, -0.85, 0.282, 0.562),
        (-1.24, 1.50, 0.34, 0.28, -1.20, 0.292, 0.580),
    ]
    lv_pts = [
        (0.84, 0.64, 0.44, 0.32, 0.45, 0.274, 0.508),
        (1.20, 0.88, 0.44, 0.32, 0.68, 0.281, 0.522),
        (1.48, 1.18, 0.40, 0.34, 0.95, 0.288, 0.542),
        (1.64, 1.50, 0.38, 0.34, 1.25, 0.296, 0.566),
        (1.62, 1.78, 0.38, 0.30, 1.45, 0.304, 0.592),
        (0.68, 0.88, 0.38, 0.28, 0.55, 0.273, 0.548),
        (1.06, 1.16, 0.38, 0.28, 0.85, 0.283, 0.568),
        (1.28, 1.50, 0.36, 0.30, 1.20, 0.294, 0.590),
    ]
    for x, y, w, h, ang, ta, tr in septum_pts + rv_pts + lv_pts:
        vent.append((x, y, w, h, ang, ta, tr, 0.048))

    av_path = [
        np.array([-0.28, 2.18, 0.0]),
        np.array([-0.10, 2.04, 0.0]),
        np.array([0.00, 1.88, 0.0]),
        np.array([0.00, 1.62, 0.0]),
    ]
    purkinje = [
        [np.array([0.0, 1.62, 0.0]), np.array([0.0, 0.66, 0.0])],
        [np.array([0.0, 0.66, 0.0]), np.array([-0.55, 0.68, 0.0]), np.array([-1.05, 1.05, 0.0]), np.array([-1.32, 1.58, 0.0])],
        [np.array([0.0, 0.66, 0.0]), np.array([0.55, 0.68, 0.0]), np.array([1.10, 1.05, 0.0]), np.array([1.36, 1.58, 0.0])],
    ]
    return {
        "atrial": atrial,
        "vent": vent,
        "sa": np.array([-1.42, 2.74, 0.0]),
        "av_path": av_path,
        "purkinje": purkinje,
    }


HEART_SPEC = _build_heart_spec()


def _tile_state(t, t_act, t_rep, rep_dur, act_dur=0.016, extra_plateau=0.0):
    """Return (depol_level in [0, 1], edge_up in [0, 1], edge_dn in [0, 1]) for one tile at beat time t."""
    up = 1.0 / (1.0 + np.exp(-(t - t_act) / (act_dur * 0.32)))
    down = 1.0 / (1.0 + np.exp(-(t - (t_rep + extra_plateau)) / (rep_dur * 0.28)))
    level = float(np.clip(up * (1.0 - down), 0.0, 1.0))
    edge_up = float(4.0 * up * (1.0 - up))
    edge_dn = float(4.0 * down * (1.0 - down))
    return level, edge_up, edge_dn


def _av_point(av_pts, frac):
    f = float(np.clip(frac, 0.0, 1.0))
    seg_n = len(av_pts) - 1
    u = f * seg_n
    idx = min(int(u), seg_n - 1)
    loc = u - idx
    return av_pts[idx] * (1.0 - loc) + av_pts[idx + 1] * loc


def build_heart_frame(t_beat, offset=ORIGIN, scale=1.04, show_sa_ready=False,
                      show_av_dot=False, av_frac=0.0, show_purkinje_flash=False,
                      show_atrial_edge=True, show_vent_edge=True, extra_plateau=0.0,
                      av_pulse=1.0, show_av_trail=False):
    """Build the tiled schematic heart at exact beat time t_beat."""
    off = np.array(offset, dtype=float)
    g = VGroup()

    # Anatomical chamber silhouettes (Polygon contours, matching vent_bg, so every tile stays cleanly inside)
    atria_bg = Polygon(
        [-1.92, 1.94, 0], [-1.96, 2.74, 0], [-1.36, 3.34, 0], [0.0, 3.22, 0],
        [1.36, 3.34, 0], [1.96, 2.74, 0], [1.92, 1.94, 0],
        fill_color=FLUID_BG, fill_opacity=0.80,
        stroke_color=FLUID_BORDER, stroke_width=2.2,
    ).round_corners(0.38)
    vent_bg = Polygon(
        [-1.96, 1.96, 0], [-1.86, 1.10, 0], [-1.14, 0.44, 0], [0.0, 0.14, 0],
        [1.16, 0.44, 0], [1.90, 1.10, 0], [2.00, 1.96, 0],
        fill_color=FLUID_BG, fill_opacity=0.80,
        stroke_color=FLUID_BORDER, stroke_width=2.2,
    ).round_corners(0.35)
    g.add(atria_bg, vent_bg)

    ins_l = Line([-1.84, 1.92, 0], [-0.26, 1.92, 0], stroke_color=INSULATOR_COL, stroke_width=5.5)
    ins_r = Line([0.26, 1.92, 0], [1.86, 1.92, 0], stroke_color=INSULATOR_COL, stroke_width=5.5)
    av_pts = HEART_SPEC["av_path"]
    av_ch = VMobject(stroke_color=FLUID_BORDER, stroke_width=7.0, stroke_opacity=0.90, fill_opacity=0)
    av_ch.set_points_as_corners(av_pts)
    g.add(ins_l, ins_r, av_ch)

    atrial_grp = VGroup()
    edge_glows = VGroup()
    for x, y, w, h, ang, ta, tr, rd in HEART_SPEC["atrial"]:
        lvl, eu, _ = _tile_state(t_beat, ta, tr, rd, act_dur=0.022)
        col = interpolate_color(ManimColor(REST_BLUE), ManimColor(PLATEAU_GOLD), lvl)
        tile = RoundedRectangle(
            corner_radius=0.09, width=w, height=h,
            fill_color=col, fill_opacity=0.88,
            stroke_color=col, stroke_width=2.2,
        ).rotate(ang).move_to([x, y, 0])
        atrial_grp.add(tile)
        if show_atrial_edge and eu > 0.18 and t_beat < 0.18:
            gl = RoundedRectangle(
                corner_radius=0.10, width=w + 0.06, height=h + 0.06,
                fill_color=EDGE_MAGENTA, fill_opacity=0.45 * eu,
                stroke_color=EDGE_MAGENTA, stroke_width=3.8 * eu,
            ).rotate(ang).move_to([x, y, 0])
            edge_glows.add(gl)

    vent_grp = VGroup()
    for x, y, w, h, ang, ta, tr, rd in HEART_SPEC["vent"]:
        lvl, eu, ed = _tile_state(t_beat, ta, tr, rd, act_dur=0.015, extra_plateau=extra_plateau)
        col = interpolate_color(ManimColor(REST_BLUE), ManimColor(PLATEAU_GOLD), lvl)
        tile = RoundedRectangle(
            corner_radius=0.09, width=w, height=h,
            fill_color=col, fill_opacity=0.88,
            stroke_color=col, stroke_width=2.2,
        ).rotate(ang).move_to([x, y, 0])
        vent_grp.add(tile)
        if show_vent_edge:
            if eu > 0.16 and 0.22 <= t_beat <= 0.35:
                gl = RoundedRectangle(
                    corner_radius=0.11, width=w + 0.08, height=h + 0.08,
                    fill_color=EDGE_MAGENTA, fill_opacity=0.58 * eu,
                    stroke_color=EDGE_MAGENTA, stroke_width=4.6 * eu,
                ).rotate(ang).move_to([x, y, 0])
                edge_glows.add(gl)
            elif ed > 0.14 and t_beat >= 0.47:
                # Broad, soft MAGENTA recovery band (NO direction arrow!)
                gl = RoundedRectangle(
                    corner_radius=0.12, width=w + 0.10, height=h + 0.10,
                    fill_color=EDGE_MAGENTA, fill_opacity=0.38 * ed,
                    stroke_color=EDGE_MAGENTA, stroke_width=3.4 * ed,
                ).rotate(ang).move_to([x, y, 0])
                edge_glows.add(gl)

    g.add(atrial_grp, vent_grp)

    purk_grp = VGroup()
    p_on = show_purkinje_flash and (0.235 <= t_beat <= 0.305)
    for path in HEART_SPEC["purkinje"]:
        pm = VMobject(
            stroke_color=EDGE_MAGENTA if p_on else TEXT,
            stroke_width=4.8 if p_on else 1.8,
            stroke_opacity=0.95 if p_on else 0.30,
            fill_opacity=0,
        )
        pm.set_points_as_corners(path)
        purk_grp.add(pm)
    g.add(purk_grp, edge_glows)

    if show_sa_ready:
        sa_pt = HEART_SPEC["sa"]
        sa_glow = Dot(sa_pt, radius=0.19, color=EDGE_MAGENTA, fill_opacity=0.40, stroke_width=0)
        sa_dot = Dot(sa_pt, radius=0.095, color=EDGE_MAGENTA, stroke_color=CELL_WHITE, stroke_width=2.0)
        g.add(sa_glow, sa_dot)

    if show_av_dot:
        if show_av_trail and av_frac > 0.02:
            trail_pts = [_av_point(av_pts, u) for u in np.linspace(0.0, av_frac, 16)]
            tr = VMobject(stroke_color=EDGE_MAGENTA, stroke_width=5.5, stroke_opacity=0.75, fill_opacity=0)
            tr.set_points_as_corners(trail_pts)
            g.add(tr)
        pos = _av_point(av_pts, av_frac)
        halo = Dot(pos, radius=0.17 * av_pulse, color=EDGE_MAGENTA, fill_opacity=0.42, stroke_width=0)
        core = Dot(pos, radius=0.095, color=EDGE_MAGENTA, stroke_color=CELL_WHITE, stroke_width=2.2)
        g.add(halo, core)

    if scale != 1.0:
        g.scale(scale, about_point=np.array([0.0, 1.72, 0.0]))
    if np.linalg.norm(off) > 1e-6:
        g.shift(off)
    return g


def live_heart(t_tracker, offset=ORIGIN, scale=1.04, show_sa_ready=False,
               show_av_dot=False, av_tracker=None, show_purkinje_flash=True,
               show_atrial_edge=True, show_vent_edge=True, extra_tracker=None,
               show_av_trail=False):
    return always_redraw(lambda: build_heart_frame(
        t_tracker.get_value(),
        offset=offset,
        scale=scale,
        show_sa_ready=show_sa_ready,
        show_av_dot=show_av_dot,
        av_frac=av_tracker.get_value() if av_tracker is not None else 0.0,
        show_purkinje_flash=show_purkinje_flash,
        show_atrial_edge=show_atrial_edge,
        show_vent_edge=show_vent_edge,
        extra_plateau=extra_tracker.get_value() if extra_tracker is not None else 0.0,
        show_av_trail=show_av_trail,
    ))


def h_bracket(x_left, x_right, y, tick=0.16, color=CELL_WHITE, sw=3.4):
    """Clean horizontal bracket below a wave (tips point UP toward the trace)."""
    return VGroup(
        Line([x_left, y + tick, 0], [x_left, y, 0], stroke_color=color, stroke_width=sw),
        Line([x_left, y, 0], [x_right, y, 0], stroke_color=color, stroke_width=sw),
        Line([x_right, y, 0], [x_right, y + tick, 0], stroke_color=color, stroke_width=sw),
    )


def ecg_wave_label(text, t_pos, y_val, t_range=(0.0, 0.80), box=PAPER_BOX, base_y=BASE_Y,
                   amp=ECG_AMP, dy=0.34, color=ECG_GREEN, size=30):
    pt = ecg_pt(t_pos, y_val, t_range=t_range, box=box, base_y=base_y, amp=amp)
    lbl = T(text, size=size, color=color, weight=BOLD).move_to(pt + UP * dy)
    return label_plate(lbl, pad_x=0.10, pad_y=0.05)


# ------------------------------------------------------------------ Helper Mixin for Smooth Sync
class FilmScene(SpokenScene):
    def advance_to(self, phrase, *anims, lead=0.2, rate_func=linear, min_dt=0.12):
        """Play animations continuously right up to `phrase`, then log exact sync via self.at()."""
        target = self.t_of(phrase) - lead
        dt = target - self.elapsed()
        if dt > min_dt and anims:
            self.play(*anims, run_time=dt, rate_func=rate_func)
        elif anims:
            self.play(*anims, run_time=min_dt, rate_func=rate_func)
        self.at(phrase, lead=lead)


# ================================================================== SCENES 00 - 22

class S00LinkAndQuestion(FilmScene):
    """Hook: one cell held its plateau; now all 10 ventricular cells sit on plateau, yet ECG is flat. Why?"""
    def construct(self):
        depol = ValueTracker(0.0)
        t_ap = ValueTracker(-35.0)
        t_ecg = ValueTracker(0.0)

        paper = build_ecg_paper()
        electrode = build_electrode(center=(0.0, 2.78, 0.0), scale=0.92)
        tag = tag_schematic()

        strip = always_redraw(lambda: build_cell_strip(
            states=np.full(STRIP_N, depol.get_value()),
        ))
        # Larger, clearer single-cell inset drawing live up phase 0 and across the gold plateau!
        inset = always_redraw(lambda: build_ap_inset(
            box=(-6.1, -2.85, 2.22, 3.52),
            t_dot_ms=t_ap.get_value(),
            draw_live=True,
            highlight_plateau_to=t_ap.get_value(),
        ))
        trace = build_ecg_live_trace(lambda u: 0.0, t_ecg, t_range=(0.0, 1.0))

        self.add(paper, electrode, strip, inset, trace, tag)

        # 0.00 -> 1.60: single cell enters phase 0 upstroke while pen runs level
        self.advance_to(
            "one ventricular cell",
            t_ap.animate.set_value(12.0),
            t_ecg.animate.set_value(0.14),
        )
        # 1.60 -> 5.18: single cell draws its full gold plateau while pen runs level
        self.advance_to(
            "nearly every",
            t_ap.animate.set_value(200.0),
            t_ecg.animate.set_value(0.38),
        )
        # 5.18 -> 8.28: all 10 cells depolarize from BLUE to GOLD together while trace stays level
        self.advance_to(
            "far above rest",
            depol.animate.set_value(1.0),
            t_ap.animate.set_value(212.0),
            t_ecg.animate.set_value(0.62),
        )
        # 8.28 -> 10.74: all 10 sit high on plateau; pen sweeps across ECG paper dead level
        self.advance_to(
            "tracing on the skin",
            t_ap.animate.set_value(220.0),
            t_ecg.animate.set_value(0.79),
        )
        # 10.74 -> 13.46: pen sweeps to right end dead level
        self.advance_to(
            "why",
            t_ap.animate.set_value(222.0),
            t_ecg.animate.set_value(0.93),
        )
        q_text = T("All depolarized. Flat. Why?", size=34, color=CELL_WHITE, weight=BOLD).move_to([-0.5, -3.12, 0])
        self.play(
            FadeIn(q_text, shift=UP * 0.08),
            t_ecg.animate.set_value(0.97),
            run_time=0.40,
        )
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(t_ecg.animate.set_value(1.0), run_time=rem, rate_func=linear)
        self.finish()


class S01Title(NarratedScene):
    """2 s title overlay above the strip while the level GREEN trace keeps running."""
    def construct(self):
        paper = build_ecg_paper()
        strip = build_cell_strip(states=np.ones(STRIP_N))
        tag = tag_schematic()
        t_ecg = ValueTracker(0.08)
        trace = build_ecg_live_trace(lambda u: 0.0, t_ecg, t_range=(0.0, 1.0), show_cursor=False)

        q_text = T("All depolarized. Flat. Why?", size=34, color=CELL_WHITE, weight=BOLD).move_to([-0.5, -3.12, 0])
        title = T("The Edges of the Wave", size=48, font=TITLE_FONT, color=CELL_WHITE).move_to([0.0, 2.94, 0])
        rule = Line([-2.2, 2.50, 0], [2.2, 2.50, 0], stroke_color=PLATEAU_GOLD, stroke_width=4.0)

        self.add(paper, strip, trace, tag, q_text)
        self.play(
            FadeOut(q_text, run_time=0.45),
            FadeIn(title, shift=UP * 0.1, run_time=0.55),
            GrowFromCenter(rule, run_time=0.55),
            t_ecg.animate(run_time=0.65, rate_func=linear).set_value(0.45),
        )
        rem = max(0.2, self.narration_s - self.elapsed())
        self.play(t_ecg.animate.set_value(0.96), run_time=rem, rate_func=linear)
        self.finish()


class S02Guess(FilmScene):
    """Ten small WHITE plateau traces stack into a tall WHITE sum curve, then get crossed out."""
    def construct(self):
        paper = build_ecg_paper()
        electrode = build_electrode(center=(0.0, 2.78, 0.0), scale=0.92)
        strip = build_cell_strip(states=np.ones(STRIP_N))
        tag = tag_schematic()

        t_ecg = ValueTracker(0.08)
        trace = build_ecg_live_trace(lambda u: 0.0, t_ecg, t_range=(0.0, 1.0), show_cursor=False)
        real_lbl = label_plate(
            T("real trace", size=28, color=ECG_GREEN, weight=BOLD).move_to([-4.55, -2.18, 0]),
            pad_x=0.10, pad_y=0.05,
        )

        ts = np.linspace(-30.0, 350.0, 120)
        mini_traces = VGroup()
        for x in strip.xs:
            pts = [
                np.array([
                    x - 0.36 + (t + 30.0) / 380.0 * 0.72,
                    STRIP_Y - 0.28 + ap_norm(t, 200.0) * 0.56,
                    0.0,
                ])
                for t in ts
            ]
            c = VMobject(stroke_color=CELL_WHITE, stroke_width=2.8, fill_opacity=0)
            c.set_points_as_corners(pts)
            mini_traces.add(c)

        x0, x1, _, _ = PAPER_BOX
        px0, px1 = x0 + 0.35, x1 - 0.35
        sum_pts = [
            np.array([
                px0 + (t + 30.0) / 380.0 * (px1 - px0),
                BASE_Y + 1.24 * ap_norm(t, 200.0),
                0.0,
            ])
            for t in ts
        ]
        sum_curve = VMobject(stroke_color=CELL_WHITE, stroke_width=5.5, fill_opacity=0)
        sum_curve.set_points_as_corners(sum_pts)
        # Placed cleanly to the right of the cross so cross strikes ONLY the white curve (0 layout_ok needed!)
        sum_lbl = label_plate(
            T("sum of cells", size=28, color=CELL_WHITE, weight=BOLD).move_to([3.55, -0.60, 0]),
            pad_x=0.10, pad_y=0.05,
        )
        cross = VGroup(
            Line([-2.4, -1.52, 0], [0.2, -0.56, 0], stroke_color=CELL_WHITE, stroke_width=7.5),
            Line([-2.4, -0.56, 0], [0.2, -1.52, 0], stroke_color=CELL_WHITE, stroke_width=7.5),
        )

        self.add(paper, electrode, strip, trace, real_lbl, tag)

        self.advance_to(
            "says the ecg",
            FadeIn(mini_traces, shift=UP * 0.15),
            t_ecg.animate.set_value(0.24),
        )
        self.advance_to(
            "action potentials added up",
            mini_traces.animate.shift(UP * 0.20),
            t_ecg.animate.set_value(0.42),
        )
        self.play(
            ReplacementTransform(mini_traces, sum_curve),
            t_ecg.animate.set_value(0.58),
            run_time=1.05,
        )
        self.play(FadeIn(sum_lbl), t_ecg.animate.set_value(0.62), run_time=0.35)
        t_sum = ValueTracker(25.0)
        sum_dot = always_redraw(lambda: Dot(
            np.array([
                px0 + (t_sum.get_value() + 30.0) / 380.0 * (px1 - px0),
                BASE_Y + 1.24 * ap_norm(t_sum.get_value(), 200.0),
                0.0,
            ]),
            radius=0.10, color=PLATEAU_GOLD, stroke_color=CELL_WHITE, stroke_width=2.5,
        ))
        self.add(sum_dot)
        self.advance_to(
            "stay high",
            t_sum.animate.set_value(130.0),
            t_ecg.animate.set_value(0.76),
        )
        self.advance_to(
            "plateau",
            t_sum.animate.set_value(220.0),
            t_ecg.animate.set_value(0.88),
        )
        self.play(Create(cross), t_ecg.animate.set_value(0.93), run_time=0.35)
        self.play(
            FadeOut(sum_curve), FadeOut(sum_lbl), FadeOut(sum_dot), FadeOut(cross),
            t_ecg.animate.set_value(1.0),
            run_time=0.75,
        )
        self.finish()


class S03Electrode(FilmScene):
    """Zoom on chest electrode, fluid, and neighboring cells: MAGENTA dipole loops appear ONLY when voltages differ."""
    def construct(self):
        c_left_v = ValueTracker(0.0)
        c_right_v = ValueTracker(0.0)
        phase = ValueTracker(0.0)
        tag = tag_schematic()

        init_strip = build_cell_strip(states=np.ones(STRIP_N))
        init_paper = build_ecg_paper()
        init_el = build_electrode(center=(0.0, 2.78, 0.0), scale=0.92)
        self.add(init_paper, init_el, init_strip, tag)

        # Brisk GOLD->BLUE and zoom so 'cannot record' (1.70 s) lands right on time
        blue_strip = build_cell_strip(states=np.zeros(STRIP_N))
        self.play(ReplacementTransform(init_strip, blue_strip), run_time=0.50)

        z_cell_y = -1.25
        z_cell_w = 2.45
        z_cell_h = 1.60
        z_gap = 0.16
        z_xs = strip_cell_xs(4, z_cell_w, z_gap, cx=0.0)

        fluid_band = RoundedRectangle(
            corner_radius=0.22, width=11.6, height=4.45,
            fill_color=FLUID_BG, fill_opacity=0.92,
            stroke_color=FLUID_BORDER, stroke_width=2.2,
        ).move_to([0.0, 0.15, 0])
        z_electrode = build_electrode(center=(0.0, 2.68, 0.0), scale=1.22)
        fluid_lbl = T("fluid around cells", size=26, color=TEXT).move_to([-4.2, 1.85, 0])

        def mk_z_cells():
            vs = [0.0, c_left_v.get_value(), c_right_v.get_value(), 0.0]
            grp = VGroup()
            for i in range(3):
                jx = (z_xs[i] + z_xs[i + 1]) / 2.0
                for dy in (-0.34, 0.34):
                    grp.add(Line(
                        [jx - 0.14, z_cell_y + dy, 0], [jx + 0.14, z_cell_y + dy, 0],
                        stroke_color=TEXT, stroke_width=4.0, stroke_opacity=0.8,
                    ))
            for x, v in zip(z_xs, vs):
                col = interpolate_color(ManimColor(REST_BLUE), ManimColor(PLATEAU_GOLD), float(np.clip(v, 0, 1)))
                grp.add(RoundedRectangle(
                    corner_radius=0.18, width=z_cell_w, height=z_cell_h,
                    fill_color=col, fill_opacity=0.88,
                    stroke_color=col, stroke_width=3.6,
                ).move_to([x, z_cell_y, 0]))
            return grp

        def mk_dipole_loops():
            diff = abs(c_left_v.get_value() - c_right_v.get_value())
            grp = VGroup()
            if diff < 0.04:
                return grp
            origin = np.array([0.0, z_cell_y + z_cell_h * 0.42, 0.0])
            for idx, r_max in enumerate((1.15, 2.05, 2.95)):
                pts = dipole_loop_points(origin, r_max, sign_y=1.0, n=52)
                loop = VMobject(
                    stroke_color=EDGE_MAGENTA,
                    stroke_width=(4.2 - 0.6 * idx) * diff,
                    stroke_opacity=(0.90 - 0.14 * idx) * diff,
                    fill_opacity=0,
                )
                loop.set_points_as_corners(pts)
                grp.add(loop)
                ph = phase.get_value()
                for b in range(3):
                    u = (ph * 0.65 + b / 3.0 + idx * 0.13) % 1.0
                    k = int(u * (len(pts) - 1))
                    grp.add(Dot(
                        pts[k], radius=0.075, color=EDGE_MAGENTA,
                        fill_opacity=0.95 * diff, stroke_width=0,
                    ))
            return grp

        z_cells = always_redraw(mk_z_cells)
        loops = always_redraw(mk_dipole_loops)

        self.play(
            FadeOut(init_paper),
            ReplacementTransform(init_el, z_electrode),
            FadeOut(blue_strip),
            FadeIn(fluid_band),
            FadeIn(z_cells),
            run_time=0.75,
        )
        self.add(loops)

        el_lbl = T("chest electrode", size=28, color=TEXT).next_to(z_electrode, RIGHT, buff=0.35)
        self.at("cannot record")
        self.play(FadeIn(el_lbl, shift=LEFT * 0.1), run_time=0.6)
        self.advance_to("what reaches it", FadeIn(fluid_lbl), phase.animate.set_value(0.5))

        self.play(c_left_v.animate.set_value(1.0), phase.animate.set_value(1.6), run_time=1.0)
        self.advance_to("that current flows", phase.animate.set_value(3.2))

        rule_lbl = T("different voltages, current flows", size=30, color=EDGE_MAGENTA, weight=BOLD).move_to([-0.6, -2.95, 0])
        self.play(FadeIn(rule_lbl, shift=UP * 0.1), phase.animate.set_value(3.6), run_time=0.5)
        self.play(c_right_v.animate.set_value(1.0), phase.animate.set_value(4.2), run_time=0.8)
        self.wait(0.35)
        self.at("differ in voltage")
        self.play(c_right_v.animate.set_value(0.0), phase.animate.set_value(5.2), run_time=0.85)
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(phase.animate.set_value(5.2 + rem * 1.1), run_time=rem, rate_func=linear)
        self.finish()


class S04Boundary(FilmScene):
    """Pull back to full 10-cell strip; wave travels halfway (left 5 GOLD 'plateau', right 5 BLUE 'rest')."""
    def construct(self):
        front = ValueTracker(-1.2)
        t_ecg = ValueTracker(0.0)
        paper = build_ecg_paper()
        electrode = build_electrode(center=(0.0, 2.78, 0.0), scale=0.92)
        tag = tag_schematic()

        strip = always_redraw(lambda: build_cell_strip(
            states=strip_cell_states(front.get_value()),
        ))

        def ecg_fn(u):
            fp = -1.2 + (u / 0.45) * 6.2 if u <= 0.45 else 5.0
            return 0.65 * strip_dipole_ecg(fp)

        trace = build_ecg_live_trace(ecg_fn, t_ecg, t_range=(0.0, 1.0))

        b_line = Line(
            [0.0, STRIP_Y - CELL_H / 2 - 0.16, 0],
            [0.0, STRIP_Y + CELL_H / 2 + 0.16, 0],
            stroke_color=EDGE_MAGENTA, stroke_width=6.0,
        )
        b_glow = Line(
            [0.0, STRIP_Y - CELL_H / 2 - 0.20, 0],
            [0.0, STRIP_Y + CELL_H / 2 + 0.20, 0],
            stroke_color=EDGE_MAGENTA, stroke_width=14.0, stroke_opacity=0.32,
        )

        plat_lbl = T("plateau", size=32, color=PLATEAU_GOLD, weight=BOLD).move_to([-2.9, 2.52, 0])
        rest_lbl = T("rest", size=32, color=REST_BLUE, weight=BOLD).move_to([2.9, 2.52, 0])
        plat_span = Line([-5.56, 2.18, 0], [-0.08, 2.18, 0], stroke_color=PLATEAU_GOLD, stroke_width=5.5)
        rest_span = Line([0.08, 2.18, 0], [5.56, 2.18, 0], stroke_color=REST_BLUE, stroke_width=5.5)

        self.add(paper, electrode, strip, trace, tag)

        # 0.00 -> 2.06: strip at rest, pen runs across flat baseline
        self.advance_to("wave halfway", t_ecg.animate.set_value(0.14))
        # 2.06 -> 4.78: wave sweeps cleanly across cells 1..5 turning them pure GOLD
        self.advance_to("behind the wave", front.animate.set_value(5.0), t_ecg.animate.set_value(0.45))
        # 4.78 -> 8.12: draw GOLD span over left 5 cells + 'plateau' + bright MAGENTA boundary line
        self.play(
            Create(plat_span), FadeIn(plat_lbl, shift=DOWN * 0.1), FadeIn(b_glow), Create(b_line),
            t_ecg.animate.set_value(0.62),
            run_time=1.35,
        )
        self.advance_to("ahead", t_ecg.animate.set_value(0.78))
        # 8.12 -> end: draw BLUE span over right 5 cells + 'rest' while pen finishes across paper
        self.play(
            Create(rest_span), FadeIn(rest_lbl, shift=DOWN * 0.1),
            t_ecg.animate.set_value(0.90),
            run_time=1.15,
        )
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(t_ecg.animate.set_value(0.98), run_time=rem, rate_func=linear)
        self.finish()


class S05Battery(FilmScene):
    """The boundary is a travelling battery: the junction (plus charges, then the MAGENTA circuit, then the
    battery icon) moves with the wave edge the whole time, turning each BLUE cell GOLD as it passes, and the
    GREEN pen deflects only while that boundary is inside the strip, returning level at the far end."""
    def construct(self):
        L = self.narration_s + 0.4
        clk = ValueTracker(0.0)
        clk.add_updater(lambda m, dt: m.increment_value(dt))

        t_bat = min(self.t_of("small battery"), L - 2.6)          # battery condenses here
        t_chg = self.t_of("positive charge")
        t_cir = self.t_of("circuit closes")

        def front_at(s):
            return float(np.interp(s, [0.0, t_bat, L], [5.0, 8.0, 11.4]))

        def front_x(fp):
            return -STRIP_SPAN / 2.0 + (fp / STRIP_N) * STRIP_SPAN

        def jx():
            return float(np.clip(front_x(front_at(clk.get_value())), -STRIP_SPAN / 2.0, STRIP_SPAN / 2.0))

        class _Pen:
            def get_value(self):
                return clk.get_value() / L

        paper = build_ecg_paper()
        electrode = build_electrode(center=(0.0, 2.78, 0.0), scale=0.92)
        tag = tag_schematic()

        strip = always_redraw(lambda: build_cell_strip(
            states=strip_cell_states(front_at(clk.get_value())),
        ))

        def ecg_fn(u):
            s = u * L
            ramp = float(np.clip((u - 0.04) / 0.12, 0.0, 1.0))
            ramp = 0.5 * (1.0 - np.cos(np.pi * ramp))
            return 0.68 * ramp * strip_dipole_ecg(front_at(s))

        trace = build_ecg_live_trace(ecg_fn, _Pen(), t_range=(0.0, 1.0))

        def cond():   # 0 -> 1 as the junction condenses into the battery
            return float(np.clip((clk.get_value() - t_bat) / 0.8, 0.0, 1.0))

        def mk_line():
            c = cond()
            if c >= 0.99:
                return VGroup()
            x = jx()
            return VGroup(
                Line([x, STRIP_Y - CELL_H / 2 - 0.16, 0], [x, STRIP_Y + CELL_H / 2 + 0.16, 0],
                     stroke_color=EDGE_MAGENTA, stroke_width=6.0, stroke_opacity=1.0 - c),
            )
        b_line = always_redraw(mk_line)

        def mk_pluses():
            s = clk.get_value()
            fade = float(np.clip((s - t_chg) / 0.5, 0.0, 1.0)) * (1.0 - cond())
            g = VGroup()
            if fade < 0.03:
                return g
            x0 = jx()
            for row, dy in enumerate((-0.34, -0.11, 0.11, 0.34)):
                for k in range(2):
                    u = ((s - t_chg) * 0.36 + row * 0.25 + k * 0.5) % 1.0
                    x = x0 - 0.82 + u * 1.64
                    op = float(np.sin(np.pi * u)) * fade
                    g.add(build_plus_mark([x, STRIP_Y + dy, 0], size=0.14, sw=4.2).set_opacity(op))
            return g
        pluses = always_redraw(mk_pluses)

        def mk_circuit():
            s = clk.get_value()
            grow = float(np.clip((s - t_cir) / 1.0, 0.0, 1.0))
            fade = 1.0 - cond()
            g = VGroup()
            if grow < 0.03 or fade < 0.03:
                return g
            x0 = jx()
            for (oy, r, sgn, sw, op0) in ((STRIP_Y + 0.28, 0.82, 1.0, 5.4, 1.0), (STRIP_Y - 0.28, 0.82, -1.0, 5.4, 1.0),
                                          (STRIP_Y + 0.28, 0.52, 1.0, 3.6, 0.8), (STRIP_Y - 0.28, 0.52, -1.0, 3.6, 0.8)):
                pts = dipole_loop_points([x0, oy, 0.0], r, sign_y=sgn, n=44)
                pts = pts[:max(2, int(len(pts) * grow))]
                g.add(VMobject(stroke_color=EDGE_MAGENTA, stroke_width=sw, stroke_opacity=op0 * fade,
                               fill_opacity=0).set_points_as_corners(pts))
            if grow > 0.99:
                top = dipole_loop_points([x0, STRIP_Y + 0.28, 0.0], 0.82, sign_y=1.0, n=44)
                bot = dipole_loop_points([x0, STRIP_Y - 0.28, 0.0], 0.82, sign_y=-1.0, n=44)
                ph = (s - t_cir - 1.0) * 0.30
                for k in range(3):
                    g.add(Dot(top[int((1.0 - ((ph + k / 3.0) % 1.0)) * (len(top) - 1))], radius=0.10,
                              color=EDGE_MAGENTA, stroke_color=CELL_WHITE, stroke_width=1.5).set_opacity(fade))
                    g.add(Dot(bot[int((1.0 - ((ph + 0.16 + k / 3.0) % 1.0)) * (len(bot) - 1))], radius=0.10,
                              color=EDGE_MAGENTA, stroke_color=CELL_WHITE, stroke_width=1.5).set_opacity(fade))
            return g
        circuit = always_redraw(mk_circuit)

        def mk_batt():
            c = cond()
            op = float(np.clip(strip_dipole_ecg(front_at(clk.get_value())) * 1.4, 0.0, 1.0)) * c
            if op < 0.04:
                return VGroup()
            return build_battery_icon([jx(), STRIP_Y, 0.0], scale=1.05).set_opacity(op)
        batt = always_redraw(mk_batt)

        self.add(clk, paper, electrode, strip, b_line, pluses, circuit, batt, trace, tag)

        self.at("small battery", lead=0.0)
        batt_lbl = T("moving boundary", size=28, color=EDGE_MAGENTA, weight=BOLD).move_to([3.0, 2.48, 0])
        self.play(FadeIn(batt_lbl, shift=DOWN * 0.1), run_time=0.6)
        self.at("traveling with the wave")
        rem = max(0.1, L - self.elapsed())
        self.wait(rem)
        self.finish()


class S06HoldBattery(NarratedScene):
    """6 s silent hold: MAGENTA battery travels the FULL length of the strip from cell 1 to 10;
    GREEN trace moves ONLY while it travels, then runs level."""
    def construct(self):
        u = ValueTracker(0.0)
        paper = build_ecg_paper()
        electrode = build_electrode(center=(0.0, 2.78, 0.0), scale=0.92)
        tag = tag_schematic()

        def front_of(val):
            if val < 0.14:
                return -1.4
            if val < 0.80:
                return -1.4 + ((val - 0.14) / 0.66) * 12.8
            return 11.4

        def front_x(fp):
            return -STRIP_SPAN / 2.0 + (fp / STRIP_N) * STRIP_SPAN

        strip = always_redraw(lambda: build_cell_strip(
            states=strip_cell_states(front_of(u.get_value())),
        ))

        def mk_batt_and_lbl():
            fp = front_of(u.get_value())
            op = float(np.clip(strip_dipole_ecg(fp) * 1.4, 0.0, 1.0))
            if op < 0.04:
                return VGroup()
            bx = np.clip(front_x(fp), -STRIP_SPAN / 2.0, STRIP_SPAN / 2.0)
            b = build_battery_icon([bx, STRIP_Y, 0.0], scale=1.05).set_opacity(op)
            lbl = T("moving boundary", size=28, color=EDGE_MAGENTA, weight=BOLD).move_to([3.0, 2.48, 0]).set_opacity(op)
            return VGroup(b, lbl)

        live_batt = always_redraw(mk_batt_and_lbl)
        trace = build_ecg_live_trace(
            lambda val: 0.72 * strip_dipole_ecg(front_of(val)),
            u, t_range=(0.0, 1.0),
        )

        self.add(paper, electrode, strip, live_batt, trace, tag)
        self.play(u.animate.set_value(1.0), run_time=self.narration_s, rate_func=linear)
        self.finish()


def _build_three_idea_panels(phase_tracker):
    """Three side-by-side frames for s07_idea and s08_hold_idea (rebuilt identically across both)."""
    xs = (-4.25, 0.0, 4.25)
    pw, ph = 3.85, 4.35
    cy = -0.05
    titles = ("all at rest", "moving edge", "all on plateau")
    colors = (REST_BLUE, EDGE_MAGENTA, PLATEAU_GOLD)

    frames = VGroup()
    heads = VGroup()
    strips = VGroup()
    papers = VGroup()
    traces = VGroup()

    for idx, (cx, ttl, col) in enumerate(zip(xs, titles, colors)):
        fr = RoundedRectangle(
            corner_radius=0.18, width=pw, height=ph,
            fill_color=BG, fill_opacity=0.95,
            stroke_color=col, stroke_width=2.8,
        ).move_to([cx, cy, 0])
        frames.add(fr)

        hd = T(ttl, size=28, color=col, weight=BOLD).move_to([cx, cy + ph / 2.0 - 0.38, 0])
        heads.add(hd)

        pbox = (cx - pw / 2.0 + 0.22, cx + pw / 2.0 - 0.22, cy - ph / 2.0 + 0.24, cy - 0.28)
        pbase = cy - ph / 2.0 + 0.62
        mp = build_ecg_paper(box=pbox, base_y=pbase, grid_nx=8, grid_ny=3)
        papers.add(mp)

        sy = cy + 0.68
        cw, ch, cg = 0.29, 0.58, 0.03
        if idx == 0:
            st = build_cell_strip(states=np.zeros(STRIP_N), y=sy, cell_w=cw, cell_h=ch, gap=cg, cx=cx, show_fluid=False)
            strips.add(st)
            tr = build_ecg_live_trace(lambda u: 0.0, phase_tracker, t_range=(0.0, 1.0), box=pbox, base_y=pbase, amp=0.72, sw=4.6)
            traces.add(tr)
        elif idx == 1:
            def _fp(u):
                return -1.2 + u * 12.4

            def _mk_mid(cx=cx, sy=sy, cw=cw, ch=ch, cg=cg):
                fp = _fp(phase_tracker.get_value())
                s_mob = build_cell_strip(states=strip_cell_states(fp), y=sy, cell_w=cw, cell_h=ch, gap=cg, cx=cx, show_fluid=False)
                span = STRIP_N * cw + (STRIP_N - 1) * cg
                bx = cx - span / 2.0 + (fp / STRIP_N) * span
                op = float(np.clip(strip_dipole_ecg(fp) * 1.4, 0.0, 1.0))
                if op < 0.05:
                    return s_mob
                bt = build_battery_icon([np.clip(bx, cx - span / 2.0, cx + span / 2.0), sy, 0.0], scale=0.58).set_opacity(op)
                return VGroup(s_mob, bt)

            strips.add(always_redraw(_mk_mid))
            tr = build_ecg_live_trace(
                lambda u: 0.78 * strip_dipole_ecg(-1.2 + u * 12.4),
                phase_tracker, t_range=(0.0, 1.0), box=pbox, base_y=pbase, amp=0.82, sw=4.6,
            )
            traces.add(tr)
        else:
            st = build_cell_strip(states=np.ones(STRIP_N), y=sy, cell_w=cw, cell_h=ch, gap=cg, cx=cx, show_fluid=False)
            strips.add(st)
            tr = build_ecg_live_trace(lambda u: 0.0, phase_tracker, t_range=(0.0, 1.0), box=pbox, base_y=pbase, amp=0.72, sw=4.6)
            traces.add(tr)

    return frames, heads, strips, papers, traces


class S07Idea(FilmScene):
    """The one idea: three side-by-side panels (all BLUE level; half/half moving edge; all GOLD level)."""
    def construct(self):
        ph = ValueTracker(0.0)
        frames, heads, strips, papers, traces = _build_three_idea_panels(ph)
        tag = tag_schematic()
        heading = T("It sees the edges.", size=46, font=TITLE_FONT, color=CELL_WHITE).move_to([0.0, 2.95, 0])

        self.add(frames, heads, papers, strips, traces, tag)

        self.advance_to("the ecg", ph.animate.set_value(0.32))

        hi_l = frames[0].copy().set_stroke(CELL_WHITE, width=5.5).set_fill(opacity=0)
        hi_r = frames[2].copy().set_stroke(CELL_WHITE, width=5.5).set_fill(opacity=0)
        self.play(FadeIn(hi_l), FadeIn(hi_r), ph.animate.set_value(0.50), run_time=0.8)
        self.advance_to("only differences", ph.animate.set_value(0.74))

        hi_m = frames[1].copy().set_stroke(EDGE_MAGENTA, width=6.5).set_fill(opacity=0)
        self.play(FadeOut(hi_l), FadeOut(hi_r), FadeIn(hi_m), ph.animate.set_value(0.84), run_time=0.65)
        self.advance_to("sees the edges", ph.animate.set_value(0.92))

        self.play(Write(heading), ph.animate.set_value(1.0), run_time=0.9)
        ph.set_value(0.05)
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(ph.animate.set_value(0.30), run_time=rem, rate_func=linear)
        self.finish()


class S08HoldIdea(NarratedScene):
    """4 s silent hold: highlight passes cleanly across the three frames in turn (fade out/in, never crossing text)."""
    def construct(self):
        ph = ValueTracker(0.05)
        frames, heads, strips, papers, traces = _build_three_idea_panels(ph)
        tag = tag_schematic()
        heading = T("It sees the edges.", size=46, font=TITLE_FONT, color=CELL_WHITE).move_to([0.0, 2.95, 0])

        hi0 = frames[0].copy().set_stroke(CELL_WHITE, width=6.2).set_fill(opacity=0)
        hi1 = frames[1].copy().set_stroke(EDGE_MAGENTA, width=6.8).set_fill(opacity=0)
        hi2 = frames[2].copy().set_stroke(PLATEAU_GOLD, width=6.2).set_fill(opacity=0)

        self.add(frames, heads, papers, strips, traces, heading, tag, hi0)
        seg = self.narration_s / 3.0
        self.play(ph.animate.set_value(0.36), run_time=seg, rate_func=linear)
        self.play(FadeOut(hi0, run_time=0.25), FadeIn(hi1, run_time=0.25), ph.animate(run_time=seg, rate_func=linear).set_value(0.70))
        self.play(FadeOut(hi1, run_time=0.25), FadeIn(hi2, run_time=0.25), ph.animate(run_time=seg, rate_func=linear).set_value(1.00))
        self.finish()


class S09PWave(FilmScene):
    """Strip morphs into schematic heart (all BLUE, MAGENTA boundary ready at SA node).
    Trace runs flat at rest, then MAGENTA edge sweeps atria turning them GOLD as GREEN pen draws P wave."""
    def construct(self):
        t_beat = ValueTracker(0.0)
        paper = build_ecg_paper()
        tag = tag_schematic()

        init_strip = build_cell_strip(states=np.zeros(STRIP_N))
        heart_0 = build_heart_frame(0.0, show_sa_ready=False)
        self.add(paper, init_strip, tag)
        self.play(ReplacementTransform(init_strip, heart_0), run_time=4.4)

        self.remove(heart_0)
        sa_on = ValueTracker(0.0)
        heart = always_redraw(lambda: build_heart_frame(
            t_beat.get_value(),
            show_sa_ready=(sa_on.get_value() > 0.5),
            show_atrial_edge=True,
            show_vent_edge=False,
        ))
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        atria_lbl = T("atria", size=28, color=TEXT).move_to([2.85, 2.74, 0])
        vent_lbl = T("ventricles", size=28, color=TEXT).move_to([3.15, 1.05, 0])
        self.add(heart, trace)

        self.advance_to("at first", FadeIn(atria_lbl), FadeIn(vent_lbl), t_beat.animate.set_value(0.025), lead=0.0)
        self.advance_to("trace is flat", t_beat.animate.set_value(0.060), lead=0.0)
        # SA node sparks, then the edge sweeps the atria across the whole last two sentences
        sa_on.set_value(1.0)
        self.advance_to("then", t_beat.animate.set_value(0.082), lead=0.0)
        sa_on.set_value(0.0)
        self.advance_to("atria", t_beat.animate.set_value(0.114), lead=0.0)
        self.advance_to("p wave", t_beat.animate.set_value(0.146), lead=0.0)

        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        self.play(FadeIn(p_lbl, shift=UP * 0.08), t_beat.animate.set_value(0.150), run_time=0.60)
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(t_beat.animate.set_value(0.154), run_time=rem, rate_func=linear)
        self.finish()


class S10HoldPWave(NarratedScene):
    """4 s silent hold: second half of atria finishes turning GOLD and GREEN pen settles onto baseline after P."""
    def construct(self):
        t_beat = ValueTracker(0.154)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(t_beat, show_atrial_edge=True, show_vent_edge=False)
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        atria_lbl = T("atria", size=28, color=PLATEAU_GOLD).move_to([2.85, 2.74, 0])
        vent_lbl = T("ventricles", size=28, color=TEXT).move_to([3.15, 1.05, 0])
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)

        self.add(paper, heart, trace, atria_lbl, vent_lbl, p_lbl, tag)
        self.play(t_beat.animate.set_value(0.175), run_time=self.narration_s, rate_func=linear)
        self.finish()


class S11Predict(FilmScene):
    """Small MAGENTA dot creeps down AV node & bundle of His; GREEN pen pauses after P; question card appears."""
    def construct(self):
        t_beat = ValueTracker(0.175)
        av_pos = ValueTracker(0.0)
        h_scale = ValueTracker(1.04)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = always_redraw(lambda: build_heart_frame(
            t_beat.get_value(),
            scale=h_scale.get_value(),
            show_av_dot=True, av_frac=av_pos.get_value(),
            show_atrial_edge=False, show_vent_edge=False,
            show_av_trail=True,
        ))
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80), show_cursor=False)
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)

        av_lbl = T("AV node,\nbundle of His", size=28, color=EDGE_MAGENTA, line_spacing=0.85).move_to([4.15, 1.92, 0])
        av_arrow = Arrow(
            [2.78, 1.92, 0], [0.24, 1.92, 0],
            buff=0.05, stroke_color=EDGE_MAGENTA, stroke_width=3.2, max_tip_length_to_length_ratio=0.10,
        )
        q_card = question_card("An edge moves. Does the trace?", color=CELL_WHITE, y=-3.12, size=32)

        self.add(paper, heart, trace, p_lbl, tag)

        self.at("wave crawls")
        self.play(
            FadeIn(av_lbl), GrowArrow(av_arrow),
            av_pos.animate.set_value(0.16),
            h_scale.animate.set_value(1.12),
            run_time=0.85,
        )
        # Gently lean in on the narrow AV bridge as the small MAGENTA dot crawls down, then ease back to 1.04
        self.advance_to("an edge is still", av_pos.animate.set_value(0.45), h_scale.animate.set_value(1.16))
        self.advance_to("should the trace", av_pos.animate.set_value(0.60), h_scale.animate.set_value(1.04))
        self.play(FadeIn(q_card, shift=UP * 0.12), av_pos.animate.set_value(0.64), run_time=0.75)
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(av_pos.animate.set_value(0.66), run_time=rem, rate_func=linear)
        self.finish()


class S12Pause(PredictPause):
    """4.5 s predict pause: question card holds, small MAGENTA dot pulses in place, GREEN pen waits."""
    QUESTION = "An edge moves. Does the trace?"
    CARD = {"color": CELL_WHITE, "size": 32, "y": -3.12}
    RING_AT = (5.32, -1.45, 0)
    SECONDS = 4.5

    def backdrop(self):
        paper = build_ecg_paper()
        tag = tag_schematic()
        t_static = ValueTracker(0.175)
        trace = build_ecg_live_trace(beat_ecg_value, t_static, t_range=(0.0, 0.80), show_cursor=False)
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        av_lbl = T("AV node,\nbundle of His", size=28, color=EDGE_MAGENTA, line_spacing=0.85).move_to([4.15, 1.92, 0])
        av_arrow = Arrow(
            [2.78, 1.92, 0], [0.24, 1.92, 0],
            buff=0.05, stroke_color=EDGE_MAGENTA, stroke_width=3.2, max_tip_length_to_length_ratio=0.10,
        )
        pulse_t = ValueTracker(0.0)
        heart = always_redraw(lambda: build_heart_frame(
            0.175, show_av_dot=True, av_frac=0.66,
            show_atrial_edge=False, show_vent_edge=False,
            show_av_trail=True,
            av_pulse=1.0 + 0.55 * np.sin(4.4 * pulse_t.get_value()),
        ))
        pulse_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(pulse_t)
        return VGroup(paper, heart, trace, p_lbl, av_lbl, av_arrow, tag)


class S13Answer(FilmScene):
    """Card dissolves; MAGENTA dot finishes crawl as GREEN pen draws nearly flat PR segment;
    tiny vs large MAGENTA batteries beside heart show proportional deflection bars."""
    def construct(self):
        t_beat = ValueTracker(0.175)
        av_pos = ValueTracker(0.66)
        hx = ValueTracker(0.0)
        paper = build_ecg_paper()
        tag = tag_schematic()

        heart = always_redraw(lambda: build_heart_frame(
            t_beat.get_value(),
            offset=RIGHT * hx.get_value(),
            show_av_dot=(av_pos.get_value() < 0.99),
            av_frac=av_pos.get_value(),
            show_atrial_edge=False,
            show_vent_edge=False,
            show_av_trail=True,
        ))
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        q_card = question_card("An edge moves. Does the trace?", color=CELL_WHITE, y=-3.12, size=32)

        self.add(paper, heart, trace, p_lbl, q_card, tag)

        self.at("stays nearly flat")
        self.play(
            FadeOut(q_card),
            av_pos.animate.set_value(1.0),
            t_beat.animate.set_value(0.240),
            run_time=1.75,
            rate_func=linear,
        )
        pr_lbl = ecg_wave_label("PR segment", 0.205, 0.0, dy=-0.42, size=26)
        self.play(FadeIn(pr_lbl, shift=UP * 0.06), run_time=0.45)

        self.advance_to("too small", hx.animate.set_value(-2.85), rate_func=smooth)

        # Clean vertical spacing: labels at y=3.36, batteries at y=2.70 (bottom >= 2.34), bar top <= 1.84!
        bar_base_y = 0.56
        small_x, large_x = 1.65, 4.35
        small_batt = build_battery_icon([small_x, 2.70, 0], scale=0.44)
        small_lbl = T("small boundary", size=24, color=EDGE_MAGENTA).move_to([small_x, 3.36, 0])
        small_bar_h = ValueTracker(0.02)
        small_bar = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.05, width=0.68, height=max(0.04, small_bar_h.get_value()),
            fill_color=ECG_GREEN, fill_opacity=0.88, stroke_color=ECG_GREEN, stroke_width=2.0,
        ).move_to([small_x, bar_base_y + max(0.04, small_bar_h.get_value()) / 2.0, 0]))
        bar_axis = Line([0.85, bar_base_y, 0], [5.25, bar_base_y, 0], stroke_color=TEXT, stroke_width=2.5)
        bar_cap = T("deflection size", size=24, color=ECG_GREEN).move_to([3.05, 0.22, 0])

        self.play(FadeIn(bar_axis), FadeIn(bar_cap), FadeIn(small_batt), FadeIn(small_lbl), run_time=0.65)
        self.add(small_bar)
        self.advance_to("the more tissue", small_bar_h.animate.set_value(0.16))

        big_frac = ValueTracker(0.06)
        large_batt = always_redraw(lambda: build_battery_icon(
            [large_x, 2.70, 0], scale=0.44 + 0.68 * big_frac.get_value(),
        ))
        large_bar = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.06, width=0.68, height=max(0.06, 0.16 + 1.12 * big_frac.get_value()),
            fill_color=ECG_GREEN, fill_opacity=0.88, stroke_color=ECG_GREEN, stroke_width=2.0,
        ).move_to([large_x, bar_base_y + max(0.06, 0.16 + 1.12 * big_frac.get_value()) / 2.0, 0]))
        large_lbl = T("large boundary", size=24, color=EDGE_MAGENTA).move_to([large_x, 3.36, 0])

        self.add(large_batt, large_bar)
        self.play(FadeIn(large_lbl), big_frac.animate.set_value(0.45), run_time=0.95, rate_func=linear)
        self.advance_to("bigger the deflection", big_frac.animate.set_value(0.72))
        rem = max(0.7, self.narration_s + 0.4 - self.elapsed())
        self.play(big_frac.animate.set_value(1.0), run_time=rem, rate_func=smooth)
        self.finish()


class S14Qrs(FilmScene):
    """Purkinje flash + broad MAGENTA wave crosses ventricles turning them GOLD as GREEN pen draws QRS;
    white bracket marks 'crossing time'."""
    def construct(self):
        t_beat = ValueTracker(0.240)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(
            t_beat, show_purkinje_flash=True, show_atrial_edge=False, show_vent_edge=True,
        )
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        pr_lbl = ecg_wave_label("PR segment", 0.205, 0.0, dy=-0.42, size=26)

        self.add(paper, heart, trace, p_lbl, pr_lbl, tag)

        self.at("wave races")
        self.advance_to("crosses the ventricles", t_beat.animate.set_value(0.275))
        self.advance_to("qrs complex", t_beat.animate.set_value(0.298))

        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), dy=-0.10, size=32).shift(RIGHT * 0.72)
        # Clear 'PR segment' early so it never overlaps the crossing-time bracket
        self.play(FadeOut(pr_lbl), FadeIn(qrs_lbl, shift=RIGHT * 0.08), run_time=0.55)

        self.advance_to("its width", t_beat.animate.set_value(0.305))

        x_q0 = ecg_pt(0.242, 0.0)[0]
        x_q1 = ecg_pt(0.316, 0.0)[0]
        br = h_bracket(x_q0, x_q1, y=-2.26, tick=0.18, color=CELL_WHITE, sw=3.6)
        ct_lbl = T("crossing time", size=28, color=CELL_WHITE, weight=BOLD).move_to([(x_q0 + x_q1) / 2.0, -3.02, 0])
        ct_line = Line([(x_q0 + x_q1) / 2.0, -2.28, 0], [(x_q0 + x_q1) / 2.0, -2.76, 0], stroke_color=CELL_WHITE, stroke_width=2.5)
        self.play(Create(br), Create(ct_line), FadeIn(ct_lbl), run_time=0.80)
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(t_beat.animate.set_value(0.310), run_time=rem, rate_func=linear)
        self.finish()


class S15HoldQrs(NarratedScene):
    """4 s silent hold: final ventricular tiles finish turning GOLD, MAGENTA edge fades, crossing-time bracket glows."""
    def construct(self):
        t_beat = ValueTracker(0.310)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(
            t_beat, show_purkinje_flash=False, show_atrial_edge=False, show_vent_edge=True,
        )
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), dy=-0.10, size=32).shift(RIGHT * 0.72)

        x_q0 = ecg_pt(0.242, 0.0)[0]
        x_q1 = ecg_pt(0.316, 0.0)[0]
        br = h_bracket(x_q0, x_q1, y=-2.26, tick=0.18, color=CELL_WHITE, sw=3.6)
        ct_lbl = T("crossing time", size=28, color=CELL_WHITE, weight=BOLD).move_to([(x_q0 + x_q1) / 2.0, -3.02, 0])
        ct_line = Line([(x_q0 + x_q1) / 2.0, -2.28, 0], [(x_q0 + x_q1) / 2.0, -2.76, 0], stroke_color=CELL_WHITE, stroke_width=2.5)

        self.add(paper, heart, trace, p_lbl, qrs_lbl, br, ct_line, ct_lbl, tag)
        self.play(
            t_beat.animate.set_value(0.342),
            br.animate.set_stroke(PLATEAU_GOLD, width=5.2),
            run_time=self.narration_s,
            rate_func=linear,
        )
        self.finish()


class S16St(FilmScene):
    """Ventricles evenly GOLD, zero MAGENTA; WHITE plateau inset returns; GREEN pen draws flat ST segment;
    hook text 'All depolarized. Flat.' returns."""
    def construct(self):
        t_beat = ValueTracker(0.342)
        t_ap = ValueTracker(30.0)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(
            t_beat, show_purkinje_flash=False, show_atrial_edge=False, show_vent_edge=False,
        )
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), dy=-0.10, size=32).shift(RIGHT * 0.72)

        inset = always_redraw(lambda: build_ap_inset(
            box=(-6.15, -2.85, 1.85, 3.35),
            t_dot_ms=t_ap.get_value(),
            highlight_plateau_to=t_ap.get_value(),
        ))

        self.add(paper, heart, trace, p_lbl, qrs_lbl, tag)

        self.at("nearly every")
        self.play(FadeIn(inset, shift=RIGHT * 0.15), t_beat.animate.set_value(0.354), run_time=0.60)
        self.advance_to("no edge left", t_ap.animate.set_value(100.0), t_beat.animate.set_value(0.386))
        self.advance_to("st segment", t_ap.animate.set_value(125.0), t_beat.animate.set_value(0.404))

        st_lbl = ecg_wave_label("ST", 0.395, 0.0, dy=0.38, size=30)
        self.play(FadeIn(st_lbl, shift=UP * 0.06), t_ap.animate.set_value(136.0), t_beat.animate.set_value(0.412), run_time=0.55)

        self.at("flat")
        hook_ret = T("All depolarized. Flat.", size=34, color=CELL_WHITE, weight=BOLD).move_to([-0.5, -3.12, 0])
        self.play(
            FadeIn(hook_ret, shift=UP * 0.08),
            t_ap.animate.set_value(146.0),
            t_beat.animate.set_value(0.420),
            run_time=0.55,
        )
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(t_ap.animate.set_value(156.0), t_beat.animate.set_value(0.426), run_time=rem, rate_func=linear)
        self.finish()


class S17HoldSt(NarratedScene):
    """4 s silent hold: ventricles remain 100% evenly GOLD, inset dot holds high on plateau, GREEN pen runs level."""
    def construct(self):
        t_beat = ValueTracker(0.426)
        t_ap = ValueTracker(156.0)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(
            t_beat, show_purkinje_flash=False, show_atrial_edge=False, show_vent_edge=False,
        )
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), dy=-0.10, size=32).shift(RIGHT * 0.72)
        st_lbl = ecg_wave_label("ST", 0.395, 0.0, dy=0.38, size=30)
        inset = always_redraw(lambda: build_ap_inset(
            box=(-6.15, -2.85, 1.85, 3.35),
            t_dot_ms=t_ap.get_value(),
            highlight_plateau_to=t_ap.get_value(),
        ))
        hook_ret = T("All depolarized. Flat.", size=34, color=CELL_WHITE, weight=BOLD).move_to([-0.5, -3.12, 0])

        self.add(paper, heart, trace, p_lbl, qrs_lbl, st_lbl, inset, hook_ret, tag)
        self.play(
            t_ap.animate.set_value(222.0),
            t_beat.animate.set_value(0.478),
            run_time=self.narration_s,
            rate_func=linear,
        )
        self.finish()


class S18TWave(FilmScene):
    """Ventricular patches fade from GOLD to BLUE at different moments, creating a broad soft MAGENTA
    recovery band (NO direction arrow); GREEN pen draws broad rounded T wave."""
    def construct(self):
        t_beat = ValueTracker(0.478)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(
            t_beat, show_purkinje_flash=False, show_atrial_edge=False, show_vent_edge=True,
        )
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), dy=-0.10, size=32).shift(RIGHT * 0.72)
        st_lbl = ecg_wave_label("ST", 0.395, 0.0, dy=0.38, size=30)

        self.add(paper, heart, trace, p_lbl, qrs_lbl, st_lbl, tag)

        self.advance_to("different regions", t_beat.animate.set_value(0.512))
        self.advance_to("broad", t_beat.animate.set_value(0.548))
        # Reach crest of T wave at 't wave' so s19_hold_t_wave smoothly finishes the last GOLD patches!
        self.advance_to("t wave", t_beat.animate.set_value(0.568))

        t_lbl = ecg_wave_label("T", 0.560, beat_ecg_value(0.560), dy=0.36, size=32)
        self.play(FadeIn(t_lbl, shift=UP * 0.08), t_beat.animate.set_value(0.576), run_time=0.60)
        rem = max(0.1, self.narration_s + 0.4 - self.elapsed())
        self.play(t_beat.animate.set_value(0.580), run_time=rem, rate_func=linear)
        self.finish()


class S19HoldTWave(NarratedScene):
    """4 s silent hold: final GOLD patches finish fading to BLUE and GREEN pen runs level after T."""
    def construct(self):
        t_beat = ValueTracker(0.580)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(
            t_beat, show_purkinje_flash=False, show_atrial_edge=False, show_vent_edge=True,
        )
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), dy=-0.10, size=32).shift(RIGHT * 0.72)
        st_lbl = ecg_wave_label("ST", 0.395, 0.0, dy=0.38, size=30)
        t_lbl = ecg_wave_label("T", 0.560, beat_ecg_value(0.560), dy=0.36, size=32)

        self.add(paper, heart, trace, p_lbl, qrs_lbl, st_lbl, t_lbl, tag)
        self.play(t_beat.animate.set_value(0.790), run_time=self.narration_s, rate_func=linear)
        self.finish()


class S20Qt(FilmScene):
    """QT bracket spans QRS-start to T-end; single-cell WHITE AP slides down and lines up underneath;
    one tracker stretches the plateau, sliding T wave and QT bracket right together."""
    def construct(self):
        ecg_box = (-6.1, 6.1, 0.75, 3.10)
        ecg_base = 1.52
        ecg_amp = 1.15
        t_range = (0.0, 0.94)

        extra_s = ValueTracker(0.0)
        br_prog = ValueTracker(0.0)
        tag = tag_schematic()

        paper = build_ecg_paper(box=ecg_box, base_y=ecg_base)

        def ecg_x(t):
            x0, x1 = ecg_box[0] + 0.25, ecg_box[1] - 0.25
            return x0 + (t - t_range[0]) / (t_range[1] - t_range[0]) * (x1 - x0)

        def mk_ecg_curve():
            ex = extra_s.get_value()
            ts = np.linspace(t_range[0], t_range[1], 280)
            pts = [np.array([ecg_x(u), ecg_base + ecg_amp * beat_ecg_value(u, ex), 0.0]) for u in ts]
            crv = VMobject(stroke_color=ECG_GREEN, stroke_width=5.5, fill_opacity=0)
            crv.set_points_as_corners(pts)
            return crv

        ecg_curve = always_redraw(mk_ecg_curve)
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), t_range=t_range, box=ecg_box, base_y=ecg_base, amp=ecg_amp, dy=0.34)
        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), t_range=t_range, box=ecg_box, base_y=ecg_base, amp=ecg_amp, dy=-0.10, size=30).shift(RIGHT * 0.68)
        t_lbl = always_redraw(lambda: ecg_wave_label(
            "T", 0.560 + extra_s.get_value(), beat_ecg_value(0.560 + extra_s.get_value(), extra_s.get_value()),
            t_range=t_range, box=ecg_box, base_y=ecg_base, amp=ecg_amp, dy=0.36, size=30,
        ))

        def mk_qt_bracket():
            ex = extra_s.get_value()
            p = br_prog.get_value()
            t0 = 0.242
            t1_full = 0.645 + ex
            t1 = t0 + p * (t1_full - t0)
            if p < 0.03:
                return VGroup()
            x0, x1 = ecg_x(t0), ecg_x(t1)
            br = h_bracket(x0, x1, y=0.22, tick=0.22, color=CELL_WHITE, sw=4.0)
            lbl = T("QT", size=32, color=CELL_WHITE, weight=BOLD).move_to([(x0 + x1) / 2.0, -0.14, 0])
            g0 = DashedLine([x0, ecg_base - 0.15, 0], [x0, -2.55, 0], stroke_color=CELL_WHITE, stroke_width=2.0, stroke_opacity=0.45)
            g1 = DashedLine([x1, ecg_base - 0.15, 0], [x1, -2.55, 0], stroke_color=CELL_WHITE, stroke_width=2.0, stroke_opacity=0.45)
            return VGroup(g0, g1, br, lbl)

        qt_bracket = always_redraw(mk_qt_bracket)

        ap_box = (-6.1, 6.1, -2.68, -0.58)
        ap_bg = RoundedRectangle(
            corner_radius=0.12, width=ap_box[1] - ap_box[0], height=ap_box[3] - ap_box[2],
            fill_color=PAPER_BG, fill_opacity=0.92, stroke_color=PAPER_BORDER, stroke_width=2.2,
        ).move_to([0.0, (ap_box[2] + ap_box[3]) / 2.0, 0])
        ap_lbl = T("one cell", size=26, color=CELL_WHITE).move_to([-4.70, -0.94, 0])

        def build_ap_static(ex_val=0.0):
            ex_ms = ex_val * 1000.0
            plat_ms = 296.0 + ex_ms
            ts = np.linspace(t_range[0], t_range[1], 300)
            py0, py1 = ap_box[2] + 0.26, ap_box[3] - 0.44
            pts = [
                np.array([
                    ecg_x(u),
                    py0 + ap_norm((u - 0.242) * 1000.0, plateau_ms=plat_ms) * (py1 - py0),
                    0.0,
                ])
                for u in ts
            ]
            crv = VMobject(stroke_color=CELL_WHITE, stroke_width=5.2, fill_opacity=0)
            crv.set_points_as_corners(pts)
            p_ts = np.linspace(0.242 + 0.022, 0.242 + (22.0 + plat_ms) / 1000.0, 80)
            p_pts = [
                np.array([
                    ecg_x(u),
                    py0 + ap_norm((u - 0.242) * 1000.0, plateau_ms=plat_ms) * (py1 - py0),
                    0.0,
                ])
                for u in p_ts
            ]
            p_crv = VMobject(stroke_color=PLATEAU_GOLD, stroke_width=6.4, fill_opacity=0)
            p_crv.set_points_as_corners(p_pts)
            return VGroup(crv, p_crv)

        ap_init = build_ap_static(0.0)
        ap_curve = always_redraw(lambda: build_ap_static(extra_s.get_value()))

        self.add(paper, ecg_curve, p_lbl, qrs_lbl, t_lbl, qt_bracket, tag)

        # Slide the full single-cell AP (box + curve + label together!) smoothly down into alignment from t=0!
        self.advance_to(
            "start of qrs",
            FadeIn(VGroup(ap_bg, ap_lbl, ap_init), shift=DOWN * 0.55),
        )
        self.remove(ap_init)
        self.add(ap_curve)

        # 2.26 -> 4.06: QT bracket sweeps smoothly from start of QRS to end of T
        self.advance_to("end of t", br_prog.animate.set_value(1.0))

        # Clean clearance above the gold plateau (py1 = -1.02, plateau ~ -1.14, label at -0.80 -> > 0.20 clear!)
        plat_tag = T("plateau", size=24, color=PLATEAU_GOLD, weight=BOLD).move_to([ecg_x(0.41), -0.82, 0])
        self.play(FadeIn(plat_tag), run_time=0.55)
        self.at("a longer plateau")

        # 5.92 -> end: ONE tracker stretches cell plateau, slides T wave right, and widens QT bracket!
        rem = max(1.8, self.narration_s + 0.4 - self.elapsed())
        self.play(
            extra_s.animate.set_value(0.115),
            plat_tag.animate.shift(RIGHT * 0.65),
            run_time=rem,
            rate_func=smooth,
        )
        self.finish()


class S21Return(FilmScene):
    """Heart replays one complete beat: flat when all BLUE, flat when ventricles are all GOLD
    (with atria back to BLUE), deflecting only while each MAGENTA boundary travels."""
    def construct(self):
        t_beat = ValueTracker(0.0)
        paper = build_ecg_paper()
        tag = tag_schematic()
        heart = live_heart(
            t_beat, show_purkinje_flash=True, show_atrial_edge=True, show_vent_edge=True,
        )
        trace = build_ecg_live_trace(beat_ecg_value, t_beat, t_range=(0.0, 0.80))

        self.add(paper, heart, trace, tag)

        # 0.00 -> 3.88: starts evenly BLUE at rest -> flat baseline
        self.advance_to("all at rest", t_beat.animate.set_value(0.075))

        # 3.88 -> 5.02: replay P, PR, QRS bringing ventricles onto pure GOLD plateau (atria back to BLUE!)
        self.advance_to("on the plateau", t_beat.animate.set_value(0.345))

        # 5.02 -> 6.16 -> 8.44: ventricles 100% pure GOLD, atria BLUE, ZERO MAGENTA -> pen runs dead level!
        self.advance_to("line stays level", t_beat.animate.set_value(0.410))
        self.advance_to("only moving disagreement", t_beat.animate.set_value(0.475))

        # 8.44 -> end: broad MAGENTA T wave writes recovery and returns to rest, lighting P, QRS, T!
        self.play(t_beat.animate.set_value(0.790), run_time=2.1, rate_func=linear)
        p_lbl = ecg_wave_label("P", 0.120, beat_ecg_value(0.120), dy=0.34)
        qrs_lbl = ecg_wave_label("QRS", 0.278, beat_ecg_value(0.278), dy=-0.10, size=32).shift(RIGHT * 0.72)
        t_lbl = ecg_wave_label("T", 0.560, beat_ecg_value(0.560), dy=0.36, size=32)
        self.play(FadeIn(p_lbl), FadeIn(qrs_lbl), FadeIn(t_lbl), run_time=0.6)
        self.finish()


class S22End(EndCard):
    LINE = "The ECG moves only while a boundary between cells travels."
