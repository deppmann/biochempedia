"""Wired to the Sun — Calvin Cycle Regulation (Chapter 2)

COLOUR MAP (one colour per concept, carried all film):
- TEAL (#3FB8C0)      : Chloroplast stroma (day) and thylakoid membrane
- NIGHT_BLUE (#183059): Chloroplast stroma at night
- GOLD (#D4A843)      : G3P · 3C sugar product, output tray, sun disc, title rule
- GREEN (#83C167)     : RuBP (5C) carrier & 3-PGA intermediate
- BLUE (#58C4DD)      : CO2 (substrate CO2, and white-ringed activating CO2)
- YELLOW (#F5D547)    : ATP energy blocks & sunlight rays
- NADPH_COL (#F48FB1) : NADPH reducing-power blocks & meter
- PURPLE (#B07FE8)    : Night sugar-burning pathway wheel
- WHITE (#FFFFFF)     : Protons (H+), pH signal (Toggle 1), active Rubisco jaw, open latch halves
- SILVER (#C8D2E0)    : Mg2+ ions & Mg2+ signal (Toggle 2)
- CYAN (#2CE6F5)      : Reduced ferredoxin (from Photosystem I)
- ORANGE (#FF9F43)    : Thioredoxin & thioredoxin signal (Toggle 3)
- RED (#FC6255)       : Closed S-S disulfide latches
- GREY (#8B93A1)      : Unswitched Rubisco clamp, moon disc, schematic tags, off switches

CARRIED WORLD:
A 16:9 chloroplast stroma cross-section: thylakoid membrane on the left, circular Calvin-cycle
conveyor at the centre (Rubisco clamp at top, reduction lane at right, shuffle drum at bottom,
PRK regeneration return at left), G3P output tray at right, ATP/NADPH meters at bottom,
sun/moon disc at top right, and 3-signal control panel at top left.

WHAT CHANGES PER SCENE (computed from lesson stoichiometry & signals):
- s00_link_and_question: Conveyor phase advances (0.72 -> 0.14 rad/s), 3 ATP + 2 NADPH meters fill
  and streams stop as sun_light interpolates 1->0; purple wheel rolls in, converts G3P to NADPH.
- s01_title: Question mark transforms into title over dimmed crawling conveyor and turning purple wheel.
- s02_futile: Conveyor & purple wheel spin fast inside 'what if' loop cycling G3P<->NADPH; then
  conveyor decelerates to 0, wheel exits, sun_light 0->1, and 3 dark switches slide in.
- s03_protons: Camera shifts left to enlarged thylakoid sac; sinusoidal pumps drive proton dots from
  stroma to lumen (stroma thins, lumen crowds) while pH gauge sits at 7 and mini conveyor turns.
- s04_predict: Pumps continue periodic strokes and proton dots cross; gauge needle covered by '?'.
- s05_pause: Predict pause holds question card with pumps stroking, protons crossing, countdown emptying.
- s06_ph_magnesium: Single ValueTracker drives pH needle from 7.0 to 8.0 and lights Toggle 1; Mg2+
  dots flow from lumen to stroma along dashed path and light Toggle 2.
- s07_rubisco_site: Zoom to Rubisco clamp; activating CO2 docks on lysine -> carbamate -> binds Mg2+
  to sharpen working active site.
- s08_two_co2: pH/Mg2+ toggles pulse; docked CO2 becomes 'switch'; plain CO2 + RuBP drift in, enter
  clamp, and split into two moving 3-PGA · 3C blocks while switch CO2 stays put.
- s09_activase: Grey unswitched clamp locks onto RuBP and jitters ('stuck'); Rubisco activase spends
  ATP to pry jaws open and free RuBP onto conveyor while working clamp cycles.
- s10_thioredoxin: Pull back to full world; PSI flashes, cyan ferredoxin moves to spinning reductase
  gear and reduces dim orange thioredoxin into 4 glowing copies over conveyor stations.
- s11_latches: 4 thioredoxin copies open 4 red S-S latches in turn, activating stations; PRK spends
  ATP to release RuBP; Toggle 3 lights orange.
- s12_idea: 3 lines connect sun to all 3 lit toggles ('made by light'); full-speed conveyor streams
  ATP/NADPH, closes Rubisco, drops GOLD G3P blocks into tray.
- s13_dusk: sun_light interpolates 1->0; thioredoxin dulls ('re-oxidized'); 4 S-S latches snap shut
  and stations slump; toggles switch off; conveyor smoothly decelerates to 0.
- s14_return: Full day-night cycle (sun_light 0->1->0) drives toggles, latches, and conveyor speed.
- s15_end: Standard EndCard with the take-home line.
"""

from bp_parts import *

# ------------------------------------------------------------------ Colour Map
NIGHT_BLUE = "#183059"
NADPH_COL = "#F48FB1"
PURPLE = "#B07FE8"
SILVER = "#C8D2E0"
CYAN = "#2CE6F5"
ORANGE = "#FF9F43"

# ------------------------------------------------------------------ Shared Geometry Constants
LOOP_CENTER = np.array([-0.20, 0.10, 0.0])
LOOP_R = 1.85
LANE_INNER = LOOP_R - 0.50   # 1.35
LANE_OUTER = LOOP_R + 0.50   # 2.35
TRAY_POS = np.array([5.35, -1.35, 0.0])
WHEEL_POS = np.array([5.35, 0.95, 0.0])
SUN_DAY_POS = np.array([5.65, 2.95, 0.0])
SUN_NIGHT_POS = np.array([5.65, 2.73, 0.0])
PANEL_POS = np.array([-4.65, 2.75, 0.0])
THYL_POS = np.array([-5.85, -0.15, 0.0])

# Station angles (radians)
ANG_RUBISCO = PI / 2
ANG_GAPDH = -0.15
ANG_FBPASE = -0.95
ANG_SBPASE = -2.20
ANG_PRK = 2.95


def _lerp_color(c1, c2, alpha):
    return interpolate_color(ManimColor(c1), ManimColor(c2), float(np.clip(alpha, 0.0, 1.0)))


def make_stroma(light_tracker=None, initial_light=1.0):
    """Full-frame chloroplast stroma fill (stroke_width=0 so never flagged as panel)."""
    bg = RoundedRectangle(
        corner_radius=0.35, width=13.5, height=7.45,
        stroke_width=0, fill_color=_lerp_color(NIGHT_BLUE, TEAL, initial_light), fill_opacity=0.18
    ).move_to(ORIGIN)
    bg.set_z_index(-10)
    if light_tracker is not None:
        bg.add_updater(
            lambda m: m.set_fill(_lerp_color(NIGHT_BLUE, TEAL, light_tracker.get_value()), opacity=0.18)
        )
    return bg


def make_sun_moon(light_tracker=None, initial_light=1.0):
    """Sun disc at top right that sinks and morphs smoothly into a moon as light_tracker -> 0."""
    def _build(a):
        a = float(np.clip(a, 0.0, 1.0))
        pos = SUN_NIGHT_POS * (1 - a) + SUN_DAY_POS * a
        g = VGroup()
        if a >= 0.45:
            k = (a - 0.45) / 0.55
            disc = Circle(radius=0.34, color=GOLD, fill_color=GOLD, fill_opacity=0.92 * k + 0.15, stroke_width=2.5).move_to(pos)
            g.add(disc)
            for i in range(8):
                ang = i * TAU / 8
                p1 = pos + np.array([np.cos(ang), np.sin(ang), 0]) * 0.42
                p2 = pos + np.array([np.cos(ang), np.sin(ang), 0]) * (0.42 + 0.15 * k)
                g.add(Line(p1, p2, color=YELLOW, stroke_width=3, stroke_opacity=k))
        else:
            k = 1.0 - a / 0.45
            moon = Circle(radius=0.30, color=GREY, fill_color=SILVER, fill_opacity=0.85 * k + 0.15, stroke_width=2).move_to(pos)
            cut = Circle(radius=0.26, color=BG, fill_color=BG, fill_opacity=0.96, stroke_width=0).move_to(pos + np.array([0.13, 0.09, 0]))
            g.add(moon, cut)
        return g

    if light_tracker is not None:
        return always_redraw(lambda: _build(light_tracker.get_value()))
    return _build(initial_light)


def make_thylakoid_bar(pulsing=True):
    """Left-edge thylakoid bar with horizontal label safely below it."""
    bar = RoundedRectangle(
        corner_radius=0.20, width=0.78, height=3.20,
        stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.26
    ).move_to(THYL_POS)
    lbl = T("thylakoid", size=24, color=TEAL).move_to(THYL_POS + DOWN * 1.92)
    g = VGroup(bar, lbl)
    g.bar, g.label = bar, lbl
    if pulsing:
        bar._pt = 0.0
        def _p(m, dt):
            m._pt += dt
            m.set_stroke(width=3.5 + 1.8 * np.sin(4.2 * m._pt))
        bar.add_updater(_p)
    return g


def make_control_panel(states=(0, 0, 0)):
    """Top-left 3-switch control panel."""
    names_on = [("pH", WHITE), ("Mg2+", SILVER), ("thioredoxin", ORANGE)]
    names_off = [("1", GREY), ("2", GREY), ("3", GREY)]

    box = RoundedRectangle(
        corner_radius=0.16, width=2.95, height=1.68,
        stroke_color=TEAL, stroke_width=2.5, fill_color=BG, fill_opacity=0.92
    ).move_to(PANEL_POS)

    rows = VGroup()
    row_objs = []
    ys = [PANEL_POS[1] + 0.48, PANEL_POS[1], PANEL_POS[1] - 0.48]
    left_x = PANEL_POS[0] - 1.25
    for i, y in enumerate(ys):
        on = bool(states[i])
        txt, col = names_on[i] if on else names_off[i]
        pill = RoundedRectangle(
            corner_radius=0.13, width=0.52, height=0.26,
            stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.28 if on else 0.06
        ).move_to([left_x + 0.26, y, 0])
        knob_x = pill.get_right()[0] - 0.13 if on else pill.get_left()[0] + 0.13
        knob = Dot(radius=0.09, color=col if on else GREY).move_to([knob_x, y, 0])
        lbl = T(txt, size=24, color=col if on else TEXT).move_to([left_x + 0.68, y, 0], aligned_edge=LEFT)
        row = VGroup(pill, knob, lbl)
        row.pill, row.knob, row.lbl, row.idx = pill, knob, lbl, i
        rows.add(row)
        row_objs.append(row)

    panel = VGroup(box, rows)
    panel.box = box
    panel.rows = row_objs
    return panel


def flip_toggle_anim(panel, idx, on=True):
    """Return animation flipping switch idx on or off with swap() on its label."""
    names_on = [("pH", WHITE), ("Mg2+", SILVER), ("thioredoxin", ORANGE)]
    names_off = [("1", GREY), ("2", GREY), ("3", GREY)]
    row = panel.rows[idx]
    txt, col = names_on[idx] if on else names_off[idx]
    target_x = row.pill.get_right()[0] - 0.13 if on else row.pill.get_left()[0] + 0.13
    new_lbl = T(txt, size=24, color=col if on else TEXT).move_to(
        [row.pill.get_right()[0] + 0.16, row.pill.get_center()[1], 0], aligned_edge=LEFT
    )
    anim = AnimationGroup(
        row.pill.animate.set_stroke(col).set_fill(col, opacity=0.28 if on else 0.06),
        row.knob.animate.move_to([target_x, row.pill.get_center()[1], 0]).set_color(col if on else GREY),
        swap(row.lbl, new_lbl, run_time=0.50),
    )
    row.lbl = new_lbl
    return anim


def _loop_pt(angle, r=LOOP_R, center=LOOP_CENTER):
    return np.array(center, dtype=float) + np.array([r * np.cos(angle), r * np.sin(angle), 0.0])


def make_rubisco_clamp_mini(active=True):
    """Schematic two-jaw Rubisco clamp positioned cleanly around top of conveyor."""
    c = _loop_pt(ANG_RUBISCO)
    col = WHITE if active else GREY
    top_jaw = Arc(radius=0.38, start_angle=0.20, angle=PI - 0.40, arc_center=c + UP * 0.36, stroke_color=col, stroke_width=5)
    bot_jaw = Arc(radius=0.38, start_angle=PI + 0.20, angle=PI - 0.40, arc_center=c + DOWN * 0.36, stroke_color=col, stroke_width=5)
    tag = T("Rubisco", size=24, color=col).next_to(top_jaw, UP, buff=0.14)
    g = VGroup(top_jaw, bot_jaw, tag)
    g.jaws = VGroup(top_jaw, bot_jaw)
    g.label = tag
    return g


def make_conveyor(phase_tracker=None, active_stations=True, show_latches=False, latch_open=False,
                  show_rubisco=True, show_labels=True, center=LOOP_CENTER, scale_f=1.0):
    """Central Calvin-cycle circular conveyor parameterized by center & scale_f."""
    c = np.array(center, dtype=float)
    r_mid = LOOP_R * scale_f
    r_in = LANE_INNER * scale_f
    r_out = LANE_OUTER * scale_f

    outer = Circle(radius=r_out, color=TEAL, stroke_width=3.5 * max(scale_f, 0.7)).move_to(c)
    inner = Circle(radius=r_in, color=TEAL, stroke_width=3.5 * max(scale_f, 0.7)).move_to(c)
    track_fill = Annulus(inner_radius=r_in, outer_radius=r_out, color=TEAL, fill_opacity=0.20, stroke_width=0).move_to(c)

    chevrons = VGroup()
    for a in [0.65, -0.75, -2.55, 2.05]:
        p = _loop_pt(a, r=r_in - 0.22 * scale_f, center=c)
        tang = np.array([np.sin(a), -np.cos(a), 0.0]) * scale_f
        rad = np.array([np.cos(a), np.sin(a), 0.0]) * scale_f
        chevrons.add(VGroup(
            Line(p - tang * 0.12 + rad * 0.09, p + tang * 0.10, color=TEAL, stroke_width=2.8),
            Line(p - tang * 0.12 - rad * 0.09, p + tang * 0.10, color=TEAL, stroke_width=2.8),
        ))

    def _carriers(ph):
        grp = VGroup()
        for k in range(3):
            a = ph - k * TAU / 3
            p = _loop_pt(a, r=r_mid, center=c)
            if show_labels:
                pill = RoundedRectangle(corner_radius=0.12, width=0.56, height=0.36, stroke_color=GREEN, stroke_width=2.2, fill_color=BG, fill_opacity=0.94).move_to(p)
                txt = M("5C", size=22, color=GREEN).move_to(pill)
                grp.add(VGroup(pill, txt))
            else:
                pill = RoundedRectangle(corner_radius=0.08, width=0.34, height=0.20, stroke_color=GREEN, stroke_width=2.2, fill_color=GREEN, fill_opacity=0.55).move_to(p)
                grp.add(pill)
        return grp

    if phase_tracker is not None:
        carriers = always_redraw(lambda: _carriers(phase_tracker.get_value()))
    else:
        carriers = _carriers(0.9)

    g = VGroup(track_fill, outer, inner, chevrons, carriers)
    g.outer, g.inner, g.carriers = outer, inner, carriers

    if show_rubisco:
        clamp = make_rubisco_clamp_mini(active=active_stations)
        g.add(clamp)
        g.clamp = clamp

    if show_latches:
        r_st = LANE_OUTER + 0.46
        st_defs = [
            ("G3P DH", ANG_GAPDH, RIGHT, 0.22),
            ("FBPase", ANG_FBPASE, DOWN, 0.20),
            ("SBPase", ANG_SBPASE, DOWN, 0.20),
            ("PRK", ANG_PRK, DOWN, 0.22),
        ]
        stations = VGroup()
        latches = []
        for name, ang, ldir, buff in st_defs:
            pt = _loop_pt(ang, r=r_st, center=c)
            rim_pt = _loop_pt(ang, r=LANE_OUTER, center=c)
            tick_end = _loop_pt(ang, r=LANE_OUTER + 0.16, center=c)
            tick = Line(rim_pt, tick_end, color=TEAL, stroke_width=2.5)
            st_col = TEXT if active_stations else GREY
            node = RoundedRectangle(
                corner_radius=0.10, width=0.38, height=0.38,
                stroke_color=st_col, stroke_width=3 if active_stations else 2,
                fill_color=TEAL if active_stations else BG, fill_opacity=0.35 if active_stations else 0.90
            ).move_to(pt)
            latch = make_latch_icon(pt, open_state=latch_open)
            lbl = T(name, size=24, color=st_col).next_to(latch, ldir, buff=buff)
            stations.add(VGroup(tick, node, latch, lbl))
            latches.append((node, lbl, latch, pt))
        g.add(stations)
        g.stations = latches

    return g


def make_latch_icon(pos, open_state=False):
    """Plain padlock-like S-S disulfide latch icon with generous box padding."""
    p = np.array(pos, dtype=float)
    if not open_state:
        body = boxed_label("S-S", RED, size=22, pad=0.10, fill_opacity=0.95)
        body.box.set_fill(BG, opacity=0.96)
        body.move_to(p)
        shackle = Arc(radius=0.13, start_angle=0, angle=PI, arc_center=body.get_top() + DOWN * 0.01, stroke_color=RED, stroke_width=3)
        return VGroup(shackle, body)
    else:
        left_h = RoundedRectangle(corner_radius=0.05, width=0.22, height=0.24, stroke_color=WHITE, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to(p + LEFT * 0.24)
        right_h = RoundedRectangle(corner_radius=0.05, width=0.22, height=0.24, stroke_color=WHITE, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to(p + RIGHT * 0.24)
        return VGroup(left_h, right_h)


def make_g3p_block():
    return boxed_label("G3P · 3C", GOLD, size=22, pad=0.12, fill_opacity=0.18)


def make_atp_block():
    return boxed_label("ATP", YELLOW, size=22, pad=0.11, fill_opacity=0.18)


def make_nadph_block():
    return boxed_label("NADPH", NADPH_COL, size=22, pad=0.11, fill_opacity=0.18)


def make_trx_token(text="Trx", color=ORANGE, size=22, pad=0.10):
    tok = boxed_label(text, color, size=size, pad=pad, fill_opacity=0.14)
    tok.box.set_fill(BG, opacity=0.92)
    return tok


def make_co2_counter(ringed=False, text="CO2"):
    """Generously padded CO2 counter circle (never scaled below 22 pt)."""
    c = Circle(radius=0.36, stroke_color=WHITE if ringed else BLUE, stroke_width=4 if ringed else 2.5, fill_color=BLUE, fill_opacity=0.24)
    t = M(text, size=22, color=TEXT).move_to(c)
    g = VGroup(c, t)
    g.circle, g.txt = c, t
    return g


def make_output_tray(count=2):
    """GOLD output tray at right holding stacked G3P · 3C blocks."""
    tray = VGroup(
        Line(TRAY_POS + np.array([-0.92, 0.42, 0]), TRAY_POS + np.array([-0.92, -0.44, 0]), color=GOLD, stroke_width=4),
        Line(TRAY_POS + np.array([-0.92, -0.44, 0]), TRAY_POS + np.array([0.92, -0.44, 0]), color=GOLD, stroke_width=4),
        Line(TRAY_POS + np.array([0.92, -0.44, 0]), TRAY_POS + np.array([0.92, 0.42, 0]), color=GOLD, stroke_width=4),
    )
    lbl = T("G3P tray", size=24, color=GOLD).next_to(tray, DOWN, buff=0.14)
    blocks = VGroup()
    for i in range(count):
        b = make_g3p_block().move_to(TRAY_POS + UP * (-0.16 + i * 0.46))
        blocks.add(b)
    g = VGroup(tray, lbl, blocks)
    g.tray, g.label, g.blocks = tray, lbl, blocks
    return g


def make_purple_wheel(rot_tracker=None):
    """Night sugar-burning pathway wheel at right."""
    wheel = Circle(radius=0.64, color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.18).move_to(WHEEL_POS)
    spokes = VGroup(*[
        Line(WHEEL_POS + np.array([np.cos(a), np.sin(a), 0]) * 0.18,
             WHEEL_POS + np.array([np.cos(a), np.sin(a), 0]) * 0.60,
             color=PURPLE, stroke_width=3)
        for a in np.linspace(0, TAU, 6, endpoint=False)
    ])
    hub = Dot(radius=0.11, color=PURPLE).move_to(WHEEL_POS)
    if rot_tracker is not None:
        spokes.add_updater(lambda m: m.become(VGroup(*[
            Line(wheel.get_center() + np.array([np.cos(a + rot_tracker.get_value()), np.sin(a + rot_tracker.get_value()), 0]) * 0.18,
                 wheel.get_center() + np.array([np.cos(a + rot_tracker.get_value()), np.sin(a + rot_tracker.get_value()), 0]) * 0.60,
                 color=PURPLE, stroke_width=3)
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ])))
    lbl = T("burns sugar", size=24, color=PURPLE).next_to(wheel, UP, buff=0.14)
    g = VGroup(wheel, spokes, hub, lbl)
    g.wheel, g.spokes, g.label = wheel, spokes, lbl
    return g


def make_meters(atp_tracker, nadph_tracker):
    """Bottom ATP (0..3) and NADPH (0..2) bar meters, spaced clear of per-CO2 tag."""
    def _bar(tracker, max_v, title, col, cx):
        bg_bar = RoundedRectangle(corner_radius=0.10, width=2.15, height=0.28, stroke_color=col, stroke_width=2, fill_color=BG, fill_opacity=0.9).move_to([cx, -3.18, 0])
        fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.08,
            width=max(0.08, 2.06 * float(np.clip(tracker.get_value() / max_v, 0.0, 1.0))),
            height=0.20, stroke_width=0, fill_color=col, fill_opacity=0.85
        ).align_to(bg_bar.get_left() + RIGHT * 0.04, LEFT).set_y(-3.18))
        lbl = always_redraw(lambda: M(f"{title}: {tracker.get_value():.0f}", size=24, color=col).move_to([cx, -2.78, 0]))
        return VGroup(bg_bar, fill, lbl)

    return VGroup(_bar(atp_tracker, 3.0, "ATP", YELLOW, -0.35), _bar(nadph_tracker, 2.0, "NADPH", NADPH_COL, 2.45))


# ------------------------------------------------------------------ Thylakoid Sac & Gauge (s03 - s06)
SAC_POS = np.array([-3.15, -0.60, 0.0])
SAC_W = 4.15
SAC_H = 4.10
GAUGE_X = 0.65
GAUGE_Y0 = -1.75
GAUGE_Y1 = 0.70


def make_thylakoid_sac(pump_phase=None, ph_tracker=None, covered=False, mini_phase=None):
    """Enlarged thylakoid sac (~60% frame height) + pumps + vertical pH gauge."""
    sac = RoundedRectangle(
        corner_radius=0.92, width=SAC_W, height=SAC_H,
        stroke_color=TEAL, stroke_width=4.5, fill_color=TEAL, fill_opacity=0.26
    ).move_to(SAC_POS)
    lumen_lbl = T("lumen", size=26, color=TEAL).move_to(SAC_POS + UP * 1.15)
    stroma_lbl = T("stroma", size=26, color=TEXT).move_to([3.05, 1.75, 0])

    wall_x = SAC_POS[0] + SAC_W / 2
    pumps = VGroup()
    for py in [SAC_POS[1] + 0.55, SAC_POS[1] - 0.75]:
        p_box = RoundedRectangle(corner_radius=0.10, width=0.58, height=0.48, stroke_color=WHITE, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to([wall_x, py, 0])
        arrow = Arrow([wall_x + 0.22, py, 0], [wall_x - 0.22, py, 0], buff=0, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        pumps.add(VGroup(p_box, arrow))

    if pump_phase is not None:
        def _stroke(m):
            s = 0.5 * (1.0 + np.sin(pump_phase.get_value()))
            for p in m:
                p[0].set_stroke(width=2.5 + 3.2 * s).set_fill(TEAL, opacity=0.12 + 0.55 * s)
        pumps.add_updater(_stroke)

    track = Line([GAUGE_X, GAUGE_Y0, 0], [GAUGE_X, GAUGE_Y1, 0], color=GREY, stroke_width=6)
    t7 = Line([GAUGE_X - 0.14, GAUGE_Y0, 0], [GAUGE_X + 0.18, GAUGE_Y0, 0], color=TEXT, stroke_width=3)
    t8 = Line([GAUGE_X - 0.14, GAUGE_Y1, 0], [GAUGE_X + 0.18, GAUGE_Y1, 0], color=TEXT, stroke_width=3)
    l7 = M("7", size=26, color=TEXT).move_to([GAUGE_X + 0.42, GAUGE_Y0, 0])
    l8 = M("8", size=26, color=TEXT).move_to([GAUGE_X + 0.42, GAUGE_Y1, 0])
    g_title = T("stroma pH", size=26, color=TEXT).next_to(track, UP, buff=0.25)
    g_schem = T("schematic", size=22, color=GREY).next_to(track, DOWN, buff=0.28)

    def _needle_y():
        v = 7.0 if ph_tracker is None else float(np.clip(ph_tracker.get_value(), 7.0, 8.0))
        return GAUGE_Y0 + (v - 7.0) * (GAUGE_Y1 - GAUGE_Y0)

    needle = always_redraw(lambda: Polygon(
        [GAUGE_X - 0.42, _needle_y() + 0.12, 0],
        [GAUGE_X - 0.42, _needle_y() - 0.12, 0],
        [GAUGE_X - 0.06, _needle_y(), 0],
        color=WHITE, fill_color=WHITE, fill_opacity=1.0, stroke_width=0
    ))

    gauge = VGroup(track, t7, t8, l7, l8, g_title, g_schem, needle)

    cover = VGroup()
    if covered:
        cbox = RoundedRectangle(
            corner_radius=0.12, width=0.68, height=2.82,
            stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.96
        ).move_to([GAUGE_X - 0.16, (GAUGE_Y0 + GAUGE_Y1) / 2, 0])
        cq = M("?", size=40, color=WHITE).move_to(cbox)
        cover.add(cbox, cq)

    mini_conv = make_conveyor(
        phase_tracker=mini_phase, show_rubisco=False, show_labels=False,
        center=np.array([5.25, -0.75, 0.0]), scale_f=0.44
    )

    rays = VGroup(*[
        DashedLine(SUN_DAY_POS + LEFT * 0.48 + DOWN * (0.05 + i * 0.13), SAC_POS + UP * 1.95 + RIGHT * (0.1 + i * 0.35),
                   color=YELLOW, stroke_width=2.5, dash_length=0.18).set_opacity(0.68)
        for i in range(3)
    ])

    g = VGroup(sac, lumen_lbl, stroma_lbl, pumps, gauge, cover, mini_conv, rays)
    g.sac, g.lumen_lbl, g.stroma_lbl, g.pumps, g.gauge, g.cover, g.mini_conv, g.rays = (
        sac, lumen_lbl, stroma_lbl, pumps, gauge, cover, mini_conv, rays
    )
    return g


def make_proton_field(n_lumen=5, n_stroma=8, seed=7):
    """Fixed-seed protons inside lumen (below 'lumen' label) and in stroma."""
    rng = np.random.default_rng(seed)
    lumen_pts = [
        [rng.uniform(SAC_POS[0] - 1.35, SAC_POS[0] + 1.15), rng.uniform(SAC_POS[1] - 1.45, SAC_POS[1] + 0.60), 0.0]
        for _ in range(n_lumen)
    ]
    stroma_pts = [
        [rng.uniform(1.65, 3.65), rng.uniform(-2.05, 0.85), 0.0]
        for _ in range(n_stroma)
    ]
    return VGroup(*[Dot(p, radius=0.10, color=WHITE) for p in lumen_pts]), VGroup(*[Dot(p, radius=0.10, color=WHITE) for p in stroma_pts])


# ------------------------------------------------------------------ Zoomed Rubisco Jaw (s07 - s09)
JAW_CENTER = np.array([0.45, 0.05, 0.0])


def make_zoomed_rubisco(center=JAW_CENTER, scale_f=1.0, active=False, open_amt=1.0, show_title=True, show_peg_lbl=True):
    """Zoomed Rubisco active-site clamp with substantial protein body fill."""
    c = np.array(center, dtype=float)
    col = WHITE if active else TEAL
    r = 1.92 * scale_f
    gap = (0.24 + 0.26 * open_amt) * scale_f
    sw = 8 if active else 5.5

    body_fill = AnnularSector(
        inner_radius=r * 0.68, outer_radius=r * 1.12,
        start_angle=0.22, angle=TAU - 0.44,
        arc_center=c, color=col, fill_opacity=0.26, stroke_width=0
    )
    r_back = r * 1.15
    y_int = (r_back ** 2 - r ** 2 + gap ** 2) / (2.0 * gap)
    if abs(y_int) < r_back and abs(y_int - gap) < r:
        x_int = -np.sqrt(r_back ** 2 - y_int ** 2)
        theta_b = np.arctan2(y_int, x_int)
        theta_u = np.arctan2(y_int - gap, x_int)
    else:
        theta_b = 0.77 * PI
        theta_u = 0.84 * PI
    upper_jaw = Arc(radius=r, start_angle=0.18, angle=theta_u - 0.18, arc_center=c + UP * gap, stroke_color=col, stroke_width=sw)
    lower_jaw = Arc(radius=r, start_angle=TAU - theta_u, angle=theta_u - 0.18, arc_center=c + DOWN * gap, stroke_color=col, stroke_width=sw)
    back_bridge = Arc(radius=r_back, start_angle=theta_b, angle=2.0 * (PI - theta_b), arc_center=c, stroke_color=col, stroke_width=sw)

    peg_pos = c + np.array([-0.40 * scale_f, -0.58 * scale_f, 0.0])
    peg = RoundedRectangle(
        corner_radius=0.07, width=0.28 * scale_f, height=0.64 * scale_f,
        stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.26
    ).move_to(peg_pos)

    g = VGroup(body_fill, upper_jaw, lower_jaw, back_bridge, peg)
    if show_peg_lbl:
        peg_lbl = T("lysine", size=26, color=TEXT).next_to(peg, DOWN, buff=0.18)
        g.add(peg_lbl)
        g.peg_lbl = peg_lbl
    if show_title:
        title = T("Rubisco", size=30, color=col).next_to(upper_jaw, UP, buff=0.26)
        g.add(title)
        g.title = title

    g.body_fill, g.upper_jaw, g.lower_jaw, g.back_bridge, g.peg = (
        body_fill, upper_jaw, lower_jaw, back_bridge, peg
    )
    g.peg_pos = peg_pos
    g.site_pos = peg_pos + UP * (0.32 * scale_f + 0.40)
    g.mg_pos = g.site_pos + RIGHT * 0.76
    g.cat_pos = c + np.array([1.05 * scale_f, 0.0, 0.0])
    return g


# ================================================================== SCENES

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(1.0)
        omega = ValueTracker(0.72)
        phase = ValueTracker(0.5)
        phase.add_updater(lambda m, dt: m.increment_value(-omega.get_value() * dt))

        atp_t = ValueTracker(0.0)
        nadph_t = ValueTracker(0.0)

        stroma = make_stroma(sun_light, 1.0)
        sun = make_sun_moon(sun_light, 1.0)
        thyl = make_thylakoid_bar(pulsing=True)
        conv = make_conveyor(phase_tracker=phase, active_stations=True)
        tray = make_output_tray(count=1)
        meters = make_meters(atp_t, nadph_t)
        bill_tag = boxed_label("per CO2: 3 ATP + 2 NADPH", GOLD, size=22, pad=0.12).move_to([-4.15, -3.12, 0])

        self.add(stroma, sun, thyl, conv, tray, meters, phase)

        stream_atp = VGroup(make_atp_block(), make_atp_block(), make_atp_block())
        stream_nadph = VGroup(make_nadph_block(), make_nadph_block())
        for i, b in enumerate(stream_atp):
            b.move_to([-4.65, 1.15 - i * 0.55, 0])
        for i, b in enumerate(stream_nadph):
            b.move_to([-4.65, -0.60 - i * 0.55, 0])
        co2 = make_co2_counter().move_to([2.05, 2.65, 0])
        g3p_drop = make_g3p_block().move_to([3.20, -0.55, 0])

        self.play(FadeIn(bill_tag), FadeIn(co2), run_time=0.55)
        self.play(
            co2.animate.move_to(_loop_pt(ANG_RUBISCO) + RIGHT * 0.35),
            atp_t.animate.set_value(3.0),
            nadph_t.animate.set_value(2.0),
            LaggedStart(
                *[b.animate.move_to([-3.05, 1.15 - i * 0.55, 0]).set_opacity(0) for i, b in enumerate(stream_atp)],
                lag_ratio=0.35, run_time=2.8
            ),
            LaggedStart(
                *[b.animate.move_to([-3.05, -0.60 - i * 0.55, 0]).set_opacity(0) for i, b in enumerate(stream_nadph)],
                lag_ratio=0.45, run_time=2.5
            ),
            run_time=3.3,
        )
        self.remove(co2)

        self.at("light reactions pay")
        self.play(FadeIn(g3p_drop), run_time=0.35)
        self.play(g3p_drop.animate.move_to(TRAY_POS + UP * 0.30), run_time=1.2)

        self.at("the sun sets")
        thyl.bar.clear_updaters()
        self.play(
            sun_light.animate.set_value(0.0),
            omega.animate.set_value(0.14),
            FadeOut(bill_tag),
            run_time=2.0,
        )

        self.at("burning sugar")
        rot = ValueTracker(0.0)
        rot.add_updater(lambda m, dt: m.increment_value(0.9 * dt))
        wheel = make_purple_wheel(rot).shift(RIGHT * 2.5)
        self.add(rot, wheel)
        self.play(wheel.animate.shift(LEFT * 2.5), run_time=0.9)

        nadph_night = make_nadph_block().move_to(WHEEL_POS + LEFT * 1.25)
        self.play(
            g3p_drop.animate.move_to(WHEEL_POS + DOWN * 0.85).set_opacity(0),
            FadeIn(nadph_night),
            run_time=1.0,
        )

        self.at("why doesn't")
        qmark = M("?", size=120, color=WHITE).move_to(LOOP_CENTER)
        self.play(
            nadph_night.animate.move_to(np.array([3.35, 0.55, 0.0])),
            GrowFromCenter(qmark),
            run_time=1.2,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        phase = ValueTracker(0.2)
        phase.add_updater(lambda m, dt: m.increment_value(-0.14 * dt))
        rot = ValueTracker(0.0)
        rot.add_updater(lambda m, dt: m.increment_value(0.8 * dt))

        stroma = make_stroma(initial_light=0.0)
        sun = make_sun_moon(initial_light=0.0)
        thyl = make_thylakoid_bar(pulsing=False)
        conv = make_conveyor(phase_tracker=phase, active_stations=True)
        tray = make_output_tray(count=1)
        wheel = make_purple_wheel(rot)
        nadph_night = make_nadph_block().move_to(np.array([3.35, 0.55, 0.0]))
        qmark = M("?", size=120, color=WHITE).move_to(LOOP_CENTER)
        atp_t, nadph_t = ValueTracker(3.0), ValueTracker(2.0)
        meters = make_meters(atp_t, nadph_t)

        self.add(stroma, sun, thyl, conv, tray, wheel, meters, nadph_night, qmark, phase, rot)

        backing = RoundedRectangle(
            corner_radius=0.22, width=7.2, height=1.75, stroke_width=0, fill_color=BG, fill_opacity=0.92
        ).move_to(LOOP_CENTER)
        title = T("Wired to the Sun", size=54, font=TITLE_FONT, color=TEXT).move_to(LOOP_CENTER + UP * 0.22)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.22)
        title_grp = VGroup(backing, title, rule)

        self.play(
            FadeOut(qmark, run_time=0.20),
            FadeOut(conv.carriers, run_time=0.20),
            FadeOut(nadph_night, run_time=0.20),
            conv.outer.animate(run_time=0.25).set_stroke(opacity=0.28),
            conv.inner.animate(run_time=0.25).set_stroke(opacity=0.28),
            FadeIn(backing, run_time=0.25),
            Write(title, run_time=0.45),
            GrowFromCenter(rule, run_time=0.45),
        )
        self.wait(0.70)
        self.play(
            FadeOut(title_grp),
            conv.outer.animate.set_stroke(opacity=1.0),
            conv.inner.animate.set_stroke(opacity=1.0),
            FadeIn(conv.carriers),
            FadeIn(nadph_night),
            run_time=0.45,
        )
        self.finish()


class S02Futile(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(0.0)
        omega = ValueTracker(0.14)
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(-omega.get_value() * dt))
        rot = ValueTracker(0.0)
        rot.add_updater(lambda m, dt: m.increment_value(1.2 * dt))

        stroma = make_stroma(sun_light, 0.0)
        sun = make_sun_moon(sun_light, 0.0)
        thyl = make_thylakoid_bar(pulsing=False)
        conv = make_conveyor(phase_tracker=phase, active_stations=True)
        tray = make_output_tray(count=1)
        wheel = make_purple_wheel(rot)
        atp_t, nadph_t = ValueTracker(3.0), ValueTracker(2.0)
        meters = make_meters(atp_t, nadph_t)
        nadph_blk = make_nadph_block().move_to(np.array([3.35, 0.55, 0.0]))

        self.add(stroma, sun, thyl, conv, tray, wheel, meters, nadph_blk, phase, rot)

        self.at("Suppose it did")
        what_if_rect = DashedVMobject(
            RoundedRectangle(corner_radius=0.28, width=10.35, height=5.80, stroke_color=WHITE, stroke_width=3),
            num_dashes=68
        ).move_to([1.35, 0.45, 0])
        what_if_lbl = boxed_label("what if", WHITE, size=24, pad=0.12, fill_opacity=0.25).move_to([-2.95, 2.90, 0])
        what_if_lbl.box.set_fill(BG, opacity=0.92)
        self.play(Create(what_if_rect), FadeIn(what_if_lbl), omega.animate.set_value(0.85), run_time=0.85)

        self.at("build sugar")
        g3p_loop = make_g3p_block().move_to([3.10, -1.25, 0])
        self.play(FadeIn(g3p_loop), run_time=0.25)
        for _ in range(2):
            self.play(
                g3p_loop.animate.move_to([3.95, 0.05, 0]),
                nadph_blk.animate.move_to([3.10, 0.78, 0]),
                run_time=1.30, rate_func=linear,
            )
            g3p_loop.move_to([3.10, -1.25, 0])
            nadph_blk.move_to([3.95, 0.78, 0])

        self.at("futile cycle")
        futile_arc = Arc(radius=0.62, start_angle=0.25, angle=1.55 * PI, arc_center=[3.50, -0.10, 0], color=RED, stroke_width=4)
        futile_tip = Triangle(color=RED, fill_color=RED, fill_opacity=1.0).scale(0.12).move_to(futile_arc.get_end()).rotate(0.4)
        futile_lbl = boxed_label("futile cycle", RED, size=24, pad=0.12).move_to([3.50, -1.95, 0])
        futile_lbl.box.set_fill(BG, opacity=0.95)
        self.play(Create(futile_arc), FadeIn(futile_tip), FadeIn(futile_lbl), run_time=1.0)

        self.at("light itself flips")
        panel = make_control_panel((0, 0, 0)).shift(LEFT * 3.8)
        self.add(panel)
        self.play(
            FadeOut(what_if_rect), FadeOut(what_if_lbl),
            FadeOut(futile_arc), FadeOut(futile_tip), FadeOut(futile_lbl),
            FadeOut(g3p_loop), FadeOut(nadph_blk),
            FadeOut(wheel, shift=RIGHT * 0.7),
            omega.animate.set_value(0.0),
            sun_light.animate.set_value(1.0),
            panel.animate.shift(RIGHT * 3.8),
            run_time=2.1,
        )

        self.at("three signals")
        self.play(Indicate(panel.box, color=TEAL, scale_factor=1.03), run_time=0.8)
        self.finish()


class S03Protons(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(1.0)
        stroma = make_stroma(sun_light, 1.0)
        sun = make_sun_moon(sun_light, 1.0)
        panel = make_control_panel((0, 0, 0))
        thyl = make_thylakoid_bar(pulsing=False)
        conv = make_conveyor(active_stations=True)
        tray = make_output_tray(count=1)
        self.add(stroma, sun, panel, thyl, conv, tray)

        self.at("Signal 1")
        pump_phase = ValueTracker(0.0)
        mini_phase = ValueTracker(0.4)
        ph_t = ValueTracker(7.0)
        sac_grp = make_thylakoid_sac(pump_phase=pump_phase, ph_tracker=ph_t, covered=False, mini_phase=mini_phase)
        lumen_dots, stroma_dots = make_proton_field(n_lumen=4, n_stroma=10, seed=7)
        protons_lbl = T("protons", size=24, color=WHITE).move_to([2.65, -2.55, 0])

        self.play(
            ReplacementTransform(thyl.bar, sac_grp.sac),
            FadeOut(thyl.label),
            FadeOut(tray),
            FadeOut(conv),
            FadeIn(sac_grp.mini_conv),
            FadeIn(sac_grp.lumen_lbl), FadeIn(sac_grp.stroma_lbl),
            FadeIn(sac_grp.pumps), FadeIn(sac_grp.gauge), FadeIn(sac_grp.rays),
            FadeIn(lumen_dots), FadeIn(stroma_dots), FadeIn(protons_lbl),
            run_time=1.6,
        )
        pump_phase.add_updater(lambda m, dt: m.increment_value(5.0 * dt))
        mini_phase.add_updater(lambda m, dt: m.increment_value(-0.75 * dt))
        self.add(pump_phase, mini_phase)

        self.at("pumps protons")
        wall_x = SAC_POS[0] + SAC_W / 2
        pump_ys = [SAC_POS[1] + 0.55, SAC_POS[1] - 0.75]
        rng = np.random.default_rng(17)
        # Pump 2 protons simultaneously per beat so proton crossing is unmistakable
        for k in range(3):
            d1, d2 = stroma_dots[0], stroma_dots[1]
            stroma_dots.remove(d1, d2)
            lumen_dots.add(d1, d2)
            dest1 = np.array([rng.uniform(SAC_POS[0] - 1.2, SAC_POS[0] + 1.0), rng.uniform(SAC_POS[1] - 0.2, SAC_POS[1] + 0.55), 0.0])
            dest2 = np.array([rng.uniform(SAC_POS[0] - 1.2, SAC_POS[0] + 1.0), rng.uniform(SAC_POS[1] - 1.3, SAC_POS[1] - 0.3), 0.0])
            self.play(
                d1.animate.move_to([wall_x, pump_ys[0], 0]),
                d2.animate.move_to([wall_x, pump_ys[1], 0]),
                run_time=0.65, rate_func=linear,
            )
            self.play(
                d1.animate.move_to(dest1),
                d2.animate.move_to(dest2),
                run_time=0.65, rate_func=linear,
            )

        self.at("Pump after pump")
        for k in range(2):
            d = stroma_dots[0]
            stroma_dots.remove(d)
            lumen_dots.add(d)
            py = pump_ys[k % 2]
            dest = np.array([rng.uniform(SAC_POS[0] - 1.2, SAC_POS[0] + 1.0), rng.uniform(SAC_POS[1] - 1.3, SAC_POS[1] + 0.55), 0.0])
            self.play(d.animate.move_to([wall_x, py, 0]), run_time=0.50, rate_func=linear)
            self.play(d.animate.move_to(dest), run_time=0.50, rate_func=linear)

        self.finish()


def _sac_backdrop_for_predict():
    """Shared builder for s04_predict end state and s05_pause backdrop."""
    stroma = make_stroma(initial_light=1.0)
    sun = make_sun_moon(initial_light=1.0)
    panel = make_control_panel((0, 0, 0))
    pump_phase = ValueTracker(0.0)
    pump_phase.add_updater(lambda m, dt: m.increment_value(4.5 * dt))
    mini_phase = ValueTracker(0.4)
    mini_phase.add_updater(lambda m, dt: m.increment_value(-0.75 * dt))
    ph_t = ValueTracker(7.0)
    sac_grp = make_thylakoid_sac(pump_phase=pump_phase, ph_tracker=ph_t, covered=True, mini_phase=mini_phase)
    lumen_dots, stroma_dots = make_proton_field(n_lumen=12, n_stroma=3, seed=21)
    protons_lbl = T("protons", size=24, color=WHITE).move_to([2.65, -2.55, 0])

    runners = VGroup()
    pump_ys = [SAC_POS[1] + 0.55, SAC_POS[1] - 0.75, SAC_POS[1] + 0.55]
    for i, py in enumerate(pump_ys):
        d = Dot([2.4, py, 0], radius=0.10, color=WHITE)
        d._t = i * 0.33
        def _cross(m, dt, py=py):
            m._t = (m._t + 0.52 * dt) % 1.0
            x = 2.5 * (1.0 - m._t) + (SAC_POS[0] - 0.9) * m._t
            m.move_to([x, py, 0])
        d.add_updater(_cross)
        runners.add(d)

    return VGroup(stroma, sun, panel, sac_grp, lumen_dots, stroma_dots, protons_lbl, runners), pump_phase, mini_phase, ph_t, sac_grp


class S04Predict(SpokenScene):
    def construct(self):
        stroma = make_stroma(initial_light=1.0)
        sun = make_sun_moon(initial_light=1.0)
        panel = make_control_panel((0, 0, 0))
        pump_phase = ValueTracker(0.0)
        pump_phase.add_updater(lambda m, dt: m.increment_value(4.5 * dt))
        mini_phase = ValueTracker(0.4)
        mini_phase.add_updater(lambda m, dt: m.increment_value(-0.75 * dt))
        ph_t = ValueTracker(7.0)
        sac_grp = make_thylakoid_sac(pump_phase=pump_phase, ph_tracker=ph_t, covered=False, mini_phase=mini_phase)
        lumen_dots, stroma_dots = make_proton_field(n_lumen=12, n_stroma=3, seed=21)
        protons_lbl = T("protons", size=24, color=WHITE).move_to([2.65, -2.55, 0])

        runners = VGroup()
        pump_ys = [SAC_POS[1] + 0.55, SAC_POS[1] - 0.75, SAC_POS[1] + 0.55]
        for i, py in enumerate(pump_ys):
            d = Dot([2.4, py, 0], radius=0.10, color=WHITE)
            d._t = i * 0.33
            def _cross(m, dt, py=py):
                m._t = (m._t + 0.52 * dt) % 1.0
                x = 2.5 * (1.0 - m._t) + (SAC_POS[0] - 0.9) * m._t
                m.move_to([x, py, 0])
            d.add_updater(_cross)
            runners.add(d)

        self.add(stroma, sun, panel, sac_grp, lumen_dots, stroma_dots, protons_lbl, runners, pump_phase, mini_phase)

        self.at("protons go")
        self.wait(2.2)

        self.at("Does the")
        cbox = RoundedRectangle(
            corner_radius=0.12, width=0.68, height=2.82,
            stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.96
        ).move_to([GAUGE_X - 0.16, (GAUGE_Y0 + GAUGE_Y1) / 2, 0])
        cq = M("?", size=40, color=WHITE).move_to(cbox)
        cover = VGroup(cbox, cq).shift(UP * 0.9)
        qcard = question_card("Stroma pH: fall or rise?", left=-1.6, y=2.85, color=WHITE, size=32, max_w=5.2)
        self.play(cover.animate.shift(DOWN * 0.9), FadeIn(qcard), run_time=0.9)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Stroma pH: fall or rise?"
    CARD = {"left": -1.6, "y": 2.85, "color": WHITE, "size": 32, "max_w": 5.2}
    SECONDS = 4.5
    RING_AT = (6.0, -3.0, 0)

    def backdrop(self):
        bg, pump_phase, mini_phase, _, _ = _sac_backdrop_for_predict()
        self.add(pump_phase, mini_phase)
        return bg


class S06PhMagnesium(SpokenScene):
    def construct(self):
        bg, pump_phase, mini_phase, ph_t, sac_grp = _sac_backdrop_for_predict()
        qcard = question_card("Stroma pH: fall or rise?", left=-1.6, y=2.85, color=WHITE, size=32, max_w=5.2)
        panel = bg[2]
        self.add(bg, qcard, pump_phase, mini_phase)

        self.at("It rises")
        rise_tag = boxed_label("about 7 → 8", WHITE, size=24, pad=0.12).move_to([2.45, 0.72, 0])
        self.play(
            FadeOut(qcard),
            sac_grp.cover.animate.shift(UP * 1.2).set_opacity(0),
            ph_t.animate.set_value(8.0),
            flip_toggle_anim(panel, 0, on=True),
            run_time=1.8,
        )
        self.remove(sac_grp.cover)
        self.play(FadeIn(rise_tag), run_time=0.5)

        self.at("Signal two")
        p_start = SAC_POS + np.array([0.85, -0.15, 0.0])
        p_end = np.array([3.40, -0.45, 0.0])
        mg_path = DashedVMobject(
            ArcBetweenPoints(p_start, p_end, angle=-0.30, color=SILVER, stroke_width=3.5),
            num_dashes=18
        )
        tb_tag = T("textbook account", size=22, color=GREY).move_to([2.65, -1.90, 0])
        self.play(Create(mg_path), FadeIn(tb_tag), run_time=1.0)

        self.at("Magnesium ions flow")
        mg_dots = VGroup(*[Dot(radius=0.12, color=SILVER).move_to(p_start) for _ in range(3)])
        mg_lbl = T("Mg2+ ions", size=24, color=SILVER).move_to([2.65, 0.02, 0])
        self.play(
            FadeIn(mg_lbl),
            LaggedStart(
                *[d.animate.move_to(p_end + np.array([-0.45 * i, -0.10 * i, 0])) for i, d in enumerate(mg_dots)],
                lag_ratio=0.35, run_time=2.4
            ),
            flip_toggle_anim(panel, 1, on=True),
        )
        self.finish()


class S07RubiscoSite(SpokenScene):
    def construct(self):
        stroma = make_stroma(initial_light=1.0)
        sun = make_sun_moon(initial_light=1.0)
        panel = make_control_panel((1, 1, 0))
        jaw = make_zoomed_rubisco(active=False, open_amt=1.0)
        self.add(stroma, sun, panel)

        self.at("Both signals act")
        self.play(FadeIn(jaw, scale=0.65), run_time=1.6)
        self.play(
            Indicate(panel.rows[0], color=WHITE, scale_factor=1.15),
            Indicate(panel.rows[1], color=SILVER, scale_factor=1.15),
            jaw.upper_jaw.animate.shift(UP * 0.12),
            jaw.lower_jaw.animate.shift(DOWN * 0.12),
            run_time=1.5,
        )

        self.at("separate carbon dioxide")
        # Start below the yellow sun rays (y ~ 0.95)
        act_co2 = make_co2_counter(ringed=True, text="CO2").move_to([4.85, 0.95, 0])
        act_lbl = T("activating CO2", size=26, color=BLUE).next_to(act_co2, UP, buff=0.16)
        act_grp = VGroup(act_co2, act_lbl)
        self.play(FadeIn(act_grp), run_time=0.5)
        self.play(act_grp.animate.move_to(jaw.site_pos + UP * 0.22), run_time=3.4)

        self.at("forming a carbamate")
        carb_lbl = T("carbamate", size=26, color=WHITE).move_to(jaw.site_pos + UP * 0.78)
        self.play(FadeOut(act_lbl), run_time=0.35)
        self.play(
            act_co2.animate.move_to(jaw.site_pos),
            swap(jaw.peg_lbl, carb_lbl, run_time=1.2),
            jaw.peg.animate.set_fill(BLUE, opacity=0.35),
            run_time=2.25,
        )
        jaw.peg_lbl = carb_lbl

        self.at("holds a magnesium ion")
        mg_dot = Dot(radius=0.19, color=SILVER).move_to([4.7, -0.35, 0])
        mg_lbl = M("Mg2+", size=24, color=SILVER).next_to(mg_dot, RIGHT, buff=0.16)
        mg_grp = VGroup(mg_dot, mg_lbl)
        self.play(FadeIn(mg_grp), run_time=0.4)
        self.play(mg_grp.animate.move_to(jaw.mg_pos + RIGHT * 0.25), run_time=2.2)

        self.at("builds the working active site")
        active_lbl = T("working active site", size=28, color=WHITE).move_to([0.45, -2.90, 0])
        self.play(
            jaw.upper_jaw.animate.shift(DOWN * 0.12).set_stroke(WHITE, width=9),
            jaw.lower_jaw.animate.shift(UP * 0.12).set_stroke(WHITE, width=9),
            jaw.back_bridge.animate.set_stroke(WHITE, width=9),
            jaw.body_fill.animate.set_fill(WHITE, opacity=0.28),
            jaw.title.animate.set_color(WHITE),
            Indicate(VGroup(act_co2, mg_dot), color=GOLD, scale_factor=1.25),
            FadeIn(active_lbl),
            run_time=1.8,
        )
        self.finish()


class S08TwoCo2(SpokenScene):
    def construct(self):
        stroma = make_stroma(initial_light=1.0)
        sun = make_sun_moon(initial_light=1.0)
        panel = make_control_panel((1, 1, 0))
        jaw = make_zoomed_rubisco(active=True, open_amt=1.0, show_peg_lbl=False)
        carb_lbl = T("carbamate", size=26, color=WHITE).move_to(jaw.site_pos + UP * 0.78)
        act_co2 = make_co2_counter(ringed=True, text="CO2").move_to(jaw.site_pos)
        mg_dot = Dot(radius=0.19, color=SILVER).move_to(jaw.mg_pos + RIGHT * 0.25)
        mg_lbl = M("Mg2+", size=24, color=SILVER).next_to(mg_dot, RIGHT, buff=0.16)
        sub_co2 = make_co2_counter(ringed=False, text="CO2").move_to([5.4, 1.35, 0])
        rubp = boxed_label("RuBP · 5C", GREEN, size=24, pad=0.14).move_to([5.4, -1.15, 0])
        self.add(stroma, sun, panel, jaw, carb_lbl, act_co2, mg_dot, mg_lbl)

        self.at("High pH")
        self.play(
            Indicate(panel.rows[0], color=WHITE, scale_factor=1.18),
            jaw.peg.animate.set_fill(GOLD, opacity=0.55),
            jaw.upper_jaw.animate.shift(UP * 0.10),
            jaw.lower_jaw.animate.shift(DOWN * 0.10),
            run_time=2.5,
        )

        self.at("more magnesium")
        self.play(
            Indicate(panel.rows[1], color=SILVER, scale_factor=1.18),
            mg_dot.animate.scale(1.25).set_color(WHITE),
            FadeIn(sub_co2), FadeIn(rubp),
            sub_co2.animate.move_to([4.4, 0.95, 0]),
            rubp.animate.move_to([4.4, -0.85, 0]),
            run_time=2.5,
        )

        self.at("one carbon dioxide")
        sw_lbl = T("switch", size=26, color=WHITE).move_to(carb_lbl.get_center())
        self.play(
            swap(carb_lbl, sw_lbl, run_time=0.9),
            sub_co2.animate.move_to([3.10, 0.45, 0]),
            rubp.animate.move_to([3.55, -0.45, 0]),
            jaw.upper_jaw.animate.shift(DOWN * 0.10),
            jaw.lower_jaw.animate.shift(UP * 0.10),
            run_time=2.6,
        )

        self.at("a different one")
        self.play(
            sub_co2.animate.move_to([2.95, 0.35, 0]),
            run_time=0.35,
        )
        self.play(
            jaw.upper_jaw.animate.shift(DOWN * 0.18),
            jaw.lower_jaw.animate.shift(UP * 0.18),
            run_time=0.25,
        )
        pga1 = boxed_label("3-PGA · 3C", GREEN, size=24, pad=0.12).move_to([3.45, -0.15, 0])
        pga2 = boxed_label("3-PGA · 3C", GREEN, size=24, pad=0.12).move_to([3.45, -1.05, 0])
        self.play(
            FadeOut(rubp), FadeIn(pga1), FadeIn(pga2),
            sub_co2.animate.next_to(pga1, RIGHT, buff=0.18),
            jaw.upper_jaw.animate.shift(UP * 0.18),
            jaw.lower_jaw.animate.shift(DOWN * 0.18),
            run_time=0.40,
        )
        pga1_grp = VGroup(pga1, sub_co2)
        self.play(
            pga1_grp.animate.move_to([4.25, -1.65, 0]),
            pga2.animate.move_to([4.25, -2.55, 0]),
            run_time=0.70,
        )
        self.finish()


class S09Activase(SpokenScene):
    def construct(self):
        stroma = make_stroma(initial_light=1.0)
        sun = make_sun_moon(initial_light=1.0)
        panel = make_control_panel((1, 1, 0))

        work_center = np.array([-2.35, -0.25, 0.0])
        work_jaw = make_zoomed_rubisco(center=work_center, scale_f=0.56, active=True, open_amt=0.7, show_peg_lbl=False)
        sw_co2 = make_co2_counter(ringed=True, text="CO2").move_to(work_jaw.site_pos)
        work_mg = Dot(radius=0.12, color=SILVER).move_to(work_jaw.mg_pos + RIGHT * 0.12)

        work_t = ValueTracker(0.0)
        work_t.add_updater(lambda m, dt: m.increment_value(2.8 * dt))
        base_up_y = work_jaw.upper_jaw.get_y()
        base_lo_y = work_jaw.lower_jaw.get_y()
        work_jaw.upper_jaw.add_updater(lambda m: m.set_y(base_up_y - 0.12 * (0.5 + 0.5 * np.sin(work_t.get_value()))))
        work_jaw.lower_jaw.add_updater(lambda m: m.set_y(base_lo_y + 0.12 * (0.5 + 0.5 * np.sin(work_t.get_value()))))

        self.add(stroma, sun, panel, work_jaw, sw_co2, work_mg, work_t)

        self.at("not switched on")
        grey_center = np.array([1.45, -0.25, 0.0])
        grey_jaw = make_zoomed_rubisco(center=grey_center, scale_f=0.56, active=False, open_amt=0.9, show_title=False, show_peg_lbl=False)
        grey_jaw.upper_jaw.set_stroke(GREY, width=6)
        grey_jaw.lower_jaw.set_stroke(GREY, width=6)
        grey_jaw.back_bridge.set_stroke(GREY, width=6)
        grey_jaw.body_fill.set_fill(GREY, opacity=0.22)
        not_on_lbl = T("not switched on", size=26, color=GREY).next_to(grey_jaw.upper_jaw, UP, buff=0.22)
        grey_grp = VGroup(grey_jaw, not_on_lbl)
        self.play(FadeIn(grey_grp, shift=LEFT * 0.8), run_time=0.65)

        self.at("clamps onto")
        rubp = boxed_label("RuBP", GREEN, size=24, pad=0.10).move_to([3.55, -1.65, 0])
        self.play(FadeIn(rubp), run_time=0.25)
        self.play(rubp.animate.move_to(grey_center + RIGHT * 0.42), run_time=0.75)
        stuck_lbl = boxed_label("stuck", RED, size=24, pad=0.10).move_to(grey_center + DOWN * 2.15)
        self.play(
            grey_jaw.upper_jaw.animate.shift(DOWN * 0.22),
            grey_jaw.lower_jaw.animate.shift(UP * 0.22),
            FadeIn(stuck_lbl),
            run_time=0.45,
        )
        shake_t = ValueTracker(0.0)
        shake_t.add_updater(lambda m, dt: m.increment_value(28.0 * dt))
        base_x = grey_jaw.get_x()
        grey_jaw.add_updater(lambda m: m.set_x(base_x + 0.04 * np.sin(shake_t.get_value())))
        self.add(shake_t)
        self.wait(1.6)

        self.at("chaperone")
        activase = boxed_label("Rubisco activase", YELLOW, size=24, pad=0.16).move_to([4.65, 0.45, 0])
        atp_blk = make_atp_block().next_to(activase, DOWN, buff=0.18)
        chap = VGroup(activase, atp_blk)
        self.play(FadeIn(chap), run_time=0.5)
        self.play(chap.animate.move_to([4.45, -0.15, 0]), run_time=1.3)

        self.at("pries the sugar loose")
        grey_jaw.clear_updaters()
        grey_jaw.set_x(base_x)
        self.play(
            FadeOut(atp_blk),
            activase.animate.move_to([4.05, -0.15, 0]),
            grey_jaw.upper_jaw.animate.shift(UP * 0.28),
            grey_jaw.lower_jaw.animate.shift(DOWN * 0.28),
            FadeOut(stuck_lbl),
            run_time=0.75,
        )
        self.play(
            rubp.animate.move_to([0.20, -2.55, 0]),
            FadeOut(activase),
            FadeOut(VGroup(grey_jaw, not_on_lbl), shift=RIGHT * 0.8),
            run_time=1.1,
        )
        self.finish()


class S10Thioredoxin(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(1.0)
        phase = ValueTracker(0.4)
        phase.add_updater(lambda m, dt: m.increment_value(-0.55 * dt))

        stroma = make_stroma(sun_light, 1.0)
        sun = make_sun_moon(sun_light, 1.0)
        panel = make_control_panel((1, 1, 0))
        thyl = make_thylakoid_bar(pulsing=True)
        conv = make_conveyor(phase_tracker=phase, active_stations=False, show_latches=True, latch_open=False)
        tray = make_output_tray(count=1)
        self.add(stroma, sun, panel, thyl, conv, tray, phase)

        self.at("Photosystem 1")
        psi_pos = THYL_POS + UP * 0.72
        psi_box = RoundedRectangle(corner_radius=0.10, width=0.60, height=0.42, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.25).move_to(psi_pos)
        psi_lbl = T("Photosystem I", size=22, color=YELLOW).move_to([-4.35, 1.48, 0])
        fd_tok = boxed_label("ferredoxin", CYAN, size=22, pad=0.11).move_to([-4.35, 0.75, 0])
        self.play(FadeIn(psi_box), FadeIn(psi_lbl), run_time=0.35)
        self.play(Indicate(psi_box, color=WHITE, scale_factor=1.18), run_time=0.45)
        self.play(FadeIn(fd_tok), run_time=0.5)

        self.at("Through a reductase")
        gear_pos = np.array([-4.15, -0.55, 0.0])
        gear_ring = Circle(radius=0.33, color=TEXT, stroke_width=3.5).move_to(gear_pos)
        gear_spokes = VGroup(*[
            Line(gear_pos + np.array([np.cos(a), np.sin(a), 0]) * 0.11,
                 gear_pos + np.array([np.cos(a), np.sin(a), 0]) * 0.38,
                 color=TEXT, stroke_width=3)
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ])
        gear_t = ValueTracker(0.0)
        gear_t.add_updater(lambda m, dt: m.increment_value(1.6 * dt))
        gear_spokes.add_updater(lambda m: m.become(VGroup(*[
            Line(gear_pos + np.array([np.cos(a + gear_t.get_value()), np.sin(a + gear_t.get_value()), 0]) * 0.11,
                 gear_pos + np.array([np.cos(a + gear_t.get_value()), np.sin(a + gear_t.get_value()), 0]) * 0.38,
                 color=TEXT, stroke_width=3)
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ])))
        red_lbl = T("reductase", size=22, color=TEXT).next_to(gear_ring, DOWN, buff=0.14)
        trx_tok = make_trx_token("thioredoxin", GREY, size=22, pad=0.11).move_to([-3.95, -2.05, 0])

        self.play(
            FadeIn(gear_ring), FadeIn(gear_spokes), FadeIn(red_lbl), FadeIn(trx_tok),
            fd_tok.animate.move_to(gear_pos + UP * 0.68),
            run_time=1.3,
        )
        self.add(gear_t)

        self.at("makes reduced", nth=1)
        lit_trx = make_trx_token("thioredoxin", ORANGE, size=22, pad=0.11).move_to(trx_tok.get_center())
        self.play(
            fd_tok.animate.set_opacity(0.30),
            swap(trx_tok, lit_trx, run_time=0.65),
        )
        targets = [
            np.array([3.55, 0.72, 0.0]),
            np.array([2.85, -2.52, 0.0]),
            np.array([-3.25, -2.52, 0.0]),
            np.array([-2.25, 2.30, 0.0]),
        ]
        self.play(FadeOut(lit_trx), FadeOut(fd_tok), run_time=0.2)
        copies = VGroup(*[make_trx_token("Trx", ORANGE, size=22, pad=0.10).move_to(lit_trx.get_center()) for _ in range(4)])
        self.play(
            *[c.animate.move_to(t) for c, t in zip(copies, targets)],
            run_time=0.8,
        )
        self.finish()


class S11Latches(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(1.0)
        omega = ValueTracker(0.25)
        phase = ValueTracker(0.4)
        phase.add_updater(lambda m, dt: m.increment_value(-omega.get_value() * dt))

        stroma = make_stroma(sun_light, 1.0)
        sun = make_sun_moon(sun_light, 1.0)
        panel = make_control_panel((1, 1, 0))
        thyl = make_thylakoid_bar(pulsing=True)
        conv = make_conveyor(phase_tracker=phase, active_stations=False, show_latches=True, latch_open=False)
        tray = make_output_tray(count=1)
        hover_pts = [
            np.array([3.55, 0.72, 0.0]),
            np.array([2.85, -2.52, 0.0]),
            np.array([-3.25, -2.52, 0.0]),
            np.array([-2.25, 2.30, 0.0]),
        ]
        copies = VGroup(*[make_trx_token("Trx", ORANGE, size=22, pad=0.10).move_to(p) for p in hover_pts])
        self.add(stroma, sun, panel, thyl, conv, tray, copies, phase)

        self.at("In four")
        self.wait(1.0)

        self.at("breaks a")
        for idx in range(4):
            node, lbl, latch, pt = conv.stations[idx]
            open_latch = make_latch_icon(pt, open_state=True)
            self.play(
                ReplacementTransform(latch, open_latch),
                node.animate.set_stroke(WHITE, width=3.5).set_fill(TEAL, opacity=0.42),
                lbl.animate.set_color(TEXT),
                copies[idx].animate.set_stroke(GOLD, width=3),
                run_time=0.85,
            )

        self.at("active shape")
        self.play(omega.animate.set_value(0.65), run_time=1.0)

        self.at("spends the ATP")
        prk_node, _, _, prk_pt = conv.stations[3]
        atp_blk = make_atp_block().move_to([-4.95, 0.62, 0])
        # Build RuBP · 5C outside lane (above PRK at [-2.25, 1.45] or move cleanly onto lane without hitting 5C)
        rubp_new = boxed_label("RuBP", GREEN, size=22, pad=0.14).move_to(prk_pt + UP * 0.65)
        self.play(
            Indicate(prk_node, color=YELLOW, scale_factor=1.22),
            atp_blk.animate.move_to(prk_pt + LEFT * 0.85),
            run_time=0.85,
        )
        self.play(
            FadeOut(atp_blk),
            FadeIn(rubp_new),
            flip_toggle_anim(panel, 2, on=True),
            run_time=0.75,
        )
        self.play(rubp_new.animate.move_to([-1.25, 2.55, 0]), run_time=0.80)
        self.finish()


class S12Idea(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(1.0)
        phase = ValueTracker(0.4)
        phase.add_updater(lambda m, dt: m.increment_value(-0.72 * dt))

        stroma = make_stroma(sun_light, 1.0)
        sun = make_sun_moon(sun_light, 1.0)
        panel = make_control_panel((1, 1, 1))
        thyl = make_thylakoid_bar(pulsing=True)
        conv = make_conveyor(phase_tracker=phase, active_stations=True, show_latches=True, latch_open=True)
        tray = make_output_tray(count=2)
        self.add(stroma, sun, panel, thyl, conv, tray, phase)

        self.at("Here is the rule")
        self.wait(1.0)

        self.at("thrown by a change")
        wires = VGroup()
        for idx, row in enumerate(panel.rows):
            start_p = SUN_DAY_POS + LEFT * 0.48 + DOWN * (idx * 0.08 - 0.08)
            mid_y = 3.50 - idx * 0.12
            wire = VMobject(color=GOLD, stroke_width=2.8)
            wire.set_points_as_corners([
                start_p,
                [start_p[0] - 0.45, mid_y, 0],
                [panel.box.get_right()[0] + 0.30, mid_y, 0],
                [panel.box.get_right()[0] + 0.08, row.pill.get_center()[1], 0],
            ])
            wires.add(wire)
        wire_lbl = T("made by light", size=24, color=GOLD).move_to([3.45, 2.90, 0])
        self.play(Create(wires), FadeIn(wire_lbl), run_time=1.7)

        self.at("the loop builds sugar")
        atp_s = make_atp_block().move_to([-4.95, 0.25, 0])
        nadph_s = make_nadph_block().move_to([-4.95, -0.45, 0])
        g3p_new = make_g3p_block().move_to([3.30, -1.05, 0])
        rule_lbl = boxed_label("runs with the light", GOLD, size=26, pad=0.14).move_to([-0.20, -3.20, 0])
        self.play(
            atp_s.animate.move_to([-3.35, 0.25, 0]).set_opacity(0),
            nadph_s.animate.move_to([-3.35, -0.45, 0]).set_opacity(0),
            FadeIn(g3p_new),
            FadeIn(rule_lbl),
            run_time=1.0,
        )
        self.play(g3p_new.animate.move_to(TRAY_POS + UP * 0.76), run_time=1.2)
        self.finish()


class S13Dusk(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(1.0)
        omega = ValueTracker(0.68)
        phase = ValueTracker(0.4)
        phase.add_updater(lambda m, dt: m.increment_value(-omega.get_value() * dt))

        stroma = make_stroma(sun_light, 1.0)
        sun = make_sun_moon(sun_light, 1.0)
        panel = make_control_panel((1, 1, 1))
        thyl = make_thylakoid_bar(pulsing=True)
        conv = make_conveyor(phase_tracker=phase, active_stations=True, show_latches=True, latch_open=True)
        tray = make_output_tray(count=3)
        hover_pts = [
            np.array([3.65, 0.72, 0.0]),
            np.array([3.05, -2.52, 0.0]),
            np.array([-3.35, -2.52, 0.0]),
            np.array([-2.25, 2.38, 0.0]),
        ]
        copies = VGroup(*[make_trx_token("Trx", ORANGE, size=22, pad=0.10).move_to(p) for p in hover_pts])
        self.add(stroma, sun, panel, thyl, conv, tray, copies, phase)

        self.at("At nightfall")
        thyl.bar.clear_updaters()
        self.play(
            sun_light.animate.set_value(0.0),
            omega.animate.set_value(0.32),
            run_time=2.2,
        )

        self.at("reoxidized")
        reox_copies = VGroup(*[make_trx_token("re-oxidized", GREY, size=22, pad=0.10).move_to(p) for p in hover_pts])
        self.play(ReplacementTransform(copies, reox_copies), run_time=1.2)

        self.at("bridges reform")
        reform_anims = []
        for idx in range(4):
            node, lbl, latch, pt = conv.stations[idx]
            closed_latch = make_latch_icon(pt, open_state=False)
            reform_anims.append(ReplacementTransform(latch, closed_latch))
            reform_anims.append(node.animate.set_stroke(GREY, width=2).set_fill(BG, opacity=0.90))
            reform_anims.append(lbl.animate.set_color(GREY))
        self.play(*reform_anims, FadeOut(reox_copies), run_time=1.3)

        self.at("switch off")
        self.play(
            flip_toggle_anim(panel, 2, on=False),
            flip_toggle_anim(panel, 1, on=False),
            flip_toggle_anim(panel, 0, on=False),
            conv.clamp.jaws.animate.set_stroke(GREY),
            conv.clamp.label.animate.set_color(GREY),
            run_time=1.1,
        )

        self.at("quietly stalls")
        self.play(omega.animate.set_value(0.0), run_time=1.1)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        sun_light = ValueTracker(0.0)
        omega = ValueTracker(0.0)
        phase = ValueTracker(0.4)
        phase.add_updater(lambda m, dt: m.increment_value(-omega.get_value() * dt))

        stroma = make_stroma(sun_light, 0.0)
        sun = make_sun_moon(sun_light, 0.0)
        panel = make_control_panel((0, 0, 0))
        thyl = make_thylakoid_bar(pulsing=False)
        conv = make_conveyor(phase_tracker=phase, active_stations=False, show_latches=True, latch_open=False)
        tray = make_output_tray(count=2)
        self.add(stroma, sun, panel, thyl, conv, tray, phase)

        self.at("wired")
        wires = VGroup()
        for idx, row in enumerate(panel.rows):
            start_p = SUN_DAY_POS + LEFT * 0.48 + DOWN * (idx * 0.08 - 0.08)
            mid_y = 3.50 - idx * 0.12
            wire = VMobject(color=GOLD, stroke_width=3.0)
            wire.set_points_as_corners([
                start_p,
                [start_p[0] - 0.45, mid_y, 0],
                [panel.box.get_right()[0] + 0.30, mid_y, 0],
                [panel.box.get_right()[0] + 0.08, row.pill.get_center()[1], 0],
            ])
            wires.add(wire)
        wired_lbl = boxed_label("wired to the sun", GOLD, size=26, pad=0.14).move_to([-0.20, -3.20, 0])
        self.play(
            sun_light.animate.set_value(1.0),
            Create(wires),
            FadeIn(wired_lbl),
            run_time=1.5,
        )

        self.at("builds while daylight")
        open_anims = []
        open_latches = []
        for idx in range(4):
            node, lbl, latch, pt = conv.stations[idx]
            ol = make_latch_icon(pt, open_state=True)
            open_latches.append(ol)
            open_anims.append(ReplacementTransform(latch, ol))
            open_anims.append(node.animate.set_stroke(WHITE, width=3.5).set_fill(TEAL, opacity=0.42))
            open_anims.append(lbl.animate.set_color(TEXT))
        g3p_new = make_g3p_block().move_to([3.30, -1.05, 0])
        self.play(
            flip_toggle_anim(panel, 0, on=True),
            flip_toggle_anim(panel, 1, on=True),
            flip_toggle_anim(panel, 2, on=True),
            *open_anims,
            conv.clamp.jaws.animate.set_stroke(WHITE),
            conv.clamp.label.animate.set_color(WHITE),
            omega.animate.set_value(0.75),
            FadeIn(g3p_new),
            run_time=1.2,
        )
        self.play(g3p_new.animate.move_to(TRAY_POS + UP * 0.76), run_time=0.75)

        self.at("rests through")
        close_anims = []
        for idx in range(4):
            node, lbl, _, pt = conv.stations[idx]
            close_anims.append(ReplacementTransform(open_latches[idx], make_latch_icon(pt, open_state=False)))
            close_anims.append(node.animate.set_stroke(GREY, width=2).set_fill(BG, opacity=0.90))
            close_anims.append(lbl.animate.set_color(GREY))
        self.play(
            sun_light.animate.set_value(0.0),
            flip_toggle_anim(panel, 2, on=False),
            flip_toggle_anim(panel, 1, on=False),
            flip_toggle_anim(panel, 0, on=False),
            *close_anims,
            conv.clamp.jaws.animate.set_stroke(GREY),
            conv.clamp.label.animate.set_color(GREY),
            omega.animate.set_value(0.0),
            run_time=1.2,
        )
        self.finish()


class S15End(EndCard):
    LINE = "Signals made by light switch the cycle on; darkness switches it off."
