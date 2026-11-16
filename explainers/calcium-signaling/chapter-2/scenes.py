"""How One Ion Carries Different Messages — calcium-signaling chapter 2.

COLOUR MAP (one colour per concept, reused across all scenes):
    CA_COLOR      = TEAL (#3FB8C0)   calcium ions, local plumes, spreading wave front
    ER_COLOR      = #A78BFA          endoplasmic reticulum (ER) membrane & internal store
    CHANNEL_COLOR = #F0C445          gold calcium-release channels
    PUMP_COLOR    = #F06A78          coral calcium pumps returning ions to the ER
    BUFFER_COLOR  = #5E9EFF          blue cytosolic calcium buffers
    SENSOR_COLOR  = GREEN (#83C167)  two-lobed calcium sensors & baseline reader state
    OUTPUT_COLOR  = #FF7A2F          orange active sensor output surface / accumulated activity
    TRACE_COLOR   = TEXT (#E8EAF0)   white calcium spike traces over time
    CELL_COLOR    = GREY (#8B93A1)   plasma membrane boundary (structural lines only; no grey text)

WORLD CARRIED THROUGH THE FILM:
    One cell with a purple ER store, gold release channels, coral pumps, blue buffers, and
    identical green two-lobed sensors. It zooms into one channel for local signaling (s03-s06),
    zooms back out for a spreading ER wave across three channels (s07), straightens the wave
    into horizontal time axes (s08-s09), compares all three patterns side by side (s10), and
    merges back into the whole cell (s11).

WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
    s01_hook    : Gold channel gates slide apart and seeded Brownian/advective calcium ions
                  (rng(1)) stream into the cytosol toward two sensors as question marks grow.
    s03_local   : Computed 1/(1+(r/lam)^2) plume and Brownian ions (rng(7)) expand from one
                  pore, blue buffers capture ions, coral pump removes ions, and schematic bars
                  track computed [Ca2+] at near vs far sensors.
    s04_predict : Channel opens briefly and computed plume stops short of both sensors below a
                  shared dashed threshold line while ions drift gently.
    s06_reveal  : Computed plume completes to the near sensor only; near bar crosses threshold
                  while far bar stays below; near two-lobed sensor binds ions, swings open
                  via angle tracker, and exposes an orange output tab.
    s07_global  : Computed traveling wave front (wave_x tracker) sweeps across the ER, opening
                  three gold channels sequentially and activating green sensors behind it.
    s08_time    : ER wave straightens into two time plots; identical computed alpha-pulse trains
                  drive green reader bars via a leaky-integrator ODE (dA/dt = a*Ca*(1-A) - b*A).
    s09_memory  : Computed leaky-integrator ODE continues across wide vs close spike trains;
                  upper green bar falls to baseline while lower bar builds into a tall orange bar.
    s10_rule    : Three live carried panels (plume particles, wave front, ODE spike reader) run
                  side by side with distinct orange output patterns, then merge into one cell.
    s11_close   : Three gold channels open in a computed spatial and rhythmic sequence, driving
                  distinct orange output rhythms on two green sensors before channels close.
"""
import numpy as np
from bp_parts import *

# ------------------------------------------------------------------ Colour map
CA_COLOR = TEAL          # #3FB8C0
ER_COLOR = "#A78BFA"     # purple ER
CHANNEL_COLOR = "#F0C445"  # gold channels
PUMP_COLOR = "#F06A78"   # coral pumps
BUFFER_COLOR = "#5E9EFF" # blue buffers
SENSOR_COLOR = GREEN     # #83C167
OUTPUT_COLOR = "#FF7A2F" # orange active output
TRACE_COLOR = TEXT       # #E8EAF0 white traces
CELL_COLOR = GREY        # #8B93A1 plasma membrane outline

# ------------------------------------------------------------------ Physics & ODE models
def plume_conc(dist, reach=1.0, lam=2.9):
    """Normalized schematic concentration profile falling off smoothly with distance from pore."""
    if reach <= 1e-4:
        return 0.04
    eff_lam = lam * reach
    return float(np.clip(0.04 + 0.94 / (1.0 + (dist / eff_lam) ** 2.2), 0.04, 0.98))


def _alpha_train(t_arr, spike_times, tau_p=0.28):
    ca = np.zeros_like(t_arr, dtype=float)
    for tk in spike_times:
        u = t_arr - tk
        m = u >= 0.0
        ca[m] += (u[m] / tau_p) * np.exp(1.0 - u[m] / tau_p)
    return np.clip(ca, 0.0, 1.05)


def _solve_reader_ode(t_arr, ca_arr, k_on=2.6, k_off=0.38):
    a = np.zeros_like(t_arr, dtype=float)
    for i in range(1, len(t_arr)):
        dt = t_arr[i] - t_arr[i - 1]
        da = k_on * ca_arr[i - 1] * (1.0 - a[i - 1]) - k_off * a[i - 1]
        a[i] = float(np.clip(a[i - 1] + da * dt, 0.0, 1.0))
    return a


T_GRID = np.linspace(0.0, 20.0, 2001)
WIDE_SPIKES = [1.5, 8.5, 15.5]
CLOSE_SPIKES = [1.5, 3.3, 5.1, 6.9, 8.7, 10.5, 12.3, 14.1, 15.9, 17.7, 19.3]
CA_WIDE_GRID = _alpha_train(T_GRID, WIDE_SPIKES)
CA_CLOSE_GRID = _alpha_train(T_GRID, CLOSE_SPIKES)
ACT_WIDE_GRID = _solve_reader_ode(T_GRID, CA_WIDE_GRID)
ACT_CLOSE_GRID = _solve_reader_ode(T_GRID, CA_CLOSE_GRID)


def ca_wide_fn(t):
    return float(np.interp(t, T_GRID, CA_WIDE_GRID))


def ca_close_fn(t):
    return float(np.interp(t, T_GRID, CA_CLOSE_GRID))


def act_wide_fn(t):
    return float(np.interp(t, T_GRID, ACT_WIDE_GRID))


def act_close_fn(t):
    return float(np.interp(t, T_GRID, ACT_CLOSE_GRID))


# ------------------------------------------------------------------ Shared biological parts
def make_channel(pos, open_tracker=None, open_val=0.0, scale=1.0, horizontal=False):
    """Gold two-leaflet channel pore that physically slides open as tracker goes 0 -> 1."""
    c = np.array(pos, dtype=float)

    def build():
        op = open_tracker.get_value() if open_tracker is not None else open_val
        op = float(np.clip(op, 0.0, 1.0))
        gap = (0.04 + 0.26 * op) * scale
        if horizontal:
            # Membrane runs horizontally; leaflets separate along x
            w, h = 0.24 * scale, 0.44 * scale
            l1 = RoundedRectangle(corner_radius=0.06 * scale, width=w, height=h,
                                  color=CHANNEL_COLOR, stroke_width=2.5 * scale,
                                  fill_color=CHANNEL_COLOR, fill_opacity=0.85).move_to(c + LEFT * (gap + w / 2))
            l2 = RoundedRectangle(corner_radius=0.06 * scale, width=w, height=h,
                                  color=CHANNEL_COLOR, stroke_width=2.5 * scale,
                                  fill_color=CHANNEL_COLOR, fill_opacity=0.85).move_to(c + RIGHT * (gap + w / 2))
        else:
            # Membrane runs vertically; leaflets separate along y
            w, h = 0.44 * scale, 0.24 * scale
            l1 = RoundedRectangle(corner_radius=0.06 * scale, width=w, height=h,
                                  color=CHANNEL_COLOR, stroke_width=2.5 * scale,
                                  fill_color=CHANNEL_COLOR, fill_opacity=0.85).move_to(c + UP * (gap + h / 2))
            l2 = RoundedRectangle(corner_radius=0.06 * scale, width=w, height=h,
                                  color=CHANNEL_COLOR, stroke_width=2.5 * scale,
                                  fill_color=CHANNEL_COLOR, fill_opacity=0.85).move_to(c + DOWN * (gap + h / 2))
        return VGroup(l1, l2)

    return always_redraw(build) if open_tracker is not None else build()


def make_pump(pos, scale=1.0, direction=LEFT):
    """Coral pump on the ER membrane with an arrow showing return into the store."""
    c = np.array(pos, dtype=float)
    body = RoundedRectangle(corner_radius=0.10 * scale, width=0.46 * scale, height=0.52 * scale,
                            color=PUMP_COLOR, stroke_width=2.5 * scale,
                            fill_color=PUMP_COLOR, fill_opacity=0.35).move_to(c)
    arr = Arrow(c - direction * 0.22 * scale, c + direction * 0.22 * scale,
                buff=0, stroke_width=3.5 * scale, max_tip_length_to_length_ratio=0.45,
                color=PUMP_COLOR)
    return VGroup(body, arr)


def make_buffer(pos, scale=1.0):
    """Blue cup-shaped cytosolic calcium buffer."""
    c = np.array(pos, dtype=float)
    cup = Arc(radius=0.22 * scale, start_angle=0.35 * PI, angle=1.3 * PI,
              arc_center=c, stroke_color=BUFFER_COLOR, stroke_width=5.5 * scale)
    rim = Circle(radius=0.22 * scale, stroke_opacity=0, fill_color=BUFFER_COLOR,
                 fill_opacity=0.18).move_to(c)
    return VGroup(rim, cup)


def make_sensor(pos, act_tracker=None, act_val=0.0, scale=1.0):
    """Green two-lobed cartoon sensor; swings lobes open and exposes an orange output tab."""
    c = np.array(pos, dtype=float)

    def build():
        val = act_tracker.get_value() if act_tracker is not None else act_val
        val = float(np.clip(val, 0.0, 1.0))
        hinge = c + DOWN * 0.34 * scale
        stem = Line(hinge + DOWN * 0.14 * scale, hinge, color=SENSOR_COLOR, stroke_width=6 * scale)

        # Two lobes pivot open from +/- 12 deg to +/- 44 deg
        swing = (12.0 + 32.0 * val) * DEGREES
        lobe_w, lobe_h = 0.34 * scale, 0.72 * scale
        left_lobe = RoundedRectangle(corner_radius=0.16 * scale, width=lobe_w, height=lobe_h,
                                     color=SENSOR_COLOR, stroke_width=3 * scale,
                                     fill_color=SENSOR_COLOR, fill_opacity=0.32)
        left_lobe.move_to(hinge + UP * (lobe_h * 0.52) + LEFT * (0.14 * scale))
        left_lobe.rotate(swing, about_point=hinge)

        right_lobe = RoundedRectangle(corner_radius=0.16 * scale, width=lobe_w, height=lobe_h,
                                      color=SENSOR_COLOR, stroke_width=3 * scale,
                                      fill_color=SENSOR_COLOR, fill_opacity=0.32)
        right_lobe.move_to(hinge + UP * (lobe_h * 0.52) + RIGHT * (0.14 * scale))
        right_lobe.rotate(-swing, about_point=hinge)

        parts = [stem, left_lobe, right_lobe]

        # Bound teal calcium ions appear in the pockets as sensor binds calcium
        if val > 0.15:
            ion_op = float(np.clip((val - 0.15) / 0.35, 0.0, 1.0))
            d1 = Dot(left_lobe.get_center() + RIGHT * 0.05 * scale, radius=0.075 * scale,
                     color=CA_COLOR).set_opacity(ion_op)
            d2 = Dot(right_lobe.get_center() + LEFT * 0.05 * scale, radius=0.075 * scale,
                     color=CA_COLOR).set_opacity(ion_op)
            parts.extend([d1, d2])

        # Orange output tab emerges from the opened cleft
        if val > 0.30:
            out_frac = float(np.clip((val - 0.30) / 0.70, 0.0, 1.0))
            tab_h = (0.12 + 0.40 * out_frac) * scale
            tab = RoundedRectangle(corner_radius=0.10 * scale, width=0.28 * scale, height=tab_h,
                                   color=OUTPUT_COLOR, stroke_width=2.5 * scale,
                                   fill_color=OUTPUT_COLOR, fill_opacity=0.92)
            tab.move_to(hinge + UP * (0.38 * scale + tab_h / 2))
            parts.append(tab)

        return VGroup(*parts)

    return always_redraw(build) if act_tracker is not None else build()


def make_plume_field(origin, reach_tracker, max_rx=5.5, max_ry=2.2, layers=10):
    """Layered translucent teal plume whose extent and brightness fall off rightward from pore."""
    o = np.array(origin, dtype=float)

    def build():
        reach = float(np.clip(reach_tracker.get_value(), 0.0, 1.0))
        g = VGroup()
        if reach <= 0.02:
            return g
        for i in range(layers, 0, -1):
            frac = i / layers
            rx = max(0.18, max_rx * reach * frac)
            ry = max(0.15, max_ry * (0.35 + 0.65 * reach) * frac)
            # Concentration decays outward; keep ellipse strictly right of pore
            alpha = 0.045 + 0.14 * ((1.0 - frac) ** 1.6) * min(1.0, reach * 1.4)
            ell = Ellipse(width=2 * rx, height=2 * ry, stroke_width=0,
                          fill_color=CA_COLOR, fill_opacity=alpha)
            ell.move_to(o + RIGHT * (rx * 0.94))
            ell.layout_ok = True
            g.add(ell)
        return g

    return always_redraw(build)


def make_bar(x, y_bottom, height, width, val_tracker, color=CA_COLOR, dynamic_orange=False,
             thresh_orange=0.45):
    """Vertical schematic bar driven by a ValueTracker (0..1)."""
    frame = Rectangle(width=width, height=height, color=GREY, stroke_width=2.5,
                      fill_color=BG, fill_opacity=0.5)
    frame.move_to([x, y_bottom + height / 2, 0])

    def build_fill():
        v = float(np.clip(val_tracker.get_value(), 0.02, 1.0))
        h = max(0.03, height * v)
        col = color
        if dynamic_orange and v > thresh_orange:
            t = float(np.clip((v - thresh_orange) / (0.85 - thresh_orange), 0.0, 1.0))
            col = interpolate_color(ManimColor(color), ManimColor(OUTPUT_COLOR), t)
        rect = Rectangle(width=width - 0.06, height=h, stroke_width=0,
                         fill_color=col, fill_opacity=0.88)
        rect.move_to([x, y_bottom + h / 2 + 0.02, 0])
        return rect

    return VGroup(frame, always_redraw(build_fill))


def make_calcium_swarm(n_ions, bounds, seed=7, speed=0.85, source=None, open_tracker=None,
                       buffers=(), capture_tracker=None, pump_pos=None, pump_tracker=None,
                       radius=0.075):
    """Computed Brownian/advective calcium ion swarm with optional buffer capture and pump uptake."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = bounds
    dots = VGroup()
    state = []
    buf_pts = [np.array(b, dtype=float) for b in buffers]
    buf_taken = [False] * len(buf_pts)

    for i in range(n_ions):
        if source is not None:
            sx, sy = source[0] - 0.25 - rng.uniform(0.1, 0.9), source[1] + rng.uniform(-0.8, 0.8)
        else:
            sx, sy = rng.uniform(x0 + 0.2, x1 - 0.2), rng.uniform(y0 + 0.2, y1 - 0.2)
        d = Dot([sx, sy, 0], radius=radius, color=CA_COLOR)
        d.layout_ok = True
        dots.add(d)
        state.append({
            "pos": np.array([sx, sy, 0.0]),
            "vel": rng.normal(0, 0.35, 3) * np.array([1, 1, 0]),
            "mode": "lumen" if source is not None and i >= 4 else "free",
            "buf_idx": -1,
        })

    def update_swarm(mob, dt):
        dt = min(dt, 0.05)
        is_open = open_tracker.get_value() > 0.25 if open_tracker is not None else True
        do_cap = capture_tracker.get_value() > 0.5 if capture_tracker is not None else False
        do_pump = pump_tracker.get_value() > 0.5 if pump_tracker is not None else False

        for idx, (d, st) in enumerate(zip(mob, state)):
            p = st["pos"]
            if st["mode"] == "bound":
                # Gentle vibration inside buffer pocket
                bp = buf_pts[st["buf_idx"]]
                p = bp + np.array([0.02 * np.sin(mob._t * 3 + idx), 0.02 * np.cos(mob._t * 2.5 + idx), 0])
                d.move_to(p)
                continue

            if st["mode"] == "lumen":
                if source is not None and is_open and rng.random() < 1.8 * dt:
                    st["mode"] = "free"
                    st["pos"] = np.array([source[0] + 0.08, source[1] + rng.uniform(-0.08, 0.08), 0.0])
                    st["vel"] = np.array([rng.uniform(1.1, 2.2), rng.uniform(-0.9, 0.9), 0.0])
                else:
                    # Gentle lumen drift left of source[0]
                    jitter = rng.normal(0, 0.45, 3) * np.array([1, 1, 0])
                    st["vel"] = 0.85 * st["vel"] + jitter * dt * 8
                    p = p + st["vel"] * dt * speed
                    if source is not None:
                        p[0] = float(np.clip(p[0], x0 - 1.4, source[0] - 0.22))
                    p[1] = float(np.clip(p[1], y0 + 0.2, min(y1 - 0.2, 1.35)))
                    st["pos"] = p
                    d.move_to(p)
                continue

            # Free cytosolic Brownian + advective motion
            jitter = rng.normal(0, 1.35, 3) * np.array([1, 1, 0])
            st["vel"] = 0.90 * st["vel"] + jitter * np.sqrt(dt)
            if source is not None and is_open and p[0] < source[0] + 1.8:
                st["vel"][0] += 0.7 * dt
            if do_pump and pump_pos is not None:
                vec = np.array(pump_pos, dtype=float) - p
                dist = np.linalg.norm(vec[:2])
                if dist < 1.8 and dist > 0.05:
                    st["vel"] += (vec / dist) * 2.2 * dt
                if dist < 0.28 and source is not None:
                    st["mode"] = "lumen"
                    st["pos"] = np.array([source[0] - 0.45, pump_pos[1] + rng.uniform(-0.2, 0.2), 0.0])
                    d.move_to(st["pos"])
                    continue

            p = p + st["vel"] * dt * speed
            if p[0] < x0:
                p[0] = x0
                st["vel"][0] = abs(st["vel"][0])
            elif p[0] > x1:
                if source is not None and is_open:
                    st["mode"] = "lumen"
                    p = np.array([source[0] - 0.4, source[1] + rng.uniform(-0.5, 0.5), 0.0])
                else:
                    p[0] = x1
                    st["vel"][0] = -abs(st["vel"][0])
            if p[1] < y0:
                p[1] = y0
                st["vel"][1] = abs(st["vel"][1])
            elif p[1] > y1:
                p[1] = y1
                st["vel"][1] = -abs(st["vel"][1])

            if do_cap and buf_pts:
                for bi, bp in enumerate(buf_pts):
                    if not buf_taken[bi] and np.linalg.norm(p[:2] - bp[:2]) < 0.52:
                        buf_taken[bi] = True
                        st["mode"] = "bound"
                        st["buf_idx"] = bi
                        p = bp.copy()
                        break

            st["pos"] = p
            d.move_to(p)

        mob._t += dt

    dots._t = 0.0
    dots.add_updater(update_swarm)
    return dots


# ------------------------------------------------------------------ World builders
def build_full_cell(ch_open=(0.0, 0.0, 0.0), sens_vals=(0.0, 0.0), dim_backdrop=False):
    """Build the carried full-cell picture (plasma membrane, purple ER, channels, pump, buffers, sensors)."""
    op = 0.30 if dim_backdrop else 1.0
    fill_op = 0.07 if dim_backdrop else 0.14

    cell = RoundedRectangle(corner_radius=1.3, width=11.8, height=5.8,
                            stroke_color=CELL_COLOR, stroke_width=3.5,
                            fill_color="#141923", fill_opacity=0.65 * op).move_to([0, -0.1, 0])
    er = RoundedRectangle(corner_radius=0.65, width=4.0, height=3.8,
                          stroke_color=ER_COLOR, stroke_width=3.5,
                          fill_color=ER_COLOR, fill_opacity=fill_op).move_to([-3.2, -0.1, 0])
    er.set_stroke(opacity=op)

    ch_pos = [-1.2, 0.9, 0]
    ch1 = make_channel(ch_pos, open_val=ch_open[0], scale=0.95)
    pump = make_pump([-1.2, -1.0, 0], scale=0.95, direction=LEFT)

    buf_coords = [[0.7, 1.3, 0], [1.4, -0.9, 0], [2.6, 0.5, 0]]
    buffers = VGroup(*[make_buffer(c, scale=0.85) for c in buf_coords])

    near_s = make_sensor([-0.15, 0.9, 0], act_val=sens_vals[0], scale=0.85)
    far_s = make_sensor([4.2, 0.2, 0], act_val=sens_vals[1], scale=0.85)

    if dim_backdrop:
        for m in (ch1, pump, buffers, near_s, far_s):
            for sm in m.family_members_with_points():
                sm.set_stroke(opacity=sm.get_stroke_opacity() * op)
                sm.set_fill(opacity=sm.get_fill_opacity() * op)

    return VGroup(cell, er, ch1, pump, buffers, near_s, far_s), {
        "cell": cell, "er": er, "ch_pos": ch_pos, "near_pos": [-0.15, 0.9, 0],
        "far_pos": [4.2, 0.2, 0], "buf_coords": buf_coords, "pump_pos": [-1.2, -1.0, 0],
        "near_s": near_s, "far_s": far_s, "ch1": ch1,
    }


def build_zoomed_stage(ch_open=0.0, near_act=0.0, far_act=0.0, plume_reach=0.0,
                       near_bar_v=0.04, far_bar_v=0.04, show_threshold=False,
                       with_trackers=True):
    """Build the zoomed-in single-channel stage shared by s03, s04, s05, s06."""
    # ER lumen on the left: x in [-6.3, -4.5], cytosol x in [-4.5, 6.2]
    er_lumen = Rectangle(width=1.8, height=4.8, stroke_width=0,
                         fill_color=ER_COLOR, fill_opacity=0.18).move_to([-5.4, 0.0, 0])
    er_wall = Line([-4.5, -2.4, 0], [-4.5, 2.4, 0], color=ER_COLOR, stroke_width=5)
    er_top = Line([-6.3, 2.4, 0], [-4.5, 2.4, 0], color=ER_COLOR, stroke_width=5)
    er_bot = Line([-6.3, -2.4, 0], [-4.5, -2.4, 0], color=ER_COLOR, stroke_width=5)
    er_lbl = T("ER", 26, ER_COLOR, weight=BOLD).move_to([-5.4, 1.9, 0])

    tr = {}
    if with_trackers:
        tr["open"] = ValueTracker(ch_open)
        tr["plume"] = ValueTracker(plume_reach)
        tr["near_act"] = ValueTracker(near_act)
        tr["far_act"] = ValueTracker(far_act)
        tr["near_bar"] = ValueTracker(near_bar_v)
        tr["far_bar"] = ValueTracker(far_bar_v)
        tr["capture"] = ValueTracker(0.0)
        tr["pump"] = ValueTracker(0.0)
    else:
        tr = None

    ch_pos = [-4.5, 0.85, 0]
    pump_pos = [-4.5, -1.15, 0]
    channel = make_channel(ch_pos, open_tracker=tr["open"] if tr else None, open_val=ch_open, scale=1.15)
    pump = make_pump(pump_pos, scale=1.05, direction=LEFT)

    plume = make_plume_field(ch_pos, tr["plume"]) if tr else VGroup()
    if not tr and plume_reach > 0.02:
        plume = make_plume_field(ch_pos, ValueTracker(plume_reach))

    buf_coords = [[-1.1, 1.65, 0], [-0.4, 0.15, 0], [1.1, 1.25, 0], [1.9, 0.25, 0], [2.9, 1.55, 0]]
    buffers = VGroup(*[make_buffer(c, scale=0.9) for c in buf_coords])

    near_pos = [-2.65, 0.85, 0]
    far_pos = [4.35, 0.85, 0]
    near_s = make_sensor(near_pos, act_tracker=tr["near_act"] if tr else None, act_val=near_act, scale=0.95)
    far_s = make_sensor(far_pos, act_tracker=tr["far_act"] if tr else None, act_val=far_act, scale=0.95)

    # Schematic concentration bars below each sensor
    bar_y0, bar_h, bar_w = -2.25, 1.85, 0.68
    near_bar = make_bar(near_pos[0], bar_y0, bar_h, bar_w, tr["near_bar"] if tr else ValueTracker(near_bar_v))
    far_bar = make_bar(far_pos[0], bar_y0, bar_h, bar_w, tr["far_bar"] if tr else ValueTracker(far_bar_v))

    thresh_y = bar_y0 + 0.44 * bar_h
    thresh_line = DashedLine([-3.55, thresh_y, 0], [5.25, thresh_y, 0],
                             color=CHANNEL_COLOR, stroke_width=3.5, dash_length=0.18)
    thresh_lbl = T("THRESHOLD (schematic)", 24, CHANNEL_COLOR, weight=BOLD).move_to([0.85, thresh_y + 0.30, 0])

    g = VGroup(er_lumen, er_wall, er_top, er_bot, er_lbl, plume, buffers, channel, pump,
               near_s, far_s, near_bar, far_bar)
    if show_threshold:
        g.add(thresh_line, thresh_lbl)

    info = {
        "ch_pos": ch_pos, "pump_pos": pump_pos, "buf_coords": buf_coords,
        "near_pos": near_pos, "far_pos": far_pos, "near_bar": near_bar, "far_bar": far_bar,
        "thresh_line": thresh_line, "thresh_lbl": thresh_lbl, "thresh_y": thresh_y,
        "channel": channel, "pump": pump, "buffers": buffers, "near_s": near_s, "far_s": far_s,
    }
    return g, tr, info


# ------------------------------------------------------------------ Scene 1: Hook
class S01Hook(SpokenScene):
    def construct(self):
        op_tr = ValueTracker(0.0)
        cell_bg, info = build_full_cell(ch_open=(0.0, 0.0, 0.0), sens_vals=(0.0, 0.0))
        # Replace static channel with live-opening channel
        ch1 = make_channel(info["ch_pos"], open_tracker=op_tr, scale=0.95)
        cell_bg.remove(info["ch1"])
        cell_bg.add(ch1)

        swarm = make_calcium_swarm(
            32, bounds=(-1.0, 5.5, -2.5, 2.3), seed=1, speed=0.95,
            source=info["ch_pos"], open_tracker=op_tr,
            buffers=info["buf_coords"], pump_pos=info["pump_pos"],
            pump_tracker=ValueTracker(1.0), radius=0.075,
        )

        # Highlighted ion drifting toward the two sensors
        probe_ion = Dot(info["ch_pos"], radius=0.11, color=CA_COLOR).set_opacity(0)
        probe_ring = Circle(radius=0.18, color=CHANNEL_COLOR, stroke_width=2.5).move_to(info["ch_pos"]).set_opacity(0)
        probe_ring.layout_ok = True

        q1 = T("?", 46, CHANNEL_COLOR, weight=BOLD).next_to(info["near_s"], UP, buff=0.38)
        q2 = T("?", 46, CHANNEL_COLOR, weight=BOLD).next_to(info["far_s"], UP, buff=0.38)
        q1.layout_ok = "contrast"
        q2.layout_ok = "contrast"

        er_lbl = T("ER", 26, ER_COLOR, weight=BOLD).move_to([-4.3, 1.2, 0])
        s1_lbl = T("sensor", 26, SENSOR_COLOR).move_to([info["near_pos"][0], info["near_pos"][1] - 1.02, 0])
        s2_lbl = T("sensor", 26, SENSOR_COLOR).next_to(info["far_s"], DOWN, buff=0.22)

        self.add(cell_bg, er_lbl, s1_lbl, s2_lbl, swarm, probe_ion, probe_ring)

        self.at("the first film")
        self.play(op_tr.animate.set_value(1.0), run_time=0.9)

        self.at("how can that")
        probe_ion.move_to(info["ch_pos"]).set_opacity(1)
        probe_ring.move_to(info["ch_pos"]).set_opacity(1)
        self.play(
            probe_ion.animate.move_to(np.array(info["near_pos"]) + UP * 0.6),
            probe_ring.animate.move_to(np.array(info["near_pos"]) + UP * 0.6),
            GrowFromCenter(q1),
            run_time=1.3,
        )
        self.play(
            probe_ion.animate.move_to(np.array(info["far_pos"]) + UP * 0.6),
            probe_ring.animate.move_to(np.array(info["far_pos"]) + UP * 0.6),
            GrowFromCenter(q2),
            run_time=1.5,
        )

        self.at("a cell cannot")
        self.play(FadeOut(probe_ring), FadeOut(probe_ion), run_time=0.5)

        self.at("instead it controls")
        where_ring = Circle(radius=0.58, color=CA_COLOR, stroke_width=3.5).move_to(info["near_pos"])
        where_lbl = T("where", 28, CA_COLOR, weight=BOLD).next_to(where_ring, DOWN, buff=0.18)
        self.play(FadeOut(s1_lbl, run_time=0.25))
        self.play(Create(where_ring), FadeIn(where_lbl), run_time=0.7)

        self.at("and when and")
        when_lbl = T("when & how often", 28, CHANNEL_COLOR, weight=BOLD).move_to([1.8, -2.15, 0])
        self.play(op_tr.animate.set_value(0.05), FadeIn(when_lbl), run_time=0.5)
        self.play(op_tr.animate.set_value(1.0), run_time=0.45)
        self.play(op_tr.animate.set_value(0.1), run_time=0.45)
        self.play(op_tr.animate.set_value(1.0), run_time=0.45)
        self.finish()


# ------------------------------------------------------------------ Scene 2: Title (1.5 s silent)
class S02Title(NarratedScene):
    def construct(self):
        cell_bg, info = build_full_cell(ch_open=(1.0, 0.0, 0.0), sens_vals=(0.0, 0.0), dim_backdrop=True)
        # Dimmed backdrop is intentionally behind the opaque title card
        cell_bg.layout_ok = True
        swarm = make_calcium_swarm(
            24, bounds=(-1.0, 5.5, -2.5, 2.3), seed=2, speed=0.55,
            source=info["ch_pos"], open_tracker=ValueTracker(0.8),
            radius=0.07,
        )
        for sm in swarm.family_members_with_points():
            sm.set_fill(opacity=0.40)
        swarm.layout_ok = True
        q1 = T("?", 46, CHANNEL_COLOR, weight=BOLD).next_to(info["near_s"], UP, buff=0.38)
        q2 = T("?", 46, CHANNEL_COLOR, weight=BOLD).next_to(info["far_s"], UP, buff=0.38)
        q1.layout_ok = "contrast"
        q2.layout_ok = "contrast"
        qs = VGroup(q1, q2)

        lesson = T("CALCIUM: THE MESSENGER KEPT AT ARM'S LENGTH", size=24, color=CA_COLOR, weight=BOLD)
        title = T("How One Ion Carries Different Messages", size=44, font=TITLE_FONT, color=TEXT)
        fit(title, max_w=10.4)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        inner = VGroup(lesson, title, rule).arrange(DOWN, buff=0.28).move_to(ORIGIN)
        title_box = SurroundingRectangle(inner, corner_radius=0.2, buff=0.34,
                                         stroke_color=GOLD, stroke_width=2.5,
                                         fill_color=BG, fill_opacity=0.95)
        card = VGroup(title_box, inner).set_z_index(10)

        self.add(cell_bg, swarm, qs)
        self.play(FadeOut(qs, run_time=0.25))
        self.play(FadeIn(card), run_time=0.55)
        self.wait(0.70)
        self.finish()


# ------------------------------------------------------------------ Scene 3: Local domain
class S03Local(SpokenScene):
    def construct(self):
        stage, tr, info = build_zoomed_stage(ch_open=0.0, plume_reach=0.0, near_bar_v=0.04, far_bar_v=0.04)
        swarm = make_calcium_swarm(
            42, bounds=(-4.3, 5.9, -2.3, 2.3), seed=7, speed=1.0,
            source=info["ch_pos"], open_tracker=tr["open"],
            buffers=info["buf_coords"], capture_tracker=tr["capture"],
            pump_pos=info["pump_pos"], pump_tracker=tr["pump"], radius=0.075,
        )
        # Tie concentration bars directly to the computed plume_conc(distance)
        info["near_bar"][1].clear_updaters()
        info["far_bar"][1].clear_updaters()

        def bar_updater(bar_tracker, dist):
            def u(m):
                v = plume_conc(dist, reach=tr["plume"].get_value())
                bar_tracker.set_value(v)
            return u

        driver = VMobject()
        driver.add_updater(lambda m: tr["near_bar"].set_value(
            plume_conc(abs(info["near_pos"][0] - info["ch_pos"][0]), reach=tr["plume"].get_value())))
        driver.add_updater(lambda m: tr["far_bar"].set_value(
            plume_conc(abs(info["far_pos"][0] - info["ch_pos"][0]), reach=tr["plume"].get_value())))

        # Re-attach bar fill redraws cleanly
        bar_y0, bar_h, bar_w = -2.25, 1.85, 0.68
        near_fill = make_bar(info["near_pos"][0], bar_y0, bar_h, bar_w, tr["near_bar"])[1]
        far_fill = make_bar(info["far_pos"][0], bar_y0, bar_h, bar_w, tr["far_bar"])[1]
        stage.remove(info["near_bar"], info["far_bar"])
        near_frame = Rectangle(width=bar_w, height=bar_h, color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.5).move_to([info["near_pos"][0], bar_y0 + bar_h / 2, 0])
        far_frame = Rectangle(width=bar_w, height=bar_h, color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.5).move_to([info["far_pos"][0], bar_y0 + bar_h / 2, 0])
        stage.add(near_frame, near_fill, far_frame, far_fill)

        ch_lbl = T("gold channel", 28, CHANNEL_COLOR).move_to([-4.5, 2.85, 0])
        plume_lbl = T("plume (schematic)", 28, CA_COLOR).move_to([-0.75, 2.85, 0])
        near_lbl = T("near sensor", 28, SENSOR_COLOR).move_to([info["near_pos"][0], -2.68, 0])
        far_lbl = T("far sensor", 28, SENSOR_COLOR).move_to([info["far_pos"][0], -2.68, 0])
        buf_lbl = T("buffers", 26, BUFFER_COLOR).move_to([2.95, 2.85, 0])
        pump_lbl = T("pump", 26, PUMP_COLOR).move_to([-5.4, -1.78, 0])
        stag = scope_tag("schematic")

        self.add(stage, driver, swarm, stag)

        self.at("open one gold")
        self.play(tr["open"].animate.set_value(1.0), FadeIn(ch_lbl), run_time=0.8)

        self.at("calcium is highest")
        self.play(tr["plume"].animate.set_value(0.55), run_time=1.8)

        self.at("before buffers capture")
        tr["capture"].set_value(1.0)
        self.play(FadeIn(buf_lbl), run_time=0.6)

        self.at("and pumps remove")
        tr["pump"].set_value(1.0)
        self.play(FadeIn(pump_lbl), run_time=0.6)

        self.at("the teal plume")
        self.play(tr["plume"].animate.set_value(1.0), FadeIn(plume_lbl), run_time=1.6)

        self.at("a sensor anchored")
        self.play(FadeIn(near_lbl), run_time=0.7)

        self.at("an identical sensor")
        self.play(FadeIn(far_lbl), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ Scene 4: Predict
def _predict_backdrop_parts():
    """Shared builder for s04_predict and s05_pause."""
    stage, tr, info = build_zoomed_stage(ch_open=0.0, plume_reach=0.0, near_bar_v=0.04,
                                         far_bar_v=0.04, show_threshold=True)
    near_lbl = T("near sensor", 28, SENSOR_COLOR).move_to([info["near_pos"][0], -2.68, 0])
    far_lbl = T("far sensor", 28, SENSOR_COLOR).move_to([info["far_pos"][0], -2.68, 0])
    q = fit_text("Which sensor responds?", max_w=10.5, size=32, color=GOLD, weight=BOLD).move_to([0.0, 3.30, 0])
    chips = VGroup(
        chip("beside the pore", TEXT, 26),
        chip("across the cell", TEXT, 26),
        chip("both", TEXT, 26),
    ).arrange(RIGHT, buff=0.38).move_to([0.0, 2.62, 0])
    stag = scope_tag("schematic").move_to([4.15, -3.28, 0])
    return stage, tr, info, near_lbl, far_lbl, q, chips, stag


class S04Predict(SpokenScene):
    def construct(self):
        stage, tr, info, near_lbl, far_lbl, q, chips, stag = _predict_backdrop_parts()
        # Hide threshold initially; reveal on cue
        info["thresh_line"].set_opacity(0)
        info["thresh_lbl"].set_opacity(0)

        swarm = make_calcium_swarm(
            26, bounds=(-4.3, 5.9, -2.2, 2.1), seed=11, speed=0.55,
            source=info["ch_pos"], open_tracker=tr["open"], radius=0.075,
        )
        driver = VMobject()
        driver.add_updater(lambda m: tr["near_bar"].set_value(
            plume_conc(abs(info["near_pos"][0] - info["ch_pos"][0]), reach=tr["plume"].get_value())))
        driver.add_updater(lambda m: tr["far_bar"].set_value(
            plume_conc(abs(info["far_pos"][0] - info["ch_pos"][0]), reach=tr["plume"].get_value())))

        self.add(stage, driver, near_lbl, far_lbl, swarm, stag)

        self.at("predict before")
        self.wait(0.3)

        self.at("both sensors switch")
        self.play(info["thresh_line"].animate.set_opacity(1), info["thresh_lbl"].animate.set_opacity(1), run_time=0.9)

        self.at("the channel opens")
        self.play(tr["open"].animate.set_value(1.0), tr["plume"].animate.set_value(0.28), run_time=1.0)
        self.play(tr["open"].animate.set_value(0.0), run_time=0.8)

        self.at("which sensor responds")
        self.play(FadeIn(q), FadeIn(chips), run_time=0.9)

        self.at("follow the fading")
        self.play(tr["plume"].animate.set_value(0.34), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ Scene 5: Pause (4.5 s silent)
class S05Pause(PredictPause):
    QUESTION = ""
    OPTIONS = ()
    RING_AT = (6.0, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        stage, tr, info, near_lbl, far_lbl, q, chips, stag = _predict_backdrop_parts()
        tr["plume"].set_value(0.34)
        tr["near_bar"].set_value(plume_conc(abs(info["near_pos"][0] - info["ch_pos"][0]), reach=0.34))
        tr["far_bar"].set_value(plume_conc(abs(info["far_pos"][0] - info["ch_pos"][0]), reach=0.34))
        swarm = make_calcium_swarm(
            26, bounds=(-4.3, 5.9, -2.2, 2.1), seed=11, speed=0.45,
            source=info["ch_pos"], open_tracker=ValueTracker(0.0), radius=0.075,
        )
        return VGroup(stage, near_lbl, far_lbl, q, chips, stag, swarm)

    def construct(self):
        self.add(self.backdrop())
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


# ------------------------------------------------------------------ Scene 6: Reveal
class S06Reveal(SpokenScene):
    def construct(self):
        stage, tr, info, near_lbl, far_lbl, q, chips, _ = _predict_backdrop_parts()
        tr["plume"].set_value(0.34)
        tr["open"].set_value(0.85)
        stag = scope_tag("schematic")

        swarm = make_calcium_swarm(
            38, bounds=(-4.3, 5.9, -2.2, 2.1), seed=13, speed=0.85,
            source=info["ch_pos"], open_tracker=tr["open"],
            buffers=info["buf_coords"], capture_tracker=tr["capture"],
            pump_pos=info["pump_pos"], pump_tracker=tr["pump"], radius=0.075,
        )
        tr["capture"].set_value(1.0)
        tr["pump"].set_value(1.0)

        driver = VMobject()
        driver.add_updater(lambda m: tr["near_bar"].set_value(
            plume_conc(abs(info["near_pos"][0] - info["ch_pos"][0]), reach=tr["plume"].get_value())))
        driver.add_updater(lambda m: tr["far_bar"].set_value(
            plume_conc(abs(info["far_pos"][0] - info["ch_pos"][0]), reach=tr["plume"].get_value())))

        head_ans = T("only the nearby sensor responds", 30, OUTPUT_COLOR, weight=BOLD).move_to([0.0, 3.25, 0])
        out_lbl = T("orange output surface", 26, OUTPUT_COLOR, weight=BOLD).move_to([-2.05, 2.35, 0])
        far_state = T("stays neutral", 26, SENSOR_COLOR).move_to([4.35, 2.25, 0])

        self.add(stage, driver, near_lbl, far_lbl, q, chips, stag, swarm)

        self.at("only the nearby")
        self.play(FadeOut(q), FadeOut(chips), run_time=0.25)
        self.play(
            FadeIn(head_ans),
            tr["open"].animate.set_value(1.0),
            tr["plume"].animate.set_value(1.0),
            run_time=1.3,
        )

        self.at("calcium beside the")
        # Emphasize near bar crossing threshold
        near_cross = T("above threshold", 24, CA_COLOR, weight=BOLD).move_to([-2.65, -3.08, 0])
        self.play(FadeIn(near_cross), run_time=0.6)

        self.at("the lower level")
        far_low = T("below threshold", 24, TEXT).move_to([3.55, -3.08, 0])
        self.play(FadeIn(far_low), FadeIn(far_state), run_time=0.6)

        self.at("the near sensor")
        self.play(tr["near_act"].animate.set_value(0.28), run_time=0.8)

        self.at("changes shape")
        self.play(tr["near_act"].animate.set_value(0.60), run_time=0.7)

        self.at("and exposes an")
        self.play(tr["near_act"].animate.set_value(1.0), FadeIn(out_lbl), run_time=0.9)

        self.at("location has selected")
        loc_note = T("same calcium, same sensor — different place", 28, TEXT).move_to([-0.5, -3.25, 0])
        self.play(FadeOut(near_cross), FadeOut(far_low), run_time=0.25)
        self.play(FadeIn(loc_note), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 7: Global wave (positive feedback)
class S07Global(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=1.2, width=12.0, height=5.8,
                                stroke_color=CELL_COLOR, stroke_width=3.5,
                                fill_color="#141923", fill_opacity=0.65).move_to([0, -0.1, 0])
        er = RoundedRectangle(corner_radius=0.5, width=9.6, height=1.5,
                              stroke_color=ER_COLOR, stroke_width=3.5,
                              fill_color=ER_COLOR, fill_opacity=0.16).move_to([-0.2, -1.65, 0])
        er_lbl = T("ER", 26, ER_COLOR, weight=BOLD).move_to([-4.4, -1.65, 0])

        ch_xs = [-3.4, -0.4, 2.6]
        ch_y = -0.90
        ch_ops = [ValueTracker(0.0) for _ in ch_xs]
        channels = VGroup(*[make_channel([x, ch_y, 0], open_tracker=op, scale=0.95, horizontal=True)
                            for x, op in zip(ch_xs, ch_ops)])

        sens_coords = [[-3.4, 1.05, 0], [-1.5, 1.45, 0], [0.4, 0.95, 0], [2.4, 1.45, 0], [4.3, 0.85, 0]]
        sens_acts = [ValueTracker(0.0) for _ in sens_coords]
        sensors = VGroup(*[make_sensor(c, act_tracker=a, scale=0.88) for c, a in zip(sens_coords, sens_acts)])

        wave_x = ValueTracker(-5.2)

        def build_wave():
            wx = wave_x.get_value()
            g = VGroup()
            if wx < -4.8:
                return g
            for k, w in enumerate((2.4, 1.5, 0.85)):
                band = RoundedRectangle(corner_radius=0.35, width=w, height=3.4,
                                        stroke_width=0, fill_color=CA_COLOR,
                                        fill_opacity=0.10 + 0.08 * k).move_to([wx, 0.65, 0])
                band.layout_ok = True
                g.add(band)
            return g

        wave_band = always_redraw(build_wave)

        # Recruitment arcs between channels
        arc12 = CurvedArrow([-3.2, -0.45, 0], [-0.6, -0.45, 0], angle=-0.55,
                            color=CHANNEL_COLOR, stroke_width=3.5)
        arc23 = CurvedArrow([-0.2, -0.45, 0], [2.4, -0.45, 0], angle=-0.55,
                            color=CHANNEL_COLOR, stroke_width=3.5)

        # Active moving teal particles across the cell
        swarm = make_calcium_swarm(
            38, bounds=(-5.5, 5.5, -0.65, 2.4), seed=19, speed=0.95,
            source=[ch_xs[0], ch_y + 0.25, 0], open_tracker=ch_ops[0], radius=0.075,
        )

        # Wave front activates sensors behind it smoothly
        driver = VMobject()

        def wave_drive(m):
            wx = wave_x.get_value()
            for sx, act in zip([c[0] for c in sens_coords], sens_acts):
                target = float(np.clip((wx - sx + 0.6) / 1.1, 0.0, 1.0))
                if target > act.get_value():
                    act.set_value(target)

        driver.add_updater(wave_drive)

        title_pf = T("POSITIVE FEEDBACK", 32, CHANNEL_COLOR, weight=BOLD).move_to([0.0, 3.22, 0])
        band_lbl = T("wave front (schematic)", 26, CA_COLOR).move_to([3.5, 3.22, 0])
        stag = scope_tag("schematic")

        self.add(cell, er, er_lbl, wave_band, channels, sensors, swarm, driver, stag)

        self.at("a local event")
        self.play(ch_ops[0].animate.set_value(1.0), wave_x.animate.set_value(-3.1), run_time=1.3)

        self.at("calcium from one")
        self.play(Create(arc12), wave_x.animate.set_value(-0.4), ch_ops[1].animate.set_value(1.0), run_time=1.8)

        self.at("then the next")
        self.play(Create(arc23), wave_x.animate.set_value(2.6), ch_ops[2].animate.set_value(1.0), run_time=1.6)

        self.at("the moving front")
        self.play(FadeIn(band_lbl), wave_x.animate.set_value(4.9), run_time=3.2)

        self.at("this spreading route")
        self.play(FadeOut(band_lbl, run_time=0.25))
        self.play(FadeIn(title_pf, run_time=0.45))
        self.finish()


# ------------------------------------------------------------------ Scene 8: Distance -> Time
def _make_time_plots(t_tracker):
    """Shared stacked wide/close pulse-train plots and computed reader bars for s08 & s09."""
    p_top = Plot(box=(-5.7, 2.3, 0.55, 2.45), xr=(0, 20), yr=(0, 1.18),
                 xticks=(), yticks=(), color=GREY, stroke=3)
    p_bot = Plot(box=(-5.7, 2.3, -2.45, -0.55), xr=(0, 20), yr=(0, 1.18),
                 xticks=(), yticks=(), xlabel="time", color=GREY, label_size=26, stroke=3)

    top_curve = p_top.live_curve(ca_wide_fn, t_tracker, color=TRACE_COLOR, width=4.5)
    bot_curve = p_bot.live_curve(ca_close_fn, t_tracker, color=TRACE_COLOR, width=4.5)
    top_dot = p_top.dot(lambda: t_tracker.get_value(), lambda: ca_wide_fn(t_tracker.get_value()),
                        color=CA_COLOR, ring=TRACE_COLOR, radius=0.09)
    bot_dot = p_bot.dot(lambda: t_tracker.get_value(), lambda: ca_close_fn(t_tracker.get_value()),
                        color=CA_COLOR, ring=TRACE_COLOR, radius=0.09)

    act_top_tr = ValueTracker(0.0)
    act_bot_tr = ValueTracker(0.0)
    driver = VMobject()
    driver.add_updater(lambda m: act_top_tr.set_value(act_wide_fn(t_tracker.get_value())))
    driver.add_updater(lambda m: act_bot_tr.set_value(act_close_fn(t_tracker.get_value())))

    bar_top = make_bar(4.3, 0.65, 1.50, 0.9, act_top_tr, color=SENSOR_COLOR, dynamic_orange=False)
    bar_bot = make_bar(4.3, -2.40, 1.85, 0.9, act_bot_tr, color=SENSOR_COLOR, dynamic_orange=True, thresh_orange=0.38)

    lbl_top = T("wide interval", 26, TRACE_COLOR).move_to([-4.3, 2.75, 0])
    lbl_bot = T("close interval", 26, TRACE_COLOR).move_to([-4.3, -0.25, 0])
    r_lbl_top = T("schematic reader activity", 24, SENSOR_COLOR).move_to([4.3, 2.75, 0])
    r_lbl_bot = T("schematic reader activity", 24, SENSOR_COLOR).move_to([4.3, -0.25, 0])

    return {
        "p_top": p_top, "p_bot": p_bot, "top_curve": top_curve, "bot_curve": bot_curve,
        "top_dot": top_dot, "bot_dot": bot_dot, "act_top_tr": act_top_tr, "act_bot_tr": act_bot_tr,
        "driver": driver, "bar_top": bar_top, "bar_bot": bar_bot,
        "lbl_top": lbl_top, "lbl_bot": lbl_bot, "r_lbl_top": r_lbl_top, "r_lbl_bot": r_lbl_bot,
    }


class S08Time(SpokenScene):
    def construct(self):
        # Start with horizontal ER wave band from s07 and straighten into time axes
        wave_strip = RoundedRectangle(corner_radius=0.3, width=9.0, height=1.2,
                                      stroke_color=ER_COLOR, stroke_width=3,
                                      fill_color=CA_COLOR, fill_opacity=0.25).move_to([-1.6, 0.0, 0])
        t_cur = ValueTracker(0.0)
        tp = _make_time_plots(t_cur)
        stag = scope_tag("schematic")

        self.add(wave_strip, stag)

        self.at("now transform distance")
        self.play(ReplacementTransform(wave_strip, VGroup(tp["p_top"], tp["p_bot"])), run_time=1.3)
        self.add(tp["driver"], tp["top_curve"], tp["top_dot"], tp["lbl_top"])

        self.at("one sensor sees")
        self.play(FadeIn(tp["bar_top"]), t_cur.animate(rate_func=linear).set_value(9.5), run_time=4.8)

        self.at("another sees closely")
        self.add(tp["bot_curve"], tp["bot_dot"], tp["lbl_bot"])
        self.play(FadeIn(tp["bar_bot"]), t_cur.animate(rate_func=linear).set_value(15.0), run_time=2.8)

        self.at("both trains can")
        # Highlight identical pulse peak on top and bottom
        pk_top = Circle(radius=0.24, color=CHANNEL_COLOR, stroke_width=3).move_to(tp["p_top"].pt(8.5 + 0.28, 1.0))
        pk_bot = Circle(radius=0.24, color=CHANNEL_COLOR, stroke_width=3).move_to(tp["p_bot"].pt(7.5 + 0.28, 1.0))
        pk_top.layout_ok = True
        pk_bot.layout_ok = True
        self.play(Create(pk_top), Create(pk_bot), t_cur.animate(rate_func=linear).set_value(17.8), run_time=2.2)

        self.at("a reader with")
        self.play(
            FadeOut(pk_top), FadeOut(pk_bot),
            FadeIn(tp["r_lbl_top"]), FadeIn(tp["r_lbl_bot"]),
            t_cur.animate(rate_func=linear).set_value(20.0),
            run_time=2.6,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 9: Biochemical memory
class S09Memory(SpokenScene):
    def construct(self):
        t_cur = ValueTracker(0.0)
        tp = _make_time_plots(t_cur)
        # Re-seed with faint full trace reference behind live cursor sweep
        ref_top = tp["p_top"].curve(ca_wide_fn, color=GREY, width=2.5, opacity=0.45)
        ref_bot = tp["p_bot"].curve(ca_close_fn, color=GREY, width=2.5, opacity=0.45)
        base_line = DashedLine([3.65, 0.70, 0], [4.95, 0.70, 0], color=GREY, stroke_width=2)
        stag = scope_tag("schematic")

        self.add(
            tp["p_top"], tp["p_bot"], ref_top, ref_bot,
            tp["driver"], tp["top_curve"], tp["bot_curve"], tp["top_dot"], tp["bot_dot"],
            tp["bar_top"], tp["bar_bot"], base_line,
            tp["lbl_top"], tp["lbl_bot"], tp["r_lbl_top"], tp["r_lbl_bot"], stag,
        )

        self.at("with long gaps")
        self.play(t_cur.animate(rate_func=linear).set_value(7.8), run_time=4.4)

        self.at("close spikes arrive")
        self.play(t_cur.animate(rate_func=linear).set_value(11.8), run_time=2.6)

        self.at("the responses can")
        self.play(t_cur.animate(rate_func=linear).set_value(16.0), run_time=2.4)

        self.at("calcium has not")
        same_top = Circle(radius=0.22, color=CA_COLOR, stroke_width=3.5).move_to(tp["p_top"].pt(8.78, 1.0))
        same_bot = Circle(radius=0.22, color=CA_COLOR, stroke_width=3.5).move_to(tp["p_bot"].pt(9.78, 1.0))
        same_top.layout_ok = True
        same_bot.layout_ok = True
        self.play(Create(same_top), Create(same_bot), t_cur.animate(rate_func=linear).set_value(18.5), run_time=1.8)

        self.at("timing matters because")
        mem_lbl = T("biochemical memory", 26, OUTPUT_COLOR, weight=BOLD).move_to([4.3, -2.85, 0])
        self.play(FadeOut(same_top), FadeOut(same_bot), FadeIn(mem_lbl),
                  t_cur.animate(rate_func=linear).set_value(20.0), run_time=2.2)
        self.finish()


# ------------------------------------------------------------------ Scene 10: The one rule + merge
class S10Rule(SpokenScene):
    def construct(self):
        pw, ph = 3.92, 4.7
        xs = [-4.22, 0.0, 4.22]
        titles = ["local domain", "spreading wave", "spike timing"]
        cols = [CA_COLOR, CHANNEL_COLOR, OUTPUT_COLOR]
        panels = VGroup()
        heads = VGroup()

        for x, ttl, col in zip(xs, titles, cols):
            fr = RoundedRectangle(corner_radius=0.18, width=pw, height=ph,
                                  stroke_color=col, stroke_width=2.5,
                                  fill_color="#141923", fill_opacity=0.65).move_to([x, -0.15, 0])
            hd = T(ttl, 26, col, weight=BOLD).move_to([x, 1.85, 0])
            panels.add(fr)
            heads.add(hd)

        # Panel 1: local plume + open near sensor
        p1_x = xs[0]
        p1_er = Line([p1_x - 1.55, -1.7, 0], [p1_x - 1.55, 1.2, 0], color=ER_COLOR, stroke_width=4)
        p1_ch = make_channel([p1_x - 1.55, -0.2, 0], open_val=1.0, scale=0.75)
        p1_plume = make_plume_field([p1_x - 1.55, -0.2, 0], ValueTracker(0.75), max_rx=2.1, max_ry=1.1, layers=6)
        p1_s = make_sensor([p1_x - 0.55, -0.2, 0], act_val=1.0, scale=0.72)
        p1_swarm = make_calcium_swarm(14, bounds=(p1_x - 1.45, p1_x + 1.55, -1.65, 1.15), seed=31,
                                      speed=0.7, source=[p1_x - 1.55, -0.2, 0],
                                      open_tracker=ValueTracker(1.0), radius=0.055)
        p1_out = T("local output", 24, OUTPUT_COLOR).move_to([p1_x, -2.05, 0])
        p1_pic = VGroup(p1_er, p1_plume, p1_ch, p1_s, p1_swarm, p1_out)

        # Panel 2: spreading wave across 3 channels + 3 sensors
        p2_x = xs[1]
        p2_er = RoundedRectangle(corner_radius=0.18, width=3.2, height=0.65,
                                 stroke_color=ER_COLOR, stroke_width=3,
                                 fill_color=ER_COLOR, fill_opacity=0.16).move_to([p2_x, -1.25, 0])
        p2_chs = VGroup(*[make_channel([p2_x + dx, -0.92, 0], open_val=1.0, scale=0.58, horizontal=True)
                          for dx in (-1.0, 0.0, 1.0)])
        p2_wave_x = ValueTracker(p2_x - 1.3)
        p2_wave = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.2, width=0.85, height=1.8, stroke_width=0,
            fill_color=CA_COLOR, fill_opacity=0.25).move_to([p2_wave_x.get_value(), 0.25, 0]))
        p2_wave.layout_ok = True
        p2_sens = VGroup(*[make_sensor([p2_x + dx, 0.35, 0], act_val=1.0, scale=0.62)
                           for dx in (-1.0, 0.0, 1.0)])
        p2_out = T("spread output", 24, OUTPUT_COLOR).move_to([p2_x, -2.05, 0])
        p2_pic = VGroup(p2_er, p2_wave, p2_chs, p2_sens, p2_out)

        # Panel 3: close spike train + tall orange reader bar
        p3_x = xs[2]
        p3_t = ValueTracker(0.0)
        p3_plot = Plot(box=(p3_x - 1.55, p3_x + 0.55, -0.65, 1.15), xr=(0, 20), yr=(0, 1.15),
                       xticks=(), yticks=(), color=GREY, stroke=2.5)
        p3_curve = p3_plot.live_curve(ca_close_fn, p3_t, color=TRACE_COLOR, width=3.2)
        p3_act = ValueTracker(0.0)
        p3_drv = VMobject()
        p3_drv.add_updater(lambda m: p3_act.set_value(act_close_fn(p3_t.get_value())))
        p3_bar = make_bar(p3_x + 1.15, -0.65, 1.85, 0.55, p3_act, color=SENSOR_COLOR,
                          dynamic_orange=True, thresh_orange=0.38)
        p3_out = T("built output", 24, OUTPUT_COLOR).move_to([p3_x, -2.05, 0])
        p3_pic = VGroup(p3_plot, p3_curve, p3_drv, p3_bar, p3_out)

        top_head = T("Where and when free calcium rises", 32, TEXT, weight=BOLD).move_to([0.0, 3.05, 0])
        focus_head = T("Place and timing (size matters too)", 30, CHANNEL_COLOR, weight=BOLD).move_to([0.0, 3.05, 0])
        stag = scope_tag("schematic")

        all_three = VGroup(panels, heads, p1_pic, p2_pic, p3_pic)
        self.add(all_three, top_head, stag)

        self.at("cells give calcium")
        self.play(p3_t.animate(rate_func=linear).set_value(6.0), p2_wave_x.animate.set_value(p2_x), run_time=3.5)

        self.at("the size of")
        self.play(FadeOut(top_head), p3_t.animate(rate_func=linear).set_value(6.8), run_time=0.45)
        self.play(FadeIn(focus_head), p3_t.animate(rate_func=linear).set_value(7.6), run_time=0.45)
        self.play(p3_t.animate(rate_func=linear).set_value(11.0), run_time=2.1)

        self.at("local domains favor")
        self.play(panels[0].animate.set_stroke(width=5), p3_t.animate(rate_func=linear).set_value(13.5), run_time=1.8)

        self.at("coordinated release can")
        self.play(panels[0].animate.set_stroke(width=2.5), panels[1].animate.set_stroke(width=5),
                  p2_wave_x.animate.set_value(p2_x + 1.1), p3_t.animate(rate_func=linear).set_value(16.5), run_time=2.0)

        self.at("repeated spikes favor")
        self.play(panels[1].animate.set_stroke(width=2.5), panels[2].animate.set_stroke(width=5),
                  p3_t.animate(rate_func=linear).set_value(20.0), run_time=2.5)

        self.at("cells combine these")
        merged_cell, minfo = build_full_cell(ch_open=(1.0, 0.0, 0.0), sens_vals=(1.0, 0.55))
        merged_lbl = T("one cell, many sensors", 30, TEXT, weight=BOLD).move_to([0.0, 3.15, 0])
        self.play(FadeOut(focus_head), run_time=0.35)
        self.play(ReplacementTransform(all_three, merged_cell), FadeIn(merged_lbl), run_time=1.5)
        self.finish()


# ------------------------------------------------------------------ Scene 11: Close (full cell rhythm)
class S11Close(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=1.3, width=11.8, height=5.8,
                                stroke_color=CELL_COLOR, stroke_width=3.5,
                                fill_color="#141923", fill_opacity=0.65).move_to([0, -0.1, 0])
        er = RoundedRectangle(corner_radius=0.65, width=4.0, height=3.8,
                              stroke_color=ER_COLOR, stroke_width=3.5,
                              fill_color=ER_COLOR, fill_opacity=0.16).move_to([-3.2, -0.1, 0])
        er_lbl = T("ER", 26, ER_COLOR, weight=BOLD).move_to([-4.3, 1.2, 0])

        ch_coords = [[-1.2, 1.1, 0], [-1.2, 0.0, 0], [-1.2, -1.1, 0]]
        ch_ops = [ValueTracker(0.0) for _ in ch_coords]
        channels = VGroup(*[make_channel(c, open_tracker=op, scale=0.85) for c, op in zip(ch_coords, ch_ops)])
        pump = make_pump([-3.2, -2.0, 0], scale=0.9, direction=DOWN)

        buf_coords = [[1.95, 1.55, 0], [1.6, -1.2, 0], [2.7, 0.3, 0]]
        buffers = VGroup(*[make_buffer(c, scale=0.85) for c in buf_coords])

        s_a_act = ValueTracker(0.0)
        s_b_act = ValueTracker(0.0)
        s_a = make_sensor([0.38, 1.1, 0], act_tracker=s_a_act, scale=0.92)
        s_b = make_sensor([4.1, -0.2, 0], act_tracker=s_b_act, scale=0.92)
        s_a_lbl = T("near reader", 26, SENSOR_COLOR).next_to(s_a, DOWN, buff=0.22).set_z_index(5)
        s_b_lbl = T("distant reader", 26, SENSOR_COLOR).next_to(s_b, DOWN, buff=0.22).set_z_index(5)

        swarm = make_calcium_swarm(
            34, bounds=(-1.0, 5.5, -2.5, 2.3), seed=41, speed=0.9,
            source=ch_coords[0], open_tracker=ch_ops[0], radius=0.075,
        )

        head = T("same ion, different patterns", 30, TEXT, weight=BOLD).move_to([0.0, 3.15, 0])

        self.add(cell, er, er_lbl, channels, pump, buffers, s_a, s_b, s_a_lbl, s_b_lbl, swarm, head)

        self.at("the cell therefore")
        self.play(ch_ops[0].animate.set_value(1.0), run_time=0.8)

        self.at("channel position sets")
        self.play(s_a_act.animate.set_value(0.95), run_time=1.0)

        self.at("feedback can enlarge")
        self.play(ch_ops[1].animate.set_value(1.0), run_time=0.6)
        self.play(ch_ops[2].animate.set_value(1.0), s_b_act.animate.set_value(0.75), run_time=1.1)

        self.at("opening and closing")
        # Distinct rhythms: channels pulse open/closed while near and distant sensors follow at different rates
        self.play(ch_ops[0].animate.set_value(0.0), ch_ops[1].animate.set_value(0.0),
                  s_a_act.animate.set_value(0.25), run_time=0.7)
        self.play(ch_ops[0].animate.set_value(1.0), ch_ops[2].animate.set_value(0.0),
                  s_a_act.animate.set_value(1.0), s_b_act.animate.set_value(0.95), run_time=0.8)
        self.play(ch_ops[0].animate.set_value(0.0), ch_ops[1].animate.set_value(1.0),
                  s_a_act.animate.set_value(0.3), run_time=0.7)

        self.at("sensors read only")
        # Settle channels closed and orange outputs gently down before end card
        self.play(
            ch_ops[0].animate.set_value(0.0),
            ch_ops[1].animate.set_value(0.0),
            ch_ops[2].animate.set_value(0.0),
            s_a_act.animate.set_value(0.05),
            s_b_act.animate.set_value(0.15),
            run_time=2.4,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 12: End card
class S12End(EndCard):
    LINE = "Cells give calcium meaning by controlling where and when free calcium rises."
