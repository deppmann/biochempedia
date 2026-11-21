"""
The Loop and the Brake — Chapter 2 of "Absorption, the Liver and Enterohepatic Circulation"

COLOUR MAP (one colour per concept for the whole film):
- WATER_CYAN   (#58C4DD) : water drops drifting through the gut and sinking into blood (carried from Ch. 1)
- BILE_ORANGE  (#F59E2D) : bile acids (dots, loop glow, recycled highlight)
- LIVER_RED    (#9E3B33 / #C95A4F) : liver organ
- FGF_PURPLE   (#B07CE8) : ileal brake signal (FXR switch and FGF19 dots)
- TEXT         (#E8EAF0) : ledger bars, numbers, questions, titles, station names
- GREY         (#8B93A1) : gut lining, villi, ducts, gallbladder wall, greyed-out bars
- GOLD         (#D4A843) : predict countdown ring, dial/question emphasis
- FAT_YELLOW   (#F5E28A) : tiny fat specks carried in micelles (s02 only)

ONE PICTURE OF THE WORLD (carried across all scenes):
Left 65%: cut-away gut tube along the lower band (duodenum -> terminal ileum with ASBT door ->
colon -> out) above a faint blood band; above it, the deep red-brown liver at upper left,
gallbladder sac below it, bile duct down to the duodenum, and portal vein rising from the
terminal ileum back to the liver.
Right 35%: the ledger — a half-circle "captured per cycle" dial at upper right, a "delivered
a day" bar (0–20 g) beside magnified "lost a day" and "made a day" bars (0–2 g), and
"teaching numbers" at bottom right.

WHAT CHANGES PER SCENE (computed from pool = 3.5 g, cycles = 5/day -> delivery = 17.5 g/day,
normal loss = 0.2–0.4 g/day [midpoint 0.3 g/day, capture ~98.3%], 90% capture -> loss = 1.75 g/day):
- s00_link_and_question : ORANGE bile-acid cluster circles the loop faster each lap (lap counter
  ticks); CYAN water drops drift and sink; outlet cyan ghost flashes; closed loop path glows.
- s01_title (silent 2s) : question fades out while title fades in above liver; loop keeps circling.
- s02_loop              : new ORANGE dots appear in liver, fill/swell gallbladder, squeeze down
  bile duct, form micelles carrying yellow fat specks to villi, and return up portal vein.
- s03_names             : four station doors/tap/pump (CYP7A1, ASBT, NTCP, BSEP) activate in turn
  while ORANGE dots circulate through ASBT->NTCP->BSEP and CYP7A1 drips new ones.
- s04_budget            : lap counter ticks 1->5; five 3.5 g blocks stack on "delivered a day" to
  17.5 g; dots slip past ASBT to "out" filling "lost a day" to the 0.2–0.4 g band.
- s05_make              : "made a day" bar appears and fills to 0.2–0.4 g matching CYP7A1 drip
  rate to outlet leak; 17.5 g delivered bar glows ORANGE ("recycled").
- s06_idea              : CYP7A1 drip and outlet leak pulse in sync; ASBT door pulses; "made a day"
  bar pulses; "make = escape" appears.
- s07_predict           : dial swings to 90%; ASBT narrows so ~10% of dots escape into colon;
  delivered stays 17.5 g; lost & made grey out with "?"; question card appears.
- s08_pause (silent)    : question holds; 90% capture simulation runs with ~10% escaping; countdown runs.
- s09_answer            : "lost a day" rises from 0.3 to 1.75 g (10% of 17.5); "before: 0.3" tick
  and "about × 6" bracket appear; colon leak thickens.
- s10_brake             : resets to steady state; zooms into ileal cell at ASBT; dots switch on
  FXR, launch PURPLE FGF19 dots up portal vein, zoom out, and turn CYP7A1 valve partly closed.
- s11_lift              : ASBT narrows & dial drops; FGF19 stream thins; brake lifts off CYP7A1,
  drip speeds up & "made a day" rises; two gallbladder pool ghosts show "keeps up" vs "cannot keep up".
- s12_close             : resets to steady state; loop glows ORANGE; tap drip & outlet leak pulse
  together; FGF19 stream pulses once.
- s13_end (EndCard)     : standard EndCard with LINE from script.json.
"""

from bp_parts import *

# ------------------------------------------------------------------ Colour map
WATER_CYAN = "#58C4DD"
BILE_ORANGE = "#F59E2D"
LIVER_FILL = "#9E3B33"
LIVER_STROKE = "#C95A4F"
FGF_PURPLE = "#B07CE8"
GUT_GREY = "#8B93A1"
FAT_YELLOW = "#F5E28A"

# ------------------------------------------------------------------ Shared geometry constants
LIVER_CENTER = np.array([-4.05, 1.72, 0.0])
GB_CENTER = np.array([-3.05, 0.25, 0.0])

PT_CYP = np.array([-4.45, 1.76, 0.0])
PT_BSEP = np.array([-3.55, 0.88, 0.0])
PT_GB_NECK = np.array([-3.45, 0.42, 0.0])
PT_DUODENUM = np.array([-5.35, -1.32, 0.0])
PT_ILEUM = np.array([-0.55, -1.32, 0.0])
PT_ASBT = np.array([-0.55, -1.06, 0.0])
PT_NTCP = np.array([-2.22, 1.48, 0.0])
PT_COLON_OUT = np.array([1.38, -1.32, 0.0])

# Ledger geometry on the right 35% (x in [2.35, 6.45])
DIAL_CENTER = np.array([4.60, 2.24, 0.0])
DIAL_RADIUS = 0.86
BAR_Y0 = -1.96
BAR_Y1 = -0.12
BAR_H = BAR_Y1 - BAR_Y0  # 1.84 scene units
DELIV_X = 2.95
LOST_X = 4.38
MADE_X = 6.04
BAR_W = 0.44

# Canonical loop waypoints for particle transport
DUCT_PTS = [
    PT_BSEP,
    np.array([-3.58, 0.45, 0.0]),
    np.array([-4.15, 0.05, 0.0]),
    np.array([-5.05, -0.45, 0.0]),
    np.array([-5.35, -1.05, 0.0]),
    PT_DUODENUM,
]
GUT_PTS = [
    PT_DUODENUM,
    np.array([-3.8, -1.36, 0.0]),
    np.array([-2.1, -1.36, 0.0]),
    PT_ILEUM,
]
PORTAL_PTS = [
    PT_ASBT,
    np.array([-0.55, -0.35, 0.0]),
    np.array([-0.82, 0.55, 0.0]),
    np.array([-1.50, 1.18, 0.0]),
    PT_NTCP,
]
LIVER_PTS = [
    PT_NTCP,
    np.array([-3.05, 1.55, 0.0]),
    np.array([-3.55, 1.18, 0.0]),
    PT_BSEP,
]
COLON_PTS = [
    PT_ILEUM,
    np.array([0.40, -1.32, 0.0]),
    PT_COLON_OUT,
]


def _smooth_path(pts, color=GUT_GREY, width=3.0, opacity=0.0):
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    m.set_points_smoothly([np.array(p, dtype=float) for p in pts])
    return m


def build_liver():
    """Asymmetric two-lobed liver silhouette (no molecules, clean organ outline)."""
    pts = [
        [-5.75, 1.05, 0],
        [-5.85, 2.05, 0],
        [-4.95, 2.52, 0],
        [-3.45, 2.38, 0],
        [-2.18, 1.92, 0],
        [-2.12, 1.25, 0],
        [-3.05, 0.92, 0],
        [-4.55, 0.86, 0],
        [-5.55, 0.88, 0],
    ]
    body = Polygon(*pts, stroke_color=LIVER_STROKE, stroke_width=3.5, fill_color=LIVER_FILL, fill_opacity=0.38)
    body.round_corners(0.35)
    return body


def build_gallbladder(scale=1.0):
    """Pear-shaped gallbladder sac below the right underside of the liver."""
    pts = [
        [-3.42, 0.48, 0],
        [-2.85, 0.42, 0],
        [-2.62, 0.14, 0],
        [-2.88, -0.06, 0],
        [-3.32, 0.10, 0],
    ]
    sac = Polygon(*pts, stroke_color=GUT_GREY, stroke_width=3.0, fill_color=LIVER_FILL, fill_opacity=0.18)
    sac.round_corners(0.18)
    if scale != 1.0:
        sac.scale(scale, about_point=PT_GB_NECK)
    return sac


def build_gut_and_vessels():
    """Cut-away gut tube with villi, colon outlet, blood band, bile duct and portal vein."""
    top_left = Line([-5.85, -1.02, 0], [-0.82, -1.02, 0], color=GUT_GREY, stroke_width=3.0)
    top_right = Line([-0.28, -1.02, 0], [1.38, -1.02, 0], color=GUT_GREY, stroke_width=3.0)
    bot_wall = Line([-5.85, -1.78, 0], [1.38, -1.78, 0], color=GUT_GREY, stroke_width=3.0)

    lumen_bg = Rectangle(width=7.23, height=0.76, stroke_width=0, fill_color=GUT_GREY, fill_opacity=0.12)
    lumen_bg.move_to([-2.235, -1.40, 0])

    villi_pts = []
    xs = np.linspace(-5.75, -0.45, 29)
    for i, x in enumerate(xs):
        y = -1.76 if i % 2 == 0 else -1.56
        villi_pts.append([x, y, 0])
    villi = VMobject(stroke_color=GUT_GREY, stroke_width=2.5, fill_opacity=0)
    villi.set_points_smoothly([np.array(p) for p in villi_pts])

    blood_band = Rectangle(width=4.40, height=0.50, stroke_color=LIVER_STROKE, stroke_width=2.0,
                           stroke_opacity=0.55, fill_color=LIVER_FILL, fill_opacity=0.22)
    blood_band.move_to([-3.65, -2.13, 0])

    duct_center = _smooth_path(DUCT_PTS, color=GUT_GREY, width=10, opacity=0.20)
    duct_line = _smooth_path(DUCT_PTS, color=GUT_GREY, width=2.8, opacity=0.85)
    gb_branch = Line(PT_GB_NECK, [-3.08, 0.25, 0], color=GUT_GREY, stroke_width=2.8)

    portal_fill = _smooth_path(PORTAL_PTS, color=LIVER_STROKE, width=14, opacity=0.18)
    portal_line = _smooth_path(PORTAL_PTS, color=LIVER_STROKE, width=2.8, opacity=0.80)

    return VGroup(lumen_bg, blood_band, duct_center, portal_fill,
                  top_left, top_right, bot_wall, villi, duct_line, gb_branch, portal_line)


def build_stations():
    """Plain geometric tap/doors/pump for CYP7A1, ASBT, NTCP, BSEP (no molecular structures)."""
    cyp_pipe = Line(PT_CYP + LEFT * 0.28, PT_CYP + RIGHT * 0.14, color=TEXT, stroke_width=4)
    cyp_spout = Line(PT_CYP + RIGHT * 0.14, PT_CYP + RIGHT * 0.14 + DOWN * 0.18, color=TEXT, stroke_width=4)
    cyp_stem = Line(PT_CYP + LEFT * 0.06, PT_CYP + LEFT * 0.06 + UP * 0.14, color=TEXT, stroke_width=3.5)
    cyp_valve = Line(PT_CYP + LEFT * 0.22 + UP * 0.14, PT_CYP + RIGHT * 0.10 + UP * 0.14, color=GOLD, stroke_width=5)
    cyp_tap = VGroup(cyp_pipe, cyp_spout, cyp_stem, cyp_valve)
    cyp_tap.valve = cyp_valve
    cyp_tap.pivot = PT_CYP + LEFT * 0.06 + UP * 0.14

    asbt_l = Line([-0.82, -1.02, 0], [-0.74, -1.02, 0], color=BILE_ORANGE, stroke_width=6)
    asbt_r = Line([-0.36, -1.02, 0], [-0.28, -1.02, 0], color=BILE_ORANGE, stroke_width=6)
    asbt_frame = VGroup(
        Line([-0.82, -1.09, 0], [-0.82, -0.95, 0], color=TEXT, stroke_width=3),
        Line([-0.28, -1.09, 0], [-0.28, -0.95, 0], color=TEXT, stroke_width=3),
    )
    asbt_door = VGroup(asbt_frame, asbt_l, asbt_r)
    asbt_door.left_leaf = asbt_l
    asbt_door.right_leaf = asbt_r

    ntcp_door = VGroup(
        Line(PT_NTCP + UP * 0.16 + LEFT * 0.04, PT_NTCP + UP * 0.05 + LEFT * 0.04, color=BILE_ORANGE, stroke_width=5),
        Line(PT_NTCP + DOWN * 0.16 + RIGHT * 0.04, PT_NTCP + DOWN * 0.05 + RIGHT * 0.04, color=BILE_ORANGE, stroke_width=5),
    )

    bsep_pump = Circle(radius=0.14, color=BILE_ORANGE, stroke_width=3.5, fill_color=BG, fill_opacity=0.85).move_to(PT_BSEP)
    bsep_arrow = Arrow(PT_BSEP + UP * 0.09, PT_BSEP + DOWN * 0.09, buff=0, stroke_width=3,
                       max_tip_length_to_length_ratio=0.45, color=TEXT)
    bsep = VGroup(bsep_pump, bsep_arrow)

    return cyp_tap, asbt_door, ntcp_door, bsep


def set_asbt_opening(asbt_door, frac):
    """frac=1.0 -> wide open; frac=0.25 -> narrow gap."""
    half_span = 0.27
    gap_half = 0.04 + 0.15 * float(np.clip(frac, 0.0, 1.0))
    asbt_door.left_leaf.put_start_and_end_on([-0.55 - half_span, -1.02, 0], [-0.55 - gap_half, -1.02, 0])
    asbt_door.right_leaf.put_start_and_end_on([-0.55 + gap_half, -1.02, 0], [-0.55 + half_span, -1.02, 0])


def set_cyp_valve(cyp_tap, openness):
    """openness=1.0 -> horizontal wide open; openness=0.3 -> tilted/partly closed."""
    angle = (1.0 - float(np.clip(openness, 0.0, 1.2))) * 0.85
    dx = 0.16 * np.cos(angle)
    dy = 0.16 * np.sin(angle)
    p = cyp_tap.pivot
    cyp_tap.valve.put_start_and_end_on(p + np.array([-dx, -dy, 0]), p + np.array([dx, dy, 0]))


def build_static_organ_labels():
    """Permanent place names positioned clear of all paths and outlines."""
    liver_lbl = T("liver", 28, LIVER_STROKE).move_to([-3.70, 2.22, 0])
    gb_lbl = T("gallbladder", 24, GUT_GREY).move_to([-1.70, -0.26, 0])
    ileum_lbl = T("terminal ileum", 24, GUT_GREY).move_to([-0.28, -2.14, 0])
    out_lbl = T("out", 26, GUT_GREY).move_to([1.78, -1.32, 0])
    return VGroup(liver_lbl, gb_lbl, ileum_lbl, out_lbl)


def build_ledger(deliv_t, lost_t, made_t, dial_t, show_dial_pct=False, show_made=False, grey_lost_made=False):
    """Build the right-35% ledger: dial, delivered bar (0-20 g), lost & made bars (0-2 g), teaching numbers tag."""
    c = DIAL_CENTER
    r = DIAL_RADIUS
    track = Arc(radius=r, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=10)
    v = lambda: float(np.clip(dial_t.get_value(), 0.001, 1.0))
    val = always_redraw(lambda: Arc(radius=r, start_angle=PI, angle=-PI * v(), arc_center=c,
                                    stroke_color=BILE_ORANGE, stroke_width=10))
    needle = always_redraw(lambda: Line(
        c, c + 0.78 * r * np.array([np.cos(PI - PI * v()), np.sin(PI - PI * v()), 0]),
        color=TEXT, stroke_width=4.5,
    ))
    dial_lbl = T("captured per cycle", 24, TEXT).move_to(c + DOWN * 0.72)
    dial_grp = VGroup(track, val, needle, dial_lbl)
    if show_dial_pct:
        pct = always_redraw(lambda: M(f"{dial_t.get_value() * 100:.0f}%", 30, GOLD).move_to(c + DOWN * 0.28))
        dial_grp.add(pct)

    # 2. Delivered bar axis (0 to 20 g)
    ax_d_x = DELIV_X - BAR_W / 2 - 0.14
    ax_d = Line([ax_d_x, BAR_Y0, 0], [ax_d_x, BAR_Y1, 0], color=GREY, stroke_width=2.5)
    base_d = Line([ax_d_x, BAR_Y0, 0], [DELIV_X + BAR_W / 2 + 0.12, BAR_Y0, 0], color=GREY, stroke_width=2.5)
    d_ticks = VGroup()
    for val_g in (0, 10, 20):
        yy = BAR_Y0 + (val_g / 20.0) * BAR_H
        d_ticks.add(Line([ax_d_x - 0.08, yy, 0], [ax_d_x, yy, 0], color=GREY, stroke_width=2.5))
        d_ticks.add(M(f"{val_g}", 22, GREY).next_to([ax_d_x - 0.10, yy, 0], LEFT, buff=0.06))
    d_unit = T("g", 22, GREY).move_to([ax_d_x + 0.10, BAR_Y1 + 0.22, 0])

    def mk_deliv_bar():
        h = max(0.02, (np.clip(deliv_t.get_value(), 0, 20) / 20.0) * BAR_H)
        return Rectangle(width=BAR_W, height=h, stroke_color=TEXT, stroke_width=2,
                         fill_color=TEXT, fill_opacity=0.82).move_to([DELIV_X, BAR_Y0 + h / 2, 0])

    deliv_bar = always_redraw(mk_deliv_bar)
    deliv_lbl = T("delivered\na day", 24, TEXT, line_spacing=0.85).move_to([DELIV_X, BAR_Y0 - 0.62, 0])

    # 3. Magnified axis (0 to 2 g) for lost & made
    ax_m_x = LOST_X - BAR_W / 2 - 0.16
    ax_m = Line([ax_m_x, BAR_Y0, 0], [ax_m_x, BAR_Y1, 0], color=GREY, stroke_width=2.5)
    base_m = Line([ax_m_x, BAR_Y0, 0], [MADE_X + BAR_W / 2 + 0.12, BAR_Y0, 0], color=GREY, stroke_width=2.5)
    m_ticks = VGroup()
    for val_g in (0, 1, 2):
        yy = BAR_Y0 + (val_g / 2.0) * BAR_H
        m_ticks.add(Line([ax_m_x - 0.08, yy, 0], [ax_m_x, yy, 0], color=GREY, stroke_width=2.5))
        m_ticks.add(M(f"{val_g}", 22, GREY).next_to([ax_m_x - 0.10, yy, 0], LEFT, buff=0.06))
    m_unit = T("g (×10)", 22, GREY).move_to([ax_m_x + 0.56, BAR_Y1 + 0.22, 0])

    def _small_bar(x_pos, tracker, dimmed=False):
        def mk():
            v_g = float(np.clip(tracker.get_value(), 0.0, 2.0))
            h = max(0.02, (v_g / 2.0) * BAR_H)
            col = GREY if dimmed else TEXT
            op = 0.25 if dimmed else 0.82
            return Rectangle(width=BAR_W, height=h, stroke_color=col, stroke_width=2,
                             fill_color=col, fill_opacity=op).move_to([x_pos, BAR_Y0 + h / 2, 0])
        return always_redraw(mk)

    lost_bar = _small_bar(LOST_X, lost_t, dimmed=grey_lost_made)
    lost_lbl = T("lost\na day", 24, GREY if grey_lost_made else TEXT, line_spacing=0.85).move_to([LOST_X, BAR_Y0 - 0.62, 0])

    band_y0 = BAR_Y0 + (0.2 / 2.0) * BAR_H
    band_y1 = BAR_Y0 + (0.4 / 2.0) * BAR_H
    lost_band = Rectangle(width=BAR_W + 0.08, height=band_y1 - band_y0, stroke_color=GOLD,
                          stroke_width=1.8, fill_color=GOLD, fill_opacity=0.25).move_to([LOST_X, (band_y0 + band_y1) / 2, 0])

    bars_grp = VGroup(ax_d, base_d, d_ticks, d_unit, deliv_bar, deliv_lbl,
                      ax_m, base_m, m_ticks, m_unit, lost_bar, lost_lbl, lost_band)

    made_bar = _small_bar(MADE_X, made_t, dimmed=grey_lost_made)
    made_lbl = T("made\na day", 24, GREY if grey_lost_made else TEXT, line_spacing=0.85).move_to([MADE_X, BAR_Y0 - 0.62, 0])
    made_band = Rectangle(width=BAR_W + 0.08, height=band_y1 - band_y0, stroke_color=GOLD,
                          stroke_width=1.8, fill_color=GOLD, fill_opacity=0.25).move_to([MADE_X, (band_y0 + band_y1) / 2, 0])
    made_grp = VGroup(made_bar, made_lbl, made_band)
    if show_made:
        bars_grp.add(made_grp)

    tag = scope_tag("teaching numbers")
    return VGroup(dial_grp, bars_grp, tag), {
        "dial": dial_grp,
        "deliv_bar": deliv_bar,
        "lost_bar": lost_bar,
        "lost_band": lost_band,
        "made_grp": made_grp,
        "made_bar": made_bar,
        "made_band": made_band,
        "tag": tag,
    }


def make_flow_paths():
    """Hidden reference Bezier paths used by particle updaters so world transforms move particles too."""
    duct = _smooth_path(DUCT_PTS)
    gut = _smooth_path(GUT_PTS)
    portal = _smooth_path(PORTAL_PTS)
    liver = _smooth_path(LIVER_PTS)
    colon = _smooth_path(COLON_PTS)
    return VGroup(duct, gut, portal, liver, colon), (duct, gut, portal, liver, colon)


def start_water_flow(scene_group, seed=7, n_drops=16):
    """Faint CYAN water drops drifting right along the gut and sinking into the blood band."""
    rng = np.random.default_rng(seed)
    drops = VGroup()
    for i in range(n_drops):
        d = Dot(radius=0.055, color=WATER_CYAN).set_opacity(0.50)
        d.u = (i / n_drops + rng.uniform(0, 0.05)) % 1.0
        d.phase = rng.uniform(0.0, 1.0)
        d.sink = i % 3 != 0
        d.layout_ok = True
        drops.add(d)

    def update_water(mob, dt):
        for d in mob:
            d.u = (d.u + 0.16 * dt) % 1.0
            x = -5.7 + 6.9 * d.u
            if d.sink and -5.3 < x < -1.5:
                prog = (x + 5.3) / 3.8
                y = -1.25 - 0.85 * (prog ** 0.8) + 0.06 * np.sin(6 * d.u + d.phase * TAU)
                op = 0.50 * (1.0 - 0.55 * prog)
            else:
                y = -1.35 + 0.08 * np.sin(8 * d.u + d.phase * TAU)
                op = 0.42
            d.move_to([x, y, 0]).set_opacity(op)

    update_water(drops, 0.0)
    drops.add_updater(update_water)
    scene_group.add(drops)
    return drops


def start_bile_loop(world_group, path_tuple, capture_frac=0.983, speed=0.28, make_rate=0.55,
                    n_loop=32, seed=11, lap_tracker=None, seed_escape=0.0):
    """Computed bile-acid particle transport using fixed-size dot pools (safe under world transforms)."""
    duct, gut, portal, liver, colon = path_tuple
    rng = np.random.default_rng(seed)
    state = {
        "speed": float(speed),
        "capture": float(capture_frac),
        "make_rate": float(make_rate),
        "escape_acc": float(seed_escape),
        "drip_acc": 0.4,
        "paused": False,
        "pool_scale": 1.0,
    }

    rank_rng = np.random.default_rng(seed + 100)
    ranks = rank_rng.permutation(n_loop)
    loop_dots = VGroup()
    for i in range(n_loop):
        d = Dot(radius=0.075, color=BILE_ORANGE)
        frac = i / n_loop
        d.seg = int(frac * 4) % 4
        d.u = (frac * 4) % 1.0
        d.jitter = rng.uniform(-0.04, 0.04, size=2)
        d.rank = int(ranks[i])
        d.layout_ok = True
        loop_dots.add(d)

    colon_pool = VGroup()
    for _ in range(14):
        c = Dot(radius=0.072, color=BILE_ORANGE).set_opacity(0.0)
        c.active = False
        c.u = 0.0
        c.jitter = rng.uniform(-0.03, 0.03, size=2)
        c.layout_ok = True
        colon_pool.add(c)

    drip_pool = VGroup()
    for _ in range(8):
        dr = Dot(radius=0.062, color=BILE_ORANGE).set_opacity(0.0)
        dr.active = False
        dr.u = 0.0
        dr.layout_ok = True
        drip_pool.add(dr)

    seg_paths = (duct, gut, portal, liver)
    seg_rates = (1.15, 0.85, 1.05, 1.35)

    def update_loop(mob, dt):
        if state["paused"]:
            return
        spd = state["speed"]
        for idx, d in enumerate(loop_dots):
            d.u += spd * seg_rates[d.seg] * dt
            if d.u >= 1.0:
                d.u -= 1.0
                prev_seg = d.seg
                d.seg = (d.seg + 1) % 4
                if prev_seg == 3 and idx == 0 and lap_tracker is not None:
                    lap_tracker.increment_value(1)
                if prev_seg == 1:
                    state["escape_acc"] += (1.0 - state["capture"])
                    if state["escape_acc"] >= 1.0:
                        state["escape_acc"] -= 1.0
                        for c in colon_pool:
                            if not c.active:
                                c.active = True
                                c.u = 0.0
                                break

            p = seg_paths[d.seg].point_from_proportion(float(np.clip(d.u, 0, 1)))
            d.move_to(p + np.array([d.jitter[0], d.jitter[1], 0]))
            show = (d.rank / len(loop_dots)) <= state["pool_scale"]
            d.set_opacity(0.95 if show else 0.0)

        for c in colon_pool:
            if not c.active:
                c.set_opacity(0.0)
                continue
            c.u += spd * 0.9 * dt
            if c.u >= 1.0:
                c.active = False
                c.set_opacity(0.0)
            else:
                p = colon.point_from_proportion(c.u)
                c.move_to(p + np.array([c.jitter[0], c.jitter[1], 0])).set_opacity(0.95)

        state["drip_acc"] += state["make_rate"] * dt
        if state["drip_acc"] >= 1.0:
            state["drip_acc"] -= 1.0
            for dr in drip_pool:
                if not dr.active:
                    dr.active = True
                    dr.u = 0.0
                    break

        cyp_start = liver.point_from_proportion(0.65)
        bsep_end = liver.point_from_proportion(1.0)
        for dr in drip_pool:
            if not dr.active:
                dr.set_opacity(0.0)
                continue
            dr.u += 0.75 * dt
            if dr.u >= 1.0:
                dr.active = False
                dr.set_opacity(0.0)
            else:
                dr.move_to(cyp_start + dr.u * (bsep_end - cyp_start)).set_opacity(0.95)

    container = VGroup(loop_dots, colon_pool, drip_pool)
    update_loop(container, 0.0)
    container.add_updater(update_loop)
    world_group.add(container)
    return container, state


def start_fgf19_stream(world_group, path_tuple, rate=0.9, settle_on_cyp=True):
    """PURPLE FGF19 signal dots using a fixed-size pool rising up portal vein to CYP7A1."""
    _, _, portal, liver, _ = path_tuple
    dots = VGroup()
    state = {"rate": float(rate), "acc": 0.3, "settle": settle_on_cyp}
    rng = np.random.default_rng(23)

    for i in range(12):
        p = Dot(radius=0.062, color=FGF_PURPLE).set_opacity(0.0)
        p.active = i < 3
        p.u = (0.2 + 0.3 * i) if p.active else 0.0
        p.off = rng.uniform(-0.04, 0.04, size=2)
        p.layout_ok = True
        dots.add(p)

    def update_fgf(mob, dt):
        state["acc"] += state["rate"] * dt
        if state["acc"] >= 1.0:
            state["acc"] -= 1.0
            for p in dots:
                if not p.active:
                    p.active = True
                    p.u = 0.0
                    break
        cyp_pt = liver.point_from_proportion(0.65)
        ntcp_pt = portal.point_from_proportion(1.0)
        for p in dots:
            if not p.active:
                p.set_opacity(0.0)
                continue
            p.u += 0.45 * dt
            if p.u >= 1.0:
                if state["settle"] and p.u < 1.5:
                    t = (p.u - 1.0) / 0.5
                    p.move_to(ntcp_pt + t * (cyp_pt - ntcp_pt)).set_opacity(0.95)
                else:
                    p.active = False
                    p.set_opacity(0.0)
            else:
                pos = portal.point_from_proportion(p.u) + np.array([p.off[0], p.off[1], 0])
                p.move_to(pos).set_opacity(0.95)

    update_fgf(dots, 0.0)
    dots.add_updater(update_fgf)
    world_group.add(dots)
    return dots, state


def build_base_world(deliv_val=17.5, lost_val=0.3, made_val=0.3, dial_val=0.983,
                     show_dial_pct=False, show_made=False, grey_lost_made=False,
                     asbt_open=1.0, cyp_open=1.0, show_stations=True,
                     capture_frac=0.983, speed=0.28, make_rate=0.55, n_loop=32, seed_escape=0.0):
    """Construct the complete carried-over world and ledger in consistent coordinates."""
    liver = build_liver()
    gb = build_gallbladder()
    gut = build_gut_and_vessels()
    cyp_tap, asbt_door, ntcp_door, bsep = build_stations()
    set_asbt_opening(asbt_door, asbt_open)
    set_cyp_valve(cyp_tap, cyp_open)

    paths_grp, path_tuple = make_flow_paths()
    organs = VGroup(gut, liver, gb, paths_grp)
    if show_stations:
        organs.add(cyp_tap, asbt_door, ntcp_door, bsep)

    world = VGroup(organs)
    water = start_water_flow(world)
    bile_grp, bile_state = start_bile_loop(world, path_tuple, capture_frac=capture_frac,
                                           speed=speed, make_rate=make_rate, n_loop=n_loop,
                                           seed_escape=seed_escape)
    organ_labels = build_static_organ_labels()

    deliv_t = ValueTracker(deliv_val)
    lost_t = ValueTracker(lost_val)
    made_t = ValueTracker(made_val)
    dial_t = ValueTracker(dial_val)
    ledger, lparts = build_ledger(deliv_t, lost_t, made_t, dial_t,
                                  show_dial_pct=show_dial_pct, show_made=show_made,
                                  grey_lost_made=grey_lost_made)

    return {
        "world": world,
        "liver": liver,
        "gb": gb,
        "gut": gut,
        "paths": path_tuple,
        "cyp": cyp_tap,
        "asbt": asbt_door,
        "ntcp": ntcp_door,
        "bsep": bsep,
        "water": water,
        "bile": bile_grp,
        "bile_state": bile_state,
        "organ_labels": organ_labels,
        "ledger": ledger,
        "lparts": lparts,
        "deliv_t": deliv_t,
        "lost_t": lost_t,
        "made_t": made_t,
        "dial_t": dial_t,
    }


def station_tags():
    """Non-overlapping tags for the four named stations (placed clear of lines & dots)."""
    t_cyp = T("CYP7A1: make", 24, TEXT).move_to([-4.60, 2.82, 0])
    t_asbt = T("ASBT: take back", 24, BILE_ORANGE).move_to([0.92, -0.58, 0])
    t_ntcp = T("NTCP: into liver", 24, TEXT).move_to([-0.88, 2.30, 0])
    t_bsep = T("BSEP: into bile", 24, BILE_ORANGE).move_to([-5.12, 0.56, 0])
    return t_cyp, t_asbt, t_ntcp, t_bsep


# ================================================================== SCENES

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.3, dial_val=0.983,
                             show_stations=False, capture_frac=0.983, speed=0.22, make_rate=0.40)
        laps = ValueTracker(1)
        lap_lbl = counter("lap {:.0f}", laps, at=[-0.6, 2.72, 0], size=28, color=BILE_ORANGE)
        cluster = VGroup(*[Dot(radius=0.08, color=BILE_ORANGE) for _ in range(5)]).arrange_in_grid(2, 3, buff=0.05)
        cluster.move_to(GB_CENTER)
        cluster.layout_ok = True

        self.add(w["world"], w["organ_labels"], w["ledger"], lap_lbl, cluster)

        duct, gut, portal, liver, _ = w["paths"]
        full_loop = VMobject(stroke_color=BILE_ORANGE, stroke_width=5, stroke_opacity=0)
        loop_pts = list(duct.get_points()) + list(gut.get_points()) + list(portal.get_points()) + list(liver.get_points())
        full_loop.set_points(loop_pts)
        self.add(full_loop)

        self.play(MoveAlongPath(cluster, full_loop, rate_func=linear), run_time=4.8)
        laps.set_value(2)
        w["bile_state"]["speed"] = 0.32

        self.at("How can so little")
        q_txt = T("How can so little go so far?", 34, TEXT).move_to([-1.8, 3.30, 0])
        self.play(FadeIn(q_txt, shift=DOWN * 0.1), MoveAlongPath(cluster, full_loop, rate_func=linear), run_time=3.2)
        laps.set_value(3)
        w["bile_state"]["speed"] = 0.44

        self.at("whatever was not taken back")
        ghost_drip = VGroup(
            Dot(radius=0.12, color=WATER_CYAN).set_opacity(0.65).move_to(PT_COLON_OUT + LEFT * 0.22),
            Circle(radius=0.20, stroke_color=WATER_CYAN, stroke_width=3).move_to(PT_COLON_OUT + LEFT * 0.22),
        )
        ghost_drip.layout_ok = True
        self.play(FadeIn(ghost_drip, run_time=0.4), MoveAlongPath(cluster, full_loop, rate_func=linear), run_time=2.5)
        self.play(FadeOut(ghost_drip, run_time=0.4))
        laps.set_value(4)

        self.at("round a loop")
        glow = full_loop.copy().set_stroke(BILE_ORANGE, width=7, opacity=0.95)
        glow.layout_ok = True
        self.play(Create(glow), MoveAlongPath(cluster, full_loop, rate_func=linear), run_time=1.8)
        self.play(FadeOut(glow), run_time=0.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.3, dial_val=0.983,
                             show_stations=False, capture_frac=0.983, speed=0.28, make_rate=0.40)
        q_txt = T("How can so little go so far?", 34, TEXT).move_to([-1.8, 3.30, 0])
        title = T("The Loop and the Brake", 40, TEXT, font=TITLE_FONT).move_to([-2.0, 3.30, 0])
        self.add(w["world"], w["organ_labels"], w["ledger"], q_txt)
        self.play(FadeOut(q_txt, run_time=0.5))
        self.play(FadeIn(title, shift=DOWN * 0.08), run_time=0.6)
        self.finish()


class S02Loop(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.3, dial_val=0.983,
                             show_stations=False, capture_frac=0.983, speed=0.28, make_rate=0.50)
        title = T("The Loop and the Brake", 40, TEXT, font=TITLE_FONT).move_to([-2.0, 3.30, 0])
        self.add(w["world"], w["organ_labels"], w["ledger"], title)
        self.play(FadeOut(title, run_time=0.4))

        self.at("from cholesterol")
        new_dots = VGroup(*[
            Dot(radius=0.09, color=BILE_ORANGE).move_to(PT_CYP + np.array([dx, dy, 0]))
            for dx, dy in [(-0.25, 0.05), (0.0, 0.14), (0.22, -0.04), (-0.08, -0.14)]
        ])
        new_dots.layout_ok = True
        self.play(LaggedStart(*[GrowFromCenter(d) for d in new_dots], lag_ratio=0.15), run_time=1.0)

        self.at("wait in the gallbladder")
        gb_dots = VGroup(*[
            Dot(radius=0.075, color=BILE_ORANGE).move_to(GB_CENTER + np.array([dx, dy, 0]))
            for dx, dy in [(-0.18, 0.06), (0.0, 0.10), (0.16, 0.02), (-0.08, -0.08), (0.12, -0.09)]
        ])
        gb_dots.layout_ok = True
        self.play(
            ReplacementTransform(new_dots, gb_dots),
            w["gb"].animate.scale(1.24, about_point=PT_GB_NECK),
            run_time=1.4,
        )

        self.at("After a meal")
        duct, gut, portal, _, _ = w["paths"]
        self.play(
            w["gb"].animate.scale(1 / 1.24, about_point=PT_GB_NECK),
            MoveAlongPath(gb_dots, duct, rate_func=linear),
            run_time=1.3,
        )

        self.at("form micelles")
        micelles = VGroup()
        for cx in (-4.45, -3.15):
            ring = Circle(radius=0.22, stroke_color=BILE_ORANGE, stroke_width=2.5, fill_color=BILE_ORANGE, fill_opacity=0.12).move_to([cx, -1.25, 0])
            fats = VGroup(*[Dot(radius=0.045, color=FAT_YELLOW).move_to([cx + dx, -1.25 + dy, 0])
                            for dx, dy in [(-0.06, 0.04), (0.06, -0.03), (0.0, 0.06)]])
            biles = VGroup(*[Dot(radius=0.045, color=BILE_ORANGE).move_to([cx + 0.22 * np.cos(a), -1.25 + 0.22 * np.sin(a), 0])
                             for a in np.linspace(0, TAU, 6, endpoint=False)])
            m = VGroup(ring, fats, biles)
            m.layout_ok = True
            micelles.add(m)
        mic_lbl = T("micelles", 26, BILE_ORANGE).move_to([-3.50, -0.68, 0])
        self.play(FadeOut(gb_dots, run_time=0.25), FadeIn(micelles, run_time=0.5), FadeIn(mic_lbl, run_time=0.4))
        self.play(micelles.animate.shift(RIGHT * 1.45 + DOWN * 0.24), run_time=4.8, rate_func=linear)

        self.at("portal blood")
        ret_cluster = VGroup(*[Dot(radius=0.07, color=BILE_ORANGE).move_to(PT_ILEUM + np.array([dx, 0, 0]))
                               for dx in (-0.1, 0.0, 0.1)])
        ret_cluster.layout_ok = True
        self.play(FadeOut(micelles), FadeOut(mic_lbl), FadeIn(ret_cluster), run_time=0.4)
        self.play(MoveAlongPath(ret_cluster, portal, rate_func=linear), run_time=1.8)
        self.play(FadeOut(ret_cluster), run_time=0.3)
        self.finish()


class S03Names(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.3, dial_val=0.983,
                             show_stations=True, capture_frac=0.983, speed=0.28, make_rate=0.75)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        for m in (w["cyp"], w["asbt"], w["ntcp"], w["bsep"]):
            m.set_opacity(0.25)
        self.add(w["world"], w["organ_labels"], w["ledger"])

        self.at("Four names")
        self.wait(0.2)

        self.at("CYP7 a one")
        self.play(w["cyp"].animate.set_opacity(1.0), FadeIn(t_cyp, shift=DOWN * 0.08), run_time=0.7)
        for _ in range(3):
            drop = Dot(radius=0.08, color=BILE_ORANGE).move_to(PT_CYP + RIGHT * 0.14 + DOWN * 0.18)
            drop.layout_ok = True
            self.play(drop.animate.move_to(PT_BSEP), run_time=1.3, rate_func=linear)
            self.remove(drop)

        self.at("takes them back")
        self.play(w["asbt"].animate.set_opacity(1.0), FadeIn(t_asbt, shift=LEFT * 0.08), run_time=0.7)
        pull_dot = Dot(radius=0.08, color=BILE_ORANGE).move_to(PT_ILEUM)
        pull_dot.layout_ok = True
        self.play(MoveAlongPath(pull_dot, w["paths"][2], rate_func=linear), run_time=2.2)
        self.remove(pull_dot)

        self.at("NTCP")
        self.play(w["ntcp"].animate.set_opacity(1.0), FadeIn(t_ntcp, shift=DOWN * 0.08), run_time=0.7)
        self.play(Indicate(w["ntcp"], color=BILE_ORANGE, scale_factor=1.2), run_time=0.8)

        self.at("BSEP")
        self.play(w["bsep"].animate.set_opacity(1.0), FadeIn(t_bsep, shift=RIGHT * 0.08), run_time=0.7)
        self.play(Indicate(w["bsep"], color=BILE_ORANGE, scale_factor=1.2), run_time=0.8)
        self.finish()


class S04Budget(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=0.0, lost_val=0.02, dial_val=0.983,
                             show_stations=True, capture_frac=0.983, speed=0.28, make_rate=0.55,
                             seed_escape=0.88)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep)

        self.at("The pool")
        pool_lbl = T("pool: about 3.5 g", 24, BILE_ORANGE).move_to([-2.35, -0.74, 0])
        self.play(FadeIn(pool_lbl), run_time=0.6)

        self.at("sent round")
        laps = ValueTracker(0)
        lap_c = counter("laps: {:.0f}", laps, at=[DELIV_X, 1.06, 0], size=24, color=BILE_ORANGE)
        self.play(FadeIn(lap_c), run_time=0.3)

        w["bile_state"]["speed"] = 0.44
        blocks = VGroup()
        for k in range(1, 6):
            y_bot = BAR_Y0 + ((k - 1) * 3.5 / 20.0) * BAR_H
            bh = (3.5 / 20.0) * BAR_H
            blk = Rectangle(width=BAR_W, height=bh, stroke_color=BG, stroke_width=1.5,
                            fill_color=TEXT, fill_opacity=0.85).move_to([DELIV_X, y_bot + bh / 2, 0])
            laps.set_value(k)
            w["deliv_t"].set_value(k * 3.5)
            self.play(FadeIn(blk, shift=DOWN * 0.12), run_time=0.45)
            blocks.add(blk)

        self.at("That delivers")
        deliv_num = M("17.5 g\na day", 22, TEXT, line_spacing=0.85).move_to([DELIV_X, 0.72, 0])
        self.play(FadeOut(lap_c), FadeIn(deliv_num), run_time=0.5)

        self.at("escape in stool")
        w["bile_state"]["speed"] = 0.28
        lost_num = M("0.2–0.4 g\na day", 22, GOLD, line_spacing=0.85).move_to([5.20, 0.74, 0])
        self.play(w["lost_t"].animate.set_value(0.30), FadeIn(lost_num), run_time=1.0)
        self.finish()


class S05Make(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.02, dial_val=0.983,
                             show_stations=True, show_made=False, capture_frac=0.983, speed=0.28, make_rate=0.55,
                             seed_escape=0.85)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        pool_lbl = T("pool: about 3.5 g", 24, BILE_ORANGE).move_to([-2.35, -0.74, 0])
        deliv_num = M("17.5 g\na day", 22, TEXT, line_spacing=0.85).move_to([DELIV_X, 0.72, 0])
        lost_num = M("0.2–0.4 g\na day", 22, GOLD, line_spacing=0.85).move_to([5.20, 0.74, 0])
        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep,
                 pool_lbl, deliv_num, lost_num)

        self.at("the liver makes")
        self.play(FadeIn(w["lparts"]["made_grp"]), run_time=0.5)
        self.play(w["made_t"].animate.set_value(0.30), run_time=1.2)

        self.at("recycled not made")
        recycled_glow = Rectangle(width=BAR_W + 0.12, height=(17.5 / 20.0) * BAR_H + 0.08,
                                  stroke_color=BILE_ORANGE, stroke_width=4, fill_color=BILE_ORANGE, fill_opacity=0.28)
        recycled_glow.move_to([DELIV_X, BAR_Y0 + (17.5 / 20.0) * BAR_H / 2, 0])
        recycled_lbl = T("recycled", 26, BILE_ORANGE).move_to([DELIV_X - 0.25, 1.30, 0])
        self.play(FadeIn(recycled_glow), FadeIn(recycled_lbl), run_time=0.8)
        self.finish()


class S06Idea(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.30, dial_val=0.983,
                             show_stations=True, show_made=True, capture_frac=0.983, speed=0.30, make_rate=0.60,
                             seed_escape=0.85)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        pool_lbl = T("pool: about 3.5 g", 24, BILE_ORANGE).move_to([-2.35, -0.74, 0])
        deliv_num = M("17.5 g\na day", 22, TEXT, line_spacing=0.85).move_to([DELIV_X, 0.72, 0])
        lost_num = M("0.2–0.4 g\na day", 22, GOLD, line_spacing=0.85).move_to([5.20, 0.74, 0])
        recycled_lbl = T("recycled", 26, BILE_ORANGE).move_to([DELIV_X - 0.25, 1.30, 0])
        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep,
                 pool_lbl, deliv_num, lost_num, recycled_lbl)

        self.at("new supply only")
        cyp_ring = Circle(radius=0.25, color=BILE_ORANGE, stroke_width=4).move_to(PT_CYP + DOWN * 0.04)
        out_ring = Circle(radius=0.18, color=BILE_ORANGE, stroke_width=4).move_to(PT_COLON_OUT + LEFT * 0.22)
        self.play(FadeIn(cyp_ring), FadeIn(out_ring), run_time=0.5)
        self.play(Indicate(cyp_ring, scale_factor=1.25), Indicate(out_ring, scale_factor=1.25), run_time=1.0)
        self.play(FadeOut(cyp_ring), FadeOut(out_ring), run_time=0.4)

        self.at("Capture mostly")
        asbt_ring = Circle(radius=0.34, color=GOLD, stroke_width=4).move_to([-0.55, -1.02, 0])
        asbt_ring.layout_ok = True
        self.play(FadeIn(asbt_ring), run_time=0.3)
        self.play(Indicate(asbt_ring, scale_factor=1.25), run_time=0.9)
        self.play(FadeOut(asbt_ring), run_time=0.3)

        self.at("how much the liver")
        rule_lbl = T("make = escape", 34, GOLD).move_to([-2.0, 3.32, 0])
        self.play(Indicate(w["lparts"]["made_bar"], color=GOLD, scale_factor=1.15), FadeIn(rule_lbl), run_time=0.9)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.30, dial_val=0.983,
                             show_stations=True, show_dial_pct=False, show_made=True,
                             capture_frac=0.983, speed=0.28, make_rate=0.55)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        deliv_num = M("17.5 g\na day", 22, TEXT, line_spacing=0.85).move_to([DELIV_X, 0.72, 0])
        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep, deliv_num)

        self.at("slip to 90")
        asbt_t = ValueTracker(1.0)
        w["asbt"].add_updater(lambda m: set_asbt_opening(m, asbt_t.get_value()))
        w["bile_state"]["capture"] = 0.90
        pct_90 = M("90%", 30, GOLD).move_to(DIAL_CENTER + DOWN * 0.28)
        self.play(w["dial_t"].animate.set_value(0.90), asbt_t.animate.set_value(0.32), run_time=1.2)
        self.play(FadeIn(pct_90), run_time=0.3)
        w["asbt"].clear_updaters()

        self.at("Delivery stays")
        self.play(Indicate(deliv_num, color=GOLD, scale_factor=1.1), run_time=0.8)

        self.at("How much must")
        grey_lost = Rectangle(width=BAR_W + 0.06, height=0.62, stroke_color=GREY, stroke_width=2,
                              fill_color=BG, fill_opacity=0.85).move_to([LOST_X, BAR_Y0 + 0.31, 0])
        grey_made = Rectangle(width=BAR_W + 0.06, height=0.62, stroke_color=GREY, stroke_width=2,
                              fill_color=BG, fill_opacity=0.85).move_to([MADE_X, BAR_Y0 + 0.31, 0])
        q_mark = T("?", 38, GOLD).move_to([(LOST_X + MADE_X) / 2, BAR_Y0 + 0.96, 0])
        q_card = question_card("How much must the liver make?", y=3.36, color=TEXT, left=-5.6, max_w=7.0, size=32)
        self.play(FadeIn(grey_lost), FadeIn(grey_made), FadeIn(q_mark), FadeIn(q_card), run_time=0.8)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "How much must the liver make?"
    CARD = {"y": 3.36, "color": TEXT, "left": -5.6, "max_w": 7.0, "size": 32}
    RING_AT = (2.35, 3.35, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.30, dial_val=0.90,
                             show_stations=True, show_dial_pct=True, show_made=True,
                             grey_lost_made=True, asbt_open=0.32,
                             capture_frac=0.90, speed=0.28, make_rate=0.55)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        deliv_num = M("17.5 g\na day", 22, TEXT, line_spacing=0.85).move_to([DELIV_X, 0.72, 0])
        q_mark = T("?", 38, GOLD).move_to([(LOST_X + MADE_X) / 2, BAR_Y0 + 0.96, 0])
        return VGroup(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep, deliv_num, q_mark)


class S09Answer(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.30, dial_val=0.90,
                             show_stations=True, show_dial_pct=True, show_made=True,
                             grey_lost_made=False, asbt_open=0.32,
                             capture_frac=0.90, speed=0.28, make_rate=0.55, seed_escape=0.7)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        deliv_num = M("17.5 g\na day", 22, TEXT, line_spacing=0.85).move_to([DELIV_X, 0.72, 0])
        q_card = question_card("How much must the liver make?", y=3.36, color=TEXT, left=-5.6, max_w=7.0, size=32)
        made_cover = Rectangle(width=BAR_W + 0.04, height=0.42, stroke_color=GREY, stroke_width=2,
                               fill_color=GREY, fill_opacity=0.35).move_to([MADE_X, BAR_Y0 + 0.21, 0])
        made_q = T("?", 30, GREY).move_to([MADE_X, BAR_Y0 + 0.84, 0])

        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep,
                 deliv_num, q_card, made_cover, made_q)

        self.at("10 % of 17")
        y_before = BAR_Y0 + (0.30 / 2.0) * BAR_H
        before_tick = DashedLine([LOST_X - 0.26, y_before, 0], [LOST_X + 0.30, y_before, 0], color=GOLD, stroke_width=2.5)
        before_lbl = T("before:\n0.3", 22, GREY, line_spacing=0.80).move_to([5.23, -1.48, 0])
        lost_live = always_redraw(
            lambda: M(f"{w['lost_t'].get_value():.2f} g\na day", 22, GOLD, line_spacing=0.85).move_to([4.95, 0.74, 0])
        )
        self.play(FadeOut(q_card), FadeIn(before_tick), FadeIn(lost_live), run_time=0.5)
        self.play(w["lost_t"].animate.set_value(1.75), run_time=2.2)

        self.at("about six times")
        y_after = BAR_Y0 + (1.75 / 2.0) * BAR_H
        bx = LOST_X + 0.30
        bracket = VGroup(
            Line([bx - 0.06, y_before, 0], [bx, y_before, 0], color=TEXT, stroke_width=2.5),
            Line([bx, y_before, 0], [bx, y_after, 0], color=TEXT, stroke_width=2.5),
            Line([bx - 0.06, y_after, 0], [bx, y_after, 0], color=TEXT, stroke_width=2.5),
        )
        mult_lbl = T("about × 6", 24, TEXT).move_to([5.58, -0.60, 0])
        self.play(FadeIn(before_lbl), Create(bracket), FadeIn(mult_lbl), run_time=0.9)

        self.at("multiplies the residue")
        self.play(Indicate(mult_lbl, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.finish()


class S10Brake(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.30, dial_val=0.983,
                             show_stations=True, show_dial_pct=False, show_made=True,
                             asbt_open=1.0, cyp_open=1.0,
                             capture_frac=0.983, speed=0.28, make_rate=0.55)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        # Deliberate camera push-in on ileal cell clips peripheral organs at frame edge
        for m in (w["gut"], w["liver"], w["gb"], w["cyp"], w["bsep"], w["ntcp"], w["asbt"]):
            m.layout_ok = "edge"
        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep)

        self.at("How does the liver know")
        zoom_pivot = np.array([-0.55, -0.58, 0.0])
        target_shift = np.array([0.55, 0.58, 0.0])
        self.play(
            FadeOut(w["organ_labels"]), FadeOut(w["ledger"]),
            FadeOut(t_cyp), FadeOut(t_asbt), FadeOut(t_ntcp), FadeOut(t_bsep),
            run_time=0.25,
        )
        self.play(
            w["world"].animate.scale(2.45, about_point=zoom_pivot).shift(target_shift),
            run_time=1.15,
        )

        # Clean zoomed ileal cell overlay (~55% of frame height); FXR sits clear right of portal vein
        ileal_cell = RoundedRectangle(corner_radius=0.28, width=3.8, height=2.9,
                                      stroke_color=GUT_GREY, stroke_width=4.0,
                                      fill_color=GUT_GREY, fill_opacity=0.14).move_to([0.35, 0.45, 0])
        ileal_cell.layout_ok = "straddle"
        cell_lbl = T("ileal cell", 28, TEXT).move_to([-2.75, 1.35, 0])
        asbt_zoom_lbl = T("ASBT", 26, BILE_ORANGE).move_to([1.15, -2.58, 0])
        self.play(FadeIn(ileal_cell), FadeIn(cell_lbl), FadeIn(asbt_zoom_lbl), run_time=0.5)

        self.at("switch on")
        fxr_box = RoundedRectangle(corner_radius=0.16, width=1.25, height=0.68,
                                   stroke_color=FGF_PURPLE, stroke_width=3.5,
                                   fill_color=FGF_PURPLE, fill_opacity=0.28).move_to([0.92, 0.45, 0])
        fxr_lbl = T("FXR", 30, TEXT).move_to([0.92, 0.45, 0])
        self.play(FadeIn(fxr_box), FadeIn(fxr_lbl), run_time=0.6)

        self.at("FGF19")
        fgf_dots, fgf_state = start_fgf19_stream(w["world"], w["paths"], rate=1.5, settle_on_cyp=True)
        fgf_lbl = T("FGF19", 28, FGF_PURPLE).move_to([2.95, 1.45, 0])
        self.play(FadeIn(fgf_lbl), run_time=0.6)

        self.at("reaches the liver")
        self.play(
            FadeOut(ileal_cell), FadeOut(cell_lbl), FadeOut(asbt_zoom_lbl),
            FadeOut(fxr_box), FadeOut(fxr_lbl), FadeOut(fgf_lbl),
            run_time=0.22,
        )
        self.play(
            w["world"].animate.shift(-target_shift).scale(1 / 2.45, about_point=zoom_pivot),
            run_time=0.65,
        )
        self.play(FadeIn(w["organ_labels"]), FadeIn(w["ledger"]),
                  FadeIn(t_cyp), FadeIn(t_asbt), FadeIn(t_ntcp), FadeIn(t_bsep), run_time=0.22)

        self.at("lower CYP7A1")
        cyp_t = ValueTracker(1.0)
        w["cyp"].add_updater(lambda m: set_cyp_valve(m, cyp_t.get_value()))
        w["bile_state"]["make_rate"] = 0.25
        brake_lbl = T("brake", 28, FGF_PURPLE).move_to([-5.08, 1.32, 0])
        self.play(cyp_t.animate.set_value(0.28), FadeIn(brake_lbl), run_time=0.8)
        w["cyp"].clear_updaters()
        self.finish()


class S11Lift(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.30, dial_val=0.983,
                             show_stations=True, show_dial_pct=False, show_made=True,
                             asbt_open=1.0, cyp_open=0.28,
                             capture_frac=0.983, speed=0.28, make_rate=0.25)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        brake_lbl = T("brake", 28, FGF_PURPLE).move_to([-5.08, 1.32, 0])
        fgf_dots, fgf_state = start_fgf19_stream(w["world"], w["paths"], rate=1.4, settle_on_cyp=True)
        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep, brake_lbl)

        self.at("ileal recovery falls")
        asbt_t = ValueTracker(1.0)
        w["asbt"].add_updater(lambda m: set_asbt_opening(m, asbt_t.get_value()))
        w["bile_state"]["capture"] = 0.88
        self.play(w["dial_t"].animate.set_value(0.88), asbt_t.animate.set_value(0.28),
                  w["lost_t"].animate.set_value(1.50), run_time=1.2)
        w["asbt"].clear_updaters()

        self.at("less FGF19")
        fgf_state["rate"] = 0.25
        fgf_state["settle"] = False

        self.at("the brake lifts")
        cyp_t = ValueTracker(0.28)
        w["cyp"].add_updater(lambda m: set_cyp_valve(m, cyp_t.get_value()))
        w["bile_state"]["make_rate"] = 1.15
        self.play(FadeOut(brake_lbl), cyp_t.animate.set_value(1.05),
                  w["made_t"].animate.set_value(1.50), run_time=1.4)
        w["cyp"].clear_updaters()

        self.at("the pool holds")
        ghost_a = build_gallbladder(scale=0.95).set_stroke(BILE_ORANGE, 3).set_fill(BILE_ORANGE, 0.45)
        ghost_a.move_to([-0.25, 0.55, 0])
        lbl_a = T("keeps up", 24, BILE_ORANGE).next_to(ghost_a, UP, buff=0.14)
        self.play(FadeIn(ghost_a), FadeIn(lbl_a), run_time=0.8)

        self.at("settles smaller")
        ghost_b = build_gallbladder(scale=0.95).set_stroke(GOLD, 3).set_fill(GOLD, 0.35)
        ghost_b.move_to([1.28, 0.55, 0])
        lbl_b = T("cannot\nkeep up", 22, GOLD, line_spacing=0.85).next_to(ghost_b, UP, buff=0.12)
        self.play(FadeIn(ghost_b), FadeIn(lbl_b), run_time=0.5)
        w["bile_state"]["pool_scale"] = 0.55
        self.play(ghost_b.animate.scale(0.55), run_time=1.4)
        self.add(scope_tag("schematic").move_to([0.85, -3.28, 0]))
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        w = build_base_world(deliv_val=17.5, lost_val=0.30, made_val=0.30, dial_val=0.983,
                             show_stations=True, show_dial_pct=False, show_made=True,
                             asbt_open=1.0, cyp_open=0.38,
                             capture_frac=0.983, speed=0.28, make_rate=0.50, seed_escape=0.85)
        t_cyp, t_asbt, t_ntcp, t_bsep = station_tags()
        fgf_dots, fgf_state = start_fgf19_stream(w["world"], w["paths"], rate=1.0, settle_on_cyp=True)
        self.add(w["world"], w["organ_labels"], w["ledger"], t_cyp, t_asbt, t_ntcp, t_bsep)

        self.at("not the store")
        duct, gut, portal, liver, _ = w["paths"]
        loop_glow = VMobject(stroke_color=BILE_ORANGE, stroke_width=7, stroke_opacity=0.9)
        loop_glow.set_points(list(duct.get_points()) + list(gut.get_points()) + list(portal.get_points()) + list(liver.get_points()))
        loop_glow.layout_ok = True
        self.play(Create(loop_glow), run_time=1.0)
        self.play(FadeOut(loop_glow), run_time=0.5)

        self.at("tops up what slips past")
        r_cyp = Circle(radius=0.25, color=BILE_ORANGE, stroke_width=4).move_to(PT_CYP + DOWN * 0.04)
        r_out = Circle(radius=0.18, color=BILE_ORANGE, stroke_width=4).move_to(PT_COLON_OUT + LEFT * 0.22)
        self.play(FadeIn(r_cyp), FadeIn(r_out), run_time=0.4)
        self.play(Indicate(r_cyp, scale_factor=1.2), Indicate(r_out, scale_factor=1.2), run_time=0.9)
        self.play(FadeOut(r_cyp), FadeOut(r_out), run_time=0.4)

        self.at("sets the brake")
        fgf_pulse = portal.copy().set_stroke(FGF_PURPLE, width=7, opacity=0.9)
        fgf_pulse.layout_ok = True
        self.play(ShowPassingFlash(fgf_pulse, time_width=0.5), run_time=1.3)
        self.finish()


class S13End(EndCard):
    LINE = "At steady state, the liver remakes only what the gut lets escape."
