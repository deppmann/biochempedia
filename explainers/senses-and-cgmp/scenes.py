"""
A Fall Can Carry a Signal (senses-and-cgmp)

COLOUR MAP (one colour per concept for the whole film):
- #2DD4BF (C_CGMP)      : cGMP (rod second messenger & gauge)
- #38BDF8 (C_CURRENT)   : Na+ / cation current & schematic current trace
- #FACC15 (C_LIGHT)     : photon / light / active rhodopsin / GTP highlight
- #34D399 (C_CYCLASE)   : cyclase (guanylyl cyclase in rod, adenylyl cyclase in nose)
- #F43F5E (C_PDE)       : PDE6 (cGMP breakdown enzyme)
- #FB923C (C_CA)        : Ca2+ ions, exchanger & Ca2+ gauge
- #F59E0B (C_CAMP)      : cAMP (olfactory second messenger & gauge)
- #A78BFA (C_GLUT)      : glutamate synaptic output
- #8B93A1 (GREY)        : membranes, inhibitory cap, inactive GMP, schematic tag
- #E8EAF0 (TEXT)        : crisp off-white primary labels & question card

CARRIED WORLD:
A cross-section of a rod outer segment (left stacked discs holding rhodopsin, central cytosol
with cyclase, PDE6, transducin, cGMP and Ca2+, right plasma membrane with three cation channels
and synaptic glutamate release, plus far-left vertical gauges and a bottom schematic current
trace). S03 zooms into rhodopsin on the disc; S09 compares the rod on the left beside an
olfactory neuron on the right; S10 foregrounds the two opposite gauges.

PER-SCENE CHANGES (and what each is computed from):
- s01_hook: Photon strike triggers a computed Gaussian dip in the sweeping schematic current trace, then recovers to dark baseline.
- s02_dark_baseline: Cyclase pulses and replenishes cGMP while PDE6 idles; cGMP docks on 2 of 3 channels, Na+/Ca2+ stream in, glutamate exits; 'Make (cyclase): steady' and 'Break (PDE6, idling): slow' build as spoken.
- s03_retinal_switch: Zoomed rhodopsin pocket; photon straightens bent 11-cis retinal bar (computed angle interpolation) into all-trans retinal, pushing rhodopsin into glowing active shape.
- s04_cascade_drop: Transducin flips GDP->GTP, lifts cap off PDE6, spinning PDE6 turns cGMP into fading GMP; cGMP gauge drops from 0.82 to 0.12 and channels snap shut.
- s05_hyperpolarize_reset: Inflow stops, computed current trace plunges continuously, glutamate dwindles; P/arrestin quiet rhodopsin, GTP->GDP resets transducin and PDE6 cap clamps back; cGMP gauge stays at 0.12.
- s06_predict_q: Exchanger pumps Ca2+ out while closed channels block entry; Ca2+ gauge falls from 0.80 to 0.15; GCAPs dock on cyclase; dim light wash settles; question card appears with no answer shown.
- s07_predict_pause: Holds s06 picture and question card for 4.5 s with pulsing '?' and countdown ring.
- s08_predict_reveal: Ca2+->cyclase feedback refills cGMP gauge from 0.12 to 0.48, 1 channel reopens, current trace sweeps up to mid-level ('Current left to shut off') and dips again at an extra flash.
- s09_nose_contrast: Rod on left beside olfactory neuron on right; odorant binds receptor, activates G protein and adenylyl cyclase; cAMP gauge climbs from 0.15 to 0.85, opening channel and depolarizing membrane.
- s10_takehome: Side-by-side gauges gently pulse around baselines: Rod cGMP drops from 0.72 to 0.22 below dashed baseline; Nose cAMP climbs from 0.25 to 0.80 above dashed baseline.
"""

from bp_parts import *

# Concept colour map
C_CGMP = "#2DD4BF"
C_CURRENT = "#38BDF8"
C_LIGHT = "#FACC15"
C_CYCLASE = "#34D399"
C_PDE = "#F43F5E"
C_CA = "#FB923C"
C_CAMP = "#F59E0B"
C_GLUT = "#A78BFA"
C_CYTOSOL = "#1E293B"


# ------------------------------------------------------------------ shared builders
def make_gauge(x, y0=-1.1, y1=2.1, width=0.56, color=C_CGMP, label="cGMP",
               init_val=0.82, baseline=None, label_size=26):
    """Vertical bar gauge driven by a ValueTracker (0..1)."""
    tr = ValueTracker(init_val)
    h = y1 - y0
    frame = Polygon(
        [x - width / 2, y0, 0], [x + width / 2, y0, 0],
        [x + width / 2, y1, 0], [x - width / 2, y1, 0],
        stroke_color=TEXT, stroke_width=2.5, fill_color=C_CYTOSOL, fill_opacity=0.65
    )

    def _fill():
        v = float(np.clip(tr.get_value(), 0.02, 1.0))
        fh = max(0.06, v * (h - 0.06))
        cx = x
        cy_bot = y0 + 0.03
        cy_top = cy_bot + fh
        hw = (width - 0.08) / 2
        return Polygon(
            [cx - hw, cy_bot, 0], [cx + hw, cy_bot, 0],
            [cx + hw, cy_top, 0], [cx - hw, cy_top, 0],
            stroke_width=0, fill_color=color, fill_opacity=0.90
        )

    bar = always_redraw(_fill)
    lab = T(label, label_size, color).move_to([x, y1 + 0.34, 0])
    g = VGroup(frame, bar, lab)
    if baseline is not None:
        by = y0 + baseline * h
        dash = DashedLine([x - width * 0.72, by, 0], [x + width * 0.72, by, 0],
                          color=TEXT, stroke_width=2.5, dash_length=0.1)
        g.add(dash)
    g.tracker = tr
    g.frame = frame
    g.lab = lab
    g.y0, g.y1, g.x = y0, y1, x
    return g


def make_channel(y, x=3.6, open_frac=1.0, cgmp_bound=False):
    """Membrane cation channel at x with pivoting gates driven by a ValueTracker."""
    tr = ValueTracker(open_frac)
    top_lip = Line([x - 0.28, y + 0.28, 0], [x + 0.28, y + 0.28, 0], color=TEXT, stroke_width=5)
    bot_lip = Line([x - 0.28, y - 0.28, 0], [x + 0.28, y - 0.28, 0], color=TEXT, stroke_width=5)

    def _gates():
        f = float(np.clip(tr.get_value(), 0.0, 1.0))
        gap = 0.02 + 0.20 * f
        upper = Line([x, y + 0.26, 0], [x, y + gap, 0], color=C_CURRENT, stroke_width=7)
        lower = Line([x, y - 0.26, 0], [x, y - gap, 0], color=C_CURRENT, stroke_width=7)
        return VGroup(upper, lower)

    gates = always_redraw(_gates)
    pocket = Arc(radius=0.12, start_angle=PI / 2, angle=PI, arc_center=[x - 0.30, y - 0.14, 0],
                 color=C_CGMP, stroke_width=3)
    dot = Dot([x - 0.32, y - 0.14, 0], radius=0.085, color=C_CGMP)
    if not cgmp_bound:
        dot.set_opacity(0.0)
    g = VGroup(top_lip, bot_lip, gates, pocket, dot)
    g.tracker = tr
    g.cgmp_dot = dot
    g.y_pos = y
    return g


def make_rod_shell(x_left=-3.5, x_right=3.6, y_bot=-1.05, y_top=2.95, channel_ys=(2.1, 0.9, -0.3)):
    """Polygon rod outer-segment silhouette with open channel pores on the right membrane."""
    cytosol = Polygon(
        [x_left, y_bot, 0], [x_right, y_bot, 0],
        [x_right, y_top, 0], [x_left, y_top, 0],
        stroke_width=0, fill_color=C_CYTOSOL, fill_opacity=0.62
    )
    cytosol.set_z_index(-6)
    left_wall = Line([x_left, y_bot, 0], [x_left, y_top, 0], color=GREY, stroke_width=4.5)
    top_wall = Line([x_left, y_top, 0], [x_right, y_top, 0], color=GREY, stroke_width=4.5)
    bot_wall = Line([x_left, y_bot, 0], [x_right, y_bot, 0], color=GREY, stroke_width=4.5)

    ys_sorted = sorted(channel_ys, reverse=True)
    segs = []
    cur_y = y_top
    for cy in ys_sorted:
        segs.append(Line([x_right, cur_y, 0], [x_right, cy + 0.28, 0], color=GREY, stroke_width=4.5))
        cur_y = cy - 0.28
    segs.append(Line([x_right, cur_y, 0], [x_right, y_bot, 0], color=GREY, stroke_width=4.5))
    right_wall = VGroup(*segs)

    # Three stacked disc membranes on the left
    discs = VGroup()
    for dy in (2.1, 1.0, -0.1):
        d = Ellipse(width=1.65, height=0.56, color=GREY, stroke_width=3,
                    fill_color=GREY, fill_opacity=0.22).move_to([-2.45, dy, 0])
        discs.add(d)

    return VGroup(cytosol, left_wall, top_wall, bot_wall, right_wall, discs), discs


def make_rhodopsin(pos=(-2.25, 2.1, 0), active=False, scale=1.0):
    """Rhodopsin block sitting on a disc membrane."""
    col = C_LIGHT if active else GREY
    op = 0.40 if active else 0.28
    body = Ellipse(width=0.60 * scale, height=0.40 * scale, color=col, stroke_width=3,
                   fill_color=col, fill_opacity=op).move_to(pos)
    return body


def make_cyclase(pos=(-0.75, -0.38, 0), bright=False):
    """Guanylyl cyclase enzyme on the lower cytosol."""
    col = C_CYCLASE
    op = 0.52 if bright else 0.28
    sw = 4.5 if bright else 3.0
    body = Ellipse(width=1.10, height=0.56, color=col, stroke_width=sw,
                   fill_color=col, fill_opacity=op).move_to(pos)
    return body


def add_cyclase_pulse(cyclase, amp=0.06, speed=3.5):
    """Continuous gentle breathing pulse on guanylyl cyclase."""
    cyclase._pt = 0.0
    base_w, base_h = cyclase.width, cyclase.height

    def _u(mob, dt):
        mob._pt += dt
        s = 1.0 + amp * np.sin(speed * mob._pt)
        mob.stretch_to_fit_width(base_w * s)
        mob.stretch_to_fit_height(base_h * s)

    cyclase.add_updater(_u)
    return cyclase


def make_pde6(pos=(2.25, 1.95, 0), capped=True):
    """Rose PDE6 enzyme with removable grey inhibitory cap."""
    core = Circle(radius=0.35, color=C_PDE, stroke_width=3.5,
                  fill_color=C_PDE, fill_opacity=0.28).move_to(pos)
    spokes = VGroup(*[
        Line(pos + 0.10 * np.array([np.cos(a), np.sin(a), 0]),
             pos + 0.31 * np.array([np.cos(a), np.sin(a), 0]),
             color=C_PDE, stroke_width=3.5)
        for a in np.linspace(0, TAU, 6, endpoint=False)
    ])
    cap = Arc(radius=0.43, start_angle=PI * 0.25, angle=PI * 0.9, arc_center=pos,
              color=GREY, stroke_width=7)
    if not capped:
        cap.shift(UP * 0.42 + LEFT * 0.15).set_opacity(0.0)
    g = VGroup(core, spokes, cap)
    g.core = core
    g.spokes = spokes
    g.cap = cap
    return g


def make_cytosol_dots(count=14, color=C_CGMP, x_range=(-1.2, 2.7), y_range=(0.22, 1.25),
                      seed=7, radius=0.09):
    """Deterministic drifting messenger or Ca2+ dots in a clean cytosol box."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        x = rng.uniform(*x_range)
        y = rng.uniform(*y_range)
        vx = rng.uniform(0.28, 0.52) * (1 if rng.random() > 0.5 else -1)
        vy = rng.uniform(0.18, 0.34) * (1 if rng.random() > 0.5 else -1)
        d = Dot([x, y, 0], radius=radius, color=color, fill_opacity=0.92)
        d._vx, d._vy = vx, vy
        dots.add(d)
    return dots


def add_drift_updater(dots, x_range=(-1.2, 2.7), y_range=(0.22, 1.25), speed_tracker=None):
    """Keep dots bouncing smoothly inside a confined cytosol box."""
    x0, x1 = x_range
    y0, y1 = y_range

    def _u(mob, dt):
        s = speed_tracker.get_value() if speed_tracker is not None else 1.0
        for d in mob:
            p = d.get_center()
            nx = p[0] + d._vx * dt * s
            ny = p[1] + d._vy * dt * s
            if nx < x0 or nx > x1:
                d._vx = -d._vx
                nx = float(np.clip(nx, x0, x1))
            if ny < y0 or ny > y1:
                d._vy = -d._vy
                ny = float(np.clip(ny, y0, y1))
            d.move_to([nx, ny, 0])

    dots.add_updater(_u)
    return dots


def make_ion_stream(ys=(2.1, 0.9), colors=(C_CURRENT, C_CURRENT, C_CA), flow_tracker=None):
    """Streaming Na+ / Ca2+ beads moving right-to-left through open channels."""
    beads = VGroup()
    rng = np.random.default_rng(11)
    for idx, cy in enumerate(ys):
        for k in range(4):
            col = colors[(idx + k) % len(colors)]
            d = Dot([5.7 - k * 0.72, cy + rng.uniform(-0.07, 0.07), 0], radius=0.085, color=col)
            d._cy = cy
            d._speed = 1.45
            beads.add(d)

    def _u(mob, dt):
        f = flow_tracker.get_value() if flow_tracker is not None else 1.0
        for d in mob:
            if f <= 0.05:
                d.set_opacity(0.0)
                continue
            d.set_opacity(min(1.0, f))
            d.shift(LEFT * d._speed * dt * (0.45 + 0.55 * f))
            if d.get_center()[0] < 2.55:
                d.move_to([5.75, d._cy, 0])

    beads.add_updater(_u)
    return beads


def make_rod_world(cgmp_val=0.82, ch_open=(1.0, 1.0, 0.0), active_rhod=False,
                   pde_capped=True, cyclase_bright=False, with_ca_gauge=False,
                   ca_val=0.80, with_cgmp_gauge=True, ion_flow=1.0,
                   with_labels=True, cgmp_x_range=(-1.2, 2.7), cgmp_y_range=(0.22, 1.22)):
    """Build the complete carried rod outer-segment world."""
    shell, discs = make_rod_shell()
    rhod_top = make_rhodopsin((-2.25, 2.1, 0), active=active_rhod)
    rhod_mid = make_rhodopsin((-2.25, 1.0, 0), active=False)
    rhod_bot = make_rhodopsin((-2.25, -0.1, 0), active=False)
    rhods = VGroup(rhod_top, rhod_mid, rhod_bot)

    cyclase = make_cyclase((-0.75, -0.38, 0), bright=cyclase_bright)
    pde = make_pde6((2.25, 1.95, 0), capped=pde_capped)

    ch_ys = (2.1, 0.9, -0.3)
    channels = VGroup(*[
        make_channel(y, open_frac=op, cgmp_bound=(op > 0.3))
        for y, op in zip(ch_ys, ch_open)
    ])

    n_cgmp = max(2, min(12, int(round(12 * cgmp_val / 0.82))))
    cgmp_op = float(np.clip(0.45 + 0.47 * (cgmp_val / 0.82), 0.45, 0.92))
    cgmp_dots = make_cytosol_dots(count=n_cgmp, color=C_CGMP, x_range=cgmp_x_range, y_range=cgmp_y_range, seed=7)
    cgmp_dots.set_opacity(cgmp_op)
    add_drift_updater(cgmp_dots, x_range=cgmp_x_range, y_range=cgmp_y_range)

    flow_tr = ValueTracker(ion_flow)
    open_ys = [y for y, op in zip(ch_ys, ch_open) if op > 0.2] or [2.1]
    ions = make_ion_stream(ys=tuple(open_ys), flow_tracker=flow_tr)

    cgmp_gauge = make_gauge(-5.65, label="cGMP", color=C_CGMP, init_val=cgmp_val, baseline=0.82) if with_cgmp_gauge else None
    ca_gauge = make_gauge(-4.50, label="Ca2+", color=C_CA, init_val=ca_val) if with_ca_gauge else None

    labels = VGroup()
    if with_labels:
        l_rhod = T("rhodopsin", 26, TEXT).move_to([-2.45, 3.25, 0])
        l_pde = T("PDE6", 26, C_PDE).move_to([2.25, 3.25, 0])
        l_cyc = T("cyclase", 26, C_CYCLASE).move_to([0.75, -0.38, 0])
        l_chan = T("channels", 26, C_CURRENT).move_to([4.85, 3.25, 0])
        labels.add(l_rhod, l_pde, l_cyc, l_chan)

    world = VGroup(shell, rhods, cyclase, pde, channels, cgmp_dots, ions, labels)
    if cgmp_gauge is not None:
        world.add(cgmp_gauge)
    if ca_gauge is not None:
        world.add(ca_gauge)

    world.shell = shell
    world.discs = discs
    world.rhod_top = rhod_top
    world.rhods = rhods
    world.cyclase = cyclase
    world.pde = pde
    world.channels = channels
    world.cgmp_dots = cgmp_dots
    world.ions = ions
    world.flow_tr = flow_tr
    world.cgmp_gauge = cgmp_gauge
    world.ca_gauge = ca_gauge
    world.labels = labels
    return world


def make_current_plot():
    """Bottom schematic current trace Plot (x in 0..10, y in 0..1.1)."""
    P = Plot(
        box=(-3.4, 3.3, -3.25, -2.04),
        xr=(0, 10), yr=(0, 1.1),
        xticks=[],
        yticks=[(0.20, "low"), (0.85, "dark")],
        ylabel="current",
        color=GREY, size=22, label_size=24, stroke=3
    )
    return P


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Sensing the World: Vision, Smell, Nitric Oxide and cGMP"
    TITLE = "A Fall Can Carry a Signal"


class S01Hook(SpokenScene):
    def construct(self):
        world = make_rod_world(cgmp_val=0.82, ch_open=(1.0, 1.0, 0.0), with_cgmp_gauge=False)
        P = make_current_plot()
        stag = scope_tag("schematic")
        t = ValueTracker(0.05)

        trace_fn = lambda x: 0.85 - 0.60 * np.exp(-((x - 3.2) / 0.85) ** 2)
        live = P.live_curve(trace_fn, t, color=C_CURRENT, width=5)
        dot = P.dot(lambda: t.get_value(), lambda: trace_fn(t.get_value()), color=C_CURRENT, ring=TEXT, radius=0.09)

        self.add(world, P, stag, live, dot)
        self.play(t.animate(rate_func=linear).set_value(1.5), run_time=self.t_of("a single photon") - 0.2)

        # Gold photon arrow flashes onto left disc; label placed clearly left of x=-3.5 wall
        photon = Arrow([-5.7, 2.1, 0], [-2.75, 2.1, 0], color=C_LIGHT, stroke_width=6, buff=0.0)
        p_lab = T("photon", 26, C_LIGHT).move_to([-4.65, 2.58, 0])
        self.play(FadeIn(photon, shift=RIGHT * 0.2), FadeIn(p_lab), run_time=0.45)

        self.at("turning an electrical")
        self.play(
            t.animate(rate_func=linear).set_value(4.0),
            world.flow_tr.animate.set_value(0.25),
            run_time=1.9
        )

        self.at("How can destroying")
        self.play(
            FadeOut(photon), FadeOut(p_lab),
            t.animate(rate_func=linear).set_value(6.8),
            world.flow_tr.animate.set_value(1.0),
            run_time=2.8
        )

        self.at("Every cascade")
        self.play(t.animate(rate_func=linear).set_value(8.8), run_time=2.8)

        self.at("Start with a rod")
        dark_lab = T("Dark state", 28, TEXT).move_to([4.9, -2.1, 0])
        self.play(
            FadeIn(dark_lab, shift=UP * 0.1),
            t.animate(rate_func=linear).set_value(9.9),
            run_time=1.3
        )
        self.finish()


class S02DarkBaseline(SpokenScene):
    def construct(self):
        world = make_rod_world(cgmp_val=0.82, ch_open=(1.0, 1.0, 0.0), with_cgmp_gauge=True)
        na_lab = T("Na+", 26, C_CURRENT).move_to([5.45, 2.55, 0])
        ca_lab = T("Ca2+", 26, C_CA).move_to([5.45, 1.38, 0])

        glut_lab = T("glutamate", 26, C_GLUT).move_to([5.25, -0.55, 0])
        glut_dots = make_cytosol_dots(count=8, color=C_GLUT, x_range=(4.0, 5.85), y_range=(-1.95, -0.95), seed=19, radius=0.095)

        def _glut_det(mob, dt):
            for idx, d in enumerate(mob):
                d.shift([0.75 * dt, -0.35 * dt, 0])
                p = d.get_center()
                if p[0] > 5.95 or p[1] < -2.15:
                    d.move_to([3.95 + 0.14 * (idx % 3), -1.00 - 0.14 * (idx % 2), 0])

        glut_dots.add_updater(_glut_det)

        add_cyclase_pulse(world.cyclase, amp=0.10, speed=4.4)
        world.pde.spokes.add_updater(lambda m, dt: m.rotate(0.75 * dt, about_point=world.pde.core.get_center()))

        make_lbl = T("Make (cyclase): steady", 28, C_CYCLASE).move_to([-3.2, -2.85, 0])
        break_lbl = T("Break (PDE6, idling): slow", 28, C_PDE).move_to([2.4, -2.85, 0])

        self.add(world, glut_dots)
        self.at("cyclase keeps making")
        self.play(FadeIn(make_lbl, shift=UP * 0.1), run_time=0.8)

        self.at("while its breakdown")
        self.play(FadeIn(break_lbl, shift=UP * 0.1), run_time=0.8)

        self.at("stays high")
        g_hi = T("high", 26, C_CGMP).next_to(world.cgmp_gauge.frame, DOWN, buff=0.16)
        self.play(FadeIn(g_hi), run_time=0.6)

        self.at("binds directly")
        bind_note = T("direct binding (no kinase)", 26, C_CGMP).move_to([0.9, -1.60, 0])
        self.play(
            Indicate(world.channels[0].cgmp_dot, color=C_CGMP, scale_factor=1.5),
            Indicate(world.channels[1].cgmp_dot, color=C_CGMP, scale_factor=1.5),
            FadeIn(bind_note),
            run_time=1.2
        )

        self.at("Sodium and calcium")
        self.play(FadeIn(na_lab), FadeIn(ca_lab), run_time=0.8)

        self.at("steady dark current")
        dep_lab = T("partly depolarized", 26, TEXT).move_to([0.9, -2.18, 0])
        self.play(FadeIn(dep_lab), run_time=0.8)

        self.at("releasing glutamate")
        self.play(FadeIn(glut_lab), Indicate(glut_lab, color=C_GLUT), run_time=0.8)
        self.finish()


class S03RetinalSwitch(SpokenScene):
    def construct(self):
        faint_rod, _ = make_rod_shell()
        faint_rod.set_opacity(0.18).set_z_index(-8)
        faint_rod.layout_ok = True

        center = np.array([-0.2, 0.2, 0])
        morph_t = ValueTracker(0.0)
        glow_t = ValueTracker(0.0)
        glow_t.add_updater(lambda m, dt: m.increment_value(dt))

        def _pocket():
            f = morph_t.get_value()
            g = glow_t.get_value()
            col = interpolate_color(ManimColor(GREY), ManimColor(C_LIGHT), f)
            w = 6.5 + 0.70 * f + 0.14 * np.sin(3.0 * g) * (0.35 + 0.65 * f)
            h = 4.5 + 0.35 * f + 0.10 * np.sin(3.0 * g) * (0.35 + 0.65 * f)
            outer = RoundedRectangle(corner_radius=0.55, width=w, height=h,
                                     stroke_color=col, stroke_width=5.5,
                                     fill_color=BG, fill_opacity=0.96).move_to(center)
            inner = RoundedRectangle(corner_radius=0.35, width=w - 1.2, height=h - 1.3,
                                     stroke_color=col, stroke_width=3.0,
                                     fill_color=col, fill_opacity=0.14 + 0.14 * f).move_to(center)
            return VGroup(outer, inner)

        pocket = always_redraw(_pocket)

        def _retinal_bar():
            f = morph_t.get_value()
            g = glow_t.get_value()
            kink = (0.64 - 0.64 * f) + 0.04 * (1.0 - f) * np.sin(4.0 * g)
            p_left = center + np.array([-1.65, -0.30 + 0.30 * f, 0])
            p_mid = center + np.array([0.0, kink, 0])
            p_right = center + np.array([1.65, -0.30 + 0.30 * f, 0])
            col = interpolate_color(ManimColor(TEXT), ManimColor(C_LIGHT), f)
            seg1 = Line(p_left, p_mid, color=col, stroke_width=13)
            seg2 = Line(p_mid, p_right, color=col, stroke_width=13)
            joint = Dot(p_mid, radius=0.10, color=col)
            return VGroup(seg1, seg2, joint)

        retinal = always_redraw(_retinal_bar)

        state_off = T("rhodopsin: OFF", 30, TEXT).move_to([center[0], 3.10, 0])
        state_on = T("rhodopsin: ON (active)", 30, C_LIGHT).move_to([center[0], 3.10, 0])
        ret_cis = T("11-cis retinal", 30, TEXT).move_to([center[0], -2.62, 0])
        ret_trans = T("all-trans retinal", 30, C_LIGHT).move_to([center[0], -2.62, 0])
        stag = scope_tag("schematic")

        self.add(faint_rod, stag, glow_t)
        self.play(FadeIn(pocket), run_time=0.9)
        self.at("a receptor holding")
        self.play(FadeIn(retinal), FadeIn(ret_cis), run_time=0.9)

        self.at("That bent shape")
        self.play(FadeIn(state_off), run_time=0.8)

        self.at("When a photon")
        wave_xs = np.linspace(-5.9, -3.5, 45)
        wave = VMobject(color=C_LIGHT, stroke_width=5)
        wave.set_points_as_corners([[x, 0.2 + 0.28 * np.sin(5.0 * x), 0] for x in wave_xs])
        tip = Arrow([-3.65, 0.2, 0], [-2.55, 0.2, 0], color=C_LIGHT, stroke_width=5, buff=0.0)
        p_wave = VGroup(wave, tip)
        p_lbl = T("photon", 26, C_LIGHT).next_to(wave, UP, buff=0.22)
        self.play(Create(wave), FadeIn(tip), FadeIn(p_lbl), run_time=0.9)

        self.at("it straightens")
        self.play(
            morph_t.animate.set_value(1.0),
            FadeOut(p_wave), FadeOut(p_lbl),
            run_time=1.8
        )
        self.play(swap(ret_cis, ret_trans, run_time=0.65), swap(state_off, state_on, run_time=0.65))

        self.at("every later step")
        no_light = T("later steps run without light", 28, TEXT).move_to([center[0], -3.18, 0])
        self.play(FadeIn(no_light, shift=UP * 0.1), run_time=1.2)
        self.finish()


class S04CascadeDrop(SpokenScene):
    def construct(self):
        world = make_rod_world(cgmp_val=0.82, ch_open=(1.0, 1.0, 0.0), active_rhod=True, pde_capped=True,
                               cgmp_y_range=(0.22, 0.95))

        # Compact two-line chips placed cleanly in the open cytosol lane (-1.45 .. +1.70)
        td1 = chip("transducin\nGDP", TEXT, size=22, pad=0.10).move_to([-0.35, 2.30, 0])
        td2 = chip("transducin\nGDP", TEXT, size=22, pad=0.10).move_to([-0.35, 1.48, 0])
        td1_gtp = chip("transducin\nGTP", C_LIGHT, size=22, pad=0.10).move_to([-0.20, 2.30, 0])
        td2_gtp = chip("transducin\nGTP", C_LIGHT, size=22, pad=0.10).move_to([-0.20, 1.48, 0])

        gmp_dots = make_cytosol_dots(count=10, color=GREY, x_range=(-1.0, 2.6), y_range=(0.22, 0.95), seed=31, radius=0.08)
        gmp_dots.set_opacity(0.0)
        add_drift_updater(gmp_dots, x_range=(-1.0, 2.6), y_range=(0.22, 0.95))

        spin_rate = ValueTracker(0.0)
        world.pde.spokes.add_updater(lambda m, dt: m.rotate(spin_rate.get_value() * dt,
                                                            about_point=world.pde.core.get_center()))

        self.add(world, gmp_dots)
        self.at("switches on many")
        self.play(FadeIn(td1), FadeIn(td2), run_time=0.9)

        self.at("swapping GDP for GTP")
        self.play(swap(td1, td1_gtp, run_time=0.65), swap(td2, td2_gtp, run_time=0.65))

        self.at("Activated transducin")
        self.play(
            td1_gtp.animate.move_to([0.65, 2.30, 0]),
            td2_gtp.animate.move_to([0.65, 1.48, 0]),
            run_time=1.0
        )
        # Slide grey inhibitory cap off PDE6 cleanly inside the rod
        self.play(
            world.pde.cap.animate.shift(UP * 0.35 + LEFT * 0.35).set_stroke(opacity=0.28),
            spin_rate.animate.set_value(2.5),
            run_time=1.0
        )
        cap_lbl = T("cap lifted", 22, GREY).move_to([2.90, 2.68, 0])
        self.play(FadeIn(cap_lbl), run_time=0.6)

        self.at("The freed enzyme")
        self.play(spin_rate.animate.set_value(6.5), run_time=0.7)
        gmp_lbl = T("cGMP -> GMP", 26, C_PDE).move_to([0.8, -1.65, 0])
        self.play(
            FadeIn(gmp_lbl),
            world.cgmp_dots.animate.set_opacity(0.18),
            gmp_dots.animate.set_opacity(0.75),
            run_time=2.0
        )
        self.play(gmp_dots.animate.set_opacity(0.18), run_time=1.6)

        self.at("As messenger levels")
        self.play(
            world.cgmp_gauge.tracker.animate.set_value(0.12),
            world.channels[0].cgmp_dot.animate.shift(LEFT * 0.6).set_opacity(0.0),
            world.channels[1].cgmp_dot.animate.shift(LEFT * 0.6).set_opacity(0.0),
            run_time=1.3
        )

        self.at("channels snap shut")
        self.play(
            world.channels[0].tracker.animate.set_value(0.0),
            world.channels[1].tracker.animate.set_value(0.0),
            world.flow_tr.animate.set_value(0.0),
            run_time=0.75
        )
        self.finish()


class S05HyperpolarizeReset(SpokenScene):
    def construct(self):
        world = make_rod_world(cgmp_val=0.12, ch_open=(0.0, 0.0, 0.0), active_rhod=True,
                               pde_capped=False, ion_flow=0.0)
        td_gtp = chip("transducin\nGTP", C_LIGHT, size=22, pad=0.10).move_to([0.20, 1.95, 0])
        td_gdp = chip("transducin\nGDP", TEXT, size=22, pad=0.10).move_to([0.20, 1.95, 0])

        P = make_current_plot()
        stag = scope_tag("schematic")
        t = ValueTracker(0.5)
        trace_fn = lambda x: 0.85 - 0.65 / (1.0 + np.exp(-2.8 * (x - 3.2)))
        live = P.live_curve(trace_fn, t, color=C_CURRENT, width=5)
        dot = P.dot(lambda: t.get_value(), lambda: trace_fn(t.get_value()), color=C_CURRENT, ring=TEXT, radius=0.09)

        glut_lab = T("glutamate\ndrops", 26, C_GLUT).move_to([5.25, -0.55, 0])
        glut_dots = make_cytosol_dots(count=5, color=C_GLUT, x_range=(4.1, 5.5), y_range=(-1.6, -1.05), seed=23, radius=0.08)
        add_drift_updater(glut_dots, x_range=(4.1, 5.5), y_range=(-1.6, -1.05))

        self.add(world, td_gtp, P, stag, live, dot, glut_dots)
        self.at("positive inflow shrinks")
        self.play(t.animate(rate_func=linear).set_value(3.0), run_time=1.5)

        self.at("the membrane hyperpolarizes")
        hyp_lbl = T("hyperpolarized", 26, C_CURRENT).move_to([5.20, 0.88, 0])
        self.play(t.animate(rate_func=linear).set_value(5.0), FadeIn(hyp_lbl), run_time=1.5)

        self.at("glutamate release drops")
        self.play(FadeIn(glut_lab), glut_dots.animate.set_opacity(0.15), t.animate(rate_func=linear).set_value(6.0), run_time=1.0)

        self.at("The next neuron")
        next_lbl = T("next neuron: light!", 26, TEXT).move_to([5.15, -2.08, 0])
        self.play(FadeIn(next_lbl), t.animate(rate_func=linear).set_value(7.2), run_time=2.0)

        self.at("To reset")
        p_tags = VGroup(
            T("P", 22, C_LIGHT).move_to([-2.55, 2.60, 0]),
            T("P", 22, C_LIGHT).move_to([-1.95, 2.60, 0]),
        )
        arr_cap = chip("arrestin", TEXT, size=22, pad=0.09).move_to([-2.25, 1.54, 0])
        self.play(
            FadeIn(p_tags), FadeIn(arr_cap),
            world.rhod_top.animate.set_color(GREY).set_fill(GREY, opacity=0.28),
            t.animate(rate_func=linear).set_value(8.4),
            run_time=2.2
        )

        self.at("while GTP hydrolysis")
        self.play(
            swap(td_gtp, td_gdp, run_time=0.8),
            world.pde.cap.animate.shift(DOWN * 0.42 + RIGHT * 0.15).set_stroke(opacity=1.0).set_fill(opacity=0.0),
            t.animate(rate_func=linear).set_value(9.3),
            run_time=2.0
        )

        self.at("Still, the rod")
        low_lbl = T("cGMP still low", 26, C_CGMP).move_to([-5.30, -1.65, 0])
        self.play(
            FadeIn(low_lbl),
            Indicate(world.cgmp_gauge.frame, color=C_CGMP, scale_factor=1.05),
            t.animate(rate_func=linear).set_value(9.9),
            run_time=1.8
        )
        self.finish()


def build_predict_world():
    """Shared world state at the end of s06 and throughout s07_predict_pause (NO answer shown)."""
    world = make_rod_world(cgmp_val=0.12, ch_open=(0.0, 0.0, 0.0), active_rhod=False,
                           pde_capped=True, cyclase_bright=True, with_ca_gauge=True,
                           ca_val=0.15, ion_flow=0.0,
                           cgmp_x_range=(0.15, 2.65), cgmp_y_range=(0.55, 1.25))
    add_cyclase_pulse(world.cyclase, amp=0.08, speed=4.2)

    light_wash = Ellipse(width=2.5, height=3.5, stroke_width=0,
                         fill_color=C_LIGHT, fill_opacity=0.15).move_to([-2.45, 1.0, 0])
    light_wash.set_z_index(-4)
    light_wash.layout_ok = True

    gcaps = chip("GCAPs", C_CA, size=24, pad=0.12).move_to([-0.75, 0.25, 0])
    exchanger = Arrow([3.1, -0.75, 0], [4.45, -0.75, 0], color=C_CA, stroke_width=5, buff=0.0)
    ex_lbl = T("Ca2+ exchanger", 24, C_CA).move_to([5.30, -0.32, 0])
    ca_dots = make_cytosol_dots(count=4, color=C_CA, x_range=(0.15, 2.65), y_range=(0.55, 1.25), seed=41, radius=0.085)
    add_drift_updater(ca_dots, x_range=(0.15, 2.65), y_range=(0.55, 1.25))

    dim_lbl = T("dim light", 24, C_LIGHT).move_to([-2.45, -1.42, 0])
    return VGroup(world, light_wash, gcaps, exchanger, ex_lbl, ca_dots, dim_lbl)


class S06PredictQ(SpokenScene):
    def construct(self):
        world = make_rod_world(cgmp_val=0.82, ch_open=(1.0, 1.0, 0.0), active_rhod=False,
                               pde_capped=True, cyclase_bright=False, with_ca_gauge=True,
                               ca_val=0.80, ion_flow=1.0,
                               cgmp_x_range=(0.15, 2.65), cgmp_y_range=(0.55, 1.25))
        ca_dots = make_cytosol_dots(count=12, color=C_CA, x_range=(0.15, 2.65), y_range=(0.55, 1.25), seed=41, radius=0.09)
        add_drift_updater(ca_dots, x_range=(0.15, 2.65), y_range=(0.55, 1.25))
        exchanger = Arrow([3.1, -0.75, 0], [4.45, -0.75, 0], color=C_CA, stroke_width=5, buff=0.0)
        ex_lbl = T("Ca2+ exchanger", 24, C_CA).move_to([5.30, -0.32, 0])
        ex_dots = VGroup(*[Dot([3.25 + k * 0.48, -0.75, 0], radius=0.08, color=C_CA) for k in range(3)])
        ex_dots.add_updater(lambda mob, dt: [
            d.shift(RIGHT * 0.9 * dt) if d.get_center()[0] < 4.75 else d.move_to([3.15, -0.75, 0])
            for d in mob
        ])

        self.add(world, ca_dots)
        self.at("calcium entered steadily")
        self.play(FadeIn(exchanger), FadeIn(ex_lbl), FadeIn(ex_dots), run_time=1.2)

        self.at("Light closed the channels")
        self.play(
            world.channels[0].tracker.animate.set_value(0.0),
            world.channels[1].tracker.animate.set_value(0.0),
            world.channels[0].cgmp_dot.animate.set_opacity(0.0),
            world.channels[1].cgmp_dot.animate.set_opacity(0.0),
            world.flow_tr.animate.set_value(0.0),
            world.cgmp_gauge.tracker.animate.set_value(0.12),
            world.cgmp_dots[2:].animate.set_opacity(0.0),
            world.cgmp_dots[:2].animate.set_opacity(0.52),
            run_time=1.8
        )

        self.at("and calcium fell")
        self.play(
            world.ca_gauge.tracker.animate.set_value(0.15),
            ca_dots[4:].animate.set_opacity(0.0),
            run_time=1.6
        )

        self.at("Low calcium switches")
        gcaps = chip("GCAPs", C_CA, size=24, pad=0.12).move_to([-0.75, 0.95, 0])
        self.play(FadeIn(gcaps), run_time=0.6)
        self.play(
            gcaps.animate.move_to([-0.75, 0.25, 0]),
            world.cyclase.animate.set_fill(C_CYCLASE, opacity=0.52).set_stroke(width=4.5),
            run_time=1.4
        )
        add_cyclase_pulse(world.cyclase, amp=0.08, speed=4.2)

        self.at("Now keep a dim")
        light_wash = Ellipse(width=2.5, height=3.5, stroke_width=0,
                             fill_color=C_LIGHT, fill_opacity=0.15).move_to([-2.45, 1.0, 0])
        light_wash.set_z_index(-4)
        light_wash.layout_ok = True
        dim_lbl = T("dim light", 24, C_LIGHT).move_to([-2.45, -1.42, 0])
        self.play(FadeIn(light_wash), FadeIn(dim_lbl), run_time=1.0)

        self.at("Will the channels")
        q = question_card("Steady light: do the channels stay shut?", color=TEXT)
        self.play(FadeIn(q.question), run_time=0.8)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = "Steady light: do the channels stay shut?"
    CARD = {"color": TEXT}
    SECONDS = 4.5

    def backdrop(self):
        bg = build_predict_world()
        qmark = T("?", 44, C_LIGHT, weight=BOLD).move_to([4.35, 1.5, 0])
        qmark._qt = 0.0
        qmark.add_updater(lambda m, dt: (setattr(m, "_qt", m._qt + dt),
                                         m.set_opacity(0.55 + 0.45 * np.sin(3.5 * m._qt))))
        return VGroup(bg, qmark)


class S08PredictReveal(SpokenScene):
    def construct(self):
        world = make_rod_world(cgmp_val=0.12, ch_open=(0.0, 0.0, 0.0), active_rhod=False,
                               pde_capped=True, cyclase_bright=True, with_ca_gauge=True,
                               ca_val=0.15, ion_flow=0.0,
                               cgmp_x_range=(0.15, 2.65), cgmp_y_range=(0.55, 1.25))
        add_cyclase_pulse(world.cyclase, amp=0.08, speed=4.2)
        light_wash = Ellipse(width=2.5, height=3.5, stroke_width=0,
                             fill_color=C_LIGHT, fill_opacity=0.15).move_to([-2.45, 1.0, 0])
        light_wash.set_z_index(-4)
        light_wash.layout_ok = True
        gcaps = chip("GCAPs", C_CA, size=24, pad=0.12).move_to([-0.75, 0.25, 0])
        # Placed inside light_wash in the open gap between the top and middle discs
        dim_lbl = T("dim light", 24, C_LIGHT).move_to([-2.45, 1.55, 0])
        q = question_card("Steady light: do the channels stay shut?", color=TEXT)

        P = make_current_plot()
        stag = scope_tag("schematic")
        t = ValueTracker(0.5)

        trace_fn = lambda x: (
            0.20 + 0.32 / (1.0 + np.exp(-2.5 * (x - 3.0)))
            - 0.32 * np.exp(-((x - 8.2) / 0.55) ** 2)
        )
        live = P.live_curve(trace_fn, t, color=C_CURRENT, width=5)
        dot = P.dot(lambda: t.get_value(), lambda: trace_fn(t.get_value()), color=C_CURRENT, ring=TEXT, radius=0.09)

        self.add(world, light_wash, gcaps, dim_lbl, q)
        self.play(FadeOut(q), run_time=0.35)
        self.play(FadeIn(P), FadeIn(stag), run_time=0.45)
        self.add(live, dot)

        self.at("the faster cyclase")
        fb_arrow = CurvedArrow([-4.15, -0.55, 0], [-1.35, -0.38, 0], angle=0.45, color=C_CA, stroke_width=4.5)
        self.play(
            Create(fb_arrow),
            world.cgmp_gauge.tracker.animate.set_value(0.48),
            t.animate(rate_func=linear).set_value(3.2),
            run_time=2.5
        )

        self.at("some channels reopen")
        self.play(
            world.channels[0].tracker.animate.set_value(0.75),
            world.channels[0].cgmp_dot.animate.set_opacity(1.0),
            world.flow_tr.animate.set_value(0.55),
            t.animate(rate_func=linear).set_value(5.6),
            run_time=2.0
        )

        self.at("This negative feedback")
        fb_lbl = T("negative feedback", 24, C_CA).move_to([-2.55, -1.32, 0])
        self.play(FadeIn(fb_lbl), t.animate(rate_func=linear).set_value(7.1), run_time=2.5)

        rest_t = self.t_of("has current left") - 0.2 - self.elapsed()
        if rest_t > 0.1:
            self.play(t.animate(rate_func=linear).set_value(7.6), run_time=rest_t)

        cur_lbl = T("Current left to shut off", 26, C_CURRENT).move_to([1.35, -1.45, 0])
        self.play(FadeIn(cur_lbl, shift=UP * 0.08), run_time=0.7)

        self.at("an extra flash")
        flash = Arrow([-3.95, 2.1, 0], [-2.75, 2.1, 0], color=C_LIGHT, stroke_width=7, buff=0.0)
        flash_lbl = T("extra flash", 24, C_LIGHT).move_to([-2.45, 2.65, 0])
        self.play(
            FadeIn(flash), FadeIn(flash_lbl),
            t.animate(rate_func=linear).set_value(9.8),
            world.flow_tr.animate.set_value(0.15),
            run_time=2.0
        )
        self.finish()


class S09NoseContrast(SpokenScene):
    def construct(self):
        tp = TwoPanel("Eye: rod cell", "Nose: olfactory neuron", colors=(C_CGMP, C_CAMP),
                      top=3.2, bottom=-2.7, gap=0.45, width=12.8, size=30)

        def _panel_shell(x0, x1, y0, y1, ch_y):
            cyto = Polygon([x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0],
                           stroke_width=0, fill_color=C_CYTOSOL, fill_opacity=0.55)
            cyto.set_z_index(-6)
            walls = VGroup(
                Line([x0, y0, 0], [x0, y1, 0], color=GREY, stroke_width=3),
                Line([x0, y1, 0], [x1, y1, 0], color=GREY, stroke_width=3),
                Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3),
                Line([x1, y1, 0], [x1, ch_y + 0.28, 0], color=GREY, stroke_width=3),
                Line([x1, ch_y - 0.28, 0], [x1, y0, 0], color=GREY, stroke_width=3),
            )
            shell = VGroup(cyto, walls)
            shell.walls = walls
            return shell

        # Left panel: rod world with live drifting cGMP dots & turning PDE6
        rod_shell = _panel_shell(-5.9, -0.9, -1.8, 1.9, 0.2)
        rod_disc = Ellipse(width=1.4, height=0.45, color=GREY, stroke_width=2.5,
                           fill_color=C_LIGHT, fill_opacity=0.22).move_to([-4.9, 1.1, 0])
        rod_pde_c = Circle(radius=0.28, color=C_PDE, stroke_width=3, fill_color=C_PDE, fill_opacity=0.25).move_to([-2.9, 1.1, 0])
        rod_spokes = VGroup(*[
            Line([-2.9, 1.1, 0] + 0.08 * np.array([np.cos(a), np.sin(a), 0]),
                 [-2.9, 1.1, 0] + 0.24 * np.array([np.cos(a), np.sin(a), 0]),
                 color=C_PDE, stroke_width=3)
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ])
        rod_spokes.add_updater(lambda m, dt: m.rotate(1.8 * dt, about_point=[-2.9, 1.1, 0]))
        rod_dots = make_cytosol_dots(count=6, color=C_CGMP, x_range=(-4.5, -1.6), y_range=(-0.1, 0.7), seed=61, radius=0.075)
        add_drift_updater(rod_dots, x_range=(-4.5, -1.6), y_range=(-0.1, 0.7))

        rod_gauge = make_gauge(-5.3, y0=-1.45, y1=0.25, width=0.42, color=C_CGMP, label="cGMP",
                               init_val=0.20, label_size=24)
        rod_ch = make_channel(0.2, x=-0.9, open_frac=0.0)
        rod_lbl_light = T("light -> cGMP falls", 24, C_CGMP).move_to([-2.95, -0.55, 0])
        rod_lbl_shut = T("channel shuts", 24, C_CURRENT).move_to([-2.55, -1.30, 0])
        left_group = VGroup(rod_shell, rod_disc, rod_pde_c, rod_spokes, rod_dots, rod_gauge, rod_ch, rod_lbl_light, rod_lbl_shut)

        # Right panel: olfactory sensory neuron (cleanly spaced labels)
        nose_shell = _panel_shell(0.9, 5.9, -1.8, 1.9, 0.95)
        rec = RoundedRectangle(corner_radius=0.14, width=0.65, height=0.85, stroke_color=C_CAMP,
                               stroke_width=3, fill_color=C_CAMP, fill_opacity=0.22).move_to([0.9, 1.0, 0])
        rec_lbl = T("odorant receptor", 24, C_CAMP).move_to([2.4, 2.25, 0])
        odorant = Dot([0.45, -0.2, 0], radius=0.13, color=C_CAMP)

        g_prot = chip("G protein", TEXT, size=24, pad=0.12).move_to([2.90, 1.25, 0])
        g_prot_on = chip("G protein", C_LIGHT, size=24, pad=0.12).move_to([2.90, 1.25, 0])

        ac = Ellipse(width=1.10, height=0.54, color=C_CYCLASE, stroke_width=3,
                     fill_color=C_CYCLASE, fill_opacity=0.28).move_to([4.15, 0.35, 0])
        ac_lbl = T("adenylyl cyclase", 24, C_CYCLASE).move_to([4.15, -0.25, 0])

        camp_gauge = make_gauge(1.70, y0=-1.45, y1=0.15, width=0.45, color=C_CAMP, label="cAMP",
                                init_val=0.15, label_size=24)
        camp_dots = make_cytosol_dots(count=9, color=C_CAMP, x_range=(2.6, 5.4), y_range=(-1.45, -0.6), seed=53, radius=0.075)
        camp_dots.set_opacity(0.0)
        add_drift_updater(camp_dots, x_range=(2.6, 5.4), y_range=(-1.45, -0.6))

        nose_ch = make_channel(0.95, x=5.9, open_frac=0.0)
        nose_flow = ValueTracker(0.0)
        nose_ions = make_ion_stream(ys=(0.95,), colors=(C_CURRENT,), flow_tracker=nose_flow)
        nose_ions.clear_updaters()
        for k, d in enumerate(nose_ions):
            d.move_to([6.15 - k * 0.25, 0.95, 0])

        def _nose_ion_u(mob, dt):
            f = nose_flow.get_value()
            for d in mob:
                if f <= 0.05:
                    d.set_opacity(0.0)
                    continue
                d.set_opacity(1.0)
                d.shift(LEFT * 0.95 * dt)
                if d.get_center()[0] < 4.9:
                    d.move_to([6.18, 0.95, 0])

        nose_ions.add_updater(_nose_ion_u)
        stag = scope_tag("schematic")

        self.add(tp, left_group, stag)
        self.at("Each olfactory neuron")
        self.play(
            FadeIn(nose_shell), FadeIn(rec), FadeIn(rec_lbl),
            FadeIn(g_prot), FadeIn(ac), FadeIn(ac_lbl),
            FadeIn(camp_gauge), FadeIn(nose_ch),
            run_time=1.4
        )
        self.add(camp_dots, nose_ions)
        # Drift odorant into position while narrator describes receptor family
        self.play(FadeIn(odorant), odorant.animate(rate_func=linear).move_to([0.45, 1.0, 0]), run_time=3.5)

        self.at("When an odorant")
        self.play(odorant.animate.move_to([0.62, 1.0, 0]), run_time=0.8)

        self.at("a G protein activates")
        self.play(
            swap(g_prot, g_prot_on, run_time=0.6),
            ac.animate.set_fill(C_CYCLASE, opacity=0.55).set_stroke(width=4.5),
            run_time=1.3
        )

        self.at("rises")
        self.play(
            camp_gauge.tracker.animate.set_value(0.85),
            camp_dots.animate.set_opacity(0.92),
            run_time=1.4
        )

        self.at("opens a related")
        self.play(
            nose_ch.tracker.animate.set_value(1.0),
            nose_flow.animate.set_value(1.0),
            run_time=1.0
        )

        self.at("depolarizes and fires")
        dep_lbl = T("depolarizes & fires!", 26, C_CAMP).move_to([4.15, -2.22, 0])
        self.play(
            nose_shell.walls.animate.set_stroke(C_CAMP, width=5),
            FadeIn(dep_lbl),
            run_time=0.9
        )
        self.finish()


class S10Takehome(SpokenScene):
    def construct(self):
        head = T("Related cyclic-nucleotide channels, opposite wiring", 28, TEXT).move_to([0, 3.18, 0])

        rod_title = T("Rod: cGMP falls", 32, C_CGMP).move_to([-3.3, 2.38, 0])
        rod_g = make_gauge(-3.85, y0=-1.65, y1=1.75, width=1.45, color=C_CGMP,
                           label="", init_val=0.72, baseline=0.72)
        rod_base_lbl = T("dark baseline", 24, TEXT).next_to([-2.95, 0.80, 0], RIGHT, buff=0.22)
        rod_arrow = Arrow([-5.15, 0.80, 0], [-5.15, -0.95, 0], color=C_CGMP, stroke_width=8, buff=0.0)
        rod_arrow_lbl = T("light", 26, C_LIGHT).next_to(rod_arrow, LEFT, buff=0.20)

        nose_title = T("Nose: cAMP rises", 32, C_CAMP).move_to([3.3, 2.38, 0])
        nose_g = make_gauge(2.35, y0=-1.65, y1=1.75, width=1.45, color=C_CAMP,
                            label="", init_val=0.25, baseline=0.25)
        nose_base_lbl = T("rest baseline", 24, TEXT).next_to([3.25, -0.80, 0], RIGHT, buff=0.22)
        nose_arrow = Arrow([1.05, -0.80, 0], [1.05, 1.05, 0], color=C_CAMP, stroke_width=8, buff=0.0)
        nose_arrow_lbl = T("odorant", 26, C_CAMP).next_to(nose_arrow, LEFT, buff=0.22)

        rod_center = ValueTracker(0.72)
        nose_center = ValueTracker(0.25)
        t_clock = ValueTracker(0.0)
        t_clock.add_updater(lambda m, dt: m.increment_value(dt))

        def _pulse_gauges(mob, dt):
            s = t_clock.get_value()
            rod_g.tracker.set_value(rod_center.get_value() + 0.04 * np.sin(3.6 * s))
            nose_g.tracker.set_value(nose_center.get_value() + 0.04 * np.sin(3.6 * s + 1.2))

        rod_g.add_updater(_pulse_gauges)
        self.add(t_clock, head, rod_title, rod_g, rod_base_lbl, nose_title, nose_g, nose_base_lbl)

        self.at("opposite directions")
        self.play(Indicate(rod_title, color=C_CGMP), Indicate(nose_title, color=C_CAMP), run_time=1.0)

        self.at("Light drives")
        self.play(
            rod_center.animate.set_value(0.22),
            GrowArrow(rod_arrow),
            FadeIn(rod_arrow_lbl),
            run_time=1.4
        )

        self.at("An odorant drives")
        self.play(
            nose_center.animate.set_value(0.80),
            GrowArrow(nose_arrow),
            FadeIn(nose_arrow_lbl),
            run_time=1.4
        )

        self.at("Keep this rule")
        rule = caption("A signal is a change from baseline, up or down.", size=32, color=C_LIGHT, y=-2.85)
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)

        self.at("A signal is")
        self.play(Indicate(rule, color=TEXT, scale_factor=1.03), run_time=1.0)
        self.finish()


class S11End(EndCard):
    LINE = "A signal is a change from baseline, up or down."
