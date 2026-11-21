"""
COLOUR MAP (one colour per concept across the whole film):
    TEAL   (#2EC4B6) : Blood vessel and bulk circulation flow
    YELLOW (#F5D547) : Messenger molecules and paracrine signal cloud
    GREEN  (#83C167) : Target cells and receptor cups (brighten when lit)
    GOLD   (#D4A843) : Lifetime (tau) gauges/bars, concentration & reach curves, brackets, clocks, predict prompts
    RED    (#FC6255) : Stop / warning cues, stuck signal, crossed-out claim, drug-block questions
    CORAL  (#FF8B5E) : Clearing enzymes (extracellular destruction, acetylcholinesterase)
    BLUE   (#58B4FF) : Reuptake transporters (sender membrane pumps, serotonin transporter)
    PURPLE (#B589FF) : Sticky extracellular matrix fibers and protective binding
    GREY   (#8B93A1) : Axes, structural reference lines, schematic scope tag
    TEXT   (#E8EAF0) : Labels, equations, and readouts

CARRIED WORLD:
    A 16:9 cross-section with a narrow synaptic gap upper-left (sender with BLUE transporter, CORAL enzyme
    in cleft, GREEN receiver cups), a paracrine tissue field centre-right (sending cell at left, GREEN
    receptor-bearing cells across uniform space), and a TEAL blood vessel running along the bottom.

WHAT CHANGES ON SCREEN (per spoken scene, and what it is computed from):
    s00_link_and_question     : Messenger dots advect along the TEAL vessel and cross the gap, lighting GREEN cups;
                                a trapped dot locks one cup ON while a RED toggle pulses (sine glow).
    s02_three_routes          : Random-walk messenger dots (fixed RNG seed 2) are cut by CORAL enzyme, pumped
                                back through BLUE transporter, and swept down into the TEAL vessel; GOLD tau gauge updates.
    s03_lifetime_and_fade     : Random-walk dots (seed 3) diffuse and clear at fractional rate 1/tau; GOLD curve
                                computes C(x) = exp(-x/lambda) and brackets lambda = sqrt(D * tau) at y = 1/e.
    s04_guiding_idea          : Single ValueTracker for tau shrinks then stretches the GOLD bar, contracts then
                                expands the computed exp(-x/sqrt(D*tau)) curve and dot cloud, and drives exp(-t/tau)
                                decay plus GOLD clock rotation when release halts.
    s05_predict_question      : Calibrated distance axis (D = 10^-6 cm^2/s) builds tau = 4 s -> 20 um cloud;
                                GOLD bar stretches 25x to 100 s and two dashed candidate arrows extend.
    s07_reveal                : RED X crosses out 500 um?; inset Plot draws computed r(tau) = 10*sqrt(tau) through
                                (4, 20) and (100, 100); cloud and bracket expand 5x to 100 um, then decay 25x slower.
    s08_sticky_tissue         : PURPLE matrix fibers weave through tissue; bound dots pause on fibers (lower D);
                                GOLD bracket shrinks 32x from 100 um (D=10^-6) to ~3 um (D=10^-9); shield deflects enzyme.
    s09_synapse_extreme       : Continuous cleaving + three rapid bursts cross the cleft and are snapped cleanly off by
                                CORAL enzyme, generating 3 distinct GREEN impulse spikes; enzyme swaps to BLUE pump.
    s10_blood_changes_bargain : Hormone dots sweep fast along TEAL flow; when gland stops, computed Plot traces
                                C(t) = 100 * 2^(-t/2.5) through half-life 2.5 min while vessel dots thin proportionally.
    s11_handoff               : Full world zooms back out; fast synapse vs lingering tissue highlight, then two
                                RED '?' drug-block badges slide partway toward CORAL enzyme and BLUE transporter.
"""

from bp_parts import *

# Override palette additions / distinct hues for this film's concept map
TEAL = "#2EC4B6"
BLUE = "#58B4FF"
CORAL = "#FF8B5E"
PURPLE = "#B589FF"


def _make_cup(pos, angle=0.0, scale=1.0, color=GREEN, lit=False):
    """U-shaped surface receptor cup pointing outward along `angle`."""
    r = 0.16 * scale
    arc = Arc(radius=r, start_angle=PI * 0.25, angle=PI * 1.5, stroke_color=color,
              stroke_width=4.5 if lit else 3.2)
    stem = Line([0, -r, 0], [0, -r - 0.12 * scale, 0], color=color, stroke_width=3.5)
    g = VGroup(arc, stem).rotate(angle)
    g.move_to(pos)
    return g


def _make_cell(center, w=1.0, h=0.85, color=GREEN, fill_op=0.14, cups=()):
    """Simple rounded cell body with optional receptor cups along its perimeter."""
    body = RoundedRectangle(corner_radius=min(0.28, h * 0.35), width=w, height=h,
                            stroke_color=color, stroke_width=3.0,
                            fill_color=color, fill_opacity=fill_op).move_to(center)
    g = VGroup(body)
    for offset, ang in cups:
        g.add(_make_cup(np.array(center) + np.array(offset), angle=ang, color=color, scale=0.85))
    g.body = body
    return g


def _make_enzyme(pos, scale=1.0, color=CORAL):
    """Notched wedge block representing a clearing enzyme (no molecular structure)."""
    r = 0.24 * scale
    sector = Sector(radius=r, start_angle=0.45, angle=TAU - 0.9,
                    fill_color=color, fill_opacity=0.85, stroke_color=color, stroke_width=2.5)
    sector.move_to(pos)
    return sector


def _make_transporter(pos, vertical=True, color=BLUE, scale=1.0):
    """Two parallel channel bars representing a membrane reuptake transporter."""
    gap = 0.14 * scale
    length = 0.34 * scale
    if vertical:
        a = RoundedRectangle(corner_radius=0.05, width=length, height=0.10 * scale,
                             fill_color=color, fill_opacity=0.85, stroke_color=color, stroke_width=2).shift(UP * gap)
        b = RoundedRectangle(corner_radius=0.05, width=length, height=0.10 * scale,
                             fill_color=color, fill_opacity=0.85, stroke_color=color, stroke_width=2).shift(DOWN * gap)
    else:
        a = RoundedRectangle(corner_radius=0.05, width=0.10 * scale, height=length,
                             fill_color=color, fill_opacity=0.85, stroke_color=color, stroke_width=2).shift(LEFT * gap)
        b = RoundedRectangle(corner_radius=0.05, width=0.10 * scale, height=length,
                             fill_color=color, fill_opacity=0.85, stroke_color=color, stroke_width=2).shift(RIGHT * gap)
    return VGroup(a, b).move_to(pos)


def _make_vessel(y_center=-1.85, height=0.88, x0=-6.3, x1=6.3):
    """Carried TEAL blood vessel spanning the bottom."""
    lumen = Rectangle(width=x1 - x0, height=height, fill_color=TEAL, fill_opacity=0.18,
                      stroke_width=0).move_to([(x0 + x1) / 2, y_center, 0])
    top_wall = Line([x0, y_center + height / 2, 0], [x1, y_center + height / 2, 0],
                    color=TEAL, stroke_width=3.5)
    bot_wall = Line([x0, y_center - height / 2, 0], [x1, y_center - height / 2, 0],
                    color=TEAL, stroke_width=3.5)
    chevrons = VGroup()
    for x in np.linspace(x0 + 1.0, x1 - 1.0, 6):
        c = VGroup(
            Line([x - 0.14, y_center + 0.12, 0], [x + 0.04, y_center, 0], color=TEAL, stroke_width=2.5),
            Line([x - 0.14, y_center - 0.12, 0], [x + 0.04, y_center, 0], color=TEAL, stroke_width=2.5),
        ).set_opacity(0.55)
        chevrons.add(c)
    g = VGroup(lumen, top_wall, bot_wall, chevrons)
    g.y_center, g.height, g.x0, g.x1 = y_center, height, x0, x1
    g.chevrons = chevrons
    return g


def _attach_vessel_flow(vessel, dots, rng, speed=2.6):
    """Advect hormone dots and flow chevrons continuously along the TEAL vessel."""
    x0, x1 = vessel.x0 + 0.15, vessel.x1 - 0.15
    yc, hh = vessel.y_center, vessel.height * 0.34
    for d in dots:
        d._vx = speed * rng.uniform(0.85, 1.15)
        d._vy = rng.uniform(-0.08, 0.08)

    def u_dots(mob, dt):
        for d in mob:
            p = d.get_center()
            nx = p[0] + d._vx * dt
            ny = p[1] + d._vy * dt
            if nx > x1:
                nx = x0 + (nx - x1)
            if abs(ny - yc) > hh:
                d._vy *= -1
                ny = np.clip(ny, yc - hh, yc + hh)
            d.move_to([nx, ny, 0])

    def u_chev(mob, dt):
        for c in mob:
            c.shift(RIGHT * speed * 0.55 * dt)
            if c.get_center()[0] > x1:
                c.shift(LEFT * (x1 - x0))

    dots.add_updater(u_dots)
    vessel.chevrons.add_updater(u_chev)


def _make_full_world(rng):
    """Build the carried 16:9 world shared by s00_link_and_question and s11_handoff."""
    # 1. Upper-left synaptic gap (x: -5.9..-1.1, y: 0.9..2.6)
    syn_sender = RoundedRectangle(corner_radius=0.35, width=2.0, height=1.7,
                                  stroke_color=TEXT, stroke_width=3.0,
                                  fill_color=TEXT, fill_opacity=0.07).move_to([-4.8, 1.75, 0])
    syn_receiver = RoundedRectangle(corner_radius=0.35, width=1.8, height=1.7,
                                    stroke_color=GREEN, stroke_width=3.2,
                                    fill_color=GREEN, fill_opacity=0.14).move_to([-2.0, 1.75, 0])
    syn_cups = VGroup(
        _make_cup([-2.92, 2.15, 0], angle=PI * 0.5, scale=0.85, color=GREEN, lit=True),
        _make_cup([-2.92, 1.35, 0], angle=PI * 0.5, scale=0.85, color=GREEN, lit=True),
    )
    syn_enzyme = _make_enzyme([-3.35, 1.85, 0], scale=0.85, color=CORAL)
    syn_transporter = _make_transporter([-3.80, 1.35, 0], vertical=True, color=BLUE, scale=0.9)

    syn_dots = VGroup()
    for i in range(6):
        d = Dot(radius=0.075, color=YELLOW).move_to([
            rng.uniform(-3.65, -3.0), rng.uniform(1.1, 2.4), 0
        ])
        d._phase = rng.uniform(0, 1)
        syn_dots.add(d)

    # 2. Centre-right paracrine tissue field (x: -0.3..6.0, y: -0.7..2.85)
    para_sender = RoundedRectangle(corner_radius=0.32, width=1.1, height=1.55,
                                   stroke_color=TEXT, stroke_width=3.0,
                                   fill_color=TEXT, fill_opacity=0.08).move_to([0.25, 1.05, 0])
    tissue_centers = [
        ([2.0, 2.1, 0], True),
        ([3.8, 2.25, 0], False),
        ([5.3, 1.75, 0], False),
        ([2.2, 0.25, 0], True),
        ([3.9, 0.4, 0], False),
        ([5.4, 0.05, 0], False),
    ]
    tissue_cells = VGroup()
    for pos, is_lit in tissue_centers:
        c = _make_cell(pos, w=1.15, h=0.9, color=GREEN,
                       fill_op=0.34 if is_lit else 0.20,
                       cups=[([-0.6, 0.0, 0], PI * 0.5)])
        tissue_cells.add(c)

    para_dots = VGroup()
    for _ in range(18):
        x = rng.uniform(0.9, 4.6)
        y = rng.uniform(-0.4, 2.5)
        d = Dot(radius=0.075, color=YELLOW).move_to([x, y, 0])
        d._vx = rng.uniform(0.35, 0.75)
        d._vy = rng.uniform(-0.28, 0.28)
        para_dots.add(d)

    # 3. Bottom TEAL blood vessel
    vessel = _make_vessel(y_center=-1.85, height=0.92, x0=-6.3, x1=6.3)
    vessel_dots = VGroup(*[
        Dot(radius=0.08, color=YELLOW).move_to([rng.uniform(-6.0, 6.0), rng.uniform(-2.15, -1.55), 0])
        for _ in range(16)
    ])

    world = VGroup(
        vessel, vessel_dots,
        syn_sender, syn_receiver, syn_cups, syn_enzyme, syn_transporter, syn_dots,
        para_sender, tissue_cells, para_dots,
    )
    world.syn_sender = syn_sender
    world.syn_receiver = syn_receiver
    world.syn_cups = syn_cups
    world.syn_enzyme = syn_enzyme
    world.syn_transporter = syn_transporter
    world.syn_dots = syn_dots
    world.para_sender = para_sender
    world.tissue_cells = tissue_cells
    world.para_dots = para_dots
    world.vessel = vessel
    world.vessel_dots = vessel_dots
    return world


def _attach_world_motion(world, rng):
    _attach_vessel_flow(world.vessel, world.vessel_dots, rng, speed=2.6)

    def u_syn(mob, dt):
        for d in mob:
            p = d.get_center()
            nx = p[0] + 0.95 * dt
            ny = p[1] + 0.25 * np.sin(nx * 5 + d._phase * TAU) * dt
            if nx > -2.95:
                nx = -3.72
                ny = rng.uniform(1.15, 2.35)
            d.move_to([nx, ny, 0])

    def u_para(mob, dt):
        for d in mob:
            p = d.get_center()
            nx = p[0] + d._vx * dt
            ny = p[1] + d._vy * dt
            if ny > 2.6 or ny < -0.55:
                d._vy *= -1
                ny = np.clip(ny, -0.55, 2.6)
            if nx > 5.7:
                nx = 0.85
                ny = rng.uniform(0.35, 1.75)
            d.move_to([nx, ny, 0])

    world.syn_dots.add_updater(u_syn)
    world.para_dots.add_updater(u_para)


def _make_tau_bar(value_tracker, max_tau=10.0, pos=(4.3, 3.15, 0), width=2.8, label_text="lifetime (τ)"):
    """GOLD gauge bar whose filled width tracks `value_tracker`."""
    bg = RoundedRectangle(corner_radius=0.08, width=width, height=0.28,
                          stroke_color=GOLD, stroke_width=2.2, fill_color=BG, fill_opacity=0.85).move_to(pos)
    left_x = bg.get_left()[0] + 0.03
    inner_w = width - 0.06
    fill = always_redraw(lambda: Rectangle(
        width=max(0.06, inner_w * np.clip(value_tracker.get_value() / max_tau, 0.02, 1.0)),
        height=0.20, fill_color=GOLD, fill_opacity=0.88, stroke_width=0
    ).move_to([left_x + max(0.06, inner_w * np.clip(value_tracker.get_value() / max_tau, 0.02, 1.0)) / 2, pos[1], 0]))
    lab = T(label_text, size=24, color=GOLD).next_to(bg, LEFT, buff=0.22)
    g = VGroup(bg, fill, lab)
    g.bg, g.fill, g.lab = bg, fill, lab
    return g


def _make_clock(phase_tracker, center=(5.0, 1.0, 0), radius=0.62, color=GOLD):
    """GOLD clock face whose hand angle follows phase_tracker (1 unit = 1 turn)."""
    rim = Circle(radius=radius, stroke_color=color, stroke_width=3.5, fill_color=BG, fill_opacity=0.85).move_to(center)
    ticks = VGroup(*[
        Line(
            np.array(center) + 0.80 * radius * np.array([np.cos(a), np.sin(a), 0]),
            np.array(center) + 0.94 * radius * np.array([np.cos(a), np.sin(a), 0]),
            color=color, stroke_width=2.2,
        )
        for a in np.linspace(0, TAU, 12, endpoint=False)
    ])
    hub = Dot(center, radius=0.05, color=color)
    hand = always_redraw(lambda: Line(
        center,
        np.array(center) + 0.72 * radius * np.array([
            np.sin(phase_tracker.get_value() * TAU),
            np.cos(phase_tracker.get_value() * TAU),
            0.0,
        ]),
        color=color, stroke_width=4.0,
    ))
    return VGroup(rim, ticks, hub, hand)


def _make_reach_bracket(x_start, length_fn, y, label_str_or_fn, color=GOLD, size=26, label_right=False):
    """Dynamic horizontal GOLD bracket spanning [x_start, x_start + length_fn()] at height y."""
    def mk_bar():
        L = max(0.18, float(length_fn()))
        x1 = x_start + L
        main = Line([x_start, y, 0], [x1, y, 0], color=color, stroke_width=3.5)
        t0 = Line([x_start, y - 0.12, 0], [x_start, y + 0.12, 0], color=color, stroke_width=3.5)
        t1 = Line([x1, y - 0.12, 0], [x1, y + 0.12, 0], color=color, stroke_width=3.5)
        return VGroup(main, t0, t1)

    bar = always_redraw(mk_bar)
    if label_right:
        if callable(label_str_or_fn):
            lab = always_redraw(lambda: T(label_str_or_fn(), size=size, color=color).move_to(
                [x_start + max(0.18, float(length_fn())) + 0.22, y, 0], aligned_edge=LEFT
            ))
        else:
            lab = T(label_str_or_fn, size=size, color=color).move_to(
                [x_start + max(0.18, float(length_fn())) + 0.22, y, 0], aligned_edge=LEFT
            )
    else:
        if callable(label_str_or_fn):
            lab = always_redraw(lambda: T(label_str_or_fn(), size=size, color=color).move_to(
                [np.clip(x_start + max(0.18, float(length_fn())) / 2, -4.4, 4.4), y + 0.34, 0]
            ))
        else:
            lab = T(label_str_or_fn, size=size, color=color).move_to(
                [np.clip(x_start + max(0.18, float(length_fn())) / 2, -4.4, 4.4), y + 0.34, 0]
            )
    return VGroup(bar, lab), bar, lab


# ==============================================================================
# SCENE 00: Link & Question (14.45 s spoken)
# ==============================================================================
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(1)
        world = _make_full_world(rng)
        _attach_world_motion(world, rng)
        tag = scope_tag("schematic")
        self.add(world, tag)

        # Beat 1: Blood carries far signals
        lbl_blood = T("blood: far signals", size=26, color=TEAL).move_to([0.0, -0.98, 0])
        self.play(FadeIn(lbl_blood, shift=UP * 0.08), run_time=0.45)

        # Beat 2: tiny gaps pass fast ones
        self.at("tiny gaps")
        lbl_gap = T("tiny gap: fast", size=26, color=YELLOW).move_to([-3.4, 3.02, 0])
        self.play(FadeIn(lbl_gap, shift=UP * 0.08), run_time=0.4)

        # Beat 3: receptors choose who answers
        self.at("and receptors")
        lbl_rec = T("receptors answer", size=26, color=GREEN).move_to([3.7, 3.12, 0])
        lit_target = world.tissue_cells[0]
        self.play(
            FadeIn(lbl_rec, shift=UP * 0.08),
            lit_target.body.animate.set_fill(GREEN, opacity=0.42),
            run_time=0.5,
        )

        # Beat 4: Once a message turns a cell on
        self.at("turns a cell on")
        self.play(FadeOut(lbl_blood), FadeOut(lbl_gap), FadeOut(lbl_rec), run_time=0.35)

        focus_cell = world.tissue_cells[0]
        cup_pos = focus_cell[1].get_center()
        trapped_dot = Dot(cup_pos + LEFT * 0.04, radius=0.095, color=YELLOW,
                          stroke_color=RED, stroke_width=2.5)
        focus_ring = Circle(radius=0.34, color=RED, stroke_width=3.5).move_to(cup_pos)

        toggle_bg = RoundedRectangle(corner_radius=0.25, width=1.34, height=0.54,
                                     stroke_color=RED, stroke_width=3.0,
                                     fill_color=RED, fill_opacity=0.22).move_to([-0.3, 3.0, 0])
        toggle_knob = Dot(toggle_bg.get_right() + LEFT * 0.25, radius=0.17, color=RED)
        toggle_on = T("ON", size=24, color=TEXT).move_to(toggle_bg.get_left() + RIGHT * 0.40)
        toggle = VGroup(toggle_bg, toggle_knob, toggle_on)

        self.play(FadeIn(trapped_dot), Create(focus_ring), FadeIn(toggle), run_time=0.5)

        # Beat 5: what shuts it off?
        self.at("what shuts it off")
        q_mark = T("?", size=56, color=GOLD, font=TITLE_FONT).move_to([-3.35, 2.95, 0])
        self.play(FadeIn(q_mark, shift=UP * 0.25), run_time=0.5)

        # Beat 6: switch stuck on
        self.at("switch stuck on")
        lbl_stuck = T("switch stuck on", size=28, color=RED).next_to(toggle, RIGHT, buff=0.25)
        pulse(toggle_bg, base=3.5, amp=2.2, speed=5.5)
        pulse(focus_ring, base=3.5, amp=2.0, speed=5.5)
        self.play(FadeIn(lbl_stuck, shift=RIGHT * 0.1), run_time=0.45)
        self.finish()


# ==============================================================================
# SCENE 01: Title Card (2.0 s silent)
# ==============================================================================
class S01Title(TitleCard):
    LESSON = "Signals and How Far They Travel"
    TITLE = "How Signals End: Clearance Sets Lifetime"


# ==============================================================================
# SCENE 02: Three Routes (17.4 s spoken)
# ==============================================================================
class S02ThreeRoutes(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(2)

        sender_wall = RoundedRectangle(corner_radius=0.3, width=2.4, height=3.8,
                                       stroke_color=TEXT, stroke_width=3.0,
                                       fill_color=TEXT, fill_opacity=0.07).move_to([-4.9, 0.7, 0])
        sender_lbl = T("sender", size=26, color=TEXT).move_to([-5.0, 2.1, 0])

        receiver_wall = RoundedRectangle(corner_radius=0.3, width=2.4, height=3.8,
                                         stroke_color=GREEN, stroke_width=3.2,
                                         fill_color=GREEN, fill_opacity=0.14).move_to([4.9, 0.7, 0])
        receiver_lbl = T("receiver", size=26, color=GREEN).move_to([5.0, 2.1, 0])
        rec_cups = VGroup(
            _make_cup([3.68, 1.45, 0], angle=PI * 0.5, scale=1.0, color=GREEN, lit=True),
            _make_cup([3.68, 0.55, 0], angle=PI * 0.5, scale=1.0, color=GREEN, lit=True),
            _make_cup([3.68, -0.35, 0], angle=PI * 0.5, scale=1.0, color=GREEN, lit=True),
        )

        vessel = _make_vessel(y_center=-2.15, height=0.82, x0=-6.3, x1=6.3)
        vessel_dots = VGroup(*[
            Dot(radius=0.075, color=YELLOW).move_to([rng.uniform(-6.0, 6.0), rng.uniform(-2.4, -1.9), 0])
            for _ in range(12)
        ])
        _attach_vessel_flow(vessel, vessel_dots, rng, speed=2.6)

        tau_tr = ValueTracker(5.0)
        tau_bar = _make_tau_bar(tau_tr, max_tau=10.0, pos=(4.3, 3.22, 0), width=2.6, label_text="lifetime")
        tag = scope_tag("schematic")

        dots = VGroup()
        for i in range(20):
            role = i % 3
            d = Dot(radius=0.085, color=YELLOW).move_to([
                rng.uniform(-3.3, 2.9), rng.uniform(-0.8, 1.9), 0
            ])
            d._role = role
            d._vx = rng.uniform(0.35, 0.75)
            d._vy = rng.uniform(-0.2, 0.2)
            d._fade = 1.0
            dots.add(d)

        active_routes = {"enzyme": False, "pump": False, "flow": False}

        def u_dots(mob, dt):
            for d in mob:
                p = d.get_center()
                nx = p[0] + d._vx * dt + rng.normal(0, 0.25 * np.sqrt(dt))
                ny = p[1] + d._vy * dt + rng.normal(0, 0.25 * np.sqrt(dt))

                if active_routes["enzyme"] and d._role == 0 and nx > -1.3:
                    d._fade = max(0.0, d._fade - 1.6 * dt)
                    d.set_opacity(d._fade)
                    if d._fade <= 0.05:
                        nx, ny = -3.4, rng.uniform(0.8, 1.85)
                        d._fade = 1.0
                        d.set_opacity(1.0)
                elif active_routes["pump"] and d._role == 1 and nx > -2.4:
                    target = np.array([-4.5, 0.25, 0])
                    vec = target - np.array([nx, ny, 0])
                    dist = np.linalg.norm(vec)
                    if dist > 0.15:
                        step = vec / dist * 2.2 * dt
                        nx, ny = nx + step[0], ny + step[1]
                    if nx < -4.2:
                        nx, ny = -3.3, rng.uniform(-0.2, 0.8)
                elif active_routes["flow"] and d._role == 2:
                    ny -= 1.2 * dt
                    nx += 0.9 * dt
                    if ny < -2.1:
                        nx, ny = rng.uniform(-1.5, 0.8), rng.uniform(0.2, 1.6)
                else:
                    if ny > 1.9 or ny < -1.0:
                        d._vy *= -1
                        ny = np.clip(ny, -1.0, 1.9)
                    if nx > 3.4 or nx < -3.55:
                        nx = -3.4
                        ny = rng.uniform(-0.5, 1.85)
                d.move_to([nx, ny, 0])

        dots.add_updater(u_dots)
        self.add(sender_wall, sender_lbl, receiver_wall, receiver_lbl, rec_cups,
                 vessel, vessel_dots, dots, tag)

        # Beat 1: Enzymes destroy outside
        self.at("Enzymes can destroy")
        enz = _make_enzyme([-1.2, 1.45, 0], scale=1.25, color=CORAL)
        lbl_enz = T("enzyme destroys", size=28, color=CORAL).move_to([-1.2, 2.40, 0])
        active_routes["enzyme"] = True
        self.play(FadeIn(enz, scale=0.8), FadeIn(lbl_enz, shift=UP * 0.1),
                  FadeIn(tau_bar), tau_tr.animate.set_value(4.2), run_time=0.7)

        # Beat 2: Transporters pump back
        self.at("Transporters can pump")
        pump = _make_transporter([-3.7, 0.25, 0], vertical=True, color=BLUE, scale=1.2)
        pump_arrow = Arrow([-2.2, 0.25, 0], [-4.1, 0.25, 0], color=BLUE, stroke_width=4.5, buff=0.05)
        lbl_pump = T("transporter pumps back", size=26, color=BLUE).move_to([-1.55, -0.55, 0])
        active_routes["pump"] = True
        self.play(FadeIn(pump), GrowArrow(pump_arrow), FadeIn(lbl_pump, shift=LEFT * 0.1),
                  tau_tr.animate.set_value(3.2), run_time=0.8)

        # Beat 3: Blood flow or diffusion sweeps away (sweeping curves on right, label cleanly above them)
        self.at("Blood flow or diffusion")
        sweep_a1 = CurvedArrow([1.5, 0.65, 0], [2.8, -1.55, 0], angle=-0.38, color=TEAL, stroke_width=4.5)
        sweep_a2 = CurvedArrow([0.65, 0.35, 0], [1.85, -1.55, 0], angle=-0.38, color=TEAL, stroke_width=4.5)
        lbl_flow = T("flow or diffusion", size=28, color=TEAL).move_to([1.75, 1.35, 0])
        active_routes["flow"] = True
        self.play(Create(sweep_a1), Create(sweep_a2), FadeIn(lbl_flow, shift=DOWN * 0.1),
                  tau_tr.animate.set_value(2.4), run_time=0.9)

        self.finish()


# ==============================================================================
# SCENE 03 & 04: Paracrine Stage
# ==============================================================================
def _build_paracrine_stage():
    """Shared paracrine field + Plot geometry carried across s03 and s04."""
    # Upper plot: x in [0, 3], box=(-4.2, 2.75, 0.62, 2.72)
    P = Plot(box=(-4.2, 2.75, 0.62, 2.72), xr=(0, 3.0), yr=(0, 1.05),
             xticks=[(0, "0")],
             yticks=[(0, "0"), (0.37, "1/3"), (1.0, "1")],
             xlabel="distance from source", ylabel="signal concentration",
             color=GREY, size=24, label_size=24)
    # Lower tissue field aligned in x (-4.2..2.75), well below xlabel (y ~ -0.05)
    sender = RoundedRectangle(corner_radius=0.25, width=1.45, height=1.75,
                              stroke_color=TEXT, stroke_width=3.0,
                              fill_color=TEXT, fill_opacity=0.08).move_to([-5.02, -1.85, 0])
    sender_lbl = T("sender", size=24, color=TEXT).move_to([-5.02, -1.85, 0])
    field = Rectangle(width=6.95, height=1.75, stroke_color=GREY, stroke_width=1.8,
                      fill_color=TEAL, fill_opacity=0.11).move_to([-0.725, -1.85, 0])
    cells = VGroup(*[
        _make_cell([x, -1.85 + (0.38 if i % 2 == 0 else -0.38), 0], w=0.92, h=0.64,
                   color=GREEN, fill_op=0.22)
        for i, x in enumerate([-3.2, -1.6, 0.0, 1.6])
    ])
    enzymes = VGroup(*[
        _make_enzyme([x, y, 0], scale=0.62, color=CORAL)
        for x, y in [(-2.4, -1.35), (-0.8, -2.35), (0.8, -1.35), (2.4, -2.25)]
    ])
    return P, sender, sender_lbl, field, cells, enzymes


class S03LifetimeAndFade(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(3)
        P, sender, sender_lbl, field, cells, enzymes = _build_paracrine_stage()

        tau_tr = ValueTracker(5.0)
        tau_bar = _make_tau_bar(tau_tr, max_tau=10.0, pos=(4.6, 3.22, 0), width=2.4, label_text="lifetime (τ)")
        tag = scope_tag("in this model")

        dots = VGroup()
        for _ in range(28):
            x_u = min(2.9, rng.exponential(1.0))
            d = Dot(radius=0.075, color=YELLOW).move_to([
                -4.2 + (x_u / 3.0) * 6.95, rng.uniform(-2.6, -1.1), 0
            ])
            d._life = rng.uniform(0.2, 1.0)
            dots.add(d)

        def u_walk(mob, dt):
            for d in mob:
                p = d.get_center()
                nx = p[0] + rng.normal(0.08 * dt, 0.72 * np.sqrt(dt))
                ny = p[1] + rng.normal(0.0, 0.55 * np.sqrt(dt))
                d._life -= dt * 0.35
                if d._life <= 0 or nx > 2.70 or nx < -4.22:
                    nx = -4.12 + rng.uniform(0, 0.35)
                    ny = rng.uniform(-2.45, -1.25)
                    d._life = rng.exponential(1.0)
                ny = np.clip(ny, -2.62, -1.08)
                d.set_opacity(np.clip(d._life, 0.15, 1.0))
                d.move_to([nx, ny, 0])

        dots.add_updater(u_walk)

        x_prog = ValueTracker(0.0)
        conc_fn = lambda x: np.exp(-x)

        def mk_area():
            x1 = x_prog.get_value()
            if x1 <= 0.05:
                return VMobject()
            xs = np.linspace(0, x1, 60)
            pts = [P.pt(0, 0)] + [P.pt(x, conc_fn(x)) for x in xs] + [P.pt(x1, 0)]
            return Polygon(*pts, fill_color=GOLD, fill_opacity=0.20, stroke_width=0)

        live_area = always_redraw(mk_area)
        live_curve = P.live_curve(conc_fn, x_prog, color=GOLD, width=5)

        self.add(P, sender, sender_lbl, field, cells, enzymes, dots, tau_bar, tag, live_area, live_curve)

        # Beat 1: called tau
        self.at("called tau")
        lbl_tau = T("τ = average\nsurvival time", size=26, color=GOLD).move_to([4.65, 2.25, 0])
        self.play(FadeIn(lbl_tau, shift=UP * 0.08), run_time=0.6)

        # Beat 2: loses the same fraction each second -> no sharp edge
        self.at("loses the same fraction")
        lbl_edge = T("no sharp edge", size=26, color=GOLD).move_to([0.9, 1.70, 0])
        self.play(x_prog.animate.set_value(3.0), run_time=3.5, rate_func=linear)
        self.play(FadeIn(lbl_edge, shift=UP * 0.08), run_time=0.5)

        # Beat 3: How fast a molecule wanders is diffusion coefficient D
        self.at("How fast a molecule")
        wander_lbl = T("D = how fast\nit wanders", size=26, color=YELLOW).move_to([4.65, -1.55, 0])
        highlight_dot = Dot([-2.8, -1.85, 0], radius=0.11, color=YELLOW, stroke_color=TEXT, stroke_width=2.5)
        traced = TracedPath(highlight_dot.get_center, stroke_color=YELLOW, stroke_width=2.5)
        self.add(traced, highlight_dot)

        def u_hi(m, dt):
            p = m.get_center()
            nx = np.clip(p[0] + rng.normal(0.15 * dt, 0.88 * np.sqrt(dt)), -3.9, 2.4)
            ny = np.clip(p[1] + rng.normal(0, 0.65 * np.sqrt(dt)), -2.55, -1.15)
            m.move_to([nx, ny, 0])

        highlight_dot.add_updater(u_hi)
        self.play(FadeIn(wander_lbl, shift=UP * 0.08), run_time=0.6)

        # Beat 4: Reach, where signal falls to about a third, is near sqrt(D * tau)
        self.at("Reach where")
        third_line = DashedLine(P.pt(0, np.exp(-1)), P.pt(1.0, np.exp(-1)), color=GREY, stroke_width=2.5)
        drop_line = DashedLine(P.pt(1.0, np.exp(-1)), P.pt(1.0, 0), color=GOLD, stroke_width=2.8)
        x_zero = P.pt(0, 0)[0]
        x_one = P.pt(1.0, 0)[0]
        # Place bracket cleanly at y=2.30, label to the right of t1 so it never touches y-tick '1' or the curve
        bracket_grp, _, _ = _make_reach_bracket(x_zero, lambda: x_one - x_zero, 2.30,
                                                "reach ≈ √(D × τ)", color=GOLD, size=26, label_right=True)
        self.play(Create(third_line), Create(drop_line), FadeIn(bracket_grp), run_time=1.0)
        self.finish()


class S04GuidingIdea(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(4)
        P, sender, sender_lbl, field, cells, enzymes = _build_paracrine_stage()

        tau_tr = ValueTracker(1.0)
        amp_tr = ValueTracker(1.0)
        clock_tr = ValueTracker(0.0)

        tau_bar = _make_tau_bar(tau_tr, max_tau=2.0, pos=(4.6, 3.22, 0), width=2.4, label_text="lifetime (τ)")
        clock = _make_clock(clock_tr, center=(4.75, 1.55, 0), radius=0.60, color=GOLD)
        tag = scope_tag("in this model")

        def mk_curve():
            lam = np.sqrt(max(tau_tr.get_value(), 0.12))
            amp = amp_tr.get_value()
            xs = np.linspace(0, 3.0, 100)
            pts = [P.pt(x, amp * np.exp(-x / lam)) for x in xs]
            m = VMobject(stroke_color=GOLD, stroke_width=5, fill_opacity=0)
            m.set_points_as_corners(pts)
            return m

        def mk_area():
            lam = np.sqrt(max(tau_tr.get_value(), 0.12))
            amp = amp_tr.get_value()
            xs = np.linspace(0, 3.0, 60)
            pts = [P.pt(0, 0)] + [P.pt(x, amp * np.exp(-x / lam)) for x in xs] + [P.pt(3.0, 0)]
            return Polygon(*pts, fill_color=GOLD, fill_opacity=0.20 * amp, stroke_width=0)

        live_area = always_redraw(mk_area)
        live_curve = always_redraw(mk_curve)

        dots = VGroup()
        for _ in range(30):
            u = rng.exponential(1.0)
            d = Dot(radius=0.075, color=YELLOW)
            d._u = min(2.9, u)
            d._y = rng.uniform(-2.6, -1.1)
            d.move_to([-4.2 + d._u / 3.0 * 6.95, d._y, 0])
            dots.add(d)

        def u_cloud(mob, dt):
            lam = np.sqrt(max(tau_tr.get_value(), 0.12))
            amp = amp_tr.get_value()
            for d in mob:
                d._u += rng.normal(0.32 * dt, 0.40 * np.sqrt(dt))
                x_u = d._u * lam
                if x_u < 0 or x_u > 2.95:
                    d._u = rng.uniform(0.0, 0.25)
                    x_u = d._u * lam
                ny = np.clip(d._y + rng.normal(0, 0.35 * np.sqrt(dt)), -2.6, -1.1)
                d._y = ny
                d.move_to([-4.2 + (x_u / 3.0) * 6.95, ny, 0])
                d.set_opacity(np.clip(amp * np.exp(-x_u / (2.5 * lam)), 0.05, 1.0))

        dots.add_updater(u_cloud)

        self.add(P, sender, sender_lbl, field, cells, enzymes, live_area, live_curve, dots, tau_bar, clock, tag)

        # Beat 1: short life first
        self.at("Clearance sets")
        lbl_case = T("short life: quick clear", size=26, color=GOLD).move_to([4.75, 0.20, 0])
        self.play(
            tau_tr.animate.set_value(0.28),
            FadeIn(lbl_case, shift=UP * 0.08),
            run_time=1.8,
        )

        # Beat 2: drops briskly when release halts
        self.at("When release stops")
        gate = Line(sender.get_corner(UR), sender.get_corner(DR), color=RED, stroke_width=6)
        self.play(Create(gate), run_time=0.25)
        self.play(
            amp_tr.animate.set_value(0.06),
            clock_tr.animate.set_value(1.0),
            run_time=1.8,
            rate_func=linear,
        )

        # Beat 3: switch to long life, wider cloud
        self.at("Longer life")
        lbl_long = T("long life: slow clear", size=26, color=GOLD).move_to([4.75, 0.20, 0])
        self.play(
            FadeOut(gate),
            swap(lbl_case, lbl_long, run_time=0.5),
            amp_tr.animate.set_value(1.0),
            tau_tr.animate.set_value(1.75),
            run_time=1.5,
        )

        # Beat 4: Longer life reaches farther, yet takes longer to clear
        self.at("yet takes longer")
        gate2 = Line(sender.get_corner(UR), sender.get_corner(DR), color=RED, stroke_width=6)
        self.play(Create(gate2), run_time=0.25)
        self.play(
            amp_tr.animate.set_value(0.48),
            clock_tr.animate.set_value(2.2),
            run_time=1.7,
            rate_func=linear,
        )
        self.finish()


# ==============================================================================
# SCENE 05, 06, 07: Water Predict, Pause, Reveal
# ==============================================================================
def _build_predict_world(rng, tau_seconds=4.0, show_arrows=False, cloud_um=20.0):
    """Shared calibrated 0..500 um water-upper-bound stage for s05, s06, s07."""
    x0, x500 = -4.6, 5.4
    um_to_x = lambda um: x0 + 0.02 * um

    sender = RoundedRectangle(corner_radius=0.22, width=1.18, height=1.50,
                              stroke_color=TEXT, stroke_width=3.0,
                              fill_color=TEXT, fill_opacity=0.08).move_to([x0 - 0.65, -0.60, 0])
    sender_lbl = T("sender", size=24, color=TEXT).move_to(sender.get_center())

    tissue_bg = Rectangle(width=10.0, height=1.50, stroke_color=GREY, stroke_width=1.6,
                          fill_color=TEAL, fill_opacity=0.11).move_to([(x0 + x500) / 2, -0.60, 0])
    cells = VGroup()
    for i in range(18):
        cx = x0 + 0.22 + i * 0.54
        cy = -0.60 + (0.28 if i % 2 == 0 else -0.28)
        c = RoundedRectangle(corner_radius=0.10, width=0.28, height=0.40,
                             stroke_color=GREEN, stroke_width=2.4,
                             fill_color=GREEN, fill_opacity=0.30 if i < 2 else 0.16).move_to([cx, cy, 0])
        cells.add(c)

    y_ax = -1.68
    axis = Line([x0, y_ax, 0], [x500 + 0.25, y_ax, 0], color=GREY, stroke_width=3.0)
    ticks = VGroup()
    tick_lbls = VGroup()
    for um in [0, 100, 200, 300, 400, 500]:
        tx = um_to_x(um)
        ticks.add(Line([tx, y_ax, 0], [tx, y_ax - 0.12, 0], color=GREY, stroke_width=2.8))
        lab = T(f"{um}", size=24, color=GREY).next_to([tx, y_ax - 0.12, 0], DOWN, buff=0.12)
        tick_lbls.add(lab)
    axis_unit = T("distance (µm)", size=24, color=GREY).next_to(tick_lbls, DOWN, buff=0.14)

    water_lbl = T("water upper bound (D = 10⁻⁶ cm²/s)", size=24, color=TEAL).move_to([-3.25, 2.48, 0])

    # Tau bar row at y=2.48: readout at x=0.86, bar frame x=2.0..5.6
    tau_tr = ValueTracker(tau_seconds)
    bar_x0, bar_y, bar_w = 2.0, 2.48, 3.6
    bar_frame = RoundedRectangle(corner_radius=0.06, width=bar_w, height=0.34,
                                 stroke_color=GOLD, stroke_width=2.0, fill_color=BG, fill_opacity=0.85)
    bar_frame.move_to([bar_x0 + bar_w / 2, bar_y, 0])
    tau_fill = always_redraw(lambda: Rectangle(
        width=max(0.14, bar_w * (tau_tr.get_value() / 100.0)),
        height=0.26, fill_color=GOLD, fill_opacity=0.9, stroke_width=0
    ).move_to([bar_x0 + max(0.14, bar_w * (tau_tr.get_value() / 100.0)) / 2, bar_y, 0]))
    tau_readout = always_redraw(lambda: M(
        f"τ = {tau_tr.get_value():.0f} s", size=24, color=GOLD
    ).move_to([0.86, bar_y, 0]))

    # Drifting YELLOW dots with decay tail proportional to cloud_um (larger dots so motion is visible)
    dots = VGroup()
    for _ in range(20):
        u = min(2.5 * cloud_um, rng.exponential(cloud_um))
        d = Dot(radius=0.075, color=YELLOW).move_to([
            x0 + 0.02 * u, rng.uniform(-1.22, 0.02), 0
        ])
        d._reach_um = cloud_um
        d._u = u
        dots.add(d)

    def u_dots(mob, dt):
        for d in mob:
            d._u += rng.normal(6.0 * dt, 14.0 * np.sqrt(dt))
            if d._u < 0 or d._u > 2.4 * d._reach_um:
                d._u = rng.uniform(0.5, 4.0)
            p = d.get_center()
            ny = np.clip(p[1] + rng.normal(0.0, 0.45 * np.sqrt(dt)), -1.24, 0.04)
            d.set_opacity(np.clip(np.exp(-d._u / (1.5 * max(d._reach_um, 1.0))), 0.15, 1.0))
            d.move_to([x0 + 0.02 * d._u, ny, 0])

    dots.add_updater(u_dots)

    # Initial 20 um bracket at y=0.42, label cleanly to the RIGHT of t1
    b20_line = Line([x0, 0.42, 0], [um_to_x(20), 0.42, 0], color=GOLD, stroke_width=3.5)
    b20_t0 = Line([x0, 0.30, 0], [x0, 0.54, 0], color=GOLD, stroke_width=3.5)
    b20_t1 = Line([um_to_x(20), 0.30, 0], [um_to_x(20), 0.54, 0], color=GOLD, stroke_width=3.5)
    b20_lbl = T("τ = 4 s → 20 µm", size=24, color=GOLD).next_to(b20_t1, RIGHT, buff=0.18)
    b20 = VGroup(b20_line, b20_t0, b20_t1, b20_lbl)

    grp = VGroup(sender, sender_lbl, tissue_bg, cells, axis, ticks, tick_lbls, axis_unit,
                 water_lbl, bar_frame, tau_fill, tau_readout, dots, b20)
    grp.um_to_x = um_to_x
    grp.x0 = x0
    grp.cells = cells
    grp.tick_lbls = tick_lbls
    grp.tau_tr = tau_tr
    grp.bar_frame = bar_frame
    grp.tau_fill = tau_fill
    grp.tau_readout = tau_readout
    grp.dots = dots
    grp.b20 = b20
    grp.water_lbl = water_lbl

    if show_arrows:
        arr_500 = DashedLine([x0, 1.62, 0], [um_to_x(500), 1.62, 0], color=TEXT, stroke_width=3.5, dash_length=0.18)
        tip_500 = Triangle(fill_color=TEXT, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-PI / 2).move_to([um_to_x(500), 1.62, 0])
        lbl_500 = T("500 µm?", size=26, color=TEXT).next_to([um_to_x(455), 1.62, 0], UP, buff=0.12)

        arr_less = DashedLine([x0, 1.05, 0], [um_to_x(135), 1.05, 0], color=GOLD, stroke_width=3.5, dash_length=0.16)
        tip_less = Triangle(fill_color=GOLD, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-PI / 2).move_to([um_to_x(135), 1.05, 0])
        lbl_less = T("much less?", size=26, color=GOLD).next_to(tip_less, RIGHT, buff=0.15)
        grp.arr_500 = VGroup(arr_500, tip_500, lbl_500)
        grp.arr_less = VGroup(arr_less, tip_less, lbl_less)
        grp.add(grp.arr_500, grp.arr_less)

    return grp


class S05PredictQuestion(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(5)
        w = _build_predict_world(rng, tau_seconds=4.0, show_arrows=False, cloud_um=20.0)
        tag = scope_tag("in this model")
        reach_init = ValueTracker(2.0)
        for d in w.dots:
            d._reach_um = 2.0
        # Live 4 s turnover clock with filled sweep sector + computed exp(-x/20) curve inside tissue_bg
        clk_tr = ValueTracker(0.0)
        clk_center = np.array([-4.05, 1.45, 0.0])
        clk = _make_clock(clk_tr, center=clk_center, radius=0.52, color=GOLD)
        clk_wedge = always_redraw(lambda: Sector(
            radius=0.46, start_angle=PI / 2,
            angle=-max(0.02, (clk_tr.get_value() % 1.0)) * TAU,
            arc_center=clk_center,
            fill_color=GOLD, fill_opacity=0.45, stroke_width=0
        ) if (clk_tr.get_value() % 1.0) > 0.01 else VMobject())

        prof_prog = ValueTracker(0.05)
        def mk_prof():
            xmax = 120.0 * prof_prog.get_value()
            xs = np.linspace(0.0, xmax, 40)
            pts = [[w.um_to_x(x), -1.35 + 1.45 * np.exp(-x / 20.0), 0] for x in xs]
            m = VMobject(stroke_color=GOLD, stroke_width=3.5, fill_opacity=0)
            m.set_points_as_corners(pts)
            return m
        prof_curve = always_redraw(mk_prof)

        w.remove(w.b20)
        self.add(w, prof_curve, clk, clk_wedge, tag)

        def sync_init(m, dt):
            r = reach_init.get_value()
            for d in m:
                d._reach_um = r

        w.dots.add_updater(sync_init)
        self.play(
            reach_init.animate.set_value(20.0),
            prof_prog.animate.set_value(1.0),
            clk_tr.animate.set_value(0.99),
            run_time=4.0,
            rate_func=linear,
        )
        w.dots.remove_updater(sync_init)

        # Beat 1: four seconds -> 20 um -> one or two cells
        self.at("four seconds")
        self.play(
            FadeIn(w.b20, shift=UP * 0.06),
            clk_tr.animate.set_value(1.30),
            run_time=1.0,
            rate_func=linear,
        )
        self.play(
            clk_tr.animate.set_value(1.99),
            run_time=2.0,
            rate_func=linear,
        )

        self.at("one or two cells")
        self.play(
            Indicate(w.cells[:2], color=GREEN, scale_factor=1.18),
            clk_tr.animate.set_value(2.65),
            run_time=1.4,
            rate_func=linear,
        )
        self.play(
            clk_tr.animate.set_value(2.99),
            run_time=0.8,
            rate_func=linear,
        )

        # Beat 2: slow clearance 25 times, to 100 seconds
        self.at("slow clearance 25 times")
        self.play(
            FadeOut(clk), FadeOut(clk_wedge), FadeOut(prof_curve),
            w.tau_tr.animate.set_value(100.0),
            run_time=2.3,
            rate_func=smooth,
        )

        # Beat 3: Does it reach 25 times farther, or much less?
        self.at("Does it reach")
        x0, um_to_x = w.x0, w.um_to_x
        arr_500 = DashedLine([x0, 1.62, 0], [um_to_x(500), 1.62, 0], color=TEXT, stroke_width=3.5, dash_length=0.18)
        tip_500 = Triangle(fill_color=TEXT, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-PI / 2).move_to([um_to_x(500), 1.62, 0])
        lbl_500 = T("500 µm?", size=26, color=TEXT).next_to([um_to_x(455), 1.62, 0], UP, buff=0.12)

        arr_less = DashedLine([x0, 1.05, 0], [um_to_x(135), 1.05, 0], color=GOLD, stroke_width=3.5, dash_length=0.16)
        tip_less = Triangle(fill_color=GOLD, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-PI / 2).move_to([um_to_x(135), 1.05, 0])
        lbl_less = T("much less?", size=26, color=GOLD).next_to(tip_less, RIGHT, buff=0.15)

        q = question_card("25× lifetime: 25× reach, or less?", y=HEAD_Y, max_w=11.5)
        self.play(
            FadeIn(q),
            Create(arr_500), FadeIn(tip_500), FadeIn(lbl_500),
            Create(arr_less), FadeIn(tip_less), FadeIn(lbl_less),
            run_time=1.3,
        )
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "25× lifetime: 25× reach, or less?"
    CARD = {"y": HEAD_Y, "max_w": 11.5}
    RING_AT = (3.85, -2.95, 0)
    SECONDS = 4.5

    def backdrop(self):
        rng = np.random.default_rng(6)
        w = _build_predict_world(rng, tau_seconds=100.0, show_arrows=True, cloud_um=20.0)
        pulse(w.bar_frame, base=2.4, amp=1.4, speed=3.5)
        return VGroup(w, scope_tag("in this model"))


class S07Reveal(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        w = _build_predict_world(rng, tau_seconds=100.0, show_arrows=True, cloud_um=20.0)
        q = question_card("25× lifetime: 25× reach, or less?", y=HEAD_Y, max_w=11.5)
        tag = scope_tag("in this model")
        self.add(w, q, tag)

        # Beat 1: Much less -> cross out 500 um? in RED and light computed 100 um mark on axis
        strike = Line(w.arr_500[2].get_corner(DL) + LEFT * 0.1,
                      w.arr_500[2].get_corner(UR) + RIGHT * 0.1,
                      color=RED, stroke_width=5)
        strike.layout_ok = True
        mark_100 = Dot([w.um_to_x(100), -1.68, 0], radius=0.11, color=GOLD)
        guide_100 = DashedLine([w.um_to_x(100), -1.68, 0], [w.um_to_x(100), 0.15, 0], color=GOLD, stroke_width=2.5)
        self.play(
            Create(strike), FadeIn(mark_100), Create(guide_100),
            w.tick_lbls[1].animate.set_color(GOLD),
            run_time=0.8,
        )

        # Beat 2: square root of lifetime -> inset computed Plot r(tau) = 10*sqrt(tau) above tissue (y: 1.35..3.05)
        self.at("square root of lifetime")
        self.play(
            FadeOut(w.arr_500), FadeOut(strike), FadeOut(w.arr_less),
            FadeOut(w.bar_frame), FadeOut(w.tau_fill), FadeOut(w.tau_readout),
            FadeOut(q), FadeOut(w.water_lbl),
            run_time=0.5,
        )
        inset = Plot(box=(0.8, 5.6, 1.35, 3.05), xr=(0, 110), yr=(0, 120),
                     xticks=[0, 4, 25, 100], yticks=[0, 20, 100],
                     xlabel="lifetime τ (s)", ylabel="reach (µm)",
                     color=GREY, size=22, label_size=24)
        tau_plot_tr = ValueTracker(0.0)
        reach_fn = lambda t: 10.0 * np.sqrt(max(t, 0.0))
        live_rc = inset.live_curve(reach_fn, tau_plot_tr, color=GOLD, width=5)
        pt_4 = Dot(inset.pt(4, 20), radius=0.08, color=YELLOW, stroke_color=GOLD, stroke_width=2.5)
        pt_100 = Dot(inset.pt(100, 100), radius=0.09, color=YELLOW, stroke_color=GOLD, stroke_width=2.5)
        rule_lbl = T("reach = √(D × τ)", size=28, color=GOLD).move_to([-3.2, 2.85, 0])
        self.play(Create(inset), FadeIn(rule_lbl), run_time=0.7)
        self.add(live_rc)
        self.play(tau_plot_tr.animate.set_value(100.0), run_time=2.2, rate_func=linear)
        self.play(FadeIn(pt_4), FadeIn(pt_100), run_time=0.4)

        # Beat 3: reach grows only 5 times, from 20 to about 100 um (5 to 10 cells)
        self.at("reach grows only")
        reach_um = ValueTracker(20.0)
        b_reach, _, _ = _make_reach_bracket(
            w.x0, lambda: 0.02 * reach_um.get_value(), 0.42,
            lambda: f"5× reach ({reach_um.get_value():.0f} µm)" if reach_um.get_value() >= 99.5 else f"{reach_um.get_value():.0f} µm",
            color=GOLD, size=26, label_right=False
        )
        self.play(FadeOut(w.b20), run_time=0.25)
        self.add(b_reach)

        def set_reach(m, dt):
            cur = reach_um.get_value()
            for d in w.dots:
                d._reach_um = cur

        w.dots.add_updater(set_reach)
        self.play(
            reach_um.animate.set_value(100.0),
            *[c.animate.set_fill(GREEN, opacity=0.35) for c in w.cells[:5]],
            run_time=2.6,
            rate_func=smooth,
        )

        # Beat 4: Meanwhile decay slows 25 times
        self.at("Meanwhile decay slows")
        clock_tr = ValueTracker(0.0)
        clock = _make_clock(clock_tr, center=(-4.2, 1.95, 0), radius=0.52, color=GOLD)
        lbl_slow = T("25× slower decay", size=26, color=GOLD).next_to(clock, RIGHT, buff=0.25)
        self.play(FadeIn(clock), FadeIn(lbl_slow), run_time=0.35)
        self.play(
            clock_tr.animate.set_value(4.5),
            w.dots.animate.set_opacity(0.45),
            run_time=2.4,
            rate_func=linear,
        )
        self.finish()


# ==============================================================================
# SCENE 08: Sticky Tissue (28.025 s spoken)
# ==============================================================================
class S08StickyTissue(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(8)

        x0, x100 = -4.6, 5.4
        um_to_x = lambda um: x0 + 0.10 * um

        sender = RoundedRectangle(corner_radius=0.25, width=1.25, height=2.2,
                                  stroke_color=TEXT, stroke_width=3.0,
                                  fill_color=TEXT, fill_opacity=0.08).move_to([x0 - 0.68, -0.35, 0])
        sender_lbl = T("sender", size=24, color=TEXT).move_to(sender.get_center())
        tissue_bg = Rectangle(width=10.0, height=2.2, stroke_color=GREY, stroke_width=1.6,
                              fill_color=TEAL, fill_opacity=0.11).move_to([(x0 + x100) / 2, -0.35, 0])
        cells = VGroup(*[
            _make_cell([x, -0.35 + (0.55 if i % 2 == 0 else -0.55), 0], w=1.05, h=0.72,
                       color=GREEN, fill_op=0.22, cups=[([-0.55, 0.0, 0], PI * 0.5)])
            for i, x in enumerate([-3.0, -1.1, 0.8, 2.7, 4.4])
        ])

        y_ax = -1.85
        axis = Line([x0, y_ax, 0], [x100 + 0.25, y_ax, 0], color=GREY, stroke_width=3.0)
        ticks = VGroup()
        tick_lbls = VGroup()
        for um in [0, 20, 40, 60, 80, 100]:
            tx = um_to_x(um)
            ticks.add(Line([tx, y_ax, 0], [tx, y_ax - 0.12, 0], color=GREY, stroke_width=2.8))
            tick_lbls.add(T(f"{um}", size=24, color=GREY).next_to([tx, y_ax - 0.12, 0], DOWN, buff=0.12))
        ax_unit = T("distance (µm)", size=24, color=GREY).next_to(tick_lbls, DOWN, buff=0.14)

        tau_tr = ValueTracker(100.0)
        tau_bar = _make_tau_bar(tau_tr, max_tau=140.0, pos=(4.3, 3.22, 0), width=2.6, label_text="τ = 100 s")
        tag = scope_tag("in this model")

        reach_um = ValueTracker(100.0)
        b_reach, _, _ = _make_reach_bracket(
            x0, lambda: 0.10 * reach_um.get_value(), 1.15,
            lambda: (
                "100 µm (water)" if reach_um.get_value() >= 99.5
                else ("about 3 µm (sticky tissue)" if reach_um.get_value() <= 3.5
                      else f"{reach_um.get_value():.0f} µm")
            ),
            color=GOLD, size=26
        )

        fibers = VGroup()
        for fy in [-1.1, -0.35, 0.45]:
            pts = [[x0 + k * 0.9, fy + 0.22 * np.sin(k * 1.4 + fy), 0] for k in range(12)]
            curve = VMobject(stroke_color=PURPLE, stroke_width=2.8, stroke_opacity=0.8)
            curve.set_points_smoothly(pts)
            fibers.add(curve)

        dots = VGroup()
        for _ in range(22):
            d = Dot(radius=0.075, color=YELLOW).move_to([
                x0 + rng.uniform(0.1, 8.5), rng.uniform(-1.25, 0.55), 0
            ])
            d._stuck = 0.0
            dots.add(d)

        sticky_mode = {"on": False}

        def u_dots(mob, dt):
            max_um = reach_um.get_value()
            max_x = x0 + 0.10 * max(max_um * 1.8, 10.0)
            for d in mob:
                if sticky_mode["on"]:
                    if d._stuck > 0:
                        d._stuck -= dt
                        continue
                    p = d.get_center()
                    nx = p[0] + rng.normal(0.0, 0.35 * np.sqrt(dt))
                    ny = p[1] + rng.normal(0.0, 0.35 * np.sqrt(dt))
                    if rng.random() < 0.05:
                        d._stuck = rng.uniform(0.25, 0.65)
                    if nx > max_x:
                        nx = x0 + rng.uniform(0.08, 0.45)
                else:
                    p = d.get_center()
                    nx = p[0] + rng.normal(0.55 * dt, 0.95 * np.sqrt(dt))
                    ny = p[1] + rng.normal(0.0, 0.65 * np.sqrt(dt))
                    if nx > x100:
                        nx = x0 + 0.1
                nx = np.clip(nx, x0 + 0.05, x100)
                ny = np.clip(ny, -1.3, 0.6)
                d.move_to([nx, ny, 0])

        dots.add_updater(u_dots)
        self.add(sender, sender_lbl, tissue_bg, cells, axis, ticks, tick_lbls, ax_unit,
                 tau_bar, b_reach, dots, tag)

        # Beat 1: Matrix fibers and receptors bind a drifting protein
        self.at("Matrix fibers")
        sticky_mode["on"] = True
        lbl_bind = T("matrix fibers bind", size=26, color=PURPLE).move_to([-2.4, 2.55, 0])
        self.play(Create(fibers), FadeIn(lbl_bind, shift=UP * 0.08), run_time=2.5)

        # Beat 2: lower diffusion shrinks reach 30-fold (D = 10^-9 -> ~3 um)
        self.at("lower diffusion")
        self.play(reach_um.animate.set_value(3.2), run_time=3.2)

        # Beat 3: square root of a thousand is about 32
        self.at("square root")
        lbl_ratio = T("1000× lower D → ÷32 reach", size=26, color=GOLD).move_to([2.4, 2.15, 0])
        self.play(FadeIn(lbl_ratio, shift=UP * 0.08), run_time=0.8)

        # Beat 4: Binding can also protect the molecule and lengthen its life
        self.at("Binding can also protect")
        bound_pos = np.array([-3.6, -0.62, 0])
        bound_dot = Dot(bound_pos, radius=0.10, color=YELLOW)
        shield = Circle(radius=0.28, color=PURPLE, stroke_width=3.5).move_to(bound_pos)
        shield_lbl = T("binding may protect", size=26, color=PURPLE).move_to([-2.2, 1.95, 0])
        probing_enz = _make_enzyme(bound_pos + RIGHT * 1.15, scale=0.85, color=CORAL)
        new_tau_lab = T("τ > 100 s", size=24, color=GOLD).next_to(tau_bar.bg, LEFT, buff=0.22)
        self.play(
            FadeOut(lbl_bind),
            FadeIn(bound_dot), Create(shield), FadeIn(shield_lbl), FadeIn(probing_enz),
            swap(tau_bar.lab, new_tau_lab, run_time=0.6),
            tau_tr.animate.set_value(130.0),
            run_time=1.0,
        )
        # Show enzyme approaching shield and deflecting away
        self.play(probing_enz.animate.move_to(bound_pos + RIGHT * 0.42), run_time=0.7)
        self.play(probing_enz.animate.move_to(bound_pos + RIGHT * 1.15 + DOWN * 0.35), run_time=0.7)

        # Beat 5: Either way, a signal-to-neighbors stays local
        self.at("Either way")
        lbl_local = T("stays local", size=28, color=GOLD).move_to([2.4, 1.1, 0])
        self.play(
            FadeIn(lbl_local, shift=UP * 0.08),
            probing_enz.animate.move_to(bound_pos + RIGHT * 0.48 + UP * 0.20),
            run_time=1.0,
        )
        self.play(probing_enz.animate.move_to(bound_pos + RIGHT * 1.35 + UP * 0.15), run_time=1.0)
        self.finish()


# ==============================================================================
# SCENE 09: Synapse Extreme (25.625 s spoken)
# ==============================================================================
class S09SynapseExtreme(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(9)

        sender = RoundedRectangle(corner_radius=0.4, width=3.8, height=4.4,
                                  stroke_color=TEXT, stroke_width=3.2,
                                  fill_color=TEXT, fill_opacity=0.07).move_to([-3.8, 0.1, 0])
        sender_lbl = T("sender", size=28, color=TEXT).move_to([-4.2, 1.85, 0])

        receiver = RoundedRectangle(corner_radius=0.4, width=3.8, height=4.4,
                                    stroke_color=GREEN, stroke_width=3.4,
                                    fill_color=GREEN, fill_opacity=0.12).move_to([3.8, 0.1, 0])
        receiver_lbl = T("receiver", size=28, color=GREEN).move_to([4.2, 1.85, 0])
        cups = VGroup(
            _make_cup([1.85, 0.85, 0], angle=PI * 0.5, scale=1.1, color=GREEN),
            _make_cup([1.85, 0.0, 0], angle=PI * 0.5, scale=1.1, color=GREEN),
            _make_cup([1.85, -0.85, 0], angle=PI * 0.5, scale=1.1, color=GREEN),
        )

        # Raised imp_plot box so xlabel 'receiver response' sits comfortably inside receiver
        imp_plot = Plot(box=(2.35, 5.25, -1.25, 0.75), xr=(0, 3.0), yr=(0, 1.2),
                        xticks=[], yticks=[], xlabel="receiver response", color=GREEN, size=22, label_size=24)
        imp_t = ValueTracker(0.0)

        def imp_fn(t):
            v = 0.05
            for t0 in (0.45, 1.45, 2.35):
                if t >= t0:
                    v += 0.95 * np.exp(-((t - t0) / 0.16) ** 2)
            return min(1.05, v)

        imp_curve = imp_plot.live_curve(imp_fn, imp_t, color=GREEN, width=4.5)
        tag = scope_tag("schematic")

        enzymes = VGroup(
            _make_enzyme([0.0, 0.85, 0], scale=1.15, color=CORAL),
            _make_enzyme([0.1, -0.65, 0], scale=1.15, color=CORAL),
        )
        badge_ms = boxed_label("about 1 ms", color=GOLD, size=26).move_to([0.0, 2.90, 0])
        lbl_enz = T("acetylcholinesterase", size=26, color=CORAL).move_to([0.0, -2.55, 0])

        self.add(sender, sender_lbl, receiver, receiver_lbl, cups, imp_plot, imp_curve, tag)

        def fire_burst(t_start, t_end, dur_cross=0.65, dur_clear=0.60):
            burst = VGroup(*[
                Dot(radius=0.085, color=YELLOW).move_to([-1.75, rng.uniform(-0.9, 0.9), 0])
                for _ in range(12)
            ])
            self.add(burst)
            self.play(
                *[d.animate.move_to([1.65, d.get_center()[1], 0]) for d in burst],
                imp_t.animate.set_value((t_start + t_end) / 2),
                receiver.animate.set_fill(GREEN, opacity=0.38),
                run_time=dur_cross,
            )
            self.play(
                *[d.animate.scale(0.35).set_opacity(0.0) for d in burst],
                imp_t.animate.set_value(t_end),
                receiver.animate.set_fill(GREEN, opacity=0.12),
                run_time=dur_clear,
            )
            self.remove(burst)

        # Beat 1: enzyme acetylcholinesterase destroys acetylcholine in ~1 ms
        self.at("an enzyme")
        self.play(FadeIn(enzymes), FadeIn(lbl_enz), run_time=0.6)
        fire_burst(0.0, 1.0, dur_cross=0.75, dur_clear=0.70)

        # Continuous cleft-cleaving demonstration while explaining ~1 ms and ~1 um scale (no freeze!)
        cleft_dots = VGroup(*[
            Dot(radius=0.10, color=YELLOW).move_to([-1.75 + i * 0.22, rng.uniform(-0.95, 0.95), 0])
            for i in range(16)
        ])
        for d in cleft_dots:
            d._vx = rng.uniform(1.0, 1.6)
            d._fade = 1.0

        def u_cleft(mob, dt):
            for d in mob:
                p = d.get_center()
                nx = p[0] + d._vx * dt
                if nx > -0.1:
                    d._fade = max(0.0, d._fade - 2.4 * dt)
                if d._fade <= 0.05 or nx > 1.3:
                    nx = -1.78
                    ny = rng.uniform(-0.95, 0.95)
                    d._fade = 1.0
                else:
                    ny = p[1]
                d.set_opacity(d._fade)
                d.move_to([nx, ny, 0])

        cleft_dots.add_updater(u_cleft)
        self.add(cleft_dots)

        # Gently rock enzymes as they cleave acetylcholine across 1 ms
        enzymes._t = 0.0
        def u_enz(mob, dt):
            mob._t += dt
            ang = 0.20 * np.sin(8.0 * mob._t)
            mob[0].rotate(ang * dt * 8.0)
            mob[1].rotate(-ang * dt * 8.0)
        enzymes.add_updater(u_enz)

        self.at("within about")
        self.play(FadeIn(badge_ms, shift=DOWN * 0.06), run_time=0.6)

        # Beat 2: rough scale near 1 um
        self.at("rough scale")
        halo = DashedVMobject(
            RoundedRectangle(corner_radius=0.6, width=3.3, height=2.9, stroke_color=GOLD, stroke_width=2.8),
            num_dashes=28
        ).move_to([0.0, 0.05, 0])
        lbl_um = T("≈ 1 µm rough scale", size=24, color=GOLD).next_to(halo, UP, buff=0.14)
        self.play(Create(halo), FadeIn(lbl_um, shift=UP * 0.06), run_time=0.9)

        # Beat 3: Wiping the gap clean keeps rapid impulses distinct (bursts 2 and 3)
        self.at("Wiping the gap")
        self.remove(cleft_dots)
        enzymes.remove_updater(u_enz)
        lbl_distinct = T("rapid impulses distinct", size=24, color=GREEN).move_to([3.8, -2.55, 0])
        self.play(FadeIn(lbl_distinct), run_time=0.35)
        fire_burst(1.0, 2.0)
        fire_burst(2.0, 3.0)

        # Beat 4: Other synapses clear serotonin by pumping it back
        self.at("Other synapses")
        transporter = _make_transporter([-1.9, 0.0, 0], vertical=True, color=BLUE, scale=1.3)
        pump_arr = Arrow([0.8, 0.0, 0], [-2.5, 0.0, 0], color=BLUE, stroke_width=5, buff=0.05)
        lbl_sero = T("serotonin reuptake", size=26, color=BLUE).move_to([0.0, -2.55, 0])
        ser_dots = VGroup(*[
            Dot(radius=0.085, color=YELLOW).move_to([rng.uniform(-0.4, 1.3), rng.uniform(-0.6, 0.6), 0])
            for _ in range(10)
        ])
        self.play(
            FadeOut(enzymes), FadeOut(halo), FadeOut(lbl_um), FadeOut(badge_ms), FadeOut(lbl_distinct),
            swap(lbl_enz, lbl_sero, run_time=0.5),
            FadeIn(transporter), GrowArrow(pump_arr), FadeIn(ser_dots),
            run_time=0.8,
        )
        self.play(
            *[d.animate.move_to([-2.9, rng.uniform(-0.5, 0.5), 0]).set_opacity(0.25) for d in ser_dots],
            run_time=2.2,
        )
        self.finish()


# ==============================================================================
# SCENE 10: Blood Changes the Bargain (15.775 s spoken)
# ==============================================================================
class S10BloodChangesBargain(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(10)

        vessel = _make_vessel(y_center=-2.25, height=0.84, x0=-6.3, x1=6.3)
        gland = RoundedRectangle(corner_radius=0.24, width=1.35, height=0.95,
                                 stroke_color=TEXT, stroke_width=3.0,
                                 fill_color=TEXT, fill_opacity=0.08).move_to([-5.3, -1.18, 0])
        gland_lbl = T("gland", size=24, color=TEXT).move_to(gland.get_center())
        targets = VGroup(*[
            _make_cell([x, -1.32, 0], w=1.0, h=0.68, color=GREEN, fill_op=0.35,
                       cups=[([0.0, -0.43, 0], PI)])
            for x in [-1.0, 2.0, 5.0]
        ])
        lbl_flow = T("flow sets range", size=26, color=TEAL).move_to([-3.1, -1.25, 0])

        # Upper Plot: raised bottom to 0.65 so xlabel sits cleanly above targets & lbl_flow
        P = Plot(box=(-3.0, 5.4, 0.65, 2.85), xr=(0, 10), yr=(0, 108),
                 xticks=[0, 2.5, 5, 7.5, 10], yticks=[(0, "0%"), (50, "50%"), (100, "100%")],
                 xlabel="minutes after secretion stops", ylabel="epinephrine",
                 color=GREY, size=24, label_size=24)
        epi_ylabel = P.ylabel
        P.remove(epi_ylabel)
        t_tr = ValueTracker(0.0)
        epi_fn = lambda t: 100.0 * (2.0 ** (-t / 2.5))
        live_curve = P.live_curve(epi_fn, t_tr, color=GOLD, width=5)
        dot_curve = P.dot(lambda: t_tr.get_value(), lambda: epi_fn(t_tr.get_value()),
                          color=YELLOW, ring=GOLD, radius=0.07)

        vessel_dots = VGroup(*[
            Dot(radius=0.08, color=YELLOW).move_to([rng.uniform(-6.0, 6.0), rng.uniform(-2.52, -1.98), 0])
            for _ in range(20)
        ])
        _attach_vessel_flow(vessel, vessel_dots, rng, speed=3.4)

        def u_thin(mob, dt):
            frac = 2.0 ** (-t_tr.get_value() / 2.5)
            n_keep = max(1, int(round(20 * frac)))
            for idx, d in enumerate(mob):
                d.set_opacity(1.0 if idx < n_keep else 0.06)

        vessel_dots.add_updater(u_thin)
        tag = scope_tag("in this model")

        self.add(vessel, vessel_dots, gland, gland_lbl, targets, lbl_flow, tag)

        # Beat 1: once secretion stops
        self.at("once secretion stops")
        stop_gate = Line([-5.95, -1.78, 0], [-4.65, -1.78, 0], color=RED, stroke_width=5.5)
        lbl_stop = T("secretion stops", size=24, color=RED).move_to([-5.1, -0.32, 0])
        self.play(Create(stop_gate), FadeIn(lbl_stop), FadeIn(P), run_time=0.55)
        self.add(live_curve, dot_curve)

        # Beat 2: Epinephrine falls by half in roughly 2-3 minutes
        self.at("Epinephrine falls")
        lbl_epi = T("epinephrine: half in 2–3 min", size=26, color=GOLD).move_to([2.6, 2.55, 0])
        half_ref = DashedLine(P.pt(0, 50), P.pt(2.5, 50), color=GOLD, stroke_width=2.5)
        half_drop = DashedLine(P.pt(2.5, 50), P.pt(2.5, 0), color=GOLD, stroke_width=2.5)
        self.play(FadeIn(epi_ylabel), FadeIn(lbl_epi), run_time=0.4)
        self.play(
            t_tr.animate.set_value(2.5),
            *[c.body.animate.set_fill(GREEN, opacity=0.22) for c in targets],
            run_time=1.4,
            rate_func=linear,
        )
        self.play(Create(half_ref), Create(half_drop), run_time=0.4)
        self.play(
            t_tr.animate.set_value(10.0),
            *[c.body.animate.set_fill(GREEN, opacity=0.10) for c in targets],
            run_time=3.0,
            rate_func=linear,
        )
        self.finish()


# ==============================================================================
# SCENE 11: Handoff (15.825 s spoken)
# ==============================================================================
class S11Handoff(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(11)
        world = _make_full_world(rng)
        _attach_world_motion(world, rng)
        tag = scope_tag("schematic")
        self.add(world, tag)

        # Beat 1: Fast removal keeps local signals brief and contained
        self.at("Fast removal")
        syn_box = SurroundingRectangle(
            VGroup(world.syn_sender, world.syn_receiver),
            color=CORAL, stroke_width=3.0, buff=0.16, corner_radius=0.25
        )
        lbl_fast = T("fast removal: brief & local", size=26, color=CORAL).next_to(syn_box, UP, buff=0.14)
        self.play(Create(syn_box), FadeIn(lbl_fast, shift=UP * 0.08), run_time=0.6)

        # Beat 2: while lingering buys range only by slowing recovery
        self.at("while lingering")
        para_box = SurroundingRectangle(
            VGroup(world.para_sender, world.tissue_cells),
            color=GOLD, stroke_width=3.0, buff=0.16, corner_radius=0.25
        )
        lbl_ling = T("lingering: wider, slower recovery", size=26, color=GOLD).next_to(para_box, UP, buff=0.14)
        self.play(Create(para_box), FadeIn(lbl_ling, shift=UP * 0.08), run_time=0.6)

        # Beat 3: What happens when a drug blocks the enzyme or transporter?
        self.at("What happens when")
        self.play(FadeOut(syn_box), FadeOut(lbl_fast), FadeOut(para_box), FadeOut(lbl_ling), run_time=0.4)

        enz_ring = Circle(radius=0.35, color=CORAL, stroke_width=4).move_to(world.syn_enzyme.get_center())
        tr_ring = Circle(radius=0.35, color=BLUE, stroke_width=4).move_to(world.syn_transporter.get_center())
        # Keep drug ? badges cleanly outside syn_sender/syn_receiver outlines (tops 2.60, bottom 0.90)
        q_enz = boxed_label("drug ?", color=RED, size=26, pad=0.16).move_to([-3.35, 3.25, 0])
        q_tr = boxed_label("drug ?", color=RED, size=26, pad=0.16).move_to([-5.2, -0.20, 0])

        self.play(Create(enz_ring), Create(tr_ring), FadeIn(q_enz), FadeIn(q_tr), run_time=0.5)
        self.play(
            q_enz.animate.move_to([-3.35, 2.95, 0]),
            q_tr.animate.move_to([-4.6, 0.35, 0]),
            run_time=2.0,
        )
        self.finish()


# ==============================================================================
# SCENE 12: End Card (3.5 s silent)
# ==============================================================================
class S12End(EndCard):
    LINE = "Clearance ends signals and sets lifetime,\ntrading local reach against tempo."
