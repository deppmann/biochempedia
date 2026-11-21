"""Smaller Filter, Same Phosphate Out — Chapter 2 of Calcium, Phosphate and Bone.

COLOUR MAP (one colour per concept for the whole film):
    BLUE    (#58C4DD) : filtered phosphate load (and filtered dots)
    GREEN   (#83C167) : reabsorbed phosphate returning to blood
    ORANGE  (#F28C38) : excreted phosphate leaving in urine (and urine counter)
    PURPLE  (#B589F5) : PTH
    MAGENTA (#EE66B8) : FGF23 (and Klotho co-receptor ring)
    TAN     (#D9B472) : calcitriol
    GREY    (#8B93A1) : tissues and structural outlines (sieve, tubule, bone)
    TEXT    (#E8EAF0) : plasma phosphate gauge, gut inlet, labels
    RED     (#FC6255) : 100% ceiling line, failed PTH signature cross

THE ONE WORLD (carried from scene to scene):
    Left: gut inlet arrow ('from gut: 800 mg/day') above a kidney sieve whose mouth width
    is proportional to filtration rate (180, 60, or 15 L/day), plus a bone block bottom-left.
    Centre: horizontal filtered-load bar inside the tubule, proportional to GFR * 0.9 * P_p
    (5,333 mg/day = 9.0 frame units), split into GREEN reabsorbed and a fixed 1.35-unit
    ORANGE excreted block (800 mg/day) above the ORANGE urine counter ('urine: 800 mg/day').
    Right: tall vertical WHITE plasma phosphate gauge (0 to 12 mg/dL, 'healthy' mark at 3.3).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s00_link_and_question : Ghost calcium bar grows with 2% excretion stream, then fades as
                            the 9-unit phosphate bar grows (85% GREEN, 15% ORANGE) with computed
                            dot flux; frame splits to compare healthy (180 L/day -> 3.3 mg/dL)
                            vs failing (15 L/day -> 5.9 mg/dL), computed from 800/(GFR*0.9*FE*10),
                            urine counters pulse, right needle shakes on the question.
    s02_brake             : PURPLE PTH slides to GREEN/ORANGE boundary with 'set by calcium'
                            thread; GREY bone block rises and buds MAGENTA FGF23, which docks
                            at the Klotho ring on the boundary while dots keep flowing.
    s03_two_jobs          : GREEN/ORANGE boundary ghost-shifts left (schematic) as PTH & FGF23
                            glow; TAN calcitriol appears by gut inlet and dims as FGF23 lowers
                            it and gut arrow briefly thins.
    s04_arithmetic        : Hormone chips park by bone; colour-matched equation strip builds term
                            by term with the voice; sieve (180), gauge (3.3), and fraction (15%)
                            highlight in sync while 3.3 mg/dL = 33 mg/L, 0.9 x 33 ≈ 30 mg/L, and
                            180 L x 30 mg/L x 0.15 ≈ 800 mg/day build word by word.
    s05_idea              : Gut and urine 800 mg/day labels pulse with 'from gut = urine'; ghost sieve
                            narrows, '15%' swells, and ghost gauge needle rises and returns,
                            establishing 'in = out: share up, or level up'.
    s06_moderate          : Sieve narrows to 60 L/day (1/3); formula 1/3 filtration -> 3x level:
                            3.3 x 3 ≈ 9.9 builds as needle climbs to 9.9 mg/dL at 15% FE; FGF23
                            and PTH slide to the boundary and push FE to 50%, shrinking the bar
                            to 2.7 units while 800 ÷ (60 x 0.9 x 0.5) ≈ 30 mg/L = 3.0 mg/dL appears.
    s07_cohort            : '50%' pulses; three schematic cohort bars (FGF23 high, phosphate and
                            PTH normal) appear with arrow and 'FGF23 first?' and bars fade cleanly.
    s08_predict           : Sieve narrows to 15 L/day (1/12); GREEN bar drains to 0 leaving 100%
                            ORANGE 1.35-unit block; needle hides behind '?' under predict card.
    s10_answer            : RED 'ceiling: 100%' stop line appears; 800 ÷ (15 x 0.9 x 1.0) ≈ 59 mg/L
                            = 5.9 mg/dL builds word by word as '?' clears to 5.9 mg/dL; ghost 50%
                            bar (2.7 units), ghost needle (11.9), and ÷ 0.5 -> 11.9 appear, then
                            ghosts fade back to the 100% / 5.9 mg/dL case.
    s11_later             : Gauge needle creeps upward from 5.9 (schematic); calcitriol dims, PTH
                            grows at boundary; 'PTH: calcium up, phosphate down' card is crossed
                            out in RED while urine stays 800 mg/day.
    s12_return            : Computed recap stepping sieve and bar smoothly through 180 (3.3),
                            60 (3.0), and 15 L/day (5.9), brightening the 5.9 needle and rule.
"""

from bp_parts import *

# ------------------------------------------------------------------ concept palette
ORANGE = "#F28C38"
PURPLE = "#B589F5"
MAGENTA = "#EE66B8"
TAN = "#D9B472"

# ------------------------------------------------------------------ physiological model
INTAKE_MG = 800.0
FILTERABLE = 0.90
BAR_REF_LOAD = INTAKE_MG / 0.15   # 5,333.33 mg/day -> 9.0 frame units
BAR_MAX_W = 9.0
ORANGE_W = BAR_MAX_W * (INTAKE_MG / BAR_REF_LOAD)  # always 1.35 frame units


def calc_plasma_p(gfr, fe, intake=INTAKE_MG):
    """Steady-state plasma phosphate (mg/dL): E = GFR * (0.9 * P_p * 10) * FE."""
    return intake / (gfr * FILTERABLE * fe * 10.0)


def calc_load_w(fe):
    """Bar width in frame units at steady state (5,333.3 mg/day = 9.0 units; 800 mg = 1.35)."""
    return ORANGE_W / max(fe, 0.01)


# ------------------------------------------------------------------ shared world geometry
BAR_RIGHT = 4.10
BAR_Y = 0.0
BAR_H = 1.04
SIEVE_X0 = -6.30
SIEVE_MOUTH_X = -5.00
GUT_POS = np.array([-4.95, 2.55, 0.0])
BONE_POS = np.array([-5.15, -2.02, 0.0])
URINE_POS = np.array([2.95, -1.92, 0.0])
GAUGE_X = 5.45
GAUGE_Y0 = -1.95
GAUGE_Y1 = 2.15
RULE_POS = np.array([-0.40, -3.18, 0.0])


def gauge_y(val):
    return GAUGE_Y0 + (np.clip(val, 0.0, 12.0) / 12.0) * (GAUGE_Y1 - GAUGE_Y0)


def make_chip(text, color, size=24, pad=0.14):
    lab = T(text, size=size, color=color)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=lab.width + 2 * pad,
        height=lab.height + 2 * pad,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=BG,
        fill_opacity=0.92,
    )
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    g.set_z_index(8)
    return g


def make_bone(pos=BONE_POS):
    rect = RoundedRectangle(
        corner_radius=0.18, width=1.95, height=0.84,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.22,
    ).move_to(pos)
    lab = T("bone", size=26, color=TEXT).move_to(rect)
    g = VGroup(rect, lab)
    g.box, g.label = rect, lab
    g.set_z_index(6)
    return g


def make_sieve_mobj(gfr_tracker):
    """Dynamic kidney sieve whose mouth height at x = SIEVE_MOUTH_X is proportional to GFR."""
    max_mouth = 1.92

    def draw():
        gfr = float(np.clip(gfr_tracker.get_value(), 10.0, 200.0))
        half_m = 0.5 * max_mouth * (gfr / 180.0)
        outer_half = 1.05
        wall_t = 0.18
        top_poly = Polygon(
            [SIEVE_X0, outer_half + wall_t, 0],
            [SIEVE_MOUTH_X, half_m + wall_t, 0],
            [SIEVE_MOUTH_X, half_m, 0],
            [SIEVE_X0, outer_half, 0],
            color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.38,
        )
        bot_poly = Polygon(
            [SIEVE_X0, -outer_half - wall_t, 0],
            [SIEVE_MOUTH_X, -half_m - wall_t, 0],
            [SIEVE_MOUTH_X, -half_m, 0],
            [SIEVE_X0, -outer_half, 0],
            color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.38,
        )
        mesh = DashedLine(
            [SIEVE_MOUTH_X, -half_m, 0], [SIEVE_MOUTH_X, half_m, 0],
            color=BLUE, stroke_width=4.0, dash_length=0.09,
        )
        return VGroup(top_poly, bot_poly, mesh)

    return always_redraw(draw)


def make_phosphate_bar(fe_tracker, load_scale_tracker=None):
    """Dynamic horizontal filtered-load bar anchored at BAR_RIGHT with fixed ORANGE 800 mg block."""
    if load_scale_tracker is None:
        load_scale_tracker = ValueTracker(1.0)

    def draw():
        fe = float(np.clip(fe_tracker.get_value(), 0.05, 1.0))
        scale = float(load_scale_tracker.get_value())
        total_w = calc_load_w(fe) * scale
        orange_w = min(ORANGE_W * scale, total_w)
        green_w = max(0.0, total_w - orange_w)

        orange_left = BAR_RIGHT - orange_w
        parts = VGroup()
        if green_w > 0.03:
            g_rect = Rectangle(
                width=green_w, height=BAR_H,
                stroke_color=GREEN, stroke_width=2.5,
                fill_color=GREEN, fill_opacity=0.46,
            ).move_to([orange_left - green_w / 2, BAR_Y, 0])
            parts.add(g_rect)

        o_rect = Rectangle(
            width=orange_w, height=BAR_H,
            stroke_color=ORANGE, stroke_width=3.2,
            fill_color=ORANGE, fill_opacity=0.76,
        ).move_to([BAR_RIGHT - orange_w / 2, BAR_Y, 0])
        parts.add(o_rect)

        border = Rectangle(
            width=total_w, height=BAR_H,
            stroke_color=BLUE, stroke_width=2.5, fill_opacity=0,
        ).move_to([BAR_RIGHT - total_w / 2, BAR_Y, 0])
        parts.add(border)
        return parts

    m = always_redraw(draw)
    m.set_z_index(2)
    return m


def make_gauge(pp_tracker, show_number=True, glow_tracker=None):
    """Vertical WHITE plasma phosphate gauge (0 to 12 mg/dL) with 'healthy' mark at 3.3."""
    spine = Line([GAUGE_X, GAUGE_Y0, 0], [GAUGE_X, GAUGE_Y1, 0], color=TEXT, stroke_width=3.5)
    ticks = VGroup()
    for v in range(0, 13, 2):
        y = gauge_y(v)
        ticks.add(Line([GAUGE_X, y, 0], [GAUGE_X + 0.16, y, 0], color=TEXT, stroke_width=2.5))
        tl = M(f"{v}", size=24, color=TEXT).next_to([GAUGE_X + 0.18, y, 0], RIGHT, buff=0.10)
        tl.set_z_index(8)
        ticks.add(tl)

    hy = gauge_y(3.3)
    h_band = Rectangle(
        width=0.40, height=0.16,
        stroke_width=0, fill_color=GREEN, fill_opacity=0.38,
    ).move_to([GAUGE_X, hy, 0])
    h_line = Line([GAUGE_X - 0.20, hy, 0], [GAUGE_X + 0.20, hy, 0], color=GREEN, stroke_width=2.5)
    # Place 'healthy' safely left of the needle tail (x <= 5.00)
    h_lab = T("healthy", size=22, color=GREEN).move_to([GAUGE_X - 0.90, hy, 0])
    h_lab.set_z_index(8)
    healthy_mark = VGroup(h_band, h_line, h_lab)

    title = T("plasma phosphate\n(mg/dL)", size=24, color=TEXT, line_spacing=0.85)
    title.move_to([5.35, 2.66, 0]).set_z_index(8)

    def draw_needle():
        val = float(pp_tracker.get_value())
        y = gauge_y(val)
        glow = float(glow_tracker.get_value()) if glow_tracker is not None else 0.0
        col = ORANGE if (glow > 0.5 or val > 4.5) else TEXT
        stem = Line([GAUGE_X - 0.34, y, 0], [GAUGE_X - 0.02, y, 0], color=col, stroke_width=5.0)
        tip = Polygon(
            [GAUGE_X, y, 0],
            [GAUGE_X - 0.18, y + 0.10, 0],
            [GAUGE_X - 0.18, y - 0.10, 0],
            color=col, stroke_width=0, fill_color=col, fill_opacity=1.0,
        )
        return VGroup(stem, tip)

    needle = always_redraw(draw_needle)
    needle.set_z_index(7)

    parts = VGroup(spine, ticks, healthy_mark, title, needle)
    readout = None
    if show_number:
        readout = always_redraw(
            lambda: M(f"{pp_tracker.get_value():.1f} mg/dL", size=26, color=TEXT).move_to([GAUGE_X - 0.05, -2.42, 0])
        )
        readout.set_z_index(8)
        parts.add(readout)
    parts.needle = needle
    parts.healthy_mark = healthy_mark
    parts.readout = readout
    parts.title = title
    return parts


def make_particle_stream(gfr_tracker, fe_tracker, seed=7):
    """Physiological particle stream: BLUE filtered packets cross the sieve, (1-FE) loop up as
    GREEN reabsorbed phosphate, FE travel to the ORANGE block and drip to the urine counter."""
    rng = np.random.default_rng(seed)
    n_dots = 46
    dots = VGroup()
    state = []
    for i in range(n_dots):
        d = Dot(radius=0.076, color=BLUE).set_opacity(0.95)
        dots.add(d)
        state.append({
            "phase": float(i) / n_dots,
            "lane": float(rng.uniform(-0.78, 0.78)),
            "reab_u": float(rng.uniform(0.14, 0.88)),
        })
    dots.set_z_index(4)
    dots.layout_ok = True   # particles flow inside the sieve/tubule/drip zone behind labels

    def update(mob, dt):
        gfr = float(np.clip(gfr_tracker.get_value(), 15.0, 180.0))
        fe = float(np.clip(fe_tracker.get_value(), 0.02, 1.0))
        speed = 0.28 + 0.18 * (gfr / 180.0)
        half_m = 0.5 * 1.72 * (gfr / 180.0)
        total_w = min(BAR_MAX_W, calc_load_w(fe))
        green_w = max(0.0, total_w - ORANGE_W)
        orange_left = BAR_RIGHT - ORANGE_W
        green_left = orange_left - green_w

        for d, st in zip(mob, state):
            st["phase"] = (st["phase"] + dt * speed) % 1.0
            p = st["phase"]
            excreted = st["lane"] > (1.0 - 2.0 * fe)
            if p < 0.22:
                u = p / 0.22
                x = SIEVE_X0 + u * (SIEVE_MOUTH_X - SIEVE_X0)
                y = st["lane"] * (0.90 * (1 - u) + half_m * u)
                d.move_to([x, y, 0]).set_color(BLUE).set_opacity(0.95)
            elif not excreted and green_w > 0.2:
                u = (p - 0.22) / 0.78
                if u < 0.56:
                    v = u / 0.56
                    x_end = green_left + st["reab_u"] * green_w
                    x = SIEVE_MOUTH_X + v * (x_end - SIEVE_MOUTH_X)
                    y = st["lane"] * min(half_m, 0.34) * (1 - 0.4 * v)
                    d.move_to([x, y, 0]).set_color(BLUE if x < green_left else GREEN).set_opacity(0.95)
                else:
                    v = (u - 0.56) / 0.44
                    x_reab = green_left + st["reab_u"] * green_w
                    x = x_reab - 0.55 * v
                    y = 0.24 + v * 1.02
                    d.move_to([x, y, 0]).set_color(GREEN).set_opacity(max(0.0, 0.95 * (1.0 - v)))
            else:
                u = (p - 0.22) / 0.78
                if u < 0.68:
                    v = u / 0.68
                    x_end = BAR_RIGHT - 0.35 - 0.45 * abs(st["lane"])
                    x = SIEVE_MOUTH_X + v * (x_end - SIEVE_MOUTH_X)
                    y = st["lane"] * min(half_m, 0.28) * (1 - 0.5 * v)
                    d.move_to([x, y, 0]).set_color(ORANGE if x >= orange_left else BLUE).set_opacity(0.95)
                else:
                    v = (u - 0.68) / 0.32
                    x = 3.42 + 0.18 * st["lane"]
                    y = -0.42 - v * 1.05
                    d.move_to([x, y, 0]).set_color(ORANGE).set_opacity(max(0.0, 0.95 * (1.0 - v)))

    dots.add_updater(update)
    return dots


def build_world(gfr=180.0, fe=0.15, pp=None, with_bone=False, with_rule=False, show_pct=False, show_gauge_num=True):
    """Build the single carried world at the given state."""
    if pp is None:
        pp = calc_plasma_p(gfr, fe)
    gfr_t = ValueTracker(gfr)
    fe_t = ValueTracker(fe)
    pp_t = ValueTracker(pp)
    glow_t = ValueTracker(0.0)

    gut_arrow = Arrow([-6.25, 2.02, 0], [-4.15, 2.02, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.24)
    gut_label = T("from gut: 800 mg/day", size=26, color=TEXT).move_to(GUT_POS).set_z_index(8)

    sieve = make_sieve_mobj(gfr_t)
    sieve_label = T(f"filtration: {gfr:.0f} L/day", size=26, color=TEXT).move_to([-4.90, 1.44, 0]).set_z_index(8)

    tubule_top = Line([SIEVE_MOUTH_X, BAR_H / 2 + 0.04, 0], [BAR_RIGHT, BAR_H / 2 + 0.04, 0], color=GREY, stroke_width=2.5).set_opacity(0.50)
    tubule_bot = Line([SIEVE_MOUTH_X, -BAR_H / 2 - 0.04, 0], [BAR_RIGHT, -BAR_H / 2 - 0.04, 0], color=GREY, stroke_width=2.5).set_opacity(0.50)
    bar = make_phosphate_bar(fe_t)

    urine_label = T("urine: 800 mg/day", size=28, color=ORANGE).move_to(URINE_POS).set_z_index(8)
    gauge = make_gauge(pp_t, show_number=show_gauge_num, glow_tracker=glow_t)
    dots = make_particle_stream(gfr_t, fe_t)

    w = VGroup(gut_arrow, gut_label, tubule_top, tubule_bot, sieve, sieve_label, bar, urine_label, gauge, dots)
    w.gfr_t, w.fe_t, w.pp_t, w.glow_t = gfr_t, fe_t, pp_t, glow_t
    w.gut_arrow, w.gut_label = gut_arrow, gut_label
    w.sieve, w.sieve_label = sieve, sieve_label
    w.tubule = VGroup(tubule_top, tubule_bot)
    w.bar, w.urine_label, w.gauge, w.dots = bar, urine_label, gauge, dots

    if with_bone:
        w.bone = make_bone()
        w.add(w.bone)
    else:
        w.bone = None

    if show_pct:
        pct_txt = "100% out" if fe >= 0.99 else f"{fe * 100:.0f}%"
        w.pct_label = T(pct_txt, size=26, color=ORANGE).move_to([BAR_RIGHT - ORANGE_W / 2, 0.88, 0]).set_z_index(8)
        w.add(w.pct_label)
    else:
        w.pct_label = None

    if with_rule:
        w.bottom_tag = T("in = out: share up, or level up", size=28, color=TEXT).move_to(RULE_POS).set_z_index(8)
        w.add(w.bottom_tag)
    else:
        w.bottom_tag = T("round numbers, steady state", size=24, color=TEXT).move_to(RULE_POS).set_z_index(8)
        w.add(w.bottom_tag)

    return w


def build_split_panel_copy(gfr, fe, title, title_color, x_center, seed=11):
    """Build one compact half-width copy for the s00 healthy-vs-failing comparison without shrinking text."""
    pp = calc_plasma_p(gfr, fe)
    frame = RoundedRectangle(
        corner_radius=0.18, width=6.15, height=5.15,
        stroke_color=title_color, stroke_width=2.5, fill_color=BG, fill_opacity=0.35,
    ).move_to([x_center, -0.25, 0])
    head = T(title, size=26, color=title_color).move_to([x_center, 1.98, 0]).set_z_index(8)

    sx0 = x_center - 2.75
    smx = x_center - 2.05
    half_m = 0.65 * (gfr / 180.0)
    sieve_top = Polygon(
        [sx0, 0.72, 0], [smx, half_m + 0.08, 0], [smx, half_m, 0], [sx0, 0.62, 0],
        color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.38,
    )
    sieve_bot = Polygon(
        [sx0, -0.72, 0], [smx, -half_m - 0.08, 0], [smx, -half_m, 0], [sx0, -0.62, 0],
        color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.38,
    )
    sieve_mesh = DashedLine([smx, -half_m, 0], [smx, half_m, 0], color=BLUE, stroke_width=3.5, dash_length=0.07)
    sieve_lab = T(f"{gfr:.0f} L/day", size=22, color=TEXT).move_to([x_center - 2.15, 1.15, 0]).set_z_index(8)

    bar_scale = 3.15 / 9.0
    bar_r = x_center + 1.25
    ow = ORANGE_W * bar_scale
    tw = calc_load_w(fe) * bar_scale
    gw = max(0.0, tw - ow)

    tub_t = Line([smx, 0.36, 0], [bar_r, 0.36, 0], color=GREY, stroke_width=2).set_opacity(0.50)
    tub_b = Line([smx, -0.36, 0], [bar_r, -0.36, 0], color=GREY, stroke_width=2).set_opacity(0.50)
    bar_grp = VGroup()
    if gw > 0.03:
        bar_grp.add(Rectangle(width=gw, height=0.66, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.46)
                    .move_to([bar_r - ow - gw / 2, 0.0, 0]))
    bar_grp.add(Rectangle(width=ow, height=0.66, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.76)
                .move_to([bar_r - ow / 2, 0.0, 0]))
    bar_grp.add(Rectangle(width=tw, height=0.66, stroke_color=BLUE, stroke_width=2, fill_opacity=0)
                .move_to([bar_r - tw / 2, 0.0, 0]))

    urine_lab = T("urine: 800 mg/day", size=24, color=ORANGE).move_to([x_center - 0.35, -1.65, 0]).set_z_index(8)

    gx = x_center + 2.15
    gy0, gy1 = -1.45, 1.35
    gy = lambda v: gy0 + (np.clip(v, 0.0, 12.0) / 12.0) * (gy1 - gy0)
    g_spine = Line([gx, gy0, 0], [gx, gy1, 0], color=TEXT, stroke_width=3)
    g_ticks = VGroup()
    for v in (0, 4, 8, 12):
        yy = gy(v)
        g_ticks.add(Line([gx, yy, 0], [gx + 0.12, yy, 0], color=TEXT, stroke_width=2))
        g_ticks.add(M(f"{v}", size=22, color=TEXT).next_to([gx + 0.14, yy, 0], RIGHT, buff=0.06))
    hy = gy(3.3)
    h_mark = Line([gx - 0.15, hy, 0], [gx + 0.15, hy, 0], color=GREEN, stroke_width=3)

    ny = gy(pp)
    n_col = ORANGE if pp > 4.5 else TEXT
    needle = VGroup(
        Line([gx - 0.35, ny, 0], [gx - 0.02, ny, 0], color=n_col, stroke_width=4.5),
        Polygon([gx, ny, 0], [gx - 0.16, ny + 0.09, 0], [gx - 0.16, ny - 0.09, 0],
                color=n_col, stroke_width=0, fill_color=n_col, fill_opacity=1.0),
    )
    pp_lab = M(f"{pp:.1f}", size=24, color=n_col).move_to([gx, -2.05, 0]).set_z_index(8)

    rng = np.random.default_rng(seed)
    dots = VGroup()
    dstate = []
    for i in range(24):
        d = Dot(radius=0.060, color=BLUE).set_opacity(0.95)
        dots.add(d)
        dstate.append({
            "phase": i / 24.0,
            "lane": float(rng.uniform(-0.7, 0.7)),
            "reab_u": float(rng.uniform(0.14, 0.88)),
        })
    dots.set_z_index(4)
    dots.layout_ok = True

    def upd(mob, dt):
        sp = 0.28 + 0.16 * (gfr / 180.0)
        green_left = bar_r - ow - gw
        for d, st in zip(mob, dstate):
            st["phase"] = (st["phase"] + dt * sp) % 1.0
            p = st["phase"]
            ex = st["lane"] > (1.0 - 2.0 * fe)
            if p < 0.25:
                u = p / 0.25
                d.move_to([sx0 + u * (smx - sx0), st["lane"] * (0.55 * (1 - u) + half_m * u), 0]).set_color(BLUE).set_opacity(0.95)
            elif not ex and gw > 0.1:
                u = (p - 0.25) / 0.75
                x_reab = green_left + st["reab_u"] * gw
                if u < 0.6:
                    v = u / 0.6
                    x = smx + v * (x_reab - smx)
                    y = st["lane"] * min(half_m, 0.22) * (1 - 0.4 * v)
                    d.move_to([x, y, 0]).set_color(BLUE if x < green_left else GREEN).set_opacity(0.95)
                else:
                    v = (u - 0.6) / 0.4
                    x = x_reab - 0.20 * v
                    y = 0.16 + v * 0.68
                    d.move_to([x, y, 0]).set_color(GREEN).set_opacity(max(0.0, 0.95 * (1.0 - v)))
            else:
                u = (p - 0.25) / 0.75
                if u < 0.68:
                    x = smx + (u / 0.68) * (bar_r - 0.22 - smx)
                    d.move_to([x, st["lane"] * 0.18, 0]).set_color(ORANGE if x >= bar_r - ow else BLUE).set_opacity(0.95)
                else:
                    v = (u - 0.68) / 0.32
                    d.move_to([bar_r - ow / 2 + 0.08 * st["lane"], -0.28 - v * 0.90, 0]).set_color(ORANGE).set_opacity(max(0.0, 0.95 * (1.0 - v)))

    dots.add_updater(upd)

    panel = VGroup(frame, head, sieve_top, sieve_bot, sieve_mesh, sieve_lab, tub_t, tub_b,
                   bar_grp, urine_lab, g_spine, g_ticks, h_mark, needle, pp_lab, dots)
    panel.urine_lab = urine_lab
    panel.needle = needle
    panel.pp_lab = pp_lab
    return panel


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        w = build_world(gfr=180.0, fe=0.15, pp=3.3)
        ca_ghost = VGroup(
            Rectangle(width=8.80, height=BAR_H, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.22)
            .move_to([BAR_RIGHT - 0.18 - 8.80 / 2, BAR_Y, 0]),
            Rectangle(width=0.18, height=BAR_H, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.45)
            .move_to([BAR_RIGHT - 0.09, BAR_Y, 0]),
        )
        ca_tag = T("calcium, last time", size=24, color=BLUE).move_to([-0.40, 1.48, 0]).set_z_index(8)

        # Show calcium flow stream while the narrator recaps the first film (0..8s)
        ca_fe = ValueTracker(0.02)
        ca_dots = make_particle_stream(w.gfr_t, ca_fe, seed=3)
        self.add(w.gut_arrow, w.gut_label, w.tubule, w.sieve, w.sieve_label, w.urine_label, w.gauge, w.bottom_tag, ca_dots)

        self.at("The first film")
        self.play(GrowFromEdge(ca_ghost, LEFT), FadeIn(ca_tag), run_time=1.8)

        self.at("Phosphate passes")
        ca_dots.clear_updaters()
        bar_scale = ValueTracker(0.05)
        grow_bar = make_phosphate_bar(w.fe_t, bar_scale)
        self.add(grow_bar, w.dots)
        self.play(
            FadeOut(ca_ghost), FadeOut(ca_tag), FadeOut(ca_dots),
            bar_scale.animate.set_value(1.0),
            run_time=1.3,
        )
        self.remove(grow_bar)
        self.add(w.bar)

        self.at("a healthy kidney")
        left_copy = build_split_panel_copy(180.0, 0.15, "Healthy (180 L/day)", GREEN, -3.20, seed=11)
        right_copy = build_split_panel_copy(15.0, 1.00, "Badly failing (15 L/day)", ORANGE, 3.20, seed=23)
        w.dots.clear_updaters()
        self.play(
            FadeOut(w),
            FadeIn(left_copy), FadeIn(right_copy),
            run_time=1.0,
        )

        self.at("both excrete 800")
        self.play(
            left_copy.urine_lab.animate.scale(1.16),
            right_copy.urine_lab.animate.scale(1.16),
            rate_func=there_and_back,
            run_time=1.0,
        )

        self.at("So why is blood phosphate high")
        q_top = T("Same output. Why higher phosphate?", size=32, color=TEXT).move_to([0.0, 3.22, 0]).set_z_index(9)
        self.play(
            FadeIn(q_top, shift=DOWN * 0.1),
            Wiggle(right_copy.needle, scale_value=1.18, rotation_angle=0.14),
            run_time=1.3,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        left_copy = build_split_panel_copy(180.0, 0.15, "Healthy (180 L/day)", GREEN, -3.20, seed=11)
        right_copy = build_split_panel_copy(15.0, 1.00, "Badly failing (15 L/day)", ORANGE, 3.20, seed=23)
        q_top = T("Same output. Why higher phosphate?", size=32, color=TEXT).move_to([0.0, 3.22, 0]).set_z_index(9)
        self.add(left_copy, right_copy, q_top)

        w = build_world(gfr=180.0, fe=0.15, pp=3.3)
        title = T("Smaller Filter, Same Phosphate Out", size=36, font=TITLE_FONT, color=TEXT).move_to([-0.85, 3.28, 0]).set_z_index(9)
        fit(title, max_w=9.8)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.10)

        self.play(
            FadeOut(left_copy), FadeOut(right_copy), FadeOut(q_top),
            FadeIn(w),
            run_time=0.75,
        )
        self.play(FadeIn(title, shift=UP * 0.08), GrowFromCenter(rule), run_time=0.6)
        self.finish()


class S02Brake(SpokenScene):
    def construct(self):
        w = build_world(gfr=180.0, fe=0.15, pp=3.3)
        self.add(w)

        pth = make_chip("PTH", PURPLE, size=24).move_to([1.00, 2.05, 0])
        pth_target = np.array([2.25, 1.15, 0.0])

        self.at("PTH throws phosphate out")
        self.play(FadeIn(pth, shift=DOWN * 0.15), run_time=0.45)
        self.play(pth.animate.move_to(pth_target), run_time=0.75)
        pth_link = Line(pth.get_bottom(), [2.75, BAR_H / 2, 0], color=PURPLE, stroke_width=2.5)
        o_pulse = Rectangle(width=ORANGE_W, height=BAR_H, stroke_color=ORANGE, stroke_width=5, fill_opacity=0).move_to([BAR_RIGHT - ORANGE_W / 2, BAR_Y, 0])
        self.play(Create(pth_link), FadeIn(o_pulse), run_time=0.45)
        self.play(FadeOut(o_pulse), run_time=0.4)

        self.at("calcium sets PTH")
        ca_tag = T("set by calcium", size=24, color=PURPLE).move_to([-0.95, 2.05, 0]).set_z_index(8)
        thread = Line(ca_tag.get_right() + RIGHT * 0.08, pth.get_left() + LEFT * 0.06, color=PURPLE, stroke_width=2)
        self.play(FadeIn(ca_tag), Create(thread), run_time=0.9)

        self.at("bone makes")
        bone = make_bone().shift(DOWN * 0.6)
        self.play(bone.animate.shift(UP * 0.6), run_time=0.8)

        self.at("FGF23")
        fgf = make_chip("FGF23", MAGENTA, size=24).move_to(bone.get_center()).scale(0.75)
        self.play(fgf.animate.scale(1.0 / 0.75).move_to([-3.30, -1.65, 0]), run_time=0.9)

        self.at("acts on the kidney")
        klotho_ring = Circle(radius=0.14, color=MAGENTA, stroke_width=4, fill_color=MAGENTA, fill_opacity=0.25).move_to([2.75, -BAR_H / 2 - 0.18, 0])
        klotho_lab = T("Klotho", size=24, color=MAGENTA).move_to([3.42, -1.12, 0]).set_z_index(8)
        fgf_target = np.array([1.75, -1.12, 0.0])
        self.play(fgf.animate.move_to(fgf_target), run_time=1.1)
        fgf_link = Line(fgf.get_right() + RIGHT * 0.04, klotho_ring.get_left() + LEFT * 0.04, color=MAGENTA, stroke_width=2.5)
        self.play(FadeIn(klotho_ring), FadeIn(klotho_lab), Create(fgf_link), run_time=0.7)
        self.finish()


class S03TwoJobs(SpokenScene):
    def construct(self):
        w = build_world(gfr=180.0, fe=0.15, pp=3.3, with_bone=True)
        pth = make_chip("PTH", PURPLE, size=24).move_to([2.25, 1.15, 0])
        pth_link = Line(pth.get_bottom(), [2.75, BAR_H / 2, 0], color=PURPLE, stroke_width=2.5)
        fgf = make_chip("FGF23", MAGENTA, size=24).move_to([1.75, -1.12, 0])
        klotho_ring = Circle(radius=0.14, color=MAGENTA, stroke_width=4, fill_color=MAGENTA, fill_opacity=0.25).move_to([2.75, -BAR_H / 2 - 0.18, 0])
        klotho_lab = T("Klotho", size=24, color=MAGENTA).move_to([3.42, -1.12, 0]).set_z_index(8)
        fgf_link = Line(fgf.get_right() + RIGHT * 0.04, klotho_ring.get_left() + LEFT * 0.04, color=MAGENTA, stroke_width=2.5)
        self.add(w, pth, pth_link, fgf, klotho_ring, klotho_lab, fgf_link)

        self.at("lowers phosphate reabsorption")
        ghost_shift = Rectangle(width=1.0, height=BAR_H, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35).move_to([2.25, BAR_Y, 0])
        both_tag = T("both: less reabsorbed", size=24, color=TEXT).move_to([0.00, 1.18, 0]).set_z_index(8)
        self.play(
            FadeIn(ghost_shift),
            pth.box.animate.set_stroke(width=5),
            fgf.box.animate.set_stroke(width=5),
            FadeIn(both_tag),
            run_time=1.0,
        )
        self.play(
            FadeOut(ghost_shift),
            pth.box.animate.set_stroke(width=2.5),
            fgf.box.animate.set_stroke(width=2.5),
            run_time=1.0,
        )

        self.at("lowers calcitriol")
        calcitriol = make_chip("calcitriol", TAN, size=24).move_to([-2.05, 2.35, 0])
        pth_up = T("PTH: ↑", size=24, color=PURPLE).move_to([0.20, 2.55, 0]).set_z_index(8)
        fgf_dn = T("FGF23: ↓", size=24, color=MAGENTA).move_to([0.20, 2.05, 0]).set_z_index(8)
        self.play(FadeIn(calcitriol), FadeIn(pth_up), FadeIn(fgf_dn), run_time=0.8)
        self.play(calcitriol.animate.shift(DOWN * 0.12).set_opacity(0.48), run_time=0.6)

        self.at("absorbed from the gut")
        less_gut = T("less from gut", size=24, color=TAN).move_to([-2.15, 1.62, 0]).set_z_index(8)
        thin_gut = Arrow([-6.25, 2.02, 0], [-4.15, 2.02, 0], buff=0, color=TAN, stroke_width=2.5, tip_length=0.16)
        self.play(FadeOut(w.gut_arrow), FadeIn(thin_gut), FadeIn(less_gut), run_time=0.55)
        self.wait(0.55)
        self.play(FadeOut(thin_gut), FadeIn(w.gut_arrow), run_time=0.50)
        self.finish()


class S04Arithmetic(SpokenScene):
    def construct(self):
        w = build_world(gfr=180.0, fe=0.15, pp=3.3, with_bone=True)
        fgf_park = make_chip("FGF23", MAGENTA, size=22, pad=0.10).move_to([-3.25, -2.02, 0])
        pth_park = make_chip("PTH", PURPLE, size=22, pad=0.10).move_to([-1.95, -2.02, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])
        self.add(w, fgf_park, pth_park, cal_park)

        t1 = T("urine 800 =", size=26, color=ORANGE)
        t2 = T("filtration", size=26, color=GREY)
        t3 = T("× filterable phosphate", size=26, color=TEXT)
        t4 = T("× fraction out", size=26, color=ORANGE)
        eq_strip = VGroup(t1, t2, t3, t4).arrange(RIGHT, buff=0.14).move_to([-0.65, 3.28, 0]).set_z_index(9)
        fit(eq_strip, max_w=10.6)

        # Pre-laid progressive arithmetic lines above the bar
        l1_a = M("3.3 mg/dL", size=24, color=TEXT)
        l1_b = M("= 33 mg/L", size=24, color=TEXT)
        line1 = VGroup(l1_a, l1_b).arrange(RIGHT, buff=0.16).move_to([0.45, 2.62, 0]).set_z_index(8)

        l2_a = M("0.9 × 33", size=24, color=TEXT)
        l2_b = M("≈ 30 mg/L", size=24, color=TEXT)
        filt_tag = T("(90% filterable)", size=22, color=TEXT)
        line2 = VGroup(l2_a, l2_b, filt_tag).arrange(RIGHT, buff=0.16).move_to([0.45, 2.10, 0]).set_z_index(8)

        l3_a = M("180 L", size=24, color=TEXT)
        l3_b = M("× 30 mg/L", size=24, color=TEXT)
        l3_c = M("× 0.15", size=24, color=ORANGE)
        l3_d = M("≈ 800 mg/day", size=24, color=ORANGE)
        line3 = VGroup(l3_a, l3_b, l3_c, l3_d).arrange(RIGHT, buff=0.14).move_to([0.45, 1.56, 0]).set_z_index(8)

        self.at("Phosphate excreted")
        self.play(FadeIn(t1), run_time=0.6)

        self.at("equals filtration")
        self.play(FadeIn(t2), run_time=0.8)

        self.at("filterable plasma phosphate")
        self.play(FadeIn(t3), run_time=0.9)

        self.at("fraction excreted")
        self.play(FadeIn(t4), run_time=0.8)

        self.at("180 liters")
        self.play(w.sieve_label.animate.scale(1.16), rate_func=there_and_back, run_time=1.0)

        self.at("of 3", lead=0.1)
        self.play(
            FadeIn(l1_a, run_time=0.35),
            w.gauge.healthy_mark.animate(rate_func=there_and_back, run_time=0.9).scale(1.18),
            w.gauge.readout.animate(rate_func=there_and_back, run_time=0.9).scale(1.12),
        )

        self.at("is 33", lead=0.1)
        self.play(FadeIn(l1_b), run_time=0.35)

        self.at("about 90", lead=0.1)
        self.play(FadeIn(l2_a), FadeIn(filt_tag), run_time=0.45)

        self.at("about 30", lead=0.1)
        self.play(FadeIn(l2_b), run_time=0.35)

        self.at("15 of the filtered")
        pct = T("15%", size=26, color=ORANGE).move_to([BAR_RIGHT - ORANGE_W / 2, 0.88, 0]).set_z_index(8)
        o_hl = Rectangle(width=ORANGE_W, height=BAR_H, stroke_color=ORANGE, stroke_width=5, fill_opacity=0).move_to([BAR_RIGHT - ORANGE_W / 2, BAR_Y, 0])
        self.play(FadeIn(pct), FadeIn(o_hl), run_time=0.5)
        self.play(FadeOut(o_hl), run_time=0.4)

        self.at("180 times", lead=0.1)
        self.play(FadeIn(l3_a), run_time=0.25)

        self.at("times 30", lead=0.1)
        self.play(FadeIn(l3_b), run_time=0.25)

        self.at("times 15", lead=0.1)
        self.play(FadeIn(l3_c), run_time=0.25)

        self.at("about 800", lead=0.1)
        self.play(FadeIn(l3_d), run_time=0.30)
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        w = build_world(gfr=180.0, fe=0.15, pp=3.3, with_bone=True, show_pct=True)
        fgf_park = make_chip("FGF23", MAGENTA, size=22, pad=0.10).move_to([-3.25, -2.02, 0])
        pth_park = make_chip("PTH", PURPLE, size=22, pad=0.10).move_to([-1.95, -2.02, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])
        self.add(w, fgf_park, pth_park, cal_park)

        self.at("excrete the phosphate")
        eq_badge = VGroup(
            T("from gut", size=28, color=TEXT),
            T("=", size=28, color=TEXT),
            T("urine", size=28, color=ORANGE),
        ).arrange(RIGHT, buff=0.16).move_to([-0.50, 2.35, 0]).set_z_index(8)
        self.play(FadeIn(eq_badge), run_time=0.35)
        self.play(
            w.gut_label.animate.scale(1.14),
            w.urine_label.animate.scale(1.14),
            rate_func=there_and_back,
            run_time=1.0,
        )
        self.wait(0.6)
        self.play(FadeOut(eq_badge), run_time=0.4)

        self.at("When filtration falls")
        ghost_jaw = VGroup(
            Polygon([SIEVE_X0, 0.96, 0], [SIEVE_MOUTH_X, 0.25, 0], [SIEVE_MOUTH_X, 0.17, 0], [SIEVE_X0, 0.84, 0],
                    color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.28),
            Polygon([SIEVE_X0, -0.96, 0], [SIEVE_MOUTH_X, -0.25, 0], [SIEVE_MOUTH_X, -0.17, 0], [SIEVE_X0, -0.84, 0],
                    color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.28),
        )
        self.play(FadeIn(ghost_jaw), run_time=0.6)
        self.play(FadeOut(ghost_jaw), run_time=0.5)

        self.at("fraction excreted must rise")
        self.play(w.pct_label.animate.scale(1.30), rate_func=there_and_back, run_time=1.0)

        self.at("plasma phosphate rises instead")
        rule_new = T("in = out: share up, or level up", size=28, color=TEXT).move_to(RULE_POS).set_z_index(8)
        self.play(
            w.pp_t.animate.set_value(7.2),
            swap(w.bottom_tag, rule_new, run_time=0.8),
            run_time=1.0,
        )
        w.bottom_tag = rule_new
        self.play(w.pp_t.animate.set_value(3.3), run_time=0.8)
        self.finish()


class S06Moderate(SpokenScene):
    def construct(self):
        w = build_world(gfr=180.0, fe=0.15, pp=3.3, with_bone=True, with_rule=True, show_pct=True)
        fgf_park = make_chip("FGF23", MAGENTA, size=22, pad=0.10).move_to([-3.25, -2.02, 0])
        pth_park = make_chip("PTH", PURPLE, size=22, pad=0.10).move_to([-1.95, -2.02, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])
        self.add(w, fgf_park, pth_park, cal_park)

        self.at("Cut filtration to 60")
        sieve_60 = T("filtration: 60 L/day", size=26, color=TEXT).move_to(w.sieve_label.get_center()).set_z_index(8)
        self.play(
            w.gfr_t.animate.set_value(60.0),
            swap(w.sieve_label, sieve_60, run_time=0.9),
            run_time=1.3,
        )
        w.sieve_label = sieve_60

        self.at("At 15")
        self.play(w.pct_label.animate.scale(1.22), rate_func=there_and_back, run_time=0.7)

        # Pre-laid formula 1 beside the gauge (stacked to stay clear of gut label and gauge title)
        f1_a = T("1/3 filtration → 3× level:", size=24, color=TEXT).move_to([0.25, 2.62, 0]).set_z_index(8)
        f1_b = M("3.3", size=24, color=TEXT)
        f1_c = M("× 3", size=24, color=TEXT)
        f1_d = M("≈ 9.9", size=24, color=ORANGE)
        f1_row2 = VGroup(f1_b, f1_c, f1_d).arrange(RIGHT, buff=0.12).move_to([0.25, 2.12, 0]).set_z_index(8)
        f1 = VGroup(f1_a, f1_b, f1_c, f1_d)

        pp_hi = calc_plasma_p(60.0, 0.15)  # 9.88 -> 9.9
        self.at("must triple", lead=0.1)
        self.play(
            FadeIn(f1_a, run_time=0.4),
            w.pp_t.animate(run_time=1.1, rate_func=linear).set_value(5.5),
        )

        self.at("3", lead=0.1)
        self.play(
            FadeIn(f1_b, run_time=0.25),
            w.pp_t.animate(run_time=0.65, rate_func=linear).set_value(7.5),
        )

        self.at("times 3", lead=0.1)
        self.play(
            FadeIn(f1_c, run_time=0.25),
            w.pp_t.animate(run_time=0.65, rate_func=linear).set_value(8.9),
        )

        self.at("is about 9", lead=0.1)
        self.play(
            FadeIn(f1_d, run_time=0.30),
            w.pp_t.animate(run_time=0.55).set_value(pp_hi),
        )

        self.at("FgF23 and Pth")
        self.play(
            pth_park.animate.move_to([2.40, 1.15, 0]).scale(1.08),
            fgf_park.animate.move_to([1.90, -1.12, 0]).scale(1.08),
            run_time=0.9,
        )

        # Pre-laid formula 2 replacing formula 1 (two stacked lines)
        f2_a = M("800 ÷ (60 × 0.9 × 0.5)", size=24, color=TEXT).move_to([0.25, 2.62, 0]).set_z_index(8)
        f2_b = M("≈ 30 mg/L = 3.0 mg/dL", size=24, color=TEXT).move_to([0.25, 2.12, 0]).set_z_index(8)

        self.at("fraction to 50")
        pct_50 = T("50%", size=26, color=ORANGE).move_to(w.pct_label.get_center()).set_z_index(8)
        pp_lo = calc_plasma_p(60.0, 0.50)  # 2.96 -> 3.0
        self.play(
            w.fe_t.animate.set_value(0.50),
            w.pp_t.animate.set_value(pp_lo),
            swap(w.pct_label, pct_50, run_time=0.7),
            swap(f1, f2_a, run_time=0.6),
            run_time=1.3,
        )
        w.pct_label = pct_50

        self.at("about 3", lead=0.1)
        self.play(FadeIn(f2_b), run_time=0.35)
        self.finish()


class S07Cohort(SpokenScene):
    def construct(self):
        w = build_world(gfr=60.0, fe=0.50, pp=calc_plasma_p(60.0, 0.50), with_bone=True, with_rule=True, show_pct=True)
        pth = make_chip("PTH", PURPLE, size=24, pad=0.10).move_to([2.40, 1.15, 0])
        fgf = make_chip("FGF23", MAGENTA, size=24, pad=0.10).move_to([1.90, -1.12, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])
        self.add(w, pth, fgf, cal_park)

        self.at("raising the fraction")
        self.play(w.pct_label.animate.scale(1.22), rate_func=there_and_back, run_time=0.9)

        self.at("In one large cohort")
        base_y = 1.82
        norm_line = DashedLine([-2.75, base_y + 0.52, 0], [1.45, base_y + 0.52, 0], color=GREY, stroke_width=2)
        b_fgf = Rectangle(width=0.68, height=1.10, stroke_color=MAGENTA, stroke_width=2.5, fill_color=MAGENTA, fill_opacity=0.65).move_to([-2.05, base_y + 1.10 / 2, 0])
        b_p = Rectangle(width=0.68, height=0.52, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.45).move_to([-0.65, base_y + 0.52 / 2, 0])
        b_pth = Rectangle(width=0.68, height=0.52, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE, fill_opacity=0.50).move_to([0.75, base_y + 0.52 / 2, 0])

        l_fgf = T("FGF23", size=22, color=MAGENTA).next_to(b_fgf, DOWN, buff=0.10)
        l_p = T("phosphate", size=22, color=TEXT).next_to(b_p, DOWN, buff=0.10)
        l_pth = T("PTH", size=22, color=PURPLE).next_to(b_pth, DOWN, buff=0.10)
        sch = T("cohort (schematic)", size=22, color=TEXT).move_to([-0.65, 3.22, 0]).set_z_index(8)

        bars = VGroup(norm_line, b_fgf, b_p, b_pth, l_fgf, l_p, l_pth, sch)
        self.play(FadeIn(bars), run_time=0.9)

        self.at("FGF23 was high")
        self.play(b_fgf.animate.set_fill(opacity=0.92), run_time=0.7)

        self.at("phosphate and PTH")
        self.play(
            b_p.animate.set_fill(opacity=0.75),
            b_pth.animate.set_fill(opacity=0.80),
            run_time=0.7,
        )

        self.at("without proving the order")
        order_arr = Arrow([-1.55, 2.72, 0], [-0.55, 2.72, 0], buff=0.05, color=GOLD, stroke_width=3, tip_length=0.18)
        q_first = T("FGF23 first?", size=24, color=GOLD).next_to(order_arr, RIGHT, buff=0.14).set_z_index(8)
        self.play(GrowArrow(order_arr), FadeIn(q_first), run_time=0.55)
        self.wait(0.45)
        self.play(FadeOut(bars), FadeOut(order_arr), run_time=0.55)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        w = build_world(gfr=60.0, fe=0.50, pp=calc_plasma_p(60.0, 0.50), with_bone=True, with_rule=True, show_pct=True)
        fgf_park = make_chip("FGF23", MAGENTA, size=22, pad=0.10).move_to([-3.25, -2.02, 0])
        pth_park = make_chip("PTH", PURPLE, size=22, pad=0.10).move_to([-1.95, -2.02, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])
        self.add(w, fgf_park, pth_park, cal_park)

        self.at("cut filtration to 15")
        sieve_15 = T("filtration: 15 L/day", size=26, color=TEXT).move_to(w.sieve_label.get_center()).set_z_index(8)
        self.play(
            w.gfr_t.animate.set_value(15.0),
            swap(w.sieve_label, sieve_15, run_time=0.9),
            run_time=1.3,
        )
        w.sieve_label = sieve_15

        self.at("excreted every milligram")
        pct_100 = T("100% out", size=26, color=ORANGE).move_to(w.pct_label.get_center()).set_z_index(8)
        self.play(
            w.fe_t.animate.set_value(1.00),
            swap(w.pct_label, pct_100, run_time=0.8),
            run_time=1.6,
        )
        w.pct_label = pct_100

        self.at("Could plasma phosphate stay normal")
        q_mark = T("?", size=42, color=GOLD).move_to([GAUGE_X - 0.58, 0.05, 0]).set_z_index(10)
        q_num = T("? mg/dL", size=26, color=GOLD).move_to(w.gauge.readout.get_center()).set_z_index(9)
        q_card = question_card("Can phosphate stay normal?", y=3.25, color=TEXT, size=32)
        self.play(FadeOut(w.gauge.needle), FadeOut(w.gauge.readout), run_time=0.35)
        self.play(FadeIn(q_num), FadeIn(q_mark), FadeIn(q_card), run_time=0.55)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Can phosphate stay normal?"
    CARD = {"y": 3.25, "color": TEXT, "size": 32}
    RING_AT = (6.20, -3.22, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = build_world(gfr=15.0, fe=1.00, pp=5.9, with_bone=True, with_rule=True, show_pct=True, show_gauge_num=False)
        w.gauge.remove(w.gauge.needle)
        fgf_park = make_chip("FGF23", MAGENTA, size=22, pad=0.10).move_to([-3.25, -2.02, 0])
        pth_park = make_chip("PTH", PURPLE, size=22, pad=0.10).move_to([-1.95, -2.02, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])

        q_mark = T("?", size=42, color=GOLD).move_to([GAUGE_X - 0.58, 0.05, 0]).set_z_index(10)
        q_mark._pt = 0.0
        q_mark.add_updater(lambda m, dt: (setattr(m, "_pt", m._pt + dt), m.set_opacity(0.65 + 0.35 * np.cos(2.4 * m._pt))))
        q_num = T("? mg/dL", size=26, color=GOLD).move_to([GAUGE_X - 0.05, -2.42, 0]).set_z_index(9)
        return VGroup(w, fgf_park, pth_park, cal_park, q_mark, q_num)


class S10Answer(SpokenScene):
    def construct(self):
        w = build_world(gfr=15.0, fe=1.00, pp=3.0, with_bone=True, with_rule=True, show_pct=True, show_gauge_num=False)
        w.gauge.remove(w.gauge.needle)
        fgf_park = make_chip("FGF23", MAGENTA, size=22, pad=0.10).move_to([-3.25, -2.02, 0])
        pth_park = make_chip("PTH", PURPLE, size=22, pad=0.10).move_to([-1.95, -2.02, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])

        q_mark = T("?", size=42, color=GOLD).move_to([GAUGE_X - 0.58, 0.05, 0]).set_z_index(10)
        q_num = T("? mg/dL", size=26, color=GOLD).move_to([GAUGE_X - 0.05, -2.42, 0]).set_z_index(9)
        q_card = question_card("Can phosphate stay normal?", y=3.25, color=TEXT, size=32)
        self.add(w, fgf_park, pth_park, cal_park, q_mark, q_num, q_card)

        self.play(FadeOut(q_card), run_time=0.5)

        self.at("fraction cannot pass")
        stop_line = Line([BAR_RIGHT + 0.05, -0.60, 0], [BAR_RIGHT + 0.05, 0.60, 0], color=RED, stroke_width=5)
        ceil_lab = T("ceiling: 100%", size=24, color=RED).move_to([3.35, 1.38, 0]).set_z_index(8)
        self.play(Create(stop_line), FadeIn(ceil_lab), run_time=0.65)

        # Pre-laid progressive calculation beside the gauge (stacked to stay clear of labels)
        c1_a = M("800", size=24, color=TEXT)
        c1_b = M("÷ (15", size=24, color=TEXT)
        c1_c = M("× 0.9 × 1.0)", size=24, color=TEXT)
        c1_row1 = VGroup(c1_a, c1_b, c1_c).arrange(RIGHT, buff=0.15).move_to([0.15, 2.66, 0]).set_z_index(8)

        c1_d = M("≈ 59 mg/L", size=24, color=TEXT)
        c1_e = M("= 5.9 mg/dL", size=24, color=ORANGE)
        c1_row2 = VGroup(c1_d, c1_e).arrange(RIGHT, buff=0.16).move_to([0.15, 2.16, 0]).set_z_index(8)

        c2_a = M("÷ 0.5", size=24, color=RED)
        c2_b = M("→ 11.9", size=24, color=RED)
        c2_row = VGroup(c2_a, c2_b).arrange(RIGHT, buff=0.15).move_to([0.15, 1.66, 0]).set_z_index(8)

        self.at("800 milligrams", lead=0.1)
        self.play(FadeIn(c1_a), run_time=0.25)

        self.at("divided by 15", lead=0.1)
        self.play(FadeIn(c1_b), run_time=0.25)

        self.at("90", lead=0.1)
        self.play(FadeIn(c1_c), run_time=0.30)

        pp_ans = calc_plasma_p(15.0, 1.00)  # 5.93 -> 5.9
        self.at("about 59", lead=0.1)
        self.play(
            FadeIn(c1_d, run_time=0.30),
            FadeOut(q_mark, run_time=0.35),
            FadeIn(w.gauge.needle, run_time=0.30),
            w.pp_t.animate(run_time=1.8).set_value(4.8),
        )

        self.at("That is 5", lead=0.1)
        real_num = always_redraw(
            lambda: M(f"{w.pp_t.get_value():.1f} mg/dL", size=26, color=TEXT).move_to([GAUGE_X - 0.05, -2.42, 0])
        ).set_z_index(8)
        self.play(
            FadeIn(c1_e, run_time=0.30),
            w.pp_t.animate(run_time=0.55).set_value(pp_ans),
            swap(q_num, real_num, run_time=0.55),
        )

        self.at("50", lead=0.1)
        ghost_green = Rectangle(width=ORANGE_W, height=BAR_H, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.35).move_to([BAR_RIGHT - ORANGE_W - ORANGE_W / 2, BAR_Y, 0])
        ghost_pp = calc_plasma_p(15.0, 0.50)  # 11.85 -> 11.9
        gy_hi = gauge_y(ghost_pp)
        ghost_needle = VGroup(
            Line([GAUGE_X - 0.34, gy_hi, 0], [GAUGE_X - 0.02, gy_hi, 0], color=RED, stroke_width=4),
            Polygon([GAUGE_X, gy_hi, 0], [GAUGE_X - 0.16, gy_hi + 0.09, 0], [GAUGE_X - 0.16, gy_hi - 0.09, 0], color=RED, stroke_width=0, fill_color=RED, fill_opacity=0.9),
        )
        ghost_lab_pre = T("at 50%", size=24, color=RED).move_to([3.45, gy_hi - 0.10, 0]).set_z_index(9)
        self.play(FadeIn(ghost_green), FadeIn(ghost_needle), FadeIn(ghost_lab_pre), run_time=0.65)

        self.at("must double", lead=0.1)
        self.play(FadeIn(c2_a), run_time=0.25)

        self.at("about 11", lead=0.1)
        ghost_lab_full = T("at 50%: 11.9", size=24, color=RED).move_to([3.45, gy_hi - 0.10, 0]).set_z_index(9)
        self.play(
            FadeIn(c2_b, run_time=0.25),
            swap(ghost_lab_pre, ghost_lab_full, run_time=0.35),
        )
        self.wait(0.65)
        self.play(FadeOut(ghost_green), FadeOut(ghost_needle), FadeOut(ghost_lab_full), run_time=0.55)
        self.finish()


class S11Later(SpokenScene):
    def construct(self):
        w = build_world(gfr=15.0, fe=1.00, pp=calc_plasma_p(15.0, 1.00), with_bone=True, with_rule=True, show_pct=True, show_gauge_num=False)
        stop_line = Line([BAR_RIGHT + 0.05, -0.60, 0], [BAR_RIGHT + 0.05, 0.60, 0], color=RED, stroke_width=5)
        ceil_lab = T("ceiling: 100%", size=24, color=RED).move_to([3.35, 1.38, 0]).set_z_index(8)
        fgf_park = make_chip("FGF23", MAGENTA, size=22, pad=0.10).move_to([-3.25, -2.02, 0])
        pth_park = make_chip("PTH", PURPLE, size=22, pad=0.10).move_to([-1.95, -2.02, 0])
        cal_park = make_chip("calcitriol", TAN, size=22, pad=0.10).move_to([-0.45, -2.02, 0])
        hi_lab = T("high & rising", size=24, color=ORANGE).move_to([GAUGE_X - 0.05, -2.42, 0]).set_z_index(8)
        self.add(w, stop_line, ceil_lab, fgf_park, pth_park, cal_park, hi_lab)

        self.at("settles high and climbs")
        self.play(w.pp_t.animate.set_value(7.4), run_time=2.8, rate_func=linear)

        self.at("Calcitriol falls")
        self.play(cal_park.animate.shift(DOWN * 0.16).set_opacity(0.45), run_time=0.8)

        self.at("PTH rises")
        self.play(pth_park.animate.move_to([1.30, 1.15, 0]).scale(1.18), run_time=0.9)

        self.at("usual signature")
        sig_box = RoundedRectangle(corner_radius=0.14, width=5.20, height=0.88, stroke_color=PURPLE, stroke_width=2.5, fill_color=BG, fill_opacity=0.92).move_to([0.20, 2.35, 0])
        sig_txt = T("PTH: calcium ↑, phosphate ↓", size=26, color=PURPLE).move_to(sig_box).set_z_index(8)
        sig_card = VGroup(sig_box, sig_txt)
        self.play(FadeIn(sig_card), run_time=0.8)

        self.at("fails here")
        cross = VGroup(
            Line(sig_box.get_corner(DL) + UR * 0.08, sig_box.get_corner(UR) + DL * 0.08, color=RED, stroke_width=5),
            Line(sig_box.get_corner(UL) + DR * 0.08, sig_box.get_corner(DR) + UL * 0.08, color=RED, stroke_width=5),
        ).set_z_index(10)
        cross.layout_ok = True   # deliberate strike-through over the failed PTH signature card
        self.play(Create(cross), run_time=0.7)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        w = build_world(gfr=180.0, fe=0.15, pp=calc_plasma_p(180.0, 0.15), with_bone=True, with_rule=True, show_pct=True)
        self.add(w)

        self.at("A smaller filter")
        sieve_60 = T("filtration: 60 L/day", size=26, color=TEXT).move_to(w.sieve_label.get_center()).set_z_index(8)
        pct_50 = T("50%", size=26, color=ORANGE).move_to(w.pct_label.get_center()).set_z_index(8)
        self.play(
            w.gfr_t.animate.set_value(60.0),
            w.fe_t.animate.set_value(0.50),
            w.pp_t.animate.set_value(calc_plasma_p(60.0, 0.50)),
            swap(w.sieve_label, sieve_60, run_time=0.7),
            swap(w.pct_label, pct_50, run_time=0.7),
            run_time=1.4,
        )
        w.sieve_label, w.pct_label = sieve_60, pct_50

        self.at("share can grow no more")
        sieve_15 = T("filtration: 15 L/day", size=26, color=TEXT).move_to(w.sieve_label.get_center()).set_z_index(8)
        pct_100 = T("100% out", size=26, color=ORANGE).move_to(w.pct_label.get_center()).set_z_index(8)
        self.play(
            w.gfr_t.animate.set_value(15.0),
            w.fe_t.animate.set_value(1.00),
            w.pp_t.animate.set_value(calc_plasma_p(15.0, 1.00)),
            swap(w.sieve_label, sieve_15, run_time=0.7),
            swap(w.pct_label, pct_100, run_time=0.7),
            run_time=1.4,
        )
        w.sieve_label, w.pct_label = sieve_15, pct_100

        self.at("blood level has to give")
        self.play(
            w.glow_t.animate.set_value(1.0),
            w.bottom_tag.animate.set_color(GOLD).scale(1.08),
            run_time=0.9,
        )
        self.finish()


class S13End(EndCard):
    LINE = "As filtration falls, a larger share must leave, or blood phosphate rises."
