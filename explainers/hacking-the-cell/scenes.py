"""
Watch It or Push It: Reporters and Actuators
===========================================

COLOUR MAP (one colour per concept across the whole film):
  NEURON     = "#89CFF0"   # ice-blue: the living neuron, soma, dendrites, axon, membrane bilayer
  CALCIUM    = "#F4A261"   # amber: calcium ions (Ca2+) and rushing positive cations (+)
  VOLTAGE    = "#FACC15"   # gold: electrical firing pulse, action potential voltage
  REPORTER   = "#2ECC71"   # emerald green: GFP / GCaMP barrel, glowing center, emitted green photon, GCaMP trace
  ACTUATOR   = "#FB7185"   # coral: channelrhodopsin-2 helices and pore
  RETINAL    = "#C084FC"   # lavender: light-sensing retinal inside channelrhodopsin-2
  GENE       = "#2DD4BF"   # bright teal: engineered protein gene
  BLUE_LIGHT = "#38BDF8"   # sky-blue: blue excitation photon, blue optogenetic light beam
  WATER      = "#BAE6FD"   # pale cyan: water droplets entering or excluded from the GFP barrel
  CALMODULIN = "#3FB8C0"   # teal: calmodulin calcium detector crescent
  PEPTIDE    = "#E8EAF0"   # crisp off-white (TEXT): partner peptide and primary labels
  HEAT       = "#FC6255"   # red: small energy loss as heat in fluorescence
  OTHER      = "#94A3B8"   # muted slate: hypothetical upstream circuit / eye rhodopsin comparison border

ONE WORLD CARRIED:
  One living ice-blue neuron (and the schematic mouse whose left turn it controls), zooming smoothly
  from the whole mouse + neuron, into the cytosol's GFP/GCaMP barrel, back out to the brain circuit,
  into the neuron's membrane with channelrhodopsin-2, and back out to the complete neuron carrying both tools.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s01_hook         : Mouse turns left (0 -> +0.55 rad); golden firing wave travels along computed axon spline;
                     seeded amber calcium dots drift inside soma; Watch? / Test cause? badges appear;
                     propagating green/blue light waves preview optical readout and control.
  s02_two_tools    : Calcium dots enter left barrel -> propagating green photon wave travels outward;
                     propagating blue light wave hits right coral pore -> golden firing pulse enters axon.
  s03_fluorescence : Zoom to emerald GFP barrel; computed blue (shorter lambda) & green (longer lambda = 1/dE)
                     propagating sine waves enter/exit a 3-level energy ladder as the electron dot rises,
                     drops via heat, and emits green light.
  s04_gfp_barrel   : Barrel folds tight around glowing core under propagating blue light; slit opens via
                     ValueTracker; pale-cyan water droplets bounce off sealed wall then slip through slit
                     while core glow dims continuously from 0.95 to 0.18.
  s05_gcamp        : Teal calmodulin and white peptide attach to slit lips; amber Ca2+ spheres enter and bind;
                     calmodulin wraps around peptide to seal slit, water retreats out completely, core glow
                     rises 0.18 -> 1.0 and emits propagating green fluorescence wave.
  s06_predict      : Mouse turns left and brain+GCaMP neuron flashes green across computed bi-exponential
                     GCaMP transients F(t) = sum(exp(-dt/tau_d) - exp(-dt/tau_r)) on Plot; question card slides in.
  s08_reveal       : Upstream "Other circuit?" drives pulses down two dashed arrows to both mouse and neuron;
                     then dims while a propagating blue light beam pushes neuron and turns mouse left.
  s09_chr2         : Lipid bilayer membrane cross-section with 7 coral ChR2 helices built sequentially and
                     gold retinal; temporary Eye rhodopsin -> G protein relay animates then clears cleanly,
                     leaving ChR2's direct central ion pore.
  s10_light_in     : Propagating blue beam bends retinal and swings coral helices wide open; '+' cations
                     stream inward while one ValueTracker drives a computed integrate-and-fire + spike
                     waveform past Threshold, firing the small neuron gold and turning the mouse left.
  s11_wrap         : Full neuron with active GCaMP (left) and ChR2 (right); gene bar above soma sends build
                     arrows to both tools, then take-home rule caption settles below while both tools pulse.
"""

from bp_parts import *

# ------------------------------------------------------------------ concept palette
NEURON = "#89CFF0"
CALCIUM = "#F4A261"
VOLTAGE = "#FACC15"
REPORTER = "#2ECC71"
ACTUATOR = "#FB7185"
BLUE_LIGHT = "#38BDF8"
WATER = "#BAE6FD"
CALMODULIN = TEAL
PEPTIDE = TEXT
HEAT = RED
OTHER = "#94A3B8"
DIM_OLIVE = "#4D6B3C"
RETINAL = "#C084FC"
GENE = "#2DD4BF"


# ------------------------------------------------------------------ shared builders
def make_neuron(center=ORIGIN, scale=1.0, glow=0.0, glow_color=REPORTER):
    """Build the carried ice-blue neuron with soma, dendrites, axon spline, and nucleus."""
    c = np.array([center[0], center[1], 0.0], dtype=float)

    soma_pts = [
        (-0.85, 0.55), (-0.45, 0.95), (0.15, 1.05), (0.72, 0.80),
        (1.05, 0.25), (1.05, -0.25), (0.72, -0.80), (0.15, -1.05),
        (-0.45, -0.95), (-0.85, -0.55), (-1.05, 0.0),
    ]
    soma = Polygon(
        *[np.array([x, y, 0.0]) for x, y in soma_pts],
        stroke_color=NEURON,
        stroke_width=5.2,
        fill_color=NEURON,
        fill_opacity=0.30,
    ).round_corners(0.35)

    soma_glow = Polygon(
        *[np.array([x * 0.90, y * 0.90, 0.0]) for x, y in soma_pts],
        stroke_width=0,
        fill_color=glow_color,
        fill_opacity=float(np.clip(glow, 0.0, 1.0)) * 0.65,
    ).round_corners(0.3)

    nucleus = Circle(radius=0.35, stroke_color=NEURON, stroke_width=2.8, fill_color=NEURON, fill_opacity=0.28)
    nucleus.move_to([-0.05, 0.0, 0.0])

    d_top = VMobject(stroke_color=NEURON, stroke_width=4.5)
    d_top.set_points_smoothly([[-0.65, 0.65, 0], [-1.30, 1.25, 0], [-1.95, 1.80, 0]])
    d_top_b = VMobject(stroke_color=NEURON, stroke_width=3.6)
    d_top_b.set_points_smoothly([[-1.30, 1.25, 0], [-1.20, 1.85, 0]])

    d_mid = VMobject(stroke_color=NEURON, stroke_width=4.6)
    d_mid.set_points_smoothly([[-0.98, 0.05, 0], [-1.75, 0.20, 0], [-2.35, 0.35, 0]])

    d_bot = VMobject(stroke_color=NEURON, stroke_width=4.5)
    d_bot.set_points_smoothly([[-0.65, -0.65, 0], [-1.35, -1.25, 0], [-2.00, -1.75, 0]])
    d_bot_b = VMobject(stroke_color=NEURON, stroke_width=3.6)
    d_bot_b.set_points_smoothly([[-1.35, -1.25, 0], [-1.95, -0.85, 0]])

    axon_pts = [
        np.array([0.95, 0.0, 0.0]),
        np.array([1.75, 0.12, 0.0]),
        np.array([2.55, -0.10, 0.0]),
        np.array([3.35, 0.08, 0.0]),
    ]
    axon = VMobject(stroke_color=NEURON, stroke_width=5.2)
    axon.set_points_smoothly(axon_pts)

    term_up = VMobject(stroke_color=NEURON, stroke_width=4.0)
    term_up.set_points_smoothly([[3.35, 0.08, 0], [3.85, 0.55, 0], [4.15, 0.80, 0]])
    term_dn = VMobject(stroke_color=NEURON, stroke_width=4.0)
    term_dn.set_points_smoothly([[3.35, 0.08, 0], [3.85, -0.45, 0], [4.15, -0.72, 0]])

    g = VGroup(soma, soma_glow, nucleus, d_top, d_top_b, d_mid, d_bot, d_bot_b, axon, term_up, term_dn)
    g.scale(scale).move_to(c + RIGHT * 0.75 * scale)
    g.soma = soma
    g.soma_glow = soma_glow
    g.nucleus = nucleus
    g.axon = axon
    g.soma_center = soma.get_center()
    g.dendrite_pt = d_mid.get_end()
    g.actuator_pt = g.soma_center + np.array([0.78 * scale, 0.55 * scale, 0.0])
    g.reporter_pt = g.soma_center + np.array([-1.45 * scale, 0.22 * scale, 0.0])
    return g


def make_mouse(center=ORIGIN, scale=1.0, angle=0.0):
    """Top-down schematic mouse silhouette facing UP (+Y) when angle=0; +angle turns left."""
    body = Ellipse(width=0.84, height=1.18, stroke_color=TEXT, stroke_width=3.2, fill_color=TEXT, fill_opacity=0.26)
    head = Triangle(stroke_color=TEXT, stroke_width=3.2, fill_color=TEXT, fill_opacity=0.30)
    head.set_height(0.46).set_width(0.56).move_to([0, 0.68, 0])
    ear_l = Circle(radius=0.16, stroke_color=TEXT, stroke_width=2.6, fill_color=TEXT, fill_opacity=0.30).move_to([-0.32, 0.36, 0])
    ear_r = Circle(radius=0.16, stroke_color=TEXT, stroke_width=2.6, fill_color=TEXT, fill_opacity=0.30).move_to([0.32, 0.36, 0])
    nose = Dot([0, 0.93, 0], radius=0.055, color=GOLD)
    tail = VMobject(stroke_color=TEXT, stroke_width=3.0)
    tail.set_points_smoothly([[0, -0.58, 0], [-0.10, -0.92, 0], [0.08, -1.20, 0]])
    g = VGroup(tail, body, ear_l, ear_r, head, nose)
    g.scale(scale).rotate(angle).move_to(center)
    g.nose = nose
    return g


def make_photon_wave(start, end, wavelength=0.45, amp=0.14, color=BLUE_LIGHT, stroke_width=5.6, phase=0.0, opacity=1.0, n_pts=120):
    """Computed transverse sine wave along start -> end with an arrowhead and optional traveling phase."""
    s = np.array([start[0], start[1], 0.0], dtype=float)
    e = np.array([end[0], end[1], 0.0], dtype=float)
    vec = e - s
    length = float(np.linalg.norm(vec))
    u = vec / max(length, 1e-6)
    perp = np.array([-u[1], u[0], 0.0])
    arrow_len = 0.24
    wave_len = max(0.2, length - arrow_len)
    ts = np.linspace(0.0, wave_len, n_pts)
    pts = [s + u * t + perp * (amp * np.sin(TAU * t / wavelength - phase)) for t in ts]
    pts.append(s + u * length)
    wave = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity, fill_opacity=0.0)
    wave.set_points_as_corners(pts)
    tip = Triangle(fill_color=color, fill_opacity=opacity, stroke_width=0).set_height(0.19)
    ang = np.arctan2(u[1], u[0]) - PI / 2
    tip.rotate(ang).move_to(e - u * 0.08)
    return VGroup(wave, tip)


def make_barrel(center=ORIGIN, height=4.4, slit=0.0, glow=1.0, width_scale=1.0):
    """GFP / GCaMP barrel built from curved wall segments + rich emerald body + glowing core."""
    c = np.array([center[0], center[1], 0.0], dtype=float)
    rx = height * 0.39 * width_scale
    ry = height * 0.50

    g_val = float(np.clip(glow, 0.0, 1.0))
    core_color = interpolate_color(ManimColor(DIM_OLIVE), ManimColor(REPORTER), g_val)
    shell_fill = Ellipse(
        width=2.0 * rx * 0.96,
        height=2.0 * ry * 0.96,
        stroke_width=0,
        fill_color=core_color,
        fill_opacity=0.24 + 0.20 * g_val,
    ).move_to(c)
    core_halo = Circle(
        radius=height * (0.20 + 0.14 * g_val),
        stroke_width=0,
        fill_color=core_color,
        fill_opacity=0.30 + 0.44 * g_val,
    ).move_to(c)
    core_dot = Circle(
        radius=height * (0.10 + 0.04 * g_val),
        stroke_color=core_color,
        stroke_width=3.5,
        fill_color=core_color,
        fill_opacity=0.50 + 0.50 * g_val,
    ).move_to(c)

    wall_kw = dict(stroke_color=REPORTER, stroke_width=8.0)
    left_wall = ParametricFunction(
        lambda t: c + np.array([-rx * np.cos(t), ry * np.sin(t), 0.0]),
        t_range=[-PI / 2, PI / 2],
        **wall_kw,
    )

    if slit <= 0.01:
        right_walls = VGroup(
            ParametricFunction(
                lambda t: c + np.array([rx * np.cos(t), ry * np.sin(t), 0.0]),
                t_range=[-PI / 2, PI / 2],
                **wall_kw,
            )
        )
        gap_ang = 0.0
    else:
        gap = 0.34 * slit * ry
        gap_ang = np.arcsin(np.clip(gap / ry, 0.0, 0.55))
        right_bot = ParametricFunction(
            lambda t: c + np.array([rx * np.cos(t), ry * np.sin(t), 0.0]),
            t_range=[-PI / 2, -gap_ang],
            **wall_kw,
        )
        right_top = ParametricFunction(
            lambda t: c + np.array([rx * np.cos(t), ry * np.sin(t), 0.0]),
            t_range=[gap_ang, PI / 2],
            **wall_kw,
        )
        right_walls = VGroup(right_bot, right_top)

    ribs = VGroup()
    for fx in (-0.52, -0.18, 0.18, 0.52):
        y_lim = ry * np.sqrt(max(0.05, 1.0 - fx * fx)) * 0.86
        ribs.add(Line(c + [fx * rx, -y_lim, 0], c + [fx * rx, y_lim, 0], stroke_color=REPORTER, stroke_width=2.5).set_opacity(0.38))

    g = VGroup(shell_fill, core_halo, ribs, core_dot, left_wall, right_walls)
    g.core_center = c
    g.rx = rx
    g.ry = ry
    return g


def make_chr2_channel(center=ORIGIN, scale=1.0, open_frac=0.0, retinal_angle=0.0):
    """7-cylinder channelrhodopsin-2 across a membrane with lavender retinal inside."""
    c = np.array([center[0], center[1], 0.0], dtype=float)
    w_cyl = 0.24 * scale
    h_cyl = 1.90 * scale
    spread = 0.30 * scale
    shift = 0.48 * scale * open_frac

    left_xs = [(-1.55 + 0.15) * spread - shift, (-1.05 + 0.15) * spread - shift, (-0.55 + 0.15) * spread - shift * 0.88, (-0.18 + 0.15) * spread - shift * 0.88]
    right_xs = [(0.22 + 0.15) * spread + shift * 0.88, (0.72 + 0.15) * spread + shift, (1.25 + 0.15) * spread + shift]

    helices = VGroup()
    for i, lx in enumerate(left_xs):
        tilt = 0.18 * open_frac * (1.0 - 0.12 * i)
        r = RoundedRectangle(
            corner_radius=w_cyl * 0.45,
            width=w_cyl,
            height=h_cyl,
            stroke_color=ACTUATOR,
            stroke_width=3.0,
            fill_color=ACTUATOR,
            fill_opacity=0.42 + 0.14 * (i % 2),
        ).move_to(c + [lx, 0, 0]).rotate(tilt)
        helices.add(r)
    for i, rx in enumerate(right_xs):
        tilt = -0.18 * open_frac * (1.0 - 0.12 * i)
        r = RoundedRectangle(
            corner_radius=w_cyl * 0.45,
            width=w_cyl,
            height=h_cyl,
            stroke_color=ACTUATOR,
            stroke_width=3.0,
            fill_color=ACTUATOR,
            fill_opacity=0.42 + 0.14 * (i % 2),
        ).move_to(c + [rx, 0, 0]).rotate(tilt)
        helices.add(r)

    # Shift retinal slightly left into the left helix bundle when pore opens so central pore stays clear
    ret_x = (-0.12 - 0.34 * open_frac) * scale
    retinal = RoundedRectangle(
        corner_radius=0.05 * scale,
        width=0.58 * scale,
        height=0.13 * scale,
        stroke_color=RETINAL,
        stroke_width=2.2,
        fill_color=RETINAL,
        fill_opacity=0.95,
    ).move_to(c + [ret_x, 0.08 * scale, 0]).rotate(0.18 + retinal_angle)

    g = VGroup(helices, retinal)
    g.helices = helices
    g.retinal = retinal
    g.pore_center = c
    return g


def make_membrane(x0=-6.0, x1=6.0, y=0.0, gap_x=None, gap_w=0.9, half_t=0.68):
    """Ice-blue lipid bilayer bars + subtle tail ticks flanking an optional central protein gap."""
    segs = VGroup()
    ticks = VGroup()
    if gap_x is None:
        intervals = [(x0, x1)]
    else:
        gx0, gx1 = gap_x - gap_w / 2, gap_x + gap_w / 2
        intervals = []
        if gx0 > x0 + 0.1:
            intervals.append((x0, gx0))
        if x1 > gx1 + 0.1:
            intervals.append((gx1, x1))

    bands = VGroup()
    for a, b in intervals:
        bands.add(Rectangle(width=b - a, height=2 * half_t, stroke_width=0, fill_color=NEURON, fill_opacity=0.32).move_to([(a + b) / 2, y, 0]))
        for dy in (half_t, -half_t):
            segs.add(Line([a, y + dy, 0], [b, y + dy, 0], stroke_color=NEURON, stroke_width=4.5))
        n_tk = max(2, int((b - a) / 0.35))
        for tx in np.linspace(a + 0.18, b - 0.18, n_tk):
            ticks.add(Line([tx, y + half_t - 0.05, 0], [tx, y + 0.12, 0], stroke_color=NEURON, stroke_width=1.8).set_opacity(0.32))
            ticks.add(Line([tx, y - half_t + 0.05, 0], [tx, y - 0.12, 0], stroke_color=NEURON, stroke_width=1.8).set_opacity(0.32))

    return VGroup(bands, ticks, segs)


def make_cation_plus(pos, radius=0.13):
    """Amber cation sphere with crisp geometric '+' drawn inside (zero glyph-overlap warnings)."""
    c = np.array([pos[0], pos[1], 0.0], dtype=float)
    dot = Circle(radius=radius, stroke_color=TEXT, stroke_width=1.8, fill_color=CALCIUM, fill_opacity=1.0).move_to(c)
    s = radius * 0.55
    h = Line(c + LEFT * s, c + RIGHT * s, stroke_color=BG, stroke_width=3.2)
    v = Line(c + DOWN * s, c + UP * s, stroke_color=BG, stroke_width=3.2)
    return VGroup(dot, h, v)


def gcamp_trace(t, spike_times=(0.6, 3.6), tau_r=0.18, tau_d=1.45):
    """Computed bi-exponential GCaMP fluorescence transient normalized to [0, 1]."""
    val = 0.08
    peak_norm = (tau_r / tau_d) ** (tau_r / (tau_d - tau_r)) - (tau_r / tau_d) ** (tau_d / (tau_d - tau_r))
    for t0 in spike_times:
        dt = t - t0
        if dt > 0:
            val += 0.88 * (np.exp(-dt / tau_d) - np.exp(-dt / tau_r)) / max(peak_norm, 1e-6)
    return float(np.clip(val, 0.0, 1.05))


def voltage_trace(tau):
    """Computed schematic membrane voltage: resting -> depolarization -> threshold spike -> repolarization."""
    t_light = 0.22
    t_thresh = 0.66
    if tau < t_light:
        return 0.16
    if tau < t_thresh:
        frac = (tau - t_light) / (t_thresh - t_light)
        return float(0.16 + 0.34 * (1.0 - np.exp(-2.2 * frac)) / (1.0 - np.exp(-2.2)))
    dt = tau - t_thresh
    if dt < 0.07:
        return float(0.50 + 0.46 * (dt / 0.07))
    if dt < 0.17:
        return float(0.96 - 0.88 * ((dt - 0.07) / 0.10))
    return float(0.08 + 0.08 * min(1.0, (dt - 0.17) / 0.12))


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Hacking the Cell: Reporters, Actuators and Genetic Tools"
    TITLE = "Watch It or Push It: Reporters and Actuators"


class S01Hook(SpokenScene):
    def construct(self):
        fire_glow = ValueTracker(0.0)
        neuron = always_redraw(lambda: make_neuron(center=(0.65, -0.20, 0), scale=1.38, glow=fire_glow.get_value(), glow_color=VOLTAGE))
        mouse_angle = ValueTracker(0.0)
        mouse = always_redraw(lambda: make_mouse(center=(-4.55, 2.25, 0), scale=0.95, angle=mouse_angle.get_value()))
        mouse_lbl = T("Mouse turns left", 26, TEXT).move_to([-4.55, 0.90, 0])

        # Seeded intracellular calcium ions drifting inside the soma
        rng = np.random.default_rng(7)
        ca_base = np.array([[rng.uniform(-0.65, 0.65), rng.uniform(-0.65, 0.65)] for _ in range(10)])
        ca_freq = rng.uniform(1.8, 3.2, size=10)
        ca_phase = rng.uniform(0, TAU, size=10)
        t_clock = ValueTracker(0.0)
        t_clock.add_updater(lambda m, dt: m.increment_value(dt))

        def _ca_dots():
            t = t_clock.get_value()
            sc = neuron.soma_center
            return VGroup(*[
                Dot(
                    sc + [ca_base[i, 0] + 0.18 * np.sin(ca_freq[i] * t + ca_phase[i]),
                          ca_base[i, 1] + 0.18 * np.cos(ca_freq[i] * 0.9 * t + ca_phase[i]), 0.0],
                    radius=0.09, color=CALCIUM,
                )
                for i in range(10)
            ])

        ca_dots = always_redraw(_ca_dots)

        # Action potential pulse travelling along the neuron axon
        pulse_u = ValueTracker(0.0)

        def _pulse():
            u = pulse_u.get_value()
            if u <= 0.001 or u >= 0.999:
                return VGroup()
            pt = neuron.axon.point_from_proportion(float(np.clip(u, 0.0, 1.0)))
            return VGroup(Dot(pt, radius=0.30, color=VOLTAGE).set_opacity(0.40), Dot(pt, radius=0.13, color=VOLTAGE))

        pulse_dot = always_redraw(_pulse)
        self.add(neuron, mouse, t_clock, ca_dots, pulse_dot)

        self.at("mouse turns left")
        self.play(mouse_angle.animate.set_value(0.55), FadeIn(mouse_lbl, run_time=0.45), run_time=0.75)

        self.at("hidden neuron fires")
        self.play(fire_glow.animate.set_value(0.55), pulse_u.animate(rate_func=linear).set_value(1.0), run_time=1.3)
        fire_glow.set_value(0.0)
        pulse_u.set_value(0.0)

        self.at("how can you watch")
        q_watch = boxed_label("Watch?", REPORTER, size=28).move_to([-4.55, -0.55, 0])
        self.play(FadeIn(q_watch, shift=RIGHT * 0.15), run_time=0.45)

        self.at("causes the turn")
        q_push = boxed_label("Test cause?", ACTUATOR, size=28).move_to([-4.55, -1.65, 0])
        self.play(FadeIn(q_push, shift=RIGHT * 0.15), run_time=0.45)

        self.at("signals inside cells")
        self.play(mouse_angle.animate.set_value(0.0), run_time=0.4)
        self.play(
            mouse_angle.animate.set_value(0.55),
            fire_glow.animate.set_value(0.50),
            pulse_u.animate(rate_func=linear).set_value(1.0),
            run_time=1.4,
        )
        fire_glow.set_value(0.0)
        pulse_u.set_value(0.0)

        self.at("engineered proteins")
        ray_on = ValueTracker(0.0)
        # Keep green ray cleanly between Watch? and Mouse turns left, clear of d_mid, labels, and badges
        ray_out = always_redraw(lambda: make_photon_wave(
            np.array([-2.95, 0.30, 0]),
            np.array([-4.55, 0.30, 0]),
            wavelength=0.42, amp=0.11, color=REPORTER, phase=6.5 * t_clock.get_value(), opacity=ray_on.get_value(),
        ))
        ray_in = always_redraw(lambda: make_photon_wave(
            neuron.actuator_pt + UR * 1.45,
            neuron.actuator_pt + UR * 0.24,
            wavelength=0.32, amp=0.10, color=BLUE_LIGHT, phase=7.5 * t_clock.get_value(), opacity=ray_on.get_value(),
        ))
        self.add(ray_out, ray_in)
        self.play(ray_on.animate.set_value(1.0), run_time=0.55)

        self.at("with light")
        self.play(fire_glow.animate.set_value(0.45), pulse_u.animate(rate_func=linear).set_value(1.0), run_time=1.35)
        pulse_u.set_value(0.0)
        self.play(fire_glow.animate.set_value(0.0), pulse_u.animate(rate_func=linear).set_value(1.0), run_time=1.35)
        self.finish()


class S02TwoTools(SpokenScene):
    def construct(self):
        neuron = make_neuron(center=(0.0, -0.2, 0), scale=1.38)
        self.add(neuron)

        rng = np.random.default_rng(11)
        ca_base = np.array([[rng.uniform(-0.50, 0.50), rng.uniform(-0.50, 0.50)] for _ in range(8)])
        t_tr = ValueTracker(0.0)
        t_tr.add_updater(lambda m, dt: m.increment_value(dt))

        ca_dots = always_redraw(lambda: VGroup(*[
            Dot(neuron.soma_center + [ca_base[i, 0] + 0.14 * np.sin(2.4 * t_tr.get_value() + i),
                                      ca_base[i, 1] + 0.14 * np.cos(2.0 * t_tr.get_value() + i), 0],
                radius=0.08, color=CALCIUM)
            for i in range(8)
        ]))
        self.add(t_tr, ca_dots)

        # Left tool: Reporter (signal -> light)
        rep_pos = neuron.dendrite_pt
        rep_barrel = make_barrel(center=rep_pos, height=0.95, slit=0.0, glow=0.9)
        rep_label = T("Reporter:\nsignal to light", 28, REPORTER).move_to([-4.65, 1.85, 0])
        rep_arrow = Arrow(neuron.soma_center + LEFT * 0.72, rep_barrel.get_right() + RIGHT * 0.08, buff=0.06, color=CALCIUM, stroke_width=4.5)
        rep_ray = always_redraw(lambda: make_photon_wave(
            rep_barrel.get_left() + LEFT * 0.12,
            rep_barrel.get_left() + LEFT * 2.10,
            wavelength=0.42, amp=0.12, color=REPORTER, phase=6.5 * t_tr.get_value(),
        ))

        # Right tool: Actuator (command -> signal)
        act_pore = make_chr2_channel(center=neuron.actuator_pt, scale=0.48, open_frac=0.65)
        act_label = T("Actuator:\ncommand to signal", 28, ACTUATOR).move_to([4.50, 2.30, 0])
        act_beam = always_redraw(lambda: make_photon_wave(
            neuron.actuator_pt + UR * 1.65,
            neuron.actuator_pt + UR * 0.35,
            wavelength=0.32, amp=0.11, color=BLUE_LIGHT, phase=7.5 * t_tr.get_value(),
        ))
        act_arrow = Arrow(neuron.actuator_pt + DL * 0.35, neuron.axon.point_from_proportion(0.28), buff=0.08, color=VOLTAGE, stroke_width=4.5)

        self.at("a reporter")
        self.play(FadeIn(rep_barrel), FadeIn(rep_label, run_time=0.45), GrowArrow(rep_arrow), run_time=0.75)

        self.at("into light")
        self.play(FadeIn(rep_ray), run_time=0.55)

        self.at("an actuator")
        self.play(FadeIn(act_pore), FadeIn(act_label, run_time=0.45), run_time=0.75)

        self.at("flash of light")
        self.play(FadeIn(act_beam), run_time=0.55)

        self.at("on command")
        self.play(GrowArrow(act_arrow), run_time=0.6)

        sig_dot = always_redraw(lambda: VGroup(
            Dot(neuron.axon.point_from_proportion((t_tr.get_value() * 0.55) % 1.0), radius=0.22, color=VOLTAGE).set_opacity(0.38),
            Dot(neuron.axon.point_from_proportion((t_tr.get_value() * 0.55) % 1.0), radius=0.10, color=VOLTAGE),
        ))
        self.add(sig_dot)
        self.finish()


class S03Fluorescence(SpokenScene):
    def construct(self):
        wave_t = ValueTracker(0.0)
        wave_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(wave_t)

        barrel_small = make_barrel(center=(-1.5, 0.0, 0), height=1.1, slit=0.0, glow=0.85)
        barrel = always_redraw(lambda: make_barrel(
            center=(-3.4, -0.1, 0), height=5.2, slit=0.0, glow=0.72 + 0.26 * np.sin(3.2 * wave_t.get_value()),
        ))
        b_label = T("GFP barrel", 30, REPORTER).move_to([-3.4, 2.95, 0])

        self.add(barrel_small)
        self.play(Transform(barrel_small, make_barrel(center=(-3.4, -0.1, 0), height=5.2, slit=0.0, glow=0.85)), FadeIn(b_label, run_time=0.5), run_time=1.3)
        self.remove(barrel_small)
        self.add(barrel)

        lx0, lx1 = 1.2, 5.4
        y_ground = -1.65
        y_relax = 1.15
        y_excite = 2.05
        lam_blue = 0.34
        lam_green = lam_blue * (y_excite - y_ground) / (y_relax - y_ground)

        e0 = Line([lx0, y_ground, 0], [lx1, y_ground, 0], color=TEXT, stroke_width=3.5)
        e1 = Line([lx0, y_relax, 0], [lx1, y_relax, 0], color=TEXT, stroke_width=3.5)
        e2 = Line([lx0, y_excite, 0], [lx1, y_excite, 0], color=TEXT, stroke_width=2.5)
        sub1 = DashedLine([lx0 + 0.5, 1.45, 0], [lx1 - 0.5, 1.45, 0], color=OTHER, stroke_width=1.8)
        sub2 = DashedLine([lx0 + 0.5, 1.75, 0], [lx1 - 0.5, 1.75, 0], color=OTHER, stroke_width=1.8)
        ladder_title = T("Energy ladder", 28, TEXT).move_to([3.3, 2.75, 0])
        ladder = VGroup(e0, e1, e2, sub1, sub2, ladder_title)
        tag = scope_tag("schematic")

        e_x = ValueTracker(2.35)
        e_y = ValueTracker(y_ground)
        electron = always_redraw(lambda: Dot([e_x.get_value(), e_y.get_value(), 0], radius=0.13, color=VOLTAGE, stroke_color=TEXT, stroke_width=2.0))

        self.at("how does fluorescence")
        self.play(FadeIn(ladder), FadeIn(electron), FadeIn(tag), run_time=0.8)

        self.at("blue photon")
        blue_wave = always_redraw(lambda: make_photon_wave(
            [0.05, 0.25, 0], [2.15, 0.25, 0], wavelength=lam_blue, amp=0.13, color=BLUE_LIGHT, phase=7.0 * wave_t.get_value(),
        ))
        blue_lbl = T("Blue in", 26, BLUE_LIGHT).move_to([0.95, 0.85, 0])
        self.play(FadeIn(blue_wave), FadeIn(blue_lbl, run_time=0.45), run_time=0.6)

        self.at("lifts an electron")
        up_arrow = Arrow([2.35, y_ground + 0.13, 0], [2.35, y_excite - 0.13, 0], buff=0, color=BLUE_LIGHT, stroke_width=4.0)
        self.play(GrowArrow(up_arrow), e_y.animate.set_value(y_excite), run_time=0.85)

        self.at("leaves as heat")
        heat_wave = VMobject(stroke_color=HEAT, stroke_width=3.8)
        h_ts = np.linspace(0, 1, 40)
        heat_pts = [
            np.array([2.50 + 1.35 * t, y_excite + (y_relax - y_excite) * t + 0.08 * np.sin(3 * TAU * t), 0.0])
            for t in h_ts
        ]
        heat_wave.set_points_as_corners(heat_pts)
        heat_lbl = T("Heat lost", 26, HEAT).move_to([4.15, 2.38, 0])
        self.play(
            Create(heat_wave),
            FadeIn(heat_lbl, run_time=0.45),
            e_x.animate.set_value(3.95),
            e_y.animate.set_value(y_relax),
            run_time=0.95,
        )

        self.at("green photon")
        dn_arrow = Arrow([3.95, y_relax - 0.13, 0], [3.95, y_ground + 0.13, 0], buff=0, color=REPORTER, stroke_width=4.0)
        green_wave = always_redraw(lambda: make_photon_wave(
            [4.15, -0.25, 0], [6.25, -0.25, 0], wavelength=lam_green, amp=0.13, color=REPORTER, phase=5.5 * wave_t.get_value(),
        ))
        green_lbl = T("Green out", 26, REPORTER).move_to([5.20, 0.35, 0])
        self.play(
            GrowArrow(dn_arrow),
            e_y.animate.set_value(y_ground),
            FadeIn(green_wave),
            FadeIn(green_lbl, run_time=0.45),
            run_time=0.95,
        )

        self.at("longer wavelength")
        shorter_lbl = T("shorter", 24, BLUE_LIGHT).move_to([0.95, -0.30, 0])
        longer_lbl = T("longer", 24, REPORTER).move_to([5.20, -0.82, 0])
        self.play(FadeIn(shorter_lbl), FadeIn(longer_lbl), run_time=0.6)
        self.finish()


class S04GfpBarrel(SpokenScene):
    def construct(self):
        slit_tr = ValueTracker(0.0)
        water_in = ValueTracker(0.0)
        glow_tr = ValueTracker(0.95)
        wscale_tr = ValueTracker(1.55)
        wave_t = ValueTracker(0.0)
        wave_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(wave_t)

        barrel = always_redraw(lambda: make_barrel(
            center=(-0.3, -0.1, 0),
            height=5.2,
            slit=slit_tr.get_value(),
            glow=glow_tr.get_value() * (0.85 + 0.15 * np.sin(3.5 * wave_t.get_value())),
            width_scale=wscale_tr.get_value(),
        ))
        title = T("GFP barrel", 30, REPORTER).move_to([-0.3, 2.95, 0])
        self.add(barrel, title)

        # Barrel visibly folds into its tight sealed barrel at start
        self.play(wscale_tr.animate.set_value(1.0), run_time=2.4)

        self.at("shielded inside")
        shield_lbl = T("Glowing core shielded", 26, TEXT).move_to([-4.2, -2.15, 0])
        shield_arr = Arrow(shield_lbl.get_right() + RIGHT * 0.1, [-0.55, -0.35, 0], buff=0.1, color=REPORTER, stroke_width=3.8)
        self.play(FadeIn(shield_lbl, run_time=0.45), GrowArrow(shield_arr), run_time=0.7)

        self.at("under blue light")
        blue_ray = always_redraw(lambda: make_photon_wave(
            [-5.8, 0.65, 0], [-2.15, 0.65, 0], wavelength=0.34, amp=0.13, color=BLUE_LIGHT, phase=7.0 * wave_t.get_value(),
        ))
        blue_lbl = T("Blue light", 28, BLUE_LIGHT).move_to([-4.2, 1.32, 0])

        water_lbl = T("Water", 28, WATER).move_to([3.9, 1.95, 0])
        water_offsets = [-0.52, -0.24, 0.02, 0.28, 0.54]

        def _water_dots():
            t = wave_t.get_value()
            w = water_in.get_value()
            g = VGroup()
            for idx, dy in enumerate(water_offsets):
                phase = (t * 0.58 + idx * 0.21) % 1.0
                x_bounce = 1.95 + 2.6 * abs(2.0 * phase - 1.0)
                x_in = 4.2 - 4.0 * phase
                x = (1.0 - w) * x_bounce + w * x_in
                g.add(Dot([x, -0.1 + dy * 0.65, 0], radius=0.13, color=WATER, stroke_color=TEXT, stroke_width=1.5).set_opacity(0.95))
            return g

        water_dots = always_redraw(_water_dots)
        self.play(
            FadeOut(shield_lbl),
            FadeOut(shield_arr),
            FadeIn(blue_ray),
            FadeIn(blue_lbl, run_time=0.45),
            run_time=0.7,
        )
        self.add(water_dots)

        self.at("cut a narrow slit")
        slit_lbl = T("Narrow slit cut", 28, GOLD).move_to([3.9, -1.85, 0])
        self.play(slit_tr.animate.set_value(1.0), FadeIn(slit_lbl, run_time=0.45), run_time=1.3)

        self.at("water slips through")
        self.play(water_in.animate.set_value(1.0), FadeIn(water_lbl, run_time=0.45), run_time=1.0)

        self.at("dims the glow")
        dim_lbl = T("Water dims the glow", 28, WATER).move_to([3.9, -2.55, 0])
        self.play(glow_tr.animate.set_value(0.18), FadeIn(dim_lbl, run_time=0.45), run_time=1.2)
        self.finish()


class S05Gcamp(SpokenScene):
    def construct(self):
        glow_tr = ValueTracker(0.18)
        wrap_tr = ValueTracker(0.0)
        water_out = ValueTracker(0.0)
        wave_t = ValueTracker(0.0)
        wave_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(wave_t)

        barrel = always_redraw(lambda: make_barrel(
            center=(-0.4, -0.1, 0),
            height=5.2,
            slit=1.0 - 0.35 * wrap_tr.get_value(),
            glow=glow_tr.get_value() * (0.86 + 0.14 * np.sin(3.2 * wave_t.get_value())),
        ))
        b_title = T("GFP barrel", 30, REPORTER).move_to([-0.4, 2.95, 0])
        gcamp_title = T("GCaMP", 32, REPORTER).move_to([-0.4, 2.95, 0])

        # Carried continuous blue excitation light on left
        blue_ray = always_redraw(lambda: make_photon_wave(
            [-5.8, 0.75, 0], [-2.25, 0.75, 0], wavelength=0.34, amp=0.12, color=BLUE_LIGHT, phase=7.0 * wave_t.get_value(),
        ))
        blue_lbl = T("Blue light", 26, BLUE_LIGHT).move_to([-4.2, 1.38, 0])

        # Water droplets inside open slit at start; cleanly pushed out & faded completely to 0 when shut out
        water_offsets = [-0.32, 0.02, 0.34]

        def _water():
            t = wave_t.get_value()
            w = water_out.get_value()
            if w > 0.75:
                return VGroup()
            g = VGroup()
            op = max(0.0, 0.95 * (1.0 - w / 0.75))
            for idx, dy in enumerate(water_offsets):
                base_x = 0.05 + 0.36 * idx + 5.5 * w
                x = base_x + 0.16 * np.sin(2.8 * t + idx)
                g.add(Dot([x, -0.1 + dy, 0], radius=0.12, color=WATER).set_opacity(op))
            return g

        water_dots = always_redraw(_water)
        self.add(barrel, b_title, blue_ray, blue_lbl, water_dots)

        calm_lbl = T("Calmodulin", 28, CALMODULIN).move_to([4.15, 2.05, 0])
        pep_lbl = T("Peptide", 28, PEPTIDE).move_to([4.15, -2.05, 0])

        def _calmodulin():
            w = wrap_tr.get_value()
            c_y = 1.05 - 1.15 * w
            c_x = 1.60 - 0.15 * w
            ang = -0.35 + 1.15 * w
            return AnnularSector(
                inner_radius=0.22,
                outer_radius=0.66,
                angle=PI * (1.15 + 0.48 * w),
                start_angle=PI * 0.25 + ang,
                color=CALMODULIN,
                fill_opacity=0.92,
            ).move_to([c_x, c_y, 0])

        def _peptide():
            w = wrap_tr.get_value()
            p_y = -1.08 + 0.98 * w
            return RoundedRectangle(
                corner_radius=0.09,
                width=0.28,
                height=0.90,
                stroke_color=PEPTIDE,
                stroke_width=2.5,
                fill_color=PEPTIDE,
                fill_opacity=0.90,
            ).move_to([1.45, p_y, 0])

        calm = always_redraw(_calmodulin)
        pep = always_redraw(_peptide)

        self.at("calmodulin")
        self.play(FadeIn(calm), FadeIn(calm_lbl, run_time=0.45), run_time=0.8)

        self.at("partner peptide")
        self.play(FadeIn(pep), FadeIn(pep_lbl, run_time=0.45), run_time=0.8)

        self.at("hybrid sensor")
        self.play(swap(b_title, gcamp_title, run_time=0.5))

        self.at("when calcium enters")
        ca_prog = ValueTracker(0.0)
        ca_starts = np.array([[5.1, 0.75, 0], [5.5, 0.10, 0], [5.0, -0.55, 0]])
        ca_ends = np.array([[1.75, 0.32, 0], [1.82, -0.10, 0], [1.72, -0.52, 0]])
        ca_spheres = always_redraw(lambda: VGroup(*[
            Dot(interpolate(ca_starts[i], ca_ends[i], ca_prog.get_value()), radius=0.13, color=CALCIUM, stroke_color=TEXT, stroke_width=1.5)
            for i in range(3)
        ]))
        ca_lbl = T("Ca²⁺", 28, CALCIUM).move_to([4.15, 1.05, 0])
        self.add(ca_spheres)
        self.play(FadeIn(ca_lbl, run_time=0.45), ca_prog.animate.set_value(1.0), run_time=1.2)

        self.at("wraps around")
        self.play(wrap_tr.animate.set_value(1.0), run_time=1.3)

        self.at("shut water out")
        self.play(water_out.animate.set_value(1.0), run_time=0.95)

        self.at("brighten the barrel")
        green_out = always_redraw(lambda: make_photon_wave(
            [-2.25, -0.85, 0], [-5.8, -0.85, 0], wavelength=0.45, amp=0.13, color=REPORTER, phase=6.0 * wave_t.get_value(),
        ))
        green_lbl = T("Green out", 26, REPORTER).move_to([-4.2, -1.52, 0])
        self.play(glow_tr.animate.set_value(1.0), FadeIn(green_out), FadeIn(green_lbl, run_time=0.45), run_time=0.9)
        self.finish()


def _predict_world(t_val=10.0, mouse_ang=0.55, glow_val=0.45):
    """Rebuild the exact S06 end-state backdrop for S07Pause."""
    brain = RoundedRectangle(corner_radius=1.1, width=5.1, height=3.2, stroke_color=NEURON, stroke_width=2.6, fill_color=NEURON, fill_opacity=0.14)
    brain.move_to([-3.15, -0.35, 0])
    neuron = make_neuron(center=(-3.45, -0.35, 0), scale=0.62, glow=glow_val)
    mouse = make_mouse(center=(-4.7, 2.40, 0), scale=0.68, angle=mouse_ang)
    n_lbl = T("GCaMP neuron", 26, REPORTER).move_to([-3.15, -2.25, 0])

    P = Plot(
        box=(0.7, 5.9, -1.5, 2.1),
        xr=(0, 10.5),
        yr=(0, 1.15),
        xticks=[],
        yticks=[(0, "0")],
        xlabel="time",
        ylabel="GCaMP light (schematic)",
        color=TEXT,
        size=24,
        label_size=26,
    )
    spikes = (0.7, 4.2, 7.6)
    curve = P.curve(lambda x: gcamp_trace(x, spike_times=spikes), x0=0, x1=t_val, color=REPORTER, width=5.5)
    dot = Dot(P.pt(t_val, gcamp_trace(t_val, spike_times=spikes)), radius=0.12, color=REPORTER, stroke_color=TEXT, stroke_width=2.5)
    return VGroup(brain, neuron, mouse, n_lbl, P, curve, dot)


class S06Predict(SpokenScene):
    def construct(self):
        brain = RoundedRectangle(corner_radius=1.1, width=5.1, height=3.2, stroke_color=NEURON, stroke_width=2.6, fill_color=NEURON, fill_opacity=0.14)
        brain.move_to([-3.15, -0.35, 0])
        t_tr = ValueTracker(0.0)
        mouse_ang = ValueTracker(0.0)
        spikes = (0.7, 4.2, 7.6)

        neuron = always_redraw(lambda: make_neuron(
            center=(-3.45, -0.35, 0),
            scale=0.62,
            glow=gcamp_trace(t_tr.get_value(), spike_times=spikes),
        ))
        mouse = always_redraw(lambda: make_mouse(center=(-4.7, 2.40, 0), scale=0.68, angle=mouse_ang.get_value()))
        n_lbl = T("GCaMP neuron", 26, REPORTER).move_to([-3.15, -2.25, 0])

        P = Plot(
            box=(0.7, 5.9, -1.5, 2.1),
            xr=(0, 10.5),
            yr=(0, 1.15),
            xticks=[],
            yticks=[(0, "0")],
            xlabel="time",
            ylabel="GCaMP light (schematic)",
            color=TEXT,
            size=24,
            label_size=26,
        )
        live = P.live_curve(lambda x: gcamp_trace(x, spike_times=spikes), t_tr, color=REPORTER, width=5.5)
        dot = P.dot(lambda: t_tr.get_value(), lambda: gcamp_trace(t_tr.get_value(), spike_times=spikes), color=REPORTER, ring=TEXT, radius=0.12)

        self.add(brain, neuron, mouse, n_lbl, P, live, dot)

        self.at("turns left")
        self.play(mouse_ang.animate.set_value(0.55), t_tr.animate(rate_func=linear).set_value(3.0), run_time=2.2)

        self.at("flashes bright green")
        self.play(mouse_ang.animate.set_value(0.0), t_tr.animate(rate_func=linear).set_value(3.9), run_time=0.65)
        self.play(mouse_ang.animate.set_value(0.55), t_tr.animate(rate_func=linear).set_value(5.6), run_time=1.3)

        self.at("pause and think")
        q = question_card("Does the flash prove causation?", y=-2.95)
        self.play(FadeIn(q, shift=UP * 0.1), t_tr.animate(rate_func=linear).set_value(6.8), run_time=0.9)

        self.at("does that flash prove")
        self.play(mouse_ang.animate.set_value(0.0), t_tr.animate(rate_func=linear).set_value(7.5), run_time=0.8)
        self.play(mouse_ang.animate.set_value(0.55), t_tr.animate(rate_func=linear).set_value(8.8), run_time=1.6)
        self.play(t_tr.animate(rate_func=linear).set_value(10.0), run_time=2.4)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Does the flash prove causation?"
    CARD = {"y": -2.95}
    RING_AT = (5.8, -2.95, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _predict_world(t_val=10.0, mouse_ang=0.55, glow_val=gcamp_trace(10.0, spike_times=(0.7, 4.2, 7.6)))


class S08Reveal(SpokenScene):
    def construct(self):
        mouse_ang = ValueTracker(0.0)
        glow_tr = ValueTracker(0.1)
        wave_t = ValueTracker(0.0)
        wave_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(wave_t)

        neuron = always_redraw(lambda: make_neuron(center=(0.6, -0.55, 0), scale=1.05, glow=glow_tr.get_value()))
        mouse = always_redraw(lambda: make_mouse(center=(-4.5, -0.35, 0), scale=0.88, angle=mouse_ang.get_value()))
        self.add(neuron, mouse)

        # Show initial correlation (turn + flash) during "Watching alone cannot prove causation"
        self.play(mouse_ang.animate.set_value(0.55), glow_tr.animate.set_value(0.95), run_time=1.3)
        self.play(mouse_ang.animate.set_value(0.0), glow_tr.animate.set_value(0.15), run_time=1.2)

        other_box = boxed_label("Other circuit?", OTHER, size=28).move_to([-1.8, 2.45, 0])
        m_start = other_box.get_bottom() + LEFT * 0.4
        m_end = np.array([-4.3, 0.65, 0.0])
        arr_mouse = DashedLine(m_start, m_end, color=OTHER, stroke_width=3.5, dash_length=0.16)
        ang_m = np.arctan2(m_end[1] - m_start[1], m_end[0] - m_start[0]) - PI / 2
        tip_m = Triangle(fill_color=OTHER, fill_opacity=1.0, stroke_width=0).set_height(0.18).rotate(ang_m).move_to(m_end)

        n_start = other_box.get_bottom() + RIGHT * 0.4
        n_end = np.array([0.4, 0.85, 0.0])
        arr_neuron = DashedLine(n_start, n_end, color=OTHER, stroke_width=3.5, dash_length=0.16)
        ang_n = np.arctan2(n_end[1] - n_start[1], n_end[0] - n_start[0]) - PI / 2
        tip_n = Triangle(fill_color=OTHER, fill_opacity=1.0, stroke_width=0).set_height(0.18).rotate(ang_n).move_to(n_end)

        pulse_u = ValueTracker(0.0)
        p_m = always_redraw(lambda: Dot(
            interpolate(other_box.get_bottom() + LEFT * 0.4, np.array([-4.3, 0.65, 0]), pulse_u.get_value()),
            radius=0.11, color=VOLTAGE,
        ).set_opacity(1.0 if 0.02 < pulse_u.get_value() < 0.98 else 0.0))
        p_n = always_redraw(lambda: Dot(
            interpolate(other_box.get_bottom() + RIGHT * 0.4, np.array([0.4, 0.85, 0]), pulse_u.get_value()),
            radius=0.11, color=VOLTAGE,
        ).set_opacity(1.0 if 0.02 < pulse_u.get_value() < 0.98 else 0.0))

        self.at("another brain circuit")
        self.play(FadeIn(other_box), Create(arr_mouse), FadeIn(tip_m), Create(arr_neuron), FadeIn(tip_n), run_time=0.65)

        self.at("drive both")
        self.add(p_m, p_n)
        for _ in range(2):
            pulse_u.set_value(0.0)
            self.play(pulse_u.animate(rate_func=linear).set_value(1.0), run_time=1.0)
            self.play(mouse_ang.animate.set_value(0.55), glow_tr.animate.set_value(0.95), run_time=0.65)
            self.play(mouse_ang.animate.set_value(0.0), glow_tr.animate.set_value(0.10), run_time=0.65)
        pulse_u.set_value(0.0)

        self.at("cannot only watch")
        self.play(
            VGroup(other_box.box, arr_mouse, tip_m, arr_neuron, tip_n).animate.set_opacity(0.42),
            other_box.label.animate.set_opacity(0.70),
            run_time=0.65,
        )

        self.at("push this neuron")
        beam = always_redraw(lambda: make_photon_wave(
            [3.6, 2.25, 0], [1.65, 0.55, 0], wavelength=0.34, amp=0.12, color=BLUE_LIGHT, phase=7.5 * wave_t.get_value(),
        ))
        push_lbl = T("Push with light", 28, BLUE_LIGHT).move_to([3.9, 2.72, 0])
        self.play(FadeIn(beam), FadeIn(push_lbl, run_time=0.45), run_time=0.6)

        ax_u = ValueTracker(0.0)
        ax_dot = always_redraw(lambda: VGroup(
            Dot(neuron.axon.point_from_proportion(ax_u.get_value() % 1.0), radius=0.22, color=VOLTAGE).set_opacity(0.38),
            Dot(neuron.axon.point_from_proportion(ax_u.get_value() % 1.0), radius=0.11, color=VOLTAGE),
        ))
        self.add(ax_dot)
        self.play(ax_u.animate(rate_func=linear).set_value(2.0), mouse_ang.animate.set_value(0.55), run_time=3.2)
        self.finish()


class S09Chr2(SpokenScene):
    def construct(self):
        mem = make_membrane(x0=-6.1, x1=6.1, y=0.35, gap_x=0.0, gap_w=1.52, half_t=0.72)
        out_lbl = T("Outside cell", 26, TEXT).move_to([-4.6, 1.50, 0])
        in_lbl = T("Inside cell", 26, TEXT).move_to([-4.6, -0.82, 0])
        self.play(FadeIn(mem), FadeIn(out_lbl), FadeIn(in_lbl), run_time=0.9)

        ret_shift = ValueTracker(0.0)
        chr2 = make_chr2_channel(center=(0.0, 0.35, 0), scale=1.42, open_frac=0.0)
        chr2_lbl = T("Channelrhodopsin-2", 30, ACTUATOR).move_to([0.0, 2.55, 0])
        ret_lbl = T("Retinal", 28, RETINAL).move_to([3.30, 1.65, 0])
        ret_arr = Arrow(ret_lbl.get_left() + LEFT * 0.08, chr2.retinal.get_right() + RIGHT * 0.10, buff=0.05, color=RETINAL, stroke_width=3.5)

        self.at("meet channel")
        self.play(
            FadeIn(chr2_lbl, run_time=0.5),
            LaggedStart(*[FadeIn(h, shift=UP * 0.12) for h in chr2.helices], lag_ratio=0.18, run_time=3.2),
        )
        self.play(
            LaggedStart(*[Indicate(h, color=GOLD, scale_factor=1.06) for h in chr2.helices], lag_ratio=0.14, run_time=3.2),
        )

        self.at("retinal")
        self.play(FadeIn(chr2.retinal), FadeIn(ret_lbl, run_time=0.45), GrowArrow(ret_arr), run_time=0.9)
        # Keep retinal & helices visibly active until relay comparison cue (eliminates 9s freeze)
        for idx in range(4):
            h = chr2.helices[idx % len(chr2.helices)]
            self.play(
                Rotate(chr2.retinal, angle=0.22, about_point=chr2.retinal.get_center()),
                Indicate(h, color=VOLTAGE, scale_factor=1.06),
                rate_func=there_and_back,
                run_time=1.1,
            )

        eye_box = boxed_label("Eye rhodopsin", OTHER, size=24).move_to([-3.9, -2.35, 0])
        gp_box = boxed_label("G protein (go-between)", OTHER, size=24).move_to([0.0, -2.35, 0])
        pore_box = boxed_label("Separate pore", OTHER, size=24).move_to([3.9, -2.35, 0])
        a1 = Arrow(eye_box.get_right() + RIGHT * 0.06, gp_box.get_left() + LEFT * 0.06, buff=0.04, color=OTHER, stroke_width=3.2)
        a2 = Arrow(gp_box.get_right() + RIGHT * 0.06, pore_box.get_left() + LEFT * 0.06, buff=0.04, color=OTHER, stroke_width=3.2)
        relay = VGroup(eye_box, a1, gp_box, a2, pore_box)

        self.at("passes the message")
        self.play(FadeIn(relay, run_time=0.65))
        # Highlight each relay step + travel arrow dot smoothly across the full 5s beat
        for _ in range(2):
            self.play(Indicate(eye_box.box, color=VOLTAGE, scale_factor=1.04), run_time=0.40)
            r_dot1 = Dot(eye_box.get_right() + RIGHT * 0.06, radius=0.10, color=VOLTAGE)
            self.add(r_dot1)
            self.play(r_dot1.animate.move_to(gp_box.get_left() + LEFT * 0.06), run_time=0.58)
            self.remove(r_dot1)
            self.play(Indicate(gp_box.box, color=VOLTAGE, scale_factor=1.04), run_time=0.40)
            r_dot2 = Dot(gp_box.get_right() + RIGHT * 0.06, radius=0.10, color=VOLTAGE)
            self.add(r_dot2)
            self.play(r_dot2.animate.move_to(pore_box.get_left() + LEFT * 0.06), run_time=0.58)
            self.remove(r_dot2)
            self.play(Indicate(pore_box.box, color=VOLTAGE, scale_factor=1.04), run_time=0.40)

        self.at("skips that")
        self.play(FadeOut(relay, shift=DOWN * 0.25), run_time=0.7)

        self.at("it is itself")
        direct_lbl = T("Direct light-gated ion pore", 28, ACTUATOR).move_to([0.0, -2.25, 0])
        self.play(FadeIn(direct_lbl, run_time=0.5))
        self.finish()


class S10LightIn(SpokenScene):
    def construct(self):
        wave_t = ValueTracker(0.0)
        wave_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(wave_t)

        open_tr = ValueTracker(0.0)
        ret_tr = ValueTracker(0.0)
        mem = always_redraw(lambda: make_membrane(x0=-6.0, x1=-0.4, y=0.0, gap_x=-3.15, gap_w=1.38 + 0.85 * open_tr.get_value(), half_t=0.70))
        chr2 = always_redraw(lambda: make_chr2_channel(center=(-3.15, 0.0, 0), scale=1.28, open_frac=open_tr.get_value(), retinal_angle=ret_tr.get_value()))
        ch_lbl = T("Channelrhodopsin-2", 26, ACTUATOR).move_to([-3.15, -2.35, 0])

        fire_tr = ValueTracker(0.0)
        mouse_ang = ValueTracker(0.0)
        neuron_sm = always_redraw(lambda: make_neuron(center=(1.6, 2.25, 0), scale=0.40, glow=fire_tr.get_value(), glow_color=VOLTAGE))
        mouse_sm = always_redraw(lambda: make_mouse(center=(4.8, 2.25, 0), scale=0.58, angle=mouse_ang.get_value()))

        v_tr = ValueTracker(0.0)
        P = Plot(
            box=(0.8, 5.9, -2.35, 0.65),
            xr=(0.0, 1.0),
            yr=(0.0, 1.08),
            xticks=[],
            yticks=[],
            xlabel="time",
            ylabel="Voltage (schematic)",
            color=TEXT,
            size=24,
            label_size=26,
        )
        # Put Threshold label on the LEFT end of dashed line (well clear of the spike at tau ~ 0.72)
        thresh_line = P.hline(0.50, label=None, color=GOLD, dashed=True)
        thresh_lbl = T("Threshold", 24, GOLD).next_to(P.pt(0.04, 0.50), UP, buff=0.10).align_to(P.pt(0.04, 0.50), LEFT)
        thresh = VGroup(thresh_line, thresh_lbl)

        live_v = P.live_curve(voltage_trace, v_tr, color=VOLTAGE, width=5.5)
        dot_v = P.dot(lambda: v_tr.get_value(), lambda: voltage_trace(v_tr.get_value()), color=VOLTAGE, ring=TEXT, radius=0.12)

        self.add(mem, chr2, ch_lbl, neuron_sm, mouse_sm, P, thresh, live_v, dot_v)

        self.at("flash blue light")
        beam = always_redraw(lambda: make_photon_wave(
            [-5.25, 2.55, 0], [-3.85, 1.15, 0], wavelength=0.34, amp=0.14, color=BLUE_LIGHT, phase=7.5 * wave_t.get_value(),
        ))
        beam_lbl = T("Blue light", 26, BLUE_LIGHT).move_to([-4.95, 2.95, 0])
        self.play(FadeIn(beam), FadeIn(beam_lbl, run_time=0.45), run_time=0.7)
        self.play(Indicate(chr2, color=BLUE_LIGHT, scale_factor=1.03), run_time=1.8)

        self.at("retinal shifts shape")
        self.play(ret_tr.animate.set_value(-0.55), run_time=0.8)

        self.at("pore opens")
        self.play(open_tr.animate.set_value(1.0), run_time=0.9)

        ion_t = ValueTracker(0.0)
        ion_t.add_updater(lambda m, dt: m.increment_value(dt))
        cation_lbl = T("Cations (+)", 26, CALCIUM).move_to([-1.10, 1.85, 0])

        def _cations():
            t = ion_t.get_value()
            g = VGroup()
            for i in range(5):
                phase = (t * 0.78 + i * 0.2) % 1.0
                x = -3.15 + 0.06 * np.sin(i * 1.9 + phase * 4.0)
                y = 1.60 - 3.05 * phase
                g.add(make_cation_plus([x, y, 0], radius=0.13))
            return g

        cations = always_redraw(_cations)

        self.at("rush in")
        self.add(ion_t, cations)
        self.play(FadeIn(cation_lbl, run_time=0.45), v_tr.animate(rate_func=linear).set_value(0.24), run_time=1.2)

        self.at("positive charge")
        self.play(v_tr.animate(rate_func=linear).set_value(0.55), run_time=2.6)

        self.at("voltage climbs")
        self.play(v_tr.animate(rate_func=linear).set_value(0.75), run_time=2.0)

        self.at("neuron fires")
        self.play(fire_tr.animate.set_value(1.0), v_tr.animate(rate_func=linear).set_value(0.86), run_time=0.7)

        self.at("mouse turns left")
        self.play(mouse_ang.animate.set_value(0.55), v_tr.animate(rate_func=linear).set_value(1.0), run_time=1.1)
        self.finish()


class S11Wrap(SpokenScene):
    def construct(self):
        t_tr = ValueTracker(0.0)
        t_tr.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t_tr)

        neuron = make_neuron(center=(0.0, 0.05, 0), scale=1.36)
        self.add(neuron)

        rep_pos = neuron.dendrite_pt
        rep_barrel = always_redraw(lambda: make_barrel(
            center=rep_pos, height=0.95, slit=0.0, glow=0.72 + 0.28 * np.sin(3.0 * t_tr.get_value()),
        ))
        rep_lbl = T("Reporter", 28, REPORTER).move_to([-4.75, 1.55, 0])
        rep_ray = always_redraw(lambda: make_photon_wave(
            rep_pos + LEFT * 0.48, rep_pos + LEFT * 2.25, wavelength=0.40, amp=0.11, color=REPORTER, phase=6.5 * t_tr.get_value(),
        ))

        act_pore = always_redraw(lambda: make_chr2_channel(
            center=neuron.actuator_pt, scale=0.48, open_frac=0.65 + 0.25 * np.sin(2.8 * t_tr.get_value()),
        ))
        act_lbl = T("Actuator", 28, ACTUATOR).move_to([4.65, 2.25, 0])
        act_beam = always_redraw(lambda: make_photon_wave(
            neuron.actuator_pt + UR * 1.55, neuron.actuator_pt + UR * 0.32, wavelength=0.32, amp=0.10, color=BLUE_LIGHT, phase=7.5 * t_tr.get_value(),
        ))

        def _live_particles():
            t = t_tr.get_value()
            p2 = (t * 0.65) % 1.0
            p3 = (t * 0.50) % 1.0
            return VGroup(
                Dot(interpolate(neuron.actuator_pt + UP * 0.42, neuron.actuator_pt + DOWN * 0.42, p2), radius=0.085, color=CALCIUM),
                Dot(neuron.axon.point_from_proportion(p3), radius=0.20, color=VOLTAGE).set_opacity(0.35),
                Dot(neuron.axon.point_from_proportion(p3), radius=0.095, color=VOLTAGE),
            )

        self.add(rep_barrel, rep_lbl, rep_ray, act_pore, act_lbl, act_beam, always_redraw(_live_particles))

        # Place Gene above soma and route g_arr1 above/left around d_top so neither arrow crosses any dendrite
        gene_box = boxed_label("Gene", GENE, size=24).move_to([0.0, 2.85, 0])
        g_corner = np.array([rep_pos[0], gene_box.get_y(), 0.0])
        g_arr1 = VGroup(
            DashedLine(gene_box.get_left() + LEFT * 0.06, g_corner, color=GENE, stroke_width=3.2),
            DashedLine(g_corner, rep_pos + UP * 0.56, color=GENE, stroke_width=3.2),
        )
        g_arr2 = DashedLine(gene_box.get_right() + RIGHT * 0.06, neuron.actuator_pt + UP * 0.56, color=GENE, stroke_width=3.2)

        self.at("from a gene")
        self.play(FadeIn(gene_box), Create(g_arr1), Create(g_arr2), run_time=0.8)

        self.at("first rule")
        self.play(FadeOut(VGroup(gene_box, g_arr1, g_arr2)), run_time=0.6)

        cap = caption("Reporters turn signals into light,\nand actuators control them on command.", size=28, color=TEXT, y=-2.95)
        self.at("reporters turn signals")
        self.play(FadeIn(cap, run_time=0.6))

        self.at("actuators control them")
        self.finish()


class S12End(EndCard):
    LINE = "Reporters turn signals into light, and actuators control them on command."
