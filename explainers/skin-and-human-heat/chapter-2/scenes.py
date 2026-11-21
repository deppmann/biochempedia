"""Where Skin Keeps Its Water — Chapter 2 of Skin, Sweat and Human Thermoregulation.

COLOUR MAP (one colour per concept, carried across the whole film):
    GREY   (#8B93A1)  skin structure, corneocytes (dead cells), keratin streaks
    BLUE   (#58C4DD)  water (sweat, vapour lines, water held in body, sweat duct)
    GOLD   (#D4A843)  lipid between cells (lamellar bodies, extruded mortar, lamellae)
    TEAL   (#3FB8C0)  electron-dense water-soluble tracer
    PURPLE (#A875FF)  tight junctions (between cells)
    TEXT   (#E8EAF0)  primary labels, questions, and take-home statements
    PEACH  (#E6A88A)  living epidermal keratinocytes (with dark nucleus dot)
    TAN    (#4E3423)  dermis connective tissue band

ONE CARRIED WORLD:
    A schematic cross-section of thin skin filling ~68% of the frame height
    (x in [-3.4, 2.6], y in [-2.45, 2.35]): air above; 4 staggered rows of flat
    GREY corneocyte plates; 2 rows of granulosum, 2 rows of spinosum, and 1 row of
    basale pale peach living cells with dark nuclei; a wavy basement membrane; a
    dark tan dermis band at the bottom; and a coiled BLUE sweat duct rising from
    the dermis through the epidermis to a surface pore.

WHAT CHANGES PER SCENE (and what it is computed from):
    s00_link_and_question  Evaporating drop's rising vapour waves (phase-integrated sine
                           curves) and dripping drop fall; BLUE water dots diffuse and
                           rebound under the skin bar (deterministic RNG velocities),
                           then the bar opens into the full skin cross-section.
    s01_title              Standard TitleCard (2.0 s).
    s02_conveyor           Tracked basal cell divides; daughter cell rides computed
                           row-by-row conveyor upward, fills with GREY keratin streaks,
                           flattens, loses its nucleus, and replaces a corneum plate.
    s03_job                BLUE water dots diffuse and rebound beneath corneum; sparse
                           computed trickle crosses corneum; BLUE sweat drops travel
                           along the coiled duct path to the pore and evaporate.
    s04_guess              Intercellular lane polylines highlight between living cells;
                           gut/kidney tight-junction inset builds; dashed PURPLE
                           expected seal line crosses living layers while water diffuses.
    s05_experiment         TEAL tracer dots walk continuously upward along computed
                           intercellular lane waypoints; hypothetical ghost dots
                           accumulate and halt at the dashed PURPLE expected seal line.
    s06_result             Ghost dots and expected seal line fade; TEAL tracers advance
                           past the lower layers to upper granulosum; GOLD lamellar
                           bodies migrate to cell margins and extrude GOLD mortar,
                           halting the tracers beneath it.
    s07_idea               Upper granulosum and corneum zoom to fill the frame; GOLD
                           mortar resolves into 3 stacked lipid stripes per gap; BLUE
                           water dots press against the GOLD mortar and turn back.
    s08_predict            PURPLE tight-junction bars appear in granulosum only, then dim
                           to faint outlines on claudin-1 loss while BLUE dots agitate
                           beneath the GOLD and the predict question appears.
    s09_pause              PredictPause holds the question and dimmed junctions for 4.5 s
                           while the countdown ring empties.
    s10_answer             With PURPLE bars faint, a stream of BLUE dots leaks through
                           upper layers into air and drives a ValueTracker-linked water-
                           loss gauge high; restoring PURPLE bars drops the leak and gauge.
    s11_return             Corneum plates, GOLD mortar, and PURPLE junctions highlight in
                           sequence while BLUE water stays held below; sweat drops climb
                           the duct to the pore and evaporate as rising BLUE vapour.
    s12_end                Standard EndCard with the take-home line.
"""

from types import SimpleNamespace
import numpy as np
from bp_parts import *

# Film-specific colours (beyond bp_style TEXT, GREY, BLUE, GOLD, TEAL, BG)
PURPLE = "#A875FF"
PEACH_STROKE = "#E6A88A"
PEACH_FILL = "#C47D5C"
NUCLEUS_FILL = "#1F1418"
NUCLEUS_RING = "#8C5846"
DERMIS_FILL = "#4E3423"
DERMIS_STROKE = "#8A6044"

# Cross-section geometry (all inside safe [-6.3, 6.3] x [-3.5, 3.5])
SKIN_X0 = -3.40
SKIN_X1 = 2.60
DERMIS_Y0 = -2.45
DERMIS_Y1 = -1.00
DUCT_X = 1.72

MAIN_COLS = [-2.88, -1.94, -1.00, -0.06, 0.88]
RIGHT_COL = 2.30

LIVING_ROWS = [
    ("basale", -0.74, 0.36, 0.78, 0.00),
    ("spinosum", -0.26, 0.34, 0.76, 0.07),
    ("spinosum", 0.20, 0.32, 0.76, -0.06),
    ("granulosum", 0.63, 0.25, 0.78, 0.05),
    ("granulosum", 0.99, 0.21, 0.80, -0.04),
]

CORNEUM_ROWS = [
    (1.30, 0.15, 0.00),
    (1.56, 0.15, 0.38),
    (1.82, 0.15, 0.08),
    (2.08, 0.15, 0.44),
]
CORNEUM_TOP = 2.16


def _membrane_y(x):
    return DERMIS_Y1 + 0.04 * np.sin(3.4 * (x - SKIN_X0))


def _duct_pt(s):
    """Parametric centerline of the coiled sweat duct from dermis (s=0) to pore (s=1)."""
    if s < 0.28:
        u = s / 0.28
        ang = u * 2.4 * PI
        x = DUCT_X + 0.22 * np.cos(ang)
        y = -2.18 + 0.45 * u + 0.12 * np.sin(ang)
        return np.array([x, y, 0.0])
    u = (s - 0.28) / 0.72
    y = -1.73 + u * (CORNEUM_TOP - (-1.73))
    amp = 0.11 * (1.0 - 0.45 * u)
    x = DUCT_X + amp * np.sin(5.5 * PI * u)
    return np.array([x, y, 0.0])


def _make_cell(cx, cy, w, h, stroke=PEACH_STROKE, fill=PEACH_FILL, fill_op=0.32,
               nucleus=True, corner=0.10):
    rect = RoundedRectangle(
        corner_radius=min(corner, h * 0.42),
        width=w,
        height=h,
        stroke_color=stroke,
        stroke_width=2.0,
        fill_color=fill,
        fill_opacity=fill_op,
    ).move_to([cx, cy, 0.0])
    if not nucleus:
        return VGroup(rect)
    nuc = Circle(
        radius=min(0.068, h * 0.24),
        stroke_color=NUCLEUS_RING,
        stroke_width=1.4,
        fill_color=NUCLEUS_FILL,
        fill_opacity=0.92,
    ).move_to([cx, cy, 0.0])
    return VGroup(rect, nuc)


def _make_plate(cx, cy, w, h, keratin=True):
    rect = RoundedRectangle(
        corner_radius=0.05,
        width=w,
        height=h,
        stroke_color=GREY,
        stroke_width=2.0,
        fill_color=GREY,
        fill_opacity=0.38,
    ).move_to([cx, cy, 0.0])
    if not keratin:
        return VGroup(rect)
    s1 = Line([cx - w * 0.34, cy + h * 0.16, 0], [cx + w * 0.34, cy + h * 0.16, 0],
              color=GREY, stroke_width=1.4).set_opacity(0.65)
    s2 = Line([cx - w * 0.28, cy - h * 0.16, 0], [cx + w * 0.28, cy - h * 0.16, 0],
              color=GREY, stroke_width=1.4).set_opacity(0.65)
    return VGroup(rect, s1, s2)


def _clipped_corneum_xs(y_shift):
    """Return (x_center, width) pairs of corneocyte plates left and right of the duct."""
    plates = []
    lx0, lx1 = -3.34, 1.38
    pw = 1.06
    gap = 0.08
    step = pw + gap
    x = lx0 - y_shift
    while x < lx1:
        a = max(x, lx0)
        b = min(x + pw, lx1)
        if b - a >= 0.32:
            plates.append(((a + b) / 2.0, b - a))
        x += step
    plates.append((2.305, 0.49))
    return plates


def build_skin_world(with_gold=False, gold_opacity=0.88, with_junctions=False, junctions_dim=False):
    """Build the carried schematic cross-section of thin skin."""
    world = VGroup()

    dermis_bg = Rectangle(
        width=SKIN_X1 - SKIN_X0,
        height=DERMIS_Y1 - DERMIS_Y0,
        stroke_color=DERMIS_STROKE,
        stroke_width=2.0,
        fill_color=DERMIS_FILL,
        fill_opacity=0.82,
    ).move_to([(SKIN_X0 + SKIN_X1) / 2.0, (DERMIS_Y0 + DERMIS_Y1) / 2.0, 0.0])

    xs_mem = np.linspace(SKIN_X0, SKIN_X1, 100)
    mem_pts = [np.array([x, _membrane_y(x), 0.0]) for x in xs_mem]
    membrane = VMobject(stroke_color=DERMIS_STROKE, stroke_width=3.0)
    membrane.set_points_as_corners(mem_pts)

    living_rows_map = {"basale": VGroup(), "spinosum": VGroup(), "granulosum": VGroup()}
    cell_grid = []
    for stratum, yc, h, w, dx in LIVING_ROWS:
        row_cells = []
        row_grp = VGroup()
        for cx0 in MAIN_COLS:
            cx = np.clip(cx0 + dx, -3.26 + w / 2, 1.34 - w / 2)
            cell = _make_cell(cx, yc, w, h)
            row_grp.add(cell)
            row_cells.append((cx, yc, w, h, cell))
        rcell = _make_cell(RIGHT_COL, yc, 0.44, h)
        row_grp.add(rcell)
        living_rows_map[stratum].add(row_grp)
        cell_grid.append(row_cells)

    lane_paths = []
    for k in range(4):
        pts = [np.array([(cell_grid[0][k][0] + cell_grid[0][k + 1][0]) / 2.0, DERMIS_Y1 + 0.03, 0.0])]
        for row in cell_grid:
            xm = (row[k][0] + row[k + 1][0]) / 2.0
            ym = row[k][1]
            pts.append(np.array([xm, ym, 0.0]))
        pts.append(np.array([pts[-1][0], 1.18, 0.0]))
        lane_paths.append(pts)

    lanes_grp = VGroup()
    for pts in lane_paths:
        ln = VMobject(stroke_color=TEXT, stroke_width=4.0, stroke_opacity=0.65)
        ln.set_points_as_corners(pts)
        lanes_grp.add(ln)

    corneum_grp = VGroup()
    corneum_rows_list = []
    for yc, h, sh in CORNEUM_ROWS:
        row_grp = VGroup()
        for cx, pw in _clipped_corneum_xs(sh):
            row_grp.add(_make_plate(cx, yc, pw, h, keratin=True))
        corneum_grp.add(row_grp)
        corneum_rows_list.append(row_grp)

    duct_pts = [_duct_pt(s) for s in np.linspace(0.0, 1.0, 90)]
    duct_bg = VMobject(stroke_color=BG, stroke_width=13.0)
    duct_bg.set_points_as_corners(duct_pts)
    duct_outer = VMobject(stroke_color=BLUE, stroke_width=8.5, stroke_opacity=0.40)
    duct_outer.set_points_as_corners(duct_pts)
    duct_core = VMobject(stroke_color=BLUE, stroke_width=4.0, stroke_opacity=0.92)
    duct_core.set_points_as_corners(duct_pts)
    duct_group = VGroup(duct_bg, duct_outer, duct_core)

    gold_mortar = VGroup()
    for y_gap in [1.16, 1.43, 1.69, 1.95]:
        gold_mortar.add(
            Rectangle(width=4.68, height=0.075, stroke_width=0, fill_color=GOLD, fill_opacity=gold_opacity)
            .move_to([-0.98, y_gap, 0.0])
        )
        gold_mortar.add(
            Rectangle(width=0.48, height=0.075, stroke_width=0, fill_color=GOLD, fill_opacity=gold_opacity)
            .move_to([RIGHT_COL, y_gap, 0.0])
        )
    for k in range(4):
        x_top = lane_paths[k][-1][0]
        gold_mortar.add(
            Rectangle(width=0.08, height=0.22, stroke_width=0, fill_color=GOLD, fill_opacity=gold_opacity)
            .move_to([x_top, 1.03, 0.0])
        )

    tight_junctions = VGroup()
    for r_idx in (3, 4):
        row = cell_grid[r_idx]
        for k in range(4):
            xm = (row[k][0] + row[k + 1][0]) / 2.0
            ym = row[k][1]
            if junctions_dim:
                bar = DashedLine(
                    [xm, ym - 0.07, 0], [xm, ym + 0.07, 0],
                    color=PURPLE, stroke_width=3.5, dash_length=0.04,
                ).set_opacity(0.35)
            else:
                bar = Line(
                    [xm, ym - 0.075, 0], [xm, ym + 0.075, 0],
                    color=PURPLE, stroke_width=7.0,
                )
            tight_junctions.add(bar)

    lower_group = VGroup(
        dermis_bg,
        membrane,
        living_rows_map["basale"],
        living_rows_map["spinosum"],
        living_rows_map["granulosum"][0],
        duct_group,
    )
    upper_group = VGroup(living_rows_map["granulosum"][1], corneum_grp)
    world.add(lower_group, upper_group)
    if with_gold:
        upper_group.add(gold_mortar)
    if with_junctions:
        world.add(tight_junctions)

    return SimpleNamespace(
        world=world,
        lower=lower_group,
        upper=upper_group,
        dermis=dermis_bg,
        membrane=membrane,
        basale=living_rows_map["basale"],
        spinosum=living_rows_map["spinosum"],
        granulosum=living_rows_map["granulosum"],
        corneum=corneum_grp,
        corneum_rows=corneum_rows_list,
        cell_grid=cell_grid,
        lane_paths=lane_paths,
        lanes_grp=lanes_grp,
        duct=duct_group,
        duct_core=duct_core,
        gold_mortar=gold_mortar,
        tight_junctions=tight_junctions,
    )


def _eval_polyline(pts, s):
    """Evaluate a polyline at normalized parameter s in [0, 1]."""
    s = float(np.clip(s, 0.0, 1.0))
    segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
    tot = sum(segs) or 1.0
    target = s * tot
    acc = 0.0
    for i, d in enumerate(segs):
        if acc + d >= target or i == len(segs) - 1:
            u = (target - acc) / max(d, 1e-6)
            return pts[i] * (1.0 - u) + pts[i + 1] * u
        acc += d
    return pts[-1]


def make_water_dots(count=30, x_lim=(-3.20, 1.25), y_lim=(-2.25, 1.12), seed=7,
                    avoid_rect=None, radius=0.075, speed_range=(0.85, 1.35)):
    """Create BLUE water dots with computed bounded thermal diffusion and barrier rebound."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        for _try in range(40):
            x = rng.uniform(x_lim[0], x_lim[1])
            y = rng.uniform(y_lim[0], y_lim[1])
            if avoid_rect is None or not (avoid_rect[0] <= x <= avoid_rect[2] and avoid_rect[1] <= y <= avoid_rect[3]):
                break
        d = Dot([x, y, 0.0], radius=radius, color=BLUE).set_opacity(0.90)
        ang = rng.uniform(0.0, TAU)
        spd = rng.uniform(speed_range[0], speed_range[1])
        d._vel = np.array([spd * np.cos(ang), spd * np.sin(ang), 0.0])
        d._phase = rng.uniform(0.0, TAU)
        d._time = 0.0
        dots.add(d)

    def _update(grp, dt):
        if dt <= 0:
            return
        for d in grp:
            d._time += dt
            p = d.get_center() + d._vel * dt
            p[0] += 0.06 * np.sin(3.0 * d._time + d._phase) * dt
            if p[0] < x_lim[0]:
                p[0] = x_lim[0]
                d._vel[0] = abs(d._vel[0])
            elif p[0] > x_lim[1]:
                p[0] = x_lim[1]
                d._vel[0] = -abs(d._vel[0])
            if p[1] < y_lim[0]:
                p[1] = y_lim[0]
                d._vel[1] = abs(d._vel[1])
            elif p[1] > y_lim[1]:
                p[1] = y_lim[1]
                d._vel[1] = -abs(d._vel[1])
            if avoid_rect is not None:
                ax0, ay0, ax1, ay1 = avoid_rect
                if ax0 <= p[0] <= ax1 and ay0 <= p[1] <= ay1:
                    if d.get_center()[1] >= ay1 - 0.05:
                        p[1] = ay1 + 0.01
                        d._vel[1] = abs(d._vel[1])
                    else:
                        p[0] = ax1 + 0.01
                        d._vel[0] = abs(d._vel[0])
            d.move_to(p)

    dots.add_updater(_update)
    return dots


def make_leak_stream(x_lim=(-2.9, 0.9), y0=1.18, y1=2.95, count=5, speed=0.65, seed=19, radius=0.065):
    """Sparse or heavy stream of BLUE dots rising through the upper skin into the air."""
    rng = np.random.default_rng(seed)
    grp = VGroup()
    for i in range(count):
        x = rng.uniform(x_lim[0], x_lim[1])
        s = (i / max(count, 1)) % 1.0
        d = Dot([x, y0 + s * (y1 - y0), 0.0], radius=radius, color=BLUE)
        d._s = s
        d._x0 = x
        d._spd = speed * rng.uniform(0.85, 1.15)
        grp.add(d)

    def _upd(g, dt):
        if dt <= 0:
            return
        span = y1 - y0
        for d in g:
            d._s = (d._s + d._spd * dt / span) % 1.0
            y = y0 + d._s * span
            x = d._x0 + 0.06 * np.sin(5.0 * d._s)
            op = 0.92 if d._s < 0.78 else max(0.05, 0.92 * (1.0 - (d._s - 0.78) / 0.22))
            d.move_to([x, y, 0.0]).set_opacity(op)

    grp.add_updater(_upd)
    return grp


def make_sweat_flow(n_drops=9, speed=0.52):
    """Sweat drops rising along the coiled BLUE duct, pooling at pore, and evaporating."""
    grp = VGroup()
    drops = VGroup()
    for i in range(n_drops):
        s = i / n_drops
        d = Dot(_duct_pt(s), radius=0.072, color=BLUE)
        d._s = s
        drops.add(d)

    puddle = Ellipse(width=0.72, height=0.11, stroke_color=BLUE, stroke_width=2.0,
                     fill_color=BLUE, fill_opacity=0.68).move_to([DUCT_X, CORNEUM_TOP + 0.05, 0.0])

    vapour = VGroup()
    for k, dx in enumerate([-0.20, 0.0, 0.20]):
        v = VMobject(stroke_color=BLUE, stroke_width=3.5)
        v._dx = dx
        v._phase = k * 1.6
        vapour.add(v)
    vapour._t = 0.0

    def _upd_drops(g, dt):
        for d in g:
            d._s = (d._s + speed * dt) % 1.0
            d.move_to(_duct_pt(d._s))

    def _upd_vap(g, dt):
        g._t += dt
        for v in g:
            ys = np.linspace(CORNEUM_TOP + 0.14, CORNEUM_TOP + 0.92, 18)
            pts = [
                np.array([
                    DUCT_X + v._dx + 0.07 * np.sin(8.0 * (y - CORNEUM_TOP) - 5.2 * g._t + v._phase),
                    y,
                    0.0,
                ])
                for y in ys
            ]
            v.set_points_as_corners(pts)

    _upd_vap(vapour, 0.0)
    drops.add_updater(_upd_drops)
    vapour.add_updater(_upd_vap)
    grp.add(drops, puddle, vapour)
    return grp


def make_tracer_stream(lane_paths, s_max=0.42, n_per_lane=3, speed=0.22, radius=0.072, stop_at=False):
    """Continuous deterministic stream of TEAL tracers walking along intercellular lanes."""
    grp = VGroup()
    for k, pts in enumerate(lane_paths):
        for j in range(n_per_lane):
            s0 = (j / n_per_lane) * s_max
            d = Dot(_eval_polyline(pts, s0), radius=radius, color=TEAL)
            d._lane = k
            d._s = s0
            d._ph = k * 1.3 + j * 2.1
            d._t = 0.0
            grp.add(d)

    def _upd(g, dt):
        if dt <= 0:
            return
        for d in g:
            d._t += dt
            if stop_at and d._s >= s_max - 0.05:
                # Cycle from lower half up to s_max and jostle at barrier
                d._s = (d._s + speed * dt) % s_max
            else:
                d._s = (d._s + speed * dt) % s_max
            base = _eval_polyline(lane_paths[d._lane], d._s)
            jit = np.array([0.025 * np.sin(6.0 * d._t + d._ph), 0.0, 0.0])
            d.move_to(base + jit)

    grp.add_updater(_upd)
    return grp


def make_epidermis_dermis_labels():
    """Left-side epidermis bracket+label and dermis label in clean positions."""
    br_x = SKIN_X0 - 0.25
    bracket = VGroup(
        Line([br_x + 0.14, CORNEUM_TOP, 0], [br_x, CORNEUM_TOP, 0], color=TEXT, stroke_width=2.5),
        Line([br_x, CORNEUM_TOP, 0], [br_x, DERMIS_Y1 + 0.05, 0], color=TEXT, stroke_width=2.5),
        Line([br_x, DERMIS_Y1 + 0.05, 0], [br_x + 0.14, DERMIS_Y1 + 0.05, 0], color=TEXT, stroke_width=2.5),
    )
    epi_lbl = T("epidermis", 28, TEXT).next_to(bracket, LEFT, buff=0.18)
    derm_lbl = T("dermis", 28, TEXT).move_to([-2.45, -2.02, 0.0])
    return VGroup(bracket, epi_lbl), derm_lbl


# ------------------------------------------------------------------ Scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        bar = RoundedRectangle(
            corner_radius=0.10, width=8.6, height=0.72,
            stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35,
        ).move_to([0.0, -1.35, 0.0])
        bar_lbl = T("skin", 28, TEXT).move_to(bar)

        evap_drop = Ellipse(width=0.95, height=0.28, stroke_color=BLUE, stroke_width=2.5,
                            fill_color=BLUE, fill_opacity=0.75).move_to([-1.6, -0.84, 0.0])
        drip_drop = Dot([1.8, -0.80, 0.0], radius=0.15, color=GREY)
        drip_drop._t = 0.0

        def _upd_drip(m, dt):
            m._t = (m._t + dt * 0.55) % 1.0
            if m._t < 0.4:
                u = m._t / 0.4
                m.move_to([1.8 + 2.55 * u, -0.80 - 0.15 * u, 0.0])
            else:
                u = (m._t - 0.4) / 0.6
                m.move_to([4.35, -0.95 - 1.55 * (u ** 2), 0.0])
            m.set_opacity(1.0 if m._t < 0.85 else max(0.1, (1.0 - m._t) / 0.15))

        drip_drop.add_updater(_upd_drip)

        vap_waves = VGroup()
        for k, dx in enumerate([-0.26, 0.0, 0.26]):
            vw = VMobject(stroke_color=BLUE, stroke_width=3.5)
            vw._dx = dx
            vw._ph = k * 1.4
            vap_waves.add(vw)
        vap_waves._t = 0.0

        def _upd_vap(g, dt):
            g._t += dt
            for v in g:
                ys = np.linspace(-0.62, 0.72, 20)
                pts = [
                    np.array([-1.6 + v._dx + 0.09 * np.sin(6.5 * (y + 0.6) - 4.2 * g._t + v._ph), y, 0.0])
                    for y in ys
                ]
                v.set_points_as_corners(pts)

        _upd_vap(vap_waves, 0.0)
        vap_waves.add_updater(_upd_vap)

        self.add(bar, bar_lbl, evap_drop, vap_waves, drip_drop)

        self.at("why doesn't")
        body_water = make_water_dots(count=26, x_lim=(-4.1, 4.1), y_lim=(-2.95, -1.80), seed=11, radius=0.075)
        self.play(FadeIn(body_water), run_time=0.45)

        self.at("seep out")
        nudgers = VGroup(*[Dot([x, -2.15, 0.0], radius=0.08, color=BLUE) for x in (-2.2, -0.3, 1.5)])
        self.play(FadeIn(nudgers), run_time=0.15)
        self.play(nudgers.animate.shift(UP * 0.36), run_time=0.55, rate_func=there_and_back)

        self.at("dead cells")
        drip_drop.clear_updaters()
        vap_waves.clear_updaters()
        body_water.clear_updaters()

        sw = build_skin_world()
        dermis_dots = make_water_dots(count=24, x_lim=(-3.25, 1.25), y_lim=(-2.30, -1.12), seed=17, radius=0.075)
        stag = scope_tag("schematic")
        self.play(
            FadeOut(VGroup(evap_drop, vap_waves, drip_drop, nudgers, body_water, bar_lbl), run_time=0.45),
            ReplacementTransform(bar, sw.world, run_time=1.0),
        )
        self.play(FadeIn(dermis_dots), FadeIn(stag), run_time=0.35)

        self.at("holds the water")
        q = T("What holds the water in?", 38, TEXT).move_to([0.0, 2.95, 0.0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.45)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Skin, Sweat and Human Thermoregulation"
    TITLE = "Where Skin Keeps Its Water"


class S02Conveyor(SpokenScene):
    def construct(self):
        sw = build_skin_world()
        epi_lbl, derm_lbl = make_epidermis_dermis_labels()
        dermis_dots = make_water_dots(
            count=22, x_lim=(-3.25, 1.25), y_lim=(-2.30, -1.12), seed=17,
            avoid_rect=(-3.25, -2.35, -1.65, -1.70), radius=0.075,
        )
        stag = scope_tag("schematic")
        self.add(sw.world, dermis_dots, stag)
        self.play(FadeIn(epi_lbl), FadeIn(derm_lbl), run_time=0.55)

        # Pick central basale cell (col index 2, x = -1.00, y = -0.74) to divide
        base_cell = sw.cell_grid[0][2][4]
        col2 = [sw.cell_grid[r][2][4] for r in range(5)]
        self.at("divide at the base")
        hl = SurroundingRectangle(base_cell, color=GOLD, buff=0.05, stroke_width=3.0)
        daughter = _make_cell(-1.00, -0.74, 0.78, 0.36)
        self.play(Create(hl), run_time=0.35)
        self.add(daughter)
        self.play(
            daughter.animate(run_time=0.75).move_to([-0.93, -0.26, 0.0]).scale(0.95),
            FadeOut(col2[1], run_time=0.40),
            FadeOut(hl, run_time=0.35),
        )

        # Conveyor rises row by row; layer labels appear on the right
        self.at("move outward")
        layer_specs = [
            ("corneum", 1.72, 28, TEXT),
            ("granulosum", 0.81, 28, TEXT),
            ("spinosum", -0.03, 28, TEXT),
            ("basale", -0.74, 28, TEXT),
        ]
        layer_lbls = VGroup()
        for name, y, sz, col in layer_specs:
            t = T(name, sz, col).move_to([3.95, y, 0.0])
            tick = Line([SKIN_X1 + 0.14, y, 0], [t.get_left()[0] - 0.14, y, 0], color=GREY, stroke_width=2.0)
            layer_lbls.add(VGroup(tick, t))
        thin_tag = T("thin skin", 24, TEXT).next_to(layer_lbls[-1][1], DOWN, buff=0.28)

        self.play(
            daughter.animate(run_time=1.8).move_to([-1.06, 0.20, 0.0]),
            Succession(Wait(0.35), FadeIn(col2[1], run_time=0.55)),
            FadeOut(col2[2], run_time=0.65),
            LaggedStart(*[FadeIn(lb, shift=LEFT * 0.1) for lb in layer_lbls], lag_ratio=0.18, run_time=1.8),
            FadeIn(thin_tag, run_time=1.8),
        )
        self.play(
            daughter.animate(run_time=0.9).move_to([-0.95, 0.63, 0.0]).stretch(0.75, 1),
            Succession(Wait(0.25), FadeIn(col2[2], run_time=0.45)),
            FadeOut(col2[3], run_time=0.45),
        )

        # Fill with keratin, flatten, lose nucleus -> replace row-0 plate cleanly (cx = -0.53)
        self.at("fill with keratin")
        k_s1 = Line([-1.30, 1.03, 0], [-0.70, 1.03, 0], color=GREY, stroke_width=2.2)
        k_s2 = Line([-1.25, 0.95, 0], [-0.75, 0.95, 0], color=GREY, stroke_width=2.2)
        k_grp = VGroup(k_s1, k_s2)
        self.play(
            daughter.animate(run_time=0.65).move_to([-1.04, 0.99, 0.0]).stretch(0.78, 1),
            Succession(Wait(0.20), FadeIn(col2[3], run_time=0.35)),
            FadeOut(col2[4], run_time=0.35),
        )
        self.play(FadeIn(k_grp), FadeOut(daughter[1]), run_time=0.55)

        # Fade out old row-0 plate at idx 2 (cx = -0.53) so new plate slots cleanly into the row without overlap
        target_plate = sw.corneum_rows[0][2]
        plate_new = _make_plate(target_plate.get_center()[0], 1.30, target_plate.width, 0.15, keratin=True)
        self.play(
            FadeOut(target_plate, shift=UP * 0.18, run_time=0.75),
            ReplacementTransform(VGroup(daughter[0], k_grp), plate_new, run_time=0.75),
            Succession(Wait(0.20), FadeIn(col2[4], run_time=0.45)),
        )

        # On "corneocytes": top GREY plates pulse with label
        self.at("corneocytes")
        corn_lbl = T("corneocytes: dead, no nucleus", 28, TEXT).move_to([-0.5, 2.92, 0.0])
        ptr = Arrow(corn_lbl.get_bottom() + DOWN * 0.05, [-0.5, 2.26, 0.0],
                    color=GREY, stroke_width=2.5, buff=0.04, tip_length=0.16)
        top_plates = sw.corneum_rows[-1]
        self.play(
            FadeIn(corn_lbl), FadeIn(ptr),
            top_plates.animate.set_stroke(TEXT, width=4.0),
            run_time=0.55,
        )
        self.play(top_plates.animate.set_stroke(GREY, width=2.0), run_time=0.55)
        self.play(top_plates.animate.shift(UP * 0.05), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S03Job(SpokenScene):
    def construct(self):
        sw = build_skin_world()
        epi_lbl, derm_lbl = make_epidermis_dermis_labels()
        water = make_water_dots(
            count=34, x_lim=(-3.25, 1.25), y_lim=(-2.25, 1.12), seed=23,
            avoid_rect=(-3.25, -2.35, -1.65, -1.70), radius=0.075, speed_range=(1.0, 1.65),
        )
        stag = scope_tag("schematic")
        self.add(sw.world, epi_lbl, derm_lbl, water, stag)

        # Highlight the wall holding water in during the opening sentence (avoids 5.7s wait freeze)
        self.play(sw.corneum.animate.set_stroke(TEXT, width=3.2), run_time=1.2)
        self.play(sw.corneum.animate.set_stroke(GREY, width=2.0), run_time=1.2)

        self.at("small steady leak")
        leak = make_leak_stream(x_lim=(-2.8, 0.6), y0=1.20, y1=2.60, count=5, speed=0.65, seed=31, radius=0.065)
        leak_lbl = T("small, steady leak", 28, BLUE).move_to([-1.25, 3.05, 0.0])
        self.add(leak)
        self.play(FadeIn(leak_lbl, shift=DOWN * 0.1), run_time=0.5)

        self.at("sweat ducts")
        sweat_flow = make_sweat_flow(n_drops=9, speed=0.55)
        sweat_lbl = T("sweat: spent\non purpose", 28, BLUE).move_to([4.45, 2.75, 0.0])
        sweat_ptr = Arrow([3.28, 2.68, 0.0], [DUCT_X + 0.35, 2.45, 0.0],
                          color=BLUE, stroke_width=2.5, buff=0.05, tip_length=0.16)
        self.play(
            sw.duct_core.animate.set_stroke(BLUE, width=6.5, opacity=1.0),
            FadeIn(sweat_flow),
            FadeIn(sweat_lbl),
            FadeIn(sweat_ptr),
            run_time=0.65,
        )
        self.finish()


class S04Guess(SpokenScene):
    def construct(self):
        sw = build_skin_world()
        epi_lbl, derm_lbl = make_epidermis_dermis_labels()
        water = make_water_dots(
            count=26, x_lim=(-3.25, 1.25), y_lim=(-2.25, 1.05), seed=29,
            avoid_rect=(-3.25, -2.35, -1.65, -1.70), radius=0.075, speed_range=(0.95, 1.55),
        )
        stag = scope_tag("schematic")
        self.add(sw.world, epi_lbl, derm_lbl, water, stag)

        self.play(Create(sw.lanes_grp), run_time=1.2)

        # Gut/kidney inset cleanly inside x in [-6.33, -3.97] (clear of epi_lbl bracket at br_x = -3.65)
        self.at("gut and kidney")
        inset_box = RoundedRectangle(
            corner_radius=0.14, width=2.35, height=1.95,
            stroke_color=PURPLE, stroke_width=2.5, fill_color=BG, fill_opacity=0.95,
        ).move_to([-5.15, 2.25, 0.0])
        inset_cells = VGroup(*[
            _make_cell(-5.79 + i * 0.64, 2.62, 0.50, 0.40) for i in range(3)
        ])
        inset_bars = VGroup(*[
            Line([-5.47 + i * 0.64, 2.51, 0], [-5.47 + i * 0.64, 2.73, 0],
                 color=PURPLE, stroke_width=7.5)
            for i in range(2)
        ])
        inset_lbl = T("gut, kidney:\ntight junctions", 24, PURPLE).move_to([-5.15, 1.72, 0.0])
        inset = VGroup(inset_box, inset_cells, inset_bars, inset_lbl)
        self.play(FadeIn(inset, shift=DOWN * 0.1), run_time=0.55)

        self.at("the natural guess")
        seal_y = -0.03
        guess_line = VGroup(
            DashedLine([SKIN_X0 + 0.05, seal_y, 0.0], [1.36, seal_y, 0.0],
                       color=PURPLE, stroke_width=4.0, dash_length=0.14),
            DashedLine([2.04, seal_y, 0.0], [SKIN_X1 - 0.04, seal_y, 0.0],
                       color=PURPLE, stroke_width=4.0, dash_length=0.14),
        )
        guess_lbl = T("expected seal?", 28, PURPLE).move_to([4.75, seal_y, 0.0])
        guess_ptr = Arrow([guess_lbl.get_left()[0] - 0.12, seal_y, 0.0], [SKIN_X1 + 0.06, seal_y, 0.0],
                          color=PURPLE, stroke_width=2.5, buff=0.04, tip_length=0.16)
        self.play(
            FadeOut(inset, run_time=0.45),
            Create(guess_line, run_time=0.65),
            FadeIn(guess_lbl, run_time=0.55),
            FadeIn(guess_ptr, run_time=0.55),
        )
        self.finish()


class S05Experiment(SpokenScene):
    def construct(self):
        sw = build_skin_world()
        water = make_water_dots(count=32, x_lim=(-3.25, 1.25), y_lim=(-2.25, -1.12), seed=37,
                                radius=0.078, speed_range=(1.05, 1.70))
        seal_y = -0.03
        guess_line = VGroup(
            DashedLine([SKIN_X0 + 0.05, seal_y, 0.0], [1.36, seal_y, 0.0],
                       color=PURPLE, stroke_width=4.0, dash_length=0.14),
            DashedLine([2.04, seal_y, 0.0], [SKIN_X1 - 0.04, seal_y, 0.0],
                       color=PURPLE, stroke_width=4.0, dash_length=0.14),
        )
        guess_lbl = T("expected seal?", 28, PURPLE).move_to([4.75, seal_y, 0.0])
        guess_ptr = Arrow([guess_lbl.get_left()[0] - 0.12, seal_y, 0.0], [SKIN_X1 + 0.06, seal_y, 0.0],
                          color=PURPLE, stroke_width=2.5, buff=0.04, tip_length=0.16)
        stag = scope_tag("schematic")
        self.add(sw.world, water, guess_line, guess_lbl, guess_ptr, stag)

        tag_study = T("newborn mouse skin, 1975", 26, TEXT).move_to([-4.05, 3.08, 0.0])
        tag_em = T("electron microscope view (schematic)", 24, TEAL).move_to([-3.55, 2.62, 0.0])
        self.play(FadeIn(tag_study), run_time=0.8)
        self.play(FadeIn(tag_em), Create(sw.lanes_grp), run_time=3.5)

        # On "followed tracers": continuous stream of TEAL tracers enters lanes and walks upward
        self.at("followed tracers")
        tracers = make_tracer_stream(sw.lane_paths, s_max=0.40, n_per_lane=4, speed=0.28, radius=0.078)
        self.play(FadeIn(tracers), run_time=0.55)

        self.at("if tight junctions")
        ghost_dots = VGroup()
        for k in range(4):
            xm = sw.lane_paths[k][2][0]
            for dy in (-0.08, 0.04, 0.16):
                gd = Circle(radius=0.065, stroke_color=TEAL, stroke_width=2.2,
                            fill_color=TEAL, fill_opacity=0.22).move_to([xm, seal_y - dy, 0.0])
                ghost_dots.add(gd)
        ghost_lbl = T("prediction if\njunctions seal", 26, TEAL).move_to([4.75, -0.82, 0.0])

        self.at("would stop there")
        self.play(FadeIn(ghost_dots), FadeIn(ghost_lbl), run_time=0.55)
        self.finish()


class S06Result(SpokenScene):
    def construct(self):
        sw = build_skin_world()
        water = make_water_dots(count=32, x_lim=(-3.25, 1.25), y_lim=(-2.25, -1.12), seed=37,
                                radius=0.078, speed_range=(1.05, 1.70))
        seal_y = -0.03
        guess_line = VGroup(
            DashedLine([SKIN_X0 + 0.05, seal_y, 0.0], [1.36, seal_y, 0.0],
                       color=PURPLE, stroke_width=4.0, dash_length=0.14),
            DashedLine([2.04, seal_y, 0.0], [SKIN_X1 - 0.04, seal_y, 0.0],
                       color=PURPLE, stroke_width=4.0, dash_length=0.14),
        )
        guess_lbl = T("expected seal?", 28, PURPLE).move_to([4.75, seal_y, 0.0])
        guess_ptr = Arrow([guess_lbl.get_left()[0] - 0.12, seal_y, 0.0], [SKIN_X1 + 0.06, seal_y, 0.0],
                          color=PURPLE, stroke_width=2.5, buff=0.04, tip_length=0.16)
        tag_study = T("newborn mouse skin, 1975", 26, TEXT).move_to([-4.05, 3.08, 0.0])
        tag_em = T("electron microscope view (schematic)", 24, TEAL).move_to([-3.55, 2.62, 0.0])
        stag = scope_tag("schematic")

        ghost_dots = VGroup()
        for k in range(4):
            xm = sw.lane_paths[k][2][0]
            for dy in (-0.08, 0.04, 0.16):
                ghost_dots.add(
                    Circle(radius=0.065, stroke_color=TEAL, stroke_width=2.2,
                           fill_color=TEAL, fill_opacity=0.22).move_to([xm, seal_y - dy, 0.0])
                )
        ghost_lbl = T("prediction if\njunctions seal", 26, TEAL).move_to([4.75, -0.82, 0.0])

        # Continuous stream advancing all the way to upper granulosum (s_max = 0.90)
        tracers = make_tracer_stream(sw.lane_paths, s_max=0.90, n_per_lane=4, speed=0.28, radius=0.075)
        self.add(sw.world, sw.lanes_grp, water, guess_line, guess_lbl, guess_ptr,
                 tag_study, tag_em, ghost_dots, ghost_lbl, tracers, stag)

        # Fade ghost prediction immediately on "Instead" / "slipped past"
        self.play(
            FadeOut(ghost_dots), FadeOut(ghost_lbl),
            FadeOut(guess_line), FadeOut(guess_lbl), FadeOut(guess_ptr),
            run_time=0.65,
        )

        # Held halt markers at upper granulosum as tracers keep arriving and halting there
        self.at("stopped high")
        halt_dots = VGroup()
        for k in range(4):
            pt = _eval_polyline(sw.lane_paths[k], 0.90)
            halt_dots.add(Dot(pt, radius=0.08, color=TEAL))
        self.play(FadeIn(halt_dots), run_time=0.55)

        self.at("lamellar bodies")
        gran_top = sw.cell_grid[4]
        granules = VGroup()
        for cx, cy, _w, _h, _m in gran_top:
            for dx in (-0.18, 0.18):
                granules.add(Ellipse(width=0.14, height=0.075, stroke_width=0,
                                     fill_color=GOLD, fill_opacity=0.95).move_to([cx + dx, cy, 0.0]))
        lam_lbl = T("lamellar bodies", 28, GOLD).move_to([4.35, 0.99, 0.0])
        lam_ptr = Arrow(lam_lbl.get_left() + LEFT * 0.05, [SKIN_X1 + 0.02, 0.99, 0.0],
                        color=GOLD, stroke_width=2.5, buff=0.04, tip_length=0.15)
        self.play(FadeIn(granules), FadeIn(lam_lbl), FadeIn(lam_ptr), run_time=0.55)

        self.at("had emptied")
        self.play(granules.animate.shift(UP * 0.14), run_time=0.5)
        self.play(ReplacementTransform(granules, sw.gold_mortar), run_time=0.75)

        self.at("main barrier")
        bar_lbl = T("lipid: main barrier", 28, GOLD).move_to([4.45, 1.69, 0.0])
        bar_ptr = Arrow(bar_lbl.get_left() + LEFT * 0.05, [SKIN_X1 + 0.02, 1.69, 0.0],
                        color=GOLD, stroke_width=2.5, buff=0.04, tip_length=0.15)
        self.play(swap(VGroup(lam_lbl, lam_ptr), VGroup(bar_lbl, bar_ptr)), run_time=0.7)
        self.finish()


class S07Idea(SpokenScene):
    def construct(self):
        sw = build_skin_world(with_gold=True)
        stag = scope_tag("schematic")
        # Detach RIGHT_COL pieces in upper layers so they fade out cleanly with sw.lower (duct)
        right_col_upper = VGroup(
            sw.granulosum[1][-1],
            *[row[-1] for row in sw.corneum_rows],
            *[sw.gold_mortar[2 * i + 1] for i in range(4)],
        )
        sw.granulosum[1].remove(sw.granulosum[1][-1])
        for row in sw.corneum_rows:
            row.remove(row[-1])
        for m in list(right_col_upper[5:]):
            sw.gold_mortar.remove(m)
        self.add(sw.world, right_col_upper, stag)

        # Zoom upper granulosum + corneum into left/center [-5.8, +0.95], leaving right free for label
        target_scale = 1.42
        shift_vec = np.array([-1.45, -1.95, 0.0])
        center_before = sw.upper.get_center().copy()
        self.play(
            FadeOut(sw.lower, run_time=0.5),
            FadeOut(right_col_upper, run_time=0.5),
            sw.upper.animate.scale(target_scale).shift(shift_vec),
            run_time=1.2,
        )

        # Dim solid gold mortar blocks and reveal 3 stacked lamellar stripes per gap
        x_left = (-3.32 - center_before[0]) * target_scale + center_before[0] + shift_vec[0]
        x_right = (1.36 - center_before[0]) * target_scale + center_before[0] + shift_vec[0]
        stripes = VGroup()
        for y_gap in [1.16, 1.43, 1.69, 1.95]:
            yg = (y_gap - center_before[1]) * target_scale + center_before[1] + shift_vec[1]
            for dy in (-0.038, 0.0, 0.038):
                stripes.add(Line([x_left, yg + dy, 0.0], [x_right, yg + dy, 0.0],
                                 color=GOLD, stroke_width=2.6))

        y_gold_bot = (1.08 - center_before[1]) * target_scale + center_before[1] + shift_vec[1]
        zoom_water = make_water_dots(
            count=28, x_lim=(x_left + 0.15, x_right - 0.15),
            y_lim=(-2.55, y_gold_bot - 0.06), seed=53, radius=0.085, speed_range=(1.0, 1.55),
        )
        self.play(
            sw.gold_mortar.animate.set_fill(opacity=0.18),
            Create(stripes),
            FadeIn(zoom_water),
            run_time=1.5,
        )

        self.at("bricks in mortar")
        bim_lbl = T("bricks in mortar", 28, GOLD).move_to([4.55, 0.35, 0.0])
        self.play(FadeIn(bim_lbl, shift=LEFT * 0.1), run_time=0.45)

        self.at("main water seal")
        idea_line = T("Main seal: lipid between dead cells", 34, TEXT).move_to([0.0, 2.98, 0.0])
        self.play(FadeIn(idea_line, shift=UP * 0.08), run_time=0.55)

        self.wait(max(0.1, self.narration_s - 2.1 - self.elapsed()))
        self.play(
            FadeOut(stripes), FadeOut(bim_lbl), FadeOut(zoom_water), FadeOut(idea_line),
            sw.gold_mortar.animate.set_fill(opacity=0.88),
            sw.upper.animate.shift(-shift_vec).scale(1.0 / target_scale),
            FadeIn(sw.lower),
            FadeIn(right_col_upper),
            run_time=1.3,
        )
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        sw = build_skin_world(with_gold=True, with_junctions=False)
        water = make_water_dots(count=26, x_lim=(-3.25, 1.25), y_lim=(-2.25, 1.05), seed=61,
                                radius=0.075, speed_range=(0.95, 1.55))
        stag = scope_tag("schematic")
        self.add(sw.world, water, stag)

        self.at("tight junctions")
        tj_lbl = T("tight junctions,\ngranular layer", 28, PURPLE).move_to([4.45, 0.81, 0.0])
        tj_ptr = Arrow(tj_lbl.get_left() + LEFT * 0.05, [SKIN_X1 + 0.04, 0.81, 0.0],
                       color=PURPLE, stroke_width=2.5, buff=0.04, tip_length=0.15)
        self.play(FadeIn(sw.tight_junctions), FadeIn(tj_lbl), FadeIn(tj_ptr), run_time=0.65)

        self.at("mice were bred")
        mouse_tag = boxed_label("mice: no claudin-1", TEXT, size=26, stroke=2.0).move_to([-4.35, 2.95, 0.0])
        self.play(FadeIn(mouse_tag, shift=RIGHT * 0.2), run_time=0.55)

        self.at("losing that protein")
        dim_tjs = build_skin_world(with_gold=True, with_junctions=True, junctions_dim=True).tight_junctions
        q = question_card("Does losing claudin-1 matter?", y=-3.02, color=TEXT, size=32)
        self.play(
            ReplacementTransform(sw.tight_junctions, dim_tjs),
            FadeIn(q.question, shift=UP * 0.1),
            run_time=0.65,
        )
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Does losing claudin-1 matter?"
    CARD = {"color": TEXT, "size": 32, "y": -3.02}
    RING_AT = (5.8, -2.95, 0)
    SECONDS = 4.5

    def backdrop(self):
        sw = build_skin_world(with_gold=True, with_junctions=True, junctions_dim=True)
        tj_lbl = T("tight junctions,\ngranular layer", 28, PURPLE).move_to([4.45, 0.81, 0.0])
        tj_ptr = Arrow(tj_lbl.get_left() + LEFT * 0.05, [SKIN_X1 + 0.04, 0.81, 0.0],
                       color=PURPLE, stroke_width=2.5, buff=0.04, tip_length=0.15)
        mouse_tag = boxed_label("mice: no claudin-1", TEXT, size=26, stroke=2.0).move_to([-4.35, 2.95, 0.0])
        water = make_water_dots(count=26, x_lim=(-3.25, 1.25), y_lim=(-2.25, 1.05), seed=61, radius=0.075)
        water.clear_updaters()
        return VGroup(sw.world, tj_lbl, tj_ptr, mouse_tag, water)


class S10Answer(SpokenScene):
    def construct(self):
        sw = build_skin_world(with_gold=True, with_junctions=True, junctions_dim=True)
        tj_lbl = T("tight junctions,\ngranular layer", 28, PURPLE).move_to([4.45, 0.81, 0.0])
        tj_ptr = Arrow(tj_lbl.get_left() + LEFT * 0.05, [SKIN_X1 + 0.04, 0.81, 0.0],
                       color=PURPLE, stroke_width=2.5, buff=0.04, tip_length=0.15)
        mouse_tag = boxed_label("mice: no claudin-1", TEXT, size=26, stroke=2.0).move_to([-4.35, 2.95, 0.0])
        q = question_card("Does losing claudin-1 matter?", y=-3.02, color=TEXT, size=32)
        water = make_water_dots(count=24, x_lim=(-3.25, 1.25), y_lim=(-2.25, 1.05), seed=61,
                                radius=0.075, speed_range=(0.95, 1.55))
        stag = scope_tag("schematic")
        self.add(sw.world, tj_lbl, tj_ptr, mouse_tag, q.question, water, stag)

        loss = ValueTracker(0.10)
        g_w, g_h = 0.55, 2.20
        gx, gy = 4.35, -0.75
        g_frame = Rectangle(width=g_w, height=g_h, stroke_color=GREY, stroke_width=2.5,
                            fill_color=BG, fill_opacity=0.8).move_to([gx, gy, 0.0])
        g_fill = always_redraw(lambda: Rectangle(
            width=g_w - 0.08,
            height=max(0.06, (g_h - 0.08) * float(np.clip(loss.get_value(), 0.0, 1.0))),
            stroke_width=0, fill_color=BLUE, fill_opacity=0.85,
        ).align_to(g_frame.get_bottom() + UP * 0.04, DOWN).set_x(gx))
        g_lbl = T("water lost\n(schematic)", 26, BLUE).next_to(g_frame, DOWN, buff=0.18)
        gauge = VGroup(g_frame, g_fill, g_lbl)

        # Keep heavy_leak in x in [-1.55, 1.15] so it never touches left-side study/outcome labels
        heavy_leak = make_leak_stream(x_lim=(-1.55, 1.15), y0=0.70, y1=3.05, count=20, speed=1.20,
                                      seed=71, radius=0.07)
        self.add(heavy_leak)
        self.play(FadeOut(q.question), FadeOut(tj_lbl), FadeOut(tj_ptr), run_time=0.45)
        self.play(
            FadeIn(gauge),
            loss.animate.set_value(0.88),
            run_time=0.95,
        )

        self.at("in 2002")
        furuse_tag = T("Furuse and colleagues, 2002", 26, TEXT).move_to([-4.25, 3.10, 0.0])
        self.play(swap(mouse_tag, furuse_tag), run_time=0.55)

        self.at("died within a day")
        died_lbl = T("died within a day of birth", 26, TEXT).move_to([-4.25, 2.62, 0.0])
        self.play(FadeIn(died_lbl, shift=DOWN * 0.08), run_time=0.45)

        self.at("tight junctions")
        self.play(FadeOut(furuse_tag), FadeOut(died_lbl), run_time=0.4)
        full_tjs = build_skin_world(with_gold=True, with_junctions=True, junctions_dim=False).tight_junctions
        steady_leak = make_leak_stream(x_lim=(-1.55, 0.85), y0=1.20, y1=2.95, count=4, speed=0.55,
                                       seed=73, radius=0.065)
        self.add(steady_leak)
        self.play(
            ReplacementTransform(sw.tight_junctions, full_tjs),
            FadeOut(heavy_leak),
            loss.animate.set_value(0.12),
            run_time=1.4,
        )
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        sw = build_skin_world(with_gold=True, with_junctions=True, junctions_dim=False)
        water = make_water_dots(count=26, x_lim=(-3.25, 1.25), y_lim=(-2.25, 1.05), seed=83,
                                radius=0.075, speed_range=(0.95, 1.55))
        steady_leak = make_leak_stream(x_lim=(-2.8, 0.6), y0=1.20, y1=2.95, count=4, speed=0.55,
                                       seed=89, radius=0.065)
        stag = scope_tag("schematic")
        self.add(sw.world, water, steady_leak, stag)

        self.at("dead cells")
        dc_lbl = T("dead cells", 28, GREY).move_to([4.35, 1.85, 0.0])
        self.play(
            sw.corneum.animate.set_stroke(TEXT, width=3.6),
            FadeIn(dc_lbl, shift=LEFT * 0.1),
            run_time=0.45,
        )
        self.play(sw.corneum.animate.set_stroke(GREY, width=2.0), run_time=0.35)

        self.at("mortared with lipid")
        lip_lbl = T("lipid mortar", 28, GOLD).move_to([4.35, 1.20, 0.0])
        self.play(
            sw.gold_mortar.animate.set_fill(opacity=1.0),
            FadeIn(lip_lbl, shift=LEFT * 0.1),
            run_time=0.45,
        )

        self.at("junctions beneath")
        tj_lbl = T("tight junctions", 28, PURPLE).move_to([4.35, 0.55, 0.0])
        self.play(
            sw.tight_junctions.animate.set_stroke(PURPLE, width=9.0),
            FadeIn(tj_lbl, shift=LEFT * 0.1),
            run_time=0.45,
        )
        self.play(sw.tight_junctions.animate.set_stroke(PURPLE, width=7.0), run_time=0.35)

        self.at("sweat ducts")
        sweat_flow = make_sweat_flow(n_drops=9, speed=0.55)
        sw_lbl = T("sweat: spent\non purpose", 28, BLUE).move_to([4.45, 2.75, 0.0])
        sw_ptr = Arrow([3.28, 2.68, 0.0], [DUCT_X + 0.35, 2.45, 0.0],
                       color=BLUE, stroke_width=2.5, buff=0.04, tip_length=0.15)
        self.play(
            sw.duct_core.animate.set_stroke(BLUE, width=6.5, opacity=1.0),
            FadeIn(sweat_flow),
            FadeIn(sw_lbl),
            FadeIn(sw_ptr),
            run_time=0.6,
        )
        self.finish()


class S12End(EndCard):
    LINE = "Skin seals in water mainly with lipid between dead cells."
