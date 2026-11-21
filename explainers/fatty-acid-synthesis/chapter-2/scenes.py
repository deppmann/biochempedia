"""
Build or Burn (Fatty Acid Synthesis, Chapter 2) — Animation Scenes
=================================================================

COLOUR MAP (one colour per concept for the whole film):
- BLUE   (#58C4DD): ACC enzyme / gate housing (ACC, ACC1, ACC2) and control lever housing
- YELLOW (#F5D547): Malonyl CoA (extender blocks, carboxyl badge, dual-job blocker, malonyl CoA gauge)
- TEAL   (#3FB8C0): Cytoplasm assembly floor, fatty acid synthase (CRDR loop), compartment boundary
- GREEN  (#83C167): Reducing power (NADPH batteries) and ON / activating cues (citrate, insulin, PP2A, "ON", "build")
- RED    (#FC6255): Mitochondrion (burning compartment, inner swirl, CPT-I gate) and OFF / brake cues (AMPK, P tag, palmitoyl CoA, "OFF", "block burning", "paid twice" cost meter)
- GOLD   (#D4A843): Palmitate / carbon chain, ATP coin, and guiding question highlights
- TEXT   (#E8EAF0): Primary labels, counters, titles
- GREY   (#8B93A1): Structural outlines, tracks, schematic tag

ONE PICTURE OF THE WORLD CARRIED THROUGH THE FILM:
Dark schematic cell cross-section split into two compartments:
- Left 55% (cytoplasm assembly floor): ACC gate with ATP coin slot, turning gear crank, and conveyor feeding malonyl extender blocks (with yellow carboxyl badge) into the circular CRDR loop of fatty acid synthase (with two green NADPH batteries at its R stations and a live chain-carbon counter).
- Right 45% (mitochondrion): large rounded double-walled organelle with a rotating inner swirl and a single hinged door (CPT-I gate) facing the cytoplasm floor.
- Zoomed scenes (s03, s04) push into the ACC gate with its ON/OFF lever while keeping the mitochondrion visible inside the right edge; s05–s10 return to the full world where ACC splits into cytoplasmic ACC1 and mitochondrial ACC2.

WHAT CHANGES IN EACH SPOKEN SCENE (and what drives the change):
- s00_link_and_question: ATP coin drops, malonyl block enters CRDR loop, both NADPH batteries drain (1.0 -> 0.15 via ValueTracker), chain counter ticks 14 -> 16 C, mitochondrion swirl brightens & speeds up, finished palmitate bar rolls off loop toward open door.
- s02_futile: Palmitate bar passes through open door and splits into 2-carbon pieces that flicker out while loop builds a replacement; "paid twice" cost meter ticks down in computed steps (1.0 -> 0.30 via ValueTracker); boundary line brightens; world dims leaving ACC glowing.
- s03_switches: Citrate tokens and insulin signal arrow drive ACC lever ValueTracker up (0.35 -> 0.75 -> 1.0), increasing crank angular velocity and malonyl block output computed from lever; palmitoyl CoA feedback token drives lever down (1.0 -> 0.15) and slows crank.
- s04_ampk: AMPK token clips P tag onto ACC, dropping lever ValueTracker to 0.0 (crank stops, blocks halt); PP2A token removes P tag, raising lever to 0.85 (crank and block stream resume).
- s05_second_job: Malonyl blocks split—most enter loop while one wedges into CPT-I door, closing door angle ValueTracker (1.05 -> 0.0 rad) and dimming mitochondrion swirl; palmitate bar bounces off closed door; dual arrows ("build", "block burning") light from one malonyl block.
- s06_predict: Single ACC gate splits into ACC1 (on cytoplasm floor, crank turning & feeding loop) and ACC2 (on mitochondrion outer wall near closed CPT-I door, crank turning slowly); predict question appears above.
- s08_answer: Question dissolves; ACC2 releases malonyl blocks traveling the short path to hold CPT-I shut (while one ACC1 block also drifts over); ACC1 blocks pulse with "building block" tag; door-blocking blocks pulse with "signal" tag.
- s09_fed: Insulin arrow and citrate tokens push ACC1/ACC2 levers to ON (1.0); central malonyl CoA gauge ValueTracker rises (0.25 -> 0.95); CRDR loop speeds up proportionally and palmitate bars stack neatly on floor while CPT-I door stays locked.
- s10_return: Highlighted malonyl CoA block copies itself: one copy slots into CRDR loop and ticks chain counter 14 -> 16 C, second copy locks closed CPT-I door; opening question returns and is answered by "malonyl CoA" sliding beneath it.
"""

from bp_parts import *


# ------------------------------------------------------------------ shared builders
def make_malonyl_block(scale=1.0, badge_color=YELLOW):
    """Rectangular malonyl extender block carrying its yellow carboxyl badge."""
    body = RoundedRectangle(
        corner_radius=0.08 * scale,
        width=0.60 * scale,
        height=0.36 * scale,
        stroke_color=YELLOW,
        stroke_width=2.6,
        fill_color=YELLOW,
        fill_opacity=0.30,
    )
    badge = Dot(radius=0.105 * scale, color=badge_color, stroke_color=TEXT, stroke_width=1.5)
    badge.move_to(body.get_corner(UR) + LEFT * 0.12 * scale + DOWN * 0.10 * scale)
    return VGroup(body, badge)


def make_palmitate_bar(label="palmitate", color=GOLD, font_size=24):
    """Finished C16 palmitate bar sized around its text so letters never overflow."""
    g = boxed_label(label, color=TEXT, size=font_size, pad=0.12, stroke=2.8, fill_opacity=0.28, corner_radius=0.10)
    g.box.set_stroke(color, 2.8)
    g.box.set_fill(color, opacity=0.28)
    return g


def make_token(text, color=GREEN, size=24):
    """Plain labelled regulatory token with opaque dark backing."""
    g = boxed_label(text, color=color, size=size, pad=0.16, stroke=2.5, fill_opacity=0.95, corner_radius=0.14)
    g.box.set_fill(BG, opacity=0.96)
    return g


def make_battery(center, level_tracker, label="NADPH"):
    """Green NADPH battery whose internal charge bar tracks `level_tracker` (0..1)."""
    c = np.array(center, dtype=float)
    w, h = 0.78, 0.42
    shell = RoundedRectangle(
        corner_radius=0.07,
        width=w,
        height=h,
        stroke_color=GREEN,
        stroke_width=2.5,
        fill_color=BG,
        fill_opacity=0.92,
    ).move_to(c)
    nub = Rectangle(
        width=0.08,
        height=0.20,
        stroke_color=GREEN,
        stroke_width=2,
        fill_color=GREEN,
        fill_opacity=0.85,
    ).next_to(shell, RIGHT, buff=0.0)

    def mk_fill():
        lvl = float(np.clip(level_tracker.get_value(), 0.03, 1.0))
        fw = (w - 0.12) * lvl
        r = Rectangle(
            width=fw,
            height=h - 0.12,
            stroke_width=0,
            fill_color=GREEN,
            fill_opacity=0.82,
        )
        r.move_to([shell.get_left()[0] + 0.06 + fw / 2, c[1], 0])
        return r

    fill = always_redraw(mk_fill)
    lbl = T(label, size=24, color=GREEN).next_to(shell, UP, buff=0.12)
    g = VGroup(shell, nub, fill, lbl)
    g.shell, g.lbl = shell, lbl
    return g


def make_acc_gate(
    center=(-4.95, -0.15, 0),
    size=(1.48, 2.20),
    label="ACC",
    crank_speed_fn=None,
    lever_tracker=None,
    show_slot=True,
    show_lever_marks=False,
    label_pos=UP,
):
    """ACC enzyme gate with housing, ATP slot, 4-spoke turning crank, and optional ON/OFF lever."""
    c = np.array(center, dtype=float)
    w, h = size
    housing = RoundedRectangle(
        corner_radius=0.18,
        width=w,
        height=h,
        stroke_color=BLUE,
        stroke_width=3.5,
        fill_color=BLUE,
        fill_opacity=0.18,
    ).move_to(c)

    parts = [housing]
    if show_slot:
        slot = RoundedRectangle(
            corner_radius=0.04,
            width=w * 0.42,
            height=0.12,
            stroke_color=GOLD,
            stroke_width=2.2,
            fill_color=BG,
            fill_opacity=0.95,
        ).move_to(c + UP * (h * 0.34))
        parts.append(slot)
    else:
        slot = None

    crank_c = c + DOWN * (h * 0.12)
    hub_r = min(w, h) * 0.27
    hub = Circle(
        radius=hub_r,
        stroke_color=BLUE,
        stroke_width=3.0,
        fill_color=BG,
        fill_opacity=0.88,
    ).move_to(crank_c)
    spoke_len = hub_r * 0.88
    angle_tr = ValueTracker(0.0)

    def mk_crank():
        a = angle_tr.get_value()
        cc = hub.get_center()
        r_now = max(hub.width / 2.0 * 0.88, 0.08)
        grp = VGroup()
        for k in range(4):
            ang = a + k * PI / 2
            tip = cc + np.array([np.cos(ang), np.sin(ang), 0.0]) * r_now
            col = YELLOW if k == 0 else BLUE
            sw = 4.5 if k == 0 else 2.5
            grp.add(Line(cc, tip, color=col, stroke_width=sw))
        tip0 = cc + np.array([np.cos(a), np.sin(a), 0.0]) * r_now
        grp.add(Dot(tip0, radius=0.075, color=YELLOW))
        grp.add(Dot(cc, radius=0.055, color=TEXT))
        return grp

    crank_arm = always_redraw(mk_crank)
    if crank_speed_fn is not None:
        hub.add_updater(lambda mob, dt: angle_tr.increment_value(dt * crank_speed_fn()))

    parts.extend([hub, crank_arm])

    lever_grp = VGroup()
    if lever_tracker is not None:
        lx = c[0] + w * 0.5 + 0.54
        track_h = h * 0.62
        track = Line([lx, c[1] - track_h / 2, 0], [lx, c[1] + track_h / 2, 0], color=GREY, stroke_width=5)
        pivot = np.array([c[0] + w * 0.48, c[1], 0.0])

        def mk_lever():
            v = float(np.clip(lever_tracker.get_value(), 0.0, 1.0))
            knob_y = (c[1] - track_h / 2) + v * track_h
            knob_pos = np.array([lx, knob_y, 0.0])
            col = GREEN if v >= 0.55 else (RED if v <= 0.35 else YELLOW)
            rod = Line(pivot, knob_pos, color=col, stroke_width=5.5)
            tab = Line(knob_pos, knob_pos + RIGHT * 0.45, color=col, stroke_width=4.5)
            knob = Dot(knob_pos, radius=0.13, color=col, stroke_color=TEXT, stroke_width=2.0)
            return VGroup(rod, tab, knob)

        lever_arm = always_redraw(mk_lever)
        lever_grp.add(track, lever_arm)
        if show_lever_marks:
            on_lbl = T("ON", size=26, color=GREEN, weight=BOLD).move_to([lx, c[1] + track_h / 2 + 0.34, 0])
            off_lbl = T("OFF", size=26, color=RED, weight=BOLD).move_to([lx, c[1] - track_h / 2 - 0.34, 0])
            lever_grp.add(on_lbl, off_lbl)
        parts.append(lever_grp)

    lbl = T(label, size=28, color=BLUE, weight=BOLD).next_to(housing, label_pos, buff=0.16)
    parts.append(lbl)

    g = VGroup(*parts)
    g.housing = housing
    g.slot = slot
    g.hub = hub
    g.angle_tr = angle_tr
    g.lever_grp = lever_grp
    g.lbl = lbl
    return g


def make_crdr_loop(center=(-1.75, -0.05, 0), radius=1.12, speed_fn=None):
    """Circular CRDR synthase wheel with 8 rotating conveyor paddles and clear exterior station letters."""
    c = np.array(center, dtype=float)
    ring = Circle(
        radius=radius,
        stroke_color=TEAL,
        stroke_width=7,
        fill_color=TEAL,
        fill_opacity=0.12,
    ).move_to(c)

    rot_tr = ValueTracker(0.0)

    def mk_wheel():
        a0 = rot_tr.get_value()
        pts = VGroup()
        # 8 rotating conveyor segments & directional paddles so motion reads at any resolution
        for k in range(8):
            ang = a0 + k * TAU / 8
            p_in = c + np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius - 0.14)
            p_out = c + np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.12)
            pts.add(Line(p_in, p_out, color=TEAL if k % 2 == 0 else GOLD, stroke_width=5.0))
        for k in range(4):
            ang = a0 + k * TAU / 4 + PI / 8
            p = c + np.array([np.cos(ang), np.sin(ang), 0.0]) * radius
            tangent = np.array([-np.sin(ang), np.cos(ang), 0.0])
            tri = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=0.95, stroke_width=0).scale(0.12)
            tri.rotate(np.arctan2(tangent[1], tangent[0]) - PI / 2)
            tri.move_to(p)
            pts.add(tri)
        return pts

    markers = always_redraw(mk_wheel)
    if speed_fn is not None:
        ring.add_updater(lambda m, dt: rot_tr.increment_value(dt * speed_fn()))

    # Station letters placed cleanly OUTSIDE the ring paddles (no ring stroke crossing letters/boxes)
    stations = VGroup()
    station_specs = (
        ("C", PI / 2, 0.34),
        ("R", PI * 0.22, 0.34),
        ("D", -PI / 2, 0.34),
        ("R", PI * 0.78, 0.34),
    )
    for ch, ang, off in station_specs:
        pos = c + np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + off)
        stations.add(T(ch, size=24, color=TEAL, weight=BOLD).move_to(pos))

    title = T("CRDR", size=28, color=TEAL, weight=BOLD).move_to(c + UP * 0.18)
    sub = T("synthase", size=24, color=TEXT).move_to(c + DOWN * 0.20)

    g = VGroup(ring, markers, stations, title, sub)
    g.ring = ring
    g.rot_tr = rot_tr
    g.title = title
    g.sub = sub
    g.stations = stations
    return g


def make_mitochondrion(
    center=(3.95, -0.05, 0),
    width=4.20,
    height=3.70,
    door_angle_tr=None,
    swirl_speed_fn=None,
    swirl_opacity_tr=None,
    door_label=None,
    wall_opacity_tr=None,
):
    """Large rounded mitochondrion with rotating inner swirl and wide hinged outer-wall door."""
    c = np.array(center, dtype=float)
    x0 = c[0] - width / 2
    cr = min(0.75, width * 0.42, height * 0.35)
    l, r = c[0] - width / 2, c[0] + width / 2
    b, t = c[1] - height / 2, c[1] + height / 2

    door_cy = c[1] - 0.35
    door_h = 1.12
    door_top = min(door_cy + door_h / 2, t - cr - 0.02)
    door_bot = max(door_cy - door_h / 2, b + cr + 0.02)
    door_h = door_top - door_bot
    door_cy = (door_top + door_bot) / 2

    wall_pts = [
        [l, door_top, 0],
        [l, t - cr, 0],
    ]
    for a in np.linspace(PI, PI / 2, 12)[1:]:
        wall_pts.append([l + cr + cr * np.cos(a), t - cr + cr * np.sin(a), 0])
    wall_pts.append([r - cr, t, 0])
    for a in np.linspace(PI / 2, 0, 12)[1:]:
        wall_pts.append([r - cr + cr * np.cos(a), t - cr + cr * np.sin(a), 0])
    wall_pts.append([r, b + cr, 0])
    for a in np.linspace(0, -PI / 2, 12)[1:]:
        wall_pts.append([r - cr + cr * np.cos(a), b + cr + cr * np.sin(a), 0])
    wall_pts.append([l + cr, b, 0])
    for a in np.linspace(-PI / 2, -PI, 12)[1:]:
        wall_pts.append([l + cr + cr * np.cos(a), b + cr + cr * np.sin(a), 0])
    wall_pts.append([l, door_bot, 0])

    bg_fill = RoundedRectangle(
        corner_radius=cr,
        width=width,
        height=height,
        stroke_width=0,
        fill_color=RED,
        fill_opacity=0.10,
    ).move_to(c)

    outer_wall = VMobject(stroke_color=RED, stroke_width=4.5, fill_opacity=0)
    outer_wall.set_points_as_corners([np.array(p) for p in wall_pts])

    inner_ring = RoundedRectangle(
        corner_radius=cr * 0.72,
        width=width * 0.76,
        height=height * 0.72,
        stroke_color=RED,
        stroke_width=2.2,
        stroke_opacity=0.40,
        fill_color=RED,
        fill_opacity=0.05,
    ).move_to(c + RIGHT * 0.12)

    swirl_tr = ValueTracker(0.0)
    swirl_op = swirl_opacity_tr if swirl_opacity_tr is not None else ValueTracker(0.55)
    swirl_c = c + RIGHT * 0.14
    swirl_rx = width * 0.31
    swirl_ry = height * 0.30

    def mk_swirl():
        a0 = swirl_tr.get_value()
        op = float(np.clip(swirl_op.get_value(), 0.15, 1.0))
        arms = VGroup()
        for k in range(3):
            theta = np.linspace(0.20, 2.3 * PI, 34)
            frac = (0.15 + 0.155 * theta) / (0.15 + 0.155 * 2.3 * PI)
            xs = swirl_c[0] + swirl_rx * frac * np.cos(theta + a0 + k * TAU / 3)
            ys = swirl_c[1] + swirl_ry * frac * np.sin(theta + a0 + k * TAU / 3)
            pts = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
            m = VMobject(stroke_color=RED, stroke_width=4.2, stroke_opacity=op, fill_opacity=0)
            m.set_points_as_corners(pts)
            arms.add(m)
            # Tip bead moving on each swirl arm makes inner oxidation rotation unambiguous
            arms.add(Dot(pts[-1], radius=0.07, color=GOLD if op > 0.6 else RED).set_opacity(op))
        return arms

    swirl = always_redraw(mk_swirl)
    if swirl_speed_fn is not None:
        inner_ring.add_updater(lambda m, dt: swirl_tr.increment_value(dt * swirl_speed_fn()))

    d_tr = door_angle_tr if door_angle_tr is not None else ValueTracker(1.08)
    hinge = np.array([x0, door_top, 0.0])

    def mk_door():
        ang = d_tr.get_value()
        p1 = hinge + np.array([np.sin(ang) * door_h, -np.cos(ang) * door_h, 0.0])
        leaf = Line(hinge, p1, color=GOLD if ang > 0.25 else RED, stroke_width=7.5)
        hinge_dot = Dot(hinge, radius=0.075, color=TEXT)
        return VGroup(leaf, hinge_dot)

    door = always_redraw(mk_door)
    mito_lbl = T("mitochondrion", size=26, color=RED).move_to([c[0], c[1] - height / 2 - 0.42, 0])

    parts = [bg_fill, inner_ring, outer_wall, swirl, door, mito_lbl]
    dlbl = None
    if door_label:
        dlbl = T(door_label, size=24, color=RED, weight=BOLD).move_to([x0 - 0.85, door_bot - 0.50, 0])
        parts.append(dlbl)

    g = VGroup(*parts)
    g.bg_fill = bg_fill
    g.outer_wall = outer_wall
    g.inner_ring = inner_ring
    g.swirl = swirl
    g.swirl_tr = swirl_tr
    g.swirl_op = swirl_op
    g.door = door
    g.door_angle_tr = d_tr
    g.hinge = hinge
    g.door_center = np.array([x0, door_cy, 0.0])
    g.mito_lbl = mito_lbl
    g.door_lbl = dlbl
    g.center_pt = c
    return g


def make_floor(x0=-6.10, x1=0.75, y=-2.45):
    """Cytoplasm floor line and label."""
    bar = Rectangle(
        width=x1 - x0,
        height=0.14,
        stroke_width=0,
        fill_color=TEAL,
        fill_opacity=0.25,
    ).move_to([(x0 + x1) / 2, y - 0.07, 0])
    line = Line([x0, y, 0], [x1, y, 0], color=TEAL, stroke_width=3.5)
    lbl = T("cytoplasm", size=26, color=TEAL).move_to([-4.6, y - 0.42, 0])
    return VGroup(bar, line, lbl)


def make_track(x0=-4.21, x1=-2.90, y=-0.62):
    """Conveyor track between ACC and CRDR loop."""
    return DashedLine([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=3.0, dash_length=0.16)


def make_chain_counter(tracker, at=(-1.75, 2.05, 0)):
    """Chain carbon counter synced to `tracker`."""
    return counter("chain: {:.0f} C", tracker, at=at, size=28, color=GOLD)


def add_conveyor_stream(scene, x0=-4.05, x1=-2.95, y=-0.62, speed_fn=lambda: 1.0, active_fn=lambda: True):
    """Continuous malonyl blocks rolling along the ACC -> CRDR conveyor whenever ACC is active."""
    phase = ValueTracker(0.0)
    driver = Dot(radius=0.001).set_opacity(0)
    driver.add_updater(lambda m, dt: phase.increment_value(dt * speed_fn()))
    scene.add(driver)

    def mk_stream():
        if not active_fn():
            return VGroup()
        p = phase.get_value() % 1.0
        bx = x0 + p * (x1 - x0)
        blk = make_malonyl_block(scale=0.82).move_to([bx, y, 0])
        return blk

    stream = always_redraw(mk_stream)
    scene.add(stream)
    return stream, driver


def build_full_world(
    acc_crank_speed=lambda: 1.8,
    loop_speed=lambda: 1.0,
    swirl_speed=lambda: 0.9,
    swirl_op=0.45,
    door_angle=1.08,
    bat1_lvl=1.0,
    bat2_lvl=1.0,
    show_batteries=True,
    door_label=None,
    acc_lever=None,
    split_acc=False,
    acc2_crank_speed=lambda: 0.9,
    acc2_lever=None,
):
    """Assemble the carried world consistently across scenes."""
    floor = make_floor()
    track = make_track()
    loop = make_crdr_loop(center=(-1.75, -0.05, 0), radius=1.12, speed_fn=loop_speed)

    door_tr = ValueTracker(door_angle)
    swirl_op_tr = ValueTracker(swirl_op)
    mito = make_mitochondrion(
        center=(3.95, -0.05, 0),
        width=4.20,
        height=3.70,
        door_angle_tr=door_tr,
        swirl_speed_fn=swirl_speed,
        swirl_opacity_tr=swirl_op_tr,
        door_label=door_label,
    )

    acc1_lbl = "ACC1" if split_acc else "ACC"
    acc1 = make_acc_gate(
        center=(-4.95, -0.15, 0),
        size=(1.48, 2.20),
        label=acc1_lbl,
        crank_speed_fn=acc_crank_speed,
        lever_tracker=acc_lever,
        show_slot=True,
        show_lever_marks=False,
        label_pos=UP,
    )

    parts = [floor, track, acc1, loop, mito]
    bat1 = bat2 = None
    b1_tr = ValueTracker(bat1_lvl)
    b2_tr = ValueTracker(bat2_lvl)
    if show_batteries:
        bat2 = make_battery((-3.68, 1.02, 0), b2_tr, "NADPH")
        bat1 = make_battery((0.25, 1.02, 0), b1_tr, "NADPH")
        parts.extend([bat2, bat1])

    acc2 = None
    if split_acc:
        acc2 = make_acc_gate(
            center=(2.48, 1.55, 0),
            size=(1.12, 1.28),
            label="ACC2",
            crank_speed_fn=acc2_crank_speed,
            lever_tracker=acc2_lever,
            show_slot=False,
            show_lever_marks=False,
            label_pos=UP,
        )
        parts.append(acc2)

    tag = scope_tag("schematic")
    parts.append(tag)

    w = VGroup(*parts)
    w.floor = floor
    w.track = track
    w.acc1 = acc1
    w.acc2 = acc2
    w.loop = loop
    w.mito = mito
    w.bat1, w.bat2 = bat1, bat2
    w.b1_tr, w.b2_tr = b1_tr, b2_tr
    w.tag = tag
    return w


# ------------------------------------------------------------------ Scene 00
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        crank_spd = ValueTracker(1.8)
        loop_spd = ValueTracker(1.1)
        swirl_spd = ValueTracker(0.75)

        w = build_full_world(
            acc_crank_speed=lambda: crank_spd.get_value(),
            loop_speed=lambda: loop_spd.get_value(),
            swirl_speed=lambda: swirl_spd.get_value(),
            swirl_op=0.45,
            door_angle=1.08,
            bat1_lvl=1.0,
            bat2_lvl=1.0,
            show_batteries=True,
            door_label=None,
        )
        chain_tr = ValueTracker(14.0)
        chain_cnt = make_chain_counter(chain_tr, at=(-1.75, 2.08, 0))
        block = make_malonyl_block().move_to([-4.05, -0.62, 0])
        atp_p0 = np.array([-5.85, 1.75, 0.0])
        atp_p1 = np.array([-5.95, 0.65, 0.0])
        atp_p2 = w.acc1.slot.get_center().copy()
        atp_coin = make_token("ATP", color=GOLD, size=24).move_to(atp_p0)

        self.add(w, chain_cnt, block)

        # Beat 1: palmitate two carbons at a time — malonyl block enters loop edge
        self.at("builds palmitate")
        self.play(block.animate.move_to([-2.95, -0.62, 0]), run_time=0.8)

        self.at("two carbons at a time")
        self.play(
            block.animate.move_to(w.loop.ring.get_left() + RIGHT * 0.25).scale(0.6).set_opacity(0.0),
            loop_spd.animate.set_value(1.9),
            run_time=0.9,
        )
        self.remove(block)

        # Beat 2: Each turn costs one ATP and two NADPH
        self.at("Each turn costs")
        self.play(FadeIn(atp_coin, shift=DOWN * 0.15), run_time=0.4)

        self.at("one ATP")
        atp_proto = atp_coin.copy()

        def move_atp(mob, alpha):
            pos = ((1 - alpha) ** 2) * atp_p0 + 2 * (1 - alpha) * alpha * atp_p1 + (alpha ** 2) * atp_p2
            m = atp_proto.copy().scale(1.0 - 0.45 * alpha).move_to(pos)
            if alpha >= 0.55:
                m.set_opacity(max(0.0, 1.0 - (alpha - 0.55) / 0.45))
            mob.become(m)

        self.play(UpdateFromAlphaFunc(atp_coin, move_atp), run_time=0.8)
        self.remove(atp_coin)

        self.at("two NADPH")
        self.play(
            w.b1_tr.animate.set_value(0.15),
            w.b2_tr.animate.set_value(0.15),
            chain_tr.animate.set_value(16.0),
            run_time=1.3,
        )
        loop_spd.set_value(1.1)

        # Beat 3: mitochondria that burn fat — inner swirl brightens & speeds up
        self.at("mitochondria that burn fat")
        self.play(
            w.mito.swirl_op.animate.set_value(0.98),
            swirl_spd.animate.set_value(1.8),
            run_time=1.0,
        )

        # Beat 4: question + palmitate bar rolls off loop toward open door (stays clear of loop & door)
        self.at("So what stops new fat")
        palm = make_palmitate_bar().move_to([0.20, -1.65, 0])
        q_txt = T("What keeps new fat unburned?", size=38, color=GOLD, weight=BOLD).move_to([0.0, 3.05, 0])
        self.play(FadeIn(palm, scale=0.85), FadeIn(q_txt, shift=DOWN * 0.12), run_time=0.6)
        self.play(palm.animate.move_to([0.48, -0.45, 0]), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ Scene 01
class S01Title(NarratedScene):
    def construct(self):
        w = build_full_world(
            acc_crank_speed=lambda: 1.8,
            loop_speed=lambda: 1.1,
            swirl_speed=lambda: 1.8,
            swirl_op=0.98,
            door_angle=1.08,
            bat1_lvl=0.15,
            bat2_lvl=0.15,
            show_batteries=True,
        )
        chain_tr = ValueTracker(16.0)
        chain_cnt = make_chain_counter(chain_tr, at=(-1.75, 2.08, 0))
        palm = make_palmitate_bar().move_to([0.48, -0.45, 0])
        q_txt = T("What keeps new fat unburned?", size=38, color=GOLD, weight=BOLD).move_to([0.0, 3.05, 0])
        title = T("Build or Burn", size=52, color=TEXT, font=TITLE_FONT, weight=BOLD).move_to([0.0, 3.02, 0])

        self.add(w, chain_cnt, palm, q_txt)
        self.play(swap(q_txt, title, run_time=0.75))
        self.play(palm.animate.shift(UP * 0.10), rate_func=there_and_back, run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ Scene 02
class S02Futile(SpokenScene):
    def construct(self):
        w = build_full_world(
            acc_crank_speed=lambda: 1.9,
            loop_speed=lambda: 1.3,
            swirl_speed=lambda: 1.8,
            swirl_op=0.95,
            door_angle=1.08,
            bat1_lvl=0.18,
            bat2_lvl=0.18,
            show_batteries=True,
        )
        palm = make_palmitate_bar().move_to([0.48, -0.45, 0])
        title = T("Build or Burn", size=52, color=TEXT, font=TITLE_FONT, weight=BOLD).move_to([0.0, 3.02, 0])

        # Horizontal cost meter labelled 'paid twice' centered high at top, clear of NADPH and boundary
        cost_lvl = ValueTracker(1.0)
        meter_bg = RoundedRectangle(
            corner_radius=0.08,
            width=2.50,
            height=0.34,
            stroke_color=RED,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to([0.25, 2.65, 0])

        def mk_meter_fill():
            v = float(np.clip(cost_lvl.get_value(), 0.05, 1.0))
            fw = 2.34 * v
            r = Rectangle(width=fw, height=0.22, stroke_width=0, fill_color=RED, fill_opacity=0.85)
            r.move_to([meter_bg.get_left()[0] + 0.08 + fw / 2, 2.65, 0])
            return r

        meter_fill = always_redraw(mk_meter_fill)
        meter_lbl = T("paid twice", size=24, color=RED, weight=BOLD).next_to(meter_bg, UP, buff=0.12)
        meter = VGroup(meter_bg, meter_fill, meter_lbl)

        # Boundary line between cytoplasm and mitochondrion
        boundary = DashedLine([1.42, -2.35, 0], [1.42, 2.15, 0], color=TEAL, stroke_width=3.5, dash_length=0.18)
        boundary.set_opacity(0.18)

        self.add(w, palm, title, boundary)
        self.play(FadeOut(title, run_time=0.45), FadeIn(meter, run_time=0.45))

        # Beat 1: build a chain, then tear it down, paying for both
        self.at("build a chain")
        palm2 = make_palmitate_bar().move_to([0.48, -1.78, 0])
        self.play(palm.animate.move_to([0.85, -0.45, 0]), FadeIn(palm2), run_time=0.45)

        self.at("then tear it down")
        pieces = VGroup(*[
            RoundedRectangle(
                corner_radius=0.05,
                width=0.22,
                height=0.34,
                stroke_color=GOLD,
                stroke_width=2,
                fill_color=GOLD,
                fill_opacity=0.75,
            )
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.06).move_to([1.65, -0.45, 0])
        self.remove(palm)
        self.add(pieces)
        self.play(
            pieces.animate.arrange(RIGHT, buff=0.26).move_to([3.95, -0.45, 0]),
            palm2.animate.move_to([0.48, -0.45, 0]),
            cost_lvl.animate.set_value(0.62),
            run_time=0.55,
        )
        self.play(FadeOut(pieces, shift=UP * 0.18), run_time=0.20)

        self.at("paying for both")
        pieces2 = VGroup(*[
            RoundedRectangle(
                corner_radius=0.05,
                width=0.22,
                height=0.34,
                stroke_color=GOLD,
                stroke_width=2,
                fill_color=GOLD,
                fill_opacity=0.75,
            )
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.06).move_to([1.65, -0.45, 0])
        self.play(palm2.animate.move_to([0.85, -0.45, 0]), run_time=0.35)
        self.remove(palm2)
        self.add(pieces2)
        self.play(
            pieces2.animate.arrange(RIGHT, buff=0.26).move_to([3.95, -0.45, 0]),
            cost_lvl.animate.set_value(0.28),
            run_time=0.50,
        )
        self.play(FadeOut(pieces2, scale=0.6), run_time=0.20)

        # Beat 2: separate places, carriers and electron pools
        self.at("separate places")
        self.play(boundary.animate.set_opacity(1.0), run_time=0.30)

        self.at("carriers")
        self.play(Indicate(w.loop.stations, color=TEAL, scale_factor=1.12), run_time=0.60)

        self.at("electron pools")
        self.play(
            Indicate(w.bat1.shell, color=GREEN, scale_factor=1.12),
            Indicate(w.bat2.shell, color=GREEN, scale_factor=1.12),
            run_time=0.70,
        )

        # Beat 3: one main control point -> dim strokes & fills cleanly except ACC gate
        self.at("one main control point")
        acc_glow = SurroundingRectangle(w.acc1.housing, corner_radius=0.22, color=GOLD, stroke_width=4.5, buff=0.04)
        self.play(
            w.floor.animate.set_opacity(0.22),
            w.track.animate.set_opacity(0.22),
            w.loop.animate.set_opacity(0.22),
            w.mito.outer_wall.animate.set_stroke(opacity=0.22),
            w.mito.inner_ring.animate.set_stroke(opacity=0.12),
            w.mito.bg_fill.animate.set_fill(opacity=0.03),
            w.mito.mito_lbl.animate.set_opacity(0.25),
            w.mito.swirl_op.animate.set_value(0.16),
            w.bat1.animate.set_opacity(0.22),
            w.bat2.animate.set_opacity(0.22),
            meter.animate.set_opacity(0.22),
            boundary.animate.set_opacity(0.22),
            Create(acc_glow),
            run_time=0.85,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 03
class S03Switches(SpokenScene):
    def _build_zoomed_stage(self, lever_init=0.35):
        lever_tr = ValueTracker(lever_init)
        crank_spd = lambda: 0.25 + 2.8 * float(np.clip(lever_tr.get_value(), 0.0, 1.0))

        floor = make_floor(x0=-6.10, x1=3.20, y=-2.50)
        acc = make_acc_gate(
            center=(-2.95, -0.05, 0),
            size=(2.15, 3.40),
            label="ACC",
            crank_speed_fn=crank_spd,
            lever_tracker=lever_tr,
            show_slot=True,
            show_lever_marks=True,
            label_pos=UP,
        )
        # CRDR loop and mitochondrion kept inside safe frame on right
        loop = make_crdr_loop(center=(2.55, -0.05, 0), radius=0.95, speed_fn=lambda: 0.6 + 1.2 * lever_tr.get_value())
        track = DashedLine([-1.05, -0.85, 0], [1.55, -0.85, 0], color=GREY, stroke_width=3, dash_length=0.16)
        mito = make_mitochondrion(
            center=(5.25, -0.05, 0),
            width=2.15,
            height=3.40,
            door_angle_tr=ValueTracker(1.05),
            swirl_speed_fn=lambda: 0.7,
            swirl_opacity_tr=ValueTracker(0.45),
        )
        mito.mito_lbl.move_to([5.20, -2.18, 0])
        tag = scope_tag("schematic")

        return VGroup(floor, track, acc, loop, mito, tag), lever_tr, acc, loop, mito

    def construct(self):
        stage, lever_tr, acc, loop, mito = self._build_zoomed_stage(0.35)
        self.add(stage)

        # Beat 1: That point is ACC, makes malonyl CoA
        self.at("That point is")
        self.play(Indicate(acc.housing, color=BLUE, scale_factor=1.04), run_time=0.65)

        self.at("makes malonyl")
        m0 = make_malonyl_block().move_to([-0.85, -0.85, 0])
        self.play(FadeIn(m0), m0.animate.move_to([1.40, -0.85, 0]), run_time=0.9)
        self.play(FadeOut(m0), run_time=0.25)

        # Beat 2: Citrate tokens push against right tip of lever (x = +0.25), clear of ON/OFF and CRDR
        self.at("Citrate")
        cit1 = make_token("citrate", color=GREEN).move_to([0.25, -1.95, 0])
        cit2 = make_token("citrate", color=GREEN).move_to([1.65, -1.95, 0])
        self.play(FadeIn(cit1, shift=UP * 0.2), FadeIn(cit2, shift=UP * 0.2), run_time=0.55)

        self.at("switches it on")
        m1 = make_malonyl_block().move_to([-0.85, -0.85, 0])
        self.play(
            cit1.animate.move_to([0.25, -0.15, 0]),
            cit2.animate.move_to([0.25, -0.80, 0]),
            lever_tr.animate.set_value(0.75),
            FadeIn(m1),
            m1.animate.move_to([1.40, -0.85, 0]),
            run_time=1.0,
        )
        self.remove(m1)

        # Beat 3: Insulin signal arrow reaches in from frame edge -> pushes lever further up
        self.at("So does insulin")
        edge_line = DashedLine([-6.02, -2.50, 0], [-6.02, 2.50, 0], color=GREY, stroke_width=2.5)
        ins_arrow = Arrow([-6.25, 1.45, 0], [-4.20, 1.00, 0], color=GREEN, stroke_width=5, buff=0)
        ins_lbl = T("insulin signal", size=24, color=GREEN, weight=BOLD).move_to([-4.60, 2.02, 0])
        self.play(Create(edge_line), GrowArrow(ins_arrow), FadeIn(ins_lbl), run_time=0.55)
        self.play(lever_tr.animate.set_value(1.0), run_time=0.6)

        # Beat 4: Palmitoyl CoA curls back from loop to clear gap at x = +0.25 and presses down
        self.at("Palmitoyl")
        palm_tok = make_token("palmitoyl CoA", color=RED, size=24).move_to([2.65, 2.05, 0])
        arc_path = ArcBetweenPoints([2.65, 1.95, 0], [0.25, 1.45, 0], angle=0.5)
        self.play(FadeIn(palm_tok, scale=0.8), run_time=0.4)
        self.play(MoveAlongPath(palm_tok, arc_path), run_time=0.95)

        self.at("switches it off")
        self.play(
            palm_tok.animate.move_to([0.0, 0.25, 0]),
            cit1.animate.move_to([0.25, -1.35, 0]).set_opacity(0.35),
            cit2.animate.move_to([0.25, -1.95, 0]).set_opacity(0.35),
            lever_tr.animate.set_value(0.15),
            run_time=1.0,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 04
class S04Ampk(SpokenScene):
    def construct(self):
        stage, lever_tr, acc, loop, mito = S03Switches._build_zoomed_stage(0.75)

        cit_icon = Dot(radius=0.14, color=GREEN, stroke_color=TEXT, stroke_width=1.5).move_to([-4.25, -0.95, 0])
        ins_icon = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=0.85, stroke_width=0).scale(0.16).rotate(-PI / 2).move_to([-4.25, 0.85, 0])
        self.add(stage, cit_icon, ins_icon)

        p_circle = Circle(radius=0.26, stroke_color=RED, stroke_width=3, fill_color=BG, fill_opacity=0.95)
        p_txt = T("P", size=26, color=RED, weight=BOLD).move_to(p_circle)
        p_tag = VGroup(p_circle, p_txt)

        # Beat 1: AMPK enters carrying P tag
        self.at("the cell's low")
        ampk = make_token("AMPK", color=RED, size=26).move_to([-5.35, 1.75, 0])
        p_tag.next_to(ampk, RIGHT, buff=0.16)
        self.play(FadeIn(ampk, shift=RIGHT * 0.2), FadeIn(p_tag, shift=RIGHT * 0.2), run_time=0.55)

        # Beat 2: attaches phosphate on ACC, drops lever to OFF
        self.at("also switches")
        self.play(
            ampk.animate.move_to([-5.05, 0.25, 0]),
            p_tag.animate.move_to([-3.55, 0.25, 0]),
            run_time=0.75,
        )

        self.at("attaching a phosphate")
        self.play(
            p_tag.animate.move_to([-2.95, 0.72, 0]),
            lever_tr.animate.set_value(0.0),
            FadeOut(ampk, shift=LEFT * 0.3),
            run_time=0.85,
        )

        # Beat 3: PP2A enters left of ACC (clear of housing border), unclips P tag
        self.at("Another enzyme")
        pp2a = make_token("PP2A", color=GREEN, size=26).move_to([-5.35, -1.65, 0])
        self.play(FadeIn(pp2a, shift=RIGHT * 0.2), run_time=0.5)

        self.at("PP2A")
        self.play(pp2a.animate.move_to([-5.15, 0.35, 0]), run_time=0.7)

        self.at("removes the phosphate")
        self.play(
            pp2a.animate.move_to([-5.35, 1.75, 0]),
            p_tag.animate.move_to([-4.45, 1.75, 0]),
            run_time=0.8,
        )

        self.at("turns it back on")
        m_out = make_malonyl_block().move_to([-0.85, -0.85, 0])
        self.play(
            FadeOut(pp2a),
            FadeOut(p_tag),
            lever_tr.animate.set_value(0.85),
            FadeIn(m_out),
            m_out.animate.move_to([1.40, -0.85, 0]),
            run_time=0.9,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 05
class S05SecondJob(SpokenScene):
    def construct(self):
        crank_spd = ValueTracker(1.8)
        loop_spd = ValueTracker(1.2)
        swirl_spd = ValueTracker(1.4)

        w = build_full_world(
            acc_crank_speed=lambda: crank_spd.get_value(),
            loop_speed=lambda: loop_spd.get_value(),
            swirl_speed=lambda: swirl_spd.get_value(),
            swirl_op=0.85,
            door_angle=1.08,
            bat1_lvl=0.85,
            bat2_lvl=0.85,
            show_batteries=True,
            door_label="CPT-I gate",
        )
        w.mito.door_lbl.set_opacity(0)
        self.add(w)

        # Beat 1: malonyl CoA has a second job — blocks split: most into loop, one right toward door
        self.at("malonyl")
        m_loop1 = make_malonyl_block().move_to([-4.05, -0.62, 0])
        m_loop2 = make_malonyl_block().move_to([-4.05, -0.62, 0])
        m_door = make_malonyl_block().move_to([-4.05, -0.62, 0])
        self.play(FadeIn(m_loop1), m_loop1.animate.move_to([-2.90, -0.62, 0]), run_time=0.7)
        self.play(FadeOut(m_loop1), FadeIn(m_loop2), FadeIn(m_door), run_time=0.25)

        self.at("second job")
        self.play(
            m_loop2.animate.move_to([-2.90, -0.62, 0]),
            m_door.animate.move_to([1.05, -0.45, 0]),
            w.mito.door_lbl.animate.set_opacity(1.0),
            run_time=1.0,
        )
        self.remove(m_loop2)

        # Beat 2: blocks CPT-I -> malonyl wedges into door, door swings shut, swirl dims
        self.at("It blocks")
        self.play(
            m_door.animate.move_to([1.62, -0.45, 0]),
            w.mito.door_angle_tr.animate.set_value(0.0),
            w.mito.swirl_op.animate.set_value(0.24),
            swirl_spd.animate.set_value(0.45),
            run_time=1.0,
        )

        # Beat 3: palmitate bar spawns clear of loop, bumps near closed door, floats back below loop
        self.at("the gate fat must pass")
        palm = make_palmitate_bar().move_to([0.25, -1.98, 0])
        self.play(FadeIn(palm, scale=0.85), run_time=0.35)
        self.play(palm.animate.move_to([0.45, -0.35, 0]), run_time=0.65)
        self.play(palm.animate.move_to([-1.75, -2.02, 0]), run_time=0.85)

        # Beat 4: two arrows from one malonyl block light at once (high clear space, clear of NADPH & mito wall)
        self.at("commits a cell to building")
        hub_m = make_malonyl_block(scale=1.15).move_to([0.15, 2.55, 0])
        arr_build = Arrow([-0.30, 2.38, 0], [-1.35, 1.55, 0], color=GREEN, stroke_width=5.5, buff=0)
        lbl_build = T("build", size=28, color=GREEN, weight=BOLD).next_to(hub_m, LEFT, buff=0.45)

        arr_block = Arrow([0.60, 2.38, 0], [1.65, 0.25, 0], color=RED, stroke_width=5.5, buff=0)
        lbl_block = T("block burning", size=28, color=RED, weight=BOLD).next_to(hub_m, RIGHT, buff=0.45)

        self.play(FadeIn(hub_m), GrowArrow(arr_build), FadeIn(lbl_build), run_time=0.65)

        self.at("shuts the door on burning")
        self.play(GrowArrow(arr_block), FadeIn(lbl_block), run_time=0.65)
        self.finish()


# ------------------------------------------------------------------ Scene 06
class S06Predict(SpokenScene):
    def construct(self):
        w = build_full_world(
            acc_crank_speed=lambda: 1.6,
            loop_speed=lambda: 1.0,
            swirl_speed=lambda: 0.45,
            swirl_op=0.24,
            door_angle=0.0,
            bat1_lvl=0.75,
            bat2_lvl=0.75,
            show_batteries=True,
            door_label="CPT-I gate",
            split_acc=False,
        )
        wedge = make_malonyl_block(scale=0.85).move_to([1.62, -0.45, 0])
        self.add(w, wedge)

        # Beat 1: ACC splits cleanly into ACC1 and ACC2 (ACC2 emerges in open floor space below ACC1)
        self.at("two forms")
        acc_copy = make_acc_gate(
            center=(-4.95, -1.78, 0),
            size=(0.95, 0.95),
            label="ACC2",
            crank_speed_fn=lambda: 0.9,
            show_slot=False,
            label_pos=RIGHT,
        )
        acc1_new_lbl = T("ACC1", size=28, color=BLUE, weight=BOLD).move_to(w.acc1.lbl)
        self.play(
            swap(w.acc1.lbl, acc1_new_lbl, run_time=0.55),
            FadeIn(acc_copy, shift=DOWN * 0.2),
        )
        w.acc1.lbl = acc1_new_lbl

        # Beat 2: ACC1 feeds synthase
        self.at("A CC1")
        m1 = make_malonyl_block().move_to([-4.05, -0.62, 0])
        self.play(FadeIn(m1), m1.animate.move_to([-2.90, -0.62, 0]), run_time=0.75)
        self.remove(m1)

        self.at("feeds the synthase")
        m2 = make_malonyl_block().move_to([-4.05, -0.62, 0])
        self.play(FadeIn(m2), m2.animate.move_to([-2.90, -0.62, 0]), run_time=0.75)
        self.remove(m2)

        # Beat 3: ACC2 slides onto mitochondrion outer wall and places label above
        self.at("A CC2")
        acc2_target = make_acc_gate(
            center=(2.48, 1.55, 0),
            size=(1.12, 1.28),
            label="ACC2",
            crank_speed_fn=lambda: 0.9,
            show_slot=False,
            label_pos=UP,
        )
        self.play(Transform(acc_copy, acc2_target), run_time=1.3)

        # Beat 4: Question text above
        self.at("Why put a")
        q = question_card("Why ACC2 on the mitochondrion?", y=3.05, max_w=9.8)
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 07
class S07PredictHold(PredictPause):
    QUESTION = "Why ACC2 on the mitochondrion?"
    CARD = {"y": 3.05, "max_w": 9.8}
    RING_AT = (5.85, 3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = build_full_world(
            acc_crank_speed=lambda: 1.4,
            loop_speed=lambda: 0.9,
            swirl_speed=lambda: 0.40,
            swirl_op=0.24,
            door_angle=0.0,
            bat1_lvl=0.75,
            bat2_lvl=0.75,
            show_batteries=True,
            door_label="CPT-I gate",
            split_acc=True,
            acc2_crank_speed=lambda: 0.9,
        )
        wedge = make_malonyl_block(scale=0.85).move_to([1.62, -0.45, 0])
        return VGroup(w, wedge)


# ------------------------------------------------------------------ Scene 08
class S08Answer(SpokenScene):
    def construct(self):
        acc2_spd = ValueTracker(0.9)
        w = build_full_world(
            acc_crank_speed=lambda: 1.5,
            loop_speed=lambda: 1.0,
            swirl_speed=lambda: 0.40,
            swirl_op=0.24,
            door_angle=0.0,
            bat1_lvl=0.75,
            bat2_lvl=0.75,
            show_batteries=True,
            door_label="CPT-I gate",
            split_acc=True,
            acc2_crank_speed=lambda: acc2_spd.get_value(),
        )
        wedge = make_malonyl_block(scale=0.85).move_to([1.62, -0.45, 0])
        q = question_card("Why ACC2 on the mitochondrion?", y=3.05, max_w=9.8)
        self.add(w, wedge, q)
        self.play(FadeOut(q), run_time=0.45)

        # Beat 1: where the blocker is made -> ACC2 releases malonyl blocks to CPT-I door
        self.at("where the blocker is made")
        acc2_spd.set_value(1.9)
        b_a2_1 = make_malonyl_block(scale=0.85).move_to([1.95, 1.05, 0])
        b_a2_2 = make_malonyl_block(scale=0.85).move_to([1.95, 1.05, 0])
        self.play(FadeIn(b_a2_1), b_a2_1.animate.move_to([1.48, 0.12, 0]), run_time=0.85)

        # Beat 2: Much of the malonyl CoA that blocks CPT-I comes from ACC2
        self.at("Much of the malonyl")
        b_a1_drift = make_malonyl_block(scale=0.85).move_to([-4.05, -0.62, 0])
        self.play(
            FadeIn(b_a2_2),
            b_a2_2.animate.move_to([1.48, -0.85, 0]),
            FadeIn(b_a1_drift),
            b_a1_drift.animate.move_to([-0.55, -1.75, 0]),
            run_time=1.3,
        )

        self.at("comes from")
        self.play(
            b_a1_drift.animate.move_to([0.95, -0.45, 0]),
            Indicate(w.acc2.housing, color=YELLOW, scale_factor=1.06),
            run_time=0.95,
        )
        self.play(FadeOut(b_a1_drift), run_time=0.3)

        # Beat 3: ACC1's malonyl CoA is mainly a building block
        self.at("mainly a building block")
        b_build1 = make_malonyl_block().move_to([-3.85, -0.62, 0])
        b_build2 = make_malonyl_block().move_to([-3.15, -0.62, 0])
        lbl_build = make_token("building block", color=GREEN, size=26).move_to([-4.95, -1.78, 0])
        self.play(
            FadeIn(b_build1),
            FadeIn(b_build2),
            FadeIn(lbl_build, shift=UP * 0.15),
            run_time=0.55,
        )
        self.play(
            b_build1.animate.scale(1.20),
            b_build2.animate.scale(1.20),
            rate_func=there_and_back,
            run_time=0.65,
        )
        self.play(b_build1.animate.move_to([-2.90, -0.62, 0]).set_opacity(0), FadeOut(b_build2), run_time=0.45)

        # Beat 4: ACC2's is mainly a signal
        self.at("mainly a signal")
        lbl_sig = make_token("signal", color=YELLOW, size=26).move_to([4.25, 2.25, 0])
        self.play(FadeIn(lbl_sig, shift=UP * 0.12), run_time=0.35)
        self.play(
            wedge.animate.scale(1.22),
            b_a2_1.animate.scale(1.22),
            b_a2_2.animate.scale(1.22),
            rate_func=there_and_back,
            run_time=0.65,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 09
class S09Fed(SpokenScene):
    def construct(self):
        lever1_tr = ValueTracker(0.25)
        lever2_tr = ValueTracker(0.25)
        malonyl_tr = ValueTracker(0.25)

        w = build_full_world(
            acc_crank_speed=lambda: 0.7 + 2.2 * lever1_tr.get_value(),
            loop_speed=lambda: 0.65 + 1.65 * malonyl_tr.get_value(),
            swirl_speed=lambda: 0.35,
            swirl_op=0.22,
            door_angle=0.0,
            bat1_lvl=0.80,
            bat2_lvl=0.80,
            show_batteries=False,
            door_label="CPT-I gate",
            split_acc=True,
            acc2_crank_speed=lambda: 0.5 + 1.7 * lever2_tr.get_value(),
            acc_lever=lever1_tr,
            acc2_lever=lever2_tr,
        )
        wedge = make_malonyl_block(scale=0.85).move_to([1.62, -0.45, 0])

        head = T("fed state", size=34, color=GREEN, weight=BOLD).move_to([0.0, 3.12, 0])

        # Central gauge labelled 'malonyl CoA' (schematic, no numbers)
        g_bg = RoundedRectangle(
            corner_radius=0.10,
            width=0.44,
            height=2.20,
            stroke_color=YELLOW,
            stroke_width=2.8,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to([0.55, 0.72, 0])

        def mk_g_fill():
            v = float(np.clip(malonyl_tr.get_value(), 0.04, 1.0))
            fh = 2.04 * v
            r = Rectangle(width=0.30, height=fh, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
            r.move_to([0.55, g_bg.get_bottom()[1] + 0.08 + fh / 2, 0])
            return r

        g_fill = always_redraw(mk_g_fill)
        g_lbl = T("malonyl CoA", size=24, color=YELLOW, weight=BOLD).next_to(g_bg, UP, buff=0.14)
        gauge = VGroup(g_bg, g_fill, g_lbl)

        self.add(w, wedge, head, gauge)

        # Beat 1: Insulin and plentiful citrate push ACC on (clear of ACC1 border)
        self.at("Insulin and plentiful citrate")
        ins_arr = Arrow([-6.28, 1.25, 0], [-5.75, 0.72, 0], color=GREEN, stroke_width=5, buff=0)
        ins_lbl = T("insulin", size=24, color=GREEN, weight=BOLD).move_to([-5.95, 1.68, 0])
        cit_tok = make_token("citrate", color=GREEN, size=24).move_to([-4.95, -1.92, 0])
        self.play(GrowArrow(ins_arr), FadeIn(ins_lbl), FadeIn(cit_tok, shift=UP * 0.15), run_time=0.55)
        self.play(
            cit_tok.animate.move_to([-4.95, -1.68, 0]),
            lever1_tr.animate.set_value(1.0),
            lever2_tr.animate.set_value(1.0),
            run_time=0.85,
        )

        # Beat 2: malonyl CoA rises
        self.at("malonyl")
        self.play(malonyl_tr.animate.set_value(0.95), run_time=1.2)

        # Beat 3: synthase gets its extenders, CPT-I gate closes
        self.at("gets its extenders")
        m_a = make_malonyl_block().move_to([-4.05, -0.62, 0])
        m_b = make_malonyl_block().move_to([-4.05, -0.62, 0])
        self.play(FadeIn(m_a), m_a.animate.move_to([-2.90, -0.62, 0]), run_time=0.55)
        self.remove(m_a)
        self.play(FadeIn(m_b), m_b.animate.move_to([-2.90, -0.62, 0]), run_time=0.5)
        self.remove(m_b)

        self.at("gate closes")
        m_lock = make_malonyl_block(scale=0.85).move_to([1.95, 1.00, 0])
        self.play(FadeIn(m_lock), m_lock.animate.move_to([1.56, 0.05, 0]), run_time=0.7)
        lock_ring = SurroundingRectangle(wedge, corner_radius=0.10, color=RED, stroke_width=3.5, buff=0.06)
        self.play(Create(lock_ring), run_time=0.45)

        # Beat 4: palmitate bars stack neatly side-by-side on floor below loop (clear of D and each other)
        self.at("tends not to burn it")
        p1 = make_palmitate_bar().move_to([-1.75, -1.95, 0])
        p2 = make_palmitate_bar().move_to([-0.82, -1.95, 0])
        self.play(FadeIn(p1), p1.animate.move_to([-2.68, -2.08, 0]), run_time=0.6)
        self.play(FadeIn(p2), p2.animate.move_to([-0.82, -2.08, 0]), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 10
class S10Return(SpokenScene):
    def construct(self):
        w = build_full_world(
            acc_crank_speed=lambda: 1.6,
            loop_speed=lambda: 1.0,
            swirl_speed=lambda: 0.40,
            swirl_op=0.22,
            door_angle=0.0,
            bat1_lvl=0.80,
            bat2_lvl=0.80,
            show_batteries=False,
            door_label="CPT-I gate",
            split_acc=True,
            acc2_crank_speed=lambda: 1.0,
        )
        p1 = make_palmitate_bar().move_to([-2.68, -2.08, 0])
        p2 = make_palmitate_bar().move_to([-0.82, -2.08, 0])
        wedge = make_malonyl_block(scale=0.85).move_to([1.62, -0.45, 0])
        chain_tr = ValueTracker(14.0)
        chain_cnt = make_chain_counter(chain_tr, at=(-2.15, 2.08, 0))
        self.add(w, p1, p2, wedge, chain_cnt)

        # Beat 1: one small molecule with two jobs (well clear of chain counter on left and ACC2 on right)
        self.at("one small molecule")
        hero_m = make_malonyl_block(scale=1.25).move_to([0.62, 1.35, 0])
        hero_ring = SurroundingRectangle(hero_m, corner_radius=0.14, color=GOLD, stroke_width=3.5, buff=0.10)
        hero_lbl = T("malonyl CoA", size=26, color=YELLOW, weight=BOLD).next_to(hero_ring, UP, buff=0.12)
        self.play(FadeIn(hero_m, scale=0.85), Create(hero_ring), FadeIn(hero_lbl), run_time=0.65)

        self.at("two jobs")
        self.play(Indicate(hero_ring, color=YELLOW, scale_factor=1.10), run_time=0.6)

        # Beat 2: brick for the chain -> copy slots onto top-right rim of CRDR loop (clear of CRDR/synthase text)
        self.at("In the cytoplasm")
        copy_brick = make_malonyl_block(scale=0.95).move_to(hero_m.get_center())
        self.add(copy_brick)

        self.at("a brick for the chain")
        arc_left = ArcBetweenPoints(hero_m.get_center(), [-0.72, 0.35, 0], angle=0.45)
        self.play(MoveAlongPath(copy_brick, arc_left), chain_tr.animate.set_value(16.0), run_time=0.9)
        self.play(FadeOut(copy_brick), run_time=0.25)

        # Beat 3: lock on the door -> second copy settles into closed CPT-I door
        self.at("At the mitochondrion")
        copy_lock = make_malonyl_block(scale=0.95).move_to(hero_m.get_center())
        self.add(copy_lock)

        self.at("a lock on the door")
        arc_right = ArcBetweenPoints(hero_m.get_center(), [1.62, -0.45, 0], angle=-0.35)
        self.play(MoveAlongPath(copy_lock, arc_right), run_time=0.9)
        self.play(Indicate(copy_lock, color=RED, scale_factor=1.18), run_time=0.45)

        # Beat 4: opening question reappears and is answered by 'malonyl CoA' sliding beneath it
        self.at("tends not to build")
        self.play(FadeOut(hero_m), FadeOut(hero_ring), FadeOut(hero_lbl), run_time=0.35)
        q_ret = T("What keeps new fat unburned?", size=32, color=GOLD, weight=BOLD).move_to([0.0, 3.18, 0])
        ans = T("malonyl CoA", size=34, color=YELLOW, weight=BOLD).move_to([0.0, 2.58, 0])
        self.play(FadeIn(q_ret, shift=DOWN * 0.1), run_time=0.4)
        self.play(FadeIn(ans, shift=UP * 0.15), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ Scene 11
class S11End(EndCard):
    LINE = "The malonyl CoA that builds fat also shuts the gate to burning."
