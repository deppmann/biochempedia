"""
Two Fixes for the Lock — Basic Concepts of Enzyme Action (Chapter 2)

COLOUR MAP (one colour per concept for the entire film):
- TEAL   (#3FB8C0): Enzyme active site (cup, hinged cleft, catalytic knobs) & lowered energy pass
- GOLD   (#D4A843): Enzyme's grip (contact ticks, catalytic alignment line, title rule)
- YELLOW (#F5D547): Substrate (key-dot, near-twin, glucose, HMG-CoA, valley particles)
- GREEN  (#83C167): Product valley marker (right-side valley endpoint)
- RED    (#FC6255): High uncatalyzed pass, ruled-out contacts (cross), blood band
- PURPLE (#B884F2): Transition state (stretched oval, peak on pass, Fix 1: fit)
- ORANGE (#F2994A): Fischer's rigid lock picture
- BLUE   (#669DF6): Phosphate group (phosphate from ATP)
- CYAN   (#8CF0FF): Water molecules
- MAGENTA(#EB73C8): Drugs & competitive inhibitors (transition-state-shaped drug, statin)
- TEXT   (#E8EAF0): Neutral labels, chips, liver cell outline, LDL dots

THE ONE CARRIED WORLD:
- Top strip (upper ~26% of the frame): the computed free-energy landscape
  G(x) = s(x) + H * exp(-(x / 1.1)**2) with s(x) = -1.3 - 0.7 * tanh(x / 1.6),
  showing the RED dashed high pass (H = 4.2) and the TEAL lowered pass (H = 1.8),
  with YELLOW particles thermally jiggling in the left valley and crossing over the
  TEAL barrier at a rate driven by a flux ValueTracker, plus a 'schematic' tag.
- Main stage (lower ~74% of the frame): the TEAL active site (cup / hinged cleft)
  interacting with substrate, transition state, rigid lock comparison, water/glucose,
  or statin inhibitor, carrying its state smoothly from scene to scene.

WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
- s00_link_and_hook:  8 GOLD contact ticks flash; cup slides left as ORANGE rigid lock & YELLOW key-dot seat; '?' pops into fix chips 1 & 2; strip particles cross G(x, 1.8) via rng(7).
- s02_fischer:        ORANGE lock grows at centre-right; round YELLOW sugar seats flush, bumped near-twin bounces off the rigid rim, round sugar re-seats; strip particles cross G(x, 1.8).
- s03_fix_fit:        Chip 1 turns PURPLE ('fit'); 8 GOLD ticks on rigid lock pulse then are crossed out in RED; TEAL cup gets loose YELLOW dot (2 ticks) then stretches to PURPLE oval (8 ticks); strip runs.
- s04_fix_shape:      Chip 2 turns TEAL ('shape'); 3 YELLOW dots tap rigid lock (zero deflection) before it exits; TEAL cup zooms to wide-open hinged cleft with knobs, BLUE phosphate chip, YELLOW glucose.
- s05_predict:        15 CYAN water dots (rng(11)) diffuse around open cleft; 'OH' marks glucose & water; one water enters with ghost arrow from phosphate, arrow vanishes; question card slides up.
- s07_answer:         Water exits cleft; glucose drops in and hinged lips close (`open` tracker 1->0), aligning knobs-glucose-phosphate on GOLD line; water-only inset stays open; 'induced fit' lands.
- s08_selection:      Empty cleft cycles open<->closed (~1.5 s period); YELLOW substrate captures a closed state and locks it; 'induced fit' & 'selection' arrows converge.
- s09_idea:           Cup resets closed on PURPLE oval; two questions ('fits best?', 'changes shape?') split by divider convert to PURPLE 'transition state' (oval glows) and TEAL 'many enzymes: yes' (cup flexes).
- s10_drug_logic:     MAGENTA drug enters cup, closes with 8 GOLD ticks, blocks incoming YELLOW substrate, and throttles top-strip flux tracker (1->0); blob morphs into PURPLE-oval silhouette.
- s11_statin:         YELLOW substrate dots stream through open HMG-CoA reductase cup onto HMG-CoA -> cholesterol pathway; two-part MAGENTA statin ('HMG-like part' + tail) seats in pocket.
- s12_statin_result:  Extra GOLD ticks light along MAGENTA tail; incoming YELLOW HMG-CoA bounces off; pathway flux slows (1->0.18); WHITE-ringed LDL dots flow faster from RED blood into liver cell.
- s13_return:         Cup closed on PURPLE oval connects via vertical PURPLE line to glowing peak of TEAL G(x, 1.8) pass; cup flexes once; faint ORANGE rigid lock ghosts still then fades; strip streams.
"""
from bp_parts import *

# Extended palette for this film (all high contrast against BG = #0f1117)
PURPLE = "#B884F2"
ORANGE = "#F2994A"
CYAN = "#8CF0FF"
MAGENTA = "#EB73C8"
BLUE = "#669DF6"  # distinct cobalt blue for phosphate (separate from TEAL #3FB8C0 & CYAN #8CF0FF)

# ------------------------------------------------------------------ computed energy landscape
def _s_curve(x):
    return -1.3 - 0.7 * np.tanh(x / 1.6)


def _G_curve(x, H):
    return _s_curve(x) + H * np.exp(-(x / 1.1) ** 2)


# Strip screen box: x in [-5.85, 5.85], y in [1.98, 3.55] (leaving y=1.55..1.95 clear on right for 'schematic')
STRIP_X0, STRIP_X1 = -5.85, 5.85
STRIP_Y0, STRIP_Y1 = 1.98, 3.55
DATA_X0, DATA_X1 = -3.3, 3.3
DATA_Y0, DATA_Y1 = -2.2, 3.1


def _strip_pt(x, y):
    fx = (x - DATA_X0) / (DATA_X1 - DATA_X0)
    fy = (y - DATA_Y0) / (DATA_Y1 - DATA_Y0)
    return np.array([
        STRIP_X0 + fx * (STRIP_X1 - STRIP_X0),
        STRIP_Y0 + fy * (STRIP_Y1 - STRIP_Y0),
        0.0,
    ])


def make_top_strip(flux=1.0, show_ts_peak=False, seed=7):
    """Build the carried top energy-landscape strip with animated valley & crossing particles."""
    xs = np.linspace(DATA_X0, DATA_X1, 140)
    high_pts = [_strip_pt(x, _G_curve(x, 4.2)) for x in xs]
    low_pts = [_strip_pt(x, _G_curve(x, 1.8)) for x in xs]

    high_raw = VMobject(stroke_color=RED, stroke_width=4.0, stroke_opacity=0.88)
    high_raw.set_points_as_corners(high_pts)
    high_curve = DashedVMobject(high_raw, num_dashes=34, dashed_ratio=0.55)

    low_curve = VMobject(stroke_color=TEAL, stroke_width=6.0, stroke_opacity=0.98)
    low_curve.set_points_as_corners(low_pts)

    divider = Line([-6.2, 1.50, 0], [6.2, 1.50, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.35)
    divider.layout_ok = True

    tag = T("schematic", size=28, color=TEXT).move_to([5.85, 1.72, 0], aligned_edge=RIGHT)

    flux_tr = ValueTracker(flux)
    rng = np.random.default_rng(seed)

    # Left-valley jiggling particles (around x_min = -2.29)
    n_valley = 12
    v_phases = rng.uniform(0, TAU, n_valley)
    v_freqs = rng.uniform(2.4, 4.2, n_valley)
    v_x_base = np.clip(rng.normal(-2.29, 0.36, n_valley), -3.05, -1.55)
    v_y_off = rng.uniform(0.08, 0.28, n_valley)

    # Crossing particles: travel from x = -2.35 over peak (-0.15) to x = +3.05
    n_cross = 7
    c_phases = np.linspace(0.0, 1.0, n_cross, endpoint=False)

    t_clock = {"t": 0.0}

    def _dots():
        t = t_clock["t"]
        fl = float(np.clip(flux_tr.get_value(), 0.0, 1.5))
        g = VGroup()
        for i in range(n_valley):
            xi = v_x_base[i] + 0.25 * np.sin(v_freqs[i] * t + v_phases[i])
            yi = _G_curve(xi, 1.8) + v_y_off[i] + 0.10 * np.abs(np.cos(1.9 * v_freqs[i] * t + v_phases[i]))
            g.add(Dot(_strip_pt(xi, yi), radius=0.082, color=YELLOW))
        if fl > 0.04:
            n_active = max(1, int(round(n_cross * min(fl, 1.0))))
            speed = 0.34 * (0.4 + 0.6 * fl)
            for j in range(n_active):
                u = (c_phases[j] + t * speed) % 1.0
                xj = -2.35 + u * 5.40
                yj = _G_curve(xj, 1.8) + 0.12
                op = min(1.0, u / 0.12) * min(1.0, (1.0 - u) / 0.12)
                g.add(Dot(_strip_pt(xj, yj), radius=0.095, color=YELLOW).set_opacity(op))
        return g

    dots = always_redraw(_dots)
    driver = VMobject().add_updater(lambda _, dt: t_clock.__setitem__("t", t_clock["t"] + dt))

    peak_x = -0.15
    peak_pt = _strip_pt(peak_x, _G_curve(peak_x, 1.8))
    ts_glow = Dot(peak_pt, radius=0.12, color=PURPLE, stroke_color=TEXT, stroke_width=2.5)
    ts_glow.set_opacity(1.0 if show_ts_peak else 0.0)

    strip = VGroup(divider, high_curve, low_curve, dots, tag, ts_glow, driver)
    strip.flux = flux_tr
    strip.peak_pt = peak_pt
    strip.ts_glow = ts_glow
    strip.tag = tag
    strip.high_curve = high_curve
    strip.low_curve = low_curve
    return strip


# ------------------------------------------------------------------ enzyme active-site cup & hinged cleft
def _rot2(pt, angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([pt[0] * c - pt[1] * s, pt[0] * s + pt[1] * c, 0.0])


def build_cup_mobject(center, scale=1.0, open_frac=0.0, show_knobs=False, opacity=1.0):
    """Build the TEAL active-site cup from two symmetric hinged lips meeting cleanly at a hinge pin."""
    c = np.array(center, dtype=float)
    ang = 0.62 * float(open_frac)  # ~35.5 deg outward per jaw

    hinge_r = np.array([0.22, -0.68, 0.0])
    rj_local = [
        np.array([0.00, -0.14, 0.0]),
        np.array([0.56, -0.10, 0.0]),
        np.array([1.08, 0.25, 0.0]),
        np.array([1.16, 0.78, 0.0]),
        np.array([0.86, 1.24, 0.0]),
        np.array([0.38, 1.32, 0.0]),
        np.array([0.30, 1.04, 0.0]),
        np.array([0.68, 0.92, 0.0]),
        np.array([0.76, 0.66, 0.0]),
        np.array([0.60, 0.34, 0.0]),
        np.array([0.00, 0.22, 0.0]),
    ]
    r_pts = [c + (hinge_r + _rot2(p, -ang)) * scale for p in rj_local]
    l_pts = [
        c + (np.array([-hinge_r[0], hinge_r[1], 0.0]) + np.array([-q[0], q[1], 0.0])) * scale
        for q in [_rot2(p, -ang) for p in rj_local]
    ]

    jaw_r = Polygon(
        *r_pts, stroke_color=TEAL, stroke_width=5.2, stroke_opacity=opacity,
        fill_color=TEAL, fill_opacity=0.48 * opacity,
    )
    jaw_l = Polygon(
        *l_pts, stroke_color=TEAL, stroke_width=5.2, stroke_opacity=opacity,
        fill_color=TEAL, fill_opacity=0.48 * opacity,
    )
    for m in (jaw_r, jaw_l):
        m.round_corners(radius=0.10 * scale)

    # Clean circular hinge bridge linking left and right jaws without overlapping rectangles
    hinge_pin = RoundedRectangle(
        corner_radius=0.16 * scale, width=0.52 * scale, height=0.34 * scale,
        stroke_color=TEAL, stroke_width=4.8, stroke_opacity=opacity,
        fill_color=TEAL, fill_opacity=0.50 * opacity,
    ).move_to(c + np.array([0.0, -0.64, 0.0]) * scale)

    g = VGroup(jaw_l, jaw_r, hinge_pin)
    if show_knobs:
        knob_local = np.array([0.46, 0.96, 0.0])
        kr_pos = c + (hinge_r + _rot2(knob_local, -ang)) * scale
        kl_pos = c + (
            np.array([-hinge_r[0], hinge_r[1], 0.0])
            + np.array([-_rot2(knob_local, -ang)[0], _rot2(knob_local, -ang)[1], 0.0])
        ) * scale
        kr = Dot(kr_pos, radius=0.12 * scale, color=TEAL, stroke_color=TEXT, stroke_width=2.2).set_opacity(opacity)
        kl = Dot(kl_pos, radius=0.12 * scale, color=TEAL, stroke_color=TEXT, stroke_width=2.2).set_opacity(opacity)
        g.add(kl, kr)
        g.knob_l, g.knob_r = kl, kr
    g.pocket_center = c
    return g


def make_live_cup(center_tr, open_tr, scale=1.0, show_knobs=False, opacity_tr=None):
    """Cup driven by ValueTrackers for center, open_frac, and optional opacity."""
    if opacity_tr is None:
        opacity_tr = ValueTracker(1.0)
    if isinstance(center_tr, (list, tuple, np.ndarray)):
        c_fn = lambda: np.array(center_tr, dtype=float)
    else:
        c_fn = center_tr
    return always_redraw(
        lambda: build_cup_mobject(
            c_fn(), scale=scale, open_frac=open_tr.get_value(),
            show_knobs=show_knobs, opacity=opacity_tr.get_value(),
        )
    )


def make_ts_oval(center, scale=1.0, color=PURPLE, opacity=1.0):
    """Stretched transition-state oval sized to fit snugly inside the closed cup."""
    return Ellipse(
        width=1.42 * scale, height=0.84 * scale,
        stroke_color=color, stroke_width=4.5, stroke_opacity=opacity,
        fill_color=color, fill_opacity=0.52 * opacity,
    ).move_to(center)


def make_contact_ticks(center, scale=1.0, count=8, oval=True, opacity=1.0):
    """GOLD contact ticks around the pocket interior."""
    c = np.array(center, dtype=float)
    rx = (0.76 if oval else 0.50) * scale
    ry = (0.48 if oval else 0.50) * scale
    if count == 8:
        angles = np.linspace(0.22 * PI, 1.78 * PI, 8)
    elif count == 2:
        angles = [1.18 * PI, 1.82 * PI]
    else:
        angles = np.linspace(0.2 * PI, 1.8 * PI, count)
    ticks = VGroup()
    for a in angles:
        d = np.array([np.cos(a), np.sin(a), 0.0])
        p_in = c + np.array([rx * d[0], ry * d[1], 0.0])
        p_out = c + np.array([(rx + 0.20 * scale) * d[0], (ry + 0.20 * scale) * d[1], 0.0])
        ticks.add(Line(p_in, p_out, color=GOLD, stroke_width=4.8 * min(1.25, max(0.85, scale)), stroke_opacity=opacity))
    return ticks


# ------------------------------------------------------------------ Fischer's rigid lock & keys
def make_rigid_lock(center, scale=1.0, opacity=1.0):
    """ORANGE flat rectangular block with straight edges and a machined U-slot cut into its top."""
    c = np.array(center, dtype=float)
    w_half = 1.25 * scale
    h_bot = -1.05 * scale
    h_top = 0.72 * scale
    slot_w = 0.42 * scale
    slot_bot = -0.18 * scale
    arc_angles = np.linspace(0.0, -PI, 16)
    arc_pts = [c + np.array([slot_w * np.cos(a), slot_bot + slot_w * np.sin(a), 0.0]) for a in arc_angles]
    pts = [
        c + np.array([-w_half, h_bot, 0.0]),
        c + np.array([w_half, h_bot, 0.0]),
        c + np.array([w_half, h_top, 0.0]),
        c + np.array([slot_w, h_top, 0.0]),
        c + np.array([slot_w, slot_bot, 0.0]),
        *arc_pts[1:-1],
        c + np.array([-slot_w, slot_bot, 0.0]),
        c + np.array([-slot_w, h_top, 0.0]),
        c + np.array([-w_half, h_top, 0.0]),
    ]
    block = Polygon(
        *pts, stroke_color=ORANGE, stroke_width=5.4, stroke_opacity=opacity,
        fill_color=ORANGE, fill_opacity=0.42 * opacity,
    )
    block.slot_center = c + np.array([0.0, slot_bot, 0.0])
    block.top_y = c[1] + h_top
    block.slot_r = slot_w
    return block


def make_key_dot(center, radius=0.40, bump=False, color=YELLOW, opacity=1.0):
    """Round YELLOW substrate key-dot, or near-twin with one small cartoon bump on the right side."""
    c = np.array(center, dtype=float)
    main = Circle(
        radius=radius, stroke_color=color, stroke_width=3.8, stroke_opacity=opacity,
        fill_color=color, fill_opacity=0.60 * opacity,
    ).move_to(c)
    if not bump:
        return main
    knob = Circle(
        radius=radius * 0.42, stroke_color=color, stroke_width=3.8, stroke_opacity=opacity,
        fill_color=color, fill_opacity=0.70 * opacity,
    ).move_to(c + RIGHT * (radius * 0.92))
    return VGroup(main, knob)


def make_lock_ticks(slot_center, radius=0.42, opacity=1.0):
    """8 GOLD ticks ringing the key seated inside the rigid lock slot."""
    c = np.array(slot_center, dtype=float)
    angles = np.linspace(0.15 * PI, 1.85 * PI, 8)
    ticks = VGroup()
    for a in angles:
        d = np.array([np.cos(a), np.sin(a), 0.0])
        ticks.add(Line(c + d * radius, c + d * (radius + 0.17), color=GOLD, stroke_width=4.8, stroke_opacity=opacity))
    return ticks


def make_red_cross(center, size=1.0):
    c = np.array(center, dtype=float)
    l1 = Line(c + np.array([-size, -size, 0]) * 0.5, c + np.array([size, size, 0]) * 0.5, color=RED, stroke_width=7.5)
    l2 = Line(c + np.array([-size, size, 0]) * 0.5, c + np.array([size, -size, 0]) * 0.5, color=RED, stroke_width=7.5)
    return VGroup(l1, l2)


# ------------------------------------------------------------------ chip & statin helpers
def make_fix_chip(num_str, text_str=None, color=TEXT, size=30, width=1.95, height=0.72, fill_opacity=0.18):
    box = RoundedRectangle(
        corner_radius=0.14, width=width, height=height,
        stroke_color=color, stroke_width=2.8, fill_color=color, fill_opacity=fill_opacity,
    )
    txt = f"{num_str}: {text_str}" if text_str else num_str
    lab = T(txt, size=size, color=color).move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    return g


def make_statin(center, scale=1.0, opacity=1.0):
    """Two-part cartoon statin: HMG-like rounded pocket end (left) + longer MAGENTA tail (right)."""
    c = np.array(center, dtype=float)
    head = Circle(
        radius=0.42 * scale, stroke_color=MAGENTA, stroke_width=4.0, stroke_opacity=opacity,
        fill_color=MAGENTA, fill_opacity=0.50 * opacity,
    ).move_to(c + LEFT * 0.55 * scale)
    tail = RoundedRectangle(
        corner_radius=0.16 * scale, width=1.35 * scale, height=0.42 * scale,
        stroke_color=MAGENTA, stroke_width=4.0, stroke_opacity=opacity,
        fill_color=MAGENTA, fill_opacity=0.40 * opacity,
    ).move_to(c + RIGHT * 0.38 * scale)
    g = VGroup(tail, head)
    g.head, g.tail = head, tail
    return g


# ------------------------------------------------------------------ shared scene builders for continuity
def _s00_end_state():
    strip = make_top_strip(flux=1.0)
    cup = build_cup_mobject([-3.6, -1.05, 0], scale=1.22, open_frac=0.0)
    oval = make_ts_oval([-3.6, -1.05, 0], scale=1.22)
    ticks = make_contact_ticks([-3.6, -1.05, 0], scale=1.22, count=8)

    lock = make_rigid_lock([2.2, -1.30, 0], scale=1.12)
    key = make_key_dot(lock.slot_center, radius=0.40 * 1.12)

    c1 = make_fix_chip("1 ?", color=TEXT, size=32, width=1.65, height=0.72)
    c2 = make_fix_chip("2 ?", color=TEXT, size=32, width=1.65, height=0.72)
    c1.move_to([1.25, 0.72, 0])
    c2.move_to([3.20, 0.72, 0])
    return strip, VGroup(cup, oval, ticks, lock, key, c1, c2)


def _s05_world(include_question=True, show_ghost=False, live_motion=True):
    """Shared world for s05_predict (end) and s06_think (backdrop)."""
    strip = make_top_strip(flux=1.0)
    cleft_pos = np.array([0.0, -0.35, 0.0])
    open_tr = ValueTracker(1.0)
    if live_motion:
        t_sway = {"t": 0.0}

        def _sway(m, dt):
            t_sway["t"] += dt
            open_tr.set_value(0.94 + 0.06 * np.sin(2.1 * t_sway["t"]))

        sway_driver = VMobject().add_updater(_sway)
    else:
        sway_driver = VMobject()

    cup = make_live_cup(cleft_pos, open_tr, scale=1.55, show_knobs=True)
    hex_lab = T("hexokinase", size=30, color=TEAL).move_to([-4.35, -1.55, 0])

    phos_bead = Dot([1.68, 0.28, 0], radius=0.17, color=BLUE, stroke_color=TEXT, stroke_width=2.2)
    phos_chip = boxed_label("phosphate from ATP", BLUE, size=28, pad=0.18).move_to([4.05, 0.75, 0])

    glu_base = np.array([-1.85, 0.95, 0.0])
    glu_dot = Dot(glu_base, radius=0.30, color=YELLOW, stroke_color=TEXT, stroke_width=2.2)
    if live_motion:
        bob(glu_dot, amp=0.05, speed=1.8, seed=3)
    glu_lab = T("glucose", size=30, color=YELLOW).next_to(glu_dot, LEFT, buff=0.42)
    oh_glu = T("OH", size=28, color=TEXT).next_to(glu_dot, RIGHT, buff=0.18)

    # 14 outer CYAN water dots placed cleanly clear of every label box + 1 inside cleft
    water_anchors = [
        [-5.25, 0.90], [-4.85, 0.15], [-5.35, -0.60], [-3.95, 0.15], [-3.40, -0.55],
        [-2.75, -0.08], [-5.05, -2.15], [-2.85, -1.95],
        [3.00, -0.32], [4.15, -0.25], [5.25, -0.15], [3.45, -1.05], [5.05, -1.00], [2.75, -1.85],
    ]
    water_dots = VGroup()
    for k, (wx, wy) in enumerate(water_anchors):
        d = Dot([wx, wy, 0], radius=0.125, color=CYAN)
        if live_motion:
            # Gentle circular diffusion clear of neighbouring labels
            base = np.array([wx, wy, 0.0])
            ph = k * 0.9
            sp = 1.6 + 0.15 * (k % 5)

            def _orb(mob, dt, b=base, p=ph, s=sp):
                mob._orb_t = getattr(mob, "_orb_t", p) + dt * s
                mob.move_to(b + np.array([0.11 * np.cos(mob._orb_t), 0.11 * np.sin(mob._orb_t), 0.0]))

            d.add_updater(_orb)
        water_dots.add(d)

    cleft_water = Dot([0.05, -0.22, 0], radius=0.13, color=CYAN)
    if live_motion:
        bob(cleft_water, amp=0.05, speed=2.0, seed=19)
    oh_wat = T("OH", size=28, color=TEXT).next_to([0.05, -0.22, 0], DOWN, buff=0.28)

    water_lab = T("water", size=30, color=CYAN).move_to([4.25, -1.75, 0])

    world = VGroup(
        strip, cup, sway_driver, hex_lab, phos_bead, phos_chip,
        glu_dot, glu_lab, oh_glu, water_dots, cleft_water, oh_wat, water_lab,
    )
    if show_ghost:
        ga = DashedLine(phos_bead.get_left() + LEFT * 0.08, cleft_water.get_right() + RIGHT * 0.14,
                        color=BLUE, stroke_width=4, dash_length=0.14).set_opacity(0.55)
        world.add(ga)
    if include_question:
        qc = question_card("Why doesn't water take it?", y=-3.05, color=TEXT, size=34)
        world.add(qc)
    return world


# ================================================================== SCENES
class S00LinkAndHook(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        cup_center = np.array([0.0, -0.95, 0.0])
        cup = build_cup_mobject(cup_center, scale=1.65, open_frac=0.0)
        oval = make_ts_oval(cup_center, scale=1.65)
        ticks = make_contact_ticks(cup_center, scale=1.65, count=8)

        # NO fade from black: start immediately with the living world
        self.add(strip, cup, oval, ticks)

        # Cue 1: "gripping the transition state hardest"
        self.at("gripping the transition")
        self.play(ticks.animate.scale(1.12).set_stroke(width=7.0), run_time=0.45)
        self.play(ticks.animate.scale(1 / 1.12).set_stroke(width=5.0), run_time=0.45)

        # Cue 2: "famous picture" -> cup slides left, ORANGE rigid lock slides in at centre-right
        self.at("famous picture")
        left_cup = build_cup_mobject([-3.6, -1.05, 0], scale=1.22, open_frac=0.0)
        left_oval = make_ts_oval([-3.6, -1.05, 0], scale=1.22)
        left_ticks = make_contact_ticks([-3.6, -1.05, 0], scale=1.22, count=8)

        lock = make_rigid_lock([2.2, -1.30, 0], scale=1.12)
        lock_off = lock.copy().shift(RIGHT * 5.0).set_opacity(0)
        key_start = lock.slot_center + UP * 1.45
        key = make_key_dot(key_start, radius=0.40 * 1.12)

        self.play(
            Transform(cup, left_cup),
            Transform(oval, left_oval),
            Transform(ticks, left_ticks),
            ReplacementTransform(lock_off, lock),
            run_time=1.3,
        )
        self.play(FadeIn(key, shift=DOWN * 0.2), run_time=0.35)
        self.play(key.animate.move_to(lock.slot_center), run_time=0.65, rate_func=rush_into)

        # Cue 3: "two fixes" -> two empty chip outlines labelled '1' and '2'
        self.at("two fixes")
        c1_box = RoundedRectangle(corner_radius=0.14, width=1.65, height=0.72, stroke_color=TEXT, stroke_width=2.8).move_to([1.25, 0.72, 0])
        c2_box = RoundedRectangle(corner_radius=0.14, width=1.65, height=0.72, stroke_color=TEXT, stroke_width=2.8).move_to([3.20, 0.72, 0])
        n1 = T("1", size=34, color=TEXT).move_to(c1_box.get_center() + LEFT * 0.35)
        n2 = T("2", size=34, color=TEXT).move_to(c2_box.get_center() + LEFT * 0.35)
        self.play(FadeIn(c1_box, n1), FadeIn(c2_box, n2), run_time=0.7)

        # Cue 4: "What are they" -> '?' (40) pops into each chip
        self.at("What are they")
        q1 = T("?", size=40, color=GOLD).move_to(c1_box.get_center() + RIGHT * 0.28)
        q2 = T("?", size=40, color=GOLD).move_to(c2_box.get_center() + RIGHT * 0.28)
        self.play(FadeIn(q1, scale=1.3), FadeIn(q2, scale=1.3), run_time=0.55)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        strip, stage = _s00_end_state()
        stage.set_opacity(0.20)
        self.add(strip, stage)

        title = T("Two Fixes for the Lock", size=54, font=TITLE_FONT, color=TEXT).move_to([0, -0.55, 0])
        fit(title, max_w=11.5)
        rule = Line(LEFT * 2.4, RIGHT * 2.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.28)

        self.play(FadeIn(title, shift=UP * 0.12), GrowFromCenter(rule), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.4)
        self.finish()


class S02Fischer(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        cup = build_cup_mobject([-3.6, -1.05, 0], scale=1.22, open_frac=0.0, opacity=0.4)
        oval = make_ts_oval([-3.6, -1.05, 0], scale=1.22, opacity=0.4)
        ticks = make_contact_ticks([-3.6, -1.05, 0], scale=1.22, count=8, opacity=0.4)

        c1 = make_fix_chip("1 ?", color=TEXT, size=30, width=1.55, height=0.68).move_to([1.25, 0.72, 0])
        c2 = make_fix_chip("2 ?", color=TEXT, size=30, width=1.55, height=0.68).move_to([3.20, 0.72, 0])

        lock = make_rigid_lock([2.2, -1.30, 0], scale=1.12)
        key = make_key_dot(lock.slot_center, radius=0.40 * 1.12)
        self.add(strip, cup, oval, ticks, lock, key, c1, c2)

        # Grow lock to fill ~60% of main stage at centre-right; key waits cleanly to the LEFT of label
        big_lock = make_rigid_lock([2.2, -1.05, 0], scale=1.50)
        key_wait = np.array([-0.10, 0.18, 0.0])
        big_key = make_key_dot(key_wait, radius=0.40 * 1.50)
        fischer_lab = T("Fischer, 1894", size=30, color=ORANGE).move_to([2.2, 1.15, 0])

        self.play(
            c1.animate.move_to([-4.95, 0.92, 0]),
            c2.animate.move_to([-2.95, 0.92, 0]),
            Transform(lock, big_lock),
            Transform(key, big_key),
            FadeIn(fischer_lab, shift=DOWN * 0.1),
            run_time=1.3,
        )

        # Cue 1: "one sugar" -> round YELLOW dot slides right over slot and drops flush
        self.at("one sugar")
        self.play(key.animate.move_to([2.2, 0.15, 0]), run_time=0.4)
        self.play(key.animate.move_to(big_lock.slot_center), run_time=0.55, rate_func=rush_into)

        # Cue 2: "ignores its near" -> first dot exits; near-twin approaches from right, catches on rim, bounces right
        self.at("ignores its near")
        self.play(key.animate.move_to([-0.2, 0.15, 0]).set_opacity(0.0), run_time=0.55)
        twin = make_key_dot([4.55, 0.15, 0], radius=0.40 * 1.50, bump=True)
        self.play(FadeIn(twin), run_time=0.25)
        catch_pos = big_lock.slot_center + UP * 1.38 + RIGHT * 0.08
        self.play(twin.animate.move_to(catch_pos), run_time=0.5, rate_func=rush_into)
        self.play(twin.animate.shift(RIGHT * 2.0 + DOWN * 0.15).rotate(-0.35), run_time=0.55, rate_func=rush_from)
        self.play(FadeOut(twin), run_time=0.25)

        # Cue 3: "lock and key" -> first dot seats again, chip 'specificity' settles under lock
        self.at("lock and key")
        key.set_opacity(1.0).move_to([-0.10, 0.18, 0])
        spec = boxed_label("specificity", TEXT, size=30, pad=0.18).move_to([2.2, -3.20, 0])
        self.play(key.animate.move_to([2.2, 0.15, 0]), FadeIn(spec, shift=UP * 0.15), run_time=0.45)
        self.play(key.animate.move_to(big_lock.slot_center), run_time=0.55, rate_func=rush_into)
        self.finish()


class S03FixFit(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        cup = build_cup_mobject([-3.6, -1.05, 0], scale=1.22, open_frac=0.0, opacity=0.4)
        oval = make_ts_oval([-3.6, -1.05, 0], scale=1.22, opacity=0.4)
        ticks_dim = make_contact_ticks([-3.6, -1.05, 0], scale=1.22, count=8, opacity=0.4)

        c1 = make_fix_chip("1 ?", color=TEXT, size=30, width=1.55, height=0.68).move_to([-4.95, 0.92, 0])
        c2 = make_fix_chip("2 ?", color=TEXT, size=30, width=1.55, height=0.68).move_to([-2.95, 0.92, 0])

        lock = make_rigid_lock([2.2, -1.05, 0], scale=1.50)
        key = make_key_dot(lock.slot_center, radius=0.40 * 1.50)
        fischer_lab = T("Fischer, 1894", size=30, color=ORANGE).move_to([2.2, 1.15, 0])
        spec = boxed_label("specificity", TEXT, size=30, pad=0.18).move_to([2.2, -3.20, 0])
        self.add(strip, cup, oval, ticks_dim, lock, key, fischer_lab, spec, c1, c2)

        # Cue 1: "Fix one" -> chip 1 fills PURPLE with 'fit'
        self.at("Fix one")
        c1_fit = make_fix_chip("1", "fit", color=PURPLE, size=30, width=1.65, height=0.68, fill_opacity=0.22).move_to([-4.95, 0.92, 0])
        self.play(swap(c1, c1_fit, run_time=0.65), FadeOut(fischer_lab, run_time=0.65), FadeOut(spec, run_time=0.65))

        # Cue 2: "cut for the substrate" -> 8 GOLD ticks light & grip tightly round YELLOW dot in ORANGE slot
        self.at("cut for the substrate")
        lock_ticks = make_lock_ticks(lock.slot_center, radius=0.42 * 1.50)
        self.play(FadeIn(lock_ticks), run_time=0.7)
        for _ in range(3):
            self.play(
                lock_ticks.animate.scale(1.14).set_stroke(width=6.8),
                key.animate.set_fill(opacity=0.88),
                run_time=0.60,
            )
            self.play(
                lock_ticks.animate.scale(1 / 1.14).set_stroke(width=4.8),
                key.animate.set_fill(opacity=0.60),
                run_time=0.60,
            )

        # Cue 3: "Enzymes don't" -> RED cross stamps over those 8 ticks and they fade
        self.at("Enzymes don't")
        cross = make_red_cross(lock.slot_center, size=1.45)
        self.play(Create(cross), run_time=0.4)
        self.play(FadeOut(lock_ticks), FadeOut(cross), run_time=0.6)

        # Cue 4: "and Pauling" -> cup brightens, loose substrate (2 ticks) -> stretched oval (8 ticks)
        self.at("and Pauling")
        hp_lab = T("Haldane, Pauling", size=30, color=PURPLE).move_to([-3.6, 0.28, 0])
        bright_cup = build_cup_mobject([-3.6, -1.15, 0], scale=1.28, open_frac=0.18, opacity=1.0)
        sub_dot = make_key_dot([-3.6, -1.15, 0], radius=0.41, color=YELLOW)
        ticks_2 = make_contact_ticks([-3.6, -1.15, 0], scale=1.28, count=2, oval=False)

        self.play(
            FadeOut(oval), FadeOut(ticks_dim),
            Transform(cup, bright_cup),
            FadeIn(hp_lab, shift=DOWN * 0.1),
            run_time=0.6,
        )
        self.play(FadeIn(sub_dot, shift=DOWN * 0.2), FadeIn(ticks_2), run_time=0.45)

        closed_cup = build_cup_mobject([-3.6, -1.15, 0], scale=1.28, open_frac=0.0, opacity=1.0)
        ts_oval = make_ts_oval([-3.6, -1.15, 0], scale=1.28)
        ticks_8 = make_contact_ticks([-3.6, -1.15, 0], scale=1.28, count=8, oval=True)
        self.play(
            ReplacementTransform(sub_dot, ts_oval),
            Transform(cup, closed_cup),
            FadeOut(ticks_2),
            FadeIn(ticks_8),
            run_time=0.75,
        )

        # Cue 5: "transition state best"
        self.at("transition state best")
        best_lab = T("best fit: transition state", size=30, color=PURPLE).move_to([-3.4, -3.00, 0])
        self.play(FadeIn(best_lab, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S04FixShape(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        c1 = make_fix_chip("1", "fit", color=PURPLE, size=30, width=1.65, height=0.68, fill_opacity=0.22).move_to([-4.95, 0.92, 0])
        c2 = make_fix_chip("2 ?", color=TEXT, size=30, width=1.55, height=0.68).move_to([-2.95, 0.92, 0])

        cup = build_cup_mobject([-3.6, -1.15, 0], scale=1.28, open_frac=0.0)
        ts_oval = make_ts_oval([-3.6, -1.15, 0], scale=1.28)
        ticks_8 = make_contact_ticks([-3.6, -1.15, 0], scale=1.28, count=8, oval=True)
        hp_lab = T("Haldane, Pauling", size=30, color=PURPLE).move_to([-3.6, 0.28, 0])
        best_lab = T("best fit: transition state", size=30, color=PURPLE).move_to([-3.4, -3.00, 0])

        lock = make_rigid_lock([2.2, -1.05, 0], scale=1.50)
        key = make_key_dot(lock.slot_center, radius=0.40 * 1.50)
        self.add(strip, c1, c2, cup, ts_oval, ticks_8, hp_lab, best_lab, lock, key)

        # Cue 1: "Fix 2" -> chip 2 fills TEAL with 'shape'
        self.at("Fix 2")
        c2_shape = make_fix_chip("2", "shape", color=TEAL, size=30, width=2.00, height=0.68, fill_opacity=0.22).move_to([-2.75, 0.92, 0])
        self.play(swap(c2, c2_shape, run_time=0.65))

        # Cue 2: "Locks don't change" -> 3 YELLOW dots tap ORANGE lock from 3 sides; lock stays rigid
        self.at("Locks don't change")
        lc = lock.get_center()
        d_left = Dot(lc + LEFT * 2.65, radius=0.14, color=YELLOW)
        d_right = Dot(lc + RIGHT * 2.65, radius=0.14, color=YELLOW)
        d_bot = Dot(lc + DOWN * 2.15, radius=0.14, color=YELLOW)
        self.play(FadeIn(d_left), FadeIn(d_right), FadeIn(d_bot), run_time=0.25)
        self.play(
            d_left.animate.move_to(lc + LEFT * 1.98),
            d_right.animate.move_to(lc + RIGHT * 1.98),
            d_bot.animate.move_to(lc + DOWN * 1.65),
            rate_func=there_and_back, run_time=0.75,
        )
        self.play(
            FadeOut(d_left), FadeOut(d_right), FadeOut(d_bot),
            FadeOut(lock), FadeOut(key),
            FadeOut(hp_lab), FadeOut(best_lab), FadeOut(ts_oval), FadeOut(ticks_8),
            run_time=0.7,
        )

        # Cue 3: "Koshland"
        self.at("Koshland")
        kosh_lab = T("Koshland, 1958", size=30, color=TEAL).move_to([-4.2, 0.08, 0])
        self.play(FadeIn(kosh_lab, shift=DOWN * 0.1), run_time=0.55)

        # Cue 4: "His case was" -> cup moves to center and opens into wide hinged cleft + knobs + phosphate chip
        self.at("His case was")
        open_cleft = build_cup_mobject([0.0, -0.35, 0], scale=1.55, open_frac=1.0, show_knobs=True)
        hex_lab = T("hexokinase", size=30, color=TEAL).move_to([-4.35, -1.55, 0])
        phos_bead = Dot([1.68, 0.28, 0], radius=0.17, color=BLUE, stroke_color=TEXT, stroke_width=2.2)
        phos_chip = boxed_label("phosphate from ATP", BLUE, size=28, pad=0.18).move_to([4.05, 0.75, 0])

        self.play(
            FadeOut(c1), FadeOut(c2_shape), FadeOut(kosh_lab),
            Transform(cup, open_cleft),
            FadeIn(hex_lab, shift=UP * 0.1),
            run_time=1.05,
        )
        self.play(FadeIn(phos_bead), FadeIn(phos_chip, shift=LEFT * 0.15), run_time=0.5)

        # Cue 5: "onto glucose" -> YELLOW dot labelled 'glucose' drifts near opening
        self.at("onto glucose")
        glu_dot = Dot([-1.85, 0.95, 0], radius=0.30, color=YELLOW, stroke_color=TEXT, stroke_width=2.2)
        glu_lab = T("glucose", size=30, color=YELLOW).next_to(glu_dot, LEFT, buff=0.42)
        self.play(FadeIn(glu_dot, shift=DOWN * 0.2), FadeIn(glu_lab, shift=RIGHT * 0.1), run_time=0.7)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        cup = build_cup_mobject([0.0, -0.35, 0], scale=1.55, open_frac=1.0, show_knobs=True)
        hex_lab = T("hexokinase", size=30, color=TEAL).move_to([-4.35, -1.55, 0])
        phos_bead = Dot([1.68, 0.28, 0], radius=0.17, color=BLUE, stroke_color=TEXT, stroke_width=2.2)
        phos_chip = boxed_label("phosphate from ATP", BLUE, size=28, pad=0.18).move_to([4.05, 0.75, 0])
        glu_dot = Dot([-1.85, 0.95, 0], radius=0.30, color=YELLOW, stroke_color=TEXT, stroke_width=2.2)
        glu_lab = T("glucose", size=30, color=YELLOW).next_to(glu_dot, LEFT, buff=0.42)
        self.add(strip, cup, hex_lab, phos_bead, phos_chip, glu_dot, glu_lab)

        # Cue 1: "Water" -> ~15 CYAN dots drift in around open cleft, completely clear of all labels
        self.at("Water")
        water_anchors = [
            [-5.25, 0.90], [-4.85, 0.15], [-5.35, -0.60], [-3.95, 0.15], [-3.40, -0.55],
            [-2.75, -0.08], [-5.05, -2.15], [-2.85, -1.95],
            [3.00, -0.32], [4.15, -0.25], [5.25, -0.15], [3.45, -1.05], [5.05, -1.00], [2.75, -1.85],
        ]
        water_dots = VGroup(*[Dot([wx, wy, 0], radius=0.125, color=CYAN) for wx, wy in water_anchors])
        cleft_water = Dot([-0.30, 0.65, 0], radius=0.13, color=CYAN)
        water_lab = T("water", size=30, color=CYAN).move_to([4.25, -1.75, 0])
        self.play(FadeIn(water_dots, lag_ratio=0.05), FadeIn(cleft_water), FadeIn(water_lab), run_time=0.8)
        for k, (wx, wy) in enumerate(water_anchors):
            d = water_dots[k]
            base = np.array([wx, wy, 0.0])
            ph = k * 0.9
            sp = 1.6 + 0.15 * (k % 5)

            def _orb(mob, dt, b=base, p=ph, s=sp):
                mob._orb_t = getattr(mob, "_orb_t", p) + dt * s
                mob.move_to(b + np.array([0.11 * np.cos(mob._orb_t), 0.11 * np.sin(mob._orb_t), 0.0]))

            d.add_updater(_orb)

        # Cue 2: "same OH group" -> small 'OH' tag on glucose and one water dot
        self.at("same OH group")
        oh_glu = T("OH", size=28, color=TEXT).next_to(glu_dot, RIGHT, buff=0.18)
        oh_wat = T("OH", size=28, color=TEXT).next_to([0.05, -0.22, 0], DOWN, buff=0.28)
        self.play(FadeIn(oh_glu), FadeIn(oh_wat), cleft_water.animate.move_to([0.05, -0.22, 0]), run_time=0.6)

        # Cue 3: "An open site" -> ghost arrow from BLUE phosphate toward cleft water
        self.at("An open site")
        ghost_arrow = DashedLine(
            phos_bead.get_left() + LEFT * 0.08,
            cleft_water.get_right() + RIGHT * 0.14,
            color=BLUE, stroke_width=4.5, dash_length=0.14,
        ).set_opacity(0.55)
        self.play(Create(ghost_arrow), run_time=0.8)

        # Cue 4: "It doesn't" -> ghost arrow vanishes, phosphate stays on lip
        self.at("It doesn't")
        self.play(FadeOut(ghost_arrow), run_time=0.45)

        # Cue 5: "Why not" -> question card slides up in lower third
        self.at("Why not")
        qc = question_card("Why doesn't water take it?", y=-3.05, color=TEXT, size=34)
        self.play(FadeIn(qc, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S06Think(PredictPause):
    QUESTION = "Why doesn't water take it?"
    CARD = {"y": -3.05, "color": TEXT, "size": 34}
    RING_AT = (5.8, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _s05_world(include_question=False, show_ghost=False, live_motion=True)


class S07Answer(SpokenScene):
    def construct(self):
        world = _s05_world(include_question=True, show_ghost=False, live_motion=False)
        strip, _cup, _sway, hex_lab, phos_bead, phos_chip, glu_dot, glu_lab, oh_glu, water_dots, cleft_water, oh_wat, water_lab, qc = world
        open_tr = ValueTracker(1.0)
        live_cup = make_live_cup([0.0, -0.35, 0], open_tr, scale=1.55, show_knobs=True)
        glu_dot.set_z_index(2)
        phos_bead.set_z_index(2)
        self.add(strip, live_cup, hex_lab, phos_bead, phos_chip, glu_dot, glu_lab, oh_glu, water_dots, cleft_water, oh_wat, water_lab, qc)

        # Card gone right away
        self.play(FadeOut(qc, shift=DOWN * 0.15), run_time=0.35)

        # Cue 1: "not ready" -> CYAN dot inside cleft drifts out cleanly (left of phosphate chip)
        self.at("not ready")
        self.play(FadeOut(oh_wat), cleft_water.animate.move_to([-2.30, 1.15, 0]), run_time=0.8)

        # Cue 2: "glucose binding" -> glucose drops in, both lips swing shut around it
        self.at("glucose binding")
        self.play(
            FadeOut(glu_lab), FadeOut(oh_glu),
            glu_dot.animate.move_to([-0.24, 0.05, 0]),
            phos_bead.animate.move_to([0.38, 0.05, 0]),
            open_tr.animate.set_value(0.0),
            run_time=1.2,
        )

        # Cue 3: "into line" -> short GOLD line links left knob - glucose - BLUE phosphate - right knob BEHIND beads
        self.at("into line")
        closed_cup = build_cup_mobject([0.0, -0.35, 0], scale=1.55, open_frac=0.0, show_knobs=True)
        gold_line = Line(
            [closed_cup.knob_l.get_center()[0], 0.05, 0],
            [closed_cup.knob_r.get_center()[0], 0.05, 0],
            color=GOLD, stroke_width=6.0,
        ).set_z_index(-1)
        self.play(Create(gold_line), run_time=0.6)

        # Cue 4: "Water is too small" -> right inset (~30% height) replays open cleft with only a CYAN dot inside, lips still
        self.at("Water is too small")
        inset_box = RoundedRectangle(corner_radius=0.14, width=3.3, height=2.35, stroke_color=GREY, stroke_width=2.5,
                                     fill_color=BG, fill_opacity=1.0).move_to([4.20, -1.15, 0]).set_z_index(4)
        inset_cup = build_cup_mobject([4.20, -1.25, 0], scale=0.84, open_frac=1.0, show_knobs=True).set_z_index(5)
        inset_wat = Dot([4.20, -1.15, 0], radius=0.12, color=CYAN).set_z_index(6)
        inset_grp = VGroup(inset_box, inset_cup, inset_wat)
        self.play(
            FadeOut(water_lab),
            FadeIn(inset_grp, shift=LEFT * 0.2),
            run_time=0.7,
        )

        # Cue 5: "induces the fit" -> inset fades, label 'induced fit' (TEAL, 30) settles under closed cleft
        self.at("induces the fit")
        ind_lab = T("induced fit", size=30, color=TEAL).move_to([-1.4, -2.45, 0])
        self.play(FadeOut(inset_grp), FadeIn(ind_lab, shift=UP * 0.1), run_time=0.7)

        # Cue 6: "many enzymes" -> chip 'many enzymes flex' (TEAL, 28) appears beside it
        self.at("many enzymes")
        flex_chip = boxed_label("many enzymes flex", TEAL, size=28, pad=0.18).move_to([1.95, -2.45, 0])
        self.play(FadeIn(flex_chip, shift=LEFT * 0.15), run_time=0.6)
        self.finish()


class S08Selection(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        open_tr = ValueTracker(0.0)
        live_cup = make_live_cup([0.0, -0.35, 0], open_tr, scale=1.55, show_knobs=True)
        hex_lab = T("hexokinase", size=30, color=TEAL).move_to([-4.35, -1.55, 0])
        phos_bead = Dot([0.38, 0.05, 0], radius=0.17, color=BLUE, stroke_color=TEXT, stroke_width=2.2).set_z_index(2)
        phos_chip = boxed_label("phosphate from ATP", BLUE, size=28, pad=0.18).move_to([4.05, 0.75, 0])
        glu_dot = Dot([-0.24, 0.05, 0], radius=0.30, color=YELLOW, stroke_color=TEXT, stroke_width=2.2).set_z_index(2)
        closed_cup = build_cup_mobject([0.0, -0.35, 0], scale=1.55, open_frac=0.0, show_knobs=True)
        gold_line = Line(
            [closed_cup.knob_l.get_center()[0], 0.05, 0],
            [closed_cup.knob_r.get_center()[0], 0.05, 0],
            color=GOLD, stroke_width=6.0,
        ).set_z_index(-1)
        ind_lab = T("induced fit", size=30, color=TEAL).move_to([-1.4, -2.45, 0])
        flex_chip = boxed_label("many enzymes flex", TEAL, size=28, pad=0.18).move_to([1.95, -2.45, 0])
        self.add(strip, live_cup, hex_lab, phos_bead, phos_chip, glu_dot, gold_line, ind_lab, flex_chip)

        self.play(
            FadeOut(hex_lab), FadeOut(phos_bead), FadeOut(phos_chip), FadeOut(glu_dot),
            FadeOut(gold_line), FadeOut(ind_lab), FadeOut(flex_chip),
            run_time=0.7,
        )

        # Cue 1: "already shift" -> empty cleft flips open<->closed (~1.5 s period)
        self.at("already shift")
        oc_lab = T("open and closed, unbound", size=30, color=TEAL).move_to([0.0, -2.35, 0])
        self.play(FadeIn(oc_lab, shift=UP * 0.1), run_time=0.45)

        for val, rt in [(1.0, 0.75), (0.0, 0.75), (1.0, 0.75), (0.0, 0.75), (1.0, 0.75), (0.0, 0.75)]:
            if self.elapsed() >= self.t_of("picks the one") - 0.8:
                break
            self.play(open_tr.animate.set_value(val), run_time=rt)

        # Cue 2: "picks the one" -> arrive during a closed moment, settle in, stay closed
        self.at("picks the one")
        if open_tr.get_value() > 0.1:
            self.play(open_tr.animate.set_value(0.0), run_time=0.5)
        sub = make_key_dot([-3.4, -0.35, 0], radius=0.40, color=YELLOW)
        self.play(FadeIn(sub, shift=RIGHT * 0.2), run_time=0.35)
        self.play(sub.animate.move_to([0.0, -0.35, 0]), run_time=0.75)

        # Cue 3: "conformational selection" -> swap label
        self.at("conformational selection")
        cs_lab = T("conformational selection", size=30, color=TEAL).move_to([0.0, -2.35, 0])
        self.play(swap(oc_lab, cs_lab, run_time=0.65))

        # Cue 4: "mix both" -> two short arrows converge, 'induced fit' & 'selection', chip 'often both'
        self.at("mix both", lead=0.45)
        arr_l = Arrow([-3.3, -0.35, 0], [-1.95, -0.35, 0], buff=0.0, color=TEAL, stroke_width=4.8, max_tip_length_to_length_ratio=0.22)
        arr_r = Arrow([3.3, -0.35, 0], [1.95, -0.35, 0], buff=0.0, color=TEAL, stroke_width=4.8, max_tip_length_to_length_ratio=0.22)
        l_ind = T("induced fit", size=28, color=TEAL).next_to(arr_l, LEFT, buff=0.18)
        l_sel = T("selection", size=28, color=TEAL).next_to(arr_r, RIGHT, buff=0.18)
        both_chip = boxed_label("often both", TEXT, size=30, pad=0.18).move_to([0.0, -3.10, 0])
        self.play(
            GrowArrow(arr_l), GrowArrow(arr_r),
            FadeIn(l_ind), FadeIn(l_sel),
            FadeIn(both_chip, shift=UP * 0.1),
            run_time=0.85,
        )
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        cup_center = np.array([0.0, -1.30, 0.0])
        open_tr = ValueTracker(0.0)
        live_cup = make_live_cup(cup_center, open_tr, scale=1.35, show_knobs=False)
        oval = make_ts_oval(cup_center, scale=1.35)
        ticks = make_contact_ticks(cup_center, scale=1.35, count=8)

        old_sub = make_key_dot([0.0, -0.35, 0], radius=0.40, color=YELLOW)
        old_lab = T("conformational selection", size=30, color=TEAL).move_to([0.0, -2.35, 0])
        old_both = boxed_label("often both", TEXT, size=30, pad=0.18).move_to([0.0, -3.10, 0])
        self.add(strip, live_cup, oval, ticks, old_sub, old_lab, old_both)

        self.play(FadeOut(old_sub), FadeOut(old_lab), FadeOut(old_both), run_time=0.5)

        # Cue 1: "fits best"
        self.at("fits best")
        q_fit = boxed_label("fits best?", TEXT, size=30, pad=0.20).move_to([-3.2, 0.72, 0])
        self.play(FadeIn(q_fit, shift=DOWN * 0.1), run_time=0.5)

        # Cue 2: "changes shape"
        self.at("changes shape")
        q_shp = boxed_label("changes shape?", TEXT, size=30, pad=0.20).move_to([3.2, 0.72, 0])
        self.play(FadeIn(q_shp, shift=DOWN * 0.1), run_time=0.5)

        # Cue 3: "separate questions"
        self.at("separate questions")
        vdiv = Line([0.0, 1.25, 0], [0.0, 0.05, 0], color=TEXT, stroke_width=3.5)
        self.play(Create(vdiv), run_time=0.55)

        # Cue 4: "the transition state"
        self.at("the transition state")
        a_fit = boxed_label("transition state", PURPLE, size=30, pad=0.20, fill_opacity=0.24).move_to([-3.2, 0.72, 0])
        self.play(
            swap(q_fit, a_fit, run_time=0.6),
            oval.animate.set_fill(opacity=0.75).set_stroke(width=5.8),
        )

        # Cue 5: "many enzymes"
        self.at("many enzymes")
        a_shp = boxed_label("many enzymes: yes", TEAL, size=30, pad=0.20, fill_opacity=0.24).move_to([3.2, 0.72, 0])
        self.play(swap(q_shp, a_shp, run_time=0.6))
        self.play(open_tr.animate.set_value(0.85), run_time=0.45)
        self.play(open_tr.animate.set_value(0.0), run_time=0.45)
        self.finish()


class S10DrugLogic(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0)
        cup_center = np.array([0.0, -1.00, 0.0])
        open_tr = ValueTracker(0.0)
        live_cup = make_live_cup(cup_center, open_tr, scale=1.45, show_knobs=False)
        oval = make_ts_oval(cup_center, scale=1.35)
        ticks = make_contact_ticks(cup_center, scale=1.35, count=8)
        a_fit = boxed_label("transition state", PURPLE, size=30, pad=0.20, fill_opacity=0.24).move_to([-3.2, 0.72, 0])
        a_shp = boxed_label("many enzymes: yes", TEAL, size=30, pad=0.20, fill_opacity=0.24).move_to([3.2, 0.72, 0])
        vdiv = Line([0.0, 1.25, 0], [0.0, 0.05, 0], color=TEXT, stroke_width=3.5)
        self.add(strip, live_cup, oval, ticks, a_fit, a_shp, vdiv)

        c_fit = boxed_label("transition state", PURPLE, size=26, pad=0.16, fill_opacity=0.24).move_to([-4.4, 0.92, 0])
        c_shp = boxed_label("many enzymes: yes", TEAL, size=26, pad=0.16, fill_opacity=0.24).move_to([4.15, 0.92, 0])
        self.play(
            FadeOut(vdiv), FadeOut(oval), FadeOut(ticks),
            ReplacementTransform(a_fit, c_fit),
            ReplacementTransform(a_shp, c_shp),
            open_tr.animate.set_value(0.90),
            run_time=0.9,
        )

        # Cue 1: "Picture a molecule" -> MAGENTA blob slides into open cup, lips close, 8 GOLD ticks light
        self.at("Picture a molecule")
        drug = RoundedRectangle(
            corner_radius=0.35, width=1.38, height=0.95,
            stroke_color=MAGENTA, stroke_width=4.0, fill_color=MAGENTA, fill_opacity=0.48,
        ).move_to([-3.8, -1.00, 0])
        drug_ticks = make_contact_ticks(cup_center, scale=1.45, count=8, oval=True)
        self.play(FadeIn(drug, shift=RIGHT * 0.2), run_time=0.4)
        self.play(drug.animate.move_to(cup_center), run_time=0.8)
        self.play(open_tr.animate.set_value(0.0), FadeIn(drug_ticks), run_time=0.65)

        # Cue 2: "cannot turn it over" -> YELLOW substrate bumps occupied cup & bounces; strip stream thins to 0
        self.at("cannot turn it over")
        sub = make_key_dot([-4.1, -1.00, 0], radius=0.40, color=YELLOW)
        self.play(FadeIn(sub), run_time=0.3)
        self.play(
            sub.animate.move_to([-2.05, -1.00, 0]),
            strip.flux.animate.set_value(0.0),
            run_time=0.8,
        )
        self.play(sub.animate.move_to([-4.4, -1.75, 0]).set_opacity(0.0), run_time=0.7)

        # Cue 3: "shaped like a transition state" -> MAGENTA blob morphs to stretched-oval silhouette + label
        self.at("shaped like a transition state")
        ts_drug = make_ts_oval(cup_center, scale=1.45, color=MAGENTA)
        drug_lab = T("transition-state-shaped drug", size=30, color=MAGENTA).move_to([0.0, -3.00, 0])
        self.play(Transform(drug, ts_drug), FadeIn(drug_lab, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S11Statin(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=0.0)
        cup_center = np.array([0.0, -1.00, 0.0])
        open_tr = ValueTracker(0.0)
        live_cup = make_live_cup(cup_center, open_tr, scale=1.45, show_knobs=False)
        ts_drug = make_ts_oval(cup_center, scale=1.45, color=MAGENTA)
        drug_ticks = make_contact_ticks(cup_center, scale=1.45, count=8, oval=True)
        c_fit = boxed_label("transition state", PURPLE, size=26, pad=0.16, fill_opacity=0.24).move_to([-4.4, 0.92, 0])
        c_shp = boxed_label("many enzymes: yes", TEAL, size=26, pad=0.16, fill_opacity=0.24).move_to([4.15, 0.92, 0])
        drug_lab = T("transition-state-shaped drug", size=30, color=MAGENTA).move_to([0.0, -3.00, 0])
        self.add(strip, live_cup, ts_drug, drug_ticks, c_fit, c_shp, drug_lab)

        new_c = np.array([0.0, 0.72, 0.0])
        self.play(
            FadeOut(strip), FadeOut(c_fit), FadeOut(c_shp), FadeOut(ts_drug), FadeOut(drug_ticks), FadeOut(drug_lab),
            open_tr.animate.set_value(0.75),
            run_time=0.55,
        )
        cup_static = build_cup_mobject(cup_center, scale=1.45, open_frac=0.75)
        self.remove(live_cup)
        self.add(cup_static)
        cup_target = build_cup_mobject(new_c, scale=1.40, open_frac=0.75)
        enz_lab = T("HMG-CoA reductase", size=30, color=TEAL).move_to([0.0, 2.75, 0])

        # Bottom schematic pathway arrow
        p_start, p_end = np.array([-3.75, -2.35, 0.0]), np.array([3.65, -2.35, 0.0])
        path_arr = Arrow(p_start, p_end, buff=0.0, color=TEXT, stroke_width=4.2, max_tip_length_to_length_ratio=0.04)
        step_ticks = VGroup(*[Line([tx, -2.52, 0], [tx, -2.18, 0], color=GREY, stroke_width=3.5) for tx in (-1.85, 0.0, 1.85)])
        l_hmg = T("HMG-CoA", size=28, color=TEXT).next_to(p_start, LEFT, buff=0.22)
        l_chol = T("cholesterol", size=28, color=TEXT).next_to(p_end, RIGHT, buff=0.22)

        # Live pathway YELLOW dots flowing through the enzyme cup and along the pathway
        p_clock = {"t": 0.0}
        p_flux = ValueTracker(1.0)
        cup_flow = ValueTracker(1.0)
        n_pdots = 7

        def _pdots():
            t = p_clock["t"]
            fl = p_flux.get_value()
            cf = cup_flow.get_value()
            g = VGroup()
            for i in range(n_pdots):
                u = ((i / n_pdots) + t * 0.24 * fl) % 1.0
                pos = p_start + (p_end - p_start) * u + UP * 0.24
                op = min(1.0, u / 0.1) * min(1.0, (1.0 - u) / 0.1)
                g.add(Dot(pos, radius=0.105, color=YELLOW).set_opacity(op))
            # Substrate dots entering and exiting through the open top cleft mouth
            if cf > 0.05:
                for k in range(3):
                    v = ((k / 3.0) + t * 0.44) % 1.0
                    if v < 0.45:
                        s = v / 0.45
                        p = np.array([-2.6 * (1 - s), 1.45 * (1 - s) + 0.72 * s, 0.0])
                    else:
                        s = (v - 0.45) / 0.55
                        p = np.array([2.6 * s, 0.72 * (1 - s) + 1.45 * s, 0.0])
                    op = min(1.0, v / 0.14) * min(1.0, (1.0 - v) / 0.14) * cf
                    g.add(Dot(p, radius=0.14, color=YELLOW).set_opacity(op))
            return g

        pdots = always_redraw(_pdots)
        pdrv = VMobject().add_updater(lambda _, dt: p_clock.__setitem__("t", p_clock["t"] + dt))

        self.play(
            Transform(cup_static, cup_target),
            FadeIn(enz_lab, shift=DOWN * 0.1),
            GrowArrow(path_arr), FadeIn(step_ticks), FadeIn(l_hmg), FadeIn(l_chol),
            run_time=1.0,
        )
        self.add(pdots, pdrv)

        # Cue 1: "Part of each" -> two-part MAGENTA statin appears with 'HMG-like part'
        self.at("Part of each")
        statin = make_statin([-4.0, 0.80, 0], scale=1.08)
        hmg_part_lab = T("HMG-like part", size=28, color=MAGENTA).next_to(statin.head, UP, buff=0.22)
        self.play(cup_flow.animate.set_value(0.0), FadeIn(statin, shift=RIGHT * 0.2), FadeIn(hmg_part_lab), run_time=0.8)

        # Cue 2: "fills its pocket" -> HMG-like end slides into pocket and seats
        self.at("fills its pocket")
        target_shift = (new_c + np.array([0.0, 0.05, 0])) - statin.head.get_center()
        self.play(
            statin.animate.shift(target_shift),
            hmg_part_lab.animate.shift(target_shift + LEFT * 0.25),
            run_time=0.95,
        )
        self.finish()


class S12StatinResult(SpokenScene):
    def construct(self):
        new_c = np.array([0.0, 0.72, 0.0])
        cup = build_cup_mobject(new_c, scale=1.40, open_frac=0.75)
        enz_lab = T("HMG-CoA reductase", size=30, color=TEAL).move_to([0.0, 2.75, 0])

        p_start, p_end = np.array([-3.75, -2.35, 0.0]), np.array([3.65, -2.35, 0.0])
        path_arr = Arrow(p_start, p_end, buff=0.0, color=TEXT, stroke_width=4.2, max_tip_length_to_length_ratio=0.04)
        step_ticks = VGroup(*[Line([tx, -2.52, 0], [tx, -2.18, 0], color=GREY, stroke_width=3.5) for tx in (-1.85, 0.0, 1.85)])
        l_hmg = T("HMG-CoA", size=28, color=TEXT).next_to(p_start, LEFT, buff=0.22)
        l_chol = T("cholesterol", size=28, color=TEXT).next_to(p_end, RIGHT, buff=0.22)

        p_clock = {"t": 0.0}
        p_flux = ValueTracker(1.0)
        p_span = ValueTracker(1.0)

        def _pdots():
            t = p_clock["t"]
            fl = p_flux.get_value()
            sp = p_span.get_value()
            x_a = -3.75 * sp + (-4.35) * (1 - sp)
            x_b = 3.65 * sp + (-1.95) * (1 - sp)
            g = VGroup()
            for i in range(6):
                u = ((i / 6) + t * 0.24 * fl) % 1.0
                pos = np.array([x_a + (x_b - x_a) * u, -2.35 + 0.24, 0.0])
                op = min(1.0, u / 0.1) * min(1.0, (1.0 - u) / 0.1)
                g.add(Dot(pos, radius=0.095, color=YELLOW).set_opacity(op))
            return g

        pdots = always_redraw(_pdots)
        pdrv = VMobject().add_updater(lambda _, dt: p_clock.__setitem__("t", p_clock["t"] + dt))

        statin = make_statin([0.0, 0.77, 0], scale=1.08)
        statin.shift((new_c + np.array([0.0, 0.05, 0])) - statin.head.get_center())
        hmg_part_lab = T("HMG-like part", size=28, color=MAGENTA).next_to(statin.head, UP, buff=0.22).shift(LEFT * 0.25)

        self.add(cup, enz_lab, path_arr, step_ticks, l_hmg, l_chol, pdots, pdrv, statin, hmg_part_lab)

        # Cue 1: "Extra contacts nearby" -> extra GOLD ticks along tail & rim; pulse contacts; incoming substrate approaches
        self.at("Extra contacts nearby")
        extra_ticks = VGroup(
            *[Line([x, 0.42, 0], [x, 0.60, 0], color=GOLD, stroke_width=4.8) for x in (-0.32, 0.0, 0.32, 0.70, 1.06, 1.42)]
        )
        tight_lab = T("far tighter than substrate", size=30, color=MAGENTA).move_to([0.0, -1.28, 0])
        self.play(FadeOut(hmg_part_lab, run_time=0.35), FadeIn(extra_ticks, lag_ratio=0.2, run_time=1.2), FadeIn(tight_lab, shift=UP * 0.1, run_time=0.8))
        for _ in range(2):
            self.play(
                extra_ticks.animate.scale(1.14).set_stroke(width=7.0),
                statin.tail.animate.set_fill(opacity=0.62).set_stroke(width=5.5),
                run_time=0.7,
            )
            self.play(
                extra_ticks.animate.scale(1 / 1.14).set_stroke(width=4.8),
                statin.tail.animate.set_fill(opacity=0.40).set_stroke(width=4.0),
                run_time=0.7,
            )

        self.at("Sitting in the active site")
        sub_bump = make_key_dot([-4.6, 0.77, 0], radius=0.37, color=YELLOW)
        self.play(FadeIn(sub_bump), run_time=0.25)
        self.play(sub_bump.animate.move_to([-2.45, 0.77, 0]), run_time=1.15, rate_func=linear)

        # Cue 2: "keeping the substrate out" -> YELLOW HMG-CoA dot bumps occupied pocket; label -> 'competitive inhibitor'
        self.at("keeping the substrate out")
        comp_lab = T("competitive inhibitor", size=30, color=MAGENTA).move_to([0.0, -1.28, 0])
        self.play(sub_bump.animate.move_to([-1.85, 0.77, 0]), run_time=0.45, rate_func=rush_into)
        self.play(
            sub_bump.animate.move_to([-4.3, -0.05, 0]).set_opacity(0.0),
            swap(tight_lab, comp_lab, run_time=0.65),
        )

        # Cue 3: "Slowing the pathway" -> YELLOW flow slows to a trickle
        self.at("Slowing the pathway")
        self.play(p_flux.animate.set_value(0.18), run_time=0.55)

        # Cue 4: "makes the liver" -> cup slides left; right half gets 'liver cell' outline + RED 'blood' band
        self.at("makes the liver")
        left_c = np.array([-3.3, 0.65, 0.0])
        left_cup = build_cup_mobject(left_c, scale=1.02, open_frac=0.75)
        delta = left_c - new_c
        left_statin = statin.copy().scale(1.02 / 1.40, about_point=new_c).shift(delta)
        left_ticks = extra_ticks.copy().scale(1.02 / 1.40, about_point=new_c).shift(delta)

        p_s2, p_e2 = np.array([-4.35, -2.35, 0.0]), np.array([-1.95, -2.35, 0.0])
        path_arr_2 = Arrow(p_s2, p_e2, buff=0.0, color=TEXT, stroke_width=3.5, max_tip_length_to_length_ratio=0.06)
        step_ticks_2 = VGroup(*[Line([tx, -2.50, 0], [tx, -2.20, 0], color=GREY, stroke_width=3.0) for tx in (-3.55, -3.15, -2.75)])

        liver_bg = RoundedRectangle(
            corner_radius=0.14, width=3.90, height=4.90,
            stroke_opacity=0.0, fill_color=TEXT, fill_opacity=0.06,
        ).move_to([2.30, -0.10, 0])
        cell_pts = [
            [4.25, 0.72, 0], [4.25, 2.35, 0], [0.35, 2.35, 0],
            [0.35, -2.55, 0], [4.25, -2.55, 0], [4.25, -0.72, 0],
        ]
        liver_wall = VMobject(stroke_color=TEXT, stroke_width=3.5, stroke_opacity=0.70, fill_opacity=0.0)
        liver_wall.set_points_as_corners(cell_pts)
        liver_lab = T("liver cell", size=30, color=TEXT).move_to([2.3, 2.75, 0])

        blood_band = RoundedRectangle(
            corner_radius=0.10, width=1.45, height=4.90,
            stroke_color=RED, stroke_width=3.0, fill_color=RED, fill_opacity=0.22,
        ).move_to([5.35, -0.10, 0])
        blood_lab = T("blood", size=28, color=RED).move_to([5.35, 2.75, 0])

        self.play(
            Transform(cup, left_cup),
            Transform(statin, left_statin),
            Transform(extra_ticks, left_ticks),
            enz_lab.animate.move_to([-3.3, 2.55, 0]),
            comp_lab.animate.move_to([-3.3, -1.15, 0]),
            Transform(path_arr, path_arr_2),
            Transform(step_ticks, step_ticks_2),
            l_hmg.animate.next_to(p_s2, LEFT, buff=0.14),
            l_chol.animate.next_to(p_e2, RIGHT, buff=0.14),
            p_span.animate.set_value(0.0),
            FadeIn(liver_bg), FadeIn(liver_wall), FadeIn(liver_lab),
            FadeIn(blood_band), FadeIn(blood_lab),
            run_time=0.80,
        )

        # Cue 5: "pull more LDL" -> WHITE-ringed dots labelled 'LDL' move from blood band into liver cell
        self.at("pull more LDL")
        ldl_clock = {"t": 0.0}
        ldl_speed = ValueTracker(0.32)

        def _ldl_dots():
            t = ldl_clock["t"]
            sp = ldl_speed.get_value()
            g = VGroup()
            ys = [0.35, 0.0, -0.35, 0.22, -0.22]
            for i in range(5):
                u = ((i / 5.0) + t * sp) % 1.0
                x = 5.35 - u * 4.30
                y = ys[i]
                op = min(1.0, u / 0.12) * min(1.0, (1.0 - u) / 0.12)
                ring = Circle(radius=0.14, stroke_color=TEXT, stroke_width=3.2, fill_color=BG, fill_opacity=0.85).move_to([x, y, 0]).set_opacity(op)
                g.add(ring)
            return g

        ldl_stream = always_redraw(_ldl_dots)
        ldl_drv = VMobject().add_updater(lambda _, dt: ldl_clock.__setitem__("t", ldl_clock["t"] + dt))
        ldl_tag = T("LDL", size=28, color=TEXT).move_to([2.3, 1.00, 0])
        ldl_arr = Arrow([4.75, -0.95, 0], [1.95, -0.95, 0], buff=0.0, color=TEXT, stroke_width=3.8, max_tip_length_to_length_ratio=0.10)
        self.add(ldl_stream, ldl_drv)
        self.play(FadeIn(ldl_tag), GrowArrow(ldl_arr), ldl_speed.animate.set_value(0.58), run_time=0.8)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        strip = make_top_strip(flux=1.0, show_ts_peak=False)
        cup_center = np.array([0.0, -1.25, 0.0])
        open_tr = ValueTracker(0.0)
        live_cup = make_live_cup(cup_center, open_tr, scale=1.35, show_knobs=False)
        oval = make_ts_oval(cup_center, scale=1.35)
        ticks = make_contact_ticks(cup_center, scale=1.35, count=8)
        c_fit = boxed_label("transition state", PURPLE, size=28, pad=0.18, fill_opacity=0.24).move_to([-3.8, 0.85, 0])
        c_shp = boxed_label("many enzymes: yes", TEAL, size=28, pad=0.18, fill_opacity=0.24).move_to([3.8, 0.85, 0])

        self.play(
            FadeIn(strip), FadeIn(live_cup), FadeIn(oval), FadeIn(ticks),
            FadeIn(c_fit), FadeIn(c_shp),
            run_time=0.65,
        )

        # Cue 1: "built to fit" -> PURPLE oval glows
        self.at("built to fit")
        self.play(oval.animate.set_fill(opacity=0.78).set_stroke(width=5.8), run_time=0.6)

        # Cue 2: "top of the climb" -> thin PURPLE line rises from oval to top of TEAL pass; TS point glows PURPLE
        self.at("top of the climb")
        conn = Line(oval.get_top() + UP * 0.05, strip.peak_pt, color=PURPLE, stroke_width=3.5)
        self.play(Create(conn), strip.ts_glow.animate.set_opacity(1.0), run_time=0.65)
        self.wait(0.8)

        # Cue 3: "Does it move" -> cup's lips open and close once
        self.at("Does it move")
        self.play(FadeOut(conn), open_tr.animate.set_value(0.85), run_time=0.45)
        self.play(open_tr.animate.set_value(0.0), run_time=0.45)

        # Cue 4: "Locks never do" -> faint ORANGE ghost of rigid lock appears beside cup, still, then fades
        self.at("Locks never do")
        ghost_lock = make_rigid_lock([3.85, -1.25, 0], scale=1.10, opacity=0.45)
        self.play(FadeIn(ghost_lock), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(ghost_lock), run_time=0.45)

        # Cue 5: "Many enzymes do" -> cup closes firmly on oval, dots stream over TEAL pass
        self.at("Many enzymes do")
        self.play(ticks.animate.set_stroke(width=5.8), strip.flux.animate.set_value(1.25), run_time=0.65)
        self.finish()


class S14End(EndCard):
    LINE = "Enzymes fit the transition state best, and many change shape."
