"""
Built While Running — Lesson: "The Wiring Problem: How a Brain Gets Built"

COLOUR MAP (one colour per concept, carried across the whole film):
  BLUE       #58C4DD   genome / DNA rules
  YELLOW     #F5D547   neurons, axons, growing branches, synapse dots, frontal cortex curve
  GREEN      #83C167   neural activity flashes (action potentials / correlated firing)
  RED        #FC6255   removal (fading, retracting branches, dying neurons/synapses)
  GREY       #8B93A1   anatomy, axes, electronic circuit board, target tissue, counting cube, roadmap bars
  TEXT       #E8EAF0   primary labels, white age scrubber, question text
  TEAL       #3FB8C0   rules ("overproduce, then select"), highlighted roadmap steps
  GOLD       #D4A843   target support highlight
  PALE_GOLD  #EAD084   nerve growth factor (NGF) drops
  MAGENTA    #E573FF   auditory cortex curve and tick
  CORAL      #FF9A6C   prefrontal cortex curve, tick and bracket

THE ONE WORLD (carried from scene to scene):
  LEFT half:  Cortex window (GREY rounded frame, ~65% of safe frame height) showing a patch of
              developing neurons with branching arbors, synapse dots, and GREEN activity flashes
              sweeping along active branches. Its size grows slowly with age, and its synapse-dot
              count tracks the age scrubber on the plot.
  RIGHT half: Age-vs-synapse-density plot (compressed age ticks: birth, 1, 2, 5, 10, 20, 30 yr;
              schematic dashed adult=1.0 line; WHITE age scrubber) or the contrasting electronic
              circuit board / 9-step developmental roadmap.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s00_link_and_question : Tightened retinal map (6 axons converging, GREEN step-sweeps) dissolves into
                          the cortex window with extending YELLOW branches and GREEN flashes; electronic
                          circuit board slides in at right with unplugged cord and rising solder smoke.
  s02_board             : Soldering iron lifts, plug seats into socket, PCB traces light up fixed; focus
                          shifts left to the cortex window where branches extend while GREEN flashes run.
  s03_running           : Board exits and Plot enters with WHITE scrubber before birth; early thicker
                          branches carry repeated GREEN flashes while thin new tips grow outward; active
                          synapses brighten/enlarge while a silent synapse dims toward RED.
  s04_extra             : Window shifts to 8 YELLOW neurons wired to GREY target, crowds to 14 neurons
                          overproducing, then 6 neurons turn RED, retract axons and fade out.
  s05_compete           : Row rewinds to 14 active neurons; GREY target releases fixed PALE_GOLD NGF
                          drops that travel retrogradely along 8 axons into somas (brightening + firing
                          GREEN), while the 6 starved neurons turn RED and fade away.
  s06_idea              : Cortex patch returns with active branches extending; extra YELLOW branches and
                          synapse dots sprout, then active ones brighten while silent ones dim RED and retract.
  s07_huttenlocher      : Faint guessed rise-then-fall arc draws and fades; counting cube scans over
                          cortex window and blinks each enclosed synapse dot in sequence as sample ticks
                          appear along the age axis.
  s08_curve             : Single WHITE age scrubber ValueTracker drives live YELLOW frontal curve
                          (1.10 at birth -> 1.50 peak at 1-2 yr -> 1.00 at 20 yr), cortex window size
                          expansion, and window synapse-dot count simultaneously.
  s09_predict           : Scrubber parks at 10 yr; cortex window enlarges further around a fixed-size
                          counting cube so enclosed dot count drops without removing dots.
  s11_answer            : Split window shows left tissue stretching (same 20 dots, cube count 12 -> 6)
                          vs right dots turning RED and vanishing (fewer dots, cube count 12 -> 6); then
                          merges into a single dendrite tracked across 3 time points as 2 spines retract.
  s12_regions           : Frontal curve dims to ghost; computed MAGENTA auditory (peak 3 mo) and CORAL
                          prefrontal (peak >15 mo, tail sloping to 30 yr) curves draw; scrubber moves to
                          age 25 as a few cortical synapse dots dim RED.
  s13_roadmap           : Nine overlapping GREY developmental bars build as a staircase; bar 7 lights
                          TEAL with RED neuron-death echo, bar 9 lights TEAL as GREEN flashes and RED
                          branch retraction run in the window.
  s14_close             : Ghost board dissolves; cortex window bursts with extra YELLOW branches/dots,
                          silent ones retract RED while active ones flash GREEN, and frontal curve
                          re-brightens up and down in step.
"""

from bp_parts import *
import numpy as np

# Extra film-specific colours (high contrast on BG #0f1117)
PALE_GOLD = "#EAD084"
MAGENTA = "#E573FF"
CORAL = "#FF9A6C"

# Shared world geometry (inside safe frame x in [-6.3, 6.3], y in [-3.5, 3.5])
WIN_CENTER = np.array([-3.45, 0.22, 0.0])
WIN_BASE_W = 5.20
WIN_BASE_H = 4.45
PLOT_BOX = (0.10, 5.90, -1.70, 2.35)

# Compressed age axis coordinates u in [0, 7.2]
AGE_TICKS = [
    (0.3, "birth"),
    (1.5, "1"),
    (2.6, "2"),
    (3.7, "5"),
    (4.8, "10"),
    (5.9, "20"),
    (6.9, "30"),
]
U_BIRTH = 0.3
U_3MO = 0.85
U_15MO = 1.95
U_PEAK_FRONTAL = 2.05
U_PEAK_AUDITORY = 0.85
U_PEAK_PREFRONTAL = 2.25
U_10YR = 4.8
U_20YR = 5.9
U_25YR = 6.4
U_30YR = 6.9


# ------------------------------------------------------------------ computed biological curves
def frontal_density(u):
    """Huttenlocher (1979) schematic frontal cortex synapse density (adult = 1.0, peak = 1.5 at 1-2 yr)."""
    u = float(u)
    if u <= U_BIRTH:
        return 1.10
    if u <= U_PEAK_FRONTAL:
        frac = (u - U_BIRTH) / (U_PEAK_FRONTAL - U_BIRTH)
        return 1.10 + 0.40 * (np.sin(0.5 * np.pi * frac) ** 1.35)
    if u <= U_20YR:
        frac = (u - U_PEAK_FRONTAL) / (U_20YR - U_PEAK_FRONTAL)
        return 1.00 + 0.50 * 0.5 * (1.0 + np.cos(np.pi * frac))
    return 1.00


def auditory_density(u):
    """Schematic auditory cortex curve: peaks ~3 mo (same schematic height 1.45, not data)."""
    u = float(u)
    if u <= U_BIRTH:
        return 1.05
    if u <= U_PEAK_AUDITORY:
        frac = (u - U_BIRTH) / (U_PEAK_AUDITORY - U_BIRTH)
        return 1.05 + 0.40 * np.sin(0.5 * np.pi * frac)
    if u <= 4.2:
        frac = (u - U_PEAK_AUDITORY) / (4.2 - U_PEAK_AUDITORY)
        return 1.00 + 0.45 * 0.5 * (1.0 + np.cos(np.pi * frac))
    return 1.00


def prefrontal_density(u):
    """Schematic prefrontal cortex curve: peaks >15 mo, continues declining into third decade (20-30 yr)."""
    u = float(u)
    if u <= U_BIRTH:
        return 1.05
    if u <= U_PEAK_PREFRONTAL:
        frac = (u - U_BIRTH) / (U_PEAK_PREFRONTAL - U_BIRTH)
        return 1.05 + 0.40 * (np.sin(0.5 * np.pi * frac) ** 1.25)
    if u <= U_30YR:
        frac = (u - U_PEAK_PREFRONTAL) / (U_30YR - U_PEAK_PREFRONTAL)
        return 1.01 + 0.44 * ((1.0 - frac) ** 1.45)
    return 1.01


def window_scale_for_age(u):
    """Tissue growth factor for cortex window outline (0.90 at birth -> 1.06 at 20-30 yr)."""
    frac = np.clip((u - U_BIRTH) / (U_20YR - U_BIRTH), 0.0, 1.0)
    return 0.90 + 0.16 * frac


# ------------------------------------------------------------------ cortex window builder
def _lerp(p0, p1, s):
    return (1.0 - s) * p0 + s * p1


def _make_flash_pulse(p0, p1, phase, speed, r_core=0.095, r_halo=0.18, scale_fn=None, center=WIN_CENTER):
    """Action-potential GREEN flash core + halo traveling along segment (p0 -> p1)."""
    def _pos(a, b, ph):
        p = _lerp(a, b, ph)
        if scale_fn is not None:
            p = center + (p - center) * scale_fn()
        return p

    core = Dot(_pos(p0, p1, phase), radius=r_core, color=GREEN, fill_opacity=0.95)
    halo = Circle(radius=r_halo, stroke_color=GREEN, stroke_width=2.4, stroke_opacity=0.65,
                  fill_color=GREEN, fill_opacity=0.18).move_to(core)
    pulse_mob = VGroup(halo, core)
    pulse_mob._seg = (p0, p1)
    pulse_mob._phase = phase
    pulse_mob._speed = speed

    def _move_flash(m, dt):
        m._phase = (m._phase + m._speed * dt) % 1.0
        a, b = m._seg
        pos = _pos(a, b, m._phase)
        m.move_to(pos)
        op = float(np.sin(np.pi * m._phase))
        m[0].set_stroke(opacity=0.15 + 0.65 * op).set_fill(opacity=0.05 + 0.22 * op)
        m[1].set_fill(opacity=0.25 + 0.75 * op)

    pulse_mob.add_updater(_move_flash)
    return pulse_mob


def make_cortex_network(
    center=WIN_CENTER,
    w=WIN_BASE_W,
    h=WIN_BASE_H,
    seed=7,
    n_neurons=14,
    reserve_top_left=False,
    synapse_level=1.0,
    growing_frac=1.0,
    flash_scale_fn=None,
):
    """Deterministic patch of developing cortex inside a RoundedRectangle frame."""
    rng = np.random.default_rng(seed)
    cx, cy, _ = center
    frame = RoundedRectangle(
        corner_radius=0.22,
        width=w,
        height=h,
        stroke_color=GREY,
        stroke_width=3.2,
        fill_color=BG,
        fill_opacity=0.70,
    ).move_to(center)

    # Inner safe box strictly inside RoundedRectangle border
    mx = w / 2 - 0.36
    my = h / 2 - 0.36
    clamp = lambda p: np.array([
        np.clip(p[0], cx - mx, cx + mx),
        np.clip(p[1], cy - my, cy + my),
        0.0,
    ])

    def _avoid_tl(p):
        if reserve_top_left and p[0] < cx + 0.15 and p[1] > cy + my - 0.68:
            p = p.copy()
            p[1] = cy + my - 0.68
        return p

    # Jittered 4x4 grid for 14 well-spread neurons
    cols, rows = 4, 4
    grid_pts = []
    for r in range(rows):
        for c in range(cols):
            gx = cx - mx * 0.78 + c * (2 * mx * 0.78 / (cols - 1)) + rng.uniform(-0.18, 0.18)
            gy = cy - my * 0.78 + r * (2 * my * 0.78 / (rows - 1)) + rng.uniform(-0.14, 0.14)
            grid_pts.append(_avoid_tl(clamp(np.array([gx, gy, 0.0]))))
    rng.shuffle(grid_pts)
    soma_pts = grid_pts[:n_neurons]

    somas = VGroup()
    early_lines = VGroup()
    late_lines = VGroup()
    extra_lines = VGroup()
    silent_lines = VGroup()
    early_segs = []
    late_segs = []
    early_syns = VGroup()
    extra_syns = VGroup()
    silent_syns = VGroup()

    for i, sp in enumerate(soma_pts):
        soma = Dot(sp, radius=0.115, color=YELLOW, fill_opacity=0.95)
        somas.add(soma)
        # 2 early active two-segment arbors per neuron
        for b in range(2):
            ang = rng.uniform(0, TAU)
            length = rng.uniform(0.75, 1.25)
            mid = _avoid_tl(clamp(sp + np.array([np.cos(ang), np.sin(ang), 0.0]) * (length * 0.55)))
            end = _avoid_tl(clamp(mid + np.array([np.cos(ang + rng.uniform(-0.55, 0.55)),
                                                  np.sin(ang + rng.uniform(-0.55, 0.55)), 0.0]) * (length * 0.55)))
            ln1 = Line(sp, mid, color=YELLOW, stroke_width=3.8, stroke_opacity=0.90)
            ln2 = Line(mid, end, color=YELLOW, stroke_width=3.0, stroke_opacity=0.85)
            early_lines.add(ln1, ln2)
            early_segs.append((sp, mid, (i * 0.37 + b * 0.51) % 1.0))
            early_segs.append((mid, end, (i * 0.37 + b * 0.51 + 0.45) % 1.0))
            early_syns.add(Dot(end, radius=0.068, color=YELLOW, fill_opacity=0.95))

        # 1 later-growing branch (some silent)
        ang_l = rng.uniform(0, TAU)
        l_len = rng.uniform(0.55, 0.95) * growing_frac
        end_l = _avoid_tl(clamp(sp + np.array([np.cos(ang_l), np.sin(ang_l), 0.0]) * max(l_len, 0.16)))
        ln_l = Line(sp, end_l, color=YELLOW, stroke_width=2.2, stroke_opacity=0.72)
        late_lines.add(ln_l)
        late_segs.append((sp, end_l))
        if i % 3 == 0:
            silent_lines.add(ln_l)
            silent_syns.add(Dot(end_l, radius=0.058, color=YELLOW, fill_opacity=0.85))

        # Extra overproduction branches & synapses
        for ex in range(2):
            ang_e = rng.uniform(0, TAU)
            e_len = rng.uniform(0.45, 0.98)
            end_e = _avoid_tl(clamp(sp + np.array([np.cos(ang_e), np.sin(ang_e), 0.0]) * e_len))
            ln_e = Line(sp, end_e, color=YELLOW, stroke_width=2.2, stroke_opacity=0.78)
            extra_lines.add(ln_e)
            extra_syns.add(Dot(end_e, radius=0.058, color=YELLOW, fill_opacity=0.90))

    # Vivid GREEN action-potential pulses traveling along early branches
    flash_dots = VGroup()
    n_flashes = min(22, len(early_segs))
    for k in range(n_flashes):
        p0, p1, ph = early_segs[(k * 2) % len(early_segs)]
        spd = 0.72 + 0.40 * ((k % 4) / 3.0)
        flash_dots.add(_make_flash_pulse(p0, p1, ph, spd, scale_fn=flash_scale_fn, center=center))

    n_keep_extra = int(np.clip((synapse_level - 0.85) / 0.65, 0.0, 1.0) * len(extra_syns))
    shown_extra_syns = VGroup(*extra_syns[:n_keep_extra]) if n_keep_extra > 0 else VGroup()

    g = VGroup(frame, early_lines, late_lines, somas, early_syns, flash_dots)
    g.frame = frame
    g.somas = somas
    g.early_lines = early_lines
    g.late_lines = late_lines
    g.early_syns = early_syns
    g.extra_lines = extra_lines
    g.extra_syns = extra_syns
    g.shown_extra_syns = shown_extra_syns
    g.silent_lines = silent_lines
    g.silent_syns = silent_syns
    g.flash_dots = flash_dots
    g.early_segs = early_segs
    g.late_segs = late_segs
    return g


# ------------------------------------------------------------------ electronic circuit board builder
def make_circuit_board(center=np.array([3.2, 0.22, 0.0]), plugged=False):
    """Electronic PCB in GREY with bold traces, solder joints, plug/cord, and soldering iron."""
    board = RoundedRectangle(
        corner_radius=0.16,
        width=4.8,
        height=3.6,
        stroke_color=GREY,
        stroke_width=3.2,
        fill_color=GREY,
        fill_opacity=0.14,
    ).move_to(center)

    trace_pts = [
        [[-1.8, 1.05], [-0.45, 1.05], [0.0, 0.45], [1.6, 0.45]],
        [[-1.8, 0.15], [-0.75, 0.15], [-0.3, -0.45], [1.6, -0.45]],
        [[-1.8, -0.95], [0.55, -0.95], [0.95, -0.15], [1.6, -0.15]],
        [[-0.45, 1.05], [-0.45, 1.35], [0.90, 1.35], [0.90, 0.45]],
    ]
    traces = VGroup()
    joints = VGroup()
    for path in trace_pts:
        pts = [center + np.array([x, y, 0.0]) for x, y in path]
        for a, b in zip(pts[:-1], pts[1:]):
            traces.add(Line(a, b, color=TEAL if plugged else GREY, stroke_width=4.8 if plugged else 3.4))
        joints.add(Dot(pts[0], radius=0.085, color=TEXT if plugged else GREY))
        joints.add(Dot(pts[-1], radius=0.085, color=TEXT if plugged else GREY))

    chip1 = Rectangle(width=0.95, height=0.68, stroke_color=GREY, stroke_width=2.8,
                      fill_color=BG, fill_opacity=0.95).move_to(center + np.array([-0.15, 0.30, 0.0]))
    chip2 = Rectangle(width=0.72, height=0.56, stroke_color=GREY, stroke_width=2.8,
                      fill_color=BG, fill_opacity=0.95).move_to(center + np.array([0.95, -0.60, 0.0]))

    socket = Rectangle(width=0.38, height=0.46, stroke_color=TEXT, stroke_width=2.8,
                       fill_color=BG, fill_opacity=1.0).move_to(board.get_right() + LEFT * 0.19 + DOWN * 0.95)

    plug_pos = socket.get_right() + RIGHT * 0.14 if plugged else socket.get_right() + np.array([0.65, -0.65, 0.0])
    plug_body = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.40,
                                 stroke_color=TEXT, stroke_width=2.8, fill_color=GREY, fill_opacity=0.55).move_to(plug_pos)
    prongs = VGroup(
        Line(plug_body.get_left() + UP * 0.09, plug_body.get_left() + UP * 0.09 + LEFT * 0.16, color=TEXT, stroke_width=3.2),
        Line(plug_body.get_left() + DOWN * 0.09, plug_body.get_left() + DOWN * 0.09 + LEFT * 0.16, color=TEXT, stroke_width=3.2),
    )
    cord_end = plug_body.get_right() + np.array([0.35, -0.55, 0.0])
    cord = CubicBezier(
        plug_body.get_right(),
        plug_body.get_right() + RIGHT * 0.35,
        cord_end + LEFT * 0.2,
        cord_end,
        color=GREY,
        stroke_width=3.8,
    )
    plug = VGroup(cord, prongs, plug_body)

    joint_target = center + np.array([0.90, 1.35, 0.0])
    tip = joint_target + np.array([0.05, 0.05, 0.0])
    shaft_end = tip + np.array([0.75, 0.92, 0.0])
    handle_end = shaft_end + np.array([0.65, 0.80, 0.0])
    iron = VGroup(
        Line(tip, shaft_end, color=TEXT, stroke_width=5.0),
        Line(shaft_end, handle_end, color=GOLD, stroke_width=12.0),
    )

    g = VGroup(board, traces, chip1, chip2, joints, socket, plug)
    g.board = board
    g.traces = traces
    g.joints = joints
    g.socket = socket
    g.plug = plug
    g.iron = iron
    g.joint_target = joint_target
    return g


def make_solder_smoke(origin):
    """Thread of rising solder smoke with an updater."""
    smoke = VMobject(stroke_color=TEXT, stroke_width=3.0, stroke_opacity=0.60, fill_opacity=0)
    smoke._t = 0.0

    def _update_smoke(m, dt):
        m._t += dt
        ys = np.linspace(0.0, 1.05, 20)
        pts = [
            origin + np.array([0.12 * np.sin(3.6 * y - 3.6 * m._t) + 0.08 * y, y, 0.0])
            for y in ys
        ]
        m.set_points_as_corners(pts)

    smoke.add_updater(_update_smoke)
    _update_smoke(smoke, 0.0)
    return smoke


# ------------------------------------------------------------------ shared Huttenlocher Plot builder
def make_age_plot(show_adult=True, show_ticks=True):
    """Standard right-side age vs synapse density plot carried across the film."""
    P = Plot(
        box=PLOT_BOX,
        xr=(0.0, 7.2),
        yr=(0.0, 1.85),
        xticks=AGE_TICKS if show_ticks else (),
        yticks=(),
        xlabel="age",
        ylabel="synapse density",
        color=GREY,
        size=24,
        label_size=26,
        stroke=3.2,
    )
    if show_adult:
        ln = P.hline(1.0, None, GREY, dashed=True)
        b = P.pt(7.2, 1.0)
        lbl = T("adult", 24, GREY).next_to(b, RIGHT, buff=0.10)
        adult = VGroup(ln, lbl)
    else:
        adult = VGroup()
    return P, adult


def make_scrubber(P, u_tracker):
    """WHITE vertical scrubber on the age axis tied to u_tracker (stops cleanly below top label band)."""
    def _mk():
        u = u_tracker.get_value()
        bot = P.pt(u, 0.0)
        top = P.pt(u, 1.56)
        ln = Line(bot, top, color=TEXT, stroke_width=3.2, stroke_opacity=0.88)
        tri = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1.0).scale(0.11).rotate(PI).next_to(bot, UP, buff=0.0)
        return VGroup(ln, tri)
    return always_redraw(_mk)


def make_counting_cube(center, side=1.18):
    """Small GREY wireframe counting cube inside the cortex window."""
    off = np.array([0.20, 0.18, 0.0])
    front = Square(side_length=side, stroke_color=TEXT, stroke_width=2.6, fill_color=GREY, fill_opacity=0.08).move_to(center)
    back = Square(side_length=side, stroke_color=GREY, stroke_width=2.0, fill_opacity=0).move_to(center + off)
    edges = VGroup(*[
        Line(front.get_corner(c), back.get_corner(c), color=GREY, stroke_width=2.0)
        for c in (UL, UR, DL, DR)
    ])
    g = VGroup(back, edges, front)
    g.front = front
    return g


# ------------------------------------------------------------------ 14-neuron competition builder (s04 / s05)
def make_neuron_row(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, n_total=14, survivors=None):
    """Row of n_total YELLOW neurons at left of window sending axons to GREY target band at right."""
    if survivors is None:
        survivors = {0, 2, 4, 6, 7, 9, 11, 13}
    cx, cy, _ = center
    frame = RoundedRectangle(
        corner_radius=0.22, width=w, height=h,
        stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.70
    ).move_to(center)

    target_x = cx + w / 2 - 0.65
    target_band = RoundedRectangle(
        corner_radius=0.10, width=0.76, height=h - 0.96,
        stroke_color=GREY, stroke_width=2.6, fill_color=GREY, fill_opacity=0.22
    ).move_to([target_x, cy - 0.24, 0.0])
    target_label = T("target", 24, TEXT).next_to(target_band, UP, buff=0.08)

    soma_x = cx - w / 2 + 0.58
    y_top = cy + h / 2 - 0.48
    y_bot = cy - h / 2 + 0.48
    ys = np.linspace(y_top, y_bot, n_total)

    somas = VGroup()
    axons = VGroup()
    surv_somas, die_somas = VGroup(), VGroup()
    surv_axons, die_axons = VGroup(), VGroup()
    axon_paths = []

    for i, y in enumerate(ys):
        p0 = np.array([soma_x, y, 0.0])
        p1_y = float(np.clip(
            y * 0.90 + (cy - 0.12) * 0.10,
            target_band.get_bottom()[1] + 0.12,
            target_band.get_top()[1] - 0.12,
        ))
        p1 = np.array([target_band.get_left()[0] + 0.18, p1_y, 0.0])
        soma = Dot(p0, radius=0.105 if n_total <= 8 else 0.085, color=YELLOW, fill_opacity=0.95)
        axon = Line(p0, p1, color=YELLOW, stroke_width=3.2 if n_total <= 8 else 2.5, stroke_opacity=0.88)
        somas.add(soma)
        axons.add(axon)
        axon_paths.append((i, p0, p1))
        if i in survivors:
            surv_somas.add(soma)
            surv_axons.add(axon)
        else:
            die_somas.add(soma)
            die_axons.add(axon)

    g = VGroup(frame, target_band, target_label, axons, somas)
    g.frame = frame
    g.target_band = target_band
    g.target_label = target_label
    g.somas = somas
    g.axons = axons
    g.surv_somas = surv_somas
    g.die_somas = die_somas
    g.surv_axons = surv_axons
    g.die_axons = die_axons
    g.axon_paths = axon_paths
    return g


def attach_row_flashes(row_group, indices=None):
    """Add vivid GREEN firing pulses along axons of a neuron row."""
    flashes = VGroup()
    paths = [p for p in row_group.axon_paths if indices is None or p[0] in indices]
    for k, (idx, p0, p1) in enumerate(paths):
        flashes.add(_make_flash_pulse(p0, p1, (k * 0.23) % 1.0, 0.78 + 0.18 * (k % 3), r_core=0.075, r_halo=0.14))
    return flashes


# ================================================================== SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        # Open on chapter 1's tightened retinal map + BLUE DNA icon with crossed list
        pal = [YELLOW, TEAL, BLUE, GOLD, YELLOW, TEAL]
        ret_box = RoundedRectangle(
            corner_radius=0.18, width=5.6, height=4.6,
            stroke_color=GREY, stroke_width=2.8, fill_color=BG, fill_opacity=0.70
        ).move_to([-2.8, 0.15, 0])
        ret_cells = VGroup(*[
            Dot(ret_box.get_left() + RIGHT * 0.58 + UP * y, radius=0.13, color=pal[i])
            for i, y in enumerate(np.linspace(1.55, -1.55, 6))
        ])
        tgt_spots = VGroup(*[
            Dot(ret_box.get_right() + LEFT * 0.65 + UP * y, radius=0.11, color=pal[i])
            for i, y in enumerate(np.linspace(1.55, -1.55, 6))
        ])
        ret_axons = VGroup(*[
            Line(a.get_center(), b.get_center(), color=pal[i], stroke_width=3.8)
            for i, (a, b) in enumerate(zip(ret_cells, tgt_spots))
        ])
        ret_label = T("retinal map", 26, TEXT).next_to(ret_box, DOWN, buff=0.22)

        # Sweeping GREEN wave across retinal cells & axons
        sweep = ValueTracker(0.0)
        wave_dots = VGroup(*[
            always_redraw(lambda i=i, a=a, b=b: VGroup(
                Circle(
                    radius=0.18, stroke_color=GREEN, stroke_width=2.5,
                    stroke_opacity=0.7 * np.sin(np.pi * np.clip((sweep.get_value() - i * 0.10) % 1.15, 0.0, 1.0)),
                    fill_color=GREEN, fill_opacity=0.22 * np.sin(np.pi * np.clip((sweep.get_value() - i * 0.10) % 1.15, 0.0, 1.0)),
                ).move_to(_lerp(a.get_center(), b.get_center(), np.clip((sweep.get_value() - i * 0.10) % 1.15, 0.0, 1.0))),
                Dot(
                    _lerp(a.get_center(), b.get_center(), np.clip((sweep.get_value() - i * 0.10) % 1.15, 0.0, 1.0)),
                    radius=0.10, color=GREEN,
                    fill_opacity=0.95 * np.sin(np.pi * np.clip((sweep.get_value() - i * 0.10) % 1.15, 0.0, 1.0))
                ),
            ))
            for i, (a, b) in enumerate(zip(ret_cells, tgt_spots))
        ])
        sweep.add_updater(lambda m, dt: m.increment_value(1.0 * dt))
        self.add(sweep)

        # BLUE DNA rule icon + crossed list at right
        dna_panel = RoundedRectangle(
            corner_radius=0.18, width=4.8, height=4.6,
            stroke_color=BLUE, stroke_width=2.8, fill_color=BLUE, fill_opacity=0.10
        ).move_to([3.1, 0.15, 0])
        ys_dna = np.linspace(-0.95, 0.95, 16)
        strand1 = VMobject(stroke_color=BLUE, stroke_width=4.0).set_points_as_corners([
            dna_panel.get_center() + np.array([-1.35 + 0.28 * np.sin(3.5 * y), y + 0.55, 0.0]) for y in ys_dna
        ])
        strand2 = VMobject(stroke_color=BLUE, stroke_width=4.0).set_points_as_corners([
            dna_panel.get_center() + np.array([-1.35 - 0.28 * np.sin(3.5 * y), y + 0.55, 0.0]) for y in ys_dna
        ])
        dna_lbl = T("genome: rules", 28, BLUE).move_to(dna_panel.get_center() + np.array([0.65, 0.88, 0.0]))
        list_lines = VGroup(*[
            Line(dna_panel.get_center() + np.array([-0.05, -0.45 - 0.28 * k, 0]),
                 dna_panel.get_center() + np.array([1.65, -0.45 - 0.28 * k, 0]),
                 color=GREY, stroke_width=3.0)
            for k in range(4)
        ])
        cross1 = Line(list_lines.get_corner(DL) + LEFT * 0.1, list_lines.get_corner(UR) + RIGHT * 0.1, color=RED, stroke_width=4.5)
        cross2 = Line(list_lines.get_corner(UL) + LEFT * 0.1, list_lines.get_corner(DR) + RIGHT * 0.1, color=RED, stroke_width=4.5)
        list_lbl = T("wire list", 24, GREY).next_to(list_lines, LEFT, buff=0.2)
        dna_group = VGroup(dna_panel, strand1, strand2, dna_lbl, list_lines, cross1, cross2, list_lbl)
        cross1.layout_ok = True
        cross2.layout_ok = True

        s_tag = scope_tag("schematic")
        self.add(ret_box, ret_axons, ret_cells, tgt_spots, ret_label, wave_dots, dna_group, s_tag)

        # Beat 1: "genome"
        self.at("genome")
        self.play(Indicate(dna_lbl, color=BLUE, scale_factor=1.08), run_time=0.6)

        # Beat 2: "tissue measures" -> retinal map dissolves into cortex window at left
        self.at("tissue measures")
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.55)
        self.remove(wave_dots, sweep)
        self.play(
            FadeOut(VGroup(ret_box, ret_axons, ret_cells, tgt_spots, ret_label), run_time=0.55),
            FadeIn(win.frame, win.somas, win.early_lines, win.early_syns, win.flash_dots, run_time=0.7),
        )
        self.play(Create(win.late_lines), run_time=1.0)

        # Beat 3: "working circuit" -> emphasize GREEN flashes running in window
        self.at("working circuit")
        self.play(win.frame.animate.set_stroke(GREEN, width=3.8), run_time=0.45)
        self.play(win.frame.animate.set_stroke(GREY, width=3.2), run_time=0.45)

        # Beat 4: "Does a brain" -> electronic circuit board slides in at right, soldering iron + smoke, top question
        self.at("Does a brain")
        pcb = make_circuit_board(center=np.array([3.2, 0.22, 0.0]), plugged=False)
        smoke = make_solder_smoke(pcb.joint_target)
        q_top = T("Switched on when finished?", 34, TEXT).move_to([0.0, 3.24, 0.0])
        self.play(
            FadeOut(dna_group, run_time=0.35),
            FadeIn(pcb, shift=LEFT * 0.4, run_time=0.7),
            FadeIn(pcb.iron, shift=LEFT * 0.4, run_time=0.7),
            FadeIn(smoke, run_time=0.6),
            FadeIn(q_top, shift=DOWN * 0.15, run_time=0.6),
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.55)
        pcb = make_circuit_board(center=np.array([3.2, 0.22, 0.0]), plugged=False)
        smoke = make_solder_smoke(pcb.joint_target)
        q_top = T("Switched on when finished?", 34, TEXT).move_to([0.0, 3.24, 0.0])
        s_tag = scope_tag("schematic")
        self.add(win, pcb, pcb.iron, smoke, q_top, s_tag)

        title = T("Built While Running", 46, TEXT, font=TITLE_FONT).move_to([0.0, 3.24, 0.0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.10)
        self.play(swap(q_top, VGroup(title, rule), run_time=0.55))
        self.play(win.late_lines.animate.set_stroke(width=2.6), run_time=0.95)
        self.play(FadeOut(VGroup(title, rule), run_time=0.35))
        self.finish()


class S02Board(SpokenScene):
    def construct(self):
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.55)
        pcb = make_circuit_board(center=np.array([3.2, 0.22, 0.0]), plugged=False)
        smoke = make_solder_smoke(pcb.joint_target)
        s_tag = scope_tag("schematic")
        self.add(win, pcb, pcb.iron, smoke, s_tag)

        self.at("assembled")
        self.remove(smoke)
        self.play(
            FadeOut(smoke, run_time=0.3),
            pcb.iron.animate.shift(UR * 1.2).set_opacity(0.0),
            run_time=0.8,
        )
        self.remove(pcb.iron)

        self.at("switched on")
        pcb_lit = make_circuit_board(center=np.array([3.2, 0.22, 0.0]), plugged=True)
        tag_on = T("assembled, then on", 28, TEXT).next_to(pcb.board, DOWN, buff=0.45)
        self.play(
            Transform(pcb.plug, pcb_lit.plug),
            Transform(pcb.traces, pcb_lit.traces),
            Transform(pcb.joints, pcb_lit.joints),
            FadeIn(tag_on, shift=UP * 0.1),
            run_time=0.85,
        )

        self.at("does not change")
        tag_fixed = T("wiring fixed", 28, GREY).move_to(tag_on)
        self.play(swap(tag_on, tag_fixed, run_time=0.55))

        self.at("developing neural")
        tag_win = T("working while built", 28, GREEN).next_to(win.frame, DOWN, buff=0.30)
        new_tips = VGroup(*[
            Line(p1, p1 + (p1 - p0) * 0.30, color=YELLOW, stroke_width=2.4, stroke_opacity=0.88)
            for p0, p1 in win.late_segs[:8]
        ])
        self.play(
            pcb.animate.set_opacity(0.35),
            tag_fixed.animate.set_opacity(0.35),
            win.frame.animate.set_stroke(TEXT, width=3.6),
            Create(new_tips),
            FadeIn(tag_win, shift=UP * 0.1),
            run_time=1.0,
        )
        self.finish()


class S03Running(SpokenScene):
    def construct(self):
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.55)
        pcb = make_circuit_board(center=np.array([3.2, 0.22, 0.0]), plugged=True).set_opacity(0.35)
        s_tag = scope_tag("schematic")
        self.add(win, pcb, s_tag)

        # Slide out circuit board and bring in Plot with WHITE scrubber parked before birth
        P, adult = make_age_plot()
        u_scrubber = ValueTracker(0.14)
        scrubber = make_scrubber(P, u_scrubber)

        self.at("Embryonic")
        self.play(
            FadeOut(pcb, shift=RIGHT * 1.2, run_time=0.6),
            Create(P, run_time=0.9),
            FadeIn(adult, run_time=0.6),
        )
        self.add(scrubber)
        # Active embryonic soma pulse while waiting for next beat
        self.play(*[s.animate.scale(1.18).set_color(GREEN) for s in win.somas[:5]], run_time=0.8)
        self.play(*[s.animate.scale(1.0 / 1.18).set_color(YELLOW) for s in win.somas[:5]], run_time=0.8)

        self.at("made early")
        self.play(win.early_lines.animate.set_stroke(width=4.4, opacity=1.0), run_time=0.9)

        self.at("still growing")
        grow_tips = VGroup(*[
            Line(p1, p1 + (p1 - p0) * 0.35, color=YELLOW, stroke_width=2.2, stroke_opacity=0.80)
            for p0, p1 in win.late_segs
        ])
        self.play(Create(grow_tips), run_time=1.8)

        self.at("help decide")
        silent_dot = win.silent_syns[0]
        self.add(silent_dot)
        # Scale each synapse dot individually about its own centre (keeps every dot inside the frame!)
        self.play(
            *[d.animate.scale(1.45).set_color(TEXT) for d in win.early_syns[:8]],
            silent_dot.animate.set_color(RED).scale(1.30),
            run_time=1.2,
        )
        self.finish()


class S04Extra(SpokenScene):
    def construct(self):
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.7)
        P, adult = make_age_plot()
        u_scrubber = ValueTracker(0.14)
        scrubber = make_scrubber(P, u_scrubber)
        s_tag = scope_tag("schematic")
        self.add(win, P, adult, scrubber, s_tag)

        self.at("overproduce")
        teal_card = boxed_label("overproduce, then select", TEAL, size=26).move_to([WIN_CENTER[0], 3.12, 0.0])
        self.play(FadeIn(teal_card, shift=DOWN * 0.25), run_time=0.6)

        self.at("whole neurons")
        row8 = make_neuron_row(n_total=8, survivors=set(range(8)))
        flashes8 = attach_row_flashes(row8)
        self.remove(win.flash_dots)
        self.play(
            FadeOut(VGroup(win.somas, win.early_lines, win.late_lines, win.early_syns), run_time=0.4),
            Transform(win.frame, row8.frame, run_time=0.5),
            FadeIn(VGroup(row8.target_band, row8.target_label, row8.axons, row8.somas), run_time=0.6),
        )
        self.add(flashes8)

        self.at("more neurons")
        survivors = {0, 2, 4, 6, 7, 9, 11, 13}
        row14 = make_neuron_row(n_total=14, survivors=survivors)
        self.remove(flashes8)
        self.play(
            FadeOut(VGroup(row8.axons, row8.somas), run_time=0.25),
            FadeIn(VGroup(row14.axons, row14.somas), run_time=0.65),
        )
        flashes14 = attach_row_flashes(row14)
        self.add(flashes14)

        self.at("many of them die")
        self.remove(flashes14)
        self.play(
            row14.die_somas.animate.set_color(RED),
            row14.die_axons.animate.set_color(RED),
            run_time=0.45,
        )
        self.play(
            FadeOut(row14.die_somas, run_time=0.55),
            FadeOut(row14.die_axons, run_time=0.55),
        )
        flashes_surv = attach_row_flashes(row14, survivors)
        self.add(flashes_surv)
        self.finish()


class S05Compete(SpokenScene):
    def construct(self):
        survivors = {0, 2, 4, 6, 7, 9, 11, 13}
        row14 = make_neuron_row(n_total=14, survivors=survivors)
        flashes14 = attach_row_flashes(row14)
        P, adult = make_age_plot()
        u_scrubber = ValueTracker(0.14)
        scrubber = make_scrubber(P, u_scrubber)
        teal_card = boxed_label("overproduce, then select", TEAL, size=26).move_to([WIN_CENTER[0], 3.12, 0.0])
        s_tag = scope_tag("schematic")
        self.add(row14, flashes14, P, adult, scrubber, teal_card, s_tag)

        self.at("competition")
        comp_card = boxed_label("competition for support", TEAL, size=26).move_to([WIN_CENTER[0], 3.12, 0.0])
        self.play(swap(teal_card, comp_card, run_time=0.65))

        self.at("limited support")
        rng = np.random.default_rng(11)
        surv_paths = [p for p in row14.axon_paths if p[0] in survivors]
        drops = VGroup()
        drop_targets = []
        for k in range(16):
            _, p0, p1 = surv_paths[k % len(surv_paths)]
            start = p1 + np.array([rng.uniform(-0.08, 0.16), rng.uniform(-0.08, 0.08), 0.0])
            drops.add(Dot(start, radius=0.072, color=PALE_GOLD, fill_opacity=0.95))
            drop_targets.append((drops[-1], p0))
        ngf_lbl = T("nerve growth factor", 26, PALE_GOLD).next_to(row14.frame, DOWN, buff=0.28)
        self.play(FadeIn(drops, scale=0.7), FadeIn(ngf_lbl, shift=UP * 0.1), run_time=0.7)

        self.at("nerve growth factor")
        self.play(*[d.animate.move_to(p0) for d, p0 in drop_targets], run_time=1.35)

        self.at("compete")
        self.remove(flashes14)
        # Scale each surviving soma about its own centre (never as a VGroup!)
        self.play(
            *[s.animate.scale(1.28).set_color(PALE_GOLD) for s in row14.surv_somas],
            FadeOut(drops, run_time=0.35),
            row14.die_somas.animate.set_color(RED),
            row14.die_axons.animate.set_color(RED),
            run_time=0.6,
        )
        self.play(FadeOut(row14.die_somas), FadeOut(row14.die_axons), run_time=0.55)
        flashes_surv = attach_row_flashes(row14, survivors)
        self.add(flashes_surv)
        self.finish()


class S06Idea(SpokenScene):
    def construct(self):
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.75)
        P, adult = make_age_plot()
        u_scrubber = ValueTracker(0.14)
        scrubber = make_scrubber(P, u_scrubber)
        teal_card = boxed_label("overproduce, then select", TEAL, size=26).move_to([WIN_CENTER[0], 3.12, 0.0])
        s_tag = scope_tag("schematic")
        # Start with early network, grow late_lines across "does not wait to be finished"
        self.add(win.frame, win.early_lines, win.somas, win.early_syns, win.flash_dots, P, adult, scrubber, teal_card, s_tag)

        line1 = T("runs while built", 26, TEXT).move_to([WIN_CENTER[0], -2.35, 0])
        line2 = T("makes extra", 26, TEXT).move_to([WIN_CENTER[0], -2.77, 0])
        line3 = T("selection after connections", 26, TEXT).move_to([WIN_CENTER[0], -3.19, 0])

        self.at("one idea")
        self.play(Indicate(teal_card, color=TEAL, scale_factor=1.05), run_time=0.6)
        # Continue growing branches during "A brain does not wait to be finished"
        self.play(Create(win.late_lines), run_time=3.2)

        self.at("runs while")
        self.play(FadeIn(line1, shift=RIGHT * 0.15), win.frame.animate.set_stroke(GREEN, width=3.5), run_time=0.65)
        self.play(win.frame.animate.set_stroke(GREY, width=3.2), run_time=0.35)

        self.at("makes extra")
        self.play(
            FadeIn(line2, shift=RIGHT * 0.15),
            Create(win.extra_lines, run_time=1.0),
            FadeIn(win.extra_syns, scale=0.6, run_time=0.9),
        )

        self.at("what stays")
        self.add(win.silent_lines, win.silent_syns)
        self.play(
            FadeIn(line3, shift=RIGHT * 0.15),
            win.early_lines.animate.set_stroke(width=4.2, opacity=1.0),
            win.silent_lines.animate.set_color(RED),
            win.silent_syns.animate.set_color(RED),
            run_time=0.8,
        )
        self.play(FadeOut(win.silent_lines), FadeOut(win.silent_syns), run_time=0.65)
        self.finish()


class S07Huttenlocher(SpokenScene):
    def construct(self):
        win = make_cortex_network(
            center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7,
            n_neurons=14, reserve_top_left=True, growing_frac=0.85
        )
        P, adult = make_age_plot()
        u_scrubber = ValueTracker(0.14)
        scrubber = make_scrubber(P, u_scrubber)
        s_tag = scope_tag("schematic")
        fc_lbl = T("frontal cortex", 24, TEXT).move_to(
            [win.frame.get_left()[0] + 1.25, win.frame.get_top()[1] - 0.36, 0.0]
        )
        self.add(win, P, adult, scrubber, fc_lbl, s_tag)

        self.at("rise")
        guess_fn = lambda u: 1.0 + 0.55 * np.sin(np.pi * np.clip((u - 0.3) / 5.6, 0.0, 1.0))
        guess_arc = DashedVMobject(P.curve(guess_fn, x0=0.3, x1=5.9, color=YELLOW, width=4.5, opacity=0.60), num_dashes=22)
        self.play(Create(guess_arc), run_time=1.6)
        self.play(FadeOut(guess_arc), run_time=0.65)

        self.at("1979")
        h_tag = T("Huttenlocher, 1979", 30, TEXT).move_to([3.0, 3.22, 0])
        self.play(FadeIn(h_tag, shift=DOWN * 0.1), run_time=0.6)

        self.at("counted synapses")
        cube_center = WIN_CENTER + np.array([0.25, -0.22, 0.0])
        cube = make_counting_cube(cube_center, side=1.35)
        inside_dots = [
            d for d in win.early_syns
            if abs(d.get_x() - cube_center[0]) < 0.65 and abs(d.get_y() - cube_center[1]) < 0.65
        ]
        self.play(
            FadeIn(cube),
            P.ylabel.animate.set_color(YELLOW),
            run_time=0.6,
        )
        for d in inside_dots[:8]:
            self.play(d.animate.scale(1.65).set_color(TEXT), run_time=0.22)
            self.play(d.animate.scale(1.0 / 1.65).set_color(YELLOW), run_time=0.18)
        self.play(P.ylabel.animate.set_color(GREY), run_time=0.35)

        self.at("many ages")
        sample_us = [0.3, 0.7, 1.2, 1.7, 2.2, 2.9, 3.7, 4.5, 5.3, 6.1, 6.7]
        sample_marks = VGroup(*[
            Line(P.pt(u, 0.0), P.pt(u, 0.12), color=TEXT, stroke_width=2.8)
            for u in sample_us
        ])
        self.play(FadeIn(sample_marks, lag_ratio=0.08), run_time=0.85)
        self.finish()


class S08Curve(SpokenScene):
    def construct(self):
        P, adult = make_age_plot()
        h_tag = T("Huttenlocher, 1979", 30, TEXT).move_to([3.0, 3.22, 0])
        s_tag = scope_tag("schematic")

        u = ValueTracker(U_BIRTH)
        scrubber = make_scrubber(P, u)
        live_curve = P.live_curve(frontal_density, u, color=YELLOW, width=5.8, x0=U_BIRTH)
        dot = P.dot(lambda: u.get_value(), lambda: frontal_density(u.get_value()), color=YELLOW, ring=TEXT, radius=0.115)

        base_win = make_cortex_network(
            center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7,
            n_neurons=14, reserve_top_left=True, growing_frac=0.95,
            flash_scale_fn=lambda: window_scale_for_age(u.get_value()),
        )
        soma_offs = [s.get_center() - WIN_CENTER for s in base_win.somas]
        early_pts = [(l.get_start() - WIN_CENTER, l.get_end() - WIN_CENTER) for l in base_win.early_lines]
        late_pts = [(l.get_start() - WIN_CENTER, l.get_end() - WIN_CENTER) for l in base_win.late_lines]
        esyn_offs = [d.get_center() - WIN_CENTER for d in base_win.early_syns]
        xsyn_offs = [d.get_center() - WIN_CENTER for d in base_win.extra_syns]

        def _mk_win():
            sc = window_scale_for_age(u.get_value())
            dens = frontal_density(u.get_value())
            fr = RoundedRectangle(
                corner_radius=0.22, width=WIN_BASE_W * sc, height=WIN_BASE_H * sc,
                stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.70
            ).move_to(WIN_CENTER)
            g = VGroup(fr)
            for a, b in early_pts:
                g.add(Line(WIN_CENTER + a * sc, WIN_CENTER + b * sc, color=YELLOW, stroke_width=3.6, stroke_opacity=0.88))
            for a, b in late_pts:
                g.add(Line(WIN_CENTER + a * sc, WIN_CENTER + b * sc, color=YELLOW, stroke_width=2.2, stroke_opacity=0.72))
            for o in soma_offs:
                g.add(Dot(WIN_CENTER + o * sc, radius=0.115, color=YELLOW, fill_opacity=0.95))
            for o in esyn_offs:
                g.add(Dot(WIN_CENTER + o * sc, radius=0.068, color=YELLOW, fill_opacity=0.95))
            n_ex = int(np.clip((dens - 1.0) / 0.50, 0.0, 1.0) * len(xsyn_offs))
            for o in xsyn_offs[:n_ex]:
                g.add(Dot(WIN_CENTER + o * sc, radius=0.062, color=YELLOW, fill_opacity=0.92))
            return g

        dyn_win = always_redraw(_mk_win)
        # Keep 'frontal cortex' comfortably inside even at sc = 0.90
        fc_lbl = T("frontal cortex", 24, TEXT).move_to(
            [WIN_CENTER[0] - WIN_BASE_W * 0.45 + 1.25, WIN_CENTER[1] + WIN_BASE_H * 0.45 - 0.38, 0.0]
        )
        flashes = base_win.flash_dots
        self.add(dyn_win, flashes, fc_lbl, P, adult, live_curve, dot, scrubber, h_tag, s_tag)

        self.at("at birth")
        birth_pt = Dot(P.pt(U_BIRTH, frontal_density(U_BIRTH)), radius=0.095, color=YELLOW)
        self.play(FadeIn(birth_pt, scale=1.4), run_time=0.5)

        self.at("infancy")
        lbl_inf = T("infancy", 22, GREY).move_to([P.pt(0.95, 0.0)[0], -2.86, 0.0])
        self.play(
            FadeIn(lbl_inf),
            u.animate(rate_func=linear).set_value(U_PEAK_FRONTAL),
            run_time=2.4,
        )

        self.at("half again")
        peak_lbl = T("peak ≈ 1.5 × adult", 26, YELLOW).move_to(P.pt(U_PEAK_FRONTAL, 1.72))
        self.play(FadeIn(peak_lbl, shift=UP * 0.1), run_time=0.6)

        self.at("declined")
        lbl_child = T("childhood", 22, GREY).move_to([P.pt(3.40, 0.0)[0], -2.86, 0.0])
        lbl_adol = T("adolescence", 22, GREY).move_to([P.pt(5.85, 0.0)[0], -2.86, 0.0])
        self.play(
            FadeIn(lbl_child),
            u.animate(rate_func=linear).set_value(U_10YR),
            run_time=1.35,
        )
        self.play(
            FadeIn(lbl_adol),
            u.animate(rate_func=linear).set_value(U_20YR),
            run_time=1.25,
        )
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        P, adult = make_age_plot()
        h_tag = T("Huttenlocher, 1979", 30, TEXT).move_to([3.0, 3.22, 0])
        curve = P.curve(frontal_density, x0=U_BIRTH, x1=U_20YR, color=YELLOW, width=5.8)
        peak_lbl = T("peak ≈ 1.5 × adult", 26, YELLOW).move_to(P.pt(U_PEAK_FRONTAL, 1.72))
        u = ValueTracker(U_10YR)
        scrubber = make_scrubber(P, u)
        dot = P.dot(lambda: u.get_value(), lambda: frontal_density(u.get_value()), color=YELLOW, ring=TEXT, radius=0.115)
        s_tag = scope_tag("schematic")

        grow = ValueTracker(window_scale_for_age(U_10YR))
        base_win = make_cortex_network(
            center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7,
            n_neurons=14, reserve_top_left=True, growing_frac=0.95,
            flash_scale_fn=lambda: grow.get_value(),
        )
        soma_offs = [s.get_center() - WIN_CENTER for s in base_win.somas]
        early_pts = [(l.get_start() - WIN_CENTER, l.get_end() - WIN_CENTER) for l in base_win.early_lines]
        esyn_offs = [d.get_center() - WIN_CENTER for d in base_win.early_syns]
        xsyn_offs = [d.get_center() - WIN_CENTER for d in base_win.extra_syns[:6]]

        def _mk_win():
            sc = grow.get_value()
            fr = RoundedRectangle(
                corner_radius=0.22, width=WIN_BASE_W * sc, height=WIN_BASE_H * sc,
                stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.70
            ).move_to(WIN_CENTER)
            g = VGroup(fr)
            for a, b in early_pts:
                g.add(Line(WIN_CENTER + a * sc, WIN_CENTER + b * sc, color=YELLOW, stroke_width=3.6, stroke_opacity=0.85))
            for o in soma_offs:
                g.add(Dot(WIN_CENTER + o * sc, radius=0.115, color=YELLOW, fill_opacity=0.95))
            for o in esyn_offs + xsyn_offs:
                g.add(Dot(WIN_CENTER + o * sc, radius=0.068, color=YELLOW, fill_opacity=0.95))
            return g

        dyn_win = always_redraw(_mk_win)
        fc_lbl = T("frontal cortex", 24, TEXT).move_to(
            [WIN_CENTER[0] - WIN_BASE_W * 0.50 + 1.25, WIN_CENTER[1] + WIN_BASE_H * 0.50 - 0.38, 0.0]
        )
        cube = make_counting_cube(WIN_CENTER + np.array([0.25, -0.22, 0.0]), side=1.25)
        self.add(dyn_win, base_win.flash_dots, cube, fc_lbl, P, adult, curve, peak_lbl, dot, scrubber, h_tag, s_tag)

        self.at("keeps growing")
        self.play(grow.animate.set_value(1.08), run_time=1.3)

        self.at("falling density")
        q = question_card("Does falling density prove loss?", y=3.22, color=TEXT, size=34, max_w=11.5)
        self.play(FadeOut(h_tag, run_time=0.25), FadeIn(q, shift=DOWN * 0.1, run_time=0.5))
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Does falling density prove loss?"
    CARD = {"y": 3.22, "color": TEXT, "size": 34, "max_w": 11.5}
    RING_AT = (4.10, -3.12, 0)
    SECONDS = 4.5

    def backdrop(self):
        P, adult = make_age_plot()
        curve = P.curve(frontal_density, x0=U_BIRTH, x1=U_20YR, color=YELLOW, width=5.8)
        peak_lbl = T("peak ≈ 1.5 × adult", 26, YELLOW).move_to(P.pt(U_PEAK_FRONTAL, 1.72))
        u = ValueTracker(U_10YR)
        scrubber = make_scrubber(P, u)
        dot = P.dot(lambda: u.get_value(), lambda: frontal_density(u.get_value()), color=YELLOW, ring=TEXT, radius=0.115)

        sc = 1.08
        base_win = make_cortex_network(
            center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7,
            n_neurons=14, reserve_top_left=True, growing_frac=0.95,
            flash_scale_fn=lambda: sc,
        )
        fr = RoundedRectangle(
            corner_radius=0.22, width=WIN_BASE_W * sc, height=WIN_BASE_H * sc,
            stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.70
        ).move_to(WIN_CENTER)
        pulse(fr, base=3.2, amp=1.4, speed=2.6)
        win_body = VGroup(fr)
        for l in base_win.early_lines:
            win_body.add(Line(WIN_CENTER + (l.get_start() - WIN_CENTER) * sc,
                              WIN_CENTER + (l.get_end() - WIN_CENTER) * sc,
                              color=YELLOW, stroke_width=3.6, stroke_opacity=0.85))
        for s in base_win.somas:
            win_body.add(Dot(WIN_CENTER + (s.get_center() - WIN_CENTER) * sc, radius=0.115, color=YELLOW, fill_opacity=0.95))
        for d in list(base_win.early_syns) + list(base_win.extra_syns[:6]):
            win_body.add(Dot(WIN_CENTER + (d.get_center() - WIN_CENTER) * sc, radius=0.068, color=YELLOW, fill_opacity=0.95))

        fc_lbl = T("frontal cortex", 24, TEXT).move_to(
            [WIN_CENTER[0] - WIN_BASE_W * 0.50 + 1.25, WIN_CENTER[1] + WIN_BASE_H * 0.50 - 0.38, 0.0]
        )
        cube = make_counting_cube(WIN_CENTER + np.array([0.25, -0.22, 0.0]), side=1.25)
        return VGroup(win_body, base_win.flash_dots, cube, fc_lbl, P, adult, curve, peak_lbl, dot, scrubber, scope_tag("schematic"))


class S11Answer(SpokenScene):
    def construct(self):
        s_tag = scope_tag("schematic")
        self.add(s_tag)

        lc = np.array([-3.25, 0.22, 0.0])
        rc = np.array([3.25, 0.22, 0.0])
        box_w, box_h = 5.4, 4.5

        # Exact geometry so BOTH cubes start at 12 and end at 6:
        # cube_side = 1.44 (half = 0.72)
        cube_side = 1.44
        half = cube_side / 2.0
        # 6 core dots: |x|,|y| <= 0.40 -> stay inside even at sc = 1.42
        core_offs = np.array([
            [-0.36, 0.32, 0], [0.05, 0.38, 0], [0.38, 0.14, 0],
            [-0.32, -0.28, 0], [0.10, -0.34, 0], [-0.04, 0.04, 0],
        ])
        # 6 perimeter inner dots: max(|x|,|y|) = 0.58 -> inside 0.72 at sc=1.0, outside 0.72 at sc=1.40 (0.58*1.4=0.81)
        perim_offs = np.array([
            [-0.58, 0.50, 0], [0.08, 0.58, 0], [0.58, 0.45, 0],
            [-0.58, -0.45, 0], [0.58, -0.48, 0], [0.04, -0.58, 0],
        ])
        # 8 far outer dots: max(|x|,|y|) >= 1.00 -> always outside 0.72, inside box even at sc=1.40
        outer_offs = np.array([
            [-1.30, 0.92, 0], [1.22, 0.98, 0], [-1.35, -0.90, 0], [1.28, -0.92, 0],
            [-1.12, 0.12, 0], [1.14, 0.20, 0], [0.06, 1.06, 0], [-0.14, -1.06, 0],
        ])
        all_offs = np.vstack([core_offs, perim_offs, outer_offs])

        # Left panel: starts compact (0.72 * box), stretches to 1.0 * box as sc goes 1.0 -> 1.40
        stretch = ValueTracker(1.0)

        def _mk_left():
            sc = stretch.get_value()
            frac = (sc - 1.0) / 0.40
            fr = RoundedRectangle(
                corner_radius=0.2,
                width=box_w * (0.76 + 0.24 * frac),
                height=box_h * (0.76 + 0.24 * frac),
                stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.70,
            ).move_to(lc)
            g = VGroup(fr)
            for off in all_offs:
                g.add(Dot(lc + off * sc, radius=0.08, color=YELLOW, fill_opacity=0.95))
            return g

        left_win = always_redraw(_mk_left)
        left_cube = make_counting_cube(lc, side=cube_side)

        # Right panel: full enlarged size from start, loses the 6 perim_offs dots
        right_frame = RoundedRectangle(
            corner_radius=0.2, width=box_w, height=box_h,
            stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.70,
        ).move_to(rc)
        right_keep_offs = np.vstack([core_offs, outer_offs])
        right_dots_keep = VGroup(*[Dot(rc + off, radius=0.08, color=YELLOW, fill_opacity=0.95) for off in right_keep_offs])
        right_dots_lose = VGroup(*[Dot(rc + off, radius=0.08, color=YELLOW, fill_opacity=0.95) for off in perim_offs])
        right_cube = make_counting_cube(rc, side=cube_side)

        # Live GREEN synaptic activity pulses on surviving core synapses in both windows
        pulse_t = ValueTracker(0.0)
        pulse_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(pulse_t)

        def _syn_flashes(center_pt, scale_fn):
            grp = VGroup()
            for k, off in enumerate(core_offs):
                ph = (pulse_t.get_value() * 1.1 + k * 0.33) % 1.0
                r = 0.09 + 0.08 * np.sin(np.pi * ph)
                op = 0.85 * np.sin(np.pi * ph)
                grp.add(Circle(radius=r, stroke_color=GREEN, stroke_width=2.5, stroke_opacity=op,
                               fill_color=GREEN, fill_opacity=0.25 * op).move_to(center_pt + off * scale_fn()))
            return grp

        left_flashes = always_redraw(lambda: _syn_flashes(lc, lambda: stretch.get_value()))
        right_flashes = always_redraw(lambda: _syn_flashes(rc, lambda: 1.0))

        def _count_left():
            sc = stretch.get_value()
            return sum(1 for off in all_offs if abs(off[0] * sc) < half and abs(off[1] * sc) < half)

        lost_flag = ValueTracker(0.0)
        left_tag = T("growth: same synapses", 26, TEXT).move_to([lc[0], -2.55, 0])
        right_tag = T("loss: fewer synapses", 26, TEXT).move_to([rc[0], -2.55, 0])
        left_cnt = always_redraw(lambda: M(f"in cube: {_count_left()}", 26, YELLOW).move_to([lc[0], -3.05, 0]))
        right_cnt = always_redraw(lambda: M(f"in cube: {12 - int(round(6 * lost_flag.get_value()))}", 26, YELLOW).move_to([rc[0], -3.05, 0]))

        self.at("Not by itself")
        self.play(
            FadeIn(left_win), FadeIn(left_cube), FadeIn(left_tag), FadeIn(left_cnt),
            FadeIn(right_frame), FadeIn(right_dots_keep), FadeIn(right_dots_lose), FadeIn(right_cube),
            FadeIn(right_tag), FadeIn(right_cnt),
            run_time=0.7,
        )
        self.add(left_flashes, right_flashes)

        self.at("tissue growth")
        self.play(stretch.animate.set_value(1.40), run_time=1.5)

        self.at("synapse loss")
        self.play(right_dots_lose.animate.set_color(RED), run_time=0.45)
        self.play(
            FadeOut(right_dots_lose, scale=0.3),
            lost_flag.animate.set_value(1.0),
            run_time=0.85,
        )

        self.at("what decided")
        q_mark = T("?", 52, RED, weight=BOLD).move_to([rc[0], 2.95, 0])
        self.play(FadeIn(q_mark, scale=1.2), run_time=0.6)

        self.at("follow the same")
        self.remove(left_flashes, right_flashes, pulse_t)
        self.play(
            FadeOut(VGroup(left_win, left_cube, left_tag, left_cnt,
                           right_frame, right_dots_keep, right_cube, right_tag, right_cnt, q_mark), run_time=0.5),
        )
        big_win = RoundedRectangle(
            corner_radius=0.22, width=10.8, height=5.1,
            stroke_color=GREY, stroke_width=3.2, fill_color=BG, fill_opacity=0.70
        ).move_to([0.0, 0.20, 0.0])
        spine_tag = T("same spines, over time", 30, YELLOW).move_to([0.0, 3.15, 0.0])

        spine_xs = np.linspace(-3.4, 3.4, 8)
        lost_idx = {2, 5}
        rows = VGroup()
        time_labels = ["time 1", "time 2", "time 3"]
        row_ys = [1.55, 0.20, -1.15]

        for r_i, (ry, t_lbl) in enumerate(zip(row_ys, time_labels)):
            dend = Line([-4.0, ry, 0], [4.0, ry, 0], color=YELLOW, stroke_width=6.5)
            tl = T(t_lbl, 24, GREY).next_to(dend, LEFT, buff=0.25)
            row_g = VGroup(dend, tl)
            for s_i, sx in enumerate(spine_xs):
                if r_i == 2 and s_i in lost_idx:
                    continue
                col = RED if (r_i == 1 and s_i in lost_idx) else YELLOW
                h_sp = 0.28 if (r_i == 1 and s_i in lost_idx) else 0.48
                stalk = Line([sx, ry, 0], [sx, ry + h_sp, 0], color=col, stroke_width=3.8)
                head = Dot([sx, ry + h_sp, 0], radius=0.095 if col == YELLOW else 0.07, color=col)
                row_g.add(stalk, head)
            rows.add(row_g)

        self.play(FadeIn(big_win), FadeIn(spine_tag), FadeIn(rows[0]), run_time=0.65)
        self.play(FadeIn(rows[1], shift=DOWN * 0.15), run_time=0.85)
        self.play(FadeIn(rows[2], shift=DOWN * 0.15), run_time=0.85)
        # GREEN firing sweep along surviving time-3 dendrite
        dend_flash = _make_flash_pulse(np.array([-4.0, -1.15, 0]), np.array([4.0, -1.15, 0]), 0.1, 0.65)
        self.add(dend_flash)
        self.finish()


class S12Regions(SpokenScene):
    def construct(self):
        P, adult = make_age_plot()
        ghost_frontal = P.curve(frontal_density, x0=U_BIRTH, x1=U_20YR, color=YELLOW, width=4.0, opacity=0.25)
        u = ValueTracker(U_10YR)
        scrubber = make_scrubber(P, u)
        s_tag = scope_tag("schematic")

        win = make_cortex_network(
            center=WIN_CENTER, w=WIN_BASE_W * 1.04, h=WIN_BASE_H * 1.04, seed=7,
            n_neurons=14, reserve_top_left=True, growing_frac=0.95
        )
        fc_lbl = T("frontal cortex", 24, TEXT).move_to(
            [win.frame.get_left()[0] + 1.25, win.frame.get_top()[1] - 0.38, 0.0]
        )
        self.add(win, fc_lbl, P, adult, ghost_frontal, scrubber, s_tag)

        self.at("timing")
        reg_head = T("timing differs by region", 30, TEXT).move_to([3.0, 3.22, 0])
        self.play(FadeIn(reg_head, shift=DOWN * 0.1), run_time=0.5)

        self.at("auditory")
        t3 = P.pt(U_3MO, 0.0)
        tick_3mo = Line(t3, t3 + UP * 0.12, color=MAGENTA, stroke_width=3.2)
        lbl_3mo = T("3 mo", 22, MAGENTA).next_to(tick_3mo, UP, buff=0.06)
        u_aud = ValueTracker(U_BIRTH)
        aud_live = P.live_curve(auditory_density, u_aud, color=MAGENTA, width=5.2, x0=U_BIRTH)
        # Placed cleanly above both auditory and ghost frontal curves, clear of y-axis
        aud_lbl = T("auditory", 26, MAGENTA).move_to(P.pt(1.05, 1.70))
        self.add(aud_live)
        self.play(
            FadeIn(tick_3mo), FadeIn(lbl_3mo), FadeIn(aud_lbl),
            u_aud.animate.set_value(4.5),
            run_time=1.8,
        )

        self.at("prefrontal")
        t15 = P.pt(U_15MO, 0.0)
        tick_15mo = Line(t15, t15 + UP * 0.12, color=CORAL, stroke_width=3.2)
        lbl_15mo = T("15 mo", 22, CORAL).next_to(tick_15mo, UP, buff=0.06)
        u_pre = ValueTracker(U_BIRTH)
        pre_live = P.live_curve(prefrontal_density, u_pre, color=CORAL, width=5.2, x0=U_BIRTH)
        # Placed cleanly above prefrontal & ghost frontal curves, clear of auditory and right-side bracket label
        pre_lbl = T("prefrontal", 26, CORAL).move_to(P.pt(3.15, 1.72))
        self.add(pre_live)
        self.play(
            FadeIn(tick_15mo), FadeIn(lbl_15mo), FadeIn(pre_lbl),
            u_pre.animate.set_value(U_20YR),
            run_time=1.9,
        )

        self.at("continuing")
        b_left = P.pt(U_20YR, 1.24)
        b_right = P.pt(U_30YR, 1.24)
        br_line = VGroup(
            Line(b_left + DOWN * 0.10, b_left, color=CORAL, stroke_width=2.8),
            Line(b_left, b_right, color=CORAL, stroke_width=2.8),
            Line(b_right, b_right + DOWN * 0.10, color=CORAL, stroke_width=2.8),
        )
        # Placed above scrubber top (1.56 in data units) and right of prefrontal label
        br_lbl = T("still losing spines", 24, CORAL).move_to(P.pt(6.25, 1.72))
        dim_syns = VGroup(*win.early_syns[:5])
        self.play(
            u_pre.animate.set_value(U_30YR),
            u.animate.set_value(U_25YR),
            FadeIn(br_line), FadeIn(br_lbl),
            dim_syns.animate.set_color(RED),
            run_time=1.8,
        )
        self.play(FadeOut(dim_syns, run_time=0.5))
        self.finish()


class S13Roadmap(SpokenScene):
    def construct(self):
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.95)
        s_tag = scope_tag("schematic")
        self.add(win, s_tag)

        bars = VGroup()
        for i in range(9):
            bx0 = -0.10 + i * 0.45
            bx1 = bx0 + 2.55
            by = 2.15 - i * 0.50
            bar = RoundedRectangle(
                corner_radius=0.08, width=bx1 - bx0, height=0.36,
                stroke_color=GREY, stroke_width=2.2, fill_color=GREY, fill_opacity=0.30
            ).move_to([(bx0 + bx1) / 2.0, by, 0.0])
            bars.add(bar)

        tag_top = T("overlapping steps, schematic", 26, GREY).move_to([3.0, 3.15, 0])
        lbl_1 = T("1 induction", 24, TEXT).next_to(bars[0], RIGHT, buff=0.18)
        lbl_9 = T("9 refinement", 24, TEXT).next_to(bars[8], LEFT, buff=0.18)

        self.at("longer build")
        self.play(FadeIn(tag_top), run_time=0.4)

        self.at("nine overlapping")
        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT * 0.12) for b in bars], lag_ratio=0.14),
            run_time=2.5,
        )
        self.play(FadeIn(lbl_1), FadeIn(lbl_9), run_time=0.5)

        self.at("naturally occurring")
        lbl_7 = T("7 neuron death", 24, TEAL).next_to(bars[6], LEFT, buff=0.18)
        echo_dots = VGroup(*[
            Dot(bars[6].get_center() + RIGHT * dx, radius=0.075, color=RED)
            for dx in (-0.38, 0.0, 0.38)
        ])
        self.play(
            bars[6].animate.set_stroke(TEAL, width=3.0).set_fill(TEAL, opacity=0.45),
            FadeIn(lbl_7),
            FadeIn(echo_dots),
            run_time=0.6,
        )
        self.play(FadeOut(echo_dots), run_time=0.45)

        self.at("activity")
        retract = win.silent_lines[0]
        self.add(retract)
        self.play(
            bars[8].animate.set_stroke(TEAL, width=3.0).set_fill(TEAL, opacity=0.45),
            lbl_9.animate.set_color(TEAL),
            retract.animate.set_color(RED).set_stroke(width=3.2),
            run_time=0.6,
        )
        self.play(FadeOut(retract), run_time=0.65)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        win = make_cortex_network(center=WIN_CENTER, w=WIN_BASE_W, h=WIN_BASE_H, seed=7, n_neurons=14, growing_frac=0.85)
        P, adult = make_age_plot()
        u = ValueTracker(U_BIRTH)
        scrubber = make_scrubber(P, u)
        live_curve = P.live_curve(frontal_density, u, color=YELLOW, width=5.8, x0=U_BIRTH)
        dot = P.dot(lambda: u.get_value(), lambda: frontal_density(u.get_value()), color=YELLOW, ring=TEXT, radius=0.115)
        s_tag = scope_tag("schematic")
        self.add(win, s_tag)

        self.at("not a board")
        ghost_pcb = make_circuit_board(center=np.array([3.1, 0.22, 0.0]), plugged=True).set_opacity(0.30)
        self.play(FadeIn(ghost_pcb, run_time=0.45))
        self.play(FadeOut(ghost_pcb, run_time=0.65))

        self.at("already at work")
        self.play(FadeIn(P), FadeIn(adult), run_time=0.55)
        self.add(live_curve, dot, scrubber)

        self.at("built with extra")
        self.play(
            Create(win.extra_lines, run_time=0.85),
            FadeIn(win.extra_syns, scale=0.7, run_time=0.85),
            u.animate(rate_func=linear).set_value(U_PEAK_FRONTAL),
            run_time=0.95,
        )

        self.at("trimmed as it runs")
        self.add(win.silent_lines, win.silent_syns)
        self.play(
            win.silent_lines.animate.set_color(RED),
            win.silent_syns.animate.set_color(RED),
            u.animate(rate_func=linear).set_value(U_20YR),
            run_time=1.0,
        )
        self.play(FadeOut(win.silent_lines), FadeOut(win.silent_syns), run_time=0.45)
        self.finish()


class S15End(EndCard):
    LINE = "A brain makes extra while it runs, then selects what stays."
