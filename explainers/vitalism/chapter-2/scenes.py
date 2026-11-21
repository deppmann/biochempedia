"""
Vitalism Chapter 2: "What Did the Work?"

COLOUR MAP (one colour per concept for the whole film):
- TEAL   (#3FB8C0): ordinary chemistry (platform, SAME RULES band) & dissolved workers (enzymes: rounded TEAL blobs with no internal structure)
- PURPLE (#A78BFA): helper tokens (cofactors / cozymase / NAD — small purple coins)
- GOLD   (#D4A843): vital force (specks, absent / drifting away unused)
- AMBER  (#C99A3B): yeast press juice tint & brass ENZYME plate border / 1907 medal accent
- TEXT   (#E8EAF0): substrates & products as blocks (SUGAR, GLYCEROL, FATTY ACID, FAT, ETHANOL, UREA), CO2 bubbles, primary labels
- BLUE   (#58C4DD): water drops (H2O) in Berthelot's fat equilibrium
- GREEN  (#83C167): synthetic fatty acid strip in Berthelot's NEW FAT
- GREY   (#8B93A1): bench glass outlines, rock/salt jar, dimmed cell/organ silhouettes, SCHEMATIC tag

THE ONE WORLD (carried from scene to scene):
The laboratory bench platform labelled ORDINARY CHEMISTRY holding Buchner's bubbling flask of clear gold yeast juice,
with the camera pushing into the juice to inspect the dissolved workers and pulling back to the bench to compare
them with dishes, organs, Berthelot's fat reaction, and the rock and salt jar.

WHAT CHANGES (computed / simulated per spoken scene):
- s00_link_and_question: Filter mesh & chloroform drop flash at the flask neck, then camera pushes into the juice where a dashed outline sheds computed rising CO2 bubbles as sugar drifts in.
- s01_title: (silent 2.0 s) Top question morphs into "What Did the Work?" while the dashed outline keeps shedding bubbles.
- s02_zymase: Dashed outline fills into a slowly rotating TEAL ZYMASE blob that consumes drifting SUGAR blocks and emits computed CO2 bubbles; 1907 medal settles on flask label.
- s03_kuhne_name: Pulls back to bench; PEPSIN and INVERTASE dishes slide in and chip white substrate blocks while the brass ENZYME ("IN LEAVEN") plate joins all three.
- s04_kuhne_belief: TEAL blobs glow inside STOMACH and EYE outlines, lift out along arrows into small dishes, then cell/organ outlines dim while all enzyme blobs brighten.
- s05_berthelot: GLYCEROL block and three FATTY ACID strips click together, shedding 3 falling BLUE water drops to form FAT, then water rises and splits them in a continuous computed cycle.
- s06_equilibrium: Matching pulsing EQUILIBRIUM two-way arrows appear under the cycling fat and above the ROCK & SALT jar; a GOLD speck fails to settle; one strip swaps to GREEN to form NEW FAT.
- s07_idea: Full platform unites enzymes under ENZYME plate and cycling FAT equilibrium; TEAL blob lifts out of ghost YEAST CELL into flask; TEAL SAME RULES band illuminates the bench.
- s08_predict: Pushes into juice around the large rotating ZYMASE blob consuming SUGAR and shedding CO2 bubbles; ONE OR SEVERAL? question card appears without splitting the blob.
- s09_predict_hold: (silent 4.5 s) PredictPause countdown ring ticks down while ZYMASE keeps rotating, taking sugar, and shedding bubbles.
- s10_team: ZYMASE splits into a 5-blob SCHEMATIC enzyme chain with hopping PURPLE cofactors (COZYMASE -> NAD), passing SUGAR through GLYCOLYSIS + 2 STEPS to ETHANOL + bubbles, then spotlights one blob.
- s11_proteins_urea: TEAL blobs get PROTEIN tags (coins stay untagged); chain shrinks into flask beside Wöhler's UREA flask; liver silhouette opens on right with 5 TEAL enzymes cycling blocks in the UREA CYCLE to drop UREA.
- s12_close: Full bench returns; last GOLD specks drift up and vanish; one TEAL enzyme lifts from the urea loop into a dish and keeps working; SAME RULES band glows beneath all objects.
- s13_end: (silent 3.5 s) Standard EndCard with Hex waving over the take-home line.
"""

from bp_parts import *

PURPLE = "#A78BFA"
AMBER = "#C99A3B"
BRASS_DARK = "#2B2210"
SLATE_FILL = "#CBD5E1"


# ---------------------------------------------------------------------------
# Computed Geometry & World Builders
# ---------------------------------------------------------------------------

def blob_points(radius=0.65, lobes=5, n=48, seed=0):
    """Deterministic rounded organic contour with no internal structure."""
    rng = np.random.default_rng(seed)
    p1 = rng.uniform(0, TAU)
    p2 = rng.uniform(0, TAU)
    pts = []
    for k in range(n):
        th = TAU * k / n
        r = radius * (1.0 + 0.08 * np.cos(lobes * th + p1) + 0.04 * np.sin((lobes - 2) * th + p2))
        pts.append([r * np.cos(th), r * np.sin(th), 0.0])
    return pts


def make_enzyme(label_text=None, radius=0.65, lobes=5, color=TEAL, label_size=26, seed=0, fill_opacity=0.52):
    """Rounded TEAL enzyme blob with optional upright centered label and rotating contour."""
    pts = blob_points(radius=radius, lobes=lobes, seed=seed)
    body = VMobject(stroke_color=color, stroke_width=3.6, fill_color=color, fill_opacity=fill_opacity)
    body.set_points_smoothly(pts + [pts[0]])
    g = VGroup(body)
    g.body = body
    g.label = None
    if label_text:
        lab = T(label_text, size=label_size, color=TEXT, weight=BOLD)
        lab.move_to(body.get_center())
        g.add(lab)
        g.label = lab
    return g


def attach_turn(blob_mob, speed=0.45):
    """Slowly rotate the enzyme's outer contour while keeping its label upright."""
    body = blob_mob.body if hasattr(blob_mob, "body") else blob_mob

    def _u(m, dt):
        m.rotate(speed * dt)
    body.add_updater(_u)
    return blob_mob


def make_block(text, color=TEXT, text_color=BG, size=24, min_w=1.30, h=0.48, pad_x=0.24):
    """Crisp solid substrate/product block with generous padding around letters."""
    lab = T(text, size=size, color=text_color, weight=BOLD)
    w = max(min_w, lab.width + 2 * pad_x)
    h_use = max(h, lab.height + 0.22)
    rect = RoundedRectangle(corner_radius=0.08, width=w, height=h_use,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.94)
    lab.move_to(rect)
    g = VGroup(rect, lab)
    g.box = rect
    g.label = lab
    return g


def make_cofactor(radius=0.22):
    """Solid PURPLE helper coin (cofactor) with pure purple fill and crisp white inner rim."""
    outer = Circle(radius=radius, stroke_color=PURPLE, stroke_width=3.2,
                   fill_color=PURPLE, fill_opacity=0.92)
    inner = Circle(radius=radius * 0.56, stroke_color=TEXT, stroke_width=1.8,
                   fill_color=PURPLE, fill_opacity=0.0).set_stroke(opacity=0.80)
    return VGroup(outer, inner)


def make_water_drop(radius=0.14):
    """Simple geometric BLUE water drop (no atoms or bonds)."""
    pts = [
        [0.0, radius * 1.45, 0.0],
        [radius * 0.95, 0.1 * radius, 0.0],
        [radius * 0.85, -radius * 0.9, 0.0],
        [0.0, -radius * 1.15, 0.0],
        [-radius * 0.85, -radius * 0.9, 0.0],
        [-radius * 0.95, 0.1 * radius, 0.0],
    ]
    drop = VMobject(stroke_color=BLUE, stroke_width=2.2, fill_color=BLUE, fill_opacity=0.88)
    drop.set_points_smoothly(pts + [pts[0]])
    return drop


def make_bench(with_same_rules=False, highlight_same_rules=False):
    """Bench platform at bottom of frame: ORDINARY CHEMISTRY (+ optional SAME RULES band)."""
    plat = RoundedRectangle(corner_radius=0.10, width=12.4, height=0.46,
                            stroke_color=TEAL, stroke_width=2.8,
                            fill_color=TEAL, fill_opacity=0.24).move_to([0.0, -3.14, 0.0])
    plat_lbl = T("ORDINARY CHEMISTRY", size=24, color=TEXT, weight=BOLD).move_to(plat)
    g = VGroup(plat, plat_lbl)
    g.plat = plat
    g.plat_lbl = plat_lbl
    g.top_y = plat.get_top()[1]
    if with_same_rules:
        fill_op = 0.45 if highlight_same_rules else 0.08
        stroke_op = 1.0 if highlight_same_rules else 0.45
        lbl_op = 1.0 if highlight_same_rules else 0.40
        band = RoundedRectangle(corner_radius=0.08, width=12.4, height=0.38,
                                stroke_color=TEAL, stroke_width=3.2,
                                fill_color=TEAL, fill_opacity=fill_op).move_to([0.0, -2.64, 0.0])
        band.set_stroke(opacity=stroke_op)
        band_lbl = T("SAME RULES", size=24, color=TEXT, weight=BOLD).move_to(band).set_opacity(lbl_op)
        g.add(band, band_lbl)
        g.band = band
        g.band_lbl = band_lbl
        g.top_y = band.get_top()[1]
    return g


def make_flask(bottom_center, height=4.2, show_zyme=False, zymase_label=True, seed=7, n_bubbles=12):
    """Buchner's Erlenmeyer flask with amber yeast juice, clean ZYMASE chip above rim, and safe bubble lanes."""
    s = height / 4.2
    outline_pts = [
        [-0.44 * s, 4.15 * s, 0],
        [-0.36 * s, 3.85 * s, 0],
        [-0.36 * s, 2.95 * s, 0],
        [-1.52 * s, 0.72 * s, 0],
        [-1.56 * s, 0.22 * s, 0],
        [-1.28 * s, 0.0, 0],
        [1.28 * s, 0.0, 0],
        [1.56 * s, 0.22 * s, 0],
        [1.52 * s, 0.72 * s, 0],
        [0.36 * s, 2.95 * s, 0],
        [0.36 * s, 3.85 * s, 0],
        [0.44 * s, 4.15 * s, 0],
    ]
    glass = VMobject(stroke_color=TEXT, stroke_width=3.2, fill_color=BG, fill_opacity=0.0)
    glass.set_points_as_corners(outline_pts)
    rim = Line([-0.46 * s, 4.15 * s, 0], [0.46 * s, 4.15 * s, 0], color=TEXT, stroke_width=3.5)

    liq_pts = [
        [-0.84 * s, 2.10 * s, 0],
        [-1.50 * s, 0.72 * s, 0],
        [-1.54 * s, 0.22 * s, 0],
        [-1.26 * s, 0.02 * s, 0],
        [1.26 * s, 0.02 * s, 0],
        [1.54 * s, 0.22 * s, 0],
        [1.50 * s, 0.72 * s, 0],
        [0.84 * s, 2.10 * s, 0],
    ]
    liquid = Polygon(*[p[:3] for p in liq_pts],
                     stroke_color=AMBER, stroke_width=2.0,
                     fill_color=AMBER, fill_opacity=0.24)
    meniscus = Line([-0.84 * s, 2.10 * s, 0], [0.84 * s, 2.10 * s, 0],
                    color=AMBER, stroke_width=2.6)

    bc = np.array(bottom_center, dtype=float)
    g = VGroup(liquid, meniscus, glass, rim)
    g.shift(bc)
    glass._ref0 = glass.get_center().copy()

    g.zymase = None
    g.zymase_badge = None
    if show_zyme:
        zb = make_enzyme(None, radius=0.48 * s, lobes=5, color=TEAL, seed=seed + 3, fill_opacity=0.58)
        zb.move_to(bc + UP * (0.88 * s))
        attach_turn(zb, speed=0.4)
        g.add(zb)
        g.zymase = zb
        if zymase_label:
            badge = boxed_label("ZYMASE", color=TEAL, size=24, pad=0.14, stroke=2.4, fill_opacity=0.20)
            badge.next_to(rim, UP, buff=0.14)
            g.add(badge)
            g.zymase_badge = badge

    rng = np.random.default_rng(seed)
    bubbles = VGroup()
    y_lo = bc[1] + 1.44 * s
    y_hi = bc[1] + 1.98 * s
    for k in range(n_bubbles):
        r = rng.uniform(0.035, 0.068) * max(s, 0.78)
        b = Circle(radius=r, stroke_color=TEXT, stroke_width=1.8,
                   fill_color=TEXT, fill_opacity=0.42)
        if show_zyme and k % 2 == 0:
            side = -1.0 if (k // 2) % 2 == 0 else 1.0
            x_off = side * rng.uniform(0.76 * s, 1.04 * s)
            b_ylo, b_yhi = bc[1] + 0.30 * s, bc[1] + 1.45 * s
        else:
            x_off = rng.uniform(-0.68 * s, 0.68 * s)
            b_ylo, b_yhi = y_lo, y_hi
        y0 = rng.uniform(b_ylo, b_yhi)
        b.move_to([bc[0] + x_off, y0, 0.0])
        b._bx = bc[0] + x_off
        b._vy = rng.uniform(0.35, 0.72) * s
        b._ph = rng.uniform(0, TAU)
        b._ylo, b._yhi = b_ylo, b_yhi
        b._t = 0.0
        b._amp = 0.04 * s

        def _bu(m, dt, ref=glass):
            m._t += dt
            d = ref.get_center() - ref._ref0
            ylo = m._ylo + d[1]
            yhi = m._yhi + d[1]
            ny = m.get_center()[1] + m._vy * dt
            if ny > yhi or ny < ylo:
                ny = ylo + (ny - ylo) % max(yhi - ylo, 1e-4)
            nx = m._bx + d[0] + m._amp * np.sin(3.0 * m._t + m._ph)
            m.move_to([nx, ny, 0.0])
            frac = (ny - ylo) / max(yhi - ylo, 1e-4)
            op = np.sin(np.pi * np.clip(frac, 0.05, 0.95))
            m.set_fill(opacity=0.45 * op).set_stroke(opacity=0.90 * op)

        b.add_updater(_bu)
        bubbles.add(b)
    g.add(bubbles)
    g.bubbles = bubbles
    g.liquid = liquid
    g.meniscus = meniscus
    g.glass = glass
    g.rim = rim
    g.s = s
    return g


def make_juice_chamber(seed=7, n_bubbles=18, bubble_mode="center"):
    """Zoomed-in view inside Buchner's flask; wide walls clear of SCHEMATIC and SUGAR."""
    meniscus_y = 2.62 if bubble_mode == "chain" else 2.38
    left_wall = ArcBetweenPoints([-6.30, meniscus_y, 0], [-6.55, -3.45, 0], angle=0.08,
                                 color=TEXT, stroke_width=3.0).set_stroke(opacity=0.48)
    right_wall = ArcBetweenPoints([6.30, meniscus_y, 0], [6.55, -3.45, 0], angle=-0.08,
                                  color=TEXT, stroke_width=3.0).set_stroke(opacity=0.48)
    meniscus = Line([-6.30, meniscus_y, 0], [6.30, meniscus_y, 0], color=AMBER, stroke_width=2.8).set_opacity(0.80)
    juice = Rectangle(width=12.8, height=meniscus_y + 3.45, stroke_width=0,
                      fill_color=AMBER, fill_opacity=0.18).move_to([0.0, (meniscus_y - 3.45) / 2, 0.0])

    rng = np.random.default_rng(seed)
    bubbles = VGroup()
    for k in range(n_bubbles):
        r = rng.uniform(0.05, 0.105)
        b = Circle(radius=r, stroke_color=TEXT, stroke_width=2.0,
                   fill_color=TEXT, fill_opacity=0.45)
        if bubble_mode == "chain":
            bx = rng.uniform(4.75, 5.75)
            y_lo, y_hi = -0.20, 1.45
        else:
            lane = k % 3
            if lane == 0:
                bx = rng.uniform(-0.85, 1.45)
                y_lo, y_hi = 1.48, 2.24
            elif lane == 1:
                bx = rng.uniform(2.35, 4.75)
                y_lo, y_hi = -1.25, 2.24
            else:
                bx = rng.uniform(-4.75, -2.05)
                y_lo, y_hi = 0.65, 2.24
        by = rng.uniform(y_lo, y_hi)
        b.move_to([bx, by, 0.0])
        b._bx = bx
        b._vy = rng.uniform(0.42, 0.88)
        b._ph = rng.uniform(0, TAU)
        b._ylo, b._yhi = y_lo, y_hi
        b._t = 0.0

        def _bu(m, dt):
            m._t += dt
            ny = m.get_center()[1] + m._vy * dt
            if ny > m._yhi:
                ny = m._ylo
            nx = m._bx + 0.08 * np.sin(2.5 * m._t + m._ph)
            m.move_to([nx, ny, 0.0])
            frac = (ny - m._ylo) / max(m._yhi - m._ylo, 1e-4)
            op = np.sin(np.pi * np.clip(frac, 0.04, 0.96))
            m.set_fill(opacity=0.45 * op).set_stroke(opacity=0.92 * op)

        b.add_updater(_bu)
        bubbles.add(b)

    g = VGroup(juice, left_wall, right_wall, meniscus, bubbles)
    g.bubbles = bubbles
    g.juice = juice
    return g


def make_sugar_stream(target_x=0.55, target_y=-0.15, start_x=-4.65, stop_gap=1.95):
    """Continuously drifting SUGAR block that approaches the enzyme/outline without intersecting it."""
    block = make_block("SUGAR", color=TEXT, text_color=BG, size=24, min_w=1.35, h=0.48)
    block.move_to([start_x, target_y, 0.0])
    block._t = 0.0
    block._x0 = start_x
    block._x1 = target_x - stop_gap
    block._y = target_y

    def _su(m, dt):
        m._t = (m._t + dt * 0.28) % 1.0
        x = m._x0 + m._t * (m._x1 - m._x0)
        y = m._y + 0.06 * np.sin(TAU * m._t)
        m.move_to([x, y, 0.0])
        op = 1.0 if m._t < 0.82 else max(0.05, (1.0 - m._t) / 0.18)
        for sub in m.family_members_with_points():
            try:
                sub.set_opacity(op)
            except Exception:
                pass

    block.add_updater(_su)
    return block


def make_rock_and_salt(bottom_center, scale=1.0, show_labels=True):
    """Mineral world icons: faceted ROCK and crystalline SALT jar."""
    s = scale
    bc = np.array(bottom_center, dtype=float)
    rock_pts = [
        [-0.75 * s, 0.0, 0],
        [-0.85 * s, 0.45 * s, 0],
        [-0.35 * s, 0.88 * s, 0],
        [0.25 * s, 0.82 * s, 0],
        [0.70 * s, 0.40 * s, 0],
        [0.62 * s, 0.0, 0],
    ]
    rock_body = Polygon(*rock_pts, stroke_color=GREY, stroke_width=2.8,
                        fill_color=GREY, fill_opacity=0.42)
    rock_facet = Line([-0.35 * s, 0.88 * s, 0], [-0.1 * s, 0.35 * s, 0],
                      color=GREY, stroke_width=2.0)
    rock_g = VGroup(rock_body, rock_facet).shift(bc + LEFT * (0.95 * s))

    jar_box = RoundedRectangle(corner_radius=0.10, width=1.05 * s, height=1.22 * s,
                               stroke_color=TEXT, stroke_width=2.6,
                               fill_color=BG, fill_opacity=0.0)
    jar_lid = RoundedRectangle(corner_radius=0.05, width=0.86 * s, height=0.22 * s,
                               stroke_color=GREY, stroke_width=2.4,
                               fill_color=GREY, fill_opacity=0.50).next_to(jar_box, UP, buff=0.02)
    salt_fill = Rectangle(width=0.92 * s, height=0.58 * s, stroke_width=0,
                          fill_color=TEXT, fill_opacity=0.72).align_to(jar_box, DOWN).shift(UP * (0.06 * s))
    jar_g = VGroup(salt_fill, jar_box, jar_lid)
    jar_g.shift(bc + RIGHT * (0.85 * s) - jar_box.get_bottom())

    g = VGroup(rock_g, jar_g)
    if show_labels:
        r_lbl = T("ROCK", size=24, color=TEXT, weight=BOLD).next_to(rock_g, UP, buff=0.18)
        s_lbl = T("SALT", size=24, color=TEXT, weight=BOLD).next_to(jar_g, UP, buff=0.18)
        g.add(r_lbl, s_lbl)
    return g


def make_yeast_cell(center, height=2.1, opacity=0.85, label_dir=DOWN):
    """Large pale budding yeast cell silhouette (no molecular detail)."""
    s = height / 2.2
    main_cell = Ellipse(width=1.45 * s, height=2.05 * s,
                        stroke_color=TEXT, stroke_width=2.8,
                        fill_color=TEXT, fill_opacity=0.10 * opacity)
    bud = Circle(radius=0.38 * s, stroke_color=TEXT, stroke_width=2.5,
                 fill_color=TEXT, fill_opacity=0.10 * opacity).move_to([0.45 * s, 0.92 * s, 0.0])
    body = VGroup(main_cell, bud)
    lbl = T("YEAST CELL", size=24, color=TEXT).next_to(main_cell, label_dir, buff=0.22)
    g = VGroup(body, lbl).move_to(center)
    g.body = body
    g.lbl = lbl
    return g


def make_dish(bottom_center, label_text=None, width=1.95, seed=1):
    """Shallow open glass dish with an active TEAL enzyme chipping at a white block."""
    bc = np.array(bottom_center, dtype=float)
    w, h = width, 0.44
    pts = [
        [-w / 2, h, 0],
        [-w * 0.40, 0.0, 0],
        [w * 0.40, 0.0, 0],
        [w / 2, h, 0],
    ]
    rim = VMobject(stroke_color=TEXT, stroke_width=2.8, fill_color=TEAL, fill_opacity=0.12)
    rim.set_points_as_corners(pts)
    rim.shift(bc)
    rim._ref0 = rim.get_center().copy()

    enz = make_enzyme(None, radius=0.32, lobes=5, color=TEAL, seed=seed, fill_opacity=0.58)
    enz.move_to(bc + [-0.34, 0.42, 0])
    blk = RoundedRectangle(corner_radius=0.05, width=0.50, height=0.28,
                           stroke_color=TEXT, stroke_width=2.0,
                           fill_color=TEXT, fill_opacity=0.90).move_to(bc + [0.32, 0.28, 0])
    chip1 = Square(side_length=0.10, stroke_width=0, fill_color=TEXT, fill_opacity=0.85).move_to(bc + [0.22, 0.56, 0])
    chip1._base = chip1.get_center().copy()
    chip1._t = seed * 0.6

    def _cu(m, dt, ref=rim):
        m._t += dt
        cyc = (m._t * 0.9) % 1.0
        d = ref.get_center() - ref._ref0
        m.move_to(m._base + d + UP * (0.34 * cyc) + RIGHT * (0.16 * cyc))
        m.set_fill(opacity=0.88 * (1.0 - cyc))

    chip1.add_updater(_cu)

    enz._t = seed * 0.4
    enz._base = enz.get_center().copy()

    def _eu(m, dt, ref=rim):
        m._t += dt
        d = ref.get_center() - ref._ref0
        m.move_to(m._base + d + RIGHT * (0.06 * np.sin(3.5 * m._t)))

    enz.add_updater(_eu)

    g = VGroup(rim, blk, enz, chip1)
    g.enz = enz
    g.lbl = None
    if label_text:
        lab = T(label_text, size=24, color=TEAL, weight=BOLD).next_to(rim, UP, buff=0.56)
        g.add(lab)
        g.lbl = lab
    return g


def make_two_way_arrow(center, width=2.2, label="EQUILIBRIUM", color=TEAL):
    """Equilibrium double arrow that pulses smoothly in step with the reversible reaction."""
    c = np.array(center, dtype=float)
    top_arr = Arrow(c + LEFT * (width / 2) + UP * 0.11,
                    c + RIGHT * (width / 2) + UP * 0.11,
                    buff=0, color=color, stroke_width=4.0, max_tip_length_to_length_ratio=0.14)
    bot_arr = Arrow(c + RIGHT * (width / 2) + DOWN * 0.11,
                    c + LEFT * (width / 2) + DOWN * 0.11,
                    buff=0, color=color, stroke_width=4.0, max_tip_length_to_length_ratio=0.14)
    arrows = VGroup(top_arr, bot_arr)
    g = VGroup(arrows)
    if label:
        lbl = T(label, size=24, color=color, weight=BOLD).next_to(arrows, DOWN, buff=0.14)
        g.add(lbl)
        g.lbl = lbl
    g.arrows = arrows
    return g


def attach_pulse_arrow(two_way_mob):
    """Pulse top/bottom equilibrium arrows alternately in step."""
    two_way_mob._pt = 0.0

    def _u(m, dt):
        m._pt += dt
        s = 0.5 + 0.5 * np.sin(2.4 * m._pt)
        m.arrows[0].set_opacity(0.45 + 0.55 * s)
        m.arrows[1].set_opacity(0.45 + 0.55 * (1.0 - s))

    two_way_mob.add_updater(_u)
    return two_way_mob


def make_fat_system(center, scale=1.0, show_fat_label=False, third_green=False, cycling=False, split_dx=0.72):
    """Berthelot's GLYCEROL + 3 FATTY ACID strips <-> FAT + 3 BLUE water drops.
    Water drops fall cleanly under the GLYCEROL block (never crossing FATTY ACID strips).
    """
    s = scale
    c = np.array(center, dtype=float)
    gly_lbl = T("GLYCEROL", size=24, color=BG, weight=BOLD)
    gly_w = max(1.90 * s, gly_lbl.width + 0.62)
    gly_h = max(1.85, 2.05 * s)

    st_sample = T("FATTY ACID", size=24, color=BG, weight=BOLD)
    strip_w = max(2.05 * s, st_sample.width + 0.36)
    strip_h = max(0.46, st_sample.height + 0.18)

    gly_box = RoundedRectangle(corner_radius=0.08, width=gly_w, height=gly_h,
                               stroke_color=TEXT, stroke_width=2.5,
                               fill_color=TEXT, fill_opacity=0.94)
    gly_box.move_to(c + LEFT * (strip_w * 0.48))
    gly_lbl.move_to(gly_box.get_center() + LEFT * 0.15)

    dy_step = min(0.64, (gly_h - 0.55) / 2.0)
    ys = [dy_step, 0.0, -dy_step]
    sockets = VGroup(*[
        Circle(radius=0.11, stroke_color=BG, stroke_width=1.8,
               fill_color=BG, fill_opacity=0.88).move_to([gly_box.get_right()[0] - 0.12, c[1] + dy, 0])
        for dy in ys
    ])
    gly_g = VGroup(gly_box, sockets, gly_lbl)

    strips = VGroup()
    drops = VGroup()
    joined_x = gly_box.get_right()[0] + strip_w / 2 + 0.12
    split_x = joined_x + split_dx * max(s, 0.72)

    for idx, dy in enumerate(ys):
        col = GREEN if (third_green and idx == 2) else SLATE_FILL
        st = RoundedRectangle(corner_radius=0.07, width=strip_w, height=strip_h,
                              stroke_color=col, stroke_width=2.4,
                              fill_color=col, fill_opacity=0.94)
        st_lbl = T("FATTY ACID", size=24, color=BG, weight=BOLD).move_to(st)
        sg = VGroup(st, st_lbl)
        sg._joined_x = joined_x
        sg._split_x = split_x
        sg._y = c[1] + dy
        sg.move_to([sg._split_x, sg._y, 0.0])
        strips.add(sg)

        dr = make_water_drop(radius=0.12)
        # Drops emerge from the seam and pool cleanly under GLYCEROL (well clear of FATTY ACID strips)
        dr._seam_x = gly_box.get_right()[0] + 0.04
        dr._seam_y = gly_box.get_bottom()[1] - 0.14
        dr._pool_x = gly_box.get_right()[0] - 0.88 + idx * 0.36
        dr._pool_y = gly_box.get_bottom()[1] - 0.44
        dr.move_to([dr._seam_x, dr._seam_y, 0.0]).set_opacity(0.0)
        drops.add(dr)

    fat_txt = "NEW FAT" if third_green else "FAT"
    fat_col = GREEN if third_green else TEXT
    fat_badge = T(fat_txt, size=28, color=fat_col, weight=BOLD)
    fat_badge.move_to([gly_box.get_right()[0] + 0.35, gly_box.get_top()[1] + 0.34, 0.0])
    if not show_fat_label:
        fat_badge.set_opacity(0.0)

    root = VGroup(gly_g, strips, drops, fat_badge)
    root.gly_g = gly_g
    root.strips = strips
    root.drops = drops
    root.fat_badge = fat_badge
    root.c = c
    root.s = s

    if cycling:
        root._t = 0.0

        def _cycle(m, dt):
            m._t += dt
            u = 0.5 - 0.5 * np.cos(TAU * m._t / 4.4)
            for sg, dr in zip(m.strips, m.drops):
                sg.move_to([sg._split_x + u * (sg._joined_x - sg._split_x), sg._y, 0.0])
                dr.move_to([dr._seam_x + u * (dr._pool_x - dr._seam_x),
                            dr._seam_y + u * (dr._pool_y - dr._seam_y), 0.0])
                dr.set_opacity(np.clip((u - 0.25) / 0.35, 0.0, 1.0))
            if not getattr(m, "_pause_badge", False):
                m.fat_badge.set_opacity(1.0 if u > 0.72 else 0.0)

        root.add_updater(_cycle)

    return root


def make_liver_cycle(center, radius=1.50, scale=1.0):
    """Simple rounded two-lobed liver silhouette enclosing 5 TEAL enzymes on a circular UREA CYCLE track."""
    s = scale
    c = np.array(center, dtype=float)
    liver_pts = [
        [-2.85 * s, -0.55 * s, 0],
        [-2.75 * s, 1.08 * s, 0],
        [-1.12 * s, 2.08 * s, 0],
        [1.08 * s, 2.04 * s, 0],
        [2.78 * s, 1.42 * s, 0],
        [3.02 * s, 0.25 * s, 0],
        [2.15 * s, -0.95 * s, 0],
        [0.30 * s, -1.78 * s, 0],
        [-1.48 * s, -1.82 * s, 0],
    ]
    liver = VMobject(stroke_color=GREY, stroke_width=3.2, fill_color=GREY, fill_opacity=0.20)
    liver.set_points_smoothly(liver_pts + [liver_pts[0]])
    liver.shift(c)

    r_track = radius * s
    track = Circle(radius=r_track, stroke_color=TEAL, stroke_width=2.6, fill_opacity=0.0).move_to(c)
    blobs = VGroup()
    angles = [PI / 2 + k * TAU / 5 for k in range(5)]
    for k, ang in enumerate(angles):
        pos = c + np.array([r_track * np.cos(ang), r_track * np.sin(ang), 0.0])
        b = make_enzyme(None, radius=0.29 * s, lobes=5, color=TEAL, seed=20 + k, fill_opacity=0.60).move_to(pos)
        attach_turn(b, speed=0.55)
        blobs.add(b)

    cyc_lbl = T("UREA\nCYCLE", size=24, color=TEXT, weight=BOLD, line_spacing=0.85).move_to(c)

    carrier = RoundedRectangle(corner_radius=0.06, width=0.28 * s, height=0.18 * s,
                               stroke_color=TEXT, stroke_width=1.8,
                               fill_color=TEXT, fill_opacity=0.92)
    carrier._ang = PI / 2
    carrier._c = c
    carrier._r = r_track

    def _loop_u(m, dt):
        m._ang -= 1.25 * dt
        m.move_to(m._c + np.array([m._r * np.cos(m._ang), m._r * np.sin(m._ang), 0.0]))

    carrier.add_updater(_loop_u)

    urea_drop = make_block("UREA", color=TEXT, text_color=BG, size=24, min_w=1.15, h=0.42)
    liv_bot = liver.get_bottom()[1]
    urea_drop._c = c
    urea_drop._y0 = liv_bot - 0.30
    urea_drop._y1 = liv_bot - 0.78
    urea_drop._t = 0.25
    urea_drop.move_to([c[0], urea_drop._y0, 0.0])

    def _drop_u(m, dt):
        m._t = (m._t + dt * 0.35) % 1.0
        m.move_to([m._c[0], m._y0 + m._t * (m._y1 - m._y0), 0.0])
        op = np.sin(np.pi * np.clip(m._t, 0.08, 0.92))
        for sub in m.family_members_with_points():
            try:
                sub.set_opacity(op)
            except Exception:
                pass

    urea_drop.add_updater(_drop_u)

    g = VGroup(liver, track, blobs, cyc_lbl, carrier, urea_drop)
    g.liver = liver
    g.track = track
    g.blobs = blobs
    g.cyc_lbl = cyc_lbl
    g.carrier = carrier
    g.urea_drop = urea_drop
    return g


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        bench = make_bench()
        top_y = bench.top_y

        rock_salt = make_rock_and_salt([-4.5, top_y + 0.02, 0.0], scale=0.82)
        yeast = make_yeast_cell([-1.6, top_y + 1.48, 0.0], height=1.95)
        flask = make_flask([2.4, top_y + 0.02, 0.0], height=4.5, show_zyme=False, seed=7, n_bubbles=12)
        sugar = make_block("SUGAR", color=TEXT, text_color=BG, size=24, min_w=1.30, h=0.48)
        sugar.move_to([2.4, top_y + 0.72, 0.0])

        self.add(bench, rock_salt, yeast, flask, sugar)
        self.wait(0.3)

        self.at("controls showed no living cell")
        neck = flask.get_top() + DOWN * 0.25
        mesh_ring = Circle(radius=0.52, stroke_color=TEAL, stroke_width=2.8,
                           fill_color=TEAL, fill_opacity=0.0).move_to(neck + UP * 0.65).set_stroke(opacity=0.75)
        mesh_lines = VGroup(*[
            Line(neck + UP * 0.65 + np.array([x, -0.38, 0]),
                 neck + UP * 0.65 + np.array([x, 0.38, 0]),
                 color=TEAL, stroke_width=2.0).set_stroke(opacity=0.75)
            for x in (-0.28, 0.0, 0.28)
        ])
        mesh_h = VGroup(*[
            Line(neck + UP * 0.65 + np.array([-0.38, y, 0]),
                 neck + UP * 0.65 + np.array([0.38, y, 0]),
                 color=TEAL, stroke_width=2.0).set_stroke(opacity=0.75)
            for y in (-0.22, 0.0, 0.22)
        ])
        mesh_g = VGroup(mesh_ring, mesh_lines, mesh_h)
        chloro_drop = make_water_drop(radius=0.14).set_color(TEAL).move_to(neck + RIGHT * 1.1 + UP * 0.75)
        chloro_lbl = T("CHLOROFORM", size=24, color=TEAL, weight=BOLD).next_to(chloro_drop, RIGHT, buff=0.15)
        ctrl_g = VGroup(mesh_g, chloro_drop, chloro_lbl)

        self.play(FadeIn(ctrl_g, run_time=0.45))
        self.play(chloro_drop.animate.move_to(neck + UP * 0.2), run_time=0.65)
        self.play(FadeOut(ctrl_g, run_time=0.55))

        self.at("so if not life")
        chamber = make_juice_chamber(seed=7, n_bubbles=18, bubble_mode="center")
        outline_pts = blob_points(radius=1.42, lobes=5, seed=11)
        solid_outline = VMobject(stroke_color=TEAL, stroke_width=4.0, fill_opacity=0.0)
        solid_outline.set_points_smoothly(outline_pts + [outline_pts[0]])
        dashed_outline = DashedVMobject(solid_outline, num_dashes=32, dashed_ratio=0.55)
        dashed_outline.move_to([0.55, -0.15, 0.0])
        attach_turn(dashed_outline, speed=0.35)
        sugar_stream = make_sugar_stream(target_x=0.55, target_y=-0.15, start_x=-4.65, stop_gap=2.25)

        self.play(FadeOut(bench, rock_salt, yeast, flask, sugar, run_time=0.55))
        self.play(FadeIn(chamber, dashed_outline, sugar_stream, run_time=0.75))

        self.at("that flask was doing the work")
        q_txt = T("WHAT DID THE WORK?", size=40, color=TEXT, weight=BOLD).move_to([0.0, 3.10, 0.0])
        self.play(FadeIn(q_txt, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        chamber = make_juice_chamber(seed=7, n_bubbles=18, bubble_mode="center")
        outline_pts = blob_points(radius=1.42, lobes=5, seed=11)
        solid_outline = VMobject(stroke_color=TEAL, stroke_width=4.0, fill_opacity=0.0)
        solid_outline.set_points_smoothly(outline_pts + [outline_pts[0]])
        dashed_outline = DashedVMobject(solid_outline, num_dashes=32, dashed_ratio=0.55)
        dashed_outline.move_to([0.55, -0.15, 0.0])
        attach_turn(dashed_outline, speed=0.35)
        sugar_stream = make_sugar_stream(target_x=0.55, target_y=-0.15, start_x=-4.65, stop_gap=2.25)
        q_txt = T("WHAT DID THE WORK?", size=40, color=TEXT, weight=BOLD).move_to([0.0, 3.10, 0.0])

        self.add(chamber, dashed_outline, sugar_stream, q_txt)
        title = T("What Did the Work?", size=48, color=TEXT, font=TITLE_FONT).move_to([0.0, 3.18, 0.0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=AMBER, stroke_width=4).next_to(title, DOWN, buff=0.14)
        self.play(swap(q_txt, VGroup(title, rule), run_time=0.85))
        self.finish()


class S02Zymase(SpokenScene):
    def construct(self):
        chamber = make_juice_chamber(seed=7, n_bubbles=18, bubble_mode="center")
        outline_pts = blob_points(radius=1.42, lobes=5, seed=11)
        solid_outline = VMobject(stroke_color=TEAL, stroke_width=4.0, fill_opacity=0.0)
        solid_outline.set_points_smoothly(outline_pts + [outline_pts[0]])
        dashed_outline = DashedVMobject(solid_outline, num_dashes=32, dashed_ratio=0.55)
        dashed_outline.move_to([0.55, -0.15, 0.0])
        attach_turn(dashed_outline, speed=0.35)
        sugar_stream = make_sugar_stream(target_x=0.55, target_y=-0.15, start_x=-4.65, stop_gap=2.25)

        title = T("What Did the Work?", size=48, color=TEXT, font=TITLE_FONT).move_to([0.0, 3.18, 0.0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=AMBER, stroke_width=4).next_to(title, DOWN, buff=0.14)
        title_g = VGroup(title, rule)

        self.add(chamber, dashed_outline, sugar_stream, title_g)
        self.play(FadeOut(title_g, run_time=0.6))

        self.at("dissolved substance")
        zym_blob = make_enzyme(None, radius=1.42, lobes=5, color=TEAL, seed=11, fill_opacity=0.54)
        zym_blob.move_to([0.55, -0.15, 0.0])
        attach_turn(zym_blob, speed=0.38)
        self.play(FadeOut(dashed_outline, run_time=0.5), FadeIn(zym_blob, run_time=0.7))

        self.at("he named it zymase")
        zym_lbl = T("ZYMASE", size=34, color=TEXT, weight=BOLD).move_to(zym_blob.get_center())
        self.play(FadeIn(zym_lbl, run_time=0.5))

        self.at("1907 nobel prize")
        flask_tag = RoundedRectangle(corner_radius=0.10, width=2.4, height=1.35,
                                     stroke_color=TEXT, stroke_width=2.2,
                                     fill_color=BG, fill_opacity=0.92).move_to([4.75, -2.50, 0.0])
        medal_ring = Circle(radius=0.52, stroke_color=AMBER, stroke_width=4.0,
                            fill_color=BRASS_DARK, fill_opacity=0.90).move_to([4.75, -2.50, 0.0])
        medal_yr = T("1907", size=24, color=TEXT, weight=BOLD).move_to(medal_ring)
        medal_g = VGroup(flask_tag, medal_ring, medal_yr)
        self.play(FadeIn(medal_g, shift=UP * 0.25, run_time=0.7))
        self.finish()


class S03KuhneName(SpokenScene):
    def construct(self):
        bench = make_bench()
        top_y = bench.top_y

        init_y = top_y + 0.02
        plate_h = 0.46
        plate_y = top_y + 0.08 + plate_h / 2
        shift_y = plate_h + 0.06

        flask = make_flask([-3.8, init_y, 0.0], height=3.8, show_zyme=True, zymase_label=True, seed=7, n_bubbles=12)
        dish1 = make_dish([0.3, init_y, 0.0], label_text="PEPSIN", width=2.1, seed=2)
        dish2 = make_dish([3.8, init_y, 0.0], label_text="INVERTASE", width=2.1, seed=4)

        self.add(bench, flask)
        self.wait(0.4)

        self.at("pepsin")
        dish1.shift(RIGHT * 2.5)
        dish2.shift(RIGHT * 2.5)
        self.play(
            dish1.animate.shift(LEFT * 2.5),
            dish2.animate.shift(LEFT * 2.5),
            run_time=1.0,
        )

        self.at("1877")
        plate_box = RoundedRectangle(corner_radius=0.08, width=10.8, height=plate_h,
                                     stroke_color=AMBER, stroke_width=3.2,
                                     fill_color=BRASS_DARK, fill_opacity=0.92).move_to([0.0, plate_y, 0.0])
        plate_lbl = T('ENZYME  ("IN LEAVEN")', size=24, color=TEXT, weight=BOLD).move_to(plate_box)
        plate = VGroup(plate_box, plate_lbl).shift(DOWN * 0.5).set_opacity(0.0)
        self.add(plate)
        self.play(
            plate.animate.shift(UP * 0.5).set_opacity(1.0),
            flask.animate.shift(UP * shift_y),
            dish1.animate.shift(UP * shift_y),
            dish2.animate.shift(UP * shift_y),
            run_time=0.9,
        )
        self.finish()


class S04KuhneBelief(SpokenScene):
    def construct(self):
        bench = make_bench()
        top_y = bench.top_y
        plate_h = 0.46
        plate_y = top_y + 0.08 + plate_h / 2
        resting_y = top_y + 0.08 + plate_h + 0.04

        plate_box = RoundedRectangle(corner_radius=0.08, width=11.6, height=plate_h,
                                     stroke_color=AMBER, stroke_width=3.2,
                                     fill_color=BRASS_DARK, fill_opacity=0.92).move_to([0.0, plate_y, 0.0])
        plate_lbl = T('ENZYME  ("IN LEAVEN")', size=24, color=TEXT, weight=BOLD).move_to(plate_box)
        plate = VGroup(plate_box, plate_lbl)

        flask = make_flask([-3.7, resting_y, 0.0], height=3.55, show_zyme=True, zymase_label=True, seed=7, n_bubbles=10)
        yeast = make_yeast_cell([-5.55, 2.05, 0.0], height=1.45)
        dish1 = make_dish([-1.0, resting_y, 0.0], label_text="PEPSIN", width=1.85, seed=2)
        dish2 = make_dish([1.2, resting_y, 0.0], label_text="INVERTASE", width=1.85, seed=4)

        self.add(bench, plate, flask, yeast, dish1, dish2)

        self.at("digestion and vision")
        st_pts = [
            [2.85, -0.05, 0], [3.45, -0.05, 0], [3.85, -0.45, 0],
            [3.75, -1.10, 0], [3.10, -1.30, 0], [2.65, -0.95, 0], [2.85, -0.45, 0],
        ]
        stomach_out = VMobject(stroke_color=TEXT, stroke_width=2.8, fill_color=TEXT, fill_opacity=0.06)
        stomach_out.set_points_smoothly(st_pts + [st_pts[0]])
        stomach_lbl = T("STOMACH", size=24, color=TEXT).next_to(stomach_out, DOWN, buff=0.14)
        stomach_blob = make_enzyme(None, radius=0.30, lobes=5, color=TEAL, seed=31, fill_opacity=0.58).move_to([3.25, -0.72, 0])
        attach_turn(stomach_blob, 0.5)

        eye_top = ArcBetweenPoints([4.50, -0.72, 0], [6.00, -0.72, 0], angle=-1.40, color=TEXT, stroke_width=2.8)
        eye_bot = ArcBetweenPoints([4.50, -0.72, 0], [6.00, -0.72, 0], angle=1.40, color=TEXT, stroke_width=2.8)
        eye_out = VGroup(eye_top, eye_bot)
        eye_lbl = T("EYE", size=24, color=TEXT).next_to(eye_out, DOWN, buff=0.14)
        eye_blob = make_enzyme(None, radius=0.20, lobes=5, color=TEAL, seed=33, fill_opacity=0.58).move_to([5.25, -0.72, 0])
        attach_turn(eye_blob, 0.5)

        d_st = make_dish([3.25, 1.35, 0.0], label_text=None, width=1.45, seed=9)
        d_st.remove(d_st.enz)
        d_eye = make_dish([5.25, 1.35, 0.0], label_text=None, width=1.45, seed=10)
        d_eye.remove(d_eye.enz)

        organs = VGroup(stomach_out, stomach_lbl, eye_out, eye_lbl)
        self.play(FadeIn(organs, stomach_blob, eye_blob, d_st[0], d_st[1], d_eye[0], d_eye[1], run_time=0.75))

        self.at("lifted out of the cell")
        arr1 = Arrow([3.25, -0.15, 0], [3.25, 1.15, 0], buff=0.05, color=TEAL, stroke_width=3.2)
        arr2 = Arrow([5.25, -0.15, 0], [5.25, 1.15, 0], buff=0.05, color=TEAL, stroke_width=3.2)
        self.play(
            Create(arr1), Create(arr2),
            stomach_blob.animate.move_to([3.05, 1.75, 0.0]),
            eye_blob.animate.move_to([5.05, 1.75, 0.0]),
            run_time=1.0,
        )

        self.at("not the cell or the tissue")
        self.play(
            yeast.animate.set_opacity(0.22),
            organs.animate.set_opacity(0.22),
            flask.zymase.body.animate.set_fill(opacity=0.80),
            dish1.enz.body.animate.set_fill(opacity=0.80),
            dish2.enz.body.animate.set_fill(opacity=0.80),
            stomach_blob.body.animate.set_fill(opacity=0.80),
            eye_blob.body.animate.set_fill(opacity=0.80),
            run_time=0.8,
        )
        self.finish()


class S05Berthelot(SpokenScene):
    def construct(self):
        bench = make_bench()
        top_y = bench.top_y

        flask = make_flask([-4.6, top_y + 0.02, 0.0], height=3.65, show_zyme=True, zymase_label=True, seed=7, n_bubbles=10)
        bg_dish1 = make_dish([-2.3, top_y + 0.02, 0.0], label_text=None, width=1.2, seed=2).set_opacity(0.32)
        bg_dish2 = make_dish([-0.9, top_y + 0.02, 0.0], label_text=None, width=1.2, seed=4).set_opacity(0.32)
        self.add(bench, bg_dish1, bg_dish2, flask)

        self.at("other half is the rules")
        fat = make_fat_system([1.65, 0.65, 0.0], scale=1.0, show_fat_label=False, cycling=False, split_dx=0.85)
        self.play(FadeIn(fat.gly_g, fat.strips, run_time=0.7))

        self.at("1854")
        yr_lbl = T("1854", size=28, color=TEXT, weight=BOLD).move_to([1.65, 3.08, 0.0])
        self.play(FadeIn(yr_lbl, run_time=0.45))

        self.at("joined glycerol to fatty acids")
        for idx in range(3):
            sg = fat.strips[idx]
            dr = fat.drops[idx]
            dr.move_to([dr._seam_x, dr._seam_y, 0.0]).set_opacity(1.0)
            self.play(sg.animate.move_to([sg._joined_x, sg._y, 0.0]), run_time=0.52)
            self.play(dr.animate.move_to([dr._pool_x, dr._pool_y, 0.0]), run_time=0.40)

        self.play(fat.fat_badge.animate.set_opacity(1.0), run_time=0.4)

        self.at("add water")
        self.play(
            fat.fat_badge.animate.set_opacity(0.0),
            *[dr.animate.move_to([dr._seam_x, dr._seam_y, 0.0]).set_opacity(0.0) for dr in fat.drops],
            *[sg.animate.move_to([sg._split_x, sg._y, 0.0]) for sg in fat.strips],
            run_time=0.95,
        )

        fat._t = 0.0

        def _cycle(m, dt):
            m._t += dt
            u = 0.5 - 0.5 * np.cos(TAU * m._t / 4.4)
            for sg, dr in zip(m.strips, m.drops):
                sg.move_to([sg._split_x + u * (sg._joined_x - sg._split_x), sg._y, 0.0])
                dr.move_to([dr._seam_x + u * (dr._pool_x - dr._seam_x),
                            dr._seam_y + u * (dr._pool_y - dr._seam_y), 0.0])
                dr.set_opacity(np.clip((u - 0.25) / 0.35, 0.0, 1.0))
            if not getattr(m, "_pause_badge", False):
                m.fat_badge.set_opacity(1.0 if u > 0.72 else 0.0)

        fat.add_updater(_cycle)
        self.finish()


class S06Equilibrium(SpokenScene):
    def construct(self):
        bench = make_bench()
        top_y = bench.top_y

        flask = make_flask([-4.6, top_y + 0.02, 0.0], height=3.6, show_zyme=True, zymase_label=True, seed=7, n_bubbles=10)
        fat = make_fat_system([0.35, 1.15, 0.0], scale=0.90, show_fat_label=False, cycling=True, split_dx=0.72)
        rock_salt = make_rock_and_salt([4.6, top_y + 0.02, 0.0], scale=0.85)
        self.add(bench, flask, fat, rock_salt)

        self.at("equilibrium chemistry")
        eq_fat = attach_pulse_arrow(make_two_way_arrow([0.35, -1.55, 0.0], width=2.4, label="EQUILIBRIUM", color=TEAL))
        self.play(FadeIn(eq_fat, run_time=0.6))

        self.at("mineral world")
        eq_min = attach_pulse_arrow(make_two_way_arrow([4.6, -0.45, 0.0], width=2.1, label="EQUILIBRIUM", color=TEAL))
        self.play(FadeIn(eq_min, run_time=0.6))

        self.at("no special law")
        speck = Dot(radius=0.14, color=GOLD).move_to([0.35, 3.25, 0.0])
        self.play(FadeIn(speck, run_time=0.2))
        self.play(speck.animate.move_to([0.35, 2.55, 0.0]), run_time=0.60)
        self.play(speck.animate.move_to([2.05, 3.35, 0.0]).set_opacity(0.0), run_time=0.70)

        self.at("also made new fats")
        old_s = fat.strips[2]
        new_st = RoundedRectangle(corner_radius=0.07, width=old_s[0].width, height=old_s[0].height,
                                  stroke_color=GREEN, stroke_width=2.4,
                                  fill_color=GREEN, fill_opacity=0.94)
        new_lbl = T("FATTY ACID", size=24, color=BG, weight=BOLD).move_to(new_st)
        new_sg = VGroup(new_st, new_lbl).move_to(old_s.get_center())
        new_sg._joined_x = old_s._joined_x
        new_sg._split_x = old_s._split_x
        new_sg._y = old_s._y

        fat._pause_badge = True
        old_badge = fat.fat_badge
        fat.remove(old_badge)
        fat.strips.remove(old_s)
        self.add(old_s, old_badge)
        self.play(FadeOut(old_s, old_badge, run_time=0.2))

        u_now = 0.5 - 0.5 * np.cos(TAU * fat._t / 4.4)
        new_sg.move_to([new_sg._split_x + u_now * (new_sg._joined_x - new_sg._split_x), new_sg._y, 0.0])
        new_badge = T("NEW FAT", size=28, color=GREEN, weight=BOLD).move_to(old_badge.get_center())
        if u_now > 0.72:
            self.play(FadeIn(new_sg, new_badge, run_time=0.25))
            self.remove(new_sg, new_badge)
        else:
            new_badge.set_opacity(0.0)
            self.play(FadeIn(new_sg, run_time=0.25))
            self.remove(new_sg)
        fat.strips.add(new_sg)
        fat.fat_badge = new_badge
        fat.add(new_badge)
        fat._pause_badge = False
        self.finish()


class S07Idea(SpokenScene):
    def construct(self):
        bench = make_bench(with_same_rules=True, highlight_same_rules=False)
        top_y = bench.top_y

        plate_h = 0.42
        plate_box = RoundedRectangle(corner_radius=0.08, width=5.6, height=plate_h,
                                     stroke_color=AMBER, stroke_width=2.8,
                                     fill_color=BRASS_DARK, fill_opacity=0.92).move_to([-3.3, top_y + 0.06 + plate_h / 2, 0.0])
        plate_lbl = T("ENZYME", size=24, color=TEXT, weight=BOLD).move_to(plate_box)
        plate = VGroup(plate_box, plate_lbl)

        rest_left = plate_box.get_top()[1] + 0.04
        flask = make_flask([-5.0, rest_left, 0.0], height=2.95, show_zyme=False, seed=7, n_bubbles=9)
        dish1 = make_dish([-2.95, rest_left, 0.0], label_text="PEPSIN", width=1.40, seed=2)
        dish2 = make_dish([-1.05, rest_left, 0.0], label_text="INVERTASE", width=1.40, seed=4)
        yeast = make_yeast_cell([-5.05, 2.05, 0.0], height=1.35, opacity=0.45, label_dir=RIGHT)

        fat = make_fat_system([2.10, 1.15, 0.0], scale=0.72, show_fat_label=False, cycling=True, split_dx=0.55)
        eq_fat = attach_pulse_arrow(make_two_way_arrow([2.10, -1.45, 0.0], width=1.9, label="EQUILIBRIUM", color=TEAL))
        rock_salt = make_rock_and_salt([5.0, top_y + 0.04, 0.0], scale=0.72)

        self.add(bench, plate, flask, dish1, dish2, yeast, fat, eq_fat, rock_salt)

        self.at("where vitalists placed a force")
        yc = yeast.body.get_center()
        haze = VGroup(*[Dot(radius=0.09, color=GOLD).move_to(yc + np.array([dx, dy, 0]))
                        for dx, dy in [(-0.25, 0.2), (0.20, 0.30), (0.0, -0.25), (-0.18, -0.12)]])
        self.play(FadeIn(haze, run_time=0.4))

        self.at("ordinary chemistry")
        top_line = T("CATALYSTS + ORDINARY RULES", size=38, color=TEXT, weight=BOLD).move_to([0.0, 3.25, 0.0])
        self.play(FadeOut(haze, run_time=0.5), FadeIn(top_line, run_time=0.6))

        self.at("catalysts can be lifted out of the cell")
        lifted_blob = make_enzyme(None, radius=0.38, lobes=5, color=TEAL, seed=11, fill_opacity=0.62)
        lifted_blob.move_to(yeast.body.get_center())
        lift_arrow = CurvedArrow(yeast.body.get_left() + LEFT * 0.08,
                                 flask.get_left() + UP * 0.45 + LEFT * 0.05,
                                 angle=0.55, color=TEAL, stroke_width=3.0)
        self.play(FadeIn(lifted_blob, run_time=0.3), Create(lift_arrow, run_time=0.4))
        self.play(lifted_blob.animate.move_to(flask.liquid.get_center() + DOWN * 0.10), run_time=0.80)
        self.play(FadeOut(lift_arrow, run_time=0.3))
        attach_turn(lifted_blob, speed=0.4)

        self.at("same rules")
        self.play(
            bench.band.animate.set_fill(opacity=0.48).set_stroke(opacity=1.0),
            bench.band_lbl.animate.set_opacity(1.0),
            run_time=0.7,
        )
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        chamber = make_juice_chamber(seed=7, n_bubbles=18, bubble_mode="center")
        zym = make_enzyme("ZYMASE", radius=1.50, lobes=5, color=TEAL, label_size=36, seed=11, fill_opacity=0.55)
        zym.move_to([0.55, -0.15, 0.0])
        attach_turn(zym, speed=0.42)
        sugar_stream = make_sugar_stream(target_x=0.55, target_y=-0.15, start_x=-4.65, stop_gap=2.25)

        self.add(chamber, zym, sugar_stream)
        self.at("predict")
        q = question_card("ONE OR SEVERAL?", y=3.12, color=TEXT, size=38).move_to([0.0, 3.12, 0.0])
        self.play(FadeIn(q, run_time=0.6))
        self.finish()


class S09PredictHold(PredictPause):
    QUESTION = "ONE OR SEVERAL?"
    CARD = {"y": 3.12, "color": TEXT, "size": 38}
    RING_AT = (5.8, -2.9, 0)
    SECONDS = 4.5

    def backdrop(self):
        chamber = make_juice_chamber(seed=7, n_bubbles=18, bubble_mode="center")
        zym = make_enzyme("ZYMASE", radius=1.50, lobes=5, color=TEAL, label_size=36, seed=11, fill_opacity=0.55)
        zym.move_to([0.55, -0.15, 0.0])
        attach_turn(zym, speed=0.42)
        sugar_stream = make_sugar_stream(target_x=0.55, target_y=-0.15, start_x=-4.65, stop_gap=2.25)
        return VGroup(chamber, zym, sugar_stream)

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD).move_to([0.0, 3.12, 0.0])
        self.add(q)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S10Team(SpokenScene):
    def construct(self):
        chamber = make_juice_chamber(seed=7, n_bubbles=12, bubble_mode="chain")
        zym = make_enzyme("ZYMASE", radius=1.50, lobes=5, color=TEAL, label_size=36, seed=11, fill_opacity=0.55)
        zym.move_to([0.55, -0.15, 0.0])
        attach_turn(zym, speed=0.42)
        q = question_card("ONE OR SEVERAL?", y=3.12, color=TEXT, size=38).move_to([0.0, 3.12, 0.0])

        self.add(chamber, zym, q)
        self.play(FadeOut(q, run_time=0.4))

        self.at("split zymase into enzymes")
        xs = [-4.1, -2.05, 0.0, 2.05, 4.1]
        chain = VGroup(*[
            attach_turn(make_enzyme(None, radius=0.54, lobes=5, color=TEAL, seed=40 + k, fill_opacity=0.58).move_to([x, 0.0, 0.0]),
                        speed=0.45)
            for k, x in enumerate(xs)
        ])
        enz_lbl = T("ENZYMES", size=28, color=TEAL, weight=BOLD).move_to([0.0, 3.08, 0.0])
        sc_tag = scope_tag("SCHEMATIC", size=24, color=GREY).shift(LEFT * 0.40)
        zym.remove(zym.label)
        self.remove(zym)
        self.add(zym.body, zym.label)
        self.play(
            FadeOut(zym.label, run_time=0.25),
            ReplacementTransform(zym.body, chain, run_time=1.0),
            FadeIn(enz_lbl, sc_tag, run_time=1.0),
        )

        self.at("plus small")
        coins = VGroup(*[make_cofactor(radius=0.20) for _ in range(3)])
        coin_specs = [(0, 1, 0.0), (1, 2, 1.4), (3, 4, 0.7)]
        for c, (i, j, ph) in zip(coins, coin_specs):
            c._x0, c._x1, c._t = xs[i] + 0.65, xs[j] - 0.65, ph
            c.move_to([(c._x0 + c._x1) / 2, 0.72, 0.0])

            def _hop(m, dt):
                m._t += dt * 1.6
                s = 0.5 - 0.5 * np.cos(m._t)
                nx = m._x0 + s * (m._x1 - m._x0)
                ny = 0.62 + 0.25 * np.sin(np.pi * s)
                m.move_to([nx, ny, 0.0])

            c.add_updater(_hop)

        cof_lbl = T("COFACTORS", size=26, color=PURPLE, weight=BOLD).move_to([0.0, -2.25, 0.0])
        self.play(FadeIn(coins, cof_lbl, run_time=0.6))

        self.at("chief among them")
        feat = make_cofactor(radius=0.34).move_to([-0.85, -1.55, 0.0])
        coz_lbl = T("COZYMASE", size=26, color=PURPLE, weight=BOLD).next_to(feat, RIGHT, buff=0.24)
        self.play(FadeOut(cof_lbl, run_time=0.25), FadeIn(feat, coz_lbl, run_time=0.45))

        self.at("known as nad")
        nad_lbl = T("NAD", size=28, color=PURPLE, weight=BOLD).next_to(feat, RIGHT, buff=0.24)
        self.play(swap(coz_lbl, nad_lbl, run_time=0.55))

        self.at("run glycolysis")
        self.play(FadeOut(feat, nad_lbl, run_time=0.3))
        b_gly = BraceBetweenPoints([-4.65, 1.15, 0], [0.55, 1.15, 0], direction=UP, color=TEXT)
        t_gly = T("GLYCOLYSIS", size=26, color=TEXT, weight=BOLD).next_to(b_gly, UP, buff=0.12)
        sugar_blk = make_block("SUGAR", color=TEXT, text_color=BG, size=24, min_w=1.25, h=0.46).move_to([-5.05, -0.95, 0.0])
        self.play(FadeIn(b_gly, t_gly, sugar_blk, run_time=0.4))
        for x in xs[:3]:
            self.play(sugar_blk.animate.move_to([x, -0.95, 0.0]), run_time=0.28)

        self.at("2 steps that make ethanol")
        b_2 = BraceBetweenPoints([1.50, 1.15, 0], [4.65, 1.15, 0], direction=UP, color=TEAL)
        t_2 = T("2 STEPS", size=24, color=TEAL, weight=BOLD).next_to(b_2, UP, buff=0.12)
        self.play(FadeIn(b_2, t_2, run_time=0.4))
        for x in xs[3:]:
            self.play(sugar_blk.animate.move_to([x, -0.95, 0.0]), run_time=0.35)

        eth_blk = make_block("ETHANOL", color=TEXT, text_color=BG, size=24, min_w=1.40, h=0.46).move_to([4.95, -0.95, 0.0])
        self.play(swap(sugar_blk, eth_blk, run_time=0.5))

        self.at("open to study 1 at a time")
        spot = Circle(radius=1.35, stroke_color=TEXT, stroke_width=3.5).move_to([0.0, -0.25, 0.0])
        sub_mid = RoundedRectangle(corner_radius=0.07, width=0.85, height=0.36,
                                   stroke_color=TEXT, stroke_width=2.0,
                                   fill_color=TEXT, fill_opacity=0.92).move_to([0.0, -0.95, 0.0])
        self.play(
            Create(spot),
            FadeIn(sub_mid),
            *[chain[i].animate.set_opacity(0.25) for i in (0, 1, 3, 4)],
            run_time=0.5,
        )
        self.wait(0.6)
        self.play(
            FadeOut(spot, sub_mid),
            *[chain[i].animate.set_opacity(1.0) for i in (0, 1, 3, 4)],
            run_time=0.45,
        )
        self.finish()


class S11ProteinsUrea(SpokenScene):
    def construct(self):
        xs = [-4.1, -2.05, 0.0, 2.05, 4.1]
        chain = VGroup(*[
            attach_turn(make_enzyme(None, radius=0.54, lobes=5, color=TEAL, seed=40 + k, fill_opacity=0.58).move_to([x, 0.2, 0.0]),
                        speed=0.45)
            for k, x in enumerate(xs)
        ])
        coins = VGroup(*[make_cofactor(radius=0.20) for _ in range(3)])
        for c, (i, j) in zip(coins, [(0, 1), (1, 2), (3, 4)]):
            c.move_to([(xs[i] + xs[j]) / 2, 0.82, 0.0])
        enz_lbl = T("ENZYMES", size=28, color=TEAL, weight=BOLD).move_to([0.0, 2.15, 0.0])
        sc_tag = scope_tag("SCHEMATIC", size=24, color=GREY).shift(LEFT * 0.40)
        self.add(chain, coins, enz_lbl, sc_tag)

        self.at("nearly all of them proteins")
        prot_tags = VGroup(*[
            T("PROTEIN", size=24, color=TEXT, weight=BOLD).next_to(chain[k], DOWN, buff=0.24)
            for k in range(5)
        ])
        self.play(FadeIn(prot_tags, run_time=0.55))

        self.at("urea made in a flask")
        bench = make_bench()
        top_y = bench.top_y
        flask = make_flask([-4.6, top_y + 0.02, 0.0], height=3.35, show_zyme=True, zymase_label=True, seed=7, n_bubbles=10)

        w_flask = make_flask([-2.0, top_y + 0.02, 0.0], height=2.1, show_zyme=False, seed=19, n_bubbles=0)
        w_flask.liquid.set_fill(color=TEAL, opacity=0.18)
        urea_blk = make_block("UREA", color=TEXT, text_color=BG, size=24, min_w=1.15, h=0.46).move_to([-2.0, top_y + 2.55, 0.0])

        self.play(FadeOut(coins, enz_lbl, prot_tags, sc_tag, run_time=0.35))
        self.play(
            ReplacementTransform(chain, flask.zymase),
            FadeIn(bench, flask.liquid, flask.meniscus, flask.glass, flask.rim, flask.bubbles, flask.zymase_badge, w_flask, urea_blk, run_time=0.8),
        )

        self.at("your liver builds it right now")
        liver_g = make_liver_cycle([2.7, 0.65, 0.0], radius=1.50, scale=0.90)
        self.play(FadeIn(liver_g.liver, run_time=0.65))

        self.at("5 enzymes")
        five_lbl = T("5 ENZYMES", size=28, color=TEAL, weight=BOLD).move_to([2.7, 2.95, 0.0])
        self.play(FadeIn(liver_g.blobs, five_lbl, run_time=0.6))

        self.at("urea cycle")
        self.play(FadeIn(liver_g.track, liver_g.cyc_lbl, liver_g.carrier, liver_g.urea_drop, run_time=0.6))
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        bench = make_bench(with_same_rules=True, highlight_same_rules=False)
        top_y = bench.top_y

        flask = make_flask([-5.15, top_y + 0.02, 0.0], height=3.05, show_zyme=True, zymase_label=True, seed=7, n_bubbles=10)
        fat = make_fat_system([-1.55, 1.35, 0.0], scale=0.68, show_fat_label=False, cycling=True, split_dx=0.36)
        rock_salt = make_rock_and_salt([0.65, top_y + 0.02, 0.0], scale=0.72)
        liver_g = make_liver_cycle([4.35, 0.55, 0.0], radius=1.42, scale=0.75)

        gold_specks = VGroup(*[
            Dot(radius=0.10, color=GOLD).set_opacity(0.65).move_to([x, y, 0.0])
            for x, y in [(-3.4, 2.65), (-0.4, 2.85), (2.2, 2.65), (4.3, 2.85)]
        ])
        self.add(bench, flask, fat, rock_salt, liver_g, gold_specks)

        self.at("nowhere left to hide")
        self.play(
            *[sp.animate.shift(UP * 1.4).set_opacity(0.0) for sp in gold_specks],
            run_time=1.3,
        )

        self.at("pull out and study")
        sep_dish = make_dish([2.10, 2.22, 0.0], label_text=None, width=1.45, seed=15)
        sep_dish.enz.set_opacity(0.0)
        lifted = liver_g.blobs[0].copy().clear_updaters()
        self.play(FadeIn(sep_dish[0], sep_dish[1], sep_dish[3], run_time=0.4))
        self.play(lifted.animate.move_to([1.76, 2.64, 0.0]), run_time=0.9)
        attach_turn(lifted, speed=0.55)

        self.at("rocks and salts")
        self.play(
            bench.band.animate.set_fill(opacity=0.48).set_stroke(opacity=1.0),
            bench.band_lbl.animate.set_opacity(1.0),
            run_time=0.75,
        )
        self.finish()


class S13End(EndCard):
    LINE = "Life's chemistry follows ordinary rules, worked by catalysts we can isolate."
