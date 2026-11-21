"""
"Empty, Busy, or Both" — Enzyme Kinetics Chapter 2 (STEMhop)

COLOUR MAP (one colour per concept, carried across all 14 scenes):
  BLUE    (#58C4DD) : Enzyme booths (E), uninhibited curve v = 60[S]/(4+[S]), original Km = 4 mM, Vmax = 60
  YELLOW  (#F5D547) : Substrate cars (S) and substrate concentration [S]
  GREEN   (#83C167) : Product cars (P) leaving completed catalysis
  MAGENTA (#E056C1) : Reversible inhibitor clamps (I), inhibited curves 1/2/3, apparent Km, inhibited Vmax
  GOLD    (#D4A843) : Predict question card, countdown ring, and ratio callouts (÷3)
  TEXT    (#E8EAF0) : Headings, axis labels, tick numbers, and un-tinted callouts
  GREY    (#8B93A1) : Axis lines, ghost curves, and schematic scope tag

CARRIED WORLD:
  Left side : Toll plaza of 6 BLUE enzyme booths (schematic) with incoming YELLOW 'S' cars,
              return loops for rejected cars, outgoing GREEN 'P' cars, hinged doorway gates,
              and MAGENTA 'I' inhibitor clamps (doorway or side site).
  Right side: Computed Michaelis-Menten graph ([S] 0..40 mM vs initial velocity 0..60 umol/min)
              with BLUE uninhibited curve v = 60[S]/(4+[S]) and dashed Vmax = 60 ceiling.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s00_link_and_question  : [S] tracker sweeps 2->32 mM driving plaza arrival/occupancy and a booth icon riding
                           v = 60[S]/(4+[S]); 'I' clamps latch onto booths and 3 computed MAGENTA curves peel off.
  s02_pools              : Plaza expands to 60%; live counters tally empty vs busy booths from simulation state;
                           MAGENTA clamps latch onto an empty booth, a busy booth, then both, and one lifts off.
  s03_competitive        : MAGENTA clamps settle only into empty doorways (EI) and bounce off busy booths (ES);
                           arriving S cars curve into return loops when meeting clamped doorways.
  s04_competitive_effect : Graph expands to 60%; ValueTracker slides apparent Km from 4 to 12 mM at v=30 along
                           v = 60[S]/(12+[S]); [S] ramps to 40 mM flooding plaza with S cars while dot climbs to Vmax=60.
  s05_uncompetitive      : Plaza expands to 60%; MAGENTA clamps lock only busy booths (ES->ESI), bouncing off E;
                           remaining empty booths fill with S cars so bound count (ES+ESI) climbs.
  s06_uncompetitive_effect: Graph expands to 60%; ValueTracker slides apparent Km left from 4 to 4/3 (~1.3) mM
                           and Vmax ceiling drops 60->20 along v = 60[S]/(4+3[S]), with ÷3 tags on both drops.
  s07_guiding_idea       : Equal split; live plaza runs while 3 slots ('empty','busy','both') highlight in turn
                           and brighten computed curve 1, curve 2, or '?' on the graph.
  s08_predict            : Side-site MAGENTA clamps lock 4 of 6 booths (both E and ES equally) leaving 2 active;
                           predict question card appears while slowed plaza runs.
  s10_answer             : Question becomes 'No'; 4 clamped booths fade leaving 2 cycling booths ('less enzyme');
                           Vmax ceiling drops 60->20 while dot and drop line hold at Km = 4 on v = 20[S]/(4+[S]).
  s11_mixed              : Side clamps on empty vs busy booths thicken unevenly (empty-heavy then busy-heavy);
                           km_mix ValueTracker shifts v = 20[S]/(km_mix+[S]) and half-speed mark 4->8.5->1.8->4 mM.
  s12_return             : Full world returns with all 3 computed curves solid; each mode highlights its slot,
                           plaza clamping pattern, and computed Km/Vmax shift in sync with narration.
"""

from bp_parts import *

# ---------------------------------------------------------------------------
# Colour map & constants
# ---------------------------------------------------------------------------
MAGENTA = "#E056C1"

VMAX = 60.0
KM = 4.0
FACTOR = 3.0  # dose factor 1 + [I]/Ki = 3


def v_base(s):
    return VMAX * s / (KM + s)


def v_comp(s):
    return VMAX * s / (FACTOR * KM + s)


def v_uncomp(s):
    return VMAX * s / (KM + FACTOR * s)


def v_noncomp(s):
    return (VMAX / FACTOR) * s / (KM + s)


def v_mixed(s, km_app, vmax_app=20.0):
    return vmax_app * s / (km_app + s)


# Standard layout boxes: (x0, x1, y0, y1)
PLAZA_45 = (-6.4, -0.55, -2.60, 2.10)
PLOT_55  = (0.75, 6.20, -2.05, 2.05)

PLAZA_60 = (-6.4, 0.85, -2.60, 2.15)
PLOT_40  = (1.95, 6.25, -1.80, 1.95)

PLAZA_38 = (-6.4, -1.70, -2.60, 2.15)
PLOT_60  = (-0.30, 6.20, -2.05, 2.25)

PLAZA_50 = (-6.4, -0.35, -2.60, 2.15)
PLOT_50  = (0.85, 6.20, -1.95, 2.15)
PLOT_50_PREDICT = (0.85, 6.20, -1.75, 2.15)


# ---------------------------------------------------------------------------
# Computed plot builder
# ---------------------------------------------------------------------------
def build_mm_plot(box, show_ceiling=True, show_blue=True, label_size=26, tick_size=22):
    """Build the Michaelis-Menten axes, blue base curve, and Vmax = 60 dashed ceiling."""
    P = Plot(
        box=box,
        xr=(0, 40),
        yr=(0, 66),
        xticks=[0, 10, 20, 30, 40],
        yticks=[0, 20, 40, 60],
        xlabel="[S] (mM)",
        ylabel="initial velocity (µmol/min)",
        color=GREY,
        size=tick_size,
        label_size=label_size,
    )
    P.tick_labels.set_color(TEXT)
    if P.xlabel:
        P.xlabel.set_color(TEXT)
    if P.ylabel:
        P.ylabel.set_color(TEXT)

    if show_blue:
        blue_curve = P.curve(v_base, color=BLUE, width=5.5)
    else:
        blue_curve = None

    if show_ceiling:
        a, b = P.pt(0, VMAX), P.pt(40, VMAX)
        ceil_line = DashedLine(a, b, color=BLUE, stroke_width=2.8, dash_length=0.14)
        ceil_lab = M("Vmax = 60", size=22, color=BLUE).next_to(b, UP, buff=0.08).align_to(b, RIGHT)
        ceiling = VGroup(ceil_line, ceil_lab)
    else:
        ceiling = None

    return P, blue_curve, ceiling


def dashed_curve(P, fn, color=MAGENTA, width=4.5, opacity=1.0):
    c = P.curve(fn, color=color, width=width, opacity=opacity)
    return DashedVMobject(c, num_dashes=28, dashed_ratio=0.55).set_stroke(color=color, width=width, opacity=opacity)


def drop_lines(P, x_val, y_val, color=BLUE, width=2.8):
    p_bot = P.pt(x_val, 0)
    p_top = P.pt(x_val, y_val)
    p_left = P.pt(0, y_val)
    vline = DashedLine(p_bot, p_top, color=color, stroke_width=width, dash_length=0.10)
    hline = DashedLine(p_left, p_top, color=color, stroke_width=width, dash_length=0.10)
    dot = Dot(p_top, radius=0.09, color=color, stroke_color=TEXT, stroke_width=2)
    return VGroup(vline, hline, dot)


def make_clamp_token(color=MAGENTA):
    """Floating 'I' clamp token with dark BG fill so 'I' is always legible."""
    box = RoundedRectangle(
        corner_radius=0.09, width=0.44, height=0.36,
        stroke_color=color, stroke_width=2.6, fill_color=BG, fill_opacity=0.95,
    )
    txt = M("I", size=22, color=color).move_to(box)
    return VGroup(box, txt)


# ---------------------------------------------------------------------------
# Toll Plaza Simulation (computed enzyme-kinetics state machine)
# ---------------------------------------------------------------------------
class TollPlaza(VGroup):
    """6-lane (or 2-lane) schematic enzyme toll plaza with live kinetics updaters."""

    def __init__(
        self,
        box,
        n_booths=6,
        seed=7,
        s_conc=12.0,
        mode="normal",
        clamped_mask=None,
        clamp_style=None,   # None, "doorway", "side"
        side_weights=None,  # optional (empty_scale, busy_scale) for mixed inhibition
        show_booth_labels=True,
        compact=False,
    ):
        super().__init__()
        self.x0, self.x1, self.y0, self.y1 = box
        self.n_booths = n_booths
        self.rng = np.random.default_rng(seed)
        self.mode = mode
        self.compact = compact
        self.show_booth_labels = show_booth_labels

        if isinstance(s_conc, ValueTracker):
            self.s_tracker = s_conc
        else:
            self.s_tracker = ValueTracker(float(s_conc))

        w = self.x1 - self.x0

        # Horizontal layout inside box
        self.x_in = self.x0 + 0.25
        self.bx = self.x0 + 0.57 * w
        self.bw = min(1.42, 0.25 * w) if not compact else min(1.24, 0.27 * w)
        self.bh = 0.40
        self.x_door = self.bx - self.bw / 2
        self.x_exit = self.bx + self.bw / 2
        self.x_out = self.x1 - 0.22

        # Vertical lane y positions: keep clear gaps (dy >= 0.88 for 6 booths)
        if n_booths == 6:
            ys = np.linspace(self.y1 - 0.36, self.y0 + 0.36, 6)
        elif n_booths == 2:
            cy = (self.y0 + self.y1) / 2
            ys = np.array([cy + 0.68, cy - 0.68])
        else:
            ys = np.linspace(self.y1 - 0.45, self.y0 + 0.45, n_booths)
        self.ys = ys

        # Clamp mask: list of None / "EI" / "ESI" per booth
        if clamped_mask is None:
            clamped_mask = [None] * n_booths
        self.clamped_mask = list(clamped_mask)
        self.clamp_style = clamp_style
        self.side_weights = side_weights or (1.0, 1.0)

        # State per booth: "E", "ES", "EI", "ESI"
        self.booth_states = []
        self.booth_timers = []
        s0 = self.s_tracker.get_value()
        p_busy = s0 / (KM + s0)
        for i in range(n_booths):
            cm = self.clamped_mask[i]
            if cm in ("EI", "ESI"):
                st = cm
            else:
                st = "ES" if (i % 2 == 0 and self.rng.random() < p_busy + 0.15) else "E"
            self.booth_states.append(st)
            self.booth_timers.append(float(self.rng.uniform(0.3, 1.4)))

        # Per-lane arrival cooldowns so high [S] populates all lanes evenly
        self.lane_cds = [float(self.rng.uniform(0.05, 0.55)) for _ in range(n_booths)]

        # Build static lane strips + return guides + booths
        self.lane_strips = VGroup()
        self.booth_boxes = VGroup()
        self.gates = VGroup()
        self.pockets = VGroup()
        self.state_labels = []
        self.clamp_mobs = []

        for i, y in enumerate(ys):
            in_strip = Rectangle(
                width=max(0.4, self.x_door - self.x_in + 0.15),
                height=0.38,
                stroke_width=0,
                fill_color=GREY,
                fill_opacity=0.11,
            ).move_to([(self.x_in + self.x_door) / 2, y, 0])
            out_strip = Rectangle(
                width=max(0.4, self.x_out - self.x_exit + 0.15),
                height=0.38,
                stroke_width=0,
                fill_color=GREY,
                fill_opacity=0.11,
            ).move_to([(self.x_exit + self.x_out) / 2, y, 0])
            # Return loop guide placed below returning car corridor
            ret_y = y - 0.38
            ret_guide = Line(
                [self.x_door - 0.72, ret_y - 0.16, 0],
                [self.x_in + 0.15, ret_y - 0.16, 0],
                color=GREY,
                stroke_width=1.6,
                stroke_opacity=0.45,
            )
            ret_tip = Triangle(
                color=GREY, fill_color=GREY, fill_opacity=0.45, stroke_width=0
            ).scale(0.06).rotate(PI / 2).move_to([self.x_in + 0.15, ret_y - 0.16, 0])
            self.lane_strips.add(in_strip, out_strip, ret_guide, ret_tip)

            box_m = RoundedRectangle(
                corner_radius=0.10,
                width=self.bw,
                height=self.bh,
                stroke_color=BLUE,
                stroke_width=2.8,
                fill_color=BLUE,
                fill_opacity=0.18,
            ).move_to([self.bx, y, 0])
            self.booth_boxes.add(box_m)

            gate = Line([self.x_door, y - 0.16, 0], [self.x_door, y + 0.16, 0], color=GREEN, stroke_width=4)
            self.gates.add(gate)

            pocket = RoundedRectangle(
                corner_radius=0.08,
                width=0.34,
                height=0.24,
                stroke_width=0,
                fill_color=YELLOW,
                fill_opacity=0.0,
            ).move_to([self.bx - self.bw * 0.25, y, 0])
            self.pockets.add(pocket)

            lbl = M("E", size=22 if compact else 24, color=BLUE).move_to([self.bx + self.bw * 0.16, y, 0])
            self.state_labels.append(lbl)

            c_mob = self._make_clamp_mob(i, y)
            self.clamp_mobs.append(c_mob)

        self.add(self.lane_strips, self.booth_boxes, self.gates, self.pockets)
        for lbl in self.state_labels:
            if show_booth_labels:
                self.add(lbl)
        for cm in self.clamp_mobs:
            self.add(cm)

        # Car pools
        self.cars_in = []
        self.cars_ret = []
        self.cars_out = []
        self._init_cars()

        self.dim_factor = 1.0
        self._refresh_booth_visuals()

    def _make_clamp_mob(self, i, y):
        """Create a MAGENTA clamp badge 'I' with dark BG fill so 'I' is always legible."""
        c_box = RoundedRectangle(
            corner_radius=0.09,
            width=0.44,
            height=0.30,
            stroke_color=MAGENTA,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.95,
        )
        c_txt = M("I", size=22, color=MAGENTA).move_to(c_box)
        prong = Line([0, 0, 0], [0.12, 0, 0], color=MAGENTA, stroke_width=4)
        g = VGroup(prong, c_box, c_txt)
        g._c_box, g._c_txt, g._prong = c_box, c_txt, prong
        self._position_clamp(g, i, y, self.clamped_mask[i])
        return g

    def _position_clamp(self, g, i, y, state, scale_fac=1.0):
        g._c_box.set_width(0.44 * scale_fac).set_height(0.30 * scale_fac)
        if state == "EI" and self.clamp_style != "side":
            cx = self.x_door - 0.30
            g._c_box.move_to([cx, y, 0])
            g._c_txt.move_to(g._c_box)
            g._prong.put_start_and_end_on([cx + 0.22 * scale_fac, y, 0], [self.x_door + 0.02, y, 0])
        else:
            cx = self.bx + 0.16
            cy = y + self.bh / 2 + 0.17
            g._c_box.move_to([cx, cy, 0])
            g._c_txt.move_to(g._c_box)
            g._prong.put_start_and_end_on([cx, cy - 0.15 * scale_fac, 0], [cx, y + self.bh / 2 - 0.01, 0])

    def _make_car(self, letter, color):
        """Bright filled car pill with high-contrast dark letter."""
        pill = RoundedRectangle(
            corner_radius=0.08,
            width=0.44,
            height=0.29,
            stroke_color=color,
            stroke_width=1.5,
            fill_color=color,
            fill_opacity=0.92,
        )
        txt = M(letter, size=22, color=BG).move_to(pill)
        g = VGroup(pill, txt)
        g._pill, g._txt, g._color = pill, txt, color
        self._set_car_vis(g, 0.0)
        return g

    def _set_car_vis(self, g, alpha):
        if alpha <= 0.01:
            g._pill.set_fill(g._color, opacity=0.0).set_stroke(g._color, opacity=0.0)
            g._txt.set_opacity(0.0)
        else:
            g._pill.set_fill(g._color, opacity=0.92 * alpha).set_stroke(g._color, opacity=1.0 * alpha)
            g._txt.set_opacity(1.0 * alpha)

    def _init_cars(self):
        for k in range(14):
            m = self._make_car("S", YELLOW)
            self.cars_in.append({"mob": m, "active": False, "lane": k % self.n_booths, "x": self.x_in})
            self.add(m)
        for k in range(8):
            m = self._make_car("S", YELLOW)
            self.cars_ret.append({"mob": m, "active": False, "lane": k % self.n_booths, "t": 0.0})
            self.add(m)
        for k in range(10):
            m = self._make_car("P", GREEN)
            self.cars_out.append({"mob": m, "active": False, "lane": k % self.n_booths, "x": self.x_exit, "speed": 1.85})
            self.add(m)

        # Pre-seed initial cars
        for idx in range(min(4, self.n_booths)):
            c = self.cars_in[idx]
            c["active"] = True
            c["lane"] = (idx * 2 + 1) % self.n_booths
            c["x"] = self.x_in + 0.55 * idx
            c["mob"].move_to([c["x"], self.ys[c["lane"]], 0])
            self._set_car_vis(c["mob"], 1.0)
        if self.n_booths >= 2:
            p0 = self.cars_out[0]
            p0["active"] = True
            p0["lane"] = 0
            p0["x"] = self.x_exit + 0.55
            p0["mob"].move_to([p0["x"], self.ys[0], 0])
            self._set_car_vis(p0["mob"], 1.0)

    def _set_clamp_vis(self, cm, active, stroke_col=MAGENTA, stroke_w=2.5, alpha=1.0):
        if not active:
            cm._c_box.set_stroke(MAGENTA, width=0, opacity=0.0).set_fill(BG, opacity=0.0)
            cm._c_txt.set_opacity(0.0)
            cm._prong.set_stroke(MAGENTA, opacity=0.0)
        else:
            cm._c_box.set_stroke(stroke_col, width=stroke_w, opacity=alpha).set_fill(BG, opacity=0.95 * alpha)
            cm._c_txt.set_color(stroke_col).set_opacity(alpha)
            cm._prong.set_stroke(stroke_col, width=4, opacity=alpha)

    def _refresh_booth_visuals(self):
        df = self.dim_factor
        for i in range(self.n_booths):
            st = self.booth_states[i]
            y = self.ys[i]
            box = self.booth_boxes[i]
            gate = self.gates[i]
            pocket = self.pockets[i]
            lbl = self.state_labels[i]
            cm = self.clamp_mobs[i]

            if st == "E":
                box.set_stroke(BLUE, width=2.8, opacity=0.95 * df).set_fill(BLUE, opacity=0.18 * df)
                gate.put_start_and_end_on([self.x_door - 0.14, y + 0.18, 0], [self.x_door, y + 0.18, 0])
                gate.set_stroke(GREEN, width=4, opacity=0.95 * df)
                pocket.set_fill(YELLOW, opacity=0.0)
                if self.show_booth_labels:
                    new_lbl = M("E", size=22 if self.compact else 24, color=BLUE).move_to([self.bx + self.bw * 0.16, y, 0])
                    lbl.become(new_lbl).set_opacity(df)
                self._set_clamp_vis(cm, False)
            elif st == "ES":
                box.set_stroke(BLUE, width=2.8, opacity=0.95 * df).set_fill(BLUE, opacity=0.28 * df)
                gate.put_start_and_end_on([self.x_door, y - 0.15, 0], [self.x_door, y + 0.15, 0])
                gate.set_stroke(YELLOW, width=4, opacity=0.95 * df)
                pocket.set_fill(YELLOW, opacity=0.95 * df)
                if self.show_booth_labels:
                    new_lbl = M("ES", size=22 if self.compact else 24, color=YELLOW).move_to([self.bx + self.bw * 0.16, y, 0])
                    lbl.become(new_lbl).set_opacity(df)
                self._set_clamp_vis(cm, False)
            elif st == "EI":
                box.set_stroke(BLUE, width=2.2, opacity=0.45 * df).set_fill(BLUE, opacity=0.07 * df)
                gate.put_start_and_end_on([self.x_door, y - 0.15, 0], [self.x_door, y + 0.15, 0])
                gate.set_stroke(MAGENTA, width=4, opacity=0.90 * df)
                pocket.set_fill(YELLOW, opacity=0.0)
                if self.show_booth_labels:
                    new_lbl = M("EI", size=22 if self.compact else 24, color=MAGENTA).move_to([self.bx + self.bw * 0.16, y, 0])
                    lbl.become(new_lbl).set_opacity(max(0.9, df))
                w_e, _ = self.side_weights
                sc = 1.08 if (self.clamp_style == "side" and w_e > 1.5) else (0.85 if (self.clamp_style == "side" and w_e < 0.8) else 1.0)
                self._position_clamp(cm, i, y, "EI", scale_fac=sc)
                col = GOLD if (self.clamp_style == "side" and w_e > 1.5) else MAGENTA
                sw = 4.5 if (self.clamp_style == "side" and w_e > 1.5) else (1.5 if (self.clamp_style == "side" and w_e < 0.8) else 2.5)
                self._set_clamp_vis(cm, True, stroke_col=col, stroke_w=sw, alpha=max(0.9, df))
            elif st == "ESI":
                box.set_stroke(BLUE, width=2.2, opacity=0.45 * df).set_fill(BLUE, opacity=0.09 * df)
                gate.put_start_and_end_on([self.x_door, y - 0.15, 0], [self.x_door, y + 0.15, 0])
                gate.set_stroke(MAGENTA, width=4, opacity=0.90 * df)
                pocket.set_fill(YELLOW, opacity=0.70 * df)
                if self.show_booth_labels:
                    new_lbl = M("ESI", size=22 if self.compact else 24, color=MAGENTA).move_to([self.bx + self.bw * 0.16, y, 0])
                    lbl.become(new_lbl).set_opacity(max(0.9, df))
                _, w_es = self.side_weights
                sc = 1.08 if (self.clamp_style == "side" and w_es > 1.5) else (0.85 if (self.clamp_style == "side" and w_es < 0.8) else 1.0)
                self._position_clamp(cm, i, y, "ESI", scale_fac=sc)
                col = GOLD if (self.clamp_style == "side" and w_es > 1.5) else MAGENTA
                sw = 4.5 if (self.clamp_style == "side" and w_es > 1.5) else (1.5 if (self.clamp_style == "side" and w_es < 0.8) else 2.5)
                self._set_clamp_vis(cm, True, stroke_col=col, stroke_w=sw, alpha=max(0.9, df))

    def count_empty(self):
        return sum(1 for s in self.booth_states if s == "E")

    def count_busy(self):
        return sum(1 for s in self.booth_states if s == "ES")

    def count_holding_s(self):
        return sum(1 for s in self.booth_states if s in ("ES", "ESI"))

    def set_clamped(self, idx, state):
        self.clamped_mask[idx] = state
        if state is None:
            if self.booth_states[idx] in ("EI", "ESI"):
                self.booth_states[idx] = "ES" if self.booth_states[idx] == "ESI" else "E"
                self.booth_timers[idx] = 0.8
        else:
            self.booth_states[idx] = state
        self._refresh_booth_visuals()

    def step(self, dt):
        if dt <= 0:
            return
        dt = min(dt, 0.08)
        s_val = float(self.s_tracker.get_value())
        # Per-lane arrival interval scales inversely with [S]
        lane_interval = float(np.clip(2.4 / (0.6 + s_val / 6.0), 0.45, 2.2))
        speed_in = 1.65 + 0.025 * s_val

        # 1. Booth turnover timers
        for i in range(self.n_booths):
            if self.booth_states[i] == "ES":
                self.booth_timers[i] -= dt
                if self.booth_timers[i] <= 0:
                    self.booth_states[i] = "E"
                    self.booth_timers[i] = 1.15
                    for p in self.cars_out:
                        if not p["active"]:
                            p["active"] = True
                            p["lane"] = i
                            p["x"] = self.x_exit + 0.22
                            p["mob"].move_to([p["x"], self.ys[i], 0])
                            self._set_car_vis(p["mob"], self.dim_factor)
                            break

        # 2. Per-lane spawning of incoming S cars
        for lane in range(self.n_booths):
            self.lane_cds[lane] -= dt
            if self.lane_cds[lane] <= 0:
                self.lane_cds[lane] = lane_interval * float(self.rng.uniform(0.8, 1.25))
                too_close = any(
                    c["active"] and c["lane"] == lane and (c["x"] - self.x_in) < 0.78
                    for c in self.cars_in
                )
                if not too_close:
                    for c in self.cars_in:
                        if not c["active"]:
                            c["active"] = True
                            c["lane"] = lane
                            c["x"] = self.x_in
                            c["mob"].move_to([c["x"], self.ys[lane], 0])
                            self._set_car_vis(c["mob"], self.dim_factor)
                            break

        # 3. Move incoming S cars (reject BEFORE reaching doorway clamp!)
        x_check = self.x_door - 0.80
        for c in self.cars_in:
            if not c["active"]:
                continue
            c["x"] += speed_in * dt
            y = self.ys[c["lane"]]
            if c["x"] >= x_check:
                st = self.booth_states[c["lane"]]
                if st == "E":
                    self.booth_states[c["lane"]] = "ES"
                    self.booth_timers[c["lane"]] = float(self.rng.uniform(0.95, 1.35))
                    c["active"] = False
                    self._set_car_vis(c["mob"], 0.0)
                else:
                    # Only spawn return car if none nearby at start of return loop
                    ret_busy = any(r["active"] and r["lane"] == c["lane"] and r["t"] < 0.45 for r in self.cars_ret)
                    c["active"] = False
                    self._set_car_vis(c["mob"], 0.0)
                    if not ret_busy:
                        for r in self.cars_ret:
                            if not r["active"]:
                                r["active"] = True
                                r["lane"] = c["lane"]
                                r["t"] = 0.0
                                r["mob"].move_to([x_check, y, 0])
                                self._set_car_vis(r["mob"], self.dim_factor)
                                break
            else:
                c["mob"].move_to([c["x"], y, 0])
                self._set_car_vis(c["mob"], self.dim_factor)

        # 4. Move returning S cars along smooth U-turn and back at y - 0.38 (clean gap from y)
        for r in self.cars_ret:
            if not r["active"]:
                continue
            r["t"] += dt * 1.45
            y0 = self.ys[r["lane"]]
            if r["t"] < 0.30:
                a = r["t"] / 0.30
                ang = a * PI
                cx = x_check - 0.16 * np.sin(ang)
                cy = y0 - 0.38 * (1 - np.cos(ang)) / 2
                r["mob"].move_to([cx, cy, 0])
                self._set_car_vis(r["mob"], self.dim_factor)
            elif r["t"] < 1.15:
                a = (r["t"] - 0.30) / 0.85
                cx = x_check - a * (x_check - self.x_in)
                cy = y0 - 0.38
                r["mob"].move_to([cx, cy, 0])
                self._set_car_vis(r["mob"], self.dim_factor)
            else:
                r["active"] = False
                self._set_car_vis(r["mob"], 0.0)

        # 5. Move outgoing P cars
        for p in self.cars_out:
            if not p["active"]:
                continue
            p["x"] += p["speed"] * dt
            if p["x"] >= self.x_out:
                p["active"] = False
                self._set_car_vis(p["mob"], 0.0)
            else:
                p["mob"].move_to([p["x"], self.ys[p["lane"]], 0])
                self._set_car_vis(p["mob"], self.dim_factor)

        self._refresh_booth_visuals()

    def start_live(self):
        return self.add_updater(lambda m, dt: m.step(dt))

    def stop_live(self):
        self.clear_updaters()
        for c in self.cars_in + self.cars_ret + self.cars_out:
            self._set_car_vis(c["mob"], 0.0)
        return self


# ---------------------------------------------------------------------------
# Scene 0: s00_link_and_question (16.05 s)
# ---------------------------------------------------------------------------
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        plaza = TollPlaza(PLAZA_45, n_booths=6, seed=7, s_conc=ValueTracker(2.0), compact=True)
        P, blue_c, ceil = build_mm_plot(PLOT_55, label_size=24)
        stag = scope_tag("booth count schematic", size=22, color=GREY)

        s_tr = plaza.s_tracker
        # Dot on blue curve + booth icon sitting cleanly above the dot (never straddling the curve)
        curve_dot = always_redraw(lambda: Dot(P.pt(s_tr.get_value(), v_base(s_tr.get_value())),
                                              radius=0.08, color=BLUE, stroke_color=TEXT, stroke_width=2))
        rider_box = RoundedRectangle(corner_radius=0.07, width=0.38, height=0.28,
                                     stroke_color=BLUE, stroke_width=2.4, fill_color=BG, fill_opacity=0.95)
        rider_lbl = M("E", size=22, color=BLUE).move_to(rider_box)
        rider = VGroup(rider_box, rider_lbl)
        rider.add_updater(lambda m: m.move_to(P.pt(s_tr.get_value(), v_base(s_tr.get_value())) + UP * 0.25))

        self.add(plaza, P, blue_c, ceil, stag, curve_dot, rider)
        plaza.start_live()

        self.play(s_tr.animate.set_value(24.0), run_time=6.4, rate_func=linear)

        # On "add an inhibitor": MAGENTA clamp tokens drop cleanly from above the clamp target (never crossing S cars)
        self.at("add an inhibitor")
        clamps_fly = []
        for idx in (1, 3, 5):
            tx = (plaza.x_door - 0.30) if idx != 3 else (plaza.bx + 0.16)
            ty = plaza.ys[idx] if idx != 3 else (plaza.ys[idx] + plaza.bh / 2 + 0.17)
            g = make_clamp_token(MAGENTA).move_to([tx, ty + 0.45, 0])
            clamps_fly.append((idx, tx, ty, g))
        self.play(*[g.animate.move_to([tx, ty, 0]) for _, tx, ty, g in clamps_fly], run_time=0.75)
        for idx, _, _, g in clamps_fly:
            self.remove(g)
            plaza.set_clamped(idx, "EI" if idx != 3 else "ESI")

        # On "three kinds": three computed MAGENTA dashed curves peel away
        self.at("three kinds")
        c1 = dashed_curve(P, v_comp, color=MAGENTA, width=4.5)
        c2 = dashed_curve(P, v_uncomp, color=MAGENTA, width=4.5)
        c3 = dashed_curve(P, v_noncomp, color=MAGENTA, width=4.5)
        l1 = M("1", size=24, color=MAGENTA).next_to(P.pt(33, v_comp(33)), UP, buff=0.14)
        l2 = M("2", size=24, color=MAGENTA).next_to(P.pt(9, v_uncomp(9)), UP, buff=0.14)
        l3 = M("3", size=24, color=MAGENTA).next_to(P.pt(22, v_noncomp(22)), DOWN, buff=0.14)
        self.play(Create(c1), Create(c2), Create(c3), run_time=2.2)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(l3), run_time=0.45)

        # On "Why?": dim plaza gently (keep cars & clamps moving!) and show question in top band
        self.at("Why")
        plaza.dim_factor = 0.55
        q_txt = T("Three inhibitors, three shapes. Why?", size=30, color=TEXT).move_to([3.3, 3.10, 0])
        fit(q_txt, max_w=6.2)
        self.play(FadeIn(q_txt), run_time=0.5)

        self.finish()


# ---------------------------------------------------------------------------
# Scene 1: s01_title (2.0 s silent)
# ---------------------------------------------------------------------------
class S01Title(NarratedScene):
    def construct(self):
        plaza = TollPlaza(PLAZA_45, n_booths=6, seed=8, s_conc=20.0, clamped_mask=[None, "EI", None, "ESI", None, "EI"], compact=True)
        plaza.dim_factor = 0.55
        P, blue_c, ceil = build_mm_plot(PLOT_55, label_size=24)
        c1 = dashed_curve(P, v_comp, color=MAGENTA, width=4.5)
        c2 = dashed_curve(P, v_uncomp, color=MAGENTA, width=4.5)
        c3 = dashed_curve(P, v_noncomp, color=MAGENTA, width=4.5)
        l1 = M("1", size=24, color=MAGENTA).next_to(P.pt(33, v_comp(33)), UP, buff=0.14)
        l2 = M("2", size=24, color=MAGENTA).next_to(P.pt(9, v_uncomp(9)), UP, buff=0.14)
        l3 = M("3", size=24, color=MAGENTA).next_to(P.pt(22, v_noncomp(22)), DOWN, buff=0.14)
        q_txt = T("Three inhibitors, three shapes. Why?", size=30, color=TEXT).move_to([3.3, 3.10, 0])
        fit(q_txt, max_w=6.2)

        # Title sits cleanly in the open top band (y ~ 3.10), zero overlap with plaza or graph
        title = T("Empty, Busy, or Both", size=44, font=TITLE_FONT, color=TEXT).move_to([0, 3.18, 0])
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.14)
        title_grp = VGroup(title, rule)

        self.add(plaza, P, blue_c, ceil, c1, c2, c3, l1, l2, l3, q_txt)
        plaza.start_live()

        def brighten(mob, alpha):
            mob.dim_factor = 0.55 + 0.45 * alpha

        self.play(
            FadeOut(q_txt),
            FadeOut(l1), FadeOut(l2), FadeOut(l3),
            c1.animate.set_stroke(opacity=0.22),
            c2.animate.set_stroke(opacity=0.22),
            c3.animate.set_stroke(opacity=0.22),
            UpdateFromAlphaFunc(plaza, brighten),
            FadeIn(title_grp, shift=UP * 0.08),
            run_time=0.65,
        )
        self.wait(0.9)
        self.play(FadeOut(title_grp), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 2: s02_pools (16.375 s)
# ---------------------------------------------------------------------------
class S02Pools(SpokenScene):
    def construct(self):
        plaza = TollPlaza(PLAZA_60, n_booths=6, seed=11, s_conc=12.0)
        P, blue_c, ceil = build_mm_plot(PLOT_40, label_size=22, tick_size=22)
        g1 = dashed_curve(P, v_comp, color=MAGENTA, width=3, opacity=0.22)
        g2 = dashed_curve(P, v_uncomp, color=MAGENTA, width=3, opacity=0.22)
        g3 = dashed_curve(P, v_noncomp, color=MAGENTA, width=3, opacity=0.22)
        stag = scope_tag("schematic", size=24, color=GREY)

        empty_box = RoundedRectangle(corner_radius=0.12, width=2.5, height=0.72,
                                     stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.15).move_to([-4.6, 2.95, 0])
        busy_box = RoundedRectangle(corner_radius=0.12, width=2.5, height=0.72,
                                    stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.15).move_to([-1.4, 2.95, 0])
        empty_lbl = always_redraw(lambda: T(f"empty: {plaza.count_empty()}", size=28, color=BLUE).move_to(empty_box))
        busy_lbl = always_redraw(lambda: T(f"busy: {plaza.count_busy()}", size=28, color=YELLOW).move_to(busy_box))

        self.add(plaza, P, blue_c, ceil, g1, g2, g3, stag, empty_box, busy_box, empty_lbl, busy_lbl)
        plaza.start_live()

        # On "empty enzyme": latch doorway clamp onto an empty booth
        self.at("empty enzyme")
        target_e = next((i for i, s in enumerate(plaza.booth_states) if s == "E"), 0)
        tok_e = make_clamp_token(MAGENTA).move_to([plaza.x_door - 0.30, plaza.ys[target_e] + 0.42, 0])
        self.play(tok_e.animate.move_to([plaza.x_door - 0.30, plaza.ys[target_e], 0]), run_time=0.65)
        self.remove(tok_e)
        plaza.set_clamped(target_e, "EI")

        # On "busy enzyme": latch side clamp onto a busy booth
        self.at("busy enzyme")
        target_b = next((i for i, s in enumerate(plaza.booth_states) if s == "ES" and i != target_e), (target_e + 1) % 6)
        plaza.booth_states[target_b] = "ES"
        tok_b = make_clamp_token(MAGENTA).move_to([plaza.bx + 1.1, plaza.ys[target_b] + plaza.bh / 2 + 0.17, 0])
        self.play(tok_b.animate.move_to([plaza.bx + 0.16, plaza.ys[target_b] + plaza.bh / 2 + 0.17, 0]), run_time=0.6)
        self.remove(tok_b)
        plaza.set_clamped(target_b, "ESI")

        # On "or both": latch another pair at once
        self.at("or both")
        avail = [i for i in range(6) if i not in (target_e, target_b)]
        plaza.set_clamped(avail[0], "EI")
        plaza.set_clamped(avail[1], "ESI")
        self.wait(0.6)

        # On "makes no product": note placed well below [S] (mM) in bottom band
        self.at("makes no product")
        note = T("tied-up = no P", size=28, color=MAGENTA).move_to([-2.8, -3.15, 0])
        self.play(FadeIn(note), run_time=0.4)

        # On "come off again": one clamp lifts away and booth resumes cycling
        self.at("come off again")
        lift_y = plaza.ys[target_e]
        plaza.set_clamped(target_e, None)
        lift_tok = make_clamp_token(MAGENTA).move_to([plaza.x_door - 0.30, lift_y, 0])
        self.play(lift_tok.animate.shift(LEFT * 0.8 + UP * 0.4).set_opacity(0), FadeOut(note), run_time=0.8)
        self.remove(lift_tok)

        self.finish()


# ---------------------------------------------------------------------------
# Scene 3: s03_competitive (13.075 s)
# ---------------------------------------------------------------------------
class S03Competitive(SpokenScene):
    def construct(self):
        plaza = TollPlaza(PLAZA_60, n_booths=6, seed=13, s_conc=10.0, clamp_style="doorway")
        P, blue_c, ceil = build_mm_plot(PLOT_40, label_size=22, tick_size=22)
        g1 = dashed_curve(P, v_comp, color=MAGENTA, width=3, opacity=0.22)
        g2 = dashed_curve(P, v_uncomp, color=MAGENTA, width=3, opacity=0.22)
        g3 = dashed_curve(P, v_noncomp, color=MAGENTA, width=3, opacity=0.22)

        head = T("competitive: grabs empty", size=32, color=MAGENTA).move_to([-2.8, 3.05, 0])
        stag = scope_tag("schematic", size=24, color=GREY)

        self.add(plaza, P, blue_c, ceil, g1, g2, g3, stag)
        plaza.start_live()

        self.at("grabs only empty")
        empty_idxs = [i for i, s in enumerate(plaza.booth_states) if s == "E"]
        if len(empty_idxs) < 2:
            plaza.booth_states[0] = "E"
            plaza.booth_states[3] = "E"
            empty_idxs = [0, 3]
        pick_e = empty_idxs[:2]
        toks = []
        for idx in pick_e:
            t = make_clamp_token(MAGENTA).move_to([plaza.x_door - 0.30, plaza.ys[idx] + 0.42, 0])
            toks.append((idx, t))
        self.play(*[t.animate.move_to([plaza.x_door - 0.30, plaza.ys[idx], 0]) for idx, t in toks], run_time=0.75)
        for idx, t in toks:
            self.remove(t)
            plaza.set_clamped(idx, "EI")

        self.at("active site")
        busy_idx = next((i for i, s in enumerate(plaza.booth_states) if s == "ES"), 1)
        plaza.booth_states[busy_idx] = "ES"
        plaza.booth_timers[busy_idx] = 2.0
        by = plaza.ys[busy_idx]
        bouncer = make_clamp_token(MAGENTA).move_to([plaza.x_door - 1.0, by + 0.32, 0])
        self.play(bouncer.animate.move_to([plaza.x_door - 0.26, by, 0]), run_time=0.45)
        self.play(bouncer.animate.move_to([plaza.x_door - 1.2, by + 0.45, 0]).set_opacity(0), run_time=0.55)
        self.remove(bouncer)

        self.at("cannot bind")
        plaza.set_clamped(pick_e[0], None)
        next_e = next((i for i, s in enumerate(plaza.booth_states) if s == "E" and i != pick_e[0]), pick_e[1])
        plaza.set_clamped(next_e, "EI")

        self.at("competitive inhibition")
        self.play(FadeIn(head), run_time=0.5)

        self.finish()


# ---------------------------------------------------------------------------
# Scene 4: s04_competitive_effect (23.525 s)
# ---------------------------------------------------------------------------
class S04CompetitiveEffect(SpokenScene):
    def construct(self):
        plaza = TollPlaza(
            PLAZA_38, n_booths=6, seed=17, s_conc=ValueTracker(8.0),
            clamped_mask=[None, "EI", None, "EI", None, None], clamp_style="doorway", compact=True
        )
        P, blue_c, ceil = build_mm_plot(PLOT_60, label_size=26, tick_size=22)
        stag = scope_tag("schematic", size=22, color=GREY)

        comp_curve = P.curve(v_comp, color=MAGENTA, width=5.5)
        blue_km = drop_lines(P, KM, 30.0, color=BLUE, width=2.8)
        blue_km_lbl = M("Km: 4", size=24, color=BLUE).next_to(P.pt(KM, 0), UP, buff=0.22).shift(RIGHT * 0.65)

        km_tr = ValueTracker(4.0)
        mag_km = always_redraw(lambda: drop_lines(P, km_tr.get_value(), 30.0, color=MAGENTA, width=3.0))
        app_lbl = M("apparent Km: 12", size=24, color=MAGENTA).next_to(P.pt(12.0, 30.0), DR, buff=0.14)
        head = T("competitive: Km rises, Vmax unchanged", size=28, color=MAGENTA).move_to([2.9, 3.05, 0])

        self.add(plaza, P, blue_c, ceil, blue_km, blue_km_lbl, stag)
        plaza.start_live()
        self.play(Create(comp_curve), run_time=1.4)

        self.at("from 4")
        self.add(mag_km)
        self.play(km_tr.animate.set_value(12.0), run_time=2.2, rate_func=smooth)

        self.at("apparent Km")
        self.play(FadeIn(app_lbl), FadeIn(head), run_time=0.45)

        self.at("own Km has not changed")
        ring_km = Circle(radius=0.22, color=BLUE, stroke_width=4).move_to(P.pt(KM, 30.0))
        self.play(Create(ring_km), run_time=0.35)
        self.play(FadeOut(ring_km), run_time=0.45)

        # High substrate: dense yellow stream fills plaza, clamps release, dot traces to Vmax=60
        self.at("very high substrate")
        s_dot_tr = ValueTracker(12.0)
        hi_dot = always_redraw(lambda: Dot(
            P.pt(s_dot_tr.get_value(), v_comp(s_dot_tr.get_value())),
            radius=0.11, color=MAGENTA, stroke_color=TEXT, stroke_width=2.5
        ))
        # Place "Vmax unchanged" cleanly above the Vmax=60 dashed line, clear of Vmax=60 on right
        vmax_lbl = M("Vmax unchanged", size=24, color=BLUE).next_to(P.pt(14.0, 60.0), UP, buff=0.10)
        self.add(hi_dot)
        plaza.set_clamped(1, None)
        plaza.set_clamped(3, None)
        self.play(
            plaza.s_tracker.animate.set_value(40.0),
            s_dot_tr.animate.set_value(39.0),
            run_time=4.2,
            rate_func=linear,
        )

        self.at("stays 60")
        self.play(FadeIn(vmax_lbl), run_time=0.4)

        self.finish()


# ---------------------------------------------------------------------------
# Scene 5: s05_uncompetitive (16.975 s)
# ---------------------------------------------------------------------------
class S05Uncompetitive(SpokenScene):
    def construct(self):
        plaza = TollPlaza(PLAZA_60, n_booths=6, seed=19, s_conc=10.0, clamp_style="side")
        P, blue_c, ceil = build_mm_plot(PLOT_40, label_size=22, tick_size=22)
        g1 = dashed_curve(P, v_comp, color=MAGENTA, width=3, opacity=0.22)
        stag = scope_tag("schematic", size=24, color=GREY)

        # Put heading left above plaza and live counter above right plot (no touch, no small font!)
        head = T("uncompetitive: grabs busy", size=30, color=MAGENTA).move_to([-2.9, 2.95, 0])
        hold_box = RoundedRectangle(corner_radius=0.12, width=3.3, height=0.62,
                                    stroke_color=YELLOW, stroke_width=2.2, fill_color=YELLOW, fill_opacity=0.14).move_to([4.1, 2.95, 0])
        hold_lbl = always_redraw(lambda: T(f"holding S: {plaza.count_holding_s()} / 6", size=24, color=YELLOW).move_to(hold_box))

        self.add(plaza, P, blue_c, ceil, g1, stag, hold_box, hold_lbl)
        plaza.start_live()

        plaza.booth_states[0] = "ES"
        plaza.booth_states[2] = "ES"
        plaza.booth_states[1] = "E"
        plaza.booth_states[4] = "E"

        self.at("grabs only busy")
        for idx in (0, 2):
            plaza.booth_states[idx] = "ES"
            tok = make_clamp_token(MAGENTA).move_to([plaza.bx + 1.1, plaza.ys[idx] + plaza.bh / 2 + 0.17, 0])
            self.play(tok.animate.move_to([plaza.bx + 0.16, plaza.ys[idx] + plaza.bh / 2 + 0.17, 0]), run_time=0.55)
            self.remove(tok)
            plaza.set_clamped(idx, "ESI")

        self.at("as ESI")
        empty_i = next((i for i, s in enumerate(plaza.booth_states) if s == "E"), 1)
        plaza.booth_states[empty_i] = "E"
        bouncer = make_clamp_token(MAGENTA).move_to([plaza.bx + 1.1, plaza.ys[empty_i] + plaza.bh / 2 + 0.17, 0])
        self.play(bouncer.animate.move_to([plaza.bx + 0.16, plaza.ys[empty_i] + plaza.bh / 2 + 0.17, 0]), run_time=0.4)
        self.play(bouncer.animate.shift(UP * 0.55 + LEFT * 0.4).set_opacity(0), run_time=0.45)
        self.remove(bouncer)

        self.at("uncompetitive inhibition")
        self.play(FadeIn(head), run_time=0.5)

        self.at("draws more enzyme and substrate")
        plaza.s_tracker.set_value(28.0)
        for idx in (1, 3, 4):
            if plaza.booth_states[idx] == "E":
                plaza.booth_states[idx] = "ES"
                plaza.booth_timers[idx] = 3.5
                plaza._refresh_booth_visuals()
                self.wait(0.35)
        plaza.set_clamped(4, "ESI")

        self.finish()


# ---------------------------------------------------------------------------
# Scene 6: s06_uncompetitive_effect (15.55 s)
# ---------------------------------------------------------------------------
class S06UncompetitiveEffect(SpokenScene):
    def construct(self):
        plaza = TollPlaza(
            PLAZA_38, n_booths=6, seed=23, s_conc=14.0,
            clamped_mask=["ESI", None, "ESI", None, "ESI", None],
            clamp_style="side", compact=True
        )
        P, blue_c, ceil = build_mm_plot(PLOT_60, label_size=26, tick_size=22)
        stag = scope_tag("schematic", size=22, color=GREY)

        uncomp_curve = P.curve(v_uncomp, color=MAGENTA, width=5.5)
        blue_km = drop_lines(P, KM, 30.0, color=BLUE, width=2.6)
        # Put Km: 4 cleanly between the blue curve and curve 2 so it never crosses apparent Km pointer
        blue_km_lbl = M("Km: 4", size=24, color=BLUE).move_to(P.pt(9.2, 25.5))

        # Slide apparent Km along curve 2 (4 -> 4/3) and drop Vmax ceiling (60 -> 20)
        km_tr = ValueTracker(4.0)
        vmax_tr = ValueTracker(60.0)

        mag_ceil = always_redraw(lambda: DashedLine(
            P.pt(0, vmax_tr.get_value()), P.pt(40, vmax_tr.get_value()),
            color=MAGENTA, stroke_width=3.0, dash_length=0.14
        ))
        # Dot sits ON curve 2 at (km_tr, v_uncomp(km_tr)) as km_tr slides left to 4/3 (where v=10)!
        mag_km = always_redraw(lambda: drop_lines(P, km_tr.get_value(), v_uncomp(km_tr.get_value()), color=MAGENTA, width=3.0))

        self.add(plaza, P, blue_c, ceil, blue_km, blue_km_lbl, stag)
        plaza.start_live()
        self.play(Create(uncomp_curve), run_time=1.3)

        self.at("apparent Km falls")
        self.add(mag_km, mag_ceil)
        self.play(km_tr.animate.set_value(4.0 / 3.0), run_time=1.5, rate_func=smooth)
        # Put apparent Km label in open area under curve 2 (around [S]=16, v=6) with neat pointer to (1.33, 10)
        app_km_lbl = M("apparent Km: ~1.3", size=24, color=MAGENTA).move_to(P.pt(17.5, 6.0))
        app_ptr = Line(app_km_lbl.get_left() + LEFT * 0.08, P.pt(4.0 / 3.0, 10.0), color=MAGENTA, stroke_width=2.0)
        self.play(Create(app_ptr), FadeIn(app_km_lbl), run_time=0.45)

        self.at("stuck")
        stuck_hl = VGroup(*[
            SurroundingRectangle(plaza.booth_boxes[i], color=MAGENTA, buff=0.05, stroke_width=3)
            for i in (0, 2, 4)
        ])
        self.play(FadeIn(stuck_hl), run_time=0.4)
        self.play(FadeOut(stuck_hl), run_time=0.5)

        self.at("Vmax falls too")
        self.play(vmax_tr.animate.set_value(20.0), run_time=1.3, rate_func=smooth)
        vmax20_lbl = M("Vmax: 20", size=24, color=MAGENTA).next_to(P.pt(39.5, 20.0), UP, buff=0.10).align_to(P.pt(39.5, 20.0), RIGHT)
        self.play(FadeIn(vmax20_lbl), run_time=0.35)

        self.at("both fall threefold")
        div_km = M("÷3", size=26, color=GOLD).next_to(app_km_lbl, RIGHT, buff=0.18)
        arr_vm = Arrow(P.pt(35.0, 56.0), P.pt(35.0, 24.0), color=GOLD, stroke_width=3, buff=0)
        div_vm = M("÷3", size=26, color=GOLD).next_to(arr_vm, LEFT, buff=0.12)
        self.play(FadeIn(div_km), GrowArrow(arr_vm), FadeIn(div_vm), run_time=0.6)

        self.finish()


# ---------------------------------------------------------------------------
# Scene 7: s07_guiding_idea (13.55 s)
# ---------------------------------------------------------------------------
class S07GuidingIdea(SpokenScene):
    def construct(self):
        plaza = TollPlaza(PLAZA_50, n_booths=6, seed=29, s_conc=12.0, clamped_mask=[None, "EI", None, "ESI", None, None], compact=True)
        P, blue_c, ceil = build_mm_plot(PLOT_50, label_size=24, tick_size=22)
        g1 = dashed_curve(P, v_comp, color=MAGENTA, width=3.5, opacity=0.22)
        g2 = dashed_curve(P, v_uncomp, color=MAGENTA, width=3.5, opacity=0.22)
        stag = scope_tag("schematic", size=22, color=GREY)

        slot_e = boxed_label("empty", color=BLUE, size=28, box=(1.75, 0.62)).move_to([-5.35, 2.95, 0])
        slot_b = boxed_label("busy", color=YELLOW, size=28, box=(1.75, 0.62)).move_to([-3.35, 2.95, 0])
        slot_both = boxed_label("both", color=MAGENTA, size=28, box=(1.75, 0.62)).move_to([-1.35, 2.95, 0])

        self.add(plaza, P, blue_c, ceil, g1, g2, stag, slot_e, slot_b, slot_both)
        plaza.start_live()

        self.at("empty")
        hl_e = SurroundingRectangle(slot_e, color=GOLD, buff=0.06, stroke_width=3)
        self.play(FadeIn(hl_e), g1.animate.set_stroke(opacity=0.95, width=4.5), run_time=0.45)

        self.at("busy")
        hl_b = SurroundingRectangle(slot_b, color=GOLD, buff=0.06, stroke_width=3)
        self.play(FadeOut(hl_e), FadeIn(hl_b), g1.animate.set_stroke(opacity=0.25, width=3.5), g2.animate.set_stroke(opacity=0.95, width=4.5), run_time=0.45)

        self.at("or both")
        hl_both = SurroundingRectangle(slot_both, color=GOLD, buff=0.06, stroke_width=3)
        q_mark = T("?", size=48, color=GOLD).move_to(P.pt(22, 32))
        self.play(FadeOut(hl_b), FadeIn(hl_both), g2.animate.set_stroke(opacity=0.25, width=3.5), FadeIn(q_mark), run_time=0.45)

        self.at("half speed point")
        km_line = drop_lines(P, KM, 30.0, color=BLUE, width=2.8)
        self.play(FadeIn(km_line), run_time=0.45)

        self.finish()


# ---------------------------------------------------------------------------
# Shared builder for Predict (s08) & Pause (s09)
# ---------------------------------------------------------------------------
def build_s08_world():
    plaza = TollPlaza(
        PLAZA_50,
        n_booths=6,
        seed=31,
        s_conc=14.0,
        clamped_mask=["EI", None, "ESI", "EI", None, "ESI"],
        clamp_style="side",
        compact=True,
    )
    P, blue_c, ceil = build_mm_plot(PLOT_50_PREDICT, label_size=24, tick_size=22)
    g1 = dashed_curve(P, v_comp, color=MAGENTA, width=3, opacity=0.18)
    g2 = dashed_curve(P, v_uncomp, color=MAGENTA, width=3, opacity=0.18)
    km_mark = drop_lines(P, KM, 30.0, color=BLUE, width=2.8)
    km_lbl = M("Km: 4", size=24, color=BLUE).next_to(P.pt(KM, 0), UP, buff=0.22).shift(RIGHT * 0.72)
    head = T("grabs both equally", size=30, color=MAGENTA).move_to([-3.35, 2.95, 0])
    # Place scope tag left of the countdown ring at (6.0, -3.0) so it never touches it
    stag = T("schematic", size=22, color=GREY).move_to([4.35, -3.20, 0])
    plaza.start_live()
    return plaza, VGroup(plaza, P, blue_c, ceil, g1, g2, km_mark, km_lbl, head, stag)


# ---------------------------------------------------------------------------
# Scene 8: s08_predict (10.825 s)
# ---------------------------------------------------------------------------
class S08Predict(SpokenScene):
    def construct(self):
        plaza, world = build_s08_world()
        self.add(world)
        q = question_card("Does the half-speed point move?", y=BOTTOM_Y - 0.05, color=TEXT, size=32, max_w=9.5)

        self.at("does the half speed point move")
        self.play(FadeIn(q), run_time=0.55)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 9: s09_pause (4.5 s silent)
# ---------------------------------------------------------------------------
class S09Pause(PredictPause):
    QUESTION = "Does the half-speed point move?"
    CARD = {"y": BOTTOM_Y - 0.05, "color": TEXT, "size": 32, "max_w": 9.5}
    SECONDS = 4.5

    def backdrop(self):
        _, world = build_s08_world()
        return world


# ---------------------------------------------------------------------------
# Scene 10: s10_answer (17.125 s)
# ---------------------------------------------------------------------------
class S10Answer(SpokenScene):
    def construct(self):
        plaza_old, world_old = build_s08_world()
        q = question_card("Does the half-speed point move?", y=BOTTOM_Y - 0.05, color=TEXT, size=32, max_w=9.5)
        self.add(world_old, q)

        no_txt = T("No.", size=42, color=TEXT, weight=BOLD).move_to(q.question)
        self.play(swap(q, no_txt, run_time=0.6))

        self.at("less enzyme")
        plaza_old.stop_live()
        plaza_2 = TollPlaza(PLAZA_50, n_booths=2, seed=37, s_conc=14.0, compact=False)
        less_lbl = T("less enzyme (2 of 6)", size=28, color=BLUE).move_to([-3.35, 2.95, 0])
        old_head = world_old[-2]
        self.play(
            FadeOut(plaza_old),
            FadeOut(old_head),
            FadeIn(plaza_2),
            FadeIn(less_lbl),
            run_time=0.8,
        )
        plaza_2.start_live()

        P = world_old[1]
        self.at("falls")
        noncomp_curve = P.curve(v_noncomp, color=MAGENTA, width=5.5)
        vmax_tr = ValueTracker(60.0)
        mag_ceil = always_redraw(lambda: DashedLine(
            P.pt(0, vmax_tr.get_value()), P.pt(40, vmax_tr.get_value()),
            color=MAGENTA, stroke_width=3.0, dash_length=0.14
        ))
        self.play(Create(noncomp_curve), run_time=1.0)
        self.add(mag_ceil)
        self.play(vmax_tr.animate.set_value(20.0), run_time=1.2, rate_func=smooth)
        vmax20_lbl = M("Vmax: 20", size=24, color=MAGENTA).next_to(P.pt(39.5, 20.0), UP, buff=0.10).align_to(P.pt(39.5, 20.0), RIGHT)
        self.play(FadeIn(vmax20_lbl), run_time=0.35)

        self.at("stays at 4")
        half_dot = Dot(P.pt(KM, 10.0), radius=0.11, color=MAGENTA, stroke_color=TEXT, stroke_width=2.5)
        h_line = DashedLine(P.pt(0, 10.0), P.pt(KM, 10.0), color=MAGENTA, stroke_width=2.8, dash_length=0.10)
        self.play(FadeIn(h_line), FadeIn(half_dot), run_time=0.5)

        self.at("pure")
        pure_lbl = T("pure noncompetitive", size=28, color=MAGENTA).move_to([3.5, 3.05, 0])
        self.play(FadeOut(no_txt), FadeIn(pure_lbl), run_time=0.5)

        self.finish()


# ---------------------------------------------------------------------------
# Scene 11: s11_mixed (15.075 s)
# ---------------------------------------------------------------------------
class S11Mixed(SpokenScene):
    def construct(self):
        plaza = TollPlaza(
            PLAZA_50, n_booths=6, seed=41, s_conc=14.0,
            clamped_mask=["EI", None, "ESI", "EI", None, "ESI"],
            clamp_style="side", side_weights=(1.0, 1.0), compact=True,
        )
        P, blue_c, ceil = build_mm_plot(PLOT_50, label_size=24, tick_size=22)
        blue_km = drop_lines(P, KM, 30.0, color=BLUE, width=2.4)
        mag_ceil = DashedLine(P.pt(0, 20.0), P.pt(40, 20.0), color=MAGENTA, stroke_width=2.8, dash_length=0.14)
        vmax_lbl = M("Vmax < 60", size=24, color=MAGENTA).next_to(P.pt(39.5, 20.0), UP, buff=0.10).align_to(P.pt(39.5, 20.0), RIGHT)

        km_mix = ValueTracker(4.0)
        mix_curve = always_redraw(lambda: P.curve(lambda s: v_mixed(s, km_mix.get_value(), 20.0), color=MAGENTA, width=5.5))
        mix_drop = always_redraw(lambda: drop_lines(P, km_mix.get_value(), 10.0, color=MAGENTA, width=3.0))
        km_read = always_redraw(
            lambda: M(f"apparent Km: {km_mix.get_value():.1f}", size=24, color=MAGENTA).next_to(
                P.pt(max(km_mix.get_value(), 5.0), 10.0), DR, buff=0.12
            )
        )

        head = T("mixed: unequal grip", size=30, color=MAGENTA).move_to([-3.35, 2.95, 0])
        stag = scope_tag("schematic", size=22, color=GREY)

        self.add(plaza, P, blue_c, ceil, blue_km, mag_ceil, vmax_lbl, mix_curve, mix_drop, km_read, stag)
        plaza.start_live()

        self.at("mixed inhibition")
        self.play(FadeIn(head), run_time=0.45)

        self.at("different strengths")
        plaza.side_weights = (2.4, 0.6)
        self.play(km_mix.animate.set_value(8.5), run_time=1.7, rate_func=smooth)

        self.at("still falls")
        plaza.side_weights = (0.6, 2.4)
        self.play(km_mix.animate.set_value(1.8), run_time=1.3, rate_func=smooth)

        self.at("can rise or fall")
        plaza.side_weights = (1.0, 1.0)
        self.play(km_mix.animate.set_value(4.0), run_time=1.0, rate_func=smooth)

        self.finish()


# ---------------------------------------------------------------------------
# Scene 12: s12_return (17.0 s)
# ---------------------------------------------------------------------------
class S12Return(SpokenScene):
    def construct(self):
        plaza = TollPlaza(PLAZA_50, n_booths=6, seed=43, s_conc=14.0, compact=True)
        P, blue_c, ceil = build_mm_plot(PLOT_50, label_size=24, tick_size=22)
        c1 = P.curve(v_comp, color=MAGENTA, width=4.5)
        c2 = P.curve(v_uncomp, color=MAGENTA, width=4.5)
        c3 = P.curve(v_noncomp, color=MAGENTA, width=4.5)
        l1 = M("1", size=24, color=MAGENTA).next_to(P.pt(33, v_comp(33)), UP, buff=0.14)
        # Put '2' cleanly above the y=20 ceiling line between curve 1 and curve 2
        l2 = M("2", size=24, color=MAGENTA).move_to(P.pt(14.5, 24.5))
        l3 = M("3", size=24, color=MAGENTA).next_to(P.pt(22, v_noncomp(22)), DOWN, buff=0.14)

        slot_e = boxed_label("empty", color=BLUE, size=26, box=(1.7, 0.56)).move_to([-5.35, 2.85, 0])
        slot_b = boxed_label("busy", color=YELLOW, size=26, box=(1.7, 0.56)).move_to([-3.35, 2.85, 0])
        slot_both = boxed_label("both", color=MAGENTA, size=26, box=(1.7, 0.56)).move_to([-1.35, 2.85, 0])

        q_top = T("What does it grab?", size=32, color=TEXT).move_to([3.3, 3.05, 0])
        stag = scope_tag("schematic", size=22, color=GREY)

        self.add(plaza, P, blue_c, ceil, c1, c2, c3, l1, l2, l3, slot_e, slot_b, slot_both, stag)
        plaza.start_live()

        self.at("what the inhibitor grabs")
        self.play(FadeIn(q_top), run_time=0.45)

        self.at("Grabbing empty enzyme")
        hl = SurroundingRectangle(slot_e, color=GOLD, buff=0.06, stroke_width=3)
        plaza.clamp_style = "doorway"
        for i in (1, 3, 5):
            plaza.set_clamped(i, "EI")
        km_1 = ValueTracker(4.0)
        d1 = always_redraw(lambda: drop_lines(P, km_1.get_value(), 30.0, color=GOLD, width=3))
        self.add(d1)
        self.play(
            FadeIn(hl),
            c1.animate.set_stroke(color=GOLD, width=6),
            c2.animate.set_stroke(opacity=0.3),
            c3.animate.set_stroke(opacity=0.3),
            km_1.animate.set_value(12.0),
            run_time=1.8,
        )

        self.at("Grabbing busy enzyme")
        self.remove(d1)
        plaza.clamp_style = "side"
        for i in range(6):
            plaza.set_clamped(i, "ESI" if i in (0, 2, 4) else None)
        km_2 = ValueTracker(4.0)
        vm_2 = ValueTracker(60.0)
        d2 = always_redraw(lambda: drop_lines(P, km_2.get_value(), vm_2.get_value() / 2.0, color=GOLD, width=3))
        c2_ceil = always_redraw(lambda: DashedLine(P.pt(0, vm_2.get_value()), P.pt(40, vm_2.get_value()), color=GOLD, stroke_width=2.5, dash_length=0.14))
        self.add(d2, c2_ceil)
        hl_b = SurroundingRectangle(slot_b, color=GOLD, buff=0.06, stroke_width=3)
        self.play(
            FadeOut(hl, run_time=0.2),
            FadeIn(hl_b, run_time=0.2),
            c1.animate.set_stroke(color=MAGENTA, width=4, opacity=0.3),
            c2.animate.set_stroke(color=GOLD, width=6, opacity=1.0),
            km_2.animate.set_value(4.0 / 3.0),
            vm_2.animate.set_value(20.0),
            run_time=1.8,
        )

        self.at("Grabbing both equally")
        self.remove(d2, c2_ceil)
        for i, st in enumerate(("EI", None, "ESI", "EI", None, "ESI")):
            plaza.set_clamped(i, st)
        vm_3 = ValueTracker(60.0)
        c3_ceil = always_redraw(lambda: DashedLine(P.pt(0, vm_3.get_value()), P.pt(40, vm_3.get_value()), color=GOLD, stroke_width=2.5, dash_length=0.14))
        d3 = drop_lines(P, KM, 10.0, color=GOLD, width=3)
        self.add(c3_ceil, d3)
        hl_both = SurroundingRectangle(slot_both, color=GOLD, buff=0.06, stroke_width=3)
        self.play(
            FadeOut(hl_b, run_time=0.2),
            FadeIn(hl_both, run_time=0.2),
            c2.animate.set_stroke(color=MAGENTA, width=4, opacity=0.3),
            c3.animate.set_stroke(color=GOLD, width=6, opacity=1.0),
            vm_3.animate.set_value(20.0),
            run_time=1.5,
        )

        self.finish()


# ---------------------------------------------------------------------------
# Scene 13: s13_end (3.5 s silent)
# ---------------------------------------------------------------------------
class S13End(EndCard):
    LINE = "Which enzymes an inhibitor grabs, empty, busy, or both, sets its pattern."
