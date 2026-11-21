"""Who Pays for Glucose? — Integration of Metabolism (Chapter 2)

COLOUR MAP (one colour per concept, carried across the whole film):
    YELLOW     = "#F5D547"  # glucose (blood glucose, brain glucose need, glycogen-derived glucose)
    ORANGE     = "#F28C38"  # liver glycogen store
    PINK       = "#FF7EB6"  # new glucose (gluconeogenesis)
    TEAL       = "#3FB8C0"  # fatty acids (from fat tissue)
    PALE_TEAL  = "#9CE3E7"  # glycerol (fat's backbone)
    GREEN      = "#83C167"  # ketone bodies
    RED        = "#FC6255"  # muscle protein (the cost) and the fatty-acid no-glucose barrier
    PERIWINKLE = "#9B9EF0"  # brain
    GOLD       = "#D4A843"  # time scrubber marker ('you are here') and predict card
    GREY       = "#8B93A1"  # organs, axes, and reference lines
    TEXT/WHITE = "#E8EAF0"  # nitrogen dots (urea), primary labels

THE ONE WORLD CARRIED FROM SCENE TO SCENE:
    (1) TOP BAND: a 5-stop time scrubber ('2 h', '12 h', '1 day', '3 days', '5 weeks') with a GOLD marker
        and 'spacing schematic' tag.
    (2) LEFT 25%: a tall blood tube with two side-by-side vertical gauges on one shared 0–8 mM scale
        (YELLOW glucose, GREEN ketones) and upward-flowing blood fuel dots.
    (3) RIGHT 30%: a PERIWINKLE brain box with its 0–120 g/day fuel bar beneath it.
    (4) CENTRE: GREY organ boxes (liver, muscle, fat, kidney — at most 6 major elements on screen)
        linked by computed fuel streams.

WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
    s00_link_and_question: GOLD scrubber marker sweeps from 12 h to 5 weeks over 6 s while blood glucose
        and ketone gauges interpolate the lesson's 5-stop fasting table midpoints; resets to 12 h on question.
    s02_savings: Scrubber advances from 12 h toward 3 days while the liver's 100 g ORANGE glycogen tank
        drains to a sliver, blood gauges interpolate the table, and liver output shifts to PINK-edged glucose.
    s03_raw_material: TEAL fatty-acid stream hits a RED 'no glucose' barrier in liver, PALE TEAL glycerol
        crosses into new glucose, and a thick RED stream leaves muscle while the protein block shrinks.
    s04_alanine_kidney: RED+WHITE alanine tokens split in liver (PINK glucose to blood, WHITE nitrogen to
        urea); kidney enters below liver and thickens its glucose stream until equal at 5 weeks.
    s05_bill: Brain's 0–120 g/day bar fills 0->120 g, splits into 17.5 g PALE TEAL glycerol and 102.5 g RED
        protein; a day counter runs 0 to 18.5 days (3.33 kg / 180 g/day) draining 1/3 of the 10 kg protein block.
    s06_idea: Muscle resets to full; a horizontal YELLOW 'nearly level' line crosses the 4 mM glucose mark
        while glycogen, glycerol, protein payers and the brain bar highlight in turn.
    s07_predict: GREEN ketone dots enter the brain and fill the top 2/3 of the 0–120 g bar down to 40 g,
        leaving the remaining 40 g glucose need unsplit as the prediction question appears.
    s09_answer: PALE TEAL glycerol refills 17.5 g inside the 40 g glucose slot, leaving 22.5 g RED protein
        beside a 102.5 g ghost (computed ratio 22.5/102.5 ≈ 1/5) as muscle's RED stream thins to ~1/5.
    s10_fat_and_hedge: A day tracker runs 0 to 75 days driving side-by-side drain bars (fat 75 days vs
        muscle ~29.6% spent at 39.5 g/day); muscle's stream then thins further toward measured ~20 g/day.
    s11_five_weeks: Scrubber returns to 5 weeks (3.75 mM glucose, 7.5 mM ketones); brain pie fills to 2/3
        GREEN / 1/3 YELLOW, kidney matches liver glucose output, and muscle stream pulses beside its old ghost.
    s12_close: Scrubber sweeps 12 h to 5 weeks, replaying glycogen drain -> muscle swell/thin -> fat-to-ketone
        brain takeover (pie to 2/3 GREEN) while blood glucose tracks close to the 'nearly level' line.
"""

from bp_parts import *

# Film-specific concept colours
ORANGE = "#F28C38"
PINK = "#FF7EB6"
PALE_TEAL = "#9CE3E7"
PERIWINKLE = "#9B9EF0"

# Lesson fasting table midpoints at stops: ["2 h", "12 h", "1 day", "3 days", "5 weeks"]
STOPS = ["2 h", "12 h", "1 day", "3 days", "5 weeks"]
STOP_X = [-4.2, -2.1, 0.0, 2.1, 4.2]
GLUCOSE_MM = [6.5, 4.75, 4.25, 3.75, 3.75]
KETONES_MM = [0.1, 0.15, 0.4, 2.5, 7.5]

# Shared geometry constants (16:9 safe frame: x in [-6.3, 6.3], y in [-3.5, 3.5])
SCRUB_Y = 2.98
TUBE_X0, TUBE_X1 = -5.65, -3.25
TUBE_Y0, TUBE_Y1 = -1.85, 1.95
GLUC_COL_X = -4.98
KET_COL_X = -4.02
COL_W = 0.54

BRAIN_CENTER = np.array([4.60, 1.55, 0.0])
BRAIN_W, BRAIN_H = 2.80, 1.15
BAR_X = 4.60
BAR_W = 0.72
BAR_Y0, BAR_Y1 = -1.85, 0.55  # 0 to 120 g/day -> 0.02 units/g

LIVER_CENTER = np.array([-0.50, 1.00, 0.0])
LIVER_W, LIVER_H = 3.30, 1.92   # x in [-2.15, 1.15], y in [0.04, 1.96]
MUSCLE_CENTER = np.array([-1.20, -1.35, 0.0])
MUSCLE_W, MUSCLE_H = 2.65, 1.62  # x in [-2.52, 0.12], y in [-2.16, -0.54]
FAT_CENTER = np.array([1.65, -1.35, 0.0])
FAT_W, FAT_H = 2.30, 1.35
KIDNEY_CENTER = np.array([1.60, -0.48, 0.0])  # x in [0.48, 2.72], y in [-0.96, 0.00] -> clear of liver (y>=0.04)
KIDNEY_W, KIDNEY_H = 2.25, 0.96


def interp_table(t_idx, values):
    """Linearly interpolate a 5-stop table at continuous index t_idx in [0, 4]."""
    t = float(np.clip(t_idx, 0.0, 4.0))
    i = min(int(t), 3)
    f = t - i
    return values[i] * (1.0 - f) + values[i + 1] * f


def scrub_x(t_idx):
    t = float(np.clip(t_idx, 0.0, 4.0))
    i = min(int(t), 3)
    f = t - i
    return STOP_X[i] * (1.0 - f) + STOP_X[i + 1] * f


def build_scrubber(t_tracker, opacity=1.0):
    """Top time scrubber with 5 stops, GOLD marker, and 'spacing schematic' tag."""
    track = Line([STOP_X[0], SCRUB_Y, 0], [STOP_X[-1], SCRUB_Y, 0], color=GREY, stroke_width=3.5)
    ticks = VGroup()
    labels = VGroup()
    for x, name in zip(STOP_X, STOPS):
        ticks.add(Line([x, SCRUB_Y - 0.10, 0], [x, SCRUB_Y + 0.10, 0], color=GREY, stroke_width=3))
        labels.add(T(name, size=24, color=TEXT).move_to([x, SCRUB_Y + 0.34, 0]))
    tag = T("spacing schematic", size=22, color=GREY).move_to([0.0, SCRUB_Y - 0.36, 0])
    base = VGroup(track, ticks, labels, tag)
    if opacity < 1.0:
        base.set_opacity(opacity)

    marker = always_redraw(
        lambda: RegularPolygon(n=4, color=GOLD, fill_color=GOLD, fill_opacity=opacity, stroke_width=2.5)
        .scale(0.16)
        .move_to([scrub_x(t_tracker.get_value()), SCRUB_Y, 0])
    )
    return VGroup(base, marker)


def build_blood_tube(t_tracker, flow_tracker):
    """Tall blood tube on the left with 0–8 mM scale, live glucose & ketone columns, and blood carrier dots."""
    tube_w = TUBE_X1 - TUBE_X0
    tube_h = TUBE_Y1 - TUBE_Y0
    tube = RoundedRectangle(
        corner_radius=0.14, width=tube_w, height=tube_h,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07
    ).move_to([(TUBE_X0 + TUBE_X1) / 2, (TUBE_Y0 + TUBE_Y1) / 2, 0])

    title = T("blood (mM)", size=26, color=TEXT).move_to([(TUBE_X0 + TUBE_X1) / 2, TUBE_Y1 + 0.30, 0])

    ticks = VGroup()
    tick_labels = VGroup()
    for val in (0, 2, 4, 6, 8):
        y = TUBE_Y0 + (val / 8.0) * tube_h
        ticks.add(Line([TUBE_X0 - 0.10, y, 0], [TUBE_X0, y, 0], color=GREY, stroke_width=2.5))
        tick_labels.add(M(str(val), size=24, color=TEXT).next_to([TUBE_X0 - 0.12, y, 0], LEFT, buff=0.08))

    def g_val():
        return interp_table(t_tracker.get_value(), GLUCOSE_MM)

    def k_val():
        return interp_table(t_tracker.get_value(), KETONES_MM)

    def make_bar(x_center, val_fn, col):
        def _draw():
            v = max(float(val_fn()), 0.08)
            h = (v / 8.0) * tube_h
            return Rectangle(
                width=COL_W, height=h, stroke_color=col, stroke_width=2.5,
                fill_color=col, fill_opacity=0.82
            ).move_to([x_center, TUBE_Y0 + h / 2, 0])
        return always_redraw(_draw)

    g_bar = make_bar(GLUC_COL_X, g_val, YELLOW)
    k_bar = make_bar(KET_COL_X, k_val, GREEN)

    g_name = T("glucose", size=24, color=YELLOW).move_to([GLUC_COL_X - 0.08, TUBE_Y0 - 0.28, 0])
    k_name = T("ketones", size=24, color=GREEN).move_to([KET_COL_X + 0.22, TUBE_Y0 - 0.28, 0])
    g_num = always_redraw(lambda: M(f"{g_val():.1f}", size=24, color=YELLOW).move_to([GLUC_COL_X - 0.08, TUBE_Y0 - 0.62, 0]))
    k_num = always_redraw(lambda: M(f"{k_val():.1f}", size=24, color=GREEN).move_to([KET_COL_X + 0.22, TUBE_Y0 - 0.62, 0]))

    rng = np.random.default_rng(7)
    n_dots = 10
    x_offsets = rng.uniform(-0.11, 0.11, size=n_dots)
    dots = VGroup(*[Dot(radius=0.06, color=TEXT).set_opacity(0.70) for _ in range(n_dots)])
    mid_x = (GLUC_COL_X + KET_COL_X) / 2

    def update_blood_dots(mob):
        ph = flow_tracker.get_value()
        for i, d in enumerate(mob):
            frac = (i / n_dots + ph * 0.65) % 1.0
            y = TUBE_Y0 + 0.14 + frac * (tube_h - 0.28)
            d.move_to([mid_x + x_offsets[i], y, 0])

    dots.add_updater(update_blood_dots)
    update_blood_dots(dots)

    grp = VGroup(tube, title, ticks, tick_labels, g_bar, k_bar, dots, g_name, k_name, g_num, k_num)
    grp.tube = tube
    grp.g_bar = g_bar
    grp.k_bar = k_bar
    return grp


def build_brain_box(ketone_share_tracker=None):
    """PERIWINKLE brain box on the right, optionally holding a fuel-mix pie sector."""
    box = RoundedRectangle(
        corner_radius=0.16, width=BRAIN_W, height=BRAIN_H,
        stroke_color=PERIWINKLE, stroke_width=3, fill_color=PERIWINKLE, fill_opacity=0.16
    ).move_to(BRAIN_CENTER)
    label = T("brain", size=30, color=PERIWINKLE).move_to(BRAIN_CENTER + LEFT * 0.55)
    g = VGroup(box, label)
    if ketone_share_tracker is not None:
        pie_c = BRAIN_CENTER + RIGHT * 0.68
        r = 0.36
        def _pie():
            kf = float(np.clip(ketone_share_tracker.get_value(), 0.0, 1.0))
            parts = VGroup()
            if kf < 0.999:
                parts.add(Sector(
                    radius=r, start_angle=PI / 2, angle=(1.0 - kf) * TAU,
                    arc_center=pie_c, color=YELLOW, fill_opacity=0.90, stroke_color=BG, stroke_width=2
                ))
            if kf > 0.001:
                parts.add(Sector(
                    radius=r, start_angle=PI / 2, angle=-kf * TAU,
                    arc_center=pie_c, color=GREEN, fill_opacity=0.90, stroke_color=BG, stroke_width=2
                ))
            parts.add(Circle(radius=r, stroke_color=TEXT, stroke_width=2).move_to(pie_c))
            return parts
        pie = always_redraw(_pie)
        g.add(pie)
    else:
        label.move_to(BRAIN_CENTER)
    g.box = box
    g.label = label
    return g


def build_brain_bar(x_center=BAR_X, y0=BAR_Y0, y1=BAR_Y1, width=BAR_W,
                    ket_g=0.0, glyc_g=0.0, prot_g=0.0, gluc_outline_g=120.0,
                    show_title=True, title_text="brain's glucose\n(g/day)"):
    """Parametric 0–120 g/day brain fuel bar with well-spaced title below 0 tick."""
    h = y1 - y0
    frame = Rectangle(width=width, height=h, stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.3)
    frame.move_to([x_center, (y0 + y1) / 2, 0])
    ticks = VGroup()
    tlabels = VGroup()
    for val in (0, 40, 80, 120):
        y = y0 + (val / 120.0) * h
        ticks.add(Line([x_center - width / 2 - 0.10, y, 0], [x_center - width / 2, y, 0], color=GREY, stroke_width=2.5))
        tlabels.add(M(str(val), size=24, color=TEXT).next_to([x_center - width / 2 - 0.12, y, 0], LEFT, buff=0.08))

    fills = VGroup()
    if gluc_outline_g > 0 and (glyc_g + prot_g == 0):
        gh = (gluc_outline_g / 120.0) * h
        fills.add(Rectangle(
            width=width - 0.04, height=gh, stroke_color=YELLOW, stroke_width=3,
            fill_color=YELLOW, fill_opacity=0.78 if ket_g == 0 else 0.12
        ).move_to([x_center, y0 + gh / 2, 0]))
    if glyc_g > 0:
        gh = (glyc_g / 120.0) * h
        fills.add(Rectangle(
            width=width - 0.04, height=gh, stroke_color=PALE_TEAL, stroke_width=1.5,
            fill_color=PALE_TEAL, fill_opacity=0.88
        ).move_to([x_center, y0 + gh / 2, 0]))
    if prot_g > 0:
        ph = (prot_g / 120.0) * h
        base_y = y0 + (glyc_g / 120.0) * h
        fills.add(Rectangle(
            width=width - 0.04, height=ph, stroke_color=RED, stroke_width=1.5,
            fill_color=RED, fill_opacity=0.85
        ).move_to([x_center, base_y + ph / 2, 0]))
    if ket_g > 0:
        kh = (ket_g / 120.0) * h
        fills.add(Rectangle(
            width=width - 0.04, height=kh, stroke_color=GREEN, stroke_width=1.5,
            fill_color=GREEN, fill_opacity=0.82
        ).move_to([x_center, y1 - kh / 2, 0]))

    g = VGroup(frame, fills, ticks, tlabels)
    if show_title:
        ttl = T(title_text, size=24, color=TEXT, line_spacing=0.85).move_to([x_center, y0 - 0.62, 0])
        g.add(ttl)
        g.title = ttl
    g.frame = frame
    return g


def build_liver(glycogen_frac=None, show_new_glucose=False):
    """GREY liver box in centre-upper position with clear non-overlapping sub-zones."""
    box = RoundedRectangle(
        corner_radius=0.16, width=LIVER_W, height=LIVER_H,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13
    ).move_to(LIVER_CENTER)
    label = T("liver", size=28, color=TEXT).move_to(LIVER_CENTER + UP * 0.72 + LEFT * 1.12)
    g = VGroup(box, label)
    g.box = box
    g.label = label

    if glycogen_frac is not None:
        tw, th = 1.35, 0.38
        tc = LIVER_CENTER + LEFT * 0.72 + DOWN * 0.62
        tank_frame = Rectangle(width=tw, height=th, stroke_color=ORANGE, stroke_width=2.5, fill_color=BG, fill_opacity=0.35).move_to(tc)
        tank_label = T("glycogen\n~100 g", size=24, color=ORANGE, line_spacing=0.82).move_to(LIVER_CENTER + LEFT * 0.72 + UP * 0.08)
        def _tank_fill():
            f = float(np.clip(glycogen_frac.get_value(), 0.04, 1.0))
            fh = th * f
            return Rectangle(
                width=tw - 0.04, height=max(fh - 0.02, 0.04), stroke_width=0,
                fill_color=ORANGE, fill_opacity=0.82
            ).move_to([tc[0], tc[1] - th / 2 + fh / 2, 0])
        tank_fill = always_redraw(_tank_fill)
        g.add(tank_frame, tank_fill, tank_label)
        g.tank_frame = tank_frame
        g.tank_label = tank_label

    if show_new_glucose:
        ng = T("new glucose", size=24, color=PINK).move_to(LIVER_CENTER + UP * 0.72 + RIGHT * 0.55)
        g.add(ng)
        g.new_glucose = ng

    return g


def build_muscle(protein_frac=None, block_label="protein"):
    """GREY muscle box at lower left of centre with RED protein block and generous label spacing."""
    box = RoundedRectangle(
        corner_radius=0.16, width=MUSCLE_W, height=MUSCLE_H,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13
    ).move_to(MUSCLE_CENTER)
    label = T("muscle", size=28, color=TEXT).move_to(MUSCLE_CENTER + UP * 0.56)
    blab = T(block_label, size=24, color=RED).move_to(MUSCLE_CENTER + UP * 0.08)

    bw, bh = 2.00, 0.44
    bc = MUSCLE_CENTER + DOWN * 0.44
    bframe = Rectangle(width=bw, height=bh, stroke_color=RED, stroke_width=2, fill_color=BG, fill_opacity=0.35).move_to(bc)

    if protein_frac is None:
        bfill = Rectangle(width=bw - 0.04, height=bh - 0.04, stroke_width=0, fill_color=RED, fill_opacity=0.82).move_to(bc)
    else:
        def _pfill():
            f = float(np.clip(protein_frac.get_value(), 0.05, 1.0))
            fh = bh * f
            return Rectangle(
                width=bw - 0.04, height=max(fh - 0.02, 0.04), stroke_width=0,
                fill_color=RED, fill_opacity=0.82
            ).move_to([bc[0], bc[1] - bh / 2 + fh / 2, 0])
        bfill = always_redraw(_pfill)

    g = VGroup(box, label, blab, bframe, bfill)
    g.box = box
    g.label = label
    g.block_frame = bframe
    g.block_label = blab
    g.block_center = bc
    g.block_w = bw
    g.block_h = bh
    return g


def build_fat():
    """GREY fat box at lower right of centre with TEAL block."""
    box = RoundedRectangle(
        corner_radius=0.16, width=FAT_W, height=FAT_H,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13
    ).move_to(FAT_CENTER)
    label = T("fat", size=28, color=TEXT).move_to(FAT_CENTER + UP * 0.40)
    bw, bh = 1.80, 0.50
    bc = FAT_CENTER + DOWN * 0.24
    fill = Rectangle(width=bw, height=bh, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.75).move_to(bc)
    g = VGroup(box, label, fill)
    g.box = box
    g.label = label
    return g


def build_kidney():
    """GREY kidney box below-right of liver, clear of liver border."""
    box = RoundedRectangle(
        corner_radius=0.16, width=KIDNEY_W, height=KIDNEY_H,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13
    ).move_to(KIDNEY_CENTER)
    label = T("kidney", size=28, color=TEXT).move_to(KIDNEY_CENTER)
    g = VGroup(box, label)
    g.box = box
    g.label = label
    return g


def make_dot_stream(p0, p1, flow_tracker, color, n=5, radius=0.07, speed=0.65,
                    edge_color=None, white_partner=False, spread=0.0, seed=7):
    """A moving stream of dots along segment p0 -> p1 driven by flow_tracker."""
    p0 = np.array(p0, dtype=float)
    p1 = np.array(p1, dtype=float)
    vec = p1 - p0
    length = np.linalg.norm(vec)
    perp = np.array([-vec[1], vec[0], 0.0]) / max(length, 1e-6)
    rng = np.random.default_rng(seed)
    offsets = rng.uniform(-spread, spread, size=n) if spread > 0 else np.zeros(n)

    items = VGroup()
    for _ in range(n):
        kw = {"stroke_color": edge_color, "stroke_width": 2.5} if edge_color else {}
        d = Dot(radius=radius, color=color, **kw)
        if white_partner:
            w = Dot(radius=radius * 0.62, color=TEXT).next_to(d, RIGHT, buff=0.02)
            items.add(VGroup(d, w))
        else:
            items.add(d)

    def _upd(mob):
        ph = flow_tracker.get_value()
        for i, item in enumerate(mob):
            frac = (i / n + ph * speed) % 1.0
            pos = p0 + frac * vec + perp * offsets[i]
            item.move_to(pos)

    items.add_updater(_upd)
    _upd(items)
    items.layout_ok = True   # flowing fuel dots intentionally travel between organs
    return items


def attach_flow_driver(scene, flow_tracker, rate=0.65):
    """Advance flow_tracker smoothly every frame so carried fuel streams keep moving."""
    drv = Mobject()
    drv.add_updater(lambda m, dt: flow_tracker.increment_value(dt * rate))
    scene.add(drv)
    return drv


# =============================================================================
# SCENES
# =============================================================================

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(1.0)
        flow = ValueTracker(0.0)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box()
        bbar = build_brain_bar(gluc_outline_g=120.0)

        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=7, radius=0.075, speed=0.48)

        self.play(FadeIn(scrubber), FadeIn(blood), FadeIn(brain), FadeIn(bbar), run_time=1.3)
        self.add(g_stream)

        self.at("turning to ketone")
        k_stream = make_dot_stream([-3.15, 2.20, 0], [3.10, 1.96, 0], flow, GREEN, n=6, radius=0.072, speed=0.48)
        self.add(k_stream)
        self.play(brain.box.animate.set_stroke(GREEN, width=6).set_fill(GREEN, opacity=0.25), run_time=1.2)
        self.play(brain.box.animate.set_stroke(PERIWINKLE, width=3).set_fill(PERIWINKLE, opacity=0.16), run_time=1.2)

        self.at("follow the blood")
        self.play(t_idx.animate.set_value(4.0), run_time=5.8, rate_func=linear)

        self.at("about one millimolar")
        y_hi = TUBE_Y0 + (4.75 / 8.0) * (TUBE_Y1 - TUBE_Y0)
        y_lo = TUBE_Y0 + (3.75 / 8.0) * (TUBE_Y1 - TUBE_Y0)
        brk_line = Line([-3.05, y_lo, 0], [-3.05, y_hi, 0], color=YELLOW, stroke_width=4)
        brk_ticks = VGroup(
            Line([-3.18, y_lo, 0], [-3.05, y_lo, 0], color=YELLOW, stroke_width=3),
            Line([-3.18, y_hi, 0], [-3.05, y_hi, 0], color=YELLOW, stroke_width=3),
        )
        brk_lab = T("about 1 mM", size=26, color=YELLOW).next_to(brk_line, RIGHT, buff=0.16)
        self.play(Create(brk_line), Create(brk_ticks), FadeIn(brk_lab), run_time=1.2)

        self.at("ketones climb")
        y_k0 = TUBE_Y0 + (0.15 / 8.0) * (TUBE_Y1 - TUBE_Y0)
        y_k1 = TUBE_Y0 + (7.50 / 8.0) * (TUBE_Y1 - TUBE_Y0)
        k_arrow = Arrow([-3.44, y_k0, 0], [-3.44, y_k1, 0],
                        color=GREEN, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.07)
        k_lab = T("0.1 to 7–8 mM", size=26, color=GREEN).move_to([-1.95, 1.35, 0])
        self.play(GrowArrow(k_arrow), FadeIn(k_lab), run_time=3.2)

        self.at("who is paying")
        q_line = T("Who pays for steady glucose?", size=34, color=TEXT).move_to([0.0, -3.05, 0])
        self.play(
            t_idx.animate.set_value(1.0),
            FadeOut(brk_line), FadeOut(brk_ticks), FadeOut(brk_lab),
            FadeOut(k_arrow), FadeOut(k_lab),
            FadeIn(q_line, shift=UP * 0.12),
            run_time=1.2
        )
        self.finish()


class S01Title(TitleCard):
    LESSON = "Integration of Metabolism: How the Body Switches Fuels"
    TITLE = "Who Pays for Glucose?"


class S02Savings(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(1.0)
        flow = ValueTracker(0.0)
        glyc = ValueTracker(1.0)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box()
        bbar = build_brain_bar(gluc_outline_g=120.0)
        liver = build_liver(glycogen_frac=glyc)
        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=7, radius=0.075, speed=0.48)

        self.add(scrubber, blood, brain, bbar, g_stream)
        self.play(FadeIn(liver), run_time=0.75)

        self.at("pays")
        liv_to_blood = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=6, radius=0.08, speed=0.68)
        self.add(liv_to_blood)
        self.play(glyc.animate.set_value(0.55), t_idx.animate.set_value(1.4), run_time=4.2, rate_func=linear)

        self.at("within a day")
        self.play(
            t_idx.animate.set_value(3.0),
            glyc.animate.set_value(0.08),
            run_time=3.4,
            rate_func=linear
        )

        self.at("after that")
        ng_lab = T("new glucose", size=24, color=PINK).move_to(LIVER_CENTER + UP * 0.72 + RIGHT * 0.55)
        pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=6,
                                      radius=0.08, speed=0.68, edge_color=PINK)
        self.remove(liv_to_blood)
        self.add(pink_stream)
        self.play(FadeIn(ng_lab), run_time=1.4)
        self.finish()


class S03RawMaterial(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(3.0)
        flow = ValueTracker(0.0)
        glyc = ValueTracker(0.08)
        prot = ValueTracker(1.0)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box()
        bbar = build_brain_bar(gluc_outline_g=120.0)
        liver = build_liver(glycogen_frac=glyc, show_new_glucose=True)
        fat = build_fat()
        muscle = build_muscle(protein_frac=prot)

        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=7, radius=0.075, speed=0.48)
        pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=6,
                                      radius=0.08, speed=0.68, edge_color=PINK)

        self.add(scrubber, blood, brain, bbar, liver, g_stream, pink_stream)
        self.play(FadeIn(fat), FadeIn(muscle), run_time=1.0)

        self.at("fatty acids")
        fa_stream = make_dot_stream([1.35, -0.62, 0], [0.55, 0.38, 0], flow, TEAL, n=6, radius=0.075, speed=0.65)
        self.add(fa_stream)

        self.at("cannot become")
        bline = Line(LIVER_CENTER + RIGHT * 0.25 + DOWN * 0.55,
                     LIVER_CENTER + RIGHT * 0.90 + UP * 0.05, color=RED, stroke_width=5)
        blab = T("no glucose", size=24, color=RED).move_to([2.08, 0.65, 0])
        self.play(Create(bline), FadeIn(blab), run_time=1.8)

        self.at("glycerol backbone")
        glyc_stream = make_dot_stream([0.90, -0.62, 0], [-0.05, 0.35, 0], flow, PALE_TEAL, n=5, radius=0.065, speed=0.68)
        glyc_lab = T("glycerol", size=24, color=PALE_TEAL).move_to([1.95, -0.10, 0])
        self.add(glyc_stream)
        self.play(FadeIn(glyc_lab), run_time=1.8)

        self.at("main raw material")
        prot_stream = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.08, 0], flow, RED, n=6,
                                      radius=0.09, speed=0.72, spread=0.14)
        self.add(prot_stream)
        self.play(prot.animate.set_value(0.75), run_time=2.8, rate_func=linear)
        self.finish()


class S04AlanineKidney(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(3.0)
        flow = ValueTracker(0.0)
        glyc = ValueTracker(0.08)
        prot = ValueTracker(0.75)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box()
        bbar = build_brain_bar(gluc_outline_g=120.0)
        liver = build_liver(glycogen_frac=glyc, show_new_glucose=True)
        fat = build_fat()
        muscle = build_muscle(protein_frac=prot)

        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=7, radius=0.075, speed=0.48)
        pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=6,
                                      radius=0.08, speed=0.68, edge_color=PINK)
        prot_stream = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.08, 0], flow, RED, n=6,
                                      radius=0.085, speed=0.68, spread=0.10)

        self.add(scrubber, blood, brain, bbar, liver, fat, muscle, g_stream, pink_stream, prot_stream)
        self.play(fat.animate.shift(RIGHT * 6.0).set_opacity(0), run_time=0.8)
        self.remove(fat)

        self.at("broken into amino")
        aa_stream = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.08, 0], flow, RED, n=5, radius=0.075, speed=0.65)
        self.remove(prot_stream)
        self.add(aa_stream)
        self.play(prot.animate.set_value(0.65), run_time=2.2, rate_func=linear)

        self.at("alanine carries")
        ala_stream = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.02, 0], flow, RED, n=5,
                                     radius=0.075, speed=0.65, white_partner=True)
        ala_lab = T("alanine", size=22, color=TEXT).move_to([-0.28, -0.363, 0])
        self.remove(aa_stream)
        self.add(ala_stream)
        self.play(FadeIn(ala_lab), run_time=1.8)

        self.at("carbon can become")
        c_arrow = Arrow([-0.35, 0.58, 0], [0.18, 1.32, 0], color=PINK, stroke_width=3.5, buff=0)
        c_to_p = make_dot_stream([-0.35, 0.58, 0], [0.18, 1.32, 0], flow, PINK, n=4, radius=0.07, speed=0.72)
        self.play(GrowArrow(c_arrow), run_time=1.4)
        self.add(c_to_p)

        self.at("dumped as urea")
        urea_lab = T("urea", size=24, color=TEXT).move_to([0.72, 0.44, 0])
        u_arrow = Arrow([-0.15, 0.54, 0], [0.35, 0.44, 0], color=TEXT, stroke_width=3, buff=0)
        n_dump = make_dot_stream([-0.15, 0.54, 0], [0.35, 0.44, 0], flow, TEXT, n=3, radius=0.055, speed=0.68)
        self.play(GrowArrow(u_arrow), FadeIn(urea_lab), run_time=1.5)
        self.add(n_dump)

        self.at("kidney joins in")
        kidney = build_kidney()
        self.play(FadeIn(kidney), run_time=1.0)
        kid_thin = make_dot_stream([0.42, -0.11, 0], [-3.20, -0.11, 0], flow, YELLOW, n=5,
                                   radius=0.052, speed=0.58, edge_color=PINK)
        self.add(kid_thin)

        self.at("by five weeks")
        kid_thick = make_dot_stream([0.42, -0.11, 0], [-3.20, -0.11, 0], flow, YELLOW, n=6,
                                    radius=0.078, speed=0.68, edge_color=PINK)
        eq_sign = T("=", size=34, color=PINK).move_to([-2.68, 0.865, 0])
        eq_lab = T("about\nequal", size=22, color=TEXT, line_spacing=0.82).move_to([-2.68, 0.395, 0])
        self.play(t_idx.animate.set_value(4.0), run_time=2.4, rate_func=linear)
        self.remove(kid_thin)
        self.add(kid_thick)
        self.play(FadeIn(eq_sign), FadeIn(eq_lab), run_time=0.8)
        self.finish()


class S05Bill(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(4.0)
        flow = ValueTracker(0.0)
        prot = ValueTracker(1.0)
        days = ValueTracker(0.0)
        g_fill = ValueTracker(0.0)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx, opacity=0.60)
        blood = build_blood_tube(t_idx, flow)
        kidney = build_kidney()
        muscle = build_muscle(protein_frac=prot)

        bx = 2.75
        by0, by1 = -1.85, 1.05
        bh = by1 - by0
        bw = 0.96
        brain_box = RoundedRectangle(
            corner_radius=0.14, width=2.40, height=0.82,
            stroke_color=PERIWINKLE, stroke_width=3, fill_color=PERIWINKLE, fill_opacity=0.16
        ).move_to([bx, 1.85, 0])
        brain_lab = T("brain", size=28, color=PERIWINKLE).move_to(brain_box)
        bar = build_brain_bar(x_center=bx, y0=by0, y1=by1, width=bw,
                              gluc_outline_g=0.0, show_title=True, title_text="if only glucose (g/day)")

        self.add(scrubber, blood, kidney, muscle, brain_box, brain_lab)
        self.play(kidney.animate.shift(DOWN * 2.5).set_opacity(0), run_time=0.8)
        self.remove(kidney)
        self.play(FadeIn(bar), run_time=0.6)

        self.at("burning only glucose")
        y_fill = always_redraw(lambda: Rectangle(
            width=bw - 0.04, height=max((g_fill.get_value() / 120.0) * bh, 0.03),
            stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.78
        ).move_to([bx, by0 + max((g_fill.get_value() / 120.0) * bh, 0.03) / 2, 0]))
        g_cnt = counter("~{:.0f} g/day", g_fill, at=[4.55, by1 - 0.15, 0], size=26, color=YELLOW)
        self.add(y_fill, g_cnt)
        self.play(g_fill.animate.set_value(120.0), run_time=4.0, rate_func=linear)

        self.at("glycerol covers")
        gh = (17.5 / 120.0) * bh
        g_band = Rectangle(
            width=bw - 0.04, height=gh, stroke_color=PALE_TEAL, stroke_width=1.5,
            fill_color=PALE_TEAL, fill_opacity=0.90
        ).move_to([bx, by0 + gh / 2, 0])
        g_lab = T("glycerol 15–20 g", size=24, color=PALE_TEAL).move_to([4.75, by0 + gh / 2, 0])
        self.play(FadeIn(g_band, shift=UP * 0.15), FadeIn(g_lab), run_time=1.8)

        self.at("the rest")
        ph = (102.5 / 120.0) * bh
        p_frac = ValueTracker(0.0)
        p_band = always_redraw(lambda: Rectangle(
            width=bw - 0.04, height=max(ph * p_frac.get_value(), 0.03),
            stroke_color=RED, stroke_width=1.5, fill_color=RED, fill_opacity=0.85
        ).move_to([bx, by0 + gh + max(ph * p_frac.get_value(), 0.03) / 2, 0]))
        p_lab = T("from protein", size=26, color=RED).move_to([4.55, by0 + gh + ph / 2, 0])
        self.remove(y_fill)
        self.add(g_band, p_band)
        self.play(p_frac.animate.set_value(1.0), FadeIn(p_lab), run_time=2.0, rate_func=linear)

        self.at("180 grams")
        arr_p0 = [bx - bw / 2 - 0.55, by0 + gh + ph * 0.35, 0]
        arr_p1 = [MUSCLE_CENTER[0] + MUSCLE_W / 2 + 0.08, MUSCLE_CENTER[1], 0]
        arr = Arrow(arr_p0, arr_p1, color=RED, stroke_width=4, buff=0)
        cost_lab = T("~180 g protein/day", size=24, color=RED).move_to([MUSCLE_CENTER[0], MUSCLE_CENTER[1] + 1.05, 0])
        cost_stream = make_dot_stream(arr_p1, arr_p0, flow, RED, n=5, radius=0.072, speed=0.68)
        self.play(GrowArrow(arr), FadeIn(cost_lab), run_time=2.2)
        self.add(cost_stream)
        self.wait(1.6)

        self.at("a third of")
        body_lab = T("body protein ~10 kg", size=24, color=RED).move_to([MUSCLE_CENTER[0], -2.42, 0])
        y_third = muscle.block_center[1] + muscle.block_h / 2 - muscle.block_h / 3.0
        dline = DashedLine([muscle.block_center[0] - muscle.block_w / 2, y_third, 0],
                           [muscle.block_center[0] + muscle.block_w / 2, y_third, 0], color=TEXT, stroke_width=2.5)
        day_cnt = counter("day {:.0f}", days, at=[MUSCLE_CENTER[0], MUSCLE_CENTER[1] + 1.56, 0], size=28, color=TEXT)
        rtag = scope_tag("rough sums")
        self.play(FadeOut(muscle.block_label, run_time=0.45), FadeIn(body_lab), Create(dline), FadeIn(rtag), run_time=0.8)
        self.add(day_cnt)
        self.play(
            days.animate.set_value(18.5),
            prot.animate.set_value(0.667),
            run_time=3.2,
            rate_func=linear
        )
        gone_lab = T("1/3 gone, ~2.5 weeks", size=24, color=TEXT).move_to([MUSCLE_CENTER[0], -2.82, 0])
        self.play(FadeIn(gone_lab), run_time=0.5)
        self.finish()


class S06Idea(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(3.0)
        flow = ValueTracker(0.0)
        glyc = ValueTracker(0.10)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box()
        bbar = build_brain_bar(glyc_g=17.5, prot_g=102.5)
        liver = build_liver(glycogen_frac=glyc, show_new_glucose=True)
        muscle = build_muscle()

        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=7, radius=0.075, speed=0.48)
        pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=6,
                                      radius=0.08, speed=0.68, edge_color=PINK)
        glyc_stream = make_dot_stream([0.90, -0.55, 0], [-0.05, 0.35, 0], flow, PALE_TEAL, n=4, radius=0.06, speed=0.68)
        prot_stream = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.08, 0], flow, RED, n=5, radius=0.08, speed=0.68)

        self.add(scrubber, blood, brain, bbar, liver, muscle, g_stream, pink_stream, glyc_stream, prot_stream)

        self.at("blood glucose")
        y4 = TUBE_Y0 + (4.0 / 8.0) * (TUBE_Y1 - TUBE_Y0)
        lvl_line = Line([TUBE_X0 + 0.08, y4, 0], [TUBE_X1 - 0.08, y4, 0], color=YELLOW, stroke_width=4)
        lvl_lab = T("nearly\nlevel", size=22, color=YELLOW, line_spacing=0.82).move_to([-2.68, y4 + 0.30, 0])
        self.play(
            blood.g_bar.animate.set_stroke(YELLOW, width=5),
            Create(lvl_line),
            FadeIn(lvl_lab),
            run_time=1.8
        )

        self.at("who pays")
        self.play(liver.tank_frame.animate.set_stroke(ORANGE, width=4), run_time=0.3)
        self.play(liver.tank_frame.animate.set_stroke(ORANGE, width=2.5), run_time=0.25)
        self.play(muscle.box.animate.set_stroke(RED, width=5), run_time=0.3)
        self.play(muscle.box.animate.set_stroke(GREY, width=3), run_time=0.25)

        self.at("how much")
        cap = caption("level on top, changing payers below", size=30, color=TEXT)
        self.play(bbar.frame.animate.set_stroke(YELLOW, width=5), FadeIn(cap), run_time=0.7)
        self.play(bbar.frame.animate.set_stroke(GREY, width=2.5), run_time=0.4)
        self.finish()


def build_s07_world(flow_tracker, ket_g_tracker):
    """Shared builder for S07Predict end frame and S08Pause backdrop."""
    t_idx = ValueTracker(4.0)
    scrubber = build_scrubber(t_idx)
    blood = build_blood_tube(t_idx, flow_tracker)
    brain = build_brain_box()
    liver = build_liver(glycogen_frac=ValueTracker(0.08), show_new_glucose=True)
    muscle = build_muscle()

    g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow_tracker, YELLOW, n=5, radius=0.065, speed=0.48)
    k_stream = make_dot_stream([-3.15, 2.20, 0], [3.10, 1.96, 0], flow_tracker, GREEN, n=7, radius=0.075, speed=0.48)
    pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow_tracker, YELLOW, n=6,
                                  radius=0.08, speed=0.68, edge_color=PINK)
    prot_stream = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.08, 0], flow_tracker, RED, n=6,
                                  radius=0.09, speed=0.68, spread=0.12)

    bh = BAR_Y1 - BAR_Y0
    bar_frame = Rectangle(width=BAR_W, height=bh, stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.3).move_to([BAR_X, (BAR_Y0 + BAR_Y1) / 2, 0])
    ticks, tlabels = VGroup(), VGroup()
    for val in (0, 40, 80, 120):
        y = BAR_Y0 + (val / 120.0) * bh
        ticks.add(Line([BAR_X - BAR_W / 2 - 0.10, y, 0], [BAR_X - BAR_W / 2, y, 0], color=GREY, stroke_width=2.5))
        tlabels.add(M(str(val), size=24, color=TEXT).next_to([BAR_X - BAR_W / 2 - 0.12, y, 0], LEFT, buff=0.08))
    bar_ttl = T("brain fuel (g/day)", size=24, color=TEXT).move_to([BAR_X, BAR_Y0 - 0.48, 0])

    def _ket_fill():
        kg = float(np.clip(ket_g_tracker.get_value(), 0.0, 80.0))
        kh = max((kg / 120.0) * bh, 0.02)
        return Rectangle(
            width=BAR_W - 0.04, height=kh, stroke_color=GREEN, stroke_width=1.5,
            fill_color=GREEN, fill_opacity=0.82 if kg > 1 else 0.0
        ).move_to([BAR_X, BAR_Y1 - kh / 2, 0])

    def _gluc_outline():
        kg = float(np.clip(ket_g_tracker.get_value(), 0.0, 80.0))
        gg = 120.0 - kg
        gh = max((gg / 120.0) * bh, 0.02)
        return Rectangle(
            width=BAR_W - 0.04, height=gh, stroke_color=YELLOW, stroke_width=3,
            fill_color=YELLOW, fill_opacity=0.14
        ).move_to([BAR_X, BAR_Y0 + gh / 2, 0])

    ket_fill = always_redraw(_ket_fill)
    gluc_box = always_redraw(_gluc_outline)

    world = VGroup(scrubber, blood, brain, liver, muscle, bar_frame, gluc_box, ket_fill, ticks, tlabels, bar_ttl,
                   g_stream, k_stream, pink_stream, prot_stream)
    world.prot_stream = prot_stream
    return world


class S07Predict(SpokenScene):
    def construct(self):
        flow = ValueTracker(0.0)
        ket_g = ValueTracker(0.0)
        attach_flow_driver(self, flow)

        world = build_s07_world(flow, ket_g)
        self.add(world)

        self.at("about a third")
        self.play(ket_g.animate.set_value(80.0), run_time=2.8, rate_func=linear)
        y40 = BAR_Y0 + (40.0 / 120.0) * (BAR_Y1 - BAR_Y0)
        k_lab = T("ketones\ninstead", size=24, color=GREEN, line_spacing=0.85).move_to([BAR_X + 1.08, (y40 + BAR_Y1) / 2, 0])
        g40_lab = T("~40 g", size=24, color=YELLOW).move_to([BAR_X + 0.92, (BAR_Y0 + y40) / 2, 0])
        self.play(FadeIn(k_lab), FadeIn(g40_lab), run_time=0.8)

        self.at("fall to a third")
        q = question_card("Muscle's share: a third, or further?", y=-3.00)
        self.play(FadeIn(q.question), run_time=0.8)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Muscle's share: a third, or further?"
    CARD = {"y": -3.00}
    SECONDS = 4.5

    def backdrop(self):
        flow = ValueTracker(0.0)
        ket_g = ValueTracker(80.0)
        attach_flow_driver(self, flow)
        world = build_s07_world(flow, ket_g)
        y40 = BAR_Y0 + (40.0 / 120.0) * (BAR_Y1 - BAR_Y0)
        k_lab = T("ketones\ninstead", size=24, color=GREEN, line_spacing=0.85).move_to([BAR_X + 1.08, (y40 + BAR_Y1) / 2, 0])
        g40_lab = T("~40 g", size=24, color=YELLOW).move_to([BAR_X + 0.92, (BAR_Y0 + y40) / 2, 0])
        return VGroup(world, k_lab, g40_lab)


class S09Answer(SpokenScene):
    def construct(self):
        flow = ValueTracker(0.0)
        ket_g = ValueTracker(80.0)
        attach_flow_driver(self, flow)

        world = build_s07_world(flow, ket_g)
        y40 = BAR_Y0 + (40.0 / 120.0) * (BAR_Y1 - BAR_Y0)
        k_lab = T("ketones\ninstead", size=24, color=GREEN, line_spacing=0.85).move_to([BAR_X + 1.08, (y40 + BAR_Y1) / 2, 0])
        g40_lab = T("~40 g", size=24, color=YELLOW).move_to([BAR_X + 0.92, (BAR_Y0 + y40) / 2, 0])
        q = question_card("Muscle's share: a third, or further?", y=-3.00)

        self.add(world, k_lab, g40_lab, q)
        self.play(FadeOut(q), run_time=0.45)

        self.at("about a fifth")
        bh = BAR_Y1 - BAR_Y0
        ghost_h = (102.5 / 120.0) * bh
        ghost_x = 1.95
        ghost = Rectangle(
            width=0.44, height=ghost_h, stroke_color=RED, stroke_width=2.5,
            fill_color=RED, fill_opacity=0.22
        ).move_to([ghost_x, BAR_Y0 + ghost_h / 2, 0])
        ghost_tag = T("old\n102.5 g", size=22, color=RED, line_spacing=0.85).next_to(ghost, UP, buff=0.14)
        thin_prot = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.08, 0], flow, RED, n=3, radius=0.048, speed=0.55)
        self.play(FadeIn(ghost), FadeIn(ghost_tag), run_time=1.4)
        world.remove(world.prot_stream)
        self.add(thin_prot)

        self.at("glycerol still covers")
        gh = (17.5 / 120.0) * bh
        ph_new = (22.5 / 120.0) * bh
        g_band = Rectangle(
            width=BAR_W - 0.04, height=gh, stroke_color=PALE_TEAL, stroke_width=1.5,
            fill_color=PALE_TEAL, fill_opacity=0.90
        ).move_to([BAR_X, BAR_Y0 + gh / 2, 0])
        p_new = Rectangle(
            width=BAR_W - 0.04, height=ph_new, stroke_color=RED, stroke_width=1.5,
            fill_color=RED, fill_opacity=0.88
        ).move_to([BAR_X, BAR_Y0 + gh + ph_new / 2, 0])
        g_lab = T("glycerol\n15–20 g", size=22, color=PALE_TEAL, line_spacing=0.85).move_to([BAR_X + 1.06, BAR_Y0 + gh / 2, 0])
        fifth_lab = T("about 1/5", size=24, color=RED).move_to([ghost_x, BAR_Y0 - 0.36, 0])
        self.play(FadeOut(g40_lab, run_time=0.35))
        self.play(FadeIn(g_band), FadeIn(p_new), FadeIn(g_lab), FadeIn(fifth_lab), run_time=1.5)

        self.at("whole cut")
        cut_arr = Arrow([BAR_X - BAR_W / 2 - 0.06, -0.62, 0],
                        [ghost_x + 0.28, -0.62, 0],
                        color=GREEN, stroke_width=4, buff=0)
        cut_lab = T("−80 g\ncut", size=24, color=GREEN, line_spacing=0.85).move_to([2.90, -1.06, 0])
        self.play(GrowArrow(cut_arr), FadeIn(cut_lab), run_time=1.0)
        self.finish()


class S10FatAndHedge(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(4.0)
        flow = ValueTracker(0.0)
        days = ValueTracker(0.0)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box()
        bbar = build_brain_bar(ket_g=80.0, glyc_g=17.5, prot_g=22.5, title_text="brain fuel\n(g/day)")
        liver = build_liver(glycogen_frac=ValueTracker(0.08), show_new_glucose=True)

        mx = -1.45
        fx = 1.65
        m_box = RoundedRectangle(corner_radius=0.16, width=2.25, height=1.10, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13).move_to([mx, -1.00, 0])
        m_lab = T("muscle", size=26, color=TEXT).move_to([mx, -0.68, 0])
        m_blk = Rectangle(width=1.70, height=0.40, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.80).move_to([mx, -1.20, 0])
        muscle = VGroup(m_box, m_lab, m_blk)

        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=6, radius=0.065, speed=0.48)
        k_stream = make_dot_stream([-3.15, 2.20, 0], [3.10, 1.96, 0], flow, GREEN, n=7, radius=0.072, speed=0.48)
        pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=5, radius=0.075, speed=0.68, edge_color=PINK)
        thin_prot = make_dot_stream([mx + 0.15, -0.42, 0], [mx + 0.15, 0.08, 0], flow, RED, n=3, radius=0.05, speed=0.55)

        self.add(scrubber, blood, brain, bbar, liver, muscle, g_stream, k_stream, pink_stream, thin_prot)

        self.at("the fat")
        f_box = RoundedRectangle(corner_radius=0.16, width=2.25, height=1.10, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13).move_to([fx, -1.00, 0])
        f_lab = T("fat", size=26, color=TEXT).move_to([fx, -0.68, 0])
        f_blk = Rectangle(width=1.70, height=0.40, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.75).move_to([fx, -1.20, 0])
        f_days = T("~75 days of energy", size=24, color=TEAL).move_to([fx, -0.22, 0])
        fat = VGroup(f_box, f_lab, f_blk, f_days)
        self.play(FadeIn(fat, shift=LEFT * 0.4), run_time=1.0)

        self.at("runs out before")
        bw = 2.00
        m_frame = Rectangle(width=bw, height=0.34, stroke_color=RED, stroke_width=2.5).move_to([mx, -2.05, 0])
        f_frame = Rectangle(width=bw, height=0.34, stroke_color=TEAL, stroke_width=2.5).move_to([fx, -2.05, 0])

        def _m_bar():
            rem = max(1.0 - (days.get_value() * 39.5) / 10000.0, 0.05)
            w = bw * rem
            return Rectangle(width=w, height=0.30, stroke_width=0, fill_color=RED, fill_opacity=0.85).move_to([mx - bw / 2 + w / 2, -2.05, 0])

        def _f_bar():
            rem = max(1.0 - days.get_value() / 75.0, 0.02)
            w = bw * rem
            return Rectangle(width=w, height=0.30, stroke_width=0, fill_color=TEAL, fill_opacity=0.85).move_to([fx - bw / 2 + w / 2, -2.05, 0])

        m_fill = always_redraw(_m_bar)
        f_fill = always_redraw(_f_bar)
        day_lbl = counter("day {:.0f} (schematic)", days, at=[0.10, -2.50, 0], size=24, color=TEXT)
        self.play(FadeIn(m_frame), FadeIn(f_frame), run_time=0.4)
        self.add(m_fill, f_fill, day_lbl)
        self.play(days.animate.set_value(75.0), run_time=2.5, rate_func=linear)
        out_tag = T("fat runs out first", size=24, color=TEAL).move_to([fx, -2.96, 0])
        self.play(FadeIn(out_tag), run_time=0.5)

        self.at("direction and size")
        rtag = scope_tag("rough sums", color=GOLD)
        self.play(FadeIn(rtag), run_time=0.8)

        self.at("measured protein loss")
        meas_stream = make_dot_stream([mx + 0.15, -0.42, 0], [mx + 0.15, 0.08, 0], flow, RED, n=2, radius=0.038, speed=0.45)
        meas_lab = T("measured: ~20 g/day", size=24, color=RED).move_to([mx - 0.15, -2.96, 0])
        self.remove(thin_prot)
        self.add(meas_stream)
        self.play(FadeIn(meas_lab), run_time=2.0)
        self.finish()


class S11FiveWeeks(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(3.5)
        flow = ValueTracker(0.0)
        pie_k = ValueTracker(0.0)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box(ketone_share_tracker=pie_k)
        bbar = build_brain_bar(ket_g=80.0, glyc_g=17.5, prot_g=22.5, title_text="brain fuel\n(g/day)")
        liver = build_liver(glycogen_frac=ValueTracker(0.06), show_new_glucose=True)
        muscle = build_muscle()

        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=5, radius=0.06, speed=0.48)
        k_stream = make_dot_stream([-3.15, 2.20, 0], [3.10, 1.96, 0], flow, GREEN, n=7, radius=0.072, speed=0.48)
        pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=6, radius=0.078, speed=0.68, edge_color=PINK)
        thin_prot = make_dot_stream([-1.05, -0.50, 0], [-1.05, 0.08, 0], flow, RED, n=2, radius=0.045, speed=0.50)

        self.add(scrubber, blood, brain, bbar, liver, muscle, g_stream, k_stream, pink_stream, thin_prot)
        self.play(t_idx.animate.set_value(4.0), run_time=1.6, rate_func=linear)

        self.at("barely moved")
        y4 = TUBE_Y0 + (4.0 / 8.0) * (TUBE_Y1 - TUBE_Y0)
        lvl_line = Line([TUBE_X0 + 0.08, y4, 0], [TUBE_X1 - 0.08, y4, 0], color=YELLOW, stroke_width=4)
        self.play(blood.g_bar.animate.set_stroke(YELLOW, width=5), Create(lvl_line), run_time=1.8)

        self.at("brain runs")
        pie_lab = T("~2/3 ketones", size=24, color=GREEN).move_to([BRAIN_CENTER[0], BRAIN_CENTER[1] + 0.80, 0])
        self.play(pie_k.animate.set_value(2.0 / 3.0), FadeIn(pie_lab), run_time=2.4)

        self.at("the kidney")
        kidney = build_kidney()
        kid_stream = make_dot_stream([0.42, -0.14, 0], [-3.20, -0.14, 0], flow, YELLOW, n=6,
                                     radius=0.078, speed=0.68, edge_color=PINK)
        eq_sign = T("=", size=34, color=PINK).move_to([-2.68, 0.865, 0])
        eq_lab = T("about\nequal", size=22, color=TEXT, line_spacing=0.82).move_to([-2.68, 0.395, 0])
        self.play(FadeIn(kidney), FadeIn(eq_sign), FadeIn(eq_lab), run_time=1.5)
        self.add(kid_stream)

        self.at("muscle pays")
        ghost_stream = DashedLine([-1.25, -0.50, 0], [-1.25, 0.08, 0], color=RED, stroke_width=6).set_opacity(0.35)
        ghost_r = DashedLine([-0.85, -0.50, 0], [-0.85, 0.08, 0], color=RED, stroke_width=6).set_opacity(0.35)
        frac_lab = T("~1/5 of old bill", size=24, color=RED).move_to([MUSCLE_CENTER[0], -2.42, 0])
        self.play(Create(ghost_stream), Create(ghost_r), FadeIn(frac_lab), run_time=1.5)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        t_idx = ValueTracker(1.0)
        flow = ValueTracker(0.0)
        glyc = ValueTracker(1.0)
        pie_k = ValueTracker(0.0)
        m_size = ValueTracker(0.055)
        attach_flow_driver(self, flow)

        scrubber = build_scrubber(t_idx)
        blood = build_blood_tube(t_idx, flow)
        brain = build_brain_box(ketone_share_tracker=pie_k)
        bbar_base = build_brain_bar(ket_g=0.0, glyc_g=0.0, prot_g=0.0, gluc_outline_g=0.0, title_text="brain fuel\n(g/day)")
        bh = BAR_Y1 - BAR_Y0

        def _bbar_fills():
            kf = float(np.clip(pie_k.get_value(), 0.0, 1.0))
            parts = VGroup()
            if kf < 0.999:
                gh = (1.0 - kf) * bh
                parts.add(Rectangle(
                    width=BAR_W - 0.04, height=gh, stroke_color=YELLOW, stroke_width=2.0,
                    fill_color=YELLOW, fill_opacity=0.78
                ).move_to([BAR_X, BAR_Y0 + gh / 2, 0]))
            if kf > 0.005:
                kh = kf * bh
                parts.add(Rectangle(
                    width=BAR_W - 0.04, height=kh, stroke_color=GREEN, stroke_width=1.5,
                    fill_color=GREEN, fill_opacity=0.82
                ).move_to([BAR_X, BAR_Y1 - kh / 2, 0]))
            return parts

        bbar = VGroup(bbar_base, always_redraw(_bbar_fills))
        liver = build_liver(glycogen_frac=glyc, show_new_glucose=True)
        muscle = build_muscle()
        fat = build_fat()

        y4 = TUBE_Y0 + (4.0 / 8.0) * (TUBE_Y1 - TUBE_Y0)
        lvl_line = Line([TUBE_X0 + 0.08, y4, 0], [TUBE_X1 - 0.08, y4, 0], color=YELLOW, stroke_width=4)
        lvl_lab = T("nearly\nlevel", size=22, color=YELLOW, line_spacing=0.82).move_to([-2.68, y4 + 0.30, 0])

        g_stream = make_dot_stream([-3.15, 2.40, 0], [3.10, 2.16, 0], flow, YELLOW, n=6, radius=0.068, speed=0.48)
        pink_stream = make_dot_stream([-2.20, 1.05, 0], [-3.20, 1.05, 0], flow, YELLOW, n=6, radius=0.078, speed=0.68, edge_color=PINK)

        m_dots = VGroup(*[Dot(radius=0.06, color=RED) for _ in range(5)])
        def _upd_m(mob):
            ph = flow.get_value()
            r = m_size.get_value()
            for i, d in enumerate(mob):
                frac = (i / 5 + ph * 0.65) % 1.0
                d.set_height(r * 2)
                d.move_to([-1.05, -0.50 + frac * 0.58, 0])
        m_dots.add_updater(_upd_m)
        m_dots.layout_ok = True

        self.add(scrubber, blood, brain, bbar, liver, muscle, fat, lvl_line, lvl_lab, g_stream, pink_stream, m_dots)

        self.at("number in the blood")
        self.play(blood.g_bar.animate.set_stroke(YELLOW, width=5), run_time=2.4)

        self.at("glycogen pays")
        self.play(t_idx.animate.set_value(2.0), glyc.animate.set_value(0.08), run_time=1.0, rate_func=linear)

        self.at("then muscle protein")
        self.play(t_idx.animate.set_value(3.0), m_size.animate.set_value(0.10), run_time=1.8, rate_func=linear)

        self.at("then fat")
        fa_stream = make_dot_stream([1.35, -0.62, 0], [0.55, 0.38, 0], flow, TEAL, n=5, radius=0.068, speed=0.62)
        k_stream = make_dot_stream([-3.15, 2.20, 0], [3.10, 1.96, 0], flow, GREEN, n=7, radius=0.072, speed=0.48)
        self.add(fa_stream, k_stream)
        self.play(
            t_idx.animate.set_value(4.0),
            m_size.animate.set_value(0.042),
            pie_k.animate.set_value(2.0 / 3.0),
            run_time=3.0,
            rate_func=linear
        )
        self.finish()


class S13End(EndCard):
    LINE = "Blood glucose holds steady while the body rewrites who pays for it."
