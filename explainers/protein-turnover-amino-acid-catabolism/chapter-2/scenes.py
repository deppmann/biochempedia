"""
WHAT PILES UP — Protein Turnover and Amino Acid Catabolism, Chapter 2
======================================================================

COLOUR MAP (one colour per concept, carried across all 13 scenes):
- BLUE   (#58C4DD) : carbon skeletons / amino-acid blocks & carbon conveyor
- GOLD   (#D4A843) : nitrogen tokens, urea wheel, urea / ammonia / glutamine carriers
- YELLOW (#F5D547) : urine flask & urine liquid (oxidizes to dark charcoal-black in alkaptonuria)
- GREEN  (#83C167) : biotin cofactor tool token & cofactor fingerprint stamp
- PURPLE (#B388EB) : vitamin B12 cofactor tool token & rearrangement stamp
- RED    (#FC6255) : broken/defective enzyme stations, blood lane (dark red), danger/neurotoxic alerts
- TEAL   (#3FB8C0) : seven-door central-metabolism hub & diagnostic focus ring
- GREY   (#8B93A1) : working enzyme stations, structural conveyor rails, schematic tag
- TEXT   (#E8EAF0) : titles, questions, primary labels

WORLD CARRIED ACROSS THE FILM:
The cellular amino-acid recycling center: an upper GOLD five-station urea wheel, a central
conveyor line of GREY enzyme stations carrying BLUE carbon skeletons into a TEAL seven-door
central-metabolism hub, a dark RED blood lane running along the bottom, and a YELLOW urine
flask at lower right. Scenes zoom into or pan across parts of this single connected world.

WHAT CHANGES ON SCREEN (and what computes it) PER SPOKEN SCENE:
- s00_link_and_hook : Nitrogen token rides into turning urea wheel -> urea capsule; carbon block
                      rides conveyor into 7-door hub; camera pushes onto urine flask whose
                      liquid color interpolates YELLOW -> black with swirling meniscus (t-driven).
- s02_line          : Camera pulls back to 3-station carbon line; BLUE blocks continuously
                      transform shape across stations (computed by x-position); GREEN tool
                      slots into station 2 and stamps cofactor fingerprint above.
- s03_succinyl      : Four tagged BLUE blocks converge into propionyl-CoA (3 sub-blocks);
                      biotin station adds a 4th carbon sub-block (methylmalonyl-CoA); B12
                      station shuffles the 4 sub-blocks into linear succinyl-CoA into lit door.
- s04_predict       : Middle station jams RED (rollers stop); upstream BLUE blocks arrive and
                      slow/queue without piling; empty left/right schematic bars appear.
- s06_answer        : Shared ValueTracker `heap_lvl` drives both the discrete stacked BLUE heap
                      behind the jam and the rising left level bar, then overflows blocks into
                      the blood lane and clouds the urine flask.
- s07_pku           : Jammed line relabels to PKU / phenylalanine hydroxylase; shared
                      `blood_lvl` ValueTracker thickens blood phenylalanine blocks and raises
                      blood gauge; blocks flow into dried blood spot card to flag PKU.
- s08_msud          : Separate branched-chain line jams RED (MSUD); dual-shape heap grows;
                      blocks enter flask and emit computed rising sine-wave amber wisps;
                      leucine tracker pulses blood blocks and raises neurotoxic warning gauge.
- s09_ammonia       : Pan up to urea wheel; wheel angular speed ramps to 0 as station turns
                      RED; shared `nh3_lvl` tracker builds GOLD heap, climbs danger gauge,
                      and swells astrocyte + brain outlines as glutamine carts fill.
- s10_garrod        : Urea wheel resumes; carbon line jams at alkaptonuria; homogentisate
                      spills to urine flask where `ox_lvl` ValueTracker darkens liquid to black;
                      diagnostic line traces back; rare other stations light up then dim.
- s11_close         : Full world view; heap forms behind RED station; TEAL magnifying ring
                      sweeps heap -> broken step; biotin (GREEN) and B12 (PURPLE) tokens glow.
"""

from bp_parts import *
import numpy as np

PURPLE = "#B388EB"
DARK_RED = "#52181C"
BLOOD_BORDER = "#A83B38"
STATION_FILL = "#222836"
HUB_FILL = "#162A30"
BLACK_URINE = "#2C2522"
LESSON_TITLE = "Protein Turnover and Amino Acid Catabolism: Tag, Recognize, Destroy, Recycle"


# ------------------------------------------------------------------ shared world builders
def make_station(x, y, label="", tag="", tag_color=RED, w=1.70, h=1.16, broken=False,
                 roller_speed=3.0, label_size=24, label_max_w=None):
    """Machine station with rotating internal rollers (stopped when broken) and clean outer labels."""
    stroke = RED if broken else GREY
    sw = 3.8 if broken else 2.5
    box = RoundedRectangle(
        corner_radius=0.16, width=w, height=h,
        stroke_color=stroke, stroke_width=sw,
        fill_color=STATION_FILL, fill_opacity=0.95,
    ).move_to([x, y, 0])

    rollers = VGroup()
    for rx in (x - w * 0.26, x + w * 0.26):
        ring = Circle(radius=0.23, stroke_color=stroke, stroke_width=3.2,
                      fill_color=BG, fill_opacity=0.9).move_to([rx, y, 0])
        spoke1 = Line([rx - 0.16, y, 0], [rx + 0.16, y, 0], color=stroke, stroke_width=3.0)
        spoke2 = Line([rx, y - 0.16, 0], [rx, y + 0.16, 0], color=stroke, stroke_width=3.0)
        gear = VGroup(ring, spoke1, spoke2)
        if not broken and roller_speed != 0:
            gear.add_updater(lambda m, dt, sp=roller_speed: m.rotate(-sp * dt, about_point=m[0].get_center()))
        rollers.add(gear)

    g = VGroup(box, rollers)
    g.box = box
    g.rollers = rollers
    g.label_mob = None
    g.tag_mob = None

    if label:
        mw = label_max_w if label_max_w is not None else (w + 1.0)
        lab = fit_text(label, max_w=mw, size=label_size, color=RED if broken else TEXT,
                       min_size=24, max_lines=2)
        lab.next_to(box, DOWN, buff=0.18)
        g.add(lab)
        g.label_mob = lab

    if tag:
        tg = boxed_label(tag, color=tag_color, size=24, pad=0.14, fill_opacity=0.22)
        tg.next_to(box, UP, buff=0.18)
        g.add(tg)
        g.tag_mob = tg

    return g


def make_conveyor_gaps(stations_x, y, start_x, end_x, station_w=1.70, belt_h=0.28, speed=1.55):
    """Conveyor belt segments in the gaps between stations (never crossing station outlines/labels)."""
    edges = [start_x]
    for sx in sorted(stations_x):
        edges.append(sx - station_w / 2)
        edges.append(sx + station_w / 2)
    edges.append(end_x)

    belts = VGroup()
    for i in range(0, len(edges), 2):
        a, b = edges[i], edges[i + 1]
        if b - a < 0.15:
            continue
        w = b - a
        cx = (a + b) / 2
        rail = Rectangle(
            width=w, height=belt_h,
            stroke_color=GREY, stroke_width=2.2,
            fill_color="#1A202B", fill_opacity=0.9,
        ).move_to([cx, y, 0])
        rail.layout_ok = True
        belts.add(rail)

        n_ticks = max(2, int(w / 0.38))
        margin = 0.08 / w
        orig_span = max(w - 0.16, 0.2)
        for k in range(n_ticks):
            tick = Line(UP * 0.09, DOWN * 0.09, color=TEXT, stroke_width=2.6).set_opacity(0.45)
            tick._phase = k / n_ticks

            def _move_tick(m, dt, r=rail, mg=margin, ospan=orig_span):
                rw = r.get_right()[0] - r.get_left()[0]
                if rw <= 1e-4:
                    return
                span = rw * (1.0 - 2.0 * mg)
                left_x = r.get_left()[0] + rw * mg
                cy = r.get_center()[1]
                m._phase = (m._phase + speed * dt / ospan) % 1.0
                m.move_to([left_x + m._phase * span, cy, 0])

            tick.add_updater(_move_tick)
            tick.move_to([a + 0.08 + (k / n_ticks) * (w - 0.16), y, 0])
            belts.add(tick)
    return belts


def make_carbon_block(stage=0, scale=1.0):
    """Schematic BLUE carbon skeleton block whose notches/shape reflect enzymatic steps."""
    s = 0.18 * scale
    if stage == 0:
        b = RoundedRectangle(corner_radius=0.05, width=2.2 * s, height=1.5 * s,
                             stroke_color=TEXT, stroke_width=1.6, fill_color=BLUE, fill_opacity=0.94)
        return VGroup(b)
    if stage == 1:
        b = RoundedRectangle(corner_radius=0.05, width=2.2 * s, height=1.5 * s,
                             stroke_color=TEXT, stroke_width=1.6, fill_color=BLUE, fill_opacity=0.94)
        notch = Square(side_length=0.85 * s, stroke_color=TEXT, stroke_width=1.4,
                       fill_color=BLUE, fill_opacity=0.98).move_to(b.get_top() + LEFT * 0.45 * s + UP * 0.35 * s)
        return VGroup(b, notch)
    if stage == 2:
        row = VGroup(*[
            RoundedRectangle(corner_radius=0.03, width=s, height=s, stroke_color=BG, stroke_width=1.5,
                             fill_color=BLUE, fill_opacity=0.95)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.02 * scale)
        knob = RoundedRectangle(corner_radius=0.03, width=s, height=s, stroke_color=TEXT, stroke_width=1.8,
                                fill_color=BLUE, fill_opacity=1.0).next_to(row[1], UP, buff=0.02 * scale)
        return VGroup(row, knob)
    row = VGroup(*[
        RoundedRectangle(corner_radius=0.03, width=s, height=s, stroke_color=BG, stroke_width=1.5,
                         fill_color=BLUE, fill_opacity=0.95)
        for _ in range(4)
    ]).arrange(RIGHT, buff=0.02 * scale)
    return row


def make_seven_doors(x, y, height=2.7, width=1.40, lit_idx=None, lit_label=None):
    """Seven-door central-metabolism hub on the right; lit_label placed safely ABOVE title."""
    panel = RoundedRectangle(
        corner_radius=0.16, width=width, height=height,
        stroke_color=TEAL, stroke_width=2.8, fill_color=HUB_FILL, fill_opacity=0.92,
    ).move_to([x, y, 0])
    doors = VGroup()
    ys = np.linspace(y + height * 0.37, y - height * 0.37, 7)
    for idx, dy in enumerate(ys):
        is_lit = (lit_idx is not None and idx == lit_idx)
        door = RoundedRectangle(
            corner_radius=0.06, width=width * 0.62, height=height * 0.085,
            stroke_color=TEAL, stroke_width=2.6 if is_lit else 1.8,
            fill_color=TEAL, fill_opacity=0.92 if is_lit else 0.24,
        ).move_to([x, dy, 0])
        doors.add(door)

    title = T("7 doors", size=24, color=TEAL).next_to(panel, UP, buff=0.14)
    g = VGroup(panel, doors, title)
    g.panel, g.doors, g.title = panel, doors, title
    if lit_idx is not None and lit_label:
        lab = boxed_label(lit_label, color=TEAL, size=24, pad=0.11, fill_opacity=0.22).next_to(title, UP, buff=0.14)
        if lab.get_right()[0] > 6.4:
            lab.align_to([6.4, 0, 0], RIGHT)
        g.add(lab)
        g.lit_label = lab
    return g


def make_urea_wheel(center, radius=1.05, speed_tracker=None, broken_idx=None):
    """Five-station urea wheel (GOLD), turning continuously unless speed_tracker -> 0."""
    c = np.array(center, dtype=float)
    ring = Circle(radius=radius, stroke_color=GOLD, stroke_width=5.0, fill_opacity=0).move_to(c)
    stations = VGroup()
    for k in range(5):
        ang = PI / 2 + k * TAU / 5
        pos = c + radius * np.array([np.cos(ang), np.sin(ang), 0.0])
        is_bad = (broken_idx is not None and k == broken_idx)
        st = Circle(
            radius=0.22 * (radius / 1.05),
            stroke_color=RED if is_bad else GOLD,
            stroke_width=3.2 if is_bad else 2.4,
            fill_color=RED if is_bad else "#2B2518",
            fill_opacity=0.9 if is_bad else 0.95,
        ).move_to(pos)
        stations.add(st)

    rotor = VGroup(ring, stations)
    rotor.ring = ring
    rotor.stations = stations
    if speed_tracker is None:
        rotor.add_updater(lambda m, dt: m.rotate(0.75 * dt, about_point=m.ring.get_center()))
    else:
        rotor.add_updater(lambda m, dt: m.rotate(0.75 * speed_tracker.get_value() * dt, about_point=m.ring.get_center()))
    return rotor


def make_blood_lane(x0=-6.1, x1=3.7, y=-2.30, h=0.66, show_label=True):
    """Dark RED blood lane along the bottom of the world."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    lane = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        stroke_color=BLOOD_BORDER, stroke_width=2.4,
        fill_color=DARK_RED, fill_opacity=0.90,
    ).move_to([cx, y, 0])
    lane.set_z_index(0)
    lane.layout_ok = True
    g = VGroup(lane)
    g.lane = lane
    if show_label:
        lab = T("blood", size=24, color=RED).next_to(lane, LEFT, buff=0.15)
        if lab.get_left()[0] < -6.3:
            lab.next_to(lane, UP, buff=0.14).align_to(lane, LEFT).shift(RIGHT * 0.1)
        g.add(lab)
        g.label_mob = lab
    return g


def make_urine_flask(center, height=1.75, darkness_tracker=None, cloud_tracker=None, wave_amp=0.06):
    """Erlenmeyer urine flask with live swirling wave-surface liquid and interior swirl curve."""
    c = np.array(center, dtype=float)
    s = height / 2.2
    pts = [
        c + np.array([-0.26 * s, 1.05 * s, 0]),
        c + np.array([-0.24 * s, 0.52 * s, 0]),
        c + np.array([-0.82 * s, -0.82 * s, 0]),
        c + np.array([-0.74 * s, -1.00 * s, 0]),
        c + np.array([0.74 * s, -1.00 * s, 0]),
        c + np.array([0.82 * s, -0.82 * s, 0]),
        c + np.array([0.24 * s, 0.52 * s, 0]),
        c + np.array([0.26 * s, 1.05 * s, 0]),
    ]
    outline = VMobject(stroke_color=TEXT, stroke_width=3.2, fill_color="#171B24", fill_opacity=0.55)
    outline.set_points_as_corners(pts)
    lip = Line(pts[0] + LEFT * 0.08 * s, pts[-1] + RIGHT * 0.08 * s, color=TEXT, stroke_width=3.5)

    clock = ValueTracker(0.0)

    def _build_liquid():
        t = clock.get_value()
        dark = float(np.clip(darkness_tracker.get_value(), 0.0, 1.0)) if darkness_tracker else 0.0
        cloud = float(np.clip(cloud_tracker.get_value(), 0.0, 1.0)) if cloud_tracker else 0.0

        col = interpolate_color(ManimColor(YELLOW), ManimColor("#B69C3F"), cloud * 0.8)
        col = interpolate_color(col, ManimColor(BLACK_URINE), dark)

        xs = np.linspace(-0.56 * s, 0.56 * s, 22)
        surf_y = -0.06 * s
        wave = wave_amp * s * np.sin(5.8 * xs / max(s, 0.2) + 4.0 * t)
        surf_pts = [c + np.array([x, surf_y + w, 0]) for x, w in zip(xs, wave)]
        liq_pts = list(surf_pts) + [
            c + np.array([0.78 * s, -0.80 * s, 0]),
            c + np.array([0.70 * s, -0.96 * s, 0]),
            c + np.array([-0.70 * s, -0.96 * s, 0]),
            c + np.array([-0.78 * s, -0.80 * s, 0]),
        ]
        liq = Polygon(*liq_pts, stroke_width=0, fill_color=col, fill_opacity=0.92)
        meniscus = VMobject(stroke_color=GREY if dark > 0.5 else YELLOW, stroke_width=2.8, stroke_opacity=0.82)
        meniscus.set_points_as_corners(surf_pts)
        # Subtle inner swirl wave inside the liquid
        sw_xs = np.linspace(-0.42 * s, 0.42 * s, 14)
        sw_ys = -0.48 * s + 0.05 * s * np.sin(6.5 * sw_xs / max(s, 0.2) - 3.4 * t)
        swirl = VMobject(stroke_color=GREY if dark > 0.5 else YELLOW, stroke_width=2.0, stroke_opacity=0.45)
        swirl.set_points_as_corners([c + np.array([x, y, 0]) for x, y in zip(sw_xs, sw_ys)])
        return VGroup(liq, meniscus, swirl)

    liquid = always_redraw(_build_liquid)
    liquid.add_updater(lambda m, dt: clock.increment_value(dt))
    flask = VGroup(liquid, outline, lip)
    flask.outline = outline
    flask.clock = clock
    return flask


def make_tool_token(text, color=GREEN):
    """Cofactor tool badge (notch key + label) that slots into the top of an enzyme station."""
    badge = boxed_label(text, color=color, size=24, pad=0.13, fill_opacity=0.28)
    peg = Rectangle(width=0.22, height=0.20, stroke_color=color, stroke_width=2.0,
                    fill_color=color, fill_opacity=0.85).next_to(badge, DOWN, buff=0)
    return VGroup(badge, peg)


def make_stamp(text, color=GREEN):
    """Fingerprint stamp badge above a station."""
    return boxed_label(text, color=color, size=24, pad=0.14, stroke=3.0, fill_opacity=0.20, corner_radius=0.08)


def make_level_bar(center, width=2.4, height=0.34, tracker=None, color=BLUE):
    """Horizontal bar gauge driven by a 0..1 ValueTracker."""
    c = np.array(center, dtype=float)
    bg = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                          stroke_color=GREY, stroke_width=2.2, fill_color="#171B24", fill_opacity=0.95).move_to(c)
    left_x = c[0] - width / 2 + 0.04

    def _fill():
        v = float(np.clip(tracker.get_value(), 0.0, 1.0)) if tracker else 0.0
        fw = max(0.05, (width - 0.08) * v)
        bar = RoundedRectangle(corner_radius=0.06, width=fw, height=height - 0.08,
                               stroke_width=0, fill_color=color, fill_opacity=0.92)
        bar.move_to([left_x + fw / 2, c[1], 0])
        return bar

    fill = always_redraw(_fill)
    return VGroup(bg, fill)


def make_vertical_gauge(center, label_text, tracker, color=BLUE, height=1.35, width=0.36):
    """Vertical schematic gauge driven by a 0..1 ValueTracker, with label cleanly above."""
    c = np.array(center, dtype=float)
    bg = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                          stroke_color=GREY, stroke_width=2.2, fill_color="#171B24", fill_opacity=0.95).move_to(c)
    bot_y = c[1] - height / 2 + 0.04

    def _fill():
        v = float(np.clip(tracker.get_value(), 0.0, 1.0))
        fh = max(0.05, (height - 0.08) * v)
        bar = RoundedRectangle(corner_radius=0.06, width=width - 0.08, height=fh,
                               stroke_width=0, fill_color=color, fill_opacity=0.92)
        bar.move_to([c[0], bot_y + fh / 2, 0])
        return bar

    fill = always_redraw(_fill)
    lab = fit_text(label_text, max_w=2.4, size=24, color=color, min_size=24, max_lines=2).next_to(bg, UP, buff=0.14)
    return VGroup(bg, fill, lab)


def make_heap_group(anchor_x, base_y, level_tracker, max_cols=3, max_rows=3,
                    color=BLUE, dual_shape=False, scale=1.0):
    """Computed discrete pile of blocks strictly fitted inside the inter-station gap."""
    slots = []
    bw, bh = 0.27 * scale, 0.19 * scale
    gap = 0.04 * scale
    for row in range(max_rows):
        cols_in_row = max(1, max_cols - (row // 2))
        for col in range(cols_in_row):
            bx = anchor_x - col * (bw + gap)
            by = base_y + row * (bh + gap)
            slots.append((bx, by, (row + col) % 2))
    total = len(slots)

    def _draw():
        n = int(round(float(np.clip(level_tracker.get_value(), 0.0, 1.0)) * total))
        g = VGroup()
        for idx in range(n):
            bx, by, kind = slots[idx]
            if dual_shape and kind == 1:
                m = RegularPolygon(n=6, radius=bw * 0.44, stroke_color=TEXT, stroke_width=1.4,
                                   fill_color=color, fill_opacity=0.92).move_to([bx, by, 0])
            else:
                m = RoundedRectangle(corner_radius=0.04, width=bw, height=bh,
                                     stroke_color=TEXT, stroke_width=1.4,
                                     fill_color=color, fill_opacity=0.94).move_to([bx, by, 0])
            g.add(m)
        return g

    return always_redraw(_draw)


def add_lane_stream(scene_mobs, x0, x1, y, speed=1.65, count=6, color=BLUE,
                    density_tracker=None, pulse_red=False):
    """Add drifting blocks ON TOP (z_index=3) of the horizontal blood lane [x0, x1]."""
    rng = np.random.default_rng(7)
    blocks = VGroup()
    span = max(0.5, x1 - x0)
    for i in range(count):
        b = RoundedRectangle(corner_radius=0.04, width=0.36, height=0.24,
                             stroke_color=RED if pulse_red else TEXT,
                             stroke_width=2.6 if pulse_red else 1.6,
                             fill_color=color, fill_opacity=0.96)
        b.set_z_index(3)
        b._phase = (i / count + rng.uniform(-0.02, 0.02)) % 1.0
        b._y_off = rng.uniform(-0.07, 0.07)

        def _upd(m, dt, idx=i):
            m._phase = (m._phase + speed * dt / span) % 1.0
            active_n = count if density_tracker is None else max(0, int(round(density_tracker.get_value() * count)))
            if idx < active_n:
                m.set_opacity(0.96)
                m.move_to([x0 + m._phase * span, y + m._y_off, 0])
            else:
                m.set_opacity(0.0)

        b.add_updater(_upd)
        b.move_to([x0 + b._phase * span, y + b._y_off, 0])
        blocks.add(b)
    blocks.set_z_index(3)
    scene_mobs.add(blocks)
    return blocks


def add_continuous_upstream(start_x, end_x, y, station_xs, speed=1.40, count=3, scale=1.12, stage_fn=None):
    """Continuous BLUE carbon blocks arriving along the line (hiding cleanly inside stations)."""
    grp = VGroup()
    span = max(0.5, end_x - start_x)
    base_p = ValueTracker(0.0)
    grp.add_updater(lambda m, dt: base_p.increment_value(speed * dt / span))

    for k in range(count):
        def _mk(idx=k):
            p = (base_p.get_value() + idx / count) % 1.0
            x = start_x + p * span
            st = stage_fn(x) if stage_fn else 1
            blk = make_carbon_block(st, scale=scale).move_to([x, y, 0])
            if any(abs(x - sx) < 0.72 for sx in station_xs):
                blk.set_opacity(0.0)
            return blk

        m = always_redraw(_mk)
        m.set_z_index(2)
        grp.add(m)
    return grp


# ------------------------------------------------------------------ Scene 0: Hook
class S00LinkAndHook(SpokenScene):
    def construct(self):
        wheel = make_urea_wheel([-3.4, 1.55, 0], radius=1.0)
        wheel_lab = T("urea wheel", size=24, color=GOLD).next_to(wheel, UP, buff=0.2)

        s1 = make_station(-2.8, -0.45, "enzyme", w=1.4, h=0.95)
        s2 = make_station(-0.2, -0.45, "enzyme", w=1.4, h=0.95)
        s3 = make_station(2.2, -0.45, "enzyme", w=1.4, h=0.95)
        belts = make_conveyor_gaps([-2.8, -0.2, 2.2], -0.45, -5.6, 3.6, station_w=1.4)
        hub = make_seven_doors(4.75, -0.20, height=2.7, width=1.4)

        blood = make_blood_lane(-5.6, 2.8, y=-2.45, h=0.62)
        dark_tr = ValueTracker(0.0)
        flask_small = make_urine_flask([4.85, -2.35, 0], height=1.40, darkness_tracker=dark_tr)
        flask_lab = T("urine", size=24, color=YELLOW).next_to(flask_small, LEFT, buff=0.2)

        stag = scope_tag("schematic")

        c_blocks = VGroup()
        for k in range(3):
            blk = make_carbon_block(0, scale=1.05)
            blk._p = k / 3.0

            def _move_c(m, dt):
                m._p = (m._p + 0.16 * dt) % 1.0
                m.move_to([-5.4 + m._p * 9.0, -0.45, 0])

            blk.add_updater(_move_c)
            blk.move_to([-5.4 + blk._p * 9.0, -0.45, 0])
            c_blocks.add(blk)

        self.add(wheel, wheel_lab, belts, s1, s2, s3, hub, blood, flask_small, flask_lab, c_blocks, stag)

        aa_start = Dot(radius=0.18, color=TEXT).move_to([-5.3, 0.85, 0])
        n_tok = Circle(radius=0.18, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.92).move_to([-5.3, 0.85, 0])
        c_tok = make_carbon_block(0, scale=1.1).move_to([-5.3, 0.85, 0])
        self.play(FadeIn(aa_start), run_time=0.4)
        self.play(
            FadeOut(aa_start, run_time=0.25),
            FadeIn(n_tok, run_time=0.25),
            FadeIn(c_tok, run_time=0.25),
            n_tok.animate.move_to([-4.6, 1.55, 0]),
            c_tok.animate.move_to([-4.6, -0.45, 0]),
            run_time=0.8,
        )

        self.at("Nitrogen is caged as urea")
        urea_cap = boxed_label("urea", color=GOLD, size=24, pad=0.12, fill_opacity=0.25).move_to([-1.8, 1.55, 0])
        self.play(n_tok.animate.move_to([-3.4, 1.55, 0]), run_time=0.6)
        self.play(FadeOut(n_tok, run_time=0.25), FadeIn(urea_cap, run_time=0.35), run_time=0.55)

        self.at("carbon enters through seven doors")
        self.play(c_tok.animate.move_to([3.9, -0.45, 0]), run_time=1.15)
        self.play(
            FadeOut(c_tok, run_time=0.25),
            hub.doors[3].animate.set_fill(TEAL, opacity=0.95),
        )

        # Beat 4: Push in on the urine flask cleanly while dimmed conveyor/wheel move on the LEFT side only
        self.at("Now picture")
        for blk in c_blocks:
            blk.clear_updaters()
        self.play(
            FadeOut(urea_cap), FadeOut(c_blocks),
            FadeOut(wheel_lab), FadeOut(flask_lab), FadeOut(flask_small),
            FadeOut(blood.label_mob), FadeOut(hub),
            FadeOut(s1.label_mob), FadeOut(s2.label_mob), FadeOut(s3.label_mob),
            run_time=0.4,
        )
        self.remove(urea_cap)

        # Keep ring hollow: pause updater during move, then dim stroke/fill cleanly and resume
        bg_shapes = VGroup(s1.box, s1.rollers, s2.box, s2.rollers, s3.box, s3.rollers, belts, blood.lane)
        bg_shapes.layout_ok = True
        wheel.layout_ok = True
        wheel.clear_updaters()
        self.play(
            wheel.animate.scale(0.55).move_to([-4.8, 0.55, 0]),
            bg_shapes.animate.scale(0.45).move_to([-4.3, -1.65, 0]).set_opacity(0.28),
            run_time=0.55,
        )
        wheel.ring.set_stroke(opacity=0.35)
        wheel.stations.set_stroke(opacity=0.35).set_fill(opacity=0.25)
        wheel.add_updater(lambda m, dt: m.rotate(0.65 * dt, about_point=m.ring.get_center()))

        big_dark = ValueTracker(0.0)
        big_flask = make_urine_flask([0.0, -0.45, 0], height=4.4, darkness_tracker=big_dark, wave_amp=0.075)
        self.play(FadeIn(big_flask), run_time=0.4)
        self.play(big_dark.animate.set_value(1.0), run_time=1.45, rate_func=linear)

        self.at("1902")
        garrod_tag = boxed_label("1902 · Garrod: inherited", color=TEXT, size=26, pad=0.18, fill_opacity=0.18)
        garrod_tag.move_to([4.15, -0.2, 0])
        self.play(FadeIn(garrod_tag, shift=LEFT * 0.2), run_time=0.6)

        self.at("How can a")
        q_txt = fit_text("How can a color point to one broken step?", max_w=11.8, size=34, color=TEXT)
        q_txt.move_to([0.0, 3.05, 0])
        q_mark = T("?", size=58, color=RED, weight=BOLD).move_to([-2.45, -0.2, 0])
        q_mark.add_updater(lambda m, dt: m.set_opacity(0.45 + 0.55 * np.sin(5.2 * self.elapsed())))
        self.play(FadeIn(q_txt), FadeIn(q_mark), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 1: Silent 2s Title
class S01Title(NarratedScene):
    def construct(self):
        wheel = make_urea_wheel([-4.8, -0.35, 0], radius=0.55)
        wheel.ring.set_stroke(opacity=0.35)
        wheel.stations.set_opacity(0.35)
        s1 = make_station(-4.9, -1.8, "", w=0.8, h=0.52).set_opacity(0.28)
        s2 = make_station(-3.5, -1.8, "", w=0.8, h=0.52).set_opacity(0.28)
        belts = make_conveyor_gaps([-4.9, -3.5], -1.8, -6.0, -2.3, station_w=0.8, belt_h=0.15).set_opacity(0.28)
        bg = VGroup(wheel, s1, s2, belts)
        bg.layout_ok = True

        big_dark = ValueTracker(1.0)
        flask = make_urine_flask([0.0, -1.25, 0], height=3.2, darkness_tracker=big_dark, wave_amp=0.06)

        q_txt = fit_text("How can a color point to one broken step?", max_w=11.8, size=34, color=TEXT).move_to([0.0, 3.05, 0])
        garrod_tag = boxed_label("1902 · Garrod: inherited", color=TEXT, size=26, pad=0.18, fill_opacity=0.18).move_to([4.15, -0.2, 0])

        brand = T(SITE_NAME, size=22, color=TEAL, weight=BOLD).set_opacity(0.9)
        brand.layout_ok = True
        lesson = fit_text(LESSON_TITLE.upper(), max_w=11.2, size=22, color=GREY, min_size=22, max_lines=2)
        title = T("What Piles Up", size=54, font=TITLE_FONT, color=TEXT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        title_blk = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.18).move_to([0.0, 2.05, 0])

        self.add(bg, flask, q_txt, garrod_tag, scope_tag("schematic"))
        self.play(FadeOut(q_txt), FadeOut(garrod_tag), FadeIn(title_blk, shift=UP * 0.1), run_time=0.65)
        self.finish()


# ------------------------------------------------------------------ Helper for carbon line scenes
def build_carbon_line_world(station_labels=("enzyme", "enzyme", "enzyme"),
                            station_xs=(-3.8, -1.2, 1.4), line_y=0.25,
                            broken_idx=None, tags=(None, None, None),
                            hub_x=4.9, hub_y=0.25, hub_h=2.7, lit_idx=None, lit_label=None,
                            blood_x0=-6.1, blood_y=-2.25, flask_pos=(5.05, -2.15, 0),
                            darkness_tr=None, cloud_tr=None, label_max_w=None):
    """Consistent carbon-line world used across s02..s08, s10."""
    stations = []
    for i, (sx, lab) in enumerate(zip(station_xs, station_labels)):
        tg = tags[i] if i < len(tags) else None
        mw = label_max_w[i] if isinstance(label_max_w, (list, tuple)) else label_max_w
        st = make_station(sx, line_y, label=lab, tag=tg or "", tag_color=RED,
                          broken=(broken_idx == i), label_max_w=mw)
        stations.append(st)

    belts = make_conveyor_gaps(station_xs, line_y, -6.1, hub_x - 0.85, station_w=1.70)
    hub = make_seven_doors(hub_x, hub_y, height=hub_h, width=1.40, lit_idx=lit_idx, lit_label=lit_label)
    blood = make_blood_lane(blood_x0, flask_pos[0] - 0.95, y=blood_y, h=0.64, show_label=False)
    flask = make_urine_flask(flask_pos, height=1.50, darkness_tracker=darkness_tr, cloud_tracker=cloud_tr)
    return VGroup(belts, *stations, hub, blood, flask), stations, belts, hub, blood, flask


# ------------------------------------------------------------------ Scene 2: Line of Enzymes
class S02Line(SpokenScene):
    def construct(self):
        flask_start = make_urine_flask([0.0, -0.5, 0], height=3.2, darkness_tracker=ValueTracker(1.0))
        stag = scope_tag("schematic")
        self.add(flask_start, stag)

        world, stations, belts, hub, blood, flask = build_carbon_line_world(
            station_labels=("enzyme", "enzyme", "enzyme"),
            station_xs=(-3.8, -1.2, 1.4),
        )
        self.play(
            ReplacementTransform(flask_start, flask),
            FadeIn(belts), FadeIn(stations[0]), FadeIn(stations[1]), FadeIn(stations[2]),
            FadeIn(hub), FadeIn(blood),
            run_time=1.2,
        )

        tf_on = ValueTracker(0.0)
        sxs = (-3.8, -1.2, 1.4)
        flow = add_continuous_upstream(
            -6.0, 4.1, 0.25, sxs, speed=1.45, count=4, scale=1.12,
            stage_fn=lambda x: 0 if tf_on.get_value() < 0.5 else (
                3 if x > sxs[2] + 0.82 else (2 if x > sxs[1] + 0.82 else (1 if x > sxs[0] + 0.82 else 0))
            ),
        )
        self.add(flow)

        self.at("Every enzyme does one step")
        tf_on.set_value(1.0)
        self.play(Indicate(stations[0].box, color=BLUE, scale_factor=1.04), run_time=0.6)

        self.at("vitamin helper")
        tool = make_tool_token("cofactor", color=GREEN).next_to(stations[1].box, UP, buff=0.02)
        self.play(FadeIn(tool, shift=DOWN * 0.35), stations[1].box.animate.set_stroke(GREEN, 3.2), run_time=0.8)

        self.at("fingerprint")
        stamp = make_stamp("cofactor = fingerprint", color=GREEN).move_to([stations[1].box.get_center()[0], 2.75, 0])
        dash = DashedLine(tool.get_top() + UP * 0.06, stamp.get_bottom() + DOWN * 0.06, color=GREEN, stroke_width=2.5)
        self.play(
            Indicate(tool, color=GREEN, scale_factor=1.12),
            Create(dash),
            FadeIn(stamp, scale=0.85),
            run_time=0.9,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 3: Succinyl-CoA Door
class S03Succinyl(SpokenScene):
    def construct(self):
        world, stations, belts, hub, blood, flask = build_carbon_line_world(
            station_labels=("step 1", "biotin enzyme", "B12 enzyme"),
            station_xs=(-3.1, -0.4, 2.3),
            hub_x=4.95, hub_y=0.25, hub_h=2.55,
            lit_idx=2, lit_label="succinyl-CoA",
        )
        self.add(world, scope_tag("schematic"))

        aa_names = ("valine", "isoleucine", "methionine", "threonine")
        aa_ys = (2.05, 1.15, -0.65, -1.55)
        tracks = VGroup()
        aa_chips = VGroup()
        for name, ay in zip(aa_names, aa_ys):
            ch = boxed_label(name, color=BLUE, size=24, pad=0.11, fill_opacity=0.22)
            ch.move_to([-5.25, ay, 0])
            aa_chips.add(ch)
            t_line = Line(ch.get_right() + RIGHT * 0.06, [-4.00, 0.25, 0], color=BLUE, stroke_width=2.2).set_opacity(0.6)
            tracks.add(t_line)

        self.at("Valine")
        self.play(
            Create(tracks),
            LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in aa_chips], lag_ratio=0.25),
            run_time=2.2,
        )

        self.at("broken down")
        self.play(
            *[c.animate.move_to([-4.1, 0.25, 0]).set_opacity(0.0) for c in aa_chips],
            FadeOut(tracks, run_time=0.6),
            run_time=0.9,
        )
        self.remove(aa_chips, tracks)

        prop_block = make_carbon_block(2, scale=1.2)[0].move_to([-1.75, 0.25, 0])
        prop_lab = T("propionyl-CoA", size=24, color=BLUE).move_to([-1.75, -1.35, 0])
        self.play(FadeIn(prop_block), FadeIn(prop_lab), run_time=0.55)

        self.at("biotin enzyme")
        biotin_tok = make_tool_token("biotin", color=GREEN).next_to(stations[1].box, UP, buff=0.02)
        self.play(FadeIn(biotin_tok, shift=DOWN * 0.3), stations[1].box.animate.set_stroke(GREEN, 3.2), run_time=0.7)

        self.at("carboxylates")
        self.play(
            prop_block.animate.move_to([-0.4, 0.25, 0]),
            FadeOut(prop_lab, run_time=0.3),
            run_time=0.65,
        )
        mm_block = make_carbon_block(2, scale=1.2).move_to([0.95, 0.25, 0])
        mm_lab = T("methylmalonyl-CoA", size=24, color=BLUE).move_to([0.95, -1.35, 0])
        self.play(ReplacementTransform(prop_block, mm_block), run_time=0.65)
        self.play(FadeIn(mm_lab), run_time=0.4)

        self.at("B12 enzyme")
        b12_tok = make_tool_token("B12", color=PURPLE).next_to(stations[2].box, UP, buff=0.02)
        self.play(FadeIn(b12_tok, shift=DOWN * 0.3), stations[2].box.animate.set_stroke(PURPLE, 3.2), run_time=0.7)

        self.at("rearranges")
        self.play(
            mm_block.animate.move_to([2.3, 0.25, 0]),
            FadeOut(mm_lab, run_time=0.3),
            run_time=0.65,
        )
        succ_block = make_carbon_block(3, scale=1.2).move_to([3.55, 0.25, 0])
        succ_lab = T("succinyl-CoA", size=24, color=TEAL).move_to([3.3, -1.35, 0])
        self.play(ReplacementTransform(mm_block, succ_block), run_time=0.7)
        self.play(FadeIn(succ_lab), succ_block.animate.move_to([4.5, 0.25, 0]), run_time=0.75)
        self.play(FadeOut(succ_block), Indicate(hub.doors[2], color=TEAL, scale_factor=1.18), run_time=0.45)

        self.at("Biotin means")
        st_bio = make_stamp("carboxylation", color=GREEN).move_to([-0.4, 2.75, 0])
        d_bio = DashedLine(biotin_tok.get_top() + UP * 0.05, st_bio.get_bottom() + DOWN * 0.05, color=GREEN, stroke_width=2.4)
        self.play(FadeOut(succ_lab, run_time=0.2), Create(d_bio), FadeIn(st_bio), run_time=0.65)

        self.at("B12 means")
        st_b12 = make_stamp("rearrangement", color=PURPLE).move_to([2.3, 2.75, 0])
        d_b12 = DashedLine(b12_tok.get_top() + UP * 0.05, st_b12.get_bottom() + DOWN * 0.05, color=PURPLE, stroke_width=2.4)
        self.play(Create(d_b12), FadeIn(st_b12), run_time=0.65)

        sxs = (-3.1, -0.4, 2.3)
        cont = add_continuous_upstream(
            -4.0, 4.15, 0.25, sxs, speed=1.45, count=3, scale=1.15,
            stage_fn=lambda x: 3 if x > sxs[2] + 0.82 else (2 if x > sxs[1] + 0.82 else 1),
        )
        self.add(cont)
        self.finish()


# ------------------------------------------------------------------ Scene 4: Predict
def build_predict_world(jammed=True, creep_speed=0.0):
    """Shared builder for s04_predict and s05_think so the cut is seamless."""
    world, stations, belts, hub, blood, flask = build_carbon_line_world(
        station_labels=("enzyme 1", "defective enzyme" if jammed else "enzyme 2", "enzyme 3"),
        station_xs=(-3.8, -0.6, 2.6),
        line_y=-0.1,
        broken_idx=1 if jammed else None,
    )

    in_panel_box = RoundedRectangle(corner_radius=0.14, width=3.4, height=1.22,
                                    stroke_color=BLUE, stroke_width=2.5, fill_color="#141923", fill_opacity=0.92).move_to([-2.9, 1.9, 0])
    in_head = T("what it takes in", size=26, color=BLUE).move_to([-2.9, 2.22, 0])
    in_tr = ValueTracker(0.02)
    in_bar = make_level_bar([-2.9, 1.58, 0], width=2.8, height=0.32, tracker=in_tr, color=BLUE)
    in_panel = VGroup(in_panel_box, in_head, in_bar)

    out_panel_box = RoundedRectangle(corner_radius=0.14, width=3.4, height=1.22,
                                     stroke_color=GREY, stroke_width=2.5, fill_color="#141923", fill_opacity=0.92).move_to([1.9, 1.9, 0])
    out_head = T("what it makes", size=26, color=TEXT).move_to([1.9, 2.22, 0])
    out_tr = ValueTracker(0.02)
    out_bar = make_level_bar([1.9, 1.58, 0], width=2.8, height=0.32, tracker=out_tr, color=TEAL)
    out_panel = VGroup(out_panel_box, out_head, out_bar)

    creep_blocks = add_continuous_upstream(-6.0, -1.60, -0.1, (-3.8,), speed=max(creep_speed, 0.01), count=4, scale=1.15)

    return world, stations, in_panel, out_panel, in_tr, out_tr, creep_blocks


class S04Predict(SpokenScene):
    def construct(self):
        world, stations, in_panel, out_panel, in_tr, out_tr, creep_blocks = build_predict_world(jammed=False, creep_speed=1.15)
        stag = scope_tag("schematic")
        self.add(world, creep_blocks, stag)

        self.at("jam")
        bad_lab = fit_text("defective enzyme", max_w=2.6, size=24, color=RED, min_size=24, max_lines=2).next_to(stations[1].box, DOWN, buff=0.18)
        for r in stations[1].rollers:
            r.clear_updaters()
        self.play(
            stations[1].box.animate.set_stroke(RED, 3.8),
            *[r[0].animate.set_stroke(RED, 2.5) for r in stations[1].rollers],
            *[r[1].animate.set_color(RED) for r in stations[1].rollers],
            *[r[2].animate.set_color(RED) for r in stations[1].rollers],
            swap(stations[1].label_mob, bad_lab, run_time=0.5),
            run_time=0.6,
        )
        stations[1].label_mob = bad_lab

        self.at("Which will rise")
        q_card = question_card("Which one rises?", y=3.25, color=TEXT, size=34)
        self.play(FadeIn(in_panel, shift=DOWN * 0.15), FadeIn(out_panel, shift=DOWN * 0.15), run_time=0.8)
        self.play(FadeIn(q_card), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 5: Silent 4.5s PredictPause
class S05Think(PredictPause):
    QUESTION = "Which one rises?"
    CARD = {"y": 3.25, "color": TEXT, "size": 34}
    RING_AT = (5.8, 3.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        world, stations, in_panel, out_panel, in_tr, out_tr, creep_blocks = build_predict_world(jammed=True, creep_speed=0.60)
        return VGroup(world, in_panel, out_panel, creep_blocks, scope_tag("schematic"))


# ------------------------------------------------------------------ Scene 6: Answer
class S06Answer(SpokenScene):
    def construct(self):
        world, stations, in_panel, out_panel, in_tr, out_tr, creep_blocks = build_predict_world(jammed=True, creep_speed=1.15)
        cloud_tr = ValueTracker(0.0)
        old_flask = world[-1]
        flask = make_urine_flask(old_flask.get_center(), height=1.50, cloud_tracker=cloud_tr)
        world.submobjects[-1] = flask

        q_card = question_card("Which one rises?", y=3.25, color=TEXT, size=34)
        self.add(world, in_panel, out_panel, creep_blocks, q_card, scope_tag("schematic"))

        heap = make_heap_group(anchor_x=-1.80, base_y=0.14, level_tracker=in_tr, max_cols=3, max_rows=3, color=BLUE)
        self.add(heap)

        self.play(FadeOut(q_card, run_time=0.35), in_panel[0].animate.set_stroke(BLUE, 3.8), run_time=0.45)

        self.at("piles up behind")
        self.play(in_tr.animate.set_value(0.95), run_time=2.5, rate_func=linear)

        self.at("spill out")
        spill_arrow = CurvedArrow([-2.10, 0.05, 0], [-2.10, -1.85, 0], angle=0.5, color=BLUE, stroke_width=3.2)
        blood_stream = add_lane_stream(self, -2.1, 3.8, -2.25, speed=1.65, count=6, color=BLUE)
        self.play(Create(spill_arrow), cloud_tr.animate.set_value(0.85), run_time=1.8)

        self.at("A broken step")
        points_lab = boxed_label("the pile-up points here", color=GOLD, size=26, pad=0.14, fill_opacity=0.20)
        points_lab.move_to([-2.3, 3.15, 0])
        ptr_arrow = Arrow([-2.05, 1.05, 0], [-0.95, 0.55, 0], color=GOLD, stroke_width=3.5, buff=0.05)
        self.play(FadeIn(points_lab), Create(ptr_arrow), Indicate(stations[1].box, color=RED, scale_factor=1.06), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ Scene 7: PKU
class S07Pku(SpokenScene):
    def construct(self):
        world, stations, belts, hub, blood, flask = build_carbon_line_world(
            station_labels=("upstream", "phenylalanine hydroxylase", "downstream"),
            station_xs=(-4.0, -1.1, 1.5),
            line_y=0.35,
            broken_idx=1,
            tags=(None, "PKU", None),
            hub_x=5.0, hub_y=0.35,
            blood_x0=-4.6, blood_y=-2.25,
            flask_pos=(5.05, -2.15, 0),
            label_max_w=(2.4, 3.2, 2.4),
        )
        blood_lvl = ValueTracker(0.25)
        heap_lvl = ValueTracker(0.65)
        heap = make_heap_group(anchor_x=-2.20, base_y=0.58, level_tracker=heap_lvl, max_cols=3, max_rows=3, color=BLUE)
        phe_lab = T("phenylalanine", size=26, color=BLUE).move_to([-2.8, 2.15, 0])
        gauge = make_vertical_gauge([-5.45, -1.90, 0], "blood\nphenylalanine", blood_lvl, color=BLUE, height=1.25)
        blood_blocks = add_lane_stream(self, -4.4, 3.8, -2.25, speed=1.65, count=7, color=BLUE, density_tracker=blood_lvl)
        upstream_flow = add_continuous_upstream(-6.0, -2.4, 0.35, (-4.0,), speed=1.35, count=3, scale=1.15)

        self.add(world, heap, phe_lab, gauge, upstream_flow, scope_tag("schematic"))
        self.play(heap_lvl.animate.set_value(0.95), run_time=2.0, rate_func=linear)

        self.at("rises in the blood")
        self.play(blood_lvl.animate.set_value(0.92), run_time=2.8, rate_func=linear)

        self.at("newborn screening")
        card_box = RoundedRectangle(corner_radius=0.16, width=2.95, height=2.55,
                                    stroke_color=TEXT, stroke_width=2.5, fill_color="#1D222D", fill_opacity=0.95).move_to([4.65, 0.45, 0])
        spot = Circle(radius=0.48, stroke_color=RED, stroke_width=3.0, fill_color="#6E181B", fill_opacity=0.95).move_to([4.65, 0.55, 0])
        card_title = T("dried blood spot", size=24, color=TEXT).move_to([4.65, 1.38, 0])
        flag_tag = boxed_label("flags PKU", color=RED, size=26, pad=0.14, fill_opacity=0.25).move_to([4.65, -0.45, 0])
        feed = Arrow([3.1, -1.85, 0], [4.05, -0.82, 0], color=RED, stroke_width=2.8, buff=0.05)

        self.play(FadeOut(hub), FadeIn(card_box), FadeIn(spot), FadeIn(card_title), Create(feed), run_time=0.9)

        self.at("dried blood spot")
        phe_dots = VGroup(*[
            Dot(radius=0.08, color=BLUE).move_to([4.65 + dx, 0.55 + dy, 0])
            for dx, dy in ((-0.2, 0.14), (0.18, 0.12), (-0.05, -0.18), (0.22, -0.10))
        ])
        self.play(FadeIn(phe_dots), spot.animate.set_stroke(BLUE, 4.0), FadeIn(flag_tag), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ Scene 8: MSUD
class S08Msud(SpokenScene):
    def construct(self):
        cloud_tr = ValueTracker(0.15)
        world, stations, belts, hub, blood, flask = build_carbon_line_world(
            station_labels=("step 1", "branched-chain\nketo-acid dehydrogenase", "step 3"),
            station_xs=(-3.9, -0.8, 2.2),
            line_y=0.35,
            broken_idx=1,
            tags=(None, "MSUD", None),
            hub_x=5.0, hub_y=1.15, hub_h=2.05,
            blood_x0=-4.6, blood_y=-2.25,
            flask_pos=(5.10, -2.15, 0),
            cloud_tr=cloud_tr,
            label_max_w=(2.4, 4.4, 2.4),
        )
        heap_lvl = ValueTracker(0.15)
        heap = make_heap_group(anchor_x=-1.92, base_y=0.58, level_tracker=heap_lvl,
                               max_cols=3, max_rows=3, color=BLUE, dual_shape=True)
        bc_lab = fit_text("branched-chain amino acids\n& keto acids", max_w=4.1, size=24, color=BLUE, min_size=24, max_lines=2)
        bc_lab.move_to([-3.6, 2.35, 0])

        leucine_lvl = ValueTracker(0.30)

        line_grp = VGroup(world, heap)
        line_grp.shift(RIGHT * 0.8)
        self.add(scope_tag("schematic"))
        self.play(line_grp.animate.shift(LEFT * 0.8), run_time=0.75)

        blood_blocks = add_lane_stream(self, -4.4, 3.8, -2.25, speed=1.65, count=7, color=BLUE,
                                       density_tracker=leucine_lvl, pulse_red=False)
        upstream_flow = add_continuous_upstream(-6.0, -2.3, 0.35, (-3.9,), speed=1.35, count=3, scale=1.15)
        self.add(upstream_flow)

        self.at("amino acids")
        self.play(FadeIn(bc_lab), heap_lvl.animate.set_value(0.95), leucine_lvl.animate.set_value(0.85),
                  run_time=2.6, rate_func=linear)

        self.at("smells of maple syrup")
        wisp_t = ValueTracker(0.0)
        wisps = VGroup()
        for k, x_off in enumerate((-0.20, 0.0, 0.20)):
            def _mk_wisp(idx=k, xo=x_off):
                t = wisp_t.get_value()
                ys = np.linspace(-1.25, -0.15, 18)
                xs = 5.10 + xo + 0.14 * np.sin(4.4 * (ys + 1.25) - 2.8 * t + idx * 1.2)
                pts = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
                w = VMobject(stroke_color=GOLD, stroke_width=3.2, stroke_opacity=0.78)
                w.set_points_as_corners(pts)
                return w

            wm = always_redraw(_mk_wisp)
            wisps.add(wm)
        wisps.add_updater(lambda m, dt: wisp_t.increment_value(dt))
        odor_lab = T("maple syrup odor", size=24, color=GOLD).move_to([3.1, -1.25, 0])
        self.add(wisps)
        self.play(cloud_tr.animate.set_value(0.75), FadeIn(odor_lab), run_time=0.9)

        self.at("is neurotoxic")
        gauge = make_vertical_gauge([-5.50, -1.85, 0], "leucine\nexcess", leucine_lvl, color=RED, height=1.25)
        for blk in blood_blocks:
            blk.set_stroke(RED, 2.8)
        self.play(FadeIn(gauge), leucine_lvl.animate.set_value(1.0), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ Scene 9: Ammonia & Astrocyte
class S09Ammonia(SpokenScene):
    def construct(self):
        faint_line = make_conveyor_gaps([-3.0, 0.0, 3.0], -3.15, -6.0, 3.8, station_w=1.1, belt_h=0.18).set_opacity(0.22)
        faint_line.layout_ok = True

        wheel_speed = ValueTracker(1.0)
        wheel = make_urea_wheel([-2.3, 0.75, 0], radius=1.22, speed_tracker=wheel_speed, broken_idx=None)
        wheel_lab = T("urea cycle", size=26, color=GOLD).move_to([-2.3, 2.55, 0])

        amm_cart = boxed_label("ammonium", color=GOLD, size=24, pad=0.14, fill_opacity=0.22).move_to([-5.0, 0.75, 0])
        blood = make_blood_lane(-4.4, 5.2, y=-2.18, h=0.62, show_label=True)

        nh3_lvl = ValueTracker(0.10)
        danger_gauge = make_vertical_gauge([-5.45, -0.80, 0], "danger", nh3_lvl, color=RED, height=1.30)
        nh3_heap = make_heap_group(anchor_x=-4.10, base_y=0.35, level_tracker=nh3_lvl,
                                   max_cols=3, max_rows=3, color=GOLD, scale=0.95)
        ammonia_lab = T("ammonia", size=26, color=GOLD).move_to([-4.35, 1.95, 0])

        self.add(faint_line, wheel, wheel_lab, amm_cart, blood, scope_tag("schematic"))

        self.at("fails")
        bad_wheel = make_urea_wheel([-2.3, 0.75, 0], radius=1.22, speed_tracker=wheel_speed, broken_idx=2)
        self.play(
            wheel_speed.animate.set_value(0.0),
            ReplacementTransform(wheel, bad_wheel),
            FadeOut(amm_cart, run_time=0.3),
            FadeIn(danger_gauge),
            run_time=1.0,
        )
        self.add(nh3_heap)
        self.play(FadeIn(ammonia_lab), nh3_lvl.animate.set_value(0.92), run_time=1.8, rate_func=linear)

        self.at("Astrocytes")
        spill_tokens = add_lane_stream(self, -4.1, 4.9, -2.18, speed=1.65, count=6, color=GOLD)

        swell_tr = ValueTracker(1.0)
        astro_center = np.array([3.1, 0.25, 0.0])

        def _mk_astro():
            sc = swell_tr.get_value()
            pts = []
            for k in range(12):
                ang = k * TAU / 12
                r = (1.18 if k % 2 == 0 else 0.72) * sc
                pts.append(astro_center + np.array([r * np.cos(ang), r * np.sin(ang), 0.0]))
            return Polygon(*pts, stroke_color=TEAL, stroke_width=3.0, fill_color="#172A30", fill_opacity=0.72)

        astro = always_redraw(_mk_astro)
        astro_lab = T("astrocyte", size=26, color=TEAL).move_to([3.1, 2.25, 0])
        glut_chip = boxed_label("glutamine", color=GOLD, size=24, pad=0.08, fill_opacity=0.25).move_to(astro_center)

        self.play(FadeIn(astro), FadeIn(astro_lab), FadeIn(glut_chip), run_time=0.75)
        self.play(swell_tr.animate.set_value(1.25), run_time=1.15)

        self.at("the brain swells")
        brain_tr = ValueTracker(1.0)

        def _mk_brain():
            sc = brain_tr.get_value()
            return RoundedRectangle(
                corner_radius=1.1 * sc, width=3.9 * sc, height=2.85 * sc,
                stroke_color=RED, stroke_width=3.2, fill_opacity=0.0,
            ).move_to(astro_center)

        brain = always_redraw(_mk_brain)
        edema_lab = T("brain edema", size=26, color=RED).move_to([3.1, 2.90, 0])
        self.add(brain)
        self.play(FadeIn(edema_lab), brain_tr.animate.set_value(1.14), run_time=0.95)
        self.finish()


# ------------------------------------------------------------------ Scene 10: Garrod / Alkaptonuria
class S10Garrod(SpokenScene):
    def construct(self):
        wheel_speed = ValueTracker(0.0)
        wheel = make_urea_wheel([-3.8, 2.45, 0], radius=0.68, speed_tracker=wheel_speed, broken_idx=None)

        ox_lvl = ValueTracker(0.0)
        world, stations, belts, hub, blood, flask = build_carbon_line_world(
            station_labels=("step 1", "step 2", "step 3"),
            station_xs=(-4.0, -1.0, 1.9),
            line_y=0.35,
            broken_idx=None,
            hub_x=4.95, hub_y=0.35,
            blood_y=-2.20,
            flask_pos=(5.0, -2.05, 0),
            darkness_tr=ox_lvl,
        )
        upstream_flow = add_continuous_upstream(-6.0, -2.3, 0.35, (-4.0,), speed=1.35, count=3, scale=1.15)
        self.add(wheel, world, upstream_flow, scope_tag("schematic"))
        self.play(wheel_speed.animate.set_value(1.0), run_time=1.1)
        self.play(FadeOut(wheel), run_time=0.45)

        self.at("a molecule called")
        alk_tag = boxed_label("alkaptonuria", color=RED, size=24, pad=0.14, fill_opacity=0.25).next_to(stations[1].box, UP, buff=0.18)
        for r in stations[1].rollers:
            r.clear_updaters()
        heap_lvl = ValueTracker(0.1)
        heap = make_heap_group(anchor_x=-2.10, base_y=0.58, level_tracker=heap_lvl, max_cols=3, max_rows=3, color=BLUE)
        homo_lab = T("homogentisate", size=26, color=BLUE).move_to([-2.9, 2.15, 0])
        self.add(heap)
        self.play(
            stations[1].box.animate.set_stroke(RED, 3.8),
            FadeIn(alk_tag),
            FadeIn(homo_lab),
            heap_lvl.animate.set_value(0.92),
            run_time=1.9,
        )

        self.at("oxidizes")
        spill = add_lane_stream(self, -2.8, 3.65, -2.20, speed=1.65, count=6, color=BLUE)
        self.play(ox_lvl.animate.set_value(1.0), run_time=2.4, rate_func=linear)

        self.at("first recognized")
        trace_path = VMobject(stroke_color=GOLD, stroke_width=3.2)
        trace_path.set_points_as_corners([
            [4.2, -1.45, 0],
            [2.9, -1.45, 0],
            [2.9, 2.45, 0],
            [-1.0, 2.45, 0],
            [-1.0, 1.85, 0],
        ])
        trace_lab = boxed_label("color → station", color=GOLD, size=26, pad=0.14, fill_opacity=0.20).move_to([0.9, 2.95, 0])
        self.play(Create(trace_path), FadeIn(trace_lab), run_time=1.2)

        self.at("as a group")
        rare_dots = VGroup(
            Dot(radius=0.16, color=RED).move_to(stations[0].box.get_top() + UP * 0.25),
            Dot(radius=0.16, color=RED).move_to(stations[2].box.get_top() + UP * 0.25),
        )
        self.play(FadeIn(rare_dots), run_time=0.5)
        self.play(rare_dots.animate.set_opacity(0.25), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ Scene 11: Close (Full World)
class S11Close(SpokenScene):
    def construct(self):
        wheel = make_urea_wheel([-4.1, 2.35, 0], radius=0.72)
        wheel_lab = T("urea wheel", size=24, color=GOLD).next_to(wheel, RIGHT, buff=0.25)

        sxs = (-3.7, -0.9, 1.9)
        s1 = make_station(sxs[0], -0.2, "step 1", w=1.65, h=1.08)
        s2 = make_station(sxs[1], -0.2, "step 2", w=1.65, h=1.08)
        s3 = make_station(sxs[2], -0.2, "step 3", w=1.65, h=1.08)
        belts = make_conveyor_gaps(sxs, -0.2, -5.9, 4.0, station_w=1.65)
        hub = make_seven_doors(4.95, -0.1, height=2.65, width=1.40)
        blood = make_blood_lane(-5.9, 3.8, y=-2.45, h=0.62)
        flask = make_urine_flask([5.05, -2.25, 0], height=1.45, darkness_tracker=ValueTracker(0.2))

        upstream_flow = add_continuous_upstream(-5.9, -2.1, -0.2, (sxs[0],), speed=1.35, count=3, scale=1.12)
        blood_stream = add_lane_stream(self, -5.7, 3.55, -2.45, speed=1.55, count=5, color=BLUE)
        self.add(wheel, wheel_lab, belts, s1, s2, s3, hub, blood, flask, upstream_flow, scope_tag("schematic"))

        self.at("jammed line")
        for r in s2.rollers:
            r.clear_updaters()
        heap_lvl = ValueTracker(0.1)
        heap = make_heap_group(anchor_x=-2.02, base_y=0.05, level_tracker=heap_lvl, max_cols=3, max_rows=3, color=BLUE)
        self.add(heap)
        self.play(
            s2.box.animate.set_stroke(RED, 3.8),
            heap_lvl.animate.set_value(0.95),
            run_time=1.2,
        )

        self.at("Find what")
        glass_ring = Circle(radius=0.55, stroke_color=TEAL, stroke_width=4.5).move_to([-2.3, 0.45, 0])
        glass_handle = Line([-1.92, 0.08, 0], [-1.62, -0.22, 0], color=TEAL, stroke_width=5.5)
        glass = VGroup(glass_ring, glass_handle)
        self.play(FadeIn(glass, scale=0.85), run_time=0.55)

        self.at("broken step")
        broken_lab = T("broken step", size=26, color=RED).move_to([sxs[1], -1.45, 0])
        self.play(
            glass.animate.move_to([sxs[1], -0.2, 0]),
            swap(s2.label_mob, broken_lab, run_time=0.5),
            run_time=0.85,
        )
        s2.label_mob = broken_lab

        self.at("which cofactor")
        bio = make_tool_token("biotin", color=GREEN).next_to(s2.box, UP, buff=0.05)
        b12 = make_tool_token("B12", color=PURPLE).next_to(s3.box, UP, buff=0.05)
        self.play(FadeOut(glass), FadeIn(bio, shift=DOWN * 0.2), FadeIn(b12, shift=DOWN * 0.2), run_time=0.65)
        self.play(Indicate(bio, color=GREEN, scale_factor=1.1), Indicate(b12, color=PURPLE, scale_factor=1.1), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ Scene 12: Standard EndCard
class S12End(EndCard):
    LINE = "A broken step announces itself by what piles up behind it."
