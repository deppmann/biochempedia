"""
================================================================================
FILM PLAN: "The Loop That Makes ATP Alone" (light-reactions__chapter-2)
================================================================================

COLOUR MAP (one colour per concept for the entire film):
- BLUE   (#58C4DD): Photosystem II (PSII), O2 released from water, H+ discs from water
- TEAL   (#3FB8C0): Cytochrome b6f (cyt b6f), H+ discs pumped by b6f
- GREEN  (#83C167): Photosystem I (PSI), NADP+/NADPH block, NADPH bin, NADPH-route links
- GOLD   (#D4A843): Electron beads, ATP synthase, ATP tokens, ATP bin, ATP-route links
- PHOTON (#FF7A52): Red-gold photon waves striking PSII and PSI
- ORANGE (#FF9838): Cyclic electron loop path around PSI and cyt b6f
- GREY   (#8B93A1): Thylakoid membrane band, schematic scope tag, rotor track
- TEXT   (#E8EAF0): Labels, counters, question card, ratio and balance tags

CARRIED WORLD:
A wide schematic thylakoid cross-section filling ~70% of the frame height: stroma
above a horizontal membrane band (y = -0.72..+0.72), lumen below. Four complexes
sit left-to-right across the membrane (PSII, cyt b6f, PSI, ATP synthase with its
14-subunit rotor), NADP+/NADPH sits in the upper-right stroma, and two upright
output bins (NADPH target=2, ATP target=3) sit in the upper-left stroma.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Two GOLD electron beads ride both photon lifts to turn
  NADP+ into NADPH, lumen H+ discs pass through ATP synthase turning its rotor
  to drop an ATP token, and the NADPH bin fills to its target line (2) while the
  ATP bin stalls below its target line (3) under a white "?" and "ATP alone?".
- s02_count: Bins and lumen empty; 4 staggered GOLD beads (1 O2's worth) ride
  the linear path, releasing 1 O2 bubble, 4 BLUE-edged H+ from water + 8
  TEAL-edged H+ from b6f (computed 4 + 4*2 = 12, tracked by lumen H+ counter),
  and filling NADPH bin to 2 while ATP target line 3 highlights.
- s03_rotor: World zooms right onto the 14-subunit ATP synthase rotor (keeping
  bins and membrane visible); H+ discs step into slots turning the ring 1/14
  turn per H+, and a full 360-deg turn pops 3 ATP tokens at even thirds (14 H+ = 3 ATP).
- s04_short: The 12 lumen H+ discs from s02 drive the 14-subunit rotor through
  12/14 * 360 = 308.6 deg, leaving 2 empty slots glowing; ATP bin climbs via
  one ValueTracker to 12 * 3/14 = 2.57 ("about 2.6"), with a bracket showing "about 0.4 short".
- s05_predict: 2 empty rotor slots glow ("2 H+ missing"); camera pans back to
  full cross-section; 1 GOLD bead drops through b6f pumping 2 TEAL-edged H+
  discs; a GOLD bead bobs at ferredoxin above PSI with a crossed-out path to
  NADP+ ("no NADPH") and a blank "?" arrow under "Where can it go?".
- s07_answer: Question dissolves; blank arrow becomes a thick ORANGE loop from
  ferredoxin back to b6f; PSII dims to 40%; bead rides the loop, drops through
  b6f pumping 2 TEAL-edged H+ discs, returns to PSI, and is lifted by a photon.
- s08_rule: H+ discs stream through ATP synthase turning its rotor and linking
  to the ATP bin (GOLD link), linear electron reaches NADPH linking to NADPH bin
  (GREEN link), then the ORANGE loop runs with its bead cycling PSI-b6f and
  ATP bin ticking to 3 while NADPH bin stays still ("protons only").
- s09_mix: 4 linear GOLD beads + 1 cyclic ORANGE-loop bead run together for
  1 O2: lumen H+ counter climbs from 12 to 14 as the loop's 2 H+ arrive, the
  rotor turns a full 360 deg, ATP bin hits 3 while NADPH stays at 2, and the
  computed photon counter (4*2 + 1) steps from 8 to 9 ("about 9 photons").
- s10_arnon: Linear route lights GOLD ("non-cyclic"), then ORANGE loop lights
  ("cyclic") with PSII dark and 1 photon at PSI; a faint dashed "other routes"
  arrow touches the bins as both settle at "3 : 2".
- s11_return: White "?" over ATP bin dissolves into the ORANGE loop; 1 bead
  finishes the linear climb into NADPH, 1 bead circles the loop pumping H+,
  then multiple beads peel off into the loop while linear flow continues and
  both bins stay at their 3 and 2 lines.
================================================================================
"""

from bp_parts import *

PHOTON_COL = "#FF7A52"
ORANGE = "#FF9838"

# Shared coordinates for the full thylakoid cross-section
MEM_TOP = 0.72
MEM_BOT = -0.72
PSII_X = -4.25
B6F_X = -1.25
PSI_X = 1.80
ATPS_X = 5.05

COMP_W = 2.26
COMP_H = 1.64
ATPS_W = 1.90
ATPS_H = 1.74

# Bin geometry (upper-left stroma)
NADPH_BIN_X = -5.65
ATP_BIN_X = -4.15
BIN_BOT_Y = 1.32
UNIT_H = 0.42       # height per molecule: 2 -> 0.84, 3 -> 1.26
BIN_W = 0.72
BIN_H = 1.46        # holds up to ~3.48

# Complex interior channel x-positions (for invisible bead motion trajectories)
PSII_CH_X = -3.42
B6F_CH_X = -0.42
PSI_CH_X = 2.55
FD_POS = np.array([1.80, 1.38, 0.0])
NADP_POS = np.array([3.85, 2.38, 0.0])


def make_membrane(x0=-6.35, x1=6.35, y_top=MEM_TOP, y_bot=MEM_BOT, gaps=None):
    """Membrane band with lines routed cleanly between complexes (no straddling)."""
    band = Rectangle(
        width=x1 - x0, height=y_top - y_bot,
        stroke_width=0, fill_color=GREY, fill_opacity=0.11,
    ).move_to([(x0 + x1) / 2, (y_top + y_bot) / 2, 0])
    g = VGroup(band)
    if not gaps:
        spans = [(x0, x1)]
    else:
        spans = []
        cur = x0
        for a, b in sorted(gaps):
            if a > cur:
                spans.append((cur, a))
            cur = max(cur, b)
        if cur < x1:
            spans.append((cur, x1))
    for a, b in spans:
        g.add(Line([a, y_top, 0], [b, y_top, 0], color=GREY, stroke_width=2.5))
        g.add(Line([a, y_bot, 0], [b, y_bot, 0], color=GREY, stroke_width=2.5))
    return g


def FULL_MEM_GAPS():
    return [
        (PSII_X - COMP_W / 2, PSII_X + COMP_W / 2),
        (B6F_X - COMP_W / 2, B6F_X + COMP_W / 2),
        (PSI_X - COMP_W / 2, PSI_X + COMP_W / 2),
        (ATPS_X - ATPS_W / 2, ATPS_X + ATPS_W / 2),
    ]


def make_complex(x, title, color, width=COMP_W, height=COMP_H, label_size=24):
    """Build complex box + label shifted slightly left so right interior channel stays clear."""
    box = RoundedRectangle(
        corner_radius=0.16, width=width, height=height,
        stroke_color=color, stroke_width=2.8,
        fill_color=color, fill_opacity=0.16,
    ).move_to([x, 0.0, 0.0])
    lab = T(title, size=label_size, color=color, line_spacing=0.85).move_to(box.get_center() + LEFT * 0.08)
    return box, lab


def make_rotor_ring(center, radius=0.45, n_slots=14, angle_tracker=None, filled_count=0,
                    empty_glow=False, slot_r=None, stroke_w=2.4):
    """Build a 14-slot schematic rotor ring (no molecular structure)."""
    c = np.array(center, dtype=float)
    sr = slot_r if slot_r is not None else radius * 0.14
    outer = Circle(radius=radius + sr * 1.35, color=GOLD, stroke_width=stroke_w,
                   fill_color=GOLD, fill_opacity=0.08).move_to(c)
    inner = Circle(radius=max(0.12, radius - sr * 1.45), color=GOLD, stroke_width=max(1.8, stroke_w * 0.8),
                   fill_color=BG, fill_opacity=0.85).move_to(c)

    def build_slots():
        theta = angle_tracker.get_value() if angle_tracker is not None else 0.0
        n_fill = int(round(filled_count.get_value())) if isinstance(filled_count, ValueTracker) else int(filled_count)
        g = VGroup()
        for i in range(n_slots):
            ang = PI / 2 - i * TAU / n_slots + theta
            pt = c + radius * np.array([np.cos(ang), np.sin(ang), 0.0])
            is_filled = i < n_fill
            if is_filled:
                dot = Circle(radius=sr, color=TEAL if i % 3 != 0 else BLUE, stroke_width=2.2,
                             fill_color=GOLD, fill_opacity=0.85).move_to(pt)
            elif empty_glow:
                dot = Circle(radius=sr * 1.12, color=PHOTON_COL, stroke_width=3.0,
                             fill_color=PHOTON_COL, fill_opacity=0.28).move_to(pt)
            else:
                dot = Circle(radius=sr, color=GOLD, stroke_width=1.8,
                             fill_color=BG, fill_opacity=0.9).move_to(pt)
            g.add(dot)
        return g

    if angle_tracker is not None or isinstance(filled_count, ValueTracker):
        slots = always_redraw(build_slots)
    else:
        slots = build_slots()
    return VGroup(outer, inner, slots)


def make_atp_synthase(x=ATPS_X, angle_tracker=None, filled_count=0, empty_glow=False):
    box = RoundedRectangle(
        corner_radius=0.16, width=ATPS_W, height=ATPS_H,
        stroke_color=GOLD, stroke_width=2.8,
        fill_color=GOLD, fill_opacity=0.14,
    ).move_to([x, 0.0, 0.0])
    rotor = make_rotor_ring([x, 0.0, 0.0], radius=0.48, n_slots=14,
                            angle_tracker=angle_tracker, filled_count=filled_count,
                            empty_glow=empty_glow, slot_r=0.065, stroke_w=2.0)
    lab = T("ATP synthase", size=24, color=GOLD).move_to([x, -1.20, 0.0])
    return VGroup(box, rotor, lab)


def make_bin(x, name, color, target_val, tracker, fmt="{:.0f}"):
    """An upright bar bin with a dashed target line and live value counter."""
    y_mid = BIN_BOT_Y + BIN_H / 2
    outline = RoundedRectangle(
        corner_radius=0.08, width=BIN_W, height=BIN_H,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=0.06,
    ).move_to([x, y_mid, 0.0])

    def mk_fill():
        val = max(0.0, min(3.35, tracker.get_value()))
        h = val * UNIT_H
        if h < 0.02:
            return VMobject()
        r = Rectangle(
            width=BIN_W - 0.08, height=h,
            stroke_width=0, fill_color=color, fill_opacity=0.72,
        )
        r.move_to([x, BIN_BOT_Y + 0.03 + h / 2, 0.0])
        return r

    fill = always_redraw(mk_fill)
    ty = BIN_BOT_Y + 0.03 + target_val * UNIT_H
    tline = DashedLine([x - BIN_W / 2 - 0.08, ty, 0], [x + BIN_W / 2 + 0.08, ty, 0],
                       color=color, stroke_width=3.0, dash_length=0.10)
    tlab = M(f"{target_val:g}", size=24, color=color).next_to(
        tline, LEFT if x < -4.8 else RIGHT, buff=0.12
    )
    name_lab = T(name, size=24, color=color).move_to([x, BIN_BOT_Y - 0.28, 0.0])
    val_lab = always_redraw(lambda: M(
        fmt(tracker.get_value()) if callable(fmt) else fmt.format(tracker.get_value()),
        size=24, color=color,
    ).move_to([x, BIN_BOT_Y + BIN_H + 0.26, 0.0]))
    return VGroup(outline, fill, tline, tlab, name_lab, val_lab)


def make_h_disc(source="b6f", radius=0.20):
    """H+ disc: BLUE-edged when from water, TEAL-edged when pumped at b6f."""
    col = BLUE if source == "water" else TEAL
    circ = Circle(radius=radius, color=col, stroke_width=3.0, fill_color=BG, fill_opacity=0.95)
    txt = T("+", size=22, color=col, weight=BOLD).move_to(circ)
    return VGroup(circ, txt)


def make_lumen_particles(seed=7, n=10, x_range=(-6.0, 3.8), y_range=(-2.10, -1.30)):
    """Lumen protons gently drifting (carried across scenes, clear of counters)."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        src = "water" if i % 3 == 0 else "b6f"
        col = BLUE if src == "water" else TEAL
        d = Dot(radius=0.095, color=col).set_opacity(0.75)
        d.move_to([rng.uniform(*x_range), rng.uniform(*y_range), 0.0])
        vx = rng.uniform(-0.28, 0.28)
        vy = rng.uniform(-0.14, 0.14)

        def drift(m, dt, vx=vx, vy=vy, xr=x_range, yr=y_range):
            m.shift([vx * dt, vy * dt, 0.0])
            p = m.get_center()
            if p[0] < xr[0]:
                m.set_x(xr[1])
            elif p[0] > xr[1]:
                m.set_x(xr[0])
            if p[1] < yr[0]:
                m.set_y(yr[1])
            elif p[1] > yr[0]:
                pass
            if p[1] < yr[0]:
                m.set_y(yr[1])
            elif p[1] > yr[1]:
                m.set_y(yr[0])

        d.add_updater(drift)
        g.add(d)
    return g


def make_photon_wave(start, end, color=PHOTON_COL):
    """Wavy photon arrow (no molecular structure)."""
    p0 = np.array(start, dtype=float)
    p1 = np.array(end, dtype=float)
    v = p1 - p0
    L = np.linalg.norm(v)
    u = v / max(L, 1e-6)
    perp = np.array([-u[1], u[0], 0.0])
    ts = np.linspace(0, 1, 36)
    pts = [p0 + t * v + perp * 0.11 * np.sin(t * 5 * PI) * (1 - 0.3 * t) for t in ts]
    wave = VMobject(stroke_color=color, stroke_width=4.0, fill_opacity=0).set_points_as_corners(pts)
    tip = Arrow(p0 + 0.72 * v, p1, buff=0, color=color, stroke_width=4.0,
                max_tip_length_to_length_ratio=0.55)
    return VGroup(wave, tip)


def linear_bead_points():
    """Trajectory for moving GOLD electron beads: routed along complex channels clear of labels."""
    return [
        np.array([PSII_X + 0.98, -0.68, 0.0]),
        np.array([PSII_X + 0.98, 0.64, 0.0]),
        np.array([PSII_X + COMP_W / 2, 0.45, 0.0]),
        np.array([B6F_X - COMP_W / 2, 0.45, 0.0]),
        np.array([B6F_X + 0.98, 0.62, 0.0]),
        np.array([B6F_X + 0.98, -0.62, 0.0]),
        np.array([B6F_X + COMP_W / 2, -0.45, 0.0]),
        np.array([PSI_X - COMP_W / 2, -0.45, 0.0]),
        np.array([PSI_X + 0.98, -0.62, 0.0]),
        np.array([PSI_X + 0.98, 0.72, 0.0]),
        FD_POS,
        np.array([2.88, 1.94, 0.0]),
    ]


def linear_bridges(color=GOLD, opacity=0.40, width=3.5):
    """Visible linear-route connectors between complex edges (never straddling boxes or text)."""
    seg1 = Line([PSII_X + COMP_W / 2, 0.45, 0], [B6F_X - COMP_W / 2, 0.45, 0],
                stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    seg2 = Line([B6F_X + COMP_W / 2, -0.45, 0], [PSI_X - COMP_W / 2, -0.45, 0],
                stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    seg3 = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    seg3.set_points_as_corners([
        np.array([PSI_X, 0.82, 0.0]),
        FD_POS,
        np.array([3.35, 2.08, 0.0]),
    ])
    return VGroup(seg1, seg2, seg3)


def cyclic_arc_only(color=ORANGE, width=6.0, opacity=1.0):
    """Upper return arc from Fd back left to b6f top edge."""
    p_fd = FD_POS
    p_arc1 = np.array([0.85, 2.05, 0.0])
    p_arc2 = np.array([-0.25, 1.92, 0.0])
    p_b6f_top = np.array([B6F_X, 0.82, 0.0])
    ts = np.linspace(0, 1, 24)
    arc_pts = [
        (1 - t) ** 3 * p_fd + 3 * (1 - t) ** 2 * t * p_arc1 + 3 * (1 - t) * t ** 2 * p_arc2 + t ** 3 * p_b6f_top
        for t in ts
    ]
    c = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    c.set_points_as_corners(arc_pts)
    return c


def cyclic_visible_bridges(color=ORANGE, width=6.0, opacity=1.0):
    """Visible ORANGE cyclic connectors: upper arc (Fd -> b6f top), lower bridge (b6f -> PSI), PSI top -> Fd."""
    arc = cyclic_arc_only(color=color, width=width, opacity=opacity)
    bot = Line([B6F_X + COMP_W / 2, -0.52, 0], [PSI_X - COMP_W / 2, -0.52, 0],
               stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    up = Line([PSI_X, 0.82, 0], FD_POS,
              stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    return VGroup(arc, bot, up)


def cyclic_bead_points():
    """Closed loop waypoints for moving GOLD beads around the cyclic route (clear of centered labels)."""
    p_fd = FD_POS
    p_arc1 = np.array([0.85, 2.05, 0.0])
    p_arc2 = np.array([-0.25, 1.92, 0.0])
    p_b6f_top = np.array([B6F_X, 0.82, 0.0])
    ts = np.linspace(0, 1, 24)
    arc_pts = [
        (1 - t) ** 3 * p_fd + 3 * (1 - t) ** 2 * t * p_arc1 + 3 * (1 - t) * t ** 2 * p_arc2 + t ** 3 * p_b6f_top
        for t in ts
    ]
    return arc_pts + [
        np.array([B6F_X + 0.98, 0.64, 0.0]),
        np.array([B6F_X + 0.98, -0.62, 0.0]),
        np.array([PSI_X - 0.98, -0.62, 0.0]),
        np.array([PSI_X + 0.98, -0.62, 0.0]),
        np.array([PSI_X + 0.98, 0.72, 0.0]),
        FD_POS,
    ]


def cyclic_bead_path():
    """Invisible closed loop trajectory for moving GOLD beads around the cyclic route."""
    c = VMobject(fill_opacity=0)
    c.set_points_as_corners(cyclic_bead_points())
    return c


def build_base_world(nadph_t, atp_t, nadph_text="NADP+", atp_fmt="{:.0f}",
                     rotor_angle=None, rotor_filled=0, rotor_glow=False):
    mem = make_membrane(gaps=FULL_MEM_GAPS())
    stroma_lab = T("stroma", size=24, color=TEXT).move_to([5.80, 2.48, 0.0])
    lumen_lab = T("lumen", size=24, color=TEXT).move_to([5.65, -2.18, 0.0])
    psii_box, psii_lab = make_complex(PSII_X, "Photosystem\nII", BLUE)
    b6f_box, b6f_lab = make_complex(B6F_X, "cytochrome\nb6f", TEAL)
    psi_box, psi_lab = make_complex(PSI_X, "Photosystem\nI", GREEN)
    atps = make_atp_synthase(ATPS_X, angle_tracker=rotor_angle, filled_count=rotor_filled, empty_glow=rotor_glow)
    nadp_box = chip(nadph_text, color=GREEN, size=26, pad=0.22).move_to(NADP_POS)
    bin_nadph = make_bin(NADPH_BIN_X, "NADPH", GREEN, 2, nadph_t)
    bin_atp = make_bin(ATP_BIN_X, "ATP", GOLD, 3, atp_t, fmt=atp_fmt)
    lumen_dots = make_lumen_particles()
    tag = scope_tag("schematic", size=24, color=TEXT)
    world = VGroup(
        mem, stroma_lab, lumen_lab,
        psii_box, psii_lab, b6f_box, b6f_lab, psi_box, psi_lab,
        atps, nadp_box, bin_nadph, bin_atp, lumen_dots, tag,
    )
    return world, {
        "mem": mem, "stroma_lab": stroma_lab, "lumen_lab": lumen_lab,
        "psii_box": psii_box, "psii_lab": psii_lab, "psii": VGroup(psii_box, psii_lab),
        "b6f_box": b6f_box, "b6f_lab": b6f_lab, "b6f": VGroup(b6f_box, b6f_lab),
        "psi_box": psi_box, "psi_lab": psi_lab, "psi": VGroup(psi_box, psi_lab),
        "atps": atps, "nadp_box": nadp_box,
        "bin_nadph": bin_nadph, "bin_atp": bin_atp,
        "lumen_dots": lumen_dots, "tag": tag,
    }


def poly_pos(pts, alpha):
    n = len(pts) - 1
    s = (alpha % 1.0) * n
    i = min(n - 1, int(s))
    f = s - i
    return (1 - f) * pts[i] + f * pts[i + 1]


def make_electron_bead(radius=0.14, halo=False):
    """GOLD electron bead (optionally with a soft filled glow halo, no outline to straddle boxes)."""
    d = Dot(radius=radius, color=GOLD)
    if not halo:
        return d
    ring = Dot(radius=radius * 2.0, color=GOLD).set_opacity(0.28)
    return VGroup(ring, d)


def start_bead_flow(pts, n_beads=3, speed=0.24, radius=0.14, color=GOLD, opacity=1.0, halo=False):
    """Return a VGroup of beads continuously riding a polyline trajectory."""
    g = VGroup()
    for i in range(n_beads):
        b = make_electron_bead(radius=radius, halo=halo)
        if not halo:
            b.set_color(color).set_opacity(opacity)
        b._ph = i / n_beads
        b.move_to(poly_pos(pts, b._ph))

        def step(m, dt, sp=speed, p=pts):
            m._ph = (m._ph + sp * dt) % 1.0
            m.move_to(poly_pos(p, m._ph))

        b.add_updater(step)
        g.add(b)
    return g


# ==============================================================================
# SCENES
# ==============================================================================

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(0.0)
        atp_t = ValueTracker(0.0)
        rotor_ang = ValueTracker(0.0)
        world, parts = build_base_world(
            nadph_t, atp_t,
            atp_fmt=lambda v: "~2" if 1.6 <= v <= 2.1 else f"{v:.0f}",
            rotor_angle=rotor_ang, rotor_filled=10,
        )
        bins = VGroup(parts["bin_nadph"], parts["bin_atp"])
        world.remove(parts["bin_nadph"], parts["bin_atp"])
        guide = linear_bridges(opacity=0.35)
        self.add(world, guide, rotor_ang)

        pts = linear_bead_points()
        seg_a = VMobject().set_points_as_corners(pts[:5])
        seg_b = VMobject().set_points_as_corners(pts[4:10])
        seg_c = VMobject().set_points_as_corners(pts[9:])

        b1 = Dot(radius=0.14, color=GOLD).move_to(pts[0])
        b2 = Dot(radius=0.14, color=GOLD).move_to(pts[0])
        pw1 = make_photon_wave([-2.75, 1.55, 0], [PSII_X + 0.55, 0.86, 0])
        pw2 = make_photon_wave([0.95, 1.55, 0], [PSI_X, 0.86, 0])

        self.add(b1)
        self.play(FadeIn(pw1, run_time=0.2))
        self.play(MoveAlongPath(b1, seg_a, run_time=1.4), FadeOut(pw1, run_time=0.5))

        h_w1 = make_h_disc("water", radius=0.20).move_to([PSII_X, -1.10, 0])
        h_b1 = make_h_disc("b6f", radius=0.20).move_to([B6F_X - 0.35, -1.10, 0])
        h_b2 = make_h_disc("b6f", radius=0.20).move_to([B6F_X + 0.35, -1.10, 0])
        self.add(b2, h_w1)
        self.play(
            MoveAlongPath(b1, seg_b, run_time=1.5),
            MoveAlongPath(b2, seg_a, run_time=1.5),
            h_w1.animate.move_to([-2.7, -1.65, 0]),
            FadeIn(pw2, run_time=0.25),
        )
        self.add(h_b1, h_b2)
        nadph_new = chip("NADPH", color=GREEN, size=26, pad=0.22).move_to(NADP_POS)
        self.play(
            MoveAlongPath(b1, seg_c, run_time=1.3),
            MoveAlongPath(b2, VMobject().set_points_as_corners(pts[4:]), run_time=1.6),
            FadeOut(pw2, run_time=0.5),
            h_b1.animate.move_to([-0.1, -1.65, 0]),
            h_b2.animate.move_to([1.2, -1.65, 0]),
        )
        self.play(
            FadeOut(b1, run_time=0.2),
            FadeOut(b2, run_time=0.2),
            swap(parts["nadp_box"], nadph_new, run_time=0.6),
        )
        parts["nadp_box"] = nadph_new

        # "The protons left behind make ATP."
        self.at("protons left behind")
        atp_tok = chip("ATP", color=GOLD, size=24, pad=0.16).move_to([ATPS_X, 1.30, 0])
        self.play(
            h_w1.animate.move_to([2.4, -1.65, 0]),
            h_b1.animate.move_to([3.0, -1.35, 0]),
            h_b2.animate.move_to([3.6, -1.05, 0]),
            rotor_ang.animate.set_value(-TAU * 0.5),
            run_time=1.2,
        )
        self.play(
            FadeOut(h_w1, run_time=0.25),
            FadeOut(h_b1, run_time=0.25),
            FadeOut(h_b2, run_time=0.25),
            rotor_ang.animate.set_value(-TAU),
            FadeIn(atp_tok, shift=UP * 0.25, run_time=0.6),
        )
        self.play(atp_tok.animate.move_to([ATPS_X, 1.80, 0]).set_opacity(0), run_time=0.7)
        self.remove(atp_tok)

        # "But the Calvin cycle needs more ATP than that."
        self.at("Calvin cycle needs more")
        # Keep gentle electron flow running so the scene stays alive while bins fill and question lands
        flow = start_bead_flow(pts, n_beads=2, speed=0.22, radius=0.12)
        self.add(flow)
        self.play(FadeIn(bins, shift=UP * 0.15), run_time=0.55)
        self.play(
            nadph_t.animate.set_value(2.0),
            atp_t.animate.set_value(1.85),
            rotor_ang.animate.set_value(-1.6 * TAU),
            run_time=2.2,
        )

        # "How can a leaf make ATP alone?"
        self.at("How can a leaf")
        q_mark = T("?", size=36, color=TEXT, weight=BOLD).move_to([ATP_BIN_X, 3.52, 0])
        head_q = T("ATP alone?", size=38, color=TEXT, weight=BOLD).move_to([0.4, 3.28, 0])
        self.play(
            FadeIn(q_mark, shift=DOWN * 0.1),
            FadeIn(head_q, shift=DOWN * 0.1),
            rotor_ang.animate.set_value(-2.2 * TAU),
            run_time=1.8,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(1.85)
        rotor_ang = ValueTracker(0.0)
        world, parts = build_base_world(
            nadph_t, atp_t, nadph_text="NADPH",
            atp_fmt=lambda v: "~2",
            rotor_angle=rotor_ang, rotor_filled=10,
        )
        guide = linear_bridges(opacity=0.35)
        q_mark = T("?", size=36, color=TEXT, weight=BOLD).move_to([ATP_BIN_X, 3.52, 0])
        head_q = T("ATP alone?", size=38, color=TEXT, weight=BOLD).move_to([0.4, 3.28, 0])
        title = T("The Loop That Makes ATP Alone", size=38, font=TITLE_FONT, color=TEXT).move_to([0.6, 3.32, 0])
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.10)

        queue_beads = start_bead_flow(linear_bead_points(), n_beads=3, speed=0.18, radius=0.11, opacity=0.45)
        rotor_ang.add_updater(lambda m, dt: m.increment_value(-0.6 * dt))

        self.add(world, guide, queue_beads, rotor_ang, q_mark, head_q)
        self.play(
            FadeOut(q_mark, run_time=0.45),
            FadeOut(head_q, run_time=0.45),
        )
        self.play(
            FadeIn(title, shift=UP * 0.08, run_time=0.6),
            GrowFromCenter(rule, run_time=0.6),
        )
        self.finish()


class S02Count(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(1.85)
        h_count = ValueTracker(0.0)
        world, parts = build_base_world(nadph_t, atp_t, nadph_text="NADPH", atp_fmt=lambda v: "~2" if v > 0.5 else "0")
        guide = linear_bridges(opacity=0.35)
        title = T("The Loop That Makes ATP Alone", size=38, font=TITLE_FONT, color=TEXT).move_to([0.6, 3.32, 0])
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.10)
        h_counter = counter("lumen H+: {:.0f}", h_count, at=[-1.25, -2.75, 0], size=28, color=TEAL)

        self.add(world, guide, title, rule)
        nadp_reset = chip("NADP+", color=GREEN, size=26, pad=0.22).move_to(NADP_POS)
        self.play(
            FadeOut(title, run_time=0.4),
            FadeOut(rule, run_time=0.4),
            nadph_t.animate.set_value(0.0),
            atp_t.animate.set_value(0.0),
            swap(parts["nadp_box"], nadp_reset, run_time=0.5),
            FadeIn(h_counter, run_time=0.4),
        )
        parts["nadp_box"] = nadp_reset

        # "Linear flow makes 2 NADPH and leaves 12 protons in the lumen."
        self.at("Linear flow makes")
        o2_bub = VGroup(
            Circle(radius=0.34, color=BLUE, stroke_width=2.8, fill_color=BLUE, fill_opacity=0.15),
            T("O2", size=24, color=BLUE, weight=BOLD),
        )
        o2_bub[1].move_to(o2_bub[0])
        o2_bub.move_to([PSII_X, -1.28, 0])
        self.play(FadeIn(o2_bub, scale=0.7, run_time=0.35))
        self.play(o2_bub.animate.move_to([-5.65, -2.25, 0]), run_time=0.7)

        # Replay 4 GOLD beads sequentially (1 O2's worth -> 4 water H+ + 8 b6f H+ = 12 H+)
        pts = linear_bead_points()
        full_path = VMobject().set_points_as_corners(pts)
        water_spots = [[-4.4, -1.88, 0], [-3.8, -1.88, 0], [-4.4, -1.32, 0], [-3.8, -1.32, 0]]
        b6f_spots = [
            [-2.4, -1.88, 0], [-1.85, -1.88, 0], [-1.3, -1.88, 0], [-0.75, -1.88, 0],
            [-2.4, -1.32, 0], [-1.85, -1.32, 0], [-1.3, -1.32, 0], [-0.75, -1.32, 0],
        ]
        for k in range(4):
            bead = Dot(radius=0.14, color=GOLD).move_to(pts[0])
            pw_ps2 = make_photon_wave([-2.75, 1.55, 0], [PSII_X + 0.55, 0.86, 0])
            hw = make_h_disc("water", radius=0.20).move_to([PSII_X, -1.05, 0])
            hb1 = make_h_disc("b6f", radius=0.20).move_to([B6F_X - 0.50, -1.05, 0])
            hb2 = make_h_disc("b6f", radius=0.20).move_to([B6F_X + 0.50, -1.05, 0])
            self.add(bead, hw, hb1, hb2)
            self.play(
                FadeIn(pw_ps2, run_time=0.15),
                MoveAlongPath(bead, full_path, run_time=0.98, rate_func=linear),
                hw.animate(run_time=0.88).move_to(water_spots[k]),
                hb1.animate(run_time=0.88).move_to(b6f_spots[2 * k]),
                hb2.animate(run_time=0.88).move_to(b6f_spots[2 * k + 1]),
                h_count.animate(run_time=0.88).set_value(3 * (k + 1)),
                nadph_t.animate(run_time=0.92).set_value(0.5 * (k + 1)),
            )
            self.remove(pw_ps2, bead)

        nadph_done = chip("NADPH", color=GREEN, size=26, pad=0.22).move_to(NADP_POS)
        self.play(swap(parts["nadp_box"], nadph_done, run_time=0.5))

        # "The Calvin cycle spends 3 ATP for every 2 NADPH."
        self.at("Calvin cycle spends")
        atp_tline_hi = DashedLine(
            [ATP_BIN_X - BIN_W / 2 - 0.12, BIN_BOT_Y + 0.03 + 3 * UNIT_H, 0],
            [ATP_BIN_X + BIN_W / 2 + 0.12, BIN_BOT_Y + 0.03 + 3 * UNIT_H, 0],
            color=YELLOW, stroke_width=5.5, dash_length=0.10,
        )
        calvin_tag = boxed_label("Calvin cycle: 3 ATP : 2 NADPH", color=GOLD, size=26).move_to([-0.5, 2.75, 0])
        flow = start_bead_flow(pts, n_beads=2, speed=0.22, radius=0.11, opacity=0.65)
        self.add(flow)
        self.play(FadeIn(atp_tline_hi, run_time=0.4), FadeIn(calvin_tag, shift=DOWN * 0.1, run_time=0.5))
        self.finish()


class S03Rotor(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(0.0)
        rotor_ang = ValueTracker(0.0)
        rotor_fill = ValueTracker(0.0)

        RC = np.array([2.0, 0.0, 0.0])
        BOX_W, BOX_H = 3.9, 3.7
        mem = make_membrane(x0=-6.35, x1=6.35, y_top=0.55, y_bot=-0.55, gaps=[(RC[0] - BOX_W / 2, RC[0] + BOX_W / 2)])
        bin_nadph = make_bin(NADPH_BIN_X, "NADPH", GREEN, 2, nadph_t)
        bin_atp = make_bin(ATP_BIN_X, "ATP", GOLD, 3, atp_t)
        bins = VGroup(bin_nadph, bin_atp)

        rotor_ring = make_rotor_ring(RC, radius=1.40, n_slots=14, angle_tracker=rotor_ang,
                                     filled_count=rotor_fill, slot_r=0.17, stroke_w=3.2)
        atp_box = RoundedRectangle(
            corner_radius=0.22, width=BOX_W, height=BOX_H,
            stroke_color=GOLD, stroke_width=3.0, fill_color=GOLD, fill_opacity=0.07,
        ).move_to(RC)
        sub_label = T("14 subunits", size=30, color=GOLD, weight=BOLD).move_to([2.0, 2.40, 0])
        cap_tag = T("14 H+ = 3 ATP", size=30, color=GOLD, weight=BOLD).move_to([2.0, -2.42, 0])
        stroma_l = T("stroma", size=24, color=TEXT).move_to([-1.5, 1.05, 0])
        lumen_l = T("lumen", size=24, color=TEXT).move_to([-1.5, -1.05, 0])
        lumen_dots = make_lumen_particles(seed=11, n=8, x_range=(-6.0, -0.3), y_range=(-2.65, -1.45))
        tag = scope_tag("schematic", size=24, color=TEXT)

        self.add(mem, bins, atp_box, rotor_ring, stroma_l, lumen_l, lumen_dots, tag)
        rotor_ring.save_state()
        atp_box.save_state()
        rotor_ring.scale(0.55).move_to([4.5, 0.0, 0])
        atp_box.scale(0.55).move_to([4.5, 0.0, 0])
        self.play(rotor_ring.animate.restore(), atp_box.animate.restore(), run_time=1.4)

        # "Its rotor has 14 subunits"
        self.at("Its rotor has")
        self.play(FadeIn(sub_label, shift=DOWN * 0.1, run_time=0.5))

        # "each carrying one proton across per turn"
        self.at("each carrying one proton")
        for i in range(3):
            hd = make_h_disc("b6f" if i < 2 else "water", radius=0.20).move_to([-0.5, -1.95, 0])
            self.add(hd)
            self.play(hd.animate.move_to([RC[0], -2.15, 0]), run_time=0.45)
            self.remove(hd)
            self.play(
                rotor_fill.animate.set_value(i + 1),
                rotor_ang.animate.set_value(-(i + 1) * TAU / 14.0),
                run_time=0.45,
            )

        # "One full turn makes three ATP"
        self.at("One full turn makes")
        ghost_arc = Arc(radius=1.72, start_angle=PI / 2, angle=-TAU * 0.98, arc_center=RC,
                        color=YELLOW, stroke_width=4.5)
        toks = VGroup(
            chip("ATP", color=GOLD, size=26, pad=0.16).move_to([5.1, 2.55, 0]),
            chip("ATP", color=GOLD, size=26, pad=0.16).move_to([5.1, 1.80, 0]),
            chip("ATP", color=GOLD, size=26, pad=0.16).move_to([5.1, 1.08, 0]),
        )
        self.play(
            Create(ghost_arc, run_time=2.2),
            rotor_fill.animate(run_time=2.2).set_value(14),
            rotor_ang.animate(run_time=2.2).set_value(-TAU),
            LaggedStart(FadeIn(toks[0]), FadeIn(toks[1]), FadeIn(toks[2]), lag_ratio=0.35, run_time=2.2),
        )

        # "So 14 protons buy three."
        self.at("So 14 protons")
        self.play(FadeIn(cap_tag, shift=UP * 0.1, run_time=0.45))
        self.wait(0.4)

        # Return the ring to its start before the scene ends
        self.play(
            FadeOut(ghost_arc, run_time=0.4),
            FadeOut(toks, run_time=0.4),
            rotor_fill.animate(run_time=0.7).set_value(0),
            rotor_ang.animate(run_time=0.7).set_value(0.0),
        )
        self.finish()


class S04Short(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        filled_t = ValueTracker(0.0)
        atp_t = ValueTracker(0.0)
        rotor_ang = ValueTracker(0.0)
        h_rem_t = ValueTracker(12.0)

        RC = np.array([2.0, 0.0, 0.0])
        BOX_W, BOX_H = 3.9, 3.7
        mem = make_membrane(x0=-6.35, x1=6.35, y_top=0.55, y_bot=-0.55, gaps=[(RC[0] - BOX_W / 2, RC[0] + BOX_W / 2)])
        bin_nadph = make_bin(NADPH_BIN_X, "NADPH", GREEN, 2, nadph_t)
        bin_atp = make_bin(
            ATP_BIN_X, "ATP", GOLD, 3, atp_t,
            fmt=lambda v: "about 2.6" if abs(v - 12 * 3 / 14) < 0.08 else f"{v:.1f}",
        )
        atp_box = RoundedRectangle(
            corner_radius=0.22, width=BOX_W, height=BOX_H,
            stroke_color=GOLD, stroke_width=3.0, fill_color=GOLD, fill_opacity=0.07,
        ).move_to(RC)
        rotor_ring = make_rotor_ring(RC, radius=1.40, n_slots=14, angle_tracker=rotor_ang,
                                     filled_count=filled_t, empty_glow=False, slot_r=0.17, stroke_w=3.2)
        sub_label = T("14 subunits", size=30, color=GOLD, weight=BOLD).move_to([2.0, 2.40, 0])
        h_rem = counter("lumen H+: {:.0f}", h_rem_t, at=[-1.5, -2.55, 0], size=28, color=TEAL)
        stroma_l = T("stroma", size=24, color=TEXT).move_to([-1.5, 1.05, 0])
        lumen_l = T("lumen", size=24, color=TEXT).move_to([-1.5, -1.05, 0])
        lumen_dots = make_lumen_particles(seed=13, n=8, x_range=(-6.0, -0.3), y_range=(-2.10, -1.35))
        tag = scope_tag("schematic", size=24, color=TEXT)

        # IMPORTANT: add rotor_ang, atp_t, h_rem_t to the scene so updaters run!
        rotor_ang.add_updater(lambda m: m.set_value(-(filled_t.get_value() / 14.0) * TAU))
        atp_t.add_updater(lambda m: m.set_value(filled_t.get_value() * 3.0 / 14.0))
        h_rem_t.add_updater(lambda m: m.set_value(max(0.0, 12.0 - filled_t.get_value())))
        self.add(mem, bin_nadph, bin_atp, atp_box, rotor_ring, sub_label, h_rem,
                 stroma_l, lumen_l, lumen_dots, tag, rotor_ang, atp_t, h_rem_t)

        # "12 protons turn the rotor, only 12 fourteenths of the way."
        self.play(filled_t.animate.set_value(12.0), run_time=4.4, rate_func=linear)

        # Swap in glowing 2 empty slots
        rotor_ring_glow = make_rotor_ring(RC, radius=1.40, n_slots=14, angle_tracker=rotor_ang,
                                          filled_count=12, empty_glow=True, slot_r=0.17, stroke_w=3.2)
        self.remove(rotor_ring)
        self.add(rotor_ring_glow)

        # Pop 2 ATP tokens outside the box -> ATP bin
        tok1 = chip("ATP", color=GOLD, size=24, pad=0.14).move_to([0.0, 2.55, 0])
        tok2 = chip("ATP", color=GOLD, size=24, pad=0.14).move_to([-1.2, 1.95, 0])
        self.play(FadeIn(tok1, run_time=0.25), FadeIn(tok2, run_time=0.25))
        self.play(
            LaggedStart(
                tok2.animate.move_to([ATP_BIN_X, BIN_BOT_Y + 2.0 * UNIT_H, 0]).set_opacity(0),
                tok1.animate.move_to([ATP_BIN_X, BIN_BOT_Y + 2.5 * UNIT_H, 0]).set_opacity(0),
                lag_ratio=0.5,
                run_time=0.95,
            ),
        )
        self.remove(tok1, tok2)

        # "That makes about 2.6 ATP, roughly 0.4 short."
        self.at("roughly")
        y_fill = BIN_BOT_Y + 0.03 + (12 * 3.0 / 14.0) * UNIT_H
        y_targ = BIN_BOT_Y + 0.03 + 3.0 * UNIT_H
        bx = ATP_BIN_X + BIN_W / 2 + 0.50
        bracket = VGroup(
            Line([bx - 0.08, y_fill, 0], [bx, y_fill, 0], color=PHOTON_COL, stroke_width=3),
            Line([bx, y_fill, 0], [bx, y_targ, 0], color=PHOTON_COL, stroke_width=3),
            Line([bx - 0.08, y_targ, 0], [bx, y_targ, 0], color=PHOTON_COL, stroke_width=3),
        )
        short_lab = T("about 0.4 short", size=26, color=PHOTON_COL, weight=BOLD).next_to(bracket, RIGHT, buff=0.14)
        self.play(Create(bracket, run_time=0.6), FadeIn(short_lab, shift=RIGHT * 0.1, run_time=0.6))

        # "The gap rests on that 14-subunit rotor."
        self.at("The gap rests")
        self.play(sub_label.animate.scale(1.18).set_color(YELLOW), run_time=0.65)
        self.play(sub_label.animate.scale(1 / 1.18).set_color(GOLD), run_time=0.65)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(12.0 * 3.0 / 14.0)
        rotor_ang_z = ValueTracker(-(12.0 / 14.0) * TAU)
        RC = np.array([2.0, 0.0, 0.0])
        BOX_W, BOX_H = 3.9, 3.7
        zoom_grp = VGroup(
            make_membrane(x0=-6.35, x1=6.35, y_top=0.55, y_bot=-0.55, gaps=[(RC[0] - BOX_W / 2, RC[0] + BOX_W / 2)]),
            RoundedRectangle(corner_radius=0.22, width=BOX_W, height=BOX_H,
                             stroke_color=GOLD, stroke_width=3.0, fill_color=GOLD, fill_opacity=0.07).move_to(RC),
            make_rotor_ring(RC, radius=1.40, n_slots=14, angle_tracker=rotor_ang_z,
                            filled_count=12, empty_glow=True, slot_r=0.17, stroke_w=3.2),
        )
        miss_tag = T("2 H+ missing", size=28, color=PHOTON_COL, weight=BOLD).move_to([2.0, 2.40, 0])
        self.add(zoom_grp, miss_tag)
        self.wait(1.6)

        # Pan back to the full cross-section
        rotor_ang = ValueTracker(-(12.0 / 14.0) * TAU)
        world, parts = build_base_world(
            nadph_t, atp_t, nadph_text="NADPH",
            atp_fmt=lambda v: f"{v:.1f}",
            rotor_angle=rotor_ang, rotor_filled=12, rotor_glow=True,
        )
        miss_small = T("2 H+ missing", size=24, color=PHOTON_COL, weight=BOLD).move_to([ATPS_X, 1.18, 0])
        self.play(
            FadeOut(zoom_grp, run_time=0.55),
            FadeOut(miss_tag, run_time=0.55),
        )
        self.play(
            FadeIn(world, run_time=0.65),
            FadeIn(miss_small, run_time=0.55),
        )

        # "Cytochrome b6f pumps two for every electron it passes."
        self.at("Cytochrome")
        b6f_bead = Dot(radius=0.14, color=GOLD).move_to([B6F_X + 0.98, 0.72, 0])
        hb1 = make_h_disc("b6f", radius=0.20).move_to([B6F_X - 0.30, -1.05, 0])
        hb2 = make_h_disc("b6f", radius=0.20).move_to([B6F_X + 0.30, -1.05, 0])
        self.add(b6f_bead)
        self.play(b6f_bead.animate.move_to([B6F_X + 0.98, -0.58, 0]), run_time=1.3)
        self.add(hb1, hb2)
        self.play(
            hb1.animate.move_to([-1.75, -1.75, 0]),
            hb2.animate.move_to([-0.75, -1.75, 0]),
            FadeOut(b6f_bead, run_time=0.5),
            run_time=1.4,
        )

        # "Predict: where could one electron go, to add protons but no NADPH?"
        self.at("Predict where could")
        fd_bead = bob(Dot(radius=0.15, color=GOLD).move_to(FD_POS), amp=0.04, speed=2.6)
        fd_lab = T("ferredoxin", size=24, color=GREEN).move_to([2.90, 1.18, 0])
        arr_nadp = Arrow(FD_POS + UP * 0.16 + RIGHT * 0.14, np.array([3.12, 2.15, 0.0]),
                         buff=0.05, color=GREEN, stroke_width=3.5).set_opacity(0.65)
        cross = VGroup(
            Line([-0.14, -0.14, 0], [0.14, 0.14, 0], color=PHOTON_COL, stroke_width=4),
            Line([-0.14, 0.14, 0], [0.14, -0.14, 0], color=PHOTON_COL, stroke_width=4),
        ).move_to(arr_nadp.get_center())
        no_nadph = T("no NADPH", size=24, color=PHOTON_COL, weight=BOLD).move_to([1.75, 2.52, 0])

        arr_blank = CurvedArrow(FD_POS + LEFT * 0.18 + UP * 0.06, np.array([0.05, 1.80, 0.0]),
                                angle=0.45, color=TEXT, stroke_width=3.5).set_opacity(0.85)
        q_arrow = T("?", size=34, color=TEXT, weight=BOLD).move_to([0.25, 2.35, 0])
        q_card = question_card("Where can it go?", y=3.28, color=TEXT, size=32, max_w=7.0).move_to([0.2, 3.28, 0])

        self.play(
            FadeOut(miss_small, run_time=0.35),
            FadeIn(fd_bead, scale=0.8, run_time=0.5),
            FadeIn(fd_lab, run_time=0.5),
            FadeIn(arr_nadp, run_time=0.5),
            FadeIn(cross, run_time=0.5),
            FadeIn(no_nadph, run_time=0.5),
            FadeIn(arr_blank, run_time=0.5),
            FadeIn(q_arrow, run_time=0.5),
            FadeIn(q_card, run_time=0.6),
        )
        self.finish()


class S06Think(PredictPause):
    QUESTION = "Where can it go?"
    CARD = {"y": 3.28, "color": TEXT, "size": 32, "max_w": 7.0}
    RING_AT = (5.95, 3.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(12.0 * 3.0 / 14.0)
        rotor_ang = ValueTracker(-(12.0 / 14.0) * TAU)
        world, _ = build_base_world(
            nadph_t, atp_t, nadph_text="NADPH",
            atp_fmt=lambda v: f"{v:.1f}",
            rotor_angle=rotor_ang, rotor_filled=12, rotor_glow=True,
        )
        hb1 = make_h_disc("b6f", radius=0.20).move_to([-1.75, -1.75, 0])
        hb2 = make_h_disc("b6f", radius=0.20).move_to([-0.75, -1.75, 0])
        fd_bead = bob(Dot(radius=0.15, color=GOLD).move_to(FD_POS), amp=0.05, speed=2.6)
        fd_lab = T("ferredoxin", size=24, color=GREEN).move_to([2.90, 1.18, 0])
        arr_nadp = Arrow(FD_POS + UP * 0.16 + RIGHT * 0.14, np.array([3.12, 2.15, 0.0]),
                         buff=0.05, color=GREEN, stroke_width=3.5).set_opacity(0.65)
        cross = VGroup(
            Line([-0.14, -0.14, 0], [0.14, 0.14, 0], color=PHOTON_COL, stroke_width=4),
            Line([-0.14, 0.14, 0], [0.14, -0.14, 0], color=PHOTON_COL, stroke_width=4),
        ).move_to(arr_nadp.get_center())
        no_nadph = T("no NADPH", size=24, color=PHOTON_COL, weight=BOLD).move_to([1.75, 2.52, 0])
        arr_blank = CurvedArrow(FD_POS + LEFT * 0.18 + UP * 0.06, np.array([0.05, 1.80, 0.0]),
                                angle=0.45, color=TEXT, stroke_width=3.5).set_opacity(0.85)
        q_arrow = T("?", size=34, color=TEXT, weight=BOLD).move_to([0.25, 2.35, 0])
        return VGroup(world, hb1, hb2, fd_bead, fd_lab, arr_nadp, cross, no_nadph, arr_blank, q_arrow)

    def construct(self):
        self.add(self.backdrop())
        qc = question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD).move_to([0.2, 3.28, 0])
        self.add(qc)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S07Answer(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(12.0 * 3.0 / 14.0)
        rotor_ang = ValueTracker(-(12.0 / 14.0) * TAU)
        world, parts = build_base_world(
            nadph_t, atp_t, nadph_text="NADP+",
            atp_fmt=lambda v: f"{v:.1f}",
            rotor_angle=rotor_ang, rotor_filled=12, rotor_glow=True,
        )
        fd_bead = make_electron_bead(radius=0.15, halo=True).move_to(FD_POS)
        fd_lab = T("ferredoxin", size=24, color=GREEN).move_to([2.90, 1.18, 0])
        arr_nadp = Arrow(FD_POS + UP * 0.16 + RIGHT * 0.14, np.array([3.12, 2.15, 0.0]),
                         buff=0.05, color=GREEN, stroke_width=3.5).set_opacity(0.65)
        cross = VGroup(
            Line([-0.14, -0.14, 0], [0.14, 0.14, 0], color=PHOTON_COL, stroke_width=4),
            Line([-0.14, 0.14, 0], [0.14, -0.14, 0], color=PHOTON_COL, stroke_width=4),
        ).move_to(arr_nadp.get_center())
        no_nadph = T("no NADPH", size=24, color=PHOTON_COL, weight=BOLD).move_to([1.75, 2.52, 0])
        arr_blank = CurvedArrow(FD_POS + LEFT * 0.18 + UP * 0.06, np.array([0.05, 1.80, 0.0]),
                                angle=0.45, color=TEXT, stroke_width=3.5).set_opacity(0.85)
        q_arrow = T("?", size=34, color=TEXT, weight=BOLD).move_to([0.25, 2.35, 0])
        q_card = question_card("Where can it go?", y=3.28, color=TEXT, size=32, max_w=7.0).move_to([0.2, 3.28, 0])

        self.add(world, fd_bead, fd_lab, arr_nadp, cross, no_nadph, arr_blank, q_arrow, q_card)

        # "Back to cytochrome b6f."
        orange_arc = cyclic_arc_only(width=7.5)
        self.play(
            FadeOut(q_card, run_time=0.5),
            FadeOut(q_arrow, run_time=0.5),
            FadeOut(arr_nadp, run_time=0.5),
            FadeOut(cross, run_time=0.5),
            FadeOut(no_nadph, run_time=0.5),
            ReplacementTransform(arr_blank, orange_arc, run_time=1.2),
            parts["psii"].animate.set_opacity(0.4),
        )

        # "At ferredoxin, the electron turns around instead of reaching NADP+."
        self.at("At ferredoxin")
        self.play(
            MoveAlongPath(fd_bead, orange_arc, run_time=3.8, rate_func=linear),
            ShowPassingFlash(orange_arc.copy().set_stroke(YELLOW, 15), time_width=0.6, run_time=3.8),
        )

        # "It falls through b6f, which pumps its two protons."
        self.at("It falls through")
        b6f_drop = VMobject().set_points_as_corners([
            np.array([B6F_X, 0.82, 0]),
            np.array([B6F_X + 0.98, 0.64, 0]),
            np.array([B6F_X + 0.98, -0.62, 0]),
        ])
        hb1 = make_h_disc("b6f", radius=0.20).move_to([B6F_X - 0.30, -1.05, 0])
        hb2 = make_h_disc("b6f", radius=0.20).move_to([B6F_X + 0.30, -1.05, 0])
        self.play(
            MoveAlongPath(fd_bead, b6f_drop, run_time=2.1, rate_func=linear),
            parts["b6f_box"].animate.set_fill(opacity=0.40).set_stroke(width=5.5),
        )
        self.add(hb1, hb2)
        self.play(
            hb1.animate.move_to([-1.75, -1.80, 0]),
            hb2.animate.move_to([-0.75, -1.80, 0]),
            parts["b6f_box"].animate.set_fill(opacity=0.16).set_stroke(width=2.8),
            run_time=2.1,
        )

        # "Then it returns to Photosystem I, and a photon lifts it again."
        self.at("Then it returns")
        bot_bridge = Line([B6F_X + COMP_W / 2, -0.52, 0], [PSI_X - COMP_W / 2, -0.52, 0],
                          color=ORANGE, stroke_width=7.5)
        ret_traj = VMobject().set_points_as_corners([
            np.array([B6F_X + 0.98, -0.62, 0]),
            np.array([PSI_X - 0.98, -0.62, 0]),
            np.array([PSI_X + 0.98, -0.62, 0]),
        ])
        cyc_label = T("cyclic flow", size=28, color=ORANGE, weight=BOLD).move_to([0.35, 2.38, 0])
        self.play(
            Create(bot_bridge, run_time=0.9),
            MoveAlongPath(fd_bead, ret_traj, run_time=2.1, rate_func=linear),
            hb1.animate.move_to([1.20, -1.80, 0]),
            hb2.animate.move_to([2.10, -1.80, 0]),
            FadeIn(cyc_label, shift=UP * 0.08, run_time=0.6),
        )

        self.at("a photon lifts it again")
        up_stem = Line([PSI_X, 0.82, 0], FD_POS, color=ORANGE, stroke_width=7.5)
        lift_traj = VMobject().set_points_as_corners([
            np.array([PSI_X + 0.98, -0.62, 0]),
            np.array([PSI_X + 0.98, 0.72, 0]),
            FD_POS,
        ])
        pw = make_photon_wave([0.9, 1.65, 0], [PSI_X, 0.85, 0])
        self.play(FadeIn(pw, run_time=0.25))
        self.play(
            Create(up_stem, run_time=0.8),
            MoveAlongPath(fd_bead, lift_traj, run_time=1.8, rate_func=linear),
            parts["psi_box"].animate.set_fill(opacity=0.38).set_stroke(width=5.5),
            FadeOut(pw, run_time=0.8),
        )
        self.play(parts["psi_box"].animate.set_fill(opacity=0.16).set_stroke(width=2.8), run_time=0.4)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(12.0 * 3.0 / 14.0)
        rotor_ang = ValueTracker(-(12.0 / 14.0) * TAU)
        world, parts = build_base_world(
            nadph_t, atp_t, nadph_text="NADPH",
            atp_fmt=lambda v: f"{v:.1f}",
            rotor_angle=rotor_ang, rotor_filled=12, rotor_glow=False,
        )
        lin_guide = linear_bridges(opacity=0.35)
        cyc_loop = cyclic_visible_bridges(width=6.0, opacity=0.9)
        cyc_label = T("cyclic flow", size=28, color=ORANGE, weight=BOLD).move_to([0.35, 2.38, 0])
        cyc_traj = cyclic_bead_path()
        bead = Dot(radius=0.14, color=GOLD).move_to(FD_POS)
        self.add(world, lin_guide, cyc_loop, cyc_label, bead, rotor_ang)

        # Keep rotor turning and bead gently active on intro
        self.play(MoveAlongPath(bead, cyc_traj, run_time=2.2, rate_func=linear))

        # "ATP is paid in protons."
        self.at("paid in protons")
        h_d1 = make_h_disc("b6f", radius=0.20).move_to([2.4, -1.75, 0])
        h_d2 = make_h_disc("water", radius=0.20).move_to([3.0, -1.75, 0])
        h_d3 = make_h_disc("b6f", radius=0.20).move_to([3.6, -1.75, 0])
        # Smooth gold link routed cleanly up the x=5.08 corridor between NADPH and stroma
        gold_link = VMobject(stroke_color=GOLD, stroke_width=4.5, fill_opacity=0)
        gold_link.set_points_smoothly([
            np.array([ATPS_X + 0.03, 1.02, 0.0]),
            np.array([ATPS_X + 0.03, 2.65, 0.0]),
            np.array([4.60, 3.24, 0.0]),
            np.array([0.80, 3.30, 0.0]),
            np.array([-2.20, 3.05, 0.0]),
            np.array([-3.35, 2.05, 0.0]),
        ])
        gold_tip = Arrow(np.array([-2.95, 2.40, 0]), np.array([-3.38, 2.02, 0]),
                         buff=0, color=GOLD, stroke_width=4.5, max_tip_length_to_length_ratio=0.5)
        self.play(
            FadeIn(h_d1, run_time=0.25), FadeIn(h_d2, run_time=0.25), FadeIn(h_d3, run_time=0.25),
            h_d1.animate(run_time=1.3).move_to([2.8, -1.55, 0]),
            h_d2.animate(run_time=1.3).move_to([3.3, -1.30, 0]),
            h_d3.animate(run_time=1.3).move_to([3.75, -1.05, 0]),
            Create(gold_link, run_time=1.5),
            Succession(Wait(1.2), FadeIn(gold_tip, run_time=0.3)),
            rotor_ang.animate(run_time=1.6).set_value(-(13.0 / 14.0) * TAU),
        )
        self.play(FadeOut(h_d1, run_time=0.25), FadeOut(h_d2, run_time=0.25), FadeOut(h_d3, run_time=0.25))

        # "NADPH is paid in electrons that reach the end."
        self.at("electrons that reach the end")
        lin_pts = linear_bead_points()
        e_lin = Dot(radius=0.14, color=GOLD).move_to(lin_pts[6])
        seg_end = VMobject().set_points_as_corners(lin_pts[6:])
        green_link = CubicBezier(
            np.array([3.35, 2.95, 0.0]),
            np.array([1.20, 3.42, 0.0]),
            np.array([-2.80, 3.42, 0.0]),
            np.array([NADPH_BIN_X, 3.34, 0.0]),
            color=GREEN, stroke_width=4.5,
        )
        green_tip = Arrow(np.array([NADPH_BIN_X + 0.35, 3.44, 0]), np.array([NADPH_BIN_X + 0.02, 3.36, 0]),
                          buff=0, color=GREEN, stroke_width=4.5, max_tip_length_to_length_ratio=0.5)
        self.add(e_lin)
        self.play(
            FadeOut(gold_link, run_time=0.35),
            FadeOut(gold_tip, run_time=0.35),
            MoveAlongPath(e_lin, seg_end, run_time=1.8, rate_func=linear),
            Create(green_link, run_time=1.6),
            Succession(Wait(1.2), FadeIn(green_tip, run_time=0.3)),
        )
        self.remove(e_lin)

        # "So a loop that never reaches the end buys ATP alone."
        self.at("a loop that never reaches")
        protons_only = T("protons only", size=28, color=ORANGE, weight=BOLD).move_to([0.35, 2.38, 0])
        h_drop1 = make_h_disc("b6f", radius=0.20).move_to([B6F_X - 0.30, -1.05, 0])
        h_drop2 = make_h_disc("b6f", radius=0.20).move_to([B6F_X + 0.30, -1.05, 0])
        atp_tok = chip("ATP", color=GOLD, size=24, pad=0.16).move_to([ATPS_X, 1.30, 0])
        self.play(
            FadeOut(green_link, run_time=0.35),
            FadeOut(green_tip, run_time=0.35),
            swap(cyc_label, protons_only, run_time=0.5),
            cyc_loop.animate.set_stroke(width=8.5),
            MoveAlongPath(bead, cyc_traj, run_time=3.4, rate_func=linear),
            ShowPassingFlash(cyc_loop.copy().set_stroke(YELLOW, 10), time_width=0.4, run_time=3.4),
            FadeIn(h_drop1, run_time=0.3),
            FadeIn(h_drop2, run_time=0.3),
            h_drop1.animate(run_time=2.5).move_to([2.6, -1.65, 0]),
            h_drop2.animate(run_time=2.5).move_to([3.3, -1.45, 0]),
            atp_t.animate(run_time=2.8).set_value(3.0),
            rotor_ang.animate(run_time=3.2).set_value(-TAU),
            FadeIn(atp_tok, shift=UP * 0.2, run_time=0.6),
        )
        self.play(atp_tok.animate.move_to([ATPS_X, 1.75, 0]).set_opacity(0), run_time=0.6)
        self.finish()


class S09Mix(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(0.0)
        atp_t = ValueTracker(0.0)
        rotor_ang = ValueTracker(0.0)
        rotor_fill = ValueTracker(0.0)
        h_count = ValueTracker(0.0)
        ph_count = ValueTracker(0.0)

        world, parts = build_base_world(
            nadph_t, atp_t, nadph_text="NADP+",
            atp_fmt=lambda v: f"{v:.0f}" if v >= 2.92 or v < 0.05 else f"{v:.1f}",
            rotor_angle=rotor_ang, rotor_filled=rotor_fill,
        )
        lin_guide = linear_bridges(opacity=0.40)
        cyc_loop = cyclic_visible_bridges(width=5.5, opacity=0.85)
        h_counter = counter("lumen H+: {:.0f}", h_count, at=[-1.25, -2.75, 0], size=28, color=TEAL)
        ph_counter = counter("photons: {:.0f}", ph_count, at=[0.2, 3.25, 0], size=28, color=PHOTON_COL)

        # IMPORTANT: add rotor_ang and atp_t so updaters fire!
        rotor_ang.add_updater(lambda m: m.set_value(-(rotor_fill.get_value() / 14.0) * TAU))
        atp_t.add_updater(lambda m: m.set_value(rotor_fill.get_value() * 3.0 / 14.0))
        self.add(world, lin_guide, cyc_loop, h_counter, ph_counter, rotor_ang, atp_t)

        # Run 2 linear GOLD beads in 0..3.4 s (4 photons, 6 H+, 1 NADPH, 1 O2)
        pts = linear_bead_points()
        full_lin = VMobject().set_points_as_corners(pts)
        o2_bub = VGroup(
            Circle(radius=0.34, color=BLUE, stroke_width=2.6, fill_color=BLUE, fill_opacity=0.15),
            T("O2", size=22, color=BLUE, weight=BOLD),
        )
        o2_bub[1].move_to(o2_bub[0])
        o2_bub.move_to([PSII_X, -1.28, 0])
        self.play(FadeIn(o2_bub, run_time=0.2), o2_bub.animate(run_time=0.45).move_to([-5.65, -2.25, 0]))

        for k in range(2):
            b = make_electron_bead(radius=0.14, halo=True).move_to(pts[0])
            self.add(b)
            self.play(
                MoveAlongPath(b, full_lin, run_time=1.15, rate_func=linear),
                h_count.animate(run_time=1.10).set_value(3 * (k + 1)),
                rotor_fill.animate(run_time=1.10).set_value(3 * (k + 1)),
                nadph_t.animate(run_time=1.10).set_value(0.5 * (k + 1)),
                ph_count.animate(run_time=1.10).set_value(2 * (k + 1)),
            )
            self.remove(b)

        # "About one electron per oxygen molecule goes around the loop."
        # Continue linear beads 3 & 4 TOGETHER with the 1 cyclic loop bead!
        self.at("About one electron")
        cyc_bead = make_electron_bead(radius=0.15, halo=True).move_to(FD_POS)
        arc_to_b6f = cyclic_arc_only()
        b6f_drop = Line([B6F_X + 0.98, 0.82, 0], [B6F_X + 0.98, -0.62, 0])
        b3 = make_electron_bead(radius=0.14, halo=True).move_to(pts[0])
        b4 = make_electron_bead(radius=0.14, halo=True).move_to(pts[0])
        self.add(cyc_bead, b3)
        self.play(
            MoveAlongPath(b3, full_lin, run_time=1.6, rate_func=linear),
            MoveAlongPath(cyc_bead, arc_to_b6f, run_time=2.2, rate_func=linear),
            ShowPassingFlash(cyc_loop.copy().set_stroke(YELLOW, 11), time_width=0.45, run_time=2.2),
            h_count.animate(run_time=1.6).set_value(9.0),
            rotor_fill.animate(run_time=1.6).set_value(9.0),
            nadph_t.animate(run_time=1.6).set_value(1.5),
            ph_count.animate(run_time=1.6).set_value(6.0),
        )
        self.remove(b3)
        self.add(b4)
        nadph_done = chip("NADPH", color=GREEN, size=26, pad=0.22).move_to(NADP_POS)
        self.play(
            MoveAlongPath(b4, full_lin, run_time=1.6, rate_func=linear),
            h_count.animate(run_time=1.6).set_value(12.0),
            rotor_fill.animate(run_time=1.6).set_value(12.0),
            nadph_t.animate(run_time=1.6).set_value(2.0),
            ph_count.animate(run_time=1.6).set_value(8.0),
        )
        self.remove(b4)
        self.play(swap(parts["nadp_box"], nadph_done, run_time=0.45))

        # "Its two protons bring the total to 14, three ATP."
        self.at("Its two protons")
        hb1 = make_h_disc("b6f", radius=0.20).move_to([B6F_X - 0.30, -1.05, 0])
        hb2 = make_h_disc("b6f", radius=0.20).move_to([B6F_X + 0.30, -1.05, 0])
        self.play(MoveAlongPath(cyc_bead, b6f_drop, run_time=1.2, rate_func=linear))
        self.add(hb1, hb2)
        self.play(
            hb1.animate.move_to([2.9, -1.65, 0]),
            hb2.animate.move_to([3.6, -1.65, 0]),
            h_count.animate.set_value(14.0),
            rotor_fill.animate.set_value(14.0),
            run_time=2.5,
        )

        # "The price is about nine photons per oxygen instead of eight."
        self.at("The price is about")
        ret_seg = VMobject().set_points_as_corners([
            np.array([B6F_X + 0.98, -0.62, 0]),
            np.array([PSI_X + 0.98, -0.62, 0]),
            np.array([PSI_X + 0.98, 0.72, 0]),
            FD_POS,
        ])
        pw = make_photon_wave([0.9, 1.65, 0], [PSI_X, 0.85, 0])
        about_9 = T("about 9 photons", size=28, color=PHOTON_COL, weight=BOLD).move_to([0.2, 3.25, 0])
        atp_tok = chip("ATP", color=GOLD, size=24, pad=0.16).move_to([ATPS_X, 1.30, 0])
        self.play(
            FadeIn(pw, run_time=0.25),
            MoveAlongPath(cyc_bead, ret_seg, run_time=2.6, rate_func=linear),
            ShowPassingFlash(cyc_loop.copy().set_stroke(YELLOW, 11), time_width=0.45, run_time=2.6),
            ph_count.animate(run_time=1.0).set_value(9.0),
            FadeIn(atp_tok, shift=UP * 0.2, run_time=0.6),
        )
        self.play(FadeOut(pw, run_time=0.25), FadeOut(ph_counter, run_time=0.25))
        self.remove(ph_counter)
        self.play(
            atp_tok.animate.move_to([ATPS_X, 1.80, 0]).set_opacity(0),
            FadeIn(about_9, run_time=0.4),
        )
        self.finish()


class S10Arnon(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(3.0)
        rotor_ang = ValueTracker(-TAU)
        world, parts = build_base_world(
            nadph_t, atp_t, nadph_text="NADPH",
            rotor_angle=rotor_ang, rotor_filled=14,
        )
        lin_guide = linear_bridges(color=GOLD, opacity=0.30, width=4.0)
        cyc_loop = cyclic_visible_bridges(color=ORANGE, width=4.5, opacity=0.35)
        arnon_tag = T("Arnon: two ways", size=28, color=TEXT, weight=BOLD).move_to([-1.65, 3.28, 0])
        self.add(world, lin_guide, cyc_loop, arnon_tag, rotor_ang)

        # Light linear route first ("non-cyclic")
        noncyc_tag = T("non-cyclic", size=26, color=GOLD, weight=BOLD).move_to([-2.4, 1.25, 0])
        lin_bright = linear_bridges(color=GOLD, opacity=0.95, width=6.0)
        lin_traj = VMobject().set_points_as_corners(linear_bead_points())
        b_lin = Dot(radius=0.14, color=GOLD).move_to(linear_bead_points()[0])
        self.add(b_lin)
        self.play(
            FadeIn(lin_bright, run_time=0.6),
            MoveAlongPath(b_lin, lin_traj, run_time=3.2, rate_func=linear),
            FadeIn(noncyc_tag, run_time=0.5),
            rotor_ang.animate.set_value(-1.5 * TAU),
        )
        self.remove(b_lin)

        # "The loop uses only the second lift, one photon per electron."
        self.at("The loop uses")
        cyc_tag = T("cyclic", size=26, color=ORANGE, weight=BOLD).move_to([0.35, 2.38, 0])
        cyc_bright = cyclic_visible_bridges(color=ORANGE, width=6.5, opacity=1.0)
        cyc_traj = cyclic_bead_path()
        b_cyc = Dot(radius=0.14, color=GOLD).move_to(FD_POS)
        pw = make_photon_wave([0.9, 1.65, 0], [PSI_X, 0.85, 0])
        self.add(b_cyc)
        # IMPORTANT: set_stroke(opacity=0.25) so we never turn on polygon fill!
        self.play(
            lin_bright.animate.set_stroke(opacity=0.25),
            parts["psii"].animate.set_opacity(0.4),
            FadeIn(cyc_bright, run_time=0.5),
            FadeIn(cyc_tag, run_time=0.4),
            FadeIn(pw, run_time=0.3),
            MoveAlongPath(b_cyc, cyc_traj, run_time=4.0, rate_func=linear),
            ShowPassingFlash(cyc_bright.copy().set_stroke(YELLOW, 10), time_width=0.4, run_time=4.0),
            rotor_ang.animate.set_value(-2.2 * TAU),
        )
        self.play(FadeOut(pw, run_time=0.35))

        # "Alongside other balancing routes, it brings the output to 3 to 2."
        self.at("Alongside other balancing")
        other_arr = DashedVMobject(
            Arrow([-1.4, 2.25, 0], [-3.35, 2.25, 0], buff=0, color=TEXT, stroke_width=4.5),
            num_dashes=6,
        ).set_stroke(opacity=0.90)
        other_lab = T("other routes", size=24, color=TEXT).next_to(other_arr, UP, buff=0.12)
        self.play(
            FadeIn(other_arr, run_time=0.5),
            FadeIn(other_lab, run_time=0.5),
            MoveAlongPath(b_cyc, cyc_traj, run_time=2.2, rate_func=linear),
            ShowPassingFlash(cyc_bright.copy().set_stroke(YELLOW, 10), time_width=0.4, run_time=2.2),
        )

        self.at("brings the output")
        ratio_tag = T("3 : 2", size=34, color=GOLD, weight=BOLD).move_to([1.3, 3.28, 0])
        self.play(
            FadeIn(ratio_tag, scale=1.1, run_time=0.5),
            MoveAlongPath(b_cyc, cyc_traj, run_time=2.5, rate_func=linear),
            ShowPassingFlash(cyc_bright.copy().set_stroke(YELLOW, 10), time_width=0.4, run_time=2.5),
            rotor_ang.animate.set_value(-2.8 * TAU),
        )
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        nadph_t = ValueTracker(2.0)
        atp_t = ValueTracker(3.0)
        rotor_ang = ValueTracker(-TAU)
        world, parts = build_base_world(
            nadph_t, atp_t, nadph_text="NADPH",
            rotor_angle=rotor_ang, rotor_filled=14,
        )
        lin_guide = linear_bridges(color=GOLD, opacity=0.45, width=4.0)
        cyc_loop = cyclic_visible_bridges(color=ORANGE, width=6.0, opacity=0.85)
        q_mark = T("?", size=36, color=TEXT, weight=BOLD).move_to([ATP_BIN_X, 3.52, 0])
        rotor_ang.add_updater(lambda m, dt: m.increment_value(-0.55 * dt))

        self.add(world, lin_guide, cyc_loop, q_mark, rotor_ang)
        # Question mark dissolves into the ORANGE loop on "So the answer..."
        self.play(
            q_mark.animate.move_to([0.35, 1.85, 0]).set_opacity(0),
            cyc_loop.animate.set_stroke(width=8.0),
            ShowPassingFlash(cyc_loop.copy().set_stroke(YELLOW, 10), time_width=0.4, run_time=2.6),
            run_time=2.6,
        )
        self.remove(q_mark)

        # "Electrons that finish the climb make NADPH."
        self.at("finish the climb")
        lin_traj = VMobject().set_points_as_corners(linear_bead_points())
        b_lin = make_electron_bead(radius=0.15, halo=True).move_to(linear_bead_points()[0])
        pw1 = make_photon_wave([-2.75, 1.55, 0], [PSII_X + 0.55, 0.86, 0])
        pw2 = make_photon_wave([0.95, 1.55, 0], [PSI_X, 0.86, 0])
        self.add(b_lin)
        self.play(
            FadeIn(pw1, run_time=0.25),
            FadeIn(pw2, run_time=0.25),
            MoveAlongPath(b_lin, lin_traj, run_time=2.8, rate_func=linear),
            ShowPassingFlash(lin_guide.copy().set_stroke(YELLOW, 10), time_width=0.45, run_time=2.8),
        )
        self.play(FadeOut(pw1, run_time=0.25), FadeOut(pw2, run_time=0.25))
        self.remove(b_lin)

        # "Electrons that circle only pump protons."
        self.at("Electrons that circle")
        cyc_traj = cyclic_bead_path()
        b_cyc = make_electron_bead(radius=0.15, halo=True).move_to(FD_POS)
        hb1 = make_h_disc("b6f", radius=0.20).move_to([B6F_X - 0.30, -1.05, 0])
        hb2 = make_h_disc("b6f", radius=0.20).move_to([B6F_X + 0.30, -1.05, 0])
        atp_tok = chip("ATP", color=GOLD, size=24, pad=0.16).move_to([ATPS_X, 1.30, 0])
        self.add(b_cyc)
        self.play(
            MoveAlongPath(b_cyc, cyc_traj, run_time=3.0, rate_func=linear),
            ShowPassingFlash(cyc_loop.copy().set_stroke(YELLOW, 12), time_width=0.5, run_time=3.0),
            FadeIn(hb1, run_time=0.35),
            FadeIn(hb2, run_time=0.35),
            hb1.animate(run_time=2.4).move_to([2.4, -1.65, 0]),
            hb2.animate(run_time=2.4).move_to([3.0, -1.65, 0]),
            FadeIn(atp_tok, shift=UP * 0.2, run_time=0.8),
        )

        # "The chloroplast sets its ratio partly by how many circle."
        self.at("The chloroplast sets")
        self.remove(b_cyc)
        cyc_flow = start_bead_flow(
            cyclic_bead_points(),
            n_beads=3, speed=0.28, radius=0.14, color=GOLD, halo=True,
        )
        lin_flow = start_bead_flow(linear_bead_points(), n_beads=2, speed=0.22, radius=0.13, color=GOLD, halo=True)
        self.add(cyc_flow, lin_flow)
        self.play(
            hb1.animate.move_to([2.9, -1.65, 0]),
            hb2.animate.move_to([3.5, -1.65, 0]),
            atp_tok.animate.move_to([ATPS_X, 1.85, 0]).set_opacity(0),
            ShowPassingFlash(cyc_loop.copy().set_stroke(YELLOW, 12), time_width=0.5, run_time=2.2),
        )
        self.play(
            FadeOut(hb1, run_time=0.4),
            FadeOut(hb2, run_time=0.4),
            ShowPassingFlash(cyc_loop.copy().set_stroke(YELLOW, 12), time_width=0.5, run_time=1.8),
        )
        self.finish()


class S12End(EndCard):
    LINE = "Looping electrons around Photosystem I adds ATP without adding NADPH."
