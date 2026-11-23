"""
Two Loops, One Ratio — Water, Sodium and Potassium Balance (STEMhop)

COLOUR MAP (one colour per concept, kept across every scene):
- WATER_BLUE  (#60C5F1): body water fill, tap water stream, osmotic water droplets, urine water
- GOLD_NA     (#F5C842): sodium ions (outside-cell dots, 5 dots per litre), solute numerator, sodium tags
- PURPLE_K    (#C084FC): potassium ions (inside-cell dots), intracellular compartment label
- TEXT        (#E8EAF0): plasma sodium gauge, ticks, needle, live readouts, cell membrane, brackets
- CYAN_OSMO   (#22D3EE): osmoreceptor neuron, action-potential spikes, thirst signal, water loop arrow
- GREEN_AVP   (#4ADE80): pituitary vasopressin hormone dots, V2 docking sites, aquaporin-2 vesicles and pores
- ORANGE_VOL  (#FB923C): sodium-loop arterial filling ring, kidney excretion valve, sodium loop arrow

ONE CARRIED WORLD:
Left/centre holds a to-scale rectangular body-water tank (width proportional to total litres, split by a
water-permeable dashed membrane into intracellular 'cells' with drifting potassium dots and extracellular
'outside cells' with drifting sodium dots, plus a tap above and an 'outside: XX.X L' readout below).
Far right holds a fixed vertical 'plasma sodium (mmol/L)' gauge (130 to 150) whose needle and digital
readout are driven by one ValueTracker from [Na+] = total_effective_solute / total_water. From s06 onward,
the tank shifts slightly right and down to accommodate the lamina terminalis osmoreceptor neuron (top left)
and the collecting duct (bottom right of the tank), which stay on screen through s14.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
- s00_hook: Tap pours 1 L (42->43 L, V_icf=28.67 L, V_ecf=14.33 L, [Na+]=5880/43=136.7), rewinds, then
  sweat spout drains 1 L at 50 mmol/L (42->41 L, V_ecf=13.43 L, [Na+]=5830/41=142.2); solute dots drift.
- s02_world: Tank pushes in to frame height; 42 L bracket spans full width, 14.0 L outside zone highlights,
  and intracellular K+ (90 dots) then extracellular Na+ (70 dots) brighten while drifting in thermal motion.
- s03_drink: Solute/water ratio builds; water droplets cross the dashed membrane bidirectionally; tap pours
  1 L into outside cells, droplets stream into cells, tank widens 42->43 L and membrane slides to 2/3-1/3.
- s04_drink_result: Fraction water term expands while solute stays constant; [Na+] needle and readout drop
  smoothly from 140 to 136.7 (5880/43); outside sliver grows from 14.0 to 14.33 L (+ about 0.3 L).
- s05_sweat: Rewinds to 42 L/140; schematic plasma (5 dots) vs sweat (2 dots) cups compare strength; spout
  drains 1 L with 2 Na+ dots, tank narrows 42->41 L (V_ecf 14.0->13.4 L), water shrinks more than solute,
  and gauge rises to 142.2 (5830/41), then eases back to 42 L/140.
- s06_sensor: Tank smoothly shifts into full-world layout; brain and osmoreceptor neuron appear; plasma
  concentrates toward 142, water droplets leave the neuron so its radius shrinks, and axon spikes accelerate.
- s07_vasopressin: Pituitary releases green vasopressin dots into extracellular fluid to dock on V2 sites
  on the collecting duct outer wall; green aquaporin-2 vesicles slide to the inner wall and open as pores;
  water droplets cross from urine back into blood and the urine stream thins.
- s08_thirst: Aquaporin-2 pores close into vesicles, urine stream widens and urine bar drops to 50 mOsm/kg;
  short of water, pores reopen, stream thins and bar rises to 1,000-1,200; thirst signal runs to tap which
  pours water and restores the gauge to 140.
- s09_idea: Water loop arrow traces gauge->neuron->tap & duct->tank; tap briefly adds water (needle dips
  and recovers) and duct briefly widens urine stream (needle rises and recovers) while water term glows.
- s10_predict: 5 new gold Na+ dots (+140 mmol) drop into fixed-width 14.0 L outside compartment, crowding
  solute and driving the gauge needle up toward 143.3 (6020/42) as the predict question appears.
- s12_answer: Water loop activates (neuron fires, duct pores open, tap pours); outside compartment widens
  by exactly 1 L (14.0->15.0 L) while cells stay fixed at 28.0 L (membrane stationary), solute density
  normalizes, and [Na+] = 6020/(28+V_ecf) settles smoothly back to 140.
- s13_sodium_loop: Orange arterial-filling ring pulses on outside compartment top; orange sodium-loop arrow
  connects to duct valve, which opens so 3 gold Na+ dots leave with isotonic water (15.0->14.4 L) while
  plasma [Na+] stays fixed at 140 throughout.
- s14_close: Water loop + gauge pulse (concentration), sodium loop + outside readout pulse (volume); needle
  drops to 132 (sparse Na+ dots) and outside compartment cycles narrow (11.0 L), medium (14.5 L), wide
  (16.2 L) at constant low concentration (132) before settling back to 15.0 L and 140.
"""

from bp_parts import *


def _left(self, phrase=None, lead=0.2, nth=0, floor=0.4):
    """Seconds from now until the next narrated cue (or the end of the narration): lets a narrated
    process unfold at the pace of the words instead of finishing early and standing still."""
    end = (self.t_of(phrase, nth) - lead) if phrase else (self.narration_s - 0.1)
    return max(floor, end - self.elapsed())


SpokenScene.left = _left

# ------------------------------------------------------------------ concept palette
WATER_BLUE = "#60C5F1"
GOLD_NA = "#F5C842"
PURPLE_K = "#C084FC"
CYAN_OSMO = "#22D3EE"
GREEN_AVP = "#4ADE80"
ORANGE_VOL = "#FB923C"
TANK_STROKE = "#94D6F5"
BRAIN_STROKE = "#94A3B8"

# ------------------------------------------------------------------ physiological constants & exact model
V_ICF_0 = 28.0
V_ECF_0 = 14.0
V_TOT_0 = V_ICF_0 + V_ECF_0        # 42.0 L
C_NA_0 = 140.0                      # mmol/L
S_ICF_0 = C_NA_0 * V_ICF_0          # 3920 mmol effective solute
S_ECF_0 = C_NA_0 * V_ECF_0          # 1960 mmol effective solute
S_TOT_0 = S_ICF_0 + S_ECF_0         # 5880 mmol


def eq_state(v_tot, s_ecf=S_ECF_0, s_icf=S_ICF_0):
    c = (s_icf + s_ecf) / v_tot
    return s_icf / c, s_ecf / c, c


DRINK_ICF, DRINK_ECF, DRINK_C = eq_state(43.0)                      # 28.667 L, 14.333 L, 136.744 mmol/L
SWEAT_ICF, SWEAT_ECF, SWEAT_C = eq_state(41.0, S_ECF_0 - 50.0)      # 27.568 L, 13.432 L, 142.195 mmol/L
SALT_PRE_C = (S_TOT_0 + 140.0) / 42.0                                # 143.333 mmol/L
SALT_POST_ICF, SALT_POST_ECF, SALT_POST_C = eq_state(43.0, S_ECF_0 + 140.0)  # 28.0 L, 15.0 L, 140.0 mmol/L

# Layout geometry modes
MODE_A = dict(x_left=-6.20, y_bot=-2.15, y_top=2.25, scale=0.165)
MODE_A_PUSH = dict(x_left=-6.20, y_bot=-2.25, y_top=2.45, scale=0.168)
MODE_B = dict(x_left=-4.20, y_bot=-2.45, y_top=1.65, scale=0.132)

# Gauge fixed coordinates (same across all scenes)
GAUGE_X = 5.60
GAUGE_Y0 = -2.30
GAUGE_Y1 = 2.10
GAUGE_C0 = 130.0
GAUGE_C1 = 150.0

# Collecting duct fixed coordinates (Mode B)
DUCT_X = 2.25
DUCT_W = 0.56          # outer width: x in [1.97, 2.53]
DUCT_WALL = 0.14       # blood-facing left wall thickness: [1.97, 2.11]
DUCT_Y1 = 0.55
DUCT_Y0 = -3.15

# Brain & neuron fixed coordinates (Mode B)
BRAIN_C = np.array([-5.30, 2.15, 0.0])
NEURON_C = np.array([-4.96, 2.18, 0.0])
PIT_C = np.array([-5.30, 1.32, 0.0])


def gauge_y(c):
    f = np.clip((c - GAUGE_C0) / (GAUGE_C1 - GAUGE_C0), 0.0, 1.0)
    return GAUGE_Y0 + f * (GAUGE_Y1 - GAUGE_Y0)


# ------------------------------------------------------------------ reusable world components
class BodyWaterWorld:
    """The carried world: to-scale body-water tank with thermal solute particles, tap, and sodium gauge."""

    def __init__(self, mode=MODE_A, v_icf=V_ICF_0, v_ecf=V_ECF_0, c_na=C_NA_0,
                 n_na_active=70, seed=7, two_line_outside=False,
                 readout_mode="live", ecf_readout_mode="live", show_tap=True,
                 highlight_140=True, needle_op=1.0):
        self.v_icf = ValueTracker(v_icf)
        self.v_ecf = ValueTracker(v_ecf)
        self.c_na = ValueTracker(c_na)
        self.needle_op = ValueTracker(needle_op)
        self.x_left_t = ValueTracker(mode["x_left"])
        self.y_bot_t = ValueTracker(mode["y_bot"])
        self.y_top_t = ValueTracker(mode["y_top"])
        self.scale_t = ValueTracker(mode["scale"])

        self.two_line_outside = two_line_outside
        self.readout_mode = readout_mode          # "live", "about", "again"
        self.ecf_readout_mode = ecf_readout_mode  # "live", "about", "hidden"
        self.na_boost = ValueTracker(1.0)
        self.k_boost = ValueTracker(1.0)
        self.ecf_glow = ValueTracker(0.0)
        self.icf_glow = ValueTracker(0.0)
        self.water_glow = ValueTracker(0.0)
        self.n_na_active = n_na_active

        # Seeded thermal particle positions in normalized compartment coordinates
        rng = np.random.default_rng(seed)
        self.n_k = 90
        self.n_na_max = 85
        self.k_u = rng.uniform(0.04, 0.96, self.n_k)
        self.k_v = rng.uniform(0.05, 0.95, self.n_k)
        ang_k = rng.uniform(0, TAU, self.n_k)
        spd_k = rng.uniform(0.055, 0.115, self.n_k)
        self.k_du = np.cos(ang_k) * spd_k * 0.6
        self.k_dv = np.sin(ang_k) * spd_k

        self.na_u = rng.uniform(0.06, 0.94, self.n_na_max)
        self.na_v = rng.uniform(0.05, 0.95, self.n_na_max)
        ang_na = rng.uniform(0, TAU, self.n_na_max)
        spd_na = rng.uniform(0.065, 0.135, self.n_na_max)
        self.na_du = np.cos(ang_na) * spd_na
        self.na_dv = np.sin(ang_na) * spd_na
        self._rng = np.random.default_rng(seed + 101)

        # Build dynamic tank layers
        self.tank_fill = always_redraw(self._mk_tank_fill)
        self.tank_border = always_redraw(self._mk_tank_border)
        self.membrane = always_redraw(self._mk_membrane)
        self.ecf_highlight = always_redraw(self._mk_ecf_highlight)
        self.comp_labels = always_redraw(self._mk_comp_labels)
        self.ecf_readout = always_redraw(self._mk_ecf_readout)

        # Particle dots
        self.k_dots = VGroup(*[Dot(radius=0.052, color=PURPLE_K, fill_opacity=0.92) for _ in range(self.n_k)])
        self.na_dots = VGroup(*[Dot(radius=0.056, color=GOLD_NA, fill_opacity=0.96) for _ in range(self.n_na_max)])
        self._place_particles()
        self.particles = VGroup(self.k_dots, self.na_dots)
        # thermal drift removed (the narration never calls for it); dots only follow the tank's changes
        self.particles.add_updater(lambda m, dt: self._place_particles())

        # Tap above right side of tank
        self.show_tap = show_tap
        self.highlight_140 = highlight_140
        self.tap = always_redraw(self._mk_tap)

        # Fixed plasma sodium gauge
        self.gauge_static = self._mk_gauge_static()
        self.gauge_needle = always_redraw(self._mk_gauge_needle)
        self.gauge_readout = always_redraw(self._mk_gauge_readout)

        # Master group (ordered back to front)
        self.group = VGroup(
            self.tank_fill,
            self.particles,
            self.tank_border,
            self.membrane,
            self.ecf_highlight,
            self.comp_labels,
            self.ecf_readout,
            self.tap,
            self.gauge_static,
            self.gauge_needle,
            self.gauge_readout,
        )

    # Geometry helpers
    def x_left(self):
        return self.x_left_t.get_value()

    def x_mem(self):
        return self.x_left_t.get_value() + self.v_icf.get_value() * self.scale_t.get_value()

    def x_right(self):
        return self.x_mem() + self.v_ecf.get_value() * self.scale_t.get_value()

    def y_bot(self):
        return self.y_bot_t.get_value()

    def y_top(self):
        return self.y_top_t.get_value()

    def _is_two_line(self):
        return self.two_line_outside or (self.scale_t.get_value() < 0.155)

    def y_dots_top(self):
        return self.y_top_t.get_value() - (0.88 if self._is_two_line() else 0.72)

    def tap_tip(self):
        return np.array([self.x_right() - 0.16, self.y_top() + 0.22, 0.0])

    # Builders
    def _mk_tank_fill(self):
        xl, xm, xr, yb, yt = self.x_left(), self.x_mem(), self.x_right(), self.y_bot(), self.y_top()
        wg = float(np.clip(self.water_glow.get_value(), 0.0, 1.0))
        ig = float(np.clip(self.icf_glow.get_value(), 0.0, 1.0))
        eg = float(np.clip(self.ecf_glow.get_value(), 0.0, 1.0))
        r = Rectangle(width=max(0.2, xr - xl), height=max(0.2, yt - yb),
                      fill_color=WATER_BLUE, fill_opacity=0.25 + 0.08 * wg,
                      stroke_color=WATER_BLUE, stroke_width=6.0 * wg, stroke_opacity=wg)
        r.move_to([(xl + xr) / 2, (yb + yt) / 2, 0])
        g = VGroup(r)
        if ig > 0.02:
            ir = Rectangle(width=max(0.1, xm - xl), height=max(0.2, yt - yb),
                           fill_color=PURPLE_K, fill_opacity=0.24 * ig,
                           stroke_color=PURPLE_K, stroke_width=4.5 * ig)
            ir.move_to([(xl + xm) / 2, (yb + yt) / 2, 0])
            g.add(ir)
        if eg > 0.02:
            er = Rectangle(width=max(0.1, xr - xm), height=max(0.2, yt - yb),
                           fill_color=GOLD_NA, fill_opacity=0.22 * eg, stroke_width=0)
            er.move_to([(xm + xr) / 2, (yb + yt) / 2, 0])
            g.add(er)
        return g

    def _mk_tank_border(self):
        xl, xr, yb, yt = self.x_left(), self.x_right(), self.y_bot(), self.y_top()
        g = VGroup(
            Line([xl, yb, 0], [xr, yb, 0]),
            Line([xl, yt, 0], [xr, yt, 0]),
            Line([xl, yb, 0], [xl, yt, 0]),
            Line([xr, yb, 0], [xr, yt, 0]),
        )
        g.set_stroke(TANK_STROKE, width=3.5)
        return g

    def _mk_membrane(self):
        xm, yb, yt = self.x_mem(), self.y_bot(), self.y_top()
        return DashedLine([xm, yb, 0], [xm, yt, 0], color=TEXT, stroke_width=3.5, dash_length=0.18)

    def _mk_ecf_highlight(self):
        op = self.ecf_glow.get_value()
        if op <= 0.02:
            return VGroup()
        xm, xr, yb, yt = self.x_mem(), self.x_right(), self.y_bot(), self.y_top()
        g = VGroup(
            Line([xm, yb, 0], [xr, yb, 0]),
            Line([xm, yt, 0], [xr, yt, 0]),
            Line([xr, yb, 0], [xr, yt, 0]),
        )
        g.set_stroke(GOLD_NA, width=6.0, opacity=op)
        return g

    def _mk_comp_labels(self):
        xl, xm, xr, yt = self.x_left(), self.x_mem(), self.x_right(), self.y_top()
        two = self._is_two_line()
        l_cells = T("cells", 24 if two else 26, PURPLE_K)
        l_cells.move_to([(xl + xm) / 2, yt - 0.34, 0])
        if two:
            l_out = T("outside\ncells", 22, GOLD_NA, line_spacing=0.82)
            # Keep well clear of both membrane and tap stream (xr - 0.16)
            cx = min(xm + 0.58, xr - 0.36 - l_out.width / 2)
            cx = max(cx, xm + l_out.width / 2 + 0.14)
            l_out.move_to([cx, yt - 0.48, 0])
        else:
            l_out = T("outside cells", 22, GOLD_NA)
            # Fits cleanly inside 41 L outside width (2.21) with >= 0.14 left and >= 0.38 right margin
            cx = xm + l_out.width / 2 + 0.16
            if cx + l_out.width / 2 > xr - 0.34:
                cx = max(xm + l_out.width / 2 + 0.12, xr - 0.34 - l_out.width / 2)
            l_out.move_to([cx, yt - 0.34, 0])
        return VGroup(l_cells, l_out)

    def _mk_ecf_readout(self):
        if self.ecf_readout_mode == "hidden":
            return VGroup()
        xm, xr, yb = self.x_mem(), self.x_right(), self.y_bot()
        v = self.v_ecf.get_value()
        if abs(v - 14.0) > 0.05:
            return VGroup()          # only the narrated 14 litres is ever printed
        prefix = "outside: "
        two = self._is_two_line()
        txt = M(f"{prefix}14 L", 24 if two else 25, TEXT)
        cx = (xm + xr) / 2
        if two:
            # Keep strictly clear of collecting duct left wall (x = 1.87)
            max_right = DUCT_X - DUCT_W / 2 - 0.18
            if cx + txt.width / 2 > max_right:
                cx = max_right - txt.width / 2
            y_pos = yb - 0.42
        else:
            if cx + txt.width / 2 > xr + 0.65:
                cx = xr + 0.65 - txt.width / 2
            y_pos = yb - 0.36
        txt.move_to([cx, y_pos, 0])
        return txt

    def _mk_tap(self):
        if not self.show_tap:
            return VGroup()
        tip = self.tap_tip()
        neck_top = tip + UP * 0.44
        pipe_right = neck_top + RIGHT * 0.44
        return VGroup(
            Line(pipe_right, neck_top, color=TEXT, stroke_width=6),
            Line(neck_top, tip, color=TEXT, stroke_width=6),
            Line(tip + LEFT * 0.09, tip + RIGHT * 0.09, color=TEXT, stroke_width=5),
            Line(neck_top + UP * 0.13 + LEFT * 0.15, neck_top + UP * 0.13 + RIGHT * 0.15,
                 color=WATER_BLUE, stroke_width=5),
            Line(neck_top, neck_top + UP * 0.13, color=TEXT, stroke_width=4),
        )

    def _mk_gauge_static(self):
        g = VGroup()
        spine = Line([GAUGE_X, GAUGE_Y0, 0], [GAUGE_X, GAUGE_Y1, 0], color=TEXT, stroke_width=4)
        track = Rectangle(
            width=0.16, height=GAUGE_Y1 - GAUGE_Y0,
            color=TEXT, stroke_width=1.5, stroke_opacity=0.35,
            fill_color=TEXT, fill_opacity=0.05,
        ).move_to([GAUGE_X + 0.08, (GAUGE_Y0 + GAUGE_Y1) / 2, 0])
        g.add(track, spine)
        if self.highlight_140:
            y140 = gauge_y(140.0)
            g.add(Line([GAUGE_X - 0.18, y140, 0], [GAUGE_X + 0.18, y140, 0], color=CYAN_OSMO, stroke_width=3.5))
        for val in (130, 135, 140, 145, 150):
            yv = gauge_y(val)
            g.add(Line([GAUGE_X - 0.16, yv, 0], [GAUGE_X, yv, 0], color=TEXT, stroke_width=3))
            lbl = M(str(val), 22, TEXT)
            lbl.move_to([GAUGE_X - 0.24 - lbl.width / 2, yv, 0])
            g.add(lbl)
        head = T("plasma sodium", 26, TEXT).move_to([GAUGE_X - 0.05, 2.98, 0])
        unit = T("(mmol/L)", 22, TEXT).move_to([GAUGE_X - 0.05, 2.58, 0])
        g.add(head, unit)
        return g

    def _mk_gauge_needle(self):
        op = float(np.clip(self.needle_op.get_value(), 0.0, 1.0))
        if op <= 0.02:
            return VGroup()
        c = self.c_na.get_value()
        yc = gauge_y(c)
        col_h = max(0.04, yc - GAUGE_Y0)
        col = Rectangle(
            width=0.14, height=col_h,
            fill_color=TEXT, fill_opacity=0.35 * op, stroke_width=0,
        ).move_to([GAUGE_X + 0.08, GAUGE_Y0 + col_h / 2, 0])
        tri = Polygon(
            [GAUGE_X + 0.14, yc, 0],
            [GAUGE_X + 0.50, yc + 0.16, 0],
            [GAUGE_X + 0.50, yc - 0.16, 0],
            color=TEXT, fill_color=TEXT, fill_opacity=op, stroke_width=1.5, stroke_opacity=op,
        )
        bar = Line([GAUGE_X - 0.12, yc, 0], [GAUGE_X + 0.18, yc, 0],
                   color=TEXT, stroke_width=5.0, stroke_opacity=op)
        return VGroup(col, bar, tri)

    def _mk_gauge_readout(self):
        c = self.c_na.get_value()
        val_i = int(round(c))
        if self.readout_mode == "hidden":
            return VGroup()          # the predict question: the answer must not be shown early
        # only numbers the narration gives (137, 140, 142) are ever printed; in between, no number
        if min(abs(c - n) for n in (137.0, 140.0, 142.0)) > 0.6:
            return VGroup()
        if self.readout_mode == "about" and abs(c - 140.0) >= 0.8:
            s = f"about {val_i}"
        elif self.readout_mode == "again":
            s = f"{val_i} again"
        else:
            s = f"{val_i} mmol/L"
        return M(s, 25, TEXT).move_to([GAUGE_X - 0.05, -2.78, 0])

    # Particle kinematics
    def _place_particles(self):
        xl, xm, xr = self.x_left(), self.x_mem(), self.x_right()
        yb, yt = self.y_bot() + 0.14, self.y_dots_top()
        kx0, kx1 = xl + 0.14, xm - 0.14
        nx0, nx1 = xm + 0.14, xr - 0.14
        kb = self.k_boost.get_value()
        nb = self.na_boost.get_value()
        for i, d in enumerate(self.k_dots):
            px = kx0 + self.k_u[i] * max(0.1, kx1 - kx0)
            py = yb + self.k_v[i] * max(0.1, yt - yb)
            d.move_to([px, py, 0])
            d.set_width(0.104 * kb)
        for i, d in enumerate(self.na_dots):
            if i < self.n_na_active:
                px = nx0 + self.na_u[i] * max(0.1, nx1 - nx0)
                py = yb + self.na_v[i] * max(0.1, yt - yb)
                d.move_to([px, py, 0])
                d.set_width(0.112 * nb)
                d.set_fill(opacity=0.96)
            else:
                d.move_to([nx0 + 0.5 * (nx1 - nx0), yb + 0.5 * (yt - yb), 0])
                d.set_fill(opacity=0.0)

    def _step_particles(self, mob, dt):
        dt = min(dt, 0.08)
        if dt <= 0:
            return
        self.k_du += self._rng.normal(0.0, 0.08 * dt, self.n_k)
        self.k_dv += self._rng.normal(0.0, 0.12 * dt, self.n_k)
        self.k_du = np.clip(self.k_du, -0.09, 0.09)
        self.k_dv = np.clip(self.k_dv, -0.15, 0.15)
        self.k_u += self.k_du * dt
        self.k_v += self.k_dv * dt
        hit_ku = (self.k_u < 0.03) | (self.k_u > 0.97)
        hit_kv = (self.k_v < 0.03) | (self.k_v > 0.97)
        self.k_du[hit_ku] *= -1
        self.k_dv[hit_kv] *= -1
        self.k_u = np.clip(self.k_u, 0.03, 0.97)
        self.k_v = np.clip(self.k_v, 0.03, 0.97)

        self.na_du += self._rng.normal(0.0, 0.12 * dt, self.n_na_max)
        self.na_dv += self._rng.normal(0.0, 0.12 * dt, self.n_na_max)
        self.na_du = np.clip(self.na_du, -0.16, 0.16)
        self.na_dv = np.clip(self.na_dv, -0.15, 0.15)
        self.na_u += self.na_du * dt
        self.na_v += self.na_dv * dt
        hit_nu = (self.na_u < 0.04) | (self.na_u > 0.96)
        hit_nv = (self.na_v < 0.03) | (self.na_v > 0.97)
        self.na_du[hit_nu] *= -1
        self.na_dv[hit_nv] *= -1
        self.na_u = np.clip(self.na_u, 0.04, 0.96)
        self.na_v = np.clip(self.na_v, 0.03, 0.97)
        self._place_particles()


# ------------------------------------------------------------------ shared scene helpers
def make_needle_ring(c_val=140.0):
    """Cyan highlight ring centered on the needle pointer (strictly right of gauge ticks)."""
    return Circle(radius=0.30, color=CYAN_OSMO, stroke_width=4.5).move_to([GAUGE_X + 0.34, gauge_y(c_val), 0])


def make_start_ref_140():
    """Visibly distinct 140 starting reference marker (hollow outline + dashed line + 'start: 140')."""
    y140 = gauge_y(140.0)
    dash = DashedLine([GAUGE_X - 0.18, y140, 0], [GAUGE_X + 0.50, y140, 0],
                      color=TEXT, stroke_width=2.5, dash_length=0.08).set_stroke(opacity=0.75)
    ghost_tri = Polygon(
        [GAUGE_X + 0.14, y140, 0],
        [GAUGE_X + 0.50, y140 + 0.16, 0],
        [GAUGE_X + 0.50, y140 - 0.16, 0],
        color=TEXT, fill_opacity=0.0, stroke_width=2.2, stroke_opacity=0.75,
    )
    lbl = M("start: 140", 24, TEXT).move_to([GAUGE_X - 0.05, -3.26, 0])
    return VGroup(dash, ghost_tri, lbl)


def make_sweat_spout(world):
    """Spout attached to the right wall of the tank (for s00_hook, s01_title, s05_sweat)."""
    def mk():
        xr = world.x_right()
        y0 = -0.65
        p0 = np.array([xr, y0, 0.0])
        p1 = np.array([xr + 0.55, y0, 0.0])
        p2 = np.array([xr + 0.55, y0 - 0.35, 0.0])
        pipe = VGroup(
            Line(p0, p1, color=TEXT, stroke_width=6),
            Line(p1, p2, color=TEXT, stroke_width=6),
            Line(p2 + LEFT * 0.09, p2 + RIGHT * 0.09, color=TEXT, stroke_width=5),
        )
        lbl = T("sweat", 24, TEXT).move_to([xr + 0.58, y0 + 0.32, 0])
        return VGroup(pipe, lbl)
    return always_redraw(mk)


def make_tap_stream(world, active_tracker):
    """Vertical pale blue water stream pouring cleanly from tap tip into tank, clear of labels."""
    phase = ValueTracker(0.0)

    def _tick(m, dt):
        if active_tracker.get_value() > 0.02:
            phase.set_value((phase.get_value() + 1.4 * min(dt, 0.08)) % 1.0)

    def mk():
        a = active_tracker.get_value()
        if a <= 0.02:
            return VGroup()
        tip = world.tap_tip()
        y_end = world.y_top() - 0.85 * a
        stream = Line(tip, [tip[0], y_end, 0], color=WATER_BLUE, stroke_width=9 * a, stroke_opacity=0.88)
        g = VGroup(stream)
        ph = phase.get_value()
        for i in range(3):
            f = (ph + i / 3.0) % 1.0
            dy = tip[1] + f * (y_end - tip[1])
            g.add(Dot([tip[0], dy, 0], radius=0.072 * min(1.0, a), color=WATER_BLUE))
        return g

    mob = always_redraw(mk)
    mob.add_updater(_tick)
    return mob


def make_sweat_stream(world, active_tracker, phase_tracker):
    """Water stream + 2 gold sodium dots draining from the sweat spout."""
    def mk():
        a = active_tracker.get_value()
        if a <= 0.02:
            return VGroup()
        xr = world.x_right()
        sx = xr + 0.55
        y_start = -1.00
        y_end = -2.45
        stream = Line([sx, y_start, 0], [sx, y_start + (y_end - y_start) * a, 0],
                      color=WATER_BLUE, stroke_width=9 * a, stroke_opacity=0.90)
        g = VGroup(stream)
        ph = phase_tracker.get_value()
        for offset in (0.15, 0.62):
            f = (ph + offset) % 1.0
            dy = y_start + f * (y_end - y_start) * a
            g.add(Dot([sx, dy, 0], radius=0.072, color=GOLD_NA))
        return g
    return always_redraw(mk)


def make_ratio_fraction(center, solute_scale, water_scale, size=34, sol_op=None, wat_op=None, bar_op=None):
    """Live 'solute / water' fraction whose numerator and denominator scale independently from trackers."""
    def mk():
        sc_s = solute_scale.get_value()
        sc_w = water_scale.get_value()
        op_s = float(np.clip(sol_op.get_value(), 0.0, 1.0)) if sol_op is not None else 1.0
        op_w = float(np.clip(wat_op.get_value(), 0.0, 1.0)) if wat_op is not None else 1.0
        op_b = float(np.clip(bar_op.get_value(), 0.0, 1.0)) if bar_op is not None else 1.0
        top = T("solute", size, GOLD_NA).scale(sc_s).set_opacity(op_s)
        bot = T("water", size, WATER_BLUE).scale(sc_w).set_opacity(op_w)
        bar_w = max(top.width, bot.width) + 0.34
        bar = Line(LEFT * bar_w / 2, RIGHT * bar_w / 2, color=TEXT, stroke_width=3.5, stroke_opacity=op_b)
        bar.move_to(center)
        top.next_to(bar, UP, buff=0.18)
        bot.next_to(bar, DOWN, buff=0.18)
        g = VGroup()
        if op_b > 0.02:
            g.add(bar)
        if op_s > 0.02:
            g.add(top)
        if op_w > 0.02:
            g.add(bot)
        return g
    return always_redraw(mk)


def make_total_bracket(world, label_fn):
    """White bracket spanning full tank width cleanly below the outside readout."""
    def mk():
        xl, xr, yb = world.x_left(), world.x_right(), world.y_bot()
        y_bar = yb - 0.84
        tick = 0.14
        br = VGroup(
            Line([xl, y_bar + tick, 0], [xl, y_bar, 0]),
            Line([xl, y_bar, 0], [xr, y_bar, 0]),
            Line([xr, y_bar, 0], [xr, y_bar + tick, 0]),
        ).set_stroke(TEXT, width=3)
        lbl = T(label_fn(), 25, TEXT).move_to([(xl + xr) / 2, y_bar - 0.32, 0])
        return VGroup(br, lbl)
    return always_redraw(mk)


def make_brain_neuron(neuron_r, spike_rate, show_pituitary=False):
    """Simple brain outline at top left with osmoreceptor neuron and optional pituitary node."""
    pts = [
        BRAIN_C + np.array([-0.82, -0.30, 0]),
        BRAIN_C + np.array([-0.86,  0.22, 0]),
        BRAIN_C + np.array([-0.50,  0.64, 0]),
        BRAIN_C + np.array([ 0.14,  0.70, 0]),
        BRAIN_C + np.array([ 0.68,  0.44, 0]),
        BRAIN_C + np.array([ 0.82, -0.05, 0]),
        BRAIN_C + np.array([ 0.52, -0.50, 0]),
        BRAIN_C + np.array([-0.20, -0.58, 0]),
    ]
    outline = VMobject(color=BRAIN_STROKE, stroke_width=3.0, fill_color=BRAIN_STROKE, fill_opacity=0.08)
    outline.set_points_smoothly([*pts, pts[0]])

    lbl = T("osmoreceptor\nneuron", 22, CYAN_OSMO, line_spacing=0.82)
    lbl.move_to([BRAIN_C[0] + 0.02, BRAIN_C[1] + 1.20, 0])

    neuron = always_redraw(lambda: Circle(
        radius=neuron_r.get_value(), color=CYAN_OSMO, stroke_width=3.5,
        fill_color=CYAN_OSMO, fill_opacity=0.28,
    ).move_to(NEURON_C))
    core = Dot(NEURON_C, radius=0.07, color=CYAN_OSMO)

    # Plasma sampling line routed cleanly over the tank top to 'outside cells'
    sample_pts = [
        np.array([-0.36, 1.65, 0.0]),
        np.array([-0.36, 1.74, 0.0]),
        np.array([-4.96, 1.74, 0.0]),
        NEURON_C + DOWN * 0.20,
    ]
    sample_line = VMobject(color=CYAN_OSMO, stroke_width=2.5)
    sample_line.set_points_as_corners(sample_pts)
    axon = Line(NEURON_C + DOWN * 0.26 + LEFT * 0.12, PIT_C + UP * 0.15, color=CYAN_OSMO, stroke_width=2.8)

    phase = ValueTracker(0.0)

    def _adv(m, dt):
        r = spike_rate.get_value()
        if r > 0.01:
            phase.set_value((phase.get_value() + r * dt) % 1.0)

    spikes = always_redraw(lambda: _mk_spikes(phase.get_value(), spike_rate.get_value(), show_pituitary, sample_line))
    spikes.add_updater(_adv)

    g = VGroup(outline, lbl, sample_line, axon, neuron, core, spikes)
    g.sample_line = sample_line
    g.axon = axon
    if show_pituitary:
        pit = Circle(radius=0.15, color=GREEN_AVP, stroke_width=3.0, fill_color=GREEN_AVP, fill_opacity=0.35).move_to(PIT_C)
        # Label cleanly to the LEFT of pituitary node: zero overlap with cyan line or green AVP dots
        pit_lbl = T("pituitary", 22, GREEN_AVP).next_to(pit, LEFT, buff=0.14)
        g.add(pit, pit_lbl)
        g.pit = pit
        g.pit_lbl = pit_lbl
    return g


def _mk_spikes(ph, rate, to_pituitary, sample_line=None):
    if rate <= 0.05:
        return VGroup()
    n = 4 if rate > 1.8 else 2
    g = VGroup()
    p0 = NEURON_C + DOWN * 0.28 + LEFT * 0.10
    p1 = PIT_C + UP * 0.14
    for i in range(n):
        f = (ph + i / n) % 1.0
        pos = p0 + f * (p1 - p0)
        g.add(Dot(pos, radius=0.085, color=CYAN_OSMO))
    return g


class CollectingDuct:
    """Vertical collecting duct at bottom right of the tank with V2 sites, aquaporin-2 pores, and urine flow."""

    def __init__(self, pore_open=0.0, show_v2=False, show_avp_stream=False, x_right_fn=None, reabsorb_boost=0.0):
        self.pore_open = ValueTracker(pore_open)
        self.v2_bound = ValueTracker(1.0 if show_v2 else 0.0)
        self.avp_flow = ValueTracker(1.0 if show_avp_stream else 0.0)
        self.urine_phase = ValueTracker(0.0)
        self.reabsorb_boost = ValueTracker(reabsorb_boost)
        self.x_right_fn = x_right_fn

        self.x_l_out = DUCT_X - DUCT_W / 2              # 1.97 (blood-facing wall)
        self.x_l_in = self.x_l_out + DUCT_WALL          # 2.11 (urine-facing apical membrane)
        self.x_r_in = DUCT_X + DUCT_W / 2 - 0.08        # 2.45
        self.x_r_out = DUCT_X + DUCT_W / 2              # 2.53
        self.pore_ys = [0.05, -0.58, -1.21, -1.84]

        self.walls = self._mk_walls()
        self.label = T("collecting\nduct", 22, TEXT, line_spacing=0.82).move_to([DUCT_X + 0.07, DUCT_Y1 + 0.44, 0])
        self.urine = always_redraw(self._mk_urine)
        self.v2_sites = always_redraw(self._mk_v2_sites)
        self.aqp2 = always_redraw(self._mk_aqp2)
        self.reabsorb = always_redraw(self._mk_reabsorb)
        self.avp_dots = always_redraw(self._mk_avp_dots)

        self.clock = VMobject()
        self.clock.add_updater(lambda m, dt: self.urine_phase.set_value((self.urine_phase.get_value() + 0.85 * min(dt, 0.08)) % 1.0))

        self.group = VGroup(
            self.clock, self.urine, self.walls, self.label,
            self.v2_sites, self.aqp2, self.reabsorb, self.avp_dots,
        )

    def _mk_walls(self):
        cell_fill = Rectangle(
            width=DUCT_WALL, height=DUCT_Y1 - DUCT_Y0,
            fill_color=TEXT, fill_opacity=0.10, stroke_width=0,
        ).move_to([(self.x_l_out + self.x_l_in) / 2, (DUCT_Y1 + DUCT_Y0) / 2, 0])
        lines = VGroup(
            Line([self.x_l_out, DUCT_Y1, 0], [self.x_l_out, DUCT_Y0, 0]),
            Line([self.x_l_in, DUCT_Y1, 0], [self.x_l_in, DUCT_Y0, 0]),
            Line([self.x_r_in, DUCT_Y1, 0], [self.x_r_in, DUCT_Y0, 0]),
        ).set_stroke(TEXT, width=3.0)
        return VGroup(cell_fill, lines)

    def _mk_urine(self):
        po = float(np.clip(self.pore_open.get_value(), 0.0, 1.0))
        cx = (self.x_l_in + self.x_r_in) / 2
        w_top = 0.32
        w_bot = 0.32 - 0.22 * po
        y_exit = DUCT_Y0 - 0.55
        poly = Polygon(
            [cx - w_top / 2, DUCT_Y1, 0],
            [cx + w_top / 2, DUCT_Y1, 0],
            [cx + w_bot / 2, DUCT_Y0, 0],
            [cx - w_bot / 2, DUCT_Y0, 0],
            fill_color=WATER_BLUE, fill_opacity=0.38 + 0.28 * (1 - po), stroke_width=0,
        )
        out_stream = Rectangle(
            width=max(0.06, w_bot), height=DUCT_Y0 - y_exit,
            fill_color=WATER_BLUE, fill_opacity=0.38 + 0.28 * (1 - po), stroke_width=0,
        ).move_to([cx, (DUCT_Y0 + y_exit) / 2, 0])
        ph = self.urine_phase.get_value()
        dashes = VGroup()
        for i in range(7):
            f = (ph + i / 7.0) % 1.0
            y = DUCT_Y1 - 0.12 - f * (DUCT_Y1 - y_exit - 0.24)
            dashes.add(Line([cx, y + 0.12, 0], [cx, y - 0.12, 0],
                            color=WATER_BLUE, stroke_width=5.0 - 2.5 * po))
        return VGroup(poly, out_stream, dashes)

    def _mk_v2_sites(self):
        b = self.v2_bound.get_value()
        g = VGroup()
        for y in self.pore_ys[:3]:
            notch = Line([self.x_l_out - 0.08, y, 0], [self.x_l_out, y, 0], color=TEXT, stroke_width=4.5)
            g.add(notch)
            if b > 0.05:
                g.add(Dot([self.x_l_out - 0.10, y, 0], radius=0.075 * min(1.0, b), color=GREEN_AVP))
        return g

    def _mk_aqp2(self):
        po = float(np.clip(self.pore_open.get_value(), 0.0, 1.0))
        g = VGroup()
        for y in self.pore_ys:
            if po < 0.55:
                f = po / 0.55
                vx = (self.x_l_out + 0.04) + f * (self.x_l_in - self.x_l_out - 0.07)
                g.add(Circle(radius=0.062, color=GREEN_AVP, stroke_width=3.0,
                             fill_color=GREEN_AVP, fill_opacity=0.45).move_to([vx, y, 0]))
            else:
                f = (po - 0.55) / 0.45
                g.add(Line([self.x_l_in - 0.08, y + 0.08 * f, 0], [self.x_l_in + 0.08, y + 0.08 * f, 0],
                           color=GREEN_AVP, stroke_width=5.0))
                g.add(Line([self.x_l_in - 0.08, y - 0.08 * f, 0], [self.x_l_in + 0.08, y - 0.08 * f, 0],
                           color=GREEN_AVP, stroke_width=5.0))
        return g

    def _mk_reabsorb(self):
        po = float(np.clip(self.pore_open.get_value(), 0.0, 1.0))
        if po < 0.65:
            return VGroup()
        ph = self.urine_phase.get_value()
        cx = (self.x_l_in + self.x_r_in) / 2
        x_end = (self.x_right_fn() - 0.15) if self.x_right_fn is not None else 1.15
        boost = float(np.clip(self.reabsorb_boost.get_value(), 0.0, 1.0))
        shifts = (0.0, 0.33, 0.67) if boost > 0.2 else (0.0, 0.5)
        rad = 0.068 * (1.0 + 0.35 * boost)
        g = VGroup()
        if boost > 0.2:
            for y in self.pore_ys:
                g.add(Arrow([self.x_l_out - 0.02, y, 0], [x_end + 0.02, y, 0],
                            buff=0.0, color=WATER_BLUE, stroke_width=2.5 * boost,
                            stroke_opacity=0.65 * boost, tip_length=0.11))
        for i, y in enumerate(self.pore_ys):
            for shift in shifts:
                f = (ph + i * 0.25 + shift) % 1.0
                px = cx - f * (cx - x_end)
                g.add(Dot([px, y, 0], radius=rad, color=WATER_BLUE))
        return g

    def _mk_avp_dots(self):
        fl = self.avp_flow.get_value()
        if fl <= 0.05:
            return VGroup()
        ph = self.urine_phase.get_value()
        g = VGroup()
        # Green hormone dots leave pituitary, travel beneath tank (never through cells!), enter
        # extracellular fluid ('outside cells'), and drift rightward to duct V2 sites.
        pts = [
            PIT_C + DOWN * 0.16,
            np.array([PIT_C[0], -2.62, 0.0]),
            np.array([0.40, -2.62, 0.0]),
            np.array([0.40, -1.85, 0.0]),
            np.array([self.x_l_out - 0.10, -0.58, 0.0]),
        ]
        segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
        tot = sum(segs)
        cum = np.cumsum([0.0] + segs) / tot
        for i in range(10):
            f = (ph * 0.65 + i / 10.0) % 1.0
            idx = int(np.searchsorted(cum, f, side="right")) - 1
            idx = max(0, min(len(segs) - 1, idx))
            t = (f - cum[idx]) / max(1e-6, cum[idx + 1] - cum[idx])
            p = pts[idx] + t * (pts[idx + 1] - pts[idx])
            g.add(Dot(p, radius=0.078 * min(1.0, fl), color=GREEN_AVP))
        return g


def make_thirst_arrow(world):
    """Cyan line from osmoreceptor neuron across top to the tap, labelled 'thirst'."""
    stroke_w = ValueTracker(3.2)
    progress = ValueTracker(1.0)

    def mk():
        prog = float(np.clip(progress.get_value(), 0.0, 1.0))
        if prog <= 0.01:
            return VGroup()
        tip = world.tap_tip()
        p0 = NEURON_C + RIGHT * 0.36 + UP * 0.12
        p1 = np.array([-3.75, 2.52, 0.0])
        p2 = np.array([tip[0] - 0.12, 2.52, 0.0])
        p3 = tip + UP * 0.56
        pts = [p0, p1, p2, p3]
        sw = stroke_w.get_value()
        segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(3)]
        tot = sum(segs)
        target_d = prog * tot
        drawn = [p0]
        acc = 0.0
        for i in range(3):
            if acc + segs[i] <= target_d:
                drawn.append(pts[i + 1])
                acc += segs[i]
            else:
                t = max(0.0, (target_d - acc) / max(1e-6, segs[i]))
                drawn.append(pts[i] + t * (pts[i + 1] - pts[i]))
                break
        path = VMobject(color=CYAN_OSMO, stroke_width=sw)
        path.set_points_as_corners(drawn)
        g = VGroup(path)
        if prog >= 0.88:
            arr = Arrow(p2 + LEFT * 0.12, p3, buff=0.0, color=CYAN_OSMO, stroke_width=sw, tip_length=0.14)
            g.add(arr)
        lbl = T("thirst", 22, CYAN_OSMO).move_to([-2.05, 2.74, 0]).set_opacity(min(1.0, prog * 1.4))
        g.add(lbl)
        return g

    mob = always_redraw(mk)
    mob.stroke_w = stroke_w
    mob.progress = progress
    return mob


def make_water_loop_arrows(world):
    """Cyan feedback loop arrow cleanly above 'thirst' and strictly left of 'plasma sodium'."""
    top_arr = CurvedArrow(
        np.array([3.92, 2.95, 0.0]),
        np.array([-4.05, 3.00, 0.0]),
        angle=0.10, color=CYAN_OSMO, stroke_width=3.5, tip_length=0.20,
    )
    lbl = T("water loop", 24, CYAN_OSMO).move_to([0.05, 3.52, 0])
    return VGroup(top_arr, lbl)


def make_sodium_loop(world, valve_open, valve_phase, ring_scale=None, loop_draw=None):
    """Orange arterial-filling ring cleanly above outside tank, arrow around duct to valve, and Na+ dots."""
    def mk_ring():
        cx = world.x_mem() + 0.48
        yt = world.y_top()
        rs = ring_scale.get_value() if ring_scale is not None else 1.0
        r = Circle(radius=0.17 * rs, color=ORANGE_VOL, stroke_width=4.5,
                   fill_color=ORANGE_VOL, fill_opacity=0.25).move_to([cx, yt + 0.16, 0])
        lbl = T("artery filling", 22, ORANGE_VOL).move_to([cx - 0.52, yt + 0.58, 0])
        return VGroup(r, lbl)

    ring = always_redraw(mk_ring)

    def mk_arrow():
        f_draw = float(np.clip(loop_draw.get_value(), 0.0, 1.0)) if loop_draw is not None else 1.0
        if f_draw <= 0.02:
            return VGroup()
        cx = world.x_mem() + 0.48
        yt = world.y_top()
        y_run = yt + 0.12   # passes cleanly below tap tip (yt + 0.22) and above tank top (yt)
        x_down = 3.06       # 0.53 right of duct right wall (2.53), 0.18 right of 'collecting duct' (2.88)
        p0 = np.array([cx + 0.18, y_run, 0.0])
        p1 = np.array([x_down, y_run, 0.0])
        p2 = np.array([x_down, -2.55, 0.0])
        p3 = np.array([DUCT_X + 0.30, -2.55, 0.0])
        pts = [p0, p1, p2, p3]
        segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(3)]
        tot = sum(segs)
        target_d = f_draw * tot
        drawn = [p0]
        acc = 0.0
        for i in range(3):
            if acc + segs[i] <= target_d:
                drawn.append(pts[i + 1])
                acc += segs[i]
            else:
                t = max(0.0, (target_d - acc) / max(1e-6, segs[i]))
                drawn.append(pts[i] + t * (pts[i + 1] - pts[i]))
                break
        path = VMobject(color=ORANGE_VOL, stroke_width=4.0)
        path.set_points_as_corners(drawn)
        g = VGroup(path)
        if f_draw >= 0.90:
            head = Arrow(p2, p3, buff=0.0, color=ORANGE_VOL, stroke_width=4.0, tip_length=0.15)
            g.add(head)
        if f_draw >= 0.45:
            op = min(1.0, (f_draw - 0.45) / 0.25)
            # Compact 4-line label (max 9 chars wide) centered cleanly between x_down (3.06) and gauge ticks (4.90)
            lbl = T("sodium\nloop:\nhormones,\nnerves", 22, ORANGE_VOL, line_spacing=0.80).set_opacity(op)
            lbl.move_to([3.96, -0.68, 0])
            g.add(lbl)
        return g

    loop_arrow = always_redraw(mk_arrow)

    def mk_valve():
        vo = valve_open.get_value()
        vy = -2.55
        gap = 0.04 + 0.14 * vo
        vl = Line([DUCT_X - 0.28, vy, 0], [DUCT_X - gap, vy, 0], color=ORANGE_VOL, stroke_width=6.5)
        vr = Line([DUCT_X + gap, vy, 0], [DUCT_X + 0.28, vy, 0], color=ORANGE_VOL, stroke_width=6.5)
        g = VGroup(vl, vr)
        if vo > 0.15:
            ph = valve_phase.get_value()
            for i in range(4):
                f = (ph + i / 4.0) % 1.0
                dy = vy - 0.10 - f * 0.95
                g.add(Dot([DUCT_X + ((i % 3) - 1) * 0.06, dy, 0], radius=0.072, color=GOLD_NA))
        return g

    valve = always_redraw(mk_valve)
    return VGroup(ring, loop_arrow, valve)


def make_membrane_droplets(world, active_tracker, direction_mode="both"):
    """Pale blue water droplets crossing the dashed membrane (bidirectional or right-to-left)."""
    phase = ValueTracker(0.0)

    def _tick(m, dt):
        if active_tracker.get_value() > 0.05:
            phase.set_value((phase.get_value() + 0.85 * min(dt, 0.08)) % 1.0)

    def mk():
        a = active_tracker.get_value()
        if a <= 0.05:
            return VGroup()
        xm = world.x_mem()
        yb, yt = world.y_bot() + 0.25, world.y_dots_top() - 0.15
        ys = np.linspace(yb, yt, 9)
        ph = phase.get_value()
        band = Rectangle(
            width=0.22, height=max(0.2, world.y_top() - world.y_bot()),
            fill_color=WATER_BLUE, fill_opacity=0.14 * min(1.0, a), stroke_width=0,
        ).move_to([xm, (world.y_bot() + world.y_top()) / 2, 0])
        g = VGroup(band)
        for i, y in enumerate(ys):
            f = (ph + (i * 0.19)) % 1.0
            sign = (1.0 if i % 2 == 0 else -1.0) if direction_mode == "both" else -1.0
            dx = sign * (-0.95 + 1.90 * f)
            g.add(Dot([xm + dx, y, 0], radius=0.078 * min(1.0, a), color=WATER_BLUE))
        return g

    mob = always_redraw(mk)
    mob.add_updater(_tick)
    return mob


# ================================================================== SCENES

class S00Hook(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_A, v_icf=V_ICF_0, v_ecf=V_ECF_0, c_na=C_NA_0, n_na_active=70)
        tap_on = ValueTracker(0.0)
        tap_stream = make_tap_stream(world, tap_on)
        cross_on = ValueTracker(0.0)
        cross_drops = make_membrane_droplets(world, cross_on, direction_mode="into_cells")
        sweat_on = ValueTracker(0.0)
        sweat_ph = ValueTracker(0.0)
        spout = make_sweat_spout(world)
        sweat_stream = make_sweat_stream(world, sweat_on, sweat_ph)

        self.add(world.group, tap_stream, cross_drops)

        # Drink 1 L of water
        self.at("drink a liter")
        self.play(tap_on.animate.set_value(1.0), cross_on.animate.set_value(1.0), run_time=0.4)
        self.play(
            world.v_icf.animate.set_value(DRINK_ICF),
            world.v_ecf.animate.set_value(DRINK_ECF),
            run_time=self.left("dips") - 0.35, rate_func=linear,
        )
        self.play(tap_on.animate.set_value(0.0), cross_on.animate.set_value(0.0), run_time=0.35)

        # Concentration dips to ~137
        self.at("dips")
        world.readout_mode = "about"
        self.play(world.c_na.animate.set_value(DRINK_C), run_time=self.left("no sodium left"), rate_func=linear)

        # No sodium left your body: gold dots pulse briefly, then rewind
        self.at("no sodium left")
        self.play(world.na_boost.animate.set_value(1.38), run_time=0.6)
        self.play(world.na_boost.animate.set_value(1.0), run_time=0.6)

        world.readout_mode = "live"
        self.play(
            world.v_icf.animate.set_value(V_ICF_0),
            world.v_ecf.animate.set_value(V_ECF_0),
            world.c_na.animate.set_value(C_NA_0),
            run_time=self.left("sweat out a liter"), rate_func=linear,
        )

        # Sweat out 1 L: fast enough that 'rises' lands right on cue (10.90 s)
        self.at("sweat out a liter")
        self.add(spout, sweat_stream)
        world.n_na_active = 68
        self.play(sweat_on.animate.set_value(1.0), run_time=0.22)
        self.play(
            sweat_ph.animate.set_value(1.2),
            world.v_icf.animate.set_value(SWEAT_ICF),
            world.v_ecf.animate.set_value(SWEAT_ECF),
            run_time=0.68, rate_func=linear,
        )

        self.at("rises")
        world.readout_mode = "about"
        self.play(
            sweat_ph.animate.set_value(2.8),
            world.c_na.animate.set_value(SWEAT_C),
            run_time=self.left("why") - 0.30, rate_func=linear,
        )
        self.play(sweat_on.animate.set_value(0.0), run_time=0.30)

        self.at("why")
        why = T("Why?", 44, TEXT, weight=BOLD).move_to([-2.4, 3.22, 0])
        self.play(FadeIn(why, shift=DOWN * 0.1), run_time=0.45)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_A, v_icf=SWEAT_ICF, v_ecf=SWEAT_ECF, c_na=SWEAT_C,
                               n_na_active=68, readout_mode="about")
        spout = make_sweat_spout(world)
        why = T("Why?", 44, TEXT, weight=BOLD).move_to([-2.4, 3.22, 0])
        # Centered over tank well left of tap pipe
        title = T("Two Loops, One Ratio", 42, TEXT, font=TITLE_FONT).move_to([-2.80, 3.30, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD_NA, stroke_width=3.5).next_to(title, DOWN, buff=0.12)

        self.add(world.group, spout, why)
        self.play(
            FadeOut(why, run_time=0.25),
            FadeOut(spout, run_time=0.25),
        )
        self.play(
            FadeIn(title, shift=UP * 0.1, run_time=0.30),
            GrowFromCenter(rule, run_time=0.30),
        )
        world.n_na_active = 70
        world.readout_mode = "live"
        self.play(
            world.v_icf.animate.set_value(V_ICF_0),
            world.v_ecf.animate.set_value(V_ECF_0),
            world.c_na.animate.set_value(C_NA_0),
            run_time=1.1, rate_func=linear,
        )
        self.play(FadeOut(title), FadeOut(rule), run_time=0.35)
        self.finish()


class S02World(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_A, v_icf=V_ICF_0, v_ecf=V_ECF_0, c_na=C_NA_0, n_na_active=70)
        self.add(world.group)

        self.play(
            world.y_bot_t.animate.set_value(MODE_A_PUSH["y_bot"]),
            world.y_top_t.animate.set_value(MODE_A_PUSH["y_top"]),
            world.scale_t.animate.set_value(MODE_A_PUSH["scale"]),
            run_time=self.left("42 liters"), rate_func=linear,
        )

        self.at("42 liters")
        bracket = make_total_bracket(world, lambda: "42 L water")
        t_42 = self.left("14 of them")
        self.play(FadeIn(bracket, shift=UP * 0.1), world.water_glow.animate.set_value(0.90), run_time=t_42 * 0.55)
        self.play(world.water_glow.animate.set_value(0.0), run_time=t_42 * 0.45)

        self.at("14 of them")
        t_14 = self.left("cells hold")
        self.play(world.ecf_glow.animate.set_value(1.0), run_time=min(1.1, t_14 * 0.45))
        self.play(world.ecf_glow.animate.set_value(0.0), run_time=max(0.4, t_14 - min(1.1, t_14 * 0.45)))

        self.at("cells hold")
        k_lbl = T("potassium holds", 28, PURPLE_K).move_to([(world.x_left() + world.x_mem()) / 2, world.y_top() + 0.36, 0])
        self.play(
            world.icf_glow.animate.set_value(1.0),
            world.k_boost.animate.set_value(1.45),
            FadeIn(k_lbl, shift=UP * 0.1),
            run_time=self.left("the fluid outside"),
        )

        self.at("the fluid outside")
        # Positioned well left of tap pipe
        na_lbl = T("sodium holds", 26, GOLD_NA).move_to([world.x_mem() + 0.65, world.y_top() + 0.36, 0])
        self.play(
            world.icf_glow.animate.set_value(0.0),
            world.k_boost.animate.set_value(1.0),
            world.ecf_glow.animate.set_value(1.0),
            world.na_boost.animate.set_value(1.45),
            FadeIn(na_lbl, shift=UP * 0.1),
            run_time=self.left() - 0.50,
        )

        self.play(
            world.ecf_glow.animate.set_value(0.0),
            world.na_boost.animate.set_value(1.0),
            FadeOut(k_lbl), FadeOut(na_lbl),
            run_time=0.45,
        )
        self.finish()


class S03Drink(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_A_PUSH, v_icf=V_ICF_0, v_ecf=V_ECF_0, c_na=C_NA_0, n_na_active=70)
        tot_litres = ValueTracker(42.0)
        bracket = make_total_bracket(world, lambda: f"{tot_litres.get_value():.0f} L water")
        tap_on = ValueTracker(0.0)
        tap_stream = make_tap_stream(world, tap_on)
        cross_both = ValueTracker(0.0)
        drops_both = make_membrane_droplets(world, cross_both, direction_mode="both")
        cross_in = ValueTracker(0.0)
        drops_in = make_membrane_droplets(world, cross_in, direction_mode="into_cells")

        sol_sc = ValueTracker(1.0)
        wat_sc = ValueTracker(1.0)
        sol_op = ValueTracker(0.0)
        wat_op = ValueTracker(0.0)
        bar_op = ValueTracker(0.0)
        frac = make_ratio_fraction(
            np.array([2.95, -0.75, 0.0]), sol_sc, wat_sc, size=34,
            sol_op=sol_op, wat_op=wat_op, bar_op=bar_op,
        )

        self.add(world.group, bracket, frac, tap_stream, drops_both, drops_in)

        # Highlight outside plasma + 140 mmol/L gauge needle right from the start
        ring = make_needle_ring(140.0)
        self.play(
            world.ecf_glow.animate.set_value(0.80),
            FadeIn(ring, scale=1.25),
            run_time=self.left("140 millimoles"),
        )
        self.at("140 millimoles")
        t_140 = self.left("a ratio")
        self.play(
            world.ecf_glow.animate.set_value(0.0),
            ring.animate.scale(1.15),
            run_time=t_140 * 0.55,
        )
        self.play(FadeOut(ring), run_time=t_140 * 0.45)

        # Build 'solute / water' fraction piece by piece tied to the body compartments
        self.at("a ratio")
        self.play(
            bar_op.animate.set_value(1.0),
            sol_op.animate.set_value(1.0),
            sol_sc.animate.set_value(1.18),
            world.na_boost.animate.set_value(1.38),
            world.ecf_glow.animate.set_value(0.75),
            run_time=self.left("over water"),
        )

        self.at("over water")
        t_wat = self.left("water crosses")
        self.play(
            sol_sc.animate.set_value(1.0),
            world.na_boost.animate.set_value(1.0),
            world.ecf_glow.animate.set_value(0.0),
            wat_op.animate.set_value(1.0),
            wat_sc.animate.set_value(1.18),
            world.water_glow.animate.set_value(0.85),
            run_time=t_wat * 0.60,
        )
        self.play(
            wat_sc.animate.set_value(1.0),
            world.water_glow.animate.set_value(0.0),
            run_time=t_wat * 0.40,
        )

        self.at("water crosses")
        self.play(cross_both.animate.set_value(1.0), run_time=0.35)
        self.wait(self.left("a liter you drink", floor=0.0) - 0.30)
        self.play(cross_both.animate.set_value(0.0), run_time=0.30)

        # Pour 1 L: focus cleanly on total body water (42 L -> 43 L); mark 140 as starting reference
        self.at("a liter you drink")
        world.ecf_readout_mode = "hidden"
        world.readout_mode = "hidden"
        ref_140 = make_start_ref_140()
        self.play(
            tap_on.animate.set_value(1.0),
            cross_in.animate.set_value(1.0),
            world.needle_op.animate.set_value(0.0),
            FadeIn(ref_140),
            run_time=0.35,
        )
        self.play(
            world.v_icf.animate.set_value(DRINK_ICF),
            world.v_ecf.animate.set_value(DRINK_ECF),
            tot_litres.animate.set_value(43.0),
            run_time=self.left() - 0.35, rate_func=linear,
        )
        self.play(tap_on.animate.set_value(0.0), cross_in.animate.set_value(0.0), run_time=0.35)
        self.finish()


class S04DrinkResult(SpokenScene):
    def construct(self):
        # Seamless from S03Drink end: tank at 43 L, '43 L water' bracket, fraction & 140 start reference visible.
        world = BodyWaterWorld(mode=MODE_A_PUSH, v_icf=DRINK_ICF, v_ecf=DRINK_ECF, c_na=C_NA_0,
                               n_na_active=70, readout_mode="hidden", ecf_readout_mode="hidden",
                               needle_op=0.0)
        bracket = make_total_bracket(world, lambda: "43 L water")
        ref_140 = make_start_ref_140()
        sol_sc = ValueTracker(1.0)
        wat_sc = ValueTracker(1.0)
        frac = make_ratio_fraction(np.array([2.95, -0.75, 0.0]), sol_sc, wat_sc, size=34)

        sliver_frac = ValueTracker(0.0)

        def mk_sliver():
            f = sliver_frac.get_value()
            if f <= 0.02:
                return VGroup()
            w_full = (DRINK_ECF - V_ECF_0) * world.scale_t.get_value()
            xr, yb, yt = world.x_right(), world.y_bot(), world.y_top()
            x0 = xr - w_full
            w_now = max(0.02, w_full * f)
            rect = Rectangle(
                width=w_now, height=yt - yb,
                fill_color=WATER_BLUE, fill_opacity=0.55, stroke_color=WATER_BLUE, stroke_width=2.5,
            ).move_to([x0 + w_now / 2, (yb + yt) / 2, 0])
            dash = DashedLine([x0, yb, 0], [x0, yt, 0], color=TEXT, stroke_width=2.5, dash_length=0.14)
            return VGroup(rect, dash)

        sliver = always_redraw(mk_sliver)

        self.add(world.group, bracket, frac, sliver, ref_140)

        self.at("same solute")
        self.play(
            sol_sc.animate.set_value(1.24),
            world.na_boost.animate.set_value(1.36),
            world.ecf_glow.animate.set_value(0.75),
            run_time=0.60,
        )
        self.play(
            sol_sc.animate.set_value(1.0),
            wat_sc.animate.set_value(1.28),
            world.na_boost.animate.set_value(1.0),
            world.ecf_glow.animate.set_value(0.0),
            world.water_glow.animate.set_value(0.65),
            world.needle_op.animate.set_value(1.0),
            run_time=self.left("concentration"),
        )

        self.at("concentration")
        t_drop = max(0.6, self.t_of("137") - self.elapsed())
        frac1 = (C_NA_0 - 139.0) / (C_NA_0 - DRINK_C)
        self.play(
            world.c_na.animate.set_value(139.0),
            world.water_glow.animate.set_value(0.35),
            run_time=t_drop * frac1, rate_func=linear,
        )
        world.readout_mode = "about"
        self.play(
            world.c_na.animate.set_value(DRINK_C),
            world.water_glow.animate.set_value(0.0),
            run_time=t_drop * (1.0 - frac1), rate_func=linear,
        )
        t_hold = max(0.3, self.left("a third of a liter") - 0.85)
        self.wait(t_hold)
        self.play(world.ecf_glow.animate.set_value(0.65), run_time=0.85)

        self.at("a third of a liter")
        sliver_lbl = T("+ about a third\nof a litre", 24, WATER_BLUE, line_spacing=0.84).move_to([world.x_right() + 1.38, 1.05, 0])
        sliver_ptr = Arrow(sliver_lbl.get_left() + LEFT * 0.06, [world.x_right() + 0.04, 1.05, 0],
                           buff=0.0, color=WATER_BLUE, stroke_width=3.0, tip_length=0.15)
        self.play(
            world.ecf_glow.animate.set_value(0.0),
            sliver_frac.animate.set_value(1.0),
            FadeIn(sliver_lbl, shift=RIGHT * 0.1),
            GrowArrow(sliver_ptr),
            run_time=self.left() - 0.3, rate_func=linear,
        )
        self.finish()


class S05Sweat(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_A_PUSH, v_icf=DRINK_ICF, v_ecf=DRINK_ECF, c_na=DRINK_C,
                               n_na_active=70, readout_mode="about")
        sol_sc = ValueTracker(1.0)
        wat_sc = ValueTracker(1.28)
        frac = make_ratio_fraction(np.array([3.05, -0.95, 0.0]), sol_sc, wat_sc, size=34)
        spout = make_sweat_spout(world)
        sweat_on = ValueTracker(0.0)
        sweat_ph = ValueTracker(0.0)
        sweat_stream = make_sweat_stream(world, sweat_on, sweat_ph)

        self.add(world.group, frac, sweat_stream)

        # Two schematic cups well separated with 2-line labels so they never crowd
        cup_p, _, p_fill, p_dots = self._make_cup(np.array([1.92, 1.18, 0.0]), "plasma\n140", 5, seed=11)
        cup_s, cup_s_body, s_fill, s_dots = self._make_cup(np.array([3.58, 1.18, 0.0]), "sweat\nabout 50", 2, seed=22)
        schem = T("schematic", 22, TEXT).move_to([2.75, 2.75, 0])

        # Split sweat label so only "sweat" shows at first; "about 50" reveals on "take 50"
        s_lbl_top = T("sweat", 22, TEXT)
        s_lbl_num = T("about 50", 22, TEXT)
        VGroup(s_lbl_top, s_lbl_num).arrange(DOWN, buff=0.08).move_to(cup_s[1].get_center())
        cup_s.submobjects[1] = VGroup(s_lbl_top, s_lbl_num)

        p_walls_lbl = VGroup(cup_p[0][1], cup_p[1])
        s_walls_lbl = VGroup(cup_s[0][1], s_lbl_top)

        world.readout_mode = "live"
        self.play(
            world.v_icf.animate.set_value(V_ICF_0),
            world.v_ecf.animate.set_value(V_ECF_0),
            world.c_na.animate.set_value(C_NA_0),
            wat_sc.animate.set_value(1.0),
            FadeIn(spout),
            FadeIn(p_walls_lbl, shift=UP * 0.08),
            FadeIn(s_walls_lbl, shift=UP * 0.08),
            FadeIn(schem),
            run_time=self.left("far weaker"), rate_func=linear,
        )

        self.at("far weaker")
        self.play(
            GrowFromEdge(p_fill, DOWN),
            GrowFromEdge(s_fill, DOWN),
            LaggedStart(*[FadeIn(d, shift=DOWN * 0.35) for d in p_dots], lag_ratio=0.15),
            LaggedStart(*[FadeIn(d, shift=DOWN * 0.35) for d in s_dots], lag_ratio=0.25),
            run_time=0.90,
        )

        self.at("varies widely")
        self.play(*[d.animate.scale(1.30) for d in s_dots], run_time=0.45)
        self.play(*[d.animate.scale(1.0 / 1.30) for d in s_dots], run_time=0.45)

        # Reveal numeric sweat label and highlight sweat cup on "take 50"
        self.at("take 50")
        hi_s = SurroundingRectangle(cup_s_body, color=GOLD_NA, buff=0.08, stroke_width=3.5)
        self.play(
            FadeIn(s_lbl_num, shift=DOWN * 0.08),
            Create(hi_s),
            run_time=0.65,
        )
        t_wait_rem = max(0.0, self.left("removes water") - 0.55)
        if t_wait_rem > 0.05:
            self.wait(t_wait_rem)
        self.play(FadeOut(hi_s), run_time=min(0.55, self.left("removes water")))

        self.at("removes water")
        world.n_na_active = 68
        world.ecf_readout_mode = "about"
        self.play(sweat_on.animate.set_value(1.0), run_time=0.30)
        self.play(
            sweat_ph.animate.set_value(2.8),
            world.v_icf.animate.set_value(SWEAT_ICF),
            world.v_ecf.animate.set_value(SWEAT_ECF),
            wat_sc.animate.set_value(0.74),
            sol_sc.animate.set_value(0.92),
            run_time=self.left("rises") - 0.30, rate_func=linear,
        )

        self.at("rises")
        world.readout_mode = "about"
        t_rise = max(0.6, min(1.15, self.t_of("142") - self.elapsed()))
        self.play(
            sweat_ph.animate.set_value(4.5),
            world.c_na.animate.set_value(SWEAT_C),
            world.na_boost.animate.set_value(1.25),
            run_time=t_rise, rate_func=linear,
        )
        self.play(sweat_on.animate.set_value(0.0), run_time=0.25)
        t_hold = max(0.3, self.left() - 0.55)
        self.wait(t_hold)

        self.play(
            FadeOut(cup_p), FadeOut(cup_s), FadeOut(schem), FadeOut(spout), FadeOut(frac),
            world.na_boost.animate.set_value(1.0),
            run_time=0.55, rate_func=linear,
        )
        self.finish()

    def _make_cup(self, center, label, n_dots, seed):
        w, h = 0.86, 0.84
        fill = Rectangle(width=w, height=h * 0.78, fill_color=WATER_BLUE, fill_opacity=0.32, stroke_width=0)
        fill.move_to(center + DOWN * 0.08)
        xl, xr = center[0] - w / 2, center[0] + w / 2
        yb, yt = center[1] - h / 2, center[1] + h / 2
        walls = VGroup(
            Line([xl, yt, 0], [xl, yb, 0]),
            Line([xl, yb, 0], [xr, yb, 0]),
            Line([xr, yb, 0], [xr, yt, 0]),
        ).set_stroke(TANK_STROKE, width=3)
        rng = np.random.default_rng(seed)
        dots = VGroup()
        xs = np.linspace(xl + 0.18, xr - 0.18, n_dots)
        for i, x in enumerate(xs):
            y = center[1] - 0.14 + (0.15 if i % 2 else -0.09) + rng.uniform(-0.03, 0.03)
            dots.add(Dot([x, y, 0], radius=0.062, color=GOLD_NA))
        body = VGroup(fill, walls, dots)
        lbl = T(label, 22, TEXT, line_spacing=0.84).move_to([center[0], yt + 0.56, 0])
        return VGroup(body, lbl), body, fill, dots


class S06Sensor(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_A_PUSH, v_icf=SWEAT_ICF, v_ecf=SWEAT_ECF, c_na=SWEAT_C,
                               n_na_active=68, readout_mode="about")
        self.add(world.group)

        # Auto-wrapping in _mk_comp_labels switches to 2-line before the outside compartment narrows
        self.play(
            world.x_left_t.animate.set_value(MODE_B["x_left"]),
            world.y_bot_t.animate.set_value(MODE_B["y_bot"]),
            world.y_top_t.animate.set_value(MODE_B["y_top"]),
            world.scale_t.animate.set_value(MODE_B["scale"]),
            run_time=self.left("osmoreceptor neurons"), rate_func=linear,
        )
        world.two_line_outside = True

        self.at("osmoreceptor neurons")
        neuron_r = ValueTracker(0.34)
        spike_rate = ValueTracker(0.9)
        brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=False)
        schem = T("schematic", 22, TEXT).move_to([-5.45, -3.35, 0])
        self.play(LaggedStart(*[FadeIn(m) for m in brain], FadeIn(schem), lag_ratio=0.35,
                              run_time=3.5))

        self.at("sense it")
        n_ring = Circle(radius=0.52, color=CYAN_OSMO, stroke_width=3.8).move_to(NEURON_C)
        sense_dot = Dot(brain.sample_line.get_start(), radius=0.085, color=CYAN_OSMO)
        self.add(sense_dot)
        self.play(
            MoveAlongPath(sense_dot, brain.sample_line),
            FadeIn(n_ring, scale=1.2),
            run_time=0.85,
        )
        self.remove(sense_dot)
        self.play(
            FadeOut(n_ring, scale=1.15),
            world.ecf_glow.animate.set_value(0.55),
            run_time=self.left("plasma grows"),
        )

        self.at("plasma grows")
        g_ring = make_needle_ring(SWEAT_C)
        t_pg = self.left("water leaves")
        self.play(
            FadeIn(g_ring, scale=1.2),
            world.ecf_glow.animate.set_value(0.85),
            world.na_boost.animate.set_value(1.28),
            run_time=t_pg * 0.50, rate_func=linear,
        )
        self.play(
            FadeOut(g_ring),
            world.ecf_glow.animate.set_value(0.0),
            world.na_boost.animate.set_value(1.0),
            run_time=t_pg * 0.50, rate_func=linear,
        )

        self.at("water leaves")
        out_drops = VGroup()
        anims = []
        for ang in (0.35, 1.35, 2.35, -0.65, -2.0):
            p0 = NEURON_C + 0.30 * np.array([np.cos(ang), np.sin(ang), 0])
            p1 = NEURON_C + 1.05 * np.array([np.cos(ang), np.sin(ang), 0])
            d = Dot(p0, radius=0.075, color=WATER_BLUE)
            out_drops.add(d)
            anims.append(d.animate.move_to(p1).set_opacity(0.0))
        self.add(out_drops)
        self.play(
            neuron_r.animate.set_value(0.24),
            *anims,
            run_time=self.left("fire faster"), rate_func=linear,
        )
        self.remove(out_drops)

        self.at("fire faster")
        self.play(spike_rate.animate.set_value(3.2), run_time=self.left())
        self.finish()


class S07Vasopressin(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_B, v_icf=SWEAT_ICF, v_ecf=SWEAT_ECF, c_na=SWEAT_C,
                               n_na_active=70, two_line_outside=True, readout_mode="about")
        neuron_r = ValueTracker(0.24)
        spike_rate = ValueTracker(3.2)
        brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=False)
        brain_pit = make_brain_neuron(neuron_r, spike_rate, show_pituitary=True)
        duct = CollectingDuct(pore_open=0.0, show_v2=False, show_avp_stream=False, x_right_fn=world.x_right)

        self.add(world.group, brain)

        # Axon signal reaches pituitary node at base of brain
        self.play(
            FadeIn(brain_pit.pit, scale=1.15),
            FadeIn(brain_pit.pit_lbl, shift=LEFT * 0.08),
            run_time=self.left("vasopressin"),
        )

        self.at("vasopressin")
        self.remove(brain)
        self.add(brain_pit)
        self.add(duct.avp_dots)
        t_avp = self.left("collecting duct")
        self.play(
            duct.avp_flow.animate.set_value(1.0),
            world.ecf_glow.animate.set_value(0.45),
            run_time=t_avp * 0.55,
        )
        self.play(world.ecf_glow.animate.set_value(0.0), run_time=t_avp * 0.45)

        self.at("collecting duct")
        self.remove(duct.avp_dots)
        self.add(duct.clock, duct.urine, duct.walls, duct.label, duct.reabsorb, duct.avp_dots)
        self.play(
            Create(duct.walls),
            FadeIn(duct.label),
            GrowFromEdge(duct.urine, UP),
            run_time=self.left("binds v2"),
        )
        self.add(duct.v2_sites, duct.aqp2)

        # V2 label cleanly on the blood side between tank and duct, with green dots docking at V2 sites
        self.at("binds v2")
        v2_lbl = T("V2", 24, GREEN_AVP).move_to([1.54, 0.42, 0])
        v2_ptr = Arrow([1.58, 0.24, 0], [duct.x_l_out - 0.08, 0.08, 0],
                       buff=0.0, color=GREEN_AVP, stroke_width=2.8, tip_length=0.12)
        dockers = VGroup(*[Dot([0.65, y, 0], radius=0.085, color=GREEN_AVP) for y in duct.pore_ys[:3]])
        self.add(dockers)
        t_v2 = self.left("aquaporin")
        self.play(
            *[d.animate.move_to([duct.x_l_out - 0.10, y, 0]) for d, y in zip(dockers, duct.pore_ys[:3])],
            FadeIn(v2_lbl, shift=DOWN * 0.08),
            GrowArrow(v2_ptr),
            run_time=t_v2 * 0.65,
        )
        self.play(duct.v2_bound.animate.set_value(1.0), FadeOut(dockers), run_time=t_v2 * 0.35)
        self.remove(dockers)

        # aquaporin-2 label cleanly between duct and gauge ticks (y = -1.68, halfway between 135 and 130)
        self.at("aquaporin")
        aqp_lbl = T("aquaporin-2", 22, GREEN_AVP).move_to([3.52, -1.68, 0])
        p_aqp_start = aqp_lbl.get_left() + LEFT * 0.06
        p_aqp_mid = np.array([duct.x_r_out + 0.08, duct.pore_ys[-1], 0.0])
        p_aqp_end = np.array([duct.x_l_in, duct.pore_ys[-1], 0.0])
        aqp_ptr = VGroup(
            Line(p_aqp_start, p_aqp_mid, color=GREEN_AVP, stroke_width=2.8),
            Arrow(p_aqp_mid, p_aqp_end, buff=0.0, color=GREEN_AVP, stroke_width=2.8, tip_length=0.14),
        )
        self.play(
            FadeIn(aqp_lbl, shift=RIGHT * 0.1),
            Succession(Create(aqp_ptr[0], run_time=0.25), GrowArrow(aqp_ptr[1], run_time=0.35)),
        )
        t_aqp = self.left("water returns")
        self.play(duct.pore_open.animate.set_value(0.55), run_time=t_aqp * 0.40, rate_func=linear)
        self.play(
            duct.pore_open.animate.set_value(1.0),
            world.v_ecf.animate.set_value(13.52),
            run_time=t_aqp * 0.60, rate_func=linear,
        )

        self.at("water returns")
        t_ret = self.left()
        self.play(
            world.v_ecf.animate.set_value(13.70),
            world.c_na.animate.set_value(141.2),
            world.water_glow.animate.set_value(0.45),
            run_time=t_ret * 0.65, rate_func=linear,
        )
        self.play(world.water_glow.animate.set_value(0.0), run_time=t_ret * 0.35)
        self.finish()


class S08Thirst(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_B, v_icf=SWEAT_ICF, v_ecf=13.7, c_na=141.2,
                               n_na_active=70, two_line_outside=True, readout_mode="about")
        neuron_r = ValueTracker(0.24)
        spike_rate = ValueTracker(2.6)
        brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=True)
        duct = CollectingDuct(pore_open=1.0, show_v2=True, show_avp_stream=True, x_right_fn=world.x_right)
        tap_on = ValueTracker(0.0)
        tap_stream = make_tap_stream(world, tap_on)

        # Vertical urine osmolality bar cleanly centered between duct (x=2.53) and gauge ticks (x=4.81)
        bar_x, bar_w = 3.86, 0.54
        bar_y0, bar_y1 = -2.05, 0.50
        u_osm = ValueTracker(800.0)
        u_band_hi = ValueTracker(0.0)

        bar_bg = VGroup(
            Line([bar_x - bar_w / 2, bar_y0, 0], [bar_x + bar_w / 2, bar_y0, 0]),
            Line([bar_x - bar_w / 2, bar_y1, 0], [bar_x + bar_w / 2, bar_y1, 0]),
            Line([bar_x - bar_w / 2, bar_y0, 0], [bar_x - bar_w / 2, bar_y1, 0]),
            Line([bar_x + bar_w / 2, bar_y0, 0], [bar_x + bar_w / 2, bar_y1, 0]),
        ).set_stroke(TEXT, width=2.5)
        bar_title = T("urine\n(mOsm/kg)", 22, TEXT, line_spacing=0.82).move_to([bar_x, bar_y1 + 0.56, 0])

        def mk_bar_fill():
            val = np.clip(u_osm.get_value(), 0.0, 1200.0)
            h = max(0.04, (val / 1200.0) * (bar_y1 - bar_y0))
            fill = Rectangle(
                width=bar_w - 0.06, height=h,
                fill_color=WATER_BLUE if val < 200 else GREEN_AVP,
                fill_opacity=0.75, stroke_width=0,
            ).move_to([bar_x, bar_y0 + h / 2, 0])
            g = VGroup(fill)
            if u_band_hi.get_value() > 0.1 and val >= 950.0:
                y_1000 = bar_y0 + (1000.0 / 1200.0) * (bar_y1 - bar_y0)
                band = Rectangle(
                    width=bar_w - 0.04, height=bar_y1 - y_1000,
                    fill_color=GREEN_AVP, fill_opacity=0.40, stroke_color=GREEN_AVP, stroke_width=2.5,
                ).move_to([bar_x, (y_1000 + bar_y1) / 2, 0])
                g.add(band)
            return g

        # Bar readout driven strictly by u_osm tracker: number and bar height ALWAYS agree!
        def mk_bar_readout():
            val = u_osm.get_value()
            if val <= 75.0:
                return T("near 50", 22, WATER_BLUE).move_to([bar_x, bar_y0 - 0.36, 0])
            if val >= 980.0:
                return T("1,000–1,200", 22, GREEN_AVP).move_to([bar_x, bar_y0 - 0.36, 0])
            return VGroup()

        bar_fill = always_redraw(mk_bar_fill)
        bar_ro = always_redraw(mk_bar_readout)
        bar_group = VGroup(bar_fill, bar_bg, bar_title, bar_ro)

        self.add(world.group, brain, duct.group, tap_stream, bar_group)

        self.at("without the hormone")
        t_drop = max(0.8, self.t_of("50") - self.elapsed())
        self.play(
            duct.avp_flow.animate.set_value(0.0),
            duct.v2_bound.animate.set_value(0.0),
            duct.pore_open.animate.set_value(0.0),
            u_osm.animate.set_value(50.0),
            world.v_ecf.animate.set_value(SWEAT_ECF),
            world.c_na.animate.set_value(SWEAT_C),
            run_time=t_drop, rate_func=linear,
        )
        t_rest = self.left("short of water")
        if t_rest > 0.05:
            self.wait(t_rest)

        self.at("short of water")
        t_rise = max(0.8, self.t_of("1") - self.elapsed())
        self.play(
            duct.avp_flow.animate.set_value(1.0),
            duct.v2_bound.animate.set_value(1.0),
            duct.pore_open.animate.set_value(1.0),
            u_osm.animate.set_value(1100.0),
            u_band_hi.animate.set_value(1.0),
            world.v_ecf.animate.set_value(13.70),
            world.c_na.animate.set_value(141.2),
            run_time=t_rise, rate_func=linear,
        )

        self.at("drive thirst")
        thirst = make_thirst_arrow(world)
        thirst.progress.set_value(0.0)
        self.add(thirst)
        bar_fill.clear_updaters()
        bar_ro.clear_updaters()
        self.play(
            thirst.progress.animate.set_value(1.0),
            FadeOut(bar_group),
            run_time=self.left("replaces water"),
        )

        self.at("replaces water")
        world.readout_mode = "live"
        self.play(tap_on.animate.set_value(1.0), run_time=0.25)
        self.play(
            world.v_icf.animate.set_value(V_ICF_0),
            world.v_ecf.animate.set_value(V_ECF_0),
            world.c_na.animate.set_value(C_NA_0),
            neuron_r.animate.set_value(0.34),
            spike_rate.animate.set_value(0.9),
            run_time=self.left() - 0.45, rate_func=linear,
        )
        self.play(tap_on.animate.set_value(0.0), run_time=0.45)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        # Pull back gently to full world layout (MODE_B) while building the ratio bar
        world = BodyWaterWorld(
            mode=dict(x_left=-4.45, y_bot=-2.55, y_top=1.78, scale=0.140),
            v_icf=V_ICF_0, v_ecf=V_ECF_0, c_na=C_NA_0,
            n_na_active=70, two_line_outside=True,
        )
        neuron_r = ValueTracker(0.34)
        spike_rate = ValueTracker(0.9)
        brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=True)
        duct = CollectingDuct(pore_open=0.65, show_v2=True, show_avp_stream=True, x_right_fn=world.x_right)
        thirst = make_thirst_arrow(world)
        tap_on = ValueTracker(0.0)
        tap_stream = make_tap_stream(world, tap_on)

        sol_sc = ValueTracker(1.0)
        wat_sc = ValueTracker(1.0)
        sol_op = ValueTracker(0.0)
        wat_op = ValueTracker(0.0)
        bar_op = ValueTracker(0.0)
        frac = make_ratio_fraction(
            np.array([3.58, 0.25, 0.0]), sol_sc, wat_sc, size=32,
            sol_op=sol_op, wat_op=wat_op, bar_op=bar_op,
        )

        target_140 = Line(
            [GAUGE_X - 0.18, gauge_y(140.0), 0],
            [GAUGE_X + 0.56, gauge_y(140.0), 0],
            color=CYAN_OSMO, stroke_width=3.8,
        )

        self.add(world.group, target_140, brain, duct.group, thirst, frac, tap_stream)

        self.play(
            world.x_left_t.animate.set_value(MODE_B["x_left"]),
            world.y_bot_t.animate.set_value(MODE_B["y_bot"]),
            world.y_top_t.animate.set_value(MODE_B["y_top"]),
            world.scale_t.animate.set_value(MODE_B["scale"]),
            run_time=self.left("plasma sodium concentration", lead=1.2), rate_func=linear,
        )

        self.at("plasma sodium concentration", lead=1.2)
        g_ring = make_needle_ring(140.0)
        t_conc = self.left("body solute")
        self.play(
            FadeIn(g_ring, scale=1.25),
            world.ecf_glow.animate.set_value(0.65),
            run_time=min(0.85, t_conc * 0.35),
        )
        self.play(
            FadeOut(g_ring),
            world.ecf_glow.animate.set_value(0.0),
            run_time=max(0.4, t_conc - min(0.85, t_conc * 0.35)),
        )

        self.at("body solute")
        self.play(
            bar_op.animate.set_value(1.0),
            sol_op.animate.set_value(1.0),
            sol_sc.animate.set_value(1.24),
            world.na_boost.animate.set_value(1.38),
            world.ecf_glow.animate.set_value(0.75),
            run_time=self.left("body water"),
        )

        self.at("body water")
        t_bw = self.left("the water loop")
        self.play(
            sol_sc.animate.set_value(1.0),
            world.na_boost.animate.set_value(1.0),
            world.ecf_glow.animate.set_value(0.0),
            wat_op.animate.set_value(1.0),
            wat_sc.animate.set_value(1.24),
            world.water_glow.animate.set_value(0.85),
            run_time=t_bw * 0.58,
        )
        self.play(
            wat_sc.animate.set_value(1.0),
            world.water_glow.animate.set_value(0.0),
            run_time=t_bw * 0.42,
        )

        self.at("the water loop")
        wloop = make_water_loop_arrows(world)
        t_loop = self.left("adding")
        self.play(Create(wloop[0]), FadeIn(wloop[1]), run_time=t_loop * 0.55)
        self.play(
            world.c_na.animate.set_value(142.2),
            world.v_ecf.animate.set_value(13.5),
            run_time=t_loop * 0.30, rate_func=linear,
        )
        self.wait(t_loop * 0.15)

        self.at("adding")
        self.play(tap_on.animate.set_value(1.0), run_time=0.16)
        self.play(
            world.c_na.animate.set_value(140.0),
            world.v_ecf.animate.set_value(14.0),
            run_time=0.52, rate_func=linear,
        )
        self.play(
            tap_on.animate.set_value(0.0),
            world.c_na.animate.set_value(137.8),
            world.v_ecf.animate.set_value(14.4),
            run_time=0.34, rate_func=linear,
        )

        self.at("removing")
        t_rem = max(0.9, self.left("reports water"))
        self.play(duct.pore_open.animate.set_value(0.0), run_time=t_rem * 0.18)
        self.play(
            world.c_na.animate.set_value(140.0),
            world.v_ecf.animate.set_value(14.0),
            run_time=t_rem * 0.57, rate_func=linear,
        )
        self.play(duct.pore_open.animate.set_value(0.65), run_time=t_rem * 0.25)

        self.at("reports water")
        h = (self.left() - 0.4) / 2
        self.play(wat_sc.animate.set_value(1.32), world.water_glow.animate.set_value(0.85), run_time=h)
        self.play(wat_sc.animate.set_value(1.0), world.water_glow.animate.set_value(0.0), run_time=h)

        self.play(FadeOut(frac), run_time=0.4)
        self.finish()


def _build_s10_world(c_na=SALT_PRE_C, with_kept_tag=True):
    """Shared builder so S10Predict end frame and S11Pause backdrop match identically."""
    world = BodyWaterWorld(mode=MODE_B, v_icf=V_ICF_0, v_ecf=V_ECF_0, c_na=c_na,
                           n_na_active=75, two_line_outside=True, readout_mode="hidden",
                           highlight_140=False)
    neuron_r = ValueTracker(0.28)
    spike_rate = ValueTracker(2.2)
    brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=True)
    duct = CollectingDuct(pore_open=0.65, show_v2=True, show_avp_stream=True, x_right_fn=world.x_right)
    thirst = make_thirst_arrow(world)
    g = VGroup(world.group, brain, duct.group, thirst)
    kept_tag = None
    if with_kept_tag:
        # Placed cleanly left of the tap pipe (x = -0.35, right edge ~ +0.52 vs tap at +1.18)
        kept_tag = T("kept: 140 mmol", 23, GOLD_NA).move_to([world.x_mem() + 0.15, world.y_top() + 0.34, 0])
        g.add(kept_tag)
    return world, neuron_r, spike_rate, duct, g, kept_tag


class S10Predict(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_B, v_icf=V_ICF_0, v_ecf=V_ECF_0, c_na=C_NA_0,
                               n_na_active=70, two_line_outside=True, highlight_140=False)
        neuron_r = ValueTracker(0.34)
        spike_rate = ValueTracker(0.9)
        brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=True)
        duct = CollectingDuct(pore_open=0.65, show_v2=True, show_avp_stream=True, x_right_fn=world.x_right)
        thirst = make_thirst_arrow(world)
        self.add(world.group, brain, duct.group, thirst)

        self.play(world.ecf_glow.animate.set_value(0.75), run_time=self.left("140 millimoles"))

        self.at("140 millimoles")
        l_out_right = world.comp_labels[1].get_right()[0]
        tap_left = world.tap_tip()[0] - 0.12
        x_entry = (l_out_right + tap_left) / 2
        y_start = world.y_top() + 0.55
        y_clear = world.y_dots_top() - 0.04
        x_targets = np.linspace(world.x_mem() + 0.22, world.x_right() - 0.22, 5)
        y_targets = [0.22, 0.02, 0.26, -0.04, 0.16]
        falling = VGroup(*[
            Dot([x_entry, y_start, 0], radius=0.095, color=GOLD_NA)
            for _ in range(5)
        ])
        self.add(falling)
        kept_tag = T("kept: 140 mmol", 23, GOLD_NA).move_to([world.x_mem() + 0.15, world.y_top() + 0.34, 0])

        def _make_drop_anim(dot, tx, ty):
            p0 = np.array([x_entry, y_start, 0.0])
            p1 = np.array([x_entry, y_clear, 0.0])
            p2 = np.array([tx, ty, 0.0])

            def _upd(mob, alpha):
                if alpha <= 0.58:
                    f = alpha / 0.58
                    mob.move_to(p0 + f * (p1 - p0))
                    mob.set_width(0.19)
                else:
                    f = (alpha - 0.58) / 0.42
                    mob.move_to(p1 + f * (p2 - p1))
                    mob.set_width(0.19 * (1.0 - 0.35 * f))

            return UpdateFromAlphaFunc(dot, _upd)

        self.play(
            LaggedStart(
                *[_make_drop_anim(d, tx, ty) for d, tx, ty in zip(falling, x_targets, y_targets)],
                lag_ratio=0.22,
            ),
            run_time=self.left("about eight grams"), rate_func=linear,
        )
        self.remove(falling)
        world.n_na_active = 75
        world.readout_mode = "hidden"
        t_salt = self.left("water loop")
        self.play(
            FadeIn(kept_tag, shift=UP * 0.1),
            world.na_boost.animate.set_value(1.36),
            world.c_na.animate.set_value(SALT_PRE_C),
            neuron_r.animate.set_value(0.28),
            spike_rate.animate.set_value(2.2),
            run_time=t_salt * 0.65, rate_func=linear,
        )
        self.play(world.na_boost.animate.set_value(1.0), run_time=t_salt * 0.35)

        self.at("water loop")
        self.play(
            world.ecf_glow.animate.set_value(0.0),
            thirst.stroke_w.animate.set_value(6.0),
            run_time=self.left("where does the gauge") * 0.5,
        )
        self.play(
            thirst.stroke_w.animate.set_value(3.2),
            run_time=self.left("where does the gauge"),
        )

        self.at("where does the gauge")
        q = question_card("Where does the gauge settle?", y=3.42, color=TEXT, size=32)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.80)
        self.finish()


class S11Pause(PredictPause):
    QUESTION = "Where does the gauge settle?"
    CARD = {"y": 3.42, "color": TEXT, "size": 32}
    RING_AT = (3.55, -2.75, 0)
    SECONDS = 4.5

    def backdrop(self):
        _, _, _, _, g, _ = _build_s10_world(c_na=SALT_PRE_C, with_kept_tag=True)
        return g


class S12Answer(SpokenScene):
    def construct(self):
        world, neuron_r, spike_rate, duct, bg_group, kept_tag = _build_s10_world(c_na=SALT_PRE_C, with_kept_tag=True)
        q = question_card("Where does the gauge settle?", y=3.42, color=TEXT, size=32)

        strip_on = ValueTracker(0.0)

        def mk_new_litre():
            f = strip_on.get_value()
            if f <= 0.02:
                return VGroup()
            x_old = world.x_mem() + V_ECF_0 * world.scale_t.get_value()
            xr, yb, yt = world.x_right(), world.y_bot(), world.y_top()
            w_now = max(0.02, xr - x_old)
            rect = Rectangle(
                width=w_now, height=yt - yb,
                fill_color=WATER_BLUE, fill_opacity=0.45 * f,
                stroke_color=WATER_BLUE, stroke_width=2.5, stroke_opacity=f,
            ).move_to([x_old + w_now / 2, (yb + yt) / 2, 0])
            dash = DashedLine([x_old, yb, 0], [x_old, yt, 0], color=TEXT, stroke_width=2.5, dash_length=0.14)
            return VGroup(rect, dash)

        new_litre = always_redraw(mk_new_litre)

        self.add(bg_group, new_litre, q.question)

        self.play(FadeOut(q.question), run_time=0.35)

        # Explicit answer reveal at the first spoken '140'; keep '140 again' as a fixed answer callout
        self.at("140")
        tick_140 = Line(
            [GAUGE_X - 0.18, gauge_y(140.0), 0],
            [GAUGE_X + 0.18, gauge_y(140.0), 0],
            color=CYAN_OSMO, stroke_width=3.5,
        )
        ring = make_needle_ring(SALT_POST_C)
        answer_callout = M("140 again", 25, TEXT).move_to([GAUGE_X - 0.05, -2.78, 0])
        self.play(
            world.c_na.animate.set_value(SALT_POST_C),
            FadeIn(tick_140),
            FadeIn(ring, scale=1.2),
            FadeIn(answer_callout),
            run_time=0.25, rate_func=linear,
        )

        # Tagged replay: return moving needle to high start, thin urine stream & emphasize returning blue drops,
        # and move needle down to 140 as v_ecf expands to SALT_POST_ECF.
        self.at("water loop")
        replay_tag = chip("replay: how the water loop restores 140", CYAN_OSMO, size=24).move_to([-0.5, 3.35, 0])
        self.play(
            FadeIn(replay_tag, shift=DOWN * 0.08),
            FadeOut(ring),
            FadeOut(answer_callout, run_time=0.25),
            world.c_na.animate.set_value(SALT_PRE_C),
            duct.pore_open.animate.set_value(0.25),
            spike_rate.animate.set_value(3.4),
            run_time=0.55, rate_func=linear,
        )
        self.play(
            duct.pore_open.animate.set_value(1.0),
            duct.reabsorb_boost.animate.set_value(1.0),
            world.water_glow.animate.set_value(0.45),
            world.v_ecf.animate.set_value(14.15),
            world.c_na.animate.set_value((S_TOT_0 + 140.0) / (V_ICF_0 + 14.15)),
            run_time=0.70, rate_func=linear,
        )
        t_restore = max(0.5, self.t_of("restored") - self.elapsed())
        self.play(
            world.v_ecf.animate.set_value(SALT_POST_ECF),
            world.c_na.animate.set_value(SALT_POST_C),
            world.water_glow.animate.set_value(0.0),
            neuron_r.animate.set_value(0.34),
            spike_rate.animate.set_value(1.0),
            run_time=t_restore, rate_func=linear,
        )

        self.at("ratio is restored")
        t_rest = self.left("140 millimoles")
        self.play(
            FadeOut(replay_tag),
            FadeIn(answer_callout, run_time=0.35),
            duct.reabsorb_boost.animate.set_value(0.0),
            FadeIn(ring),
            world.na_boost.animate.set_value(1.32),
            run_time=t_rest * 0.55,
        )
        self.play(
            FadeOut(ring),
            world.na_boost.animate.set_value(1.0),
            run_time=t_rest * 0.45,
        )

        self.at("140 millimoles")
        plus_lbl = T("+1 L", 25, WATER_BLUE).move_to([world.x_right() + 0.50, world.y_top() + 0.05, 0])
        self.play(strip_on.animate.set_value(1.0), FadeIn(plus_lbl, shift=UP * 0.1), run_time=self.left("outside the cells"))

        self.at("outside the cells")
        t_out = self.left()
        self.play(world.ecf_glow.animate.set_value(0.95), world.na_boost.animate.set_value(1.28), run_time=t_out * 0.45)
        self.play(world.ecf_glow.animate.set_value(0.0), world.na_boost.animate.set_value(1.0), run_time=t_out * 0.55)
        self.finish()


class S13SodiumLoop(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_B, v_icf=SALT_POST_ICF, v_ecf=SALT_POST_ECF, c_na=SALT_POST_C,
                               n_na_active=75, two_line_outside=True)
        neuron_r = ValueTracker(0.34)
        spike_rate = ValueTracker(0.9)
        brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=True)
        duct = CollectingDuct(pore_open=0.65, show_v2=True, show_avp_stream=True, x_right_fn=world.x_right)
        thirst = make_thirst_arrow(world)

        valve_open = ValueTracker(0.0)
        valve_ph = ValueTracker(0.0)
        ring_scale = ValueTracker(1.0)
        loop_draw = ValueTracker(0.0)
        valve_clock = VMobject()
        valve_clock.add_updater(lambda m, dt: valve_ph.set_value((valve_ph.get_value() + 0.85 * min(dt, 0.08)) % 1.0))
        na_loop = make_sodium_loop(world, valve_open, valve_ph, ring_scale=ring_scale, loop_draw=loop_draw)

        self.add(world.group, brain, duct.group, thirst, valve_clock)

        self.play(
            world.ecf_glow.animate.set_value(0.95),
            world.na_boost.animate.set_value(1.32),
            run_time=self.left("sodium content"),
        )

        self.at("sodium content")
        t_sc = self.left("a second loop")
        # Gold volume span bar across outside compartment so volume-by-content is visible over a large area
        vol_span = DoubleArrow(
            [world.x_mem() + 0.08, (world.y_bot() + world.y_top()) / 2, 0],
            [world.x_right() - 0.08, (world.y_bot() + world.y_top()) / 2, 0],
            buff=0.0, color=GOLD_NA, stroke_width=4.5, tip_length=0.16,
        )
        self.play(
            GrowFromCenter(vol_span),
            world.ecf_glow.animate.set_value(0.35),
            world.na_boost.animate.set_value(1.0),
            run_time=t_sc * 0.50,
        )
        self.play(
            FadeOut(vol_span),
            world.ecf_glow.animate.set_value(0.95),
            run_time=t_sc * 0.50,
        )

        self.at("a second loop")
        self.add(na_loop[0], na_loop[1])
        t_2nd = self.left("it senses")
        self.play(
            world.ecf_glow.animate.set_value(0.0),
            FadeIn(na_loop[0]),
            loop_draw.animate.set_value(0.35),
            ring_scale.animate.set_value(1.32),
            run_time=t_2nd * 0.55,
        )
        self.play(ring_scale.animate.set_value(1.0), run_time=t_2nd * 0.45)

        self.at("it senses")
        t_sense = self.left("sets how much")
        self.play(
            loop_draw.animate.set_value(1.0),
            ring_scale.animate.set_value(1.35),
            run_time=t_sense * 0.55, rate_func=linear,
        )
        self.play(ring_scale.animate.set_value(1.0), run_time=t_sense * 0.45)

        self.at("sets how much")
        self.play(FadeIn(na_loop[2]), run_time=0.35)
        world.n_na_active = 72
        self.play(
            valve_open.animate.set_value(1.0),
            world.v_ecf.animate.set_value(14.4),
            run_time=max(0.8, self.left() - 0.80), rate_func=linear,
        )
        self.play(valve_open.animate.set_value(0.25), run_time=0.45)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        world = BodyWaterWorld(mode=MODE_B, v_icf=V_ICF_0, v_ecf=14.4, c_na=C_NA_0,
                               n_na_active=72, two_line_outside=True)
        neuron_r = ValueTracker(0.34)
        spike_rate = ValueTracker(0.9)
        brain = make_brain_neuron(neuron_r, spike_rate, show_pituitary=True)
        duct = CollectingDuct(pore_open=0.65, show_v2=True, show_avp_stream=True, x_right_fn=world.x_right)
        thirst = make_thirst_arrow(world)
        wloop = make_water_loop_arrows(world)
        valve_open = ValueTracker(0.25)
        valve_ph = ValueTracker(0.0)
        ring_scale = ValueTracker(1.0)
        na_loop = make_sodium_loop(world, valve_open, valve_ph, ring_scale=ring_scale)

        self.add(world.group, brain, duct.group, thirst, wloop, na_loop)

        # Two loops, two quantities: briefly spotlight each loop before naming its quantity
        t_intro = self.left("water fixes")
        self.play(
            wloop[0].animate.set_stroke(width=6.5),
            run_time=t_intro * 0.48,
        )
        self.play(
            wloop[0].animate.set_stroke(width=3.5),
            ring_scale.animate.set_value(1.30),
            world.ecf_glow.animate.set_value(0.65),
            run_time=t_intro * 0.52,
        )

        self.at("water fixes")
        conc_lbl = T("concentration", 24, CYAN_OSMO).move_to([GAUGE_X - 0.05, -3.26, 0])
        g_ring = make_needle_ring(140.0)
        self.play(
            ring_scale.animate.set_value(1.0),
            world.ecf_glow.animate.set_value(0.0),
            FadeIn(conc_lbl, shift=UP * 0.1),
            FadeIn(g_ring),
            wloop[0].animate.set_stroke(width=6.0),
            run_time=0.80,
        )
        self.play(FadeOut(g_ring), wloop[0].animate.set_stroke(width=3.5), run_time=self.left("fixes the volume"))

        self.at("fixes the volume")
        vol_lbl = T("volume", 24, ORANGE_VOL).move_to([0.25, world.y_bot() - 0.88, 0])
        t_vol = self.left("low", nth=0)
        self.play(
            FadeIn(vol_lbl, shift=UP * 0.1),
            world.ecf_glow.animate.set_value(0.95),
            world.v_ecf.animate.set_value(15.0),
            run_time=t_vol * 0.58, rate_func=linear,
        )
        world.n_na_active = 75
        self.play(world.ecf_glow.animate.set_value(0.0), run_time=t_vol * 0.42)

        self.at("low", nth=0)
        low_lbl = T("low reading", 24, CYAN_OSMO).move_to([GAUGE_X - 0.05, -3.26, 0])
        self.play(
            swap(conc_lbl, low_lbl, run_time=0.5),
            FadeOut(vol_lbl, run_time=0.4),
            world.c_na.animate.set_value(132.0),
            world.water_glow.animate.set_value(0.55),
            run_time=1.8, rate_func=linear,
        )
        t_hold = self.left("low", nth=1, floor=0.0)
        if t_hold > 0.05:
            self.wait(t_hold)

        # Body sodium low (52 dots, 11.03 L), normal (70 dots, 14.85 L), high (75 dots, 15.91 L) — all at low reading 132!
        self.at("low", nth=1)
        world.n_na_active = 52
        state_lbl = T("low", 24, GOLD_NA).move_to([0.25, world.y_bot() - 0.88, 0])
        self.play(
            world.water_glow.animate.set_value(0.0),
            world.v_ecf.animate.set_value(11.03),
            FadeIn(state_lbl, run_time=0.18),
            run_time=0.40, rate_func=linear,
        )

        self.at("normal")
        world.n_na_active = 70
        state_lbl2 = T("normal", 24, GOLD_NA).move_to([0.25, world.y_bot() - 0.88, 0])
        self.play(
            world.v_ecf.animate.set_value(14.85),
            swap(state_lbl, state_lbl2, run_time=0.26),
            run_time=0.38, rate_func=linear,
        )

        self.at("or high")
        world.n_na_active = 75
        state_lbl3 = T("high", 24, GOLD_NA).move_to([0.25, world.y_bot() - 0.88, 0])
        self.play(
            world.v_ecf.animate.set_value(15.91),
            swap(state_lbl2, state_lbl3, run_time=0.26),
            run_time=0.40, rate_func=linear,
        )
        self.wait(0.32)

        world.n_na_active = 75
        self.play(
            FadeOut(state_lbl3), FadeOut(low_lbl),
            world.v_ecf.animate.set_value(15.0),
            world.c_na.animate.set_value(140.0),
            run_time=0.65, rate_func=linear,
        )
        self.finish()


class S15End(EndCard):
    LINE = "Sodium concentration reports water; sodium content sets the volume."
