"""Putting the Tool in One Cell Type (hacking-the-cell__chapter-2).

COLOUR MAP (one colour per concept across the entire film):
- NEURON_A       = "#89CFF0"  ice-blue: neuron type A
- NEURON_B       = "#A78BFA"  soft violet: neuron type B
- NEIGHBOR       = "#64748B"  muted slate: neighboring cells (cell stroke)
- NEIGHBOR_LABEL = "#CBD5E1"  bright cool slate-white: readable label for Neighbors
- REPORTER       = "#2ECC71"  emerald green: fluorescent reporter (GFP)
- ACTUATOR       = "#FB7185"  coral: light-gated actuator
- PROMOTER       = GOLD       gold: promoter & loxP sites
- STOP_COL       = "#EF4444"  crimson: STOP block / roadblock
- CRE_COL        = "#2DD4BF"  teal: Cre recombinase enzyme
- FLP_COL        = "#C084FC"  lavender: Flp recombinase enzyme & Flp sites
- TEXT           = "#E8EAF0"  off-white: DNA backbone, reading arrow, primary labels

ONE WORLD CARRIED:
- Upper tissue field of multipolar Neuron A (ice-blue), Neuron B (violet), and Neighbor (slate) cells
  paired with the lower chromosome / DNA track; when DNA editing is the focus, the DNA track enlarges
  across the center stage, then returns below the tissue field when cell-type targeting resumes.

WHAT CHANGES PER SCENE (and what it is computed from):
- s01_link_hook:    12 neurons extend neurites; reporter/actuator badges enter; a target bracket scans
                    cells and locks onto Type A; identical chromosome tracks appear inside all 12 nuclei
                    and expand into the lower DNA track with a reading window sweeping linearly over x.
- s02_transgene:    Transgene DNA glides into a schematic fertilized egg's chromosome, expands into a
                    two-block DNA bar, and a computed sinusoidal RNA ribbon y = A*sin(k*(x - v*t)) glides
                    off the coding block to build a protein badge.
- s03_green_mouse:  RNA packets travel from the active-everywhere GFP track to all 12 neurons, smoothly
                    ramping every cell and a schematic green mouse outline from dark to emerald (tracker
                    t in 0..1) while RNA ribbon flows, then a gold ring isolates Type A amid the green crowd.
- s04_cre_setup:    All 12 cells reset smoothly to dark baseline; DNA splits into Gene 1 + Gene 2 slot;
                    crimson STOP and two same-direction gold loxP triangles flank STOP; a reading capsule
                    travels from the promoter, hits STOP, and rebounds repeatedly (piecewise x(t) bounce).
- s05_cre_surprise: Teal Cre ring-clamps scan across the DNA and dock onto both loxP triangles while arms
                    stay connected, bend the intervening DNA upward into a computed arch, snip STOP away as
                    an encircled excised ring, rejoin with one loxP, and emit emerald RNA transcript packets.
- s06_address:      Type A promoter -> Cre drives Cre only inside Type A neurons; teal Cre clamps excise
                    their chromosome STOP bars, rejoin the reporter backbone, and ramp Type A glow 0->1
                    while Type B and Neighbors keep intact STOP bars and stay dark.
- s07_predict:      Zooms onto one Type A cell with a stop-free chromosome while a reading capsule sweeps;
                    computed mitosis separates it cleanly into two ice-blue daughters as Cre fades to 0;
                    question_card enters with a reporter-check cursor sweeping before the pause.
- s08_pause:        PredictPause holds the two-daughter stop-free backdrop and question_card while the
                    4.5 s countdown ring empties continuously.
- s09_reveal_caveat:Question clears; both daughters flare emerald green and divide into 4 green
                    descendants linked by lineage branches; panning left with full-size labels reveals a
                    neighbor where a brief Cre flash snips STOP and yields faint green leak flagged by a ring.
- s10_flp_wrap:     Tissue field + two DNA tracks (Cre/loxP -> Reporter, Flp/Flp sites -> Actuator);
                    lavender Flp clamps bypass gold loxP above the track, excise STOP only at lavender
                    diamonds, rejoin both backbones, and light Type A emerald and Type B coral.
"""
import numpy as np
from bp_parts import *

# ------------------------------------------------------------------ concept palette
NEURON_A = "#89CFF0"
NEURON_B = "#A78BFA"
NEIGHBOR = "#64748B"
NEIGHBOR_LABEL = "#CBD5E1"
REPORTER = "#2ECC71"
ACTUATOR = "#FB7185"
PROMOTER = GOLD
STOP_COL = "#EF4444"
CRE_COL = "#2DD4BF"
FLP_COL = "#C084FC"

# Deterministic 3x4 staggered tissue field layout (x, y, kind, seed)
TISSUE_LAYOUT = [
    (-4.9, 1.98, "A", 11),
    (-2.0, 2.04, "N", 12),
    (0.8, 1.98, "B", 13),
    (4.1, 2.02, "A", 14),
    (-3.5, 0.90, "B", 21),
    (-0.6, 0.94, "A", 22),
    (2.3, 0.94, "N", 23),
    (5.1, 0.86, "B", 24),
    (-4.8, -0.02, "N", 31),
    (-1.9, 0.00, "B", 32),
    (1.2, 0.00, "A", 33),
    (4.3, -0.02, "N", 34),
]

KIND_COLOR = {"A": NEURON_A, "B": NEURON_B, "N": NEIGHBOR}


def _lerp_col(c1, c2, alpha):
    return interpolate_color(ManimColor(c1), ManimColor(c2), float(np.clip(alpha, 0.0, 1.0)))


# ------------------------------------------------------------------ reusable biological drawings
def make_neuron(pos, kind="A", scale=1.0, glow=0.0, glow_color=REPORTER,
                show_dna=False, has_stop=True, has_cre=False, has_flp=False, seed=0):
    """Multipolar neuron (or compact neighbor cell) with rich soma fill, neurites, nucleus, and mini DNA."""
    rng = np.random.default_rng(seed)
    base_col = KIND_COLOR[kind]
    center = np.array([pos[0], pos[1], 0.0], dtype=float)
    r_soma = (0.52 if kind != "N" else 0.42) * scale

    fill_col = _lerp_col(_lerp_col(base_col, BG, 0.25), glow_color, glow)
    stroke_col = _lerp_col(base_col, glow_color, 0.45 * float(np.clip(glow, 0.0, 1.0)))

    g = VGroup()
    n_branches = 5 if kind != "N" else 3
    base_angles = np.linspace(0, TAU, n_branches, endpoint=False) + rng.uniform(-0.22, 0.22, n_branches)
    branches = VGroup()
    for idx, ang in enumerate(base_angles):
        length = r_soma * (1.56 if (kind != "N" and idx == 0) else rng.uniform(1.24, 1.45))
        p0 = center + r_soma * 0.85 * np.array([np.cos(ang), np.sin(ang), 0.0])
        p1 = center + length * np.array([np.cos(ang + 0.10), np.sin(ang + 0.10), 0.0])
        branches.add(Line(p0, p1, color=stroke_col, stroke_width=5.2 * scale))
        if kind != "N" and idx % 2 == 1:
            twig_ang = ang + rng.choice([-0.42, 0.42])
            p2 = p1 + r_soma * 0.40 * np.array([np.cos(twig_ang), np.sin(twig_ang), 0.0])
            branches.add(Line(p1, p2, color=stroke_col, stroke_width=3.6 * scale))
    g.add(branches)

    soma = Circle(radius=r_soma, color=stroke_col, stroke_width=4.8 * scale,
                  fill_color=fill_col, fill_opacity=0.96).move_to(center)
    g.add(soma)
    g.soma = soma

    nuc_w, nuc_h = r_soma * 1.14, r_soma * 0.66
    nuc = Ellipse(width=nuc_w, height=nuc_h, color=TEXT, stroke_width=2.2 * scale,
                  fill_color=BG, fill_opacity=0.92).move_to(center)
    g.add(nuc)

    if show_dna:
        track = Line(center + LEFT * (nuc_w * 0.36), center + RIGHT * (nuc_w * 0.36),
                     color=TEXT, stroke_width=2.8 * scale)
        g.add(track)
        if has_stop:
            stop_bar = Rectangle(width=nuc_w * 0.26, height=nuc_h * 0.46,
                                 color=STOP_COL, stroke_width=0, fill_color=STOP_COL, fill_opacity=1.0).move_to(center)
            g.add(stop_bar)
        else:
            site_dot = Dot(center, radius=0.060 * scale, color=PROMOTER if kind != "B" else FLP_COL)
            g.add(site_dot)

    if has_cre:
        cre = make_enzyme_clamp(center + DR * (r_soma * 0.62), color=CRE_COL, radius=0.14 * scale)
        g.add(cre)
    if has_flp:
        flp = make_enzyme_clamp(center + DL * (r_soma * 0.62), color=FLP_COL, radius=0.14 * scale, angle=PI)
        g.add(flp)

    return g


def build_tissue_field(scale=0.95, y_shift=0.0, glow_fn=None, show_dna=False,
                       stop_fn=None, cre_fn=None, flp_fn=None, layout=TISSUE_LAYOUT):
    """Build the 12-cell tissue field deterministically from TISSUE_LAYOUT."""
    field = VGroup()
    cells = []
    for x, y, kind, seed in layout:
        g_val, g_col = glow_fn(kind) if glow_fn else (0.0, REPORTER)
        has_stop = stop_fn(kind) if stop_fn else True
        has_cre = cre_fn(kind) if cre_fn else False
        has_flp = flp_fn(kind) if flp_fn else False
        c = make_neuron((x, y + y_shift), kind=kind, scale=scale, glow=g_val, glow_color=g_col,
                        show_dna=show_dna, has_stop=has_stop, has_cre=has_cre, has_flp=has_flp, seed=seed)
        field.add(c)
        cells.append((kind, c))
    field.cells = cells
    return field


def tissue_legend(y=3.35):
    """Top legend labels positioned completely above the highest neuron dendrites."""
    lbl_a = T("Type A", 28, NEURON_A).move_to([-4.9, y, 0])
    lbl_n = T("Neighbors", 28, NEIGHBOR_LABEL).move_to([-2.0, y, 0])
    lbl_b = T("Type B", 28, NEURON_B).move_to([0.8, y, 0])
    return VGroup(lbl_a, lbl_b, lbl_n)


def make_enzyme_clamp(center, color=CRE_COL, radius=0.45, angle=0.0):
    """Filled C-shaped enzyme clamp that grips DNA sites (no molecular structure)."""
    return AnnularSector(
        inner_radius=0.52 * radius,
        outer_radius=radius,
        start_angle=0.48 + angle,
        angle=TAU - 0.96,
        arc_center=np.array([center[0], center[1], 0.0]),
        color=color,
        fill_color=color,
        fill_opacity=0.90,
        stroke_width=2.0,
    )


def make_promoter_arrow(x_left, y, width=1.4, height=0.62, color=PROMOTER):
    """Bent transcription-start arrow sitting cleanly on a bold promoter bar."""
    base = Rectangle(width=width, height=0.16, color=color, stroke_width=0,
                     fill_color=color, fill_opacity=0.96).move_to([x_left + width / 2, y, 0])
    stem_x = x_left + 0.22
    stem = Line([stem_x, y, 0], [stem_x, y + height, 0], color=color, stroke_width=5.8)
    top_arm = Arrow([stem_x - 0.02, y + height, 0], [stem_x + 0.95, y + height, 0],
                    buff=0, color=color, stroke_width=5.8, max_tip_length_to_length_ratio=0.32)
    return VGroup(base, stem, top_arm)


def make_site_marker(center, kind="loxp", scale=1.0):
    """Right-pointing gold triangle for loxP or lavender diamond for Flp site."""
    c = np.array([center[0], center[1], 0.0])
    if kind == "loxp":
        pts = [c + np.array([-0.22 * scale, 0.30 * scale, 0]),
               c + np.array([-0.22 * scale, -0.30 * scale, 0]),
               c + np.array([0.30 * scale, 0.0, 0])]
        return Polygon(*pts, color=PROMOTER, stroke_width=3.2, fill_color=PROMOTER, fill_opacity=0.96)
    pts = [c + np.array([0, 0.32 * scale, 0]),
           c + np.array([0.26 * scale, 0, 0]),
           c + np.array([0, -0.32 * scale, 0]),
           c + np.array([-0.26 * scale, 0, 0])]
    return Polygon(*pts, color=FLP_COL, stroke_width=3.2, fill_color=FLP_COL, fill_opacity=0.96)


def make_dna_block(text, center, width, height=0.88, color=REPORTER, size=28, fill_opacity=0.52):
    """DNA coding/stop block whose box fits the text cleanly with zero overflow."""
    lab = fit_text(text, max_w=width - 0.20, size=size, color=TEXT, min_size=24, max_lines=1)
    box = RoundedRectangle(corner_radius=0.14, width=max(width, lab.width + 0.32), height=height,
                           stroke_color=color, stroke_width=4.0, fill_color=color, fill_opacity=fill_opacity).move_to(center)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box, g.label = box, lab
    return g


def connect_dna_segments(points_or_mobs, y, color=TEXT, stroke=6.0):
    """Draw horizontal backbone segments ONLY in the gaps between blocks (never crossing labels)."""
    segs = VGroup()
    for a, b in zip(points_or_mobs[:-1], points_or_mobs[1:]):
        x0 = a if isinstance(a, (int, float)) else a.get_right()[0]
        x1 = b if isinstance(b, (int, float)) else b.get_left()[0]
        if x1 - x0 > 0.03:
            segs.add(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=stroke))
    return segs


def rna_ribbon(x0, x1, y_base, phase, amp=0.22, freq=5.0, color=REPORTER):
    """Computed sinusoidal mRNA wave ribbon with moving transcript beads."""
    xs = np.linspace(x0, x1, 64)
    pts = [np.array([x, y_base + amp * np.sin(freq * (x - x0) - phase), 0.0]) for x in xs]
    curve = VMobject(stroke_color=color, stroke_width=6.5, fill_opacity=0)
    curve.set_points_as_corners(pts)
    beads = VGroup()
    span = x1 - x0
    for k in range(3):
        frac = ((phase * 0.14 + k / 3.0) % 1.0)
        bx = x0 + frac * span
        by = y_base + amp * np.sin(freq * (bx - x0) - phase)
        beads.add(Dot([bx, by, 0], radius=0.12, color=color))
    return VGroup(curve, beads)


def reading_capsule(x, y, color=TEXT):
    """Filled reading polymerase capsule moving along a DNA track."""
    body = RoundedRectangle(corner_radius=0.15, width=0.88, height=0.32,
                            color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.88).move_to([x, y, 0])
    tip = Triangle(color=color, fill_color=color, fill_opacity=0.96).scale(0.15).rotate(-PI / 2).next_to(body, RIGHT, buff=0.04)
    return VGroup(body, tip)


def schematic_mouse(center=(4.75, -1.78, 0), glow=0.0):
    """Clean schematic mouse silhouette (oval body, head, ear, tail) — never a molecular structure."""
    c = np.array(center, dtype=float)
    fill_col = _lerp_col(NEIGHBOR, REPORTER, glow)
    stroke_col = _lerp_col(TEXT, REPORTER, glow)
    op = 0.55 + 0.40 * float(np.clip(glow, 0.0, 1.0))
    body = Ellipse(width=1.70, height=1.00, color=stroke_col, stroke_width=3.8,
                   fill_color=fill_col, fill_opacity=op).move_to(c + LEFT * 0.15)
    head = Ellipse(width=0.78, height=0.60, color=stroke_col, stroke_width=3.8,
                   fill_color=fill_col, fill_opacity=op).move_to(c + RIGHT * 0.76 + UP * 0.08)
    ear = Circle(radius=0.23, color=stroke_col, stroke_width=3.2,
                 fill_color=fill_col, fill_opacity=op).move_to(c + RIGHT * 0.58 + UP * 0.42)
    eye = Dot(c + RIGHT * 0.90 + UP * 0.14, radius=0.06, color=TEXT)
    tail = ArcBetweenPoints(c + LEFT * 0.98 + DOWN * 0.05, c + LEFT * 1.60 + UP * 0.30,
                            angle=-0.9, color=stroke_col, stroke_width=4.2)
    return VGroup(tail, body, head, ear, eye)


def daughter_backdrop():
    """Exact end-state of s07_predict carried into s08_pause and s09_reveal_caveat."""
    g = VGroup()
    c_left = make_neuron((-2.65, 0.48), kind="A", scale=2.45, glow=0.0, show_dna=True, has_stop=False, seed=11)
    c_right = make_neuron((2.65, 0.48), kind="A", scale=2.45, glow=0.0, show_dna=True, has_stop=False, seed=14)
    # Top dendrite tip is at 0.48 + 2.45*0.52*1.56 = 2.47, well clear of y = 3.10 labels
    lbl_l = T("Daughter 1", 28, NEURON_A).move_to([-2.65, 3.12, 0])
    lbl_r = T("Daughter 2", 28, NEURON_A).move_to([2.65, 3.12, 0])
    no_cre = T("Cre = 0  |  STOP gone", 28, TEXT).move_to([0.0, -1.92, 0])
    g.add(c_left, c_right, lbl_l, lbl_r, no_cre)
    g.c_left, g.c_right, g.lbl_l, g.lbl_r, g.no_cre = c_left, c_right, lbl_l, lbl_r, no_cre
    return g


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Hacking the Cell: Reporters, Actuators and Genetic Tools"
    TITLE = "Putting the Tool in One Cell Type"


class S01LinkHook(SpokenScene):
    def construct(self):
        field = build_tissue_field(scale=0.95, y_shift=0.10)
        legend = tissue_legend(y=3.35)

        self.play(FadeIn(field, lag_ratio=0.05), FadeIn(legend),
                  run_time=min(1.5, max(0.3, self.t_of("glowing reporter") - 0.3)))

        self.at("glowing reporter")
        rep_badge = boxed_label("Reporter (glow)", REPORTER, size=28, fill_opacity=0.18).move_to([-3.3, -1.45, 0])
        self.play(FadeIn(rep_badge, shift=UP * 0.2), run_time=1.0)

        self.at("actuator")
        act_badge = boxed_label("Actuator (light gate)", ACTUATOR, size=28, fill_opacity=0.18).move_to([3.2, -1.45, 0])
        self.play(FadeIn(act_badge, shift=UP * 0.2), run_time=1.1)

        self.at("billions of cells")
        scan_pos = ValueTracker(0.0)
        scan_pts = [
            field.cells[2][1].soma.get_center(),
            field.cells[6][1].soma.get_center(),
            field.cells[4][1].soma.get_center(),
            field.cells[0][1].soma.get_center(),
        ]
        target_ring = always_redraw(lambda: DashedVMobject(
            Circle(radius=0.66, color=PROMOTER, stroke_width=5.2), num_dashes=18
        ).move_to(
            scan_pts[min(int(scan_pos.get_value()), 2)]
            * (1.0 - (scan_pos.get_value() % 1.0))
            + scan_pts[min(int(scan_pos.get_value()) + 1, 3)]
            * (scan_pos.get_value() % 1.0)
            if scan_pos.get_value() < 3.0 else scan_pts[3]
        ))
        q_tag = T("Target?", 28, PROMOTER).move_to([0.0, -1.45, 0])
        self.add(target_ring)
        self.play(FadeIn(q_tag), scan_pos.animate.set_value(3.0),
                  run_time=max(0.8, self.t_of("one chosen cell type") - 0.25 - self.elapsed()),
                  rate_func=linear)

        self.at("one chosen cell type")
        self.remove(target_ring)
        a_rings = VGroup(*[
            Circle(radius=0.64, color=PROMOTER, stroke_width=5.2).move_to(c.soma.get_center())
            for k, c in field.cells if k == "A"
        ])
        self.play(FadeIn(a_rings), FadeOut(q_tag),
                  rep_badge.animate.move_to([-3.6, -1.38, 0]),
                  act_badge.animate.move_to([3.6, -1.38, 0]),
                  run_time=max(1.2, self.t_of("same chromosomes") - 0.25 - self.elapsed()))

        self.at("same chromosomes")
        mini_tracks = VGroup()
        for _, c in field.cells:
            ctr = c.soma.get_center()
            mini_tracks.add(Line(ctr + LEFT * 0.19, ctr + RIGHT * 0.19, color=TEXT, stroke_width=3.2))
        chrom_bar = Line([-5.4, -2.50, 0], [5.4, -2.50, 0], color=TEXT, stroke_width=7.0)
        chrom_lbl = T("Same chromosomes in every cell", 28, TEXT).move_to([0.0, -3.10, 0])
        self.play(FadeIn(mini_tracks), Create(chrom_bar), FadeIn(chrom_lbl),
                  run_time=max(1.0, self.t_of("where a gene is read") - 0.25 - self.elapsed()))

        self.at("where a gene is read")
        read_x = ValueTracker(-4.4)
        window = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.14, width=2.8, height=0.66,
            stroke_color=PROMOTER, stroke_width=4.8, fill_color=PROMOTER, fill_opacity=0.45
        ).move_to([read_x.get_value(), -2.50, 0]))
        self.add(window)
        self.play(read_x.animate.set_value(4.0),
                  run_time=max(1.2, self.narration_s - self.elapsed() - 0.1), rate_func=linear)
        self.finish()


class S02Transgene(SpokenScene):
    def construct(self):
        chrom_bar = Line([-5.4, -2.50, 0], [5.4, -2.50, 0], color=TEXT, stroke_width=7.0)
        self.add(chrom_bar)

        egg = Circle(radius=1.80, color=TEXT, stroke_width=4.8,
                     fill_color=_lerp_col(TEXT, BG, 0.72), fill_opacity=0.92).move_to([-2.6, 1.05, 0])
        egg_nuc = Circle(radius=0.70, color=TEXT, stroke_width=3.5, fill_color=BG, fill_opacity=0.94).move_to([-2.6, 1.05, 0])
        egg_chrom = Line([-3.08, 1.05, 0], [-2.12, 1.05, 0], color=TEXT, stroke_width=4.8)
        egg_lbl = T("Fertilized egg", 30, TEXT).next_to(egg, UP, buff=0.22)

        trans_piece = RoundedRectangle(corner_radius=0.12, width=2.10, height=0.62,
                                       color=PROMOTER, stroke_width=4.0, fill_color=REPORTER, fill_opacity=0.65).move_to([3.0, 1.05, 0])
        trans_piece.set_z_index(10)
        trans_lbl = T("Transgene DNA", 30, PROMOTER).next_to(trans_piece, UP, buff=0.22)
        trans_lbl.set_z_index(10)

        self.at("transgene")
        self.play(FadeOut(chrom_bar, run_time=0.6), FadeIn(egg), FadeIn(egg_nuc), FadeIn(egg_chrom),
                  FadeIn(egg_lbl), FadeIn(trans_piece), FadeIn(trans_lbl), run_time=1.2)
        self.play(trans_piece.animate.move_to([0.9, 1.05, 0]),
                  trans_lbl.animate.move_to([0.9, 1.92, 0]),
                  run_time=max(0.6, self.t_of("fertilized egg") - 0.2 - self.elapsed()), rate_func=linear)

        self.at("fertilized egg")
        self.play(FadeOut(trans_lbl, run_time=0.4),
                  trans_piece.animate.scale(0.28).move_to([-2.6, 1.05, 0]),
                  run_time=max(0.8, self.t_of("two parts") - 0.25 - self.elapsed()))

        self.at("two parts")
        y_dna = -0.35
        prom_arrow = make_promoter_arrow(-5.1, y_dna, width=2.9, height=1.08, color=PROMOTER)
        code_block = make_dna_block("Coding sequence", [2.0, y_dna, 0], width=5.1, height=1.18,
                                    color=REPORTER, size=30, fill_opacity=0.55)
        backbone = connect_dna_segments([-5.9, prom_arrow[0], code_block, 5.9], y_dna, color=TEXT, stroke=6.5)
        self.play(FadeOut(egg), FadeOut(egg_nuc), FadeOut(egg_chrom), FadeOut(egg_lbl),
                  FadeOut(trans_piece),
                  Create(backbone), FadeIn(prom_arrow), FadeIn(code_block),
                  run_time=max(0.9, self.t_of("promoter") - 0.25 - self.elapsed()))

        self.at("promoter")
        prom_lbl = T("Promoter: where & when", 30, PROMOTER).move_to([-3.6, y_dna - 1.32, 0])
        scan_x = ValueTracker(-4.9)
        cap = always_redraw(lambda: reading_capsule(scan_x.get_value(), y_dna + 0.54, color=PROMOTER))
        self.play(FadeIn(prom_lbl, shift=UP * 0.15), run_time=0.7)
        self.add(cap)
        self.play(scan_x.animate.set_value(-2.1),
                  run_time=max(0.8, self.t_of("coding sequence") - 0.2 - self.elapsed()), rate_func=linear)
        self.remove(cap)

        self.at("coding sequence")
        code_lbl = T("Coding sequence: what is made", 30, REPORTER).move_to([2.1, y_dna - 1.32, 0])
        phase = ValueTracker(0.0)
        rna = always_redraw(lambda: rna_ribbon(
            -0.3, 4.2, y_dna + 1.52, phase.get_value(), amp=0.26, freq=4.5, color=REPORTER
        ))
        rna_lbl = T("RNA", 28, REPORTER).move_to([1.95, y_dna + 2.15, 0])
        prot_badge = boxed_label("Protein", REPORTER, size=30, fill_opacity=0.18).move_to([5.15, y_dna + 1.65, 0])
        self.add(rna)
        self.play(FadeIn(code_lbl, shift=UP * 0.15), FadeIn(rna_lbl), FadeIn(prot_badge, shift=RIGHT * 0.2),
                  phase.animate.set_value(20.0),
                  run_time=max(1.5, self.narration_s - self.elapsed() - 0.1), rate_func=linear)
        self.finish()


class S03GreenMouse(SpokenScene):
    def construct(self):
        glow_t = ValueTracker(0.0)
        field = build_tissue_field(scale=0.95, y_shift=0.10)
        y_dna = -2.15
        prom_arrow = make_promoter_arrow(-5.1, y_dna, width=2.2, height=0.78, color=PROMOTER)
        code_block = make_dna_block("Coding sequence", [1.3, y_dna, 0], width=4.0, height=0.90,
                                    color=REPORTER, size=28, fill_opacity=0.52)
        backbone = connect_dna_segments([-5.9, prom_arrow[0], code_block, 3.4], y_dna, color=TEXT, stroke=6.0)
        prom_lbl = T("Promoter: where & when", 28, PROMOTER).move_to([-3.7, y_dna - 0.90, 0])
        code_lbl = T("Coding sequence: what is made", 28, REPORTER).move_to([1.5, y_dna - 0.90, 0])
        self.add(field, backbone, prom_arrow, code_block, prom_lbl, code_lbl)

        self.at("promoter active")
        new_prom_lbl = T("Active everywhere", 28, PROMOTER).move_to([-3.8, y_dna - 0.90, 0])
        self.play(swap(prom_lbl, new_prom_lbl, run_time=0.8))

        self.at("green fluorescent protein")
        gfp_block = make_dna_block("GFP gene", [1.3, y_dna, 0], width=3.6, height=0.90,
                                   color=REPORTER, size=28, fill_opacity=0.56)
        new_code_lbl = T("Green fluorescent protein", 28, REPORTER).move_to([1.4, y_dna - 0.90, 0])
        new_backbone = connect_dna_segments([-5.9, prom_arrow[0], gfp_block, 3.4], y_dna, color=TEXT, stroke=6.0)
        self.play(FadeOut(backbone), FadeIn(new_backbone),
                  ReplacementTransform(code_block, gfp_block),
                  swap(code_lbl, new_code_lbl, run_time=0.6),
                  run_time=max(0.9, self.t_of("Every cell reads") - 0.25 - self.elapsed()))

        self.at("Every cell reads")
        rays = VGroup(*[
            Arrow([1.3, y_dna + 0.52, 0], c.soma.get_center() + DOWN * 0.28,
                  buff=0.05, color=REPORTER, stroke_width=3.8, max_tip_length_to_length_ratio=0.10)
            for _, c in field.cells
        ])
        rays.layout_ok = True
        live_field = always_redraw(lambda: build_tissue_field(
            scale=0.95, y_shift=0.10, glow_fn=lambda k: (glow_t.get_value(), REPORTER)
        ))
        self.remove(field)
        self.add(live_field)
        self.play(Create(rays, lag_ratio=0.04), glow_t.animate.set_value(0.45),
                  run_time=max(1.0, self.t_of("glowing green mouse") - 0.2 - self.elapsed()))

        self.at("glowing green mouse")
        live_mouse = always_redraw(lambda: schematic_mouse(center=(5.05, -1.72, 0), glow=glow_t.get_value()).scale(0.90))
        mouse_tag = T("schematic", 24, TEXT).move_to([5.05, -2.78, 0])
        self.add(live_mouse)
        self.play(FadeIn(mouse_tag), FadeOut(rays), glow_t.animate.set_value(1.0),
                  run_time=max(1.5, self.t_of("every neuron lights up") - 0.25 - self.elapsed()))

        self.at("every neuron lights up")
        wave_phase = ValueTracker(0.0)
        active_wave = always_redraw(lambda: rna_ribbon(
            -0.3, 3.0, y_dna + 1.04, wave_phase.get_value(), amp=0.18, freq=5.5, color=REPORTER
        ))
        self.add(active_wave)
        scan_t = ValueTracker(0.0)
        scan_pts = [
            np.array([TISSUE_LAYOUT[0][0], TISSUE_LAYOUT[0][1] + 0.10, 0]),
            np.array([TISSUE_LAYOUT[2][0], TISSUE_LAYOUT[2][1] + 0.10, 0]),
            np.array([TISSUE_LAYOUT[6][0], TISSUE_LAYOUT[6][1] + 0.10, 0]),
            np.array([TISSUE_LAYOUT[3][0], TISSUE_LAYOUT[3][1] + 0.10, 0]),
        ]
        iso_ring = always_redraw(lambda: Circle(radius=0.66, color=PROMOTER, stroke_width=5.2).move_to(
            scan_pts[min(int(scan_t.get_value()), 2)]
            * (1.0 - (scan_t.get_value() % 1.0))
            + scan_pts[min(int(scan_t.get_value()) + 1, 3)]
            * (scan_t.get_value() % 1.0)
            if scan_t.get_value() < 3.0 else scan_pts[3]
        ))
        self.add(iso_ring)
        self.play(wave_phase.animate.set_value(14.0), scan_t.animate.set_value(3.0),
                  run_time=max(1.2, self.t_of("isolate one cell type") - 0.2 - self.elapsed()), rate_func=linear)

        self.at("isolate one cell type")
        iso_lbl = T("Target: Type A only?", 28, PROMOTER).move_to([-3.4, -0.95, 0])
        self.play(FadeIn(iso_lbl), wave_phase.animate.set_value(24.0),
                  run_time=max(1.0, self.narration_s - self.elapsed() - 0.1), rate_func=linear)
        self.finish()


class S04CreSetup(SpokenScene):
    def construct(self):
        reset_t = ValueTracker(1.0)
        live_field = always_redraw(lambda: build_tissue_field(
            scale=0.92, y_shift=0.14, glow_fn=lambda k: (reset_t.get_value(), REPORTER)
        ))
        legend = tissue_legend(y=3.35)
        self.add(live_field, legend)
        self.play(reset_t.animate.set_value(0.0),
                  run_time=max(0.8, self.t_of("split the job") - 0.25 - self.elapsed()))
        self.remove(live_field)
        field = build_tissue_field(scale=0.92, y_shift=0.14)
        self.add(field)

        self.at("split the job")
        y1, y2 = -1.62, -3.02
        g1_tag = T("Gene 1", 28, REPORTER).move_to([-5.45, y1, 0])
        g2_box = RoundedRectangle(corner_radius=0.12, width=5.6, height=0.62,
                                  color=CRE_COL, stroke_width=3.2, fill_color=CRE_COL, fill_opacity=0.28).move_to([0.0, y2, 0])
        g2_tag = T("Gene 2 (next)", 28, CRE_COL).move_to(g2_box)
        self.play(FadeIn(g1_tag), FadeIn(g2_box), FadeIn(g2_tag),
                  run_time=max(1.0, self.t_of("behind a strong promoter") - 0.25 - self.elapsed()))

        self.at("behind a strong promoter")
        prom_arrow = make_promoter_arrow(-4.3, y1, width=1.6, height=0.65, color=PROMOTER)
        prom_lbl = T("Strong promoter", 28, PROMOTER).move_to([-3.5, y1 - 0.72, 0])
        rep_block = make_dna_block("Reporter", [4.1, y1, 0], width=2.5, height=0.80,
                                   color=REPORTER, size=28, fill_opacity=0.35)
        backbone = connect_dna_segments([-4.6, prom_arrow[0], rep_block, 5.9], y1, color=TEXT, stroke=5.8)
        self.play(Create(backbone), FadeIn(prom_arrow), FadeIn(prom_lbl), FadeIn(rep_block),
                  run_time=max(1.0, self.t_of("block it with a stop") - 0.25 - self.elapsed()))

        self.at("block it with a stop")
        stop_block = make_dna_block("STOP", [0.6, y1, 0], width=1.65, height=0.80,
                                    color=STOP_COL, size=28, fill_opacity=0.60)
        backbone2 = connect_dna_segments([-4.6, prom_arrow[0], stop_block, rep_block, 5.9], y1, color=TEXT, stroke=5.8)
        self.play(FadeOut(backbone), FadeIn(backbone2), FadeIn(stop_block, shift=DOWN * 0.25),
                  run_time=max(1.0, self.t_of("Flank that stop block") - 0.25 - self.elapsed()))

        self.at("Flank that stop block")
        lox_l = make_site_marker([-0.85, y1], kind="loxp", scale=1.12)
        lox_r = make_site_marker([2.05, y1], kind="loxp", scale=1.12)
        backbone3 = connect_dna_segments([-4.6, prom_arrow[0], lox_l, stop_block, lox_r, rep_block, 5.9],
                                         y1, color=TEXT, stroke=5.8)
        self.play(FadeOut(backbone2), FadeIn(backbone3),
                  FadeIn(lox_l, shift=RIGHT * 0.25), FadeIn(lox_r, shift=LEFT * 0.25),
                  run_time=max(1.0, self.t_of("pointing the same way") - 0.25 - self.elapsed()))

        self.at("pointing the same way")
        lox_lbl_l = T("loxP (34 bp)", 24, PROMOTER).move_to([-0.85, y1 - 0.72, 0])
        lox_lbl_r = T("loxP (34 bp)", 24, PROMOTER).move_to([2.05, y1 - 0.72, 0])
        self.play(FadeIn(lox_lbl_l), FadeIn(lox_lbl_r),
                  lox_l.animate.scale(1.18), lox_r.animate.scale(1.18), run_time=0.9)
        self.play(lox_l.animate.scale(1.0 / 1.18), lox_r.animate.scale(1.0 / 1.18),
                  run_time=max(0.5, self.t_of("stop intact") - 0.2 - self.elapsed()))

        self.at("stop intact")
        # Capsule moves at y1+0.56 up to rx=-0.50 so tip bumps against left edge of STOP
        rx = ValueTracker(-3.2)
        cap = always_redraw(lambda: reading_capsule(rx.get_value(), y1 + 0.56, color=TEXT))
        self.add(cap)
        self.play(rx.animate.set_value(-0.50), run_time=0.9, rate_func=linear)
        blocked = T("Blocked!", 28, STOP_COL).move_to([0.95, y1 + 0.84, 0])

        self.at("every cell stays dark")
        self.play(FadeIn(blocked), rx.animate.set_value(-2.3), run_time=0.65)
        self.play(rx.animate.set_value(-0.50), run_time=0.65)
        self.play(rx.animate.set_value(-2.1),
                  run_time=max(0.4, self.narration_s - self.elapsed() - 0.1))
        self.finish()


class S05CreSurprise(SpokenScene):
    def construct(self):
        y_dna = -0.85
        prom = make_promoter_arrow(-5.3, y_dna, width=1.6, height=0.86, color=PROMOTER)
        prom_lbl = T("Strong promoter", 28, PROMOTER).move_to([-4.5, y_dna - 1.05, 0])
        lox_l = make_site_marker([-1.9, y_dna], kind="loxp", scale=1.40)
        stop_block = make_dna_block("STOP", [0.0, y_dna, 0], width=1.75, height=1.00,
                                    color=STOP_COL, size=32, fill_opacity=0.60)
        lox_r = make_site_marker([1.9, y_dna], kind="loxp", scale=1.40)
        rep_block = make_dna_block("Reporter", [4.45, y_dna, 0], width=2.75, height=1.12,
                                   color=REPORTER, size=32, fill_opacity=0.36)
        lox_lbl_l = T("loxP", 26, PROMOTER).move_to([-1.9, y_dna - 1.05, 0])
        lox_lbl_r = T("loxP", 26, PROMOTER).move_to([1.9, y_dna - 1.05, 0])

        arms = always_redraw(lambda: VGroup(
            Line([prom[0].get_right()[0], y_dna, 0], [lox_l.get_left()[0], y_dna, 0], color=TEXT, stroke_width=6.5),
            Line([-5.8, y_dna, 0], [prom[0].get_left()[0], y_dna, 0], color=TEXT, stroke_width=6.5),
            Line([lox_r.get_right()[0], y_dna, 0], [rep_block.get_left()[0], y_dna, 0], color=TEXT, stroke_width=6.5),
            Line([rep_block.get_right()[0], y_dna, 0], [6.0, y_dna, 0], color=TEXT, stroke_width=6.5),
        ))
        inner_segs = connect_dna_segments([lox_l, stop_block, lox_r], y_dna, color=TEXT, stroke=6.5)
        self.add(arms, inner_segs, prom, prom_lbl, lox_l, stop_block, lox_r, rep_block, lox_lbl_l, lox_lbl_r)

        self.at("recombinase called")
        cre_l = make_enzyme_clamp([-4.3, 1.85], color=CRE_COL, radius=0.58)
        cre_r = make_enzyme_clamp([4.3, 1.85], color=CRE_COL, radius=0.58, angle=PI)
        cre_lbl = T("Cre recombinase", 30, CRE_COL).move_to([0.0, 3.35, 0])
        self.play(FadeIn(cre_l), FadeIn(cre_r), FadeIn(cre_lbl), run_time=0.9)
        self.play(cre_l.animate.move_to([-1.9, 1.25, 0]),
                  cre_r.animate.move_to([1.9, 1.25, 0]),
                  run_time=max(1.5, self.t_of("cuts and rejoins") - 0.25 - self.elapsed()), rate_func=linear)

        self.at("cuts and rejoins")
        self.play(cre_l.animate.move_to([-1.9, y_dna + 0.14, 0]),
                  cre_r.animate.move_to([1.9, y_dna + 0.14, 0]),
                  run_time=max(1.0, self.t_of("at lox") - 0.25 - self.elapsed()))

        self.at("at lox")
        self.play(Indicate(lox_l, color=PROMOTER), Indicate(lox_r, color=PROMOTER),
                  run_time=max(0.8, self.t_of("Here is the twist") - 0.25 - self.elapsed()))

        self.at("Here is the twist")
        stop_w_half = stop_block.width / 2
        loop_y = y_dna + 1.55
        loop_arc_l = ArcBetweenPoints([-0.90, y_dna + 0.15, 0], [-stop_w_half, loop_y, 0],
                                      angle=-1.05, color=TEXT, stroke_width=5.8)
        loop_arc_r = ArcBetweenPoints([stop_w_half, loop_y, 0], [0.90, y_dna + 0.15, 0],
                                      angle=-1.05, color=TEXT, stroke_width=5.8)
        self.play(
            FadeOut(inner_segs), FadeOut(lox_lbl_l), FadeOut(lox_lbl_r),
            cre_l.animate.move_to([-0.64, y_dna + 0.20, 0]),
            cre_r.animate.move_to([0.64, y_dna + 0.20, 0]),
            lox_l.animate.move_to([-0.90, y_dna + 0.15, 0]),
            lox_r.animate.move_to([0.90, y_dna + 0.15, 0]),
            stop_block.animate.move_to([0.0, loop_y, 0]),
            Create(loop_arc_l), Create(loop_arc_r),
            run_time=max(1.5, self.t_of("by deleting") - 0.25 - self.elapsed()),
        )

        self.at("by deleting")
        twist_lbl = T("Turns gene ON by deleting DNA", 30, CRE_COL).move_to([0.0, 3.35, 0])
        self.play(swap(cre_lbl, twist_lbl, run_time=0.7),
                  run_time=max(0.8, self.t_of("cuts out the stop") - 0.25 - self.elapsed()))

        self.at("cuts out the stop")
        excised_y = loop_y + 0.35
        excised_ring = Circle(radius=1.10, color=STOP_COL, stroke_width=4.8).move_to([0.0, excised_y, 0])
        single_lox = make_site_marker([0.0, y_dna], kind="loxp", scale=1.40)
        single_lox_lbl = T("1 loxP left", 26, PROMOTER).move_to([0.0, y_dna - 1.05, 0])
        self.remove(arms)
        clean_backbone = connect_dna_segments([-5.8, prom[0], single_lox, rep_block, 6.0], y_dna, color=TEXT, stroke=6.5)
        excised_group = VGroup(stop_block, excised_ring, lox_r)

        self.play(FadeOut(loop_arc_l), FadeOut(loop_arc_r), FadeIn(excised_ring),
                  stop_block.animate.move_to([0.0, excised_y, 0]),
                  lox_r.animate.scale(0.65).move_to(excised_ring.get_bottom()),
                  ReplacementTransform(lox_l, single_lox),
                  FadeIn(clean_backbone), FadeIn(single_lox_lbl),
                  run_time=max(0.8, self.t_of("clears the") - 0.25 - self.elapsed()))

        self.at("clears the")
        self.play(excised_group.animate.shift(LEFT * 3.8 + UP * 0.2).set_opacity(0.0),
                  FadeOut(cre_l), FadeOut(cre_r),
                  run_time=0.85)

        lit_rep = make_dna_block("Reporter", [4.45, y_dna, 0], width=2.75, height=1.12,
                                 color=REPORTER, size=32, fill_opacity=0.72)
        rx = ValueTracker(-3.7)
        cap = always_redraw(lambda: reading_capsule(rx.get_value(), y_dna + 0.92, color=REPORTER))
        self.add(cap)
        self.play(rx.animate.set_value(2.9),
                  run_time=max(0.55, self.t_of("build the tool") - 0.20 - self.elapsed()),
                  rate_func=linear)

        self.at("build the tool")
        self.play(ReplacementTransform(rep_block, lit_rep), run_time=0.25)
        phase = ValueTracker(0.0)
        rna = always_redraw(lambda: rna_ribbon(
            3.0, 5.9, y_dna + 1.48, phase.get_value(), amp=0.25, freq=5.5, color=REPORTER
        ))
        self.add(rna)
        self.play(phase.animate.set_value(14.0),
                  run_time=max(0.8, self.narration_s + 0.25 - self.elapsed()), rate_func=linear)
        self.finish()


class S06Address(SpokenScene):
    def construct(self):
        glow_a = ValueTracker(0.0)
        stop_a = {"val": True}
        cre_a = {"val": False}

        field = always_redraw(lambda: build_tissue_field(
            scale=0.94, y_shift=0.12, show_dna=True,
            glow_fn=lambda k: (glow_a.get_value() if k == "A" else 0.0, REPORTER),
            stop_fn=lambda k: stop_a["val"] if k == "A" else True,
            cre_fn=lambda k: cre_a["val"] if k == "A" else False,
        ))
        legend = tissue_legend(y=3.35)

        y_dna = -2.10
        prom_a = make_promoter_arrow(-5.6, y_dna, width=1.25, height=0.62, color=NEURON_A)
        cre_gene = make_dna_block("Cre", [-2.6, y_dna, 0], width=1.65, height=0.84,
                                  color=CRE_COL, size=28, fill_opacity=0.52)
        bb_l = connect_dna_segments([-6.0, prom_a[0], cre_gene, -1.45], y_dna, color=TEXT, stroke=5.5)
        lbl_ta = T("Type A promoter -> Cre", 26, NEURON_A).move_to([-3.75, y_dna - 0.86, 0])

        prom_s = make_promoter_arrow(-0.4, y_dna, width=1.1, height=0.62, color=PROMOTER)
        lox_l = make_site_marker([1.15, y_dna], kind="loxp", scale=1.10)
        stop_b = make_dna_block("STOP", [2.25, y_dna, 0], width=1.40, height=0.84,
                                color=STOP_COL, size=26, fill_opacity=0.60)
        lox_r = make_site_marker([3.35, y_dna], kind="loxp", scale=1.10)
        rep_b = make_dna_block("Reporter", [4.95, y_dna, 0], width=2.10, height=0.84,
                               color=REPORTER, size=26, fill_opacity=0.35)
        bb_r = connect_dna_segments([-0.8, prom_s[0], lox_l, stop_b, lox_r, rep_b, 6.1], y_dna, color=TEXT, stroke=5.5)
        lbl_rep = T("loxP - STOP - loxP -> Reporter", 26, TEXT).move_to([2.65, y_dna - 0.86, 0])

        self.add(field, legend, bb_l, prom_a, cre_gene, lbl_ta,
                 bb_r, prom_s, lox_l, stop_b, lox_r, rep_b, lbl_rep)

        self.at("So which cells")
        self.play(Indicate(lbl_ta, color=CRE_COL),
                  run_time=max(1.0, self.t_of("gene behind a promoter") - 0.25 - self.elapsed()))

        self.at("gene behind a promoter")
        act_arrows = VGroup(*[
            Arrow([-2.6, y_dna + 0.50, 0],
                  [x, y + 0.12 - 0.36, 0], buff=0.05, color=CRE_COL, stroke_width=3.8,
                  max_tip_length_to_length_ratio=0.10)
            for x, y, k, _ in TISSUE_LAYOUT if k == "A"
        ])
        act_arrows.layout_ok = True
        self.play(Create(act_arrows, lag_ratio=0.12),
                  run_time=max(1.0, self.t_of("neuron type A") - 0.25 - self.elapsed()))

        self.at("neuron type A")
        cre_a["val"] = True
        self.play(FadeOut(act_arrows),
                  run_time=max(0.8, self.t_of("snips out the stop") - 0.25 - self.elapsed()))

        self.at("snips out the stop")
        stop_a["val"] = False
        single_lox = make_site_marker([2.25, y_dna], kind="loxp", scale=1.10)
        clean_bb_r = connect_dna_segments([-0.8, prom_s[0], single_lox, rep_b, 6.1], y_dna, color=TEXT, stroke=5.5)
        new_lbl_rep = T("1 loxP -> Reporter (Type A)", 26, REPORTER).move_to([2.65, y_dna - 0.86, 0])
        self.play(FadeOut(stop_b), FadeOut(bb_r), FadeIn(clean_bb_r),
                  ReplacementTransform(lox_l, single_lox),
                  lox_r.animate.move_to([2.25, y_dna, 0]).set_opacity(0),
                  swap(lbl_rep, new_lbl_rep, run_time=0.6),
                  run_time=max(0.7, self.t_of("lights up green") - 0.2 - self.elapsed()))

        self.at("lights up green")
        lit_rep = make_dna_block("Reporter", [4.95, y_dna, 0], width=2.10, height=0.84,
                                 color=REPORTER, size=26, fill_opacity=0.72)
        phase = ValueTracker(0.0)
        rna_r = always_redraw(lambda: rna_ribbon(
            3.95, 6.0, y_dna + 0.84, phase.get_value(), amp=0.18, freq=5.5, color=REPORTER
        ))
        self.add(rna_r)
        self.play(glow_a.animate.set_value(1.0), ReplacementTransform(rep_b, lit_rep),
                  phase.animate(rate_func=linear).set_value(10.0),
                  run_time=max(1.1, self.t_of("Neighboring cells") - 0.25 - self.elapsed()))

        self.at("Neighboring cells")
        self.remove(rna_r)
        check_b = Circle(radius=0.64, color=NEURON_B, stroke_width=4.8).move_to([TISSUE_LAYOUT[2][0], TISSUE_LAYOUT[2][1] + 0.12, 0])
        check_n = Circle(radius=0.54, color=STOP_COL, stroke_width=4.8).move_to([TISSUE_LAYOUT[6][0], TISSUE_LAYOUT[6][1] + 0.12, 0])
        keep_lbl = T("No Cre  |  STOP intact", 28, STOP_COL).move_to([0.0, -1.10, 0])
        self.play(Create(check_b), Create(check_n), FadeIn(keep_lbl),
                  run_time=max(1.0, self.t_of("stay dark") - 0.25 - self.elapsed()))

        self.at("stay dark")
        stop_bars = VGroup(*[
            Rectangle(
                width=0.18 if k == "B" else 0.15,
                height=0.18 if k == "B" else 0.15,
                color=STOP_COL, stroke_width=2.5, fill_color=STOP_COL, fill_opacity=1.0
            ).move_to([x, y + 0.12, 0])
            for x, y, k, _ in TISSUE_LAYOUT if k in ("B", "N")
        ])
        self.add(stop_bars)
        self.play(*[Indicate(bar, color="#FF8A8A", scale_factor=1.65, rate_func=there_and_back) for bar in stop_bars],
                  run_time=max(0.8, self.narration_s - self.elapsed() - 0.1))
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        glow_p = ValueTracker(0.95)
        parent = always_redraw(lambda: make_neuron(
            (0.0, 0.48), kind="A", scale=2.55, glow=glow_p.get_value(), glow_color=REPORTER,
            show_dna=True, has_stop=False, has_cre=True, seed=11
        ))
        p_lbl = T("Neuron A", 30, NEURON_A).move_to([0.0, 3.18, 0])

        y_bar = -1.98
        prom = make_promoter_arrow(-3.6, y_bar, width=1.15, height=0.58, color=PROMOTER)
        lox = make_site_marker([-1.25, y_bar], kind="loxp", scale=1.22)
        rep = make_dna_block("Reporter", [1.55, y_bar, 0], width=2.6, height=0.84,
                             color=REPORTER, size=28, fill_opacity=0.58)
        bb = connect_dna_segments([-4.0, prom[0], lox, rep, 3.4], y_bar, color=TEXT, stroke=5.5)
        bar_lbl = T("STOP removed permanently", 28, PROMOTER).move_to([0.0, y_bar - 0.82, 0])

        self.at("Pause here")
        self.add(parent)
        self.play(FadeIn(p_lbl), Create(bb), FadeIn(prom), FadeIn(lox), FadeIn(rep), FadeIn(bar_lbl),
                  run_time=1.0)
        rx = ValueTracker(-2.5)
        cap = always_redraw(lambda: reading_capsule(rx.get_value(), y_bar + 0.72, color=REPORTER))
        self.add(cap)
        self.play(rx.animate.set_value(0.2),
                  run_time=max(0.8, self.t_of("removed that stop block") - 0.25 - self.elapsed()), rate_func=linear)

        self.at("removed that stop block")
        self.play(rx.animate.set_value(2.6), Indicate(lox, color=PROMOTER),
                  run_time=max(1.0, self.t_of("for good") - 0.25 - self.elapsed()), rate_func=linear)

        self.at("for good")
        self.remove(cap)
        self.play(glow_p.animate.set_value(0.0),
                  FadeOut(bb), FadeOut(prom), FadeOut(lox), FadeOut(rep), FadeOut(bar_lbl),
                  run_time=max(0.9, self.t_of("later divides") - 0.25 - self.elapsed()))

        self.at("later divides")
        self.remove(parent)
        split_t = ValueTracker(0.0)
        div_cells = always_redraw(lambda: VGroup(
            make_neuron((-2.65 * split_t.get_value(), 0.48), kind="A",
                        scale=2.55 - 0.10 * split_t.get_value(), glow=0.0,
                        show_dna=True, has_stop=False, has_cre=True, seed=11),
            make_neuron((2.65 * split_t.get_value(), 0.48), kind="A",
                        scale=2.55 - 0.10 * split_t.get_value(), glow=0.0,
                        show_dna=True, has_stop=False, has_cre=True, seed=14),
        ))
        bd = daughter_backdrop()
        self.add(div_cells)
        self.play(split_t.animate.set_value(1.0), FadeOut(p_lbl),
                  FadeIn(bd.lbl_l), FadeIn(bd.lbl_r),
                  run_time=max(1.2, self.t_of("stop making") - 0.25 - self.elapsed()))

        self.at("stop making")
        self.remove(div_cells)
        c_l_cre = make_neuron((-2.65, 0.48), kind="A", scale=2.45, glow=0.0, show_dna=True,
                              has_stop=False, has_cre=True, seed=11)
        c_r_cre = make_neuron((2.65, 0.48), kind="A", scale=2.45, glow=0.0, show_dna=True,
                              has_stop=False, has_cre=True, seed=14)
        self.add(c_l_cre, c_r_cre)
        self.play(ReplacementTransform(c_l_cre, bd.c_left),
                  ReplacementTransform(c_r_cre, bd.c_right),
                  FadeIn(bd.no_cre),
                  run_time=max(1.0, self.t_of("Do those daughter cells") - 0.25 - self.elapsed()))

        self.at("Do those daughter cells")
        q = question_card("Do daughter cells still make the reporter?")
        # Highlight both unlocked daughter nuclei sequentially as the question finishes
        chk = Circle(radius=1.18, color=PROMOTER, stroke_width=4.5).move_to([-2.65, 0.48, 0])
        self.play(FadeIn(q.question), Create(chk), run_time=1.0)
        self.play(chk.animate.move_to([2.65, 0.48, 0]), run_time=1.3)
        self.play(FadeOut(chk), run_time=max(0.4, self.narration_s - self.elapsed() - 0.1))
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Do daughter cells still make the reporter?"
    SECONDS = 4.5

    def backdrop(self):
        return daughter_backdrop()


class S09RevealCaveat(SpokenScene):
    def construct(self):
        bd = daughter_backdrop()
        q = question_card("Do daughter cells still make the reporter?")
        self.add(bd, q.question)

        self.at("Yes")
        glow_d = ValueTracker(0.0)
        self.remove(bd.c_left, bd.c_right)
        live_daughters = always_redraw(lambda: VGroup(
            make_neuron((-2.65, 0.48), kind="A", scale=2.45, glow=glow_d.get_value(), glow_color=REPORTER,
                        show_dna=True, has_stop=False, seed=11),
            make_neuron((2.65, 0.48), kind="A", scale=2.45, glow=glow_d.get_value(), glow_color=REPORTER,
                        show_dna=True, has_stop=False, seed=14),
        ))
        self.add(live_daughters)
        ans = T("Yes — unlocked gene inherited", 28, REPORTER).move_to([0.0, -1.92, 0])
        self.play(FadeOut(q.question), glow_d.animate.set_value(1.0),
                  swap(bd.no_cre, ans, run_time=0.7),
                  run_time=max(1.2, self.t_of("stop block is gone") - 0.25 - self.elapsed()))

        self.at("stop block is gone")
        hl_l = Circle(radius=1.35, color=PROMOTER, stroke_width=4.5).move_to([-2.65, 0.48, 0])
        hl_r = Circle(radius=1.35, color=PROMOTER, stroke_width=4.5).move_to([2.65, 0.48, 0])
        self.play(Create(hl_l), Create(hl_r), run_time=0.9)
        self.play(FadeOut(hl_l), FadeOut(hl_r),
                  run_time=max(0.6, self.t_of("every descendant") - 0.25 - self.elapsed()))

        self.at("every descendant")
        self.remove(live_daughters)
        lit_l = make_neuron((-2.65, 0.48), kind="A", scale=2.45, glow=1.0, glow_color=REPORTER,
                            show_dna=True, has_stop=False, seed=11)
        lit_r = make_neuron((2.65, 0.48), kind="A", scale=2.45, glow=1.0, glow_color=REPORTER,
                            show_dna=True, has_stop=False, seed=14)
        self.add(lit_l, lit_r)

        lineage_title = T("Lineage traced", 30, REPORTER).move_to([0.0, 3.15, 0])
        desc_xs = [-4.5, -1.5, 1.5, 4.5]
        desc_cells = VGroup(*[
            make_neuron((dx, -0.18), kind="A", scale=1.48, glow=1.0, glow_color=REPORTER,
                        show_dna=True, has_stop=False, seed=40 + i)
            for i, dx in enumerate(desc_xs)
        ])
        parent_node = Dot([0.0, 2.35, 0], radius=0.16, color=NEURON_A)
        d_nodes = [Dot([-3.0, 1.35, 0], radius=0.14, color=REPORTER),
                   Dot([3.0, 1.35, 0], radius=0.14, color=REPORTER)]
        branches = VGroup(
            Line(parent_node.get_center(), d_nodes[0].get_center(), color=NEURON_A, stroke_width=4.5),
            Line(parent_node.get_center(), d_nodes[1].get_center(), color=NEURON_A, stroke_width=4.5),
            Line(d_nodes[0].get_center(), desc_cells[0].soma.get_top() + UP * 0.14, color=REPORTER, stroke_width=4.0),
            Line(d_nodes[0].get_center(), desc_cells[1].soma.get_top() + UP * 0.14, color=REPORTER, stroke_width=4.0),
            Line(d_nodes[1].get_center(), desc_cells[2].soma.get_top() + UP * 0.14, color=REPORTER, stroke_width=4.0),
            Line(d_nodes[1].get_center(), desc_cells[3].soma.get_top() + UP * 0.14, color=REPORTER, stroke_width=4.0),
        )
        self.play(FadeOut(bd.lbl_l), FadeOut(bd.lbl_r), FadeOut(ans),
                  FadeIn(lineage_title), FadeIn(parent_node), FadeIn(d_nodes[0]), FadeIn(d_nodes[1]),
                  Create(branches),
                  ReplacementTransform(lit_l, VGroup(desc_cells[0], desc_cells[1])),
                  ReplacementTransform(lit_r, VGroup(desc_cells[2], desc_cells[3])),
                  run_time=max(2.0, self.t_of("trace cell lineages") - 0.25 - self.elapsed()))

        self.at("trace cell lineages")
        desc_lbl = T("4 descendants — all green", 28, REPORTER).move_to([0.0, -2.05, 0])
        self.play(FadeIn(desc_lbl), Indicate(branches, color=PROMOTER, scale_factor=1.0),
                  run_time=max(1.2, self.t_of("carries a catch") - 0.25 - self.elapsed()))

        self.at("carries a catch")
        tree_geom = VGroup(parent_node, d_nodes[0], d_nodes[1], branches, desc_cells)
        lineage_title_sm = T("Lineage traced", 28, REPORTER).move_to([-3.2, 2.35, 0])
        desc_lbl_sm = T("4 green descendants", 26, REPORTER).move_to([-3.2, -1.70, 0])
        neighbor_dark = make_neuron((3.6, 0.25), kind="N", scale=2.15, glow=0.0,
                                    show_dna=True, has_stop=True, seed=55)
        n_lbl = T("Unintended neighbor", 28, NEIGHBOR_LABEL).move_to([3.6, 2.35, 0])
        self.play(tree_geom.animate.scale(0.64).move_to([-3.2, 0.35, 0]),
                  ReplacementTransform(lineage_title, lineage_title_sm),
                  ReplacementTransform(desc_lbl, desc_lbl_sm),
                  FadeIn(neighbor_dark), FadeIn(n_lbl),
                  run_time=max(1.2, self.t_of("Brief early") - 0.25 - self.elapsed()))

        self.at("Brief early")
        flash_cre = make_enzyme_clamp([3.6, 0.25], color=CRE_COL, radius=0.54)
        cre_note = T("Brief early Cre!", 28, CRE_COL).move_to([3.6, -1.70, 0])
        self.play(FadeIn(flash_cre), FadeIn(cre_note),
                  run_time=max(0.7, self.t_of("unlock unintended cells") - 0.25 - self.elapsed()))

        self.at("unlock unintended cells")
        neighbor_leaked = make_neuron((3.6, 0.25), kind="N", scale=2.15, glow=0.85, glow_color=REPORTER,
                                      show_dna=True, has_stop=False, seed=55)
        leak_note = T("Early leak?", 28, PROMOTER).move_to([3.6, -1.70, 0])
        self.play(FadeOut(flash_cre),
                  ReplacementTransform(neighbor_dark, neighbor_leaked),
                  swap(cre_note, leak_note, run_time=0.5),
                  run_time=max(1.1, self.t_of("check every") - 0.25 - self.elapsed()))

        self.at("check every")
        check_ring = Circle(radius=1.24, color=PROMOTER, stroke_width=5.0).move_to([3.6, 0.25, 0])
        check_lbl = T("Check every Cre line with a reporter", 28, PROMOTER).move_to([0.0, -2.85, 0])
        self.play(Create(check_ring), FadeIn(check_lbl), run_time=0.7)
        self.play(check_ring.animate.scale(1.06), rate_func=there_and_back, run_time=1.0)
        self.finish()


class S10FlpWrap(SpokenScene):
    def construct(self):
        glow_a = ValueTracker(0.0)
        glow_b = ValueTracker(0.0)
        state = {"stop_a": True, "stop_b": True, "cre_a": False, "flp_b": False}

        field = always_redraw(lambda: build_tissue_field(
            scale=0.94, y_shift=0.12, show_dna=True,
            glow_fn=lambda k: (glow_a.get_value(), REPORTER) if k == "A" else (
                (glow_b.get_value(), ACTUATOR) if k == "B" else (0.0, REPORTER)
            ),
            stop_fn=lambda k: state["stop_a"] if k == "A" else (state["stop_b"] if k == "B" else True),
            cre_fn=lambda k: state["cre_a"] if k == "A" else False,
            flp_fn=lambda k: state["flp_b"] if k == "B" else False,
        ))
        legend = tissue_legend(y=3.35)

        y_dna = -2.10
        lox_l = make_site_marker([-5.3, y_dna], kind="loxp", scale=1.10)
        stop_a = make_dna_block("STOP", [-4.15, y_dna, 0], width=1.28, height=0.82,
                                color=STOP_COL, size=26, fill_opacity=0.60)
        lox_r = make_site_marker([-3.0, y_dna], kind="loxp", scale=1.10)
        rep_b = make_dna_block("Reporter", [-1.45, y_dna, 0], width=2.05, height=0.82,
                               color=REPORTER, size=26, fill_opacity=0.35)
        bb_l = connect_dna_segments([-6.0, lox_l, stop_a, lox_r, rep_b, -0.30], y_dna, color=TEXT, stroke=5.5)
        lbl_l = T("Cre  |  loxP sites", 26, CRE_COL).move_to([-3.2, y_dna - 0.86, 0])

        flp_l = make_site_marker([0.9, y_dna], kind="flp", scale=1.10)
        stop_b = make_dna_block("STOP", [2.05, y_dna, 0], width=1.28, height=0.82,
                                color=STOP_COL, size=26, fill_opacity=0.60)
        flp_r = make_site_marker([3.2, y_dna], kind="flp", scale=1.10)
        act_b = make_dna_block("Actuator", [4.8, y_dna, 0], width=2.05, height=0.82,
                               color=ACTUATOR, size=26, fill_opacity=0.35)
        bb_r = connect_dna_segments([0.2, flp_l, stop_b, flp_r, act_b, 6.0], y_dna, color=TEXT, stroke=5.5)
        lbl_r = T("Flp  |  Flp sites", 26, FLP_COL).move_to([3.1, y_dna - 0.86, 0])

        self.add(field, legend, bb_l, lox_l, stop_a, lox_r, rep_b, lbl_l,
                 bb_r, flp_l, stop_b, flp_r, act_b, lbl_r)

        self.at("second tool")
        b_centers = [np.array([x, y + 0.12, 0]) for x, y, k, _ in TISSUE_LAYOUT if k == "B"]
        b_scan = ValueTracker(0.0)
        b_ring = always_redraw(lambda: Circle(radius=0.62, color=ACTUATOR, stroke_width=5.0).move_to(
            b_centers[min(int(b_scan.get_value()), 2)] * (1.0 - (b_scan.get_value() % 1.0))
            + b_centers[min(int(b_scan.get_value()) + 1, 3)] * (b_scan.get_value() % 1.0)
            if b_scan.get_value() < 3.0 else b_centers[3]
        ))
        self.add(b_ring)
        self.play(b_scan.animate(rate_func=linear).set_value(3.0),
                  Indicate(act_b, color=ACTUATOR, rate_func=there_and_back),
                  run_time=max(1.4, self.t_of("yeast enzyme") - 0.25 - self.elapsed()))
        self.remove(b_ring)

        self.at("yeast enzyme")
        flp_clamp_1 = make_enzyme_clamp([-5.3, y_dna + 0.90], color=FLP_COL, radius=0.34)
        flp_clamp_2 = make_enzyme_clamp([2.05, y_dna + 0.90], color=FLP_COL, radius=0.34, angle=PI)
        flp_tag = T("Flp", 26, FLP_COL).move_to([4.8, y_dna + 0.90, 0])
        self.play(FadeIn(flp_clamp_1), FadeIn(flp_clamp_2), FadeIn(flp_tag), run_time=0.7)

        self.at("cuts only its own")
        # Stay safely above y_dna + 0.80 (-1.30) while passing over left track -> zero STOP/Reporter straddle
        self.play(flp_clamp_1.animate.move_to([-5.3, y_dna + 0.80, 0]), run_time=0.35)
        self.play(flp_clamp_1.animate.move_to([-1.5, y_dna + 0.92, 0]), FadeOut(flp_tag), run_time=0.6)
        self.play(flp_clamp_1.animate.move_to([0.9, y_dna + 0.08, 0]),
                  flp_clamp_2.animate.move_to([3.2, y_dna + 0.08, 0]),
                  run_time=max(0.8, self.t_of("Drive") - 0.25 - self.elapsed()))

        self.at("Drive")
        cre_clamp_1 = make_enzyme_clamp([-5.3, y_dna + 0.08], color=CRE_COL, radius=0.34)
        cre_clamp_2 = make_enzyme_clamp([-3.0, y_dna + 0.08], color=CRE_COL, radius=0.34, angle=PI)
        state["cre_a"] = True
        state["flp_b"] = True
        self.play(FadeIn(cre_clamp_1), FadeIn(cre_clamp_2),
                  run_time=max(0.9, self.t_of("unlocks its own tool") - 0.25 - self.elapsed()))

        self.at("unlocks its own tool")
        state["stop_a"] = False
        state["stop_b"] = False
        single_lox = make_site_marker([-4.15, y_dna], kind="loxp", scale=1.10)
        single_flp = make_site_marker([2.05, y_dna], kind="flp", scale=1.10)
        clean_bb_l = connect_dna_segments([-6.0, single_lox, rep_b, -0.30], y_dna, color=TEXT, stroke=5.5)
        clean_bb_r = connect_dna_segments([0.2, single_flp, act_b, 6.0], y_dna, color=TEXT, stroke=5.5)
        lit_rep = make_dna_block("Reporter", [-1.45, y_dna, 0], width=2.05, height=0.82,
                                 color=REPORTER, size=26, fill_opacity=0.72)
        lit_act = make_dna_block("Actuator", [4.8, y_dna, 0], width=2.05, height=0.82,
                                 color=ACTUATOR, size=26, fill_opacity=0.72)
        self.play(
            FadeOut(stop_a, run_time=0.5), FadeOut(stop_b, run_time=0.5),
            FadeOut(bb_l, run_time=0.4), FadeOut(bb_r, run_time=0.4),
            FadeIn(clean_bb_l), FadeIn(clean_bb_r),
            FadeOut(cre_clamp_1, run_time=0.5), FadeOut(cre_clamp_2, run_time=0.5),
            FadeOut(flp_clamp_1, run_time=0.5), FadeOut(flp_clamp_2, run_time=0.5),
            ReplacementTransform(lox_l, single_lox),
            FadeOut(lox_r, run_time=0.4),
            ReplacementTransform(flp_l, single_flp),
            FadeOut(flp_r, run_time=0.4),
            ReplacementTransform(rep_b, lit_rep),
            ReplacementTransform(act_b, lit_act),
            glow_a.animate.set_value(1.0),
            glow_b.animate.set_value(1.0),
            run_time=1.35,
        )

        self.at("Promoters and recombinases")
        phase = ValueTracker(0.0)
        rna_l = always_redraw(lambda: rna_ribbon(
            -2.45, -0.45, y_dna + 0.82, phase.get_value(), amp=0.18, freq=5.5, color=REPORTER
        ))
        rna_r = always_redraw(lambda: rna_ribbon(
            3.75, 5.80, y_dna + 0.82, phase.get_value(), amp=0.18, freq=5.5, color=ACTUATOR
        ))
        self.add(rna_l, rna_r)
        self.play(phase.animate.set_value(18.0),
                  run_time=max(1.0, self.narration_s - self.elapsed() - 0.1), rate_func=linear)
        self.finish()


class S11End(EndCard):
    LINE = "Promoters and recombinases place each tool in chosen cells."
