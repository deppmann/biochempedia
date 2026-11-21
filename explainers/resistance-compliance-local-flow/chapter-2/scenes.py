"""Who Turns the Tap — Resistance, Compliance and Local Blood Flow (Chapter 2)

COLOUR MAP (one colour per concept for the whole film)
- BLOOD_COL    (#F28B82, pale RED)   : blood dots flowing through vessels
- PRESSURE_COL (#E8EAF0, WHITE)      : pressure, pressure gauges, resistance bar, transmural wall arrows
- ARTERIOLE_COL(#FF862F, ORANGE)     : arterioles, smooth-muscle rings, tap-handle icons
- CAPILLARY_COL(#4DD0E1, CYAN)       : capillaries and oxygen supply gauge outline
- VESSEL_COL   (#7A8CA0, SLATE)      : aorta, small arteries, venules, veins, right atrium
- FLOW_COL     (#D4A843, GOLD)       : muscle bed's flow bar and muscle branch flow dots
- SIGNAL_COL   (#83C167, GREEN)      : signals from the tissue itself (adenosine, K+, CO2, H+, low O2, ATP, breakdown products)
- NO_COL       (#58C4DD, BLUE)       : nitric oxide from the endothelium
- NERVE_COL    (#B388FF, PURPLE)     : sympathetic / vasodilator nerves and neural spark

ONE PICTURE OF THE WORLD
The systemic circulation as parallel vascular beds fed by a pressure-regulated SLATE aorta and
draining into the right atrium, with each bed containing a small artery, an ORANGE arteriole
("the tap" with smooth-muscle rings and a tap handle), CYAN capillaries threading a tissue block,
and an outgoing vein. The film zooms from the two-branch overview into the single muscle/heart
bed (with a live autoregulation plot on the right), then pulls back to four parallel organ beds
(heart, brain, muscle, skin) sharing the same tap mechanism under different controllers.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from)
- s00_link_and_question: Blood dots flow along computed paths in the 2-branch loop; the camera transforms into the zoomed muscle bed while flow = P / R drives dot speed and the GOLD flow bar; a hand outline + '?' land over the tap.
- s02_work: Tissue pulses faster; GREEN tissue signals and BLUE endothelial NO dots stream to the arteriole; arteriole radius widens, R drops via Poiseuille scaling (r^-4), computed flow rises, red dots speed up, GOLD flow bar rises.
- s03_autoreg: Tissue returns to steady state; WHITE perfusion pressure gauge slides up, down, up while computed autoregulatory arteriole radius adjusts so GOLD flow bar stays nearly steady; schematic plot axes fade in.
- s04_curve: Driven by one pressure ValueTracker sweeping low -> middle -> high -> middle, the WHITE gauge, arteriole width, GOLD flow bar, and live plot curve + dot all trace the computed autoregulation curve Q(P).
- s05_predict: Equation appears; pressure tracker climbs within the middle range so WHITE gauge rises, plot dot slides along the 'nearly level' stretch, and GOLD flow bar stays almost still while arteriole width holds fixed with a '?'.
- s07_answer: Pressure climbs then falls across the middle range; arteriole rings narrow then widen dynamically via R(P), WHITE resistance bar rises and falls in proportion with pressure while GOLD flow bar stays nearly level; transmural arrows press outward.
- s08_berne: Plot fades; tissue morphs to striated heart muscle; CYAN oxygen gauge drains; coronary arteriole widens, WHITE resistance bar drops, GOLD flow bar rises, and GREEN breakdown dots wash into the vein.
- s09_adenosine: GREEN ATP token splits into adenosine and diffuses to the arteriole, widening it; a blocker bar crosses the path and two schematic flow bars show preserved normal-O2 flow vs blunted low-O2 flow.
- s10_idea: World pulls back to four parallel organ beds (heart, brain, muscle, skin) with steady aorta pressure, flowing blood dots (GOLD-tinted in muscle), glowing taps, and four empty hand outlines.
- s11_heart_brain: Heart branch fills its hand with GREEN signals and widens; brain branch sparks a neuron, raises and lowers its CO2 gauge, and dilates then constricts its arteriole and blood flow accordingly.
- s12_muscle: Muscle branch fills its hand with GREEN metabolites and speeds GOLD-tinted dots; a 'flow rise' bar splits into five ~20% coloured slices; PURPLE sympathetic nerve pulses fail to constrict the working arteriole.
- s13_skin: Body-temperature thermometer rises smoothly; PURPLE nerve wires pulse into the skin hand outline, widening the skin arteriole and accelerating blood flow while skin tissue stays dim.
- s14_close: All four branches brighten together with pressure wall-stretch arrows, GREEN chemistry dots at heart and muscle, neuron spark at brain, and PURPLE heat-tuned nerves at skin while blood flows through all four.
"""
from bp_parts import *

# ------------------------------------------------------------------ COLOUR MAP
BLOOD_COL = "#F28B82"
PRESSURE_COL = TEXT
ARTERIOLE_COL = ORANGE
CAPILLARY_COL = "#4DD0E1"
VESSEL_COL = "#7A8CA0"
FLOW_COL = GOLD
SIGNAL_COL = GREEN
NO_COL = BLUE
NERVE_COL = "#B388FF"

# ------------------------------------------------------------------ COMPUTED MODEL
def autoreg_flow(p):
    """Schematic autoregulation curve Q(p) for p in [0, 1].
    Low p (< 0.28): steep rise.
    Middle range (0.28..0.72): nearly level, visibly tilted upward (0.46 -> 0.56).
    High p (> 0.72): steep rise again.
    """
    p = float(np.clip(p, 0.02, 1.0))
    s_low = 0.5 * (1.0 - np.tanh((p - 0.28) / 0.06))
    s_high = 0.5 * (1.0 + np.tanh((p - 0.72) / 0.06))
    s_mid = np.clip(1.0 - s_low - s_high, 0.0, 1.0)
    q_low = 1.65 * p
    q_mid = 0.46 + (0.56 - 0.46) * ((p - 0.28) / 0.44)
    q_high = 0.56 + 1.45 * (p - 0.72)
    return float(np.clip(s_low * q_low + s_mid * q_mid + s_high * q_high, 0.03, 0.98))


def autoreg_res(p):
    """Normalized resistance R = P / Q in [0.12, 0.96] scaled for display."""
    p = float(np.clip(p, 0.05, 1.0))
    q = max(autoreg_flow(p), 0.05)
    return float(np.clip(0.55 * (p / q), 0.12, 0.96))


def radius_from_res(res, r_rest=0.26):
    """Poiseuille scaling r ~ R^(-1/4), relative to resting resistance ~0.55."""
    res = max(float(res), 0.12)
    return float(np.clip(r_rest * (0.55 / res) ** 0.25, 0.15, 0.43))


# ------------------------------------------------------------------ PATH & PARTICLE HELPERS
def _sample_polyline(pts, n=120):
    pts = [np.array(p, dtype=float) for p in pts]
    dists = [0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        dists.append(dists[-1] + float(np.linalg.norm(b - a)))
    total = max(dists[-1], 1e-6)
    s_vals = np.linspace(0.0, total, n)
    out = []
    idx = 0
    for s in s_vals:
        while idx < len(dists) - 2 and dists[idx + 1] < s:
            idx += 1
        seg_len = max(dists[idx + 1] - dists[idx], 1e-6)
        u = (s - dists[idx]) / seg_len
        out.append((1.0 - u) * pts[idx] + u * pts[idx + 1])
    return np.array(out), total


def make_flowing_dots(paths_pts, flow_fn, color=BLOOD_COL, per_path=8, radius=0.072, seed=7, opacity=0.95):
    """Dots flowing along polyline paths at speed proportional to flow_fn()."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for path_pts in paths_pts:
        samples, total = _sample_polyline(path_pts, n=140)
        for k in range(per_path):
            d = Dot(radius=radius, color=color).set_opacity(opacity)
            d._s = (k / per_path + rng.uniform(0.0, 0.04)) % 1.0
            d._samples = samples
            d._total = total

            def upd(mob, dt, fn=flow_fn):
                spd = 0.45 + 1.85 * float(fn())
                mob._s = (mob._s + spd * dt / max(mob._total * 0.25, 0.45)) % 1.0
                idx = min(int(mob._s * (len(mob._samples) - 1)), len(mob._samples) - 1)
                mob.move_to(mob._samples[idx])

            idx0 = min(int(d._s * (len(samples) - 1)), len(samples) - 1)
            d.move_to(samples[idx0])
            d.add_updater(upd)
            g.add(d)
    g.layout_ok = True
    return g


def make_tap_icon(center, scale=1.0, angle_fn=None, glow=False):
    """Small ORANGE tap-handle icon: vertical stem + crossbar handle that turns."""
    c = np.array(center, dtype=float)

    def build():
        ang = float(angle_fn()) if angle_fn is not None else 0.0
        stem = Line(c + DOWN * 0.16 * scale, c + UP * 0.14 * scale, color=ARTERIOLE_COL, stroke_width=5 * scale)
        pivot = c + UP * 0.14 * scale
        cap = Circle(radius=0.055 * scale, color=ARTERIOLE_COL, fill_color=ARTERIOLE_COL, fill_opacity=1.0).move_to(pivot)
        bar = Line(pivot + LEFT * 0.22 * scale, pivot + RIGHT * 0.22 * scale, color=ARTERIOLE_COL, stroke_width=6 * scale)
        d1 = Dot(pivot + LEFT * 0.22 * scale, radius=0.045 * scale, color=ARTERIOLE_COL)
        d2 = Dot(pivot + RIGHT * 0.22 * scale, radius=0.045 * scale, color=ARTERIOLE_COL)
        handle = VGroup(bar, d1, d2).rotate(ang, about_point=pivot)
        if glow:
            halo = Circle(radius=0.28 * scale, color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.18).move_to(c + UP * 0.12 * scale)
            return VGroup(halo, stem, cap, handle)
        return VGroup(stem, cap, handle)

    g = always_redraw(build) if angle_fn is not None else build()
    g.layout_ok = True
    return g


def make_hand_outline(center, scale=0.65, color=TEXT, variant=0):
    """Clean schematic gripping/turning hand outline (never a filled solid box)."""
    spread = 0.04 * (variant - 1.5)
    pts = [
        [-0.22, -0.35, 0], [-0.26, -0.05, 0], [-0.42, 0.06 + spread, 0], [-0.36, 0.17 + spread, 0],
        [-0.20, 0.08, 0], [-0.20, 0.34, 0], [-0.11, 0.36, 0], [-0.10, 0.10, 0],
        [-0.04, 0.40 - spread, 0], [0.05, 0.40 - spread, 0], [0.05, 0.10, 0],
        [0.11, 0.36, 0], [0.20, 0.34, 0], [0.19, 0.08, 0],
        [0.25, 0.26 + spread, 0], [0.33, 0.23 + spread, 0], [0.27, -0.08, 0],
        [0.20, -0.35, 0],
    ]
    poly = Polygon(*pts, color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.08)
    poly.scale(scale).move_to(center)
    poly.layout_ok = True
    return poly


def make_vertical_bar(tracker_or_fn, center, height=1.6, width=0.34, color=PRESSURE_COL,
                      label="", label_pos=UP, label_size=26):
    """Vertical meter bar tied to a ValueTracker or callable returning [0..1]."""
    c = np.array(center, dtype=float)
    fn = tracker_or_fn.get_value if hasattr(tracker_or_fn, "get_value") else tracker_or_fn
    frame = RoundedRectangle(corner_radius=0.07, width=width, height=height,
                             stroke_color=color, stroke_width=2.8, fill_color=BG, fill_opacity=0.85).move_to(c)
    bottom_y = c[1] - height / 2 + 0.04
    inner_h = height - 0.08
    inner_w = width - 0.10

    def mk_fill():
        v = float(np.clip(fn(), 0.03, 1.0))
        h = max(0.05, v * inner_h)
        r = Rectangle(width=inner_w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.82)
        r.move_to([c[0], bottom_y + h / 2, 0])
        return r

    def mk_tick():
        v = float(np.clip(fn(), 0.03, 1.0))
        y = bottom_y + v * inner_h
        return Line([c[0] - width / 2 - 0.06, y, 0], [c[0] + width / 2 + 0.06, y, 0],
                    color=TEXT, stroke_width=3.5)

    fill = always_redraw(mk_fill)
    tick = always_redraw(mk_tick)
    g = VGroup(frame, fill, tick)
    if label:
        lab = T(label, size=label_size, color=color).next_to(frame, label_pos, buff=0.16)
        g.add(lab)
        g.label = lab
    g.frame = frame
    g.fill = fill
    g.tick = tick
    return g


# ------------------------------------------------------------------ WORLD A: TWO-BRANCH OVERVIEW (s00 opening)
def make_two_branch_world():
    """Opening parallel loop from film 1: SLATE aorta + steady WHITE gauge feeding 'muscle' and 'other beds' into right atrium."""
    aorta_x, ra_x = -4.8, 4.6
    y_top, y_bot = 1.15, -1.25

    aorta = Line([aorta_x, y_bot - 0.3, 0], [aorta_x, y_top + 0.3, 0], color=VESSEL_COL, stroke_width=14)
    aorta_lab = T("aorta", size=26, color=VESSEL_COL).next_to(aorta, UP, buff=0.18)

    p_val = ValueTracker(0.62)
    gauge = make_vertical_bar(p_val, center=[-5.8, -0.05, 0], height=1.8, width=0.34,
                              color=PRESSURE_COL, label="held nearly\nsteady", label_pos=DOWN, label_size=24)

    ra = RoundedRectangle(corner_radius=0.25, width=0.75, height=2.9, color=VESSEL_COL,
                          stroke_width=3, fill_color=VESSEL_COL, fill_opacity=0.16).move_to([ra_x + 0.45, -0.05, 0])
    ra_lab = T("right\natrium", size=24, color=VESSEL_COL).next_to(ra, UP, buff=0.18)

    branches = VGroup()
    taps = VGroup()
    paths = []
    for y, name, fcol in ((y_top, "muscle", FLOW_COL), (y_bot, "other beds", VESSEL_COL)):
        art = Line([aorta_x, y, 0], [-2.5, y, 0], color=VESSEL_COL, stroke_width=10)
        ar_l = Line([-2.5, y + 0.18, 0], [-0.7, y + 0.18, 0], color=ARTERIOLE_COL, stroke_width=4)
        ar_r = Line([-2.5, y - 0.18, 0], [-0.7, y - 0.18, 0], color=ARTERIOLE_COL, stroke_width=4)
        rings = VGroup(*[Line([x, y - 0.24, 0], [x, y + 0.24, 0], color=ARTERIOLE_COL, stroke_width=5)
                         for x in np.linspace(-2.25, -0.95, 4)])
        tap = make_tap_icon([-1.6, y + 0.32, 0], scale=0.85)
        taps.add(tap)
        caps = VGroup(*[
            CubicBezier([-0.7, y, 0], [0.1, y + dy, 0], [1.1, y + dy, 0], [1.9, y, 0],
                        color=CAPILLARY_COL, stroke_width=3)
            for dy in (-0.34, 0.0, 0.34)
        ])
        vein = Line([1.9, y, 0], [ra_x + 0.08, y, 0], color=VESSEL_COL, stroke_width=10)
        lab = T(name, size=28, color=fcol if name == "muscle" else TEXT).move_to([-3.6, y + 0.42, 0])
        branches.add(VGroup(art, ar_l, ar_r, rings, caps, vein, lab))
        for dy in (-0.20, 0.20):
            paths.append([[aorta_x, y, 0], [-2.5, y, 0], [-0.7, y, 0], [0.6, y + dy, 0], [1.9, y, 0], [ra_x + 0.08, y, 0]])

    dots = make_flowing_dots(paths, lambda: 0.45, color=BLOOD_COL, per_path=5, radius=0.05, seed=7)
    world = VGroup(aorta, aorta_lab, gauge, ra, ra_lab, branches, taps, dots)
    world.taps = taps
    world.p_val = p_val
    world.dots = dots
    return world


# ------------------------------------------------------------------ WORLD B: SINGLE BED (s00 zoom -> s09)
def make_single_bed(p_tracker, res_tracker, flow_tracker, r_tracker=None, tissue_label="working",
                    is_heart=False, arteriole_label=None, show_res_bar=False, show_flow_bar=True,
                    bed_x=-3.0, seed=7):
    """Main left-55% single vascular bed filling ~70% of frame height (y = -2.6 .. +2.5)."""
    r_fn = (lambda: r_tracker.get_value()) if r_tracker is not None else (lambda: radius_from_res(res_tracker.get_value()))

    art_y0, art_y1 = 2.45, 1.72
    art_w = 0.36
    artery = VGroup(
        Line([bed_x - art_w, art_y0, 0], [bed_x - art_w, art_y1, 0], color=VESSEL_COL, stroke_width=6.5),
        Line([bed_x + art_w, art_y0, 0], [bed_x + art_w, art_y1, 0], color=VESSEL_COL, stroke_width=6.5),
    )

    gauge = make_vertical_bar(p_tracker, center=[-5.52, 1.50, 0], height=1.85, width=0.42,
                              color=PRESSURE_COL, label="perfusion\npressure", label_pos=DOWN, label_size=24)
    tap_line = DashedLine([-5.28, 2.08, 0], [bed_x - art_w - 0.05, 2.08, 0], color=PRESSURE_COL, stroke_width=2.5, dash_length=0.12)

    ar_y0, ar_y1 = 1.72, 0.75

    def mk_arteriole():
        r = float(r_fn())
        lw = Line([bed_x - r, ar_y0, 0], [bed_x - r, ar_y1, 0], color=ARTERIOLE_COL, stroke_width=6)
        rw = Line([bed_x + r, ar_y0, 0], [bed_x + r, ar_y1, 0], color=ARTERIOLE_COL, stroke_width=6)
        ring_w = 5.5 + max(0.0, (0.28 - r) * 18.0)
        rings = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=2 * r + 0.18, height=0.11,
                             stroke_color=ARTERIOLE_COL, stroke_width=ring_w * 0.55,
                             fill_color=ARTERIOLE_COL, fill_opacity=0.28).move_to([bed_x, y, 0])
            for y in np.linspace(ar_y1 + 0.14, ar_y0 - 0.14, 4)
        ])
        top_c = VGroup(
            Line([bed_x - art_w, art_y1, 0], [bed_x - r, ar_y0, 0], color=VESSEL_COL, stroke_width=5),
            Line([bed_x + art_w, art_y1, 0], [bed_x + r, ar_y0, 0], color=VESSEL_COL, stroke_width=5),
        )
        return VGroup(top_c, lw, rw, rings)

    arteriole_dyn = always_redraw(mk_arteriole)
    arteriole_dyn.layout_ok = True

    def mk_endo():
        r = float(r_fn()) - 0.04
        return VGroup(
            Line([bed_x - r, ar_y0 - 0.05, 0], [bed_x - r, ar_y1 + 0.05, 0], color=NO_COL, stroke_width=3.5),
            Line([bed_x + r, ar_y0 - 0.05, 0], [bed_x + r, ar_y1 + 0.05, 0], color=NO_COL, stroke_width=3.5),
        )

    endo = always_redraw(mk_endo).set_opacity(0.0)
    endo.layout_ok = True

    def mk_tap():
        r = float(r_fn())
        ang = (r - 0.26) * 3.2
        c = np.array([bed_x + r + 0.28, (ar_y0 + ar_y1) / 2, 0])
        stem = Line(c + LEFT * 0.16, c + RIGHT * 0.12, color=ARTERIOLE_COL, stroke_width=4.5)
        pivot = c + RIGHT * 0.12
        knob = Circle(radius=0.05, color=ARTERIOLE_COL, fill_color=ARTERIOLE_COL, fill_opacity=1.0).move_to(pivot)
        bar = Line(pivot + DOWN * 0.20, pivot + UP * 0.20, color=ARTERIOLE_COL, stroke_width=5.5)
        bar.add(Dot(bar.get_top(), radius=0.04, color=ARTERIOLE_COL))
        bar.add(Dot(bar.get_bottom(), radius=0.04, color=ARTERIOLE_COL))
        bar.rotate(ang, about_point=pivot)
        return VGroup(stem, knob, bar)

    tap_dyn = always_redraw(mk_tap)
    tap_dyn.layout_ok = True

    tis_top, tis_bot = 0.16, -2.02
    tis_w, tis_h = 3.20, tis_top - tis_bot
    tissue_box = RoundedRectangle(corner_radius=0.22, width=tis_w, height=tis_h,
                                  stroke_color=VESSEL_COL, stroke_width=3.2,
                                  fill_color="#323F5B", fill_opacity=0.88).move_to([bed_x, (tis_top + tis_bot) / 2, 0])
    cap_xs = [bed_x - 1.26, bed_x - 0.94, bed_x + 0.94, bed_x + 1.26]
    capillaries = VGroup()
    cap_paths = []
    for cx in cap_xs:
        p0 = np.array([bed_x + np.sign(cx - bed_x) * 0.28, ar_y1, 0])
        p1 = np.array([cx, 0.02, 0])
        p2 = np.array([cx, -1.82, 0])
        p3 = np.array([bed_x + np.sign(cx - bed_x) * 0.16, -2.20, 0])
        c1 = CubicBezier(p0, [cx, ar_y1, 0], [cx, 0.35, 0], p1, color=CAPILLARY_COL, stroke_width=4.2)
        mid = Line(p1, p2, color=CAPILLARY_COL, stroke_width=4.2)
        c2 = CubicBezier(p2, [cx, -2.04, 0], [p3[0], -2.00, 0], p3, color=CAPILLARY_COL, stroke_width=4.2)
        capillaries.add(VGroup(c1, mid, c2))
        cap_paths.append([[bed_x, art_y0, 0], [bed_x, ar_y1, 0], p0, [cx, 0.50, 0], p1, p2, [bed_x, -2.20, 0], [bed_x, -2.85, 0]])

    striations = VGroup()
    if is_heart:
        for yy in np.linspace(tis_bot + 0.34, tis_top - 0.34, 6):
            striations.add(Line([bed_x - 1.52, yy, 0], [bed_x - 1.34, yy, 0],
                                color=BLOOD_COL, stroke_width=2.4).set_opacity(0.40))
            striations.add(Line([bed_x + 1.34, yy, 0], [bed_x + 1.52, yy, 0],
                                color=BLOOD_COL, stroke_width=2.4).set_opacity(0.40))

    vein_w = 0.38
    vein = VGroup(
        Line([bed_x - vein_w, -2.20, 0], [bed_x - vein_w, -2.90, 0], color=VESSEL_COL, stroke_width=6.5),
        Line([bed_x + vein_w, -2.20, 0], [bed_x + vein_w, -2.90, 0], color=VESSEL_COL, stroke_width=6.5),
    )

    dots = make_flowing_dots(cap_paths, flow_tracker.get_value, color=BLOOD_COL, per_path=8, radius=0.072, seed=seed)

    g = VGroup(tissue_box, striations, artery, capillaries, vein, arteriole_dyn, endo, tap_dyn, gauge, tap_line, dots)
    g.tissue_box = tissue_box
    g.arteriole_dyn = arteriole_dyn
    g.endo = endo
    g.tap_dyn = tap_dyn
    g.gauge = gauge
    g.dots = dots
    g.cap_paths = cap_paths
    g.bed_x = bed_x

    if tissue_label:
        tlab = T(tissue_label, size=26, color=TEXT).move_to([-5.25, -2.42, 0])
        g.add(tlab)
        g.tissue_label = tlab

    if arteriole_label:
        alab = T(arteriole_label, size=26, color=ARTERIOLE_COL).move_to([-3.0, 2.74, 0])
        g.add(alab)
        g.arteriole_label = alab

    if show_flow_bar:
        fbar = make_vertical_bar(flow_tracker, center=[-0.38, -1.35, 0], height=1.65, width=0.42,
                                 color=FLOW_COL, label="flow", label_pos=DOWN, label_size=26)
        g.add(fbar)
        g.flow_bar = fbar

    if show_res_bar:
        rbar = make_vertical_bar(res_tracker, center=[-0.38, 0.95, 0], height=1.55, width=0.42,
                                 color=PRESSURE_COL, label="resistance", label_pos=UP, label_size=26)
        g.add(rbar)
        g.res_bar = rbar

    return g


def make_autoreg_plot():
    """Schematic autoregulation plot on the right 45% (no numbers, 'nearly level' middle)."""
    return Plot(box=(1.05, 6.05, -1.95, 1.75), xr=(0.0, 1.0), yr=(0.0, 1.0),
                xticks=(), yticks=(), xlabel="perfusion pressure", ylabel="flow", color=TEXT, label_size=26)


def make_nearly_level_brace(P):
    """Bracket over the middle range of the autoregulation curve labelled 'nearly level'."""
    p0 = P.pt(0.28, autoreg_flow(0.28) + 0.08)
    p1 = P.pt(0.72, autoreg_flow(0.72) + 0.08)
    br = BraceBetweenPoints(p0, p1, direction=UP, color=GOLD)
    lab = T("nearly level", size=26, color=GOLD).next_to(br, UP, buff=0.14)
    return VGroup(br, lab)


# ------------------------------------------------------------------ WORLD C: FOUR PARALLEL BRANCHES (s10 -> s14)
BRANCH_YS = {"heart": 2.00, "brain": 0.68, "muscle": -0.64, "skin": -1.96}


def _branch_op_anims(organ_grp, hand, op):
    """Animate branch & hand opacity without filling hollow capillaries or hand outlines."""
    art, pad, caps, vein, org_lab = organ_grp
    return [
        art.animate.set_stroke(opacity=op),
        pad.animate.set_stroke(opacity=op).set_fill(opacity=0.60 * op),
        caps.animate.set_stroke(opacity=op),
        vein.animate.set_stroke(opacity=op),
        org_lab.animate.set_opacity(op),
        hand.animate.set_stroke(opacity=op).set_fill(opacity=0.08 * op),
    ]


def make_four_branch_world(radii_trackers, flow_trackers, active_organs=None,
                           show_hands=False, show_glow_taps=False, seed=7):
    """Four parallel organ beds off the SLATE aorta, rejoining at the right atrium (x = -5.5 .. +2.2)."""
    aorta_x, ra_x = -4.85, 1.85
    y_top, y_bot = BRANCH_YS["heart"], BRANCH_YS["skin"]

    aorta = Line([aorta_x, y_bot - 0.35, 0], [aorta_x, y_top + 0.35, 0], color=VESSEL_COL, stroke_width=13)
    aorta_lab = T("aorta", size=26, color=VESSEL_COL).next_to(aorta, UP, buff=0.15).shift(LEFT * 0.28)

    p_aorta = ValueTracker(0.65)
    gauge = make_vertical_bar(p_aorta, center=[-5.85, 0.02, 0], height=2.3, width=0.38,
                              color=PRESSURE_COL, label="pressure", label_pos=DOWN, label_size=24)

    ra = RoundedRectangle(corner_radius=0.20, width=0.55, height=4.5, color=VESSEL_COL,
                          stroke_width=3, fill_color=VESSEL_COL, fill_opacity=0.22).move_to([ra_x + 0.35, 0.02, 0])
    ra_lab = T("right\natrium", size=24, color=VESSEL_COL).next_to(ra, UP, buff=0.14)

    organ_groups = {}
    branch_dots = {}
    hands = {}
    taps = {}

    for idx, (org, y) in enumerate(BRANCH_YS.items()):
        op = 1.0 if (active_organs is None or org in active_organs) else 0.32
        r_trk = radii_trackers[org]
        f_trk = flow_trackers[org]

        art = Line([aorta_x, y, 0], [-3.35, y, 0], color=VESSEL_COL, stroke_width=8).set_stroke(opacity=op)
        org_col = FLOW_COL if org == "muscle" else TEXT
        org_lab = T(org, size=26, color=org_col).move_to([-4.02, y + 0.42, 0]).set_opacity(op)

        def mk_ar(y=y, trk=r_trk, op=op):
            r = float(trk.get_value())
            top = Line([-3.35, y + r, 0], [-1.75, y + r, 0], color=ARTERIOLE_COL, stroke_width=4.5)
            bot = Line([-3.35, y - r, 0], [-1.75, y - r, 0], color=ARTERIOLE_COL, stroke_width=4.5)
            rings = VGroup(*[
                Line([x, y - r - 0.06, 0], [x, y + r + 0.06, 0], color=ARTERIOLE_COL, stroke_width=4.5)
                for x in np.linspace(-3.12, -1.98, 4)
            ])
            return VGroup(top, bot, rings).set_stroke(opacity=op)

        ar_dyn = always_redraw(mk_ar)
        ar_dyn.layout_ok = True

        tap = make_tap_icon([-2.55, y + 0.34, 0], scale=0.72,
                            angle_fn=(lambda trk=r_trk: (trk.get_value() - 0.16) * 4.5),
                            glow=show_glow_taps)
        tap.set_stroke(opacity=op)
        taps[org] = tap

        pad = RoundedRectangle(corner_radius=0.14, width=2.05, height=0.78, stroke_color=VESSEL_COL,
                               stroke_width=2.2, fill_color="#303C56", fill_opacity=0.80 * op).move_to([-0.75, y, 0]).set_stroke(opacity=op)
        caps = VGroup(*[
            CubicBezier([-1.75, y, 0], [-1.15, y + dy, 0], [-0.35, y + dy, 0], [0.25, y, 0],
                        color=CAPILLARY_COL, stroke_width=3.2, fill_opacity=0.0).set_stroke(opacity=op)
            for dy in (-0.25, 0.0, 0.25)
        ])
        vein = Line([0.25, y, 0], [ra_x + 0.08, y, 0], color=VESSEL_COL, stroke_width=8).set_stroke(opacity=op)

        dcol = FLOW_COL if org == "muscle" else BLOOD_COL
        paths = [
            [[aorta_x, y, 0], [-3.35, y, 0], [-1.75, y, 0], [-0.75, y + dy, 0], [0.25, y, 0], [ra_x + 0.08, y, 0]]
            for dy in (-0.16, 0.16)
        ]
        dots = make_flowing_dots(paths, f_trk.get_value, color=dcol, per_path=6, radius=0.058, seed=seed + idx, opacity=op)
        branch_dots[org] = dots

        grp = VGroup(art, pad, caps, vein, org_lab)
        organ_groups[org] = (grp, ar_dyn)

        hand = make_hand_outline([-2.02, y + 0.50, 0], scale=0.46, color=TEXT, variant=idx)
        if show_hands:
            hand.set_stroke(opacity=op).set_fill(opacity=0.08 * op)
        else:
            hand.set_stroke(opacity=0.0).set_fill(opacity=0.0)
        hands[org] = hand

    static_grp = VGroup(aorta, aorta_lab, ra, ra_lab, *[g for g, _ in organ_groups.values()])
    dyn_grp = VGroup(gauge, *[a for _, a in organ_groups.values()], *taps.values(), *branch_dots.values(), *hands.values())
    world = VGroup(static_grp, dyn_grp)
    refs = {
        "static": static_grp,
        "dyn": dyn_grp,
        "organ_groups": {o: g for o, (g, _) in organ_groups.items()},
        "hands": hands,
        "taps": taps,
        "dots": branch_dots,
        "p_aorta": p_aorta,
    }
    return world, refs


def default_four_trackers(r_init=0.14, f_init=0.35):
    radii = {o: ValueTracker(r_init) for o in BRANCH_YS}
    flows = {o: ValueTracker(f_init) for o in BRANCH_YS}
    return radii, flows


def make_signal_stream(start, end, color=SIGNAL_COL, n=8, seed=11, radius=0.045, speed=0.65):
    """Animated stream of dots travelling from `start` to `end`."""
    rng = np.random.default_rng(seed)
    p0, p1 = np.array(start, dtype=float), np.array(end, dtype=float)
    perp = np.array([-(p1[1] - p0[1]), p1[0] - p0[0], 0.0])
    nrm = np.linalg.norm(perp)
    if nrm > 1e-6:
        perp /= nrm
    g = VGroup()
    for i in range(n):
        d = Dot(radius=radius, color=color).set_opacity(0.9)
        d._u = (i / n + rng.uniform(0, 0.05)) % 1.0
        d._lat = rng.uniform(-0.14, 0.14)

        def upd(mob, dt, s=speed):
            mob._u = (mob._u + s * dt) % 1.0
            pos = (1.0 - mob._u) * p0 + mob._u * p1 + perp * mob._lat * np.sin(mob._u * PI)
            mob.move_to(pos)
            mob.set_opacity(0.95 * np.sin(mob._u * PI) + 0.05)

        d.move_to((1.0 - d._u) * p0 + d._u * p1)
        d.add_updater(upd)
        g.add(d)
    g.layout_ok = True
    return g


def make_transmural_arrows(bed_x=-3.0, y_mid=1.0, r_fn=None):
    """Small WHITE outward arrows pressing on the arteriole wall from inside (myogenic response)."""
    def mk():
        r = float(r_fn()) if r_fn else 0.22
        arrows = VGroup()
        for yy in (y_mid - 0.25, y_mid + 0.25):
            arrows.add(Arrow([bed_x - 0.04, yy, 0], [bed_x - r + 0.02, yy, 0],
                             color=PRESSURE_COL, stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.45))
            arrows.add(Arrow([bed_x + 0.04, yy, 0], [bed_x + r - 0.02, yy, 0],
                             color=PRESSURE_COL, stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.45))
        return arrows
    g = always_redraw(mk)
    g.layout_ok = True
    return g


# ------------------------------------------------------------------ SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        two = make_two_branch_world()
        self.add(two)

        self.at("each tissue sets")
        glows = VGroup(*[Circle(radius=0.35, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.22).move_to(t.get_center())
                         for t in two.taps])
        self.play(FadeIn(glows), run_time=0.45)
        self.play(FadeOut(glows), run_time=0.45)

        self.at("by its arterioles")
        p_trk = ValueTracker(0.55)
        res_trk = ValueTracker(0.55)
        flow_trk = ValueTracker(0.45)
        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="muscle")
        self.play(FadeOut(two, run_time=0.6))
        self.play(FadeIn(bed, run_time=0.8))

        self.at("who turns that tap")
        hand = make_hand_outline([bed.bed_x + 0.72, 1.38, 0], scale=0.65, color=TEXT)
        qmark = T("?", size=34, color=GOLD, weight=BOLD).next_to(hand, RIGHT, buff=0.14)
        q_top = T("Who turns the tap?", size=34, color=TEXT).move_to([0.0, 3.25, 0])
        self.play(FadeIn(hand, shift=DOWN * 0.15), FadeIn(qmark), FadeIn(q_top), run_time=0.6)

        self.at("listen to")
        self.play(Indicate(qmark, color=GOLD, scale_factor=1.18), run_time=0.6)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.55)
        res_trk = ValueTracker(0.55)
        flow_trk = ValueTracker(0.45)
        r_trk = ValueTracker(0.26)
        r_trk._t = 0.0
        r_trk.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt), m.set_value(0.26 + 0.015 * np.sin(3.2 * m._t))))
        self.add(r_trk)

        bed = make_single_bed(p_trk, res_trk, flow_trk, r_tracker=r_trk, tissue_label="muscle")
        q_top = T("Who turns the tap?", size=34, color=TEXT).move_to([0.0, 3.25, 0])
        title = T("Who Turns the Tap", size=44, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.25, 0])
        self.add(bed, q_top)
        self.play(swap(q_top, title, run_time=0.9))
        self.wait(0.8)
        self.finish()


class S02Work(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.55)
        res_trk = ValueTracker(0.55)
        flow_trk = ValueTracker(0.42)
        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="muscle")
        title = T("Who Turns the Tap", size=44, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.25, 0])
        self.add(bed, title)
        self.play(FadeOut(title, run_time=0.35))

        self.at("works harder")
        work_lab = T("working", size=28, color=SIGNAL_COL).move_to(bed.tissue_label.get_center())
        work_pulse = RoundedRectangle(corner_radius=0.22, width=3.24, height=2.22,
                                      stroke_color=SIGNAL_COL, stroke_width=5, fill_color=SIGNAL_COL,
                                      fill_opacity=0.14).move_to(bed.tissue_box)
        work_pulse._pt = 0.0
        work_pulse.add_updater(lambda m, dt: (
            setattr(m, "_pt", m._pt + dt),
            m.set_stroke(opacity=0.45 + 0.45 * np.sin(6.5 * m._pt)),
            m.set_fill(opacity=0.08 + 0.16 * (0.5 + 0.5 * np.sin(6.5 * m._pt))),
        ))
        self.play(swap(bed.tissue_label, work_lab, run_time=0.45), FadeIn(work_pulse, run_time=0.4))

        self.at("arterioles relax")
        self.play(res_trk.animate.set_value(0.22), flow_trk.animate.set_value(0.86), run_time=1.4)

        self.at("flow follows")
        sig_stream = make_signal_stream([bed.bed_x - 0.3, 0.08, 0], [bed.bed_x - 0.18, 1.15, 0],
                                        color=SIGNAL_COL, n=10, seed=11, radius=0.062, speed=0.65)
        sig_tag = T("tissue signals", size=28, color=SIGNAL_COL).move_to([1.3, 2.25, 0])
        self.play(FadeIn(sig_stream), FadeIn(sig_tag), run_time=0.6)

        self.at("several overlap")
        self.play(Indicate(sig_tag, color=SIGNAL_COL, scale_factor=1.08), run_time=0.5)

        self.at("working tissue")
        self.play(FadeOut(work_lab, run_time=0.35))

        col_x = 1.65
        col_ys = [1.55, 0.90, 0.25, -0.40, -1.05]
        names_cues = [
            ("adenosine", "adenosine"),
            ("potassium", "K\u207a"),
            ("carbon dioxide", "CO\u2082"),
            ("hydrogen ions", "H\u207a"),
            ("low oxygen", "low O\u2082"),
        ]
        tags = VGroup()
        for (cue, txt), yy in zip(names_cues, col_ys):
            self.at(cue)
            t = T(txt, size=28, color=SIGNAL_COL).move_to([col_x, yy, 0])
            tags.add(t)
            self.play(FadeIn(t, shift=RIGHT * 0.15), run_time=0.35)

        self.at("the endothelium")
        no_stream = make_signal_stream([bed.bed_x + 0.18, 0.72, 0], [bed.bed_x + 0.35, 1.45, 0],
                                       color=NO_COL, n=8, seed=19, radius=0.062, speed=0.65)
        no_tag = T("nitric oxide", size=28, color=NO_COL).move_to([1.65, -1.85, 0])
        self.play(bed.endo.animate.set_opacity(0.95), FadeIn(no_stream), run_time=0.5)
        self.at("nitric oxide")
        self.play(FadeIn(no_tag, shift=UP * 0.1), run_time=0.4)
        self.finish()


class S03Autoreg(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.50)
        res_trk = ValueTracker(0.22)
        flow_trk = ValueTracker(0.86)
        self.add(p_trk, res_trk, flow_trk)
        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label=None)

        sig_tag = T("tissue signals", size=28, color=SIGNAL_COL).move_to([1.3, 2.25, 0])
        no_tag = T("nitric oxide", size=28, color=NO_COL).move_to([1.65, -1.85, 0])
        self.add(bed, sig_tag, no_tag)
        demand_lab = T("demand fixed", size=26, color=TEXT).move_to([-5.25, -2.42, 0])
        self.play(FadeOut(sig_tag, run_time=0.35), FadeOut(no_tag, run_time=0.35),
                  res_trk.animate.set_value(0.55), flow_trk.animate.set_value(0.50),
                  FadeIn(demand_lab, run_time=0.5))

        self.at("hold flow steady")
        flow_trk.add_updater(lambda m: m.set_value(autoreg_flow(p_trk.get_value())))
        res_trk.add_updater(lambda m: m.set_value(autoreg_res(p_trk.get_value())))
        self.play(p_trk.animate.set_value(0.58), run_time=1.0)

        self.at("perfusion pressure changes")
        self.play(p_trk.animate.set_value(0.72), run_time=1.2)
        self.play(p_trk.animate.set_value(0.30), run_time=1.3)

        self.at("demand stays the same")
        self.play(p_trk.animate.set_value(0.64), run_time=1.4)
        self.play(p_trk.animate.set_value(0.45), run_time=1.1)

        self.at("autoregulation")
        head = T("autoregulation", size=34, color=TEXT).move_to([0.0, 3.25, 0])
        P = make_autoreg_plot()
        self.play(FadeIn(head, shift=UP * 0.1), Create(P), run_time=0.9)
        self.finish()


class S04Curve(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.45)
        res_trk = ValueTracker(autoreg_res(0.45))
        flow_trk = ValueTracker(autoreg_flow(0.45))
        flow_trk.add_updater(lambda m: m.set_value(autoreg_flow(p_trk.get_value())))
        res_trk.add_updater(lambda m: m.set_value(autoreg_res(p_trk.get_value())))
        self.add(p_trk, res_trk, flow_trk)

        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="demand fixed")
        head = T("autoregulation", size=34, color=TEXT).move_to([0.0, 3.25, 0])
        P = make_autoreg_plot()
        self.add(bed, head, P)

        self.at("Plot pressure")
        x_hl = Underline(P.xlabel, color=GOLD, stroke_width=4)
        self.play(Create(x_hl), p_trk.animate.set_value(0.05), run_time=0.9)
        self.play(FadeOut(x_hl), run_time=0.35)

        self.at("flow up the side")
        live = P.live_curve(autoreg_flow, p_trk, color=PRESSURE_COL, width=6, x0=0.05)
        dot = P.dot(lambda: p_trk.get_value(), lambda: autoreg_flow(p_trk.get_value()),
                    color=PRESSURE_COL, ring=GOLD, radius=0.13)
        y_hl = Underline(P.ylabel, color=GOLD, stroke_width=4)
        self.play(Create(y_hl), run_time=0.5)
        self.play(FadeOut(y_hl), run_time=0.35)
        self.add(live, dot)

        self.at("At low pressures")
        self.play(p_trk.animate.set_value(0.28), run_time=2.5, rate_func=linear)

        self.at("middle range")
        self.play(p_trk.animate.set_value(0.55), run_time=1.6, rate_func=linear)

        self.at("nearly level")
        brace = make_nearly_level_brace(P)
        self.play(FadeIn(brace), p_trk.animate.set_value(0.72), run_time=1.8, rate_func=linear)

        self.at("Above that range")
        self.play(p_trk.animate.set_value(0.95), run_time=1.8, rate_func=linear)

        self.play(p_trk.animate.set_value(0.45), run_time=1.0)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.36)
        res_trk = ValueTracker(autoreg_res(0.45))
        flow_trk = ValueTracker(autoreg_flow(0.36))
        flow_trk.add_updater(lambda m: m.set_value(autoreg_flow(p_trk.get_value())))
        self.add(p_trk, res_trk, flow_trk)

        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="demand fixed")
        P = make_autoreg_plot()
        curve = P.curve(autoreg_flow, x0=0.05, x1=0.95, color=PRESSURE_COL, width=6)
        brace = make_nearly_level_brace(P)
        dot = P.dot(lambda: p_trk.get_value(), lambda: autoreg_flow(p_trk.get_value()),
                    color=PRESSURE_COL, ring=GOLD, radius=0.13)
        head = T("autoregulation", size=34, color=TEXT).move_to([0.0, 3.25, 0])
        self.add(bed, P, curve, brace, dot, head)

        self.at("flow equals")
        eq = T("flow = pressure drop \u00f7 resistance", size=32, color=PRESSURE_COL).move_to([0.55, 2.75, 0])
        self.play(FadeOut(head, run_time=0.35), FadeIn(eq, run_time=0.6))

        self.at("middle range")
        self.play(p_trk.animate.set_value(0.64), run_time=3.6, rate_func=linear)

        self.at("what must the arterioles")
        outline = RoundedRectangle(corner_radius=0.12, width=1.1, height=1.00,
                                   stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([bed.bed_x, 1.23, 0])
        qmark = T("?", size=36, color=GOLD, weight=BOLD).next_to(outline, LEFT, buff=0.15)
        qcard = question_card("What are the arterioles doing?", color=TEXT, size=34, y=3.32, max_w=10.2)
        self.play(FadeIn(outline), FadeIn(qmark), FadeIn(qcard), run_time=0.7)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "What are the arterioles doing?"
    CARD = {"y": 3.32, "color": TEXT, "size": 34, "max_w": 10.2}
    RING_AT = (5.85, 3.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        p_trk = ValueTracker(0.54)
        p_trk._t = 0.0
        p_trk.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt), m.set_value(0.54 + 0.04 * np.sin(1.8 * m._t))))
        res_trk = ValueTracker(autoreg_res(0.45))
        flow_trk = ValueTracker(autoreg_flow(0.54))
        flow_trk.add_updater(lambda m: m.set_value(autoreg_flow(p_trk.get_value())))

        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="demand fixed")
        P = make_autoreg_plot()
        curve = P.curve(autoreg_flow, x0=0.05, x1=0.95, color=PRESSURE_COL, width=6)
        brace = make_nearly_level_brace(P)
        dot = P.dot(lambda: p_trk.get_value(), lambda: autoreg_flow(p_trk.get_value()),
                    color=PRESSURE_COL, ring=GOLD, radius=0.13)
        eq = T("flow = pressure drop \u00f7 resistance", size=32, color=PRESSURE_COL).move_to([0.55, 2.75, 0])
        outline = RoundedRectangle(corner_radius=0.12, width=1.1, height=1.00,
                                   stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([bed.bed_x, 1.23, 0])
        qmark = T("?", size=36, color=GOLD, weight=BOLD).next_to(outline, LEFT, buff=0.15)
        qmark._pt = 0.0
        qmark.add_updater(lambda m, dt: (setattr(m, "_pt", m._pt + dt),
                                         m.set_opacity(0.65 + 0.35 * np.sin(3.5 * m._pt))))
        return Group(p_trk, res_trk, flow_trk, bed, P, curve, brace, dot, eq, outline, qmark, scope_tag("schematic"))


class S07Answer(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.36)
        res_trk = ValueTracker(autoreg_res(0.36))
        flow_trk = ValueTracker(autoreg_flow(0.36))
        flow_trk.add_updater(lambda m: m.set_value(autoreg_flow(p_trk.get_value())))
        res_trk.add_updater(lambda m: m.set_value(autoreg_res(p_trk.get_value())))
        self.add(p_trk, res_trk, flow_trk)

        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="demand fixed", show_res_bar=True)
        P = make_autoreg_plot()
        curve = P.curve(autoreg_flow, x0=0.05, x1=0.95, color=PRESSURE_COL, width=6)
        brace = make_nearly_level_brace(P)
        dot = P.dot(lambda: p_trk.get_value(), lambda: autoreg_flow(p_trk.get_value()),
                    color=PRESSURE_COL, ring=GOLD, radius=0.13)
        eq = T("flow = pressure drop \u00f7 resistance", size=32, color=PRESSURE_COL).move_to([0.55, 2.75, 0])
        outline = RoundedRectangle(corner_radius=0.12, width=1.1, height=1.00,
                                   stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([bed.bed_x, 1.23, 0])
        qmark = T("?", size=36, color=GOLD, weight=BOLD).next_to(outline, LEFT, buff=0.15)
        qcard = question_card("What are the arterioles doing?", color=TEXT, size=34, y=3.32, max_w=10.2)

        self.add(bed, P, curve, brace, dot, eq, outline, qmark, qcard)

        self.at("narrowing")
        self.play(FadeOut(qcard), FadeOut(outline), FadeOut(qmark), run_time=0.55)

        self.at("while pressure rises")
        self.play(p_trk.animate.set_value(0.68), run_time=1.55, rate_func=linear)

        self.at("resistance must rise")
        self.play(Indicate(bed.res_bar.frame, color=GOLD, scale_factor=1.06), run_time=0.7)

        self.at("When pressure falls")
        self.play(p_trk.animate.set_value(0.32), run_time=2.4, rate_func=linear)

        self.at("myogenic response")
        arrows = make_transmural_arrows(bed_x=bed.bed_x, y_mid=1.23,
                                        r_fn=lambda: radius_from_res(res_trk.get_value()))
        myo_lab = T("myogenic response", size=28, color=ARTERIOLE_COL).move_to([0.0, 3.30, 0])
        self.play(FadeIn(arrows), FadeIn(myo_lab), run_time=0.6)
        self.play(p_trk.animate.set_value(0.56), run_time=2.2)
        self.finish()


class S08Berne(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.52)
        res_trk = ValueTracker(0.58)
        flow_trk = ValueTracker(0.45)

        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="heart muscle",
                              is_heart=True, arteriole_label="coronary arteriole", show_res_bar=True)
        bed.tissue_box._ht = 0.0
        bed.tissue_box.add_updater(lambda m, dt: (
            setattr(m, "_ht", m._ht + dt),
            m.set_fill(opacity=0.68 + 0.22 * np.sin(5.2 * m._ht)),
        ))
        P = make_autoreg_plot()
        curve = P.curve(autoreg_flow, x0=0.05, x1=0.95, color=PRESSURE_COL, width=6)
        self.add(bed, P, curve)

        self.at("In the heart")
        self.play(FadeOut(P, run_time=0.5), FadeOut(curve, run_time=0.5))

        self.at("1963")
        berne_tag = T("Berne, 1963", size=28, color=TEXT).move_to([-5.3, 3.25, 0])
        self.play(FadeIn(berne_tag, shift=UP * 0.1), run_time=0.5)

        self.at("short of oxygen")
        o2_trk = ValueTracker(0.88)
        o2_gauge = make_vertical_bar(o2_trk, center=[2.0, 0.35, 0], height=1.95, width=0.44,
                                     color=CAPILLARY_COL, label="oxygen\nsupply", label_pos=DOWN, label_size=26)
        self.play(FadeIn(o2_gauge), run_time=0.4)
        self.play(o2_trk.animate.set_value(0.18), run_time=1.5)

        self.at("Coronary resistance fell")
        self.play(res_trk.animate.set_value(0.24), flow_trk.animate.set_value(0.85), run_time=1.3)

        self.at("breakdown products")
        bp_stream = make_signal_stream([bed.bed_x + 0.1, -1.65, 0], [bed.bed_x + 0.1, -2.85, 0],
                                       color=SIGNAL_COL, n=9, seed=23, radius=0.062, speed=0.75)
        bp_lab = T("breakdown products", size=28, color=SIGNAL_COL).move_to([2.4, -2.15, 0])
        self.play(FadeIn(bp_stream), FadeIn(bp_lab), run_time=0.6)
        self.finish()


class S09Adenosine(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        p_trk = ValueTracker(0.52)
        res_trk = ValueTracker(0.48)
        flow_trk = ValueTracker(0.48)
        bed = make_single_bed(p_trk, res_trk, flow_trk, tissue_label="heart muscle",
                              is_heart=True, arteriole_label="coronary arteriole", show_res_bar=False)
        bed.tissue_box._ht = 0.0
        bed.tissue_box.add_updater(lambda m, dt: (
            setattr(m, "_ht", m._ht + dt),
            m.set_fill(opacity=0.68 + 0.22 * np.sin(5.2 * m._ht)),
        ))
        o2_trk = ValueTracker(0.20)
        o2_gauge = make_vertical_bar(o2_trk, center=[1.45, 0.35, 0], height=1.85, width=0.42,
                                     color=CAPILLARY_COL, label="oxygen\nsupply", label_pos=DOWN, label_size=24)
        self.add(bed, o2_gauge)

        self.at("proposed that adenosine")
        prop_tag = T("Berne's proposal", size=28, color=TEXT).move_to([-5.0, 3.25, 0])
        atp_tok = chip("ATP", color=SIGNAL_COL, size=24, pad=0.12).move_to([bed.bed_x, -0.95, 0])
        self.play(FadeIn(prop_tag), FadeIn(atp_tok), run_time=0.55)

        self.at("breaks down")
        ad_tok = chip("adenosine", color=SIGNAL_COL, size=22, pad=0.12).move_to([bed.bed_x, -0.75, 0])
        ad_tok[0].set_fill(BG, opacity=0.95)
        rem_dot = Dot(radius=0.075, color=SIGNAL_COL).move_to([bed.bed_x, -1.45, 0])
        self.play(FadeOut(atp_tok, run_time=0.25), FadeIn(ad_tok, run_time=0.4), FadeIn(rem_dot, run_time=0.4))

        self.at("diffuses")
        ad_stream = make_signal_stream([bed.bed_x, 0.16, 0], [bed.bed_x, 1.40, 0],
                                       color=SIGNAL_COL, n=7, seed=29, radius=0.06, speed=0.70)
        self.play(ad_tok.animate.move_to([bed.bed_x, -0.35, 0]), FadeIn(ad_stream), run_time=1.0)

        self.at("dilates them")
        self.play(res_trk.animate.set_value(0.22), flow_trk.animate.set_value(0.86), run_time=1.1)

        self.at("blockade studies")
        blk = boxed_label("blocker", color=RED, size=24, pad=0.14, fill_opacity=0.22).move_to([bed.bed_x, -0.45, 0])
        blk.box.set_fill(BG, opacity=0.95)
        stop_bar = Line([bed.bed_x - 0.22, 0.45, 0], [bed.bed_x + 0.22, 0.45, 0], color=RED, stroke_width=4.5)
        self.play(FadeOut(ad_tok, run_time=0.25), FadeOut(ad_stream, run_time=0.25),
                  FadeIn(blk, shift=RIGHT * 0.20, run_time=0.50), Create(stop_bar, run_time=0.45))

        self.at("potent dilator")
        norm_val = ValueTracker(0.82)
        short_val = ValueTracker(0.82)
        bar_n = make_vertical_bar(norm_val, center=[3.25, 0.35, 0], height=2.0, width=0.48,
                                  color=FLOW_COL, label="normal\noxygen", label_pos=DOWN, label_size=24)
        bar_s = make_vertical_bar(short_val, center=[5.15, 0.35, 0], height=2.0, width=0.48,
                                  color=FLOW_COL, label="oxygen\nshort", label_pos=DOWN, label_size=24)
        ref_n = DashedLine([2.95, 1.15, 0], [3.55, 1.15, 0], color=TEXT, stroke_width=2.5)
        ref_s = DashedLine([4.85, 1.15, 0], [5.45, 1.15, 0], color=TEXT, stroke_width=2.5)
        self.play(FadeIn(bar_n), FadeIn(bar_s), FadeIn(ref_n), FadeIn(ref_s), run_time=0.7)

        self.at("unless oxygen delivery")
        overlap_tag = T("other signals likely overlap", size=26, color=SIGNAL_COL).move_to([4.15, -2.15, 0])
        self.play(norm_val.animate.set_value(0.76), short_val.animate.set_value(0.36),
                  FadeIn(overlap_tag, shift=UP * 0.1), run_time=1.3)
        self.finish()


class S10Idea(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        radii, flows = default_four_trackers(r_init=0.14, f_init=0.35)
        world, refs = make_four_branch_world(radii, flows, show_hands=False, show_glow_taps=False)

        self.play(FadeIn(world), run_time=0.9)

        self.at("arterioles are the tap")
        glows = VGroup(*[
            Circle(radius=0.28, color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.22)
            .move_to(refs["taps"][o].get_center())
            for o in BRANCH_YS
        ])
        self.play(FadeIn(glows), run_time=0.5)
        self.play(FadeOut(glows), run_time=0.5)

        self.at("who turns it")
        head = T("Same tap. Different hands.", size=34, color=TEXT).move_to([0.0, 3.35, 0])
        self.play(
            *[refs["hands"][o].animate.set_stroke(opacity=1.0).set_fill(opacity=0.08) for o in BRANCH_YS],
            FadeIn(head, shift=UP * 0.1),
            run_time=0.7,
        )
        self.finish()


class S11HeartBrain(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        radii, flows = default_four_trackers(r_init=0.14, f_init=0.35)
        world, refs = make_four_branch_world(radii, flows, active_organs=set(BRANCH_YS), show_hands=True)
        head = T("Same tap. Different hands.", size=34, color=TEXT).move_to([0.0, 3.35, 0])
        self.add(world, head)

        self.at("In the heart")
        heart_sigs = make_signal_stream([-0.8, BRANCH_YS["heart"], 0], [-2.02, BRANCH_YS["heart"] + 0.42, 0],
                                        color=SIGNAL_COL, n=7, seed=31, radius=0.055, speed=0.80)
        heart_tag = T("metabolism", size=28, color=SIGNAL_COL).move_to([4.15, BRANCH_YS["heart"], 0])
        anims = []
        for o in BRANCH_YS:
            anims.extend(_branch_op_anims(refs["organ_groups"][o], refs["hands"][o], 1.0 if o == "heart" else 0.30))
        self.play(
            *anims,
            refs["hands"]["heart"].animate.set_stroke(color=SIGNAL_COL, opacity=1.0).set_fill(color=SIGNAL_COL, opacity=0.32),
            FadeIn(heart_sigs), FadeIn(heart_tag),
            radii["heart"].animate.set_value(0.23), flows["heart"].animate.set_value(0.75),
            run_time=1.0,
        )

        self.at("In the brain")
        y_br = BRANCH_YS["brain"]
        soma = Dot([3.15, y_br + 0.32, 0], radius=0.11, color=NERVE_COL)
        dend = VGroup(*[
            Line(soma.get_center(), soma.get_center() + np.array([dx, dy, 0]), color=NERVE_COL, stroke_width=2.8)
            for dx, dy in [(-0.22, 0.14), (-0.25, -0.08), (0.05, 0.24), (0.20, 0.14)]
        ])
        axon = CubicBezier(
            soma.get_center(),
            [1.6, y_br + 0.62, 0],
            [-0.4, y_br + 0.68, 0],
            [-2.02, y_br + 0.50, 0],
            color=NERVE_COL, stroke_width=3.5,
        )
        neuron = VGroup(dend, axon, soma)
        brain_tag = T("neural activity", size=26, color=TEXT).move_to([4.75, y_br + 0.32, 0])
        self.play(
            *_branch_op_anims(refs["organ_groups"]["heart"], refs["hands"]["heart"], 0.35),
            *_branch_op_anims(refs["organ_groups"]["brain"], refs["hands"]["brain"], 1.0),
            FadeIn(neuron), FadeIn(brain_tag),
            run_time=0.6,
        )

        self.at("active neurons")
        spark = Dot(soma.get_center(), radius=0.075, color=GOLD)
        self.play(MoveAlongPath(spark, axon),
                  refs["hands"]["brain"].animate.set_stroke(color=NERVE_COL, opacity=1.0).set_fill(color=NERVE_COL, opacity=0.32),
                  radii["brain"].animate.set_value(0.22), flows["brain"].animate.set_value(0.72),
                  run_time=0.9)
        self.play(FadeOut(spark, run_time=0.25))

        self.at("Carbon dioxide")
        co2_trk = ValueTracker(0.50)
        co2_gauge = make_vertical_bar(co2_trk, center=[3.35, BRANCH_YS["brain"] - 0.32, 0], height=0.85, width=0.28,
                                      color=SIGNAL_COL, label="CO\u2082", label_pos=RIGHT, label_size=26)
        self.play(FadeIn(co2_gauge), run_time=0.5)

        self.at("A rise dilates")
        self.play(co2_trk.animate.set_value(0.92), radii["brain"].animate.set_value(0.26),
                  flows["brain"].animate.set_value(0.88), run_time=1.2)

        self.at("a fall constricts")
        self.play(co2_trk.animate.set_value(0.15), radii["brain"].animate.set_value(0.10),
                  flows["brain"].animate.set_value(0.22), run_time=1.3)
        self.finish()


class S12Muscle(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        radii, flows = default_four_trackers(r_init=0.14, f_init=0.35)
        active = {"muscle"}
        world, refs = make_four_branch_world(radii, flows, active_organs=active, show_hands=True)
        head = T("Same tap. Different hands.", size=34, color=TEXT).move_to([0.0, 3.35, 0])
        self.add(world, head)

        self.at("In working muscle")
        mus_sigs = make_signal_stream([-0.8, BRANCH_YS["muscle"], 0], [-2.02, BRANCH_YS["muscle"] + 0.42, 0],
                                      color=SIGNAL_COL, n=8, seed=41, radius=0.055, speed=0.85)
        self.play(FadeIn(mus_sigs),
                  refs["hands"]["muscle"].animate.set_stroke(color=SIGNAL_COL, opacity=1.0).set_fill(color=SIGNAL_COL, opacity=0.32),
                  radii["muscle"].animate.set_value(0.26), flows["muscle"].animate.set_value(0.90),
                  run_time=1.0)

        self.at("no single dilator")
        bar_x, bar_y = 4.35, BRANCH_YS["muscle"] + 0.15
        bar_w, bar_h = 2.8, 0.42
        whole_bar = RoundedRectangle(corner_radius=0.06, width=bar_w, height=bar_h,
                                     stroke_color=FLOW_COL, stroke_width=2.5, fill_color=FLOW_COL, fill_opacity=0.8)
        whole_bar.move_to([bar_x, bar_y, 0])
        bar_lab = T("flow rise", size=26, color=FLOW_COL).next_to(whole_bar, UP, buff=0.14)
        self.play(FadeIn(whole_bar), FadeIn(bar_lab), run_time=0.6)

        self.at("20 to 30")
        fracs = [0.24, 0.21, 0.20, 0.18, 0.17]
        cols = [SIGNAL_COL, NO_COL, FLOW_COL, ARTERIOLE_COL, CAPILLARY_COL]
        slices = VGroup()
        cx = bar_x - bar_w / 2
        for fr, col in zip(fracs, cols):
            sw = bar_w * fr
            sl = Rectangle(width=sw - 0.03, height=bar_h, stroke_color=BG, stroke_width=2,
                           fill_color=col, fill_opacity=0.88).move_to([cx + sw / 2, bar_y, 0])
            slices.add(sl)
            cx += sw
        no_single = T("no single dilator", size=26, color=TEXT).next_to(whole_bar, DOWN, buff=0.16)
        self.play(FadeOut(whole_bar, run_time=0.25), FadeIn(slices, run_time=0.5), FadeIn(no_single, run_time=0.5))

        self.at("blunts sympathetic constriction")
        nerve_wire = CubicBezier([-3.75, BRANCH_YS["muscle"] - 0.62, 0], [-3.25, BRANCH_YS["muscle"] - 0.62, 0],
                                 [-2.75, BRANCH_YS["muscle"] - 0.55, 0], [-2.55, BRANCH_YS["muscle"] - 0.30, 0],
                                 color=NERVE_COL, stroke_width=4.5)
        blunt_tag = T("constriction blunted", size=26, color=NERVE_COL).move_to([4.35, BRANCH_YS["muscle"] - 0.95, 0])
        pulse_dot = Dot(nerve_wire.get_start(), radius=0.08, color=NERVE_COL)
        self.play(Create(nerve_wire), FadeIn(blunt_tag), run_time=0.5)
        self.play(MoveAlongPath(pulse_dot, nerve_wire), radii["muscle"].animate.set_value(0.24), run_time=0.6)
        self.play(radii["muscle"].animate.set_value(0.26), FadeOut(pulse_dot, run_time=0.2), run_time=0.5)
        self.finish()


class S13Skin(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        radii, flows = default_four_trackers(r_init=0.14, f_init=0.35)
        world, refs = make_four_branch_world(radii, flows, active_organs={"skin"}, show_hands=True)
        head = T("Same tap. Different hands.", size=34, color=TEXT).move_to([0.0, 3.35, 0])
        self.add(world, head)

        self.at("nerves turn it")
        y_sk = BRANCH_YS["skin"]
        wire1 = CubicBezier([2.75, y_sk + 0.58, 0], [0.6, y_sk + 0.64, 0],
                            [-1.1, y_sk + 0.60, 0], [-2.02, y_sk + 0.50, 0],
                            color=NERVE_COL, stroke_width=4.5)
        wire2 = CubicBezier([2.75, y_sk + 0.44, 0], [0.6, y_sk + 0.50, 0],
                            [-1.1, y_sk + 0.48, 0], [-1.95, y_sk + 0.42, 0],
                            color=NERVE_COL, stroke_width=3.5)
        self.play(Create(wire1), Create(wire2),
                  refs["hands"]["skin"].animate.set_stroke(color=NERVE_COL, opacity=1.0).set_fill(color=NERVE_COL, opacity=0.32),
                  run_time=0.8)

        self.at("body temperature")
        temp_trk = ValueTracker(0.22)
        bulb_c = np.array([3.35, y_sk - 0.15, 0])
        stem_bg = RoundedRectangle(corner_radius=0.09, width=0.22, height=1.25, stroke_color=TEXT,
                                   stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to(bulb_c + UP * 0.68)
        bulb = Circle(radius=0.21, stroke_color=TEXT, stroke_width=2.5, fill_color=BLOOD_COL, fill_opacity=0.9).move_to(bulb_c)
        merc = always_redraw(lambda: Rectangle(
            width=0.13, height=max(0.08, temp_trk.get_value() * 1.15), stroke_width=0,
            fill_color=BLOOD_COL, fill_opacity=0.95
        ).move_to([bulb_c[0], bulb_c[1] + 0.10 + max(0.08, temp_trk.get_value() * 1.15) / 2, 0]))
        temp_lab = T("body\ntemperature", size=24, color=TEXT).next_to(stem_bg, RIGHT, buff=0.18)
        therm = VGroup(stem_bg, merc, bulb, temp_lab)
        self.play(FadeIn(therm), run_time=0.6)

        p_dot = Dot(wire1.get_start(), radius=0.08, color=NERVE_COL)
        self.play(
            temp_trk.animate.set_value(0.92),
            MoveAlongPath(p_dot, wire1),
            radii["skin"].animate.set_value(0.28),
            flows["skin"].animate.set_value(0.96),
            run_time=2.6,
        )
        self.play(FadeOut(p_dot, run_time=0.25))

        self.at("6 to 8")
        est_tag = T("heating: estimated 6\u20138 L/min", size=24, color=GOLD).move_to([4.40, y_sk - 0.72, 0])
        self.play(FadeIn(est_tag, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        radii, flows = default_four_trackers(r_init=0.20, f_init=0.55)
        world, refs = make_four_branch_world(radii, flows, active_organs=set(BRANCH_YS), show_hands=True)
        self.add(world)

        self.at("same everywhere")
        glows = VGroup(*[
            Circle(radius=0.28, color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.22)
            .move_to(refs["taps"][o].get_center())
            for o in BRANCH_YS
        ])
        self.play(FadeIn(glows), *[radii[o].animate.set_value(0.25) for o in BRANCH_YS], run_time=0.6)
        self.play(FadeOut(glows), run_time=0.4)

        self.at("hand on it")
        self.play(*[Indicate(refs["hands"][o], color=GOLD, scale_factor=1.12) for o in BRANCH_YS], run_time=0.6)

        self.at("Pressure")
        p_arrows = VGroup()
        for o, y in BRANCH_YS.items():
            p_arrows.add(Arrow([-2.55, y, 0], [-2.55, y + 0.24, 0], color=PRESSURE_COL, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.45))
            p_arrows.add(Arrow([-2.55, y, 0], [-2.55, y - 0.24, 0], color=PRESSURE_COL, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.45))
        p_tag = T("pressure", size=26, color=PRESSURE_COL).move_to([4.25, 2.85, 0])
        self.play(FadeIn(p_arrows), FadeIn(p_tag), run_time=0.45)

        self.at("own chemistry")
        chem_h = make_signal_stream([-0.8, BRANCH_YS["heart"], 0], [-2.02, BRANCH_YS["heart"] + 0.42, 0],
                                    color=SIGNAL_COL, n=6, seed=51, radius=0.055, speed=0.80)
        chem_m = make_signal_stream([-0.8, BRANCH_YS["muscle"], 0], [-2.02, BRANCH_YS["muscle"] + 0.42, 0],
                                    color=SIGNAL_COL, n=6, seed=52, radius=0.055, speed=0.80)
        chem_tag = T("own chemistry", size=26, color=SIGNAL_COL).move_to([4.25, BRANCH_YS["heart"], 0])
        self.play(FadeIn(chem_h), FadeIn(chem_m), FadeIn(chem_tag),
                  refs["hands"]["heart"].animate.set_stroke(color=SIGNAL_COL, opacity=1.0).set_fill(color=SIGNAL_COL, opacity=0.28),
                  refs["hands"]["muscle"].animate.set_stroke(color=SIGNAL_COL, opacity=1.0).set_fill(color=SIGNAL_COL, opacity=0.28),
                  run_time=0.5)

        self.at("neurons")
        y_br = BRANCH_YS["brain"]
        soma = Dot([3.05, y_br, 0], radius=0.10, color=NERVE_COL)
        axon = CubicBezier(
            soma.get_center(),
            [2.1, y_br + 0.62, 0],
            [-0.4, y_br + 0.66, 0],
            [-2.02, y_br + 0.50, 0],
            color=NERVE_COL, stroke_width=3.5,
        )
        neur_tag = T("neurons", size=26, color=TEXT).move_to([4.25, y_br, 0])
        self.play(FadeIn(soma), Create(axon), FadeIn(neur_tag),
                  refs["hands"]["brain"].animate.set_stroke(color=NERVE_COL, opacity=1.0).set_fill(color=NERVE_COL, opacity=0.28),
                  run_time=0.45)

        self.at("nerves tuned to body heat")
        y_sk = BRANCH_YS["skin"]
        wire = CubicBezier([2.70, y_sk + 0.50, 0], [0.6, y_sk + 0.56, 0],
                           [-1.1, y_sk + 0.54, 0], [-2.02, y_sk + 0.48, 0],
                           color=NERVE_COL, stroke_width=4)
        bulb_c = np.array([2.72, y_sk - 0.36, 0])
        t_stem = RoundedRectangle(corner_radius=0.06, width=0.14, height=0.72, stroke_color=TEXT,
                                  stroke_width=2.0, fill_color=BG, fill_opacity=0.9).move_to(bulb_c + UP * 0.40)
        t_bulb = Circle(radius=0.13, stroke_color=TEXT, stroke_width=2.0, fill_color=BLOOD_COL, fill_opacity=0.9).move_to(bulb_c)
        t_merc = Rectangle(width=0.08, height=0.58, stroke_width=0, fill_color=BLOOD_COL, fill_opacity=0.95).move_to(bulb_c + UP * 0.35)
        therm = VGroup(t_stem, t_merc, t_bulb)
        heat_tag = T("nerves + body heat", size=24, color=NERVE_COL).next_to(t_stem, RIGHT, buff=0.20).set_y(y_sk - 0.04)
        self.play(Create(wire), FadeIn(therm), FadeIn(heat_tag), flows["skin"].animate.set_value(0.85),
                  refs["hands"]["skin"].animate.set_stroke(color=NERVE_COL, opacity=1.0).set_fill(color=NERVE_COL, opacity=0.28),
                  run_time=0.40)
        self.finish()


class S15End(EndCard):
    LINE = "Arterioles are every organ's tap; organs differ in who turns it."
