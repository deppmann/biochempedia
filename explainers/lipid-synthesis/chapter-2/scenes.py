"""Three Drugs, One Gauge — Lipid Synthesis Chapter 2

COLOUR MAP (one colour per concept, carried across the entire film):
- CHOL_COL   = GOLD (#D4A843)   : cholesterol tokens, ER cholesterol pool, ER gauge arc & "ER cholesterol"
- LDL_COL    = YELLOW (#F5D547) : blood LDL circles & blood-LDL meter
- CELL_COL   = BLUE (#58C4DD)   : liver cell membrane, ER ribbon, Golgi, nucleus, LDL receptor cups, SCAP/SREBP-2
- STATIN_COL = RED (#FC6255)    : statin stop & statin dial tick
- EZET_COL   = ORANGE (#FF9F43) : ezetimibe gate & ezetimibe dial tick
- RESIN_COL  = PURPLE (#A57BFF) : bile-acid resin pill/mesh & resin dial tick
- BILE_COL   = GREEN (#83C167)  : bile acids (droplets & outflow) and positive answer highlight
- PCSK9_COL  = MAGENTA (#E85D9E): PCSK9 secreted tags, PCSK9 nuclear arrow & receptor tagging
- LYSO_COL   = DARK_RED (#D9534F/#5E1D24): lysosome compartment
- STRUCT_COL = GREY (#8B93A1)   : vessel/gut borders, inactive gauge track, reference ticks
- LABEL_COL  = TEXT (#E8EAF0)   : neutral labels, dial needle, question card, merged gauge arrow

CARRIED PICTURE OF THE WORLD:
Left strip: blood channel with drifting YELLOW LDL circles (plus blood-LDL meter on far left in s08-s11).
Upper two-thirds right: schematic liver cell cross-section with LDL receptor cups along the left membrane,
folded ER ribbon and GOLD cholesterol pool around a central half-circle ER cholesterol gauge (no numbers),
lower synthesis pipe with HMG-CoA reductase valve feeding the ER pool, and Golgi / nucleus / lysosome on the right.
Bottom third: horizontal rippling gut band joined to the liver cell by a "from gut" inflow pipe (and "bile acids" outflow in s04-s07, s11).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: LDL circles drift (linear flow + RNG(7)), gut walls ripple (traveling sine wave), GOLD tokens flow through synthesis and gut pipes into ER pool; gauge needle dips 0.74->0.40 and 2 extra cups pop on and retract; 3 drug pills land at sites; dotted arc + "?" link gut pills to receptors.
- s02_statin: Gut dims; RED statin slides into reductase valve, reducing computed downstream token pass rate from 1.0 to 0.15 while upstream tokens queue; ER pool shrinks; gauge needle swings down 1/3 (0.74->0.40) and RED "statin" tick marks dial.
- s03_ezetimibe: Statin lifts out (valve flow -> 1.0); ORANGE ezetimibe forms gate at "from gut" opening, bouncing ~85% of computed gut GOLD tokens onward along gut; ER pool shrinks; gauge swings down (0.74->0.45) and ORANGE "ezetimibe" tick marks dial.
- s04_predict: Orange gate lifts; gauge returns to resting 0.74; "bile acids" pipe opens and GOLD tokens convert to GREEN droplets sliding down; PURPLE resin opens into mesh trapping GREEN droplets along gut; top question card appears.
- s06_resin_answer: "falls" highlights then card dissolves; GOLD->GREEN conversion rate triples, draining ER pool visibly; gauge swings down (0.74->0.35) and PURPLE "resin" tick joins red & orange ticks near low position.
- s07_idea: All 3 drugs sit active at once; 3 coloured arrows trace from sites and merge into 1 white arrow at gauge needle; needle sits low (0.36) and receptor cups grow 3->5; coloured arrows fade leaving only the white gauge arrow.
- s08_receptors: SCAP carries SREBP-2 from ER to Golgi, frees "active SREBP-2" into nucleus; nuclear arrow drives receptor row from 3 to 8 cups; captured LDL circles enter cell at higher rate and computed blood-LDL bar falls (0.85->0.35); clock icon sweeps 360 deg once.
- s09_pcsk9: Second (magenta) arrow leaves nucleus; MAGENTA PCSK9 tags secrete into blood; one receptor cup captures LDL in an inward pocket, gets clipped by a PCSK9 tag, and travels into the new dark-red lysosome where it fades.
- s10_brake: Statin returns to valve with gauge low (0.35); 2 of 8 cups are carried by PCSK9 tags to lysosome (6 remain); blood-LDL bar drifts partially up (0.35->0.50, below 0.85 start); both nuclear arrows pulse together.
- s11_return: Three drug sites pulse in turn on their cues; GOLD tokens drain from ER pool as gauge needle falls (0.72->0.34); receptor row grows 6->8 and LDL circles stream inside, dropping blood-LDL bar (0.50->0.34).
"""
from bp_parts import *

# ------------------------------------------------------------------ Palette
CHOL_COL = GOLD
LDL_COL = YELLOW
CELL_COL = BLUE
STATIN_COL = RED
EZET_COL = "#FF9F43"
RESIN_COL = "#A57BFF"
BILE_COL = GREEN
PCSK9_COL = "#E85D9E"
LYSO_FILL = "#5E1D24"
LYSO_STROKE = "#D9534F"
STRUCT_COL = GREY
LABEL_COL = TEXT

# ------------------------------------------------------------------ Fixed Coordinates
BLOOD_X0, BLOOD_X1 = -5.60, -4.15
CELL_X0, CELL_X1 = -4.15, 6.20
CELL_Y0, CELL_Y1 = -1.14, 2.86

GUT_X0, GUT_X1 = -6.25, 6.25
GUT_Y0, GUT_Y1 = -3.05, -1.80
GUT_MID_Y = (GUT_Y0 + GUT_Y1) / 2

GUT_PIPE_X = -0.55
BILE_PIPE_X = 1.45
VALVE_PT = np.array([-2.55, -0.52, 0.0])
DIAL_CENTER = np.array([0.85, 0.98, 0.0])
DIAL_R = 0.85
ER_POOL_CENTER = np.array([-1.75, 1.24, 0.0])
GOLGI_PT = np.array([3.20, 1.52, 0.0])
NUCLEUS_PT = np.array([5.15, 1.50, 0.0])
NUCLEUS_R = 0.72
LYSO_PT = np.array([5.15, -0.18, 0.0])
LYSO_R = 0.44
METER_X = -6.20
METER_Y0, METER_Y1 = -0.85, 1.90


def _rounded_cell_outline(x0, x1, y0, y1, r=0.28):
    """Build liver cell perimeter as a VMobject (not RoundedRectangle) so layout_check treats it as biology, not a UI panel."""
    pts = []
    corners = [
        (x1 - r, y1 - r, 0, PI / 2),
        (x0 + r, y1 - r, PI / 2, PI),
        (x0 + r, y0 + r, PI, 3 * PI / 2),
        (x1 - r, y0 + r, 3 * PI / 2, TAU),
    ]
    for cx, cy, a0, a1 in corners:
        for a in np.linspace(a0, a1, 8):
            pts.append([cx + r * np.cos(a), cy + r * np.sin(a), 0.0])
    pts.append(pts[0])
    m = VMobject(stroke_color=CELL_COL, stroke_width=3.5, fill_color=CELL_COL, fill_opacity=0.07)
    m.set_points_as_corners(pts)
    return m


def _er_ribbon():
    """Schematic ER compartment around cholesterol pool & central gauge (open central window for dial & labels)."""
    bx0, bx1, by0, by1, br = -2.25, 2.02, 0.36, 2.26, 0.22
    bpts = []
    for cx, cy, a0, a1 in [(bx1 - br, by1 - br, 0, PI / 2), (bx0 + br, by1 - br, PI / 2, PI),
                           (bx0 + br, by0 + br, PI, 3 * PI / 2), (bx1 - br, by0 + br, 3 * PI / 2, TAU)]:
        for a in np.linspace(a0, a1, 6):
            bpts.append([cx + br * np.cos(a), cy + br * np.sin(a), 0.0])
    bpts.append(bpts[0])
    er_bg = VMobject(stroke_color=CELL_COL, stroke_width=2.5, stroke_opacity=0.55,
                     fill_color=CELL_COL, fill_opacity=0.09)
    er_bg.set_points_as_corners(bpts)

    # Folded ER cisternae accent waves strictly in corners clear of pool, dial, and tick labels
    left_wave = VMobject(stroke_color=CELL_COL, stroke_width=2.4, stroke_opacity=0.50)
    left_wave.set_points_smoothly([
        np.array([-2.14, 1.80, 0.0]),
        np.array([-1.96, 2.12, 0.0]),
        np.array([-1.77, 1.82, 0.0]),
        np.array([-1.58, 2.12, 0.0]),
    ])
    right_wave = VMobject(stroke_color=CELL_COL, stroke_width=2.4, stroke_opacity=0.50)
    right_wave.set_points_smoothly([
        np.array([1.72, 2.08, 0.0]),
        np.array([1.92, 1.75, 0.0]),
        np.array([1.72, 1.42, 0.0]),
        np.array([1.92, 1.12, 0.0]),
    ])
    return VGroup(er_bg, left_wave, right_wave)


def _cup_shape(y_pos, scale=1.0, color=CELL_COL):
    """A single LDL receptor cup on the left membrane (x = CELL_X0), opening leftward into blood."""
    s = 0.15 * scale
    pts = [
        np.array([CELL_X0 - 0.17 * scale, y_pos + s, 0.0]),
        np.array([CELL_X0 - 0.02, y_pos + 0.55 * s, 0.0]),
        np.array([CELL_X0 + 0.14 * scale, y_pos, 0.0]),
        np.array([CELL_X0 - 0.02, y_pos - 0.55 * s, 0.0]),
        np.array([CELL_X0 - 0.17 * scale, y_pos - s, 0.0]),
    ]
    stem = Line([CELL_X0, y_pos, 0], [CELL_X0 + 0.25 * scale, y_pos, 0], color=color, stroke_width=3.5)
    cup = VMobject(stroke_color=color, stroke_width=4.0, fill_opacity=0)
    cup.set_points_as_corners(pts)
    return VGroup(stem, cup)


def _cup_ys(n):
    """Evenly spaced y positions for n receptor cups along the left membrane (below 'LDL receptors' label)."""
    if n <= 0:
        return []
    lo, hi = -0.78, 1.98
    if n == 1:
        return [(lo + hi) / 2]
    if n <= 4:
        span = 0.65 * (n - 1)
        mid = 0.60
        return list(np.linspace(mid - span / 2, mid + span / 2, n))
    return list(np.linspace(lo, hi, n))


def _pill(text, color, size=24, pad=0.19):
    """A compact drug pill/badge built with boxed_label (pad=0.19 prevents corner overflow)."""
    return boxed_label(text, color=color, size=size, pad=pad, stroke=2.5, fill_opacity=0.22, corner_radius=0.12)


def _golgi_stack():
    """Small schematic 3-cisterna Golgi stack at GOLGI_PT."""
    g = VGroup()
    for dy, w in [(-0.24, 0.68), (0.0, 0.88), (0.24, 0.64)]:
        c = RoundedRectangle(corner_radius=0.08, width=w, height=0.15,
                             stroke_color=CELL_COL, stroke_width=2.5, fill_color=CELL_COL, fill_opacity=0.18)
        c.move_to(GOLGI_PT + UP * dy)
        g.add(c)
    return g


def _resin_mesh():
    """Purple trapping mesh in the gut band (x in [1.45, 3.35], y in [-2.86, -1.98])."""
    x0, x1, y0, y1 = 1.45, 3.35, -2.86, -1.98
    frame = RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=y1 - y0,
                             stroke_color=RESIN_COL, stroke_width=3.0, fill_color=RESIN_COL, fill_opacity=0.14)
    frame.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    lines = VGroup()
    for x in np.linspace(x0 + 0.25, x1 - 0.25, 5):
        lines.add(Line([x, y0 + 0.05, 0], [x, y1 - 0.05, 0], stroke_color=RESIN_COL, stroke_width=1.8, stroke_opacity=0.7))
    for y in np.linspace(y0 + 0.22, y1 - 0.22, 3):
        lines.add(Line([x0 + 0.05, y, 0], [x1 - 0.05, y, 0], stroke_color=RESIN_COL, stroke_width=1.8, stroke_opacity=0.7))
    return VGroup(frame, lines)


def _resin_badge_below():
    """Place the 'resin' label cleanly below the gut mesh so moving gut particles never cross its text."""
    lab = boxed_label("resin", RESIN_COL, size=24, pad=0.14, fill_opacity=0.22, corner_radius=0.12).move_to([2.40, -3.52, 0])
    stem = Line([2.40, -2.88, 0], lab.get_top() + UP * 0.04, color=RESIN_COL, stroke_width=2.2)
    return VGroup(stem, lab)


def _dial_tick(val, color, label_text, label_pos):
    """A coloured radial tick on the ER gauge rim + fanned label with short leader line."""
    ang = PI - PI * float(np.clip(val, 0.02, 0.98))
    u = np.array([np.cos(ang), np.sin(ang), 0.0])
    p_in = DIAL_CENTER + (DIAL_R - 0.13) * u
    p_out = DIAL_CENTER + (DIAL_R + 0.13) * u
    tick = Line(p_in, p_out, color=color, stroke_width=5)
    lab = T(label_text, size=24, color=color).move_to(np.array(label_pos, dtype=float))
    target = lab.get_right() + RIGHT * 0.10 if lab.get_center()[0] < p_out[0] else lab.get_left() + LEFT * 0.10
    leader = Line(p_out, target, color=color, stroke_width=2.0, stroke_opacity=0.85)
    return VGroup(tick, leader, lab)


TICK_POS = {
    "ezetimibe": [-0.68, 1.92, 0.0],
    "statin": [-0.72, 1.48, 0.0],
    "resin": [-0.72, 1.04, 0.0],
}


def _nuc_arrow_mob():
    """Arrow from nucleus to surface receptor row, routed cleanly above 'LDL receptors' at y = 2.68."""
    path = VMobject(stroke_color=CELL_COL, stroke_width=4.0)
    path.set_points_as_corners([
        [NUCLEUS_PT[0] - 0.52, NUCLEUS_PT[1] + 0.54, 0],
        [NUCLEUS_PT[0] - 0.52, 2.68, 0],
        [-3.95, 2.68, 0],
        [-3.95, 2.22, 0],
    ])
    tip = Arrow([-3.95, 2.55, 0], [-3.95, 2.16, 0], buff=0, color=CELL_COL, stroke_width=4, tip_length=0.20)
    return VGroup(path, tip)


def _pcsk9_arrow_mob():
    """Magenta arrow from nucleus to surface, routed at y = 0.26 between ER bottom (0.36) and statin pill (<= 0.13)."""
    path = VMobject(stroke_color=PCSK9_COL, stroke_width=3.8)
    path.set_points_smoothly([
        NUCLEUS_PT + np.array([-0.64, -0.36, 0.0]),
        np.array([3.65, 0.26, 0.0]),
        np.array([0.80, 0.26, 0.0]),
        np.array([-2.20, 0.26, 0.0]),
        np.array([-3.75, 0.26, 0.0]),
    ])
    tip = Arrow([-3.35, 0.26, 0], [-3.85, 0.26, 0], buff=0, color=PCSK9_COL, stroke_width=3.8, tip_length=0.18)
    return VGroup(path, tip)


class WorldState:
    """Holds all shared trackers and dynamic builders for the carried world across scenes."""

    def __init__(self, gauge=0.74, cups=3, valve_open=1.0, gut_open=1.0, er_pool=1.0,
                 gut_dim=1.0, show_bile=False, resin_mesh=False, ldl_level=0.85,
                 show_meter=False, uptake_rate=0.0, bile_rate=0.25, show_golgi=False,
                 show_lyso=False, pcsk9_in_blood=False, gut_lane_y=-2.14, seed=7):
        self.sim_t = ValueTracker(0.0)
        self.gauge = ValueTracker(gauge)
        self.cups_n = ValueTracker(cups)
        self.valve_open = ValueTracker(valve_open)
        self.gut_open = ValueTracker(gut_open)
        self.er_pool = ValueTracker(er_pool)
        self.gut_dim = ValueTracker(gut_dim)
        self.ldl_level = ValueTracker(ldl_level)
        self.uptake_rate = ValueTracker(uptake_rate)
        self.bile_rate = ValueTracker(bile_rate)
        self.show_bile = show_bile
        self.resin_mesh_on = resin_mesh
        self.show_meter = show_meter
        self.show_golgi = show_golgi
        self.show_lyso = show_lyso
        self.pcsk9_in_blood = pcsk9_in_blood
        self.gut_lane_y = gut_lane_y
        self.rng = np.random.default_rng(seed)

    def advance(self, mob, dt):
        self.sim_t.increment_value(dt)

    def build(self, top_labels=True):
        """Construct the full carried world VGroup with live always_redraw process layers."""
        root = VGroup()

        driver = Dot(radius=0.001).set_opacity(0).move_to([0, 0, 0])
        driver.add_updater(self.advance)
        root.add(driver)

        # 1. Blood channel (left strip)
        blood_bg = Rectangle(width=BLOOD_X1 - BLOOD_X0, height=CELL_Y1 - CELL_Y0,
                             stroke_width=0, fill_color=LDL_COL, fill_opacity=0.05)
        blood_bg.move_to([(BLOOD_X0 + BLOOD_X1) / 2, (CELL_Y0 + CELL_Y1) / 2, 0])
        blood_left = Line([BLOOD_X0, CELL_Y0, 0], [BLOOD_X0, CELL_Y1, 0], color=STRUCT_COL, stroke_width=3)
        root.add(blood_bg, blood_left)

        # 2. Liver cell cross-section + ER ribbon + nucleus + synthesis pipe
        cell_wall = _rounded_cell_outline(CELL_X0, CELL_X1, CELL_Y0, CELL_Y1)
        er_rib = _er_ribbon()
        er_label = T("ER", size=24, color=CELL_COL).move_to([0.85, 2.44, 0])
        rec_label = T("LDL receptors", size=24, color=CELL_COL).move_to([-2.78, 2.40, 0])

        # Lower synthesis pipe: x from -3.55 to -1.55 at y = -0.52, then turns up into ER bottom (y = 0.36)
        synth_top = Line([-3.55, -0.39, 0], [-1.68, -0.39, 0], color=STRUCT_COL, stroke_width=2.5)
        synth_bot = Line([-3.55, -0.65, 0], [-1.42, -0.65, 0], color=STRUCT_COL, stroke_width=2.5)
        synth_up_l = Line([-1.68, -0.39, 0], [-1.68, 0.36, 0], color=STRUCT_COL, stroke_width=2.5)
        synth_up_r = Line([-1.42, -0.65, 0], [-1.42, 0.36, 0], color=STRUCT_COL, stroke_width=2.5)
        valve_top = Polygon([-2.72, -0.35, 0], [-2.38, -0.35, 0], [-2.55, -0.45, 0],
                            stroke_color=CELL_COL, stroke_width=2, fill_color=CELL_COL, fill_opacity=0.35)
        valve_bot = Polygon([-2.72, -0.69, 0], [-2.38, -0.69, 0], [-2.55, -0.59, 0],
                            stroke_color=CELL_COL, stroke_width=2, fill_color=CELL_COL, fill_opacity=0.35)
        valve_label = T("HMG-CoA reductase", size=24, color=LABEL_COL).move_to([-2.28, -0.92, 0])
        synth_grp = VGroup(synth_top, synth_bot, synth_up_l, synth_up_r, valve_top, valve_bot, valve_label)

        # Nucleus on cell's right
        nuc = Circle(radius=NUCLEUS_R, stroke_color=CELL_COL, stroke_width=3,
                     fill_color=CELL_COL, fill_opacity=0.14).move_to(NUCLEUS_PT)
        nuc_label = T("nucleus", size=24, color=CELL_COL).move_to(NUCLEUS_PT)
        root.add(cell_wall, er_rib, er_label, rec_label, synth_grp, nuc, nuc_label)

        if self.show_golgi:
            golgi = _golgi_stack()
            golgi_lab = T("Golgi", size=24, color=CELL_COL).move_to(GOLGI_PT + UP * 0.62)
            root.add(golgi, golgi_lab)

        if self.show_lyso:
            lyso = Circle(radius=LYSO_R, stroke_color=LYSO_STROKE, stroke_width=3.5,
                          fill_color=LYSO_FILL, fill_opacity=0.85).move_to(LYSO_PT)
            lyso_lab = T("lysosome", size=24, color=LABEL_COL).move_to(LYSO_PT + DOWN * 0.68)
            root.add(lyso, lyso_lab)

        # 3. ER Cholesterol Gauge (schematic half-circle dial, NO numbers)
        track = Arc(radius=DIAL_R, start_angle=PI, angle=-PI, arc_center=DIAL_CENTER,
                    stroke_color=STRUCT_COL, stroke_width=10)
        dial_arc = always_redraw(lambda: Arc(
            radius=DIAL_R, start_angle=PI,
            angle=-PI * float(np.clip(self.gauge.get_value(), 0.02, 0.98)),
            arc_center=DIAL_CENTER, stroke_color=CHOL_COL, stroke_width=10))
        dial_needle = always_redraw(lambda: Line(
            DIAL_CENTER,
            DIAL_CENTER + 0.78 * DIAL_R * np.array([
                np.cos(PI - PI * float(np.clip(self.gauge.get_value(), 0.02, 0.98))),
                np.sin(PI - PI * float(np.clip(self.gauge.get_value(), 0.02, 0.98))),
                0.0
            ]),
            color=LABEL_COL, stroke_width=5))
        dial_hub = Dot(DIAL_CENTER, radius=0.07, color=LABEL_COL)
        dial_lab = T("ER cholesterol", size=24, color=CHOL_COL).move_to(DIAL_CENTER + DOWN * 0.36)
        root.add(track, dial_arc, dial_needle, dial_hub, dial_lab)

        # 4. Dynamic ER cholesterol pool
        pool_offsets = self.rng.uniform([-0.32, -0.30], [0.32, 0.30], size=(14, 2))

        def _draw_pool():
            lvl = float(np.clip(self.er_pool.get_value(), 0.15, 1.0))
            n_show = max(2, int(round(lvl * len(pool_offsets))))
            t = self.sim_t.get_value()
            g = VGroup()
            for i in range(n_show):
                dx, dy = pool_offsets[i]
                jx = 0.025 * np.sin(1.7 * t + i * 1.1)
                jy = 0.025 * np.cos(1.4 * t + i * 0.9)
                g.add(Dot(ER_POOL_CENTER + np.array([dx + jx, dy + jy, 0]),
                          radius=0.068, color=CHOL_COL, fill_opacity=0.92))
            return g

        root.add(always_redraw(_draw_pool))

        # 5. Receptor cups on left cell membrane
        def _draw_cups():
            n = int(round(self.cups_n.get_value()))
            return VGroup(*[_cup_shape(y) for y in _cup_ys(n)])

        root.add(always_redraw(_draw_cups))

        # 6. From-gut pipe (at x = -0.55, label on right) + optional Bile-acids pipe (x = 1.45)
        gp_l = Line([GUT_PIPE_X - 0.13, GUT_Y1, 0], [GUT_PIPE_X - 0.13, CELL_Y0, 0], color=STRUCT_COL, stroke_width=2.5)
        gp_r = Line([GUT_PIPE_X + 0.13, GUT_Y1, 0], [GUT_PIPE_X + 0.13, CELL_Y0, 0], color=STRUCT_COL, stroke_width=2.5)
        gp_lab = T("from gut", size=24, color=CHOL_COL).move_to([GUT_PIPE_X + 1.02, (GUT_Y1 + CELL_Y0) / 2, 0])
        root.add(gp_l, gp_r, gp_lab)

        if self.show_bile:
            bp_l = Line([BILE_PIPE_X - 0.10, CELL_Y0, 0], [BILE_PIPE_X - 0.10, GUT_Y1, 0], color=BILE_COL, stroke_width=2.5)
            bp_r = Line([BILE_PIPE_X + 0.10, CELL_Y0, 0], [BILE_PIPE_X + 0.10, GUT_Y1, 0], color=BILE_COL, stroke_width=2.5)
            bp_lab = T("bile acids", size=24, color=BILE_COL).move_to([BILE_PIPE_X + 0.96, (GUT_Y1 + CELL_Y0) / 2, 0])
            root.add(bp_l, bp_r, bp_lab)

        # 7. Gut band with peristaltic sine walls
        def _draw_gut():
            t = self.sim_t.get_value()
            op = float(np.clip(self.gut_dim.get_value(), 0.25, 1.0))
            xs = np.linspace(GUT_X0, GUT_X1, 64)
            top_pts = [np.array([x, GUT_Y1 + 0.05 * np.sin(2.1 * x - 1.8 * t), 0.0]) for x in xs]
            bot_pts = [np.array([x, GUT_Y0 - 0.05 * np.sin(2.1 * x - 1.8 * t + 0.8), 0.0]) for x in xs]
            top_line = VMobject(stroke_color=STRUCT_COL, stroke_width=3.0, stroke_opacity=op).set_points_smoothly(top_pts)
            bot_line = VMobject(stroke_color=STRUCT_COL, stroke_width=3.0, stroke_opacity=op).set_points_smoothly(bot_pts)
            fill_pts = top_pts + list(reversed(bot_pts)) + [top_pts[0]]
            fill_poly = VMobject(stroke_width=0, fill_color=STRUCT_COL, fill_opacity=0.09 * op).set_points_as_corners(fill_pts)
            return VGroup(fill_poly, top_line, bot_line)

        gut_mob = always_redraw(_draw_gut)
        gut_lab = T("gut", size=28, color=LABEL_COL).move_to([-5.65, GUT_MID_Y, 0])
        root.add(gut_mob, gut_lab)

        if self.resin_mesh_on:
            root.add(_resin_mesh(), _resin_badge_below())

        # 8. Live computed particles
        ldl_phases = np.linspace(0.0, 1.0, 10, endpoint=False)
        ldl_xoff = self.rng.uniform(-0.38, 0.28, size=10)

        def _draw_particles():
            t = self.sim_t.get_value()
            g = VGroup()

            # (a) Blood LDL circles
            up_r = float(self.uptake_rate.get_value())
            for i, ph in enumerate(ldl_phases):
                u = (ph + 0.14 * t) % 1.0
                y = CELL_Y1 - 0.18 - u * (CELL_Y1 - CELL_Y0 - 0.36)
                x = (BLOOD_X0 + BLOOD_X1) / 2 + ldl_xoff[i]
                if up_r > 0.05 and (i % 3 == 0 or (up_r > 0.5 and i % 2 == 0)):
                    if 0.30 < u < 0.72:
                        frac = (u - 0.30) / 0.42
                        x = (CELL_X0 - 0.32) + frac * 1.05
                        op = 1.0 - max(0.0, (frac - 0.6) / 0.4)
                        g.add(Dot([x, y, 0], radius=0.105, color=LDL_COL, fill_opacity=0.9 * op))
                        continue
                g.add(Dot([x, y, 0], radius=0.11, color=LDL_COL, fill_opacity=0.92))

            if self.pcsk9_in_blood:
                for i in range(3):
                    u = (0.18 + i * 0.33 + 0.10 * t) % 1.0
                    py = CELL_Y1 - 0.28 - u * (CELL_Y1 - CELL_Y0 - 0.56)
                    px = BLOOD_X1 - 0.24 - 0.18 * (i % 2)
                    tag = RegularPolygon(4, radius=0.075, color=PCSK9_COL, fill_color=PCSK9_COL, fill_opacity=0.55)
                    tag.move_to([px, py, 0])
                    g.add(tag)

            # (b) Synthesis pipe GOLD tokens (x from -3.45 to -1.55 at y = -0.52, then up to y = 0.42)
            v_open = float(self.valve_open.get_value())
            for i in range(6):
                u = (i / 6.0 + 0.22 * t) % 1.0
                if v_open < 0.4:
                    if i < 4:
                        qx = -3.35 + 0.19 * i + 0.015 * np.sin(3 * t + i)
                        qy = -0.52 + 0.03 * np.cos(2.5 * t + i)
                        g.add(Dot([qx, qy, 0], radius=0.065, color=CHOL_COL, fill_opacity=0.95))
                    else:
                        su = ((i - 4) * 0.5 + 0.12 * t) % 1.0
                        if su < 0.55:
                            px = -2.25 + (su / 0.55) * 0.70
                            py = -0.52
                        else:
                            px = -1.55
                            py = -0.52 + ((su - 0.55) / 0.45) * 0.85
                        g.add(Dot([px, py, 0], radius=0.055, color=CHOL_COL, fill_opacity=0.75))
                else:
                    if u < 0.70:
                        px = -3.45 + (u / 0.70) * 1.90
                        py = -0.52
                    else:
                        px = -1.55
                        py = -0.52 + ((u - 0.70) / 0.30) * 0.85
                    g.add(Dot([px, py, 0], radius=0.065, color=CHOL_COL, fill_opacity=0.95))

            # (c) Gut GOLD tokens (upper lane y = self.gut_lane_y)
            g_open = float(self.gut_open.get_value())
            g_op = float(np.clip(self.gut_dim.get_value(), 0.25, 1.0))
            base_y = self.gut_lane_y
            for i in range(7):
                u = (i / 7.0 + 0.13 * t) % 1.0
                gx = -4.65 + u * 10.2
                gy = base_y + 0.06 * np.sin(i * 1.9)
                if i in (0, 2, 4) and (GUT_PIPE_X - 0.20) < gx < (GUT_PIPE_X + 1.05):
                    frac = (gx - (GUT_PIPE_X - 0.20)) / 1.25
                    if g_open > 0.5:
                        px = GUT_PIPE_X
                        py = base_y + frac * (0.36 - base_y)
                        g.add(Dot([px, py, 0], radius=0.065, color=CHOL_COL, fill_opacity=0.95 * g_op))
                        continue
                    elif i in (0, 2):
                        if frac < 0.45:
                            px = GUT_PIPE_X - 0.12 * (0.45 - frac)
                            py = base_y + (frac / 0.45) * (GUT_Y1 - 0.10 - base_y)
                        else:
                            bf = (frac - 0.45) / 0.55
                            px = GUT_PIPE_X + bf * 1.15
                            py = (GUT_Y1 - 0.10) - bf * ((GUT_Y1 - 0.10) - base_y)
                        g.add(Dot([px, py, 0], radius=0.065, color=CHOL_COL, fill_opacity=0.95 * g_op))
                        continue
                    else:
                        px = GUT_PIPE_X
                        py = base_y + frac * (0.36 - base_y)
                        g.add(Dot([px, py, 0], radius=0.055, color=CHOL_COL, fill_opacity=0.75 * g_op))
                        continue
                g.add(Dot([gx, gy, 0], radius=0.065, color=CHOL_COL, fill_opacity=0.90 * g_op))

            # (d) Bile-acid GREEN droplets
            if self.show_bile:
                br = float(self.bile_rate.get_value())
                n_bile = 5 if br > 0.5 else 3
                speed = 0.24 if br > 0.5 else 0.14
                for i in range(n_bile):
                    u = (i / float(n_bile) + speed * t) % 1.0
                    if u < 0.48:
                        f = u / 0.48
                        if f < 0.45:
                            bx = -0.35 + (f / 0.45) * (BILE_PIPE_X + 0.35)
                            by = 0.36 - (f / 0.45) * (0.36 - (CELL_Y0 + 0.15))
                        else:
                            sf = (f - 0.45) / 0.55
                            bx = BILE_PIPE_X
                            by = (CELL_Y0 + 0.15) - sf * ((CELL_Y0 + 0.15) - GUT_MID_Y)
                    else:
                        f = (u - 0.48) / 0.52
                        if self.resin_mesh_on:
                            bx = BILE_PIPE_X + f * 4.0
                            by = GUT_MID_Y + 0.16 * np.sin(i * 2.1)
                        else:
                            bx = BILE_PIPE_X + f * 1.4
                            by = GUT_MID_Y - 0.10 * np.sin(f * PI)
                    g.add(Dot([bx, by, 0], radius=0.075, color=BILE_COL, fill_opacity=0.95))

            return g

        root.add(always_redraw(_draw_particles))

        # 9. Optional Blood-LDL meter (far left, clear of blood channel wall)
        if self.show_meter:
            m_frame = Rectangle(width=0.24, height=METER_Y1 - METER_Y0, stroke_color=STRUCT_COL, stroke_width=2.5,
                                fill_color=BG, fill_opacity=0.8).move_to([METER_X, (METER_Y0 + METER_Y1) / 2, 0])
            m_fill = always_redraw(lambda: Rectangle(
                width=0.18,
                height=max(0.06, float(np.clip(self.ldl_level.get_value(), 0.02, 1.0)) * (METER_Y1 - METER_Y0 - 0.06)),
                stroke_width=0, fill_color=LDL_COL, fill_opacity=0.88,
            ).move_to([
                METER_X,
                METER_Y0 + 0.03 + max(0.06, float(np.clip(self.ldl_level.get_value(), 0.02, 1.0)) * (METER_Y1 - METER_Y0 - 0.06)) / 2,
                0,
            ]))
            m_lab = T("blood\nLDL", size=24, color=LDL_COL, line_spacing=0.85).move_to([METER_X + 0.02, METER_Y1 + 0.48, 0])
            root.add(m_frame, m_fill, m_lab)

        # 10. Top labels & schematic tag
        if top_labels:
            blood_lab = T("blood", size=26, color=LDL_COL).move_to([(BLOOD_X0 + BLOOD_X1) / 2, 3.16, 0])
            cell_lab = T("liver cell", size=28, color=CELL_COL).move_to([1.10, 3.16, 0])
            root.add(blood_lab, cell_lab)
            root.top_labels = VGroup(blood_lab, cell_lab)
        else:
            root.top_labels = VGroup()

        root.scope = scope_tag("schematic")
        root.add(root.scope)
        return root


# ==================================================================
# SCENES
# ==================================================================

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.74, cups=3, valve_open=1.0, gut_open=1.0, er_pool=0.90, gut_lane_y=-2.08)
        world = ws.build()
        self.add(world)

        self.at("reading falls")
        self.play(ws.gauge.animate.set_value(0.40), run_time=0.7)

        self.at("makes more LDL")
        self.play(ws.cups_n.animate.set_value(5), run_time=0.6)
        self.wait(0.8)
        self.play(ws.cups_n.animate.set_value(3), ws.gauge.animate.set_value(0.74), run_time=0.7)

        self.at("three drugs")
        statin_pill = _pill("statin", STATIN_COL, pad=0.14).move_to([-2.95, -0.04, 0])
        ezet_pill = _pill("ezetimibe", EZET_COL).move_to([-2.45, -2.62, 0])
        resin_pill = _pill("resin", RESIN_COL).move_to([2.40, -2.62, 0])
        self.play(FadeIn(statin_pill, shift=DOWN * 0.2),
                  FadeIn(ezet_pill, shift=DOWN * 0.2),
                  FadeIn(resin_pill, shift=DOWN * 0.2), run_time=0.6)

        self.at("statin blocks")
        red_stop = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.28,
                                    stroke_color=STATIN_COL, stroke_width=2.5,
                                    fill_color=STATIN_COL, fill_opacity=0.85).move_to(VALVE_PT)
        self.play(
            statin_pill.animate.move_to([-2.55, -0.04, 0]),
            FadeIn(red_stop),
            ws.valve_open.animate.set_value(0.15),
            run_time=0.6,
        )

        self.at("other two act")
        self.play(Indicate(ezet_pill, color=EZET_COL), Indicate(resin_pill, color=RESIN_COL), run_time=0.7)

        self.at("How can a drug")
        # Route arcs cleanly left of "HMG-CoA reductase" (left edge ~ -3.40) and below "from gut" ([+0.25, -1.47])
        arc1 = DashedVMobject(VMobject().set_points_smoothly([
            np.array([-2.45, -1.92, 0.0]),
            np.array([-3.75, -1.48, 0.0]),
            np.array([-3.92, -0.82, 0.0]),
            np.array([-3.92, 0.16, 0.0]),
        ]), num_dashes=16, dashed_ratio=0.55).set_stroke(LABEL_COL, 3.2)
        arc2 = DashedVMobject(VMobject().set_points_smoothly([
            np.array([2.40, -1.92, 0.0]),
            np.array([0.55, -1.72, 0.0]),
            np.array([-2.65, -1.72, 0.0]),
            np.array([-3.92, -1.42, 0.0]),
            np.array([-3.95, 0.08, 0.0]),
        ]), num_dashes=28, dashed_ratio=0.55).set_stroke(LABEL_COL, 3.2)
        qmark = T("?", size=44, color=LABEL_COL, weight=BOLD).move_to([-3.12, -1.44, 0])
        self.play(Create(arc1), Create(arc2), FadeIn(qmark, scale=1.2), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Lipid Synthesis: Building Cholesterol from Acetyl-CoA"
    TITLE = "Three Drugs, One Gauge"


class S02Statin(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.74, cups=3, valve_open=1.0, gut_open=1.0, er_pool=0.95, gut_dim=0.35)
        world = ws.build()
        statin_pill = _pill("statin", STATIN_COL, pad=0.14).move_to([-2.55, -0.04, 0])
        red_stop = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.28,
                                    stroke_color=STATIN_COL, stroke_width=2.5,
                                    fill_color=STATIN_COL, fill_opacity=0.85).move_to(VALVE_PT + RIGHT * 0.45)
        self.add(world, statin_pill, red_stop)

        self.at("statin blocks")
        self.play(
            red_stop.animate.move_to(VALVE_PT),
            ws.valve_open.animate.set_value(0.15),
            run_time=0.8,
        )

        self.at("Less new cholesterol")
        self.play(ws.er_pool.animate.set_value(0.55), run_time=1.0)

        self.at("gauge reads low")
        tick_statin = _dial_tick(0.40, STATIN_COL, "statin", TICK_POS["statin"])
        self.play(ws.gauge.animate.set_value(0.40), FadeIn(tick_statin), run_time=0.9)
        self.finish()


class S03Ezetimibe(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.74, cups=3, valve_open=0.15, gut_open=1.0, er_pool=0.95,
                        gut_dim=1.0, gut_lane_y=-2.10)
        world = ws.build()
        red_stop = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.28,
                                    stroke_color=STATIN_COL, stroke_width=2.5,
                                    fill_color=STATIN_COL, fill_opacity=0.85).move_to(VALVE_PT)
        statin_pill = _pill("statin", STATIN_COL, pad=0.14).move_to([-2.55, -0.04, 0])
        tick_statin = _dial_tick(0.40, STATIN_COL, "statin", TICK_POS["statin"])
        tick_statin[0].set_opacity(0.45)
        tick_statin[1].set_opacity(0.45)
        ezet_pill = _pill("ezetimibe", EZET_COL).move_to([-2.45, -2.62, 0])
        self.add(world, red_stop, statin_pill, tick_statin, ezet_pill)

        self.play(
            FadeOut(red_stop, shift=LEFT * 0.3),
            FadeOut(statin_pill, shift=LEFT * 0.3),
            ws.valve_open.animate.set_value(1.0),
            run_time=0.7,
        )

        self.at("blocks cholesterol", lead=0.45)
        gate = RoundedRectangle(corner_radius=0.04, width=0.38, height=0.16,
                                stroke_color=EZET_COL, stroke_width=2.5,
                                fill_color=EZET_COL, fill_opacity=0.90).move_to([GUT_PIPE_X, GUT_Y1, 0])
        stem = Line(ezet_pill.get_right() + RIGHT * 0.06, [GUT_PIPE_X - 0.14, GUT_Y1 - 0.10, 0],
                    color=EZET_COL, stroke_width=2.2)
        self.play(FadeIn(gate), Create(stem), ws.gut_open.animate.set_value(0.15), run_time=0.7)

        self.at("less arrives")
        self.play(ws.er_pool.animate.set_value(0.58), run_time=0.9)

        self.at("ER reading drops")
        tick_ezet = _dial_tick(0.45, EZET_COL, "ezetimibe", TICK_POS["ezetimibe"])
        self.play(ws.gauge.animate.set_value(0.45), FadeIn(tick_ezet), run_time=0.9)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.45, cups=3, valve_open=1.0, gut_open=0.15, er_pool=0.85,
                        gut_dim=1.0, show_bile=False, resin_mesh=False, bile_rate=0.25, gut_lane_y=-2.10)
        world = ws.build()
        tick_statin = _dial_tick(0.40, STATIN_COL, "statin", TICK_POS["statin"])
        tick_ezet = _dial_tick(0.45, EZET_COL, "ezetimibe", TICK_POS["ezetimibe"])
        for tk in (tick_statin, tick_ezet):
            tk[0].set_opacity(0.45)
            tk[1].set_opacity(0.45)
        gate = RoundedRectangle(corner_radius=0.04, width=0.38, height=0.16,
                                stroke_color=EZET_COL, stroke_width=2.5,
                                fill_color=EZET_COL, fill_opacity=0.90).move_to([GUT_PIPE_X, GUT_Y1, 0])
        ezet_pill = _pill("ezetimibe", EZET_COL).move_to([-2.45, -2.62, 0])
        resin_pill = _pill("resin", RESIN_COL, pad=0.14).move_to([2.40, -3.52, 0])
        self.add(world, tick_statin, tick_ezet, gate, ezet_pill, resin_pill)

        self.play(
            FadeOut(gate, shift=UP * 0.25),
            FadeOut(ezet_pill, shift=DOWN * 0.2),
            ws.gut_open.animate.set_value(1.0),
            ws.gauge.animate.set_value(0.74),
            run_time=0.8,
        )

        bp_l = Line([BILE_PIPE_X - 0.10, CELL_Y0, 0], [BILE_PIPE_X - 0.10, GUT_Y1, 0], color=BILE_COL, stroke_width=2.5)
        bp_r = Line([BILE_PIPE_X + 0.10, CELL_Y0, 0], [BILE_PIPE_X + 0.10, GUT_Y1, 0], color=BILE_COL, stroke_width=2.5)
        bp_lab = T("bile acids", size=24, color=BILE_COL).move_to([BILE_PIPE_X + 0.96, (GUT_Y1 + CELL_Y0) / 2, 0])
        self.play(Create(bp_l), Create(bp_r), FadeIn(bp_lab), run_time=0.7)

        self.at("makes bile acids")
        ws.show_bile = True
        self.wait(1.5)

        self.at("resin traps")
        mesh = _resin_mesh()
        resin_below = _resin_badge_below()
        ws.resin_mesh_on = True
        self.play(FadeOut(resin_pill), FadeIn(mesh), FadeIn(resin_below), run_time=0.8)

        self.at("Predict")
        self.play(FadeOut(world.top_labels), run_time=0.35)
        q = question_card("ER cholesterol?", ["rises", "falls", "no change"],
                          y=3.40, color=LABEL_COL, size=30, chip_size=24,
                          chips_at=[0.95, 3.40, 0], left=-5.4)
        q.chips.arrange(RIGHT, buff=0.28).move_to([0.95, 3.40, 0])
        self.play(FadeIn(q.question), FadeIn(q.chips), run_time=0.6)
        self.finish()


class S05PredictHold(PredictPause):
    QUESTION = "ER cholesterol?"
    OPTIONS = ["rises", "falls", "no change"]
    CARD = {"y": 3.40, "color": LABEL_COL, "size": 30, "chip_size": 24, "left": -5.4}
    CHIPS_AT = [0.95, 3.40, 0]
    RING_AT = (5.85, 3.40, 0)
    SECONDS = 4.5

    def backdrop(self):
        ws = WorldState(gauge=0.74, cups=3, valve_open=1.0, gut_open=1.0, er_pool=0.85,
                        gut_dim=1.0, show_bile=True, resin_mesh=True, bile_rate=0.25)
        world = ws.build(top_labels=False)
        tick_statin = _dial_tick(0.40, STATIN_COL, "statin", TICK_POS["statin"])
        tick_ezet = _dial_tick(0.45, EZET_COL, "ezetimibe", TICK_POS["ezetimibe"])
        for tk in (tick_statin, tick_ezet):
            tk[0].set_opacity(0.45)
            tk[1].set_opacity(0.45)
        return VGroup(world, tick_statin, tick_ezet)

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD)
        q.chips.arrange(RIGHT, buff=0.28).move_to([0.95, 3.40, 0])
        self.add(q)
        ring, run = countdown(self.SECONDS, center=self.RING_AT, radius=0.28, color=CHOL_COL)
        self.add(ring)
        self.play(run)
        self.finish()


class S06ResinAnswer(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.74, cups=3, valve_open=1.0, gut_open=1.0, er_pool=0.85,
                        gut_dim=1.0, show_bile=True, resin_mesh=True, bile_rate=0.25)
        world = ws.build(top_labels=False)
        tick_statin = _dial_tick(0.40, STATIN_COL, "statin", TICK_POS["statin"])
        tick_ezet = _dial_tick(0.45, EZET_COL, "ezetimibe", TICK_POS["ezetimibe"])
        for tk in (tick_statin, tick_ezet):
            tk[0].set_opacity(0.45)
            tk[1].set_opacity(0.45)
        q = question_card("ER cholesterol?", ["rises", "falls", "no change"],
                          y=3.40, color=LABEL_COL, size=30, chip_size=24,
                          chips_at=[0.95, 3.40, 0], left=-5.4)
        q.chips.arrange(RIGHT, buff=0.28).move_to([0.95, 3.40, 0])
        self.add(world, tick_statin, tick_ezet, q)

        self.at("falls", lead=0.35)
        falls_chip = q.chips[1]
        self.play(falls_chip[0].animate.set_stroke(BILE_COL, 4).set_fill(BILE_COL, 0.35),
                  falls_chip[1].animate.set_color(BILE_COL), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(q), run_time=0.45)

        top_blood = T("blood", size=26, color=LDL_COL).move_to([(BLOOD_X0 + BLOOD_X1) / 2, 3.16, 0])
        top_cell = T("liver cell", size=28, color=CELL_COL).move_to([1.10, 3.16, 0])
        self.play(FadeIn(top_blood), FadeIn(top_cell), run_time=0.4)

        self.at("turns more of")
        self.play(ws.bile_rate.animate.set_value(0.95), ws.er_pool.animate.set_value(0.35), run_time=1.5)

        self.at("ER cholesterol drops")
        tick_resin = _dial_tick(0.35, RESIN_COL, "resin", TICK_POS["resin"])
        self.play(ws.gauge.animate.set_value(0.35), FadeIn(tick_resin), run_time=0.9)
        self.finish()


class S07Idea(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.36, cups=3, valve_open=0.15, gut_open=0.15, er_pool=0.40,
                        gut_dim=1.0, show_bile=True, resin_mesh=True, bile_rate=0.90, gut_lane_y=-2.10)
        world = ws.build()
        red_stop = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.28,
                                    stroke_color=STATIN_COL, stroke_width=2.5,
                                    fill_color=STATIN_COL, fill_opacity=0.85).move_to(VALVE_PT)
        statin_pill = _pill("statin", STATIN_COL, pad=0.14).move_to([-2.55, -0.04, 0])
        gate = RoundedRectangle(corner_radius=0.04, width=0.38, height=0.16,
                                stroke_color=EZET_COL, stroke_width=2.5,
                                fill_color=EZET_COL, fill_opacity=0.90).move_to([GUT_PIPE_X, GUT_Y1, 0])
        ezet_pill = _pill("ezetimibe", EZET_COL).move_to([-2.45, -2.62, 0])
        stem_ez = Line(ezet_pill.get_right() + RIGHT * 0.06, [GUT_PIPE_X - 0.14, GUT_Y1 - 0.10, 0],
                       color=EZET_COL, stroke_width=2.2)
        self.add(world, red_stop, statin_pill, gate, ezet_pill, stem_ez)

        # Route 3 coloured arrows cleanly clear of all labels ("HMG-CoA reductase", "from gut", "bile acids")
        self.at("Any drug")
        hub = np.array([0.85, 0.14, 0.0])
        a_statin = CurvedArrow(np.array([-2.32, -0.40, 0]), hub + LEFT * 0.10, angle=-0.12, color=STATIN_COL, stroke_width=4, tip_length=0.18)
        a_ezet = CurvedArrow(np.array([-0.55, -1.75, 0]), hub + DL * 0.08, angle=-0.30, color=EZET_COL, stroke_width=4, tip_length=0.18)
        a_resin = CurvedArrow(np.array([1.55, -1.94, 0]), hub + RIGHT * 0.08, angle=-0.18, color=RESIN_COL, stroke_width=4, tip_length=0.18)
        a_white = Arrow(hub, DIAL_CENTER + DOWN * 0.56, buff=0.0, color=LABEL_COL, stroke_width=5, tip_length=0.18)
        self.play(Create(a_statin), Create(a_ezet), Create(a_resin), GrowArrow(a_white), run_time=1.2)

        self.at("tends to raise")
        self.play(ws.cups_n.animate.set_value(5), run_time=1.0)

        self.at("not where the")
        self.play(FadeOut(a_statin), FadeOut(a_ezet), FadeOut(a_resin), run_time=0.8)
        self.finish()


class S08Receptors(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.35, cups=3, valve_open=0.15, gut_open=1.0, er_pool=0.45,
                        gut_dim=0.45, show_bile=False, show_meter=True, ldl_level=0.85,
                        uptake_rate=0.0, show_golgi=True)
        world = ws.build()
        self.add(world)

        # SCAP carries SREBP-2 in open corridor clear of ER (x <= 2.02) and Golgi (y >= 1.15)
        scap = _pill("SCAP", CELL_COL, size=24, pad=0.19).move_to([2.90, 0.86, 0])
        srebp = _pill("SREBP-2", CHOL_COL, size=24, pad=0.19).move_to([2.90, 0.02, 0])
        pair = VGroup(scap, srebp)
        self.play(FadeIn(pair), run_time=0.35)
        self.play(pair.animate.move_to([3.20, 0.46, 0]), run_time=0.55)

        active = _pill("active SREBP-2", CELL_COL, size=24, pad=0.19).move_to([3.42, 0.36, 0])
        self.play(FadeOut(pair), FadeIn(active), run_time=0.3)

        self.at("turns on the LDL")
        self.play(active.animate.move_to([4.02, 0.32, 0]), run_time=0.55)
        to_nuc = Arrow([4.30, 0.62, 0], [4.78, 0.92, 0], buff=0.05, color=CELL_COL, stroke_width=3.5, tip_length=0.18)
        self.play(GrowArrow(to_nuc), FadeOut(active), run_time=0.35)

        nuc_arrow = _nuc_arrow_mob()
        self.play(Create(nuc_arrow), FadeOut(to_nuc), run_time=0.85)

        self.at("Liver cells carry")
        self.play(ws.cups_n.animate.set_value(8), run_time=1.3)

        self.at("More of them")
        self.play(ws.uptake_rate.animate.set_value(0.95), ws.ldl_level.animate.set_value(0.35), run_time=2.0)

        self.at("This takes hours")
        clk_c = np.array([5.72, 2.42, 0.0])
        clk_ring = Circle(radius=0.28, stroke_color=LABEL_COL, stroke_width=2.8, fill_color=BG, fill_opacity=0.85).move_to(clk_c)
        clk_hr = Line(clk_c, clk_c + UP * 0.13, color=LABEL_COL, stroke_width=2.8)
        clk_min = Line(clk_c, clk_c + UP * 0.21, color=CHOL_COL, stroke_width=2.4)
        self.play(FadeIn(clk_ring), FadeIn(clk_hr), FadeIn(clk_min), run_time=0.3)
        self.play(Rotate(clk_min, angle=-TAU, about_point=clk_c),
                  Rotate(clk_hr, angle=-TAU / 12, about_point=clk_c), run_time=1.8)
        self.finish()


class S09Pcsk9(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.35, cups=8, valve_open=0.15, gut_open=1.0, er_pool=0.45,
                        gut_dim=0.45, show_bile=False, show_meter=True, ldl_level=0.35,
                        uptake_rate=0.95, show_golgi=True, show_lyso=False)
        world = ws.build()
        nuc_arrow = _nuc_arrow_mob()
        self.add(world, nuc_arrow)

        self.at("turns on one more")
        pcsk9_arrow = _pcsk9_arrow_mob()
        self.play(Create(pcsk9_arrow), run_time=0.9)

        self.at("makes PCSK9")
        pcsk9_chip = _pill("PCSK9", PCSK9_COL, size=24, pad=0.19).move_to([2.80, -0.45, 0])
        sec_tag = RegularPolygon(4, radius=0.10, color=PCSK9_COL, fill_color=PCSK9_COL, fill_opacity=0.9).move_to([2.80, 0.26, 0])
        self.play(FadeIn(pcsk9_chip), FadeIn(sec_tag), run_time=0.35)
        self.play(sec_tag.animate.move_to([-4.45, 0.26, 0]), run_time=0.80)

        self.at("PCSK9 binds")
        lyso = Circle(radius=LYSO_R, stroke_color=LYSO_STROKE, stroke_width=3.5,
                      fill_color=LYSO_FILL, fill_opacity=0.85).move_to(LYSO_PT)
        lyso_lab = T("lysosome", size=24, color=LABEL_COL).move_to(LYSO_PT + DOWN * 0.68)

        pocket_cup = _cup_shape(-0.08, scale=1.05, color=CELL_COL).move_to([-3.35, -0.08, 0])
        pocket_ldl = Dot([-3.54, -0.08, 0], radius=0.10, color=LDL_COL)
        tag = RegularPolygon(4, radius=0.10, color=PCSK9_COL, fill_color=PCSK9_COL, fill_opacity=0.9).move_to([-3.18, 0.08, 0])
        tagged_pkg = VGroup(pocket_cup, pocket_ldl, tag)
        self.play(FadeIn(lyso), FadeIn(lyso_lab), FadeIn(pocket_cup), FadeIn(pocket_ldl), run_time=0.7)
        self.play(FadeOut(pcsk9_chip), ReplacementTransform(sec_tag, tag), run_time=0.5)

        self.at("sends it to the lysosome")
        self.play(tagged_pkg.animate.move_to(LYSO_PT).scale(0.65), run_time=1.1)
        self.play(FadeOut(tagged_pkg), run_time=0.45)
        self.finish()


class S10Brake(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.35, cups=8, valve_open=0.15, gut_open=1.0, er_pool=0.45,
                        gut_dim=0.45, show_bile=False, show_meter=True, ldl_level=0.35,
                        uptake_rate=0.75, show_golgi=True, show_lyso=True, pcsk9_in_blood=True)
        world = ws.build()
        red_stop = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.28,
                                    stroke_color=STATIN_COL, stroke_width=2.5,
                                    fill_color=STATIN_COL, fill_opacity=0.85).move_to(VALVE_PT)
        statin_pill = _pill("statin", STATIN_COL, size=22, pad=0.11).move_to([-2.55, -0.08, 0])
        start_y = METER_Y0 + 0.85 * (METER_Y1 - METER_Y0)
        start_tick = DashedLine([METER_X - 0.20, start_y, 0], [METER_X + 0.20, start_y, 0],
                                color=LABEL_COL, stroke_width=2.5)
        nuc_arrow = _nuc_arrow_mob()
        pcsk9_arrow = _pcsk9_arrow_mob()
        self.add(world, red_stop, statin_pill, start_tick, nuc_arrow, pcsk9_arrow)

        c1 = VGroup(_cup_shape(0.0, color=CELL_COL), RegularPolygon(4, radius=0.09, color=PCSK9_COL, fill_color=PCSK9_COL, fill_opacity=0.9).move_to([-3.85, 0.14, 0]))
        c2 = VGroup(_cup_shape(0.36, color=CELL_COL), RegularPolygon(4, radius=0.09, color=PCSK9_COL, fill_color=PCSK9_COL, fill_opacity=0.9).move_to([-3.85, 0.50, 0]))
        self.add(c1, c2)
        self.play(
            ws.cups_n.animate.set_value(6),
            c1.animate.move_to(LYSO_PT + LEFT * 0.12).scale(0.6),
            c2.animate.move_to(LYSO_PT + RIGHT * 0.12).scale(0.6),
            run_time=1.2,
        )
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.35)

        self.at("statin raises")
        pcsk9_badge = _pill("PCSK9", PCSK9_COL, size=24, pad=0.19).move_to([2.80, -0.45, 0])
        p_tags = VGroup(*[
            RegularPolygon(4, radius=0.09, color=PCSK9_COL, fill_color=PCSK9_COL, fill_opacity=0.9).move_to([x, 0.26, 0])
            for x in (3.15, 2.45)
        ])
        self.play(FadeIn(pcsk9_badge), FadeIn(p_tags), run_time=0.35)
        self.play(p_tags.animate.move_to([-4.55, 0.26, 0]), run_time=0.80)
        self.play(FadeOut(pcsk9_badge), FadeOut(p_tags), run_time=0.3)

        self.at("gives back part")
        self.play(ws.ldl_level.animate.set_value(0.50), ws.uptake_rate.animate.set_value(0.50), run_time=1.3)

        self.at("The gauge")
        self.play(
            Indicate(nuc_arrow, color=CELL_COL, scale_factor=1.03),
            Indicate(pcsk9_arrow, color=PCSK9_COL, scale_factor=1.03),
            run_time=1.3,
        )
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        ws = WorldState(gauge=0.72, cups=6, valve_open=0.15, gut_open=0.15, er_pool=0.85,
                        gut_dim=1.0, show_bile=True, resin_mesh=True, show_meter=True,
                        ldl_level=0.50, uptake_rate=0.50, bile_rate=0.40, pcsk9_in_blood=True,
                        gut_lane_y=-2.10)
        world = ws.build()
        red_stop = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.28,
                                    stroke_color=STATIN_COL, stroke_width=2.5,
                                    fill_color=STATIN_COL, fill_opacity=0.85).move_to(VALVE_PT)
        statin_pill = _pill("statin", STATIN_COL, pad=0.14).move_to([-2.55, -0.04, 0])
        gate = RoundedRectangle(corner_radius=0.04, width=0.38, height=0.16,
                                stroke_color=EZET_COL, stroke_width=2.5,
                                fill_color=EZET_COL, fill_opacity=0.90).move_to([GUT_PIPE_X, GUT_Y1, 0])
        ezet_pill = _pill("ezetimibe", EZET_COL).move_to([-2.45, -2.62, 0])
        stem_ez = Line(ezet_pill.get_right() + RIGHT * 0.06, [GUT_PIPE_X - 0.14, GUT_Y1 - 0.10, 0],
                       color=EZET_COL, stroke_width=2.2)
        self.add(world, red_stop, statin_pill, gate, ezet_pill, stem_ez)

        self.at("making line")
        self.play(Indicate(red_stop, color=STATIN_COL, scale_factor=1.35),
                  Indicate(statin_pill, color=STATIN_COL, scale_factor=1.1), run_time=0.7)

        self.at("absorption")
        self.play(Indicate(gate, color=EZET_COL, scale_factor=1.35),
                  Indicate(ezet_pill, color=EZET_COL, scale_factor=1.1), run_time=0.7)

        self.at("bile acid drain")
        pulse_ring = RoundedRectangle(corner_radius=0.12, width=1.95, height=0.92,
                                      stroke_color=RESIN_COL, stroke_width=5).move_to([2.40, -2.42, 0])
        self.play(ws.bile_rate.animate.set_value(0.95), Create(pulse_ring), run_time=0.6)
        self.play(FadeOut(pulse_ring), run_time=0.3)

        self.at("Each one empties")
        self.play(ws.er_pool.animate.set_value(0.32), ws.gauge.animate.set_value(0.34), run_time=1.8)

        self.at("with more receptors")
        self.play(ws.cups_n.animate.set_value(8), ws.uptake_rate.animate.set_value(0.95),
                  ws.ldl_level.animate.set_value(0.34), run_time=1.6)
        self.finish()


class S12End(EndCard):
    LINE = "Lower liver ER cholesterol any way, and receptors tend to rise."
