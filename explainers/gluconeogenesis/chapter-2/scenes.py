"""
Who Picks the Direction — Gluconeogenesis Chapter 2 (STEMhop)

COLOUR MAP (one colour per concept for the whole film):
- BLUE (#58C4DD):    glycolysis and its enzymes (left lane, downward, PFK-1)
- ORANGE (#FF8C42):  gluconeogenesis and its bypass enzymes (right lane, upward, FBPase-1)
- YELLOW (#F5D547):  glucose and carbon intermediates (glucose, 2 pyruvate, F6P, F-1,6-BP, carbon cargo dots)
- GREEN (#83C167):   ATP / GTP high-energy phosphates
- RED (#FC6255):     wasted phosphates and wasted heat
- MAGENTA (#E066FF): fructose-2,6-bisphosphate, the regulator (chip, tokens, level gauge)
- GOLD (#D4A843):    "both downhill" thermodynamic highlight and predict countdown ring
- GREY (#8B93A1):    liver cell membrane, structural frames, schematic tag
- TEXT (#E8EAF0):    neutral labels, bifunctional protein outline, insulin/glucagon/PKA chips, white 'P' tag

CARRIED WORLD:
A GREY liver-cell membrane encloses a vertical two-lane metabolic road between YELLOW 'glucose' (top)
and YELLOW '2 pyruvate' (bottom). The LEFT lane (BLUE, downward) is glycolysis; the RIGHT lane
(ORANGE, upward) is gluconeogenesis. Three stations cross the road (glucose pair, middle pair,
pyruvate pair), each with a BLUE gate and an ORANGE gate. Views zoom cleanly between the full cell
and the middle station (with the bifunctional two-lobed protein and MAGENTA '2,6 level' gauge).

WHAT CHANGES IN EACH SPOKEN SCENE (and what computes it):
- s00_link_and_question: YELLOW carbon dots cycle continuously down BLUE and up ORANGE simultaneously
  (flux = 1.0, 1.0); camera transitions to middle station as YELLOW F-1,6-BP sits on the road and
  MAGENTA F-2,6-BP bobs off the road.
- s02_stakes_predict: Pullback to full cell; 3 enzyme pairs pulse in sequence; YELLOW carbon loop
  accelerates from speed 1.0 to 2.4 while 'glucose made: 0' swaps to RED 'wasted per turn: ?'.
- s04_answer: Computed energy tally (6 spent - 2 returned = 4 wasted): 6 GREEN chips appear, 2 slide
  across to cancel 2, leaving 4 that fly to the 3 stations (1, 1, 2) and turn into 4 rising RED
  sinusoidal heat waves.
- s05_middle_pair: Zoom into middle station; highlighted YELLOW carbon dot cycles down PFK-1 gate
  (F6P -> F-1,6-BP) and back up FBPase-1 gate at equal computed flux (0.60, 0.60).
- s06_twin_answer: Parked MAGENTA token expands into F-2,6-BP chip; computed regulator tracker c
  rises (0.35 -> 0.88), widening PFK-1 gate (gly_flux(c)) and narrowing FBPase-1 gate (gng_flux(c)).
- s07_one_idea: Pullback to full road; lanes equalize, then each station's opposing gates reciprocally
  widen and narrow via computed flux trackers, slowing the futile loop.
- s08_one_protein: Middle station shifts left; two-lobed protein appears at right; kinase lobe puffs
  MAGENTA tokens as c rises (0.35 -> 0.85), phosphatase lobe swallows tokens as c falls (0.85 -> 0.20),
  driving the MAGENTA gauge and middle gates together.
- s09_fed: Outside-cell 'insulin' signals protein (no white 'P'); kinase wins, c climbs (0.45 -> 0.92),
  gauge fills, MAGENTA tokens dock, PFK-1 widens and BLUE glycolysis stream speeds up.
- s10_fasting: 'insulin' leaves, 'glucagon' arrives, signals 'PKA' to stamp WHITE 'P' onto protein;
  phosphatase wins, MAGENTA tokens pop, c falls (0.92 -> 0.08), FBPase-1 widens and ORANGE stream runs.
- s11_other_pairs: Pullback to full road with mini P-tagged protein; 'own controls' appear at top/bottom
  pairs, ORANGE flux dominates (0.95) over BLUE trickle (0.15), and only 1 faint RED heat wisp rises.
- s12_close: All 6 gates pulse together, both lanes equalize briefly, then MAGENTA switch swings up
  (c -> 0.92, BLUE dominates) and back down (c -> 0.08, ORANGE dominates).
"""

from bp_parts import *

ORANGE = "#FF8C42"
MAGENTA = "#E066FF"

# ------------------------------------------------------------------ computed model
K_REG = 0.35
SPENT_PHOSPHATES = 6
RETURNED_PHOSPHATES = 2
WASTED_PHOSPHATES = SPENT_PHOSPHATES - RETURNED_PHOSPHATES  # 4


def gly_flux(c):
    """PFK-1 / glycolytic flux in [0.16, 1.0] computed from F-2,6-BP level c in [0, 1]."""
    c = float(np.clip(c, 0.0, 1.0))
    return 0.16 + 0.84 * (c * c / (c * c + K_REG * K_REG))


def gng_flux(c):
    """FBPase-1 / gluconeogenic flux in [0.16, 1.0] reciprocally inhibited by c in [0, 1]."""
    c = float(np.clip(c, 0.0, 1.0))
    return 0.16 + 0.84 * (K_REG * K_REG / (c * c + K_REG * K_REG))


# ------------------------------------------------------------------ shared geometry helpers
def _rounded_cell_outline(center, w, h, r=0.85, color=GREY, stroke=4.0, fill_opacity=0.14):
    """Build a smooth rounded liver-cell membrane as a VMobject (not a rectangular panel)."""
    cx, cy = center[0], center[1]
    hw, hh = w / 2 - r, h / 2 - r
    pts = []
    corners = [
        (cx + hw, cy + hh, 0, PI / 2),
        (cx - hw, cy + hh, PI / 2, PI),
        (cx - hw, cy - hh, PI, 3 * PI / 2),
        (cx + hw, cy - hh, 3 * PI / 2, TAU),
    ]
    for ox, oy, a0, a1 in corners:
        for a in np.linspace(a0, a1, 14):
            pts.append([ox + r * np.cos(a), oy + r * np.sin(a), 0.0])
    pts.append(pts[0])
    m = VMobject(stroke_color=color, stroke_width=stroke, fill_color=color, fill_opacity=fill_opacity)
    m.set_points_as_corners([np.array(p) for p in pts])
    return m


def _lane_chevron(x, y, direction, color, size=0.15):
    """Small V-chevron arrow pointing DOWN (-1) or UP (+1) along a lane."""
    s = size
    d = direction
    return VMobject(stroke_color=color, stroke_width=4.0, fill_opacity=0).set_points_as_corners([
        np.array([x - s, y - d * s, 0.0]),
        np.array([x, y + d * 0.4 * s, 0.0]),
        np.array([x + s, y - d * s, 0.0]),
    ])


def _make_gate(x, y, color, flux_fn, jaw_len=0.22):
    """Two-jaw enzyme gate straddling a vertical lane at (x, y); gap scales with flux_fn()."""
    def build():
        fl = float(np.clip(flux_fn(), 0.1, 1.0))
        gap = 0.07 + 0.22 * fl
        sw = 3.0 + 4.5 * fl
        op = 0.45 + 0.55 * fl
        left_jaw = VGroup(
            Line([x - gap - jaw_len, y + 0.12, 0], [x - gap, y, 0], color=color, stroke_width=sw),
            Line([x - gap, y, 0], [x - gap - jaw_len, y - 0.12, 0], color=color, stroke_width=sw),
        ).set_stroke(opacity=op)
        right_jaw = VGroup(
            Line([x + gap + jaw_len, y + 0.12, 0], [x + gap, y, 0], color=color, stroke_width=sw),
            Line([x + gap, y, 0], [x + gap + jaw_len, y - 0.12, 0], color=color, stroke_width=sw),
        ).set_stroke(opacity=op)
        return VGroup(left_jaw, right_jaw)
    return always_redraw(build)


def _lane_dots(x, y_top, y_bot, direction, flux_fn, n_dots=7, base_speed=1.65, radius=0.11, seed=7):
    """Continuous stream of YELLOW carbon cargo beads moving along one lane at computed flux speed."""
    rng = np.random.default_rng(seed)
    span = y_top - y_bot
    phases = [(i / n_dots + rng.uniform(-0.015, 0.015)) % 1.0 for i in range(n_dots)]
    op0 = 0.40 + 0.60 * min(1.0, float(np.clip(flux_fn(), 0.0, 2.8)))
    dots = VGroup()
    for ph in phases:
        d = Dot(radius=radius, color=YELLOW, stroke_color=TEXT, stroke_width=1.2)
        d._ph = ph
        d._dot_op = op0
        d.set_fill(opacity=op0)
        d.set_stroke(opacity=op0)

        def upd(m, dt, x=x, y0=y_bot, y1=y_top, span=span, dir_=direction, fn=flux_fn):
            cur = float(m.get_fill_opacity())
            if cur <= 1e-4:
                return
            fade = min(1.0, cur / max(getattr(m, "_dot_op", 1.0), 1e-4))
            y_exp = y1 - m._ph * span if dir_ < 0 else y0 + m._ph * span
            y_cur = m.get_center()[1]
            if abs(y_cur - y_exp) > 0.05:
                m._ph = ((y1 - y_cur) / span if dir_ < 0 else (y_cur - y0) / span) % 1.0
            fl = float(np.clip(fn(), 0.0, 2.8))
            m._ph = (m._ph + dt * base_speed * fl / span) % 1.0
            y = y1 - m._ph * span if dir_ < 0 else y0 + m._ph * span
            m.move_to([x, y, 0.0])
            op = 0.40 + 0.60 * min(1.0, fl)
            m._dot_op = op
            m.set_fill(opacity=op * fade)
            m.set_stroke(opacity=op * fade)

        d.add_updater(upd)
        y_init = y_top - ph * span if direction < 0 else y_bot + ph * span
        d.move_to([x, y_init, 0.0])
        dots.add(d)
    return dots


def _heat_wave(x, y0, height=1.0, amp=0.14, freq=3.0, color=RED, opacity=1.0, phase=0.0):
    """Computed sinusoidal heat wisp rising from (x, y0)."""
    ys = np.linspace(0, height, 36)
    pts = [np.array([x + amp * np.sin(freq * TAU * (dy / height) + phase), y0 + dy, 0.0]) for dy in ys]
    w = VMobject(stroke_color=color, stroke_width=4.5, stroke_opacity=opacity, fill_opacity=0)
    w.set_points_as_corners(pts)
    tip = Triangle(color=color, fill_color=color, fill_opacity=opacity, stroke_width=0).scale(0.10)
    tip.move_to(pts[-1])
    return VGroup(w, tip)


def _two_lobed_protein(center, width=4.2, height=2.45, color=TEXT):
    """Smooth cartoon two-lobed bifunctional protein (NOT a molecular structure)."""
    cx, cy = center[0], center[1]
    rx = width * 0.5
    ry = height * 0.5
    ts = np.linspace(0, TAU, 96)
    pts = []
    for t in ts:
        x = cx + rx * np.cos(t)
        pinch = 0.62 + 0.38 * (np.cos(t) ** 2)
        y = cy + ry * pinch * np.sin(t)
        pts.append(np.array([x, y, 0.0]))
    pts.append(pts[0])
    body = VMobject(stroke_color=color, stroke_width=4.0, fill_color=color, fill_opacity=0.10)
    body.set_points_as_corners(pts)
    kx, px = cx - width * 0.24, cx + width * 0.24
    lobe_k = Circle(radius=height * 0.30, stroke_width=0, fill_color=BLUE, fill_opacity=0.0).move_to([kx, cy, 0])
    lobe_p = Circle(radius=height * 0.30, stroke_width=0, fill_color=ORANGE, fill_opacity=0.0).move_to([px, cy, 0])
    return body, lobe_k, lobe_p


def _phosphate_badge(at, size=24, radius=0.28):
    """Small WHITE 'P' tag representing a phosphate stamped onto the protein."""
    c = Circle(radius=radius, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.22).move_to(at)
    p = T("P", size=size, color=TEXT, weight=BOLD).move_to(c)
    return VGroup(c, p)


# ------------------------------------------------------------------ Full-Cell Road World
FULL_X_CENTER = -1.25
FULL_BLUE_X = -2.25
FULL_ORANGE_X = -0.25
FULL_STATION_YS = (1.15, -0.25, -1.65)  # glucose pair, middle pair, pyruvate pair


def build_full_world(gly_fn, gng_fn, station_fns=None, show_station_labels=False, seed=7):
    """Build the carried full liver-cell two-lane road in fixed coordinates."""
    cell = _rounded_cell_outline([FULL_X_CENTER, -0.25, 0], w=7.9, h=5.95, r=0.85)
    top_chip = chip("glucose", YELLOW, size=26, pad=0.18).move_to([FULL_X_CENTER, 2.25, 0])
    bot_chip = chip("2 pyruvate", YELLOW, size=26, pad=0.18).move_to([FULL_X_CENTER, -2.75, 0])

    y_top = top_chip.get_bottom()[1] - 0.05
    y_bot = bot_chip.get_top()[1] + 0.05

    blue_lane = Line([FULL_BLUE_X, y_top, 0], [FULL_BLUE_X, y_bot, 0], color=BLUE, stroke_width=5.5)
    orange_lane = Line([FULL_ORANGE_X, y_bot, 0], [FULL_ORANGE_X, y_top, 0], color=ORANGE, stroke_width=5.5)

    chevrons = VGroup(
        _lane_chevron(FULL_BLUE_X, 1.65, -1, BLUE),
        _lane_chevron(FULL_BLUE_X, 0.45, -1, BLUE),
        _lane_chevron(FULL_BLUE_X, -0.95, -1, BLUE),
        _lane_chevron(FULL_ORANGE_X, -0.95, +1, ORANGE),
        _lane_chevron(FULL_ORANGE_X, 0.45, +1, ORANGE),
        _lane_chevron(FULL_ORANGE_X, 1.65, +1, ORANGE),
    )

    # Labels safely inside cell walls (-5.20 .. +2.70) and clear of lanes and gate jaws
    lbl_gly = T("glycolysis", 24, BLUE).move_to([FULL_BLUE_X - 1.45, 2.00, 0])
    lbl_gng = T("gluconeogenesis", 24, ORANGE).move_to([FULL_ORANGE_X + 1.50, 2.00, 0])

    if station_fns is None:
        station_fns = [(gly_fn, gng_fn)] * 3

    gates = VGroup()
    for y, (gf, nf) in zip(FULL_STATION_YS, station_fns):
        gates.add(_make_gate(FULL_BLUE_X, y, BLUE, gf), _make_gate(FULL_ORANGE_X, y, ORANGE, nf))

    dots_gly = _lane_dots(FULL_BLUE_X, y_top - 0.05, y_bot + 0.05, -1, gly_fn, n_dots=7, base_speed=1.65, radius=0.11, seed=seed)
    dots_gng = _lane_dots(FULL_ORANGE_X, y_top - 0.05, y_bot + 0.05, +1, gng_fn, n_dots=7, base_speed=1.65, radius=0.11, seed=seed + 1)

    station_labels = VGroup()
    if show_station_labels:
        for txt, y in zip(("glucose pair", "middle pair", "pyruvate pair"), FULL_STATION_YS):
            # Left-aligned cleanly past the right jaw (+0.30) and inside cell right wall (+2.70)
            t = T(txt, 24, TEXT).move_to([FULL_ORANGE_X + 0.72, y, 0], aligned_edge=LEFT)
            station_labels.add(t)

    world = VGroup(cell, blue_lane, orange_lane, chevrons, top_chip, bot_chip,
                   lbl_gly, lbl_gng, gates, dots_gly, dots_gng, station_labels)
    world.cell = cell
    world.top_chip = top_chip
    world.bot_chip = bot_chip
    world.blue_lane = blue_lane
    world.orange_lane = orange_lane
    world.lbl_gly = lbl_gly
    world.lbl_gng = lbl_gng
    world.gates = gates
    world.dots_gly = dots_gly
    world.dots_gng = dots_gng
    world.station_labels = station_labels
    return world


# ------------------------------------------------------------------ Zoomed Middle-Station World
def build_mid_world(x_mid, gly_fn, gng_fn, cell_w=10.6, lane_dx=2.3, seed=17, with_cell=True):
    """Build the zoomed middle-station picture centered at x_mid."""
    g = VGroup()
    if with_cell:
        cell = _rounded_cell_outline([x_mid, -0.05, 0], w=cell_w, h=6.45, r=0.85)
        g.add(cell)
        g.cell = cell
    else:
        g.cell = None

    f6p = chip("fructose-6-phosphate", YELLOW, size=26, pad=0.18).move_to([x_mid, 2.25, 0])
    f16bp = chip("fructose-1,6-bisphosphate", YELLOW, size=26, pad=0.18).move_to([x_mid, -2.05, 0])

    bx = x_mid - lane_dx
    ox = x_mid + lane_dx
    y_top = f6p.get_bottom()[1] - 0.06
    y_bot = f16bp.get_top()[1] + 0.06

    blue_lane = Line([bx, y_top, 0], [bx, y_bot, 0], color=BLUE, stroke_width=5.5)
    orange_lane = Line([ox, y_bot, 0], [ox, y_top, 0], color=ORANGE, stroke_width=5.5)

    chevrons = VGroup(
        _lane_chevron(bx, 1.15, -1, BLUE, size=0.17),
        _lane_chevron(bx, -1.15, -1, BLUE, size=0.17),
        _lane_chevron(ox, -1.15, +1, ORANGE, size=0.17),
        _lane_chevron(ox, 1.15, +1, ORANGE, size=0.17),
    )

    gate_pfk = _make_gate(bx, 0.0, BLUE, gly_fn, jaw_len=0.26)
    gate_fbp = _make_gate(ox, 0.0, ORANGE, gng_fn, jaw_len=0.26)

    lbl_pfk = T("PFK-1", 26, BLUE).move_to([bx - 1.25, 0.0, 0])
    lbl_fbp = T("FBPase-1", 26, ORANGE).move_to([ox + 1.40, 0.0, 0])

    dots_gly = _lane_dots(bx, y_top - 0.05, y_bot + 0.05, -1, gly_fn, n_dots=6, base_speed=1.60, radius=0.115, seed=seed)
    dots_gng = _lane_dots(ox, y_top - 0.05, y_bot + 0.05, +1, gng_fn, n_dots=6, base_speed=1.60, radius=0.115, seed=seed + 1)

    g.add(blue_lane, orange_lane, chevrons, f6p, f16bp, gate_pfk, gate_fbp, lbl_pfk, lbl_fbp, dots_gly, dots_gng)
    g.f6p = f6p
    g.f16bp = f16bp
    g.blue_lane = blue_lane
    g.orange_lane = orange_lane
    g.gate_pfk = gate_pfk
    g.gate_fbp = gate_fbp
    g.lbl_pfk = lbl_pfk
    g.lbl_fbp = lbl_fbp
    g.dots_gly = dots_gly
    g.dots_gng = dots_gng
    g.bx = bx
    g.ox = ox
    g.y_top = y_top
    g.y_bot = y_bot
    return g


def build_protein_stage(c_tracker, with_cell_wall=False):
    """Build the shared s08/s09/s10 left-shifted middle station + MAGENTA gauge + two-lobed protein."""
    x_mid = -3.65
    mid = build_mid_world(
        x_mid,
        lambda: gly_flux(c_tracker.get_value()),
        lambda: gng_flux(c_tracker.get_value()),
        lane_dx=1.00,
        seed=29,
        with_cell=False,
    )
    # Place PFK-1 and FBPase-1 strictly clear of gate jaws (max extent ~0.55 from lane center)
    mid.lbl_pfk.set_font_size(24).move_to([mid.bx - 1.15, 0.0, 0])
    mid.lbl_fbp.set_font_size(24).move_to([mid.ox + 1.32, 0.0, 0])

    # Vertical MAGENTA gauge at x = -0.25 (clear of FBPase-1 ending around -0.82)
    gx = -0.25
    gauge_h = 3.0
    gauge_w = 0.48
    gauge_y0 = -1.6
    gauge_frame = RoundedRectangle(corner_radius=0.10, width=gauge_w, height=gauge_h,
                                   stroke_color=MAGENTA, stroke_width=2.5, fill_color=BG, fill_opacity=0.85)
    gauge_frame.move_to([gx, gauge_y0 + gauge_h / 2, 0])
    gauge_lbl = T("2,6 level", 26, MAGENTA).next_to(gauge_frame, UP, buff=0.22)

    def make_fill():
        frac = float(np.clip(c_tracker.get_value(), 0.04, 0.98))
        fh = max(0.12, (gauge_h - 0.08) * frac)
        r = RoundedRectangle(corner_radius=0.06, width=gauge_w - 0.10, height=fh,
                             stroke_width=0, fill_color=MAGENTA, fill_opacity=0.85)
        r.move_to([gx, gauge_y0 + 0.04 + fh / 2, 0])
        return r

    gauge_fill = always_redraw(make_fill)

    # Two-lobed protein on the right inside the cell (x in [0.45, 4.65])
    prot_center = np.array([2.55, -0.15, 0.0])
    prot_body, lobe_k, lobe_p = _two_lobed_protein(prot_center, width=4.2, height=2.45, color=TEXT)
    lbl_prot = T("one protein", 28, TEXT).next_to(prot_body, UP, buff=0.65)
    lbl_kinase = T("kinase\nhalf", 24, TEXT).move_to([prot_center[0] - 1.00, prot_center[1], 0])
    lbl_phos = T("phosphatase\nhalf", 24, TEXT).move_to([prot_center[0] + 0.96, prot_center[1], 0])

    stage = VGroup(mid, gauge_frame, gauge_fill, gauge_lbl, lobe_k, lobe_p, prot_body, lbl_prot, lbl_kinase, lbl_phos)
    if with_cell_wall:
        wall = Line([4.85, -3.1, 0], [4.85, 2.9, 0], color=GREY, stroke_width=4.0)
        stage.add(wall)
        stage.wall = wall
    else:
        stage.wall = None

    stage.mid = mid
    stage.gauge_frame = gauge_frame
    stage.gauge_fill = gauge_fill
    stage.gauge_lbl = gauge_lbl
    stage.prot_center = prot_center
    stage.prot_body = prot_body
    stage.lobe_k = lobe_k
    stage.lobe_p = lobe_p
    stage.lbl_prot = lbl_prot
    stage.lbl_kinase = lbl_kinase
    stage.lbl_phos = lbl_phos
    return stage


# ================================================================== SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        v_gly = ValueTracker(0.95)
        v_gng = ValueTracker(0.95)
        world = build_full_world(lambda: v_gly.get_value(), lambda: v_gng.get_value(), seed=1)
        both_tag = chip("both downhill", GOLD, size=26, pad=0.16).move_to([4.55, 2.35, 0])
        sc = scope_tag("schematic")
        self.add(world, both_tag, sc)

        self.at("Both pathways")
        self.play(
            both_tag[0].animate.set_fill(opacity=0.38),
            world.cell.animate.set_stroke(width=6.0),
            run_time=1.0,
        )
        self.play(
            both_tag[0].animate.set_fill(opacity=0.16),
            world.cell.animate.set_stroke(width=4.0),
            run_time=0.8,
        )

        # Transition to zoomed middle station showing the two near-twin molecules
        self.at("two near")
        twin_cell = _rounded_cell_outline([0.0, -0.15, 0], w=12.0, h=5.8, r=0.85)
        x_road = -2.45
        bx_t, ox_t = x_road - 0.95, x_road + 0.95
        f16_chip = chip("fructose-1,6-bisphosphate", YELLOW, size=26, pad=0.20).move_to([x_road, -0.30, 0])
        y_top_r, y_bot_r = 2.45, -2.75
        top_seg_b = Line([bx_t, y_top_r, 0], [bx_t, f16_chip.get_top()[1] + 0.06, 0], color=BLUE, stroke_width=5.5)
        bot_seg_b = Line([bx_t, f16_chip.get_bottom()[1] - 0.06, 0], [bx_t, y_bot_r, 0], color=BLUE, stroke_width=5.5)
        bot_seg_o = Line([ox_t, y_bot_r, 0], [ox_t, f16_chip.get_bottom()[1] - 0.06, 0], color=ORANGE, stroke_width=5.5)
        top_seg_o = Line([ox_t, f16_chip.get_top()[1] + 0.06, 0], [ox_t, y_top_r, 0], color=ORANGE, stroke_width=5.5)
        chev_t = VGroup(
            _lane_chevron(bx_t, 1.5, -1, BLUE, size=0.17),
            _lane_chevron(bx_t, -1.85, -1, BLUE, size=0.17),
            _lane_chevron(ox_t, -1.85, +1, ORANGE, size=0.17),
            _lane_chevron(ox_t, 1.5, +1, ORANGE, size=0.17),
        )
        d_top_b = _lane_dots(bx_t, y_top_r - 0.05, f16_chip.get_top()[1] + 0.12, -1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=3)
        d_bot_b = _lane_dots(bx_t, f16_chip.get_bottom()[1] - 0.12, y_bot_r + 0.05, -1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=4)
        d_bot_o = _lane_dots(ox_t, f16_chip.get_bottom()[1] - 0.12, y_bot_r + 0.05, +1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=5)
        d_top_o = _lane_dots(ox_t, y_top_r - 0.05, f16_chip.get_top()[1] + 0.12, +1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=6)
        twin_dots = VGroup(d_top_b, d_bot_b, d_bot_o, d_top_o)

        f26_chip = chip("fructose-2,6-bisphosphate", MAGENTA, size=26, pad=0.20).move_to([2.85, -0.30, 0])

        # Clear interior of full world while transforming cell outline to avoid ghosting dots over chips
        world_interior = VGroup(
            world.blue_lane, world.orange_lane, world.top_chip, world.bot_chip,
            world.lbl_gly, world.lbl_gng, world.gates, world.dots_gly, world.dots_gng, world.station_labels,
            *[m for m in world if m not in (world.cell, world.blue_lane, world.orange_lane, world.top_chip, world.bot_chip,
                                            world.lbl_gly, world.lbl_gng, world.gates, world.dots_gly, world.dots_gng, world.station_labels)]
        )
        self.play(
            FadeOut(world_interior, run_time=0.45),
            FadeOut(both_tag, run_time=0.45),
            Transform(world.cell, twin_cell, run_time=0.75),
        )
        self.play(
            FadeIn(top_seg_b), FadeIn(bot_seg_b), FadeIn(bot_seg_o), FadeIn(top_seg_o),
            FadeIn(chev_t), FadeIn(twin_dots),
            FadeIn(f16_chip, shift=UP * 0.2), FadeIn(f26_chip, shift=UP * 0.2),
            run_time=0.65,
        )

        self.at("step on the road")
        self.play(f16_chip[0].animate.set_fill(opacity=0.38), run_time=0.6)
        self.play(f16_chip[0].animate.set_fill(opacity=0.16), run_time=0.6)

        self.at("on neither road")
        bob(f26_chip, amp=0.14, speed=2.6, seed=1)

        self.at("why does the liver")
        q_text = T("Why make it at all?", 36, TEXT).move_to([0.0, 3.25, 0])
        self.play(FadeIn(q_text, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        twin_cell = _rounded_cell_outline([0.0, -0.15, 0], w=12.0, h=5.8, r=0.85)
        x_road = -2.45
        bx_t, ox_t = x_road - 0.95, x_road + 0.95
        f16_chip = chip("fructose-1,6-bisphosphate", YELLOW, size=26, pad=0.20).move_to([x_road, -0.30, 0])
        y_top_r, y_bot_r = 2.45, -2.75
        segs = VGroup(
            Line([bx_t, y_top_r, 0], [bx_t, f16_chip.get_top()[1] + 0.06, 0], color=BLUE, stroke_width=5.5),
            Line([bx_t, f16_chip.get_bottom()[1] - 0.06, 0], [bx_t, y_bot_r, 0], color=BLUE, stroke_width=5.5),
            Line([ox_t, y_bot_r, 0], [ox_t, f16_chip.get_bottom()[1] - 0.06, 0], color=ORANGE, stroke_width=5.5),
            Line([ox_t, f16_chip.get_top()[1] + 0.06, 0], [ox_t, y_top_r, 0], color=ORANGE, stroke_width=5.5),
            _lane_chevron(bx_t, 1.5, -1, BLUE, size=0.17),
            _lane_chevron(bx_t, -1.85, -1, BLUE, size=0.17),
            _lane_chevron(ox_t, -1.85, +1, ORANGE, size=0.17),
            _lane_chevron(ox_t, 1.5, +1, ORANGE, size=0.17),
        )
        twin_dots = VGroup(
            _lane_dots(bx_t, y_top_r - 0.05, f16_chip.get_top()[1] + 0.12, -1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=3),
            _lane_dots(bx_t, f16_chip.get_bottom()[1] - 0.12, y_bot_r + 0.05, -1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=4),
            _lane_dots(ox_t, f16_chip.get_bottom()[1] - 0.12, y_bot_r + 0.05, +1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=5),
            _lane_dots(ox_t, y_top_r - 0.05, f16_chip.get_top()[1] + 0.12, +1, lambda: 1.0, n_dots=4, base_speed=1.55, radius=0.11, seed=6),
        )
        f26_chip = chip("fructose-2,6-bisphosphate", MAGENTA, size=26, pad=0.20).move_to([2.85, -0.30, 0])
        q_text = T("Why make it at all?", 36, TEXT).move_to([0.0, 3.25, 0])
        sc = scope_tag("schematic")
        self.add(twin_cell, segs, twin_dots, f16_chip, f26_chip, q_text, sc)

        title = T("Who Picks the Direction", size=44, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.25, 0])
        parked_token = Dot(radius=0.16, color=MAGENTA, stroke_color=TEXT, stroke_width=2).move_to([5.4, -0.30, 0])

        self.play(
            swap(q_text, title, run_time=0.8),
            Transform(f26_chip, parked_token, run_time=1.0),
        )
        self.wait(0.6)
        self.play(FadeOut(title, run_time=0.4))
        self.finish()


class S02StakesPredict(SpokenScene):
    def construct(self):
        v_gly = ValueTracker(0.85)
        v_gng = ValueTracker(0.85)
        world = build_full_world(lambda: v_gly.get_value(), lambda: v_gng.get_value(), seed=10)
        sc = scope_tag("schematic")
        self.play(FadeIn(world), FadeIn(sc), run_time=0.8)

        self.at("opposing enzymes")
        pair_names = ("glucose pair", "middle pair", "pyruvate pair")
        pair_labels = VGroup()
        for txt, y in zip(pair_names, FULL_STATION_YS):
            ring_l = Circle(radius=0.38, color=BLUE, stroke_width=4).move_to([FULL_BLUE_X, y, 0])
            ring_r = Circle(radius=0.38, color=ORANGE, stroke_width=4).move_to([FULL_ORANGE_X, y, 0])
            lbl = T(txt, 24, TEXT).move_to([FULL_ORANGE_X + 0.72, y, 0], aligned_edge=LEFT)
            pair_labels.add(lbl)
            self.play(FadeIn(ring_l), FadeIn(ring_r), FadeIn(lbl, shift=RIGHT * 0.1), run_time=0.55)
            self.play(FadeOut(ring_l), FadeOut(ring_r), run_time=0.35)

        self.at("at full speed")
        made_box = boxed_label("glucose made: 0", YELLOW, size=26, pad=0.22).move_to([4.6, 0.55, 0])
        self.play(
            v_gly.animate.set_value(2.4),
            v_gng.animate.set_value(2.4),
            FadeIn(made_box, shift=UP * 0.15),
            run_time=1.4,
        )

        self.at("How many")
        waste_q_box = boxed_label("wasted per turn: ?", RED, size=26, pad=0.22).move_to([4.6, 0.55, 0])
        q = question_card("Phosphates wasted per turn?", y=3.25, color=TEXT, size=36).question
        self.play(
            swap(made_box, waste_q_box, run_time=0.7),
            FadeIn(q, shift=DOWN * 0.1),
            v_gly.animate.set_value(1.2),
            v_gng.animate.set_value(1.2),
            run_time=0.9,
        )
        self.finish()


class S03PredictPause(PredictPause):
    QUESTION = "Phosphates wasted per turn?"
    CARD = {"y": 3.25, "color": TEXT, "size": 36}
    RING_AT = (5.85, -2.10, 0)
    SECONDS = 4.5

    def backdrop(self):
        world = build_full_world(lambda: 1.0, lambda: 1.0, show_station_labels=True, seed=11)
        waste_box = boxed_label("wasted per turn: ?", RED, size=26, pad=0.22).move_to([4.6, 0.55, 0])
        q_mark = waste_box.label
        q_mark._ft = 0.0

        def flick(m, dt):
            m._ft += dt
            m.set_opacity(0.65 + 0.35 * np.sin(3.5 * m._ft))

        q_mark.add_updater(flick)
        return VGroup(world, waste_box, scope_tag("schematic"))


class S04Answer(SpokenScene):
    def construct(self):
        v_gly = ValueTracker(1.1)
        v_gng = ValueTracker(1.1)
        world = build_full_world(lambda: v_gly.get_value(), lambda: v_gng.get_value(), show_station_labels=True, seed=12)
        waste_q_box = boxed_label("wasted per turn: ?", RED, size=26, pad=0.22).move_to([4.6, 0.55, 0])
        q = question_card("Phosphates wasted per turn?", y=3.25, color=TEXT, size=36).question
        sc = scope_tag("schematic")
        self.add(world, waste_q_box, q, sc)

        # "Four."
        waste_4_box = boxed_label(f"wasted per turn: {WASTED_PHOSPHATES}", RED, size=26, pad=0.22).move_to([4.6, 2.35, 0])
        self.play(
            FadeOut(q, run_time=0.5),
            Transform(waste_q_box, waste_4_box, run_time=0.7),
        )

        # "Rebuilding spends six"
        self.at("Rebuilding spends")
        stack_6 = VGroup(*[
            RoundedRectangle(corner_radius=0.10, width=0.62, height=0.34, stroke_color=GREEN, stroke_width=2.5,
                             fill_color=GREEN, fill_opacity=0.35)
            for _ in range(SPENT_PHOSPHATES)
        ]).arrange(DOWN, buff=0.12).move_to([4.6, -0.15, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in stack_6], lag_ratio=0.12), run_time=1.2)

        # "and breaking down returns only two"
        self.at("returns only")
        ret_2 = VGroup(*[
            RoundedRectangle(corner_radius=0.10, width=0.62, height=0.34, stroke_color=GREEN, stroke_width=2.5,
                             fill_color=GREEN, fill_opacity=0.35)
            for _ in range(RETURNED_PHOSPHATES)
        ]).arrange(DOWN, buff=0.12).move_to([3.3, -1.07, 0])
        self.play(FadeIn(ret_2, shift=RIGHT * 0.2), run_time=0.5)
        cancel_targets = stack_6[4:]
        self.play(
            ret_2[0].animate.move_to(cancel_targets[0]),
            ret_2[1].animate.move_to(cancel_targets[1]),
            run_time=0.6,
        )
        self.play(FadeOut(ret_2), FadeOut(cancel_targets), run_time=0.4)
        rem_4 = stack_6[:4]

        # Place chips in the clear corridor between the two lanes (x = -1.25) or clear right side
        # "One is lost at the glucose pair"
        self.at("at the glucose pair")
        self.play(rem_4[0].animate.scale(0.8).move_to([-1.25, FULL_STATION_YS[0], 0]), run_time=0.65)

        # "one at the middle pair"
        self.at("at the middle pair")
        self.play(rem_4[1].animate.scale(0.8).move_to([-1.25, FULL_STATION_YS[1], 0]), run_time=0.65)

        # "and two at the pyruvate pair"
        self.at("at the pyruvate pair")
        self.play(
            rem_4[2].animate.scale(0.68).move_to([-1.25, FULL_STATION_YS[2] + 0.16, 0]),
            rem_4[3].animate.scale(0.68).move_to([-1.25, FULL_STATION_YS[2] - 0.16, 0]),
            run_time=0.75,
        )

        # "All of it ends as heat." -> rise into clear space above the cell without crossing labels
        self.at("ends as heat")
        heat_t = ValueTracker(0.0)
        heat_xs = (-3.75, -2.90, +0.55, +1.45)
        waves = VGroup(*[
            always_redraw(lambda x=hx, ph=idx * 1.1: _heat_wave(x, 2.75 + 0.25 * heat_t.get_value(), height=0.75, phase=ph + 4.5 * heat_t.get_value()))
            for idx, hx in enumerate(heat_xs)
        ])
        self.play(
            rem_4[0].animate.move_to([heat_xs[0], 2.85, 0]),
            rem_4[1].animate.move_to([heat_xs[1], 2.85, 0]),
            rem_4[2].animate.move_to([heat_xs[2], 2.85, 0]),
            rem_4[3].animate.move_to([heat_xs[3], 2.85, 0]),
            run_time=0.55,
        )
        self.play(FadeOut(rem_4, run_time=0.25))
        self.add(waves)
        self.play(heat_t.animate.set_value(1.4), run_time=1.2, rate_func=linear)
        self.finish()


class S05MiddlePair(SpokenScene):
    def construct(self):
        c = ValueTracker(0.35)
        mid = build_mid_world(0.0, lambda: gly_flux(c.get_value()), lambda: gng_flux(c.get_value()), lane_dx=2.3, seed=21)
        parked_token = Dot(radius=0.14, color=MAGENTA, stroke_color=TEXT, stroke_width=2).move_to([4.7, 1.5, 0])
        sc = scope_tag("schematic")
        self.play(FadeIn(mid), FadeIn(parked_token), FadeIn(sc), run_time=0.9)

        self.at("puts a phosphate on")
        pulse_down = Dot(radius=0.16, color=YELLOW, stroke_color=TEXT, stroke_width=2.5).move_to([mid.bx, mid.y_top, 0])
        self.play(FadeIn(pulse_down, scale=1.2), run_time=0.25)
        self.play(pulse_down.animate.move_to([mid.bx, mid.y_bot, 0]), run_time=1.3)
        self.play(
            mid.f16bp[0].animate.set_fill(opacity=0.38),
            FadeOut(pulse_down),
            run_time=0.4,
        )
        self.play(mid.f16bp[0].animate.set_fill(opacity=0.16), run_time=0.35)

        self.at("that phosphate back off")
        pulse_up = Dot(radius=0.16, color=YELLOW, stroke_color=TEXT, stroke_width=2.5).move_to([mid.ox, mid.y_bot, 0])
        self.play(FadeIn(pulse_up, scale=1.2), run_time=0.25)
        self.play(pulse_up.animate.move_to([mid.ox, mid.y_top, 0]), run_time=1.3)
        self.play(
            mid.f6p[0].animate.set_fill(opacity=0.38),
            FadeOut(pulse_up),
            run_time=0.4,
        )
        self.play(mid.f6p[0].animate.set_fill(opacity=0.16), run_time=0.35)

        self.at("same liver cell")
        self.play(mid.cell.animate.set_stroke(color=TEXT, width=6.0), run_time=0.6)
        self.play(mid.cell.animate.set_stroke(color=GREY, width=4.0), run_time=0.7)
        self.finish()


class S06TwinAnswer(SpokenScene):
    def construct(self):
        c = ValueTracker(0.35)
        mid = build_mid_world(0.0, lambda: gly_flux(c.get_value()), lambda: gng_flux(c.get_value()), lane_dx=2.3, seed=22)
        parked_token = Dot(radius=0.14, color=MAGENTA, stroke_color=TEXT, stroke_width=2).move_to([4.7, 1.5, 0])
        sc = scope_tag("schematic")
        self.add(mid, parked_token, sc)

        self.at("twin comes in")
        f26_chip = boxed_label("fructose-2,6-\nbisphosphate", MAGENTA, size=26, pad=0.20).move_to([0.0, 0.25, 0])
        self.play(Transform(parked_token, f26_chip), run_time=1.0)

        self.at("speeds up")
        tok_l = VGroup(*[
            Dot(radius=0.11, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to(f26_chip.get_left() + LEFT * 0.1)
            for _ in range(2)
        ])
        plus = T("+", 36, BLUE, weight=BOLD).move_to([mid.bx - 0.85, 0.65, 0])
        self.add(tok_l)
        self.play(
            tok_l[0].animate.move_to([mid.bx - 0.35, 0.42, 0]),
            tok_l[1].animate.move_to([mid.bx - 0.35, -0.42, 0]),
            c.animate.set_value(0.88),
            mid.blue_lane.animate.set_stroke(width=8.0),
            FadeIn(plus, scale=1.2),
            run_time=1.2,
        )

        self.at("and slows")
        tok_r = VGroup(*[
            Dot(radius=0.11, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to(f26_chip.get_right() + RIGHT * 0.1)
            for _ in range(2)
        ])
        minus = T("-", 40, ORANGE, weight=BOLD).move_to([mid.ox + 0.85, 0.65, 0])
        self.add(tok_r)
        self.play(
            tok_r[0].animate.move_to([mid.ox + 0.35, 0.42, 0]),
            tok_r[1].animate.move_to([mid.ox + 0.35, -0.42, 0]),
            mid.orange_lane.animate.set_stroke(width=3.5),
            FadeIn(minus, scale=1.2),
            run_time=1.2,
        )

        self.at("opposite effects")
        self.play(
            plus.animate.scale(1.25),
            minus.animate.scale(1.25),
            run_time=0.8,
        )
        self.play(
            plus.animate.scale(1 / 1.25),
            minus.animate.scale(1 / 1.25),
            run_time=0.8,
        )

        self.at("is the pathway")
        lbl_16 = T("1,6 = pathway", 28, YELLOW).next_to(mid.f16bp, DOWN, buff=0.22)
        self.play(FadeIn(lbl_16, shift=UP * 0.1), run_time=0.7)

        self.at("is the regulator")
        lbl_26 = T("2,6 = regulator", 28, MAGENTA).next_to(f26_chip, DOWN, buff=0.22)
        self.play(FadeIn(lbl_26, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07OneIdea(SpokenScene):
    def construct(self):
        g_top = ValueTracker(0.70)
        n_top = ValueTracker(0.70)
        g_mid = ValueTracker(0.70)
        n_mid = ValueTracker(0.70)
        g_bot = ValueTracker(0.70)
        n_bot = ValueTracker(0.70)

        world = build_full_world(
            lambda: (g_top.get_value() + g_mid.get_value() + g_bot.get_value()) / 3.0,
            lambda: (n_top.get_value() + n_mid.get_value() + n_bot.get_value()) / 3.0,
            station_fns=[
                (lambda: g_top.get_value(), lambda: n_top.get_value()),
                (lambda: g_mid.get_value(), lambda: n_mid.get_value()),
                (lambda: g_bot.get_value(), lambda: n_bot.get_value()),
            ],
            seed=25,
        )
        mid_toks = VGroup(
            Dot(radius=0.09, color=MAGENTA).move_to([FULL_BLUE_X - 0.30, FULL_STATION_YS[1] + 0.25, 0]),
            Dot(radius=0.09, color=MAGENTA).move_to([FULL_ORANGE_X + 0.30, FULL_STATION_YS[1] + 0.25, 0]),
        )
        both_tag = chip("both downhill", GOLD, size=26, pad=0.16).move_to([4.55, 2.35, 0])
        head = T("Downhill both ways: the cell chooses", 34, TEXT).move_to([0.0, 3.25, 0])
        sc = scope_tag("schematic")
        self.play(FadeIn(world), FadeIn(mid_toks), FadeIn(both_tag), FadeIn(head), FadeIn(sc), run_time=0.9)

        self.at("energy cannot choose")
        self.play(
            both_tag[0].animate.set_fill(opacity=0.40),
            world.blue_lane.animate.set_stroke(width=7.5),
            world.orange_lane.animate.set_stroke(width=7.5),
            run_time=1.1,
        )
        self.play(
            both_tag[0].animate.set_fill(opacity=0.16),
            world.blue_lane.animate.set_stroke(width=5.5),
            world.orange_lane.animate.set_stroke(width=5.5),
            run_time=0.9,
        )

        self.at("chooses by regulation")
        self.play(head.animate.set_color(GOLD), run_time=0.7)
        self.play(head.animate.set_color(TEXT), run_time=0.7)

        self.at("turns one enzyme")
        self.play(g_top.animate.set_value(0.95), n_top.animate.set_value(0.18), run_time=0.9)
        self.play(g_mid.animate.set_value(0.95), n_mid.animate.set_value(0.18), run_time=0.9)
        self.play(
            g_bot.animate.set_value(0.95), n_bot.animate.set_value(0.18),
            world.blue_lane.animate.set_stroke(width=7.5),
            world.orange_lane.animate.set_stroke(width=3.5),
            run_time=1.0,
        )
        self.finish()


class S08OneProtein(SpokenScene):
    def construct(self):
        c = ValueTracker(0.35)
        stage = build_protein_stage(c, with_cell_wall=False)
        sc = scope_tag("schematic")
        prot_group = VGroup(stage.lobe_k, stage.lobe_p, stage.prot_body, stage.lbl_prot, stage.lbl_kinase, stage.lbl_phos)
        self.play(FadeIn(stage.mid), FadeIn(stage.gauge_frame), FadeIn(stage.gauge_fill), FadeIn(stage.gauge_lbl), FadeIn(sc), run_time=0.8)

        self.at("A single protein")
        self.play(FadeIn(prot_group, shift=LEFT * 0.2), run_time=0.9)

        self.at("kinase half makes")
        puffs = VGroup(*[
            Dot(radius=0.11, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to([stage.prot_center[0] - 0.95, 0.95, 0])
            for _ in range(3)
        ])
        self.add(puffs)
        self.play(
            stage.lobe_k.animate.set_fill(opacity=0.38),
            LaggedStart(*[p.animate.move_to([-0.25, 0.50 - 0.50 * i, 0]) for i, p in enumerate(puffs)], lag_ratio=0.18),
            c.animate.set_value(0.85),
            run_time=2.2,
        )
        self.play(FadeOut(puffs), stage.lobe_k.animate.set_fill(opacity=0.0), run_time=0.5)

        self.at("phosphatase half destroys")
        swallow = VGroup(*[
            Dot(radius=0.11, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to([-0.25, 0.50 - 0.50 * i, 0])
            for i in range(3)
        ])
        self.add(swallow)
        self.play(
            stage.lobe_p.animate.set_fill(opacity=0.38),
            LaggedStart(*[p.animate.move_to([stage.prot_center[0] + 0.95, 0.95, 0]).scale(0.1) for p in swallow], lag_ratio=0.18),
            c.animate.set_value(0.20),
            run_time=2.0,
        )
        self.play(FadeOut(swallow), stage.lobe_p.animate.set_fill(opacity=0.0), run_time=0.4)

        self.at("Whichever half wins")
        self.play(c.animate.set_value(0.48), run_time=1.0)
        self.finish()


class S09Fed(SpokenScene):
    def construct(self):
        c = ValueTracker(0.45)
        stage = build_protein_stage(c, with_cell_wall=True)
        meal_tag = chip("after a meal", GOLD, size=26, pad=0.16).move_to([-5.05, 3.15, 0])
        sc = scope_tag("schematic")
        self.add(stage, meal_tag, sc)

        self.at("insulin keeps")
        ins_chip = chip("insulin", TEXT, size=24, pad=0.16).move_to([5.80, 2.25, 0])
        sig_arrow = Arrow([5.05, 2.05, 0], [4.15, 1.45, 0], color=TEXT, stroke_width=3.5, buff=0.05)
        self.play(FadeIn(ins_chip, shift=LEFT * 0.15), GrowArrow(sig_arrow), run_time=0.9)

        self.at("kinase half wins")
        self.play(
            stage.lobe_k.animate.set_fill(opacity=0.42),
            stage.lobe_p.animate.set_fill(opacity=0.0),
            run_time=1.1,
        )

        self.at("rises")
        # Route tokens above/around the labels so they never cross letters
        tok_l = Dot(radius=0.10, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to([stage.prot_center[0] - 0.95, 0.95, 0])
        tok_r = Dot(radius=0.10, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to([stage.prot_center[0] - 0.95, 0.95, 0])
        self.add(tok_l, tok_r)
        self.play(
            c.animate.set_value(0.92),
            tok_l.animate.move_to([stage.mid.bx - 0.35, 0.55, 0]),
            tok_r.animate.move_to([stage.mid.ox + 0.35, 0.55, 0]),
            run_time=1.8,
        )

        self.at("speeds up")
        self.play(stage.mid.lbl_pfk.animate.scale(1.10), run_time=0.5)
        self.play(stage.mid.lbl_pfk.animate.scale(1 / 1.10), run_time=0.5)

        self.at("slows")
        self.play(stage.mid.orange_lane.animate.set_stroke(width=3.5), run_time=0.5)

        self.at("glycolysis runs")
        self.play(stage.mid.blue_lane.animate.set_stroke(width=8.5), run_time=0.9)
        self.finish()


class S10Fasting(SpokenScene):
    def construct(self):
        c = ValueTracker(0.92)
        stage = build_protein_stage(c, with_cell_wall=True)
        stage.lobe_k.set_fill(opacity=0.42)
        stage.mid.blue_lane.set_stroke(width=8.5, opacity=1.0)
        stage.mid.orange_lane.set_stroke(width=3.5, opacity=0.40)

        meal_tag = chip("after a meal", GOLD, size=26, pad=0.16).move_to([-5.05, 3.15, 0])
        ins_chip = chip("insulin", TEXT, size=24, pad=0.16).move_to([5.80, 2.25, 0])
        sig_ins = Arrow([5.05, 2.05, 0], [4.15, 1.45, 0], color=TEXT, stroke_width=3.5, buff=0.05)
        tok_l = Dot(radius=0.10, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to([stage.mid.bx - 0.35, 0.55, 0])
        tok_r = Dot(radius=0.10, color=MAGENTA, stroke_color=TEXT, stroke_width=1.5).move_to([stage.mid.ox + 0.35, 0.55, 0])
        sc = scope_tag("schematic")
        self.add(stage, meal_tag, ins_chip, sig_ins, tok_l, tok_r, sc)

        self.at("glucagon takes over")
        fast_tag = chip("in a fast", ORANGE, size=26, pad=0.16).move_to([-5.05, 3.15, 0])
        gluc_chip = chip("glucagon", TEXT, size=24, pad=0.16).move_to([5.90, 2.25, 0])
        self.play(
            swap(meal_tag, fast_tag, run_time=0.7),
            FadeOut(sig_ins, run_time=0.4),
            swap(ins_chip, gluc_chip, run_time=0.7),
        )

        self.at("Working through")
        pka_chip = chip("PKA", TEXT, size=24, pad=0.14).move_to([3.85, 2.25, 0])
        sig_gluc = Arrow([gluc_chip.get_left()[0] - 0.08, 2.25, 0], [pka_chip.get_right()[0] + 0.08, 2.25, 0], color=TEXT, stroke_width=3.5, buff=0.04)
        self.play(GrowArrow(sig_gluc), FadeIn(pka_chip), run_time=0.8)

        self.at("adds a phosphate")
        # Stamp P badge cleanly just above the right lobe rim, clear of 'one protein' and 'PKA'
        p_badge = _phosphate_badge(stage.prot_center + np.array([1.10, 1.12, 0]), size=24, radius=0.28)
        self.play(pka_chip.animate.move_to([4.15, 1.55, 0]), FadeOut(sig_gluc), run_time=0.6)
        self.play(FadeIn(p_badge, scale=1.3), run_time=0.5)
        self.play(FadeOut(pka_chip), run_time=0.4)

        self.at("phosphatase half wins")
        self.play(
            stage.lobe_k.animate.set_fill(opacity=0.0),
            stage.lobe_p.animate.set_fill(opacity=0.42),
            run_time=1.0,
        )

        self.at("Fructose")
        self.play(
            tok_l.animate.move_to([stage.prot_center[0] + 0.95, 0.95, 0]).scale(0.1).set_opacity(0.25),
            tok_r.animate.move_to([stage.prot_center[0] + 0.95, 0.95, 0]).scale(0.1).set_opacity(0.25),
            c.animate.set_value(0.08),
            run_time=2.2,
        )
        self.play(FadeOut(tok_l), FadeOut(tok_r), run_time=0.3)

        self.at("FBP")
        self.play(
            stage.mid.blue_lane.animate.set_stroke(width=3.5, opacity=0.40),
            stage.mid.orange_lane.animate.set_stroke(width=8.5, opacity=1.0),
            run_time=1.1,
        )
        self.finish()


class S11OtherPairs(SpokenScene):
    def construct(self):
        v_gly = ValueTracker(0.16)
        v_gng = ValueTracker(0.95)
        world = build_full_world(lambda: v_gly.get_value(), lambda: v_gng.get_value(), show_station_labels=True, seed=31)

        # Miniature P-tagged protein + low MAGENTA gauge beside middle station (x >= 3.05, clear of cell right wall 2.70)
        mini_prot, _, mini_lp = _two_lobed_protein([4.45, -0.25, 0], width=1.6, height=0.95, color=TEXT)
        mini_lp.set_fill(opacity=0.35)
        mini_p = _phosphate_badge([4.95, 0.35, 0], size=22, radius=0.25)
        mini_g_box = RoundedRectangle(corner_radius=0.06, width=0.24, height=1.1, stroke_color=MAGENTA, stroke_width=2.0).move_to([3.20, -0.25, 0])
        mini_g_fill = Rectangle(width=0.16, height=0.14, stroke_width=0, fill_color=MAGENTA, fill_opacity=0.85).move_to([3.20, -0.70, 0])
        mini_switch = VGroup(mini_lp, mini_prot, mini_p, mini_g_box, mini_g_fill)

        sc = scope_tag("schematic")
        self.play(FadeIn(world), FadeIn(mini_switch), FadeIn(sc), run_time=0.8)

        self.at("controls of their own")
        own_top = chip("own controls", TEXT, size=24, pad=0.14).move_to([4.35, FULL_STATION_YS[0], 0])
        own_bot = chip("own controls", TEXT, size=24, pad=0.14).move_to([4.35, FULL_STATION_YS[2], 0])
        self.play(FadeIn(own_top, shift=LEFT * 0.15), FadeIn(own_bot, shift=LEFT * 0.15), run_time=0.8)

        self.at("one direction dominates")
        self.play(world.orange_lane.animate.set_stroke(width=8.5), world.blue_lane.animate.set_stroke(width=3.5), run_time=0.9)

        self.at("waste stays small")
        wisp_t = ValueTracker(0.0)
        # Single faint RED wisp rises cleanly above the cell without crossing any text
        wisp = always_redraw(lambda: _heat_wave(
            2.45, 2.35 + 0.35 * wisp_t.get_value(),
            height=0.75, opacity=max(0.30, 0.65 - 0.25 * wisp_t.get_value()), phase=4.0 * wisp_t.get_value()
        ))
        waste_lbl = T("waste stays small", 26, RED).move_to([4.45, 2.35, 0])
        self.add(wisp)
        self.play(FadeIn(waste_lbl, shift=UP * 0.1), wisp_t.animate.set_value(1.2), run_time=1.3, rate_func=linear)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        c = ValueTracker(0.08)
        v_gly = ValueTracker(0.16)
        v_gng = ValueTracker(0.95)
        world = build_full_world(lambda: v_gly.get_value(), lambda: v_gng.get_value(), show_station_labels=True, seed=35)

        mini_prot, mini_lk, mini_lp = _two_lobed_protein([5.05, -0.25, 0], width=1.6, height=0.95, color=TEXT)
        mini_lp.set_fill(opacity=0.35)
        mini_p = _phosphate_badge([5.55, 0.55, 0], size=22, radius=0.25)
        gx, gy0, gh = 3.55, -0.95, 1.4
        g_box = RoundedRectangle(corner_radius=0.06, width=0.28, height=gh, stroke_color=MAGENTA, stroke_width=2.2).move_to([gx, gy0 + gh / 2, 0])
        g_fill = always_redraw(lambda: Rectangle(
            width=0.18,
            height=max(0.10, (gh - 0.08) * float(np.clip(c.get_value(), 0.04, 0.96))),
            stroke_width=0, fill_color=MAGENTA, fill_opacity=0.85,
        ).move_to([gx, gy0 + 0.04 + max(0.10, (gh - 0.08) * float(np.clip(c.get_value(), 0.04, 0.96))) / 2, 0]))
        g_lbl = T("2,6 level", 24, MAGENTA).next_to(g_box, UP, buff=0.18)
        both_tag = chip("both downhill", GOLD, size=26, pad=0.16).move_to([4.55, 2.35, 0])
        sc = scope_tag("schematic")
        self.add(world, mini_lk, mini_lp, mini_prot, mini_p, g_box, g_fill, g_lbl, sc)

        self.at("not set by")
        pulses = VGroup(*[
            Circle(radius=0.32, color=BLUE if x == FULL_BLUE_X else ORANGE, stroke_width=3.5).move_to([x, y, 0])
            for y in FULL_STATION_YS for x in (FULL_BLUE_X, FULL_ORANGE_X)
        ])
        self.play(FadeIn(pulses), run_time=0.7)
        self.play(FadeOut(pulses), run_time=0.7)

        self.at("Downhill made")
        self.play(
            FadeIn(both_tag),
            v_gly.animate.set_value(0.65),
            v_gng.animate.set_value(0.65),
            world.blue_lane.animate.set_stroke(width=6.0),
            world.orange_lane.animate.set_stroke(width=6.0),
            run_time=1.1,
        )

        self.at("Regulation decides")
        self.play(
            c.animate.set_value(0.92),
            FadeOut(mini_p),
            mini_lp.animate.set_fill(opacity=0.0),
            mini_lk.animate.set_fill(opacity=0.35),
            v_gly.animate.set_value(0.95),
            v_gng.animate.set_value(0.16),
            world.blue_lane.animate.set_stroke(width=8.5),
            world.orange_lane.animate.set_stroke(width=3.5),
            run_time=1.2,
        )
        self.play(
            c.animate.set_value(0.08),
            FadeIn(mini_p),
            mini_lk.animate.set_fill(opacity=0.0),
            mini_lp.animate.set_fill(opacity=0.35),
            v_gly.animate.set_value(0.16),
            v_gng.animate.set_value(0.95),
            world.blue_lane.animate.set_stroke(width=3.5),
            world.orange_lane.animate.set_stroke(width=8.5),
            run_time=1.2,
        )
        self.finish()


class S13End(EndCard):
    LINE = "Speed one enzyme, slow its opposite, and one direction wins."
