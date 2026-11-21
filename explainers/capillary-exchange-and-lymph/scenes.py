"""Filtering All the Way — Capillary Exchange, Lymph and Edema (18 scenes).

COLOUR MAP (one colour per concept for the whole film):
- BLOOD_COL = RED (#FC6255): capillary blood fill and drifting blood dots
- PROTEIN_COL = GOLD (#D4A843): plasma protein (albumin) dots, hold-back bar & arrows
- PUSH_COL = TEXT (#E8EAF0): hydrostatic push bar, arrows, pressure ribbon, probe ring
- WATER_COL = BLUE (#58C4DD): water / filtrate drops and steady-state curve
- MAT_COL = GREEN (#83C167): endothelial glycocalyx fibre mat
- TEXTBOOK_COL = ORANGE (#FF862F): textbook dashed line, ghost arrows, absorbs shading
- CELL_COL = GREY (#8B93A1): lining cells and plot axes

THE ONE WORLD (carried from scene to scene):
Top 40%: horizontal capillary tube (arterial end 32 mmHg at left, venous end 12 mmHg at right),
lower wall of flat lining cells with narrow clefts, thin green glycocalyx lining inside, dark
tissue band underneath, white probe ring on the tube. Right edge: two shared-scale (0..35 mmHg)
vertical bars ('push' white, 'hold-back' gold). Bottom 40%: aligned linear plot (x = 32..12 mmHg,
y = -6..+16 mmHg net filtration, bold zero line with 'out' above and 'in' below). Cleft scenes
(s06..s09) zoom into one gap between two lining cells while keeping inset plot & bars on the right.

WHAT CHANGES PER SCENE:
- s00_hook: Blood dots drift L->R and blue water drops seep out along whole tube; textbook dashed
  ghost arrows (out at arterial, in at venous) appear, then question text across top.
- s01_title: Question & ghost arrows fade out as title fades in across top; blood & seepage continue.
- s02_push: Probe slides to Pc=18; push bar fills to 18 - (-1) = 19 via ValueTracker; push arrow grows.
- s03_holdback: Plasma albumin brightens, glycocalyx glows, 6 mmHg outside protein & arrow appear,
  and hold-back bar outline builds to 26 - 6 = 20 mmHg.
- s04_net: Two gold dots slip through cleft; gold bar fills to 0.9*(26-6)=18 inside 20 outline;
  1-unit net glows, one blue drop leaves, and point (18, +1) appears on plot.
- s05_textbook: Pressure ribbon runs 32->12; hold-back locks at 18; probe visits Pc=32 (push=33, net=+15)
  and Pc=12 (push=13, net=-5); dashed orange textbook line draws through (32,+15)..(12,-5).
- s06_cleft: Padlock flashes; view zooms into one cleft (two lining cells, glycocalyx sieve, thin film
  holding 6 gold dots) with inset plot & compact bars on right.
- s07_rinse: Push bar rises above hold-back; blue stream filters down through mat and rinses gold dots
  out of thin film (leaving 3-4) while gold bar glows steady at 18.
- s08_reverse: Push bar drops below hold-back; blue stream reverses upward; gold dots pile up in thin
  film (4->14) and gold bar shrinks to match push until absorption stops.
- s09_idea: Side-by-side cleft comparison: left filters steadily (rinsed film, tall gold bar); right
  absorbs briefly then freezes as gold piles up and gold bar shrinks ('stop').
- s10_predict: Pull back to full world; probe slides to venous end (Pc=12, push=13); 'steady state'
  tag and three choice chips ('absorb?', 'filter?', 'zero?') appear at top.
- s11_pause: Silent 4.5 s PredictPause: blood flows, probe holds at Pc=12 (push=13), gold bar flickers 12..14.
- s12_answer: 'filter?' glows; gold bar settles to 12.7 (pi_g=11.9, net=+0.3 from steady-state model),
  slow outward drop leaves and (12,+0.3) plots; brief ghosts show stop-itself and zero-flow washout.
- s13_steady: Probe slides to arterial end (Pc=32, pi_g=2.6, hold-back=21.1, net=+12), fast outward drops,
  then sweeps right plotting (24,+4), (20,+1.6), (16,+0.6) with thinning outward drops.
- s14_curve: Textbook <0 region shades orange ('absorbs'); solid blue steady-state curve computed from
  Michel-Levick equation draws from 32 to 12, bending near 22 and flattening above 0 ('hockey stick').
- s15_evidence: Probe at low pressure (Pc=12, push drops to 8); brief inward burst slows & stops as
  gold piles in circular gap inset and schematic timer ticks, then slight outward filtration resumes.
- s16_close: Full world: gold bar & blue curve glow together; orange 'absorbs' fades out; tissue blue
  drops drift down toward bottom edge with downward white '?' arrow.
- s17_end: Standard EndCard with take-home line.
"""
from bp_parts import *

ORANGE = "#FF862F"
BLOOD_COL = RED
PROTEIN_COL = GOLD
PUSH_COL = TEXT
WATER_COL = BLUE
MAT_COL = GREEN
TEXTBOOK_COL = ORANGE
CELL_COL = GREY

# World geometry constants
TUBE_X0, TUBE_X1 = -5.2, 3.4
TUBE_Y0, TUBE_Y1 = 1.62, 2.42
CELL_Y0, CELL_Y1 = 1.44, 1.62
TISS_Y0, TISS_Y1 = 0.48, 1.44

PLOT_BOX = (-5.2, 3.4, -2.65, -0.25)
BAR_X_PUSH = 4.42
BAR_X_HB = 5.78
BAR_Y0 = 0.62
BAR_SCALE = 0.05  # 35 mmHg -> 1.75 units (top y = 2.37)
BAR_W = 0.56

# Cleft gap centers along tube (includes x for Pc=24, 22, 20, 18, 16 and near 32 & 12)
GAP_XS = [-4.65, -3.55, -2.75, -1.76, -0.90, -0.04, 0.82, 1.68, 2.54, 3.12]
GAP_W = 0.11

# Steady-state Michel-Levick physical model
PI_P = 26.0
P_I = -1.0
SIGMA = 0.9
K_PE = 0.47


def x_of_pc(pc):
    return TUBE_X0 + (32.0 - pc) / 20.0 * (TUBE_X1 - TUBE_X0)


def pc_of_x(x):
    return 32.0 - (x - TUBE_X0) / (TUBE_X1 - TUBE_X0) * 20.0


def textbook_net(pc):
    return (pc - P_I) - 18.0


def steady_net(pc):
    """Solve Jv = (Pc - Pi) - sigma * (pi_p - pi_g(Jv)) for net filtration pressure."""
    lo, hi = 1e-6, 40.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        pe = K_PE * mid
        if pe < 1e-6:
            ratio = (1.0 - SIGMA) / ((1.0 - SIGMA) + SIGMA * pe)
        else:
            ratio = (1.0 - SIGMA) / (1.0 - SIGMA * np.exp(-pe))
        pi_g = PI_P * ratio
        val = mid - ((pc - P_I) - SIGMA * (PI_P - pi_g))
        if val < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def steady_pig(pc):
    net = steady_net(pc)
    pe = K_PE * net
    return PI_P * ((1.0 - SIGMA) / (1.0 - SIGMA * np.exp(-pe)))


def _make_probe(pc_tracker):
    def mk():
        x = x_of_pc(pc_tracker.get_value())
        ring = RoundedRectangle(
            corner_radius=0.14, width=0.42, height=1.14,
            stroke_color=PUSH_COL, stroke_width=4.0, fill_opacity=0.0
        ).move_to([x, (CELL_Y0 + TUBE_Y1) / 2, 0])
        ring.layout_ok = True
        return ring
    return always_redraw(mk)


def _make_bar(x, tracker, color, max_val=35.0):
    def mk():
        v = float(np.clip(tracker.get_value(), 0.0, max_val))
        h = max(0.02, v * BAR_SCALE)
        rect = Rectangle(
            width=BAR_W, height=h,
            stroke_color=color, stroke_width=2.0,
            fill_color=color, fill_opacity=0.82 if v > 0.05 else 0.0
        )
        rect.move_to([x, BAR_Y0 + h / 2, 0])
        rect.layout_ok = True
        return rect
    return always_redraw(mk)


def _make_bar_outline(x, val, color):
    h = val * BAR_SCALE
    rect = DashedVMobject(
        Rectangle(width=BAR_W + 0.06, height=h, stroke_color=color, stroke_width=2.5, fill_opacity=0.0),
        num_dashes=20
    )
    rect.move_to([x, BAR_Y0 + h / 2, 0])
    rect.layout_ok = True
    return rect


def _make_bar_num(x, tracker, color, fmt="{:.0f}", min_y=0.0):
    def mk():
        v = float(np.clip(tracker.get_value(), 0.0, 35.0))
        y_top = BAR_Y0 + max(v, min_y) * BAR_SCALE
        lbl = M(fmt.format(v), 24, color).move_to([x, y_top + 0.25, 0])
        return lbl
    return always_redraw(mk)


def build_world_static():
    """Build the static parts of THE WORLD (tube, cells, glycocalyx, tissue, plot, bar baselines)."""
    # Tissue background (no stroke so it never triggers panel outside check)
    tiss_bg = Rectangle(
        width=TUBE_X1 - TUBE_X0, height=TISS_Y1 - TISS_Y0,
        stroke_width=0, fill_color="#161c28", fill_opacity=0.92
    ).move_to([(TUBE_X0 + TUBE_X1) / 2, (TISS_Y0 + TISS_Y1) / 2, 0])
    tiss_bg.set_z_index(-5)
    tiss_bot = Line([TUBE_X0, TISS_Y0, 0], [TUBE_X1, TISS_Y0, 0], color=CELL_COL, stroke_width=2.0)

    # Blood lumen background
    lumen = Rectangle(
        width=TUBE_X1 - TUBE_X0, height=TUBE_Y1 - TUBE_Y0,
        stroke_width=0, fill_color=BLOOD_COL, fill_opacity=0.14
    ).move_to([(TUBE_X0 + TUBE_X1) / 2, (TUBE_Y0 + TUBE_Y1) / 2, 0])
    lumen.set_z_index(-5)

    # Upper wall
    upper_wall = Line([TUBE_X0, TUBE_Y1, 0], [TUBE_X1, TUBE_Y1, 0], color=CELL_COL, stroke_width=4.0)

    # Lower wall: flat lining cells with narrow cleft gaps
    cells = VGroup()
    edges = [TUBE_X0]
    for gx in GAP_XS:
        edges.append(gx - GAP_W / 2)
        edges.append(gx + GAP_W / 2)
    edges.append(TUBE_X1)
    for i in range(0, len(edges), 2):
        x_a, x_b = edges[i], edges[i + 1]
        c = RoundedRectangle(
            corner_radius=0.05, width=x_b - x_a, height=CELL_Y1 - CELL_Y0,
            stroke_color=CELL_COL, stroke_width=2.2, fill_color="#232a3a", fill_opacity=0.95
        ).move_to([(x_a + x_b) / 2, (CELL_Y0 + CELL_Y1) / 2, 0])
        c.layout_ok = True
        cells.add(c)

    # Green glycocalyx mat along inside of lower wall
    xs_mat = np.linspace(TUBE_X0, TUBE_X1, 140)
    pts_mat = [[x, CELL_Y1 + 0.04 + 0.02 * np.sin(18 * (x - TUBE_X0)), 0] for x in xs_mat]
    mat_line = VMobject(stroke_color=MAT_COL, stroke_width=4.5)
    mat_line.set_points_as_corners(pts_mat)
    mat_line.layout_ok = True
    mat_fill = Rectangle(
        width=TUBE_X1 - TUBE_X0, height=0.07, stroke_width=0,
        fill_color=MAT_COL, fill_opacity=0.25
    ).move_to([(TUBE_X0 + TUBE_X1) / 2, CELL_Y1 + 0.035, 0])
    mat_fill.set_z_index(-3)

    # Labels on tube and tissue
    art_lbl = T("arterial end", 24, TEXT).move_to([TUBE_X0 + 0.85, TUBE_Y1 + 0.30, 0])
    ven_lbl = T("venous end", 24, TEXT).move_to([TUBE_X1 - 0.80, TUBE_Y1 + 0.30, 0])
    tiss_lbl = T("tissue", 24, TEXT).move_to([TUBE_X0 + 1.10, TISS_Y0 + 0.25, 0])

    # Shared bar baselines & names
    bar_base = Line([BAR_X_PUSH - 0.45, BAR_Y0, 0], [BAR_X_HB + 0.45, BAR_Y0, 0], color=CELL_COL, stroke_width=2.5)
    push_lbl = T("push", 24, PUSH_COL).move_to([BAR_X_PUSH, BAR_Y0 - 0.28, 0])
    hb_lbl = T("hold-back", 24, PROTEIN_COL).move_to([BAR_X_HB, BAR_Y0 - 0.28, 0])

    # Bottom plot
    P = Plot(
        box=PLOT_BOX, xr=(32, 12), yr=(-6, 16),
        xticks=[32, 28, 24, 20, 18, 16, 12],
        yticks=[(-5, "-5"), (0, "0"), (5, "5"), (10, "10"), (15, "15")],
        xlabel="capillary pressure (mmHg)", ylabel="net (mmHg)",
        color=CELL_COL, size=22, label_size=24
    )
    zero_line = Line(P.pt(32, 0), P.pt(12, 0), color=TEXT, stroke_width=3.5)
    out_lbl = T("out", 24, TEXT).move_to(P.pt(13.2, 3.0))
    in_lbl = T("in", 24, TEXT).move_to(P.pt(29.2, -3.2))

    world = VGroup(
        tiss_bg, lumen, tiss_bot, upper_wall, cells, mat_fill, mat_line,
        art_lbl, ven_lbl, tiss_lbl,
        bar_base, push_lbl, hb_lbl,
        P, zero_line, out_lbl, in_lbl
    )
    return world, P, mat_line, cells


def make_blood_stream(seed=7, n_red=20, n_gold=14):
    """Flowing red blood cells and gold albumin dots moving L->R in the capillary lumen."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    w = TUBE_X1 - TUBE_X0
    for i in range(n_red):
        d = Ellipse(width=0.28, height=0.11, color=BLOOD_COL, stroke_width=1.2, fill_color=BLOOD_COL, fill_opacity=0.68)
        x = TUBE_X0 + rng.uniform(0.16, w - 0.16)
        y = rng.uniform(TUBE_Y0 + 0.16, TUBE_Y1 - 0.13)
        d.move_to([x, y, 0])
        d.vx = rng.uniform(0.95, 1.45)
        d.layout_ok = True

        def u_red(m, dt, x0=TUBE_X0, x1=TUBE_X1):
            m.shift(RIGHT * m.vx * dt)
            if m.get_x() > x1 - 0.15:
                m.shift(LEFT * (x1 - x0 - 0.30))
        d.add_updater(u_red)
        g.add(d)

    g.gold_dots = VGroup()
    for i in range(n_gold):
        d = Dot(radius=0.062, color=PROTEIN_COL).set_opacity(0.92)
        x = TUBE_X0 + rng.uniform(0.08, w - 0.08)
        y = rng.uniform(TUBE_Y0 + 0.14, TUBE_Y1 - 0.12)
        d.move_to([x, y, 0])
        d.vx = rng.uniform(0.85, 1.25)
        d.layout_ok = True

        def u_gold(m, dt, x0=TUBE_X0, x1=TUBE_X1):
            m.shift(RIGHT * m.vx * dt)
            if m.get_x() > x1 - 0.06:
                m.shift(LEFT * (x1 - x0 - 0.12))
        d.add_updater(u_gold)
        g.add(d)
        g.gold_dots.add(d)
    g.set_z_index(1)
    return g


def make_tube_drops(mode="seep_all", pc_tracker=None, flux_fn=None, seed=11):
    """Water/filtrate drops moving out through clefts (or reversing in during absorption)."""
    rng = np.random.default_rng(seed)
    g = VGroup()

    if mode == "seep_all":
        for gx in GAP_XS:
            for k in range(2):
                d = Dot(radius=0.066, color=WATER_COL).set_opacity(0.88)
                phase = (k * 0.5 + rng.uniform(0, 0.4)) % 1.0
                d.move_to([gx, CELL_Y1 - phase * (CELL_Y1 - TISS_Y0 - 0.10), 0])
                d.gx = gx
                d.speed = rng.uniform(0.38, 0.52)
                d.layout_ok = True

                def u_seep(m, dt):
                    m.shift(DOWN * m.speed * dt)
                    if m.get_y() < TISS_Y0 + 0.08:
                        m.move_to([m.gx, CELL_Y1, 0])
                d.add_updater(u_seep)
                g.add(d)
    elif mode == "probe":
        for k in range(5):
            d = Dot(radius=0.068, color=WATER_COL).set_opacity(0.92)
            phase = k / 5.0
            gx = x_of_pc(pc_tracker.get_value()) if pc_tracker else 0.82
            d.move_to([gx, CELL_Y1 - phase * (CELL_Y1 - TISS_Y0 - 0.12), 0])
            d.phase = phase
            d.layout_ok = True

            def u_probe(m, dt):
                fl = flux_fn() if flux_fn else 1.0
                gx_now = x_of_pc(pc_tracker.get_value()) if pc_tracker else 0.82
                nearest = min(GAP_XS, key=lambda gxx: abs(gxx - gx_now))
                x_use = nearest if abs(nearest - gx_now) < 0.45 else gx_now
                span = CELL_Y1 - (TISS_Y0 + 0.10)
                if abs(fl) < 0.05:
                    m.set_opacity(0.0)
                    return
                m.set_opacity(0.92)
                v = np.sign(fl) * (0.34 + 0.09 * min(abs(fl), 15.0))
                m.phase = (m.phase + v * dt / span) % 1.0
                y = CELL_Y1 - m.phase * span
                m.move_to([x_use, y, 0])
            d.add_updater(u_probe)
            g.add(d)
    elif mode == "steady_all":
        for gx in GAP_XS:
            pc = pc_of_x(gx)
            fl = steady_net(pc)
            n_d = 3 if fl > 5.0 else (2 if fl > 1.2 else 1)
            for k in range(n_d):
                d = Dot(radius=0.066, color=WATER_COL).set_opacity(0.90)
                span = CELL_Y1 - (TISS_Y0 + 0.10)
                phase = (k / n_d + rng.uniform(0, 0.2)) % 1.0
                d.move_to([gx, CELL_Y1 - phase * span, 0])
                d.gx = gx
                d.phase = phase
                d.speed = 0.28 + 0.08 * fl
                d.layout_ok = True

                def u_st(m, dt, sp=span):
                    m.phase = (m.phase + m.speed * dt / sp) % 1.0
                    m.move_to([m.gx, CELL_Y1 - m.phase * sp, 0])
                d.add_updater(u_st)
                g.add(d)
    g.set_z_index(2)
    return g


def make_cleft_view(left_x=-6.0, right_x=1.9, y_top=2.8, y_bot=-3.1, gap_w=1.4,
                    cell_y0=-1.1, cell_y1=0.7, seed=19):
    """Build the zoomed cleft geometry (blood above, 2 lining cells, glycocalyx sieve, thin film, tissue)."""
    cx = (left_x + right_x) / 2.0
    gx0, gx1 = cx - gap_w / 2.0, cx + gap_w / 2.0
    w_cell_l = gx0 - left_x
    w_cell_r = right_x - gx1
    cell_h = cell_y1 - cell_y0

    lumen = Rectangle(
        width=right_x - left_x, height=y_top - cell_y1,
        stroke_width=0, fill_color=BLOOD_COL, fill_opacity=0.14
    ).move_to([cx, (y_top + cell_y1) / 2.0, 0])
    lumen.set_z_index(-5)

    tiss = Rectangle(
        width=right_x - left_x, height=cell_y0 - y_bot,
        stroke_width=0, fill_color="#161c28", fill_opacity=0.92
    ).move_to([cx, (cell_y0 + y_bot) / 2.0, 0])
    tiss.set_z_index(-5)

    cell_l = RoundedRectangle(
        corner_radius=0.14, width=w_cell_l, height=cell_h,
        stroke_color=CELL_COL, stroke_width=3.0, fill_color="#232a3a", fill_opacity=0.96
    ).move_to([(left_x + gx0) / 2.0, (cell_y0 + cell_y1) / 2.0, 0])
    cell_r = RoundedRectangle(
        corner_radius=0.14, width=w_cell_r, height=cell_h,
        stroke_color=CELL_COL, stroke_width=3.0, fill_color="#232a3a", fill_opacity=0.96
    ).move_to([(gx1 + right_x) / 2.0, (cell_y0 + cell_y1) / 2.0, 0])
    cell_l.layout_ok = True
    cell_r.layout_ok = True

    # Green glycocalyx sieve mat across the top of cells and spanning the gap mouth
    mat_bg = Rectangle(
        width=right_x - left_x, height=0.28,
        stroke_width=0, fill_color=MAT_COL, fill_opacity=0.24
    ).move_to([cx, cell_y1 + 0.14, 0])
    mat_bg.set_z_index(-3)
    fibres = VGroup()
    xs = np.linspace(left_x, right_x, 90)
    pts1 = [[x, cell_y1 + 0.10 + 0.05 * np.sin(10 * (x - left_x)), 0] for x in xs]
    pts2 = [[x, cell_y1 + 0.22 + 0.05 * np.cos(13 * (x - left_x)), 0] for x in xs]
    for pts in (pts1, pts2):
        ln = VMobject(stroke_color=MAT_COL, stroke_width=3.5)
        ln.set_points_as_corners(pts)
        ln.layout_ok = True
        fibres.add(ln)
    # Cross-fibres specifically across the sieve mouth
    for xf in np.linspace(gx0 + 0.12, gx1 - 0.12, 7):
        vln = Line([xf, cell_y1 + 0.02, 0], [xf, cell_y1 + 0.30, 0], color=MAT_COL, stroke_width=2.5)
        vln.layout_ok = True
        fibres.add(vln)

    # Thin film pocket just beneath the mat inside the gap
    film_y0, film_y1 = cell_y1 - 0.62, cell_y1 - 0.04
    film_box = DashedVMobject(
        Rectangle(width=gap_w - 0.12, height=film_y1 - film_y0, stroke_color=WATER_COL, stroke_width=2.5, fill_opacity=0.0),
        num_dashes=18
    ).move_to([cx, (film_y0 + film_y1) / 2.0, 0])
    film_box.layout_ok = True

    # Blood cells & albumin flowing above the mat (kept clear of 'blood' label at top left)
    rng = np.random.default_rng(seed)
    blood_dots = VGroup()
    for i in range(14):
        is_gold = (i % 2 == 1)
        if is_gold:
            d = Dot(radius=0.075, color=PROTEIN_COL).set_opacity(0.92)
        else:
            d = Ellipse(width=0.42, height=0.17, color=BLOOD_COL, stroke_width=1.5, fill_color=BLOOD_COL, fill_opacity=0.68)
        d.move_to([rng.uniform(left_x + 0.25, right_x - 0.25), rng.uniform(cell_y1 + 0.44, y_top - 0.72), 0])
        d.vx = rng.uniform(0.90, 1.35)
        d.layout_ok = True

        def u_b(m, dt, lx=left_x, rx=right_x):
            m.shift(RIGHT * m.vx * dt)
            if m.get_x() > rx - 0.22:
                m.shift(LEFT * (rx - lx - 0.44))
        d.add_updater(u_b)
        blood_dots.add(d)
    blood_dots.set_z_index(1)

    geom = VGroup(lumen, tiss, cell_l, cell_r, mat_bg, fibres, film_box)
    info = {
        "cx": cx, "gx0": gx0, "gx1": gx1, "cell_y0": cell_y0, "cell_y1": cell_y1,
        "film_y0": film_y0, "film_y1": film_y1, "y_top": y_top, "y_bot": y_bot,
        "cell_l_center": cell_l.get_center(), "cell_r_center": cell_r.get_center(),
        "film_box": film_box, "fibres": fibres
    }
    return geom, blood_dots, info


def make_cleft_inset_plot():
    """Small inset plot at top-right during cleft scenes (built natively at readable font size >= 22)."""
    P = Plot(
        box=(2.9, 6.2, 1.25, 2.95), xr=(32, 12), yr=(-6, 16),
        xticks=[(32, "32"), (12, "12")], yticks=[(0, "0"), (15, "15")],
        color=CELL_COL, size=22, label_size=22, stroke=2.5
    )
    zero = Line(P.pt(32, 0), P.pt(12, 0), color=TEXT, stroke_width=2.5)
    tb = DashedVMobject(Line(P.pt(32, 15), P.pt(12, -5), color=TEXTBOOK_COL, stroke_width=3.5), num_dashes=14)
    rest_dot = Dot(P.pt(18, 1), radius=0.09, color=WATER_COL, stroke_color=TEXT, stroke_width=2)
    return VGroup(P, zero, tb, rest_dot)


def make_compact_bars(push_tr, hb_tr, x_push=3.75, x_hb=5.25, y0=-2.25, scale=0.055):
    base = Line([x_push - 0.45, y0, 0], [x_hb + 0.45, y0, 0], color=CELL_COL, stroke_width=2.5)
    lp = T("push", 24, PUSH_COL).move_to([x_push, y0 - 0.30, 0])
    lh = T("hold-back", 24, PROTEIN_COL).move_to([x_hb, y0 - 0.30, 0])

    def mk_bar(x, tr, col):
        def fn():
            v = float(np.clip(tr.get_value(), 0.0, 35.0))
            h = max(0.03, v * scale)
            r = Rectangle(width=0.56, height=h, stroke_color=col, stroke_width=2.0, fill_color=col, fill_opacity=0.82)
            r.move_to([x, y0 + h / 2, 0])
            r.layout_ok = True
            return r
        return always_redraw(fn)

    return VGroup(base, lp, lh, mk_bar(x_push, push_tr, PUSH_COL), mk_bar(x_hb, hb_tr, PROTEIN_COL))


def add_textbook_plot(P):
    pts = [(32, 15), (24, 7), (20, 3), (16, -1), (12, -5)]
    dots = VGroup(*[Dot(P.pt(x, y), radius=0.085, color=TEXTBOOK_COL) for x, y in pts])
    line = DashedVMobject(Line(P.pt(32, 15), P.pt(12, -5), color=TEXTBOOK_COL, stroke_width=4.0), num_dashes=20)
    lbl = T("textbook", 24, TEXTBOOK_COL).move_to(P.pt(24.5, 11.8))
    return dots, line, lbl


def add_steady_points(P, up_to=5):
    coords = [(12, steady_net(12)), (16, steady_net(16)), (20, steady_net(20)), (24, steady_net(24)), (32, steady_net(32))]
    dots = VGroup(*[Dot(P.pt(x, y), radius=0.09, color=WATER_COL, stroke_color=TEXT, stroke_width=2) for x, y in coords[:up_to]])
    return dots


def add_rest_point(P):
    dot = Dot(P.pt(18, 1), radius=0.095, color=WATER_COL, stroke_color=TEXT, stroke_width=2)
    lbl = T("rest: +1", 24, WATER_COL).move_to(P.pt(16.0, 4.4))
    return dot, lbl


def make_padlock(pos, color=PROTEIN_COL):
    shackle = Arc(radius=0.10, start_angle=0, angle=PI, stroke_color=color, stroke_width=3).move_to([pos[0], pos[1] + 0.10, 0])
    body = RoundedRectangle(corner_radius=0.04, width=0.26, height=0.22, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.35).move_to([pos[0], pos[1] - 0.04, 0])
    txt = T("fixed", 22, color).next_to(body, RIGHT, buff=0.10)
    return VGroup(shackle, body, txt)


# ------------------------------------------------------------------ scenes

class S00Hook(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(18.0)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=7)
        drops = make_tube_drops(mode="seep_all", seed=11)
        self.add(world, probe, blood, drops)

        # Textbook dashed orange ghost arrows over tube
        art_ghost = VGroup(*[
            Arrow([gx, TUBE_Y0 + 0.1, 0], [gx, TISS_Y0 + 0.25, 0], buff=0, color=TEXTBOOK_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28)
            for gx in (-4.65, -3.55, -2.75)
        ])
        ven_ghost = VGroup(*[
            Arrow([gx, TISS_Y0 + 0.25, 0], [gx, TUBE_Y0 + 0.1, 0], buff=0, color=TEXTBOOK_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28)
            for gx in (1.68, 2.54, 3.12)
        ])
        tb_lbl = T("textbook", 26, TEXTBOOK_COL).move_to([-0.9, TUBE_Y1 + 0.30, 0])
        q_txt = T("Does it come back?", 36, PUSH_COL, weight=BOLD).move_to([-0.9, 3.30, 0])

        self.at("fluid seeps")
        self.wait(0.3)

        self.at("the textbook")
        self.play(FadeIn(art_ghost), FadeIn(ven_ghost), FadeIn(tb_lbl), run_time=0.65)

        self.at("does it")
        self.play(FadeIn(q_txt, shift=DOWN * 0.1), run_time=0.45)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(18.0)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=8)
        drops = make_tube_drops(mode="seep_all", seed=12)

        art_ghost = VGroup(*[
            Arrow([gx, TUBE_Y0 + 0.1, 0], [gx, TISS_Y0 + 0.25, 0], buff=0, color=TEXTBOOK_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28)
            for gx in (-4.65, -3.55, -2.75)
        ])
        ven_ghost = VGroup(*[
            Arrow([gx, TISS_Y0 + 0.25, 0], [gx, TUBE_Y0 + 0.1, 0], buff=0, color=TEXTBOOK_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28)
            for gx in (1.68, 2.54, 3.12)
        ])
        tb_lbl = T("textbook", 26, TEXTBOOK_COL).move_to([-0.9, TUBE_Y1 + 0.30, 0])
        q_txt = T("Does it come back?", 36, PUSH_COL, weight=BOLD).move_to([-0.9, 3.30, 0])

        self.add(world, probe, blood, drops, art_ghost, ven_ghost, tb_lbl, q_txt)
        title = T("Filtering All the Way", 46, PUSH_COL, font=TITLE_FONT).move_to([-0.9, 3.30, 0])
        self.play(FadeOut(q_txt), FadeOut(art_ghost), FadeOut(ven_ghost), FadeOut(tb_lbl), run_time=0.55)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.55)
        self.wait(0.45)
        self.play(FadeOut(title), run_time=0.35)
        self.finish()


class S02Push(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(22.0)
        push_tr = ValueTracker(0.0)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=9)
        drops = make_tube_drops(mode="probe", pc_tracker=pc_tr, flux_fn=lambda: 1.5, seed=13)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = always_redraw(lambda: M(f"{push_tr.get_value():.0f}", 24, PUSH_COL).move_to([BAR_X_PUSH, BAR_Y0 + push_tr.get_value() * BAR_SCALE + 0.24, 0]) if push_tr.get_value() > 0.5 else VMobject())

        tag = scope_tag("teaching numbers", size=22, color=TEXT)
        self.add(world, probe, blood, drops, push_bar, push_num, tag)

        # Slide probe to 18 mmHg
        self.at("start with the push")
        rest_lbl = T("resting muscle", 24, PUSH_COL).move_to([x_of_pc(18.0), 3.25, 0])
        self.play(pc_tr.animate.set_value(18.0), FadeIn(rest_lbl), run_time=0.9)

        # Push arrow grows at probe
        x18 = x_of_pc(18.0)
        push_arr = Arrow([x18, CELL_Y1, 0], [x18, TISS_Y0 + 0.62, 0], buff=0, color=PUSH_COL, stroke_width=4.5, max_tip_length_to_length_ratio=0.28)
        in_lbl = T("inside 18", 24, PUSH_COL).move_to([x18, TUBE_Y1 + 0.30, 0])
        out_tiss_lbl = T("tissue -1", 24, PUSH_COL).move_to([x18 - 0.92, TISS_Y0 + 0.25, 0])

        self.at("resting muscle")
        self.play(GrowArrow(push_arr), run_time=0.6)

        self.at("18")
        self.play(FadeIn(in_lbl), run_time=0.4)

        self.at("minus one")
        self.play(FadeIn(out_tiss_lbl), run_time=0.4)

        self.at("the push is 19")
        self.play(push_tr.animate.set_value(19.0), run_time=0.8)
        self.finish()


class S03Holdback(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(18.0)
        push_tr = ValueTracker(19.0)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=10)
        drops = make_tube_drops(mode="probe", pc_tracker=pc_tr, flux_fn=lambda: 1.5, seed=14)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
        tag = scope_tag("teaching numbers", size=22, color=TEXT)

        x18 = x_of_pc(18.0)
        rest_lbl = T("resting muscle", 24, PUSH_COL).move_to([x18, 3.25, 0])
        push_arr = Arrow([x18, CELL_Y1, 0], [x18, TISS_Y0 + 0.62, 0], buff=0, color=PUSH_COL, stroke_width=4.5, max_tip_length_to_length_ratio=0.28)
        in_lbl = T("inside 18", 24, PUSH_COL).move_to([x18, TUBE_Y1 + 0.30, 0])
        out_tiss_lbl = T("tissue -1", 24, PUSH_COL).move_to([x18 - 0.92, TISS_Y0 + 0.25, 0])

        self.add(world, probe, blood, drops, push_bar, push_num, tag, rest_lbl, push_arr, in_lbl, out_tiss_lbl)

        self.at("plasma proteins")
        # Brighten gold dots & show inward pull arrows
        plasma_lbl = T("plasma 26", 24, PROTEIN_COL).move_to([x_of_pc(23.2), TUBE_Y1 + 0.30, 0])
        pull_arrs = VGroup(
            Arrow([x18 - 0.55, TISS_Y0 + 0.62, 0], [x18 - 0.55, CELL_Y1, 0], buff=0, color=PROTEIN_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28),
            Arrow([x18 + 0.55, TISS_Y0 + 0.62, 0], [x18 + 0.55, CELL_Y1, 0], buff=0, color=PROTEIN_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28),
        )
        self.play(
            *[d.animate.scale(1.35).set_opacity(1.0) for d in blood.gold_dots],
            FadeIn(plasma_lbl),
            run_time=0.6
        )

        self.at("pull water")
        self.play(GrowArrow(pull_arrs[0]), GrowArrow(pull_arrs[1]), run_time=0.6)

        self.at("sugary lining")
        glyc_lbl = T("glycocalyx", 24, MAT_COL).move_to([x_of_pc(24.0), TISS_Y0 + 0.25, 0])
        glyc_ptr = Arrow([x_of_pc(24.0), TISS_Y0 + 0.48, 0], [x_of_pc(24.0), CELL_Y1 + 0.02, 0], buff=0, color=MAT_COL, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)
        self.play(mat.animate.set_stroke(width=8.0), FadeIn(glyc_lbl), GrowArrow(glyc_ptr), run_time=0.7)

        self.at("pulls back with 6")
        out_gold = VGroup(
            Dot([x18 + 1.40, CELL_Y0 - 0.14, 0], radius=0.052, color=PROTEIN_COL),
            Dot([x18 + 1.62, CELL_Y0 - 0.22, 0], radius=0.052, color=PROTEIN_COL),
            Dot([x18 + 1.84, CELL_Y0 - 0.12, 0], radius=0.052, color=PROTEIN_COL),
        )
        back_arr = Arrow([x18 + 1.05, CELL_Y0 - 0.12, 0], [x18 + 1.05, TISS_Y0 + 0.56, 0], buff=0, color=PROTEIN_COL, stroke_width=3.5, max_tip_length_to_length_ratio=0.3)
        out6_lbl = T("outside 6", 24, PROTEIN_COL).move_to([x18 + 1.62, TISS_Y0 + 0.25, 0])
        hb_outline = _make_bar_outline(BAR_X_HB, 20.0, PROTEIN_COL)
        eq_lbl = M("26 - 6 = 20", 24, PROTEIN_COL).move_to([5.10, 2.75, 0])
        self.play(FadeIn(out_gold), GrowArrow(back_arr), FadeIn(out6_lbl), Create(hb_outline), FadeIn(eq_lbl), run_time=0.8)
        self.finish()


class S04Net(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        mat.set_stroke(width=7.0)
        pc_tr = ValueTracker(18.0)
        push_tr = ValueTracker(19.0)
        hb_tr = ValueTracker(0.0)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=11)
        for d in blood.gold_dots:
            d.scale(1.3).set_opacity(1.0)
        drops = make_tube_drops(mode="probe", pc_tracker=pc_tr, flux_fn=lambda: 1.0, seed=15)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
        hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
        hb_outline = _make_bar_outline(BAR_X_HB, 20.0, PROTEIN_COL)
        hb_num = always_redraw(lambda: M(f"{hb_tr.get_value():.0f}", 24, PROTEIN_COL).move_to([BAR_X_HB, BAR_Y0 + 20.0 * BAR_SCALE + 0.28, 0]) if hb_tr.get_value() > 0.5 else VMobject())
        tag = scope_tag("teaching numbers", size=22, color=TEXT)

        x18 = x_of_pc(18.0)
        rest_lbl = T("resting muscle", 24, PUSH_COL).move_to([x18, 3.25, 0])
        push_arr = Arrow([x18, CELL_Y1, 0], [x18, TISS_Y0 + 0.62, 0], buff=0, color=PUSH_COL, stroke_width=4.5, max_tip_length_to_length_ratio=0.28)
        in_lbl = T("inside 18", 24, PUSH_COL).move_to([x18, TUBE_Y1 + 0.30, 0])
        out_tiss_lbl = T("tissue -1", 24, PUSH_COL).move_to([x18 - 0.92, TISS_Y0 + 0.25, 0])
        plasma_lbl = T("plasma 26", 24, PROTEIN_COL).move_to([x_of_pc(23.2), TUBE_Y1 + 0.30, 0])
        pull_arrs = VGroup(
            Arrow([x18 - 0.55, TISS_Y0 + 0.62, 0], [x18 - 0.55, CELL_Y1, 0], buff=0, color=PROTEIN_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28),
            Arrow([x18 + 0.55, TISS_Y0 + 0.62, 0], [x18 + 0.55, CELL_Y1, 0], buff=0, color=PROTEIN_COL, stroke_width=4, max_tip_length_to_length_ratio=0.28),
        )
        glyc_lbl = T("glycocalyx", 24, MAT_COL).move_to([x_of_pc(24.0), TISS_Y0 + 0.25, 0])
        glyc_ptr = Arrow([x_of_pc(24.0), TISS_Y0 + 0.48, 0], [x_of_pc(24.0), CELL_Y1 + 0.02, 0], buff=0, color=MAT_COL, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)
        out_gold = VGroup(
            Dot([x18 + 1.40, CELL_Y0 - 0.14, 0], radius=0.052, color=PROTEIN_COL),
            Dot([x18 + 1.62, CELL_Y0 - 0.22, 0], radius=0.052, color=PROTEIN_COL),
            Dot([x18 + 1.84, CELL_Y0 - 0.12, 0], radius=0.052, color=PROTEIN_COL),
        )
        back_arr = Arrow([x18 + 1.05, CELL_Y0 - 0.12, 0], [x18 + 1.05, TISS_Y0 + 0.56, 0], buff=0, color=PROTEIN_COL, stroke_width=3.5, max_tip_length_to_length_ratio=0.3)
        out6_lbl = T("outside 6", 24, PROTEIN_COL).move_to([x18 + 1.62, TISS_Y0 + 0.25, 0])
        eq_old = M("26 - 6 = 20", 24, PROTEIN_COL).move_to([5.10, 2.75, 0])

        self.add(
            world, probe, blood, drops, push_bar, push_num, hb_bar, hb_outline, hb_num, tag,
            rest_lbl, push_arr, in_lbl, out_tiss_lbl, plasma_lbl, pull_arrs, glyc_lbl, glyc_ptr,
            out_gold, back_arr, out6_lbl, eq_old
        )

        self.at("lets a little")
        slip1 = Dot([x18, TUBE_Y0 + 0.08, 0], radius=0.055, color=PROTEIN_COL)
        slip2 = Dot([x18 + 0.04, TUBE_Y0 + 0.15, 0], radius=0.055, color=PROTEIN_COL)
        self.add(slip1, slip2)
        self.play(
            slip1.animate.move_to([x18 - 0.08, CELL_Y0 - 0.18, 0]),
            slip2.animate.move_to([x18 + 0.08, CELL_Y0 - 0.25, 0]),
            run_time=1.0
        )

        self.at("nine tenths")
        eq_new = M("0.9 × 20 = 18", 24, PROTEIN_COL).move_to([5.10, 2.75, 0])
        self.play(hb_tr.animate.set_value(18.0), swap(eq_old, eq_new, run_time=0.7), run_time=0.8)

        self.at("push 19")
        diff_glow = Rectangle(
            width=BAR_W + 0.06, height=1.0 * BAR_SCALE + 0.04,
            stroke_color=WATER_COL, stroke_width=3.0, fill_color=WATER_COL, fill_opacity=0.45
        ).move_to([BAR_X_PUSH, BAR_Y0 + 18.5 * BAR_SCALE, 0])
        net_lbl = M("net: +1 out", 24, WATER_COL).move_to([5.10, -0.15, 0])
        self.play(FadeIn(diff_glow), FadeIn(net_lbl), run_time=0.6)

        self.at("one outward")
        single_drop = Dot([x18, CELL_Y1, 0], radius=0.075, color=WATER_COL)
        single_drop.layout_ok = True
        rest_dot, rest_pt_lbl = add_rest_point(P)
        self.add(single_drop)
        self.play(
            single_drop.animate.move_to([x18, TISS_Y0 + 0.18, 0]),
            FadeIn(rest_dot, scale=1.4), FadeIn(rest_pt_lbl),
            run_time=0.8
        )
        self.finish()


class S05Textbook(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(18.0)
        push_tr = ValueTracker(19.0)
        hb_tr = ValueTracker(18.0)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=12)
        drops = make_tube_drops(mode="probe", pc_tracker=pc_tr, flux_fn=lambda: (pc_tr.get_value() - P_I) - 18.0, seed=16)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
        hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
        hb_num = _make_bar_num(BAR_X_HB, hb_tr, PROTEIN_COL)
        rest_dot, rest_pt_lbl = add_rest_point(P)
        tag = scope_tag("teaching numbers", size=22, color=TEXT)
        net_lbl = always_redraw(lambda: M(f"net: {(push_tr.get_value() - hb_tr.get_value()):+.0f}", 24, TEXTBOOK_COL if abs(push_tr.get_value() - hb_tr.get_value()) > 1.2 else WATER_COL).move_to([5.10, -0.15, 0]))

        self.add(world, probe, blood, drops, push_bar, push_num, hb_bar, hb_num, rest_dot, rest_pt_lbl, tag, net_lbl)

        # Pressure ribbon along tube: bright at left, dim at right
        ribbon = VGroup()
        n_seg = 20
        for i in range(n_seg):
            x_a = TUBE_X0 + i / n_seg * (TUBE_X1 - TUBE_X0)
            x_b = TUBE_X0 + (i + 1) / n_seg * (TUBE_X1 - TUBE_X0)
            op = 0.85 - 0.65 * (i / (n_seg - 1))
            seg = Line([x_a, TUBE_Y1 - 0.08, 0], [x_b, TUBE_Y1 - 0.08, 0], color=PUSH_COL, stroke_width=6.0).set_opacity(op)
            seg.layout_ok = True
            ribbon.add(seg)
        p32 = M("32", 24, PUSH_COL).move_to([TUBE_X0 - 0.56, (TUBE_Y0 + TUBE_Y1) / 2, 0])
        p12 = M("12", 24, PUSH_COL).move_to([TUBE_X1 + 0.44, (TUBE_Y0 + TUBE_Y1) / 2, 0])

        self.at("falls along the capillary")
        self.play(FadeIn(ribbon), FadeIn(p32), FadeIn(p12), run_time=0.8)

        self.at("keep the hold back")
        padlock = make_padlock([BAR_X_HB - 0.15, BAR_Y0 + 18.0 * BAR_SCALE + 0.68])
        self.play(FadeIn(padlock), run_time=0.5)

        tb_dots, tb_line, tb_lbl = add_textbook_plot(P)

        self.at("arterial end")
        self.play(pc_tr.animate.set_value(32.0), push_tr.animate.set_value(33.0), run_time=1.0)
        self.play(FadeIn(tb_dots[0], scale=1.4), run_time=0.35)

        self.at("5 inward")
        self.play(pc_tr.animate.set_value(12.0), push_tr.animate.set_value(13.0), run_time=1.1)
        self.play(FadeIn(tb_dots[4], scale=1.4), run_time=0.35)

        self.at("textbook picture")
        self.play(
            Create(tb_line),
            FadeIn(tb_dots[1]), FadeIn(tb_dots[2]), FadeIn(tb_dots[3]),
            FadeIn(tb_lbl),
            run_time=1.0
        )
        self.finish()


class S06Cleft(SpokenScene):
    def construct(self):
        # Start on world state briefly, flash padlock, then zoom into cleft
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(12.0)
        push_tr = ValueTracker(13.0)
        hb_tr = ValueTracker(18.0)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=13)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
        padlock = make_padlock([BAR_X_HB - 0.15, BAR_Y0 + 18.0 * BAR_SCALE + 0.68])
        tb_dots, tb_line, tb_lbl = add_textbook_plot(P)
        rest_dot, rest_pt_lbl = add_rest_point(P)
        tag = scope_tag("teaching numbers", size=22, color=TEXT)
        pre_world = VGroup(world, probe, blood, push_bar, hb_bar, padlock, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, tag)
        self.add(pre_world)

        self.at("outside protein fixed")
        self.play(Indicate(padlock, color=TEXTBOOK_COL, scale_factor=1.35), run_time=0.8)

        # Build zoomed cleft view + inset plot + compact bars
        cleft_geom, cleft_blood, info = make_cleft_view(seed=19)
        inset_plot = make_cleft_inset_plot()
        push_tr2 = ValueTracker(19.0)
        hb_tr2 = ValueTracker(18.0)
        bars2 = make_compact_bars(push_tr2, hb_tr2)
        tiss_lbl = T("tissue", 24, TEXT).move_to([-5.2, -2.65, 0])
        blood_lbl = T("blood", 24, BLOOD_COL).move_to([-5.2, 2.45, 0])

        # 6 gold dots inside thin film
        rng = np.random.default_rng(21)
        film_gold = VGroup()
        for k in range(6):
            gx = info["gx0"] + 0.22 + (k % 3) * 0.45 + rng.uniform(-0.06, 0.06)
            gy = info["film_y0"] + 0.16 + (k // 3) * 0.25
            d = Dot([gx, gy, 0], radius=0.065, color=PROTEIN_COL)
            d.base = np.array([gx, gy, 0])
            d.ph = k * 1.1
            d.layout_ok = True

            def u_fg(m, dt):
                m.ph += 2.2 * dt
                m.move_to(m.base + np.array([0.04 * np.cos(m.ph), 0.03 * np.sin(1.3 * m.ph), 0]))
            d.add_updater(u_fg)
            film_gold.add(d)

        # Gentle trickle drops through gap
        cleft_drops = VGroup()
        for k in range(3):
            d = Dot([info["cx"], info["cell_y1"] - k * 1.1, 0], radius=0.075, color=WATER_COL).set_opacity(0.85)
            d.layout_ok = True

            def u_cd(m, dt, ytop=info["cell_y1"], ybot=info["y_bot"] + 0.2):
                m.shift(DOWN * 0.55 * dt)
                if m.get_y() < ybot:
                    m.set_y(ytop)
            d.add_updater(u_cd)
            cleft_drops.add(d)

        self.at("zoom in")
        self.play(FadeOut(pre_world), run_time=0.25)
        self.play(
            FadeIn(cleft_geom), FadeIn(cleft_blood), FadeIn(inset_plot), FadeIn(bars2),
            FadeIn(tiss_lbl), FadeIn(blood_lbl), FadeIn(tag),
            run_time=0.45
        )

        self.at("like a sieve")
        glyc_lbl = T("glycocalyx", 24, MAT_COL).move_to([info["cell_r_center"][0], 0.05, 0])
        glyc_arr = Arrow([info["cell_r_center"][0], 0.30, 0], [info["cell_r_center"][0], info["cell_y1"] + 0.04, 0], buff=0, color=MAT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        self.play(info["fibres"].animate.set_stroke(width=5.5), FadeIn(glyc_lbl), GrowArrow(glyc_arr), run_time=0.7)

        self.at("thin film")
        film_lbl = T("thin film", 24, WATER_COL).move_to([info["cell_l_center"][0], 0.25, 0])
        film_arr = Arrow([info["cell_l_center"][0] + 0.85, 0.25, 0], [info["gx0"] + 0.04, 0.35, 0], buff=0, color=WATER_COL, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        self.play(FadeIn(film_lbl), GrowArrow(film_arr), FadeIn(film_gold), FadeIn(cleft_drops), run_time=0.8)
        self.finish()


class S07Rinse(SpokenScene):
    def construct(self):
        cleft_geom, cleft_blood, info = make_cleft_view(seed=20)
        inset_plot = make_cleft_inset_plot()
        push_tr = ValueTracker(19.0)
        hb_tr = ValueTracker(18.0)
        bars = make_compact_bars(push_tr, hb_tr)
        tag = scope_tag("teaching numbers", size=22, color=TEXT)
        tiss_lbl = T("tissue", 24, TEXT).move_to([-5.2, -2.65, 0])
        blood_lbl = T("blood", 24, BLOOD_COL).move_to([-5.2, 2.45, 0])
        glyc_lbl = T("glycocalyx", 24, MAT_COL).move_to([info["cell_r_center"][0], 0.05, 0])
        glyc_arr = Arrow([info["cell_r_center"][0], 0.30, 0], [info["cell_r_center"][0], info["cell_y1"] + 0.04, 0], buff=0, color=MAT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        film_lbl = T("thin film", 24, WATER_COL).move_to([info["cell_l_center"][0], 0.25, 0])
        film_arr = Arrow([info["cell_l_center"][0] + 0.85, 0.25, 0], [info["gx0"] + 0.04, 0.35, 0], buff=0, color=WATER_COL, stroke_width=3, max_tip_length_to_length_ratio=0.22)

        # 6 gold dots initially in thin film
        rng = np.random.default_rng(22)
        film_gold = VGroup()
        for k in range(6):
            gx = info["gx0"] + 0.22 + (k % 3) * 0.45
            gy = info["film_y0"] + 0.16 + (k // 3) * 0.25
            d = Dot([gx, gy, 0], radius=0.065, color=PROTEIN_COL)
            d.layout_ok = True
            film_gold.add(d)

        # Stream of water drops flowing down through mat & gap
        stream_speed = ValueTracker(0.9)
        stream = VGroup()
        for k in range(10):
            dx = info["cx"] + ((k % 3) - 1) * 0.30
            dy = info["cell_y1"] + 0.45 - k * 0.40
            d = Dot([dx, dy, 0], radius=0.075, color=WATER_COL).set_opacity(0.9)
            d.dx = dx
            d.layout_ok = True

            def u_s(m, dt, y0=info["cell_y1"] + 0.55, y1=info["y_bot"] + 0.25):
                m.shift(DOWN * stream_speed.get_value() * dt)
                if m.get_y() < y1:
                    m.set_y(y0)
            d.add_updater(u_s)
            stream.add(d)

        self.add(
            cleft_geom, cleft_blood, inset_plot, bars, tag,
            tiss_lbl, blood_lbl, glyc_lbl, glyc_arr, film_lbl, film_arr,
            film_gold, stream
        )

        self.at("vessel filters")
        self.play(push_tr.animate.set_value(22.0), stream_speed.animate.set_value(1.85), run_time=0.8)

        self.at("streams out")
        self.wait(0.4)

        self.at("rinses the film")
        # Flush 3 of the 6 gold dots downward out of the gap, leaving 3 behind
        rinsed_lbl = T("rinsed", 26, WATER_COL).move_to([info["cell_l_center"][0], -0.45, 0])
        self.play(
            film_gold[0].animate.move_to([info["cx"] - 0.3, info["y_bot"] + 0.35, 0]).set_opacity(0.25),
            film_gold[1].animate.move_to([info["cx"] + 0.1, info["y_bot"] + 0.45, 0]).set_opacity(0.25),
            film_gold[3].animate.move_to([info["cx"] + 0.35, info["y_bot"] + 0.30, 0]).set_opacity(0.25),
            FadeIn(rinsed_lbl),
            run_time=1.0
        )

        self.at("stays strong")
        hb_glow = Rectangle(
            width=0.64, height=18.0 * 0.055 + 0.06,
            stroke_color=PROTEIN_COL, stroke_width=3.5, fill_opacity=0.0
        ).move_to([5.25, -2.25 + 9.0 * 0.055, 0])
        hb_glow.layout_ok = True
        self.play(FadeIn(hb_glow), run_time=0.5)
        self.finish()


class S08Reverse(SpokenScene):
    def construct(self):
        cleft_geom, cleft_blood, info = make_cleft_view(seed=23)
        inset_plot = make_cleft_inset_plot()
        push_tr = ValueTracker(22.0)
        hb_tr = ValueTracker(18.0)
        bars = make_compact_bars(push_tr, hb_tr)
        tag = scope_tag("teaching numbers", size=22, color=TEXT)
        tiss_lbl = T("tissue", 24, TEXT).move_to([-5.2, -2.65, 0])
        blood_lbl = T("blood", 24, BLOOD_COL).move_to([-5.2, 2.45, 0])
        glyc_lbl = T("glycocalyx", 24, MAT_COL).move_to([info["cell_r_center"][0], 0.05, 0])
        glyc_arr = Arrow([info["cell_r_center"][0], 0.30, 0], [info["cell_r_center"][0], info["cell_y1"] + 0.04, 0], buff=0, color=MAT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        film_lbl = T("thin film", 24, WATER_COL).move_to([info["cell_l_center"][0], 0.25, 0])
        film_arr = Arrow([info["cell_l_center"][0] + 0.85, 0.25, 0], [info["gx0"] + 0.04, 0.35, 0], buff=0, color=WATER_COL, stroke_width=3, max_tip_length_to_length_ratio=0.22)

        # 4 initial gold dots in film + 10 more arriving from tissue
        film_gold = VGroup()
        for k in range(4):
            gx = info["gx0"] + 0.24 + k * 0.30
            gy = info["film_y0"] + 0.25
            d = Dot([gx, gy, 0], radius=0.065, color=PROTEIN_COL)
            d.layout_ok = True
            film_gold.add(d)

        incoming_gold = VGroup()
        rng = np.random.default_rng(29)
        for k in range(10):
            sx = info["gx0"] + rng.uniform(0.18, 1.22)
            sy = info["y_bot"] + rng.uniform(0.35, 1.65)
            d = Dot([sx, sy, 0], radius=0.065, color=PROTEIN_COL)
            d.target_pos = np.array([info["gx0"] + 0.18 + (k % 5) * 0.25 + rng.uniform(-0.04, 0.04),
                                     info["film_y0"] + 0.14 + (k // 5) * 0.26 + rng.uniform(-0.04, 0.04), 0])
            d.layout_ok = True
            incoming_gold.add(d)

        # Water drop stream (velocity tracker: positive = down, negative = up)
        vy_tr = ValueTracker(1.2)
        stream = VGroup()
        for k in range(10):
            dx = info["cx"] + ((k % 3) - 1) * 0.30
            dy = info["cell_y1"] + 0.45 - k * 0.40
            d = Dot([dx, dy, 0], radius=0.075, color=WATER_COL).set_opacity(0.9)
            d.layout_ok = True

            def u_rev(m, dt, ytop=info["cell_y1"] + 0.55, ybot=info["y_bot"] + 0.25):
                vy = vy_tr.get_value()
                m.shift(DOWN * vy * dt)
                if vy > 0 and m.get_y() < ybot:
                    m.set_y(ytop)
                elif vy < 0 and m.get_y() > ytop:
                    m.set_y(ybot)
            d.add_updater(u_rev)
            stream.add(d)

        self.add(
            cleft_geom, cleft_blood, inset_plot, bars, tag,
            tiss_lbl, blood_lbl, glyc_lbl, glyc_arr, film_lbl, film_arr,
            film_gold, incoming_gold, stream
        )

        self.at("reverse the stream")
        self.play(push_tr.animate.set_value(12.0), vy_tr.animate.set_value(-1.6), run_time=0.9)

        self.at("vessel absorbs")
        self.play(*[d.animate.move_to(d.target_pos) for d in incoming_gold[:3]], run_time=1.6)

        self.at("stays behind")
        # Gold dots move up into thin film and stop under the mat
        self.play(*[d.animate.move_to(d.target_pos) for d in incoming_gold[3:6]], run_time=1.2)

        self.at("piles up")
        left_lbl = T("left behind", 24, PROTEIN_COL).move_to([info["cell_l_center"][0], -0.45, 0])
        self.play(
            *[d.animate.move_to(d.target_pos) for d in incoming_gold[6:]],
            FadeIn(left_lbl),
            run_time=0.9
        )

        self.at("weakens")
        self.play(hb_tr.animate.set_value(12.0), vy_tr.animate.set_value(0.0), run_time=1.0)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        tp = TwoPanel("filtering: strong", "absorbing: weakens", colors=(WATER_COL, PROTEIN_COL), top=2.65, bottom=-3.05, gap=0.35, width=12.8, size=28)
        headline = T("hold-back set by flow", 32, PUSH_COL, weight=BOLD).move_to([0, 3.25, 0])

        # Build left and right clefts cleanly inside each panel without scaling text
        # Left panel x: -6.375 .. -0.175 -> cleft -6.0 .. -2.1, bar at -1.0
        l_geom, l_blood, l_info = make_cleft_view(left_x=-6.05, right_x=-2.05, y_top=1.85, y_bot=-2.65, gap_w=0.95, cell_y0=-0.95, cell_y1=0.45, seed=31)
        l_hb = ValueTracker(18.0)
        l_bar_base = Line([-1.55, -2.15, 0], [-0.55, -2.15, 0], color=CELL_COL, stroke_width=2.5)
        l_bar = always_redraw(lambda: Rectangle(width=0.52, height=max(0.03, l_hb.get_value() * 0.11), stroke_color=PROTEIN_COL, stroke_width=2, fill_color=PROTEIN_COL, fill_opacity=0.85).move_to([-1.05, -2.15 + l_hb.get_value() * 0.055, 0]))
        l_bar.layout_ok = True
        l_bar_lbl = T("hold-back", 22, PROTEIN_COL).move_to([-1.05, -2.50, 0])
        l_film_gold = VGroup(*[Dot([l_info["gx0"] + 0.22 + k * 0.25, l_info["film_y0"] + 0.24, 0], radius=0.055, color=PROTEIN_COL) for k in range(3)])
        for d in l_film_gold:
            d.layout_ok = True
        l_stream = VGroup()
        for k in range(7):
            dx = l_info["cx"] + ((k % 3) - 1) * 0.22
            d = Dot([dx, l_info["cell_y1"] + 0.35 - k * 0.42, 0], radius=0.065, color=WATER_COL).set_opacity(0.9)
            d.layout_ok = True

            def u_ls(m, dt, y0=l_info["cell_y1"] + 0.35, y1=l_info["y_bot"] + 0.25):
                m.shift(DOWN * 1.4 * dt)
                if m.get_y() < y1:
                    m.set_y(y0)
            d.add_updater(u_ls)
            l_stream.add(d)

        # Right panel x: 0.175 .. 6.375 -> cleft 0.55 .. 4.55, bar at 5.55
        r_geom, r_blood, r_info = make_cleft_view(left_x=0.55, right_x=4.55, y_top=1.85, y_bot=-2.65, gap_w=0.95, cell_y0=-0.95, cell_y1=0.45, seed=32)
        r_hb = ValueTracker(18.0)
        r_vy = ValueTracker(-1.3)
        r_bar_base = Line([5.05, -2.15, 0], [6.05, -2.15, 0], color=CELL_COL, stroke_width=2.5)
        r_bar = always_redraw(lambda: Rectangle(width=0.52, height=max(0.03, r_hb.get_value() * 0.11), stroke_color=PROTEIN_COL, stroke_width=2, fill_color=PROTEIN_COL, fill_opacity=0.85).move_to([5.55, -2.15 + r_hb.get_value() * 0.055, 0]))
        r_bar.layout_ok = True
        r_bar_lbl = T("hold-back", 22, PROTEIN_COL).move_to([5.55, -2.50, 0])
        r_film_gold = VGroup()
        rng_r = np.random.default_rng(33)
        for k in range(12):
            gx = r_info["gx0"] + 0.16 + (k % 4) * 0.21 + rng_r.uniform(-0.03, 0.03)
            gy = r_info["film_y0"] + 0.14 + (k // 4) * 0.18 + rng_r.uniform(-0.03, 0.03)
            sx = r_info["gx0"] + rng_r.uniform(0.14, 0.80)
            sy = r_info["y_bot"] + rng_r.uniform(0.30, 1.30)
            d = Dot([sx, sy, 0], radius=0.055, color=PROTEIN_COL)
            d.target_pos = np.array([gx, gy, 0])
            d.layout_ok = True
            r_film_gold.add(d)
        r_stream = VGroup()
        for k in range(7):
            dx = r_info["cx"] + ((k % 3) - 1) * 0.22
            d = Dot([dx, r_info["y_bot"] + 0.35 + k * 0.40, 0], radius=0.065, color=WATER_COL).set_opacity(0.9)
            d.layout_ok = True

            def u_rs(m, dt, y0=r_info["cell_y1"] + 0.35, y1=r_info["y_bot"] + 0.25):
                vy = r_vy.get_value()
                m.shift(DOWN * vy * dt)
                if vy < 0 and m.get_y() > y0:
                    m.set_y(y1)
            d.add_updater(u_rs)
            r_stream.add(d)

        self.add(
            tp, l_geom, l_blood, l_bar_base, l_bar, l_bar_lbl, l_film_gold, l_stream,
            r_geom, r_blood, r_bar_base, r_bar, r_bar_lbl, r_film_gold, r_stream
        )

        self.at("set by the flow")
        self.play(FadeIn(headline, shift=DOWN * 0.1), run_time=0.6)

        self.at("filtering keeps")
        self.play(Indicate(l_bar, color=WATER_COL, scale_factor=1.08), run_time=0.6)

        self.at("absorbing weakens")
        self.play(
            *[d.animate.move_to(d.target_pos) for d in r_film_gold],
            r_hb.animate.set_value(7.0),
            r_vy.animate.set_value(-0.3),
            run_time=1.0
        )

        self.at("absorption stops")
        stop_tag = boxed_label("stop", color=RED, size=24).move_to([r_info["cell_r_center"][0], -0.42, 0])
        self.play(r_vy.animate.set_value(0.0), FadeIn(stop_tag), run_time=0.5)
        self.finish()


def _build_predict_scene_state():
    """Shared builder for S10Predict and S11Pause so frames match seamlessly."""
    world, P, mat, cells = build_world_static()
    pc_tr = ValueTracker(12.0)
    push_tr = ValueTracker(13.0)
    hb_tr = ValueTracker(13.0)
    probe = _make_probe(pc_tr)
    blood = make_blood_stream(seed=41)
    push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
    push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
    hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
    tb_dots, tb_line, tb_lbl = add_textbook_plot(P)
    rest_dot, rest_pt_lbl = add_rest_point(P)
    steady_tag = T("steady state", 24, TEAL).move_to([-5.3, 3.30, 0])
    teach_tag = scope_tag("teaching numbers", size=22, color=TEXT)
    choices = VGroup(
        boxed_label("absorb?", PUSH_COL, size=26),
        boxed_label("filter?", PUSH_COL, size=26),
        boxed_label("zero?", PUSH_COL, size=26),
    ).arrange(RIGHT, buff=0.35).move_to([1.2, 3.35, 0])
    return world, P, pc_tr, push_tr, hb_tr, probe, blood, push_bar, push_num, hb_bar, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, steady_tag, teach_tag, choices


class S10Predict(SpokenScene):
    def construct(self):
        world, P, pc_tr, push_tr, hb_tr, probe, blood, push_bar, push_num, hb_bar, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, steady_tag, teach_tag, choices = _build_predict_scene_state()
        pc_tr.set_value(18.0)
        push_tr.set_value(19.0)
        hb_tr.set_value(18.0)
        self.add(world, probe, blood, push_bar, push_num, hb_bar, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, teach_tag)

        self.at("venous end")
        self.play(pc_tr.animate.set_value(12.0), push_tr.animate.set_value(13.0), run_time=0.9)

        self.at("only 13")
        self.wait(0.2)

        self.at("steady state")
        self.play(FadeIn(steady_tag), run_time=0.45)

        self.at("absorb filter")
        self.play(FadeIn(choices[0]), FadeIn(choices[1]), run_time=0.6)

        self.at("exactly zero")
        self.play(FadeIn(choices[2]), run_time=0.4)
        self.finish()


class S11Pause(PredictPause):
    QUESTION = ""
    OPTIONS = ()
    RING_AT = (5.05, -1.55, 0)
    SECONDS = 4.5

    def backdrop(self):
        world, P, pc_tr, push_tr, hb_tr, probe, blood, push_bar, push_num, hb_bar, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, steady_tag, teach_tag, choices = _build_predict_scene_state()
        # Flicker gold bar between 12 and 14 without settling
        t_flick = {"t": 0.0}

        def u_hb(m, dt):
            t_flick["t"] += dt
            hb_tr.set_value(13.0 + 1.0 * np.sin(5.0 * t_flick["t"]))
        hb_bar.add_updater(u_hb)
        return VGroup(world, probe, blood, push_bar, push_num, hb_bar, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, steady_tag, teach_tag, choices)


class S12Answer(SpokenScene):
    def construct(self):
        world, P, pc_tr, push_tr, hb_tr, probe, blood, push_bar, push_num, hb_bar, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, steady_tag, teach_tag, choices = _build_predict_scene_state()
        hb_tr.set_value(13.0)
        hb_num = _make_bar_num(BAR_X_HB, hb_tr, PROTEIN_COL, fmt="{:.1f}")
        drops = make_tube_drops(mode="probe", pc_tracker=pc_tr, flux_fn=lambda: 0.3, seed=51)
        self.add(world, probe, blood, drops, push_bar, push_num, hb_bar, hb_num, tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, steady_tag, teach_tag, choices)

        # Dissolve question choices; 'filter?' stays and glows
        filter_chip = choices[1]
        self.at("a trickle outward")
        self.play(
            FadeOut(choices[0]), FadeOut(choices[2]),
            filter_chip.box.animate.set_stroke(WATER_COL, width=4.0).set_fill(WATER_COL, opacity=0.25),
            filter_chip.label.animate.set_color(WATER_COL),
            run_time=0.6
        )

        self.at("about 0")
        film_lbl = T("film protein: 11.9", 22, PROTEIN_COL).move_to([5.15, 3.12, 0])
        net_lbl = M("net +0.3 out", 24, WATER_COL).move_to([5.10, -0.15, 0])
        pt12 = Dot(P.pt(12, steady_net(12)), radius=0.10, color=WATER_COL, stroke_color=TEXT, stroke_width=2.5)
        self.play(hb_tr.animate.set_value(12.7), FadeIn(film_lbl), FadeIn(net_lbl), FadeIn(pt12, scale=1.4), run_time=0.8)

        # Brief dashed ghost 1: absorbing piles protein up and stops itself
        self.at("absorbing would pile")
        g1_box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=2.5, height=1.25, stroke_color=TEXTBOOK_COL, stroke_width=2.5), num_dashes=22).move_to([5.0, -1.45, 0])
        g1_arr = Arrow([4.3, -1.75, 0], [4.3, -1.10, 0], buff=0, color=WATER_COL, stroke_width=3.5, max_tip_length_to_length_ratio=0.3)
        g1_dots = VGroup(*[Dot([5.1 + 0.16 * (k % 4), -1.65 + 0.16 * (k // 4), 0], radius=0.05, color=PROTEIN_COL) for k in range(8)])
        g1_txt = T("stops", 22, RED).move_to([5.5, -1.05, 0])
        g1 = VGroup(g1_box, g1_arr, g1_dots, g1_txt)
        self.play(FadeIn(g1), run_time=0.6)

        self.at("stop itself")
        self.play(g1_arr.animate.set_opacity(0.25), run_time=0.5)
        self.play(FadeOut(g1), run_time=0.35)

        # Brief dashed ghost 2: if water stopped moving, protein seeps out & hold-back vanishes
        self.at("if water stopped")
        g2_box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=2.9, height=1.25, stroke_color=PROTEIN_COL, stroke_width=2.5), num_dashes=24).move_to([5.0, -1.45, 0])
        g2_dots = VGroup(*[Dot([4.4 + 0.22 * k, -1.20, 0], radius=0.055, color=PROTEIN_COL) for k in range(4)])
        g2_txt = T("protein leaks out", 22, PROTEIN_COL).move_to([5.0, -1.80, 0])
        g2 = VGroup(g2_box, g2_dots, g2_txt)
        self.play(FadeIn(g2), run_time=0.5)
        self.play(g2_dots.animate.shift(DOWN * 0.24), hb_tr.animate.set_value(2.0), run_time=1.0)

        self.at("hold back vanished")
        self.play(FadeOut(g2), hb_tr.animate.set_value(12.7), run_time=0.7)
        self.finish()


class S13Steady(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(12.0)
        push_tr = ValueTracker(13.0)
        hb_tr = ValueTracker(12.7)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=61)
        drops = make_tube_drops(mode="probe", pc_tracker=pc_tr, flux_fn=lambda: steady_net(pc_tr.get_value()), seed=62)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
        hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
        hb_num = _make_bar_num(BAR_X_HB, hb_tr, PROTEIN_COL, fmt="{:.1f}")
        tb_dots, tb_line, tb_lbl = add_textbook_plot(P)
        rest_dot, rest_pt_lbl = add_rest_point(P)
        pt12 = Dot(P.pt(12, steady_net(12)), radius=0.10, color=WATER_COL, stroke_color=TEXT, stroke_width=2.5)
        steady_tag = T("steady state", 24, TEAL).move_to([-5.3, 3.30, 0])
        teach_tag = scope_tag("teaching numbers", size=22, color=TEXT)
        film_lbl = T("film protein: 11.9", 22, PROTEIN_COL).move_to([5.15, 3.12, 0])
        net_lbl = always_redraw(lambda: M(f"net ~ {steady_net(pc_tr.get_value()):+.1f}", 24, WATER_COL).move_to([5.10, -0.15, 0]))

        self.add(
            world, probe, blood, drops, push_bar, push_num, hb_bar, hb_num,
            tb_dots, tb_line, tb_lbl, rest_dot, rest_pt_lbl, pt12,
            steady_tag, teach_tag, film_lbl, net_lbl
        )

        self.at("arterial end")
        film_lbl_32 = T("film protein: 2.6", 22, PROTEIN_COL).move_to([5.15, 3.12, 0])
        self.play(
            pc_tr.animate.set_value(32.0),
            push_tr.animate.set_value(33.0),
            run_time=1.0
        )

        self.at("holdback grows")
        self.play(hb_tr.animate.set_value(21.1), swap(film_lbl, film_lbl_32, run_time=0.6), run_time=0.9)

        self.at("falls from 15")
        pt32 = Dot(P.pt(32, steady_net(32)), radius=0.10, color=WATER_COL, stroke_color=TEXT, stroke_width=2.5)
        self.play(FadeIn(pt32, scale=1.4), run_time=0.5)

        self.at("every point filters")
        model_tag = T("illustrative model", 22, TEXT).next_to(teach_tag, UP, buff=0.12).align_to(teach_tag, RIGHT)
        pt24 = Dot(P.pt(24, steady_net(24)), radius=0.10, color=WATER_COL, stroke_color=TEXT, stroke_width=2.5)
        pt20 = Dot(P.pt(20, steady_net(20)), radius=0.10, color=WATER_COL, stroke_color=TEXT, stroke_width=2.5)
        pt16 = Dot(P.pt(16, steady_net(16)), radius=0.10, color=WATER_COL, stroke_color=TEXT, stroke_width=2.5)
        self.play(FadeOut(film_lbl_32), FadeIn(model_tag), pc_tr.animate.set_value(24.0), push_tr.animate.set_value(25.0), hb_tr.animate.set_value(20.7), run_time=0.45)
        self.play(FadeIn(pt24), pc_tr.animate.set_value(20.0), push_tr.animate.set_value(21.0), hb_tr.animate.set_value(19.4), run_time=0.45)
        self.play(FadeIn(pt20), pc_tr.animate.set_value(16.0), push_tr.animate.set_value(17.0), hb_tr.animate.set_value(16.4), run_time=0.45)
        self.add(pt16)
        self.finish()


class S14Curve(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(16.0)
        push_tr = ValueTracker(17.0)
        hb_tr = ValueTracker(16.4)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=71)
        drops = make_tube_drops(mode="steady_all", seed=72)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
        hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
        hb_num = _make_bar_num(BAR_X_HB, hb_tr, PROTEIN_COL, fmt="{:.1f}")
        tb_dots, tb_line, tb_lbl = add_textbook_plot(P)
        s_dots = add_steady_points(P, up_to=5)
        steady_tag = T("steady state", 24, TEAL).move_to([-5.3, 3.30, 0])
        teach_tag = scope_tag("teaching numbers", size=22, color=TEXT)
        model_tag = T("illustrative model", 22, TEXT).next_to(teach_tag, UP, buff=0.12).align_to(teach_tag, RIGHT)

        self.add(
            world, probe, blood, drops, push_bar, push_num, hb_bar, hb_num,
            tb_dots, tb_line, tb_lbl, s_dots, steady_tag, teach_tag, model_tag
        )

        # Shade textbook absorbs region (17 to 12, below 0)
        abs_poly = Polygon(
            P.pt(17, 0), P.pt(12, 0), P.pt(12, -5),
            stroke_width=0, fill_color=TEXTBOOK_COL, fill_opacity=0.28
        )
        abs_lbl = T("absorbs", 22, TEXTBOOK_COL).move_to(P.pt(16.6, -3.8))
        abs_ptr = Arrow(abs_lbl.get_right() + RIGHT * 0.08, P.pt(13.6, -2.5), buff=0, color=TEXTBOOK_COL, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)

        self.at("textbook line")
        self.play(FadeIn(abs_poly), FadeIn(abs_lbl), GrowArrow(abs_ptr), run_time=0.8)

        # Computed steady curve drawn from 32 down to 12
        draw_pc = ValueTracker(32.0)

        def mk_steady_live():
            cur = draw_pc.get_value()
            xs = np.linspace(32.0, cur, 80) if 32.0 - cur > 0.1 else np.array([32.0, 31.9])
            pts = [P.pt(x, steady_net(x)) for x in xs]
            m = VMobject(stroke_color=WATER_COL, stroke_width=5.5, fill_opacity=0)
            m.set_points_as_corners(pts)
            return m
        live_steady = always_redraw(mk_steady_live)
        self.add(live_steady)

        self.at("steady curve")
        self.play(draw_pc.animate.set_value(22.0), run_time=0.60, rate_func=linear)

        self.at("bends near 22")
        y22 = steady_net(22.0)
        bend_tick = Line(P.pt(22, y22), P.pt(22, 0.4), color=WATER_COL, stroke_width=2.5)
        bend_lbl = T("bend ~22", 24, WATER_COL).move_to(P.pt(22.0, -2.5))
        self.play(Create(bend_tick), FadeIn(bend_lbl), run_time=0.45)

        self.at("flattens just above")
        self.play(draw_pc.animate.set_value(12.0), run_time=1.2, rate_func=linear)

        self.at("hockey stick")
        hs_lbl = T("hockey stick", 24, WATER_COL, weight=BOLD).move_to(P.pt(15.6, 7.6))
        self.play(FadeIn(hs_lbl), run_time=0.45)
        self.finish()


class S15Evidence(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(12.0)
        push_tr = ValueTracker(13.0)
        hb_tr = ValueTracker(12.7)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=81)
        flux_tr = ValueTracker(0.3)
        drops = make_tube_drops(mode="probe", pc_tracker=pc_tr, flux_fn=lambda: flux_tr.get_value(), seed=82)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
        hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
        hb_num = _make_bar_num(BAR_X_HB, hb_tr, PROTEIN_COL, fmt="{:.1f}")
        tb_dots, tb_line, tb_lbl = add_textbook_plot(P)
        s_dots = add_steady_points(P, up_to=5)
        steady_curve = P.curve(steady_net, x0=32.0, x1=12.0, color=WATER_COL, width=5.0)
        abs_poly = Polygon(P.pt(17, 0), P.pt(12, 0), P.pt(12, -5), stroke_width=0, fill_color=TEXTBOOK_COL, fill_opacity=0.28)
        abs_lbl = T("absorbs", 22, TEXTBOOK_COL).move_to(P.pt(16.6, -3.8))
        abs_ptr = Arrow(abs_lbl.get_right() + RIGHT * 0.08, P.pt(13.6, -2.5), buff=0, color=TEXTBOOK_COL, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        steady_tag = T("steady state", 24, TEAL).move_to([-5.3, 3.30, 0])
        teach_tag = scope_tag("teaching numbers", size=22, color=TEXT)
        model_tag = T("illustrative model", 22, TEXT).next_to(teach_tag, UP, buff=0.12).align_to(teach_tag, RIGHT)

        self.add(
            world, probe, blood, drops, push_bar, push_num, hb_bar, hb_num,
            tb_dots, tb_line, tb_lbl, s_dots, steady_curve, abs_poly, abs_lbl, abs_ptr,
            steady_tag, teach_tag, model_tag
        )

        # Frog capillaries tag at top
        self.at("single frog capillaries")
        frog_tag = T("single frog capillaries", 24, PUSH_COL).move_to([-1.8, 3.30, 0])
        self.play(FadeIn(frog_tag), run_time=0.5)

        # Small timer beside probe (in top band) and small circular gap inset at right beside plot
        timer_c = np.array([1.75, 3.30, 0.0])
        clock_bg = Circle(radius=0.22, color=PUSH_COL, stroke_width=2.5).move_to(timer_c)
        clock_angle = ValueTracker(PI / 2)
        clock_hand = always_redraw(lambda: Line(timer_c, timer_c + 0.17 * np.array([np.cos(clock_angle.get_value()), np.sin(clock_angle.get_value()), 0]), color=WATER_COL, stroke_width=3))
        timer_lbl = T("time (schematic)", 22, PUSH_COL).next_to(clock_bg, RIGHT, buff=0.14)

        inset_c = np.array([5.05, -1.05, 0.0])
        inset_ring = Circle(radius=0.80, stroke_color=CELL_COL, stroke_width=3.0, fill_color="#161c28", fill_opacity=0.95).move_to(inset_c)
        inset_ring.layout_ok = True
        inset_mat = Line([inset_c[0] - 0.65, inset_c[1] + 0.25, 0], [inset_c[0] + 0.65, inset_c[1] + 0.25, 0], color=MAT_COL, stroke_width=4.5)
        inset_gold = VGroup(*[
            Dot([inset_c[0] - 0.45 + 0.22 * (k % 5), inset_c[1] - 0.45 + 0.20 * (k // 5), 0], radius=0.055, color=PROTEIN_COL)
            for k in range(10)
        ])
        for d in inset_gold:
            d.layout_ok = True

        self.at("held at low pressure")
        self.play(
            push_tr.animate.set_value(8.0),
            FadeIn(clock_bg), FadeIn(clock_hand), FadeIn(timer_lbl),
            FadeIn(inset_ring), FadeIn(inset_mat), FadeIn(inset_gold),
            run_time=0.7
        )

        self.at("absorbed only briefly")
        # Short inward burst + gold collects under mat as clock hand turns
        self.play(
            flux_tr.animate.set_value(-4.5),
            clock_angle.animate.set_value(PI / 2 - 1.8),
            *[d.animate.shift(UP * 0.35) for d in inset_gold],
            run_time=1.3
        )

        self.at("fell to near zero")
        self.play(
            flux_tr.animate.set_value(0.0),
            hb_tr.animate.set_value(8.0),
            clock_angle.animate.set_value(PI / 2 - 3.6),
            run_time=1.1
        )

        self.at("slight filtration")
        self.play(
            flux_tr.animate.set_value(0.35),
            hb_tr.animate.set_value(7.6),
            clock_angle.animate.set_value(PI / 2 - 4.8),
            run_time=1.0
        )

        self.at("animal vessels")
        animal_tag = T("animal data", 22, TEAL).next_to(model_tag, UP, buff=0.12).align_to(model_tag, RIGHT)
        self.play(FadeIn(animal_tag), run_time=0.5)
        self.finish()


class S16Close(SpokenScene):
    def construct(self):
        world, P, mat, cells = build_world_static()
        pc_tr = ValueTracker(12.0)
        push_tr = ValueTracker(13.0)
        hb_tr = ValueTracker(12.7)
        probe = _make_probe(pc_tr)
        blood = make_blood_stream(seed=91)
        drops = make_tube_drops(mode="steady_all", seed=92)
        push_bar = _make_bar(BAR_X_PUSH, push_tr, PUSH_COL)
        push_num = _make_bar_num(BAR_X_PUSH, push_tr, PUSH_COL)
        hb_bar = _make_bar(BAR_X_HB, hb_tr, PROTEIN_COL)
        hb_num = _make_bar_num(BAR_X_HB, hb_tr, PROTEIN_COL, fmt="{:.1f}")
        tb_dots, tb_line, tb_lbl = add_textbook_plot(P)
        s_dots = add_steady_points(P, up_to=5)
        steady_curve = P.curve(steady_net, x0=32.0, x1=12.0, color=WATER_COL, width=5.0)
        abs_poly = Polygon(P.pt(17, 0), P.pt(12, 0), P.pt(12, -5), stroke_width=0, fill_color=TEXTBOOK_COL, fill_opacity=0.28)
        abs_lbl = T("absorbs", 22, TEXTBOOK_COL).move_to(P.pt(16.6, -3.8))
        abs_ptr = Arrow(abs_lbl.get_right() + RIGHT * 0.08, P.pt(13.6, -2.5), buff=0, color=TEXTBOOK_COL, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        steady_tag = T("steady state", 24, TEAL).move_to([-5.3, 3.30, 0])
        teach_tag = scope_tag("teaching numbers", size=22, color=TEXT)
        model_tag = T("illustrative model", 22, TEXT).next_to(teach_tag, UP, buff=0.12).align_to(teach_tag, RIGHT)
        animal_tag = T("animal data", 22, TEAL).next_to(model_tag, UP, buff=0.12).align_to(model_tag, RIGHT)

        self.add(
            world, probe, blood, drops, push_bar, push_num, hb_bar, hb_num,
            tb_dots, tb_line, tb_lbl, s_dots, steady_curve, abs_poly, abs_lbl, abs_ptr,
            steady_tag, teach_tag, model_tag, animal_tag
        )

        # Tissue drops drifting toward bottom edge of tissue band
        tiss_drops = VGroup()
        for k in range(8):
            x = TUBE_X0 + 1.7 + k * 0.86
            d = Dot([x, TISS_Y1 - 0.28, 0], radius=0.06, color=WATER_COL).set_opacity(0.85)
            d.layout_ok = True
            tiss_drops.add(d)
        self.add(tiss_drops)

        self.at("protein's pull")
        hb_glow = Rectangle(
            width=BAR_W + 0.08, height=12.7 * BAR_SCALE + 0.06,
            stroke_color=PROTEIN_COL, stroke_width=3.5, fill_opacity=0.0
        ).move_to([BAR_X_HB, BAR_Y0 + 6.35 * BAR_SCALE, 0])
        hb_glow.layout_ok = True
        self.play(FadeIn(hb_glow), steady_curve.animate.set_stroke(width=8.5), run_time=0.8)

        self.at("not turn it around")
        self.play(FadeOut(abs_poly), FadeOut(abs_lbl), FadeOut(abs_ptr), run_time=0.7)

        self.at("another way home")
        exit_arr = Arrow([4.95, -0.45, 0], [4.95, -1.85, 0], buff=0, color=PUSH_COL, stroke_width=4.5, max_tip_length_to_length_ratio=0.28)
        q_mark = T("?", 34, PUSH_COL, weight=BOLD).next_to(exit_arr, RIGHT, buff=0.16)
        self.play(
            *[d.animate.set_y(TISS_Y0 + 0.14) for d in tiss_drops],
            GrowArrow(exit_arr), FadeIn(q_mark),
            run_time=1.0
        )
        self.finish()


class S17End(EndCard):
    LINE = "Protein can slow filtration, but cannot reverse it for long."
