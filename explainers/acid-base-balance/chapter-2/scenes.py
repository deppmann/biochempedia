"""
Pushing the Same Way — Acid-Base Balance, Chapter 2

COLOUR MAP (one colour per concept for the whole film):
- BLUE   (#58C4DD): bicarbonate (HCO3-), upper tank fluid & dots, kidney-set top term, metabolic labels/arrows
- ORANGE (#FF862F): dissolved carbon dioxide (CO2), lower tank fluid & bubbles, lung-set bottom term, respiratory labels/arrows
- RED    (#FC6255): acid disturbance / drain plug on upper tank
- WHITE  (#E8EAF0): pH gauge, needle, brackets, Winter scale, fraction bar, live readouts, questions
- PINK   (#D147BD): lungs and tracheal/bronchial tubes
- PURPLE (#9A72AC): kidney and renal tube

WORLD CARRIED FROM SCENE TO SCENE (16:9 frame, x in [-6.3, 6.3], y in [-3.5, 3.5]):
- CENTRE: Two stacked clear tanks on one shared 50 mmol/L scale: BLUE bicarbonate above a split WHITE fraction bar,
  ORANGE dissolved CO2 below, fluid heights always computed in proportion to concentration.
- LEFT: PURPLE kidney connected to the upper tank; PINK lungs connected to the lower tank; WHITE readout 'pCO2 XX mmHg' under lungs.
- RIGHT: Vertical WHITE pH gauge (6.0 to 7.6), bright tick at 7.40, live needle ALWAYS computed as 6.1 + log10(HCO3- / (0.03 * pCO2)).
- BOTTOM RIGHT: 'human plasma, 37 C'. BOTTOM LEFT: 'made-up patient' (s02-s10) or 'illustrative: pCO2 40 to 50' (s11-s13).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Lungs swell at resting rate and 24 BLUE dots drift; lungs/lower tank and kidney/upper tank pulse on cue; RED plug pops open and HCO3- twitches down (24 -> 20 -> 24) with computed pH needle twitching (7.40 -> 7.32 -> 7.40).
- s02_kinds: RED plug opens and HCO3- drains steadily from 24 to 12 mmol/L; 12 BLUE dots exit as fluid falls; ratio updates live (20 : 1 -> 10 : 1) and needle drops computed from 6.1 + log10(HCO3-/1.2) to 7.10.
- s03_no_help: Equation '0.03 x 40 = 1.2' builds word by word joining pCO2 40 to the 1.2 mmol/L ORANGE layer; clamp sits on lung tube holding pCO2 at 40; ratio expands to '12 : 1.2 = 10 : 1'; needle settles at 7.10 with faint ghost tick.
- s04_lungs: Clamp lifts; stopwatch ('minutes') morphs to clock ('12 to 24 hours'); lungs swell deeper/faster; ORANGE bubbles stream from lower tank through lungs; pCO2 counts down (40 -> 28) while dCO2 = 0.03*pCO2 thins and computed pH climbs off 7.10.
- s05_measured: pCO2 finishes settling from 28 to 27 mmHg and stops; dCO2 settles at 0.81 (0.03 x 27); ratio settles at '12 : 0.81 = 14.8 : 1'; '6.1 + 1.17 = 7.27' builds under gauge as needle settles at computed 7.27.
- s06_predict: Target line at 7.40 ('full repair') and 'target 20 : 1' appear; '?' blinks beside pCO2 27; question 'For 20 : 1, pCO2 = ?' appears across top.
- s08_answer: Dashed ORANGE ghost level appears at 0.60 (0.03 x 20, 'needs 20 mmHg') below real 0.81 ('27'); working '12 ÷ 20 = 0.6' and '0.6 ÷ 0.03 = 20 mmHg' build beside lower tank; WHITE bracket measures 7.10 -> 7.27 ('0.17 bought back'); dashed bracket measures 7.27 -> 7.40 ('not all').
- s09_idea: BLUE and ORANGE down-arrows pulse together ('same way'); needle glows at 7.27; ghost needle rises to 7.37 ('some chronic cases') and fades; 7.40 dashed line becomes solid WHITE wall ('never past 7.40').
- s10_winter: Vertical pCO2 scale (20 to 40) slides in beside readout; general formula '1.5 x HCO3- + 8 ± 2' builds, then '1.5 x 12 + 8 = 26' and '26 ± 2' build; band 24-28 lights ('expected'); marker drops at 27 inside band while 20 sits below; seeded scatter cloud (rng=7) appears ('schematic scatter', 'a fit, not a law').
- s11_respiratory: Resets to rest (24 / 1.2, pCO2 40, pH 7.40); lungs slow/shallow and pCO2 climbs 40 -> 50 (dCO2 -> 1.50, computed needle drops to 7.30); buffering raises HCO3- 24 -> 25 ('+1 at once: other blood buffers'); kidney glows PURPLE, BLUE dots flow into upper tank raising HCO3- to 29 ('+5 over days', computed needle 7.39 < 7.40); '0.03 x 50 = 1.5' and '20 x 1.5 = 30' build as dashed ghost at 30 ('+6 for full') appears.
- s12_two_things: Arrows beside tanks flip opposite ('two processes') then return same way; ghost Winter band appears with marker sliding well outside ('off the fit'); both labels pulse and fade.
- s13_close: World shifts to metabolic compensation case (12 / 0.81, pH 7.27), then morphs to respiratory compensation case (29 / 1.50, pH 7.39); solid 7.40 wall pulses while both positions remain below it.
"""

from bp_parts import *  # noqa: F401,F403

# ------------------------------------------------------------------ Constants & Computed Model
BICARB_COLOR = BLUE
CO2_COLOR = ORANGE
ACID_COLOR = RED
GAUGE_COLOR = WHITE
LUNG_COLOR = PINK
KIDNEY_COLOR = PURPLE

CO2_SOL = 0.03
PK = 6.1
FULL_SCALE_MMOL = 50.0

# Tank geometry (centre column)
TANK_X = -0.32
TANK_W = 2.24
TANK_H = 2.14
TANK_GAP = 0.56
UPPER_BOT = TANK_GAP / 2.0      # +0.28
UPPER_TOP = UPPER_BOT + TANK_H  # +2.42
LOWER_TOP = -TANK_GAP / 2.0     # -0.28
LOWER_BOT = LOWER_TOP - TANK_H  # -2.42
H_SCALE = TANK_H / FULL_SCALE_MMOL

# Organ positions (left column)
KIDNEY_POS = np.array([-5.00, 1.50, 0.0])
LUNG_POS = np.array([-5.00, -0.68, 0.0])
PCO2_POS = np.array([-5.05, -2.02, 0.0])

# Gauge geometry (right column)
GAUGE_X = 4.15
GAUGE_Y0 = -2.35  # pH 6.0
GAUGE_Y1 = 2.45   # pH 7.6
PH_MIN = 6.0
PH_MAX = 7.6


def dco2_of(pco2):
    return CO2_SOL * float(pco2)


def ph_of(hco3, pco2):
    d = max(dco2_of(pco2), 1e-4)
    h = max(float(hco3), 1e-4)
    return PK + np.log10(h / d)


def ph_to_y(ph):
    frac = (float(ph) - PH_MIN) / (PH_MAX - PH_MIN)
    return GAUGE_Y0 + np.clip(frac, 0.0, 1.0) * (GAUGE_Y1 - GAUGE_Y0)


def fluid_rect(h_bot, mmol, color, opacity=0.62):
    h = max(0.015, float(mmol) * H_SCALE)
    r = Rectangle(
        width=TANK_W - 0.12,
        height=h,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=color,
        stroke_width=1.8,
    )
    r.move_to([TANK_X, h_bot + 0.03 + h / 2.0, 0.0])
    return r


def make_tank_outline(y_bot, y_top, color=TEXT):
    """Glass tank outline drawn over fluid via z_index=3."""
    rect = RoundedRectangle(
        corner_radius=0.10,
        width=TANK_W,
        height=y_top - y_bot,
        stroke_color=color,
        stroke_width=3.2,
        fill_opacity=0.0,
    ).move_to([TANK_X, (y_bot + y_top) / 2.0, 0.0])
    rect.set_z_index(3)
    return rect


def make_kidney(center=KIDNEY_POS):
    """Stylized bean-shaped kidney with hilum indentation and renal tube to upper tank."""
    pts = [
        [-0.38, 0.66, 0],
        [0.34, 0.72, 0],
        [0.62, 0.32, 0],
        [0.32, 0.06, 0],
        [0.32, -0.06, 0],
        [0.62, -0.32, 0],
        [0.34, -0.72, 0],
        [-0.38, -0.66, 0],
        [-0.70, -0.26, 0],
        [-0.70, 0.26, 0],
    ]
    bean = VMobject(stroke_color=KIDNEY_COLOR, stroke_width=4.4, fill_color=KIDNEY_COLOR, fill_opacity=0.44)
    bean.set_points_smoothly([np.array(p) + center for p in pts] + [np.array(pts[0]) + center])
    pelvis = ArcBetweenPoints(
        center + np.array([0.24, 0.20, 0]),
        center + np.array([0.24, -0.20, 0]),
        angle=1.2,
        color=KIDNEY_COLOR,
        stroke_width=3.2,
    )
    tube_start = center + np.array([0.36, 0.0, 0])
    tube_end = np.array([TANK_X - TANK_W / 2.0 - 0.04, center[1], 0.0])
    tube = Line(tube_start, tube_end, color=KIDNEY_COLOR, stroke_width=4.2)
    organ = VGroup(bean, pelvis)
    organ.set_z_index(2)
    tube.set_z_index(1)
    return organ, tube


def make_lungs(center=LUNG_POS):
    """Stylized symmetrical lungs with trachea and tube to lower tank."""
    def lobe(sign):
        pts = [
            [sign * 0.14, 0.48, 0],
            [sign * 0.52, 0.40, 0],
            [sign * 0.76, -0.16, 0],
            [sign * 0.72, -0.62, 0],
            [sign * 0.22, -0.58, 0],
            [sign * 0.12, -0.10, 0],
        ]
        m = VMobject(stroke_color=LUNG_COLOR, stroke_width=4.2, fill_color=LUNG_COLOR, fill_opacity=0.42)
        m.set_points_smoothly([np.array(p) + center for p in pts] + [np.array(pts[0]) + center])
        return m

    lobe_l = lobe(-1)
    lobe_r = lobe(1)
    trachea = Line(center + np.array([0, 0.78, 0]), center + np.array([0, 0.26, 0]), color=LUNG_COLOR, stroke_width=5.2)
    bronch_l = Line(center + np.array([0, 0.28, 0]), center + np.array([-0.34, 0.04, 0]), color=LUNG_COLOR, stroke_width=3.4)
    bronch_r = Line(center + np.array([0, 0.28, 0]), center + np.array([0.34, 0.04, 0]), color=LUNG_COLOR, stroke_width=3.4)
    lungs_body = VGroup(lobe_l, lobe_r, trachea, bronch_l, bronch_r)
    lungs_body.set_z_index(2)
    tube_start = center + np.array([0.74, -0.08, 0])
    tube_end = np.array([TANK_X - TANK_W / 2.0 - 0.04, center[1] - 0.08, 0.0])
    tube = Line(tube_start, tube_end, color=LUNG_COLOR, stroke_width=4.2)
    tube.set_z_index(1)
    return lungs_body, tube


def make_bicarb_dots(hco3_t, seed=7):
    """Seeded BLUE dots representing bicarbonate (1 dot per mmol/L, active count = round(hco3))."""
    rng = np.random.default_rng(seed)
    max_n = 30
    coords = []
    for _ in range(max_n):
        fx = rng.uniform(-0.84, 0.84)
        fy = rng.uniform(0.10, 0.90)
        vx = rng.uniform(-0.46, 0.46)
        vy = rng.uniform(-0.28, 0.28)
        coords.append([fx, fy, vx, vy])

    dots = VGroup()
    state = {"coords": coords}
    for _ in range(max_n):
        d = Dot(radius=0.072, color=BICARB_COLOR, fill_opacity=0.95)
        d.set_z_index(1)
        dots.add(d)

    def update_dots(mob, dt):
        val = float(hco3_t.get_value())
        active_n = int(np.clip(round(val), 0, max_n))
        fluid_h = max(0.22, val * H_SCALE)
        half_w = (TANK_W - 0.30) / 2.0
        for idx, d in enumerate(mob):
            if idx >= active_n:
                d.set_opacity(0.0)
                continue
            d.set_opacity(0.95)
            c = state["coords"][idx]
            c[0] += c[2] * dt
            c[1] += c[3] * dt
            if c[0] > 0.90 or c[0] < -0.90:
                c[2] *= -1
                c[0] = np.clip(c[0], -0.90, 0.90)
            if c[1] > 0.90 or c[1] < 0.10:
                c[3] *= -1
                c[1] = np.clip(c[1], 0.10, 0.90)
            x = TANK_X + c[0] * half_w
            y = UPPER_BOT + 0.06 + c[1] * max(fluid_h - 0.10, 0.10)
            d.move_to([x, y, 0.0])

    dots.add_updater(update_dots)
    update_dots(dots, 0.0)
    return dots


def make_co2_bubbles(rate_t, seed=11):
    """ORANGE bubbles streaming vertically up centre of lower tank, through lung tube, and out trachea."""
    rng = np.random.default_rng(seed)
    n_bub = 12
    phases = [i / n_bub + rng.uniform(-0.02, 0.02) for i in range(n_bub)]
    offsets = [rng.uniform(-0.05, 0.05) for _ in range(n_bub)]
    bubbles = VGroup()
    for _ in range(n_bub):
        b = Circle(radius=0.058, color=CO2_COLOR, stroke_width=2.4, fill_color=CO2_COLOR, fill_opacity=0.55)
        b.set_z_index(1)
        bubbles.add(b)

    # Clean interior path: left-centre of lower tank -> up -> left out tube -> lungs -> trachea
    p0 = np.array([TANK_X - 0.68, LOWER_BOT + 0.10, 0.0])
    p1 = np.array([TANK_X - 0.68, LUNG_POS[1] - 0.08, 0.0])
    p2 = np.array([TANK_X - TANK_W / 2.0 - 0.08, LUNG_POS[1] - 0.08, 0.0])
    p3 = np.array([LUNG_POS[0], LUNG_POS[1] - 0.08, 0.0])
    p4 = np.array([LUNG_POS[0], LUNG_POS[1] + 0.85, 0.0])
    pts = [p0, p1, p2, p3, p4]
    segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(4)]
    tot = sum(segs)
    cum = [0.0]
    for s in segs:
        cum.append(cum[-1] + s / tot)

    def sample_path(s):
        s = s % 1.0
        for i in range(4):
            if s <= cum[i + 1]:
                u = (s - cum[i]) / max(cum[i + 1] - cum[i], 1e-6)
                return (1.0 - u) * pts[i] + u * pts[i + 1]
        return pts[-1]

    def update_bubbles(mob, dt):
        r = float(rate_t.get_value())
        for i, b in enumerate(mob):
            if r <= 0.02:
                b.set_opacity(0.0)
                continue
            phases[i] = (phases[i] + r * dt * 0.34) % 1.0
            pos = sample_path(phases[i])
            pos = pos + np.array([offsets[i] * 0.5, offsets[i] * 0.5, 0.0])
            b.move_to(pos)
            alpha = 0.88 if phases[i] < 0.85 else max(0.0, (1.0 - phases[i]) / 0.15) * 0.88
            b.set_fill(opacity=alpha * 0.58)
            b.set_stroke(opacity=alpha)

    bubbles.add_updater(update_bubbles)
    update_bubbles(bubbles, 0.0)
    return bubbles


def make_ph_gauge(hco3_t, pco2_t, wall_mode=False, tremble_t=None, show_740_lbl=True):
    """Vertical pH gauge (6.0 to 7.6) with computed needle and 7.40 mark."""
    spine = Line([GAUGE_X, GAUGE_Y0, 0], [GAUGE_X, GAUGE_Y1, 0], color=GAUGE_COLOR, stroke_width=4.2)
    track = Rectangle(
        width=0.26,
        height=GAUGE_Y1 - GAUGE_Y0,
        stroke_width=0.0,
        fill_color=GAUGE_COLOR,
        fill_opacity=0.18,
    ).move_to([GAUGE_X, (GAUGE_Y0 + GAUGE_Y1) / 2.0, 0.0])

    title = T("pH", 28, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X, GAUGE_Y1 + 0.44, 0.0])

    ticks = VGroup()
    for val, lbl in [(6.0, "6.0"), (6.5, "6.5"), (7.0, "7.0"), (7.6, "7.6")]:
        y = ph_to_y(val)
        tk = Line([GAUGE_X - 0.14, y, 0], [GAUGE_X, y, 0], color=GAUGE_COLOR, stroke_width=2.6)
        lb = M(lbl, 22, TEXT).next_to(tk, LEFT, buff=0.10)
        ticks.add(tk, lb)

    y74 = ph_to_y(7.40)
    tick74 = Line([GAUGE_X - 0.12, y74, 0], [GAUGE_X + 0.52, y74, 0], color=GAUGE_COLOR, stroke_width=5.0 if wall_mode else 3.5)
    lbl74 = M("7.40", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X + 0.62, y74, 0.0], aligned_edge=LEFT)

    def build_needle():
        ph = ph_of(hco3_t.get_value(), pco2_t.get_value())
        if tremble_t is not None:
            ph += 0.008 * np.sin(5.0 * tremble_t.get_value())
        ny = ph_to_y(ph)
        tri = Polygon(
            [GAUGE_X + 0.06, ny, 0],
            [GAUGE_X + 0.30, ny + 0.11, 0],
            [GAUGE_X + 0.30, ny - 0.11, 0],
            color=GAUGE_COLOR,
            fill_color=GAUGE_COLOR,
            fill_opacity=1.0,
            stroke_width=1.5,
        )
        bar = Line([GAUGE_X - 0.10, ny, 0], [GAUGE_X + 0.08, ny, 0], color=GAUGE_COLOR, stroke_width=4.0)
        g = VGroup(bar, tri)
        g.set_z_index(4)
        return g

    needle = always_redraw(build_needle)
    return VGroup(track, spine, title, ticks), tick74, lbl74, needle


def make_fraction_bar(ratio_text_fn):
    """Split WHITE fraction bar that always leaves a clean gap around the centered ratio label."""
    def mk():
        txt_str = ratio_text_fn()
        sz = 22 if len(txt_str) > 10 else 26
        lbl = M(txt_str, sz, GAUGE_COLOR, weight=BOLD).move_to([TANK_X, 0.0, 0.0])
        pad = 0.14
        left_x = min(TANK_X - 1.32, lbl.get_left()[0] - 0.34)
        right_x = max(TANK_X + 1.32, lbl.get_right()[0] + 0.34)
        l_bar = Line([left_x, 0.0, 0.0], [lbl.get_left()[0] - pad, 0.0, 0.0], color=GAUGE_COLOR, stroke_width=5.0)
        r_bar = Line([lbl.get_right()[0] + pad, 0.0, 0.0], [right_x, 0.0, 0.0], color=GAUGE_COLOR, stroke_width=5.0)
        return VGroup(l_bar, r_bar, lbl)
    return always_redraw(mk)


def make_plug(open_t):
    """RED plug on the bottom-right floor of the upper tank; pops downward when open_t goes 0 -> 1."""
    base_x = TANK_X + 0.78
    base_y = UPPER_BOT

    def mk():
        o = float(open_t.get_value())
        plug = RoundedRectangle(
            corner_radius=0.04,
            width=0.28,
            height=0.12,
            stroke_color=ACID_COLOR,
            stroke_width=2.0,
            fill_color=ACID_COLOR,
            fill_opacity=0.95,
        )
        plug.move_to([base_x + 0.08 * o, base_y - 0.13 * o, 0.0])
        plug.rotate(-0.45 * o)
        plug.set_z_index(4)
        return plug

    return always_redraw(mk)


class AcidBaseWorld:
    """Shared builder for the persistent world across s00..s13."""

    def __init__(
        self,
        hco3=24.0,
        pco2=40.0,
        breath_amp=0.105,
        breath_speed=2.4,
        bubble_rate=0.0,
        ratio_mode="simple",
        patient_tag="made-up patient",
        show_patient_tag=False,
        ghost_710=False,
        wall_740=False,
        dashed_740=False,
        show_740_lbl=True,
        show_numbers=True,
        tremble=False,
    ):
        self.hco3_t = ValueTracker(hco3)
        self.pco2_t = ValueTracker(pco2)
        self.breath_amp_t = ValueTracker(breath_amp)
        self.breath_speed_t = ValueTracker(breath_speed)
        self.bubble_rate_t = ValueTracker(bubble_rate)
        self.plug_open_t = ValueTracker(0.0)
        self.tremble_t = ValueTracker(0.0) if tremble else None

        self.ratio_mode = ratio_mode
        self.show_numbers = show_numbers
        self.show_740_lbl = show_740_lbl

        # Tanks
        self.upper_outline = make_tank_outline(UPPER_BOT, UPPER_TOP)
        self.lower_outline = make_tank_outline(LOWER_BOT, LOWER_TOP)
        self.upper_fluid = always_redraw(lambda: fluid_rect(UPPER_BOT, self.hco3_t.get_value(), BICARB_COLOR, 0.58))
        self.lower_fluid = always_redraw(lambda: fluid_rect(LOWER_BOT, dco2_of(self.pco2_t.get_value()), CO2_COLOR, 0.80))

        self.bicarb_label = T("bicarbonate", 28, BICARB_COLOR, weight=BOLD).move_to([TANK_X, UPPER_TOP + 0.24, 0.0])
        self.co2_label = T("dissolved CO2", 28, CO2_COLOR, weight=BOLD).move_to([TANK_X, LOWER_BOT - 0.24, 0.0])

        # Ratio bar
        def ratio_str():
            h = self.hco3_t.get_value()
            d = dco2_of(self.pco2_t.get_value())
            r = h / max(d, 1e-4)
            if self.ratio_mode == "full_12":
                return f"12 : {d:.2f} = {r:.1f} : 1"
            if self.ratio_mode == "full_12_int":
                return "12 : 1.2 = 10 : 1"
            if self.ratio_mode == "none":
                return "HCO3- / CO2"
            return f"{r:.0f} : 1"

        self.fraction_bar = make_fraction_bar(ratio_str)

        # Organs
        self.kidney, self.kidney_tube = make_kidney()
        self.kidney_label = T("kidney", 28, KIDNEY_COLOR, weight=BOLD).move_to([KIDNEY_POS[0], KIDNEY_POS[1] + 0.96, 0.0])

        self.lungs, self.lung_tube = make_lungs()
        self.lungs_label = T("lungs", 28, LUNG_COLOR, weight=BOLD).move_to([LUNG_POS[0], LUNG_POS[1] + 1.05, 0.0])

        self._lung_base = self.lungs.copy()
        self._lung_phase = 0.0

        def breathe(mob, dt):
            amp = float(self.breath_amp_t.get_value())
            spd = float(self.breath_speed_t.get_value())
            self._lung_phase += dt * spd
            s = 1.0 + amp * np.sin(self._lung_phase)
            ref = self._lung_base.copy().scale(s, about_point=LUNG_POS)
            for part, ref_part in zip(mob, ref):
                part.match_points(ref_part)

        self.lungs.add_updater(breathe)

        if self.tremble_t is not None:
            self.tremble_t.add_updater(lambda m, dt: m.increment_value(dt))

        self.bicarb_dots = make_bicarb_dots(self.hco3_t)
        self.co2_bubbles = make_co2_bubbles(self.bubble_rate_t)
        self.plug = make_plug(self.plug_open_t)

        # Readouts (aligned_edge=LEFT clear of tank right walls)
        tank_right = TANK_X + TANK_W / 2.0
        self.pco2_readout = always_redraw(
            lambda: M(f"pCO2 {self.pco2_t.get_value():.0f} mmHg", 26, GAUGE_COLOR).move_to(PCO2_POS)
        )
        self.hco3_num = always_redraw(
            lambda: M(f"{self.hco3_t.get_value():.0f}", 30, BICARB_COLOR, weight=BOLD).move_to([tank_right + 0.22, UPPER_BOT + 0.72, 0.0], aligned_edge=LEFT)
        )
        self.dco2_num = always_redraw(
            lambda: M(
                "1.2" if abs(dco2_of(self.pco2_t.get_value()) - 1.2) < 0.01 else f"{dco2_of(self.pco2_t.get_value()):.2f}",
                28,
                CO2_COLOR,
                weight=BOLD,
            ).move_to([tank_right + 0.22, LOWER_BOT + 0.30, 0.0], aligned_edge=LEFT)
        )

        # Gauge
        self.gauge_base, self.tick74, self.lbl74, self.needle = make_ph_gauge(
            self.hco3_t, self.pco2_t, wall_mode=wall_740, tremble_t=self.tremble_t
        )

        self.ghost_710 = None
        if ghost_710:
            y71 = ph_to_y(7.10)
            self.ghost_710 = Line([GAUGE_X - 0.12, y71, 0], [GAUGE_X + 0.44, y71, 0], color=GAUGE_COLOR, stroke_width=2.5).set_opacity(0.55)

        self.dashed_740_line = None
        if dashed_740:
            y74 = ph_to_y(7.40)
            self.dashed_740_line = DashedLine([GAUGE_X - 0.30, y74, 0], [GAUGE_X + 0.54, y74, 0], color=GAUGE_COLOR, stroke_width=3.2, dash_length=0.10)

        self.wall_740_line = None
        self.wall_740_lbl = None
        if wall_740:
            y74 = ph_to_y(7.40)
            self.wall_740_line = Line([GAUGE_X - 0.30, y74, 0], [GAUGE_X + 0.56, y74, 0], color=GAUGE_COLOR, stroke_width=6.0)
            self.wall_740_lbl = T("never past 7.40", 22, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X + 0.30, y74 + 0.28, 0.0], aligned_edge=LEFT)

        self.plasma_tag = T("human plasma, 37 C", 24, TEXT).move_to([6.20, -3.26, 0.0], aligned_edge=RIGHT)
        self.patient_tag = T(patient_tag, 24, TEXT).move_to([-6.20, -3.26, 0.0], aligned_edge=LEFT)
        self.show_patient_tag = show_patient_tag

    def base_group(self):
        items = [
            self.upper_fluid,
            self.lower_fluid,
            self.bicarb_dots,
            self.co2_bubbles,
            self.upper_outline,
            self.lower_outline,
            self.plug,
            self.bicarb_label,
            self.co2_label,
            self.fraction_bar,
            self.kidney_tube,
            self.kidney,
            self.kidney_label,
            self.lung_tube,
            self.lungs,
            self.lungs_label,
            self.gauge_base,
            self.tick74,
            self.needle,
            self.plasma_tag,
        ]
        if self.wall_740_line:
            items.extend([self.wall_740_line, self.wall_740_lbl])
        elif self.show_740_lbl:
            items.append(self.lbl74)
        if self.dashed_740_line:
            items.append(self.dashed_740_line)
        if self.ghost_710:
            items.append(self.ghost_710)
        if self.show_numbers:
            items.extend([self.pco2_readout, self.hco3_num, self.dco2_num])
        if self.show_patient_tag:
            items.append(self.patient_tag)
        if self.tremble_t is not None:
            items.append(self.tremble_t)
        return Group(*items)


def make_clamp(pos):
    top_jaw = Line(pos + UP * 0.26 + LEFT * 0.14, pos + UP * 0.06 + RIGHT * 0.14, color=GAUGE_COLOR, stroke_width=4.0)
    bot_jaw = Line(pos + DOWN * 0.26 + LEFT * 0.14, pos + DOWN * 0.06 + RIGHT * 0.14, color=GAUGE_COLOR, stroke_width=4.0)
    bar = Line(pos + UP * 0.28 + LEFT * 0.14, pos + DOWN * 0.28 + LEFT * 0.14, color=GAUGE_COLOR, stroke_width=4.0)
    g = VGroup(top_jaw, bot_jaw, bar)
    g.set_z_index(5)
    return g


def make_stopwatch(center, label_text="minutes"):
    rim = Circle(radius=0.28, color=GAUGE_COLOR, stroke_width=3.0).move_to(center)
    crown = Line(center + UP * 0.28, center + UP * 0.40, color=GAUGE_COLOR, stroke_width=4.0)
    hand = Line(center, center + UR * 0.17, color=CO2_COLOR, stroke_width=3.5)
    lbl = T(label_text, 24, GAUGE_COLOR).next_to(rim, DOWN, buff=0.12)
    return VGroup(rim, crown, hand, lbl)


def make_clock(center, label_text="12 to 24 hours"):
    rim = Circle(radius=0.30, color=GAUGE_COLOR, stroke_width=3.0).move_to(center)
    h_hand = Line(center, center + UP * 0.16, color=GAUGE_COLOR, stroke_width=3.5)
    m_hand = Line(center, center + RIGHT * 0.21, color=CO2_COLOR, stroke_width=3.0)
    lbl = T(label_text, 24, GAUGE_COLOR).next_to(rim, DOWN, buff=0.12)
    return VGroup(rim, h_hand, m_hand, lbl)


def make_calendar(center, label_text="days"):
    box = RoundedRectangle(corner_radius=0.06, width=0.60, height=0.54, stroke_color=GAUGE_COLOR, stroke_width=3.0, fill_color=BG, fill_opacity=0.85).move_to(center)
    top_bar = Line(box.get_corner(UL) + DOWN * 0.15, box.get_corner(UR) + DOWN * 0.15, color=KIDNEY_COLOR, stroke_width=3.5)
    grid = VGroup(*[Dot(radius=0.028, color=GAUGE_COLOR).move_to(box.get_center() + [dx, dy - 0.06, 0]) for dx in (-0.14, 0, 0.14) for dy in (-0.07, 0.07)])
    lbl = T(label_text, 24, GAUGE_COLOR).next_to(box, DOWN, buff=0.10)
    return VGroup(box, top_bar, grid, lbl)


def make_dir_arrow(pos, direction, color, label_text=None):
    start = pos - direction * 0.36
    end = pos + direction * 0.36
    arr = Arrow(start, end, buff=0.0, color=color, stroke_width=6.0, max_tip_length_to_length_ratio=0.32)
    if label_text:
        lbl = T(label_text, 24, color, weight=BOLD).next_to(arr, RIGHT, buff=0.14)
        return VGroup(arr, lbl)
    return arr


def make_calc_line(pco2_t):
    """WHITE connector line below pCO2 readout + equation '0.03 x pCO2 = dCO2' clear of tank and readout."""
    def mk():
        p = float(pco2_t.get_value())
        d = dco2_of(p)
        d_str = "1.2" if abs(d - 1.2) < 0.005 else f"{d:.2f}"
        eq = M(f"0.03 × {p:.0f} = {d_str}", 22, GAUGE_COLOR).move_to([-1.66, -1.66, 0.0], aligned_edge=RIGHT)
        conn = Line([-4.35, -2.30, 0.0], [TANK_X - TANK_W / 2.0 - 0.10, LOWER_BOT + 0.08, 0.0], color=GAUGE_COLOR, stroke_width=2.5)
        return VGroup(conn, eq)
    return always_redraw(mk)


def make_winter_scale(x_pos=-3.45, y_bot=-2.45, y_top=-1.25, p_min=20.0, p_max=40.0):
    """Short vertical WHITE scale of pCO2 (20 to 40 mmHg) beside readout under lungs."""
    def py(v):
        return y_bot + ((v - p_min) / (p_max - p_min)) * (y_top - y_bot)

    spine = Line([x_pos, y_bot, 0], [x_pos, y_top, 0], color=GAUGE_COLOR, stroke_width=3.0)
    ticks = VGroup()
    for v in (20, 40):
        y = py(v)
        tk = Line([x_pos - 0.10, y, 0], [x_pos + 0.10, y, 0], color=GAUGE_COLOR, stroke_width=2.5)
        lb = M(str(v), 22, TEXT).next_to(tk, LEFT, buff=0.08)
        ticks.add(tk, lb)

    band_h = py(28) - py(24)
    band = Rectangle(
        width=0.46,
        height=band_h,
        fill_color=GAUGE_COLOR,
        fill_opacity=0.22,
        stroke_color=GAUGE_COLOR,
        stroke_width=2.0,
    ).move_to([x_pos + 0.23, (py(24) + py(28)) / 2.0, 0.0])
    band_lbl = T("expected\n24–28", 22, GAUGE_COLOR, line_spacing=0.85).move_to([x_pos + 0.58, (py(24) + py(28)) / 2.0 - 0.04, 0.0], aligned_edge=LEFT)
    return spine, ticks, band, band_lbl, py


def flash_highlight(scene, mob, color=GOLD, run_time=0.8):
    """Momentary highlight underline below a live readout without mutating always_redraw submobjects."""
    y = mob.get_bottom()[1] - 0.08
    ul = Line([mob.get_left()[0], y, 0], [mob.get_right()[0], y, 0], color=color, stroke_width=4.5)
    scene.play(Create(ul, run_time=run_time * 0.45))
    scene.play(FadeOut(ul, run_time=run_time * 0.55))


# ------------------------------------------------------------------ Scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(hco3=24.0, pco2=40.0, breath_amp=0.105, breath_speed=2.4, bubble_rate=0.0)
        self.add(w.base_group())

        self.wait(1.0)
        flash_highlight(self, w.fraction_bar, color=GAUGE_COLOR, run_time=1.8)

        self.at("lungs keep its bottom")
        self.play(
            Indicate(w.lungs, color=LUNG_COLOR, scale_factor=1.10),
            Indicate(w.lower_outline, color=CO2_COLOR, scale_factor=1.05),
            run_time=1.4,
        )

        self.at("kidney keeps its top")
        self.play(
            Indicate(w.kidney, color=KIDNEY_COLOR, scale_factor=1.10),
            Indicate(w.upper_outline, color=BICARB_COLOR, scale_factor=1.05),
            run_time=2.2,
        )

        self.at("pushes one term")
        self.play(w.plug_open_t.animate.set_value(1.0), w.hco3_t.animate.set_value(20.0), run_time=0.75)
        self.play(w.plug_open_t.animate.set_value(0.0), w.hco3_t.animate.set_value(24.0), run_time=0.75)

        self.at("what does the other")
        q = T("What does the other keeper do?", 36, GAUGE_COLOR, weight=BOLD).move_to([0.0, 3.30, 0.0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=1.0)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = AcidBaseWorld(hco3=24.0, pco2=40.0, breath_amp=0.105, breath_speed=2.4, bubble_rate=0.0)
        q = T("What does the other keeper do?", 36, GAUGE_COLOR, weight=BOLD).move_to([0.0, 3.30, 0.0])
        title = T("Pushing the Same Way", 44, GAUGE_COLOR, font=TITLE_FONT, weight=BOLD).move_to([0.0, 3.30, 0.0])
        self.add(w.base_group(), q)
        self.play(FadeOut(q, run_time=0.4), FadeIn(title, run_time=0.45))
        self.wait(1.15)
        self.play(FadeOut(title, run_time=0.35))
        self.finish()


class S02Kinds(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(hco3=24.0, pco2=40.0, breath_amp=0.105, breath_speed=2.4, bubble_rate=0.0, show_patient_tag=False)
        self.add(w.base_group())

        resp_lbl = T("respiratory", 28, CO2_COLOR, weight=BOLD).move_to([2.15, -1.35, 0.0])
        meta_lbl = T("metabolic", 28, BICARB_COLOR, weight=BOLD).move_to([2.15, 1.85, 0.0])

        self.play(Indicate(w.lower_outline, color=CO2_COLOR, scale_factor=1.04), run_time=2.4)

        self.at("is respiratory")
        self.play(FadeIn(resp_lbl, shift=RIGHT * 0.1), Indicate(w.lungs, color=LUNG_COLOR, scale_factor=1.10), run_time=2.0)

        self.play(Indicate(w.upper_outline, color=BICARB_COLOR, scale_factor=1.04), run_time=1.8)

        self.at("it is metabolic")
        self.play(FadeIn(meta_lbl, shift=RIGHT * 0.1), Indicate(w.kidney, color=KIDNEY_COLOR, scale_factor=1.10), run_time=2.0)

        self.at("metabolic acidosis")
        self.play(FadeOut(resp_lbl, run_time=0.8), FadeIn(w.patient_tag, run_time=1.0))

        self.at("falls from", lead=0.45)
        self.play(w.plug_open_t.animate.set_value(1.0), run_time=0.3)
        self.play(w.hco3_t.animate.set_value(12.0), run_time=1.2, rate_func=linear)
        self.play(w.plug_open_t.animate.set_value(0.0), run_time=0.25)
        self.finish()


class S03NoHelp(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(hco3=12.0, pco2=40.0, breath_amp=0.105, breath_speed=2.4, bubble_rate=0.0, show_patient_tag=True)
        meta_lbl = T("metabolic", 28, BICARB_COLOR, weight=BOLD).move_to([2.15, 1.85, 0.0])
        self.add(w.base_group(), meta_lbl)

        c1 = M("0.03", 22, GAUGE_COLOR)
        c2 = M("×", 22, GAUGE_COLOR)
        c3 = M("40", 22, GAUGE_COLOR)
        c4 = M("= 1.2", 22, GAUGE_COLOR)
        VGroup(c1, c2, c3, c4).arrange(RIGHT, buff=0.14).move_to([-1.66, -1.66, 0.0], aligned_edge=RIGHT)
        conn = Line([-4.35, -2.30, 0.0], [TANK_X - TANK_W / 2.0 - 0.10, LOWER_BOT + 0.08, 0.0], color=GAUGE_COLOR, stroke_width=2.5)

        self.at("dissolved carbon dioxide")
        self.play(Indicate(w.lower_outline, color=CO2_COLOR, scale_factor=1.06), run_time=2.0)

        self.at("0")
        self.play(Create(conn), FadeIn(c1), run_time=0.8)

        self.at("times its pressure")
        self.play(FadeIn(c2), run_time=0.4)
        flash_highlight(self, w.pco2_readout, color=CO2_COLOR, run_time=1.3)

        self.at("40")
        self.play(FadeIn(c3), run_time=0.7)

        self.at("that is", lead=-0.2)
        self.play(FadeIn(c4), run_time=0.5)
        flash_highlight(self, w.dco2_num, color=CO2_COLOR, run_time=1.4)

        self.at("hold it there")
        clamp = make_clamp(np.array([-2.85, -0.76, 0.0]))
        self.play(FadeIn(clamp, shift=DOWN * 0.2), run_time=0.9)

        self.at("ratio drops to")
        w.ratio_mode = "full_12_int"
        self.wait(0.05)
        flash_highlight(self, w.fraction_bar, color=GAUGE_COLOR, run_time=2.2)

        self.at("would fall to")
        y71 = ph_to_y(7.10)
        ghost = Line([GAUGE_X - 0.12, y71, 0], [GAUGE_X + 0.44, y71, 0], color=GAUGE_COLOR, stroke_width=2.5).set_opacity(0.55)
        no_help = T("7.10, no help", 22, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X + 0.56, y71, 0.0], aligned_edge=LEFT)
        self.add(ghost)
        self.wait(0.45)
        self.play(FadeIn(no_help), run_time=0.9)
        self.finish()


class S04Lungs(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=12.0, pco2=40.0, breath_amp=0.105, breath_speed=2.4, bubble_rate=0.0,
            ratio_mode="full_12", show_patient_tag=True, ghost_710=True,
        )
        meta_lbl = T("metabolic", 28, BICARB_COLOR, weight=BOLD).move_to([2.15, 1.85, 0.0])
        calc = make_calc_line(w.pco2_t)
        clamp = make_clamp(np.array([-2.85, -0.76, 0.0]))
        y71 = ph_to_y(7.10)
        no_help = T("7.10, no help", 22, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X + 0.56, y71, 0.0], aligned_edge=LEFT)
        self.add(w.base_group(), meta_lbl, calc, clamp, no_help)

        self.at("within minutes")
        sw = make_stopwatch(np.array([-2.85, 0.92, 0.0]), "minutes")
        self.play(FadeOut(clamp, shift=UP * 0.25, run_time=0.45), FadeOut(no_help, run_time=0.35), FadeIn(sw, run_time=0.45))

        self.at("begins to deepen")
        self.play(
            w.breath_amp_t.animate.set_value(0.132),
            w.breath_speed_t.animate.set_value(3.2),
            w.bubble_rate_t.animate.set_value(1.1),
            w.pco2_t.animate.set_value(28.0),
            run_time=5.4,
            rate_func=linear,
        )

        self.at("over about")
        clk = make_clock(np.array([-2.85, 0.92, 0.0]), "12 to 24 hours")
        self.play(FadeOut(sw, run_time=0.35), FadeIn(clk, run_time=0.55))

        self.at("both terms fall")
        arr_u = make_dir_arrow(np.array([1.85, 1.15, 0.0]), DOWN, BICARB_COLOR, "down")
        arr_d = make_dir_arrow(np.array([1.85, -1.15, 0.0]), DOWN, CO2_COLOR, "down")
        self.play(FadeIn(arr_u), FadeIn(arr_d), run_time=1.0)
        self.finish()


class S05Measured(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=12.0, pco2=28.0, breath_amp=0.132, breath_speed=3.2, bubble_rate=1.1,
            ratio_mode="full_12", show_patient_tag=True, ghost_710=True,
        )
        meta_lbl = T("metabolic", 28, BICARB_COLOR, weight=BOLD).move_to([2.15, 1.85, 0.0])
        calc = make_calc_line(w.pco2_t)
        clk = make_clock(np.array([-2.85, 0.92, 0.0]), "12 to 24 hours")
        arr_u = make_dir_arrow(np.array([1.85, 1.15, 0.0]), DOWN, BICARB_COLOR, "down")
        arr_d = make_dir_arrow(np.array([1.85, -1.15, 0.0]), DOWN, CO2_COLOR, "down")
        self.add(w.base_group(), meta_lbl, calc, clk, arr_u, arr_d)

        self.play(FadeOut(clk, run_time=0.4), FadeOut(arr_u, run_time=0.4), FadeOut(arr_d, run_time=0.4), FadeOut(meta_lbl, run_time=0.4))

        self.at("settles at")
        self.play(w.pco2_t.animate.set_value(27.0), run_time=1.8)

        self.at("that leaves")
        flash_highlight(self, w.dco2_num, color=CO2_COLOR, run_time=1.4)

        self.at("12")
        flash_highlight(self, w.fraction_bar, color=GAUGE_COLOR, run_time=1.6)

        e1 = M("6.1 +", 22, GAUGE_COLOR)
        e2 = M("1.17", 22, GAUGE_COLOR)
        e3 = M("= 7.27", 22, GAUGE_COLOR)
        VGroup(e1, e2, e3).arrange(RIGHT, buff=0.14).move_to([GAUGE_X + 0.15, -2.82, 0.0])

        self.at("its log")
        self.play(FadeIn(e1), run_time=0.45)

        self.at("is 1", lead=-0.15)
        self.play(FadeIn(e2), run_time=0.5)

        self.at("pH is", lead=-0.45)
        y27 = ph_to_y(ph_of(12.0, 27.0))
        lbl27 = M("7.27", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X - 0.22, y27, 0.0], aligned_edge=RIGHT)
        self.play(FadeIn(e3), FadeIn(lbl27), run_time=0.55)
        self.finish()


def build_predict_world(q_mark_alpha=None):
    w = AcidBaseWorld(
        hco3=12.0, pco2=27.0, breath_amp=0.132, breath_speed=3.2, bubble_rate=1.0,
        ratio_mode="full_12", show_patient_tag=True, ghost_710=True, dashed_740=True,
        show_740_lbl=False, tremble=True,
    )
    calc = make_calc_line(w.pco2_t)
    y27 = ph_to_y(ph_of(12.0, 27.0))
    lbl27 = M("7.27", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X - 0.22, y27, 0.0], aligned_edge=RIGHT)
    y74 = ph_to_y(7.40)
    full_lbl = T("full repair", 22, GAUGE_COLOR).move_to([GAUGE_X + 0.16, y74 + 0.28, 0.0], aligned_edge=LEFT)
    target_ratio = M("20 : 1", 24, GAUGE_COLOR).move_to([2.18, 0.0, 0.0], aligned_edge=LEFT)
    q_mark = M("?", 28, GOLD, weight=BOLD).next_to(w.pco2_readout, RIGHT, buff=0.08)
    if q_mark_alpha is not None:
        q_mark.add_updater(lambda m, dt: m.set_opacity(0.35 + 0.65 * abs(np.sin(2.4 * w.tremble_t.get_value()))))
    return w, Group(w.base_group(), calc, lbl27, full_lbl, target_ratio, q_mark), full_lbl, target_ratio, q_mark, lbl27


class S06Predict(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=12.0, pco2=27.0, breath_amp=0.132, breath_speed=3.2, bubble_rate=1.1,
            ratio_mode="full_12", show_patient_tag=True, ghost_710=True,
        )
        calc = make_calc_line(w.pco2_t)
        y27 = ph_to_y(ph_of(12.0, 27.0))
        lbl27 = M("7.27", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X - 0.22, y27, 0.0], aligned_edge=RIGHT)
        eq_under = M("6.1 + 1.17 = 7.27", 22, GAUGE_COLOR).move_to([GAUGE_X + 0.15, -2.82, 0.0])
        self.add(w.base_group(), calc, lbl27, eq_under)

        self.at("full repair")
        y74 = ph_to_y(7.40)
        d74 = DashedLine([GAUGE_X - 0.30, y74, 0], [GAUGE_X + 0.54, y74, 0], color=GAUGE_COLOR, stroke_width=3.2, dash_length=0.10)
        full_lbl = T("full repair", 22, GAUGE_COLOR).move_to([GAUGE_X + 0.16, y74 + 0.28, 0.0], aligned_edge=LEFT)
        target_ratio = M("20 : 1", 24, GAUGE_COLOR).move_to([2.18, 0.0, 0.0], aligned_edge=LEFT)
        self.play(FadeOut(w.lbl74, run_time=0.25), FadeOut(eq_under, run_time=0.35), Create(d74), FadeIn(full_lbl), FadeIn(target_ratio), run_time=1.0)

        self.at("bicarbonate at")
        flash_highlight(self, w.hco3_num, color=BICARB_COLOR, run_time=1.0)

        self.at("how low would")
        t_blink = ValueTracker(0.0)
        t_blink.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t_blink)
        q_mark = M("?", 28, GOLD, weight=BOLD).next_to(w.pco2_readout, RIGHT, buff=0.08)
        q_mark.add_updater(lambda m, dt: m.set_opacity(0.35 + 0.65 * abs(np.sin(2.4 * t_blink.get_value()))))
        q_card = question_card("For 20 : 1, pCO2 = ?", y=3.30, color=GAUGE_COLOR, size=34)
        self.play(FadeIn(q_mark), FadeIn(q_card), run_time=0.9)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "For 20 : 1, pCO2 = ?"
    CARD = {"y": 3.30, "color": GAUGE_COLOR, "size": 34}
    RING_AT = (5.75, 3.30, 0.0)
    SECONDS = 4.5

    def backdrop(self):
        _, grp, _, _, _, _ = build_predict_world(q_mark_alpha=True)
        return grp


def make_s08_working():
    w1a = M("12", 22, GAUGE_COLOR)
    w1b = M("÷ 20", 22, GAUGE_COLOR)
    w1c = M("= 0.6", 22, GAUGE_COLOR)
    line1 = VGroup(w1a, w1b, w1c).arrange(RIGHT, buff=0.14).move_to([1.02, -0.60, 0.0], aligned_edge=LEFT)
    w2a = M("0.6 ÷", 22, GAUGE_COLOR)
    w2b = M("0.03", 22, GAUGE_COLOR)
    w2c = M("= 20 mmHg", 22, GAUGE_COLOR)
    row2a = VGroup(w2a, w2b).arrange(RIGHT, buff=0.14).move_to([1.02, -0.98, 0.0], aligned_edge=LEFT)
    w2c.move_to([1.02, -1.30, 0.0], aligned_edge=LEFT)
    line2 = VGroup(row2a, w2c)
    return line1, line2, (w1a, w1b, w1c, w2a, w2b, w2c)


class S08Answer(SpokenScene):
    def construct(self):
        w, grp, full_lbl, target_ratio, q_mark, lbl27 = build_predict_world(q_mark_alpha=None)
        q_card = question_card("For 20 : 1, pCO2 = ?", y=3.30, color=GAUGE_COLOR, size=34)
        self.add(grp, q_card)

        self.play(FadeOut(q_card, run_time=0.30), FadeOut(q_mark, run_time=0.30))

        self.at("to 20", lead=-0.2)
        y_ghost = LOWER_BOT + 0.03 + 0.60 * H_SCALE
        ghost_line = DashedLine(
            [TANK_X - TANK_W / 2.0 + 0.08, y_ghost, 0],
            [TANK_X + TANK_W / 2.0 - 0.08, y_ghost, 0],
            color=CO2_COLOR,
            stroke_width=3.0,
            dash_length=0.10,
        )
        ghost_ptr = Line([TANK_X + 0.28, y_ghost, 0], [TANK_X + 0.28, -1.62, 0], color=CO2_COLOR, stroke_width=2.0)
        ghost_lbl = T("needs\n20 mmHg", 22, CO2_COLOR, weight=BOLD, line_spacing=0.85).move_to([TANK_X + 0.28, -1.22, 0.0])
        real_lbl = T("27", 24, CO2_COLOR, weight=BOLD).move_to([TANK_X + TANK_W / 2.0 + 0.22, LOWER_BOT + 0.72, 0.0], aligned_edge=LEFT)
        self.play(Create(ghost_line), Create(ghost_ptr), FadeIn(ghost_lbl), FadeIn(real_lbl), run_time=1.3)

        _, _, (w1a, w1b, w1c, w2a, w2b, w2c) = make_s08_working()

        self.at("20 to 1")
        self.play(FadeIn(w1b), run_time=0.4)

        self.at("12 on top")
        self.play(FadeIn(w1a), run_time=0.4)

        self.at("needs", lead=-0.10)
        self.play(FadeIn(w1c), run_time=0.5)

        self.at("Divide by")
        self.play(FadeIn(w2a), run_time=0.35)
        self.play(FadeIn(w2b), run_time=0.45)

        self.at("20", nth=2, lead=0.05)
        self.play(FadeIn(w2c), run_time=0.5)

        self.at("stopped at")
        flash_highlight(self, w.pco2_readout, color=CO2_COLOR, run_time=1.2)

        self.at("bought back")
        y71 = ph_to_y(7.10)
        y27 = ph_to_y(ph_of(12.0, 27.0))
        y74 = ph_to_y(7.40)
        br_x = GAUGE_X + 0.45
        br1 = VGroup(
            Line([br_x - 0.08, y71, 0], [br_x, y71, 0], color=GAUGE_COLOR, stroke_width=2.5),
            Line([br_x, y71, 0], [br_x, y27, 0], color=GAUGE_COLOR, stroke_width=2.5),
            Line([br_x - 0.08, y27, 0], [br_x, y27, 0], color=GAUGE_COLOR, stroke_width=2.5),
        )
        br1_lbl = T("0.17\nbought back", 22, GAUGE_COLOR, line_spacing=0.85).move_to([br_x + 0.14, (y71 + y27) / 2.0 - 0.12, 0.0], aligned_edge=LEFT)
        self.play(Create(br1), FadeIn(br1_lbl), run_time=1.4)

        self.at("not all of it")
        br2 = DashedLine([br_x, y27 + 0.04, 0], [br_x, y74 - 0.04, 0], color=GAUGE_COLOR, stroke_width=2.5, dash_length=0.07)
        br2_lbl = T("not all", 22, GAUGE_COLOR).move_to([br_x + 0.14, (y27 + y74) / 2.0, 0.0], aligned_edge=LEFT)
        self.play(Create(br2), FadeIn(br2_lbl), run_time=0.8)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=12.0, pco2=27.0, breath_amp=0.132, breath_speed=3.2, bubble_rate=1.1,
            ratio_mode="full_12", show_patient_tag=True, ghost_710=True, dashed_740=True, show_740_lbl=False,
        )
        calc = make_calc_line(w.pco2_t)
        y71 = ph_to_y(7.10)
        y27 = ph_to_y(ph_of(12.0, 27.0))
        y74 = ph_to_y(7.40)
        lbl27 = M("7.27", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X - 0.22, y27, 0.0], aligned_edge=RIGHT)
        full_lbl = T("full repair", 22, GAUGE_COLOR).move_to([GAUGE_X + 0.16, y74 + 0.28, 0.0], aligned_edge=LEFT)
        target_ratio = M("20 : 1", 24, GAUGE_COLOR).move_to([2.18, 0.0, 0.0], aligned_edge=LEFT)

        y_ghost = LOWER_BOT + 0.03 + 0.60 * H_SCALE
        ghost_line = DashedLine([TANK_X - TANK_W / 2.0 + 0.08, y_ghost, 0], [TANK_X + TANK_W / 2.0 - 0.08, y_ghost, 0], color=CO2_COLOR, stroke_width=3.0, dash_length=0.10)
        ghost_ptr = Line([TANK_X + 0.28, y_ghost, 0], [TANK_X + 0.28, -1.62, 0], color=CO2_COLOR, stroke_width=2.0)
        ghost_lbl = T("needs\n20 mmHg", 22, CO2_COLOR, weight=BOLD, line_spacing=0.85).move_to([TANK_X + 0.28, -1.22, 0.0])
        real_lbl = T("27", 24, CO2_COLOR, weight=BOLD).move_to([TANK_X + TANK_W / 2.0 + 0.22, LOWER_BOT + 0.72, 0.0], aligned_edge=LEFT)
        line1, line2, _ = make_s08_working()

        br_x = GAUGE_X + 0.45
        br1 = VGroup(
            Line([br_x - 0.08, y71, 0], [br_x, y71, 0], color=GAUGE_COLOR, stroke_width=2.5),
            Line([br_x, y71, 0], [br_x, y27, 0], color=GAUGE_COLOR, stroke_width=2.5),
            Line([br_x - 0.08, y27, 0], [br_x, y27, 0], color=GAUGE_COLOR, stroke_width=2.5),
        )
        br1_lbl = T("0.17\nbought back", 22, GAUGE_COLOR, line_spacing=0.85).move_to([br_x + 0.14, (y71 + y27) / 2.0 - 0.12, 0.0], aligned_edge=LEFT)
        br2 = DashedLine([br_x, y27 + 0.04, 0], [br_x, y74 - 0.04, 0], color=GAUGE_COLOR, stroke_width=2.5, dash_length=0.07)
        br2_lbl = T("not all", 22, GAUGE_COLOR).move_to([br_x + 0.14, (y27 + y74) / 2.0, 0.0], aligned_edge=LEFT)

        self.add(w.base_group(), calc, lbl27, full_lbl, target_ratio, ghost_line, ghost_ptr, ghost_lbl, real_lbl, line1, line2, br1, br1_lbl, br2, br2_lbl)

        self.play(
            FadeOut(ghost_line), FadeOut(ghost_ptr), FadeOut(ghost_lbl), FadeOut(real_lbl),
            FadeOut(line1), FadeOut(line2),
            FadeOut(br1), FadeOut(br1_lbl), FadeOut(br2), FadeOut(br2_lbl), FadeOut(target_ratio),
            run_time=1.2,
        )
        flash_highlight(self, w.fraction_bar, color=GAUGE_COLOR, run_time=2.4)

        self.at("same direction")
        arr_u = make_dir_arrow(np.array([1.74, 1.15, 0.0]), DOWN, BICARB_COLOR)
        arr_d = make_dir_arrow(np.array([1.74, -1.15, 0.0]), DOWN, CO2_COLOR)
        same_lbl = T("same way", 24, GAUGE_COLOR, weight=BOLD).move_to([2.08, 0.0, 0.0], aligned_edge=LEFT)
        self.play(FadeIn(arr_u), FadeIn(arr_d), FadeIn(same_lbl), run_time=1.4)
        self.play(
            Indicate(arr_u, color=BICARB_COLOR),
            Indicate(arr_d, color=CO2_COLOR),
            Indicate(w.upper_outline, color=BICARB_COLOR, scale_factor=1.04),
            Indicate(w.lower_outline, color=CO2_COLOR, scale_factor=1.04),
            run_time=2.6,
        )

        self.at("usually part way")
        glow = Circle(radius=0.16, color=GOLD, stroke_width=3.5).move_to([GAUGE_X + 0.18, y27, 0.0])
        self.play(FadeIn(glow, run_time=0.5), Indicate(lbl27, color=GOLD, scale_factor=1.08, run_time=1.8))
        self.play(FadeOut(glow, run_time=0.6))

        self.at("chronic respiratory disorders")
        ghost_y_t = ValueTracker(y27)
        ghost_needle = always_redraw(lambda: Polygon(
            [GAUGE_X + 0.06, ghost_y_t.get_value(), 0],
            [GAUGE_X + 0.30, ghost_y_t.get_value() + 0.11, 0],
            [GAUGE_X + 0.30, ghost_y_t.get_value() - 0.11, 0],
            color=GAUGE_COLOR, fill_color=GAUGE_COLOR, fill_opacity=0.45, stroke_width=1.5,
        ))
        chronic_tag = T("some chronic\ncases", 22, GAUGE_COLOR, line_spacing=0.85).move_to([GAUGE_X + 0.44, y74 - 0.34, 0.0], aligned_edge=LEFT)
        self.add(ghost_needle)
        self.play(ghost_y_t.animate.set_value(ph_to_y(7.37)), FadeIn(chronic_tag), run_time=2.6)
        self.wait(0.8)
        self.play(FadeOut(ghost_needle), FadeOut(chronic_tag), run_time=0.6)

        self.at("never carries")
        wall = Line([GAUGE_X - 0.30, y74, 0], [GAUGE_X + 0.56, y74, 0], color=GAUGE_COLOR, stroke_width=6.0)
        wall_lbl = T("never past 7.40", 22, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X + 0.30, y74 + 0.28, 0.0], aligned_edge=LEFT)
        self.play(FadeOut(w.dashed_740_line, run_time=0.35), FadeOut(full_lbl, run_time=0.35))
        self.play(Create(wall), FadeIn(wall_lbl), run_time=1.8)
        self.finish()


class S10Winter(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=12.0, pco2=27.0, breath_amp=0.132, breath_speed=3.2, bubble_rate=1.1,
            ratio_mode="full_12", show_patient_tag=True, ghost_710=True, wall_740=True,
        )
        calc = make_calc_line(w.pco2_t)
        y27 = ph_to_y(ph_of(12.0, 27.0))
        lbl27 = M("7.27", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X - 0.22, y27, 0.0], aligned_edge=RIGHT)
        arr_u = make_dir_arrow(np.array([1.74, 1.15, 0.0]), DOWN, BICARB_COLOR)
        arr_d = make_dir_arrow(np.array([1.74, -1.15, 0.0]), DOWN, CO2_COLOR)
        same_lbl = T("same way", 24, GAUGE_COLOR, weight=BOLD).move_to([2.08, 0.0, 0.0], aligned_edge=LEFT)
        self.add(w.base_group(), calc, lbl27, arr_u, arr_d, same_lbl)

        self.play(FadeOut(arr_u), FadeOut(arr_d), FadeOut(same_lbl), FadeOut(calc), run_time=0.45)

        spine, ticks, band, band_lbl, py = make_winter_scale(x_pos=-3.45, y_bot=-2.45, y_top=-1.25)
        scale_hdr = M("pCO2", 22, TEXT).move_to([-2.85, -1.06, 0.0])
        self.play(FadeIn(spine, shift=RIGHT * 0.2), FadeIn(ticks), FadeIn(scale_hdr), run_time=1.0)

        g1 = M("1.5", 22, GAUGE_COLOR)
        g2 = M("× HCO3-", 22, GAUGE_COLOR)
        g3 = M("+ 8", 22, GAUGE_COLOR)
        g4 = M("± 2", 22, GAUGE_COLOR)
        gen_r1 = VGroup(g1, g2).arrange(RIGHT, buff=0.13)
        gen_r2 = VGroup(g3, g4).arrange(RIGHT, buff=0.13)
        gen_grp = VGroup(gen_r1, gen_r2).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([-2.95, 0.96, 0.0])

        self.at("expects one")
        self.play(FadeIn(g1), run_time=0.4)
        self.at("times bicarbonate")
        self.play(FadeIn(g2), run_time=0.5)
        self.at("plus 8")
        self.play(FadeIn(g3), run_time=0.45)
        self.at("give or take")
        self.play(FadeIn(g4), run_time=0.5)

        f1 = M("1.5", 22, GAUGE_COLOR, weight=BOLD)
        f2 = M("× 12", 22, GAUGE_COLOR, weight=BOLD)
        f3 = M("+ 8", 22, GAUGE_COLOR, weight=BOLD)
        f4 = M("= 26", 22, GAUGE_COLOR, weight=BOLD)
        f_top = VGroup(f1, f2, f3).arrange(RIGHT, buff=0.13)
        VGroup(f_top, f4).arrange(DOWN, buff=0.07).move_to([-2.95, 0.98, 0.0])
        band_26_2 = M("26 ± 2", 22, GAUGE_COLOR, weight=BOLD).move_to([-2.95, 0.56, 0.0])

        self.at("one and a half", nth=1)
        self.play(FadeOut(gen_grp, run_time=0.25), FadeIn(f1, run_time=0.35))
        self.at("times 12", lead=-0.1)
        self.play(FadeIn(f2), run_time=0.4)
        self.at("plus 8", nth=1)
        self.play(FadeIn(f3), run_time=0.4)
        self.at("is 26", lead=-0.1)
        self.play(FadeIn(f4), FadeIn(band_26_2), run_time=0.55)

        self.at("24 to 28")
        self.play(FadeIn(band), FadeIn(band_lbl), run_time=1.4)

        self.at("27 fits")
        marker27 = Dot(point=[-3.45 + 0.23, py(27), 0.0], radius=0.075, color=CO2_COLOR, stroke_color=GAUGE_COLOR, stroke_width=2.0)
        tick27 = M("27 ✓", 22, CO2_COLOR, weight=BOLD).move_to([-2.78, -1.52, 0.0], aligned_edge=LEFT)
        ptr27 = Line([-2.84, -1.58, 0.0], [-3.14, py(27) + 0.04, 0.0], color=CO2_COLOR, stroke_width=2.0)
        mark20 = Dot(point=[-3.45 + 0.23, py(20), 0.0], radius=0.06, color=GAUGE_COLOR)
        self.play(FadeIn(marker27, shift=DOWN * 0.2), FadeIn(tick27), Create(ptr27), FadeIn(mark20), run_time=1.4)

        self.at("fitted to people")
        rng = np.random.default_rng(7)
        dots = VGroup()
        for _ in range(20):
            dx = rng.uniform(0.05, 0.41)
            pv = np.clip(rng.normal(26.0, 2.2), 20.8, 37.5)
            dots.add(Dot(point=[-3.45 + dx, py(pv), 0.0], radius=0.032, color=GAUGE_COLOR, fill_opacity=0.75))
        scat_lbl = T("a fit, not a law", 22, GAUGE_COLOR, weight=BOLD).move_to([-3.40, 0.24, 0.0])
        scat_tag = T("schematic scatter", 22, TEXT).move_to([-3.00, -2.76, 0.0])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.06, run_time=1.8), FadeIn(scat_lbl), FadeIn(scat_tag))
        self.finish()


class S11Respiratory(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=12.0, pco2=27.0, breath_amp=0.132, breath_speed=3.2, bubble_rate=1.1,
            ratio_mode="full_12", show_patient_tag=True, ghost_710=True, wall_740=True,
        )
        lbl27 = M("7.27", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X - 0.22, ph_to_y(ph_of(12.0, 27.0)), 0.0], aligned_edge=RIGHT)
        spine, ticks, band, band_lbl, py = make_winter_scale()
        scale_hdr = M("pCO2", 22, TEXT).move_to([-2.85, -1.06, 0.0])
        formula = M("1.5 × 12 + 8\n= 26", 22, GAUGE_COLOR, weight=BOLD, line_spacing=0.85).move_to([-2.95, 0.98, 0.0])
        band_26_2 = M("26 ± 2", 22, GAUGE_COLOR, weight=BOLD).move_to([-2.95, 0.56, 0.0])
        marker27 = Dot(point=[-3.45 + 0.23, py(27), 0.0], radius=0.075, color=CO2_COLOR, stroke_color=GAUGE_COLOR, stroke_width=2.0)
        tick27 = M("27 ✓", 22, CO2_COLOR, weight=BOLD).move_to([-2.78, -1.52, 0.0], aligned_edge=LEFT)
        ptr27 = Line([-2.84, -1.58, 0.0], [-3.14, py(27) + 0.04, 0.0], color=CO2_COLOR, stroke_width=2.0)
        scat_lbl = T("a fit, not a law", 22, GAUGE_COLOR, weight=BOLD).move_to([-3.40, 0.24, 0.0])
        scat_tag = T("schematic scatter", 22, TEXT).move_to([-3.00, -2.76, 0.0])
        winter_grp = Group(spine, ticks, band, band_lbl, scale_hdr, formula, band_26_2, marker27, tick27, ptr27, scat_lbl, scat_tag)
        self.add(w.base_group(), lbl27, winter_grp)

        new_tag = T("illustrative: pCO2 40 to 50", 24, TEXT).move_to([-6.20, -3.26, 0.0], aligned_edge=LEFT)
        w.ratio_mode = "simple"
        self.play(
            FadeOut(winter_grp, run_time=0.45),
            FadeOut(lbl27, run_time=0.45),
            swap(w.patient_tag, new_tag, run_time=0.6),
            w.hco3_t.animate.set_value(24.0),
            w.pco2_t.animate.set_value(40.0),
            w.breath_amp_t.animate.set_value(0.082),
            w.breath_speed_t.animate.set_value(2.1),
            w.bubble_rate_t.animate.set_value(0.0),
            run_time=1.0,
        )
        w.patient_tag = new_tag

        self.at("rises first")
        arr_co2 = make_dir_arrow(np.array([1.80, -1.15, 0.0]), UP, CO2_COLOR)
        self.play(
            w.breath_amp_t.animate.set_value(0.035),
            w.breath_speed_t.animate.set_value(1.0),
            FadeIn(arr_co2),
            run_time=1.2,
        )

        self.at("the kidney")
        self.play(Indicate(w.kidney, color=KIDNEY_COLOR, scale_factor=1.10), run_time=1.6)

        self.at("Take a rise")
        self.play(w.pco2_t.animate.set_value(50.0), run_time=1.6)

        plus1_top = T("+1 at once:", 24, BICARB_COLOR, weight=BOLD)
        plus1_sub = T("other blood buffers", 22, BICARB_COLOR)
        buff_lbl = VGroup(plus1_top, plus1_sub).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([1.02, 1.92, 0.0], aligned_edge=LEFT)

        self.at("at once the blood's other buffers")
        self.play(FadeIn(plus1_sub), run_time=0.6)

        self.at("add about", lead=-0.2)
        self.play(w.hco3_t.animate.set_value(25.0), FadeIn(plus1_top), run_time=2.0)

        self.at("over days as the kidney")
        cal = make_calendar(np.array([-2.85, 0.68, 0.0]), "days")
        self.play(FadeIn(cal), run_time=0.5)

        flow_dots = VGroup(*[Dot(radius=0.06, color=BICARB_COLOR).move_to(KIDNEY_POS + RIGHT * 0.4) for _ in range(4)])
        self.add(flow_dots)
        self.play(
            w.kidney.animate.set_fill(opacity=0.68),
            LaggedStart(*[d.animate.move_to([TANK_X, UPPER_BOT + 0.85, 0.0]) for d in flow_dots[:2]], lag_ratio=0.3, run_time=1.1),
        )
        self.play(
            LaggedStart(*[d.animate.move_to([TANK_X, UPPER_BOT + 0.85, 0.0]) for d in flow_dots[2:]], lag_ratio=0.3, run_time=1.35),
            w.hco3_t.animate.set_value(27.0),
            run_time=1.35,
            rate_func=linear,
        )
        self.remove(flow_dots)

        days_lbl = T("+5 over days", 26, BICARB_COLOR, weight=BOLD).move_to([1.02, 1.85, 0.0], aligned_edge=LEFT)
        arr_hco3 = make_dir_arrow(np.array([1.70, 1.15, 0.0]), UP, BICARB_COLOR)
        same_lbl = T("same way", 24, GAUGE_COLOR, weight=BOLD).move_to([1.95, 0.0, 0.0], aligned_edge=LEFT)
        self.at("the rise")
        self.play(
            w.hco3_t.animate.set_value(28.1),
            FadeIn(arr_hco3),
            FadeIn(same_lbl),
            run_time=0.9,
            rate_func=linear,
        )
        self.play(FadeOut(buff_lbl), w.hco3_t.animate.set_value(28.4), run_time=0.20, rate_func=linear)
        self.play(FadeIn(days_lbl), w.hco3_t.animate.set_value(29.0), run_time=0.30, rate_func=linear)

        self.at("Full repair needs")
        calc_50 = make_calc_line(w.pco2_t)
        self.play(FadeIn(calc_50), run_time=0.5)

        u1 = M("20", 22, GAUGE_COLOR, weight=BOLD)
        u2 = M("×", 22, GAUGE_COLOR, weight=BOLD)
        u3 = M("1.5", 22, GAUGE_COLOR, weight=BOLD)
        u4 = M("= 30", 22, GAUGE_COLOR, weight=BOLD)
        VGroup(u1, u2, u3, u4).arrange(RIGHT, buff=0.13).move_to([-1.66, 1.95, 0.0], aligned_edge=RIGHT)

        self.at("20 times")
        self.play(FadeIn(u1), FadeIn(u2), run_time=0.35)

        self.at("times 1", lead=-0.1)
        self.play(FadeIn(u3), run_time=0.4)

        self.at("30")
        y30 = UPPER_BOT + 0.03 + 30.0 * H_SCALE
        ghost30 = DashedLine([TANK_X - TANK_W / 2.0 + 0.08, y30, 0], [TANK_X + TANK_W / 2.0 - 0.08, y30, 0], color=BICARB_COLOR, stroke_width=2.8, dash_length=0.10)
        self.play(FadeIn(u4), Create(ghost30), run_time=0.45)

        self.at("six more")
        full6 = T("+6 for full", 24, BICARB_COLOR, weight=BOLD).move_to([1.02, 2.38, 0.0], aligned_edge=LEFT)
        self.play(FadeIn(full6), run_time=0.5)
        self.finish()


class S12TwoThings(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=29.0, pco2=50.0, breath_amp=0.035, breath_speed=1.0, bubble_rate=0.0,
            ratio_mode="none", patient_tag="illustrative: pCO2 40 to 50", show_patient_tag=True,
            ghost_710=True, wall_740=True, show_numbers=False,
        )
        arr_u = make_dir_arrow(np.array([1.80, 1.15, 0.0]), UP, BICARB_COLOR)
        arr_d = make_dir_arrow(np.array([1.80, -1.15, 0.0]), UP, CO2_COLOR)
        self.add(w.base_group(), arr_u, arr_d)

        self.at("opposite directions")
        two_proc = T("two\nprocesses", 24, GAUGE_COLOR, weight=BOLD, line_spacing=0.85).move_to([1.95, 0.0, 0.0], aligned_edge=LEFT)
        self.play(Rotate(arr_d, PI), FadeIn(two_proc), run_time=0.7)
        self.play(Indicate(arr_u, color=RED), Indicate(arr_d, color=RED), run_time=0.8)

        self.at("far off the fit")
        spine, _, band, _, py = make_winter_scale(x_pos=-3.45, y_bot=-2.45, y_top=-1.25)
        band.set_opacity(0.45)
        ghost_winter = VGroup(spine, band).set_opacity(0.6)
        off_dot = Dot(point=[-3.45 + 0.23, py(26), 0.0], radius=0.08, color=RED)
        off_lbl = T("off the fit", 22, RED, weight=BOLD).move_to([-3.08, py(37), 0.0], aligned_edge=LEFT)
        self.play(FadeIn(ghost_winter), FadeIn(off_dot), run_time=0.45)
        self.play(off_dot.animate.move_to([-3.45 + 0.23, py(37), 0.0]), FadeIn(off_lbl), run_time=0.85)

        self.at("two things")
        self.play(Indicate(two_proc, color=GOLD), Indicate(off_lbl, color=GOLD), run_time=0.8)
        self.play(FadeOut(two_proc), FadeOut(off_lbl), FadeOut(ghost_winter), FadeOut(off_dot), Rotate(arr_d, PI), run_time=0.6)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        w = AcidBaseWorld(
            hco3=12.0, pco2=27.0, breath_amp=0.132, breath_speed=3.2, bubble_rate=1.1,
            ratio_mode="full_12", patient_tag="made-up patient", show_patient_tag=True,
            ghost_710=True, wall_740=True,
        )
        arr_u = make_dir_arrow(np.array([1.80, 1.15, 0.0]), DOWN, BICARB_COLOR)
        arr_d = make_dir_arrow(np.array([1.80, -1.15, 0.0]), DOWN, CO2_COLOR)
        y27 = ph_to_y(ph_of(12.0, 27.0))
        lbl27 = M("7.27", 24, GAUGE_COLOR, weight=BOLD).move_to([GAUGE_X - 0.22, y27, 0.0], aligned_edge=RIGHT)
        self.add(w.base_group(), arr_u, arr_d, lbl27)

        self.at("the lungs answer")
        self.play(Indicate(w.lungs, color=LUNG_COLOR, scale_factor=1.06), run_time=1.2)

        self.at("the kidney answers")
        w.ratio_mode = "simple"
        self.play(FadeOut(lbl27, run_time=0.35))
        new_tag = T("illustrative: pCO2 40 to 50", 24, TEXT).move_to([-6.20, -3.26, 0.0], aligned_edge=LEFT)
        self.play(
            w.hco3_t.animate.set_value(29.0),
            w.pco2_t.animate.set_value(50.0),
            w.breath_amp_t.animate.set_value(0.035),
            w.breath_speed_t.animate.set_value(1.0),
            w.bubble_rate_t.animate.set_value(0.0),
            Rotate(arr_u, PI),
            Rotate(arr_d, PI),
            w.kidney.animate.set_fill(opacity=0.68),
            run_time=2.4,
        )
        self.play(swap(w.patient_tag, new_tag, run_time=0.45))

        self.at("neither overshoots")
        dot_meta = Dot(point=[GAUGE_X + 0.16, y27, 0.0], radius=0.065, color=BICARB_COLOR).set_opacity(0.85)
        self.play(FadeIn(dot_meta), Indicate(w.wall_740_line, color=GOLD, scale_factor=1.06), Indicate(w.wall_740_lbl, color=GOLD), run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "Compensation moves the other term the same way, never past 7.40."
