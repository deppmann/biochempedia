"""
STEMhop — Cardiac Output and Venous Return, Chapter 2: "Which Vessels Relaxed?"

COLOUR MAP (one colour per concept, carried from Chapter 1):
- BLUE   : the heart's line (cardiac function curve, Q = b + Pra) and "lift" / "opposite ways"
- GREEN  : the veins' line (venous return curve, Q = (Pms - Pra)/Rvr), filling pressure, and "tilt" / "same way"
- YELLOW : the operating point (the crossing) and its dashed drop-lines to both axes
- RED    : the vein-collapse band (Pra from -4 to -2 mmHg)
- GREY   : axes, ticks, ghosts of previous curve/dot positions, and model/clarity scope tags
- TEXT   : questions, prompts, buttons, and primary readouts

ONE PICTURE OF THE WORLD (carried across all scenes):
The flow-versus-pressure plot (Pra -4..10 mmHg, Q 0..10 L/min) filling ~72% of the frame height on
the left, with the rule rows, case buttons, and live readouts on the right. Flow dots drift
continuously along the veins' line toward the crossing and up the heart's line away from it.

WHAT CHANGES PER SPOKEN SCENE (all curves and crossings computed from the lesson's linear model):
- s00_link_and_question : crossing pulses at (2, 5); "resistance falls" drops in; Pra dot nudges right/left under "Pra: up or down?"
- s02_one_line          : BLUE heart line lifts (b: 3 -> 4) with GREY ghost; YELLOW dot slides along unmoved GREEN line to (1.5, 5.5) and returns
- s03_slopes            : dot slides along heart's line (x/y axis arrows both point up/right) then along veins' line (axis arrows point opposite ways)
- s04_rule              : rule rows build on the right while GREEN then BLUE lines shift/pulse to demonstrate same-way vs opposite-way slides
- s05_which_resistance  : "resistance falls" splits into TPR = (92-2)/5 = 18 and Rvr = 1 (GREEN), then swaps to "veins" and "arterioles" buttons
- s06_veins             : "veins" lights; GREEN line shifts left (Pms: 7 -> 5) with ghost; dot slides down BLUE line to (1, 4) with down/left axis arrows, then resets
- s07_predict           : GREEN pivot ring at (7, 0); GREEN line tilts steeper (Rvr: 1 -> 0.5) to (2, 10)-(7, 0); dot flashes at (2, 5) under question
- s09_answer            : dot and drop-lines slide up BLUE line from (2, 5) to (3.67, 6.67) while Pra/Q Readout updates 2.0->3.7 and 5.0->6.7
- s10_arterioles        : "arterioles" lights; tilted GREEN line pulses, then BLUE line lifts (b: 3 -> 4) with GREY ghost and "tilt"/"lift" tags
- s11_both_lines        : dot moves to (3.33, 7.33) with Readout updating 3.7->3.3 and 6.7->7.3; opposite x-axis arrows compare longer GREEN tilt vs shorter BLUE lift
- s12_close             : "Pra: up or down?" returns briefly; lifted BLUE line pulses, then tilted GREEN line glows under the settled dot at (3.33, 7.33)
"""
from bp_parts import *

# Plot box: height 4.4 (+ axis labels ~1.4 => ~5.8 units = 72.5% of frame height), centred slightly left
PLOT_BOX = (-5.3, 1.4, -1.95, 2.45)
PLOT_XR = (-4, 10)
PLOT_YR = (0, 10)
X_TICKS = [-4, -2, 0, 2, 4, 6, 8, 10]
Y_TICKS = [0, 2, 4, 6, 8, 10]

Q_HEART_B = 3.0
PMS_BASE = 7.0
RVR_BASE = 1.0


def q_heart(pra, b=Q_HEART_B):
    return b + pra


def q_veins(pra, pms=PMS_BASE, rvr=RVR_BASE):
    return (pms - max(pra, -2.0)) / rvr


def operating_point(b=Q_HEART_B, pms=PMS_BASE, rvr=RVR_BASE):
    """Exact intersection of Q = b + Pra and Q = (Pms - Pra) / Rvr."""
    pra = (pms - rvr * b) / (1.0 + rvr)
    return pra, b + pra


def build_base_plot():
    """Build the carried-over axes, collapse band, and scope tag."""
    P = Plot(
        box=PLOT_BOX,
        xr=PLOT_XR,
        yr=PLOT_YR,
        xticks=X_TICKS,
        yticks=Y_TICKS,
        xlabel="right atrial pressure (mmHg)",
        ylabel="flow (L/min)",
        color=GREY,
        size=24,
        label_size=26,
        stroke=3,
    )
    bl = P.pt(-4, 0)
    tr = P.pt(-2, 10)
    collapse = Rectangle(
        width=tr[0] - bl[0],
        height=tr[1] - bl[1],
        stroke_width=0,
        fill_color=RED,
        fill_opacity=0.14,
    ).move_to([(bl[0] + tr[0]) / 2, (bl[1] + tr[1]) / 2, 0])
    collapse_edge = DashedLine(
        P.pt(-2, 0), P.pt(-2, 10), color=RED, stroke_width=2, stroke_opacity=0.45, dash_length=0.14
    )
    tag = scope_tag("illustrative model", size=24, color=GREY)
    return P, VGroup(collapse, collapse_edge), tag


def make_heart_curve(P, b_val, color=BLUE, width=6, dashed=False, opacity=1.0):
    x1 = min(7.0, 10.0 - b_val)
    if not dashed:
        return P.curve(lambda x: q_heart(x, b_val), x0=0.0, x1=x1, color=color, width=width, opacity=opacity)
    return DashedLine(
        P.pt(0.0, q_heart(0.0, b_val)),
        P.pt(x1, q_heart(x1, b_val)),
        color=color,
        stroke_width=max(2, width - 2),
        stroke_opacity=opacity,
        dash_length=0.16,
    )


def make_veins_curve(P, pms=PMS_BASE, rvr=RVR_BASE, color=GREEN, width=6, dashed=False, opacity=1.0):
    x_top = max(-4.0, pms - 10.0 * rvr)
    x_zero = min(10.0, pms)
    if x_top < -2.0:
        pts = [P.pt(-4.0, q_veins(-4.0, pms, rvr)), P.pt(-2.0, q_veins(-2.0, pms, rvr)), P.pt(x_zero, 0.0)]
    else:
        pts = [P.pt(x_top, q_veins(x_top, pms, rvr)), P.pt(x_zero, 0.0)]
    if not dashed:
        m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m
    segs = VGroup()
    for a, b in zip(pts[:-1], pts[1:]):
        segs.add(DashedLine(a, b, color=color, stroke_width=max(2, width - 2), stroke_opacity=opacity, dash_length=0.16))
    return segs


def make_curve_labels(P):
    """Compact concept labels placed cleanly clear of all curves and axes."""
    heart_lab = T("heart", size=26, color=BLUE).move_to(P.pt(8.3, 9.3))
    veins_lab = T("veins", size=26, color=GREEN).move_to(P.pt(9.1, 1.1))
    return heart_lab, veins_lab


def make_drop_lines(P, pra_fn, q_fn, color=YELLOW):
    def mk():
        x, y = pra_fn(), q_fn()
        p = P.pt(x, y)
        return VGroup(
            DashedLine(p, P.pt(x, 0.0), color=color, stroke_width=2.5, dash_length=0.12),
            DashedLine(p, P.pt(-4.0, y), color=color, stroke_width=2.5, dash_length=0.12),
        )
    return always_redraw(mk)


def make_flow_dots(P, b_fn, pms_fn, rvr_fn, opacity_scale=1.0):
    """Drifting beads along both curves: GREEN down veins toward crossing, BLUE up heart away from crossing."""
    n_v, n_h = 8, 7
    dots = VGroup()
    for i in range(n_v):
        d = Dot(radius=0.085, color="#C8F7B0")
        d._kind, d._phase = "v", i / n_v
        dots.add(d)
    for i in range(n_h):
        d = Dot(radius=0.085, color="#B5ECFA")
        d._kind, d._phase = "h", i / n_h
        dots.add(d)

    def update_dots(mob, dt):
        b, pms, rvr = b_fn(), pms_fn(), rvr_fn()
        pra_c, _ = operating_point(b, pms, rvr)
        v_left = max(-4.0, pms - 10.0 * rvr)
        h_right = min(7.0, 10.0 - b)
        for d in mob:
            d._phase = (d._phase + 0.24 * dt) % 1.0
            s = d._phase
            fade = min(1.0, s / 0.10, (1.0 - s) / 0.10)
            if d._kind == "v":
                x = v_left + s * max(0.1, pra_c - v_left)
                y = q_veins(x, pms, rvr)
            else:
                x = pra_c + s * max(0.1, h_right - pra_c)
                y = q_heart(x, b)
            d.move_to(P.pt(x, y))
            d.set_opacity(0.88 * opacity_scale * fade)

    dots.add_updater(update_dots)
    update_dots(dots, 0.0)
    return dots


def build_rule_rows(dimmed=True):
    """Two-row rule summary at the right edge (from s04 onward)."""
    rows = []
    specs = [
        (GREEN, True, "veins move: same way", 1.15),
        (BLUE, False, "heart moves: opposite ways", 0.35),
    ]
    for col, down, txt, y in specs:
        icon = Line(
            [-0.22, 0.14 if down else -0.14, 0],
            [0.22, -0.14 if down else 0.14, 0],
            color=col,
            stroke_width=5,
        )
        lab = fit_text(txt, max_w=3.85, size=24, color=col, max_lines=1)
        row = VGroup(icon, lab).arrange(RIGHT, buff=0.18)
        row.move_to([1.85 + row.width / 2, y, 0])
        if dimmed:
            row.set_opacity(0.65)
        rows.append(row)
    return VGroup(*rows)


def build_vessel_buttons(lit=None):
    """Separate 'veins' and 'arterioles' buttons in the upper-right panel."""
    v_col = GREEN if lit == "veins" else TEXT
    a_col = BLUE if lit == "arterioles" else TEXT
    v_btn = boxed_label("veins", color=v_col, size=26, box=(1.8, 0.65), fill_opacity=0.35 if lit == "veins" else 0.12)
    a_btn = boxed_label("arterioles", color=a_col, size=26, box=(2.2, 0.65), fill_opacity=0.35 if lit == "arterioles" else 0.12)
    g = VGroup(v_btn, a_btn).arrange(RIGHT, buff=0.25).move_to([3.95, 2.25, 0])
    return g, v_btn, a_btn


def build_readout(pra_fn, q_fn):
    """Live readout panel for Pra and output Q in the lower-right panel."""
    return Readout(
        [
            ("Pra", pra_fn, "{:4.1f} mmHg", YELLOW),
            ("Q", q_fn, "{:4.1f} L/min", YELLOW),
        ],
        at=[3.95, -0.85, 0],
        size=25,
        widest=[10.0, 10.0],
    )


def make_axis_arrows(P, y_dir=UP, x_dir=RIGHT, y_col=BLUE, x_col=BLUE, x_pra=2.0):
    """Small arrows tucked cleanly inside the plot axes (clear of all ticks and curves)."""
    y_c = P.pt(-3.45, 5.5)
    y_arr = Arrow(y_c - y_dir * 0.65, y_c + y_dir * 0.65, color=y_col, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.32)
    x_c = P.pt(x_pra, 0.52)
    x_arr = Arrow(x_c - x_dir * 0.65, x_c + x_dir * 0.65, color=x_col, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.32)
    return VGroup(y_arr, x_arr)


# ------------------------------------------------------------------ Scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        pra_t = ValueTracker(2.0)
        q_t = ValueTracker(5.0)
        heart = make_heart_curve(P, Q_HEART_B)
        veins = make_veins_curve(P, PMS_BASE, RVR_BASE)
        h_lab, v_lab = make_curve_labels(P)
        drops = make_drop_lines(P, pra_t.get_value, q_t.get_value)
        dot = P.dot(pra_t.get_value, q_t.get_value, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: Q_HEART_B, lambda: PMS_BASE, lambda: RVR_BASE)

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot)

        self.at("rising line")
        self.play(heart.animate.set_stroke(width=10), rate_func=there_and_back, run_time=0.8)

        self.at("crosses")
        self.play(Indicate(dot, color=YELLOW, scale_factor=1.5), run_time=0.7)

        self.at("falling line")
        self.play(veins.animate.set_stroke(width=10), rate_func=there_and_back, run_time=0.8)

        self.at("resistance falls")
        res_tag = boxed_label("resistance falls ↓", color=TEXT, size=26, fill_opacity=0.14).move_to([-2.0, 3.28, 0])
        self.play(FadeIn(res_tag, shift=DOWN * 0.2), run_time=0.6)

        self.at("right atrial pressure")
        q_text = T("Pra: up or down?", size=38, color=TEXT).move_to([2.1, 3.28, 0])
        q_mark = always_redraw(lambda: T("?", size=30, color=TEXT).move_to(P.pt(pra_t.get_value() + 0.65, 0.55)))
        self.play(FadeIn(q_text, shift=UP * 0.1), FadeIn(q_mark), run_time=0.45)
        self.play(pra_t.animate.set_value(2.9), run_time=0.55)
        self.play(pra_t.animate.set_value(1.1), run_time=0.7)
        self.play(pra_t.animate.set_value(2.0), FadeOut(q_mark), FadeOut(res_tag), run_time=0.55)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        heart = make_heart_curve(P, Q_HEART_B)
        veins = make_veins_curve(P, PMS_BASE, RVR_BASE)
        h_lab, v_lab = make_curve_labels(P)
        drops = make_drop_lines(P, lambda: 2.0, lambda: 5.0)
        dot = P.dot(lambda: 2.0, lambda: 5.0, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: Q_HEART_B, lambda: PMS_BASE, lambda: RVR_BASE)
        for m in (heart, veins, drops, dot):
            m.layout_ok = "covered"  # plot curves sit behind the centered title card

        q_prev = T("Pra: up or down?", size=38, color=TEXT).move_to([2.1, 3.28, 0])

        brand = T(SITE_NAME, size=22, color=TEAL, weight=BOLD)
        brand.layout_ok = True
        lesson = T("CARDIAC OUTPUT AND VENOUS RETURN", size=24, color=TEXT)
        title = T("Which Vessels Relaxed?", size=52, font=TITLE_FONT, color=TEXT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        card = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.28).move_to(UP * 0.25)
        card_bg = RoundedRectangle(
            corner_radius=0.22,
            width=card.width + 0.9,
            height=card.height + 0.7,
            stroke_color=GOLD,
            stroke_width=1.5,
            stroke_opacity=0.35,
            fill_color=BG,
            fill_opacity=0.9,
        ).move_to(UP * 0.25)
        card_bg.layout_ok = True  # title card backdrop over the center of the plot

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot, q_prev)
        self.play(
            FadeOut(q_prev, run_time=0.35),
            FadeIn(card_bg, run_time=0.35),
            FadeIn(card, shift=UP * 0.1, run_time=0.4),
        )
        self.wait(0.95)
        self.play(FadeOut(card, run_time=0.35), FadeOut(card_bg, run_time=0.35))
        self.finish()


class S02OneLine(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        b_t = ValueTracker(Q_HEART_B)
        heart = always_redraw(lambda: make_heart_curve(P, b_t.get_value()))
        veins = make_veins_curve(P, PMS_BASE, RVR_BASE)
        h_lab, v_lab = make_curve_labels(P)

        pra_fn = lambda: operating_point(b_t.get_value(), PMS_BASE, RVR_BASE)[0]
        q_fn = lambda: operating_point(b_t.get_value(), PMS_BASE, RVR_BASE)[1]
        drops = make_drop_lines(P, pra_fn, q_fn)
        dot = P.dot(pra_fn, q_fn, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, b_t.get_value, lambda: PMS_BASE, lambda: RVR_BASE)

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot)

        self.at("only one line")
        ghost_h = make_heart_curve(P, Q_HEART_B, color=GREY, width=4, dashed=True, opacity=0.8)
        self.add(ghost_h)
        self.bring_to_front(heart, drops, dot)
        self.play(b_t.animate.set_value(4.0), run_time=1.6)

        self.at("line that stayed")
        self.play(veins.animate.set_stroke(width=10), run_time=0.7)

        self.at("slides along")
        self.play(b_t.animate.set_value(Q_HEART_B), veins.animate.set_stroke(width=6), run_time=1.8)
        self.play(FadeOut(ghost_h), run_time=0.5)
        self.finish()


class S03Slopes(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        pra_t = ValueTracker(2.0)
        mode = ["heart"]
        q_fn = lambda: q_heart(pra_t.get_value()) if mode[0] == "heart" else q_veins(pra_t.get_value())

        heart = make_heart_curve(P, Q_HEART_B)
        veins = make_veins_curve(P, PMS_BASE, RVR_BASE)
        h_lab, v_lab = make_curve_labels(P)
        drops = make_drop_lines(P, pra_t.get_value, q_fn)
        dot = P.dot(pra_t.get_value, q_fn, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: Q_HEART_B, lambda: PMS_BASE, lambda: RVR_BASE)

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot)

        self.at("slopes up")
        h_trace = Arrow(P.pt(0.6, 3.6), P.pt(6.0, 9.0), color=BLUE, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.08)
        self.play(GrowArrow(h_trace), run_time=0.9)

        self.at("slide along it", nth=0)
        arr_same = make_axis_arrows(P, y_dir=UP, x_dir=RIGHT, y_col=BLUE, x_col=BLUE)
        lab_same = T("same way", size=30, color=BLUE).move_to([3.7, 1.15, 0])
        self.play(FadeIn(arr_same), FadeIn(lab_same), run_time=0.5)
        self.play(pra_t.animate.set_value(3.5), run_time=1.1)
        self.play(pra_t.animate.set_value(2.0), run_time=1.1)

        self.at("slopes down")
        v_trace = Arrow(P.pt(-0.6, 7.6), P.pt(5.8, 1.2), color=GREEN, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.08)
        self.play(FadeOut(h_trace), FadeOut(arr_same), GrowArrow(v_trace), run_time=0.8)

        self.at("slide along it", nth=1)
        mode[0] = "veins"
        arr_opp = make_axis_arrows(P, y_dir=UP, x_dir=LEFT, y_col=GREEN, x_col=GREEN)
        lab_opp = T("opposite ways", size=30, color=GREEN).move_to([3.7, 0.35, 0])
        self.play(FadeIn(arr_opp), FadeIn(lab_opp), run_time=0.5)
        self.play(pra_t.animate.set_value(0.5), run_time=1.1)
        self.play(pra_t.animate.set_value(2.0), run_time=1.1)
        self.play(FadeOut(v_trace), FadeOut(arr_opp), FadeOut(lab_same), FadeOut(lab_opp), run_time=0.5)
        self.finish()


class S04Rule(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        b_t = ValueTracker(Q_HEART_B)
        pms_t = ValueTracker(PMS_BASE)
        heart = always_redraw(lambda: make_heart_curve(P, b_t.get_value()))
        veins = always_redraw(lambda: make_veins_curve(P, pms_t.get_value(), RVR_BASE))
        h_lab, v_lab = make_curve_labels(P)

        pra_fn = lambda: operating_point(b_t.get_value(), pms_t.get_value(), RVR_BASE)[0]
        q_fn = lambda: operating_point(b_t.get_value(), pms_t.get_value(), RVR_BASE)[1]
        drops = make_drop_lines(P, pra_fn, q_fn)
        dot = P.dot(pra_fn, q_fn, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, b_t.get_value, pms_t.get_value, lambda: RVR_BASE)
        rows = build_rule_rows(dimmed=False)

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot)

        self.at("line that shifted")
        ghost_v = make_veins_curve(P, PMS_BASE, RVR_BASE, color=GREY, width=4, dashed=True, opacity=0.8)
        self.add(ghost_v)
        self.bring_to_front(veins, heart, drops, dot)
        self.play(pms_t.animate.set_value(8.2), run_time=1.1)

        self.at("one left standing")
        glow_h = make_heart_curve(P, Q_HEART_B, color=BLUE, width=16, opacity=0.38)
        h_slide_arr = Arrow(
            P.pt(3.1, 6.1) + UL * 0.22,
            P.pt(5.5, 8.5) + UL * 0.22,
            color=BLUE,
            stroke_width=6,
            buff=0,
            max_tip_length_to_length_ratio=0.14,
        )
        self.add(glow_h)
        self.bring_to_front(heart, drops, dot)
        self.play(FadeIn(glow_h), GrowArrow(h_slide_arr), run_time=0.8)
        self.play(
            pms_t.animate.set_value(PMS_BASE),
            FadeOut(ghost_v),
            FadeOut(glow_h),
            FadeOut(h_slide_arr),
            run_time=0.9,
        )

        self.at("move the veins")
        self.play(FadeIn(rows[0][0]), pms_t.animate.set_value(8.2), run_time=1.0)
        self.play(FadeIn(rows[0][1], shift=RIGHT * 0.12), run_time=0.5)

        self.at("same way")
        self.play(pms_t.animate.set_value(PMS_BASE), run_time=1.0)

        self.at("move the heart's line")
        self.play(FadeIn(rows[1][0]), b_t.animate.set_value(4.0), run_time=1.0)
        self.play(FadeIn(rows[1][1], shift=RIGHT * 0.12), run_time=0.5)

        self.at("opposite ways")
        self.play(b_t.animate.set_value(Q_HEART_B), run_time=0.8)
        self.play(rows.animate.set_opacity(0.65), run_time=0.45)
        self.finish()


class S05WhichResistance(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        heart = make_heart_curve(P, Q_HEART_B)
        veins = make_veins_curve(P, PMS_BASE, RVR_BASE)
        h_lab, v_lab = make_curve_labels(P)
        drops = make_drop_lines(P, lambda: 2.0, lambda: 5.0)
        dot = P.dot(lambda: 2.0, lambda: 5.0, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: Q_HEART_B, lambda: PMS_BASE, lambda: RVR_BASE)
        rows = build_rule_rows(dimmed=True)

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot, rows)

        res_tag = boxed_label("resistance falls ↓", color=TEXT, size=26, fill_opacity=0.14).move_to([-2.0, 3.28, 0])
        self.play(FadeIn(res_tag, shift=DOWN * 0.2), run_time=0.7)

        self.at("resistance fell")
        self.play(Indicate(res_tag, color=YELLOW, scale_factor=1.08), run_time=0.7)

        self.at("which resistance")
        q_sub = T("which one?", size=28, color=YELLOW).next_to(res_tag, RIGHT, buff=0.45)
        self.play(FadeIn(q_sub), run_time=0.45)

        self.at("total peripheral resistance")
        tpr_val = (92 - 2) / 5
        tpr_sym = boxed_label("TPR = (MAP - Pra) / Q", color=TEXT, size=24, fill_opacity=0.14).move_to([-1.1, 3.36, 0])
        self.play(FadeOut(q_sub, run_time=0.25))
        self.play(ReplacementTransform(res_tag, tpr_sym), run_time=0.65)

        self.at("arterial pressure", nth=0)
        self.play(tpr_sym.box.animate.set_stroke(YELLOW, width=4), rate_func=there_and_back, run_time=1.0)

        self.at("illustrative")
        tpr_num = boxed_label("TPR = (92 - 2) / 5", color=TEXT, size=24, fill_opacity=0.14).move_to([-1.1, 3.36, 0])
        self.play(swap(tpr_sym, tpr_num, run_time=0.65))

        self.at("comes out at 18")
        tpr_done = boxed_label(f"TPR = {tpr_val:g}", color=TEXT, size=26, fill_opacity=0.14).move_to([-1.0, 3.36, 0])
        self.play(swap(tpr_num, tpr_done, run_time=0.6))

        self.at("resistance to venous return")
        rvr_tag = boxed_label("Rvr = 1", color=GREEN, size=26, fill_opacity=0.14).move_to([1.9, 3.36, 0])
        units = T("units: mmHg·min/L", size=22, color=TEXT).move_to([0.45, 2.68, 0])
        self.play(FadeIn(rvr_tag), FadeIn(units), veins.animate.set_stroke(width=10), run_time=0.7)
        self.play(veins.animate.set_stroke(width=6), run_time=0.5)

        self.at("so say which")
        btns, _, _ = build_vessel_buttons(lit=None)
        self.play(FadeOut(tpr_done), FadeOut(rvr_tag), FadeOut(units), run_time=0.4)
        self.play(FadeIn(btns), run_time=0.5)
        self.finish()


class S06Veins(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        pms_t = ValueTracker(PMS_BASE)
        heart = make_heart_curve(P, Q_HEART_B)
        veins = always_redraw(lambda: make_veins_curve(P, pms_t.get_value(), RVR_BASE))
        h_lab, v_lab = make_curve_labels(P)

        pra_fn = lambda: operating_point(Q_HEART_B, pms_t.get_value(), RVR_BASE)[0]
        q_fn = lambda: operating_point(Q_HEART_B, pms_t.get_value(), RVR_BASE)[1]
        drops = make_drop_lines(P, pra_fn, q_fn)
        dot = P.dot(pra_fn, q_fn, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: Q_HEART_B, pms_t.get_value, lambda: RVR_BASE)
        rows = build_rule_rows(dimmed=True)
        btns, v_btn, a_btn = build_vessel_buttons(lit=None)

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot, rows, btns)

        self.at("suppose the veins")
        v_lit = boxed_label("veins", color=GREEN, size=26, box=(1.8, 0.65), fill_opacity=0.35).move_to(v_btn)
        self.play(Transform(v_btn, v_lit), run_time=0.5)

        self.at("filling pressure falls")
        pms_ring = Circle(radius=0.16, color=GREEN, stroke_width=4).move_to(P.pt(7, 0))
        shift_tag = T("shift size schematic", size=24, color=GREY).move_to([4.0, -0.7, 0])
        self.play(FadeIn(pms_ring), FadeIn(shift_tag), run_time=0.6)

        self.at("sliding left")
        ghost_v = make_veins_curve(P, PMS_BASE, RVR_BASE, color=GREY, width=4, dashed=True, opacity=0.8)
        self.add(ghost_v)
        self.bring_to_front(veins, heart, drops, dot)
        self.play(pms_t.animate.set_value(5.0), pms_ring.animate.move_to(P.pt(5, 0)), run_time=1.8)

        self.at("slide down")
        arr_down = make_axis_arrows(P, y_dir=DOWN, x_dir=LEFT, y_col=BLUE, x_col=BLUE, x_pra=3.4)
        self.play(FadeIn(arr_down), rows[0].animate.set_opacity(1.0), run_time=0.6)

        self.at("both fall")
        self.play(Indicate(rows[0], color=GREEN, scale_factor=1.06), run_time=0.7)
        v_dim = boxed_label("veins", color=TEXT, size=26, box=(1.8, 0.65), fill_opacity=0.12).move_to(v_btn)
        self.play(
            pms_t.animate.set_value(PMS_BASE),
            FadeOut(ghost_v),
            FadeOut(pms_ring),
            FadeOut(arr_down),
            FadeOut(shift_tag),
            rows[0].animate.set_opacity(0.65),
            Transform(v_btn, v_dim),
            run_time=0.9,
        )
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        rvr_t = ValueTracker(RVR_BASE)
        heart = make_heart_curve(P, Q_HEART_B)
        veins = always_redraw(lambda: make_veins_curve(P, PMS_BASE, rvr_t.get_value()))
        h_lab, v_lab = make_curve_labels(P)
        drops = make_drop_lines(P, lambda: 2.0, lambda: 5.0)
        dot = P.dot(lambda: 2.0, lambda: 5.0, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: Q_HEART_B, lambda: PMS_BASE, rvr_t.get_value)
        rows = build_rule_rows(dimmed=True)
        btns, _, _ = build_vessel_buttons(lit=None)

        self.add(P, collapse, tag, heart, veins, h_lab, v_lab, flow, drops, dot, rows, btns)

        self.at("resistance")
        pivot = Circle(radius=0.18, color=GREEN, stroke_width=4).move_to(P.pt(7, 0))
        self.play(FadeIn(pivot), run_time=0.6)

        self.at("nothing else")
        ghost_v = make_veins_curve(P, PMS_BASE, RVR_BASE, color=GREY, width=4, dashed=True, opacity=0.8)
        self.add(ghost_v)
        self.bring_to_front(veins, heart, drops, dot, pivot)
        self.play(rvr_t.animate.set_value(0.5), run_time=3.2)

        self.at("zero flow point")
        self.play(Indicate(pivot, color=GREEN, scale_factor=1.35), run_time=0.7)

        dot._ft = 0.0
        dot.add_updater(lambda m, dt: (setattr(m, "_ft", m._ft + dt), m.set_opacity(0.78 + 0.22 * np.sin(3.5 * m._ft))))

        self.at("which way")
        q_card = question_card("Output and Pra: which way?", y=3.25, color=TEXT, size=36)
        self.play(FadeIn(q_card), run_time=0.6)
        self.finish()


class S08PredictHold(PredictPause):
    QUESTION = "Output and Pra: which way?"
    CARD = {"y": 3.25, "color": TEXT, "size": 36}
    RING_AT = (5.4, -1.9, 0)
    SECONDS = 4.5

    def backdrop(self):
        P, collapse, tag = build_base_plot()
        heart = make_heart_curve(P, Q_HEART_B)
        ghost_v = make_veins_curve(P, PMS_BASE, RVR_BASE, color=GREY, width=4, dashed=True, opacity=0.8)
        veins = make_veins_curve(P, PMS_BASE, 0.5)
        h_lab, v_lab = make_curve_labels(P)
        pivot = Circle(radius=0.18, color=GREEN, stroke_width=4).move_to(P.pt(7, 0))
        drops = make_drop_lines(P, lambda: 2.0, lambda: 5.0)
        dot = P.dot(lambda: 2.0, lambda: 5.0, color=YELLOW, ring=TEXT, radius=0.13)
        dot._ft = 0.0
        dot.add_updater(lambda m, dt: (setattr(m, "_ft", m._ft + dt), m.set_opacity(0.78 + 0.22 * np.sin(3.0 * m._ft))))
        flow = make_flow_dots(P, lambda: Q_HEART_B, lambda: PMS_BASE, lambda: 0.5)
        rows = build_rule_rows(dimmed=True)
        btns, _, _ = build_vessel_buttons(lit=None)
        return VGroup(P, collapse, tag, ghost_v, veins, heart, h_lab, v_lab, pivot, flow, drops, dot, rows, btns)


class S09Answer(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        pra_t = ValueTracker(2.0)
        q_fn = lambda: q_heart(pra_t.get_value(), Q_HEART_B)

        heart = make_heart_curve(P, Q_HEART_B)
        ghost_v = make_veins_curve(P, PMS_BASE, RVR_BASE, color=GREY, width=4, dashed=True, opacity=0.8)
        veins = make_veins_curve(P, PMS_BASE, 0.5)
        h_lab, v_lab = make_curve_labels(P)
        pivot = Circle(radius=0.18, color=GREEN, stroke_width=4).move_to(P.pt(7, 0))
        drops = make_drop_lines(P, pra_t.get_value, q_fn)
        dot = P.dot(pra_t.get_value, q_fn, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: Q_HEART_B, lambda: PMS_BASE, lambda: 0.5)
        rows = build_rule_rows(dimmed=True)
        btns, _, _ = build_vessel_buttons(lit=None)
        q_card = question_card("Output and Pra: which way?", y=3.25, color=TEXT, size=36)
        ro = build_readout(pra_t.get_value, q_fn)

        self.add(P, collapse, tag, ghost_v, veins, heart, h_lab, v_lab, pivot, flow, drops, dot, rows, btns, q_card, ro)

        pra_ans, q_ans = operating_point(Q_HEART_B, PMS_BASE, 0.5)  # 3.67, 6.67

        self.play(FadeOut(q_card), run_time=0.4)

        self.at("slide along")
        self.play(
            pra_t.animate.set_value(pra_ans),
            rows[0].animate.set_opacity(1.0),
            run_time=2.2,
        )

        self.at("both rise")
        self.play(Indicate(rows[0], color=GREEN, scale_factor=1.06), run_time=0.7)

        self.at("from 2")
        x_step = Arrow(P.pt(2.0, 0.52), P.pt(pra_ans, 0.52), color=YELLOW, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.25)
        self.play(GrowArrow(x_step, run_time=1.0), ro.box.animate(rate_func=there_and_back, run_time=1.4).set_stroke(YELLOW, width=5))

        self.at("millimeters of mercury")
        self.play(FadeOut(x_step), run_time=0.4)

        self.at("from 5")
        y_step = Arrow(P.pt(-3.3, 5.0), P.pt(-3.3, q_ans), color=YELLOW, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.25)
        self.play(GrowArrow(y_step, run_time=1.0), ro.box.animate(rate_func=there_and_back, run_time=1.4).set_stroke(YELLOW, width=5))

        self.at("liters a minute")
        self.play(FadeOut(y_step), FadeOut(ghost_v), FadeOut(pivot), rows[0].animate.set_opacity(0.65), run_time=0.6)
        self.finish()


class S10Arterioles(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        b_t = ValueTracker(Q_HEART_B)
        pra_0, q_0 = operating_point(Q_HEART_B, PMS_BASE, 0.5)  # 3.67, 6.67

        heart = always_redraw(lambda: make_heart_curve(P, b_t.get_value()))
        veins = make_veins_curve(P, PMS_BASE, 0.5)
        h_lab, v_lab = make_curve_labels(P)
        drops = make_drop_lines(P, lambda: pra_0, lambda: q_0)
        dot = P.dot(lambda: pra_0, lambda: q_0, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, b_t.get_value, lambda: PMS_BASE, lambda: 0.5)
        rows = build_rule_rows(dimmed=True)
        btns, _, a_btn = build_vessel_buttons(lit=None)
        ro = build_readout(lambda: pra_0, lambda: q_0)

        self.add(P, collapse, tag, veins, heart, h_lab, v_lab, flow, drops, dot, rows, btns, ro)

        self.at("arteriolar dilation")
        a_lit = boxed_label("arterioles", color=BLUE, size=26, box=(2.2, 0.65), fill_opacity=0.35).move_to(a_btn)
        self.play(Transform(a_btn, a_lit), run_time=0.6)

        self.at("lowers resistance")
        pivot = Circle(radius=0.18, color=GREEN, stroke_width=4).move_to(P.pt(7, 0))
        glow_v = make_veins_curve(P, PMS_BASE, 0.5, color=GREEN, width=14, opacity=0.35)
        self.add(glow_v)
        self.bring_to_front(veins, heart, drops, dot, pivot)
        self.play(FadeIn(pivot), FadeIn(glow_v), Indicate(pivot, color=GREEN, scale_factor=1.35), run_time=1.3)

        self.at("tilting")
        tilt_arr = CurvedArrow(
            P.pt(4.3, 2.7),
            P.pt(4.9, 4.2),
            angle=-0.35,
            color=GREEN,
            stroke_width=5,
            tip_length=0.22,
        )
        self.play(Create(tilt_arr), glow_v.animate(rate_func=there_and_back).set_stroke(width=18, opacity=0.55), run_time=1.2)

        self.at("lowers afterload")
        ghost_h = make_heart_curve(P, Q_HEART_B, color=GREY, width=4, dashed=True, opacity=0.8)
        self.add(ghost_h)
        self.bring_to_front(heart, drops, dot)
        self.play(
            FadeOut(pivot),
            FadeOut(glow_v),
            FadeOut(tilt_arr),
            b_t.animate.set_value(4.0),
            run_time=2.4,
        )

        self.at("two lines move")
        tilt_tag = T("tilt", size=26, color=GREEN).move_to(P.pt(5.5, 4.7))
        lift_tag = T("lift", size=26, color=BLUE).move_to(P.pt(0.7, 6.0))
        self.play(FadeIn(tilt_tag), FadeIn(lift_tag), run_time=0.6)
        self.finish()


class S11BothLines(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        pra_0, q_0 = operating_point(Q_HEART_B, PMS_BASE, 0.5)   # 3.67, 6.67
        pra_1, q_1 = operating_point(4.0, PMS_BASE, 0.5)         # 3.33, 7.33

        pra_t = ValueTracker(pra_0)
        q_t = ValueTracker(q_0)

        ghost_h = make_heart_curve(P, Q_HEART_B, color=GREY, width=4, dashed=True, opacity=0.8)
        heart = make_heart_curve(P, 4.0)
        veins = make_veins_curve(P, PMS_BASE, 0.5)
        h_lab, v_lab = make_curve_labels(P)

        base_dot = Dot(P.pt(2.0, 5.0), radius=0.10, color=GREY).set_opacity(0.75)
        drops = make_drop_lines(P, pra_t.get_value, q_t.get_value)
        dot = P.dot(pra_t.get_value, q_t.get_value, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: 4.0, lambda: PMS_BASE, lambda: 0.5)
        rows = build_rule_rows(dimmed=True)
        btns, _, _ = build_vessel_buttons(lit="arterioles")
        ro = build_readout(pra_t.get_value, q_t.get_value)
        tilt_tag = T("tilt", size=26, color=GREEN).move_to(P.pt(5.5, 4.7))
        lift_tag = T("lift", size=26, color=BLUE).move_to(P.pt(0.7, 6.0))

        self.add(P, collapse, tag, ghost_h, veins, heart, h_lab, v_lab, base_dot, flow, drops, dot, rows, btns, ro, tilt_tag, lift_tag)

        self.at("both shifts")
        self.play(pra_t.animate.set_value(pra_1), q_t.animate.set_value(q_1), run_time=2.0)

        self.at("pull opposite ways")
        t_lbl = T("tilt", size=24, color=GREEN)
        t_arr = Arrow(ORIGIN, RIGHT * 1.35, color=GREEN, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.22)
        t_grp = VGroup(t_lbl, t_arr).arrange(RIGHT, buff=0.14)

        l_arr = Arrow(ORIGIN, LEFT * 0.65, color=BLUE, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.36)
        l_lbl = T("lift", size=24, color=BLUE)
        l_grp = VGroup(l_arr, l_lbl).arrange(RIGHT, buff=0.14)

        opp_grp = VGroup(t_grp, l_grp).arrange(RIGHT, buff=0.55).move_to([-2.0, -3.26, 0])
        self.play(FadeIn(opp_grp), run_time=0.6)

        self.at("larger shift wins")
        self.play(Indicate(t_grp, color=GREEN, scale_factor=1.08), l_grp.animate.set_opacity(0.45), run_time=0.9)

        self.at("tilt wins")
        self.play(Indicate(t_grp, color=GREEN, scale_factor=1.10), t_arr.animate(rate_func=there_and_back).set_stroke(width=9), run_time=1.0)

        self.at("reaches about")
        y_step = Arrow(P.pt(-3.3, 5.0), P.pt(-3.3, q_1), color=YELLOW, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.22)
        self.play(GrowArrow(y_step, run_time=1.0), ro.box.animate(rate_func=there_and_back, run_time=1.4).set_stroke(YELLOW, width=5))
        self.play(FadeOut(y_step), run_time=0.4)

        self.at("atrial pressure about")
        x_step = Arrow(P.pt(2.0, 0.52), P.pt(pra_1, 0.52), color=YELLOW, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.28)
        self.play(
            GrowArrow(x_step, run_time=1.0),
            Indicate(dot, color=YELLOW, scale_factor=1.35, run_time=1.0),
            ro.box.animate(rate_func=there_and_back, run_time=1.4).set_stroke(YELLOW, width=5),
        )
        self.play(FadeOut(x_step), run_time=0.4)

        self.at("chosen for clarity")
        clarity = T("sizes chosen for clarity", size=24, color=GREY).move_to([3.95, -2.25, 0])
        self.play(FadeIn(clarity), run_time=0.6)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        P, collapse, tag = build_base_plot()
        pra_1, q_1 = operating_point(4.0, PMS_BASE, 0.5)  # 3.33, 7.33

        heart = make_heart_curve(P, 4.0)
        veins = make_veins_curve(P, PMS_BASE, 0.5)
        h_lab, v_lab = make_curve_labels(P)
        base_dot = Dot(P.pt(2.0, 5.0), radius=0.10, color=GREY).set_opacity(0.75)
        drops = make_drop_lines(P, lambda: pra_1, lambda: q_1)
        dot = P.dot(lambda: pra_1, lambda: q_1, color=YELLOW, ring=TEXT, radius=0.13)
        flow = make_flow_dots(P, lambda: 4.0, lambda: PMS_BASE, lambda: 0.5)
        rows = build_rule_rows(dimmed=True)

        self.add(P, collapse, tag, veins, heart, h_lab, v_lab, base_dot, flow, drops, dot, rows)

        self.at("atrial pressure")
        q_text = T("Pra: up or down?", size=38, color=TEXT).move_to([2.1, 3.28, 0])
        self.play(FadeIn(q_text, shift=UP * 0.1), run_time=0.6)

        self.at("depends which vessels")
        self.play(FadeOut(q_text), run_time=0.5)
        self.play(veins.animate(rate_func=there_and_back, run_time=1.4).set_stroke(width=9))

        self.at("spot the shifted line")
        glow_h = make_heart_curve(P, 4.0, color=BLUE, width=16, opacity=0.40)
        self.add(glow_h)
        self.bring_to_front(heart, drops, dot)
        self.play(
            FadeIn(glow_h),
            heart.animate.set_stroke(width=10),
            rows[1].animate.set_opacity(1.0),
            run_time=0.8,
        )
        self.play(
            FadeOut(glow_h),
            heart.animate.set_stroke(width=6),
            rows[1].animate.set_opacity(0.65),
            run_time=0.6,
        )

        self.at("the unmoved one")
        glow = make_veins_curve(P, PMS_BASE, 0.5, color=GREEN, width=16, opacity=0.42)
        settle_arr = Arrow(
            P.pt(5.6, 2.8) + UR * 0.22,
            P.pt(3.65, 6.7) + UR * 0.22,
            color=GREEN,
            stroke_width=6,
            buff=0,
            max_tip_length_to_length_ratio=0.14,
        )
        self.add(glow)
        self.bring_to_front(veins, drops, dot)
        self.play(
            FadeIn(glow),
            veins.animate.set_stroke(width=9),
            rows[0].animate.set_opacity(1.0),
            run_time=0.8,
        )
        self.play(
            GrowArrow(settle_arr),
            Indicate(dot, color=YELLOW, scale_factor=1.3),
            run_time=1.0,
        )
        self.play(FadeOut(settle_arr), rows[0].animate.set_opacity(0.65), run_time=0.6)
        self.finish()


class S13End(EndCard):
    LINE = "The crossing slides along the unmoved line; its slope sets the direction."
