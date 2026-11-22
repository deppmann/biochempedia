"""Why Control Comes Before the Cut — STEMhop explainer animation.

COLOUR MAP (one colour per concept for the whole film):
- MEMBRANE        = "#94A3B8"   # plasma membrane, cell outline, apoptotic parcels
- CELL_FILL       = "#1B2638"   # translucent cytosol interior fill (distinguishes cell from BG)
- SUBSTRATE       = "#E2E8F0"   # target proteins, structural beams, DNA band
- PHOSPHATE       = "#83C167"   # reversible phosphate tag (kinase / phosphatase)
- INITIATOR_INACT = "#FB7185"   # inactive initiator procaspase-8 monomers
- ACTIVE_CASPASE  = "#EF4444"   # active paired caspase-8 initiator & active cut
- EXEC_INACT      = "#FDBA74"   # inactive linker-locked executioner caspase-3 dimers
- EXEC_ACTIVE     = "#F97316"   # unlocked active executioner cutters
- DNASE_COLOR     = "#2DD4BF"   # freed DNA-cutting enzyme (distinct from executioners)
- FAS_COLOR       = "#A78BFA"   # Fas ligand trimer & Fas death receptors
- FADD_COLOR      = "#38BDF8"   # FADD two-ended bridge & assembly platform
- NECROSIS_COLOR  = "#F5D547"   # contrasting necrotic cell swelling & spill
- GOLD            = "#D4A843"   # predict question, countdown ring, DISC bracket

ONE WORLD, CARRIED:
One schematic animal cell (cool slate-blue membrane, dark slate cytosol) carried across the film:
we zoom between the cytosol (reversible vs permanent cut, stored precursors, initiator vs
executioner designs, dilution & assembly platform), the upper plasma membrane (Fas/FADD/DISC),
and the full cell view (executioner demolition into membrane-wrapped parcels vs necrosis).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook: Stored precursors diffuse via seeded Langevin walk around the central trigger; then
  left phosphate cycles vertically on/off a bar (sin(t)) while right caspase shears a bar whose
  halves separate via computed dx(t).
- s02_irreversible_zymogens: Kinase/phosphatase cycle phosphate; then full cell fills frame as
  active cutter shears two bars and 8 inactive precursors diffuse via seeded Langevin walk.
- s03_two_designs: Precursors sort into upper diffusing initiators (circular-bounded walk) and
  lower linker-locked executioner dimer; a cut snaps the linker, opening active jaws to shear a target.
- s04_predict_q: Cytosol expands; 6 sparse initiators diffuse far apart via seeded Langevin walk
  while the question card enters below.
- s05_pause: PredictPause holds the question and ticks the 4.5 s countdown ring while the 6 sparse
  initiators continue their computed diffusion from s04's final state.
- s06_predict_reveal: All 6 monomers continue diffusing until two collide elastically and separate;
  an assembly platform rises and pulls 4 monomers into adjacent pairs that snap to vivid active red.
- s07_fas_fadd: Trimeric Fas ligand descends onto 3 membrane-diffusing Fas receptors, slides them
  into a cluster, docks 3 cyan FADD bridges, and captures diffusing procaspase-8 monomers.
- s08_disc_cuts: DISC bracket encloses the cluster while waiting executioner dimers diffuse below;
  paired caspase-8 flares active red, descends to clip the linkers, unlocking cutters to slice bars.
- s09_demolition_outcome: Active executioners travel across the cell to chop structural beams and
  free a DNA-chopping enzyme to cut DNA; left necrotic cell swells and bursts while right apoptotic
  cell shrinks into 4 intact parcels that a neighbouring cell engulfs.
"""

from bp_parts import *
from kx_manim import TAIL

# ---- Film-wide concept palette ----
MEMBRANE = "#94A3B8"
CELL_FILL = "#24344D"
SUBSTRATE = "#E2E8F0"
PHOSPHATE = "#83C167"
INITIATOR_INACT = "#FB7185"
ACTIVE_CASPASE = "#EF4444"
EXEC_INACT = "#FDBA74"
EXEC_ACTIVE = "#F97316"
DNASE_COLOR = "#2DD4BF"
FAS_COLOR = "#A78BFA"
FADD_COLOR = "#38BDF8"
NECROSIS_COLOR = "#F5D547"


# ------------------------------------------------------------------ computed diffusion helper
def simulate_brownian(
    n,
    bounds,
    duration,
    seed,
    speed=0.85,
    min_sep=0.95,
    init_pos=None,
    circle_bound=None,
    exclude_zone=None,
):
    """Compute deterministic 2D Langevin/Brownian paths inside `bounds = (xmin, xmax, ymin, ymax)`."""
    rng = np.random.default_rng(seed)
    xmin, xmax, ymin, ymax = bounds
    dt = 0.05
    steps = int(np.ceil(duration / dt)) + 2

    def valid(pt):
        if pt[0] < xmin or pt[0] > xmax or pt[1] < ymin or pt[1] > ymax:
            return False
        if circle_bound is not None:
            cx, cy, rmax = circle_bound
            if np.hypot(pt[0] - cx, pt[1] - cy) > rmax:
                return False
        if exclude_zone is not None:
            ex, ey, rexcl = exclude_zone
            if np.hypot(pt[0] - ex, pt[1] - ey) < rexcl:
                return False
        return True

    if init_pos is not None:
        pos = np.array(init_pos, dtype=float).copy()
    else:
        pos = np.zeros((n, 2), dtype=float)
        for i in range(n):
            cand = np.array([(xmin + xmax) / 2, (ymin + ymax) / 2])
            for _ in range(150):
                c = np.array([rng.uniform(xmin + 0.25, xmax - 0.25), rng.uniform(ymin + 0.25, ymax - 0.25)])
                if valid(c) and all(np.linalg.norm(c - pos[j]) >= min_sep for j in range(i)):
                    cand = c
                    break
            pos[i] = cand

    angles = rng.uniform(0, TAU, size=n)
    vel = np.column_stack([np.cos(angles), np.sin(angles)]) * speed
    traj = np.zeros((steps, n, 2), dtype=float)
    traj[0] = pos

    for k in range(1, steps):
        angles += rng.normal(0.0, 0.45 * np.sqrt(dt), size=n)
        vel = 0.85 * vel + 0.15 * np.column_stack([np.cos(angles), np.sin(angles)]) * speed
        for i in range(n):
            for j in range(i + 1, n):
                diff = pos[i] - pos[j]
                dist = np.linalg.norm(diff)
                if 1e-4 < dist < min_sep:
                    push = (diff / dist) * (min_sep - dist) * 2.4
                    vel[i] += push
                    vel[j] -= push
        norms = np.linalg.norm(vel, axis=1, keepdims=True)
        vel = np.where(norms > speed * 1.4, vel / np.maximum(norms, 1e-6) * speed * 1.4, vel)
        pos = pos + vel * dt

        for i in range(n):
            if pos[i, 0] < xmin:
                pos[i, 0] = xmin + (xmin - pos[i, 0])
                vel[i, 0] = abs(vel[i, 0])
            elif pos[i, 0] > xmax:
                pos[i, 0] = xmax - (pos[i, 0] - xmax)
                vel[i, 0] = -abs(vel[i, 0])
            if pos[i, 1] < ymin:
                pos[i, 1] = ymin + (ymin - pos[i, 1])
                vel[i, 1] = abs(vel[i, 1])
            elif pos[i, 1] > ymax:
                pos[i, 1] = ymax - (pos[i, 1] - ymax)
                vel[i, 1] = -abs(vel[i, 1])

            if circle_bound is not None:
                cx, cy, rmax = circle_bound
                d = pos[i] - np.array([cx, cy])
                dist = np.linalg.norm(d)
                if dist > rmax and dist > 1e-6:
                    nvec = d / dist
                    pos[i] = np.array([cx, cy]) + nvec * (rmax - (dist - rmax) * 0.5)
                    vn = np.dot(vel[i], nvec)
                    if vn > 0:
                        vel[i] -= 2.0 * vn * nvec

            if exclude_zone is not None:
                ex, ey, rexcl = exclude_zone
                d = pos[i] - np.array([ex, ey])
                dist = np.linalg.norm(d)
                if dist < rexcl and dist > 1e-6:
                    nvec = d / dist
                    pos[i] = np.array([ex, ey]) + nvec * rexcl
                    vn = np.dot(vel[i], nvec)
                    if vn < 0:
                        vel[i] -= 2.0 * vn * nvec

            angles[i] = np.arctan2(vel[i, 1], vel[i, 0])
        traj[k] = pos
    return traj, dt


def sample_traj(traj, dt, t):
    idx = np.clip(t / dt, 0.0, len(traj) - 1.0001)
    k = int(idx)
    frac = idx - k
    return traj[k] * (1.0 - frac) + traj[k + 1] * frac


# ------------------------------------------------------------------ reusable biological shapes
def make_cell_shell(radius=2.95, center=ORIGIN, color=MEMBRANE, stroke_width=5.5):
    outer = Circle(radius=radius, color=color, stroke_width=stroke_width,
                   fill_color=CELL_FILL, fill_opacity=0.88).move_to(center)
    inner = Circle(radius=radius - 0.14, color=color, stroke_width=2.2, stroke_opacity=0.65).move_to(center)
    return VGroup(outer, inner)


def make_initiator_monomer(active=False, locked=True, scale=1.0):
    col = ACTIVE_CASPASE if active else INITIATOR_INACT
    fill_op = 0.62 if active else 0.42
    if not active:
        body = RoundedRectangle(corner_radius=0.16 * scale, width=0.82 * scale, height=0.42 * scale,
                                stroke_color=col, stroke_width=3.2, fill_color=col, fill_opacity=fill_op)
        parts = [body]
        if locked:
            cap = Line(body.get_right() + LEFT * 0.17 * scale + UP * 0.15 * scale,
                       body.get_right() + LEFT * 0.17 * scale + DOWN * 0.15 * scale,
                       color=TEXT, stroke_width=2.8)
            parts.append(cap)
        return VGroup(*parts)
    pts = [
        [-0.44 * scale, -0.22 * scale, 0],
        [0.20 * scale, -0.22 * scale, 0],
        [0.48 * scale, -0.16 * scale, 0],
        [0.20 * scale, 0.0, 0],
        [0.48 * scale, 0.16 * scale, 0],
        [0.20 * scale, 0.22 * scale, 0],
        [-0.44 * scale, 0.22 * scale, 0],
    ]
    jaw = Polygon(*pts, color=col, stroke_width=3.4, fill_color=col, fill_opacity=fill_op)
    return VGroup(jaw)


def make_executioner_dimer(locked=True, scale=1.0):
    col = EXEC_INACT if locked else EXEC_ACTIVE
    fill_op = 0.45 if locked else 0.62
    sub_w, sub_h = 0.60 * scale, 0.50 * scale
    if locked:
        left_sub = RoundedRectangle(corner_radius=0.14 * scale, width=sub_w, height=sub_h,
                                    stroke_color=col, stroke_width=3.2, fill_color=col, fill_opacity=fill_op).shift(LEFT * 0.37 * scale)
        right_sub = RoundedRectangle(corner_radius=0.14 * scale, width=sub_w, height=sub_h,
                                     stroke_color=col, stroke_width=3.2, fill_color=col, fill_opacity=fill_op).shift(RIGHT * 0.37 * scale)
        linker = RoundedRectangle(corner_radius=0.05 * scale, width=0.62 * scale, height=0.15 * scale,
                                  stroke_color=GOLD, stroke_width=2.8, fill_color=BG, fill_opacity=0.95)
        return VGroup(left_sub, right_sub, linker)

    def open_sub(shift_x):
        pts = [
            [-0.30 * scale, -0.25 * scale, 0],
            [0.30 * scale, -0.25 * scale, 0],
            [0.30 * scale, 0.25 * scale, 0],
            [0.09 * scale, 0.25 * scale, 0],
            [0.0, 0.03 * scale, 0],
            [-0.09 * scale, 0.25 * scale, 0],
            [-0.30 * scale, 0.25 * scale, 0],
        ]
        return Polygon(*pts, color=col, stroke_width=3.4, fill_color=col, fill_opacity=fill_op).shift(RIGHT * shift_x)

    l_sub = open_sub(-0.38 * scale)
    r_sub = open_sub(0.38 * scale)
    stub_l = Line([-0.24 * scale, -0.04 * scale, 0], [-0.08 * scale, -0.04 * scale, 0], color=GOLD, stroke_width=3.2)
    stub_r = Line([0.08 * scale, -0.04 * scale, 0], [0.24 * scale, -0.04 * scale, 0], color=GOLD, stroke_width=3.2)
    return VGroup(l_sub, r_sub, stub_l, stub_r)


def make_protein_bar(width=2.6, height=0.38, color=SUBSTRATE):
    return RoundedRectangle(corner_radius=0.10, width=width, height=height,
                            stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.38)


def make_cut_halves(width=2.6, height=0.38, color=SUBSTRATE, center=ORIGIN):
    left_pts = [
        [-width / 2, -height / 2, 0],
        [-0.06, -height / 2, 0],
        [0.04, height / 2, 0],
        [-width / 2, height / 2, 0],
    ]
    right_pts = [
        [-0.04, -height / 2, 0],
        [width / 2, -height / 2, 0],
        [width / 2, height / 2, 0],
        [0.06, height / 2, 0],
    ]
    l_half = Polygon(*left_pts, color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.38).move_to(center + LEFT * (width * 0.25))
    r_half = Polygon(*right_pts, color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.38).move_to(center + RIGHT * (width * 0.25))
    return l_half, r_half


def make_phosphate_tag():
    dot = Circle(radius=0.28, color=PHOSPHATE, stroke_width=2.8, fill_color=PHOSPHATE, fill_opacity=0.95)
    txt = T("P", size=24, color=BG, weight=BOLD).move_to(dot)
    return VGroup(dot, txt)


def make_caspase_cutter(color=ACTIVE_CASPASE, scale=1.0):
    pts = [
        [-0.48 * scale, -0.34 * scale, 0],
        [0.44 * scale, -0.19 * scale, 0],
        [0.06 * scale, 0.0, 0],
        [0.44 * scale, 0.19 * scale, 0],
        [-0.48 * scale, 0.34 * scale, 0],
    ]
    return Polygon(*pts, color=color, stroke_width=3.4, fill_color=color, fill_opacity=0.60)


def make_membrane_band(y=1.1, x_left=-6.2, x_right=6.2):
    cyto_zone = Rectangle(width=x_right - x_left, height=y + 3.5, stroke_width=0,
                          fill_color=CELL_FILL, fill_opacity=0.55).move_to([(x_left + x_right) / 2, (y - 3.5) / 2, 0])
    top_line = Line([x_left, y + 0.12, 0], [x_right, y + 0.12, 0], color=MEMBRANE, stroke_width=4.5)
    bot_line = Line([x_left, y - 0.12, 0], [x_right, y - 0.12, 0], color=MEMBRANE, stroke_width=4.5)
    fill = Rectangle(width=x_right - x_left, height=0.24, stroke_width=0, fill_color=MEMBRANE, fill_opacity=0.26).move_to([(x_left + x_right) / 2, y, 0])
    return VGroup(cyto_zone, fill, top_line, bot_line)


def make_fas_receptor(x=0.0, y_mem=1.1):
    rod = RoundedRectangle(corner_radius=0.08, width=0.24, height=1.55,
                           stroke_color=FAS_COLOR, stroke_width=3.2, fill_color=FAS_COLOR, fill_opacity=0.45).move_to([x, y_mem - 0.05, 0])
    head = RoundedRectangle(corner_radius=0.06, width=0.40, height=0.22,
                            stroke_color=FAS_COLOR, stroke_width=3.0, fill_color=FAS_COLOR, fill_opacity=0.60).move_to([x, y_mem + 0.72, 0])
    tail = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.20,
                            stroke_color=FAS_COLOR, stroke_width=3.0, fill_color=FAS_COLOR, fill_opacity=0.60).move_to([x, y_mem - 0.82, 0])
    return VGroup(rod, head, tail)


def make_fas_ligand(x=0.0, y=2.65, spread=0.72):
    lobe_x = [-spread, 0.0, spread]
    lobes = VGroup(*[
        Circle(radius=0.24, color=FAS_COLOR, stroke_width=3.2, fill_color=FAS_COLOR, fill_opacity=0.68).move_to([x + lx, y - 0.25, 0])
        for lx in lobe_x
    ])
    bridge = RoundedRectangle(corner_radius=0.10, width=2 * spread + 0.54, height=0.28,
                              stroke_color=FAS_COLOR, stroke_width=3.2, fill_color=FAS_COLOR, fill_opacity=0.50).move_to([x, y + 0.08, 0])
    return VGroup(bridge, lobes)


def make_fadd_bridge(x=0.0, y=-0.25):
    shaft = RoundedRectangle(corner_radius=0.08, width=0.30, height=0.82,
                             stroke_color=FADD_COLOR, stroke_width=3.2, fill_color=FADD_COLOR, fill_opacity=0.48).move_to([x, y, 0])
    top_cup = RoundedRectangle(corner_radius=0.06, width=0.46, height=0.20,
                               stroke_color=FADD_COLOR, stroke_width=3.0, fill_color=FADD_COLOR, fill_opacity=0.62).move_to([x, y + 0.42, 0])
    bot_cup = RoundedRectangle(corner_radius=0.06, width=0.46, height=0.20,
                               stroke_color=FADD_COLOR, stroke_width=3.0, fill_color=FADD_COLOR, fill_opacity=0.62).move_to([x, y - 0.42, 0])
    return VGroup(shaft, top_cup, bot_cup)


# ------------------------------------------------------------------ world builders shared across scenes
def build_s04_monomers(seed=4, duration=29.0):
    bounds = (-5.3, 5.3, -1.4, 2.50)
    traj, dt = simulate_brownian(6, bounds, duration, seed=seed, speed=0.75, min_sep=1.55)
    return traj, dt, bounds


def build_disc_assembly(y_mem=1.25, center_x=0.0):
    mem = make_membrane_band(y=y_mem)
    xs = [center_x - 0.72, center_x, center_x + 0.72]
    receptors = VGroup(*[make_fas_receptor(x, y_mem) for x in xs])
    ligand = make_fas_ligand(x=center_x, y=y_mem + 1.15, spread=0.72)
    fadds = VGroup(*[make_fadd_bridge(x, y_mem - 1.38) for x in xs])
    casp8s = VGroup(*[
        make_initiator_monomer(active=False, locked=True, scale=0.90).rotate(-PI / 2).move_to([x, y_mem - 2.26, 0])
        for x in xs
    ])
    return mem, ligand, receptors, fadds, casp8s


# ================================================================== SCENES
class S00Title(TitleCard):
    LESSON = "Death Receptors, BCL-2 and Caspases"
    TITLE = "Why Control Comes Before the Cut"


class S01Hook(SpokenScene):
    def construct(self):
        # Beat 1: Schematic cell filling ~70% of frame height; stored locked precursors diffuse around "?"
        cell = make_cell_shell(radius=2.90, center=ORIGIN)
        bounds = (-2.15, 2.15, -2.15, 2.15)
        traj, dt = simulate_brownian(
            6, bounds, 9.0, seed=1, speed=0.65, min_sep=0.98,
            circle_bound=(0.0, 0.0, 2.15), exclude_zone=(0.0, 0.0, 1.25),
        )
        t_sim = ValueTracker(0.0)

        precursors = VGroup(*[
            make_initiator_monomer(active=False, locked=True, scale=0.92) if i % 2 == 0
            else make_executioner_dimer(locked=True, scale=0.84)
            for i in range(6)
        ])
        for i, mob in enumerate(precursors):
            mob.move_to([*sample_traj(traj, dt, 0.0)[i], 0])
            mob.add_updater(lambda m, idx=i: m.move_to([*sample_traj(traj, dt, t_sim.get_value())[idx], 0]))

        q_ring = Circle(radius=0.52, color=GOLD, stroke_width=3.8, fill_color=BG, fill_opacity=0.95)
        q_txt = T("?", size=34, color=GOLD, weight=BOLD).move_to(q_ring)
        q_badge = VGroup(q_ring, q_txt).move_to([0, 0, 0])
        cell_lbl = T("Ready within hours — no misfire?", size=30, color=TEXT).move_to([0, 3.28, 0])

        self.add(cell, precursors, q_badge, scope_tag("schematic", size=24, color=MEMBRANE))
        self.play(FadeIn(cell_lbl), run_time=0.35)

        # Drift inside the cell cleanly before "never trigger" (at 4.06 s)
        self.play(t_sim.animate.set_value(2.8), run_time=2.5, rate_func=linear)
        self.at("never trigger")
        self.play(
            q_ring.animate(rate_func=there_and_back).set_stroke(ACTIVE_CASPASE, width=7).scale(1.14),
            t_sim.animate.set_value(5.6),
            run_time=2.2,
            rate_func=linear,
        )

        # Beat 2: Zoom into cytosol comparison — left reversible phosphate vs right permanent caspase cut
        self.at("caspases")
        for m in precursors:
            m.clear_updaters()
        self.play(FadeOut(cell), FadeOut(precursors), FadeOut(q_badge), FadeOut(cell_lbl), run_time=0.45)

        tp = TwoPanel("Reversible tag", "Permanent cut", colors=(PHOSPHATE, ACTIVE_CASPASE),
                      top=3.05, bottom=-2.35, gap=0.45, width=12.4, size=30)
        tp.left_frame.set_fill(CELL_FILL, opacity=0.72)
        tp.right_frame.set_fill(CELL_FILL, opacity=0.72)
        self.play(FadeIn(tp), run_time=0.4)

        # Left side: protein bar + vertically cycling phosphate dot; reversible arrows to the right
        left_c = tp.area("left")[0]
        bar_l = make_protein_bar(width=2.9, height=0.40, color=SUBSTRATE).move_to(left_c + DOWN * 0.35)
        phos = make_phosphate_tag()
        phase = ValueTracker(0.0)

        def update_phos(m):
            lift = 0.5 * (1.0 - np.cos(phase.get_value()))  # 0 (bound) -> 1 (detached) -> 0
            m.move_to(bar_l.get_top() + UP * (0.34 + 1.05 * lift))

        phos.add_updater(update_phos)
        arrow_up = CurvedArrow(bar_l.get_top() + RIGHT * 0.72 + UP * 0.35,
                               bar_l.get_top() + RIGHT * 0.72 + UP * 1.35,
                               angle=0.5, color=PHOSPHATE, stroke_width=3.0)
        arrow_dn = CurvedArrow(bar_l.get_top() + LEFT * 0.72 + UP * 1.35,
                               bar_l.get_top() + LEFT * 0.72 + UP * 0.35,
                               angle=0.5, color=PHOSPHATE, stroke_width=3.0)
        lbl_l = T("Reversible", size=28, color=PHOSPHATE).next_to(bar_l, DOWN, buff=0.48)

        # Right side: protein bar + active caspase cutter
        right_c = tp.area("right")[0]
        bar_r = make_protein_bar(width=2.9, height=0.40, color=SUBSTRATE).move_to(right_c + DOWN * 0.35)
        cutter = make_caspase_cutter(color=ACTIVE_CASPASE, scale=1.05).move_to(right_c + UP * 1.15 + LEFT * 0.7)
        casp_lbl = T("Caspase", size=28, color=ACTIVE_CASPASE).next_to(cutter, UP, buff=0.18)

        self.play(FadeIn(bar_l), FadeIn(bar_r), FadeIn(cutter), FadeIn(casp_lbl), run_time=0.45)

        self.at("cut other proteins")
        self.play(
            cutter.animate.move_to(bar_r.get_center() + LEFT * 0.12),
            casp_lbl.animate.move_to([right_c[0], right_c[1] + 1.35, 0]),
            run_time=0.5,
        )
        l_half, r_half = make_cut_halves(width=2.9, height=0.40, color=SUBSTRATE, center=bar_r.get_center())
        self.remove(bar_r)
        self.add(l_half, r_half)

        sep = ValueTracker(0.05)
        l_base = l_half.get_center().copy()
        r_base = r_half.get_center().copy()
        l_half.add_updater(lambda m: m.move_to(l_base + LEFT * sep.get_value()))
        r_half.add_updater(lambda m: m.move_to(r_base + RIGHT * sep.get_value()))

        self.play(
            sep.animate.set_value(0.55),
            cutter.animate.move_to(right_c + UP * 0.45 + LEFT * 1.35),
            run_time=0.9,
        )

        self.at("Unlike a phosphate")
        self.add(phos)
        self.play(FadeIn(arrow_up), FadeIn(arrow_dn), FadeIn(lbl_l), run_time=0.25)
        self.play(phase.animate.set_value(PI), run_time=0.9, rate_func=linear)

        self.at("no enzyme can rejoin")
        ret_arc = ArcBetweenPoints(r_half.get_top() + LEFT * 0.1 + UP * 0.14,
                                   l_half.get_top() + RIGHT * 0.1 + UP * 0.14,
                                   angle=0.8, color=ACTIVE_CASPASE, stroke_width=3.2)
        cross_x = VGroup(
            Line([-0.22, -0.22, 0], [0.22, 0.22, 0], color=ACTIVE_CASPASE, stroke_width=4.2),
            Line([-0.22, 0.22, 0], [0.22, -0.22, 0], color=ACTIVE_CASPASE, stroke_width=4.2),
        ).move_to(ret_arc.get_top() + DOWN * 0.05)
        lbl_r = T("Cannot rejoin", size=28, color=ACTIVE_CASPASE).move_to([right_c[0], lbl_l.get_center()[1], 0])

        self.play(FadeIn(lbl_r), run_time=0.25)
        self.play(
            Create(ret_arc), Create(cross_x),
            phase.animate.set_value(TAU * 1.3),
            sep.animate.set_value(0.82),
            run_time=1.8,
            rate_func=linear,
        )
        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(phase.animate.set_value(TAU * 2.0), run_time=rem, rate_func=linear)
        self.finish()


class S02IrreversibleZymogens(SpokenScene):
    def construct(self):
        # Beat 1: Kinase adds phosphate, phosphatase takes it off (already visible at t=0)
        bg_box = RoundedRectangle(corner_radius=0.3, width=11.6, height=4.9,
                                  stroke_color=MEMBRANE, stroke_width=3.5,
                                  fill_color=CELL_FILL, fill_opacity=0.82).move_to([0, 0.2, 0])
        bar = make_protein_bar(width=4.0, height=0.48, color=SUBSTRATE).move_to([0, -0.45, 0])
        phos = make_phosphate_tag().move_to([-2.4, 1.4, 0])
        kin_chip = boxed_label("Kinase", PHOSPHATE, size=28).move_to([-3.2, 2.05, 0])
        phos_chip = boxed_label("Phosphatase", SUBSTRATE, size=28).move_to([3.2, 2.05, 0])
        title_l = T("Reversible tag", size=30, color=PHOSPHATE).move_to([0, 3.25, 0])

        self.add(bg_box, bar, kin_chip, phos_chip, phos, title_l, scope_tag("schematic", size=24, color=MEMBRANE))

        # Kinase adds P onto the bar
        self.play(phos.animate.move_to(bar.get_top() + UP * 0.34), run_time=1.3)

        self.at("phosphatase")
        self.play(phos.animate.move_to([2.4, 1.2, 0]), run_time=1.4)

        # Beat 2: Cut is permanent -> active caspase slices structural bars inside the cell
        self.at("cut is permanent")
        self.play(FadeOut(kin_chip), FadeOut(phos_chip), FadeOut(phos), FadeOut(bar), run_time=0.35)

        cell = make_cell_shell(radius=2.90, center=[0, -0.15, 0])
        title_c = T("Permanent cut", size=30, color=ACTIVE_CASPASE).move_to([0, 3.25, 0])
        bar_a = make_protein_bar(width=2.2, height=0.36, color=SUBSTRATE).move_to([-0.55, 0.45, 0])
        bar_b = make_protein_bar(width=2.2, height=0.36, color=SUBSTRATE).move_to([0.55, -0.75, 0])
        cutter = make_caspase_cutter(color=ACTIVE_CASPASE, scale=1.0).move_to([-1.65, 1.30, 0])

        self.play(
            ReplacementTransform(bg_box, cell),
            swap(title_l, title_c, run_time=0.45),
            FadeIn(bar_a), FadeIn(bar_b), FadeIn(cutter),
            run_time=0.55,
        )

        self.at("start cutting")
        self.play(cutter.animate.move_to(bar_a.get_center() + LEFT * 0.1), run_time=0.5)
        la, ra = make_cut_halves(2.2, 0.36, SUBSTRATE, bar_a.get_center())
        self.remove(bar_a)
        self.add(la, ra)
        self.play(
            la.animate.shift(LEFT * 0.32 + UP * 0.10),
            ra.animate.shift(RIGHT * 0.32 + DOWN * 0.10),
            cutter.animate.move_to(bar_b.get_center() + LEFT * 0.1),
            run_time=0.7,
        )
        lb, rb = make_cut_halves(2.2, 0.36, SUBSTRATE, bar_b.get_center())
        self.remove(bar_b)
        self.add(lb, rb)
        self.play(
            lb.animate.shift(LEFT * 0.32 + DOWN * 0.10),
            rb.animate.shift(RIGHT * 0.32 + UP * 0.10),
            cutter.animate.move_to([-1.55, -0.75, 0]),
            run_time=0.8,
        )

        # Beat 3: Stored inactive precursors waiting throughout the cytosol (bring in right at "To act fast")
        self.at("To act fast")
        bounds = (-2.15, 2.15, -2.30, 2.00)
        init_pos = [[0.0, -0.15]] + [
            [1.55 * np.cos(a), -0.15 + 1.55 * np.sin(a)]
            for a in np.linspace(0, TAU, 7, endpoint=False)
        ]
        traj, dt = simulate_brownian(8, bounds, 12.0, seed=2, speed=0.45, min_sep=1.18,
                                     init_pos=init_pos, circle_bound=(0.0, -0.15, 2.15))
        t_sim = ValueTracker(0.0)
        precursors = VGroup()
        for i in range(8):
            m = make_initiator_monomer(active=False, locked=True, scale=0.80) if i < 5 else make_executioner_dimer(locked=True, scale=0.66)
            m.move_to([*sample_traj(traj, dt, 0.0)[i], 0])
            precursors.add(m)

        lbl_prec = T("Inactive precursors", size=30, color=TEXT).move_to([0, 3.25, 0])
        self.play(
            FadeOut(la), FadeOut(ra), FadeOut(lb), FadeOut(rb), FadeOut(cutter),
            swap(title_c, lbl_prec, run_time=0.5),
            FadeIn(precursors, lag_ratio=0.04),
            run_time=0.8,
        )

        for i, mob in enumerate(precursors):
            mob.add_updater(lambda m, idx=i: m.move_to([*sample_traj(traj, dt, t_sim.get_value())[idx], 0]))

        rem = max(0.5, self.narration_s + TAIL - self.elapsed())
        self.play(t_sim.animate.set_value(rem), run_time=rem, rate_func=linear)
        self.finish()


class S03TwoDesigns(SpokenScene):
    def construct(self):
        # Carried cell interior split into Upper (Initiators) & Lower (Executioners)
        cell = make_cell_shell(radius=2.75, center=[0, 0.0, 0])
        bounds_up = (-2.05, 2.05, 0.52, 2.05)
        traj_up, dt_up = simulate_brownian(6, bounds_up, 27.0, seed=3, speed=0.55, min_sep=0.92,
                                           circle_bound=(0.0, 0.0, 2.02))
        t_sim = ValueTracker(0.0)

        inits = VGroup(*[make_initiator_monomer(active=False, locked=True, scale=0.84) for _ in range(6)])
        for i, m in enumerate(inits):
            m.move_to([*sample_traj(traj_up, dt_up, 0.0)[i], 0])

        execs = VGroup(*[make_executioner_dimer(locked=True, scale=0.80) for _ in range(3)])
        exec_pos = [[-1.50, -1.20, 0], [0.0, -1.30, 0], [1.50, -1.20, 0]]
        for m, p in zip(execs, exec_pos):
            m.move_to(p)

        self.add(cell, inits, execs, scope_tag("schematic", size=24, color=MEMBRANE))

        for i, mob in enumerate(inits):
            mob.add_updater(lambda m, idx=i: m.move_to([*sample_traj(traj_up, dt_up, t_sim.get_value())[idx], 0]))

        self.at("two designs")
        divider = DashedLine([-2.55, 0.05, 0], [2.55, 0.05, 0], color=MEMBRANE, stroke_width=2.2, dash_length=0.14)
        self.play(Create(divider), t_sim.animate.set_value(2.0), run_time=1.0, rate_func=linear)

        self.at("Initiator")
        lbl_init = T("Initiators (caspase-8): single chains", size=28, color=INITIATOR_INACT).move_to([0, 3.25, 0])
        self.play(FadeIn(lbl_init), run_time=0.25)
        self.play(t_sim.animate.set_value(4.5), run_time=1.0, rate_func=linear)

        self.at("float as")
        self.play(t_sim.animate.set_value(8.5), run_time=2.8, rate_func=linear)

        self.at("Executioner")
        lbl_exec = T("Executioners (caspase-3): dimers", size=28, color=EXEC_INACT).move_to([0, -3.25, 0])
        focal_dimer = make_executioner_dimer(locked=True, scale=1.42).move_to([-0.85, -1.20, 0])
        self.play(FadeIn(lbl_exec), run_time=0.25)
        self.play(
            FadeOut(execs[0]), FadeOut(execs[2]),
            ReplacementTransform(execs[1], focal_dimer),
            t_sim.animate.set_value(12.5),
            run_time=1.1,
        )

        self.at("those pairs")
        self.play(t_sim.animate.set_value(17.2), run_time=1.8, rate_func=linear)

        self.at("uncut linker")
        linker_box = SurroundingRectangle(focal_dimer[2], color=GOLD, buff=0.08, stroke_width=3.0)
        linker_lbl = fit_text("Uncut linker", max_w=2.4, size=28, color=GOLD).move_to([-4.6, -1.20, 0])
        arrow_l = Arrow(linker_lbl.get_right() + RIGHT * 0.1, focal_dimer[2].get_left() + LEFT * 0.12,
                        buff=0.0, color=GOLD, stroke_width=3.2, max_tip_length_to_length_ratio=0.14)
        self.play(FadeIn(linker_lbl), run_time=0.25)
        self.play(Create(linker_box), Create(arrow_l),
                  t_sim.animate.set_value(20.5), run_time=1.3, rate_func=linear)

        self.at("Only a cut")
        unlocked_dimer = make_executioner_dimer(locked=False, scale=1.2).move_to(focal_dimer.get_center())
        cut_flash = Line(focal_dimer[2].get_top() + UP * 0.35, focal_dimer[2].get_bottom() + DOWN * 0.35,
                         color=ACTIVE_CASPASE, stroke_width=6.0)
        target_bar = make_protein_bar(width=1.45, height=0.30, color=SUBSTRATE).move_to([0.85, -0.85, 0])
        unlock_lbl = fit_text("Cut unlocks cutter", max_w=3.3, size=28, color=EXEC_ACTIVE).move_to([-4.6, -1.20, 0])

        self.play(
            FadeOut(linker_box), FadeOut(arrow_l),
            swap(linker_lbl, unlock_lbl, run_time=0.4),
            Create(cut_flash),
            FadeIn(target_bar),
            t_sim.animate.set_value(23.5),
            run_time=0.5,
        )
        self.play(FadeOut(cut_flash), ReplacementTransform(focal_dimer, unlocked_dimer),
                  t_sim.animate.set_value(24.0), run_time=0.35)
        self.play(unlocked_dimer.animate.move_to(target_bar.get_center() + DOWN * 0.42),
                  t_sim.animate.set_value(24.8), run_time=0.65)
        l_h, r_h = make_cut_halves(1.45, 0.30, SUBSTRATE, target_bar.get_center())
        self.remove(target_bar)
        self.add(l_h, r_h)
        rem = max(0.3, self.narration_s + TAIL - self.elapsed())
        self.play(
            l_h.animate.shift(LEFT * 0.28 + UP * 0.20),
            r_h.animate.shift(RIGHT * 0.28 + UP * 0.20),
            unlocked_dimer.animate.shift(DOWN * 0.16),
            t_sim.animate.set_value(26.5),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        # Upper cytosol expands to fill 65% of frame; 6 sparse initiator monomers drift far apart
        traj, dt, _ = build_s04_monomers(seed=4, duration=29.0)
        t_sim = ValueTracker(0.0)

        cyto_frame = RoundedRectangle(corner_radius=0.35, width=12.0, height=4.85,
                                      stroke_color=MEMBRANE, stroke_width=4.2,
                                      fill_color=CELL_FILL, fill_opacity=0.86).move_to([0, 0.55, 0])
        zone_lbl = T("Cytosol: single initiator chains", size=28, color=INITIATOR_INACT).move_to([0, 3.25, 0])

        monomers = VGroup(*[make_initiator_monomer(active=False, locked=True, scale=1.0) for _ in range(6)])
        for i, m in enumerate(monomers):
            m.move_to([*sample_traj(traj, dt, 0.0)[i], 0])
            m.add_updater(lambda mob, idx=i: mob.move_to([*sample_traj(traj, dt, t_sim.get_value())[idx], 0]))

        self.add(cyto_frame, monomers, scope_tag("schematic", size=24, color=MEMBRANE))
        self.play(FadeIn(zone_lbl), run_time=0.25)
        self.play(t_sim.animate.set_value(1.0), run_time=0.7, rate_func=linear)

        self.at("two initiator")
        pair_lbl = T("Need to pair up to switch on", size=28, color=GOLD).move_to([0, -2.35, 0])
        self.play(FadeIn(pair_lbl), run_time=0.25)
        self.play(t_sim.animate.set_value(5.0), run_time=2.3, rate_func=linear)

        self.at("healthy cell")
        self.play(FadeOut(pair_lbl), run_time=0.25)
        self.play(t_sim.animate.set_value(13.2), run_time=4.6, rate_func=linear)

        self.at("Pause and")
        q = question_card("Why don't floating initiators pair up on their own?",
                          y=BOTTOM_Y + 0.1, color=GOLD, size=30, max_w=10.2)
        self.play(FadeIn(q.question), run_time=0.25)
        self.play(t_sim.animate.set_value(15.2), run_time=0.6, rate_func=linear)

        rem = max(0.1, self.narration_s + TAIL - self.elapsed())
        self.play(t_sim.animate.set_value(18.0), run_time=rem, rate_func=linear)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Why don't floating initiators pair up on their own?"
    OPTIONS = ()
    CARD = {"y": BOTTOM_Y + 0.1, "color": GOLD, "size": 30, "max_w": 10.2}
    RING_AT = (5.85, -2.55, 0)
    SECONDS = 4.5

    def backdrop(self):
        traj, dt, _ = build_s04_monomers(seed=4, duration=29.0)
        self._t_sim = ValueTracker(18.0)

        cyto_frame = RoundedRectangle(corner_radius=0.35, width=12.0, height=4.85,
                                      stroke_color=MEMBRANE, stroke_width=4.2,
                                      fill_color=CELL_FILL, fill_opacity=0.86).move_to([0, 0.55, 0])
        zone_lbl = T("Cytosol: single initiator chains", size=28, color=INITIATOR_INACT).move_to([0, 3.25, 0])

        monomers = VGroup(*[make_initiator_monomer(active=False, locked=True, scale=1.0) for _ in range(6)])
        for i, m in enumerate(monomers):
            m.move_to([*sample_traj(traj, dt, 18.0)[i], 0])
            m.add_updater(lambda mob, idx=i: mob.move_to([*sample_traj(traj, dt, self._t_sim.get_value())[idx], 0]))

        self.add(scope_tag("schematic", size=24, color=MEMBRANE))
        return VGroup(cyto_frame, zone_lbl, monomers)

    def construct(self):
        self.add(self.backdrop())
        self.add(question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD))
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run, self._t_sim.animate(run_time=self.SECONDS, rate_func=linear).set_value(22.5))
        self.finish()


class S06PredictReveal(SpokenScene):
    def construct(self):
        # Continue seamlessly from s05 end (t=22.5 -> 27.2)
        traj, dt, _ = build_s04_monomers(seed=4, duration=29.0)
        t_sim = ValueTracker(22.5)

        cyto_frame = RoundedRectangle(corner_radius=0.35, width=12.0, height=4.85,
                                      stroke_color=MEMBRANE, stroke_width=4.2,
                                      fill_color=CELL_FILL, fill_opacity=0.86).move_to([0, 0.55, 0])
        zone_lbl = T("Too dilute to hold together", size=28, color=INITIATOR_INACT).move_to([0, 3.25, 0])
        monomers = VGroup(*[make_initiator_monomer(active=False, locked=True, scale=1.0) for _ in range(6)])
        for i, m in enumerate(monomers):
            m.move_to([*sample_traj(traj, dt, 22.5)[i], 0])
            m.add_updater(lambda mob, idx=i: mob.move_to([*sample_traj(traj, dt, t_sim.get_value())[idx], 0]))

        self.add(cyto_frame, monomers, scope_tag("schematic", size=24, color=MEMBRANE))
        self.play(FadeIn(zone_lbl), run_time=0.25)
        self.play(t_sim.animate.set_value(26.5), run_time=3.7, rate_func=linear)

        # Beat 1: Random bump & elastic separation
        self.at("Random bumps")
        monomers[0].clear_updaters()
        monomers[1].clear_updaters()
        p_meet = np.array([0.0, 0.65, 0.0])
        self.play(
            monomers[0].animate.move_to(p_meet + LEFT * 0.44),
            monomers[1].animate.move_to(p_meet + RIGHT * 0.44),
            t_sim.animate.set_value(27.5),
            run_time=0.85,
        )
        bump_ring = Circle(radius=0.60, color=TEXT, stroke_width=2.8).move_to(p_meet)
        self.play(FadeIn(bump_ring, run_time=0.15))
        self.play(
            FadeOut(bump_ring, run_time=0.2),
            monomers[0].animate.move_to([-2.4, 1.45, 0]),
            monomers[1].animate.move_to([2.4, 1.45, 0]),
            t_sim.animate.set_value(28.8),
            run_time=1.3,
        )

        # Beat 2: Assembly platform rises and packs 4 copies side by side
        self.at("assembly platform")
        for m in monomers:
            m.clear_updaters()
        rack_body = RoundedRectangle(corner_radius=0.16, width=5.8, height=0.58,
                                     stroke_color=FADD_COLOR, stroke_width=3.5,
                                     fill_color=FADD_COLOR, fill_opacity=0.35).move_to([0, -0.40, 0])
        slot_xs = [-1.95, -0.95, 0.95, 1.95]
        slots = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.68, height=0.24,
                             stroke_color=FADD_COLOR, stroke_width=2.8,
                             fill_color=BG, fill_opacity=0.92).move_to([sx, -0.08, 0])
            for sx in slot_xs
        ])
        rack_lbl = T("Assembly platform", size=28, color=FADD_COLOR).next_to(rack_body, DOWN, buff=0.26)
        platform = VGroup(rack_body, slots, rack_lbl)
        plat_lbl_top = T("Assembly platform packs copies side by side", size=28, color=FADD_COLOR).move_to([0, 3.25, 0])

        # Move free monomers 4, 5 smoothly into top band before platform rises so they never cross rack_lbl
        self.play(
            swap(zone_lbl, plat_lbl_top, run_time=0.45),
            monomers[4].animate.move_to([-3.6, 2.25, 0]),
            monomers[5].animate.move_to([3.6, 2.25, 0]),
            FadeIn(platform, shift=UP * 0.25),
            run_time=1.0,
        )

        self.at("side by side")
        target_slots = [np.array([sx, 0.42, 0.0]) for sx in slot_xs]
        self.play(
            *[monomers[i].animate.rotate(PI / 2).move_to(target_slots[i]) for i in range(4)],
            run_time=1.3,
        )

        # Beat 3: Crowded pairs snap together and activate (rose -> vivid red)
        self.at("pair up")
        active_pairs = VGroup()
        for i_a, i_b in ((0, 1), (2, 3)):
            cx = (slot_xs[i_a] + slot_xs[i_b]) / 2
            a_act = make_initiator_monomer(active=True, locked=False, scale=1.0).rotate(PI / 2).move_to([cx - 0.25, 0.44, 0])
            b_act = make_initiator_monomer(active=True, locked=False, scale=1.0).rotate(PI / 2).move_to([cx + 0.25, 0.44, 0])
            active_pairs.add(a_act, b_act)

        glow_l = Circle(radius=0.72, color=ACTIVE_CASPASE, stroke_width=3.2, fill_color=ACTIVE_CASPASE, fill_opacity=0.18).move_to([-1.45, 0.44, 0])
        glow_r = Circle(radius=0.72, color=ACTIVE_CASPASE, stroke_width=3.2, fill_color=ACTIVE_CASPASE, fill_opacity=0.18).move_to([1.45, 0.44, 0])
        act_lbl = T("Paired & active", size=28, color=ACTIVE_CASPASE).move_to([0, 1.50, 0])

        self.play(
            *[ReplacementTransform(monomers[i], active_pairs[i]) for i in range(4)],
            FadeIn(glow_l), FadeIn(glow_r), FadeIn(act_lbl, run_time=0.4),
            run_time=0.95,
        )

        # Beat 4: Gathering, not a cut; keep remaining 2 free monomers diffusing in upper band (y >= 2.05)
        self.at("gathering")
        cap = caption("First step for initiators: gathering, not a cut.", size=28, color=TEXT)
        traj_free, dt_free = simulate_brownian(
            2, (-5.1, 5.1, 2.05, 2.55), 6.0, seed=6, speed=0.55, min_sep=1.2,
            init_pos=[monomers[4].get_center()[:2], monomers[5].get_center()[:2]],
        )
        t_free = ValueTracker(0.0)
        for idx, m in enumerate((monomers[4], monomers[5])):
            m.add_updater(lambda mob, k=idx: mob.move_to([*sample_traj(traj_free, dt_free, t_free.get_value())[k], 0]))

        self.play(FadeIn(cap, run_time=0.4))
        rem = max(0.3, self.narration_s + TAIL - self.elapsed())
        self.play(t_free.animate.set_value(min(5.8, rem)), run_time=rem, rate_func=linear)
        self.finish()


class S07FasFadd(SpokenScene):
    def construct(self):
        y_mem = 1.1
        mem = make_membrane_band(y=y_mem)
        outside_lbl = T("Outside cell", size=28, color=MEMBRANE).move_to([-4.6, 2.75, 0])
        cyto_lbl = T("Cytosol", size=28, color=MEMBRANE).move_to([-4.9, -0.45, 0])

        init_xs = [-2.5, 0.0, 2.5]
        receptors = VGroup(*[make_fas_receptor(x, y_mem) for x in init_xs])
        # Subtle lateral membrane diffusion until ligand clusters them
        lat_t = ValueTracker(0.0)
        for i, rec in enumerate(receptors):
            x0 = init_xs[i]
            rec.add_updater(lambda m, bx=x0, k=i: m.move_to([bx + 0.16 * np.sin(lat_t.get_value() * 1.4 + k * 2.1), y_mem - 0.05, 0]))

        fas_lbl = T("Fas", size=28, color=FAS_COLOR).move_to([3.35, y_mem + 0.55, 0])

        cyto_bounds = (-4.8, 4.8, -2.75, -2.10)
        traj_c, dt_c = simulate_brownian(4, cyto_bounds, 24.0, seed=7, speed=0.58, min_sep=1.4)
        t_c = ValueTracker(0.0)
        free_c8 = VGroup(*[make_initiator_monomer(active=False, locked=True, scale=0.92).rotate(-PI / 2) for _ in range(4)])
        for i, m in enumerate(free_c8):
            m.move_to([*sample_traj(traj_c, dt_c, 0.0)[i], 0])
            m.add_updater(lambda mob, idx=i: mob.move_to([*sample_traj(traj_c, dt_c, t_c.get_value())[idx], 0]))

        self.add(mem, outside_lbl, cyto_lbl, receptors, free_c8, scope_tag("schematic", size=24, color=MEMBRANE))

        self.at("outside the cell")
        self.play(t_c.animate.set_value(2.0), lat_t.animate.set_value(2.0), run_time=1.4, rate_func=linear)

        # Killer T cell presents 3-part Fas ligand
        self.at("killer")
        tcell_lbl = T("Killer T cell", size=28, color=TEXT).move_to([0, 3.36, 0])
        tcell_arc = Arc(radius=8.5, start_angle=-PI * 0.58, angle=PI * 0.16, color=MEMBRANE, stroke_width=3.8).move_to([0, 3.04, 0])
        ligand = make_fas_ligand(x=0.0, y=2.60, spread=0.95)
        lig_lbl = T("Fas ligand", size=28, color=FAS_COLOR).next_to(ligand, RIGHT, buff=0.28)
        self.play(FadeIn(tcell_lbl), FadeIn(tcell_arc), FadeIn(ligand), FadeIn(lig_lbl), run_time=0.3)
        self.play(t_c.animate.set_value(5.0), lat_t.animate.set_value(5.0), run_time=1.2, rate_func=linear)

        # Ligand binds Fas and slides receptors into a cluster
        self.at("binds")
        self.play(
            ligand.animate.move_to([0, y_mem + 1.02, 0]),
            lig_lbl.animate.move_to([2.45, y_mem + 1.15, 0]),
            FadeIn(fas_lbl),
            t_c.animate.set_value(8.8),
            lat_t.animate.set_value(8.8),
            run_time=1.8,
        )

        self.at("pulls several")
        for rec in receptors:
            rec.clear_updaters()
        clustered_xs = [-0.72, 0.0, 0.72]
        clustered_ligand = make_fas_ligand(x=0.0, y=y_mem + 1.15, spread=0.72)
        self.play(
            *[receptors[i].animate.move_to([clustered_xs[i], y_mem - 0.05, 0]) for i in range(3)],
            Transform(ligand, clustered_ligand),
            fas_lbl.animate.move_to([1.65, y_mem + 0.55, 0]),
            lig_lbl.animate.move_to([2.05, y_mem + 1.28, 0]),
            t_c.animate.set_value(12.8),
            run_time=2.0,
        )

        # Two-ended FADD bridges dock onto clustered receptor tails
        self.at("bridge protein")
        fadds = VGroup(*[make_fadd_bridge(x, y_mem - 1.38) for x in clustered_xs])
        fadds_start = fadds.copy().shift(DOWN * 0.65)
        fadd_lbl = T("FADD", size=28, color=FADD_COLOR).move_to([1.85, y_mem - 1.38, 0])
        self.play(FadeIn(fadds_start), run_time=0.25)
        self.play(t_c.animate.set_value(15.5), run_time=0.6, rate_func=linear)

        self.at("clustered receptor")
        self.play(Transform(fadds_start, fadds), FadeIn(fadd_lbl), t_c.animate.set_value(18.5), run_time=1.6)

        # FADD's other end grabs inactive procaspase-8
        self.at("grabs")
        for i in range(3):
            free_c8[i].clear_updaters()
        c8_lbl = T("Procaspase-8", size=28, color=INITIATOR_INACT).move_to([2.45, y_mem - 2.30, 0])
        self.play(
            *[free_c8[i].animate.move_to([clustered_xs[i], y_mem - 2.26, 0]) for i in range(3)],
            t_c.animate.set_value(21.5),
            run_time=1.5,
        )
        self.play(FadeIn(c8_lbl), run_time=0.25)
        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(t_c.animate.set_value(22.2), run_time=rem, rate_func=linear)
        self.finish()


class S08DiscCuts(SpokenScene):
    def construct(self):
        y_mem = 1.25
        mem, ligand, receptors, fadds, casp8s = build_disc_assembly(y_mem=y_mem, center_x=0.0)
        fas_lbl = T("Fas", size=28, color=FAS_COLOR).move_to([1.65, y_mem + 0.55, 0])
        fadd_lbl = T("FADD", size=28, color=FADD_COLOR).move_to([1.85, y_mem - 1.38, 0])
        c8_lbl = T("Procaspase-8", size=28, color=INITIATOR_INACT).move_to([2.45, y_mem - 2.26, 0])

        # Waiting executioner dimers gently drift in the lower cytosol until active caspase-8 arrives
        traj_ex, dt_ex = simulate_brownian(
            2, (-3.8, 3.8, -2.55, -2.08), 18.0, seed=8, speed=0.45, min_sep=2.8,
            init_pos=[[-2.35, -2.30], [2.35, -2.30]],
        )
        t_ex = ValueTracker(0.0)
        exec_l = make_executioner_dimer(locked=True, scale=1.08)
        exec_r = make_executioner_dimer(locked=True, scale=1.08)
        exec_l.move_to([*sample_traj(traj_ex, dt_ex, 0.0)[0], 0])
        exec_r.move_to([*sample_traj(traj_ex, dt_ex, 0.0)[1], 0])
        exec_l.add_updater(lambda m: m.move_to([*sample_traj(traj_ex, dt_ex, t_ex.get_value())[0], 0]))
        exec_r.add_updater(lambda m: m.move_to([*sample_traj(traj_ex, dt_ex, t_ex.get_value())[1], 0]))

        exec_lbl = T("Executioner dimers (locked)", size=28, color=EXEC_INACT).move_to([0, -3.25, 0])

        self.add(mem, ligand, receptors, fadds, casp8s, fas_lbl, fadd_lbl, c8_lbl,
                 exec_l, exec_r, exec_lbl, scope_tag("schematic", size=24, color=MEMBRANE))

        # Beat 1: Bracket encircles Fas ligand + Fas + FADD + Procaspase-8 as "DISC"
        self.at("one platform")
        disc_group = VGroup(ligand, receptors, fadds, casp8s)
        disc_box = SurroundingRectangle(disc_group, color=GOLD, buff=0.16, stroke_width=3.6, corner_radius=0.12)
        disc_lbl = T("DISC", size=32, color=GOLD, weight=BOLD).next_to(disc_box, LEFT, buff=0.28)
        self.play(t_ex.animate.set_value(2.5), run_time=2.5, rate_func=linear)

        self.at("DISC")
        self.play(FadeIn(disc_lbl), run_time=0.25)
        self.play(Create(disc_box), t_ex.animate.set_value(6.0), run_time=1.3, rate_func=linear)

        # Beat 2: Inside DISC, paired caspase-8 chains sit side by side, pair up, switch on; 3rd remains inactive
        self.at("side by side")
        self.play(
            casp8s[0].animate.shift(RIGHT * 0.28),
            casp8s[1].animate.shift(LEFT * 0.14),
            t_ex.animate.set_value(10.0),
            run_time=1.1,
        )

        self.at("pair up")
        act_c8_0 = make_initiator_monomer(active=True, locked=False, scale=0.90).rotate(-PI / 2).move_to(casp8s[0].get_center())
        act_c8_1 = make_initiator_monomer(active=True, locked=False, scale=0.90).rotate(-PI / 2).move_to(casp8s[1].get_center())
        c8_active_lbl = T("Active caspase-8", size=28, color=ACTIVE_CASPASE).move_to([2.95, y_mem - 2.26, 0])

        self.at("switch on")
        self.play(
            ReplacementTransform(casp8s[0], act_c8_0),
            ReplacementTransform(casp8s[1], act_c8_1),
            swap(c8_lbl, c8_active_lbl, run_time=0.45),
            t_ex.animate.set_value(12.5),
            run_time=0.9,
        )

        # Beat 3: No kinase or second messenger needed
        self.at("No kinase")
        no_kin_lbl = fit_text("No kinase or\n2nd messenger", max_w=3.8, size=28, color=TEXT).move_to([-3.85, -0.45, 0])
        self.play(FadeIn(no_kin_lbl), run_time=0.25)
        self.play(t_ex.animate.set_value(14.8), run_time=1.6, rate_func=linear)
        self.play(FadeOut(no_kin_lbl), run_time=0.25)
        self.play(t_ex.animate.set_value(16.2), run_time=0.7, rate_func=linear)

        # Beat 4: Active caspase-8 pair clips linkers on both executioner dimers, then retracts as cutters slice bars
        self.at("Active")
        exec_l.clear_updaters()
        exec_r.clear_updaters()
        c8_pair = VGroup(act_c8_0, act_c8_1)
        c8_active_lbl_l = T("Active caspase-8", size=28, color=ACTIVE_CASPASE).move_to([-4.1, -1.55, 0])
        self.play(
            exec_l.animate.move_to([-2.1, -2.30, 0]),
            exec_r.animate.move_to([2.1, -2.30, 0]),
            c8_pair.animate.move_to([-2.1, -1.55, 0]),
            swap(c8_active_lbl, c8_active_lbl_l, run_time=0.85),
            run_time=0.85,
        )

        self.at("clips the linker")
        flash_l = Line(exec_l[2].get_top() + UP * 0.25, exec_l[2].get_bottom() + DOWN * 0.25, color=ACTIVE_CASPASE, stroke_width=6.0)
        self.play(Create(flash_l), FadeOut(c8_active_lbl_l), run_time=0.25)
        self.play(FadeOut(flash_l), c8_pair.animate.move_to([2.1, -1.55, 0]), run_time=0.70)
        flash_r = Line(exec_r[2].get_top() + UP * 0.25, exec_r[2].get_bottom() + DOWN * 0.25, color=ACTIVE_CASPASE, stroke_width=6.0)
        self.play(Create(flash_r), run_time=0.25)

        self.at("unlocking them")
        un_l = make_executioner_dimer(locked=False, scale=1.08).move_to(exec_l.get_center())
        un_r = make_executioner_dimer(locked=False, scale=1.08).move_to(exec_r.get_center())
        exec_act_lbl = T("Active executioners", size=28, color=EXEC_ACTIVE).move_to([0, -3.25, 0])
        bar_l = make_protein_bar(width=1.7, height=0.28, color=SUBSTRATE).move_to([-4.5, -2.15, 0])
        bar_r = make_protein_bar(width=1.7, height=0.28, color=SUBSTRATE).move_to([4.5, -2.15, 0])

        self.play(
            FadeOut(flash_r),
            FadeOut(c8_pair, shift=UP * 0.35),
            ReplacementTransform(exec_l, un_l),
            ReplacementTransform(exec_r, un_r),
            swap(exec_lbl, exec_act_lbl, run_time=0.45),
            FadeIn(bar_l), FadeIn(bar_r),
            run_time=0.65,
        )
        self.play(
            un_l.animate.move_to(bar_l.get_center() + DOWN * 0.42),
            un_r.animate.move_to(bar_r.get_center() + DOWN * 0.42),
            run_time=0.65,
        )
        lh1, rh1 = make_cut_halves(1.7, 0.28, SUBSTRATE, bar_l.get_center())
        lh2, rh2 = make_cut_halves(1.7, 0.28, SUBSTRATE, bar_r.get_center())
        self.remove(bar_l, bar_r)
        self.add(lh1, rh1, lh2, rh2)
        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(
            lh1.animate.shift(LEFT * 0.28 + UP * 0.16),
            rh1.animate.shift(RIGHT * 0.28 + UP * 0.16),
            lh2.animate.shift(LEFT * 0.28 + UP * 0.16),
            rh2.animate.shift(RIGHT * 0.28 + UP * 0.16),
            un_l.animate.shift(DOWN * 0.22),
            un_r.animate.shift(DOWN * 0.22),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


class S09DemolitionOutcome(SpokenScene):
    def construct(self):
        # Beat 1: Whole cell — active executioners cut structural beams & free DNA-chopping enzyme to chop DNA
        cell = make_cell_shell(radius=2.60, center=ORIGIN)
        beam1 = make_protein_bar(width=2.3, height=0.26, color=SUBSTRATE).move_to([0.0, 1.30, 0])
        beam2 = make_protein_bar(width=2.3, height=0.26, color=SUBSTRATE).move_to([0.0, -1.30, 0])
        dna_band = RoundedRectangle(corner_radius=0.10, width=1.8, height=0.42,
                                    stroke_color=SUBSTRATE, stroke_width=3.2,
                                    fill_color=SUBSTRATE, fill_opacity=0.35).move_to([0.75, 0.0, 0])
        dna_lbl = T("DNA", size=28, color=SUBSTRATE, weight=BOLD).move_to(dna_band)
        dnase = make_caspase_cutter(color=DNASE_COLOR, scale=0.68).move_to([-1.62, 0.0, 0])
        inhibitor = RoundedRectangle(corner_radius=0.04, width=0.16, height=0.42,
                                     stroke_color=GOLD, stroke_width=2.8,
                                     fill_color=BG, fill_opacity=0.95).move_to([-1.14, 0.0, 0])
        cutter1 = make_executioner_dimer(locked=False, scale=0.86).move_to([-1.25, 0.72, 0])
        cutter2 = make_executioner_dimer(locked=False, scale=0.86).move_to([1.25, -0.72, 0])
        top_lbl = T("Executioners dismantle cell", size=30, color=EXEC_ACTIVE).move_to([0, 3.25, 0])

        self.add(cell, beam1, beam2, dna_band, dna_lbl, dnase, inhibitor, cutter1, cutter2, top_lbl,
                 scope_tag("schematic", size=24, color=MEMBRANE))

        self.at("structural proteins")
        self.play(
            cutter1.animate.move_to(beam1.get_center() + DOWN * 0.30),
            cutter2.animate.move_to(beam2.get_center() + DOWN * 0.30),
            run_time=0.75,
        )
        b1l, b1r = make_cut_halves(2.3, 0.26, SUBSTRATE, beam1.get_center())
        b2l, b2r = make_cut_halves(2.3, 0.26, SUBSTRATE, beam2.get_center())
        self.remove(beam1, beam2)
        self.add(b1l, b1r, b2l, b2r)
        self.play(
            b1l.animate.shift(LEFT * 0.35 + UP * 0.10),
            b1r.animate.shift(RIGHT * 0.35 + DOWN * 0.10),
            b2l.animate.shift(LEFT * 0.35 + DOWN * 0.10),
            b2r.animate.shift(RIGHT * 0.35 + UP * 0.10),
            cutter1.animate.move_to([-1.14, 0.72, 0]),
            cutter2.animate.move_to([1.25, -0.68, 0]),
            run_time=0.75,
        )

        self.at("free an enzyme")
        self.play(cutter1.animate.move_to(inhibitor.get_center() + UP * 0.48), run_time=0.35)
        cut_inh = Line(inhibitor.get_left() + LEFT * 0.08, inhibitor.get_right() + RIGHT * 0.08,
                       color=ACTIVE_CASPASE, stroke_width=5.0)
        self.play(Create(cut_inh), run_time=0.15)
        dnase_lbl = T("DNase", size=28, color=DNASE_COLOR).next_to(dnase, DOWN, buff=0.20)
        self.play(
            FadeOut(cut_inh),
            FadeOut(inhibitor, shift=DOWN * 0.35),
            cutter1.animate.move_to([-1.40, 0.72, 0]),
            run_time=0.35,
        )
        self.play(FadeIn(dnase_lbl), run_time=0.20)

        self.at("chops")
        dnase_lbl_cut = T("DNase", size=28, color=DNASE_COLOR).move_to([-0.18, 0.52, 0])
        self.play(FadeOut(dna_lbl, run_time=0.2), FadeOut(dnase_lbl, run_time=0.2))
        self.play(dnase.animate.rotate(-PI / 2).move_to([-0.45, 0.52, 0]), run_time=0.22)
        self.play(
            dnase.animate.move_to(dna_band.get_center() + UP * 0.52),
            run_time=0.28,
        )
        dna_l, dna_r = make_cut_halves(1.8, 0.42, SUBSTRATE, dna_band.get_center())
        self.remove(dna_band)
        self.add(dna_l, dna_r)
        self.play(
            dna_l.animate.shift(LEFT * 0.25 + DOWN * 0.08),
            dna_r.animate.shift(RIGHT * 0.35 + UP * 0.08),
            dnase.animate.shift(UP * 0.08),
            FadeIn(dnase_lbl_cut, run_time=0.18),
            run_time=0.70,
        )

        # Beat 2: Left Necrosis (swells & bursts) vs Right Apoptosis (shrinks into intact parcels)
        self.at("injured necrotic")
        self.play(FadeOut(dnase_lbl_cut, run_time=0.22))
        apop_grp = VGroup(cell, b1l, b1r, b2l, b2r, dna_l, dna_r, cutter1, cutter2, dnase)
        nec_cell = Circle(radius=1.35, color=NECROSIS_COLOR, stroke_width=4.2,
                          fill_color=NECROSIS_COLOR, fill_opacity=0.22).move_to([-3.2, 0.1, 0])
        nec_debris = VGroup(*[
            Dot(radius=0.10, color=NECROSIS_COLOR).move_to([-3.2 + dx, 0.1 + dy, 0])
            for dx, dy in [(-0.5, 0.4), (0.5, 0.3), (-0.4, -0.4), (0.6, -0.3), (0.0, 0.6), (0.0, -0.55)]
        ])
        nec_lbl = T("Necrosis: swell & spill", size=28, color=NECROSIS_COLOR).move_to([-3.2, 2.75, 0])
        apop_lbl = T("Apoptosis: intact parcels", size=28, color=MEMBRANE).move_to([2.6, 2.75, 0])

        self.play(
            FadeOut(top_lbl, run_time=0.35),
            apop_grp.animate.scale(0.82).move_to([2.6, 0.05, 0]),
            FadeIn(nec_cell, run_time=0.45), FadeIn(nec_debris, run_time=0.45),
            FadeIn(nec_lbl, run_time=0.4), FadeIn(apop_lbl, run_time=0.4),
            run_time=1.0,
        )

        self.at("swells and bursts")
        nec_burst = DashedVMobject(Circle(radius=2.05, color=NECROSIS_COLOR, stroke_width=4.2).move_to([-3.2, 0.1, 0]), num_dashes=18)
        spill_vecs = [LEFT * 1.4 + UP * 0.9, RIGHT * 1.3 + UP * 0.8, LEFT * 1.2 + DOWN * 1.0,
                      RIGHT * 1.4 + DOWN * 0.9, UP * 1.5, DOWN * 1.5]
        self.play(
            ReplacementTransform(nec_cell, nec_burst),
            *[nec_debris[i].animate.shift(spill_vecs[i]) for i in range(6)],
            run_time=1.5,
        )

        self.at("shrinks")
        self.play(apop_grp.animate.scale(0.58), run_time=1.2)

        self.at("wrapped parcels")
        parcel_offsets = [[-0.65, 0.55, 0], [0.65, 0.55, 0], [-0.55, -0.60, 0], [0.60, -0.60, 0]]
        parcels = VGroup()
        for off in parcel_offsets:
            c = np.array([2.6, 0.05, 0]) + np.array(off)
            mem_p = Circle(radius=0.46, color=MEMBRANE, stroke_width=3.8, fill_color=CELL_FILL, fill_opacity=0.92).move_to(c)
            frag = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.18, color=SUBSTRATE, stroke_width=2.2,
                                    fill_color=SUBSTRATE, fill_opacity=0.45).move_to(c)
            parcels.add(VGroup(mem_p, frag))

        self.play(ReplacementTransform(apop_grp, parcels), run_time=1.1)

        # Beat 3: Neighbouring cell swallows parcels; no inflammation
        self.at("neighbors swallow")
        self.play(FadeOut(nec_burst), FadeOut(nec_debris), FadeOut(nec_lbl), run_time=0.45)
        neighbour = RoundedRectangle(corner_radius=1.2, width=2.9, height=3.7,
                                     stroke_color=MEMBRANE, stroke_width=4.2,
                                     fill_color=CELL_FILL, fill_opacity=0.88).move_to([5.4, 0.0, 0])
        neigh_lbl = T("Neighbour cell", size=28, color=TEXT).move_to([4.5, 2.25, 0])
        self.play(
            apop_lbl.animate.move_to([-2.4, 2.75, 0]),
            parcels.animate.shift(LEFT * 1.2),
            FadeIn(neighbour, shift=LEFT * 0.8),
            neighbour.animate.move_to([4.5, 0.0, 0]),
            run_time=1.0,
        )
        self.bring_to_front(parcels)
        self.play(FadeIn(neigh_lbl), run_time=0.25)

        self.at("no inflammation")
        no_inf = T("No inflammation", size=28, color=TEXT).move_to([-2.4, 2.05, 0])
        self.play(FadeIn(no_inf), run_time=0.25)
        self.play(
            parcels[1].animate.move_to([3.95, 0.45, 0]),
            parcels[3].animate.move_to([4.05, -0.55, 0]),
            run_time=1.4,
        )

        # Beat 4: Final tie-back to the guiding idea
        self.at("Because cuts")
        cap = caption("Gathering initiators on a platform holds the trigger.", size=28, color=TEXT)
        self.play(FadeIn(cap), run_time=0.25)
        rem = max(0.3, self.narration_s + TAIL - self.elapsed())
        self.play(
            parcels[0].animate.shift(RIGHT * 1.4),
            parcels[2].animate.shift(RIGHT * 1.4),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


class S10End(EndCard):
    LINE = "Caspase cuts cannot be undone, so assembly platforms control initiator activation."
