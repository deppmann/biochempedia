"""
Holding On: The Latch — Smooth Muscle and the Myogenic Response (Chapter 2)

COLOUR MAP (one colour per concept, kept across the entire film):
- YELLOW (#F5D547): calcium (calcium chip / stimulation signal)
- GREEN  (#83C167): myosin light-chain kinase (MLCK)
- RED    (#FC6255): myosin light-chain phosphatase (MLCP)
- GOLD   (#D4A843): phosphate badge ('P' on LC20), phosphorylation trace, dephosphorylation midpoint
- BLUE   (#58C4DD): myosin heads (free or phosphorylated cycling), thick filament, force trace/bars, ATP use meter
- GREY   (#8B93A1): actin filament, purified myosin surface, axes, scope tags
- MAGENTA (#EE66CC): latch bridge (attached myosin head without a phosphate) and latch-held force
- TEXT   (#E8EAF0): narration-synced headings, question cards, trapped bead

ONE WORLD CARRIED ALL FILM:
Top 55% of frame: GREY actin filament spanning the width above a BLUE thick filament carrying six
articulated BLUE myosin heads (replaced by three heads on a GREY surface + bead/laser trap in s07-s10).
Bottom-left: the shrunk seesaw (GREEN MLCK kinase vs RED MLCP phosphatase, YELLOW calcium above kinase).
Bottom-right: the time plot (GOLD phosphorylation, BLUE force) that morphs into model bars (s05) and
the Hammell et al. timeline (s07-s10).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Seesaw tips kinase-down, 4 heads get GOLD P badges and stroke actin, Hai-Murphy ODE traces (p and force) climb; then calcium stays lit while kinase drops, P drops to ~25% of peak as 3 heads lose P yet stay attached on a flat force plateau while 1 P-head keeps cycling.
- s02_four_states: Dashed BLUE ghost curve slides down along the computed GOLD trace; 4 heads step into a 2x2 grid of the 4 Hai-Murphy states while GREEN/RED arrows add/remove GOLD P badges on both detached and attached heads.
- s03_latch_bridge: Seesaw rocks and badge count follows; one attached head loses its P badge to RED phosphatase, turns MAGENTA ("latch bridge"), holds while a clock ticks slowly and a neighbouring BLUE head cycles twice before it releases once.
- s04_one_idea: Full Hai-Murphy ODE replay in one sweep; attached heads losing P turn MAGENTA, "cycling" counter drops 4 -> 1, and schematic "ATP use" meter drops while force stays high.
- s05_model_numbers: Computed steady-state Hai-Murphy bars (k2=0.5, k3=0.4, k4=0.1, k7=0.01 /s): 67% P (4/6 heads, force=1.00) vs 17% P (1/6 heads, force=0.858 ~ 86%, 82% MAGENTA latch share); top wobbles between computed k7=0.02 (0.748) and k7=0.005 (0.929) bounds while 1 P-head cycles.
- s06_economy: In the head row, 1 P-head cycles continuously while MAGENTA latch heads turn over one by one; a rigid GREY rigor panel ("rigor: no ATP") receives a RED cross and fades; "ATP use" meter holds low but nonzero.
- s07_trap: 3 detached heads on purified myosin attach and pull actin + white bead into laser trap cone while force rises to plateau; RED phosphatase drops in; timeline draws scaled bars at 32 s (tonic) and 21 s (phasic).
- s08_predict: Question marks sit on trapped heads' P badges; parallel-assay GOLD bar drains to 50% as a GOLD dashed line drops onto the timeline at 27 s; question card appears.
- s10_answer: Tonic segment past 27 s (27..32 s) grows MAGENTA ("held past the midpoint"), phasic gap (21..27 s) is bracketed ("ended before"), and "purified proteins, not a vessel" tag appears by the trap.
- s11_close: Full muscle world returns; Hai-Murphy ODE curves rise and part ways while gap glows; seesaw sets P badges, slow MAGENTA release holds actin, and low "ATP" meter sits beside full BLUE "force" gauge.
"""

from bp_parts import *  # noqa: F401,F403

MAGENTA = "#EE66CC"
HEAD_XS = [-4.25, -2.55, -0.85, 0.85, 2.55, 4.25]
ACTIN_Y = 2.15
THICK_Y = -0.08
SEESAW_C = np.array([-3.55, -2.42, 0.0])
PLOT_BOX = (1.10, 5.95, -2.85, -0.90)
TIMELINE_BOX = (-1.45, 5.55, -2.65, -0.55)


# ------------------------------------------------------------------ Hai-Murphy ODE model
def hai_murphy_steady(k1, k2=0.5, k3=0.4, k4=0.1, k7=0.01):
    """Solve steady-state fractions [M, Mp, AMp, AM] for the 4-state Hai-Murphy model."""
    A = np.array([
        [1.0, 1.0, 1.0, 1.0],
        [k1, -(k2 + k3), k4, 0.0],
        [0.0, k3, -(k2 + k4), k1],
        [0.0, 0.0, k2, -(k1 + k7)],
    ])
    x = np.linalg.solve(A, np.array([1.0, 0.0, 0.0, 0.0]))
    return x, float(x[1] + x[2]), float(x[2] + x[3]), float(x[3])


def _compute_hm_trajectory(t_max=34.0, dt=0.05):
    """Integrate the 4-state Hai-Murphy ODE over [0, t_max] for stimulus transient."""
    n = int(round(t_max / dt)) + 1
    ts = np.linspace(0.0, t_max, n)
    ps, fs = np.zeros(n), np.zeros(n)
    x = np.array([1.0, 0.0, 0.0, 0.0])
    k2, k3, k4, k7 = 0.5, 0.4, 0.1, 0.01
    for i, t in enumerate(ts):
        ps[i] = x[1] + x[2]
        fs[i] = x[2] + x[3]
        k1 = 1.6 if t < 8.0 else 0.15
        dx = np.array([
            -k1 * x[0] + k2 * x[1] + k7 * x[3],
            k1 * x[0] - (k2 + k3) * x[1] + k4 * x[2],
            k3 * x[1] - (k2 + k4) * x[2] + k1 * x[3],
            k2 * x[2] - (k1 + k7) * x[3],
        ])
        x = np.clip(x + dt * dx, 0.0, 1.0)
        x /= x.sum()
    return ts, ps, fs


_HM_TS, _HM_PS, _HM_FS = _compute_hm_trajectory()
_HM_P_PEAK = float(np.max(_HM_PS))
_HM_F_PEAK = float(np.max(_HM_FS))


def hm_p_norm(t):
    """Phosphorylation normalized to peak (0..1) from the Hai-Murphy ODE."""
    return float(np.interp(t, _HM_TS, _HM_PS) / _HM_P_PEAK)


def hm_f_norm(t):
    """Force normalized to peak (0..1) from the Hai-Murphy ODE."""
    return float(np.interp(t, _HM_TS, _HM_FS) / _HM_F_PEAK)


_, _P67, _F67, _ = hai_murphy_steady(1.0)
_, _P17, _F17, _L17 = hai_murphy_steady(0.1)
_, _, _F17_HIGH, _ = hai_murphy_steady(0.1, k7=0.005)
_, _, _F17_LOW, _ = hai_murphy_steady(0.1, k7=0.02)
RATIO_86 = _F17 / _F67              # 0.8584
LATCH_SHARE = _L17 / _F17           # 0.8197
RATIO_HIGH = _F17_HIGH / _F67       # 0.9288
RATIO_LOW = _F17_LOW / _F67         # 0.7479


# ------------------------------------------------------------------ World parts
def make_actin(y=ACTIN_Y, width=11.6, x_center=0.0, notched_xs=HEAD_XS):
    """GREY actin filament bar with subtle binding notches and label."""
    bar = RoundedRectangle(corner_radius=0.10, width=width, height=0.28,
                           stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.28)
    bar.move_to([x_center, y, 0])
    notches = VGroup()
    for hx in notched_xs:
        if x_center - width / 2 + 0.3 <= hx <= x_center + width / 2 - 0.3:
            n = RoundedRectangle(corner_radius=0.04, width=0.34, height=0.08,
                                 stroke_width=0, fill_color=BG, fill_opacity=0.85)
            n.move_to([hx, y - 0.11, 0])
            notches.add(n)
    lab = T("actin", 24, GREY).move_to([x_center - width / 2, y + 0.34, 0], aligned_edge=LEFT)
    g = VGroup(bar, notches, lab)
    g.bar, g.label = bar, lab
    return g


def make_thick_filament(y=THICK_Y, width=10.6, x_center=0.0, show_label=True):
    """BLUE thick filament bar."""
    bar = RoundedRectangle(corner_radius=0.12, width=width, height=0.34,
                           stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.22)
    bar.move_to([x_center, y, 0])
    g = VGroup(bar)
    g.bar = bar
    if show_label:
        lab = T("thick filament", 22, BLUE).move_to([x_center - width / 2, y - 0.38, 0], aligned_edge=LEFT)
        g.add(lab)
        g.label = lab
    return g


class MyosinHead(VGroup):
    """Articulated myosin head with ValueTrackers for attachment, power stroke, P badge, and latch color."""

    def __init__(self, base_x, base_y=THICK_Y + 0.17, attach=0.0, stroke=0.0, has_p=False,
                 latch=0.0, actin_y=ACTIN_Y - 0.14, seed=0, quiver_amp=0.024):
        super().__init__()
        self.base_x = base_x
        self.base_y = base_y
        self.actin_y = actin_y
        self.seed = seed
        self.quiver_amp = quiver_amp
        self.t_clock = 0.0

        self.attach_vt = ValueTracker(attach)
        self.stroke_vt = ValueTracker(stroke)
        self.p_vt = ValueTracker(1.0 if has_p else 0.0)
        self.latch_vt = ValueTracker(latch)

        self.neck = Line([base_x, base_y, 0], [base_x, base_y + 0.85, 0], color=BLUE, stroke_width=6)
        self.bulb = RoundedRectangle(corner_radius=0.20, width=0.60, height=0.40,
                                     stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.42)
        self.badge_bg = Circle(radius=0.22, stroke_color=GOLD, stroke_width=2.0, fill_color=GOLD, fill_opacity=0.92)
        self.badge_txt = T("P", 22, BG, weight=BOLD)
        self.badge = VGroup(self.badge_bg, self.badge_txt)

        self.add(self.neck, self.bulb, self.badge)
        self._sync(0.0)
        self.add_updater(lambda mob, dt: mob._sync(dt))

    def _sync(self, dt):
        self.t_clock += dt
        a = float(np.clip(self.attach_vt.get_value(), 0.0, 1.0))
        s = float(np.clip(self.stroke_vt.get_value(), 0.0, 1.0))
        pv = float(np.clip(self.p_vt.get_value(), 0.0, 1.0))
        lv = float(np.clip(self.latch_vt.get_value(), 0.0, 1.0))

        col = interpolate_color(ManimColor(BLUE), ManimColor(MAGENTA), lv)
        q = self.quiver_amp * np.sin(13.0 * self.t_clock + self.seed * 1.9) if a > 0.7 else 0.0

        y_detached = self.base_y + 0.82
        y_attached = self.actin_y - 0.20
        hy = y_detached + a * (y_attached - y_detached) + q
        hx = self.base_x + (0.20 - 0.44 * s) * a

        self.bulb.set_color(col)
        self.bulb.set_fill(col, opacity=0.42 + 0.20 * lv)
        self.bulb.move_to([hx, hy, 0])

        self.neck.set_color(col)
        self.neck.put_start_and_end_on([self.base_x, self.base_y, 0], [hx, hy - 0.14, 0])

        # Badge clear of bulb (bulb half-w 0.30 + badge radius 0.22 + 0.08 gap = 0.60)
        bpos = np.array([hx + 0.60, hy - 0.02, 0.0])
        self.badge_bg.move_to(bpos)
        self.badge_txt.move_to(bpos)
        if pv < 0.02:
            self.badge_bg.set_fill(GOLD, opacity=0.0)
            self.badge_bg.set_stroke(GOLD, opacity=0.0)
            self.badge_txt.set_opacity(0.0)
        else:
            self.badge_bg.set_fill(GOLD, opacity=pv * 0.92)
            self.badge_bg.set_stroke(GOLD, opacity=pv)
            self.badge_txt.set_opacity(pv)


def make_head_row(states, base_y=THICK_Y + 0.17, actin_y=ACTIN_Y - 0.14, xs=HEAD_XS, quiver_amp=0.024):
    """Build 6 MyosinHead objects from list of (attach, stroke, has_p, latch) tuples."""
    heads = VGroup()
    for i, (hx, st) in enumerate(zip(xs, states)):
        a, s, p, l = st
        heads.add(MyosinHead(hx, base_y=base_y, attach=a, stroke=s, has_p=p, latch=l,
                             actin_y=actin_y, seed=i, quiver_amp=quiver_amp))
    return heads


def cycle_head(scene, head, total_s=2.4, extra_anims=()):
    """Animate one honest cross-bridge cycle (detach -> reattach -> power stroke) on a phosphorylated head."""
    t1 = total_s * 0.34
    t2 = total_s * 0.32
    t3 = total_s - t1 - t2
    scene.play(head.attach_vt.animate.set_value(0.0), head.stroke_vt.animate.set_value(0.0), *extra_anims, run_time=t1)
    scene.play(head.attach_vt.animate.set_value(1.0), run_time=t2)
    scene.play(head.stroke_vt.animate.set_value(0.85), run_time=t3)


def make_seesaw(center=SEESAW_C, tilt=0.0, ca_lit=False):
    """Shrunk kinase/phosphatase seesaw at bottom-left driven by tilt and ca_lit trackers."""
    c = np.array(center, dtype=float)
    half_len = 1.45
    fulcrum = Polygon(c + UP * 0.02, c + LEFT * 0.30 + DOWN * 0.46, c + RIGHT * 0.30 + DOWN * 0.46,
                      stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.25)
    beam = Line(c + LEFT * half_len, c + RIGHT * half_len, color=GREY, stroke_width=5)
    mlck = boxed_label("MLCK kinase", GREEN, size=22, pad=0.12)
    mlcp = boxed_label("MLCP phosphatase", RED, size=22, pad=0.12)
    ca = boxed_label("calcium", YELLOW, size=22, pad=0.12)

    tilt_vt = ValueTracker(tilt)
    ca_vt = ValueTracker(1.0 if ca_lit else 0.0)

    def _update(mob):
        ang = float(tilt_vt.get_value())
        dx = half_len * np.cos(ang)
        dy = half_len * np.sin(ang)
        l_tip = c + np.array([-dx, -dy, 0.0])
        r_tip = c + np.array([dx, dy, 0.0])
        beam.put_start_and_end_on(l_tip, r_tip)
        mlck.move_to(l_tip + UP * 0.44)
        mlcp.move_to(r_tip + UP * 0.44)
        ca.move_to(l_tip + UP * 1.06)
        cv = float(np.clip(ca_vt.get_value(), 0.0, 1.0))
        ca.box.set_fill(YELLOW, opacity=0.14 + 0.38 * cv)
        ca.box.set_stroke(YELLOW, width=2.5 + 1.5 * cv)

    g = VGroup(fulcrum, beam, mlck, mlcp, ca)
    _update(g)
    g.add_updater(_update)
    g.tilt_vt, g.ca_vt = tilt_vt, ca_vt
    g.mlck, g.mlcp, g.ca, g.beam = mlck, mlcp, ca, beam
    return g


def make_time_plot(tau_end=0.0, box=PLOT_BOX, x_max=30.0, show_tag=True):
    """Bottom-right schematic time plot driven by Hai-Murphy ODE curves up to tau_vt."""
    P = Plot(box=box, xr=(0, x_max), yr=(0, 1.08), xticks=(), yticks=(),
             xlabel="time", ylabel="", color=GREY, size=22, label_size=22)
    P.xlabel.move_to([(box[0] + box[1]) / 2 - 0.5, box[2] - 0.32, 0])

    tau_vt = ValueTracker(tau_end)
    p_curve = P.live_curve(hm_p_norm, tau_vt, color=GOLD, width=5)
    f_curve = P.live_curve(hm_f_norm, tau_vt, color=BLUE, width=5)

    leg_f = VGroup(Line([0, 0, 0], [0.35, 0, 0], color=BLUE, stroke_width=5), T("force", 22, BLUE)).arrange(RIGHT, buff=0.10)
    leg_p = VGroup(Line([0, 0, 0], [0.35, 0, 0], color=GOLD, stroke_width=5), T("phosphorylation", 22, GOLD)).arrange(RIGHT, buff=0.10)
    legend = VGroup(leg_f, leg_p).arrange(RIGHT, buff=0.35).move_to([(box[0] + box[1]) / 2, box[3] + 0.28, 0])

    g = VGroup(P, legend, p_curve, f_curve)
    if show_tag:
        tag = T("schematic", 22, GREY).move_to([box[1], box[2] - 0.32, 0], aligned_edge=RIGHT)
        g.add(tag)
        g.tag = tag
    g.plot, g.legend, g.tau_vt, g.p_curve, g.f_curve = P, legend, tau_vt, p_curve, f_curve
    return g


def make_atp_meter(val=0.85, pos=(0.15, -1.85, 0), height=1.55, label="ATP use", color=BLUE, pulse_low=False):
    """Schematic vertical bar meter for ATP use or force (no numbers)."""
    vt = ValueTracker(val)
    w = 0.42
    frame = RoundedRectangle(corner_radius=0.08, width=w, height=height,
                             stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.8)
    frame.move_to(pos)
    bottom_y = frame.get_bottom()[1] + 0.04
    inner_h = height - 0.08
    fill = Rectangle(width=w - 0.08, height=max(0.05, inner_h * val),
                     stroke_width=0, fill_color=color, fill_opacity=0.78)
    fill.move_to([pos[0], bottom_y + fill.height / 2, 0])
    lab = T(label, 22, color).next_to(frame, DOWN, buff=0.14)

    t_acc = [0.0]

    def _upd(mob, dt):
        t_acc[0] += dt
        v = float(np.clip(vt.get_value(), 0.05, 1.0))
        if pulse_low:
            v = float(np.clip(v + 0.03 * np.sin(3.5 * t_acc[0]), 0.05, 1.0))
        h = max(0.05, inner_h * v)
        fill.stretch_to_fit_height(h)
        fill.move_to([pos[0], bottom_y + h / 2, 0])

    g = VGroup(frame, fill, lab)
    g.add_updater(_upd)
    g.vt, g.frame, g.fill, g.label = vt, frame, fill, lab
    return g


def make_trap_rig(bead_shift=0.0, p_values=(1, 1, 1), attach=1.0, stroke=0.4, quiver=True):
    """Purified myosin surface + 3 trapped heads + actin + white bead + laser trap cone."""
    surf_y = 0.46
    actin_y = 2.22
    xs = [-2.6, -0.8, 1.0]

    surface = RoundedRectangle(corner_radius=0.08, width=6.4, height=0.22,
                               stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.25)
    surface.move_to([-0.8, surf_y - 0.11, 0])
    # Place label cleanly on the LEFT end of surface so it stays clear of surface border and timeline
    surf_lab = T("purified myosin", 22, GREY).move_to([-4.0, surf_y - 0.48, 0], aligned_edge=LEFT)

    shift_vt = ValueTracker(bead_shift)
    actin = make_actin(y=actin_y, width=7.2, x_center=-0.2 + bead_shift, notched_xs=xs)
    actin_base_x = -0.2

    bead_x0 = 3.65
    bead = Circle(radius=0.33, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.92)
    bead.move_to([bead_x0 + bead_shift, actin_y, 0])

    cone = Polygon([3.65, 3.05, 0], [4.55, 1.18, 0], [2.75, 1.18, 0],
                   stroke_color=TEAL, stroke_width=2, stroke_opacity=0.45,
                   fill_color=TEAL, fill_opacity=0.12)
    trap_lab = T("laser trap", 22, TEAL).next_to(cone, RIGHT, buff=0.18).shift(DOWN * 0.25)

    heads = VGroup()
    for i, (hx, pv) in enumerate(zip(xs, p_values)):
        heads.add(MyosinHead(hx, base_y=surf_y, attach=attach, stroke=stroke, has_p=bool(pv),
                             latch=0.0, actin_y=actin_y - 0.14, seed=i, quiver_amp=0.026 if quiver else 0.0))

    t_acc = [0.0]

    def _upd_trap(mob, dt):
        t_acc[0] += dt
        dx = float(shift_vt.get_value())
        tremble = 0.024 * np.sin(14.0 * t_acc[0]) if quiver else 0.0
        actin.bar.move_to([actin_base_x + dx + tremble, actin_y, 0])
        actin.label.move_to([actin_base_x - 3.6 + dx, actin_y + 0.34, 0], aligned_edge=LEFT)
        bead.move_to([bead_x0 + dx + tremble, actin_y, 0])

    g = VGroup(cone, trap_lab, surface, surf_lab, actin, bead, heads)
    g.add_updater(_upd_trap)
    g.shift_vt, g.heads, g.bead, g.cone, g.actin, g.surface = shift_vt, heads, bead, cone, actin, surface
    return g


def make_timeline(tonic_t=0.0, phasic_t=0.0, box=TIMELINE_BOX):
    """Hammell et al. 2022 horizontal timeline (0..40 s) with scaled tonic & phasic bars."""
    P = Plot(box=box, xr=(0, 40), yr=(0, 3.4), xticks=[0, 10, 20, 30, 40], yticks=(),
             xlabel="seconds after injection", ylabel="", color=GREY, size=22, label_size=22)

    ton_vt = ValueTracker(tonic_t)
    pha_vt = ValueTracker(phasic_t)

    y_ton = 2.15
    y_pha = 0.72
    bar_h = 0.38

    def _bar(y_val, vt, col, fill_op):
        def mk():
            v = float(np.clip(vt.get_value(), 0.05, 40.0))
            x0, x1 = P.pt(0, y_val)[0], P.pt(v, y_val)[0]
            r = Rectangle(width=max(0.04, x1 - x0), height=bar_h,
                          stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=fill_op)
            r.move_to([(x0 + x1) / 2, P.pt(0, y_val)[1], 0])
            return r
        return always_redraw(mk)

    ton_bar = _bar(y_ton, ton_vt, BLUE, 0.85)
    pha_bar = _bar(y_pha, pha_vt, BLUE, 0.35)

    ton_top_y = P.pt(0, y_ton)[1] + bar_h / 2
    pha_top_y = P.pt(0, y_pha)[1] + bar_h / 2
    ton_lab = T("tonic (pig): 32 s", 22, TEXT).move_to([P.pt(0.6, 0)[0], ton_top_y + 0.14, 0], aligned_edge=DL)
    pha_lab = T("phasic (chicken): 21 s", 22, TEXT).move_to([P.pt(0.6, 0)[0], pha_top_y + 0.14, 0], aligned_edge=DL)
    tag = T("medians", 22, GREY).move_to([box[0], box[3] + 0.16, 0], aligned_edge=LEFT)

    g = VGroup(P, ton_bar, pha_bar, ton_lab, pha_lab, tag)
    g.plot, g.ton_vt, g.pha_vt = P, ton_vt, pha_vt
    g.ton_lab, g.pha_lab, g.ton_bar, g.pha_bar = ton_lab, pha_lab, ton_bar, pha_bar
    g.y_ton, g.y_pha, g.bar_h = y_ton, y_pha, bar_h
    return g


def make_parallel_assay(level=1.0):
    """Small side panel at bottom-left showing GOLD parallel assay bar draining."""
    panel = RoundedRectangle(corner_radius=0.14, width=3.1, height=2.2,
                             stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.85)
    panel.move_to([-4.25, -1.65, 0])
    head = T("parallel assay", 24, GOLD).move_to([-4.25, -0.82, 0])
    track = RoundedRectangle(corner_radius=0.08, width=0.75, height=1.25,
                             stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=0.9)
    track.move_to([-4.25, -1.85, 0])
    lv_vt = ValueTracker(level)
    bot_y = track.get_bottom()[1] + 0.04
    inner_h = 1.17
    fill = Rectangle(width=0.67, height=max(0.05, inner_h * level),
                     stroke_width=0, fill_color=GOLD, fill_opacity=0.85)
    fill.move_to([-4.25, bot_y + fill.height / 2, 0])

    def _upd(mob):
        v = float(np.clip(lv_vt.get_value(), 0.04, 1.0))
        h = max(0.05, inner_h * v)
        fill.stretch_to_fit_height(h)
        fill.move_to([-4.25, bot_y + h / 2, 0])

    g = VGroup(panel, head, track, fill)
    g.add_updater(_upd)
    g.lv_vt = lv_vt
    return g


# ------------------------------------------------------------------ Scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        heads = make_head_row([(0.0, 0.0, False, 0.0)] * 6)
        seesaw = make_seesaw(tilt=0.0, ca_lit=False)
        tplot = make_time_plot(tau_end=0.0)
        self.add(actin, thick, heads, seesaw, tplot)

        self.at("balance of kinase")
        self.play(seesaw.tilt_vt.animate.set_value(0.14), run_time=1.3)
        self.play(seesaw.tilt_vt.animate.set_value(-0.10), run_time=1.3)
        self.play(seesaw.tilt_vt.animate.set_value(0.06), run_time=1.1)

        self.at("while force is being built")
        tag_built = T("force being built", 26, BLUE).move_to([0.0, 3.05, 0])
        self.play(
            FadeIn(tag_built),
            seesaw.tilt_vt.animate.set_value(0.18),
            *[heads[i].p_vt.animate.set_value(1.0) for i in (0, 1, 3, 4)],
            run_time=1.0,
        )
        self.play(
            *[heads[i].attach_vt.animate.set_value(1.0) for i in (0, 1, 3, 4)],
            *[heads[i].stroke_vt.animate.set_value(0.85) for i in (0, 1, 3, 4)],
            tplot.tau_vt.animate.set_value(8.5),
            run_time=2.0,
            rate_func=linear,
        )

        self.at("stimulated")
        self.play(seesaw.ca_vt.animate.set_value(1.0), run_time=0.8)

        self.at("falls back toward low")
        self.play(
            seesaw.tilt_vt.animate.set_value(-0.08),
            *[heads[i].p_vt.animate.set_value(0.0) for i in (0, 1, 4)],
            tplot.tau_vt.animate.set_value(24.0),
            run_time=2.6,
            rate_func=linear,
        )

        # Keep head 3 (still carrying P) cycling while force stays near peak
        self.at("near its peak")
        self.play(tplot.tau_vt.animate.set_value(29.0),
                  heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0),
                  run_time=1.0, rate_func=linear)
        self.play(heads[3].attach_vt.animate.set_value(1.0), heads[3].stroke_vt.animate.set_value(0.85), run_time=1.0)

        self.at("holding the load")
        q_txt = T("What holds the load?", 38, TEXT).move_to([0.0, 3.05, 0])
        self.play(swap(tag_built, q_txt, run_time=0.6))
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        states = [
            (1.0, 0.85, False, 0.0),
            (1.0, 0.85, False, 0.0),
            (0.0, 0.0, False, 0.0),
            (1.0, 0.85, True, 0.0),
            (1.0, 0.85, False, 0.0),
            (0.0, 0.0, False, 0.0),
        ]
        heads = make_head_row(states)
        seesaw = make_seesaw(tilt=-0.08, ca_lit=True)
        tplot = make_time_plot(tau_end=29.0, x_max=33.0)
        q_txt = T("What holds the load?", 38, TEXT).move_to([0.0, 3.05, 0])

        self.add(actin, thick, heads, seesaw, tplot, q_txt)
        title_txt = T("Holding On: The Latch", 44, TEXT, font=TITLE_FONT).move_to([0.0, 3.05, 0])
        self.play(
            swap(q_txt, title_txt, run_time=0.7),
            tplot.tau_vt.animate.set_value(32.5),
            heads[3].attach_vt.animate.set_value(0.0),
            run_time=1.1,
            rate_func=linear,
        )
        self.play(heads[3].attach_vt.animate.set_value(1.0), run_time=0.7)
        self.finish()


class S02FourStates(SpokenScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        states = [
            (1.0, 0.85, False, 0.0),
            (1.0, 0.85, False, 0.0),
            (0.0, 0.0, False, 0.0),
            (1.0, 0.85, True, 0.0),
            (1.0, 0.85, False, 0.0),
            (0.0, 0.0, False, 0.0),
        ]
        heads = make_head_row(states)
        seesaw = make_seesaw(tilt=-0.08, ca_lit=True)
        tplot = make_time_plot(tau_end=30.0)
        self.add(actin, thick, heads, seesaw, tplot)

        # Keep active phosphorylated head 3 cycling while ghost trace peels down
        cycle_head(self, heads[3], total_s=2.4)
        self.at("follow it down")
        ghost_vt = ValueTracker(0.0)

        def _ghost():
            w = float(ghost_vt.get_value())
            fn = lambda t: (1.0 - w) * hm_f_norm(t) + w * hm_p_norm(t)
            c = tplot.plot.curve(fn, x0=8.0, x1=30.0, color=BLUE, width=4, n=80)
            return DashedVMobject(c, num_dashes=18, dashed_ratio=0.55)

        ghost = always_redraw(_ghost)
        self.add(ghost)
        self.play(ghost_vt.animate.set_value(1.0), run_time=1.4)
        self.play(FadeOut(ghost), run_time=0.4)

        self.at("In 1988")
        tag = T("Hai and Murphy, 1988 (model)", 24, GOLD).move_to([-6.1, 3.25, 0], aligned_edge=LEFT)
        self.play(FadeIn(tag), FadeOut(tplot), FadeOut(thick), FadeOut(heads), run_time=1.0)

        gx_l, gx_r = 0.15, 3.75
        by_top, by_bot = 0.85, -1.15
        ly_top, ly_bot = 0.45, -1.55

        h_np_att = MyosinHead(gx_l, base_y=by_top, attach=1.0, stroke=0.0, has_p=False, actin_y=ACTIN_Y - 0.14, seed=0)
        h_p_att = MyosinHead(gx_r, base_y=by_top, attach=1.0, stroke=0.0, has_p=True, actin_y=ACTIN_Y - 0.14, seed=1)
        h_np_det = MyosinHead(gx_l, base_y=by_bot, attach=0.0, stroke=0.0, has_p=False, actin_y=ACTIN_Y - 0.14, seed=2)
        h_p_det = MyosinHead(gx_r, base_y=by_bot, attach=0.0, stroke=0.0, has_p=True, actin_y=ACTIN_Y - 0.14, seed=3)

        l_np_att = T("no P, attached", 26, BLUE).move_to([gx_l, ly_top, 0])
        l_p_att = T("P, attached", 26, GOLD).move_to([gx_r, ly_top, 0])
        l_np_det = T("no P, detached", 26, BLUE).move_to([gx_l, ly_bot, 0])
        l_p_det = T("P, detached", 26, GOLD).move_to([gx_r, ly_bot, 0])

        # Stage the 2x2 arrival cleanly across the kinetic-model and four-states lines
        self.play(FadeIn(h_p_att), FadeIn(h_np_att), run_time=1.5)
        self.play(FadeIn(h_p_det), FadeIn(h_np_det), run_time=1.5)
        self.play(FadeIn(l_p_att), FadeIn(l_np_att), run_time=1.3)

        self.at("attached or not")
        self.play(FadeIn(l_p_det), FadeIn(l_np_det), run_time=1.4)

        # Kinase arrows start from right-of-calcium corridor (above MLCP, clear of calcium) -> left of no-P heads
        self.at("act on heads")
        k_orig = seesaw.mlck.get_corner(UR) + np.array([0.14, 0.08, 0.0])
        arr_k_att = Arrow(k_orig, [gx_l - 0.45, 1.75, 0], color=GREEN, stroke_width=3.5, tip_length=0.2, buff=0)
        arr_k_det = Arrow(seesaw.mlck.get_right() + RIGHT * 0.14, [gx_l - 0.45, -0.35, 0],
                          color=GREEN, stroke_width=3.5, tip_length=0.2, buff=0)
        l_np_att_new = T("P, attached", 26, GOLD).move_to([gx_l, ly_top, 0])
        l_np_det_new = T("P, detached", 26, GOLD).move_to([gx_l, ly_bot, 0])
        self.play(Create(arr_k_att), Create(arr_k_det), run_time=0.55)
        self.play(h_np_att.p_vt.animate.set_value(1.0), h_np_det.p_vt.animate.set_value(1.0),
                  swap(l_np_att, l_np_att_new, run_time=0.5), swap(l_np_det, l_np_det_new, run_time=0.5), run_time=0.65)

        # Phosphatase arrows both originate at MLCP (p_orig): arr_p_det goes to the detached head,
        # while arr_p_att curves wide below and to the right around the detached head to the attached head.
        p_orig = seesaw.mlcp.get_right() + RIGHT * 0.16
        arr_p_det = CurvedArrow(p_orig, [gx_r + 1.05, -0.35, 0], angle=0.35, color=RED, stroke_width=3.5, tip_length=0.2)
        arr_p_att = TipableVMobject(color=RED, stroke_width=3.5)
        arr_p_att.set_points_smoothly([
            p_orig,
            np.array([1.85, -2.35, 0.0]),
            np.array([4.95, -2.00, 0.0]),
            np.array([5.55, -0.30, 0.0]),
            np.array([5.45, 1.05, 0.0]),
            np.array([gx_r + 1.05, 1.75, 0.0]),
        ])
        arr_p_att.add_tip(tip_length=0.2)
        l_p_att_new = T("no P, attached", 26, BLUE).move_to([gx_r, ly_top, 0])
        l_p_det_new = T("no P, detached", 26, BLUE).move_to([gx_r, ly_bot, 0])
        self.play(FadeOut(arr_k_att), FadeOut(arr_k_det), Create(arr_p_det), Create(arr_p_att), run_time=0.5)
        self.play(h_p_att.p_vt.animate.set_value(0.0), h_p_det.p_vt.animate.set_value(0.0),
                  swap(l_p_att, l_p_att_new, run_time=0.5), swap(l_p_det, l_p_det_new, run_time=0.5), run_time=0.65)
        self.play(FadeOut(arr_p_det), FadeOut(arr_p_att), run_time=0.3)
        self.finish()


class S03LatchBridge(SpokenScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        states = [
            (1.0, 0.8, True, 0.0),
            (0.0, 0.0, False, 0.0),
            (1.0, 0.85, True, 0.0),   # focus head (index 2)
            (1.0, 0.3, True, 0.0),    # cycling neighbour (index 3)
            (1.0, 0.8, True, 0.0),
            (0.0, 0.0, False, 0.0),
        ]
        heads = make_head_row(states)
        seesaw = make_seesaw(tilt=0.14, ca_lit=True)
        tplot = make_time_plot(tau_end=30.0)
        self.add(actin, thick, heads, seesaw, tplot)

        self.at("balance still sets")
        self.play(seesaw.tilt_vt.animate.set_value(-0.10),
                  heads[0].p_vt.animate.set_value(0.0),
                  heads[4].p_vt.animate.set_value(0.0), run_time=1.2)
        self.play(seesaw.tilt_vt.animate.set_value(0.06),
                  heads[0].p_vt.animate.set_value(1.0),
                  heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0), run_time=1.0)

        self.at("loses its phosphate")
        phosp_tok = Arrow(seesaw.mlcp.get_top() + UP * 0.1, [HEAD_XS[2] - 0.15, 1.30, 0],
                          color=RED, stroke_width=4, tip_length=0.2, buff=0)
        self.play(Create(phosp_tok), heads[3].attach_vt.animate.set_value(1.0), run_time=0.55)
        self.play(heads[2].p_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.9), run_time=0.8)
        self.play(FadeOut(phosp_tok), heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0), run_time=0.6)
        self.play(heads[3].attach_vt.animate.set_value(1.0), heads[3].stroke_vt.animate.set_value(0.5), run_time=0.9)

        self.at("latch bridge")
        lb_lab = T("latch bridge", 28, MAGENTA).move_to([HEAD_XS[2], 3.05, 0])
        self.play(heads[2].latch_vt.animate.set_value(1.0), FadeIn(lb_lab), run_time=0.7)

        self.at("slow detachment")
        clk_c = np.array([HEAD_XS[1] - 0.15, 2.98, 0.0])
        clk_ring = Circle(radius=0.36, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.8).move_to(clk_c)
        clk_ang = ValueTracker(PI / 2)
        clk_hand = always_redraw(lambda: Line(clk_c, clk_c + 0.27 * np.array([np.cos(clk_ang.get_value()), np.sin(clk_ang.get_value()), 0]),
                                              color=GOLD, stroke_width=3.5))
        rate_tag = T("rate-limiting step", 24, MAGENTA).next_to(clk_ring, LEFT, buff=0.22)
        self.play(FadeIn(clk_ring), FadeIn(clk_hand), FadeIn(rate_tag), run_time=0.35)

        for _ in range(2):
            self.play(heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0),
                      clk_ang.animate.increment_value(-PI * 0.45), run_time=0.38)
            self.play(heads[3].attach_vt.animate.set_value(1.0),
                      clk_ang.animate.increment_value(-PI * 0.45), run_time=0.34)
            self.play(heads[3].stroke_vt.animate.set_value(0.9),
                      clk_ang.animate.increment_value(-PI * 0.45), run_time=0.38)

        self.play(heads[2].attach_vt.animate.set_value(0.0),
                  heads[2].latch_vt.animate.set_value(0.0),
                  clk_ang.animate.increment_value(-PI * 0.45), run_time=0.55)
        self.play(heads[2].p_vt.animate.set_value(1.0), heads[2].attach_vt.animate.set_value(0.75), run_time=0.4)
        self.finish()


class S04OneIdea(SpokenScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        heads = make_head_row([(0.0, 0.0, False, 0.0)] * 6)
        seesaw = make_seesaw(tilt=0.0, ca_lit=True)
        tplot = make_time_plot(tau_end=0.0)
        cyc_vt = ValueTracker(0)
        cyc_txt = always_redraw(lambda: T(f"cycling: {int(round(cyc_vt.get_value()))}", 24, BLUE).move_to([-4.6, 3.05, 0]))
        atp_meter = make_atp_meter(val=0.15, pos=(0.15, -1.85, 0), height=1.55, label="ATP use", color=BLUE)

        self.add(actin, thick, heads, seesaw, tplot, cyc_txt, atp_meter)

        self.at("switches heads on")
        self.play(
            seesaw.tilt_vt.animate.set_value(0.18),
            *[heads[i].p_vt.animate.set_value(1.0) for i in (0, 1, 3, 4)],
            cyc_vt.animate.set_value(4),
            atp_meter.vt.animate.set_value(0.90),
            run_time=0.7,
        )
        self.play(
            *[heads[i].attach_vt.animate.set_value(1.0) for i in (0, 1, 3, 4)],
            *[heads[i].stroke_vt.animate.set_value(0.85) for i in (0, 1, 3, 4)],
            tplot.tau_vt.animate.set_value(9.0),
            run_time=1.3,
            rate_func=linear,
        )

        self.at("lose it let go slowly")
        self.play(
            seesaw.tilt_vt.animate.set_value(-0.08),
            *[heads[i].p_vt.animate.set_value(0.0) for i in (0, 1, 4)],
            *[heads[i].latch_vt.animate.set_value(1.0) for i in (0, 1, 4)],
            cyc_vt.animate.set_value(1),
            tplot.tau_vt.animate.set_value(24.0),
            run_time=1.8,
            rate_func=linear,
        )

        self.at("outlast the phosphate")
        idea_txt = T("force outlasts the phosphate", 34, TEXT).move_to([0.3, 3.05, 0])
        self.play(FadeIn(idea_txt), tplot.tau_vt.animate.set_value(30.0), run_time=1.0, rate_func=linear)

        self.at("while cycling")
        cycle_head(self, heads[3], total_s=2.2, extra_anims=[atp_meter.vt.animate.set_value(0.22)])
        self.finish()


class S05ModelNumbers(SpokenScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        states_67 = [
            (1.0, 0.85, True, 0.0),
            (1.0, 0.85, True, 0.0),
            (0.0, 0.0, False, 0.0),
            (1.0, 0.85, True, 0.0),
            (1.0, 0.85, True, 0.0),
            (0.0, 0.0, False, 0.0),
        ]
        heads = make_head_row(states_67)
        seesaw = make_seesaw(tilt=0.12, ca_lit=True)
        tplot = make_time_plot(tau_end=30.0)
        self.add(actin, thick, heads, seesaw, tplot)

        self.at("illustrative run")
        bar_base_y = -2.45
        bar_h_ref = 1.55
        bar_w = 1.05
        x_left, x_right = 2.25, 4.65

        bar_axis = Line([1.25, bar_base_y, 0], [5.75, bar_base_y, 0], color=GREY, stroke_width=2.5)
        bar_67 = Rectangle(width=bar_w, height=bar_h_ref, stroke_color=BLUE, stroke_width=2.5,
                           fill_color=BLUE, fill_opacity=0.80)
        bar_67.move_to([x_left, bar_base_y + bar_h_ref / 2, 0])
        lbl_67 = T("67%\nphosphorylated", 22, TEXT, line_spacing=0.85).next_to([x_left, bar_base_y, 0], DOWN, buff=0.16)
        val_67 = M("1.00", 22, BLUE).next_to(bar_67, UP, buff=0.08)

        h17 = bar_h_ref * RATIO_86
        r_vt = ValueTracker(0.02)
        latch_frac_vt = ValueTracker(0.0)

        def _mk_right_bar():
            h = max(0.04, bar_h_ref * float(r_vt.get_value()))
            lf = float(np.clip(latch_frac_vt.get_value(), 0.0, 1.0)) * LATCH_SHARE
            hl, hc = h * lf, max(0.0, h * (1.0 - lf))
            g = VGroup()
            if hl > 0.01:
                rl = Rectangle(width=bar_w, height=hl, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.82)
                rl.move_to([x_right, bar_base_y + hl / 2, 0])
                g.add(rl)
            if hc > 0.01:
                rc = Rectangle(width=bar_w, height=hc, stroke_width=0, fill_color=BLUE, fill_opacity=0.80)
                rc.move_to([x_right, bar_base_y + hl + hc / 2, 0])
                g.add(rc)
            border = Rectangle(width=bar_w, height=h, stroke_color=BLUE, stroke_width=2.5, fill_opacity=0)
            border.move_to([x_right, bar_base_y + h / 2, 0])
            g.add(border)
            return g

        bar_17 = always_redraw(_mk_right_bar)
        lbl_17 = T("17%\nphosphorylated", 22, TEXT, line_spacing=0.85).next_to([x_right, bar_base_y, 0], DOWN, buff=0.16)
        val_17 = M("≈86%", 22, BLUE).move_to([x_right, bar_base_y + h17 + 0.18, 0])
        run_tag = T("illustrative model run", 22, GREY).move_to([5.75, -0.46, 0], aligned_edge=RIGHT)

        bars_group = VGroup(bar_axis, bar_67, lbl_67, val_67, lbl_17, run_tag)
        self.play(FadeOut(tplot), FadeIn(bars_group), run_time=0.8)
        self.add(bar_17)
        cycle_head(self, heads[4], total_s=2.0)

        self.at("held about")
        self.play(
            seesaw.tilt_vt.animate.set_value(-0.14),
            r_vt.animate.set_value(RATIO_86),
            heads[0].p_vt.animate.set_value(0.0),
            heads[1].p_vt.animate.set_value(0.0),
            heads[4].p_vt.animate.set_value(0.0),
            heads[0].latch_vt.animate.set_value(1.0),
            heads[1].latch_vt.animate.set_value(1.0),
            heads[4].latch_vt.animate.set_value(1.0),
            heads[2].attach_vt.animate.set_value(1.0),
            heads[2].stroke_vt.animate.set_value(0.85),
            heads[2].latch_vt.animate.set_value(1.0),
            run_time=2.2,
        )
        self.play(FadeIn(val_17), run_time=0.4)

        self.at("Most of it sat")
        self.play(latch_frac_vt.animate.set_value(1.0),
                  heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0), run_time=1.2)
        self.play(heads[3].attach_vt.animate.set_value(1.0), heads[3].stroke_vt.animate.set_value(0.85), run_time=1.1)

        self.at("depends on the constants")
        m_hi = Line([x_right - 0.68, bar_base_y + bar_h_ref * RATIO_HIGH, 0],
                    [x_right + 0.68, bar_base_y + bar_h_ref * RATIO_HIGH, 0], color=GREY, stroke_width=2.5)
        m_lo = Line([x_right - 0.68, bar_base_y + bar_h_ref * RATIO_LOW, 0],
                    [x_right + 0.68, bar_base_y + bar_h_ref * RATIO_LOW, 0], color=GREY, stroke_width=2.5)
        self.play(FadeIn(m_hi), FadeIn(m_lo), FadeOut(val_17), run_time=0.35)
        self.play(r_vt.animate.set_value(RATIO_HIGH),
                  heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0), run_time=1.2)
        self.play(r_vt.animate.set_value(RATIO_LOW),
                  heads[3].attach_vt.animate.set_value(1.0), heads[3].stroke_vt.animate.set_value(0.85), run_time=1.2)
        self.play(r_vt.animate.set_value(RATIO_86),
                  heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0), run_time=1.0)
        self.play(FadeIn(val_17), FadeOut(m_hi), FadeOut(m_lo),
                  heads[3].attach_vt.animate.set_value(1.0), heads[3].stroke_vt.animate.set_value(0.85), run_time=0.9)

        self.at("not a structure")
        not_imaged = T("model, not imaged", 26, GREY).move_to([0.0, 3.05, 0])
        self.play(FadeIn(not_imaged), run_time=0.5)
        cycle_head(self, heads[3], total_s=2.0)
        self.finish()


class S06Economy(SpokenScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        states = [
            (1.0, 0.85, False, 1.0),
            (1.0, 0.85, False, 1.0),
            (1.0, 0.85, False, 1.0),
            (1.0, 0.40, True, 0.0),
            (1.0, 0.85, False, 1.0),
            (0.0, 0.0, False, 0.0),
        ]
        heads = make_head_row(states)
        seesaw = make_seesaw(tilt=-0.12, ca_lit=True)
        tplot = make_time_plot(tau_end=30.0)
        atp_chip = chip("ATP present", TEAL, size=22, pad=0.14).move_to([0.0, -0.58, 0])
        self.add(actin, thick, heads, seesaw, tplot, atp_chip)

        cycle_head(self, heads[3], total_s=2.1)
        cycle_head(self, heads[3], total_s=2.1)

        self.at("keep cycling")
        self.play(
            heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0),
            heads[0].attach_vt.animate.set_value(0.0), heads[0].latch_vt.animate.set_value(0.0),
            run_time=1.0,
        )
        self.play(
            heads[3].attach_vt.animate.set_value(1.0), heads[3].stroke_vt.animate.set_value(0.9),
            heads[5].p_vt.animate.set_value(1.0), heads[5].attach_vt.animate.set_value(1.0),
            run_time=1.0,
        )
        self.play(
            heads[3].attach_vt.animate.set_value(0.0), heads[3].stroke_vt.animate.set_value(0.0),
            heads[5].p_vt.animate.set_value(0.0), heads[5].latch_vt.animate.set_value(1.0),
            heads[1].attach_vt.animate.set_value(0.0), heads[1].latch_vt.animate.set_value(0.0),
            run_time=1.1,
        )

        self.at("Nor is it rigor")
        rigor_bg = RoundedRectangle(corner_radius=0.14, width=5.0, height=2.45,
                                    stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.96)
        rigor_bg.move_to([3.50, -1.85, 0])
        r_actin = Line([1.3, -1.05, 0], [5.7, -1.05, 0], color=GREY, stroke_width=6)
        r_thick = Line([1.5, -2.05, 0], [5.5, -2.05, 0], color=GREY, stroke_width=6)
        r_heads = VGroup(*[Line([x, -2.05, 0], [x, -1.10, 0], color=GREY, stroke_width=5)
                           for x in (1.9, 2.7, 3.5, 4.3, 5.1)])
        fuel_box = Rectangle(width=0.45, height=0.65, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([1.7, -2.58, 0])
        rigor_lbl = T("rigor: no ATP", 24, GREY).next_to(fuel_box, RIGHT, buff=0.22)
        rigor_panel = VGroup(rigor_bg, r_actin, r_thick, r_heads, fuel_box, rigor_lbl)

        self.play(FadeOut(tplot), FadeIn(rigor_panel),
                  heads[3].attach_vt.animate.set_value(1.0), heads[3].stroke_vt.animate.set_value(0.8),
                  run_time=0.8)

        cross1 = Line([1.3, -2.15, 0], [5.6, -0.85, 0], color=RED, stroke_width=6)
        cross2 = Line([1.3, -0.85, 0], [5.6, -2.15, 0], color=RED, stroke_width=6)
        cross = VGroup(cross1, cross2)
        self.play(Create(cross), run_time=0.55)
        self.wait(0.6)
        self.play(FadeOut(rigor_panel), FadeOut(cross), FadeIn(tplot), run_time=0.7)

        self.at("economy")
        atp_meter = make_atp_meter(val=0.22, pos=(0.15, -1.85, 0), height=1.55, label="ATP use",
                                   color=BLUE, pulse_low=True)
        self.play(FadeIn(atp_meter), run_time=0.5)
        cycle_head(self, heads[3], total_s=2.0)
        self.finish()


class S07Trap(SpokenScene):
    def construct(self):
        # Start detached, then attach and pull bead + actin right as BLUE force rises to plateau
        trap = make_trap_rig(bead_shift=0.0, p_values=(1, 1, 1), attach=0.0, stroke=0.0, quiver=True)
        tag = T("Hammell et al., 2022", 24, GOLD).move_to([-6.1, 3.25, 0], aligned_edge=LEFT)
        tplot = make_time_plot(tau_end=0.0, box=PLOT_BOX, show_tag=False)
        tplot.remove(tplot.p_curve)
        tplot.legend.remove(tplot.legend[1])
        tplot.legend.move_to([(PLOT_BOX[0] + PLOT_BOX[1]) / 2, PLOT_BOX[3] + 0.28, 0])

        self.add(trap, tag, tplot)

        self.play(
            *[h.attach_vt.animate.set_value(1.0) for h in trap.heads],
            run_time=1.8,
        )
        self.play(
            *[h.stroke_vt.animate.set_value(0.65) for h in trap.heads],
            trap.shift_vt.animate.set_value(0.28),
            tplot.tau_vt.animate.set_value(7.5),
            run_time=3.4,
            rate_func=linear,
        )

        self.at("laser trap")
        self.play(
            trap.shift_vt.animate.set_value(0.45),
            tplot.tau_vt.animate.set_value(20.0),
            run_time=3.8,
            rate_func=linear,
        )

        self.at("injected the phosphatase")
        phos_chip = chip("phosphatase", RED, size=22, pad=0.14).move_to([-5.20, 2.52, 0])
        self.play(FadeIn(phos_chip), run_time=0.35)
        self.play(phos_chip.animate.move_to([-5.20, 1.35, 0]), run_time=0.75)
        phos_arr = Arrow([-4.12, 1.35, 0], [-3.05, 1.35, 0], color=RED, stroke_width=4, tip_length=0.2, buff=0)
        self.play(Create(phos_arr), run_time=0.4)
        self.play(FadeOut(phos_chip), FadeOut(phos_arr), run_time=0.35)

        self.at("Tonic myosin")
        tl = make_timeline(tonic_t=0.0, phasic_t=0.0)
        self.play(FadeOut(tplot), FadeIn(tl), run_time=0.8)
        self.play(tl.ton_vt.animate.set_value(32.0), run_time=3.8)

        self.at("Phasic myosin")
        self.play(tl.pha_vt.animate.set_value(21.0), run_time=3.0)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        trap = make_trap_rig(bead_shift=0.45, p_values=(1, 1, 1), attach=1.0, stroke=0.65, quiver=True)
        tag = T("Hammell et al., 2022", 24, GOLD).move_to([-6.1, 3.25, 0], aligned_edge=LEFT)
        tl = make_timeline(tonic_t=32.0, phasic_t=21.0)
        self.add(trap, tag, tl)

        self.at("not timed")
        q_marks = VGroup(*[
            T("?", 26, GOLD, weight=BOLD).next_to(h.badge_bg, RIGHT, buff=0.08)
            for h in trap.heads
        ])
        for qm in q_marks:
            self.play(FadeIn(qm), run_time=0.65)

        self.at("parallel assay")
        assay = make_parallel_assay(level=1.0)
        self.play(FadeIn(assay), run_time=0.8)

        self.at("near 27 seconds")
        mid_line = DashedLine(tl.plot.pt(27, 0), tl.plot.pt(27, 3.4), color=GOLD, stroke_width=3.5, dash_length=0.14)
        mid_lbl = T("phosphate midpoint ≈27 s", 24, GOLD).next_to(tl.plot.pt(27, 3.4), UP, buff=0.14)
        self.play(assay.lv_vt.animate.set_value(0.50), Create(mid_line), FadeIn(mid_lbl), run_time=2.2)

        self.at("Which hold")
        qcard = question_card("Which hold is stronger evidence?", y=3.15, color=TEXT, size=34, max_w=10.0)
        self.play(swap(tag, qcard, run_time=0.65))
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Which hold is stronger evidence?"
    CARD = {"y": 3.15, "color": TEXT, "size": 34, "max_w": 10.0}
    RING_AT = (5.9, 3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        trap = make_trap_rig(bead_shift=0.45, p_values=(1, 1, 1), attach=1.0, stroke=0.65, quiver=True)
        q_marks = VGroup(*[
            T("?", 26, GOLD, weight=BOLD).next_to(h.badge_bg, RIGHT, buff=0.08)
            for h in trap.heads
        ])
        tl = make_timeline(tonic_t=32.0, phasic_t=21.0)
        assay = make_parallel_assay(level=0.50)
        mid_line = DashedLine(tl.plot.pt(27, 0), tl.plot.pt(27, 3.4), color=GOLD, stroke_width=3.5, dash_length=0.14)
        mid_lbl = T("phosphate midpoint ≈27 s", 24, GOLD).next_to(tl.plot.pt(27, 3.4), UP, buff=0.14)
        return VGroup(trap, q_marks, tl, assay, mid_line, mid_lbl)


class S10Answer(SpokenScene):
    def construct(self):
        trap = make_trap_rig(bead_shift=0.45, p_values=(1, 1, 1), attach=1.0, stroke=0.65, quiver=True)
        q_marks = VGroup(*[
            T("?", 26, GOLD, weight=BOLD).next_to(h.badge_bg, RIGHT, buff=0.08)
            for h in trap.heads
        ])
        tl = make_timeline(tonic_t=32.0, phasic_t=21.0)
        assay = make_parallel_assay(level=0.50)
        mid_line = DashedLine(tl.plot.pt(27, 0), tl.plot.pt(27, 3.4), color=GOLD, stroke_width=3.5, dash_length=0.14)
        mid_lbl = T("phosphate midpoint ≈27 s", 24, GOLD).next_to(tl.plot.pt(27, 3.4), UP, buff=0.14)
        qcard = question_card("Which hold is stronger evidence?", y=3.15, color=TEXT, size=34, max_w=10.0)
        self.add(trap, q_marks, tl, assay, mid_line, mid_lbl, qcard)

        self.at("tonic hold")
        x27 = tl.plot.pt(27, tl.y_ton)[0]
        x32 = tl.plot.pt(32, tl.y_ton)[0]
        y_ton = tl.plot.pt(0, tl.y_ton)[1]
        past_vt = ValueTracker(0.05)

        def _mk_past():
            frac = float(np.clip(past_vt.get_value(), 0.04, 1.0))
            w = max(0.04, (x32 - x27) * frac)
            r = Rectangle(width=w, height=tl.bar_h,
                          stroke_color=MAGENTA, stroke_width=3, fill_color=MAGENTA, fill_opacity=0.90)
            r.move_to([x27 + w / 2, y_ton, 0])
            return r

        past_seg = always_redraw(_mk_past)
        self.play(FadeOut(qcard), run_time=0.6)
        self.add(past_seg)

        # Grow the 27..32 s MAGENTA hold segment across "Only it outlasted that clock"
        self.at("outlasted that clock")
        past_lbl = T("held past\nthe midpoint", 22, MAGENTA, line_spacing=0.85).move_to([x32 + 0.16, y_ton, 0], aligned_edge=LEFT)
        self.play(past_vt.animate.set_value(1.0), FadeIn(past_lbl), run_time=2.8, rate_func=linear)

        self.at("phasic hold ended")
        x21 = tl.plot.pt(21, tl.y_pha)[0]
        y_pha = tl.plot.pt(0, tl.y_pha)[1]
        br_line = Line([x21, y_pha, 0], [x27, y_pha, 0], color=RED, stroke_width=4)
        tick_l = Line([x21, y_pha - 0.14, 0], [x21, y_pha + 0.14, 0], color=RED, stroke_width=3)
        tick_r = Line([x27, y_pha - 0.14, 0], [x27, y_pha + 0.14, 0], color=RED, stroke_width=3)
        ended_lbl = T("ended before", 22, RED).move_to([x27 + 0.22, y_pha, 0], aligned_edge=LEFT)
        self.play(Create(tick_l), Create(br_line), Create(tick_r), run_time=1.4)
        self.play(FadeIn(ended_lbl), run_time=0.8)

        self.at("purified pig")
        limit_tag = T("purified proteins, not a vessel", 24, TEXT).move_to([0.0, 3.05, 0])
        self.play(FadeIn(limit_tag), run_time=0.9)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        actin = make_actin()
        thick = make_thick_filament()
        heads = make_head_row([(0.0, 0.0, False, 0.0)] * 6)
        seesaw = make_seesaw(tilt=0.0, ca_lit=True)
        tplot = make_time_plot(tau_end=0.0, show_tag=False)
        self.add(actin, thick, heads, seesaw, tplot)

        # Force is built up to peak (tau 0 -> 8.5)
        self.play(tplot.tau_vt.animate.set_value(8.5),
                  seesaw.tilt_vt.animate.set_value(0.18),
                  run_time=2.4, rate_func=linear)

        self.at("part")
        ts_gap = np.linspace(8.5, 30.0, 40)
        top_pts = [tplot.plot.pt(t, hm_f_norm(t)) for t in ts_gap]
        bot_pts = [tplot.plot.pt(t, hm_p_norm(t)) for t in reversed(ts_gap)]
        gap_poly = Polygon(*(top_pts + bot_pts), stroke_width=0, fill_color=MAGENTA, fill_opacity=0.22)
        gap_poly.layout_ok = True
        self.play(tplot.tau_vt.animate.set_value(30.0), FadeIn(gap_poly), run_time=2.0, rate_func=linear)

        self.at("balance sets")
        self.play(*[heads[i].p_vt.animate.set_value(1.0) for i in (0, 1, 3, 4)], run_time=0.8)
        self.play(
            *[heads[i].attach_vt.animate.set_value(1.0) for i in (0, 1, 3, 4)],
            *[heads[i].stroke_vt.animate.set_value(0.85) for i in (0, 1, 3, 4)],
            run_time=1.0,
        )

        self.at("Slow release")
        self.play(
            seesaw.tilt_vt.animate.set_value(-0.08),
            *[heads[i].p_vt.animate.set_value(0.0) for i in (0, 1, 4)],
            *[heads[i].latch_vt.animate.set_value(1.0) for i in (0, 1, 4)],
            run_time=1.6,
        )
        cycle_head(self, heads[3], total_s=2.4)
        cycle_head(self, heads[3], total_s=2.4)

        self.at("holds force cheaply")
        atp_m = make_atp_meter(val=0.20, pos=(-0.22, -1.85, 0), height=1.55, label="ATP", color=BLUE, pulse_low=True)
        frc_m = make_atp_meter(val=0.90, pos=(0.48, -1.85, 0), height=1.55, label="force", color=BLUE, pulse_low=False)
        self.play(FadeIn(atp_m), FadeIn(frc_m), run_time=0.8)
        self.finish()


class S12End(EndCard):
    LINE = "The phosphate switches myosin on; slow release lets force outlast it."
