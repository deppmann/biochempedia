"""
FILM: Right-Side Out: How Vesicles Form and Signal
LESSON: Exosomes and Extracellular Vesicles: Signals Between Cells

COLOUR MAP (one colour per concept for the entire film):
  MEMBRANE = "#F5C542"  (warm-gold: plasma membrane & vesicle lipid bilayer)
  CYTOSOL  = "#38BDF8"  (cool-cyan: cell cytosol & sealed internal cargo)
  LIGAND   = "#FB7185"  (coral: outward-facing membrane protein / MHC class II / receptor head)
  LUMEN    = "#475569"  (slate-blue: endosome / MVB lumen fluid, trapped outside fluid)
  MATCH    = "#34D399"  (emerald-green: matching T-cell receptor & active target signaling)
  SILENT   = "#A78BFA"  (muted-violet: non-matching receptor & lysosome degradation sink)
  TEXT     = "#E8EAF0"  (crisp white-slate text)
  BG       = "#0f1117"  (dark slate extracellular backdrop)

ONE WORLD CARRIED:
  Left: donor B cell (warm-gold membrane, cyan cytosol, coral surface ligands/receptors).
  Middle: dark extracellular gap.
  Right: target T cells (top matching emerald receptor, bottom non-matching violet receptor).
  We zoom into the donor membrane (endocytosis -> inward bud -> MVB -> two exits -> microvesicle),
  then pan right across the gap to the target cell membrane (three action lanes).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s01_hook:            A coral-studded vesicle buds from the donor B cell and traverses the gap via a
                       smooth trajectory tracker t_v while highlighting the matching vs non-matching
                       target receptors and tracing an internal-origin question path.
  s02_bcell:           Three peptide-loaded MHC class II vesicles bud and drift across the gap along
                       computed paths (tracker p); the upper docks into the matching emerald receptor,
                       triggering an expanding emerald signaling wave, while the lower rebounds off
                       the non-matching violet receptor.
  s03_endocytosis:     Camera zooms onto the donor plasma membrane (tracker z 0->1), then a
                       continuous deformation tracker p (0->1) dimples the gold membrane inward into
                       cyan cytosol, encloses slate-blue outside fluid, pinches shut into an endosome,
                       and carries it inward with the coral receptor head pointing into the lumen.
  s04_predict_q:       Zoomed endosome expands to fill the frame; continuous budding tracker b (0->0.78)
                       pushes a gold rim patch inward into the slate-blue lumen while cyan cytosol
                       droplets stream into the growing bud, holding mid-pinch with two '?' markers.
  s06_reveal:          Tracker b completes the pinch-off (0.78->1.0), turning '?' into 'Ligands face out'
                       and 'Cytosol sealed inside'; four more vesicles pinch off sequentially from around
                       the rim and follow deterministic non-overlapping paths inside the MVB lumen.
  s07_two_doors:       Two MVB trajectories branch from the sorting room: an upper copy glides to the
                       violet lysosome and fragments into vanishing pieces; the main MVB glides to the
                       plasma membrane, opens a computed fusion pore, and spills intact exosomes out.
  s08_microvesicles:   An outward budding tracker m (0->1) bulges a patch of donor plasma membrane
                       straight outward into the gap, pinching off a microvesicle that drifts side by
                       side with an exosome across the gap to show identical orientation and size.
  s09_three_ways:      Camera pans right onto the target cell membrane divided into 3 lanes: Lane 1
                       docks a vesicle onto an emerald receptor and propagates an inward signaling
                       cascade; Lane 2 merges a vesicle bilayer into the membrane and spills cargo.
  s10_uptake_and_rule: Lane 3 wraps the target membrane around a vesicle (endocytic tracker e 0->1),
                       carries the endosome to a violet lysosome, traces a rare dashed escape dot, and
                       highlights outward coral ligands (contact) vs sealed cyan cargo across Lanes 1-3.
"""

from bp_parts import *

# ------------------------------------------------------------------ Colour Map
MEMBRANE = "#F5C542"
CYTOSOL = "#38BDF8"
LIGAND = "#FB7185"
LUMEN = "#475569"
MATCH = "#34D399"
SILENT = "#A78BFA"


# ------------------------------------------------------------------ Shared Geometry Builders
def _unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0.0])


def make_ligand(pos, angle=0.0, color=LIGAND, peptide=False, tail=False, scale=1.0):
    """Coral outward-facing membrane protein / MHC class II cup + optional white peptide bar."""
    u = _unit(angle)
    n = np.array([-u[1], u[0], 0.0])
    g = VGroup()
    if tail:
        stalk_in = Line(pos - u * 0.24 * scale, pos, color=color, stroke_width=4.0 * scale)
        g.add(stalk_in)
    stem = Line(pos, pos + u * 0.16 * scale, color=color, stroke_width=4.5 * scale)
    head_c = pos + u * 0.26 * scale
    if peptide:
        cup = Arc(
            radius=0.11 * scale,
            start_angle=angle - PI * 0.55,
            angle=PI * 1.1,
            arc_center=head_c - u * 0.03 * scale,
            color=color,
            stroke_width=4.5 * scale,
        )
        pep = Line(
            head_c - n * 0.065 * scale + u * 0.03 * scale,
            head_c + n * 0.065 * scale + u * 0.03 * scale,
            color=TEXT,
            stroke_width=4.0 * scale,
        )
        g.add(stem, cup, pep)
    else:
        head = Dot(head_c, radius=0.085 * scale, color=color)
        g.add(stem, head)
    return g


def make_target_receptor(pos, angle=PI, match=True, scale=1.0):
    """Target T-cell receptor: emerald matching cup or muted-violet mismatched fork."""
    u = _unit(angle)
    n = np.array([-u[1], u[0], 0.0])
    col = MATCH if match else SILENT
    stem = Line(pos, pos + u * 0.22 * scale, color=col, stroke_width=5.0 * scale)
    tip = pos + u * 0.26 * scale
    if match:
        cup = Arc(
            radius=0.14 * scale,
            start_angle=angle - PI * 0.48,
            angle=PI * 0.96,
            arc_center=tip + u * 0.08 * scale,
            color=col,
            stroke_width=5.0 * scale,
        )
        return VGroup(stem, cup)
    fork = VGroup(
        Line(tip, tip + u * 0.12 * scale + n * 0.14 * scale, color=col, stroke_width=4.5 * scale),
        Line(tip, tip + u * 0.12 * scale - n * 0.14 * scale, color=col, stroke_width=4.5 * scale),
    )
    return VGroup(stem, fork)


def make_vesicle(center, radius=0.38, n_ligands=6, peptide=False, cargo_dots=3, seed=7, angle_offset=0.25, scale_lig=0.78):
    """Gold-ringed vesicle enclosing cyan cytosol + cargo dots, with outward coral ligands."""
    c = np.array(center, dtype=float)
    ring = Circle(
        radius=radius,
        stroke_color=MEMBRANE,
        stroke_width=max(2.0, 4.5 * min(1.0, radius / 0.30)),
        fill_color=CYTOSOL,
        fill_opacity=0.22,
    ).move_to(c)
    g = VGroup(ring)
    rng = np.random.default_rng(seed)
    for _ in range(cargo_dots):
        r = rng.uniform(0.12 * radius, 0.52 * radius)
        th = rng.uniform(0, TAU)
        d = Dot(c + np.array([r * np.cos(th), r * np.sin(th), 0.0]), radius=max(0.015, 0.045 * (radius / 0.38)), color=CYTOSOL)
        g.add(d)
    for k in range(n_ligands):
        th = angle_offset + k * TAU / n_ligands
        p = c + radius * _unit(th)
        g.add(make_ligand(p, angle=th, color=LIGAND, peptide=peptide, scale=scale_lig))
    return g


def make_donor_cell_left(edge_x=-3.2, y_span=3.6, peptide=False, n_lig=7):
    """Curved right edge of the donor B cell filling the left side of the frame."""
    ys = np.linspace(-y_span, y_span, 56)
    xs = edge_x - 0.14 * (ys ** 2)
    pts = [np.array([-7.15, -y_span, 0.0])]
    for x, y in zip(xs, ys):
        pts.append(np.array([x, y, 0.0]))
    pts.append(np.array([-7.15, y_span, 0.0]))
    fill = Polygon(*pts, stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.16)
    mem_pts = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
    membrane = VMobject(stroke_color=MEMBRANE, stroke_width=6.5, fill_opacity=0)
    membrane.set_points_smoothly(mem_pts)
    ligs = VGroup()
    for y in np.linspace(-2.5, 2.5, n_lig):
        x = edge_x - 0.14 * (y ** 2)
        dx_dy = -0.28 * y
        ang = np.arctan2(-dx_dy, 1.0)
        ligs.add(make_ligand(np.array([x, y, 0.0]), angle=ang, peptide=peptide, scale=0.85))
    return VGroup(fill, membrane, ligs)


def make_target_cell_right(center_y=1.55, match=True, x_edge=3.35, half_h=1.35):
    """Curved left edge of a target T cell on the right side of the frame."""
    ys = np.linspace(center_y - half_h, center_y + half_h, 40)
    dy = ys - center_y
    xs = x_edge + 0.18 * (dy ** 2)
    pts = [np.array([7.15, center_y - half_h, 0.0])]
    for x, y in zip(xs, ys):
        pts.append(np.array([x, y, 0.0]))
    pts.append(np.array([7.15, center_y + half_h, 0.0]))
    fill_col = MATCH if match else SILENT
    fill = Polygon(*pts, stroke_width=0, fill_color=fill_col, fill_opacity=0.12)
    mem_pts = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
    membrane = VMobject(stroke_color=MEMBRANE, stroke_width=6.0, fill_opacity=0)
    membrane.set_points_smoothly(mem_pts)
    recs = VGroup()
    for y_off in (-0.65, 0.0, 0.65):
        y = center_y + y_off
        x = x_edge + 0.18 * (y_off ** 2)
        ang = PI + np.arctan2(-0.36 * y_off, 1.0)
        recs.add(make_target_receptor(np.array([x, y, 0.0]), angle=ang, match=match, scale=0.95))
    return VGroup(fill, membrane, recs)


def make_mvb(center, radius=1.05, n_ves=5, seed=7, ves_r=0.23):
    """Multivesicular body: gold outer rim, slate-blue lumen, packed small coral-studded vesicles."""
    c = np.array(center, dtype=float)
    outer = Circle(
        radius=radius,
        stroke_color=MEMBRANE,
        stroke_width=5.5,
        fill_color=LUMEN,
        fill_opacity=0.45,
    ).move_to(c)
    g = VGroup(outer)
    angles = np.linspace(0.3, TAU + 0.3, n_ves, endpoint=False)
    offsets = [c + (radius * 0.48 if k % 2 == 0 else radius * 0.38) * _unit(a) for k, a in enumerate(angles)]
    if n_ves == 5:
        offsets[0] = c + np.array([0.0, 0.0, 0.0])
        for k in range(1, 5):
            a = 0.45 + (k - 1) * TAU / 4.0
            offsets[k] = c + radius * 0.52 * _unit(a)
    for k, off in enumerate(offsets):
        g.add(make_vesicle(off, radius=ves_r, n_ligands=4, cargo_dots=2, seed=seed + k, angle_offset=0.2 * k, scale_lig=0.52))
    return g


def make_signal_waves(origin, phase, color=MATCH, max_r=1.25):
    """Propagating intracellular signaling arcs inside a target cell driven by continuous phase."""
    g = VGroup()
    for k in range(3):
        f = (phase + k / 3.0) % 1.0
        r = 0.22 + max_r * f
        op = 0.90 * (1.0 - f)
        g.add(
            Arc(
                radius=r,
                start_angle=-PI * 0.35,
                angle=PI * 0.70,
                arc_center=origin,
                color=color,
                stroke_width=5.5,
            ).set_stroke(opacity=op)
        )
    return g


# ------------------------------------------------------------------ Parametric Endocytosis & Budding Geometry
def _endocytosis_geometry(p, drift=0.0, zoom=1.0, rec_pulse=0.0):
    """Compute plasma membrane, lumen pocket, and receptor pose from endocytosis progress p in [0, 1]."""
    x_mem = 1.6 + 1.4 * (1.0 - zoom)
    y_top, y_bot = 3.55, -3.55
    ys = np.linspace(y_bot, y_top, 120)
    cyto_rect = Polygon(
        [-7.15, y_bot, 0], [x_mem, y_bot, 0], [x_mem, y_top, 0], [-7.15, y_top, 0],
        stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.18,
    )
    g = VGroup(cyto_rect)

    if p < 0.72:
        u = p / 0.72
        depth = 3.8 * np.sin(u * PI / 2)
        if u > 0.35:
            t_n = (u - 0.35) / 0.65
            pts = []
            phi_0 = 0.28 * (1.0 - 0.75 * t_n)
            cx = x_mem - 2.3 * (0.4 + 0.6 * t_n)
            rx = 1.65 * (0.5 + 0.5 * t_n)
            ry = 1.55 * (0.65 + 0.35 * t_n)
            bx0 = min(x_mem, cx + rx * np.cos(phi_0))
            by0 = ry * np.sin(phi_0)
            y_mem_neck = by0 + 0.55 * (1.0 - 0.55 * t_n)

            for y in np.linspace(y_top, y_mem_neck, 24)[:-1]:
                pts.append(np.array([x_mem, y, 0.0]))

            p0_top = np.array([x_mem, y_mem_neck, 0.0])
            p1_top = np.array([x_mem, by0, 0.0])
            t_bulb = np.array([-rx * np.sin(phi_0), ry * np.cos(phi_0), 0.0])
            k_tan = min(0.55 * by0 / max(1e-6, abs(t_bulb[1])), 0.40 * max(0.02, x_mem - bx0) / max(1e-6, abs(t_bulb[0])))
            bulb_top = np.array([bx0, by0, 0.0])
            p2_top = bulb_top - k_tan * t_bulb
            for s in np.linspace(0.0, 1.0, 16)[:-1]:
                pts.append(((1 - s) ** 3) * p0_top + 3 * ((1 - s) ** 2) * s * p1_top + 3 * (1 - s) * (s ** 2) * p2_top + (s ** 3) * bulb_top)

            phis = np.linspace(phi_0, TAU - phi_0, 80)
            for ph in phis:
                bx = min(x_mem, cx + rx * np.cos(ph))
                by = ry * np.sin(ph)
                pts.append(np.array([bx, by, 0.0]))

            bulb_bot = np.array([bx0, -by0, 0.0])
            p1_bot = np.array([p2_top[0], -p2_top[1], 0.0])
            p2_bot = np.array([x_mem, -by0, 0.0])
            p3_bot = np.array([x_mem, -y_mem_neck, 0.0])
            for s in np.linspace(0.0, 1.0, 16)[1:]:
                pts.append(((1 - s) ** 3) * bulb_bot + 3 * ((1 - s) ** 2) * s * p1_bot + 3 * (1 - s) * (s ** 2) * p2_bot + (s ** 3) * p3_bot)

            for y in np.linspace(-y_mem_neck, y_bot, 24)[1:]:
                pts.append(np.array([x_mem, y, 0.0]))
            mem_pts = pts
        else:
            xs = [x_mem - depth * np.exp(-((y / 1.15) ** 2)) for y in ys]
            mem_pts = [np.array([x, y, 0.0]) for x, y in zip(reversed(xs), reversed(ys))]

        poly_pts = [np.array([7.15, y_top, 0.0])] + mem_pts + [np.array([7.15, y_bot, 0.0])]
        out_cut = Polygon(*poly_pts, stroke_width=0, fill_color=BG, fill_opacity=1.0)
        g.add(out_cut)
        if u > 0.10:
            pocket_pts = [pt for pt in mem_pts if pt[0] < x_mem - 0.04]
            if len(pocket_pts) >= 3:
                lumen_poly = Polygon(*pocket_pts, stroke_width=0, fill_color=LUMEN, fill_opacity=0.38 * min(1.0, (u - 0.10) / 0.45))
                g.add(lumen_poly)
        mem = VMobject(stroke_color=MEMBRANE, stroke_width=6.5, fill_opacity=0)
        mem.set_points_smoothly(mem_pts)
        g.add(mem)

        deepest = min(mem_pts, key=lambda pt: pt[0] + 0.05 * abs(pt[1]))
        rec_scale = (1.15 + 0.20 * zoom) * (1.0 + 0.08 * np.sin(rec_pulse * TAU))
        g.add(make_ligand(deepest, angle=0.0, color=LIGAND, tail=True, scale=rec_scale))
        return g, np.array(deepest), False

    w = (p - 0.72) / 0.28
    pm = Line([x_mem, y_bot, 0], [x_mem, y_top, 0], color=MEMBRANE, stroke_width=6.5)
    dark_out = Polygon([x_mem, y_bot, 0], [7.15, y_bot, 0], [7.15, y_top, 0], [x_mem, y_top, 0],
                       stroke_width=0, fill_color=BG, fill_opacity=1.0)
    exo_c = np.array([-0.55 - 1.35 * w - 0.65 * drift, 0.0, 0.0])
    exo_r = 1.65 + 0.18 * w
    endo = Circle(radius=exo_r, stroke_color=MEMBRANE, stroke_width=6.5, fill_color=LUMEN, fill_opacity=0.42).move_to(exo_c)
    g.add(dark_out, pm, endo)
    rec_pos = exo_c + np.array([-exo_r, 0.0, 0.0])
    g.add(make_ligand(rec_pos, angle=0.0, color=LIGAND, tail=True, scale=1.35))
    return g, rec_pos, True


def _inward_bud_geometry(b, center=np.array([-0.15, -0.15, 0.0]), R=2.45, drift_x=0.0, flow=0.0):
    """Zoomed endosome surrounded by cyan cytosol, with a rounded inward bud at the right rim (theta=0)
    driven by b in [0, 1].
    """
    c = np.array(center, dtype=float)
    cyto_bg = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.16)
    g = VGroup(cyto_bg)

    if b < 0.86:
        u = b / 0.86
        small_depth = 0.58 * max(0.0, (u - 0.18) / 0.82)
        if u <= 0.30:
            bud_depth = 0.95 * (u / 0.30)
            thetas = np.linspace(0.0, TAU, 240, endpoint=False)
            pts = []
            for th in thetas:
                dth = ((th + PI) % TAU) - PI
                dth2 = ((th - 2.15 + PI) % TAU) - PI
                dth3 = ((th - 4.15 + PI) % TAU) - PI
                if u < 0.02:
                    r = R
                else:
                    indent = bud_depth * np.exp(-((dth / 0.42) ** 2))
                    indent += small_depth * np.exp(-((dth2 / 0.24) ** 2))
                    indent += small_depth * np.exp(-((dth3 / 0.24) ** 2))
                    r = R - indent
                pts.append(c + r * _unit(th))
            tip = c + np.array([R - bud_depth, 0.0, 0.0])
            bud_c = tip + np.array([0.43 * min(1.0, u / 0.30), 0.0, 0.0])
        else:
            t_n = (u - 0.30) / 0.70
            theta_neck = 0.42 * (1.0 - 0.76 * t_n)
            bx = R - 0.52 - 0.88 * t_n
            r_bulb = 0.43 + 0.13 * t_n
            bud_c = c + np.array([bx, 0.0, 0.0])
            tip = bud_c - np.array([r_bulb, 0.0, 0.0])
            phi_neck = 1.05 * (1.0 - t_n) + 0.24 * t_n

            pts = []
            for th in np.linspace(theta_neck, TAU - theta_neck, 180):
                dth2 = ((th - 2.15 + PI) % TAU) - PI
                dth3 = ((th - 4.15 + PI) % TAU) - PI
                r = R - small_depth * (np.exp(-((dth2 / 0.24) ** 2)) + np.exp(-((dth3 / 0.24) ** 2)))
                pts.append(c + r * _unit(th))

            rim_bot = c + R * _unit(-theta_neck)
            bulb_bot = bud_c + r_bulb * _unit(-phi_neck)
            p1_bot = np.array([0.65 * rim_bot[0] + 0.35 * bulb_bot[0], 0.30 * rim_bot[1] + 0.70 * bulb_bot[1], 0.0])
            p2_bot = np.array([0.30 * rim_bot[0] + 0.70 * bulb_bot[0], 0.20 * rim_bot[1] + 0.80 * bulb_bot[1], 0.0])
            for s in np.linspace(0.0, 1.0, 14)[1:-1]:
                pts.append(((1 - s) ** 3) * rim_bot + 3 * ((1 - s) ** 2) * s * p1_bot + 3 * (1 - s) * (s ** 2) * p2_bot + (s ** 3) * bulb_bot)

            for ph in np.linspace(TAU - phi_neck, phi_neck, 56):
                pts.append(bud_c + r_bulb * _unit(ph))

            bulb_top = bud_c + r_bulb * _unit(phi_neck)
            rim_top = c + R * _unit(theta_neck)
            p1_top = np.array([0.30 * rim_top[0] + 0.70 * bulb_top[0], 0.20 * rim_top[1] + 0.80 * bulb_top[1], 0.0])
            p2_top = np.array([0.65 * rim_top[0] + 0.35 * bulb_top[0], 0.30 * rim_top[1] + 0.70 * bulb_top[1], 0.0])
            for s in np.linspace(0.0, 1.0, 14)[1:-1]:
                pts.append(((1 - s) ** 3) * bulb_top + 3 * ((1 - s) ** 2) * s * p1_top + 3 * (1 - s) * (s ** 2) * p2_top + (s ** 3) * rim_top)

        lumen = Polygon(*pts, stroke_color=MEMBRANE, stroke_width=6.0, fill_color=LUMEN, fill_opacity=0.45)
        g.add(lumen)
        outer_pt = tip + np.array([-0.52, 0.0, 0.0])
        inner_pt = bud_c
        # Stream cyan cytosol droplets into the growing bud; omit dots near inner_pt once '?' appears
        if u > 0.05:
            x_start = c[0] + R + 0.75
            x_end = bud_c[0] - 0.05
            for k in range(5):
                phase = (flow + k * 0.20) % 1.0
                px = x_start + (x_end - x_start) * phase
                py = c[1] + (k - 2.0) * 0.14 * (1.0 - 0.65 * phase)
                pos = np.array([px, py, 0.0])
                if b >= 0.72 and np.linalg.norm(pos - inner_pt) < 0.44:
                    continue
                g.add(Dot(pos, radius=0.09, color=CYTOSOL))
        if b < 0.22:
            rec_op = 1.0 if b <= 0.12 else (0.22 - b) / 0.10
            lig = make_ligand(tip, angle=PI, color=LIGAND, tail=True, scale=1.15)
            lig.set_stroke(opacity=rec_op).set_fill(opacity=rec_op)
            g.add(lig)
        return g, tip, bud_c, outer_pt, inner_pt

    w = (b - 0.86) / 0.14
    endo = Circle(radius=R, stroke_color=MEMBRANE, stroke_width=6.0, fill_color=LUMEN, fill_opacity=0.45).move_to(c)
    bud_c = c + np.array([R - 1.40 - 0.70 * w - drift_x, 0.0, 0.0])
    bud_r = 0.56
    ves = make_vesicle(bud_c, radius=bud_r, n_ligands=4, cargo_dots=3, seed=7, angle_offset=PI + 0.35 * drift_x, scale_lig=0.95)
    g.add(endo, ves)
    outer_pt = bud_c + np.array([-bud_r - 0.42, 0.0, 0.0])
    inner_pt = bud_c
    return g, bud_c + np.array([-bud_r, 0.0, 0.0]), bud_c, outer_pt, inner_pt


def _microvesicle_bud_geometry(m, x_mem=-1.2, bud_y=1.35):
    """Plasma membrane at x_mem budding straight outward (rightward) into the extracellular gap."""
    y_top, y_bot = 3.55, -3.55
    pts = []
    if m < 0.82:
        u = m / 0.82
        out_depth = 1.85 * np.sin(u * PI / 2)
        ys = np.linspace(y_bot, y_top, 140)
        for y in ys:
            dy = y - bud_y
            sigma = 0.72 - 0.22 * max(0.0, (u - 0.35) / 0.65)
            bulge = out_depth * np.exp(-((dy / sigma) ** 2))
            pts.append(np.array([x_mem + bulge, y, 0.0]))
        poly_pts = [np.array([-7.15, y_bot, 0.0])] + pts + [np.array([-7.15, y_top, 0.0])]
        cyto = Polygon(*poly_pts, stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.18)
        mem = VMobject(stroke_color=MEMBRANE, stroke_width=6.0, fill_opacity=0)
        mem.set_points_smoothly(pts)
        tip = np.array([x_mem + out_depth, bud_y, 0.0])
        lig_top = np.array([x_mem + out_depth * 0.72, bud_y + 0.36, 0.0])
        lig_bot = np.array([x_mem + out_depth * 0.72, bud_y - 0.36, 0.0])
        g = VGroup(
            cyto,
            mem,
            make_ligand(tip, angle=0.0, scale=0.82),
            make_ligand(lig_top, angle=0.45, scale=0.82),
            make_ligand(lig_bot, angle=-0.45, scale=0.82),
        )
        return g, tip
    w = (m - 0.82) / 0.18
    cyto = Polygon(
        [-7.15, y_bot, 0.0], [x_mem, y_bot, 0.0], [x_mem, y_top, 0.0], [-7.15, y_top, 0.0],
        stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.18,
    )
    mem = Line([x_mem, y_bot, 0.0], [x_mem, y_top, 0.0], color=MEMBRANE, stroke_width=6.0)
    ves_c = np.array([x_mem + 1.65 + 2.15 * w, bud_y, 0.0])
    ves = make_vesicle(ves_c, radius=0.44, n_ligands=6, cargo_dots=3, seed=11, angle_offset=0.25 * w, scale_lig=0.82)
    return VGroup(cyto, mem, ves), ves_c


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Exosomes and Extracellular Vesicles: Signals Between Cells"
    TITLE = "Right-Side Out: How Vesicles Form and Signal"


class S01Hook(SpokenScene):
    def construct(self):
        donor = make_donor_cell_left(edge_x=-3.25)
        t_match = make_target_cell_right(center_y=1.45, match=True, x_edge=3.35)
        t_silent = make_target_cell_right(center_y=-1.45, match=False, x_edge=3.35)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(donor, t_match, t_silent, tag)

        t_v = ValueTracker(0.0)
        start_c = np.array([-3.0, 0.0, 0.0])
        mid_c = np.array([0.45, 0.05, 0.0])

        def build_ves():
            u = t_v.get_value()
            pos = start_c + (mid_c - start_c) * u + UP * 0.28 * np.sin(PI * u)
            return make_vesicle(pos, radius=0.44, n_ligands=6, cargo_dots=3, seed=7, angle_offset=0.75 * u, scale_lig=0.85)

        ves = always_redraw(build_ves)
        self.add(ves)

        self.play(t_v.animate.set_value(0.82), run_time=3.4, rate_func=linear)

        self.at("matching target cell")
        q_mark = T("?", size=42, color=TEXT, weight=BOLD).move_to([0.45, 1.15, 0.0])
        sig_t = ValueTracker(0.0)
        sig_wave = always_redraw(lambda: make_signal_waves([3.35, 1.45, 0.0], sig_t.get_value(), color=MATCH, max_r=1.25))
        self.add(sig_wave)
        self.play(t_v.animate.set_value(0.98), sig_t.animate.set_value(0.85), FadeIn(q_mark), run_time=2.5, rate_func=linear)

        self.at("forms inside the sender")
        self.remove(sig_wave)
        inner_ghost = DashedVMobject(Circle(radius=0.52, color=LUMEN, stroke_width=4.0).move_to([-4.95, 0.0, 0.0]), num_dashes=14)
        inner_arrow = CurvedArrow(np.array([-4.35, 0.1, 0.0]), np.array([-0.15, 0.15, 0.0]), angle=-0.35, color=LIGAND, stroke_width=4.0)
        q_out = T("faces out?", size=28, color=LIGAND).move_to([-2.15, 1.65, 0.0])
        self.play(Create(inner_ghost), Create(inner_arrow), FadeIn(q_out), t_v.animate.set_value(1.12), run_time=3.2)
        self.play(t_v.animate.set_value(1.22), run_time=1.8, rate_func=linear)

        self.at("immune case")
        b_lab = T("B cell", size=28, color=CYTOSOL).move_to([-5.35, 2.95, 0.0])
        t_lab = T("Target T cells", size=28, color=MATCH).move_to([4.55, 3.15, 0.0])
        self.play(
            FadeOut(inner_ghost), FadeOut(inner_arrow), FadeOut(q_out), FadeOut(q_mark),
            FadeIn(b_lab), FadeIn(t_lab),
            t_v.animate.set_value(1.45),
            run_time=3.2,
            rate_func=smooth,
        )
        self.finish()


class S02Bcell(SpokenScene):
    def construct(self):
        donor = make_donor_cell_left(edge_x=-3.25, peptide=True)
        t_match = make_target_cell_right(center_y=1.45, match=True, x_edge=3.50)
        t_silent = make_target_cell_right(center_y=-1.45, match=False, x_edge=3.50)
        b_lab = T("B cell", size=28, color=CYTOSOL).move_to([-5.35, 2.95, 0.0])
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(donor, t_match, t_silent, b_lab, tag)

        p = ValueTracker(0.0)
        sig_p = ValueTracker(0.0)

        def v1_pos(u):
            s = min(1.0, u / 0.68)
            return np.array([-2.35 + 4.80 * s, 1.35 + 0.10 * np.sin(s * PI / 2), 0.0])

        def v2_pos(u):
            return np.array([-2.35 + 4.00 * min(1.0, u), 0.0 + 0.25 * np.sin(u * PI), 0.0])

        def v3_pos(u):
            if u < 0.62:
                s = u / 0.62
                return np.array([-2.35 + 5.05 * s, -1.35 - 0.10 * np.sin(s * PI / 2), 0.0])
            s = (u - 0.62) / 0.38
            return np.array([2.70 - 1.65 * s, -1.45 - 0.62 * s, 0.0])

        vesicles = always_redraw(lambda: VGroup(
            make_vesicle(v1_pos(p.get_value()), radius=0.35, n_ligands=6, peptide=True, cargo_dots=3, seed=7, angle_offset=0.25 * p.get_value(), scale_lig=0.78),
            make_vesicle(v2_pos(p.get_value()), radius=0.35, n_ligands=6, peptide=True, cargo_dots=3, seed=13, angle_offset=0.4 + 0.6 * p.get_value(), scale_lig=0.78),
            make_vesicle(v3_pos(p.get_value()), radius=0.35, n_ligands=6, peptide=True, cargo_dots=3, seed=19, angle_offset=0.2 + 0.5 * p.get_value(), scale_lig=0.78),
        ))
        self.add(vesicles)

        self.play(p.animate.set_value(0.24), run_time=2.6, rate_func=linear)

        self.at("extracellular vesicles")
        ev_lab = T("Extracellular vesicles", size=28, color=MEMBRANE).move_to([0.0, 2.95, 0.0])
        self.play(FadeIn(ev_lab), p.animate.set_value(0.46), run_time=3.6, rate_func=linear)

        self.at("display peptide")
        mhc_lab = T("MHC class II + peptide", size=28, color=LIGAND).move_to([-0.85, -3.10, 0.0])
        self.play(FadeIn(mhc_lab), p.animate.set_value(0.68), run_time=4.5, rate_func=linear)

        self.at("switch on only")
        sig_wave = always_redraw(lambda: make_signal_waves([3.50, 1.45, 0.0], sig_p.get_value(), color=MATCH, max_r=1.25))
        self.add(sig_wave)
        active_lab = T("Matching T cell: active", size=28, color=MATCH).move_to([4.55, 3.15, 0.0])
        silent_lab = T("Non-matching:\nsilent", size=28, color=SILENT).move_to([5.25, -1.45, 0.0])
        self.play(
            p.animate.set_value(0.90),
            sig_p.animate.set_value(1.2),
            FadeIn(active_lab),
            FadeIn(silent_lab),
            run_time=4.5,
            rate_func=linear,
        )

        self.at("Nothing enters")
        focus = Circle(radius=0.68, color=TEXT, stroke_width=3).move_to([2.75, 1.45, 0.0])
        stay_lab = T("Vesicle stays outside", size=28, color=TEXT).move_to([-0.2, 2.05, 0.0])
        self.play(Create(focus), FadeIn(stay_lab), p.animate.set_value(1.0), sig_p.animate.set_value(1.8), run_time=2.2, rate_func=linear)
        self.finish()


class S03Endocytosis(SpokenScene):
    def construct(self):
        p = ValueTracker(0.0)
        d = ValueTracker(0.0)
        z = ValueTracker(0.0)
        rp = ValueTracker(0.0)
        scene_geo = always_redraw(lambda: _endocytosis_geometry(p.get_value(), drift=d.get_value(), zoom=z.get_value(), rec_pulse=rp.get_value())[0])
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(scene_geo, tag)

        cyto_lab = T("Cytosol", size=28, color=CYTOSOL).move_to([-5.2, 3.10, 0.0])
        out_lab = T("Outside", size=28, color=TEXT).move_to([4.4, 3.10, 0.0])
        # Zoom into the donor surface during the opening question
        self.play(FadeIn(cyto_lab), FadeIn(out_lab), z.animate.set_value(1.0), run_time=3.6, rate_func=smooth)

        self.at("Follow a receptor")
        rec_lab = T("Coral head faces outside", size=28, color=LIGAND).move_to([4.35, 0.85, 0.0])
        rec_arr = Arrow([3.1, 0.50, 0], [2.15, 0.08, 0], color=LIGAND, buff=0.05, stroke_width=4)
        self.play(FadeIn(rec_lab), Create(rec_arr), run_time=1.4)
        self.play(rp.animate.set_value(2.0), run_time=4.2, rate_func=linear)

        self.at("First, the plasma")
        flip_lab = T("Endocytosis: flip 1", size=30, color=MEMBRANE).move_to([-1.6, 3.10, 0.0])
        self.play(FadeOut(rec_lab), FadeOut(rec_arr), FadeIn(flip_lab), p.animate.set_value(0.20), run_time=1.2, rate_func=linear)
        self.play(p.animate.set_value(1.0), run_time=6.2, rate_func=smooth)

        self.at("points the head")
        inward_lab = T("Head points inward", size=28, color=LIGAND).move_to([-2.2, -2.55, 0.0])
        lumen_lab = T("Trapped outside fluid", size=28, color=TEXT).move_to([-2.2, 2.25, 0.0])
        in_arr = Arrow([-3.15, 0.0, 0], [-1.75, 0.0, 0], color=LIGAND, buff=0.05, stroke_width=4.5)
        self.play(FadeIn(inward_lab), FadeIn(lumen_lab), Create(in_arr), d.animate.set_value(0.35), run_time=1.5)
        self.play(d.animate.set_value(1.0), run_time=3.2, rate_func=smooth)
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        b = ValueTracker(0.0)
        flow = ValueTracker(0.0)
        bud_geo = always_redraw(lambda: _inward_bud_geometry(b.get_value(), flow=flow.get_value())[0])
        tag = scope_tag("schematic", size=24, color=TEXT)
        cyto_lab = T("Cytosol", size=28, color=CYTOSOL).move_to([-5.2, 2.95, 0.0])
        lumen_lab = T("Endosome fluid", size=28, color=TEXT).move_to([-0.55, -2.95, 0.0])
        self.add(bud_geo, cyto_lab, lumen_lab, tag)

        self.at("membrane bulges")
        bud_lab = T("Inward bud: flip 2", size=28, color=MEMBRANE).move_to([4.35, 2.45, 0.0])
        self.play(FadeIn(bud_lab), b.animate.set_value(0.14), flow.animate.set_value(0.45), run_time=1.0)
        self.play(b.animate.set_value(0.62), flow.animate.set_value(3.0), run_time=7.0, rate_func=linear)

        self.at("drop of cytosol")
        drop_lab = T("Cytosol fills bud", size=28, color=CYTOSOL).move_to([4.35, -1.75, 0.0])
        self.play(b.animate.set_value(0.78), flow.animate.set_value(4.0), FadeIn(drop_lab), run_time=2.6, rate_func=linear)

        self.at("Before it pinches")
        _, _, _, outer_pt, inner_pt = _inward_bud_geometry(0.78)
        q_out = T("?", size=38, color=TEXT, weight=BOLD).move_to(outer_pt)
        q_in = T("?", size=38, color=TEXT, weight=BOLD).move_to(inner_pt)
        q_card = question_card("Where does the coral head end up?", y=3.22, color=GOLD, size=30, max_w=11.0)
        self.play(FadeOut(drop_lab), FadeIn(q_out), FadeIn(q_in), FadeIn(q_card), flow.animate.set_value(5.6), run_time=4.4, rate_func=linear)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Where does the coral head end up?"
    OPTIONS = ()
    CARD = {"y": 3.22, "size": 30, "max_w": 11.0}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        bud_geo, _, _, outer_pt, inner_pt = _inward_bud_geometry(0.78, flow=0.6)
        cyto_lab = T("Cytosol", size=28, color=CYTOSOL).move_to([-5.2, 2.95, 0.0])
        lumen_lab = T("Endosome fluid", size=28, color=TEXT).move_to([-0.55, -2.95, 0.0])
        bud_lab = T("Inward bud: flip 2", size=28, color=MEMBRANE).move_to([4.35, 2.45, 0.0])
        q_out = T("?", size=38, color=TEXT, weight=BOLD).move_to(outer_pt)
        q_in = T("?", size=38, color=TEXT, weight=BOLD).move_to(inner_pt)
        return VGroup(bud_geo, cyto_lab, lumen_lab, bud_lab, q_out, q_in)


class S06Reveal(SpokenScene):
    def construct(self):
        b = ValueTracker(0.78)
        drift_x = ValueTracker(0.0)
        bud_geo = always_redraw(lambda: _inward_bud_geometry(b.get_value(), drift_x=drift_x.get_value())[0])
        cyto_lab = T("Cytosol", size=28, color=CYTOSOL).move_to([-5.2, 2.95, 0.0])
        lumen_lab = T("Endosome fluid", size=28, color=TEXT).move_to([-0.55, -2.95, 0.0])
        bud_lab = T("Inward bud: flip 2", size=28, color=MEMBRANE).move_to([4.35, 2.45, 0.0])
        _, _, _, outer_pt, inner_pt = _inward_bud_geometry(0.78)
        q_out = T("?", size=38, color=TEXT, weight=BOLD).move_to(outer_pt)
        q_in = T("?", size=38, color=TEXT, weight=BOLD).move_to(inner_pt)
        q_card = question_card("Where does the coral head end up?", y=3.22, color=GOLD, size=30, max_w=11.0)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(bud_geo, cyto_lab, lumen_lab, bud_lab, q_out, q_in, q_card, tag)

        self.play(FadeOut(q_card), FadeOut(bud_lab), FadeOut(q_out), FadeOut(q_in), b.animate.set_value(0.82), run_time=0.45, rate_func=linear)
        self.play(b.animate.set_value(1.0), run_time=1.95, rate_func=smooth)

        def _bud_c():
            return np.array([-0.15 + 0.35 - drift_x.get_value(), -0.15, 0.0])

        self.at("coral head faces")
        out_lab = T("Ligands face out", size=28, color=LIGAND).move_to([4.65, 1.15, 0.0])
        out_arr = always_redraw(lambda: Arrow(
            out_lab.get_left() + LEFT * 0.18,
            _bud_c() + 0.81 * _unit(PI / 2 + 0.35 * drift_x.get_value()) + np.array([0.14, 0.04, 0.0]),
            color=LIGAND, buff=0.05, stroke_width=4,
        ))
        self.play(FadeIn(out_lab), FadeIn(out_arr), drift_x.animate.set_value(0.14), run_time=4.0, rate_func=linear)

        self.at("cytosol stays sealed")
        in_lab = T("Cytosol sealed inside", size=28, color=CYTOSOL).move_to([4.65, -0.55, 0.0])
        in_arr = always_redraw(lambda: Arrow(
            in_lab.get_left() + LEFT * 0.18,
            _bud_c() + np.array([0.10, -0.18, 0.0]),
            color=CYTOSOL, buff=0.05, stroke_width=4,
        ))
        self.play(FadeIn(in_lab), FadeIn(in_arr), drift_x.animate.set_value(0.25), run_time=3.5, rate_func=linear)

        self.at("keep cell orientation")
        rule_cap = caption("Ligands face out; internal cargo stays sealed.", size=28, color=TEXT, y=-3.10)
        self.play(FadeOut(out_lab), FadeOut(out_arr), FadeOut(in_lab), FadeOut(in_arr), swap(lumen_lab, rule_cap, run_time=0.8), run_time=0.9)

        pack_t = ValueTracker(0.0)
        endo_c = np.array([-0.15, -0.15, 0.0])
        rim_angles = [2.4, 3.8, 0.65, 5.6]
        dest_pts = [
            endo_c + np.array([-1.25, 0.95, 0.0]),
            endo_c + np.array([-1.25, -0.95, 0.0]),
            endo_c + np.array([1.25, 0.95, 0.0]),
            endo_c + np.array([1.25, -0.95, 0.0]),
        ]

        def extra_ves():
            u = pack_t.get_value()
            vg = VGroup()
            for k, (ang, dst) in enumerate(zip(rim_angles, dest_pts)):
                local_u = np.clip((u - k * 0.15) / 0.45, 0.0, 1.0)
                if local_u > 0.05:
                    start = endo_c + 2.02 * _unit(ang)
                    pos = start + (dst - start) * local_u + 0.15 * np.sin(u * 2.0 + k) * UP
                    sc = 0.40 + 0.60 * local_u
                    vg.add(make_vesicle(pos, radius=0.40 * sc, n_ligands=4, cargo_dots=2, seed=20 + k, angle_offset=0.3 * k + 0.6 * u, scale_lig=0.72 * sc))
            return vg

        extra = always_redraw(extra_ves)
        self.add(extra)
        self.play(pack_t.animate.set_value(0.95), drift_x.animate.set_value(0.32), run_time=5.4, rate_func=linear)

        self.at("compartment packed")
        mvb_lab = T("Multivesicular body", size=32, color=MEMBRANE).move_to([0.0, 3.10, 0.0])
        self.play(FadeIn(mvb_lab), pack_t.animate.set_value(1.45), drift_x.animate.set_value(0.35), run_time=4.0, rate_func=linear)
        self.finish()


class S07TwoDoors(SpokenScene):
    def construct(self):
        y_top, y_bot = 3.55, -3.55
        x_mem = 2.2
        cyto = Polygon([-7.15, y_bot, 0], [x_mem, y_bot, 0], [x_mem, y_top, 0], [-7.15, y_top, 0],
                       stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.16)
        pm = Line([x_mem, y_bot, 0], [x_mem, y_top, 0], color=MEMBRANE, stroke_width=6.0)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(cyto, pm, tag)

        mvb_main = make_mvb(np.array([-4.4, -0.2, 0.0]), radius=1.02, n_ves=5, seed=7)
        lyso = Circle(radius=1.02, stroke_color=SILENT, stroke_width=5.5, fill_color=SILENT, fill_opacity=0.22).move_to([-0.2, 1.85, 0.0])
        lyso_lab = T("Lysosome", size=28, color=SILENT).next_to(lyso, UP, buff=0.18)
        exits_lab = T("Two exits", size=30, color=TEXT).move_to([-4.4, 2.95, 0.0])
        path_up = CurvedArrow(np.array([-3.3, 0.45, 0.0]), np.array([-1.35, 1.75, 0.0]), angle=-0.2, color=SILENT, stroke_width=3.5)
        path_dn = CurvedArrow(np.array([-3.3, -0.75, 0.0]), np.array([1.75, -1.35, 0.0]), angle=0.2, color=MEMBRANE, stroke_width=3.5)

        self.play(FadeIn(mvb_main), FadeIn(lyso), FadeIn(lyso_lab), FadeIn(exits_lab), Create(path_up), Create(path_dn), run_time=2.4)
        self.play(mvb_main.animate.shift(RIGHT * 0.25), run_time=1.8, rate_func=smooth)

        self.at("fuses with a lysosome")
        mvb_up = mvb_main.copy()
        self.add(mvb_up)
        self.play(mvb_up.animate.move_to([-0.2, 1.85, 0.0]).scale(0.85), run_time=2.4, rate_func=smooth)
        frags = VGroup(*[
            Dot(np.array([-0.2, 1.85, 0]) + 0.45 * _unit(k * TAU / 8), radius=0.06, color=MEMBRANE if k % 2 == 0 else LIGAND)
            for k in range(8)
        ])
        dig_lab = T("Broken down", size=28, color=SILENT).move_to([-0.2, 0.35, 0.0])
        self.play(ReplacementTransform(mvb_up, frags), FadeIn(dig_lab), run_time=1.4)
        self.play(FadeOut(frags), run_time=1.0)

        self.at("moves to the surface")
        self.play(mvb_main.animate.move_to([1.15, -1.35, 0.0]), run_time=1.2, rate_func=smooth)

        self.at("fuses with the plasma")
        spill = ValueTracker(0.0)
        pore_y = -1.35
        pore_r = 1.08

        def fused_pocket():
            u = spill.get_value()
            d_x = 1.75 * (1.0 - 0.30 * min(1.0, u))
            pocket_curve = [
                np.array([x_mem, pore_y - pore_r, 0.0]),
                np.array([x_mem - 0.45 * d_x, pore_y - 0.92, 0.0]),
                np.array([x_mem - 0.92 * d_x, pore_y - 0.72, 0.0]),
                np.array([x_mem - 1.08 * d_x, pore_y, 0.0]),
                np.array([x_mem - 0.92 * d_x, pore_y + 0.72, 0.0]),
                np.array([x_mem - 0.45 * d_x, pore_y + 0.92, 0.0]),
                np.array([x_mem, pore_y + pore_r, 0.0]),
            ]
            pts = (
                [
                    np.array([x_mem, y_bot, 0.0]),
                    np.array([x_mem, pore_y - pore_r - 0.70, 0.0]),
                    np.array([x_mem, pore_y - pore_r - 0.30, 0.0]),
                ]
                + pocket_curve
                + [
                    np.array([x_mem, pore_y + pore_r + 0.30, 0.0]),
                    np.array([x_mem, pore_y + pore_r + 0.70, 0.0]),
                    np.array([x_mem, pore_y + pore_r + 1.80, 0.0]),
                    np.array([x_mem, y_top, 0.0]),
                ]
            )
            mem = VMobject(stroke_color=MEMBRANE, stroke_width=6.0, fill_opacity=0)
            mem.set_points_smoothly(pts)
            cut = Polygon(
                *(pocket_curve + [np.array([x_mem + 0.06, pore_y + pore_r, 0.0]), np.array([x_mem + 0.06, pore_y - pore_r, 0.0])]),
                stroke_width=0, fill_color=BG, fill_opacity=1.0,
            )
            starts = [
                np.array([1.70, pore_y, 0.0]),
                np.array([1.32, pore_y + 0.44, 0.0]),
                np.array([0.82, pore_y + 0.26, 0.0]),
                np.array([0.82, pore_y - 0.26, 0.0]),
                np.array([1.32, pore_y - 0.44, 0.0]),
            ]
            ctrls = [
                np.array([2.75, pore_y, 0.0]),
                np.array([2.55, pore_y + 0.32, 0.0]),
                np.array([2.50, pore_y + 0.22, 0.0]),
                np.array([2.50, pore_y - 0.22, 0.0]),
                np.array([2.55, pore_y - 0.32, 0.0]),
            ]
            ends = [
                np.array([4.25, pore_y - 0.10, 0.0]),
                np.array([4.95, pore_y + 0.60, 0.0]),
                np.array([3.55, pore_y + 0.80, 0.0]),
                np.array([3.50, pore_y - 1.00, 0.0]),
                np.array([5.15, pore_y - 0.75, 0.0]),
            ]
            exos = VGroup()
            for k, (start, ctrl, end) in enumerate(zip(starts, ctrls, ends)):
                t = min(1.0, u * 1.05)
                pos = ((1 - t) ** 2) * start + 2 * (1 - t) * t * ctrl + (t ** 2) * end + RIGHT * 0.45 * max(0.0, u - 0.8)
                exos.add(make_vesicle(pos, radius=0.26, n_ligands=5, cargo_dots=2, seed=30 + k, angle_offset=0.5 * u + k, scale_lig=0.62))
            return VGroup(cut, mem, exos)

        fused = always_redraw(fused_pocket)
        self.remove(pm, mvb_main)
        self.add(fused)
        self.play(FadeOut(path_up), FadeOut(path_dn), spill.animate.set_value(0.08), run_time=0.45, rate_func=linear)
        self.play(spill.animate.set_value(0.85), run_time=4.95, rate_func=smooth)

        self.at("are exosomes")
        exo_lab = T("Exosomes", size=30, color=MEMBRANE).move_to([4.5, 0.45, 0.0])
        self.play(FadeIn(exo_lab), spill.animate.set_value(0.93), run_time=0.45, rate_func=linear)
        self.play(spill.animate.set_value(1.22), run_time=1.75, rate_func=linear)
        self.finish()


class S08Microvesicles(SpokenScene):
    def construct(self):
        x_mem = -1.2
        m = ValueTracker(0.0)
        bud_geo = always_redraw(lambda: _microvesicle_bud_geometry(m.get_value(), x_mem=x_mem, bud_y=1.35)[0])

        exo_x = ValueTracker(1.25)
        exo_lower = always_redraw(lambda: make_vesicle([exo_x.get_value(), -1.35, 0.0], radius=0.44, n_ligands=6, cargo_dots=3, seed=7, angle_offset=0.25 * exo_x.get_value(), scale_lig=0.82))
        exo_lab = always_redraw(lambda: T("Exosome", size=28, color=MEMBRANE).move_to([exo_x.get_value(), -2.35, 0.0]))
        tag = scope_tag("schematic", size=24, color=TEXT)

        self.add(bud_geo, exo_lower, exo_lab, tag)
        self.play(exo_x.animate.set_value(1.65), run_time=2.4, rate_func=linear)

        self.at("budding straight outward")
        mv_lab = T("Microvesicle", size=28, color=MEMBRANE).move_to([1.95, 2.35, 0.0])
        self.play(m.animate.set_value(0.92), exo_x.animate.set_value(2.10), FadeIn(mv_lab), run_time=6.4, rate_func=smooth)

        self.at("exact same orientation")
        same_lab = T("Same orientation: ligands out, cytosol inside", size=28, color=TEXT).move_to([2.9, 3.05, 0.0])
        fit(same_lab, max_w=7.5)
        self.play(FadeIn(same_lab), m.animate.set_value(1.0), exo_x.animate.set_value(2.60), mv_lab.animate.move_to([2.60, 2.35, 0.0]), run_time=3.8, rate_func=linear)
        self.play(m.animate.set_value(1.032), exo_x.animate.set_value(2.98), mv_lab.animate.move_to([2.98, 2.35, 0.0]), run_time=4.4, rate_func=linear)

        self.at("unproven origin")
        brace = BraceBetweenPoints([3.78, -1.55, 0], [3.78, 1.55, 0], direction=RIGHT, color=TEXT)
        ev_lab = T("Extracellular\nvesicles", size=28, color=TEXT).next_to(brace, RIGHT, buff=0.14)
        self.play(Create(brace), FadeIn(ev_lab), run_time=2.4)
        self.finish()


class S09ThreeWays(SpokenScene):
    def construct(self):
        # Pan right onto target cell membrane (x_mem slides from +1.2 -> -1.6)
        pan_x = ValueTracker(1.2)
        target_geo = always_redraw(lambda: VGroup(
            Polygon([pan_x.get_value(), -3.55, 0], [7.15, -3.55, 0], [7.15, 3.55, 0], [pan_x.get_value(), 3.55, 0],
                    stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.14),
            Line([pan_x.get_value(), -3.55, 0], [pan_x.get_value(), 3.55, 0], color=MEMBRANE, stroke_width=6.0),
            make_target_receptor(np.array([pan_x.get_value(), 2.05, 0.0]), angle=PI, match=True, scale=1.0),
        ))
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(target_geo, tag)
        self.play(pan_x.animate.set_value(-1.6), run_time=2.3, rate_func=smooth)

        x_mem = -1.6
        div1 = DashedLine([-6.4, 0.95, 0], [6.4, 0.95, 0], color=GREY, stroke_width=2, dash_length=0.16)
        div2 = DashedLine([-6.4, -1.05, 0], [6.4, -1.05, 0], color=GREY, stroke_width=2, dash_length=0.16)
        l1_lab = T("1. Surface ligand", size=28, color=LIGAND).move_to([3.8, 2.75, 0.0])
        l2_lab = T("2. Membrane fusion", size=28, color=CYTOSOL).move_to([4.35, 0.68, 0.0])
        l3_lab = T("3. Uptake", size=28, color=TEXT).move_to([4.5, -1.35, 0.0])

        self.at("three ways")
        self.play(Create(div1), Create(div2), FadeIn(l1_lab), FadeIn(l2_lab), FadeIn(l3_lab), run_time=2.2)

        self.at("First, a surface")
        v1_x = ValueTracker(-4.8)
        v1 = always_redraw(lambda: make_vesicle([v1_x.get_value(), 2.05, 0.0], radius=0.38, n_ligands=6, cargo_dots=3, seed=7, angle_offset=0.0, scale_lig=0.80))
        self.add(v1)
        self.play(v1_x.animate.set_value(-2.68), run_time=2.5, rate_func=smooth)

        sig_w = ValueTracker(0.0)
        waves = always_redraw(lambda: make_signal_waves([x_mem, 2.05, 0.0], sig_w.get_value(), color=MATCH, max_r=1.25))
        self.add(waves)
        sig1_lab = T("Signals on contact", size=26, color=MATCH).move_to([1.35, 2.05, 0.0])
        self.play(sig_w.animate.set_value(1.1), FadeIn(sig1_lab), run_time=2.5, rate_func=linear)

        self.at("Second, the vesicle")
        f_t = ValueTracker(0.0)

        def lane2_ves_and_cargo():
            u = f_t.get_value()
            if u < 0.38:
                s = u / 0.38
                vx = -4.8 + 2.82 * s
                return make_vesicle([vx, 0.0, 0.0], radius=0.38, n_ligands=6, cargo_dots=3, seed=11, angle_offset=0.2 + 0.5 * s, scale_lig=0.80)
            s = (u - 0.38) / 0.62
            arc_r = max(0.06, 0.38 * (1.0 - 0.82 * min(1.0, s)))
            patch = Arc(radius=arc_r, start_angle=PI / 2, angle=PI, arc_center=[x_mem, 0.0, 0], color=MEMBRANE, stroke_width=5.5)
            dots = VGroup(
                Dot([x_mem + 0.35 + 2.15 * s, 0.22 * min(1.0, s), 0], radius=0.105, color=CYTOSOL),
                Dot([x_mem + 0.65 + 2.75 * s, -0.10 * min(1.0, s), 0], radius=0.105, color=CYTOSOL),
                Dot([x_mem + 0.25 + 1.65 * s, 0.30 * min(1.0, s), 0], radius=0.105, color=CYTOSOL),
                Dot([x_mem + 0.45 + 2.45 * s, 0.05 * min(1.0, s), 0], radius=0.105, color=CYTOSOL),
            )
            return VGroup(patch, dots)

        v2 = always_redraw(lane2_ves_and_cargo)
        self.add(v2)
        spill_lab = T("Cargo into cytosol", size=26, color=CYTOSOL).move_to([1.45, -0.62, 0.0])
        self.play(f_t.animate.set_value(0.84), sig_w.animate.set_value(2.4), run_time=4.8, rate_func=linear)
        self.play(FadeIn(spill_lab), f_t.animate.set_value(1.12), sig_w.animate.set_value(3.2), run_time=2.0, rate_func=linear)
        self.finish()


class S10UptakeAndRule(SpokenScene):
    def construct(self):
        x_mem = -1.6
        cyto = Polygon([x_mem, -3.55, 0], [7.15, -3.55, 0], [7.15, 3.55, 0], [x_mem, 3.55, 0],
                       stroke_width=0, fill_color=CYTOSOL, fill_opacity=0.14)
        pm = Line([x_mem, -1.05, 0], [x_mem, 3.55, 0], color=MEMBRANE, stroke_width=6.0)
        div1 = DashedLine([-6.4, 0.95, 0], [6.4, 0.95, 0], color=GREY, stroke_width=2, dash_length=0.16)
        div2 = DashedLine([-6.4, -1.05, 0], [6.4, -1.05, 0], color=GREY, stroke_width=2, dash_length=0.16)
        l1_lab = T("1. Surface ligand", size=28, color=LIGAND).move_to([3.8, 2.75, 0.0])
        l2_lab = T("2. Membrane fusion", size=28, color=CYTOSOL).move_to([4.35, 0.68, 0.0])
        l3_lab = T("3. Uptake", size=28, color=TEXT).move_to([4.5, -1.35, 0.0])
        rec1 = make_target_receptor(np.array([x_mem, 2.05, 0.0]), angle=PI, match=True, scale=1.0)
        v1 = make_vesicle([-2.82, 2.05, 0.0], radius=0.38, n_ligands=6, cargo_dots=3, seed=7, angle_offset=0.0, scale_lig=0.80)
        sig1_lab = T("Signals on contact", size=26, color=MATCH).move_to([1.35, 2.05, 0.0])
        diff_t = ValueTracker(0.0)
        cargo_spilled = always_redraw(lambda: VGroup(
            Dot([x_mem + 2.55 + 0.55 * diff_t.get_value(), 0.22, 0], radius=0.105, color=CYTOSOL),
            Dot([x_mem + 3.25 + 0.55 * diff_t.get_value(), -0.10, 0], radius=0.105, color=CYTOSOL),
            Dot([x_mem + 1.95 + 0.55 * diff_t.get_value(), 0.30, 0], radius=0.105, color=CYTOSOL),
            Dot([x_mem + 2.85 + 0.55 * diff_t.get_value(), 0.05, 0], radius=0.105, color=CYTOSOL),
        ))
        spill_lab = T("Cargo into cytosol", size=26, color=CYTOSOL).move_to([1.45, -0.62, 0.0])
        sig_w = ValueTracker(0.0)
        waves = always_redraw(lambda: make_signal_waves([x_mem, 2.05, 0.0], sig_w.get_value(), color=MATCH, max_r=1.25))
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(cyto, pm, div1, div2, l1_lab, l2_lab, l3_lab, rec1, v1, sig1_lab, waves, cargo_spilled, spill_lab, tag)

        e_t = ValueTracker(0.0)
        lyso = Circle(radius=0.44, stroke_color=SILENT, stroke_width=4.5, fill_color=SILENT, fill_opacity=0.22).move_to([4.55, -2.52, 0.0])
        lyso_lab = T("Lysosome", size=26, color=SILENT).move_to([4.55, -1.90, 0.0])

        def lane3_uptake():
            u = e_t.get_value()
            if u < 0.25:
                s = u / 0.25
                vx = -4.8 + 2.5 * s
                pm_bot = Line([x_mem, -3.55, 0], [x_mem, -1.05, 0], color=MEMBRANE, stroke_width=6.0)
                ves = make_vesicle([vx, -2.25, 0.0], radius=0.38, n_ligands=5, cargo_dots=3, seed=15, scale_lig=0.76)
                return VGroup(pm_bot, ves)
            if u < 0.56:
                s = (u - 0.25) / 0.31
                vx = -2.3 + 1.15 * s
                ys = np.linspace(-3.55, -1.05, 64)
                pts = [np.array([x_mem + 1.75 * s * np.exp(-(((y + 2.25) / 0.75) ** 2)), y, 0.0]) for y in ys]
                pts[0][0] = x_mem
                pts[-1][0] = x_mem
                cut_pts = [np.array([x_mem - 0.05, -3.55, 0.0])] + pts + [np.array([x_mem - 0.05, -1.05, 0.0])]
                pocket_cut = Polygon(*cut_pts, stroke_width=0, fill_color=BG, fill_opacity=1.0)
                wrap = VMobject(stroke_color=MEMBRANE, stroke_width=6.0, fill_opacity=0)
                wrap.set_points_smoothly(pts)
                ves = make_vesicle([vx, -2.25, 0.0], radius=0.38, n_ligands=5, cargo_dots=3, seed=15, scale_lig=0.76)
                return VGroup(pocket_cut, wrap, ves)
            s = (u - 0.56) / 0.44
            ex = (x_mem + 0.68) + 3.47 * s
            ey = -2.25 - 0.35 * s
            pm_bot = Line([x_mem, -3.55, 0], [x_mem, -1.05, 0], color=MEMBRANE, stroke_width=6.0)
            endo = Circle(radius=0.68, stroke_color=MEMBRANE, stroke_width=5.5, fill_color=LUMEN, fill_opacity=0.45).move_to([ex, ey, 0.0])
            ves = make_vesicle([ex, ey, 0.0], radius=0.36, n_ligands=5, cargo_dots=3, seed=15, angle_offset=0.5 * s, scale_lig=0.72)
            return VGroup(pm_bot, endo, ves)

        v3 = always_redraw(lane3_uptake)
        self.add(v3)
        self.play(e_t.animate.set_value(0.24), sig_w.animate.set_value(0.45), diff_t.animate.set_value(0.15), run_time=1.4, rate_func=linear)

        self.at("swallow the vesicle")
        self.play(e_t.animate.set_value(0.66), sig_w.animate.set_value(2.05), diff_t.animate.set_value(0.45), run_time=5.4, rate_func=linear)

        self.at("usually ends up")
        self.play(FadeIn(lyso), FadeIn(lyso_lab), e_t.animate.set_value(1.0), sig_w.animate.set_value(3.25), diff_t.animate.set_value(0.70), run_time=3.6, rate_func=linear)
        deg_lab = T("Often degraded", size=26, color=SILENT).move_to([0.35, -3.12, 0.0])
        self.play(FadeIn(deg_lab), sig_w.animate.set_value(3.75), diff_t.animate.set_value(0.80), run_time=1.2, rate_func=linear)

        self.at("if it escapes")
        esc_arr = DashedLine([2.90, -2.08, 0], [2.42, -1.48, 0], color=CYTOSOL, stroke_width=3.5, dash_length=0.10)
        esc_p = ValueTracker(0.0)
        esc_dot = always_redraw(lambda: Dot(
            np.array([2.90, -2.08, 0]) + (np.array([2.42, -1.48, 0]) - np.array([2.90, -2.08, 0])) * esc_p.get_value(),
            radius=0.105, color=CYTOSOL,
        ))
        esc_lab = T("Rare escape or sensing", size=24, color=CYTOSOL).move_to([0.45, -1.45, 0.0])
        self.add(esc_dot)
        self.play(Create(esc_arr), esc_p.animate.set_value(1.0), FadeIn(esc_lab), sig_w.animate.set_value(4.75), diff_t.animate.set_value(0.95), run_time=2.8, rate_func=linear)

        self.at("Orientation decides")
        h1 = Circle(radius=0.70, color=LIGAND, stroke_width=3.5).move_to(v1.get_center())
        h2 = Circle(radius=0.28, color=CYTOSOL, stroke_width=3.5).move_to(v3[2][0].get_center())
        self.play(Create(h1), Create(h2), sig_w.animate.set_value(6.05), diff_t.animate.set_value(1.15), run_time=3.8, rate_func=linear)
        self.finish()


class S11End(EndCard):
    LINE = "Extracellular vesicles keep cell orientation:\nligands face out, internal cargo stays sealed."
