"""
"What Plasma Sodium Reports" — Body Water and Its Compartments (Chapter 2)

COLOUR MAP (one colour per concept, carried all film):
- BLUE   (#58C4DD): water (water dots, the "water only" membrane channel, water in fraction, body water tank)
- GREEN  (#83C167): inside cells (ICF compartment, left room, 28 L baseline)
- ORANGE (#FF862F): outside cells (ECF compartment, right room, 14 L baseline)
- YELLOW (#F5D547): effective solute (potassium-salt chips in ICF, sodium-salt chips in ECF, dial needle,
                    cation terms in fraction, body sodium/potassium tanks, sodium stock piles)
- GOLD   (#D4A843): question mark, title rule, predict UI
- GREY   (#8B93A1): cell membrane, non-exchangeable bone sodium band, plot axes, scope tags
- TEXT   (#E8EAF0): dial ring, digital readout, fraction bar, Edelman regression line, tracer dots, headings

ONE WORLD CARRIED:
Two side-by-side fluid rooms (GREEN ICF on the left at 28 L, ORANGE ECF on the right at 14 L) joined by a
GREY cell membrane with a BLUE water-only door, filled with moving BLUE water dots and jiggling YELLOW
effective-solute chips (28 in ICF, 14 in ECF: 1 chip = 300 mOsm). On the right sits a round WHITE plasma
sodium dial (120-150 mmol/L) with a YELLOW needle, a live mmol/L readout, and (from s02 onward) the
cation-over-water fraction directly beneath it.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: BLUE water dots cross both ways through the membrane door and equilibrate; dial
  needle swings from 140 down to 125 mmol/L and blinks "low" while GOLD "?" and "Lost sodium?" appear.
- s02_two_parts: The fraction (YELLOW sodium / BLUE water) builds under the dial; sodium chips and water
  dots pulse in turn; needle sweeps 140 -> 128 -> 140 to show either term moves it.
- s03_water_dilutes: A BLUE 1 L water load drops into ECF and dissolves into 6 water dots that split 2/3
  (4 dots) into ICF and 1/3 (2 dots) in ECF; compartments expand from (28, 14) to (28.67, 14.33) L and
  dial needle + readout slide from 140.0 to 136.7 mmol/L (computed as 140 * 42 / 43).
- s04_predict: World resets to (28, 14) L and 140 mmol/L; 2 YELLOW chips (600 mOsm K+ salts) lift out of
  ICF and exit the frame while 14 ECF Na+ chips remain; "Rise, fall, or stay?" appears.
- s06_cells_shrink: "Rise, fall, or stay?" swaps to "falls"; BLUE water dots stream through the door from
  ICF to ECF and ICF narrows from 28.0 to 27.3 L (computed from C = 12,000 / 42 = 285.7 mOsm/kg,
  ICF = 7,800 / C = 27.3 L).
- s07_sodium_falls: ECF widens from 14.0 to 14.7 L as its 14 YELLOW chips spread apart; BLUE "water" in
  the fraction swells and the dial needle + readout slide from 140 to 133 mmol/L (computed as
  140 * 14 / 14.7); "bookkeeping" swaps to "real life: messier".
- s08_idea: Fraction transforms to "sodium + potassium" / "all body water" as chips in both rooms and
  water in both rooms pulse; a YELLOW "sodium stock" pile appears with a GREY struck-through link to the dial.
- s09_edelman: Rooms + dial shrink to the left 40% while three tanks ("body sodium", "body potassium",
  "body water") appear on the right; WHITE isotope tracer dots drop into the sodium tank and mix through
  its upper exchangeable part, leaving the dark base unreached.
- s10_result: A flat schematic "single store: poor" cloud flashes beside the sodium tank; the tanks merge
  into the fraction beside a computed Edelman regression line y = 1.11*x - 25.6 with schematic points
  (r = 0.83, fixed seed 7); a lower-left point glows for "edema: high sodium stock".
- s11_limits: "correlation, not experiment" appears above the Edelman plot; the body sodium tank returns
  and its dark base relabels to "bone sodium" and glows once.
- s12_close: World pulls back to full size with needle low at 133; BLUE water swells in the fraction and
  three YELLOW sodium-stock piles ("low", "normal", "high") connect equally to the same low needle.
"""

from bp_parts import *

# ------------------------------------------------------------------ model constants
TBW0 = 42.0
ICF0 = 28.0
ECF0 = 14.0
C0 = 300.0
OSM_ICF0 = ICF0 * C0       # 8400 mOsm
OSM_ECF0 = ECF0 * C0       # 4200 mOsm
NA0 = 140.0

# 1 L solute-free water (s03)
ICF_S03 = ICF0 * (TBW0 + 1.0) / TBW0     # 28.6667 L
ECF_S03 = ECF0 * (TBW0 + 1.0) / TBW0     # 14.3333 L
NA_S03 = NA0 * TBW0 / (TBW0 + 1.0)       # 136.744 mmol/L

# 600 mOsm K+ depletion (s06 / s07)
OSM_K_REMOVED = 600.0
C_S06 = (OSM_ICF0 - OSM_K_REMOVED + OSM_ECF0) / TBW0   # 285.714 mOsm/kg
ICF_S06 = (OSM_ICF0 - OSM_K_REMOVED) / C_S06           # 27.3 L
ECF_S07 = OSM_ECF0 / C_S06                             # 14.7 L
NA_S07 = NA0 * ECF0 / ECF_S07                          # 133.333 mmol/L

# Dial mapping (120..150 mmol/L across 220 deg: 200 deg -> -20 deg)
DIAL_MIN = 120.0
DIAL_MAX = 150.0
DIAL_ANG0 = 200.0 * DEGREES
DIAL_SWEEP = -220.0 * DEGREES


def _dial_angle(na):
    frac = np.clip((na - DIAL_MIN) / (DIAL_MAX - DIAL_MIN), 0.0, 1.0)
    return DIAL_ANG0 + frac * DIAL_SWEEP


# ------------------------------------------------------------------ world builders
# Full-size room geometry: left wall x=-6.0, 1 L = 0.20 units -> ICF=5.6, ECF=2.8
FULL_X0 = -6.0
FULL_Y0 = -2.35
FULL_Y1 = 1.95
FULL_SCALE_X = 0.20

# Shrunk left-40% geometry for s09..s11
MINI_X0 = -6.2
MINI_Y0 = -2.35
MINI_Y1 = 0.65
MINI_SCALE_X = 0.115


class FluidWorld:
    """Two-compartment world (ICF green, ECF orange, membrane with blue door, moving water & solute chips)."""

    def __init__(self, icf=ICF0, ecf=ECF0, k_chips=28, na_chips=14,
                 x0=FULL_X0, y0=FULL_Y0, y1=FULL_Y1, scale_x=FULL_SCALE_X,
                 seed=7, dot_r=0.055, chip_w=0.30, chip_h=0.20,
                 show_labels=True, label_fmt="{:.1f} L", crossing_mode=False):
        self.icf_tr = ValueTracker(icf)
        self.ecf_tr = ValueTracker(ecf)
        self.x0, self.y0, self.y1, self.sx = x0, y0, y1, scale_x
        self.dot_r = dot_r
        self.rng = np.random.default_rng(seed)

        # Compartment rectangles driven by live volume trackers
        def mk_icf_box():
            w = self.icf_tr.get_value() * self.sx
            return Rectangle(
                width=w, height=self.y1 - self.y0,
                stroke_color=GREEN, stroke_width=3.5,
                fill_color=GREEN, fill_opacity=0.18,
            ).move_to([self.x0 + w / 2, (self.y0 + self.y1) / 2, 0])

        def mk_ecf_box():
            w_i = self.icf_tr.get_value() * self.sx
            w_e = self.ecf_tr.get_value() * self.sx
            return Rectangle(
                width=w_e, height=self.y1 - self.y0,
                stroke_color=ORANGE, stroke_width=3.5,
                fill_color=ORANGE, fill_opacity=0.18,
            ).move_to([self.x0 + w_i + w_e / 2, (self.y0 + self.y1) / 2, 0])

        self.icf_box = always_redraw(mk_icf_box)
        self.ecf_box = always_redraw(mk_ecf_box)

        # Cell membrane with central BLUE water-only channel
        door_h = 0.22 * (self.y1 - self.y0)
        ym = (self.y0 + self.y1) / 2

        def mk_membrane():
            xm = self.x0 + self.icf_tr.get_value() * self.sx
            top_wall = Line([xm, self.y1, 0], [xm, ym + door_h / 2, 0], color=GREY, stroke_width=6)
            bot_wall = Line([xm, ym - door_h / 2, 0], [xm, self.y0, 0], color=GREY, stroke_width=6)
            ch_w = 0.26 * (self.sx / FULL_SCALE_X)
            ch_top = Line([xm - ch_w, ym + door_h / 2, 0], [xm + ch_w, ym + door_h / 2, 0], color=BLUE, stroke_width=5)
            ch_bot = Line([xm - ch_w, ym - door_h / 2, 0], [xm + ch_w, ym - door_h / 2, 0], color=BLUE, stroke_width=5)
            door_glow = Line([xm, ym - door_h / 2 + 0.04, 0], [xm, ym + door_h / 2 - 0.04, 0],
                             color=BLUE, stroke_width=4, stroke_opacity=0.55)
            return VGroup(top_wall, bot_wall, ch_top, ch_bot, door_glow)

        self.membrane = always_redraw(mk_membrane)

        # Room labels placed cleanly above y1 (never inside rooms)
        self.labels = VGroup()
        if show_labels:
            def mk_labels():
                w_i = self.icf_tr.get_value() * self.sx
                w_e = self.ecf_tr.get_value() * self.sx
                xi = self.x0 + w_i / 2
                xe = self.x0 + w_i + w_e / 2
                ly = self.y1 + 0.36
                if self.sx >= 0.16:
                    t_i = T(f"ICF  {label_fmt.format(self.icf_tr.get_value())}", size=26, color=GREEN).move_to([xi, ly, 0])
                    t_e = T(f"ECF  {label_fmt.format(self.ecf_tr.get_value())}", size=26, color=ORANGE).move_to([xe, ly, 0])
                else:
                    t_i = T(f"ICF {self.icf_tr.get_value():.1f}L", size=22, color=GREEN).move_to([xi, ly - 0.05, 0])
                    t_e = T(f"ECF {self.ecf_tr.get_value():.1f}L", size=22, color=ORANGE).move_to([xe, ly - 0.05, 0])
                return VGroup(t_i, t_e)
            self.labels = always_redraw(mk_labels)

        # Water dots (BLUE): 2 per L in full size (56 + 28), 1 per L in mini (28 + 14)
        n_per_l = 2 if self.sx >= 0.16 else 1
        n_icf_dots = int(round(icf * n_per_l))
        n_ecf_dots = int(round(ecf * n_per_l))
        self.water_dots = VGroup()
        self._dot_states = []

        pad = 0.20 * (self.sx / FULL_SCALE_X) + self.dot_r
        for side, count in (("icf", n_icf_dots), ("ecf", n_ecf_dots)):
            for _ in range(count):
                fx = float(self.rng.uniform(0.08, 0.92))
                fy = float(self.rng.uniform(0.08, 0.92))
                vx = float(self.rng.uniform(-0.22, 0.22))
                vy = float(self.rng.uniform(-0.22, 0.22))
                if abs(vx) < 0.06:
                    vx = 0.10 if vx >= 0 else -0.10
                if abs(vy) < 0.06:
                    vy = 0.10 if vy >= 0 else -0.10
                d = Dot(radius=self.dot_r, color=BLUE, fill_opacity=0.85)
                d._side = side
                d._fx = fx
                d._fy = fy
                d._vx = vx
                d._vy = vy
                d._crossing = crossing_mode and (self.rng.random() < 0.18)
                self._place_dot(d, pad)
                self.water_dots.add(d)

        # Solute chips (YELLOW rounded pills, jiggling gently in place, never crossing)
        self.icf_chips = self._build_chips("icf", k_chips, chip_w, chip_h)
        self.ecf_chips = self._build_chips("ecf", na_chips, chip_w, chip_h)

        self.group = VGroup(self.icf_box, self.ecf_box, self.membrane,
                            self.water_dots, self.icf_chips, self.ecf_chips, self.labels)

    def _bounds(self, side, pad):
        w_i = self.icf_tr.get_value() * self.sx
        w_e = self.ecf_tr.get_value() * self.sx
        if side == "icf":
            xmin, xmax = self.x0 + pad, self.x0 + w_i - pad
        else:
            xmin, xmax = self.x0 + w_i + pad, self.x0 + w_i + w_e - pad
        ymin, ymax = self.y0 + pad, self.y1 - pad
        return xmin, xmax, ymin, ymax

    def _place_dot(self, d, pad):
        xmin, xmax, ymin, ymax = self._bounds(d._side, pad)
        x = xmin + d._fx * max(xmax - xmin, 0.05)
        y = ymin + d._fy * max(ymax - ymin, 0.05)
        d.move_to([x, y, 0])

    def _build_chips(self, side, n, cw, ch):
        g = VGroup()
        if n <= 0:
            return g
        cols = 4 if side == "icf" else 2
        rows = int(np.ceil(n / cols))
        for idx in range(n):
            r, c = divmod(idx, cols)
            fx = (c + 0.5 + self.rng.uniform(-0.16, 0.16)) / cols
            fy = (r + 0.5 + self.rng.uniform(-0.16, 0.16)) / rows
            pill = RoundedRectangle(
                corner_radius=min(cw, ch) * 0.35, width=cw, height=ch,
                stroke_color=YELLOW, stroke_width=2.0,
                fill_color=YELLOW, fill_opacity=0.82,
            )
            pill._side = side
            pill._fx = float(np.clip(fx, 0.10, 0.90))
            pill._fy = float(np.clip(fy, 0.08, 0.92))
            pill._phase = float(self.rng.uniform(0, TAU))
            pill._freq = float(self.rng.uniform(2.2, 3.6))
            pill._t = 0.0
            pad = 0.24 * (self.sx / FULL_SCALE_X)
            xmin, xmax, ymin, ymax = self._bounds(side, pad)
            pill.move_to([xmin + pill._fx * (xmax - xmin), ymin + pill._fy * (ymax - ymin), 0])
            g.add(pill)
        return g

    def start_motion(self, jiggle_chips=True):
        pad_dot = 0.20 * (self.sx / FULL_SCALE_X) + self.dot_r
        pad_chip = 0.24 * (self.sx / FULL_SCALE_X)

        def step_dot(d, dt):
            if dt <= 0:
                return
            d._fx += d._vx * dt * 0.28
            d._fy += d._vy * dt * 0.28
            if d._fx < 0.06:
                d._fx = 0.06
                d._vx = abs(d._vx)
            elif d._fx > 0.94:
                d._fx = 0.94
                d._vx = -abs(d._vx)
            if d._fy < 0.06:
                d._fy = 0.06
                d._vy = abs(d._vy)
            elif d._fy > 0.94:
                d._fy = 0.94
                d._vy = -abs(d._vy)
            self._place_dot(d, pad_dot)

        for d in self.water_dots:
            d.add_updater(step_dot)

        if jiggle_chips:
            def step_chip(p, dt):
                if dt <= 0:
                    return
                p._t += dt
                xmin, xmax, ymin, ymax = self._bounds(p._side, pad_chip)
                bx = xmin + p._fx * (xmax - xmin)
                by = ymin + p._fy * (ymax - ymin)
                amp = 0.032 * (self.sx / FULL_SCALE_X)
                dx = amp * np.sin(p._freq * p._t + p._phase)
                dy = amp * np.cos(p._freq * 0.85 * p._t + p._phase)
                p.move_to([bx + dx, by + dy, 0])

            for ch in (*self.icf_chips, *self.ecf_chips):
                ch.add_updater(step_chip)

    def stop_motion(self):
        for d in self.water_dots:
            d.clear_updaters()
        for ch in (*self.icf_chips, *self.ecf_chips):
            ch.clear_updaters()

    def membrane_x(self):
        return self.x0 + self.icf_tr.get_value() * self.sx

    def door_y(self):
        return (self.y0 + self.y1) / 2


def make_dial(na_tracker, center=(4.45, 1.85, 0), radius=0.82, title_size=26,
              num_size=28, fmt="{:.1f}", show_readout=True, tremble_tracker=None):
    """Round WHITE plasma sodium dial with YELLOW needle and live mmol/L readout."""
    c = np.array(center, dtype=float)
    ring = Circle(radius=radius, color=TEXT, stroke_width=4.0, fill_color=BG, fill_opacity=0.92).move_to(c)

    # Ticks at 120, 130, 140, 150
    ticks = VGroup()
    for val in (120, 130, 140, 150):
        ang = _dial_angle(val)
        p_out = c + radius * np.array([np.cos(ang), np.sin(ang), 0])
        p_in = c + (radius - 0.14 * (radius / 0.82)) * np.array([np.cos(ang), np.sin(ang), 0])
        col = YELLOW if val == 140 else GREY
        ticks.add(Line(p_in, p_out, color=col, stroke_width=3.5 if val == 140 else 2.5))

    hub = Dot(c, radius=0.065 * (radius / 0.82), color=YELLOW)

    def mk_needle():
        val = na_tracker.get_value()
        if tremble_tracker is not None:
            val += tremble_tracker.get_value()
        ang = _dial_angle(val)
        tip = c + 0.78 * radius * np.array([np.cos(ang), np.sin(ang), 0])
        return Line(c, tip, color=YELLOW, stroke_width=5.0 * (radius / 0.82))

    needle = always_redraw(mk_needle)
    title = T("plasma sodium", size=title_size, color=TEXT).move_to(c + UP * (radius + 0.34))

    parts = [ring, ticks, needle, hub, title]
    readout = None
    if show_readout:
        readout = always_redraw(
            lambda: M(f"{fmt.format(na_tracker.get_value())} mmol/L", num_size, YELLOW)
            .move_to(c + DOWN * (radius + 0.32))
        )
        parts.append(readout)

    g = VGroup(*parts)
    g.ring = ring
    g.needle = needle
    g.title = title
    g.readout = readout
    g.center_pt = c
    g.radius_val = radius
    return g


def make_fraction(top_text="sodium", bot_text="water", center=(4.45, -0.45, 0),
                  size=26, bar_w=2.7, top_scale=1.0, bot_scale=1.0):
    """Simple YELLOW-over-BLUE fraction under the dial."""
    c = np.array(center, dtype=float)
    top = T(top_text, size=size, color=YELLOW).scale(top_scale).move_to(c + UP * 0.32)
    bar = Line(c + LEFT * (bar_w / 2), c + RIGHT * (bar_w / 2), color=TEXT, stroke_width=3.5)
    bot = T(bot_text, size=size, color=BLUE).scale(bot_scale).move_to(c + DOWN * 0.32)
    g = VGroup(top, bar, bot)
    g.top, g.bar, g.bot = top, bar, bot
    return g


def make_sodium_pile(n_chips, label_text, center, chip_w=0.24, chip_h=0.16, tag_size=24):
    """A pyramid-like pile of YELLOW chips representing body sodium stock."""
    chips = VGroup()
    rows = []
    rem = n_chips
    row_len = int(np.ceil(np.sqrt(2 * n_chips)))
    while rem > 0 and row_len > 0:
        take = min(rem, row_len)
        rows.append(take)
        rem -= take
        row_len = max(1, row_len - 1)
    if rem > 0:
        rows[0] += rem

    for r_idx, cnt in enumerate(rows):
        y = r_idx * (chip_h + 0.05)
        for c_idx in range(cnt):
            x = (c_idx - (cnt - 1) / 2) * (chip_w + 0.05)
            chips.add(RoundedRectangle(
                corner_radius=0.05, width=chip_w, height=chip_h,
                stroke_color=YELLOW, stroke_width=1.8, fill_color=YELLOW, fill_opacity=0.85,
            ).move_to([x, y, 0]))

    chips.move_to(center)
    lab = T(label_text, size=tag_size, color=YELLOW).next_to(chips, DOWN, buff=0.16)
    g = VGroup(chips, lab)
    g.chips, g.label = chips, lab
    return g


def make_edelman_tanks(center_y=-0.25):
    """Three plain stores for s09/s10/s11: body sodium, body potassium, body water."""
    specs = [
        ("body sodium", 1.15, YELLOW, 0.72, 0.28),
        ("body potassium", 3.30, YELLOW, 0.92, 0.08),
        ("body water", 5.45, BLUE, 1.00, 0.00),
    ]
    w, h = 1.32, 2.75
    tanks = VGroup()
    for name, cx, col, exch_frac, non_frac in specs:
        outer = RoundedRectangle(
            corner_radius=0.10, width=w, height=h,
            stroke_color=col, stroke_width=3.0, fill_color=col, fill_opacity=0.08,
        ).move_to([cx, center_y, 0])
        exch_h = h * exch_frac
        exch = Rectangle(
            width=w - 0.06, height=exch_h - 0.04,
            stroke_width=0, fill_color=col, fill_opacity=0.25,
        ).move_to([cx, center_y + h / 2 - exch_h / 2 - 0.02, 0])
        base = VGroup()
        if non_frac > 0:
            bh = h * non_frac
            b_rect = Rectangle(
                width=w - 0.06, height=bh - 0.03,
                stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.45,
            ).move_to([cx, center_y - h / 2 + bh / 2 + 0.02, 0])
            base.add(b_rect)
        parts = name.split(" ")
        lbl = T(f"{parts[0]}\n{parts[1]}", size=24, color=col, line_spacing=0.85).next_to(outer, DOWN, buff=0.20)
        tk = VGroup(exch, base, outer, lbl)
        tk.outer, tk.exch, tk.base, tk.label = outer, exch, base, lbl
        tanks.add(tk)
    return tanks


def make_edelman_plot():
    """Computed Edelman regression line y = 1.11 x - 25.6 and schematic cloud (r ~ 0.83)."""
    P = Plot(
        box=(1.55, 6.05, -1.75, 1.85),
        xr=(115, 170), yr=(98, 168),
        xticks=(), yticks=(),
        xlabel="cation per litre water",
        ylabel="serum sodium",
        color=GREY, label_size=24,
    )
    fn = lambda x: 1.11 * x - 25.6
    rng = np.random.default_rng(7)
    xs = rng.uniform(121, 166, 28)
    # Orthogonal noise calibrated so empirical r ~ 0.83
    ys = fn(xs) + rng.normal(0, 6.2, len(xs))
    ys = np.clip(ys, 102, 164)
    dots = VGroup(*[Dot(P.pt(x, y), radius=0.06, color=YELLOW, fill_opacity=0.85) for x, y in zip(xs, ys)])
    # Lower-left edema point (low serum sodium despite excess sodium stock)
    ex, ey = 123.0, 109.5
    edema_dot = Dot(P.pt(ex, ey), radius=0.095, color=GOLD, stroke_color=TEXT, stroke_width=2.5)
    return P, fn, dots, edema_dot


# ================================================================== scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        world = FluidWorld(icf=ICF0, ecf=ECF0, k_chips=28, na_chips=14, label_fmt="{:.0f} L")
        na = ValueTracker(NA0)
        dial_g = make_dial(na, fmt="{:.0f}")

        # Membrane "water only" label neatly below membrane to stay clear of dots
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])

        self.add(world.group, dial_g, door_lbl)
        world.start_motion(jiggle_chips=True)

        # Beat 1: water crosses both ways through the BLUE door and settles
        runners = []
        mx = world.membrane_x()
        dy = world.door_y()
        for idx, (start_x, end_x, offset_y) in enumerate([
            (mx - 1.3, mx + 0.9, 0.14),
            (mx + 1.0, mx - 1.4, -0.14),
            (mx - 0.9, mx + 1.2, -0.05),
            (mx + 0.8, mx - 1.0, 0.08),
        ]):
            cd = Dot(radius=0.075, color=BLUE).move_to([start_x, dy + offset_y, 0])
            self.add(cd)
            runners.append((cd, [mx, dy + offset_y * 0.4, 0], [end_x, dy + offset_y * 1.4, 0]))

        self.play(
            *[Succession(
                cd.animate(run_time=1.4).move_to(p_mid),
                cd.animate(run_time=1.4).move_to(p_end),
                FadeOut(cd, run_time=0.4),
            ) for cd, p_mid, p_end in runners],
        )

        self.at("same number")
        self.wait(0.8)

        # Beat 2: blood test reads low plasma sodium -> needle swings down, readout blinks "low"
        self.at("blood test")
        low_tag = boxed_label("low", color=YELLOW, size=24).next_to(dial_g.readout, DOWN, buff=0.22)
        self.play(na.animate.set_value(125.0), FadeIn(low_tag), run_time=1.3)
        self.play(FadeOut(low_tag), run_time=0.20)
        self.play(FadeIn(low_tag), run_time=0.20)

        # Beat 3: "Has this body lost sodium?" -> GOLD ? beside dial, "Lost sodium?" at top
        self.at("has this body")
        q_mark = T("?", size=64, color=GOLD, weight=BOLD).move_to([2.90, 1.95, 0])
        top_q = T("Lost sodium?", size=34, color=GOLD, weight=BOLD).move_to([-0.5, 3.15, 0])
        self.play(FadeIn(q_mark, scale=1.15), FadeIn(top_q, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = FluidWorld(icf=ICF0, ecf=ECF0, k_chips=28, na_chips=14, label_fmt="{:.0f} L")
        na = ValueTracker(125.0)
        dial_g = make_dial(na, fmt="{:.0f}")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])
        low_tag = boxed_label("low", color=YELLOW, size=24).next_to(dial_g.readout, DOWN, buff=0.22)
        q_mark = T("?", size=64, color=GOLD, weight=BOLD).move_to([2.90, 1.95, 0])
        top_q = T("Lost sodium?", size=34, color=GOLD, weight=BOLD).move_to([-0.5, 3.15, 0])

        title = T("What Plasma Sodium Reports", size=38, font=TITLE_FONT, color=TEXT).move_to([-0.7, 3.22, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.14)

        self.add(world.group, dial_g, door_lbl, low_tag, q_mark, top_q)
        world.start_motion(jiggle_chips=True)

        self.play(
            FadeOut(top_q), FadeOut(q_mark), FadeOut(low_tag),
            run_time=0.4,
        )
        self.play(
            FadeIn(title), GrowFromCenter(rule),
            na.animate.set_value(NA0),
            run_time=0.7,
        )
        self.finish()


class S02TwoParts(SpokenScene):
    def construct(self):
        world = FluidWorld(icf=ICF0, ecf=ECF0, k_chips=28, na_chips=14, label_fmt="{:.0f} L")
        na = ValueTracker(NA0)
        dial_g = make_dial(na, fmt="{:.0f}")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])
        title = T("What Plasma Sodium Reports", size=38, font=TITLE_FONT, color=TEXT).move_to([-0.7, 3.22, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.14)

        self.add(world.group, dial_g, door_lbl, title, rule)
        world.start_motion(jiggle_chips=True)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.6)

        # Build fraction under the dial
        self.at("sodium per")
        frac = make_fraction("sodium", "water")
        self.play(FadeIn(frac.top, shift=DOWN * 0.1), Create(frac.bar), FadeIn(frac.bot, shift=UP * 0.1), run_time=1.0)

        # Pulse "sodium" + ECF sodium chips
        self.at("the sodium")
        self.play(
            Indicate(frac.top, color=YELLOW, scale_factor=1.18),
            *[Indicate(c, color=WHITE, scale_factor=1.22) for c in world.ecf_chips[:6]],
            run_time=0.9,
        )

        # Pulse "water" + ECF water dots
        self.at("the water")
        ecf_dots = [d for d in world.water_dots if d._side == "ecf"]
        self.play(
            Indicate(frac.bot, color=BLUE, scale_factor=1.18),
            *[Indicate(d, color=WHITE, scale_factor=1.4) for d in ecf_dots[:12]],
            run_time=0.9,
        )

        # Wobble needle once down and back up
        self.at("change either one")
        self.play(na.animate.set_value(128.0), run_time=0.8)
        self.play(na.animate.set_value(NA0), run_time=0.8)
        self.finish()


class S03WaterDilutes(SpokenScene):
    def construct(self):
        world = FluidWorld(icf=ICF0, ecf=ECF0, k_chips=28, na_chips=14, label_fmt="{:.2f} L")
        na = ValueTracker(NA0)
        dial_g = make_dial(na, fmt="{:.1f}")
        frac = make_fraction("sodium", "water")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])
        stag = scope_tag("model, rounded numbers")

        self.add(world.group, dial_g, frac, door_lbl, stag)
        world.start_motion(jiggle_chips=True)

        # Drop 1 L water block into ORANGE room (label stays clear above ECF heading)
        load_lbl = T("1 L water", size=24, color=BLUE, weight=BOLD).move_to([1.0, 3.05, 0])
        load_block = RoundedRectangle(
            corner_radius=0.12, width=0.85, height=0.52,
            stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.45,
        ).move_to([1.0, 1.45, 0])
        self.play(FadeIn(load_lbl, shift=DOWN * 0.1), FadeIn(load_block, shift=DOWN * 0.2), run_time=0.6)
        self.play(load_block.animate.move_to([1.0, 0.1, 0]), run_time=1.0)

        # Dissolve into 6 BLUE water dots (4 -> ICF, 2 -> ECF)
        new_dots = []
        for idx in range(6):
            nd = Dot(radius=0.06, color=BLUE, fill_opacity=0.92).move_to([1.0 + (idx % 3 - 1) * 0.25, 0.1 + (idx // 3 - 0.5) * 0.25, 0])
            new_dots.append(nd)
        self.play(FadeOut(load_block, run_time=0.3), FadeOut(load_lbl, run_time=0.3), *[FadeIn(d, run_time=0.3) for d in new_dots])

        # "No sodium left the body"
        self.at("no sodium")
        no_na_tag = boxed_label("no sodium lost", color=YELLOW, size=24).move_to([4.45, -1.95, 0])
        self.play(
            FadeIn(no_na_tag),
            *[Indicate(c, color=WHITE, scale_factor=1.18) for c in world.ecf_chips[:5]],
            run_time=0.9,
        )

        # Spread 2/3 into ICF, 1/3 stays in ECF; rooms expand to 28.67 L and 14.33 L
        self.at("spread through")
        mx = world.membrane_x()
        dy = world.door_y()
        icf_dests = [[-1.6, 0.4, 0], [-2.5, -0.5, 0], [-3.3, 0.7, 0], [-4.1, -0.8, 0]]
        ecf_dests = [[1.6, 0.8, 0], [1.9, -0.7, 0]]
        cross_anims = [
            Succession(d.animate(run_time=0.9).move_to([mx, dy + (i - 1.5) * 0.12, 0]),
                       d.animate(run_time=1.1).move_to(pos))
            for i, (d, pos) in enumerate(zip(new_dots[:4], icf_dests))
        ] + [
            d.animate(run_time=1.8).move_to(pos)
            for d, pos in zip(new_dots[4:], ecf_dests)
        ]
        # Slightly spread ECF chips apart as ECF widens
        for c in world.ecf_chips:
            c._fx = float(np.clip(0.5 + (c._fx - 0.5) * 1.10, 0.10, 0.90))

        self.play(
            world.icf_tr.animate(run_time=2.0).set_value(ICF_S03),
            world.ecf_tr.animate(run_time=2.0).set_value(ECF_S03),
            *cross_anims,
        )

        # "diluted" -> water word grows noticeably
        self.at("diluted")
        big_water = T("water", size=34, color=BLUE, weight=BOLD).move_to(frac.bot)
        self.play(swap(frac.bot, big_water, run_time=0.6))
        frac.bot = big_water

        # "falls from 140 to about 136.7"
        self.at("falls from")
        self.play(na.animate.set_value(NA_S03), run_time=2.2)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = FluidWorld(icf=ICF0, ecf=ECF0, k_chips=28, na_chips=14, label_fmt="{:.0f} L")
        na = ValueTracker(NA0)
        dial_g = make_dial(na, fmt="{:.0f}")
        frac = make_fraction("sodium", "water")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])
        book_tag = boxed_label("bookkeeping", color=GREY, size=24).move_to([-5.0, 3.12, 0])

        self.add(world.group, dial_g, frac, door_lbl, book_tag)
        world.start_motion(jiggle_chips=True)

        # Remove 600 mOsm potassium salts (2 chips = 600 mOsm) out the top of GREEN room
        self.at("remove")
        removed = VGroup(world.icf_chips[-1], world.icf_chips[-2])
        for c in removed:
            c.clear_updaters()
            world.icf_chips.remove(c)
        self.add(removed)
        rem_lbl = T("600 mOsm potassium salts", size=24, color=YELLOW).move_to([-1.25, 3.12, 0])
        self.play(removed.animate.arrange(RIGHT, buff=0.14).move_to([-3.2, 1.35, 0]), FadeIn(rem_lbl), run_time=0.7)
        self.play(removed.animate.shift(UP * 1.4), FadeOut(removed), FadeOut(rem_lbl, shift=UP * 0.3), run_time=1.5)

        # "Not one sodium ion leaves"
        self.at("not one sodium")
        self.play(*[Indicate(c, color=WHITE, scale_factor=1.22) for c in world.ecf_chips], run_time=0.9)

        # "Does plasma sodium rise, fall, or stay the same?"
        self.at("does plasma sodium")
        q = question_card("Rise, fall, or stay?", y=3.12, color=TEXT, size=30, max_w=6.2)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Rise, fall, or stay?"
    CARD = {"y": 3.12, "color": TEXT, "size": 30, "max_w": 6.2}
    RING_AT = (5.8, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        world = FluidWorld(icf=ICF0, ecf=ECF0, k_chips=26, na_chips=14, label_fmt="{:.0f} L")
        na = ValueTracker(NA0)
        trem = ValueTracker(0.0)
        trem._t = 0.0

        def wobble(tr, dt):
            tr._t += dt
            tr.set_value(0.35 * np.sin(5.0 * tr._t))

        trem.add_updater(wobble)
        self.add(trem)

        dial_g = make_dial(na, fmt="{:.0f}", tremble_tracker=trem)
        frac = make_fraction("sodium", "water")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])
        book_tag = boxed_label("bookkeeping", color=GREY, size=24).move_to([-5.0, 3.12, 0])
        world.start_motion(jiggle_chips=True)
        return VGroup(world.group, dial_g, frac, door_lbl, book_tag)


class S06CellsShrink(SpokenScene):
    def construct(self):
        world = FluidWorld(icf=ICF0, ecf=ECF0, k_chips=26, na_chips=14, label_fmt="{:.1f} L")
        na = ValueTracker(NA0)
        dial_g = make_dial(na, fmt="{:.0f}")
        frac = make_fraction("sodium", "water")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])
        book_tag = boxed_label("bookkeeping", color=GREY, size=24).move_to([-5.0, 3.12, 0])
        q = question_card("Rise, fall, or stay?", y=3.12, color=TEXT, size=30, max_w=6.2)

        self.add(world.group, dial_g, frac, door_lbl, book_tag, q)
        world.start_motion(jiggle_chips=True)

        # "It falls."
        ans = T("falls", size=34, color=GOLD, weight=BOLD).move_to(q)
        self.play(swap(q, ans, run_time=0.7))

        # "With fewer of them, cells hold less water"
        self.at("with fewer")
        self.play(*[Indicate(c, color=WHITE, scale_factor=1.18) for c in world.icf_chips[:10]], run_time=0.9)

        # "cells shrink from 28 to about 27.3 litres. That water moves outside."
        self.at("cells shrink")
        mx = world.membrane_x()
        dy = world.door_y()
        stream_dots = [
            Dot(radius=0.075, color=BLUE).move_to([mx - 1.1 - i * 0.4, dy + (i - 1.5) * 0.22, 0])
            for i in range(4)
        ]
        self.add(*stream_dots)
        self.play(
            world.icf_tr.animate(run_time=3.2).set_value(ICF_S06),
            *[Succession(
                d.animate(run_time=1.3).move_to([mx - 0.14, dy + (i - 1.5) * 0.08, 0]),
                d.animate(run_time=1.3).move_to([mx + 0.8 + i * 0.25, dy + (i - 1.5) * 0.26, 0]),
                FadeOut(d, run_time=0.4),
            ) for i, d in enumerate(stream_dots)],
        )
        self.at("that water")
        self.play(FadeOut(ans), run_time=0.5)
        self.finish()


class S07SodiumFalls(SpokenScene):
    def construct(self):
        # Start with ICF shrunk to 27.3 L and ECF visually showing 14.0 -> 14.7 widening
        world = FluidWorld(icf=ICF_S06, ecf=ECF0, k_chips=26, na_chips=14, label_fmt="{:.1f} L")
        na = ValueTracker(NA0)
        dial_g = make_dial(na, fmt="{:.0f}")
        frac = make_fraction("sodium", "water")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])
        book_tag = boxed_label("bookkeeping", color=GREY, size=24).move_to([-5.0, 3.12, 0])

        self.add(world.group, dial_g, frac, door_lbl, book_tag)
        world.start_motion(jiggle_chips=True)

        # Beat 1: ORANGE room widens to 14.7 L, chips spread apart
        for c in world.ecf_chips:
            c._fx = float(np.clip(0.5 + (c._fx - 0.5) * 1.12, 0.10, 0.90))
        self.play(world.ecf_tr.animate.set_value(ECF_S07), run_time=2.2)

        # Beat 2: "Plasma sodium falls from 140 to about 133"
        self.at("plasma sodium falls")
        big_water = T("water", size=34, color=BLUE, weight=BOLD).move_to(frac.bot)
        self.play(swap(frac.bot, big_water, run_time=0.5))
        frac.bot = big_water
        self.play(na.animate.set_value(NA_S07), run_time=2.4)

        # Beat 3: "No sodium was lost"
        self.at("no sodium")
        no_na_tag = boxed_label("no sodium lost", color=YELLOW, size=24).move_to([4.45, -1.95, 0])
        self.play(FadeIn(no_na_tag), *[Indicate(c, color=WHITE, scale_factor=1.18) for c in world.ecf_chips[:5]], run_time=0.9)

        # Beat 4: "Real potassium depletion is messier"
        self.at("messier")
        real_tag = boxed_label("real life: messier", color=ORANGE, size=24).move_to([-4.6, 3.12, 0])
        self.play(swap(book_tag, real_tag, run_time=0.7))

        # Beat 5: "So plasma sodium still falls" -> needle stays low, tag dims
        self.at("still falls")
        self.play(real_tag.animate.set_opacity(0.45), Indicate(dial_g.needle, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


class S08Idea(SpokenScene):
    def construct(self):
        world = FluidWorld(icf=ICF_S06, ecf=ECF_S07, k_chips=26, na_chips=14, label_fmt="{:.1f} L")
        na = ValueTracker(NA_S07)
        dial_g = make_dial(na, fmt="{:.0f}")
        frac = make_fraction("sodium", "water")
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])

        self.add(world.group, dial_g, frac, door_lbl)
        world.start_motion(jiggle_chips=True)

        self.at("here is the idea")
        idea_hd = T("The idea", size=32, color=GOLD, weight=BOLD).move_to([-1.2, 3.12, 0])
        self.play(FadeIn(idea_hd, shift=DOWN * 0.1), run_time=0.6)

        # Transform fraction top to "sodium + potassium" and pulse BOTH rooms' chips
        self.at("sodium and potassium")
        new_top = T("sodium + potassium", size=24, color=YELLOW).move_to(frac.top)
        self.play(
            swap(frac.top, new_top, run_time=0.8),
            *[Indicate(c, color=WHITE, scale_factor=1.18) for c in (*world.icf_chips[:8], *world.ecf_chips[:6])],
        )
        frac.top = new_top

        # Transform fraction bottom to "all body water" and pulse water dots in both rooms
        self.at("of body water")
        new_bot = T("all body water", size=24, color=BLUE).move_to(frac.bot)
        self.play(
            swap(frac.bot, new_bot, run_time=0.8),
            *[Indicate(d, color=WHITE, scale_factor=1.35) for d in world.water_dots[:20]],
        )
        frac.bot = new_bot

        # "not a gauge of the body's sodium stock" -> pile + struck-through GREY link
        self.at("not a gauge")
        pile = make_sodium_pile(10, "sodium stock", center=[4.45, -2.42, 0])
        link = Line([4.45, -1.82, 0], [4.45, -1.16, 0], color=GREY, stroke_width=4)
        strike1 = Line([4.15, -1.62, 0], [4.75, -1.36, 0], color=GREY, stroke_width=5)
        strike2 = Line([4.15, -1.36, 0], [4.75, -1.62, 0], color=GREY, stroke_width=5)
        self.play(FadeIn(pile), Create(link), run_time=0.8)
        self.play(Create(strike1), Create(strike2), run_time=0.6)
        self.finish()


class S09Edelman(SpokenScene):
    def construct(self):
        # Mini world on left 40% (x = -6.2..-1.37), dial above it
        world = FluidWorld(
            icf=ICF_S06, ecf=ECF_S07, k_chips=26, na_chips=14,
            x0=MINI_X0, y0=MINI_Y0, y1=MINI_Y1, scale_x=MINI_SCALE_X,
            dot_r=0.042, chip_w=0.18, chip_h=0.12, label_fmt="{:.1f} L",
        )
        na = ValueTracker(NA_S07)
        dial_g = make_dial(na, center=(-3.8, 2.25, 0), radius=0.58, title_size=22, num_size=24, fmt="{:.0f}")
        frac = make_fraction("sodium + potassium", "all body water", center=(-3.8, -3.05, 0), size=22, bar_w=3.2)
        tag = T("Edelman, 1958  ·  98 patients", size=28, color=TEXT, weight=BOLD).move_to([2.95, 3.12, 0])

        self.add(world.group, dial_g, frac)
        world.start_motion(jiggle_chips=True)

        self.at("in 1958")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.8)

        # Bring in empty tank outlines early so there is no long empty pause while introducing the 98 patients
        tanks = make_edelman_tanks(center_y=-0.25)
        self.at("tested this")
        self.play(*[FadeIn(VGroup(tk.outer, tk.label), shift=UP * 0.12) for tk in tanks], run_time=1.0)

        # Fill each store as narrator names them: exchangeable sodium, potassium, total body water
        self.at("measured exchangeable")
        self.play(FadeIn(tanks[0].exch), FadeIn(tanks[0].base), run_time=1.1)
        self.play(FadeIn(tanks[1].exch), FadeIn(tanks[1].base), run_time=1.1)
        self.play(FadeIn(tanks[2].exch), run_time=1.1)

        # "isotope dilution" -> tracer dots appear above sodium tank; "mixes with" -> drop and mix
        na_tank = tanks[0]
        rng = np.random.default_rng(7)
        ex_top = na_tank.exch.get_top()[1] - 0.12
        ex_bot = na_tank.exch.get_bottom()[1] + 0.12
        cx = na_tank.outer.get_center()[0]
        tracers = VGroup(*[
            Dot([cx + rng.uniform(-0.48, 0.48), ex_top + 0.55, 0], radius=0.055, color=TEXT)
            for _ in range(14)
        ])
        self.at("isotope dilution")
        self.play(FadeIn(tracers, shift=DOWN * 0.15), run_time=0.6)

        self.at("mixes with")
        self.play(
            *[d.animate.move_to([cx + rng.uniform(-0.48, 0.48), rng.uniform(ex_bot, ex_top), 0]) for d in tracers],
            run_time=1.2,
        )
        ex_lbl = T("exchangeable\nsodium", size=22, color=TEXT, line_spacing=0.85).next_to(na_tank.outer, UP, buff=0.18)
        no_mix_lbl = T("does not\nmix", size=22, color=GREY, line_spacing=0.85).move_to([-0.42, -1.25, 0])
        no_mix_ptr = Arrow(no_mix_lbl.get_right() + RIGHT * 0.06, na_tank.base.get_left() + LEFT * 0.05,
                           color=GREY, stroke_width=3.5, buff=0)
        self.play(FadeIn(ex_lbl), FadeIn(no_mix_lbl), Create(no_mix_ptr), run_time=0.7)
        self.finish()


class S10Result(SpokenScene):
    def construct(self):
        world = FluidWorld(
            icf=ICF_S06, ecf=ECF_S07, k_chips=26, na_chips=14,
            x0=MINI_X0, y0=MINI_Y0, y1=MINI_Y1, scale_x=MINI_SCALE_X,
            dot_r=0.042, chip_w=0.18, chip_h=0.12, label_fmt="{:.1f} L",
        )
        na = ValueTracker(NA_S07)
        dial_g = make_dial(na, center=(-3.8, 2.25, 0), radius=0.58, title_size=22, num_size=24, fmt="{:.0f}")
        frac = make_fraction("sodium + potassium", "all body water", center=(-3.8, -3.05, 0), size=22, bar_w=3.2)
        tag = T("Edelman, 1958  ·  98 patients", size=28, color=TEXT, weight=BOLD).move_to([2.95, 3.12, 0])
        tanks = make_edelman_tanks(center_y=-0.25)

        self.add(world.group, dial_g, frac, tag, tanks)
        world.start_motion(jiggle_chips=True)

        # Beat 1: "correlated poorly with any single store" -> fade out K & water tanks, show flat cloud beside sodium tank
        rng = np.random.default_rng(7)
        poor_box = RoundedRectangle(corner_radius=0.12, width=3.3, height=2.3, stroke_color=GREY, stroke_width=2.5).move_to([4.05, 0.15, 0])
        poor_dots = VGroup(*[
            Dot([4.05 + rng.uniform(-1.35, 1.35), 0.15 + rng.uniform(-0.85, 0.85), 0], radius=0.055, color=YELLOW, fill_opacity=0.65)
            for _ in range(18)
        ])
        poor_lbl = T("single store: poor (schematic)", size=22, color=GREY).next_to(poor_box, DOWN, buff=0.22)
        self.play(FadeOut(tanks[1]), FadeOut(tanks[2]), run_time=0.35)
        self.play(FadeIn(poor_box), FadeIn(poor_dots), FadeIn(poor_lbl), run_time=0.45)

        # Beat 2: tanks transform into the cation/water fraction beside the Edelman plot
        self.at("it followed")
        self.play(FadeOut(poor_box), FadeOut(poor_dots), FadeOut(poor_lbl), run_time=0.4)

        merged_frac = make_fraction("Na + K", "water", center=(-0.15, -0.25, 0), size=24, bar_w=1.50)
        P, fn, cloud, edema_dot = make_edelman_plot()
        x_tr = ValueTracker(115.0)
        live_ln = P.live_curve(fn, x_tr, color=TEXT, width=5)
        tr_dot = P.dot(lambda: x_tr.get_value(), lambda: fn(x_tr.get_value()), color=YELLOW, ring=TEXT, radius=0.09)
        r_tag = T("schematic points, r = 0.83", size=22, color=GREY).move_to([3.8, -3.05, 0])

        self.play(swap(tanks[0], merged_frac, run_time=0.7), Create(P), FadeIn(r_tag), run_time=0.9)
        self.add(live_ln, tr_dot)
        self.play(
            x_tr.animate.set_value(170.0),
            FadeIn(cloud),
            run_time=2.6,
            rate_func=linear,
        )
        self.remove(tr_dot)

        # Beat 3: "Patients with edema..." -> lower-left point glows, label placed in open upper-left space
        self.at("patients with edema")
        ed_lbl = T("edema:\nhigh sodium stock", size=22, color=GOLD, line_spacing=0.85).move_to([2.92, 1.05, 0])
        ed_ptr = Arrow(ed_lbl.get_bottom() + LEFT * 0.45 + DOWN * 0.08, edema_dot.get_top() + UP * 0.14,
                       color=GOLD, stroke_width=3.5, buff=0)
        self.play(FadeIn(edema_dot, scale=1.5), FadeIn(ed_lbl), Create(ed_ptr), run_time=0.9)
        self.play(Indicate(edema_dot, color=YELLOW, scale_factor=1.5), run_time=0.8)
        self.finish()


class S11Limits(SpokenScene):
    def construct(self):
        world = FluidWorld(
            icf=ICF_S06, ecf=ECF_S07, k_chips=26, na_chips=14,
            x0=MINI_X0, y0=MINI_Y0, y1=MINI_Y1, scale_x=MINI_SCALE_X,
            dot_r=0.042, chip_w=0.18, chip_h=0.12, label_fmt="{:.1f} L",
        )
        na = ValueTracker(NA_S07)
        dial_g = make_dial(na, center=(-3.8, 2.25, 0), radius=0.58, title_size=22, num_size=24, fmt="{:.0f}")
        frac = make_fraction("sodium + potassium", "all body water", center=(-3.8, -3.05, 0), size=22, bar_w=3.2)

        P, fn, cloud, edema_dot = make_edelman_plot()
        fit_line = P.curve(fn, color=TEXT, width=5)
        r_tag = T("schematic points, r = 0.83", size=22, color=GREY).move_to([3.8, -3.05, 0])
        ed_lbl = T("edema:\nhigh sodium stock", size=22, color=GOLD, line_spacing=0.85).move_to([2.92, 1.05, 0])
        ed_ptr = Arrow(ed_lbl.get_bottom() + LEFT * 0.45 + DOWN * 0.08, edema_dot.get_top() + UP * 0.14,
                       color=GOLD, stroke_width=3.5, buff=0)

        self.add(world.group, dial_g, frac, P, fit_line, cloud, edema_dot, ed_lbl, ed_ptr, r_tag)
        world.start_motion(jiggle_chips=True)

        # Beat 1: "correlation in sick patients, not an experiment"
        self.at("correlation in sick")
        lim_tag = boxed_label("correlation, not experiment", color=GOLD, size=24).move_to([3.8, 3.05, 0])
        self.play(FadeIn(lim_tag, shift=DOWN * 0.1), run_time=0.8)

        # Beat 2: "exchangeable cation is not total cation" -> bring back body sodium tank
        self.at("exchangeable cation")
        na_tank = make_edelman_tanks(center_y=-0.15)[0]
        na_tank.move_to([-0.15, -0.15, 0])
        na_tank.label.next_to(na_tank.outer, UP, buff=0.18)
        self.play(FadeIn(na_tank, shift=UP * 0.1), run_time=0.9)

        # Beat 3: "bone sodium does not exchange" -> dark base relabelled and glows
        self.at("bone sodium")
        bone_lbl = T("bone\nsodium", size=22, color=TEXT, line_spacing=0.85).next_to(na_tank.outer, DOWN, buff=0.45)
        bone_ptr = Arrow(bone_lbl.get_top() + UP * 0.06, na_tank.outer.get_bottom() + DOWN * 0.04,
                         color=GOLD, stroke_width=3.5, buff=0)
        self.play(FadeIn(bone_lbl), Create(bone_ptr), run_time=0.8)
        self.play(Indicate(na_tank.base, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        world = FluidWorld(icf=ICF_S06, ecf=ECF_S07, k_chips=26, na_chips=14, label_fmt="{:.1f} L")
        na = ValueTracker(NA_S07)
        dial_g = make_dial(na, fmt="{:.0f}")
        frac = make_fraction("sodium + potassium", "all body water", size=24, bar_w=3.2)
        door_lbl = T("water only", size=22, color=BLUE).move_to([world.membrane_x(), FULL_Y0 - 0.35, 0])

        self.add(world.group, dial_g, frac, door_lbl)
        world.start_motion(jiggle_chips=True)

        # Beat 1: "too much water for the cation present"
        self.at("too much water")
        big_water = T("all body water", size=29, color=BLUE).move_to(frac.bot)
        self.play(
            swap(frac.bot, big_water, run_time=0.6),
            *[Indicate(d, color=WHITE, scale_factor=1.35) for d in world.water_dots[:24]],
        )
        frac.bot = big_water

        # Beat 2: "low, normal or high" -> three sodium stock piles connected equally to the same low needle
        self.at("body sodium is")
        p_low = make_sodium_pile(3, "low", center=[3.15, -2.55, 0], chip_w=0.22, chip_h=0.14, tag_size=22)
        p_norm = make_sodium_pile(6, "normal", center=[4.45, -2.55, 0], chip_w=0.22, chip_h=0.14, tag_size=22)
        p_high = make_sodium_pile(10, "high", center=[5.75, -2.55, 0], chip_w=0.22, chip_h=0.14, tag_size=22)

        hub_pt = np.array([4.45, -1.25, 0.0])
        lines = VGroup(*[
            Line(p.chips.get_top() + UP * 0.08, hub_pt, color=TEXT, stroke_width=3)
            for p in (p_low, p_norm, p_high)
        ])
        q_mark = T("?", size=56, color=GOLD, weight=BOLD).move_to([2.90, 1.95, 0])

        self.play(
            FadeIn(p_low), FadeIn(p_norm), FadeIn(p_high),
            Create(lines), FadeIn(q_mark),
            run_time=1.0,
        )
        self.play(FadeOut(q_mark), run_time=0.8)
        self.finish()


class S13End(EndCard):
    LINE = "Plasma sodium reports cation per litre of water, not body sodium."
