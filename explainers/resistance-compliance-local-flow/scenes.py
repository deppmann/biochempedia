"""Where the Pressure Goes — Resistance, Compliance and Local Blood Flow.

COLOUR MAP (one colour per concept, used across every scene):
    BLOOD_COLOR       = "#FF7A70"   pale RED: blood dots flowing through every vessel
    PRESSURE_COLOR    = "#E8EAF0"   WHITE (TEXT): pressure bars, gauges, profile curve, equations
    ARTERIOLE_COLOR   = "#FF862F"   ORANGE: arterioles, smooth-muscle rings, tap-handle valves
    CAP_COLOR         = "#38D9E8"   CYAN: capillary bed and its share of resistance/pressure
    VESSEL_COLOR      = "#7E8898"   SLATE grey: small artery, venule, vein, aorta, right atrium
    MUSCLE_FLOW_COLOR = "#D4A843"   GOLD: skeletal-muscle bed flow and gold-tinted flow dots
    OTHER_FLOW_COLOR  = "#B388FF"   PURPLE: all other parallel systemic beds and their flow

THE ONE PICTURE OF THE WORLD:
    Left-to-right vascular bed (small artery -> muscular arteriole -> 12-capillary fan -> venule -> vein)
    across the upper frame, aligned above its computed pressure-drop profile (0-100 mmHg), then
    zoomed out to the two-branch parallel systemic loop (muscle bed in parallel with other beds,
    aorta to right atrium) and zoomed in on the muscle arteriole radius/resistance tap.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s00_hook:        Blood dots flow through the muscle bed (continuity speed profile); the arterial
                     pressure bar lights a 15% CYAN capillary slice, capillary fan pulses, and 85% '?' opens.
    s02_rule:        Inlet/outlet pressure gauges set the high-to-low gradient; blood speed surges and
                     a flow arrow sweeps along the bed while the segment highlights and Q = dP / R builds.
    s03_series:      A highlighted red dot traverses all 5 series segments in turn; paired inlet/outlet
                     volume counters tick up at equal rate; empty pressure axes align below the segments.
    s04_profile:     Computed piecewise-linear pressure profile (93 -> 84 -> 30 -> 16.5 -> 3 mmHg) draws
                     with the travelling dot; arteriole (54/90 = 60%) and capillary (13.5/90 = 15%) fills grow.
    s05_capillaries: Single capillary shortens and replicates 1 -> 24 in parallel while its computed
                     resistance bar R ~ L / N drops from above to below the single-arteriole bar.
    s06_parallel:    Muscle bed pulls back into the top branch of the parallel loop (aorta to right atrium)
                     as the other beds branch, gauges, driving-pressure brackets, and flow bars build.
    s07_idea:        Heart pump beats at the aorta while the arterial gauge trembles gently around steady
                     MAP; tap handles appear and glow on each bed's arteriole.
    s08_tap:         Zoomed muscle arteriole smooth-muscle rings rhythmically squeeze and relax the lumen,
                     tracking inner radius r while resistance ~ 1 / r^4 appears.
    s09_dilate:      Muscle arteriole rings relax and lumen widens; muscle flow bar grows, total peripheral
                     resistance bar shortens, and open '?' markers replace steady-pressure/other-bed claims.
    s10_predict:     Zoomed arteriole breathes gently and returns to resting r0 while the full resistance bar
                     and 'half' line appear, followed by dashed ghosts at 2*r0 and 1.19*r0 under the question.
    s12_answer:      Arteriole widens smoothly from r = 1.00 to r = 1.19 (= 2^(1/4)), driving r^4 from
                     1.0 to 2.0, dropping the resistance bar to half, and speeding lumen dots.
    s13_close:       Back to the full loop: ghost of the s04 arteriole pressure drop glows under the muscle
                     branch, aorta gauge settles steady, and both beds' arteriolar tap handles glow.
"""
from bp_parts import *

# ------------------------------------------------------------------ concept palette
BLOOD_COLOR = "#FF7A70"
PRESSURE_COLOR = TEXT
ARTERIOLE_COLOR = ORANGE
CAP_COLOR = "#38D9E8"
VESSEL_COLOR = "#7E8898"
MUSCLE_FLOW_COLOR = GOLD
OTHER_FLOW_COLOR = "#B388FF"

# ------------------------------------------------------------------ bed & plot geometry
# X boundaries of the 5 series segments in scene units (shared by s00..s04 and the plot below)
SEG_X = (-4.2, -2.0, 0.0, 2.4, 3.9, 5.4)  # art_in, arl_in, cap_in, ven_in, vein_in, vein_out
PLOT_BOX = (-4.2, 5.4, -2.85, -0.45)

# Worked-problem pressures (mmHg) from lesson_for_context.mdx (MAP=93, Pra=3, dP=90)
P_KNOTS = (
    (0.0, 93.0),
    (SEG_X[1] - SEG_X[0], 84.0),   # 2.2: drop 9 (10%)
    (SEG_X[2] - SEG_X[0], 30.0),   # 4.2: drop 54 (60%)
    (SEG_X[3] - SEG_X[0], 16.5),   # 6.6: drop 13.5 (15%)
    (SEG_X[5] - SEG_X[0], 3.0),    # 9.6: drop 13.5 (15%)
)


def pressure_at(x_data):
    xs = [k[0] for k in P_KNOTS]
    ys = [k[1] for k in P_KNOTS]
    return float(np.interp(x_data, xs, ys))


def _tube_poly(xa, xb, yc, ra, rb, color, fill_op=0.30, stroke_w=3.8):
    pts = [
        [xa, yc + ra, 0], [xb, yc + rb, 0],
        [xb, yc - rb, 0], [xa, yc - ra, 0],
    ]
    return Polygon(*pts, stroke_color=color, stroke_width=stroke_w, fill_color=color, fill_opacity=fill_op)


def build_muscle_bed(y_center=1.30, art_r=0.38, arl_r=0.19, cap_spread=0.90, n_caps=12,
                     ven_r=0.23, vein_r=0.42):
    """Build the single muscle bed path left-to-right at SEG_X, returning a VGroup with named parts."""
    x0, x1, x2, x3, x4, x5 = SEG_X
    yc = y_center

    artery = _tube_poly(x0, x1, yc, art_r, art_r * 0.85, VESSEL_COLOR)
    arteriole = _tube_poly(x1, x2, yc, arl_r, arl_r, ARTERIOLE_COLOR, fill_op=0.32)
    rings = VGroup(*[
        RoundedRectangle(
            corner_radius=0.05, width=0.14, height=2 * arl_r + 0.16,
            stroke_color=ARTERIOLE_COLOR, stroke_width=2.5,
            fill_color=ARTERIOLE_COLOR, fill_opacity=0.42,
        ).move_to([x, yc, 0])
        for x in np.linspace(x1 + 0.25, x2 - 0.25, 5)
    ])

    cap_ys = np.linspace(yc - cap_spread, yc + cap_spread, n_caps)
    caps = VGroup()
    for cy in cap_ys:
        path = VMobject(stroke_color=CAP_COLOR, stroke_width=3.5)
        p_in = np.array([x2, yc + (cy - yc) * 0.15, 0.0])
        p_m1 = np.array([x2 + 0.45, cy, 0.0])
        p_m2 = np.array([x3 - 0.45, cy, 0.0])
        p_out = np.array([x3, yc + (cy - yc) * 0.18, 0.0])
        path.set_points_as_corners([p_in, p_m1, p_m2, p_out])
        caps.add(path)

    venule = _tube_poly(x3, x4, yc, ven_r, ven_r * 1.35, VESSEL_COLOR)
    vein = _tube_poly(x4, x5, yc, vein_r * 0.88, vein_r, VESSEL_COLOR)

    bed = VGroup(artery, arteriole, rings, caps, venule, vein)
    bed.artery = artery
    bed.arteriole = arteriole
    bed.rings = rings
    bed.caps = caps
    bed.venule = venule
    bed.vein = vein
    bed.y_center = yc
    bed.cap_ys = cap_ys
    return bed


def _bed_point_and_radius(u, channel, y_center, cap_ys, art_r=0.38, arl_r=0.19, ven_r=0.23, vein_r=0.42):
    """Map normalized progress u in [0, 1) along the muscle bed to (x, y_center, local_half_r, rel_speed)."""
    x0, x1, x2, x3, x4, x5 = SEG_X
    x = x0 + u * (x5 - x0)
    if x < x1:
        f = (x - x0) / (x1 - x0)
        return x, y_center, art_r * (1 - 0.15 * f), 1.0
    if x < x2:
        return x, y_center, arl_r, 1.55
    if x < x3:
        cy = cap_ys[channel % len(cap_ys)]
        s = (x - x2) / (x3 - x2)
        if s < 0.18:
            t = s / 0.18
            y = y_center + (cy - y_center) * (0.15 + 0.85 * t)
        elif s > 0.82:
            t = (1.0 - s) / 0.18
            y = y_center + (cy - y_center) * (0.18 + 0.82 * t)
        else:
            y = cy
        return x, y, 0.025, 0.52
    if x < x4:
        f = (x - x3) / (x4 - x3)
        return x, y_center, ven_r * (1 + 0.35 * f), 0.95
    f = (x - x4) / (x5 - x4)
    return x, y_center, vein_r * (0.88 + 0.12 * f), 0.85


def make_bed_blood_stream(y_center=1.30, cap_ys=None, n_dots=58, seed=7, speed_tracker=None,
                          dot_color=BLOOD_COLOR, dot_radius=0.072):
    """Continuous deterministic blood stream flowing left-to-right through the muscle bed."""
    if cap_ys is None:
        cap_ys = np.linspace(y_center - 0.90, y_center + 0.90, 12)
    rng = np.random.default_rng(seed)
    us = rng.random(n_dots)
    chans = rng.integers(0, len(cap_ys), size=n_dots)
    jits = rng.uniform(-0.55, 0.55, size=n_dots)

    dots = VGroup()
    for i in range(n_dots):
        x, y, r, _ = _bed_point_and_radius(us[i], chans[i], y_center, cap_ys)
        d = Dot([x, y + jits[i] * r, 0], radius=dot_radius, color=dot_color)
        d._u = float(us[i])
        d._ch = int(chans[i])
        d._jit = float(jits[i])
        dots.add(d)

    def step(group, dt):
        mul = speed_tracker.get_value() if speed_tracker is not None else 1.0
        for d in group:
            _, _, _, vrel = _bed_point_and_radius(d._u, d._ch, y_center, cap_ys)
            d._u = (d._u + dt * 0.22 * vrel * mul) % 1.0
            x, y, r, _ = _bed_point_and_radius(d._u, d._ch, y_center, cap_ys)
            d.move_to([x, y + d._jit * r, 0])

    dots.add_updater(step)
    dots.set_z_index(2)
    return dots


def make_pressure_plot(with_guides=True):
    """Create the s03/s04 aligned pressure profile plot."""
    P = Plot(
        box=PLOT_BOX,
        xr=(0.0, SEG_X[-1] - SEG_X[0]),
        yr=(0.0, 100.0),
        xticks=[],
        yticks=[(0, "0"), (50, "50"), (100, "100")],
        ylabel="pressure (mmHg)",
        color=VESSEL_COLOR,
        size=24,
        label_size=24,
    )
    guides = VGroup()
    if with_guides:
        for xb in SEG_X[1:-1]:
            xd = xb - SEG_X[0]
            guides.add(DashedLine(
                P.pt(xd, 0.0), P.pt(xd, 100.0),
                color=VESSEL_COLOR, stroke_width=1.8, dash_length=0.1, stroke_opacity=0.45,
            ))
    return P, guides


def pressure_gauge(x, y_bottom, height, fill_frac, color=PRESSURE_COLOR, width=0.40):
    """Vertical pressure column gauge with outer tube and filled level."""
    outer = RoundedRectangle(
        corner_radius=0.08, width=width, height=height,
        stroke_color=color, stroke_width=2.8, fill_color=BG, fill_opacity=0.85,
    ).move_to([x, y_bottom + height / 2, 0])
    fh = max(0.08, height * fill_frac)
    fill = Rectangle(
        width=width - 0.08, height=fh,
        stroke_width=0, fill_color=color, fill_opacity=0.90,
    ).move_to([x, y_bottom + fh / 2 + 0.03, 0])
    g = VGroup(outer, fill)
    g.outer = outer
    g.fill = fill
    return g


def add_gauge_tremble(gauge_fill, amp=0.035, freq=5.2):
    """Add gentle heartbeat pulse oscillation to the aorta gauge level."""
    gauge_fill._base_y = gauge_fill.get_center()[1]
    gauge_fill._gt = 0.0

    def tremble(m, dt):
        m._gt += dt
        m.move_to([m.get_center()[0], m._base_y + amp * np.sin(freq * m._gt), 0])

    gauge_fill.add_updater(tremble)


def tap_icon(pos, color=ARTERIOLE_COLOR, scale=1.0):
    """Clean valve tap-handle icon placed above an arteriole."""
    stem = Line([0, 0, 0], [0, 0.25 * scale, 0], color=color, stroke_width=4.5)
    bar = Line([-0.24 * scale, 0.25 * scale, 0], [0.24 * scale, 0.25 * scale, 0], color=color, stroke_width=5.5)
    cap_l = Dot([-0.24 * scale, 0.25 * scale, 0], radius=0.05 * scale, color=color)
    cap_r = Dot([0.24 * scale, 0.25 * scale, 0], radius=0.05 * scale, color=color)
    return VGroup(stem, bar, cap_l, cap_r).move_to(pos)


def heart_icon(pos, color=BLOOD_COLOR, scale=1.0, animate_beat=True):
    """Simple geometric heart pump icon (no molecular structure)."""
    t = np.linspace(0, TAU, 80)
    hx = 16 * np.sin(t) ** 3
    hy = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    pts = [np.array([x, y, 0.0]) * 0.023 * scale for x, y in zip(hx, hy)]
    h = Polygon(*pts, stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.75)
    h.move_to(pos)
    if animate_beat:
        h._ht = 0.0

        def beat(m, dt):
            m._ht += dt
            s = 1.0 + 0.14 * np.sin(5.2 * m._ht) ** 4
            m.set_height(0.78 * scale * s)

        h.add_updater(beat)
    return h


def build_parallel_loop(r_muscle_tracker=None, speed_muscle_tracker=None, speed_other_tracker=None,
                        include_bars=True, muscle_flow_val=None, other_flow_val=None):
    """Build the two-branch parallel systemic circulation (aorta -> muscle + other beds -> right atrium)."""
    x_ao = -4.15
    x_ra_in = 2.35
    y_top, y_bot = 1.68, -1.68

    # Vertical aorta and venous collecting manifold
    aorta = RoundedRectangle(
        corner_radius=0.1, width=0.46, height=y_top - y_bot + 0.56,
        stroke_color=VESSEL_COLOR, stroke_width=3.5, fill_color=VESSEL_COLOR, fill_opacity=0.30,
    ).move_to([x_ao, 0.0, 0])
    aorta_inlet = Polygon(
        [-5.05, 0.25, 0], [x_ao - 0.23, 0.25, 0],
        [x_ao - 0.23, -0.25, 0], [-5.05, -0.25, 0],
        stroke_color=VESSEL_COLOR, stroke_width=3.2, fill_color=VESSEL_COLOR, fill_opacity=0.30,
    )
    venous_col = RoundedRectangle(
        corner_radius=0.1, width=0.42, height=y_top - y_bot + 0.50,
        stroke_color=VESSEL_COLOR, stroke_width=3.5, fill_color=VESSEL_COLOR, fill_opacity=0.28,
    ).move_to([x_ra_in, 0.0, 0])

    ra_box = RoundedRectangle(
        corner_radius=0.14, width=1.22, height=0.95,
        stroke_color=VESSEL_COLOR, stroke_width=3.2, fill_color=VESSEL_COLOR, fill_opacity=0.28,
    ).move_to([3.25, 0.0, 0])
    ra_conn = Line([x_ra_in + 0.21, 0, 0], [ra_box.get_left()[0], 0, 0], color=VESSEL_COLOR, stroke_width=6)
    ra_label = T("right\natrium", size=24, color=TEXT, line_spacing=0.8).move_to(ra_box)

    def make_branch(yc, branch_col, arl_col, cap_col, is_muscle):
        xa, xb, xc, xd, xe = -3.92, -2.50, -1.00, 0.78, 2.14
        art = _tube_poly(xa, xb, yc, 0.23, 0.23, branch_col, fill_op=0.30, stroke_w=3.2)
        vein = _tube_poly(xd, xe, yc, 0.24, 0.24, branch_col, fill_op=0.30, stroke_w=3.2)

        cap_ys = np.linspace(yc - 0.58, yc + 0.58, 7)
        caps = VGroup()
        for cy in cap_ys:
            p = VMobject(stroke_color=cap_col, stroke_width=3.0)
            p.set_points_as_corners([
                [xc, yc + (cy - yc) * 0.16, 0],
                [xc + 0.35, cy, 0],
                [xd - 0.35, cy, 0],
                [xd, yc + (cy - yc) * 0.16, 0],
            ])
            caps.add(p)

        def mk_arl():
            rr = r_muscle_tracker.get_value() if (is_muscle and r_muscle_tracker is not None) else 1.0
            rh = 0.15 * rr
            body = _tube_poly(xb, xc, yc, rh, rh, arl_col, fill_op=0.34, stroke_w=3.4)
            rgs = VGroup(*[
                RoundedRectangle(
                    corner_radius=0.04, width=0.11, height=2 * rh + 0.14,
                    stroke_color=arl_col, stroke_width=2.2, fill_color=arl_col, fill_opacity=0.45,
                ).move_to([xx, yc, 0])
                for xx in np.linspace(xb + 0.22, xc - 0.22, 4)
            ])
            return VGroup(body, rgs)

        arl = always_redraw(mk_arl) if (is_muscle and r_muscle_tracker is not None) else mk_arl()
        return VGroup(art, arl, caps, vein), cap_ys, (xa, xb, xc, xd, xe)

    top_branch, top_cys, segs = make_branch(y_top, VESSEL_COLOR, ARTERIOLE_COLOR, CAP_COLOR, True)
    bot_branch, bot_cys, _ = make_branch(y_bot, OTHER_FLOW_COLOR, OTHER_FLOW_COLOR, OTHER_FLOW_COLOR, False)

    top_lab = T("muscle", size=26, color=MUSCLE_FLOW_COLOR).move_to([-0.15, y_top + 0.85, 0])
    bot_lab = T("other beds", size=26, color=OTHER_FLOW_COLOR).move_to([-0.15, y_bot - 0.85, 0])

    # Blood dots flowing along both branches
    def branch_dots(yc, cys, dot_col, seed, st, n=32):
        rng = np.random.default_rng(seed)
        us = rng.random(n)
        chs = rng.integers(0, len(cys), size=n)
        jits = rng.uniform(-0.55, 0.55, size=n)
        xa, xb, xc, xd, xe = segs
        dots = VGroup()

        def xy_at(u, ch, jit):
            x = xa + u * (xe - xa)
            if x < xb:
                return x, yc + jit * 0.16, 1.0
            if x < xc:
                return x, yc + jit * 0.09, 1.4
            if x < xd:
                s = (x - xc) / (xd - xc)
                cy = cys[ch]
                if s < 0.2:
                    y = yc + (cy - yc) * (0.16 + 0.84 * s / 0.2)
                elif s > 0.8:
                    y = yc + (cy - yc) * (0.16 + 0.84 * (1 - s) / 0.2)
                else:
                    y = cy
                return x, y, 0.58
            return x, yc + jit * 0.16, 0.9

        for i in range(n):
            px, py, _ = xy_at(us[i], chs[i], jits[i])
            d = Dot([px, py, 0], radius=0.065, color=dot_col)
            d._u, d._ch, d._jit = float(us[i]), int(chs[i]), float(jits[i])
            dots.add(d)

        def step(grp, dt):
            mul = st.get_value() if st is not None else 1.0
            for d in grp:
                _, _, vrel = xy_at(d._u, d._ch, d._jit)
                d._u = (d._u + dt * 0.24 * vrel * mul) % 1.0
                px, py, _ = xy_at(d._u, d._ch, d._jit)
                d.move_to([px, py, 0])

        dots.add_updater(step)
        dots.set_z_index(2)
        return dots

    top_dots = branch_dots(y_top, top_cys, MUSCLE_FLOW_COLOR, 11, speed_muscle_tracker)
    bot_dots = branch_dots(y_bot, bot_cys, BLOOD_COLOR, 23, speed_other_tracker)

    # Aorta gauge (tall, at left of aorta) and right atrium gauge (short, above RA)
    ao_gauge = pressure_gauge(-4.85, 0.62, 1.75, 0.88, PRESSURE_COLOR, width=0.34)
    ao_lab = T("mean\narterial\npressure", size=24, color=PRESSURE_COLOR, line_spacing=0.82).move_to([-5.35, -1.45, 0])
    ra_gauge = pressure_gauge(3.25, 0.68, 0.85, 0.22, PRESSURE_COLOR, width=0.28)

    world = VGroup(
        aorta_inlet, aorta, venous_col, ra_conn, ra_box, ra_label,
        top_branch, bot_branch, top_lab, bot_lab,
        ao_gauge, ao_lab, ra_gauge,
    )
    world.aorta_group = VGroup(aorta_inlet, aorta)
    world.top_group = VGroup(top_branch, top_lab)
    world.bot_group = VGroup(bot_branch, bot_lab)
    world.ra_group = VGroup(venous_col, ra_conn, ra_box, ra_label, ra_gauge)
    world.top_dots = top_dots
    world.bot_dots = bot_dots
    world.ao_gauge = ao_gauge
    world.ao_lab = ao_lab
    world.ra_gauge = ra_gauge
    world.ra_box = ra_box
    world.top_arl_center = np.array([-1.75, y_top, 0.0])
    world.bot_arl_center = np.array([-1.75, y_bot, 0.0])
    world.aorta_inlet_pos = np.array([-5.55, 0.0, 0.0])

    if include_bars:
        base_y = -2.05
        if muscle_flow_val is None:
            muscle_flow_val = ValueTracker(1.25)
        if other_flow_val is None:
            other_flow_val = ValueTracker(2.05)

        bar_base = Line([4.15, base_y, 0], [6.35, base_y, 0], color=VESSEL_COLOR, stroke_width=2.5)
        m_bar = always_redraw(lambda: Rectangle(
            width=0.52, height=max(0.1, muscle_flow_val.get_value()),
            stroke_color=MUSCLE_FLOW_COLOR, stroke_width=2.5,
            fill_color=MUSCLE_FLOW_COLOR, fill_opacity=0.84,
        ).move_to([4.62, base_y + max(0.1, muscle_flow_val.get_value()) / 2, 0]))
        o_bar = always_redraw(lambda: Rectangle(
            width=0.52, height=max(0.1, other_flow_val.get_value()),
            stroke_color=OTHER_FLOW_COLOR, stroke_width=2.5,
            fill_color=OTHER_FLOW_COLOR, fill_opacity=0.84,
        ).move_to([5.82, base_y + max(0.1, other_flow_val.get_value()) / 2, 0]))
        m_lbl = T("muscle\nflow", size=24, color=MUSCLE_FLOW_COLOR, line_spacing=0.8).move_to([4.62, base_y - 0.45, 0])
        o_lbl = T("other\nbeds", size=24, color=OTHER_FLOW_COLOR, line_spacing=0.8).move_to([5.82, base_y - 0.45, 0])

        world.bars = VGroup(bar_base, m_bar, o_bar, m_lbl, o_lbl)
        world.m_bar = m_bar
        world.o_bar = o_bar
        world.m_lbl = m_lbl
        world.o_lbl = o_lbl
        world.add(world.bars)

    return world


def build_zoomed_arteriole(r_tracker, x_center=-0.8, y_center=0.05, r0_scene=0.78, half_len=3.3):
    """Zoomed-in muscle arteriole with smooth-muscle rings and flowing dots driven by r_tracker.

    Rings are placed with a wider central gap at x_center so the 'r' arrow and label sit cleanly
    between rings, and the lumen uses Polygon so layout_check does not treat it as a panel.
    """
    yc = y_center
    xc = x_center
    ring_offsets = (-half_len + 0.55, -half_len + 1.35, -half_len + 2.15,
                    half_len - 2.15, half_len - 1.35, half_len - 0.55)

    def mk_tube():
        r = r0_scene * r_tracker.get_value()
        body = _tube_poly(xc - half_len, xc + half_len, yc, r, r, ARTERIOLE_COLOR, fill_op=0.28, stroke_w=4.2)
        rings = VGroup(*[
            RoundedRectangle(
                corner_radius=0.10, width=0.36, height=2 * r + 0.34,
                stroke_color=ARTERIOLE_COLOR, stroke_width=3,
                fill_color=ARTERIOLE_COLOR, fill_opacity=0.40,
            ).move_to([xc + dx, yc, 0])
            for dx in ring_offsets
        ])
        return VGroup(body, rings)

    tube = always_redraw(mk_tube)

    stub_l = _tube_poly(xc - half_len - 0.9, xc - half_len, yc, r0_scene * 1.35, r0_scene * 1.35,
                        VESSEL_COLOR, fill_op=0.22, stroke_w=2.8)
    stub_r = _tube_poly(xc + half_len, xc + half_len + 0.9, yc, r0_scene * 1.5, r0_scene * 1.5,
                        CAP_COLOR, fill_op=0.20, stroke_w=2.8)

    rng = np.random.default_rng(19)
    n_dots = 44
    us = rng.random(n_dots)
    jits = rng.uniform(-0.76, 0.76, size=n_dots)
    dots = VGroup()
    for i in range(n_dots):
        r = r0_scene * r_tracker.get_value()
        d = Dot([xc - half_len + us[i] * 2 * half_len, yc + jits[i] * r, 0], radius=0.085, color=BLOOD_COLOR)
        d._u, d._jit = float(us[i]), float(jits[i])
        dots.add(d)

    def step(grp, dt):
        rr = r_tracker.get_value()
        r = r0_scene * rr
        v = 0.25 * (rr ** 2)
        for d in grp:
            d._u = (d._u + dt * v) % 1.0
            d.move_to([xc - half_len + d._u * 2 * half_len, yc + d._jit * r, 0])

    dots.add_updater(step)
    dots.set_z_index(2)
    return VGroup(stub_l, stub_r, tube), dots


# ==============================================================================
# SCENES
# ==============================================================================
class S00Hook(SpokenScene):
    def construct(self):
        bed = build_muscle_bed()
        dots = make_bed_blood_stream(bed.y_center, bed.cap_ys, seed=7)

        bed_lbl = T("muscle bed", size=28, color=TEXT).move_to([0.6, 2.65, 0])
        cat_tag = T("anesthetized cat", size=24, color=CAP_COLOR).move_to([-4.6, 3.25, 0])

        bar_x, bar_y0, bar_h, bar_w = -5.45, -2.15, 4.2, 0.58
        bar_full = Rectangle(
            width=bar_w, height=bar_h,
            stroke_color=PRESSURE_COLOR, stroke_width=3,
            fill_color=PRESSURE_COLOR, fill_opacity=0.84,
        ).move_to([bar_x, bar_y0 + bar_h / 2, 0])
        bar_lbl = T("arterial\npressure", size=24, color=PRESSURE_COLOR, line_spacing=0.85).move_to([bar_x, bar_y0 - 0.55, 0])

        self.add(bed, dots, bed_lbl, cat_tag, bar_full, bar_lbl)

        self.at("about 15 %")
        cap_h = 0.15 * bar_h
        cap_slice = Rectangle(
            width=bar_w, height=cap_h,
            stroke_color=CAP_COLOR, stroke_width=3,
            fill_color=CAP_COLOR, fill_opacity=0.92,
        ).move_to([bar_x, bar_y0 + cap_h / 2, 0])
        cap_lbl = T("capillaries: about 15%", size=26, color=CAP_COLOR).move_to([-3.0, bar_y0 + cap_h / 2, 0])
        cap_tick = Line([bar_x + bar_w / 2 + 0.05, bar_y0 + cap_h / 2, 0],
                        [cap_lbl.get_left()[0] - 0.12, bar_y0 + cap_h / 2, 0],
                        color=CAP_COLOR, stroke_width=2.5)
        self.play(FadeIn(cap_slice), FadeIn(cap_tick), FadeIn(cap_lbl), run_time=0.7)

        self.at("narrowest vessels")
        self.play(bed.caps.animate.set_stroke(width=5.8), run_time=0.45, rate_func=there_and_back)
        self.play(bed.caps.animate.set_stroke(width=5.8), run_time=0.45, rate_func=there_and_back)

        self.at("where does the rest")
        rest_h = 0.85 * bar_h
        rest_box = Rectangle(
            width=bar_w, height=rest_h,
            stroke_color=PRESSURE_COLOR, stroke_width=4,
            fill_color=PRESSURE_COLOR, fill_opacity=0.95,
        ).move_to([bar_x, bar_y0 + cap_h + rest_h / 2, 0])
        q_mark = T("?", size=42, color=BG, weight=BOLD).move_to(rest_box)
        q_mark.layout_ok = True
        q_top = T("Where does the rest go?", size=36, color=PRESSURE_COLOR, weight=BOLD).move_to([0.6, 3.18, 0])
        self.play(FadeIn(rest_box), FadeIn(q_mark), FadeIn(q_top), run_time=0.65)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        bed = build_muscle_bed()
        dots = make_bed_blood_stream(bed.y_center, bed.cap_ys, seed=7)
        bed_lbl = T("muscle bed", size=28, color=TEXT).move_to([0.6, 2.65, 0])
        cat_tag = T("anesthetized cat", size=24, color=CAP_COLOR).move_to([-4.6, 3.25, 0])

        bar_x, bar_y0, bar_h, bar_w = -5.45, -2.15, 4.2, 0.58
        cap_h = 0.15 * bar_h
        rest_h = 0.85 * bar_h
        bar_lbl = T("arterial\npressure", size=24, color=PRESSURE_COLOR, line_spacing=0.85).move_to([bar_x, bar_y0 - 0.55, 0])
        cap_slice = Rectangle(width=bar_w, height=cap_h, stroke_color=CAP_COLOR, stroke_width=3,
                              fill_color=CAP_COLOR, fill_opacity=0.92).move_to([bar_x, bar_y0 + cap_h / 2, 0])
        cap_lbl = T("capillaries: about 15%", size=26, color=CAP_COLOR).move_to([-3.0, bar_y0 + cap_h / 2, 0])
        cap_tick = Line([bar_x + bar_w / 2 + 0.05, bar_y0 + cap_h / 2, 0],
                        [cap_lbl.get_left()[0] - 0.12, bar_y0 + cap_h / 2, 0], color=CAP_COLOR, stroke_width=2.5)
        rest_box = Rectangle(width=bar_w, height=rest_h, stroke_color=PRESSURE_COLOR, stroke_width=4,
                             fill_color=PRESSURE_COLOR, fill_opacity=0.95).move_to([bar_x, bar_y0 + cap_h + rest_h / 2, 0])
        q_mark = T("?", size=42, color=BG, weight=BOLD).move_to(rest_box)
        q_mark.layout_ok = True
        q_top = T("Where does the rest go?", size=36, color=PRESSURE_COLOR, weight=BOLD).move_to([0.6, 3.18, 0])

        bar_group = VGroup(bar_lbl, cap_slice, cap_lbl, cap_tick, rest_box, q_mark)
        self.add(bed, dots, bed_lbl, cat_tag, bar_group, q_top)

        title = T("Where the Pressure Goes", size=44, font=TITLE_FONT, color=PRESSURE_COLOR).move_to([0.4, 3.10, 0])
        rule = Line([-2.2, 2.76, 0], [3.0, 2.76, 0], color=GOLD, stroke_width=3.5)

        self.play(FadeOut(q_top), FadeOut(cat_tag), FadeOut(bar_group), FadeOut(bed_lbl), run_time=0.45)
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.6)
        self.wait(0.55)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.35)
        self.finish()


class S02Rule(SpokenScene):
    def construct(self):
        bed = build_muscle_bed()
        speed = ValueTracker(1.0)
        dots = make_bed_blood_stream(bed.y_center, bed.cap_ys, seed=7, speed_tracker=speed)
        self.add(bed, dots)

        g_high = pressure_gauge(-4.85, 0.25, 2.25, 0.90, PRESSURE_COLOR, width=0.42)
        lbl_high = T("high", size=28, color=PRESSURE_COLOR).next_to(g_high, UP, buff=0.15)
        g_low = pressure_gauge(5.85, 0.25, 2.25, 0.20, PRESSURE_COLOR, width=0.42)
        lbl_low = T("low", size=28, color=PRESSURE_COLOR).next_to(g_low, UP, buff=0.15)

        self.play(FadeIn(g_high), FadeIn(lbl_high), FadeIn(g_low), FadeIn(lbl_low), run_time=0.8)

        self.at("high pressure to low")
        flow_arrow = Arrow([-4.1, 0.12, 0], [5.3, 0.12, 0], color=PRESSURE_COLOR, stroke_width=5.5, buff=0)
        self.play(Create(flow_arrow), speed.animate.set_value(2.2), run_time=1.1)
        self.play(speed.animate.set_value(1.0), FadeOut(flow_arrow), run_time=0.8)

        self.at("stretch of vessel")
        seg_hl = SurroundingRectangle(bed.artery, color=PRESSURE_COLOR, stroke_width=4, buff=0.08)
        self.play(Create(seg_hl), run_time=0.6)

        self.at("flow equals")
        eq = T("flow = pressure drop ÷ resistance", size=34, color=PRESSURE_COLOR, weight=BOLD).move_to([0.4, 3.08, 0])
        self.play(Write(eq), run_time=2.4)
        self.finish()


class S03Series(SpokenScene):
    def construct(self):
        bed = build_muscle_bed()
        dots = make_bed_blood_stream(bed.y_center, bed.cap_ys, seed=7)
        eq = T("flow = pressure drop ÷ resistance", size=34, color=PRESSURE_COLOR, weight=BOLD).move_to([0.4, 3.08, 0])
        self.add(bed, dots, eq)

        travel_x = ValueTracker(SEG_X[0])
        hero = always_redraw(lambda: Dot(
            [travel_x.get_value(), bed.y_center, 0],
            radius=0.15, color=BLOOD_COLOR, stroke_color=MUSCLE_FLOW_COLOR, stroke_width=3.5,
        ))
        hero.set_z_index(4)

        seg_defs = [
            ("small artery", bed.artery, SEG_X[0], SEG_X[1], "small artery", TEXT),
            ("arterial", bed.arteriole, SEG_X[1], SEG_X[2], "arteriole", ARTERIOLE_COLOR),
            ("many capillaries", bed.caps, SEG_X[2], SEG_X[3], "capillaries", CAP_COLOR),
            ("venule", bed.venule, SEG_X[3], SEG_X[4], "venule", TEXT),
            ("vein", bed.vein, SEG_X[4], SEG_X[5], "vein", TEXT),
        ]

        prev_lbl = None
        prev_mob = None
        self.at("small artery")
        self.add(hero)
        for i, (cue, mob, xa, xb, label_txt, col) in enumerate(seg_defs):
            if i > 0:
                self.at(cue)
            lbl = T(label_txt, size=28, color=col).move_to([(xa + xb) / 2, 2.58, 0])
            anims = [
                travel_x.animate.set_value((xa + xb) / 2),
                mob.animate.set_stroke(width=5.8),
                FadeIn(lbl),
            ]
            if prev_lbl is not None:
                anims.append(FadeOut(prev_lbl))
            if prev_mob is not None:
                anims.append(prev_mob.animate.set_stroke(width=3.5))
            self.play(*anims, run_time=0.65)
            prev_lbl, prev_mob = lbl, mob

        self.play(travel_x.animate.set_value(SEG_X[-1]), prev_mob.animate.set_stroke(width=3.5),
                  FadeOut(prev_lbl), run_time=0.5)
        self.remove(hero)

        self.at("end to end")
        vol = ValueTracker(0.0)
        c_in = counter("{:.0f}", vol, at=[-4.95, 1.30, 0], size=34, color=MUSCLE_FLOW_COLOR)
        c_out = counter("{:.0f}", vol, at=[5.90, 1.30, 0], size=34, color=MUSCLE_FLOW_COLOR)
        tag_in = T("same flow", size=24, color=MUSCLE_FLOW_COLOR).move_to([-4.95, 2.02, 0])
        tag_out = T("same flow", size=24, color=MUSCLE_FLOW_COLOR).move_to([5.72, 2.02, 0])
        self.play(FadeIn(c_in), FadeIn(c_out), FadeIn(tag_in), FadeIn(tag_out), run_time=0.45)

        self.play(vol.animate.set_value(10.0), run_time=2.5, rate_func=linear)

        self.at("share of the pressure drop")
        P, guides = make_pressure_plot(with_guides=True)
        self.play(
            Create(P), FadeIn(guides),
            vol.animate.set_value(20.0),
            run_time=2.6, rate_func=linear,
        )
        self.finish()


class S04Profile(SpokenScene):
    def construct(self):
        bed = build_muscle_bed()
        dots = make_bed_blood_stream(bed.y_center, bed.cap_ys, seed=7)
        P, guides = make_pressure_plot(with_guides=True)
        eq_big = T("flow = pressure drop ÷ resistance", size=34, color=PRESSURE_COLOR, weight=BOLD).move_to([0.4, 3.08, 0])
        eq_small = T("flow = pressure drop ÷ resistance", size=24, color=PRESSURE_COLOR).move_to([3.55, 3.22, 0])
        tag = scope_tag("made-up round numbers")

        self.add(bed, dots, P, guides, eq_big)
        self.play(Transform(eq_big, eq_small), FadeIn(tag), run_time=0.7)

        self.at("90")
        x_prog = ValueTracker(0.0)
        live = P.live_curve(pressure_at, x_prog, color=PRESSURE_COLOR, width=5)
        dot = P.dot(lambda: x_prog.get_value(), lambda: pressure_at(x_prog.get_value()),
                    color=PRESSURE_COLOR, ring=MUSCLE_FLOW_COLOR, radius=0.10)
        top_dot = always_redraw(lambda: Dot(
            [SEG_X[0] + x_prog.get_value(), bed.y_center, 0],
            radius=0.12, color=BLOOD_COLOR, stroke_color=MUSCLE_FLOW_COLOR, stroke_width=3,
        ))
        top_dot.set_z_index(4)
        self.add(live, dot, top_dot)

        n_93 = M("93", size=24, color=PRESSURE_COLOR).next_to(P.pt(0.0, 93.0), DR, buff=0.22)
        n_84 = M("84", size=24, color=PRESSURE_COLOR).next_to(P.pt(2.2, 84.0), UR, buff=0.16)
        n_30 = M("30", size=24, color=PRESSURE_COLOR).next_to(P.pt(4.2, 30.0), DL, buff=0.16)
        n_165 = M("16.5", size=24, color=PRESSURE_COLOR).next_to(P.pt(6.6, 16.5), UR, buff=0.14)
        n_3 = M("3", size=24, color=PRESSURE_COLOR).next_to(P.pt(9.6, 3.0), UL, buff=0.18)

        self.play(FadeIn(n_93, run_time=0.25), x_prog.animate.set_value(2.2), run_time=0.95, rate_func=linear)
        self.play(FadeIn(n_84, run_time=0.25), x_prog.animate.set_value(4.2), run_time=0.95, rate_func=linear)
        self.play(FadeIn(n_30, run_time=0.25), x_prog.animate.set_value(6.6), run_time=0.95, rate_func=linear)
        self.play(FadeIn(n_165, run_time=0.25), x_prog.animate.set_value(9.6), run_time=1.05, rate_func=linear)
        self.play(FadeIn(n_3), run_time=0.25)
        self.remove(top_dot)

        self.at("about 60")
        arl_fill = Polygon(
            P.pt(2.2, 84.0), P.pt(4.2, 30.0), P.pt(2.2, 30.0),
            stroke_width=0, fill_color=ARTERIOLE_COLOR, fill_opacity=0.40,
        )
        arl_br = BraceBetweenPoints(P.pt(4.2, 30.0), P.pt(4.2, 84.0), direction=RIGHT, color=ARTERIOLE_COLOR)
        arl_lbl = T("54 of 90:\n60%", size=24, color=ARTERIOLE_COLOR, weight=BOLD, line_spacing=0.8).move_to([1.35, arl_br.get_center()[1], 0])
        self.play(
            FadeIn(arl_fill), GrowFromCenter(arl_br), FadeIn(arl_lbl),
            bed.arteriole.animate.set_stroke(width=6),
            run_time=0.75,
        )
        self.play(bed.arteriole.animate.set_stroke(width=3.8), run_time=0.35)

        self.at("about 15")
        cap_fill = Polygon(
            P.pt(4.2, 30.0), P.pt(6.6, 16.5), P.pt(4.2, 16.5),
            stroke_width=0, fill_color=CAP_COLOR, fill_opacity=0.42,
        )
        cap_lbl = T("13.5 of\n90: 15%", size=24, color=CAP_COLOR, weight=BOLD, line_spacing=0.8).move_to([3.15, -1.40, 0])
        cap_ptr = Line(cap_lbl.get_corner(DL) + np.array([-0.06, -0.06, 0]), P.pt(5.4, 23.25), color=CAP_COLOR, stroke_width=2.8)
        self.play(
            FadeIn(cap_fill), FadeIn(cap_ptr), FadeIn(cap_lbl),
            bed.caps.animate.set_stroke(width=5.8),
            run_time=0.75,
        )
        self.play(bed.caps.animate.set_stroke(width=3.5), run_time=0.35)
        self.finish()


class S05Capillaries(SpokenScene):
    def construct(self):
        arl = _tube_poly(-5.4, -3.3, 0.3, 0.32, 0.32, ARTERIOLE_COLOR, fill_op=0.30, stroke_w=4.0)
        rings = VGroup(*[
            RoundedRectangle(
                corner_radius=0.06, width=0.18, height=0.88,
                stroke_color=ARTERIOLE_COLOR, stroke_width=2.5, fill_color=ARTERIOLE_COLOR, fill_opacity=0.42,
            ).move_to([xx, 0.3, 0])
            for xx in np.linspace(-5.05, -3.65, 4)
        ])

        # Faint background fan showing the rest of the bed initially, while 1 bright capillary is outlined
        ghost_fan = VGroup()
        for cy in np.linspace(-1.7, 2.3, 12):
            p = VMobject(stroke_color=CAP_COLOR, stroke_width=2.0, stroke_opacity=0.22)
            p.set_points_as_corners([
                [-3.30, 0.3 + (cy - 0.3) * 0.12, 0],
                [-2.92, cy, 0], [-1.48, cy, 0],
                [-1.10, 0.3 + (cy - 0.3) * 0.12, 0],
            ])
            ghost_fan.add(p)

        n_count = ValueTracker(1.0)
        cap_len = ValueTracker(4.2)
        cap_r = ValueTracker(0.1)

        def mk_fan():
            n = int(round(n_count.get_value()))
            L = cap_len.get_value()
            x_start = -3.30
            x_end = x_start + L
            ys = [0.3] if n == 1 else np.linspace(-2.0, 2.6, n)
            grp = VGroup()
            for cy in ys:
                p = VMobject(stroke_color=CAP_COLOR, stroke_width=4.5 if n == 1 else 2.8)
                p.set_points_as_corners([
                    [x_start, 0.3 + (cy - 0.3) * 0.12, 0],
                    [x_start + 0.38, cy, 0],
                    [x_end - 0.38, cy, 0],
                    [x_end, 0.3 + (cy - 0.3) * 0.12, 0],
                ])
                grp.add(p)
            return grp

        fan = always_redraw(mk_fan)

        rng = np.random.default_rng(31)
        nd = 32
        us = rng.random(nd)
        seeds = rng.integers(0, 24, size=nd)
        dots = VGroup()
        for i in range(nd):
            d = Dot([-5.4 + us[i] * 5.0, 0.3, 0], radius=0.07, color=BLOOD_COLOR)
            d._u, d._s = float(us[i]), int(seeds[i])
            dots.add(d)

        def step_dots(grp, dt):
            n = int(round(n_count.get_value()))
            L = cap_len.get_value()
            x_start = -3.30
            ys = [0.3] if n == 1 else np.linspace(-2.0, 2.6, n)
            for d in grp:
                d._u = (d._u + dt * 0.24) % 1.0
                x = -5.4 + d._u * (2.1 + L)
                if x < x_start:
                    y = 0.3 + ((d._s % 5) - 2) * 0.09
                else:
                    cy = ys[d._s % len(ys)]
                    s = (x - x_start) / max(L, 0.5)
                    if s < 0.16:
                        y = 0.3 + (cy - 0.3) * (0.12 + 0.88 * s / 0.16)
                    elif s > 0.84:
                        y = 0.3 + (cy - 0.3) * (0.12 + 0.88 * (1 - s) / 0.16)
                    else:
                        y = cy
                d.move_to([x, y, 0])

        dots.add_updater(step_dots)
        dots.set_z_index(2)

        tag = scope_tag("schematic")
        self.add(ghost_fan, arl, rings, fan, dots, tag)

        base_y = -1.6
        base_line = Line([2.2, base_y, 0], [6.1, base_y, 0], color=VESSEL_COLOR, stroke_width=2.5)
        r_ttl = T("resistance", size=28, color=PRESSURE_COLOR).move_to([4.15, 2.85, 0])
        bar_a = Rectangle(
            width=0.72, height=2.2, stroke_color=ARTERIOLE_COLOR, stroke_width=3,
            fill_color=ARTERIOLE_COLOR, fill_opacity=0.84,
        ).move_to([3.1, base_y + 1.1, 0])
        lbl_a = T("one\narteriole", size=24, color=ARTERIOLE_COLOR, line_spacing=0.8).move_to([3.1, base_y - 0.45, 0])

        bar_c = always_redraw(lambda: Rectangle(
            width=0.72, height=max(0.15, cap_r.get_value()),
            stroke_color=CAP_COLOR, stroke_width=3,
            fill_color=CAP_COLOR, fill_opacity=0.84,
        ).move_to([5.1, base_y + max(0.15, cap_r.get_value()) / 2, 0]))
        lbl_c = T("one\ncapillary", size=24, color=CAP_COLOR, line_spacing=0.8).move_to([5.1, base_y - 0.45, 0])

        self.at("One capillary")
        self.add(bar_c)
        self.play(
            FadeIn(base_line), FadeIn(r_ttl), FadeIn(bar_a), FadeIn(lbl_a), FadeIn(lbl_c),
            cap_r.animate.set_value(3.3),
            run_time=1.3,
        )

        self.at("each is short")
        self.play(cap_len.animate.set_value(2.2), cap_r.animate.set_value(2.5), run_time=1.1)

        self.at("many lie side by side")
        lbl_all = T("all capillaries\ntogether", size=24, color=CAP_COLOR, line_spacing=0.8).move_to([5.1, base_y - 0.45, 0])
        self.play(
            FadeOut(ghost_fan),
            n_count.animate.set_value(24.0),
            cap_r.animate.set_value(0.55),
            run_time=2.2, rate_func=linear,
        )
        self.play(swap(lbl_c, lbl_all, run_time=0.5))

        self.at("In muscle")
        muscle_tag = T("in muscle", size=26, color=MUSCLE_FLOW_COLOR).move_to([4.15, 2.25, 0])
        self.play(FadeIn(muscle_tag), run_time=0.5)
        self.finish()


class S06Parallel(SpokenScene):
    def construct(self):
        m_flow = ValueTracker(0.15)
        o_flow = ValueTracker(0.15)
        loop = build_parallel_loop(muscle_flow_val=m_flow, other_flow_val=o_flow)
        tag = scope_tag("schematic")

        # Pull-back settle of the top branch into the loop's upper arm
        self.add(loop.top_dots, tag)
        self.play(FadeIn(loop.top_group, scale=1.08), run_time=0.8)

        self.at("side by side")
        self.add(loop.bot_dots)
        self.play(FadeIn(loop.bot_group), run_time=1.2)

        self.at("from the yorta")
        self.play(
            FadeIn(loop.aorta_group),
            FadeIn(loop.ao_gauge),
            FadeIn(loop.ao_lab),
            run_time=1.1,
        )

        self.at("drained side by side")
        self.play(FadeIn(loop.ra_group), run_time=1.0)

        self.at("same driving pressure")
        br_top = BraceBetweenPoints([-3.95, 2.72, 0], [2.35, 2.72, 0], direction=UP, color=PRESSURE_COLOR)
        br_top_lbl = T("same driving pressure", size=26, color=PRESSURE_COLOR).next_to(br_top, UP, buff=0.08)
        br_bot = BraceBetweenPoints([-3.95, -2.72, 0], [2.35, -2.72, 0], direction=DOWN, color=PRESSURE_COLOR)
        br_bot_lbl = T("same driving pressure", size=26, color=PRESSURE_COLOR).next_to(br_bot, DOWN, buff=0.08)
        self.play(
            GrowFromCenter(br_top), FadeIn(br_top_lbl),
            GrowFromCenter(br_bot), FadeIn(br_bot_lbl),
            FadeIn(loop.bars),
            m_flow.animate.set_value(1.25),
            o_flow.animate.set_value(2.05),
            run_time=1.5,
        )
        self.finish()


class S07Idea(SpokenScene):
    def construct(self):
        m_flow = ValueTracker(1.25)
        o_flow = ValueTracker(2.05)
        loop = build_parallel_loop(muscle_flow_val=m_flow, other_flow_val=o_flow)
        tag = scope_tag("schematic")
        self.add(loop, loop.top_dots, loop.bot_dots, tag)

        self.at("The heart")
        heart = heart_icon(loop.aorta_inlet_pos, color=BLOOD_COLOR, scale=1.0, animate_beat=True)
        steady_tag = T("held nearly\nsteady", size=24, color=PRESSURE_COLOR, line_spacing=0.8).move_to([-4.95, 2.95, 0])
        add_gauge_tremble(loop.ao_gauge.fill)
        self.play(FadeIn(heart), FadeIn(steady_tag), run_time=0.6)

        self.at("Each tissue")
        idea = T("Each tissue sets its own flow", size=34, color=MUSCLE_FLOW_COLOR, weight=BOLD).move_to([0.2, 3.15, 0])
        self.play(FadeIn(idea, shift=UP * 0.1), run_time=0.6)

        self.at("its own arterioles")
        tap_top = tap_icon(loop.top_arl_center + UP * 0.44, color=ARTERIOLE_COLOR, scale=0.95)
        tap_bot = tap_icon(loop.bot_arl_center + UP * 0.44, color=ARTERIOLE_COLOR, scale=0.95)
        self.play(FadeIn(tap_top), FadeIn(tap_bot), run_time=0.55)
        self.play(tap_top.animate.scale(1.25), run_time=0.35, rate_func=there_and_back)
        self.play(tap_bot.animate.scale(1.25), run_time=0.35, rate_func=there_and_back)
        self.finish()


class S08Tap(SpokenScene):
    def construct(self):
        r_trk = ValueTracker(1.0)
        r0_scene = 1.05
        tube, dots = build_zoomed_arteriole(r_trk, x_center=0.0, y_center=0.35, r0_scene=r0_scene, half_len=3.6)
        self.add(tube, dots)

        self.play(r_trk.animate.set_value(0.80), run_time=1.4, rate_func=there_and_back)
        self.play(r_trk.animate.set_value(1.16), run_time=1.4, rate_func=there_and_back)

        self.at("Poiseuille's law")
        self.play(r_trk.animate.set_value(1.0), run_time=0.5)

        self.at("radius")
        r_arrow = always_redraw(lambda: DoubleArrow(
            [0.0, 0.35, 0], [0.0, 0.35 + r0_scene * r_trk.get_value(), 0],
            color=PRESSURE_COLOR, stroke_width=4, tip_length=0.18, buff=0,
        ))
        r_badge = always_redraw(lambda: VGroup(
            BackgroundRectangle(
                T("r", size=32, color=PRESSURE_COLOR, weight=BOLD),
                color=BG, fill_opacity=0.88, buff=0.07,
            ),
            T("r", size=32, color=PRESSURE_COLOR, weight=BOLD),
        ).move_to([0.34, 0.35 + 0.5 * r0_scene * r_trk.get_value(), 0]))
        r_badge.set_z_index(6)
        self.play(FadeIn(r_arrow), FadeIn(r_badge), run_time=0.4)

        self.at("fourth")
        poiseuille = T("resistance ∝ 1 / r⁴", size=36, color=PRESSURE_COLOR, weight=BOLD).move_to([0.0, -2.35, 0])
        self.play(FadeIn(poiseuille, shift=UP * 0.1), run_time=0.6)
        self.play(r_trk.animate.set_value(0.86), run_time=0.9, rate_func=there_and_back)
        self.finish()


class S09Dilate(SpokenScene):
    def construct(self):
        r_muscle = ValueTracker(1.0)
        s_muscle = ValueTracker(1.0)
        s_other = ValueTracker(1.0)
        m_flow = ValueTracker(1.25)
        o_flow = ValueTracker(2.05)
        tpr = ValueTracker(1.35)

        loop = build_parallel_loop(
            r_muscle_tracker=r_muscle,
            speed_muscle_tracker=s_muscle,
            speed_other_tracker=s_other,
            muscle_flow_val=m_flow,
            other_flow_val=o_flow,
        )
        heart = heart_icon(loop.aorta_inlet_pos, color=BLOOD_COLOR, scale=1.0, animate_beat=True)
        add_gauge_tremble(loop.ao_gauge.fill)
        steady_tag = T("held nearly\nsteady", size=24, color=PRESSURE_COLOR, line_spacing=0.8).move_to([-4.95, 2.95, 0])
        tag = scope_tag("schematic")
        self.add(loop, loop.top_dots, loop.bot_dots, heart, steady_tag, tag)

        self.at("relax")
        self.play(
            r_muscle.animate.set_value(1.55),
            s_muscle.animate.set_value(2.1),
            m_flow.animate.set_value(2.35),
            run_time=1.8,
        )

        self.at("total resistance")
        tpr_base_y = 0.65
        tpr_base = Line([4.5, tpr_base_y, 0], [5.9, tpr_base_y, 0], color=VESSEL_COLOR, stroke_width=2.5)
        tpr_bar = always_redraw(lambda: Rectangle(
            width=0.62, height=max(0.15, tpr.get_value()),
            stroke_color=PRESSURE_COLOR, stroke_width=3,
            fill_color=PRESSURE_COLOR, fill_opacity=0.84,
        ).move_to([5.2, tpr_base_y + max(0.15, tpr.get_value()) / 2, 0]))
        tpr_lbl = T("total\nresistance", size=24, color=PRESSURE_COLOR, line_spacing=0.8).move_to([5.2, 2.75, 0])
        self.play(FadeIn(tpr_base), FadeIn(tpr_bar), FadeIn(tpr_lbl), run_time=0.45)
        self.play(tpr.animate.set_value(0.55), run_time=1.2)

        self.at("every other bed")
        other_q = T("?", size=40, color=OTHER_FLOW_COLOR, weight=BOLD).move_to([5.82, 0.32, 0])
        held_q = T("held or not?", size=26, color=GOLD, weight=BOLD).move_to([-4.95, 2.95, 0])
        self.play(
            loop.o_bar.animate.set_opacity(0.35),
            FadeIn(other_q),
            swap(steady_tag, held_q, run_time=0.7),
            run_time=0.9,
        )
        self.finish()


def _predict_backdrop(r_trk=None):
    """Shared zoomed arteriole + resistance bar backdrop for s10_predict and s11_pause."""
    if r_trk is None:
        r_trk = ValueTracker(1.0)
    r0_scene = 0.72
    tube, dots = build_zoomed_arteriole(r_trk, x_center=-1.2, y_center=-0.05, r0_scene=r0_scene, half_len=3.0)

    r_arrow = always_redraw(lambda: DoubleArrow(
        [-1.2, -0.05, 0], [-1.2, -0.05 + r0_scene * r_trk.get_value(), 0],
        color=PRESSURE_COLOR, stroke_width=3.5, tip_length=0.16, buff=0,
    ))
    r_badge = always_redraw(lambda: VGroup(
        BackgroundRectangle(
            T("r", size=30, color=PRESSURE_COLOR, weight=BOLD),
            color=BG, fill_opacity=0.88, buff=0.06,
        ),
        T("r", size=30, color=PRESSURE_COLOR, weight=BOLD),
    ).move_to([-0.86, -0.05 + 0.5 * r0_scene * r_trk.get_value(), 0]))
    r_badge.set_z_index(6)

    eq_lbl = T("resistance ∝ 1 / r⁴", size=30, color=PRESSURE_COLOR).move_to([-1.2, -2.55, 0])

    ghost_2x = VGroup(
        DashedLine([-4.2, -0.05 + 2 * r0_scene, 0], [1.8, -0.05 + 2 * r0_scene, 0], color=CAP_COLOR, stroke_width=3),
        DashedLine([-4.2, -0.05 - 2 * r0_scene, 0], [1.8, -0.05 - 2 * r0_scene, 0], color=CAP_COLOR, stroke_width=3),
    )
    ghost_19 = VGroup(
        DashedLine([-4.2, -0.05 + 1.19 * r0_scene, 0], [1.8, -0.05 + 1.19 * r0_scene, 0], color=GOLD, stroke_width=3.2),
        DashedLine([-4.2, -0.05 - 1.19 * r0_scene, 0], [1.8, -0.05 - 1.19 * r0_scene, 0], color=GOLD, stroke_width=3.2),
    )

    bar_x, bar_y0, bar_h = 4.35, -1.65, 3.0
    bar_base = Line([3.55, bar_y0, 0], [5.15, bar_y0, 0], color=VESSEL_COLOR, stroke_width=2.5)
    r_bar = Rectangle(
        width=0.72, height=bar_h, stroke_color=PRESSURE_COLOR, stroke_width=3,
        fill_color=PRESSURE_COLOR, fill_opacity=0.84,
    ).move_to([bar_x, bar_y0 + bar_h / 2, 0])
    r_title = T("resistance", size=26, color=PRESSURE_COLOR).move_to([bar_x, bar_y0 - 0.42, 0])
    half_y = bar_y0 + 0.5 * bar_h
    half_line = DashedLine([3.65, half_y, 0], [5.15, half_y, 0], color=GOLD, stroke_width=3)
    half_lbl = T("half", size=24, color=GOLD).next_to(half_line, RIGHT, buff=0.12)

    bar_grp = VGroup(bar_base, r_bar, r_title, half_line, half_lbl)
    return VGroup(tube, dots, r_arrow, r_badge, eq_lbl), bar_grp, ghost_2x, ghost_19


class S10Predict(SpokenScene):
    def construct(self):
        r_trk = ValueTracker(1.0)
        main_grp, bar_grp, ghost_2x, ghost_19 = _predict_backdrop(r_trk)
        q = question_card("How much wider halves resistance?", y=3.15, color=PRESSURE_COLOR, size=34, max_w=11.5)
        self.add(main_grp)
        self.play(FadeIn(q.question), r_trk.animate(rate_func=there_and_back).set_value(1.12), run_time=1.0)

        self.at("have their resistance")
        self.play(FadeIn(bar_grp), r_trk.animate(rate_func=there_and_back).set_value(0.92), run_time=1.2)

        self.at("Twice as wide")
        self.play(Create(ghost_2x), run_time=0.8)

        self.at("much less")
        self.play(Create(ghost_19), run_time=0.8)
        self.finish()


class S11Pause(PredictPause):
    QUESTION = "How much wider halves resistance?"
    CARD = {"y": 3.15, "color": TEXT, "size": 34, "max_w": 11.5}
    RING_AT = (5.8, -2.9, 0)
    SECONDS = 4.5

    def backdrop(self):
        main_grp, bar_grp, ghost_2x, ghost_19 = _predict_backdrop()
        pulse(ghost_2x, base=3.0, amp=1.0, speed=3.0)
        pulse(ghost_19, base=3.2, amp=1.0, speed=3.0)
        return VGroup(main_grp, bar_grp, ghost_2x, ghost_19)


class S12Answer(SpokenScene):
    def construct(self):
        r_trk = ValueTracker(1.0)
        r0_scene = 0.72
        tube, dots = build_zoomed_arteriole(r_trk, x_center=-1.2, y_center=-0.05, r0_scene=r0_scene, half_len=3.0)

        ghost_2x = VGroup(
            DashedLine([-4.2, -0.05 + 2 * r0_scene, 0], [1.8, -0.05 + 2 * r0_scene, 0], color=CAP_COLOR, stroke_width=2.5).set_opacity(0.45),
            DashedLine([-4.2, -0.05 - 2 * r0_scene, 0], [1.8, -0.05 - 2 * r0_scene, 0], color=CAP_COLOR, stroke_width=2.5).set_opacity(0.45),
        )
        ghost_19 = VGroup(
            DashedLine([-4.2, -0.05 + 1.19 * r0_scene, 0], [1.8, -0.05 + 1.19 * r0_scene, 0], color=GOLD, stroke_width=3.2),
            DashedLine([-4.2, -0.05 - 1.19 * r0_scene, 0], [1.8, -0.05 - 1.19 * r0_scene, 0], color=GOLD, stroke_width=3.2),
        )

        bar_x, bar_y0, bar_h = 4.35, -1.65, 3.0
        bar_base = Line([3.55, bar_y0, 0], [5.15, bar_y0, 0], color=VESSEL_COLOR, stroke_width=2.5)
        r_bar = always_redraw(lambda: Rectangle(
            width=0.72, height=bar_h / (r_trk.get_value() ** 4),
            stroke_color=PRESSURE_COLOR, stroke_width=3,
            fill_color=PRESSURE_COLOR, fill_opacity=0.84,
        ).move_to([bar_x, bar_y0 + 0.5 * bar_h / (r_trk.get_value() ** 4), 0]))
        r_title = T("resistance", size=26, color=PRESSURE_COLOR).move_to([bar_x, bar_y0 - 0.42, 0])
        half_y = bar_y0 + 0.5 * bar_h
        half_line = DashedLine([3.65, half_y, 0], [5.15, half_y, 0], color=GOLD, stroke_width=3)
        half_lbl = T("half", size=24, color=GOLD).next_to(half_line, RIGHT, buff=0.12)

        q = question_card("How much wider halves resistance?", y=3.15, color=PRESSURE_COLOR, size=34, max_w=11.5)
        self.add(tube, dots, ghost_2x, ghost_19, bar_base, r_bar, r_title, half_line, half_lbl, q)
        self.play(FadeOut(q), run_time=0.45)

        c_r = counter("r: 1.00 → {:.2f}", r_trk, at=[-1.2, -2.25, 0], size=30, color=GOLD)
        c_r4 = always_redraw(lambda: M(f"r⁴: 1.0 → {r_trk.get_value() ** 4:.1f}", size=30, color=PRESSURE_COLOR).move_to([-1.2, -2.88, 0]))
        self.play(FadeIn(c_r), FadeIn(c_r4), run_time=0.4)

        self.at("19 % wider")
        self.play(r_trk.animate.set_value(2.0 ** 0.25), run_time=3.2, rate_func=smooth)

        self.at("small change")
        lbl_2x = T("2× wider: 1/16 resistance", size=26, color=CAP_COLOR).move_to([-1.2, 2.25, 0])
        self.play(FadeIn(lbl_2x), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(lbl_2x), FadeOut(ghost_2x), run_time=0.7)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        loop = build_parallel_loop(include_bars=False)
        heart = heart_icon(loop.aorta_inlet_pos, color=BLOOD_COLOR, scale=1.0, animate_beat=True)
        add_gauge_tremble(loop.ao_gauge.fill)
        self.add(loop, loop.top_dots, loop.bot_dots, heart)

        self.at("where the taps are")
        P_ghost = Plot(
            box=(-3.92, 2.14, -0.75, 0.75),
            xr=(0.0, SEG_X[-1] - SEG_X[0]),
            yr=(0.0, 100.0),
            xticks=[], yticks=[],
            color=VESSEL_COLOR, stroke=2,
        )
        ghost_curve = P_ghost.curve(pressure_at, color=PRESSURE_COLOR, width=4, opacity=0.75)
        arl_drop = Polygon(
            P_ghost.pt(2.2, 84.0), P_ghost.pt(4.2, 30.0), P_ghost.pt(2.2, 30.0),
            stroke_width=0, fill_color=ARTERIOLE_COLOR, fill_opacity=0.50,
        )
        self.play(FadeIn(P_ghost), FadeIn(ghost_curve), FadeIn(arl_drop), run_time=0.5)

        self.at("Hold that pressure steady")
        steady_tag = T("held nearly\nsteady", size=24, color=PRESSURE_COLOR, line_spacing=0.8).move_to([-4.95, 2.95, 0])
        self.play(FadeOut(P_ghost), FadeOut(ghost_curve), FadeOut(arl_drop), FadeIn(steady_tag), run_time=0.55)

        self.at("each tissue's own")
        tap_top = tap_icon(loop.top_arl_center + UP * 0.44, color=ARTERIOLE_COLOR, scale=1.0)
        tap_bot = tap_icon(loop.bot_arl_center + UP * 0.44, color=ARTERIOLE_COLOR, scale=1.0)
        self.play(FadeIn(tap_top), FadeIn(tap_bot), run_time=0.5)
        self.play(tap_top.animate.scale(1.25), tap_bot.animate.scale(1.25), run_time=0.45, rate_func=there_and_back)
        self.finish()


class S14End(EndCard):
    LINE = "With pressure held steady, each tissue's arterioles set its flow."
