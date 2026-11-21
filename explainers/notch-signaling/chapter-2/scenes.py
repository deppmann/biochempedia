"""Equal Neighbours, Opposite Fates — Lateral inhibition by Notch signaling.

COLOUR MAP (one colour per concept across the entire film):
  AMBER  (#F5A623) : Ligand (Delta / Sending) / Sender / Nerve fate
  TEAL   (#3FB8C0) : Notch receptor / Receiver / Skin membrane identity
  CYAN   (#58C4DD) : NICD (cleaved Notch intracellular domain / nuclear signal)
  INDIGO (#1B2240 fill, #6E82D8 stroke) : Cell nucleus
  EMERALD(#52C77A) : Active Notch target gene & Hes-type repressors
  GOLD   (#D4A843) : Extracellular lock (negative regulatory region) & predict highlight
  CORAL  (#FC6255) : ADAM protease cut (outside membrane)
  VIOLET (#B388FF) : γ-Secretase cut (inside membrane)
  GREY   (#8B93A1) : Neutral cell membrane, plot axes, schematic tags
  TEXT   (#E8EAF0) : Primary labels and headings

CARRIED WORLD:
  Two identical touching cells (Cell A left, Cell B right) sharing a vertical border at x = 0,
  with twin live Sending / NICD gauges and a computed 'Schematic ligand level' plot below;
  zooming out in S08–S09 to the same cells inside a 25-cell honeycomb sheet, then back to a pair in S10.

COMPUTED SCENE CHANGES:
  s00_title         : Standard TitleCard for "Equal Neighbours, Opposite Fates".
  s01_hook          : Ligand pull peels lock, ADAM & γ-secretase cut, freeing 1 NICD; zooms out to identical cells A & B with baseline fluctuations.
  s02_equal_start   : Symmetric bidirectional tugs send equal NICD pulses to both nuclei; computed ODE traces A & B advance together at 0.50.
  s03_chance_lead   : Chance +1 ligand on A tugs B's Notch (lock/cuts -> NICD), turning on emerald repressors in B that block nerve and pull B's Sending down (computed ODE t=2.5->3.9).
  s04_predict       : B's ligands thin out & dim; dashed return arrow from B to A pulses with '?'; question card appears at top.
  s05_pause         : Standard PredictPause holding the S04 world and question card for 4.5 s with countdown ring.
  s06_feedback      : A's NICD drops, nerve stays ON, A's Sending surges; double-inhibition loop builds word by word ('Left ⊣ right's sending ⊣ left's sending = left boosts left'); ODE curves diverge (t=3.9->7.0).
  s07_diverge       : Computed ODE traces sweep apart (t=7.0->12.0); A becomes warm amber Sender: nerve, B becomes cool teal/emerald Receiver: skin; banner 'Lateral inhibition'.
  s08_sheet         : Pulls back from A & B into a 25-cell honeycomb; computed multi-cell lateral-inhibition ODE (rng seed 7) sorts spaced amber senders surrounded by teal receivers.
  s09_reach_and_flex: Zooms onto central amber sender; thin swaying amber extensions reach 2–3 cell diameters out to brush distant teal Notch, widening bristle spacing.
  s10_closing       : Blends back to crisp sender/receiver pair in the sheet with steady one-way contact pulses keeping opposite fates.
  s11_end           : Standard EndCard with exact take-home line.
"""

from bp_parts import *  # noqa: F401,F403

# ------------------------------------------------------------------ Film Palette
AMBER = "#F5A623"
EMERALD = "#52C77A"
VIOLET = "#B388FF"
INDIGO_FILL = "#1B2240"
INDIGO_STROKE = "#6E82D8"
CELL_FILL = "#151924"
CELL_STROKE = "#6E7787"
CYAN = BLUE
CORAL = RED


# ------------------------------------------------------------------ Computed Lateral-Inhibition ODE
def _compute_two_cell_ode(t_max=12.0, dt=0.02):
    """Coupled dimensionless lateral-inhibition ODE for touching cells A and B.
    Symmetric fixed point at D* = 0.5, N* = 0.5; chance lead injected at t = 2.5.
    """
    n = int(round(t_max / dt)) + 1
    ts = np.linspace(0.0, t_max, n)
    da = np.empty(n)
    db = np.empty(n)
    na = np.empty(n)
    nb = np.empty(n)
    da[0] = db[0] = na[0] = nb[0] = 0.5
    rng = np.random.default_rng(7)
    for i in range(n - 1):
        if ts[i] < 2.5:
            da[i + 1] = float(np.clip(0.5 + rng.normal(0.0, 0.008), 0.48, 0.52))
            db[i + 1] = float(np.clip(0.5 + rng.normal(0.0, 0.008), 0.48, 0.52))
            na[i + 1] = 0.5
            nb[i + 1] = 0.5
            if ts[i + 1] >= 2.5 - 0.5 * dt:
                da[i + 1] = 0.58
                db[i + 1] = 0.50
        elif ts[i] < 3.9:
            # Hold Cell A at the initial chance-lead state until S06 closes the feedback loop
            na[i + 1] = 0.50
            da[i + 1] = 0.58
            d_nb = 1.2 * (da[i] ** 3 / (0.125 + da[i] ** 3) - nb[i])
            d_db = 1.4 * (1.0 / (1.0 + (nb[i] / 0.5) ** 4) - db[i])
            nb[i + 1] = float(np.clip(nb[i] + dt * d_nb, 0.0, 1.0))
            db[i + 1] = float(np.clip(db[i] + dt * d_db, 0.0, 1.0))
        else:
            d_na = 1.2 * (db[i] ** 3 / (0.125 + db[i] ** 3) - na[i])
            d_nb = 1.2 * (da[i] ** 3 / (0.125 + da[i] ** 3) - nb[i])
            d_da = 1.4 * (1.0 / (1.0 + (na[i] / 0.5) ** 4) - da[i])
            d_db = 1.4 * (1.0 / (1.0 + (nb[i] / 0.5) ** 4) - db[i])
            na[i + 1] = float(np.clip(na[i] + dt * d_na, 0.0, 1.0))
            nb[i + 1] = float(np.clip(nb[i] + dt * d_nb, 0.0, 1.0))
            da[i + 1] = float(np.clip(da[i] + dt * d_da, 0.0, 1.0))
            db[i + 1] = float(np.clip(db[i] + dt * d_db, 0.0, 1.0))
    return ts, da, db, na, nb


_TS, _DA, _DB, _NA, _NB = _compute_two_cell_ode()


def two_cell_state(t):
    """Interpolated (D_A, D_B, N_A, N_B) at simulation time t in [0, 12]."""
    t = float(np.clip(t, 0.0, 12.0))
    return (
        float(np.interp(t, _TS, _DA)),
        float(np.interp(t, _TS, _DB)),
        float(np.interp(t, _TS, _NA)),
        float(np.interp(t, _TS, _NB)),
    )


def _compute_sheet_ode(seed=7, steps=900, dt=0.02):
    """Compute 25-cell hexagonal honeycomb lateral-inhibition trajectories.
    Cell 12 (center) and Cell 13 (right neighbour) correspond to the carried pair A & B.
    """
    r_hex = 0.56
    dx = np.sqrt(3.0) * r_hex
    dy = 1.5 * r_hex
    centers = []
    for r in range(5):
        for c in range(5):
            x = (c - 2) * dx + (0.5 * dx if r % 2 == 1 else 0.0) - 0.25 * dx
            y = (2 - r) * dy
            centers.append(np.array([x, y, 0.0]))
    centers = np.array(centers)
    adj = [
        [j for j in range(25) if i != j and np.linalg.norm(centers[i] - centers[j]) < 1.2 * dx]
        for i in range(25)
    ]

    rng = np.random.default_rng(seed)
    d = 0.5 + rng.uniform(-0.04, 0.04, 25)
    d[12] = 0.62
    d[13] = 0.38
    n = np.full(25, 0.5)

    d_hist = [d.copy()]
    for _ in range(steps):
        d_nbr = np.array([
            0.65 * max(d[j] for j in adj[i]) + 0.35 * np.mean([d[j] for j in adj[i]])
            for i in range(25)
        ])
        n = np.clip(n + dt * 1.2 * (d_nbr ** 3 / (0.125 + d_nbr ** 3) - n), 0.0, 1.0)
        d = np.clip(d + dt * 1.4 * (1.0 / (1.0 + (n / 0.5) ** 4) - d), 0.0, 1.0)
        d_hist.append(d.copy())

    ring2 = [j for j in range(25) if 1.45 * dx < np.linalg.norm(centers[12] - centers[j]) < 2.15 * dx]
    d_ext = d.copy()
    n_ext = n.copy()
    ext_hist = [d_ext.copy()]
    for _ in range(700):
        d_nbr = np.empty(25)
        for i in range(25):
            base = 0.65 * max(d_ext[j] for j in adj[i]) + 0.35 * np.mean([d_ext[j] for j in adj[i]])
            d_nbr[i] = max(base, 0.90 * d_ext[12]) if i in ring2 else base
        n_ext = np.clip(n_ext + dt * 1.2 * (d_nbr ** 3 / (0.125 + d_nbr ** 3) - n_ext), 0.0, 1.0)
        d_ext = np.clip(d_ext + dt * 1.4 * (1.0 / (1.0 + (n_ext / 0.5) ** 4) - d_ext), 0.0, 1.0)
        ext_hist.append(d_ext.copy())

    return centers, adj, ring2, np.array(d_hist), np.array(ext_hist)


_HEX_CENTERS, _HEX_ADJ, _RING2, _SHEET_D, _EXT_D = _compute_sheet_ode()


# ------------------------------------------------------------------ Shared Visual Builders
CELL_TOP = 2.65
CELL_BOT = -0.95
CELL_W = 5.2
CLEFT_HALF = 0.43
CELL_CY = (CELL_TOP + CELL_BOT) / 2.0  # 0.85
NUC_X = 3.85
NUC_Y = 0.82


def make_ligand(pos, direction=RIGHT, scale=1.0, opacity=1.0):
    """Membrane-anchored warm amber ligand: stem + globular head pointing toward neighbour."""
    d = np.array(direction, dtype=float)
    d = d / np.linalg.norm(d)
    stem = Line(pos, pos + d * 0.34 * scale, color=AMBER, stroke_width=5 * scale, stroke_opacity=opacity)
    head = Circle(radius=0.11 * scale, color=AMBER, fill_color=AMBER, fill_opacity=0.95 * opacity, stroke_width=2)
    head.move_to(pos + d * 0.40 * scale)
    return VGroup(stem, head)


def make_receptor(pos, direction=LEFT, scale=1.0, opacity=1.0, with_lock=False):
    """Cool teal Notch receptor with U-shaped receiving cup and optional gold lock."""
    d = np.array(direction, dtype=float)
    d = d / np.linalg.norm(d)
    perp = np.array([-d[1], d[0], 0.0])
    stem = Line(pos - d * 0.14 * scale, pos + d * 0.34 * scale, color=TEAL, stroke_width=5 * scale, stroke_opacity=opacity)
    cup = VGroup(
        Line(pos + d * 0.34 * scale + perp * 0.13 * scale, pos + d * 0.50 * scale + perp * 0.15 * scale, color=TEAL, stroke_width=4.5 * scale, stroke_opacity=opacity),
        Line(pos + d * 0.34 * scale - perp * 0.13 * scale, pos + d * 0.50 * scale - perp * 0.15 * scale, color=TEAL, stroke_width=4.5 * scale, stroke_opacity=opacity),
        Line(pos + d * 0.34 * scale + perp * 0.13 * scale, pos + d * 0.34 * scale - perp * 0.13 * scale, color=TEAL, stroke_width=4.5 * scale, stroke_opacity=opacity),
    )
    tail = Line(pos - d * 0.14 * scale, pos - d * 0.36 * scale, color=CYAN, stroke_width=4 * scale, stroke_opacity=opacity)
    g = VGroup(stem, cup, tail)
    if with_lock:
        lock = Arc(radius=0.14 * scale, start_angle=-PI / 2, angle=PI, color=GOLD, stroke_width=4 * scale, arc_center=pos + d * 0.22 * scale)
        if d[0] < 0:
            lock.rotate(PI, about_point=pos + d * 0.22 * scale)
        g.add(lock)
    return g


def make_dashed_arrow(start, end, color=GOLD, stroke_width=4.5, dash_length=0.14):
    """Dashed line ending in a crisp filled arrowhead."""
    s, e = np.array(start, dtype=float), np.array(end, dtype=float)
    v = e - s
    length = np.linalg.norm(v)
    u = v / max(length, 1e-6)
    line_end = e - u * 0.22
    ln = DashedLine(s, line_end, color=color, stroke_width=stroke_width, dash_length=dash_length)
    tip = Triangle(color=color, fill_color=color, fill_opacity=1.0).scale(0.11)
    tip.rotate(np.arctan2(u[1], u[0]) - PI / 2)
    tip.move_to(e - u * 0.10)
    return VGroup(ln, tip)


def make_gauge(label_text, tr_t, state_idx, at, color, width=1.18):
    """Horizontal live bar gauge + monospace readout driven directly by tr_t via two_cell_state."""
    lbl = T(label_text, size=24, color=color).move_to([at[0] - 1.24, at[1], 0], aligned_edge=LEFT)
    bar_x0 = at[0] + 0.14
    bg = RoundedRectangle(corner_radius=0.06, width=width, height=0.22, stroke_color=GREY, stroke_width=1.8,
                          fill_color=BG, fill_opacity=0.85).move_to([bar_x0 + width / 2, at[1], 0])

    def mk_fill():
        val = two_cell_state(tr_t.get_value())[state_idx]
        v = float(np.clip(val, 0.02, 1.0))
        w = max(0.04, width * v)
        r = Rectangle(width=w, height=0.16, stroke_width=0, fill_color=color, fill_opacity=0.92)
        r.move_to([bar_x0 + w / 2, at[1], 0])
        return r

    def mk_num():
        val = two_cell_state(tr_t.get_value())[state_idx]
        return M(f"{val:.2f}", size=24, color=TEXT).move_to([bar_x0 + width + 0.56, at[1], 0])

    fill = always_redraw(mk_fill)
    num = always_redraw(mk_num)
    return VGroup(lbl, bg, fill, num)


def make_two_cell_world(t_val=0.0, show_plot=True, fate_a="Nerve ?", fate_b="Skin ?",
                        b_repressor=False, a_amber_count=3, b_amber_count=3, b_dim=False):
    """Build the carried two-cell world and timeline plot at simulation time t_val."""
    tr_t = ValueTracker(t_val)

    h = CELL_TOP - CELL_BOT
    cell_a = RoundedRectangle(corner_radius=0.22, width=CELL_W, height=h, stroke_color=CELL_STROKE,
                              stroke_width=3.5, fill_color=CELL_FILL, fill_opacity=0.92).move_to([-(CLEFT_HALF + CELL_W / 2), CELL_CY, 0])
    cell_b = RoundedRectangle(corner_radius=0.22, width=CELL_W, height=h, stroke_color=CELL_STROKE,
                              stroke_width=3.5, fill_color=CELL_FILL, fill_opacity=0.92).move_to([CLEFT_HALF + CELL_W / 2, CELL_CY, 0])
    wall = VGroup()

    nuc_a = Ellipse(width=2.15, height=1.02, stroke_color=INDIGO_STROKE, stroke_width=3,
                    fill_color=INDIGO_FILL, fill_opacity=0.95).move_to([-NUC_X, NUC_Y, 0])
    nuc_b = Ellipse(width=2.15, height=1.02, stroke_color=INDIGO_STROKE, stroke_width=3,
                    fill_color=INDIGO_FILL, fill_opacity=0.95).move_to([NUC_X, NUC_Y, 0])
    nuc_lbl_a = T("Nucleus", size=24, color=TEXT).move_to([-NUC_X, NUC_Y + 0.72, 0])
    nuc_lbl_b = T("Nucleus", size=24, color=TEXT).move_to([NUC_X, NUC_Y + 0.72, 0])

    gene_a = boxed_label("Gene", GREY, size=22, box=(1.65, 0.44)).move_to(nuc_a.get_center())
    gene_b = boxed_label(
        "Repressors" if b_repressor else "Gene",
        EMERALD if b_repressor else GREY,
        size=22,
        box=(1.85, 0.44),
        fill_opacity=0.25 if b_repressor else 0.15,
    ).move_to(nuc_b.get_center())

    head_a = T("Cell A", size=28, color=TEXT, weight=BOLD).move_to([-4.68, 2.25, 0])
    head_b = T("Cell B", size=28, color=TEXT, weight=BOLD).move_to([4.68, 2.25, 0])

    nerve_a = boxed_label(fate_a, AMBER if "ON" in fate_a or "Sender" in fate_a else TEXT, size=24, box=(1.92, 0.44)).move_to([-2.55, 2.25, 0])
    nerve_b = boxed_label(fate_b, TEAL if "Receiver" in fate_b else (GREY if "blocked" in fate_b else TEXT), size=24, box=(1.92, 0.44)).move_to([2.55, 2.25, 0])

    g_send_a = make_gauge("Sending", tr_t, 0, at=[-4.02, -0.15, 0], color=AMBER)
    g_nicd_a = make_gauge("NICD", tr_t, 2, at=[-4.02, -0.58, 0], color=CYAN)
    g_send_b = make_gauge("Sending", tr_t, 1, at=[2.22, -0.15, 0], color=AMBER)
    g_nicd_b = make_gauge("NICD", tr_t, 3, at=[2.22, -0.58, 0], color=CYAN)

    ys_rec_b = [0.30, 0.95, 1.60]
    if a_amber_count <= 3:
        ys_lig_a = ys_rec_b[:a_amber_count]
    elif a_amber_count == 4:
        ys_lig_a = [0.30, 0.95, 1.60, 2.22]
    else:
        ys_lig_a = [-0.10, 0.30, 0.95, 1.60, 2.12]
    ligs_a = VGroup(*[make_ligand(np.array([-CLEFT_HALF, y, 0]), RIGHT) for y in ys_lig_a])
    recs_b = VGroup(*[make_receptor(np.array([CLEFT_HALF, y, 0]), LEFT) for y in ys_rec_b])

    ys_rec_a = [0.62, 1.27, 1.92]
    if b_amber_count <= 0:
        ys_lig_b = []
    elif b_amber_count == 1:
        ys_lig_b = [1.27]
    elif b_amber_count == 2:
        ys_lig_b = [1.27, 1.92]
    else:
        ys_lig_b = ys_rec_a[:b_amber_count]
    ligs_b = VGroup(*[make_ligand(np.array([CLEFT_HALF, y, 0]), LEFT, opacity=0.45 if b_dim else 1.0) for y in ys_lig_b])
    recs_a = VGroup(*[make_receptor(np.array([-CLEFT_HALF, y, 0]), RIGHT) for y in ys_rec_a])

    world = VGroup(
        cell_a, cell_b, wall,
        nuc_a, nuc_b, nuc_lbl_a, nuc_lbl_b,
        gene_a, gene_b,
        head_a, head_b, nerve_a, nerve_b,
        g_send_a, g_nicd_a, g_send_b, g_nicd_b,
        ligs_a, recs_b, ligs_b, recs_a,
    )

    plot_objs = VGroup()
    if show_plot:
        P = Plot(box=(-4.45, 4.5, -2.95, -1.65), xr=(0, 12), yr=(0, 1),
                 xticks=[], yticks=[(0, "0"), (0.5, "0.5"), (1, "1")],
                 xlabel="time (schematic)", ylabel="", size=22, label_size=24)
        ptitle = T("Schematic ligand level", size=24, color=TEXT).move_to([-4.45, -1.32, 0], aligned_edge=LEFT)
        leg_a = VGroup(Line(ORIGIN, RIGHT * 0.35, color=AMBER, stroke_width=6), T("Cell A", size=24, color=AMBER)).arrange(RIGHT, buff=0.12).move_to([5.55, -1.95, 0])
        leg_b = VGroup(Line(ORIGIN, RIGHT * 0.35, color=TEAL, stroke_width=4), T("Cell B", size=24, color=TEAL)).arrange(RIGHT, buff=0.12).move_to([5.55, -2.45, 0])
        curve_a = P.live_curve(lambda x: two_cell_state(x)[0], tr_t, color=AMBER, width=6)
        curve_b = P.live_curve(lambda x: two_cell_state(x)[1], tr_t, color=TEAL, width=4)
        dot_a = P.dot(lambda: tr_t.get_value(), lambda: two_cell_state(tr_t.get_value())[0], color=AMBER, ring=TEXT, radius=0.07)
        dot_b = P.dot(lambda: tr_t.get_value(), lambda: two_cell_state(tr_t.get_value())[1], color=TEAL, ring=TEXT, radius=0.07)
        plot_objs = VGroup(P, ptitle, leg_a, leg_b, curve_a, curve_b, dot_a, dot_b)

    return {
        "all": VGroup(world, plot_objs),
        "world": world,
        "plot_group": plot_objs,
        "cell_a": cell_a, "cell_b": cell_b, "wall": wall,
        "nuc_a": nuc_a, "nuc_b": nuc_b,
        "gene_a": gene_a, "gene_b": gene_b,
        "head_a": head_a, "head_b": head_b,
        "nerve_a": nerve_a, "nerve_b": nerve_b,
        "g_send_a": g_send_a, "g_nicd_a": g_nicd_a,
        "g_send_b": g_send_b, "g_nicd_b": g_nicd_b,
        "ligs_a": ligs_a, "recs_b": recs_b, "ligs_b": ligs_b, "recs_a": recs_a,
        "tr_t": tr_t,
    }


def hex_polygon(center, radius=0.56, color=CELL_STROKE, fill_color=CELL_FILL, fill_opacity=0.92, stroke_width=3):
    """Pointy-top regular hexagon at `center`."""
    verts = [
        center + np.array([radius * np.cos(PI / 6 + k * PI / 3), radius * np.sin(PI / 6 + k * PI / 3), 0.0])
        for k in range(6)
    ]
    return Polygon(*verts, color=color, stroke_width=stroke_width, fill_color=fill_color, fill_opacity=fill_opacity)


def hex_color_for_D(d_val):
    """Map computed ligand level D in [0, 1] to cell fill and stroke colours."""
    if d_val >= 0.55:
        alpha = np.clip((d_val - 0.55) / 0.45, 0.0, 1.0)
        return interpolate_color(ManimColor(CELL_STROKE), ManimColor(AMBER), alpha), 0.20 + 0.55 * alpha
    else:
        alpha = np.clip((0.55 - d_val) / 0.45, 0.0, 1.0)
        return interpolate_color(ManimColor(CELL_STROKE), ManimColor(TEAL), alpha), 0.20 + 0.42 * alpha


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Notch: Signaling by Contact and by Cutting"
    TITLE = "Equal Neighbours, Opposite Fates"


class S01Hook(SpokenScene):
    def construct(self):
        # Beat 1 (0..6.5s): Recap of Film 1 — one pull, lock peel, ADAM + gamma cuts, 1 NICD -> nucleus
        m_left = Line([-1.05, -2.5, 0], [-1.05, 2.5, 0], color=CELL_STROKE, stroke_width=5)
        m_right = Line([0.85, -2.5, 0], [0.85, 2.5, 0], color=CELL_STROKE, stroke_width=5)
        nuc = Ellipse(width=2.8, height=1.5, stroke_color=INDIGO_STROKE, stroke_width=3.5,
                      fill_color=INDIGO_FILL, fill_opacity=0.95).move_to([4.1, 0.0, 0])
        nuc_t = T("Nucleus", size=26, color=TEXT).move_to(nuc.get_top() + UP * 0.30)
        gene = boxed_label("Target gene", GREY, size=24, box=(2.15, 0.48)).move_to(nuc.get_center())

        lig = make_ligand(np.array([-1.05, 0.0, 0]), RIGHT, scale=2.2)
        rec = make_receptor(np.array([0.85, 0.0, 0]), LEFT, scale=2.2, with_lock=True)
        lbl_lig = T("Ligand", size=28, color=AMBER).next_to(m_left, LEFT, buff=0.60)
        lbl_rec = T("Notch", size=28, color=TEAL).move_to([-0.10, 1.35, 0])
        recap_grp = VGroup(m_left, m_right, nuc, nuc_t, gene, lig, rec, lbl_lig, lbl_rec)

        self.play(FadeIn(recap_grp), run_time=0.8)

        self.at("pull turned one")
        self.play(m_left.animate.shift(LEFT * 0.22), lig.animate.shift(LEFT * 0.22), rec.animate.shift(LEFT * 0.18), run_time=0.8)
        lock_mob = rec[3]
        adam_cut = Line([0.55, 0.45, 0], [0.55, -0.45, 0], color=CORAL, stroke_width=6)
        gam_cut = Line([0.85, 0.45, 0], [0.85, -0.45, 0], color=VIOLET, stroke_width=6)
        self.play(FadeOut(lock_mob, shift=UP * 0.3), Create(adam_cut), run_time=0.45)
        self.play(Create(gam_cut), run_time=0.45)

        self.at("into one nuclear signal")
        nicd_dot = Dot([1.55, 0.0, 0], radius=0.18, color=CYAN)
        nicd_lbl = T("NICD", size=24, color=CYAN).move_to([2.05, -0.45, 0])
        self.play(FadeOut(adam_cut), FadeOut(gam_cut), FadeIn(nicd_dot), FadeIn(nicd_lbl), run_time=0.35)
        self.play(
            FadeOut(nicd_lbl, run_time=0.3),
            nicd_dot.animate.move_to(gene.get_left() + LEFT * 0.24),
            run_time=1.0,
        )
        self.play(
            gene.box.animate.set_stroke(EMERALD).set_fill(EMERALD, opacity=0.35),
            gene.label.animate.set_color(EMERALD),
            run_time=0.5,
        )

        # Beat 2 (7.0s): Zoom out / transform cleanly into the carried two-cell world
        self.at("Now set two")
        w = make_two_cell_world(t_val=0.0, show_plot=True, fate_a="Nerve / Skin ?", fate_b="Nerve / Skin ?")
        self.play(FadeOut(recap_grp), FadeOut(nicd_dot), run_time=0.45)
        self.play(FadeIn(w["all"]), run_time=0.85)

        self.at("How do they pick")
        q_top = T("How do two identical cells pick opposite fates?", size=30, color=GOLD).move_to([0.0, 3.22, 0])
        pulse_a = Dot([-0.80, 0.82, 0], radius=0.11, color=CYAN)
        pulse_b = Dot([0.80, 0.82, 0], radius=0.11, color=CYAN)
        self.add(pulse_a, pulse_b)
        self.play(
            FadeIn(q_top, shift=DOWN * 0.1),
            pulse_a.animate.move_to(w["gene_a"].get_right() + RIGHT * 0.14),
            pulse_b.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14),
            w["tr_t"].animate.set_value(0.65),
            run_time=2.2,
            rate_func=linear,
        )
        self.remove(pulse_a, pulse_b)

        self.at("Nothing outside tells them")
        ext_left = DashedLine([-6.1, -0.8, 0], [-6.1, 2.5, 0], color=GREY, stroke_width=2.5)
        ext_right = DashedLine([6.1, -0.8, 0], [6.1, 2.5, 0], color=GREY, stroke_width=2.5)
        no_ext_banner = T("Nothing outside assigns either fate", size=28, color=TEXT).move_to([0.0, 3.22, 0])
        self.play(
            FadeIn(ext_left), FadeIn(ext_right),
            swap(q_top, no_ext_banner, run_time=0.7),
            w["tr_t"].animate.set_value(1.05),
            run_time=1.4,
        )

        self.at("becomes nerve")
        self.play(
            w["nerve_a"].box.animate.set_stroke(AMBER),
            w["nerve_a"].label.animate.set_color(AMBER),
            w["tr_t"].animate.set_value(1.45),
            run_time=1.5,
            rate_func=linear,
        )
        self.at("becomes skin")
        self.play(
            w["nerve_b"].box.animate.set_stroke(TEAL),
            w["nerve_b"].label.animate.set_color(TEAL),
            w["tr_t"].animate.set_value(1.90),
            run_time=1.8,
            rate_func=linear,
        )
        self.finish()


class S02EqualStart(SpokenScene):
    def construct(self):
        w = make_two_cell_world(t_val=0.0, show_plot=True, fate_a="Undecided", fate_b="Undecided")
        self.add(w["all"])

        top_note = T("Equal toolkit on both sides", size=30, color=TEXT).move_to([0.0, 3.22, 0])
        self.play(FadeIn(top_note), w["tr_t"].animate.set_value(0.50), run_time=3.6, rate_func=linear)

        self.at("amber ligands to send")
        lig_tag_a = fit_text("Ligand\n(send)", max_w=1.6, size=24, color=AMBER).move_to([-1.58, 1.62, 0])
        lig_tag_b = fit_text("Ligand\n(send)", max_w=1.6, size=24, color=AMBER).move_to([1.58, 1.62, 0])
        self.play(
            w["ligs_a"].animate.scale(1.12),
            w["ligs_b"].animate.scale(1.12),
            FadeIn(lig_tag_a),
            FadeIn(lig_tag_b),
            w["tr_t"].animate.set_value(0.95),
            run_time=2.2,
            rate_func=linear,
        )

        self.at("receptors to receive")
        rec_tag_a = fit_text("Notch\n(receive)", max_w=1.6, size=24, color=TEAL).move_to([-1.58, 0.48, 0])
        rec_tag_b = fit_text("Notch\n(receive)", max_w=1.6, size=24, color=TEAL).move_to([1.58, 0.48, 0])
        self.play(
            w["recs_a"].animate.scale(1.12),
            w["recs_b"].animate.scale(1.12),
            FadeIn(rec_tag_a),
            FadeIn(rec_tag_b),
            w["tr_t"].animate.set_value(1.30),
            run_time=2.0,
            rate_func=linear,
        )

        self.at("At the start")
        arr_ab = Arrow([-0.35, 1.45, 0], [0.45, 1.45, 0], color=AMBER, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.3)
        arr_ba = Arrow([0.35, 0.45, 0], [-0.45, 0.45, 0], color=AMBER, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.3)
        eq_badge = boxed_label("Equal pull  (A = B)", TEXT, size=26).move_to([0.0, 3.22, 0])
        self.play(swap(top_note, eq_badge, run_time=0.6), GrowArrow(arr_ab), GrowArrow(arr_ba), run_time=0.8)

        # Route NICD dots cleanly at y=1.02 between lig_tag (y=1.62) and rec_tag (y=0.48), stopping outside gene boxes
        for end_t in [1.70, 2.10]:
            p_a = Dot([-0.80, 1.02, 0], radius=0.11, color=CYAN)
            p_b = Dot([0.80, 1.02, 0], radius=0.11, color=CYAN)
            self.add(p_a, p_b)
            self.play(
                p_a.animate.move_to(w["gene_a"].get_right() + RIGHT * 0.14),
                p_b.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14),
                w["tr_t"].animate.set_value(end_t),
                run_time=2.2,
                rate_func=linear,
            )
            self.remove(p_a, p_b)

        self.at("Neither cell has")
        self.play(
            FadeOut(lig_tag_a), FadeOut(lig_tag_b),
            FadeOut(rec_tag_a), FadeOut(rec_tag_b),
            FadeOut(arr_ab), FadeOut(arr_ba),
            w["tr_t"].animate.set_value(2.45),
            run_time=3.2,
            rate_func=linear,
        )
        self.finish()


class S03ChanceLead(SpokenScene):
    def construct(self):
        w = make_two_cell_world(t_val=2.45, show_plot=True, fate_a="Undecided", fate_b="Undecided")
        self.add(w["all"])

        self.at("random chance gives")
        extra_lig = make_ligand(np.array([-CLEFT_HALF, 2.22, 0]), RIGHT, scale=1.0)
        chance_lbl = T("Random chance: +1 ligand on A", size=28, color=AMBER).move_to([0.0, 3.22, 0])
        self.play(
            FadeIn(extra_lig, scale=1.4),
            FadeIn(chance_lbl),
            w["tr_t"].animate.set_value(2.60),
            run_time=3.5,
            rate_func=linear,
        )

        self.at("pulls harder on")
        pull_arr = Arrow([-0.30, 1.60, 0], [-1.15, 1.60, 0], color=AMBER, stroke_width=5, buff=0)
        lock = Arc(radius=0.18, start_angle=PI / 2, angle=PI, color=GOLD, stroke_width=5, arc_center=[0.21, 1.60, 0])
        adam = Line([0.28, 1.82, 0], [0.28, 1.38, 0], color=CORAL, stroke_width=5)
        gamma = Line([0.43, 1.82, 0], [0.43, 1.38, 0], color=VIOLET, stroke_width=5)
        self.play(GrowArrow(pull_arr), FadeIn(lock), run_time=1.0)
        self.play(FadeOut(lock, shift=UP * 0.25), Create(adam), run_time=0.8)
        self.play(Create(gamma), run_time=0.8)

        self.at("releasing more cyan")
        nicd_b = VGroup(
            Dot([0.75, 1.40, 0], radius=0.14, color=CYAN),
            Dot([0.95, 1.15, 0], radius=0.12, color=CYAN),
        )
        self.play(FadeOut(adam), FadeOut(gamma), FadeOut(pull_arr), FadeIn(nicd_b), run_time=0.5)
        self.play(
            nicd_b.animate.move_to(w["gene_b"].get_left() + LEFT * 0.18),
            w["tr_t"].animate.set_value(3.05),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(FadeOut(nicd_b), run_time=0.35)

        self.at("turns on repressors")
        rep_chip = boxed_label("Repressors", EMERALD, size=22, box=(1.85, 0.44), fill_opacity=0.25).move_to(w["gene_b"])
        rep_banner = T("Notch turns on repressors with two linked jobs", size=28, color=EMERALD).move_to([0.0, 3.22, 0])
        self.play(
            swap(chance_lbl, rep_banner, run_time=0.7),
            swap(w["gene_b"], rep_chip, run_time=0.7),
            run_time=0.7,
        )
        self.play(w["tr_t"].animate.set_value(3.35), run_time=2.1, rate_func=linear)

        self.at("block the nerve")
        # Route arc cleanly to the left of the "Nucleus" label so it never covers letters
        arc_nerve = CurvedArrow(w["nuc_b"].get_left() + UP * 0.20, w["nerve_b"].get_bottom() + LEFT * 0.35,
                                angle=-0.25, color=EMERALD, stroke_width=4)
        blocked_b = boxed_label("Nerve: blocked", GREY, size=24, box=(1.92, 0.44)).move_to(w["nerve_b"])
        self.play(Create(arc_nerve), swap(w["nerve_b"], blocked_b, run_time=0.6), w["tr_t"].animate.set_value(3.60), run_time=1.8, rate_func=linear)

        self.at("lower the right")
        arc_send = CurvedArrow(w["nuc_b"].get_bottom() + LEFT * 0.3, w["g_send_b"].get_top() + RIGHT * 0.2,
                               angle=0.35, color=EMERALD, stroke_width=4)
        self.play(
            Create(arc_send),
            FadeOut(w["ligs_b"][0]),
            w["ligs_b"][1:].animate.set_opacity(0.45),
            w["tr_t"].animate.set_value(3.90),
            run_time=2.5,
            rate_func=linear,
        )
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        w = make_two_cell_world(
            t_val=3.9, show_plot=True,
            fate_a="Nerve ?", fate_b="Nerve: blocked",
            b_repressor=True, a_amber_count=4, b_amber_count=2, b_dim=True,
        )
        self.add(w["all"])

        self.at("follow the loop")
        ret_arr = make_dashed_arrow([0.35, 0.90, 0], [-1.35, 0.90, 0], color=GOLD, stroke_width=4.5, dash_length=0.14)
        q_mark = T("?", size=38, color=GOLD, weight=BOLD).move_to([-1.10, 1.35, 0])
        self.play(Create(ret_arr), FadeIn(q_mark), run_time=2.4)

        self.at("now displays fewer")
        self.play(
            w["ligs_b"].animate.set_opacity(0.25),
            Indicate(w["ligs_b"], color=GOLD, scale_factor=1.22),
            run_time=3.2,
        )

        self.at("What happens next")
        q = question_card("Cell B sends less ligand: what happens to Cell A next?", y=3.25, max_w=10.6, size=30)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=1.0)
        # Sweep dashed return arrow and ? pulse smoothly across the border while asking
        sweep = VGroup(ret_arr, q_mark)
        for _ in range(2):
            self.play(sweep.animate.shift(LEFT * 0.22).set_opacity(0.45), run_time=1.1, rate_func=linear)
            self.play(sweep.animate.shift(RIGHT * 0.22).set_opacity(1.0), run_time=1.1, rate_func=linear)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Cell B sends less ligand: what happens to Cell A next?"
    CARD = {"y": 3.25, "max_w": 10.6, "size": 30}
    RING_AT = (6.0, 3.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = make_two_cell_world(
            t_val=3.9, show_plot=True,
            fate_a="Nerve ?", fate_b="Nerve: blocked",
            b_repressor=True, a_amber_count=4, b_amber_count=2, b_dim=True,
        )
        ret_arr = make_dashed_arrow([0.35, 0.90, 0], [-1.35, 0.90, 0], color=GOLD, stroke_width=4.5, dash_length=0.14)
        q_mark = T("?", size=38, color=GOLD, weight=BOLD).move_to([-1.10, 1.35, 0])
        return VGroup(w["all"], ret_arr, q_mark)


class S06Feedback(SpokenScene):
    def construct(self):
        w = make_two_cell_world(
            t_val=3.9, show_plot=True,
            fate_a="Nerve ?", fate_b="Nerve: blocked",
            b_repressor=True, a_amber_count=4, b_amber_count=2, b_dim=True,
        )
        ret_arr = make_dashed_arrow([0.35, 0.90, 0], [-1.35, 0.90, 0], color=GOLD, stroke_width=4.5, dash_length=0.14)
        q_mark = T("?", size=38, color=GOLD, weight=BOLD).move_to([-1.10, 1.35, 0])
        q = question_card("Cell B sends less ligand: what happens to Cell A next?", y=3.25, max_w=10.6, size=30)
        self.add(w["all"], ret_arr, q_mark, q)

        self.play(FadeOut(q), FadeOut(q_mark), FadeOut(ret_arr), run_time=0.8)

        self.at("left cell receives less")
        self.play(w["tr_t"].animate.set_value(4.90), run_time=2.8, rate_func=linear)

        self.at("nerve program stays")
        nerve_on = boxed_label("Nerve: ON", AMBER, size=24, box=(1.92, 0.44)).move_to(w["nerve_a"])
        self.play(swap(w["nerve_a"], nerve_on, run_time=0.6), w["tr_t"].animate.set_value(5.45), run_time=2.0, rate_func=linear)

        self.at("even more ligand")
        extra_lig_a = VGroup(
            make_ligand(np.array([-CLEFT_HALF, 2.48, 0]), RIGHT),
            make_ligand(np.array([-CLEFT_HALF, -0.10, 0]), RIGHT),
        )
        self.play(
            FadeIn(extra_lig_a, shift=RIGHT * 0.15),
            w["tr_t"].animate.set_value(6.05),
            run_time=2.4,
            rate_func=linear,
        )

        # Build the loop label word by word in time with the narration:
        # "Left ⊣ right's sending ⊣ left's sending = left boosts left"
        lbl_p1 = T("Left \u22a3 right's sending", size=26, color=AMBER)
        lbl_p2 = T("\u22a3 left's sending", size=26, color=TEAL)
        lbl_p3 = T("= left boosts left", size=26, color=GOLD)
        loop_lbl = VGroup(lbl_p1, lbl_p2, lbl_p3).arrange(RIGHT, buff=0.14).move_to([0.0, 3.22, 0])
        fit(loop_lbl, max_w=12.2)

        top_arc = CurvedArrow([-0.72, 2.66, 0], [0.72, 2.66, 0], angle=-0.32, color=AMBER, stroke_width=4.5, tip_length=0.18)
        bot_arc = CurvedArrow([0.72, -0.56, 0], [-0.72, -0.56, 0], angle=-0.32, color=TEAL, stroke_width=4.0, tip_length=0.18)

        self.at("The left cell lowers")
        self.play(
            Create(top_arc),
            FadeIn(lbl_p1, shift=RIGHT * 0.08),
            w["tr_t"].animate.set_value(6.30),
            run_time=2.2,
            rate_func=linear,
        )

        self.at("right cell's sending lowers")
        self.play(
            Create(bot_arc),
            FadeIn(lbl_p2, shift=RIGHT * 0.08),
            w["tr_t"].animate.set_value(6.55),
            run_time=2.2,
            rate_func=linear,
        )

        self.at("Two breaks in a row")
        self.play(
            top_arc.animate.set_stroke(width=6.0),
            bot_arc.animate.set_color(GOLD).set_stroke(width=5.5),
            w["tr_t"].animate.set_value(6.75),
            run_time=2.6,
            rate_func=linear,
        )

        self.at("boosts the left cell")
        self.play(
            FadeIn(lbl_p3, shift=RIGHT * 0.08),
            w["tr_t"].animate.set_value(6.85),
            run_time=1.8,
            rate_func=linear,
        )

        self.at("When notch lowers")
        self.play(w["tr_t"].animate.set_value(7.00), run_time=4.2, rate_func=linear)
        self.finish()


class S07Diverge(SpokenScene):
    def construct(self):
        w = make_two_cell_world(
            t_val=7.0, show_plot=True,
            fate_a="Nerve: ON", fate_b="Nerve: blocked",
            b_repressor=True, a_amber_count=5, b_amber_count=1, b_dim=True,
        )
        self.add(w["all"])

        # Continuously tint Cell A toward amber and Cell B toward teal as computed ODE diverges
        def tint_cells(_mob):
            da, db, _, _ = two_cell_state(w["tr_t"].get_value())
            aa = float(np.clip((da - 0.70) / 0.30, 0.0, 1.0))
            ab = float(np.clip((0.30 - db) / 0.21, 0.0, 1.0))
            w["cell_a"].set_stroke(interpolate_color(ManimColor(CELL_STROKE), ManimColor(AMBER), aa), width=3.5 + aa)
            w["cell_a"].set_fill(interpolate_color(ManimColor(CELL_FILL), ManimColor(AMBER), aa * 0.14), opacity=0.92)
            w["cell_b"].set_stroke(interpolate_color(ManimColor(CELL_STROKE), ManimColor(TEAL), ab), width=3.5 + ab)
            w["cell_b"].set_fill(interpolate_color(ManimColor(CELL_FILL), ManimColor(TEAL), ab * 0.14), opacity=0.92)

        w["cell_a"].add_updater(tint_cells)
        self.at("Watch the schematic curves")
        self.play(w["tr_t"].animate.set_value(10.8), run_time=6.4, rate_func=linear)

        self.at("left cell sends without")
        sender_a = boxed_label("Sender: nerve", AMBER, size=24, box=(1.96, 0.44)).move_to(w["nerve_a"])
        self.play(
            w["head_a"].animate.set_color(AMBER),
            FadeOut(w["recs_a"]),
            swap(w["nerve_a"], sender_a, run_time=0.8),
            run_time=0.8,
        )
        self.play(w["tr_t"].animate.set_value(11.6), run_time=3.2, rate_func=linear)

        self.at("right cell receives without")
        recv_b = boxed_label("Receiver: skin", TEAL, size=24, box=(1.96, 0.44)).move_to(w["nerve_b"])
        self.play(
            w["head_b"].animate.set_color(TEAL),
            FadeOut(w["ligs_b"]),
            swap(w["nerve_b"], recv_b, run_time=0.8),
            run_time=0.8,
        )
        self.play(w["tr_t"].animate.set_value(12.0), run_time=3.2, rate_func=linear)
        w["cell_a"].remove_updater(tint_cells)

        p1 = Dot([0.80, 0.90, 0], radius=0.14, color=CYAN)
        self.add(p1)
        self.play(p1.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14), run_time=0.9, rate_func=linear)
        self.remove(p1)

        self.at("Biologists call")
        banner = T("Lateral inhibition", size=34, color=GOLD, weight=BOLD).move_to([0.0, 3.22, 0])
        self.play(FadeIn(banner), run_time=0.5)

        self.at("lateral inhibition")
        p2 = Dot([0.80, 1.25, 0], radius=0.14, color=CYAN)
        self.add(p2)
        self.play(p2.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14), run_time=1.6, rate_func=linear)
        self.remove(p2)
        self.finish()


class S08Sheet(SpokenScene):
    def construct(self):
        shift = np.array([-1.0, -0.05, 0.0])
        centers = _HEX_CENTERS + shift

        hex_cells = VGroup()
        for i in range(25):
            if i == 12:
                sc, fo = AMBER, 0.65
            elif i == 13:
                sc, fo = TEAL, 0.55
            else:
                sc, fo = CELL_STROKE, 0.20
            hex_cells.add(hex_polygon(centers[i], radius=0.56, color=sc, fill_color=sc, fill_opacity=fo))

        big_a = hex_polygon(np.array([-1.5, 0.1, 0]), radius=1.55, color=AMBER, fill_color=AMBER, fill_opacity=0.65)
        big_b = hex_polygon(np.array([1.2, 0.1, 0]), radius=1.55, color=TEAL, fill_color=TEAL, fill_opacity=0.55)
        lbl_a = T("A", size=34, color=TEXT, weight=BOLD).move_to(big_a)
        lbl_b = T("B", size=34, color=TEXT, weight=BOLD).move_to(big_b)
        self.add(big_a, big_b, lbl_a, lbl_b)

        self.at("zoom out from")
        sheet_title = T("Schematic cell sheet", size=32, color=TEXT).move_to([-1.0, 3.22, 0])
        leg = VGroup(
            boxed_label("Nerve (sender)", AMBER, size=24, box=(2.5, 0.48)),
            boxed_label("Skin (receiver)", TEAL, size=24, box=(2.5, 0.48)),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.25, 0.85, 0])
        self.play(FadeOut(lbl_a), FadeOut(lbl_b), run_time=0.35)
        pair_target = VGroup(hex_cells[12], hex_cells[13])
        self.play(ReplacementTransform(VGroup(big_a, big_b), pair_target), run_time=1.3)
        others = VGroup(*[hex_cells[i] for i in range(25) if i not in (12, 13)])
        self.play(FadeIn(others), FadeIn(sheet_title), FadeIn(leg), run_time=2.0)
        # Swap separate groups for unified hex_cells so updaters animate all 25 hexagons!
        self.remove(pair_target, others)
        self.add(hex_cells)

        self.at("Because the notch signal")
        contact_tag = T("Contact only —\nno diffusion", size=24, color=TEXT, line_spacing=0.85).move_to([4.25, -0.55, 0])
        self.play(FadeIn(contact_tag), run_time=1.2)
        # Pulse cell 12's border while explaining contact-only
        self.play(Indicate(hex_cells[12], color=AMBER, scale_factor=1.06), run_time=2.0)

        self.at("compares itself only")
        nbr_arrows = VGroup(*[
            Arrow(centers[12] + (centers[j] - centers[12]) * 0.25,
                  centers[12] + (centers[j] - centers[12]) * 0.72,
                  color=AMBER, stroke_width=4.5, buff=0, max_tip_length_to_length_ratio=0.35)
            for j in _HEX_ADJ[12]
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in nbr_arrows], lag_ratio=0.14), run_time=3.5)

        self.at("Every emerging nerve")
        step_tr = ValueTracker(0.0)
        n_steps = len(_SHEET_D) - 1

        def update_sheet(grp):
            idx = int(np.clip(round(step_tr.get_value() * n_steps), 0, n_steps))
            d_vec = _SHEET_D[idx]
            for i in range(25):
                col, fop = hex_color_for_D(d_vec[i])
                grp[i].set_stroke(col, width=3.5 if d_vec[i] > 0.6 else 2.5)
                grp[i].set_fill(col, opacity=fop)

        hex_cells.add_updater(update_sheet)
        self.play(FadeOut(nbr_arrows), step_tr.animate.set_value(1.0), run_time=4.3, rate_func=linear)
        hex_cells.remove_updater(update_sheet)

        self.at("leaving spaced nerve")
        ring_highlights = VGroup(*[
            hex_polygon(centers[j], radius=0.56, color=EMERALD, fill_color=TEAL, fill_opacity=0.0, stroke_width=4.5)
            for j in _HEX_ADJ[12]
        ])
        ring_note = T("No two\nsenders touch", size=24, color=GOLD, line_spacing=0.85).move_to([4.25, -1.55, 0])
        self.play(FadeIn(ring_highlights), FadeIn(ring_note), run_time=1.4)
        self.play(Indicate(ring_highlights, color=EMERALD, scale_factor=1.05), run_time=1.8)
        self.finish()


class S09ReachAndFlex(SpokenScene):
    def construct(self):
        shift = np.array([-0.8, -0.05, 0.0])
        centers = _HEX_CENTERS + shift
        d_start = _SHEET_D[-1]

        hex_cells = VGroup()
        for i in range(25):
            col, fop = hex_color_for_D(d_start[i])
            hex_cells.add(hex_polygon(centers[i], radius=0.56, color=col, fill_color=col, fill_opacity=fop, stroke_width=3))

        banner = T("Thin extensions (schematic)", size=30, color=TEXT).move_to([-0.8, 3.22, 0])
        self.add(hex_cells, banner)

        self.at("Cells can also tune")
        sheet_pivot = centers[12].copy()
        self.play(hex_cells.animate.scale(1.22, about_point=sheet_pivot), run_time=4.8)

        scaled_centers = np.array([h.get_center() for h in hex_cells])
        c12 = scaled_centers[12]

        target_ids = [2, 5, 8, 15, 18, 22]
        targets = [scaled_centers[j] for j in target_ids]
        phase = ValueTracker(0.0)

        def make_filopodia():
            t = phase.get_value()
            g = VGroup()
            for k, tgt in enumerate(targets):
                vec = tgt - c12
                dist = np.linalg.norm(vec)
                u = vec / max(dist, 1e-6)
                perp = np.array([-u[1], u[0], 0.0])
                reach = min(1.0, t / 2.4)
                p0 = c12 + u * 0.42
                p3 = c12 + u * (0.42 + (dist - 0.50) * reach)
                sway = 0.22 * np.sin(2.8 * t + k * 1.4)
                p1 = p0 + (p3 - p0) * 0.35 + perp * sway
                p2 = p0 + (p3 - p0) * 0.70 - perp * sway * 0.85
                fil = VMobject(stroke_color=AMBER, stroke_width=4.5)
                fil.set_points_smoothly([p0, p1, p2, p3])
                tip = Dot(p3, radius=0.10, color=AMBER)
                g.add(fil, tip)
            return g

        self.at("send out thin moving")
        fils = always_redraw(make_filopodia)
        self.add(fils)
        self.play(phase.animate.set_value(2.4), run_time=2.25, rate_func=linear)

        self.at("touch neighbors a few")
        touch_rings = VGroup(*[
            Circle(radius=0.24, color=TEAL, stroke_width=4.5).move_to(tgt)
            for tgt in targets
        ])
        self.play(FadeIn(touch_rings), phase.animate.set_value(10.0), run_time=5.5, rate_func=linear)

        self.at("help space the bristles")
        ext_tr = ValueTracker(0.0)
        n_ext = len(_EXT_D) - 1

        def update_ext(grp):
            idx = int(np.clip(round(ext_tr.get_value() * n_ext), 0, n_ext))
            d_vec = _EXT_D[idx]
            for i in range(25):
                col, fop = hex_color_for_D(d_vec[i])
                grp[i].set_stroke(col, width=3.5 if d_vec[i] > 0.6 else 2.5)
                grp[i].set_fill(col, opacity=fop)

        hex_cells.add_updater(update_ext)
        note_space = fit_text("Wider bristle spacing via touch", max_w=3.1, size=24, color=TEAL).move_to([4.50, 0.0, 0])
        self.play(
            FadeOut(touch_rings),
            FadeIn(note_space),
            ext_tr.animate.set_value(1.0),
            phase.animate.set_value(15.0),
            run_time=4.0,
            rate_func=linear,
        )
        hex_cells.remove_updater(update_ext)

        rem = max(0.5, self.narration_s - self.elapsed())
        self.play(phase.animate.set_value(15.0 + 1.4 * rem), run_time=rem, rate_func=linear)
        self.finish()


class S10Closing(SpokenScene):
    def construct(self):
        w = make_two_cell_world(
            t_val=12.0, show_plot=True,
            fate_a="Sender: nerve", fate_b="Receiver: skin",
            b_repressor=True, a_amber_count=5, b_amber_count=0, b_dim=False,
        )
        w["cell_a"].set_stroke(AMBER, width=4.5).set_fill(AMBER, opacity=0.14)
        w["head_a"].set_color(AMBER)
        w["cell_b"].set_stroke(TEAL, width=4.5).set_fill(TEAL, opacity=0.14)
        w["head_b"].set_color(TEAL)
        w["recs_a"].set_opacity(0)
        w["ligs_b"].set_opacity(0)

        banner = T("Mutual brake -> opposite fates", size=32, color=GOLD).move_to([0.0, 3.22, 0])
        self.play(FadeIn(w["all"]), FadeIn(banner), run_time=1.2)

        self.at("turns a small starting")
        p0 = Dot([0.80, 0.95, 0], radius=0.14, color=CYAN)
        self.add(p0)
        self.play(
            p0.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14),
            Indicate(w["ligs_a"], color=AMBER, scale_factor=1.08),
            run_time=3.2,
            rate_func=linear,
        )
        self.remove(p0)

        self.at("Two neighbors need no")
        no_map = T("No outside map  |  No diffusing signal", size=26, color=TEXT).move_to([0.0, 3.22, 0])
        p0b = Dot([0.80, 1.35, 0], radius=0.14, color=CYAN)
        self.add(p0b)
        self.play(
            swap(banner, no_map, run_time=0.8),
            p0b.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14),
            run_time=3.6,
            rate_func=linear,
        )
        self.remove(p0b)

        self.at("weakening a")
        p1 = Dot([0.80, 0.90, 0], radius=0.14, color=CYAN)
        self.add(p1)
        self.play(
            p1.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14),
            Indicate(w["ligs_a"], color=AMBER, scale_factor=1.1),
            run_time=3.2,
            rate_func=linear,
        )
        self.remove(p1)

        self.at("grows into two opposite")
        p2 = Dot([0.80, 1.30, 0], radius=0.14, color=CYAN)
        self.add(p2)
        self.play(
            p2.animate.move_to(w["gene_b"].get_left() + LEFT * 0.14),
            Indicate(w["cell_a"], color=AMBER, scale_factor=1.02),
            Indicate(w["cell_b"], color=TEAL, scale_factor=1.02),
            run_time=2.6,
            rate_func=linear,
        )
        self.remove(p2)
        self.finish()


class S11End(EndCard):
    LINE = "When Notch lowers a cell's sending, equal neighbours split into opposite fates."
