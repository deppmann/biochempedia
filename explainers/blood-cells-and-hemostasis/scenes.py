"""
The Ratio Nobody Regulates — animation scenes for Blood Cells, Hematocrit and Clotting.

COLOUR MAP (one colour per concept, same in every scene):
    RED     (#FC6255) : red blood cells, packed red-cell column, hematocrit numerator, progenitors/reticulocytes
    AMBER   (#F2A93B) : blood plasma, plasma column, diuresis drop, indicator-dilution tracer
    CYAN    (#58C4DD) : oxygen (tissue O2 gauges, oxygen wash, oxygen halo, O2 input chip)
    MAGENTA (#E066FF) : erythropoietin (EPO) and HIF-2 alpha switch (blocks, EPO gene, hormone dots, EPO curve)
    SLATE   (#8E9AAF) : kidney tissue outlines, tubules, hydroxylase enzyme hexagon
    TAN     (#C8A97E) : bone marrow block
    TEXT    (#E8EAF0) : whole blood total, hematocrit ratio/marker/brackets, day counter, question text

THE ONE CARRIED WORLD:
    Left: vertical 0-60% hematocrit scale alongside a spun-blood tube (RED packed cells below, AMBER plasma
    above, WHITE marker and readout tracking computed Hct = V_red / (V_red + V_plasma)).
    Right: horizontal blood vessel band with RED cells flowing left-to-right; above it a TAN bone marrow
    block opening onto the vessel; below it a SLATE kidney tissue patch with three tubules and two
    interstitial cells carrying CYAN oxygen gauges. A 'schematic' tag sits at bottom right all film.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s00_hook      : Two spun tubes (untrained 44% vs trained 38% from V_red/V_tot) stand side by side while
                    RED dot stacks count up (5 vs 7) so the trained stack grows taller despite the shorter red layer.
    s02_ratio     : Zoomed tube divides into labelled volumes (2.2 L red, 2.8 L plasma, 5.0 L total) that
                    compose into the computed fraction 2.2 / 5.0 = 44% while the scale marker snaps to 44%.
    s03_two_knobs : Single live ValueTrackers (v_red, v_plasma) drive column heights, bracket total, fraction
                    terms, and scale marker together as red cells rise (2.2->3.1 L, 52%) then plasma rises (2.8->4.0 L, 36%).
    s04_plasma    : Ghost 44% line remains fixed while v_red and v_plasma step through pregnancy (+plasma > +red,
                    Hct falls) and altitude diuresis (-plasma, red held still, Hct rises).
    s05_mass      : Pull back to full world; indicator-dilution syringe and CO-rebreathing mask cards pulse and
                    shrink to chips; tube marker is circled as 'a share' apart from a dashed vessel dot-grid 'a count'.
    s06_idea      : Ratio readout dims; RED numerator brightens as a MAGENTA EPO arrow connects kidney to marrow
                    to vessel; camera pushes toward kidney where tight CYAN halos illuminate only the two cells.
    s07_kidney    : Kidney patch fills frame; dashed tubule-interior outline is struck through; CYAN tissue wash
                    is visibly paler than vessel wash; vessel red cells thin and CYAN oxygen gauges drop step.
    s08_hif       : Single interstitial cell fills frame; under bright CYAN O2 wash, hydroxylase tags MAGENTA
                    HIF-2 alpha blocks to 'destroyed'; when O2 falls, hydroxylase dims and blocks activate 'EPO gene'.
    s09_predict   : Full world with schematic day counter (0->2) and two computed curves: EPO rises steeply over
                    days 0-2 and begins to ease while new red cells remain flat; MAGENTA dots stream kidney->marrow.
    s11_answer    : Open marrow shows 4 progenitors (2 begin crumbling before EPO saves all 4); cells divide into
                    8 reticulocytes exiting into the vessel as days 2->4 tick and the RED curve climbs behind EPO.
    s12_close     : Full world recaps rapid plasma swings (marker down/up, RED still), dims ratio/dial, fires
                    kidney O2 halo -> marrow -> new red cells, and finally steps the tube RED column and marker up.
"""

import numpy as np
from bp_parts import *

AMBER = "#F2A93B"
CYAN = BLUE          # #58C4DD
MAGENTA = "#E066FF"
SLATE = "#8E9AAF"
TAN = "#C8A97E"

RNG_SEED = 7


def _hct(v_red, v_plasma):
    return 100.0 * v_red / max(v_red + v_plasma, 1e-6)


def _rbc_disc(radius_x=0.14, radius_y=0.08, color=RED, opacity=0.92):
    outer = Ellipse(width=2 * radius_x, height=2 * radius_y, color=color, stroke_width=1.5,
                    fill_color=color, fill_opacity=opacity)
    dimple = Ellipse(width=1.05 * radius_x, height=0.85 * radius_y, color="#9E2B22", stroke_width=0,
                     fill_color="#9E2B22", fill_opacity=0.55)
    return VGroup(outer, dimple)


def _retic_disc(radius_x=0.14, radius_y=0.082):
    base = _rbc_disc(radius_x, radius_y, color=RED, opacity=0.92)
    specks = VGroup(
        Dot([-0.04, 0.015, 0], radius=0.018, color=TEXT),
        Dot([0.035, -0.015, 0], radius=0.018, color=TEXT),
        Dot([0.005, 0.025, 0], radius=0.015, color=TEXT),
    )
    return VGroup(base, specks)


def _attach_drift(mob, vx, x0, x1):
    mob._vx, mob._x0, mob._x1 = vx, x0, x1

    def _drift(m, dt):
        m.shift(RIGHT * m._vx * dt)
        if m.get_center()[0] > m._x1:
            m.shift(LEFT * (m._x1 - m._x0))

    mob.add_updater(_drift)
    return mob


def make_vessel_band(x0=-1.4, x1=6.1, y_mid=0.15, height=1.05, n_cells=12, speed=0.9, seed=RNG_SEED, cell_rx=None):
    """Horizontal blood vessel band with continuously drifting red cells (left -> right)."""
    rng = np.random.default_rng(seed)
    w = x1 - x0
    wall_top = Line([x0, y_mid + height / 2, 0], [x1, y_mid + height / 2, 0], color=SLATE, stroke_width=3)
    wall_bot = Line([x0, y_mid - height / 2, 0], [x1, y_mid - height / 2, 0], color=SLATE, stroke_width=3)
    lumen = Rectangle(width=w, height=height, stroke_width=0, fill_color=RED, fill_opacity=0.08).move_to([(x0 + x1) / 2, y_mid, 0])
    lumen.layout_ok = True

    cells = VGroup()
    sx = cell_rx if cell_rx is not None else max(0.095, min(0.15, height * 0.14))
    sy = sx * 0.58
    for i in range(n_cells):
        c = _rbc_disc(sx, sy)
        cx = x0 + (i + rng.uniform(0.15, 0.85)) * (w / n_cells)
        cy = y_mid + rng.uniform(-height * 0.28, height * 0.28)
        c.move_to([cx, cy, 0])
        _attach_drift(c, speed * rng.uniform(0.85, 1.15), x0 + 0.18, x1 - 0.18)
        cells.add(c)
    cells.layout_ok = True
    band = VGroup(lumen, wall_bot, wall_top, cells)
    band.lumen = lumen
    band.cells = cells
    band.y_mid = y_mid
    band.x0, band.x1 = x0, x1
    band.height_val = height
    return band


def make_marrow_block(center=(2.4, 2.0, 0), width=3.8, height=1.25, label="marrow", label_size=26):
    """Pale TAN bone marrow block with an opening facing down toward the vessel."""
    cx, cy, _ = center
    hw, hh = width / 2, height / 2
    gap_hw = min(0.45, width * 0.14)
    pts = [
        [cx - gap_hw, cy - hh, 0],
        [cx - hw, cy - hh, 0],
        [cx - hw, cy + hh, 0],
        [cx + hw, cy + hh, 0],
        [cx + hw, cy - hh, 0],
        [cx + gap_hw, cy - hh, 0],
    ]
    outline = VMobject(color=TAN, stroke_width=3).set_points_as_corners(pts)
    fill = RoundedRectangle(corner_radius=0.08, width=width, height=height, stroke_width=0,
                            fill_color=TAN, fill_opacity=0.16).move_to(center)
    fill.layout_ok = True
    lab = T(label, size=label_size, color=TAN).move_to(center) if label else VGroup()
    g = VGroup(fill, outline, lab)
    g.fill_rect = fill
    g.outline = outline
    g.label_mob = lab
    g.opening = np.array([cx, cy - hh, 0.0])
    return g


def make_interstitial_cell(pos, gauge_tracker=None, star=False, scale=1.0, gauge_val=0.55, gauge_scale=1.0):
    """Round or fibroblast-like interstitial cell with a CYAN oxygen gauge."""
    if star:
        angles = np.linspace(0, TAU, 10, endpoint=False)
        radii = [0.34 * scale if i % 2 == 0 else 0.17 * scale for i in range(10)]
        pts = [[pos[0] + r * np.cos(a), pos[1] + r * np.sin(a), 0] for a, r in zip(angles, radii)]
        body = Polygon(*pts, color=TEXT, stroke_width=2.5, fill_color=SLATE, fill_opacity=0.35)
    else:
        body = Circle(radius=0.22 * scale, color=TEXT, stroke_width=2.2, fill_color=SLATE, fill_opacity=0.35).move_to(pos)

    gw, gh = 0.28 * scale * gauge_scale, 0.09 * scale * gauge_scale
    g_pos = np.array([pos[0], pos[1], 0.0]) + DOWN * (0.45 * scale if star else 0.30 * scale)
    g_bg = Rectangle(width=gw, height=gh, color=CYAN, stroke_width=1.8, fill_color=BG, fill_opacity=0.9).move_to(g_pos)

    if gauge_tracker is not None:
        def _mk_bar():
            frac = float(np.clip(gauge_tracker.get_value(), 0.08, 1.0))
            bw = max(0.02, gw * frac)
            bar = Rectangle(width=bw, height=gh * 0.72, stroke_width=0, fill_color=CYAN, fill_opacity=0.95)
            bar.move_to([g_pos[0] - gw / 2 + bw / 2, g_pos[1], 0])
            return bar
        g_bar = always_redraw(_mk_bar)
    else:
        bw = gw * gauge_val
        g_bar = Rectangle(width=bw, height=gh * 0.72, stroke_width=0, fill_color=CYAN, fill_opacity=0.95)
        g_bar.move_to([g_pos[0] - gw / 2 + bw / 2, g_pos[1], 0])

    g = VGroup(body, g_bg, g_bar)
    g.body = body
    g.gauge = VGroup(g_bg, g_bar)
    g.cell_center = np.array(pos, dtype=float)
    return g


def make_kidney_patch(center=(2.4, -1.75, 0), width=4.8, height=1.95, gauge_tracker=None, star_cells=False, show_label=True):
    """SLATE kidney tissue patch with 3 tubule outlines and 2 interstitial cells between them."""
    cx, cy, _ = center
    patch_box = RoundedRectangle(corner_radius=0.22, width=width, height=height, color=SLATE,
                                 stroke_width=2.2, fill_color=SLATE, fill_opacity=0.08).move_to(center)
    patch_box.layout_ok = True

    tub_w = width * 0.22
    tub_h = height * 0.62
    xs = [cx - width * 0.31, cx, cx + width * 0.31]
    tubules = VGroup(*[
        RoundedRectangle(corner_radius=tub_w * 0.42, width=tub_w, height=tub_h, color=SLATE,
                         stroke_width=2.5, fill_color=BG, fill_opacity=0.6).move_to([x, cy + height * 0.05, 0])
        for x in xs
    ])
    c_scale = min(1.35, width / 4.2)
    c1 = make_interstitial_cell([cx - width * 0.155, cy + height * 0.06, 0], gauge_tracker=gauge_tracker,
                                star=star_cells, scale=c_scale)
    c2 = make_interstitial_cell([cx + width * 0.155, cy + height * 0.06, 0], gauge_tracker=gauge_tracker,
                                star=star_cells, scale=c_scale)

    lab = T("kidney", size=24, color=SLATE).next_to(patch_box, DOWN, buff=0.14) if show_label else VGroup()
    g = VGroup(patch_box, tubules, c1, c2, lab)
    g.patch_box = patch_box
    g.tubules = tubules
    g.cells = [c1, c2]
    g.label_mob = lab
    return g


def make_scale(x=-5.4, y_bot=-2.1, h_full=4.2, tick_step=20, tick_size=22):
    """Vertical 0-60% scale whose 0..60 span equals 0..60% of h_full."""
    y_60 = y_bot + 0.60 * h_full
    axis = Line([x, y_bot, 0], [x, y_60, 0], color=TEXT, stroke_width=2.5)
    ticks = VGroup()
    labels = VGroup()
    for val in range(0, 61, tick_step):
        y = y_bot + (val / 100.0) * h_full
        tk = Line([x - 0.12, y, 0], [x, y, 0], color=TEXT, stroke_width=2.5)
        lb = M(f"{val}%", size=tick_size, color=TEXT).next_to(tk, LEFT, buff=0.08)
        ticks.add(tk)
        labels.add(lb)
    g = VGroup(axis, ticks, labels)
    g.x_axis = axis
    g.y_bot = y_bot
    g.h_full = h_full
    return g


def make_static_tube(x=-4.4, y_bot=-2.1, h_full=4.2, width=0.72, hct_frac=0.44, label=None, label_pos="below"):
    """Fixed-height spun blood tube (packed RED below, AMBER plasma above)."""
    h_red = hct_frac * h_full
    h_amb = (1.0 - hct_frac) * h_full
    red_col = Rectangle(width=width, height=h_red, stroke_width=0, fill_color=RED, fill_opacity=0.82)
    red_col.move_to([x, y_bot + h_red / 2, 0])
    amb_col = Rectangle(width=width, height=h_amb, stroke_width=0, fill_color=AMBER, fill_opacity=0.68)
    amb_col.move_to([x, y_bot + h_red + h_amb / 2, 0])
    border = RoundedRectangle(corner_radius=0.08, width=width, height=h_full, color=TEXT, stroke_width=2.5,
                              fill_opacity=0).move_to([x, y_bot + h_full / 2, 0])
    g = VGroup(red_col, amb_col, border)
    if label:
        lb = T(label, size=24, color=TEXT)
        if label_pos == "above":
            lb.next_to(border, UP, buff=0.16)
        else:
            lb.next_to(border, DOWN, buff=0.16)
        g.add(lb)
        g.label_mob = lb
    g.red_col = red_col
    g.amb_col = amb_col
    g.border = border
    return g


def make_live_tube(v_red_tr, v_plasma_tr, x=-4.4, y_bot=-2.1, h_per_l=0.78, width=0.82, scale_h_full=None):
    """Tube whose RED and AMBER heights are computed live from v_red_tr and v_plasma_tr (in litres)."""
    if scale_h_full is None:
        scale_h_full = 5.0 * h_per_l

    def _mk_red():
        hr = max(0.05, v_red_tr.get_value() * h_per_l)
        r = Rectangle(width=width, height=hr, stroke_width=0, fill_color=RED, fill_opacity=0.82)
        r.move_to([x, y_bot + hr / 2, 0])
        return r

    def _mk_amb():
        hr = max(0.05, v_red_tr.get_value() * h_per_l)
        ha = max(0.05, v_plasma_tr.get_value() * h_per_l)
        a = Rectangle(width=width, height=ha, stroke_width=0, fill_color=AMBER, fill_opacity=0.68)
        a.move_to([x, y_bot + hr + ha / 2, 0])
        return a

    def _mk_border():
        ht = max(0.2, (v_red_tr.get_value() + v_plasma_tr.get_value()) * h_per_l)
        return RoundedRectangle(corner_radius=0.08, width=width, height=ht, color=TEXT,
                                stroke_width=2.5, fill_opacity=0).move_to([x, y_bot + ht / 2, 0])

    return VGroup(always_redraw(_mk_red), always_redraw(_mk_amb), always_redraw(_mk_border))


def make_scale_marker(v_red_tr, v_plasma_tr, scale_x=-5.4, y_bot=-2.1, h_full=4.2, tube_left=-4.76, show_readout=False, readout_at=None, opacity_tr=None):
    """WHITE pointer on the 0-60% scale driven by computed Hct = 100 * v_red / (v_red + v_plasma)."""
    if opacity_tr is None:
        opacity_tr = ValueTracker(1.0)

    def _mk_ptr():
        op = float(np.clip(opacity_tr.get_value(), 0.0, 1.0))
        hct = _hct(v_red_tr.get_value(), v_plasma_tr.get_value())
        y = y_bot + (hct / 100.0) * h_full
        tri = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=op, stroke_width=0).scale(0.11).rotate(-PI / 2)
        tri.move_to([scale_x + 0.14, y, 0])
        tick = Line([scale_x, y, 0], [tube_left - 0.04, y, 0], color=TEXT, stroke_width=3, stroke_opacity=op)
        g = VGroup(tri, tick)
        if show_readout:
            ro = M(f"{hct:.0f}%", size=26, color=TEXT).set_opacity(op)
            if readout_at is not None:
                ro.move_to(readout_at)
            else:
                ro.move_to([scale_x + 0.35, y_bot + 0.60 * h_full + 0.36, 0])
            g.add(ro)
        return g
    m = always_redraw(_mk_ptr)
    m.opacity_tr = opacity_tr
    return m


def build_full_world(v_red=2.2, v_plasma=2.8, gauge_val=0.55, show_tube_readout=True, show_teaching_tag=True):
    """Standard full-world layout reused across s00, s01, s05, s06, s09, s10, s12."""
    v_red_tr = ValueTracker(v_red)
    v_pl_tr = ValueTracker(v_plasma)
    o2_tr = ValueTracker(gauge_val)

    scale = make_scale(x=-5.35, y_bot=-2.15, h_full=4.2)
    tube = make_live_tube(v_red_tr, v_pl_tr, x=-4.45, y_bot=-2.15, h_per_l=4.2 / 5.0, width=0.72, scale_h_full=4.2)
    marker = make_scale_marker(v_red_tr, v_pl_tr, scale_x=-5.35, y_bot=-2.15, h_full=4.2,
                               tube_left=-4.45 - 0.36, show_readout=show_tube_readout,
                               readout_at=[-5.35, -2.15 + 0.60 * 4.2 + 0.38, 0])
    marrow = make_marrow_block(center=(2.6, 2.0, 0), width=3.8, height=1.25)
    vessel = make_vessel_band(x0=-0.6, x1=6.1, y_mid=0.15, height=1.05, n_cells=12, speed=0.9)
    kidney = make_kidney_patch(center=(2.6, -1.75, 0), width=4.6, height=1.95, gauge_tracker=o2_tr)

    tags = VGroup(scope_tag("schematic"))
    if show_teaching_tag:
        t_num = T("teaching numbers", size=22, color=SLATE).move_to([-4.45, -3.1, 0])
        tags.add(t_num)

    world = VGroup(scale, tube, marker, marrow, vessel, kidney, tags)
    world.scale_mob = scale
    world.tube = tube
    world.marker = marker
    world.marrow = marrow
    world.vessel = vessel
    world.kidney = kidney
    world.tags = tags
    world.v_red_tr = v_red_tr
    world.v_pl_tr = v_pl_tr
    world.o2_tr = o2_tr
    return world


def build_zoom_tube_world(v_red=2.2, v_plasma=2.8, show_readout=False):
    """Tube zoomed at left (~65% frame height), compact marrow/vessel/kidney on far right."""
    h_per_l = 0.72
    h_full = 5.0 * h_per_l
    y_bot = -2.25
    v_red_tr = ValueTracker(v_red)
    v_pl_tr = ValueTracker(v_plasma)
    o2_tr = ValueTracker(0.55)

    scale = make_scale(x=-5.45, y_bot=y_bot, h_full=h_full)
    tube = make_live_tube(v_red_tr, v_pl_tr, x=-4.5, y_bot=y_bot, h_per_l=h_per_l, width=0.82, scale_h_full=h_full)
    marker = make_scale_marker(v_red_tr, v_pl_tr, scale_x=-5.45, y_bot=y_bot, h_full=h_full,
                               tube_left=-4.5 - 0.41, show_readout=show_readout,
                               readout_at=[-5.45, y_bot + 0.60 * h_full + 0.36, 0])

    # Compact right-side world (x: +2.6 to +6.1) with crisp visible drifting red cells
    marrow = make_marrow_block(center=(4.35, 1.95, 0), width=3.0, height=1.0, label="marrow", label_size=22)
    vessel = make_vessel_band(x0=2.6, x1=6.1, y_mid=0.25, height=1.08, n_cells=11, speed=1.4, cell_rx=0.145)
    kidney = make_kidney_patch(center=(4.35, -1.55, 0), width=3.2, height=1.6, gauge_tracker=o2_tr, show_label=False)

    t_num = T("teaching numbers", size=22, color=SLATE).move_to([-4.5, -3.1, 0])
    tags = VGroup(scope_tag("schematic"), t_num)

    world = VGroup(scale, tube, marker, marrow, vessel, kidney, tags)
    world.scale_mob = scale
    world.tube = tube
    world.marker = marker
    world.marrow = marrow
    world.vessel = vessel
    world.kidney = kidney
    world.tags = tags
    world.v_red_tr = v_red_tr
    world.v_pl_tr = v_pl_tr
    world.h_per_l = h_per_l
    world.h_full = h_full
    world.y_bot = y_bot
    return world


def _epo_curve(day):
    """Smooth schematic EPO curve (0..1): peaks around day 1.5 then eases smoothly while staying above baseline."""
    if day <= 0:
        return 0.12
    peak = 0.48 * (day / 1.35) * np.exp(1.0 - day / 1.35)
    plateau = 0.34 * (1.0 - np.exp(-day / 0.6))
    return float(np.clip(0.12 + peak + plateau, 0.12, 0.92))


def _retic_curve(day):
    """Smooth schematic new red cells curve (0..1): flat through day 2, rises gradually over days 2.2..4."""
    if day <= 2.0:
        return 0.12
    return float(np.clip(0.12 + 0.72 * ((day - 2.0) / 2.2) ** 1.4, 0.12, 0.86))


def build_predict_world(day_val=2.0):
    """Full world + schematic EPO and new-red-cells tracks at the right (used in s09_predict and s10_pause)."""
    v_red_tr = ValueTracker(2.2)
    v_pl_tr = ValueTracker(2.8)
    o2_tr = ValueTracker(0.32)
    day_tr = ValueTracker(day_val)

    scale = make_scale(x=-5.45, y_bot=-2.15, h_full=4.0)
    tube = make_live_tube(v_red_tr, v_pl_tr, x=-4.65, y_bot=-2.15, h_per_l=4.0 / 5.0, width=0.66, scale_h_full=4.0)
    marker = make_scale_marker(v_red_tr, v_pl_tr, scale_x=-5.45, y_bot=-2.15, h_full=4.0,
                               tube_left=-4.65 - 0.33, show_readout=False)

    marrow = make_marrow_block(center=(-1.05, 1.75, 0), width=3.1, height=1.1, label="marrow", label_size=24)
    vessel = make_vessel_band(x0=-3.3, x1=1.35, y_mid=0.05, height=0.95, n_cells=9, speed=0.75)
    kidney = make_kidney_patch(center=(-1.05, -1.75, 0), width=3.6, height=1.75, gauge_tracker=o2_tr, show_label=True)

    p_epo = Plot(box=(2.1, 6.0, 0.65, 2.35), xr=(0, 4.2), yr=(0, 1.0), xticks=[], yticks=[],
                 xlabel="", ylabel="", color=SLATE, stroke=2.5)
    epo_lab = T("EPO in plasma", size=24, color=MAGENTA).next_to([2.1, 2.35, 0], UP, buff=0.12).align_to([2.1, 0, 0], LEFT)
    epo_line = p_epo.live_curve(_epo_curve, day_tr, color=MAGENTA, width=5)

    p_red = Plot(box=(2.1, 6.0, -2.05, -0.35), xr=(0, 4.2), yr=(0, 1.0), xticks=[], yticks=[],
                 xlabel="", ylabel="", color=SLATE, stroke=2.5)
    red_lab = T("new red cells", size=24, color=RED).next_to([2.1, -0.35, 0], UP, buff=0.12).align_to([2.1, 0, 0], LEFT)
    red_line = p_red.live_curve(_retic_curve, day_tr, color=RED, width=5)

    day_readout = counter("day {:.0f}", day_tr, at=[5.05, 3.15, 0], size=30, color=TEXT)
    t_num = T("teaching numbers", size=22, color=SLATE).move_to([-4.65, -3.1, 0])
    tags = VGroup(scope_tag("schematic"), t_num)

    world = VGroup(scale, tube, marker, marrow, vessel, kidney,
                   p_epo, epo_lab, epo_line, p_red, red_lab, red_line, day_readout, tags)
    world.day_tr = day_tr
    world.marrow = marrow
    world.vessel = vessel
    world.kidney = kidney
    world.p_epo = p_epo
    world.p_red = p_red
    world.day_readout = day_readout
    return world


# ==============================================================================
# SCENES
# ==============================================================================

class S00Hook(SpokenScene):
    def construct(self):
        marrow = make_marrow_block(center=(2.6, 2.0, 0), width=3.8, height=1.25)
        vessel = make_vessel_band(x0=-0.6, x1=6.1, y_mid=0.15, height=1.05, n_cells=12, speed=0.9)
        o2_tr = ValueTracker(0.55)
        kidney = make_kidney_patch(center=(2.6, -1.75, 0), width=4.6, height=1.95, gauge_tracker=o2_tr)
        tag = scope_tag("schematic")

        y_bot, h_full = -2.05, 4.0
        scale = make_scale(x=-5.55, y_bot=y_bot, h_full=h_full)
        tube_un = make_static_tube(x=-4.8, y_bot=y_bot, h_full=h_full, width=0.64, hct_frac=0.44,
                                   label="untrained", label_pos="below")
        tube_tr = make_static_tube(x=-3.25, y_bot=y_bot, h_full=h_full, width=0.64, hct_frac=0.38,
                                   label="trained", label_pos="below")

        y_un = y_bot + 0.44 * h_full
        ptr = VGroup(
            Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=0).scale(0.1).rotate(-PI / 2).move_to([-5.42, y_un, 0]),
            Line([-5.55, y_un, 0], [-5.14, y_un, 0], color=TEXT, stroke_width=3),
            M("44%", size=24, color=TEXT).move_to([-5.55, y_bot + 0.60 * h_full + 0.34, 0]),
        )

        self.add(marrow, vessel, kidney, tag, scale, tube_un, tube_tr, ptr)
        # Tubes settle cleanly during "Two tubes of spun blood"
        tube_un.red_col.save_state()
        tube_tr.red_col.save_state()
        self.play(Indicate(tube_un.border, color=TEXT, scale_factor=1.03),
                  Indicate(tube_tr.border, color=TEXT, scale_factor=1.03), run_time=2.2)

        self.at("shorter red layer")
        un_dots = VGroup(*[Dot([-4.22, y_bot + 0.14 + i * 0.28, 0], radius=0.095, color=RED) for i in range(5)])
        tr_dots = VGroup(*[Dot([-2.67, y_bot + 0.14 + i * 0.28, 0], radius=0.095, color=RED) for i in range(7)])
        short_bar = Line([-3.65, y_bot + 0.38 * h_full, 0], [-2.85, y_bot + 0.38 * h_full, 0], color=TEXT, stroke_width=3)
        self.play(Create(short_bar), run_time=0.8)

        self.at("carry more")
        self.play(LaggedStart(*[FadeIn(d, scale=1.2) for d in un_dots], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(d, scale=1.2) for d in tr_dots], lag_ratio=0.16),
                  run_time=2.4)

        self.at("how does")
        q = T("Fewer? Or more?", size=34, color=TEXT).move_to([0.0, 3.15, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.wait(0.7)

        self.play(
            FadeOut(VGroup(tube_tr, un_dots, tr_dots, short_bar), shift=DOWN * 0.4),
            tube_un.animate.shift(RIGHT * 0.35),
            ptr[1].animate.put_start_and_end_on([-5.35, y_un, 0], [-4.83, y_un, 0]),
            ptr[0].animate.move_to([-5.22, y_un, 0]),
            ptr[2].animate.move_to([-5.35, y_bot + 0.60 * h_full + 0.34, 0]),
            scale.animate.shift(RIGHT * 0.2),
            run_time=0.75,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = build_full_world(v_red=2.2, v_plasma=2.8, gauge_val=0.55, show_tube_readout=True, show_teaching_tag=False)
        world.v_red_tr.set_value(1.85)
        q = T("Fewer? Or more?", size=34, color=TEXT).move_to([0.0, 3.15, 0])
        title = T("The Ratio Nobody Regulates", size=42, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.15, 0])

        self.add(world, q)
        self.play(swap(q, title, run_time=0.7), world.v_red_tr.animate(run_time=1.2).set_value(2.2))
        self.wait(0.7)
        self.finish()


class S02Ratio(SpokenScene):
    def construct(self):
        world = build_zoom_tube_world(v_red=2.2, v_plasma=2.8, show_readout=False)
        y_bot, h_per_l = world.y_bot, world.h_per_l
        # Start marker near 0 and tube columns settling smoothly as hematocrit definition is spoken
        world.v_red_tr.set_value(1.6)
        world.v_pl_tr.set_value(3.4)
        self.add(world)

        self.at("packed red cells")
        lab_red_name = T("red cells", size=28, color=RED).move_to([-2.72, y_bot + 1.1 * h_per_l, 0])
        # Packed red column rises smoothly to 2.2 L as narrator explains "volume of packed red cells"
        self.play(world.v_red_tr.animate(run_time=2.2).set_value(2.2),
                  world.v_pl_tr.animate(run_time=2.2).set_value(2.8),
                  FadeIn(lab_red_name, shift=RIGHT * 0.15, run_time=1.0))

        self.at("whole blood")
        y_top = y_bot + 5.0 * h_per_l
        bx = -1.25
        bracket = VGroup(
            Line([bx - 0.12, y_bot, 0], [bx, y_bot, 0], color=TEXT, stroke_width=3),
            Line([bx, y_bot, 0], [bx, y_top, 0], color=TEXT, stroke_width=3),
            Line([bx - 0.12, y_top, 0], [bx, y_top, 0], color=TEXT, stroke_width=3),
        )
        lab_tot_name = T("whole blood", size=28, color=TEXT).move_to([0.05, y_top - 0.35, 0])
        self.play(Create(bracket, run_time=1.6), FadeIn(lab_tot_name, shift=RIGHT * 0.1, run_time=1.0))

        self.at("untrained adult")
        tube_hi = Rectangle(width=0.72, height=5.0 * h_per_l - 0.10, color=TEXT, stroke_width=4,
                            fill_color=TEXT, fill_opacity=0.18).move_to([-4.5, y_bot + 2.5 * h_per_l, 0])
        self.play(FadeIn(tube_hi, run_time=0.5), Indicate(bracket, color=TEXT, scale_factor=1.05, run_time=1.1))
        self.play(FadeOut(tube_hi, run_time=0.45))

        self.at("2 2")
        lab_red = T("2.2 L red cells", size=28, color=RED).move_to([-2.72, y_bot + 1.1 * h_per_l, 0])
        red_hi = Rectangle(width=0.72, height=2.2 * h_per_l - 0.10, color=RED, stroke_width=4.5,
                           fill_color=RED, fill_opacity=0.25).move_to([-4.5, y_bot + 1.1 * h_per_l, 0])
        self.play(FadeIn(red_hi, run_time=0.4),
                  swap(lab_red_name, lab_red, run_time=0.8),
                  Indicate(world.tube[0], color=RED, scale_factor=1.05, run_time=1.2))
        self.play(FadeOut(red_hi, run_time=0.4))

        self.at("2 8")
        lab_pl = T("2.8 L plasma", size=28, color=AMBER).move_to([-2.72, y_bot + (2.2 + 1.4) * h_per_l, 0])
        lab_tot = T("5.0 L blood", size=28, color=TEXT).move_to([-0.15, y_top - 0.35, 0])
        pl_hi = Rectangle(width=0.72, height=2.8 * h_per_l - 0.10, color=AMBER, stroke_width=4.5,
                          fill_color=AMBER, fill_opacity=0.25).move_to([-4.5, y_bot + (2.2 + 1.4) * h_per_l, 0])
        self.play(FadeIn(pl_hi, run_time=0.4),
                  FadeIn(lab_pl, shift=RIGHT * 0.15, run_time=0.9),
                  Indicate(world.tube[1], color=AMBER, scale_factor=1.05, run_time=1.3))
        self.play(FadeOut(pl_hi, run_time=0.4),
                  swap(lab_tot_name, lab_tot, run_time=0.8),
                  Indicate(bracket, color=TEXT, scale_factor=1.04, run_time=1.0))

        self.at("44 percent")
        fx, fy = 0.45, -0.35
        num = M("2.2", size=32, color=RED).move_to([fx, fy + 0.38, 0])
        bar = Line([fx - 0.52, fy, 0], [fx + 0.52, fy, 0], color=TEXT, stroke_width=3)
        den = M("5.0", size=32, color=TEXT).move_to([fx, fy - 0.38, 0])
        eq = M("=", size=34, color=TEXT).move_to([fx + 0.85, fy, 0])
        pct = M("44%", size=34, color=TEXT).move_to([fx + 1.55, fy, 0])

        src_num = M("2.2", size=28, color=RED).move_to(lab_red.get_left() + RIGHT * 0.35)
        src_den = M("5.0", size=28, color=TEXT).move_to(lab_tot.get_left() + RIGHT * 0.35)
        self.add(src_num, src_den)
        self.play(Transform(src_num, num), Transform(src_den, den), Create(bar), run_time=0.7)
        self.play(FadeIn(eq), FadeIn(pct, scale=1.15), Indicate(world.marker, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.finish()


class S03TwoKnobs(SpokenScene):
    def construct(self):
        world = build_zoom_tube_world(v_red=2.2, v_plasma=2.8, show_readout=False)
        y_bot, h_per_l = world.y_bot, world.h_per_l
        v_r, v_p = world.v_red_tr, world.v_pl_tr

        lab_red = always_redraw(lambda: T(f"{v_r.get_value():.1f} L red cells", size=28, color=RED)
                                .move_to([-2.72, y_bot + 0.5 * v_r.get_value() * h_per_l, 0]))
        lab_pl = always_redraw(lambda: T(f"{v_p.get_value():.1f} L plasma", size=28, color=AMBER)
                               .move_to([-2.72, y_bot + (v_r.get_value() + 0.5 * v_p.get_value()) * h_per_l, 0]))
        bx = -1.25

        def _mk_bracket():
            y_top = y_bot + (v_r.get_value() + v_p.get_value()) * h_per_l
            return VGroup(
                Line([bx - 0.12, y_bot, 0], [bx, y_bot, 0], color=TEXT, stroke_width=3),
                Line([bx, y_bot, 0], [bx, y_top, 0], color=TEXT, stroke_width=3),
                Line([bx - 0.12, y_top, 0], [bx, y_top, 0], color=TEXT, stroke_width=3),
            )
        bracket = always_redraw(_mk_bracket)
        lab_tot = always_redraw(lambda: T(f"{v_r.get_value() + v_p.get_value():.1f} L blood", size=28, color=TEXT)
                                .move_to([-0.15, y_bot + (v_r.get_value() + v_p.get_value()) * h_per_l - 0.35, 0]))

        fx, fy = 0.45, -0.35
        num = always_redraw(lambda: M(f"{v_r.get_value():.1f}", size=32, color=RED).move_to([fx, fy + 0.38, 0]))
        bar = Line([fx - 0.52, fy, 0], [fx + 0.52, fy, 0], color=TEXT, stroke_width=3)
        den = always_redraw(lambda: M(f"{round(v_r.get_value(), 1) + round(v_p.get_value(), 1):.1f}", size=32, color=TEXT).move_to([fx, fy - 0.38, 0]))
        eq = M("=", size=34, color=TEXT).move_to([fx + 0.85, fy, 0])
        pct = always_redraw(lambda: M(f"{_hct(round(v_r.get_value(), 1), round(v_p.get_value(), 1)):.0f}%", size=34, color=TEXT).move_to([fx + 1.55, fy, 0]))

        self.add(world, lab_red, lab_pl, bracket, lab_tot, num, bar, den, eq, pct)

        self.at("its top")
        box_top = SurroundingRectangle(num, color=RED, buff=0.1, stroke_width=2.5)
        self.play(Create(box_top), run_time=0.45)
        self.at("its bottom")
        box_bot = SurroundingRectangle(den, color=TEXT, buff=0.1, stroke_width=2.5)
        self.play(FadeOut(box_top), Create(box_bot), run_time=0.45)
        self.play(FadeOut(box_bot), run_time=0.45)

        self.at("add red cells")
        self.play(v_r.animate(run_time=1.5).set_value(3.0))
        self.wait(0.35)
        self.play(v_r.animate(run_time=0.8).set_value(2.2))

        self.at("add plasma")
        self.play(v_p.animate(run_time=1.5).set_value(4.0))
        self.wait(0.35)
        self.play(v_p.animate(run_time=0.8).set_value(2.8))

        self.at("nothing in the body")
        ratio_ctrl = ValueTracker(0.44)
        # Empty fmt so the strike line across the dial does not cross digits
        d = dial(ratio_ctrl, center=[0.7, -2.0, 0], radius=0.65, label="set the ratio?", color=TEXT, fmt="", size=24)
        strike = Line([0.05, -2.35, 0], [1.35, -1.35, 0], color=RED, stroke_width=5)
        strike.layout_ok = True
        self.play(FadeIn(d), run_time=0.4)
        self.play(Create(strike), run_time=0.35)
        self.wait(0.45)
        self.play(FadeOut(VGroup(d, strike)), Indicate(num, color=RED), Indicate(den, color=TEXT), run_time=0.7)
        self.finish()


class S04Plasma(SpokenScene):
    def construct(self):
        world = build_zoom_tube_world(v_red=2.2, v_plasma=2.8, show_readout=False)
        y_bot, h_full = world.y_bot, world.h_full
        v_r, v_p = world.v_red_tr, world.v_pl_tr

        y_44 = y_bot + 0.44 * h_full
        ghost = DashedLine([-5.55, y_44, 0], [-4.02, y_44, 0], color=TEXT, stroke_width=2.5, dash_length=0.12).set_opacity(0.65)
        ghost_lab = T("start", size=22, color=TEXT).set_opacity(0.75).next_to([-4.02, y_44, 0], RIGHT, buff=0.14)
        self.add(world, ghost, ghost_lab)

        case_preg = T("pregnancy", size=32, color=AMBER).move_to([-1.2, 2.2, 0])
        self.at("pregnancy expands plasma")
        self.play(FadeIn(case_preg, shift=DOWN * 0.1), run_time=0.4)
        self.play(v_p.animate.set_value(4.3), v_r.animate.set_value(2.45), run_time=2.8)

        self.at("first days at altitude")
        case_alt = T("altitude, first days", size=32, color=CYAN).move_to([-0.7, 2.2, 0])
        self.play(swap(case_preg, case_alt, run_time=0.8),
                  v_r.animate(run_time=1.4).set_value(2.2),
                  v_p.animate(run_time=1.4).set_value(2.8))

        self.at("a diuresis")
        drop_top = Triangle(color=AMBER, fill_color=AMBER, fill_opacity=0.9, stroke_width=0).scale(0.14)
        drop_bot = Dot(radius=0.13, color=AMBER).move_to(drop_top.get_bottom() + UP * 0.03)
        drop = VGroup(drop_bot, drop_top).move_to([-3.95, y_bot + 4.5 * world.h_per_l, 0])
        self.play(FadeIn(drop, scale=0.8), run_time=0.3)
        self.play(drop.animate.shift(RIGHT * 1.1 + DOWN * 0.9).set_opacity(0),
                  v_p.animate.set_value(2.1), run_time=2.2)
        self.remove(drop)

        self.at("red cell mass")
        note = T("red cell mass: little changed", size=28, color=RED).move_to([-0.2, 0.35, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S05Mass(SpokenScene):
    def construct(self):
        world = build_full_world(v_red=2.2, v_plasma=2.8, gauge_val=0.55, show_tube_readout=True, show_teaching_tag=True)
        self.add(world)

        grid = VGroup(*[
            Dot([3.4 + (i % 5) * 0.32, -0.08 + (i // 5) * 0.23, 0], radius=0.055, color=RED)
            for i in range(15)
        ]).set_opacity(0.65)
        grid.layout_ok = True

        self.at("cannot give you a mass")
        q_mark = T("?", size=40, color=TEXT).move_to([-3.5, 0.6, 0])
        self.add(grid)
        self.play(FadeIn(grid), FadeIn(q_mark), run_time=0.5)
        self.play(q_mark.animate.move_to([1.2, 0.9, 0]).set_opacity(0), run_time=1.8)
        self.remove(q_mark)

        # Card 1: Syringe with AMBER tracer (kept clearly left of vessel x0=-0.6)
        self.at("indicator dilution")
        syr_body = Rectangle(width=0.9, height=0.26, color=TEXT, stroke_width=2, fill_color=AMBER, fill_opacity=0.45)
        syr_plunger = Line(syr_body.get_left() + LEFT * 0.28, syr_body.get_left(), color=TEXT, stroke_width=3)
        syr_needle = Line(syr_body.get_right(), syr_body.get_right() + RIGHT * 0.3, color=TEXT, stroke_width=2)
        tracer = VGroup(*[Dot(syr_body.get_right() + RIGHT * (0.38 + 0.13 * k) + UP * ((k % 2 - 0.5) * 0.14),
                              radius=0.045, color=AMBER) for k in range(4)])
        c1_icon = VGroup(syr_plunger, syr_body, syr_needle, tracer)
        c1_lab = T("indicator dilution", size=22, color=AMBER)
        c1_box = RoundedRectangle(corner_radius=0.14, width=2.85, height=1.2, color=AMBER, stroke_width=2.5,
                                  fill_color=BG, fill_opacity=0.94)
        c1_inner = VGroup(c1_icon, c1_lab).arrange(DOWN, buff=0.14).move_to(c1_box)
        card1 = VGroup(c1_box, c1_inner).move_to([-2.2, 1.85, 0])
        self.play(FadeIn(card1, shift=RIGHT * 0.2), run_time=0.6)
        self.play(Indicate(card1, scale_factor=1.05, color=AMBER), run_time=0.5)

        chip1 = chip("indicator dilution", color=AMBER, size=22).move_to([-2.3, -1.55, 0])
        self.play(FadeOut(c1_icon, run_time=0.25),
                  Transform(c1_box, chip1[0], run_time=0.6),
                  Transform(c1_lab, chip1[1], run_time=0.6))

        # Card 2: Mask with breath arrow -> CO rebreathing (no overlap with vessel)
        self.at("carbon monoxide rebreathing")
        mask = Arc(radius=0.25, start_angle=-PI / 2, angle=PI, color=TEXT, stroke_width=2.5).rotate(PI / 2)
        breath = Arrow(mask.get_bottom() + DOWN * 0.05, mask.get_bottom() + RIGHT * 0.6, color=RED,
                       stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.3)
        c2_icon = VGroup(mask, breath)
        c2_lab = T("CO rebreathing", size=22, color=RED)
        c2_box = RoundedRectangle(corner_radius=0.14, width=2.85, height=1.2, color=RED, stroke_width=2.5,
                                  fill_color=BG, fill_opacity=0.94)
        c2_inner = VGroup(c2_icon, c2_lab).arrange(DOWN, buff=0.14).move_to(c2_box)
        card2 = VGroup(c2_box, c2_inner).move_to([-2.2, 1.85, 0])
        self.play(FadeIn(card2, shift=RIGHT * 0.2), run_time=0.6)
        self.play(Indicate(card2, scale_factor=1.05, color=RED), run_time=0.5)

        chip2 = chip("CO rebreathing", color=RED, size=22).move_to([-2.3, -2.5, 0])
        self.play(FadeOut(c2_icon, run_time=0.25),
                  Transform(c2_box, chip2[0], run_time=0.6),
                  Transform(c2_lab, chip2[1], run_time=0.6))

        self.at("reports a share")
        y_44 = -2.15 + 0.44 * 4.2
        share_ring = Circle(radius=0.36, color=TEXT, stroke_width=3).move_to([-5.05, y_44, 0])
        share_ring.layout_ok = True
        share_lab = T("a share", size=28, color=TEXT).move_to([-2.9, y_44, 0])
        self.play(Create(share_ring), FadeIn(share_lab, shift=RIGHT * 0.1), run_time=0.5)

        self.at("never a count")
        count_ring = DashedVMobject(Ellipse(width=1.85, height=0.95, color=RED, stroke_width=3), num_dashes=16)
        count_ring.move_to(grid.get_center())
        count_ring.layout_ok = True
        count_lab = T("a count", size=28, color=RED).move_to([4.05, 1.0, 0])
        self.play(Create(count_ring), FadeIn(count_lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S06Idea(SpokenScene):
    def construct(self):
        world = build_full_world(v_red=2.2, v_plasma=2.8, gauge_val=0.55, show_tube_readout=True, show_teaching_tag=True)
        self.add(world)
        self.wait(1.2)

        self.at("nothing in the body")
        self.play(world.marker.opacity_tr.animate.set_value(0.42), run_time=1.2)
        self.play(Indicate(world.marker, color=SLATE, scale_factor=1.03), run_time=1.0)

        self.at("its numerator")
        # Inset highlight inside RED column so it never straddles tube border
        red_hi = SurroundingRectangle(world.tube[0], color=RED, buff=-0.04, stroke_width=4)
        num_lab = T("numerator", size=26, color=RED).move_to([-2.75, -1.25, 0])

        pts = [
            world.kidney.get_right() + LEFT * 0.1,
            [5.65, -1.75, 0],
            [5.65, 2.0, 0],
            world.marrow.get_right() + RIGHT * 0.05,
        ]
        epo_path = VMobject(color=MAGENTA, stroke_width=4).set_points_as_corners(pts)
        epo_tip = Arrow([5.1, 2.0, 0], world.marrow.get_right() + LEFT * 0.05, color=MAGENTA, stroke_width=4, buff=0)
        marrow_out = Arrow(world.marrow.opening + DOWN * 0.06, [2.6, 0.55, 0], color=RED, stroke_width=4, buff=0)
        self.play(Create(red_hi), FadeIn(num_lab), Create(epo_path), FadeIn(epo_tip), run_time=1.6)
        self.play(Create(marrow_out), run_time=0.7)

        for k in range(3):
            c = _rbc_disc(0.13, 0.075)
            c.move_to([2.3 + k * 0.28, 0.32 - k * 0.12, 0])
            _attach_drift(c, 0.9, world.vessel.x0 + 0.18, world.vessel.x1 - 0.18)
            world.vessel.cells.add(c)

        self.at("reading the oxygen")
        halos = VGroup(*[
            Circle(radius=0.44, color=CYAN, stroke_width=2.5, fill_color=CYAN, fill_opacity=0.22).move_to(cell.cell_center)
            for cell in world.kidney.cells
        ])
        halos.layout_ok = True
        o2_lab = T("oxygen, here", size=28, color=CYAN).move_to([-1.45, -1.75, 0])
        self.play(FadeIn(halos, scale=0.8), FadeIn(o2_lab, shift=RIGHT * 0.1), run_time=1.0)
        self.finish()


class S07Kidney(SpokenScene):
    def construct(self):
        o2_tr = ValueTracker(0.55)

        vessel = make_vessel_band(x0=-4.1, x1=6.1, y_mid=2.55, height=0.95, n_cells=12, speed=1.3, cell_rx=0.155)
        v_wash = Rectangle(width=10.2, height=1.2, stroke_width=0, fill_color=CYAN, fill_opacity=0.26).move_to([1.0, 2.55, 0])
        v_wash.layout_ok = True

        scale = make_scale(x=-5.65, y_bot=-2.1, h_full=3.4, tick_step=30, tick_size=22)
        tube = make_static_tube(x=-5.05, y_bot=-2.1, h_full=3.4, width=0.52, hct_frac=0.44)
        t_num = T("teaching numbers", size=22, color=SLATE).move_to([-4.95, -3.1, 0])

        patch_center = (1.1, -0.55, 0)
        patch_w, patch_h = 9.4, 4.55
        patch_box = RoundedRectangle(corner_radius=0.26, width=patch_w, height=patch_h, color=SLATE,
                                     stroke_width=3, fill_color=SLATE, fill_opacity=0.07).move_to(patch_center)
        patch_box.layout_ok = True

        k_wash = Rectangle(width=patch_w - 0.15, height=patch_h - 0.15, stroke_width=0,
                           fill_color=CYAN, fill_opacity=0.06).move_to(patch_center)
        k_wash.layout_ok = True

        tub_xs = [-1.85, 1.1, 4.05]
        tubules = VGroup(*[
            RoundedRectangle(corner_radius=0.45, width=1.42, height=3.15, color=SLATE,
                             stroke_width=3.5, fill_color=BG, fill_opacity=0.72).move_to([x, -0.55, 0])
            for x in tub_xs
        ])

        c1 = make_interstitial_cell([-0.38, -0.40, 0], gauge_tracker=o2_tr, star=True, scale=1.35, gauge_scale=1.35)
        c2 = make_interstitial_cell([2.58, -0.40, 0], gauge_tracker=o2_tr, star=True, scale=1.35, gauge_scale=1.35)

        tag = scope_tag("schematic")
        self.add(v_wash, vessel, scale, tube, t_num, patch_box, tubules, c1, c2, tag)

        self.at("interstitial cells")
        lab1 = T("interstitial cell", size=24, color=TEXT).move_to([-0.38, 1.32, 0])
        lab2 = T("interstitial cell", size=24, color=TEXT).move_to([2.58, 1.32, 0])
        self.play(FadeIn(lab1, shift=DOWN * 0.1), FadeIn(lab2, shift=DOWN * 0.1), run_time=1.0)
        self.play(Indicate(c1.body, color=TEXT), Indicate(c2.body, color=TEXT), run_time=1.0)

        self.at("rather than in them")
        ghost_cell = DashedVMobject(Circle(radius=0.42, color=RED, stroke_width=3.5), num_dashes=12).move_to([1.1, -0.55, 0])
        strike = Line([0.62, -0.98, 0], [1.58, -0.12, 0], color=RED, stroke_width=4.5)
        strike.layout_ok = True
        self.play(Create(ghost_cell), run_time=0.6)
        self.play(Create(strike), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(VGroup(ghost_cell, strike)), run_time=0.6)

        self.at("relatively low oxygen zone")
        low_o2_lab = T("relatively low oxygen", size=26, color=CYAN).move_to([1.1, -2.42, 0])
        self.play(FadeIn(k_wash, run_time=1.2), FadeIn(low_o2_lab, shift=UP * 0.1, run_time=0.8))

        self.at("small fall in blood")
        thin_cells = VGroup(*[vessel.cells[i] for i in range(0, len(vessel.cells), 3)])
        gauge_tag = T("schematic", size=22, color=SLATE).move_to([2.58, -1.38, 0])
        self.play(FadeOut(thin_cells), FadeIn(gauge_tag), o2_tr.animate.set_value(0.22), run_time=2.2)
        self.finish()


class S08Hif(SpokenScene):
    def construct(self):
        o2_wash_op = ValueTracker(0.22)
        cell_border = RoundedRectangle(corner_radius=0.55, width=11.6, height=5.8, color=SLATE,
                                       stroke_width=3.5, fill_opacity=0).move_to([0, 0.1, 0])
        cell_wash = always_redraw(lambda: RoundedRectangle(corner_radius=0.52, width=11.45, height=5.65, stroke_width=0,
                                                           fill_color=CYAN, fill_opacity=o2_wash_op.get_value()).move_to([0, 0.1, 0]))
        cell_wash.layout_ok = True
        cell_lab = T("interstitial cell", size=26, color=SLATE).move_to([-4.0, 2.55, 0])
        tag = scope_tag("schematic")
        self.add(cell_wash, cell_border, cell_lab, tag)

        # HIF-2 alpha block drifts continuously during first sentence + well-oxygenated setup
        self.at("the switch inside them")
        hif1 = boxed_label("HIF-2 alpha", color=MAGENTA, size=26, pad=0.18).move_to([-4.6, 0.1, 0])
        self.play(FadeIn(hif1, shift=RIGHT * 0.25), run_time=1.0)
        self.play(hif1.animate.move_to([-3.85, 0.1, 0]), run_time=3.5, rate_func=linear)

        # Wide hydroxylase hexagon centered at [-1.1, 0.1, 0] so "hydroxylase" never touches edges
        self.at("hydroxylase enzymes")
        hex_enz = RegularPolygon(6, radius=1.18, color=SLATE, stroke_width=3, fill_color=SLATE, fill_opacity=0.22)
        hex_enz.stretch(1.28, 0).move_to([-1.1, 0.1, 0])
        enz_lab = T("hydroxylase", size=24, color=TEXT).move_to(hex_enz)
        enz_grp = VGroup(hex_enz, enz_lab)

        c_o2 = chip("oxygen", color=CYAN, size=22, pad=0.14).move_to([-2.9, 1.95, 0])
        c_fe = chip("iron", color=TEXT, size=22, pad=0.14).move_to([-1.1, 1.95, 0])
        c_og = chip("2-oxoglutarate", color=SLATE, size=22, pad=0.14).move_to([1.15, 1.95, 0])
        inputs = VGroup(c_o2, c_fe, c_og)

        bin_box = RoundedRectangle(corner_radius=0.1, width=2.0, height=0.92, color=SLATE, stroke_width=2.5,
                                   fill_color=BG, fill_opacity=0.85).move_to([-1.1, -1.85, 0])
        bin_lab = T("destroyed", size=24, color=SLATE).move_to(bin_box)
        bin_grp = VGroup(bin_box, bin_lab)

        self.play(FadeIn(enz_grp), FadeIn(inputs), FadeIn(bin_grp), run_time=1.0)
        self.play(hif1.animate.move_to([-3.85, -0.5, 0]), run_time=1.5)

        self.at("for destruction")
        tag_dot = Dot(hif1.get_top() + UP * 0.06, radius=0.09, color=SLATE)
        self.play(FadeIn(tag_dot), run_time=0.4)
        self.play(VGroup(hif1, tag_dot).animate.move_to(bin_box.get_center()).scale(0.55).set_opacity(0), run_time=1.1)
        self.remove(hif1, tag_dot)

        # Low oxygen state: EPO gene box at [+4.2, 0.1, 0]
        self.at("when oxygen falls")
        epo_box = boxed_label("EPO gene", color=MAGENTA, size=28, pad=0.22).move_to([4.2, 0.1, 0])
        self.play(
            o2_wash_op.animate.set_value(0.05),
            c_o2.animate.set_opacity(0.25),
            enz_grp.animate.set_opacity(0.32),
            FadeIn(epo_box),
            run_time=1.2,
        )

        # HIF-2 alpha blocks pile up at [+1.75, 0.1, 0] — clear of BOTH hex_enz (right ~0.4) and epo_box (left ~3.2)
        self.at("turns on the")
        hif_stack = VGroup(
            boxed_label("HIF-2 alpha", color=MAGENTA, size=24, pad=0.16).move_to([-3.95, -0.2, 0]),
            boxed_label("HIF-2 alpha", color=MAGENTA, size=24, pad=0.16).move_to([-3.95, -1.05, 0]),
        )
        self.play(FadeIn(hif_stack, shift=RIGHT * 0.2), run_time=0.5)
        target_stack = hif_stack.copy().arrange(DOWN, buff=0.16).move_to([1.75, 0.1, 0])
        p_bot = VMobject().set_points_as_corners([
            hif_stack[1].get_center(),
            [-3.1, -1.16, 0],
            [0.8, -1.16, 0],
            target_stack[1].get_center(),
        ])
        p_top = VMobject().set_points_as_corners([
            hif_stack[0].get_center(),
            [-3.75, 1.06, 0],
            [-3.45, 1.41, 0],
            [0.45, 1.41, 0],
            [1.45, 1.34, 0],
            [1.75, 1.06, 0],
            target_stack[0].get_center(),
        ])
        self.play(
            MoveAlongPath(hif_stack[1], p_bot),
            MoveAlongPath(hif_stack[0], p_top),
            run_time=0.8,
        )
        self.play(epo_box[0].animate.set_fill(MAGENTA, opacity=0.42), run_time=0.35)

        epo_dots = VGroup(*[Dot([5.35 + (k % 2) * 0.35, 0.1 + (k // 2 - 1) * 0.28, 0], radius=0.085, color=MAGENTA) for k in range(6)])
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.3) for d in epo_dots], lag_ratio=0.1), run_time=0.9)
        self.play(epo_dots.animate.shift(RIGHT * 0.8).set_opacity(0), run_time=0.6)
        self.remove(*epo_dots)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        world = build_predict_world(day_val=0.0)
        self.add(world)

        self.at("breathing thin air")
        self.play(world.day_tr.animate.set_value(0.8), run_time=1.0, rate_func=linear)

        self.at("plasma erythropoietin rises")
        dots = [Dot(world.kidney.get_top() + UP * 0.05, radius=0.08, color=MAGENTA) for _ in range(5)]
        self.play(
            world.day_tr.animate(run_time=3.2, rate_func=linear).set_value(2.0),
            LaggedStart(*[
                Succession(
                    d.animate(run_time=1.2).move_to(world.marrow.get_bottom() + UP * 0.25),
                    FadeOut(d, run_time=0.3),
                )
                for d in dots
            ], lag_ratio=0.25),
            world.marrow.fill_rect.animate(run_time=2.0).set_fill(TAN, opacity=0.38),
        )
        self.remove(*dots)

        self.at("new red cells")
        flat_hi = Line(world.p_red.pt(0.1, 0.12), world.p_red.pt(2.0, 0.12), color=RED, stroke_width=6)
        self.play(ShowPassingFlash(flat_hi, time_width=0.5), run_time=1.0)

        self.at("why does the cell count")
        q = T("Why does the count lag?", size=34, color=TEXT).move_to([-1.6, 3.15, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Why does the count lag?"
    OPTIONS = ()
    CARD = {"y": 3.15, "color": TEXT, "left": -4.2, "max_w": 7.0, "size": 34}
    RING_AT = (3.9, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        world = build_predict_world(day_val=2.0)
        world.marrow.fill_rect.set_fill(TAN, opacity=0.38)
        pulse(world.marrow.outline, base=3.0, amp=1.5, speed=3.5)
        return world


class S11Answer(SpokenScene):
    def construct(self):
        day_tr = ValueTracker(2.0)
        marrow = make_marrow_block(center=(-2.1, 1.15, 0), width=6.8, height=2.9, label="", label_size=26)
        marrow_lab = T("marrow", size=26, color=TAN).move_to([-4.6, 2.25, 0])
        vessel = make_vessel_band(x0=-5.5, x1=1.3, y_mid=-1.55, height=1.25, n_cells=8, speed=0.9)

        p_epo = Plot(box=(2.1, 6.0, 0.65, 2.35), xr=(0, 4.2), yr=(0, 1.0), xticks=[], yticks=[], color=SLATE, stroke=2.5)
        epo_lab = T("EPO in plasma", size=24, color=MAGENTA).next_to([2.1, 2.35, 0], UP, buff=0.12).align_to([2.1, 0, 0], LEFT)
        epo_line = p_epo.live_curve(_epo_curve, day_tr, color=MAGENTA, width=5)

        p_red = Plot(box=(2.1, 6.0, -2.05, -0.35), xr=(0, 4.2), yr=(0, 1.0), xticks=[], yticks=[], color=SLATE, stroke=2.5)
        red_lab = T("new red cells", size=24, color=RED).next_to([2.1, -0.35, 0], UP, buff=0.12).align_to([2.1, 0, 0], LEFT)
        red_line = p_red.live_curve(_retic_curve, day_tr, color=RED, width=5)

        day_readout = counter("day {:.0f}", day_tr, at=[5.05, 3.15, 0], size=30, color=TEXT)
        tag = scope_tag("schematic")

        pxs = [-3.9, -2.7, -1.5, -0.3]
        progs = VGroup(*[
            Circle(radius=0.34, color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.65).move_to([x, 1.15, 0])
            for x in pxs
        ])

        self.add(marrow, marrow_lab, vessel, p_epo, epo_lab, epo_line, p_red, red_lab, red_line, day_readout, tag, progs)

        # Two progenitors begin crumbling before hormone rescues them
        self.play(progs[0].animate.set_opacity(0.35).scale(0.84),
                  progs[2].animate.set_opacity(0.35).scale(0.84), run_time=1.8)

        self.at("preventing the death")
        epo_dots = VGroup(*[Dot([x, 2.85, 0], radius=0.09, color=MAGENTA) for x in pxs])
        self.play(LaggedStart(*[d.animate.move_to([x, 1.5, 0]) for d, x in zip(epo_dots, pxs)], lag_ratio=0.12),
                  progs[0].animate.set_opacity(1.0).scale(1 / 0.84),
                  progs[2].animate.set_opacity(1.0).scale(1 / 0.84),
                  run_time=1.8)
        self.play(FadeOut(epo_dots), run_time=0.4)

        self.at("divide and mature")
        retics = VGroup()
        targets = []
        for idx, x in enumerate(pxs):
            for dx, dy in [(-0.26, 0.25), (0.26, -0.25)]:
                rt = _retic_disc(0.18, 0.11).move_to([x, 1.15, 0])
                retics.add(rt)
                targets.append([x + dx, 1.05 + dy, 0])
        self.play(FadeOut(progs, run_time=0.4),
                  *[FadeIn(r, run_time=0.45) for r in retics])
        self.play(*[r.animate.move_to(t) for r, t in zip(retics, targets)], run_time=1.0)

        # Label points directly to the rightmost reticulocyte, then clears as cells exit into the stream
        retic_lab = T("reticulocyte (holds RNA)", size=24, color=TEXT).move_to([-0.8, 2.2, 0])
        retic_ptr = Arrow(retic_lab.get_bottom() + RIGHT * 0.3, retics[-2].get_top() + UP * 0.05,
                          color=TEXT, stroke_width=2.5, buff=0.04, max_tip_length_to_length_ratio=0.22)
        self.play(FadeIn(retic_lab, shift=DOWN * 0.1), Create(retic_ptr), run_time=0.5)

        self.at("release of reticulocytes")
        self.play(FadeOut(VGroup(retic_lab, retic_ptr)), run_time=0.4)
        self.play(
            day_tr.animate(run_time=4.2, rate_func=linear).set_value(4.0),
            LaggedStart(*[
                Succession(
                    r.animate(run_time=0.65).move_to([-2.1, -0.35, 0]),
                    r.animate(run_time=0.95).move_to([-1.2 + i * 0.3, -1.55 + ((i % 3) - 1) * 0.28, 0]),
                )
                for i, r in enumerate(retics)
            ], lag_ratio=0.14),
        )
        for r in retics:
            _attach_drift(r, 0.85, vessel.x0 + 0.18, vessel.x1 - 0.18)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        world = build_full_world(v_red=2.2, v_plasma=2.8, gauge_val=0.55, show_tube_readout=True, show_teaching_tag=True)
        self.add(world)
        v_r, v_p = world.v_red_tr, world.v_pl_tr

        self.at("two unrelated events")
        self.play(v_p.animate.set_value(3.8), run_time=0.9)
        self.play(v_p.animate.set_value(2.1), run_time=1.0)
        self.play(v_p.animate.set_value(2.8), run_time=0.7)

        self.at("not aiming at that number")
        d = dial(ValueTracker(0.44), center=[-1.8, -1.8, 0], radius=0.55, label="set the ratio?", color=TEXT, fmt="", size=22)
        strike = Line([-2.35, -2.1, 0], [-1.25, -1.2, 0], color=RED, stroke_width=4)
        strike.layout_ok = True
        self.play(world.marker.opacity_tr.animate.set_value(0.42), FadeIn(d), Create(strike), run_time=0.6)
        self.play(FadeOut(VGroup(d, strike)), run_time=0.5)

        self.at("kidney cell orders")
        halos = VGroup(*[
            Circle(radius=0.42, color=CYAN, stroke_width=2.5, fill_color=CYAN, fill_opacity=0.22).move_to(cell.cell_center)
            for cell in world.kidney.cells
        ])
        halos.layout_ok = True
        pts = [world.kidney.get_right() + LEFT * 0.1, [5.65, -1.75, 0], [5.65, 2.0, 0], world.marrow.get_right() + RIGHT * 0.05]
        epo_path = VMobject(color=MAGENTA, stroke_width=4).set_points_as_corners(pts)
        epo_tip = Arrow([5.1, 2.0, 0], world.marrow.get_right() + LEFT * 0.05, color=MAGENTA, stroke_width=4, buff=0)
        new_discs = [_rbc_disc(0.13, 0.075).move_to(world.marrow.opening + DOWN * 0.1) for _ in range(3)]
        self.play(FadeIn(halos), Create(epo_path), FadeIn(epo_tip), run_time=0.9)
        self.play(LaggedStart(*[d_mob.animate(run_time=0.7).move_to([2.2 + k * 0.4, 0.15 + (k - 1) * 0.2, 0])
                                for k, d_mob in enumerate(new_discs)], lag_ratio=0.15))
        for d_mob in new_discs:
            _attach_drift(d_mob, 0.9, world.vessel.x0 + 0.18, world.vessel.x1 - 0.18)

        self.at("the ratio follows")
        self.play(world.marker.opacity_tr.animate.set_value(1.0), v_r.animate.set_value(2.45), run_time=1.1)
        self.finish()


class S13End(EndCard):
    LINE = "Hematocrit is a ratio; the kidney regulates its numerator by local oxygen."
