"""Two Clocks for Pressure — Regulating Arterial Pressure (STEMhop).

COLOUR MAP (one colour per concept, constant across all 17 scenes):
- BRIGHT_WHITE (#FFFFFF) : arterial pressure trace, pressure marker, remaining-error indicator
- RED          (#FC6255) : squeeze clamp on the small arteries, and the "no reflex" ghost trace
- CYAN         (#38E0F0) : carotid sinus & aortic arch stretch sensors, firing signals, reflex correction/push
- PURPLE       (#B88CFF) : vagal (parasympathetic) output wire from brainstem to heart
- ORANGE       (#FF9F43) : sympathetic output wires from brainstem to heart, small arteries, and vein
- BLOOD_BLUE   (#6FB8FF) : blood fluid lumen and flowing blood dots (and water drops leaving the kidney)
- GOLD         (#F2C14E) : sodium (salt) dots, salt-intake horizontal line, daily salt-loss gap, crossing balance
- GREEN        (#83C167) : kidney organ, renal branch, and the kidney's pressure-natriuresis line
- TEXT         (#E8EAF0) : crisp high-contrast labels, axes, and titles (full opacity, never grey)

ONE WORLD CARRIED FROM SCENE TO SCENE:
- Left 55% of the frame (x -6.2..+0.2, y -2.6..+2.6, ~70% of frame height): a schematic circulation loop
  built once and rebuilt in the same place every scene — pulsing heart pump at lower left, rising artery
  into the aortic arch with an upward carotid sinus bulge, two cyan stretch-sensor rings, brainstem box
  at top left with purple vagal wire and three orange sympathetic wires, clamped small-arteries tube at
  right, wide returning vein along the bottom, and (from s09 onward) a green kidney on a parallel branch
  upstream of the clamped small arteries with a bottom outlet.
- Right 45% of the frame (x +1.50..+6.00, y -1.85..+2.20): a live plot that starts as mean arterial
  pressure (95..125 mmHg) vs seconds (s00-s09) and transforms in s10 into sodium output vs mean arterial
  pressure (90..125 mmHg) for the slow days clock (s10-s15).

WHAT CHANGES ON SCREEN IN EACH SPOKEN SCENE (and what it is computed from):
- s00_hook      : Blood circulates at resting heart rate; live white pressure trace runs three seeded schematic
                  bumps with partial reflex recovery, each triggering computed cyan sensor pulses and purple/orange
                  wire responses, ending with the top question.
- s02_squeeze   : Pressure marker marks 93 then rounds to 100; red clamp closes and narrows small arteries;
                  wires dim (open-loop ghost) while red dashed curve computes P_open(t) = 100 + 20*(1 - exp(-t/tau))
                  up to 120 mmHg.
- s03_sensor    : Disturbance bracket spans 100..120 (D = 20); real white trace starts rising; view pushes in on
                  carotid sinus then aortic arch as wall radius and cyan sensor firing rate grow linearly with
                  computed pressure rise above 100.
- s04_arc       : View pulls back; cyan pulses travel to brainstem; purple vagal wire thickens and heart/flow slow;
                  orange sympathetic wires thin, small arteries partially widen (clamp still on), and vein widens;
                  white trace bends along computed closed-loop P(t) = 100 + (20/3)*(1 - exp(-t/tau)).
- s05_gain      : White trace settles at computed 100 + 20/(1+2) = 106.7; 20-mmHg bracket splits into cyan
                  removed = 13.3 and white left = 6.7; ratio 13.3 / 6.7 = 2 builds directly from the two pieces.
- s06_predict   : The 20-mmHg bracket divides into 3 equal thirds (2 cyan, 1 white); white pressure dot is nudged
                  upward and eased back to 106.7 while vagal/sympathetic wire strength and sensor firing track
                  (P - 100) continuously; top predict question appears.
- s08_answer    : White error arrow (P - 100) and cyan downward push arrow (2*(P - 100)) appear; a dashed ghost
                  dot slides from 106.7 down to 100, shrinking both arrows proportionally to zero and easing ghost
                  wires to rest, then fades while the real state remains at 106.7; red ghost trace fades out.
- s09_idea      : Green kidney appears on its parallel branch with outlet; brainstem + wires and the left: 6.7
                  bracket pulse for "how far", then the kidney pulses for "where", with the reflex state intact.
- s10_kidney    : Plot clock rotates and morphs seconds -> days; time trace collapses into a white pressure marker
                  at 106.7 on the new mean-pressure x-axis; gold salt dots enter at top and gold + blue drops exit
                  the kidney; green kidney line draws from excretion = 10*(P - 85) on a hidden y scale (150 at 40%).
- s11_crossing  : Dashed gold salt-in line slides in at y = 150; exact crossing at P = 100 glows with equal
                  in/out gold arrows and vertical drop to 100 while the white pressure marker remains at 106.7.
- s12_drain     : Vertical gold gap (excretion - 150) shades at P = 106.7 ("lose 67 per day"); gold/water drops
                  outpace intake, blood fluid visibly thins, day counter ticks, and one pressure tracker drives the
                  marker, gap height, live loss readout (67 -> 30 -> 10), and gradual reflex easing as P steps
                  106.7 -> 103 -> 101.
- s13_none_left : Pressure tracker reaches 100, closing the gold gap to "balance" with equal salt in/out and
                  resting reflex wires; red clamp pulses closed while heart beats at resting rate with smaller
                  stroke puffs in thinner blood; a ghost of the 6.7 error bracket flashes and shrinks to zero.
- s14_final_say : On the renal plot, pressure is nudged right (draining salt/water) then left (piling salt/water),
                  each time ticking the day counter as computed salt imbalance drives pressure slowly back to 100.
- s15_close     : Full world holds at 100 with clamp on; nerves/brainstem/sensors pulse for "seconds", kidney and
                  both lines pulse for "days", and a dashed cyan arrow with "?" connects brainstem to kidney.
"""

from bp_parts import *  # noqa: F401,F403

# ---------------------------------------------------------------------------
# Concept palette (strictly one colour per concept)
# ---------------------------------------------------------------------------
BRIGHT_WHITE = "#FFFFFF"
CYAN = "#38E0F0"
PURPLE = "#B88CFF"
ORANGE = "#FF9F43"
BLOOD_BLUE = "#6FB8FF"
SALT_GOLD = "#F2C14E"
KIDNEY_GREEN = GREEN          # #83C167
CLAMP_RED = RED               # #FC6255
AXIS_INK = "#D4DAE6"          # high-contrast readable axis & tick colour (never dim grey)
DIM_WIRE = "#525A6B"          # ONLY used for the explicitly "greyed out / cut" ghost wires in s02

# ---------------------------------------------------------------------------
# Quantitative lesson models (Worked Problems Part A & Part B)
# ---------------------------------------------------------------------------
P_REST_REAL = 93.0
P_BASE = 100.0
DISTURBANCE = 20.0
GAIN = 2.0
P_OPEN = P_BASE + DISTURBANCE                  # 120.0 mmHg
ERROR_SS = DISTURBANCE / (1.0 + GAIN)          # 6.6667 mmHg (6.7)
CORR_SS = GAIN * ERROR_SS                      # 13.3333 mmHg (13.3)
P_CLOSED = P_BASE + ERROR_SS                   # 106.6667 mmHg (106.7)

RENAL_SLOPE = 10.0                             # mEq/day per mmHg
RENAL_THRESH = 85.0                            # mmHg
SALT_INTAKE = 150.0                            # mEq/day
RENAL_YMAX = 375.0                             # puts 150 at exactly 40.0% of y-axis height


def p_open_curve(t, t0=0.0, tau=1.35):
    u = max(0.0, t - t0)
    return P_BASE + DISTURBANCE * (1.0 - np.exp(-u / tau))


def p_closed_curve(t, t0=0.0, tau=1.8):
    u = max(0.0, t - t0)
    return P_BASE + ERROR_SS * (1.0 - np.exp(-u / tau))


def renal_excretion(p):
    return max(0.0, RENAL_SLOPE * (p - RENAL_THRESH))


def daily_loss(p):
    return renal_excretion(p) - SALT_INTAKE


def hook_trace_fn():
    """Seeded schematic pressure trace for s00_hook: 3 bumps with partial reflex recovery."""
    rng = np.random.default_rng(7)
    # Small seeded micro-jitter table for natural baseline feel
    t_grid = np.linspace(0.0, 10.0, 201)
    jitter = rng.normal(0.0, 0.35, size=len(t_grid))
    # Smooth jitter slightly so it looks like a physiological trace
    jitter = np.convolve(jitter, np.array([0.2, 0.6, 0.2]), mode="same")
    jitter[0] = 0.0
    jitter[-1] = 0.0

    def fn(t):
        t = float(np.clip(t, 0.0, 10.0))
        j = float(np.interp(t, t_grid, jitter))
        # Bump 1 (up, t ~ 1.4..3.5): jumps ~+13, reflex trims to ~+4.2 residual
        b1 = 13.5 * np.exp(-((t - 1.75) / 0.45) ** 2) + 4.0 * (1.0 / (1.0 + np.exp(-6.0 * (t - 1.65)))) * np.exp(-max(0.0, t - 2.3) / 1.8)
        # Bump 2 (down, t ~ 3.9..6.0): drops ~-5.2 cleanly inside plot (no flat clipping!), reflex trims partway back
        b2 = -4.2 * np.exp(-((t - 4.35) / 0.45) ** 2) - 1.6 * (1.0 / (1.0 + np.exp(-6.0 * (t - 4.25)))) * np.exp(-max(0.0, t - 4.9) / 1.6)
        # Bump 3 (up, t ~ 6.5..9.8): jumps ~+13, reflex trims partway back, never quite reaches 100
        b3 = 13.0 * np.exp(-((t - 6.85) / 0.45) ** 2) + 4.8 * (1.0 / (1.0 + np.exp(-6.0 * (t - 6.75))))
        return float(np.clip(P_BASE + j + b1 + b2 + b3, 95.8, 124.2))

    return fn


# ---------------------------------------------------------------------------
# Plot coordinates & shared builders
# ---------------------------------------------------------------------------
PLOT_BOX = (1.50, 6.00, -1.85, 2.20)
WORLD_CENTER = np.array([-3.10, 0.15, 0.0])


def make_time_plot(show_x_label=True):
    P = Plot(
        box=PLOT_BOX,
        xr=(0.0, 10.0),
        yr=(95.0, 125.0),
        xticks=(),
        yticks=[(95, "95"), (100, "100"), (110, "110"), (120, "120"), (125, "125")],
        xlabel="seconds" if show_x_label else "",
        ylabel="mean pressure (mmHg)",
        color=AXIS_INK,
        size=22,
        label_size=24,
        stroke=3,
    )
    # Keep tick labels and axis labels bright and readable (never dim grey)
    for t in P.tick_labels:
        t.set_color(TEXT)
    if P.xlabel:
        P.xlabel.set_color(TEXT)
    if P.ylabel:
        P.ylabel.set_color(TEXT)
    base_line = DashedLine(
        P.pt(0.0, P_BASE),
        P.pt(10.0, P_BASE),
        color=BRIGHT_WHITE,
        stroke_width=2.5,
        dash_length=0.14,
    ).set_opacity(0.65)
    return P, base_line


def make_renal_plot():
    P = Plot(
        box=PLOT_BOX,
        xr=(90.0, 125.0),
        yr=(0.0, RENAL_YMAX),
        xticks=[(90, "90"), (100, "100"), (110, "110"), (120, "120")],
        yticks=(),
        xlabel="mean pressure (mmHg)",
        ylabel="sodium out per day",
        color=AXIS_INK,
        size=22,
        label_size=24,
        stroke=3,
    )
    for t in P.tick_labels:
        t.set_color(TEXT)
    if P.xlabel:
        P.xlabel.set_color(TEXT)
    if P.ylabel:
        P.ylabel.set_color(TEXT)
    return P


def make_plot_tag(text):
    """Bottom-right tag under the plot in crisp readable text (full opacity)."""
    t = T(text, size=22, color=TEXT)
    return t.move_to([6.10 - t.width / 2, -3.28, 0.0])


def make_clock_badge(label_text="seconds", hand_angle=0.0, center=(5.05, 3.22, 0.0)):
    """Small clock icon + label cleanly in the upper-right band above the plot."""
    c = np.array(center, dtype=float)
    rim = Circle(radius=0.20, color=TEXT, stroke_width=2.8).move_to(c)
    hr_hand = Line(c, c + 0.10 * np.array([np.sin(hand_angle * 0.2), np.cos(hand_angle * 0.2), 0.0]),
                   color=TEXT, stroke_width=2.8)
    min_hand = Line(c, c + 0.15 * np.array([np.sin(hand_angle), np.cos(hand_angle), 0.0]),
                    color=SALT_GOLD if label_text == "days" else CYAN, stroke_width=2.8)
    lbl = T(label_text, size=24, color=SALT_GOLD if label_text == "days" else TEXT).next_to(rim, RIGHT, buff=0.14)
    g = VGroup(rim, hr_hand, min_hand, lbl)
    g.rim, g.hr_hand, g.min_hand, g.lbl = rim, hr_hand, min_hand, lbl
    return g


def make_bracket(p_bot, p_top, color=TEXT, width=0.14, stroke=3.2):
    """Clean right-facing bracket spanning p_bot to p_top at shared x."""
    x = p_bot[0]
    y0, y1 = p_bot[1], p_top[1]
    pts = [
        [x - width, y0, 0.0],
        [x, y0, 0.0],
        [x, y1, 0.0],
        [x - width, y1, 0.0],
    ]
    m = VMobject(stroke_color=color, stroke_width=stroke, fill_opacity=0)
    m.set_points_as_corners(pts)
    return m


# ---------------------------------------------------------------------------
# Circulation loop path helpers
# ---------------------------------------------------------------------------
def _sample_polyline(ctrl_pts, n_per_seg=18):
    """Smooth Catmull-Rom-like corner rounding along control points -> uniform arc-length samples."""
    pts = [np.array([p[0], p[1], 0.0], dtype=float) for p in ctrl_pts]
    raw = []
    m = len(pts)
    for i in range(m - 1):
        p0 = pts[max(0, i - 1)]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[min(m - 1, i + 2)]
        for k in range(n_per_seg):
            t = k / n_per_seg
            t2, t3 = t * t, t * t * t
            q = 0.5 * (
                (2 * p1)
                + (-p0 + p2) * t
                + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                + (-p0 + 3 * p1 - 3 * p2 + p3) * t3
            )
            raw.append(q)
    raw.append(pts[-1])
    raw = np.array(raw)
    segs = np.linalg.norm(np.diff(raw, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(segs)])
    s /= max(s[-1], 1e-6)
    return raw, s


def _interp_path(raw, s, u):
    u = float(u % 1.0)
    x = float(np.interp(u, s, raw[:, 0]))
    y = float(np.interp(u, s, raw[:, 1]))
    return np.array([x, y, 0.0])


def _tube_polygon(centerline, half_widths):
    """Build a closed filled tube Polygon from a centerline and per-vertex half-widths."""
    n = len(centerline)
    left_pts, right_pts = [], []
    for i in range(n):
        if i == 0:
            tan = centerline[1] - centerline[0]
        elif i == n - 1:
            tan = centerline[-1] - centerline[-2]
        else:
            tan = centerline[i + 1] - centerline[i - 1]
        L = np.linalg.norm(tan)
        if L < 1e-6:
            nrm = np.array([0.0, 1.0, 0.0])
        else:
            tan = tan / L
            nrm = np.array([-tan[1], tan[0], 0.0])
        w = half_widths[i]
        left_pts.append(centerline[i] + nrm * w)
        right_pts.append(centerline[i] - nrm * w)
    outline = left_pts + list(reversed(right_pts))
    return outline, left_pts, right_pts


# ---------------------------------------------------------------------------
# THE WORLD: Circulation loop + sensors + brainstem + wires + clamp + kidney
# ---------------------------------------------------------------------------
class CirculationWorld(VGroup):
    """Carried-over schematic circulation loop on the left 55% of the frame.

    All physiological dynamics are driven from ValueTrackers:
      - pressure     : arterial pressure in mmHg (100 = rest, 106.7 = reflex steady state)
      - clamp        : 0 = open/hidden, 1 = closed on small arteries
      - vagal        : 0 = resting, +1 = reflex up (bright/thick), -1 = cut/greyed
      - symp         : 0 = resting, -1 = reflex down (dim/thin), -2 = cut/greyed
      - volume       : 1.0 = normal blood volume, 0.58 = drained volume (thinner fluid, smaller puffs)
      - cam_scale/dx/dy : smooth push-in / pull-back transform (used in s03 & s04)
    """

    def __init__(
        self,
        pressure=P_BASE,
        clamp=0.0,
        vagal=0.0,
        symp=0.0,
        volume=1.0,
        kidney=False,
        salt_in=0.0,
        salt_out_from_pressure=False,
        show_labels=True,
        show_wire_labels=False,
        cam_scale=1.0,
        cam_dx=0.0,
        cam_dy=0.0,
        seed=7,
    ):
        super().__init__()
        self.rng = np.random.default_rng(seed)

        # State trackers
        self.pressure = ValueTracker(float(pressure))
        self.clamp = ValueTracker(float(clamp))
        self.vagal = ValueTracker(float(vagal))
        self.symp = ValueTracker(float(symp))
        self.volume = ValueTracker(float(volume))
        self.cam_scale = ValueTracker(float(cam_scale))
        self.cam_dx = ValueTracker(float(cam_dx))
        self.cam_dy = ValueTracker(float(cam_dy))
        self.salt_in_rate = ValueTracker(float(salt_in))
        self.salt_out_coupled = bool(salt_out_from_pressure)
        self.kidney_on = bool(kidney)
        self.show_labels = bool(show_labels)

        # Internal phase accumulators for continuous physiology
        self._beat_phase = 0.0
        self._flow_phase = 0.0
        self._sensor_phase = 0.0
        self._aff_phase = 0.0
        self._salt_phase = 0.0
        self._last_geom_state = None

        # Precompute centerline of the main circulation loop (clockwise from heart outlet -> heart inlet)
        # Heart center (-4.80, -1.60); arch top y = 1.35; small arteries at x = -0.55; vein along y = -1.78
        self._heart_c = np.array([-4.80, -1.60, 0.0])
        self._brain_c = np.array([-4.95, 2.32, 0.0])
        self._carotid_c = np.array([-2.75, 2.26, 0.0])
        self._arch_sensor_c = np.array([-1.65, 1.35, 0.0])
        self._clamp_c = np.array([-0.55, -0.15, 0.0])
        self._kidney_c = np.array([-2.15, 0.02, 0.0])

        loop_ctrl = [
            (-4.80, -0.95),  # leave top of heart
            (-4.80, 0.25),   # ascending artery
            (-4.55, 1.12),   # bend into arch
            (-3.60, 1.35),   # arch left
            (-2.75, 1.35),   # carotid branch point
            (-1.65, 1.35),   # aortic arch sensor
            (-0.82, 1.15),   # top-right bend
            (-0.55, 0.55),   # top of small arteries
            (-0.55, -0.15),  # middle of clamped small arteries
            (-0.55, -0.95),  # bottom of small arteries
            (-0.88, -1.68),  # bottom-right bend into vein
            (-1.75, -1.78),  # vein right
            (-3.10, -1.78),  # vein middle
            (-4.15, -1.70),  # enter right side of heart
        ]
        self._loop_pts, self._loop_s = _sample_polyline(loop_ctrl, n_per_seg=10)

        # Closed flow cycle for blood dots (includes pass through heart)
        flow_ctrl = loop_ctrl + [(-4.80, -1.60), (-4.80, -0.95)]
        self._flow_pts, self._flow_s = _sample_polyline(flow_ctrl, n_per_seg=8)

        # Afferent paths (carotid sensor -> brainstem, arch sensor -> brainstem)
        self._aff1_pts, self._aff1_s = _sample_polyline(
            [(-2.75, 2.26), (-3.35, 2.30), (-3.95, 2.32)], n_per_seg=8
        )
        self._aff2_pts, self._aff2_s = _sample_polyline(
            [(-1.65, 1.35), (-2.25, 1.82), (-3.15, 2.08), (-3.95, 2.20)], n_per_seg=8
        )

        # Efferent wire centerlines
        self._vagal_pts, _ = _sample_polyline(
            [(-5.48, 2.02), (-5.88, 1.35), (-5.92, 0.05), (-5.84, -1.05), (-5.45, -1.48)], n_per_seg=8
        )
        self._symp_stem, _ = _sample_polyline(
            [(-4.22, 2.02), (-3.92, 1.25), (-3.85, 0.55)], n_per_seg=6
        )
        self._symp_heart, _ = _sample_polyline(
            [(-3.85, 0.55), (-4.00, -0.35), (-4.28, -1.12)], n_per_seg=6
        )
        self._symp_art, _ = _sample_polyline(
            [(-3.85, 0.55), (-2.85, 0.88), (-1.55, 0.78), (-0.82, 0.48)], n_per_seg=6
        )
        self._symp_vein, _ = _sample_polyline(
            [(-3.85, 0.55), (-3.68, -0.45), (-3.50, -1.52)], n_per_seg=6
        )

        # Layers (ordered back to front)
        self.vessel_group = VGroup()
        self.blood_dots = VGroup()
        self.heart_group = VGroup()
        self.kidney_group = VGroup()
        self.wire_group = VGroup()
        self.afferent_group = VGroup()
        self.sensor_group = VGroup()
        self.clamp_group = VGroup()
        self.salt_group = VGroup()
        self.brainstem_group = VGroup()
        self.label_group = VGroup()
        self.wire_label_group = VGroup()

        self.add(
            self.vessel_group,
            self.kidney_group,
            self.blood_dots,
            self.heart_group,
            self.wire_group,
            self.afferent_group,
            self.sensor_group,
            self.clamp_group,
            self.salt_group,
            self.brainstem_group,
            self.label_group,
            self.wire_label_group,
        )

        # Build blood dots (20 evenly spaced around the loop)
        self._n_blood = 20
        for i in range(self._n_blood):
            d = Dot(radius=0.068, color=BLOOD_BLUE, fill_opacity=0.92)
            d.u0 = i / self._n_blood
            self.blood_dots.add(d)

        # Build sensor ripple rings (3 per sensor)
        self._carotid_ripples = VGroup(*[Circle(radius=0.25, color=CYAN, stroke_width=2.5) for _ in range(3)])
        self._arch_ripples = VGroup(*[Circle(radius=0.22, color=CYAN, stroke_width=2.5) for _ in range(3)])
        self.sensor_group.add(self._carotid_ripples, self._arch_ripples)

        # Sensor core rings (stretched by pressure)
        self._carotid_ring = Circle(radius=0.28, color=CYAN, stroke_width=5.0)
        self._arch_ring = Ellipse(width=0.30, height=0.46, color=CYAN, stroke_width=5.0)
        self.sensor_group.add(self._carotid_ring, self._arch_ring)

        # Travelling cyan afferent pulses (3 on carotid afferent, 3 on arch afferent)
        self._aff1_dots = VGroup(*[Dot(radius=0.055, color=CYAN) for _ in range(3)])
        self._aff2_dots = VGroup(*[Dot(radius=0.055, color=CYAN) for _ in range(3)])
        self.afferent_group.add(self._aff1_dots, self._aff2_dots)

        # Heartbeat stroke puff indicator (ring/wave leaving top of heart on each beat)
        self._puff = Circle(radius=0.14, color=BLOOD_BLUE, stroke_width=4.0, fill_color=BLOOD_BLUE, fill_opacity=0.35)
        self.heart_group.add(self._puff)

        # Salt-in dots (entering top of arch) & Salt+Water-out drops (exiting kidney outlet)
        self._n_salt_in = 4
        self._n_salt_out = 8
        self._salt_in_dots = VGroup(*[Dot(radius=0.068, color=SALT_GOLD) for _ in range(self._n_salt_in)])
        self._salt_out_dots = VGroup(*[Dot(radius=0.068, color=SALT_GOLD) for _ in range(self._n_salt_out)])
        self._water_out_dots = VGroup(*[Dot(radius=0.056, color=BLOOD_BLUE) for _ in range(self._n_salt_out)])
        self.salt_group.add(self._salt_in_dots, self._salt_out_dots, self._water_out_dots)

        # Static labels (repositioned with camera)
        self.lbl_heart = T("heart", size=24, color=TEXT)
        self.lbl_vein = T("vein", size=24, color=TEXT)
        self.lbl_small_art = T("small\narteries", size=22, color=TEXT, line_spacing=0.85)
        if self.show_labels:
            self.label_group.add(self.lbl_heart, self.lbl_vein, self.lbl_small_art)

        # Optional reflex wire status labels in the clean lower-left band (y = -3.22)
        self.lbl_vagal = T("vagal: up", size=24, color=PURPLE).move_to([-4.95, -3.22, 0.0])
        self.lbl_symp = T("sympathetic: down", size=24, color=ORANGE).move_to([-1.75, -3.22, 0.0])
        if show_wire_labels:
            self.wire_label_group.add(self.lbl_vagal, self.lbl_symp)

        # Initial geometry build & continuous updater
        self._rebuild_geometry()
        self._update_dynamic(0.0)
        self.add_updater(lambda m, dt: m._tick(dt))

    def to_scene(self, p):
        arr = np.asarray(p, dtype=float)
        if arr.shape[0] == 2:
            arr = np.array([arr[0], arr[1], 0.0])
        s = self.cam_scale.get_value()
        sh = np.array([self.cam_dx.get_value(), self.cam_dy.get_value(), 0.0])
        return WORLD_CENTER + s * (arr - WORLD_CENTER) + sh

    def sc(self):
        return self.cam_scale.get_value()

    def _state_key(self):
        return (
            round(self.pressure.get_value(), 2),
            round(self.clamp.get_value(), 3),
            round(self.vagal.get_value(), 2),
            round(self.symp.get_value(), 2),
            round(self.volume.get_value(), 3),
            round(self.cam_scale.get_value(), 4),
            round(self.cam_dx.get_value(), 4),
            round(self.cam_dy.get_value(), 4),
            self.kidney_on,
        )

    def _rebuild_geometry(self):
        p = self.pressure.get_value()
        cl = float(np.clip(self.clamp.get_value(), 0.0, 1.0))
        vg = self.vagal.get_value()
        sy = self.symp.get_value()
        vol = float(np.clip(self.volume.get_value(), 0.45, 1.25))
        s = self.sc()

        # Stretch factor from pressure above 100 (visible wall bulge in s03+)
        stretch = float(np.clip((p - P_BASE) / 15.0, -0.25, 1.2))

        # --- 1. Main circulation loop tube (variable half-width per segment) ---
        pts = np.array([self.to_scene(q) for q in self._loop_pts])
        half_w = []
        # Small arteries half-width: rest 0.19 -> clamped 0.085; reflex symp down relaxes partway to 0.13
        symp_relax = float(np.clip(-sy, 0.0, 1.0)) if sy > -1.5 else 0.0
        art_w_small = (0.19 * (1.0 - cl) + (0.085 + 0.045 * symp_relax) * cl) * s
        vein_w = (0.25 + 0.055 * symp_relax) * s * (0.72 + 0.28 * vol)
        arch_w = (0.20 + 0.085 * max(0.0, stretch)) * s

        for q in self._loop_pts:
            qx, qy = q[0], q[1]
            if qx > -0.85 and -1.05 < qy < 0.75:
                # Smooth pinch around y = -0.15
                pinch = np.exp(-((qy + 0.15) / 0.55) ** 2)
                w = (0.19 * s) * (1.0 - pinch) + art_w_small * pinch
            elif qy < -1.25:
                w = vein_w
            elif qy > 0.95:
                w = arch_w
            else:
                w = 0.20 * s
            half_w.append(w)

        outline, left_wall, right_wall = _tube_polygon(pts, half_w)
        # Blood fluid fill inside lumen: visibly thins & dims as volume drops in s12-s14
        fluid_op = float(np.clip(0.14 + 0.30 * vol, 0.18, 0.46))
        fluid_poly = Polygon(*outline, stroke_width=0, fill_color=BLOOD_BLUE, fill_opacity=fluid_op)
        wall_l = VMobject(stroke_color=AXIS_INK, stroke_width=3.2 * np.sqrt(s), fill_opacity=0).set_points_as_corners(left_wall)
        wall_r = VMobject(stroke_color=AXIS_INK, stroke_width=3.2 * np.sqrt(s), fill_opacity=0).set_points_as_corners(right_wall)

        # Carotid side branch & bulge (stretches clearly with pressure)
        stem_bot = self.to_scene([-2.75, 1.35, 0.0])
        car_c = self.to_scene(self._carotid_c)
        stem_w = 0.11 * s
        car_stem_fill = Polygon(
            stem_bot + LEFT * stem_w, stem_bot + RIGHT * stem_w,
            car_c + RIGHT * stem_w, car_c + LEFT * stem_w,
            stroke_width=0, fill_color=BLOOD_BLUE, fill_opacity=fluid_op,
        )
        car_stem_l = Line(stem_bot + LEFT * stem_w + UP * 0.14 * s, car_c + LEFT * stem_w, color=AXIS_INK, stroke_width=3.0 * np.sqrt(s))
        car_stem_r = Line(stem_bot + RIGHT * stem_w + UP * 0.14 * s, car_c + RIGHT * stem_w, color=AXIS_INK, stroke_width=3.0 * np.sqrt(s))
        car_r = (0.24 + 0.13 * max(0.0, stretch)) * s
        car_bulge = Circle(
            radius=car_r,
            stroke_color=AXIS_INK,
            stroke_width=3.2 * np.sqrt(s),
            fill_color=BLOOD_BLUE,
            fill_opacity=fluid_op + 0.06,
        ).move_to(car_c)

        self.vessel_group.submobjects = [fluid_poly, car_stem_fill, wall_l, wall_r, car_stem_l, car_stem_r, car_bulge]

        # --- 2. Kidney parallel branch & organ (s09+) ---
        self.kidney_group.submobjects = []
        if self.kidney_on:
            kc = self.to_scene(self._kidney_c)
            # Parallel arterial branch from arch (-2.15, 1.35) down into top of kidney
            ka_top = self.to_scene([-2.15, 1.25, 0.0])
            ka_bot = self.to_scene([-2.15, 0.50, 0.0])
            k_art = Line(ka_top, ka_bot, color=BLOOD_BLUE, stroke_width=10.0 * s).set_opacity(fluid_op + 0.12)
            k_art_l = Line(ka_top + LEFT * 0.07 * s, ka_bot + LEFT * 0.07 * s, color=AXIS_INK, stroke_width=2.4)
            k_art_r = Line(ka_top + RIGHT * 0.07 * s, ka_bot + RIGHT * 0.07 * s, color=AXIS_INK, stroke_width=2.4)
            # Renal vein starts outside the right border of the widened kidney bean and joins vein
            kv_pts = [self.to_scene(q) for q in [(-1.45, -0.15), (-1.24, -0.58), (-1.22, -1.72)]]
            k_vein = VMobject(stroke_color=BLOOD_BLUE, stroke_width=9.5 * s, stroke_opacity=fluid_op + 0.12).set_points_smoothly(kv_pts)
            k_vein_out = VMobject(stroke_color=AXIS_INK, stroke_width=2.4).set_points_smoothly(kv_pts)
            # Green kidney organ box sized with generous padding around "kidney" label
            bean = RoundedRectangle(
                corner_radius=0.34 * s,
                width=1.40 * s,
                height=0.96 * s,
                stroke_color=KIDNEY_GREEN,
                stroke_width=4.0 * np.sqrt(s),
                fill_color=KIDNEY_GREEN,
                fill_opacity=0.28,
            ).move_to(kc)
            k_lbl = T("kidney", size=int(round(24 * min(s, 1.25))), color=KIDNEY_GREEN).move_to(kc)
            # Small vertical urine outlet tube below kidney (stops clearly above vein)
            out_top = self.to_scene([-2.15, -0.46, 0.0])
            out_bot = self.to_scene([-2.15, -0.88, 0.0])
            out_l = Line(out_top + LEFT * 0.08 * s, out_bot + LEFT * 0.08 * s, color=KIDNEY_GREEN, stroke_width=3.0)
            out_r = Line(out_top + RIGHT * 0.08 * s, out_bot + RIGHT * 0.08 * s, color=KIDNEY_GREEN, stroke_width=3.0)
            self.kidney_group.add(k_art, k_art_l, k_art_r, k_vein, k_vein_out, bean, k_lbl, out_l, out_r)
            self.kidney_bean = bean
            self.kidney_label = k_lbl

        # --- 3. Heart chamber (core shape; dynamic beat scales it in _update_dynamic) ---
        hc = self.to_scene(self._heart_c)
        self._heart_body = RoundedRectangle(
            corner_radius=0.42 * s,
            width=1.22 * s,
            height=1.18 * s,
            stroke_color=TEXT,
            stroke_width=4.0 * np.sqrt(s),
            fill_color=BLOOD_BLUE,
            fill_opacity=float(np.clip(0.24 + 0.28 * vol, 0.25, 0.55)),
        ).move_to(hc)
        # Small directional flow chevron inside heart (upward pump)
        chev = VMobject(stroke_color=BRIGHT_WHITE, stroke_width=3.2 * np.sqrt(s), fill_opacity=0)
        chev.set_points_as_corners([
            hc + np.array([-0.20, -0.10, 0.0]) * s,
            hc + np.array([0.0, 0.18, 0.0]) * s,
            hc + np.array([0.20, -0.10, 0.0]) * s,
        ])
        self._heart_chev = chev
        self.heart_group.submobjects = [self._heart_body, self._heart_chev, self._puff]

        # --- 4. Autonomic wires (PURPLE vagal & ORANGE sympathetic) ---
        if vg < -0.5:
            v_col, v_w, v_op = DIM_WIRE, 2.4, 0.45
        else:
            v_col = PURPLE
            v_w = (3.6 + 3.4 * max(0.0, vg)) * np.sqrt(s)
            v_op = float(np.clip(0.68 + 0.32 * vg, 0.55, 1.0))

        if sy < -1.5:
            s_col, s_w, s_op = DIM_WIRE, 2.2, 0.40
        else:
            s_col = ORANGE
            s_w = (3.6 + 1.8 * sy) * np.sqrt(s)          # sy = -1 -> thinner (1.8); sy = 0 -> 3.6
            s_w = max(1.6, s_w)
            s_op = float(np.clip(0.82 + 0.45 * sy, 0.28, 1.0))

        vagal_curve = VMobject(stroke_color=v_col, stroke_width=v_w, stroke_opacity=v_op).set_points_as_corners(
            [self.to_scene(q) for q in self._vagal_pts]
        )
        symp_curves = VGroup(*[
            VMobject(stroke_color=s_col, stroke_width=s_w, stroke_opacity=s_op).set_points_as_corners(
                [self.to_scene(q) for q in path]
            )
            for path in (self._symp_stem, self._symp_heart, self._symp_art, self._symp_vein)
        ])
        # If wires are cut (s02 ghost), draw tiny red X cut marks cleanly on the wires (off vessels)
        cut_marks = VGroup()
        if vg < -0.5:
            for pt in ([-5.90, 0.35, 0.0], [-4.08, 1.72, 0.0]):
                cp = self.to_scene(pt)
                d = 0.13 * s
                cut_marks.add(
                    Line(cp + np.array([-d, -d, 0]), cp + np.array([d, d, 0]), color=CLAMP_RED, stroke_width=3.5),
                    Line(cp + np.array([-d, d, 0]), cp + np.array([d, -d, 0]), color=CLAMP_RED, stroke_width=3.5),
                )
        self.vagal_wire = vagal_curve
        self.symp_wires = symp_curves
        self.wire_group.submobjects = [vagal_curve, symp_curves, cut_marks]

        # --- 5. Afferent CYAN guide lines ---
        aff1_line = DashedLine(
            self.to_scene([-3.02, 2.26, 0.0]), self.to_scene([-3.95, 2.32, 0.0]),
            color=CYAN, stroke_width=2.2, dash_length=0.10,
        ).set_opacity(0.65)
        aff2_line = VMobject(stroke_color=CYAN, stroke_width=2.2, stroke_opacity=0.55).set_points_as_corners(
            [self.to_scene(q) for q in self._aff2_pts]
        )
        self.afferent_group.submobjects = [aff1_line, aff2_line, self._aff1_dots, self._aff2_dots]

        # --- 6. Sensor core rings ---
        self._carotid_ring.become(
            Circle(radius=car_r + 0.05 * s, color=CYAN, stroke_width=5.0 * np.sqrt(s)).move_to(car_c)
        )
        arch_c = self.to_scene(self._arch_sensor_c)
        self._arch_ring.become(
            Ellipse(
                width=(0.24 + 0.05 * max(0.0, stretch)) * s,
                height=(arch_w * 2.0 + 0.12 * s),
                color=CYAN,
                stroke_width=5.0 * np.sqrt(s),
            ).move_to(arch_c)
        )

        # --- 7. RED Clamp on small arteries ---
        self.clamp_group.submobjects = []
        if cl > 0.02:
            cc = self.to_scene(self._clamp_c)
            # Jaws move inward as cl goes 0 -> 1
            gap = (0.48 - 0.36 * cl) * s
            jaw_w, jaw_h = 0.24 * s, 0.62 * s
            jaw_l = RoundedRectangle(
                corner_radius=0.06 * s, width=jaw_w, height=jaw_h,
                stroke_color=CLAMP_RED, stroke_width=3.0, fill_color=CLAMP_RED, fill_opacity=0.88 * cl,
            ).move_to(cc + LEFT * (gap + jaw_w / 2))
            jaw_r = RoundedRectangle(
                corner_radius=0.06 * s, width=jaw_w, height=jaw_h,
                stroke_color=CLAMP_RED, stroke_width=3.0, fill_color=CLAMP_RED, fill_opacity=0.88 * cl,
            ).move_to(cc + RIGHT * (gap + jaw_w / 2))
            # Small red inward arrows on the jaws
            bar_l = Line(cc + LEFT * (gap + jaw_w + 0.18 * s), cc + LEFT * (gap + jaw_w), color=CLAMP_RED, stroke_width=5.0 * cl)
            bar_r = Line(cc + RIGHT * (gap + jaw_w + 0.18 * s), cc + RIGHT * (gap + jaw_w), color=CLAMP_RED, stroke_width=5.0 * cl)
            self.clamp_group.add(jaw_l, jaw_r, bar_l, bar_r)

        # --- 8. Brainstem box ---
        bc = self.to_scene(self._brain_c)
        bs = boxed_label("brainstem", TEXT, size=int(round(24 * min(s, 1.25))), pad=0.18, fill_opacity=0.22)
        bs.move_to(bc)
        self.brainstem_box = bs
        self.brainstem_group.submobjects = [bs]

        # --- 9. Static labels (clean clearance from every vessel wall) ---
        self.lbl_heart.move_to(self.to_scene([-4.80, -2.52, 0.0]))
        self.lbl_vein.move_to(self.to_scene([-2.35, -2.42, 0.0]))
        self.lbl_small_art.move_to(self.to_scene([-0.22, 2.02, 0.0]))

        self._last_geom_state = self._state_key()

    def _update_dynamic(self, dt):
        p = self.pressure.get_value()
        vg = self.vagal.get_value()
        vol = float(np.clip(self.volume.get_value(), 0.45, 1.25))
        s = self.sc()

        # Heartbeat frequency slows when vagal is up (resting ~1.15 Hz, reflex ~0.72 Hz)
        hr = 1.15 - 0.42 * float(np.clip(vg, 0.0, 1.4))
        self._beat_phase = (self._beat_phase + dt * hr) % 1.0
        # Heartbeat contraction wave
        beat_pulse = np.exp(-((self._beat_phase - 0.15) / 0.09) ** 2)
        puff_scale = 0.55 + 0.45 * vol   # smaller stroke puff when volume is drained!
        if hasattr(self, "_heart_body"):
            hc = self.to_scene(self._heart_c)
            # Re-scale cleanly around base size
            target_h = 1.18 * s * (1.0 + 0.085 * beat_pulse * puff_scale)
            target_w = 1.22 * s * (1.0 + 0.085 * beat_pulse * puff_scale)
            self._heart_body.stretch_to_fit_height(target_h)
            self._heart_body.stretch_to_fit_width(target_w)
            self._heart_body.move_to(hc)

        # Stroke puff moving out of top of heart on each beat
        puff_u = self._beat_phase
        puff_pos = self.to_scene([-4.80, -0.92 + 0.85 * puff_u, 0.0])
        puff_r = (0.06 + 0.12 * puff_scale) * (1.0 - 0.45 * puff_u) * s
        puff_op = float(np.clip(np.sin(puff_u * PI) * (0.40 + 0.50 * vol), 0.0, 0.90))
        self._puff.become(
            Circle(radius=max(0.02, puff_r), color=BLOOD_BLUE, stroke_width=3.5 * puff_scale,
                   fill_color=BLOOD_BLUE, fill_opacity=puff_op * 0.55)
            .set_stroke(opacity=puff_op)
            .move_to(puff_pos)
        )

        # Blood flow dots moving clockwise around the loop
        # Speed slows with heart rate; fewer visible dots return along vein when volume is low
        flow_speed = 0.115 * (hr / 1.15) * (0.68 + 0.32 * vol)
        self._flow_phase = (self._flow_phase + dt * flow_speed) % 1.0
        n_active = max(11, int(round(self._n_blood * (0.55 + 0.45 * vol))))
        for i, d in enumerate(self.blood_dots):
            if i >= n_active:
                d.set_opacity(0.0)
                continue
            u = (d.u0 + self._flow_phase) % 1.0
            q = _interp_path(self._flow_pts, self._flow_s, u)
            d.move_to(self.to_scene(q))
            d.set_opacity(0.90)
            d.scale_to_fit_width(0.13 * s)

        # Sensor firing rate speeds up with pressure above 100
        fire_hz = float(np.clip(0.85 + 0.24 * (p - P_BASE), 0.35, 4.0))
        self._sensor_phase = (self._sensor_phase + dt * fire_hz) % 1.0
        car_c = self.to_scene(self._carotid_c)
        arch_c = self.to_scene(self._arch_sensor_c)
        stretch = float(np.clip((p - P_BASE) / 15.0, 0.0, 1.3))
        base_r_car = (0.29 + 0.13 * stretch) * s
        base_r_arc = (0.24 + 0.08 * stretch) * s
        for k in range(3):
            ph = (self._sensor_phase + k / 3.0) % 1.0
            op = float(np.clip((1.0 - ph) * (0.48 + 0.50 * min(1.0, max(0.0, (p - 98.0) / 8.0))), 0.0, 0.95))
            self._carotid_ripples[k].become(
                Circle(radius=base_r_car + (0.34 + 0.18 * stretch) * ph * s, color=CYAN, stroke_width=(3.0 + 1.4 * stretch) * (1.0 - 0.5 * ph))
                .set_stroke(opacity=op)
                .move_to(car_c)
            )
            self._arch_ripples[k].become(
                Circle(radius=base_r_arc + (0.30 + 0.16 * stretch) * ph * s, color=CYAN, stroke_width=(2.8 + 1.4 * stretch) * (1.0 - 0.5 * ph))
                .set_stroke(opacity=op)
                .move_to(arch_c)
            )

        # Cyan afferent pulses travelling up to brainstem (disabled if wires cut)
        aff_on = self.vagal.get_value() > -0.5
        self._aff_phase = (self._aff_phase + dt * fire_hz * 0.65) % 1.0
        for k in range(3):
            ph = (self._aff_phase + k / 3.0) % 1.0
            if aff_on:
                q1 = _interp_path(self._aff1_pts, self._aff1_s, ph)
                q2 = _interp_path(self._aff2_pts, self._aff2_s, ph)
                self._aff1_dots[k].move_to(self.to_scene(q1)).set_opacity(0.92)
                self._aff2_dots[k].move_to(self.to_scene(q2)).set_opacity(0.88)
            else:
                self._aff1_dots[k].set_opacity(0.0)
                self._aff2_dots[k].set_opacity(0.0)

        # Salt-in dots (entering arch at top) and Salt+Water drops (exiting kidney outlet)
        sin_r = self.salt_in_rate.get_value()
        if self.salt_out_coupled and self.kidney_on:
            sout_r = max(0.0, renal_excretion(p) / SALT_INTAKE) * sin_r
        else:
            sout_r = 0.0
        self._salt_phase += dt

        for k, d in enumerate(self._salt_in_dots):
            if sin_r <= 0.05:
                d.set_opacity(0.0)
            else:
                ph = (self._salt_phase * 0.55 * sin_r + k / self._n_salt_in) % 1.0
                # Drop into top of aortic arch at (-3.55, 2.05 -> 1.38)
                q = np.array([-3.55 + 0.06 * np.sin(k * 2.1), 2.02 - 0.64 * ph, 0.0])
                d.move_to(self.to_scene(q)).set_opacity(float(np.sin(ph * PI)))

        n_out_vis = int(np.clip(round(self._n_salt_out * (sout_r / 1.8)), 0, self._n_salt_out))
        for k in range(self._n_salt_out):
            sd = self._salt_out_dots[k]
            wd = self._water_out_dots[k]
            if not self.kidney_on or sout_r <= 0.05 or k >= n_out_vis:
                sd.set_opacity(0.0)
                wd.set_opacity(0.0)
            else:
                ph = (self._salt_phase * 0.65 * max(0.3, sout_r) + k / max(1, n_out_vis)) % 1.0
                # Stream cleanly out of bottom kidney nozzle (-2.15, -0.92) down to (-2.15, -1.48), clear of vein (-1.62)
                y_drop = -0.92 - 0.52 * ph
                x_off = 0.08 * ((k % 2) * 2 - 1)
                op = float(np.sin(ph * PI))
                sd.move_to(self.to_scene([-2.15 + x_off, y_drop, 0.0])).set_opacity(op)
                wd.move_to(self.to_scene([-2.15 - x_off, y_drop - 0.06, 0.0])).set_opacity(op * 0.90)

    def _tick(self, dt):
        if self._state_key() != self._last_geom_state:
            self._rebuild_geometry()
        self._update_dynamic(dt)


# ---------------------------------------------------------------------------
# Helpers for shared plot overlays carried across scenes
# ---------------------------------------------------------------------------
def build_s05_plot_state(show_ghost=True, show_brackets=True, trace_end=6.0):
    """Build the right-hand time plot at the settled reflex state (P = 106.7)."""
    P, base_line = make_time_plot()
    start_lbl = T("start: 100 (rounded from 93)", size=22, color=TEXT).move_to(
        [P.pt(5.2, 95.0)[0], P.pt(0, 97.3)[1], 0.0]
    )
    tag = make_plot_tag("teaching numbers")

    ghost_grp = VGroup()
    if show_ghost:
        ghost_curve = DashedVMobject(P.curve(lambda t: p_open_curve(t, 0.0, 1.35), 0.0, 6.2, color=CLAMP_RED, width=4.0), num_dashes=26)
        ghost_curve.set_opacity(0.55)
        ghost_lbl = T("no reflex: 120", size=22, color=CLAMP_RED).move_to([P.pt(3.6, 122.4)[0], P.pt(0, 122.4)[1], 0.0])
        ghost_lbl.set_opacity(0.85)
        ghost_grp.add(ghost_curve, ghost_lbl)

    br_grp = VGroup()
    if show_brackets:
        bx = P.pt(6.6, P_BASE)[0]
        b_rem = make_bracket([bx, P.pt(0, P_CLOSED)[1], 0], [bx, P.pt(0, P_OPEN)[1], 0], color=CYAN)
        b_left = make_bracket([bx, P.pt(0, P_BASE)[1], 0], [bx, P.pt(0, P_CLOSED)[1], 0], color=BRIGHT_WHITE)
        l_rem = T("removed:\n13.3", size=22, color=CYAN, line_spacing=0.85).next_to(b_rem, RIGHT, buff=0.14)
        l_left = T("left: 6.7", size=22, color=BRIGHT_WHITE).next_to(b_left, RIGHT, buff=0.14)
        br_grp.add(b_rem, b_left, l_rem, l_left)

    p_lbl = M("106.7", size=26, color=BRIGHT_WHITE).move_to([P.pt(3.15, 109.5)[0], P.pt(0, 109.5)[1], 0.0])
    return P, base_line, start_lbl, tag, ghost_grp, br_grp, p_lbl


def build_renal_base(p_tracker, show_kidney_line=True, show_intake=True, show_crossing=True, tag_text="teaching lines",
                     clock_center=(5.05, 2.74, 0.0)):
    """Build the right-hand renal plot (s10-s15) with computed lines and live marker."""
    P = make_renal_plot()
    tag = make_plot_tag(tag_text)
    clock = make_clock_badge("days", hand_angle=0.8, center=clock_center)

    k_grp = VGroup()
    if show_kidney_line:
        k_line = P.curve(renal_excretion, 90.0, 122.5, color=KIDNEY_GREEN, width=5.5)
        k_lbl = T("kidney", size=26, color=KIDNEY_GREEN).move_to(P.pt(109.0, 325.0))
        k_grp.add(k_line, k_lbl)

    in_grp = VGroup()
    if show_intake:
        in_line = DashedLine(P.pt(90.0, SALT_INTAKE), P.pt(125.0, SALT_INTAKE), color=SALT_GOLD, stroke_width=4.0, dash_length=0.16)
        in_lbl = T("salt in", size=24, color=SALT_GOLD).move_to([P.pt(120.5, SALT_INTAKE)[0], P.pt(0, SALT_INTAKE)[1] - 0.34, 0.0])
        in_grp.add(in_line, in_lbl)

    cr_grp = VGroup()
    if show_crossing:
        eq_pt = P.pt(P_BASE, SALT_INTAKE)
        ring = Circle(radius=0.18, color=SALT_GOLD, stroke_width=4.5, fill_color=SALT_GOLD, fill_opacity=0.18).move_to(eq_pt)
        vdrop = DashedLine(eq_pt + DOWN * 0.18, P.pt(P_BASE, 0.0), color=TEXT, stroke_width=2.2, dash_length=0.10).set_opacity(0.65)
        cr_lbl = T("out = in", size=24, color=SALT_GOLD).move_to(P.pt(94.8, 208.0))
        cr_grp.add(vdrop, ring, cr_lbl)

    # Live white pressure marker: vertical guide + dot on kidney curve + small tick triangle on x-axis
    def _mk_marker():
        pv = float(np.clip(p_tracker.get_value(), 90.0, 125.0))
        xb = P.pt(pv, 0.0)
        yt = P.pt(pv, renal_excretion(pv)) if show_kidney_line else P.pt(pv, 0.0)
        guide = DashedLine(xb, yt, color=BRIGHT_WHITE, stroke_width=2.0, dash_length=0.09).set_opacity(0.65)
        tri = Triangle(color=BRIGHT_WHITE, fill_color=BRIGHT_WHITE, fill_opacity=1.0).scale(0.11).move_to(xb + UP * 0.06)
        dot = Dot(yt if show_kidney_line else xb, radius=0.105, color=BRIGHT_WHITE, stroke_color=BG, stroke_width=2.0)
        return VGroup(guide, tri, dot) if show_kidney_line else VGroup(tri, dot)

    marker = always_redraw(_mk_marker)
    return P, tag, clock, k_grp, in_grp, cr_grp, marker


# ===========================================================================
# SCENE 00: HOOK (13.15 s)
# ===========================================================================
class S00Hook(SpokenScene):
    def construct(self):
        world = CirculationWorld(pressure=P_BASE, clamp=0.0, vagal=0.0, symp=0.0, volume=1.0)
        P, base_line = make_time_plot()
        tag = make_plot_tag("schematic")

        fn = hook_trace_fn()
        t_tr = ValueTracker(0.0)
        live = P.live_curve(fn, t_tr, color=BRIGHT_WHITE, width=4.8)
        dot = P.dot(lambda: t_tr.get_value(), lambda: fn(t_tr.get_value()), color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.10)

        # Couple world pressure & reflex flicker directly to the live hook curve
        def sync_hook(m, dt):
            tv = t_tr.get_value()
            pv = fn(tv)
            world.pressure.set_value(pv)
            err = (pv - P_BASE) / 10.0
            # Brief reflex response lags slightly behind each bump
            world.vagal.set_value(float(np.clip(err * 0.9, -0.3, 1.1)))
            world.symp.set_value(float(np.clip(-err * 0.9, -1.1, 0.3)))

        world.add_updater(sync_hook)

        self.add(world, P, base_line, tag, live, dot)

        # 0.0 -> 5.2s: posture and activity push pressure around (bumps 1 & 2)
        self.play(t_tr.animate.set_value(5.6), run_time=max(0.5, self.t_of("within seconds") - 0.2), rate_func=linear)

        # 5.3s -> 10.4s: within seconds a reflex pushes back, never quite finishes (bump 3)
        self.play(t_tr.animate.set_value(9.3), run_time=max(0.5, self.t_of("what decides") - 0.25 - self.elapsed()), rate_func=linear)

        # Question across top
        q = T("Where does pressure settle?", size=34, color=BRIGHT_WHITE).move_to([0.0, 3.28, 0.0])
        self.play(
            FadeIn(q, shift=DOWN * 0.12),
            t_tr.animate.set_value(9.8),
            run_time=0.8,
            rate_func=linear,
        )
        self.finish()


# ===========================================================================
# SCENE 01: TITLE (silent 2.0 s)
# ===========================================================================
class S01Title(NarratedScene):
    def construct(self):
        world = CirculationWorld(pressure=P_BASE + 3.0, clamp=0.0, vagal=0.25, symp=-0.25, volume=1.0)
        P, base_line = make_time_plot()
        tag = make_plot_tag("schematic")

        # Trace smooths from the hook's slight offset down to a flat line at 100
        def smooth_fn(t):
            return P_BASE + 3.0 * np.exp(-t / 1.1)

        t_tr = ValueTracker(0.5)
        live = P.live_curve(smooth_fn, t_tr, color=BRIGHT_WHITE, width=4.8)
        dot = P.dot(lambda: t_tr.get_value(), lambda: smooth_fn(t_tr.get_value()), color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.10)

        q = T("Where does pressure settle?", size=34, color=BRIGHT_WHITE).move_to([0.0, 3.28, 0.0])
        title = T("Two Clocks for Pressure", size=40, font=TITLE_FONT, color=BRIGHT_WHITE).move_to([0.0, 3.28, 0.0])
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=SALT_GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.10)

        self.add(world, P, base_line, tag, live, dot, q)

        # Fade out question cleanly before fading in title; smooth trace and return wires to resting
        self.play(
            FadeOut(q),
            t_tr.animate.set_value(2.4),
            world.pressure.animate.set_value(P_BASE),
            world.vagal.animate.set_value(0.0),
            world.symp.animate.set_value(0.0),
            run_time=0.45,
            rate_func=linear,
        )
        self.play(
            FadeIn(title, shift=UP * 0.08),
            GrowFromCenter(rule),
            t_tr.animate.set_value(5.0),
            run_time=0.55,
            rate_func=linear,
        )
        self.play(t_tr.animate.set_value(9.4), run_time=1.0, rate_func=linear)
        self.finish()


# ===========================================================================
# SCENE 02: SQUEEZE (14.80 s)
# ===========================================================================
class S02Squeeze(SpokenScene):
    def construct(self):
        world = CirculationWorld(pressure=P_BASE, clamp=0.0, vagal=0.0, symp=0.0, volume=1.0)
        P, base_line = make_time_plot()
        tag = make_plot_tag("teaching numbers")

        # Continuous flat trace at 100
        t_flat = ValueTracker(0.2)
        flat_line = P.live_curve(lambda t: P_BASE, t_flat, color=BRIGHT_WHITE, width=4.5)
        flat_dot = P.dot(lambda: t_flat.get_value(), lambda: P_BASE, color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.095)

        self.add(world, P, base_line, tag, flat_line, flat_dot)

        # Draw flat line forward up to "Call it 100" (no fake 93 dot on a 95-bottom axis!)
        self.play(t_flat.animate.set_value(4.8), run_time=max(0.4, self.t_of("call it 100") - 0.2), rate_func=linear)

        # Label the dashed 100 line cleanly as the script states
        start_lbl = T("start: 100 (rounded from 93)", size=22, color=TEXT).move_to(
            [P.pt(5.2, 95.0)[0], P.pt(0, 97.3)[1], 0.0]
        )
        self.play(FadeIn(start_lbl, shift=UP * 0.06), t_flat.animate.set_value(5.6), run_time=0.75, rate_func=linear)

        # Wait to "Squeeze the small"
        rest_t = self.t_of("squeeze the small") - 0.2 - self.elapsed()
        if rest_t > 0.1:
            self.play(t_flat.animate.set_value(6.0), run_time=rest_t, rate_func=linear)

        # RED clamp closes on small arteries, visibly narrowing the tube
        self.play(world.clamp.animate.set_value(1.0), run_time=0.95)

        # Wait to "with no reflex"
        self.at("with no reflex")
        # Grey out / cut wires for the open-loop ghost
        self.play(world.vagal.animate.set_value(-1.0), world.symp.animate.set_value(-2.0), run_time=0.55)

        # On "climb to 120": dashed RED ghost trace climbs 100 -> 120
        self.at("climb to 120", lead=0.35)
        tg = ValueTracker(0.0)
        ghost_live = always_redraw(
            lambda: DashedVMobject(
                P.curve(lambda u: p_open_curve(u, 0.0, 1.35), 0.0, max(0.15, tg.get_value()), color=CLAMP_RED, width=4.5),
                num_dashes=max(2, int(round(4.2 * tg.get_value()))),
            )
            if tg.get_value() > 0.18
            else VGroup()
        )
        ghost_dot = P.dot(lambda: tg.get_value(), lambda: p_open_curve(tg.get_value(), 0.0, 1.35), color=CLAMP_RED, ring=CLAMP_RED, radius=0.09)
        ghost_lbl = T("no reflex: 120", size=22, color=CLAMP_RED).move_to([P.pt(3.6, 122.4)[0], P.pt(0, 122.4)[1], 0.0])
        self.add(ghost_live, ghost_dot)
        self.play(tg.animate.set_value(6.2), run_time=1.8, rate_func=smooth)
        self.play(FadeIn(ghost_lbl), FadeOut(ghost_dot), run_time=0.4)
        self.finish()


# ===========================================================================
# SCENE 03: SENSOR (12.525 s)
# ===========================================================================
class S03Sensor(SpokenScene):
    def construct(self):
        # Start with clamp closed, wires momentarily greyed out then returning to colour
        # Keep external static labels outside world so fading them out never suspends world's updater
        world = CirculationWorld(pressure=P_BASE, clamp=1.0, vagal=-1.0, symp=-2.0, volume=1.0, show_labels=False)
        ext_labels = VGroup(
            T("heart", size=24, color=TEXT).move_to(world.to_scene([-4.80, -2.52, 0.0])),
            T("vein", size=24, color=TEXT).move_to(world.to_scene([-2.35, -2.42, 0.0])),
            T("small\narteries", size=22, color=TEXT, line_spacing=0.85).move_to(world.to_scene([-0.22, 2.02, 0.0])),
        )
        P, base_line, start_lbl, tag, ghost_grp, _, _ = build_s05_plot_state(show_ghost=True, show_brackets=False)

        t_real = ValueTracker(0.05)
        real_live = P.live_curve(lambda t: p_closed_curve(t, 0.0, 1.8), t_real, color=BRIGHT_WHITE, width=5.0)
        real_dot = P.dot(lambda: t_real.get_value(), lambda: p_closed_curve(t_real.get_value(), 0.0, 1.8),
                         color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.10)

        # Disturbance bracket 100 -> 120
        bx = P.pt(6.6, P_BASE)[0]
        dist_br = make_bracket([bx, P.pt(0, P_BASE)[1], 0], [bx, P.pt(0, P_OPEN)[1], 0], color=CLAMP_RED)
        dist_lbl = T("disturbance:\n20", size=22, color=CLAMP_RED, line_spacing=0.85).next_to(dist_br, RIGHT, buff=0.14)

        plot_all = VGroup(P, base_line, start_lbl, tag, ghost_grp, real_live, real_dot, dist_br, dist_lbl)
        self.add(world, ext_labels, P, base_line, start_lbl, tag, ghost_grp, real_live, real_dot)

        # On "rise of 20": show disturbance bracket
        self.at("rise of 20")
        self.play(Create(dist_br), FadeIn(dist_lbl), run_time=0.75)

        # Return wires to colour (reflex intact) & start rising real white trace
        self.at("stretch receptors", lead=0.45)
        self.play(
            world.vagal.animate.set_value(0.0),
            world.symp.animate.set_value(0.0),
            t_real.animate.set_value(1.5),
            world.pressure.animate.set_value(p_closed_curve(1.5, 0.0, 1.8)),
            run_time=1.1,
        )

        # On "carotid sinuses": fade plot & external labels cleanly first, then push in on carotid sinus bulge
        self.at("carotid sinuses", lead=0.45)
        self.play(FadeOut(plot_all), FadeOut(ext_labels), run_time=0.25)
        self.play(
            world.cam_scale.animate.set_value(1.26),
            world.cam_dx.animate.set_value(2.75),
            world.cam_dy.animate.set_value(-0.42),
            world.pressure.animate.set_value(104.5),
            run_time=0.80,
        )
        car_lbl = T("carotid sinus", size=30, color=CYAN).move_to([2.85, 2.38, 0.0])
        car_arr = Arrow(car_lbl.get_left() + LEFT * 0.10, world.to_scene(world._carotid_c) + RIGHT * 0.56,
                        color=CYAN, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.16)
        self.play(FadeIn(car_lbl), GrowArrow(car_arr), run_time=0.55)

        # On "and in the [aortic] arch": pan smoothly toward aortic arch, keeping full ripple margin below top edge
        self.at("and in the", lead=0.20)
        new_car_pos = np.array([2.35, 2.48, 0.0])
        arch_after = WORLD_CENTER + 1.26 * (world._arch_sensor_c - WORLD_CENTER) + np.array([1.90, -0.32, 0.0])
        car_after = WORLD_CENTER + 1.26 * (world._carotid_c - WORLD_CENTER) + np.array([1.90, -0.32, 0.0])
        arch_lbl = T("aortic arch", size=30, color=CYAN).move_to([4.45, 1.34, 0.0])
        arch_arr = Arrow(arch_lbl.get_left() + LEFT * 0.10, arch_after + RIGHT * 0.42,
                         color=CYAN, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.14)
        new_car_arr = Arrow(new_car_pos + LEFT * (car_lbl.width / 2 + 0.10), car_after + RIGHT * 0.56,
                            color=CYAN, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.16)
        self.play(
            world.cam_dx.animate.set_value(1.90),
            world.cam_dy.animate.set_value(-0.32),
            car_lbl.animate.move_to(new_car_pos),
            Transform(car_arr, new_car_arr),
            world.pressure.animate.set_value(107.0),
            run_time=0.85,
        )
        self.play(FadeIn(arch_lbl), GrowArrow(arch_arr), run_time=0.50)

        # On "fire faster as the walls stretch": push pressure continuously so bulge & firing accelerate visibly
        self.at("fire faster", lead=0.25)
        self.play(world.pressure.animate.set_value(116.0), run_time=2.3, rate_func=smooth)
        self.finish()


# ===========================================================================
# SCENE 04: ARC (17.10 s)
# ===========================================================================
class S04Arc(SpokenScene):
    def construct(self):
        # Start from the zoomed-in sensor state of s03, then pull back cleanly before fading in plot
        world = CirculationWorld(
            pressure=105.0, clamp=1.0, vagal=0.0, symp=0.0, volume=1.0,
            show_labels=True, show_wire_labels=False,
            cam_scale=1.26, cam_dx=1.90, cam_dy=-0.32,
        )
        world.label_group.set_opacity(0.0)

        P, base_line, start_lbl, tag, ghost_grp, _, _ = build_s05_plot_state(show_ghost=True, show_brackets=False)
        bx = P.pt(6.6, P_BASE)[0]
        dist_br = make_bracket([bx, P.pt(0, P_BASE)[1], 0], [bx, P.pt(0, P_OPEN)[1], 0], color=CLAMP_RED)
        dist_lbl = T("disturbance:\n20", size=22, color=CLAMP_RED, line_spacing=0.85).next_to(dist_br, RIGHT, buff=0.14)

        t_real = ValueTracker(1.4)
        real_live = P.live_curve(lambda t: p_closed_curve(t, 0.0, 1.8), t_real, color=BRIGHT_WHITE, width=5.0)
        real_dot = P.dot(lambda: t_real.get_value(), lambda: p_closed_curve(t_real.get_value(), 0.0, 1.8),
                         color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.10)

        plot_grp = VGroup(P, base_line, start_lbl, tag, ghost_grp, dist_br, dist_lbl, real_live, real_dot)

        self.add(world)

        # Pull back smoothly to left side first, then fade in plot (zero transient collisions!)
        self.play(
            world.cam_scale.animate.set_value(1.0),
            world.cam_dx.animate.set_value(0.0),
            world.cam_dy.animate.set_value(0.0),
            run_time=0.75,
        )
        self.play(
            world.label_group.animate.set_opacity(1.0),
            FadeIn(plot_grp),
            run_time=0.35,
        )
        # Pulse brainstem as cyan signals arrive
        self.play(
            Indicate(world.brainstem_box, color=CYAN, scale_factor=1.08),
            t_real.animate.set_value(2.3),
            world.pressure.animate.set_value(p_closed_curve(2.3, 0.0, 1.8)),
            run_time=0.85,
        )

        # Vagal output up (purple wire thickens & brightens)
        self.at("vagal output")
        self.play(
            world.vagal.animate.set_value(1.0),
            FadeIn(world.lbl_vagal, shift=UP * 0.08),
            t_real.animate.set_value(3.2),
            world.pressure.animate.set_value(p_closed_curve(3.2, 0.0, 1.8)),
            run_time=1.1,
        )

        # Sympathetic output down (orange wires thin & dim)
        self.at("sympathetic output")
        self.play(
            world.symp.animate.set_value(-1.0),
            FadeIn(world.lbl_symp, shift=UP * 0.08),
            t_real.animate.set_value(4.2),
            world.pressure.animate.set_value(p_closed_curve(4.2, 0.0, 1.8)),
            run_time=1.1,
        )

        # Heart slows (blood dots & heartbeat visibly slow; subtle indicator on heart)
        self.at("the heart slows")
        self.play(
            Indicate(world.lbl_heart, color=PURPLE, scale_factor=1.12),
            t_real.animate.set_value(5.0),
            world.pressure.animate.set_value(p_closed_curve(5.0, 0.0, 1.8)),
            run_time=1.2,
        )

        # Small arteries relax partly (clamp stays closed, tube still narrower than at rest)
        self.at("small arteries relax")
        self.play(
            Indicate(world.lbl_small_art, color=ORANGE, scale_factor=1.10),
            t_real.animate.set_value(5.6),
            world.pressure.animate.set_value(p_closed_curve(5.6, 0.0, 1.8)),
            run_time=1.4,
        )

        # Veins relax, less blood returns; trace bends cleanly below red ghost
        self.at("veins relax")
        self.play(
            Indicate(world.lbl_vein, color=ORANGE, scale_factor=1.12),
            world.volume.animate.set_value(0.92),
            t_real.animate.set_value(6.2),
            world.pressure.animate.set_value(P_CLOSED),
            run_time=1.6,
        )
        self.finish()


# ===========================================================================
# SCENE 05: GAIN (13.40 s)
# ===========================================================================
class S05Gain(SpokenScene):
    def construct(self):
        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            show_wire_labels=True,
        )
        P, base_line, start_lbl, tag, ghost_grp, _, p_lbl = build_s05_plot_state(show_ghost=True, show_brackets=False)

        bx = P.pt(6.6, P_BASE)[0]
        dist_br = make_bracket([bx, P.pt(0, P_BASE)[1], 0], [bx, P.pt(0, P_OPEN)[1], 0], color=CLAMP_RED)
        dist_lbl = T("disturbance:\n20", size=22, color=CLAMP_RED, line_spacing=0.85).next_to(dist_br, RIGHT, buff=0.14)

        # Trace draws flat forward at 106.7 (from x=0.4 to x=6.2)
        t_tr = ValueTracker(2.2)
        live = P.live_curve(lambda t: P_CLOSED, t_tr, color=BRIGHT_WHITE, width=5.0)
        dot = P.dot(lambda: t_tr.get_value(), lambda: P_CLOSED, color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.10)

        self.add(world, P, base_line, start_lbl, tag, ghost_grp, dist_br, dist_lbl, live, dot)

        # Pressure settles near 106.7
        self.at("settles near")
        self.play(FadeIn(p_lbl, shift=UP * 0.08), t_tr.animate.set_value(3.8), run_time=1.2, rate_func=linear)

        # Wait to "reflex removed"
        rest_t = self.t_of("reflex removed") - 0.25 - self.elapsed()
        if rest_t > 0.1:
            self.play(t_tr.animate.set_value(4.5), run_time=rest_t, rate_func=linear)

        # Split disturbance bracket into upper CYAN "removed: 13.3" and lower WHITE "left: 6.7"
        b_rem = make_bracket([bx, P.pt(0, P_CLOSED)[1], 0], [bx, P.pt(0, P_OPEN)[1], 0], color=CYAN)
        b_left = make_bracket([bx, P.pt(0, P_BASE)[1], 0], [bx, P.pt(0, P_CLOSED)[1], 0], color=BRIGHT_WHITE)
        l_rem = T("removed:\n13.3", size=22, color=CYAN, line_spacing=0.85).next_to(b_rem, RIGHT, buff=0.14)
        l_left = T("left: 6.7", size=22, color=BRIGHT_WHITE).next_to(b_left, RIGHT, buff=0.14)

        self.play(
            FadeOut(dist_br, run_time=0.25),
            Succession(FadeOut(dist_lbl, run_time=0.25), FadeIn(l_rem, run_time=0.45)),
            Create(b_rem, run_time=0.75),
            t_tr.animate.set_value(5.1),
            run_time=0.85,
        )

        # "and left 6.7"
        self.at("and left")
        self.play(Create(b_left), FadeIn(l_left), t_tr.animate.set_value(5.7), run_time=0.9)

        # "Correction divided by what is left gives a gain of 2" (crisp spacing, no crossing labels)
        self.at("correction divided")
        eq_num = M("13.3", size=34, color=CYAN)
        eq_div = M("÷", size=34, color=TEXT)
        eq_den = M("6.7", size=34, color=BRIGHT_WHITE)
        eq_eq = M("=", size=34, color=TEXT)
        eq_val = M("2", size=34, color=SALT_GOLD)
        eq_grp = VGroup(eq_num, eq_div, eq_den, eq_eq, eq_val).arrange(RIGHT, buff=0.16).move_to([3.75, 3.24, 0.0])

        self.play(
            Indicate(l_rem, color=CYAN, scale_factor=1.08),
            Indicate(l_left, color=BRIGHT_WHITE, scale_factor=1.08),
            FadeIn(eq_num, shift=UP * 0.12),
            FadeIn(eq_div),
            FadeIn(eq_den, shift=UP * 0.12),
            t_tr.animate.set_value(6.0),
            run_time=1.0,
        )
        self.at("gain of 2", lead=0.25)
        self.play(FadeIn(eq_eq), FadeIn(eq_val, shift=RIGHT * 0.08), t_tr.animate.set_value(6.2), run_time=0.6)
        self.finish()


# ===========================================================================
# SCENE 06: PREDICT (11.65 s)
# ===========================================================================
class S06Predict(SpokenScene):
    def construct(self):
        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            show_wire_labels=True,
        )
        P, base_line, start_lbl, tag, ghost_grp, br_grp, p_lbl = build_s05_plot_state(show_ghost=True, show_brackets=True)

        p_dot_val = ValueTracker(P_CLOSED)
        # Live trace holds flat across 0..5.8 and moves dot vertically when nudged
        base_trace = P.curve(lambda t: P_CLOSED, 0.0, 5.8, color=BRIGHT_WHITE, width=4.8)
        dot = P.dot(lambda: 5.8, lambda: p_dot_val.get_value(), color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.11)
        # Vertical nudge connector from 106.7 to dot when nudged
        nudge_line = always_redraw(
            lambda: Line(P.pt(5.8, P_CLOSED), P.pt(5.8, p_dot_val.get_value()), color=BRIGHT_WHITE, stroke_width=3.5)
            if abs(p_dot_val.get_value() - P_CLOSED) > 0.25
            else VGroup()
        )

        # Couple world reflex strength to the nudged dot pressure
        def sync_nudge(m, dt):
            pv = p_dot_val.get_value()
            world.pressure.set_value(pv)
            scale = (pv - P_BASE) / ERROR_SS   # 1.0 at 106.7, ~2.2 at 115
            world.vagal.set_value(float(np.clip(scale, 0.0, 1.9)))
            world.symp.set_value(float(np.clip(-scale, -1.5, 0.0)))

        world.add_updater(sync_nudge)

        self.add(world, P, base_line, start_lbl, tag, ghost_grp, br_grp, p_lbl, base_trace, nudge_line, dot)

        # On "removes [two-thirds]": show 3 equal segments of the 20-mmHg bracket
        self.at("removes")
        bx = P.pt(6.35, P_BASE)[0]
        seg1 = Line([bx, P.pt(0, 100.0)[1], 0], [bx, P.pt(0, 106.67)[1] - 0.04, 0], color=BRIGHT_WHITE, stroke_width=8.0)
        seg2 = Line([bx, P.pt(0, 106.67)[1] + 0.04, 0], [bx, P.pt(0, 113.33)[1] - 0.04, 0], color=CYAN, stroke_width=8.0)
        seg3 = Line([bx, P.pt(0, 113.33)[1] + 0.04, 0], [bx, P.pt(0, 120.0)[1], 0], color=CYAN, stroke_width=8.0)
        thirds = VGroup(seg1, seg2, seg3)
        self.play(Create(thirds), run_time=1.0)

        # On "further pressure strays": hide static 106.7 while dot nudges up to 116 -> stronger reflex
        self.at("further pressure strays")
        self.play(FadeOut(p_lbl, run_time=0.25), p_dot_val.animate.set_value(116.0), run_time=1.4, rate_func=smooth)

        # On "harder the reflex pushes": ease back down to 106.7 and restore 106.7 label
        self.at("harder the reflex")
        self.play(p_dot_val.animate.set_value(P_CLOSED), run_time=1.4, rate_func=smooth)
        self.play(FadeIn(p_lbl, run_time=0.25))

        # On "So why does it stop short of 100?": show top question card matching S07Pause
        self.at("so why does")
        q = T("Why not all the way to 100?", size=34, color=BRIGHT_WHITE).move_to([-0.55, 3.28, 0.0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.65)
        self.finish()


# ===========================================================================
# SCENE 07: PAUSE (silent 4.5 s — PredictPause)
# ===========================================================================
class S07Pause(PredictPause):
    QUESTION = "Why not all the way to 100?"
    CARD = {"y": 3.28, "color": BRIGHT_WHITE, "size": 34, "max_w": 10.0}
    RING_AT = (5.80, 3.24, 0.0)
    SECONDS = 4.5

    def backdrop(self):
        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            show_wire_labels=True,
        )
        P, base_line, start_lbl, tag, ghost_grp, br_grp, p_lbl = build_s05_plot_state(show_ghost=True, show_brackets=True)

        # Trace keeps drawing flat forward at 106.7 during the 4.5 s pause
        t_tr = ValueTracker(0.5)
        live = P.live_curve(lambda t: P_CLOSED, t_tr, color=BRIGHT_WHITE, width=4.8)
        dot = P.dot(lambda: t_tr.get_value(), lambda: P_CLOSED, color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.10)

        def advance(m, dt):
            t_tr.set_value(min(5.9, t_tr.get_value() + dt * 1.1))

        live.add_updater(advance)
        return VGroup(world, P, base_line, start_lbl, tag, ghost_grp, br_grp, p_lbl, live, dot)


# ===========================================================================
# SCENE 08: ANSWER (8.075 s)
# ===========================================================================
class S08Answer(SpokenScene):
    def construct(self):
        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            show_wire_labels=True,
        )
        P, base_line, start_lbl, tag, ghost_grp, _, p_lbl = build_s05_plot_state(show_ghost=True, show_brackets=False)
        q = T("Why not all the way to 100?", size=34, color=BRIGHT_WHITE).move_to([-0.55, 3.28, 0.0])

        # Real trace & real dot at 106.7
        real_trace = P.curve(lambda t: P_CLOSED, 0.0, 5.5, color=BRIGHT_WHITE, width=4.8)
        real_dot = Dot(P.pt(5.5, P_CLOSED), radius=0.105, color=BRIGHT_WHITE)

        # Real error double-arrow (100..106.7) and real push arrow (120 -> 106.7, length = 2 * error)
        ax_x = P.pt(6.6, P_BASE)[0]
        err_arr = DoubleArrow(
            [ax_x, P.pt(0, P_BASE)[1], 0], [ax_x, P.pt(0, P_CLOSED)[1], 0],
            color=BRIGHT_WHITE, stroke_width=4.0, buff=0.02, tip_length=0.16,
        )
        err_lbl = T("error", size=24, color=BRIGHT_WHITE).next_to(err_arr, RIGHT, buff=0.16)

        push_arr = Arrow(
            [ax_x, P.pt(0, P_OPEN)[1], 0], [ax_x, P.pt(0, P_CLOSED)[1], 0],
            color=CYAN, stroke_width=5.0, buff=0.02, tip_length=0.20,
        )
        push_lbl = T("push", size=24, color=CYAN).next_to(push_arr, RIGHT, buff=0.16)

        self.add(world, P, base_line, start_lbl, tag, ghost_grp, p_lbl, real_trace, real_dot, q)

        # Dissolve question card and show proportional error & push arrows
        self.play(FadeOut(q), GrowArrow(err_arr), FadeIn(err_lbl), run_time=0.65)
        self.at("proportional to")
        self.play(GrowArrow(push_arr), FadeIn(push_lbl), run_time=0.75)

        # Thought experiment (dashed ghost only): ghost dot slides 106.7 -> 100
        self.at("at 100", lead=0.35)
        gp = ValueTracker(P_CLOSED)
        gx = P.pt(4.5, P_BASE)[0]

        def mk_ghost_arrows():
            pv = gp.get_value()
            err = max(0.0, pv - P_BASE)
            g = VGroup()
            g.add(DashedVMobject(Circle(radius=0.13, color=BRIGHT_WHITE, stroke_width=3.0).move_to([gx, P.pt(0, pv)[1], 0]), num_dashes=8))
            if err > 0.35:
                y0 = P.pt(0, P_BASE)[1]
                y1 = P.pt(0, pv)[1]
                y2 = P.pt(0, pv + GAIN * err)[1]
                g.add(DoubleArrow([gx, y0, 0], [gx, y1, 0], color=BRIGHT_WHITE, stroke_width=3.2, buff=0.02, tip_length=0.14).set_opacity(0.75))
                g.add(Arrow([gx, y2, 0], [gx, y1, 0], color=CYAN, stroke_width=4.0, buff=0.02, tip_length=0.16).set_opacity(0.75))
            return g

        ghost_exp = always_redraw(mk_ghost_arrows)
        # Dim the real arrows briefly during thought experiment, and temporarily ease wires
        self.add(ghost_exp)
        self.play(
            err_arr.animate.set_opacity(0.30),
            push_arr.animate.set_opacity(0.30),
            err_lbl.animate.set_opacity(0.35),
            push_lbl.animate.set_opacity(0.35),
            gp.animate.set_value(P_BASE),
            world.vagal.animate.set_value(0.1),
            world.symp.animate.set_value(-0.1),
            run_time=1.8,
            rate_func=smooth,
        )

        # "and so would the push": ghost fades, real dot & full-length arrows + reflex state remain; red ghost trace fades out
        self.at("so would the push")
        self.play(
            FadeOut(ghost_exp),
            FadeOut(ghost_grp),
            err_arr.animate.set_opacity(1.0),
            push_arr.animate.set_opacity(1.0),
            err_lbl.animate.set_opacity(1.0),
            push_lbl.animate.set_opacity(1.0),
            world.vagal.animate.set_value(1.0),
            world.symp.animate.set_value(-1.0),
            run_time=0.95,
        )
        self.finish()


# ===========================================================================
# SCENE 09: ONE IDEA (15.20 s)
# ===========================================================================
class S09Idea(SpokenScene):
    def construct(self):
        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            kidney=False, show_wire_labels=True,
        )
        P, base_line, start_lbl, tag, _, _, p_lbl = build_s05_plot_state(show_ghost=False, show_brackets=False)

        # Keep the "left: 6.7" bracket visible
        bx = P.pt(6.6, P_BASE)[0]
        b_left = make_bracket([bx, P.pt(0, P_BASE)[1], 0], [bx, P.pt(0, P_CLOSED)[1], 0], color=BRIGHT_WHITE)
        l_left = T("left: 6.7", size=22, color=BRIGHT_WHITE).next_to(b_left, RIGHT, buff=0.14)

        t_tr = ValueTracker(2.0)
        live = P.live_curve(lambda t: P_CLOSED, t_tr, color=BRIGHT_WHITE, width=4.8)
        dot = P.dot(lambda: t_tr.get_value(), lambda: P_CLOSED, color=BRIGHT_WHITE, ring=BRIGHT_WHITE, radius=0.10)

        self.add(world, P, base_line, start_lbl, tag, p_lbl, b_left, l_left, live, dot)

        # Advance trace gently up to "Guyton's framework"
        self.play(t_tr.animate.set_value(3.2), run_time=max(0.4, self.t_of("guyton's framework") - 0.2), rate_func=linear)

        # Small tag at top left: "Guyton's framework"
        g_tag = T("Guyton's framework", size=24, color=SALT_GOLD).move_to([-5.05, 3.38, 0.0])
        self.play(FadeIn(g_tag, shift=RIGHT * 0.1), t_tr.animate.set_value(4.0), run_time=0.7)

        # On "two controllers": kidney appears on its parallel branch!
        self.at("two controllers")
        world.kidney_on = True
        world._rebuild_geometry()
        self.play(FadeIn(world.kidney_group), t_tr.animate.set_value(4.8), run_time=0.95)

        # On "how far pressure strays": glow left: 6.7 bracket + pulse brainstem & wires; label 'how far'
        self.at("how far pressure")
        lbl_how_far = T("how far", size=26, color=CYAN).move_to([-1.85, 3.06, 0.0])
        self.play(
            Indicate(VGroup(b_left, l_left), color=CYAN, scale_factor=1.12),
            Indicate(world.brainstem_box, color=CYAN, scale_factor=1.10),
            FadeIn(lbl_how_far, shift=UP * 0.08),
            t_tr.animate.set_value(5.6),
            run_time=1.1,
        )

        # On "where pressure ends up": pulse kidney; label 'where' cleanly left of kidney outlet
        self.at("where pressure ends")
        lbl_where = T("where", size=26, color=KIDNEY_GREEN).move_to([-2.78, -1.18, 0.0])
        self.play(
            Indicate(world.kidney_bean, color=KIDNEY_GREEN, scale_factor=1.14),
            FadeIn(lbl_where, shift=UP * 0.08),
            t_tr.animate.set_value(6.0),
            run_time=1.0,
        )
        self.finish()


# ===========================================================================
# SCENE 10: KIDNEY / SWITCH CLOCKS (14.55 s)
# ===========================================================================
class S10Kidney(SpokenScene):
    def construct(self):
        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            kidney=True, salt_in=0.0, salt_out_from_pressure=False, show_wire_labels=True,
        )
        g_tag = T("Guyton's framework", size=24, color=SALT_GOLD).move_to([-5.05, 3.38, 0.0])

        # Start with the seconds time plot from s09
        P_old, base_line, start_lbl, tag_old, _, _, p_lbl = build_s05_plot_state(show_ghost=False, show_brackets=False)
        old_trace = P_old.curve(lambda t: P_CLOSED, 0.0, 5.8, color=BRIGHT_WHITE, width=4.8)
        old_dot = Dot(P_old.pt(5.8, P_CLOSED), radius=0.10, color=BRIGHT_WHITE)
        clock_sec = make_clock_badge("seconds", hand_angle=0.0, center=(4.95, 3.24, 0.0))

        old_plot_grp = VGroup(P_old, base_line, start_lbl, p_lbl, old_trace)
        self.add(world, g_tag, old_plot_grp, old_dot, tag_old, clock_sec)

        # "from seconds to days": rotate clock hands and morph seconds -> days; transform plot cleanly (no cross-fade overlap)
        self.at("from seconds to days")
        clock_days = make_clock_badge("days", hand_angle=0.8, center=(5.05, 2.74, 0.0))
        P_new = make_renal_plot()
        tag_new = make_plot_tag("teaching lines")
        new_marker_pt = P_new.pt(P_CLOSED, 0.0)
        new_tri = Triangle(color=BRIGHT_WHITE, fill_color=BRIGHT_WHITE, fill_opacity=1.0).scale(0.11).move_to(new_marker_pt + UP * 0.06)
        lbl_pnow = T("pressure now", size=22, color=BRIGHT_WHITE).move_to(P_new.pt(116.2, 66.0))
        arr_pnow = Arrow(lbl_pnow.get_left() + LEFT * 0.08, new_marker_pt + UR * 0.14, color=BRIGHT_WHITE,
                         stroke_width=2.5, buff=0.04, max_tip_length_to_length_ratio=0.18)

        self.play(
            Rotate(clock_sec.min_hand, angle=-TAU, about_point=clock_sec.rim.get_center()),
            Rotate(clock_sec.hr_hand, angle=-PI / 2, about_point=clock_sec.rim.get_center()),
            run_time=0.70,
        )
        self.play(
            FadeOut(old_plot_grp),
            FadeOut(tag_old),
            FadeOut(clock_sec),
            old_dot.animate.move_to(new_marker_pt),
            run_time=0.45,
        )
        self.play(
            FadeIn(P_new),
            FadeIn(tag_new),
            FadeIn(clock_days),
            FadeIn(new_tri),
            FadeIn(lbl_pnow),
            GrowArrow(arr_pnow),
            run_time=0.60,
        )

        # "The squeeze stays on": pulse RED clamp
        self.at("squeeze stays on")
        self.play(Indicate(world.clamp_group, color=CLAMP_RED, scale_factor=1.18), run_time=0.95)

        # "As pressure rises, the kidney excretes more sodium, and water follows"
        self.at("as pressure rises")
        world.salt_out_coupled = True
        self.play(world.salt_in_rate.animate.set_value(1.0), run_time=0.9)
        self.at("more sodium")
        self.play(Indicate(world.kidney_bean, color=SALT_GOLD, scale_factor=1.12), run_time=0.9)

        # "Plotted, the kidney's line climbs with pressure"
        self.at("plotted")
        k_line = P_new.curve(renal_excretion, 90.0, 122.5, color=KIDNEY_GREEN, width=5.5)
        k_lbl = T("kidney", size=26, color=KIDNEY_GREEN).move_to(P_new.pt(109.0, 325.0))
        # Move white marker cleanly up onto the kidney curve at 106.7 with a dashed guide to x-axis
        guide = DashedLine(new_marker_pt, P_new.pt(P_CLOSED, renal_excretion(P_CLOSED)), color=BRIGHT_WHITE, stroke_width=2.0, dash_length=0.09).set_opacity(0.65)
        self.play(
            Create(k_line),
            Create(guide),
            old_dot.animate.move_to(P_new.pt(P_CLOSED, renal_excretion(P_CLOSED))),
            run_time=1.8,
        )
        self.play(FadeIn(k_lbl, shift=UP * 0.08), run_time=0.5)
        self.finish()


# ===========================================================================
# SCENE 11: CROSSING (11.30 s)
# ===========================================================================
class S11Crossing(SpokenScene):
    def construct(self):
        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            kidney=True, salt_in=1.0, salt_out_from_pressure=True, show_wire_labels=False,
        )
        # Keep reflex status labels outside world so fading them out never suspends world's updater
        wire_labels = VGroup(
            T("vagal: up", size=24, color=PURPLE).move_to([-4.95, -3.22, 0.0]),
            T("sympathetic: down", size=24, color=ORANGE).move_to([-1.75, -3.22, 0.0]),
        )
        g_tag = T("Guyton's framework", size=24, color=SALT_GOLD).move_to([-5.05, 3.38, 0.0])

        p_tr = ValueTracker(P_CLOSED)
        P, tag, clock, k_grp, _, _, marker = build_renal_base(
            p_tr, show_kidney_line=True, show_intake=False, show_crossing=False
        )
        lbl_pnow = T("pressure now", size=22, color=BRIGHT_WHITE).move_to(P.pt(116.2, 66.0))
        arr_pnow = Arrow(lbl_pnow.get_left() + LEFT * 0.08, P.pt(P_CLOSED, 0.0) + UR * 0.14, color=BRIGHT_WHITE,
                         stroke_width=2.5, buff=0.04, max_tip_length_to_length_ratio=0.18)

        self.add(world, wire_labels, g_tag, P, tag, clock, k_grp, marker, lbl_pnow, arr_pnow)

        # "flat line": dashed GOLD salt-in line slides in at y = 150
        self.at("flat line")
        in_line = DashedLine(P.pt(90.0, SALT_INTAKE), P.pt(125.0, SALT_INTAKE), color=SALT_GOLD, stroke_width=4.0, dash_length=0.16)
        in_lbl = T("salt in", size=24, color=SALT_GOLD).move_to([P.pt(120.5, SALT_INTAKE)[0], P.pt(0, SALT_INTAKE)[1] - 0.34, 0.0])
        self.play(Create(in_line), FadeIn(in_lbl, shift=RIGHT * 0.1), run_time=1.3)

        # "cross once": crossing ring glows at 100 + vertical drop to x-tick 100
        self.at("cross once")
        eq_pt = P.pt(P_BASE, SALT_INTAKE)
        ring = Circle(radius=0.18, color=SALT_GOLD, stroke_width=4.5, fill_color=SALT_GOLD, fill_opacity=0.22).move_to(eq_pt)
        vdrop = DashedLine(eq_pt + DOWN * 0.18, P.pt(P_BASE, 0.0), color=TEXT, stroke_width=2.2, dash_length=0.10).set_opacity(0.65)
        self.play(Create(vdrop), FadeIn(ring, scale=1.5), run_time=0.9)

        # "Only at that crossing does salt out equal salt in": label + clear equal balanced GOLD arrows
        self.at("only at that crossing")
        cr_lbl = T("out = in", size=24, color=SALT_GOLD).move_to(P.pt(94.8, 208.0))
        self.play(FadeIn(cr_lbl, shift=UP * 0.08), run_time=0.65)

        self.at("equal salt in")
        arr_in = Arrow(eq_pt + LEFT * 0.28 + DOWN * 0.24, eq_pt + LEFT * 0.28 + UP * 0.24, color=SALT_GOLD,
                       stroke_width=4.2, buff=0.0, max_tip_length_to_length_ratio=0.35)
        arr_out = Arrow(eq_pt + RIGHT * 0.28 + UP * 0.24, eq_pt + RIGHT * 0.28 + DOWN * 0.24, color=SALT_GOLD,
                        stroke_width=4.2, buff=0.0, max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(arr_in), GrowArrow(arr_out), run_time=0.7)
        self.finish()


# ===========================================================================
# SCENE 12: DRAIN (13.375 s)
# ===========================================================================
class S12Drain(SpokenScene):
    def construct(self):
        p_tr = ValueTracker(P_CLOSED)
        day_tr = ValueTracker(0.0)

        world = CirculationWorld(
            pressure=P_CLOSED, clamp=1.0, vagal=1.0, symp=-1.0, volume=0.92,
            kidney=True, salt_in=1.0, salt_out_from_pressure=True, show_wire_labels=False,
        )
        # Keep reflex status labels outside world so fading them out never suspends world's updater
        wire_labels = VGroup(
            T("vagal: up", size=24, color=PURPLE).move_to([-4.95, -3.22, 0.0]),
            T("sympathetic: down", size=24, color=ORANGE).move_to([-1.75, -3.22, 0.0]),
        )
        g_tag = T("Guyton's framework", size=24, color=SALT_GOLD).move_to([-5.05, 3.38, 0.0])

        # Couple world pressure, volume, and reflex easing directly to p_tr!
        def sync_drain(m, dt):
            pv = p_tr.get_value()
            world.pressure.set_value(pv)
            frac_err = float(np.clip((pv - P_BASE) / ERROR_SS, 0.0, 1.0))
            world.vagal.set_value(frac_err)
            world.symp.set_value(-frac_err)
            # Volume shrinks smoothly from 0.92 (at 106.7) down to 0.60 (at 100)
            world.volume.set_value(0.60 + 0.32 * frac_err)

        world.add_updater(sync_drain)

        P, tag, clock, k_grp, in_grp, cr_grp, marker = build_renal_base(
            p_tr, show_kidney_line=True, show_intake=True, show_crossing=True
        )

        # Live vertical shaded GOLD loss gap between kidney line and salt-in line at x = p_tr
        def mk_gap():
            pv = p_tr.get_value()
            ex = renal_excretion(pv)
            if abs(ex - SALT_INTAKE) < 3.0:
                return VGroup()
            p_in = P.pt(pv, SALT_INTAKE)
            p_ex = P.pt(pv, ex)
            h = abs(p_ex[1] - p_in[1])
            bar = Rectangle(
                width=0.22, height=max(0.04, h),
                stroke_color=SALT_GOLD, stroke_width=2.5,
                fill_color=SALT_GOLD, fill_opacity=0.45,
            ).move_to([p_in[0], 0.5 * (p_in[1] + p_ex[1]), 0.0])
            return bar

        gap_bar = always_redraw(mk_gap)

        # Live loss readout placed cleanly in open space right of the bar (constant 2-line format, size 24, zero overlaps!)
        def mk_loss_readout():
            pv = p_tr.get_value()
            loss = max(0.0, daily_loss(pv))
            txt = "salt lost\nper day"
            lbl = T(txt, size=24, color=SALT_GOLD, line_spacing=0.85).move_to(P.pt(118.2, 200.0))
            p_mid = P.pt(pv, 0.5 * (SALT_INTAKE + renal_excretion(pv)))
            ln = Line(p_mid + RIGHT * 0.14, lbl.get_left() + LEFT * 0.10, color=SALT_GOLD, stroke_width=2.2)
            return VGroup(ln, lbl)

        loss_readout = always_redraw(mk_loss_readout)

        # Live pressure & day counters in top right band (completely clear of plot y-label)
        day_lbl = always_redraw(lambda: M(f"day {int(round(day_tr.get_value()))}", size=26, color=SALT_GOLD).move_to([2.45, 3.28, 0.0]))
        p_now_num = always_redraw(lambda: M(f"MAP {p_tr.get_value():.1f}", size=26, color=BRIGHT_WHITE).move_to([4.85, 3.28, 0.0]))

        self.add(world, wire_labels, g_tag, P, tag, clock, k_grp, in_grp, cr_grp, marker)

        # "loses salt and water every day": reveal shaded gold gap ("lose 67 per day") & counters
        self.at("loses salt")
        self.play(FadeIn(gap_bar), FadeIn(loss_readout), FadeIn(day_lbl), FadeIn(p_now_num), run_time=0.85)

        # "Volume shrinks, less blood returns, and pressure falls": cleanly remove reflex-up/down labels as reflex eases, step 106.7 -> 103
        self.at("volume shrinks")
        self.play(
            FadeOut(wire_labels, run_time=0.45),
            p_tr.animate.set_value(103.0),
            day_tr.animate.set_value(2.0),
            Rotate(clock.min_hand, angle=-TAU * 2, about_point=clock.rim.get_center()),
            run_time=2.6,
            rate_func=smooth,
        )

        # "Lower pressure means less excretion, so each day's loss shrinks": step 103 -> 101 ("lose 10")
        self.at("lower pressure")
        self.play(
            p_tr.animate.set_value(101.0),
            day_tr.animate.set_value(4.0),
            Rotate(clock.min_hand, angle=-TAU * 2, about_point=clock.rim.get_center()),
            run_time=2.8,
            rate_func=smooth,
        )
        self.finish()


# ===========================================================================
# SCENE 13: NONE LEFT (10.775 s)
# ===========================================================================
class S13NoneLeft(SpokenScene):
    def construct(self):
        p_tr = ValueTracker(101.0)
        day_tr = ValueTracker(4.0)

        world = CirculationWorld(
            pressure=101.0, clamp=1.0, vagal=0.15, symp=-0.15, volume=0.65,
            kidney=True, salt_in=1.0, salt_out_from_pressure=True, show_wire_labels=False,
        )
        g_tag = T("Guyton's framework", size=24, color=SALT_GOLD).move_to([-5.05, 3.38, 0.0])

        def sync_final(m, dt):
            pv = p_tr.get_value()
            world.pressure.set_value(pv)
            frac_err = float(np.clip((pv - P_BASE) / ERROR_SS, 0.0, 1.0))
            world.vagal.set_value(frac_err)
            world.symp.set_value(-frac_err)
            world.volume.set_value(0.58 + 0.34 * frac_err)

        world.add_updater(sync_final)

        P, tag, clock, k_grp, in_grp, cr_grp, marker = build_renal_base(
            p_tr, show_kidney_line=True, show_intake=True, show_crossing=True
        )

        def mk_gap():
            pv = p_tr.get_value()
            ex = renal_excretion(pv)
            if abs(ex - SALT_INTAKE) < 1.5:
                return VGroup()
            p_in = P.pt(pv, SALT_INTAKE)
            p_ex = P.pt(pv, ex)
            return Rectangle(
                width=0.20, height=max(0.03, abs(p_ex[1] - p_in[1])),
                stroke_color=SALT_GOLD, stroke_width=2.5, fill_color=SALT_GOLD, fill_opacity=0.45,
            ).move_to([p_in[0], 0.5 * (p_in[1] + p_ex[1]), 0.0])

        gap_bar = always_redraw(mk_gap)
        loss_lbl = T("salt lost", size=24, color=SALT_GOLD).move_to(P.pt(118.2, 200.0))
        bal_lbl = T("balance", size=26, color=SALT_GOLD).move_to(P.pt(117.5, 200.0))

        day_lbl = always_redraw(lambda: M(f"day {int(round(day_tr.get_value()))}", size=26, color=SALT_GOLD).move_to([2.45, 3.28, 0.0]))
        p_now_num = always_redraw(lambda: M(f"MAP {p_tr.get_value():.1f}", size=26, color=BRIGHT_WHITE).move_to([4.85, 3.28, 0.0]))

        self.add(world, g_tag, P, tag, clock, k_grp, in_grp, cr_grp, gap_bar, marker, loss_lbl, day_lbl, p_now_num)

        # "stops only at the crossing": slide 101 -> 100, gap closes, swap to 'balance'
        self.at("stops only at")
        self.play(
            p_tr.animate.set_value(P_BASE),
            day_tr.animate.set_value(6.0),
            Rotate(clock.min_hand, angle=-TAU * 2, about_point=clock.rim.get_center()),
            swap(loss_lbl, bal_lbl, run_time=1.0),
            run_time=1.35,
            rate_func=smooth,
        )

        # "The squeeze is still on": pulse RED clamp emphatically
        self.at("squeeze is still on")
        self.play(Indicate(world.clamp_group, color=CLAMP_RED, scale_factor=1.24), run_time=0.95)

        # "so the heart now pumps less": highlight heart pumping smaller puffs at resting rate
        self.at("heart now pumps less")
        self.play(Indicate(world.lbl_heart, color=BLOOD_BLUE, scale_factor=1.16), run_time=0.95)

        # "The reflex left an error. The kidney leaves none."
        self.at("reflex left an error")
        err_w = ValueTracker(ERROR_SS)

        def mk_err_ghost():
            ew = err_w.get_value()
            if ew < 0.15:
                return VGroup()
            p0 = P.pt(P_BASE, 72.0)
            p1 = P.pt(P_BASE + ew, 72.0)
            ln = Line(p0, p1, color=BRIGHT_WHITE, stroke_width=5.0)
            t0 = Line(p0 + DOWN * 0.10, p0 + UP * 0.10, color=BRIGHT_WHITE, stroke_width=3.5)
            t1 = Line(p1 + DOWN * 0.10, p1 + UP * 0.10, color=BRIGHT_WHITE, stroke_width=3.5)
            lbl = T(f"left: {ew:.1f}", size=24, color=BRIGHT_WHITE).next_to(t1, RIGHT, buff=0.16)
            return VGroup(ln, t0, t1, lbl)

        err_ghost = always_redraw(mk_err_ghost)
        self.add(err_ghost)
        self.play(FadeIn(err_ghost), run_time=0.45)

        self.at("kidney leaves none")
        self.play(err_w.animate.set_value(0.0), run_time=0.95, rate_func=smooth)
        self.remove(err_ghost)
        self.finish()


# ===========================================================================
# SCENE 14: FINAL SAY / INFINITE GAIN (11.675 s)
# ===========================================================================
class S14FinalSay(SpokenScene):
    def construct(self):
        p_tr = ValueTracker(P_BASE)
        day_tr = ValueTracker(0.0)

        world = CirculationWorld(
            pressure=P_BASE, clamp=1.0, vagal=0.0, symp=0.0, volume=0.58,
            kidney=True, salt_in=1.0, salt_out_from_pressure=True, show_wire_labels=False,
        )
        g_tag = T("Guyton's framework", size=24, color=SALT_GOLD).move_to([-5.05, 3.38, 0.0])

        def sync_demo(m, dt):
            pv = p_tr.get_value()
            world.pressure.set_value(pv)
            # Volume responds visually to excess drain (pv > 100) or retention (pv < 100)
            world.volume.set_value(float(np.clip(0.58 - 0.015 * (pv - P_BASE), 0.48, 0.78)))

        world.add_updater(sync_demo)

        P, tag, clock, k_grp, in_grp, cr_grp, marker = build_renal_base(
            p_tr, show_kidney_line=True, show_intake=True, show_crossing=True, tag_text="teaching lines · schematic"
        )

        # Shaded vertical imbalance bar (above intake = draining GOLD, below intake = retaining GOLD)
        def mk_gap():
            pv = p_tr.get_value()
            ex = renal_excretion(pv)
            if abs(ex - SALT_INTAKE) < 3.0:
                return VGroup()
            p_in = P.pt(pv, SALT_INTAKE)
            p_ex = P.pt(pv, ex)
            return Rectangle(
                width=0.22, height=max(0.04, abs(p_ex[1] - p_in[1])),
                stroke_color=SALT_GOLD, stroke_width=2.5, fill_color=SALT_GOLD, fill_opacity=0.45,
            ).move_to([p_in[0], 0.5 * (p_in[1] + p_ex[1]), 0.0])

        gap_bar = always_redraw(mk_gap)
        day_lbl = always_redraw(lambda: M(f"day {int(round(day_tr.get_value()))}", size=26, color=SALT_GOLD).move_to([1.65, 3.28, 0.0]))

        self.add(world, g_tag, P, tag, clock, k_grp, in_grp, cr_grp, gap_bar, marker, day_lbl)

        # Nudge RIGHT (+8 mmHg -> 108): salt drains until pressure slides back to 100
        self.at("keeps changing volume")
        self.play(p_tr.animate.set_value(108.0), run_time=0.65, rate_func=smooth)
        self.play(
            p_tr.animate.set_value(P_BASE),
            day_tr.animate.set_value(4.0),
            Rotate(clock.min_hand, angle=-TAU * 2, about_point=clock.rim.get_center()),
            run_time=2.5,
            rate_func=smooth,
        )

        # "Guyton called that an infinite gain" — cleanly in top band above plot, zero overlap with kidney line!
        self.at("guyton called")
        inf_lbl = T("infinite gain (Guyton)", size=24, color=SALT_GOLD).move_to([4.45, 3.28, 0.0])
        self.play(FadeIn(inf_lbl, shift=UP * 0.08), run_time=0.6)

        # Nudge LEFT (-7 mmHg -> 93): salt piles in (in > out) until pressure slides back to 100
        self.play(p_tr.animate.set_value(93.0), run_time=0.6, rate_func=smooth)
        self.at("it is slow", lead=0.4)
        self.play(
            p_tr.animate.set_value(P_BASE),
            day_tr.animate.set_value(8.0),
            Rotate(clock.min_hand, angle=-TAU * 2, about_point=clock.rim.get_center()),
            run_time=2.4,
            rate_func=smooth,
        )
        self.finish()


# ===========================================================================
# SCENE 15: CLOSE (10.075 s)
# ===========================================================================
class S15Close(SpokenScene):
    def construct(self):
        p_tr = ValueTracker(P_BASE)
        world = CirculationWorld(
            pressure=P_BASE, clamp=1.0, vagal=0.0, symp=0.0, volume=0.58,
            kidney=True, salt_in=1.0, salt_out_from_pressure=True, show_wire_labels=False,
        )
        g_tag = T("Guyton's framework", size=24, color=SALT_GOLD).move_to([-5.05, 3.38, 0.0])

        P, tag, clock, k_grp, in_grp, cr_grp, marker = build_renal_base(
            p_tr, show_kidney_line=True, show_intake=True, show_crossing=True, tag_text="teaching lines"
        )
        self.add(world, g_tag, P, tag, clock, k_grp, in_grp, cr_grp, marker)

        # "within seconds": pulse brainstem, sensors, wires; label 'seconds' clearly right of Guyton's tag
        self.at("within seconds")
        lbl_sec = T("seconds", size=26, color=CYAN).move_to([-1.85, 3.06, 0.0])
        self.play(
            Indicate(world.brainstem_box, color=CYAN, scale_factor=1.10),
            Indicate(world.sensor_group, color=CYAN, scale_factor=1.10),
            FadeIn(lbl_sec, shift=UP * 0.08),
            run_time=0.95,
        )

        # "over days": pulse kidney, green line, gold line, ring; label 'days' cleanly left of falling drops
        self.at("over days")
        lbl_days = T("days", size=26, color=KIDNEY_GREEN).move_to([-3.12, -1.16, 0.0])
        self.play(
            Indicate(world.kidney_bean, color=KIDNEY_GREEN, scale_factor=1.14),
            Indicate(k_grp[0], color=KIDNEY_GREEN, scale_factor=1.03),
            Indicate(in_grp[0], color=SALT_GOLD, scale_factor=1.03),
            Indicate(cr_grp[1], color=SALT_GOLD, scale_factor=1.22),
            FadeIn(lbl_days, shift=UP * 0.08),
            run_time=1.05,
        )

        # "helps set ... still argued": dashed CYAN arrow from brainstem toward kidney with '?' inside open dark space
        self.at("helps set")
        q_start = world.to_scene([-4.45, 1.98, 0.0])
        q_end = world.to_scene([-2.78, 0.42, 0.0])
        q_arrow = DashedLine(q_start, q_end, color=CYAN, stroke_width=4.0, dash_length=0.14)
        q_tip = Arrow(q_end - (q_end - q_start) * 0.16, q_end, color=CYAN, stroke_width=4.0, buff=0.0, max_tip_length_to_length_ratio=0.65)
        q_mark = T("?", size=32, color=CYAN, weight=BOLD).move_to([-3.32, 0.22, 0.0])
        open_lbl = T("open question", size=24, color=CYAN).move_to([-3.25, -3.22, 0.0])
        self.play(Create(q_arrow), FadeIn(q_tip), FadeIn(q_mark, scale=1.3), run_time=0.95)
        self.at("still argued")
        self.play(FadeIn(open_lbl, shift=UP * 0.08), run_time=0.65)
        self.finish()


# ===========================================================================
# SCENE 16: END CARD (silent 3.5 s — standard EndCard, no construct override)
# ===========================================================================
class S16End(EndCard):
    LINE = "A fast reflex shrinks pressure errors; slow salt balance sets the level."
