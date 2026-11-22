"""Proof Beyond the Pellet: Controls and Counts — scenes.py

COLOUR MAP (one colour per concept, carried across every scene):
- VESICLE_GOLD  (#F5C542): Extracellular vesicle lipid bilayer membrane
- CARGO_CYAN    (#38BDF8): Internal cytosol & sealed RNA / microRNA cargo
- LIGAND_CORAL  (#FB7185): Outward-facing surface proteins / ligands
- PROTEIN_AMBER (#D97706): Free protein clumps, aggregates, & RNA-binding protein shield
- LIPO_SLATE    (#94A3B8): Lipoproteins & pale calf-serum vesicles (contaminants)
- CELL_EMERALD  (#34D399): Target-cell response / passing control / verified signal
- CUT_RED       (#FC6255): Enzymatic cleavage (protease / RNase) & negative/broken state
- DETERGENT_TEAL(#3FB8C0): Detergent disrupting lipid membrane
- TEXT / GOLD   (#E8EAF0 / #D4A843): Equations, prompts, and highlights

ONE WORLD CARRIED FROM SCENE TO SCENE:
A clear laboratory centrifuge tube of donor medium carrying vesicles (gold ring, cyan cytosol,
coral surface ligands) and co-sedimenting contaminants (amber protein clumps, slate lipoproteins,
tangled RNA-protein specks, pale serum vesicles), paired with a recipient target cell and
quantitative readouts that zoom from the 100,000 x g pellet into a sucrose gradient,
protease/RNase protection panels, single-vesicle sphere volume, and a 50-vesicle copy grid.

WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT COMPUTATION DRIVES IT):
- s01_hook: Hero vesicle exhibits outward ligands & sealed cytosol; Stokes-like settling + fixed-seed
  Brownian motion brings particles down into a curved-bottom pellet while a droplet activates the emerald target cell.
- s02_pellet: ValueTracker centrifugal g-force (300 -> 2,000 -> 100,000 x g) drives computed
  sedimentation velocities into the bottom pellet, then zooms in to highlight all 5 co-pelleted classes.
- s03_gradient: Bottom-loaded sucrose density gradient (1.04 to 1.30 g/mL) integrates buoyancy
  dz/dt = k * (rho_grad(z) - rho_p) per particle with a live density histogram until vesicles equilibrate at 1.13-1.19 g/mL.
- s04_gradient_controls: Aliquot streams transfer from vesicle band, dense band, and cell-free mock
  onto 3 target-cell dishes with rising emerald activity bar only on the vesicle layer while lipoproteins overlap.
- s05_protection: TwoPanel comparison runs animated scissors (protease/RNase) alone vs with detergent
  droplets; intact membrane blocks internal cleavage, detergent breaks ring arcs, protein cap shields RNA.
- s06_volume: Live ValueTracker computes V = (4/3)*pi*r^3 for d = 0 -> 100 nm (5.2e-19 L), multiplied by 1 uM
  and N_A (~0.3 molecules/vesicle), shown across 3 ligand-studded vesicles with 1 internal cyan dot.
- s07_predict_q: ValueTracker counters ramp to 2,000,000,000 vesicles and 40,000,000 copies under
  copies / particles, presenting the 3 predict options before the pause.
- s09_reveal: Completes 40,000,000 / 2,000,000,000 = 0.02 (1 in 50), populates a 5x10 grid of
  50 vesicles (49 empty, 1 with 1 cyan dot), then grows a zoomed vesicle studded with many coral ligands.
- s10_closing: Concentrates cyan dots into 1 rare subset vesicle in the 50-vesicle grid, then pulls
  back to the 3 animated verification icons (Separate vesicles, Locate cargo, Count copies) with checks.
"""

from bp_parts import *

# ------------------------------------------------------------------ Concept palette
VESICLE_GOLD = "#F5C542"
CARGO_CYAN = "#38BDF8"
LIGAND_CORAL = "#FB7185"
PROTEIN_AMBER = "#D97706"
LIPO_SLATE = "#94A3B8"
SERUM_PALE = "#CBD5E1"
CELL_EMERALD = "#34D399"
CUT_RED = "#FC6255"
DETERGENT_TEAL = TEAL
PANEL_BG = "#161B26"


# ------------------------------------------------------------------ Shared builders
def make_vesicle(radius=0.22, n_ligands=8, has_cargo=True, n_dots=2, seed=7,
                 ligand_len=0.09, stroke_w=4.0):
    """Gold bilayer ring, optional cyan cytosol + internal RNA dots, coral outward ligands."""
    ring = Circle(
        radius=radius,
        stroke_color=VESICLE_GOLD,
        stroke_width=stroke_w,
        fill_color=CARGO_CYAN if has_cargo else BG,
        fill_opacity=0.28 if has_cargo else 0.9,
    )
    g = VGroup(ring)
    if has_cargo and n_dots > 0:
        rng = np.random.default_rng(seed)
        dots = VGroup()
        for _ in range(n_dots):
            ang = rng.uniform(0, TAU)
            rr = rng.uniform(0.0, radius * 0.45)
            d = Dot(
                point=np.array([rr * np.cos(ang), rr * np.sin(ang), 0.0]),
                radius=max(0.028, radius * 0.14),
                color=CARGO_CYAN,
            )
            dots.add(d)
        g.add(dots)
    if n_ligands > 0:
        ligs = VGroup()
        for k in range(n_ligands):
            ang = k * TAU / n_ligands
            u = np.array([np.cos(ang), np.sin(ang), 0.0])
            stem = Line(u * radius, u * (radius + ligand_len),
                        color=LIGAND_CORAL, stroke_width=max(2.0, stroke_w * 0.65))
            head = Dot(u * (radius + ligand_len),
                       radius=max(0.025, radius * 0.14), color=LIGAND_CORAL)
            ligs.add(VGroup(stem, head))
        g.add(ligs)
        g.ligands = ligs
    else:
        g.ligands = VGroup()
    g.ring = ring
    return g


def make_protein_clump(scale=1.0, seed=11):
    """Irregular amber protein aggregate."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(5):
        off = np.array([rng.uniform(-0.08, 0.08), rng.uniform(-0.07, 0.07), 0.0]) * scale
        r = rng.uniform(0.055, 0.095) * scale
        blob = Circle(radius=r, stroke_color=PROTEIN_AMBER, stroke_width=2.0,
                      fill_color=PROTEIN_AMBER, fill_opacity=0.78).move_to(off)
        g.add(blob)
    return g


def make_lipoprotein(radius=0.13):
    """Round slate-grey lipoprotein sphere."""
    return Circle(radius=radius, stroke_color=LIPO_SLATE, stroke_width=2.5,
                  fill_color=LIPO_SLATE, fill_opacity=0.50)


def make_rna_protein_speck(scale=1.0):
    """Tangled RNA strand bound with amber protein dots."""
    pts = [np.array([-0.14, -0.04, 0]), np.array([-0.05, 0.07, 0]),
           np.array([0.04, -0.06, 0]), np.array([0.14, 0.05, 0])]
    strand = VMobject(stroke_color=CARGO_CYAN, stroke_width=3.2)
    strand.set_points_smoothly([p * scale for p in pts])
    c1 = Dot(pts[1] * scale, radius=0.045 * scale, color=PROTEIN_AMBER)
    c2 = Dot(pts[2] * scale, radius=0.045 * scale, color=PROTEIN_AMBER)
    return VGroup(strand, c1, c2)


def make_serum_vesicle(radius=0.16):
    """Pale calf-serum vesicle (distinct from donor gold vesicles)."""
    return Circle(radius=radius, stroke_color=SERUM_PALE, stroke_width=2.8,
                  fill_color=SERUM_PALE, fill_opacity=0.20)


def make_tube(center=(-3.8, 0.0, 0), width=2.7, height=5.1, fluid_frac=0.84):
    """Clear laboratory centrifuge tube with fluid fill and rounded bottom."""
    cx, cy, _ = center
    r = width / 2.0
    top_y = cy + height / 2.0
    bot_y = cy - height / 2.0
    arc_cy = bot_y + r

    left_wall = Line([cx - r, top_y, 0], [cx - r, arc_cy, 0], color=TEXT, stroke_width=3.5)
    bot_arc = Arc(radius=r, start_angle=PI, angle=PI, arc_center=[cx, arc_cy, 0],
                  color=TEXT, stroke_width=3.5)
    right_wall = Line([cx + r, arc_cy, 0], [cx + r, top_y, 0], color=TEXT, stroke_width=3.5)
    rim = Line([cx - r - 0.1, top_y, 0], [cx + r + 0.1, top_y, 0], color=TEXT, stroke_width=4.0)

    f_top = bot_y + height * fluid_frac
    fluid_rect = Rectangle(
        width=width - 0.08, height=max(0.2, f_top - arc_cy),
        stroke_width=0, fill_color=CARGO_CYAN, fill_opacity=0.14,
    ).move_to([cx, (f_top + arc_cy) / 2.0, 0])
    fluid_bot = Sector(
        radius=r - 0.04, start_angle=PI, angle=PI, arc_center=[cx, arc_cy, 0],
        stroke_width=0, fill_color=CARGO_CYAN, fill_opacity=0.14,
    )
    meniscus = Line([cx - r + 0.05, f_top, 0], [cx + r - 0.05, f_top, 0],
                    color=CARGO_CYAN, stroke_width=2.5, stroke_opacity=0.7)

    tube = VGroup(fluid_bot, fluid_rect, meniscus, left_wall, bot_arc, right_wall, rim)
    tube.cx = cx
    tube.r = r
    tube.arc_cy = arc_cy
    tube.inner_bounds = (cx - r + 0.28, cx + r - 0.28, bot_y + 0.28, f_top - 0.20)
    tube.bottom_pt = np.array([cx, bot_y + 0.28, 0.0])
    tube.top_pt = np.array([cx, top_y, 0.0])
    return tube


def tube_floor_y(tube, x, pad=0.30):
    """Exact rounded-bottom floor height inside a centrifuge tube at horizontal coordinate x."""
    dx = np.clip(x - tube.cx, -(tube.r - pad), tube.r - pad)
    rad = max(0.1, tube.r - pad)
    return tube.arc_cy - np.sqrt(max(0.0, rad * rad - dx * dx))


def make_target_cell(center=(4.1, -0.2, 0), radius=1.25, active=False):
    """Recipient cell with surface membrane, nucleus, and optional emerald activation."""
    c = np.array(center, dtype=float)
    col = CELL_EMERALD if active else TEXT
    outer = Circle(radius=radius, stroke_color=col, stroke_width=4.5,
                   fill_color=CELL_EMERALD if active else CARGO_CYAN,
                   fill_opacity=0.28 if active else 0.12).move_to(c)
    nucleus = Circle(radius=radius * 0.36, stroke_color=col, stroke_width=2.5,
                     fill_color=col, fill_opacity=0.22).move_to(c + DOWN * 0.08)
    recs = VGroup()
    for ang in np.linspace(PI * 0.72, PI * 1.28, 4):
        u = np.array([np.cos(ang), np.sin(ang), 0.0])
        recs.add(Line(c + u * radius, c + u * (radius + 0.16), color=col, stroke_width=3.5))
    g = VGroup(outer, nucleus, recs)
    g.outer, g.nucleus, g.recs = outer, nucleus, recs
    return g


def make_scissors(center=(0, 0, 0), scale=0.45, color=CUT_RED, open_angle=0.35):
    """Schematic enzyme scissors (crossed blades + handle rings)."""
    c = np.array(center, dtype=float)
    b1 = Line(LEFT * 0.45 * scale, RIGHT * 0.75 * scale, color=color, stroke_width=4.0)
    b2 = Line(LEFT * 0.45 * scale, RIGHT * 0.75 * scale, color=color, stroke_width=4.0)
    b1.rotate(open_angle, about_point=ORIGIN)
    b2.rotate(-open_angle, about_point=ORIGIN)
    h1 = Circle(radius=0.16 * scale, color=color, stroke_width=3.5).move_to(b1.get_start() + LEFT * 0.12 * scale)
    h2 = Circle(radius=0.16 * scale, color=color, stroke_width=3.5).move_to(b2.get_start() + LEFT * 0.12 * scale)
    g = VGroup(b1, b2, h1, h2).move_to(c)
    g.b1, g.b2 = b1, b2
    return g


def build_predict_backdrop():
    """Shared visual state for end of S07PredictQ and S08Pause.backdrop()."""
    top_eq = VGroup(
        T("copies per vesicle  =", 32, TEXT),
        T("cargo copies", 32, CARGO_CYAN),
        T("÷", 34, TEXT),
        T("particles counted", 32, VESICLE_GOLD),
    ).arrange(RIGHT, buff=0.22).move_to([0, 2.85, 0])

    card = RoundedRectangle(
        corner_radius=0.20, width=10.2, height=2.55,
        stroke_color=TEAL, stroke_width=2.5,
        fill_color=PANEL_BG, fill_opacity=0.92,
    ).move_to([0, 0.75, 0])

    num_txt = M("40,000,000 copies", 38, CARGO_CYAN).move_to([-0.8, 1.38, 0])
    div_bar = Line([-3.7, 0.75, 0], [2.1, 0.75, 0], color=TEXT, stroke_width=4.0)
    den_txt = M("2,000,000,000 vesicles", 38, VESICLE_GOLD).move_to([-0.8, 0.15, 0])
    eq_q = M("=  ?", 44, GOLD).move_to([3.55, 0.75, 0])
    return VGroup(top_eq, card, num_txt, div_bar, den_txt, eq_q)


def build_grid_50(origin=(-2.65, -0.70, 0), dx=0.76, dy=0.72, occupied_idx=17,
                  n_dots_in_occupied=1, r=0.24):
    """5x10 grid of 50 tiny gold vesicle rings; only `occupied_idx` holds cyan dot(s)."""
    ox, oy, _ = origin
    grid = VGroup()
    rng = np.random.default_rng(7)
    for row in range(5):
        for col in range(10):
            idx = row * 10 + col
            px = ox + (col - 4.5) * dx
            py = oy + (2.0 - row) * dy
            occ = (idx == occupied_idx)
            ring = Circle(
                radius=r,
                stroke_color=VESICLE_GOLD,
                stroke_width=3.2 if occ else 2.4,
                fill_color=CARGO_CYAN if occ else PANEL_BG,
                fill_opacity=0.32 if occ else 0.85,
            ).move_to([px, py, 0])
            cell = VGroup(ring)
            if occ:
                if n_dots_in_occupied == 1:
                    cell.add(Dot([px, py, 0], radius=0.075, color=CARGO_CYAN))
                else:
                    for _ in range(n_dots_in_occupied):
                        ang = rng.uniform(0, TAU)
                        rr = rng.uniform(0, r * 0.48)
                        cell.add(Dot([px + rr * np.cos(ang), py + rr * np.sin(ang), 0],
                                     radius=0.05, color=CARGO_CYAN))
            grid.add(cell)
    return grid


# ================================================================== SCENES
class S00Title(TitleCard):
    LESSON = "Exosomes and Extracellular Vesicles: Signals Between Cells"
    TITLE = "Proof Beyond the Pellet: Controls and Counts"


class S01Hook(SpokenScene):
    def construct(self):
        # 1. Hero vesicle illustrating outward ligands + sealed cytosol
        hero = make_vesicle(radius=1.55, n_ligands=12, has_cargo=True, n_dots=4,
                            seed=7, ligand_len=0.30, stroke_w=7.5).move_to([-2.7, 0.15, 0])
        lbl_out = T("Ligands face outward", 30, LIGAND_CORAL).move_to([2.95, 1.35, 0])
        arr_out = Arrow(lbl_out.get_left() + LEFT * 0.14, hero.get_right() + LEFT * 0.05 + UP * 0.65,
                        color=LIGAND_CORAL, stroke_width=4.0, buff=0.05)
        lbl_in = T("Cytosol sealed inside", 30, CARGO_CYAN).move_to([2.95, -0.70, 0])
        arr_in = Arrow(lbl_in.get_left() + LEFT * 0.14, hero.get_center() + RIGHT * 0.55 + DOWN * 0.28,
                       color=CARGO_CYAN, stroke_width=4.0, buff=0.05)

        stag = scope_tag("schematic")
        self.add(stag)
        self.play(FadeIn(hero, scale=0.92), run_time=0.55)

        self.at("face outward")
        self.play(FadeIn(lbl_out), GrowArrow(arr_out), run_time=0.75)

        self.at("seal cytosol")
        self.play(FadeIn(lbl_in), GrowArrow(arr_in), run_time=0.80)

        # 2. Transition hero into centrifuge tube + recipient target cell world
        tube = make_tube(center=(-4.0, 0.0, 0), width=2.7, height=5.1, fluid_frac=0.84)
        tube_lbl = T("Donor medium", 28, TEXT).next_to(tube, UP, buff=0.18)

        rng = np.random.default_rng(7)
        x0, x1, y0, y1 = tube.inner_bounds
        particles = VGroup()
        contam_group = VGroup()
        for i in range(6):
            p = make_vesicle(radius=0.19, n_ligands=6, has_cargo=True, n_dots=1,
                             seed=10 + i, ligand_len=0.06, stroke_w=3.2)
            p.move_to([rng.uniform(x0, x1), rng.uniform(y0 + 0.7, y1), 0])
            p.vy = -rng.uniform(0.11, 0.16)
            p.vx = rng.uniform(-0.04, 0.04)
            particles.add(p)
        for i in range(4):
            p = make_protein_clump(scale=0.95, seed=20 + i)
            p.move_to([rng.uniform(x0, x1), rng.uniform(y0 + 0.6, y1), 0])
            p.vy = -rng.uniform(0.12, 0.18)
            p.vx = rng.uniform(-0.04, 0.04)
            contam_group.add(p)
            particles.add(p)
        for i in range(4):
            p = make_lipoprotein(radius=0.13)
            p.move_to([rng.uniform(x0, x1), rng.uniform(y0 + 0.6, y1), 0])
            p.vy = -rng.uniform(0.09, 0.14)
            p.vx = rng.uniform(-0.04, 0.04)
            contam_group.add(p)
            particles.add(p)
        for i in range(3):
            p = make_rna_protein_speck(scale=0.95)
            p.move_to([rng.uniform(x0, x1), rng.uniform(y0 + 0.6, y1), 0])
            p.vy = -rng.uniform(0.10, 0.15)
            p.vx = rng.uniform(-0.04, 0.04)
            contam_group.add(p)
            particles.add(p)

        cell = make_target_cell(center=(4.2, -0.2, 0), radius=1.22, active=False)
        cell_lbl = T("Target cell", 28, TEXT).next_to(cell, UP, buff=0.22)

        self.play(
            FadeOut(hero), FadeOut(lbl_out), FadeOut(arr_out),
            FadeOut(lbl_in), FadeOut(arr_in),
            run_time=0.4,
        )
        self.play(
            FadeIn(tube), FadeIn(tube_lbl), FadeIn(particles),
            FadeIn(cell), FadeIn(cell_lbl),
            run_time=0.7,
        )

        settling_on = ValueTracker(1.2)

        def settle_step(mob, dt):
            s = settling_on.get_value()
            if s <= 0:
                return
            for p in mob:
                nx = p.get_center()[0] + p.vx * dt * s
                if nx < x0 or nx > x1:
                    p.vx *= -1
                    nx = np.clip(nx, x0, x1)
                floor_y = tube_floor_y(tube, nx, pad=0.32)
                ny = p.get_center()[1] + p.vy * dt * s
                if ny <= floor_y:
                    ny = floor_y
                    p.vy = 0.0
                    p.vx = 0.0
                p.move_to([nx, ny, 0])

        particles.add_updater(settle_step)

        self.at("centrifuge pellet")
        settling_on.set_value(3.8)
        pellet_arc = Sector(radius=tube.r - 0.05, start_angle=PI, angle=PI,
                            arc_center=[tube.cx, tube.arc_cy, 0],
                            stroke_color=VESICLE_GOLD, stroke_width=2.0,
                            fill_color=PROTEIN_AMBER, fill_opacity=0.38)
        pellet_lbl = T("Pellet", 28, VESICLE_GOLD).next_to(tube, DOWN, buff=0.18)
        self.play(FadeIn(pellet_arc), FadeIn(pellet_lbl), run_time=0.8)

        droplet = Dot(tube.bottom_pt + UP * 0.25, radius=0.15, color=VESICLE_GOLD)
        arc_path = ArcBetweenPoints(tube.bottom_pt + RIGHT * 0.7 + UP * 0.25,
                                    cell.outer.get_left() + LEFT * 0.22, angle=-0.45)
        self.play(MoveAlongPath(droplet, arc_path), run_time=0.95)
        self.play(
            FadeOut(droplet),
            cell.outer.animate.set_stroke(CELL_EMERALD).set_fill(CELL_EMERALD, opacity=0.34),
            cell.nucleus.animate.set_stroke(CELL_EMERALD).set_fill(CELL_EMERALD, opacity=0.28),
            cell.recs.animate.set_color(CELL_EMERALD),
            cell_lbl.animate.set_color(CELL_EMERALD),
            run_time=0.55,
        )

        self.at("how can you tell")
        q_mark = T("?", 88, TEXT, weight=BOLD).move_to([0.15, 0.25, 0])
        q_sub = T("Vesicle or contaminant?", 28, GOLD).next_to(q_mark, DOWN, buff=0.25)
        self.play(FadeIn(q_mark, scale=0.85), FadeIn(q_sub), run_time=0.75)

        self.at("far more than vesicles")
        particles.clear_updaters()
        mixed_tag = T("Mixed pellet", 28, PROTEIN_AMBER).move_to([0.15, 1.85, 0])
        self.play(
            FadeIn(mixed_tag),
            Indicate(contam_group, color=PROTEIN_AMBER, scale_factor=1.15),
            run_time=1.0,
        )
        self.finish()


class S02Pellet(SpokenScene):
    def construct(self):
        tube = make_tube(center=(-3.7, 0.0, 0), width=2.8, height=5.2, fluid_frac=0.84)
        x0, x1, y0, y1 = tube.inner_bounds

        rng = np.random.default_rng(17)
        all_p = VGroup()
        cells_debris = []

        for _ in range(4):
            d = Circle(radius=0.22, stroke_color=LIPO_SLATE, stroke_width=2.5,
                       fill_color=LIPO_SLATE, fill_opacity=0.45)
            d.move_to([rng.uniform(x0, x1), rng.uniform(0.1, y1), 0])
            d.speed_factor = 3.0
            cells_debris.append(d)
            all_p.add(d)
        for i in range(5):
            v = make_vesicle(radius=0.17, n_ligands=6, has_cargo=True, n_dots=1, seed=30 + i,
                             ligand_len=0.05, stroke_w=3.0)
            v.move_to([rng.uniform(x0, x1), rng.uniform(-0.3, y1), 0])
            v.speed_factor = 0.85
            all_p.add(v)
        for i in range(4):
            pr = make_protein_clump(scale=0.85, seed=40 + i)
            pr.move_to([rng.uniform(x0, x1), rng.uniform(-0.3, y1), 0])
            pr.speed_factor = 0.92
            all_p.add(pr)
        for _ in range(4):
            lp = make_lipoprotein(radius=0.12)
            lp.move_to([rng.uniform(x0, x1), rng.uniform(-0.3, y1), 0])
            lp.speed_factor = 0.80
            all_p.add(lp)
        for _ in range(3):
            rn = make_rna_protein_speck(scale=0.85)
            rn.move_to([rng.uniform(x0, x1), rng.uniform(-0.3, y1), 0])
            rn.speed_factor = 0.84
            all_p.add(rn)
        for _ in range(3):
            sv = make_serum_vesicle(radius=0.14)
            sv.move_to([rng.uniform(x0, x1), rng.uniform(-0.3, y1), 0])
            sv.speed_factor = 0.86
            all_p.add(sv)

        g_tracker = ValueTracker(300.0)
        g_readout = counter("Spin speed: {:,.0f} × g", g_tracker, at=[2.45, 2.55, 0], size=32, color=TEXT)

        b1 = boxed_label("Low: cells", TEXT, size=26, box=(4.8, 0.65)).move_to([2.45, 1.5, 0])
        b2 = boxed_label("Medium: debris", TEXT, size=26, box=(4.8, 0.65)).move_to([2.45, 0.55, 0])
        b3 = boxed_label("100,000 × g: small particles", VESICLE_GOLD, size=26, box=(4.8, 0.65)).move_to([2.45, -0.4, 0])

        stag = scope_tag("schematic")
        self.add(tube, all_p, g_readout, stag)

        def sed_updater(mob, dt):
            g_val = g_tracker.get_value()
            rate = np.log10(max(g_val, 10.0)) * 0.22
            for p in mob:
                if p in cells_debris:
                    vy = rate * p.speed_factor
                else:
                    vy = (0.04 if g_val < 5000 else rate * 0.80) * p.speed_factor
                px = p.get_center()[0]
                floor_y = tube_floor_y(tube, px, pad=0.30)
                ny = max(floor_y, p.get_center()[1] - vy * dt)
                p.move_to([px, ny, 0])

        all_p.add_updater(sed_updater)

        self.play(FadeIn(b1), run_time=0.6)
        self.play(g_tracker.animate.set_value(2000.0), FadeIn(b2), run_time=2.3)

        self.at("finishing")
        self.play(g_tracker.animate.set_value(100000.0), FadeIn(b3), run_time=2.2)

        self.at("size and density")
        sort_note = T("Sorts by size & density, not identity", 28, GOLD).move_to([2.45, -1.6, 0])
        pellet_pack = Sector(radius=tube.r - 0.06, start_angle=PI, angle=PI,
                             arc_center=[tube.cx, tube.arc_cy, 0],
                             stroke_color=VESICLE_GOLD, stroke_width=2.0,
                             fill_color=PROTEIN_AMBER, fill_opacity=0.32)
        self.play(FadeIn(sort_note), FadeIn(pellet_pack), run_time=1.0)
        # Keep particles compacting gently until zoom
        self.wait(1.2)
        all_p.clear_updaters()

        self.at("So the pellet")
        zoom_circle = Circle(radius=2.75, stroke_color=VESICLE_GOLD, stroke_width=4.5,
                             fill_color=PANEL_BG, fill_opacity=0.96).move_to([-2.4, -0.15, 0])
        zoom_title = T("Mixed 100,000 × g pellet", 32, VESICLE_GOLD).move_to([-2.4, 2.98, 0])

        z_ves = make_vesicle(radius=0.40, n_ligands=8, has_cargo=True, n_dots=2, seed=7,
                             ligand_len=0.11, stroke_w=5.0).move_to([-3.5, 0.72, 0])
        z_ves2 = make_vesicle(radius=0.32, n_ligands=7, has_cargo=True, n_dots=1, seed=9,
                              ligand_len=0.09, stroke_w=4.5).move_to([-3.5, -0.55, 0])
        z_prot = make_protein_clump(scale=2.0, seed=21).move_to([-1.25, 1.15, 0])
        z_lipo = make_lipoprotein(radius=0.30).move_to([-1.05, 0.15, 0])
        z_rna = make_rna_protein_speck(scale=2.0).move_to([-1.25, -0.75, 0])
        z_serum = make_serum_vesicle(radius=0.34).move_to([-1.55, -1.65, 0])
        z_ves_tag = T("Vesicles", 26, VESICLE_GOLD).next_to(z_ves, UP, buff=0.15)

        zoom_contents = VGroup(z_ves, z_ves2, z_prot, z_lipo, z_rna, z_serum, z_ves_tag)

        self.play(
            FadeOut(tube), FadeOut(all_p), FadeOut(pellet_pack), FadeOut(g_readout),
            FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(sort_note),
            run_time=0.4,
        )
        self.play(FadeIn(zoom_circle), FadeIn(zoom_title), FadeIn(zoom_contents), run_time=0.7)

        l_prot = T("Protein clumps", 30, PROTEIN_AMBER).move_to([3.55, 1.35, 0])
        a_prot = Arrow(l_prot.get_left() + LEFT * 0.14, z_prot.get_right() + RIGHT * 0.12,
                       color=PROTEIN_AMBER, stroke_width=3.5, buff=0.05)

        l_lipo = T("Lipoproteins", 30, LIPO_SLATE).move_to([3.55, 0.35, 0])
        a_lipo = Arrow(l_lipo.get_left() + LEFT * 0.14, z_lipo.get_right() + RIGHT * 0.12,
                       color=LIPO_SLATE, stroke_width=3.5, buff=0.05)

        l_rna = T("RNA–protein complexes", 30, CARGO_CYAN).move_to([3.55, -0.65, 0])
        a_rna = Arrow(l_rna.get_left() + LEFT * 0.14, z_rna.get_right() + RIGHT * 0.12,
                      color=CARGO_CYAN, stroke_width=3.5, buff=0.05)

        l_serum = T("Calf serum vesicles", 30, SERUM_PALE).move_to([3.55, -1.65, 0])
        a_serum = Arrow(l_serum.get_left() + LEFT * 0.14, z_serum.get_right() + RIGHT * 0.12,
                        color=SERUM_PALE, stroke_width=3.5, buff=0.05)

        self.at("protein clumps")
        self.play(FadeIn(l_prot), GrowArrow(a_prot), Indicate(z_prot, color=PROTEIN_AMBER), run_time=0.8)

        self.at("lipoproteins")
        self.play(FadeIn(l_lipo), GrowArrow(a_lipo), Indicate(z_lipo, color=LIPO_SLATE), run_time=0.8)

        self.at("protein complexes")
        self.play(FadeIn(l_rna), GrowArrow(a_rna), Indicate(z_rna, color=CARGO_CYAN), run_time=0.8)

        self.at("calf serum vesicles")
        self.play(FadeIn(l_serum), GrowArrow(a_serum), Indicate(z_serum, color=SERUM_PALE), run_time=0.8)
        self.finish()


class S03Gradient(SpokenScene):
    def construct(self):
        cx, top_y, bot_y, w = -3.3, 2.5, -2.5, 2.9
        r = w / 2.0
        n_bands = 14
        band_h = (top_y - bot_y) / n_bands
        bands = VGroup()
        for i in range(n_bands):
            frac = i / (n_bands - 1)
            y_c = top_y - (i + 0.5) * band_h
            b = Rectangle(width=w - 0.06, height=band_h + 0.01, stroke_width=0,
                          fill_color=LIPO_SLATE, fill_opacity=0.08 + 0.36 * frac).move_to([cx, y_c, 0])
            bands.add(b)

        left_wall = Line([cx - r, top_y, 0], [cx - r, bot_y, 0], color=TEXT, stroke_width=3.5)
        right_wall = Line([cx + r, top_y, 0], [cx + r, bot_y, 0], color=TEXT, stroke_width=3.5)
        bot_wall = Line([cx - r, bot_y, 0], [cx + r, bot_y, 0], color=TEXT, stroke_width=3.5)
        rim = Line([cx - r - 0.1, top_y, 0], [cx + r + 0.1, top_y, 0], color=TEXT, stroke_width=4.0)
        tube_title = T("Bottom-loaded sucrose gradient", 28, TEXT).move_to([cx, 3.05, 0])

        def y_to_rho(y):
            f = (top_y - y) / (top_y - bot_y)
            return 1.04 + f * (1.30 - 1.04)

        def rho_to_y(rho):
            f = (rho - 1.04) / (1.30 - 1.04)
            return top_y - f * (top_y - bot_y)

        ruler = Line([cx + r + 0.32, bot_y, 0], [cx + r + 0.32, top_y, 0], color=TEXT, stroke_width=2.5)
        ticks = VGroup()
        for rho, txt in [(1.05, "1.05"), (1.16, "1.16"), (1.28, "1.28 g/mL")]:
            ty = rho_to_y(rho)
            tk = Line([cx + r + 0.25, ty, 0], [cx + r + 0.41, ty, 0], color=TEXT, stroke_width=2.5)
            lb = M(txt, 24, TEXT).next_to(tk, RIGHT, buff=0.12)
            ticks.add(tk, lb)

        rotor_center = np.array([3.65, 2.35, 0.0])
        rotor_arc = Arc(radius=0.42, start_angle=0, angle=1.4 * PI, arc_center=rotor_center,
                        color=TEAL, stroke_width=4.5)
        rotor_tip = Triangle(color=TEAL, fill_color=TEAL, fill_opacity=1.0).scale(0.11).move_to(
            rotor_arc.get_end()).rotate(0.4)
        rotor = VGroup(rotor_arc, rotor_tip)
        rotor_lbl = T("Equilibrium spin", 26, TEAL).next_to(rotor, DOWN, buff=0.15)

        rng = np.random.default_rng(33)
        vesicles, proteins = VGroup(), VGroup()
        for i in range(6):
            v = make_vesicle(radius=0.19, n_ligands=6, has_cargo=True, n_dots=1, seed=50 + i,
                             ligand_len=0.05, stroke_w=3.2)
            v.move_to([cx + rng.uniform(-0.95, 0.95), rng.uniform(bot_y + 0.26, bot_y + 0.56), 0])
            v.target_rho = rng.uniform(1.14, 1.18)
            vesicles.add(v)
        for i in range(6):
            pr = make_protein_clump(scale=1.0, seed=60 + i)
            pr.move_to([cx + rng.uniform(-0.95, 0.95), rng.uniform(bot_y + 0.22, bot_y + 0.50), 0])
            pr.target_rho = rng.uniform(1.27, 1.31)
            proteins.add(pr)

        # Live computed Gaussian density-distribution Plot (updates from actual particle y-positions!)
        dens_plot = Plot(
            box=(1.85, 5.95, -2.15, 1.05),
            xr=(1.04, 1.30),
            yr=(0.0, 1.0),
            xticks=[(1.05, "1.05"), (1.16, "1.16"), (1.28, "1.28")],
            yticks=[],
            xlabel="density (g/mL)",
            ylabel="count (computed)",
            color=TEXT, size=22, label_size=24, stroke=2.5,
        )

        def density_curve_mob(mob_group, col):
            xs = np.linspace(1.04, 1.30, 80)
            rhos = [y_to_rho(p.get_center()[1]) for p in mob_group]
            ys = np.zeros_like(xs)
            for rp in rhos:
                ys += np.exp(-0.5 * ((xs - rp) / 0.022) ** 2)
            ys = np.clip(ys / max(1.0, len(rhos) * 1.05), 0.0, 0.96)
            pts = [dens_plot.pt(x, y) for x, y in zip(xs, ys)]
            base_l, base_r = dens_plot.pt(1.04, 0.0), dens_plot.pt(1.30, 0.0)
            poly = Polygon(base_l, *pts, base_r, stroke_color=col, stroke_width=3.5,
                           fill_color=col, fill_opacity=0.28)
            return poly

        ves_curve = always_redraw(lambda: density_curve_mob(vesicles, VESICLE_GOLD))
        prot_curve = always_redraw(lambda: density_curve_mob(proteins, PROTEIN_AMBER))

        stag = scope_tag("schematic")
        self.add(bands, left_wall, right_wall, bot_wall, rim, tube_title, ruler, ticks, stag)
        self.play(FadeIn(vesicles), FadeIn(proteins), Create(dens_plot), run_time=0.8)
        self.add(ves_curve, prot_curve)

        step_tag = T("Step 1: Separate by density", 26, GOLD).move_to([2.6, 2.90, 0])
        self.play(FadeIn(step_tag), run_time=0.55)

        spin_active = ValueTracker(0.0)

        def float_updater(mob, dt):
            s = spin_active.get_value()
            if s <= 0.01:
                return
            for p in mob:
                y = p.get_center()[1]
                rho_m = y_to_rho(y)
                vy = 4.2 * s * (rho_m - p.target_rho)
                ny = np.clip(y + vy * dt, bot_y + 0.22, top_y - 0.25)
                p.move_to([p.get_center()[0], ny, 0])

        def spin_rotor(mob, dt):
            s = spin_active.get_value()
            if s > 0.01:
                mob.rotate(-3.0 * s * dt, about_point=rotor_center)

        rotor_center = np.array([5.45, 2.85, 0.0])
        rotor.move_to(rotor_center)
        rotor_lbl.next_to(rotor, DOWN, buff=0.14)

        self.at("Researchers load")
        self.play(FadeIn(rotor), FadeIn(rotor_lbl), run_time=0.55)

        vesicles.add_updater(float_updater)
        proteins.add_updater(float_updater)
        rotor.add_updater(spin_rotor)
        spin_active.set_value(1.0)

        self.at("Why do vesicles")
        q_float = T("Why float upward?", 26, VESICLE_GOLD).move_to([1.95, 2.15, 0])
        self.play(FadeIn(q_float), run_time=0.6)

        self.at("Membrane lipid")
        lipid_note = T("Lipid < protein density", 26, CARGO_CYAN).move_to([1.95, 2.15, 0])
        self.play(swap(q_float, lipid_note, run_time=0.6), run_time=0.65)

        self.at("vesicles rise")
        y_top_band = rho_to_y(1.13)
        y_bot_band = rho_to_y(1.19)
        band_box = Rectangle(
            width=w - 0.08, height=(y_top_band - y_bot_band),
            stroke_color=VESICLE_GOLD, stroke_width=2.8,
            fill_color=VESICLE_GOLD, fill_opacity=0.16,
        ).move_to([cx, (y_top_band + y_bot_band) / 2.0, 0])
        band_box.layout_ok = True

        self.play(FadeOut(step_tag), FadeOut(lipid_note), run_time=0.35)

        band_lbl = T("1.13–1.19 g/mL: vesicles", 26, VESICLE_GOLD).move_to([1.95, 1.85, 0])
        band_arr = Arrow(band_lbl.get_left() + LEFT * 0.12, [cx + r + 0.06, y_top_band - 0.06, 0],
                         color=VESICLE_GOLD, stroke_width=3.5, buff=0.05)

        self.play(FadeIn(band_box), FadeIn(band_lbl), GrowArrow(band_arr), run_time=0.8)

        self.at("free proteins")
        spin_active.set_value(0.0)
        vesicles.clear_updaters()
        proteins.clear_updaters()
        rotor.clear_updaters()

        prot_lbl = T("Denser: free protein", 26, PROTEIN_AMBER).move_to([4.75, 2.55, 0])
        prot_arr = Arrow(prot_lbl.get_bottom() + DOWN * 0.10, dens_plot.pt(1.28, 0.82) + UP * 0.10,
                         color=PROTEIN_AMBER, stroke_width=3.5, buff=0.05)
        self.play(FadeOut(rotor), FadeOut(rotor_lbl), run_time=0.25)
        self.play(FadeIn(prot_lbl), GrowArrow(prot_arr), run_time=0.55)
        self.finish()


class S04GradientControls(SpokenScene):
    def construct(self):
        def mini_grad_tube(x, title_str, has_vesicles=True):
            top_y, bot_y, w = 2.2, -2.0, 1.85
            r = w / 2.0
            bands = VGroup()
            for i in range(10):
                frac = i / 9.0
                bh = (top_y - bot_y) / 10.0
                bands.add(Rectangle(width=w - 0.06, height=bh + 0.01, stroke_width=0,
                                    fill_color=LIPO_SLATE, fill_opacity=0.08 + 0.34 * frac).move_to(
                    [x, top_y - (i + 0.5) * bh, 0]))
            walls = VGroup(
                Line([x - r, top_y, 0], [x - r, bot_y, 0], color=TEXT, stroke_width=3.0),
                Line([x - r, bot_y, 0], [x + r, bot_y, 0], color=TEXT, stroke_width=3.0),
                Line([x + r, bot_y, 0], [x + r, top_y, 0], color=TEXT, stroke_width=3.0),
            )
            ttl = fit_text(title_str, max_w=2.4, size=26, color=TEXT).move_to([x, 2.72, 0])
            g = VGroup(bands, walls, ttl)
            if has_vesicles:
                band_y = 0.25
                band_hi = Rectangle(width=w - 0.08, height=0.78, stroke_color=VESICLE_GOLD, stroke_width=2.2,
                                    fill_color=VESICLE_GOLD, fill_opacity=0.16).move_to([x, band_y, 0])
                band_hi.layout_ok = True
                ves = VGroup(*[
                    make_vesicle(radius=0.14, n_ligands=5, has_cargo=True, n_dots=1, seed=70 + k,
                                 ligand_len=0.04, stroke_w=2.5).move_to(
                        [x + dx, band_y + dy, 0])
                    for k, (dx, dy) in enumerate([(-0.45, 0.14), (0.05, -0.10), (0.45, 0.12), (-0.15, 0.22)])
                ])
                prots = VGroup(*[
                    make_protein_clump(scale=0.72, seed=80 + k).move_to([x + dx, bot_y + dy, 0])
                    for k, (dx, dy) in enumerate([(-0.42, 0.28), (0.10, 0.22), (0.45, 0.30)])
                ])
                g.add(band_hi, ves, prots)
                g.ves_pt = np.array([x + r, band_y, 0.0])
                g.prot_pt = np.array([x + r, bot_y + 0.28, 0.0])
                g.band_right = np.array([x + r, band_y - 0.1, 0.0])
            else:
                mock_pel = Ellipse(width=1.1, height=0.24, stroke_color=LIPO_SLATE, stroke_width=2.0,
                                   fill_color=LIPO_SLATE, fill_opacity=0.28).move_to([x, bot_y + 0.24, 0])
                g.add(mock_pel)
                g.mock_pt = np.array([x + r, bot_y + 0.26, 0.0])
            return g

        t_grad = mini_grad_tube(-4.75, "Gradient", has_vesicles=True)
        t_mock = mini_grad_tube(-1.95, "Cell-free mock", has_vesicles=False)

        dish_specs = [
            ("Vesicle layer (1.13–1.19)", 1.95, VESICLE_GOLD),
            ("Denser protein layer", 0.05, PROTEIN_AMBER),
            ("Cell-free mock", -1.85, LIPO_SLATE),
        ]
        dishes = VGroup()
        for label_txt, yy, col in dish_specs:
            dish_ring = RoundedRectangle(corner_radius=0.20, width=5.4, height=1.58,
                                         stroke_color=col, stroke_width=2.8,
                                         fill_color=PANEL_BG, fill_opacity=0.92).move_to([3.2, yy, 0])
            c_icon = make_target_cell(center=(1.25, yy, 0), radius=0.44, active=False)
            lbl = fit_text(label_txt, max_w=3.7, size=25, color=col, max_lines=1).move_to([3.85, yy + 0.36, 0])
            status = T("Waiting for sample", 24, TEXT).move_to([3.85, yy - 0.14, 0])
            bar_bg = Rectangle(width=3.2, height=0.22, stroke_color=GREY, stroke_width=1.8,
                               fill_color=BG, fill_opacity=0.85).move_to([3.85, yy - 0.50, 0])
            row = VGroup(dish_ring, c_icon, lbl, status, bar_bg)
            row.dish_ring, row.c_icon, row.lbl, row.status, row.bar_bg = dish_ring, c_icon, lbl, status, bar_bg
            dishes.add(row)

        stag = scope_tag("schematic")
        self.add(t_grad, t_mock, dishes, stag)

        self.at("test every layer")
        # Visible pipette transfer + dish fluid highlight so the assay process is unmistakable
        for idx, (src_pt, col, curve_ang) in enumerate([
            (t_grad.ves_pt, VESICLE_GOLD, -0.25),
            (t_grad.prot_pt, PROTEIN_AMBER, 0.18),
        ]):
            dst = dishes[idx].c_icon.get_center()
            arc = ArcBetweenPoints(src_pt, dst, angle=curve_ang)
            drop = Dot(src_pt, radius=0.14, color=col)
            trail = DashedVMobject(arc, num_dashes=10, color=col, dashed_ratio=0.55)
            trail.set_stroke(width=4.5)
            self.play(
                Create(trail),
                MoveAlongPath(drop, arc),
                dishes[idx].dish_ring.animate.set_fill(col, opacity=0.20),
                run_time=0.95,
            )
            s_testing = T("Applied to cells", 24, col).move_to(dishes[idx].status.get_center())
            self.play(FadeOut(drop), FadeOut(trail), swap(dishes[idx].status, s_testing, run_time=0.35),
                      run_time=0.40)
            dishes[idx].status = s_testing

        self.at("mock pellet")
        dst3 = dishes[2].c_icon.get_center()
        arc3 = ArcBetweenPoints(t_mock.mock_pt, dst3, angle=0.15)
        drop3 = Dot(t_mock.mock_pt, radius=0.14, color=LIPO_SLATE)
        trail3 = DashedVMobject(arc3, num_dashes=10, color=LIPO_SLATE, dashed_ratio=0.55)
        trail3.set_stroke(width=4.5)
        self.play(
            Create(trail3),
            MoveAlongPath(drop3, arc3),
            dishes[2].dish_ring.animate.set_fill(LIPO_SLATE, opacity=0.18),
            run_time=1.05,
        )
        s3_testing = T("Applied to cells", 24, LIPO_SLATE).move_to(dishes[2].status.get_center())
        self.play(FadeOut(drop3), FadeOut(trail3), swap(dishes[2].status, s3_testing, run_time=0.35),
                  run_time=0.40)
        dishes[2].status = s3_testing

        self.at("activity tracks")
        act_tracker = ValueTracker(0.02)
        bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.05, 3.2 * act_tracker.get_value()), height=0.22,
            stroke_width=0, fill_color=CELL_EMERALD, fill_opacity=0.95,
        ).align_to(dishes[0].bar_bg, LEFT).match_y(dishes[0].bar_bg))
        self.add(bar_fill)

        s0_new = T("Active signal", 25, CELL_EMERALD).move_to(dishes[0].status.get_center())
        s1_new = T("No response", 25, TEXT).move_to(dishes[1].status.get_center())
        s2_new = T("No response", 25, TEXT).move_to(dishes[2].status.get_center())
        self.play(
            dishes[0].dish_ring.animate.set_stroke(CELL_EMERALD, width=3.5).set_fill(CELL_EMERALD, opacity=0.18),
            dishes[1].dish_ring.animate.set_fill(PANEL_BG, opacity=0.92),
            dishes[2].dish_ring.animate.set_fill(PANEL_BG, opacity=0.92),
            dishes[0].c_icon.outer.animate.set_stroke(CELL_EMERALD).set_fill(CELL_EMERALD, opacity=0.40),
            dishes[0].c_icon.nucleus.animate.set_stroke(CELL_EMERALD).set_fill(CELL_EMERALD, opacity=0.32),
            dishes[0].c_icon.recs.animate.set_color(CELL_EMERALD),
            swap(dishes[0].status, s0_new, run_time=0.6),
            swap(dishes[1].status, s1_new, run_time=0.6),
            swap(dishes[2].status, s2_new, run_time=0.6),
            run_time=0.8,
        )
        self.play(act_tracker.animate.set_value(0.92), run_time=4.2)

        self.at("some lipoproteins")
        stray_lipo = make_lipoprotein(radius=0.19).move_to([-4.65, -1.5, 0])
        zoom_lipo_box = Circle(radius=0.72, stroke_color=LIPO_SLATE, stroke_width=3.0,
                               fill_color=PANEL_BG, fill_opacity=0.95).move_to([-3.35, -2.82, 0])
        zoom_ves = make_vesicle(radius=0.23, n_ligands=6, has_cargo=True, n_dots=1, seed=7,
                                ligand_len=0.05, stroke_w=3.2).move_to([-3.62, -2.78, 0])
        zoom_lp = make_lipoprotein(radius=0.19).move_to([-3.06, -3.15, 0])
        zoom_lp2 = make_lipoprotein(radius=0.16).move_to([-3.35, -3.20, 0])
        caveat_lbl = fit_text("Some lipoproteins overlap", max_w=3.2, size=24, color=LIPO_SLATE).move_to([-0.90, -3.02, 0])
        caveat_arr = Arrow(zoom_lipo_box.get_top() + UP * 0.06, t_grad.band_right + RIGHT * 0.06,
                           color=LIPO_SLATE, stroke_width=3.2, buff=0.05)
        self.play(FadeIn(stray_lipo), run_time=0.35)
        self.play(stray_lipo.animate.move_to([-4.45, 0.22, 0]), run_time=1.8)
        self.play(FadeIn(zoom_lipo_box, scale=0.6), FadeIn(zoom_ves), FadeIn(zoom_lp), FadeIn(zoom_lp2),
                  GrowArrow(caveat_arr), FadeIn(caveat_lbl), run_time=1.0)
        self.play(zoom_lp.animate.move_to([-3.02, -2.75, 0]),
                  zoom_lp2.animate.move_to([-3.32, -2.62, 0]), run_time=2.2)
        self.finish()


class S05Protection(SpokenScene):
    def construct(self):
        tp = TwoPanel("Enzyme alone", "Enzyme + detergent",
                      colors=(CARGO_CYAN, CUT_RED), top=3.05, bottom=-1.45, gap=0.45, width=12.4, size=30)
        tp.left_frame.set_fill(PANEL_BG, opacity=0.85)
        tp.right_frame.set_fill(PANEL_BG, opacity=0.85)

        def panel_vesicle(center, n_ligands=10):
            v = make_vesicle(radius=1.18, n_ligands=n_ligands, has_cargo=True, n_dots=0,
                             ligand_len=0.22, stroke_w=6.0).move_to(center)
            rnas = VGroup()
            for dy, amp in [(0.36, 0.12), (0.0, -0.14), (-0.36, 0.11)]:
                pts = [np.array([-0.58, dy, 0]), np.array([-0.18, dy + amp, 0]),
                       np.array([0.18, dy - amp, 0]), np.array([0.58, dy, 0])]
                s = VMobject(stroke_color=CARGO_CYAN, stroke_width=4.8)
                s.set_points_smoothly([p + center for p in pts])
                rnas.add(s)
            v.rnas = rnas
            v.add(rnas)
            return v

        lc = tp.area("left")[0] + UP * 0.15
        rc = tp.area("right")[0] + UP * 0.15
        v_left = panel_vesicle(lc)
        v_right = panel_vesicle(rc)

        stag = scope_tag("schematic")
        self.add(tp, v_left, v_right, stag)

        outside_tag = T("Surface proteins", 26, LIGAND_CORAL).move_to([lc[0], -1.08, 0])
        inside_tag = T("Sealed RNA cargo", 26, CARGO_CYAN).move_to([rc[0], -1.08, 0])
        self.play(FadeIn(outside_tag), FadeIn(inside_tag), run_time=0.6)
        self.play(Indicate(v_left.ligands, color=LIGAND_CORAL),
                  Indicate(v_right.rnas, color=CARGO_CYAN), run_time=1.3)

        self.at("Treat the vesicles")
        sc_left = make_scissors(center=lc + LEFT * 2.1 + UP * 0.85, scale=0.68, color=CUT_RED)
        sc_right = make_scissors(center=rc + LEFT * 2.1 + UP * 0.85, scale=0.68, color=CUT_RED)
        enz_badge = T("Protease / RNase added", 26, CUT_RED).move_to([0.0, 3.35, 0])
        self.play(FadeOut(outside_tag), FadeOut(inside_tag),
                  FadeIn(sc_left), FadeIn(sc_right), FadeIn(enz_badge), run_time=0.7)
        # Active scissor approach & snip motion before "Surface proteins"
        self.play(
            sc_left.animate.move_to(lc + LEFT * 1.72 + UP * 0.45),
            sc_right.animate.move_to(rc + LEFT * 1.72 + UP * 0.45),
            run_time=1.2,
        )
        self.play(
            Rotate(sc_left.b1, -0.25), Rotate(sc_left.b2, 0.25),
            Rotate(sc_right.b1, -0.25), Rotate(sc_right.b2, 0.25),
            rate_func=there_and_back, run_time=0.8,
        )

        self.at("Surface proteins")
        self.play(sc_left.animate.move_to(lc + LEFT * 1.72), run_time=0.45)
        self.play(FadeOut(v_left.ligands, scale=1.15), run_time=0.55)
        self.play(sc_left.animate.move_to(lc + LEFT * 1.95 + DOWN * 0.25), run_time=0.55)

        self.at("while sealed cargo")
        surv_lbl = T("Sealed cargo survives", 26, CELL_EMERALD).move_to([lc[0], -1.08, 0])
        self.play(FadeIn(surv_lbl), Indicate(v_left.rnas, color=CARGO_CYAN, scale_factor=1.1), run_time=0.9)

        self.at("Adding detergent")
        det_drops = VGroup(*[
            Dot(rc + np.array([np.cos(a), np.sin(a), 0]) * 1.60, radius=0.11, color=DETERGENT_TEAL)
            for a in np.linspace(0, TAU, 8, endpoint=False)
        ])
        self.play(FadeIn(det_drops), run_time=0.3)
        self.play(*[d.animate.move_to(rc + (d.get_center() - rc) * 0.72) for d in det_drops], run_time=0.7)

        frags = VGroup(*[
            Arc(radius=1.22, start_angle=a, angle=0.38, arc_center=rc,
                color=VESICLE_GOLD, stroke_width=5.5)
            for a in np.linspace(0.2, TAU - 0.3, 6)
        ])
        self.play(FadeOut(det_drops), ReplacementTransform(v_right.ring, frags), run_time=0.6)
        self.play(frags.animate.scale(1.12), run_time=0.4)

        self.at("internal cargo")
        self.play(sc_right.animate.move_to(rc), run_time=0.45)
        lost_lbl = T("Both surface & internal cut", 26, CUT_RED).move_to([rc[0], -1.08, 0])
        self.play(
            FadeOut(v_right.ligands, scale=1.1),
            FadeOut(v_right.rnas, scale=0.8),
            FadeIn(lost_lbl),
            run_time=0.8,
        )

        self.at("One caution")
        # Wide caution card keeping scissors and text completely clear of borders
        caut_box = RoundedRectangle(corner_radius=0.16, width=10.8, height=1.25,
                                    stroke_color=PROTEIN_AMBER, stroke_width=2.5,
                                    fill_color=PANEL_BG, fill_opacity=0.95).move_to([-0.85, -2.52, 0])
        loose_rna = VMobject(stroke_color=CARGO_CYAN, stroke_width=4.5)
        loose_rna.set_points_smoothly([
            np.array([-5.75, -2.52, 0]), np.array([-5.30, -2.32, 0]),
            np.array([-4.85, -2.72, 0]), np.array([-4.40, -2.52, 0]),
        ])
        cap_prot = Arc(radius=0.48, start_angle=-0.25, angle=PI + 0.5,
                       arc_center=[-5.08, -2.48, 0], stroke_color=PROTEIN_AMBER, stroke_width=10.0)
        sc_caut = make_scissors(center=[-3.95, -2.30, 0], scale=0.42, color=CUT_RED)
        caut_txt = T("Caution: bound protein can shield loose RNA", 26, PROTEIN_AMBER).move_to([0.35, -2.52, 0])
        self.play(FadeIn(caut_box), FadeIn(loose_rna), FadeIn(cap_prot), FadeIn(sc_caut), FadeIn(caut_txt),
                  run_time=0.7)
        self.play(sc_caut.animate.move_to([-4.35, -2.42, 0]), rate_func=there_and_back, run_time=0.9)
        self.finish()


class S06Volume(SpokenScene):
    def construct(self):
        d_nm = 100.0
        r_m = (d_nm / 2.0) * 1e-9
        vol_L = (4.0 / 3.0) * np.pi * (r_m ** 3) * 1000.0  # 5.236e-19 L
        conc_M = 1e-6
        N_A = 6.022e23
        molecules = vol_L * conc_M * N_A  # 0.315

        v_center = np.array([-3.45, 0.25, 0.0])
        hero = make_vesicle(radius=1.80, n_ligands=16, has_cargo=True, n_dots=0,
                            ligand_len=0.22, stroke_w=7.5).move_to(v_center)
        diam_line = DoubleArrow(v_center + LEFT * 1.80, v_center + RIGHT * 1.80,
                                color=TEXT, stroke_width=3.5, buff=0, tip_length=0.22)
        diam_lbl = M("100 nm", 32, TEXT).next_to(diam_line, UP, buff=0.18)

        # Framed calculation panel on the right
        calc_panel = RoundedRectangle(corner_radius=0.18, width=6.4, height=4.8,
                                      stroke_color=CARGO_CYAN, stroke_width=2.2,
                                      fill_color=PANEL_BG, fill_opacity=0.92).move_to([2.95, 0.25, 0])

        self.add(hero, calc_panel)

        r_x = 2.95
        # Live computed sphere volume fill (d = 100 nm => V = 5.2e-19 L)
        vol_frac = ValueTracker(0.08)
        lumen_op = ValueTracker(0.36)
        lumen_fill = always_redraw(lambda: Circle(
            radius=max(0.08, 1.74 * vol_frac.get_value()),
            stroke_width=0, fill_color=CARGO_CYAN, fill_opacity=lumen_op.get_value(),
        ).move_to(v_center))

        self.add(lumen_fill)
        # Fill the vesicle lumen smoothly before "100 nanometers" is spoken
        self.play(vol_frac.animate.set_value(1.0), run_time=5.4)

        self.at("100 nanometers")
        self.play(Create(diam_line), FadeIn(diam_lbl), run_time=0.8)
        self.play(Indicate(diam_lbl, color=GOLD, scale_factor=1.1), run_time=0.7)

        vol_val = ValueTracker(0.1)
        vol_live = always_redraw(lambda: M(
            f"V ≤ {vol_val.get_value():.1f} × 10⁻¹⁹ L", 32, CARGO_CYAN
        ).move_to([r_x, 1.95, 0]))
        eq1_sub = M("V = (4/3) π r³  (r = 50 nm)", 24, TEXT).move_to([r_x, 1.38, 0])
        fit(eq1_sub, max_w=5.6)

        self.at("encloses at most")
        self.add(vol_live)
        self.play(
            vol_val.animate.set_value(5.0),
            FadeIn(eq1_sub),
            lumen_op.animate.set_value(0.62),
            run_time=3.2,
        )
        vol_final = M("V ≤ 5 × 10⁻¹⁹ L", 32, CARGO_CYAN).move_to([r_x, 1.95, 0])
        self.remove(vol_live)
        self.add(vol_final)
        self.play(
            lumen_op.animate.set_value(0.28),
            Indicate(vol_final, color=GOLD, scale_factor=1.08),
            run_time=1.5,
        )
        self.play(
            lumen_op.animate.set_value(0.50),
            Indicate(eq1_sub, color=CARGO_CYAN, scale_factor=1.04),
            run_time=1.4,
        )

        self.at("Multiply that volume")
        eq2 = M("× 1 µM  (10⁻⁶ mol/L)", 28, TEXT).move_to([r_x, 0.55, 0])
        self.play(FadeIn(eq2), lumen_op.animate.set_value(0.36), run_time=1.2)
        self.play(Indicate(eq2, color=CARGO_CYAN, scale_factor=1.05), lumen_op.animate.set_value(0.46), run_time=1.6)

        self.at("by Avogadro's number")
        eq3 = M("× 6 × 10²³ /mol", 28, TEXT).move_to([r_x, -0.22, 0])
        div_rule = Line([0.65, -0.75, 0], [5.25, -0.75, 0], color=TEXT, stroke_width=3.0)
        mol_bar_bg = Rectangle(width=3.2, height=0.22, stroke_color=GREY, stroke_width=1.8,
                               fill_color=BG, fill_opacity=0.85).move_to([v_center[0], -2.25, 0])
        mol_t = ValueTracker(0.01)
        mol_bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.03, 3.2 * mol_t.get_value()), height=0.22,
            stroke_width=0, fill_color=CARGO_CYAN, fill_opacity=0.95,
        ).align_to(mol_bar_bg, LEFT).match_y(mol_bar_bg))
        mol_unit = T("vs 1 molecule", 24, TEXT).next_to(mol_bar_bg, DOWN, buff=0.14)
        self.play(FadeIn(eq3), Create(div_rule), FadeIn(mol_bar_bg), FadeIn(mol_unit), run_time=2.5)

        three_ves = VGroup(*[
            make_vesicle(radius=0.66, n_ligands=12, has_cargo=False, n_dots=0,
                         ligand_len=0.13, stroke_w=4.5).move_to([-5.15 + i * 1.85, 0.65, 0])
            for i in range(3)
        ])
        single_dot = Dot(three_ves[1].get_center(), radius=0.14, color=CARGO_CYAN)
        dot_note = T("1 dot across 3 vesicles", 26, CARGO_CYAN).move_to([-3.3, -0.68, 0])
        rim_note = T("Surface: many ligands each", 26, LIGAND_CORAL).move_to([-3.3, -1.30, 0])

        self.at("Passive trapping")
        eq4 = M(f"≈ {molecules:.1f} molecules / vesicle", 28, VESICLE_GOLD).move_to([r_x, -1.32, 0])
        self.play(
            FadeOut(hero), FadeOut(lumen_fill), FadeOut(diam_line), FadeOut(diam_lbl),
            run_time=0.45,
        )
        self.play(FadeIn(three_ves), FadeIn(eq4), run_time=0.75)

        self.at("roughly")
        self.add(mol_bar_fill)
        self.play(
            mol_t.animate.set_value(0.315),
            three_ves[1].ring.animate.set_fill(CARGO_CYAN, opacity=0.32),
            FadeIn(single_dot, scale=0.5),
            FadeIn(dot_note),
            FadeIn(rim_note),
            run_time=1.4,
        )
        self.finish()


class S07PredictQ(SpokenScene):
    def construct(self):
        top_eq = VGroup(
            T("copies per vesicle  =", 32, TEXT),
            T("cargo copies", 32, CARGO_CYAN),
            T("÷", 34, TEXT),
            T("particles counted", 32, VESICLE_GOLD),
        ).arrange(RIGHT, buff=0.22).move_to([0, 2.85, 0])

        card = RoundedRectangle(
            corner_radius=0.20, width=10.2, height=2.55,
            stroke_color=TEAL, stroke_width=2.5,
            fill_color=PANEL_BG, fill_opacity=0.92,
        ).move_to([0, 0.75, 0])

        self.play(FadeIn(top_eq[0]), FadeIn(card), run_time=0.7)
        self.at("cargo copies")
        self.play(FadeIn(top_eq[1]), FadeIn(top_eq[2]), run_time=0.75)
        self.at("particles counted")
        self.play(FadeIn(top_eq[3]), run_time=0.75)

        den_val = ValueTracker(0.0)
        num_val = ValueTracker(0.0)
        div_bar = Line([-3.7, 0.75, 0], [2.1, 0.75, 0], color=TEXT, stroke_width=4.0)
        den_counter = counter("{:,.0f} vesicles", den_val, at=[-0.8, 0.15, 0], size=38, color=VESICLE_GOLD)
        num_counter = counter("{:,.0f} copies", num_val, at=[-0.8, 1.38, 0], size=38, color=CARGO_CYAN)
        eq_q = M("=  ?", 44, GOLD).move_to([3.55, 0.75, 0])

        self.at("Suppose a purified")
        self.play(Create(div_bar), run_time=0.8)

        self.at("holds")
        self.add(den_counter)
        self.play(den_val.animate.set_value(2_000_000_000), run_time=0.75)

        self.at("and 40")
        self.add(num_counter)
        self.play(num_val.animate.set_value(40_000_000), run_time=0.85)
        self.play(FadeIn(eq_q), run_time=0.6)

        qcard = question_card("What does the average vesicle hold?", ["Many", "About 1", "Far less than 1"],
                              y=-3.05, color=GOLD, size=30, chip_size=26)
        self.at("Does the average")
        self.play(FadeIn(qcard.question), run_time=0.65)
        self.at("many copies")
        self.play(FadeIn(qcard.chips[0]), run_time=0.45)
        self.at("about one copy")
        self.play(FadeIn(qcard.chips[1]), run_time=0.45)
        self.at("far less")
        self.play(FadeIn(qcard.chips[2]), run_time=0.55)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "What does the average vesicle hold?"
    OPTIONS = ["Many", "About 1", "Far less than 1"]
    CARD = {"y": -3.05, "color": GOLD, "size": 30, "chip_size": 26}
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_backdrop()


class S09Reveal(SpokenScene):
    def construct(self):
        bd = build_predict_backdrop()
        qcard = question_card("What does the average vesicle hold?", ["Many", "About 1", "Far less than 1"],
                              y=-3.05, color=GOLD, size=30, chip_size=26)
        self.add(bd, qcard)

        self.play(
            qcard.chips[2][0].animate.set_stroke(CELL_EMERALD, width=3.5).set_fill(CELL_EMERALD, opacity=0.28),
            qcard.chips[2][1].animate.set_color(CELL_EMERALD),
            FadeOut(qcard.chips[0]), FadeOut(qcard.chips[1]), FadeOut(qcard.question),
            run_time=0.75,
        )

        ratio = 40_000_000 / 2_000_000_000  # 0.02
        eq_top = VGroup(
            M("40,000,000", 32, CARGO_CYAN),
            M("÷", 32, TEXT),
            M("2,000,000,000", 32, VESICLE_GOLD),
            M(f"=  {ratio:.2f}", 34, CELL_EMERALD),
        ).arrange(RIGHT, buff=0.22).move_to([-0.8, 2.75, 0])

        self.at("40 million")
        # FadeOut old text cleanly BEFORE FadeIn of new top equation, and animate live ratio gauge
        self.play(FadeOut(bd), FadeOut(qcard.chips[2]), run_time=0.35)
        self.play(FadeIn(eq_top[:3]), run_time=0.65)

        ratio_val = ValueTracker(0.0)
        ratio_live = always_redraw(lambda: M(f"=  {ratio_val.get_value():.2f}", 34, CELL_EMERALD).next_to(
            eq_top[2], RIGHT, buff=0.22))
        self.at("is 0")
        self.add(ratio_live)
        self.play(ratio_val.animate.set_value(ratio), run_time=1.5)
        self.remove(ratio_live)
        self.add(eq_top[3])

        eq_one50 = M("=  1 copy in 50 vesicles", 30, CARGO_CYAN).move_to([-0.8, 1.98, 0])
        grid = build_grid_50(origin=(-2.65, -0.70, 0), dx=0.76, dy=0.72,
                             occupied_idx=17, n_dots_in_occupied=1, r=0.24)

        self.at("That is just")
        self.play(FadeIn(eq_one50), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(cell, scale=0.7) for cell in grid], lag_ratio=0.03), run_time=2.2)

        self.at("Counts in real")
        # Sweep row-by-row across all 50 vesicles showing 49 empty vs 1 occupied, plus below-1 readout
        row_hl = SurroundingRectangle(grid[:10], color=CARGO_CYAN, buff=0.06, stroke_width=3.2,
                                      fill_color=CARGO_CYAN, fill_opacity=0.08)
        self.play(FadeIn(row_hl), run_time=0.3)
        for r_idx in range(1, 5):
            self.play(row_hl.animate.move_to(grid[r_idx * 10:(r_idx + 1) * 10].get_center()), run_time=0.85)
        below_lbl = T("Real samples: < 1 copy / vesicle", 26, CARGO_CYAN).move_to([-2.65, -2.95, 0])
        self.play(FadeOut(row_hl), FadeIn(below_lbl), run_time=0.6)

        self.at("A vesicle surface")
        surf_ves = make_vesicle(radius=1.32, n_ligands=0, has_cargo=True, n_dots=0,
                                stroke_w=6.5).move_to([3.85, -0.55, 0])
        surf_ves.ring.set_fill(PANEL_BG, opacity=0.92)
        ligs = VGroup()
        for k in range(20):
            ang = k * TAU / 20
            u = np.array([np.cos(ang), np.sin(ang), 0.0])
            stem = Line(surf_ves.get_center() + u * 1.32, surf_ves.get_center() + u * 1.56,
                        color=LIGAND_CORAL, stroke_width=3.5)
            head = Dot(surf_ves.get_center() + u * 1.56, radius=0.058, color=LIGAND_CORAL)
            ligs.add(VGroup(stem, head))
        surf_lbl = T("Surface: many ligand copies", 26, LIGAND_CORAL).move_to([3.85, 1.45, 0])
        self.play(FadeIn(surf_ves), FadeIn(surf_lbl), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(lg, scale=0.6) for lg in ligs], lag_ratio=0.05), run_time=1.8)
        self.finish()


class S10Closing(SpokenScene):
    def construct(self):
        grid = build_grid_50(origin=(0.0, -0.1, 0), dx=0.88, dy=0.82,
                             occupied_idx=17, n_dots_in_occupied=1, r=0.27)
        grid_title = T("Low average ≠ zero signalling", 30, TEXT).move_to([0.0, 2.82, 0])
        stag = scope_tag("schematic")
        self.add(grid, grid_title, stag)

        # Dim the 49 non-subset rings while concentrating copies into rare subset vesicle #17
        others = VGroup(*[grid[i] for i in range(50) if i != 17])
        rare_ring = Circle(radius=0.34, stroke_color=CARGO_CYAN, stroke_width=4.0).move_to(grid[17].get_center())
        incoming_dots = VGroup(*[
            Dot(grid[i].get_center(), radius=0.09, color=CARGO_CYAN)
            for i in (0, 5, 9, 22, 34, 41, 48)
        ])
        self.play(
            others.animate.set_opacity(0.32),
            Create(rare_ring),
            FadeIn(incoming_dots),
            run_time=1.0,
        )
        self.play(*[d.animate.move_to(grid[17].get_center()) for d in incoming_dots], run_time=2.2)

        rare_cell = build_grid_50(origin=(0.0, -0.1, 0), dx=0.88, dy=0.82,
                                  occupied_idx=17, n_dots_in_occupied=8, r=0.27)[17]
        rare_lbl = T("Rare subset carrying most copies?", 28, CARGO_CYAN).move_to([0.0, -2.78, 0])

        self.at("rare subset")
        self.play(
            FadeOut(incoming_dots),
            ReplacementTransform(grid[17], rare_cell),
            FadeIn(rare_lbl),
            run_time=1.0,
        )
        self.play(rare_cell.animate.scale(1.15), rare_ring.animate.scale(1.15), run_time=1.5)

        self.at("realistic doses")
        self.play(
            FadeOut(others), FadeOut(rare_cell), FadeOut(rare_ring),
            FadeOut(grid_title), FadeOut(rare_lbl), FadeOut(stag),
            run_time=0.45,
        )

        panels = VGroup()
        x_cols = [-4.15, 0.0, 4.15]
        titles = ["1. Separate vesicles", "2. Locate cargo", "3. Count copies"]
        colors = [VESICLE_GOLD, CARGO_CYAN, GOLD]

        # Icon 1: mini sucrose gradient (particles start at bottom, separate upward)
        ic1_dots_ves = VGroup(Dot(DOWN * 0.6 + LEFT * 0.25, radius=0.10, color=VESICLE_GOLD),
                              Dot(DOWN * 0.6 + RIGHT * 0.22, radius=0.10, color=VESICLE_GOLD))
        ic1_dots_prot = VGroup(Dot(DOWN * 0.8 + LEFT * 0.2, radius=0.10, color=PROTEIN_AMBER),
                               Dot(DOWN * 0.8 + RIGHT * 0.2, radius=0.10, color=PROTEIN_AMBER))
        ic1_band = Rectangle(width=1.48, height=0.58, stroke_color=VESICLE_GOLD, stroke_width=2.0,
                             fill_color=VESICLE_GOLD, fill_opacity=0.25).shift(UP * 0.28)
        ic1 = VGroup(
            Rectangle(width=1.55, height=2.25, stroke_color=TEXT, stroke_width=2.5,
                      fill_color=LIPO_SLATE, fill_opacity=0.16),
            ic1_band,
            ic1_dots_ves,
            ic1_dots_prot,
        )
        # Icon 2: vesicle protection
        ic2_v = make_vesicle(radius=0.85, n_ligands=8, has_cargo=True, n_dots=3, seed=7,
                             ligand_len=0.16, stroke_w=4.5)
        ic2_sc = make_scissors(center=(-1.12, 0.55, 0), scale=0.46, color=CUT_RED)
        ic2 = VGroup(ic2_v, ic2_sc)
        # Icon 3: copies / particles
        ic3_bar_bg = Rectangle(width=2.2, height=0.20, stroke_color=GREY, stroke_width=1.5,
                               fill_color=BG, fill_opacity=0.8)
        ic3_bar_fill = Rectangle(width=0.08, height=0.20, stroke_width=0,
                                 fill_color=CARGO_CYAN, fill_opacity=0.95)
        ic3 = VGroup(
            M("copies", 28, CARGO_CYAN),
            Line(LEFT * 1.15, RIGHT * 1.15, color=TEXT, stroke_width=3.2),
            M("particles", 28, VESICLE_GOLD),
            ic3_bar_bg,
        ).arrange(DOWN, buff=0.16)

        icons = [ic1, ic2, ic3]
        for x, ttl, col, ic in zip(x_cols, titles, colors, icons):
            frame = RoundedRectangle(corner_radius=0.18, width=3.8, height=4.15,
                                     stroke_color=col, stroke_width=2.5,
                                     fill_color=PANEL_BG, fill_opacity=0.92).move_to([x, 0.2, 0])
            head = fit_text(ttl, max_w=3.4, size=28, color=col).move_to([x, 1.85, 0])
            ic.move_to([x, -0.15, 0])
            card = VGroup(frame, head, ic)
            card.frame, card.head, card.ic = frame, head, ic
            panels.add(card)

        ic3_bar_fill.align_to(ic3_bar_bg, LEFT).match_y(ic3_bar_bg)
        dose_banner = T("Realistic doses + honest controls", 30, TEXT).move_to([0, 2.95, 0])
        self.play(FadeIn(dose_banner), FadeIn(panels), FadeIn(ic3_bar_fill), run_time=0.65)
        # Animate all 3 mini-verification processes across 7.3..13.5s
        self.play(
            ic1_dots_ves.animate.move_to(ic1_band.get_center()),
            ic2_sc.animate.move_to(ic2_v.get_left() + LEFT * 0.12),
            ic3_bar_fill.animate.stretch_to_fit_width(0.35).align_to(ic3_bar_bg, LEFT),
            run_time=1.8,
        )
        self.play(
            FadeOut(ic2_v.ligands),
            ic2_sc.animate.shift(LEFT * 0.25 + DOWN * 0.2),
            run_time=1.2,
        )

        def check_mark(at_pt):
            p1 = np.array(at_pt) + np.array([-0.22, 0.02, 0])
            p2 = np.array(at_pt) + np.array([-0.04, -0.18, 0])
            p3 = np.array(at_pt) + np.array([0.26, 0.20, 0])
            m = VMobject(stroke_color=CELL_EMERALD, stroke_width=6.0)
            m.set_points_as_corners([p1, p2, p3])
            return m

        c1 = check_mark([-4.15, -2.45, 0])
        c2 = check_mark([0.0, -2.45, 0])
        c3 = check_mark([4.15, -2.45, 0])

        self.at("separating vesicles")
        self.play(panels[0].frame.animate.set_stroke(CELL_EMERALD, width=4.5).set_fill(CELL_EMERALD, opacity=0.14),
                  Create(c1), run_time=0.85)

        self.at("locating cargo")
        self.play(panels[1].frame.animate.set_stroke(CELL_EMERALD, width=4.5).set_fill(CELL_EMERALD, opacity=0.14),
                  Create(c2), run_time=0.85)

        self.at("counting copies")
        self.play(panels[2].frame.animate.set_stroke(CELL_EMERALD, width=4.5).set_fill(CELL_EMERALD, opacity=0.14),
                  Create(c3), run_time=0.85)
        self.finish()


class S11End(EndCard):
    LINE = "Proving vesicle signalling requires separating vesicles,\nlocating cargo, and counting copies."
