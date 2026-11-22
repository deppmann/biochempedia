"""Making Pulses and Fixing Place — animation for STEMhop (shape-of-a-signal, chapter 2).

COLOUR MAP (one colour per concept across the whole film):
- GOLD (#D4A843)  : Signal / outside stimulus / cAMP messenger / phosphate tags (P)
- TEAL (#3FB8C0)  : Decoder / effector (NF-kappaB, PKA, LAT cluster, delayed pulse curve)
- GREEN (#83C167) : Active / kinase-favoured state (nuclear NF-kappaB gene on, active PKA/channel, kinases, "stay on longer")
- RED (#FC6255)   : Inhibitor / phosphatase brake (IkappaB, IkappaBalpha, phosphatases, negative-feedback brake)
- GREY (#8B93A1)  : Cell membranes, AKAP scaffold, axes, schematic boundaries (shapes/axes only; labels use TEXT or concept colours)
- TEXT (#E8EAF0)  : Labels, questions, laser beam

CARRIED WORLD:
A large cross-section of a single cell on the left (plasma membrane across top, cytoplasm in middle,
nucleus oval at bottom) paired with a live computed trace panel on the right; zooming in to the plasma
membrane for spatial anchoring (AKAP/PKA) and an inset glass-slide bilayer for purified LAT clustering
and kinase/phosphatase sorting, then returning to the living cell membrane for FRAP and the full
panoramic cell for the wrap-up.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook: Recap duration block and spike train draw on the Plot, clear, then a steady amber beam hits the membrane while a computed delayed-feedback oscillation draws on the trace and a local membrane spot lights up.
- s02_delay_feedback: Computed no-delay ODE curve settles monotonically flat; adding a delay starts the computed delayed-feedback ODE curve overshooting above and below steady level while the clock hand turns and live Active A(t) and Brake B(t) gauges move in phase with the computed ODE.
- s03_nfkb_loop: Steady stimulus shatters IkappaB clamps; NF-kappaB translocates into the nucleus as the computed NF-kappaB ODE curve climbs, lights the IkappaBalpha gene, and fills the synthesis-delay progress bar to 100% before fresh IkappaBalpha appears.
- s04_nfkb_oscillate: Continues the exact computed NF-kappaB ODE trajectory: fresh IkappaBalpha exports NF-kappaB (trace drops), steady stimulus degrades it, and two more computed pulses cycle before zooming cleanly to the plasma membrane.
- s05_akap_place: AKAP anchors PKA beside a channel while an identical PKA sits far away; a seeded 2D random-walk cloud of cAMP blooms locally on the left, switching left PKA and its channel green while the distant PKA remains unreached teal.
- s06_lat_slide: Continues from the living membrane into an artificial bilayer inset where kinase adds amber phosphates to receptor tail and LAT; a seeded Langevin simulation pulls LAT and partners together with dynamic weak-contact lines into a coalesced liquid-like cluster.
- s07_predict_q: Computed 2D particle kinematics pull green kinases inward to drift inside the cluster while red phosphatases bounce elastically off its rim and stay outside, ending with the prediction question card.
- s09_predict_reveal_caveat: Cluster turns green as computed steady-state phosphate fraction bars rise inside vs stay low outside; closes to living cell membrane where a laser bleaches a spot and computed exponential FRAP recovery runs identically inside both "Liquid droplet?" and "Fixed scaffold?" panels.
- s10_wrap: Panoramic carried cell runs the computed NF-kappaB oscillation (cell + right trace) at bottom while anchored green PKA with local cAMP and the cautiously labelled membrane cluster sit at the top membrane.
"""
from bp_parts import *

# Concept colours
C_SIGNAL = GOLD
C_DECODER = TEAL
C_ACTIVE = GREEN
C_BRAKE = RED
C_STRUCT = GREY
C_TEXT = TEXT
C_CELL_FILL = "#151A26"
C_NUC_FILL = "#1B2233"

# ------------------------------------------------------------------
# Computed ODE / simulation models (deterministic, shared across scenes)
# ------------------------------------------------------------------

def compute_delay_feedback(tau=1.2, t_max=12.0, dt=0.01):
    """Integrate delayed negative feedback ODE:
        dA/dt = s / (1 + (B / K)^hill) - gA * A
        dB/dt = b * A(t - tau) - gB * B
    For tau == 0, uses instantaneous brake B = (b / gB) * A so no-delay settles flat.
    Returns (t_arr, A_arr, B_arr, A_steady).
    """
    n = int(round(t_max / dt)) + 1
    d_steps = int(round(tau / dt))
    A = np.zeros(n)
    B = np.zeros(n)
    s, K, hill, gA, b, gB = 1.8, 0.5, 5, 1.5, 1.5, 1.5
    for i in range(n - 1):
        if tau <= 0.0:
            b_eff = (b / gB) * A[i]
            dA = s / (1.0 + (b_eff / K) ** hill) - gA * A[i]
            A[i + 1] = max(0.0, A[i] + dt * dA)
            B[i + 1] = (b / gB) * A[i + 1]
        else:
            a_del = A[max(0, i - d_steps)]
            dB = b * a_del - gB * B[i]
            dA = s / (1.0 + (B[i] / K) ** hill) - gA * A[i]
            A[i + 1] = max(0.0, A[i] + dt * dA)
            B[i + 1] = max(0.0, B[i] + dt * dB)
    t_arr = np.linspace(0.0, t_max, n)
    a_grid = np.linspace(0.0, 2.0, 2000)
    a_steady = float(a_grid[np.argmin(np.abs(s / (1.0 + (a_grid / K) ** hill) - gA * a_grid))])
    return t_arr, A, B, a_steady


_T_NODELAY, _A_NODELAY, _, _A_STEADY = compute_delay_feedback(tau=0.0, t_max=12.0)
_T_DELAY, _A_DELAY, _B_DELAY, _ = compute_delay_feedback(tau=1.2, t_max=12.0)


def delay_curve_fn(tau_on=True):
    ts = _T_DELAY if tau_on else _T_NODELAY
    ys = _A_DELAY if tau_on else _A_NODELAY
    return lambda t: float(np.interp(t, ts, ys))


def delay_brake_val(t):
    return float(np.interp(t, _T_DELAY, _B_DELAY))


def compute_nfkb_ode(t_max=15.0, dt=0.01):
    """3-variable NF-kappaB / IkappaBalpha delayed negative-feedback oscillator under steady stimulus.
    N: nuclear NF-kappaB (0..1.15), M: IkappaBalpha mRNA delay intermediate, I: free IkappaBalpha.
    """
    n = int(round(t_max / dt)) + 1
    N = np.zeros(n)
    M = np.zeros(n)
    I = np.zeros(n)
    N[0], M[0], I[0] = 0.04, 0.0, 0.95
    d_steps = int(round(1.1 / dt))
    for k in range(n - 1):
        n_del = N[max(0, k - d_steps)]
        dN = 1.45 / (1.0 + (I[k] / 0.28) ** 3) - 1.15 * N[k] * (0.25 + 1.4 * I[k])
        dM = 1.35 * (n_del ** 2) / (0.35 ** 2 + n_del ** 2) - 1.1 * M[k]
        dI = 1.55 * M[k] - 0.95 * I[k]
        N[k + 1] = float(np.clip(N[k] + dt * dN, 0.0, 1.25))
        M[k + 1] = float(np.clip(M[k] + dt * dM, 0.0, 1.5))
        I[k + 1] = float(np.clip(I[k] + dt * dI, 0.0, 1.5))
    return np.linspace(0.0, t_max, n), N, M, I


_T_NFKB, _N_NFKB, _M_NFKB, _I_NFKB = compute_nfkb_ode(t_max=14.0)


def nfkb_n_fn(t):
    return float(np.interp(t, _T_NFKB, _N_NFKB))


# ------------------------------------------------------------------
# Carried World Builders
# ------------------------------------------------------------------

def build_cell(x0=-6.1, x1=0.2, y0=-3.1, y1=2.6, with_labels=True):
    """Build the carried cross-section of a single cell with top plasma membrane and bottom nucleus."""
    cx = (x0 + x1) / 2.0
    w = x1 - x0
    h = y1 - y0
    body = RoundedRectangle(
        corner_radius=0.55, width=w, height=h,
        stroke_color=C_STRUCT, stroke_width=3.5,
        fill_color=C_CELL_FILL, fill_opacity=0.85,
    ).move_to([cx, (y0 + y1) / 2.0, 0])

    xs = np.linspace(x0 + 0.35, x1 - 0.35, 60)
    arc_y = y1 - 0.04 + 0.14 * np.cos(np.pi * (xs - cx) / w)
    outer_mem = VMobject(stroke_color=C_STRUCT, stroke_width=4.5)
    outer_mem.set_points_as_corners([np.array([x, y + 0.09, 0]) for x, y in zip(xs, arc_y)])
    inner_mem = VMobject(stroke_color=C_STRUCT, stroke_width=3.0)
    inner_mem.set_points_as_corners([np.array([x, y - 0.07, 0]) for x, y in zip(xs, arc_y)])
    membrane = VGroup(outer_mem, inner_mem)

    nuc_w = w * 0.74
    nuc_h = h * 0.40
    nuc_c = np.array([cx, y0 + nuc_h * 0.5 + 0.28, 0.0])
    nuc_outer = RoundedRectangle(
        corner_radius=nuc_h * 0.48, width=nuc_w, height=nuc_h,
        stroke_color=C_STRUCT, stroke_width=3.0,
        fill_color=C_NUC_FILL, fill_opacity=0.90,
    ).move_to(nuc_c)
    nuc_dash = DashedVMobject(
        RoundedRectangle(
            corner_radius=nuc_h * 0.46, width=nuc_w - 0.14, height=nuc_h - 0.14,
            stroke_color=C_STRUCT, stroke_width=2.0,
        ).move_to(nuc_c),
        num_dashes=34,
    )
    nucleus = VGroup(nuc_outer, nuc_dash)

    g = VGroup(body, membrane, nucleus)
    g.body = body
    g.membrane = membrane
    g.nucleus = nucleus
    g.nuc_center = nuc_c
    g.mem_top_y = y1 + 0.12
    g.cx = cx

    if with_labels:
        cyto_lbl = T("Cytoplasm", 24, C_TEXT).move_to([x1 - 1.10, y1 - 0.65, 0])
        nuc_lbl = T("Nucleus", 24, C_TEXT).move_to([nuc_c[0] - nuc_w * 0.29, nuc_c[1] - nuc_h * 0.06, 0])
        mem_lbl = T("Plasma membrane", 24, C_TEXT).move_to([x0 + 1.45, y1 + 0.46, 0])
        g.add(cyto_lbl, nuc_lbl, mem_lbl)
        g.cyto_lbl = cyto_lbl
        g.nuc_lbl = nuc_lbl
        g.mem_lbl = mem_lbl
    return g


def build_plasma_membrane_zoom(y_mem=1.65, x_left=-6.3, x_right=6.3):
    """Full-width plasma membrane zoom view (same bilayer aesthetic as the carried cell)."""
    bg_cyto = Rectangle(
        width=14.4, height=y_mem + 4.2,
        stroke_width=0, fill_color=C_CELL_FILL, fill_opacity=0.75,
    ).move_to([0, (y_mem - 4.2) / 2.0, 0])
    bg_cyto.set_z_index(-5)
    xs = np.linspace(x_left, x_right, 80)
    ys = y_mem + 0.08 * np.cos(0.35 * xs)
    top_line = VMobject(stroke_color=C_STRUCT, stroke_width=5)
    top_line.set_points_as_corners([np.array([x, y + 0.11, 0]) for x, y in zip(xs, ys)])
    bot_line = VMobject(stroke_color=C_STRUCT, stroke_width=4)
    bot_line.set_points_as_corners([np.array([x, y - 0.11, 0]) for x, y in zip(xs, ys)])
    bilayer = VGroup(bg_cyto, top_line, bot_line)
    mem_lbl = T("Plasma membrane", 26, C_TEXT).move_to([0, y_mem + 0.55, 0])
    cyto_lbl = T("Cytoplasm", 26, C_TEXT).move_to([-4.9, -2.75, 0])
    g = VGroup(bilayer, mem_lbl, cyto_lbl)
    g.y_mem = y_mem
    g.mem_lbl = mem_lbl
    g.cyto_lbl = cyto_lbl
    return g


def build_steady_beam(x=-2.45, y_top=3.38, y_mem=2.68, label="Steady stimulus"):
    """Amber beam hitting top membrane, with label placed clearly to its right above membrane."""
    beam = VGroup(
        Rectangle(width=0.45, height=y_top - y_mem, stroke_width=0, fill_color=C_SIGNAL, fill_opacity=0.35).move_to([x, (y_top + y_mem) / 2, 0]),
        Arrow(np.array([x, y_top, 0]), np.array([x, y_mem, 0]), buff=0, color=C_SIGNAL, stroke_width=6, max_tip_length_to_length_ratio=0.32),
        Dot(np.array([x, y_mem - 0.05, 0]), radius=0.14, color=C_SIGNAL),
    )
    if label:
        lbl = T(label, 24, C_SIGNAL).next_to(beam, RIGHT, buff=0.18).shift(UP * 0.18)
        beam.add(lbl)
        beam.lbl = lbl
    return beam


def make_nfkb_complex(center, scale=1.0):
    """Teal NF-kappaB capsule shape."""
    box = RoundedRectangle(
        corner_radius=0.26 * scale, width=1.65 * scale, height=0.62 * scale,
        stroke_color=C_DECODER, stroke_width=3.0,
        fill_color=C_DECODER, fill_opacity=0.22,
    )
    lbl = T("NF-κB", max(24, int(round(26 * scale))), C_DECODER).move_to(box)
    return VGroup(box, lbl).move_to(center)


def make_ikb_clamp(center, name="IκB", scale=1.0):
    """Coral IkappaB clamp bracket wrapping NF-kappaB with high-contrast dark backing."""
    w, h = 2.08 * scale, 1.04 * scale
    c_rect = RoundedRectangle(
        corner_radius=0.32 * scale, width=w, height=h,
        stroke_color=C_BRAKE, stroke_width=4.0,
        fill_color=C_BRAKE, fill_opacity=0.12,
    ).move_to(center)
    backing = RoundedRectangle(
        corner_radius=0.12, width=1.1, height=0.44,
        stroke_width=0, fill_color=BG, fill_opacity=0.96,
    )
    tag = boxed_label(name, C_BRAKE, size=24, pad=0.10, stroke=2.5, fill_opacity=0.18)
    backing.match_width(tag).match_height(tag)
    tag_pos = center + UP * (h * 0.5 + 0.26)
    backing.move_to(tag_pos)
    tag.move_to(tag_pos)
    g = VGroup(c_rect, backing, tag)
    g.ring = c_rect
    g.tag = VGroup(backing, tag)
    return g


def make_akap_and_pka(anchor_x=-3.1, y_mem=1.55, pka_color=C_DECODER, label_akap=True, with_cradle=True):
    """AKAP anchor cradle tethered to membrane, holding PKA without touching PKA's box."""
    pka_c = np.array([anchor_x, y_mem - 1.15, 0.0])
    pka_body = RoundedRectangle(
        corner_radius=0.28, width=1.15, height=0.62,
        stroke_color=pka_color, stroke_width=3.0,
        fill_color=pka_color, fill_opacity=0.22,
    ).move_to(pka_c)
    pka_lbl = T("PKA", 26, pka_color).move_to(pka_body)
    pka = VGroup(pka_body, pka_lbl)

    if with_cradle:
        # Radius 0.78 > half-diag of 1.15x0.62 (0.653) so cradle clears PKA box cleanly;
        # stem joins cradle smoothly at PI/2 (top of arc: pka_c[1] + 0.78 = y_mem - 0.37)
        stem = Line([anchor_x, y_mem, 0], [anchor_x, y_mem - 0.37, 0], color=C_STRUCT, stroke_width=6)
        stem.set_cap_style(CapStyleType.ROUND)
        cradle = Arc(
            radius=0.78, start_angle=PI / 2, angle=1.5 * PI,
            arc_center=pka_c,
            color=C_STRUCT, stroke_width=6,
        )
        cradle.set_cap_style(CapStyleType.ROUND)
        akap_shape = VGroup(stem, cradle)
    else:
        stem = Line([anchor_x, y_mem, 0], [anchor_x, pka_body.get_top()[1] + 0.02, 0], color=C_STRUCT, stroke_width=7)
        bar = Line([anchor_x - 0.35, pka_body.get_top()[1] + 0.04, 0], [anchor_x + 0.35, pka_body.get_top()[1] + 0.04, 0], color=C_STRUCT, stroke_width=6)
        akap_shape = VGroup(stem, bar)

    g = VGroup(akap_shape, pka)
    g.akap_shape = akap_shape
    g.pka = pka
    g.pka_body = pka_body
    g.pka_lbl = pka_lbl
    if label_akap:
        akap_lbl = T("AKAP", 24, C_TEXT).move_to([anchor_x + 0.85, y_mem - 0.42, 0])
        g.add(akap_lbl)
        g.akap_lbl = akap_lbl
    return g


def make_channel(x=-4.6, y_mem=1.65, active=False, label="Channel"):
    """Membrane channel pair spanning the bilayer."""
    col = C_ACTIVE if active else C_STRUCT
    gap = 0.22 if active else 0.08
    left_sub = RoundedRectangle(corner_radius=0.08, width=0.26, height=0.62, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).move_to([x - 0.14 - gap / 2, y_mem, 0])
    right_sub = RoundedRectangle(corner_radius=0.08, width=0.26, height=0.62, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).move_to([x + 0.14 + gap / 2, y_mem, 0])
    g = VGroup(left_sub, right_sub)
    if label:
        lbl = T(label, 24, col if active else C_TEXT).next_to(g, UP, buff=0.22)
        g.add(lbl)
        g.lbl = lbl
    g.left_sub, g.right_sub = left_sub, right_sub
    return g


def make_glass_slide_frame(center=(0.0, -0.05, 0.0), width=12.2, height=5.5, badge="Glass slide: purified proteins, no cell", bilayer_frac=0.22):
    """Crisp inset frame for the purified protein reconstitution experiments."""
    c = np.array(center, dtype=float)
    frame = RoundedRectangle(
        corner_radius=0.22, width=width, height=height,
        stroke_color=C_TEXT, stroke_width=3.0,
        fill_color="#121722", fill_opacity=0.96,
    ).move_to(c)
    top_y = c[1] + height / 2.0
    pill = boxed_label(badge, C_TEXT, size=26, pad=0.14, stroke=2.5, fill_opacity=0.18)
    pill.move_to([c[0] - width / 2.0 + pill.width / 2.0 + 0.25, top_y + 0.44, 0])
    by = c[1] + height * bilayer_frac
    bx0, bx1 = c[0] - width / 2.0 + 0.45, c[0] + width / 2.0 - 0.45
    b1 = Line([bx0, by + 0.07, 0], [bx1, by + 0.07, 0], color=C_STRUCT, stroke_width=4)
    b2 = Line([bx0, by - 0.07, 0], [bx1, by - 0.07, 0], color=C_STRUCT, stroke_width=3)
    bilayer_lbl = T("Artificial bilayer", 24, C_TEXT).move_to([bx1 - 1.35, by + 0.30, 0])
    g = VGroup(frame, pill, b1, b2, bilayer_lbl)
    g.frame = frame
    g.pill = pill
    g.bilayer_y = by
    g.bx0, g.bx1 = bx0, bx1
    return g


def make_lat_cluster_backdrop(slide_center=(0.0, 0.72, 0.0), slide_w=12.0, slide_h=4.65, seed=19):
    """Build the coalesced LAT cluster + drifting kinases inside + bouncing phosphatases outside."""
    slide = make_glass_slide_frame(center=slide_center, width=slide_w, height=slide_h, bilayer_frac=0.31)
    cc = np.array([slide_center[0], slide_center[1] - 0.50, 0.0])
    rx, ry = 2.40, 1.12

    cluster_fill = Ellipse(
        width=2 * rx, height=2 * ry,
        stroke_color=C_DECODER, stroke_width=3.5,
        fill_color=C_DECODER, fill_opacity=0.18,
    ).move_to(cc)
    # Place LAT cluster label cleanly between cluster top (cc[1]+ry) and bilayer (slide.bilayer_y)
    cluster_lbl = T("LAT cluster", 26, C_DECODER).move_to([cc[0], cc[1] + ry + 0.25, 0])

    rng = np.random.default_rng(seed)
    lat_pts = [cc + np.array([rng.uniform(-1.25, 1.25), rng.uniform(-0.55, 0.55), 0.0]) for _ in range(5)]
    lat_dots = VGroup(*[Dot(p, radius=0.09, color=C_DECODER).set_opacity(0.75) for p in lat_pts])
    weak_lines = VGroup()
    for i in range(len(lat_pts)):
        for j in range(i + 1, len(lat_pts)):
            if np.linalg.norm(lat_pts[i] - lat_pts[j]) < 1.8:
                weak_lines.add(DashedLine(lat_pts[i], lat_pts[j], color=C_DECODER, stroke_width=2.0, dash_length=0.10).set_opacity(0.55))

    kinases = VGroup()
    for k in range(6):
        ang = k * TAU / 6.0 + 0.3
        p0 = cc + np.array([0.85 * np.cos(ang), 0.42 * np.sin(ang), 0.0])
        blk = RoundedRectangle(corner_radius=0.10, width=0.42, height=0.30, stroke_color=C_ACTIVE, stroke_width=2.5, fill_color=C_ACTIVE, fill_opacity=0.78).move_to(p0)
        blk._cx, blk._cy = cc[0], cc[1]
        blk._rx, blk._ry = rx - 0.40, ry - 0.30
        blk._phase = k * 1.05
        blk._freq = 1.1 + 0.18 * (k % 3)
        kinases.add(blk)

    phosphatases = VGroup()
    outside_anchors = [
        cc + np.array([-3.7, 0.45, 0.0]),
        cc + np.array([-4.4, -0.25, 0.0]),
        cc + np.array([-3.5, -0.75, 0.0]),
        cc + np.array([3.7, 0.45, 0.0]),
        cc + np.array([4.4, -0.25, 0.0]),
        cc + np.array([3.5, -0.75, 0.0]),
    ]
    for idx, base in enumerate(outside_anchors):
        blk = RoundedRectangle(corner_radius=0.10, width=0.46, height=0.32, stroke_color=C_BRAKE, stroke_width=2.5, fill_color=C_BRAKE, fill_opacity=0.78).move_to(base)
        blk._base = base.copy()
        blk._dir = -1.0 if idx < 3 else 1.0
        blk._phase = idx * 0.9
        blk._cc = cc.copy()
        blk._rx = rx
        phosphatases.add(blk)

    kin_tag = boxed_label("Kinases in", C_ACTIVE, size=24, pad=0.12, stroke=2.5, fill_opacity=0.22)
    kin_tag.move_to([cc[0], cc[1] - ry - 0.30, 0])
    phos_tag = boxed_label("Phosphatases out", C_BRAKE, size=24, pad=0.12, stroke=2.5, fill_opacity=0.22)
    phos_tag.move_to([slide_center[0] - slide_w / 2.0 + phos_tag.width / 2.0 + 0.35, slide.bilayer_y + 0.48, 0])

    g = VGroup(slide, cluster_fill, weak_lines, lat_dots, kinases, phosphatases, cluster_lbl, kin_tag, phos_tag)
    g.slide = slide
    g.cluster_fill = cluster_fill
    g.kinases = kinases
    g.phosphatases = phosphatases
    g.cluster_lbl = cluster_lbl
    g.kin_tag = kin_tag
    g.phos_tag = phos_tag
    g.cc = cc
    g.rx = rx
    g.ry = ry
    return g


def attach_cluster_particle_updaters(g, kinases=True, phosphatases=True):
    """Attach computed kinematics updaters: kinases circulate inside, phosphatases bounce off rim."""
    if kinases:
        for blk in g.kinases:
            blk._t = 0.0

            def u_kin(m, dt):
                m._t += dt
                ang = m._phase + m._freq * m._t
                rad = 0.55 + 0.25 * np.sin(1.7 * m._t + m._phase)
                m.move_to([m._cx + m._rx * rad * np.cos(ang), m._cy + m._ry * rad * np.sin(ang), 0.0])

            blk.add_updater(u_kin)

    if phosphatases:
        for blk in g.phosphatases:
            blk._t = 0.0

            def u_phos(m, dt):
                m._t += dt
                wave = abs(np.sin(1.45 * m._t + m._phase))
                rim_x = m._cc[0] + m._dir * (m._rx + 0.25)
                far_x = m._cc[0] + m._dir * (m._rx + 1.85)
                x = rim_x + wave * (far_x - rim_x)
                y = m._base[1] + 0.15 * np.sin(2.1 * m._t + m._phase)
                m.move_to([x, y, 0.0])

            blk.add_updater(u_phos)


# ------------------------------------------------------------------
# SCENES
# ------------------------------------------------------------------

class S00Title(TitleCard):
    LESSON = "The Shape of a Signal: Size, Duration, Frequency and Place"
    TITLE = "Making Pulses and Fixing Place"


class S01Hook(SpokenScene):
    def construct(self):
        cell = build_cell(with_labels=True)
        P = Plot(
            box=(1.5, 6.1, -2.0, 2.2),
            xr=(0, 10), yr=(0, 1.3),
            xticks=[], yticks=[(0, "0"), (0.53, "steady"), (1.1, "high")],
            xlabel="time", ylabel="Signal",
        )
        tag = scope_tag("schematic")

        self.play(FadeIn(cell), Create(P), FadeIn(tag), run_time=self.beat(0.08))

        # Beat 1: recap duration & spikes from Film 1
        self.at("how long")
        dur_curve = P.curve(lambda t: 0.9 if 0.5 <= t <= 4.2 else 0.05, x0=0.0, x1=4.8, color=C_DECODER, width=5)
        dur_lbl = T("Duration", 26, C_DECODER).move_to(P.pt(2.4, 1.15))
        self.play(Create(dur_curve), FadeIn(dur_lbl), run_time=1.3)

        self.at("spikes arrived")
        spk_fn = lambda t: 0.05 + 0.95 * sum(np.exp(-((t - tc) / 0.22) ** 2) for tc in (5.6, 7.1, 8.6))
        spk_curve = P.curve(spk_fn, x0=4.8, x1=9.8, color=C_DECODER, width=5)
        spk_lbl = T("Spikes", 26, C_DECODER).move_to(P.pt(7.3, 1.15))
        self.play(Create(spk_curve), FadeIn(spk_lbl), run_time=1.2)

        # Beat 2: steady outside stimulus
        self.at("outside stimulus")
        self.play(FadeOut(dur_curve), FadeOut(dur_lbl), FadeOut(spk_curve), FadeOut(spk_lbl), run_time=0.45)
        beam = build_steady_beam(x=-2.25, y_top=3.38, y_mem=2.68, label="Steady stimulus")
        self.play(FadeIn(beam, shift=DOWN * 0.15), run_time=1.0)

        # Beat 3: pulses from steady stimulus (computed delayed feedback wave)
        self.at("make pulses")
        t_trk = ValueTracker(0.0)
        wave = P.live_curve(lambda t: delay_curve_fn(True)(t), t_trk, color=C_DECODER, width=5)
        dot = P.dot(lambda: t_trk.get_value(), lambda: delay_curve_fn(True)(t_trk.get_value()), color=C_TEXT, ring=C_DECODER)
        pulses_lbl = T("Pulses?", 28, C_DECODER).move_to([3.8, 2.75, 0])
        self.add(wave, dot)
        self.play(FadeIn(pulses_lbl), t_trk.animate.set_value(4.8), run_time=1.05, rate_func=linear)

        # Beat 4: local signal on membrane + question mark (clear of Cytoplasm & Plasma membrane)
        self.at("keep one signal local")
        local_spot = Circle(radius=0.38, stroke_color=C_SIGNAL, stroke_width=3.5, fill_color=C_SIGNAL, fill_opacity=0.30).move_to([-5.05, 2.15, 0])
        local_lbl = T("Local?", 28, C_SIGNAL).move_to([-5.05, 1.15, 0])
        qmark = T("?", 52, C_TEXT, weight=BOLD).move_to([0.85, 0.25, 0])
        self.play(
            FadeIn(local_spot), FadeIn(local_lbl), FadeIn(qmark),
            t_trk.animate.set_value(8.0),
            run_time=1.5, rate_func=linear,
        )

        # Beat 5: wire loops and organize space
        self.at("wire loops")
        loop_ring = DashedVMobject(
            Arc(radius=0.58, start_angle=0.2, angle=TAU - 0.6, arc_center=np.array([-2.95, 0.80, 0]), color=C_DECODER, stroke_width=3.5),
            num_dashes=16,
        )
        loop_lbl = T("Loops", 26, C_DECODER).move_to([-2.95, -0.05, 0])
        self.play(
            Create(loop_ring), FadeIn(loop_lbl),
            t_trk.animate.set_value(10.0),
            run_time=1.1, rate_func=linear,
        )

        self.at("organize space")
        space_ring = DashedVMobject(Circle(radius=0.56, color=C_SIGNAL, stroke_width=3.0).move_to(local_spot), num_dashes=16)
        self.play(Create(space_ring), run_time=0.8)
        self.finish()


class S02DelayFeedback(SpokenScene):
    def construct(self):
        cell = build_cell(with_labels=False)
        cell_lbl = T("Cell pathway", 26, C_TEXT).move_to([-2.95, 3.12, 0])

        act_chip = boxed_label("Active", C_DECODER, size=28, pad=0.18)
        act_chip.move_to([-2.95, 1.48, 0])
        brake_arc = CurvedArrow(
            np.array([-2.15, 1.22, 0]), np.array([-3.75, 1.22, 0]),
            angle=-1.55, color=C_BRAKE, stroke_width=5,
        )
        brake_lbl = T("Negative feedback", 24, C_BRAKE).move_to([-2.95, 0.05, 0])

        # Live level bars inside nucleus showing computed Active A(t) and Brake B(t)
        a_gauge_bg = RoundedRectangle(corner_radius=0.06, width=2.8, height=0.28, stroke_color=C_DECODER, stroke_width=2.0, fill_color=BG, fill_opacity=0.85).move_to([-2.55, -1.25, 0])
        b_gauge_bg = RoundedRectangle(corner_radius=0.06, width=2.8, height=0.28, stroke_color=C_BRAKE, stroke_width=2.0, fill_color=BG, fill_opacity=0.85).move_to([-2.55, -1.85, 0])
        a_glbl = T("Active", 22, C_DECODER).next_to(a_gauge_bg, LEFT, buff=0.14)
        b_glbl = T("Brake", 22, C_BRAKE).next_to(b_gauge_bg, LEFT, buff=0.14)

        P = Plot(
            box=(1.5, 6.1, -2.0, 2.2),
            xr=(0, 12), yr=(0, 1.3),
            xticks=[], yticks=[(0, "0"), (_A_STEADY, "steady"), (1.1, "high")],
            xlabel="time", ylabel="Activity",
        )
        steady_line = DashedLine(P.pt(0, _A_STEADY), P.pt(12, _A_STEADY), color=C_STRUCT, stroke_width=2.5)
        tag = scope_tag("schematic")

        self.play(
            FadeIn(cell), FadeIn(cell_lbl), FadeIn(act_chip),
            FadeIn(a_gauge_bg), FadeIn(b_gauge_bg), FadeIn(a_glbl), FadeIn(b_glbl),
            Create(P), FadeIn(steady_line), FadeIn(tag),
            run_time=self.beat(0.06),
        )

        # Beat 1: No delay settles flat immediately
        t0 = ValueTracker(0.0)
        nodelay_live = P.live_curve(delay_curve_fn(False), t0, color=C_STRUCT, width=4)
        a_bar0 = always_redraw(lambda: Rectangle(width=max(0.04, 2.72 * min(1.0, delay_curve_fn(False)(t0.get_value()) / 1.15)), height=0.20, stroke_width=0, fill_color=C_DECODER, fill_opacity=0.85).move_to(a_gauge_bg).align_to(a_gauge_bg, LEFT).shift(RIGHT * 0.04))
        b_bar0 = always_redraw(lambda: Rectangle(width=max(0.04, 2.72 * min(1.0, delay_curve_fn(False)(t0.get_value()) / 1.15)), height=0.20, stroke_width=0, fill_color=C_BRAKE, fill_opacity=0.85).move_to(b_gauge_bg).align_to(b_gauge_bg, LEFT).shift(RIGHT * 0.04))
        # Legend placed cleanly above the plot so curves never cross it
        nodelay_lbl = T("— No delay", 24, C_TEXT).move_to([5.35, 2.72, 0])
        self.add(nodelay_live, a_bar0, b_bar0)
        self.play(Create(brake_arc), FadeIn(brake_lbl), FadeIn(nodelay_lbl), run_time=0.5)
        self.play(t0.animate.set_value(12.0), run_time=3.1, rate_func=linear)
        self.remove(nodelay_live, a_bar0, b_bar0)
        nodelay_dashed = DashedVMobject(P.curve(delay_curve_fn(False), color=C_STRUCT, width=4), num_dashes=36)
        self.add(nodelay_dashed)

        # Beat 2: Add a delay -> clock icon on feedback loop with rotating hand
        self.at("Add a delay")
        clock_c = np.array([-2.95, 0.35, 0.0])
        clock_face = Circle(radius=0.30, stroke_color=C_BRAKE, stroke_width=3.5, fill_color=BG, fill_opacity=0.95).move_to(clock_c)
        clock_hr = Line(clock_c, clock_c + UP * 0.16, color=C_TEXT, stroke_width=3)
        clock_hand = Line(clock_c, clock_c + RIGHT * 0.21, color=C_BRAKE, stroke_width=3)
        clock = VGroup(clock_face, clock_hr, clock_hand)
        delay_lbl = T("Delay", 26, C_BRAKE).move_to([-2.95, -0.22, 0])
        withdelay_lbl = T("— With delay", 24, C_DECODER).move_to([3.45, 2.72, 0])
        self.play(
            FadeOut(brake_lbl, run_time=0.3), FadeIn(clock), FadeIn(delay_lbl), FadeIn(withdelay_lbl),
            run_time=0.75,
        )

        # Beat 3: Computed delayed feedback curve + synchronized brake pulse + rotating clock hand + live gauges
        self.at("arrives late")
        t1 = ValueTracker(0.0)
        delay_live = P.live_curve(delay_curve_fn(True), t1, color=C_DECODER, width=5)
        dot = P.dot(lambda: t1.get_value(), lambda: delay_curve_fn(True)(t1.get_value()), color=C_TEXT, ring=C_DECODER)
        a_bar1 = always_redraw(lambda: Rectangle(width=max(0.04, 2.72 * min(1.0, delay_curve_fn(True)(t1.get_value()) / 1.15)), height=0.20, stroke_width=0, fill_color=C_DECODER, fill_opacity=0.85).move_to(a_gauge_bg).align_to(a_gauge_bg, LEFT).shift(RIGHT * 0.04))
        b_bar1 = always_redraw(lambda: Rectangle(width=max(0.04, 2.72 * min(1.0, delay_brake_val(t1.get_value()) / 1.15)), height=0.20, stroke_width=0, fill_color=C_BRAKE, fill_opacity=0.85).move_to(b_gauge_bg).align_to(b_gauge_bg, LEFT).shift(RIGHT * 0.04))

        def brake_sync(m):
            b = delay_brake_val(t1.get_value())
            m.set_stroke(width=3.0 + 7.0 * min(1.0, b / 1.1))

        def clock_sync(m):
            ang = -1.6 * t1.get_value()
            m.put_start_and_end_on(clock_c, clock_c + 0.22 * np.array([np.cos(ang), np.sin(ang), 0.0]))

        brake_arc.add_updater(brake_sync)
        clock_hand.add_updater(clock_sync)

        self.add(delay_live, dot, a_bar1, b_bar1)
        self.play(t1.animate.set_value(1.85), run_time=3.5, rate_func=linear)

        # Beat 4: Overshoot too hot, then too cold
        self.at("overshoot too hot")
        hot_lbl = T("too hot", 24, C_SIGNAL).move_to(P.pt(1.85, 1.24))
        self.play(FadeIn(hot_lbl, run_time=0.25), t1.animate.set_value(3.2), run_time=1.2, rate_func=linear)

        self.at("then too cold")
        cold_lbl = T("too cold", 24, C_DECODER).move_to([3.92, -1.74, 0])
        self.play(FadeIn(cold_lbl, run_time=0.2), t1.animate.set_value(4.13), run_time=1.4, rate_func=linear)

        # Beat 5: Strong feedback + short-lived proteins -> repeating pulses
        self.at("feedback is strong")
        self.play(FadeOut(hot_lbl, run_time=0.25), FadeOut(cold_lbl, run_time=0.25), t1.animate.set_value(8.5), run_time=2.8, rate_func=linear)
        self.at("rise and fall in pulses")
        self.play(t1.animate.set_value(12.0), run_time=2.5, rate_func=linear)
        brake_arc.remove_updater(brake_sync)
        clock_hand.remove_updater(clock_sync)
        self.finish()


class S03NfkbLoop(SpokenScene):
    def construct(self):
        cell = build_cell(with_labels=True)
        dock_x, dock_y = cell.cx + 0.55, -1.62
        gene_bar = RoundedRectangle(
            corner_radius=0.10, width=2.2, height=0.44,
            stroke_color=C_STRUCT, stroke_width=2.5,
            fill_color=C_STRUCT, fill_opacity=0.20,
        ).move_to([cell.cx + 0.35, -2.42, 0])
        gene_lbl = T("IκBα gene", 24, C_TEXT).move_to(gene_bar)
        gene = VGroup(gene_bar, gene_lbl)

        nfkb = make_nfkb_complex([cell.cx, 0.72, 0])
        ikb = make_ikb_clamp([cell.cx, 0.72, 0], name="IκB")

        P = Plot(
            box=(1.5, 6.1, -1.2, 2.2),
            xr=(0, 14), yr=(-0.22, 1.38),
            xticks=[], yticks=[(-0.15, "low"), (1.1, "high")],
            xlabel="time", ylabel="Nuclear NF-κB",
        )
        tag = scope_tag("schematic")

        bar_bg = RoundedRectangle(corner_radius=0.10, width=4.2, height=0.40, stroke_color=C_BRAKE, stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to([3.8, -2.55, 0])
        bar_lbl = T("IκBα synthesis delay", 24, C_TEXT).next_to(bar_bg, UP, buff=0.14)
        prog = ValueTracker(0.0)
        bar_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.08,
            width=max(0.08, 4.12 * prog.get_value()),
            height=0.32,
            stroke_width=0,
            fill_color=C_BRAKE,
            fill_opacity=0.80 if prog.get_value() > 0.02 else 0.0,
        ).move_to(bar_bg).align_to(bar_bg, LEFT).shift(RIGHT * 0.04))

        t_trk = ValueTracker(0.0)
        live = P.live_curve(nfkb_n_fn, t_trk, color=C_ACTIVE, width=5)
        dot = P.dot(lambda: t_trk.get_value(), lambda: nfkb_n_fn(t_trk.get_value()), color=C_TEXT, ring=C_ACTIVE, radius=0.10)

        self.play(FadeIn(cell), FadeIn(gene), FadeIn(nfkb), FadeIn(ikb), Create(P), FadeIn(tag), run_time=self.beat(0.06))
        self.add(live, dot)

        # Beat 1: Steady signal triggers destruction of IkappaB
        self.at("steady signal")
        beam = build_steady_beam(x=-2.25, y_top=3.38, y_mem=2.68, label="Steady signal")
        self.play(FadeIn(beam, shift=DOWN * 0.15), run_time=0.9)

        self.at("destruction")
        pieces = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.55, height=0.28, stroke_color=C_BRAKE, stroke_width=2.5, fill_color=C_BRAKE, fill_opacity=0.55)
            .move_to(ikb.ring.get_center() + d * 0.4)
            for d in (UL, UR, DL, DR)
        ])
        self.play(FadeOut(ikb.tag, run_time=0.35), ReplacementTransform(ikb.ring, pieces), run_time=0.85)
        self.play(
            pieces[0].animate.shift(UL * 0.45).set_opacity(0),
            pieces[1].animate.shift(UR * 0.45).set_opacity(0),
            pieces[2].animate.shift(DL * 0.45).set_opacity(0),
            pieces[3].animate.shift(DR * 0.45).set_opacity(0),
            nfkb.animate.shift(DOWN * 0.25),
            t_trk.animate.set_value(0.55),
            run_time=1.1, rate_func=linear,
        )
        self.remove(pieces)

        # Beat 2: Free NF-kappaB enters the nucleus & curve climbs
        self.at("enter the nucleus")
        self.play(
            nfkb.animate.move_to([dock_x, dock_y, 0]),
            t_trk.animate.set_value(2.6),
            run_time=2.0, rate_func=linear,
        )

        # Beat 3: Activation builds its own brake -> docks & lights gene
        self.at("activation builds")
        self.play(
            gene_bar.animate.set_fill(C_ACTIVE, opacity=0.45).set_stroke(C_ACTIVE, width=3.5),
            gene_lbl.animate.set_color(C_ACTIVE),
            t_trk.animate.set_value(2.8),
            run_time=1.2,
        )

        # Beat 4: Switches on IkappaBalpha gene, synthesis delay bar fills, fresh IkappaBalpha appears
        self.at("switches on the gene")
        self.play(FadeIn(bar_bg), FadeIn(bar_lbl), run_time=0.5)
        self.add(bar_fill)
        self.play(
            prog.animate.set_value(1.0),
            t_trk.animate.set_value(3.0),
            run_time=3.2, rate_func=linear,
        )

        self.at("which takes time")
        fresh_ikb = make_ikb_clamp([cell.cx + 1.45, 0.25, 0], name="IκBα", scale=0.82)
        self.play(FadeIn(fresh_ikb, scale=0.85), run_time=0.8)
        self.finish()


class S04NfkbOscillate(SpokenScene):
    def construct(self):
        cell = build_cell(with_labels=True)
        dock_x, dock_y = cell.cx + 0.55, -1.62
        gene_bar = RoundedRectangle(
            corner_radius=0.10, width=2.2, height=0.44,
            stroke_color=C_ACTIVE, stroke_width=3.5,
            fill_color=C_ACTIVE, fill_opacity=0.45,
        ).move_to([cell.cx + 0.35, -2.42, 0])
        gene_lbl = T("IκBα gene", 24, C_ACTIVE).move_to(gene_bar)
        gene = VGroup(gene_bar, gene_lbl)

        beam = build_steady_beam(x=-2.25, y_top=3.38, y_mem=2.68, label="Steady signal")
        nfkb = make_nfkb_complex([dock_x, dock_y, 0])
        fresh_ikb = make_ikb_clamp([cell.cx + 1.45, 0.25, 0], name="IκBα", scale=0.82)

        P = Plot(
            box=(1.5, 6.1, -1.2, 2.2),
            xr=(0, 14), yr=(-0.22, 1.38),
            xticks=[], yticks=[(-0.15, "low"), (1.1, "high")],
            xlabel="time", ylabel="Nuclear NF-κB",
        )
        tag = scope_tag("schematic")
        tag.set_z_index(10)

        t_trk = ValueTracker(3.0)
        live = P.live_curve(nfkb_n_fn, t_trk, color=C_ACTIVE, width=5)
        dot = P.dot(lambda: t_trk.get_value(), lambda: nfkb_n_fn(t_trk.get_value()), color=C_TEXT, ring=C_ACTIVE, radius=0.10)
        self.add(cell, gene, beam, nfkb, fresh_ikb, P, live, dot, tag)

        # Beat 1: Fresh IkappaBalpha enters nucleus and binds NF-kappaB cleanly inside nucleus
        self.at("binds")
        target_ikb = make_ikb_clamp([dock_x, dock_y, 0], name="IκBα", scale=1.0)
        self.play(Transform(fresh_ikb, target_ikb), run_time=1.0)

        # Beat 2: Pulls NF-kappaB back out to cytoplasm, curve drops
        self.at("pulls it back out")
        complex_grp = VGroup(nfkb, fresh_ikb)
        self.play(
            complex_grp.animate.shift(np.array([cell.cx - dock_x, 0.72 - dock_y, 0.0])),
            gene_bar.animate.set_fill(C_STRUCT, opacity=0.20).set_stroke(C_STRUCT, width=2.5),
            gene_lbl.animate.set_color(C_TEXT),
            t_trk.animate.set_value(6.2),
            run_time=1.4, rate_func=linear,
        )

        # Beat 3: Steady stimulus stays on -> new inhibitor breaks down too
        self.at("breaks down too")
        pieces = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.55, height=0.28, stroke_color=C_BRAKE, stroke_width=2.5, fill_color=C_BRAKE, fill_opacity=0.55)
            .move_to(fresh_ikb.ring.get_center() + d * 0.4)
            for d in (UL, UR, DL, DR)
        ])
        self.play(FadeOut(fresh_ikb.tag, run_time=0.3), ReplacementTransform(fresh_ikb.ring, pieces), run_time=0.65)
        self.play(
            pieces[0].animate.shift(UL * 0.45).set_opacity(0),
            pieces[1].animate.shift(UR * 0.45).set_opacity(0),
            pieces[2].animate.shift(DL * 0.45).set_opacity(0),
            pieces[3].animate.shift(DR * 0.45).set_opacity(0),
            t_trk.animate.set_value(7.4),
            run_time=0.7, rate_func=linear,
        )
        self.remove(pieces)

        # Beat 4: Second pulse on trace + synchronized nuclear entry/exit driven by nfkb_n_fn(t_trk)
        self.at("starting the next pulse")

        def move_nfkb(m):
            val = nfkb_n_fn(t_trk.get_value())
            s = 1.0 / (1.0 + np.exp(-14.0 * (val - 0.45)))
            x = cell.cx + (dock_x - cell.cx) * s
            y = 0.72 + (dock_y - 0.72) * s
            m.move_to([x, y, 0.0])

        nfkb.add_updater(move_nfkb)
        self.play(
            gene_bar.animate.set_fill(C_ACTIVE, opacity=0.45).set_stroke(C_ACTIVE, width=3.5),
            gene_lbl.animate.set_color(C_ACTIVE),
            t_trk.animate.set_value(10.15),
            run_time=0.85, rate_func=linear,
        )
        self.play(
            gene_bar.animate.set_fill(C_STRUCT, opacity=0.20).set_stroke(C_STRUCT, width=2.5),
            gene_lbl.animate.set_color(C_TEXT),
            t_trk.animate.set_value(11.8),
            run_time=0.70, rate_func=linear,
        )
        self.play(
            t_trk.animate.set_value(14.0),
            run_time=0.70, rate_func=linear,
        )
        nfkb.clear_updaters()

        # Beat 5: Cleanly transition into zoomed plasma membrane (tag stays on top!)
        self.at("Now stay in the cell")
        self.remove(live, dot)
        right_stuff = VGroup(P, P.curve(nfkb_n_fn, x0=0, x1=14, color=C_ACTIVE, width=5))
        mem_zoom = build_plasma_membrane_zoom(y_mem=1.65)
        self.play(
            FadeOut(right_stuff, run_time=0.45),
            FadeOut(beam, run_time=0.45),
            FadeOut(VGroup(cell, gene, nfkb), run_time=0.55),
            FadeIn(mem_zoom, run_time=0.8),
            run_time=1.0,
        )
        self.bring_to_front(tag)
        self.finish()


class S05AkapPlace(SpokenScene):
    def construct(self):
        mem = build_plasma_membrane_zoom(y_mem=1.65)
        tag = scope_tag("schematic")

        ch_left = make_channel(x=-4.4, y_mem=1.65, active=False, label="Channel")
        ch_right = make_channel(x=4.4, y_mem=1.65, active=False, label="Other target")
        self.add(mem, tag)
        self.play(FadeIn(ch_left), run_time=1.4)
        self.play(FadeIn(ch_right), run_time=1.4)

        # Show two local-activity meters at bottom (revealed when cAMP is narrated)
        g_l_bg = RoundedRectangle(corner_radius=0.08, width=2.6, height=0.28, stroke_color=C_SIGNAL, stroke_width=2.0, fill_color=BG, fill_opacity=0.85).move_to([-3.1, -2.05, 0])
        g_l_lbl = T("Local cAMP", 22, C_SIGNAL).next_to(g_l_bg, UP, buff=0.10)
        g_r_bg = RoundedRectangle(corner_radius=0.08, width=2.6, height=0.28, stroke_color=C_SIGNAL, stroke_width=2.0, fill_color=BG, fill_opacity=0.85).move_to([3.3, -2.05, 0])
        g_r_lbl = T("Distant cAMP", 22, C_SIGNAL).next_to(g_r_bg, UP, buff=0.10)
        camp_level = ValueTracker(0.0)
        g_l_fill = always_redraw(lambda: Rectangle(width=max(0.04, 2.52 * camp_level.get_value()), height=0.20, stroke_width=0, fill_color=C_SIGNAL, fill_opacity=0.90 if camp_level.get_value() > 0.02 else 0.0).move_to(g_l_bg).align_to(g_l_bg, LEFT).shift(RIGHT * 0.04).set_z_index(2))
        g_l_fill.set_z_index(2)

        # Beat 1: Anchoring protein parks PKA beside one membrane channel
        self.at("anchoring protein")
        akap_left = make_akap_and_pka(anchor_x=-3.1, y_mem=1.55, pka_color=C_DECODER, label_akap=True)
        self.play(FadeIn(akap_left.akap_shape), FadeIn(akap_left.akap_lbl), run_time=0.80)

        self.at("parks the kinase")
        self.play(FadeIn(akap_left.pka, shift=UP * 0.2), run_time=1.1)

        pka_right_box = RoundedRectangle(
            corner_radius=0.28, width=1.15, height=0.62,
            stroke_color=C_DECODER, stroke_width=3.0,
            fill_color=C_DECODER, fill_opacity=0.22,
        ).move_to([3.3, 0.35, 0])
        pka_right_lbl = T("PKA", 26, C_DECODER).move_to(pka_right_box)
        pka_right = VGroup(pka_right_box, pka_right_lbl)
        self.play(FadeIn(pka_right), run_time=1.0)

        # Beat 2: Local cloud of cAMP confined below membrane & away from AKAP/Channel labels
        self.at("local cloud")
        rng = np.random.default_rng(7)
        src = np.array([-3.75, 1.10, 0.0])
        n_camp = 46
        camp_dots = VGroup()
        for k in range(n_camp):
            d = Dot(src.copy(), radius=0.085, color=C_SIGNAL).set_opacity(0.95)
            d._pos = src.copy()
            d._age = rng.uniform(0.0, 2.0)
            d._max_age = rng.uniform(1.6, 2.8)
            camp_dots.add(d)

        cloud_halo = Circle(radius=1.22, stroke_width=0, fill_color=C_SIGNAL, fill_opacity=0.16).move_to([-3.75, 0.22, 0])
        cloud_ring = DashedVMobject(Circle(radius=1.22, stroke_color=C_SIGNAL, stroke_width=2.5).move_to([-3.75, 0.22, 0]), num_dashes=28)
        camp_lbl = T("cAMP", 26, C_SIGNAL).move_to([-5.45, 0.22, 0])

        def step_camp(m, dt):
            m._age += dt
            if m._age >= m._max_age:
                m._age = 0.0
                m._pos = src + np.array([rng.uniform(-0.25, 0.25), rng.uniform(-0.20, 0.0), 0.0])
            else:
                step = rng.normal(0.0, 1.15 * np.sqrt(max(dt, 1e-3)), size=2)
                nxt = m._pos + np.array([step[0], step[1], 0.0])
                if nxt[1] > 1.32:
                    nxt[1] = 1.32 - (nxt[1] - 1.32)
                offset = nxt - np.array([-3.75, 0.22, 0.0])
                if np.linalg.norm(offset) > 1.12:
                    nxt -= 0.30 * offset
                m._pos = nxt
            m.move_to(m._pos)
            m.set_opacity(0.95 * (1.0 - 0.50 * (m._age / m._max_age)))

        for d in camp_dots:
            d.add_updater(step_camp)

        cloud_halo.set_z_index(-2)
        cloud_ring.set_z_index(-2)
        camp_dots.set_z_index(-1)
        self.add(cloud_halo, cloud_ring, camp_dots, g_l_fill)
        self.play(
            FadeIn(g_l_bg), FadeIn(g_l_lbl), FadeIn(g_r_bg), FadeIn(g_r_lbl),
            FadeIn(cloud_halo), FadeIn(cloud_ring), FadeIn(camp_lbl),
            camp_level.animate.set_value(0.92),
            run_time=1.3,
        )

        # Beat 3: Switches on nearby PKA and its channel (turn bright GREEN)
        self.at("switches on")
        ch_left_on = make_channel(x=-4.4, y_mem=1.65, active=True, label="Channel")
        self.play(
            akap_left.pka_body.animate.set_stroke(C_ACTIVE).set_fill(C_ACTIVE, opacity=0.35),
            akap_left.pka_lbl.animate.set_color(C_ACTIVE),
            Transform(ch_left, ch_left_on),
            run_time=1.5,
        )

        # Beat 4: Identical PKA across the cell never sees it
        self.at("Identical PKA")
        ring_far = DashedVMobject(Circle(radius=0.88, color=C_TEXT, stroke_width=2.5).move_to(pka_right), num_dashes=18)
        self.play(Create(ring_far), run_time=1.4)
        self.finish()


class S06LatSlide(SpokenScene):
    def construct(self):
        # Continue seamlessly from S05 plasma membrane with subtle motion before opening glass slide
        mem = build_plasma_membrane_zoom(y_mem=1.65)
        ch_left = make_channel(x=-4.4, y_mem=1.65, active=True, label="Channel")
        ch_right = make_channel(x=4.4, y_mem=1.65, active=False, label="Other target")
        akap_left = make_akap_and_pka(anchor_x=-3.1, y_mem=1.55, pka_color=C_ACTIVE, label_akap=True)
        spot_badge = boxed_label("Signaling spot on demand", C_DECODER, size=26, pad=0.14).move_to([0.0, -0.35, 0])
        tag = scope_tag("schematic")
        self.add(mem, ch_left, ch_right, akap_left, tag)
        self.play(FadeIn(spot_badge, shift=UP * 0.2), run_time=1.4)

        self.at("glass slide")
        slide = make_glass_slide_frame(center=(0.0, -0.05, 0.0), width=12.2, height=5.5)
        self.play(
            FadeOut(VGroup(mem, ch_left, ch_right, akap_left, spot_badge), run_time=0.45),
            FadeIn(slide, run_time=0.8),
        )

        by = slide.bilayer_y
        tail = Line([-3.45, by, 0], [-3.45, by - 1.85, 0], color=C_TEXT, stroke_width=5)
        tail_lbl = T("Receptor tail", 24, C_TEXT).next_to(tail, LEFT, buff=0.18)
        self.play(Create(tail), FadeIn(tail_lbl), run_time=0.8)

        # Beat 1: Kinase puts phosphate on receptor tail
        self.at("kinase put phosphate")
        kin = boxed_label("Kinase", C_ACTIVE, size=24, pad=0.14).move_to([-1.2, by - 0.95, 0])
        self.play(FadeIn(kin), run_time=0.5)
        self.play(kin.animate.move_to([-1.85, by - 0.95, 0]), run_time=0.6)

        tail_ps = VGroup()
        for py in (by - 0.50, by - 1.05, by - 1.60):
            p = Circle(radius=0.24, stroke_color=C_SIGNAL, stroke_width=2.5, fill_color=C_SIGNAL, fill_opacity=0.85).move_to([-3.05, py, 0])
            ptxt = T("P", 22, BG, weight=BOLD).move_to(p)
            tail_ps.add(VGroup(p, ptxt))
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in tail_ps], lag_ratio=0.25), run_time=1.1)

        # Beat 2: Phosphates reach purified adaptor LAT
        self.at("Phosphates then")
        rng = np.random.default_rng(11)
        init_pts = np.array([
            [-0.1, by - 0.95],
            [0.8, by - 2.05],
            [2.4, by - 0.85],
            [3.9, by - 1.65],
            [1.6, by - 2.95],
            [4.5, by - 0.90],
            [0.2, by - 1.55],
            [3.2, by - 2.20],
            [-0.7, by - 2.45],
            [4.6, by - 2.85],
        ], dtype=float)
        cluster_center = np.array([1.95, by - 1.95])

        mols = VGroup()
        mol_ps = VGroup()
        p_offset = np.array([-0.62, 0.0, 0.0])
        p_init_pts = [
            [-1.20, by - 0.35, 0],
            [-2.40, by - 1.85, 0],
            [-1.85, by - 0.25, 0],
            [-1.75, by - 2.95, 0],
            [-2.45, by - 2.85, 0],
        ]
        for idx, pt in enumerate(init_pts):
            is_lat = idx < 5
            if is_lat:
                body = RoundedRectangle(corner_radius=0.14, width=0.72, height=0.34, stroke_color=C_DECODER, stroke_width=3.0, fill_color=C_DECODER, fill_opacity=0.28).move_to([pt[0], pt[1], 0])
                p_circ = Circle(radius=0.22, stroke_color=C_SIGNAL, stroke_width=2.0, fill_color=C_SIGNAL, fill_opacity=0.90)
                p_txt = T("P", 22, BG, weight=BOLD).move_to(p_circ)
                p_badge = VGroup(p_circ, p_txt).move_to(p_init_pts[idx])
                mol_ps.add(p_badge)
            else:
                body = Circle(radius=0.20, stroke_color=C_DECODER, stroke_width=3.0, fill_color=C_DECODER, fill_opacity=0.22).move_to([pt[0], pt[1], 0])
            mols.add(body)

        lat_lbl = T("LAT", 26, C_DECODER).next_to(mols[0], UP, buff=0.18)
        partners_lbl = T("Partners", 24, C_DECODER).next_to(mols[5], UP, buff=0.18)
        self.play(FadeIn(mols), FadeIn(lat_lbl), FadeIn(partners_lbl), run_time=0.8)

        self.at("adapter LAT")
        self.play(FadeIn(mol_ps, scale=0.7), run_time=0.3)
        self.play(
            LaggedStart(*[
                mol_ps[idx].animate.move_to(mols[idx].get_center() + p_offset)
                for idx in range(5)
            ], lag_ratio=0.12),
            run_time=1.1,
        )

        # Beat 3: Many weak contacts pull LAT and partners into a liquid-like cluster
        self.at("Many weak contacts")
        self.play(FadeOut(lat_lbl, run_time=0.3), FadeOut(partners_lbl, run_time=0.3))

        sim_t = ValueTracker(0.0)
        n_steps = 120
        traj = np.zeros((n_steps, len(init_pts), 2))
        pos = init_pts.copy()
        vel = np.zeros_like(pos)
        for s_i in range(n_steps):
            traj[s_i] = pos
            forces = np.zeros_like(pos)
            for i in range(len(pos)):
                forces[i] += np.array([0.45 * (cluster_center[0] - pos[i, 0]), 1.35 * (cluster_center[1] - pos[i, 1])])
                for j in range(i + 1, len(pos)):
                    diff = pos[j] - pos[i]
                    dist = np.linalg.norm(diff) + 1e-6
                    u = diff / dist
                    if dist < 1.35:
                        f_pair = -2.8 * (1.35 - dist) * u
                    elif dist < 3.6:
                        f_pair = 0.35 * u
                    else:
                        f_pair = np.zeros(2)
                    forces[i] += f_pair
                    forces[j] -= f_pair
                if i < 5:
                    pi = pos[i] + p_offset[:2]
                    for j in range(len(pos)):
                        if i == j:
                            continue
                        targets = [pos[j], pos[j] + p_offset[:2]] if j < 5 else [pos[j]]
                        for pj in targets:
                            d2 = pj - pi
                            dist2 = np.linalg.norm(d2) + 1e-6
                            if dist2 < 0.88:
                                f2 = -4.2 * (0.88 - dist2) * (d2 / dist2)
                                forces[i] += f2
                                forces[j] -= f2
            noise = rng.normal(0.0, 0.14, size=pos.shape)
            vel = 0.72 * vel + 0.045 * forces + 0.03 * noise
            pos = pos + vel

        def interp_pos(idx, frac):
            u = np.clip(frac, 0.0, 1.0) * (n_steps - 1)
            k0 = int(np.floor(u))
            k1 = min(n_steps - 1, k0 + 1)
            a = u - k0
            return (1 - a) * traj[k0, idx] + a * traj[k1, idx]

        for idx, m in enumerate(mols):
            m.add_updater(lambda mob, idx=idx: mob.move_to([interp_pos(idx, sim_t.get_value())[0], interp_pos(idx, sim_t.get_value())[1], 0.0]))
        for idx in range(5):
            mol_ps[idx].add_updater(lambda mob, idx=idx: mob.move_to([interp_pos(idx, sim_t.get_value())[0] + p_offset[0], interp_pos(idx, sim_t.get_value())[1] + p_offset[1], 0.0]))
        mol_ps.set_z_index(4)

        def mk_contacts():
            g = VGroup()
            frac = sim_t.get_value()
            pts = [interp_pos(i, frac) for i in range(len(mols))]
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    if np.linalg.norm(pts[i] - pts[j]) < 1.65:
                        g.add(DashedLine([pts[i][0], pts[i][1], 0], [pts[j][0], pts[j][1], 0], color=C_SIGNAL, stroke_width=2.0, dash_length=0.09).set_opacity(0.65))
            return g

        contacts = always_redraw(mk_contacts)
        droplet = always_redraw(lambda: Ellipse(
            width=5.2,
            height=2.85,
            stroke_color=C_DECODER,
            stroke_width=3.0 * min(1.0, max(0.0, (sim_t.get_value() - 0.35) / 0.65)),
            fill_color=C_DECODER,
            fill_opacity=0.18 * min(1.0, max(0.0, (sim_t.get_value() - 0.35) / 0.65)),
        ).move_to([cluster_center[0], cluster_center[1], 0.0]))

        self.add(droplet, contacts)
        self.play(sim_t.animate.set_value(1.0), run_time=3.8, rate_func=linear)
        cluster_lbl = T("LAT cluster", 26, C_DECODER).move_to([cluster_center[0], cluster_center[1] + 1.62, 0.0])
        self.play(FadeIn(cluster_lbl), run_time=0.5)
        self.finish()


class S07PredictQ(SpokenScene):
    def construct(self):
        g = make_lat_cluster_backdrop(slide_center=(0.0, 0.64, 0.0), slide_w=12.0, slide_h=4.65)
        tag = scope_tag("schematic").move_to([5.35, 3.32, 0])
        self.add(g.slide, g.cluster_fill, g.cluster_lbl, tag)
        for m in g[2:4]:
            self.add(m)

        outside_kin_offsets = [
            [-2.95, 0.75, 0.0],
            [-2.95, -0.15, 0.0],
            [-2.35, -1.05, 0.0],
            [2.95, 0.75, 0.0],
            [2.95, -0.15, 0.0],
            [2.35, -1.05, 0.0],
        ]
        kin_targets = []
        for idx, blk in enumerate(g.kinases):
            rad0 = 0.55 + 0.25 * np.sin(blk._phase)
            kin_targets.append(np.array([
                blk._cx + blk._rx * rad0 * np.cos(blk._phase),
                blk._cy + blk._ry * rad0 * np.sin(blk._phase),
                0.0,
            ]))
            blk.move_to(g.cc + np.array(outside_kin_offsets[idx]))

        self.add(g.kinases, g.phosphatases)
        attach_cluster_particle_updaters(g, kinases=False, phosphatases=True)

        self.at("pulls kinases in")
        self.play(
            *[g.kinases[i].animate.move_to(kin_targets[i]) for i in range(len(g.kinases))],
            FadeIn(g.kin_tag),
            run_time=0.9,
        )
        attach_cluster_particle_updaters(g, kinases=True, phosphatases=False)

        self.at("keeps phosphatases")
        self.play(FadeIn(g.phos_tag), run_time=0.9)

        self.at("Predict what happens")
        q = question_card(
            "Kinases in, phosphatases out: signals stay on longer, or shut off faster?",
            options=["Stay on longer", "Shut off faster"],
            y=-3.15, left=-6.0, max_w=10.6, size=28, chip_size=26,
        )
        self.play(FadeIn(q.chips), run_time=0.7)
        self.at("Compared with outside")
        self.play(FadeIn(q.question), run_time=0.6)
        self.finish()


class S08Pause(PredictPause):
    SECONDS = 4.5
    QUESTION = "Kinases in, phosphatases out: signals stay on longer, or shut off faster?"
    OPTIONS = ["Stay on longer", "Shut off faster"]
    CARD = {"y": -3.15, "left": -6.0, "max_w": 10.6, "size": 28, "chip_size": 26}

    def backdrop(self):
        g = make_lat_cluster_backdrop(slide_center=(0.0, 0.64, 0.0), slide_w=12.0, slide_h=4.65)
        attach_cluster_particle_updaters(g)
        tag = scope_tag("schematic").move_to([5.35, 3.32, 0])
        return VGroup(g, tag)


class S09PredictRevealCaveat(SpokenScene):
    def construct(self):
        g = make_lat_cluster_backdrop(slide_center=(0.0, 0.64, 0.0), slide_w=12.0, slide_h=4.65)
        attach_cluster_particle_updaters(g)
        tag = scope_tag("schematic").move_to([5.35, 3.32, 0])
        q = question_card(
            "Kinases in, phosphatases out: signals stay on longer, or shut off faster?",
            options=["Stay on longer", "Shut off faster"],
            y=-3.15, left=-6.0, max_w=10.6, size=28, chip_size=26,
        )
        self.add(g, tag, q)

        # Beat 1: Answer reveal -> Stay on longer
        self.play(
            FadeOut(q.question, run_time=0.35),
            FadeOut(q.chips[1], run_time=0.35),
            q.chips[0].animate.set_stroke(C_ACTIVE, width=3.5).set_fill(C_ACTIVE, opacity=0.25),
            g.cluster_fill.animate.set_stroke(C_ACTIVE).set_fill(C_ACTIVE, opacity=0.35),
            run_time=0.9,
        )
        ans_lbl = T("Signals stay on longer", 28, C_ACTIVE).move_to([0.0, -3.10, 0])
        self.play(FadeIn(ans_lbl), run_time=0.4)

        self.at("adding phosphate speeds up")
        f_in = ValueTracker(0.5)
        f_out = ValueTracker(0.5)
        bar_box = RoundedRectangle(corner_radius=0.12, width=3.1, height=1.55, stroke_color=C_STRUCT, stroke_width=2.5, fill_color=BG, fill_opacity=0.90).move_to([4.15, 0.25, 0])
        bar_title = T("Signal ON", 24, C_TEXT).move_to([4.15, 0.78, 0])
        in_bar = always_redraw(lambda: Rectangle(width=2.3 * f_in.get_value(), height=0.28, stroke_width=0, fill_color=C_ACTIVE, fill_opacity=0.85).move_to([2.80 + 1.15 * f_in.get_value(), 0.25, 0]))
        out_bar = always_redraw(lambda: Rectangle(width=2.3 * f_out.get_value(), height=0.28, stroke_width=0, fill_color=C_BRAKE, fill_opacity=0.85).move_to([2.80 + 1.15 * f_out.get_value(), -0.25, 0]))
        in_lbl = T("In", 22, C_ACTIVE).move_to([5.42, 0.25, 0])
        out_lbl = T("Out", 22, C_BRAKE).move_to([5.36, -0.25, 0])
        for p in g.phosphatases[3:]:
            p.clear_updaters()
            p.set_opacity(0.0)
        self.play(FadeIn(bar_box), FadeIn(bar_title), FadeIn(in_lbl), FadeIn(out_lbl), run_time=0.35)
        self.add(in_bar, out_bar)
        self.play(f_in.animate.set_value(0.90), f_out.animate.set_value(0.15), run_time=1.8)

        # Beat 2: In living cells -> cross-transition directly to living cell membrane (no blank frame!)
        self.at("In living cells")
        mem = build_plasma_membrane_zoom(y_mem=1.65)
        cell_badge = boxed_label("Living cell", C_DECODER, size=26, pad=0.14).move_to([-4.6, 2.85, 0])
        spot = Circle(radius=0.65, stroke_color=C_DECODER, stroke_width=3.5, fill_color=C_DECODER, fill_opacity=0.55).move_to([-2.0, 0.95, 0])
        spot_lbl = T("Bright spot", 24, C_DECODER).next_to(spot, DOWN, buff=0.16)

        P_frap = Plot(
            box=(1.5, 6.0, -2.1, 0.25),
            xr=(0, 6), yr=(0, 1.1),
            xticks=[], yticks=[(0, "0"), (1.0, "full")],
            xlabel="time after bleach", ylabel="Brightness",
        )
        tag_bot = scope_tag("schematic")
        self.play(
            FadeOut(VGroup(g, q.chips[0], ans_lbl, bar_box, bar_title, in_bar, out_bar, in_lbl, out_lbl, tag), run_time=0.45),
            FadeIn(VGroup(mem, cell_badge, spot, spot_lbl, P_frap, tag_bot), run_time=0.65),
        )

        self.at("bleaches a bright spot")
        laser = Line([-2.0, 3.38, 0], [-2.0, 0.95, 0], color=C_TEXT, stroke_width=8)
        self.play(Create(laser), spot.animate.set_fill(BG, opacity=0.90).set_stroke(C_STRUCT), run_time=0.6)
        self.play(FadeOut(laser, run_time=0.3), FadeOut(spot_lbl, run_time=0.3))

        self.at("times its refill")
        frap_t = ValueTracker(0.0)
        frap_fn = lambda t: 0.10 + 0.85 * (1.0 - np.exp(-0.55 * t))
        frap_live = P_frap.live_curve(frap_fn, frap_t, color=C_DECODER, width=5)
        frap_dot = P_frap.dot(lambda: frap_t.get_value(), lambda: frap_fn(frap_t.get_value()), color=C_TEXT, ring=C_DECODER)
        spot_fill = always_redraw(lambda: Circle(
            radius=0.62, stroke_width=0,
            fill_color=C_DECODER, fill_opacity=0.60 * frap_fn(frap_t.get_value()),
        ).move_to([-2.0, 0.95, 0]))
        ex_dots = VGroup()
        for k_i, ang in enumerate(np.linspace(0, TAU, 8, endpoint=False)):
            d = Dot([-2.0 + 1.1 * np.cos(ang), 0.95 + 0.8 * np.sin(ang), 0], radius=0.075, color=C_DECODER)
            d._ang = ang
            d._k = k_i

            def u_ex(m, dt):
                a = m._ang + 0.8 * frap_t.get_value()
                r = 0.25 + 0.75 * max(0.0, 1.0 - frap_t.get_value() / 5.5)
                m.move_to([-2.0 + r * np.cos(a), 0.95 + 0.75 * r * np.sin(a), 0])

            d.add_updater(u_ex)
            ex_dots.add(d)
        self.add(spot_fill, frap_live, frap_dot, ex_dots)
        self.play(frap_t.animate.set_value(5.8), run_time=3.5, rate_func=linear)

        # Beat 3: Split zoom -> Liquid droplet? vs Fixed scaffold?
        self.at("happens in a droplet")
        for d in ex_dots:
            d.clear_updaters()
        self.play(FadeOut(VGroup(mem, cell_badge, spot, spot_fill, P_frap, frap_live, frap_dot, ex_dots), run_time=0.45))

        tp = TwoPanel("Liquid droplet?", "Fixed scaffold?", colors=(C_DECODER, C_SIGNAL), top=2.95, bottom=-2.15, gap=0.45, width=12.4, size=30)
        debate_badge = boxed_label("Living cells: still debated", C_SIGNAL, size=28, pad=0.14).move_to([-0.8, -2.95, 0])

        lc_c = tp.area("left")[0]
        drop_ring = Circle(radius=1.35, stroke_color=C_DECODER, stroke_width=3.0, fill_color=C_DECODER, fill_opacity=0.16).move_to(lc_c)
        drop_dots = VGroup()
        for k in range(10):
            ang = k * TAU / 10.0
            d = Dot(lc_c + np.array([1.7 * np.cos(ang), 1.3 * np.sin(ang), 0.0]), radius=0.11, color=C_DECODER)
            d._ang = ang
            d._k = k
            d._c = lc_c.copy()
            d._t = 0.0

            def u_drop(m, dt):
                m._t += dt
                r = 0.55 + 1.05 * (0.5 + 0.5 * np.sin(1.4 * m._t + m._k * 0.7))
                a = m._ang + 0.6 * m._t
                m.move_to(m._c + np.array([r * np.cos(a), 0.85 * r * np.sin(a), 0.0]))

            d.add_updater(u_drop)
            drop_dots.add(d)

        rc_c = tp.area("right")[0]
        scaffold_bar = VGroup(
            Line(rc_c + LEFT * 1.6, rc_c + RIGHT * 1.6, color=C_STRUCT, stroke_width=6),
            *[Line(rc_c + RIGHT * x + UP * 0.25, rc_c + RIGHT * x + DOWN * 0.25, color=C_STRUCT, stroke_width=4) for x in (-1.2, -0.4, 0.4, 1.2)],
        )
        scaf_lbl = T("Fixed sites", 24, C_TEXT).next_to(scaffold_bar, DOWN, buff=0.45)
        scaf_dots = VGroup()
        for k in range(6):
            site_x = (-1.2, -0.4, 0.4, 1.2, -0.4, 0.4)[k]
            d = Dot(rc_c + np.array([site_x, 0.0 if k < 4 else 0.75, 0.0]), radius=0.11, color=C_DECODER)
            d._site = rc_c + np.array([site_x, 0.0, 0.0])
            d._t = 0.0
            d._k = k

            def u_scaf(m, dt):
                m._t += dt
                off = max(0.0, np.sin(1.6 * m._t + m._k * 1.1))
                m.move_to(m._site + UP * (0.95 * off) + RIGHT * (0.20 * np.cos(m._t + m._k)))

            d.add_updater(u_scaf)
            scaf_dots.add(d)

        self.play(FadeIn(tp), FadeIn(drop_ring), FadeIn(scaffold_bar), FadeIn(scaf_lbl), run_time=0.8)
        self.add(drop_dots, scaf_dots)

        self.at("remain debated")
        self.play(FadeIn(debate_badge, scale=0.95), run_time=0.5)
        self.finish()


class S10Wrap(SpokenScene):
    def construct(self):
        cell = build_cell(with_labels=False)
        mem_lbl = T("Plasma membrane", 24, C_TEXT).move_to([-2.15, 3.06, 0])
        nuc_lbl = T("Nucleus", 24, C_TEXT).move_to([-4.30, -1.75, 0])

        # Top left of cell: Channel + AKAP vertical tether (no arc crossing PKA!) + soft glow cAMP
        ch = make_channel(x=-5.05, y_mem=2.55, active=True, label="")
        camp_pocket = Circle(radius=0.72, stroke_width=0, fill_color=C_SIGNAL, fill_opacity=0.18).move_to([-4.25, 1.78, 0])
        akap_pka = make_akap_and_pka(anchor_x=-3.95, y_mem=2.45, pka_color=C_ACTIVE, label_akap=False, with_cradle=False)
        akap_pka.pka_body.set(width=0.92, height=0.50)
        akap_pka.pka.remove(akap_pka.pka_lbl)
        akap_pka.pka_lbl = T("PKA", 22, C_ACTIVE).move_to(akap_pka.pka_body)
        akap_pka.pka.add(akap_pka.pka_lbl)
        akap_pka.move_to([-3.95, 1.82, 0])
        bar_y = akap_pka.pka_body.get_top()[1] + 0.04
        akap_pka.akap_shape[1].put_start_and_end_on([-3.95 - 0.35, bar_y, 0], [-3.95 + 0.35, bar_y, 0])
        akap_pka.akap_shape[0].put_start_and_end_on([-3.95, 2.65, 0], [-3.95, bar_y, 0])
        akap_lbl = T("Anchored PKA", 24, C_ACTIVE).move_to([-4.25, 0.72, 0])

        # Top right of cell: Cluster (debated in cells)
        clust = Ellipse(width=1.55, height=0.80, stroke_color=C_DECODER, stroke_width=3.0, fill_color=C_DECODER, fill_opacity=0.22).move_to([-1.25, 2.02, 0])
        clust_lbl = T("Cluster\n(debated in cells)", 24, C_DECODER, line_spacing=0.85).move_to([-1.25, 1.06, 0])

        # Bottom of cell: Pulsing NF-kappaB driven by computed ODE; docks right of Nucleus label
        dock_x = cell.cx + 0.55
        nfkb = make_nfkb_complex([dock_x, -1.55, 0], scale=0.82)
        loop_lbl = T("NF-κB loop", 24, C_DECODER).move_to([dock_x, -2.42, 0])

        P = Plot(
            box=(1.5, 6.1, -1.0, 2.2),
            xr=(0, 14), yr=(-0.14, 1.38),
            xticks=[], yticks=[(0, "low"), (1.1, "high")],
            xlabel="time", ylabel="Pulses",
        )
        tag = scope_tag("schematic")

        t_trk = ValueTracker(0.0)
        live = P.live_curve(nfkb_n_fn, t_trk, color=C_DECODER, width=5)
        dot = P.dot(lambda: t_trk.get_value(), lambda: nfkb_n_fn(t_trk.get_value()), color=C_TEXT, ring=C_DECODER, radius=0.10)

        # Decisive nuclear import/export step driven by computed ODE N(t), never hovering on nuclear rim
        def move_nfkb(m):
            val = nfkb_n_fn(t_trk.get_value())
            s = 1.0 / (1.0 + np.exp(-14.0 * (val - 0.45)))
            y = 0.08 - 1.68 * s
            x = cell.cx + 0.55 * s
            m.move_to([x, y, 0.0])

        nfkb.add_updater(move_nfkb)

        self.play(
            FadeIn(cell), FadeIn(mem_lbl), FadeIn(nuc_lbl),
            FadeIn(camp_pocket), FadeIn(ch), FadeIn(akap_pka), FadeIn(akap_lbl),
            FadeIn(clust), FadeIn(clust_lbl), FadeIn(nfkb), FadeIn(loop_lbl),
            Create(P), FadeIn(tag),
            run_time=1.0,
        )
        self.add(live, dot)
        self.play(t_trk.animate.set_value(5.0), run_time=5.0, rate_func=linear)

        self.at("Delayed negative feedback")
        pulse_cap = boxed_label("Delayed feedback → pulses", C_DECODER, size=24, pad=0.12).move_to([3.35, -2.02, 0])
        self.play(FadeIn(pulse_cap), t_trk.animate.set_value(5.6), run_time=0.45, rate_func=linear)
        self.play(t_trk.animate.set_value(9.0), run_time=3.0, rate_func=linear)

        self.at("location decides")
        place_cap = boxed_label("Location → which targets answer", C_SIGNAL, size=24, pad=0.12).move_to([3.35, -2.75, 0])
        self.play(FadeIn(place_cap), t_trk.animate.set_value(9.6), run_time=0.45, rate_func=linear)
        self.play(t_trk.animate.set_value(13.5), run_time=2.75, rate_func=linear)

        self.at("Read on")
        self.play(t_trk.animate.set_value(14.0), run_time=1.0, rate_func=linear)
        nfkb.clear_updaters()
        self.finish()


class S11End(EndCard):
    LINE = "Delayed negative feedback makes pulses, and location restricts which targets answer."
