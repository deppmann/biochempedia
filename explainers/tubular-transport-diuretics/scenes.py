"""
The Sodium That Flows On — Tubular Transport, Segment by Segment
=================================================================

COLOUR MAP (one colour per concept for the entire film):
- Sodium (Na+ ions, sodium load):           C_NA     = YELLOW  (#F5D547)
- Potassium (K+ ions, ROMK channel):        C_K      = MAGENTA (#E855B8)
- Basolateral Na+-K+ pump (shared engine):  C_PUMP   = RED     (#FC6255)
- Proximal tubule (PT: NHE3, SGLT2):        C_PT     = TEAL    (#3FB8C0)
- Thick ascending limb (TAL: NKCC2):        C_TAL    = ORANGE  (#F59E3F)
- Distal convoluted tubule (DCT: NCC):      C_DCT    = PURPLE  (#A77BFF)
- Collecting duct (CD: ENaC):               C_CD     = BLUE    (#58C4DD)
- Electrical charge signs (+, -):           C_CHARGE = WHITE   (#FFFFFF)
- Tubular fluid (lumen):                    C_LUMEN  = #253145
- Body side (surrounding tissue):           C_BODY   = #1C212E
- Basolateral membrane highlight:           C_BASO   = #9BB0CC
- Aldosterone hormone drop:                 C_ALDO   = #AEE6FF
- Labels and text (full opacity, never grey): TEXT   = #E8EAF0

THE ONE PICTURE OF THE WORLD (carried across the whole film):
A schematic left-to-right cross-section of a kidney tubule split into four
coloured segments (TEAL proximal tubule, ORANGE thick ascending limb, PURPLE
distal convoluted tubule, BLUE collecting duct), with pale fluid in the upper
lumen, a row of simple epithelial cells below with segment-specific apical
doors on their top wall and turning RED Na+-K+ pumps in their base, a dark
'body side' band below, a 'urine' cup at the right end, a horizontal sodium
share bar along the bottom, and a 'schematic' tag at bottom right. Cell-level
scenes push straight into one TEAL or BLUE cell from this same world and pull
back to it.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_hook:    Mass-balance Na+ stream flows along the lumen and crosses each
               segment's wall; shutting the ORANGE gate sets TAL uptake to 0%,
               rerouting 25% of Na+ past it and ramping K+ secretion in the
               BLUE segment into the urine cup.
- s02_tube:    Smooth push-in into one TEAL cell; Na+ dots drift past in the
               lumen, then pass down through the glowing TEAL apical door as
               the apical membrane brightens white.
- s03_pump:    Same TEAL cell; basolateral border brightens slate, a turning
               RED Na+-K+ pump appears in the base and exports Na+ out into the
               body side, keeping intracellular Na+ count low so apical inflow
               continues.
- s04_doors:   Pull-back to the whole tube; four distinct geometric apical
               doors light in turn as named while identical RED pumps turn in
               every segment's base and Na+ flows through all four doors.
- s05_shares:  Bottom share bar grows computed blocks of exact widths 65, 25,
               5, and 3 out of 100 units (leaving 2% unlabelled) while the
               lumen Na+ dot flux visibly thins by those exact fractions along
               the tube.
- s06_drug:    Unlocked matching padlocks appear over each door; the ORANGE
               padlock drops and locks onto NKCC2, shutting ORANGE uptake to
               0% so Na+ bypasses it while the 25% bar block pulses.
- s07_flow:    Blocked Na+ stream runs thick through PURPLE and BLUE; the 25%
               ORANGE bar block slides past the 5% + 3% blocks (bracketed as
               ~8% downstream) so the 3.1x width mismatch is directly visible.
- s08_enac:    Glide right and push-in into one BLUE collecting duct cell;
               crowded lumen Na+ dots drop one by one through the open BLUE
               ENaC channel carrying white + signs with no partner ion while
               the RED pump exports Na+ at the base.
- s09_predict: White + signs ride down through ENaC out of the lumen while a
               schematic lumen-charge meter enters at zero at the right edge
               and the prediction question appears at top.
- s11_answer:  Charge-meter ValueTracker swings smoothly from 0 to negative as
               white - signs populate the lumen; the MAGENTA ROMK channel opens
               and intracellular K+ dots rise through it toward the negative
               lumen and pour into the urine cup.
- s12_idea:    Pull-back to the whole tube; doors light in sequence, all RED
               pumps pulse together, the ORANGE padlock closes, a thick Na+
               stream surges to BLUE, and K+ pours into the urine cup.
- s13_scope:   A top-left 'sodium arriving' slider ValueTracker rises from low
               to high, directly thickening both the Na+ flux to BLUE and K+
               flow into urine; an aldosterone droplet lands on BLUE, further
               increasing K+ flow via a second tracker.
- s14_close:   A moving flow highlight traces from the padlocked ORANGE door
               along the thick Na+ stream to BLUE and into the K+ stream
               filling the urine cup while all four doors and padlock remain.
"""
from bp_parts import *
import numpy as np

# ------------------------------------------------------------------ palette
C_NA = YELLOW             # #F5D547  sodium
C_K = "#E855B8"           # vivid magenta: potassium / ROMK
C_PUMP = RED              # #FC6255  basolateral Na+-K+ pump
C_PT = TEAL               # #3FB8C0  proximal tubule
C_TAL = "#F59E3F"         # vivid orange: thick ascending limb
C_DCT = "#A77BFF"         # vivid purple: distal convoluted tubule
C_CD = BLUE               # #58C4DD  collecting duct
C_CHARGE = WHITE          # #FFFFFF  charge signs (+, -)
C_LUMEN = "#253145"       # pale-tinted tubular fluid
C_CELL_FILL = "#161B26"   # cell interior fill
C_BODY = "#1C212E"        # body side tissue band
C_BASO = "#9BB0CC"        # basolateral membrane highlight
C_ALDO = "#AEE6FF"        # blue-white aldosterone drop
C_STROKE_DIM = "#4D596D"  # subtle structural divider

# ------------------------------------------------------------------ world geometry (whole tube)
TUBE_X0 = -6.15
TUBE_X1 = 4.55
LUMEN_Y0 = 0.70
LUMEN_Y1 = 2.15
CELL_Y0 = -0.65
CELL_Y1 = 0.70
BODY_Y0 = -1.60
BODY_Y1 = -0.65

# Segment boundaries along x (total width = 10.70)
SEGS = [
    ("pt",  -6.15, -2.75, C_PT,  4, "NHE3, SGLT2", 65),
    ("tal", -2.75,  0.05, C_TAL, 3, "NKCC2",       25),
    ("dct",  0.05,  2.25, C_DCT, 2, "NCC",          5),
    ("cd",   2.25,  4.55, C_CD,  2, "ENaC",         3),
]
SEG_BY_KEY = {s[0]: s for s in SEGS}
SEG_MID = {s[0]: 0.5 * (s[1] + s[2]) for s in SEGS}

# Bottom horizontal share bar: 100 units = 8.00 scene units (x = -6.15 .. 1.85)
BAR_X0 = -6.15
BAR_W = 8.00
BAR_Y0 = -3.22
BAR_Y1 = -2.58
BAR_YC = 0.5 * (BAR_Y0 + BAR_Y1)
BAR_H = BAR_Y1 - BAR_Y0

# Urine cup at right end of whole tube
CUP_X0, CUP_X1 = 4.82, 6.12
CUP_Y0, CUP_Y1 = -0.78, 1.05
CUP_XC = 0.5 * (CUP_X0 + CUP_X1)

# Single-cell zoomed coordinates
Z_X0, Z_X1 = -6.30, 6.30
Z_CX0, Z_CX1 = -3.35, 3.35
Z_LUMEN_Y0, Z_LUMEN_Y1 = 1.15, 2.75
Z_CELL_Y0, Z_CELL_Y1 = -1.85, 1.15
Z_BODY_Y0, Z_BODY_Y1 = -2.92, -1.85


# ------------------------------------------------------------------ reusable parts
def make_scope_tag():
    """High-contrast full-opacity schematic tag in bottom-right safe corner."""
    return scope_tag("schematic", size=24, color=TEXT)


def make_pump(center, radius=0.22, speed=2.2):
    """Turning RED Na+-K+ pump cartoon (ring + 3 turning spokes + center hub)."""
    c = np.array(center, dtype=float)
    bg = Circle(radius=radius, fill_color=BG, fill_opacity=1.0,
                stroke_color=C_PUMP, stroke_width=3.5).move_to(c)
    rotor = VGroup()
    for k in range(3):
        ang = k * TAU / 3.0
        p1 = c + radius * 0.85 * np.array([np.cos(ang), np.sin(ang), 0.0])
        spoke = Line(c, p1, color=C_PUMP, stroke_width=3.2)
        tip = Dot(p1, radius=radius * 0.19, color=C_PUMP)
        rotor.add(spoke, tip)
    hub = Dot(c, radius=radius * 0.22, color=TEXT)
    rotor.add_updater(lambda m, dt, s=speed: m.rotate(-s * dt, about_point=m.get_center()))
    g = VGroup(bg, rotor, hub)
    g.bg, g.rotor, g.hub = bg, rotor, hub
    return g


def make_door(kind, center, color, scale=1.0, dark=False):
    """Simple geometric apical door shape per segment (no molecular structures)."""
    c = np.array(center, dtype=float)
    col = "#495264" if dark else color
    fill_op = 0.15 if dark else 0.35
    sw = 3.2 * scale
    g = VGroup()
    if kind == "pt":
        # Twin notched doors (NHE3 & SGLT2)
        for dx in (-0.28, 0.28):
            w, h = 0.36 * scale, 0.34 * scale
            p_c = c + RIGHT * dx * scale
            l_bar = RoundedRectangle(corner_radius=0.05 * scale, width=0.11 * scale, height=h,
                                     stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op
                                     ).move_to(p_c + LEFT * 0.12 * scale)
            r_bar = RoundedRectangle(corner_radius=0.05 * scale, width=0.11 * scale, height=h,
                                     stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op
                                     ).move_to(p_c + RIGHT * 0.12 * scale)
            cap = Arc(radius=0.14 * scale, start_angle=0, angle=PI, arc_center=p_c + UP * 0.14 * scale,
                      color=col, stroke_width=sw * 0.85)
            g.add(l_bar, r_bar, cap)
    elif kind == "tal":
        # Triple-bar cotransporter chute (NKCC2)
        h = 0.38 * scale
        frame = RoundedRectangle(corner_radius=0.08 * scale, width=0.72 * scale, height=h,
                                 stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op
                                 ).move_to(c)
        bars = VGroup(*[
            Line(c + np.array([dx * scale, -h * 0.44, 0]), c + np.array([dx * scale, h * 0.44, 0]),
                 color=col, stroke_width=sw * 0.85)
            for dx in (-0.15, 0.15)
        ])
        g.add(frame, bars)
    elif kind == "dct":
        # Paired chevron / diamond-notched gate (NCC)
        h = 0.36 * scale
        left_p = Polygon(
            c + np.array([-0.34 * scale, h / 2, 0]),
            c + np.array([-0.08 * scale, h / 2, 0]),
            c + np.array([-0.16 * scale, 0.0, 0]),
            c + np.array([-0.08 * scale, -h / 2, 0]),
            c + np.array([-0.34 * scale, -h / 2, 0]),
            stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op,
        )
        right_p = Polygon(
            c + np.array([0.34 * scale, h / 2, 0]),
            c + np.array([0.08 * scale, h / 2, 0]),
            c + np.array([0.16 * scale, 0.0, 0]),
            c + np.array([0.08 * scale, -h / 2, 0]),
            c + np.array([0.34 * scale, -h / 2, 0]),
            stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op,
        )
        g.add(left_p, right_p)
    elif kind == "cd":
        # Simple open vertical channel (ENaC)
        h = 0.40 * scale
        l_bar = RoundedRectangle(corner_radius=0.06 * scale, width=0.14 * scale, height=h,
                                 stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op
                                 ).move_to(c + LEFT * 0.20 * scale)
        r_bar = RoundedRectangle(corner_radius=0.06 * scale, width=0.14 * scale, height=h,
                                 stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op
                                 ).move_to(c + RIGHT * 0.20 * scale)
        g.add(l_bar, r_bar)
    elif kind == "romk":
        # Outward-flaring potassium exit channel (ROMK)
        h = 0.42 * scale
        l_wall = Polygon(
            c + np.array([-0.32 * scale, h / 2, 0]),
            c + np.array([-0.18 * scale, h / 2, 0]),
            c + np.array([-0.12 * scale, -h / 2, 0]),
            c + np.array([-0.26 * scale, -h / 2, 0]),
            stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op,
        )
        r_wall = Polygon(
            c + np.array([0.32 * scale, h / 2, 0]),
            c + np.array([0.18 * scale, h / 2, 0]),
            c + np.array([0.12 * scale, -h / 2, 0]),
            c + np.array([0.26 * scale, -h / 2, 0]),
            stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op,
        )
        g.add(l_wall, r_wall)
    return g


def make_padlock(center, color, locked=False, scale=1.0):
    """Simple schematic padlock (unlocked outline or closed solid lock)."""
    c = np.array(center, dtype=float)
    bw, bh = 0.36 * scale, 0.28 * scale
    body = RoundedRectangle(
        corner_radius=0.05 * scale, width=bw, height=bh,
        stroke_color=color, stroke_width=3.0 * scale,
        fill_color=color, fill_opacity=0.85 if locked else 0.10,
    ).move_to(c)
    shackle_r = 0.11 * scale
    shackle_c = body.get_top() + (UP * 0.01 if locked else UP * 0.10) * scale
    shackle = Arc(radius=shackle_r, start_angle=0, angle=PI, arc_center=shackle_c,
                  color=color, stroke_width=3.0 * scale)
    if not locked:
        shackle.shift(RIGHT * 0.07 * scale)
    # Keyhole dot when locked
    g = VGroup(shackle, body)
    if locked:
        kh = Dot(c, radius=0.042 * scale, color=BG)
        g.add(kh)
    g.body, g.shackle = body, shackle
    return g


def make_urine_cup(x0=CUP_X0, x1=CUP_X1, y0=CUP_Y0, y1=CUP_Y1, fill_tracker=None, label=True):
    """Open beaker/cup at the right end of the tubule with optional dynamic fluid level."""
    xc = 0.5 * (x0 + x1)
    w = x1 - x0
    h = y1 - y0
    # Cup interior background (dark)
    interior = Rectangle(width=w, height=h, fill_color="#141923", fill_opacity=0.95,
                         stroke_width=0).move_to([xc, 0.5 * (y0 + y1), 0])
    # Dynamic fluid fill inside cup
    ft = fill_tracker if fill_tracker is not None else ValueTracker(0.28)

    def _mk_fluid():
        lvl = float(np.clip(ft.get_value(), 0.08, 0.88))
        fh = h * lvl
        return Rectangle(
            width=w - 0.08, height=fh,
            fill_color="#354663", fill_opacity=0.85, stroke_width=0,
        ).move_to([xc, y0 + fh / 2 + 0.03, 0])

    fluid = always_redraw(_mk_fluid)
    # U-shaped beaker wall (open at top)
    wall = VMobject(stroke_color=TEXT, stroke_width=3.5, fill_opacity=0)
    wall.set_points_as_corners([
        [x0 - 0.06, y1 + 0.04, 0],
        [x0, y1, 0],
        [x0, y0, 0],
        [x1, y0, 0],
        [x1, y1, 0],
        [x1 + 0.06, y1 + 0.04, 0],
    ])
    g = VGroup(interior, fluid, wall)
    g.fill_tracker = ft
    if label:
        lab = T("urine", size=26, color=TEXT).move_to([xc, y0 - 0.36, 0])
        g.add(lab)
        g.label = lab
    return g


def make_empty_bar():
    """The bottom horizontal share bar frame (100 units wide = BAR_W)."""
    rect = Rectangle(
        width=BAR_W, height=BAR_H,
        stroke_color=TEXT, stroke_width=2.5,
        fill_color="#141822", fill_opacity=0.85,
    ).move_to([BAR_X0 + BAR_W / 2, BAR_YC, 0])
    return rect


def build_share_blocks(include_tag=True, include_thin_labels=True):
    """Build the 65/25/5/3 computed blocks for the bottom share bar."""
    blocks = {}
    x_cur = BAR_X0
    for key, _, _, col, _, _, pct in SEGS:
        bw = BAR_W * (pct / 100.0)
        rect = Rectangle(
            width=bw, height=BAR_H - 0.06,
            stroke_color=col, stroke_width=3.0,
            fill_color=col, fill_opacity=0.30,
        ).move_to([x_cur + bw / 2, BAR_YC, 0])
        if pct >= 20:
            lab = M(f"{pct}%", size=26, color=TEXT).move_to(rect.get_center())
            grp = VGroup(rect, lab)
            grp.rect, grp.lab = rect, lab
        else:
            grp = VGroup(rect)
            grp.rect, grp.lab = rect, None
        blocks[key] = grp
        x_cur += bw

    thin_labels = VGroup()
    if include_thin_labels:
        # 5% above-left of purple block with leader tick; 3% above-right of blue block
        p_cx = blocks["dct"].rect.get_center()[0]
        b_cx = blocks["cd"].rect.get_center()[0]
        l5 = M("5%", size=24, color=C_DCT).move_to([p_cx - 0.35, BAR_Y1 + 0.42, 0])
        t5 = Line([p_cx - 0.25, BAR_Y1 + 0.22, 0], [p_cx, BAR_Y1 + 0.03, 0], color=C_DCT, stroke_width=2.2)
        l3 = M("3%", size=24, color=C_CD).move_to([b_cx + 0.42, BAR_Y1 + 0.42, 0])
        t3 = Line([b_cx + 0.30, BAR_Y1 + 0.22, 0], [b_cx, BAR_Y1 + 0.03, 0], color=C_CD, stroke_width=2.2)
        thin_labels.add(l5, t5, l3, t3)

    tag = None
    if include_tag:
        tag = T("rounded human estimates", size=24, color=TEXT).move_to([BAR_X0, BAR_Y1 + 0.42, 0], aligned_edge=LEFT)

    return blocks, thin_labels, tag


# ------------------------------------------------------------------ whole-tube world builder
def build_whole_tube(
    show_doors=True,
    show_door_labels=False,
    show_pumps=True,
    tal_blocked=False,
    show_bar=True,
    cup_fill=0.28,
):
    """Build the continuous whole-tube schematic world in its canonical coordinates."""
    world = VGroup()

    # 1. Lumen band
    lumen = Rectangle(
        width=TUBE_X1 - TUBE_X0, height=LUMEN_Y1 - LUMEN_Y0,
        fill_color=C_LUMEN, fill_opacity=0.95, stroke_width=0,
    ).move_to([0.5 * (TUBE_X0 + TUBE_X1), 0.5 * (LUMEN_Y0 + LUMEN_Y1), 0])
    top_wall = Line([TUBE_X0, LUMEN_Y1, 0], [TUBE_X1, LUMEN_Y1, 0], color=TEXT, stroke_width=3.2)

    # 2. Body side band
    body = Rectangle(
        width=TUBE_X1 - TUBE_X0, height=BODY_Y1 - BODY_Y0,
        fill_color=C_BODY, fill_opacity=0.95, stroke_width=0,
    ).move_to([0.5 * (TUBE_X0 + TUBE_X1), 0.5 * (BODY_Y0 + BODY_Y1), 0])
    body_bottom = Line([TUBE_X0, BODY_Y0, 0], [TUBE_X1, BODY_Y0, 0], color=C_STROKE_DIM, stroke_width=2.0)
    # Placed in the clean gap between PT pump (-4.45) and TAL pump (-1.35)
    body_label = T("body side", size=26, color=TEXT).move_to([-2.90, 0.5 * (BODY_Y0 + BODY_Y1), 0])

    # 3. Coloured segments (cells + apical top bar + cell dividers)
    seg_groups = {}
    doors = {}
    door_labels = {}
    pumps = {}

    cells_layer = VGroup()
    apical_layer = VGroup()
    doors_layer = VGroup()
    pumps_layer = VGroup()
    labels_layer = VGroup()

    for key, x0, x1, col, n_cells, dname, _ in SEGS:
        sw = x1 - x0
        xc = 0.5 * (x0 + x1)
        # Segment cell strip
        cell_bg = Rectangle(
            width=sw, height=CELL_Y1 - CELL_Y0,
            fill_color=col, fill_opacity=0.16,
            stroke_color=col, stroke_width=2.4,
        ).move_to([xc, 0.5 * (CELL_Y0 + CELL_Y1), 0])
        # Vertical cell dividers inside segment
        divs = VGroup()
        for j in range(1, n_cells):
            xd = x0 + j * sw / n_cells
            divs.add(Line([xd, CELL_Y0, 0], [xd, CELL_Y1, 0], color=col, stroke_width=1.6, stroke_opacity=0.55))
        # Apical membrane coloured highlight bar
        ap_bar = Line([x0 + 0.02, LUMEN_Y0, 0], [x1 - 0.02, LUMEN_Y0, 0], color=col, stroke_width=5.5)
        seg_g = VGroup(cell_bg, divs, ap_bar)
        seg_groups[key] = seg_g
        cells_layer.add(cell_bg, divs)
        apical_layer.add(ap_bar)

        # Apical door
        door = make_door(key, [xc, LUMEN_Y0, 0], col, scale=0.95, dark=(tal_blocked and key == "tal"))
        doors[key] = door
        if show_doors:
            doors_layer.add(door)

        # Door label above lumen top wall
        dlab = T(dname, size=28, color=col).move_to([xc, LUMEN_Y1 + 0.36, 0])
        door_labels[key] = dlab
        if show_door_labels:
            labels_layer.add(dlab)

        # Turning RED Na+-K+ pump in cell base
        pmp = make_pump([xc, CELL_Y0, 0], radius=0.22, speed=2.2)
        pumps[key] = pmp
        if show_pumps:
            pumps_layer.add(pmp)

    # 4. Urine cup
    cup_ft = ValueTracker(cup_fill)
    cup = make_urine_cup(fill_tracker=cup_ft)

    # 5. Bottom empty bar
    bar = make_empty_bar() if show_bar else VGroup()

    world.add(lumen, top_wall, body, body_bottom, cells_layer, apical_layer,
              doors_layer, pumps_layer, body_label, cup, bar, labels_layer)
    world.lumen = lumen
    world.top_wall = top_wall
    world.body = body
    world.body_label = body_label
    world.segs = seg_groups
    world.doors = doors
    world.door_labels = door_labels
    world.pumps = pumps
    world.cup = cup
    world.cup_ft = cup_ft
    world.bar = bar
    world.doors_layer = doors_layer
    world.pumps_layer = pumps_layer
    world.labels_layer = labels_layer
    return world


def make_tube_ion_system(tal_open_val=1.0, k_rate_val=0.15, na_load_val=0.75, aldo_val=0.0,
                         seed=7, show_k=True):
    """Computed mass-balance Na+ (YELLOW) and K+ (MAGENTA) particle flow in whole tube.

    Driven directly by ValueTrackers:
      - tal_open: 1.0 = normal 25% TAL uptake; 0.0 = TAL blocked -> 25% flows on to DCT/CD/urine.
      - na_load:  0.15..1.0 scales active sodium stream density.
      - k_rate:   0.0..1.0 scales baseline potassium secretion into urine.
      - aldo:     0.0..0.5 extra aldosterone amplification on potassium secretion.
    """
    rng = np.random.default_rng(seed)
    tal_open = ValueTracker(tal_open_val)
    k_rate = ValueTracker(k_rate_val)
    na_load = ValueTracker(na_load_val)
    aldo = ValueTracker(aldo_val)

    # Stratified deterministic fates for 56 Na+ ions matching 65/25/5/3/2 shares
    n_na = 56
    fates = (np.arange(n_na) + rng.uniform(0.15, 0.85, n_na)) / n_na
    rng.shuffle(fates)
    phases = rng.uniform(0.0, 1.0, n_na)
    lanes = rng.uniform(0.95, 1.92, n_na)
    # Deterministic subset of blocked-TAL ions that enter ENaC vs go straight to urine
    tal_to_enac = (rng.random(n_na) < 0.35) | True  # all sodium missed at the TAL travels on to ENaC
    # Priority order for na_load scaling (always keep a balanced subset visible)
    na_rank = rng.permutation(n_na) / n_na

    na_dots = VGroup(*[Dot(radius=0.068, color=C_NA) for _ in range(n_na)])

    # 22 K+ ions rising from BLUE collecting duct cells into lumen and into urine cup
    n_k = 22
    k_phases = (np.arange(n_k) + rng.uniform(0.0, 0.6, n_k)) / n_k
    k_x0 = SEG_MID["cd"] + rng.uniform(-0.42, 0.42, n_k)
    k_lanes = rng.uniform(1.05, 1.78, n_k)
    k_rank = rng.permutation(n_k) / n_k
    k_dots = VGroup(*[Dot(radius=0.068, color=C_K) for _ in range(n_k)])

    state = {"t": 0.0}

    def _na_pos(p, u, lane, enters_enac_when_blocked, t_open):
        # Determine target exit x
        if u < 0.65:
            exit_x = SEG_MID["pt"]
        elif u < 0.90:
            if t_open > 0.5:
                exit_x = SEG_MID["tal"]
            elif enters_enac_when_blocked:
                exit_x = SEG_MID["cd"]
            else:
                exit_x = None
        elif u < 0.95:
            exit_x = SEG_MID["dct"]
        elif u < 0.98:
            exit_x = SEG_MID["cd"]
        else:
            exit_x = None

        if exit_x is not None:
            # Travel horizontally in lumen (0..0.68), drop through door/cell/pump (0.68..0.92), into body (0.92..1.0)
            if p < 0.68:
                f = p / 0.68
                x = TUBE_X0 + 0.12 + f * (exit_x - (TUBE_X0 + 0.12))
                y = lane
            elif p < 0.90:
                f = (p - 0.68) / 0.22
                x = exit_x + 0.08 * np.sin(f * PI)
                y = lane + f * (CELL_Y0 - lane)
            else:
                f = (p - 0.90) / 0.10
                x = exit_x + 0.12 * (f - 0.5)
                y = CELL_Y0 - 0.15 - f * 0.62
        else:
            # Travel entire lumen to tube end (0..0.82), then arc into urine cup (0.82..1.0)
            if p < 0.82:
                f = p / 0.82
                x = TUBE_X0 + 0.12 + f * (TUBE_X1 - (TUBE_X0 + 0.12))
                y = lane
            else:
                f = (p - 0.82) / 0.18
                x = TUBE_X1 + f * (CUP_XC - TUBE_X1)
                y = lane * (1 - f) + (CUP_Y0 + 0.28) * f - 0.18 * np.sin(f * PI)
        return np.array([x, y, 0.0])

    def _k_pos(p, x_start, lane):
        # Rise from BLUE cell interior through apical membrane into lumen (0..0.38),
        # flow right to tube exit (0.38..0.74), pour into urine cup (0.74..1.0)
        if p < 0.38:
            f = p / 0.38
            x = x_start
            y = (CELL_Y0 + 0.28) + f * (lane - (CELL_Y0 + 0.28))
        elif p < 0.74:
            f = (p - 0.38) / 0.36
            x = x_start + f * (TUBE_X1 - x_start)
            y = lane
        else:
            f = (p - 0.74) / 0.26
            x = TUBE_X1 + f * (CUP_XC - TUBE_X1)
            y = lane * (1 - f) + (CUP_Y0 + 0.30) * f - 0.16 * np.sin(f * PI)
        return np.array([x, y, 0.0])

    def _update(mob, dt):
        state["t"] += dt
        t = state["t"]
        t_open = tal_open.get_value()
        load = float(np.clip(na_load.get_value(), 0.12, 1.0))
        kr = float(np.clip(k_rate.get_value() + aldo.get_value(), 0.0, 1.0))

        for i, d in enumerate(na_dots):
            p = (phases[i] + 0.155 * t) % 1.0
            d.move_to(_na_pos(p, fates[i], lanes[i], tal_to_enac[i], t_open))
            visible = (na_rank[i] <= load)
            d.set_opacity(1.0 if visible else 0.0)

        for i, d in enumerate(k_dots):
            p = (k_phases[i] + 0.24 * t) % 1.0
            d.move_to(_k_pos(p, k_x0[i], k_lanes[i]))
            visible = show_k and (k_rank[i] < kr)
            d.set_opacity(1.0 if visible else 0.0)

    ions = VGroup(na_dots, k_dots)
    # Initial placement so frame 0 is already populated
    _update(ions, 0.0)
    ions.add_updater(_update)
    ions.tal_open = tal_open
    ions.k_rate = k_rate
    ions.na_load = na_load
    ions.aldo = aldo
    ions.na_dots = na_dots
    ions.k_dots = k_dots
    return ions


# ------------------------------------------------------------------ single-cell zoomed world builder
def build_single_cell(
    seg_key="pt",
    door_x=0.0,
    show_door=True,
    door_glow=False,
    apical_white=False,
    baso_slate=False,
    show_pump=False,
    pump_speed=2.2,
    lumen_x1=Z_X1,
    right_open=False,
):
    """Build zoomed single-cell view (TEAL PT cell or BLUE CD principal cell)."""
    col = SEG_BY_KEY[seg_key][3]
    g = VGroup()

    # Lumen fluid band
    lumen = Rectangle(
        width=lumen_x1 - Z_X0, height=Z_LUMEN_Y1 - Z_LUMEN_Y0,
        fill_color=C_LUMEN, fill_opacity=0.95, stroke_width=0,
    ).move_to([0.5 * (Z_X0 + lumen_x1), 0.5 * (Z_LUMEN_Y0 + Z_LUMEN_Y1), 0])
    top_wall = Line([Z_X0, Z_LUMEN_Y1, 0], [lumen_x1, Z_LUMEN_Y1, 0], color=TEXT, stroke_width=3.2)

    # Body side band
    body_x1 = lumen_x1 if right_open else Z_X1
    body = Rectangle(
        width=body_x1 - Z_X0, height=Z_BODY_Y1 - Z_BODY_Y0,
        fill_color=C_BODY, fill_opacity=0.95, stroke_width=0,
    ).move_to([0.5 * (Z_X0 + body_x1), 0.5 * (Z_BODY_Y0 + Z_BODY_Y1), 0])
    body_bottom = Line([Z_X0, Z_BODY_Y0, 0], [body_x1, Z_BODY_Y0, 0], color=C_STROKE_DIM, stroke_width=2.0)
    body_label = T("body side", size=26, color=TEXT).move_to([-4.95, 0.5 * (Z_BODY_Y0 + Z_BODY_Y1), 0])

    # Neighbouring partial cells (left always; right unless right_open for urine cup)
    l_cell = Rectangle(
        width=(Z_CX0 - 0.14) - Z_X0, height=Z_CELL_Y1 - Z_CELL_Y0,
        fill_color=col, fill_opacity=0.09, stroke_color=col, stroke_width=2.0, stroke_opacity=0.55,
    ).move_to([0.5 * (Z_X0 + Z_CX0 - 0.14), 0.5 * (Z_CELL_Y0 + Z_CELL_Y1), 0])
    neighbours = VGroup(l_cell)
    if not right_open:
        r_cell = Rectangle(
            width=Z_X1 - (Z_CX1 + 0.14), height=Z_CELL_Y1 - Z_CELL_Y0,
            fill_color=col, fill_opacity=0.09, stroke_color=col, stroke_width=2.0, stroke_opacity=0.55,
        ).move_to([0.5 * (Z_CX1 + 0.14 + Z_X1), 0.5 * (Z_CELL_Y0 + Z_CELL_Y1), 0])
        neighbours.add(r_cell)

    # Central cell body
    cell_box = Rectangle(
        width=Z_CX1 - Z_CX0, height=Z_CELL_Y1 - Z_CELL_Y0,
        fill_color=col, fill_opacity=0.16, stroke_color=col, stroke_width=3.0,
    ).move_to([0.5 * (Z_CX0 + Z_CX1), 0.5 * (Z_CELL_Y0 + Z_CELL_Y1), 0])

    # Apical membrane line (can brighten to thick WHITE)
    ap_line = Line(
        [Z_CX0, Z_CELL_Y1, 0], [Z_CX1, Z_CELL_Y1, 0],
        color=WHITE if apical_white else col,
        stroke_width=8.0 if apical_white else 5.0,
    )

    # Basolateral border (left + bottom + right of central cell)
    baso_line = VMobject(
        stroke_color=C_BASO if baso_slate else col,
        stroke_width=7.5 if baso_slate else 0.0,
        stroke_opacity=1.0 if baso_slate else 0.0,
        fill_opacity=0,
    )
    baso_line.set_points_as_corners([
        [Z_CX0, Z_CELL_Y1 - 0.04, 0],
        [Z_CX0, Z_CELL_Y0, 0],
        [Z_CX1, Z_CELL_Y0, 0],
        [Z_CX1, Z_CELL_Y1 - 0.04, 0],
    ])

    # Apical door
    door = make_door(seg_key, [door_x, Z_CELL_Y1, 0], col, scale=1.55)
    if door_glow:
        door.set_stroke(width=5.5)

    # Basolateral RED Na+-K+ pump (returned as attribute; added separately to scene so cell_box
    # is never treated as a clipping panel around the transmembrane pump)
    pump = make_pump([0.0, Z_CELL_Y0, 0], radius=0.44, speed=pump_speed)

    g.add(lumen, top_wall, body, body_bottom, neighbours, cell_box, ap_line, baso_line, body_label)
    if show_door:
        g.add(door)

    g.lumen = lumen
    g.top_wall = top_wall
    g.body = body
    g.body_label = body_label
    g.neighbours = neighbours
    g.cell_box = cell_box
    g.ap_line = ap_line
    g.baso_line = baso_line
    g.door = door
    g.pump = pump
    g.has_pump = show_pump
    return g


def make_na_token(radius=0.105, with_plus=False):
    """A YELLOW sodium dot, optionally carrying a crisp WHITE plus sign."""
    dot = Dot(radius=radius, color=C_NA)
    if not with_plus:
        return dot
    plus = VGroup(
        Line(LEFT * 0.055, RIGHT * 0.055, color=C_CHARGE, stroke_width=2.6),
        Line(DOWN * 0.055, UP * 0.055, color=C_CHARGE, stroke_width=2.6),
    ).move_to(dot.get_center() + UR * 0.12)
    return VGroup(dot, plus)


def make_cell_ion_system(
    door_x=0.0,
    enter_rate=1.0,
    pump_on=1.0,
    with_plus=False,
    lumen_x1=Z_X1,
    crowded=False,
    romk_on=0.0,
    romk_x=1.35,
    cup_target=None,
    bob_only=False,
    seed=11,
):
    """Computed ion transport inside the single-cell zoomed view.

    Trackers:
      - enter: 0..1 fraction of entering Na+ stream active
      - pump:  0..1 whether pump throws Na+ out the basolateral base
      - romk:  0..1 whether K+ dots rise through ROMK into lumen & cup
    """
    rng = np.random.default_rng(seed)
    enter_tr = ValueTracker(enter_rate)
    pump_tr = ValueTracker(pump_on)
    romk_tr = ValueTracker(romk_on)

    # 1. Lumen drifting Na+ dots (kept in lower/mid lumen so upper strip stays clear for white '-' signs)
    n_lum = 22 if crowded else 14
    lum_phases = (np.arange(n_lum) + rng.uniform(0.0, 0.7, n_lum)) / n_lum
    lum_y = rng.uniform(Z_LUMEN_Y0 + 0.30, Z_LUMEN_Y0 + 0.92, n_lum)
    lum_bob_seed = rng.uniform(0.0, TAU, n_lum)
    lum_dots = VGroup(*[make_na_token(radius=0.105, with_plus=with_plus) for _ in range(n_lum)])

    # 2. Transcellular Na+ dots (entering through apical door -> cell -> RED pump -> body side)
    n_trans = 6
    trans_phases = np.linspace(0.0, 1.0, n_trans, endpoint=False)
    trans_dots = VGroup(*[make_na_token(radius=0.11, with_plus=with_plus) for _ in range(n_trans)])

    # 3. Intracellular / secreted K+ dots (for s11_answer)
    n_k = 10
    k_phases = np.linspace(0.0, 1.0, n_k, endpoint=False)
    k_jx = rng.uniform(-0.22, 0.22, n_k)
    k_dots = VGroup(*[Dot(radius=0.11, color=C_K) for _ in range(n_k)])

    state = {"t": 0.0}
    lx0 = Z_X0 + 0.25
    lx1 = lumen_x1 - 0.25

    def _update(mob, dt):
        state["t"] += dt
        t = state["t"]
        ev = enter_tr.get_value()
        pv = pump_tr.get_value()
        rv = romk_tr.get_value()

        # Lumen Na+
        for i, d in enumerate(lum_dots):
            if bob_only:
                x = lx0 + lum_phases[i] * (lx1 - lx0)
                y = lum_y[i] + 0.05 * np.sin(2.4 * t + lum_bob_seed[i])
            else:
                p = (lum_phases[i] + 0.14 * t) % 1.0
                x = lx0 + p * (lx1 - lx0)
                y = lum_y[i]
            d.move_to([x, y, 0.0])

        # Transcellular Na+ through apical door -> RED pump -> body side
        for i, d in enumerate(trans_dots):
            if ev < 0.05:
                d.set_opacity(0.0)
                continue
            d.set_opacity(1.0)
            p = (trans_phases[i] + (0.04 if bob_only else 0.24) * t) % 1.0
            if pv < 0.5:
                # Before pump exists (s02_tube): enter door and settle slowly in upper cell
                if p < 0.45:
                    f = p / 0.45
                    x = door_x
                    y = (Z_LUMEN_Y0 + 0.48) - f * 1.15
                else:
                    f = (p - 0.45) / 0.55
                    x = door_x + (0.55 if i % 2 == 0 else -0.55) * f
                    y = (Z_LUMEN_Y0 - 0.67) - 0.65 * f
            else:
                # Full transcellular path: lumen -> apical door -> curve smoothly toward pump -> thrown into body side
                # Stays sparse inside cell and clears lower-left 'sodium alone' label cleanly
                if p < 0.26:
                    f = p / 0.26
                    x = door_x
                    y = (Z_LUMEN_Y0 + 0.55) - f * 0.90
                elif p < 0.68:
                    f = (p - 0.26) / 0.42
                    xf = f ** 0.55
                    x = door_x * (1 - xf) + 0.0 * xf
                    y = (Z_LUMEN_Y0 - 0.35) + f * (Z_CELL_Y0 - (Z_LUMEN_Y0 - 0.35))
                else:
                    f = (p - 0.68) / 0.32
                    x = 0.28 * ((i % 3) - 1) * f
                    y = Z_CELL_Y0 - 0.22 - f * 0.66
            d.move_to([x, y, 0.0])

        # Secreted K+ through ROMK -> lumen -> right edge urine cup
        for i, d in enumerate(k_dots):
            if rv < 0.05:
                d.set_opacity(0.0)
                continue
            d.set_opacity(1.0)
            p = (k_phases[i] + 0.26 * t) % 1.0
            if p < 0.38:
                f = p / 0.38
                x = romk_x + k_jx[i] * (1 - f)
                y = (Z_CELL_Y0 + 0.72) + f * ((Z_LUMEN_Y0 + 0.42) - (Z_CELL_Y0 + 0.72))
            elif p < 0.72:
                f = (p - 0.38) / 0.34
                x = romk_x + f * ((lumen_x1 - 0.10) - romk_x)
                y = Z_LUMEN_Y0 + 0.42 + 0.14 * np.sin(f * PI)
            else:
                f = (p - 0.72) / 0.28
                tx, ty = cup_target if cup_target is not None else (5.25, -0.95)
                x = (lumen_x1 - 0.10) + f * (tx - (lumen_x1 - 0.10))
                y = (Z_LUMEN_Y0 + 0.42) * (1 - f) + ty * f - 0.15 * np.sin(f * PI)
            d.move_to([x, y, 0.0])

    grp = VGroup(lum_dots, trans_dots, k_dots)
    _update(grp, 0.0)
    grp.add_updater(_update)
    grp.enter_tr = enter_tr
    grp.pump_tr = pump_tr
    grp.romk_tr = romk_tr
    return grp


def make_charge_meter(center=(5.12, 2.02, 0), val=0.0):
    """Schematic lumen-charge meter (no numbers): needle driven by ValueTracker (-1..+1)."""
    c = np.array(center, dtype=float)
    tr = ValueTracker(val)

    card = RoundedRectangle(
        corner_radius=0.16, width=2.36, height=1.68,
        stroke_color=TEXT, stroke_width=2.2,
        fill_color=BG, fill_opacity=0.96,
    ).move_to(c)

    arc_c = c + DOWN * 0.14
    r = 0.54
    track = Arc(radius=r, start_angle=PI, angle=-PI, arc_center=arc_c,
                stroke_color="#5B677B", stroke_width=8)
    # Zero tick at top
    t0 = Line(arc_c + UP * (r - 0.08), arc_c + UP * (r + 0.09), color=TEXT, stroke_width=3.0)
    # Minus and plus marks at left and right ends, and 0 well inside card top
    minus_m = M("−", size=24, color=C_CHARGE).move_to(arc_c + LEFT * (r + 0.24) + UP * 0.06)
    plus_m = M("+", size=24, color=C_CHARGE).move_to(arc_c + RIGHT * (r + 0.24) + UP * 0.06)
    zero_m = M("0", size=22, color=TEXT).move_to(arc_c + UP * (r + 0.21))

    # Needle: val = 0 -> straight up (PI/2), val = -1 -> left (PI - 0.22), val = +1 -> right (0.22)
    def _mk_needle():
        v = float(np.clip(tr.get_value(), -1.0, 1.0))
        ang = PI / 2 - v * (PI / 2 - 0.24)
        tip = arc_c + 0.84 * r * np.array([np.cos(ang), np.sin(ang), 0.0])
        return VGroup(
            Line(arc_c, tip, color=C_CHARGE, stroke_width=4.5),
            Dot(arc_c, radius=0.065, color=C_CHARGE),
        )

    needle = always_redraw(_mk_needle)
    lab = T("lumen charge", size=24, color=TEXT).move_to(c + DOWN * 0.56)
    g = VGroup(card, track, t0, minus_m, plus_m, zero_m, needle, lab)
    g.tracker = tr
    g.card = card
    g.arc_c = arc_c
    g.lab = lab
    return g


# ================================================================== SCENES

class S00Hook(SpokenScene):
    """Opening hook: whole tubule with Na+ flow, orange door shuts, K+ leaves in urine."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=False, show_pumps=True,
                                 tal_blocked=False, show_bar=True, cup_fill=0.26)
        ions = make_tube_ion_system(tal_open_val=1.0, k_rate_val=0.14, na_load_val=0.80, seed=7)
        tag = make_scope_tag()

        self.add(world, ions, tag)

        # Cue 1: Close one sodium door near the middle
        self.at("Close one sodium door")
        orange_gate = make_door("tal", [SEG_MID["tal"], LUMEN_Y0, 0], C_TAL, scale=0.95, dark=True)
        gate_bar = RoundedRectangle(
            corner_radius=0.06, width=0.86, height=0.22,
            stroke_color=C_TAL, stroke_width=4.0, fill_color=C_TAL, fill_opacity=0.95,
        ).move_to([SEG_MID["tal"], LUMEN_Y0 + 0.55, 0])
        glow = RoundedRectangle(
            corner_radius=0.12, width=1.04, height=0.56,
            stroke_color=C_TAL, stroke_width=4.5, fill_color=C_TAL, fill_opacity=0.16,
        ).move_to([SEG_MID["tal"], LUMEN_Y0, 0])

        self.play(FadeIn(gate_bar, run_time=0.25))
        self.play(
            gate_bar.animate.move_to([SEG_MID["tal"], LUMEN_Y0, 0]),
            Transform(world.doors["tal"], orange_gate),
            FadeIn(glow),
            ions.tal_open.animate.set_value(0.0),
            run_time=0.85,
        )

        # Cue 2: more potassium leaves in the urine farther down
        self.at("more potassium")
        self.play(
            ions.k_rate.animate.set_value(0.92),
            world.cup_ft.animate.set_value(0.46),
            run_time=1.4,
        )

        # Cue 3: Why potassium?
        self.at("Why potassium")
        q = T("Why potassium?", size=42, color=WHITE, weight=BOLD).move_to([0.0, 3.18, 0])
        self.play(FadeIn(q, shift=UP * 0.12), run_time=0.55)

        self.finish()


class S01Title(NarratedScene):
    """2 s silent title over the living tubule; orange gate resets open, K+ returns to trickle."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=False, show_pumps=True,
                                 tal_blocked=True, show_bar=True, cup_fill=0.46)
        ions = make_tube_ion_system(tal_open_val=0.0, k_rate_val=0.92, na_load_val=0.80, seed=7)
        tag = make_scope_tag()

        gate_bar = RoundedRectangle(
            corner_radius=0.06, width=0.86, height=0.22,
            stroke_color=C_TAL, stroke_width=4.0, fill_color=C_TAL, fill_opacity=0.95,
        ).move_to([SEG_MID["tal"], LUMEN_Y0, 0])
        q = T("Why potassium?", size=42, color=WHITE, weight=BOLD).move_to([0.0, 3.18, 0])

        title = T("The Sodium That Flows On", size=44, color=WHITE, font=TITLE_FONT).move_to([0.0, 3.22, 0])
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.14)
        open_door = make_door("tal", [SEG_MID["tal"], LUMEN_Y0, 0], C_TAL, scale=0.95, dark=False)

        self.add(world, ions, gate_bar, q, tag)
        self.play(FadeOut(q), run_time=0.22)
        self.play(
            FadeIn(title, shift=UP * 0.08, run_time=0.45),
            GrowFromCenter(rule, run_time=0.45),
            gate_bar.animate(run_time=0.75).shift(UP * 0.55).set_opacity(0.0),
            Transform(world.doors["tal"], open_door, run_time=0.75),
            ions.tal_open.animate(run_time=0.75).set_value(1.0),
            ions.k_rate.animate(run_time=0.95).set_value(0.14),
            world.cup_ft.animate(run_time=0.95).set_value(0.28),
        )
        self.finish()


class S02Tube(SpokenScene):
    """Push-in on one TEAL proximal cell; apical door glows and apical membrane brightens white."""

    def construct(self):
        cell = build_single_cell(
            seg_key="pt", door_x=0.0, show_door=True,
            door_glow=False, apical_white=False, baso_slate=False, show_pump=False,
        )
        ions = make_cell_ion_system(door_x=0.0, enter_rate=0.0, pump_on=0.0, seed=12)
        tag = make_scope_tag()

        # Start slightly pulled back and smoothly push in on the single TEAL cell
        stage = VGroup(cell, ions)
        stage.scale(0.84).shift(RIGHT * 0.25 + DOWN * 0.08)
        self.add(stage, tag)
        self.play(
            stage.animate.scale(1.0 / 0.84).shift(LEFT * 0.25 + UP * 0.08),
            run_time=2.8,
            rate_func=smooth,
        )

        # Cue: through its own door -> TEAL door glows, yellow dots enter
        self.at("its own door")
        door_ring = RoundedRectangle(
            corner_radius=0.14, width=1.65, height=0.82,
            stroke_color=C_PT, stroke_width=4.5, fill_color=C_PT, fill_opacity=0.18,
        ).move_to([0.0, Z_CELL_Y1, 0])
        self.play(
            FadeIn(door_ring),
            cell.door.animate.set_stroke(width=5.5),
            ions.enter_tr.animate.set_value(1.0),
            run_time=0.9,
        )

        # Cue: apical side -> top membrane brightens thick WHITE, labelled 'apical: faces fluid'
        self.at("apical side")
        ap_bright = Line([Z_CX0, Z_CELL_Y1, 0], [Z_CX1, Z_CELL_Y1, 0], color=WHITE, stroke_width=8.5)
        ap_lab = T("apical: faces fluid", size=30, color=WHITE).move_to([-2.35, 3.24, 0])
        ap_ptr = Arrow(
            start=[-2.35, 2.98, 0], end=[-2.35, Z_CELL_Y1 + 0.14, 0],
            color=WHITE, stroke_width=3.0, buff=0.0, max_tip_length_to_length_ratio=0.16,
        )
        self.play(
            Transform(cell.ap_line, ap_bright),
            FadeIn(ap_lab, shift=DOWN * 0.1),
            GrowArrow(ap_ptr),
            run_time=0.9,
        )
        self.finish()


class S03Pump(SpokenScene):
    """Same TEAL cell: basolateral membrane brightens slate, turning RED Na+-K+ pump exports Na+."""

    def construct(self):
        cell = build_single_cell(
            seg_key="pt", door_x=0.0, show_door=True,
            door_glow=True, apical_white=True, baso_slate=False, show_pump=False,
        )
        door_ring = RoundedRectangle(
            corner_radius=0.14, width=1.65, height=0.82,
            stroke_color=C_PT, stroke_width=4.5, fill_color=C_PT, fill_opacity=0.18,
        ).move_to([0.0, Z_CELL_Y1, 0])
        ap_lab = T("apical: faces fluid", size=30, color=WHITE).move_to([-2.35, 3.24, 0])
        ap_ptr = Arrow(
            start=[-2.35, 2.98, 0], end=[-2.35, Z_CELL_Y1 + 0.14, 0],
            color=WHITE, stroke_width=3.0, buff=0.0, max_tip_length_to_length_ratio=0.16,
        )
        ions = make_cell_ion_system(door_x=0.0, enter_rate=1.0, pump_on=0.0, seed=12)
        tag = make_scope_tag()

        self.add(cell, door_ring, ap_lab, ap_ptr, ions, tag)

        # Cue: basolateral side -> base and sides brighten to SLATE, labelled 'basolateral'
        self.at("basolateral side")
        baso_lit = VMobject(stroke_color=C_BASO, stroke_width=8.0, fill_opacity=0)
        baso_lit.set_points_as_corners([
            [Z_CX0, Z_CELL_Y1 - 0.04, 0],
            [Z_CX0, Z_CELL_Y0, 0],
            [Z_CX1, Z_CELL_Y0, 0],
            [Z_CX1, Z_CELL_Y1 - 0.04, 0],
        ])
        baso_lab = T("basolateral", size=28, color="#DCE7F5").move_to([4.92, -0.35, 0])
        baso_tick = Line([Z_CX1 + 0.08, -0.35, 0], [baso_lab.get_left()[0] - 0.12, -0.35, 0],
                         color=C_BASO, stroke_width=3.0)
        self.play(
            Create(baso_lit),
            FadeIn(baso_lab, shift=LEFT * 0.1),
            Create(baso_tick),
            run_time=0.9,
        )

        # Cue: sodium-potassium pump -> RED turning pump appears in base and exports Na+
        self.at("sodium potassium pump")
        pump = make_pump([0.0, Z_CELL_Y0, 0], radius=0.45, speed=2.4)
        pump_lab = T("Na⁺-K⁺ pump", size=28, color=C_PUMP).move_to([2.35, -2.40, 0])
        pump_tick = Line([0.55, Z_CELL_Y0 - 0.25, 0], [pump_lab.get_left()[0] - 0.14, -2.40, 0],
                         color=C_PUMP, stroke_width=2.8)
        self.play(
            FadeIn(pump, scale=0.8),
            FadeIn(pump_lab, shift=LEFT * 0.1),
            Create(pump_tick),
            ions.pump_tr.animate.set_value(1.0),
            run_time=0.95,
        )

        # Cue: keeps sodium low inside, so it flows in -> emphasize steady apical entry
        self.at("keeps sodium low")
        self.play(
            Indicate(door_ring, color=C_PT, scale_factor=1.08),
            run_time=0.8,
        )
        self.at("so it flows in")
        self.play(
            Indicate(cell.door, color=C_NA, scale_factor=1.08),
            run_time=0.8,
        )
        self.finish()


class S04Doors(SpokenScene):
    """Pull back to whole tube; four distinct doors light as named, shared RED pumps turn below."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=False, show_pumps=True,
                                 tal_blocked=False, show_bar=True, cup_fill=0.28)
        ions = make_tube_ion_system(tal_open_val=1.0, k_rate_val=0.12, na_load_val=0.80, seed=7)
        tag = make_scope_tag()

        self.add(world, ions, tag)

        cues = [
            ("proximal tubule", "pt"),
            ("thick ascending limb", "tal"),
            ("distal convoluted tubule", "dct"),
            ("collecting duct", "cd"),
        ]
        for phrase, key in cues:
            self.at(phrase)
            col = SEG_BY_KEY[key][3]
            d = world.doors[key]
            lab = world.door_labels[key]
            halo = RoundedRectangle(
                corner_radius=0.12, width=1.12, height=0.62,
                stroke_color=col, stroke_width=4.0, fill_color=col, fill_opacity=0.16,
            ).move_to(d.get_center())
            self.play(
                FadeIn(halo, run_time=0.3),
                FadeIn(lab, shift=UP * 0.12, run_time=0.45),
                Indicate(d, color=WHITE, scale_factor=1.14, run_time=0.7),
            )
            self.play(FadeOut(halo, run_time=0.4))

        self.finish()


class S05Shares(SpokenScene):
    """Bottom share bar fills with 65%, 25%, 5%, 3% blocks as named; Na+ stream thins accordingly."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=True, show_pumps=True,
                                 tal_blocked=False, show_bar=True, cup_fill=0.28)
        ions = make_tube_ion_system(tal_open_val=1.0, k_rate_val=0.12, na_load_val=0.90, seed=7)
        tag = make_scope_tag()
        blocks, thin_labels, est_tag = build_share_blocks(include_tag=True, include_thin_labels=True)

        self.add(world, ions, tag)

        # Tag above the bar
        self.at("rounded human estimates")
        self.play(FadeIn(est_tag, shift=UP * 0.08), run_time=0.5)

        # 65% proximal tubule (computed growth driven by ValueTracker)
        self.at("proximal tubule")
        self._grow_block(blocks["pt"], 65, C_PT, run_time=1.35)

        # 25% thick limb
        self.at("thick limb")
        self._grow_block(blocks["tal"], 25, C_TAL, run_time=1.05)

        # 5% distal convoluted tubule
        self.at("distal convoluted tubule")
        self.play(
            GrowFromEdge(blocks["dct"], LEFT),
            FadeIn(thin_labels[0]),
            Create(thin_labels[1]),
            run_time=0.85,
        )

        # 3% collecting duct
        self.at("collecting duct")
        self.play(
            GrowFromEdge(blocks["cd"], LEFT),
            FadeIn(thin_labels[2]),
            Create(thin_labels[3]),
            run_time=0.75,
        )

        self.finish()

    def _grow_block(self, blk, target_pct, col, run_time=1.0):
        """Grow a wide share block from left edge with its live % counter driven by one tracker."""
        x_left = blk.rect.get_left()[0]
        full_w = blk.rect.width
        tr = ValueTracker(0.01)

        def _mk_rect():
            f = float(np.clip(tr.get_value(), 0.01, 1.0))
            w = max(0.06, full_w * f)
            return Rectangle(
                width=w, height=BAR_H - 0.06,
                stroke_color=col, stroke_width=3.0,
                fill_color=col, fill_opacity=0.30,
            ).move_to([x_left + w / 2, BAR_YC, 0])

        def _mk_num():
            f = float(np.clip(tr.get_value(), 0.0, 1.0))
            w = max(0.06, full_w * f)
            if w < 0.78:
                return VGroup()
            val = int(round(f * target_pct))
            return M(f"{val}%", size=26, color=TEXT).move_to([x_left + w / 2, BAR_YC, 0])

        live_r = always_redraw(_mk_rect)
        live_n = always_redraw(_mk_num)
        self.add(live_r, live_n)
        self.play(tr.animate.set_value(1.0), run_time=run_time, rate_func=smooth)
        self.remove(live_r, live_n)
        self.add(blk)


class S06Drug(SpokenScene):
    """Unlocked padlocks hover over each door; furosemide locks ORANGE NKCC2, 25% block pulses."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=True, show_pumps=True,
                                 tal_blocked=False, show_bar=True, cup_fill=0.28)
        ions = make_tube_ion_system(tal_open_val=1.0, k_rate_val=0.12, na_load_val=0.90, seed=7)
        blocks, thin_labels, est_tag = build_share_blocks(include_tag=True, include_thin_labels=True)
        tag = make_scope_tag()

        self.add(world, ions, *blocks.values(), thin_labels, est_tag, tag)

        # Cue: a different drug can block each one -> 4 unlocked padlocks hover near doors
        self.at("different drug")
        locks = {}
        for key, _, _, col, _, _, _ in SEGS:
            locks[key] = make_padlock([SEG_MID[key], LUMEN_Y0 + 0.68, 0], col, locked=False, scale=0.92)
        self.play(*[FadeIn(lk, shift=DOWN * 0.15) for lk in locks.values()], run_time=0.8)

        # Cue: Furosemide -> ORANGE padlock closes onto NKCC2, orange door goes dark, 25% pulses
        self.at("Furosamide")
        closed_lock = make_padlock([SEG_MID["tal"], LUMEN_Y0 + 0.04, 0], C_TAL, locked=True, scale=1.05)
        dark_tal = make_door("tal", [SEG_MID["tal"], LUMEN_Y0, 0], C_TAL, scale=0.95, dark=True)
        drug_lab = T("furosemide", size=28, color=C_TAL, weight=BOLD).move_to([SEG_MID["tal"], 3.16, 0])

        self.play(
            Transform(locks["tal"], closed_lock),
            Transform(world.doors["tal"], dark_tal),
            FadeIn(drug_lab, shift=DOWN * 0.1),
            ions.tal_open.animate.set_value(0.0),
            run_time=1.0,
        )

        self.finish()


class S07Flow(SpokenScene):
    """Blocked 25% sodium runs thick downstream; 25% bar block slides past the ~8% bracket."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=True, show_pumps=True,
                                 tal_blocked=True, show_bar=True, cup_fill=0.34)
        ions = make_tube_ion_system(tal_open_val=0.0, k_rate_val=0.22, na_load_val=0.92, seed=7)
        blocks, thin_labels, est_tag = build_share_blocks(include_tag=True, include_thin_labels=True)
        tag = make_scope_tag()

        # Carry locked orange padlock + furosemide label + other subtle unlocked padlocks
        closed_lock = make_padlock([SEG_MID["tal"], LUMEN_Y0 + 0.04, 0], C_TAL, locked=True, scale=1.05)
        drug_lab = T("furosemide", size=28, color=C_TAL, weight=BOLD).move_to([SEG_MID["tal"], 3.16, 0])

        self.add(world, ions, closed_lock, drug_lab, *blocks.values(), thin_labels, est_tag, tag)

        # Cue: quarter of filtered sodium flows on -> 25% ORANGE block slides right past purple & blue
        self.at("quarter of filtered")
        # Ghost outline in the vacated 25% slot
        ghost = DashedVMobject(
            Rectangle(width=blocks["tal"].rect.width, height=BAR_H - 0.06,
                      stroke_color=C_TAL, stroke_width=2.0).move_to(blocks["tal"].rect.get_center()),
            num_dashes=16,
        )
        target_x = 4.05  # width = 2.00 -> spans [3.05, 5.05], clearly past bar end (1.85)
        flows_lab = T("flows on: up to ~25%", size=26, color=C_TAL).move_to([4.25, BAR_Y1 + 0.50, 0])

        self.add(ghost)
        self.play(
            FadeOut(est_tag, run_time=0.4),
            blocks["tal"].animate(run_time=1.3).move_to([target_x, BAR_YC, 0]),
            FadeIn(flows_lab, shift=UP * 0.1, run_time=0.9),
        )

        # Cue: segments downstream normally take back only about 8% -> PURPLE + BLUE glow under bracket
        self.at("segments downstream")
        p_left = blocks["dct"].rect.get_left()[0]
        b_right = blocks["cd"].rect.get_right()[0]
        b_mid = 0.5 * (p_left + b_right)
        bracket = VMobject(stroke_color=TEXT, stroke_width=2.8, fill_opacity=0)
        bracket.set_points_as_corners([
            [p_left, BAR_Y1 + 0.06, 0],
            [p_left, BAR_Y1 + 0.18, 0],
            [b_right, BAR_Y1 + 0.18, 0],
            [b_right, BAR_Y1 + 0.06, 0],
        ])
        b_stem = Line([b_mid, BAR_Y1 + 0.18, 0], [b_mid, BAR_Y1 + 0.30, 0], color=TEXT, stroke_width=2.6)
        ds_lab = T("downstream: ~8%", size=26, color=TEXT).move_to([0.85, BAR_Y1 + 0.54, 0])

        self.play(FadeOut(thin_labels), run_time=0.25)
        self.play(
            blocks["dct"].rect.animate.set_fill(opacity=0.65).set_stroke(width=4.5),
            blocks["cd"].rect.animate.set_fill(opacity=0.65).set_stroke(width=4.5),
            Create(bracket),
            Create(b_stem),
            FadeIn(ds_lab, shift=UP * 0.08),
            run_time=0.85,
        )
        self.finish()


class S08Enac(SpokenScene):
    """Push-in on one BLUE collecting duct cell; crowded Na+ drops through ENaC alone with +."""

    def construct(self):
        cell = build_single_cell(
            seg_key="cd", door_x=-1.25, show_door=True,
            door_glow=True, apical_white=False, baso_slate=False, show_pump=True,
        )
        enac_lab = T("ENaC", size=28, color=C_CD, weight=BOLD).move_to([-2.48, 0.55, 0])
        pump_lab = T("Na⁺-K⁺ pump", size=26, color=C_PUMP).move_to([2.25, -2.40, 0])
        ions = make_cell_ion_system(
            door_x=-1.25, enter_rate=0.0, pump_on=1.0, with_plus=True, crowded=True, seed=15,
        )
        tag = make_scope_tag()

        # Glide right and push into the BLUE collecting duct cell
        stage = VGroup(cell, cell.pump, enac_lab, pump_lab, ions)
        stage.scale(0.84).shift(LEFT * 0.45 + UP * 0.05)
        self.add(stage, tag)
        self.play(
            stage.animate.scale(1.0 / 0.84).shift(RIGHT * 0.45 + DOWN * 0.05),
            run_time=2.6,
            rate_func=smooth,
        )

        # Cue: ENaC lets sodium in alone -> Na+ with white + signs drop through open ENaC channel
        self.at("lets sodium in alone")
        alone_lab = T("sodium alone", size=28, color=C_NA, weight=BOLD).move_to([-1.82, -1.15, 0])
        self.play(
            ions.enter_tr.animate.set_value(1.0),
            FadeIn(alone_lab, shift=UP * 0.1),
            Indicate(cell.door, color=WHITE, scale_factor=1.12),
            run_time=1.0,
        )
        self.finish()


class S09Predict(SpokenScene):
    """Positive charge leaves lumen through ENaC; blank charge meter at 0; predict question."""

    def construct(self):
        lumen_x1 = 3.65
        cell = build_single_cell(
            seg_key="cd", door_x=-1.25, show_door=True,
            door_glow=True, apical_white=False, baso_slate=False, show_pump=True,
            lumen_x1=lumen_x1, right_open=False,
        )
        enac_lab = T("ENaC", size=28, color=C_CD, weight=BOLD).move_to([-2.48, 0.55, 0])
        alone_lab = T("sodium alone", size=28, color=C_NA, weight=BOLD).move_to([-1.82, -1.15, 0])
        pump_lab = T("Na⁺-K⁺ pump", size=26, color=C_PUMP).move_to([2.25, -2.40, 0])
        ions = make_cell_ion_system(
            door_x=-1.25, enter_rate=1.0, pump_on=1.0, with_plus=True,
            lumen_x1=lumen_x1, crowded=True, seed=15,
        )
        meter = make_charge_meter(center=(5.12, 2.02, 0), val=0.0)
        tag = make_scope_tag()

        self.add(cell, cell.pump, enac_lab, alone_lab, pump_lab, ions, tag)

        # Cue: positive charge is leaving -> bring in schematic charge meter at zero
        self.at("positive charge")
        self.play(FadeIn(meter, shift=LEFT * 0.2), run_time=0.85)

        # Cue: What happens to the charge -> white question card across top
        self.at("What happens")
        q = question_card("What charge is left behind?", y=3.30, color=WHITE, size=34)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.65)
        self.finish()


class S10Pause(PredictPause):
    """4.5 s predict pause: question holds, Na+ bobs, ENaC shimmers, needle trembles, pump turns."""
    QUESTION = "What charge is left behind?"
    CARD = {"y": 3.30, "color": WHITE, "size": 34}
    RING_AT = (5.88, 3.45, 0)
    SECONDS = 4.5

    def backdrop(self):
        lumen_x1 = 3.65
        cell = build_single_cell(
            seg_key="cd", door_x=-1.25, show_door=True,
            door_glow=True, apical_white=False, baso_slate=False, show_pump=True,
            pump_speed=1.1, lumen_x1=lumen_x1, right_open=False,
        )
        enac_lab = T("ENaC", size=28, color=C_CD, weight=BOLD).move_to([-2.48, 0.55, 0])
        alone_lab = T("sodium alone", size=28, color=C_NA, weight=BOLD).move_to([-1.82, -1.15, 0])
        pump_lab = T("Na⁺-K⁺ pump", size=26, color=C_PUMP).move_to([2.25, -2.40, 0])
        ions = make_cell_ion_system(
            door_x=-1.25, enter_rate=1.0, pump_on=1.0, with_plus=True,
            lumen_x1=lumen_x1, crowded=True, bob_only=True, seed=15,
        )
        meter = make_charge_meter(center=(5.12, 2.02, 0), val=0.0)
        tag = make_scope_tag()

        # Deliberate visual-note idle details for the pause: ENaC shimmers faintly, needle trembles at 0
        cell.pump.set_z_index(2)
        self.add(cell.pump)
        return VGroup(cell, enac_lab, alone_lab, pump_lab, ions, meter, tag)


class S11Answer(SpokenScene):
    """Lumen goes negative, meter swings left, ROMK opens and K+ leaves into the urine cup."""

    def construct(self):
        lumen_x1 = 3.65
        cell = build_single_cell(
            seg_key="cd", door_x=-1.25, show_door=True,
            door_glow=True, apical_white=False, baso_slate=False, show_pump=True,
            lumen_x1=lumen_x1, right_open=True,
        )
        enac_lab = T("ENaC", size=28, color=C_CD, weight=BOLD).move_to([-2.48, 0.55, 0])
        alone_lab = T("sodium alone", size=28, color=C_NA, weight=BOLD).move_to([-1.82, -1.15, 0])
        pump_lab = T("Na⁺-K⁺ pump", size=26, color=C_PUMP).move_to([2.25, -2.40, 0])
        meter = make_charge_meter(center=(5.12, 2.02, 0), val=0.0)
        q = question_card("What charge is left behind?", y=3.30, color=WHITE, size=34)

        # Compact urine cup at right edge of frame below the charge meter
        cup = make_urine_cup(x0=4.55, x1=5.95, y0=-1.65, y1=0.25, fill_tracker=ValueTracker(0.28), label=True)
        ions = make_cell_ion_system(
            door_x=-1.25, enter_rate=1.0, pump_on=1.0, with_plus=True,
            lumen_x1=lumen_x1, crowded=True, romk_on=0.0, romk_x=1.35,
            cup_target=(5.25, -1.05), seed=15,
        )
        tag = make_scope_tag()

        self.add(cell, cell.pump, enac_lab, alone_lab, pump_lab, meter, cup, ions, q, tag)

        # Cue: It goes negative -> dissolve question, swing needle to negative, scatter white minus signs
        # Placed cleanly in the upper lumen strip above the Na+ stream so no + signs collide with them
        self.at("goes negative")
        minus_coords = [
            (-5.4, 2.48), (-3.9, 2.45), (-2.4, 2.50), (-0.9, 2.46),
            (0.6, 2.49), (2.0, 2.46), (3.1, 2.48),
        ]
        minuses = VGroup(*[M("−", size=34, color=C_CHARGE).move_to([x, y, 0]) for x, y in minus_coords])
        neg_lab = T("negative", size=26, color=C_CHARGE, weight=BOLD).move_to([5.12, 3.22, 0])

        self.play(
            FadeOut(q, run_time=0.45),
            meter.tracker.animate(run_time=1.0).set_value(-0.82),
            FadeIn(minuses, lag_ratio=0.08, run_time=0.9),
            FadeIn(neg_lab, shift=UP * 0.08, run_time=0.6),
        )

        # Cue: drives potassium out of the cell -> MAGENTA ROMK opens and K+ rises into lumen & urine
        self.at("drives potassium")
        romk_door = make_door("romk", [1.35, Z_CELL_Y1, 0], C_K, scale=1.55)
        self.play(
            FadeIn(romk_door, scale=0.8),
            ions.romk_tr.animate.set_value(1.0),
            cup.fill_tracker.animate.set_value(0.54),
            run_time=1.2,
        )

        # Cue: potassium channel called ROMK -> reveal ROMK label
        self.at("potassium channel")
        romk_lab = T("ROMK", size=28, color=C_K, weight=BOLD).move_to([2.48, 0.55, 0])
        self.play(
            FadeIn(romk_lab, shift=UP * 0.1),
            Indicate(romk_door, color=WHITE, scale_factor=1.12),
            run_time=0.85,
        )
        self.finish()


class S12Idea(SpokenScene):
    """The one idea on the whole tube: four doors, one pump, upstream block -> ENaC -> potassium."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=True, show_pumps=True,
                                 tal_blocked=False, show_bar=False, cup_fill=0.28)
        ions = make_tube_ion_system(tal_open_val=1.0, k_rate_val=0.14, na_load_val=0.88, seed=7)
        tag = make_scope_tag()

        self.add(world, ions, tag)

        # Cue: Every segment has its own sodium door -> 4 doors light in turn
        self.at("its own sodium door")
        self.play(
            LaggedStart(
                *[Indicate(world.doors[k], color=WHITE, scale_factor=1.28, run_time=0.55)
                  for k in ("pt", "tal", "dct", "cd")],
                lag_ratio=0.35,
            )
        )

        # Cue: every door runs on one pump -> all RED pumps pulse together
        self.at("one pump")
        pump_rings = VGroup(*[
            Circle(radius=0.34, stroke_color=C_PUMP, stroke_width=4.0).move_to(world.pumps[k].get_center())
            for k in ("pt", "tal", "dct", "cd")
        ])
        self.play(FadeIn(pump_rings, scale=0.7), run_time=0.35)
        self.play(
            *[Indicate(world.pumps[k], color=C_PUMP, scale_factor=1.22) for k in ("pt", "tal", "dct", "cd")],
            FadeOut(pump_rings),
            run_time=0.85,
        )

        # Cue: Block an upstream door -> padlocked ORANGE door closes and glows
        self.at("Block an upstream door")
        closed_lock = make_padlock([SEG_MID["tal"], LUMEN_Y0 + 0.04, 0], C_TAL, locked=True, scale=1.05)
        dark_tal = make_door("tal", [SEG_MID["tal"], LUMEN_Y0, 0], C_TAL, scale=0.95, dark=True)
        lock_glow = RoundedRectangle(
            corner_radius=0.12, width=1.06, height=0.62,
            stroke_color=C_TAL, stroke_width=4.5, fill_color=C_TAL, fill_opacity=0.18,
        ).move_to([SEG_MID["tal"], LUMEN_Y0, 0])
        self.play(
            FadeIn(closed_lock, shift=DOWN * 0.25),
            FadeIn(lock_glow),
            Transform(world.doors["tal"], dark_tal),
            ions.tal_open.animate.set_value(0.0),
            run_time=0.8,
        )

        # Cue: the sodium it misses reaches ENaC -> highlight thick yellow flow toward BLUE
        self.at("the sodium it misses")
        self.play(
            Indicate(world.doors["cd"], color=C_NA, scale_factor=1.25),
            run_time=0.85,
        )

        # Cue: More potassium is secreted -> strong MAGENTA stream + top white headline
        self.at("More potassium")
        head = T("Missed sodium costs potassium", size=38, color=WHITE, weight=BOLD).move_to([0.0, 3.24, 0])
        self.play(
            ions.k_rate.animate.set_value(0.95),
            world.cup_ft.animate.set_value(0.52),
            FadeIn(head, shift=UP * 0.1),
            run_time=1.0,
        )
        self.finish()


class S13Scope(SpokenScene):
    """Whole-tube view: 'sodium arriving' slider scales Na+ & K+ streams; aldosterone adds more K+."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=True, show_pumps=True,
                                 tal_blocked=True, show_bar=False, cup_fill=0.32)
        closed_lock = make_padlock([SEG_MID["tal"], LUMEN_Y0 + 0.04, 0], C_TAL, locked=True, scale=1.05)
        # Start low on sodium arriving so the slider sweep visibly thickens both streams
        ions = make_tube_ion_system(tal_open_val=0.0, k_rate_val=0.22, na_load_val=0.30, aldo_val=0.0, seed=7)
        tag = make_scope_tag()

        # Simple top-left slider driven by one ValueTracker s_tr in [0, 1] (schematic, no numbers)
        s_tr = ValueTracker(0.15)
        sx0, sx1, sy = -4.95, -1.75, 3.00
        track = Line([sx0, sy, 0], [sx1, sy, 0], color=TEXT, stroke_width=5.0)
        fill_bar = always_redraw(lambda: Line(
            [sx0, sy, 0], [sx0 + s_tr.get_value() * (sx1 - sx0), sy, 0],
            color=C_NA, stroke_width=6.0,
        ))
        knob = always_redraw(lambda: Dot(
            [sx0 + s_tr.get_value() * (sx1 - sx0), sy, 0],
            radius=0.14, color=C_NA, stroke_color=WHITE, stroke_width=2.5,
        ))
        sl_title = T("sodium arriving", size=26, color=C_NA).move_to([0.5 * (sx0 + sx1), sy + 0.42, 0])
        sl_lo = T("low", size=22, color=TEXT).next_to([sx0, sy, 0], LEFT, buff=0.18)
        sl_hi = T("high", size=22, color=TEXT).next_to([sx1, sy, 0], RIGHT, buff=0.18)
        slider = VGroup(track, fill_bar, knob, sl_title, sl_lo, sl_hi)

        # Couple Na+ load and baseline K+ rate directly to slider tracker s_tr
        def _sync_slider(mob):
            v = float(np.clip(s_tr.get_value(), 0.0, 1.0))
            ions.na_load.set_value(0.25 + 0.72 * v)
            ions.k_rate.set_value(0.14 + 0.56 * v)

        ions.add_updater(_sync_slider)

        self.add(world, closed_lock, ions, tag)
        self.play(FadeIn(slider, shift=DOWN * 0.1), run_time=0.65)

        # Cue: extra sodium and flow arrive -> slide from low to high
        self.at("extra sodium")
        self.play(
            s_tr.animate.set_value(0.88),
            world.cup_ft.animate.set_value(0.50),
            run_time=2.2,
            rate_func=smooth,
        )

        # Cue: aldosterone -> blue-white hormone drop drifts straight down right of 'ENaC' onto BLUE segment
        self.at("aldosterone")
        drop_x = SEG_MID["cd"] + 0.94  # x = 4.34, cleanly right of 'ENaC' (ends ~3.92) and inside BLUE [2.25, 4.55]
        drop = VGroup(
            Circle(radius=0.16, stroke_color=WHITE, stroke_width=2.5, fill_color=C_ALDO, fill_opacity=0.92),
            Polygon([-0.13, 0.07, 0], [0.13, 0.07, 0], [0.0, 0.28, 0],
                    stroke_color=WHITE, stroke_width=1.8, fill_color=C_ALDO, fill_opacity=0.92),
        ).move_to([drop_x, 3.22, 0])
        aldo_lab = T("aldosterone", size=26, color=C_ALDO, weight=BOLD).move_to([SEG_MID["cd"] - 0.35, 3.22, 0])

        cd_glow = Rectangle(
            width=SEG_BY_KEY["cd"][2] - SEG_BY_KEY["cd"][1], height=CELL_Y1 - CELL_Y0,
            stroke_color=C_ALDO, stroke_width=5.5, fill_color=C_CD, fill_opacity=0.35,
        ).move_to([SEG_MID["cd"], 0.5 * (CELL_Y0 + CELL_Y1), 0])

        self.play(FadeIn(drop), FadeIn(aldo_lab, shift=DOWN * 0.08), run_time=0.6)
        self.play(
            drop.animate.move_to([drop_x, LUMEN_Y1 + 0.02, 0]),
            run_time=1.0,
            rate_func=smooth,
        )
        self.play(
            FadeOut(drop, scale=0.6),
            FadeIn(cd_glow),
            ions.aldo.animate.set_value(0.35),
            world.cup_ft.animate.set_value(0.68),
            run_time=1.0,
        )
        self.finish()


class S14Close(SpokenScene):
    """Slider & aldosterone fade; highlight traces from padlocked ORANGE door to BLUE and filling cup."""

    def construct(self):
        world = build_whole_tube(show_doors=True, show_door_labels=True, show_pumps=True,
                                 tal_blocked=True, show_bar=False, cup_fill=0.52)
        closed_lock = make_padlock([SEG_MID["tal"], LUMEN_Y0 + 0.04, 0], C_TAL, locked=True, scale=1.05)
        ions = make_tube_ion_system(tal_open_val=0.0, k_rate_val=0.72, na_load_val=0.92, aldo_val=0.25, seed=7)
        tag = make_scope_tag()

        # Carry ending state of s13 slider & aldosterone label briefly, then fade cleanly
        sx0, sx1, sy = -4.95, -1.75, 3.00
        old_slider = VGroup(
            Line([sx0, sy, 0], [sx1, sy, 0], color=TEXT, stroke_width=5.0),
            Line([sx0, sy, 0], [sx0 + 0.88 * (sx1 - sx0), sy, 0], color=C_NA, stroke_width=6.0),
            Dot([sx0 + 0.88 * (sx1 - sx0), sy, 0], radius=0.14, color=C_NA, stroke_color=WHITE, stroke_width=2.5),
            T("sodium arriving", size=26, color=C_NA).move_to([0.5 * (sx0 + sx1), sy + 0.42, 0]),
            T("low", size=22, color=TEXT).next_to([sx0, sy, 0], LEFT, buff=0.18),
            T("high", size=22, color=TEXT).next_to([sx1, sy, 0], RIGHT, buff=0.18),
            T("aldosterone", size=26, color=C_ALDO, weight=BOLD).move_to([SEG_MID["cd"] - 0.35, 3.22, 0]),
        )

        self.add(world, closed_lock, ions, old_slider, tag)
        self.play(FadeOut(old_slider), run_time=0.8)

        # Follow the path with a smooth glowing focus frame moving from padlocked ORANGE door -> BLUE -> urine cup
        focus_x = ValueTracker(SEG_MID["tal"])

        focus_box = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.18, width=1.85, height=LUMEN_Y1 - CELL_Y0 + 0.04,
            stroke_color=C_NA if focus_x.get_value() < 3.8 else C_K,
            stroke_width=3.6, fill_opacity=0.0,
        ).move_to([focus_x.get_value(), 0.5 * (LUMEN_Y1 + CELL_Y0), 0]))

        self.play(FadeIn(focus_box), run_time=0.6)

        # Cue: Whatever it misses, the tube downstream has to handle -> glide focus to BLUE segment
        self.at("Whatever it misses")
        self.play(
            focus_x.animate.set_value(SEG_MID["cd"]),
            run_time=2.4,
            rate_func=smooth,
        )

        # Cue: and potassium pays the price -> glide focus onto urine cup as it fills slightly
        self.at("potassium pays")
        self.play(
            focus_x.animate.set_value(CUP_XC),
            world.cup_ft.animate.set_value(0.76),
            run_time=1.35,
            rate_func=smooth,
        )
        self.finish()


class S15End(EndCard):
    LINE = "Sodium missed upstream reaches ENaC, and more potassium is secreted."
