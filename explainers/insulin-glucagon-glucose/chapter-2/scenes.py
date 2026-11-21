"""
Holding Glucose Still — Chapter 2 of Insulin, Glucagon and Blood Glucose

COLOUR MAP (one colour per concept for the whole film):
- YELLOW (#F5D547): glucose (blood glucose dots, glucose curve, blood glucose gauge, entry/exit arrows)
- PURPLE (#C084FC): insulin (insulin dots from islet, insulin gauge, reduced-secretion curve)
- BLUE   (#4B8BFA): membrane transporters (GLUT4 doors on muscle and fat, weaker-action curve)
- GREY   (#8B93A1): cells, organs, blood band outline, axes, structural containers
- GREEN  (#83C167): supported / verified ('measured, not assumed' tick)
- RED    (#FC6255): not identified / refuted assumption (defect '?' and cross, 'liver: 0' cross)
- CYAN   (#2CE5E5): clamp glucose pump (external glucose J, pump bar, pump dots, feedback loop)
- MAGENTA(#F05AD8): endogenous glucose (body makes / mostly liver EGP, tracer rings, liver bar)
- TEXT   (#E8EAF0): disposal (Rd bar, all-tissues exit), primary labels, equations, question cards

THE ONE CARRIED WORLD:
Across the middle-left sits a wide translucent 'blood' band carrying flowing YELLOW glucose dots,
supplied above-left by the GREY 'liver' (and in early scenes a top-centre 'glucose drink' cup, plus
in clamp scenes a top-left CYAN 'pump' and left PURPLE insulin gauge), regulated by the GREY islet
above-right, drained below into the GREY 'muscle and fat' block through movable BLUE transporter
doors, and read out at the band's right end by a vertical 'blood glucose' gauge.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Islet fires PURPLE insulin dots on pull-back; insulin opens more BLUE
  doors and thins liver inflow; drink cup pours YELLOW glucose dots and a ValueTracker drives the
  gauge past the 'too high' line; particle velocity & exit count update from insulin/door state.
- s02_curve: Single ValueTracker t (0..2 h) simultaneously drives the blood glucose gauge and plots
  the computed healthy OGTT curve g(t) = 90 + 60*(t/0.75)*exp(1 - t/0.75) peaking in 140-160 mg/dL.
- s03_two_faults: Run 1 cuts insulin dot rate, closes BLUE doors, thickens liver inflow, and plots
  computed high curve g_sec(t); Run 2 restores insulin dots, keeps doors closed/liver high, and
  plots dashed curve g_act(t), both synced to the gauge tracker.
- s04_balance: Drink+liver inflows gather into an 'in' arrow and tissue exit into an 'out' arrow;
  arrow widths and gauge ValueTracker change together from equal (steady) to in > out (climbing).
- s05_clamps: Caliper bracket pins glucose gauge (high then basal); PURPLE insulin gauge tracker
  rises to plateau opening BLUE doors; CYAN pump dial oscillates by computed feedback while
  pumping CYAN-ringed glucose dots to hold the glucose gauge steady at basal.
- s06_rule: World flows transform into stacked bars (CYAN J + MAGENTA EGP) matching WHITE disposal
  bar (Rd) via coordinated height trackers as Rd = J + EGP builds.
- s07_predict: World splits into side-by-side copies A and B; MAGENTA EGP shrinks to 0; shared
  0-7 mg/kg/min axis bars and CYAN pump dot rates update to 5.71 (A) and 2.86 (B).
- s09_answer: WHITE disposal bars grow on the same 0-7 axis to match 5.71 (A) and 2.86 (B) with
  exit dot flux in B half of A, ratio 2.86 / 5.71 = 0.50 computed, then zoom into B's cell with '?'.
- s10_liver: Copy B fades; A's liver trickles MAGENTA dots; CYAN-ringed/MAGENTA-ringed tracer dots
  mix in blood to drive the 'blood samples' readout and stack MAGENTA EGP = 0.50 onto CYAN 5.71,
  growing WHITE Rd to computed 5.71 + 0.50 = 6.21.
- s11_close: Pulls back to full carried world; inset curve glows, clamp pins gauge so 'in' and 'out'
  arrows equalize, and pump, liver trickle, and tissue exit pulse in sequence with Rd = J + EGP.
"""

from bp_parts import *

# Override / extend house palette so every concept colour is distinct and high-contrast on BG (#0f1117)
BLUE = "#4B8BFA"      # membrane transporters (distinct from CYAN)
PURPLE = "#C084FC"    # insulin
CYAN = "#2CE5E5"      # clamp glucose pump (J)
MAGENTA = "#F05AD8"   # endogenous glucose / liver (EGP) and tracer rings
WHITE = TEXT          # disposal (Rd) and primary crisp text


# ---------------------------------------------------------------------------
# Mathematical models (computed from lesson numbers; deterministic RNG)
# ---------------------------------------------------------------------------
def ogtt_healthy(t):
    """Healthy 75 g OGTT curve (mg/dL) over 0..2 h: 90 basal, peaks at 150 (140-160 band), <140 by 2 h."""
    if t <= 0:
        return 90.0
    return 90.0 + 60.0 * (t / 0.75) * np.exp(1.0 - t / 0.75)


def ogtt_less_secretion(t):
    """Schematic curve for reduced insulin secretion: climbs higher (~185) and stays elevated longer."""
    if t <= 0:
        return 95.0
    return 95.0 + 90.0 * (t / 0.90) * np.exp(1.0 - t / 0.90)


def ogtt_weaker_action(t):
    """Schematic curve for weaker insulin action: similar high trajectory (~183), not identical."""
    if t <= 0:
        return 95.0
    return 95.0 + 88.0 * (t / 0.96) * np.exp(1.0 - t / 0.96)


# ---------------------------------------------------------------------------
# Reusable carried-world builder and particle flow simulator
# ---------------------------------------------------------------------------
def make_islet(center, scale=1.0):
    """Three-cell GREY islet icon (no molecular structures)."""
    c1 = RoundedRectangle(width=0.68, height=0.46, corner_radius=0.18, color=GREY, stroke_width=2.8,
                          fill_color=GREY, fill_opacity=0.22).shift(LEFT * 0.24 + UP * 0.10)
    c2 = RoundedRectangle(width=0.68, height=0.46, corner_radius=0.18, color=GREY, stroke_width=2.8,
                          fill_color=GREY, fill_opacity=0.22).shift(RIGHT * 0.24 + UP * 0.10)
    c3 = RoundedRectangle(width=0.72, height=0.46, corner_radius=0.18, color=GREY, stroke_width=2.8,
                          fill_color=GREY, fill_opacity=0.22).shift(DOWN * 0.18)
    g = VGroup(c1, c2, c3).scale(scale).move_to(center)
    return g


def make_liver(center, width=1.65, height=0.92, label_size=26):
    """GREY liver lobe polygon with crisp 'liver' label."""
    pts = [
        [-0.50 * width, -0.35 * height, 0],
        [-0.45 * width,  0.32 * height, 0],
        [ 0.10 * width,  0.46 * height, 0],
        [ 0.50 * width,  0.18 * height, 0],
        [ 0.42 * width, -0.38 * height, 0],
    ]
    shape = Polygon(*pts, color=GREY, stroke_width=3.0, fill_color=GREY, fill_opacity=0.20)
    shape.round_corners(radius=0.14)
    shape.move_to(center)
    lbl = T("liver", size=label_size, color=TEXT).move_to(shape.get_center() + DOWN * 0.02)
    return VGroup(shape, lbl)


def make_cup(center, label="glucose drink", label_size=24):
    """GREY glucose drink cup above blood band."""
    pts = [
        [-0.42,  0.40, 0],
        [ 0.42,  0.40, 0],
        [ 0.30, -0.40, 0],
        [-0.30, -0.40, 0],
    ]
    body = Polygon(*pts, color=GREY, stroke_width=3.0, fill_color=GREY, fill_opacity=0.18)
    fill = Polygon(
        [-0.36, 0.14, 0], [0.36, 0.14, 0], [0.27, -0.36, 0], [-0.27, -0.36, 0],
        color=YELLOW, stroke_width=0, fill_color=YELLOW, fill_opacity=0.45
    )
    cup = VGroup(fill, body).move_to(center)
    lbl = T(label, size=label_size, color=TEXT).next_to(cup, UP, buff=0.12)
    return VGroup(cup, lbl)


def make_pump(center, dial_tracker=None, label="pump", label_size=24, scale=1.0):
    """CYAN glucose clamp pump with live twitching rate dial (generous padding so label clears dial)."""
    w, h = 1.92 * scale, 0.86 * scale
    box = RoundedRectangle(width=w, height=h, corner_radius=0.14 * scale,
                           stroke_color=CYAN, stroke_width=3.0, fill_color=CYAN, fill_opacity=0.18).move_to(center)
    lbl = T(label, size=label_size, color=CYAN).move_to(box.get_center() + LEFT * 0.28 * scale)
    dial_c = box.get_center() + RIGHT * 0.52 * scale
    ring = Circle(radius=0.20 * scale, stroke_color=CYAN, stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to(dial_c)
    if dial_tracker is None:
        dial_tracker = ValueTracker(0.5)
    needle = always_redraw(lambda: Line(
        ring.get_center(),
        ring.get_center() + 0.15 * scale * np.array([
            np.cos(PI * 0.75 - dial_tracker.get_value() * PI * 0.8),
            np.sin(PI * 0.75 - dial_tracker.get_value() * PI * 0.8),
            0.0,
        ]),
        color=TEXT, stroke_width=3.0
    ))
    return VGroup(box, lbl, ring, needle)


def make_gauge(center, height=2.2, width=0.48, level_tracker=None, fill_color=YELLOW,
               label="blood glucose", label_size=24, too_high_frac=0.72, basal_frac=0.30,
               show_too_high=False, show_basal=False):
    """Vertical tube gauge driven by level_tracker (0..1). Never overwrites VGroup.height!"""
    if level_tracker is None:
        level_tracker = ValueTracker(basal_frac)
    x, y = center[0], center[1]
    y0, y1 = y - height / 2, y + height / 2
    tube = RoundedRectangle(width=width, height=height, corner_radius=0.10,
                            stroke_color=GREY, stroke_width=3.0, fill_color=GREY, fill_opacity=0.12).move_to(center)

    def mk_fill():
        f = float(np.clip(level_tracker.get_value(), 0.04, 0.96))
        h = max(0.06, f * (height - 0.08))
        r = RoundedRectangle(width=width - 0.10, height=h, corner_radius=0.06,
                             stroke_width=0, fill_color=fill_color, fill_opacity=0.88)
        r.move_to([x, y0 + 0.04 + h / 2, 0])
        return r

    fill = always_redraw(mk_fill)
    parts = [tube, fill]
    lbl = T(label, size=label_size, color=TEXT if fill_color == YELLOW else fill_color)
    lbl.next_to(tube, DOWN, buff=0.18)
    parts.append(lbl)
    if show_too_high:
        hy = y0 + too_high_frac * height
        hline = DashedLine([x - width / 2 - 0.10, hy, 0], [x + width / 2 + 0.10, hy, 0],
                           color=RED, stroke_width=3.0, dash_length=0.08)
        htag = T("too high", size=22, color=RED).next_to(hline, RIGHT, buff=0.14)
        parts.extend([hline, htag])
    if show_basal:
        by = y0 + basal_frac * height
        bline = DashedLine([x - width / 2 - 0.10, by, 0], [x + width / 2 + 0.10, by, 0],
                           color=TEXT, stroke_width=2.5, dash_length=0.08)
        btag = T("basal", size=22, color=TEXT).next_to(bline, LEFT, buff=0.14)
        parts.extend([bline, btag])
    g = VGroup(*parts)
    g.tube = tube
    g.lbl = lbl
    g.g_y0 = y0
    g.g_y1 = y1
    g.g_h = height
    return g


def make_clamp_bracket(gauge, level_tracker, label="held"):
    """GOLD caliper bracket that tracks the gauge's pinned level."""
    def mk():
        f = float(np.clip(level_tracker.get_value(), 0.08, 0.92))
        cy = gauge.g_y0 + f * gauge.g_h
        x = gauge.tube.get_center()[0]
        hw = gauge.tube.width / 2 + 0.14
        bracket = VGroup(
            Line([x - hw, cy + 0.14, 0], [x + hw, cy + 0.14, 0], color=GOLD, stroke_width=4.0),
            Line([x - hw, cy - 0.14, 0], [x + hw, cy - 0.14, 0], color=GOLD, stroke_width=4.0),
            Line([x + hw, cy - 0.14, 0], [x + hw, cy + 0.14, 0], color=GOLD, stroke_width=4.0),
        )
        tag = T(label, size=24, color=GOLD).next_to(bracket, RIGHT, buff=0.14)
        return VGroup(bracket, tag)
    return always_redraw(mk)


def make_blood_stream(x0, x1, y_bot, y_top, n_glucose=18, n_cyan=0, n_tracer=0,
                      speed_tracker=None, seed=7):
    """Computed particle stream moving across the blood band without touching the top-left 'blood' label."""
    rng = np.random.default_rng(seed)
    lane_y0 = y_bot + 0.12
    lane_y1 = y_top - 0.50   # keeps clear of 'blood' label in upper-left of band
    if lane_y1 <= lane_y0 + 0.12:
        lane_y1 = y_top - 0.14
    if speed_tracker is None:
        speed_tracker = ValueTracker(1.0)

    dots = VGroup()
    specs = []
    total = n_glucose + n_cyan + n_tracer
    for i in range(total):
        if i < n_glucose:
            d = Dot(radius=0.068, color=YELLOW, fill_opacity=0.95)
        elif i < n_glucose + n_cyan:
            d = Dot(radius=0.075, color=YELLOW, stroke_color=CYAN, stroke_width=3.2, fill_opacity=0.95)
        else:
            d = Dot(radius=0.082, color=YELLOW, stroke_color=MAGENTA, stroke_width=3.8, fill_opacity=1.0)
        px = rng.uniform(x0 + 0.18, x1 - 0.18)
        py = rng.uniform(lane_y0, lane_y1)
        vx = rng.uniform(0.70, 1.15)
        d.move_to([px, py, 0])
        dots.add(d)
        specs.append([px, py, vx])

    def update_stream(mob, dt):
        sp = float(speed_tracker.get_value())
        w = (x1 - 0.18) - (x0 + 0.18)
        for d, s in zip(mob, specs):
            s[0] += s[2] * sp * dt
            if s[0] > x1 - 0.18:
                s[0] -= w
            d.move_to([s[0], s[1], 0])

    dots.add_updater(update_stream)
    dots.set_z_index(1)
    dots.specs = specs
    return dots


def make_vertical_flow(x, y_start, y_end, color=YELLOW, ring_color=None, n=4,
                       rate_tracker=None, seed=11, radius=0.062, spread_x=0.14, x_end=None):
    """Computed stream of dots along a vertical or angled path."""
    rng = np.random.default_rng(seed)
    if rate_tracker is None:
        rate_tracker = ValueTracker(1.0)
    if x_end is None:
        x_end = x
    dx = x_end - x
    dy = y_end - y_start
    dots = VGroup()
    state = []
    for i in range(n):
        kw = {"radius": radius, "color": color, "fill_opacity": 0.95}
        if ring_color:
            kw.update(stroke_color=ring_color, stroke_width=3.0)
        d = Dot(**kw)
        prog = (i / max(n, 1) + rng.uniform(0, 0.15)) % 1.0
        ox = rng.uniform(-spread_x, spread_x)
        d.move_to([x + prog * dx + ox, y_start + prog * dy, 0])
        dots.add(d)
        state.append([prog, ox, rng.uniform(0.55, 0.85)])

    def upd(mob, dt):
        r = float(rate_tracker.get_value())
        active_n = int(round(np.clip(r, 0.0, 1.5) * n))
        for idx, (d, st) in enumerate(zip(mob, state)):
            if idx >= active_n or r <= 0.02:
                d.set_opacity(0.0)
                continue
            d.set_opacity(0.95)
            st[0] = (st[0] + st[2] * max(0.35, r) * dt) % 1.0
            d.move_to([x + st[0] * dx + st[1], y_start + st[0] * dy, 0])

    dots.add_updater(upd)
    dots.set_z_index(1)
    return dots


def make_transporter_doors(xs, y_surface, y_inside, open_tracker, width=0.28, height=0.14):
    """BLUE transporter doors along muscle-and-fat top edge: open_tracker (0..1) raises doors to surface."""
    doors = VGroup()
    n = len(xs)
    for idx, x in enumerate(xs):
        thresh = idx / max(n, 1)

        def mk_door(x=x, thresh=thresh):
            frac = float(np.clip((open_tracker.get_value() - thresh * 0.6) / 0.4, 0.0, 1.0))
            cy = y_inside + frac * (y_surface - y_inside)
            r = RoundedRectangle(width=width, height=height, corner_radius=0.04,
                                 stroke_color=BLUE, stroke_width=2.5,
                                 fill_color=BLUE, fill_opacity=0.35 + 0.55 * frac)
            r.move_to([x, cy, 0])
            return r

        doors.add(always_redraw(mk_door))
    return doors


def build_base_world(
    blood_x=(-5.7, 0.55),
    blood_y=(-0.55, 0.55),
    mf_y=(-2.50, -1.35),
    gauge_x=1.85,
    gauge_y=0.05,
    gauge_h=2.10,
    glucose_lvl=0.30,
    doors_open=0.45,
    show_too_high=False,
    show_basal=False,
    n_glucose=18,
    n_cyan=0,
    n_tracer=0,
    seed=7,
):
    """Build the carried world components in consistent coordinates."""
    bx0, bx1 = blood_x
    by0, by1 = blood_y
    bw = bx1 - bx0
    bh = by1 - by0
    bcx, bcy = (bx0 + bx1) / 2, (by0 + by1) / 2

    blood_box = RoundedRectangle(
        width=bw, height=bh, corner_radius=0.18,
        stroke_color=GREY, stroke_width=3.0, fill_color=GREY, fill_opacity=0.15
    ).move_to([bcx, bcy, 0])
    blood_lbl = T("blood", size=24, color=TEXT).move_to([bx0 + 0.55, by1 - 0.22, 0]).set_z_index(5)

    mf_bot, mf_top = mf_y
    mf_h = mf_top - mf_bot
    mf_box = RoundedRectangle(
        width=bw, height=mf_h, corner_radius=0.14,
        stroke_color=GREY, stroke_width=3.0, fill_color=GREY, fill_opacity=0.18
    ).move_to([bcx, (mf_bot + mf_top) / 2, 0])
    mf_lbl = T("muscle and fat", size=26, color=TEXT).move_to([bcx, mf_bot + 0.30, 0]).set_z_index(5)

    g_tracker = ValueTracker(glucose_lvl)
    speed_tracker = ValueTracker(1.0)
    doors_tracker = ValueTracker(doors_open)

    door_xs = np.linspace(bx0 + 0.7, bx1 - 0.7, 6)
    doors = make_transporter_doors(door_xs, y_surface=mf_top, y_inside=mf_bot + 0.72, open_tracker=doors_tracker)

    stream = make_blood_stream(bx0, bx1, by0, by1, n_glucose=n_glucose, n_cyan=n_cyan,
                               n_tracer=n_tracer, speed_tracker=speed_tracker, seed=seed)

    gauge = make_gauge([gauge_x, gauge_y, 0], height=gauge_h, level_tracker=g_tracker,
                       fill_color=YELLOW, label="blood glucose", label_size=24,
                       show_too_high=show_too_high, show_basal=show_basal)

    return {
        "blood_box": blood_box,
        "blood_lbl": blood_lbl,
        "mf_box": mf_box,
        "mf_lbl": mf_lbl,
        "doors": doors,
        "stream": stream,
        "gauge": gauge,
        "g_tracker": g_tracker,
        "speed_tracker": speed_tracker,
        "doors_tracker": doors_tracker,
        "bx0": bx0, "bx1": bx1, "by0": by0, "by1": by1,
        "mf_top": mf_top, "mf_bot": mf_bot,
    }


def make_axis_bars(x_axis, y_bot, y_top, max_val=7.0, label="mg per kg per min", label_size=22):
    """Shared vertical axis 0..max_val for clamp bar charts (s07, s09, s10)."""
    ax = Line([x_axis, y_bot, 0], [x_axis, y_top, 0], color=GREY, stroke_width=2.8)
    base = Line([x_axis, y_bot, 0], [x_axis + 1.95, y_bot, 0], color=GREY, stroke_width=2.8)
    ticks = VGroup()
    tlabels = VGroup()
    for v in (0, 2, 4, 6):
        py = y_bot + (v / max_val) * (y_top - y_bot)
        ticks.add(Line([x_axis - 0.08, py, 0], [x_axis, py, 0], color=GREY, stroke_width=2.5))
        tl = M(f"{v}", size=22, color=TEXT).next_to([x_axis - 0.08, py, 0], LEFT, buff=0.08)
        tlabels.add(tl)
    ulbl = T(label, size=label_size, color=TEXT).next_to(base, DOWN, buff=0.16)
    g = VGroup(ax, base, ticks, tlabels, ulbl)
    g.g_y_bot = y_bot
    g.g_y_top = y_top
    g.max_val = max_val
    return g


def make_live_bar(x, y_bot, y_top, max_val, val_tracker, color, width=0.44,
                  base_tracker=None, show_num=True, num_fmt="{:.2f}", num_size=22):
    """Bar driven by ValueTracker, optionally stacked on base_tracker, with agreeing number."""
    def mk_bar():
        v = max(0.0, float(val_tracker.get_value()))
        b = max(0.0, float(base_tracker.get_value())) if base_tracker is not None else 0.0
        if v < 0.02:
            return VGroup()
        yb = y_bot + (b / max_val) * (y_top - y_bot)
        yt = y_bot + ((b + v) / max_val) * (y_top - y_bot)
        h = max(0.03, yt - yb)
        r = Rectangle(width=width, height=h, stroke_color=color, stroke_width=2.5,
                      fill_color=color, fill_opacity=0.82)
        r.move_to([x, yb + h / 2, 0])
        return r

    bar = always_redraw(mk_bar)
    if not show_num:
        return bar, VGroup()

    def mk_num():
        v = max(0.0, float(val_tracker.get_value()))
        b = max(0.0, float(base_tracker.get_value())) if base_tracker is not None else 0.0
        if v < 0.02:
            return VGroup()
        yt = y_bot + ((b + v) / max_val) * (y_top - y_bot)
        txt = M(num_fmt.format(b + v if base_tracker is not None and color == TEXT else v),
                size=num_size, color=color)
        txt.move_to([x, yt + 0.22, 0])
        return txt

    num = always_redraw(mk_num)
    return bar, num


# ---------------------------------------------------------------------------
# Scene 0: s00_link_and_question (18.2 s)
# ---------------------------------------------------------------------------
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        islet = make_islet([0.0, 0.9, 0], scale=1.6)
        rule_row = T("glucose -> metabolism -> electrical signal -> insulin", size=26, color=TEXT).move_to([0.0, -0.45, 0])
        burn_rate = ValueTracker(1.2)
        burn_dots = make_vertical_flow(0.0, 0.45, 1.35, color=YELLOW, n=5, rate_tracker=burn_rate,
                                       seed=1, radius=0.07, spread_x=0.35)
        self.add(islet, burn_dots, rule_row)
        self.play(FadeIn(islet, shift=UP * 0.1), FadeIn(rule_row), run_time=0.6)

        w = build_base_world(
            blood_x=(-5.7, 0.55), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=1.85, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.30, doors_open=0.35, show_too_high=True, n_glucose=18, seed=7
        )
        liver = make_liver([-4.35, 1.75, 0], width=1.6, height=0.88, label_size=26)
        liver_rate = ValueTracker(0.9)
        liver_arrow = always_redraw(lambda: Arrow(
            [-4.35, 1.28, 0], [-4.35, 0.58, 0], buff=0.04,
            color=YELLOW, stroke_width=2.5 + 3.5 * liver_rate.get_value(), max_tip_length_to_length_ratio=0.30
        ))
        liver_dots = make_vertical_flow(-4.35, 1.24, 0.62, color=YELLOW, n=3, rate_tracker=liver_rate, seed=2)

        exit_rate = ValueTracker(0.5)
        exit_dots = make_vertical_flow(-2.55, -0.58, -1.35, color=YELLOW, n=5, rate_tracker=exit_rate,
                                       seed=3, spread_x=1.5)

        ins_rate = ValueTracker(1.0)
        ins_stream = make_vertical_flow(0.1, 1.38, -1.25, color=PURPLE, n=6, rate_tracker=ins_rate,
                                        seed=5, radius=0.058, spread_x=0.30)

        self.at("releases insulin")
        self.remove(burn_dots)
        rule_small = T("glucose -> metabolism -> electrical signal -> insulin", size=22, color=TEXT)
        rule_small.move_to([6.25 - rule_small.width / 2, 3.25, 0]).set_z_index(5)
        self.play(
            islet.animate.scale(1.0 / 1.6).move_to([0.1, 1.78, 0]),
            ReplacementTransform(rule_row, rule_small),
            FadeIn(w["blood_box"]), FadeIn(w["blood_lbl"]),
            FadeIn(w["mf_box"]), FadeIn(w["mf_lbl"]),
            FadeIn(w["doors"]), FadeIn(w["gauge"]),
            FadeIn(liver), FadeIn(liver_arrow),
            run_time=1.3
        )
        self.add(w["stream"], liver_dots, exit_dots, ins_stream)

        self.at("act on")
        ins_to_l = make_vertical_flow(-0.3, 1.32, 1.12, x_end=-3.6, color=PURPLE, n=4,
                                      rate_tracker=ins_rate, seed=6, radius=0.055, spread_x=0.06)
        self.add(ins_to_l)
        self.play(
            liver_rate.animate.set_value(0.35),
            w["doors_tracker"].animate.set_value(0.95),
            exit_rate.animate.set_value(1.1),
            run_time=1.6
        )

        self.at("climbs too high")
        cup = make_cup([-2.05, 1.85, 0], label="glucose drink", label_size=24)
        drink_rate = ValueTracker(1.2)
        drink_dots = make_vertical_flow(-2.05, 1.38, 0.58, color=YELLOW, n=6, rate_tracker=drink_rate,
                                        seed=8, radius=0.068, spread_x=0.14)
        self.play(FadeIn(cup, shift=DOWN * 0.1), run_time=0.5)
        self.add(drink_dots)
        self.play(
            w["g_tracker"].animate.set_value(0.86),
            w["speed_tracker"].animate.set_value(1.45),
            run_time=2.0
        )

        self.at("too little insulin")
        q1_box = boxed_label("too little insulin?", PURPLE, size=26, pad=0.20)
        q1_dots = VGroup(*[Dot(radius=0.055, color=PURPLE, fill_opacity=0.35).shift(RIGHT * i * 0.22) for i in range(3)])
        q1_dots.next_to(q1_box, DOWN, buff=0.14)
        q1 = VGroup(q1_box, q1_dots).move_to([4.85, 1.25, 0])
        self.play(FadeIn(q1, shift=LEFT * 0.15), run_time=0.7)

        self.at("works too weakly")
        q2_box = boxed_label("weak response?", BLUE, size=26, pad=0.20)
        q2_bar = Line(LEFT * 0.65, RIGHT * 0.65, color=GREY, stroke_width=3.0)
        q2_door = RoundedRectangle(width=0.26, height=0.13, corner_radius=0.04,
                                   stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.85).move_to(q2_bar)
        q2_icon = VGroup(q2_bar, q2_door).next_to(q2_box, DOWN, buff=0.18)
        q2 = VGroup(q2_box, q2_icon).move_to([4.85, -0.55, 0])
        self.play(FadeIn(q2, shift=LEFT * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 1: s01_title (2.0 s silent)
# ---------------------------------------------------------------------------
class S01Title(NarratedScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-5.7, 0.55), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=1.85, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.86, doors_open=0.85, show_too_high=True, n_glucose=20, seed=7
        )
        w["speed_tracker"].set_value(1.4)
        liver = make_liver([-4.35, 1.75, 0], width=1.6, height=0.88, label_size=26)
        cup = make_cup([-2.05, 1.85, 0], label="glucose drink", label_size=24)
        islet = make_islet([0.1, 1.78, 0], scale=1.0)
        liver_dots = make_vertical_flow(-4.35, 1.24, 0.62, color=YELLOW, n=3,
                                        rate_tracker=ValueTracker(0.4), seed=2)
        drink_dots = make_vertical_flow(-2.05, 1.38, 0.58, color=YELLOW, n=6,
                                        rate_tracker=ValueTracker(1.0), seed=8, radius=0.068)
        exit_dots = make_vertical_flow(-2.55, -0.58, -1.35, color=YELLOW, n=5,
                                       rate_tracker=ValueTracker(0.9), seed=3, spread_x=1.5)

        q1 = boxed_label("too little insulin?", PURPLE, size=26, pad=0.20).move_to([4.85, 1.25, 0])
        q2 = boxed_label("weak response?", BLUE, size=26, pad=0.20).move_to([4.85, -0.55, 0])
        q1_s = boxed_label("too little insulin?", PURPLE, size=22, pad=0.14).move_to([5.05, 1.15, 0])
        q2_s = boxed_label("weak response?", BLUE, size=22, pad=0.14).move_to([5.05, -0.15, 0])

        title = T("Holding Glucose Still", size=44, font=TITLE_FONT, color=TEXT).move_to([0, 3.22, 0])
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.10)

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"],
            liver, cup, islet, liver_dots, drink_dots, exit_dots, q1, q2
        )
        self.play(
            FadeIn(title, shift=DOWN * 0.12), GrowFromCenter(rule),
            ReplacementTransform(q1, q1_s),
            ReplacementTransform(q2, q2_s),
            run_time=0.9
        )
        self.finish()


# ---------------------------------------------------------------------------
# Scene 2: s02_curve (20.825 s)
# ---------------------------------------------------------------------------
class S02Curve(SpokenScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-5.8, -0.55), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=0.75, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.30, doors_open=0.55, show_too_high=False, n_glucose=18, seed=7
        )
        liver = make_liver([-4.55, 1.75, 0], width=1.45, height=0.84, label_size=24)
        cup = make_cup([-2.45, 1.85, 0], label="glucose drink", label_size=22)
        islet = make_islet([-0.75, 1.75, 0], scale=0.95)

        drink_rate = ValueTracker(0.0)
        liver_rate = ValueTracker(0.6)
        ins_rate = ValueTracker(0.6)
        exit_rate = ValueTracker(0.6)

        drink_dots = make_vertical_flow(-2.45, 1.38, 0.58, color=YELLOW, n=6, rate_tracker=drink_rate, seed=8, radius=0.065)
        liver_dots = make_vertical_flow(-4.55, 1.28, 0.60, color=YELLOW, n=3, rate_tracker=liver_rate, seed=2)
        ins_dots = make_vertical_flow(-0.75, 1.35, -1.28, color=PURPLE, n=5, rate_tracker=ins_rate, seed=5, radius=0.055, spread_x=0.22)
        exit_dots = make_vertical_flow(-3.15, -0.58, -1.35, color=YELLOW, n=5, rate_tracker=exit_rate, seed=3, spread_x=1.4)

        P = Plot(box=(2.30, 6.20, -1.75, 1.85), xr=(0, 2), yr=(80, 200),
                 xticks=[0, 1, 2], yticks=[(80, "80"), (140, "140"), (160, "160"), (200, "200")],
                 xlabel="hours", ylabel="mg/dL", size=22, label_size=24)
        b_lo = P.pt(0, 140)[1]
        b_hi = P.pt(2, 160)[1]
        band = Rectangle(width=P.x1 - P.x0, height=b_hi - b_lo, stroke_width=0,
                         fill_color=YELLOW, fill_opacity=0.14).move_to([(P.x0 + P.x1) / 2, (b_lo + b_hi) / 2, 0])
        h140 = P.hline(140, color=GREY, dashed=True)

        t_tr = ValueTracker(0.0)
        w["g_tracker"].add_updater(lambda tr: tr.set_value(
            np.clip(0.15 + (ogtt_healthy(t_tr.get_value()) - 80.0) / 120.0 * 0.80, 0.10, 0.95)
        ))
        live = P.live_curve(ogtt_healthy, t_tr, color=YELLOW, width=5.5)
        dot = P.dot(lambda: t_tr.get_value(), lambda: ogtt_healthy(t_tr.get_value()), color=YELLOW, ring=TEXT, radius=0.10)

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"], w["g_tracker"],
            liver, cup, islet, drink_dots, liver_dots, ins_dots, exit_dots
        )
        self.play(Create(P), FadeIn(band), FadeIn(h140), run_time=1.0)
        self.add(live, dot, scope_tag("peak timing schematic"))

        self.at("75 grams")
        dose_tag = T("75 g", size=22, color=YELLOW).next_to(cup[0], LEFT, buff=0.16)
        self.play(FadeIn(dose_tag), drink_rate.animate.set_value(1.2), run_time=0.5)

        self.at("blood glucose readings")
        self.play(
            t_tr.animate.set_value(0.85),
            ins_rate.animate.set_value(1.1),
            w["doors_tracker"].animate.set_value(0.90),
            exit_rate.animate.set_value(1.05),
            run_time=4.5, rate_func=linear
        )

        self.at("140 to 160")
        healthy_tag = T("healthy (shape schematic)", size=22, color=YELLOW).move_to([4.95, 2.42, 0])
        self.play(
            t_tr.animate.set_value(2.0),
            drink_rate.animate.set_value(0.35),
            FadeIn(healthy_tag),
            run_time=3.8, rate_func=linear
        )

        self.at("blends three things")
        self.at("absorption")
        lbl_abs = boxed_label("absorption", YELLOW, size=22, pad=0.12).move_to([-2.45, 3.08, 0])
        self.play(FadeIn(lbl_abs), run_time=0.35)

        self.at("insulin secretion")
        lbl_sec = boxed_label("secretion", PURPLE, size=22, pad=0.12).move_to([-0.65, 3.08, 0])
        self.play(FadeIn(lbl_sec), run_time=0.35)

        self.at("insulin action")
        lbl_act = boxed_label("action", BLUE, size=22, pad=0.12).move_to([-3.15, -3.05, 0])
        # Clean arrow routed well below the '80' and '0' axis ticks into the x-axis
        arr_c = CurvedArrow(lbl_act.get_right() + RIGHT * 0.08, [3.45, -1.82, 0], angle=0.28,
                            color=BLUE, stroke_width=2.5)
        self.play(FadeIn(lbl_act), Create(arr_c), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 3: s03_two_faults (21.5 s)
# ---------------------------------------------------------------------------
class S03TwoFaults(SpokenScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-5.8, -0.55), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=0.75, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.22, doors_open=0.85, show_too_high=False, n_glucose=18, seed=7
        )
        liver = make_liver([-4.55, 1.75, 0], width=1.45, height=0.84, label_size=24)
        cup = make_cup([-2.45, 1.85, 0], label="glucose drink", label_size=22)
        islet = make_islet([-0.75, 1.75, 0], scale=0.95)

        liver_rate = ValueTracker(0.45)
        liver_arrow = always_redraw(lambda: Arrow(
            [-4.55, 1.28, 0], [-4.55, 0.58, 0], buff=0.04,
            color=YELLOW, stroke_width=2.5 + 4.5 * liver_rate.get_value(), max_tip_length_to_length_ratio=0.30
        ))
        ins_rate = ValueTracker(0.95)
        exit_rate = ValueTracker(0.95)
        drink_rate = ValueTracker(0.95)

        drink_dots = make_vertical_flow(-2.45, 1.38, 0.58, color=YELLOW, n=5, rate_tracker=drink_rate, seed=8, radius=0.065)
        liver_dots = make_vertical_flow(-4.55, 1.26, 0.60, color=YELLOW, n=4, rate_tracker=liver_rate, seed=2)
        ins_dots = make_vertical_flow(-0.75, 1.35, -1.28, color=PURPLE, n=6, rate_tracker=ins_rate, seed=5, radius=0.055, spread_x=0.22)
        exit_dots = make_vertical_flow(-3.15, -0.58, -1.35, color=YELLOW, n=6, rate_tracker=exit_rate, seed=3, spread_x=1.4)

        P = Plot(box=(2.30, 6.20, -1.75, 1.85), xr=(0, 2), yr=(80, 200),
                 xticks=[0, 1, 2], yticks=[(80, "80"), (140, "140"), (160, "160"), (200, "200")],
                 xlabel="hours", ylabel="mg/dL", size=22, label_size=24)
        healthy_c = P.curve(ogtt_healthy, color=YELLOW, width=4.0, opacity=0.65)
        healthy_lbl = T("healthy", size=22, color=YELLOW).move_to(P.pt(1.55, 118))

        t1 = ValueTracker(0.0)
        t2 = ValueTracker(0.0)
        run_mode = ValueTracker(1.0)

        def sync_gauge(tr):
            val = ogtt_less_secretion(t1.get_value()) if run_mode.get_value() < 1.5 else ogtt_weaker_action(t2.get_value())
            tr.set_value(np.clip(0.15 + (val - 80.0) / 120.0 * 0.80, 0.10, 0.96))

        w["g_tracker"].add_updater(sync_gauge)

        c_sec = P.live_curve(ogtt_less_secretion, t1, color=PURPLE, width=5.5)
        d_sec = P.dot(lambda: t1.get_value(), lambda: ogtt_less_secretion(t1.get_value()), color=PURPLE, ring=TEXT, radius=0.09)

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"], w["g_tracker"],
            liver, liver_arrow, cup, islet,
            drink_dots, liver_dots, ins_dots, exit_dots,
            P, healthy_c, healthy_lbl, c_sec, d_sec, scope_tag("curves schematic")
        )

        self.at("reduce secretion")
        self.play(ins_rate.animate.set_value(0.25), run_time=0.8)

        self.at("muscle and fat")
        self.play(w["doors_tracker"].animate.set_value(0.25), exit_rate.animate.set_value(0.35), run_time=0.9)

        self.at("liver releases more")
        self.play(liver_rate.animate.set_value(1.25), t1.animate.set_value(0.95), run_time=2.0, rate_func=linear)

        self.at("climbs higher")
        lbl_sec = T("less secretion", size=22, color=PURPLE).move_to([4.75, 2.64, 0])
        self.play(t1.animate.set_value(2.0), FadeIn(lbl_sec), run_time=1.8, rate_func=linear)
        self.remove(d_sec)

        self.at("hold insulin constant")
        run_mode.set_value(2.0)
        self.play(ins_rate.animate.set_value(1.0), run_time=0.9)

        self.at("weaken its action")
        c_act_pts = [P.pt(x, ogtt_weaker_action(x)) for x in np.linspace(0, 2.0, 80)]
        c_act_full = DashedVMobject(VMobject(stroke_color=BLUE, stroke_width=5.0).set_points_as_corners(c_act_pts),
                                    num_dashes=26)
        self.play(Create(c_act_full), t2.animate.set_value(2.0), run_time=2.2, rate_func=linear)

        self.at("same directions")
        lbl_act = T("weaker action (dashed)", size=22, color=BLUE).move_to([4.75, 3.08, 0])
        self.play(FadeIn(lbl_act), c_sec.animate.set_stroke(width=7.5), run_time=0.6)
        self.play(c_sec.animate.set_stroke(width=5.5), run_time=0.5)

        self.at("type 2 diabetes")
        # Place cleanly above peak well clear of 'less secretion' and curves
        t2_tag = boxed_label("type 2: often both", TEXT, size=22, pad=0.10).move_to([4.65, 2.08, 0])
        self.play(FadeIn(t2_tag), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 4: s04_balance (18.15 s)
# ---------------------------------------------------------------------------
class S04Balance(SpokenScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-4.5, 0.70), blood_y=(-0.55, 0.55), mf_y=(-2.55, -1.45),
            gauge_x=1.85, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.35, doors_open=0.65, show_too_high=False, n_glucose=18, seed=7
        )
        liver = make_liver([-3.7, 1.85, 0], width=1.45, height=0.82, label_size=24)
        cup = make_cup([-1.7, 1.90, 0], label="glucose drink", label_size=22)

        in_w = ValueTracker(0.32)
        out_w = ValueTracker(0.32)

        in_arrow = always_redraw(lambda: Arrow(
            [-6.05, 0.0, 0], [-4.55, 0.0, 0], buff=0.0,
            color=YELLOW, stroke_width=28 * in_w.get_value(),
            max_tip_length_to_length_ratio=0.35
        ))
        in_lbl = T("in", size=28, color=YELLOW).next_to([-5.35, 0.28, 0], UP, buff=0.14)

        out_arrow = always_redraw(lambda: Arrow(
            [-1.9, -0.58, 0], [-1.9, -1.42, 0], buff=0.0,
            color=YELLOW, stroke_width=28 * out_w.get_value(),
            max_tip_length_to_length_ratio=0.45
        ))
        out_lbl = T("out", size=28, color=YELLOW).next_to([-1.35, -1.0, 0], RIGHT, buff=0.14)

        exit_dots = make_vertical_flow(-2.65, -0.58, -1.40, color=YELLOW, n=5,
                                       rate_tracker=ValueTracker(0.75), seed=13, spread_x=0.8)

        inset_box = RoundedRectangle(width=3.6, height=2.1, corner_radius=0.12,
                                     stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to([4.4, 2.05, 0])
        inset_p = Plot(box=(2.95, 5.95, 1.25, 2.75), xr=(0, 2), yr=(80, 200), xticks=[], yticks=[], stroke=2.5)
        ic_healthy = inset_p.curve(ogtt_healthy, color=YELLOW, width=3.0, opacity=0.65)
        ic_fault = inset_p.curve(ogtt_less_secretion, color=PURPLE, width=3.5)
        ic_weak = DashedVMobject(inset_p.curve(ogtt_weaker_action, color=BLUE, width=3.5), num_dashes=16)
        inset = VGroup(inset_box, inset_p, ic_healthy, ic_fault, ic_weak)

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"], exit_dots,
            liver, cup, in_arrow, in_lbl, out_arrow, out_lbl, inset
        )

        self.at("holds steady")
        eq_lbl = T("in = out: level holds", size=30, color=TEXT).move_to([-1.9, 3.05, 0])
        self.play(FadeIn(eq_lbl), run_time=0.6)

        self.at("equals glucose leaving")
        self.wait(0.8)

        self.at("entry runs ahead")
        climb_lbl = T("in > out: level climbs", size=30, color=YELLOW).move_to([-1.9, 3.05, 0])
        self.play(
            swap(eq_lbl, climb_lbl, run_time=0.5),
            in_w.animate.set_value(0.75),
            out_w.animate.set_value(0.22),
            w["g_tracker"].animate.set_value(0.85),
            w["speed_tracker"].animate.set_value(1.4),
            run_time=2.2
        )

        self.at("not which fault")
        q1 = boxed_label("too little insulin?", PURPLE, size=24, pad=0.16).move_to([4.45, -0.15, 0])
        q2 = boxed_label("weak response?", BLUE, size=24, pad=0.16).move_to([4.45, -1.05, 0])
        self.play(FadeIn(q1, shift=UP * 0.1), FadeIn(q2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 5: s05_clamps (23.5 s)
# ---------------------------------------------------------------------------
class S05Clamps(SpokenScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-4.6, 0.70), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=2.25, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.72, doors_open=0.45, show_too_high=False, show_basal=True, n_glucose=18, seed=7
        )
        liver = make_liver([-0.55, 1.80, 0], width=1.50, height=0.84, label_size=24)
        cup = make_cup([-2.75, 1.85, 0], label="glucose drink", label_size=22)
        islet = make_islet([1.35, 1.80, 0], scale=0.95)

        inset_box = RoundedRectangle(width=3.2, height=1.8, corner_radius=0.12,
                                     stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to([4.5, 2.25, 0])
        inset_p = Plot(box=(3.15, 5.85, 1.55, 2.90), xr=(0, 2), yr=(80, 200), xticks=[], yticks=[], stroke=2.5)
        inset_c = inset_p.curve(ogtt_less_secretion, color=PURPLE, width=3.5)
        inset = VGroup(inset_box, inset_p, inset_c)

        ins_rate = ValueTracker(0.4)
        ins_dots = make_vertical_flow(1.35, 1.40, -1.28, color=PURPLE, n=7, rate_tracker=ins_rate,
                                      seed=5, radius=0.058, spread_x=0.35)
        exit_rate = ValueTracker(0.5)
        exit_dots = make_vertical_flow(-1.95, -0.58, -1.35, color=YELLOW, n=6, rate_tracker=exit_rate,
                                       seed=3, spread_x=2.0)

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"],
            liver, cup, islet, inset, ins_dots, exit_dots
        )

        self.at("hold glucose still")
        bracket = make_clamp_bracket(w["gauge"], w["g_tracker"], label="held")
        self.play(FadeOut(cup), FadeIn(bracket), run_time=0.8)

        self.at("hyperglycemic clamp")
        beta_tag = T("beta cell's side", size=24, color=PURPLE).next_to(islet, UP, buff=0.14)
        self.play(w["g_tracker"].animate.set_value(0.84), ins_rate.animate.set_value(1.25), run_time=1.8)

        self.at("beta cells side")
        self.play(FadeIn(beta_tag), run_time=0.6)

        self.at("second clamp")
        self.remove(ins_dots)
        self.play(
            FadeOut(inset), FadeOut(islet), FadeOut(beta_tag),
            w["g_tracker"].animate.set_value(0.30),
            run_time=1.6
        )

        self.at("raised plateau")
        ins_lvl = ValueTracker(0.15)
        ins_gauge = make_gauge([-5.65, 0.05, 0], height=2.10, level_tracker=ins_lvl,
                               fill_color=PURPLE, label="insulin:\nraised plateau", label_size=22)
        ins_bath = make_vertical_flow(-1.95, 0.55, -1.30, color=PURPLE, n=8,
                                      rate_tracker=ValueTracker(1.0), seed=15, radius=0.055, spread_x=2.2)
        self.play(FadeIn(ins_gauge), run_time=0.5)
        self.add(ins_bath)
        self.play(
            ins_lvl.animate.set_value(0.82),
            w["doors_tracker"].animate.set_value(0.95),
            exit_rate.animate.set_value(1.15),
            run_time=1.8
        )

        self.at("pump adds glucose")
        dial_tr = ValueTracker(0.5)
        pump = make_pump([-3.25, 1.95, 0], dial_tracker=dial_tr, label="pump", label_size=24)
        pump_line = Line([-3.25, 1.52, 0], [-3.25, 0.55, 0], color=CYAN, stroke_width=3.5)
        pump_dots = make_vertical_flow(-3.25, 1.48, 0.58, color=YELLOW, ring_color=CYAN, n=5,
                                       rate_tracker=ValueTracker(1.1), seed=19, radius=0.068, spread_x=0.10)
        cyan_stream = make_blood_stream(-4.6, 0.70, -0.55, 0.55, n_glucose=10, n_cyan=10,
                                        speed_tracker=w["speed_tracker"], seed=21)
        self.remove(w["stream"])
        self.add(cyan_stream)
        self.play(FadeIn(pump), Create(pump_line), run_time=0.7)
        self.add(pump_dots)

        self.at("repeated measurements")
        fb_loop = VGroup(
            Line([2.25, 1.15, 0], [2.25, 2.95, 0], color=CYAN, stroke_width=2.5),
            Line([2.25, 2.95, 0], [-3.25, 2.95, 0], color=CYAN, stroke_width=2.5),
            Arrow([-3.25, 2.95, 0], [-3.25, 2.40, 0], buff=0.0, color=CYAN, stroke_width=2.5, max_tip_length_to_length_ratio=0.35),
        )
        dial_tr._t = 0.0
        dial_tr.add_updater(lambda tr, dt: (setattr(tr, "_t", tr._t + dt), tr.set_value(0.5 + 0.25 * np.sin(4.5 * tr._t))))
        self.add(dial_tr)
        self.play(Create(fb_loop), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 6: s06_rule (19.725 s)
# ---------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-4.6, 0.65), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=1.80, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.30, doors_open=0.95, show_too_high=False, show_basal=False,
            n_glucose=10, n_cyan=10, seed=21
        )
        ins_lvl = ValueTracker(0.82)
        ins_gauge = make_gauge([-5.65, 0.05, 0], height=2.10, level_tracker=ins_lvl,
                               fill_color=PURPLE, label="insulin", label_size=24)
        dial_tr = ValueTracker(0.5)
        dial_tr._t = 0.0
        dial_tr.add_updater(lambda tr, dt: (setattr(tr, "_t", tr._t + dt), tr.set_value(0.5 + 0.22 * np.sin(4.0 * tr._t))))
        pump = make_pump([-3.25, 1.95, 0], dial_tracker=dial_tr, label="pump", label_size=24)
        pump_line = Line([-3.25, 1.52, 0], [-3.25, 0.55, 0], color=CYAN, stroke_width=3.5)
        liver = make_liver([-0.55, 1.80, 0], width=1.45, height=0.82, label_size=24)
        liver_arrow = Arrow([-0.55, 1.34, 0], [-0.55, 0.55, 0], buff=0.04, color=MAGENTA, stroke_width=3.0,
                            max_tip_length_to_length_ratio=0.35)
        bracket = make_clamp_bracket(w["gauge"], w["g_tracker"], label="held")

        pump_dots = make_vertical_flow(-3.25, 1.48, 0.58, color=YELLOW, ring_color=CYAN, n=5,
                                       rate_tracker=ValueTracker(1.1), seed=19, radius=0.068)
        liver_dots = make_vertical_flow(-0.55, 1.30, 0.58, color=MAGENTA, n=3,
                                        rate_tracker=ValueTracker(0.45), seed=22, radius=0.055)
        exit_dots = make_vertical_flow(-1.95, -0.58, -1.35, color=YELLOW, n=6,
                                       rate_tracker=ValueTracker(1.1), seed=3, spread_x=1.8)

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"], dial_tr,
            ins_gauge, pump, pump_line, liver, liver_arrow, bracket,
            pump_dots, liver_dots, exit_dots, scope_tag("bar heights schematic")
        )

        y_base = -1.65
        h_j = ValueTracker(0.0)
        h_egp = ValueTracker(0.0)
        h_rd = ValueTracker(0.0)

        bar_j = always_redraw(lambda: Rectangle(
            width=0.72, height=max(0.02, h_j.get_value()), stroke_color=CYAN, stroke_width=2.5,
            fill_color=CYAN, fill_opacity=0.80
        ).move_to([3.70, y_base + max(0.02, h_j.get_value()) / 2, 0]) if h_j.get_value() > 0.03 else VGroup())

        bar_egp = always_redraw(lambda: Rectangle(
            width=0.72, height=max(0.02, h_egp.get_value()), stroke_color=MAGENTA, stroke_width=2.5,
            fill_color=MAGENTA, fill_opacity=0.85
        ).move_to([3.70, y_base + h_j.get_value() + max(0.02, h_egp.get_value()) / 2, 0]) if h_egp.get_value() > 0.03 else VGroup())

        bar_rd = always_redraw(lambda: Rectangle(
            width=0.72, height=max(0.02, h_rd.get_value()), stroke_color=TEXT, stroke_width=2.5,
            fill_color=TEXT, fill_opacity=0.82
        ).move_to([5.45, y_base + max(0.02, h_rd.get_value()) / 2, 0]) if h_rd.get_value() > 0.03 else VGroup())

        self.add(bar_j, bar_egp, bar_rd)

        self.at("glucose in equals")
        eq_sign = M("=", size=42, color=TEXT).move_to([4.58, y_base + 1.35, 0])
        self.play(
            h_j.animate.set_value(2.05),
            h_egp.animate.set_value(0.55),
            h_rd.animate.set_value(2.60),
            FadeIn(eq_sign),
            run_time=2.2
        )

        self.at("disposal")
        lbl_rd = T("disposal (Rd):\nall tissues", size=22, color=TEXT).move_to([5.45, y_base - 0.55, 0])
        self.play(FadeIn(lbl_rd), run_time=0.6)

        self.at("equals the pump rate")
        lbl_j = T("pump (J)", size=22, color=CYAN).move_to([3.70, y_base - 0.42, 0])
        lbl_egp = T("body makes (EGP)", size=22, color=MAGENTA).move_to([4.25, y_base + 2.95, 0])
        eq_main = M("Rd = J + EGP", size=34, color=TEXT).move_to([4.55, 2.65, 0])
        self.play(FadeIn(lbl_j), FadeIn(lbl_egp), FadeIn(eq_main), run_time=1.0)

        self.at("mostly the liver")
        self.play(liver[0].animate.set_stroke(MAGENTA, 5.0), run_time=0.7)
        self.play(liver[0].animate.set_stroke(GREY, 3.0), run_time=0.6)

        self.at("lost in urine")
        urine_tag = T("urine loss negligible", size=22, color=GOLD).move_to([4.55, 2.08, 0])
        self.play(FadeIn(urine_tag), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------
# Shared builder for A vs B panels (s07_predict, s08_pause, s09_answer)
# ---------------------------------------------------------------------------
def build_ab_panels(j_a=5.71, j_b=2.86, egp_init=0.0, rd_a=0.0, rd_b=0.0, seed=31):
    """Build side-by-side simplified copies A and B for s07, s08, s09."""
    panels = []
    for idx, (name, x_center, j_val, rd_val) in enumerate((("A", -3.25, j_a, rd_a), ("B", 3.25, j_b, rd_b))):
        # Compact vertical frame y = -2.18 .. 2.48 leaves clean bottom band for ratio & zoom-in
        frame = RoundedRectangle(width=6.05, height=4.66, corner_radius=0.16,
                                 stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.25).move_to([x_center, 0.15, 0])
        head = T(name, size=32, color=TEXT, weight=BOLD).move_to([x_center - 2.45, 2.12, 0])
        same_ins = boxed_label("same insulin", PURPLE, size=22, pad=0.10).move_to([x_center - 0.85, 2.12, 0])

        bx0, bx1 = x_center - 2.75, x_center - 0.10
        by0, by1 = -0.60, 0.38
        blood = RoundedRectangle(width=bx1 - bx0, height=by1 - by0, corner_radius=0.12,
                                 stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.15).move_to([(bx0 + bx1) / 2, (by0 + by1) / 2, 0])
        b_lbl = T("blood", size=22, color=TEXT).move_to([bx0 + 0.48, by1 - 0.20, 0]).set_z_index(5)

        pump_x = x_center - 2.10
        dial_tr = ValueTracker(0.5)
        pump = make_pump([pump_x, 1.32, 0], dial_tracker=dial_tr, label="pump", label_size=22, scale=0.82)
        pump_line = Line([pump_x, 0.96, 0], [pump_x, by1, 0], color=CYAN, stroke_width=3.0)

        liver = make_liver([x_center - 0.55, 1.32, 0], width=1.18, height=0.66, label_size=22)

        g_tr = ValueTracker(0.32)
        gauge = make_gauge([x_center + 0.32, -0.08, 0], height=1.35, width=0.34, level_tracker=g_tr,
                           fill_color=YELLOW, label="basal", label_size=22)
        clamp_line = Line([x_center + 0.10, -0.32, 0], [x_center + 0.54, -0.32, 0], color=GOLD, stroke_width=3.5)

        mf = RoundedRectangle(width=bx1 - bx0, height=0.76, corner_radius=0.10,
                              stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.18).move_to([(bx0 + bx1) / 2, -1.66, 0])
        mf_lbl = T("muscle & fat", size=22, color=TEXT).move_to([mf.get_center()[0], -1.78, 0]).set_z_index(5)
        d_tr = ValueTracker(0.85 if name == "A" else 0.45)
        doors = make_transporter_doors(np.linspace(bx0 + 0.42, bx1 - 0.42, 4), y_surface=-1.28, y_inside=-1.56,
                                       open_tracker=d_tr, width=0.22, height=0.10)

        rate_f = 1.15 if name == "A" else 0.58
        p_rate = ValueTracker(rate_f)
        p_dots = make_vertical_flow(pump_x, 0.92, by1 + 0.06, color=YELLOW, ring_color=CYAN, n=4,
                                    rate_tracker=p_rate, seed=seed + idx, radius=0.055, spread_x=0.08)
        stream = make_blood_stream(bx0, bx1, by0, by1, n_glucose=8, n_cyan=8 if name == "A" else 4,
                                   speed_tracker=ValueTracker(1.2 if name == "A" else 0.75), seed=seed + 10 + idx)
        exit_dots = make_vertical_flow((bx0 + bx1) / 2, by0 - 0.02, -1.26, color=YELLOW,
                                       n=5 if name == "A" else 2, rate_tracker=ValueTracker(rate_f),
                                       seed=seed + 20 + idx, radius=0.052, spread_x=0.90)

        ax_x = x_center + 1.10
        y_bot, y_top = -1.52, 1.45
        axis = make_axis_bars(ax_x, y_bot, y_top, max_val=7.0, label="mg/kg/min", label_size=22)

        j_tr = ValueTracker(j_val)
        egp_tr = ValueTracker(egp_init)
        rd_tr = ValueTracker(rd_val)

        bar_j, num_j = make_live_bar(ax_x + 0.44, y_bot, y_top, 7.0, j_tr, CYAN, width=0.38, num_size=22)
        bar_egp, _ = make_live_bar(ax_x + 0.44, y_bot, y_top, 7.0, egp_tr, MAGENTA, width=0.38, base_tracker=j_tr, show_num=False)
        bar_rd, num_rd = make_live_bar(ax_x + 1.38, y_bot, y_top, 7.0, rd_tr, TEXT, width=0.38, num_size=22)

        grp = VGroup(frame, head, same_ins, blood, b_lbl, pump, pump_line, liver, gauge, clamp_line,
                     mf, mf_lbl, doors, p_dots, stream, exit_dots, axis, bar_j, num_j, bar_egp, bar_rd, num_rd)
        panels.append({
            "grp": grp, "frame": frame, "head": head, "liver": liver, "mf": mf,
            "j_tr": j_tr, "egp_tr": egp_tr, "rd_tr": rd_tr, "p_rate": p_rate, "dial_tr": dial_tr,
            "x_center": x_center, "ax_x": ax_x, "y_bot": y_bot, "y_top": y_top,
        })
    return panels


# ---------------------------------------------------------------------------
# Scene 7: s07_predict (19.5 s)
# ---------------------------------------------------------------------------
class S07Predict(SpokenScene):
    def construct(self):
        pA, pB = build_ab_panels(j_a=0.0, j_b=0.0, egp_init=0.65, seed=31)
        self.add(pA["grp"], pB["grp"])
        tag_data = T("made-up data", size=22, color=TEXT).move_to([-5.35, -3.15, 0])
        self.add(tag_data)

        self.at("same raised insulin")
        self.play(Indicate(pA["grp"][2], color=PURPLE), Indicate(pB["grp"][2], color=PURPLE), run_time=0.8)

        self.at("liver adds nothing")
        l0_a = T("liver: 0 (assumed)", size=22, color=MAGENTA).move_to([pA["liver"].get_center()[0] - 0.10, 0.76, 0])
        l0_b = T("liver: 0 (assumed)", size=22, color=MAGENTA).move_to([pB["liver"].get_center()[0] - 0.10, 0.76, 0])
        self.play(
            pA["egp_tr"].animate.set_value(0.0),
            pB["egp_tr"].animate.set_value(0.0),
            FadeIn(l0_a), FadeIn(l0_b),
            run_time=1.0
        )

        self.at("pump runs at")
        self.play(pA["j_tr"].animate.set_value(5.71), run_time=1.4)

        self.at("b's runs at")
        self.play(pB["j_tr"].animate.set_value(2.86), run_time=1.2)

        self.at("whose tissues")
        q = question_card("Whose tissues respond less?", y=3.15, color=TEXT, size=34)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 8: s08_pause (4.5 s silent)
# ---------------------------------------------------------------------------
class S08Pause(PredictPause):
    QUESTION = "Whose tissues respond less?"
    CARD = {"y": 3.15, "color": TEXT, "size": 34}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        pA, pB = build_ab_panels(j_a=5.71, j_b=2.86, egp_init=0.0, seed=31)
        l0_a = T("liver: 0 (assumed)", size=22, color=MAGENTA).move_to([pA["liver"].get_center()[0] - 0.10, 0.76, 0])
        l0_b = T("liver: 0 (assumed)", size=22, color=MAGENTA).move_to([pB["liver"].get_center()[0] - 0.10, 0.76, 0])
        tag_data = T("made-up data", size=22, color=TEXT).move_to([-5.35, -3.15, 0])
        return VGroup(pA["grp"], pB["grp"], l0_a, l0_b, tag_data)


# ---------------------------------------------------------------------------
# Scene 9: s09_answer (17.825 s)
# ---------------------------------------------------------------------------
class S09Answer(SpokenScene):
    def construct(self):
        pA, pB = build_ab_panels(j_a=5.71, j_b=2.86, egp_init=0.0, seed=31)
        l0_a = T("liver: 0 (assumed)", size=22, color=MAGENTA).move_to([pA["liver"].get_center()[0] - 0.10, 0.76, 0])
        l0_b = T("liver: 0 (assumed)", size=22, color=MAGENTA).move_to([pB["liver"].get_center()[0] - 0.10, 0.76, 0])
        tag_data = T("made-up data", size=22, color=TEXT).move_to([-5.35, -3.15, 0])
        q = question_card("Whose tissues respond less?", y=3.15, color=TEXT, size=34)
        self.add(pA["grp"], pB["grp"], l0_a, l0_b, tag_data, q)

        ans_b = T("B's tissues respond less", size=32, color=GOLD).move_to([0, 3.15, 0])
        self.play(swap(q, ans_b, run_time=0.6), pB["frame"].animate.set_stroke(GOLD, 3.5), run_time=0.9)

        self.at("pump rate is disposal")
        self.play(pA["rd_tr"].animate.set_value(5.71), pB["rd_tr"].animate.set_value(2.86), run_time=1.4)

        self.at("about half")
        ratio = M("2.86 / 5.71 = 0.50 (about half)", size=24, color=GOLD).move_to([-2.05, -2.72, 0])
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.7)

        self.at("not which step")
        # Clean zoom-in circle in the open bottom band below B's muscle & fat, linked by dashed lines
        zoom_ring = Circle(radius=0.52, stroke_color=RED, stroke_width=3.0, fill_color=BG, fill_opacity=0.95).move_to([1.85, -2.92, 0])
        cell_out = RoundedRectangle(width=0.72, height=0.46, corner_radius=0.10, stroke_color=GREY, stroke_width=2.5).move_to(zoom_ring)
        q_mark = T("?", size=30, color=RED, weight=BOLD).move_to(cell_out)
        defect_lbl = T("× defect not identified", size=22, color=RED).next_to(zoom_ring, RIGHT, buff=0.20)
        z_line1 = DashedLine([1.50, -2.06, 0], [1.45, -2.55, 0], color=RED, stroke_width=2.2, dash_length=0.08)
        z_line2 = DashedLine([2.20, -2.06, 0], [2.25, -2.55, 0], color=RED, stroke_width=2.2, dash_length=0.08)
        zoom = VGroup(z_line1, z_line2, zoom_ring, cell_out, q_mark, defect_lbl).set_z_index(8)
        self.play(FadeIn(zoom), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 10: s10_liver (15.8 s)
# ---------------------------------------------------------------------------
class S10Liver(SpokenScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-4.6, 0.65), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=1.80, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.30, doors_open=0.90, show_too_high=False, show_basal=False,
            n_glucose=10, n_cyan=10, seed=21
        )
        ins_lvl = ValueTracker(0.82)
        ins_gauge = make_gauge([-5.65, 0.05, 0], height=2.10, level_tracker=ins_lvl,
                               fill_color=PURPLE, label="insulin", label_size=24)
        dial_tr = ValueTracker(0.5)
        pump = make_pump([-3.25, 1.95, 0], dial_tracker=dial_tr, label="pump", label_size=24)
        pump_line = Line([-3.25, 1.52, 0], [-3.25, 0.55, 0], color=CYAN, stroke_width=3.5)
        liver = make_liver([-0.55, 1.80, 0], width=1.45, height=0.82, label_size=24)
        bracket = make_clamp_bracket(w["gauge"], w["g_tracker"], label="held")

        # Place 'liver: 0 (assumed)' cleanly to the right of liver, out of the trickle path
        l0_tag = T("liver: 0 (assumed)", size=22, color=MAGENTA).next_to(liver, RIGHT, buff=0.22)
        l0_cross = Line(l0_tag.get_left() + LEFT * 0.05, l0_tag.get_right() + RIGHT * 0.05, color=RED, stroke_width=3.5)
        l0_cross.layout_ok = True

        pump_dots = make_vertical_flow(-3.25, 1.48, 0.58, color=YELLOW, ring_color=CYAN, n=5,
                                       rate_tracker=ValueTracker(1.1), seed=19, radius=0.068)
        exit_dots = make_vertical_flow(-1.95, -0.58, -1.35, color=YELLOW, n=6,
                                       rate_tracker=ValueTracker(1.1), seed=3, spread_x=1.8)

        ax_x, y_bot, y_top = 3.45, -1.65, 1.80
        axis = make_axis_bars(ax_x, y_bot, y_top, max_val=7.0, label="mg per kg per min", label_size=22)
        j_tr = ValueTracker(5.71)
        egp_tr = ValueTracker(0.0)
        rd_tr = ValueTracker(5.71)

        bar_j, num_j = make_live_bar(ax_x + 0.56, y_bot, y_top, 7.0, j_tr, CYAN, width=0.50, num_size=22)
        bar_egp, _ = make_live_bar(ax_x + 0.56, y_bot, y_top, 7.0, egp_tr, MAGENTA, width=0.50,
                                   base_tracker=j_tr, show_num=False)
        bar_rd, num_rd = make_live_bar(ax_x + 1.50, y_bot, y_top, 7.0, rd_tr, TEXT, width=0.50, num_size=22)

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"],
            ins_gauge, pump, pump_line, liver, bracket, l0_tag,
            pump_dots, exit_dots,
            axis, bar_j, num_j, bar_egp, bar_rd, num_rd
        )
        self.play(Create(l0_cross), run_time=0.6)

        self.at("may not stop it")
        liver_rate = ValueTracker(0.65)
        liver_dots = make_vertical_flow(-0.55, 1.34, 0.58, color=MAGENTA, n=4,
                                        rate_tracker=liver_rate, seed=22, radius=0.055)
        self.add(liver_dots)
        self.wait(0.8)

        self.at("with a tracer")
        tracer_stream = make_blood_stream(-4.6, 0.65, -0.55, 0.55, n_glucose=8, n_cyan=6, n_tracer=5,
                                          speed_tracker=w["speed_tracker"], seed=44)
        tracer_lbl = T("tracer", size=22, color=MAGENTA).move_to([-4.25, 1.15, 0])
        s_txt = T("blood\nsamples", size=22, color=TEXT, line_spacing=0.60)
        s_box = RoundedRectangle(width=s_txt.width + 0.24, height=s_txt.height + 0.12, corner_radius=0.10,
                                 stroke_color=TEXT, stroke_width=2.0, fill_color=BG, fill_opacity=0.92)
        sample_box = VGroup(s_box, s_txt.move_to(s_box)).move_to([-1.60, 0.99, 0])
        sample_probe = Line([-1.60, s_box.get_bottom()[1], 0], [-1.60, 0.45, 0], color=TEXT, stroke_width=2.2)
        self.remove(w["stream"])
        self.add(tracer_stream)

        # Fade out num_j before stacking MAGENTA EGP on top of CYAN J
        j_note = M("J = 5.71", size=22, color=CYAN).move_to([ax_x + 0.85, 2.52, 0])
        egp_num = counter("EGP = {:.2f}", egp_tr, at=[ax_x + 0.85, 2.12, 0], size=22, color=MAGENTA)
        self.play(FadeOut(num_j), FadeIn(j_note), FadeIn(tracer_lbl), FadeIn(sample_probe), FadeIn(sample_box), run_time=0.6)
        self.add(egp_num)
        self.play(egp_tr.animate.set_value(0.50), run_time=1.3)

        self.at("pump plus")
        self.play(rd_tr.animate.set_value(6.21), run_time=1.4)

        self.at("measured not assumed")
        meas_tag = boxed_label("✓ measured, not assumed", GREEN, size=24, pad=0.14).move_to([4.45, 3.08, 0])
        self.play(FadeIn(meas_tag), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 11: s11_close (13.2 s)
# ---------------------------------------------------------------------------
class S11Close(SpokenScene):
    def construct(self):
        w = build_base_world(
            blood_x=(-4.6, 0.65), blood_y=(-0.55, 0.55), mf_y=(-2.50, -1.35),
            gauge_x=1.80, gauge_y=0.05, gauge_h=2.10,
            glucose_lvl=0.30, doors_open=0.90, show_too_high=False, show_basal=False,
            n_glucose=10, n_cyan=10, n_tracer=2, seed=21
        )
        ins_lvl = ValueTracker(0.82)
        ins_gauge = make_gauge([-5.65, 0.05, 0], height=2.10, level_tracker=ins_lvl,
                               fill_color=PURPLE, label="insulin", label_size=24)
        dial_tr = ValueTracker(0.5)
        pump = make_pump([-3.25, 1.95, 0], dial_tracker=dial_tr, label="pump", label_size=24)
        pump_line = Line([-3.25, 1.52, 0], [-3.25, 0.55, 0], color=CYAN, stroke_width=3.5)
        liver = make_liver([-0.55, 1.80, 0], width=1.45, height=0.82, label_size=24)

        pump_dots = make_vertical_flow(-3.25, 1.48, 0.58, color=YELLOW, ring_color=CYAN, n=5,
                                       rate_tracker=ValueTracker(1.1), seed=19, radius=0.068)
        liver_dots = make_vertical_flow(-0.55, 1.34, 0.58, color=MAGENTA, n=4,
                                        rate_tracker=ValueTracker(0.75), seed=22, radius=0.055)
        exit_dots = make_vertical_flow(-1.95, -0.58, -1.35, color=YELLOW, n=6,
                                       rate_tracker=ValueTracker(1.1), seed=3, spread_x=1.8)

        inset_box = RoundedRectangle(width=3.2, height=1.85, corner_radius=0.12,
                                     stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to([4.5, 2.05, 0])
        inset_p = Plot(box=(3.15, 5.85, 1.30, 2.75), xr=(0, 2), yr=(80, 200), xticks=[], yticks=[], stroke=2.5)
        ic1 = inset_p.curve(ogtt_less_secretion, color=PURPLE, width=3.5)
        ic2 = DashedVMobject(inset_p.curve(ogtt_weaker_action, color=BLUE, width=3.5), num_dashes=16)
        inset = VGroup(inset_box, inset_p, ic1, ic2)
        q1 = boxed_label("too little insulin?", PURPLE, size=22, pad=0.12).move_to([4.5, 0.45, 0])
        q2 = boxed_label("weak response?", BLUE, size=22, pad=0.12).move_to([4.5, -0.30, 0])

        eq_main = M("Rd = J + EGP", size=36, color=TEXT).move_to([-1.8, 3.05, 0])

        self.add(
            w["blood_box"], w["blood_lbl"], w["mf_box"], w["mf_lbl"],
            w["doors"], w["gauge"], w["stream"],
            ins_gauge, pump, pump_line, liver,
            pump_dots, liver_dots, exit_dots,
            inset, q1, q2, eq_main
        )

        self.at("tipping not why")
        self.play(inset_box.animate.set_stroke(GOLD, 3.5), run_time=0.6)
        self.play(inset_box.animate.set_stroke(GREY, 2.5), run_time=0.5)

        self.at("freeze the level")
        bracket = make_clamp_bracket(w["gauge"], w["g_tracker"], label="held")
        in_arr = Arrow([-1.95, 1.35, 0], [-1.95, 0.58, 0], buff=0.0, color=YELLOW, stroke_width=8.0, tip_length=0.22)
        out_arr = Arrow([-1.95, -0.55, 0], [-1.95, -1.35, 0], buff=0.0, color=YELLOW, stroke_width=8.0, tip_length=0.22)
        in_lbl = T("in = out", size=26, color=TEXT).move_to([4.5, -1.55, 0])
        self.play(FadeOut(q1), FadeOut(q2), FadeIn(bracket), FadeIn(in_arr), FadeIn(out_arr), FadeIn(in_lbl), run_time=0.8)

        self.at("what the pump adds")
        self.play(Indicate(pump[0], color=CYAN), run_time=0.6)

        self.at("what the body makes")
        self.play(Indicate(liver[0], color=MAGENTA), run_time=0.6)

        self.at("what the tissues take")
        self.play(w["mf_box"].animate.set_stroke(TEXT, 6.0), run_time=0.3)
        self.play(w["mf_box"].animate.set_stroke(GREY, 3.0), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 12: s12_end (3.5 s silent)
# ---------------------------------------------------------------------------
class S12End(EndCard):
    LINE = "Hold glucose still, and what enters must equal what leaves."
