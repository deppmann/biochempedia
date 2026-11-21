"""
Who Winds the Spring? — Chapter 2 of "The Pyruvate Dehydrogenase Complex: The One-Way Gate to the Cycle"

COLOUR MAP (one colour per concept for the whole film):
- YELLOW (#F5D547): carbon cargo (pyruvate, 2-carbon acetyl unit, acetate)
- GREEN  (#83C167): acetyl-CoA, thioester, coil spring, forward arrow
- ORANGE (#FF9F43): electrons (2 e-), NADH, oxidation energy drop (-50 kJ/mol)
- BLUE   (#58C4DD): enzymes and the complex (E1, E2 core, E3)
- PINK   (#F472B6): coenzymes (lipoamide swinging arm, CoA)
- GREY   (#8B93A1): CO2, axes, ledger structure and shelves, cliff/valley ground
- RED    (#FC6255): blocked / not allowed crosses
- PURPLE (#B388FF): ATP (blocked at entrance; -30.5 kJ/mol reference line)
- CYAN   (#00E5FF): ordinary oxygen ester
- WHITE  (#FFFFFF): energy-level ball, water drops, primary contrast highlights

THE ONE WORLD (carried across scenes):
- Left 35%: the PDC complex (BLUE E2 core circle at [-4.75, -0.25, 0], BLUE E1 ellipse upper-left,
  BLUE E3 ellipse upper-right, PINK lipoamide arm tethered to E2 that swings between E1, E2, E3).
- Right 60%: the energy ledger (vertical axis at x = -0.85 from +10 at y = +2.35 down to -60 at y = -2.20,
  ticks every 10, WHITE ball on energy shelves, three sequential entry slots at x = 0.95, 3.10, 5.15).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Pyruvate chip moves into E1 as PINK arm swings along a circular arc E1->E2->E3;
  CO2 bubble rises, acetyl-CoA exits right with a parametric helical spring that quivers, NADH exits down;
  PURPLE ATP is rejected at entrance; WHITE ball sits at 0 kJ/mol.
- s02_books: Complex dims to 55% while arm keeps sweeping; ghost WHITE ball rolls down (0 to -22)
  and up (0 to +10) on computed vertical paths with a live kJ/mol counter; three ledger slots build.
- s03_oxidation: 2 C unit oxidizes at E1 (YELLOW->ORANGE) and 2 e- dots ride the swinging arm E1->E2->E3
  into NADH; ValueTracker dg1 (0 -> -50 kJ/mol) grows the ORANGE downward bar and moves the WHITE ball to -50.
- s04_thioester: Acetyl snaps onto CoA into acetyl-CoA while free-acetate ghost is crossed out;
  ValueTracker dg2 (-50 -> -19 kJ/mol) drives both the GREEN +31 bar and the helical spring's
  computed coil compression simultaneously; GREEN bracket spans 31 of the 50 oxidation units.
- s05_co2: CO2 bubble rises out of complex; ValueTracker dg3 (-19 -> -33 kJ/mol) grows the GREY -14
  bar and rolls the WHITE ball to -33; running sum builds -50 + 31 - 14 = -33; WHITE bracket spans 0 to -33.
- s06_idea: Computed energy-transfer arcs connect oxidation (-50) to NADH and to the +31 thioester
  bar+spring; top 19 units of ORANGE bar and 14 units of CO2 bar highlight and slide into the 0..-33 bracket.
- s07_one_way: K_eq = exp(33 / (0.008314 * 310.15)) (~4e5) is computed and counted up to 4 x 10^5;
  YELLOW pyruvate chips stream continuously through the GREEN forward arrow into GREEN acetyl-CoA chips
  while a backward chip bounces off the RED-crossed backward arrow.
- s08_predict: Complex and ledger shrink into compact top insets; two large side-by-side chips
  (CYAN oxygen ester, GREEN thioester) appear with identical parametric springs and bobbing WHITE water drops.
- s10_answer: Water drops fall onto both chips and uncoil their springs; ValueTrackers e_o (0 -> -21)
  and e_s (0 -> -31) grow CYAN and GREEN hydrolysis bars past a PURPLE -30.5 ATP line; inset ledger
  +31 arrow pulses with the -31 hydrolysis bar.
- s11_why: 'stored in the bond?' is crossed out; CYAN O (r=0.72) and GREEN S (r=1.22) discs show
  strong vs faint C=O overlap glow and computed schematic resonance bars; GREEN thioester boulder
  rolls down a computed sigmoid cliff profile and splits into acetate and CoA in the valley.
- s12_close: Full world returns; ATP is rejected; oxidation and NADH highlight; two wound acetyl-CoA chips
  travel right into citric acid cycle and fatty-acid synthesis tokens while forward traffic streams.
"""
from bp_parts import *

# ---- Concept Palette ----
ORANGE = "#FF9F43"
PINK = "#F472B6"
PURPLE = "#B388FF"
CYAN = "#00E5FF"

# ---- Thermodynamic constants (from lesson_for_context.mdx) ----
DG_OX = -50.0
DG_THIO = 31.0
DG_CO2 = -14.0
DG_TOTAL = DG_OX + DG_THIO + DG_CO2  # -33.0 kJ/mol
R_KJ = 0.008314
T_BODY = 310.15
K_EQ = float(np.exp(-DG_TOTAL / (R_KJ * T_BODY)))  # ~3.63e5 -> lesson rounded value 4 x 10^5
DG_O_ESTER = -21.0
DG_S_ESTER = -31.0
DG_ATP = -30.5

# ---- Shared World Coordinates ----
CX_E2 = -4.75
CY_E2 = -0.25
R_E2 = 0.90
POS_E2 = np.array([CX_E2, CY_E2, 0.0])
POS_E1 = np.array([CX_E2 - 0.85, CY_E2 + 1.50, 0.0])   # [-5.60, 1.25]
POS_E3 = np.array([CX_E2 + 0.85, CY_E2 + 1.50, 0.0])   # [-3.90, 1.25]
ARM_PIVOT = np.array([CX_E2, CY_E2 + 0.30, 0.0])       # [-4.75, +0.05]

ARM_LEN = 0.72
ANGLE_E1 = np.deg2rad(132)
ANGLE_E2 = np.deg2rad(-25)
ANGLE_E3 = np.deg2rad(48)

# Ledger geometry (right 60%)
LED_X_AXIS = -0.85
LED_X_RIGHT = 6.10
LED_Y_TOP = 2.35     # +10 kJ/mol
LED_Y_BOT = -2.20    # -60 kJ/mol
SLOT_X = [0.95, 3.10, 5.15]

# Carried chip positions (clear of E2 right edge -3.85 and tick left edge -1.45)
ACOA_POS = np.array([-2.78, -0.35, 0.0])
NADH_POS = np.array([-3.25, -1.75, 0.0])


def ledger_y(dg):
    """Map free energy (kJ/mol) in [-60, +10] linearly to scene y."""
    return LED_Y_BOT + (dg - (-60.0)) / 70.0 * (LED_Y_TOP - LED_Y_BOT)


def make_spring(p0, p1, turns=6.0, radius=0.13, color=GREEN, stroke_width=4.2):
    """Computed 2D projection of a helical coil spring between p0 and p1."""
    p0 = np.array(p0, dtype=float)
    p1 = np.array(p1, dtype=float)
    vec = p1 - p0
    length = max(float(np.linalg.norm(vec)), 1e-4)
    u = vec / length
    v = np.array([-u[1], u[0], 0.0])
    s = np.linspace(0.0, 1.0, 150)
    env = np.sin(np.pi * np.clip((s - 0.08) / 0.84, 0.0, 1.0))
    pts = [
        p0 + (si * length) * u + (radius * env_i * np.sin(2.0 * np.pi * turns * si)) * v
        for si, env_i in zip(s, env)
    ]
    m = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
    m.set_points_as_corners(pts)
    return m


def make_teardrop(center, height=0.80, color=WHITE):
    """Computed parametric teardrop for a water drop."""
    c = np.array(center, dtype=float)
    t = np.linspace(0.0, 2.0 * np.pi, 80)
    w = height * 0.36
    h = height * 0.50
    x = w * np.sin(t) * (np.sin(t / 2.0) ** 1.3)
    y = -h * np.cos(t)
    pts = [c + np.array([xi, yi, 0.0]) for xi, yi in zip(x, y)]
    m = VMobject(stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.36)
    m.set_points_as_corners(pts)
    m.close_path()
    return m


def make_arm(angle_rad, pivot=ARM_PIVOT, length=ARM_LEN, color=PINK):
    """Lipoamide swinging arm from pivot at angle_rad with a fork tip."""
    u = np.array([np.cos(angle_rad), np.sin(angle_rad), 0.0])
    end = pivot + length * u
    stem = Line(pivot, end, color=color, stroke_width=5.5)
    hub = Dot(pivot, radius=0.09, color=color)
    tip = Arc(radius=0.12, start_angle=angle_rad - 1.1, angle=2.2, arc_center=end, color=color, stroke_width=4.0)
    return VGroup(stem, hub, tip)


def build_complex(opacity=1.0):
    """Build the PDC complex at left 35% of the frame."""
    e2_circle = Circle(radius=R_E2, color=BLUE, stroke_width=4.2, fill_color=BLUE, fill_opacity=0.34 * opacity).move_to(POS_E2)
    e2_label = T("E2", size=30, color=WHITE).move_to(POS_E2 + DOWN * 0.45)

    e1_ell = Ellipse(width=1.58, height=0.94, color=BLUE, stroke_width=4.0, fill_color=BLUE, fill_opacity=0.34 * opacity).move_to(POS_E1)
    e1_label = T("E1", size=28, color=WHITE).move_to(POS_E1)

    e3_ell = Ellipse(width=1.58, height=0.94, color=BLUE, stroke_width=4.0, fill_color=BLUE, fill_opacity=0.34 * opacity).move_to(POS_E3)
    e3_label = T("E3", size=28, color=WHITE).move_to(POS_E3)

    g = VGroup(e2_circle, e1_ell, e3_ell, e2_label, e1_label, e3_label)
    g.e2, g.e1, g.e3 = e2_circle, e1_ell, e3_ell
    if opacity < 1.0:
        for m in (e2_circle, e1_ell, e3_ell):
            m.set_stroke(opacity=opacity)
        for lb in (e2_label, e1_label, e3_label):
            lb.set_opacity(opacity)
    return g


def build_ledger(include_ball=True, include_ph=True):
    """Build the energy ledger at right 60% of the frame."""
    panel = RoundedRectangle(
        corner_radius=0.14, width=LED_X_RIGHT - LED_X_AXIS + 0.1, height=LED_Y_TOP - LED_Y_BOT + 0.2,
        stroke_color=GREY, stroke_width=1.4, fill_color="#181C26", fill_opacity=0.70,
    ).move_to([(LED_X_AXIS + LED_X_RIGHT) / 2 + 0.05, (LED_Y_TOP + LED_Y_BOT) / 2, 0])
    panel.layout_ok = True

    y_axis = Line([LED_X_AXIS, LED_Y_BOT, 0], [LED_X_AXIS, LED_Y_TOP, 0], color=GREY, stroke_width=3.4)
    y0 = ledger_y(0.0)
    zero_line = DashedLine([LED_X_AXIS, y0, 0], [LED_X_RIGHT, y0, 0], color=GREY, stroke_width=2.5, dash_length=0.14)

    ticks = VGroup()
    tick_labels = VGroup()
    for val in range(-60, 11, 10):
        yv = ledger_y(val)
        ticks.add(Line([LED_X_AXIS - 0.12, yv, 0], [LED_X_AXIS, yv, 0], color=GREY, stroke_width=2.8))
        lab = M(f"{val:+d}" if val > 0 else f"{val}", size=22, color=TEXT).next_to([LED_X_AXIS - 0.14, yv, 0], LEFT, buff=0.08)
        tick_labels.add(lab)

    ylabel = T("free energy (kJ/mol)", size=24, color=TEXT).move_to([LED_X_AXIS + 1.35, LED_Y_TOP + 0.40, 0])
    g = VGroup(panel, y_axis, zero_line, ticks, tick_labels, ylabel)
    g.y_axis = y_axis
    g.zero_line = zero_line

    if include_ph:
        ph_tag = T("standard values, pH 7", size=24, color=TEXT).move_to([-0.25, -3.15, 0])
        g.add(ph_tag)
        g.ph_tag = ph_tag

    shelf_0 = Line([-0.42, y0, 0], [0.16, y0, 0], color=GREY, stroke_width=4.5)
    g.add(shelf_0)
    g.shelf_0 = shelf_0

    if include_ball:
        ball_0 = Dot([-0.13, y0 + 0.14, 0], radius=0.14, color=WHITE, stroke_color=TEXT, stroke_width=1.5)
        pyr_lab = T("pyruvate", size=24, color=TEXT).next_to(ball_0, UP, buff=0.12)
        g.add(ball_0, pyr_lab)
        g.ball = ball_0
        g.pyr_lab = pyr_lab
    return g


def ledger_bar(x, y_from, y_to, color, bar_w=0.44, fill_opacity=0.90):
    """Wide filled energy bar with an arrowhead from y_from to y_to at x."""
    dy = y_to - y_from
    if abs(dy) < 0.04:
        return VGroup()
    sgn = 1.0 if dy > 0 else -1.0
    head_h = min(0.28, abs(dy) * 0.45)
    stem_end = y_to - sgn * head_h
    pts_bar = [
        [x - bar_w / 2, y_from, 0],
        [x + bar_w / 2, y_from, 0],
        [x + bar_w / 2, stem_end, 0],
        [x + bar_w * 0.82, stem_end, 0],
        [x, y_to, 0],
        [x - bar_w * 0.82, stem_end, 0],
        [x - bar_w / 2, stem_end, 0],
    ]
    poly = Polygon(*pts_bar, color=color, stroke_width=2.0, fill_color=color, fill_opacity=fill_opacity)
    return poly


def ledger_arrow(x, dg_from, dg_to, color, bar_w=0.44):
    """Filled vertical energy bar-arrow between dg_from and dg_to at x."""
    return ledger_bar(x, ledger_y(dg_from), ledger_y(dg_to), color, bar_w=bar_w)


def make_cross(mob, color=RED, pad=0.08):
    """Build a crisp RED X over a mobject (marked layout_ok for deliberate strike-through)."""
    dl = mob.get_corner(DL) + np.array([-pad, -pad, 0])
    ur = mob.get_corner(UR) + np.array([pad, pad, 0])
    ul = mob.get_corner(UL) + np.array([-pad, pad, 0])
    dr = mob.get_corner(DR) + np.array([pad, -pad, 0])
    c = VGroup(Line(dl, ur, color=color, stroke_width=5.5), Line(ul, dr, color=color, stroke_width=5.5))
    c.layout_ok = True
    return c


def slot_bases():
    """Three empty slot markers along the ledger baseline."""
    y_base = LED_Y_BOT - 0.25
    slots = VGroup()
    for idx, sx in enumerate(SLOT_X, 1):
        bar = Line([sx - 0.42, y_base, 0], [sx + 0.42, y_base, 0], color=GREY, stroke_width=3.2)
        num = M(f"{idx}", size=24, color=TEXT).next_to(bar, DOWN, buff=0.10)
        slots.add(VGroup(bar, num))
    return slots


def add_three_ledger_entries(show_labels=True):
    """Return the completed 3 bars, shelves, and optional labels for s05/s06/s07/s12."""
    a1 = ledger_arrow(SLOT_X[0], 0.0, DG_OX, ORANGE)
    s1 = Line([SLOT_X[0] - 0.40, ledger_y(DG_OX), 0], [SLOT_X[0] + 0.40, ledger_y(DG_OX), 0], color=GREY, stroke_width=4)
    a2 = ledger_arrow(SLOT_X[1], DG_OX, DG_OX + DG_THIO, GREEN)
    s2 = Line([SLOT_X[1] - 0.40, ledger_y(DG_OX + DG_THIO), 0], [SLOT_X[1] + 0.40, ledger_y(DG_OX + DG_THIO), 0], color=GREY, stroke_width=4)
    a3 = ledger_arrow(SLOT_X[2], DG_OX + DG_THIO, DG_TOTAL, GREY)
    s3 = Line([SLOT_X[2] - 0.40, ledger_y(DG_TOTAL), 0], [SLOT_X[2] + 0.40, ledger_y(DG_TOTAL), 0], color=GREY, stroke_width=4)
    items = [a1, s1, a2, s2, a3, s3]
    if show_labels:
        l1 = T("oxidation\n~ -50", size=24, color=ORANGE, line_spacing=0.85).move_to([SLOT_X[0] + 1.02, ledger_y(-8.0), 0])
        l2 = T("thioester\n~ +31", size=24, color=GREEN, line_spacing=0.85).move_to([SLOT_X[1] + 1.00, ledger_y(-8.0), 0])
        l3 = T("lose CO2\n~ -14", size=24, color=TEXT, line_spacing=0.85).move_to([SLOT_X[2], ledger_y(-42.5), 0])
        items.extend([l1, l2, l3])
    return VGroup(*items)


def overall_bracket_group():
    """WHITE bracket spanning 0 to -33 on the left of the ledger."""
    x_b = 0.42
    y_top, y_bot = ledger_y(0.0), ledger_y(DG_TOTAL)
    brace = VGroup(
        Line([x_b + 0.14, y_top, 0], [x_b, y_top, 0], color=WHITE, stroke_width=3.5),
        Line([x_b, y_top, 0], [x_b, y_bot, 0], color=WHITE, stroke_width=3.5),
        Line([x_b, y_bot, 0], [x_b + 0.14, y_bot, 0], color=WHITE, stroke_width=3.5),
    )
    lab = T("overall\n~ -33", size=24, color=WHITE, line_spacing=0.85).move_to([-0.22, (y_top + y_bot) / 2, 0])
    return VGroup(brace, lab)


def make_reaction_stream(flow_t, y_lane=-1.35, x_left=-5.95, x_mid=-4.25, span=1.50):
    """Shared helper: stream of YELLOW pyruvate -> GREEN acetyl-CoA chips."""
    g = VGroup()
    for phase in (0.0, 0.33, 0.66):
        p = (flow_t.get_value() * 0.48 + phase) % 1.0
        if p < 0.45:
            x = x_left + (p / 0.45) * span
            dot = RoundedRectangle(corner_radius=0.08, width=0.68, height=0.30, color=YELLOW, fill_color=YELLOW, fill_opacity=0.72).move_to([x, y_lane, 0])
        else:
            x = x_mid + ((p - 0.45) / 0.55) * (span + 0.35)
            dot = RoundedRectangle(corner_radius=0.08, width=0.75, height=0.30, color=GREEN, fill_color=GREEN, fill_opacity=0.72).move_to([x, y_lane, 0])
        g.add(dot)
    return g


def compact_complex_inset(center=(-4.85, 2.50, 0)):
    """Compact PDC inset for top-left in s08/s09/s10."""
    c = np.array(center, dtype=float)
    e2 = Circle(radius=0.38, color=BLUE, stroke_width=3.0, fill_color=BLUE, fill_opacity=0.28).move_to(c + DOWN * 0.18)
    e1 = Ellipse(width=0.68, height=0.40, color=BLUE, stroke_width=2.8, fill_color=BLUE, fill_opacity=0.28).move_to(c + np.array([-0.42, 0.42, 0]))
    e3 = Ellipse(width=0.68, height=0.40, color=BLUE, stroke_width=2.8, fill_color=BLUE, fill_opacity=0.28).move_to(c + np.array([0.42, 0.42, 0]))
    arm = make_arm(ANGLE_E3, pivot=c + UP * 0.10, length=0.42)
    lab = T("PDC", size=24, color=BLUE).next_to(e2, DOWN, buff=0.12)
    return VGroup(e2, e1, e3, arm, lab)


def compact_ledger_inset(center=(4.75, 2.50, 0)):
    """Compact energy-ledger inset for top-right in s08/s09/s10."""
    c = np.array(center, dtype=float)
    w, h = 2.6, 1.45
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=GREY, stroke_width=2.2,
                           fill_color="#181C26", fill_opacity=0.92).move_to(c)
    y_zero = c[1] + 0.46
    y_m50 = c[1] - 0.50
    y_m19 = y_m50 + 0.60
    y_m33 = y_m19 - 0.27
    zline = DashedLine([c[0] - 1.0, y_zero, 0], [c[0] + 1.0, y_zero, 0], color=GREY, stroke_width=1.8, dash_length=0.1)
    a1 = ledger_bar(c[0] - 0.65, y_zero, y_m50, ORANGE, bar_w=0.22)
    a2 = ledger_bar(c[0] + 0.00, y_m50, y_m19, GREEN, bar_w=0.22)
    a3 = ledger_bar(c[0] + 0.65, y_m19, y_m33, GREY, bar_w=0.22)
    lab = T("ledger (-33)", size=24, color=TEXT).next_to(box, DOWN, buff=0.12)
    g = VGroup(box, zline, a1, a2, a3, lab)
    g.green_arrow = a2
    g.box = box
    return g


# ==============================================================================
# SCENES
# ==============================================================================

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        cpx = build_complex()
        led = build_ledger()
        arm_ang = ValueTracker(ANGLE_E1)
        arm = always_redraw(lambda: make_arm(arm_ang.get_value()))

        self.play(FadeIn(cpx), FadeIn(arm), Create(led), run_time=0.9)

        # Recap motion across the first sentence
        self.at("one pyruvate")
        pyr = chip("pyruvate", YELLOW, size=24, pad=0.18, fill_opacity=0.32).move_to([-5.60, 2.60, 0])
        self.play(
            FadeIn(pyr, shift=RIGHT * 0.25),
            cpx.e1.animate.set_fill(opacity=0.60),
            led.ball.animate.shift(UP * 0.08),
            run_time=0.8,
        )
        self.play(
            pyr.animate.move_to([-5.60, 2.22, 0]),
            led.ball.animate.shift(DOWN * 0.08),
            run_time=1.0,
        )

        self.at("and left as")
        acoa = chip("acetyl-CoA", GREEN, size=22, pad=0.18, fill_opacity=0.32).move_to(ACOA_POS)
        self.play(
            FadeOut(pyr, scale=0.65),
            cpx.e1.animate.set_fill(opacity=0.34),
            cpx.e2.animate.set_fill(opacity=0.60),
            arm_ang.animate.set_value(ANGLE_E2),
            run_time=1.4,
        )
        self.play(FadeIn(acoa, shift=RIGHT * 0.30), run_time=0.8)

        self.at("carbon dioxide")
        co2 = boxed_label("CO2", GREY, size=24, pad=0.18, fill_opacity=0.35).move_to([-5.60, 2.32, 0])
        self.play(FadeIn(co2, shift=UP * 0.15), run_time=0.55)
        self.play(co2.animate.shift(UP * 0.85).set_opacity(0.0), run_time=1.0)
        self.remove(co2)

        self.at("and NADH")
        nadh = chip("NADH", ORANGE, size=24, pad=0.20, fill_opacity=0.32).move_to(NADH_POS)
        self.play(
            cpx.e2.animate.set_fill(opacity=0.34),
            cpx.e3.animate.set_fill(opacity=0.60),
            arm_ang.animate.set_value(ANGLE_E3),
            run_time=1.8,
        )
        self.play(FadeIn(nadh, shift=DOWN * 0.25), cpx.e3.animate.set_fill(opacity=0.34), run_time=0.9)

        # On 'wound spring', tight GREEN coil spring appears on acetyl-CoA and quivers visibly
        self.at("wound spring")
        quiv_t = ValueTracker(0.0)
        spr_anchor = acoa.get_top() + UP * 0.14
        spring = always_redraw(lambda: make_spring(
            spr_anchor + LEFT * 0.65,
            spr_anchor + LEFT * 0.65 + RIGHT * (1.30 + 0.12 * np.sin(8.0 * quiv_t.get_value())),
            turns=7.5, radius=0.16, color=GREEN, stroke_width=4.5,
        ))
        spring_driver = Dot().set_opacity(0)
        spring_driver.add_updater(lambda m, dt: quiv_t.increment_value(dt))
        self.add(spring_driver)
        self.play(FadeIn(spring), arm_ang.animate.set_value(ANGLE_E1), run_time=1.2)

        # On 'no ATP went in', PURPLE ATP slides toward E1 entrance and is turned back by RED cross
        self.at("no ATP went in")
        atp = chip("ATP", PURPLE, size=24, pad=0.18, fill_opacity=0.26).move_to([-5.70, 2.85, 0])
        self.play(FadeIn(atp, shift=RIGHT * 0.2), run_time=0.45)
        self.play(atp.animate.move_to([-5.60, 2.35, 0]), arm_ang.animate.set_value(ANGLE_E2), run_time=0.8)
        x_mark = make_cross(atp)
        self.play(Create(x_mark), run_time=0.4)
        self.play(atp.animate.shift(LEFT * 0.45).set_opacity(0), FadeOut(x_mark), run_time=0.6)
        self.remove(atp)

        # On 'So who wound it?', white question across top
        self.at("So who wound")
        q_txt = T("Who wound the spring?", size=34, color=WHITE).move_to([0.0, 3.25, 0])
        self.play(FadeIn(q_txt, shift=DOWN * 0.1), arm_ang.animate.set_value(ANGLE_E3), run_time=0.8)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        cpx = build_complex()
        led = build_ledger()
        acoa = chip("acetyl-CoA", GREEN, size=22, pad=0.18, fill_opacity=0.26).move_to(ACOA_POS)
        nadh = chip("NADH", ORANGE, size=24, pad=0.20, fill_opacity=0.26).move_to(NADH_POS)

        quiv_t = ValueTracker(0.0)
        spr_anchor = acoa.get_top() + UP * 0.14
        spring = always_redraw(lambda: make_spring(
            spr_anchor + LEFT * 0.65,
            spr_anchor + LEFT * 0.65 + RIGHT * (1.30 + 0.12 * np.sin(8.0 * quiv_t.get_value())),
            turns=7.5, radius=0.16, color=GREEN, stroke_width=4.5,
        ))
        arm_t = ValueTracker(0.0)
        arm = always_redraw(lambda: make_arm(ANGLE_E3 + 0.25 * np.sin(2.4 * arm_t.get_value())))
        driver = Dot().set_opacity(0)
        driver.add_updater(lambda m, dt: (quiv_t.increment_value(dt), arm_t.increment_value(dt)))

        q_txt = T("Who wound the spring?", size=34, color=WHITE).move_to([0.0, 3.25, 0])
        title = T("Who Winds the Spring?", size=40, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.40, 0])
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.07)

        self.add(cpx, led, acoa, nadh, spring, arm, driver, q_txt)
        self.play(swap(q_txt, VGroup(title, rule), run_time=0.9))
        self.finish()


class S02Books(SpokenScene):
    def construct(self):
        cpx = build_complex(opacity=1.0)
        led = build_ledger()
        acoa = chip("acetyl-CoA", GREEN, size=22, pad=0.18, fill_opacity=0.26).move_to(ACOA_POS)
        nadh = chip("NADH", ORANGE, size=24, pad=0.20, fill_opacity=0.26).move_to(NADH_POS)
        spr_anchor = acoa.get_top() + UP * 0.14
        quiv_t = ValueTracker(0.0)
        spring = always_redraw(lambda: make_spring(
            spr_anchor + LEFT * 0.65,
            spr_anchor + LEFT * 0.65 + RIGHT * (1.30 + 0.12 * np.sin(8.0 * quiv_t.get_value())),
            turns=7.5, radius=0.16, color=GREEN, stroke_width=4.5,
        ))
        arm_t = ValueTracker(0.0)
        arm = always_redraw(lambda: make_arm(ANGLE_E3 + 0.45 * np.sin(2.4 * arm_t.get_value())))
        driver = Dot().set_opacity(0)
        driver.add_updater(lambda m, dt: (quiv_t.increment_value(dt), arm_t.increment_value(dt)))

        title = T("Who Winds the Spring?", size=40, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.40, 0])
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.07)

        self.add(cpx, led, acoa, nadh, spring, arm, driver, title, rule)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.5)

        self.at("keep the energy")
        self.play(
            cpx.animate.set_opacity(0.55),
            acoa.animate.set_opacity(0.55),
            nadh.animate.set_opacity(0.55),
            run_time=1.0,
        )

        self.at("Pyruvate starts")
        ring_hi = Circle(radius=0.20, color=GOLD, stroke_width=3.5).move_to(led.ball)
        e_val = ValueTracker(0.0)
        e_ro = counter("{:+.0f} kJ/mol", e_val, at=[3.75, ledger_y(0.0) + 0.38, 0], size=26, color=TEXT)
        self.play(Create(ring_hi), FadeIn(e_ro), run_time=1.2)
        self.play(Indicate(led.pyr_lab, scale_factor=1.12, color=GOLD), FadeOut(ring_hi), run_time=1.8)

        # Downhill ghost ball + bar
        self.at("Downhill releases")
        y0 = ledger_y(0.0)
        g_dn = always_redraw(lambda: Dot([1.55, ledger_y(e_val.get_value()), 0], radius=0.15, color=WHITE).set_opacity(0.8))
        arr_dn = always_redraw(lambda: ledger_bar(2.15, y0, ledger_y(min(e_val.get_value(), -1.5)), GREY, bar_w=0.30, fill_opacity=0.65))
        lab_dn = T("energy released", size=26, color=TEXT).move_to([3.85, ledger_y(-12.0), 0])
        self.add(g_dn, arr_dn)
        self.play(e_val.animate.set_value(-22.0), FadeIn(lab_dn), run_time=1.45)
        self.remove(g_dn, arr_dn)
        self.play(FadeOut(lab_dn), e_val.animate.set_value(0.0), run_time=0.4)

        # Uphill ghost ball + bar
        self.at("uphill spends")
        g_up = always_redraw(lambda: Dot([1.55, ledger_y(e_val.get_value()), 0], radius=0.15, color=WHITE).set_opacity(0.8))
        arr_up = always_redraw(lambda: ledger_bar(2.15, y0, ledger_y(max(e_val.get_value(), 1.5)), GREY, bar_w=0.30, fill_opacity=0.65))
        lab_up = T("energy spent", size=26, color=TEXT).move_to([3.85, ledger_y(-6.0), 0])
        self.add(g_up, arr_up)
        self.play(e_val.animate.set_value(10.0), FadeIn(lab_up), run_time=1.3)
        self.remove(g_up, arr_up)
        self.play(FadeOut(lab_up), FadeOut(e_ro), run_time=0.45)

        # Three empty slots + order tag
        self.at("list three entries")
        slots = slot_bases()
        order_tag = T("ledger order, not reaction order", size=26, color=GOLD).move_to([3.05, 3.25, 0])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.12) for s in slots], lag_ratio=0.35), FadeIn(order_tag), run_time=1.9)
        self.finish()


class S03Oxidation(SpokenScene):
    def construct(self):
        cpx = build_complex(opacity=0.55)
        led = build_ledger()
        slots = slot_bases()
        order_tag = T("ledger order, not reaction order", size=26, color=GOLD).move_to([3.05, 3.25, 0])
        arm_ang = ValueTracker(ANGLE_E1)
        arm = always_redraw(lambda: make_arm(arm_ang.get_value()))
        self.add(cpx, led, slots, order_tag, arm)

        self.at("First entry")
        two_c = chip("2 C", YELLOW, size=24, pad=0.16, fill_opacity=0.28).move_to([-5.60, 2.28, 0])
        self.play(FadeIn(two_c, scale=0.85), Indicate(slots[0], scale_factor=1.2, color=ORANGE), run_time=1.6)

        self.at("Two carbons")
        glow = Circle(radius=0.50, color=ORANGE, stroke_width=4.0, fill_color=ORANGE, fill_opacity=0.35).move_to(two_c)
        ox_step = T("aldehyde -> acid", size=24, color=ORANGE).move_to([-4.65, 3.05, 0])
        self.play(FadeIn(glow), FadeIn(ox_step), cpx.e1.animate.set_fill(color=ORANGE, opacity=0.45), two_c.animate.set_color(ORANGE), run_time=2.6)
        self.play(FadeOut(glow), FadeOut(ox_step), cpx.e1.animate.set_fill(color=BLUE, opacity=0.20), run_time=1.2)

        self.at("electrons end")
        e_dots = VGroup(Dot(LEFT * 0.10, radius=0.11, color=ORANGE), Dot(RIGHT * 0.10, radius=0.11, color=ORANGE))
        e_dots.move_to(ARM_PIVOT + ARM_LEN * np.array([np.cos(ANGLE_E1), np.sin(ANGLE_E1), 0]))
        e_lab = T("2 e⁻", size=24, color=ORANGE).move_to([-4.75, 2.00, 0])
        nadh = chip("NADH", ORANGE, size=24, pad=0.20, fill_opacity=0.32).move_to(NADH_POS)
        self.play(FadeIn(e_dots), FadeIn(e_lab), run_time=0.5)

        def follow_tip(mob):
            ang = arm_ang.get_value()
            mob.move_to(ARM_PIVOT + ARM_LEN * np.array([np.cos(ang), np.sin(ang), 0]))

        e_dots.add_updater(follow_tip)
        self.play(arm_ang.animate.set_value(ANGLE_E2), cpx.e2.animate.set_fill(opacity=0.45), run_time=1.2)
        self.play(arm_ang.animate.set_value(ANGLE_E3), cpx.e2.animate.set_fill(opacity=0.20), cpx.e3.animate.set_fill(color=ORANGE, opacity=0.45), run_time=1.2)
        e_dots.remove_updater(follow_tip)
        self.play(FadeOut(e_lab), e_dots.animate.move_to(nadh.get_center()), FadeIn(nadh, shift=DOWN * 0.25), cpx.e3.animate.set_fill(color=BLUE, opacity=0.20), run_time=0.8)
        self.remove(e_dots)

        # In step with 'falls about 50', ValueTracker dg1 drives wide ORANGE bar & WHITE ball together
        self.at("falls about")
        dg1 = ValueTracker(0.0)
        y0 = ledger_y(0.0)
        ball_x = ValueTracker(-0.13)

        live_bar1 = always_redraw(lambda: ledger_bar(SLOT_X[0], y0, ledger_y(min(dg1.get_value(), -1.5)), ORANGE))
        led.remove(led.ball)
        self.remove(led.ball)
        rock_t = ValueTracker(0.0)
        ball = always_redraw(lambda: Dot(
            [ball_x.get_value() + (0.06 * np.sin(3.5 * rock_t.get_value()) if dg1.get_value() <= -49.5 else 0.0),
             ledger_y(dg1.get_value()) + 0.14, 0],
            radius=0.14, color=WHITE, stroke_color=TEXT, stroke_width=1.5,
        ))
        self.add(live_bar1, ball)
        self.play(ball_x.animate.set_value(SLOT_X[0]), run_time=0.35)
        self.play(dg1.animate.set_value(DG_OX), run_time=1.8, rate_func=smooth)

        shelf1 = Line([SLOT_X[0] - 0.40, ledger_y(DG_OX), 0], [SLOT_X[0] + 0.40, ledger_y(DG_OX), 0], color=GREY, stroke_width=4)
        lab1 = T("oxidation\n~ -50", size=24, color=ORANGE, line_spacing=0.85).move_to([SLOT_X[0] + 1.02, ledger_y(-8.0), 0])
        self.play(Create(shelf1), FadeIn(lab1), run_time=0.55)

        driver = Dot().set_opacity(0)
        driver.add_updater(lambda m, dt: rock_t.increment_value(dt))
        self.add(driver)
        self.finish()


class S04Thioester(SpokenScene):
    def construct(self):
        cpx = build_complex(opacity=0.55)
        led = build_ledger(include_ball=False)
        slots = slot_bases()
        order_tag = T("ledger order, not reaction order", size=26, color=GOLD).move_to([3.05, 3.25, 0])
        a1 = ledger_arrow(SLOT_X[0], 0.0, DG_OX, ORANGE)
        s1 = Line([SLOT_X[0] - 0.40, ledger_y(DG_OX), 0], [SLOT_X[0] + 0.40, ledger_y(DG_OX), 0], color=GREY, stroke_width=4)
        l1 = T("oxidation\n~ -50", size=24, color=ORANGE, line_spacing=0.85).move_to([SLOT_X[0] + 1.02, ledger_y(-8.0), 0])
        nadh = chip("NADH", ORANGE, size=24, pad=0.20, fill_opacity=0.26).move_to(NADH_POS)
        arm = make_arm(ANGLE_E2)

        acetyl = chip("acetyl", YELLOW, size=24, pad=0.14, fill_opacity=0.26).move_to([-3.20, 0.35, 0])
        coa = chip("CoA", PINK, size=24, pad=0.14, fill_opacity=0.26).move_to([-2.42, -0.45, 0])

        self.add(cpx, led, slots, order_tag, a1, s1, l1, nadh, arm, acetyl, coa)

        dg2 = ValueTracker(DG_OX)  # -50 -> -19
        ball_x = ValueTracker(SLOT_X[0])
        ball = always_redraw(lambda: Dot([ball_x.get_value(), ledger_y(dg2.get_value()) + 0.14, 0], radius=0.14, color=WHITE, stroke_color=TEXT, stroke_width=1.5))
        self.add(ball)

        self.at("acetyl group is stored")
        acoa = chip("acetyl-CoA", GREEN, size=22, pad=0.18, fill_opacity=0.26).move_to(ACOA_POS)
        self.play(acetyl.animate.move_to(ACOA_POS + UP * 0.32), coa.animate.move_to(ACOA_POS + DOWN * 0.32), run_time=1.3)
        self.play(ReplacementTransform(VGroup(acetyl, coa), acoa), run_time=0.8)

        spr_anchor = acoa.get_top() + UP * 0.14
        spring = always_redraw(lambda: make_spring(
            spr_anchor + LEFT * (0.95 - 0.30 * ((dg2.get_value() - DG_OX) / DG_THIO)),
            spr_anchor + RIGHT * (0.95 - 0.30 * ((dg2.get_value() - DG_OX) / DG_THIO)),
            turns=3.0 + 4.5 * ((dg2.get_value() - DG_OX) / DG_THIO),
            radius=0.12 + 0.04 * ((dg2.get_value() - DG_OX) / DG_THIO),
            color=GREEN, stroke_width=4.5,
        ))
        self.play(FadeIn(spring), run_time=0.7)

        self.at("not set free")
        free_ac = chip("free acetate", YELLOW, size=22, pad=0.16, fill_opacity=0.16).move_to([-5.25, -2.05, 0])
        x_free = make_cross(free_ac)
        self.play(FadeIn(free_ac), run_time=0.6)
        self.play(Create(x_free), run_time=0.6)
        self.play(FadeOut(free_ac), FadeOut(x_free), run_time=0.9)

        self.at("costs about")
        live_bar2 = always_redraw(lambda: ledger_bar(SLOT_X[1], ledger_y(DG_OX), ledger_y(max(dg2.get_value(), DG_OX + 1.5)), GREEN))
        self.add(live_bar2)
        self.play(ball_x.animate.set_value(SLOT_X[1]), run_time=0.5)
        self.play(dg2.animate.set_value(DG_OX + DG_THIO), run_time=2.2, rate_func=smooth)

        shelf2 = Line([SLOT_X[1] - 0.40, ledger_y(DG_OX + DG_THIO), 0], [SLOT_X[1] + 0.40, ledger_y(DG_OX + DG_THIO), 0], color=GREY, stroke_width=4)
        lab2 = T("thioester\n~ +31", size=24, color=GREEN, line_spacing=0.85).move_to([SLOT_X[1] + 1.00, ledger_y(-8.0), 0])
        self.play(Create(shelf2), FadeIn(lab2), run_time=0.6)

        self.at("most of the")
        x_brk = 1.32
        brk = VGroup(
            Line([x_brk - 0.14, ledger_y(DG_OX), 0], [x_brk, ledger_y(DG_OX), 0], color=GREEN, stroke_width=4.0),
            Line([x_brk, ledger_y(DG_OX), 0], [x_brk, ledger_y(-19.0), 0], color=GREEN, stroke_width=4.0),
            Line([x_brk, ledger_y(-19.0), 0], [x_brk - 0.14, ledger_y(-19.0), 0], color=GREEN, stroke_width=4.0),
        )
        brk_lab = T("31 of 50", size=24, color=GREEN).next_to(brk, RIGHT, buff=0.14)
        self.play(Create(brk), FadeIn(brk_lab), run_time=1.3)
        self.finish()


class S05Co2(SpokenScene):
    def construct(self):
        cpx = build_complex(opacity=0.55)
        led = build_ledger(include_ball=False)
        slots = slot_bases()
        order_tag = T("ledger order, not reaction order", size=26, color=GOLD).move_to([3.05, 3.25, 0])

        a1 = ledger_arrow(SLOT_X[0], 0.0, DG_OX, ORANGE)
        s1 = Line([SLOT_X[0] - 0.40, ledger_y(DG_OX), 0], [SLOT_X[0] + 0.40, ledger_y(DG_OX), 0], color=GREY, stroke_width=4)
        l1 = T("oxidation\n~ -50", size=24, color=ORANGE, line_spacing=0.85).move_to([SLOT_X[0] + 1.02, ledger_y(-8.0), 0])
        a2 = ledger_arrow(SLOT_X[1], DG_OX, -19.0, GREEN)
        s2 = Line([SLOT_X[1] - 0.40, ledger_y(-19.0), 0], [SLOT_X[1] + 0.40, ledger_y(-19.0), 0], color=GREY, stroke_width=4)
        l2 = T("thioester\n~ +31", size=24, color=GREEN, line_spacing=0.85).move_to([SLOT_X[1] + 1.00, ledger_y(-8.0), 0])

        nadh = chip("NADH", ORANGE, size=24, pad=0.20, fill_opacity=0.26).move_to(NADH_POS)
        acoa = chip("acetyl-CoA", GREEN, size=22, pad=0.18, fill_opacity=0.26).move_to(ACOA_POS)
        spr_anchor = acoa.get_top() + UP * 0.14
        q_t = ValueTracker(0.0)
        spring = always_redraw(lambda: make_spring(
            spr_anchor + LEFT * 0.65,
            spr_anchor + LEFT * 0.65 + RIGHT * (1.30 + 0.10 * np.sin(8.0 * q_t.get_value())),
            turns=7.5, radius=0.15, color=GREEN, stroke_width=4.5,
        ))
        q_drv = Dot().set_opacity(0)
        q_drv.add_updater(lambda m, dt: q_t.increment_value(dt))
        arm = make_arm(ANGLE_E2)

        dg3 = ValueTracker(-19.0)
        ball_x = ValueTracker(SLOT_X[1])
        ball = always_redraw(lambda: Dot([ball_x.get_value(), ledger_y(dg3.get_value()) + 0.14, 0], radius=0.14, color=WHITE, stroke_color=TEXT, stroke_width=1.5))

        self.add(cpx, led, slots, order_tag, a1, s1, l1, a2, s2, l2, nadh, acoa, spring, q_drv, arm, ball)

        self.at("carbon dioxide leaves")
        co2 = boxed_label("CO2", GREY, size=24, pad=0.20, fill_opacity=0.35).move_to([-5.60, 2.30, 0])
        live_bar3 = always_redraw(lambda: ledger_bar(SLOT_X[2], ledger_y(-19.0), ledger_y(min(dg3.get_value(), -20.2)), GREY))
        self.add(live_bar3)
        self.play(FadeIn(co2, shift=UP * 0.15), ball_x.animate.set_value(SLOT_X[2]), run_time=0.7)
        self.play(
            co2.animate.shift(UP * 1.05).set_opacity(0.0),
            dg3.animate.set_value(DG_TOTAL),
            run_time=2.5, rate_func=smooth,
        )
        self.remove(co2)

        shelf3 = Line([SLOT_X[2] - 0.40, ledger_y(DG_TOTAL), 0], [SLOT_X[2] + 0.40, ledger_y(DG_TOTAL), 0], color=GREY, stroke_width=4)
        lab3 = T("lose CO2\n~ -14", size=24, color=TEXT, line_spacing=0.85).move_to([SLOT_X[2], ledger_y(-41.0), 0])
        self.play(Create(shelf3), FadeIn(lab3), run_time=0.8)

        self.at("found by difference")
        diff_tag = T("by difference,\napprox.", size=22, color=TEXT, line_spacing=0.85).move_to([SLOT_X[2], ledger_y(-53.5), 0])
        diff_span = DashedLine([SLOT_X[1] + 0.45, ledger_y(-19.0), 0], [SLOT_X[2] - 0.45, ledger_y(-19.0), 0], color=GREY, stroke_width=2.5)
        self.play(FadeIn(diff_tag), Create(diff_span), run_time=1.8)
        self.play(FadeOut(diff_span), run_time=0.6)

        # Running sum at top
        self.at("Add them up")
        sum_pos = [3.05, 3.25, 0]
        s_a = M("-50", size=28, color=ORANGE).move_to(sum_pos)
        self.play(swap(order_tag, s_a, run_time=0.65), Indicate(a1, scale_factor=1.08, color=ORANGE))

        self.at("plus 31")
        s_b = M("-50 + 31", size=28, color=TEXT).move_to(sum_pos)
        self.play(swap(s_a, s_b, run_time=0.55), Indicate(live_bar2 if False else a2, scale_factor=1.08, color=GREEN))

        self.at("minus 14")
        s_c = M("-50 + 31 - 14", size=28, color=TEXT).move_to(sum_pos)
        self.play(swap(s_b, s_c, run_time=0.65), Indicate(live_bar3, scale_factor=1.08, color=WHITE))

        self.at("33 overall")
        s_d = M("-50 + 31 - 14 = -33", size=28, color=WHITE).move_to(sum_pos)
        brk_all = overall_bracket_group()
        self.play(swap(s_c, s_d, run_time=0.55), FadeIn(brk_all), run_time=1.0)
        self.finish()


class S06Idea(SpokenScene):
    def construct(self):
        cpx = build_complex(opacity=0.55)
        led = build_ledger(include_ball=False)
        slots = slot_bases()
        sum_txt = M("-50 + 31 - 14 = -33", size=28, color=WHITE).move_to([3.05, 3.25, 0])
        entries = add_three_ledger_entries(show_labels=True)
        a1, _, a2, _, a3, _, l1, l2, l3 = entries
        l3.move_to([SLOT_X[2], ledger_y(-41.0), 0])
        diff_tag = T("by difference,\napprox.", size=22, color=TEXT, line_spacing=0.85).move_to([SLOT_X[2], ledger_y(-53.5), 0])
        brk_all = overall_bracket_group()
        ball = Dot([SLOT_X[2], ledger_y(DG_TOTAL) + 0.14, 0], radius=0.14, color=WHITE, stroke_color=TEXT, stroke_width=1.5)

        nadh = chip("NADH", ORANGE, size=24, pad=0.20, fill_opacity=0.26).move_to(NADH_POS)
        acoa = chip("acetyl-CoA", GREEN, size=22, pad=0.18, fill_opacity=0.26).move_to(ACOA_POS)
        spr_anchor = acoa.get_top() + UP * 0.14
        q_t = ValueTracker(0.0)
        spring = always_redraw(lambda: make_spring(
            spr_anchor + LEFT * 0.65,
            spr_anchor + LEFT * 0.65 + RIGHT * (1.30 + 0.10 * np.sin(8.0 * q_t.get_value())),
            turns=7.5, radius=0.15, color=GREEN, stroke_width=4.5,
        ))
        q_drv = Dot().set_opacity(0)
        q_drv.add_updater(lambda m, dt: q_t.increment_value(dt))
        arm = make_arm(ANGLE_E2)

        self.add(cpx, led, slots, sum_txt, entries, diff_tag, brk_all, ball, nadh, acoa, spring, q_drv, arm)

        self.at("The oxidation")
        ox_glow = ledger_bar(SLOT_X[0], ledger_y(0.0), ledger_y(DG_OX), GOLD, bar_w=0.52, fill_opacity=0.55)
        self.play(FadeIn(ox_glow), a2.animate.set_opacity(0.25), a3.animate.set_opacity(0.25), run_time=1.6)
        self.play(FadeOut(ox_glow), run_time=1.0)

        self.at("for the NADH")
        arc_nadh = CurvedArrow([SLOT_X[0] - 0.22, ledger_y(-56.0), 0], nadh.get_right() + RIGHT * 0.15, angle=-0.12, color=ORANGE, stroke_width=5.5)
        self.play(Create(arc_nadh), Indicate(nadh, scale_factor=1.12, color=ORANGE), run_time=1.1)
        self.play(FadeOut(arc_nadh), run_time=0.5)

        self.at("for the thioester")
        arc_thio = CurvedArrow([SLOT_X[0] + 0.25, ledger_y(-35.0), 0], [SLOT_X[1] - 0.25, ledger_y(-35.0), 0], angle=0.35, color=GREEN, stroke_width=5.5)
        arc_thio.layout_ok = True
        thio_glow = ledger_bar(SLOT_X[1], ledger_y(DG_OX), ledger_y(-19.0), GREEN, bar_w=0.52, fill_opacity=0.55)
        self.play(Create(arc_thio), a2.animate.set_opacity(0.90), FadeIn(thio_glow), Indicate(acoa, scale_factor=1.12, color=GREEN), run_time=1.2)
        self.play(FadeOut(arc_thio), FadeOut(thio_glow), run_time=0.5)

        self.at("What is left")
        leftover_seg = ledger_bar(SLOT_X[0], ledger_y(0.0), ledger_y(-19.0), GOLD, bar_w=0.32, fill_opacity=0.95)
        co2_seg = ledger_bar(SLOT_X[2], ledger_y(-19.0), ledger_y(DG_TOTAL), WHITE, bar_w=0.32, fill_opacity=0.95)
        self.play(a3.animate.set_opacity(0.90), FadeIn(leftover_seg), FadeIn(co2_seg), run_time=1.6)

        self.at("makes the gate")
        self.play(
            leftover_seg.animate.move_to([0.72, (ledger_y(0.0) + ledger_y(-19.0)) / 2, 0]),
            co2_seg.animate.move_to([0.72, (ledger_y(-19.0) + ledger_y(DG_TOTAL)) / 2, 0]),
            run_time=1.2,
        )
        one_way = T("leftover + CO2 = one-way", size=26, color=GOLD).move_to([3.05, -3.15, 0])
        self.play(swap(led.ph_tag, one_way, run_time=0.7))
        self.finish()


class S07OneWay(SpokenScene):
    def construct(self):
        cpx = build_complex(opacity=1.0)
        led = build_ledger(include_ball=False, include_ph=False)
        slots = slot_bases()
        entries = add_three_ledger_entries(show_labels=True)
        brk_all = overall_bracket_group()
        ball = Dot([SLOT_X[2], ledger_y(DG_TOTAL) + 0.14, 0], radius=0.14, color=WHITE, stroke_color=TEXT, stroke_width=1.5)
        led_group = VGroup(led, slots, entries, brk_all, ball)

        arm_t = ValueTracker(0.0)
        arm = always_redraw(lambda: make_arm(ANGLE_E3 + 0.45 * np.sin(2.4 * arm_t.get_value())))
        drv = Dot().set_opacity(0)
        drv.add_updater(lambda m, dt: arm_t.increment_value(dt))

        self.add(cpx, led_group, arm, drv)
        self.play(led_group.animate.set_opacity(0.42), run_time=0.7)

        self.at("drop of about")
        _ = K_EQ
        k_val = ValueTracker(1.0)
        k_counter = counter("K ~ {:.0f} × 10⁵ at 37 °C", k_val, at=[-4.2, 3.05, 0], size=28, color=WHITE, mono=False)
        self.play(FadeIn(k_counter), k_val.animate.set_value(4.0), run_time=2.8)

        fwd_arrow = Arrow([-5.90, -1.75, 0], [-2.75, -1.75, 0], buff=0, color=GREEN, stroke_width=11, max_tip_length_to_length_ratio=0.18)
        fwd_lab = T("forward", size=24, color=GREEN).next_to(fwd_arrow, DOWN, buff=0.10)
        bwd_arrow = Arrow([-2.75, -2.55, 0], [-5.90, -2.55, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.14)
        self.play(GrowArrow(fwd_arrow), FadeIn(fwd_lab), GrowArrow(bwd_arrow), run_time=1.3)

        self.at("In practice")
        flow_t = ValueTracker(0.0)
        flow_drv = Dot().set_opacity(0)
        flow_drv.add_updater(lambda m, dt: flow_t.increment_value(dt))
        stream = always_redraw(lambda: make_reaction_stream(flow_t, y_lane=-1.35, x_left=-6.0, x_mid=-4.25, span=1.50))
        self.add(flow_drv, stream)

        self.at("no enzyme runs")
        x_bwd = make_cross(bwd_arrow, pad=0.12)
        tag_anim = T("in animals", size=24, color=TEXT).move_to([-5.35, -3.15, 0])
        self.play(Create(x_bwd), FadeIn(tag_anim), run_time=0.6)

        bounce_chip = chip("acetyl-CoA", GREEN, size=22, pad=0.14, fill_opacity=0.26).move_to([-2.40, -3.22, 0])
        self.play(FadeIn(bounce_chip), run_time=0.25)
        self.play(bounce_chip.animate.move_to([-3.35, -3.22, 0]), run_time=0.45, rate_func=linear)
        self.play(bounce_chip.animate.move_to([-2.45, -3.22, 0]), run_time=0.5, rate_func=rush_from)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        cpx_in = compact_complex_inset(center=(-4.85, 2.50, 0))
        led_in = compact_ledger_inset(center=(4.75, 2.50, 0))
        self.play(FadeIn(cpx_in), FadeIn(led_in), run_time=0.9)

        self.at("Picture two esters")
        o_chip = chip("oxygen ester", CYAN, size=36, pad=0.40, fill_opacity=0.28).move_to([-2.65, -0.55, 0])
        s_chip = chip("thioester", GREEN, size=36, pad=0.40, fill_opacity=0.28).move_to([2.50, -0.55, 0])

        quiv_t = ValueTracker(0.0)
        o_spr = always_redraw(lambda: make_spring(
            o_chip.get_top() + np.array([-1.05, 0.30, 0]),
            o_chip.get_top() + np.array([1.05 + 0.10 * np.sin(7.0 * quiv_t.get_value()), 0.30, 0]),
            turns=7.0, radius=0.20, color=CYAN, stroke_width=4.5,
        ))
        s_spr = always_redraw(lambda: make_spring(
            s_chip.get_top() + np.array([-1.05, 0.30, 0]),
            s_chip.get_top() + np.array([1.05 + 0.10 * np.sin(7.0 * quiv_t.get_value()), 0.30, 0]),
            turns=7.0, radius=0.20, color=GREEN, stroke_width=4.5,
        ))
        q_drv = Dot().set_opacity(0)
        q_drv.add_updater(lambda m, dt: quiv_t.increment_value(dt))
        self.add(q_drv)

        self.play(FadeIn(o_chip), FadeIn(o_spr), run_time=1.8)
        self.at("this one joined")
        self.play(FadeIn(s_chip), FadeIn(s_spr), run_time=1.6)

        self.at("Split each with")
        w_o = VGroup(make_teardrop([-2.65, 1.25, 0], height=0.80, color=WHITE),
                     T("water", size=26, color=WHITE).move_to([-2.65, 2.00, 0]))
        w_s = VGroup(make_teardrop([2.50, 1.25, 0], height=0.80, color=WHITE),
                     T("water", size=26, color=WHITE).move_to([2.50, 2.00, 0]))
        self.play(FadeIn(w_o, shift=DOWN * 0.18), FadeIn(w_s, shift=DOWN * 0.18), run_time=0.9)
        bob(w_o, amp=0.09, speed=2.6, seed=0)
        bob(w_s, amp=0.09, speed=2.6, seed=1.2)

        self.at("Which releases more")
        q_card = question_card("Which releases more?", y=3.18, color=WHITE, size=32, max_w=5.5).move_to([0.0, 3.18, 0])
        self.play(FadeIn(q_card), run_time=0.6)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Which releases more?"
    CARD = {"y": 3.18, "color": WHITE, "max_w": 5.5, "size": 32}
    RING_AT = (5.9, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        cpx_in = compact_complex_inset(center=(-4.85, 2.50, 0))
        led_in = compact_ledger_inset(center=(4.75, 2.50, 0))
        o_chip = chip("oxygen ester", CYAN, size=36, pad=0.40, fill_opacity=0.28).move_to([-2.65, -0.55, 0])
        s_chip = chip("thioester", GREEN, size=36, pad=0.40, fill_opacity=0.28).move_to([2.50, -0.55, 0])

        quiv_t = ValueTracker(0.0)
        o_spr = always_redraw(lambda: make_spring(
            o_chip.get_top() + np.array([-1.05, 0.30, 0]),
            o_chip.get_top() + np.array([1.05 + 0.10 * np.sin(7.0 * quiv_t.get_value()), 0.30, 0]),
            turns=7.0, radius=0.20, color=CYAN, stroke_width=4.5,
        ))
        s_spr = always_redraw(lambda: make_spring(
            s_chip.get_top() + np.array([-1.05, 0.30, 0]),
            s_chip.get_top() + np.array([1.05 + 0.10 * np.sin(7.0 * quiv_t.get_value()), 0.30, 0]),
            turns=7.0, radius=0.20, color=GREEN, stroke_width=4.5,
        ))
        q_drv = Dot().set_opacity(0)
        q_drv.add_updater(lambda m, dt: quiv_t.increment_value(dt))

        w_o = VGroup(make_teardrop([-2.65, 1.25, 0], height=0.80, color=WHITE),
                     T("water", size=26, color=WHITE).move_to([-2.65, 2.00, 0]))
        w_s = VGroup(make_teardrop([2.50, 1.25, 0], height=0.80, color=WHITE),
                     T("water", size=26, color=WHITE).move_to([2.50, 2.00, 0]))
        bob(w_o, amp=0.09, speed=2.6, seed=0)
        bob(w_s, amp=0.09, speed=2.6, seed=1.2)
        return VGroup(cpx_in, led_in, o_chip, s_chip, o_spr, s_spr, q_drv, w_o, w_s)

    def construct(self):
        self.add(self.backdrop())
        q_card = question_card(self.QUESTION, **self.CARD).move_to([0.0, 3.18, 0])
        self.add(q_card)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S10Answer(SpokenScene):
    def construct(self):
        cpx_in = compact_complex_inset(center=(-4.85, 2.50, 0))
        led_in = compact_ledger_inset(center=(4.75, 2.50, 0))
        o_chip = chip("oxygen ester", CYAN, size=32, pad=0.30, fill_opacity=0.26).move_to([-2.4, 0.35, 0])
        s_chip = chip("thioester", GREEN, size=32, pad=0.30, fill_opacity=0.26).move_to([2.4, 0.35, 0])
        o_spr = make_spring(o_chip.get_top() + np.array([-0.85, 0.22, 0]), o_chip.get_top() + np.array([0.85, 0.22, 0]),
                            turns=7.0, radius=0.15, color=CYAN, stroke_width=4.0)
        s_spr = make_spring(s_chip.get_top() + np.array([-0.85, 0.22, 0]), s_chip.get_top() + np.array([0.85, 0.22, 0]),
                            turns=7.0, radius=0.15, color=GREEN, stroke_width=4.0)
        w_o = VGroup(make_teardrop([-2.4, 1.72, 0], height=0.60, color=WHITE), T("water", size=24, color=WHITE).move_to([-2.4, 2.25, 0]))
        w_s = VGroup(make_teardrop([2.4, 1.72, 0], height=0.60, color=WHITE), T("water", size=24, color=WHITE).move_to([2.4, 2.25, 0]))
        q_card = question_card("Which releases more?", y=3.18, color=WHITE, size=32, max_w=5.5).move_to([0.0, 3.18, 0])

        self.add(cpx_in, led_in, o_chip, s_chip, o_spr, s_spr, w_o, w_s, q_card)

        sc_x = -4.60
        sc_y0, sc_y1 = -0.38, -3.18
        scale_y = lambda v: sc_y0 + (v / -35.0) * (sc_y1 - sc_y0)

        self.at("The sulfur one")
        self.play(FadeOut(q_card), Indicate(s_chip, scale_factor=1.10, color=GREEN), run_time=0.8)

        ax = Line([sc_x, sc_y0, 0], [sc_x, sc_y1, 0], color=GREY, stroke_width=3.2)
        z_line = DashedLine([sc_x, sc_y0, 0], [4.0, sc_y0, 0], color=GREY, stroke_width=2.2, dash_length=0.14)
        tks = VGroup()
        tlabs = VGroup()
        for val in range(0, -36, -5):
            yv = scale_y(val)
            tks.add(Line([sc_x - 0.1, yv, 0], [sc_x, yv, 0], color=GREY, stroke_width=2.5))
            if val % 10 == 0 or val == -35:
                tlabs.add(M(f"{val}", size=22, color=TEXT).next_to([sc_x - 0.12, yv, 0], LEFT, buff=0.08))
        sc_unit = T("kJ/mol", size=22, color=TEXT).next_to([sc_x, sc_y0, 0], LEFT, buff=0.55)
        self.play(Create(ax), Create(z_line), Create(tks), FadeIn(tlabs), FadeIn(sc_unit), run_time=0.8)

        self.at("oxygen ester gives")
        e_o = ValueTracker(0.0)
        o_spr_rel = make_spring(o_chip.get_top() + np.array([-1.05, 0.22, 0]), o_chip.get_top() + np.array([1.05, 0.22, 0]),
                                turns=4.0, radius=0.10, color=CYAN, stroke_width=3.5)
        arr_o = always_redraw(lambda: ledger_bar(-2.4, sc_y0, scale_y(min(e_o.get_value(), -1.5)), CYAN, bar_w=0.34))
        self.add(arr_o)
        self.play(
            w_o.animate.move_to(o_chip.get_top() + UP * 0.2).set_opacity(0),
            ReplacementTransform(o_spr, o_spr_rel),
            e_o.animate.set_value(DG_O_ESTER),
            run_time=1.8,
        )
        self.remove(w_o)
        lab_o = T("about -21", size=26, color=CYAN).next_to([-2.4, scale_y(DG_O_ESTER), 0], LEFT, buff=0.30)
        self.play(FadeIn(lab_o), run_time=0.5)

        self.at("thioester gives")
        e_s = ValueTracker(0.0)
        s_spr_rel = make_spring(s_chip.get_top() + np.array([-1.05, 0.22, 0]), s_chip.get_top() + np.array([1.05, 0.22, 0]),
                                turns=4.0, radius=0.10, color=GREEN, stroke_width=3.5)
        arr_s = always_redraw(lambda: ledger_bar(2.4, sc_y0, scale_y(min(e_s.get_value(), -1.5)), GREEN, bar_w=0.34))
        self.add(arr_s)
        self.play(
            w_s.animate.move_to(s_chip.get_top() + UP * 0.2).set_opacity(0),
            ReplacementTransform(s_spr, s_spr_rel),
            e_s.animate.set_value(DG_S_ESTER),
            run_time=1.8,
        )
        self.remove(w_s)
        lab_s = T("about -31", size=26, color=GREEN).move_to([1.25, scale_y(-21.0), 0])
        self.play(FadeIn(lab_s), run_time=0.45)

        self.at("matching ATP's")
        y_atp = scale_y(DG_ATP)
        atp_line = DashedLine([sc_x, y_atp, 0], [3.9, y_atp, 0], color=PURPLE, stroke_width=3.5, dash_length=0.16)
        atp_lab = T("ATP ~ -30.5", size=24, color=PURPLE).next_to([3.9, y_atp, 0], RIGHT, buff=0.16)
        self.play(Create(atp_line), FadeIn(atp_lab), run_time=1.2)

        self.at("same 31")
        self.play(led_in.animate.scale(1.18).shift(UP * 0.12 + LEFT * 0.15), run_time=0.6)
        self.play(
            Indicate(led_in.green_arrow, scale_factor=1.25, color=GOLD),
            Indicate(arr_s, scale_factor=1.12, color=GOLD),
            run_time=1.6,
        )
        self.finish()


class S11Why(SpokenScene):
    def construct(self):
        tag_sch = scope_tag("schematic")
        self.add(tag_sch)

        myth = T("stored in the bond?", size=38, color=WHITE).move_to([0.0, 0.5, 0])
        self.play(FadeIn(myth), run_time=0.6)

        self.at("energy hides in")
        x_myth = make_cross(myth, pad=0.16)
        self.play(Create(x_myth), run_time=0.9)

        self.at("Breaking a bond")
        costs = T("Breaking a bond always costs energy", size=32, color=GOLD).move_to([0.0, -0.75, 0])
        self.play(FadeIn(costs, shift=UP * 0.1), run_time=1.5)

        self.at("Sulfur is larger")
        self.play(FadeOut(myth), FadeOut(x_myth), FadeOut(costs), run_time=0.5)

        co_o = chip("C=O", GREY, size=32, pad=0.28, fill_opacity=0.28).move_to([-4.2, 1.35, 0])
        co_s = chip("C=O", GREY, size=32, pad=0.28, fill_opacity=0.28).move_to([1.4, 1.35, 0])
        o_disc = Circle(radius=0.72, color=CYAN, stroke_width=4.5, fill_color=CYAN, fill_opacity=0.32).next_to(co_o, RIGHT, buff=0.08)
        s_disc = Circle(radius=1.22, color=GREEN, stroke_width=4.5, fill_color=GREEN, fill_opacity=0.28).next_to(co_s, RIGHT, buff=0.08)
        o_lab = T("O", size=34, color=CYAN).move_to(o_disc)
        s_lab = T("S", size=36, color=GREEN).move_to(s_disc)

        glow_t = ValueTracker(0.0)
        glow_drv = Dot().set_opacity(0)
        glow_drv.add_updater(lambda m, dt: glow_t.increment_value(dt))
        self.add(glow_drv)

        o_contact = np.array([(co_o.get_right()[0] + o_disc.get_left()[0]) / 2, 1.35, 0])
        s_contact = np.array([(co_s.get_right()[0] + s_disc.get_left()[0]) / 2, 1.35, 0])
        o_glow = always_redraw(lambda: Circle(
            radius=0.34 + 0.10 * np.sin(4.5 * glow_t.get_value()),
            color=CYAN, stroke_width=0, fill_color=CYAN, fill_opacity=0.55 + 0.25 * np.sin(4.5 * glow_t.get_value()),
        ).move_to(o_contact))
        s_glow = always_redraw(lambda: Circle(
            radius=0.14 + 0.02 * np.sin(4.5 * glow_t.get_value()),
            color=GREEN, stroke_width=0, fill_color=GREEN, fill_opacity=0.20,
        ).move_to(s_contact))

        self.play(FadeIn(co_o), FadeIn(o_disc), FadeIn(o_lab), FadeIn(co_s), FadeIn(s_disc), FadeIn(s_lab), run_time=1.4)
        self.add(o_glow, s_glow)
        self.wait(1.6)

        self.at("little resonance help")
        res_title = T("resonance help (schematic)", size=28, color=TEXT).move_to([0.0, -0.55, 0])
        bar_f = ValueTracker(0.0)
        bar_o = always_redraw(lambda: Rectangle(width=max(0.06, 6.2 * bar_f.get_value()), height=0.50, color=CYAN, stroke_width=3.2, fill_color=CYAN, fill_opacity=0.65).move_to([-2.9 + 3.1 * bar_f.get_value(), -1.30, 0]))
        bar_s = always_redraw(lambda: Rectangle(width=max(0.06, 1.45 * bar_f.get_value()), height=0.50, color=GREEN, stroke_width=3.2, fill_color=GREEN, fill_opacity=0.65).move_to([-2.9 + 0.725 * bar_f.get_value(), -2.05, 0]))
        lab_bo = T("O ester", size=26, color=CYAN).move_to([-4.25, -1.30, 0])
        lab_bs = T("thioester", size=26, color=GREEN).move_to([-4.25, -2.05, 0])
        self.play(FadeIn(res_title), FadeIn(lab_bo), FadeIn(lab_bs), run_time=0.5)
        self.add(bar_o, bar_s)
        self.play(bar_f.animate.set_value(1.0), run_time=1.7)

        self.at("Its products")
        self.play(
            FadeOut(co_o), FadeOut(o_disc), FadeOut(o_lab), FadeOut(o_glow),
            FadeOut(co_s), FadeOut(s_disc), FadeOut(s_lab), FadeOut(s_glow),
            FadeOut(res_title), FadeOut(bar_o), FadeOut(bar_s), FadeOut(lab_bo), FadeOut(lab_bs),
            run_time=0.6,
        )

        cliff_y = lambda x: -0.35 - 1.50 * np.tanh(1.1 * (x + 0.3))
        xs = np.linspace(-5.8, 5.8, 160)
        cliff_pts = [np.array([x, cliff_y(x), 0.0]) for x in xs]
        cliff_curve = VMobject(stroke_color=GREY, stroke_width=5.5, fill_opacity=0)
        cliff_curve.set_points_as_corners(cliff_pts)
        ground_pts = cliff_pts + [np.array([5.8, -3.1, 0.0]), np.array([-5.8, -3.1, 0.0])]
        ground_poly = Polygon(*ground_pts, stroke_width=0, fill_color="#3A4252", fill_opacity=0.45)

        r_b = 0.85
        x_boulder = ValueTracker(-3.2)

        def boulder_mob():
            xb = x_boulder.get_value()
            dx = 0.02
            slope = (cliff_y(xb + dx) - cliff_y(xb - dx)) / (2 * dx)
            n = np.array([-slope, 1.0, 0.0])
            n /= np.linalg.norm(n)
            center = np.array([xb, cliff_y(xb), 0.0]) + r_b * n
            circ = Circle(radius=r_b, color=GREEN, stroke_width=4.5, fill_color=GREEN, fill_opacity=0.35).move_to(center)
            lab = T("thioester", size=24, color=GREEN).move_to(center)
            return VGroup(circ, lab)

        boulder = always_redraw(boulder_mob)
        self.play(FadeIn(ground_poly), Create(cliff_curve), FadeIn(boulder), run_time=1.4)

        self.at("boulder perched")
        self.play(x_boulder.animate.set_value(2.6), run_time=2.0, rate_func=rush_into)

        boulder_final = boulder_mob()
        self.remove(boulder)
        self.add(boulder_final)
        ac_chip = chip("acetate", YELLOW, size=28, pad=0.22, fill_opacity=0.26).move_to([1.95, cliff_y(1.95) + 0.54, 0])
        coa_chip = chip("CoA", PINK, size=28, pad=0.22, fill_opacity=0.26).move_to([4.15, cliff_y(4.15) + 0.54, 0])
        self.play(ReplacementTransform(boulder_final, VGroup(ac_chip, coa_chip)), run_time=0.8)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        cpx = build_complex(opacity=1.0)
        led = build_ledger(include_ball=False, include_ph=False)
        entries = add_three_ledger_entries(show_labels=True)
        a1 = entries[0]
        brk_all = overall_bracket_group()
        ball = Dot([SLOT_X[2], ledger_y(DG_TOTAL) + 0.14, 0], radius=0.14, color=WHITE, stroke_color=TEXT, stroke_width=1.5)
        nadh = chip("NADH", ORANGE, size=24, pad=0.18, fill_opacity=0.26).move_to([-4.75, -1.60, 0])

        fwd_arrow = Arrow([-5.90, -2.58, 0], [-3.40, -2.58, 0], buff=0, color=GREEN, stroke_width=10, max_tip_length_to_length_ratio=0.18)
        bwd_arrow = Arrow([-3.40, -3.14, 0], [-5.90, -3.14, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.14)
        x_bwd = make_cross(bwd_arrow, pad=0.10)

        arm_t = ValueTracker(0.0)
        arm = always_redraw(lambda: make_arm(ANGLE_E3 + 0.40 * np.sin(2.2 * arm_t.get_value())))
        drv = Dot().set_opacity(0)
        drv.add_updater(lambda m, dt: arm_t.increment_value(dt))

        flow_t = ValueTracker(0.0)
        flow_drv = Dot().set_opacity(0)
        flow_drv.add_updater(lambda m, dt: flow_t.increment_value(dt))
        stream = always_redraw(lambda: make_reaction_stream(flow_t, y_lane=-2.18, x_left=-5.95, x_mid=-4.50, span=1.15))

        self.play(
            FadeIn(cpx), FadeIn(led), FadeIn(entries), FadeIn(brk_all), FadeIn(ball),
            FadeIn(nadh), FadeIn(fwd_arrow), FadeIn(bwd_arrow), FadeIn(x_bwd),
            run_time=0.6,
        )
        self.add(arm, drv, flow_drv, stream)

        self.at("no ATP")
        atp = chip("ATP", PURPLE, size=24, pad=0.18, fill_opacity=0.26).move_to([-5.70, 2.80, 0])
        self.play(FadeIn(atp), run_time=0.35)
        self.play(atp.animate.move_to([-5.60, 2.30, 0]), run_time=0.45)
        x_atp = make_cross(atp)
        self.play(Create(x_atp), run_time=0.3)
        self.play(FadeOut(atp), FadeOut(x_atp), run_time=0.55)

        self.at("two carbons one notch")
        ox_glow = ledger_bar(SLOT_X[0], ledger_y(0.0), ledger_y(DG_OX), GOLD, bar_w=0.46, fill_opacity=0.45)
        self.play(FadeIn(ox_glow), run_time=0.8)
        self.play(FadeOut(ox_glow), run_time=0.6)

        self.at("paid for the")
        self.play(Indicate(nadh, scale_factor=1.14, color=ORANGE), run_time=1.3)

        # Tokens placed cleanly at bottom-right below ledger
        tca_tok = boxed_label("citric acid cycle", GREEN, size=24, pad=0.16).move_to([2.00, -3.34, 0])
        fas_tok = boxed_label("fatty-acid synthesis", GREEN, size=24, pad=0.16).move_to([4.92, -3.34, 0])

        self.at("citric acid cycle's")
        acoa1 = chip("acetyl-CoA", GREEN, size=22, pad=0.12, fill_opacity=0.32).move_to(ACOA_POS)
        spr1 = make_spring(acoa1.get_top() + np.array([-0.52, 0.06, 0]), acoa1.get_top() + np.array([0.52, 0.06, 0]),
                           turns=7.0, radius=0.09, color=GREEN, stroke_width=3.5)
        pack1 = VGroup(acoa1, spr1)
        self.play(FadeIn(tca_tok), FadeIn(pack1), run_time=0.45)
        self.play(pack1.animate.move_to([-2.45, -3.15, 0]), run_time=0.65, rate_func=linear)
        self.play(pack1.animate.move_to([-0.55, -3.15, 0]).set_opacity(0), run_time=0.8)
        self.remove(pack1)

        self.at("fatty acid synthesis")
        acoa2 = chip("acetyl-CoA", GREEN, size=22, pad=0.12, fill_opacity=0.32).move_to(ACOA_POS)
        spr2 = make_spring(acoa2.get_top() + np.array([-0.52, 0.06, 0]), acoa2.get_top() + np.array([0.52, 0.06, 0]),
                           turns=7.0, radius=0.09, color=GREEN, stroke_width=3.5)
        pack2 = VGroup(acoa2, spr2)
        self.play(FadeIn(fas_tok), FadeIn(pack2), run_time=0.45)
        self.play(pack2.animate.move_to([-2.45, -3.15, 0]), run_time=0.45, rate_func=linear)
        self.play(pack2.animate.move_to([-0.25, -3.15, 0]), run_time=0.35, rate_func=linear)
        self.play(pack2.animate.move_to([-0.25, -2.72, 0]), run_time=0.30, rate_func=linear)
        self.play(pack2.animate.move_to([4.88, -2.72, 0]).set_opacity(0), run_time=0.85)
        self.remove(pack2)

        self.at("traffic one")
        self.play(Indicate(fwd_arrow, scale_factor=1.08, color=GREEN), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "Oxidation pays for NADH and the thioester; the rest makes it one-way."
