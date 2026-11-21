# ==============================================================================
# COLOUR MAP (one colour per concept for the entire film)
#   BLUE        (#58C4DD) : flow, blood, capillary band, heart
#   GREEN       (#83C167) : oxygen uptake (VO2), uptake bar, oxygen dots
#   ORANGE      (#FF9F43) : oxygen extraction (Fick rectangle height)
#   PURPLE      (#B07DF5) : working thigh muscle and other muscle fibres
#   YELLOW      (#F5D547) : the question and the ceiling
#   RED         (#FC6255) : caution, strike-throughs, "fits, not proven"
#   GREY        (#8B93A1) : axes, inactive icons, schematic reference lines
#   MAGENTA     (#FF5CA8) : lactate (blood lactate gauge, dots, arrows, curve)
#   MAGENTA_LT  (#FFA0CC) : second person's schematic lactate curve
#   TEAL        (#3FB8C0) : glucose made by liver, carbohydrate energy ring
#   LIVER_BROWN (#B67D52) : liver
#   TEXT        (#E8EAF0) : primary text and threshold markers
#
# THE ONE WORLD, CARRIED ACROSS THE FILM:
#   Left edge: GREEN oxygen-uptake bar with YELLOW dashed ceiling line & race-pace level.
#   Left: PURPLE working thigh muscle feeding a horizontal BLUE capillary band with
#   drifting BLUE blood dots and seeping MAGENTA lactate dots.
#   Centre above band: tall vertical MAGENTA 'blood lactate' gauge.
#   Right end of band (from S03 onward): three lactate takers (PURPLE 'other fibres',
#   BLUE 'heart', LIVER_BROWN 'liver' returning TEAL glucose dots).
#   Top-left corner: shrunk Fick rectangle badge. Bottom-right: 'schematic' tag.
#
# WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
#   s00_link_and_question : Fick rectangle highlights flow then shrinks to badge; uptake bar
#                           creeps up, lactate dots seep out and gauge rises via piecewise
#                           pacing tracker; question fades in.
#   s02_three_things      : Uptake bar zooms to centre-left; ceiling, bracketed sustained
#                           fraction, and economy speed dot animate in turn; link line connects to gauge.
#   s03_fuel_not_waste    : Trash icon crossed out; lactate dots stream to newly added takers
#                           (other fibres, heart wink out; liver returns TEAL glucose dots).
#   s04_a_third           : TEAL ring draws and MAGENTA 120-deg sector (exact 1/3) sweeps;
#                           60-min clock hand sweeps 360 deg while lactate stream continues.
#   s05_balance           : Gauge zooms to centre with 'appearance' IN and 'clearance' OUT
#                           arrows; work-rate dial steps 3x and both arrows thicken equally
#                           so gauge level stays flat.
#   s06_predict           : Work-rate dial steps 3x more; IN arrow thickens each step while
#                           OUT arrow caps at peak; gauge stays frozen; top question appears.
#   s08_answer            : Gap bar widens each step; single work-rate tracker drives BOTH
#                           gauge height and computed curve y = lactate_fn(w) on unfolding plot.
#   s09_threshold         : Plot expands to 65% height; tracker sweeps past bend; threshold vlines
#                           mark bends of two computed curves (lactate_fn, lactate_fn2);
#                           4 mmol/L & % ceiling struck.
#   s10_not_oxygen        : Plot shrinks to upper right; O2 inflow sends GREEN dots into muscle,
#                           uptake bar rises further below ceiling, thicker IN arrow tips gauge up.
#   s12_trained           : Two OUT arrows appear under gauge; trained width & dot flux scale to
#                           exact 1.34x untrained via live pct tracker (0 -> +34%) then merge back.
#   s13_close             : IN/OUT arrows rock and settle IN-heavy; GREEN O2 dots enter muscle,
#                           bright MAGENTA stream traces full path to takers, gauge ticks up.
# ==============================================================================

from bp_parts import *

ORANGE = "#FF9F43"
PURPLE = "#B07DF5"
MAGENTA = "#FF5CA8"
MAGENTA_LT = "#FFA0CC"
LIVER_BROWN = "#B67D52"

# Shared physiological curve model (schematic, normalized to [0, 1] x [0, 1])
CLEARANCE_PEAK_W = 0.48
THRESHOLD_W1 = 0.58
THRESHOLD_W2 = 0.74


def lactate_fn(w):
    return 0.14 + 0.10 * w + 0.11 * np.log1p(np.exp((w - THRESHOLD_W1) / 0.07))


def lactate_fn2(w):
    return 0.12 + 0.08 * w + 0.11 * np.log1p(np.exp((w - THRESHOLD_W2) / 0.07))


# ------------------------------------------------------------------ world geometry helpers
BAR_X = -5.55
BAR_W = 0.62
BAR_Y0 = -2.40
BAR_H = 3.30          # track stops right at the YELLOW ceiling line so label sits cleanly above
CEIL_Y = BAR_Y0 + BAR_H

MUSCLE_C = np.array([-3.10, -0.70, 0.0])
BAND_Y = -1.45
BAND_H = 0.66
BAND_X0 = -2.15
BAND_X1_WIDE = 5.45
BAND_X1_TAKERS = 3.10

GAUGE_X = 0.45
GAUGE_Y0 = -0.85
GAUGE_H = 2.85
GAUGE_W = 0.92

TAKERS_X = 3.90
FIBRES_Y = -0.15
HEART_Y = -1.35
LIVER_Y = -2.50


def make_fick_full(center=(-1.2, 0.4, 0)):
    """First film's Fick rectangle: flow (BLUE width) x extraction (ORANGE height) = O2 uptake (GREEN area)."""
    c = np.array(center, dtype=float)
    w, h = 4.2, 2.35
    fill = Rectangle(width=w, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.22).move_to(c)
    left_edge = Line(c + [-w / 2, -h / 2, 0], c + [-w / 2, h / 2, 0], color=ORANGE, stroke_width=7)
    bot_edge = Line(c + [-w / 2, -h / 2, 0], c + [w / 2, -h / 2, 0], color=BLUE, stroke_width=7)
    top_edge = Line(c + [-w / 2, h / 2, 0], c + [w / 2, h / 2, 0], color=GREY, stroke_width=2.5)
    right_edge = Line(c + [w / 2, -h / 2, 0], c + [w / 2, h / 2, 0], color=GREY, stroke_width=2.5)
    area_lbl = T("O2 uptake", 32, GREEN).move_to(c)
    flow_lbl = T("flow", 30, BLUE).next_to(bot_edge, DOWN, buff=0.18)
    extr_lbl = T("extraction", 30, ORANGE).next_to(left_edge, LEFT, buff=0.18)
    box_grp = VGroup(fill, top_edge, right_edge, left_edge, bot_edge)
    lbl_grp = VGroup(area_lbl, flow_lbl, extr_lbl)
    g = VGroup(box_grp, lbl_grp)
    g.box_grp, g.lbl_grp = box_grp, lbl_grp
    g.fill, g.bot_edge, g.left_edge = fill, bot_edge, left_edge
    g.area_lbl, g.flow_lbl, g.extr_lbl = area_lbl, flow_lbl, extr_lbl
    return g


def make_fick_badge(center=(-5.25, 2.85, 0)):
    """Shrunk corner Fick badge kept throughout the film."""
    c = np.array(center, dtype=float)
    w, h = 1.15, 0.56
    rect = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2, fill_color=GREEN, fill_opacity=0.16).move_to(c)
    bot = Line(c + [-w / 2, -h / 2, 0], c + [w / 2, -h / 2, 0], color=BLUE, stroke_width=5)
    left = Line(c + [-w / 2, -h / 2, 0], c + [-w / 2, h / 2, 0], color=ORANGE, stroke_width=5)
    lbl = T("Fick", 22, TEXT).move_to(c)
    box_grp = VGroup(rect, left, bot)
    g = VGroup(box_grp, lbl)
    g.box_grp, g.lbl = box_grp, lbl
    return g


def make_muscle(center=MUSCLE_C, width=1.95, height=2.40):
    """Stylized thigh muscle belly with longitudinal fibres (no molecular detail)."""
    c = np.array(center, dtype=float)
    body = RoundedRectangle(corner_radius=0.55, width=width, height=height,
                            stroke_color=PURPLE, stroke_width=3.8, fill_color=PURPLE, fill_opacity=0.28).move_to(c)
    fibres = VGroup()
    for dx in (-0.45, -0.15, 0.15, 0.45):
        x = c[0] + dx * (width / 1.95)
        y_span = height * 0.34
        fibres.add(Line([x, c[1] - y_span, 0], [x, c[1] + y_span, 0], color=PURPLE, stroke_width=2.4, stroke_opacity=0.65))
    lbl = T("muscle", 26, PURPLE).next_to(body, UP, buff=0.16)
    g = VGroup(body, fibres, lbl)
    g.body, g.fibres, g.lbl = body, fibres, lbl
    return g


def make_uptake_bar(pace_tracker, x=BAR_X, y0=BAR_Y0, h=BAR_H, w=BAR_W,
                    show_pace_lbl=True, show_title=True, show_ceil_lbl=True):
    """Vertical GREEN oxygen-uptake bar with YELLOW dashed ceiling line at its top."""
    ceil_y = y0 + h
    track = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                      fill_color=BG, fill_opacity=0.6).move_to([x, y0 + h / 2, 0])

    def mk_fill():
        frac = float(np.clip(pace_tracker.get_value(), 0.04, 0.98))
        fh = h * frac
        return Rectangle(width=w - 0.06, height=fh, stroke_width=0,
                         fill_color=GREEN, fill_opacity=0.78).move_to([x, y0 + fh / 2 + 0.02, 0])

    fill = always_redraw(mk_fill)
    ceil_line = DashedLine([x - w * 0.85, ceil_y, 0], [x + w * 0.85, ceil_y, 0],
                           color=YELLOW, stroke_width=4, dash_length=0.12)
    g = VGroup(track, fill, ceil_line)
    g.track, g.fill, g.ceil_line = track, fill, ceil_line
    if show_ceil_lbl:
        ceil_lbl = T("ceiling", 24, YELLOW).next_to(ceil_line, UP, buff=0.14)
        g.add(ceil_lbl)
        g.ceil_lbl = ceil_lbl
    if show_title:
        title_lbl = T("O2 uptake", 24, GREEN).next_to(track, DOWN, buff=0.16)
        g.add(title_lbl)
        g.title_lbl = title_lbl
    if show_pace_lbl:
        def mk_pace():
            fy = y0 + h * float(np.clip(pace_tracker.get_value(), 0.04, 0.98))
            tick = Line([x + w / 2, fy, 0], [x + w / 2 + 0.16, fy, 0], color=GREEN, stroke_width=3)
            txt = T("race\npace", 24, GREEN, line_spacing=0.8).next_to(tick, RIGHT, buff=0.06).shift(UP * 0.08)
            return VGroup(tick, txt)
        pace_lbl = always_redraw(mk_pace)
        g.add(pace_lbl)
        g.pace_lbl = pace_lbl
    return g


def make_gauge(lvl_tracker, x=GAUGE_X, y0=GAUGE_Y0, h=GAUGE_H, w=GAUGE_W, label="blood lactate", label_size=28):
    """Vertical blood lactate gauge filled from bottom with MAGENTA."""
    track = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=GREY, stroke_width=3,
                             fill_color=BG, fill_opacity=0.80).move_to([x, y0 + h / 2, 0])

    def mk_fill():
        frac = float(np.clip(lvl_tracker.get_value(), 0.03, 0.96))
        fh = max(0.08, (h - 0.08) * frac)
        return RoundedRectangle(corner_radius=0.08, width=w - 0.10, height=fh, stroke_width=0,
                                fill_color=MAGENTA, fill_opacity=0.84).move_to([x, y0 + 0.04 + fh / 2, 0])

    fill = always_redraw(mk_fill)
    lbl = T(label, label_size, MAGENTA).next_to(track, UP, buff=0.16)
    g = VGroup(track, fill, lbl)
    g.track, g.fill, g.lbl = track, fill, lbl
    return g


def make_band(x0=BAND_X0, x1=BAND_X1_WIDE, y=BAND_Y, h=BAND_H, with_branches=False):
    """Horizontal BLUE capillary band, optionally branching to the 3 takers."""
    rect = Rectangle(width=x1 - x0, height=h, stroke_color=BLUE, stroke_width=2.8,
                     fill_color=BLUE, fill_opacity=0.20).move_to([(x0 + x1) / 2, y, 0])
    g = VGroup(rect)
    g.rect = rect
    if with_branches:
        for ty in (FIBRES_Y, HEART_Y, LIVER_Y):
            br = Line([x1, y, 0], [TAKERS_X - 0.52, ty, 0], color=BLUE, stroke_width=6.5, stroke_opacity=0.50)
            g.add(br)
    return g


def make_heart(center, scale=1.0):
    """Stylized anatomical-feel heart icon in BLUE (two lobes + apex)."""
    c = np.array(center, dtype=float)
    pts = np.array([
        [0.0, -0.38, 0.0], [-0.36, -0.05, 0.0], [-0.42, 0.22, 0.0], [-0.24, 0.38, 0.0],
        [0.0, 0.22, 0.0], [0.24, 0.38, 0.0], [0.42, 0.22, 0.0], [0.36, -0.05, 0.0]
    ]) * scale + c
    return Polygon(*pts, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.22).round_corners(0.12 * scale)


def make_liver(center, scale=1.0):
    """Stylized two-lobe liver wedge in LIVER_BROWN."""
    c = np.array(center, dtype=float)
    pts = np.array([
        [-0.48, -0.22, 0.0], [-0.42, 0.26, 0.0], [0.12, 0.30, 0.0],
        [0.50, 0.16, 0.0], [0.36, -0.14, 0.0], [-0.14, -0.26, 0.0]
    ]) * scale + c
    return Polygon(*pts, color=LIVER_BROWN, stroke_width=3, fill_color=LIVER_BROWN, fill_opacity=0.26).round_corners(0.08 * scale)


def make_takers(x=TAKERS_X):
    """Three lactate takers at right end of band: other fibres, heart, liver."""
    fib_box = RoundedRectangle(corner_radius=0.14, width=1.05, height=0.68,
                               stroke_color=PURPLE, stroke_width=3.5, fill_color=PURPLE, fill_opacity=0.30).move_to([x, FIBRES_Y, 0])
    fib_str = VGroup(*[Line([x - 0.28, FIBRES_Y - 0.16 + i * 0.16, 0], [x + 0.28, FIBRES_Y - 0.16 + i * 0.16, 0],
                            color=PURPLE, stroke_width=2.2, stroke_opacity=0.65) for i in range(3)])
    fib_lbl = T("other fibres", 24, PURPLE).next_to(fib_box, RIGHT, buff=0.16)
    fibres = VGroup(fib_box, fib_str, fib_lbl)
    fibres.shape, fibres.lbl = fib_box, fib_lbl

    heart_shp = make_heart([x, HEART_Y, 0], scale=1.00)
    heart_lbl = T("heart", 24, BLUE).next_to(heart_shp, RIGHT, buff=0.18)
    heart = VGroup(heart_shp, heart_lbl)
    heart.shape, heart.lbl = heart_shp, heart_lbl

    liver_shp = make_liver([x, LIVER_Y, 0], scale=1.02)
    liver_lbl = T("liver", 24, LIVER_BROWN).next_to(liver_shp, RIGHT, buff=0.18)
    liver = VGroup(liver_shp, liver_lbl)
    liver.shape, liver.lbl = liver_shp, liver_lbl

    g = VGroup(fibres, heart, liver)
    g.fibres, g.heart, g.liver = fibres, heart, liver
    return g


def make_trash_icon(center):
    """Small GREY trash can icon for 'not waste'."""
    c = np.array(center, dtype=float)
    can = Polygon(c + [-0.26, 0.26, 0], c + [0.26, 0.26, 0], c + [0.20, -0.32, 0], c + [-0.20, -0.32, 0],
                  color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18)
    lid = Line(c + [-0.32, 0.34, 0], c + [0.32, 0.34, 0], color=GREY, stroke_width=4)
    handle = ArcBetweenPoints(c + [-0.10, 0.34, 0], c + [0.10, 0.34, 0], angle=-PI, color=GREY, stroke_width=3)
    stripes = VGroup(Line(c + [-0.08, 0.16, 0], c + [-0.06, -0.22, 0], color=GREY, stroke_width=2),
                     Line(c + [0.08, 0.16, 0], c + [0.06, -0.22, 0], color=GREY, stroke_width=2))
    return VGroup(can, lid, handle, stripes)


def make_red_cross(target, size=0.95):
    """RED X over target icon."""
    c = target.get_center()
    d = size * 0.45
    x = VGroup(Line(c + [-d, -d, 0], c + [d, d, 0], color=RED, stroke_width=6),
               Line(c + [-d, d, 0], c + [d, -d, 0], color=RED, stroke_width=6))
    x.layout_ok = True
    return x


def make_strike_cross(target):
    """Deliberate RED strike-through X over a rejected '?' tag."""
    w = max(target.width * 0.48, 0.35)
    h = max(target.height * 0.55, 0.25)
    c = target.get_center()
    x = VGroup(Line(c + [-w, -h, 0], c + [w, h, 0], color=RED, stroke_width=5),
               Line(c + [-w, h, 0], c + [w, -h, 0], color=RED, stroke_width=5))
    x.layout_ok = True
    return x


def attach_blood_stream(dots_group, x0=BAND_X0 + 0.1, x1=BAND_X1_WIDE - 0.1, y=BAND_Y, h=BAND_H,
                        n=24, speed=2.1, seed=7, color=BLUE, radius=0.082, opacity=0.88):
    """Populates dots_group with deterministic blood dots drifting along the band."""
    rng = np.random.default_rng(seed)
    for _ in range(n):
        d = Dot([rng.uniform(x0, x1), y + rng.uniform(-h * 0.32, h * 0.32), 0],
                radius=radius, color=color).set_opacity(opacity)
        d._vx = speed * rng.uniform(0.9, 1.1)
        d.layout_ok = True

        def upd(m, dt, a=x0, b=x1):
            m.shift(RIGHT * m._vx * dt)
            if m.get_x() > b:
                m.shift(LEFT * (b - a))
        d.add_updater(upd)
        dots_group.add(d)
    return dots_group


def attach_lactate_stream(dots_group, active_tracker, x0=MUSCLE_C[0] + 0.15, x1=BAND_X1_WIDE - 0.1,
                          y=BAND_Y, n=20, speed=2.25, seed=17, to_takers=False):
    """MAGENTA lactate dots seeping from muscle into band; optionally routed into takers (and TEAL from liver)."""
    rng = np.random.default_rng(seed)
    targets = [FIBRES_Y, HEART_Y, LIVER_Y]
    for i in range(n):
        t_idx = i % 3
        d = Dot([rng.uniform(x0, x1), y + rng.uniform(-0.14, 0.14), 0],
                radius=0.084, color=MAGENTA)
        d._phase = rng.uniform(0.0, 1.0)
        d._ty = targets[t_idx]
        d._is_liver = (t_idx == 2)
        d._off = rng.uniform(-0.10, 0.10)
        d._spd = speed * rng.uniform(0.88, 1.12) / max(x1 - x0, 1.0)
        d.layout_ok = True

        def upd(m, dt, tr=active_tracker, ax0=x0, ax1=x1, by=y, tt=to_takers):
            amt = float(np.clip(tr.get_value(), 0.0, 1.0))
            m._phase = (m._phase + m._spd * dt) % 1.0
            p = m._phase
            if not tt:
                px = ax0 + p * (ax1 - ax0)
                py = MUSCLE_C[1] * (1 - min(p / 0.18, 1.0)) + (by + m._off) * min(p / 0.18, 1.0)
                m.move_to([px, py, 0])
                m.set_color(MAGENTA)
                m.set_opacity(0.92 * amt)
            else:
                if p < 0.12:
                    u = p / 0.12
                    px = ax0 + u * (BAND_X0 + 0.1 - ax0)
                    py = MUSCLE_C[1] * (1 - u) + (by + m._off) * u
                    m.set_color(MAGENTA)
                    m.set_opacity(0.92 * amt)
                elif p < 0.72:
                    u = (p - 0.12) / 0.60
                    px = (BAND_X0 + 0.1) + u * (BAND_X1_TAKERS - (BAND_X0 + 0.1))
                    py = by + m._off
                    m.set_color(MAGENTA)
                    m.set_opacity(0.92 * amt)
                elif p < 0.88:
                    u = (p - 0.72) / 0.16
                    px = BAND_X1_TAKERS + u * (TAKERS_X - 0.15 - BAND_X1_TAKERS)
                    py = (by + m._off) * (1 - u) + m._ty * u
                    m.set_color(MAGENTA)
                    op = (1.0 - 0.75 * max(0.0, u - 0.65) / 0.35) if not m._is_liver else 1.0
                    m.set_opacity(0.92 * amt * op)
                else:
                    u = (p - 0.88) / 0.12
                    if m._is_liver:
                        px = (TAKERS_X - 0.15) - u * 1.15
                        py = m._ty + u * (by - m._ty) * 0.55
                        m.set_color(TEAL)
                        m.set_opacity(0.92 * amt * (1.0 - u * 0.85))
                    else:
                        px = TAKERS_X - 0.1
                        py = m._ty
                        m.set_opacity(0.0)
                m.move_to([px, py, 0])
        d.add_updater(upd)
        dots_group.add(d)
    return dots_group


def make_work_dial(tracker, center=(-5.15, -2.15, 0), radius=0.76, label="work rate"):
    """Schematic half-circle work-rate dial with ticks and needle (no numbers)."""
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=8)
    ticks = VGroup()
    for f in (0.0, 0.25, 0.5, 0.75, 1.0):
        ang = PI - PI * f
        p0 = c + 0.88 * radius * np.array([np.cos(ang), np.sin(ang), 0])
        p1 = c + 1.08 * radius * np.array([np.cos(ang), np.sin(ang), 0])
        ticks.add(Line(p0, p1, color=GREY, stroke_width=2.5))
    v = lambda: float(np.clip(tracker.get_value(), 0.02, 1.0))
    arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI, angle=-PI * v(),
                                    arc_center=c, stroke_color=YELLOW, stroke_width=8))
    needle = always_redraw(lambda: Line(c, c + 0.78 * radius * np.array([np.cos(PI - PI * v()), np.sin(PI - PI * v()), 0]),
                                        color=TEXT, stroke_width=4.5))
    hub = Dot(c, radius=0.06, color=TEXT)
    lbl = T(label, 24, TEXT).move_to(c + DOWN * 0.38)
    return VGroup(track, ticks, arc, needle, hub, lbl)


def make_thick_arrow(p0, p1, rate_tracker, color=MAGENTA, base_h=0.22, tip_w=0.34):
    """Horizontal block arrow whose shaft thickness scales cleanly with rate_tracker."""
    p0 = np.array(p0, dtype=float)
    p1 = np.array(p1, dtype=float)
    direction = 1.0 if p1[0] >= p0[0] else -1.0

    def mk():
        r = max(0.25, float(rate_tracker.get_value()))
        half_h = 0.5 * base_h * r
        head_half_h = half_h + 0.14
        neck_x = p1[0] - direction * tip_w
        pts = [
            [p0[0], p0[1] - half_h, 0],
            [neck_x, p0[1] - half_h, 0],
            [neck_x, p0[1] - head_half_h, 0],
            [p1[0], p1[1], 0],
            [neck_x, p0[1] + head_half_h, 0],
            [neck_x, p0[1] + half_h, 0],
            [p0[0], p0[1] + half_h, 0],
        ]
        return Polygon(*pts, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.82)

    return always_redraw(mk)


def make_static_arrow(p0, p1, rate, color=MAGENTA, base_h=0.36, tip_w=0.34):
    """Static horizontal block arrow for rotation/beam animations."""
    p0 = np.array(p0, dtype=float)
    p1 = np.array(p1, dtype=float)
    direction = 1.0 if p1[0] >= p0[0] else -1.0
    half_h = 0.5 * base_h * max(0.25, float(rate))
    head_half_h = half_h + 0.14
    neck_x = p1[0] - direction * tip_w
    pts = [
        [p0[0], p0[1] - half_h, 0],
        [neck_x, p0[1] - half_h, 0],
        [neck_x, p0[1] - head_half_h, 0],
        [p1[0], p1[1], 0],
        [neck_x, p0[1] + head_half_h, 0],
        [neck_x, p0[1] + half_h, 0],
        [p0[0], p0[1] + half_h, 0],
    ]
    return Polygon(*pts, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.82)


def make_o2_inflow(muscle_c=MUSCLE_C, n=8, seed=29):
    """Short BLUE left inflow into lower muscle with steady GREEN oxygen dots (clear of race-pace label)."""
    left_x = muscle_c[0] - 0.90
    inflow_x0 = left_x - 0.92
    in_y = muscle_c[1] - 0.45   # y = -1.20, comfortably below race-pace label
    ch = Rectangle(width=0.92, height=0.36, stroke_color=BLUE, stroke_width=2.5,
                   fill_color=BLUE, fill_opacity=0.20).move_to([(inflow_x0 + left_x) / 2, in_y, 0])
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for i in range(n):
        d = Dot([inflow_x0 + (i / n) * 1.45, in_y + rng.uniform(-0.09, 0.09), 0],
                radius=0.068, color=GREEN)
        d._phase = i / n
        d._off = rng.uniform(-0.09, 0.09)
        d.layout_ok = True

        def upd(m, dt, x_start=inflow_x0, my=in_y):
            m._phase = (m._phase + 0.65 * dt) % 1.0
            px = x_start + m._phase * 1.50
            m.move_to([px, my + m._off, 0])
            m.set_opacity(0.95 * (1.0 - max(0.0, (m._phase - 0.72) / 0.28)))
        d.add_updater(upd)
        dots.add(d)
    g = VGroup(ch, dots)
    g.channel, g.dots = ch, dots
    return g


# ------------------------------------------------------------------ SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        stag = scope_tag("schematic")
        self.add(stag)

        # Recap: Fick rectangle large in upper-left so shrinking to corner badge never crosses muscle
        fick = make_fick_full(center=(-2.3, 1.35, 0))
        self.play(FadeIn(fick), run_time=0.9)
        # Pulse area gently while explaining first film's ceiling
        self.play(fick.fill.animate.set_fill(opacity=0.38), run_time=1.8)
        self.play(fick.fill.animate.set_fill(opacity=0.22), run_time=1.8)

        self.at("oxygen delivery")
        glow = SurroundingRectangle(fick.bot_edge, color=BLUE, buff=0.06, stroke_width=5)
        self.play(Create(glow), fick.bot_edge.animate.set_stroke(width=11), run_time=0.9)
        self.play(FadeOut(glow), run_time=0.6)

        self.at("no one races")
        badge = make_fick_badge()
        pace_tr = ValueTracker(0.50)
        lac_tr = ValueTracker(0.18)
        lac_flow_tr = ValueTracker(0.18)

        bar = make_uptake_bar(pace_tr)
        muscle = make_muscle()
        band = make_band(x1=BAND_X1_WIDE)
        gauge = make_gauge(lac_tr)
        blood_dots = VGroup()
        lac_dots = VGroup()

        # Transform Fick rectangle directly into corner badge while world fades in (never an empty frame)
        self.play(
            FadeOut(fick.lbl_grp, run_time=0.35),
            ReplacementTransform(fick.box_grp, badge.box_grp, run_time=1.2),
            FadeIn(badge.lbl, run_time=1.2),
            FadeIn(VGroup(bar, muscle, band, gauge), run_time=1.4),
        )
        attach_blood_stream(blood_dots, x1=BAND_X1_WIDE, seed=7)
        attach_lactate_stream(lac_dots, lac_flow_tr, x1=BAND_X1_WIDE, seed=17, to_takers=False)
        self.add(blood_dots, lac_dots)

        self.at("pace rises")
        self.play(
            pace_tr.animate.set_value(0.68),
            lac_flow_tr.animate.set_value(0.90),
            lac_tr.animate(rate_func=rush_into).set_value(0.60),
            run_time=2.8,
        )

        self.at("muscle running out")
        q = T("Is oxygen running out?", 38, YELLOW).move_to([0.3, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.9)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        pace_tr = ValueTracker(0.68)
        lac_tr = ValueTracker(0.60)
        lac_flow_tr = ValueTracker(0.55)

        badge = make_fick_badge()
        bar = make_uptake_bar(pace_tr)
        muscle = make_muscle()
        band = make_band(x1=BAND_X1_WIDE)
        gauge = make_gauge(lac_tr)
        stag = scope_tag("schematic")
        blood_dots = attach_blood_stream(VGroup(), x1=BAND_X1_WIDE, seed=7)
        lac_dots = attach_lactate_stream(VGroup(), lac_flow_tr, x1=BAND_X1_WIDE, seed=17, to_takers=False)
        q = T("Is oxygen running out?", 38, YELLOW).move_to([0.3, 3.05, 0])
        title = T("The Balance Behind the Bend", 44, TEXT, font=TITLE_FONT).move_to([0.4, 3.05, 0])

        self.add(badge, bar, muscle, band, gauge, stag, blood_dots, lac_dots, q)
        self.play(swap(q, title, run_time=0.7))
        self.finish()


class S02ThreeThings(SpokenScene):
    def construct(self):
        pace_tr = ValueTracker(0.68)
        lac_tr = ValueTracker(0.60)
        lac_flow_tr = ValueTracker(0.55)

        badge = make_fick_badge()
        muscle = make_muscle(center=MUSCLE_C)
        band = make_band(x0=-2.75, x1=BAND_X1_WIDE)
        gauge = make_gauge(lac_tr, x=4.65)
        stag = scope_tag("schematic")
        blood_dots = attach_blood_stream(VGroup(), x0=-2.65, x1=BAND_X1_WIDE, seed=7)
        lac_dots = attach_lactate_stream(VGroup(), lac_flow_tr, x0=-3.4, x1=BAND_X1_WIDE, seed=17, to_takers=False)

        bar_left = make_uptake_bar(pace_tr).set_z_index(10)
        bar_left.pace_lbl.clear_updaters()
        bar_left_geom = VGroup(bar_left.track, bar_left.fill, bar_left.ceil_line).set_z_index(10)
        bar_left_lbls = VGroup(bar_left.ceil_lbl, bar_left.title_lbl, bar_left.pace_lbl).set_z_index(10)
        # Zoomed bar sits cleanly at x=-1.4 between dimmed muscle (-3.65) and dimmed gauge (+4.65)
        bar_big = make_uptake_bar(pace_tr, x=-1.45, y0=-2.25, h=4.45, w=0.92,
                                  show_pace_lbl=False, show_title=False, show_ceil_lbl=False).set_z_index(10)

        review_tag = T("Joyner and Coyle, review", 24, GREY).move_to([-4.2, 3.18, 0])
        self.add(badge, bar_left_geom, bar_left_lbls, muscle, band, gauge, stag, blood_dots, lac_dots)
        self.play(
            FadeOut(badge, run_time=1.4),
            muscle.animate(run_time=1.4).shift([-0.55, -0.05, 0]).set_opacity(0.22),
            band.animate(run_time=1.4).set_opacity(0.22),
            gauge.animate(run_time=1.4).set_opacity(0.25),
            blood_dots.animate(run_time=1.4).set_opacity(0.22),
            lac_flow_tr.animate(run_time=1.4).set_value(0.24),
            FadeOut(bar_left_lbls, run_time=0.4),
            ReplacementTransform(bar_left_geom, bar_big, run_time=1.4),
            FadeIn(review_tag, run_time=1.4),
        )

        self.at("the ceiling itself")
        ceil_tag = T("ceiling", 30, YELLOW).next_to(bar_big.ceil_line, RIGHT, buff=0.22)
        self.play(
            bar_big.ceil_line.animate.set_stroke(width=7),
            FadeIn(ceil_tag, shift=RIGHT * 0.1),
            run_time=1.0,
        )

        self.at("the fraction")
        race_y = bar_big.track.get_bottom()[1] + 4.45 * 0.68
        brace_ln = BraceBetweenPoints([-0.82, -2.25, 0], [-0.82, race_y, 0], direction=RIGHT, color=GREEN).set_z_index(10)
        frac_lbl = T("fraction sustained", 28, GREEN).next_to(brace_ln, RIGHT, buff=0.18).set_z_index(10)
        self.play(FadeIn(brace_ln), FadeIn(frac_lbl, shift=RIGHT * 0.1), run_time=1.2)

        self.at("and economy")
        # Placed cleanly BELOW the capillary band (y = -2.25..-3.10) so it never touches band or dots
        cost_chip = chip("O2 cost", GREEN, size=26)
        spd_arr = Arrow(LEFT * 0.85, RIGHT * 0.85, color=TEXT, stroke_width=4, buff=0)
        spd_lbl = T("speed", 24, TEXT).next_to(spd_arr, UP, buff=0.08)
        econ_row = VGroup(cost_chip, VGroup(spd_arr, spd_lbl)).arrange(RIGHT, buff=0.28).move_to([2.6, -2.95, 0])
        econ_lbl = T("oxygen cost per speed", 26, GREEN).next_to(econ_row, UP, buff=0.16)
        spd_dot = Dot(spd_arr.get_start(), radius=0.075, color=GREEN)
        self.play(FadeIn(econ_row), FadeIn(econ_lbl), run_time=1.0)
        self.add(spd_dot)
        self.play(spd_dot.animate(rate_func=linear).move_to(spd_arr.get_end()), run_time=2.4)
        self.remove(spd_dot)

        self.at("that fraction")
        self.play(brace_ln.animate.set_color(YELLOW), run_time=0.8)

        self.at("lactate threshold")
        link = Line(frac_lbl.get_right() + RIGHT * 0.12, gauge.track.get_left() + LEFT * 0.12,
                    color=TEXT, stroke_width=3)
        thresh_lbl = T("lactate threshold", 26, TEXT).move_to([2.45, 0.72, 0])
        self.play(
            gauge.animate.set_opacity(1.0),
            Create(link),
            FadeIn(thresh_lbl),
            run_time=0.8,
        )

        # Slide bar back to left edge and restore full world
        bar_restore = make_uptake_bar(pace_tr)
        bar_restore.pace_lbl.clear_updaters()
        bar_restore_geom = VGroup(bar_restore.track, bar_restore.fill, bar_restore.ceil_line)
        bar_restore_lbls = VGroup(bar_restore.ceil_lbl, bar_restore.title_lbl, bar_restore.pace_lbl)
        gauge_world = make_gauge(lac_tr, x=GAUGE_X)
        muscle_world = make_muscle()
        band_world = make_band(x1=BAND_X1_WIDE)
        self.play(
            FadeOut(VGroup(ceil_tag, brace_ln, frac_lbl, econ_row, econ_lbl, link, thresh_lbl, review_tag), run_time=0.35),
            ReplacementTransform(bar_big, bar_restore_geom, run_time=0.7),
            FadeIn(bar_restore_lbls, rate_func=squish_rate_func(smooth, 0.45, 1.0), run_time=0.7),
            ReplacementTransform(gauge, gauge_world, run_time=0.7),
            ReplacementTransform(muscle, muscle_world, run_time=0.7),
            ReplacementTransform(band, band_world, run_time=0.7),
            blood_dots.animate(run_time=0.7).set_opacity(0.88),
            lac_flow_tr.animate(run_time=0.7).set_value(0.55),
            FadeIn(badge, rate_func=squish_rate_func(smooth, 0.45, 1.0), run_time=0.7),
        )
        self.finish()


class S03FuelNotWaste(SpokenScene):
    def construct(self):
        pace_tr = ValueTracker(0.68)
        lac_tr = ValueTracker(0.60)
        lac_flow_tr = ValueTracker(0.45)

        badge = make_fick_badge()
        bar = make_uptake_bar(pace_tr)
        muscle = make_muscle()
        band = make_band(x1=BAND_X1_WIDE)
        gauge = make_gauge(lac_tr)
        stag = scope_tag("schematic")
        blood_dots = attach_blood_stream(VGroup(), x1=BAND_X1_WIDE, seed=7)
        lac_dots = attach_lactate_stream(VGroup(), lac_flow_tr, x1=BAND_X1_WIDE, seed=17, to_takers=False)
        self.add(badge, bar, muscle, band, gauge, stag, blood_dots, lac_dots)

        self.at("start with lactate")
        self.play(gauge.lbl.animate.set_color(YELLOW), run_time=0.55)
        self.play(gauge.lbl.animate.set_color(MAGENTA), run_time=0.55)

        self.at("not waste")
        trash = make_trash_icon(center=[-3.15, 1.85, 0])
        self.play(FadeIn(trash), run_time=0.4)
        rcross = make_red_cross(trash)
        self.play(Create(rcross), run_time=0.4)
        self.play(FadeOut(trash), FadeOut(rcross), run_time=0.45)

        self.at("some pyruvate")
        self.play(
            muscle.fibres.animate.set_color(MAGENTA),
            lac_flow_tr.animate.set_value(0.95),
            run_time=2.4,
        )
        self.play(muscle.fibres.animate.set_color(PURPLE), run_time=0.7)

        self.at("leaves the fibers")
        band_takers = make_band(x1=BAND_X1_TAKERS, with_branches=True)
        takers = make_takers()
        self.play(ReplacementTransform(band, band_takers), run_time=0.6)
        self.remove(blood_dots, lac_dots)
        blood_dots2 = attach_blood_stream(VGroup(), x1=BAND_X1_TAKERS, seed=7)
        lac_dots2 = attach_lactate_stream(VGroup(), lac_flow_tr, x1=BAND_X1_TAKERS, seed=17, to_takers=True)
        self.add(blood_dots2, lac_dots2)

        self.at("other fibers")
        self.play(FadeIn(takers.fibres), run_time=0.45)

        self.at("the heart")
        self.play(FadeIn(takers.heart), run_time=0.20)

        self.at("burn it")
        f1 = Circle(radius=0.22, color=MAGENTA, stroke_width=3).move_to(takers.fibres.shape.get_center())
        f2 = Circle(radius=0.22, color=MAGENTA, stroke_width=3).move_to(takers.heart.shape.get_center())
        self.play(Create(f1), Create(f2), run_time=0.25)
        self.play(FadeOut(f1), FadeOut(f2), run_time=0.25)

        self.at("the liver")
        self.play(FadeIn(takers.liver), run_time=0.45)
        self.finish()


class S04AThird(SpokenScene):
    def construct(self):
        pace_tr = ValueTracker(0.68)
        lac_tr = ValueTracker(0.60)
        lac_flow_tr = ValueTracker(0.95)

        badge = make_fick_badge()
        bar = make_uptake_bar(pace_tr)
        muscle = make_muscle()
        band = make_band(x1=BAND_X1_TAKERS, with_branches=True)
        gauge = make_gauge(lac_tr)
        takers = make_takers()
        stag = scope_tag("schematic")
        blood_dots = attach_blood_stream(VGroup(), x1=BAND_X1_TAKERS, seed=7)
        lac_dots = attach_lactate_stream(VGroup(), lac_flow_tr, x1=BAND_X1_TAKERS, seed=17, to_takers=True)
        self.add(badge, bar, muscle, band, gauge, takers, stag, blood_dots, lac_dots)

        self.at("tracer study")
        ring_c = np.array([2.55, 1.55, 0.0])
        ring = Annulus(inner_radius=0.66, outer_radius=1.06, color=TEAL, fill_opacity=0.82).move_to(ring_c)
        ring_lbl = T("carbohydrate energy", 26, TEAL).next_to(ring, UP, buff=0.16)
        # Placed cleanly in open upper-left space, well clear of blood lactate gauge
        study_tag = T("6 trained, 6 untrained men", 24, GREY).move_to([-2.3, 2.85, 0])
        self.play(DrawBorderThenFill(ring), FadeIn(ring_lbl), FadeIn(study_tag), run_time=2.0)

        self.at("estimated third")
        sweep = ValueTracker(0.001)
        slice_mob = always_redraw(lambda: AnnularSector(
            inner_radius=0.66, outer_radius=1.06, start_angle=PI / 2,
            angle=-sweep.get_value(), color=MAGENTA, fill_opacity=0.92, arc_center=ring_c
        ))
        self.add(slice_mob)
        self.play(sweep.animate(rate_func=linear).set_value(TAU / 3), run_time=2.4)
        est_lbl = fit_text("from blood lactate\n(estimate)", max_w=2.45, size=24, color=MAGENTA).next_to(ring, RIGHT, buff=0.18).shift(UP * 0.25)
        self.play(FadeIn(est_lbl), run_time=0.45)

        self.at("60 minutes")
        clk_c = np.array([5.05, 1.55, 0.0])
        clk_face = Circle(radius=0.50, color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.85).move_to(clk_c)
        clk_ang = ValueTracker(0.0)
        clk_hand = always_redraw(lambda: Line(
            clk_c,
            clk_c + 0.38 * np.array([np.sin(clk_ang.get_value()), np.cos(clk_ang.get_value()), 0]),
            color=YELLOW, stroke_width=4,
        ))
        clk_lbl = T("60 min at threshold", 24, TEXT).next_to(clk_face, DOWN, buff=0.14)
        if clk_lbl.get_right()[0] > 6.3:
            clk_lbl.align_to([6.25, 0, 0], RIGHT)
        self.play(FadeIn(clk_face), FadeIn(clk_lbl), FadeOut(est_lbl), run_time=0.4)
        self.add(clk_hand)
        self.play(clk_ang.animate(rate_func=linear).set_value(TAU), run_time=1.8)

        self.play(
            FadeOut(VGroup(ring, slice_mob, ring_lbl, study_tag, clk_face, clk_hand, clk_lbl)),
            run_time=0.6,
        )
        self.finish()


def _balance_world(work_val=0.58, app_val=0.84, clr_val=0.84, lac_val=0.35, peak_tag=False):
    """Shared zoomed-balance backdrop used cleanly across S05, S06, S07."""
    lac_tr_c = ValueTracker(lac_val)
    work_tr = ValueTracker(work_val)
    app_tr = ValueTracker(app_val)
    clr_tr = ValueTracker(clr_val)

    muscle = make_muscle(center=[-3.75, -0.75, 0]).set_opacity(0.20)
    band = make_band(x0=-2.85, x1=BAND_X1_TAKERS, with_branches=True).set_opacity(0.20)
    takers = make_takers().set_opacity(0.20)
    stag = scope_tag("schematic")
    blood_dots = attach_blood_stream(VGroup(), x0=-2.75, x1=BAND_X1_TAKERS, seed=7)

    # Gauge starts above the band (y0 = -1.00) so blood dots pass cleanly underneath it
    gauge = make_gauge(lac_tr_c, x=0.0, y0=-1.00, h=3.15, w=1.22, label="blood lactate", label_size=28)
    in_arr = make_thick_arrow([-2.65, 0.55, 0], [-0.72, 0.55, 0], app_tr, color=MAGENTA, base_h=0.52)
    out_arr = make_thick_arrow([0.72, 0.55, 0], [2.65, 0.55, 0], clr_tr, color=MAGENTA, base_h=0.52)
    in_lbl = T("appearance", 28, MAGENTA).move_to([-1.85, 1.32, 0])
    out_lbl = T("clearance", 28, MAGENTA).move_to([1.72, 1.32, 0])
    bal_txt = T("appearance vs clearance", 32, TEXT).move_to([0.0, -2.35, 0])
    dial_mob = make_work_dial(work_tr, center=(-5.15, -2.15, 0), radius=0.76)

    g = VGroup(muscle, band, takers, stag, blood_dots, gauge,
               in_arr, out_arr, in_lbl, out_lbl, bal_txt, dial_mob)
    if peak_tag:
        pk = T("at its peak", 24, TEXT).move_to([1.72, -0.25, 0])
        g.add(pk)
    return g, work_tr, app_tr, clr_tr, in_arr, out_arr


class S05Balance(SpokenScene):
    def construct(self):
        pace_tr = ValueTracker(0.68)
        lac_tr = ValueTracker(0.60)
        lac_flow_tr = ValueTracker(0.95)

        badge = make_fick_badge()
        bar = make_uptake_bar(pace_tr)
        muscle = make_muscle()
        band = make_band(x1=BAND_X1_TAKERS, with_branches=True)
        gauge_small = make_gauge(lac_tr)
        takers = make_takers()
        stag = scope_tag("schematic")
        blood_dots = attach_blood_stream(VGroup(), x1=BAND_X1_TAKERS, seed=7)
        lac_dots = attach_lactate_stream(VGroup(), lac_flow_tr, x1=BAND_X1_TAKERS, seed=17, to_takers=True)
        self.add(badge, bar, muscle, band, gauge_small, takers, stag, blood_dots, lac_dots)

        lac_tr_c = ValueTracker(0.35)
        gauge_big = make_gauge(lac_tr_c, x=0.0, y0=-1.00, h=3.15, w=1.22, label="blood lactate", label_size=28)
        muscle_dim = make_muscle(center=[-3.75, -0.75, 0]).set_opacity(0.20)
        band_dim = make_band(x0=-2.85, x1=BAND_X1_TAKERS, with_branches=True).set_opacity(0.20)
        self.play(
            FadeOut(bar),
            FadeOut(badge),
            FadeOut(lac_dots),
            ReplacementTransform(muscle, muscle_dim),
            ReplacementTransform(band, band_dim),
            takers.animate.set_opacity(0.20),
            ReplacementTransform(gauge_small, gauge_big),
            run_time=1.3,
        )

        self.at("balance of appearance")
        app_tr = ValueTracker(0.42)
        clr_tr = ValueTracker(0.42)
        in_arr = make_thick_arrow([-2.65, 0.55, 0], [-0.72, 0.55, 0], app_tr, color=MAGENTA, base_h=0.52)
        out_arr = make_thick_arrow([0.72, 0.55, 0], [2.65, 0.55, 0], clr_tr, color=MAGENTA, base_h=0.52)
        in_lbl = T("appearance", 28, MAGENTA).move_to([-1.85, 1.32, 0])
        out_lbl = T("clearance", 28, MAGENTA).move_to([1.72, 1.32, 0])
        bal_txt = T("appearance vs clearance", 32, TEXT).move_to([0.0, -2.35, 0])
        self.play(FadeIn(in_arr), FadeIn(out_arr), FadeIn(in_lbl), FadeIn(out_lbl), FadeIn(bal_txt), run_time=1.4)

        self.at("how fast it enters")
        self.play(in_lbl.animate.set_color(YELLOW), run_time=0.55)
        self.play(in_lbl.animate.set_color(MAGENTA), run_time=0.55)

        self.at("how well it is removed")
        self.play(out_lbl.animate.set_color(YELLOW), run_time=0.55)
        self.play(out_lbl.animate.set_color(MAGENTA), run_time=0.55)

        self.at("as work rises")
        work_tr = ValueTracker(0.20)
        dial_mob = make_work_dial(work_tr, center=(-5.15, -2.15, 0), radius=0.76)
        self.play(FadeIn(dial_mob), run_time=0.5)
        for w_val, r_val in ((0.33, 0.56), (0.46, 0.70), (0.58, 0.84)):
            self.play(
                work_tr.animate.set_value(w_val),
                app_tr.animate.set_value(r_val),
                clr_tr.animate.set_value(r_val),
                run_time=0.6,
            )
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        bg, work_tr, app_tr, clr_tr, in_arr, out_arr = _balance_world()
        self.add(bg)

        self.at("step")
        steps = ((0.72, 1.00), (0.86, 1.16), (1.00, 1.32))
        self.play(work_tr.animate.set_value(steps[0][0]), app_tr.animate.set_value(steps[0][1]), run_time=1.2)

        self.at("appearance climbs")
        for w_val, r_val in steps[1:]:
            self.play(work_tr.animate.set_value(w_val), app_tr.animate.set_value(r_val), run_time=1.2)

        self.at("reached its peak")
        pk = T("at its peak", 24, TEXT).move_to([1.72, -0.25, 0])
        self.play(FadeIn(pk), run_time=0.7)

        self.at("what does blood lactate")
        q = T("Clearance flat. Lactate does what?", 34, YELLOW).move_to([0.0, 3.18, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = "Clearance flat. Lactate does what?"
    CARD = {"y": 3.18, "color": YELLOW, "size": 34}
    RING_AT = (5.85, -2.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        bg, _, _, _, in_arr, out_arr = _balance_world(work_val=1.00, app_val=1.32, clr_val=0.84, peak_tag=True)
        pulse(in_arr, base=2.5, amp=1.6, speed=4.0)
        pulse(out_arr, base=2.5, amp=1.6, speed=4.0)
        return bg


class S08Answer(SpokenScene):
    def construct(self):
        # Start directly in split layout after dissolving top question (zero ghost cross-fade)
        w_plot = ValueTracker(0.32)
        lac_linked = ValueTracker(lactate_fn(0.32))
        lac_linked.add_updater(lambda m: m.set_value(lactate_fn(w_plot.get_value())))
        self.add(lac_linked)

        gauge_left = make_gauge(lac_linked, x=-2.25, y0=-1.00, h=3.15, w=0.92, label="blood lactate", label_size=26)
        app_r = ValueTracker(0.84)
        clr_r = ValueTracker(0.84)
        in_left = make_thick_arrow([-4.35, 0.55, 0], [-2.82, 0.55, 0], app_r, color=MAGENTA, base_h=0.45)
        out_left = make_thick_arrow([-1.68, 0.55, 0], [-0.25, 0.55, 0], clr_r, color=MAGENTA, base_h=0.45)
        in_lbl = T("appearance", 24, MAGENTA).move_to([-3.75, 1.25, 0])
        out_lbl = T("clearance", 24, MAGENTA).move_to([-0.85, 1.25, 0])
        dial_left = make_work_dial(w_plot, center=(-5.15, -2.15, 0), radius=0.76)

        # Dimmed band & muscle stay on left only (never behind right-side plot!)
        muscle_bg = make_muscle(center=[-3.75, -0.75, 0]).set_opacity(0.18)
        muscle_bg.remove(muscle_bg.lbl)
        band_bg = make_band(x0=-2.85, x1=-0.15).set_opacity(0.18)
        blood_dots = attach_blood_stream(VGroup(), x0=-2.75, x1=-0.25, seed=7)

        # Shaded MAGENTA gap bar showing appearance - clearance widening below gauge
        def mk_gap():
            g_w = max(0.06, (app_r.get_value() - clr_r.get_value()) * 2.1)
            return Rectangle(width=g_w, height=0.38, stroke_color=MAGENTA, stroke_width=2,
                             fill_color=MAGENTA, fill_opacity=0.48).move_to([-2.25, -2.15, 0])
        gap_bar = always_redraw(mk_gap)
        gap_lbl = T("the gap", 24, MAGENTA).move_to([-2.25, -2.65, 0])

        P = Plot(box=(0.70, 5.75, -1.45, 2.15), xr=(0, 1), yr=(0, 1.0),
                 xlabel="work rate", ylabel="blood lactate", color=GREY, label_size=26)
        curve = P.live_curve(lactate_fn, w_plot, color=MAGENTA, width=6)
        dot = P.dot(lambda: w_plot.get_value(), lambda: lactate_fn(w_plot.get_value()), color=MAGENTA, ring=TEXT, radius=0.10)
        stag = scope_tag("schematic")

        q = T("Clearance flat. Lactate does what?", 34, YELLOW).move_to([0.0, 3.18, 0])
        self.add(muscle_bg, band_bg, blood_dots, stag, gauge_left, in_left, out_left,
                 in_lbl, out_lbl, dial_left, gap_bar, gap_lbl, P, curve, dot, q)
        self.play(FadeOut(q), run_time=0.45)

        self.at("appearance outpaces")
        self.play(
            w_plot.animate(rate_func=linear).set_value(0.96),
            app_r.animate(rate_func=linear).set_value(1.42),
            run_time=3.6,
        )

        self.at("trained men")
        study_tag = T("trained men, one study", 24, GREY).move_to([4.0, 2.88, 0])
        self.play(FadeIn(study_tag), run_time=0.6)

        self.at("peak below the threshold")
        pk_pt = P.pt(CLEARANCE_PEAK_W, 0)
        pk_tick = Line(pk_pt + DOWN * 0.08, pk_pt + UP * 0.16, color=TEXT, stroke_width=4)
        # Placed cleanly above the flat curve with a short pointer arrow so zero text overlaps curve or xlabel
        pk_lbl = T("clearance peak", 24, TEXT).move_to([pk_pt[0] - 0.65, 0.15, 0])
        pk_arr = Arrow(pk_lbl.get_bottom() + DOWN * 0.06, [pk_pt[0], -1.25, 0],
                       color=TEXT, stroke_width=2.5, buff=0, tip_length=0.16)
        self.play(FadeIn(pk_tick), FadeIn(pk_lbl), Create(pk_arr), run_time=0.8)

        self.at("does not prove")
        caution = T("fits, not proven", 26, RED).move_to([2.65, 1.35, 0])
        self.play(FadeIn(caution), run_time=0.8)
        self.finish()


class S09Threshold(SpokenScene):
    def construct(self):
        # Plot expands to ~65% height; gauge shrinks beside it, driven by single tracker
        w_tr = ValueTracker(0.40)
        lac_tr = ValueTracker(lactate_fn(0.40))
        lac_tr.add_updater(lambda m: m.set_value(lactate_fn(w_tr.get_value())))
        self.add(lac_tr)

        gauge = make_gauge(lac_tr, x=-4.85, y0=-1.65, h=2.95, w=0.78, label="blood lactate", label_size=24)
        P = Plot(box=(-2.3, 5.2, -1.95, 2.35), xr=(0, 1), yr=(0, 1.0),
                 xlabel="work rate", ylabel="blood lactate", color=GREY, label_size=26)
        c1 = P.curve(lactate_fn, color=MAGENTA, width=6)
        d1 = P.dot(lambda: w_tr.get_value(), lambda: lactate_fn(w_tr.get_value()), color=MAGENTA, ring=TEXT, radius=0.10)
        stag = scope_tag("schematic")
        self.add(gauge, P, c1, d1, stag)

        self.at("lactate threshold")
        v1_line = DashedLine(P.pt(THRESHOLD_W1, 0), P.pt(THRESHOLD_W1, 1.0), color=TEXT, stroke_width=3, dash_length=0.14)
        v1_lbl = T("lactate threshold", 26, TEXT).next_to(P.pt(THRESHOLD_W1, 1.0), UP, buff=0.14)
        self.play(Create(v1_line), FadeIn(v1_lbl), run_time=0.9)

        self.at("the workload")
        self.play(w_tr.animate(rate_func=linear).set_value(0.96), run_time=3.5)

        self.at("no universal value")
        w2 = ValueTracker(0.0)
        c2 = P.live_curve(lactate_fn2, w2, color=MAGENTA_LT, width=5)
        self.add(c2)
        self.play(w2.animate(rate_func=linear).set_value(0.96), run_time=1.5)
        v2_line = DashedLine(P.pt(THRESHOLD_W2, 0), P.pt(THRESHOLD_W2, 1.0), color=TEXT, stroke_width=3, dash_length=0.14)
        self.play(Create(v2_line), run_time=0.5)

        self.at("four millimoles")
        h_ref = DashedLine(P.pt(0, 0.44), P.pt(1, 0.44), color=GREY, stroke_width=3, dash_length=0.14)
        h_lbl = T("4 mmol/L?", 26, TEXT).next_to(P.pt(0.02, 0.44), UP, buff=0.10).align_to(P.pt(0.02, 0.44), LEFT)
        self.play(Create(h_ref), FadeIn(h_lbl), run_time=0.6)
        x_mmol = make_strike_cross(h_lbl)
        self.play(Create(x_mmol), run_time=0.35)

        self.at("share of the ceiling")
        # Wide open empty space inside upper-left of plot, clear of curves and 4 mmol/L?
        pct_lbl = T("% of ceiling?", 26, YELLOW).move_to([-0.25, 1.45, 0])
        self.play(FadeIn(pct_lbl), run_time=0.35)
        x_pct = make_strike_cross(pct_lbl)
        self.play(Create(x_pct), run_time=0.35)
        self.finish()


class S10NotOxygen(SpokenScene):
    def construct(self):
        pace_tr = ValueTracker(0.68)
        lac_tr = ValueTracker(0.72)
        lac_flow_tr = ValueTracker(0.95)
        app_tr = ValueTracker(1.25)
        clr_tr = ValueTracker(0.75)

        badge = make_fick_badge()
        bar = make_uptake_bar(pace_tr)
        muscle = make_muscle()
        band = make_band(x1=BAND_X1_TAKERS, with_branches=True)
        gauge = make_gauge(lac_tr, x=-0.35, y0=-0.88, h=2.55, w=0.78, label="blood lactate", label_size=26)
        in_arr = make_thick_arrow([-2.05, 0.40, 0], [-0.85, 0.40, 0], app_tr, color=MAGENTA, base_h=0.36)
        out_arr = make_thick_arrow([0.15, 0.40, 0], [1.35, 0.40, 0], clr_tr, color=MAGENTA, base_h=0.36)
        takers = make_takers()
        P_sm = Plot(box=(2.05, 5.75, 0.85, 2.75), xr=(0, 1), yr=(0, 1.0),
                    xlabel="work rate", color=GREY, label_size=24)
        c_sm = P_sm.curve(lactate_fn, color=MAGENTA, width=4)
        v_sm = DashedLine(P_sm.pt(THRESHOLD_W1, 0), P_sm.pt(THRESHOLD_W1, 1.0), color=TEXT, stroke_width=2.5, dash_length=0.10)
        d_sm = P_sm.dot(lambda: 0.82, lambda: lactate_fn(0.82), color=MAGENTA, ring=TEXT, radius=0.08)

        stag = scope_tag("schematic")
        blood_dots = attach_blood_stream(VGroup(), x1=BAND_X1_TAKERS, seed=7)
        lac_dots = attach_lactate_stream(VGroup(), lac_flow_tr, x1=BAND_X1_TAKERS, seed=17, to_takers=True)
        self.add(badge, bar, muscle, band, gauge, in_arr, out_arr, takers, P_sm, c_sm, v_sm, d_sm, stag, blood_dots, lac_dots)

        self.at("oxygen runs out")
        q = T("Is oxygen running out?", 32, YELLOW).move_to([0.3, 3.15, 0])
        no_ans = T("No", 36, RED, weight=BOLD).next_to(q, RIGHT, buff=0.35)
        self.play(FadeIn(q), run_time=0.45)
        self.play(FadeIn(no_ans, scale=1.1), run_time=0.45)

        self.at("above the threshold")
        self.play(FadeOut(q), FadeOut(no_ans), run_time=0.45)

        self.at("consuming oxygen")
        inflow = make_o2_inflow()
        self.play(FadeIn(inflow.channel), run_time=0.5)
        self.add(inflow.dots)
        self.play(pace_tr.animate.set_value(0.82), run_time=1.8)

        self.at("still cleared")
        f1 = Circle(radius=0.22, color=MAGENTA, stroke_width=3).move_to(takers.fibres.shape.get_center())
        f2 = Circle(radius=0.22, color=MAGENTA, stroke_width=3).move_to(takers.heart.shape.get_center())
        self.play(Create(f1), Create(f2), run_time=0.4)
        self.play(FadeOut(f1), FadeOut(f2), run_time=0.4)

        self.at("balance has tipped")
        self.play(lac_tr.animate.set_value(0.90), run_time=1.2)
        self.finish()


class S12Trained(SpokenScene):
    def construct(self):
        # Clean focus on gauge + two side-by-side OUT arrows underneath (zero background clutter)
        lac_tr = ValueTracker(0.72)
        stag = scope_tag("schematic")
        gauge = make_gauge(lac_tr, x=0.0, y0=0.45, h=2.35, w=0.90, label="blood lactate", label_size=28)
        single_out = make_thick_arrow([0.55, 1.55, 0], [2.25, 1.55, 0], ValueTracker(0.80), color=MAGENTA, base_h=0.45)
        self.add(stag, gauge, single_out)

        self.at("compared trained")
        un_r = ValueTracker(1.0)
        tr_r = ValueTracker(1.0)
        pct_tr = ValueTracker(0.0)

        arr_un = make_thick_arrow([-3.65, -0.75, 0], [-1.35, -0.75, 0], un_r, color=MAGENTA, base_h=0.56)
        arr_tr = make_thick_arrow([1.35, -0.75, 0], [3.65, -0.75, 0], tr_r, color=MAGENTA, base_h=0.56)
        lbl_un = T("untrained", 28, TEXT).move_to([-2.50, 0.05, 0])
        lbl_tr = T("trained", 28, TEXT).move_to([2.50, 0.05, 0])

        # Lactate dots flowing through both OUT arrows (trained speed scales with tr_r)
        flow_dots = VGroup()
        for side, x_start, r_tr in ((-1, -3.55, un_r), (1, 1.45, tr_r)):
            for k in range(4):
                d = Dot([x_start + k * 0.48, -0.75, 0], radius=0.06, color=TEXT).set_opacity(0.85)
                d._p = k / 4.0
                d.layout_ok = True

                def upd(m, dt, xs=x_start, rt=r_tr):
                    m._p = (m._p + 0.55 * rt.get_value() * dt) % 1.0
                    m.move_to([xs + m._p * 1.90, -0.75, 0])
                d.add_updater(upd)
                flow_dots.add(d)

        self.play(FadeOut(single_out), FadeIn(VGroup(arr_un, arr_tr, lbl_un, lbl_tr)), run_time=0.8)
        self.add(flow_dots)

        self.at("own threshold")
        tag_un = T("at own threshold", 24, GREY).move_to([-2.50, -1.65, 0])
        tag_tr = T("at own threshold", 24, GREY).move_to([2.50, -1.65, 0])
        self.play(FadeIn(tag_un), FadeIn(tag_tr), run_time=0.6)

        self.at("clearance was")
        pct_lbl = counter("+{:.0f}%", pct_tr, at=[4.65, -0.75, 0], size=34, color=YELLOW)
        self.add(pct_lbl)
        self.play(
            tr_r.animate.set_value(1.34),
            pct_tr.animate.set_value(34.0),
            run_time=1.8,
        )

        self.at("an association")
        assoc = T("groups compared, not caused", 26, RED).move_to([0.0, -2.55, 0])
        self.play(FadeIn(assoc), run_time=0.6)
        self.wait(0.8)

        single_back = make_thick_arrow([0.55, 1.55, 0], [2.25, 1.55, 0], ValueTracker(0.85), color=MAGENTA, base_h=0.45)
        self.remove(flow_dots)
        self.play(
            FadeOut(VGroup(tag_un, tag_tr, pct_lbl, assoc, lbl_un, lbl_tr)),
            ReplacementTransform(VGroup(arr_un, arr_tr), single_back),
            run_time=0.7,
        )
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        pace_tr = ValueTracker(0.82)
        lac_tr = ValueTracker(0.72)
        lac_flow_tr = ValueTracker(0.95)

        badge = make_fick_badge()
        bar = make_uptake_bar(pace_tr)
        muscle = make_muscle()
        inflow = make_o2_inflow()
        band = make_band(x1=BAND_X1_TAKERS, with_branches=True)
        gauge = make_gauge(lac_tr, x=-0.35, y0=-0.88, h=2.55, w=0.78, label="blood lactate", label_size=26)
        beam_in = make_static_arrow([-2.05, 0.40, 0], [-0.85, 0.40, 0], 1.25, color=MAGENTA, base_h=0.36)
        beam_out = make_static_arrow([0.15, 0.40, 0], [1.35, 0.40, 0], 0.75, color=MAGENTA, base_h=0.36)
        takers = make_takers()

        P_sm = Plot(box=(2.05, 5.75, 0.85, 2.75), xr=(0, 1), yr=(0, 1.0),
                    xlabel="work rate", color=GREY, label_size=24)
        c_sm = P_sm.curve(lactate_fn, color=MAGENTA, width=4)
        v_sm = DashedLine(P_sm.pt(THRESHOLD_W1, 0), P_sm.pt(THRESHOLD_W1, 1.0), color=TEXT, stroke_width=2.5, dash_length=0.10)
        d_sm = P_sm.dot(lambda: 0.82, lambda: lactate_fn(0.82), color=MAGENTA, ring=TEXT, radius=0.08)

        stag = scope_tag("schematic")
        blood_dots = attach_blood_stream(VGroup(), x1=BAND_X1_TAKERS, seed=7)
        lac_dots = attach_lactate_stream(VGroup(), lac_flow_tr, x1=BAND_X1_TAKERS, seed=17, to_takers=True)
        self.add(badge, bar, muscle, inflow, band, gauge, beam_in, beam_out, takers,
                 P_sm, c_sm, v_sm, d_sm, stag, blood_dots, lac_dots)

        self.at("balanced tipping")
        pivot = np.array([-0.35, 0.40, 0.0])
        self.play(
            Rotate(beam_in, angle=-0.16, about_point=pivot),
            Rotate(beam_out, angle=-0.16, about_point=pivot),
            run_time=0.7,
        )
        self.play(
            Rotate(beam_in, angle=0.34, about_point=pivot),
            Rotate(beam_out, angle=0.34, about_point=pivot),
            run_time=0.8,
        )

        self.at("keeps flowing")
        p_main = VMobject(stroke_color=MAGENTA, stroke_width=7).set_points_as_corners(
            [[-2.25, BAND_Y, 0], [BAND_X1_TAKERS, BAND_Y, 0], [TAKERS_X - 0.35, HEART_Y, 0]]
        )
        p_top = Line([BAND_X1_TAKERS, BAND_Y, 0], [TAKERS_X - 0.35, FIBRES_Y, 0], color=MAGENTA, stroke_width=6)
        p_bot = Line([BAND_X1_TAKERS, BAND_Y, 0], [TAKERS_X - 0.35, LIVER_Y, 0], color=MAGENTA, stroke_width=6)
        p_main.layout_ok = True
        p_top.layout_ok = True
        p_bot.layout_ok = True
        self.play(Create(p_main), Create(p_top), Create(p_bot), run_time=1.8)
        self.play(FadeOut(VGroup(p_main, p_top, p_bot)), run_time=0.8)

        self.at("arrives faster")
        self.play(beam_in.animate.scale(1.14), run_time=0.5)
        self.play(beam_in.animate.scale(1 / 1.14), beam_out.animate.scale(1.08), run_time=0.5)
        self.play(beam_out.animate.scale(1 / 1.08), lac_tr.animate.set_value(0.90), run_time=0.9)
        self.finish()


class S14End(EndCard):
    LINE = "Lactate builds when appearance outruns clearance, not when oxygen runs out."
