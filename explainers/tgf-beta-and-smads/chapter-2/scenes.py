"""Context and Brakes: How Cells Read TGF-β — animation scenes.

COLOUR MAP (one colour per concept, used across the entire film):
- TGF-β ligand dimer:          AMBER       (#F5A228)
- Type II receptor:            CYAN        (#58C4DD, bp_style BLUE)
- Type I receptor:             INDIGO      (#818CF8)
- Phosphate (P):               YELLOW      (#F5D547, bp_style YELLOW)
- R-Smad (Smad2/3):            EMERALD     (#34D399)
- Smad4:                       VIOLET      (#B388FF)
- Nuclear rim & DNA highlight: GOLD        (#D4A843, bp_style GOLD)
- Epithelial partner:          TERRACOTTA  (#E87A5D)
- Fibroblast partner:          SKY_BLUE    (#60B5F7)
- Arrest / Stop dividing:      TEAL/GREEN  (#3FB8C0 / #83C167)
- Tumour escape / Myc down:    RED         (#FC6255)
- Extracellular matrix (ECM):  GREY        (#8B93A1)
- Latent precursor wrapper:    SLATE       (#94A3B8)
- Inhibitory Smad7 / Smad6:    CRIMSON     (#F43F5E)
- Smurf ubiquitin ligase:      BURNT_AMBER (#F97316)

CARRIED WORLD:
A cellular cross-section running from extracellular matrix fibres above, across the plasma
membrane (Type II + Type I receptors) in the middle, down into the golden nuclear rim and
DNA strand at the bottom — zooming smoothly into the nuclear DNA when DNA reading and
cell-specific gene responses are the subject, and pulling back to the membrane-to-nucleus
cross-section for the three layered brakes.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook:            Computed sinusoidal DNA wave propagates; Smad trimer glides from bridged
                       receptors across the nuclear rim; epithelial cell-cycle ring halts under
                       a teal arrest bar while a late-tumour outline migrates rightward.
- s02_weak_grip:       A 2,560-bp DNA sequence is generated with np.random.default_rng(7) (p=0.25
                       per base) and scanned for exact GTCT matches; the DNA ribbon scrolls past
                       a live bp counter and match counter while the Smad MH1 prong dips, wobbles,
                       and slips off single GTCT notches, and '4 × 4 × 4 × 4 = 256' builds in sync.
- s03_partners:        Closed chromatin coils open at cell-specific positions in two side-by-side
                       nuclei; terracotta and sky-blue partner blocks dock on nearby DNA so the
                       identical hovering Smad trimers snap firmly into place and light up.
- s04_outcomes_cancer: From the carried TwoPanel nuclei, p15/p21 bars rise and Myc drops in
                       epithelial cells while collagen fibres grow in fibroblasts; then the
                       epithelial panel transitions to Late tumour as the arrest bar snaps in two,
                       a tumour cell migrates, and an immune cell halts.
- s05_predict:         Camera pulls up to the carried membrane cross-section; amber TGF-β dimers
                       bob gently among grey ECM fibres above unphosphorylated, separated Type II
                       and Type I receptors while the nuclear Smad signal stays flat at zero.
- s07_brake1_latent:   Slate wrapper rings appear around the bobbing amber dimers, cut free yet stay
                       clamped ('Cut, but still bound (latent)') and tethered to ECM fibres; a teal
                       integrin pulls one cage open and protease scissors snip another, freeing an
                       amber dimer to bridge Type II and Type I and light P.
- s08_brake2_smad7:    Phosphorylated Smad trimer enters the nucleus above waving DNA and switches
                       on the Smad7 gene; crimson Smad7 blocks rise to cap Type I's docking site
                       and physically bounce an incoming emerald R-Smad away, with Smad6 shown on
                       the BMP branch.
- s09_brake3_smurfs:   Crimson Smad7 recruits burnt-amber Smurf ligase; gold ubiquitin beads chain
                       onto Type I and pull it into a contracting degradation ring as the signal
                       meter drops to rest, followed by Smad4 loss and GS-catch loosening.
- s10_return_rule:     Full balanced cross-section settles: nuclear DNA with open chromatin and
                       cell-specific partners glows below while latent cages, Smad7, and Smurf
                       restrain the membrane relay above.
"""

from bp_parts import *

# Concept palette
AMBER = "#F5A228"
CYAN = BLUE           # #58C4DD
INDIGO = "#818CF8"
EMERALD = "#34D399"
VIOLET = "#B388FF"
TERRACOTTA = "#E87A5D"
SKY_BLUE = "#60B5F7"
SLATE = "#94A3B8"
CRIMSON = "#F43F5E"
BURNT_AMBER = "#F97316"

# Deterministic 2,560-bp DNA sequence for s02 (equal base frequencies -> 1 in 256 expected)
_RNG = np.random.default_rng(7)
_BASES = np.array(list("ACGT"))
_SEQ = "".join(_RNG.choice(_BASES, size=2560))
GTCT_SITES = [i for i in range(len(_SEQ) - 3) if _SEQ[i:i + 4] == "GTCT"]


# ------------------------------------------------------------------ shared schematic parts
def make_p_badge(center=ORIGIN, radius=0.26):
    """Yellow phosphate badge with crisp dark P (>= 24 pt, generous margin inside circle)."""
    c = Circle(radius=radius, color=YELLOW, fill_color=YELLOW, fill_opacity=1.0, stroke_width=2.5).move_to(center)
    t = T("P", size=24, color=BG, weight=BOLD).move_to(c)
    return VGroup(c, t)


def make_ligand(center=ORIGIN, scale=1.0, color=AMBER):
    """Schematic TGF-beta dimer: two symmetric lobes joined by a short bridge."""
    lobe_l = RoundedRectangle(corner_radius=0.18, width=0.44, height=0.36, color=color,
                              fill_color=color, fill_opacity=0.90, stroke_width=3.0).shift(LEFT * 0.24)
    lobe_r = RoundedRectangle(corner_radius=0.18, width=0.44, height=0.36, color=color,
                              fill_color=color, fill_opacity=0.90, stroke_width=3.0).shift(RIGHT * 0.24)
    bridge = Line(LEFT * 0.08, RIGHT * 0.08, color=TEXT, stroke_width=3.5)
    return VGroup(lobe_l, lobe_r, bridge).scale(scale).move_to(center)


def make_smad_trimer(center=ORIGIN, scale=1.0, phosphorylated=True, show_prong=True, with_smad4=True):
    """2 emerald R-Smad wedges + 1 violet Smad4 cap + optional MH1 prong.
    P badges sit cleanly on the upper shoulders flanking Smad4 (no straddle, never < 24 pt)."""
    r1 = RoundedRectangle(corner_radius=0.14, width=0.72, height=0.48, color=EMERALD,
                          fill_color=EMERALD, fill_opacity=0.36, stroke_width=3.5).shift(LEFT * 0.42 + DOWN * 0.12)
    r2 = RoundedRectangle(corner_radius=0.14, width=0.72, height=0.48, color=EMERALD,
                          fill_color=EMERALD, fill_opacity=0.36, stroke_width=3.5).shift(RIGHT * 0.42 + DOWN * 0.12)
    geom = VGroup(r1, r2)
    if with_smad4:
        s4 = RoundedRectangle(corner_radius=0.16, width=0.66, height=0.44, color=VIOLET,
                              fill_color=VIOLET, fill_opacity=0.38, stroke_width=3.5).shift(UP * 0.42)
        geom.add(s4)
    if show_prong:
        prong = Polygon([-0.18, -0.37, 0], [0.18, -0.37, 0], [0.0, -0.62, 0],
                        color=EMERALD, fill_color=EMERALD, fill_opacity=0.65, stroke_width=3.0)
        geom.add(prong)
    geom.scale(scale)

    g = VGroup(geom)
    if phosphorylated:
        # Place unscaled P badges (>= 24 pt) clear of r1, r2, s4, and any left-docking partner
        p1_pos = np.array([-0.74 * max(scale, 0.85), 0.50 * max(scale, 0.85), 0.0])
        p2_pos = np.array([0.74 * max(scale, 0.85), 0.50 * max(scale, 0.85), 0.0])
        g.add(make_p_badge(p1_pos, radius=0.26), make_p_badge(p2_pos, radius=0.26))
    return g.move_to(center)


def make_partner(kind="epithelial", center=ORIGIN, scale=1.0):
    """Cell-specific partner transcription factor with a shape that clasps the Smad trimer."""
    if kind == "epithelial":
        body = Polygon(
            [-0.58, -0.36, 0], [0.50, -0.36, 0], [0.50, -0.10, 0],
            [0.26, -0.10, 0], [0.26, 0.24, 0], [-0.50, 0.24, 0],
            color=TERRACOTTA, fill_color=TERRACOTTA, fill_opacity=0.40, stroke_width=3.5
        )
        foot = RoundedRectangle(corner_radius=0.07, width=0.92, height=0.16, color=TERRACOTTA,
                                fill_color=TERRACOTTA, fill_opacity=0.68, stroke_width=2.5).shift(DOWN * 0.44)
    else:
        body = Polygon(
            [-0.52, -0.36, 0], [0.54, -0.36, 0], [0.46, 0.28, 0],
            [-0.22, 0.28, 0], [-0.22, -0.02, 0], [-0.52, -0.12, 0],
            color=SKY_BLUE, fill_color=SKY_BLUE, fill_opacity=0.40, stroke_width=3.5
        )
        foot = RoundedRectangle(corner_radius=0.07, width=0.92, height=0.16, color=SKY_BLUE,
                                fill_color=SKY_BLUE, fill_opacity=0.68, stroke_width=2.5).shift(DOWN * 0.44)
    return VGroup(body, foot).scale(scale).move_to(center)


def make_wave_dna(x0=-5.8, x1=5.8, y=0.0, amp=0.12, k=1.4, phase=0.0, n_rungs=24, color=GOLD):
    """Computed sinusoidal DNA ribbon with base-pair rungs."""
    xs = np.linspace(x0, x1, 140)
    top_pts = [np.array([x, y + 0.14 + amp * np.sin(k * x - phase), 0.0]) for x in xs]
    bot_pts = [np.array([x, y - 0.14 + amp * np.sin(k * x - phase + 0.5), 0.0]) for x in xs]
    s1 = VMobject(color=color, stroke_width=4.5).set_points_as_corners(top_pts)
    s2 = VMobject(color=TEXT, stroke_width=3.5, stroke_opacity=0.80).set_points_as_corners(bot_pts)
    rungs = VGroup()
    for rx in np.linspace(x0 + 0.25, x1 - 0.25, n_rungs):
        yt = y + 0.14 + amp * np.sin(k * rx - phase)
        yb = y - 0.14 + amp * np.sin(k * rx - phase + 0.5)
        rungs.add(Line([rx, yb, 0], [rx, yt, 0], color=GREY, stroke_width=2.5))
    return VGroup(rungs, s2, s1)


def make_membrane_band(y=0.75, x0=-6.4, x1=6.4):
    """Plasma membrane bilayer bars across the frame."""
    top = Line([x0, y + 0.15, 0], [x1, y + 0.15, 0], color=SLATE, stroke_width=4.5)
    bot = Line([x0, y - 0.15, 0], [x1, y - 0.15, 0], color=SLATE, stroke_width=4.5)
    fill = Rectangle(width=x1 - x0, height=0.30, fill_color=SLATE, fill_opacity=0.20, stroke_width=0).move_to([0, y, 0])
    return VGroup(fill, top, bot)


def make_ecm_fibres(y_min=1.35, y_max=2.78, x0=-6.2, x1=6.2):
    """Crisscrossing schematic extracellular matrix fibres."""
    return VGroup(
        Line([x0, y_min + 0.30, 0], [x1, y_max - 0.20, 0], color=GREY, stroke_width=3.5, stroke_opacity=0.58),
        Line([x0, y_max - 0.15, 0], [x1, y_min + 0.45, 0], color=GREY, stroke_width=3.5, stroke_opacity=0.52),
        Line([x0 + 0.3, y_min + 0.78, 0], [x1 - 0.2, y_min + 0.72, 0], color=GREY, stroke_width=3.0, stroke_opacity=0.48),
        Line([x0 + 0.8, y_max - 0.42, 0], [x1 - 1.0, y_min + 0.20, 0], color=GREY, stroke_width=3.0, stroke_opacity=0.48),
    )


def make_receptor_pair(cx=0.0, y_mem=0.75, active=False, gap=1.48, gs_open=False, scale=1.0):
    """Type II (cyan) on left + Type I (indigo) on right across the membrane."""
    x2 = -gap / 2
    x1 = gap / 2
    t2_ext = RoundedRectangle(corner_radius=0.14, width=0.46, height=0.68, color=CYAN,
                              fill_color=CYAN, fill_opacity=0.34 if active else 0.18, stroke_width=3.5).move_to([x2, 0.42, 0])
    t2_tm = Line([x2, 0.12, 0], [x2, -0.25, 0], color=CYAN, stroke_width=8)
    t2_kin = RoundedRectangle(corner_radius=0.14, width=0.58, height=0.66, color=CYAN,
                              fill_color=CYAN, fill_opacity=0.36 if active else 0.18, stroke_width=3.5).move_to([x2, -0.62, 0])
    t2 = VGroup(t2_ext, t2_tm, t2_kin)

    t1_ext = RoundedRectangle(corner_radius=0.14, width=0.46, height=0.68, color=INDIGO,
                              fill_color=INDIGO, fill_opacity=0.34 if active else 0.18, stroke_width=3.5).move_to([x1, 0.42, 0])
    t1_tm = Line([x1, 0.12, 0], [x1, -0.25, 0], color=INDIGO, stroke_width=8)
    t1_kin = RoundedRectangle(corner_radius=0.14, width=0.60, height=0.66, color=INDIGO,
                              fill_color=INDIGO, fill_opacity=0.36 if active else 0.18, stroke_width=3.5).move_to([x1, -0.62, 0])
    gs_angle = -0.55 if (active or gs_open) else 0.0
    gs_bar = Line([x1 - 0.36, -0.35, 0], [x1 - 0.36, -0.72, 0], color=GOLD, stroke_width=5.5)
    gs_bar.rotate(gs_angle, about_point=[x1 - 0.36, -0.35, 0])
    t1 = VGroup(t1_ext, t1_tm, t1_kin, gs_bar)

    geom = VGroup(t2, t1).scale(scale).shift([cx, y_mem, 0])
    g = VGroup(geom)
    g.t2, g.t1, g.t1_kin, g.gs_bar = t2, t1, t1_kin, gs_bar
    if active:
        p = make_p_badge([cx, y_mem - 0.62 * scale, 0], radius=0.24)
        g.add(p)
        g.p_badge = p
    return g


def make_nuclear_rim(y=-1.65, width=13.2):
    """Golden glowing nuclear envelope arc across the bottom of the cellular cross-section."""
    arc = ArcBetweenPoints([-width / 2, y - 0.45, 0], [width / 2, y - 0.45, 0], angle=-0.22,
                           color=GOLD, stroke_width=5.5)
    glow = ArcBetweenPoints([-width / 2, y - 0.45, 0], [width / 2, y - 0.45, 0], angle=-0.22,
                            color=GOLD, stroke_width=16, stroke_opacity=0.22)
    return VGroup(glow, arc)


def make_latent_cage(center=ORIGIN, open_frac=0.0):
    """Two slate-grey precursor wrapper shells around a center, opening by open_frac in [0, 1]."""
    ang_off = 0.65 * open_frac
    top_shell = Arc(radius=0.56, start_angle=0.15 + ang_off, angle=PI - 0.30, arc_center=center,
                    color=SLATE, stroke_width=6.5)
    bot_shell = Arc(radius=0.56, start_angle=PI + 0.15 - ang_off, angle=PI - 0.30, arc_center=center,
                    color=SLATE, stroke_width=6.5)
    return VGroup(top_shell, bot_shell)


def make_scissors(center=ORIGIN, color=TEXT):
    """Clean schematic protease scissor icon."""
    b1 = Line([-0.28, -0.18, 0], [0.28, 0.18, 0], color=color, stroke_width=3.5)
    b2 = Line([-0.28, 0.18, 0], [0.28, -0.18, 0], color=color, stroke_width=3.5)
    r1 = Circle(radius=0.10, color=color, stroke_width=3.0).move_to([-0.34, -0.22, 0])
    r2 = Circle(radius=0.10, color=color, stroke_width=3.0).move_to([-0.34, 0.22, 0])
    return VGroup(b1, b2, r1, r2).move_to(center)


def make_membrane_world(active=False, with_dimers=True, caged=False, y_nuc=-1.65):
    """Standard carried membrane-to-nucleus cross-section for s05-s10."""
    ecm = make_ecm_fibres(y_min=1.35, y_max=2.78)
    mem = make_membrane_band(y=0.72)
    rec = make_receptor_pair(cx=0.0, y_mem=0.72, active=active, gap=1.48 if active else 2.2)
    nuc = make_nuclear_rim(y=y_nuc)
    world = VGroup(ecm, mem, rec, nuc)
    world.ecm, world.mem, world.rec, world.nuc = ecm, mem, rec, nuc
    dimers, cages, tethers = VGroup(), VGroup(), VGroup()
    if with_dimers:
        spots = [(-3.6, 2.20, 0), (-1.4, 2.25, 0), (1.3, 2.22, 0), (3.6, 2.18, 0)]
        for pos in spots:
            d = make_ligand(pos, scale=0.84)
            dimers.add(d)
            if caged:
                cages.add(make_latent_cage(pos, open_frac=0.0))
                tethers.add(Line(np.array(pos) + UP * 0.54, np.array(pos) + UP * 0.78 + RIGHT * 0.15,
                                 color=SLATE, stroke_width=3.2))
        world.add(dimers, cages, tethers)
    world.dimers, world.cages, world.tethers = dimers, cages, tethers
    return world


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "TGF-β and Smads"
    TITLE = "Context and Brakes: How Cells Read TGF-β"


class S01Hook(SpokenScene):
    def construct(self):
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(1.2 * dt))
        self.add(phase)

        rim = ArcBetweenPoints([-6.3, 1.35, 0], [6.3, 1.35, 0], angle=-0.24, color=GOLD, stroke_width=5.5)
        rim_glow = ArcBetweenPoints([-6.3, 1.35, 0], [6.3, 1.35, 0], angle=-0.24, color=GOLD, stroke_width=16, stroke_opacity=0.22)
        dna = always_redraw(lambda: make_wave_dna(x0=-5.8, x1=5.8, y=-0.32, amp=0.11, phase=phase.get_value()))
        smad = make_smad_trimer([-0.3, 2.75, 0], scale=1.0, phosphorylated=True, show_prong=False)
        smad_lbl = T("Smad complex", 28, EMERALD).next_to(smad, RIGHT, buff=0.25)

        # Compact receptor bridge at top-left, label clearly inside frame
        rec = make_receptor_pair(cx=-2.55, y_mem=2.55, active=False, gap=1.35, scale=0.72)
        lig = make_ligand([-2.55, 3.22, 0], scale=0.72)
        rec_lbl = T("Type II + Type I", 28, CYAN).next_to(rec, LEFT, buff=0.22)
        tag = scope_tag("schematic")

        self.play(FadeIn(rim_glow), FadeIn(rim), FadeIn(dna), FadeIn(tag), run_time=0.7)
        self.add(rec, lig, rec_lbl)
        self.at("bridged two kinases")
        rec_on = make_receptor_pair(cx=-2.55, y_mem=2.55, active=True, gap=1.18, scale=0.72)
        self.play(
            lig.animate.move_to([-2.55, 2.95, 0]),
            Transform(rec, rec_on),
            run_time=0.9,
        )
        self.at("into the nucleus")
        self.play(
            FadeIn(smad),
            FadeIn(smad_lbl),
            smad.animate.move_to([0.0, 0.72, 0]),
            smad_lbl.animate.move_to([2.35, 0.72, 0]),
            run_time=1.3,
        )

        # Left: dividing cell cycle ring halted by Stop dividing bar placed cleanly below ring
        epi_ring = Circle(radius=0.64, color=TEAL, stroke_width=6).move_to([-3.7, -1.55, 0])
        epi_dot = Dot(color=TEAL, radius=0.12).move_to(epi_ring.get_top())
        spin = ValueTracker(1.0)
        epi_ang = ValueTracker(0.0)
        epi_ang.add_updater(lambda m, dt: m.increment_value(2.4 * spin.get_value() * dt))
        self.add(epi_ang)
        epi_dot.add_updater(lambda m: m.move_to(
            epi_ring.get_center() + 0.64 * np.array([np.cos(epi_ang.get_value()), np.sin(epi_ang.get_value()), 0])
        ))
        pause_bars = VGroup(
            Line([-3.84, -1.75, 0], [-3.84, -1.35, 0], color=TEAL, stroke_width=6),
            Line([-3.56, -1.75, 0], [-3.56, -1.35, 0], color=TEAL, stroke_width=6),
        )
        stop_bar = boxed_label("Stop dividing", TEAL, size=28, pad=0.14).move_to([-3.7, -2.62, 0])
        epi_lbl = T("Healthy epithelial cell", 28, TEXT).move_to([-3.7, -3.28, 0])
        arr_l = Arrow([-0.4, 0.15, 0], [-2.85, -1.05, 0], color=TEAL, stroke_width=4, buff=0.12)

        self.at("halts many healthy")
        self.play(FadeIn(epi_ring), FadeIn(epi_dot), FadeIn(epi_lbl), GrowArrow(arr_l), run_time=0.9)
        self.play(spin.animate.set_value(0.0), FadeIn(pause_bars), FadeIn(stop_bar), run_time=0.7)

        # Right: late tumour cell migrates rightward
        tum_track = Line([1.3, -2.05, 0], [5.7, -2.05, 0], color=GREY, stroke_width=3)
        tum_cell = RoundedRectangle(corner_radius=0.28, width=1.20, height=0.60, color=RED,
                                    fill_color=RED, fill_opacity=0.32, stroke_width=4).move_to([2.0, -1.68, 0])
        tum_lbl = T("Late tumour: move", 28, RED).move_to([3.5, -2.65, 0])
        arr_r = Arrow([0.3, 0.15, 0], [2.1, -1.25, 0], color=RED, stroke_width=4, buff=0.12)
        self.at("late tumors spread")
        self.play(FadeIn(tum_track), FadeIn(tum_cell), FadeIn(tum_lbl), GrowArrow(arr_r), run_time=0.8)
        self.play(tum_cell.animate.shift(RIGHT * 2.8), run_time=2.3, rate_func=linear)

        self.at("opposite answers")
        q_top = T("Same signal → opposite answers?", 30, GOLD).move_to([2.55, 3.12, 0])
        self.play(FadeIn(q_top), run_time=0.7)

        self.at("holds it back")
        q_brake = boxed_label("What holds it back?", AMBER, size=28, pad=0.15).move_to([2.55, 2.38, 0])
        self.play(FadeIn(q_brake), run_time=0.6)
        self.finish()


class S02WeakGrip(SpokenScene):
    def construct(self):
        head = T("Smad MH1 domain meets DNA", 34, TEXT).move_to([0, HEAD_Y, 0])
        tag = scope_tag("schematic")

        bp_pos = ValueTracker(0.0)
        self.add(bp_pos)
        window_bp = 420.0  # wider window so computed GTCT hits stay visible as ribbon scrolls

        def draw_genome_ribbon():
            pos = bp_pos.get_value()
            x0, x1, y = -5.8, 5.8, -0.65
            scale = (x1 - x0) / window_bp
            back_top = Line([x0, y + 0.18, 0], [x1, y + 0.18, 0], color=GOLD, stroke_width=4.5)
            back_bot = Line([x0, y - 0.18, 0], [x1, y - 0.18, 0], color=TEXT, stroke_width=3.5, stroke_opacity=0.80)
            g = VGroup(back_top, back_bot)
            # Fixed 27 tick slots so always_redraw never changes submobject count
            first_tick = int(pos // 16) * 16
            ticks_xs = [x0 + (b - pos) * scale for b in range(first_tick, first_tick + 27 * 16, 16)]
            for tx in ticks_xs:
                if x0 <= tx <= x1:
                    g.add(Line([tx, y - 0.16, 0], [tx, y + 0.16, 0], color=GREY, stroke_width=2.2))
                else:
                    g.add(Line([x0, y, 0], [x0, y, 0], color=BG, stroke_width=0))
            # Fixed 6 GTCT notch + label slots
            vis_sites = [idx for idx in GTCT_SITES if pos - 4 <= idx <= pos + window_bp][:6]
            last_label_x = -99.0
            for slot in range(6):
                if slot < len(vis_sites):
                    x = x0 + (vis_sites[slot] - pos) * scale
                    notch = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.46, color=YELLOW,
                                             fill_color=YELLOW, fill_opacity=0.90, stroke_width=2).move_to([x, y, 0])
                    if -4.6 <= x <= 4.6 and (x - last_label_x) >= 1.35:
                        lbl = T("GTCT", 24, YELLOW, weight=BOLD).move_to([x, y - 0.65, 0])
                        last_label_x = x
                    else:
                        lbl = T("GTCT", 24, BG).move_to([-4.5 + slot * 1.8, -3.45, 0])
                else:
                    notch = RoundedRectangle(corner_radius=0.06, width=0.02, height=0.02, color=BG,
                                             fill_color=BG, fill_opacity=0, stroke_width=0).move_to([x0, y, 0])
                    lbl = T("GTCT", 24, BG).move_to([-4.5 + slot * 1.8, -3.45, 0])
                g.add(notch, lbl)
            return g

        ribbon = always_redraw(draw_genome_ribbon)
        first_site = GTCT_SITES[0]
        bp_pos.set_value(max(0.0, first_site - 140.0))

        smad = make_smad_trimer([0.0, 1.15, 0], scale=1.18, phosphorylated=True, show_prong=True)
        smad_lbl = T("Smad MH1 prong", 28, EMERALD).move_to([0.0, 2.48, 0])

        self.play(FadeIn(head), FadeIn(tag), FadeIn(ribbon), run_time=0.8)
        self.at("meets DNA")
        self.play(FadeIn(smad), FadeIn(smad_lbl), run_time=0.8)

        self.at("reads a tiny")
        site_x = -5.8 + (first_site - bp_pos.get_value()) * (11.6 / window_bp)
        self.play(
            smad.animate.move_to([site_x, 0.36, 0]),
            smad_lbl.animate.move_to([site_x, 1.85, 0]),
            run_time=1.0,
        )

        self.at("such as GTCT")
        tag_box = boxed_label("4-base tag: GTCT", YELLOW, size=26, pad=0.14).move_to([0.0, -2.90, 0])
        self.play(FadeIn(tag_box), run_time=0.6)

        self.at("grips it weakly")
        for ang, dx in [(0.16, 0.14), (-0.18, -0.16), (0.14, 0.12)]:
            self.play(
                Rotate(smad, ang, about_point=smad.get_center()),
                smad.animate.shift(RIGHT * dx + UP * 0.12),
                run_time=0.30,
            )
        self.play(
            smad.animate.move_to([0.0, 0.92, 0]).rotate(-0.12),
            smad_lbl.animate.move_to([0.0, 2.38, 0]),
            run_time=0.50,
        )

        # Build '4 × 4 × 4 × 4 = 256' word-by-word beside the overlay; never show a number before spoken
        f_4a = M("4", 26, GOLD)
        f_x1 = M("×", 26, TEXT)
        f_4b = M("4", 26, GOLD)
        f_x2 = M("×", 26, TEXT)
        f_4c = M("4", 26, GOLD)
        f_x3 = M("×", 26, TEXT)
        f_4d = M("4", 26, GOLD)
        f_eq = M("=", 26, TEXT)
        f_256 = M("256", 26, GOLD)
        formula_parts = VGroup(f_4a, f_x1, f_4b, f_x2, f_4c, f_x3, f_4d, f_eq, f_256).arrange(RIGHT, buff=0.09)
        formula_box = RoundedRectangle(
            corner_radius=0.14, width=formula_parts.width + 0.36, height=formula_parts.height + 0.28,
            stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.14,
        ).move_to([-3.35, -2.90, 0])
        formula_parts.move_to(formula_box)

        ov_256 = boxed_label("4 bases: 1 in 256 bp", GOLD, size=24, pad=0.14).move_to([1.65, -2.90, 0])
        ov_mil = boxed_label("4 bases: 1 in 256 bp (millions of sites)", GOLD, size=24, pad=0.14).move_to([1.65, -2.90, 0])

        self.at("one of four letters")
        self.play(FadeOut(tag_box), FadeIn(formula_box), FadeIn(f_4a), run_time=0.45)

        self.at("so a 4 base tag")
        self.play(FadeIn(f_x1), FadeIn(f_4b), run_time=0.25)
        self.play(FadeIn(f_x2), FadeIn(f_4c), run_time=0.25)
        self.play(FadeIn(f_x3), FadeIn(f_4d), run_time=0.25)

        self.at("appears by chance")
        c_bp = counter("scanned = {:4.0f} bp", bp_pos, at=[-4.15, 2.40, 0], size=26, color=TEXT)
        hits_val = always_redraw(lambda: M(
            f"GTCT hits = {sum(1 for i in GTCT_SITES if i <= bp_pos.get_value() + 210.0):3d}",
            26, YELLOW
        ).move_to([-4.15, 1.85, 0]))
        self.play(FadeIn(c_bp), FadeIn(hits_val), run_time=0.40)
        self.play(bp_pos.animate.set_value(820.0), run_time=1.55, rate_func=linear)

        self.at("256")
        self.play(FadeIn(f_eq), FadeIn(f_256), FadeIn(ov_256), run_time=0.55)
        self.play(bp_pos.animate.set_value(1450.0), run_time=2.25, rate_func=linear)

        self.at("millions of times")
        self.play(swap(ov_256, ov_mil, run_time=0.55))
        self.play(
            bp_pos.animate.set_value(2050.0),
            smad.animate.shift(DOWN * 0.35),
            run_time=2.25,
            rate_func=linear,
        )
        self.play(smad.animate.shift(UP * 0.45), run_time=0.50)

        self.at("alone cannot pick")
        miss_lbl = boxed_label("Weak grip:\ncannot pick a gene", RED, size=26, pad=0.14).move_to([4.15, 2.15, 0])
        self.play(FadeIn(miss_lbl), run_time=0.7)
        self.finish()


class S03Partners(SpokenScene):
    def construct(self):
        tp = TwoPanel("Epithelial nucleus", "Fibroblast nucleus", colors=(TERRACOTTA, SKY_BLUE), top=3.15, bottom=-2.35)
        tag = scope_tag("schematic")
        self.play(FadeIn(tp), FadeIn(tag), run_time=0.7)

        def build_panel_dna(cx, y_dna, open_x_off):
            strand = Line([cx - 2.65, y_dna, 0], [cx + 2.65, y_dna, 0], color=GOLD, stroke_width=4.5)
            # Start with closed chromatin coils covering the entire DNA strand including binding sites
            coil_dxs = [-2.20, -1.65, -1.10, -0.55, 0.00, 0.55, 1.10, 1.65, 2.20]
            coils = VGroup(*[
                Circle(radius=0.22, color=GREY, fill_color=GREY, fill_opacity=0.45, stroke_width=2.5)
                .move_to([cx + dx, y_dna, 0])
                for dx in coil_dxs
            ])
            gtct_box = RoundedRectangle(corner_radius=0.06, width=0.68, height=0.34, color=YELLOW,
                                        fill_color=YELLOW, fill_opacity=0.28, stroke_width=2.5).move_to([cx + open_x_off + 0.44, y_dna, 0])
            gtct_txt = T("GTCT", 24, YELLOW, weight=BOLD).move_to([cx + open_x_off + 0.44, y_dna - 0.48, 0])
            part_box = RoundedRectangle(corner_radius=0.06, width=0.84, height=0.34, color=TEXT,
                                        fill_color=TEXT, fill_opacity=0.18, stroke_width=2.5).move_to([cx + open_x_off - 0.72, y_dna, 0])
            sites = VGroup(gtct_box, gtct_txt, part_box).set_opacity(0)
            return VGroup(strand, gtct_box, gtct_txt, part_box, coils), gtct_box, part_box, coils, sites, coil_dxs

        lx, rx = -3.3, 3.3
        y_dna = -0.95
        off_l, off_r = -0.60, 0.40
        dna_l, gtct_l, pbox_l, coils_l, sites_l, dxs_l = build_panel_dna(lx, y_dna, off_l)
        dna_r, gtct_r, pbox_r, coils_r, sites_r, dxs_r = build_panel_dna(rx, y_dna, off_r)

        smad_l = make_smad_trimer([lx + off_l + 0.44, 0.85, 0], scale=0.92, phosphorylated=True, show_prong=True)
        smad_r = make_smad_trimer([rx + off_r + 0.44, 0.85, 0], scale=0.92, phosphorylated=True, show_prong=True)
        bob(smad_l, amp=0.06, speed=2.6, seed=0)
        bob(smad_r, amp=0.06, speed=2.6, seed=1.5)

        self.play(FadeIn(dna_l), FadeIn(dna_r), FadeIn(smad_l), FadeIn(smad_r), run_time=0.8)

        self.at("partner transcription factors")
        part_l = make_partner("epithelial", [lx - 1.75, 0.72, 0], scale=0.88)
        part_r = make_partner("fibroblast", [rx - 1.75, 0.72, 0], scale=0.88)
        part_l_lbl = T("Epithelial partner", 26, TERRACOTTA).move_to([lx - 1.25, 1.98, 0])
        part_r_lbl = T("Fibroblast partner", 26, SKY_BLUE).move_to([rx - 1.25, 1.98, 0])
        self.play(FadeIn(part_l), FadeIn(part_r), FadeIn(part_l_lbl), FadeIn(part_r_lbl), run_time=1.0)

        self.at("chromatin open")
        open_l = T("Open chromatin", 26, TERRACOTTA).move_to([lx + off_l, -1.95, 0])
        open_r = T("Open chromatin", 26, SKY_BLUE).move_to([rx + off_r, -1.95, 0])
        # Shift coils outward from each cell type's specific binding window
        target_dxs_l = [-2.40, -2.18, -2.02, 0.48, 0.82, 1.18, 1.56, 1.94, 2.32]
        target_dxs_r = [-2.32, -1.96, -1.60, -1.24, -0.96, 1.48, 1.74, 2.02, 2.32]
        self.play(
            *[c.animate.move_to([lx + dx, y_dna, 0]).set_opacity(0.38) for c, dx in zip(coils_l, target_dxs_l)],
            *[c.animate.move_to([rx + dx, y_dna, 0]).set_opacity(0.38) for c, dx in zip(coils_r, target_dxs_r)],
            sites_l.animate.set_opacity(1.0),
            sites_r.animate.set_opacity(1.0),
            FadeIn(open_l), FadeIn(open_r),
            run_time=1.0,
        )

        self.at("locks onto")
        smad_l.clear_updaters()
        smad_r.clear_updaters()
        self.play(
            part_l.animate.move_to(pbox_l.get_center() + UP * 0.44),
            part_r.animate.move_to(pbox_r.get_center() + UP * 0.44),
            run_time=0.9,
        )
        self.at("beside a partner")
        self.play(
            smad_l.animate.move_to(gtct_l.get_center() + UP * 0.62),
            smad_r.animate.move_to(gtct_r.get_center() + UP * 0.62),
            run_time=0.9,
        )

        self.at("carries one message")
        msg = caption("Same Smad complex: 'TGF-β is here'", size=30, color=EMERALD)
        msg_l = T("TGF-β is here", 24, EMERALD).move_to([lx + off_l + 0.44, 0.65, 0])
        msg_r = T("TGF-β is here", 24, EMERALD).move_to([rx + off_r + 0.44, 0.65, 0])
        self.play(FadeIn(msg), FadeIn(msg_l), FadeIn(msg_r), run_time=0.9)

        self.at("partners decide")
        dec_cap = caption("Partners decide which genes turn on or off", size=30, color=GOLD)
        arr_l = Arrow([lx + 0.90, -0.45, 0], [lx + 2.35, -0.45, 0], color=TERRACOTTA, stroke_width=4, buff=0.1)
        arr_r = Arrow([rx + 1.65, -0.45, 0], [rx + 2.65, -0.45, 0], color=SKY_BLUE, stroke_width=4, buff=0.1)
        self.play(
            swap(msg, dec_cap, run_time=0.6),
            GrowArrow(arr_l), GrowArrow(arr_r),
            run_time=1.0,
        )
        self.finish()


class S04OutcomesCancer(SpokenScene):
    def construct(self):
        tp = TwoPanel("Epithelial nucleus", "Fibroblast nucleus", colors=(TERRACOTTA, SKY_BLUE), top=3.15, bottom=-2.65)
        tag = scope_tag("schematic")
        lx, rx = -3.3, 3.3
        y_dna = 1.15  # lower than heading so Smad + partner sit cleanly below heading

        dna_l = Line([lx - 2.5, y_dna, 0], [lx + 2.5, y_dna, 0], color=GOLD, stroke_width=4.5)
        dna_r = Line([rx - 2.5, y_dna, 0], [rx + 2.5, y_dna, 0], color=GOLD, stroke_width=4.5)
        part_l = make_partner("epithelial", [lx - 0.72, y_dna + 0.40, 0], scale=0.72)
        smad_l = make_smad_trimer([lx + 0.35, y_dna + 0.54, 0], scale=0.75, phosphorylated=True, show_prong=True)
        part_r = make_partner("fibroblast", [rx - 0.62, y_dna + 0.40, 0], scale=0.72)
        smad_r = make_smad_trimer([rx + 0.45, y_dna + 0.54, 0], scale=0.75, phosphorylated=True, show_prong=True)

        self.add(tp, tag, dna_l, dna_r, part_l, smad_l, part_r, smad_r)

        # Epithelial p15, p21 upward bars & Myc downward bar
        p_track = ValueTracker(0.0)
        p_bar = always_redraw(lambda: Rectangle(
            width=0.58, height=max(0.06, 0.90 * p_track.get_value()),
            color=GREEN, fill_color=GREEN, fill_opacity=0.68, stroke_width=2.5
        ).move_to([lx - 1.55, -0.25 + 0.45 * p_track.get_value(), 0]))
        p_lbl = T("p15, p21 ↑", 28, GREEN).move_to([lx - 1.55, -0.62, 0])

        myc_track = ValueTracker(1.0)
        myc_bar = always_redraw(lambda: Rectangle(
            width=0.58, height=max(0.08, 0.85 * myc_track.get_value()),
            color=RED, fill_color=RED, fill_opacity=0.58, stroke_width=2.5
        ).move_to([lx + 1.35, -0.25 + 0.425 * myc_track.get_value(), 0]))
        myc_lbl = T("Myc ↓", 28, RED).move_to([lx + 1.35, -0.62, 0])

        self.at("p15 and p21")
        # Transcriptional activation pulses travel along epithelial & fibroblast DNA toward targets
        act_l = Arrow([lx + 0.6, y_dna - 0.12, 0], [lx + 2.2, y_dna - 0.12, 0], color=GREEN, stroke_width=4.5, buff=0.05)
        self.add(p_bar)
        self.play(GrowArrow(act_l), FadeIn(p_lbl), p_track.animate.set_value(1.0), run_time=1.0)

        self.at("stop division")
        arrest_bar = boxed_label("Stop dividing", TEAL, size=28, pad=0.12).move_to([lx, -1.28, 0])
        self.play(FadeIn(arrest_bar), run_time=0.7)

        self.at("shut off MYC")
        self.add(myc_bar)
        self.play(FadeIn(myc_lbl), myc_track.animate.set_value(0.12), run_time=0.9)

        # Fibroblast collagen genes
        self.at("in fibroblasts")
        act_r = Arrow([rx + 0.7, y_dna - 0.12, 0], [rx + 2.2, y_dna - 0.12, 0], color=SKY_BLUE, stroke_width=4.5, buff=0.05)
        col_track = ValueTracker(0.0)
        col_bar = always_redraw(lambda: Rectangle(
            width=0.65, height=max(0.06, 1.05 * col_track.get_value()),
            color=SKY_BLUE, fill_color=SKY_BLUE, fill_opacity=0.60, stroke_width=2.5
        ).move_to([rx - 1.4, -0.35 + 0.525 * col_track.get_value(), 0]))
        col_lbl = T("Collagen ↑", 28, SKY_BLUE).move_to([rx - 1.4, -0.75, 0])
        self.play(GrowArrow(act_r), run_time=0.6)

        self.at("collagen genes")
        fibres = VGroup(
            Line([rx + 0.1, -0.30, 0], [rx + 2.3, 0.45, 0], color=SKY_BLUE, stroke_width=4.5),
            Line([rx + 0.1, 0.45, 0], [rx + 2.3, -0.30, 0], color=SKY_BLUE, stroke_width=4.5),
            Line([rx + 0.2, 0.08, 0], [rx + 2.2, 0.08, 0], color=TEXT, stroke_width=3.2, stroke_opacity=0.65),
        )
        mat_lbl = T("Matrix / repair", 28, SKY_BLUE).move_to([rx + 0.9, -1.35, 0])
        self.add(col_bar)
        self.play(FadeIn(col_lbl), col_track.animate.set_value(1.0), Create(fibres), FadeIn(mat_lbl), run_time=1.3)

        # Early in cancer: restrained (show arrested tumour cell held behind the stop bar)
        self.at("early in cancer")
        early_badge = boxed_label("Early tumour: restrained", GREEN, size=26, pad=0.12).move_to([lx, -2.08, 0])
        self.play(FadeIn(early_badge), run_time=0.8)

        self.at("obey the stop")
        self.play(Indicate(arrest_bar, color=GREEN, scale_factor=1.06), run_time=1.0)
        self.play(Indicate(early_badge, color=GREEN, scale_factor=1.04), run_time=1.0)

        # Late tumour: arrest bar breaks, cell moves, immune quieting inside Late tumour panel
        self.at("escape arrest")
        p_bar.clear_updaters()
        myc_bar.clear_updaters()
        late_head = T("Late tumour", 32, RED).move_to(tp.left_head.get_center())
        half_l = Line([lx - 1.15, -1.28, 0], [lx - 0.15, -1.28, 0], color=RED, stroke_width=6)
        half_r = Line([lx + 0.15, -1.28, 0], [lx + 1.15, -1.28, 0], color=RED, stroke_width=6)
        self.play(
            swap(tp.left_head, late_head, run_time=0.5),
            tp.left_frame.animate.set_stroke(color=RED),
            FadeOut(arrest_bar), FadeOut(early_badge),
            FadeOut(p_bar), FadeOut(p_lbl), FadeOut(myc_bar), FadeOut(myc_lbl), FadeOut(act_l),
            FadeIn(half_l), FadeIn(half_r),
            run_time=0.8,
        )
        self.play(
            half_l.animate.shift(LEFT * 0.45 + DOWN * 0.15).rotate(0.25),
            half_r.animate.shift(RIGHT * 0.45 + DOWN * 0.15).rotate(-0.25),
            run_time=0.5,
        )
        self.play(FadeOut(half_l), FadeOut(half_r), run_time=0.3)

        self.at("push them to move")
        # Route motility arrow cleanly down the centre between p15/p21 and Myc
        side_arr = Arrow([lx + 0.05, 0.90, 0], [lx - 0.35, -0.95, 0], color=RED, stroke_width=4, buff=0.1)
        mot_lbl = T("Motility", 28, RED).move_to([lx - 1.55, -1.35, 0])
        tum_cell = RoundedRectangle(corner_radius=0.20, width=0.88, height=0.44, color=RED,
                                    fill_color=RED, fill_opacity=0.34, stroke_width=3).move_to([lx - 2.0, -2.05, 0])
        self.play(GrowArrow(side_arr), FadeIn(mot_lbl), FadeIn(tum_cell), run_time=0.6)
        self.play(tum_cell.animate.shift(RIGHT * 1.45), run_time=1.0, rate_func=linear)

        self.at("nearby immune cells")
        imm_lbl = T("Immune quieting", 26, TEXT).move_to([lx + 1.35, -1.35, 0])
        imm_dot = Circle(radius=0.22, color=TEXT, fill_color=TEXT, fill_opacity=0.40, stroke_width=3).move_to([lx + 1.35, -2.05, 0])
        self.play(FadeIn(imm_lbl), FadeIn(imm_dot), run_time=0.6)
        self.play(imm_dot.animate.set_fill(opacity=0.12).set_stroke(opacity=0.55), run_time=0.7)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = make_membrane_world(active=False, with_dimers=True, caged=False)
        for i, d in enumerate(world.dimers):
            bob(d, amp=0.08, speed=2.2, seed=i * 1.1)

        ecm_lbl = T("Extracellular matrix", 28, TEXT).move_to([-4.2, 3.25, 0])
        t2_lbl = T("Type II", 28, CYAN).move_to([-2.15, 0.20, 0])
        t1_lbl = T("Type I", 28, INDIGO).move_to([2.15, 0.20, 0])
        tag = scope_tag("schematic").move_to([5.5, 3.30, 0])

        smad_rest = make_smad_trimer([0.0, -0.95, 0], scale=0.85, phosphorylated=False, show_prong=False, with_smad4=False)
        sig_lbl = T("No Smad signal", 28, RED).move_to([0.0, -2.22, 0])

        self.play(
            FadeIn(world.ecm), FadeIn(world.mem), FadeIn(world.rec), FadeIn(world.nuc),
            FadeIn(ecm_lbl), FadeIn(t2_lbl), FadeIn(t1_lbl), FadeIn(tag),
            run_time=1.0,
        )

        self.at("matrix holds plenty")
        tgf_lbl = T("TGF-β dimers", 28, AMBER).move_to([0.0, 3.25, 0])
        self.play(FadeIn(world.dimers), FadeIn(tgf_lbl), run_time=1.0)

        self.at("nearby cells show")
        self.play(FadeIn(smad_rest), FadeIn(sig_lbl), run_time=0.9)

        self.at("away from its receptors")
        q = question_card("Plenty of TGF-β nearby, receptors silent. What keeps it away?", max_w=10.2)
        self.play(FadeIn(q.question), run_time=0.9)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Plenty of TGF-β nearby, receptors silent. What keeps it away?"
    SECONDS = 4.5

    def backdrop(self):
        world = make_membrane_world(active=False, with_dimers=True, caged=False)
        for i, d in enumerate(world.dimers):
            bob(d, amp=0.08, speed=2.2, seed=i * 1.1)
        ecm_lbl = T("Extracellular matrix", 28, TEXT).move_to([-4.2, 3.25, 0])
        tgf_lbl = T("TGF-β dimers", 28, AMBER).move_to([0.0, 3.25, 0])
        t2_lbl = T("Type II", 28, CYAN).move_to([-2.15, 0.20, 0])
        t1_lbl = T("Type I", 28, INDIGO).move_to([2.15, 0.20, 0])
        tag = scope_tag("schematic").move_to([5.5, 3.30, 0])
        smad_rest = make_smad_trimer([0.0, -0.95, 0], scale=0.85, phosphorylated=False, show_prong=False, with_smad4=False)
        sig_lbl = T("No Smad signal", 28, RED).move_to([0.0, -2.22, 0])
        return VGroup(world, ecm_lbl, tgf_lbl, t2_lbl, t1_lbl, tag, smad_rest, sig_lbl)


class S07Brake1Latent(SpokenScene):
    def construct(self):
        world = make_membrane_world(active=False, with_dimers=True, caged=False)
        ecm_lbl = T("Extracellular matrix", 26, TEXT).move_to([-4.65, 3.28, 0])
        t2_lbl = T("Type II", 28, CYAN).move_to([-2.15, 0.20, 0])
        t1_lbl = T("Type I", 28, INDIGO).move_to([2.15, 0.20, 0])
        tag = scope_tag("schematic")
        q = question_card("Plenty of TGF-β nearby, receptors silent. What keeps it away?", max_w=10.2)
        self.add(world, ecm_lbl, t2_lbl, t1_lbl, tag, q.question)

        # Keep dimers gently bobbing in ECM fluid so there is no frozen stretch before/after caging
        for i, d in enumerate(world.dimers):
            bob(d, amp=0.07, speed=2.0, seed=i * 1.1)
        self.play(FadeOut(q.question), run_time=0.7)

        self.at("three layered")
        b1_head = boxed_label("Brake 1: Latent wrapper", SLATE, size=26, pad=0.12).move_to([4.45, 3.28, 0])
        self.play(FadeIn(b1_head), run_time=0.7)

        self.at("a wrapper piece")
        cages = VGroup(*[make_latent_cage(d.get_center(), open_frac=0.0) for d in world.dimers])
        cut_caps = VGroup(*[
            VGroup(
                Arc(radius=0.56, start_angle=-0.16, angle=0.32, arc_center=d.get_center(), color=SLATE, stroke_width=6.5),
                Arc(radius=0.56, start_angle=PI - 0.16, angle=0.32, arc_center=d.get_center(), color=SLATE, stroke_width=6.5),
            )
            for d in world.dimers
        ])
        # Sync cage and cap bobbing identically to its dimer
        for i, (d, c, cap) in enumerate(zip(world.dimers, cages, cut_caps)):
            d.clear_updaters()
            bob(d, amp=0.06, speed=1.8, seed=i * 1.1)
            bob(c, amp=0.06, speed=1.8, seed=i * 1.1)
            bob(cap, amp=0.06, speed=1.8, seed=i * 1.1)
        self.play(FadeIn(cages), FadeIn(cut_caps), run_time=0.85)

        self.at("cut free")
        for cap in cut_caps:
            cap.clear_updaters()
        self.play(FadeOut(cut_caps, scale=1.18), run_time=0.6)

        self.at("stays clamped")
        latent_lbl = boxed_label("Cut, but still bound (latent)", SLATE, size=24, pad=0.12).move_to([-0.25, 3.28, 0])
        latent_arr = Arrow([-1.90, 3.04, 0], [-3.15, 2.62, 0], color=SLATE, stroke_width=3.2, buff=0.04)
        self.play(FadeIn(latent_lbl), GrowArrow(latent_arr), run_time=0.7)

        self.at("tethered to the")
        tether_specs = [
            (np.array([-0.485, 0.280, 0.0]), np.array([-4.55, 2.52, 0.0])),
            (np.array([0.508, 0.236, 0.0]), np.array([-0.45, 2.245, 0.0])),
            (np.array([0.541, 0.145, 0.0]), np.array([2.25, 2.28, 0.0])),
            (np.array([0.485, 0.280, 0.0]), np.array([4.55, 2.456, 0.0])),
        ]
        tethers = VGroup()
        for c, (rim_off, anc) in zip(cages, tether_specs):
            t_ln = Line(c.get_center() + rim_off, anc, color=SLATE, stroke_width=3.2)
            t_ln.add_updater(lambda m, c=c, off=rim_off, anc=anc: m.put_start_and_end_on(c.get_center() + off, anc))
            tethers.add(t_ln)
        self.play(FadeIn(tethers), run_time=0.9)

        self.at("freed locally")
        integ = VGroup(
            Line([-2.5, 0.60, 0], [-2.5, 1.35, 0], color=TEAL, stroke_width=6),
            Line([-2.5, 1.35, 0], [-1.80, 1.85, 0], color=TEAL, stroke_width=4.5),
        )
        integ_lbl = T("Integrin", 28, TEAL).move_to([-3.6, 1.12, 0])
        self.play(FadeIn(integ), FadeIn(integ_lbl), run_time=0.6)

        self.at("integrin pulls")
        world.dimers[1].clear_updaters()
        cages[1].clear_updaters()
        pull_vec = DOWN * 0.12 + LEFT * 0.04
        open_cage_l = make_latent_cage(world.dimers[1].get_center() + pull_vec, open_frac=1.0)
        self.play(
            integ.animate.shift(DOWN * 0.14),
            world.dimers[1].animate.shift(pull_vec),
            Transform(cages[1], open_cage_l),
            run_time=0.65,
        )

        self.at("protease cuts")
        scissors = make_scissors([2.45, 2.22, 0], color=TEXT)
        prot_lbl = T("Protease", 28, TEXT).move_to([2.25, 1.40, 0])
        world.dimers[2].clear_updaters()
        cages[2].clear_updaters()
        tethers[2].clear_updaters()
        open_cage_r = make_latent_cage(world.dimers[2].get_center(), open_frac=1.0)
        self.play(FadeIn(scissors), FadeIn(prot_lbl), run_time=0.25)
        self.play(
            scissors.animate.move_to([1.95, 2.22, 0]),
            Transform(cages[2], open_cage_r),
            FadeOut(tethers[2]),
            run_time=0.50,
        )
        freed = world.dimers[2]
        freed.clear_updaters()
        rec_on = make_receptor_pair(cx=0.0, y_mem=0.72, active=True, gap=1.48)
        self.play(
            freed.animate.move_to([0.0, 1.28, 0]),
            Transform(world.rec, rec_on),
            t2_lbl.animate.move_to([-1.75, 0.15, 0]),
            t1_lbl.animate.move_to([1.75, 0.15, 0]),
            run_time=0.75,
        )
        self.finish()


class S08Brake2Smad7(SpokenScene):
    def construct(self):
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(1.1 * dt))
        self.add(phase)

        world = make_membrane_world(active=True, with_dimers=False)
        lig = make_ligand([0.0, 1.28, 0], scale=0.84)
        t2_lbl = T("Type II", 28, CYAN).move_to([-1.75, 0.24, 0])
        t1_lbl = T("Type I", 28, INDIGO).move_to([1.82, 0.24, 0])
        b2_head = boxed_label("Brake 2: Smad7 feedback", CRIMSON, size=28, pad=0.14).move_to([-3.8, 3.28, 0])
        tag = scope_tag("schematic")

        # Continuous waving DNA inside nucleus
        dna = always_redraw(lambda: make_wave_dna(x0=-5.2, x1=2.0, y=-2.80, amp=0.10, phase=phase.get_value(), n_rungs=14, color=GOLD))
        gene_lbl = T("Smad7 gene", 28, CRIMSON).move_to([-0.8, -3.32, 0])

        self.add(world, lig, t2_lbl, t1_lbl, b2_head, tag, dna)

        smad_act = make_smad_trimer([0.0, -0.88, 0], scale=0.85, phosphorylated=True, show_prong=False)
        self.play(FadeIn(smad_act), run_time=0.6)

        self.at("makes its own inhibitor")
        self.play(smad_act.animate.move_to([-2.4, -2.30, 0]), run_time=0.85)

        self.at("switch on the gene")
        self.play(FadeIn(gene_lbl), run_time=0.7)
        s7_1 = boxed_label("Smad7", CRIMSON, size=26, pad=0.12).move_to([-0.3, -2.25, 0])
        s7_2 = boxed_label("Smad7", CRIMSON, size=26, pad=0.12).move_to([0.8, -1.30, 0])
        self.play(FadeIn(s7_1, shift=UP * 0.25), run_time=0.65)
        self.play(FadeIn(s7_2, shift=UP * 0.25), run_time=0.65)

        self.at("cap the active")
        self.play(s7_2.animate.move_to([0.75, -0.68, 0]), run_time=1.1)

        self.at("blocking incoming")
        r_smad = RoundedRectangle(corner_radius=0.14, width=0.72, height=0.46, color=EMERALD,
                                  fill_color=EMERALD, fill_opacity=0.38, stroke_width=3.2).move_to([3.8, -0.75, 0])
        r_lbl = T("R-Smad", 26, EMERALD).next_to(r_smad, DOWN, buff=0.16)
        self.play(FadeIn(r_smad), FadeIn(r_lbl), run_time=0.5)
        self.play(
            r_smad.animate.move_to([1.95, -0.68, 0]),
            r_lbl.animate.move_to([1.95, -1.16, 0]),
            run_time=0.65,
        )
        self.play(
            r_smad.animate.move_to([4.15, -0.72, 0]),
            r_lbl.animate.move_to([4.15, -1.20, 0]),
            run_time=0.75,
        )

        fb_arr = CurvedArrow([0.55, -2.25, 0], [0.95, -1.10, 0], angle=0.55, color=CRIMSON, stroke_width=3.2)
        self.play(Create(fb_arr), run_time=0.65)

        self.at("plays a similar")
        bmp_card = boxed_label("Smad6:\nprefers BMP branch", CRIMSON, size=26, pad=0.16).move_to([4.05, 3.16, 0])
        self.play(FadeIn(bmp_card), run_time=0.7)

        self.at("the BMP branch")
        self.play(Indicate(bmp_card, color=CRIMSON, scale_factor=1.05), run_time=0.7)
        self.finish()


class S09Brake3Smurfs(SpokenScene):
    def construct(self):
        # Slightly lower nuclear rim so Degradation ring & disease badges never touch it
        world = make_membrane_world(active=True, with_dimers=False, y_nuc=-2.00)
        lig = make_ligand([0.0, 1.28, 0], scale=0.84)
        t2_lbl = T("Type II", 28, CYAN).move_to([-1.85, 1.22, 0])
        t1_lbl = T("Type I", 28, INDIGO).move_to([1.85, 1.22, 0])
        cap_s7 = boxed_label("Smad7", CRIMSON, size=26, pad=0.12).move_to([0.75, -0.58, 0])
        b3_head = boxed_label("Brake 3: Ubiquitin destruction", BURNT_AMBER, size=28, pad=0.14).move_to([-3.55, 3.28, 0])
        tag = scope_tag("schematic")

        # Signal meter placed cleanly in open left cytosol (below membrane, above nuclear rim)
        sig_val = ValueTracker(1.0)
        sig_bg = Rectangle(width=2.6, height=0.34, color=GREY, stroke_width=2.5).move_to([-4.45, -0.45, 0])
        sig_fill = always_redraw(lambda: Rectangle(
            width=max(0.06, 2.52 * sig_val.get_value()), height=0.26,
            color=EMERALD if sig_val.get_value() > 0.35 else SLATE,
            fill_color=EMERALD if sig_val.get_value() > 0.35 else SLATE,
            fill_opacity=0.88, stroke_width=0
        ).align_to(sig_bg.get_left() + RIGHT * 0.04, LEFT).set_y(-0.45))
        sig_lbl = T("Receptor signal", 26, TEXT).next_to(sig_bg, UP, buff=0.15)

        self.add(world, lig, t2_lbl, t1_lbl, cap_s7, b3_head, tag, sig_bg, sig_fill, sig_lbl)

        self.at("recruits ubiquitin ligases")
        smurf = boxed_label("Smurf ligase", BURNT_AMBER, size=26, pad=0.12).move_to([4.5, -0.68, 0])
        self.play(FadeIn(smurf), run_time=0.8)
        self.play(smurf.animate.move_to([2.95, -0.68, 0]), run_time=2.6)

        self.at("tag the receptor")
        ub_beads = VGroup(
            Circle(radius=0.13, color=GOLD, fill_color=GOLD, fill_opacity=0.95, stroke_width=2).move_to([1.22, -0.05, 0]),
            Circle(radius=0.13, color=GOLD, fill_color=GOLD, fill_opacity=0.95, stroke_width=2).move_to([1.52, -0.05, 0]),
            Circle(radius=0.13, color=GOLD, fill_color=GOLD, fill_opacity=0.95, stroke_width=2).move_to([1.82, -0.05, 0]),
        )
        ub_lbl = T("Ub", 26, GOLD, weight=BOLD).move_to([2.42, -0.05, 0])
        smad_target = make_smad_trimer([-2.0, -1.05, 0], scale=0.72, phosphorylated=True, show_prong=False)
        ub_smad = Circle(radius=0.13, color=GOLD, fill_color=GOLD, fill_opacity=0.95, stroke_width=2).move_to([-0.92, -1.05, 0])
        self.play(FadeIn(ub_beads), FadeIn(ub_lbl), FadeIn(smad_target), FadeIn(ub_smad), run_time=0.9)

        self.at("with ubiquitin for destruction")
        deg_ring = DashedVMobject(Circle(radius=0.48, color=BURNT_AMBER, stroke_width=4), num_dashes=16).move_to([0.9, -1.60, 0])
        deg_lbl = T("Degradation", 26, BURNT_AMBER).move_to([2.75, -1.60, 0])
        self.play(FadeIn(deg_ring), FadeIn(deg_lbl), FadeOut(cap_s7), run_time=0.6)
        self.play(
            Rotate(deg_ring, PI, about_point=deg_ring.get_center()),
            world.rec.t1.animate.move_to(deg_ring.get_center()).scale(0.55).set_opacity(0.18),
            world.rec.p_badge.animate.set_opacity(0.15),
            FadeOut(t1_lbl),
            FadeOut(ub_lbl),
            ub_beads.animate.move_to(deg_ring.get_center() + UP * 0.2).set_opacity(0.20),
            smad_target.animate.shift(DOWN * 0.35).set_opacity(0.18),
            ub_smad.animate.shift(DOWN * 0.35).set_opacity(0.18),
            sig_val.animate.set_value(0.05),
            run_time=1.7,
        )

        self.at("local and brief")
        quiet_lbl = boxed_label("Local and brief", TEAL, size=28, pad=0.14).move_to([-4.45, -1.25, 0])
        self.play(
            FadeOut(deg_ring), FadeOut(deg_lbl), FadeOut(smurf),
            FadeOut(smad_target), FadeOut(ub_smad), FadeOut(ub_beads), FadeOut(world.rec.t1), FadeOut(world.rec.p_badge),
            FadeIn(quiet_lbl),
            run_time=0.8,
        )

        self.at("breaking a key part")
        dis_l = boxed_label("Smad4 lost", VIOLET, size=26, pad=0.14).move_to([-4.2, -2.85, 0])
        self.play(FadeIn(dis_l), run_time=0.7)

        self.at("safety catch")
        dis_r = boxed_label("GS safety catch loosened", GOLD, size=26, pad=0.14).move_to([0.0, -2.85, 0])
        self.play(FadeIn(dis_r), run_time=0.7)

        self.at("human disease")
        dis_out = boxed_label("Human disease", RED, size=28, pad=0.14).move_to([4.35, -2.85, 0])
        arr_d = Arrow(dis_r.get_right() + RIGHT * 0.1, dis_out.get_left() + LEFT * 0.1, color=RED, stroke_width=4, buff=0.05)
        self.play(GrowArrow(arr_d), FadeIn(dis_out), run_time=0.8)
        self.finish()


class S10ReturnRule(SpokenScene):
    def construct(self):
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(1.0 * dt))
        self.add(phase)

        ecm = make_ecm_fibres(y_min=1.55, y_max=2.75)
        mem = make_membrane_band(y=0.72)
        rec = make_receptor_pair(cx=0.0, y_mem=0.72, active=False, gap=1.35)
        nuc = make_nuclear_rim(y=-0.78)
        tag = scope_tag("schematic")

        # Caged latent dimers placed clear of left/right badges, tethered to ECM fibres
        caged_spots = [(-2.6, 2.15, 0), (2.8, 2.15, 0)]
        caged_anchors = [
            (np.array([-0.485, 0.280, 0.0]), np.array([-3.50, 2.469, 0.0])),
            (np.array([0.485, 0.280, 0.0]), np.array([3.70, 2.409, 0.0])),
        ]
        caged_grp = VGroup()
        for pos, (rim_off, anc) in zip(caged_spots, caged_anchors):
            d = make_ligand(pos, scale=0.78)
            c = make_latent_cage(pos, open_frac=0.0)
            t = Line(np.array(pos) + rim_off, anc, color=SLATE, stroke_width=3.2)
            bob(d, amp=0.03, speed=1.5, seed=pos[0])
            caged_grp.add(d, c, t)

        s7 = boxed_label("Smad7", CRIMSON, size=26, pad=0.12).move_to([1.95, 0.05, 0])
        smurf = boxed_label("Smurf", BURNT_AMBER, size=26, pad=0.12).move_to([3.75, 0.05, 0])

        dna_l = always_redraw(lambda: make_wave_dna(x0=-5.8, x1=-0.5, y=-2.45, amp=0.07, phase=phase.get_value(), n_rungs=10))
        dna_r = always_redraw(lambda: make_wave_dna(x0=0.5, x1=5.8, y=-2.45, amp=0.07, phase=phase.get_value() + 1.0, n_rungs=10))

        part_l = make_partner("epithelial", [-4.05, -1.78, 0], scale=0.72)
        smad_l = make_smad_trimer([-2.95, -1.70, 0], scale=0.74, phosphorylated=True, show_prong=True)
        part_r = make_partner("fibroblast", [2.55, -1.78, 0], scale=0.72)
        smad_r = make_smad_trimer([3.65, -1.70, 0], scale=0.74, phosphorylated=True, show_prong=True)

        self.play(FadeIn(ecm), FadeIn(mem), FadeIn(rec), FadeIn(nuc), FadeIn(tag), run_time=0.8)

        self.at("both context and control")
        ctx_badge = boxed_label("Context", TERRACOTTA, size=28, pad=0.14).move_to([-4.6, -0.25, 0])
        ctl_badge = boxed_label("Control", CRIMSON, size=28, pad=0.14).move_to([-4.6, 3.25, 0])
        self.play(FadeIn(ctx_badge), FadeIn(ctl_badge), run_time=0.8)

        self.at("inside the nucleus")
        self.play(FadeIn(dna_l), FadeIn(dna_r), run_time=0.8)

        self.at("partner factors")
        self.play(FadeIn(part_l), FadeIn(smad_l), FadeIn(part_r), FadeIn(smad_r), run_time=0.9)

        self.at("decide which genes")
        epi_out = T("Epithelial targets", 26, TERRACOTTA).move_to([-3.3, -3.15, 0])
        fib_out = T("Fibroblast targets", 26, SKY_BLUE).move_to([3.1, -3.15, 0])
        self.play(FadeIn(epi_out), FadeIn(fib_out), run_time=0.8)

        self.at("outside and at the membrane")
        self.play(FadeIn(caged_grp), FadeIn(s7), FadeIn(smurf), run_time=0.9)

        self.at("where and how long")
        b_lbl = T("Latent wrapper + Smad7 + Smurf", 28, GOLD).move_to([1.2, 3.28, 0])
        self.play(FadeIn(b_lbl), run_time=0.8)
        self.finish()


class S11End(EndCard):
    LINE = "Partner factors choose Smad targets, and layered brakes restrain the signal."
