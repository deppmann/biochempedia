"""A Voltage With Passengers — Tubular Transport, Segment by Segment (Chapter 2)

COLOUR MAP (one colour per concept for the entire film):
- TEAL    (#3FB8C0) : proximal tubule segment (and STEMhop / schematic tag)
- ORANGE  (#F08C42) : thick ascending limb (TAL) cells and NKCC2 cotransporter door
- PURPLE  (#B388EB) : distal convoluted tubule (DCT) segment
- BLUE    (#58C4DD) : collecting duct segment
- YELLOW  (#F5D547) : sodium ions (Na+, +1) and 1-charge bar
- MAGENTA (#E86CE6) : potassium ions (K+, +1), ROMK channel, and K+ recycling loop
- CYAN    (#2CE6FF) : chloride ions (Cl-, -1) and basolateral Cl- channel
- GREEN   (#83C167) : divalent ions calcium (Ca2+) and magnesium (Mg2+, 2+) and 2-charge / share bars
- RED     (#FC6255) : basolateral Na+-K+-ATPase pump and furosemide block / padlock
- WATER   (#B8D8E8) : luminal water droplets (s02)
- TEXT    (#E8EAF0) : charge signs (+ / -), labels, headings, gauge needle
- GOLD    (#D4A843) : predict pause ring, circuit highlight accent, junction claudin markers
- GREY    (#8B93A1) : structural outlines, axis tracks, reference lines

ONE PICTURE OF THE WORLD CARRIED THROUGH THE FILM:
A longitudinal nephron cross-section (lumen above, epithelial cell layer in the middle,
blood side below) seen at two zoom levels:
  - Macro 4-segment nephron + right-side urine cup (s00, s13)
  - Close-up thick ascending limb cell with left/right neighbours, cation-selective
    paracellular junction gap, NKCC2 + ROMK apical doors, basolateral Na+-K+ pump +
    Cl- channel, and the persistent 0 to +10 mV lumen voltage gauge on the right
    (s02 through s12, and s14).

WHAT CHANGES ON SCREEN PER SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Na+ stream flows past padlocked NKCC2 to collecting duct where K+ enters lumen; Ca2+/Mg2+ (2+) stream drifts past into urine cup as camera pushes gently toward ORANGE segment. Computed from steady segment velocities and piecewise-linear paths.
- s02_record: Glass pipettes slide onto lumen ends while perfusate flows; Na+ and Cl- cross cell while water droplets bounce off apical wall; lumen + signs appear and voltage gauge needle + readout rise from 0 to +7 mV via a shared ValueTracker.
- s03_puzzle: Luminal fluid streams steadily while NKCC2 door turns on a computed 2 s cycle admitting 1 Na+, 1 K+, 2 Cl- together; tally counts +1 +1 -2 = 0 while gauge holds +7 mV with "?".
- s04_exits: Na+ exits via rotating RED pump, Cl- channel opens and Cl- exits to blood side leaving - signs below while K+ remains inside cell.
- s05_predict: Lumen fills with abundant Na+ and Cl- and scarce K+; NKCC2 pauses mid-turn waiting for K+ as question card appears above.
- s07_recycle: ROMK channel opens; K+ follows computed closed recycling loop (NKCC2 in -> ROMK out -> lumen -> NKCC2) as NKCC2 resumes 2 s cycle and + signs gather in lumen.
- s08_circuit: Cl- exit and K+ recycling loop illuminate together as one glowing electrical circuit around the door while "?" vanishes from the +7 mV gauge.
- s09_passengers: View centers on the cation-selective junction gap; + lumen drives Na+ (1 arrow) and Ca2+/Mg2+ (2 arrows) paracellularly toward blood with computed 2x velocity for 2+ ions.
- s10_numbers: Two vertical bars beside the gap rise to exp(-z*V/26.7 mV) at V=+7 mV (0.77 for z=1, 0.59 for z=2) driven by ValueTrackers synced to percentage labels while 2+ ions cross the gap.
- s11_share: Two horizontal 0-100% range bars at bottom fill to textbook estimates (60-70% Mg, 20-25% Ca) while 2+ ions continue crossing the junction.
- s12_idea: Full circuit glows with "passengers" crossing; furosemide padlock closes on NKCC2, circuit fades, + signs thin, gauge needle drops schematically below +7, and 2+ ions divert along lumen.
- s13_return: Pull back to 4-segment nephron; 2+ ions accumulate as a rising GREEN layer in the urine cup, while TEAL proximal segment glows showing greater paracellular 2+ uptake ("not in this rule").
- s14_close: Return to thick limb; padlock lifts, NKCC2 + ROMK + Cl- circuit restarts, + signs return, gauge rises back to +7 mV, and 2+ ions resume crossing the junction.
"""
from bp_parts import *

# ------------------------------------------------------------------ Film Colours
ORANGE = "#F08C42"
PURPLE = "#B388EB"
MAGENTA = "#E86CE6"
CYAN = "#2CE6FF"
WATER = "#B8D8E8"

LUMEN_FILL = "#192334"
BLOOD_FILL = "#161B26"
CELL_TINT_OP = 0.14

# Physics constants from lesson_for_context.mdx
V_LUMEN_MV = 7.0
RT_F_MV = 26.7
EQ_Z1 = float(np.exp(-1 * V_LUMEN_MV / RT_F_MV))  # ~0.7694 -> 77%
EQ_Z2 = float(np.exp(-2 * V_LUMEN_MV / RT_F_MV))  # ~0.5920 -> 59%


# ------------------------------------------------------------------ Shared Ion & Device Builders
def make_ion(kind, scale=1.0):
    """Build an ion dot matching the film colour map.
    2+ label uses size=22 in BG on a filled circle (stroke_width=0) so contrast and size pass layout checks.
    """
    if kind == "Na":
        return Dot(radius=0.12 * scale, color=YELLOW, stroke_width=0)
    if kind == "K":
        return Dot(radius=0.12 * scale, color=MAGENTA, stroke_width=0)
    if kind == "Cl":
        d = Dot(radius=0.13 * scale, color=CYAN, stroke_width=0)
        bar = Rectangle(width=0.13 * scale, height=0.032 * scale, fill_color=BG, fill_opacity=1.0, stroke_width=0)
        return VGroup(d, bar.move_to(d))
    if kind == "Ca":
        r = 0.23 * scale
        d = Dot(radius=r, color=GREEN, stroke_width=0)
        lbl = T("2+", size=max(22, int(round(22 * scale))), color=BG, weight=BOLD).move_to(d)
        return VGroup(d, lbl)
    if kind == "H2O":
        body = Circle(radius=0.13 * scale, fill_color=WATER, fill_opacity=0.85, stroke_color=WATER, stroke_width=1.5)
        shine = Dot(radius=0.035 * scale, color=TEXT, stroke_width=0).shift(UL * 0.04 * scale)
        return VGroup(body, shine)
    raise ValueError(kind)


def make_pump(center, radius=0.30, angle=0.0):
    """Basolateral Na+-K+-ATPase pump (RED wheel with spokes that rotates continuously)."""
    ring = Circle(radius=radius, stroke_color=RED, stroke_width=4.5, fill_color=RED, fill_opacity=0.20).move_to(center)
    spokes = VGroup(*[
        Line(center, center + radius * 0.85 * np.array([np.cos(a + angle), np.sin(a + angle), 0]),
             color=RED, stroke_width=3.5)
        for a in (0, 2 * PI / 3, 4 * PI / 3)
    ])
    hub = Dot(radius=0.06, color=TEXT).move_to(center)
    return VGroup(ring, spokes, hub)


def add_pump_spin(pump, speed=1.4):
    """Continuous rotation updater for the basolateral pump."""
    spokes = pump[1]
    spokes.add_updater(lambda m, dt: m.rotate(speed * dt, about_point=pump[0].get_center()))
    return pump


def make_padlock(center, scale=1.0):
    """RED furosemide padlock closed over a door."""
    shackle = Arc(radius=0.18 * scale, start_angle=0, angle=PI, stroke_color=RED, stroke_width=5 * scale).move_to(
        np.array(center) + UP * 0.19 * scale
    )
    body = RoundedRectangle(corner_radius=0.06 * scale, width=0.44 * scale, height=0.34 * scale,
                            fill_color=RED, fill_opacity=0.92, stroke_color=TEXT, stroke_width=2 * scale).move_to(
        np.array(center) - UP * 0.04 * scale
    )
    hole = Dot(radius=0.045 * scale, color=BG).move_to(body.get_center())
    return VGroup(shackle, body, hole)


def make_channel(center, color, width=0.68, height=0.36):
    """Apical or basolateral ion channel (two flanking pillars with a central pore)."""
    c = np.array(center, dtype=float)
    lw = width * 0.28
    left = RoundedRectangle(corner_radius=0.06, width=lw, height=height, fill_color=color, fill_opacity=0.85,
                            stroke_color=color, stroke_width=2).move_to(c + LEFT * (width * 0.32))
    right = RoundedRectangle(corner_radius=0.06, width=lw, height=height, fill_color=color, fill_opacity=0.85,
                             stroke_color=color, stroke_width=2).move_to(c + RIGHT * (width * 0.32))
    pore = Rectangle(width=width * 0.36, height=height * 0.85, fill_color=BG, fill_opacity=0.9,
                     stroke_width=0).move_to(c)
    return VGroup(pore, left, right)


def make_nkcc2_door(center, angle=0.0, width=1.0, height=0.42):
    """NKCC2 cotransporter door: ORANGE housing with rotating 4-pocket barrel."""
    c = np.array(center, dtype=float)
    frame = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                             fill_color=ORANGE, fill_opacity=0.22, stroke_color=ORANGE, stroke_width=3.5).move_to(c)
    wheel = VGroup(
        Circle(radius=0.22, stroke_color=ORANGE, stroke_width=3.5, fill_color=BG, fill_opacity=0.92).move_to(c),
        Line(c + LEFT * 0.20, c + RIGHT * 0.20, color=ORANGE, stroke_width=3),
        Line(c + DOWN * 0.20, c + UP * 0.20, color=ORANGE, stroke_width=3),
    ).rotate(angle, about_point=c)
    return VGroup(frame, wheel)


# ------------------------------------------------------------------ Voltage Gauge (s02..s12, s14)
class VoltageGauge(VGroup):
    """Vertical lumen voltage gauge (0 to +10 mV) at the right edge, driven by one ValueTracker."""

    def __init__(self, tracker, x=5.55, y0=-1.35, y1=1.55, show_number=True):
        super().__init__()
        self.tracker = tracker
        self.x, self.y0, self.y1 = x, y0, y1
        bar_x = x - 0.30
        self.title = T("lumen\nvoltage", size=24, color=TEXT, line_spacing=0.85).move_to([x, y1 + 0.68, 0])
        self.add(self.title)

        h = y1 - y0
        self.track = Rectangle(width=0.34, height=h, fill_color=LUMEN_FILL, fill_opacity=0.85,
                               stroke_color=GREY, stroke_width=2.5).move_to([bar_x, (y0 + y1) / 2, 0])
        self.add(self.track)

        def mk_fill():
            v = float(np.clip(tracker.get_value(), 0.0, 10.0))
            fh = max(0.02, h * (v / 10.0))
            return Rectangle(width=0.28, height=fh, fill_color=GOLD, fill_opacity=0.80, stroke_width=0).move_to(
                [bar_x, y0 + fh / 2, 0]
            )

        def mk_needle():
            v = float(np.clip(tracker.get_value(), 0.0, 10.0))
            ny = y0 + h * (v / 10.0)
            p1 = np.array([bar_x - 0.26, ny, 0])
            p2 = np.array([bar_x - 0.04, ny + 0.09, 0])
            p3 = np.array([bar_x - 0.04, ny - 0.09, 0])
            return Polygon(p1, p2, p3, fill_color=TEXT, fill_opacity=1.0, stroke_width=0)

        self.fill_bar = always_redraw(mk_fill)
        self.needle = always_redraw(mk_needle)
        self.add(self.fill_bar, self.needle)

        for mv, txt in ((0, "0"), (5, "+5"), (10, "+10")):
            ty = y0 + h * (mv / 10.0)
            self.add(Line([bar_x + 0.17, ty, 0], [bar_x + 0.29, ty, 0], color=GREY, stroke_width=2.5))
            self.add(M(txt, size=22, color=TEXT).move_to([bar_x + 0.62, ty, 0]))

        self.readout = None
        if show_number:
            self.readout = always_redraw(
                lambda: M(f"{tracker.get_value():+.1f} mV".replace(".0", ""), size=24, color=GOLD).move_to(
                    [x, y0 - 0.36, 0]
                )
            )
            self.add(self.readout)


# ------------------------------------------------------------------ Macro 4-Segment Nephron (s00, s13)
def build_macro_world(blocked=True, proximal_glow=False, cup_green_level=0.0):
    """Build the 4-segment nephron tube + urine cup (x: -6.3..6.2, y: -2.2..2.2)."""
    g = VGroup()
    segs = [
        ("proximal", TEAL, -6.30, -3.75),
        ("thick limb", ORANGE, -3.65, -1.10),
        ("distal", PURPLE, -1.00, 1.55),
        ("collecting", BLUE, 1.65, 4.20),
    ]
    y_top_lumen = 1.45
    y_apical = 0.45
    y_base = -0.75
    y_blood_bot = -1.75

    lumen_bg = Rectangle(width=10.50, height=y_top_lumen - y_apical, fill_color=LUMEN_FILL, fill_opacity=0.85,
                         stroke_width=0).move_to([-1.05, (y_top_lumen + y_apical) / 2, 0]).set_z_index(-5)
    blood_bg = Rectangle(width=10.50, height=y_base - y_blood_bot, fill_color=BLOOD_FILL, fill_opacity=0.80,
                         stroke_width=0).move_to([-1.05, (y_base + y_blood_bot) / 2, 0]).set_z_index(-5)
    g.add(lumen_bg, blood_bg)

    g.add(Line([-6.30, y_top_lumen, 0], [4.20, y_top_lumen, 0], color=GREY, stroke_width=3.5))

    doors = {}
    pumps = VGroup()
    seg_labels = VGroup()
    prox_left_cell = None
    for name, col, x0, x1 in segs:
        cx = (x0 + x1) / 2
        gap_w = 0.56 if name == "proximal" else 0.34
        c1_w = (x1 - x0 - gap_w) / 2
        for idx_c, sx in enumerate((x0 + c1_w / 2, x1 - c1_w / 2)):
            fill_op = 0.30 if (proximal_glow and name == "proximal") else CELL_TINT_OP
            cell_fill = Rectangle(width=c1_w, height=y_apical - y_base, fill_color=col, fill_opacity=fill_op,
                                  stroke_width=0).move_to([sx, (y_apical + y_base) / 2, 0]).set_z_index(-4)
            g.add(cell_fill)
            cell_lines = VGroup(
                Line([sx - c1_w / 2, y_apical, 0], [sx + c1_w / 2, y_apical, 0], color=col, stroke_width=3.5),
                Line([sx - c1_w / 2, y_base, 0], [sx + c1_w / 2, y_base, 0], color=col, stroke_width=3.5),
                Line([sx - c1_w / 2, y_base, 0], [sx - c1_w / 2, y_apical, 0], color=col, stroke_width=3),
                Line([sx + c1_w / 2, y_base, 0], [sx + c1_w / 2, y_apical, 0], color=col, stroke_width=3),
            )
            g.add(cell_lines)
            if name == "proximal" and idx_c == 0:
                prox_left_cell = cell_lines

        door_x = x0 + c1_w * 0.55
        door_box = RoundedRectangle(corner_radius=0.07, width=0.55, height=0.28, fill_color=col, fill_opacity=0.85,
                                    stroke_color=TEXT if (blocked and name == "thick limb") else col,
                                    stroke_width=2.5).move_to([door_x, y_apical, 0])
        g.add(door_box)
        doors[name] = door_box
        pump = make_pump([x1 - c1_w * 0.5, y_base, 0], radius=0.20)
        pumps.add(pump)
        lbl = T(name, size=24, color=col).move_to([cx, y_top_lumen + 0.38, 0])
        seg_labels.add(lbl)

    g.add(pumps, seg_labels)

    padlock = None
    if blocked:
        padlock = make_padlock(doors["thick limb"].get_center(), scale=0.82)
        g.add(padlock)

    blood_lbl = T("blood side", size=24, color=TEXT).move_to([-1.05, y_blood_bot - 0.32, 0])
    g.add(blood_lbl)

    # Lower cup rim (cy1=0.72) so lumen ions sail cleanly above the rim into the cup center
    cx0, cx1, cy0, cy1 = 4.60, 6.10, -1.65, 0.72
    cup_fill_base = Rectangle(width=cx1 - cx0 - 0.08, height=0.45, fill_color=BLUE, fill_opacity=0.25,
                              stroke_width=0).move_to([(cx0 + cx1) / 2, cy0 + 0.24, 0]).set_z_index(-4)
    g.add(cup_fill_base)
    if cup_green_level > 0.01:
        gh = 0.70 * cup_green_level
        cup_green = Rectangle(width=cx1 - cx0 - 0.08, height=gh, fill_color=GREEN, fill_opacity=0.65,
                              stroke_width=0).move_to([(cx0 + cx1) / 2, cy0 + 0.46 + gh / 2, 0]).set_z_index(-4)
        g.add(cup_green)
    cup_walls = VGroup(
        Line([cx0, cy1, 0], [cx0, cy0, 0], color=TEXT, stroke_width=4),
        Line([cx0, cy0, 0], [cx1, cy0, 0], color=TEXT, stroke_width=4),
        Line([cx1, cy0, 0], [cx1, cy1, 0], color=TEXT, stroke_width=4),
    )
    cup_lbl = T("urine", size=26, color=TEXT).move_to([(cx0 + cx1) / 2, cy0 - 0.35, 0])
    g.add(cup_walls, cup_lbl)

    return g, doors, pumps, padlock, (cx0, cx1, cy0, cy1), prox_left_cell


# ------------------------------------------------------------------ Close-up Thick-Limb World (s02..s12, s14)
def build_closeup_world(shift_x=0.0, show_romk=False, show_cl=False, blocked=False,
                        plus_positions=None, minus_positions=None, minus_y=None,
                        plus_count=5, minus_count=4, junction_glow=False, hide_right_cell=False):
    """Build the close-up thick-limb cell world. Returns a dict of parts for animation."""
    y_lumen_top = 2.40
    y_apical = 1.00
    y_base = -1.40
    y_blood_bot = -2.65

    lx0, lx1 = -6.30, -5.05 + shift_x
    if lx1 - lx0 < 0.7:
        lx0 = lx1 - 0.7
    mx0, mx1 = -4.65 + shift_x, 0.75 + shift_x
    gx0, gx1 = mx1, mx1 + 1.10
    rx0, rx1 = gx1, 4.15 + shift_x
    gap_cx = (gx0 + gx1) / 2

    # Spacious transporter spacing inside main cell (mx0..mx1 = 5.40 units):
    # Pump at mx0 + 1.25 and Cl- channel at mx0 + 4.30 leave 3.05 units between them for "Cl- channel".
    nkcc_x = mx0 + 2.05
    romk_x = mx0 + 3.85
    pump_x = mx0 + 1.25
    cl_x = mx0 + 4.30

    world = VGroup()

    band_x0 = lx0
    band_x1 = rx1
    lumen_bg = Rectangle(width=band_x1 - band_x0, height=y_lumen_top - y_apical,
                         fill_color=LUMEN_FILL, fill_opacity=0.85, stroke_width=0).move_to(
        [(band_x0 + band_x1) / 2, (y_lumen_top + y_apical) / 2, 0]
    ).set_z_index(-5)
    blood_bg = Rectangle(width=band_x1 - band_x0, height=y_base - y_blood_bot,
                         fill_color=BLOOD_FILL, fill_opacity=0.80, stroke_width=0).move_to(
        [(band_x0 + band_x1) / 2, (y_base + y_blood_bot) / 2, 0]
    ).set_z_index(-5)
    world.add(lumen_bg, blood_bg)
    world.add(Line([band_x0, y_lumen_top, 0], [band_x1, y_lumen_top, 0], color=GREY, stroke_width=3.5))

    def _cell_walls(x0, x1, apical_gaps=(), base_gaps=(), tint_op=CELL_TINT_OP):
        cg = VGroup()
        fill = Rectangle(width=x1 - x0, height=y_apical - y_base, fill_color=ORANGE,
                         fill_opacity=tint_op, stroke_width=0).move_to([(x0 + x1) / 2, (y_apical + y_base) / 2, 0]).set_z_index(-4)
        cg.add(fill)
        cg.add(Line([x0, y_base, 0], [x0, y_apical, 0], color=ORANGE, stroke_width=4.5))
        cg.add(Line([x1, y_base, 0], [x1, y_apical, 0], color=ORANGE, stroke_width=4.5))

        def _horiz(y, gaps):
            pts = [x0]
            for a, b in sorted(gaps):
                pts.extend([a, b])
            pts.append(x1)
            for i in range(0, len(pts), 2):
                if pts[i + 1] - pts[i] > 0.05:
                    cg.add(Line([pts[i], y, 0], [pts[i + 1], y, 0], color=ORANGE, stroke_width=4.5))

        _horiz(y_apical, apical_gaps)
        _horiz(y_base, base_gaps)
        return cg

    left_cell = _cell_walls(lx0, lx1, tint_op=0.09)
    world.add(left_cell)

    ap_gaps = [(nkcc_x - 0.50, nkcc_x + 0.50)]
    if show_romk:
        ap_gaps.append((romk_x - 0.34, romk_x + 0.34))
    ba_gaps = [(pump_x - 0.32, pump_x + 0.32)]
    if show_cl:
        ba_gaps.append((cl_x - 0.34, cl_x + 0.34))
    main_cell = _cell_walls(mx0, mx1, apical_gaps=ap_gaps, base_gaps=ba_gaps)
    world.add(main_cell)

    right_cell = _cell_walls(rx0, rx1, tint_op=0.09)
    if not hide_right_cell:
        world.add(right_cell)

    j_y = y_apical - 0.22
    j_col = GOLD if junction_glow else GREY
    j_sw = 5 if junction_glow else 3
    junction_marks = VGroup(
        Line([gx0, j_y, 0], [gx0 + 0.16, j_y, 0], color=j_col, stroke_width=j_sw),
        Line([gx1 - 0.16, j_y, 0], [gx1, j_y, 0], color=j_col, stroke_width=j_sw),
    )
    world.add(junction_marks)

    nkcc2 = make_nkcc2_door([nkcc_x, y_apical, 0])
    pump = make_pump([pump_x, y_base, 0], radius=0.32)
    world.add(nkcc2, pump)

    romk = make_channel([romk_x, y_apical, 0], MAGENTA) if show_romk else None
    if romk is not None:
        world.add(romk)
    cl_ch = make_channel([cl_x, y_base, 0], CYAN) if show_cl else None
    if cl_ch is not None:
        world.add(cl_ch)

    padlock = make_padlock([nkcc_x, y_apical + 0.02, 0], scale=1.05) if blocked else None
    if padlock is not None:
        world.add(padlock)

    plus_signs = VGroup()
    if plus_positions is not None:
        for px in plus_positions:
            plus_signs.add(T("+", size=30, color=TEXT, weight=BOLD).move_to([px, y_lumen_top - 0.34, 0]))
    elif plus_count > 0:
        pxs = np.linspace(mx0 + 0.55, gx0 - 0.15, plus_count)
        for px in pxs:
            plus_signs.add(T("+", size=30, color=TEXT, weight=BOLD).move_to([px, y_lumen_top - 0.34, 0]))
    world.add(plus_signs)

    # Minus signs keep clear of "blood side" (mx0 + 0.90) AND clear of Cl- channel exit chute (cl_x = mx0 + 4.30)
    my = minus_y if minus_y is not None else y_base - 0.50
    minus_signs = VGroup()
    if minus_positions is not None:
        for mx in minus_positions:
            minus_signs.add(T("−", size=32, color=TEXT, weight=BOLD).move_to([mx, my, 0]))
    elif minus_count > 0:
        default_mxs = [mx0 + 2.50, mx0 + 3.10, mx0 + 3.65, mx0 + 5.05][:minus_count]
        for mx in default_mxs:
            minus_signs.add(T("−", size=32, color=TEXT, weight=BOLD).move_to([mx, my, 0]))
    world.add(minus_signs)

    return {
        "world": world,
        "main_cell": main_cell,
        "right_cell": right_cell,
        "nkcc2": nkcc2,
        "pump": pump,
        "romk": romk,
        "cl_ch": cl_ch,
        "padlock": padlock,
        "junction": junction_marks,
        "plus": plus_signs,
        "minus": minus_signs,
        "coords": {
            "mx0": mx0, "mx1": mx1, "gx0": gx0, "gx1": gx1, "gap_cx": gap_cx,
            "rx0": rx0, "rx1": rx1,
            "nkcc_x": nkcc_x, "romk_x": romk_x, "pump_x": pump_x, "cl_x": cl_x,
            "y_lumen_top": y_lumen_top, "y_apical": y_apical, "y_base": y_base, "y_blood_bot": y_blood_bot,
        },
    }


def make_ion_stream(items, path_pts, speed, seed=7):
    """Create a group of ions moving continuously along a polyline path (updater-driven, computed)."""
    pts = [np.array(p, dtype=float) for p in path_pts]
    segs = [pts[i + 1] - pts[i] for i in range(len(pts) - 1)]
    lens = [float(np.linalg.norm(s)) for s in segs]
    total = sum(lens)
    cum = np.cumsum([0.0] + lens)

    def eval_pt(s):
        u = s % total
        for i in range(len(lens)):
            if u <= cum[i + 1] + 1e-9:
                f = (u - cum[i]) / max(lens[i], 1e-6)
                return pts[i] + f * segs[i]
        return pts[-1]

    rng = np.random.default_rng(seed)
    grp = VGroup()
    n = len(items)
    for idx, kind in enumerate(items):
        mob = make_ion(kind)
        mob._s = (idx / max(n, 1)) * total + float(rng.uniform(-0.08, 0.08))
        mob.move_to(eval_pt(mob._s))
        grp.add(mob)

    def upd(m, dt):
        for mob in m:
            mob._s += speed * dt
            mob.move_to(eval_pt(mob._s))

    grp.add_updater(upd)
    return grp


# ================================================================== SCENES

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        macro, doors, pumps, padlock, cup, _ = build_macro_world(blocked=True)
        tag = scope_tag("schematic")
        self.add(macro, tag)
        for p in pumps:
            add_pump_spin(p, speed=1.3)

        glow_ring = SurroundingRectangle(doors["thick limb"], corner_radius=0.1, buff=0.12,
                                         color=ORANGE, stroke_width=4)
        na_stream = make_ion_stream(
            ["Na"] * 7,
            [[-6.0, 0.85, 0], [-2.3, 0.85, 0], [0.5, 0.85, 0], [2.45, 0.85, 0], [2.45, -0.15, 0], [3.5, -1.20, 0]],
            speed=1.6, seed=11,
        )
        self.play(Create(glow_ring), FadeIn(na_stream), run_time=0.6)

        # "cost potassium"
        self.at("cost potassium")
        k_stream = make_ion_stream(
            ["K"] * 4,
            [[3.35, -0.15, 0], [3.35, 0.96, 0], [4.35, 0.96, 0], [5.35, -0.95, 0]],
            speed=1.4, seed=19,
        )
        minus_cd = VGroup(
            T("−", size=26, color=TEXT, weight=BOLD).move_to([2.15, 1.30, 0]),
            T("−", size=26, color=TEXT, weight=BOLD).move_to([3.05, 1.30, 0]),
        )
        self.play(FadeIn(k_stream), FadeIn(minus_cd), run_time=0.5)

        # "raises urinary calcium" -> large GREEN 2+ dots pass cleanly below minus signs and above cup rim
        self.at("raises urinary calcium")
        ca_stream = make_ion_stream(
            ["Ca"] * 4,
            [[-5.8, 0.92, 0], [-2.3, 0.92, 0], [1.5, 0.92, 0], [5.35, 0.92, 0], [5.35, -0.85, 0]],
            speed=1.45, seed=23,
        )
        self.play(FadeIn(ca_stream), run_time=0.5)

        # "carries no"
        self.at("carries no")
        self.play(Indicate(padlock, color=RED, scale_factor=1.18), run_time=0.6)

        # "so how"
        self.at("so how")
        q_text = T("A sodium door moves calcium?", size=38, color=TEXT, weight=BOLD).move_to([0, 3.05, 0])
        world_all = VGroup(macro, glow_ring, minus_cd, na_stream, k_stream, ca_stream)
        self.play(
            world_all.animate.scale(1.06, about_point=[-1.0, -0.2, 0]).shift(DOWN * 0.20 + LEFT * 0.15),
            FadeIn(q_text, shift=DOWN * 0.12),
            run_time=0.95,
        )
        self.finish()


class S01Title(TitleCard):
    LESSON = "Tubular Transport, Segment by Segment"
    TITLE = "A Voltage With Passengers"


class S02Record(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=0.0, show_romk=False, show_cl=False, blocked=False,
                                 plus_count=0, minus_count=0)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        tag = scope_tag("schematic")
        perfusate = make_ion_stream(
            ["Na", "Cl", "Na", "Cl", "Na"],
            [[-4.7, 1.55, 0], [3.1, 1.55, 0]],
            speed=1.15, seed=2,
        )
        self.add(cw["world"], perfusate, tag)

        # "single"
        self.at("single")
        pip_l = Polygon([-6.4, 2.25, 0], [-4.95, 2.05, 0], [-4.95, 1.35, 0], [-6.4, 1.15, 0],
                        fill_color=WATER, fill_opacity=0.22, stroke_color=TEXT, stroke_width=2.5).shift(LEFT * 1.4)
        pip_r = Polygon([4.50, 2.25, 0], [3.25, 2.05, 0], [3.25, 1.35, 0], [4.50, 1.15, 0],
                        fill_color=WATER, fill_opacity=0.22, stroke_color=TEXT, stroke_width=2.5).shift(RIGHT * 1.4)
        iso_lbl = T("isolated rabbit tubule", size=28, color=TEXT).move_to([-2.4, 3.00, 0])
        self.play(
            pip_l.animate.shift(RIGHT * 1.4),
            pip_r.animate.shift(LEFT * 1.4),
            FadeIn(iso_lbl),
            run_time=0.9,
        )

        # "salt left"
        self.at("salt left")
        na_salt = make_ion_stream(
            ["Na"] * 3,
            [[-4.2, 1.55, 0], [C["nkcc_x"], 1.30, 0], [C["nkcc_x"], -0.2, 0], [C["nkcc_x"], -2.1, 0]],
            speed=1.40, seed=3,
        )
        cl_salt = make_ion_stream(
            ["Cl"] * 3,
            [[-3.6, 1.65, 0], [C["nkcc_x"], 1.30, 0], [C["cl_x"], -0.2, 0], [C["cl_x"], -2.1, 0]],
            speed=1.40, seed=5,
        )
        self.play(FadeIn(na_salt), FadeIn(cl_salt), run_time=0.45)

        # "water stayed" -> droplets bounce cleanly between y=1.35 and y=1.65 (far below + signs at 2.06)
        self.at("water stayed")
        drops = VGroup()
        rng = np.random.default_rng(7)
        for i, wx in enumerate([-3.5, -2.0, -0.5, 1.0]):
            d = make_ion("H2O").move_to([wx, 1.50, 0])
            d._base = np.array([wx, 1.46, 0])
            d._ph = float(rng.uniform(0, TAU))
            drops.add(d)

        def bounce_h2o(m, dt):
            for idx, d in enumerate(m):
                d._ph += 2.6 * dt
                dy = abs(np.sin(d._ph)) * 0.24
                dx = 0.12 * np.sin(d._ph * 0.5 + idx)
                d.move_to(d._base + np.array([dx, dy - 0.12, 0]))

        drops.add_updater(bounce_h2o)
        water_lbl = T("water stays", size=28, color=WATER).move_to([2.0, 3.00, 0])
        self.play(FadeIn(drops), FadeIn(water_lbl), run_time=0.45)

        # "positive"
        self.at("positive")
        v_track = ValueTracker(0.0)
        gauge = VoltageGauge(v_track)
        plus_signs = VGroup(*[
            T("+", size=30, color=TEXT, weight=BOLD).move_to([px, C["y_lumen_top"] - 0.34, 0])
            for px in np.linspace(C["mx0"] + 0.55, C["gx0"] - 0.15, 5)
        ])
        self.play(FadeIn(plus_signs), FadeIn(gauge), run_time=0.25)
        self.play(v_track.animate.set_value(7.0), run_time=0.70, rate_func=smooth)

        # "about 7"
        self.at("about 7")
        about_lbl = T("about +7 mV", size=24, color=GOLD).move_to([5.55, -2.20, 0])
        self.play(FadeIn(about_lbl), run_time=0.35)
        self.finish()


class S03Puzzle(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=0.0, show_romk=False, show_cl=False, blocked=False,
                                 plus_count=5, minus_count=0)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.35)
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        tag = scope_tag("schematic")
        lumen_flow = make_ion_stream(
            ["Na", "Cl", "Na", "Cl", "Na", "Cl"],
            [[C["mx0"] - 0.8, 1.55, 0], [C["rx1"] - 0.2, 1.55, 0]],
            speed=1.35, seed=9,
        )
        self.add(cw["world"], lumen_flow, gauge, tag)

        # "nkcc2" -> centered cleanly between left wall (mx0) and NKCC2 door (nkcc_x)
        self.at("nkcc2")
        nkcc_lbl = T("NKCC2", size=26, color=ORANGE, weight=BOLD).move_to([C["mx0"] + 0.85, C["y_apical"] - 0.45, 0])
        self.play(FadeIn(nkcc_lbl), run_time=0.4)

        # "one sodium", "one potassium", "two chlorides"
        self.at("one sodium")
        i_na = make_ion("Na").move_to([C["nkcc_x"] - 0.36, C["y_apical"] + 0.45, 0])
        self.play(FadeIn(i_na, shift=DOWN * 0.12), run_time=0.3)

        self.at("one potassium")
        i_k = make_ion("K").move_to([C["nkcc_x"] - 0.10, C["y_apical"] + 0.45, 0])
        self.play(FadeIn(i_k, shift=DOWN * 0.12), run_time=0.3)

        self.at("two chlorides")
        i_cl1 = make_ion("Cl").move_to([C["nkcc_x"] + 0.18, C["y_apical"] + 0.45, 0])
        i_cl2 = make_ion("Cl").move_to([C["nkcc_x"] + 0.46, C["y_apical"] + 0.45, 0])
        self.play(FadeIn(i_cl1, shift=DOWN * 0.12), FadeIn(i_cl2, shift=DOWN * 0.12), run_time=0.35)

        # "together"
        self.at("together")
        quartet = VGroup(i_na, i_k, i_cl1, i_cl2)
        self.play(
            Rotate(cw["nkcc2"][1], angle=PI / 2, about_point=cw["nkcc2"][0].get_center()),
            quartet.animate.shift(DOWN * 1.15),
            run_time=0.6,
        )

        cycle = {"t": 0.0}
        loop_ions = VGroup(make_ion("Na"), make_ion("K"), make_ion("Cl"), make_ion("Cl"))
        loop_ions.set_opacity(0)
        self.add(loop_ions)

        def nkcc_cycle(m, dt):
            cycle["t"] = (cycle["t"] + dt) % 2.0
            ph = cycle["t"] / 2.0
            m[1].rotate((PI / 2) * dt, about_point=m[0].get_center())
            offsets = [-0.36, -0.10, 0.18, 0.46]
            y_pos = C["y_apical"] + 0.50 - 1.25 * ph
            op = 1.0 if 0.08 < ph < 0.88 else 0.0
            for ion, dx in zip(loop_ions, offsets):
                ion.move_to([C["nkcc_x"] + dx, y_pos, 0]).set_opacity(op)

        cw["nkcc2"].add_updater(nkcc_cycle)

        # "no net charge"
        self.at("no net charge")
        tally = M("+1 +1 −2 = 0", size=28, color=TEXT).move_to([C["nkcc_x"] + 0.25, -0.25, 0])
        self.play(FadeOut(quartet, run_time=0.25), FadeIn(tally), run_time=0.5)

        # "where does the voltage"
        self.at("where does the voltage")
        q_mark = T("?", size=46, color=GOLD, weight=BOLD).move_to([4.62, 0.15, 0])
        self.play(FadeIn(q_mark, scale=1.2), run_time=0.45)
        self.finish()


class S04Exits(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=0.0, show_romk=False, show_cl=False, blocked=False,
                                 plus_count=5, minus_count=0)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        nkcc_lbl = T("NKCC2", size=26, color=ORANGE, weight=BOLD).move_to([C["mx0"] + 0.85, C["y_apical"] - 0.45, 0])
        q_mark = T("?", size=46, color=GOLD, weight=BOLD).move_to([4.62, 0.15, 0])
        tag = scope_tag("schematic")
        self.add(cw["world"], gauge, nkcc_lbl, q_mark, tag)

        nk_t = {"t": 0.0}
        nk_ions = VGroup(make_ion("Na"), make_ion("K"), make_ion("Cl"), make_ion("Cl"))
        self.add(nk_ions)

        def nk_upd(m, dt):
            nk_t["t"] = (nk_t["t"] + dt) % 2.0
            ph = nk_t["t"] / 2.0
            m[1].rotate((PI / 2) * dt, about_point=m[0].get_center())
            for ion, dx in zip(nk_ions, [-0.36, -0.10, 0.18, 0.46]):
                ion.move_to([C["nkcc_x"] + dx, C["y_apical"] + 0.50 - 1.20 * ph, 0])
                ion.set_opacity(1.0 if 0.08 < ph < 0.88 else 0.0)

        cw["nkcc2"].add_updater(nk_upd)

        k_wait = VGroup(*[
            bob(make_ion("K").move_to([C["nkcc_x"] + 0.8 + 0.4 * i, -0.15 + 0.18 * (i % 2), 0]), amp=0.05, seed=i)
            for i in range(4)
        ])
        self.add(k_wait)

        # "follow each ion"
        self.at("follow each ion")
        blood_lbl = T("blood side", size=26, color=TEXT).move_to([C["mx0"] + 0.90, C["y_blood_bot"] + 0.30, 0])
        door_ring = SurroundingRectangle(cw["nkcc2"][0], corner_radius=0.1, buff=0.03, color=GOLD, stroke_width=4)
        self.play(FadeIn(blood_lbl), Create(door_ring), Indicate(cw["nkcc2"], color=ORANGE, scale_factor=1.2), run_time=0.45)

        # "sodium leaves"
        self.at("sodium leaves")
        na_exit = make_ion_stream(
            ["Na"] * 3,
            [[C["nkcc_x"], 0.20, 0], [C["pump_x"], C["y_base"], 0], [C["pump_x"], C["y_base"] - 0.72, 0]],
            speed=1.25, seed=12,
        )
        na_path = VMobject(stroke_color=YELLOW, stroke_width=6, stroke_opacity=0.75).set_points_as_corners(
            [[C["nkcc_x"], 0.20, 0], [C["pump_x"], C["y_base"], 0], [C["pump_x"], C["y_base"] - 0.72, 0]])
        self.play(FadeOut(door_ring), Create(na_path), FadeIn(na_exit), Indicate(cw["nkcc2"], color=ORANGE, scale_factor=1.2), run_time=0.45)

        self.at("the pump")
        self.play(Indicate(cw["pump"], color=RED, scale_factor=1.3), run_time=0.5)

        # "chloride leaves" -> label cleanly placed between pump and Cl- channel, far clear of both
        self.at("chloride leaves")
        cl_ch = make_channel([C["cl_x"], C["y_base"], 0], CYAN)
        cl_lbl = T("Cl− channel", size=26, color=CYAN, weight=BOLD).move_to([C["mx0"] + 2.82, C["y_base"] + 0.48, 0])
        cl_exit = make_ion_stream(
            ["Cl"] * 4,
            [[C["nkcc_x"] + 0.25, 0.20, 0], [C["cl_x"], 0.20, 0], [C["cl_x"], C["y_base"] - 0.85, 0]],
            speed=1.35, seed=17,
        )
        cl_path = VMobject(stroke_color=CYAN, stroke_width=6, stroke_opacity=0.75).set_points_as_corners(
            [[C["nkcc_x"] + 0.25, 0.20, 0], [C["cl_x"], 0.20, 0], [C["cl_x"], C["y_base"] - 0.85, 0]])
        self.play(FadeIn(cl_ch), FadeIn(cl_lbl), FadeIn(cl_exit), Create(cl_path), run_time=0.4)

        self.at("chloride channels")
        self.play(Indicate(cl_ch, color=CYAN, scale_factor=1.3), run_time=0.5)

        # "negative charge" -> minus signs straddle the Cl- channel chute without overlapping it
        self.at("negative charge")
        minus_signs = VGroup(*[
            T("−", size=32, color=TEXT, weight=BOLD).move_to([mx, C["y_base"] - 0.50, 0])
            for mx in [C["mx0"] + 2.50, C["mx0"] + 3.10, C["mx0"] + 3.65, C["mx0"] + 5.05]
        ])
        self.play(FadeIn(minus_signs, lag_ratio=0.15), run_time=0.65)
        self.finish()


def build_s05_end_state():
    """Exact shared builder for s05 end and s06 PredictPause backdrop."""
    cw = build_closeup_world(shift_x=0.0, show_romk=False, show_cl=True, blocked=False,
                             plus_count=5, minus_count=4)
    C = cw["coords"]
    add_pump_spin(cw["pump"], speed=0.55)
    v_track = ValueTracker(7.0)
    gauge = VoltageGauge(v_track)
    nkcc_lbl = T("NKCC2", size=26, color=ORANGE, weight=BOLD).move_to([C["mx0"] + 0.85, C["y_apical"] - 0.45, 0])
    cl_lbl = T("Cl− channel", size=26, color=CYAN, weight=BOLD).move_to([C["mx0"] + 2.82, C["y_base"] + 0.48, 0])
    blood_lbl = T("blood side", size=26, color=TEXT).move_to([C["mx0"] + 0.90, C["y_blood_bot"] + 0.30, 0])
    q_mark = T("?", size=46, color=GOLD, weight=BOLD).move_to([4.62, 0.15, 0])

    rng = np.random.default_rng(42)
    lumen_ions = VGroup()
    for _ in range(10):
        lumen_ions.add(make_ion("Na").move_to([rng.uniform(C["mx0"], C["rx1"] - 0.3), rng.uniform(1.25, 1.85), 0]))
    for _ in range(10):
        lumen_ions.add(make_ion("Cl").move_to([rng.uniform(C["mx0"], C["rx1"] - 0.3), rng.uniform(1.25, 1.85), 0]))
    lumen_ions.add(make_ion("K").move_to([C["rx1"] - 0.45, 1.62, 0]))

    k_wait = VGroup(*[
        bob(make_ion("K").move_to([C["nkcc_x"] + 0.8 + 0.4 * i, -0.15 + 0.18 * (i % 2), 0]), amp=0.05, seed=i)
        for i in range(4)
    ])

    t_acc = {"t": 0.0}
    v_track.add_updater(lambda vt, dt: (t_acc.__setitem__("t", t_acc["t"] + dt),
                                        vt.set_value(7.0 + 0.18 * np.sin(5.5 * t_acc["t"]))))

    return VGroup(cw["world"], gauge, nkcc_lbl, cl_lbl, blood_lbl, q_mark, lumen_ions, k_wait, scope_tag("schematic"))


class S05Predict(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=0.0, show_romk=False, show_cl=True, blocked=False,
                                 plus_count=5, minus_count=4)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.1)
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        nkcc_lbl = T("NKCC2", size=26, color=ORANGE, weight=BOLD).move_to([C["mx0"] + 0.85, C["y_apical"] - 0.45, 0])
        cl_lbl = T("Cl− channel", size=26, color=CYAN, weight=BOLD).move_to([C["mx0"] + 2.82, C["y_base"] + 0.48, 0])
        blood_lbl = T("blood side", size=26, color=TEXT).move_to([C["mx0"] + 0.90, C["y_blood_bot"] + 0.30, 0])
        q_mark = T("?", size=46, color=GOLD, weight=BOLD).move_to([4.62, 0.15, 0])
        tag = scope_tag("schematic")

        k_wait = VGroup(*[
            bob(make_ion("K").move_to([C["nkcc_x"] + 0.8 + 0.4 * i, -0.15 + 0.18 * (i % 2), 0]), amp=0.05, seed=i)
            for i in range(4)
        ])
        self.add(cw["world"], gauge, nkcc_lbl, cl_lbl, blood_lbl, q_mark, k_wait, tag)

        # "now potassium"
        self.at("now potassium")
        rng = np.random.default_rng(42)
        lumen_ions = VGroup()
        for _ in range(10):
            lumen_ions.add(make_ion("Na").move_to([rng.uniform(C["mx0"], C["rx1"] - 0.3), rng.uniform(1.25, 1.85), 0]))
        for _ in range(10):
            lumen_ions.add(make_ion("Cl").move_to([rng.uniform(C["mx0"], C["rx1"] - 0.3), rng.uniform(1.25, 1.85), 0]))
        lumen_ions.add(make_ion("K").move_to([C["rx1"] - 0.45, 1.62, 0]))
        for idx, ion in enumerate(lumen_ions):
            ion._vx = 0.25 if idx < 20 else 0.05
        lumen_ions.add_updater(lambda m, dt: [
            ion.shift(RIGHT * ion._vx * dt) if ion.get_x() < C["rx1"] - 0.2 else ion.move_to([C["mx0"] + 0.1, ion.get_y(), 0])
            for ion in m
        ])
        self.play(FadeIn(lumen_ions), run_time=0.55)

        # "tubular fluid"
        self.at("tubular fluid")
        self.play(Rotate(cw["nkcc2"][1], angle=PI / 4, about_point=cw["nkcc2"][0].get_center()), run_time=0.9, rate_func=there_and_back)

        # "so how does"
        self.at("so how does")
        q_card = question_card("Where does its potassium come from?", y=3.05, color=TEXT, size=34, max_w=11.0)
        self.play(FadeIn(q_card), run_time=0.55)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Where does its potassium come from?"
    CARD = {"y": 3.05, "color": TEXT, "size": 34, "max_w": 11.0}
    RING_AT = (6.05, 3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_s05_end_state()


class S07Recycle(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=0.0, show_romk=False, show_cl=True, blocked=False,
                                 plus_positions=[-4.0, -2.6], minus_count=4)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        nkcc_lbl = T("NKCC2", size=26, color=ORANGE, weight=BOLD).move_to([C["mx0"] + 0.85, C["y_apical"] - 0.45, 0])
        cl_lbl = T("Cl− channel", size=26, color=CYAN, weight=BOLD).move_to([C["mx0"] + 2.82, C["y_base"] + 0.48, 0])
        blood_lbl = T("blood side", size=26, color=TEXT).move_to([C["mx0"] + 0.90, C["y_blood_bot"] + 0.30, 0])
        q_mark = T("?", size=46, color=GOLD, weight=BOLD).move_to([4.62, 0.15, 0])
        q_card = question_card("Where does its potassium come from?", y=3.05, color=TEXT, size=34, max_w=11.0)
        tag = scope_tag("schematic")
        self.add(cw["world"], gauge, nkcc_lbl, cl_lbl, blood_lbl, q_mark, q_card, tag)

        # "it recycles"
        self.at("it recycles")
        romk = make_channel([C["romk_x"], C["y_apical"], 0], MAGENTA)
        romk_lbl = T("ROMK", size=26, color=MAGENTA, weight=BOLD).move_to([C["romk_x"] + 0.82, C["y_apical"] - 0.50, 0])
        self.play(FadeOut(q_card), FadeIn(romk), FadeIn(romk_lbl), run_time=0.55)

        # "goes back into the lumen"
        self.at("goes back into the lumen")
        loop_pts = [
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], 0.25, 0],
            [C["romk_x"], 0.25, 0],
            [C["romk_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
        ]
        loop_path = VMobject(stroke_color=MAGENTA, stroke_width=4, stroke_opacity=0.65).set_points_as_corners(loop_pts)
        k_loop = make_ion_stream(["K"] * 5, loop_pts, speed=1.9, seed=31)
        na_exit = make_ion_stream(["Na"] * 2, [[C["nkcc_x"], 0.25, 0], [C["pump_x"], C["y_base"] - 0.72, 0]], speed=1.2, seed=33)
        cl_exit = make_ion_stream(["Cl"] * 3, [[C["nkcc_x"] + 0.25, 0.12, 0], [C["cl_x"], 0.12, 0], [C["cl_x"], C["y_base"] - 0.72, 0]], speed=1.3, seed=35)
        cw["nkcc2"][1].add_updater(lambda m, dt: m.rotate((PI / 2) * dt, about_point=cw["nkcc2"][0].get_center()))
        self.play(Create(loop_path), FadeIn(k_loop), FadeIn(na_exit), FadeIn(cl_exit), run_time=0.7)

        # "channel romk"
        self.at("channel romk")
        self.play(Indicate(romk, color=MAGENTA, scale_factor=1.12), run_time=0.6)

        # "positive charge"
        self.at("positive charge")
        extra_plus = VGroup(
            T("+", size=30, color=TEXT, weight=BOLD).move_to([-1.2, C["y_lumen_top"] - 0.34, 0]),
            T("+", size=30, color=TEXT, weight=BOLD).move_to([0.2, C["y_lumen_top"] - 0.34, 0]),
        )
        self.play(FadeIn(extra_plus, shift=UP * 0.2), run_time=0.55)
        self.finish()


class S08Circuit(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=0.0, show_romk=True, show_cl=True, blocked=False,
                                 plus_count=5, minus_count=4)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        cw["nkcc2"][1].add_updater(lambda m, dt: m.rotate((PI / 2) * dt, about_point=cw["nkcc2"][0].get_center()))
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        nkcc_lbl = T("NKCC2", size=26, color=ORANGE, weight=BOLD).move_to([C["mx0"] + 0.85, C["y_apical"] - 0.45, 0])
        romk_lbl = T("ROMK", size=26, color=MAGENTA, weight=BOLD).move_to([C["romk_x"] + 0.82, C["y_apical"] - 0.50, 0])
        cl_lbl = T("Cl− channel", size=26, color=CYAN, weight=BOLD).move_to([C["mx0"] + 2.82, C["y_base"] + 0.48, 0])
        blood_lbl = T("blood side", size=26, color=TEXT).move_to([C["mx0"] + 0.90, C["y_blood_bot"] + 0.30, 0])
        q_mark = T("?", size=46, color=GOLD, weight=BOLD).move_to([4.62, 0.15, 0])
        tag = scope_tag("schematic")

        loop_pts = [
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], 0.25, 0],
            [C["romk_x"], 0.25, 0],
            [C["romk_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
        ]
        cl_pts = [[C["nkcc_x"], 0.10, 0], [C["cl_x"], 0.10, 0], [C["cl_x"], C["y_base"] - 0.70, 0]]
        loop_line = VMobject(stroke_color=MAGENTA, stroke_width=4, stroke_opacity=0.55).set_points_as_corners(loop_pts)
        cl_line = VMobject(stroke_color=CYAN, stroke_width=4, stroke_opacity=0.55).set_points_as_corners(cl_pts)
        k_loop = make_ion_stream(["K"] * 5, loop_pts, speed=1.9, seed=41)
        cl_exit = make_ion_stream(["Cl"] * 4, cl_pts, speed=1.35, seed=43)
        na_exit = make_ion_stream(["Na"] * 2, [[C["nkcc_x"], 0.25, 0], [C["pump_x"], C["y_base"] - 0.70, 0]], speed=1.2, seed=45)

        self.add(cw["world"], gauge, nkcc_lbl, romk_lbl, cl_lbl, blood_lbl, q_mark,
                 loop_line, cl_line, k_loop, cl_exit, na_exit, tag)

        # "negative charge"
        self.at("negative charge")
        self.play(cl_line.animate.set_stroke(width=8, opacity=1.0), run_time=0.55)

        # "positive charge"
        self.at("positive charge")
        self.play(loop_line.animate.set_stroke(width=8, opacity=1.0), Indicate(cw["plus"], color=TEXT, scale_factor=1.3), run_time=0.8)

        # "ends up"
        self.at("ends up")
        self.play(Indicate(gauge.track, color=GOLD, scale_factor=1.12), run_time=0.8)

        # "a few millivolts"
        self.at("a few millivolts")
        self.play(FadeOut(q_mark), run_time=0.45)

        # "the circuit around"
        self.at("the circuit around")
        circuit_lbl = T("circuit", size=28, color=GOLD, weight=BOLD).move_to([(C["nkcc_x"] + C["romk_x"]) / 2, -0.32, 0])
        onecell_tag = T("classic one-cell picture", size=24, color=TEXT).move_to([-4.2, -3.15, 0])
        self.play(
            loop_line.animate.set_stroke(color=GOLD, width=8),
            cl_line.animate.set_stroke(color=GOLD, width=8),
            FadeIn(circuit_lbl),
            FadeIn(onecell_tag),
            run_time=0.6,
        )
        self.finish()


class S09Passengers(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=-0.65, show_romk=True, show_cl=True, blocked=False,
                                 plus_count=5, minus_count=4, junction_glow=True)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        cw["nkcc2"][1].add_updater(lambda m, dt: m.rotate((PI / 2) * dt, about_point=cw["nkcc2"][0].get_center()))
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        blood_lbl = T("blood side", size=26, color=TEXT).move_to([C["mx0"] + 0.90, C["y_blood_bot"] + 0.30, 0])
        tag = scope_tag("schematic")

        k_loop = make_ion_stream(
            ["K"] * 4,
            [[C["nkcc_x"], 1.45, 0], [C["nkcc_x"], 0.22, 0], [C["romk_x"], 0.22, 0], [C["romk_x"], 1.45, 0], [C["nkcc_x"], 1.45, 0]],
            speed=1.7, seed=51,
        )
        self.add(cw["world"], gauge, blood_lbl, k_loop, tag)

        # "the junctions" -> 3-line wrapped label cleanly centered inside right neighbour cell
        self.at("the junctions")
        j_lbl = T("cation-\nselective\njunction", size=24, color=GOLD, weight=BOLD, line_spacing=0.85).move_to(
            [C["rx0"] + 1.25, 0.22, 0]
        )
        j_arr = Arrow([C["rx0"] + 0.50, 0.78, 0], [C["rx0"] - 0.05, 0.78, 0],
                      color=GOLD, stroke_width=3.5, buff=0.02, tip_length=0.16)
        self.play(FadeIn(j_lbl), GrowArrow(j_arr), run_time=0.55)

        self.at("cations through")
        self.play(Indicate(cw["junction"], color=GOLD, scale_factor=1.4), Indicate(j_lbl, color=GOLD, scale_factor=1.12), run_time=0.9)

        # "positive lumen"
        self.at("positive lumen")
        gx = C["gap_cx"]
        na_gap = make_ion_stream(["Na"] * 3, [[gx - 0.25, 1.60, 0], [gx - 0.22, -2.05, 0]], speed=0.85, seed=53)
        ca_gap = make_ion_stream(["Ca"] * 3, [[gx + 0.16, 1.60, 0], [gx + 0.16, -2.05, 0]], speed=1.70, seed=55)
        self.play(FadeIn(na_gap), FadeIn(ca_gap), run_time=0.55)

        # "two charges"
        self.at("two charges")
        def attach_arrows(stream, double=False):
            arrows = VGroup()
            for ion in stream:
                if double:
                    a = VGroup(
                        Arrow(ORIGIN, DOWN * 0.36, color=GREEN, stroke_width=3.0, tip_length=0.12),
                        Arrow(ORIGIN, DOWN * 0.36, color=GREEN, stroke_width=3.0, tip_length=0.12).shift(RIGHT * 0.10),
                    )
                    a._host = ion
                    a.add_updater(lambda m: m.next_to(m._host, RIGHT, buff=0.03))
                else:
                    a = Arrow(ORIGIN, DOWN * 0.36, color=YELLOW, stroke_width=3.0, tip_length=0.12)
                    a._host = ion
                    a.add_updater(lambda m: m.next_to(m._host, LEFT, buff=0.04))
                arrows.add(a)
            return arrows

        na_arrs = attach_arrows(na_gap, double=False)
        ca_arrs = attach_arrows(ca_gap, double=True)
        self.play(FadeIn(na_arrs), FadeIn(ca_arrs), run_time=0.5)

        # "pushed twice as hard"
        self.at("pushed twice as hard")
        twice_lbl = T("2× push", size=26, color=GREEN, weight=BOLD).move_to([C["rx0"] + 1.25, -0.78, 0])
        self.play(FadeIn(twice_lbl), run_time=0.45)
        self.finish()


class S10Numbers(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=-0.65, show_romk=True, show_cl=True, blocked=False,
                                 plus_count=5, minus_count=4, junction_glow=True, hide_right_cell=True)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        cw["nkcc2"][1].add_updater(lambda m, dt: m.rotate((PI / 2) * dt, about_point=cw["nkcc2"][0].get_center()))
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        blood_lbl = T("blood side", size=26, color=TEXT).move_to([C["mx0"] + 0.90, C["y_blood_bot"] + 0.30, 0])
        tag = scope_tag("schematic")

        gx = C["gap_cx"]
        ca_gap = make_ion_stream(["Ca"] * 3, [[gx, 1.62, 0], [gx, -2.05, 0]], speed=1.55, seed=61)
        k_loop = make_ion_stream(
            ["K"] * 4,
            [[C["nkcc_x"], 1.45, 0], [C["nkcc_x"], 0.22, 0], [C["romk_x"], 0.22, 0], [C["romk_x"], 1.45, 0], [C["nkcc_x"], 1.45, 0]],
            speed=1.7, seed=63,
        )
        self.add(cw["world"], gauge, blood_lbl, ca_gap, k_loop, tag)

        # Bars beside the gap (x = 1.94..4.01, y = -2.18..-0.40)
        bar_h = 1.78
        bar_w = 0.72
        by0 = -2.18
        x_b1, x_b2 = 2.30, 3.65
        panel_cx = (x_b1 + x_b2) / 2

        bars_title = T("lumen level relative\nto blood level", size=24, color=TEXT, line_spacing=0.85).move_to([panel_cx, 3.05, 0])
        blood_top = T("blood level", size=22, color=TEXT).move_to([panel_cx, by0 + bar_h + 0.24, 0])
        out1 = Rectangle(width=bar_w, height=bar_h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([x_b1, by0 + bar_h / 2, 0])
        out2 = Rectangle(width=bar_w, height=bar_h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([x_b2, by0 + bar_h / 2, 0])

        self.play(FadeIn(bars_title), FadeIn(blood_top), FadeIn(out1), FadeIn(out2), run_time=0.6)

        # "plus 7"
        self.at("plus 7")
        self.play(Indicate(gauge.readout, color=GOLD, scale_factor=1.18), run_time=0.8)

        # Formula built piece by piece above the bars (y = 1.25..2.22, centered at panel_cx)
        # "lumen over blood"
        self.at("lumen over blood")
        eq_lhs = M("lumen / blood =", size=22, color=TEXT).move_to([panel_cx, 2.10, 0])
        self.play(FadeIn(eq_lhs), run_time=0.55)

        # "e to the"
        self.at("e to the")
        frac_y = 1.54
        frac_w = 1.70
        exp_open = M("exp(", size=22, color=TEXT).move_to([panel_cx - frac_w / 2 - 0.46, frac_y, 0])
        exp_close = M(")", size=22, color=TEXT).move_to([panel_cx + frac_w / 2 + 0.24, frac_y, 0])
        self.play(FadeIn(exp_open), FadeIn(exp_close), run_time=0.4)

        # "minus charge" -> show -z in numerator (pre-centered as a pair over frac_line)
        self.at("minus charge")
        num_pair = VGroup(M("−z", size=22, color=TEXT), M("× V", size=22, color=TEXT)).arrange(RIGHT, buff=0.10)
        num_pair.move_to([panel_cx, frac_y + 0.28, 0])
        num_z, num_v = num_pair[0], num_pair[1]
        self.play(FadeIn(num_z), run_time=0.4)

        # "times voltage" -> show x V in numerator
        self.at("times voltage")
        self.play(FadeIn(num_v), run_time=0.45)

        # "26" -> show fraction line and 26.7 mV in denominator (never before spoken)
        self.at("26")
        frac_line = Line([panel_cx - frac_w / 2, frac_y, 0], [panel_cx + frac_w / 2, frac_y, 0], color=TEXT, stroke_width=2.5)
        den_rt = M("26.7 mV", size=22, color=TEXT).move_to([panel_cx, frac_y - 0.28, 0])
        self.play(Create(frac_line), FadeIn(den_rt), run_time=0.75)

        # "put in" -> substitute V -> 7 mV (compute cleanly centered numerator)
        self.at("put in")
        num_old = VGroup(num_z, num_v)
        num_new = M("−z × 7 mV", size=22, color=GOLD).move_to([panel_cx, frac_y + 0.28, 0])
        self.play(
            Indicate(gauge.readout, color=GOLD, scale_factor=1.15),
            swap(num_old, num_new, run_time=0.7),
            run_time=0.75,
        )

        # Helper for downward arrow inside each bar outline as lumen level falls
        def make_down_arrow(x, tracker):
            def mk():
                top_y = by0 + bar_h - 0.07
                bot_y = by0 + bar_h * tracker.get_value() + 0.06
                if top_y - bot_y < 0.16:
                    return VGroup()
                return Arrow([x, top_y, 0], [x, bot_y, 0], color=TEXT, stroke_width=3.2, buff=0, tip_length=0.12)
            return always_redraw(mk)

        # Case 1: "for one charge" -> yellow bar starts at blood level (1.0), no % number yet
        self.at("for one charge")
        f1 = ValueTracker(1.0)
        fill1 = always_redraw(lambda: Rectangle(
            width=bar_w - 0.06, height=max(0.02, bar_h * f1.get_value()),
            fill_color=YELLOW, fill_opacity=0.84, stroke_width=0
        ).move_to([x_b1, by0 + max(0.02, bar_h * f1.get_value()) / 2, 0]))
        arr1 = make_down_arrow(x_b1, f1)
        lbl1 = T("one\ncharge", size=22, color=YELLOW, line_spacing=0.85).move_to([x_b1, by0 - 0.40, 0])
        z1_row = VGroup(
            M("z = 1 →", size=22, color=YELLOW),
            M("0.77 (77%)", size=22, color=YELLOW),
        ).arrange(RIGHT, buff=0.14).move_to([panel_cx, 0.58, 0])
        z1_lhs, z1_rhs = z1_row[0], z1_row[1]
        self.add(fill1, arr1)
        self.play(FadeIn(fill1), FadeIn(lbl1), FadeIn(z1_lhs), run_time=0.6)

        # "the lumen can fall" -> bar falls from 1.0 down to EQ_Z1 while downward arrow grows inside outline
        self.at("the lumen can fall")
        self.play(f1.animate.set_value(EQ_Z1), run_time=1.5, rate_func=smooth)

        # "77" -> reveal 0.77 (77%) and 77% inside bar 1
        self.at("77")
        pct1 = M("77%", size=22, color=BG, weight=BOLD).move_to([x_b1, by0 + bar_h * EQ_Z1 * 0.5, 0])
        self.play(FadeIn(z1_rhs), FadeIn(pct1), run_time=0.45)

        # Case 2: "for two charges" -> green bar starts at blood level (1.0), no % number yet
        self.at("for two charges")
        f2 = ValueTracker(1.0)
        fill2 = always_redraw(lambda: Rectangle(
            width=bar_w - 0.06, height=max(0.02, bar_h * f2.get_value()),
            fill_color=GREEN, fill_opacity=0.84, stroke_width=0
        ).move_to([x_b2, by0 + max(0.02, bar_h * f2.get_value()) / 2, 0]))
        arr2 = make_down_arrow(x_b2, f2)
        lbl2 = T("two\ncharges", size=22, color=GREEN, line_spacing=0.85).move_to([x_b2, by0 - 0.40, 0])
        z2_row = VGroup(
            M("z = 2 →", size=22, color=GREEN),
            M("0.59 (59%)", size=22, color=GREEN),
        ).arrange(RIGHT, buff=0.14).move_to([panel_cx, 0.24, 0])
        z2_lhs, z2_rhs = z2_row[0], z2_row[1]
        self.add(fill2, arr2)
        self.play(FadeIn(fill2), FadeIn(lbl2), FadeIn(z2_lhs), run_time=0.6)

        # "as low as" (second occurrence) -> bar 2 falls from 1.0 down to EQ_Z2
        self.at("as low as", nth=1)
        self.play(f2.animate.set_value(EQ_Z2), run_time=0.65, rate_func=smooth)

        # "59" -> reveal 0.59 (59%) and 59% inside bar 2
        self.at("59")
        pct2 = M("59%", size=22, color=BG, weight=BOLD).move_to([x_b2, by0 + bar_h * EQ_Z2 * 0.5, 0])
        self.play(FadeIn(z2_rhs), FadeIn(pct2), run_time=0.45)

        # "equilibrium limit"
        self.at("equilibrium limit")
        lim_tag = T("equilibrium limit, not measured", size=24, color=GOLD).move_to([1.50, -3.18, 0])
        self.play(FadeIn(lim_tag), run_time=0.45)
        self.finish()


class S11Share(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=-0.65, show_romk=True, show_cl=True, blocked=False,
                                 plus_count=5, minus_count=4, minus_y=-1.75, junction_glow=True)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        cw["nkcc2"][1].add_updater(lambda m, dt: m.rotate((PI / 2) * dt, about_point=cw["nkcc2"][0].get_center()))
        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track)
        tag = scope_tag("schematic")

        gx = C["gap_cx"]
        ca_gap = make_ion_stream(["Ca"] * 3, [[gx, 1.62, 0], [gx, -1.75, 0]], speed=1.55, seed=71)
        k_loop = make_ion_stream(
            ["K"] * 4,
            [[C["nkcc_x"], 1.45, 0], [C["nkcc_x"], 0.22, 0], [C["romk_x"], 0.22, 0], [C["romk_x"], 1.45, 0], [C["nkcc_x"], 1.45, 0]],
            speed=1.7, seed=73,
        )
        self.add(cw["world"], gauge, ca_gap, k_loop, tag)

        def make_range_bar(title_str, lo, hi, x0, x1, y):
            w = x1 - x0
            track = Rectangle(width=w, height=0.32, fill_color=LUMEN_FILL, fill_opacity=0.9,
                              stroke_color=GREY, stroke_width=2.5).move_to([(x0 + x1) / 2, y, 0])
            t0 = M("0%", size=22, color=TEXT).move_to([x0, y - 0.34, 0])
            t100 = M("100%", size=22, color=TEXT).move_to([x1, y - 0.34, 0])
            lbl = T(title_str, size=26, color=GREEN, weight=BOLD).move_to([(x0 + x1) / 2, y + 0.44, 0])
            prog = ValueTracker(0.0)
            band = always_redraw(lambda: Rectangle(
                width=max(0.03, w * ((hi - lo) / 100.0) * prog.get_value()),
                height=0.26, fill_color=GREEN, fill_opacity=0.88, stroke_width=0
            ).move_to([x0 + w * (lo / 100.0) + max(0.03, w * ((hi - lo) / 100.0) * prog.get_value()) / 2, y, 0]))
            return VGroup(track, t0, t100, lbl, band), prog

        mg_bar, mg_p = make_range_bar("magnesium: 60–70%", 60, 70, -5.60, -1.40, -3.02)
        ca_bar, ca_p = make_range_bar("calcium: 20–25%", 20, 25, -0.30, 3.90, -3.02)
        est_tag = T("textbook estimates", size=24, color=TEXT).move_to([-0.85, -2.14, 0])

        # "about 60 to 70"
        self.at("about 60 to 70")
        self.play(FadeIn(mg_bar), FadeIn(est_tag), run_time=0.45)
        self.play(mg_p.animate.set_value(1.0), run_time=0.9, rate_func=smooth)

        # "about 20 to 25"
        self.at("about 20 to 25")
        self.play(FadeIn(ca_bar), run_time=0.45)
        self.play(ca_p.animate.set_value(1.0), run_time=0.9, rate_func=smooth)
        self.finish()


class S12Idea(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=-0.65, show_romk=True, show_cl=True, blocked=False,
                                 plus_count=5, minus_count=4, junction_glow=True)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=1.3)
        nk_run = {"on": True}
        cw["nkcc2"][1].add_updater(lambda m, dt: m.rotate((PI / 2) * dt, about_point=cw["nkcc2"][0].get_center()) if nk_run["on"] else None)

        v_track = ValueTracker(7.0)
        gauge = VoltageGauge(v_track, show_number=False)
        v_num = M("+7 mV", size=24, color=GOLD).move_to([5.55, -1.71, 0])
        tag = scope_tag("schematic")

        loop_pts = [
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], 0.22, 0],
            [C["romk_x"], 0.22, 0],
            [C["romk_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
        ]
        cl_pts = [[C["nkcc_x"], 0.10, 0], [C["cl_x"], 0.10, 0], [C["cl_x"], C["y_base"] - 0.70, 0]]
        loop_line = VMobject(stroke_color=MAGENTA, stroke_width=6, stroke_opacity=0.85).set_points_as_corners(loop_pts)
        cl_line = VMobject(stroke_color=CYAN, stroke_width=6, stroke_opacity=0.85).set_points_as_corners(cl_pts)
        k_loop = make_ion_stream(["K"] * 5, loop_pts, speed=1.8, seed=81)
        cl_exit = make_ion_stream(["Cl"] * 4, cl_pts, speed=1.3, seed=83)

        gx = C["gap_cx"]
        ca_gap = make_ion_stream(["Ca"] * 3, [[gx, 1.62, 0], [gx, -2.05, 0]], speed=1.6, seed=85)
        pass_lbl = T("passengers", size=26, color=GREEN, weight=BOLD).move_to([C["rx0"] + 1.25, -0.40, 0])
        pass_arr = Arrow([C["rx0"] + 0.40, -0.15, 0], [C["rx0"] - 0.05, -0.15, 0],
                         color=GREEN, stroke_width=3.5, buff=0.02, tip_length=0.16)

        self.add(cw["world"], gauge, v_num, loop_line, cl_line, k_loop, cl_exit, ca_gap, pass_lbl, pass_arr, tag)

        # "a door can move"
        self.at("a door can move")
        self.play(
            loop_line.animate.set_stroke(color=GOLD, width=8),
            cl_line.animate.set_stroke(color=GOLD, width=8),
            run_time=0.6,
        )

        # "block that door" -> ca_trickle starts at y=1.05 so it never overlaps lumen ca_divert at y=1.62
        self.at("block that door")
        nk_run["on"] = False
        padlock = make_padlock([C["nkcc_x"], C["y_apical"] + 0.02, 0], scale=1.05)
        furo_lbl = T("furosemide", size=28, color=RED, weight=BOLD).move_to([C["nkcc_x"], C["y_apical"] - 0.55, 0])
        schem_drop = T("voltage drops", size=22, color=TEXT).move_to([5.55, -1.71, 0])

        ca_gap.clear_updaters()
        ca_divert = make_ion_stream(["Ca"] * 3, [[C["mx0"] + 0.2, 1.58, 0], [C["rx1"] - 0.1, 1.58, 0]], speed=1.45, seed=87)
        ca_trickle = make_ion_stream(["Ca"] * 1, [[gx, 1.05, 0], [gx, -2.05, 0]], speed=0.45, seed=89)

        self.play(
            FadeIn(padlock, shift=DOWN * 0.2),
            FadeIn(furo_lbl),
            FadeOut(loop_line), FadeOut(cl_line), FadeOut(k_loop), FadeOut(cl_exit),
            FadeOut(cw["plus"][1:-1]),
            FadeOut(ca_gap),
            swap(v_num, schem_drop, run_time=0.5),
            v_track.animate.set_value(1.2),
            FadeIn(ca_divert),
            FadeIn(ca_trickle),
            run_time=1.0,
        )
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        cup_lv = ValueTracker(0.10)
        macro, doors, pumps, padlock, cup, prox_left = build_macro_world(blocked=True, proximal_glow=False, cup_green_level=0.0)
        for p in pumps:
            add_pump_spin(p, speed=1.3)
        cx0, cx1, cy0, cy1 = cup
        cup_green = always_redraw(lambda: Rectangle(
            width=cx1 - cx0 - 0.08, height=max(0.02, 0.72 * cup_lv.get_value()),
            fill_color=GREEN, fill_opacity=0.72, stroke_width=0
        ).move_to([(cx0 + cx1) / 2, cy0 + 0.46 + max(0.02, 0.72 * cup_lv.get_value()) / 2, 0]).set_z_index(-4))
        tag = scope_tag("schematic")
        self.add(macro, cup_green, tag)

        # "furosemide" -> GREEN 2+ ions sail cleanly over cup rim (y=0.72) into cup center
        self.at("furosemide")
        ca_urine = make_ion_stream(
            ["Ca"] * 5,
            [[-4.0, 0.96, 0], [-2.3, 0.96, 0], [1.5, 0.96, 0], [5.35, 0.96, 0], [5.35, -0.55, 0]],
            speed=1.65, seed=91,
        )
        self.play(FadeIn(ca_urine), cup_lv.animate.set_value(0.95), run_time=2.5, rate_func=linear)

        # "proximal tubule"
        self.at("proximal tubule")
        prox_gap_x = -5.02
        prox_ca = make_ion_stream(
            ["Ca"] * 3,
            [[prox_gap_x, 1.15, 0], [prox_gap_x, -1.35, 0]],
            speed=1.35, seed=93,
        )
        self.play(FadeIn(prox_ca), prox_left.animate.set_stroke(color=TEAL, width=6), run_time=0.6)

        # "this rule leaves"
        self.at("this rule leaves")
        not_rule = T("not in this rule", size=26, color=GOLD, weight=BOLD).move_to([-5.02, -2.35, 0])
        self.play(FadeIn(not_rule), run_time=0.5)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        cw = build_closeup_world(shift_x=-0.65, show_romk=True, show_cl=True, blocked=True,
                                 plus_positions=[-4.6], minus_count=1, junction_glow=False)
        C = cw["coords"]
        add_pump_spin(cw["pump"], speed=0.8)
        nk_run = {"on": False}
        cw["nkcc2"][1].add_updater(lambda m, dt: m.rotate((PI / 2) * dt, about_point=cw["nkcc2"][0].get_center()) if nk_run["on"] else None)

        v_track = ValueTracker(1.2)
        gauge = VoltageGauge(v_track, show_number=False)
        v_num14 = M("+7 mV", size=24, color=GOLD).move_to([5.55, -1.71, 0])
        tag = scope_tag("schematic")
        self.add(cw["world"], gauge, tag)

        # "look past"
        self.at("look past")
        self.play(cw["padlock"].animate.shift(UP * 0.45).set_opacity(0), run_time=0.65)

        self.at("a door carries")
        self.play(Indicate(cw["nkcc2"], color=ORANGE, scale_factor=1.15), run_time=0.9)
        self.at("voltage its")
        self.play(Indicate(gauge.track, color=GOLD, scale_factor=1.12), run_time=0.8)

        # "what voltage"
        self.at("what voltage")
        nk_run["on"] = True
        loop_pts = [
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], 0.22, 0],
            [C["romk_x"], 0.22, 0],
            [C["romk_x"], C["y_apical"] + 0.50, 0],
            [C["nkcc_x"], C["y_apical"] + 0.50, 0],
        ]
        cl_pts = [[C["nkcc_x"], 0.10, 0], [C["cl_x"], 0.10, 0], [C["cl_x"], C["y_base"] - 0.70, 0]]
        k_loop = make_ion_stream(["K"] * 5, loop_pts, speed=1.9, seed=101)
        cl_exit = make_ion_stream(["Cl"] * 4, cl_pts, speed=1.35, seed=103)
        extra_plus = VGroup(*[
            T("+", size=30, color=TEXT, weight=BOLD).move_to([px, C["y_lumen_top"] - 0.34, 0])
            for px in [-3.3, -2.0, -0.7, 0.5]
        ])
        self.play(
            FadeIn(k_loop), FadeIn(cl_exit), FadeIn(extra_plus),
            v_track.animate.set_value(7.0),
            run_time=1.1,
        )
        self.play(FadeIn(v_num14), run_time=0.3)

        # "which ions"
        self.at("which ions")
        gx = C["gap_cx"]
        ca_gap = make_ion_stream(["Ca"] * 3, [[gx, 1.62, 0], [gx, -2.05, 0]], speed=1.65, seed=105)
        self.play(FadeIn(ca_gap), run_time=0.45)
        self.finish()


class S15End(EndCard):
    LINE = "Block a door that builds voltage, and its passenger ions move less."
