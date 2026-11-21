"""
Power Falls Furthest — Skeletal Muscle Mechanics (Chapter 2)

COLOUR MAP (one colour per concept across the whole film):
- BLUE (#58C4DD):    skeletal muscle & myosin heads
- ORANGE (#FF862F):  load & force (holding force, twitch force, laser-trap trace)
- YELLOW (#F5D547):  shortening speed & speed-load curve
- GREEN (#83C167):   external power & power-load curve
- RED (#FC6255):     rejected / zero (lactate cross-out)
- GOLD (#D4A843):    titles, questions, emphasis handles & key takeaways
- GREY (#8B93A1):    axes, ceiling bar, actin/thick filament structure, dimmed lactate chip
- CYAN (#2EE6D6):    calcium (Ca2+) & calcium store
- MAGENTA (#E85FD5): inorganic phosphate (Pi)
- WHITE (#FFFFFF):   protons (H+)
- TEXT (#E8EAF0):    body labels, tick numbers & live readouts

ONE WORLD:
A BLUE model muscle hanging from a GREY ceiling bar lifts an ORANGE load block beside live
force and power bars and Hill's computed speed-load and power-load curves; zooming into the
muscle reveals the schematic myosin/actin motor and calcium store, then a single myosin-actin
laser trap, then rat metabolite meters, before pulling back to the opening muscle and bars.

WHAT CHANGES PER SPOKEN SCENE:
- s00_link_and_question: ghost power curve draws to 1/3 load peak, muscle lifts load with rising lift counter, ORANGE force bar drops 100->80 N, GREEN power bar drops 3.8->1.8 W.
- s02_fatigue: muscle shrinks to lifting icon while computed Hill speed & power plots appear; ceiling (F0), top speed (vmax), and sag (a/F0) bob in turn.
- s03_ceiling: fresh curves leave ghosts; ceiling slides 100->80 N (F0, a scale) reshaping both curves so peak power drops 3.8->3.1 W (-20%).
- s04_predict: top speed slides 0.40->0.32 m/s (b scales) reshaping the speed curve while the power curve waits dimmed at 3.1 W.
- s06_answer: 0.8 x 0.8 = 0.64 combines; power curve updates to 2.44 W (-36%).
- s07_sag: curvature a/F0 drops 0.25->0.15 at fixed endpoints, bowing speed lower and shrinking peak power to 1.80 W (-53%).
- s08_rule: plots part for the force & power bars; three speed-curve handles connect into the shrunken GREEN power bar.
- s09_suspects: zooms into fibre interior with cycling myosin heads & Ca2+ stream; lactate is crossed out, Pi gathers, Ca2+ thins, fewer H+ appear, 3 question marks hover.
- s10_motor: zooms to laser trap with myosin pulls moving bead & spiking ORANGE trace; H+ cuts spikes ~20%, Pi removes tallest spikes & shortens grips.
- s11_rats: fibre at left while two rat time-strips sweep live: force holds until Pi crosses breakpoint while protons rise; second strip shows faster stimulation.
- s12_close: returns to opening muscle + load and bars; 80 N force, 0.32 m/s speed, and sag badge pulse into the 1.8 W power bar.
"""

from bp_parts import *

CYAN = "#2EE6D6"
MAGENTA = "#E85FD5"
MODEL_TAG = "model muscle, made-up numbers"


# ------------------------------------------------------------------ Hill model equations (computed)
def hill_v(F, F0=100.0, a=25.0, b=0.100):
    return np.maximum(0.0, b * (F0 - F) / np.maximum(F + a, 1e-6))


def hill_p(F, F0=100.0, a=25.0, b=0.100):
    return F * hill_v(F, F0, a, b)


def hill_peak(F0=100.0, a=25.0, b=0.100):
    q = a / max(F0, 1e-6)
    f_star = np.sqrt(q * q + q) - q
    F_best = f_star * F0
    return F_best, hill_p(F_best, F0, a, b)


def _tag(text=MODEL_TAG):
    t = T(text, size=22, color=TEXT)
    return t.move_to([FRAME_X - 0.15 - t.width / 2, -FRAME_Y + 0.22 + t.height / 2, 0])


# ------------------------------------------------------------------ Shared world builders
def build_muscle_rig(center=(-3.6, 0.25, 0), scale=1.0, phase_tracker=None, label_inside=True):
    """Ceiling bar + BLUE muscle block + tendon + ORANGE load block driven by phase_tracker in [0, 1]."""
    cx_tr = ValueTracker(float(center[0]))
    cy_tr = ValueTracker(float(center[1]))
    tr = phase_tracker if phase_tracker is not None else ValueTracker(0.0)

    base_h = 2.65 * scale
    base_w = 1.50 * scale
    tendon_len = 0.60 * scale
    load_h = 1.05 * scale
    load_w = 1.70 * scale

    def _mk_rig():
        cx = cx_tr.get_value()
        cy = cy_tr.get_value()
        ceil_y = cy + 2.55 * scale
        ceil_bar = Line(
            [cx - 1.75 * scale, ceil_y, 0],
            [cx + 1.75 * scale, ceil_y, 0],
            color=GREY,
            stroke_width=8 * scale,
        )
        lift = float(tr.get_value())
        h = base_h * (1.0 - 0.26 * lift)
        w = base_w / np.sqrt(1.0 - 0.26 * lift)
        m_top = ceil_y - 0.04 * scale
        m_bot = m_top - h
        muscle = RoundedRectangle(
            corner_radius=0.28 * scale,
            width=w,
            height=h,
            stroke_color=BLUE,
            stroke_width=4.5 * scale,
            fill_color=BLUE,
            fill_opacity=0.38,
        ).move_to([cx, (m_top + m_bot) / 2, 0])
        tendon = Line(
            [cx, m_bot, 0],
            [cx, m_bot - tendon_len, 0],
            color=GREY,
            stroke_width=5 * scale,
        )
        load_box = RoundedRectangle(
            corner_radius=0.14 * scale,
            width=load_w,
            height=load_h,
            stroke_color=ORANGE,
            stroke_width=4.5 * scale,
            fill_color=ORANGE,
            fill_opacity=0.38,
        ).move_to([cx, m_bot - tendon_len - load_h / 2, 0])
        grp = VGroup(ceil_bar, muscle, tendon, load_box)
        if label_inside:
            m_lbl = T("muscle", size=max(22, int(round(30 * scale))), color=TEXT).move_to(muscle)
            l_lbl = T("load", size=max(22, int(round(28 * scale))), color=TEXT).move_to(load_box)
            grp.add(m_lbl, l_lbl)
        return grp

    body = always_redraw(_mk_rig)
    rig = VGroup(body)
    rig.phase = tr
    rig.cx_tr = cx_tr
    rig.cy_tr = cy_tr
    return rig


def start_lift_updater(rig_or_tr, freq=0.50, progressive_slow=False, lift_counter_tr=None):
    """Attach a mechanical lift-and-lower updater to rig (a VGroup in the scene). Updates rig.phase."""
    phase_tr = rig_or_tr.phase if hasattr(rig_or_tr, "phase") else rig_or_tr
    state = {"t": 0.0, "cycle": 0, "counted": False}

    def _upd(mob, dt):
        state["t"] += dt
        period = (1.35 + 0.42 * state["cycle"]) if progressive_slow else (1.0 / freq)
        u = state["t"] / period
        if u >= 1.0:
            state["t"] -= period
            state["cycle"] += 1
            state["counted"] = False
            period = (1.35 + 0.42 * state["cycle"]) if progressive_slow else (1.0 / freq)
            u = state["t"] / period
        val = 0.5 * (1.0 - np.cos(TAU * u))
        phase_tr.set_value(val)
        if lift_counter_tr is not None and u >= 0.48 and not state["counted"]:
            state["counted"] = True
            lift_counter_tr.set_value(lift_counter_tr.get_value() + 1)

    rig_or_tr.add_updater(_upd)
    return rig_or_tr


def build_bars(
    f_tr,
    p_tr,
    x_force=1.4,
    x_power=4.4,
    y_base=-2.1,
    max_h=3.6,
    bar_w=1.30,
    show_ghost_outline=False,
    v_tr=None,
    x_speed=None,
    two_line_labels=False,
    speed_bar_w=1.35,
):
    """Tall vertical bars on one baseline: ORANGE holding force (0..100 N) and GREEN peak power (0..4 W)."""
    left_x = min(x_force, x_power) - bar_w * 0.65
    right_x = max(x_force, x_power) + bar_w * 0.65
    baseline = Line([left_x, y_base, 0], [right_x, y_base, 0], color=GREY, stroke_width=4)
    g = VGroup(baseline)

    def _bar_group(x, tr, max_val, col, label_txt, fmt, w=bar_w, ghost=False, num_size=28):
        out = VGroup()
        if ghost:
            gh = max_h if max_val == 100.0 else (max_h * (3.8 / 4.0) if max_val == 4.0 else max_h)
            # Top and vertical side markers for fresh level, leaving interior clear for bar value
            ghost_outline = VGroup(
                DashedLine([x - w / 2, y_base, 0], [x - w / 2, y_base + gh, 0], color=col, stroke_width=2.5),
                DashedLine([x + w / 2, y_base, 0], [x + w / 2, y_base + gh, 0], color=col, stroke_width=2.5),
                DashedLine([x - w / 2, y_base + gh, 0], [x + w / 2, y_base + gh, 0], color=col, stroke_width=2.5),
            ).set_opacity(0.55)
            out.add(ghost_outline)

        def _dyn():
            val = max(0.0, float(tr.get_value()))
            frac = np.clip(val / max_val, 0.01, 1.0)
            h = max_h * frac
            rect = Rectangle(
                width=w,
                height=h,
                stroke_color=col,
                stroke_width=3.5,
                fill_color=col,
                fill_opacity=0.45,
            ).move_to([x, y_base + h / 2, 0])
            num = M(fmt.format(val), size=num_size, color=TEXT).next_to(rect, UP, buff=0.14)
            return VGroup(rect, num)

        lbl_str = label_txt.replace(" ", "\n") if two_line_labels else label_txt
        lbl = T(lbl_str, size=25 if two_line_labels else 28, color=col, line_spacing=0.85)
        lbl.move_to([x, y_base - (0.48 if two_line_labels else 0.38), 0])
        out.add(always_redraw(_dyn), lbl)
        return out

    g.force_grp = _bar_group(x_force, f_tr, 100.0, ORANGE, "holding force", "{:.0f} N", ghost=show_ghost_outline)
    g.power_grp = _bar_group(x_power, p_tr, 4.0, GREEN, "peak power", "{:.1f} W", ghost=show_ghost_outline)
    g.add(g.force_grp, g.power_grp)

    if v_tr is not None and x_speed is not None:
        g.speed_grp = _bar_group(
            x_speed,
            v_tr,
            0.40,
            YELLOW,
            "top speed",
            "{:.2f} m/s",
            w=speed_bar_w,
            ghost=show_ghost_outline,
            num_size=24,
        )
        g.add(g.speed_grp)
    return g


def build_two_plots(
    F0_tr,
    a_tr,
    b_tr,
    p_F0_tr=None,
    p_a_tr=None,
    p_b_tr=None,
    left_box=(-6.0, -0.5, -1.95, 1.60),
    right_box=(0.75, 6.25, -1.95, 1.60),
    power_opacity_tr=None,
    with_ghosts=False,
    xticks=(0, 25, 50, 75, 100),
):
    """Build Hill speed-load and power-load plots driven by trackers."""
    pF0 = p_F0_tr or F0_tr
    pa = p_a_tr or a_tr
    pb = p_b_tr or b_tr
    pop = power_opacity_tr if power_opacity_tr is not None else ValueTracker(1.0)

    Pv = Plot(
        box=left_box,
        xr=(0, 105),
        yr=(0, 0.44),
        xticks=list(xticks),
        yticks=[(0, "0"), (0.2, "0.2"), (0.4, "0.4")],
        xlabel="load F (N)",
        ylabel="speed v (m/s)",
        color=GREY,
        size=22,
        label_size=26,
    )
    Pp = Plot(
        box=right_box,
        xr=(0, 105),
        yr=(0, 4.2),
        xticks=list(xticks),
        yticks=[(0, "0"), (2, "2"), (4, "4")],
        xlabel="load F (N)",
        ylabel="power P (W)",
        color=GREY,
        size=22,
        label_size=26,
    )
    for P in (Pv, Pp):
        P.tick_labels.set_color(TEXT)
        for tk in P.tick_labels:
            # Give extra 0.05 clearance from axes/endpoint dots
            if tk.get_center()[0] < P.x0:
                tk.shift(LEFT * 0.05)
            else:
                tk.shift(DOWN * 0.04)
        if P.xlabel:
            P.xlabel.set_color(TEXT).shift(DOWN * 0.04)
        if P.ylabel:
            P.ylabel.set_color(TEXT)

    ghosts = VGroup()
    if with_ghosts:
        gv = Pv.curve(lambda x: hill_v(x, 100.0, 25.0, 0.100), x0=0, x1=100.0, color=YELLOW, width=4, opacity=0.35)
        gp = Pp.curve(lambda x: hill_p(x, 100.0, 25.0, 0.100), x0=0, x1=100.0, color=GREEN, width=4, opacity=0.35)
        # Put 'fresh' outside to the upper-right of the fresh curve, never near peak labels
        glab = T("fresh", size=24, color=TEXT).move_to(Pp.pt(78, 2.75))
        ghosts.add(gv, gp, glab)

    def _v_dyn():
        F0, a, b = F0_tr.get_value(), a_tr.get_value(), b_tr.get_value()
        vmax = b * F0 / max(a, 1e-6)
        c = Pv.curve(lambda x: hill_v(x, F0, a, b), x0=0, x1=F0, color=YELLOW, width=7)
        d_f0 = Dot(Pv.pt(F0, 0), radius=0.085, color=ORANGE, stroke_color=TEXT, stroke_width=2)
        d_vm = Dot(Pv.pt(0, vmax), radius=0.085, color=YELLOW, stroke_color=TEXT, stroke_width=2)
        return VGroup(c, d_f0, d_vm)

    def _p_dyn():
        F0, a, b = pF0.get_value(), pa.get_value(), pb.get_value()
        op = float(pop.get_value())
        c = Pp.curve(lambda x: hill_p(x, F0, a, b), x0=0, x1=F0, color=GREEN, width=7, opacity=op)
        fb, pbv = hill_peak(F0, a, b)
        dot = Dot(Pp.pt(fb, pbv), radius=0.095, color=GREEN, stroke_color=TEXT, stroke_width=2).set_opacity(op)
        return VGroup(c, dot)

    v_live = always_redraw(_v_dyn)
    p_live = always_redraw(_p_dyn)
    return Pv, Pp, v_live, p_live, ghosts


def build_compact_fibre(center=(-3.85, 0.1, 0), scale=0.72, head_phase=None, show_tokens=True):
    """Compact schematic fibre view used in s11 with tokens cleanly placed between myosin stems."""
    cx, cy, _ = center
    tr = head_phase if head_phase is not None else ValueTracker(0.0)
    sac = RoundedRectangle(
        corner_radius=0.22 * scale,
        width=5.4 * scale,
        height=1.05 * scale,
        stroke_color=CYAN,
        stroke_width=3.5,
        fill_color=CYAN,
        fill_opacity=0.24,
    ).move_to([cx, cy + 2.15 * scale, 0])
    sac_lbl = T("calcium store", size=24, color=CYAN).move_to(sac)

    actin = RoundedRectangle(
        corner_radius=0.08 * scale,
        width=5.8 * scale,
        height=0.28 * scale,
        stroke_color=GREY,
        stroke_width=3,
        fill_color=GREY,
        fill_opacity=0.45,
    ).move_to([cx, cy + 0.55 * scale, 0])
    actin_lbl = T("actin", size=24, color=TEXT).next_to(actin, UP, buff=0.10).align_to(actin, LEFT)

    thick = RoundedRectangle(
        corner_radius=0.10 * scale,
        width=5.8 * scale,
        height=0.44 * scale,
        stroke_color=GREY,
        stroke_width=3,
        fill_color=GREY,
        fill_opacity=0.45,
    ).move_to([cx, cy - 1.35 * scale, 0])
    thick_lbl = T("myosin", size=24, color=BLUE).next_to(thick, DOWN, buff=0.12)

    # 4 well-spaced heads so tokens fit cleanly in the wide gaps between stems
    xs = np.array([-2.1, -0.7, 0.7, 2.1]) * scale + cx

    def _heads():
        ph = tr.get_value()
        g = VGroup()
        for idx, hx in enumerate(xs):
            ang = 0.14 * np.sin(ph + idx * 0.9)
            base = np.array([hx, cy - 1.13 * scale, 0])
            tip = base + np.array([np.sin(ang) * 0.45 * scale, 1.25 * scale, 0])
            stem = Line(base, tip, color=BLUE, stroke_width=5 * scale)
            knob = Dot(tip, radius=0.16 * scale, color=BLUE, stroke_color=TEXT, stroke_width=2)
            g.add(stem, knob)
        return g

    grp = VGroup(sac, sac_lbl, actin, actin_lbl, thick, thick_lbl, always_redraw(_heads))
    if show_tokens:
        # Place Pi and H+ in wide gaps between stems (-1.4, 0.0, +1.4) with r=0.31 circles (zero overflow/tight)
        pi_dots = VGroup(*[
            VGroup(
                Circle(radius=0.31, color=MAGENTA, stroke_width=2.5, fill_color=MAGENTA, fill_opacity=0.28),
                M("Pi", size=22, color=MAGENTA),
            ).move_to([cx + dx * scale, cy + dy * scale, 0])
            for dx, dy in [(-1.4, -0.25), (1.4, -0.25)]
        ])
        h_dots = VGroup(*[
            VGroup(
                Circle(radius=0.31, color=WHITE, stroke_width=2.5, fill_color=WHITE, fill_opacity=0.18),
                M("H+", size=22, color=WHITE),
            ).move_to([cx + dx * scale, cy + dy * scale, 0])
            for dx, dy in [(0.0, -0.55)]
        ])
        ca_dots = VGroup(*[
            Dot(radius=0.07, color=CYAN).move_to([cx + dx * scale, cy + 1.20 * scale, 0])
            for dx in [-0.7, 0.6]
        ])
        grp.add(pi_dots, h_dots, ca_dots)
        grp.pi_dots, grp.h_dots, grp.ca_dots = pi_dots, h_dots, ca_dots
        grp.sac, grp.thick = sac, thick
    return grp


# ------------------------------------------------------------------ SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        lifts_tr = ValueTracker(0.0)
        f_tr = ValueTracker(100.0)
        p_tr = ValueTracker(3.8)

        rig = build_muscle_rig(center=(-3.8, 0.25, 0), scale=1.0, phase_tracker=lift_phase)
        bars = build_bars(f_tr, p_tr, x_force=1.20, x_power=4.55, y_base=-2.1, max_h=3.6, bar_w=1.20)
        tag = _tag(MODEL_TAG)

        # Ghost power curve behind bars; peak at x = 0.65 + 0.309 * (5.15 - 0.65) = 2.04 (clear of ORANGE bar <= 1.80)
        ghost_plot = Plot(
            box=(0.65, 5.15, -2.05, 0.70),
            xr=(0, 100),
            yr=(0, 4.2),
            color=GREY,
            stroke=2,
        )
        ghost_axes = ghost_plot.axes.set_opacity(0.30)
        ghost_t = ValueTracker(0.0)
        ghost_curve = ghost_plot.live_curve(lambda x: hill_p(x, 100, 25, 0.100), ghost_t, color=GREEN, width=5)
        ghost_curve.set_opacity(0.48)
        fb, pb = hill_peak(100, 25, 0.100)
        peak_pt = ghost_plot.pt(fb, pb)
        peak_lbl = T("~1/3 load", size=24, color=GREEN).move_to([2.90, 0.88, 0])
        peak_line = DashedLine(ghost_plot.pt(fb, 0), peak_pt, color=GREEN, stroke_width=3)
        peak_arrow = Line(peak_pt + UR * 0.08, peak_lbl.get_left() + LEFT * 0.08, color=GREEN, stroke_width=2.5)
        peak_mark = VGroup(Dot(peak_pt, radius=0.10, color=GREEN), peak_line, peak_arrow, peak_lbl)

        self.add(rig, bars, tag)
        self.add(ghost_axes, ghost_curve)
        self.play(ghost_t.animate.set_value(100.0), run_time=3.1, rate_func=linear)
        self.play(FadeIn(peak_mark), run_time=0.7)
        self.wait(0.9)
        self.play(FadeOut(ghost_axes), FadeOut(ghost_curve), FadeOut(peak_mark), run_time=0.8)

        self.at("again and again")
        lift_cnt = counter("lifts: {:.0f}", lifts_tr, at=[-3.8, -2.95, 0], size=28, color=TEXT)
        self.play(FadeIn(lift_cnt), run_time=0.3)
        start_lift_updater(rig, progressive_slow=True, lift_counter_tr=lifts_tr)

        self.at("dips a little")
        self.play(f_tr.animate.set_value(80.0), run_time=1.3)

        self.at("why")
        q_txt = T("Why does power fall further?", size=38, color=GOLD).move_to([0.0, 3.25, 0])
        self.play(FadeIn(q_txt, shift=DOWN * 0.1, run_time=0.5), p_tr.animate(run_time=1.8).set_value(1.8))
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        f_tr = ValueTracker(80.0)
        p_tr = ValueTracker(1.8)

        rig = build_muscle_rig(center=(-3.8, 0.25, 0), scale=1.0, phase_tracker=lift_phase)
        start_lift_updater(rig, freq=0.50)
        bars = build_bars(f_tr, p_tr, x_force=1.20, x_power=4.55, y_base=-2.1, max_h=3.6, bar_w=1.20)
        q_txt = T("Why does power fall further?", size=38, color=GOLD).move_to([0.0, 3.25, 0])
        title = T("Power Falls Furthest", size=48, color=GOLD, font=TITLE_FONT).move_to([0.0, 3.25, 0])
        tag = _tag(MODEL_TAG)

        self.add(rig, bars, q_txt, tag)
        self.play(
            swap(q_txt, title, run_time=0.8),
            f_tr.animate(run_time=1.2).set_value(100.0),
            p_tr.animate(run_time=1.2).set_value(3.8),
        )
        self.finish()


class S02Fatigue(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        F0_tr = ValueTracker(100.0)
        a_tr = ValueTracker(25.0)
        b_tr = ValueTracker(0.100)

        f_tr = ValueTracker(100.0)
        p_tr = ValueTracker(3.8)
        rig = build_muscle_rig(center=(-3.8, 0.25, 0), scale=1.0, phase_tracker=lift_phase)
        start_lift_updater(rig, freq=0.50)
        old_bars = build_bars(f_tr, p_tr, x_force=1.20, x_power=4.55, y_base=-2.1, max_h=3.6, bar_w=1.20)
        old_title = T("Power Falls Furthest", size=48, color=GOLD, font=TITLE_FONT).move_to([0.0, 3.25, 0])
        tag = _tag(MODEL_TAG)

        icon = build_muscle_rig(center=(0.0, 2.55, 0), scale=0.36, phase_tracker=lift_phase, label_inside=False)
        start_lift_updater(icon, freq=0.50)
        Pv, Pp, v_live, p_live, _ = build_two_plots(F0_tr, a_tr, b_tr)

        self.add(rig, old_bars, old_title, tag)
        self.play(
            FadeOut(old_title),
            FadeOut(old_bars),
            FadeOut(rig),
            FadeIn(icon),
            run_time=0.5,
        )
        self.play(Create(Pv), Create(Pp), run_time=0.8)

        x_draw = ValueTracker(0.0)
        v_grow = Pv.live_curve(lambda x: hill_v(x, 100, 25, 0.100), x_draw, color=YELLOW, width=7)
        p_grow = Pp.live_curve(lambda x: hill_p(x, 100, 25, 0.100), x_draw, color=GREEN, width=7)
        self.add(v_grow, p_grow)
        self.play(x_draw.animate.set_value(100.0), run_time=2.0, rate_func=linear)
        self.remove(v_grow, p_grow)
        self.add(v_live, p_live)

        self.at("recovers with rest")
        rest_tag = T("recovers with rest", size=28, color=GOLD).move_to([3.3, 2.75, 0])
        self.play(FadeIn(rest_tag, shift=LEFT * 0.15), run_time=0.6)

        self.at("the ceiling")
        self.play(FadeOut(rest_tag), run_time=0.3)
        h_ceil = T("ceiling", size=28, color=GOLD).move_to(Pv.pt(88, 0.08))
        self.play(FadeIn(h_ceil), run_time=0.3)
        self.play(F0_tr.animate.set_value(84.0), rate_func=there_and_back, run_time=1.8)

        self.at("top speed")
        h_vmax = T("top speed", size=28, color=GOLD).move_to(Pv.pt(26, 0.40))
        self.play(FadeIn(h_vmax), run_time=0.3)
        self.play(b_tr.animate.set_value(0.082), rate_func=there_and_back, run_time=1.8)

        self.at("sags more")
        h_sag = T("sag", size=28, color=GOLD).move_to(Pv.pt(48, 0.19))
        self.play(FadeIn(h_sag), run_time=0.3)
        sag_t = ValueTracker(0.25)

        def _sag_bob(mob, dt):
            q = sag_t.get_value()
            a_tr.set_value(100.0 * q)
            b_tr.set_value(0.40 * q)

        sag_t.add_updater(_sag_bob)
        self.add(sag_t)
        self.play(sag_t.animate.set_value(0.14), rate_func=there_and_back, run_time=1.2)
        sag_t.clear_updaters()
        a_tr.set_value(25.0)
        b_tr.set_value(0.100)
        self.finish()


class S03Ceiling(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        F0_tr = ValueTracker(100.0)
        a_tr = ValueTracker(25.0)
        b_tr = ValueTracker(0.100)

        icon = build_muscle_rig(center=(0.0, 2.55, 0), scale=0.36, phase_tracker=lift_phase, label_inside=False)
        start_lift_updater(icon, freq=0.50)
        Pv, Pp, v_live, p_live, ghosts = build_two_plots(F0_tr, a_tr, b_tr, with_ghosts=True)
        tag = _tag(MODEL_TAG)

        self.add(icon, Pv, Pp, v_live, p_live, tag)

        self.at("peak power starts")
        pk_lbl = M("3.8 W", size=28, color=GREEN).move_to(Pp.pt(45, 4.18))
        self.play(FadeIn(ghosts), FadeIn(pk_lbl), run_time=0.7)

        self.at("cut the ceiling")
        ceil_tag = T("ceiling -20%", size=28, color=ORANGE).move_to(Pv.pt(75, 0.25))
        self.play(
            F0_tr.animate.set_value(80.0),
            a_tr.animate.set_value(20.0),
            FadeIn(ceil_tag),
            run_time=3.2,
        )

        self.at("peak power falls")
        # Place cleanly inside the open green arch (F=30, P=1.2..2.0) completely clear of both curves
        new_pk_lbl = M("3.1 W", size=28, color=GREEN).move_to(Pp.pt(30, 1.85))
        pct_tag = M("-20%", size=28, color=GREEN).move_to(Pp.pt(30, 1.15))
        self.play(swap(pk_lbl, new_pk_lbl, run_time=0.6), FadeIn(pct_tag), run_time=0.8)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        F0_tr = ValueTracker(80.0)
        a_tr = ValueTracker(20.0)
        b_tr = ValueTracker(0.100)
        p_F0 = ValueTracker(80.0)
        p_a = ValueTracker(20.0)
        p_b = ValueTracker(0.100)
        pop_tr = ValueTracker(1.0)

        icon = build_muscle_rig(center=(0.0, 2.55, 0), scale=0.36, phase_tracker=lift_phase, label_inside=False)
        start_lift_updater(icon, freq=0.50)
        Pv, Pp, v_live, p_live, ghosts = build_two_plots(
            F0_tr, a_tr, b_tr, p_F0, p_a, p_b, power_opacity_tr=pop_tr, with_ghosts=True
        )
        ceil_tag = T("ceiling -20%", size=28, color=ORANGE).move_to(Pv.pt(75, 0.25))
        pk_lbl = M("3.1 W", size=28, color=GREEN).move_to(Pp.pt(30, 1.85))
        pct_tag = M("-20%", size=28, color=GREEN).move_to(Pp.pt(30, 1.15))
        tag = _tag(MODEL_TAG)

        self.add(icon, Pv, Pp, ghosts, v_live, p_live, ceil_tag, pk_lbl, pct_tag, tag)

        self.at("top speed fall")
        vmax_tag = T("top speed -20%", size=28, color=YELLOW).move_to(Pv.pt(42, 0.36))
        self.play(
            b_tr.animate.set_value(0.080),
            pop_tr.animate.set_value(0.45),
            FadeIn(vmax_tag),
            run_time=2.4,
        )

        self.at("two cuts")
        # Move icon left & slightly up cleanly before question card appears so there is zero overlap
        self.play(
            FadeOut(pk_lbl),
            FadeOut(pct_tag),
            icon.cx_tr.animate.set_value(-5.1),
            icon.cy_tr.animate.set_value(2.98),
            run_time=0.7,
        )
        self.play(Indicate(ceil_tag, color=ORANGE), Indicate(vmax_tag, color=YELLOW), run_time=1.1)

        self.at("does peak power")
        q_card = question_card("Power down 40%?", y=3.15, size=34)
        self.play(FadeIn(q_card), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Power down 40%?"
    CARD = {"y": 3.15, "size": 34}
    RING_AT = (5.6, 3.1, 0)
    SECONDS = 4.5

    def backdrop(self):
        lift_phase = ValueTracker(0.0)
        F0_tr = ValueTracker(80.0)
        a_tr = ValueTracker(20.0)
        b_tr = ValueTracker(0.080)
        p_F0 = ValueTracker(80.0)
        p_a = ValueTracker(20.0)
        p_b = ValueTracker(0.100)
        pop_tr = ValueTracker(0.45)

        icon = build_muscle_rig(center=(-5.1, 2.98, 0), scale=0.36, phase_tracker=lift_phase, label_inside=False)
        start_lift_updater(icon, freq=0.50)
        Pv, Pp, v_live, p_live, ghosts = build_two_plots(
            F0_tr, a_tr, b_tr, p_F0, p_a, p_b, power_opacity_tr=pop_tr, with_ghosts=True
        )
        ceil_tag = T("ceiling -20%", size=28, color=ORANGE).move_to(Pv.pt(75, 0.25))
        vmax_tag = T("top speed -20%", size=28, color=YELLOW).move_to(Pv.pt(42, 0.36))
        tag = _tag(MODEL_TAG)
        return VGroup(icon, Pv, Pp, ghosts, v_live, p_live, ceil_tag, vmax_tag, tag)


class S06Answer(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        F0_tr = ValueTracker(80.0)
        a_tr = ValueTracker(20.0)
        b_tr = ValueTracker(0.080)
        p_F0 = ValueTracker(80.0)
        p_a = ValueTracker(20.0)
        p_b = ValueTracker(0.100)
        pop_tr = ValueTracker(0.45)

        icon = build_muscle_rig(center=(-5.1, 2.98, 0), scale=0.36, phase_tracker=lift_phase, label_inside=False)
        start_lift_updater(icon, freq=0.50)
        Pv, Pp, v_live, p_live, ghosts = build_two_plots(
            F0_tr, a_tr, b_tr, p_F0, p_a, p_b, power_opacity_tr=pop_tr, with_ghosts=True
        )
        ceil_tag = T("ceiling -20%", size=28, color=ORANGE).move_to(Pv.pt(75, 0.25))
        vmax_tag = T("top speed -20%", size=28, color=YELLOW).move_to(Pv.pt(42, 0.36))
        q_card = question_card("Power down 40%?", y=3.15, size=34)
        tag = _tag(MODEL_TAG)

        self.add(icon, Pv, Pp, ghosts, v_live, p_live, ceil_tag, vmax_tag, q_card, tag)
        self.play(FadeOut(q_card), run_time=0.5)
        self.play(
            icon.cx_tr.animate.set_value(0.0),
            icon.cy_tr.animate.set_value(2.55),
            run_time=0.7,
        )

        self.at("force times speed")
        f_chip = M("0.8", size=34, color=ORANGE).move_to([2.1, 2.95, 0])
        times_s = M("×", size=34, color=TEXT).move_to([2.8, 2.95, 0])
        v_chip = M("0.8", size=34, color=YELLOW).move_to([3.5, 2.95, 0])
        self.play(FadeIn(f_chip), FadeIn(times_s), FadeIn(v_chip), run_time=0.8)

        self.at("two cuts multiply")
        self.play(Indicate(VGroup(f_chip, times_s, v_chip), color=GOLD), run_time=0.9)

        self.at("8 is")
        eq_res = M("= 0.64", size=34, color=GREEN).next_to(v_chip, RIGHT, buff=0.22)
        self.play(FadeIn(eq_res, shift=LEFT * 0.15), run_time=0.7)

        self.at("peak power falls")
        pk_lbl = M("2.4 W", size=28, color=GREEN).move_to(Pp.pt(30, 1.45))
        pct_tag = M("-36%", size=28, color=GREEN).move_to(Pp.pt(30, 0.78))
        self.play(
            pop_tr.animate.set_value(1.0),
            p_b.animate.set_value(0.080),
            run_time=2.1,
        )
        self.play(FadeIn(pk_lbl), FadeIn(pct_tag), run_time=0.6)
        self.finish()


class S07Sag(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        F0_tr = ValueTracker(80.0)
        a_tr = ValueTracker(20.0)
        b_tr = ValueTracker(0.080)

        icon = build_muscle_rig(center=(0.0, 2.55, 0), scale=0.36, phase_tracker=lift_phase, label_inside=False)
        start_lift_updater(icon, freq=0.50)
        Pv, Pp, v_live, p_live, ghosts = build_two_plots(F0_tr, a_tr, b_tr, with_ghosts=True)
        ceil_tag = T("ceiling -20%", size=28, color=ORANGE).move_to(Pv.pt(75, 0.25))
        vmax_tag = T("top speed -20%", size=28, color=YELLOW).move_to(Pv.pt(42, 0.36))
        pk_lbl = M("2.4 W", size=28, color=GREEN).move_to(Pp.pt(30, 1.45))
        pct_tag = M("-36%", size=28, color=GREEN).move_to(Pp.pt(30, 0.78))
        tag = _tag(MODEL_TAG)

        self.add(icon, Pv, Pp, ghosts, v_live, p_live, ceil_tag, vmax_tag, pk_lbl, pct_tag, tag)

        self.at("sag more")
        # Clear 2.4 W / -36% as the curve starts sagging so it never sits over the shrinking hump
        sag_tag = T("more sag", size=28, color=YELLOW).move_to(Pv.pt(46, 0.145))
        self.play(FadeOut(pk_lbl), FadeOut(pct_tag), run_time=0.35)
        self.play(
            a_tr.animate.set_value(12.0),
            b_tr.animate.set_value(0.048),
            FadeIn(sag_tag),
            run_time=2.2,
        )

        self.at("peak power falls")
        # 1.8 W inside arch at (26, 0.85); -53% cleanly in gap at (50, 2.55)
        new_pk = M("1.8 W", size=28, color=GREEN).move_to(Pp.pt(26, 0.85))
        new_pct = M("-53%", size=28, color=GREEN).move_to(Pp.pt(50, 2.55))
        self.play(FadeIn(new_pk), FadeIn(new_pct), run_time=0.6)

        self.at("in all")
        fb0, pb0 = hill_peak(100.0, 25.0, 0.100)
        fb3, pb3 = hill_peak(80.0, 12.0, 0.048)
        top_y = Pp.pt(fb0, pb0)[1]
        bot_y = Pp.pt(fb3, pb3)[1]
        bx = Pp.pt(fb0, pb0)[0] + 0.05
        drop_bracket = VGroup(
            Line([bx, top_y, 0], [bx + 0.16, top_y, 0], color=GREEN, stroke_width=3.5),
            Line([bx + 0.16, top_y, 0], [bx + 0.16, bot_y, 0], color=GREEN, stroke_width=3.5),
            Line([bx, bot_y, 0], [bx + 0.16, bot_y, 0], color=GREEN, stroke_width=3.5),
        )
        self.play(Create(drop_bracket), Indicate(ceil_tag, color=ORANGE), run_time=1.3)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        F0_tr = ValueTracker(80.0)
        a_tr = ValueTracker(12.0)
        b_tr = ValueTracker(0.048)
        f_bar = ValueTracker(80.0)
        p_bar = ValueTracker(1.8)

        icon = build_muscle_rig(center=(0.0, 2.80, 0), scale=0.33, phase_tracker=lift_phase, label_inside=False)
        start_lift_updater(icon, freq=0.50)
        Pv, Pp, v_live, p_live, ghosts = build_two_plots(
            F0_tr,
            a_tr,
            b_tr,
            left_box=(-6.2, -2.35, -1.80, 1.45),
            right_box=(2.60, 6.25, -1.80, 1.45),
            with_ghosts=True,
            xticks=(0, 50, 100),
        )
        ghosts[2].move_to(Pp.pt(82, 3.05))

        bars = build_bars(
            f_bar,
            p_bar,
            x_force=-0.95,
            x_power=1.20,
            y_base=-1.80,
            max_h=3.15,
            bar_w=1.28,
            show_ghost_outline=True,
            two_line_labels=True,
        )
        tag = _tag(MODEL_TAG)

        self.add(icon, Pv, Pp, ghosts, v_live, p_live, tag)
        self.play(FadeIn(bars), run_time=0.9)

        self.at("the ceiling")
        c_ring = Circle(radius=0.22, color=GOLD, stroke_width=6).move_to(Pv.pt(80, 0))
        self.play(Create(c_ring), run_time=0.5)

        self.at("top speed")
        v_ring = Circle(radius=0.22, color=GOLD, stroke_width=6).move_to(Pv.pt(0, 0.32))
        self.play(Create(v_ring), run_time=0.5)

        self.at("shape too")
        s_ring = Circle(radius=0.22, color=GOLD, stroke_width=6).move_to(Pv.pt(28, hill_v(28, 80, 12, 0.048)))
        s_arc = Pv.curve(lambda x: hill_v(x, 80, 12, 0.048), x0=10, x1=52, color=GOLD, width=8)
        self.play(Create(s_arc), Create(s_ring), run_time=0.6)

        self.at("all of them")
        p_target = np.array([1.20, -1.80 + 3.15 * (1.8 / 4.0) / 2, 0])
        rays = VGroup(*[
            CurvedArrow(r.get_center(), p_target, angle=-0.22, color=GOLD, stroke_width=3, tip_length=0.15)
            for r in (v_ring, s_ring, c_ring)
        ])
        rays.layout_ok = "covered"  # connecting rays intentionally bridge from plots into the green bar
        self.play(Create(rays), run_time=0.85)

        self.at("further than force")
        rule_lbl = T("power pays for each loss", size=28, color=GOLD).move_to([-0.7, -3.10, 0])
        self.play(FadeIn(rule_lbl), Indicate(bars.power_grp, color=GOLD, scale_factor=1.06), run_time=0.9)
        self.finish()


class S09Suspects(SpokenScene):
    def construct(self):
        P_in = Plot(
            box=(-6.15, -3.55, 1.95, 3.35),
            xr=(0, 100),
            yr=(0, 4.2),
            color=GREY,
            stroke=2,
        )
        in_fresh = P_in.curve(lambda x: hill_p(x, 100, 25, 0.100), x0=0, x1=100, color=GREEN, width=3, opacity=0.35)
        in_fat = P_in.curve(lambda x: hill_p(x, 80, 12, 0.048), x0=0, x1=80, color=GREEN, width=4)
        in_lbl = T("power loss", size=24, color=GREEN).next_to(P_in, DOWN, buff=0.10)
        inset = VGroup(P_in, in_fresh, in_fat, in_lbl)

        sac = RoundedRectangle(
            corner_radius=0.3,
            width=7.4,
            height=1.1,
            stroke_color=CYAN,
            stroke_width=4,
            fill_color=CYAN,
            fill_opacity=0.22,
        ).move_to([1.5, 2.65, 0])
        sac_lbl = T("calcium store", size=28, color=CYAN).move_to(sac)

        actin = RoundedRectangle(
            corner_radius=0.1,
            width=8.2,
            height=0.34,
            stroke_color=GREY,
            stroke_width=3.5,
            fill_color=GREY,
            fill_opacity=0.45,
        ).move_to([1.5, 0.50, 0])
        actin_lbl = T("actin", size=28, color=TEXT).next_to(actin, UP, buff=0.14).align_to(actin, RIGHT)

        thick = RoundedRectangle(
            corner_radius=0.12,
            width=8.2,
            height=0.52,
            stroke_color=GREY,
            stroke_width=3.5,
            fill_color=GREY,
            fill_opacity=0.45,
        ).move_to([1.5, -1.80, 0])
        thick_lbl = T("myosin", size=28, color=BLUE).next_to(thick, DOWN, buff=0.14)

        head_phase = ValueTracker(0.0)
        # 6 evenly spaced heads: -1.80, -0.48, +0.84, +2.16, +3.48, +4.80 (gap centers: -1.14, 0.18, 1.50, 2.82, 4.14)
        head_xs = np.linspace(-1.80, 4.80, 6)

        def _heads():
            ph = head_phase.get_value()
            g = VGroup()
            for idx, hx in enumerate(head_xs):
                ang = 0.14 * np.sin(ph + idx * 0.85)
                base = np.array([hx, -1.54, 0])
                tip = base + np.array([np.sin(ang) * 0.55, 1.50, 0])
                g.add(Line(base, tip, color=BLUE, stroke_width=6))
                g.add(Dot(tip, radius=0.20, color=BLUE, stroke_color=TEXT, stroke_width=2))
            return g

        head_phase.add_updater(lambda m, dt: m.set_value(m.get_value() + 2.2 * dt))

        ca_rate = ValueTracker(1.0)
        rng = np.random.default_rng(7)
        ca_xs = rng.uniform(-1.6, 4.4, 14)
        ca_ys = rng.uniform(0.75, 2.05, 14)
        ca_t = ValueTracker(0.0)
        ca_t.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))

        def _ca_stream():
            t = ca_t.get_value()
            n_show = max(3, int(round(14 * ca_rate.get_value())))
            g = VGroup()
            for i in range(n_show):
                y = 2.05 - ((2.05 - ca_ys[i] + t * 0.85) % 1.30)
                g.add(Dot([ca_xs[i], y, 0], radius=0.08, color=CYAN))
            return g

        tag = _tag("schematic")
        heads_mob = always_redraw(_heads)
        ca_mob = always_redraw(_ca_stream)
        self.add(head_phase, ca_t, inset, sac, sac_lbl, actin, actin_lbl, thick, thick_lbl, heads_mob, ca_mob, tag)
        self.wait(0.8)

        self.at("lactic acid")
        lac = boxed_label("lactate", color=GREY, size=26, fill_opacity=0.24).move_to([-4.6, -0.35, 0])
        lac.label.set_color(TEXT)
        self.play(FadeIn(lac, shift=RIGHT * 0.5), run_time=0.9)

        self.at("away from the lactate")
        cross = VGroup(
            Line(lac.get_corner(DL) + UR * 0.08, lac.get_corner(UR) + DL * 0.08, color=RED, stroke_width=5),
            Line(lac.get_corner(UL) + DR * 0.08, lac.get_corner(DR) + UL * 0.08, color=RED, stroke_width=5),
        )
        cross.layout_ok = True  # deliberate RED strike-through across lactate token
        self.play(Create(cross), run_time=0.5)
        self.play(
            lac.box.animate.move_to([-4.8, -2.55, 0]).set_opacity(0.45),
            lac.label.animate.move_to([-4.8, -2.55, 0]).set_opacity(0.75),
            cross.animate.move_to([-4.8, -2.55, 0]).set_opacity(0.75),
            run_time=1.0,
        )

        self.at("inorganic phosphate")
        # Strictly inside gaps between stems (-1.14, 0.18, 1.50, 2.82, 4.14), y=-0.45, radius=0.33
        pi_coords = [(-1.14, -0.45), (0.18, -0.45), (1.50, -0.45), (2.82, -0.45), (4.14, -0.45)]
        pi_toks = VGroup(*[
            VGroup(
                Circle(radius=0.33, color=MAGENTA, stroke_width=3, fill_color=MAGENTA, fill_opacity=0.26),
                M("Pi", size=24, color=MAGENTA),
            ).move_to([x, y, 0])
            for x, y in pi_coords
        ])
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in pi_toks], lag_ratio=0.10), run_time=1.1)

        self.at("failing calcium release")
        self.play(ca_rate.animate.set_value(0.22), run_time=1.3)

        self.at("protons count")
        # Strictly inside gaps (-1.14, 1.50) at y=-1.15, radius=0.32
        h_coords = [(-1.14, -1.15), (1.50, -1.15)]
        h_toks = VGroup(*[
            VGroup(
                Circle(radius=0.32, color=WHITE, stroke_width=2.5, fill_color=WHITE, fill_opacity=0.18),
                M("H+", size=22, color=WHITE),
            ).move_to([x, y, 0])
            for x, y in h_coords
        ])
        temp_tag = T("smaller near body temperature", size=26, color=TEXT).move_to([1.5, -2.95, 0])
        self.play(FadeIn(h_toks), FadeIn(temp_tag), run_time=1.1)

        self.at("still debated")
        q_pi = T("?", size=34, color=GOLD).move_to([-2.85, -0.45, 0])
        q_ca = T("?", size=34, color=GOLD).next_to(sac, RIGHT, buff=0.24)
        q_h = T("?", size=34, color=GOLD).move_to([2.82, -1.15, 0])
        self.play(FadeIn(q_pi), FadeIn(q_ca), FadeIn(q_h), run_time=0.8)
        self.finish()


class S10Motor(SpokenScene):
    def construct(self):
        platform = RoundedRectangle(
            corner_radius=0.12,
            width=4.4,
            height=0.45,
            stroke_color=GREY,
            stroke_width=3.5,
            fill_color=GREY,
            fill_opacity=0.45,
        ).move_to([-3.0, -2.05, 0])
        actin = RoundedRectangle(
            corner_radius=0.08,
            width=4.6,
            height=0.24,
            stroke_color=GREY,
            stroke_width=3,
            fill_color=GREY,
            fill_opacity=0.45,
        ).move_to([-2.7, -0.05, 0])
        bead_base = np.array([-5.1, -0.05, 0])
        beam_cone = Polygon(
            [-5.65, 2.35, 0],
            [-4.55, 2.35, 0],
            [-4.85, -0.25, 0],
            [-5.35, -0.25, 0],
            stroke_color=TEAL,
            stroke_width=2.5,
            fill_color=TEAL,
            fill_opacity=0.22,
        )
        trap_lbl = T("laser trap", size=28, color=TEAL).next_to(beam_cone, UP, buff=0.14)
        no_lac_tag = T("no lactate", size=28, color=TEXT).move_to([-2.0, 2.75, 0])
        tag = _tag("schematic")

        trace_ax = Plot(
            box=(0.75, 6.15, -2.05, 1.95),
            xr=(0, 10),
            yr=(0, 1.2),
            xlabel="time",
            ylabel="force (schematic)",
            color=GREY,
            size=22,
            label_size=26,
        )
        trace_ax.ylabel.set_color(ORANGE)
        if trace_ax.xlabel:
            trace_ax.xlabel.set_color(TEXT)

        amp_tr = ValueTracker(1.0)
        cap_tr = ValueTracker(1.2)
        dur_tr = ValueTracker(1.0)
        sim_t = ValueTracker(0.0)
        sim_t.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))
        self.add(sim_t)

        heights = [1.0, 0.56, 0.92, 0.48, 0.86, 0.52]

        def _trace_force(tau):
            period = 1.45
            idx = int(np.floor(tau / period))
            u = (tau % period) / period
            w = 0.42 * dur_tr.get_value()
            raw_h = heights[idx % len(heights)]
            h = min(raw_h * amp_tr.get_value(), cap_tr.get_value())
            if 0.0 < u < w:
                return max(0.04, h * np.sin(PI * u / w) ** 0.7)
            return 0.04

        def _trap_live():
            t = sim_t.get_value()
            f_now = _trace_force(t)
            dx = 0.28 * f_now
            bead = Dot(bead_base + RIGHT * dx, radius=0.26, color=TEAL, stroke_color=TEXT, stroke_width=2.5)
            heads = VGroup()
            for j, hx in enumerate([-3.9, -2.9, -1.9]):
                ang = (0.32 * f_now) if (j % 2 == 0 or f_now > 0.45) else -0.12
                base = np.array([hx, -1.82, 0])
                tip = base + np.array([np.sin(ang) * 0.75, 1.55, 0])
                heads.add(Line(base, tip, color=BLUE, stroke_width=6))
                heads.add(Dot(tip, radius=0.18, color=BLUE, stroke_color=TEXT, stroke_width=2))
            pts = []
            for k in range(240):
                s = k / 239.0 * 10.0
                val = _trace_force(max(0.0, t - (10.0 - s) * 0.55))
                pts.append(trace_ax.pt(s, val))
            crv = VMobject(stroke_color=ORANGE, stroke_width=5, fill_opacity=0)
            crv.set_points_as_corners(pts)
            return VGroup(bead, heads, crv)

        self.add(platform, actin, beam_cone, trap_lbl, trace_ax, tag, always_redraw(_trap_live))
        self.wait(0.8)

        self.at("laser trap")
        self.play(Indicate(trap_lbl, color=TEAL), run_time=0.8)

        self.at("no lactate")
        self.play(FadeIn(no_lac_tag), run_time=0.6)

        self.at("acid cut")
        # Place in gaps between heads (-3.9, -2.9, -1.9) with r=0.31 circles
        h_toks = VGroup(*[
            VGroup(
                Circle(radius=0.31, color=WHITE, stroke_width=2.5, fill_color=WHITE, fill_opacity=0.18),
                M("H+", size=22, color=WHITE),
            ).move_to([x, y, 0])
            for x, y in [(-3.4, -1.32), (-2.4, -1.32), (-1.3, -1.32)]
        ])
        avg_line = DashedLine(trace_ax.pt(0, 0.72), trace_ax.pt(10, 0.72), color=GOLD, stroke_width=3)
        acid_tag = T("about -20%", size=28, color=ORANGE).move_to([5.1, 2.25, 0])
        self.play(
            FadeIn(h_toks),
            Create(avg_line),
            FadeIn(acid_tag),
            amp_tr.animate.set_value(0.80),
            avg_line.animate.shift(DOWN * (trace_ax.pt(0, 0.72)[1] - trace_ax.pt(0, 0.56)[1])),
            run_time=1.6,
        )

        self.at("phosphate")
        pi_toks = VGroup(*[
            VGroup(
                Circle(radius=0.31, color=MAGENTA, stroke_width=3, fill_color=MAGENTA, fill_opacity=0.26),
                M("Pi", size=22, color=MAGENTA),
            ).move_to([x, y, 0])
            for x, y in [(-4.4, -0.75), (-3.4, -0.62), (-2.4, -0.62)]
        ])
        pi_tag = T("strongest pulls gone", size=28, color=MAGENTA).move_to([3.6, 3.05, 0])
        self.play(
            FadeIn(pi_toks),
            FadeIn(pi_tag),
            cap_tr.animate.set_value(0.50),
            run_time=1.4,
        )

        self.at("let go sooner")
        self.play(dur_tr.animate.set_value(0.38), run_time=0.9)
        self.finish()


class S11Rats(SpokenScene):
    def construct(self):
        head_phase = ValueTracker(0.0)
        head_phase.add_updater(lambda m, dt: m.set_value(m.get_value() + 1.8 * dt))
        self.add(head_phase)

        fibre = build_compact_fibre(center=(-3.85, 0.1, 0), scale=0.72, head_phase=head_phase, show_tokens=True)
        tag = _tag("schematic")
        t_rat = ValueTracker(0.0)

        def _force_norm(u):
            return 0.90 if u < 0.45 else max(0.22, 0.90 - 1.35 * (u - 0.45))

        def _pi_norm(u):
            return min(0.95, 0.15 + 0.85 * u)

        def _h_norm(u):
            return min(0.90, 0.10 + 0.82 * u)

        def _force_fast(u):
            return 0.90 if u < 0.45 else max(0.10, 0.90 - 1.65 * (u - 0.45))

        # Top right: 3 vertical meters + time strip (no xlabel on top strip so 'association, not cause' sits cleanly)
        P_top = Plot(box=(0.45, 5.95, 0.45, 2.10), xr=(0, 1), yr=(0, 1.05), color=GREY, size=22)
        bp_line = DashedLine(P_top.pt(0, 0.53), P_top.pt(1, 0.53), color=MAGENTA, stroke_width=2.5)
        bp_lbl = T("breakpoint", size=22, color=MAGENTA).next_to(P_top.pt(0.02, 0.53), UP, buff=0.08).align_to(P_top.pt(0.02, 0.53), LEFT)

        top_pi = P_top.live_curve(_pi_norm, t_rat, color=MAGENTA, width=5)
        top_h = P_top.live_curve(_h_norm, t_rat, color=WHITE, width=4)
        top_f = P_top.live_curve(_force_norm, t_rat, color=ORANGE, width=6)

        def _meters():
            u = t_rat.get_value()
            specs = [
                (1.15, _force_norm(u), ORANGE, "twitch force"),
                (3.20, _pi_norm(u), MAGENTA, "phosphate"),
                (5.25, _h_norm(u), WHITE, "protons"),
            ]
            g = VGroup()
            for mx, val, col, name in specs:
                bg = Rectangle(width=0.56, height=0.82, stroke_color=col, stroke_width=2.5).move_to([mx, 2.70, 0])
                fill_h = max(0.03, 0.82 * val)
                fg = Rectangle(
                    width=0.56,
                    height=fill_h,
                    stroke_width=0,
                    fill_color=col,
                    fill_opacity=0.55,
                ).move_to([mx, bg.get_bottom()[1] + fill_h / 2, 0])
                lbl = T(name, size=22, color=col).next_to(bg, UP, buff=0.08)
                g.add(bg, fg, lbl)
            return g

        P_bot = Plot(box=(0.45, 5.95, -2.35, -0.75), xr=(0, 1), yr=(0, 1.05), xlabel="time", color=GREY, size=22, label_size=24)
        P_bot.xlabel.set_color(TEXT)
        bot_tag = T("faster stimulation", size=24, color=TEXT).next_to(P_bot, DOWN, buff=0.14).align_to(P_bot, LEFT)
        dim = lambda c: interpolate_color(ManimColor(c), ManimColor(BG), 0.35)
        bot_pi = P_bot.live_curve(_pi_norm, t_rat, color=dim(MAGENTA), width=4)
        bot_h = P_bot.live_curve(_h_norm, t_rat, color=dim(WHITE), width=3.5)
        bot_f = P_bot.live_curve(_force_fast, t_rat, color=dim(ORANGE), width=5)

        self.add(
            fibre,
            P_top,
            bp_line,
            bp_lbl,
            P_bot,
            bot_tag,
            tag,
            top_pi,
            top_h,
            top_f,
            bot_pi,
            bot_h,
            bot_f,
            always_redraw(_meters),
        )
        self.wait(0.6)

        self.at("twitch force")
        self.play(t_rat.animate.set_value(1.0), run_time=4.4, rate_func=linear)

        self.at("association")
        assoc = T("association, not cause", size=30, color=GOLD).move_to([3.2, -0.15, 0])
        self.play(FadeIn(assoc, shift=UP * 0.1), run_time=0.7)

        self.at("still open")
        qs = VGroup(
            T("?", size=30, color=GOLD).next_to(fibre.sac, RIGHT, buff=0.16),
            T("?", size=30, color=GOLD).move_to([-6.10, -0.05, 0]),
            T("?", size=30, color=GOLD).move_to([-1.50, -0.75, 0]),
        )
        self.play(FadeIn(qs), run_time=0.7)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        lift_phase = ValueTracker(0.0)
        f_tr = ValueTracker(80.0)
        p_tr = ValueTracker(1.8)
        v_tr = ValueTracker(0.32)

        rig = build_muscle_rig(center=(-3.85, 0.25, 0), scale=1.0, phase_tracker=lift_phase)
        start_lift_updater(rig, freq=0.50)
        bars = build_bars(
            f_tr,
            p_tr,
            x_force=0.20,
            x_power=5.15,
            y_base=-2.05,
            max_h=3.05,
            bar_w=1.28,
            show_ghost_outline=True,
            v_tr=v_tr,
            x_speed=2.68,
            two_line_labels=True,
            speed_bar_w=1.95,
        )
        bars.speed_grp.set_opacity(0.0)

        # Small YELLOW "more sag" curve badge well above the speed bar's readout
        sag_ax = Plot(box=(2.03, 3.33, 1.85, 2.75), xr=(0, 80), yr=(0, 0.35), color=GREY, stroke=2)
        sag_crv = sag_ax.curve(lambda x: hill_v(x, 80, 12, 0.048), x0=0, x1=80, color=YELLOW, width=4)
        sag_lbl = T("more sag", size=24, color=YELLOW).next_to(sag_ax, UP, buff=0.10)
        sag_badge = VGroup(sag_ax, sag_crv, sag_lbl)

        tag = _tag(MODEL_TAG)
        self.add(rig, bars.force_grp, bars.power_grp, bars[0], tag)
        self.wait(0.6)

        self.at("still held")
        self.play(Indicate(bars.force_grp, color=ORANGE, scale_factor=1.06), run_time=1.1)

        self.at("more than half")
        self.play(Indicate(bars.power_grp, color=GREEN, scale_factor=1.06), run_time=1.1)

        self.at("force times speed")
        bars.speed_grp.set_opacity(1.0)
        self.play(FadeIn(bars.speed_grp), FadeIn(sag_badge), run_time=0.8)

        self.at("every loss at once")
        self.play(
            Indicate(bars.force_grp, color=GOLD, scale_factor=1.06),
            Indicate(bars.speed_grp, color=GOLD, scale_factor=1.06),
            Indicate(sag_badge, color=GOLD, scale_factor=1.06),
            Indicate(bars.power_grp, color=GREEN, scale_factor=1.06),
            run_time=1.3,
        )
        self.finish()


class S13End(EndCard):
    LINE = "Fatigue lowers force and often speed, so power suffers most."
