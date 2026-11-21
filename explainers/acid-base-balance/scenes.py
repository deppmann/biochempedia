"""
One Ratio, Two Keepers — Acid-Base Balance (16 scenes)

COLOUR MAP (one colour per concept, same in every scene):
  BLUE   (#58C4DD) : bicarbonate (HCO3-, the base) — upper tank fluid, dots, filtered/reclaimed base
  ORANGE (#FF8C3B) : dissolved carbon dioxide (CO2, the acid) — lower tank fluid, bubbles
  RED    (#FC6255) : added acid / free hydrogen ions (H+) — rain, burst dots, acid tray
  WHITE  (#E8EAF0) : pH gauge, needle, fraction bar, ratio, equation
  PINK   (#F47BA0) : lungs and lung tube
  PURPLE (#B482E8) : kidney, kidney tube, and proximal tubule
  TEAL   (#3FB8C0) : phosphate carriers (s13)
  GOLD   (#D4A843) : glutamine and ammonium tokens (s13)

THE ONE WORLD (carried from scene to scene):
  Centre: two 50 mmol/L tanks on a shared vertical scale (upper BLUE bicarbonate, thick WHITE fraction bar,
          lower ORANGE dissolved CO2), fluid heights always proportional to concentration.
  Left:   PINK lungs beside the lower tank joined by a tube; PURPLE kidney beside the upper tank joined by a tube.
  Right:  vertical pH gauge (6.0 to 7.6, bright tick at 7.40) whose WHITE needle is ALWAYS computed from
          pH = 6.1 + log10([HCO3-] / [CO2]).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s00_hook        : RED acid dots fall under gravity into the upper tank; ORANGE bubbles drift out through
                    breathing lungs; needle trembles around computed pH 7.40; free H+ counter shows 40 nmol/L.
  s02_fraction    : Fraction bar brightens, needle pulses at 7.40, BLUE/ORANGE fluids highlight with
                    24 mmol/L and 1.2 mmol/L as spoken, 20 : 1 appears on the split bar, and reaction line
                    CO2 + H2O -> H2CO3 -> H+ + HCO3- builds term by term beside the lower tank.
  s03_equation    : Equation under the gauge builds pH = 6.1 + log(ratio), tags 6.1 as pK: acid = base with
                    gauge tick flash, then transforms to 6.1 + 1.30 -> 7.40 as needle glows.
  s04_double      : bicarb and co2 ValueTrackers animate 24/1.2 -> 48/2.4 -> 24/1.2 -> 12/1.2 -> 24/1.2,
                    driving fluid heights, ratio (20:1 -> 10:1 -> 20:1), computed needle (7.40 -> 7.10 -> 7.40),
                    and equation 6.1 + log 10 = 6.1 + 1 = 7.1 builds under the gauge as spoken.
  s05_sealed      : 'best here' band lights at 6.1, pK 6.1 tick and 1.3-below bracket appear; lid and lung clamp
                    close; RED acid burst converts BLUE dots into ORANGE bubbles that sink, driving bicarb 24->19,
                    co2 1.2->6.2 with stepped label (1.2..6.2), and computed needle 7.40->6.59.
  s06_predict     : Sealed state holds with jostling ORANGE bubbles, breathing lungs behind clamp, and trembling
                    low needle while 'closed: poor buffer' and the predict question appear.
  s08_open        : Rewinds to 24/1.2 (7.40), lid/clamp open, lungs brighten; RED burst reacts into ORANGE bubbles
                    that exit through breathing lungs so co2 stays on 1.2 line while bicarb drops 24->19 and needle dips to 7.30.
  s09_twentyfold  : Gauge slides right; two bars grow in exact 55 : 2.6 proportion (open vs sealed buffering)
                    with 'all bicarbonate buffers' / 'tiny CO2 pool limits' tags and bracket 'about ×20'.
  s10_idea        : Bars fade, gauge returns; fraction bar and named terms highlight; lungs/tube pulse with ticking
                    stopwatch 'minutes'; kidney/tube brighten and pulse with calendar 'days'.
  s11_not_removal : RED dots gather into bottom tray ('sulfuric acid' / 'still in the body') while ORANGE leaves lungs
                    and trapped RED cannot exit via lungs; dashed 24 line marks 'spent' bicarbonate gap; kidney pulses.
  s12_reclaim     : Kidney morphs into U-shaped tubule with pale cell wall; BLUE stream circulates around the U-loop
                    and returns to blood; 4,000 : 50 (80:1) bars grow; highlighted BLUE dot vanishes as fresh BLUE
                    appears, and tally '−1 tubule, +1 blood = net 0' appears beside the tubule.
  s13_make_new    : Enlarged wall cell splits H2CO3 into H+ ('to urine') and HCO3- ('to blood'), then shrinks back;
                    RED dots stream into urine droplet on TEAL phosphate and GOLD ammonium from glutamine while BLUE
                    dots drop into tank, closing 'spent' gap (19->24) and returning needle to 7.40.
  s14_close       : Full world at 24/1.2, 20:1, steady 7.40; RED rain resumes; lungs breathe ORANGE out ('minutes');
                    tubule excretes RED to urine and returns BLUE to tank ('days').
"""
from bp_parts import *

# ------------------------------------------------------------------ Palette
BICARB_COL = BLUE
CO2_COL = "#FF8C3B"
ACID_COL = RED
GAUGE_COL = TEXT
LUNG_COL = "#F47BA0"
KIDNEY_COL = "#B482E8"
PHOS_COL = TEAL
AMM_COL = GOLD

# ------------------------------------------------------------------ Shared Geometry
TANK_X = 0.0
TANK_W = 2.75
TANK_H = 2.10
MAX_MMOL = 50.0
UPPER_BOT = 0.26
UPPER_TOP = UPPER_BOT + TANK_H     # 2.36
LOWER_TOP = -0.26
LOWER_BOT = LOWER_TOP - TANK_H     # -2.36
FRAC_Y = 0.0
FRAC_X0 = -1.62
FRAC_X1 = 1.62

GAUGE_X0 = 5.05
GAUGE_BOT = -2.36
GAUGE_TOP = 2.36
PH_MIN, PH_MAX = 6.0, 7.6

LUNG_POS = np.array([-3.85, -1.32, 0.0])
KIDNEY_POS = np.array([-3.85, 1.32, 0.0])


def compute_ph(bicarb, co2):
    return 6.1 + np.log10(max(bicarb, 0.05) / max(co2, 0.05))


def ph_to_y(ph):
    frac = np.clip((ph - PH_MIN) / (PH_MAX - PH_MIN), 0.0, 1.0)
    return GAUGE_BOT + frac * (GAUGE_TOP - GAUGE_BOT)


def conc_to_h(mmol):
    return np.clip(mmol / MAX_MMOL, 0.0, 1.0) * TANK_H


def make_plasma_tag():
    return scope_tag("human plasma, 37 C", size=24, color=TEXT)


def make_tank_frame(bot, top, color=TEXT):
    """Tank outline made from Lines so layout_check never flags tubes/dots as 'outside' a panel."""
    x0, x1 = TANK_X - TANK_W / 2, TANK_X + TANK_W / 2
    return VGroup(
        Line([x0, bot, 0], [x0, top, 0], color=color, stroke_width=3.8),
        Line([x0, top, 0], [x1, top, 0], color=color, stroke_width=3.8),
        Line([x1, top, 0], [x1, bot, 0], color=color, stroke_width=3.8),
        Line([x1, bot, 0], [x0, bot, 0], color=color, stroke_width=3.8),
    )


def make_lungs(dim=True):
    """Symmetric pair of PINK lung lobes + airway stem."""
    op = 0.48 if dim else 0.82
    st_op = 0.62 if dim else 1.0
    lobe_pts_l = [[-0.09, 0.70, 0], [-0.66, 0.61, 0], [-0.86, -0.18, 0], [-0.79, -0.79, 0], [-0.09, -0.70, 0]]
    lobe_pts_r = [[0.09, 0.70, 0], [0.66, 0.61, 0], [0.86, -0.18, 0], [0.79, -0.79, 0], [0.09, -0.70, 0]]
    left = Polygon(*lobe_pts_l, color=LUNG_COL, stroke_width=4.0, stroke_opacity=st_op,
                   fill_color=LUNG_COL, fill_opacity=op).round_corners(0.26)
    right = Polygon(*lobe_pts_r, color=LUNG_COL, stroke_width=4.0, stroke_opacity=st_op,
                    fill_color=LUNG_COL, fill_opacity=op).round_corners(0.26)
    stem = VGroup(
        Line([0, 0.88, 0], [0, 0.30, 0], color=LUNG_COL, stroke_width=4.5, stroke_opacity=st_op),
        Line([0, 0.30, 0], [-0.34, 0.07, 0], color=LUNG_COL, stroke_width=4.0, stroke_opacity=st_op),
        Line([0, 0.30, 0], [0.34, 0.07, 0], color=LUNG_COL, stroke_width=4.0, stroke_opacity=st_op),
    )
    return VGroup(left, right, stem).move_to(LUNG_POS)


def make_kidney(dim=True):
    """Bean-shaped PURPLE kidney silhouette."""
    op = 0.48 if dim else 0.82
    st_op = 0.62 if dim else 1.0
    pts = [
        [-0.18, 0.84, 0], [-0.68, 0.64, 0], [-0.78, 0.0, 0],
        [-0.68, -0.64, 0], [-0.18, -0.84, 0], [0.32, -0.64, 0],
        [0.16, -0.18, 0], [0.16, 0.18, 0], [0.32, 0.64, 0],
    ]
    body = Polygon(*pts, color=KIDNEY_COL, stroke_width=4.0, stroke_opacity=st_op,
                   fill_color=KIDNEY_COL, fill_opacity=op).round_corners(0.30)
    return body.move_to(KIDNEY_POS)


def make_tube(x0, x1, y, color, dim=True, half_gap=0.12):
    st_op = 0.55 if dim else 1.0
    return VGroup(
        Line([x0, y + half_gap, 0], [x1, y + half_gap, 0], color=color, stroke_width=3.2, stroke_opacity=st_op),
        Line([x0, y - half_gap, 0], [x1, y - half_gap, 0], color=color, stroke_width=3.2, stroke_opacity=st_op),
    )


def set_organ_brightness(organ, tube, color, bright=True):
    op = 0.78 if bright else 0.40
    st = 1.0 if bright else 0.52
    for m in organ.family_members_with_points():
        if isinstance(m, Polygon):
            m.set_fill(color, opacity=op).set_stroke(color, opacity=st)
        else:
            m.set_stroke(color, opacity=st)
    for ln in tube:
        ln.set_stroke(color, opacity=st)


def start_breathing(lungs, period=3.6, phase=0.0):
    lungs._bt = phase
    lungs._base_h = lungs.height

    def upd(mob, dt):
        mob._bt += dt
        s = 1.0 + 0.105 * np.sin(TAU * mob._bt / period)
        mob.set_height(mob._base_h * s)
    lungs.add_updater(upd)


def make_dot_swarm(n, x0, x1, y_bot, y_top_fn, color, seed=7, radius=0.058, speed=0.48, jitter_y=0.32):
    """Computed random-drift dots trapped inside [x0, x1] x [y_bot, y_top_fn()]."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    pad_x = radius + 0.06
    pad_y = radius + 0.015
    for _ in range(n):
        y_lo = y_bot + pad_y
        y_hi = max(y_lo + 0.01, y_top_fn() - pad_y)
        x = rng.uniform(x0 + pad_x, x1 - pad_x)
        y = rng.uniform(y_lo, y_hi)
        d = Dot([x, y, 0], radius=radius, color=color, fill_opacity=0.92)
        d._vx = rng.uniform(0.35 * speed, speed) * (1 if rng.random() > 0.5 else -1)
        d._vy = rng.uniform(-jitter_y, jitter_y)
        d.layout_ok = True
        dots.add(d)

    def upd(mob, dt):
        top_lim = y_top_fn() - pad_y
        bot_lim = y_bot + pad_y
        if top_lim <= bot_lim:
            mid = (y_top_fn() + y_bot) / 2
            for d in mob:
                nx = d.get_center()[0] + d._vx * dt
                if nx < x0 + pad_x or nx > x1 - pad_x:
                    d._vx *= -1
                    nx = np.clip(nx, x0 + pad_x, x1 - pad_x)
                d.move_to([nx, mid, 0])
            return
        for d in mob:
            c = d.get_center()
            nx = c[0] + d._vx * dt
            ny = c[1] + d._vy * dt
            if nx < x0 + pad_x or nx > x1 - pad_x:
                d._vx *= -1
                nx = np.clip(nx, x0 + pad_x, x1 - pad_x)
            if ny < bot_lim or ny > top_lim:
                d._vy *= -1
                ny = np.clip(ny, bot_lim, top_lim)
            d.move_to([nx, ny, 0])
    dots.add_updater(upd)
    return dots


def make_lung_bubbles(n, x_start, x_end, y_mid, seed=11, opacity=0.75, speed=0.80):
    """ORANGE bubbles drifting from the lower tank through the lung tube."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        t_frac = i / max(n, 1)
        x = x_start + t_frac * (x_end - x_start)
        y = y_mid + rng.uniform(-0.04, 0.04)
        b = Circle(radius=0.052, color=CO2_COL, stroke_width=2.5, fill_color=CO2_COL, fill_opacity=opacity * 0.85)
        b.set_stroke(CO2_COL, opacity=opacity)
        b.move_to([x, y, 0])
        b._y0 = y
        b._ph = rng.uniform(0, TAU)
        b.layout_ok = True
        g.add(b)
    g._active = True
    g._speed = speed

    def upd(mob, dt):
        if not mob._active:
            return
        for b in mob:
            c = b.get_center()
            nx = c[0] - mob._speed * dt
            if nx < x_end:
                nx = x_start
            ny = b._y0 + 0.03 * np.sin(3.5 * nx + b._ph)
            b.move_to([nx, ny, 0])
    g.add_updater(upd)
    return g


def make_gauge(bicarb_t, co2_t, gauge_x_t, tremble_amp_t=None):
    """Tall vertical pH gauge (6.0 to 7.6) whose WHITE needle is always computed from bicarb_t and co2_t."""
    gx = lambda: gauge_x_t.get_value()

    def build_static():
        x = gx()
        spine = Line([x, GAUGE_BOT, 0], [x, GAUGE_TOP, 0], color=GAUGE_COL, stroke_width=3.8)
        ticks = VGroup()
        labels = VGroup()
        for k in range(9):
            v = 6.0 + 0.2 * k
            y = ph_to_y(v)
            is_74 = abs(v - 7.4) < 1e-3
            tlen = 0.20 if is_74 else 0.13
            sw = 4.5 if is_74 else 2.6
            col = WHITE if is_74 else TEXT
            ticks.add(Line([x, y, 0], [x + tlen, y, 0], color=col, stroke_width=sw))
            txt = M(f"{v:.2f}" if is_74 else f"{v:.1f}", 22, col)
            txt.move_to([x + 0.34 + txt.width / 2, y, 0])
            labels.add(txt)
        head = T("pH", 30, WHITE).move_to([x, GAUGE_TOP + 0.36, 0])
        return VGroup(spine, ticks, labels, head)

    static_part = always_redraw(build_static)

    tremble_t = ValueTracker(0.0)
    if tremble_amp_t is not None:
        tremble_t.add_updater(lambda m, dt: m.increment_value(dt))

    def build_needle():
        x = gx()
        ph = compute_ph(bicarb_t.get_value(), co2_t.get_value())
        if tremble_amp_t is not None:
            ph += tremble_amp_t.get_value() * np.sin(5.5 * tremble_t.get_value())
        y = ph_to_y(ph)
        tri = Polygon(
            [x - 0.04, y, 0],
            [x - 0.38, y + 0.12, 0],
            [x - 0.38, y - 0.12, 0],
            color=WHITE, fill_color=WHITE, fill_opacity=1.0, stroke_width=1.5,
        )
        bar = Line([x - 0.54, y, 0], [x - 0.04, y, 0], color=WHITE, stroke_width=4.2)
        return VGroup(bar, tri)

    needle = always_redraw(build_needle)
    g = VGroup(static_part, needle)
    g._tremble = tremble_t
    return g


def make_stopwatch(center, color=LUNG_COL):
    """Stopwatch icon with a continuously ticking second hand."""
    c = np.array(center, dtype=float)
    r = 0.34
    ring = Circle(radius=r, color=color, stroke_width=3.6).move_to(c)
    crown = Line(c + UP * r, c + UP * (r + 0.11), color=color, stroke_width=4.2)
    cap = Line(c + UP * (r + 0.11) + LEFT * 0.10, c + UP * (r + 0.11) + RIGHT * 0.10, color=color, stroke_width=3.6)
    t_trk = ValueTracker(0.0)
    t_trk.add_updater(lambda m, dt: m.increment_value(dt))
    hand = always_redraw(lambda: Line(
        c,
        c + 0.74 * r * np.array([np.sin(2.4 * t_trk.get_value()), np.cos(2.4 * t_trk.get_value()), 0]),
        color=WHITE, stroke_width=3.2,
    ))
    g = VGroup(ring, crown, cap, hand)
    g._trk = t_trk
    return g


def make_calendar(center, color=KIDNEY_COL):
    """Calendar icon."""
    c = np.array(center, dtype=float)
    box = RoundedRectangle(corner_radius=0.06, width=0.62, height=0.58, color=color, stroke_width=3.2,
                           fill_color=BG, fill_opacity=0.8).move_to(c)
    bar = Line(c + [-0.31, 0.12, 0], c + [0.31, 0.12, 0], color=color, stroke_width=3.2)
    ring1 = Line(c + [-0.15, 0.22, 0], c + [-0.15, 0.36, 0], color=color, stroke_width=3.6)
    ring2 = Line(c + [0.15, 0.22, 0], c + [0.15, 0.36, 0], color=color, stroke_width=3.6)
    dots = VGroup(*[
        Dot(c + [-0.15 + 0.15 * ix, -0.02 - 0.13 * iy, 0], radius=0.034, color=TEXT)
        for ix in range(3) for iy in range(2)
    ])
    return VGroup(box, bar, ring1, ring2, dots)


def make_split_frac_bar():
    """Split fraction bar leaving a clean central gap for '20 : 1' so no line crosses the letters."""
    return VGroup(
        Line([FRAC_X0, FRAC_Y, 0], [-0.88, FRAC_Y, 0], color=WHITE, stroke_width=7.5),
        Line([0.88, FRAC_Y, 0], [FRAC_X1, FRAC_Y, 0], color=WHITE, stroke_width=7.5),
    )


def make_world(bicarb=24.0, co2=1.2, lungs_dim=True, kidney_dim=True, gauge_x=GAUGE_X0,
               tremble=0.0, show_ratio=False, seed=7):
    """Build the carried world cleanly with shared ValueTrackers."""
    bicarb_t = ValueTracker(bicarb)
    co2_t = ValueTracker(co2)
    gauge_x_t = ValueTracker(gauge_x)
    tremble_t = ValueTracker(tremble)

    upper_fluid = always_redraw(lambda: Rectangle(
        width=TANK_W - 0.04,
        height=max(0.02, conc_to_h(bicarb_t.get_value())),
        stroke_width=0, fill_color=BICARB_COL, fill_opacity=0.48,
    ).move_to([TANK_X, UPPER_BOT + max(0.02, conc_to_h(bicarb_t.get_value())) / 2, 0]))

    lower_fluid = always_redraw(lambda: Rectangle(
        width=TANK_W - 0.04,
        height=max(0.04, conc_to_h(co2_t.get_value())),
        stroke_width=2.0, stroke_color=CO2_COL, fill_color=CO2_COL, fill_opacity=0.49,
    ).move_to([TANK_X, LOWER_BOT + max(0.04, conc_to_h(co2_t.get_value())) / 2, 0]))

    upper_dots = make_dot_swarm(
        30, TANK_X - TANK_W / 2 + 0.08, TANK_X + TANK_W / 2 - 0.08,
        UPPER_BOT, lambda: UPPER_BOT + conc_to_h(bicarb_t.get_value()),
        BICARB_COL, seed=seed, radius=0.072, speed=0.68, jitter_y=0.42,
    )
    lower_bubbles = make_dot_swarm(
        16, TANK_X - TANK_W / 2 + 0.08, TANK_X + TANK_W / 2 - 0.08,
        LOWER_BOT, lambda: LOWER_BOT + max(0.11, conc_to_h(co2_t.get_value())),
        CO2_COL, seed=seed + 3, radius=0.042, speed=0.72, jitter_y=0.14,
    )

    upper_frame = make_tank_frame(UPPER_BOT, UPPER_TOP)
    lower_frame = make_tank_frame(LOWER_BOT, LOWER_TOP)
    frac_bar = make_split_frac_bar() if show_ratio else Line([FRAC_X0, FRAC_Y, 0], [FRAC_X1, FRAC_Y, 0], color=WHITE, stroke_width=7.5)

    bicarb_lbl = T("bicarbonate", 28, BICARB_COL).move_to([TANK_X, UPPER_TOP + 0.42, 0])
    co2_lbl = T("dissolved CO2", 28, CO2_COL).move_to([TANK_X, LOWER_BOT - 0.30, 0])

    lungs = make_lungs(dim=lungs_dim)
    lung_tube = make_tube(-3.10, -TANK_W / 2, -1.32, LUNG_COL, dim=lungs_dim)
    start_breathing(lungs, period=3.6)

    kidney = make_kidney(dim=kidney_dim)
    kidney_tube = make_tube(-3.55, -TANK_W / 2, 1.32, KIDNEY_COL, dim=kidney_dim)

    lung_bubbles = make_lung_bubbles(8, -TANK_W / 2 - 0.06, -3.12, -1.32, seed=seed + 5,
                                     opacity=0.92 if not lungs_dim else 0.72,
                                     speed=1.05 if not lungs_dim else 0.78)

    gauge = make_gauge(bicarb_t, co2_t, gauge_x_t, tremble_amp_t=tremble_t)
    ratio_lbl = M("20 : 1", 34, WHITE).move_to([0, FRAC_Y, 0])

    world = VGroup(
        upper_fluid, lower_fluid, upper_dots, lower_bubbles,
        lung_bubbles, lung_tube, lungs, kidney_tube, kidney,
        upper_frame, lower_frame, frac_bar,
        bicarb_lbl, co2_lbl, gauge,
    )
    if show_ratio:
        world.add(ratio_lbl)

    class W:
        pass
    w = W()
    w.group = world
    w.bicarb = bicarb_t
    w.co2 = co2_t
    w.gauge_x = gauge_x_t
    w.tremble = tremble_t
    w.upper_fluid = upper_fluid
    w.lower_fluid = lower_fluid
    w.upper_dots = upper_dots
    w.lower_bubbles = lower_bubbles
    w.upper_frame = upper_frame
    w.lower_frame = lower_frame
    w.frac_bar = frac_bar
    w.bicarb_lbl = bicarb_lbl
    w.co2_lbl = co2_lbl
    w.lungs = lungs
    w.lung_tube = lung_tube
    w.lung_bubbles = lung_bubbles
    w.kidney = kidney
    w.kidney_tube = kidney_tube
    w.gauge = gauge
    w.ratio_lbl = ratio_lbl
    return w


def make_acid_rain(x0=-1.10, x1=1.10, y_start=UPPER_TOP - 0.08, y_end=0.85, n=16, speed=1.65, seed=19):
    """RED dots raining slowly into the upper tank."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        x = rng.uniform(x0, x1)
        y = y_end + (i / n) * (y_start - y_end)
        d = Dot([x, y, 0], radius=0.062, color=ACID_COL, fill_opacity=0.95)
        d._x0 = x
        d._vy = speed * rng.uniform(0.85, 1.15)
        d.layout_ok = True
        g.add(d)
    g._active = True

    def upd(mob, dt):
        for d in mob:
            c = d.get_center()
            ny = c[1] - d._vy * dt
            if ny < y_end:
                if mob._active:
                    ny = y_start
                    d.set_opacity(0.95)
                else:
                    d.set_opacity(0.0)
                    continue
            d.move_to([d._x0, ny, 0])
    g.add_updater(upd)
    return g


def make_lid_and_clamp():
    """Glass lid over the upper tank + clamp on the lung tube."""
    lid = RoundedRectangle(corner_radius=0.05, width=TANK_W + 0.22, height=0.14,
                           color=TEXT, stroke_width=3.0, fill_color=TEXT, fill_opacity=0.25)
    lid.move_to([TANK_X, UPPER_TOP + 0.07, 0])
    clamp = VGroup(
        Line([-2.28, -1.06, 0], [-2.28, -1.58, 0], color=GOLD, stroke_width=6.5),
        Line([-2.16, -1.06, 0], [-2.16, -1.58, 0], color=GOLD, stroke_width=6.5),
    )
    return lid, clamp


def make_sealed_state(tremble=0.014):
    """Shared sealed state (bicarb=19, co2=6.2, lid on, clamp closed) for s06_predict and s07_pause."""
    w = make_world(bicarb=19.0, co2=6.2, lungs_dim=True, kidney_dim=True, tremble=tremble, seed=21)
    w.lung_bubbles._active = False
    w.lung_bubbles.set_opacity(0.0)
    lid, clamp = make_lid_and_clamp()
    closed_lbl = T("closed: poor buffer", 24, WHITE).move_to([3.12, 1.98, 0])
    ptr = Line([1.56, 2.34, 0], [2.10, 2.12, 0], color=WHITE, stroke_width=2.5)
    plasma_tag = make_plasma_tag()
    return w, lid, clamp, VGroup(closed_lbl, ptr), plasma_tag


def make_tubule_group(open_exit=False):
    """Simple U-shaped PURPLE schematic tubule beside the upper tank with pale cells along the blood-facing wall."""
    # Bend outer reaches x ~ -4.94, leaving x <= -5.2 free for icons/labels
    top_outer = Line([-1.95, 2.04, 0], [-4.20, 2.04, 0], color=KIDNEY_COL, stroke_width=3.4)
    top_inner = Line([-1.95, 1.72, 0], [-4.05, 1.72, 0], color=KIDNEY_COL, stroke_width=3.4)
    if open_exit:
        bend_outer = Arc(radius=0.74, start_angle=PI / 2, angle=0.692 * PI,
                         arc_center=[-4.20, 1.30, 0], color=KIDNEY_COL, stroke_width=3.4)
    else:
        bend_outer = ArcBetweenPoints([-4.20, 2.04, 0], [-4.20, 0.56, 0], angle=PI, color=KIDNEY_COL, stroke_width=3.4)
    bend_inner = ArcBetweenPoints([-4.05, 1.72, 0], [-4.05, 0.88, 0], angle=PI, color=KIDNEY_COL, stroke_width=3.4)
    bot_inner = Line([-4.05, 0.88, 0], [-2.58, 0.88, 0], color=KIDNEY_COL, stroke_width=3.4)
    bot_outer = Line([-4.20, 0.56, 0], [-2.58, 0.56, 0], color=KIDNEY_COL, stroke_width=3.4)
    # Row of pale cells between tubule (x=-2.50) and tank/blood (x=-1.33)
    cells = VGroup()
    for cy in [0.74, 1.04, 1.34, 1.64]:
        cell = RoundedRectangle(corner_radius=0.05, width=0.36, height=0.24,
                                color=KIDNEY_COL, stroke_width=2.2, fill_color=KIDNEY_COL, fill_opacity=0.28)
        cell.move_to([-2.28, cy, 0])
        cells.add(cell)
    blood_lbl = T("blood", 24, TEXT).move_to([-1.96, 0.34, 0])
    g = VGroup(top_outer, top_inner, bend_outer, bend_inner, bot_inner, bot_outer, cells, blood_lbl)
    g.bend_outer = bend_outer
    g.cells = cells
    g.blood_lbl = blood_lbl
    return g


def tubule_u_point(s):
    """Parametric point along the U-tubule lumen centerline for s in [0, 1]."""
    if s < 0.36:
        u = s / 0.36
        return np.array([-1.35 + u * (-4.05 - (-1.35)), 1.88, 0.0])
    elif s < 0.64:
        u = (s - 0.36) / 0.28
        ang = PI / 2 + u * PI
        return np.array([-4.05 + 0.58 * np.cos(ang), 1.30 + 0.58 * np.sin(ang), 0.0])
    else:
        u = (s - 0.64) / 0.36
        return np.array([-4.05 + u * (-1.35 - (-4.05)), 0.72, 0.0])


def excrete_path_point(s):
    """Parametric point along the lower tubule lumen and exit_tube path to the urine droplet for s in [0, 1]."""
    pts = [
        np.array([-2.60, 0.72, 0.0]),
        np.array([-4.05, 0.72, 0.0]),
        np.array([-4.20, 0.56, 0.0]),
        np.array([-5.45, 0.56, 0.0]),
        np.array([-5.45, 0.18, 0.0]),
    ]
    segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
    total = sum(segs)
    target = (s % 1.0) * total
    acc = 0.0
    for i, seg_len in enumerate(segs):
        if target <= acc + seg_len or i == len(segs) - 1:
            u = np.clip((target - acc) / max(seg_len, 1e-9), 0.0, 1.0)
            return pts[i] + u * (pts[i + 1] - pts[i])
        acc += seg_len
    return pts[-1]


TRAY_X = -3.10


def make_acid_tray(n_dots=10, seed=41, center_x=TRAY_X):
    """Shallow RED tray under the left side (away from dissolved CO2) holding unbreathed protons."""
    tray = VGroup(
        Line([center_x - 0.72, -2.96, 0], [center_x - 0.72, -3.28, 0], color=ACID_COL, stroke_width=3.4),
        Line([center_x - 0.72, -3.28, 0], [center_x + 0.72, -3.28, 0], color=ACID_COL, stroke_width=3.4),
        Line([center_x + 0.72, -3.28, 0], [center_x + 0.72, -2.96, 0], color=ACID_COL, stroke_width=3.4),
    )
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for i in range(n_dots):
        x = center_x - 0.56 + (i % 5) * 0.28 + rng.uniform(-0.03, 0.03)
        y = -3.18 + (i // 5) * 0.13
        d = Dot([x, y, 0], radius=0.052, color=ACID_COL, fill_opacity=0.92)
        d.layout_ok = True
        dots.add(d)
    return tray, dots


def make_tray_labels(center_x=TRAY_X):
    """Labels flanking the sulfuric-acid tray, clear of dissolved CO2 and the plasma scope tag."""
    still_lbl = T("still in the body", 24, ACID_COL).move_to([center_x + 0.90, -3.14, 0], aligned_edge=LEFT)
    sulf_lbl = T("sulfuric acid", 24, ACID_COL).move_to([center_x - 0.90, -3.14, 0], aligned_edge=RIGHT)
    return still_lbl, sulf_lbl


def make_buffering_bars():
    """Shared 55 : 2.6 open-vs-sealed buffering comparison bars and ×20 bracket for s09 and s10."""
    base_y = -1.12
    max_h = 2.90
    open_h = max_h
    sealed_h = max_h * (2.6 / 55.0)
    x_open, x_sealed, bar_w = 2.58, 4.54, 0.58

    baseline = Line([2.02, base_y, 0], [5.04, base_y, 0], color=TEXT, stroke_width=3.2)
    axis_lbl = T("acid per pH unit", 26, TEXT).move_to([3.58, base_y - 1.80, 0])

    open_bar = Rectangle(width=bar_w, height=open_h, color=BICARB_COL, stroke_width=3.2,
                         fill_color=BICARB_COL, fill_opacity=0.28).move_to([x_open, base_y + open_h / 2, 0])
    open_lbl = M("open: 55", 26, BICARB_COL).move_to([x_open, base_y + open_h + 0.28, 0])
    open_icon = make_lungs(dim=False).set_height(0.38).move_to([x_open, base_y - 0.34, 0])
    open_tag = T("all\nbicarbonate\nbuffers", 22, BICARB_COL, line_spacing=0.80).move_to([x_open, base_y - 1.06, 0])

    sealed_bar = Rectangle(width=bar_w, height=sealed_h, color=TEXT, stroke_width=3.0,
                           fill_color=TEXT, fill_opacity=0.35).move_to([x_sealed, base_y + sealed_h / 2, 0])
    sealed_lbl = M("sealed: 2.6", 24, TEXT).move_to([x_sealed - 0.08, base_y + sealed_h + 0.36, 0])
    lid_icon = RoundedRectangle(corner_radius=0.04, width=0.55, height=0.14, color=TEXT, stroke_width=2.5,
                                fill_color=TEXT, fill_opacity=0.30).move_to([x_sealed, base_y - 0.34, 0])
    sealed_tag = T("tiny CO2 pool\nlimits", 22, TEXT, line_spacing=0.85).move_to([x_sealed + 0.04, base_y - 0.98, 0])

    br_x = 2.92
    bracket = BraceBetweenPoints([br_x, base_y + sealed_h, 0], [br_x, base_y + open_h, 0], direction=RIGHT, color=WHITE)
    x20_lbl = T("about ×20", 26, WHITE).next_to(bracket, RIGHT, buff=0.14)
    all_grp = VGroup(
        baseline, axis_lbl, open_bar, open_icon, open_lbl, open_tag,
        sealed_bar, lid_icon, sealed_lbl, sealed_tag, bracket, x20_lbl,
    )
    return (
        all_grp, baseline, axis_lbl, open_bar, open_icon, open_lbl, open_tag,
        sealed_bar, lid_icon, sealed_lbl, sealed_tag, bracket, x20_lbl,
    )


# ================================================================== SCENES
class S00Hook(SpokenScene):
    def construct(self):
        w = make_world(bicarb=24.0, co2=1.2, lungs_dim=True, kidney_dim=True, tremble=0.015, seed=7)
        rain = make_acid_rain()
        rain._active = False
        rain.set_opacity(0.0)
        acid_lbl = T("acid, every day", 28, ACID_COL).move_to([2.95, 2.02, 0])
        h_counter = M("free H+: 40 nmol/L", 26, TEXT).move_to([4.55, 3.30, 0])
        q_txt = T("What holds pH there?", 34, WHITE).move_to([-1.25, 3.30, 0])

        self.add(w.group, rain)
        self.at("free hydrogen")
        self.play(FadeIn(h_counter, shift=DOWN * 0.08), run_time=0.35)

        self.at("metabolism adds acid")
        rain._active = True
        self.play(FadeIn(acid_lbl), run_time=0.35)

        self.at("stays near")
        tick_glow = Dot([GAUGE_X0, ph_to_y(7.4), 0], radius=0.09, color=WHITE)
        self.play(FadeIn(tick_glow), run_time=0.25)
        self.play(FadeOut(tick_glow), run_time=0.30)

        self.at("what holds")
        self.play(FadeIn(q_txt, shift=DOWN * 0.08), run_time=0.30)
        self.finish()


class S01Title(SpokenScene):
    def construct(self):
        w = make_world(bicarb=24.0, co2=1.2, lungs_dim=True, kidney_dim=True, tremble=0.010, seed=7)
        rain = make_acid_rain()
        q_txt = T("What holds pH there?", 34, WHITE).move_to([-1.25, 3.30, 0])
        title = T("One Ratio, Two Keepers", 42, WHITE, font=TITLE_FONT).move_to([0.0, 3.50, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.07)

        self.add(w.group, rain, q_txt)
        rain._active = False
        self.play(FadeOut(q_txt, run_time=0.25), FadeIn(title, shift=UP * 0.08, run_time=0.5), GrowFromCenter(rule, run_time=0.5))
        self.wait(0.95)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.4)
        self.finish()


class S02Fraction(SpokenScene):
    def construct(self):
        w = make_world(bicarb=24.0, co2=1.2, lungs_dim=True, kidney_dim=True, tremble=0.008, seed=7)
        plasma_tag = make_plasma_tag()
        lbl_top = M("24 mmol/L", 28, BICARB_COL).move_to([1.62, 0.90, 0], aligned_edge=LEFT)
        lbl_bot = M("1.2 mmol/L", 28, CO2_COL).move_to([1.62, -1.98, 0], aligned_edge=LEFT)
        split_bar = make_split_frac_bar()

        rx_co2 = M("CO2", 24, WHITE)
        rx_h2o = M("+ H2O", 24, WHITE)
        rx_h2co3 = M("→ H2CO3", 24, WHITE)
        rx_row1 = VGroup(rx_co2, rx_h2o, rx_h2co3).arrange(RIGHT, buff=0.10)
        rx_row1.move_to([1.62 + rx_row1.width / 2, -0.78, 0])

        rx_arr2 = M("→", 24, WHITE)
        rx_hp = M("H+", 24, ACID_COL)
        rx_plus2 = M("+", 24, WHITE)
        rx_hco3 = M("HCO3-", 24, BICARB_COL)
        rx_row2 = VGroup(rx_arr2, rx_hp, rx_plus2, rx_hco3).arrange(RIGHT, buff=0.10)
        rx_row2.move_to([1.92 + rx_row2.width / 2, -1.24, 0])

        self.add(w.group, plasma_tag)

        self.at("fraction")
        glow = Dot([GAUGE_X0, ph_to_y(7.4), 0], radius=0.10, color=WHITE)
        self.play(w.frac_bar.animate.set_stroke(WHITE, width=10.0), FadeIn(glow), run_time=0.4)
        self.play(w.frac_bar.animate.set_stroke(WHITE, width=7.0), FadeOut(glow), run_time=0.4)

        self.at("bicarbonate")
        self.play(w.upper_fluid.animate.set_fill(BICARB_COL, opacity=0.62), run_time=0.45)

        self.at("24 millimoles")
        self.play(FadeIn(lbl_top, shift=RIGHT * 0.1), run_time=0.45)

        self.at("dissolved carbon")
        self.play(w.lower_fluid.animate.set_fill(CO2_COL, opacity=0.72), run_time=0.45)

        self.at("1 2")
        self.play(FadeIn(lbl_bot, shift=RIGHT * 0.1), run_time=0.45)

        self.at("20 to 1")
        self.play(ReplacementTransform(w.frac_bar, split_bar), FadeIn(w.ratio_lbl), run_time=0.45)

        self.at("why is carbon dioxide")
        self.play(FadeIn(rx_co2, shift=RIGHT * 0.08), run_time=0.35)

        self.at("with water")
        self.play(FadeIn(rx_h2o, shift=RIGHT * 0.08), run_time=0.30)

        self.at("forms carbonic")
        self.play(FadeIn(rx_h2co3, shift=RIGHT * 0.08), run_time=0.35)

        self.at("releases a proton")
        self.play(FadeIn(rx_arr2), FadeIn(rx_hp), FadeIn(rx_plus2), FadeIn(rx_hco3), run_time=0.45)
        self.finish()


class S03Equation(SpokenScene):
    def construct(self):
        w = make_world(bicarb=24.0, co2=1.2, lungs_dim=True, kidney_dim=True, tremble=0.0, show_ratio=True, seed=7)
        plasma_tag = make_plasma_tag()
        lbl_top = M("24 mmol/L", 28, BICARB_COL).move_to([1.62, 0.90, 0], aligned_edge=LEFT)
        lbl_bot = M("1.2 mmol/L", 28, CO2_COL).move_to([1.62, -1.98, 0], aligned_edge=LEFT)

        eq1_ph = M("pH =", 24, WHITE)
        eq1_61 = M("6.1", 24, WHITE)
        eq1_log = M("+ log(ratio)", 24, WHITE)
        eq1 = VGroup(eq1_ph, eq1_61, eq1_log).arrange(RIGHT, buff=0.15).move_to([4.35, -2.76, 0])

        eq2 = M("pH = 6.1 + 1.30", 26, WHITE).move_to([4.35, -2.76, 0])
        eq3 = M("pH = 7.40", 28, WHITE).move_to([4.35, -2.76, 0])

        pk_y = ph_to_y(6.1)
        pk_tick = Line([GAUGE_X0 - 0.16, pk_y, 0], [GAUGE_X0 + 0.18, pk_y, 0], color=WHITE, stroke_width=4.0)
        pk_tag = T("pK: acid = base", 22, WHITE).move_to([2.05, -3.26, 0])
        pk_ptr = Line(pk_tag.get_corner(UR) + [0.06, 0.02, 0], eq1_61.get_bottom() + DOWN * 0.06, color=WHITE, stroke_width=2.2)

        self.add(w.group, plasma_tag, lbl_top, lbl_bot)

        self.at("pH is")
        self.play(Write(eq1_ph), run_time=0.40)

        self.at("6 1")
        self.play(FadeIn(eq1_61), run_time=0.35)

        self.at("plus the log")
        self.play(FadeIn(eq1_log), run_time=0.40)
        self.play(w.ratio_lbl.animate.set_color(GOLD), run_time=0.35)
        self.play(w.ratio_lbl.animate.set_color(WHITE), run_time=0.35)

        self.at("the pair's pK")
        self.play(FadeIn(pk_tick), FadeIn(pk_tag), Create(pk_ptr), run_time=0.45)

        self.at("log 20")
        self.play(FadeOut(pk_tick), FadeOut(pk_tag), FadeOut(pk_ptr), run_time=0.35)

        self.at("1 3")
        self.play(swap(eq1, eq2, run_time=0.45))

        self.at("pH 7 4")
        self.play(swap(eq2, eq3, run_time=0.45))
        glow = Dot([GAUGE_X0, ph_to_y(7.4), 0], radius=0.11, color=WHITE)
        self.play(FadeIn(glow), run_time=0.25)
        self.play(FadeOut(glow), run_time=0.35)
        self.finish()


class S04Double(SpokenScene):
    def construct(self):
        w = make_world(bicarb=24.0, co2=1.2, lungs_dim=True, kidney_dim=True, tremble=0.0, show_ratio=True, seed=7)
        w.group.remove(w.ratio_lbl)
        plasma_tag = make_plasma_tag()

        lbl_top = always_redraw(lambda: M(f"{w.bicarb.get_value():.0f} mmol/L", 28, BICARB_COL).move_to(
            [1.50, UPPER_BOT + conc_to_h(w.bicarb.get_value()) - 0.12, 0], aligned_edge=LEFT
        ))
        lbl_bot = always_redraw(lambda: M(f"{w.co2.get_value():.1f} mmol/L", 28, CO2_COL).move_to(
            [1.50, LOWER_BOT + conc_to_h(w.co2.get_value()) + 0.22, 0], aligned_edge=LEFT
        ))
        x2_top = M("×2", 28, BICARB_COL).move_to([-1.92, UPPER_BOT + conc_to_h(48.0) - 0.12, 0])
        x2_bot = M("×2", 28, CO2_COL).move_to([-1.92, LOWER_BOT + conc_to_h(2.4) + 0.22, 0])
        co2_pulse = Rectangle(
            width=TANK_W - 0.04, height=max(0.04, conc_to_h(2.4)),
            stroke_width=4.0, stroke_color=WHITE, fill_color=CO2_COL, fill_opacity=0.85,
        ).move_to([TANK_X, LOWER_BOT + max(0.04, conc_to_h(2.4)) / 2, 0])
        ratio_live = always_redraw(lambda: M(f"{w.bicarb.get_value() / w.co2.get_value():.0f} : 1", 34, WHITE).move_to([0, FRAC_Y, 0]))
        ph_low = compute_ph(12.0, 1.2)
        ph_tag = M(f"{ph_low:.2f}", 26, WHITE).move_to([GAUGE_X0 - 1.02, ph_to_y(ph_low), 0])

        eq_a = M("6.1 + log 10", 22, WHITE)
        eq_b = M("= 6.1 + 1", 22, WHITE)
        eq_c = M("= 7.1", 22, WHITE)
        VGroup(eq_a, eq_b, eq_c).arrange(RIGHT, buff=0.14).move_to([4.15, -2.76, 0])

        self.add(w.group, plasma_tag, lbl_top, lbl_bot, ratio_live)

        self.at("double both")
        self.play(
            w.bicarb.animate.set_value(48.0), w.co2.animate.set_value(2.4),
            FadeIn(x2_top), FadeIn(x2_bot), run_time=1.3,
        )
        self.play(FadeIn(co2_pulse), x2_bot.animate.scale(1.18), run_time=0.22)
        self.play(FadeOut(co2_pulse), x2_bot.animate.scale(1 / 1.18), run_time=0.23)

        self.at("does not move")
        self.wait(0.6)
        self.play(
            w.bicarb.animate.set_value(24.0), w.co2.animate.set_value(1.2),
            FadeOut(x2_top), FadeOut(x2_bot), run_time=1.0,
        )

        self.at("the top alone")
        self.play(w.bicarb.animate.set_value(12.0), run_time=1.5)

        self.at("log 10")
        self.play(FadeIn(eq_a, shift=RIGHT * 0.06), run_time=0.35)

        self.at("is 1")
        self.play(FadeIn(eq_b, shift=RIGHT * 0.06), run_time=0.35)

        self.at("7 1")
        self.play(FadeIn(eq_c, shift=RIGHT * 0.06), FadeIn(ph_tag), run_time=0.35)

        self.at("follows the ratio")
        self.remove(ph_tag)
        self.play(FadeOut(eq_a), FadeOut(eq_b), FadeOut(eq_c), w.bicarb.animate.set_value(24.0), run_time=1.4)
        self.finish()


class S05Sealed(SpokenScene):
    def construct(self):
        w = make_world(bicarb=24.0, co2=1.2, lungs_dim=True, kidney_dim=True, tremble=0.0, show_ratio=True, seed=7)
        plasma_tag = make_plasma_tag()
        lid, clamp = make_lid_and_clamp()
        lid.shift(RIGHT * 2.0).set_opacity(0)
        clamp.set_opacity(0)
        full_bar = Line([FRAC_X0, FRAC_Y, 0], [FRAC_X1, FRAC_Y, 0], color=WHITE, stroke_width=7.0)

        pk_y = ph_to_y(6.1)
        ph74_y = ph_to_y(7.4)
        pk_band = Rectangle(
            width=0.52, height=0.56, color=WHITE, stroke_width=0, fill_color=WHITE, fill_opacity=0.20,
        ).move_to([GAUGE_X0, pk_y, 0])
        best_lbl = T("best here", 22, WHITE).move_to([GAUGE_X0 - 0.24, pk_y + 0.20, 0], aligned_edge=RIGHT)
        pk_tick = Line([GAUGE_X0 - 0.16, pk_y, 0], [GAUGE_X0, pk_y, 0], color=TEXT, stroke_width=3.0)
        pk_lbl = M("pK 6.1", 24, TEXT).move_to([GAUGE_X0 - 0.24, pk_y - 0.24, 0], aligned_edge=RIGHT)
        bracket = BraceBetweenPoints([3.74, pk_y, 0], [3.74, ph74_y, 0], direction=LEFT, color=TEXT)
        br_lbl = T("1.3 above", 24, TEXT).next_to(bracket, LEFT, buff=0.10)

        dose_tag = T("schematic dose", 24, TEXT).move_to([0.0, -3.08, 0])

        def _co2_step():
            v = w.co2.get_value()
            for thr, txt in [(6.10, "6.2"), (4.75, "4.8"), (3.55, "3.6"), (2.35, "2.4")]:
                if v >= thr:
                    return txt
            return "1.2"

        co2_step_lbl = always_redraw(lambda: M(_co2_step(), 28, CO2_COL).move_to([1.60, LOWER_BOT + 0.50, 0], aligned_edge=LEFT))

        rng = np.random.default_rng(31)
        burst_red = VGroup(*[
            Dot([rng.uniform(-1.0, 1.0), rng.uniform(UPPER_TOP - 0.35, UPPER_TOP - 0.08), 0], radius=0.062, color=ACID_COL)
            for _ in range(14)
        ])
        for d in burst_red:
            d.layout_ok = True
        new_co2_dots = VGroup(*[
            Circle(radius=0.056, color=CO2_COL, stroke_width=2.5, fill_color=CO2_COL, fill_opacity=0.80)
            .move_to([d.get_center()[0], UPPER_BOT + 0.35 + rng.uniform(-0.15, 0.15), 0])
            for d in burst_red
        ])
        for b in new_co2_dots:
            b.layout_ok = True

        self.add(w.group, plasma_tag)

        self.at("work best near")
        self.play(FadeIn(pk_band), FadeIn(best_lbl), run_time=0.50)

        self.at("pK")
        self.play(FadeIn(pk_tick), FadeIn(pk_lbl), run_time=0.45)

        self.at("1 3")
        self.play(Create(bracket), FadeIn(br_lbl), run_time=0.55)

        self.at("seal bicarbonate")
        w.lung_bubbles._active = False
        self.play(
            lid.animate.shift(LEFT * 2.0).set_opacity(1.0),
            clamp.animate.set_opacity(1.0),
            FadeOut(w.lung_bubbles),
            FadeOut(w.ratio_lbl),
            ReplacementTransform(w.frac_bar, full_bar),
            run_time=0.65,
        )

        self.at("add acid")
        self.add(burst_red)
        self.play(
            FadeIn(dose_tag),
            *[d.animate.move_to([d.get_center()[0], UPPER_BOT + 0.48, 0]) for d in burst_red],
            run_time=0.85,
        )

        self.at("each proton")
        self.play(*[ReplacementTransform(r, b) for r, b in zip(burst_red, new_co2_dots)], run_time=0.75)
        self.play(
            *[b.animate.move_to([b.get_center()[0], LOWER_BOT + 0.18, 0]) for b in new_co2_dots],
            w.bicarb.animate.set_value(19.0),
            run_time=1.0,
        )

        self.at("multiplies", lead=0.25)
        self.add(co2_step_lbl)
        self.play(w.co2.animate.set_value(6.2), FadeOut(new_co2_dots), run_time=1.05)

        self.at("pH crashes")
        self.wait(0.4)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w, lid, clamp, closed_grp, plasma_tag = make_sealed_state(tremble=0.015)
        closed_grp.set_opacity(0)
        q_lbl = T("A poor buffer, yet the main one?", 32, WHITE).move_to([0.0, 3.32, 0])

        self.add(w.group, lid, clamp, plasma_tag)

        self.at("poor buffer")
        self.play(closed_grp.animate.set_opacity(1.0), run_time=0.45)

        self.at("so how can")
        self.play(FadeIn(q_lbl, shift=DOWN * 0.08), run_time=0.5)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "A poor buffer, yet the main one?"
    CARD = {"y": 3.32, "color": WHITE, "size": 32}
    RING_AT = (-5.90, -3.10, 0)
    SECONDS = 4.5

    def backdrop(self):
        w, lid, clamp, closed_grp, plasma_tag = make_sealed_state(tremble=0.015)
        return VGroup(w.group, lid, clamp, closed_grp, plasma_tag)


class S08Open(SpokenScene):
    def construct(self):
        w, lid, clamp, closed_grp, plasma_tag = make_sealed_state(tremble=0.0)
        q_lbl = T("A poor buffer, yet the main one?", 32, WHITE).move_to([0.0, 3.32, 0])
        open_lbl = T("open", 28, LUNG_COL).move_to([LUNG_POS[0], LUNG_POS[1] - 1.24, 0])
        co2_out_lbl = T("CO2 out", 26, CO2_COL).move_to([-2.22, -0.78, 0])
        dose_tag = T("schematic dose", 24, TEXT).move_to([0.0, -3.08, 0])

        y_12 = LOWER_BOT + conc_to_h(1.2)
        dash_12 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_12, 0], [TANK_X + TANK_W / 2 + 0.08, y_12, 0],
                             color=CO2_COL, stroke_width=2.6, dash_length=0.12)

        rng = np.random.default_rng(31)
        burst_red = VGroup(*[
            Dot([rng.uniform(-1.0, 1.0), rng.uniform(UPPER_TOP - 0.35, UPPER_TOP - 0.08), 0], radius=0.062, color=ACID_COL)
            for _ in range(12)
        ])
        for d in burst_red:
            d.layout_ok = True
        bubbles_out = VGroup(*[
            Circle(radius=0.056, color=CO2_COL, stroke_width=2.5, fill_color=CO2_COL, fill_opacity=0.80)
            .move_to([d.get_center()[0], UPPER_BOT + 0.45, 0])
            for d in burst_red
        ])
        for b in bubbles_out:
            b.layout_ok = True

        def _bubble_path(p0, dy):
            x0, y0 = p0[0], p0[1]
            r = 0.28
            y_turn = -1.32 + dy + r
            pts = [np.array([x0, y0, 0.0])]
            n_arc = 7
            for k in range(n_arc + 1):
                ang = -k * (PI / 2) / n_arc
                pts.append(np.array([x0 - r + r * np.cos(ang), y_turn + r * np.sin(ang), 0.0]))
            pts.append(np.array([-3.85, -1.32 + dy, 0.0]))
            segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
            cum = np.concatenate([[0.0], np.cumsum(segs)])
            total = cum[-1]
            uni = []
            for sv in np.linspace(0.0, total, 48):
                idx = min(max(int(np.searchsorted(cum, sv, side="right")) - 1, 0), len(segs) - 1)
                u = (sv - cum[idx]) / max(segs[idx], 1e-9)
                uni.append(pts[idx] + u * (pts[idx + 1] - pts[idx]))
            path = VMobject()
            path.set_points_as_corners(uni)
            alpha_fade = float(np.clip((total - 0.70) / total, 0.75, 0.92))
            return path, alpha_fade

        def _move_bubble(b, path, alpha_fade):
            def anim(m, alpha):
                m.move_to(path.point_from_proportion(alpha))
                fade = 1.0 if alpha <= alpha_fade else max(0.0, 1.0 - (alpha - alpha_fade) / max(1.0 - alpha_fade, 1e-6))
                m.set_fill(opacity=0.80 * fade)
                m.set_stroke(opacity=fade)
            return UpdateFromAlphaFunc(b, anim)

        self.add(w.group, lid, clamp, closed_grp, q_lbl, plasma_tag)

        self.at("the body is open")
        self.play(
            FadeOut(q_lbl), FadeOut(closed_grp),
            w.bicarb.animate.set_value(24.0),
            w.co2.animate.set_value(1.2),
            lid.animate.shift(RIGHT * 2.0).set_opacity(0),
            clamp.animate.set_opacity(0),
            run_time=0.95,
        )
        set_organ_brightness(w.lungs, w.lung_tube, LUNG_COL, bright=True)
        w.lung_bubbles._active = True
        w.lung_bubbles._speed = 0.95
        self.play(FadeIn(open_lbl), Create(dash_12), FadeIn(dose_tag), w.lung_bubbles.animate.set_opacity(0.90), run_time=0.5)

        self.at("the lungs breathe")
        self.add(burst_red)
        self.play(*[d.animate.move_to([d.get_center()[0], UPPER_BOT + 0.48, 0]) for d in burst_red], run_time=0.75)
        self.play(*[ReplacementTransform(r, b) for r, b in zip(burst_red, bubbles_out)], run_time=0.45)
        bubble_anims = []
        for b in bubbles_out:
            path, alpha_fade = _bubble_path(b.get_center(), rng.uniform(-0.025, 0.025))
            bubble_anims.append(_move_bubble(b, path, alpha_fade))
        self.play(
            FadeIn(co2_out_lbl, run_time=0.45),
            LaggedStart(*bubble_anims, lag_ratio=0.04, run_time=1.25),
        )

        self.at("bottom term stays")
        self.play(dash_12.animate.set_stroke(WHITE, width=3.8), run_time=0.35)
        self.play(dash_12.animate.set_stroke(CO2_COL, width=2.6), run_time=0.35)

        self.at("only the top")
        self.play(w.bicarb.animate.set_value(19.0), run_time=1.0)
        self.finish()


class S09Twentyfold(SpokenScene):
    def construct(self):
        w = make_world(bicarb=19.0, co2=1.2, lungs_dim=False, kidney_dim=True, tremble=0.0, seed=29)
        set_organ_brightness(w.kidney, w.kidney_tube, KIDNEY_COL, bright=False)
        w.kidney.set_fill(KIDNEY_COL, opacity=0.22).set_stroke(KIDNEY_COL, opacity=0.32)
        for ln in w.kidney_tube:
            ln.set_stroke(KIDNEY_COL, opacity=0.32)
        plasma_tag = make_plasma_tag()
        y_12 = LOWER_BOT + conc_to_h(1.2)
        dash_12 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_12, 0], [TANK_X + TANK_W / 2 + 0.08, y_12, 0],
                             color=CO2_COL, stroke_width=2.6, dash_length=0.12)

        (_, baseline, axis_lbl, open_bar, open_icon, open_lbl, open_tag,
         sealed_bar, lid_icon, sealed_lbl, sealed_tag, bracket, x20_lbl) = make_buffering_bars()

        self.add(w.group, dash_12, plasma_tag)
        self.at("measure buffering")
        self.play(w.gauge_x.animate.set_value(5.65), FadeIn(baseline), FadeIn(axis_lbl), run_time=0.85)

        self.at("open")
        self.play(GrowFromEdge(open_bar, DOWN), FadeIn(open_icon), FadeIn(open_tag), run_time=0.85)

        self.at("55")
        self.play(FadeIn(open_lbl), run_time=0.40)

        self.at("sealed")
        self.play(GrowFromEdge(sealed_bar, DOWN), FadeIn(lid_icon), FadeIn(sealed_tag), run_time=0.70)

        self.at("2 6")
        self.play(FadeIn(sealed_lbl), run_time=0.40)

        self.at("20 fold")
        self.play(Create(bracket), FadeIn(x20_lbl), run_time=0.45)
        self.finish()


class S10Idea(SpokenScene):
    def construct(self):
        w = make_world(bicarb=19.0, co2=1.2, lungs_dim=False, kidney_dim=True, gauge_x=5.65, tremble=0.0, seed=29)
        plasma_tag = make_plasma_tag()
        y_12 = LOWER_BOT + conc_to_h(1.2)
        dash_12 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_12, 0], [TANK_X + TANK_W / 2 + 0.08, y_12, 0],
                             color=CO2_COL, stroke_width=2.6, dash_length=0.12)
        bars_all, *_ = make_buffering_bars()
        top_title = T("One ratio, two keepers", 34, WHITE).move_to([0.0, 3.32, 0])

        sw = make_stopwatch([-5.50, -1.05, 0], color=LUNG_COL)
        min_lbl = T("minutes", 26, LUNG_COL).move_to([-5.50, -1.78, 0])
        cal = make_calendar([-5.50, 1.55, 0], color=KIDNEY_COL)
        days_lbl = T("days", 26, KIDNEY_COL).move_to([-5.50, 0.85, 0])

        self.add(w.group, dash_12, plasma_tag, bars_all)

        self.at("one idea")
        self.play(FadeIn(top_title, shift=DOWN * 0.08), run_time=0.4)
        self.wait(0.45)
        self.play(FadeOut(bars_all), run_time=0.45)
        self.play(w.gauge_x.animate.set_value(GAUGE_X0), run_time=0.55)

        self.at("one ratio")
        self.play(w.frac_bar.animate.set_stroke(WHITE, width=11.0), run_time=0.45)
        self.play(w.frac_bar.animate.set_stroke(WHITE, width=7.0), run_time=0.45)

        self.at("bicarbonate")
        self.play(w.upper_fluid.animate.set_fill(BICARB_COL, opacity=0.68), run_time=0.35)
        self.play(w.upper_fluid.animate.set_fill(BICARB_COL, opacity=0.45), run_time=0.35)

        self.at("dissolved carbon")
        self.play(w.lower_fluid.animate.set_fill(CO2_COL, opacity=0.75), run_time=0.35)
        self.play(w.lower_fluid.animate.set_fill(CO2_COL, opacity=0.48), run_time=0.35)

        self.at("the lungs hold")
        pulse(w.lung_tube, base=3.6, amp=2.2, speed=5.0)
        self.play(FadeIn(sw), FadeIn(min_lbl), run_time=0.5)

        self.at("the kidney sets")
        set_organ_brightness(w.kidney, w.kidney_tube, KIDNEY_COL, bright=True)
        pulse(w.kidney_tube, base=3.6, amp=2.2, speed=5.0)
        self.play(FadeIn(cal), FadeIn(days_lbl), run_time=0.5)
        self.finish()


class S11NotRemoval(SpokenScene):
    def construct(self):
        w = make_world(bicarb=19.0, co2=1.2, lungs_dim=False, kidney_dim=False, tremble=0.0, seed=29)
        plasma_tag = make_plasma_tag()
        y_12 = LOWER_BOT + conc_to_h(1.2)
        dash_12 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_12, 0], [TANK_X + TANK_W / 2 + 0.08, y_12, 0],
                             color=CO2_COL, stroke_width=2.6, dash_length=0.12)
        tray, tray_dots = make_acid_tray(n_dots=10)
        still_lbl, sulf_lbl = make_tray_labels()

        y_24 = UPPER_BOT + conc_to_h(24.0)
        y_19 = UPPER_BOT + conc_to_h(19.0)
        dash_24 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_24, 0], [TANK_X + TANK_W / 2 + 0.08, y_24, 0],
                             color=BICARB_COL, stroke_width=2.8, dash_length=0.12)
        spent_band = Rectangle(width=TANK_W - 0.04, height=y_24 - y_19, stroke_width=0,
                               fill_color=BICARB_COL, fill_opacity=0.25).move_to([TANK_X, (y_24 + y_19) / 2, 0])
        spent_lbl = T("spent", 26, BICARB_COL).move_to([2.12, (y_24 + y_19) / 2, 0])

        self.add(w.group, dash_12, plasma_tag)

        self.at("sulfuric acid")
        scatter = tray_dots.copy()
        for i, d in enumerate(scatter):
            d.move_to([-0.8 + (i % 5) * 0.4, 0.7 + (i // 5) * 0.3, 0])
        self.add(scatter)
        self.play(
            FadeIn(tray), FadeIn(sulf_lbl),
            *[ReplacementTransform(s, t) for s, t in zip(scatter, tray_dots)],
            run_time=1.0,
        )

        self.at("breathed off")
        test_red = Dot([TRAY_X, -2.96, 0], radius=0.062, color=ACID_COL)
        test_red.layout_ok = True
        self.add(test_red)
        self.play(test_red.animate.move_to([-1.4, -1.45, 0]), run_time=0.65)
        self.play(test_red.animate.move_to([TRAY_X - 0.15, -3.10, 0]), run_time=0.65)
        self.remove(test_red)

        self.at("protons stay")
        self.play(FadeIn(still_lbl), run_time=0.45)

        self.at("bicarbonate they spent")
        self.play(Create(dash_24), FadeIn(spent_band), FadeIn(spent_lbl), run_time=0.6)

        self.at("until the kidney")
        self.play(w.kidney.animate.scale(1.14), run_time=0.4)
        self.play(w.kidney.animate.scale(1 / 1.14), run_time=0.4)
        self.finish()


class S12Reclaim(SpokenScene):
    def construct(self):
        w = make_world(bicarb=19.0, co2=1.2, lungs_dim=True, kidney_dim=False, tremble=0.0, seed=29)
        plasma_tag = make_plasma_tag()
        y_12 = LOWER_BOT + conc_to_h(1.2)
        dash_12 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_12, 0], [TANK_X + TANK_W / 2 + 0.08, y_12, 0],
                             color=CO2_COL, stroke_width=2.6, dash_length=0.12)
        tray, tray_dots = make_acid_tray(n_dots=10)
        still_lbl, sulf_lbl = make_tray_labels()

        y_24 = UPPER_BOT + conc_to_h(24.0)
        y_19 = UPPER_BOT + conc_to_h(19.0)
        dash_24 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_24, 0], [TANK_X + TANK_W / 2 + 0.08, y_24, 0],
                             color=BICARB_COL, stroke_width=2.8, dash_length=0.12)
        spent_band = Rectangle(width=TANK_W - 0.04, height=y_24 - y_19, stroke_width=0,
                               fill_color=BICARB_COL, fill_opacity=0.25).move_to([TANK_X, (y_24 + y_19) / 2, 0])
        spent_lbl = T("spent", 26, BICARB_COL).move_to([2.12, (y_24 + y_19) / 2, 0])

        tubule = make_tubule_group()
        filt_lbl = T("filtered", 24, BICARB_COL).move_to([-2.45, 2.30, 0])

        # Continuous BLUE stream circulating through the entire U-tubule
        n_stream = 18
        stream = VGroup()
        for i in range(n_stream):
            d = Dot(tubule_u_point(i / n_stream), radius=0.068, color=BICARB_COL)
            d._s = i / n_stream
            d.layout_ok = True
            stream.add(d)

        def upd_stream(mob, dt):
            for d in mob:
                d._s = (d._s + 0.24 * dt) % 1.0
                d.move_to(tubule_u_point(d._s))

        # Top-left 4,000 vs 50 (exact 80 : 1 height ratio) bars
        bx0, by0 = -6.05, 2.28
        h_4000 = 1.32
        h_50 = h_4000 / 80.0
        bar_4000 = Rectangle(width=0.38, height=h_4000, color=BICARB_COL, stroke_width=2.5,
                             fill_color=BICARB_COL, fill_opacity=0.55).move_to([bx0, by0 + h_4000 / 2, 0])
        bar_50 = Rectangle(width=0.38, height=h_50, color=ACID_COL, stroke_width=2.0,
                           fill_color=ACID_COL, fill_opacity=0.95).move_to([bx0 + 0.65, by0 + h_50 / 2, 0])
        bar_base = Line([bx0 - 0.25, by0, 0], [bx0 + 0.90, by0, 0], color=TEXT, stroke_width=2.5)
        lbl_4000 = T("about 4,000 mmol a day", 24, BICARB_COL).move_to([-5.62, 3.38, 0], aligned_edge=LEFT)
        lbl_50 = T("day's acid: about 50", 24, ACID_COL).move_to([-3.85, 2.75, 0])
        ptr_50 = Line([bx0 + 0.65, by0 + 0.05, 0], [lbl_50.get_left()[0] - 0.14, 2.66, 0], color=ACID_COL, stroke_width=2.0)
        bars_grp = VGroup(bar_base, bar_4000, bar_50, lbl_4000, lbl_50, ptr_50)

        dot_lum = Dot([-3.45, 0.72, 0], radius=0.075, color=WHITE, stroke_color=BICARB_COL, stroke_width=3)
        dot_bld = Dot([-1.75, 0.72, 0], radius=0.075, color=BICARB_COL, stroke_color=WHITE, stroke_width=2.5)
        arc = DashedVMobject(ArcBetweenPoints([-3.45, 0.72, 0], [-1.75, 0.72, 0], angle=-1.1, color=WHITE, stroke_width=2.8))
        ind_lbl = T("indirect route", 24, WHITE).move_to([-3.35, 0.04, 0])
        tally_lbl = T("−1 tubule, +1 blood = net 0", 24, WHITE).move_to([-4.15, 2.88, 0])

        w.group.remove(w.kidney, w.kidney_tube)
        k_grp = VGroup(w.kidney, w.kidney_tube)
        self.add(w.group, k_grp, dash_12, plasma_tag, tray, tray_dots, still_lbl, sulf_lbl, dash_24, spent_band, spent_lbl)

        self.wait(0.35)
        self.play(ReplacementTransform(k_grp, tubule), FadeIn(filt_lbl), FadeIn(stream), run_time=0.9)
        stream.add_updater(upd_stream)

        self.at("4 000")
        self.play(FadeIn(bar_base), FadeIn(bar_4000), FadeIn(lbl_4000), run_time=0.55)

        self.at("80 times")
        self.play(FadeIn(bar_50), FadeIn(ptr_50), FadeIn(lbl_50), run_time=0.50)

        self.at("takes it back")
        ret_dots = VGroup(*[Dot([-3.6 + 0.4 * i, 0.72, 0], radius=0.055, color=BICARB_COL) for i in range(4)])
        for d in ret_dots:
            d.layout_ok = True
        self.add(ret_dots)
        self.play(*[d.animate.move_to([-1.25, 0.72, 0]) for d in ret_dots], run_time=0.8)
        self.remove(ret_dots)

        self.at("each filtered bicarbonate is destroyed")
        self.play(FadeIn(dot_lum), Create(arc), FadeIn(ind_lbl), run_time=0.55)
        self.play(FadeOut(dot_lum), FadeIn(dot_bld), run_time=0.55)

        self.at("sends a twin")
        self.play(dot_bld.animate.move_to([-0.85, 0.72, 0]), run_time=0.75)
        self.remove(dot_bld)

        self.at("nothing gained")
        self.play(FadeOut(bars_grp), FadeOut(arc), FadeOut(ind_lbl), run_time=0.45)
        self.play(FadeIn(tally_lbl), spent_band.animate.set_fill(BICARB_COL, opacity=0.58), run_time=0.35)
        self.play(spent_band.animate.set_fill(BICARB_COL, opacity=0.25), run_time=0.35)
        self.finish()


class S13MakeNew(SpokenScene):
    def construct(self):
        w = make_world(bicarb=19.0, co2=1.2, lungs_dim=True, kidney_dim=False, tremble=0.0, seed=29)
        w.group.remove(w.kidney, w.kidney_tube)
        plasma_tag = make_plasma_tag()
        y_12 = LOWER_BOT + conc_to_h(1.2)
        dash_12 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_12, 0], [TANK_X + TANK_W / 2 + 0.08, y_12, 0],
                             color=CO2_COL, stroke_width=2.6, dash_length=0.12)
        tray, tray_dots = make_acid_tray(n_dots=7)
        still_lbl, sulf_lbl = make_tray_labels()

        y_24 = UPPER_BOT + conc_to_h(24.0)
        y_19 = UPPER_BOT + conc_to_h(19.0)
        dash_24 = DashedLine([TANK_X - TANK_W / 2 - 0.08, y_24, 0], [TANK_X + TANK_W / 2 + 0.08, y_24, 0],
                             color=BICARB_COL, stroke_width=2.8, dash_length=0.12)
        spent_band = Rectangle(width=TANK_W - 0.04, height=y_24 - y_19, stroke_width=0,
                               fill_color=BICARB_COL, fill_opacity=0.25).move_to([TANK_X, (y_24 + y_19) / 2, 0])
        spent_lbl = T("spent", 26, BICARB_COL).move_to([2.12, (y_24 + y_19) / 2, 0])

        tubule = make_tubule_group()
        exit_tube = VGroup(
            Line([-4.20, 0.56, 0], [-5.45, 0.56, 0], color=KIDNEY_COL, stroke_width=3.2),
            Line([-5.45, 0.56, 0], [-5.45, 0.18, 0], color=KIDNEY_COL, stroke_width=3.2),
        )
        droplet = Polygon([-5.45, 0.12, 0], [-5.63, -0.22, 0], [-5.45, -0.38, 0], [-5.27, -0.22, 0],
                          color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.28).round_corners(0.08)
        urine_lbl = T("urine", 24, GOLD).move_to([-5.45, -0.62, 0])
        schem_lbl = T("proportions schematic", 24, TEXT).move_to([-4.35, 3.25, 0])

        big_cell = RoundedRectangle(
            corner_radius=0.10, width=1.55, height=0.88,
            color=KIDNEY_COL, stroke_width=3.2, fill_color=BG, fill_opacity=0.96,
        ).move_to([-2.55, 1.32, 0])
        in_co2 = Circle(radius=0.065, color=CO2_COL, stroke_width=2.5, fill_color=CO2_COL, fill_opacity=0.85).move_to([-1.45, 1.32, 0])
        in_co2.layout_ok = True
        h2co3_chip = boxed_label("H2CO3", WHITE, size=22, pad=0.10).move_to(big_cell.get_center())
        split_red = Dot(big_cell.get_center(), radius=0.062, color=ACID_COL)
        split_blue = Dot(big_cell.get_center(), radius=0.062, color=BICARB_COL)
        split_red.layout_ok = True
        split_blue.layout_ok = True
        to_urine_lbl = T("to urine", 22, ACID_COL).move_to([-3.85, 0.28, 0])
        to_blood_lbl = T("to blood", 22, BICARB_COL).move_to([-2.08, 2.46, 0])

        glut = boxed_label("glutamine", AMM_COL, size=22, pad=0.10).move_to([-3.28, 1.30, 0])
        amm_lbl = T("ammonium", 24, AMM_COL).move_to([-3.55, 2.38, 0])
        phos_lbl = T("phosphate", 24, PHOS_COL).move_to([-3.32, 1.28, 0])

        # Ongoing acid-excretion stream before phosphate/ammonium detail
        stream_red = VGroup(*[Dot(excrete_path_point(i / 4), radius=0.048, color=ACID_COL) for i in range(4)])
        for i, d in enumerate(stream_red):
            d._s = i / 4
            d.layout_ok = True

        def upd_sred(mob, dt):
            for d in mob:
                d._s = (d._s + 0.23 * dt) % 1.0
                d.move_to(excrete_path_point(d._s))

        phos_tokens = VGroup(*[
            VGroup(
                RoundedRectangle(corner_radius=0.06, width=0.24, height=0.16, color=PHOS_COL, stroke_width=2.2,
                                 fill_color=PHOS_COL, fill_opacity=0.38),
                Dot(ORIGIN, radius=0.042, color=ACID_COL),
            ).move_to([-2.8 - 0.55 * i, 0.72, 0])
            for i in range(2)
        ])
        amm_tokens = VGroup(*[
            Circle(radius=0.10, color=AMM_COL, stroke_width=2.5, fill_color=AMM_COL, fill_opacity=0.0)
            .set_stroke(AMM_COL, opacity=0.0)
            .scale(0.25)
            .move_to(glut.get_bottom() + DOWN * 0.14)
            for _ in range(5)
        ])

        def curve_to_tubule(dot, target):
            p0 = dot.get_center()
            p1 = np.array(target, dtype=float)
            pts = [p0, np.array([-1.85, -2.0, 0.0]), np.array([-1.56, 0.25, 0.0])]
            if p1[0] < -2.9:
                pts.append(np.array([-2.65, 0.72, 0.0]))
            pts.append(p1)
            path = VMobject()
            path.set_points_smoothly(pts)
            return MoveAlongPath(dot, path)

        excrete_pts = [
            np.array([-2.60, 0.72, 0.0]),
            np.array([-4.05, 0.72, 0.0]),
            np.array([-4.20, 0.56, 0.0]),
            np.array([-5.45, 0.56, 0.0]),
            np.array([-5.45, 0.18, 0.0]),
        ]
        excrete_total = sum(np.linalg.norm(excrete_pts[i + 1] - excrete_pts[i]) for i in range(len(excrete_pts) - 1))

        def excrete_along_tube(mob):
            x0 = mob.get_center()[0]
            s0 = float(np.clip((-2.60 - x0) / excrete_total, 0.0, 0.43))
            end_pt = excrete_path_point(0.9999)
            drop_pt = droplet.get_center()
            orig_ops = [(m, m.get_fill_opacity(), m.get_stroke_opacity()) for m in mob.family_members_with_points()]

            def anim(m, alpha):
                if alpha <= 0.85:
                    s = s0 + (alpha / 0.85) * (0.9999 - s0)
                    m.move_to(excrete_path_point(s))
                    fade = 1.0
                else:
                    u = (alpha - 0.85) / 0.15
                    m.move_to(end_pt * (1.0 - u) + drop_pt * u)
                    fade = 1.0 - u
                for sub, fo, so in orig_ops:
                    sub.set_fill(opacity=fo * fade)
                    sub.set_stroke(opacity=so * fade)

            return UpdateFromAlphaFunc(mob, anim)

        self.add(w.group, tubule, dash_12, plasma_tag, tray, tray_dots, still_lbl, sulf_lbl,
                 dash_24, spent_band, spent_lbl)

        self.at("Job 2")
        open_bend = Arc(radius=0.74, start_angle=PI / 2, angle=0.692 * PI,
                        arc_center=[-4.20, 1.30, 0], color=KIDNEY_COL, stroke_width=3.4)
        self.play(Transform(tubule.bend_outer, open_bend), Create(exit_tube), FadeIn(droplet), FadeIn(urine_lbl), FadeIn(schem_lbl), run_time=0.6)

        self.at("inside a kidney cell")
        self.play(
            FadeOut(tubule.cells[1]), FadeOut(tubule.cells[2]), FadeOut(tubule.cells[3]),
            FadeIn(big_cell), FadeIn(in_co2), run_time=0.45,
        )
        self.play(in_co2.animate.move_to(big_cell.get_center()), run_time=0.50)

        self.at("carbonic acid")
        self.play(ReplacementTransform(in_co2, h2co3_chip), run_time=0.45)

        self.at("proton goes to the urine")
        self.play(FadeOut(h2co3_chip), FadeIn(split_red), FadeIn(split_blue), run_time=0.30)
        self.play(split_red.animate.move_to([-3.65, 0.72, 0]), FadeIn(to_urine_lbl), run_time=0.65)

        self.at("new bicarbonate")
        self.play(split_blue.animate.move_to([-1.45, 1.32, 0]), FadeIn(to_blood_lbl), run_time=0.55)
        self.play(
            split_blue.animate.move_to([-0.80, 1.05, 0]).set_opacity(0),
            split_red.animate.move_to([-4.20, 0.65, 0]).set_opacity(0),
            w.bicarb.animate.set_value(19.6),
            run_time=0.55,
        )
        self.play(
            FadeOut(big_cell), FadeOut(to_urine_lbl), FadeOut(to_blood_lbl),
            FadeIn(tubule.cells[1]), FadeIn(tubule.cells[2]), FadeIn(tubule.cells[3]),
            run_time=0.35,
        )
        self.remove(split_red, split_blue)
        self.add(stream_red)
        stream_red.add_updater(upd_sred)

        self.at("ride out on phosphate")
        stream_red.clear_updaters()
        self.remove(stream_red)
        p_reds = VGroup(tray_dots[0], tray_dots[1])
        self.play(
            FadeIn(phos_lbl), FadeIn(phos_tokens),
            curve_to_tubule(p_reds[0], phos_tokens[0].get_center()),
            curve_to_tubule(p_reds[1], phos_tokens[1].get_center()),
            run_time=0.65,
        )
        new_b1 = VGroup(*[Dot([-1.75, 1.1 + 0.3 * i, 0], radius=0.055, color=BICARB_COL) for i in range(2)])
        for d in new_b1:
            d.layout_ok = True
        self.play(
            *[excrete_along_tube(tok) for tok in phos_tokens],
            *[excrete_along_tube(rd) for rd in p_reds],
            FadeIn(new_b1),
            run_time=0.75,
        )
        self.play(
            *[d.animate.move_to([-0.5 + 0.6 * i, 0.9, 0]) for i, d in enumerate(new_b1)],
            w.bicarb.animate.set_value(20.8),
            run_time=0.55,
        )
        self.remove(new_b1, phos_tokens)

        self.at("ammonium")
        a_reds = VGroup(*tray_dots[2:])
        self.play(
            FadeOut(phos_lbl), FadeOut(tubule.cells[1]), FadeOut(tubule.cells[2]),
            FadeIn(glut), FadeIn(amm_lbl), run_time=0.35,
        )
        self.add(amm_tokens)
        self.play(
            *[
                tok.animate.scale(4.0).set_fill(AMM_COL, opacity=0.48).set_stroke(AMM_COL, opacity=1.0)
                .move_to([-2.65 - 0.33 * i, 0.72, 0])
                for i, tok in enumerate(amm_tokens)
            ],
            *[curve_to_tubule(rd, [-2.65 - 0.33 * i, 0.72, 0]) for i, rd in enumerate(a_reds)],
            run_time=0.80,
        )
        new_b2 = VGroup(*[Dot([-1.52, 0.8 + 0.22 * i, 0], radius=0.055, color=BICARB_COL) for i in range(5)])
        for d in new_b2:
            d.layout_ok = True
        self.at("which also yields")
        self.play(
            *[excrete_along_tube(tok) for tok in amm_tokens],
            *[excrete_along_tube(rd) for rd in a_reds],
            FadeIn(new_b2),
            FadeOut(spent_band), FadeOut(spent_lbl),
            FadeOut(still_lbl), FadeOut(sulf_lbl),
            tray.animate.set_stroke(opacity=0.30),
            w.bicarb.animate.set_value(24.0),
            run_time=0.85,
        )
        self.play(*[d.animate.move_to([-0.8 + 0.4 * i, 1.0, 0]) for i, d in enumerate(new_b2)], run_time=0.4)
        self.remove(new_b2, amm_tokens)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        w = make_world(bicarb=24.0, co2=1.2, lungs_dim=False, kidney_dim=False, tremble=0.0, show_ratio=True, seed=29)
        w.group.remove(w.kidney, w.kidney_tube)
        plasma_tag = make_plasma_tag()
        tubule = make_tubule_group(open_exit=True)
        exit_tube = VGroup(
            Line([-4.20, 0.56, 0], [-5.45, 0.56, 0], color=KIDNEY_COL, stroke_width=3.2),
            Line([-5.45, 0.56, 0], [-5.45, 0.18, 0], color=KIDNEY_COL, stroke_width=3.2),
        )
        droplet = Polygon([-5.45, 0.12, 0], [-5.63, -0.22, 0], [-5.45, -0.38, 0], [-5.27, -0.22, 0],
                          color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.28).round_corners(0.08)
        urine_lbl = T("urine", 24, GOLD).move_to([-5.45, -0.62, 0])

        rain = make_acid_rain()
        sw = make_stopwatch([-5.55, -1.65, 0], color=LUNG_COL)
        min_lbl = T("minutes", 26, LUNG_COL).move_to([-5.55, -2.35, 0])
        cal = make_calendar([-5.60, 2.78, 0], color=KIDNEY_COL)
        days_lbl = T("days", 26, KIDNEY_COL).move_to([-5.60, 2.12, 0])

        excrete_dots = VGroup(*[Dot(excrete_path_point(i / 4), radius=0.052, color=ACID_COL) for i in range(4)])
        return_dots = VGroup(*[Dot([-1.95 + 0.35 * i, 1.30, 0], radius=0.052, color=BICARB_COL) for i in range(4)])
        for i, d in enumerate(excrete_dots):
            d._s = i / 4
        for d in (*excrete_dots, *return_dots):
            d.layout_ok = True

        def upd_excrete(mob, dt):
            for d in mob:
                d._s = (d._s + 0.26 * dt) % 1.0
                d.move_to(excrete_path_point(d._s))

        def upd_return(mob, dt):
            for d in mob:
                nx = d.get_center()[0] + 0.65 * dt
                if nx > -0.65:
                    nx = -1.95
                d.move_to([nx, 1.30, 0])

        excrete_dots.add_updater(upd_excrete)
        return_dots.add_updater(upd_return)

        self.add(w.group, tubule, exit_tube, droplet, urine_lbl, rain, excrete_dots, return_dots, plasma_tag)

        self.at("breathing clears")
        w.lung_bubbles._speed = 1.05
        self.play(FadeIn(sw), FadeIn(min_lbl), run_time=0.5)

        self.at("the kidney repays")
        self.play(FadeIn(cal), FadeIn(days_lbl), run_time=0.5)
        self.finish()


class S15End(EndCard):
    LINE = "pH follows one ratio: lungs hold the bottom, kidneys rebuild the top."
