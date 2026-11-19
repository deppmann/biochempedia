"""
The Tie That Holds — Cardiac Action Potentials and the ECG (STEMhop)

COLOUR MAP (one colour per concept, constant across the entire film):
  VOLTAGE_COL   = "#FFFFFF"  bright WHITE : membrane voltage trace, voltage tracker dot, key callouts
  NA_COL        = "#FF745C"  CORAL        : fast sodium channel (Nav1.5), Na+ ions, inactivation bar
  CA_COL        = "#F5C842"  GOLD         : L-type calcium channel (Cav1.2), Ca2+ ions, inward pull arrow
  K_COL         = "#58C4DD"  BLUE         : potassium channels (notch gate, IKr/IKs/hERG, IK1), K+ ions, outward pull arrow
  CELL_FILL     = "#252E3F"  pale slate   : cell interior (left side of membrane slice)
  MEMBRANE_FILL = "#475266"  slate-grey   : lipid bilayer membrane slice with fixed channel slots
  AXIS_COL      = "#C5CEDE"  silver-white : plot axes, ticks, axis labels, schematic scope tag

ONE WORLD CARRIED FROM SCENE TO SCENE:
  16:9 frame split cleanly into two permanent zones:
  - LEFT ~56%: large voltage-vs-time plot (y: -90 to +40 mV, x: 0 to 400 ms) driven by a conductance-based
    ventricular myocyte ODE (E_K = -91 mV, E_Na = +48 mV, E_Ca = +60 mV), plus a bottom-left scope tag
    "schematic, teaching values" kept throughout the film.
  - RIGHT ~40%: tall cross-section of one ventricular cell membrane (inside on the left, outside on the right)
    with five fixed channel slots (top to bottom): CORAL Na+, brief BLUE notch gate, GOLD L-type Ca2+,
    paired BLUE delayed rectifiers (IKr/hERG and IKs), and the wide hinged BLUE IK1 inward-rectifier double-door,
    with a dedicated right-hand label column clear of all ion streams and tug-of-war arrows.

WHAT CHANGES IN EVERY SPOKEN SCENE (and what it is computed from):
  s00_hook      : 3 ms ODE nerve spike flicks up (+33 mV) & down; WHITE dot then draws the 300 ms ODE ventricular AP and stops high on the plateau.
  s02_rest      : WHITE dot sweeps the flat -90 mV resting baseline; wide BLUE IK1 double-door opens (g_K1 at -90 mV) with bidirectional/net-outward K+ ion flow.
  s03_upstroke  : CORAL Na+ opens & rushes inward; WHITE dot shoots -90 -> +31 mV (ODE phase 0); IK1 swings nearly shut (g_K1(V)); Na+ bars shut; brief BLUE gate blinks open & cuts phase 1 notch.
  s05_puzzle    : WHITE dot glides continuously across the 200 ms ODE plateau near 0 mV as a measured bracket grows underneath; barred Na+ pulses once.
  s06_tug       : Trace rewinds to plateau start; GOLD L-type Ca2+ opens (inward stream + inward arrow ~ |I_CaL|) and BLUE IKr/IKs opens (outward stream + arrow ~ I_Kdr).
  s08_idea      : Arrows merge into a membrane tug-of-war rope with centre knot; as WHITE dot creeps down the ODE plateau (+13 -> +1 mV), BLUE arrow lengthens slightly and knot drifts right.
  s10_why       : Dashed ghost of wide-open resting IK1 door & dashed ghost drop to -90 mV appear beside the nearly shut IK1 door while plateau streams continue.
  s11_rectifier : Ghosts fade, real nearly-shut IK1 crack lights up; GOLD and BLUE streams & arrows thin together (low total conductance) while staying nearly balanced.
  s13_predict   : Trace rewinds to plateau start with original bracket; white blocker bar slides across upper IKr pore, thinning BLUE stream and shortening BLUE arrow; question card appears.
  s15_answer    : WHITE dot draws the ODE-computed hERG-blocked AP (f_Kr = 0.76) extending past the ghost normal trace and bracket; two proportional QT bars grow in the lower plot strip.
  s17_reserve   : Blocker lifts and trace morphs back to normal ODE AP; three BLUE K+ channels pulse in turn, one dims, and the other two brighten with increased outward K+ flow.
  s18_break     : GOLD Ca2+ dots accumulate inside the membrane (ODE ca_i); GOLD channel closes, inward arrow collapses, tug-of-war knot slides fully to BLUE, and WHITE dot begins phase 3 fall.
  s19_finish    : As ODE voltage falls past -40 mV, g_K1 surges and wide IK1 door swings open again; WHITE dot accelerates down to -90 mV at ~320 ms and settles on the rest line.
  s21_return    : Full ODE AP replays briskly once: upstroke -> nearly equal GOLD/BLUE plateau arrows with IK1 shut -> arrows part & trace falls, leaving the plateau segment lit in bright white.
"""

from bp_parts import *

# ---------------------------------------------------------------------------
# COLOUR MAP (constant across all 23 scenes)
# ---------------------------------------------------------------------------
VOLTAGE_COL = "#FFFFFF"
NA_COL = "#FF745C"
CA_COL = "#F5C842"
K_COL = "#58C4DD"
CELL_FILL = "#252E3F"
CELL_STROKE = "#46526A"
MEMBRANE_FILL = "#475266"
MEMBRANE_STROKE = "#8F9BB3"
AXIS_COL = "#C5CEDE"
REST_LINE_COL = "#8AD3E6"
GHOST_COL = "#B8C4D8"

# ---------------------------------------------------------------------------
# FIXED WORLD GEOMETRY (safe frame: x in [-6.5, 6.5], y in [-3.55, 3.55])
# ---------------------------------------------------------------------------
PLOT_BOX = (-5.55, 0.85, -2.20, 2.40)     # left ~56% of frame
PLOT_XR = (0.0, 400.0)
PLOT_YR = (-104.0, 42.0)

CELL_X0 = 1.55
MEM_X = 3.80
MEM_W = 0.36
MEM_X0 = MEM_X - MEM_W / 2.0              # 3.62
MEM_X1 = MEM_X + MEM_W / 2.0              # 3.98
MEM_Y0 = -2.52
MEM_Y1 = 2.52

ION_X_IN = 1.92                           # left end of ion travel corridor (inside cell)
ION_X_OUT = 5.02                          # right end of ion travel corridor (outside cell)
LABEL_X = 5.26                            # dedicated right-hand label column (ion-free, arrow-free)

# Fixed vertical channel centres along the membrane wall
Y_NA = 2.02
Y_ITO = 1.36
Y_CA = 0.50
Y_ROPE = -0.06
Y_IKR = -0.50
Y_IKS = -0.90
Y_KDR = -0.70
Y_IK1 = -1.86
IK1_HALF_H = 0.44                         # total IK1 doorway aperture = 0.88 scene units

PREDICT_Q = "Block one outward current: the plateau?"
PREDICT_CARD_KW = {"y": 3.36, "color": VOLTAGE_COL, "size": 32, "max_w": 12.2}
SCOPE_TEXT = "schematic, teaching values"


# ---------------------------------------------------------------------------
# COMPUTED BIOPHYSICAL ODE MODEL (ventricular myocyte + 3 ms nerve spike)
# ---------------------------------------------------------------------------
def _sig(x):
    return 1.0 / (1.0 + np.exp(np.clip(x, -40.0, 40.0)))


def simulate_ventricular_ap(f_Kr=1.0, dt=0.1, t_end=400.0):
    """Conductance-based teaching model of a human ventricular myocyte AP.

    C_m dV/dt = -(I_Na + I_to + I_CaL + I_Kr + I_Ks + I_K1 + I_bg + I_stim)
    Reversal potentials follow lesson_for_context.mdx (E_Ca = +60 mV, E_K near -91 mV).
    """
    E_K = -91.0
    E_Na = 48.0
    E_Ca = 60.0
    E_bg = -45.0
    g_bg = 0.0045

    n = int(round(t_end / dt)) + 1
    ts = np.linspace(0.0, t_end, n)
    V = np.zeros(n)
    I_Na = np.zeros(n)
    I_to = np.zeros(n)
    I_CaL = np.zeros(n)
    I_Kr = np.zeros(n)
    I_Ks = np.zeros(n)
    I_K1 = np.zeros(n)
    g_K1_arr = np.zeros(n)
    ca_arr = np.zeros(n)

    v = -90.0
    m, h = 0.0, 1.0
    r_to, s_to = 0.0, 1.0
    d, f, f_ca = 0.0, 1.0, 1.0
    ca_i = 0.0
    xr, xs = 0.0, 0.0

    for i in range(n):
        t = ts[i]
        g_K1 = 0.22 * _sig((v + 56.0) / 8.5) + 0.0015

        m_inf = _sig(-(v + 40.0) / 5.5)
        h_inf = _sig((v + 74.0) / 4.5)
        tau_m = 0.25
        tau_h = 0.48 if v > -35.0 else 10.0

        r_inf = _sig(-(v - 8.0) / 6.0)
        s_inf = _sig((v + 18.0) / 6.0)
        tau_r = 1.0
        tau_s = 6.5 if v > -20.0 else 35.0

        d_inf = _sig(-(v + 14.0) / 5.5)
        f_inf = _sig((v + 24.0) / 6.0)
        tau_d = 4.0
        tau_f = 950.0 if v > -25.0 else 30.0

        xr_inf = _sig(-(v + 18.0) / 7.0)
        xs_inf = _sig(-(v + 12.0) / 8.5)
        tau_xr = 35.0 if v > -30.0 else 35.0
        tau_xs = 560.0 if v > -30.0 else 45.0

        i_na = 8.2 * (m ** 3) * h * (v - E_Na)
        i_to = 0.130 * r_to * s_to * (v - E_K)
        g_ca = 0.0325 * d * f * f_ca
        i_ca = g_ca * (v - E_Ca)
        g_kr = 0.0110 * f_Kr * xr
        g_ks = 0.024 * (xs ** 2)
        i_kr = g_kr * (v - E_K)
        i_ks = g_ks * (v - E_K)
        i_k1 = g_K1 * (v - E_K)
        i_bg = g_bg * (v - E_bg)

        i_stim = -40.0 if (20.0 <= t <= 21.6) else 0.0

        V[i] = v
        I_Na[i] = i_na
        I_to[i] = i_to
        I_CaL[i] = i_ca
        I_Kr[i] = i_kr
        I_Ks[i] = i_ks
        I_K1[i] = i_k1
        g_K1_arr[i] = g_K1
        ca_arr[i] = ca_i

        dv = -(i_na + i_to + i_ca + i_kr + i_ks + i_k1 + i_bg + i_stim)
        v += dv * dt
        m += (m_inf - m) / tau_m * dt
        h += (h_inf - h) / tau_h * dt
        r_to += (r_inf - r_to) / tau_r * dt
        s_to += (s_inf - s_to) / tau_s * dt
        d += (d_inf - d) / tau_d * dt
        f += (f_inf - f) / tau_f * dt
        ca_in = max(0.0, -i_ca) * 0.00125
        ca_i += (ca_in - ca_i / 600.0) * dt
        f_ca_inf = 1.0 / (1.0 + (ca_i / 0.44) ** 4.0)
        f_ca += (f_ca_inf - f_ca) / 40.0 * dt
        xr += (xr_inf - xr) / tau_xr * dt
        xs += (xs_inf - xs) / tau_xs * dt

    return {
        "t": ts, "V": V, "I_Na": I_Na, "I_to": I_to,
        "I_CaL": I_CaL, "I_Kr": I_Kr, "I_Ks": I_Ks,
        "I_Kdr": I_Kr + I_Ks, "I_K1": I_K1,
        "g_K1": g_K1_arr, "ca_i": ca_arr,
    }


def simulate_nerve_spike(dt=0.05, t_end=60.0):
    """Brief ~3 ms nerve spike computed from fast Na+ and delayed K+ currents (+33 mV peak, no plateau)."""
    E_K, E_Na = -91.0, 38.0
    n = int(round(t_end / dt)) + 1
    ts = np.linspace(0.0, t_end, n)
    V = np.zeros(n)
    v, m, h, nk = -90.0, 0.0, 1.0, 0.0
    for i in range(n):
        t = ts[i]
        m_inf = _sig(-(v + 42.0) / 5.5)
        h_inf = _sig((v + 68.0) / 5.0)
        n_inf = _sig(-(v + 32.0) / 8.0)
        i_na = 19.0 * (m ** 3) * h * (v - E_Na)
        i_k = 5.5 * (nk ** 4) * (v - E_K)
        i_k1 = 0.25 * (v - E_K)
        i_stim = -65.0 if (20.0 <= t <= 20.9) else 0.0
        V[i] = v
        v += -(i_na + i_k + i_k1 + i_stim) * dt
        m += (m_inf - m) / 0.14 * dt
        h += (h_inf - h) / (0.75 if v > -35.0 else 4.0) * dt
        nk += (n_inf - nk) / (1.45 if v > -40.0 else 2.0) * dt
    return ts, V


SIM_NORM = simulate_ventricular_ap(f_Kr=1.0)
SIM_HERG = simulate_ventricular_ap(f_Kr=0.76)   # partial hERG block: repolarizes ~350 ms, clear of 'rest'
NERVE_T, NERVE_V = simulate_nerve_spike()
REST_T = np.linspace(0.0, 400.0, 201)
REST_V = np.full_like(REST_T, -90.0)


def sim_val(sim, key, t_ms):
    return float(np.interp(t_ms, sim["t"], sim[key]))


def v_norm(t_ms):
    return sim_val(SIM_NORM, "V", t_ms)


def sample_curve_points(plot, ts, vs, t0, t1):
    """Dense adaptive point list from precomputed ODE arrays (sharp upstroke & smooth plateau)."""
    if t1 <= t0 + 1e-6:
        return []
    fine = ts[(ts >= max(t0, 19.0)) & (ts <= min(t1, 45.0))][::2]
    coarse = np.arange(t0, t1, 2.5)
    grid = np.unique(np.concatenate([np.array([t0, t1]), coarse, fine]))
    grid = grid[(grid >= t0) & (grid <= t1)]
    vals = np.interp(grid, ts, vs)
    return [plot.pt(float(x), float(np.clip(y, plot.yr[0], plot.yr[1]))) for x, y in zip(grid, vals)]


def make_static_curve(plot, ts, vs, t0=0.0, t1=400.0, color=VOLTAGE_COL, width=5.5, opacity=1.0, dashed=False):
    pts = sample_curve_points(plot, ts, vs, t0, t1)
    if dashed:
        raw = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
        if len(pts) >= 2:
            raw.set_points_as_corners(pts)
        return DashedVMobject(raw, num_dashes=42, dashed_ratio=0.55).set_stroke(color, width=width, opacity=opacity)
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    if len(pts) >= 2:
        m.set_points_as_corners(pts)
    return m


def make_live_curve(plot, ts, vs, tracker, t0=0.0, color=VOLTAGE_COL, width=5.5):
    def mk():
        t1 = float(tracker.get_value())
        m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
        pts = sample_curve_points(plot, ts, vs, t0, t1)
        if len(pts) >= 2:
            m.set_points_as_corners(pts)
        return m
    return always_redraw(mk)


def make_voltage_dot(plot, ts, vs, tracker, radius=0.145, color=VOLTAGE_COL,
                     trail_ms=34.0, show_trail=False):
    """Larger glowing voltage marker with a short luminous trail along the active trace."""
    def _mk():
        t1 = float(tracker.get_value())
        v1 = float(np.interp(t1, ts, vs))
        pt = plot.pt(t1, v1)
        g = VGroup()
        if show_trail and t1 > 2.5:
            t_start = max(0.0, t1 - trail_ms)
            pts = sample_curve_points(plot, ts, vs, t_start, t1)
            if len(pts) >= 2:
                outer = VMobject(stroke_color=TEAL, stroke_width=14.0, stroke_opacity=0.28, fill_opacity=0)
                outer.set_points_as_corners(pts)
                inner = VMobject(stroke_color=color, stroke_width=9.0, stroke_opacity=0.60, fill_opacity=0)
                inner.set_points_as_corners(pts)
                g.add(outer, inner)
        halo = Circle(
            radius=radius * 1.65,
            stroke_color=TEAL, stroke_width=2.0, stroke_opacity=0.58,
            fill_color=TEAL, fill_opacity=0.24,
        ).move_to(pt)
        core = Dot(pt, radius=radius, color=color, stroke_color=TEAL, stroke_width=3.0)
        g.add(halo, core)
        return g
    return always_redraw(_mk)


def make_voltage_fill(plot, ts, vs, tracker, t0=0.0, color=TEAL, opacity=0.18):
    """Stroke-free translucent fill under V(t) down to -90 mV (depolarized excursion above rest)."""
    def _mk():
        return VMobject()  # fill under the curve removed: the narration never claims an area
        t1 = float(tracker.get_value())
        if t1 <= t0 + 1.0:
            return VMobject()
        fine = ts[(ts >= max(t0, 19.0)) & (ts <= min(t1, 45.0))][::2]
        coarse = np.arange(t0, t1, 2.5)
        grid = np.unique(np.concatenate([np.array([t0, t1]), coarse, fine]))
        grid = grid[(grid >= t0) & (grid <= t1)]
        vals = np.maximum(np.interp(grid, ts, vs), -90.0)
        if np.max(vals) <= -89.5 or len(grid) < 2:
            return VMobject()
        pts = [plot.pt(float(x), float(np.clip(y, plot.yr[0], plot.yr[1]))) for x, y in zip(grid, vals)]
        base_r = plot.pt(float(t1), -90.0)
        base_l = plot.pt(float(t0), -90.0)
        poly = Polygon(*pts, base_r, base_l, stroke_width=0, fill_color=color, fill_opacity=opacity)
        poly.set_z_index(-3)
        return poly
    m = always_redraw(_mk)
    m.set_z_index(-3)
    return m


def make_static_voltage_fill(plot, ts, vs, t0=0.0, t1=325.0, color=TEAL, opacity=0.18):
    return VMobject()  # fill removed (no narrated claim)
    fine = ts[(ts >= max(t0, 19.0)) & (ts <= min(t1, 45.0))][::2]
    coarse = np.arange(t0, t1, 2.5)
    grid = np.unique(np.concatenate([np.array([t0, t1]), coarse, fine]))
    grid = grid[(grid >= t0) & (grid <= t1)]
    vals = np.maximum(np.interp(grid, ts, vs), -90.0)
    pts = [plot.pt(float(x), float(np.clip(y, plot.yr[0], plot.yr[1]))) for x, y in zip(grid, vals)]
    poly = Polygon(*pts, plot.pt(float(t1), -90.0), plot.pt(float(t0), -90.0),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)
    poly.set_z_index(-3)
    return poly


def make_voltage_readout(ts, vs, tracker):
    """Live oscilloscope readout (V and t) driven by the same ValueTracker as the voltage dot."""
    sample = M("-90 mV · 400 ms", size=24)
    w = sample.width + 0.56
    h = sample.height + 0.30
    box = RoundedRectangle(
        corner_radius=0.10, width=w, height=h,
        stroke_color=AXIS_COL, stroke_width=2.0, stroke_opacity=0.65,
        fill_color=BG, fill_opacity=0.92,
    ).move_to([PLOT_BOX[1] - w / 2.0, 2.74, 0.0])

    def _txt():
        t_val = float(tracker.get_value())
        v_val = float(np.interp(t_val, ts, vs))
        s = f"{v_val:+4.0f} mV · {t_val:3.0f} ms"
        return M(s, size=24, color=VOLTAGE_COL).move_to(box.get_center())

    txt = always_redraw(_txt)
    return VGroup(box, txt)


def wait_dur(scene, phrase, lead=0.2):
    """Seconds remaining until `phrase` (minus lead), never negative."""
    return max(0.0, scene.t_of(phrase) - lead - scene.elapsed())


# ---------------------------------------------------------------------------
# REUSABLE WORLD BUILDERS (identical placement across all 23 scenes)
# ---------------------------------------------------------------------------
def build_scope_tag():
    t = T(SCOPE_TEXT, size=22, color=AXIS_COL)
    t.move_to([-6.52 + t.width / 2.0, -3.54, 0.0])
    return t


def build_plot():
    return Plot(
        box=PLOT_BOX,
        xr=PLOT_XR,
        yr=PLOT_YR,
        xticks=[(0, "0"), (100, "100"), (200, "200"), (300, "300"), (400, "400")],
        yticks=[(-90, "-90"), (-60, "-60"), (-30, "-30"), (0, "0"), (30, "+30")],
        xlabel="time (ms)",
        ylabel="voltage (mV)",
        color=AXIS_COL,
        size=24,
        label_size=28,
        stroke=3,
    )


def build_rest_line(P, with_label=True):
    a, b = P.pt(0.0, -90.0), P.pt(400.0, -90.0)
    ln = DashedLine(a, b, color=REST_LINE_COL, stroke_width=2.6, dash_length=0.14)
    g = VGroup(ln)
    if with_label:
        # Raised clearly above the -90 mV dot + larger glowing halo corridor and steep phase-3 drop
        lab = T("rest", size=26, color=REST_LINE_COL).next_to(b, UP, buff=0.46).align_to(b, RIGHT)
        g.add(lab)
        g.label = lab
    g.line = ln
    return g


def build_plateau_bracket(P, t_start=48.0, t_end_tracker=None, t_end=248.0, with_label=True):
    """Bracket underneath the plateau, cleanly clear of the vertical upstroke and rest line."""
    y_b = -0.60

    def _make_bracket(te):
        x0 = P.pt(t_start, 0.0)[0]
        x1 = P.pt(max(t_start + 4.0, te), 0.0)[0]
        horiz = Line([x0, y_b, 0], [x1, y_b, 0], color=VOLTAGE_COL, stroke_width=4.2)
        t_l = Line([x0, y_b, 0], [x0, y_b + 0.18, 0], color=VOLTAGE_COL, stroke_width=4.2)
        t_r = Line([x1, y_b, 0], [x1, y_b + 0.18, 0], color=VOLTAGE_COL, stroke_width=4.2)
        return VGroup(horiz, t_l, t_r)

    if t_end_tracker is not None:
        br = always_redraw(lambda: _make_bracket(float(t_end_tracker.get_value())))
    else:
        br = _make_bracket(t_end)
    if not with_label:
        return br
    # Slight rightward centre (t=162 ms) keeps 'p' generously clear of the upstroke at t=20 ms
    xm = P.pt(162.0, 0.0)[0]
    lab = T("plateau, about 200 ms", size=26, color=VOLTAGE_COL).move_to([xm, y_b - 0.36, 0.0])
    return VGroup(br, lab), br, lab


def make_channel_housing(y_c, half_h, color=MEMBRANE_STROKE, fill_opacity=0.20, active=True):
    """Upper and lower channel protein lips framing a pore cut through the membrane."""
    lip_h = 0.09
    w = MEM_W + 0.16
    op = 1.0 if active else 0.45
    top_lip = RoundedRectangle(
        corner_radius=0.04, width=w, height=lip_h,
        stroke_color=color, stroke_width=2.5, stroke_opacity=op,
        fill_color=color, fill_opacity=fill_opacity if active else 0.08,
    ).move_to([MEM_X, y_c + half_h + lip_h / 2.0, 0.0])
    bot_lip = RoundedRectangle(
        corner_radius=0.04, width=w, height=lip_h,
        stroke_color=color, stroke_width=2.5, stroke_opacity=op,
        fill_color=color, fill_opacity=fill_opacity if active else 0.08,
    ).move_to([MEM_X, y_c - half_h - lip_h / 2.0, 0.0])
    pore = Rectangle(
        width=MEM_W + 0.04, height=2 * half_h,
        stroke_width=0, fill_color=BG, fill_opacity=0.90,
    ).move_to([MEM_X, y_c, 0.0])
    return VGroup(pore, top_lip, bot_lip)


def make_ik1_doors(open_tracker, color=K_COL, opacity=1.0, dashed=False, static_open=None):
    """Hinged wide double-door for IK1: openness 1.0 = wide open at rest, ~0.04 = thin crack at plateau."""
    hinge_top = np.array([MEM_X, Y_IK1 + IK1_HALF_H, 0.0])
    hinge_bot = np.array([MEM_X, Y_IK1 - IK1_HALF_H, 0.0])
    leaf_len = IK1_HALF_H - 0.035

    def _build(op_val):
        if dashed:
            # High-visibility dashed ghost outline of the wide-open resting doorway
            p_top = hinge_top + RIGHT * 0.72
            p_bot = hinge_bot + RIGHT * 0.72
            l1 = DashedLine(hinge_top, p_top, color=color, stroke_width=5.5, dash_length=0.11).set_opacity(opacity)
            l2 = DashedLine(hinge_bot, p_bot, color=color, stroke_width=5.5, dash_length=0.11).set_opacity(opacity)
            vert = DashedLine(p_top, p_bot, color=color, stroke_width=3.2, dash_length=0.10).set_opacity(opacity * 0.75)
            h1 = Dot(hinge_top, radius=0.055, color=color).set_opacity(opacity)
            h2 = Dot(hinge_bot, radius=0.055, color=color).set_opacity(opacity)
            return VGroup(l1, l2, vert, h1, h2)
        ang_top = -PI / 2.0 + 0.10 + op_val * (PI / 2.0 - 0.10)
        ang_bot = +PI / 2.0 - 0.10 - op_val * (PI / 2.0 - 0.10)
        p_top = hinge_top + leaf_len * np.array([np.cos(ang_top), np.sin(ang_top), 0.0])
        p_bot = hinge_bot + leaf_len * np.array([np.cos(ang_bot), np.sin(ang_bot), 0.0])
        l1 = Line(hinge_top, p_top, color=color, stroke_width=7.5).set_stroke(opacity=opacity)
        l2 = Line(hinge_bot, p_bot, color=color, stroke_width=7.5).set_stroke(opacity=opacity)
        h1 = Dot(hinge_top, radius=0.055, color=color).set_opacity(opacity)
        h2 = Dot(hinge_bot, radius=0.055, color=color).set_opacity(opacity)
        return VGroup(l1, l2, h1, h2)

    if static_open is not None:
        return _build(static_open)
    return always_redraw(lambda: _build(float(open_tracker.get_value())))


class MembraneWorld(VGroup):
    """The persistent right-hand cell membrane cross-section with all five fixed channel slots."""

    def __init__(self, na_state="empty", ito_open=False, ca_state="empty",
                 kdr_state="empty", ik1_open=0.05, ik1_dim=False, herg_barred=False):
        super().__init__()
        self.cell_bg = Rectangle(
            width=MEM_X0 - CELL_X0, height=MEM_Y1 - MEM_Y0,
            fill_color=CELL_FILL, fill_opacity=0.92,
            stroke_width=0.0,
        ).move_to([(CELL_X0 + MEM_X0) / 2.0, (MEM_Y0 + MEM_Y1) / 2.0, 0.0])
        self.cell_border = VMobject(stroke_color=CELL_STROKE, stroke_width=2.0, fill_opacity=0)
        self.cell_border.set_points_as_corners([
            [MEM_X0, MEM_Y1, 0.0], [CELL_X0, MEM_Y1, 0.0],
            [CELL_X0, MEM_Y0, 0.0], [MEM_X0, MEM_Y0, 0.0],
        ])

        self.wall = Rectangle(
            width=MEM_W, height=MEM_Y1 - MEM_Y0,
            fill_color=MEMBRANE_FILL, fill_opacity=1.0,
            stroke_color=MEMBRANE_STROKE, stroke_width=2.5,
        ).move_to([MEM_X, 0.0, 0.0])

        self.inside_lbl = T("inside", size=28, color=VOLTAGE_COL).move_to([(CELL_X0 + MEM_X0) / 2.0, 2.82, 0.0])
        self.outside_lbl = T("outside", size=28, color=VOLTAGE_COL).move_to([5.15, 2.82, 0.0])
        self.add(self.cell_bg, self.cell_border, self.wall, self.inside_lbl, self.outside_lbl)

        # Slot 1: CORAL Na+ channel
        na_col = NA_COL if na_state != "empty" else MEMBRANE_STROKE
        self.na_housing = make_channel_housing(Y_NA, 0.16, color=na_col, active=(na_state != "empty"))
        if na_state == "barred_dim":
            self.na_housing.set_opacity(0.45)
        self.na_bar = Line(
            [MEM_X0 - 0.10, Y_NA - 0.14, 0.0],
            [MEM_X1 + 0.10, Y_NA + 0.14, 0.0],
            color=NA_COL, stroke_width=6.0,
        )
        self.na_bar.set_opacity(1.0 if na_state == "barred" else (0.45 if na_state == "barred_dim" else 0.0))
        self.add(self.na_housing, self.na_bar)

        # Slot 2: Brief BLUE K+ notch gate
        ito_col = K_COL if ito_open else MEMBRANE_STROKE
        self.ito_housing = make_channel_housing(Y_ITO, 0.10, color=ito_col, active=ito_open)
        self.ito_plug = Rectangle(
            width=MEM_W * 0.72, height=0.18,
            fill_color=MEMBRANE_FILL, fill_opacity=0.0 if ito_open else 0.95,
            stroke_width=0,
        ).move_to([MEM_X, Y_ITO, 0.0])
        self.add(self.ito_housing, self.ito_plug)

        # Slot 3: GOLD L-type calcium channel (empty slate slot until calcium is introduced!)
        self.ca_state_active = ValueTracker(0.0 if ca_state == "empty" else 1.0)
        ca_col = CA_COL if ca_state != "empty" else MEMBRANE_STROKE
        self.ca_housing = make_channel_housing(Y_CA, 0.20, color=ca_col, active=(ca_state == "open"))
        if ca_state == "dim":
            self.ca_housing.set_opacity(0.40)
        self.ca_gate_val = ValueTracker(1.0 if ca_state in ("open", "dim") else 0.0)
        self.ca_gate = always_redraw(lambda: self._make_ca_plug())
        self.add(self.ca_housing, self.ca_gate)

        # Slot 4: BLUE delayed-rectifier pair (upper = IKr/hERG, lower = IKs)
        kdr_col = K_COL if kdr_state != "empty" else MEMBRANE_STROKE
        self.ikr_housing = make_channel_housing(Y_IKR, 0.13, color=kdr_col, active=(kdr_state != "empty"))
        self.iks_housing = make_channel_housing(Y_IKS, 0.13, color=kdr_col, active=(kdr_state != "empty"))
        self.herg_bar = Line(
            [MEM_X0 - 0.12, Y_IKR - 0.13, 0.0],
            [MEM_X1 + 0.12, Y_IKR + 0.13, 0.0],
            color=VOLTAGE_COL, stroke_width=6.5,
        ).set_opacity(1.0 if herg_barred else 0.0)
        self.add(self.ikr_housing, self.iks_housing, self.herg_bar)

        # Slot 5: Wide BLUE IK1 hinged double-door
        self.ik1_housing = make_channel_housing(Y_IK1, IK1_HALF_H, color=K_COL, active=not ik1_dim)
        if ik1_dim:
            self.ik1_housing.set_opacity(0.38)
        self.ik1_open = ValueTracker(ik1_open)
        self.ik1_doors = make_ik1_doors(self.ik1_open, color=K_COL, opacity=0.38 if ik1_dim else 1.0)
        self.add(self.ik1_housing, self.ik1_doors)

    def _make_ca_plug(self):
        # No premature gold block when slot is still empty!
        if self.ca_state_active.get_value() < 0.5:
            return Rectangle(
                width=MEM_W * 0.78, height=0.36,
                fill_color=MEMBRANE_FILL, fill_opacity=0.92, stroke_width=0,
            ).move_to([MEM_X, Y_CA, 0.0])
        op = float(np.clip(self.ca_gate_val.get_value(), 0.0, 1.0))
        shut_h = 0.20 * (1.0 - op)
        if shut_h < 0.008:
            return VMobject()
        top_s = Rectangle(
            width=MEM_W * 0.85, height=shut_h,
            fill_color=CA_COL, fill_opacity=0.72, stroke_width=0,
        ).move_to([MEM_X, Y_CA + 0.20 - shut_h / 2.0, 0.0])
        bot_s = Rectangle(
            width=MEM_W * 0.85, height=shut_h,
            fill_color=CA_COL, fill_opacity=0.72, stroke_width=0,
        ).move_to([MEM_X, Y_CA - 0.20 + shut_h / 2.0, 0.0])
        return VGroup(top_s, bot_s)


def make_channel_label(text, y, color, size=28, line_spacing=0.82):
    lab = T(text, size=size, color=color, line_spacing=line_spacing)
    lab.move_to([LABEL_X + lab.width / 2.0, y, 0.0])
    return lab


def make_ion_stream(y_center, color, direction, count=20, spread_y=0.14, speed=1.05,
                    rate_tracker=None, seed=7, radius=0.115, bidir=False):
    """Deterministic ion dots flowing strictly within [ION_X_IN, ION_X_OUT] across the membrane.

    direction: -1 for inward (outside -> inside), +1 for outward (inside -> outside).
    rate_tracker (0..1.5): scales active dot density & flow speed from the ODE current.
    """
    rng = np.random.default_rng(seed)
    phases = (np.arange(count) / float(count) + rng.uniform(-0.025, 0.025, size=count)) % 1.0
    dys = rng.uniform(-spread_y, spread_y, size=count)
    dirs = np.array([direction] * count, dtype=float)
    if bidir:
        # Bidirectional flicker with clear net outward drift (IK1 at rest)
        dirs = np.array([1.0 if i % 3 != 0 else -1.0 for i in range(count)], dtype=float)
    state = {"t": 0.0}
    dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(count)])

    def _update(mob, dt):
        r = 1.0 if rate_tracker is None else float(np.clip(rate_tracker.get_value(), 0.0, 1.5))
        state["t"] += dt * (0.60 + 0.55 * r)
        active_n = int(round(count * min(1.0, r)))
        for k, d in enumerate(mob):
            if k >= active_n or r <= 0.02:
                d.set_opacity(0.0)
                d.move_to([MEM_X, y_center, 0.0])
                continue
            u = (phases[k] + speed * state["t"]) % 1.0
            if dirs[k] > 0:
                x = ION_X_IN + u * (ION_X_OUT - ION_X_IN)
            else:
                x = ION_X_OUT - u * (ION_X_OUT - ION_X_IN)
            y = y_center + dys[k] + 0.03 * np.sin(TAU * u + k)
            edge_fade = min(1.0, u / 0.09, (1.0 - u) / 0.09)
            d.move_to([x, y, 0.0])
            d.set_opacity(float(edge_fade * min(1.0, 0.78 + 0.28 * r)))

    _update(dots, 0.0)
    dots.add_updater(_update)
    return dots


def make_tug_of_war(ca_len_tr, k_len_tr, y_ca_tr, y_k_tr, rope_mode_tr,
                    tremble_amp=0.0, seed=11):
    """Opposing GOLD (inward, left) and BLUE (outward, right) current arrows that merge into a rope."""
    state = {"t": 0.0}

    def _build():
        l_ca = max(0.0, float(ca_len_tr.get_value()))
        l_k = max(0.0, float(k_len_tr.get_value()))
        y_ca = float(y_ca_tr.get_value())
        y_k = float(y_k_tr.get_value())
        rm = float(np.clip(rope_mode_tr.get_value(), 0.0, 1.0))

        diff = (l_k - l_ca) / max(l_ca + l_k, 0.25)
        tremble = 0.0  # no decorative wobble: the knot moves only with the computed currents
        knot_x = MEM_X + rm * (0.68 * diff + tremble)
        knot_x = float(np.clip(knot_x, ION_X_IN + 0.35, ION_X_OUT - 0.35))

        ca_start_x = (1.0 - rm) * (MEM_X + 0.44) + rm * knot_x
        k_start_x = (1.0 - rm) * (MEM_X - 0.44) + rm * knot_x
        ca_end_x = max(ION_X_IN - 0.10, ca_start_x - l_ca)
        k_end_x = min(ION_X_OUT + 0.08, k_start_x + l_k)

        parts = VGroup()
        if l_ca > 0.12 and ca_start_x - ca_end_x > 0.14:
            a_ca = Arrow(
                [ca_start_x, y_ca, 0.0], [ca_end_x, y_ca, 0.0],
                buff=0.0, color=CA_COL, stroke_width=9.0,
                max_tip_length_to_length_ratio=0.28, max_stroke_width_to_length_ratio=12,
            )
            parts.add(a_ca)
        if l_k > 0.12 and k_end_x - k_start_x > 0.14:
            a_k = Arrow(
                [k_start_x, y_k, 0.0], [k_end_x, y_k, 0.0],
                buff=0.0, color=K_COL, stroke_width=9.0,
                max_tip_length_to_length_ratio=0.28, max_stroke_width_to_length_ratio=12,
            )
            parts.add(a_k)
        # Never show a lone floating knot when no arrows are present
        if rm > 0.15 and (l_ca > 0.12 or l_k > 0.12):
            knot = Circle(
                radius=0.115, color=VOLTAGE_COL, stroke_width=4.0,
                fill_color=BG, fill_opacity=1.0,
            ).move_to([knot_x, (y_ca + y_k) / 2.0, 0.0]).set_opacity(rm)
            parts.add(knot)
        return parts

    mob = always_redraw(_build)
    if False:
        mob.add_updater(lambda m, dt: state.__setitem__("t", state["t"] + dt))
    return mob


def current_lengths_at(t_ms, sim=SIM_NORM, scale=1.0):
    i_ca = abs(min(0.0, sim_val(sim, "I_CaL", t_ms)))
    i_k = max(0.0, sim_val(sim, "I_Kdr", t_ms))
    l_ca = float(np.clip(0.84 * i_ca * scale, 0.0, 1.35))
    l_k = float(np.clip(1.04 * i_k * scale, 0.0, 1.35))
    return l_ca, l_k


# ===========================================================================
# SCENE 00: HOOK (spoken, 12.025 s)
# ===========================================================================
class S00Hook(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        mem = MembraneWorld(na_state="empty", ito_open=False, ca_state="empty",
                            kdr_state="empty", ik1_open=0.05, ik1_dim=True)
        self.add(P, tag, mem)

        # Nerve spike (3 ms wide, peaks at +33 mV, computed from fast Na+/K+ ODE)
        t_nerve = ValueTracker(12.0)
        nerve_fill = make_voltage_fill(P, NERVE_T, NERVE_V, t_nerve, color=AXIS_COL, opacity=0.28)
        nerve_curve = make_live_curve(P, NERVE_T, NERVE_V, t_nerve, color=AXIS_COL, width=4.6)
        nerve_dot = make_voltage_dot(P, NERVE_T, NERVE_V, t_nerve, radius=0.12, color=AXIS_COL, trail_ms=14.0)
        nerve_readout = make_voltage_readout(NERVE_T, NERVE_V, t_nerve)
        # Placed cleanly above the ventricular plateau so nothing sits inside the depolarization fill
        nerve_lbl = T("nerve spike", size=26, color=AXIS_COL).move_to(P.pt(125.0, 31.0))
        nerve_ptr = Line(
            nerve_lbl.get_left() + LEFT * 0.08,
            P.pt(28.0, 31.0),
            color=AXIS_COL, stroke_width=2.6,
        )

        self.at("nerve spike")
        self.add(nerve_fill, nerve_curve, nerve_dot, nerve_readout)
        self.play(t_nerve.animate.set_value(42.0), run_time=1.15, rate_func=linear)
        d_gap = max(0.7, wait_dur(self, "excite a ventricular"))
        self.play(
            FadeIn(nerve_lbl),
            Create(nerve_ptr),
            t_nerve.animate.set_value(58.0),
            run_time=min(0.85, d_gap),
            rate_func=linear,
        )
        rem_n = wait_dur(self, "excite a ventricular")
        if rem_n > 0.25:
            nerve_flash = make_static_curve(P, NERVE_T, NERVE_V, 18.0, 36.0, color=VOLTAGE_COL, width=9.0, opacity=0.85)
            self.play(ShowPassingFlash(nerve_flash, time_width=0.55), run_time=rem_n)

        # Ventricular action potential (300 ms wide, computed from cardiac ODE)
        t_vent = ValueTracker(12.0)
        vent_fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_vent, color=TEAL, opacity=0.22)
        vent_curve = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_vent, color=VOLTAGE_COL, width=6.0)
        vent_dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_vent)
        vent_readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_vent)
        vent_lbl = T("ventricular cell", size=26, color=VOLTAGE_COL).move_to(P.pt(282.0, 24.0))

        self.at("excite a ventricular")
        self.remove(nerve_dot, nerve_readout)
        self.add(vent_fill, vent_curve, vent_dot, vent_readout)
        d_up = max(1.4, wait_dur(self, "stays depolarized"))
        self.play(
            t_vent.animate.set_value(82.0),
            FadeIn(vent_lbl),
            run_time=d_up,
            rate_func=linear,
        )

        # Sweep smoothly across the full 300 ms depolarized duration and back to rest
        self.at("stays depolarized")
        d_sweep = max(2.2, wait_dur(self, "what holds it"))
        self.play(t_vent.animate.set_value(325.0), run_time=d_sweep, rate_func=linear)

        # On the question, glide dot high onto the plateau and ask "What holds it up?"
        self.at("what holds it")
        q = T("What holds it up?", size=38, color=VOLTAGE_COL).move_to([0.0, 3.36, 0.0])
        full_fill = make_static_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 325.0, color=TEAL, opacity=0.22)
        full_trace = make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 325.0, color=VOLTAGE_COL, width=6.0)
        self.remove(vent_fill, vent_curve)
        self.add(full_fill, full_trace, vent_dot)
        rem = max(0.9, self.narration_s - self.elapsed() - 0.1)
        self.play(t_vent.animate.set_value(135.0), FadeIn(q, shift=UP * 0.1), run_time=rem)
        self.finish()


# ===========================================================================
# SCENE 01: TITLE BEAT (silent, 2.0 s)
# ===========================================================================
class S01Title(NarratedScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        mem = MembraneWorld(na_state="empty", ito_open=False, ca_state="empty",
                            kdr_state="empty", ik1_open=0.05, ik1_dim=True)
        nerve_fill = make_static_voltage_fill(P, NERVE_T, NERVE_V, 0.0, 58.0, color=AXIS_COL, opacity=0.28)
        nerve_curve = make_static_curve(P, NERVE_T, NERVE_V, 0.0, 58.0, color=AXIS_COL, width=4.6)
        nerve_lbl = T("nerve spike", size=26, color=AXIS_COL).move_to(P.pt(125.0, 31.0))
        nerve_ptr = Line(nerve_lbl.get_left() + LEFT * 0.08, P.pt(28.0, 31.0), color=AXIS_COL, stroke_width=2.6)
        vent_lbl = T("ventricular cell", size=26, color=VOLTAGE_COL).move_to(P.pt(282.0, 24.0))

        t_vent = ValueTracker(325.0)
        vent_fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_vent, color=TEAL, opacity=0.22)
        vent_curve = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_vent, color=VOLTAGE_COL, width=6.0)
        vent_dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_vent)

        title = T("The Tie That Holds", size=44, color=VOLTAGE_COL, font=TITLE_FONT).move_to([-1.2, 3.36, 0.0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.08)

        self.add(P, tag, mem, nerve_fill, nerve_curve, nerve_lbl, nerve_ptr, vent_lbl, vent_fill, vent_curve, vent_dot)
        # Rewind smoothly to t=16 ms (clear of '-90' y-tick label!)
        self.play(
            FadeIn(title, shift=UP * 0.08),
            GrowFromCenter(rule),
            FadeOut(nerve_fill), FadeOut(nerve_curve), FadeOut(nerve_lbl), FadeOut(nerve_ptr), FadeOut(vent_lbl),
            t_vent.animate.set_value(16.0),
            run_time=1.55,
            rate_func=smooth,
        )
        self.play(FadeOut(title), FadeOut(rule), run_time=0.45)
        self.finish()


# ===========================================================================
# SCENE 02: REST / PHASE 4 (spoken, 12.65 s)
# ===========================================================================
class S02Rest(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        mem = MembraneWorld(na_state="empty", ito_open=False, ca_state="empty",
                            kdr_state="empty", ik1_open=0.05, ik1_dim=True)

        t_tr = ValueTracker(16.0)
        live = make_live_curve(P, REST_T, REST_V, t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, REST_T, REST_V, t_tr)
        readout = make_voltage_readout(REST_T, REST_V, t_tr)

        self.add(P, tag, mem, live, dot, readout)

        # Highlight the ventricular cell cross-section while sweeping the resting baseline
        cell_focus = Rectangle(
            width=MEM_X1 - CELL_X0 + 0.14, height=MEM_Y1 - MEM_Y0 + 0.14,
            stroke_color=TEAL, stroke_width=4.0, fill_opacity=0.0,
        ).move_to([(CELL_X0 + MEM_X1) / 2.0, (MEM_Y0 + MEM_Y1) / 2.0, 0.0])
        d1 = max(1.0, wait_dur(self, "at rest"))
        self.play(
            ShowPassingFlash(cell_focus, time_width=0.55),
            t_tr.animate.set_value(185.0),
            run_time=d1,
            rate_func=linear,
        )

        # At rest (-90 mV): briskly draw rest line, open wide IK1 door, and start dense K+ flow!
        self.at("at rest")
        rest_ln = build_rest_line(P, with_label=True)
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)
        ik1_rate = ValueTracker(0.0)
        ik1_stream = make_ion_stream(Y_IK1, K_COL, direction=+1, count=22, spread_y=0.30,
                                     speed=1.10, rate_tracker=ik1_rate, seed=21, radius=0.115, bidir=True)
        self.add(ik1_stream)
        lit_doors = make_ik1_doors(mem.ik1_open, color=K_COL, opacity=1.0)
        d2 = max(1.5, wait_dur(self, "potassium current"))
        d2_open = min(1.5, d2 * 0.45)
        self.play(
            Create(rest_ln.line),
            FadeIn(rest_ln.label),
            mem.ik1_housing.animate.set_opacity(1.0),
            FadeOut(mem.ik1_doors), FadeIn(lit_doors),
            mem.ik1_open.animate.set_value(1.0),
            ik1_rate.animate.set_value(1.2),
            t_tr.animate.set_value(255.0),
            run_time=d2_open,
            rate_func=linear,
        )
        mem.ik1_doors = lit_doors
        if d2 - d2_open > 0.15:
            self.play(t_tr.animate.set_value(320.0), run_time=d2 - d2_open, rate_func=linear)

        self.at("potassium current")
        d3 = max(0.8, wait_dur(self, "IK1"))
        self.play(t_tr.animate.set_value(358.0), run_time=d3, rate_func=linear)

        self.at("IK1")
        rem = max(0.6, self.narration_s - self.elapsed() - 0.1)
        self.play(FadeIn(ik1_lbl), t_tr.animate.set_value(390.0), run_time=rem, rate_func=linear)
        self.finish()


# ===========================================================================
# SCENE 03: UPSTROKE & NOTCH (spoken, 12.175 s)
# ===========================================================================
class S03Upstroke(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="empty", ito_open=False, ca_state="empty",
                            kdr_state="empty", ik1_open=1.0, ik1_dim=False)
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)
        ik1_rate = ValueTracker(1.2)
        ik1_stream = make_ion_stream(Y_IK1, K_COL, direction=+1, count=22, spread_y=0.30,
                                     speed=1.10, rate_tracker=ik1_rate, seed=21, radius=0.115, bidir=True)

        t_tr = ValueTracker(16.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ik1_lbl, ik1_stream, fill, live, dot, readout)

        # Advance resting trace gently to stimulus at t=20 ms
        d0 = max(0.3, wait_dur(self, "sodium channels open"))
        self.play(t_tr.animate.set_value(19.5), run_time=d0, rate_func=linear)

        # Sodium channels open, CORAL Na+ dots rush inward
        self.at("sodium channels open")
        na_open_housing = make_channel_housing(Y_NA, 0.16, color=NA_COL, active=True)
        na_lbl = make_channel_label("Na⁺", Y_NA, NA_COL, size=28)
        na_rate = ValueTracker(0.0)
        na_stream = make_ion_stream(Y_NA, NA_COL, direction=-1, count=22, spread_y=0.12,
                                    speed=1.25, rate_tracker=na_rate, seed=31, radius=0.115)
        self.add(na_stream)
        d1 = max(0.6, wait_dur(self, "voltage shoots up"))
        self.play(
            Transform(mem.na_housing, na_open_housing),
            FadeIn(na_lbl),
            na_rate.animate.set_value(1.25),
            run_time=d1,
        )

        # Voltage shoots up past zero (+31 mV); IK1 swings almost shut and fades back
        self.at("voltage shoots up")
        d2 = max(1.2, wait_dur(self, "channels inactivate"))
        self.play(
            t_tr.animate.set_value(22.8),
            mem.ik1_open.animate.set_value(0.04),
            ik1_rate.animate.set_value(0.0),
            mem.ik1_housing.animate.set_opacity(0.38),
            ik1_lbl.animate.set_opacity(0.0),
            run_time=d2,
            rate_func=rush_into,
        )
        self.remove(mem.ik1_doors, ik1_lbl)
        mem.ik1_doors = make_ik1_doors(mem.ik1_open, color=K_COL, opacity=0.38)
        self.add(mem.ik1_doors)

        # Sodium channels inactivate: bar snaps across CORAL pore as last Na+ ions finish crossing
        self.at("channels inactivate")
        d3 = max(0.8, wait_dur(self, "brief outward potassium"))
        self.play(
            mem.na_bar.animate.set_opacity(1.0),
            na_rate.animate.set_value(0.0),
            t_tr.animate.set_value(25.5),
            run_time=d3,
            rate_func=linear,
        )

        # Brief outward potassium gate blinks open -> small notch (rich stream + brief outward arrow)
        self.at("brief outward potassium")
        ito_open_housing = make_channel_housing(Y_ITO, 0.10, color=K_COL, active=True)
        ito_rate = ValueTracker(0.0)
        ito_stream = make_ion_stream(Y_ITO, K_COL, direction=+1, count=22, spread_y=0.09,
                                     speed=1.22, rate_tracker=ito_rate, seed=37, radius=0.112)
        ito_arrow = Arrow(
            [MEM_X - 0.36, Y_ITO, 0.0], [MEM_X + 0.92, Y_ITO, 0.0],
            buff=0.0, color=K_COL, stroke_width=7.5,
            max_tip_length_to_length_ratio=0.28, max_stroke_width_to_length_ratio=12,
        )
        self.add(ito_stream)
        d4 = max(0.6, wait_dur(self, "cuts a small notch"))
        self.play(
            Transform(mem.ito_housing, ito_open_housing),
            mem.ito_plug.animate.set_opacity(0.0),
            GrowArrow(ito_arrow),
            ito_rate.animate.set_value(1.25),
            t_tr.animate.set_value(30.5),
            run_time=d4,
        )

        self.at("cuts a small notch")
        rem = max(0.8, self.narration_s - self.elapsed() - 0.1)
        self.play(t_tr.animate.set_value(36.5), run_time=rem, rate_func=linear)
        self.finish()


# ===========================================================================
# SCENE 04: HOLD OVER NOTCH (silent, 4.0 s)
# ===========================================================================
class S04HoldUpstroke(NarratedScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred", ito_open=True, ca_state="empty",
                            kdr_state="empty", ik1_open=0.04, ik1_dim=True)
        na_lbl = make_channel_label("Na⁺", Y_NA, NA_COL, size=28)

        ito_rate = ValueTracker(1.25)
        ito_stream = make_ion_stream(Y_ITO, K_COL, direction=+1, count=22, spread_y=0.09,
                                     speed=1.18, rate_tracker=ito_rate, seed=37, radius=0.112)
        ito_arrow = Arrow(
            [MEM_X - 0.36, Y_ITO, 0.0], [MEM_X + 0.92, Y_ITO, 0.0],
            buff=0.0, color=K_COL, stroke_width=7.5,
            max_tip_length_to_length_ratio=0.28, max_stroke_width_to_length_ratio=12,
        )

        t_tr = ValueTracker(36.5)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, na_lbl, ito_stream, ito_arrow, fill, live, dot, readout)

        # First half: brief K+ current keeps flowing as voltage rides over notch into plateau
        self.play(
            t_tr.animate.set_value(50.0),
            mem.na_housing.animate.set_opacity(0.45),
            mem.na_bar.animate.set_opacity(0.45),
            FadeOut(na_lbl),
            run_time=2.0,
            rate_func=linear,
        )
        # Second half: brief notch gate closes and tapers off cleanly
        ito_closed = make_channel_housing(Y_ITO, 0.10, color=MEMBRANE_STROKE, active=False)
        self.play(
            t_tr.animate.set_value(64.0),
            ito_rate.animate.set_value(0.0),
            FadeOut(ito_arrow),
            mem.ito_plug.animate.set_opacity(0.95),
            Transform(mem.ito_housing, ito_closed),
            run_time=1.9,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 05: THE PLATEAU PUZZLE (spoken, 9.9 s)
# ===========================================================================
class S05Puzzle(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="empty",
                            kdr_state="empty", ik1_open=0.04, ik1_dim=True)

        t_tr = ValueTracker(64.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)
        self.add(P, tag, rest_ln, mem, fill, live, dot, readout)

        # Glide smoothly across plateau; barred CORAL Na+ pulses clearly once to show it is not the cause
        self.at("voltage does not")
        na_ring = RoundedRectangle(
            corner_radius=0.10, width=1.10, height=0.56,
            color=NA_COL, stroke_width=5.0, fill_color=NA_COL, fill_opacity=0.18,
        ).move_to([MEM_X, Y_NA, 0.0])
        d1 = max(1.2, wait_dur(self, "hangs near zero"))
        self.play(
            t_tr.animate.set_value(100.0),
            run_time=d1 * 0.52,
            rate_func=linear,
        )
        self.play(
            t_tr.animate.set_value(135.0),
            run_time=d1 * 0.48,
            rate_func=linear,
        )

        # Bracket + live elapsed ms counter + 0 mV reference line grow continuously across plateau
        self.at("hangs near zero")
        zero_ln = DashedLine(
            P.pt(0.0, 0.0), P.pt(400.0, 0.0),
            color=AXIS_COL, stroke_width=2.2, dash_length=0.14,
        ).set_opacity(0.55)
        br_end = ValueTracker(135.0)
        _, br_mob, br_lbl = build_plateau_bracket(P, t_start=48.0, t_end_tracker=br_end, t_end=248.0, with_label=True)
        xm_live = P.pt(162.0, 0.0)[0]
        live_ms = always_redraw(
            lambda: M(f"{max(0.0, br_end.get_value() - 48.0):.0f} ms", size=28, color=VOLTAGE_COL).move_to([xm_live, -0.96, 0.0])
        )
        self.add(br_mob, live_ms)
        d2 = max(2.0, wait_dur(self, "this long stretch"))
        self.play(
            Create(zero_ln),
            t_tr.animate.set_value(175.0),
            br_end.animate.set_value(175.0),
            run_time=min(1.4, d2 * 0.42),
            rate_func=linear,
        )
        self.play(
            t_tr.animate.set_value(225.0),
            br_end.animate.set_value(225.0),
            run_time=max(0.8, d2 - min(1.4, d2 * 0.42)),
            rate_func=linear,
        )

        self.at("this long stretch")
        live_ms.clear_updaters()
        plat_flash = make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 48.0, 248.0,
                                       color=VOLTAGE_COL, width=12.0, opacity=0.75)
        rem = max(1.2, self.narration_s - self.elapsed() - 0.1)
        self.play(
            t_tr.animate.set_value(248.0),
            br_end.animate.set_value(248.0),
            FadeOut(zero_ln),
            swap(live_ms, br_lbl, run_time=0.7),
            ShowPassingFlash(plat_flash, time_width=0.50),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 06: TWO OPPOSING CURRENTS (spoken, 12.35 s)
# ===========================================================================
class S06Tug(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="empty",
                            kdr_state="empty", ik1_open=0.04, ik1_dim=True)

        t_tr = ValueTracker(248.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)
        br_grp, _, _ = build_plateau_bracket(P, t_start=48.0, t_end=248.0, with_label=True)

        self.add(P, tag, rest_ln, mem, br_grp, fill, live, dot, readout)

        # Briskly rewind dot & fill to start of plateau, then highlight the two membrane channel slots
        self.at("two sets of")
        d0 = max(1.8, wait_dur(self, "L type calcium"))
        d0_rew = min(2.1, d0 * 0.62)
        self.play(t_tr.animate.set_value(50.0), FadeOut(br_grp), run_time=d0_rew, rate_func=smooth)
        slot_ca = RoundedRectangle(
            corner_radius=0.10, width=1.05, height=0.68,
            color=AXIS_COL, stroke_width=4.0, fill_color=AXIS_COL, fill_opacity=0.14,
        ).move_to([MEM_X, Y_CA, 0.0])
        slot_kdr = RoundedRectangle(
            corner_radius=0.10, width=1.05, height=0.92,
            color=AXIS_COL, stroke_width=4.0, fill_color=AXIS_COL, fill_opacity=0.14,
        ).move_to([MEM_X, Y_KDR, 0.0])
        if d0 - d0_rew > 0.3:
            self.play(FadeIn(slot_ca), FadeIn(slot_kdr), run_time=d0 - d0_rew)
        else:
            self.add(slot_ca, slot_kdr)

        # L-type calcium channel opens briskly: dense vivid GOLD dots flow inward, thick GOLD arrow grows
        self.at("L type calcium")
        ca_open_h = make_channel_housing(Y_CA, 0.20, color=CA_COL, active=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        ca_rate = ValueTracker(0.0)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.15, rate_tracker=ca_rate, seed=61, radius=0.115)

        ca_len = ValueTracker(0.0)
        k_len = ValueTracker(0.0)
        y_ca_tr = ValueTracker(0.14)
        y_k_tr = ValueTracker(-0.22)
        rope_tr = ValueTracker(0.0)
        arrows = make_tug_of_war(ca_len, k_len, y_ca_tr, y_k_tr, rope_tr)

        mem.ca_state_active.set_value(1.0)
        self.add(ca_stream, arrows)
        l_ca0, l_k0 = current_lengths_at(70.0)
        d1 = max(1.8, wait_dur(self, "delayed rectifier potassium"))
        d1_open = min(1.25, d1 * 0.45)
        self.play(
            FadeOut(slot_ca),
            Transform(mem.ca_housing, ca_open_h),
            mem.ca_gate_val.animate.set_value(1.0),
            FadeIn(ca_lbl),
            ca_rate.animate.set_value(1.25),
            ca_len.animate.set_value(l_ca0),
            t_tr.animate.set_value(58.0),
            run_time=d1_open,
        )
        if d1 - d1_open > 0.15:
            self.play(t_tr.animate.set_value(68.0), run_time=d1 - d1_open, rate_func=linear)

        # Delayed-rectifier potassium channels open briskly: dense vivid BLUE dots flow outward, thick BLUE arrow grows
        self.at("delayed rectifier potassium")
        ikr_open = make_channel_housing(Y_IKR, 0.13, color=K_COL, active=True)
        iks_open = make_channel_housing(Y_IKS, 0.13, color=K_COL, active=True)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
        k_rate = ValueTracker(0.0)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=67, radius=0.112)
        self.add(k_stream_r, k_stream_s)
        rem = max(1.8, self.narration_s - self.elapsed() - 0.1)
        rem_open = min(1.25, rem * 0.45)
        self.play(
            FadeOut(slot_kdr),
            Transform(mem.ikr_housing, ikr_open),
            Transform(mem.iks_housing, iks_open),
            FadeIn(kdr_lbl),
            k_rate.animate.set_value(1.25),
            k_len.animate.set_value(max(l_k0, l_ca0 * 0.96)),
            t_tr.animate.set_value(74.0),
            run_time=rem_open,
        )
        if rem - rem_open > 0.15:
            self.play(t_tr.animate.set_value(82.0), run_time=rem - rem_open, rate_func=linear)
        self.finish()


# ===========================================================================
# SCENE 07: HOLD OPPOSING CURRENTS (silent, 4.0 s)
# ===========================================================================
class S07HoldTug(NarratedScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)

        ca_rate = ValueTracker(1.25)
        k_rate = ValueTracker(1.25)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.15, rate_tracker=ca_rate, seed=61, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=67, radius=0.112)

        l_ca0, _ = current_lengths_at(70.0)
        ca_len = ValueTracker(l_ca0)
        k_len = ValueTracker(l_ca0 * 0.96)
        arrows = make_tug_of_war(ca_len, k_len, ValueTracker(0.14), ValueTracker(-0.22), ValueTracker(0.0))

        t_tr = ValueTracker(82.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ca_stream, k_stream_r, k_stream_s,
                 arrows, fill, live, dot, readout)
        self.play(t_tr.animate.set_value(98.0), run_time=3.9, rate_func=linear)
        self.finish()


# ===========================================================================
# SCENE 08: THE ONE IDEA — A NEAR TIE (spoken, 13.975 s)
# ===========================================================================
class S08Idea(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)

        ca_rate = ValueTracker(1.25)
        k_rate = ValueTracker(1.25)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.15, rate_tracker=ca_rate, seed=61, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=67, radius=0.112)

        l_ca0, _ = current_lengths_at(70.0)
        ca_len = ValueTracker(l_ca0)
        k_len = ValueTracker(l_ca0 * 0.96)
        y_ca_tr = ValueTracker(0.14)
        y_k_tr = ValueTracker(-0.22)
        rope_tr = ValueTracker(0.0)
        arrows = make_tug_of_war(ca_len, k_len, y_ca_tr, y_k_tr, rope_tr, tremble_amp=0.02, seed=8)

        t_tr = ValueTracker(98.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ca_stream, k_stream_r, k_stream_s,
                 arrows, fill, live, dot, readout)

        # Glide into "the plateau is" with zero dead pause
        d0 = max(0.5, wait_dur(self, "the plateau is"))
        self.play(t_tr.animate.set_value(110.0), run_time=d0, rate_func=linear)

        # Slide the two arrows together into a tug-of-war rope across the membrane
        self.at("the plateau is")
        tie_txt = T("A near tie", size=38, color=VOLTAGE_COL).move_to([0.0, 3.36, 0.0])
        d1 = max(1.4, wait_dur(self, "inward and outward"))
        self.play(
            y_ca_tr.animate.set_value(Y_ROPE),
            y_k_tr.animate.set_value(Y_ROPE),
            rope_tr.animate.set_value(1.0),
            ca_len.animate.set_value(1.12),
            k_len.animate.set_value(1.12),
            FadeIn(tie_txt, shift=UP * 0.08),
            t_tr.animate.set_value(130.0),
            run_time=d1,
        )

        self.at("inward and outward")
        d2 = max(1.5, wait_dur(self, "voltage changes only"))
        self.play(t_tr.animate.set_value(152.0), run_time=d2, rate_func=linear)

        self.at("voltage changes only")
        d3 = max(1.5, wait_dur(self, "drifting down as"))
        self.play(
            t_tr.animate.set_value(172.0),
            k_len.animate.set_value(1.18),
            ca_len.animate.set_value(1.08),
            run_time=d3,
            rate_func=linear,
        )

        self.at("drifting down as")
        rem = max(1.2, self.narration_s - self.elapsed() - 0.1)
        self.play(
            t_tr.animate.set_value(190.0),
            k_len.animate.set_value(1.24),
            ca_len.animate.set_value(1.04),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 09: WATCH THE NEAR TIE (silent, 3.0 s)
# ===========================================================================
class S09Watch(NarratedScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
        tie_txt = T("A near tie", size=38, color=VOLTAGE_COL).move_to([0.0, 3.36, 0.0])

        ca_rate = ValueTracker(1.25)
        k_rate = ValueTracker(1.25)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.15, rate_tracker=ca_rate, seed=61, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=67, radius=0.112)

        arrows = make_tug_of_war(ValueTracker(1.04), ValueTracker(1.24), ValueTracker(Y_ROPE),
                                 ValueTracker(Y_ROPE), ValueTracker(1.0), tremble_amp=0.04, seed=9)

        t_tr = ValueTracker(190.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, tie_txt, ca_stream, k_stream_r, k_stream_s,
                 arrows, fill, live, dot, readout)
        self.play(t_tr.animate.set_value(204.0), run_time=2.9, rate_func=linear)
        self.finish()


# ===========================================================================
# SCENE 10: WHY DOESN'T RESTING K+ DRAG IT DOWN? (spoken, 9.15 s)
# ===========================================================================
class S10Why(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
        tie_txt = T("A near tie", size=38, color=VOLTAGE_COL).move_to([0.0, 3.36, 0.0])

        ca_rate = ValueTracker(1.25)
        k_rate = ValueTracker(1.25)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.15, rate_tracker=ca_rate, seed=61, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=67, radius=0.112)

        arrows = make_tug_of_war(ValueTracker(1.04), ValueTracker(1.24), ValueTracker(Y_ROPE),
                                 ValueTracker(Y_ROPE), ValueTracker(1.0), tremble_amp=0.03, seed=10)

        t_tr = ValueTracker(204.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, tie_txt, ca_stream, k_stream_r, k_stream_s,
                 arrows, fill, live, dot, readout)

        # Crisp dashed GHOST outline of wide-open resting IK1 doorway
        self.at("at rest")
        ghost_doors = make_ik1_doors(None, color=K_COL, opacity=0.90, dashed=True, static_open=1.0)
        at_rest_lbl = make_channel_label("at rest", Y_IK1, K_COL, size=28)
        d1 = max(1.4, wait_dur(self, "why doesn't it"))
        self.play(FadeOut(tie_txt), FadeIn(ghost_doors), FadeIn(at_rest_lbl), t_tr.animate.set_value(210.0), run_time=min(1.6, d1))
        if d1 > 1.65:
            self.play(t_tr.animate.set_value(216.0), run_time=d1 - 1.6, rate_func=linear)

        # Ghost dashed WHITE line dropping straight to -90 mV + "?" beside IK1 door
        self.at("why doesn't it")
        p_top = P.pt(216.0, v_norm(216.0))
        p_bot = P.pt(232.0, -90.0)
        ghost_drop = DashedLine(p_top, p_bot, color=VOLTAGE_COL, stroke_width=4.2, dash_length=0.14).set_opacity(0.75)
        qmark = T("?", size=48, color=VOLTAGE_COL, weight=BOLD).move_to([2.58, Y_IK1, 0.0])
        rem = max(1.2, self.narration_s - self.elapsed() - 0.1)
        self.play(Create(ghost_drop), FadeIn(qmark), t_tr.animate.set_value(222.0), run_time=rem)
        self.finish()


# ===========================================================================
# SCENE 11: INWARD RECTIFIER IK1 (spoken, 14.25 s)
# ===========================================================================
class S11Rectifier(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)

        ghost_doors = make_ik1_doors(None, color=K_COL, opacity=0.90, dashed=True, static_open=1.0)
        at_rest_lbl = make_channel_label("at rest", Y_IK1, K_COL, size=28)
        p_top = P.pt(216.0, v_norm(216.0))
        p_bot = P.pt(232.0, -90.0)
        ghost_drop = DashedLine(p_top, p_bot, color=VOLTAGE_COL, stroke_width=4.2, dash_length=0.14).set_opacity(0.75)
        qmark = T("?", size=48, color=VOLTAGE_COL, weight=BOLD).move_to([2.58, Y_IK1, 0.0])

        ca_rate = ValueTracker(1.25)
        k_rate = ValueTracker(1.25)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.15, rate_tracker=ca_rate, seed=61, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=67, radius=0.112)

        ca_len = ValueTracker(1.04)
        k_len = ValueTracker(1.24)
        arrows = make_tug_of_war(ca_len, k_len, ValueTracker(Y_ROPE), ValueTracker(Y_ROPE),
                                 ValueTracker(1.0), tremble_amp=0.03, seed=11)

        t_tr = ValueTracker(222.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ghost_doors, at_rest_lbl,
                 ghost_drop, qmark, ca_stream, k_stream_r, k_stream_s, arrows, fill, live, dot, readout)

        # Glide steadily across opening sentence to "passes current well"
        d0 = max(1.0, wait_dur(self, "passes current well"))
        self.play(t_tr.animate.set_value(228.0), run_time=d0, rate_func=linear)

        self.at("passes current well")
        d1 = max(1.0, wait_dur(self, "largely shuts"))
        self.play(ghost_doors.animate.set_opacity(1.0), t_tr.animate.set_value(232.0), run_time=d1)

        # Largely shuts at plateau voltages: fade ghosts, light up real nearly-shut IK1 crack
        self.at("largely shuts")
        ik1_shut_lbl = make_channel_label("IK1\nlargely\nshut", Y_IK1 - 0.14, K_COL, size=26, line_spacing=0.72)
        lit_doors = make_ik1_doors(mem.ik1_open, color=K_COL, opacity=1.0)
        d2 = max(1.4, wait_dur(self, "total conductance"))
        self.play(
            FadeOut(ghost_drop), FadeOut(qmark), FadeOut(ghost_doors),
            swap(at_rest_lbl, ik1_shut_lbl, run_time=0.8),
            mem.ik1_housing.animate.set_opacity(1.0),
            FadeOut(mem.ik1_doors), FadeIn(lit_doors),
            t_tr.animate.set_value(236.0),
            run_time=min(1.6, d2),
        )
        mem.ik1_doors = lit_doors
        if d2 > 1.65:
            self.play(t_tr.animate.set_value(239.0), run_time=d2 - 1.6, rate_func=linear)

        # Total conductance is low -> visibly thinner yet vivid balanced GOLD & BLUE streams + smaller arrows
        self.at("total conductance")
        small_lbl = T("small currents", size=28, color=VOLTAGE_COL).move_to([3.80, -3.12, 0.0])
        d3 = max(1.2, wait_dur(self, "small currents"))
        self.play(
            ca_rate.animate.set_value(0.64),
            k_rate.animate.set_value(0.64),
            ca_len.animate.set_value(0.78),
            k_len.animate.set_value(0.84),
            t_tr.animate.set_value(242.0),
            run_time=d3,
        )

        self.at("small currents")
        rem = max(0.8, self.narration_s - self.elapsed() - 0.1)
        self.play(FadeIn(small_lbl, shift=UP * 0.06), t_tr.animate.set_value(246.0), run_time=rem)
        self.finish()


# ===========================================================================
# SCENE 12: HOLD SMALL CURRENTS (silent, 5.0 s)
# ===========================================================================
class S12HoldRectifier(NarratedScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=False)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
        ik1_shut_lbl = make_channel_label("IK1\nlargely\nshut", Y_IK1 - 0.14, K_COL, size=26, line_spacing=0.72)
        small_lbl = T("small currents", size=28, color=VOLTAGE_COL).move_to([3.80, -3.12, 0.0])

        ca_rate = ValueTracker(0.64)
        k_rate = ValueTracker(0.64)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.10, rate_tracker=ca_rate, seed=61, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.10, rate_tracker=k_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.08, rate_tracker=k_rate, seed=67, radius=0.112)

        ca_len = ValueTracker(0.78)
        k_len = ValueTracker(0.84)
        arrows = make_tug_of_war(ca_len, k_len, ValueTracker(Y_ROPE),
                                 ValueTracker(Y_ROPE), ValueTracker(1.0), tremble_amp=0.04, seed=12)

        t_tr = ValueTracker(246.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ik1_shut_lbl, small_lbl,
                 ca_stream, k_stream_r, k_stream_s, arrows, fill, live, dot, readout)
        self.play(
            t_tr.animate.set_value(258.0),
            ca_len.animate.set_value(0.74),
            k_len.animate.set_value(0.88),
            run_time=4.9,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 13: PREDICT — BLOCK ONE OUTWARD CURRENT (spoken, 9.2 s)
# ===========================================================================
def build_predict_state(tremble=0.04):
    """Exact end-of-s13 world, shared with S14Pause.backdrop() for a frame-identical handoff."""
    P = build_plot()
    tag = build_scope_tag()
    rest_ln = build_rest_line(P, with_label=True)
    mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                        kdr_state="open", ik1_open=0.04, ik1_dim=False, herg_barred=True)
    ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
    kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
    ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)
    br_grp, _, _ = build_plateau_bracket(P, t_start=48.0, t_end=248.0, with_label=True)

    ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                speed=1.08, rate_tracker=ValueTracker(0.68), seed=61, radius=0.115)
    k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=14, spread_y=0.08,
                                 speed=1.08, rate_tracker=ValueTracker(0.68), seed=67, radius=0.112)

    arrows = make_tug_of_war(ValueTracker(0.86), ValueTracker(0.54), ValueTracker(Y_ROPE),
                             ValueTracker(Y_ROPE), ValueTracker(1.0), tremble_amp=tremble, seed=14)

    t_tr = ValueTracker(50.0)
    fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
    live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
    dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
    readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)
    return VGroup(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ik1_lbl, br_grp,
                  ca_stream, k_stream_s, arrows, fill, live, dot, readout)


class S13Predict(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=False, herg_barred=False)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
        ik1_shut_lbl = make_channel_label("IK1\nlargely\nshut", Y_IK1 - 0.14, K_COL, size=26, line_spacing=0.72)
        small_lbl = T("small currents", size=28, color=VOLTAGE_COL).move_to([3.80, -3.12, 0.0])

        ca_rate = ValueTracker(0.68)
        kr_rate = ValueTracker(0.68)
        ks_rate = ValueTracker(0.68)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.08, rate_tracker=ca_rate, seed=61, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=14, spread_y=0.08,
                                     speed=1.08, rate_tracker=kr_rate, seed=63, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=14, spread_y=0.08,
                                     speed=1.08, rate_tracker=ks_rate, seed=67, radius=0.112)

        ca_len = ValueTracker(0.86)
        k_len = ValueTracker(0.86)
        arrows = make_tug_of_war(ca_len, k_len, ValueTracker(Y_ROPE), ValueTracker(Y_ROPE),
                                 ValueTracker(1.0), tremble_amp=0.035, seed=13)

        t_tr = ValueTracker(258.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ik1_shut_lbl, small_lbl,
                 ca_stream, k_stream_r, k_stream_s, arrows, fill, live, dot, readout)

        # Rewind dot & fill cleanly to plateau start across full opening phrase
        self.at("so this balance")
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)
        br_grp, _, _ = build_plateau_bracket(P, t_start=48.0, t_end=248.0, with_label=True)
        d0 = max(1.8, wait_dur(self, "block just one"))
        self.play(
            t_tr.animate.set_value(50.0),
            FadeOut(small_lbl),
            swap(ik1_shut_lbl, ik1_lbl, run_time=0.8),
            FadeIn(br_grp),
            run_time=d0,
        )

        # Physically slide white blocker bar across upper IKr pore -> stream thins & BLUE arrow shrinks
        self.at("block just one")
        mem.herg_bar.shift(RIGHT * 0.65)
        d1 = max(1.5, wait_dur(self, "what happens to"))
        self.play(
            mem.herg_bar.animate.shift(LEFT * 0.65).set_opacity(1.0),
            kr_rate.animate.set_value(0.0),
            k_len.animate.set_value(0.54),
            run_time=min(1.6, d1),
        )
        if d1 > 1.65:
            # Keep active currents visibly pulling during the remainder before the question
            self.wait(d1 - 1.6)

        self.at("what happens to")
        q = question_card(PREDICT_Q, **PREDICT_CARD_KW)
        self.play(FadeIn(q, shift=UP * 0.08), run_time=0.9)
        self.finish()


# ===========================================================================
# SCENE 14: PREDICT PAUSE (silent, 4.5 s — PredictPause)
# ===========================================================================
class S14Pause(PredictPause):
    QUESTION = PREDICT_Q
    CARD = PREDICT_CARD_KW
    RING_AT = (6.05, -3.12, 0.0)
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_state(tremble=0.035)


# ===========================================================================
# SCENE 15: ANSWER — LENGTHENED PLATEAU, hERG, LONGER QT (spoken, 13.675 s)
# ===========================================================================
def build_qt_strip(P, long_frac_tr):
    """Two plain horizontal QT bars in the open lower area of the plot (clear of traces & rest line)."""
    strip_box = RoundedRectangle(
        corner_radius=0.10, width=4.05, height=1.18,
        stroke_color=AXIS_COL, stroke_width=2.0,
        fill_color=BG, fill_opacity=0.94,
    ).move_to([-3.12, -1.04, 0.0])

    x_lbl = -4.70
    x_bar = -4.18
    y_top = -0.78
    y_bot = -1.30
    base_w = 2.00
    ext_w = 2.52

    lbl1 = T("QT", size=26, color=AXIS_COL).move_to([x_lbl, y_top, 0.0])
    bar1 = Rectangle(width=base_w, height=0.22, fill_color=AXIS_COL, fill_opacity=0.85, stroke_width=0)
    bar1.move_to([x_bar + base_w / 2.0, y_top, 0.0])

    lbl2 = T("QT", size=26, color=VOLTAGE_COL).move_to([x_lbl, y_bot, 0.0])
    bar2 = always_redraw(
        lambda: Rectangle(
            width=base_w + (ext_w - base_w) * float(np.clip(long_frac_tr.get_value(), 0.0, 1.0)),
            height=0.24, fill_color=VOLTAGE_COL, fill_opacity=0.95, stroke_width=0,
        ).move_to([
            x_bar + (base_w + (ext_w - base_w) * float(np.clip(long_frac_tr.get_value(), 0.0, 1.0))) / 2.0,
            y_bot, 0.0,
        ])
    )
    return VGroup(strip_box, lbl1, bar1, lbl2, bar2)


class S15Answer(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=False, herg_barred=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)
        br_grp, _, _ = build_plateau_bracket(P, t_start=48.0, t_end=248.0, with_label=True)
        q = question_card(PREDICT_Q, **PREDICT_CARD_KW)

        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.08, rate_tracker=ValueTracker(0.68), seed=61, radius=0.115)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=14, spread_y=0.08,
                                     speed=1.08, rate_tracker=ValueTracker(0.68), seed=67, radius=0.112)

        arrows = make_tug_of_war(ValueTracker(0.86), ValueTracker(0.54), ValueTracker(Y_ROPE),
                                 ValueTracker(Y_ROPE), ValueTracker(1.0), tremble_amp=0.03, seed=15)

        t_tr = ValueTracker(50.0)
        fill = make_voltage_fill(P, SIM_HERG["t"], SIM_HERG["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_HERG["t"], SIM_HERG["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_HERG["t"], SIM_HERG["V"], t_tr)
        readout = make_voltage_readout(SIM_HERG["t"], SIM_HERG["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ik1_lbl, br_grp, q,
                 ca_stream, k_stream_s, arrows, fill, live, dot, readout)

        # Dissolve question card; show ghost normal trace; draw ODE hERG-blocked curve PAST bracket
        self.at("it lengthens")
        ghost_norm = make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 325.0,
                                       color=GHOST_COL, width=3.5, opacity=0.55, dashed=True)
        self.add(ghost_norm)
        self.bring_to_front(live, dot)
        d0 = max(2.5, wait_dur(self, "called h e r g"))
        self.play(
            FadeOut(q),
            FadeIn(ghost_norm),
            t_tr.animate.set_value(272.0),
            run_time=d0,
            rate_func=linear,
        )

        # Label the partly barred channel 'hERG'
        self.at("called h e r g")
        herg_lbl = make_channel_label("hERG", Y_IKR, K_COL, size=28)
        d1 = max(1.5, wait_dur(self, "the longer plateau"))
        self.play(
            swap(kdr_lbl, herg_lbl, run_time=0.7),
            t_tr.animate.set_value(296.0),
            run_time=d1,
            rate_func=linear,
        )

        # Swap out plateau bracket cleanly BEFORE bringing in QT strip (zero overlap!)
        self.at("the longer plateau")
        qt_frac = ValueTracker(0.0)
        qt_strip = build_qt_strip(P, qt_frac)
        d2 = max(1.2, wait_dur(self, "longer QT interval"))
        self.play(
            swap(br_grp, qt_strip, run_time=1.0),
            t_tr.animate.set_value(310.0),
            run_time=d2,
            rate_func=linear,
        )

        self.at("longer QT interval")
        rem = max(1.0, self.narration_s - self.elapsed() - 0.1)
        self.play(qt_frac.animate.set_value(0.65), t_tr.animate.set_value(320.0), run_time=rem, rate_func=linear)
        self.finish()


# ===========================================================================
# SCENE 16: HOLD LENGTHENED PLATEAU & QT BAR (silent, 5.0 s)
# ===========================================================================
class S16HoldAnswer(NarratedScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=False, herg_barred=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        herg_lbl = make_channel_label("hERG", Y_IKR, K_COL, size=28)
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)

        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.10, rate_tracker=ValueTracker(0.68), seed=61, radius=0.115)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=14, spread_y=0.08,
                                     speed=1.10, rate_tracker=ValueTracker(0.68), seed=67, radius=0.112)
        arrows = make_tug_of_war(ValueTracker(0.86), ValueTracker(0.54), ValueTracker(Y_ROPE),
                                 ValueTracker(Y_ROPE), ValueTracker(1.0), tremble_amp=0.035, seed=16)

        ghost_norm = make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 325.0,
                                       color=GHOST_COL, width=3.5, opacity=0.55, dashed=True)
        qt_frac = ValueTracker(0.65)
        qt_strip = build_qt_strip(P, qt_frac)

        t_tr = ValueTracker(320.0)
        fill = make_voltage_fill(P, SIM_HERG["t"], SIM_HERG["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_HERG["t"], SIM_HERG["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_HERG["t"], SIM_HERG["V"], t_tr)
        readout = make_voltage_readout(SIM_HERG["t"], SIM_HERG["V"], t_tr)

        self.add(P, tag, rest_ln, mem, ca_lbl, herg_lbl, ik1_lbl, ca_stream, k_stream_s,
                 arrows, fill, ghost_norm, qt_strip, live, dot, readout)

        # Finish longer plateau & repolarize smoothly to -90 mV by t=358 ms (well left of 'rest'!)
        self.play(
            t_tr.animate.set_value(358.0),
            qt_frac.animate.set_value(1.0),
            run_time=4.8,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 17: REPOLARIZATION RESERVE (spoken, 11.8 s)
# ===========================================================================
class S17Reserve(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="dim",
                            kdr_state="open", ik1_open=0.04, ik1_dim=False, herg_barred=True)
        herg_lbl = make_channel_label("hERG", Y_IKR, K_COL, size=28)
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)

        ghost_norm = make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 325.0,
                                       color=GHOST_COL, width=3.5, opacity=0.55, dashed=True)
        long_fill = make_static_voltage_fill(P, SIM_HERG["t"], SIM_HERG["V"], 0.0, 358.0, color=TEAL, opacity=0.20)
        long_curve = make_static_curve(P, SIM_HERG["t"], SIM_HERG["V"], 0.0, 358.0,
                                       color=VOLTAGE_COL, width=6.0)
        qt_strip = build_qt_strip(P, ValueTracker(1.0))

        kr_rate = ValueTracker(0.0)
        ks_rate = ValueTracker(0.95)
        k1_rate = ValueTracker(0.0)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=16, spread_y=0.08,
                                     speed=1.15, rate_tracker=kr_rate, seed=71, radius=0.115)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=18, spread_y=0.09,
                                     speed=1.15, rate_tracker=ks_rate, seed=73, radius=0.115)
        k_stream_1 = make_ion_stream(Y_IK1, K_COL, direction=+1, count=18, spread_y=0.28,
                                     speed=0.95, rate_tracker=k1_rate, seed=79, radius=0.112)

        self.add(P, tag, rest_ln, mem, herg_lbl, ik1_lbl,
                 long_fill, ghost_norm, long_curve, qt_strip, k_stream_r, k_stream_s, k_stream_1)

        # Briskly lift bar and morph trace & fill back to normal shape, then flow vibrant K+ streams
        self.at("losing one current")
        norm_fill = make_static_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 325.0, color=TEAL, opacity=0.20)
        norm_curve = make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 325.0,
                                       color=VOLTAGE_COL, width=6.0)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)
        d0 = max(2.0, wait_dur(self, "several potassium currents"))
        d0_morph = min(1.7, d0 * 0.45)
        self.play(
            FadeOut(qt_strip), FadeOut(ghost_norm),
            mem.herg_bar.animate.shift(RIGHT * 0.55).set_opacity(0.0),
            Transform(long_fill, norm_fill),
            Transform(long_curve, norm_curve),
            swap(herg_lbl, kdr_lbl, run_time=0.8),
            kr_rate.animate.set_value(1.10),
            ks_rate.animate.set_value(1.10),
            run_time=d0_morph,
        )
        if d0 - d0_morph > 0.3:
            t_rep = ValueTracker(235.0)
            rep_dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_rep)
            rep_readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_rep)
            self.add(rep_dot, rep_readout)
            self.play(t_rep.animate.set_value(330.0), run_time=d0 - d0_morph, rate_func=linear)
            self.remove(rep_dot, rep_readout)

        # Three BLUE channels pulse in turn; one dims and IKs ramps up strongly (IK1 stays shut!)
        self.at("several potassium currents")
        r1 = RoundedRectangle(corner_radius=0.10, width=0.92, height=0.46, color=K_COL, stroke_width=5.0).move_to([MEM_X, Y_IKR, 0])
        r2 = RoundedRectangle(corner_radius=0.10, width=0.92, height=0.46, color=K_COL, stroke_width=5.0).move_to([MEM_X, Y_IKS, 0])
        r3 = RoundedRectangle(corner_radius=0.12, width=1.00, height=1.10, color=K_COL, stroke_width=5.0).move_to([MEM_X, Y_IK1, 0])
        self.play(FadeIn(r1), run_time=0.52)
        self.play(FadeOut(r1), FadeIn(r2), run_time=0.52)
        self.play(FadeOut(r2), run_time=0.52)

        d1 = max(1.2, wait_dur(self, "repolarization reserve"))
        iks_boost = RoundedRectangle(
            corner_radius=0.10, width=0.96, height=0.48,
            color=K_COL, stroke_width=4.5, fill_color=K_COL, fill_opacity=0.14,
        ).move_to([MEM_X, Y_IKS, 0])
        self.play(
            mem.ikr_housing.animate.set_opacity(0.30),
            kr_rate.animate.set_value(0.10),
            ks_rate.animate.set_value(1.45),
            FadeIn(iks_boost),
            run_time=d1,
        )

        self.at("repolarization reserve")
        res_lbl = T("repolarization reserve", size=36, color=K_COL).move_to([0.0, 3.36, 0.0])
        self.play(FadeIn(res_lbl, shift=UP * 0.08), run_time=0.85)
        self.finish()


# ===========================================================================
# SCENE 18: HOW THE TIE BREAKS — Ca2+ INACTIVATION (spoken, 15.325 s)
# ===========================================================================
class S18Break(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="open",
                            kdr_state="open", ik1_open=0.04, ik1_dim=True)
        ca_lbl = make_channel_label("L-type\ncalcium", Y_CA, CA_COL, size=28)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)

        ca_rate = ValueTracker(1.10)
        k_rate = ValueTracker(1.15)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=22, spread_y=0.14,
                                    speed=1.10, rate_tracker=ca_rate, seed=81, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=83, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=87, radius=0.112)

        ca_len = ValueTracker(0.98)
        k_len = ValueTracker(1.06)
        arrows = make_tug_of_war(ca_len, k_len, ValueTracker(Y_ROPE), ValueTracker(Y_ROPE),
                                 ValueTracker(1.0), tremble_amp=0.025, seed=18)

        t_tr = ValueTracker(208.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        # Gathering intracellular Ca2+ dots just inside the membrane near the GOLD channel
        rng = np.random.default_rng(180)
        ca_pool_pts = [
            [rng.uniform(2.45, 3.45), rng.uniform(Y_CA - 0.34, Y_CA + 0.34), 0.0]
            for _ in range(16)
        ]
        ca_pool = VGroup(*[Dot(p, radius=0.095, color=CA_COL).set_opacity(0.0) for p in ca_pool_pts])

        self.add(P, tag, rest_ln, mem, ca_lbl, kdr_lbl, ca_pool,
                 ca_stream, k_stream_r, k_stream_s, arrows, fill, live, dot, readout)

        # Continuous drift during opening question
        d0 = max(1.2, wait_dur(self, "the L type"))
        self.play(t_tr.animate.set_value(222.0), run_time=d0, rate_func=linear)

        # L-type channels inactivate: shut with time at depolarized voltages & as Ca2+ builds up inside
        self.at("the L type")
        d1 = max(2.0, wait_dur(self, "calcium builds up"))
        self.play(
            t_tr.animate.set_value(240.0),
            mem.ca_gate_val.animate.set_value(0.50),
            ca_rate.animate.set_value(0.58),
            *[d.animate.set_opacity(0.88) for d in ca_pool[:7]],
            run_time=d1,
            rate_func=linear,
        )

        self.at("calcium builds up")
        d2 = max(1.6, wait_dur(self, "calcium's pull fades"))
        self.play(
            t_tr.animate.set_value(256.0),
            mem.ca_gate_val.animate.set_value(0.04),
            ca_rate.animate.set_value(0.0),
            *[d.animate.set_opacity(0.95) for d in ca_pool[7:]],
            ca_len.animate.set_value(0.42),
            run_time=d2,
            rate_func=linear,
        )

        # Calcium's pull fades, potassium currents win -> rope marker slides fully to BLUE, dot starts to fall
        self.at("calcium's pull fades")
        d3 = max(1.0, wait_dur(self, "potassium currents win"))
        self.play(
            ca_len.animate.set_value(0.04),
            k_len.animate.set_value(1.24),
            t_tr.animate.set_value(272.0),
            run_time=d3,
            rate_func=smooth,
        )

        self.at("potassium currents win")
        rem = max(1.0, self.narration_s - self.elapsed() - 0.1)
        self.play(
            t_tr.animate.set_value(283.0),
            k_rate.animate.set_value(1.30),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 19: IK1 FINISHES REPOLARIZATION (spoken, 11.35 s)
# ===========================================================================
class S19Finish(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="closed",
                            kdr_state="open", ik1_open=0.06, ik1_dim=True)
        kdr_lbl = make_channel_label("IKr and\nIKs", Y_KDR, K_COL, size=28)

        k_rate = ValueTracker(1.25)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=83, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=12, spread_y=0.07,
                                     speed=1.15, rate_tracker=k_rate, seed=87, radius=0.112)

        t_tr = ValueTracker(283.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        self.add(P, tag, rest_ln, mem, kdr_lbl, k_stream_r, k_stream_s, fill, live, dot, readout)

        # As voltage falls, IK1 conducts again -> door swings wide open driven by g_K1(V)
        self.at("as the voltage")
        d0 = max(1.0, wait_dur(self, "IK1 conducts again"))
        self.play(t_tr.animate.set_value(293.0), run_time=d0, rate_func=linear)

        self.at("IK1 conducts again")
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)
        ik1_rate = ValueTracker(0.0)
        ik1_stream = make_ion_stream(Y_IK1, K_COL, direction=+1, count=22, spread_y=0.30,
                                     speed=1.15, rate_tracker=ik1_rate, seed=91, radius=0.115)
        lit_doors = make_ik1_doors(mem.ik1_open, color=K_COL, opacity=1.0)
        self.add(ik1_stream)
        d1 = max(2.2, wait_dur(self, "the cell returns"))
        self.play(
            FadeOut(mem.ik1_doors), FadeIn(lit_doors),
            mem.ik1_housing.animate.set_opacity(1.0),
            FadeIn(ik1_lbl),
            mem.ik1_open.animate.set_value(1.0),
            ik1_rate.animate.set_value(1.25),
            t_tr.animate.set_value(320.0),
            k_rate.animate.set_value(0.25),
            run_time=d1,
            rate_func=smooth,
        )
        mem.ik1_doors = lit_doors

        # Cell returns to flat rest near -90 mV
        self.at("the cell returns")
        rem = max(1.8, self.narration_s - self.elapsed() - 0.1)
        self.play(
            t_tr.animate.set_value(358.0),
            k_rate.animate.set_value(0.0),
            FadeOut(kdr_lbl),
            ik1_rate.animate.set_value(1.10),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 20: HOLD COMPLETE TRACE AT REST (silent, 5.0 s)
# ===========================================================================
class S20HoldFinish(NarratedScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="barred_dim", ito_open=False, ca_state="closed",
                            kdr_state="empty", ik1_open=1.0, ik1_dim=False)
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)

        ik1_rate = ValueTracker(1.10)
        ik1_stream = make_ion_stream(Y_IK1, K_COL, direction=+1, count=22, spread_y=0.30,
                                     speed=1.10, rate_tracker=ik1_rate, seed=91, radius=0.115, bidir=True)

        t_tr = ValueTracker(358.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        glow_curve = make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 0.0, 358.0,
                                       color=VOLTAGE_COL, width=10.5, opacity=0.50)

        self.add(P, tag, rest_ln, mem, ik1_lbl, ik1_stream, fill, live, dot, readout)
        self.play(
            t_tr.animate.set_value(392.0),
            run_time=4.8,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 21: RETURN TO THE ONE IDEA (spoken, 13.0 s)
# ===========================================================================
class S21Return(SpokenScene):
    def construct(self):
        P = build_plot()
        tag = build_scope_tag()
        rest_ln = build_rest_line(P, with_label=True)
        mem = MembraneWorld(na_state="empty", ito_open=False, ca_state="empty",
                            kdr_state="empty", ik1_open=1.0, ik1_dim=False)
        ik1_lbl = make_channel_label("IK1", Y_IK1, K_COL, size=28)

        t_tr = ValueTracker(16.0)
        fill = make_voltage_fill(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=TEAL, opacity=0.20)
        live = make_live_curve(P, SIM_NORM["t"], SIM_NORM["V"], t_tr, color=VOLTAGE_COL, width=6.0)
        dot = make_voltage_dot(P, SIM_NORM["t"], SIM_NORM["V"], t_tr)
        readout = make_voltage_readout(SIM_NORM["t"], SIM_NORM["V"], t_tr)

        ca_rate = ValueTracker(0.0)
        k_rate = ValueTracker(0.0)
        ca_stream = make_ion_stream(Y_CA, CA_COL, direction=-1, count=18, spread_y=0.13,
                                    speed=1.12, rate_tracker=ca_rate, seed=211, radius=0.115)
        k_stream_r = make_ion_stream(Y_IKR, K_COL, direction=+1, count=10, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=213, radius=0.112)
        k_stream_s = make_ion_stream(Y_IKS, K_COL, direction=+1, count=10, spread_y=0.07,
                                     speed=1.12, rate_tracker=k_rate, seed=217, radius=0.112)

        ca_len = ValueTracker(0.0)
        k_len = ValueTracker(0.0)
        rope_tr = ValueTracker(0.0)
        arrows = make_tug_of_war(ca_len, k_len, ValueTracker(Y_ROPE), ValueTracker(Y_ROPE),
                                 rope_tr, tremble_amp=0.025, seed=21)

        ik1_rate = ValueTracker(1.10)
        ik1_stream = make_ion_stream(Y_IK1, K_COL, direction=+1, count=22, spread_y=0.30,
                                     speed=1.10, rate_tracker=ik1_rate, seed=91, radius=0.115, bidir=True)
        self.add(P, tag, rest_ln, mem, ik1_lbl, ik1_stream, ca_stream, k_stream_r, k_stream_s,
                 arrows, fill, live, dot, readout)

        # Quick replay: resting IK1 flows, then the upstroke swings the door nearly shut
        self.at("so the long")
        na_open = make_channel_housing(Y_NA, 0.16, color=NA_COL, active=True)
        d0 = max(1.8, wait_dur(self, "it takes opposing"))
        self.play(t_tr.animate.set_value(19.5), run_time=d0 * 0.45, rate_func=linear)
        self.play(
            Transform(mem.na_housing, na_open),
            t_tr.animate.set_value(50.0),
            mem.ik1_open.animate.set_value(0.04),
            ik1_rate.animate.set_value(0.0),
            ik1_lbl.animate.set_opacity(0.0),
            mem.ik1_housing.animate.set_opacity(0.38),
            run_time=d0 * 0.33,
            rate_func=linear,
        )
        self.play(
            mem.na_bar.animate.set_opacity(0.45),
            mem.na_housing.animate.set_opacity(0.45),
            t_tr.animate.set_value(58.0),
            run_time=d0 * 0.22,
        )

        # Opposing pulls, closely matched along the plateau
        self.at("it takes opposing")
        ca_open = make_channel_housing(Y_CA, 0.20, color=CA_COL, active=True)
        ikr_open = make_channel_housing(Y_IKR, 0.13, color=K_COL, active=True)
        iks_open = make_channel_housing(Y_IKS, 0.13, color=K_COL, active=True)
        mem.ca_state_active.set_value(1.0)
        d1 = max(2.0, wait_dur(self, "while the resting"))
        self.play(
            Transform(mem.ca_housing, ca_open),
            mem.ca_gate_val.animate.set_value(1.0),
            Transform(mem.ikr_housing, ikr_open),
            Transform(mem.iks_housing, iks_open),
            ca_rate.animate.set_value(1.0),
            k_rate.animate.set_value(1.0),
            rope_tr.animate.set_value(1.0),
            ca_len.animate.set_value(0.92),
            k_len.animate.set_value(0.96),
            t_tr.animate.set_value(162.0),
            run_time=d1,
            rate_func=linear,
        )

        # Resting potassium path is largely shut
        self.at("while the resting")
        ik1_box = RoundedRectangle(corner_radius=0.12, width=1.00, height=1.10,
                                   color=K_COL, stroke_width=4.2).move_to([MEM_X, Y_IK1, 0.0])
        d2 = max(2.0, wait_dur(self, "when the match"))
        self.play(FadeIn(ik1_box), t_tr.animate.set_value(244.0), run_time=d2, rate_func=linear)

        # When the match ends, the plateau ends; plateau stays brightly lit in WHITE (same concept colour!)
        self.at("when the match")
        plateau_glow = VGroup(
            make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 48.0, 248.0, color=VOLTAGE_COL, width=13.0, opacity=0.32),
            make_static_curve(P, SIM_NORM["t"], SIM_NORM["V"], 48.0, 248.0, color=VOLTAGE_COL, width=7.5, opacity=1.0),
        )
        rem = max(1.4, self.narration_s - self.elapsed() - 0.1)
        self.play(
            FadeOut(ik1_box),
            ca_len.animate.set_value(0.0),
            k_len.animate.set_value(1.18),
            ca_rate.animate.set_value(0.0),
            mem.ca_gate_val.animate.set_value(0.0),
            t_tr.animate.set_value(288.0),
            FadeIn(plateau_glow),
            run_time=rem * 0.5,
            rate_func=linear,
        )
        # Only as the voltage falls does the resting door swing wide again
        self.play(
            mem.ik1_open.animate.set_value(1.0),
            mem.ik1_housing.animate.set_opacity(1.0),
            ik1_rate.animate.set_value(1.10),
            k_len.animate.set_value(0.0),
            k_rate.animate.set_value(0.0),
            t_tr.animate.set_value(335.0),
            run_time=rem * 0.5,
            rate_func=smooth,
        )
        self.bring_to_front(live, dot)
        self.finish()


# ===========================================================================
# SCENE 22: STANDARD END CARD (silent, 3.5 s — EndCard, no construct override)
# ===========================================================================
class S22End(EndCard):
    LINE = "The plateau lasts while small inward and outward currents nearly cancel."
