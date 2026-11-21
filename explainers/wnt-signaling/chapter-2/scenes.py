"""
"Frizzled's Second Job: Aligning a Sheet" — STEMhop Explainer (wnt-signaling / chapter-2)

COLOUR MAP (one colour per concept for the entire film):
- Frizzled receptor       : FRIZZLED_COL = "#2EC4B6"  (Teal)
- Dishevelled             : DSH_COL      = "#F5A623"  (Amber)
- Van Gogh / Vangl        : VANGL_COL    = "#E85D9E"  (Magenta)
- Prickle                 : PRICKLE_COL  = "#B388FF"  (Lavender)
- Flamingo cadherin       : FLAMINGO_COL = "#E6ECF5"  (Silver-white)
- Wing actin hair / normal: HAIR_COL     = "#4ADE80"  (Emerald green)
- Misdirected / disrupted : MISDIR_COL   = "#FF6B4A"  (Coral-orange)
- Wnt signal / focus cue  : WNT_COL      = "#F5D547"  (Gold)
- beta-Catenin / TCF      : BETA_COL     = "#6C9EFF"  (Periwinkle blue)
- Cell membrane outline   : CELL_EDGE    = "#7D8CA3"  (Slate border)
- Cell interior fill      : CELL_FILL    = "#1C2436"  (Deep blue-slate)

ONE WORLD CARRIED THROUGH THE FILM:
A top-down hexagonal epithelial sheet of cells whose membrane edges sort Frizzled/Dishevelled
opposite Van Gogh/Prickle so neighbours align (first as the fly wing epithelium sprouting
emerald hairs toward the wing tip, then zoomed into six cells showing edge sorting and Flamingo
bridges, and finally widened into the vertebrate neural plate with a dashed midline that narrows
and folds into a tube).

WHAT CHANGES ON SCREEN (per spoken scene) & WHAT IT IS COMPUTED FROM:
- s01_hook: Film-1 Frizzled/Dishevelled->beta-catenin diagram gives way to a honeycomb sheet of
  hexagonal cells where emerald hairs sprout and rotate from random initial angles (seed 7) to 0 rad
  pointing toward the wing tip, without beta-catenin.
- s02_pcp_puzzle: The carried hexagonal sheet pans smoothly inside the safe frame while hairs
  illuminate column by column along x; a focus ring then isolates one cell and its 6 geometric
  neighbours.
- s03_mosaic: Five central cells lose Frizzled (dark dashed outlines) and their hairs rotate into
  disordered angles computed from RNG seed 13; flanking normal cells on Body and Tip sides gain
  highlight rings.
- s04_mosaic_result: Normal hairs on the tip side smoothly rotate by pi (backward toward the patch)
  and recolor to coral-orange while body-side hairs stay at 0 rad; small arrows on both sides aim
  at the patch with tip-side arrows highlighted as 'backward', then curved relay arrows propagate
  from neighbour to neighbour across borders.
- s05_edge_sorting: Six zoomed-in hexagonal cells sort RNG-seeded (seed 7) Frizzled/Dishevelled
  particles linearly to each cell's right (tip-side) vertical edge and Van Gogh/Prickle particles
  to each cell's left (body-side) vertical edge.
- s06_flamingo_hair: Silver Flamingo cadherin bridges extend across all 5 intercellular clefts,
  locking Frizzled-to-Van Gogh borders with each border bridge labelled 'Frizzled : Van Gogh',
  then tapered emerald actin hairs grow rightward from every Frizzled edge via a growth tracker (0 -> 1).
- s07_no_beta_catenin: Quiet nuclei appear inside the 6 cells with beta-catenin/TCF absent;
  local Frizzled/Dishevelled edge markers brighten and drive hair placement without nuclear signaling.
- s08_vertebrate_neural: The cell sheet reforms into a wide flat neural plate across x=0 midline;
  Wnt dots enter and midline-facing edges mark Frizzled (teal) vs outer Vangl (magenta); an
  intercalation tracker p (0 -> 1) computes cell convergence toward x=0, vertical elongation, and
  inward curling of the outer neural folds into a closed tube.
- s09_predict: The intercalation tracker rewinds (1 -> 0) back to the flat wide plate, edge polarity
  marks desaturate to neutral slate, and the question card fades in.
- s11_neural_defects: Side-by-side computed trajectories on TwoPanel: Left (Normal PCP) runs p: 0->1
  to narrow and close the folds; Right (Disrupted PCP) assigns random edge angles (seed 11), stalls
  convergence (p: 0->0.10), leaving the plate wide and coral neural folds open.
"""
from bp_parts import *

# ------------------------------------------------------------------ Concept palette
FRIZZLED_COL = "#2EC4B6"   # Teal
DSH_COL      = "#F5A623"   # Amber
VANGL_COL    = "#E85D9E"   # Magenta
PRICKLE_COL  = "#B388FF"   # Lavender
FLAMINGO_COL = "#E6ECF5"   # Silver-white
HAIR_COL     = "#4ADE80"   # Emerald
MISDIR_COL   = "#FF6B4A"   # Coral-orange
WNT_COL      = "#F5D547"   # Gold
BETA_COL     = "#6C9EFF"   # Periwinkle blue
CELL_EDGE    = "#7D8CA3"   # Cell outline
CELL_FILL    = "#1C2436"   # Cell interior fill


def dark_chip(text, border_color=TEXT, text_color=None, size=26, pad=0.22):
    """High-contrast rounded badge with dark BG fill so text always stays >10:1 readable."""
    tcol = border_color if text_color is None else text_color
    label = T(text, size=size, color=tcol)
    box = RoundedRectangle(
        corner_radius=0.14,
        width=label.width + 2 * pad,
        height=label.height + 2 * pad,
        stroke_color=border_color,
        stroke_width=2.5,
        fill_color=BG,
        fill_opacity=0.95,
    )
    return VGroup(box, label.move_to(box))


# ------------------------------------------------------------------ Geometry builders
def _hex_vertices(center, rx, ry=None):
    """Pointy-top hexagon vertices (vertical left & right edges)."""
    ry = rx if ry is None else ry
    cx, cy = center[0], center[1]
    angles = [np.pi / 6 + k * np.pi / 3 for k in range(6)]
    return [np.array([cx + rx * np.cos(a), cy + ry * np.sin(a), 0.0]) for a in angles]


def make_hex_cell(center, rx=0.56, ry=None, stroke_color=CELL_EDGE, stroke_width=2.8,
                  fill_color=CELL_FILL, fill_opacity=0.85, dashed=False):
    verts = _hex_vertices(center, rx, ry)
    poly = Polygon(*verts, stroke_color=stroke_color, stroke_width=stroke_width,
                   fill_color=fill_color, fill_opacity=fill_opacity)
    if dashed:
        dash_edges = VGroup(*[
            DashedLine(verts[i], verts[(i + 1) % 6], color=stroke_color,
                       stroke_width=stroke_width, dash_length=0.10)
            for i in range(6)
        ])
        fill_poly = Polygon(*verts, stroke_width=0, fill_color=fill_color, fill_opacity=fill_opacity)
        return VGroup(fill_poly, dash_edges)
    return poly


def make_wing_hair(origin, length=0.54, angle=0.0, color=HAIR_COL, base_w=0.11):
    """Tapered sharp actin wing hair starting at `origin` pointing at `angle`."""
    tip = np.array([length, 0.0, 0.0])
    b1 = np.array([0.0, base_w / 2.0, 0.0])
    b2 = np.array([0.0, -base_w / 2.0, 0.0])
    hair = Polygon(b1, tip, b2, stroke_color=color, stroke_width=2.0,
                   fill_color=color, fill_opacity=0.95)
    hair.rotate(angle, about_point=ORIGIN)
    hair.shift(origin)
    return hair


def build_wing_sheet(cols=10, rows=5, rx=0.56, origin=np.array([0.0, 0.0, 0.0]),
                     mutant_rc=None, hair_angles=None, hair_colors=None,
                     hair_scale=1.0, show_fz_edges=False):
    """Build a honeycomb sheet of pointy-top hexagonal cells with emerald hairs."""
    mutant_rc = set(mutant_rc or ())
    hair_angles = hair_angles or {}
    hair_colors = hair_colors or {}
    dx = np.sqrt(3) * rx
    dy = 1.5 * rx
    cells = {}
    polys = VGroup()
    edges = VGroup()
    hairs = VGroup()
    for r in range(rows):
        row_shift = 0.5 * dx if (r % 2 == 1) else 0.0
        for c in range(cols):
            cx = origin[0] + (c - (cols - 1) / 2.0) * dx + row_shift - 0.25 * dx
            cy = origin[1] + ((rows - 1) / 2.0 - r) * dy
            center = np.array([cx, cy, 0.0])
            is_mut = (r, c) in mutant_rc
            poly = make_hex_cell(
                center, rx=rx,
                stroke_color=MISDIR_COL if is_mut else CELL_EDGE,
                stroke_width=3.0 if is_mut else 2.5,
                fill_color="#121620" if is_mut else CELL_FILL,
                fill_opacity=0.9 if is_mut else 0.78,
                dashed=is_mut,
            )
            polys.add(poly)
            rv = rx * np.sqrt(3) / 2.0 * 0.88
            hv = rx * 0.43
            fz_e = Line(center + np.array([rv, -hv, 0]), center + np.array([rv, hv, 0]),
                        color=FRIZZLED_COL, stroke_width=5.0)
            vg_e = Line(center + np.array([-rv, -hv, 0]), center + np.array([-rv, hv, 0]),
                        color=VANGL_COL, stroke_width=5.0)
            if show_fz_edges and not is_mut:
                edges.add(fz_e)
            ang = hair_angles.get((r, c), 0.0)
            hcol = hair_colors.get((r, c), HAIR_COL)
            h_len = 0.54 * (rx / 0.56) * hair_scale
            if is_mut:
                anchor = center - np.array([np.cos(ang), np.sin(ang), 0.0]) * (0.20 * h_len)
            else:
                anchor = center + np.array([-0.10 * rx, 0.0, 0.0])
                if ang > np.pi / 2 or ang < -np.pi / 2:
                    anchor = center + np.array([0.15 * rx, 0.0, 0.0])
            hair = make_wing_hair(anchor, length=max(h_len, 0.02), angle=ang,
                                  color=hcol, base_w=0.115 * (rx / 0.56))
            hairs.add(hair)
            cells[(r, c)] = {
                "poly": poly, "hair": hair, "center": center,
                "fz_edge": fz_e, "vg_edge": vg_e, "rx": rx, "is_mut": is_mut
            }
    grp = VGroup(polys, edges, hairs)
    return grp, cells


def build_six_cell_row(y_center=-0.05, rx=0.98, ry=1.95, gap=0.22):
    """Build the zoomed-in row of 6 tall hexagonal cells filling ~65% of frame height."""
    hex_w = np.sqrt(3) * rx
    dx = hex_w + gap
    cells = []
    group = VGroup()
    for i in range(6):
        cx = (i - 2.5) * dx
        center = np.array([cx, y_center, 0.0])
        poly = make_hex_cell(center, rx=rx, ry=ry, stroke_color=CELL_EDGE,
                             stroke_width=3.2, fill_color=CELL_FILL, fill_opacity=0.82)
        group.add(poly)
        right_x = cx + hex_w / 2.0
        left_x = cx - hex_w / 2.0
        edge_y = ry * 0.48
        cells.append({
            "poly": poly, "center": center,
            "right_x": right_x, "left_x": left_x, "edge_y": edge_y,
            "rx": rx, "ry": ry,
        })
    return group, cells


def neural_plate_geometry(p, center=ORIGIN, scale_x=1.0, scale_y=1.0,
                          cols=8, rows=4, random_angles=None):
    """Compute neural plate cell centers, cell half-widths/heights, and plate bounds."""
    base_cw = 1.12 * scale_x
    base_ch = 0.78 * scale_y
    cw = base_cw * (1.0 - 0.56 * p)
    ch = base_ch * (1.0 + 0.72 * p)
    cells = []
    for r in range(rows):
        intercal = (0.20 * cw * p) * (1.0 if r % 2 == 0 else -1.0)
        for c in range(cols):
            col_offset = c - (cols - 1) / 2.0
            x = center[0] + col_offset * cw + intercal * (1.0 - abs(col_offset) / (cols / 2.0)) * 0.6
            squeeze_y = 0.08 * ch * p * (1.0 if c % 2 == 0 else -1.0) * (1.0 - abs(col_offset) / cols)
            y = center[1] + ((rows - 1) / 2.0 - r) * ch + squeeze_y
            if random_angles is not None:
                ang = random_angles[r * cols + c]
            else:
                ang = 0.0 if col_offset < 0 else np.pi
            cells.append({
                "pos": np.array([x, y, 0.0]),
                "rx": cw * 0.48,
                "ry": ch * 0.46,
                "ang": ang,
                "side": -1 if col_offset < 0 else 1,
            })
    plate_half_w = (cols / 2.0) * cw + 0.12 * scale_x
    plate_half_h = (rows / 2.0) * ch + 0.14 * scale_y
    return cells, plate_half_w, plate_half_h


def render_neural_plate(p, center=ORIGIN, scale_x=1.0, scale_y=1.0,
                        polarity_mode="normal", fold_close=True,
                        random_angles=None, show_wnt=False):
    """Build a snapshot VGroup of the neural plate at intercalation progress p in [0, 1]."""
    cells, hw, hh = neural_plate_geometry(p, center=center, scale_x=scale_x, scale_y=scale_y,
                                          random_angles=random_angles)
    g = VGroup()
    sheet_bg = RoundedRectangle(
        corner_radius=0.26, width=2 * hw + 0.34 * scale_x, height=2 * hh + 0.30 * scale_y,
        stroke_color=CELL_EDGE, stroke_width=2.5, fill_color="#141A29", fill_opacity=0.78
    ).move_to(center)
    g.add(sheet_bg)

    for info in cells:
        pos, rx, ry, ang = info["pos"], info["rx"], info["ry"], info["ang"]
        cell = make_hex_cell(pos, rx=rx, ry=ry, stroke_color=CELL_EDGE, stroke_width=2.0,
                             fill_color=CELL_FILL, fill_opacity=0.88)
        g.add(cell)
        if polarity_mode != "none":
            if polarity_mode == "grey":
                c1, c2 = "#6B7280", "#4B5563"
            else:
                c1, c2 = FRIZZLED_COL, VANGL_COL
            offset = np.array([rx * 0.58 * np.cos(ang), ry * 0.58 * np.sin(ang), 0.0])
            perp = np.array([-np.sin(ang), np.cos(ang), 0.0])
            e_len = min(rx, ry) * 0.42
            p_m = pos + offset
            g.add(Line(p_m - perp * e_len, p_m + perp * e_len, color=c1, stroke_width=5.0))
            p_l = pos - offset
            g.add(Line(p_l - perp * e_len, p_l + perp * e_len, color=c2, stroke_width=5.0))

    mid = DashedLine(center + UP * (hh + 0.16 * scale_y), center + DOWN * (hh + 0.16 * scale_y),
                     color="#CBD5E1", stroke_width=2.8, dash_length=0.14)
    g.add(mid)

    if fold_close:
        fold_in = p * (hw - 0.14 * scale_x)
        fold_col = HAIR_COL if polarity_mode == "normal" else (MISDIR_COL if polarity_mode == "scrambled" else "#8B93A1")
        lx = center[0] - hw + fold_in
        rx_f = center[0] + hw - fold_in
        left_fold = ArcBetweenPoints(
            np.array([lx, center[1] - hh, 0.0]),
            np.array([lx, center[1] + hh, 0.0]),
            angle=-0.25 * (1.0 - p) + 0.01,
            color=fold_col, stroke_width=6.0,
        )
        right_fold = ArcBetweenPoints(
            np.array([rx_f, center[1] - hh, 0.0]),
            np.array([rx_f, center[1] + hh, 0.0]),
            angle=0.25 * (1.0 - p) - 0.01,
            color=fold_col, stroke_width=6.0,
        )
        if p > 0.05:
            flap_w = max(0.08, fold_in)
            l_flap = Rectangle(width=flap_w, height=2 * hh, stroke_width=0,
                               fill_color=fold_col, fill_opacity=0.14).move_to(
                                   [center[0] - hw + flap_w / 2.0, center[1], 0.0])
            r_flap = Rectangle(width=flap_w, height=2 * hh, stroke_width=0,
                               fill_color=fold_col, fill_opacity=0.14).move_to(
                                   [center[0] + hw - flap_w / 2.0, center[1], 0.0])
            g.add(l_flap, r_flap)
        g.add(left_fold, right_fold)

    if show_wnt:
        rng = np.random.default_rng(19)
        for _ in range(10):
            wx = center[0] + rng.uniform(-hw * 0.9, hw * 0.9)
            wy = center[1] + rng.uniform(-hh * 0.9, hh * 0.9)
            g.add(Dot([wx, wy, 0.0], radius=0.075, color=WNT_COL).set_opacity(0.9))
    return g


def build_sorted_six_cells_state():
    """Shared builder for the sorted 6-cell row carried across s05 -> s06 -> s07."""
    row_group, cells = build_six_cell_row(y_center=-0.05, rx=0.98, ry=1.95, gap=0.22)
    fz_bars, vg_bars = VGroup(), VGroup()
    dots = VGroup()
    for c in cells:
        cx, cy = c["center"][0], c["center"][1]
        rx_in = c["right_x"] - 0.16
        lx_in = c["left_x"] + 0.16
        ys = np.linspace(-c["edge_y"] * 0.78, c["edge_y"] * 0.78, 4)
        fz_bars.add(Line([c["right_x"] - 0.04, cy - c["edge_y"], 0],
                         [c["right_x"] - 0.04, cy + c["edge_y"], 0],
                         color=FRIZZLED_COL, stroke_width=7.5))
        vg_bars.add(Line([c["left_x"] + 0.04, cy - c["edge_y"], 0],
                         [c["left_x"] + 0.04, cy + c["edge_y"], 0],
                         color=VANGL_COL, stroke_width=7.5))
        for y_off in ys:
            dots.add(Dot([rx_in + 0.05, cy + y_off, 0], radius=0.085, color=FRIZZLED_COL))
            dots.add(Dot([rx_in - 0.14, cy + y_off, 0], radius=0.080, color=DSH_COL))
            dots.add(Dot([lx_in - 0.05, cy + y_off, 0], radius=0.085, color=VANGL_COL))
            dots.add(Dot([lx_in + 0.14, cy + y_off, 0], radius=0.080, color=PRICKLE_COL))
    return row_group, cells, fz_bars, vg_bars, dots


# ================================================================== SCENES
class S00Title(TitleCard):
    LESSON = "Wnt: β-Catenin and Planar Polarity"
    TITLE = "Frizzled's Second Job: Aligning a Sheet"


class S01Hook(SpokenScene):
    def construct(self):
        # Film 1 compact callback box on upper-left; wing outline on right
        f1_box = RoundedRectangle(corner_radius=0.16, width=4.9, height=3.0,
                                  stroke_color=CELL_EDGE, stroke_width=2.2,
                                  fill_color="#141A29", fill_opacity=0.92).move_to([-4.0, 1.80, 0])
        f1_head = T("Film 1: β-catenin path", 24, TEXT).move_to([-4.0, 2.78, 0])
        fz_chip = dark_chip("Frizzled", FRIZZLED_COL, size=24).move_to([-5.15, 2.02, 0])
        dsh_chip = dark_chip("Dishevelled", DSH_COL, size=24).move_to([-2.85, 2.02, 0])
        bcat_chip = dark_chip("β-catenin saved", BETA_COL, size=24).move_to([-4.0, 0.78, 0])
        f1_arrow = Arrow([-4.0, 1.60, 0], [-4.0, 1.18, 0], buff=0.0, color=TEXT, stroke_width=3, tip_length=0.14)
        f1_group = VGroup(f1_box, f1_head, fz_chip, dsh_chip, f1_arrow, bcat_chip)

        # Fly-wing outline on the right
        wing_body = Polygon(
            [-0.7, 0.2, 0], [0.9, 1.6, 0], [3.9, 1.9, 0], [5.7, 0.8, 0],
            [5.8, -0.3, 0], [4.1, -1.7, 0], [1.0, -1.5, 0], [-0.7, -0.4, 0],
            stroke_color=CELL_EDGE, stroke_width=3.5, fill_color="#161D2E", fill_opacity=0.85
        ).round_corners(0.6)
        wing_title = T("Fly wing", 28, TEXT).next_to(wing_body, UP, buff=0.20)

        rng = np.random.default_rng(7)
        init_angles = {(r, c): float(rng.uniform(-np.pi * 0.75, np.pi * 0.75))
                       for r in range(5) for c in range(10)}
        sheet_init, cells_init = build_wing_sheet(
            cols=10, rows=5, rx=0.56, origin=np.array([0.0, 0.0, 0.0]),
            hair_angles=init_angles, hair_scale=0.18
        )
        sheet_target, cells_target = build_wing_sheet(
            cols=10, rows=5, rx=0.56, origin=np.array([0.0, 0.0, 0.0]),
            hair_angles={}, hair_scale=1.0, show_fz_edges=True
        )
        tip_lbl = T("Wing tip →", 28, HAIR_COL).move_to([4.7, 3.05, 0])
        tag = scope_tag("schematic")

        self.play(FadeIn(f1_box), FadeIn(f1_head), FadeIn(wing_body), FadeIn(wing_title), run_time=1.3)

        self.at("frizzled")
        self.play(FadeIn(fz_chip, shift=UP * 0.1), FadeIn(dsh_chip, shift=UP * 0.1), run_time=1.4)

        self.at("from destruction")
        self.play(GrowArrow(f1_arrow), FadeIn(bcat_chip, shift=DOWN * 0.1), run_time=1.5)

        self.at("How can those")
        # Dim Film 1 box and zoom cleanly into the honeycomb sheet
        self.play(FadeOut(VGroup(f1_group, wing_body, wing_title)), run_time=0.55)
        self.play(FadeIn(sheet_init, scale=0.84), FadeIn(tag), run_time=0.85)

        self.at("align every hair")
        anims = [Transform(c_init["hair"], cells_target[k]["hair"]) for k, c_init in cells_init.items()]
        self.play(FadeIn(tip_lbl), *anims, run_time=1.7)

        self.at("without")
        no_bcat = dark_chip("× No β-catenin", MISDIR_COL, size=26).move_to([-4.35, 3.05, 0])
        self.play(FadeIn(no_bcat, shift=DOWN * 0.08), run_time=1.2)

        self.at("They run a")
        sep_lbl = T("Separate polarity system", 32, FRIZZLED_COL).move_to([-0.5, -3.05, 0])
        fz_edges = VGroup(*[c["fz_edge"] for c in cells_target.values()])
        self.play(FadeIn(sep_lbl), LaggedStart(*[Create(e) for e in fz_edges], lag_ratio=0.02),
                  run_time=2.5)
        self.finish()


class S02PcpPuzzle(SpokenScene):
    def construct(self):
        # Carried 10x5 sheet starting shifted slightly right so panning left stays inside [-6.2, 6.2]
        sheet, cells = build_wing_sheet(
            cols=10, rows=5, rx=0.56, origin=np.array([0.45, 0.0, 0.0]),
            show_fz_edges=True
        )
        tip_lbl = T("Wing tip →", 28, HAIR_COL).move_to([4.7, 3.05, 0])
        tag = scope_tag("schematic")
        self.add(sheet, tip_lbl, tag)

        # Gentle pan leftward (0.45 -> -0.45: sheet stays inside [-5.7, +5.7])
        self.play(sheet.animate.shift(LEFT * 0.45), run_time=3.5, rate_func=linear)

        self.at("Every cell grows")
        cols_order = sorted(cells.keys(), key=lambda rc: (rc[1], rc[0]))
        flashes = [Indicate(cells[k]["hair"], color=WNT_COL, scale_factor=1.25) for k in cols_order]
        self.play(LaggedStart(*flashes, lag_ratio=0.03), sheet.animate.shift(LEFT * 0.30), run_time=2.8)

        self.at("points toward the")
        self.play(Indicate(tip_lbl, color=WNT_COL, scale_factor=1.15),
                  sheet.animate.shift(LEFT * 0.20), run_time=2.0)

        self.at("This shared direction")
        head = T("Planar cell polarity", 36, TEXT).move_to([-1.2, 3.05, 0])
        dir_arrow = Arrow([-4.5, -2.55, 0], [3.5, -2.55, 0], color=HAIR_COL, stroke_width=4.5)
        dir_lbl = T("Shared direction across the sheet", 28, HAIR_COL).move_to([-0.5, -3.10, 0])
        self.play(FadeIn(head, shift=DOWN * 0.08), GrowArrow(dir_arrow), FadeIn(dir_lbl), run_time=3.8)

        self.at("Yet no single")
        # Clear bottom arrow & label before bringing in Local view only
        self.play(FadeOut(VGroup(dir_arrow, dir_lbl)), run_time=0.25)

        center_cell = cells[(2, 4)]
        c_pt = center_cell["poly"].get_center()
        focus_ring = Circle(radius=1.68, color=WNT_COL, stroke_width=5.0).move_to(c_pt)
        focus_ring.layout_ok = True
        local_lbl = dark_chip("Local view only", WNT_COL, size=26).move_to([c_pt[0], -2.95, 0])
        ptr = Line([c_pt[0], local_lbl.get_top()[1] + 0.05, 0],
                   [c_pt[0], c_pt[1] - 1.72, 0], color=WNT_COL, stroke_width=3.0)

        dim_anims = []
        keep_rc = {(2, 4), (2, 3), (2, 5), (1, 3), (1, 4), (3, 3), (3, 4)}
        for rc, cinfo in cells.items():
            if rc not in keep_rc:
                dim_anims.append(cinfo["poly"].animate.set_opacity(0.28))
                dim_anims.append(cinfo["hair"].animate.set_opacity(0.28))
                dim_anims.append(cinfo["fz_edge"].animate.set_opacity(0.28))
        self.play(*dim_anims, Create(focus_ring), Create(ptr), FadeIn(local_lbl), run_time=1.1)
        self.finish()


class S03Mosaic(SpokenScene):
    def construct(self):
        # Carried 10x5 sheet restored to full brightness at origin=[0, -0.05, 0]
        sheet, cells = build_wing_sheet(
            cols=10, rows=5, rx=0.56, origin=np.array([0.0, -0.05, 0.0]),
            show_fz_edges=True
        )
        head = T("Planar cell polarity", 34, TEXT).move_to([-1.2, 3.05, 0])
        tip_lbl = T("Wing tip →", 28, HAIR_COL).move_to([4.7, 3.05, 0])
        tag = scope_tag("schematic")
        self.add(sheet, head, tip_lbl, tag)

        # Gentle focus shift while introducing the experiment
        self.play(sheet.animate.shift(RIGHT * 0.15), run_time=2.4, rate_func=linear)

        self.at("Charles Vinson")
        cite = T("Vinson & Adler, 1987", 26, WNT_COL).move_to([-4.3, -3.05, 0])
        self.play(FadeIn(cite, shift=UP * 0.1), run_time=1.3)

        self.at("small patches lacking")
        mutant_rc = {(2, 4), (2, 5), (1, 4), (3, 4), (1, 3)}
        rng = np.random.default_rng(13)
        mut_angles = {rc: float(rng.uniform(-np.pi, np.pi)) for rc in mutant_rc}
        mut_anims = []
        for rc in mutant_rc:
            cinfo = cells[rc]
            ang = mut_angles[rc]
            h_len = 0.54
            anchor = cinfo["poly"].get_center() - np.array([np.cos(ang), np.sin(ang), 0.0]) * (0.20 * h_len)
            new_hair = make_wing_hair(anchor, length=h_len, angle=ang, color=MISDIR_COL, base_w=0.115)
            mut_anims.extend([
                cinfo["poly"].animate.set_stroke(MISDIR_COL, width=3.2).set_fill("#0d1017", opacity=0.95),
                FadeOut(cinfo["fz_edge"]),
                Transform(cinfo["hair"], new_hair),
            ])
        no_fz_lbl = dark_chip("No Frizzled patch", MISDIR_COL, size=26).move_to([0.0, 2.90, 0])
        self.play(FadeOut(head), run_time=0.4)
        self.play(*mut_anims, FadeIn(no_fz_lbl), run_time=3.6)

        self.at("looked closely at")
        spin_anims = [
            Rotate(cells[rc]["hair"], angle=float(rng.uniform(-0.8, 0.8)),
                   about_point=cells[rc]["poly"].get_center())
            for rc in mutant_rc
        ]
        self.play(*spin_anims, run_time=0.85)

        self.at("normal cells beside")
        body_rc = [(2, 3), (3, 3)]
        tip_rc = [(2, 6), (1, 5), (3, 5)]
        body_rings = VGroup(*[
            make_hex_cell(cells[rc]["poly"].get_center(), rx=0.56,
                          stroke_color=HAIR_COL, stroke_width=4.8, fill_opacity=0.0)
            for rc in body_rc
        ])
        tip_rings = VGroup(*[
            make_hex_cell(cells[rc]["poly"].get_center(), rx=0.56,
                          stroke_color=WNT_COL, stroke_width=4.8, fill_opacity=0.0)
            for rc in tip_rc
        ])
        body_lbl = dark_chip("Body side", HAIR_COL, size=26).move_to([-4.1, 2.90, 0])
        tip_lbl_side = dark_chip("Tip side", WNT_COL, size=26).move_to([4.1, 2.90, 0])
        self.play(FadeOut(tip_lbl), run_time=0.3)
        self.play(Create(body_rings), Create(tip_rings), FadeIn(body_lbl), FadeIn(tip_lbl_side), run_time=1.9)
        self.finish()


class S04MosaicResult(SpokenScene):
    def construct(self):
        mutant_rc = {(2, 4), (2, 5), (1, 4), (3, 4), (1, 3)}
        rng = np.random.default_rng(13)
        mut_angles = {rc: float(rng.uniform(-np.pi, np.pi)) for rc in mutant_rc}
        mut_colors = {rc: MISDIR_COL for rc in mutant_rc}

        sheet, cells = build_wing_sheet(
            cols=10, rows=5, rx=0.56, origin=np.array([0.15, -0.05, 0.0]),
            mutant_rc=mutant_rc, hair_angles=mut_angles, hair_colors=mut_colors,
            show_fz_edges=True
        )
        no_fz_lbl = dark_chip("No Frizzled patch", MISDIR_COL, size=26).move_to([0.0, 2.90, 0])
        body_lbl = dark_chip("Body side", HAIR_COL, size=26).move_to([-4.1, 2.90, 0])
        tip_lbl_side = dark_chip("Tip side", WNT_COL, size=26).move_to([4.1, 2.90, 0])
        cite = T("Vinson & Adler, 1987", 24, WNT_COL).move_to([-4.3, -3.05, 0])
        tag = scope_tag("schematic")

        body_rc = [(2, 3), (3, 3)]
        tip_rc = [(2, 6), (1, 5), (3, 5), (2, 7)]
        body_rings = VGroup(*[
            make_hex_cell(cells[rc]["poly"].get_center(), rx=0.56,
                          stroke_color=HAIR_COL, stroke_width=4.8, fill_opacity=0.0)
            for rc in body_rc
        ])
        tip_rings = VGroup(*[
            make_hex_cell(cells[rc]["poly"].get_center(), rx=0.56,
                          stroke_color=WNT_COL, stroke_width=4.8, fill_opacity=0.0)
            for rc in tip_rc[:3]
        ])
        self.add(sheet, no_fz_lbl, body_lbl, tip_lbl_side, cite, tag, body_rings, tip_rings)

        # Normal hairs next to the patch point toward it (tip-side hairs rotate backward;
        # small arrows on both sides aim at the patch).
        body_toward_arrows = VGroup(*[
            Arrow(
                cells[rc]["poly"].get_center() + np.array([-0.24, 0.24, 0.0]),
                cells[rc]["poly"].get_center() + np.array([0.24, 0.24, 0.0]),
                buff=0, color=WNT_COL, stroke_width=4.0, tip_length=0.14,
            )
            for rc in body_rc
        ])
        tip_toward_arrows = VGroup(*[
            Arrow(
                cells[rc]["poly"].get_center() + np.array([0.24, 0.24, 0.0]),
                cells[rc]["poly"].get_center() + np.array([-0.24, 0.24, 0.0]),
                buff=0, color=WNT_COL, stroke_width=4.0, tip_length=0.14,
            )
            for rc in tip_rc[:3]
        ])

        flip_anims = []
        for rc in tip_rc:
            cinfo = cells[rc]
            center = cinfo["poly"].get_center()
            rx = 0.56
            new_hair = make_wing_hair(center + np.array([0.15 * rx, 0.0, 0.0]),
                                      length=0.54, angle=np.pi,
                                      color=HAIR_COL, base_w=0.115)
            flip_anims.append(Transform(cinfo["hair"], new_hair))
        self.play(*flip_anims, run_time=1.8)

        self.at("point toward")
        self.play(
            LaggedStart(*[GrowArrow(a) for a in body_toward_arrows], lag_ratio=0.12),
            LaggedStart(*[GrowArrow(a) for a in tip_toward_arrows], lag_ratio=0.12),
            run_time=1.4,
        )

        self.at("on the tip")
        tip_misdir_lbl = dark_chip("Tip side: misdirected", MISDIR_COL, size=26).move_to([4.1, 2.90, 0])
        backward_chip = dark_chip("← backward", MISDIR_COL, size=24).move_to([3.8, -2.65, 0])
        tip_target_pt = cells[(3, 5)]["poly"].get_center() + np.array([0.0, 0.16, 0.0])
        backward_ptr = Line(backward_chip.get_top() + UP * 0.05, tip_target_pt,
                            color=MISDIR_COL, stroke_width=2.8)
        self.play(swap(tip_lbl_side, tip_misdir_lbl, run_time=0.6))
        self.play(
            *[cells[rc]["hair"].animate.set_color(MISDIR_COL) for rc in tip_rc],
            tip_rings.animate.set_stroke(color=MISDIR_COL),
            tip_toward_arrows.animate.set_color(MISDIR_COL),
            FadeIn(backward_chip, shift=UP * 0.06),
            Create(backward_ptr),
            run_time=2.5,
        )

        self.at("on the body")
        body_ok_lbl = dark_chip("Body side: normal", HAIR_COL, size=26).move_to([-4.1, 2.90, 0])
        self.play(swap(body_lbl, body_ok_lbl, run_time=0.6))
        self.play(
            body_rings.animate.set_stroke(width=8.0),
            body_toward_arrows.animate.set_color(HAIR_COL),
            *[cells[rc]["hair"].animate.scale(1.18) for rc in body_rc],
            run_time=2.4,
        )

        self.at("Because genetically")
        gen_norm = T("Normal genes, wrong direction", 28, MISDIR_COL).move_to([-1.3, -3.05, 0])
        self.play(FadeOut(cite, run_time=0.35))
        self.play(
            FadeIn(gen_norm, shift=UP * 0.08),
            tip_rings.animate.set_stroke(width=8.0),
            *[cells[rc]["hair"].animate.scale(1.15) for rc in tip_rc],
            run_time=2.4,
        )

        self.at("pass polarity information")
        relay_pairs = [((2, 1), (2, 2)), ((2, 2), (2, 3)), ((2, 5), (2, 6)), ((2, 6), (2, 7))]
        relay_arrows = VGroup()
        for a_rc, b_rc in relay_pairs:
            p1 = cells[a_rc]["poly"].get_center() + UP * 0.14
            p2 = cells[b_rc]["poly"].get_center() + UP * 0.14
            arc = CurvedArrow(p1, p2, angle=-0.52, color=WNT_COL, stroke_width=4.2, tip_length=0.16)
            relay_arrows.add(arc)
        relay_lbl = dark_chip("Neighbour-to-neighbour cue", WNT_COL, size=26).move_to([0.0, -3.05, 0])
        self.play(
            FadeOut(body_toward_arrows, run_time=0.35),
            FadeOut(tip_toward_arrows, run_time=0.35),
            FadeOut(backward_chip, run_time=0.35),
            FadeOut(backward_ptr, run_time=0.35),
            swap(gen_norm, relay_lbl, run_time=0.65),
        )
        self.play(LaggedStart(*[Create(a) for a in relay_arrows], lag_ratio=0.22), run_time=3.4)
        self.finish()


class S05EdgeSorting(SpokenScene):
    def construct(self):
        prev_sheet, _ = build_wing_sheet(cols=10, rows=5, rx=0.56, origin=np.array([0.0, -0.05, 0.0]))
        self.add(prev_sheet)

        row_group, cells = build_six_cell_row(y_center=-0.05, rx=0.98, ry=1.95, gap=0.22)
        tag = scope_tag("schematic")
        head = T("Inside each normal wing cell", 34, TEXT).move_to([0.0, 3.2, 0])

        rng = np.random.default_rng(7)
        fz_dots, dsh_dots, vg_dots, pk_dots = VGroup(), VGroup(), VGroup(), VGroup()
        fz_targets, dsh_targets, vg_targets, pk_targets = [], [], [], []
        for c in cells:
            cx, cy = c["center"][0], c["center"][1]
            rx_in = c["right_x"] - 0.16
            lx_in = c["left_x"] + 0.16
            ys = np.linspace(-c["edge_y"] * 0.78, c["edge_y"] * 0.78, 4)
            for k in range(4):
                p_fz = np.array([cx + rng.uniform(-0.35, 0.35), cy + rng.uniform(-0.85, 0.85), 0.0])
                p_dsh = np.array([cx + rng.uniform(-0.35, 0.35), cy + rng.uniform(-0.85, 0.85), 0.0])
                p_vg = np.array([cx + rng.uniform(-0.35, 0.35), cy + rng.uniform(-0.85, 0.85), 0.0])
                p_pk = np.array([cx + rng.uniform(-0.35, 0.35), cy + rng.uniform(-0.85, 0.85), 0.0])
                fz_dots.add(Dot(p_fz, radius=0.085, color=FRIZZLED_COL))
                dsh_dots.add(Dot(p_dsh, radius=0.080, color=DSH_COL))
                vg_dots.add(Dot(p_vg, radius=0.085, color=VANGL_COL))
                pk_dots.add(Dot(p_pk, radius=0.080, color=PRICKLE_COL))

                fz_targets.append(np.array([rx_in + 0.05, cy + ys[k], 0.0]))
                dsh_targets.append(np.array([rx_in - 0.14, cy + ys[k], 0.0]))
                vg_targets.append(np.array([lx_in - 0.05, cy + ys[k], 0.0]))
                pk_targets.append(np.array([lx_in + 0.14, cy + ys[k], 0.0]))

        self.play(FadeOut(prev_sheet, scale=1.25), run_time=0.6)
        self.play(
            FadeIn(row_group, scale=0.9), FadeIn(head), FadeIn(tag),
            FadeIn(fz_dots), FadeIn(dsh_dots), FadeIn(vg_dots), FadeIn(pk_dots),
            run_time=2.0,
        )

        self.play(
            *[d.animate.shift([rng.uniform(-0.10, 0.10), rng.uniform(-0.10, 0.10), 0])
              for grp in (fz_dots, dsh_dots, vg_dots, pk_dots) for d in grp],
            run_time=2.8,
        )

        self.at("Teal")
        fz_bars = VGroup(*[
            Line([c["right_x"] - 0.04, c["center"][1] - c["edge_y"], 0],
                 [c["right_x"] - 0.04, c["center"][1] + c["edge_y"], 0],
                 color=FRIZZLED_COL, stroke_width=7.5)
            for c in cells
        ])
        fz_lbl = dark_chip("Frizzled", FRIZZLED_COL, size=26).move_to([2.4, 2.55, 0])
        dsh_lbl = dark_chip("Dishevelled", DSH_COL, size=26).move_to([4.8, 2.55, 0])
        tip_side_lbl = T("Tip-side edge →", 26, FRIZZLED_COL).move_to([3.5, -2.55, 0])
        self.play(
            *[d.animate.move_to(t) for d, t in zip(fz_dots, fz_targets)],
            *[d.animate.move_to(t) for d, t in zip(dsh_dots, dsh_targets)],
            Create(fz_bars),
            FadeIn(fz_lbl), FadeIn(dsh_lbl), FadeIn(tip_side_lbl),
            run_time=5.0,
        )

        self.at("On the opposite")
        vg_bars = VGroup(*[
            Line([c["left_x"] + 0.04, c["center"][1] - c["edge_y"], 0],
                 [c["left_x"] + 0.04, c["center"][1] + c["edge_y"], 0],
                 color=VANGL_COL, stroke_width=7.5)
            for c in cells
        ])
        vg_lbl = dark_chip("Van Gogh", VANGL_COL, size=26).move_to([-4.6, 2.55, 0])
        pk_lbl = dark_chip("Prickle", PRICKLE_COL, size=26).move_to([-2.3, 2.55, 0])
        body_side_lbl = T("← Body-side edge", 26, VANGL_COL).move_to([-3.5, -2.55, 0])
        self.play(
            *[d.animate.move_to(t) for d, t in zip(vg_dots, vg_targets)],
            *[d.animate.move_to(t) for d, t in zip(pk_dots, pk_targets)],
            Create(vg_bars),
            FadeIn(vg_lbl), FadeIn(pk_lbl), FadeIn(body_side_lbl),
            run_time=5.0,
        )

        self.at("Each cell builds")
        two_sides = T("Two distinct sides per cell", 28, TEXT).move_to([0.0, -3.15, 0])
        self.play(FadeIn(two_sides, shift=UP * 0.08),
                  *[Indicate(b, color=WNT_COL, scale_factor=1.08) for b in (fz_bars[2], vg_bars[2])],
                  run_time=2.2)
        self.finish()


class S06FlamingoHair(SpokenScene):
    def construct(self):
        row_group, cells, fz_bars, vg_bars, dots = build_sorted_six_cells_state()
        tag = scope_tag("schematic")
        self.add(row_group, fz_bars, vg_bars, dots, tag)

        border_xs = [(cells[i]["right_x"] + cells[i + 1]["left_x"]) / 2.0 for i in range(5)]
        # Indicate the 5 shared borders during the opening phrase
        border_marks = VGroup(*[
            DashedLine([bx, -1.0, 0], [bx, 0.9, 0], color=FLAMINGO_COL, stroke_width=2.5)
            for bx in border_xs
        ])
        self.play(LaggedStart(*[Create(m) for m in border_marks], lag_ratio=0.12), run_time=1.7)

        self.at("silver flamingo")
        bridges = VGroup()
        for i in range(5):
            x_l = cells[i]["right_x"] - 0.02
            x_r = cells[i + 1]["left_x"] + 0.02
            cy = cells[i]["center"][1]
            for y_off in np.linspace(-cells[i]["edge_y"] * 0.72, cells[i]["edge_y"] * 0.72, 4):
                bridges.add(Line([x_l, cy + y_off, 0], [x_r, cy + y_off, 0],
                                 color=FLAMINGO_COL, stroke_width=6.0))
        flam_lbl = dark_chip("Flamingo bridges", FLAMINGO_COL, size=24).move_to([0.0, 3.30, 0])
        self.play(FadeOut(border_marks, run_time=0.25))
        self.play(LaggedStart(*[Create(b) for b in bridges], lag_ratio=0.04),
                  FadeIn(flam_lbl), run_time=0.75)

        self.at("One cell's frizzled")
        spot_box = RoundedRectangle(
            corner_radius=0.14, width=0.82, height=2.25,
            stroke_color=WNT_COL, stroke_width=4.0, fill_opacity=0.0
        ).move_to([border_xs[2], -0.05, 0])
        fz_face = dark_chip("Frizzled edge", FRIZZLED_COL, size=26).move_to([-2.4, -2.85, 0])
        vs_txt = T("faces", 26, TEXT).move_to([0.0, -2.85, 0])
        vg_face = dark_chip("Van Gogh edge", VANGL_COL, size=26).move_to([2.5, -2.85, 0])
        face_group = VGroup(fz_face, vs_txt, vg_face)

        bridge_labels = VGroup()
        bridge_ticks = VGroup()
        for i, bx in enumerate(border_xs):
            ly = 2.15 if i % 2 == 0 else 2.68
            lbl = T("Frizzled : Van Gogh", 22, FLAMINGO_COL).move_to([bx, ly, 0])
            tick = Line([bx, lbl.get_bottom()[1] - 0.06, 0], [bx, 0.72, 0],
                        color=FLAMINGO_COL, stroke_width=2.0).set_opacity(0.8)
            bridge_labels.add(lbl)
            bridge_ticks.add(tick)

        self.play(
            Create(spot_box),
            FadeIn(face_group),
            LaggedStart(*[FadeIn(l, shift=DOWN * 0.05) for l in bridge_labels], lag_ratio=0.08),
            LaggedStart(*[Create(tk) for tk in bridge_ticks], lag_ratio=0.08),
            run_time=1.8,
        )
        self.play(fz_bars[2].animate.set_stroke(width=12.0),
                  vg_bars[3].animate.set_stroke(width=12.0), run_time=1.2)
        self.play(fz_bars[2].animate.set_stroke(width=7.5),
                  vg_bars[3].animate.set_stroke(width=7.5), run_time=0.8)

        self.at("Each cell grows")
        grow = ValueTracker(0.02)

        def make_all_hairs():
            t = grow.get_value()
            g = VGroup()
            for c in cells:
                origin = np.array([c["right_x"] - 0.04, c["center"][1], 0.0])
                g.add(make_wing_hair(origin, length=1.15 * t, angle=0.0, color=HAIR_COL, base_w=0.22))
            return g

        live_hairs = always_redraw(make_all_hairs)
        actin_lbl = dark_chip("Actin hairs at Frizzled edge", HAIR_COL, size=26).move_to([0.0, -2.85, 0])
        self.play(FadeOut(spot_box, run_time=0.25), swap(face_group, actin_lbl, run_time=0.55))
        self.add(live_hairs)
        self.play(grow.animate.set_value(1.0), run_time=4.2)
        self.finish()


class S07NoBetaCatenin(SpokenScene):
    def construct(self):
        row_group, cells, fz_bars, vg_bars, dots = build_sorted_six_cells_state()
        bridges = VGroup()
        for i in range(5):
            x_l = cells[i]["right_x"] - 0.02
            x_r = cells[i + 1]["left_x"] + 0.02
            cy = cells[i]["center"][1]
            for y_off in np.linspace(-cells[i]["edge_y"] * 0.72, cells[i]["edge_y"] * 0.72, 4):
                bridges.add(Line([x_l, cy + y_off, 0], [x_r, cy + y_off, 0],
                                 color=FLAMINGO_COL, stroke_width=6.0))
        hairs = VGroup(*[
            make_wing_hair(np.array([c["right_x"] - 0.04, c["center"][1], 0.0]),
                           length=1.15, angle=0.0, color=HAIR_COL, base_w=0.22)
            for c in cells
        ])
        tag = scope_tag("schematic")
        self.add(row_group, fz_bars, vg_bars, dots, bridges, hairs, tag)

        # Quiet nuclei + silent gene lines appear inside every cell
        nuclei = VGroup(*[
            DashedVMobject(Circle(radius=0.34, color=CELL_EDGE, stroke_width=2.4), num_dashes=14)
            .move_to(c["center"] + LEFT * 0.05).set_opacity(0.65)
            for c in cells
        ])
        self.play(LaggedStart(*[Create(n) for n in nuclei], lag_ratio=0.12), run_time=3.5)

        self.at("Planar polarity in")
        no_bcat = dark_chip("× No β-catenin", MISDIR_COL, size=28).move_to([-2.3, 2.75, 0])
        no_tcf = dark_chip("× No TCF", MISDIR_COL, size=28).move_to([1.9, 2.75, 0])
        nuc_lbl = T("Nucleus stays quiet", 28, TEXT).move_to([-0.4, -2.75, 0])
        # Pulse bright Frizzled-vs-Van Gogh edges & actin hairs cleanly as visual note requests
        for b in fz_bars:
            pulse(b, base=8.5, amp=3.0, speed=3.2)
        for b in vg_bars:
            pulse(b, base=8.5, amp=3.0, speed=3.2)
        self.play(FadeIn(no_bcat), FadeIn(nuc_lbl), run_time=2.0)
        self.play(FadeIn(no_tcf), nuclei.animate.set_opacity(0.28), run_time=3.2)

        self.at("Instead of switching")
        self.play(
            nuclei.animate.set_opacity(0.16),
            *[h.animate.stretch(1.06, 0, about_point=h.get_left()) for h in hairs],
            run_time=2.4,
        )

        self.at("frizzled and")
        edge_lbl = dark_chip("Frizzled + Dishevelled place the hair", FRIZZLED_COL, size=28).move_to([-0.2, -2.75, 0])
        self.play(swap(nuc_lbl, edge_lbl, run_time=0.65))
        self.play(
            *[h.animate.stretch(1.0 / 1.06, 0, about_point=h.get_left()) for h in hairs],
            run_time=3.0,
        )
        self.finish()


class S08VertebrateNeural(SpokenScene):
    def construct(self):
        row_group, cells, fz_bars, vg_bars, dots = build_sorted_six_cells_state()
        self.add(row_group, fz_bars, vg_bars, dots)

        p = ValueTracker(0.0)
        plate_center = np.array([0.0, 0.0, 0.0])
        plate_wide = render_neural_plate(0.0, center=plate_center, scale_x=0.95, scale_y=0.74,
                                         polarity_mode="none", fold_close=False)
        head = T("Vertebrate neural plate", 34, TEXT).move_to([0.0, 3.25, 0])
        mid_lbl = T("Midline", 26, "#CBD5E1").move_to([0.0, 2.65, 0])
        tag = scope_tag("schematic")

        self.play(FadeOut(VGroup(row_group, fz_bars, vg_bars, dots), scale=0.75), run_time=0.6)
        self.play(FadeIn(plate_wide, scale=1.08), FadeIn(head), FadeIn(tag), run_time=2.8)

        self.at("The future brain")
        self.play(FadeIn(mid_lbl, shift=DOWN * 0.08), plate_wide[0].animate.set_stroke("#CBD5E1", width=3.5),
                  run_time=3.8)
        self.play(plate_wide[0].animate.set_stroke(CELL_EDGE, width=2.5), run_time=1.0)

        self.at("Guided by polarity")
        rng = np.random.default_rng(19)
        wnt_dots = VGroup()
        wnt_targets = []
        for _ in range(10):
            sx = rng.choice([-5.4, 5.4])
            sy = rng.uniform(-1.5, 1.4)
            tx = rng.uniform(-3.6, 3.6)
            ty = rng.uniform(-1.0, 1.0)
            wnt_dots.add(Dot([sx, sy, 0.0], radius=0.09, color=WNT_COL))
            wnt_targets.append(np.array([tx, ty, 0.0]))
        wnt_dots.set_z_index(10)
        wnt_lbl = dark_chip("Wnt signals", WNT_COL, size=26).move_to([-4.6, 2.65, 0])
        self.play(FadeIn(wnt_lbl), FadeIn(wnt_dots),
                  *[d.animate.move_to(t) for d, t in zip(wnt_dots, wnt_targets)],
                  run_time=2.8)

        self.at("identify which edge")
        plate_pol = render_neural_plate(0.0, center=plate_center, scale_x=0.95, scale_y=0.74,
                                        polarity_mode="normal", fold_close=True)
        fz_legend = dark_chip("Frizzled → midline", FRIZZLED_COL, size=24).move_to([4.15, 2.65, 0])
        self.play(FadeOut(plate_wide, run_time=0.35), FadeIn(plate_pol, run_time=0.55), FadeIn(fz_legend), run_time=2.8)
        self.bring_to_front(wnt_dots)

        self.at("They squeeze between")
        self.remove(plate_pol)
        live_plate = always_redraw(lambda: render_neural_plate(
            p.get_value(), center=plate_center, scale_x=0.95, scale_y=0.74,
            polarity_mode="normal", fold_close=True, show_wnt=False
        ))
        tube_lbl = T("Narrowed & folded into neural tube", 28, HAIR_COL).move_to([-0.4, -3.05, 0])
        self.add(live_plate)
        self.bring_to_front(wnt_dots)
        self.play(
            p.animate.set_value(1.0),
            *[d.animate.move_to([t[0] * 0.44, t[1] * 1.45, 0.0]) for d, t in zip(wnt_dots, wnt_targets)],
            FadeOut(head, run_time=0.4),
            FadeIn(tube_lbl, shift=UP * 0.08),
            run_time=4.4,
        )
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        p = ValueTracker(1.0)
        center = np.array([0.0, 0.15, 0.0])
        live_plate = always_redraw(lambda: render_neural_plate(
            p.get_value(), center=center, scale_x=0.95, scale_y=0.74,
            polarity_mode="normal", fold_close=True
        ))
        mid_lbl = T("Midline", 26, "#CBD5E1").move_to([0.0, 2.72, 0])
        tag = scope_tag("schematic").move_to([5.6, 3.3, 0])
        self.add(live_plate, mid_lbl, tag)

        self.play(p.animate.set_value(0.0), run_time=2.6)

        self.at("Suppose these cells")
        self.remove(live_plate)
        plate_norm = render_neural_plate(0.0, center=center, scale_x=0.95, scale_y=0.74,
                                         polarity_mode="normal", fold_close=True)
        plate_grey = render_neural_plate(0.0, center=center, scale_x=0.95, scale_y=0.74,
                                         polarity_mode="grey", fold_close=True)
        self.add(plate_norm)
        no_dir = dark_chip("No midline polarity", CELL_EDGE, text_color=TEXT, size=26).move_to([-4.2, 2.72, 0])
        self.play(FadeOut(plate_norm, run_time=0.4), FadeIn(plate_grey, run_time=0.5), FadeIn(no_dir), run_time=3.2)

        self.at("What would happen")
        q = question_card("Cells cannot find the midline: plate width? Do the folds meet?",
                          y=-3.0, size=28, max_w=10.5)
        self.play(FadeIn(q.question, shift=UP * 0.08), run_time=2.2)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Cells cannot find the midline: plate width? Do the folds meet?"
    CARD = {"y": -3.0, "size": 28, "max_w": 10.5}
    SECONDS = 4.5

    def backdrop(self):
        center = np.array([0.0, 0.15, 0.0])
        plate_grey = render_neural_plate(0.0, center=center, scale_x=0.95, scale_y=0.74,
                                         polarity_mode="grey", fold_close=True)
        mid_lbl = T("Midline", 26, "#CBD5E1").move_to([0.0, 2.72, 0])
        no_dir = dark_chip("No midline polarity", CELL_EDGE, text_color=TEXT, size=26).move_to([-4.2, 2.72, 0])
        tag = scope_tag("schematic").move_to([5.6, 3.3, 0])
        return VGroup(plate_grey, mid_lbl, no_dir, tag)


class S11NeuralDefects(SpokenScene):
    def construct(self):
        tp = TwoPanel("Normal PCP", "Disrupted PCP: open tube",
                      colors=(FRIZZLED_COL, MISDIR_COL), top=3.20, bottom=-2.35, gap=0.45, width=12.6, size=30)
        tag = scope_tag("schematic").move_to([5.6, 3.45, 0])
        left_c = tp.area("left")[0] + UP * 0.08
        right_c = tp.area("right")[0] + UP * 0.08

        rng = np.random.default_rng(11)
        rand_angles = [float(rng.uniform(-np.pi, np.pi)) for _ in range(32)]

        p_left = ValueTracker(0.0)
        p_right = ValueTracker(0.0)

        left_plate = always_redraw(lambda: render_neural_plate(
            p_left.get_value(), center=left_c, scale_x=0.54, scale_y=0.50,
            polarity_mode="normal", fold_close=True
        ))
        right_plate = always_redraw(lambda: render_neural_plate(
            p_right.get_value(), center=right_c, scale_x=0.54, scale_y=0.50,
            polarity_mode="scrambled", fold_close=True, random_angles=rand_angles
        ))

        self.play(FadeIn(tp), FadeIn(tag), FadeIn(left_plate), FadeIn(right_plate), run_time=1.8)

        self.at("cells lose their")
        self.play(
            p_left.animate.set_value(1.0),
            p_right.animate.set_value(0.10),
            run_time=5.4,
        )

        self.at("Disrupting these genes")
        _, hw_r, hh_r = neural_plate_geometry(0.10, center=right_c, scale_x=0.54, scale_y=0.50)
        fold_in_r = 0.10 * (hw_r - 0.14 * 0.54)
        gap_brace = DoubleArrow(
            [right_c[0] - hw_r + fold_in_r + 0.1, right_c[1] - hh_r - 0.36, 0],
            [right_c[0] + hw_r - fold_in_r - 0.1, right_c[1] - hh_r - 0.36, 0],
            buff=0, color=MISDIR_COL, stroke_width=4.0, tip_length=0.16
        )
        open_lbl = T("Stays wide & open", 26, MISDIR_COL).move_to([right_c[0], -1.85, 0])
        closed_lbl = T("Closes cleanly", 26, HAIR_COL).move_to([left_c[0], -1.85, 0])
        self.play(GrowFromCenter(gap_brace), FadeIn(open_lbl), FadeIn(closed_lbl),
                  p_right.animate.set_value(0.05), run_time=3.4)

        self.at("including spina")
        spina_chip = dark_chip("e.g. spina bifida", MISDIR_COL, size=26).move_to([right_c[0], right_c[1] + hh_r + 0.55, 0])
        self.play(FadeIn(spina_chip, shift=DOWN * 0.08), p_right.animate.set_value(0.11), run_time=2.5)

        self.at("Whether aligning wing")
        cap = caption("Neighbours sort Frizzled to one edge so the sheet agrees.", size=28, color=TEXT, y=-3.05)
        self.play(FadeIn(cap, shift=UP * 0.08), p_right.animate.set_value(0.06),
                  tp.left_frame.animate.set_stroke(width=4.5), run_time=2.8)

        self.at("neighbors sort frizzled")
        self.play(tp.left_frame.animate.set_stroke(width=2.5),
                  spina_chip[0].animate.set_stroke(width=4.5),
                  run_time=2.6)
        self.finish()


class S12End(EndCard):
    LINE = "Planar polarity aligns cells as neighbours sort Frizzled to one edge."
