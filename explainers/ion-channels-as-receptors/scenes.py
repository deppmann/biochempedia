"""Open a Hole, Spend the Gradient — STEMhop explainer animation.

COLOUR MAP (one colour per concept for the entire film):
- YELLOW (#F5D547): Na+ ions, Na+ channel, E_Na, Na+ driving force
- TEAL   (#3FB8C0): K+ ions, K+ channel, E_K, K+ driving force
- BLUE   (#58C4DD): Lipid bilayer membrane & generic/multi-ion channel body
- GREEN  (#83C167): Na+/K+ pump (ATP-driven uphill transport) & open-state accent
- TEXT   (#E8EAF0): Membrane voltage Vm (gauge needle, readout, trace, primary labels)
- RED    (#FC6255): Electrical pull / negative inner membrane charge / signal trigger
- GREY   (#8B93A1): Gauge track, axes, closed gate, schematic tags

CARRIED WORLD:
A cross-section of a cell membrane (Outside Na+ above, lipid bilayer across the middle,
Inside K+ below) filling >60% of the frame height, paired on the right with a vertical
membrane-voltage gauge Vm (schematic, -100 mV to +80 mV).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_hook: Ions execute computed thermal motion (fixed-seed rng); a slow 3-step receptor
  chain advances and is skipped as a signal opens the pore, Na+ streams inward by
  (Vm - E_Na), and Vm integrates upward via dVm/dt = -k*(Vm - E_Na).
- s02_pump_vs_channel: Left pump cycles conformational states to push 3 Na+ up and 2 K+
  down per ATP while its computed counter ticks ~10^2 ions/s; right channel opens and
  streams Na+ downhill while its counter races at ~10^7 ions/s.
- s03_two_forces: Concentration push arrow grows from Outside->Inside density difference,
  electrical pull arrow grows toward negative inner charges at -70 mV, and both merge
  into the electrochemical gradient driving computed Na+ flow through the pore.
- s04_equilibrium: Vm sweeps to +60 mV then -90 mV; electrical pull length L_elec =
  L_conc * (Vm / E_ion) updates continuously until it balances concentration push and
  net pore flux reaches zero at E_Na and E_K.
- s05_driving_force_rule: Live vertical brackets grow along the gauge from Vm (-70 mV)
  to E_Na (+60 mV) and E_K (-90 mV) while counters compute Vm - E = -130 mV and +20 mV
  and force arrows scale proportionally.
- s06_predict_q: Na+ and K+ ions bounce off two closed channel gates in computed thermal
  motion while the predict question card appears in the bottom band.
- s08_predict_reveal: Na+ channel opens and Vm integrates up toward +60 mV with dense
  computed inward Na+ flux; Na+ shuts and Vm returns to -70 mV; K+ channel opens with
  sparse outward flux (scaled by 20/130) as Vm nudges down toward -90 mV.
- s09_single_channel: A 2-state Markov chain (fixed seed) switches one patch-clamped
  channel between Closed and Open, synchronizing gate snapping, ion bursts, and a live
  scrolling square trace at fixed step height as open probability rises with signal.
- s10_closing: Brief channel opening sends a few computed Na+ ions across while Vm swings
  boldly and bulk concentration meters stay near 100%; a multi-ion channel then passes
  Na+ and K+ together so Vm settles between E_K and E_Na.
"""
from bp_parts import *

# Concept colour map
NA_COL = YELLOW
K_COL = TEAL
MEM_COL = BLUE
PUMP_COL = GREEN
VOLT_COL = TEXT
ELEC_COL = RED
STRUCT_COL = GREY

# Shared carried-world geometry (16:9 safe frame: x in [-6.3, 6.3], y in [-3.5, 3.5])
MEM_X0, MEM_X1 = -6.0, 1.9
MEM_Y0, MEM_Y1 = -0.34, 0.34
OUT_Y0, OUT_Y1 = 0.54, 2.24
IN_Y0, IN_Y1 = -1.78, -0.54

GAUGE_X = 3.45
GAUGE_Y0, GAUGE_Y1 = -2.00, 2.40
V_MIN, V_MAX = -100.0, 80.0
E_NA = 60.0
E_K = -90.0
V_REST = -70.0


def v_to_y(v):
    """Map membrane voltage (mV) linearly onto the vertical gauge y-coordinate."""
    frac = (v - V_MIN) / (V_MAX - V_MIN)
    return GAUGE_Y0 + frac * (GAUGE_Y1 - GAUGE_Y0)


def build_bilayer(x0=MEM_X0, x1=MEM_X1, gaps=(), gap_half=0.52):
    """Build the horizontal lipid bilayer with clean cutouts for embedded proteins."""
    g = VGroup()
    intervals = []
    cur = x0
    for gx in sorted(gaps):
        if gx - gap_half > cur:
            intervals.append((cur, gx - gap_half))
        cur = max(cur, gx + gap_half)
    if x1 > cur:
        intervals.append((cur, x1))

    for a, b in intervals:
        band = Rectangle(
            width=b - a,
            height=MEM_Y1 - MEM_Y0,
            stroke_width=0,
            fill_color=MEM_COL,
            fill_opacity=0.22,
        ).move_to([(a + b) / 2, 0.0, 0.0])
        top_line = Line([a, MEM_Y1, 0], [b, MEM_Y1, 0], color=MEM_COL, stroke_width=4)
        bot_line = Line([a, MEM_Y0, 0], [b, MEM_Y0, 0], color=MEM_COL, stroke_width=4)
        g.add(band, top_line, bot_line)
        n_lipids = max(2, int((b - a) / 0.28))
        for k in range(n_lipids):
            lx = a + (k + 0.5) * (b - a) / n_lipids
            g.add(
                Line([lx, MEM_Y1 - 0.05, 0], [lx, 0.05, 0], color=MEM_COL, stroke_width=2).set_opacity(0.45),
                Line([lx, MEM_Y0 + 0.05, 0], [lx, -0.05, 0], color=MEM_COL, stroke_width=2).set_opacity(0.45),
            )
    return g


def build_compartment_headers(x0=MEM_X0, include_legends=True):
    """Build Outside / Inside labels and ion colour legends strictly clear of ion paths."""
    out_lab = T("Outside", size=28, color=TEXT, weight=BOLD).move_to([x0 + 0.68, 2.75, 0])
    in_lab = T("Inside", size=28, color=TEXT, weight=BOLD).move_to([x0 + 0.56, -2.20, 0])
    g = VGroup(out_lab, in_lab)
    if include_legends:
        na_dot = Dot([x0 + 1.75, 2.75, 0], radius=0.10, color=NA_COL)
        na_txt = T("Na+", size=26, color=NA_COL, weight=BOLD).next_to(na_dot, RIGHT, buff=0.12)
        k_dot = Dot([x0 + 1.55, -2.20, 0], radius=0.10, color=K_COL)
        k_txt = T("K+", size=26, color=K_COL, weight=BOLD).next_to(k_dot, RIGHT, buff=0.12)
        g.add(na_dot, na_txt, k_dot, k_txt)
    return g


def build_channel(x, color=MEM_COL, open_tracker=None, y=0.0):
    """Build a gated pore protein with left/right subunits and hinged gate bar."""
    wall_w, wall_h = 0.26, 1.02
    pore_half = 0.28
    left_wall = RoundedRectangle(
        corner_radius=0.08, width=wall_w, height=wall_h,
        stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.38,
    ).move_to([x - pore_half - wall_w / 2, y, 0])
    right_wall = RoundedRectangle(
        corner_radius=0.08, width=wall_w, height=wall_h,
        stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.38,
    ).move_to([x + pore_half + wall_w / 2, y, 0])

    if open_tracker is None:
        gate = Line([x - pore_half + 0.03, y, 0], [x + pore_half - 0.03, y, 0], color=TEXT, stroke_width=6)
    else:
        def mk_gate():
            op = float(np.clip(open_tracker.get_value(), 0.0, 1.0))
            pivot = np.array([x - pore_half + 0.03, y, 0.0])
            ang = -op * 1.15
            L = 2 * pore_half - 0.06
            end = pivot + np.array([L * np.cos(ang), L * np.sin(ang), 0.0])
            col = GREEN if op > 0.4 else TEXT
            return Line(pivot, end, color=col, stroke_width=6)
        gate = always_redraw(mk_gate)

    return VGroup(left_wall, right_wall, gate)


def build_pump(x, phase_tracker, y=0.0):
    """Build a conformational Na+/K+ pump that rocks between inward-open and outward-open."""
    def mk():
        ph = float(phase_tracker.get_value())  # 0 = open inside, 1 = open outside
        tilt = (0.5 - ph) * 0.28
        left_pts = [
            [x - 0.46, y - 0.50, 0],
            [x - 0.16 - tilt, y - 0.50, 0],
            [x - 0.10 + tilt, y + 0.50, 0],
            [x - 0.46, y + 0.50, 0],
        ]
        right_pts = [
            [x + 0.16 + tilt, y - 0.50, 0],
            [x + 0.46, y - 0.50, 0],
            [x + 0.46, y + 0.50, 0],
            [x + 0.10 - tilt, y + 0.50, 0],
        ]
        lw = Polygon(*left_pts, stroke_color=PUMP_COL, stroke_width=3.5, fill_color=PUMP_COL, fill_opacity=0.38)
        rw = Polygon(*right_pts, stroke_color=PUMP_COL, stroke_width=3.5, fill_color=PUMP_COL, fill_opacity=0.38)
        return VGroup(lw, rw)
    return always_redraw(mk)


def build_gauge(vm_tracker, show_e_na=False, show_e_k=False, show_readout=True, gx=GAUGE_X):
    """Build the carried vertical membrane voltage gauge with live needle and readout."""
    track = RoundedRectangle(
        corner_radius=0.08, width=0.22, height=GAUGE_Y1 - GAUGE_Y0,
        stroke_color=STRUCT_COL, stroke_width=2.5, fill_color=STRUCT_COL, fill_opacity=0.20,
    ).move_to([gx, (GAUGE_Y0 + GAUGE_Y1) / 2, 0])
    title = T("Vm (schematic)", size=24, color=STRUCT_COL).move_to([gx + 0.55, 2.85, 0])

    ticks = VGroup()
    for val, txt in [(-100, "−100"), (-70, "−70"), (0, "0"), (80, "+80")]:
        ty = v_to_y(val)
        ticks.add(Line([gx - 0.22, ty, 0], [gx - 0.09, ty, 0], color=STRUCT_COL, stroke_width=2.5))
        lab = M(txt, size=22, color=STRUCT_COL).next_to([gx - 0.26, ty, 0], LEFT, buff=0.08)
        ticks.add(lab)

    needle = always_redraw(lambda: VGroup(
        Line([gx - 0.13, v_to_y(vm_tracker.get_value()), 0],
             [gx + 0.22, v_to_y(vm_tracker.get_value()), 0], color=VOLT_COL, stroke_width=5),
        Triangle(color=VOLT_COL, fill_color=VOLT_COL, fill_opacity=1.0).scale(0.12).rotate(PI / 2).move_to(
            [gx + 0.30, v_to_y(vm_tracker.get_value()), 0]
        ),
    ))

    g = VGroup(track, title, ticks, needle)

    if show_e_na:
        ey = v_to_y(E_NA)
        na_tick = Line([gx - 0.12, ey, 0], [gx + 0.38, ey, 0], color=NA_COL, stroke_width=4)
        na_lab = M("E_Na +60", size=24, color=NA_COL).next_to([gx + 0.66, ey + 0.26, 0], RIGHT, buff=0.06)
        g.add(na_tick, na_lab)

    if show_e_k:
        ky = v_to_y(E_K)
        k_tick = Line([gx - 0.12, ky, 0], [gx + 0.38, ky, 0], color=K_COL, stroke_width=4)
        k_lab = M("E_K −90", size=24, color=K_COL).next_to([gx + 0.66, ky - 0.26, 0], RIGHT, buff=0.06)
        g.add(k_tick, k_lab)

    if show_readout:
        ro = always_redraw(lambda: M(
            f"Vm = {vm_tracker.get_value():+.0f} mV" if abs(vm_tracker.get_value()) >= 0.5 else "Vm = 0 mV",
            size=26, color=VOLT_COL,
        ).move_to([gx + 0.55, -2.55, 0]))
        g.add(ro)

    return g


def make_ion_swarm(
    seed, n_na=32, n_k=32, x0=MEM_X0 + 0.18, x1=MEM_X1 - 0.18,
    pores=(), allow_cross=None, speed_scale=0.55,
):
    """Create a computed ion particle simulation with thermal motion and pore flux.

    pores: list of (pore_x, open_tracker, dir_sign_fn, rate_fn)
    Returns (VGroup of Dot mobjects, updater function dt -> None).
    """
    rng = np.random.default_rng(seed)
    na_dots = []
    k_dots = []

    # Initial thermal positions
    na_pos = np.column_stack([
        rng.uniform(x0, x1, n_na),
        rng.uniform(OUT_Y0 + 0.08, OUT_Y1 - 0.08, n_na),
    ])
    na_vel = rng.normal(0.0, speed_scale, (n_na, 2))
    na_state = np.zeros(n_na, dtype=int)  # 0=outside, 1=crossing down, 2=inside

    k_pos = np.column_stack([
        rng.uniform(x0, x1, n_k),
        rng.uniform(IN_Y0 + 0.08, IN_Y1 - 0.08, n_k),
    ])
    k_vel = rng.normal(0.0, speed_scale, (n_k, 2))
    k_state = np.zeros(n_k, dtype=int)  # 0=inside, 1=crossing up, 2=outside

    for p in na_pos:
        na_dots.append(Dot([p[0], p[1], 0.0], radius=0.095, color=NA_COL))
    for p in k_pos:
        k_dots.append(Dot([p[0], p[1], 0.0], radius=0.095, color=K_COL))

    swarm = VGroup(*na_dots, *k_dots)
    # Keep track of active crossing slots
    cross_timer = {"na": 0.0, "k": 0.0}

    def step_group(pos, vel, state, dots, y_lo, y_hi, ion_kind, dt):
        for i in range(len(dots)):
            st = state[i]
            if st == 0:
                pos[i] += vel[i] * dt
                if pos[i, 0] < x0:
                    pos[i, 0] = x0
                    vel[i, 0] = abs(vel[i, 0])
                elif pos[i, 0] > x1:
                    pos[i, 0] = x1
                    vel[i, 0] = -abs(vel[i, 0])
                if pos[i, 1] < y_lo:
                    pos[i, 1] = y_lo
                    vel[i, 1] = abs(vel[i, 1])
                elif pos[i, 1] > y_hi:
                    pos[i, 1] = y_hi
                    vel[i, 1] = -abs(vel[i, 1])
                # Slight thermal jitter
                vel[i] += rng.normal(0.0, 0.25 * dt, 2)
                spd = np.linalg.norm(vel[i])
                if spd > 1.2 * speed_scale:
                    vel[i] *= 1.2 * speed_scale / spd
            else:
                # Crossing through assigned pore x (stored in vel[i, 0] = pore_x, vel[i, 1] = vy)
                px, vy = vel[i, 0], vel[i, 1]
                pos[i, 0] += (px - pos[i, 0]) * min(1.0, 12.0 * dt)
                pos[i, 1] += vy * dt
                if ion_kind == "na" and pos[i, 1] < IN_Y0 + 0.12:
                    # Recycle smoothly to outer pool so concentration stays visually rich
                    state[i] = 0
                    pos[i] = [rng.uniform(x0, x1), OUT_Y1 - 0.12]
                    vel[i] = rng.normal(0.0, speed_scale, 2)
                elif ion_kind == "k" and pos[i, 1] > OUT_Y1 - 0.12:
                    state[i] = 0
                    pos[i] = [rng.uniform(x0, x1), IN_Y0 + 0.12]
                    vel[i] = rng.normal(0.0, speed_scale, 2)

            dots[i].move_to([pos[i, 0], pos[i, 1], 0.0])

        # Check open pores for ion entry
        for px, kind_match, op_fn, vy_fn in pores:
            if kind_match != ion_kind:
                continue
            if op_fn() > 0.5:
                rate = vy_fn()  # desired crossings per second
                if rate > 0.05:
                    cross_timer[ion_kind] += rate * dt
                    while cross_timer[ion_kind] >= 1.0:
                        cross_timer[ion_kind] -= 1.0
                        # Pick closest idle ion in pool to pore mouth
                        idle = np.where(state == 0)[0]
                        if len(idle) == 0:
                            break
                        mouth_y = OUT_Y0 + 0.1 if ion_kind == "na" else IN_Y1 - 0.1
                        dists = np.hypot(pos[idle, 0] - px, pos[idle, 1] - mouth_y)
                        pick = idle[int(np.argmin(dists))]
                        state[pick] = 1
                        pos[pick, 0] = px + rng.uniform(-0.10, 0.10)
                        pos[pick, 1] = mouth_y
                        vy_speed = -max(1.8, 0.55 * rate) if ion_kind == "na" else max(1.3, 0.55 * rate)
                        vel[pick] = [px, vy_speed]

    def update(mob, dt):
        dt = min(dt, 0.06)
        step_group(na_pos, na_vel, na_state, na_dots, OUT_Y0 + 0.08, OUT_Y1 - 0.08, "na", dt)
        step_group(k_pos, k_vel, k_state, k_dots, IN_Y0 + 0.08, IN_Y1 - 0.08, "k", dt)

    swarm.add_updater(update)
    return swarm


# ------------------------------------------------------------------ scenes
class S00Hook(SpokenScene):
    def construct(self):
        pore_x = -2.0
        op = ValueTracker(0.0)
        vm = ValueTracker(V_REST)

        bilayer = build_bilayer(gaps=(pore_x,))
        headers = build_compartment_headers()
        chan = build_channel(pore_x, color=MEM_COL, open_tracker=op)
        gauge = build_gauge(vm)

        # Rate proportional to driving force |Vm - E_Na| when gate is open
        swarm = make_ion_swarm(
            seed=10, n_na=30, n_k=28,
            pores=[(pore_x, "na", lambda: op.get_value(), lambda: 0.12 * max(0.0, E_NA - vm.get_value()))],
        )

        # Slow G-protein/kinase chain inset in upper right of membrane area (clear of pore & ions)
        chain_steps = VGroup(
            boxed_label("Receptor", STRUCT_COL, size=24, pad=0.14),
            boxed_label("G protein", STRUCT_COL, size=24, pad=0.14),
            boxed_label("Kinase", STRUCT_COL, size=24, pad=0.14),
        ).arrange(RIGHT, buff=0.45).move_to([-0.2, 2.75, 0])
        c_arr1 = Arrow(chain_steps[0].get_right(), chain_steps[1].get_left(), buff=0.06, color=STRUCT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        c_arr2 = Arrow(chain_steps[1].get_right(), chain_steps[2].get_left(), buff=0.06, color=STRUCT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        chain_grp = VGroup(chain_steps, c_arr1, c_arr2)

        ms_badge = boxed_label("~1 ms?", NA_COL, size=28, pad=0.16).move_to([0.3, -2.20, 0])

        self.add(bilayer, headers, chan, gauge, swarm)
        self.at("about a millisecond")
        self.play(FadeIn(ms_badge, shift=UP * 0.1), run_time=0.5)

        self.at("hand their message")
        self.play(FadeIn(chain_grp), run_time=0.5)
        # Step highlight cleanly below the boxes (y=2.36) so nothing crosses text
        relay_dot = Dot([chain_steps[0].get_center()[0], 2.34, 0], radius=0.08, color=ELEC_COL)
        self.play(
            FadeIn(relay_dot),
            chain_steps[0].box.animate.set_stroke(ELEC_COL),
            run_time=0.5,
        )
        self.play(
            relay_dot.animate.move_to([chain_steps[1].get_center()[0], 2.34, 0]),
            chain_steps[1].box.animate.set_stroke(ELEC_COL),
            run_time=1.0,
        )
        self.play(
            relay_dot.animate.move_to([chain_steps[2].get_center()[0], 2.34, 0]),
            chain_steps[2].box.animate.set_stroke(ELEC_COL),
            run_time=1.0,
        )

        self.at("skips that chain")
        self.play(FadeOut(VGroup(chain_grp, relay_dot), shift=UP * 0.15), run_time=0.55)

        self.at("opens a hole")
        sig = Dot([pore_x - 0.55, 0.72, 0], radius=0.12, color=ELEC_COL)
        self.play(FadeIn(sig, scale=1.3), run_time=0.3)
        self.play(sig.animate.move_to([pore_x - 0.42, 0.38, 0]), op.animate.set_value(1.0), run_time=0.45)
        self.play(FadeOut(sig), run_time=0.2)

        self.at("ions rush through")
        # Integrate dVm/dt = -k*(Vm - E_Na) smoothly toward +32 mV
        self.at("voltage shifts")
        self.play(vm.animate.set_value(32.0), run_time=1.4, rate_func=rush_from)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Ion Channels as Receptors"
    TITLE = "Open a Hole, Spend the Gradient"


class S02PumpVsChannel(SpokenScene):
    def construct(self):
        pump_x, chan_x = -1.5, 3.0
        pump_ph = ValueTracker(0.0)
        chan_op = ValueTracker(0.0)
        pump_cnt = ValueTracker(0.0)
        chan_cnt = ValueTracker(0.0)

        bilayer = build_bilayer(x0=-6.0, x1=6.0, gaps=(pump_x, chan_x))
        headers = build_compartment_headers(x0=-6.0)
        pump = build_pump(pump_x, pump_ph)
        chan = build_channel(chan_x, color=MEM_COL, open_tracker=chan_op)

        swarm = make_ion_swarm(
            seed=20, n_na=42, n_k=36, x0=-5.8, x1=5.8,
            pores=[(chan_x, "na", lambda: chan_op.get_value(), lambda: 8.5)],
        )

        pump_lab = T("Pump (ATP)", size=28, color=PUMP_COL, weight=BOLD).move_to([pump_x, 2.75, 0])
        chan_lab = T("Channel", size=28, color=MEM_COL, weight=BOLD).move_to([chan_x, 2.75, 0])

        pump_rate = M("~10² ions/s", size=26, color=PUMP_COL).move_to([pump_x, -2.20, 0])
        pump_live = counter("moved: {:.0f}", pump_cnt, at=[pump_x, -2.75, 0], size=26, color=TEXT)
        chan_rate = M("~10⁷ ions/s", size=26, color=NA_COL).move_to([chan_x, -2.20, 0])
        chan_live = counter("moved: {:,.0f}", chan_cnt, at=[chan_x, -2.75, 0], size=26, color=TEXT)

        self.add(bilayer, headers, swarm)
        self.at("Two kinds of protein")
        self.play(FadeIn(pump), FadeIn(chan), FadeIn(pump_lab), FadeIn(chan_lab), run_time=0.7)

        self.at("A pump binds ions")
        p_na = Dot([pump_x, -0.45, 0], radius=0.11, color=NA_COL)
        p_k = Dot([pump_x, 0.45, 0], radius=0.11, color=K_COL)
        self.play(FadeIn(p_na, scale=1.2), run_time=0.4)

        self.at("uses")
        atp_tag = boxed_label("ATP", PUMP_COL, size=24, pad=0.12).move_to([pump_x, -2.20, 0])
        self.play(FadeIn(atp_tag, shift=UP * 0.15), run_time=0.35)

        self.at("pushes them uphill")
        self.play(
            pump_ph.animate.set_value(1.0),
            p_na.animate.move_to([pump_x, 0.65, 0]),
            run_time=0.55,
        )
        self.play(FadeIn(p_k), FadeOut(p_na), run_time=0.15)
        self.play(
            pump_ph.animate.set_value(0.0),
            p_k.animate.move_to([pump_x, -0.65, 0]),
            run_time=0.55,
        )
        self.play(FadeOut(p_k), FadeOut(atp_tag), run_time=0.15)

        self.at("only a few hundred")
        self.play(FadeIn(pump_rate), FadeIn(pump_live), run_time=0.4)
        self.play(pump_cnt.animate.set_value(300), run_time=1.0, rate_func=linear)

        self.at("A channel is a gated pore")
        chan_open_lab = T("Open channel", size=28, color=MEM_COL, weight=BOLD).move_to([chan_x, 2.75, 0])
        self.play(Indicate(chan, color=NA_COL), run_time=0.6)

        self.at("Open it")
        self.play(chan_op.animate.set_value(1.0), swap(chan_lab, chan_open_lab, run_time=0.5), run_time=0.5)

        self.at("millions")
        self.play(FadeIn(chan_rate), FadeIn(chan_live), run_time=0.4)
        self.play(
            chan_cnt.animate.set_value(10_000_000),
            pump_cnt.animate.set_value(600),
            run_time=2.2,
            rate_func=linear,
        )

        self.at("Pumps build gradients slowly")
        self.play(pump_ph.animate.set_value(1.0), pump_cnt.animate.set_value(900), run_time=1.4, rate_func=linear)
        self.at("channels spend them fast")
        self.play(chan_cnt.animate.set_value(20_000_000), pump_ph.animate.set_value(0.0), run_time=1.4, rate_func=linear)
        self.finish()


class S03TwoForces(SpokenScene):
    def construct(self):
        pore_x = -0.3
        op = ValueTracker(1.0)
        vm = ValueTracker(V_REST)

        bilayer = build_bilayer(gaps=(pore_x,))
        headers = build_compartment_headers()
        chan = build_channel(pore_x, color=MEM_COL, open_tracker=op)
        gauge = build_gauge(vm)

        swarm = make_ion_swarm(
            seed=30, n_na=32, n_k=28,
            pores=[(pore_x, "na", lambda: 1.0, lambda: 10.0)],
        )

        self.add(bilayer, headers, chan, gauge, swarm)

        self.at("Two forces")
        conc_arrow = Arrow([-2.4, 1.45, 0], [-2.4, 0.25, 0], buff=0, color=NA_COL, stroke_width=8, max_tip_length_to_length_ratio=0.28)

        self.at("Crowded ions spread")
        self.play(GrowArrow(conc_arrow), run_time=0.6)
        self.at("from high concentration")
        conc_badge = boxed_label("Concentration push", NA_COL, size=22, pad=0.11).move_to([-1.60, 2.75, 0])
        self.play(FadeIn(conc_badge, shift=DOWN * 0.1), run_time=0.5)

        self.at("Membrane voltage pulls")
        minus_signs = VGroup(*[
            M("−", size=26, color=ELEC_COL).move_to([x, -0.46, 0])
            for x in [-5.3, -4.1, -2.9, -1.7, 0.9, 1.6]
        ])
        minus_signs.layout_ok = "contrast"
        elec_arrow = Arrow([0.8, 1.45, 0], [0.8, 0.25, 0], buff=0, color=ELEC_COL, stroke_width=8, max_tip_length_to_length_ratio=0.28)
        elec_badge = boxed_label("Voltage pull", ELEC_COL, size=22, pad=0.11).move_to([1.25, 2.75, 0])

        self.play(FadeIn(minus_signs), GrowArrow(elec_arrow), FadeIn(elec_badge, shift=DOWN * 0.1), run_time=0.8)

        self.at("resting neuron")
        rest_tag = M("−70 mV (rest)", size=24, color=VOLT_COL).next_to([GAUGE_X + 0.45, v_to_y(V_REST), 0], RIGHT, buff=0.08)
        self.play(FadeIn(rest_tag), run_time=0.5)

        self.at("Together")
        comb_arrow = Arrow([pore_x, 1.50, 0], [pore_x, -0.15, 0], buff=0, color=VOLT_COL, stroke_width=10, max_tip_length_to_length_ratio=0.28)
        self.play(
            conc_arrow.animate.move_to([pore_x - 0.16, 0.80, 0]),
            elec_arrow.animate.move_to([pore_x + 0.16, 0.80, 0]),
            FadeOut(VGroup(conc_badge, elec_badge)),
            run_time=0.9,
        )
        self.at("electrochemical gradient")
        grad_badge = boxed_label("Electrochemical gradient", VOLT_COL, size=26, pad=0.16).move_to([-0.5, -2.85, 0])
        self.play(
            ReplacementTransform(VGroup(conc_arrow, elec_arrow), comb_arrow),
            FadeIn(grad_badge, shift=UP * 0.1),
            run_time=0.8,
        )
        self.finish()


class S04Equilibrium(SpokenScene):
    def construct(self):
        pore_x = -0.3
        op = ValueTracker(1.0)
        vm = ValueTracker(V_REST)
        mode = {"ion": "na", "reveal_target": False}  # "na" or "k"

        bilayer = build_bilayer(gaps=(pore_x,))
        headers = build_compartment_headers()
        chan = build_channel(pore_x, color=MEM_COL, open_tracker=op)
        gauge = build_gauge(vm, show_e_na=False, show_e_k=False)

        # Computed pore flux goes to zero as Vm reaches E_ion!
        def flux_rate():
            v = vm.get_value()
            if mode["ion"] == "na":
                return 0.12 * max(0.0, E_NA - v)
            return 0.12 * max(0.0, v - E_K)

        swarm = make_ion_swarm(
            seed=40, n_na=30, n_k=30,
            pores=[
                (pore_x, "na", lambda: 1.0 if mode["ion"] == "na" else 0.0, flux_rate),
                (pore_x, "k", lambda: 1.0 if mode["ion"] == "k" else 0.0, flux_rate),
            ],
        )

        # Computed opposing force arrows: L_conc fixed (1.05), L_elec proportional to Vm / E_ion
        L_CONC = 1.05

        def mk_force_arrows():
            v = vm.get_value()
            if mode["ion"] == "na":
                # Concentration pushes inward (down: dy = -L_CONC)
                c_arr = Arrow([-3.8, 1.55, 0], [-3.8, 1.55 - L_CONC, 0], buff=0, color=NA_COL, stroke_width=8, max_tip_length_to_length_ratio=0.30)
                # Electrical force on Na+: downward (dy < 0) when Vm < 0, upward (dy > 0) when Vm > 0
                dy = L_CONC * (v / E_NA)
                if abs(dy) < 0.12:
                    e_arr = Dot([-2.4, 1.02, 0], radius=0.07, color=ELEC_COL)
                elif dy < 0:
                    e_arr = Arrow([-2.4, 1.55, 0], [-2.4, 1.55 + dy, 0], buff=0, color=ELEC_COL, stroke_width=8, max_tip_length_to_length_ratio=0.30)
                else:
                    e_arr = Arrow([-2.4, 0.50, 0], [-2.4, 0.50 + dy, 0], buff=0, color=ELEC_COL, stroke_width=8, max_tip_length_to_length_ratio=0.30)
            else:
                # K+ concentration pushes outward (up: dy = +L_CONC)
                c_arr = Arrow([-3.8, -1.55, 0], [-3.8, -1.55 + L_CONC, 0], buff=0, color=K_COL, stroke_width=8, max_tip_length_to_length_ratio=0.30)
                # Electrical pull on K+ is inward (down: dy < 0) when Vm < 0
                dy = L_CONC * (v / abs(E_K))
                if abs(dy) < 0.12:
                    e_arr = Dot([-2.4, -1.02, 0], radius=0.07, color=ELEC_COL)
                elif dy < 0:
                    e_arr = Arrow([-2.4, -0.50, 0], [-2.4, -0.50 + dy, 0], buff=0, color=ELEC_COL, stroke_width=8, max_tip_length_to_length_ratio=0.30)
                else:
                    e_arr = Arrow([-2.4, -1.55, 0], [-2.4, -1.55 + dy, 0], buff=0, color=ELEC_COL, stroke_width=8, max_tip_length_to_length_ratio=0.30)
            return VGroup(c_arr, e_arr)

        arrows = always_redraw(mk_force_arrows)

        def mk_net_readout():
            v = vm.get_value()
            target = E_NA if mode["ion"] == "na" else E_K
            gap = v - target
            if abs(gap) < 2.0:
                txt = "Net flow = 0 (balanced)"
                col = GREEN
            elif mode["reveal_target"]:
                txt = f"Pull toward {target:+.0f} mV"
                col = VOLT_COL
            else:
                txt = "Net flow ≠ 0"
                col = VOLT_COL
            return M(txt, size=26, color=col).move_to([-0.8, -2.90, 0])

        net_ro = always_redraw(mk_net_readout)
        eq_title = boxed_label("Equilibrium potential (E)", VOLT_COL, size=26, pad=0.14).move_to([-0.5, 2.75, 0])

        self.add(bilayer, headers, chan, gauge, swarm)
        self.at("balances those two forces")
        self.add(arrows, net_ro)

        self.at("equilibrium potential")
        self.play(FadeIn(eq_title), run_time=0.6)

        self.at("Sodium is crowded outside")
        na_label_txt = T("Na+ concentration push", size=24, color=NA_COL).move_to([-4.35, 1.88, 0])
        na_elec_txt = T("Voltage pull", size=24, color=ELEC_COL).move_to([-1.50, 1.88, 0])
        na_label = VGroup(BackgroundRectangle(na_label_txt, color=BG, fill_opacity=1.0, buff=0.06), na_label_txt)
        na_elec_label = VGroup(BackgroundRectangle(na_elec_txt, color=BG, fill_opacity=1.0, buff=0.06), na_elec_txt)
        self.play(FadeIn(na_label), FadeIn(na_elec_label), run_time=0.5)

        self.at("strongly positive inside")
        self.play(vm.animate.set_value(20.0), run_time=1.3)

        self.at("about plus 60")
        mode["reveal_target"] = True
        e_na_tick = Line([GAUGE_X - 0.12, v_to_y(E_NA), 0], [GAUGE_X + 0.38, v_to_y(E_NA), 0], color=NA_COL, stroke_width=4)
        e_na_lab = M("E_Na ≈ +60", size=24, color=NA_COL).next_to([GAUGE_X + 0.56, v_to_y(E_NA) + 0.28, 0], RIGHT, buff=0.06)
        self.play(
            vm.animate.set_value(E_NA), FadeIn(e_na_tick), FadeIn(e_na_lab),
            run_time=max(0.35, self.t_of("60") - 0.2 - self.elapsed()),
        )

        self.at("holds it back")
        self.wait(0.8)

        self.at("Potassium is crowded inside")
        self.play(FadeOut(na_label), FadeOut(na_elec_label), run_time=0.35)
        mode["ion"] = "k"
        mode["reveal_target"] = False
        vm.set_value(V_REST)
        k_label_txt = T("K+ concentration push", size=24, color=K_COL).move_to([-4.35, -1.83, 0])
        k_elec_txt = T("Voltage pull", size=24, color=ELEC_COL).move_to([-1.50, -1.83, 0])
        k_label = VGroup(BackgroundRectangle(k_label_txt, color=BG, fill_opacity=1.0, buff=0.06), k_label_txt)
        k_elec_label = VGroup(BackgroundRectangle(k_elec_txt, color=BG, fill_opacity=1.0, buff=0.06), k_elec_txt)
        self.play(FadeIn(k_label), FadeIn(k_elec_label), run_time=0.4)

        self.at("its balance point")
        mode["reveal_target"] = True
        e_k_tick = Line([GAUGE_X - 0.12, v_to_y(E_K), 0], [GAUGE_X + 0.38, v_to_y(E_K), 0], color=K_COL, stroke_width=4)
        e_k_lab = M("E_K ≈ −90", size=24, color=K_COL).next_to([GAUGE_X + 0.56, v_to_y(E_K) - 0.28, 0], RIGHT, buff=0.06)
        self.play(
            vm.animate.set_value(E_K), FadeIn(e_k_tick), FadeIn(e_k_lab),
            run_time=max(0.4, self.t_of("90") - 0.2 - self.elapsed()),
        )

        self.at("sits below rest")
        rest_mark = M("rest −70", size=22, color=STRUCT_COL).next_to([GAUGE_X + 0.56, v_to_y(V_REST), 0], RIGHT, buff=0.06)
        self.play(FadeIn(rest_mark), run_time=0.5)
        self.finish()


class S05DrivingForceRule(SpokenScene):
    def construct(self):
        pore_x = -0.3
        op = ValueTracker(1.0)
        vm = ValueTracker(V_REST)

        bilayer = build_bilayer(gaps=(pore_x,))
        headers = build_compartment_headers()
        chan = build_channel(pore_x, color=MEM_COL, open_tracker=op)
        gauge = build_gauge(vm, show_e_na=True, show_e_k=True)
        swarm = make_ion_swarm(
            seed=50, n_na=28, n_k=28,
            pores=[(pore_x, "na", lambda: 1.0, lambda: 8.0)],
        )

        self.add(bilayer, headers, chan, gauge, swarm)

        self.at("An open channel pulls")
        pull_arr = Arrow(
            [GAUGE_X + 0.48, v_to_y(V_REST) + 0.15, 0],
            [GAUGE_X + 0.48, v_to_y(E_NA) - 0.15, 0],
            buff=0, color=NA_COL, stroke_width=5, max_tip_length_to_length_ratio=0.14,
        )
        self.play(GrowArrow(pull_arr), run_time=1.0)

        self.at("The pull is the driving force")
        formula = boxed_label("Driving force = Vm − E", VOLT_COL, size=28, pad=0.16).move_to([-0.5, 2.75, 0])
        self.play(FadeOut(pull_arr), FadeIn(formula, shift=DOWN * 0.1), run_time=0.6)

        self.at("membrane voltage minus")
        self.wait(0.5)

        self.at("For sodium")
        na_prog = ValueTracker(0.0)
        na_bar = always_redraw(lambda: Line(
            [GAUGE_X + 0.50, v_to_y(V_REST), 0],
            [GAUGE_X + 0.50, v_to_y(V_REST + na_prog.get_value() * (E_NA - V_REST)), 0],
            color=NA_COL, stroke_width=10,
        ))
        na_gap_num = always_redraw(lambda: M(
            f"{0 if abs(-130.0 * na_prog.get_value()) < 0.5 else -130.0 * na_prog.get_value():.0f} mV",
            size=24, color=NA_COL,
        ).next_to([GAUGE_X + 0.66, v_to_y(-5.0), 0], RIGHT, buff=0.06))
        na_eq_lhs = M("Na+: −70 − (+60)", size=28, color=NA_COL)
        na_eq_rhs = M("= −130 mV", size=28, color=NA_COL)
        na_eq_grp = VGroup(na_eq_lhs, na_eq_rhs).arrange(RIGHT, buff=0.22).move_to([-1.2, -2.55, 0])
        self.add(na_bar, na_gap_num)
        self.play(FadeIn(na_eq_lhs), run_time=0.4)
        self.play(
            na_prog.animate.set_value(1.0),
            run_time=max(0.4, self.t_of("is minus 130") - 0.2 - self.elapsed()),
            rate_func=linear,
        )

        self.at("is minus 130")
        self.play(FadeIn(na_eq_rhs), run_time=0.35)
        self.at("a huge gap")
        na_force_arr = Arrow([-3.4, 1.75, 0], [-3.4, 0.55, 0], buff=0, color=NA_COL, stroke_width=10, max_tip_length_to_length_ratio=0.28)
        self.play(GrowArrow(na_force_arr), run_time=0.7)

        self.at("For potassium")
        k_prog = ValueTracker(0.0)
        k_bar = always_redraw(lambda: Line(
            [GAUGE_X + 0.50, v_to_y(V_REST), 0],
            [GAUGE_X + 0.50, v_to_y(V_REST + k_prog.get_value() * (E_K - V_REST)), 0],
            color=K_COL, stroke_width=10,
        ))
        k_gap_num = always_redraw(lambda: M(
            f"+{20.0 * k_prog.get_value():.0f} mV", size=24, color=K_COL,
        ).next_to([GAUGE_X + 0.66, v_to_y(-78.0), 0], RIGHT, buff=0.06))
        k_eq_lhs = M("K+:  −70 − (−90)", size=28, color=K_COL)
        k_eq_rhs = M("= +20 mV", size=28, color=K_COL)
        k_eq_grp = VGroup(k_eq_lhs, k_eq_rhs).arrange(RIGHT, buff=0.22).move_to([-1.2, -3.10, 0])
        k_eq_grp.align_to(na_eq_grp, LEFT)
        self.add(k_bar, k_gap_num)
        self.play(FadeIn(k_eq_lhs), run_time=0.4)
        self.play(
            k_prog.animate.set_value(1.0),
            run_time=max(0.4, self.t_of("is just 20") - 0.2 - self.elapsed()),
            rate_func=linear,
        )

        self.at("is just 20")
        k_force_arr = Arrow([-1.9, -0.95, 0], [-1.9, -0.60, 0], buff=0, color=K_COL, stroke_width=6, max_tip_length_to_length_ratio=0.45)
        self.play(FadeIn(k_eq_rhs), GrowArrow(k_force_arr), run_time=0.5)
        self.finish()


def build_predict_world():
    """Shared world builder for S06PredictQ, S07PredictPause, and S08PredictReveal."""
    na_x, k_x = -1.55, 0.85
    op_na = ValueTracker(0.0)
    op_k = ValueTracker(0.0)
    vm = ValueTracker(V_REST)

    bilayer = build_bilayer(gaps=(na_x, k_x))
    headers = build_compartment_headers()
    ch_na = build_channel(na_x, color=NA_COL, open_tracker=op_na)
    ch_k = build_channel(k_x, color=K_COL, open_tracker=op_k)
    gauge = build_gauge(vm, show_e_na=True, show_e_k=True)
    na_lab = T("Na+ channel", size=26, color=NA_COL, weight=BOLD).move_to([na_x, 2.38, 0])
    k_lab = T("K+ channel", size=26, color=K_COL, weight=BOLD).move_to([k_x, 2.38, 0])
    return bilayer, headers, ch_na, ch_k, gauge, na_lab, k_lab, op_na, op_k, vm, na_x, k_x


PREDICT_QUESTION = "Which ion rushes harder, and which way does Vm move?"
PREDICT_CARD_KW = {"y": -3.08, "max_w": 10.6, "size": 28}


class S06PredictQ(SpokenScene):
    def construct(self):
        bilayer, headers, ch_na, ch_k, gauge, na_lab, k_lab, op_na, op_k, vm, na_x, k_x = build_predict_world()
        swarm = make_ion_swarm(seed=60, n_na=30, n_k=30)

        self.add(bilayer, headers, ch_na, ch_k, gauge, swarm)
        self.at("two closed channels")
        self.play(Indicate(ch_na, color=NA_COL), Indicate(ch_k, color=K_COL), run_time=0.7)

        self.at("one for sodium")
        self.play(FadeIn(na_lab, shift=DOWN * 0.1), run_time=0.5)

        self.at("one for potassium")
        self.play(FadeIn(k_lab, shift=DOWN * 0.1), run_time=0.5)

        self.at("Pause and predict")
        q = question_card(PREDICT_QUESTION, **PREDICT_CARD_KW)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)

        self.at("open each in turn")
        self.play(Indicate(ch_na, color=NA_COL), run_time=0.7)
        self.at("which ion rushes harder")
        self.play(Indicate(ch_k, color=K_COL), run_time=0.7)
        self.at("does voltage move each time")
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = PREDICT_QUESTION
    CARD = PREDICT_CARD_KW
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        bilayer, headers, ch_na, ch_k, gauge, na_lab, k_lab, *_ = build_predict_world()
        swarm = make_ion_swarm(seed=60, n_na=30, n_k=30)
        swarm.clear_updaters()  # static snapshot of the exact end state; countdown ring animates
        return VGroup(bilayer, headers, ch_na, ch_k, gauge, na_lab, k_lab, swarm)


class S08PredictReveal(SpokenScene):
    def construct(self):
        bilayer, headers, ch_na, ch_k, gauge, na_lab, k_lab, op_na, op_k, vm, na_x, k_x = build_predict_world()

        # Flux computed directly from driving force |Vm - E_ion|
        swarm = make_ion_swarm(
            seed=60, n_na=32, n_k=32,
            pores=[
                (na_x, "na", lambda: op_na.get_value(), lambda: 0.12 * max(0.0, E_NA - vm.get_value())),
                (k_x, "k", lambda: op_k.get_value(), lambda: 0.12 * max(0.0, vm.get_value() - E_K)),
            ],
        )
        self.add(bilayer, headers, ch_na, ch_k, gauge, na_lab, k_lab, swarm)

        self.at("Sodium's gap is huge")
        na_gap_line = Line([GAUGE_X + 0.48, v_to_y(V_REST), 0], [GAUGE_X + 0.48, v_to_y(E_NA), 0], color=NA_COL, stroke_width=8)
        self.play(Create(na_gap_line), op_na.animate.set_value(1.0), run_time=0.7)

        self.at("it pours inward")
        self.at("voltage shoots upward")
        self.play(vm.animate.set_value(42.0), FadeOut(na_gap_line), run_time=1.0, rate_func=rush_from)

        self.at("positive charge in")
        plus_tag = boxed_label("+ charge enters", NA_COL, size=24, pad=0.12).move_to([na_x, -2.20, 0])
        self.play(FadeIn(plus_tag), run_time=0.5)

        self.at("that is depolarization")
        depol_tag = boxed_label("Depolarisation", NA_COL, size=28, pad=0.16).move_to([-0.5, -3.05, 0])
        self.play(FadeIn(depol_tag, shift=UP * 0.1), run_time=0.6)

        self.at("Now shut sodium")
        self.play(
            op_na.animate.set_value(0.0),
            FadeOut(plus_tag),
            FadeOut(depol_tag),
            vm.animate.set_value(V_REST),
            run_time=1.0,
        )

        self.at("open potassium")
        k_gap_line = Line([GAUGE_X + 0.48, v_to_y(V_REST), 0], [GAUGE_X + 0.48, v_to_y(E_K), 0], color=K_COL, stroke_width=8)
        self.play(op_k.animate.set_value(1.0), Create(k_gap_line), run_time=0.7)

        self.at("Its gap is small")
        self.at("potassium leaks out gently")
        leak_tag = boxed_label("+ charge leaks out", K_COL, size=24, pad=0.12).move_to([k_x, -2.20, 0])
        self.play(FadeIn(leak_tag), run_time=0.6)

        self.at("nudges the voltage")
        self.play(vm.animate.set_value(-85.0), FadeOut(k_gap_line), run_time=1.5, rate_func=smooth)
        self.finish()


class S09SingleChannel(SpokenScene):
    def construct(self):
        # Top half: zoomed membrane patch with glass pipette sealed over one channel
        pore_x = -2.0
        patch_y = 1.35
        op = ValueTracker(0.0)
        sig_level = ValueTracker(0.22)  # open probability: 0.22 (Weak) -> 0.78 (Strong)
        open_pct = ValueTracker(22.0)

        # Membrane patch around y = 1.35
        patch_l = RoundedRectangle(corner_radius=0.06, width=3.2, height=0.50, stroke_color=MEM_COL, stroke_width=3.5, fill_color=MEM_COL, fill_opacity=0.22).move_to([pore_x - 2.15, patch_y, 0])
        patch_r = RoundedRectangle(corner_radius=0.06, width=3.2, height=0.50, stroke_color=MEM_COL, stroke_width=3.5, fill_color=MEM_COL, fill_opacity=0.22).move_to([pore_x + 2.15, patch_y, 0])
        chan = build_channel(pore_x, color=NA_COL, open_tracker=op, y=patch_y)

        # Glass pipette cone sealing onto the membrane patch
        pip_left = Line([pore_x - 1.25, 3.35, 0], [pore_x - 0.72, patch_y + 0.25, 0], color=VOLT_COL, stroke_width=4)
        pip_right = Line([pore_x + 1.25, 3.35, 0], [pore_x + 0.72, patch_y + 0.25, 0], color=VOLT_COL, stroke_width=4)
        pip_fill = Polygon(
            [pore_x - 1.25, 3.35, 0], [pore_x + 1.25, 3.35, 0],
            [pore_x + 0.72, patch_y + 0.25, 0], [pore_x - 0.72, patch_y + 0.25, 0],
            stroke_width=0, fill_color=MEM_COL, fill_opacity=0.10,
        )
        pip_lab = T("Patch pipette", size=26, color=VOLT_COL).move_to([pore_x - 2.45, 2.75, 0])
        pipette = VGroup(pip_fill, pip_left, pip_right)

        # Signal slider & live open-time readout on upper right (clear of patch)
        slider_x0, slider_x1, slider_y = 2.0, 5.2, 2.15
        slider_track = Line([slider_x0, slider_y, 0], [slider_x1, slider_y, 0], color=STRUCT_COL, stroke_width=8)
        slider_title = T("Signal strength", size=26, color=VOLT_COL).move_to([3.6, 2.75, 0])
        weak_lab = T("Weak", size=22, color=STRUCT_COL).next_to([slider_x0, slider_y, 0], DOWN, buff=0.20)
        strong_lab = T("Strong", size=22, color=NA_COL).next_to([slider_x1, slider_y, 0], DOWN, buff=0.20)
        knob = always_redraw(lambda: Dot(
            [slider_x0 + np.clip((sig_level.get_value() - 0.22) / 0.56, 0.0, 1.0) * (slider_x1 - slider_x0), slider_y, 0],
            radius=0.15, color=NA_COL,
        ))
        open_ro = counter("Open time: {:.0f}%", open_pct, at=[3.6, 1.15, 0], size=28, color=GREEN)
        controls = VGroup(slider_track, slider_title, weak_lab, strong_lab, knob, open_ro)

        # Bottom half: live scrolling single-channel current Plot (schematic), leaving right edge clear for step-height callout
        trace_plot = Plot(
            box=(-5.0, 4.15, -2.55, -0.35),
            xr=(0.0, 10.0), yr=(-0.15, 1.25),
            xticks=[], yticks=[(0.0, "Closed"), (1.0, "Open")],
            xlabel="time", ylabel="Single-channel current (schematic)",
            color=STRUCT_COL, size=24, label_size=24,
        )

        # Computed 2-state Markov simulation with fixed seed
        rng = np.random.default_rng(42)
        n_hist = 180
        trace_vals = np.zeros(n_hist, dtype=float)
        state = {"open": 0, "accum": 0.0}
        step_dt = 0.05

        # Bursting ions inside pipette that shoot down through pore whenever state["open"] == 1
        n_burst = 14
        ion_pos = np.column_stack([
            rng.uniform(pore_x - 0.50, pore_x + 0.50, n_burst),
            rng.uniform(patch_y + 0.45, 3.05, n_burst),
        ])
        ion_cross = np.zeros(n_burst, dtype=bool)
        ion_dots = VGroup(*[Dot([p[0], p[1], 0], radius=0.085, color=NA_COL) for p in ion_pos])

        def sim_step(mob, dt):
            dt = min(dt, 0.06)
            state["accum"] += dt
            p_target = float(sig_level.get_value())
            while state["accum"] >= step_dt:
                state["accum"] -= step_dt
                # Markov switch rates set so stationary P(open) == p_target
                k_close = 5.5 * (1.0 - p_target)
                k_open = 5.5 * p_target
                if state["open"] == 1:
                    if rng.random() < k_close * step_dt:
                        state["open"] = 0
                else:
                    if rng.random() < k_open * step_dt:
                        state["open"] = 1
                trace_vals[:-1] = trace_vals[1:]
                trace_vals[-1] = float(state["open"])

            op.set_value(float(state["open"]))
            open_pct.set_value(100.0 * float(np.mean(trace_vals[-35:])))

            for i in range(n_burst):
                if ion_cross[i]:
                    ion_pos[i, 1] -= 3.2 * dt
                    ion_pos[i, 0] += (pore_x - ion_pos[i, 0]) * min(1.0, 10.0 * dt)
                    if ion_pos[i, 1] < patch_y - 0.95:
                        ion_cross[i] = False
                        ion_pos[i] = [rng.uniform(pore_x - 0.55, pore_x + 0.55), rng.uniform(patch_y + 0.65, 3.05)]
                else:
                    ion_pos[i] += rng.normal(0.0, 0.35 * dt, 2)
                    ion_pos[i, 0] = np.clip(ion_pos[i, 0], pore_x - 0.60, pore_x + 0.60)
                    ion_pos[i, 1] = np.clip(ion_pos[i, 1], patch_y + 0.40, 3.10)
                    if state["open"] == 1 and rng.random() < 4.5 * dt:
                        ion_cross[i] = True
                        ion_pos[i] = [pore_x + rng.uniform(-0.12, 0.12), patch_y + 0.25]
                ion_dots[i].move_to([ion_pos[i, 0], ion_pos[i, 1], 0.0])

        def mk_trace():
            xs = np.linspace(0.0, 10.0, n_hist)
            pts = []
            for j in range(n_hist):
                if j > 0:
                    pts.append(trace_plot.pt(xs[j], trace_vals[j - 1]))
                pts.append(trace_plot.pt(xs[j], trace_vals[j]))
            m = VMobject(stroke_color=NA_COL, stroke_width=4, fill_opacity=0)
            m.set_points_as_corners(pts)
            return m

        live_trace = always_redraw(mk_trace)
        open_ref = trace_plot.hline(1.0, color=GREEN, dashed=True)

        self.add(patch_l, patch_r, chan, ion_dots)
        self.at("A glass pipette")
        self.play(FadeIn(pipette), FadeIn(pip_lab), run_time=0.8)

        self.at("the patch clamp")
        self.play(Create(trace_plot), FadeIn(open_ref), run_time=0.8)
        self.add(live_trace)
        ion_dots.add_updater(sim_step)

        self.at("one channel at a time")
        self.wait(1.0)

        self.at("The current jumps")
        self.at("at a fixed height")
        y0_sc = trace_plot.pt(10.0, 0.0)[1]
        y1_sc = trace_plot.pt(10.0, 1.0)[1]
        height_brace = Line([4.45, y0_sc, 0], [4.45, y1_sc, 0], color=GREEN, stroke_width=6)
        height_lab = T("Fixed step", size=24, color=GREEN).next_to(height_brace, RIGHT, buff=0.14)
        self.play(Create(height_brace), FadeIn(height_lab), run_time=0.7)

        self.at("A stronger signal")
        self.play(FadeIn(controls), run_time=0.6)
        self.at("does not widen")
        self.play(sig_level.animate.set_value(0.50), run_time=1.8, rate_func=linear)

        self.at("raises the share of time")
        self.play(sig_level.animate.set_value(0.78), run_time=2.0, rate_func=linear)
        self.finish()


class S10Closing(SpokenScene):
    def construct(self):
        pore_x = -0.5
        op = ValueTracker(0.0)
        vm = ValueTracker(V_REST)
        multi_mode = {"on": False}

        bilayer = build_bilayer(gaps=(pore_x,))
        headers = build_compartment_headers()
        chan = build_channel(pore_x, color=MEM_COL, open_tracker=op)
        gauge = build_gauge(vm, show_e_na=True, show_e_k=True)

        def na_rate():
            if op.get_value() < 0.5:
                return 0.0
            return 5.0 if multi_mode["on"] else 3.0

        def k_rate():
            if op.get_value() < 0.5 or not multi_mode["on"]:
                return 0.0
            return 5.0

        swarm = make_ion_swarm(
            seed=70, n_na=30, n_k=30,
            pores=[
                (pore_x, "na", lambda: op.get_value(), na_rate),
                (pore_x, "k", lambda: op.get_value() if multi_mode["on"] else 0.0, k_rate),
            ],
        )

        # Live bulk concentration meters (virtually flat near 100%)
        na_bulk = ValueTracker(100.0)
        k_bulk = ValueTracker(100.0)
        meters = Readout(
            [
                ("Bulk Na+ out", lambda: na_bulk.get_value(), "{:6.2f}%", NA_COL),
                ("Bulk K+ in", lambda: k_bulk.get_value(), "{:6.2f}%", K_COL),
            ],
            at=[-1.0, -2.92, 0], size=24, widest=[100.00, 100.00], color=STRUCT_COL,
        )

        self.add(bilayer, headers, chan, gauge, swarm)

        self.at("Few ions need to cross")
        self.play(op.animate.set_value(1.0), run_time=0.35)
        self.play(vm.animate.set_value(28.0), na_bulk.animate.set_value(99.99), run_time=1.8, rate_func=rush_from)
        self.play(op.animate.set_value(0.0), run_time=0.3)

        self.at("large voltage")
        self.wait(0.4)

        self.at("Bulk concentrations barely shift")
        self.play(FadeIn(meters, shift=UP * 0.1), run_time=0.6)

        self.at("nothing new is made")
        self.wait(0.8)

        self.at("A channel passing several ions")
        multi_mode["on"] = True
        multi_lab = boxed_label("Multi-ion channel", MEM_COL, size=26, pad=0.14).move_to([pore_x, 2.75, 0])
        self.play(FadeOut(meters), FadeIn(multi_lab, shift=DOWN * 0.1), op.animate.set_value(1.0), run_time=0.7)

        self.at("between their equilibrium potentials")
        target_y = v_to_y(-5.0)
        target_mark = Line([GAUGE_X - 0.15, target_y, 0], [GAUGE_X + 0.38, target_y, 0], color=GREEN, stroke_width=5)
        target_lab = T("target", size=22, color=GREEN).move_to([GAUGE_X + 0.95, target_y, 0])
        self.play(vm.animate.set_value(-5.0), FadeIn(target_mark), FadeIn(target_lab), run_time=1.4)

        self.at("Spend the stored gradient")
        self.at("fast signal")
        self.wait(1.0)
        self.finish()


class S11End(EndCard):
    LINE = "An open channel pulls membrane voltage toward its ion’s equilibrium potential."
