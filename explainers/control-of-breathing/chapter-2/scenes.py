"""Thin Air, Same Lever — Control of Breathing, Chapter 2.

COLOUR MAP (one colour per concept, kept for the whole film):
    TEAL   (#3FB8C0) : carbon dioxide (CO2 block, washed-out CO2 dots)
    ORANGE (#FF8C2E) : oxygen (inspired O2, alveolar PO2 remainder, O2 dots, O2 curve)
    PURPLE (#C07BFF) : hydrogen ions / alkalosis (H+ blood band, inhibition bars)
    BLUE   (#58C4DD) : brainstem controller (medulla chip)
    GREEN  (#83C167) : ventilation, the lever (bellows, ventilation axis)
    YELLOW (#F5D547) : what to look at (operating-point dots, ticks, rings, gain bracket)
    RED    (#FC6255) : removed or stopped (cross on unchanged pie / arterial tag)
    GREY   (#8B93A1) : structure and hedges (mountain, dial, ruler, carotid sensor, kidney, model values)

THE WORLD (carried across all scenes):
    Left 35%: GREY mountain slope with small GREY climber + GREY barometric dial below (760 -> 500 mmHg).
    Top-left (when active): O2 response curve inset above the mountain.
    Right 65%: GREY ruler (0 to 150 mmHg) beside one tall gas column (ORANGE inspired O2 bar minus TEAL
    CO2/0.80 block leaving ORANGE alveolar PO2 remainder) with GREEN bellows at its base; BLUE controller
    chip and GREY carotid sensor at far right when referenced; bottom-right 'model values' scope tag.

WHAT CHANGES IN EACH SPOKEN SCENE (and what computes it):
    s00_link_and_question : Bellows pumps harder -> PaCO2 swings down (40->24->40), alveolar PO2 grows
                            (99.7->119.7->99.7) while Hill-computed O2 saturation pip barely moves
                            (97.4%->98.4%); then climber walks up slope, dial winds 760->500, inspired O2
                            shortens from 0.21*(PB-47) while TEAL block stays at 50.0.
    s02_what_changed      : 21% ORANGE/GREY pie holds fixed as dial finishes winding to 500 and RED cross
                            marks no change; inspired O2 bar & counter drop from 149.7 to 95.1; bellows
                            and controller pulse unchanged.
    s03_model_values      : Three arithmetic steps (500-47=453, 0.21*453, =95.1 mmHg) build in order and
                            settle the inspired O2 bar at 95.1 with a YELLOW tick.
    s04_predict           : Sea-level ghost column (99.7) builds beside the 95.1 bar; CO2=40 chip settles
                            above the bar; question & YELLOW '?' pose the prediction.
    s06_answer            : CO2 chip grows downward into a 50.0 TEAL block (40/0.80=50), leaving 45.1 ORANGE
                            remainder marked by YELLOW ring; GREY 'half' bracket spans 45.1 to 99.7.
    s07_hyperventilation  : Bellows speeds up, climber chest rises, TEAL dots stream out as PaCO2 tracker
                            drops 40->30; TEAL block shrinks 50.0->37.5 and alveolar PO2 climbs 45.1->57.6.
    s08_gain_hedge        : YELLOW bracket spans 45.1->57.6 (+12.5 mmHg) with check (40-30)/0.80; empty
                            vessel + crossed-out arterial tag contrast alveolar vs arterial.
    s09_oxygen_arm        : Computed Weil hyperbola V_E = 3.35 + 180/(PO2-32) traces live at top left;
                            YELLOW dot slides 100->45.1 into 50-60 band, second dot marks 57.6, joined to ruler.
    s10_idea              : Controller, carotid sensor and bellows pulse unchanged ('same loop'); dot slides
                            100->45.1; bellows pumps and PaCO2 oscillates 40<->30 moving PO2 45.1<->57.6.
    s11_brake             : Inset fades; TEAL dots exit and PURPLE H+ dots in blood band thin out ('pH up');
                            two PURPLE inhibition bars reach controller & carotid sensor, slowing bellows.
    s12_days              : Time strip marker advances seconds->days; GREY kidney sends arrow restoring
                            PURPLE H+ dots partway; sensors brighten, inhibition thins, bellows climbs.
    s13_close             : Extra overlays fade to the 6 core pieces; controller & sensor pulse unchanged;
                            bellows pumps swinging alveolar PO2 between 45.1 and 57.6.
"""
from bp_parts import *

# ------------------------------------------------------------------ concept palette
CO2_COL = TEAL
O2_COL = "#FF8C2E"
H_COL = "#C07BFF"
CTRL_COL = BLUE
VENT_COL = GREEN
FOCUS_COL = YELLOW
STOP_COL = RED
STRUCT_COL = GREY

# ------------------------------------------------------------------ physiological math
R_EXCHANGE = 0.80
FIO2 = 0.21
PH2O = 47.0


def inspired_po2(pb):
    return FIO2 * (pb - PH2O)


def co2_term(paco2):
    return paco2 / R_EXCHANGE


def alveolar_po2(pb, paco2):
    return inspired_po2(pb) - co2_term(paco2)


def hill_sat(po2, p50=26.0, n=2.7):
    p = max(float(po2), 0.1) ** n
    return p / (p + p50 ** n)


def weil_vent(po2):
    """Human isocapnic hypoxic response hyperbola from lesson_for_context.mdx (A=180, asymptote=32)."""
    return 3.35 + 180.0 / max(float(po2) - 32.0, 2.0)


# ------------------------------------------------------------------ shared world coordinates
RULER_X = 1.15
COL_X = 2.25
COL_W = 1.76
Y_ZERO = -1.70
Y_MAX = 2.58
MMHG_SCALE = (Y_MAX - Y_ZERO) / 150.0   # 0.02853 scene units per mmHg


def y_mmhg(val):
    return Y_ZERO + float(val) * MMHG_SCALE


# Mountain profile points (x in [-6.05, -1.85], y in [-1.00, -0.24])
SLOPE_PTS = [
    np.array([-6.05, -1.00, 0.0]),
    np.array([-5.20, -0.96, 0.0]),
    np.array([-4.10, -0.70, 0.0]),
    np.array([-3.05, -0.40, 0.0]),
    np.array([-2.25, -0.24, 0.0]),
    np.array([-1.85, -0.24, 0.0]),
]


def slope_point(t):
    """Interpolate (x, y) along the walkable mountain slope for t in [0, 1]."""
    t = float(np.clip(t, 0.0, 1.0))
    pts = SLOPE_PTS[:5]
    u = t * (len(pts) - 1)
    i = min(int(u), len(pts) - 2)
    f = u - i
    return pts[i] * (1 - f) + pts[i + 1] * f


def make_mountain():
    fill_pts = SLOPE_PTS + [np.array([-1.85, -1.10, 0.0]), np.array([-6.05, -1.10, 0.0])]
    body = Polygon(*fill_pts, stroke_width=0, fill_color=STRUCT_COL, fill_opacity=0.14)
    ridge = VMobject(stroke_color=STRUCT_COL, stroke_width=3.5).set_points_as_corners(SLOPE_PTS)
    return VGroup(body, ridge)


def make_climber(climb_tracker, breath_amp=None, breath_phase=None):
    """Small GREY climber standing on the slope at climb_tracker in [0, 1]."""
    def mk():
        base = slope_point(climb_tracker.get_value())
        chest_r = 0.0
        if breath_amp is not None and breath_phase is not None:
            chest_r = 0.045 * breath_amp.get_value() * max(0.0, np.sin(breath_phase.get_value()))
        feet = base + UP * 0.02
        hip = feet + UP * 0.19
        shoulder = hip + UP * 0.21
        head_c = shoulder + UP * 0.11
        leg_l = Line(hip, feet + LEFT * 0.07, color=TEXT, stroke_width=3)
        leg_r = Line(hip, feet + RIGHT * 0.07, color=TEXT, stroke_width=3)
        torso = Line(hip, shoulder, color=TEXT, stroke_width=4)
        chest = Ellipse(
            width=0.13 + chest_r * 2.4,
            height=0.16 + chest_r * 1.1,
            color=STRUCT_COL,
            stroke_width=2.5,
            fill_color=STRUCT_COL,
            fill_opacity=0.38,
        ).move_to((hip + shoulder) / 2 + RIGHT * chest_r * 0.4)
        arm_f = Line(shoulder + DOWN * 0.04, shoulder + DOWN * 0.06 + RIGHT * 0.14, color=TEXT, stroke_width=2.8)
        arm_b = Line(shoulder + DOWN * 0.04, shoulder + DOWN * 0.15 + LEFT * 0.09, color=TEXT, stroke_width=2.8)
        head = Circle(radius=0.075, color=TEXT, stroke_width=2.8, fill_color=STRUCT_COL, fill_opacity=0.45).move_to(head_c)
        return VGroup(leg_l, leg_r, torso, chest, arm_b, arm_f, head)
    return always_redraw(mk)


def make_baro_dial(pb_tracker, center=(-4.0, -1.85, 0.0), radius=0.70):
    """GREY barometric pressure dial reading pb_tracker in mmHg (400..800 range)."""
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=STRUCT_COL, stroke_width=8)

    def frac():
        return float(np.clip((pb_tracker.get_value() - 400.0) / 400.0, 0.02, 0.98))

    val_arc = always_redraw(
        lambda: Arc(radius=radius, start_angle=PI, angle=-PI * frac(), arc_center=c, stroke_color=TEXT, stroke_width=5)
    )
    needle = always_redraw(
        lambda: Line(
            c,
            c + 0.78 * radius * np.array([np.cos(PI - PI * frac()), np.sin(PI - PI * frac()), 0.0]),
            color=FOCUS_COL,
            stroke_width=4,
        )
    )
    pivot = Dot(c, radius=0.045, color=TEXT)
    readout = always_redraw(
        lambda: M(f"{pb_tracker.get_value():.0f} mmHg", 25, TEXT).move_to(c + DOWN * 0.31)
    )
    lab = T("barometric", 24, STRUCT_COL).move_to(c + DOWN * 0.65)
    return VGroup(track, val_arc, needle, pivot, readout, lab)


def make_ruler():
    """GREY vertical ruler 0..150 mmHg at RULER_X."""
    axis = Line([RULER_X, y_mmhg(0), 0], [RULER_X, y_mmhg(150), 0], color=STRUCT_COL, stroke_width=3)
    ticks, labels = VGroup(), VGroup()
    for v in (0, 30, 60, 90, 120, 150):
        y = y_mmhg(v)
        ticks.add(Line([RULER_X, y, 0], [RULER_X - 0.12, y, 0], color=STRUCT_COL, stroke_width=2.5))
        t = M(str(v), 24, STRUCT_COL).next_to([RULER_X - 0.14, y, 0], LEFT, buff=0.08)
        labels.add(t)
    unit = T("mmHg", 24, STRUCT_COL).move_to([RULER_X - 0.50, y_mmhg(150) + 0.35, 0])
    return VGroup(axis, ticks, labels, unit)


def make_gas_column(pb_tracker, paco2_tracker, show_co2=True):
    """Live gas column built from the simplified alveolar gas equation."""
    def mk_rem():
        pb = pb_tracker.get_value()
        if show_co2:
            po2 = max(0.5, alveolar_po2(pb, paco2_tracker.get_value()))
        else:
            po2 = max(0.5, inspired_po2(pb))
        h = po2 * MMHG_SCALE
        return Rectangle(
            width=COL_W,
            height=h,
            stroke_color=O2_COL,
            stroke_width=3,
            fill_color=O2_COL,
            fill_opacity=0.22,
        ).move_to([COL_X, Y_ZERO + h / 2, 0])

    rem_box = always_redraw(mk_rem)
    g = VGroup(rem_box)
    if show_co2:
        def mk_co2():
            pb = pb_tracker.get_value()
            paco2 = paco2_tracker.get_value()
            top = y_mmhg(inspired_po2(pb))
            bot = y_mmhg(max(0.5, alveolar_po2(pb, paco2)))
            h = max(0.05, top - bot)
            return Rectangle(
                width=COL_W,
                height=h,
                stroke_color=CO2_COL,
                stroke_width=3,
                fill_color=CO2_COL,
                fill_opacity=0.24,
            ).move_to([COL_X, (top + bot) / 2, 0])
        g.add(always_redraw(mk_co2))
    return g


def make_o2_dots(pb_tracker, paco2_tracker=None, n=18, seed=7):
    """Drifting ORANGE O2 dots strictly inside the ORANGE portion of the gas column."""
    rng = np.random.default_rng(seed)
    fx = rng.uniform(0.10, 0.90, size=n)
    fy = rng.uniform(0.06, 0.94, size=n)
    vx = rng.uniform(-0.22, 0.22, size=n)
    vy = rng.uniform(0.18, 0.36, size=n)
    dots = VGroup()
    for i in range(n):
        d = Dot(radius=0.05, color=O2_COL).set_opacity(0.88)
        d._fx, d._fy, d._vx, d._vy = float(fx[i]), float(fy[i]), float(vx[i]), float(vy[i])

        def upd(mob, dt, pb_t=pb_tracker, co2_t=paco2_tracker):
            mob._fx += mob._vx * dt
            mob._fy += mob._vy * dt
            if mob._fx < 0.08 or mob._fx > 0.92:
                mob._vx *= -1
                mob._fx = float(np.clip(mob._fx, 0.08, 0.92))
            if mob._fy > 0.94:
                mob._fy = 0.06
            pb = pb_t.get_value()
            top_val = alveolar_po2(pb, co2_t.get_value()) if co2_t is not None else inspired_po2(pb)
            h = max(0.25, top_val * MMHG_SCALE)
            x = (COL_X - COL_W / 2) + mob._fx * COL_W
            y = Y_ZERO + mob._fy * h
            mob.move_to([x, y, 0])

        d.add_updater(upd)
        upd(d, 0.0)
        dots.add(d)
    dots.layout_ok = True   # O2 gas dots inside column may pass behind internal column label
    return dots


def make_bellows(phase_tracker, amp_tracker, center=(COL_X, -2.26, 0.0)):
    """GREEN ventilation bellows at the base of the gas column."""
    c = np.array(center, dtype=float)
    neck = Line([COL_X, Y_ZERO, 0], [COL_X, c[1] + 0.34, 0], color=VENT_COL, stroke_width=5)

    def mk_body():
        s = 0.5 + 0.5 * np.sin(phase_tracker.get_value())   # 0..1
        amp = amp_tracker.get_value()
        w = 1.38 + 0.34 * amp * s
        h = 0.46 + 0.22 * amp * s
        top_y = c[1] + h / 2
        bot_y = c[1] - h / 2
        left_pts = [
            [c[0] - w / 2, top_y, 0],
            [c[0] - w * 0.36, top_y - h * 0.25, 0],
            [c[0] - w / 2, c[1], 0],
            [c[0] - w * 0.36, bot_y + h * 0.25, 0],
            [c[0] - w / 2, bot_y, 0],
        ]
        right_pts = [
            [c[0] + w / 2, bot_y, 0],
            [c[0] + w * 0.36, bot_y + h * 0.25, 0],
            [c[0] + w / 2, c[1], 0],
            [c[0] + w * 0.36, top_y - h * 0.25, 0],
            [c[0] + w / 2, top_y, 0],
        ]
        poly = Polygon(
            *(left_pts + right_pts),
            stroke_color=VENT_COL,
            stroke_width=3.5 + 1.0 * s,
            fill_color=VENT_COL,
            fill_opacity=0.22 + 0.16 * s,
        )
        rib = Line([c[0] - w * 0.34, c[1], 0], [c[0] + w * 0.34, c[1], 0], color=VENT_COL, stroke_width=2.5)
        return VGroup(poly, rib)

    body = always_redraw(mk_body)
    return VGroup(neck, body)


def make_controller_chip(pos=(5.30, 2.20, 0)):
    c = boxed_label("controller", CTRL_COL, size=26, pad=0.18)
    c.move_to(pos)
    return c


def make_carotid_sensor(pos=(5.30, 1.02, 0)):
    """GREY carotid fork + small chemoreceptor body at the bifurcation."""
    p = np.array(pos, dtype=float)
    stem = Line(p + DOWN * 0.38, p, color=STRUCT_COL, stroke_width=6)
    br_l = Line(p, p + UL * 0.34 + UP * 0.10, color=STRUCT_COL, stroke_width=5)
    br_r = Line(p, p + UR * 0.34 + UP * 0.10, color=STRUCT_COL, stroke_width=5)
    body = Circle(radius=0.105, color=TEXT, stroke_width=2.5, fill_color=STRUCT_COL, fill_opacity=0.75).move_to(p + UP * 0.05)
    lab = T("carotid sensor", 24, STRUCT_COL).next_to(stem, DOWN, buff=0.18)
    return VGroup(stem, br_l, br_r, body, lab)


def make_ghost_sea_level(x=5.05):
    """Faint GREY sea-level reference column (149.7 total, 50.0 CO2, 99.7 PO2)."""
    w = 1.04
    h_rem = 99.7 * MMHG_SCALE
    h_co2 = 50.0 * MMHG_SCALE
    rem = Rectangle(width=w, height=h_rem, stroke_color=STRUCT_COL, stroke_width=2, fill_color=STRUCT_COL, fill_opacity=0.12)
    rem.move_to([x, Y_ZERO + h_rem / 2, 0])
    co2 = Rectangle(width=w, height=h_co2, stroke_color=STRUCT_COL, stroke_width=2, fill_color=STRUCT_COL, fill_opacity=0.06)
    co2.move_to([x, Y_ZERO + h_rem + h_co2 / 2, 0])
    num = M("99.7", 26, STRUCT_COL).move_to(rem.get_center())
    tag = T("sea level", 26, STRUCT_COL).next_to(co2, UP, buff=0.16)
    return VGroup(rem, co2, num, tag)


def make_o2_curve_inset():
    """Top-left Weil hyperbola inset, computed from V_E = 3.35 + 180 / (PO2 - 32)."""
    P = Plot(
        box=(-5.55, -2.10, 1.15, 2.55),
        xr=(40, 105),
        yr=(0, 24),
        xticks=[40, 50, 60, 100],
        yticks=(),
        xlabel="alveolar PO2",
        ylabel="ventilation",
        color=STRUCT_COL,
        size=22,
        label_size=24,
    )
    P.ylabel.set_color(VENT_COL)
    bl = P.pt(50, 0)
    tr = P.pt(60, 24)
    band = Rectangle(
        width=tr[0] - bl[0],
        height=tr[1] - bl[1],
        stroke_width=0,
        fill_color=O2_COL,
        fill_opacity=0.20,
    ).move_to((bl + tr) / 2)
    band_lab = M("50–60", 22, O2_COL).move_to(P.pt(55, 21.8))
    curve = P.curve(weil_vent, x0=42.0, x1=105.0, color=O2_COL, width=5)
    sketch = T("in this sketch", 22, STRUCT_COL).move_to([-2.70, 2.82, 0])
    return P, band, band_lab, curve, sketch


def make_col_po2_label(po2_fn, y_fn=None):
    """Compact 2-line PO2 label centered inside the ORANGE remainder box."""
    def mk():
        val = po2_fn()
        y = y_fn() if y_fn is not None else y_mmhg(val * 0.5)
        return M(f"PO2\n{val:.1f}", 24, TEXT, line_spacing=0.82).move_to([COL_X, y, 0])
    return always_redraw(mk)


def make_col_co2_label(paco2_fn, pb=500.0):
    """Compact 2-line CO2/0.80 label centered inside the TEAL block."""
    def mk():
        c = paco2_fn()
        term = co2_term(c)
        y = y_mmhg(inspired_po2(pb) - term * 0.5)
        return M(f"{c:.0f} ÷ 0.80\n= {term:.1f}", 22, TEXT, line_spacing=0.82).move_to([COL_X, y, 0])
    return always_redraw(mk)


# ================================================================== SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        pb = ValueTracker(760.0)
        paco2 = ValueTracker(40.0)
        climb = ValueTracker(0.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.65)
        b_speed = ValueTracker(3.2)

        def step_breath(m, dt):
            b_phase.increment_value(b_speed.get_value() * dt)

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(step_breath)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)

        # Left-aligned segment labels strictly right of column (x >= 3.28)
        lx = COL_X + COL_W / 2 + 0.16
        insp_lab = always_redraw(
            lambda: M(f"inspired O2 {inspired_po2(pb.get_value()):.1f}", 22, O2_COL)
            .move_to([lx, y_mmhg(inspired_po2(pb.get_value())) + 0.14, 0], aligned_edge=LEFT)
        )
        co2_lab = always_redraw(
            lambda: M(f"CO2/0.80 {co2_term(paco2.get_value()):.1f}", 22, CO2_COL)
            .move_to([lx, y_mmhg(inspired_po2(pb.get_value()) - co2_term(paco2.get_value()) * 0.5), 0], aligned_edge=LEFT)
        )
        alv_lab = always_redraw(
            lambda: M(f"alveolar PO2\n{alveolar_po2(pb.get_value(), paco2.get_value()):.1f}", 22, O2_COL, line_spacing=0.82)
            .move_to([lx, y_mmhg(alveolar_po2(pb.get_value(), paco2.get_value()) * 0.5), 0], aligned_edge=LEFT)
        )

        # Small ORANGE O2 saturation pip far right (x = 5.90, clear of labels)
        sat_x = 5.95
        sat_bot, sat_top = -1.55, 0.35
        sat_track = Line([sat_x, sat_bot, 0], [sat_x, sat_top, 0], color=STRUCT_COL, stroke_width=6)
        sat_pip = always_redraw(
            lambda: Dot(
                [sat_x, sat_bot + hill_sat(alveolar_po2(pb.get_value(), paco2.get_value())) * (sat_top - sat_bot), 0],
                radius=0.10,
                color=O2_COL,
                stroke_color=TEXT,
                stroke_width=2,
            )
        )
        sat_title = T("O2 sat", 22, O2_COL).move_to([sat_x - 0.08, sat_top + 0.24, 0])
        sat_num = always_redraw(
            lambda: M(f"{100 * hill_sat(alveolar_po2(pb.get_value(), paco2.get_value())):.1f}%", 22, O2_COL)
            .move_to([sat_x - 0.10, sat_bot - 0.26, 0])
        )

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag)
        self.add(sat_track, sat_pip, sat_title, sat_num)
        self.add(insp_lab, co2_lab, alv_lab)

        self.at("breathing harder")
        self.play(
            b_amp.animate.set_value(1.35),
            b_speed.animate.set_value(6.0),
            paco2.animate.set_value(24.0),
            run_time=3.2,
        )

        self.at("barely moved oxygen")
        self.play(
            b_amp.animate.set_value(0.65),
            b_speed.animate.set_value(3.2),
            paco2.animate.set_value(40.0),
            run_time=2.8,
        )

        self.at("up a mountain")
        self.play(
            FadeOut(sat_track), FadeOut(sat_pip), FadeOut(sat_title), FadeOut(sat_num),
            climb.animate.set_value(0.75),
            pb.animate.set_value(560.0),
            run_time=2.8,
            rate_func=linear,
        )

        self.at("still about 21")
        q = T("Still 21 percent. Why gasp?", 36, TEXT).move_to([0.0, 3.30, 0])
        self.play(FadeIn(q, shift=DOWN * 0.08), run_time=0.9)

        self.at("why is the climber")
        self.play(
            climb.animate.set_value(0.92),
            pb.animate.set_value(525.0),
            run_time=1.8,
            rate_func=linear,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        pb = ValueTracker(525.0)
        paco2 = ValueTracker(40.0)
        climb = ValueTracker(0.92)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.65)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(3.2 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        lx = COL_X + COL_W / 2 + 0.18
        insp_lab = always_redraw(
            lambda: M(f"inspired O2 {inspired_po2(pb.get_value()):.1f}", 22, O2_COL)
            .move_to([lx, y_mmhg(inspired_po2(pb.get_value())) + 0.14, 0], aligned_edge=LEFT)
        )
        co2_lab = always_redraw(
            lambda: M(f"CO2/0.80 {co2_term(paco2.get_value()):.1f}", 22, CO2_COL)
            .move_to([lx, y_mmhg(inspired_po2(pb.get_value()) - 25.0), 0], aligned_edge=LEFT)
        )
        alv_lab = always_redraw(
            lambda: M(f"alveolar PO2 {alveolar_po2(pb.get_value(), paco2.get_value()):.1f}", 22, O2_COL)
            .move_to([lx, y_mmhg(alveolar_po2(pb.get_value(), paco2.get_value()) * 0.5), 0], aligned_edge=LEFT)
        )

        q = T("Still 21 percent. Why gasp?", 36, TEXT).move_to([0.0, 3.30, 0])
        title = T("Thin Air, Same Lever", 42, TEXT, font=TITLE_FONT).move_to([0.0, 3.45, 0])

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, insp_lab, co2_lab, alv_lab, q)
        self.play(
            swap(q, title, run_time=0.7),
            climb.animate.set_value(1.0),
            pb.animate.set_value(505.0),
            run_time=1.8,
            rate_func=linear,
        )
        self.finish()


class S02WhatChanged(SpokenScene):
    def construct(self):
        pb = ValueTracker(760.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.65)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(3.2 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, None, show_co2=False)
        dots = make_o2_dots(pb, None, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        ctrl = boxed_label("controller", CTRL_COL, size=22, pad=0.14).move_to([5.58, 2.25, 0])
        insp_num = always_redraw(
            lambda: M(f"inspired O2\n{inspired_po2(pb.get_value()):.1f}", 22, O2_COL, line_spacing=0.82)
            .move_to([COL_X, y_mmhg(inspired_po2(pb.get_value())) + 0.44, 0])
        )

        # 21% O2 pie at top-left above mountain
        pie_c = np.array([-4.05, 1.50, 0.0])
        r_pie = 0.68
        grey_sector = Sector(
            radius=r_pie,
            angle=TAU * 0.79,
            start_angle=TAU * 0.21,
            color=STRUCT_COL,
            fill_opacity=0.45,
            stroke_color=STRUCT_COL,
            stroke_width=2,
        ).move_arc_center_to(pie_c)
        o2_sector = Sector(
            radius=r_pie,
            angle=TAU * 0.21,
            start_angle=0.0,
            color=O2_COL,
            fill_opacity=0.85,
            stroke_color=O2_COL,
            stroke_width=2,
        ).move_arc_center_to(pie_c)
        pie_lab = T("21% O2", 26, O2_COL).move_to(pie_c + UP * (r_pie + 0.28))
        pie_group = VGroup(grey_sector, o2_sector, pie_lab)
        cross = VGroup(
            Line(pie_c + UL * 0.52, pie_c + DR * 0.52, color=STOP_COL, stroke_width=6),
            Line(pie_c + UR * 0.52, pie_c + DL * 0.52, color=STOP_COL, stroke_width=6),
        )

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, ctrl, insp_num)

        self.at("not the fraction")
        self.play(FadeIn(pie_group), run_time=0.8)
        self.play(Create(cross), run_time=0.6)

        self.at("Barometric pressure falls")
        self.play(pb.animate.set_value(500.0), run_time=4.8, rate_func=linear)
        self.play(FadeOut(pie_group), FadeOut(cross), run_time=0.6)

        self.at("loop is untouched")
        self.play(
            Indicate(bellows, color=VENT_COL, scale_factor=1.08),
            Indicate(ctrl[0], color=FOCUS_COL, scale_factor=1.08),
            run_time=1.4,
        )

        self.at("input is dropped")
        arr = Arrow(
            [4.60, y_mmhg(95.1) - 0.65, 0],
            [COL_X + COL_W / 2 + 0.10, y_mmhg(95.1) - 0.65, 0],
            color=FOCUS_COL,
            stroke_width=4,
            buff=0.0,
        )
        low_lab = T("lower input", 26, FOCUS_COL).next_to(arr, RIGHT, buff=0.14)
        self.play(GrowArrow(arr), FadeIn(low_lab), run_time=1.0)
        self.finish()


class S03ModelValues(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.95)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(4.5 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        bar_val = ValueTracker(149.7)

        def mk_bar():
            v = max(1.0, bar_val.get_value())
            h = v * MMHG_SCALE
            return Rectangle(
                width=COL_W,
                height=h,
                stroke_color=O2_COL,
                stroke_width=3,
                fill_color=O2_COL,
                fill_opacity=0.22,
            ).move_to([COL_X, Y_ZERO + h / 2, 0])

        col = always_redraw(mk_bar)
        dots = make_o2_dots(pb, None, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        insp_lab = always_redraw(
            lambda: T("inspired O2", 24, O2_COL).move_to([COL_X, y_mmhg(bar_val.get_value()) + 0.26, 0])
        )

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, insp_lab)

        self.at("model values")
        self.play(Transform(tag, scope_tag("model values", size=24, color=FOCUS_COL)), run_time=1.8)
        self.play(Transform(tag, scope_tag("model values", size=24, color=STRUCT_COL)), run_time=1.6)

        step1 = M("500 - 47 = 453", 26, TEXT).move_to([3.55, 2.05, 0], aligned_edge=LEFT)
        step2 = M("0.21 × 453", 26, TEXT).next_to(step1, DOWN, buff=0.35, aligned_edge=LEFT)
        step3 = M("= 95.1 mmHg", 26, O2_COL).next_to(step2, DOWN, buff=0.35, aligned_edge=LEFT)

        self.at("Barometric pressure")
        self.play(
            Indicate(dial_g[4], color=FOCUS_COL, scale_factor=1.10),
            bar_val.animate.set_value(120.0),
            run_time=3.5,
            rate_func=linear,
        )

        self.at("Subtract water vapor")
        self.play(
            FadeIn(step1, shift=RIGHT * 0.1),
            bar_val.animate.set_value(108.0),
            run_time=2.8,
            rate_func=linear,
        )

        self.at("of the rest")
        self.play(FadeIn(step2, shift=RIGHT * 0.1), bar_val.animate.set_value(95.1), run_time=1.6)
        tick = Line([RULER_X - 0.16, y_mmhg(95.1), 0], [RULER_X + 0.18, y_mmhg(95.1), 0], color=FOCUS_COL, stroke_width=5)
        self.play(FadeIn(step3, shift=RIGHT * 0.1), Create(tick), run_time=1.2)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.95)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(4.5 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, None, show_co2=False)
        dots = make_o2_dots(pb, None, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        tick = Line([RULER_X - 0.16, y_mmhg(95.1), 0], [RULER_X + 0.18, y_mmhg(95.1), 0], color=FOCUS_COL, stroke_width=5)
        insp_num = M("95.1", 26, O2_COL).next_to(tick, LEFT, buff=0.14).shift(UP * 0.18)

        ghost = make_ghost_sea_level(x=5.05)
        co2_chip = boxed_label("CO2 40", CO2_COL, size=26, pad=0.16).move_to([COL_X, y_mmhg(95.1) + 0.46, 0])
        q = T("Alveolar oxygen here?", 36, TEXT).move_to([0.0, 3.45, 0])
        qmark = M("?", 40, FOCUS_COL).move_to([RULER_X - 0.58, y_mmhg(45.0), 0])

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, tick, insp_num)

        self.at("At sea level")
        self.play(GrowFromEdge(ghost[0], DOWN), run_time=2.8)
        self.play(GrowFromEdge(ghost[1], DOWN), FadeIn(ghost[2]), FadeIn(ghost[3]), run_time=2.6)

        self.at("down to 95")
        sweep = DashedLine([4.25, y_mmhg(99.7), 0], [RULER_X + 0.18, y_mmhg(95.1), 0], color=FOCUS_COL, stroke_width=3)
        self.play(Create(sweep), Indicate(tick, color=FOCUS_COL, scale_factor=1.35), run_time=1.8)
        self.play(FadeOut(sweep), run_time=0.6)

        self.at("Carbon dioxide is still")
        self.play(FadeIn(co2_chip, shift=DOWN * 0.35), run_time=2.2)

        self.at("where does the alveolus")
        self.play(FadeIn(q), FadeIn(qmark), run_time=1.4)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Alveolar oxygen here?"
    CARD = {"y": 3.45, "color": TEXT, "size": 36}
    RING_AT = (6.05, -2.35, 0)
    SECONDS = 4.5

    def backdrop(self):
        pb = ValueTracker(500.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.95)

        dial_g = make_baro_dial(pb)
        dial_g._trem_t = 0.0

        def trem_upd(m, dt):
            m._trem_t += dt
            pb.set_value(500.0 + 1.8 * np.sin(9.0 * m._trem_t))

        dial_g.add_updater(trem_upd)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(4.5 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        ruler = make_ruler()
        col = make_gas_column(pb, None, show_co2=False)
        dots = make_o2_dots(pb, None, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        tick = Line([RULER_X - 0.16, y_mmhg(95.1), 0], [RULER_X + 0.18, y_mmhg(95.1), 0], color=FOCUS_COL, stroke_width=5)
        insp_num = M("95.1", 26, O2_COL).next_to(tick, LEFT, buff=0.14).shift(UP * 0.18)
        ghost = make_ghost_sea_level(x=5.05)
        co2_chip = boxed_label("CO2 40", CO2_COL, size=26, pad=0.16).move_to([COL_X, y_mmhg(95.1) + 0.46, 0])
        qmark = M("?", 40, FOCUS_COL).move_to([RULER_X - 0.58, y_mmhg(45.0), 0])

        return VGroup(
            mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag,
            tick, insp_num, ghost, co2_chip, qmark
        )


class S06Answer(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(0.5)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.95)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(4.5 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        tick = Line([RULER_X - 0.16, y_mmhg(95.1), 0], [RULER_X + 0.18, y_mmhg(95.1), 0], color=FOCUS_COL, stroke_width=5)
        insp_num = M("95.1", 26, O2_COL).next_to(tick, LEFT, buff=0.14).shift(UP * 0.18)
        ghost = make_ghost_sea_level(x=5.05)
        co2_chip = boxed_label("CO2 40", CO2_COL, size=26, pad=0.16).move_to([COL_X, y_mmhg(95.1) + 0.46, 0])
        q = T("Alveolar oxygen here?", 36, TEXT).move_to([0.0, 3.45, 0])
        qmark = M("?", 40, FOCUS_COL).move_to([RULER_X - 0.58, y_mmhg(45.0), 0])

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, tick, insp_num, ghost, co2_chip, q, qmark)

        self.at("Carbon dioxide")
        self.play(FadeOut(q), FadeOut(qmark), FadeOut(co2_chip), run_time=0.8)
        self.play(paco2.animate.set_value(40.0), run_time=4.6, rate_func=linear)

        self.at("takes 50 away")
        co2_eq = M("40 ÷ 0.80\n= 50", 22, TEXT, line_spacing=0.82).move_to([COL_X, y_mmhg(70.1), 0])
        self.play(FadeIn(co2_eq), run_time=1.4)

        self.at("leaves about 45")
        ring = Circle(radius=0.11, color=FOCUS_COL, stroke_width=4).move_to([RULER_X, y_mmhg(45.1), 0])
        rem_lab = M("PO2\n45.1", 24, TEXT, line_spacing=0.82).move_to([COL_X, y_mmhg(22.5), 0])
        self.play(Create(ring), FadeIn(rem_lab), run_time=1.4)

        self.at("less than half")
        br = BraceBetweenPoints([3.30, y_mmhg(45.1), 0], [3.30, y_mmhg(99.7), 0], direction=RIGHT, color=STRUCT_COL)
        half_lab = T("half", 24, STRUCT_COL).next_to(br, RIGHT, buff=0.10)
        self.play(GrowFromCenter(br), FadeIn(half_lab), run_time=1.4)
        self.finish()


class S07Hyperventilation(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(40.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.80)
        b_speed = ValueTracker(3.8)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(b_speed.get_value() * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        tick = Line([RULER_X - 0.16, y_mmhg(95.1), 0], [RULER_X + 0.18, y_mmhg(95.1), 0], color=FOCUS_COL, stroke_width=5)
        same_air = T("same air  95.1", 24, STRUCT_COL).move_to([3.45, y_mmhg(95.1), 0], aligned_edge=LEFT)

        ring = always_redraw(
            lambda: Circle(radius=0.11, color=FOCUS_COL, stroke_width=4)
            .move_to([RULER_X, y_mmhg(alveolar_po2(500.0, paco2.get_value())), 0])
        )
        co2_eq = make_col_co2_label(lambda: paco2.get_value(), pb=500.0)
        rem_lab = make_col_po2_label(lambda: alveolar_po2(500.0, paco2.get_value()))

        co2_stream = VGroup()
        rng = np.random.default_rng(19)
        for i in range(10):
            d = Dot(radius=0.05, color=CO2_COL).set_opacity(0.0)
            d._x0 = float(COL_X + rng.uniform(-0.55, 0.55))
            d._t = float(i * 0.25)
            co2_stream.add(d)
        co2_stream.layout_ok = True

        stream_on = ValueTracker(0.0)

        def upd_stream(mob, dt):
            on = stream_on.get_value()
            for d in mob:
                d._t = (d._t + dt * 0.9) % 2.0
                if on < 0.5:
                    d.set_opacity(0.0)
                else:
                    y = y_mmhg(95.1) + 0.1 + d._t * 0.9
                    d.move_to([d._x0, y, 0])
                    d.set_opacity(max(0.0, 0.85 * (1.0 - d._t / 2.0)))

        co2_stream.add_updater(upd_stream)

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, tick, same_air, ring, co2_eq, rem_lab, co2_stream)

        self.at("drives harder breathing")
        self.play(b_amp.animate.set_value(1.50), b_speed.animate.set_value(6.5), run_time=2.2)

        self.at("washes out")
        stream_on.set_value(1.0)
        self.play(paco2.animate.set_value(30.0), run_time=5.4, rate_func=linear)

        self.at("takes only")
        self.play(Indicate(co2_eq, color=CO2_COL, scale_factor=1.08), run_time=2.2)

        self.at("alveolus rises")
        stream_on.set_value(0.0)
        self.play(Indicate(ring, color=FOCUS_COL, scale_factor=1.3), Indicate(rem_lab, color=FOCUS_COL, scale_factor=1.08), run_time=2.0)
        self.finish()


class S08GainHedge(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(30.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(1.50)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(6.5 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        tick = Line([RULER_X - 0.16, y_mmhg(95.1), 0], [RULER_X + 0.18, y_mmhg(95.1), 0], color=FOCUS_COL, stroke_width=5)
        ring = Circle(radius=0.11, color=FOCUS_COL, stroke_width=4).move_to([RULER_X, y_mmhg(57.6), 0])
        co2_eq = M("30 ÷ 0.80\n= 37.5", 22, TEXT, line_spacing=0.82).move_to([COL_X, y_mmhg(76.35), 0])
        rem_lab = M("PO2\n57.6", 24, TEXT, line_spacing=0.82).move_to([COL_X, y_mmhg(36.0), 0])

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, tick, ring, co2_eq, rem_lab)

        self.at("The gain is")
        br = BraceBetweenPoints([3.32, y_mmhg(45.1), 0], [3.32, y_mmhg(57.6), 0], direction=RIGHT, color=FOCUS_COL)
        gain_lab = M("+12.5 mmHg", 24, FOCUS_COL).next_to(br, RIGHT, buff=0.14)
        self.play(GrowFromCenter(br), FadeIn(gain_lab), run_time=2.2)

        self.at("ten divided by")
        chk = M("(40 - 30) ÷ 0.80", 24, TEXT).move_to([3.65, y_mmhg(76.35), 0], aligned_edge=LEFT)
        self.play(FadeIn(chk), run_time=2.2)

        self.at("alveolar not arterial")
        alv_pin = T("alveolar", 24, TEXT).move_to([0.05, y_mmhg(15.0), 0])
        alv_line = Line(alv_pin.get_right() + RIGHT * 0.08, [COL_X - COL_W / 2 - 0.02, y_mmhg(15.0), 0], color=STRUCT_COL, stroke_width=3)
        v_top = Line([4.0, -1.20, 0], [5.7, -1.20, 0], color=STRUCT_COL, stroke_width=3)
        v_bot = Line([4.0, -1.60, 0], [5.7, -1.60, 0], color=STRUCT_COL, stroke_width=3)
        art_tag = T("arterial", 24, STRUCT_COL).move_to([4.85, -2.02, 0])
        art_cross = VGroup(
            Line(art_tag.get_corner(DL) + LEFT * 0.08, art_tag.get_corner(UR) + RIGHT * 0.08, color=STOP_COL, stroke_width=4),
            Line(art_tag.get_corner(UL) + LEFT * 0.08, art_tag.get_corner(DR) + RIGHT * 0.08, color=STOP_COL, stroke_width=4),
        )
        art_cross.layout_ok = True   # deliberate strike-through on 'arterial'
        self.play(FadeIn(alv_pin), Create(alv_line), Create(v_top), Create(v_bot), FadeIn(art_tag), Create(art_cross), run_time=2.0)

        self.at("model output")
        self.play(Transform(tag, scope_tag("model values", size=24, color=FOCUS_COL)), run_time=1.0)
        self.play(Transform(tag, scope_tag("model values", size=24, color=STRUCT_COL)), run_time=1.0)
        self.finish()


class S09OxygenArm(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(30.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        po2_dot_t = ValueTracker(100.0)
        b_amp = ValueTracker(0.75)

        def step_breath(m, dt):
            # Tie ventilation bellows speed & amplitude to the curve dot's ventilation readout
            v = weil_vent(po2_dot_t.get_value()) / 6.0
            b_amp.set_value(float(np.clip(0.65 * v, 0.70, 1.85)))
            b_phase.increment_value(float(np.clip(3.2 * v, 3.4, 8.2)) * dt)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(step_breath)

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        rem_lab = M("PO2\n57.6", 24, TEXT, line_spacing=0.82).move_to([COL_X, y_mmhg(28.8), 0])

        P, band, band_lab, curve, sketch = make_o2_curve_inset()
        curve_t = ValueTracker(42.0)
        live_c = P.live_curve(weil_vent, curve_t, x0=42.0, color=O2_COL, width=5)
        dot1 = P.dot(lambda: po2_dot_t.get_value(), lambda: weil_vent(po2_dot_t.get_value()), color=FOCUS_COL, ring=TEXT, radius=0.09)
        drop_line = always_redraw(
            lambda: DashedLine(
                P.pt(po2_dot_t.get_value(), 0),
                P.pt(po2_dot_t.get_value(), weil_vent(po2_dot_t.get_value())),
                color=FOCUS_COL,
                stroke_width=2.5,
            )
        )
        vent_bar = always_redraw(
            lambda: Line(
                P.pt(40, 0),
                P.pt(40, weil_vent(po2_dot_t.get_value())),
                color=VENT_COL,
                stroke_width=8,
            )
        )

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, rem_lab)

        self.at("sensor has leverage")
        self.play(FadeIn(P), FadeIn(sketch), run_time=0.8)
        self.add(live_c)
        self.play(curve_t.animate.set_value(105.0), run_time=3.2, rate_func=linear)
        self.remove(live_c)
        self.add(curve)

        self.at("shallow above")
        self.play(FadeIn(dot1), FadeIn(drop_line), FadeIn(vent_bar), run_time=0.6)
        self.play(po2_dot_t.animate.set_value(62.0), run_time=3.2, rate_func=linear)

        self.at("and steepens")
        self.play(FadeIn(band), FadeIn(band_lab), po2_dot_t.animate.set_value(45.1), run_time=3.6, rate_func=linear)

        self.at("45 and 58")
        dot2 = Dot(P.pt(57.6, weil_vent(57.6)), radius=0.09, color=FOCUS_COL, stroke_color=TEXT, stroke_width=2.5)
        p45 = P.pt(45.1, weil_vent(45.1))
        p58 = P.pt(57.6, weil_vent(57.6))
        l45 = VMobject(color=STRUCT_COL, stroke_width=2.5, stroke_opacity=0.8).set_points_as_corners([
            p45,
            np.array([-1.18, p45[1], 0.0]),
            np.array([-1.18, y_mmhg(45.1), 0.0]),
            np.array([RULER_X, y_mmhg(45.1), 0.0]),
        ])
        l58 = VMobject(color=STRUCT_COL, stroke_width=2.5, stroke_opacity=0.8).set_points_as_corners([
            p58,
            np.array([-1.32, p58[1], 0.0]),
            np.array([-1.32, -0.22, 0.0]),
            np.array([1.03, -0.22, 0.0]),
            np.array([RULER_X, y_mmhg(57.6), 0.0]),
        ])
        m45 = Circle(radius=0.08, color=FOCUS_COL, stroke_width=3).move_to([RULER_X, y_mmhg(45.1), 0])
        m58 = Circle(radius=0.08, color=FOCUS_COL, stroke_width=3).move_to([RULER_X, y_mmhg(57.6), 0])
        self.play(FadeIn(dot2), Create(l45), Create(l58), Create(m45), Create(m58), run_time=2.2)
        self.finish()


class S10Idea(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(35.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(1.15)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(4.8 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        ctrl = make_controller_chip(pos=(5.25, 2.15, 0))
        carotid = make_carotid_sensor(pos=(5.25, 0.95, 0))

        P, band, band_lab, curve, sketch = make_o2_curve_inset()
        po2_dot_t = ValueTracker(100.0)
        dot1 = P.dot(lambda: po2_dot_t.get_value(), lambda: weil_vent(po2_dot_t.get_value()), color=FOCUS_COL, ring=TEXT, radius=0.09)
        rem_lab = make_col_po2_label(lambda: alveolar_po2(500.0, paco2.get_value()))

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, ctrl, carotid, P, band, band_lab, curve, sketch, dot1, rem_lab)

        self.at("does not rebuild")
        same_lab = T("same loop", 26, TEXT).next_to(ctrl, UP, buff=0.20)
        self.play(
            FadeIn(same_lab),
            Indicate(bellows, color=VENT_COL, scale_factor=1.08),
            Indicate(ctrl[0], color=CTRL_COL, scale_factor=1.08),
            Indicate(carotid[:4], color=TEXT, scale_factor=1.08),
            run_time=2.2,
        )

        self.at("moves the operating point")
        self.play(po2_dot_t.animate.set_value(45.1), run_time=2.0, rate_func=linear)

        self.at("lever finally buys")
        self.play(paco2.animate.set_value(40.0), run_time=1.8)
        self.play(paco2.animate.set_value(30.0), run_time=2.0)
        self.play(paco2.animate.set_value(38.0), run_time=1.6)

        self.at("asked below")
        hb_tag = T("oxygen carried:\nasked below", 24, STRUCT_COL).move_to([5.15, -0.95, 0])
        self.play(FadeIn(hb_tag), paco2.animate.set_value(30.0), run_time=1.2)
        self.finish()


class S11Brake(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(34.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(1.50)
        b_speed = ValueTracker(6.5)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(b_speed.get_value() * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        ctrl = make_controller_chip(pos=(5.30, 2.20, 0))
        carotid = make_carotid_sensor(pos=(5.30, 1.02, 0))

        band_box = Rectangle(width=0.66, height=1.40, color=STRUCT_COL, stroke_width=2.5, fill_color=H_COL, fill_opacity=0.10).move_to([3.70, -0.35, 0])
        rng = np.random.default_rng(23)
        h_dots = VGroup(*[
            Dot([3.70 + rng.uniform(-0.22, 0.22), -0.35 + rng.uniform(-0.56, 0.56), 0], radius=0.06, color=H_COL)
            for _ in range(18)
        ])
        ph_lab = T("pH up", 26, H_COL).next_to(band_box, DOWN, buff=0.18)

        # Continuous TEAL CO2 washout stream while paco2 drops 34 -> 30
        co2_stream = VGroup()
        for i in range(12):
            d = Dot(radius=0.055, color=CO2_COL).set_opacity(0.0)
            d._x0 = float(COL_X + rng.uniform(-0.6, 0.6))
            d._t = float(i * 0.18)
            co2_stream.add(d)
        co2_stream.layout_ok = True
        stream_on = ValueTracker(1.0)

        def upd_stream(mob, dt):
            on = stream_on.get_value()
            for d in mob:
                d._t = (d._t + dt * 1.1) % 2.0
                if on < 0.5:
                    d.set_opacity(0.0)
                else:
                    y = y_mmhg(95.1) + 0.1 + d._t * 0.95
                    d.move_to([d._x0, y, 0])
                    d.set_opacity(max(0.0, 0.85 * (1.0 - d._t / 2.0)))

        co2_stream.add_updater(upd_stream)

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, ctrl, carotid, band_box, h_dots, co2_stream)

        self.at("Washing out carbon dioxide")
        self.play(paco2.animate.set_value(30.0), run_time=2.4, rate_func=linear)

        self.at("raises pH")
        self.play(
            LaggedStart(*[FadeOut(d, shift=UP * 0.15) for d in h_dots[7:]], lag_ratio=0.08),
            FadeIn(ph_lab),
            run_time=2.4,
        )

        def inhib_bar(start, end):
            u = end - start
            u = u / np.linalg.norm(u)
            perp = np.array([-u[1], u[0], 0.0])
            return VGroup(Line(start, end, color=H_COL, stroke_width=5), Line(end - perp * 0.15, end + perp * 0.15, color=H_COL, stroke_width=5.5))

        bar_ctrl = inhib_bar(band_box.get_top() + UP * 0.04 + LEFT * 0.08, ctrl.get_left() + LEFT * 0.10)
        bar_car = inhib_bar(band_box.get_top() + UP * 0.04 + RIGHT * 0.16, carotid[3].get_left() + LEFT * 0.14)

        self.at("inhibits ventilation")
        self.play(Create(bar_ctrl), run_time=1.4)

        self.at("carotid body")
        stream_on.set_value(0.0)
        self.play(Create(bar_car), b_amp.animate.set_value(0.80), b_speed.animate.set_value(3.4), run_time=0.8)
        held_br = BraceBetweenPoints([COL_X + 0.94, -2.58, 0], [COL_X + 0.94, -1.94, 0], direction=RIGHT, color=STRUCT_COL)
        held_lab = T("held back", 24, STRUCT_COL).next_to(held_br, RIGHT, buff=0.10)
        self.play(GrowFromCenter(held_br), FadeIn(held_lab), run_time=0.5)
        self.finish()


class S12Days(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(30.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(0.85)
        b_speed = ValueTracker(3.8)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(b_speed.get_value() * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        ctrl = make_controller_chip(pos=(5.30, 2.20, 0))
        carotid = make_carotid_sensor(pos=(5.30, 1.02, 0))

        band_box = Rectangle(width=0.66, height=1.40, color=STRUCT_COL, stroke_width=2.5, fill_color=H_COL, fill_opacity=0.10).move_to([3.70, -0.35, 0])
        rng = np.random.default_rng(23)
        h_pts = [np.array([3.70 + rng.uniform(-0.22, 0.22), -0.35 + rng.uniform(-0.56, 0.56), 0]) for _ in range(18)]
        h_dots_kept = VGroup(*[Dot(p, radius=0.055, color=H_COL) for p in h_pts[:7]])
        h_dots_rec = VGroup(*[Dot(p, radius=0.055, color=H_COL) for p in h_pts[7:13]])

        def inhib_bar(start, end):
            u = end - start
            u = u / np.linalg.norm(u)
            perp = np.array([-u[1], u[0], 0.0])
            return VGroup(Line(start, end, color=H_COL, stroke_width=4), Line(end - perp * 0.14, end + perp * 0.14, color=H_COL, stroke_width=5))

        bar_ctrl = inhib_bar(band_box.get_top() + UP * 0.04 + LEFT * 0.08, ctrl.get_left() + LEFT * 0.10)
        bar_car = inhib_bar(band_box.get_top() + UP * 0.04 + RIGHT * 0.16, carotid[3].get_left() + LEFT * 0.14)

        # Bottom time strip cleanly below 'barometric' (-2.64)
        strip_y = -3.34
        strip_line = Line([-5.6, strip_y, 0], [3.2, strip_y, 0], color=STRUCT_COL, stroke_width=3)
        marks = [("seconds", -5.0), ("hours", -2.5), ("days", 0.0), ("longer", 2.5)]
        strip_ticks = VGroup()
        strip_labs = VGroup()
        for name, mx in marks:
            strip_ticks.add(Line([mx, strip_y - 0.08, 0], [mx, strip_y + 0.08, 0], color=STRUCT_COL, stroke_width=3))
            strip_labs.add(T(name, 22, STRUCT_COL).next_to([mx, strip_y + 0.10, 0], UP, buff=0.08))
        time_x = ValueTracker(-5.0)
        time_dot = always_redraw(lambda: Dot([time_x.get_value(), strip_y, 0], radius=0.10, color=FOCUS_COL))
        time_dot.add_updater(lambda m, dt: time_x.set_value(min(0.0, time_x.get_value() + (5.0 / 11.5) * dt)))

        # Kidney icon cleanly separated at bottom-right above scope_tag
        kidney_c = np.array([5.30, -1.05, 0.0])
        kidney_outer = ArcBetweenPoints(kidney_c + UP * 0.30 + LEFT * 0.10, kidney_c + DOWN * 0.30 + LEFT * 0.10, angle=-2.6, color=STRUCT_COL, stroke_width=4)
        kidney_inner = ArcBetweenPoints(kidney_c + UP * 0.30 + LEFT * 0.10, kidney_c + DOWN * 0.30 + LEFT * 0.10, angle=0.6, color=STRUCT_COL, stroke_width=4)
        kidney_lab = T("kidney", 24, STRUCT_COL).next_to(kidney_c, DOWN, buff=0.36)
        kidney = VGroup(kidney_outer, kidney_inner, kidney_lab)
        k_arr = Arrow(kidney_c + LEFT * 0.25, band_box.get_right() + RIGHT * 0.08 + DOWN * 0.45, color=STRUCT_COL, stroke_width=3.5, buff=0.05)

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, ctrl, carotid, band_box, h_dots_kept, bar_ctrl, bar_car)
        self.add(strip_line, strip_ticks, strip_labs, time_dot)

        self.at("kidney acts on")
        self.play(FadeIn(kidney), GrowArrow(k_arr), FadeIn(h_dots_rec), run_time=2.0)

        self.at("sensors grow more sensitive")
        self.play(
            ctrl[0].animate.set_stroke(width=4.5, color=FOCUS_COL),
            carotid[3].animate.set_fill(FOCUS_COL, opacity=0.85),
            bar_ctrl.animate.set_stroke(width=1.8).set_opacity(0.45),
            bar_car.animate.set_stroke(width=1.8).set_opacity(0.45),
            run_time=2.0,
        )

        self.at("climb further")
        self.play(
            b_amp.animate.set_value(1.45),
            b_speed.animate.set_value(6.4),
            paco2.animate.set_value(26.0),
            run_time=2.6,
        )

        self.at("asks for each")
        clocks_tag = T("clocks: asked below", 24, STRUCT_COL).move_to([5.05, -2.42, 0])
        self.play(FadeIn(clocks_tag), run_time=1.0)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        pb = ValueTracker(500.0)
        paco2 = ValueTracker(40.0)
        climb = ValueTracker(1.0)
        b_phase = ValueTracker(0.0)
        b_amp = ValueTracker(1.35)

        bellows = make_bellows(b_phase, b_amp)
        bellows.add_updater(lambda m, dt: b_phase.increment_value(4.8 * dt))

        mtn = make_mountain()
        climber = make_climber(climb, b_amp, b_phase)
        dial_g = make_baro_dial(pb)
        ruler = make_ruler()
        col = make_gas_column(pb, paco2, show_co2=True)
        dots = make_o2_dots(pb, paco2, n=18, seed=7)
        vent_lab = T("ventilation", 26, VENT_COL).next_to([COL_X - 0.90, -2.26, 0], LEFT, buff=0.22)
        tag = scope_tag("model values", size=24, color=STRUCT_COL)
        ctrl = make_controller_chip(pos=(5.30, 2.20, 0))
        carotid = make_carotid_sensor(pos=(5.30, 1.02, 0))
        ring = always_redraw(
            lambda: Circle(radius=0.11, color=FOCUS_COL, stroke_width=4)
            .move_to([RULER_X, y_mmhg(alveolar_po2(500.0, paco2.get_value())), 0])
        )
        rem_lab = make_col_po2_label(lambda: alveolar_po2(500.0, paco2.get_value()))

        self.add(mtn, climber, dial_g, ruler, col, dots, bellows, vent_lab, tag, ctrl, carotid, ring, rem_lab)

        self.at("nothing in the controller")
        self.play(
            Indicate(ctrl[0], color=CTRL_COL, scale_factor=1.08),
            Indicate(carotid[:4], color=TEXT, scale_factor=1.08),
            paco2.animate.set_value(30.0),
            run_time=2.4,
        )

        self.at("mountain carried")
        self.play(paco2.animate.set_value(40.0), run_time=2.0)

        self.at("same single lever")
        self.play(paco2.animate.set_value(30.0), run_time=2.2)
        self.play(paco2.animate.set_value(40.0), run_time=2.2)
        self.finish()


class S14End(EndCard):
    LINE = "Altitude moves the operating point to where breathing finally buys oxygen."
