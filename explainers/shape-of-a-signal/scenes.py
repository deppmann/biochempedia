"""Reading a Signal in Time — animation for shape-of-a-signal.

COLOUR MAP (one colour per concept, carried across every scene):
  AMBER  (#F5A623) : upstream signal (EGF, NGF, ERK, Ca2+ spikes)
  TEAL   (#3FB8C0) : decoder / delayed protein / unstabilized c-Fos / decay clock
  ACTIVE (#5CE08A) : active or stabilized output (cell fate, protected c-Fos, stacked decoder)
  CORAL  (#FC6255) : decay, fast breakdown, leaky droplets, broken timer
  STRUCT (#8B93A1) : carried lane frames, axes, ticks
  TEXT   (#E8EAF0) : primary labels, titles, equations

CARRIED WORLD:
  A full-frame two-lane timeline (SIGNAL amber lane on top, DECODER teal lane on bottom)
  carrying the biological signal above and the downstream decoder's response below.

PER-SCENE MOTION & COMPUTATION:
  s01_hook             : EGF->ERK drives cell division (computed pinch & split); NGF->ERK drives neurite branching (computed branch extension).
  s02_four_features    : Two-lane world forms; 4 signal features grow/sweep in top lane; decoder clock ticks in bottom lane.
  s03_duration_erk     : Computed brief EGF vs long NGF ERK curves trace live; vertical comparison clock sweeps into delayed product curve.
  s04_cfos_mechanism   : Slow/fast routes connect ERK to c-Fos; brief run decays with coral fragments; long run stabilizes into green curve.
  s05_predict_q        : Brief EGF pulse sweeps top lane; shielded mutant c-Fos emerges; dashed green vs coral candidate curves draw live.
  s06_pause            : PredictPause holds question and backdrop while the 4.5 s countdown ring sweeps continuously.
  s07_predict_reveal   : Solid green c-Fos curve climbs past ERK shutoff while coral curve clears; top lane morphs into Ca2+ spike train.
  s08_frequency_bucket : Live leaky-bucket water level and bottom decoder curve driven by exact spike-plus-exponential-decay math.
  s09_frequency_math   : Exact y(t) = sum 2^(-(t - t_i)/30) curves draw live for 120 s (6%) vs 15 s (71%) gaps with synced tracker dots.
  s10_wrap             : Side-by-side duration (ERK/c-Fos) and frequency (Ca2+ staircase) traces draw live around a ticking decoder clock.
"""
from bp_parts import *  # noqa: F401,F403

# Concept colours
AMBER = "#F5A623"
TEAL_DEC = TEAL       # "#3FB8C0"
ACTIVE = "#5CE08A"
CORAL = RED           # "#FC6255"
STRUCT = GREY         # "#8B93A1"


# ------------------------------------------------------------------ computed signal & decoder functions
def erk_brief(t):
    """Brief EGF-driven ERK pulse peaking near t=1.2 and returning to 0 by t=3.2."""
    if t <= 0.3:
        return 0.0
    u = t - 0.3
    val = (u / 0.7) ** 2 * np.exp(2.0 * (1.0 - u / 0.7))
    return float(np.clip(val, 0.0, 1.0))


def erk_long(t):
    """Long NGF-driven ERK plateau rising by t=1.2 and staying high past t=8.5."""
    if t <= 0.3:
        return 0.0
    rise = 1.0 - np.exp(-((t - 0.3) / 0.45) ** 2)
    fall = 1.0 / (1.0 + np.exp((t - 8.8) / 0.35))
    return float(np.clip(0.96 * rise * fall, 0.0, 1.0))


def delayed_product(t):
    """Delayed protein transcription/translation curve rising around t=4.2..7.5."""
    if t <= 3.4:
        return 0.0
    return float(0.82 / (1.0 + np.exp(-(t - 5.2) / 0.55)))


def cfos_unstable_after_brief(t):
    """Fresh c-Fos appears after brief ERK shuts off and breaks down quickly."""
    if t <= 3.5:
        return 0.0
    u = t - 3.5
    val = 0.32 * (u / 1.1) ** 2 * np.exp(2.0 * (1.0 - u / 1.1))
    return float(np.clip(val, 0.0, 1.0))


def cfos_stabilized_after_long(t):
    """Long ERK stays on to phosphorylate c-Fos, turning it stable and rising."""
    if t <= 3.5:
        return 0.0
    return float(0.98 / (1.0 + np.exp(-(t - 5.3) / 0.65)))


def cfos_mutant_after_brief(t):
    """Always-stable mutant c-Fos builds up even after a brief ERK pulse."""
    if t <= 3.5:
        return 0.0
    return float(0.94 / (1.0 + np.exp(-(t - 5.3) / 0.65)))


def exp_train(t, spike_times, half_time):
    """Exact leaky-bucket / exponential decay sum: sum of 2^(-(t - t_i)/half_time) for t_i <= t."""
    total = 0.0
    for ti in spike_times:
        if t >= ti:
            total += 2.0 ** (-(t - ti) / half_time)
    return float(total)


def spike_train_y(t, spike_times, width=0.14):
    """Sharp brief calcium spike pulse train of unit height."""
    val = 0.0
    for ti in spike_times:
        val = max(val, float(np.exp(-((t - ti) / width) ** 2)))
    return val


# ------------------------------------------------------------------ shared visual builders
def two_lane_frame(top_y=(0.35, 2.55), bot_y=(-2.35, -0.15), x_range=(-6.0, 6.0),
                   top_title="SIGNAL", bot_title="DECODER"):
    """Build the carried two-lane timeline container."""
    x0, x1 = x_range
    w = x1 - x0
    cx = (x0 + x1) / 2.0
    th = top_y[1] - top_y[0]
    tcy = (top_y[0] + top_y[1]) / 2.0
    bh = bot_y[1] - bot_y[0]
    bcy = (bot_y[0] + bot_y[1]) / 2.0

    top_box = RoundedRectangle(
        corner_radius=0.16, width=w, height=th,
        stroke_color=AMBER, stroke_width=2.2, fill_color=AMBER, fill_opacity=0.06,
    ).move_to([cx, tcy, 0])
    bot_box = RoundedRectangle(
        corner_radius=0.16, width=w, height=bh,
        stroke_color=TEAL_DEC, stroke_width=2.2, fill_color=TEAL_DEC, fill_opacity=0.06,
    ).move_to([cx, bcy, 0])

    t_lab = T(top_title, 24, AMBER, weight=BOLD).move_to(
        [x0 + 0.25, top_y[1] - 0.24, 0], aligned_edge=LEFT
    )
    b_lab = T(bot_title, 24, TEAL_DEC, weight=BOLD).move_to(
        [x0 + 0.25, bot_y[1] - 0.24, 0], aligned_edge=LEFT
    )
    g = VGroup(top_box, bot_box, t_lab, b_lab)
    g.top_box, g.bot_box = top_box, bot_box
    g.top_lab, g.bot_lab = t_lab, b_lab
    return g


def area_under(plot, fn, tracker, color, x0=None, opacity=0.30):
    """Live filled polygon between a curve and y=0 up to tracker."""
    x0 = plot.xr[0] if x0 is None else x0

    def mk():
        x1 = tracker.get_value()
        if x1 - x0 <= 1e-4:
            return VMobject(stroke_width=0, fill_opacity=0)
        n = max(6, int(100 * (x1 - x0) / (plot.xr[1] - plot.xr[0])) + 2)
        xs = np.linspace(x0, x1, n)
        pts = [plot.pt(x0, plot.yr[0])]
        for x in xs:
            y = float(np.clip(fn(x), plot.yr[0], plot.yr[1]))
            pts.append(plot.pt(x, y))
        pts.append(plot.pt(x1, plot.yr[0]))
        return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)

    return always_redraw(mk)


def clock_icon(center, radius=0.65, color=TEAL_DEC, angle_tracker=None):
    """A crisp analog clock with live rotating hand tied to angle_tracker (radians clockwise)."""
    c = np.array(center, dtype=float)
    rim = Circle(radius=radius, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.10).move_to(c)
    ticks = VGroup()
    for k in range(12):
        ang = k * TAU / 12.0
        p0 = c + radius * 0.80 * np.array([np.cos(ang), np.sin(ang), 0])
        p1 = c + radius * 0.94 * np.array([np.cos(ang), np.sin(ang), 0])
        ticks.add(Line(p0, p1, color=color, stroke_width=2.5 if k % 3 == 0 else 1.5))
    pivot = Dot(c, radius=0.055, color=TEXT)

    if angle_tracker is None:
        angle_tracker = ValueTracker(0.0)

    def mk_hand():
        a = PI / 2.0 - angle_tracker.get_value()
        tip = c + radius * 0.68 * np.array([np.cos(a), np.sin(a), 0])
        return Line(c, tip, color=TEXT, stroke_width=4.0)

    hand = always_redraw(mk_hand)
    return VGroup(rim, ticks, hand, pivot)


def top_right_tag(text="schematic", size=24, color=STRUCT):
    """Scope tag placed in top-right safe corner when bottom-right holds a countdown ring."""
    t = T(text, size, color)
    return t.move_to([FRAME_X - 0.2 - t.width / 2, FRAME_Y - 0.28 - t.height / 2, 0])


# ------------------------------------------------------------------ S00 Title
class S00Title(TitleCard):
    LESSON = "The Shape of a Signal: Size, Duration, Frequency and Place"
    TITLE = "Reading a Signal in Time"


# ------------------------------------------------------------------ S01 Hook
class S01Hook(SpokenScene):
    def construct(self):
        head = T("Two growth factors, one kinase", 34, TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        cell_shell = RoundedRectangle(
            corner_radius=0.45, width=11.8, height=4.9,
            stroke_color=TEAL_DEC, stroke_width=3.0, fill_color=TEAL_DEC, fill_opacity=0.06,
        ).move_to([0, 0.05, 0])
        mid_bot = DashedLine([0, 0.90, 0], [0, -2.35, 0], color=STRUCT, stroke_width=2.5, dash_length=0.14)
        cell_lbl = T("PC12 cell", 24, TEAL_DEC).move_to([-4.95, 2.22, 0])

        egf = chip("EGF", AMBER, size=28).move_to([-4.6, 1.48, 0])
        erk_l = chip("ERK", AMBER, size=30).move_to([-2.1, 1.48, 0])
        arr_egf = Arrow(egf.get_right() + RIGHT * 0.1, erk_l.get_left() + LEFT * 0.1, buff=0, color=AMBER, stroke_width=4)

        ngf = chip("NGF", AMBER, size=28).move_to([1.6, 1.48, 0])
        erk_r = chip("ERK", AMBER, size=30).move_to([4.1, 1.48, 0])
        arr_ngf = Arrow(ngf.get_right() + RIGHT * 0.1, erk_r.get_left() + LEFT * 0.1, buff=0, color=AMBER, stroke_width=4)

        div_t = ValueTracker(0.0)

        def mk_div_cell():
            p = div_t.get_value()
            cx, cy = -3.0, -0.78
            sep = 0.72 * p
            r = 0.64 - 0.13 * p
            c1 = Circle(radius=r, stroke_color=ACTIVE, stroke_width=3.5, fill_color=ACTIVE, fill_opacity=0.22).move_to([cx - sep, cy, 0])
            c2 = Circle(radius=r, stroke_color=ACTIVE, stroke_width=3.5, fill_color=ACTIVE, fill_opacity=0.22).move_to([cx + sep, cy, 0])
            n1 = Dot([cx - sep, cy, 0], radius=0.12, color=TEXT)
            n2 = Dot([cx + sep, cy, 0], radius=0.12, color=TEXT)
            if p < 0.08:
                return VGroup(c1, n1)
            return VGroup(c1, c2, n1, n2)

        div_cell = always_redraw(mk_div_cell)
        arr_div = Arrow([-2.1, 0.96, 0], [-2.75, 0.06, 0], buff=0, color=ACTIVE, stroke_width=3.5)
        lbl_div = T("Divide", 28, ACTIVE, weight=BOLD).move_to([-3.0, -2.06, 0])

        diff_t = ValueTracker(0.0)
        branch_angles = [0.22, -0.32, -0.85, -2.30, 2.75]
        branch_lens = [1.10, 1.15, 0.65, 0.68, 1.10]

        def mk_diff_cell():
            p = diff_t.get_value()
            cx, cy = 3.1, -0.68
            r = 0.50 - 0.09 * p
            soma = Circle(radius=r, stroke_color=ACTIVE, stroke_width=3.5, fill_color=ACTIVE, fill_opacity=0.22).move_to([cx, cy, 0])
            nuc = Dot([cx, cy, 0], radius=0.12, color=TEXT)
            branches = VGroup()
            if p > 0.02:
                for ang, bl in zip(branch_angles, branch_lens):
                    d = np.array([np.cos(ang), np.sin(ang), 0])
                    s_pt = np.array([cx, cy, 0]) + r * d
                    e_pt = s_pt + (bl * p) * d
                    branches.add(Line(s_pt, e_pt, color=ACTIVE, stroke_width=4.0))
                    if p > 0.5:
                        sub_p = (p - 0.5) / 0.5
                        for side in (-0.38, 0.38):
                            sd = np.array([np.cos(ang + side), np.sin(ang + side), 0])
                            branches.add(Line(e_pt, e_pt + (0.28 * sub_p) * sd, color=ACTIVE, stroke_width=2.8))
            return VGroup(branches, soma, nuc)

        diff_cell = always_redraw(mk_diff_cell)
        arr_diff = Arrow([4.1, 0.96, 0], [3.45, 0.06, 0], buff=0, color=ACTIVE, stroke_width=3.5)
        lbl_diff = T("Differentiate", 28, ACTIVE, weight=BOLD).move_to([3.1, -2.06, 0])

        q_badge = chip("?", AMBER, size=34).move_to([0, 1.48, 0])

        self.add(cell_shell, mid_bot, cell_lbl, head, tag, div_cell, diff_cell)
        self.play(FadeIn(egf), FadeIn(ngf), run_time=0.9)

        self.at("switch on")
        self.play(GrowArrow(arr_egf), GrowArrow(arr_ngf), FadeIn(erk_l), FadeIn(erk_r), run_time=2.2)

        self.at("inside one cell")
        self.play(FadeIn(q_badge), run_time=1.2)

        self.at("order division")
        self.play(GrowArrow(arr_div), div_t.animate.set_value(1.0), FadeIn(lbl_div), run_time=1.6)

        self.at("nerve like branches")
        self.play(GrowArrow(arr_diff), diff_t.animate.set_value(1.0), FadeIn(lbl_diff), run_time=2.2)

        self.at("molecule is identical")
        eq_l = T("identical", 24, AMBER).move_to([0, 2.22, 0])
        self.play(
            erk_l.animate.set_stroke(GOLD, 4),
            erk_r.animate.set_stroke(GOLD, 4),
            FadeIn(eq_l),
            run_time=1.4,
        )

        self.at("carry the difference")
        sig_t = ValueTracker(0.0)
        sig_base = Line([-4.5, -2.95, 0], [4.5, -2.95, 0], color=STRUCT, stroke_width=2.0)

        def mk_sig_hint():
            u = sig_t.get_value()
            xs = np.linspace(0.0, max(u, 0.05), max(4, int(60 * u) + 2))
            pts = []
            for x in xs:
                px = -4.5 + 9.0 * x
                py = -2.95 + 0.34 * np.exp(-((x - 0.25) / 0.08) ** 2) + 0.28 * np.exp(-((x - 0.65) / 0.16) ** 2)
                pts.append([px, py, 0])
            m = VMobject(stroke_color=AMBER, stroke_width=4.0)
            m.set_points_as_corners(pts)
            return m

        sig_hint = always_redraw(mk_sig_hint)
        self.add(sig_base, sig_hint)
        self.play(sig_t.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S02 Four Features
class S02FourFeatures(SpokenScene):
    def construct(self):
        head = T("Four features of a signal", 34, TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")
        world = two_lane_frame()

        msg_badge = chip("same messenger", AMBER, size=28).move_to([-3.65, 1.40, 0])
        id_note = T("identity is only part of the message", 26, TEXT).move_to([1.95, 1.40, 0])

        self.add(head, tag, world)
        self.play(FadeIn(msg_badge), run_time=1.0)
        self.at("identity is only")
        self.play(FadeIn(id_note), run_time=1.2)
        self.wait(1.2)
        self.play(FadeOut(msg_badge), FadeOut(id_note), run_time=0.45)

        self.at("four features")

        bar_t = ValueTracker(0.01)

        def mk_bars():
            s = bar_t.get_value()
            b1 = Rectangle(width=0.38, height=1.20 * s, stroke_color=AMBER, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.35)
            b2 = Rectangle(width=0.38, height=0.42 * s, stroke_color=AMBER, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.35)
            b1.move_to([-4.45, 0.90 + 0.60 * s, 0])
            b2.move_to([-3.85, 0.90 + 0.21 * s, 0])
            return VGroup(b1, b2)

        bars = always_redraw(mk_bars)
        lbl_much = T("How much", 26, AMBER, weight=BOLD).move_to([-4.15, 0.60, 0])

        plat_t = ValueTracker(0.01)

        def mk_plats():
            s = plat_t.get_value()
            p1 = RoundedRectangle(corner_radius=0.06, width=0.45 * s, height=0.34, stroke_color=AMBER, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.35)
            p2 = RoundedRectangle(corner_radius=0.06, width=1.65 * s, height=0.34, stroke_color=AMBER, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.35)
            p1.move_to([-2.35 + 0.225 * s, 1.85, 0])
            p2.move_to([-2.35 + 0.825 * s, 1.25, 0])
            return VGroup(p1, p2)

        plats = always_redraw(mk_plats)
        lbl_long = T("How long", 26, AMBER, weight=BOLD).move_to([-1.45, 0.60, 0])

        spk_t = ValueTracker(0.01)

        def mk_spikes():
            s = spk_t.get_value()
            g = VGroup()
            for row_y, xs in ((1.85, [0.45, 1.55]), (1.22, [0.35, 0.70, 1.05, 1.40, 1.75])):
                pts = [[0.2, row_y, 0]]
                for x in xs:
                    if x <= 0.2 + 1.8 * s:
                        pts.extend([[x - 0.06, row_y, 0], [x, row_y + 0.34, 0], [x + 0.06, row_y, 0]])
                pts.append([0.2 + 1.8 * s, row_y, 0])
                m = VMobject(stroke_color=AMBER, stroke_width=3.5)
                m.set_points_as_corners(pts)
                g.add(m)
            return g

        spikes = always_redraw(mk_spikes)
        lbl_often = T("How often", 26, AMBER, weight=BOLD).move_to([1.25, 0.60, 0])

        ring_w = Circle(radius=0.58, stroke_color=STRUCT, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.08).move_to([4.25, 1.50, 0])
        loc_dot = Dot([4.62, 1.65, 0], radius=0.14, color=AMBER)
        loc_halo = Circle(radius=0.25, stroke_color=AMBER, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.22).move_to([4.62, 1.65, 0])
        lbl_where = T("Where", 26, AMBER, weight=BOLD).move_to([4.25, 0.60, 0])

        self.at("how much")
        self.add(bars)
        self.play(bar_t.animate.set_value(1.0), FadeIn(lbl_much), run_time=0.55)

        self.at("how long")
        self.add(plats)
        self.play(plat_t.animate.set_value(1.0), FadeIn(lbl_long), run_time=0.55)

        self.at("how often")
        self.add(spikes)
        self.play(spk_t.animate.set_value(1.0), FadeIn(lbl_often), run_time=0.55)

        self.at("and where")
        self.play(FadeIn(ring_w), GrowFromCenter(loc_halo), GrowFromCenter(loc_dot), FadeIn(lbl_where), run_time=0.65)

        self.at("reading time")
        dec_box = chip("Decoder", TEAL_DEC, size=32).move_to([-1.4, -1.25, 0])
        arr_down = Arrow([0.0, 0.35, 0], [0.0, -0.15, 0], buff=0, color=TEAL_DEC, stroke_width=4.0)
        clk_ang = ValueTracker(0.0)
        clk = clock_icon([1.3, -1.25, 0], radius=0.68, color=TEAL_DEC, angle_tracker=clk_ang)
        spd_lbl = T("built-in speed", 28, TEAL_DEC).move_to([3.75, -1.25, 0])

        self.play(GrowArrow(arr_down), FadeIn(dec_box), FadeIn(clk), clk_ang.animate.set_value(TAU * 0.25), run_time=1.8, rate_func=linear)
        self.at("downstream protein")
        self.play(FadeIn(spd_lbl), clk_ang.animate.set_value(TAU * 1.0), run_time=3.5, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S03 Duration ERK
class S03DurationErk(SpokenScene):
    def construct(self):
        head = T("How long? Reading ERK duration", 34, TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")
        world = two_lane_frame(top_title="ERK", bot_title="DECODER")

        p_top = Plot(
            box=(-4.8, 5.5, 0.55, 1.98), xr=(0, 10), yr=(0, 1.15),
            xticks=[], yticks=[], xlabel="", ylabel="", color=STRUCT, stroke=2.5,
        )
        p_bot = Plot(
            box=(-4.8, 5.5, -1.78, -0.72), xr=(0, 10), yr=(0, 1.15),
            xticks=[], yticks=[], xlabel="", ylabel="", color=STRUCT, size=24, stroke=2.5,
        )
        time_lbl = T("time", 24, STRUCT).move_to([2.9, -2.06, 0])

        t_brief = ValueTracker(0.01)
        t_long = ValueTracker(0.01)
        t_del = ValueTracker(0.01)
        t_scan = ValueTracker(2.4)

        brief_curve = p_top.live_curve(erk_brief, t_brief, color=AMBER, width=5)
        brief_fill = area_under(p_top, erk_brief, t_brief, AMBER, opacity=0.22)
        long_curve = p_top.live_curve(erk_long, t_long, color=GOLD, width=6)
        long_fill = area_under(p_top, erk_long, t_long, GOLD, opacity=0.14)

        lbl_brief = T("EGF: brief ERK", 26, AMBER, weight=BOLD).move_to([-2.4, 2.24, 0])
        lbl_long = T("NGF: long ERK", 26, GOLD, weight=BOLD).move_to([3.1, 2.24, 0])

        self.add(head, tag, world, p_top, p_bot, time_lbl)
        # Sweep baseline slightly during intro ("Start with how long?") so frame is alive
        self.add(brief_fill, brief_curve)
        self.play(t_brief.animate.set_value(0.55), run_time=2.4, rate_func=linear)

        self.at("turns erk on briefly")
        self.play(t_brief.animate.set_value(10.0), FadeIn(lbl_brief), run_time=2.5, rate_func=linear)

        self.at("keeps erk on")
        self.add(long_fill, long_curve)
        self.play(t_long.animate.set_value(10.0), FadeIn(lbl_long), run_time=3.2, rate_func=linear)

        self.at("no stopwatch")
        sw_center = np.array([0.0, -1.24, 0])
        sw_ring = Circle(radius=0.40, stroke_color=STRUCT, stroke_width=3.0).move_to(sw_center)
        sw_hand = Line(sw_center, sw_center + UP * 0.26, color=STRUCT, stroke_width=3.0)
        sw_x1 = Line(sw_center + UL * 0.34, sw_center + DR * 0.34, color=CORAL, stroke_width=4.5)
        sw_x2 = Line(sw_center + UR * 0.34, sw_center + DL * 0.34, color=CORAL, stroke_width=4.5)
        sw_lbl = T("no stopwatch", 26, CORAL).next_to(sw_ring, RIGHT, buff=0.35)
        sw_grp = VGroup(sw_ring, sw_hand, sw_x1, sw_x2, sw_lbl)
        self.play(FadeIn(sw_grp), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(sw_grp), run_time=0.5)

        self.at("compares erk against")
        arr_drop = Arrow([0.0, 0.35, 0], [0.0, -0.15, 0], buff=0, color=TEAL_DEC, stroke_width=4.5)
        bot_delayed = T("Delayed product", 24, TEAL_DEC, weight=BOLD).move_to(world.bot_lab, aligned_edge=LEFT)
        scan_line = always_redraw(lambda: DashedLine(
            p_bot.pt(t_scan.get_value(), 0), p_top.pt(t_scan.get_value(), 1.05),
            color=TEXT, stroke_width=2.5, dash_length=0.14,
        ))
        del_curve = p_bot.live_curve(delayed_product, t_del, color=TEAL_DEC, width=6)
        del_fill = area_under(p_bot, delayed_product, t_del, TEAL_DEC, opacity=0.22)
        del_lbl = T("delayed protein", 24, TEAL_DEC, weight=BOLD).move_to([3.85, -0.58, 0])

        self.play(GrowArrow(arr_drop), swap(world.bot_lab, bot_delayed, run_time=0.6), run_time=0.6)
        self.add(scan_line, del_fill, del_curve)

        self.at("delayed protein")
        self.play(
            t_del.animate.set_value(10.0),
            t_scan.animate.set_value(6.2),
            FadeIn(del_lbl),
            run_time=4.2,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ S04 c-Fos Mechanism
class S04CfosMechanism(SpokenScene):
    def construct(self):
        head = T("How c-Fos times the ERK signal", 34, TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        top_l = RoundedRectangle(corner_radius=0.14, width=5.75, height=1.80, stroke_color=AMBER, stroke_width=2.0, fill_color=AMBER, fill_opacity=0.06).move_to([-3.05, 1.72, 0])
        top_r = RoundedRectangle(corner_radius=0.14, width=5.75, height=1.80, stroke_color=AMBER, stroke_width=2.0, fill_color=AMBER, fill_opacity=0.06).move_to([3.05, 1.72, 0])
        bot_l = RoundedRectangle(corner_radius=0.14, width=5.75, height=2.15, stroke_color=TEAL_DEC, stroke_width=2.0, fill_color=TEAL_DEC, fill_opacity=0.06).move_to([-3.05, -1.42, 0])
        bot_r = RoundedRectangle(corner_radius=0.14, width=5.75, height=2.15, stroke_color=TEAL_DEC, stroke_width=2.0, fill_color=TEAL_DEC, fill_opacity=0.06).move_to([3.05, -1.42, 0])

        lbl_l = T("Brief ERK (EGF)", 26, AMBER, weight=BOLD).move_to([-5.65, 2.34, 0], aligned_edge=LEFT)
        lbl_r = T("Long ERK (NGF)", 26, GOLD, weight=BOLD).move_to([0.45, 2.34, 0], aligned_edge=LEFT)
        lbl_bl = T("c-Fos", 24, TEAL_DEC, weight=BOLD).move_to([-5.65, -0.58, 0], aligned_edge=LEFT)
        lbl_br = T("c-Fos", 24, TEAL_DEC, weight=BOLD).move_to([0.45, -0.58, 0], aligned_edge=LEFT)

        p_tl = Plot(box=(-5.4, -0.5, 0.96, 2.02), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.0)
        p_tr = Plot(box=(0.7, 5.6, 0.96, 2.02), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.0)
        p_bl = Plot(box=(-5.4, -0.5, -2.28, -0.82), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.0)
        p_br = Plot(box=(0.7, 5.6, -2.28, -0.82), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.0)

        slow_path = CubicBezier(
            [-4.8, 0.80, 0], [-4.8, 0.35, 0], [-3.8, 0.35, 0], [-3.8, -0.22, 0],
            color=TEAL_DEC, stroke_width=3.5,
        )
        slow_tip = Arrow([-3.8, -0.15, 0], [-3.8, -0.34, 0], buff=0, color=TEAL_DEC, stroke_width=3.5)
        slow_lbl = T("Slow route: make c-Fos", 24, TEAL_DEC).move_to([-2.0, 0.24, 0])

        fast_arr = Arrow([1.95, 0.80, 0], [1.95, -0.34, 0], buff=0, color=ACTIVE, stroke_width=4.0)
        fast_lbl = T("Fast route: add phosphates", 24, ACTIVE).move_to([4.15, 0.24, 0])

        t_l = ValueTracker(0.01)
        t_r = ValueTracker(0.01)
        frag_t = ValueTracker(0.0)

        c_tl = p_tl.live_curve(erk_brief, t_l, color=AMBER, width=5)
        f_tl = area_under(p_tl, erk_brief, t_l, AMBER, opacity=0.30)
        dot_tl = p_tl.dot(lambda: t_l.get_value(), lambda: erk_brief(t_l.get_value()), color=TEXT, ring=AMBER, radius=0.09)
        c_bl = p_bl.live_curve(cfos_unstable_after_brief, t_l, color=TEAL_DEC, width=5)
        f_bl = area_under(p_bl, cfos_unstable_after_brief, t_l, TEAL_DEC, opacity=0.30)
        dot_bl = p_bl.dot(lambda: t_l.get_value(), lambda: cfos_unstable_after_brief(t_l.get_value()), color=TEXT, ring=TEAL_DEC, radius=0.09)

        c_tr = p_tr.live_curve(erk_long, t_r, color=GOLD, width=5)
        f_tr = area_under(p_tr, erk_long, t_r, GOLD, opacity=0.24)
        dot_tr = p_tr.dot(lambda: t_r.get_value(), lambda: erk_long(t_r.get_value()), color=TEXT, ring=GOLD, radius=0.09)

        def mk_br_curve():
            u = t_r.get_value()
            col = ACTIVE if u >= 4.6 else TEAL_DEC
            m = VMobject(stroke_color=col, stroke_width=5, fill_opacity=0)
            if u > 0.05:
                xs = np.linspace(0, u, max(4, int(90 * u / 10.0) + 2))
                pts = [p_br.pt(x, cfos_stabilized_after_long(x)) for x in xs]
                if len(pts) >= 2:
                    m.set_points_as_corners(pts)
            return m

        def mk_br_fill():
            x1 = t_r.get_value()
            if x1 <= 1e-4:
                return VMobject(stroke_width=0, fill_opacity=0)
            col = ACTIVE if x1 >= 4.6 else TEAL_DEC
            n = max(6, int(100 * x1 / 10.0) + 2)
            xs = np.linspace(0, x1, n)
            pts = [p_br.pt(0, 0)]
            for x in xs:
                y = float(np.clip(cfos_stabilized_after_long(x), p_br.yr[0], p_br.yr[1]))
                pts.append(p_br.pt(x, y))
            pts.append(p_br.pt(x1, 0))
            return Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=0.32)

        c_br = always_redraw(mk_br_curve)
        f_br = always_redraw(mk_br_fill)
        dot_br = always_redraw(lambda: Dot(
            p_br.pt(t_r.get_value(), cfos_stabilized_after_long(t_r.get_value())),
            radius=0.09, color=TEXT,
            stroke_color=ACTIVE if t_r.get_value() >= 4.6 else TEAL_DEC, stroke_width=3,
        ))

        rng = np.random.default_rng(7)
        frag_offsets = rng.uniform(-0.30, 0.30, size=(6, 2))

        def mk_frags():
            p = frag_t.get_value()
            if p <= 0.02:
                return VGroup()
            g = VGroup()
            base_pt = p_bl.pt(5.2, 0.36)
            for dx, dy in frag_offsets:
                pos = base_pt + np.array([dx * (1 + 0.7 * p), -0.32 * p + dy * 0.25, 0])
                g.add(Square(side_length=0.12, stroke_color=CORAL, stroke_width=2, fill_color=CORAL, fill_opacity=0.75 * (1.0 - 0.3 * p)).move_to(pos))
            return g

        frags = always_redraw(mk_frags)

        self.add(head, tag, top_l, top_r, bot_l, bot_r, lbl_l, lbl_r, lbl_bl, lbl_br, p_tl, p_tr, p_bl, p_br)
        self.add(f_tl, c_tl, dot_tl, f_bl, c_bl, dot_bl, frags, f_tr, c_tr, dot_tr, f_br, c_br, dot_br)

        # Start brief ERK rising immediately during intro ("In fibroblasts...")
        self.play(t_l.animate.set_value(1.3), run_time=1.8, rate_func=linear)

        self.at("switches on a gene")
        self.play(Create(slow_path), GrowArrow(slow_tip), FadeIn(slow_lbl), t_l.animate.set_value(3.2), run_time=2.8, rate_func=linear)

        self.at("takes time")
        self.play(t_l.animate.set_value(5.0), run_time=2.0, rate_func=linear)

        self.at("breaks down quickly")
        lbl_brk = T("c-Fos breaks down", 24, CORAL, weight=BOLD).move_to([-2.15, -1.02, 0])
        self.play(t_l.animate.set_value(10.0), frag_t.animate.set_value(1.0), FadeIn(lbl_brk), run_time=3.2, rate_func=linear)

        self.at("works as a timer")
        gap_bar = Line(p_bl.pt(1.2, 0.05), p_bl.pt(3.5, 0.05), color=CORAL, stroke_width=5)
        gap_lbl = T("ERK off early", 22, CORAL).move_to([-4.35, -1.78, 0])
        self.play(Create(gap_bar), FadeIn(gap_lbl), run_time=1.6)

        self.at("erk stays on")
        self.play(t_r.animate.set_value(4.5), run_time=2.0, rate_func=linear)

        self.at("c fos appears")
        p_badge1 = chip("P", ACTIVE, size=24, pad=0.14).move_to(p_br.pt(5.8, 0.72) + UP * 0.52)
        p_badge2 = chip("P", ACTIVE, size=24, pad=0.10).move_to(p_br.pt(7.9, 0.96) + UP * 0.30)
        lbl_stab = T("stabilized c-Fos", 24, ACTIVE, weight=BOLD).move_to([2.01, -1.00, 0])
        self.play(
            GrowArrow(fast_arr), FadeIn(fast_lbl),
            FadeIn(p_badge1), FadeIn(p_badge2), FadeIn(lbl_stab),
            t_r.animate.set_value(6.8),
            run_time=0.8, rate_func=linear,
        )
        self.play(t_r.animate.set_value(10.0), run_time=1.4, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S05 Predict Q & S06 Pause
def _build_predict_backdrop():
    """Shared builder so S05PredictQ ends on the exact frame S06Pause holds."""
    head = T("Test this timer: always-stable mutant", 32, TEXT).move_to([-0.8, 3.22, 0])
    tag = top_right_tag("schematic")
    world = two_lane_frame(top_y=(0.35, 2.45), bot_y=(-2.15, -0.05), top_title="ERK (brief EGF)", bot_title="c-Fos (mutant)")

    p_top = Plot(box=(-4.9, 5.5, 0.52, 1.92), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.5)
    p_bot = Plot(box=(-4.9, 5.5, -1.96, -0.58), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.5)

    c_erk = p_top.curve(erk_brief, color=AMBER, width=5)
    f_erk = Polygon(
        *[p_top.pt(0, 0), *[p_top.pt(x, erk_brief(x)) for x in np.linspace(0, 10, 90)], p_top.pt(10, 0)],
        stroke_width=0, fill_color=AMBER, fill_opacity=0.22,
    )

    shield = boxed_label("Always stable mutant", TEAL_DEC, size=24, pad=0.16).move_to([-2.85, -1.10, 0])
    no_p = T("no P needed", 22, STRUCT).next_to(shield, DOWN, buff=0.14)

    pts_up = [p_bot.pt(x, cfos_mutant_after_brief(x)) for x in np.linspace(3.5, 9.6, 70)]
    pts_dn = [p_bot.pt(x, cfos_unstable_after_brief(x)) for x in np.linspace(3.5, 9.6, 70)]
    c_up = DashedVMobject(VMobject(stroke_color=ACTIVE, stroke_width=5).set_points_as_corners(pts_up), num_dashes=16)
    c_dn = DashedVMobject(VMobject(stroke_color=CORAL, stroke_width=5).set_points_as_corners(pts_dn), num_dashes=16)
    lbl_up = T("build up?", 26, ACTIVE, weight=BOLD).move_to([4.5, -0.46, 0])
    lbl_dn = T("vanish?", 26, CORAL, weight=BOLD).move_to([4.5, -1.48, 0])

    g = VGroup(head, tag, world, p_top, p_bot, f_erk, c_erk, shield, no_p, c_up, c_dn, lbl_up, lbl_dn)
    return g, p_top, p_bot, c_erk, f_erk, shield, no_p, c_up, c_dn, lbl_up, lbl_dn


class S05PredictQ(SpokenScene):
    QUESTION = "Brief ERK + always-stable c-Fos: build up, or vanish?"

    def construct(self):
        head = T("Test this timer: always-stable mutant", 32, TEXT).move_to([-0.8, 3.22, 0])
        tag = top_right_tag("schematic")
        world = two_lane_frame(top_y=(0.35, 2.45), bot_y=(-2.15, -0.05), top_title="ERK (brief EGF)", bot_title="c-Fos (mutant)")

        p_top = Plot(box=(-4.9, 5.5, 0.52, 1.92), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.5)
        p_bot = Plot(box=(-4.9, 5.5, -1.96, -0.58), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.5)

        t_erk = ValueTracker(0.01)
        c_erk = p_top.live_curve(erk_brief, t_erk, color=AMBER, width=5)
        f_erk = area_under(p_top, erk_brief, t_erk, AMBER, opacity=0.22)

        self.add(head, tag, world, p_top, p_bot, f_erk, c_erk)
        self.play(t_erk.animate.set_value(10.0), run_time=2.6, rate_func=linear)

        self.at("suppose a mutation")
        shield = boxed_label("Always stable mutant", TEAL_DEC, size=24, pad=0.16).move_to([-2.85, -1.10, 0])
        self.play(Create(shield.box), Write(shield.label), run_time=2.2)

        self.at("no phosphates needed")
        no_p = T("no P needed", 22, STRUCT).next_to(shield, DOWN, buff=0.14)
        self.play(FadeIn(no_p), run_time=1.8)

        self.at("brief egf pulse")
        t_cand = ValueTracker(3.51)

        def mk_dashed(fn, col):
            def inner():
                u = t_cand.get_value()
                if u <= 3.6:
                    return VMobject(stroke_width=0)
                pts = [p_bot.pt(x, fn(x)) for x in np.linspace(3.5, u, max(4, int(60 * (u - 3.5) / 6.1) + 2))]
                return DashedVMobject(VMobject(stroke_color=col, stroke_width=5).set_points_as_corners(pts), num_dashes=max(2, int(16 * (u - 3.5) / 6.1)))
            return always_redraw(inner)

        d_up = mk_dashed(cfos_mutant_after_brief, ACTIVE)
        d_dn = mk_dashed(cfos_unstable_after_brief, CORAL)
        self.add(d_up, d_dn)
        self.play(t_cand.animate.set_value(9.6), run_time=2.2, rate_func=linear)

        self.at("build up")
        lbl_up = T("build up?", 26, ACTIVE, weight=BOLD).move_to([4.5, -0.46, 0])
        lbl_dn = T("vanish?", 26, CORAL, weight=BOLD).move_to([4.5, -1.48, 0])
        q = question_card(self.QUESTION, y=-2.95, color=GOLD, size=30, max_w=10.6)
        self.play(FadeIn(lbl_up), FadeIn(lbl_dn), FadeIn(q), run_time=1.6)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Brief ERK + always-stable c-Fos: build up, or vanish?"
    CARD = {"y": -2.95, "color": GOLD, "size": 30, "max_w": 10.6}
    RING_AT = (5.9, -2.95, 0)
    SECONDS = 4.5

    def backdrop(self):
        g, *_ = _build_predict_backdrop()
        return g


# ------------------------------------------------------------------ S07 Predict Reveal
class S07PredictReveal(SpokenScene):
    def construct(self):
        g, p_top, p_bot, c_erk, f_erk, shield, no_p, c_up, c_dn, lbl_up, lbl_dn = _build_predict_backdrop()
        world = g[2]
        q = question_card(S06Pause.QUESTION, y=-2.95, color=GOLD, size=30, max_w=10.6)
        self.add(g, q)

        t_res = ValueTracker(3.51)
        solid_up = p_bot.live_curve(cfos_mutant_after_brief, t_res, color=ACTIVE, width=6, x0=3.5)
        fill_up = area_under(p_bot, cfos_mutant_after_brief, t_res, ACTIVE, x0=3.5, opacity=0.25)
        ans_lbl = T("c-Fos builds up!", 28, ACTIVE, weight=BOLD).move_to([4.15, -0.44, 0])

        self.play(FadeOut(q), FadeOut(c_dn), FadeOut(lbl_dn), FadeOut(c_up), FadeOut(lbl_up), run_time=0.55)
        self.add(fill_up, solid_up)

        self.at("without fast breakdown")
        self.play(t_res.animate.set_value(7.2), FadeIn(ans_lbl), run_time=3.1, rate_func=linear)

        self.at("erk shuts off")
        shut_dash = DashedLine(p_top.pt(2.8, 0), p_top.pt(2.8, 0.96), color=CORAL, stroke_width=3.0, dash_length=0.12)
        shut_lbl = T("ERK off", 24, CORAL, weight=BOLD).move_to([-1.2, 1.55, 0])
        self.play(FadeIn(shut_dash), FadeIn(shut_lbl), t_res.animate.set_value(9.6), run_time=1.4, rate_func=linear)

        self.at("brief and long")
        broken = chip("Clock broken: brief looks like long", CORAL, size=28).move_to([0.0, -2.95, 0])
        self.play(FadeIn(broken), run_time=1.2)

        self.at("lost its clock")
        self.wait(1.4)
        self.play(FadeOut(broken), FadeOut(shut_dash), FadeOut(shut_lbl), run_time=0.6)

        self.at("repeating spikes")
        spk_times = [1.0, 2.3, 3.6, 4.9, 6.2, 7.5, 8.8]
        t_spk = ValueTracker(0.01)
        spk_curve = p_top.live_curve(lambda t: spike_train_y(t, spk_times, width=0.12), t_spk, color=AMBER, width=5)
        new_head = T("Carrying the idea to repeating spikes", 32, TEXT).move_to([-0.8, 3.22, 0])
        lbl_ca = T("Ca2+ spikes", 24, AMBER, weight=BOLD).move_to(world.top_lab, aligned_edge=LEFT)
        lbl_dec = T("Decoder", 24, TEAL_DEC, weight=BOLD).move_to(world.bot_lab, aligned_edge=LEFT)
        self.play(
            FadeOut(c_erk), FadeOut(f_erk),
            FadeOut(shield), FadeOut(no_p),
            FadeOut(fill_up), FadeOut(solid_up), FadeOut(ans_lbl),
            swap(g[0], new_head, run_time=0.5),
            swap(world.top_lab, lbl_ca, run_time=0.5),
            swap(world.bot_lab, lbl_dec, run_time=0.5),
            run_time=0.55,
        )
        self.add(spk_curve)
        self.play(t_spk.animate.set_value(9.6), run_time=1.6, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S08 Frequency Bucket
class S08FrequencyBucket(SpokenScene):
    def construct(self):
        head = T("How often? Counting spikes with a leaky decoder", 32, TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        bk_x, bk_y0, bk_w, bk_h = -4.85, -1.25, 1.55, 2.35
        bk_walls = VMobject(stroke_color=TEAL_DEC, stroke_width=4.0)
        bk_walls.set_points_as_corners([
            [bk_x - bk_w / 2, bk_y0 + bk_h, 0],
            [bk_x - bk_w / 2, bk_y0, 0],
            [bk_x - 0.14, bk_y0, 0],
        ])
        bk_walls2 = VMobject(stroke_color=TEAL_DEC, stroke_width=4.0)
        bk_walls2.set_points_as_corners([
            [bk_x + 0.14, bk_y0, 0],
            [bk_x + bk_w / 2, bk_y0, 0],
            [bk_x + bk_w / 2, bk_y0 + bk_h, 0],
        ])
        bk_lbl = T("Leaky bucket", 26, TEAL_DEC, weight=BOLD).move_to([bk_x, 1.52, 0])
        leak_lbl = T("leaks out", 24, CORAL).move_to([bk_x, -2.25, 0])

        world = two_lane_frame(top_y=(0.35, 2.50), bot_y=(-2.35, -0.10), x_range=(-3.2, 6.0),
                               top_title="Ca2+ spikes", bot_title="Decoder activity")
        p_top = Plot(box=(-2.7, 5.6, 0.55, 1.95), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.5)
        p_bot = Plot(box=(-2.7, 5.6, -2.12, -0.58), xr=(0, 10), yr=(0, 3.2), color=STRUCT, stroke=2.5)

        slow_spks = [1.2, 5.2, 9.2]
        fast_spks = [0.8, 2.0, 3.2, 4.4, 5.6, 6.8, 8.0, 9.2]

        mode = ValueTracker(0.0)
        t_sim = ValueTracker(0.01)

        def current_params():
            m = int(round(mode.get_value()))
            if m in (0, 2):
                return slow_spks, 1.5, TEAL_DEC
            if m == 1:
                return fast_spks, 1.5, TEAL_DEC
            return fast_spks, 1.5, ACTIVE

        def mk_top_spikes():
            spks, _, _ = current_params()
            u = t_sim.get_value()
            m = VMobject(stroke_color=AMBER, stroke_width=5, fill_opacity=0)
            if u > 0.05:
                xs = np.linspace(0, u, max(6, int(160 * u / 10.0) + 2))
                pts = [p_top.pt(x, spike_train_y(x, spks, width=0.11)) for x in xs]
                if len(pts) >= 2:
                    m.set_points_as_corners(pts)
            return m

        def mk_bot_curve():
            spks, tau, col = current_params()
            u = t_sim.get_value()
            m = VMobject(stroke_color=col, stroke_width=5, fill_opacity=0)
            if u > 0.05:
                xs = np.linspace(0, u, max(6, int(160 * u / 10.0) + 2))
                pts = [p_bot.pt(x, min(3.15, exp_train(x, spks, tau))) for x in xs]
                if len(pts) >= 2:
                    m.set_points_as_corners(pts)
            return m

        def mk_bot_fill():
            spks, tau, col = current_params()
            u = t_sim.get_value()
            if u <= 0.05:
                return VMobject(stroke_width=0, fill_opacity=0)
            xs = np.linspace(0, u, max(6, int(100 * u / 10.0) + 2))
            pts = [p_bot.pt(0, 0)] + [p_bot.pt(x, min(3.15, exp_train(x, spks, tau))) for x in xs] + [p_bot.pt(u, 0)]
            return Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=0.22)

        def mk_bucket_water():
            spks, tau, col = current_params()
            u = t_sim.get_value()
            lvl = exp_train(u, spks, tau)
            frac = float(np.clip(lvl / 3.0, 0.0, 0.96))
            if frac <= 0.01:
                return VGroup()
            wh = frac * (bk_h - 0.08)
            return Rectangle(
                width=bk_w - 0.10, height=wh,
                stroke_width=0, fill_color=col, fill_opacity=0.55,
            ).move_to([bk_x, bk_y0 + 0.04 + wh / 2.0, 0])

        def mk_drips():
            spks, tau, _ = current_params()
            u = t_sim.get_value()
            lvl = exp_train(u, spks, tau)
            if lvl <= 0.06:
                return VGroup()
            g = VGroup()
            for k in range(2):
                phase = (u * 1.4 + k * 0.5) % 1.0
                dy = bk_y0 - 0.08 - 0.65 * phase
                g.add(Dot([bk_x, dy, 0], radius=0.065, color=CORAL).set_opacity(1.0 - 0.5 * phase))
            return g

        top_spk_mob = always_redraw(mk_top_spikes)
        bot_fill_mob = always_redraw(mk_bot_fill)
        bot_cur_mob = always_redraw(mk_bot_curve)
        water_mob = always_redraw(mk_bucket_water)
        drips_mob = always_redraw(mk_drips)

        case_lbl = T("brief spikes, slow rate", 24, AMBER).move_to([2.8, 2.24, 0])

        self.add(head, tag, world, p_top, p_bot)
        self.add(top_spk_mob, bot_fill_mob, bot_cur_mob)
        self.play(FadeIn(case_lbl), t_sim.animate.set_value(9.8), run_time=3.2, rate_func=linear)

        self.at("stronger cues send")
        case_fast = T("stronger cue: faster spikes", 24, AMBER).move_to([2.8, 2.24, 0])
        mode.set_value(1.0)
        t_sim.set_value(0.01)
        self.play(swap(case_lbl, case_fast, run_time=0.45), run_time=0.45)
        self.play(t_sim.animate.set_value(5.0), run_time=3.2, rate_func=linear)

        self.at("turns on fast")
        dec_note = T("fast on, slow decay", 24, TEAL_DEC).move_to([3.3, -0.34, 0])
        self.play(FadeIn(dec_note), t_sim.animate.set_value(9.8), run_time=3.2, rate_func=linear)

        self.at("leaky bucket")
        bucket_grp = VGroup(bk_walls, bk_walls2, bk_lbl, leak_lbl)
        case_rare = T("rare cups: drain away", 24, TEAL_DEC).move_to([2.8, 2.24, 0])
        mode.set_value(2.0)
        t_sim.set_value(0.01)
        self.add(water_mob, drips_mob)
        self.play(swap(case_fast, case_rare, run_time=0.35), FadeOut(dec_note), FadeIn(bucket_grp), run_time=0.35)
        self.play(t_sim.animate.set_value(9.8), run_time=2.3, rate_func=linear)

        self.at("rapid cups stack")
        case_stack = T("rapid cups: stack higher!", 24, ACTIVE, weight=BOLD).move_to([2.8, 2.24, 0])
        mode.set_value(3.0)
        t_sim.set_value(0.01)
        self.play(swap(case_rare, case_stack, run_time=0.35), run_time=0.35)
        self.play(t_sim.animate.set_value(9.8), run_time=3.4, rate_func=linear)

        self.at("whatever activity remains")
        self.wait(1.0)
        self.finish()


# ------------------------------------------------------------------ S09 Frequency Math
class S09FrequencyMath(SpokenScene):
    def construct(self):
        formula = M("fraction left = (1/2)^(gap ÷ half-time)", 26, TEXT)
        ht_lbl = M("half-time = 30 s", 26, TEAL_DEC)
        top_row = VGroup(formula, ht_lbl).arrange(RIGHT, buff=0.65).move_to([0, 3.22, 0])

        top_l = RoundedRectangle(corner_radius=0.14, width=5.85, height=1.38, stroke_color=AMBER, stroke_width=2.0, fill_color=AMBER, fill_opacity=0.05).move_to([-3.10, 1.84, 0])
        top_r = RoundedRectangle(corner_radius=0.14, width=5.85, height=1.38, stroke_color=AMBER, stroke_width=2.0, fill_color=AMBER, fill_opacity=0.05).move_to([3.10, 1.84, 0])
        bot_l = RoundedRectangle(corner_radius=0.14, width=5.85, height=3.42, stroke_color=TEAL_DEC, stroke_width=2.0, fill_color=TEAL_DEC, fill_opacity=0.05).move_to([-3.10, -0.84, 0])
        bot_r = RoundedRectangle(corner_radius=0.14, width=5.85, height=3.42, stroke_color=TEAL_DEC, stroke_width=2.0, fill_color=TEAL_DEC, fill_opacity=0.05).move_to([3.10, -0.84, 0])

        lbl_l = T("Spikes 120 s apart", 26, AMBER, weight=BOLD).move_to([-5.75, 2.28, 0], aligned_edge=LEFT)
        lbl_r = T("Spikes 15 s apart", 26, AMBER, weight=BOLD).move_to([0.45, 2.28, 0], aligned_edge=LEFT)

        p_tl = Plot(box=(-5.40, -0.55, 1.28, 2.04), xr=(0, 240), yr=(0, 1.15), color=STRUCT, stroke=2.0)
        p_bl = Plot(
            box=(-5.40, -0.55, -1.62, 0.48), xr=(0, 240), yr=(0, 3.2),
            xticks=[0, 120, 240], yticks=[(0, "0"), (1, "1"), (2, "2"), (3, "3")],
            xlabel="", ylabel="", color=STRUCT, size=24, stroke=2.2,
        )
        p_tr = Plot(box=(0.80, 5.65, 1.28, 2.04), xr=(0, 60), yr=(0, 1.15), color=STRUCT, stroke=2.0)
        p_br = Plot(
            box=(0.80, 5.65, -1.62, 0.48), xr=(0, 60), yr=(0, 3.2),
            xticks=[0, 15, 30, 45, 60], yticks=[(0, "0"), (1, "1"), (2, "2"), (3, "3")],
            xlabel="", ylabel="", color=STRUCT, size=24, stroke=2.2,
        )
        xl_l = T("time (s)", 22, STRUCT).move_to([-3.0, -2.28, 0])
        xl_r = T("time (s)", 22, STRUCT).move_to([3.2, -2.28, 0])

        spks_120 = [0.0, 120.0, 240.0]
        spks_15 = [0.0, 15.0, 30.0, 45.0, 60.0]

        tL = ValueTracker(0.1)
        tR = ValueTracker(0.1)

        c_tl = p_tl.live_curve(lambda t: spike_train_y(t, spks_120, width=3.0), tL, color=AMBER, width=4.5)
        c_bl = p_bl.live_curve(lambda t: exp_train(t, spks_120, 30.0), tL, color=TEAL_DEC, width=5)
        f_bl = area_under(p_bl, lambda t: exp_train(t, spks_120, 30.0), tL, TEAL_DEC, opacity=0.22)
        dot_l = p_bl.dot(lambda: tL.get_value(), lambda: exp_train(tL.get_value(), spks_120, 30.0), color=TEXT, ring=TEAL_DEC, radius=0.10)

        c_tr = p_tr.live_curve(lambda t: spike_train_y(t, spks_15, width=0.8), tR, color=AMBER, width=4.5)
        c_br = p_br.live_curve(lambda t: exp_train(t, spks_15, 30.0), tR, color=ACTIVE, width=5)
        f_br = area_under(p_br, lambda t: exp_train(t, spks_15, 30.0), tR, ACTIVE, opacity=0.22)
        dot_r = p_br.dot(lambda: tR.get_value(), lambda: exp_train(tR.get_value(), spks_15, 30.0), color=TEXT, ring=ACTIVE, radius=0.10)

        # Start fully lit (no black start frame!) and immediately animate first spike decay
        self.add(top_l, top_r, bot_l, bot_r, p_tl, p_bl, p_tr, p_br, xl_l, xl_r, c_tl, f_bl, c_bl, dot_l)
        self.play(Write(formula), tL.animate.set_value(20.0), run_time=3.5, rate_func=linear)

        self.at("take a 30")
        self.play(FadeIn(ht_lbl), tL.animate.set_value(35.0), run_time=2.2, rate_func=linear)

        self.at("120 seconds apart")
        self.play(FadeIn(lbl_l), tL.animate.set_value(119.5), run_time=2.0, rate_func=linear)

        self.at("120 divided by 30")
        eq_l1 = M("120 ÷ 30 = 4", 24, TEXT).move_to([-2.7, 0.15, 0])
        ht_marks = VGroup(*[
            DashedLine(p_bl.pt(m, 0), p_bl.pt(m, 2.0 ** (-m / 30.0)), color=STRUCT, stroke_width=2.0, dash_length=0.08)
            for m in (30, 60, 90, 120)
        ])
        self.play(FadeIn(eq_l1), tL.animate.set_value(120.0), Create(ht_marks), run_time=3.2, rate_func=linear)

        self.at("leaves 1 sixteenth")
        eq_l2 = M("(1/2)^4 = 1/16 ≈ 6%", 24, TEAL_DEC).move_to([-2.7, -0.35, 0])
        self.play(FadeIn(eq_l2), tL.animate.set_value(145.0), run_time=1.4, rate_func=linear)

        self.at("about 6 percent")
        self.play(tL.animate.set_value(240.0), run_time=2.0, rate_func=linear)

        self.at("15 seconds apart")
        self.add(c_tr, f_br, c_br, dot_r)
        self.play(FadeIn(lbl_r), tR.animate.set_value(14.9), run_time=1.4, rate_func=linear)

        self.at("15 divided by 30")
        eq_r1 = M("15 ÷ 30 = 0.5", 24, TEXT).move_to([2.55, 0.34, 0])
        self.play(FadeIn(eq_r1), tR.animate.set_value(28.0), run_time=2.6, rate_func=linear)

        self.at("power of 1 half")
        eq_r2 = M("(1/2)^0.5 ≈ 71%", 24, ACTIVE).move_to([2.55, -0.02, 0])
        self.play(FadeIn(eq_r2), run_time=0.9)

        self.at("about 71 percent")
        self.play(tR.animate.set_value(60.0), run_time=2.0, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S10 Wrap
class S10Wrap(SpokenScene):
    def construct(self):
        head = T("Duration and frequency follow one rule", 34, TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        top_l = RoundedRectangle(corner_radius=0.14, width=4.8, height=1.55, stroke_color=AMBER, stroke_width=2.0, fill_color=AMBER, fill_opacity=0.05).move_to([-3.65, 1.72, 0])
        bot_l = RoundedRectangle(corner_radius=0.14, width=4.8, height=2.25, stroke_color=TEAL_DEC, stroke_width=2.0, fill_color=TEAL_DEC, fill_opacity=0.05).move_to([-3.65, -0.95, 0])
        lbl_dl = T("Duration: ERK", 26, AMBER, weight=BOLD).move_to([-5.80, 2.25, 0], aligned_edge=LEFT)
        lbl_cl = T("c-Fos output", 24, ACTIVE, weight=BOLD).move_to([-5.80, -0.08, 0], aligned_edge=LEFT)

        p_tl = Plot(box=(-5.7, -1.6, 1.12, 2.02), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.0)
        p_bl = Plot(box=(-5.7, -1.6, -1.92, -0.32), xr=(0, 10), yr=(0, 1.15), color=STRUCT, stroke=2.0)

        top_r = RoundedRectangle(corner_radius=0.14, width=4.8, height=1.55, stroke_color=AMBER, stroke_width=2.0, fill_color=AMBER, fill_opacity=0.05).move_to([3.65, 1.72, 0])
        bot_r = RoundedRectangle(corner_radius=0.14, width=4.8, height=2.25, stroke_color=TEAL_DEC, stroke_width=2.0, fill_color=TEAL_DEC, fill_opacity=0.05).move_to([3.65, -0.95, 0])
        lbl_dr = T("Frequency: Ca2+", 26, AMBER, weight=BOLD).move_to([1.50, 2.25, 0], aligned_edge=LEFT)
        lbl_cr = T("Decoder staircase", 24, ACTIVE, weight=BOLD).move_to([1.50, -0.08, 0], aligned_edge=LEFT)

        p_tr = Plot(box=(1.6, 5.7, 1.12, 2.02), xr=(0, 120), yr=(0, 1.15), color=STRUCT, stroke=2.0)
        p_br = Plot(box=(1.6, 5.7, -1.92, -0.32), xr=(0, 120), yr=(0, 3.5), color=STRUCT, stroke=2.0)

        t_u = ValueTracker(0.05)
        lambda_t = ValueTracker(0.05)

        c_tl_b = p_tl.live_curve(erk_brief, lambda_t, color=AMBER, width=4)
        c_tl_l = p_tl.live_curve(erk_long, lambda_t, color=GOLD, width=5)
        c_bl_b = p_bl.live_curve(cfos_unstable_after_brief, lambda_t, color=TEAL_DEC, width=4)
        c_bl_l = p_bl.live_curve(cfos_stabilized_after_long, lambda_t, color=ACTIVE, width=5)
        f_bl_l = area_under(p_bl, cfos_stabilized_after_long, lambda_t, ACTIVE, opacity=0.22)

        spks_s = [0.0, 120.0]
        spks_f = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0, 105.0, 120.0]

        def mk_tr_spikes(spks, spike_w, col, stroke_w, opacity):
            def inner():
                x1 = t_u.get_value()
                m = VMobject(stroke_color=col, stroke_width=stroke_w, stroke_opacity=opacity, fill_opacity=0)
                if x1 > 1e-3:
                    n = max(4, int(480 * x1 / 120.0) + 2)
                    pts = p_tr._pts(lambda t: spike_train_y(t, spks, width=spike_w), 0.0, x1, n)
                    if len(pts) >= 2:
                        m.set_points_as_corners(pts)
                return m
            return always_redraw(inner)

        c_tr_s = mk_tr_spikes(spks_s, 2.0, AMBER, 6.0, 0.45)
        c_tr_f = mk_tr_spikes(spks_f, 1.2, GOLD, 3.5, 1.0)
        c_br_s = p_br.live_curve(lambda t: exp_train(t, spks_s, 30.0), t_u, color=TEAL_DEC, width=4)
        c_br_f = p_br.live_curve(lambda t: exp_train(t, spks_f, 30.0), t_u, color=ACTIVE, width=5)
        f_br_f = area_under(p_br, lambda t: exp_train(t, spks_f, 30.0), t_u, ACTIVE, opacity=0.22)

        clk_ang = ValueTracker(0.0)
        clk = clock_icon([0.0, 0.35, 0], radius=0.52, color=TEAL_DEC, angle_tracker=clk_ang)
        clk_lbl = T("decoder\ntiming", 24, TEAL_DEC).move_to([0.0, -0.58, 0])
        arr_l = Arrow([-0.62, -0.95, 0], [-1.18, -0.95, 0], buff=0, color=TEAL_DEC, stroke_width=3.5)
        arr_r = Arrow([0.62, -0.95, 0], [1.18, -0.95, 0], buff=0, color=TEAL_DEC, stroke_width=3.5)

        cap = caption("Compare a signal against a decoder's delay or decay.", size=28, color=TEXT, y=-2.95)

        self.add(head, tag, top_l, bot_l, top_r, bot_r, lbl_dl, lbl_cl, lbl_dr, lbl_cr, p_tl, p_bl, p_tr, p_br)
        self.add(c_tl_b, c_tl_l, c_bl_b, f_bl_l, c_bl_l, c_tr_s, c_tr_f, c_br_s, f_br_f, c_br_f)
        self.play(lambda_t.animate.set_value(4.5), t_u.animate.set_value(50.0), run_time=2.5, rate_func=linear)

        self.at("compare a signal")
        self.play(FadeIn(clk), FadeIn(clk_lbl), GrowArrow(arr_l), GrowArrow(arr_r), FadeIn(cap), run_time=1.0)

        self.at("carries many orders")
        self.play(
            lambda_t.animate.set_value(10.0),
            t_u.animate.set_value(120.0),
            clk_ang.animate.set_value(TAU * 0.75),
            run_time=3.4,
            rate_func=linear,
        )

        self.at("real proteins")
        self.play(clk_ang.animate.set_value(TAU * 1.40), run_time=4.0, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S11 End
class S11End(EndCard):
    LINE = "Cells read duration and frequency against the timing of a decoder."
