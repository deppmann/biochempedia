"""Beating Diffusion: The Signaling Endosome — animation for Long-Distance Signaling in Neurons.

COLOUR MAP (one colour per concept for the whole film):
    MEMBRANE_COL   (#E8EAF0, slate-white)   Plasma membrane outer leaflet / soma & axon outline
    MEMBRANE_INNER (#A7B2C6, silver-slate)  Plasma membrane cytoplasmic leaflet (inner side)
    NUCLEUS_COL    (#9C8EFF / #6450DB)      Nucleus & CREB gene switch (indigo-violet)
    NGF_COL        (#F2C14E, gold)          Nerve growth factor (NGF) survival signal
    TRKA_COL       (#3FB8C0, teal)          TrkA receptor (extracellular + transmembrane)
    KINASE_COL     (#F06292, magenta-pink)  TrkA active kinase domain & phosphorylation
    MT_COL         (#58C4DD, steel-blue)    Axonal microtubules (- end at soma, + end at tip)
    KINESIN_COL    (#E58E43, muted orange)  Cargo kinesin motor (walks toward + end)
    DYNEIN_COL     (#83C167, emerald-green) Cytoplasmic dynein + dynactin & motor transport
    DIFF_COL       (#FC6255, red-amber)     Slow diffusion / 58-day failure timescale
    STRUCT_COL     (#8B93A1, grey)          Campenot sealed barrier, brackets, axes, scope tags

CARRIED WORLD:
    One sympathetic neuron (cell body + indigo nucleus on the left, long thin axon across
    the center, branched axon tip touching an NGF-releasing target organ on the right).
    Math scenes hold this neuron in the upper third and compute diffusion/transport below;
    the endocytosis scenes zoom into the right axon tip plasma membrane; the transport scenes
    zoom along the axon interior showing polarized microtubules and motors carrying the exact
    same signaling endosome home to the nucleus.

SCENE CHANGES (what moves / changes and what computes it):
    s00_title               Standard TitleCard (silent 2.0 s).
    s01_hook                NGF particles arrive at axon tip and perform a computed 1D random walk
                            (rng seed 7, D = 10 um^2/s) stalling near the tip while span & scale
                            brackets measure the ~30 um cell body vs cm-long axon.
    s02_diffusion_math      Computed 2D random walk inside a 30 um cell-body zoom inset (sigma =
                            sqrt(2*D*dt)) synchronized with a live t = 0..45 s counter and 45 s bar
                            while t = x^2 / 2D populates step by step.
    s03_centimeter_fails    Transforms smoothly from s02 end state as x stretches to 1 cm (10,000 um);
                            1D random-walk NGF dots jitter near the tip making negligible leftward
                            progress while the red-amber diffusion bar grows across the frame to
                            5,000,000 s (~58 days) and the indigo nucleus dims.
    s04_campenot            Campenot barrier seals the dish into two chambers; NGF fills only the
                            right axon chamber while a computed retrograde pulse crosses beneath
                            the barrier into the left cell body, illuminating the nucleus (CREB active).
    s05_endocytosis_predict Retrograde arrow travels tip-to-soma, then zooms into the tip membrane:
                            NGF binds teal TrkA, and a C1-smooth circular-flask membrane pocket folds
                            inward while TrkA kinase tails stay in the cytoplasm; freezes before
                            pinch with question_card.
    s06_pause               Standard PredictPause holding the pinched membrane pocket and question
                            while the 4.5 s countdown ring empties.
    s07_topology_reveal     Smooth flask neck pinches shut into a free signaling endosome (outer
                            white leaflet visibly becomes inner lumen lining), trapping gold NGF
                            inside while magenta kinase tails phosphorylate partner blocks.
    s08_microtubules_motors Zooms out to axon interior with polarized steel-blue microtubules (- left,
                            + right); orange kinesin steps toward +, then emerald dynein + dynactin
                            latches onto the signaling endosome and walks steadily leftward toward -.
    s09_motor_math          One ValueTracker drives dynein + endosome from tip to soma over t = 0..10,000 s
                            at v = 1 um/s, synced with live t = x/v arithmetic, a 500x bar comparison
                            (58 days vs < 3 hr), and nuclear activation on arrival.
    s10_takeaway            Stream of active signaling endosomes hauled continuously leftward along
                            microtubules into the illuminated cell body beside the 58 days vs < 3 hr
                            comparison and 'leading model' hedge tag.
    s11_end                 Standard EndCard with the take-home line.
"""
from types import SimpleNamespace
from bp_parts import *

# ------------------------------------------------------------------ concept colour map
MEMBRANE_COL = TEXT          # #E8EAF0 warm slate-white
MEMBRANE_INNER = "#A7B2C6"   # cytoplasmic leaflet / inner outline
SOMA_FILL = "#212B3F"        # rich dark intracellular slate-blue (distinct from #0F1117 BG)
PANEL_FILL = "#20293D"       # framed computed-panel fill
NUCLEUS_STROKE = "#9C8EFF"
NUCLEUS_DIM = "#2E2660"
NUCLEUS_LIT = "#6450DB"
NGF_COL = "#F2C14E"          # gold survival signal
TRKA_COL = TEAL              # #3FB8C0 receptor
KINASE_COL = "#F06292"       # magenta-pink catalytic tail
MT_COL = BLUE                # #58C4DD steel-blue microtubule
KINESIN_COL = "#E58E43"      # muted orange outward motor
DYNEIN_COL = GREEN           # #83C167 emerald homeward motor
DIFF_COL = RED               # #FC6255 slow diffusion / 58-day bar
STRUCT_COL = GREY            # #8B93A1 barriers, axes, brackets, scope tags


# ------------------------------------------------------------------ shared world builders
def build_neuron(center_y=0.25, scale=1.0, nucleus_lit=0.65, include_organ=True, sx_offset=0.0):
    """Build the carried sympathetic neuron schematic spanning the frame width."""
    cy = center_y
    sx = -4.2 * scale + sx_offset
    soma_r = 0.96 * scale

    dendrites = VGroup()
    for ang, length, branch_ang in [
        (142 * DEGREES, 0.95 * scale, 22 * DEGREES),
        (178 * DEGREES, 1.02 * scale, -18 * DEGREES),
        (-142 * DEGREES, 0.95 * scale, -24 * DEGREES),
    ]:
        p0 = np.array([sx + soma_r * 0.88 * np.cos(ang), cy + soma_r * 0.88 * np.sin(ang), 0.0])
        p1 = p0 + length * 0.55 * np.array([np.cos(ang), np.sin(ang), 0.0])
        p2 = p1 + length * 0.50 * np.array([np.cos(ang + branch_ang), np.sin(ang + branch_ang), 0.0])
        p3 = p1 + length * 0.42 * np.array([np.cos(ang - branch_ang), np.sin(ang - branch_ang), 0.0])
        dendrites.add(
            Line(p0, p1, color=MEMBRANE_COL, stroke_width=4.0 * scale),
            Line(p1, p2, color=MEMBRANE_COL, stroke_width=2.8 * scale),
            Line(p1, p3, color=MEMBRANE_COL, stroke_width=2.8 * scale),
        )

    x_soma_right = sx + soma_r * 0.92
    x_tip_split = 3.55 * scale + sx_offset * 0.3
    axon_half = 0.17 * scale

    soma = Circle(radius=soma_r, color=MEMBRANE_COL, stroke_width=4.4 * scale,
                  fill_color=SOMA_FILL, fill_opacity=0.98).move_to([sx, cy, 0.0])
    nuc_fill = interpolate_color(ManimColor(NUCLEUS_DIM), ManimColor(NUCLEUS_LIT), nucleus_lit)
    nucleus = Circle(radius=0.47 * scale, color=NUCLEUS_STROKE, stroke_width=3.6 * scale,
                     fill_color=nuc_fill, fill_opacity=0.94).move_to([sx, cy, 0.0])

    axon_fill = Rectangle(
        width=(x_tip_split - x_soma_right),
        height=2 * axon_half,
        stroke_width=0,
        fill_color=SOMA_FILL,
        fill_opacity=0.98,
    ).move_to([(x_soma_right + x_tip_split) / 2, cy, 0.0])
    axon_top = Line([x_soma_right, cy + axon_half, 0.0], [x_tip_split, cy + axon_half, 0.0],
                    color=MEMBRANE_COL, stroke_width=4.0 * scale)
    axon_bot = Line([x_soma_right, cy - axon_half, 0.0], [x_tip_split, cy - axon_half, 0.0],
                    color=MEMBRANE_COL, stroke_width=4.0 * scale)

    tip_branches = VGroup()
    tip_ends = []
    for dy, y_off in [(0.72 * scale, axon_half), (0.0, 0.0), (-0.72 * scale, -axon_half)]:
        start = np.array([x_tip_split - 0.05 * scale, cy + y_off, 0.0])
        mid = np.array([x_tip_split + 0.50 * scale, cy + dy * 0.55, 0.0])
        end = np.array([x_tip_split + 1.00 * scale, cy + dy, 0.0])
        branch = VMobject(color=MEMBRANE_COL, stroke_width=3.6 * scale)
        branch.set_points_smoothly([start, mid, end])
        bouton = Dot(end, radius=0.12 * scale, color=MEMBRANE_COL, fill_opacity=0.45,
                     stroke_color=MEMBRANE_COL, stroke_width=2.8 * scale)
        tip_branches.add(branch, bouton)
        tip_ends.append(end)

    organ = VGroup()
    if include_organ:
        ox = 5.20 * scale
        organ_arc = RoundedRectangle(
            corner_radius=0.35 * scale,
            width=1.35 * scale,
            height=2.65 * scale,
            stroke_color=NGF_COL,
            stroke_width=3.4 * scale,
            fill_color=NGF_COL,
            fill_opacity=0.20,
        ).move_to([ox, cy, 0.0])
        organ.add(organ_arc)

    grp = VGroup(dendrites, axon_fill, soma, axon_top, axon_bot, tip_branches, nucleus, organ)
    return SimpleNamespace(
        group=grp,
        dendrites=dendrites,
        soma=soma,
        nucleus=nucleus,
        axon_top=axon_top,
        axon_bot=axon_bot,
        axon_fill=axon_fill,
        tip_branches=tip_branches,
        organ=organ,
        soma_center=np.array([sx, cy, 0.0]),
        soma_r=soma_r,
        axon_left=x_soma_right,
        axon_right=x_tip_split,
        axon_half=axon_half,
        tip_ends=tip_ends,
        tip_center=np.array([x_tip_split + 0.55 * scale, cy, 0.0]),
    )


def build_signaling_endosome(center=ORIGIN, radius=0.65):
    """Build the signaling endosome: outer silver-slate ring, inner bright outer-leaflet ring,
    teal TrkA facing lumen with gold NGF bound inside, magenta kinase tails outside."""
    c = np.array(center, dtype=float)
    outer_ring = Circle(radius=radius, color=MEMBRANE_INNER, stroke_width=3.8,
                        fill_color=SOMA_FILL, fill_opacity=0.96).move_to(c)
    inner_ring = Circle(radius=radius * 0.84, color=MEMBRANE_COL, stroke_width=4.8,
                        fill_color=BG, fill_opacity=0.94).move_to(c)

    receptors = VGroup()
    ngfs = VGroup()
    kinases = VGroup()
    for ang in [35 * DEGREES, 145 * DEGREES, -90 * DEGREES]:
        u = np.array([np.cos(ang), np.sin(ang), 0.0])
        p_in = c + u * (radius * 0.56)
        p_out = c + u * (radius * 1.12)
        bar = Line(p_in, p_out, color=TRKA_COL, stroke_width=max(5.0, radius * 10))
        cup = Arc(radius=radius * 0.14, start_angle=ang - PI / 2, angle=PI,
                  arc_center=p_in, color=TRKA_COL, stroke_width=max(3.8, radius * 7))
        receptors.add(bar, cup)

        ngf_pos = c + u * (radius * 0.38)
        ngf = Dot(ngf_pos, radius=max(0.06, radius * 0.17), color=NGF_COL)
        ngfs.add(ngf)

        k_end = c + u * (radius * 1.48)
        tail = Line(p_out, k_end, color=KINASE_COL, stroke_width=max(4.5, radius * 8))
        tip = Dot(k_end, radius=max(0.05, radius * 0.14), color=KINASE_COL)
        kinases.add(tail, tip)

    g = VGroup(outer_ring, inner_ring, receptors, ngfs, kinases)
    ns = SimpleNamespace(group=g, outer=outer_ring, inner=inner_ring,
                         receptors=receptors, ngfs=ngfs, kinases=kinases)
    return g, ns


def _pocket_points(phi, y_top=1.75, half_w=6.2):
    """C1-smooth tangent-matched double-arc omega pocket parameterized by phi in [0.02, 2.74].
    Guarantees zero neck cusps and zero self-intersections."""
    phi = float(np.clip(phi, 0.02, 2.74))
    r_lip = 0.42
    # Main bulb radius scales smoothly from very flat (large R_b) down to ~1.12 at deep pinch
    R_b = 2.75 / phi
    c_lip_x = (R_b + r_lip) * np.sin(phi)
    c_lip_y = y_top - r_lip
    c_bulb_y = c_lip_y + (R_b + r_lip) * np.cos(phi)

    # Left flat segment: [-half_w, -c_lip_x)
    n_flat = 16
    n_lip = 18
    n_cup = 72
    x_lf = np.linspace(-half_w, -c_lip_x, n_flat, endpoint=False)
    y_lf = np.full_like(x_lf, y_top)

    # Left lip arc: center (-c_lip_x, c_lip_y), angle from PI/2 down to PI/2 - phi
    th_l = np.linspace(PI / 2, PI / 2 - phi, n_lip, endpoint=False)
    x_ll = -c_lip_x + r_lip * np.cos(th_l)
    y_ll = c_lip_y + r_lip * np.sin(th_l)

    # Main bulb arc: center (0, c_bulb_y), alpha from -phi to +phi
    alphas = np.linspace(-phi, phi, n_cup, endpoint=False)
    x_cup = R_b * np.sin(alphas)
    y_cup = c_bulb_y - R_b * np.cos(alphas)

    # Right lip arc: center (+c_lip_x, c_lip_y), angle from PI/2 + phi down to PI/2
    th_r = np.linspace(PI / 2 + phi, PI / 2, n_lip, endpoint=False)
    x_rl = c_lip_x + r_lip * np.cos(th_r)
    y_rl = c_lip_y + r_lip * np.sin(th_r)

    # Right flat segment: [+c_lip_x, +half_w]
    x_rf = np.linspace(c_lip_x, half_w, n_flat)
    y_rf = np.full_like(x_rf, y_top)

    x = np.concatenate([x_lf, x_ll, x_cup, x_rl, x_rf])
    y = np.concatenate([y_lf, y_ll, y_cup, y_rl, y_rf])

    # Exact tangent and cytoplasm-facing normal
    dx = np.gradient(x)
    dy = np.gradient(y)
    ds = np.hypot(dx, dy) + 1e-9
    tx, ty = dx / ds, dy / ds
    nx, ny = ty, -tx

    thick = 0.14
    outer = np.column_stack([x, y, np.zeros_like(x)])
    inner = np.column_stack([x + thick * nx, y + thick * ny, np.zeros_like(x)])
    normals = np.column_stack([nx, ny, np.zeros_like(x)])
    cup_start = n_flat + n_lip
    return outer, inner, normals, (cup_start, n_cup)


def build_pinched_membrane(phi=2.45, y_top=1.75, ngf_bound=1.0, show_labels=True):
    """Build zoomed axon tip membrane pocket with bound NGF, teal TrkA, and magenta kinase tails."""
    outer_pts, inner_pts, normals, (cup_start, n_cup) = _pocket_points(phi, y_top=y_top)

    cyto_poly = Polygon(
        *outer_pts,
        np.array([outer_pts[-1, 0], -2.55, 0.0]),
        np.array([outer_pts[0, 0], -2.55, 0.0]),
        stroke_width=0,
        fill_color=SOMA_FILL,
        fill_opacity=0.95,
    )
    outer_curve = VMobject(color=MEMBRANE_COL, stroke_width=6.0).set_points_as_corners(outer_pts)
    inner_curve = VMobject(color=MEMBRANE_INNER, stroke_width=3.8).set_points_as_corners(inner_pts)

    idx_list = [cup_start + int(n_cup * 0.30), cup_start + int(n_cup * 0.70)]
    receptors = VGroup()
    ngfs = VGroup()
    kinases = VGroup()
    for idx in idx_list:
        p = outer_pts[idx]
        n = normals[idx]
        p_ext = p - n * 0.44
        p_mem_in = p + n * 0.24
        bar = Line(p_ext, p_mem_in, color=TRKA_COL, stroke_width=10)
        ang = np.arctan2(-n[1], -n[0])
        cup = Arc(radius=0.15, start_angle=ang - PI / 2, angle=PI, arc_center=p_ext,
                  color=TRKA_COL, stroke_width=5.5)
        receptors.add(bar, cup)

        ngf_pos = p_ext - n * (0.12 + (1.0 - ngf_bound) * 0.85)
        ngfs.add(Dot(ngf_pos, radius=0.145, color=NGF_COL))

        k_end = p_mem_in + n * 0.50
        tail = Line(p_mem_in, k_end, color=KINASE_COL, stroke_width=8.0)
        knob = Dot(k_end, radius=0.115, color=KINASE_COL)
        kinases.add(tail, knob)

    g = VGroup(cyto_poly, inner_curve, outer_curve, receptors, ngfs, kinases)
    if show_labels:
        l_out = T("Outside (extracellular)", 28, MEMBRANE_COL).move_to([-4.0, 2.58, 0])
        l_cyto = T("Cytoplasm (inside)", 28, MEMBRANE_COL).move_to([-4.2, -1.85, 0])
        l_trka = T("TrkA", 28, TRKA_COL).move_to([3.7, 2.48, 0])
        l_ngf = T("NGF", 28, NGF_COL).move_to([2.1, 2.48, 0])
        l_kin = T("active kinase", 28, KINASE_COL).move_to([3.8, -1.85, 0])
        g.add(l_out, l_cyto, l_trka, l_ngf, l_kin)
    return g


def build_pinched_backdrop():
    """Exact backdrop shared by the end of S05 and the silent S06Pause."""
    g = build_pinched_membrane(phi=0.7, y_top=1.75, ngf_bound=1.0, show_labels=True)
    tag = T("schematic", 24, STRUCT_COL).move_to([FRAME_X - 0.2 - 0.75, FRAME_Y - 0.35, 0])
    return VGroup(g, tag)


def build_kinesin(pos, phase=0.0, scale=1.0):
    """Cargo kinesin schematic stepping toward + end (rightward)."""
    p = np.array(pos, dtype=float)
    step = 0.14 * scale * np.sin(phase)
    lift_a = max(0.0, 0.11 * scale * np.cos(phase))
    lift_b = max(0.0, -0.11 * scale * np.cos(phase))
    foot_a = np.array([p[0] - step, p[1] + lift_a, 0.0])
    foot_b = np.array([p[0] + step, p[1] + lift_b, 0.0])
    hip = np.array([p[0], p[1] + 0.42 * scale, 0.0])
    cargo = np.array([p[0], p[1] + 0.76 * scale, 0.0])
    legs = VGroup(
        Line(foot_a, hip, color=KINESIN_COL, stroke_width=5.5 * scale),
        Line(foot_b, hip, color=KINESIN_COL, stroke_width=5.5 * scale),
        Line(hip, cargo, color=KINESIN_COL, stroke_width=5.0 * scale),
    )
    heads = VGroup(
        Dot(foot_a, radius=0.09 * scale, color=KINESIN_COL),
        Dot(foot_b, radius=0.09 * scale, color=KINESIN_COL),
        Circle(radius=0.20 * scale, color=KINESIN_COL, stroke_width=3.8 * scale,
               fill_color=KINESIN_COL, fill_opacity=0.35).move_to(cargo),
    )
    return VGroup(legs, heads)


def build_dynein_with_endosome(track_y, x_pos, phase=0.0, scale=1.0, endosome_radius=0.52):
    """Cytoplasmic dynein + dynactin collar hauling the signaling endosome along the track."""
    step = 0.14 * scale * np.sin(phase)
    lift_a = max(0.0, 0.11 * scale * np.cos(phase))
    lift_b = max(0.0, -0.11 * scale * np.cos(phase))
    foot_a = np.array([x_pos - step, track_y + 0.06 + lift_a, 0.0])
    foot_b = np.array([x_pos + step, track_y + 0.06 + lift_b, 0.0])
    hub = np.array([x_pos, track_y + 0.48 * scale, 0.0])

    legs = VGroup(
        Line(foot_a, hub, color=DYNEIN_COL, stroke_width=6.0 * scale),
        Line(foot_b, hub, color=DYNEIN_COL, stroke_width=6.0 * scale),
    )
    feet = VGroup(
        Circle(radius=0.11 * scale, color=DYNEIN_COL, stroke_width=3.8 * scale,
               fill_color=BG, fill_opacity=1.0).move_to(foot_a),
        Circle(radius=0.11 * scale, color=DYNEIN_COL, stroke_width=3.8 * scale,
               fill_color=BG, fill_opacity=1.0).move_to(foot_b),
    )
    endo_center = np.array([x_pos, track_y + 0.68 * scale + endosome_radius * 1.15, 0.0])
    collar = Arc(radius=endosome_radius * 1.18, start_angle=-145 * DEGREES, angle=110 * DEGREES,
                 arc_center=endo_center, color=DYNEIN_COL, stroke_width=7.0 * scale)
    stalk = Line(hub, endo_center + DOWN * (endosome_radius * 1.18), color=DYNEIN_COL, stroke_width=6.0 * scale)
    endo_g, _ = build_signaling_endosome(endo_center, radius=endosome_radius)
    endo_g.rotate(60 * DEGREES, about_point=endo_center)
    return VGroup(legs, feet, stalk, collar, endo_g)


def build_mt_track(x0, x1, y, stroke=6.5, n_chevrons=6):
    """Build a polarized steel-blue microtubule double-rail track with minus-end chevrons."""
    rail_a = Line([x0, y + 0.06, 0.0], [x1, y + 0.06, 0.0], color=MT_COL, stroke_width=stroke * 0.65)
    rail_b = Line([x0, y - 0.06, 0.0], [x1, y - 0.06, 0.0], color=MT_COL, stroke_width=stroke * 0.65)
    signs = VGroup()
    xs = np.linspace(x0 + 1.0, x1 - 1.0, n_chevrons)
    for xi in xs:
        ch = VGroup(
            Line([xi + 0.14, y + 0.14, 0.0], [xi - 0.12, y, 0.0], color=MT_COL, stroke_width=3.5),
            Line([xi + 0.14, y - 0.14, 0.0], [xi - 0.12, y, 0.0], color=MT_COL, stroke_width=3.5),
        )
        signs.add(ch)
    return VGroup(rail_a, rail_b, signs)


def _s02_diffusion_traj():
    """Compute the 2D random-walk NGF trajectory inside the 30 um cell body (rng seed 7)."""
    rng = np.random.default_rng(7)
    n_part = 24
    dt_step = 0.25
    n_steps = 181
    D = 10.0
    sigma_um = np.sqrt(2.0 * D * dt_step)
    traj_um = np.zeros((n_steps, n_part, 2))
    angles0 = rng.uniform(-0.7, 0.7, size=n_part)
    traj_um[0, :, 0] = 13.0 * np.cos(angles0)
    traj_um[0, :, 1] = 13.0 * np.sin(angles0)
    for s_i in range(1, n_steps):
        pos = traj_um[s_i - 1] + rng.normal(0.0, sigma_um, size=(n_part, 2))
        r_norm = np.hypot(pos[:, 0], pos[:, 1])
        out = r_norm > 14.0
        if np.any(out):
            pos[out] *= (14.0 / r_norm[out])[:, None]
        traj_um[s_i] = pos
    return traj_um


def build_s02_end_state():
    """Shared helper so S02 ends and S03 starts on the exact same computed panel."""
    neuron = build_neuron(center_y=2.52, scale=0.66, nucleus_lit=0.90, include_organ=True)
    panel_l = RoundedRectangle(corner_radius=0.18, width=5.95, height=4.45,
                               stroke_color=STRUCT_COL, stroke_width=2.0,
                               fill_color=PANEL_FILL, fill_opacity=0.95).move_to([-3.25, -0.82, 0])
    panel_r = RoundedRectangle(corner_radius=0.18, width=5.95, height=4.45,
                               stroke_color=STRUCT_COL, stroke_width=2.0,
                               fill_color=PANEL_FILL, fill_opacity=0.95).move_to([3.15, -0.82, 0])

    eq = M("t ≈ x² / 2D", 36, TEXT).move_to([-3.25, 0.85, 0])
    eq_2d = M("2D = 20 µm²/s", 30, MT_COL).move_to([-3.25, 0.18, 0])
    step_x = M("x = 30 µm", 28, TEXT).move_to([-3.25, -0.48, 0])
    step_x2 = M("30² = 900 µm²", 28, TEXT).move_to([-3.25, -1.08, 0])
    step_res = M("900 ÷ 20 = 45 s", 30, DYNEIN_COL).move_to([-3.25, -1.72, 0])

    bar_bg = Rectangle(width=4.3, height=0.40, stroke_color=STRUCT_COL, stroke_width=2.2,
                       fill_opacity=0.0).move_to([-3.55, -2.48, 0])
    bar_fill = Rectangle(width=4.3 * (45.0 / 60.0), height=0.36, stroke_width=0,
                         fill_color=DYNEIN_COL, fill_opacity=0.92).align_to(bar_bg, LEFT).set_y(bar_bg.get_y())
    bar_lbl = M("45 s", 26, DYNEIN_COL).next_to(bar_bg, RIGHT, buff=0.16)

    inset_center = np.array([3.15, -0.78, 0.0])
    inset_r = 1.32
    inset_cell = Circle(radius=inset_r, color=MEMBRANE_COL, stroke_width=4.0,
                        fill_color=SOMA_FILL, fill_opacity=0.98).move_to(inset_center)
    inset_nuc = Circle(radius=0.50, color=NUCLEUS_STROKE, stroke_width=3.2,
                       fill_color=NUCLEUS_LIT, fill_opacity=0.92).move_to(inset_center)
    inset_title = T("30 µm cell body (zoom)", 26, MEMBRANE_COL).next_to(inset_cell, UP, buff=0.16)
    um_to_scene = inset_r / 15.0
    traj_um = _s02_diffusion_traj()
    inset_dots = VGroup(*[
        Dot(
            inset_center + np.array([traj_um[-1, j, 0] * um_to_scene,
                                     traj_um[-1, j, 1] * um_to_scene, 0.0]),
            radius=0.075, color=NGF_COL,
        )
        for j in range(traj_um.shape[1])
    ])
    clk = M("t =   45 s", 28, NGF_COL).move_to([3.15, -2.52, 0])
    return SimpleNamespace(
        neuron=neuron, panel_l=panel_l, panel_r=panel_r, eq=eq, eq_2d=eq_2d,
        step_x=step_x, step_x2=step_x2, step_res=step_res,
        bar_bg=bar_bg, bar_fill=bar_fill, bar_lbl=bar_lbl,
        inset_center=inset_center, inset_r=inset_r,
        inset_cell=inset_cell, inset_nuc=inset_nuc, inset_title=inset_title,
        inset_dots=inset_dots, clk=clk,
    )


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Long-Distance Signaling in Neurons"
    TITLE = "Beating Diffusion: The Signaling Endosome"


class S01Hook(SpokenScene):
    def construct(self):
        neuron = build_neuron(center_y=0.42, scale=1.04, nucleus_lit=0.75, include_organ=True)
        tag = scope_tag("schematic")

        rng = np.random.default_rng(7)
        n_ngf = 12
        ngf_starts = np.array([
            [5.40 + rng.uniform(-0.35, 0.35), 0.42 + rng.uniform(-0.95, 0.95), 0.0]
            for _ in range(n_ngf)
        ])
        ngf_targets = np.array([
            neuron.tip_ends[i % 3] + np.array([-0.14, rng.uniform(-0.08, 0.08), 0.0])
            for i in range(n_ngf)
        ])
        ngf_dots = VGroup(*[Dot(p, radius=0.105, color=NGF_COL) for p in ngf_starts])

        lbl_nuc = T("nucleus", 28, NUCLEUS_STROKE).next_to(neuron.soma, UP, buff=0.35)
        lbl_tip = T("axon tip", 28, MEMBRANE_COL).next_to(neuron.tip_branches, UP, buff=0.38).shift(LEFT * 0.55)
        lbl_organ = T("target organ", 28, NGF_COL).next_to(neuron.organ, UP, buff=0.35)
        if lbl_organ.get_right()[0] > FRAME_X - 0.15:
            lbl_organ.align_to([FRAME_X - 0.15, 0, 0], RIGHT)

        self.add(tag)
        self.play(FadeIn(neuron.group), FadeIn(ngf_dots),
                  FadeIn(lbl_nuc), FadeIn(lbl_tip), FadeIn(lbl_organ), run_time=1.4)

        self.at("survival signal")
        self.play(
            *[ngf_dots[i].animate.move_to(ngf_targets[i]) for i in range(n_ngf)],
            run_time=2.2,
        )

        self.at("centimeters")
        dist_arrow = DoubleArrow(
            [neuron.soma_center[0] + 1.05, 1.52, 0],
            [neuron.tip_center[0] - 0.65, 1.52, 0],
            color=NGF_COL, stroke_width=4.0, tip_length=0.22,
        )
        lbl_cm = T("centimeters", 30, NGF_COL).next_to(dist_arrow, UP, buff=0.18)
        self.play(GrowFromCenter(dist_arrow), FadeIn(lbl_cm), run_time=1.0)

        self.at("its nucleus")
        self.play(neuron.nucleus.animate.set_stroke(width=5.8), run_time=0.7)

        # Beat 3: Computed 1D diffusion walk + live spread envelope showing why diffusion stalls
        self.at("diffuse home")
        n_walk = 16
        base_x = neuron.axon_right - 0.15
        walk_positions = np.array([
            [base_x - rng.uniform(0.0, 0.35), 0.42 + rng.uniform(-0.10, 0.10), 0.0]
            for _ in range(n_walk)
        ])
        walk_dots = VGroup(*[Dot(p, radius=0.095, color=NGF_COL) for p in walk_positions])
        spread_bar = Rectangle(width=0.6, height=0.38, stroke_color=DIFF_COL, stroke_width=2.5,
                               fill_color=DIFF_COL, fill_opacity=0.28).move_to([base_x - 0.3, 0.42, 0])

        def walk_step(mob, dt):
            steps_x = rng.normal(-0.05 * dt, 0.70 * np.sqrt(max(dt, 1e-4)), size=n_walk)
            steps_y = rng.normal(0.0, 0.16 * np.sqrt(max(dt, 1e-4)), size=n_walk)
            for idx, d in enumerate(mob):
                walk_positions[idx, 0] = float(np.clip(walk_positions[idx, 0] + steps_x[idx],
                                                       neuron.axon_right - 1.55, neuron.axon_right + 0.12))
                walk_positions[idx, 1] = float(np.clip(walk_positions[idx, 1] + steps_y[idx],
                                                       0.42 - 0.11, 0.42 + 0.11))
                d.move_to(walk_positions[idx])
            min_x = float(walk_positions[:, 0].min())
            w = max(0.3, neuron.axon_right - min_x + 0.15)
            spread_bar.stretch_to_fit_width(w).move_to([neuron.axon_right - w / 2 + 0.05, 0.42, 0])

        walk_dots.add_updater(walk_step)
        self.add(spread_bar, walk_dots)
        q_mark = T("diffuse? (too slow)", 28, DIFF_COL).move_to([2.1, -0.60, 0.0])
        self.play(FadeIn(q_mark), run_time=0.9)

        self.at("move it instead")
        q_transport = T("active transport?", 28, DYNEIN_COL).move_to([-1.2, -0.60, 0.0])
        self.play(FadeIn(q_transport), run_time=0.9)

        self.at("thousand times longer")
        self.play(FadeOut(q_mark), FadeOut(q_transport), run_time=0.4)
        axon_bracket = BraceBetweenPoints(
            [neuron.axon_left, -0.22, 0.0],
            [neuron.axon_right, -0.22, 0.0],
            direction=DOWN, color=MT_COL,
        )
        lbl_1000x = T("axon: 1,000× longer", 28, MT_COL).next_to(axon_bracket, DOWN, buff=0.18)
        self.play(GrowFromCenter(axon_bracket), FadeIn(lbl_1000x), run_time=1.0)

        self.at("cell body")
        soma_bracket = BraceBetweenPoints(
            [neuron.soma_center[0] - neuron.soma_r, -1.05, 0.0],
            [neuron.soma_center[0] + neuron.soma_r, -1.05, 0.0],
            direction=DOWN, color=NUCLEUS_STROKE,
        )
        lbl_30 = T("cell body: ~30 µm", 28, NUCLEUS_STROKE).next_to(soma_bracket, DOWN, buff=0.18)
        self.play(GrowFromCenter(soma_bracket), FadeIn(lbl_30), run_time=0.9)
        self.finish()


class S02DiffusionMath(SpokenScene):
    def construct(self):
        neuron = build_neuron(center_y=2.52, scale=0.66, nucleus_lit=0.70, include_organ=True)
        panel_l = RoundedRectangle(corner_radius=0.18, width=5.95, height=4.45,
                                   stroke_color=STRUCT_COL, stroke_width=2.0,
                                   fill_color=PANEL_FILL, fill_opacity=0.95).move_to([-3.25, -0.82, 0])
        panel_r = RoundedRectangle(corner_radius=0.18, width=5.95, height=4.45,
                                   stroke_color=STRUCT_COL, stroke_width=2.0,
                                   fill_color=PANEL_FILL, fill_opacity=0.95).move_to([3.15, -0.82, 0])
        tag = scope_tag("schematic")
        self.add(tag)
        self.play(FadeIn(neuron.group), FadeIn(panel_l), FadeIn(panel_r), run_time=0.7)

        self.at("equals")
        eq = M("t ≈ x² / 2D", 36, TEXT).move_to([-3.25, 0.85, 0])
        self.play(Write(eq), run_time=2.5)

        inset_center = np.array([3.15, -0.78, 0.0])
        inset_r = 1.32
        inset_cell = Circle(radius=inset_r, color=MEMBRANE_COL, stroke_width=4.0,
                            fill_color=SOMA_FILL, fill_opacity=0.98).move_to(inset_center)
        inset_nuc = Circle(radius=0.50, color=NUCLEUS_STROKE, stroke_width=3.2,
                           fill_color=NUCLEUS_DIM, fill_opacity=0.92).move_to(inset_center)
        inset_title = T("30 µm cell body (zoom)", 26, MEMBRANE_COL).next_to(inset_cell, UP, buff=0.16)

        t_sim = ValueTracker(0.0)
        bar_col_t = ValueTracker(0.0)
        traj_um = _s02_diffusion_traj()
        n_steps, n_part = traj_um.shape[0], traj_um.shape[1]
        dt_step = 0.25

        um_to_scene = inset_r / 15.0

        def get_particles():
            idx = min(n_steps - 1, int(round(t_sim.get_value() / dt_step)))
            dots = VGroup()
            for j in range(n_part):
                p = inset_center + np.array([traj_um[idx, j, 0] * um_to_scene,
                                             traj_um[idx, j, 1] * um_to_scene, 0.0])
                dots.add(Dot(p, radius=0.075, color=NGF_COL))
            return dots

        live_dots = always_redraw(get_particles)
        clk = counter("t = {:4.0f} s", t_sim, at=[3.15, -2.52, 0], size=28, color=NGF_COL)
        bar_bg = Rectangle(width=4.3, height=0.40, stroke_color=STRUCT_COL, stroke_width=2.2,
                           fill_opacity=0.0).move_to([-3.55, -2.48, 0])
        bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.04, 4.3 * (t_sim.get_value() / 60.0)),
            height=0.36, stroke_width=0,
            fill_color=interpolate_color(ManimColor(TEXT), ManimColor(DYNEIN_COL), bar_col_t.get_value()),
            fill_opacity=0.92,
        ).align_to(bar_bg, LEFT).set_y(bar_bg.get_y()))
        bar_lbl = always_redraw(lambda: M(
            f"{t_sim.get_value():.0f} s", 26,
            interpolate_color(ManimColor(TEXT), ManimColor(DYNEIN_COL), bar_col_t.get_value()),
        ).next_to(bar_bg, RIGHT, buff=0.16))

        self.at("for a protein")
        self.play(
            FadeIn(inset_cell), FadeIn(inset_nuc), FadeIn(inset_title), FadeIn(bar_bg),
            run_time=1.0,
        )
        self.add(live_dots, clk, bar_fill, bar_lbl)

        self.at("twice that constant")
        eq_2d = M("2D = 20 µm²/s", 30, MT_COL).move_to([-3.25, 0.18, 0])
        self.play(FadeIn(eq_2d, shift=UP * 0.1), run_time=1.0)

        self.at("20 square")
        self.play(Indicate(eq_2d, color=TEXT, scale_factor=1.08), run_time=1.1)

        self.at("across a")
        step_x = M("x = 30 µm", 28, TEXT).move_to([-3.25, -0.48, 0])
        self.play(FadeIn(step_x), run_time=0.8)
        self.play(t_sim.animate.set_value(18.0), run_time=2.2, rate_func=linear)

        self.at("squared is")
        step_x2 = M("30² = 900 µm²", 28, TEXT).move_to([-3.25, -1.08, 0])
        self.play(FadeIn(step_x2), t_sim.animate.set_value(32.0), run_time=2.3, rate_func=linear)

        self.at("over 20 is")
        step_res = M("900 ÷ 20 = 45 s", 30, DYNEIN_COL).move_to([-3.25, -1.72, 0])
        self.play(FadeIn(step_res), t_sim.animate.set_value(45.0), run_time=1.0, rate_func=linear)

        self.at("works fine there")
        self.play(
            bar_col_t.animate.set_value(1.0),
            inset_nuc.animate.set_fill(NUCLEUS_LIT, opacity=0.92),
            neuron.nucleus.animate.set_fill(NUCLEUS_LIT, opacity=0.92),
            run_time=1.0,
        )
        self.finish()


class S03CentimeterFails(SpokenScene):
    def construct(self):
        s2 = build_s02_end_state()
        tag = scope_tag("schematic")
        self.add(
            tag, s2.neuron.group, s2.panel_l, s2.panel_r, s2.eq, s2.eq_2d,
            s2.step_x, s2.step_x2, s2.step_res,
            s2.bar_bg, s2.bar_fill, s2.bar_lbl,
            s2.inset_cell, s2.inset_nuc, s2.inset_dots, s2.inset_title, s2.clk,
        )

        self.at("one centimeter")
        span_line = DoubleArrow(
            [s2.neuron.soma_center[0] + 0.65, 3.30, 0],
            [s2.neuron.tip_center[0] - 0.35, 3.30, 0],
            color=DIFF_COL, stroke_width=3.2, tip_length=0.18,
        )
        span_lbl = M("1 cm = 10,000 µm", 26, DIFF_COL).next_to(span_line, UP, buff=0.06)
        new_x = M("x = 1 cm (10,000 µm)", 26, DIFF_COL).move_to([-3.25, -0.34, 0])

        tube_left, tube_right = 0.55, 5.75
        tube_y = -0.18
        tube_box = Rectangle(width=tube_right - tube_left, height=0.98,
                             stroke_color=MEMBRANE_COL, stroke_width=3.2,
                             fill_color=SOMA_FILL, fill_opacity=0.98).move_to([(tube_left + tube_right) / 2, tube_y, 0])
        tube_nuc = Circle(radius=0.31, color=NUCLEUS_STROKE, stroke_width=2.8,
                          fill_color=NUCLEUS_DIM, fill_opacity=0.90).move_to([tube_left + 0.44, tube_y, 0])
        tube_lbl_l = T("nucleus", 24, NUCLEUS_STROKE).next_to(tube_box, UP, buff=0.16).align_to(tube_box, LEFT)
        tube_lbl_r = T("tip (0 µm)", 24, NGF_COL).next_to(tube_box, UP, buff=0.16).align_to(tube_box, RIGHT)
        tube_dist = M("10,000 µm", 24, DIFF_COL).next_to(tube_box, DOWN, buff=0.16)

        # Compact both panels above y = -1.78 so full-width 58-day bar sits cleanly below them
        new_panel_l = RoundedRectangle(corner_radius=0.18, width=5.95, height=3.15,
                                       stroke_color=STRUCT_COL, stroke_width=2.0,
                                       fill_color=PANEL_FILL, fill_opacity=0.95).move_to([-3.25, -0.18, 0])
        new_panel_r = RoundedRectangle(corner_radius=0.18, width=5.95, height=3.15,
                                       stroke_color=STRUCT_COL, stroke_width=2.0,
                                       fill_color=PANEL_FILL, fill_opacity=0.95).move_to([3.15, -0.18, 0])

        self.play(
            GrowFromCenter(span_line), FadeIn(span_lbl),
            Transform(s2.panel_l, new_panel_l),
            Transform(s2.panel_r, new_panel_r),
            s2.eq.animate.move_to([-3.25, 0.92, 0]),
            s2.eq_2d.animate.move_to([-3.25, 0.30, 0]),
            swap(s2.step_x, new_x, run_time=0.65),
            FadeOut(s2.step_x2, run_time=0.35),
            FadeOut(s2.step_res, run_time=0.35),
            FadeOut(s2.bar_bg, run_time=0.35),
            FadeOut(s2.bar_fill, run_time=0.35),
            FadeOut(s2.bar_lbl, run_time=0.35),
            FadeOut(s2.inset_cell, run_time=0.45),
            FadeOut(s2.inset_nuc, run_time=0.45),
            FadeOut(s2.inset_dots, run_time=0.45),
            FadeOut(s2.inset_title, run_time=0.45),
            FadeOut(s2.clk, run_time=0.45),
            run_time=1.0,
        )

        rng = np.random.default_rng(7)
        n_dots = 18
        pos_um = np.full(n_dots, 9950.0)
        ys_off = rng.uniform(-0.32, 0.32, size=n_dots)
        walk_dots = VGroup(*[
            Dot([tube_right - 0.10, tube_y + ys_off[i], 0], radius=0.08, color=NGF_COL)
            for i in range(n_dots)
        ])

        def diffuse_1d(mob, dt):
            sim_dt = 450.0 * dt
            sigma = np.sqrt(2.0 * 10.0 * sim_dt)
            steps = rng.normal(0.0, sigma, size=n_dots)
            for i, d in enumerate(mob):
                pos_um[i] = float(np.clip(pos_um[i] + steps[i], 0.0, 9970.0))
                fx = pos_um[i] / 10000.0
                d.move_to([tube_left + fx * (tube_right - tube_left), tube_y + ys_off[i], 0.0])

        walk_dots.add_updater(diffuse_1d)
        self.play(FadeIn(tube_box), FadeIn(tube_nuc), FadeIn(tube_lbl_l),
                  FadeIn(tube_lbl_r), FadeIn(tube_dist), run_time=0.6)
        self.add(walk_dots)

        self.at("squared is")
        new_x2 = M("10,000² = 100,000,000 µm²", 24, TEXT).move_to([-3.25, -0.86, 0])
        self.play(FadeIn(new_x2), run_time=0.8)

        self.at("over 20 is")
        new_res = M("100,000,000 ÷ 20 = 5,000,000 s", 22, DIFF_COL).move_to([-3.25, -1.38, 0])
        fit(new_res, max_w=new_panel_l.width - 0.5)
        bar_t = ValueTracker(0.0)
        bar_x0 = -5.8
        full_w = 11.6
        diff_bar = always_redraw(lambda: Rectangle(
            width=max(0.08, full_w * bar_t.get_value()),
            height=0.48, stroke_color=DIFF_COL, stroke_width=2.2,
            fill_color=DIFF_COL, fill_opacity=0.88,
        ).move_to([bar_x0 + max(0.08, full_w * bar_t.get_value()) / 2, -2.42, 0]))
        days_lbl = always_redraw(lambda: M(
            f"≈ {58.0 * bar_t.get_value():.0f} days ({5000000 * bar_t.get_value():,.0f} s)",
            26, TEXT
        ).move_to([0.0, -3.02, 0]))
        self.add(diff_bar, days_lbl)
        self.play(
            FadeIn(new_res, run_time=0.9),
            bar_t.animate(run_time=1.1, rate_func=linear).set_value(1.0),
        )

        self.at("about 58 days")
        days_lbl.clear_updaters()
        diff_bar.clear_updaters()
        self.play(
            Indicate(days_lbl, color=DIFF_COL, scale_factor=1.12),
            Indicate(diff_bar, color=NGF_COL, scale_factor=1.02),
            run_time=1.2,
        )

        self.at("cannot wait")
        self.play(
            s2.neuron.nucleus.animate.set_fill(NUCLEUS_DIM, opacity=0.45).set_stroke(opacity=0.45),
            tube_nuc.animate.set_fill(NUCLEUS_DIM, opacity=0.35).set_stroke(opacity=0.40),
            run_time=1.2,
        )
        self.finish()


class S04Campenot(SpokenScene):
    def construct(self):
        neuron = build_neuron(center_y=-0.08, scale=1.0, nucleus_lit=0.25, include_organ=False, sx_offset=0.52)
        tag = scope_tag("schematic")
        self.add(tag)
        self.play(FadeIn(neuron.group), run_time=1.0)

        self.at("sealed barrier")
        chamber_l = RoundedRectangle(
            corner_radius=0.15, width=6.05, height=4.1,
            stroke_color=STRUCT_COL, stroke_width=2.5,
            fill_color=PANEL_FILL, fill_opacity=0.65,
        ).move_to([-3.15, -0.08, 0]).set_z_index(-1)
        chamber_r = RoundedRectangle(
            corner_radius=0.15, width=5.65, height=4.1,
            stroke_color=NGF_COL, stroke_width=2.5,
            fill_color=PANEL_FILL, fill_opacity=0.65,
        ).move_to([3.05, -0.08, 0]).set_z_index(-1)

        barrier = Rectangle(
            width=0.34, height=3.3,
            stroke_color=MEMBRANE_COL, stroke_width=2.8,
            fill_color=STRUCT_COL, fill_opacity=0.75,
        ).move_to([0.04, 1.05, 0])
        seal_cuff = Rectangle(
            width=0.42, height=0.42,
            stroke_color=MEMBRANE_COL, stroke_width=2.2,
            fill_color=SOMA_FILL, fill_opacity=0.90,
        ).move_to([0.04, -0.08, 0])

        lbl_barrier = T("sealed barrier", 28, MEMBRANE_COL).move_to([0.04, 3.05, 0])
        lbl_left = T("Cell body chamber", 28, MEMBRANE_COL).move_to([-3.15, 2.38, 0])
        lbl_right = T("Axon chamber", 28, NGF_COL).move_to([3.05, 2.38, 0])

        self.play(FadeIn(chamber_l), FadeIn(chamber_r), run_time=0.6)
        self.play(barrier.animate.move_to([0.04, -0.08, 0]), run_time=0.9)
        self.play(FadeIn(lbl_barrier), FadeIn(seal_cuff), FadeIn(lbl_left), FadeIn(lbl_right), run_time=0.6)

        self.at("fluids apart")
        lbl_no_ngf = T("no NGF", 28, MEMBRANE_COL).move_to([-3.15, -1.65, 0])
        self.play(FadeIn(lbl_no_ngf), run_time=0.6)

        self.at("nerve growth factor")
        rng = np.random.default_rng(7)
        ngf_pts = [
            [rng.uniform(0.55, 5.55), rng.uniform(-0.95, 1.65), 0.0]
            for _ in range(26)
        ]
        ngf_chamber_dots = VGroup(*[Dot(p, radius=0.095, color=NGF_COL) for p in ngf_pts])
        vels = rng.uniform(-0.24, 0.24, size=(26, 2))

        def drift_right_chamber(mob, dt):
            for i, d in enumerate(mob):
                d.shift([vels[i, 0] * dt, vels[i, 1] * dt, 0.0])
                p = d.get_center()
                if p[0] < 0.48 or p[0] > 5.65:
                    vels[i, 0] *= -1
                    d.set_x(float(np.clip(p[0], 0.48, 5.65)))
                if p[1] < -1.00 or p[1] > 1.70:
                    vels[i, 1] *= -1
                    d.set_y(float(np.clip(p[1], -1.00, 1.70)))

        lbl_ngf = T("+ NGF", 28, NGF_COL).move_to([3.05, -1.65, 0])
        ngf_chamber_dots.add_updater(drift_right_chamber)
        self.play(
            chamber_r.animate.set_fill(NGF_COL, opacity=0.16),
            FadeIn(ngf_chamber_dots), FadeIn(lbl_ngf),
            run_time=1.2,
        )

        self.at("cell bodies survive")
        pulse_x = ValueTracker(neuron.axon_right)
        pulse_dot = always_redraw(lambda: Dot([pulse_x.get_value(), -0.08, 0.0], radius=0.15, color=KINASE_COL))
        pulse_halo = always_redraw(lambda: Circle(radius=0.28, color=KINASE_COL, stroke_width=3.2,
                                                  fill_opacity=0.20).move_to([pulse_x.get_value(), -0.08, 0.0]))
        self.add(pulse_halo, pulse_dot)
        self.play(pulse_x.animate.set_value(neuron.soma_center[0]), run_time=2.3, rate_func=linear)
        pulse_dot.clear_updaters()
        pulse_halo.clear_updaters()
        lbl_surv = T("cell bodies survive", 28, DYNEIN_COL).move_to([-3.15, -2.58, 0])
        self.play(FadeIn(lbl_surv), FadeOut(pulse_dot), FadeOut(pulse_halo), run_time=0.5)

        self.at("inside the nucleus")
        self.play(neuron.nucleus.animate.set_fill(NUCLEUS_LIT, opacity=0.98), run_time=0.9)

        self.at("gene switch")
        lbl_creb = T("CREB active", 28, NUCLEUS_STROKE).next_to(neuron.soma, UP, buff=0.22)
        self.play(FadeIn(lbl_creb, shift=UP * 0.1), run_time=0.4)
        self.finish()


class S05EndocytosisPredict(SpokenScene):
    def construct(self):
        neuron = build_neuron(center_y=0.15, scale=1.04, nucleus_lit=0.80, include_organ=True)
        tag = T("schematic", 24, STRUCT_COL).move_to([FRAME_X - 0.2 - 0.75, FRAME_Y - 0.35, 0])
        self.add(tag)
        self.play(FadeIn(neuron.group), run_time=0.6)

        sig_x = ValueTracker(neuron.axon_right)
        sig_dot = always_redraw(lambda: Dot([sig_x.get_value(), 0.15, 0.0], radius=0.15, color=KINASE_COL))
        retro_arrow = Arrow([3.2, 0.96, 0], [-2.8, 0.96, 0], color=KINASE_COL, stroke_width=5.8, buff=0)
        self.add(sig_dot)
        self.play(GrowArrow(retro_arrow), sig_x.animate.set_value(neuron.soma_center[0]),
                  run_time=4.2, rate_func=linear)

        self.at("retrograde signaling")
        lbl_retro = T("Retrograde signaling", 32, KINASE_COL).next_to(retro_arrow, UP, buff=0.22)
        self.play(FadeIn(lbl_retro), run_time=1.0)

        self.at("at the tip")
        self.remove(sig_dot)
        self.play(FadeOut(neuron.group), FadeOut(retro_arrow), FadeOut(lbl_retro), run_time=0.6)

        phi_t = ValueTracker(0.02)
        ngf_t = ValueTracker(0.0)
        live_tip = always_redraw(lambda: build_pinched_membrane(
            phi=phi_t.get_value(),
            y_top=1.75,
            ngf_bound=ngf_t.get_value(),
            show_labels=True,
        ))
        self.add(live_tip)

        self.at("binds its receptor")
        self.play(ngf_t.animate.set_value(1.0), run_time=2.2, rate_func=smooth)

        self.at("pinches inward")
        self.play(phi_t.animate.set_value(0.7), run_time=3.0, rate_func=smooth)

        self.at("predict")
        q = question_card("Does TrkA's active kinase face into the vesicle or out?")
        self.play(FadeIn(q), run_time=0.8)

        outer_pts, _, normals, (cup_start, n_cup) = _pocket_points(0.7, y_top=1.75)
        knob_pts = [
            outer_pts[idx] + normals[idx] * 0.74
            for idx in [cup_start + int(n_cup * 0.30), cup_start + int(n_cup * 0.70)]
        ]
        self.at("active kinase")
        halos = VGroup(*[
            Circle(radius=0.32, color=KINASE_COL, stroke_width=4.0,
                   fill_color=KINASE_COL, fill_opacity=0.25).move_to(p)
            for p in knob_pts
        ])
        self.play(FadeIn(halos), run_time=0.4)
        for _ in range(2):
            self.play(
                *[h.animate.scale(1.65).set_stroke(opacity=0.95).set_fill(opacity=0.40) for h in halos],
                rate_func=there_and_back, run_time=1.45,
            )
        self.play(FadeOut(halos), run_time=0.3)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Does TrkA's active kinase face into the vesicle or out?"
    OPTIONS = ()
    SECONDS = 4.5

    def backdrop(self):
        return build_pinched_backdrop()


class S07TopologyReveal(SpokenScene):
    def construct(self):
        tag = T("schematic", 24, STRUCT_COL).move_to([FRAME_X - 0.2 - 0.75, FRAME_Y - 0.35, 0])
        self.add(tag)

        phi_t = ValueTracker(0.7)
        pocket = always_redraw(lambda: build_pinched_membrane(
            phi=phi_t.get_value(), y_top=1.75, ngf_bound=1.0, show_labels=False
        ))
        l_out = T("Outside (extracellular)", 28, MEMBRANE_COL).move_to([-4.0, 2.58, 0])
        # Placed cleanly left of partner blocks (partners at x = +/- 1.65)
        l_cyto = T("Cytoplasm (inside)", 26, MEMBRANE_COL).move_to([-4.55, -2.10, 0])
        self.add(pocket, l_out, l_cyto)

        self.play(phi_t.animate.set_value(2.74), run_time=3.2, rate_func=smooth)

        self.at("folds inward")
        flat_outer = Line([-6.2, 1.75, 0], [6.2, 1.75, 0], color=MEMBRANE_COL, stroke_width=6.0)
        flat_inner = Line([-6.2, 1.61, 0], [6.2, 1.61, 0], color=MEMBRANE_INNER, stroke_width=3.8)
        cyto_bg = Rectangle(width=12.4, height=5.20, stroke_width=0, fill_color=SOMA_FILL,
                            fill_opacity=0.95).move_to([0.0, -0.85, 0])

        endo_g, endo_ns = build_signaling_endosome([0.0, -0.05, 0.0], radius=1.18)
        lbl_endo = T("Signaling endosome", 30, TRKA_COL).move_to([3.95, 0.85, 0])
        lbl_kin = T("kinase faces out\n(cytoplasm)", 26, KINASE_COL, line_spacing=0.85).move_to([3.95, -0.35, 0])

        self.remove(pocket)
        self.add(cyto_bg, flat_inner, flat_outer, endo_g)
        self.remove(l_cyto)
        self.add(l_cyto)

        self.play(
            endo_g.animate.shift(DOWN * 0.20),
            FadeIn(lbl_endo), FadeIn(lbl_kin),
            run_time=1.8,
        )

        # Rotate vesicle slightly while highlighting outer->inner membrane topology over 6.8..12.8 s
        c_endo = endo_ns.inner.get_center()
        kin_ring = Circle(radius=1.76, color=KINASE_COL, stroke_width=4.0).move_to(c_endo)
        self.play(Create(kin_ring), Rotate(endo_g, angle=18 * DEGREES, about_point=c_endo), run_time=2.2)
        lining_trace = Circle(radius=1.18 * 0.84, color=MEMBRANE_COL, stroke_width=7.5).move_to(c_endo)
        self.play(FadeOut(kin_ring), Create(lining_trace), Rotate(endo_g, angle=-18 * DEGREES, about_point=c_endo), run_time=3.2)
        self.play(FadeOut(lining_trace), run_time=1.0)

        self.at("now lines the vesicle")
        lbl_lining = T("outer face → inner lining", 26, MEMBRANE_COL).move_to([-4.05, 0.65, 0])
        arr_lining = Arrow(
            lbl_lining.get_right() + RIGHT * 0.14,
            endo_ns.inner.get_left() + RIGHT * 0.10,
            color=MEMBRANE_COL, stroke_width=4.0, tip_length=0.22,
        )
        self.play(
            endo_ns.inner.animate.set_stroke(width=8.5),
            FadeIn(lbl_lining), GrowArrow(arr_lining),
            run_time=1.8,
        )

        self.at("trapped inside")
        lbl_ngf_in = T("NGF trapped inside", 26, NGF_COL).move_to([-4.05, -0.25, 0])
        self.play(
            swap(lbl_lining, lbl_ngf_in, run_time=0.8),
            FadeOut(arr_lining, run_time=0.4),
            endo_ns.inner.animate.set_stroke(width=4.8),
            endo_ns.ngfs.animate.scale(1.18),
            run_time=1.8,
        )

        self.at("stays in the cytoplasm")
        partners = VGroup(
            RoundedRectangle(corner_radius=0.12, width=1.35, height=0.56, stroke_color=TEXT,
                             stroke_width=2.6, fill_color=TEXT, fill_opacity=0.16).move_to([-1.65, -3.05, 0]),
            RoundedRectangle(corner_radius=0.12, width=1.35, height=0.56, stroke_color=TEXT,
                             stroke_width=2.6, fill_color=TEXT, fill_opacity=0.16).move_to([1.65, -3.05, 0]),
        )
        p_labels = VGroup(
            T("partner", 24, TEXT).move_to(partners[0]),
            T("partner", 24, TEXT).move_to(partners[1]),
        )
        self.play(FadeIn(partners), FadeIn(p_labels), run_time=0.8)

        self.at("ready to")
        self.play(
            partners[0].animate.move_to([-1.65, -2.10, 0]).set_stroke(KINASE_COL),
            p_labels[0].animate.move_to([-1.65, -2.10, 0]),
            partners[1].animate.move_to([1.65, -2.10, 0]).set_stroke(KINASE_COL),
            p_labels[1].animate.move_to([1.65, -2.10, 0]),
            run_time=0.55,
        )
        p_badges = VGroup(
            T("+ P", 26, KINASE_COL).next_to(partners[0], DOWN, buff=0.14),
            T("+ P", 26, KINASE_COL).next_to(partners[1], DOWN, buff=0.14),
        )
        self.play(FadeIn(p_badges), run_time=0.35)
        self.finish()


class S08MicrotubulesMotors(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        axon_top = Line([-5.9, 2.38, 0], [5.9, 2.38, 0], color=MEMBRANE_COL, stroke_width=4.5)
        axon_bot = Line([-5.9, -2.35, 0], [5.9, -2.35, 0], color=MEMBRANE_COL, stroke_width=4.5)
        axon_fill = Rectangle(width=11.8, height=4.73, stroke_width=0, fill_color=SOMA_FILL,
                              fill_opacity=0.95).move_to([0.0, 0.015, 0])

        lbl_soma = T("← Cell body", 28, NUCLEUS_STROKE).move_to([-4.6, 2.88, 0])
        lbl_tip = T("Axon tip →", 28, NGF_COL).move_to([4.6, 2.88, 0])
        endo_g, _ = build_signaling_endosome([3.8, -0.35, 0.0], radius=0.52)

        self.add(tag, axon_fill)
        self.play(Create(axon_top), Create(axon_bot), FadeIn(lbl_soma), FadeIn(lbl_tip),
                  FadeIn(endo_g), run_time=1.8)

        mt_upper = build_mt_track(-5.6, 5.6, 0.95, stroke=6.5, n_chevrons=6)
        mt_lower = build_mt_track(-5.6, 5.6, -1.35, stroke=6.5, n_chevrons=6)
        lbl_mt = T("Microtubules", 28, MT_COL).move_to([0.0, 2.88, 0])
        self.play(Create(mt_upper), Create(mt_lower), FadeIn(lbl_mt), run_time=3.2)

        self.at("toward the tip")
        lbl_plus = T("+ end", 28, MT_COL).move_to([4.85, 1.50, 0])
        plus_pulse = Arrow([3.2, 1.48, 0], [4.2, 1.48, 0], color=MT_COL, stroke_width=4.0, buff=0)
        self.play(FadeIn(lbl_plus), GrowArrow(plus_pulse), run_time=1.4)

        self.at("toward the cell body")
        lbl_minus = T("− end", 28, MT_COL).move_to([-4.85, 1.50, 0])
        minus_pulse = Arrow([-3.2, 1.48, 0], [-4.2, 1.48, 0], color=MT_COL, stroke_width=4.0, buff=0)
        self.play(FadeIn(lbl_minus), GrowArrow(minus_pulse), run_time=1.4)

        self.at("walk outward")
        kin_x = ValueTracker(-3.2)
        kin_mob = always_redraw(lambda: build_kinesin(
            [kin_x.get_value(), 1.02, 0.0],
            phase=kin_x.get_value() * 8.0,
            scale=1.18,
        ))
        # Place Kinesin label cleanly in the open central lane between the two tracks
        lbl_kin = T("Kinesin (+ end →)", 26, KINESIN_COL).move_to([0.0, 0.22, 0])
        self.add(kin_mob)
        self.play(
            FadeIn(lbl_kin, run_time=0.5),
            FadeOut(plus_pulse, run_time=0.4),
            FadeOut(minus_pulse, run_time=0.4),
            kin_x.animate(run_time=2.5, rate_func=linear).set_value(3.8),
        )

        self.at("dynein")
        self.play(FadeOut(endo_g), FadeOut(lbl_kin), run_time=0.3)

        dyn_x = ValueTracker(3.8)
        dyn_mob = always_redraw(lambda: build_dynein_with_endosome(
            track_y=-1.35,
            x_pos=dyn_x.get_value(),
            phase=dyn_x.get_value() * 8.0,
            scale=1.05,
            endosome_radius=0.46,
        ))
        lbl_dyn = T("← Dynein + dynactin (− end)", 26, DYNEIN_COL).move_to([0.0, -1.88, 0])
        self.add(dyn_mob)
        self.play(FadeIn(lbl_dyn), run_time=0.4)

        self.at("walks toward")
        self.play(dyn_x.animate.set_value(2.2), run_time=1.5, rate_func=linear)

        self.at("signaling endosome home")
        self.play(dyn_x.animate.set_value(-4.2), run_time=3.6, rate_func=linear)
        self.finish()


class S09MotorMath(SpokenScene):
    def construct(self):
        neuron = build_neuron(center_y=2.48, scale=0.64, nucleus_lit=0.25, include_organ=True)
        mt_axon = Line([neuron.axon_left, 2.48, 0], [neuron.axon_right, 2.48, 0],
                       color=MT_COL, stroke_width=4.0)
        panel_bg = RoundedRectangle(corner_radius=0.18, width=12.6, height=4.30,
                                    stroke_color=STRUCT_COL, stroke_width=2.0,
                                    fill_color=PANEL_FILL, fill_opacity=0.95).move_to([0.0, -0.80, 0])

        t_motor = ValueTracker(0.0)
        x_start = neuron.axon_right - 0.15
        x_end = neuron.soma_center[0] + 0.35

        def get_carrier():
            frac = float(np.clip(t_motor.get_value() / 10000.0, 0.0, 1.0))
            cx = x_start + frac * (x_end - x_start)
            endo, _ = build_signaling_endosome([cx, 2.48, 0.0], radius=0.19)
            collar = Arc(radius=0.25, start_angle=-30 * DEGREES, angle=140 * DEGREES,
                         arc_center=[cx, 2.48, 0.0], color=DYNEIN_COL, stroke_width=4.5)
            return VGroup(collar, endo)

        carrier = always_redraw(get_carrier)
        tag = scope_tag("schematic")
        self.add(tag, neuron.group, mt_axon, panel_bg, carrier)

        self.at("distance divided by speed")
        eq = M("t = x / v", 36, TEXT).move_to([-3.2, 0.78, 0])
        self.play(Write(eq), run_time=1.2)

        self.at("micrometer per second")
        eq_v = M("v ≈ 1 µm/s", 28, DYNEIN_COL).move_to([-3.2, 0.16, 0])
        ro = Readout([
            ("x", lambda: t_motor.get_value(), "{:6.0f} µm", TEXT),
            ("t", lambda: t_motor.get_value(), "{:6.0f} s", DYNEIN_COL),
        ], at=[4.05, 0.15, 0], size=26, widest=[10000, 10000], title="dynein trip (1 µm/s)")

        # Live trip progress bar driven by t_motor so motion spans the whole math panel
        prog_bg = Rectangle(width=5.6, height=0.22, stroke_color=STRUCT_COL, stroke_width=1.8,
                            fill_opacity=0.0).move_to([-2.4, -0.88, 0])
        prog_fill = always_redraw(lambda: Rectangle(
            width=max(0.03, 5.6 * (t_motor.get_value() / 10000.0)),
            height=0.18, stroke_width=0, fill_color=DYNEIN_COL, fill_opacity=0.90,
        ).align_to(prog_bg, LEFT).set_y(prog_bg.get_y()))
        self.play(FadeIn(eq_v), FadeIn(ro), FadeIn(prog_bg), run_time=0.7)
        self.add(prog_fill)

        self.play(t_motor.animate.set_value(5500.0), run_time=1.5, rate_func=linear)

        self.at("covers")
        eq_calc = M("10,000 µm ÷ 1 µm/s = 10,000 s (< 3 hr)", 24, DYNEIN_COL).move_to([-2.05, -0.44, 0])
        self.play(
            FadeIn(eq_calc, run_time=0.6),
            t_motor.animate(run_time=1.6, rate_func=linear).set_value(10000.0),
        )

        self.at("Five million")
        self.play(FadeOut(prog_bg), FadeOut(prog_fill), run_time=0.4)
        bar_w = 10.6
        bar_x0 = -5.3
        # Grow diffusion bar dynamically to 58 days vs 1/500 width emerald dynein bar
        bar_grow = ValueTracker(0.0)
        diff_bar = always_redraw(lambda: Rectangle(
            width=max(0.06, bar_w * bar_grow.get_value()),
            height=0.38, stroke_color=DIFF_COL, stroke_width=2.0,
            fill_color=DIFF_COL, fill_opacity=0.88,
        ).move_to([bar_x0 + max(0.06, bar_w * bar_grow.get_value()) / 2, -1.32, 0]))
        diff_lbl = M("Diffusion: 5,000,000 s (≈ 58 days)", 24, DIFF_COL).move_to([-2.4, -1.76, 0]).align_to([bar_x0, 0, 0], LEFT)

        motor_w = bar_w / 500.0
        motor_bar = Rectangle(width=max(0.03, motor_w), height=0.38, stroke_color=DYNEIN_COL, stroke_width=2.5,
                              fill_color=DYNEIN_COL, fill_opacity=0.95).move_to([bar_x0 + max(0.03, motor_w) / 2, -2.18, 0])
        motor_lbl = M("Dynein: 10,000 s (< 3 hr)", 24, DYNEIN_COL).next_to(motor_bar, RIGHT, buff=0.22)
        ratio_lbl = M("5,000,000 s ÷ 10,000 s = 500× faster", 28, NGF_COL).move_to([0.0, -2.65, 0])

        self.add(diff_bar)
        self.play(bar_grow.animate.set_value(1.0), FadeIn(diff_lbl),
                  FadeIn(motor_bar), FadeIn(motor_lbl),
                  run_time=1.8, rate_func=linear)

        self.at("500")
        self.play(FadeIn(ratio_lbl), run_time=0.6)

        self.at("leading model")
        new_tag = scope_tag("leading model")
        self.play(swap(tag, new_tag, run_time=0.5))

        self.at("trigger survival genes")
        lbl_genes = T("survival genes ON", 26, NUCLEUS_STROKE).move_to([-2.0, 3.40, 0])
        self.play(
            neuron.nucleus.animate.set_fill(NUCLEUS_LIT, opacity=0.98),
            FadeIn(lbl_genes),
            run_time=0.5,
        )
        self.finish()


class S10Takeaway(SpokenScene):
    def construct(self):
        neuron = build_neuron(center_y=0.55, scale=1.06, nucleus_lit=0.92, include_organ=True)
        mt = Line([neuron.axon_left, 0.55, 0], [neuron.axon_right, 0.55, 0],
                  color=MT_COL, stroke_width=4.6)
        tag = scope_tag("leading model")
        self.add(neuron.group, mt, tag)

        stream_t = ValueTracker(0.0)
        x_start = neuron.axon_right - 0.1
        x_end = neuron.soma_center[0] + 0.58
        span = x_start - x_end

        def make_stream():
            t = stream_t.get_value()
            g = VGroup()
            for k in range(3):
                u = (t + k / 3.0) % 1.0
                cx = x_start - u * span
                endo, _ = build_signaling_endosome([cx, 0.55, 0.0], radius=0.25)
                collar = Arc(radius=0.31, start_angle=-30 * DEGREES, angle=140 * DEGREES,
                             arc_center=[cx, 0.55, 0.0], color=DYNEIN_COL, stroke_width=4.8)
                g.add(collar, endo)
            return g

        stream = always_redraw(make_stream)
        self.add(stream)

        lbl_nuc = T("survival genes ON", 28, NUCLEUS_STROKE).move_to([-3.3, 2.15, 0])
        lbl_dyn = T("← dynein + signaling endosomes", 28, DYNEIN_COL).move_to([1.25, 1.65, 0])
        self.play(FadeIn(lbl_nuc), FadeIn(lbl_dyn), stream_t.animate.set_value(0.25), run_time=1.6, rate_func=linear)

        # Framed summary card in lower third comparing diffusion vs dynein
        comp_box = RoundedRectangle(corner_radius=0.16, width=10.6, height=1.75,
                                    stroke_color=STRUCT_COL, stroke_width=2.0,
                                    fill_color=PANEL_FILL, fill_opacity=0.92).move_to([0.0, -2.05, 0])

        self.at("passive spreading")
        comp_diff = M("Diffusion: ~58 days", 28, DIFF_COL).move_to([-2.6, -1.72, 0])
        comp_dyn = M("Dynein: < 3 hr", 28, DYNEIN_COL).move_to([2.6, -1.72, 0])
        self.play(FadeIn(comp_box), FadeIn(comp_diff), stream_t.animate.set_value(0.75), run_time=2.5, rate_func=linear)

        self.at("active signaling endosomes")
        self.play(stream_t.animate.set_value(1.30), run_time=2.8, rate_func=linear)

        self.at("survival message")
        self.play(FadeIn(comp_dyn), stream_t.animate.set_value(1.80), run_time=2.5, rate_func=linear)

        self.at("leading model")
        self.play(stream_t.animate.set_value(2.40), run_time=3.2, rate_func=linear)

        self.at("other retrograde routes")
        other_note = T("other retrograde routes remain open", 26, MEMBRANE_COL).move_to([0.0, -2.48, 0])
        self.play(
            FadeIn(other_note, run_time=0.6),
            stream_t.animate(run_time=2.7, rate_func=linear).set_value(2.95),
        )
        self.finish()


class S11End(EndCard):
    LINE = "Over long axons, dynein carries active signaling endosomes where diffusion fails."
