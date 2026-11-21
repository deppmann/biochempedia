"""
What the Scan Sees — Thyroid Hormone, Chapter 2
================================================

COLOUR MAP (one colour per concept for the entire film):
- BLUE   (#58C4DD): T4 (hormone dots, blood hormone gauge arc/needle, T4 feedback arrow)
- GREEN  (#83C167): T3 (hormone segments on thyroglobulin and exported T3 dots)
- YELLOW (#F5D547): Ordinary dietary iodide (dots) and hidden-gauge '?'
- ORANGE (#FF862F): Radioactive iodine-123 tracer (dots and thyroid scan glow)
- PINK   (#FF7EB6): MCT8 hormone transporter doors
- PURPLE (#9A72AC): Deiodinases (D2 in opening link-back)
- CYAN   (#2EE6D6): NIS (sodium-iodide symporter) doors on the blood side of follicle cells
- MAGENTA(#E040FB): TSH from the pituitary
- GREY   (#8B93A1): Glands, follicle cells, blood vessels, colloid gel, pituitary, scan camera
- TEXT   (#E8EAF0): White/light text for labels, headings, and the schematic tag

ONE CARRIED PICTURE OF THE WORLD:
- Macro view: The neck — a two-lobed butterfly thyroid gland (centre-left), a blood vessel
  beside it carrying hormone/iodide/tracer dots, and a schematic 'blood hormone' dial gauge
  at the right (with the pituitary + TSH/T4 loop above when relevant).
- Micro view: Zoom into one thyroid follicle — 10 cube-shaped cells in a ring around a central
  colloid gel lumen, wrapped by a curving blood capillary entering from the left and looping
  around the outside of the ring.

WHAT CHANGES ON SCREEN (and what it is computed from):
- s00_link_and_question: T4 enters tissue cell via PINK MCT8 and PURPLE D2 converts it to GREEN T3;
  camera moves to two-lobed gland + blood vessel with continuously flowing BLUE T4 dots, while a
  computed ORANGE scan glow rises via a ValueTracker and '?' hides the blood hormone gauge.
- s01_title: Standard TitleCard ("What the Scan Sees") for 2.0 s.
- s02_follicle: Gland glow dims and zooms into the 10-cell follicle + curving capillary; blood and
  colloid faces highlight in sequence, CYAN NIS doors open, and YELLOW iodide dots cross along
  computed radial paths through NIS doors into the cells.
- s03_build: Highlighted cell moves YELLOW iodide to apical TPO spark; iodide attaches to pale GREY
  thyroglobulin strands, segments turn BLUE (T4) and GREEN (T3), MAGENTA TSH drives inward
  pinching/digestion of a colloid vesicle, and computed BLUE/GREEN dots exit via PINK MCT8 into blood.
- s04_tracer: CYAN NIS doors pulse while YELLOW iodide enters; ORANGE tracer dots mix into
  capillary flow and enter with YELLOW iodide (colloid ORANGE glow integrates accumulated tracer),
  clock sweeps hours later, camera pulls back to whole gland under descending scan camera.
- s05_idea: Split world — glowing gland with active inset follicle at left vs vessel + gauge at right
  separated by dashed divider; trapping (NIS), fixing (colloid strands), and iodide supply stream
  animate in turn while BLUE vessel dots drift independently of scan glow.
- s06_predict: Follicle view with steady YELLOW + ORANGE mix entering NIS; on 'iodine load', a dense
  computed wave of YELLOW dots floods the capillary from left while ORANGE count stays constant
  and colloid glow holds steady as question card appears at top.
- s07_pause: PredictPause holds question card and countdown ring while the dense YELLOW flood and
  sparse ORANGE dots keep drifting slowly in the capillary.
- s08_answer: Dilution ratio N_tracer/(N_tracer+N_iodide) drops sharply so NIS passes mostly YELLOW
  and colloid/gland-inset glow fades ('lower uptake'); then YELLOW drains away ('iodine short') so
  nearly every trapped dot is ORANGE and glow brightens ('high uptake'); '?' lifts off gauge and
  BLUE needle drifts down while scan glows bright.
- s09_nodule: Whole gland under scan camera + pituitary + MAGENTA TSH arrow + gauge; one lower-right
  nodule brightens ORANGE and pours extra BLUE dots into blood, gauge needle rises, BLUE feedback
  arrow suppresses/thins MAGENTA TSH, and the rest of both lobes dims to faint ORANGE.
- s10_read_together: Nodule scan slides left beside matching-size blood hormone gauge + vessel at
  right; white 'read together' bracket joins them; gauge highlights on hormone level, scan + iodide
  inflow highlight on uptake and location.
- s11_close: Opening two-lobed gland + vessel returns; camera eases in smoothly on gland and edge
  CYAN NIS doors pulling YELLOW + ORANGE dots inward, BLUE vessel dots pulse without altering gland
  glow, and 'Bright = more hormone?' appears, is crossed through in RED, and fades while moving.
- s12_end: Standard EndCard with the take-home line.
"""
from bp_parts import *

# Distinct concept colours
CYAN = "#2EE6D6"       # NIS door (distinct from BLUE #58C4DD and GREEN #83C167)
PINK = "#FF7EB6"       # MCT8 transporter (distinct from MAGENTA)
MAGENTA = "#E040FB"    # TSH from the pituitary
PURPLE = "#9A72AC"     # Deiodinase (D2)
ORANGE = "#FF862F"     # Radioactive iodine-123 tracer & scan glow

# Standard shared positions
GLAND_POS = np.array([-1.5, -0.15, 0.0])
VESSEL_X = 1.65
GAUGE_POS = np.array([4.35, -0.30, 0.0])

FOL_CENTER = np.array([-0.85, -0.15, 0.0])
FOL_R_IN = 1.35
FOL_R_OUT = 2.20
CAP_R_IN = 2.28
CAP_R_OUT = 2.80
CAP_R_MID = 2.54
N_CELLS = 10


def _tag():
    """Consistent schematic tag in bottom-right corner at full opacity."""
    return scope_tag("schematic", size=24, color=TEXT)


def build_thyroid_shape(center=GLAND_POS, height=4.9, stroke_color=GREY, stroke_width=3.5,
                        fill_color=ORANGE, fill_opacity=0.0):
    """Build a smooth butterfly-shaped two-lobed thyroid gland centered at `center`."""
    pts_raw = [
        (-0.55, 0.25), (-0.82, 1.05), (-1.42, 1.85), (-1.95, 1.25),
        (-2.05, -0.10), (-1.75, -1.55), (-1.12, -1.85), (-0.62, -0.95),
        (-0.42, -0.30), (0.00, -0.36), (0.42, -0.30), (0.62, -0.95),
        (1.12, -1.85), (1.75, -1.55), (2.05, -0.10), (1.95, 1.25),
        (1.42, 1.85), (0.82, 1.05), (0.55, 0.25), (0.00, 0.18),
    ]
    pts = [np.array([x, y, 0.0]) for x, y in pts_raw]
    poly = VMobject(stroke_color=stroke_color, stroke_width=stroke_width,
                    fill_color=fill_color, fill_opacity=fill_opacity)
    poly.set_points_smoothly(pts + [pts[0]])
    poly.scale(height / max(poly.height, 1e-6))
    poly.move_to(center)
    return poly


def build_glowing_gland(glow_tracker, center=GLAND_POS, height=4.9, nodule=False,
                        nodule_tracker=None, scale_tracker=None):
    """Return group of the two-lobed gland with ValueTracker-driven ORANGE scan glow."""
    sc = (lambda: scale_tracker.get_value()) if scale_tracker is not None else (lambda: 1.0)
    glow_fill = always_redraw(lambda: build_thyroid_shape(
        center=center, height=height * sc() * 0.96, stroke_color=ORANGE, stroke_width=0,
        fill_color=ORANGE, fill_opacity=float(np.clip(glow_tracker.get_value(), 0.0, 0.90))
    ))
    outline = always_redraw(lambda: build_thyroid_shape(
        center=center, height=height * sc(), stroke_color=GREY, stroke_width=3.5,
        fill_color=GREY, fill_opacity=0.10
    )) if scale_tracker is not None else build_thyroid_shape(
        center=center, height=height, stroke_color=GREY, stroke_width=3.5,
        fill_color=GREY, fill_opacity=0.10
    )
    g = VGroup(outline, glow_fill)
    if scale_tracker is None:
        # Draw outline above glow_fill for crisp border
        outline_top = build_thyroid_shape(center=center, height=height, stroke_color=GREY,
                                          stroke_width=3.5, fill_opacity=0.0)
        g.add(outline_top)
        g.outline = outline_top
    else:
        outline_top = always_redraw(lambda: build_thyroid_shape(
            center=center, height=height * sc(), stroke_color=GREY, stroke_width=3.5,
            fill_opacity=0.0
        ))
        g.add(outline_top)
        g.outline = outline_top

    if nodule and nodule_tracker is not None:
        nod_pos = center + np.array([height * 0.30, -height * 0.18, 0.0])
        nod_r = height * 0.13
        nod = always_redraw(lambda: Circle(
            radius=nod_r, stroke_color=ORANGE, stroke_width=3.0,
            fill_color=ORANGE, fill_opacity=float(np.clip(nodule_tracker.get_value(), 0.05, 0.95)),
        ).move_to(nod_pos))
        g.add(nod)
        g.nodule = nod
        g.nodule_pos = nod_pos
        g.nodule_r = nod_r
    return g


def build_vessel(x=VESSEL_X, y_bot=-2.70, y_top=2.60, width=0.56):
    """Vertical GREY blood vessel beside the gland."""
    left_wall = Line([x - width / 2, y_bot, 0], [x - width / 2, y_top, 0], color=GREY, stroke_width=3.0)
    right_wall = Line([x + width / 2, y_bot, 0], [x + width / 2, y_top, 0], color=GREY, stroke_width=3.0)
    fill = Rectangle(width=width, height=y_top - y_bot, stroke_width=0,
                     fill_color=GREY, fill_opacity=0.16).move_to([x, (y_bot + y_top) / 2, 0])
    g = VGroup(fill, left_wall, right_wall)
    g.x, g.y_bot, g.y_top, g.width = x, y_bot, y_top, width
    return g


def make_vessel_stream(x=VESSEL_X, y_bot=-2.60, y_top=2.50, width=0.42,
                       n_blue=11, n_yellow=0, n_orange=0, speed=0.22, seed=7,
                       blue_scale_fn=None):
    """Continuous deterministic stream of dots flowing upward in the vertical vessel."""
    rng = np.random.default_rng(seed)
    specs = []
    items = [(BLUE, n_blue, 0.090)] + [(YELLOW, n_yellow, 0.072)] + [(ORANGE, n_orange, 0.075)]
    for col, count, rad in items:
        for _ in range(count):
            specs.append((col, float(rng.uniform(0.0, 1.0)),
                          float(rng.uniform(-width * 0.34, width * 0.34)),
                          float(rng.uniform(0.85, 1.15)), rad))
    t_acc = [0.0]

    def build_dots():
        g = VGroup()
        sc_b = blue_scale_fn() if blue_scale_fn is not None else 1.0
        for col, u0, dx, sp, rad in specs:
            u = (u0 + speed * sp * t_acc[0]) % 1.0
            y = y_bot + u * (y_top - y_bot)
            r = rad * (sc_b if col == BLUE else 1.0)
            g.add(Dot([x + dx, y, 0], radius=r, color=col))
        return g

    mob = always_redraw(build_dots)
    mob._t_acc = t_acc
    mob.add_updater(lambda m, dt: t_acc.__setitem__(0, t_acc[0] + dt))
    mob.layout_ok = True   # blood-stream dots inside vessel walls
    return mob


def build_hormone_gauge(tracker, center=GAUGE_POS, radius=1.22, label="blood hormone",
                        hidden_tracker=None):
    """Schematic half-circle gauge with BLUE needle/arc, NO numbers, optional '?' cover."""
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=10)
    v = lambda: float(np.clip(tracker.get_value(), 0.02, 0.98))
    val_arc = always_redraw(lambda: Arc(
        radius=radius, start_angle=PI, angle=-PI * v(), arc_center=c, stroke_color=BLUE, stroke_width=10
    ))
    needle = always_redraw(lambda: Line(
        c, c + 0.80 * radius * np.array([np.cos(PI - PI * v()), np.sin(PI - PI * v()), 0]),
        color=BLUE, stroke_width=5.5
    ))
    hub = Dot(c, radius=0.08, color=TEXT)
    lbl = T(label, 28, TEXT).move_to(c + DOWN * 0.65)
    g = VGroup(track, val_arc, needle, hub, lbl)
    g.gauge_center = c
    g.label_mob = lbl

    if hidden_tracker is not None:
        def mk_cover():
            op = float(np.clip(hidden_tracker.get_value(), 0.0, 1.0))
            if op < 0.02:
                return VGroup()
            dy = (1.0 - op) * 0.95
            disc_r = radius * 0.56
            disc_c = c + UP * (0.48 * radius + dy)
            disc = Circle(radius=disc_r, stroke_color=YELLOW, stroke_width=2.5 * op,
                          fill_color=BG, fill_opacity=0.96 * op).move_to(disc_c)
            q = T("?", 48, YELLOW, weight=BOLD).set_opacity(op).move_to(disc)
            return VGroup(disc, q)
        cover = always_redraw(mk_cover)
        g.add(cover)
        g.cover = cover
    return g


def build_follicle(center=FOL_CENTER, r_in=FOL_R_IN, r_out=FOL_R_OUT, n_cells=N_CELLS,
                   colloid_glow=None, highlight_cell=None, nis_doors=False):
    """Build the 10-cell thyroid follicle ring + colloid lumen + optional NIS doors."""
    c = np.array(center, dtype=float)
    if colloid_glow is not None:
        lumen = always_redraw(lambda: Circle(
            radius=r_in, stroke_width=0,
            fill_color=ORANGE if colloid_glow.get_value() > 0.08 else GREY,
            fill_opacity=max(0.20, float(np.clip(colloid_glow.get_value(), 0.0, 0.85)))
        ).move_to(c))
    else:
        lumen = Circle(radius=r_in, stroke_width=0, fill_color=GREY, fill_opacity=0.20).move_to(c)

    cells = VGroup()
    cell_centers = []
    cell_angles = []
    d_theta = TAU / n_cells
    for k in range(n_cells):
        ang = (k + 0.5) * d_theta
        cell_angles.append(ang)
        r_mid = 0.5 * (r_in + r_out)
        cell_centers.append(c + r_mid * np.array([np.cos(ang), np.sin(ang), 0.0]))
        a0 = k * d_theta + 0.025
        a1 = (k + 1) * d_theta - 0.025
        is_hi = (highlight_cell == k)
        stroke_col = TEXT if is_hi else GREY
        stroke_w = 3.5 if is_hi else 2.5
        fill_op = 0.22 if is_hi else 0.13
        sector = AnnularSector(
            inner_radius=r_in, outer_radius=r_out, angle=a1 - a0, start_angle=a0,
            arc_center=c, stroke_color=stroke_col, stroke_width=stroke_w,
            fill_color=GREY, fill_opacity=fill_op
        )
        cells.add(sector)

    doors = VGroup()
    if nis_doors:
        for ang in cell_angles:
            doors.add(_make_door(c + r_out * np.array([np.cos(ang), np.sin(ang), 0.0]), ang, CYAN))

    g = VGroup(lumen, cells, doors)
    g.lumen = lumen
    g.cells = cells
    g.doors = doors
    g.cell_centers = cell_centers
    g.cell_angles = cell_angles
    g.center_pt = c
    return g


def _make_door(pos, radial_angle, color=CYAN, width=0.22):
    """Two short parallel channel bars oriented radially across the membrane at `pos`."""
    r_hat = np.array([np.cos(radial_angle), np.sin(radial_angle), 0.0])
    t_hat = np.array([-np.sin(radial_angle), np.cos(radial_angle), 0.0])
    half_len = 0.12
    sep = width * 0.55
    b1 = Line(pos - r_hat * half_len + t_hat * sep, pos + r_hat * half_len + t_hat * sep,
              color=color, stroke_width=4.5)
    b2 = Line(pos - r_hat * half_len - t_hat * sep, pos + r_hat * half_len - t_hat * sep,
              color=color, stroke_width=4.5)
    gap = Line(pos - t_hat * sep * 0.7, pos + t_hat * sep * 0.7, color=BG, stroke_width=5.0)
    return VGroup(gap, b1, b2)


def build_capillary(center=FOL_CENTER, r_in=CAP_R_IN, r_out=CAP_R_OUT):
    """Curving capillary wrapping around the follicle with clean left inlet and right downward outlet."""
    c = np.array(center, dtype=float)
    r_mid = 0.5 * (r_in + r_out)
    w = r_out - r_in
    ang_in = np.arcsin(np.clip(w * 0.48 / r_out, 0.0, 0.9))
    ang_in_i = np.arcsin(np.clip(w * 0.48 / r_in, 0.0, 0.9))
    # Left horizontal inlet meeting circular ring smoothly
    x_in_out = c[0] - r_out * np.cos(ang_in)
    y_in_top = c[1] + r_out * np.sin(ang_in)
    y_in_bot = c[1] - r_out * np.sin(ang_in)
    inlet_top = Line([-6.5, y_in_top, 0], [x_in_out, y_in_top, 0], color=GREY, stroke_width=3.0)
    inlet_bot = Line([-6.5, y_in_bot, 0], [x_in_out, y_in_bot, 0], color=GREY, stroke_width=3.0)

    # Outer arcs: top goes from PI - ang_in down to 0.0; bottom goes from -PI + ang_in up to -ang_in_i
    arc_top_out = Arc(radius=r_out, start_angle=PI - ang_in, angle=-(PI - ang_in),
                      arc_center=c, color=GREY, stroke_width=3.0)
    arc_top_in = Arc(radius=r_in, start_angle=PI - ang_in_i, angle=-(PI - ang_in_i),
                     arc_center=c, color=GREY, stroke_width=3.0)
    ang_bot_end = 0.22
    ang_junc = np.arccos(r_in / r_out)
    arc_bot_out = Arc(radius=r_out, start_angle=-PI + ang_in, angle=(PI - ang_in - ang_junc),
                      arc_center=c, color=GREY, stroke_width=3.0)
    arc_bot_in = Arc(radius=r_in, start_angle=-PI + ang_in_i, angle=(PI - ang_in_i - ang_bot_end),
                     arc_center=c, color=GREY, stroke_width=3.0)

    # Downward outlet tangent at right
    outlet_r = Line([c[0] + r_out, c[1], 0], [c[0] + r_out, -3.55, 0], color=GREY, stroke_width=3.0)
    outlet_l = Line([c[0] + r_in, c[1] - r_out * np.sin(ang_junc), 0],
                    [c[0] + r_in, -3.55, 0], color=GREY, stroke_width=3.0)

    ring_fill = Annulus(inner_radius=r_in, outer_radius=r_out, arc_center=c,
                        stroke_width=0, fill_color=GREY, fill_opacity=0.14)
    inlet_fill = Rectangle(width=abs(x_in_out + 6.5), height=y_in_top - y_in_bot, stroke_width=0,
                           fill_color=GREY, fill_opacity=0.14).move_to([(-6.5 + x_in_out) / 2, c[1], 0])
    outlet_fill = Rectangle(width=w, height=abs(c[1] + 3.55), stroke_width=0,
                            fill_color=GREY, fill_opacity=0.14).move_to([c[0] + r_mid, (c[1] - 3.55) / 2, 0])
    cap_fill = Union(ring_fill, inlet_fill, outlet_fill,
                     stroke_width=0, fill_color=GREY, fill_opacity=0.14)
    return VGroup(cap_fill,
                  inlet_top, inlet_bot, arc_top_out, arc_top_in, arc_bot_out, arc_bot_in, outlet_l, outlet_r)


def cap_path_point(u, branch=1, lane=0.0, center=FOL_CENTER, r_mid=CAP_R_MID):
    """Map u in [0, 1] along the capillary: left inlet -> upper/lower arc -> lower-right outlet."""
    c = np.array(center, dtype=float)
    r = r_mid + lane
    if u < 0.24:
        f = u / 0.24
        x = -6.4 + f * ((c[0] - r) - (-6.4))
        return np.array([x, c[1] + lane * 0.7, 0.0])
    elif u < 0.78:
        f = (u - 0.24) / 0.54
        ang = PI - f * PI if branch >= 0 else -PI + f * PI
        return c + r * np.array([np.cos(ang), np.sin(ang), 0.0])
    else:
        f = (u - 0.78) / 0.22
        y = c[1] + f * (-3.50 - c[1])
        return np.array([c[0] + r, y, 0.0])


def make_capillary_stream(n_yellow_tracker=None, n_yellow=10, n_orange=0, n_blue=6,
                          speed=0.16, seed=11, center=FOL_CENTER, r_mid=CAP_R_MID):
    """Continuous deterministic stream of dots flowing along the curving capillary."""
    rng = np.random.default_rng(seed)
    max_y = 48
    yellow_specs = [(float(rng.uniform(0, 1)), 1 if i % 2 == 0 else -1,
                     float(rng.uniform(-0.14, 0.14)), float(rng.uniform(0.85, 1.15)))
                    for i in range(max_y)]
    orange_specs = [(float(rng.uniform(0, 1)), 1 if i % 2 == 0 else -1,
                     float(rng.uniform(-0.12, 0.12)), float(rng.uniform(0.9, 1.1)))
                    for i in range(max(n_orange, 12))]
    blue_specs = [(float(rng.uniform(0, 1)), 1 if i % 2 == 0 else -1,
                   float(rng.uniform(-0.14, 0.14)), float(rng.uniform(0.85, 1.15)))
                  for i in range(max(n_blue, 12))]
    t_acc = [0.0]

    def mk():
        g = VGroup()
        ny = int(round(n_yellow_tracker.get_value())) if n_yellow_tracker is not None else n_yellow
        ny = max(0, min(max_y, ny))
        for i in range(ny):
            u0, br, ln, sp = yellow_specs[i]
            u = (u0 + speed * sp * t_acc[0]) % 1.0
            g.add(Dot(cap_path_point(u, br, ln, center, r_mid), radius=0.082, color=YELLOW))
        for i in range(n_orange):
            u0, br, ln, sp = orange_specs[i]
            u = (u0 + speed * sp * t_acc[0]) % 1.0
            g.add(Dot(cap_path_point(u, br, ln, center, r_mid), radius=0.088, color=ORANGE))
        for i in range(n_blue):
            u0, br, ln, sp = blue_specs[i]
            u = (u0 + speed * sp * t_acc[0]) % 1.0
            g.add(Dot(cap_path_point(u, br, ln, center, r_mid), radius=0.092, color=BLUE))
        return g

    mob = always_redraw(mk)
    mob._t_acc = t_acc
    mob.add_updater(lambda m, dt: t_acc.__setitem__(0, t_acc[0] + dt))
    mob.layout_ok = True   # capillary dots inside vessel walls
    return mob


def make_trapping_dots(follicle, n_slots=10, orange_prob_fn=lambda: 0.0,
                       target_r=None, speed=0.48, seed=21):
    """Dots entering from capillary through CYAN NIS doors into follicle cells or colloid."""
    rng = np.random.default_rng(seed)
    r_dest = target_r if target_r is not None else 0.5 * (FOL_R_IN + FOL_R_OUT)
    slots = []
    for k in range(n_slots):
        ang = follicle.cell_angles[k % len(follicle.cell_angles)]
        phase0 = float(rng.uniform(0.0, 1.0))
        slots.append((ang, phase0, float(rng.uniform(-0.08, 0.08))))
    t_acc = [0.0]

    def mk():
        g = VGroup()
        p_or = float(np.clip(orange_prob_fn(), 0.0, 1.0))
        for idx, (ang, ph0, da) in enumerate(slots):
            raw = ph0 + speed * t_acc[0]
            cycle = int(np.floor(raw))
            f = raw - cycle
            r = CAP_R_MID + f * (r_dest - CAP_R_MID)
            val = ((idx * 7 + cycle * 13) % 100) / 100.0
            is_orange = val < p_or
            col = ORANGE if is_orange else YELLOW
            pos = follicle.center_pt + r * np.array([np.cos(ang + da), np.sin(ang + da), 0.0])
            g.add(Dot(pos, radius=0.074, color=col))
        return g

    mob = always_redraw(mk)
    mob.add_updater(lambda m, dt: t_acc.__setitem__(0, t_acc[0] + dt))
    mob.layout_ok = True   # trapping particles moving through NIS doors
    return mob


def build_thyroglobulin_strands(center=FOL_CENTER):
    """Plain wavy GREY protein strands inside the colloid (no molecular structure)."""
    c = np.array(center, dtype=float)
    strands = VGroup()
    offsets = [(-0.42, 0.48, 0.15), (0.35, 0.38, -0.20), (-0.30, -0.45, 0.35), (0.28, -0.35, -0.35)]
    for dx, dy, rot in offsets:
        pts = [
            c + np.array([dx - 0.36, dy + 0.08, 0.0]),
            c + np.array([dx - 0.12, dy - 0.10, 0.0]),
            c + np.array([dx + 0.12, dy + 0.10, 0.0]),
            c + np.array([dx + 0.36, dy - 0.06, 0.0]),
        ]
        s = VMobject(color=GREY, stroke_width=4.5).set_points_smoothly(pts)
        s.rotate(rot, about_point=c + np.array([dx, dy, 0.0]))
        strands.add(s)
    return strands


# ---------------------------------------------------------------------------
# SCENES
# ---------------------------------------------------------------------------

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        # Opening link-back: ghost of first film's tissue cell at left
        cell_box = RoundedRectangle(corner_radius=0.35, width=4.0, height=3.5,
                                    stroke_color=GREY, stroke_width=3.2,
                                    fill_color=GREY, fill_opacity=0.14).move_to([-2.3, 0.0, 0])
        cell_lbl = T("last time", 28, TEXT).next_to(cell_box, UP, buff=0.22)
        mct8_door = _make_door(cell_box.get_left(), PI, color=PINK, width=0.28)
        mct8_lbl = T("MCT8", 28, PINK).next_to(mct8_door, DOWN, buff=0.32).shift(LEFT * 0.72)
        d2_blob = RoundedRectangle(corner_radius=0.18, width=1.15, height=0.76,
                                   stroke_color=PURPLE, stroke_width=3.0,
                                   fill_color=PURPLE, fill_opacity=0.24).move_to(cell_box.get_center() + LEFT * 0.20)
        d2_lbl = T("D2", 28, PURPLE).move_to(d2_blob)
        t4_dot = Dot(cell_box.get_left() + LEFT * 1.4, radius=0.14, color=BLUE)
        t4_lbl = T("T4", 28, BLUE).next_to(t4_dot, UP, buff=0.18)

        ghost = VGroup(cell_box, cell_lbl, mct8_door, mct8_lbl, d2_blob, d2_lbl, t4_dot, t4_lbl)
        self.play(FadeIn(ghost), run_time=0.7)
        # Move T4 dot up to the left of D2 (clear of 'D2' box and letters), then transform to T3 at right
        d2_entry = d2_blob.get_left() + LEFT * 0.32
        self.play(t4_dot.animate.move_to(d2_entry),
                  t4_lbl.animate.next_to(d2_entry, UP, buff=0.26),
                  run_time=1.3)
        t3_start = d2_blob.get_right() + RIGHT * 0.16
        t3_end = d2_blob.get_right() + RIGHT * 1.15
        t3_lbl = T("T3", 28, GREEN).next_to(t3_end, UP, buff=0.22)
        t3_dot = Dot(t3_start, radius=0.14, color=GREEN)
        self.play(FadeOut(t4_dot), FadeIn(t3_dot), swap(t4_lbl, t3_lbl, run_time=0.5), run_time=0.6)
        self.play(t3_dot.animate.move_to(t3_end), run_time=0.7)

        # Swing to the neck: two-lobed thyroid + blood vessel (fade ALL link-back items including t3_lbl, t3_dot!)
        self.at("built in the gland")
        glow = ValueTracker(0.0)
        gland = build_glowing_gland(glow, center=GLAND_POS, height=4.9)
        vessel = build_vessel()
        stream = make_vessel_stream(n_blue=12, speed=0.22, seed=1)
        gland_lbl = T("thyroid gland", 28, TEXT).next_to(gland, DOWN, buff=0.22)

        self.play(FadeOut(ghost), FadeOut(t3_lbl), FadeOut(t3_dot),
                  FadeIn(gland), FadeIn(vessel), FadeIn(gland_lbl), run_time=1.0)
        self.add(stream)

        # Thyroid scan glowing ORANGE
        self.at("thyroid scan")
        self.play(glow.animate.set_value(0.68), run_time=1.6)
        glow_phase = [0.0]

        def breathe(t_mob, dt):
            glow_phase[0] += dt
            glow.set_value(0.68 + 0.08 * np.sin(2.4 * glow_phase[0]))

        self.add(VMobject().add_updater(breathe))

        # Question + blood hormone gauge hidden behind '?'
        self.at("bright gland")
        q_text = T("Bright = more hormone?", 38, TEXT, weight=BOLD).move_to([-0.5, 3.05, 0])
        h_val = ValueTracker(0.55)
        h_hide = ValueTracker(1.0)
        gauge = build_hormone_gauge(h_val, center=GAUGE_POS, hidden_tracker=h_hide)
        self.play(FadeIn(q_text), FadeIn(gauge), run_time=0.9)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Thyroid Hormone: Tissues Decide What T4 Becomes"
    TITLE = "What the Scan Sees"


class S02Follicle(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        glow_mac = ValueTracker(0.60)
        gland_mac = build_glowing_gland(glow_mac, center=GLAND_POS, height=4.9)
        self.add(gland_mac)

        fol = build_follicle(center=FOL_CENTER, nis_doors=False)
        cap = build_capillary(center=FOL_CENTER)
        cap_stream = make_capillary_stream(n_yellow=11, n_blue=6, speed=0.16, seed=2)

        colloid_lbl = T("colloid", 28, TEXT).move_to(FOL_CENTER)
        blood_lbl = T("blood", 28, TEXT).move_to([-4.65, FOL_CENTER[1] + 0.90, 0])

        self.play(glow_mac.animate.set_value(0.12), gland_mac.animate.scale(2.4).set_opacity(0.0),
                  FadeIn(cap), FadeIn(fol), run_time=1.6)
        self.remove(gland_mac)
        self.add(cap_stream)
        self.play(FadeIn(blood_lbl), run_time=0.6)

        self.at("the colloid")
        self.play(FadeIn(colloid_lbl), run_time=0.6)

        self.at("faces blood")
        outer_arcs = VGroup(*[
            Arc(radius=FOL_R_OUT, start_angle=k * TAU / N_CELLS + 0.03,
                angle=TAU / N_CELLS - 0.06, arc_center=FOL_CENTER,
                color=TEXT, stroke_width=6.0)
            for k in range(N_CELLS)
        ])
        self.play(FadeIn(outer_arcs), run_time=0.7)

        self.at("colloid on the other")
        inner_arcs = VGroup(*[
            Arc(radius=FOL_R_IN, start_angle=k * TAU / N_CELLS + 0.03,
                angle=TAU / N_CELLS - 0.06, arc_center=FOL_CENTER,
                color=TEXT, stroke_width=6.0)
            for k in range(N_CELLS)
        ])
        self.play(FadeOut(outer_arcs), FadeIn(inner_arcs), run_time=0.7)

        self.at("on the blood side")
        doors = VGroup(*[_make_door(FOL_CENTER + FOL_R_OUT * np.array([np.cos(a), np.sin(a), 0]), a, CYAN)
                         for a in fol.cell_angles])
        nis_lbl = T("NIS", 28, CYAN).move_to([2.65, 1.55, 0])
        nis_ptr = Arrow(nis_lbl.get_left() + LEFT * 0.08,
                        FOL_CENTER + (FOL_R_OUT + 0.08) * np.array([np.cos(fol.cell_angles[0]), np.sin(fol.cell_angles[0]), 0]),
                        buff=0.05, color=CYAN, stroke_width=3.0, max_tip_length_to_length_ratio=0.18)
        self.play(FadeOut(inner_arcs), FadeIn(doors), FadeIn(nis_lbl), GrowArrow(nis_ptr), run_time=0.8)

        self.at("pulls iodide in")
        trap = make_trapping_dots(fol, n_slots=10, orange_prob_fn=lambda: 0.0,
                                  target_r=0.5 * (FOL_R_IN + FOL_R_OUT), speed=0.55, seed=21)
        self.add(trap)
        self.finish()


class S03Build(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        hi_idx = 9
        hi_ang = (hi_idx + 0.5) * TAU / N_CELLS
        fol = build_follicle(center=FOL_CENTER, highlight_cell=hi_idx, nis_doors=True)
        cap = build_capillary(center=FOL_CENTER)
        cap_stream = make_capillary_stream(n_yellow=11, n_blue=6, speed=0.18, seed=3)

        strands = build_thyroglobulin_strands(center=FOL_CENTER)
        blood_lbl = T("blood", 28, TEXT).move_to([-4.65, FOL_CENTER[1] + 0.90, 0])
        nis_lbl = T("NIS", 28, CYAN).move_to([2.65, 1.65, 0])
        nis_ptr = Arrow(nis_lbl.get_left() + LEFT * 0.08,
                        FOL_CENTER + (FOL_R_OUT + 0.08) * np.array([np.cos(fol.cell_angles[0]), np.sin(fol.cell_angles[0]), 0]),
                        buff=0.05, color=CYAN, stroke_width=3.0, max_tip_length_to_length_ratio=0.18)

        self.add(cap, fol, cap_stream, blood_lbl, nis_lbl, nis_ptr)

        r_vec = np.array([np.cos(hi_ang), np.sin(hi_ang), 0.0])
        apical_pt = FOL_CENTER + FOL_R_IN * r_vec
        basal_pt = FOL_CENTER + FOL_R_OUT * r_vec
        iodides = VGroup(*[
            Dot(basal_pt - r_vec * (0.15 + 0.08 * i) + np.array([-r_vec[1], r_vec[0], 0]) * ((i - 1) * 0.14),
                radius=0.075, color=YELLOW)
            for i in range(4)
        ])
        self.play(FadeIn(iodides), run_time=0.4)
        self.play(*[d.animate.move_to(apical_pt + r_vec * 0.12 + np.array([-r_vec[1], r_vec[0], 0]) * ((i - 1.5) * 0.12))
                    for i, d in enumerate(iodides)], run_time=1.0)

        # TPO spark at colloid face + thyroglobulin strands
        self.at("the enzyme")
        tpo_spark = Star(n=6, outer_radius=0.15, inner_radius=0.06, color=TEXT,
                         fill_color=TEXT, fill_opacity=0.95).move_to(apical_pt)
        tpo_lbl = T("TPO", 28, TEXT).move_to([2.65, 0.55, 0])
        tpo_ptr = Arrow(tpo_lbl.get_left() + LEFT * 0.08, apical_pt + RIGHT * 0.12,
                        buff=0.05, color=TEXT, stroke_width=2.5, max_tip_length_to_length_ratio=0.14)
        self.play(FadeIn(tpo_spark), FadeIn(tpo_lbl), GrowArrow(tpo_ptr), run_time=0.8)
        self.play(Create(strands), run_time=1.8)

        # Label thyroglobulin and attach yellow iodide dots sequentially across strands
        self.at("large protein")
        tg_lbl = T("thyroglobulin", 28, TEXT).move_to([-4.45, 2.05, 0])
        tg_ptr = Arrow(tg_lbl.get_right() + RIGHT * 0.08, strands[0].get_top() + LEFT * 0.1,
                       buff=0.05, color=GREY, stroke_width=2.8, max_tip_length_to_length_ratio=0.15)
        self.play(FadeIn(tg_lbl), GrowArrow(tg_ptr), run_time=0.7)
        for i, d in enumerate(iodides):
            self.play(d.animate.move_to(strands[i % len(strands)].get_center()), run_time=0.65)

        # Short segments on strands couple sequentially into BLUE T4 and GREEN T3
        self.at("join into")
        segs = VGroup()
        seg_cols = [BLUE, BLUE, BLUE, GREEN, BLUE, GREEN]
        for i, col in enumerate(seg_cols):
            st = strands[i % len(strands)]
            p0 = st.point_from_proportion(0.20 if i < 4 else 0.60)
            p1 = st.point_from_proportion(0.48 if i < 4 else 0.88)
            segs.add(Line(p0, p1, color=col, stroke_width=9.5))
        t4_key = T("T4", 28, BLUE).move_to([2.65, -2.55, 0])
        t3_key = T("T3", 28, GREEN).next_to(t4_key, RIGHT, buff=0.45)
        self.play(FadeOut(iodides), FadeIn(t4_key), FadeIn(t3_key), run_time=0.5)
        for seg in segs:
            self.play(Create(seg), run_time=0.55)

        # MAGENTA TSH arrow reaches blood face
        self.at("driven by")
        tsh_start = np.array([5.8, -0.55, 0.0])
        tsh_end = basal_pt + r_vec * 0.68
        tsh_arrow = Arrow(tsh_start, tsh_end, buff=0.05, color=MAGENTA, stroke_width=5.5)
        tsh_lbl = T("TSH", 28, MAGENTA).next_to(tsh_arrow, UP, buff=0.14)
        self.play(GrowArrow(tsh_arrow), FadeIn(tsh_lbl), run_time=1.0)

        # Cell takes a colloid vesicle back in and digests it
        self.at("takes colloid")
        ves_pos = apical_pt - r_vec * 0.25
        vesicle = Circle(radius=0.30, color=GREY, stroke_width=2.5,
                         fill_color=GREY, fill_opacity=0.28).move_to(ves_pos)
        ves_dots = VGroup(
            Dot(ves_pos + UP * 0.08 + LEFT * 0.08, radius=0.070, color=BLUE),
            Dot(ves_pos + DOWN * 0.08 + LEFT * 0.04, radius=0.070, color=BLUE),
            Dot(ves_pos + UP * 0.04 + RIGHT * 0.09, radius=0.070, color=BLUE),
            Dot(ves_pos + DOWN * 0.07 + RIGHT * 0.08, radius=0.065, color=GREEN),
        )
        ves_grp = VGroup(vesicle, ves_dots)
        cell_mid = FOL_CENTER + 0.5 * (FOL_R_IN + FOL_R_OUT) * r_vec
        self.play(FadeIn(ves_grp), run_time=0.4)
        self.play(ves_grp.animate.move_to(cell_mid), run_time=0.7)
        self.play(vesicle.animate.scale(0.15).set_opacity(0.0), run_time=0.5)
        self.remove(vesicle)

        # Mostly T4 (and a few T3) exit via PINK MCT8 doors into blood; fade TPO & thyroglobulin labels
        self.at("mostly")
        mct_pos = FOL_CENTER + FOL_R_OUT * np.array([np.cos(hi_ang - 0.14), np.sin(hi_ang - 0.14), 0.0])
        mct_door = _make_door(mct_pos, hi_ang - 0.14, PINK, width=0.22)
        mct_lbl = T("MCT8", 28, PINK).move_to([2.90, -1.60, 0])
        mct_ptr = Arrow(mct_lbl.get_left() + LEFT * 0.08, mct_pos + RIGHT * 0.12,
                        buff=0.05, color=PINK, stroke_width=2.8, max_tip_length_to_length_ratio=0.16)
        self.play(FadeIn(mct_door), FadeIn(mct_lbl), GrowArrow(mct_ptr),
                  FadeOut(tpo_lbl), FadeOut(tpo_ptr), FadeOut(tpo_spark),
                  FadeOut(tg_lbl), FadeOut(tg_ptr),
                  run_time=0.8)

        out_dots = VGroup(
            Dot(cell_mid, radius=0.080, color=BLUE),
            Dot(cell_mid + UP * 0.1, radius=0.080, color=BLUE),
            Dot(cell_mid + DOWN * 0.1, radius=0.080, color=BLUE),
            Dot(cell_mid + LEFT * 0.08, radius=0.072, color=GREEN),
        )
        self.play(FadeOut(ves_dots), FadeIn(out_dots), run_time=0.2)
        exit_pt = FOL_CENTER + CAP_R_MID * np.array([np.cos(hi_ang - 0.14), np.sin(hi_ang - 0.14), 0.0])
        self.play(*[d.animate.move_to(exit_pt + np.array([0.08 * (i - 1.5), -0.35 * i, 0]))
                    for i, d in enumerate(out_dots)], run_time=1.3)
        self.play(out_dots.animate.shift(DOWN * 1.4).set_opacity(0.0), run_time=1.2)
        self.finish()


class S04Tracer(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        colloid_glow = ValueTracker(0.0)
        fol = build_follicle(center=FOL_CENTER, colloid_glow=colloid_glow, nis_doors=True)
        cap = build_capillary(center=FOL_CENTER)
        blood_lbl = T("blood", 28, TEXT).move_to([-4.65, FOL_CENTER[1] + 0.90, 0])
        nis_lbl = T("NIS", 28, CYAN).move_to([2.65, 1.55, 0])
        nis_ptr = Arrow(nis_lbl.get_left() + LEFT * 0.08,
                        FOL_CENTER + (FOL_R_OUT + 0.08) * np.array([np.cos(fol.cell_angles[0]), np.sin(fol.cell_angles[0]), 0]),
                        buff=0.05, color=CYAN, stroke_width=3.0, max_tip_length_to_length_ratio=0.18)

        n_orange_cap = [0]
        p_orange_trap = [0.0]
        rng = np.random.default_rng(4)
        y_specs = [(float(rng.uniform(0, 1)), 1 if i % 2 == 0 else -1,
                    float(rng.uniform(-0.14, 0.14)), float(rng.uniform(0.85, 1.15))) for i in range(11)]
        o_specs = [(float(rng.uniform(0, 1)), 1 if i % 2 == 0 else -1,
                    float(rng.uniform(-0.10, 0.10)), float(rng.uniform(0.90, 1.10))) for i in range(6)]
        t_acc = [0.0]

        def mk_stream():
            g = VGroup()
            for u0, br, ln, sp in y_specs:
                u = (u0 + 0.17 * sp * t_acc[0]) % 1.0
                g.add(Dot(cap_path_point(u, br, ln), radius=0.072, color=YELLOW))
            for i in range(n_orange_cap[0]):
                u0, br, ln, sp = o_specs[i]
                u = (u0 + 0.17 * sp * t_acc[0]) % 1.0
                g.add(Dot(cap_path_point(u, br, ln), radius=0.082, color=ORANGE))
            return g

        stream = always_redraw(mk_stream)
        stream.add_updater(lambda m, dt: t_acc.__setitem__(0, t_acc[0] + dt))
        stream.layout_ok = True

        # Ordinary iodide already trapping via NIS from t=0
        trap = make_trapping_dots(fol, n_slots=10, orange_prob_fn=lambda: p_orange_trap[0],
                                  target_r=0.95, speed=0.52, seed=41)

        self.add(cap, fol, stream, trap, blood_lbl, nis_lbl, nis_ptr)

        # CYAN NIS doors pulse on "borrows the first step"
        self.at("borrows the")
        self.play(fol.doors.animate.set_stroke(width=8.5), run_time=0.5, rate_func=there_and_back)

        # ORANGE tracer dots appear in capillary and mix with ordinary iodide
        self.at("radioactive iodine")
        n_orange_cap[0] = 6
        tracer_lbl = T("tracer (iodine-123)", 28, ORANGE).move_to([3.95, 2.55, 0])
        tracer_dot_icon = Dot(tracer_lbl.get_left() + LEFT * 0.25, radius=0.095, color=ORANGE)
        self.play(FadeIn(tracer_lbl), FadeIn(tracer_dot_icon), run_time=0.8)
        # Keep doors pulsing softly as tracer arrives before "carries it in"
        self.play(fol.doors.animate.set_stroke(width=7.5), run_time=1.0, rate_func=there_and_back)

        # NIS carries tracer + ordinary iodide into colloid, making colloid glow ORANGE
        self.at("carries it in")
        p_orange_trap[0] = 0.38
        self.play(colloid_glow.animate.set_value(0.54), run_time=2.8)

        # Clock sweeps "Hours later", pull back to whole two-lobed gland under scan camera
        self.at("hours later")
        clock_c = np.array([-5.3, 2.7, 0.0])
        clock_ring = Circle(radius=0.44, color=TEXT, stroke_width=3.0).move_to(clock_c)
        clock_hand = Line(clock_c, clock_c + UP * 0.32, color=GOLD, stroke_width=4.0)
        clock_lbl = T("hours later", 26, TEXT).next_to(clock_ring, RIGHT, buff=0.20)
        self.play(FadeIn(clock_ring), FadeIn(clock_hand), FadeIn(clock_lbl), run_time=0.3)
        self.play(Rotate(clock_hand, angle=-TAU * 0.75, about_point=clock_c), run_time=1.3)

        micro_grp = VGroup(cap, fol, blood_lbl, nis_lbl, nis_ptr, tracer_lbl, tracer_dot_icon)
        mac_glow = ValueTracker(0.54)
        gland = build_glowing_gland(mac_glow, center=GLAND_POS + DOWN * 0.25, height=4.2)
        vessel = build_vessel(y_bot=-2.8, y_top=2.0)
        v_stream = make_vessel_stream(y_bot=-2.7, y_top=1.9, n_blue=8, n_yellow=4, n_orange=2, speed=0.22, seed=42)

        cam_head = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.3, height=0.52, stroke_color=GREY,
                             stroke_width=3.0, fill_color=GREY, fill_opacity=0.24),
            Rectangle(width=1.7, height=0.15, stroke_width=0, fill_color=TEXT, fill_opacity=0.35).shift(DOWN * 0.26),
        ).move_to([GLAND_POS[0], 3.9, 0.0])
        cam_lbl = T("scan camera", 28, TEXT).next_to(cam_head, RIGHT, buff=0.25)

        self.remove(stream, trap)
        self.play(FadeOut(micro_grp), FadeIn(gland), FadeIn(vessel), run_time=0.8)
        self.add(v_stream)
        self.play(cam_head.animate.move_to([GLAND_POS[0], 2.55, 0.0]),
                  cam_lbl.animate.move_to([GLAND_POS[0] + 2.45, 2.55, 0.0]),
                  run_time=0.8)

        self.at("and where")
        frac_lbl = T("fraction held", 28, ORANGE).move_to([4.35, 0.0, 0.0])
        self.play(mac_glow.animate.set_value(0.75), FadeIn(frac_lbl), run_time=0.9)
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        head = T("Uptake = tracer held", 34, TEXT, weight=BOLD).move_to([0.0, HEAD_Y, 0.0])
        self.add(head)

        left_center = np.array([-3.2, 0.45, 0.0])
        mac_glow = ValueTracker(0.70)
        gland = build_glowing_gland(mac_glow, center=left_center, height=4.2)

        # Small active inset follicle at the gland's upper-left edge
        inset_c = np.array([-5.25, 1.55, 0.0])
        inset_ring = Circle(radius=0.72, color=GREY, stroke_width=2.8, fill_color=ORANGE, fill_opacity=0.36).move_to(inset_c)
        inset_doors = VGroup(
            _make_door(inset_c + UP * 0.72, PI / 2, CYAN, width=0.16),
            _make_door(inset_c + LEFT * 0.72, PI, CYAN, width=0.16),
            _make_door(inset_c + DOWN * 0.72, -PI / 2, CYAN, width=0.16),
        )
        inset_strands = VGroup(
            Line(inset_c + [-0.30, 0.14, 0], inset_c + [0.30, 0.10, 0], color=GREY, stroke_width=3.8),
            Line(inset_c + [-0.26, -0.14, 0], inset_c + [0.28, -0.10, 0], color=GREY, stroke_width=3.8),
        )
        t_in = [0.0]

        def mk_inset_dots():
            g = VGroup()
            dirs = [UP, LEFT, DOWN]
            for i, d in enumerate(dirs):
                f = (t_in[0] * 0.55 + i * 0.33) % 1.0
                p = inset_c + d * (0.95 - f * 0.60)
                col = ORANGE if i == 1 else YELLOW
                g.add(Dot(p, radius=0.055, color=col))
            return g

        inset_dots = always_redraw(mk_inset_dots)
        inset_dots.add_updater(lambda m, dt: t_in.__setitem__(0, t_in[0] + dt))
        inset_dots.layout_ok = True
        inset_grp = VGroup(inset_ring, inset_doors, inset_strands)

        divider = DashedLine([0.25, 2.6, 0], [0.25, -3.1, 0], color=GREY, stroke_width=2.5, dash_length=0.16)
        vessel = build_vessel(x=1.65, y_bot=-2.55, y_top=2.35)
        n_y_ves = [2]
        rng = np.random.default_rng(5)
        b_specs = [(float(rng.uniform(0, 1)), float(rng.uniform(-0.15, 0.15)), float(rng.uniform(0.85, 1.15))) for _ in range(11)]
        y_specs = [(float(rng.uniform(0, 1)), float(rng.uniform(-0.15, 0.15)), float(rng.uniform(0.85, 1.15))) for _ in range(12)]
        t_acc = [0.0]

        def mk_v():
            g = VGroup()
            for u0, dx, sp in b_specs:
                u = (u0 + 0.22 * sp * t_acc[0]) % 1.0
                g.add(Dot([1.65 + dx, -2.45 + u * 4.70, 0], radius=0.090, color=BLUE))
            for u0, dx, sp in y_specs[:n_y_ves[0]]:
                u = (u0 + 0.24 * sp * t_acc[0]) % 1.0
                g.add(Dot([1.65 + dx, -2.45 + u * 4.70, 0], radius=0.072, color=YELLOW))
            return g

        v_stream = always_redraw(mk_v)
        v_stream.add_updater(lambda m, dt: t_acc.__setitem__(0, t_acc[0] + dt))
        v_stream.layout_ok = True

        h_val = ValueTracker(0.55)
        h_hide = ValueTracker(1.0)
        gauge = build_hormone_gauge(h_val, center=[4.35, -0.15, 0], radius=1.20, hidden_tracker=h_hide)

        self.add(gland, inset_grp, inset_dots, vessel, v_stream, gauge)

        self.at("uptake reports")
        self.play(mac_glow.animate.set_value(0.78), run_time=0.8)

        s_y = [-1.98, -2.52, -3.06]
        l_trap = T("trapping", 28, CYAN).move_to([left_center[0], s_y[0], 0])
        l_fix = T("fixing iodine", 28, YELLOW).move_to([left_center[0], s_y[1], 0])
        l_sup = T("iodide supply", 28, YELLOW).move_to([left_center[0], s_y[2], 0])

        self.at("trapping")
        self.play(FadeIn(l_trap), inset_doors.animate.set_stroke(width=8.0), run_time=0.55)
        self.play(inset_doors.animate.set_stroke(width=4.5), run_time=0.3)

        self.at("fixing iodine")
        self.play(FadeIn(l_fix), inset_strands.animate.set_color(YELLOW), run_time=0.55)

        self.at("iodide supply")
        n_y_ves[0] = 10
        self.play(FadeIn(l_sup), run_time=0.7)

        self.at("does not measure")
        self.play(Create(divider), run_time=0.8)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        colloid_glow = ValueTracker(0.55)
        fol = build_follicle(center=FOL_CENTER, colloid_glow=colloid_glow, nis_doors=True)
        cap = build_capillary(center=FOL_CENTER)

        n_yellow = ValueTracker(8)
        cap_stream = make_capillary_stream(n_yellow_tracker=n_yellow, n_orange=4, n_blue=0,
                                           speed=0.16, seed=6)
        trap = make_trapping_dots(fol, n_slots=10, orange_prob_fn=lambda: 0.33,
                                  target_r=0.95, speed=0.48, seed=61)

        blood_lbl = T("blood", 28, TEXT).move_to([-4.65, FOL_CENTER[1] + 0.90, 0])
        nis_lbl = T("NIS", 28, CYAN).move_to([2.65, 1.55, 0])
        nis_ptr = Arrow(nis_lbl.get_left() + LEFT * 0.08,
                        FOL_CENTER + (FOL_R_OUT + 0.08) * np.array([np.cos(fol.cell_angles[0]), np.sin(fol.cell_angles[0]), 0]),
                        buff=0.05, color=CYAN, stroke_width=3.0, max_tip_length_to_length_ratio=0.18)

        self.add(cap, fol, cap_stream, trap, blood_lbl, nis_lbl, nis_ptr)

        self.at("ordinary iodide")
        iod_lbl = T("ordinary\niodide", 28, YELLOW).move_to([-5.05, -1.75, 0])
        self.play(FadeIn(iod_lbl), run_time=0.7)

        self.at("same doors")
        self.play(fol.doors.animate.set_stroke(width=8.5), run_time=0.45, rate_func=there_and_back)

        self.at("iodine load")
        load_lbl = T("iodine load", 28, YELLOW).move_to([-5.05, -1.75, 0])
        self.play(swap(iod_lbl, load_lbl, run_time=0.6),
                  n_yellow.animate.set_value(40), run_time=2.0)

        self.at("does uptake")
        q_card = question_card("Uptake: rise or fall?", y=3.20, color=TEXT, size=34)
        self.play(FadeIn(q_card), run_time=0.7)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Uptake: rise or fall?"
    CARD = {"y": 3.20, "color": TEXT, "size": 34}
    RING_AT = (5.8, -2.1, 0)
    SECONDS = 4.5

    def backdrop(self):
        colloid_glow = ValueTracker(0.55)
        fol = build_follicle(center=FOL_CENTER, colloid_glow=colloid_glow, nis_doors=True)
        cap = build_capillary(center=FOL_CENTER)
        n_yellow = ValueTracker(40)
        cap_stream = make_capillary_stream(n_yellow_tracker=n_yellow, n_orange=4, n_blue=0,
                                           speed=0.09, seed=6)
        blood_lbl = T("blood", 28, TEXT).move_to([-4.65, FOL_CENTER[1] + 0.90, 0])
        nis_lbl = T("NIS", 28, CYAN).move_to([2.65, 1.55, 0])
        nis_ptr = Arrow(nis_lbl.get_left() + LEFT * 0.08,
                        FOL_CENTER + (FOL_R_OUT + 0.08) * np.array([np.cos(fol.cell_angles[0]), np.sin(fol.cell_angles[0]), 0]),
                        buff=0.05, color=CYAN, stroke_width=3.0, max_tip_length_to_length_ratio=0.18)
        load_lbl = T("iodine load", 28, YELLOW).move_to([-5.05, -1.75, 0])
        return VGroup(cap, fol, cap_stream, blood_lbl, nis_lbl, nis_ptr, load_lbl, _tag())


class S08Answer(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        colloid_glow = ValueTracker(0.55)
        inset_glow = ValueTracker(0.55)
        n_yellow = ValueTracker(40)
        n_orange = 4

        fol = build_follicle(center=FOL_CENTER, colloid_glow=colloid_glow, nis_doors=True)
        cap = build_capillary(center=FOL_CENTER)
        cap_stream = make_capillary_stream(n_yellow_tracker=n_yellow, n_orange=n_orange, n_blue=0,
                                           speed=0.16, seed=6)
        trap = make_trapping_dots(
            fol, n_slots=10,
            orange_prob_fn=lambda: n_orange / max(n_orange + n_yellow.get_value(), 1.0),
            target_r=0.95, speed=0.48, seed=81
        )
        blood_lbl = T("blood", 28, TEXT).move_to([-4.65, FOL_CENTER[1] + 0.90, 0])
        load_lbl = T("iodine load", 28, YELLOW).move_to([-5.05, -1.75, 0])
        q_card = question_card("Uptake: rise or fall?", y=3.20, color=TEXT, size=34)

        inset = build_glowing_gland(inset_glow, center=[4.35, 2.00, 0], height=1.75)
        uptake_low_lbl = T("lower uptake", 28, ORANGE).move_to([4.35, 0.78, 0])

        self.add(cap, fol, cap_stream, trap, blood_lbl, load_lbl, q_card)

        self.at("it falls")
        self.play(FadeOut(q_card), FadeIn(inset), FadeIn(uptake_low_lbl),
                  colloid_glow.animate.set_value(0.14),
                  inset_glow.animate.set_value(0.14),
                  run_time=1.8)

        self.at("dilutes the tracer")
        self.wait(0.8)

        self.at("flip it")
        short_lbl = T("iodine short", 28, YELLOW).move_to([-5.05, -1.75, 0])
        uptake_hi_lbl = T("high uptake", 28, ORANGE).move_to([4.35, 0.78, 0])
        self.play(FadeOut(load_lbl), FadeOut(uptake_low_lbl), run_time=0.45)
        self.play(FadeIn(short_lbl), n_yellow.animate.set_value(2), run_time=2.0)

        self.at("uptake runs high")
        self.play(FadeIn(uptake_hi_lbl),
                  colloid_glow.animate.set_value(0.85),
                  inset_glow.animate.set_value(0.85),
                  run_time=1.4)

        self.at("yet blood")
        h_val = ValueTracker(0.55)
        h_hide = ValueTracker(1.0)
        gauge = build_hormone_gauge(h_val, center=[4.35, -1.10, 0], radius=1.15, hidden_tracker=h_hide)
        self.play(FadeIn(gauge), run_time=0.5)
        self.play(h_hide.animate.set_value(0.0), run_time=0.6)
        self.play(h_val.animate.set_value(0.18), run_time=1.4)
        self.finish()


class S09Nodule(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        lobe_glow = ValueTracker(0.45)
        nod_glow = ValueTracker(0.45)
        gland = build_glowing_gland(lobe_glow, center=GLAND_POS + DOWN * 0.15, height=4.4,
                                    nodule=True, nodule_tracker=nod_glow)
        vessel = build_vessel(x=VESSEL_X, y_bot=-2.75, y_top=2.15)
        blue_n = [8]
        rng = np.random.default_rng(9)
        b_specs = [(float(rng.uniform(0, 1)), float(rng.uniform(-0.15, 0.15)), float(rng.uniform(0.85, 1.15))) for _ in range(22)]
        y_specs = [(float(rng.uniform(0, 1)), float(rng.uniform(-0.15, 0.15)), float(rng.uniform(0.85, 1.15))) for _ in range(7)]
        o_specs = [(float(rng.uniform(0, 1)), float(rng.uniform(-0.15, 0.15)), float(rng.uniform(0.85, 1.15))) for _ in range(4)]
        t_acc = [0.0]

        def mk_v():
            g = VGroup()
            for u0, dx, sp in b_specs[:blue_n[0]]:
                u = (u0 + 0.22 * sp * t_acc[0]) % 1.0
                g.add(Dot([VESSEL_X + dx, -2.65 + u * 4.70, 0], radius=0.090, color=BLUE))
            for u0, dx, sp in y_specs:
                u = (u0 + 0.20 * sp * t_acc[0]) % 1.0
                g.add(Dot([VESSEL_X + dx, -2.65 + u * 4.70, 0], radius=0.068, color=YELLOW))
            for u0, dx, sp in o_specs:
                u = (u0 + 0.20 * sp * t_acc[0]) % 1.0
                g.add(Dot([VESSEL_X + dx, -2.65 + u * 4.70, 0], radius=0.072, color=ORANGE))
            return g

        stream = always_redraw(mk_v)
        stream.add_updater(lambda m, dt: t_acc.__setitem__(0, t_acc[0] + dt))
        stream.layout_ok = True

        cam_head = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.3, height=0.48, stroke_color=GREY,
                             stroke_width=3.0, fill_color=GREY, fill_opacity=0.24),
            Rectangle(width=1.7, height=0.14, stroke_width=0, fill_color=TEXT, fill_opacity=0.35).shift(DOWN * 0.24),
        ).move_to([GLAND_POS[0], 2.70, 0.0])
        cam_lbl = T("scan camera", 28, TEXT).next_to(cam_head, LEFT, buff=0.22)

        pit_pos = np.array([4.35, 2.55, 0.0])
        pit = Circle(radius=0.42, stroke_color=GREY, stroke_width=3.0,
                     fill_color=GREY, fill_opacity=0.22).move_to(pit_pos)
        pit_lbl = T("pituitary", 28, TEXT).next_to(pit, RIGHT, buff=0.18)

        tsh_strength = ValueTracker(1.0)
        tsh_arrow = always_redraw(lambda: Arrow(
            pit.get_left() + LEFT * 0.05 + DOWN * 0.15,
            GLAND_POS + np.array([1.25, 1.35, 0.0]),
            buff=0.05, color=MAGENTA,
            stroke_width=1.5 + 4.5 * tsh_strength.get_value(),
        ).set_opacity(0.15 + 0.85 * tsh_strength.get_value()))
        tsh_lbl = always_redraw(lambda: T("TSH", 28, MAGENTA).set_opacity(
            0.20 + 0.80 * tsh_strength.get_value()
        ).move_to([2.65, 2.45, 0.0]))

        h_val = ValueTracker(0.50)
        gauge = build_hormone_gauge(h_val, center=[4.35, -1.10, 0], radius=1.18)

        self.add(gland, vessel, stream, cam_head, cam_lbl, pit, pit_lbl, tsh_arrow, tsh_lbl, gauge)

        self.at("shows where")
        self.play(cam_head.animate.shift(DOWN * 0.12), run_time=0.45, rate_func=there_and_back)

        self.at("one nodule")
        blue_n[0] = 20
        nod_lbl = T("one bright nodule", 28, ORANGE).move_to([-0.9, -2.95, 0.0])
        nod_ptr = Arrow(nod_lbl.get_top() + UP * 0.06, gland.nodule_pos + DOWN * (gland.nodule_r + 0.08),
                        buff=0.04, color=ORANGE, stroke_width=3.0, max_tip_length_to_length_ratio=0.18)
        self.play(nod_glow.animate.set_value(0.92), h_val.animate.set_value(0.88),
                  FadeIn(nod_lbl), GrowArrow(nod_ptr), run_time=1.8)

        self.at("suppresses")
        fb_arrow = Arrow([VESSEL_X + 0.30, 1.15, 0.0], pit.get_bottom() + DOWN * 0.08,
                         buff=0.05, color=BLUE, stroke_width=4.5)
        self.play(GrowArrow(fb_arrow), tsh_strength.animate.set_value(0.0), run_time=1.8)

        self.at("takes up little")
        self.play(lobe_glow.animate.set_value(0.10), run_time=1.4)
        self.finish()


class S10ReadTogether(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        lobe_glow = ValueTracker(0.10)
        nod_glow = ValueTracker(0.92)
        gland = build_glowing_gland(lobe_glow, center=[-3.1, -0.15, 0], height=3.9,
                                    nodule=True, nodule_tracker=nod_glow)
        cam_head = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.0, height=0.42, stroke_color=GREY,
                             stroke_width=2.8, fill_color=GREY, fill_opacity=0.24),
            Rectangle(width=1.5, height=0.12, stroke_width=0, fill_color=TEXT, fill_opacity=0.35).shift(DOWN * 0.20),
        ).move_to([-3.1, 2.20, 0.0])
        scan_lbl = T("scan: where & uptake", 28, ORANGE).move_to([-3.1, -2.55, 0.0])

        rng = np.random.default_rng(10)
        in_specs = [(ORANGE if i % 3 == 0 else YELLOW, float(rng.uniform(0, 1)),
                     float(rng.uniform(-0.35, 0.35))) for i in range(9)]
        t_in = [0.0]

        def mk_in():
            g = VGroup()
            for col, u0, dy in in_specs:
                u = (u0 + 0.38 * t_in[0]) % 1.0
                x = -6.0 + u * 2.2
                y = -0.15 + dy * (1.0 - 0.5 * u)
                g.add(Dot([x, y, 0], radius=0.072, color=col))
            return g

        inflow = always_redraw(mk_in)
        inflow.add_updater(lambda m, dt: t_in.__setitem__(0, t_in[0] + dt))
        inflow.layout_ok = True

        vessel = build_vessel(x=1.55, y_bot=-2.05, y_top=1.95, width=0.50)
        v_stream = make_vessel_stream(x=1.55, y_bot=-1.95, y_top=1.85, width=0.38,
                                      n_blue=14, speed=0.22, seed=101)
        h_val = ValueTracker(0.88)
        gauge = build_hormone_gauge(h_val, center=[4.25, -0.05, 0], radius=1.22, label="blood hormone")

        self.add(gland, cam_head, scan_lbl, inflow, vessel, v_stream, gauge)

        self.at("read with the")
        b_left, b_right, b_y = -4.2, 5.2, 2.72
        bracket = VGroup(
            Line([b_left, b_y - 0.25, 0], [b_left, b_y, 0], color=TEXT, stroke_width=3.5),
            Line([b_left, b_y, 0], [b_right, b_y, 0], color=TEXT, stroke_width=3.5),
            Line([b_right, b_y, 0], [b_right, b_y - 0.25, 0], color=TEXT, stroke_width=3.5),
        )
        read_lbl = T("read together", 30, TEXT, weight=BOLD).next_to(bracket, UP, buff=0.14)
        self.play(Create(bracket), FadeIn(read_lbl), run_time=0.9)

        self.at("report the hormone")
        gauge_ring = Arc(radius=1.36, start_angle=PI, angle=-PI, arc_center=[4.25, -0.05, 0],
                         color=BLUE, stroke_width=6.0)
        self.play(FadeIn(gauge_ring), run_time=0.6)
        self.play(FadeOut(gauge_ring), run_time=0.6)

        self.at("what the gland")
        scan_hi = build_thyroid_shape(center=[-3.1, -0.15, 0], height=4.05,
                                      stroke_color=ORANGE, stroke_width=6.0, fill_opacity=0.0)
        self.play(FadeIn(scan_hi), nod_glow.animate.set_value(0.98), run_time=0.7)
        self.play(FadeOut(scan_hi), run_time=0.6)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        tag = _tag()
        self.add(tag)

        glow = ValueTracker(0.72)
        sc_tr = ValueTracker(1.0)
        gland = build_glowing_gland(glow, center=GLAND_POS, height=4.8, scale_tracker=sc_tr)
        vessel = build_vessel()
        pulse_scale = [1.0]
        stream = make_vessel_stream(n_blue=12, speed=0.22, seed=11, blue_scale_fn=lambda: pulse_scale[0])
        h_val = ValueTracker(0.55)
        gauge = build_hormone_gauge(h_val, center=GAUGE_POS)

        self.add(gland, vessel, gauge, stream)

        self.at("busy trap")
        edge_pts = [
            (GLAND_POS + np.array([-2.68, 0.55, 0]), PI),
            (GLAND_POS + np.array([-2.66, -0.25, 0]), PI),
            (GLAND_POS + np.array([-2.56, -1.00, 0]), PI),
        ]
        edge_doors = VGroup(*[_make_door(p, a, CYAN, width=0.20) for p, a in edge_pts])
        trap_lbl = T("NIS trap", 28, CYAN).move_to([-5.25, 1.55, 0.0])

        t_in = [0.0]

        def mk_edge_dots():
            g = VGroup()
            for i, (p, _) in enumerate(edge_pts):
                for j in range(2):
                    f = (t_in[0] * 0.65 + 0.35 * i + 0.5 * j) % 1.0
                    start = p + LEFT * 1.15
                    end = p + RIGHT * 0.45
                    col = ORANGE if (i + j) % 3 == 0 else YELLOW
                    g.add(Dot(start + f * (end - start), radius=0.074, color=col))
            return g

        edge_dots = always_redraw(mk_edge_dots)
        edge_dots.add_updater(lambda m, dt: t_in.__setitem__(0, t_in[0] + dt))
        edge_dots.layout_ok = True

        self.play(sc_tr.animate.set_value(1.06), FadeIn(edge_doors), FadeIn(trap_lbl), run_time=0.7)
        self.add(edge_dots)

        self.at("not a full")
        p_t = ValueTracker(0.0)

        def sync_pulse(m):
            pulse_scale[0] = 1.0 + 0.65 * np.sin(PI * p_t.get_value())

        p_hook = VMobject().add_updater(sync_pulse)
        self.add(p_hook)
        self.play(p_t.animate.set_value(1.0), run_time=0.9)
        self.remove(p_hook)
        pulse_scale[0] = 1.0

        self.at("pictures tracer")
        q_text = T("Bright = more hormone?", 36, TEXT, weight=BOLD).move_to([-0.5, 3.05, 0])
        strike = Line(q_text.get_left() + LEFT * 0.15, q_text.get_right() + RIGHT * 0.15,
                      color=RED, stroke_width=5.5)
        strike.layout_ok = True   # deliberate strike-through across the misconception line
        self.play(FadeIn(q_text), run_time=0.45)
        self.play(Create(strike), run_time=0.55)
        self.wait(0.8)
        self.play(FadeOut(q_text), FadeOut(strike), run_time=0.6)
        self.finish()


class S12End(EndCard):
    LINE = "A scan shows what the gland traps, not what blood carries."
