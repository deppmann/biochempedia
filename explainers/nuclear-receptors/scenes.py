"""
One Protein, Two Grips: How Nuclear Receptors Wait
Lesson: Nuclear Receptors: Receptors That Are Transcription Factors

COLOUR MAP (one colour per concept across the whole film):
- TEAL   (#3FB8C0): Nuclear receptor protein (receptor bar, ligand pocket, DNA-binding domain, hinge)
- YELLOW (#F5D547): Ligand / hormone / lipid (cortisol, estradiol, thyroid hormone, fatty/bile acids)
- ORANGE (#F08A4B): AF-1 switching surface
- GOLD   (#D4A843): Zinc ions in the DNA-binding domain, predict question / highlight
- CREAM  (#EDE4CE): DNA double strand, response elements, histone spools
- INDIGO (#7C8CF8): RXR partner receptor
- GREY   (#8B93A1): Hsp90 chaperones, inactive surface receptor, structural membrane/baseline lines
- RED    (#FC6255): Co-repressor, active off state, blocked RNA polymerase
- GREEN  (#83C167): Co-activator, acetyl tags, newly copied RNA strand, active ON state
- SLATE  (#6E829E): Plasma membrane & nuclear envelope boundaries
- TEXT   (#E8EAF0): Crisp labels and narrative tags

CARRIED WORLD:
A cross-section of a target cell (extracellular space on the left, plasma membrane, cytoplasm,
nuclear envelope with nuclear pore, and pale cream DNA inside the nucleus on the right) that zooms
into the modular receptor on DNA, splits into two waiting lanes (Route 1 off DNA with Hsp90; Route 2
on DNA with RXR), and zooms into Route 2 on DNA with histones and a schematic transcription meter.

SCENE MOTION SUMMARY (computed / state-driven per spoken scene):
- s01_hook: Surface receptor knock extends a cytoplasmic relay line before fading; hydrophobic steroid spheres diffuse along seeded random-walk-biased paths across the phospholipid bilayer into the cytoplasm.
- s02_one_protein: Steroid enters pocket; single receptor enters nucleus and docks onto DNA; RNA strand polymerizes continuously along computed helical curve via ValueTracker.
- s03_domains: Gene counter increments 1 -> 48 as receptor expands into 4 domains; ligand glides along computed path into pocket; 6 base-pair ticks light sequentially as zinc block reads DNA.
- s04_pairs: Second modular receptor glides in to dimerize on DNA; two 6-bp response-element half-sites highlight; computed signal pulse travels from ligand through DNA grip to sprout RNA.
- s05_wait_chaperone: Stage splits into two lanes; Hsp90 clamps glide onto receptor, flex pocket open, and tether DNA-binding teeth leftward away from the nuclear pore barrier.
- s06_chaperone_release: Cortisol enters pocket; Hsp90 clamps loosen; complex translocates through nuclear pore, sheds clamps, and dimerizes on DNA; nuclear estrogen receptor holds clamps inside nucleus.
- s07_wait_dna_predict: Route 1 collapses and Route 2 expands; RXR glides to pair with empty thyroid receptor on DNA; schematic transcription meter sweeps needle between Baseline and Quieter.
- s09_reveal_active_off: Meter drops to Active off; co-repressor docks onto receptor; acetyl tags peel off histones one by one; histones slide tighter by computed spacing while RNA polymerase bounces off blocked chromatin.
- s10_swap_and_close: Thyroid hormone binds; co-repressor leaves and co-activator docks; acetyl tags reattach; histones slide apart, RNA polymerase transcribes elongating RNA, meter rises to ON, lipids approach receptor, and receptor bridges ligand and DNA.
"""

from bp_parts import *

# Extended house palette (all high contrast on BG #0f1117)
ORANGE = "#F08A4B"
CREAM = "#EDE4CE"
INDIGO = "#7C8CF8"
SLATE = "#6E829E"
LABEL_MUTED = "#B8C2D1"


# ------------------------------------------------------------------ shared world builders
def build_dna_strand(x0=-5.2, x1=5.2, y=0.0, amp=0.18, freq=2.4, color=CREAM, stroke=4.0):
    """Build a computed double-helix ribbon between x0 and x1 centered at y."""
    xs = np.linspace(x0, x1, 140)
    pts1 = [np.array([x, y + amp * np.sin(freq * (x - x0)), 0.0]) for x in xs]
    pts2 = [np.array([x, y - amp * np.sin(freq * (x - x0)), 0.0]) for x in xs]
    s1 = VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts1)
    s2 = VMobject(stroke_color=color, stroke_width=stroke * 0.85, stroke_opacity=0.85).set_points_as_corners(pts2)
    rungs = VGroup()
    n_rungs = max(6, int((x1 - x0) * 3.2))
    for xr in np.linspace(x0 + 0.15, x1 - 0.15, n_rungs):
        y1 = y + amp * np.sin(freq * (xr - x0))
        y2 = y - amp * np.sin(freq * (xr - x0))
        if abs(y1 - y2) > 0.05:
            rungs.add(Line([xr, y1, 0], [xr, y2, 0], color=color, stroke_width=2.0, stroke_opacity=0.6))
    return VGroup(rungs, s1, s2)


def build_bilayer(x=-3.2, y0=-2.3, y1=2.45, color=SLATE):
    """Schematic phospholipid bilayer strip at x (no molecular structures)."""
    g = VGroup()
    ys = np.linspace(y0, y1, 18)
    for y in ys:
        g.add(Dot([x - 0.18, y, 0], radius=0.075, color=color))
        g.add(Dot([x + 0.18, y, 0], radius=0.075, color=color))
        g.add(Line([x - 0.10, y, 0], [x - 0.02, y, 0], color=color, stroke_width=2.0))
        g.add(Line([x + 0.10, y, 0], [x + 0.02, y, 0], color=color, stroke_width=2.0))
    return g


def build_nuclear_envelope(x=1.4, y0=-2.3, y1=2.45, pore_y=0.0, pore_h=1.1, color=SLATE):
    """Dashed double-line nuclear envelope divider at x with a central nuclear pore gap."""
    half = pore_h / 2
    g = VGroup()
    if pore_y - half > y0 + 0.1:
        g.add(DashedLine([x, y0, 0], [x, pore_y - half, 0], color=color, stroke_width=4.5, dash_length=0.18))
        g.add(DashedLine([x + 0.12, y0, 0], [x + 0.12, pore_y - half, 0], color=color, stroke_width=3.0, dash_length=0.18))
    if y1 > pore_y + half + 0.1:
        g.add(DashedLine([x, pore_y + half, 0], [x, y1, 0], color=color, stroke_width=4.5, dash_length=0.18))
        g.add(DashedLine([x + 0.12, pore_y + half, 0], [x + 0.12, y1, 0], color=color, stroke_width=3.0, dash_length=0.18))
    for py in (pore_y - half, pore_y + half):
        g.add(RoundedRectangle(corner_radius=0.05, width=0.30, height=0.12, color=color, fill_color=color, fill_opacity=0.65)
              .move_to([x + 0.06, py, 0]))
    return g


def build_compact_receptor(center=ORIGIN, scale=1.0, color=TEAL, pocket_open=0.0, flip_x=False):
    """A single receptor protein with a right-side ligand pocket cup and lower DNA-gripping teeth."""
    body = RoundedRectangle(corner_radius=0.26, width=3.5, height=1.28, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.30)
    pocket_ring = Arc(radius=0.44, start_angle=PI * (0.28 + 0.12 * (1 - pocket_open)),
                      angle=PI * (1.44 - 0.24 * (1 - pocket_open)),
                      arc_center=[1.05, 0.0, 0], stroke_color=color, stroke_width=5.5)
    tooth1 = RoundedRectangle(corner_radius=0.08, width=0.36, height=0.50, stroke_color=color, stroke_width=3.5,
                              fill_color=color, fill_opacity=0.36).move_to([-0.85, -0.84, 0])
    tooth2 = RoundedRectangle(corner_radius=0.08, width=0.36, height=0.50, stroke_color=color, stroke_width=3.5,
                              fill_color=color, fill_opacity=0.36).move_to([-0.22, -0.84, 0])
    af1 = RoundedRectangle(corner_radius=0.18, width=0.76, height=1.04, stroke_color=ORANGE, stroke_width=3.5,
                           fill_color=ORANGE, fill_opacity=0.30).move_to([-1.32, 0.0, 0])
    g = VGroup(body, af1, pocket_ring, tooth1, tooth2)
    if flip_x:
        g.scale([-1, 1, 1])
    g.scale(scale).move_to(center)
    g.dna_grip = VGroup(tooth1, tooth2)
    g.af1 = af1
    g.body = body
    return g


def build_modular_receptor(center=ORIGIN, scale=1.0, mirror=False, color=TEAL):
    """4-domain modular receptor: AF-1 | DNA-binding (2 zinc dots) | Hinge | Ligand pocket + AF-2."""
    af1 = RoundedRectangle(corner_radius=0.20, width=2.2, height=1.70, stroke_color=ORANGE, stroke_width=4,
                           fill_color=ORANGE, fill_opacity=0.30).move_to([-4.2, 0.0, 0])
    dbd = RoundedRectangle(corner_radius=0.18, width=2.3, height=1.70, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.30).move_to([-1.65, 0.0, 0])
    zn1 = Dot([-2.05, 0.12, 0], radius=0.16, color=GOLD)
    zn2 = Dot([-1.25, 0.12, 0], radius=0.16, color=GOLD)
    tooth_l = RoundedRectangle(corner_radius=0.06, width=0.34, height=0.54, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=0.38).move_to([-2.05, -1.06, 0])
    tooth_r = RoundedRectangle(corner_radius=0.06, width=0.34, height=0.54, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=0.38).move_to([-1.25, -1.06, 0])
    hinge_pts = [np.array([-0.5 + 1.5 * t, 0.14 * np.sin(TAU * t), 0.0]) for t in np.linspace(0, 1, 25)]
    hinge = VMobject(stroke_color=color, stroke_width=6.5).set_points_as_corners(hinge_pts)
    lbd = RoundedRectangle(corner_radius=0.26, width=3.8, height=1.88, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.28).move_to([2.9, 0.0, 0])
    pocket_cup = Circle(radius=0.50, stroke_color=YELLOW, stroke_width=3.0, stroke_opacity=0.70,
                        fill_color=BG, fill_opacity=0.90).move_to([2.9, 0.0, 0])
    g = VGroup(hinge, af1, dbd, zn1, zn2, tooth_l, tooth_r, lbd, pocket_cup)
    if mirror:
        g.scale([-1, 1, 1])
    g.scale(scale).move_to(center)
    g.af1 = af1
    g.dbd = dbd
    g.zincs = VGroup(zn1, zn2)
    g.teeth = VGroup(tooth_l, tooth_r)
    g.hinge = hinge
    g.lbd = lbd
    g.pocket = pocket_cup
    return g


def build_hsp90_clamps(receptor, radius=0.82, color=GREY):
    """Two curved Hsp90 clamp arms hugging top (pocket) and bottom (DNA grip) of receptor."""
    c = receptor.get_center()
    top_clamp = Arc(radius=radius, start_angle=0.16 * PI, angle=0.68 * PI, arc_center=c + UP * 0.20,
                    stroke_color=color, stroke_width=10)
    bot_clamp = Arc(radius=radius, start_angle=-0.84 * PI, angle=0.68 * PI, arc_center=c + DOWN * 0.28,
                    stroke_color=color, stroke_width=10)
    return VGroup(top_clamp, bot_clamp)


def build_tr_rxr_stage(active_off=False):
    """Shared world for S07 (end), S08 (PredictPause), S09, and S10:
    Route 2 nuclear stage with DNA, empty Thyroid Receptor + RXR, and Schematic Transcription Meter."""
    header = T("Route 2: Waiting on DNA", size=30, color=TEAL).move_to([-2.2, 3.15, 0])

    # Nuclear frame (x: -6.25..2.45, y: -2.2..2.5)
    nuc_box = RoundedRectangle(corner_radius=0.22, width=8.7, height=4.7, stroke_color=SLATE,
                               stroke_width=2.8, fill_color=SLATE, fill_opacity=0.07).move_to([-1.90, 0.15, 0])
    nuc_tag = T("Nucleus", size=24, color=TEXT).move_to([-5.35, 2.15, 0])

    dna = build_dna_strand(x0=-5.95, x1=2.25, y=-1.35, amp=0.16, freq=2.5)
    dna_lbl = T("DNA", size=26, color=CREAM).move_to([-5.4, -1.9, 0])

    # Empty Thyroid receptor (TEAL) on left half-site (x: -3.85..-1.65)
    tr = RoundedRectangle(corner_radius=0.22, width=2.2, height=1.55, stroke_color=TEAL, stroke_width=4,
                          fill_color=TEAL, fill_opacity=0.30).move_to([-2.75, -0.15, 0])
    tr_teeth = VGroup(
        RoundedRectangle(corner_radius=0.05, width=0.26, height=0.45, stroke_color=TEAL, stroke_width=3,
                         fill_color=TEAL, fill_opacity=0.38).move_to([-3.12, -1.05, 0]),
        RoundedRectangle(corner_radius=0.05, width=0.26, height=0.45, stroke_color=TEAL, stroke_width=3,
                         fill_color=TEAL, fill_opacity=0.38).move_to([-2.38, -1.05, 0]),
    )
    pocket = Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=0.95).move_to([-2.75, 0.12, 0])
    tr_lbl = T("Thyroid R", size=26, color=TEAL).next_to(tr, UP, buff=0.16)

    # Partner RXR (INDIGO) on right half-site (x: -1.48..+0.32)
    rxr = RoundedRectangle(corner_radius=0.22, width=1.80, height=1.50, stroke_color=INDIGO, stroke_width=4,
                           fill_color=INDIGO, fill_opacity=0.30).move_to([-0.58, -0.18, 0])
    rxr_teeth = VGroup(
        RoundedRectangle(corner_radius=0.05, width=0.26, height=0.45, stroke_color=INDIGO, stroke_width=3,
                         fill_color=INDIGO, fill_opacity=0.38).move_to([-0.88, -1.05, 0]),
        RoundedRectangle(corner_radius=0.05, width=0.26, height=0.45, stroke_color=INDIGO, stroke_width=3,
                         fill_color=INDIGO, fill_opacity=0.38).move_to([-0.28, -1.05, 0]),
    )
    rxr_lbl = T("RXR", size=28, color=INDIGO).next_to(rxr, UP, buff=0.16)

    # Schematic Transcription Meter on right (x: 2.8..6.2)
    meter_box = RoundedRectangle(corner_radius=0.18, width=3.4, height=4.7, stroke_color=SLATE,
                                 stroke_width=2.8, fill_color=BG, fill_opacity=0.92).move_to([4.5, 0.15, 0])
    meter_title = T("Transcription", size=26, color=TEXT).move_to([4.5, 2.2, 0])
    meter_sub = T("(schematic)", size=22, color=LABEL_MUTED).move_to([4.5, 1.82, 0])

    bar_x = 3.5
    y_bot, y_mid, y_top = -1.5, -0.1, 1.3
    track = Rectangle(width=0.48, height=y_top - y_bot, stroke_color=GREY, stroke_width=2.8,
                      fill_color=BG, fill_opacity=1.0).move_to([bar_x, (y_top + y_bot) / 2, 0])
    base_line = DashedLine([bar_x - 0.36, y_mid, 0], [bar_x + 0.42, y_mid, 0], color=TEXT, stroke_width=3)
    lbl_on = T("ON", size=24, color=GREEN).move_to([5.35, y_top - 0.15, 0])
    lbl_base = T("Baseline", size=24, color=TEXT).move_to([5.35, y_mid, 0])
    lbl_off = (T("Active off", size=24, color=RED) if active_off
               else T("Quieter", size=24, color=LABEL_MUTED)).move_to([5.35, y_bot + 0.15, 0])

    stage = VGroup(header, nuc_box, nuc_tag, dna, dna_lbl, tr, tr_teeth, pocket, tr_lbl,
                   rxr, rxr_teeth, rxr_lbl, meter_box, meter_title, meter_sub, track, base_line,
                   lbl_on, lbl_base, lbl_off)
    stage.tr = tr
    stage.tr_lbl = tr_lbl
    stage.pocket = pocket
    stage.rxr = rxr
    stage.rxr_lbl = rxr_lbl
    stage.dna = dna
    stage.bar_x = bar_x
    stage.y_bot = y_bot
    stage.y_mid = y_mid
    stage.y_top = y_top
    stage.meter_box = meter_box
    stage.lbl_off = lbl_off
    return stage


def meter_fill_and_dot(bar_x, y_mid, tracker, y_bot=-1.5, y_top=1.3, neutral=False):
    """Live meter fill + needle dot driven by a single ValueTracker in [-1, +1] (0 = Baseline)."""
    def _y():
        v = float(np.clip(tracker.get_value(), -1.0, 1.0))
        return y_mid + (y_top - y_mid) * v if v >= 0 else y_mid + (y_mid - y_bot) * v

    def _col():
        if neutral:
            return GOLD
        v = tracker.get_value()
        if v > 0.12:
            return GREEN
        if v < -0.12:
            return RED
        return GOLD

    def mk_fill():
        y = _y()
        h = abs(y - y_mid)
        if h < 0.02:
            return VMobject()
        c = _col()
        return Rectangle(width=0.44, height=h, stroke_width=0, fill_color=c, fill_opacity=0.88)\
            .move_to([bar_x, (y + y_mid) / 2, 0])

    def mk_dot():
        return Dot([bar_x, _y(), 0], radius=0.14, color=TEXT, stroke_color=_col(), stroke_width=3)

    return always_redraw(mk_fill), always_redraw(mk_dot)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Nuclear Receptors: Receptors That Are Transcription Factors"
    TITLE = "One Protein, Two Grips: How Nuclear Receptors Wait"


class S01Hook(SpokenScene):
    def construct(self):
        bilayer = build_bilayer(x=-3.2, y0=-2.25, y1=2.45)
        nuc_env = build_nuclear_envelope(x=1.4, y0=-2.25, y1=2.45, pore_y=0.1, pore_h=1.1)
        dna = build_dna_strand(x0=2.0, x1=5.8, y=0.1, amp=0.22, freq=2.6, stroke=4.5)

        lbl_out = T("Outside cell", size=28, color=TEXT).move_to([-4.8, 2.95, 0])
        lbl_mem = T("Membrane", size=28, color=TEXT).move_to([-3.2, -2.65, 0])
        lbl_cyto = T("Cytoplasm", size=28, color=TEXT).move_to([-0.9, 2.95, 0])
        lbl_nuc = T("Nucleus", size=28, color=TEXT).move_to([3.9, 2.95, 0])
        lbl_dna = T("DNA", size=28, color=CREAM).move_to([3.9, -0.60, 0])
        tag = scope_tag("schematic", color=LABEL_MUTED)

        surf_rec = VGroup(
            RoundedRectangle(corner_radius=0.1, width=0.70, height=0.46, stroke_color=GREY, stroke_width=3.5,
                             fill_color=GREY, fill_opacity=0.28).move_to([-3.2, 1.15, 0]),
            Arc(radius=0.24, start_angle=PI * 0.5, angle=PI, arc_center=[-3.55, 1.15, 0], stroke_color=GREY, stroke_width=4.5),
        )
        knock_dot = Dot([-5.3, 1.15, 0], radius=0.22, color=GREY)
        relay_p = ValueTracker(0.0)
        relay_line = always_redraw(lambda: DashedLine(
            [-2.75, 1.15, 0], [-2.75 + 3.0 * relay_p.get_value(), 1.15, 0],
            color=GREY, stroke_width=5.5, dash_length=0.14
        ) if relay_p.get_value() > 0.03 else VMobject())
        relay_nodes = VGroup(
            Dot([-2.1, 1.15, 0], radius=0.16, color=GREY),
            Dot([-1.0, 1.15, 0], radius=0.16, color=GREY),
            Dot([0.1, 1.15, 0], radius=0.16, color=GREY),
        )
        relay_lbl = T("Surface relay", size=28, color=GREY).move_to([-1.2, 1.78, 0])

        self.play(FadeIn(bilayer), FadeIn(nuc_env), FadeIn(dna),
                  FadeIn(lbl_out), FadeIn(lbl_mem), FadeIn(lbl_cyto), FadeIn(lbl_nuc), FadeIn(lbl_dna),
                  FadeIn(surf_rec), FadeIn(knock_dot), FadeIn(tag), run_time=0.6)

        self.at("knock")
        self.play(knock_dot.animate.move_to([-3.68, 1.15, 0]), run_time=0.9)
        self.add(relay_line)
        self.play(relay_p.animate.set_value(1.0), FadeIn(relay_lbl),
                  LaggedStart(*[FadeIn(n, scale=1.4) for n in relay_nodes], lag_ratio=0.35),
                  run_time=2.6, rate_func=linear)

        # Computed diffusion trajectories across the lipid bilayer (fixed seed)
        rng = np.random.default_rng(7)
        p1 = ValueTracker(0.0)
        p2 = ValueTracker(0.0)
        jitter1 = np.cumsum(rng.normal(0.0, 0.06, 50))
        jitter1 -= np.linspace(0, jitter1[-1], 50)
        jitter2 = np.cumsum(rng.normal(0.0, 0.06, 50))
        jitter2 -= np.linspace(0, jitter2[-1], 50)

        def steroid_pos(tr, y0, jit):
            u = float(np.clip(tr.get_value(), 0.0, 1.0))
            idx = min(len(jit) - 1, int(u * (len(jit) - 1)))
            return np.array([-5.2 + 6.1 * u, y0 + jit[idx], 0.0])

        cortisol = always_redraw(lambda: Dot(steroid_pos(p1, -0.35, jitter1), radius=0.30, color=YELLOW))
        estradiol = always_redraw(lambda: Dot(steroid_pos(p2, -1.35, jitter2), radius=0.30, color=YELLOW))
        lbl_cort_out = T("Hormone", size=28, color=YELLOW).move_to([-5.0, 0.25, 0])
        lbl_cort_in = T("Cortisol", size=28, color=YELLOW).move_to([-0.8, 0.30, 0])
        lbl_est_in = T("Estradiol", size=28, color=YELLOW).move_to([-0.8, -1.90, 0])

        self.at("What happens")
        self.play(FadeOut(surf_rec), FadeOut(knock_dot), FadeOut(relay_line), FadeOut(relay_nodes),
                  FadeOut(relay_lbl), FadeIn(cortisol), FadeIn(lbl_cort_out), run_time=0.5)

        self.at("slips straight")
        self.play(p1.animate.set_value(0.58), FadeOut(lbl_cort_out), run_time=2.5, rate_func=linear)

        self.at("Steroid hormones")
        cap = caption("Hydrophobic steroids cross directly", size=30, color=YELLOW, y=-3.25)
        self.play(FadeIn(estradiol), FadeIn(lbl_cort_in), FadeIn(cap), run_time=0.5)
        self.play(p1.animate.set_value(0.92), p2.animate.set_value(0.68), run_time=2.8, rate_func=linear)
        self.play(FadeIn(lbl_est_in), p1.animate.set_value(1.0), p2.animate.set_value(0.98),
                  run_time=2.4, rate_func=linear)
        self.finish()


class S02OneProtein(SpokenScene):
    def construct(self):
        nuc_env = build_nuclear_envelope(x=-2.3, y0=-2.3, y1=2.6, pore_y=0.4, pore_h=1.4)
        dna = build_dna_strand(x0=-1.6, x1=5.8, y=-1.55, amp=0.18, freq=2.6, stroke=4.5)
        lbl_dna = T("DNA", size=28, color=CREAM).move_to([-1.0, -2.08, 0])
        tag = scope_tag("schematic", color=LABEL_MUTED)

        rec = build_compact_receptor(center=[-4.4, 0.85, 0], scale=1.05, pocket_open=1.0)
        rec_lbl = T("1 receptor protein", size=28, color=TEAL).next_to(rec, UP, buff=0.22)
        hormone = Dot([-5.5, -0.75, 0], radius=0.22, color=YELLOW)
        h_lbl = T("Hormone", size=28, color=YELLOW).next_to(hormone, DOWN, buff=0.20)

        self.play(FadeIn(nuc_env), FadeIn(dna), FadeIn(lbl_dna), FadeIn(rec), FadeIn(rec_lbl),
                  FadeIn(hormone), FadeIn(h_lbl), FadeIn(tag), run_time=0.6)

        self.at("catches")
        target_pocket = rec.get_center() + RIGHT * 1.1
        self.play(hormone.animate.move_to(target_pocket), FadeOut(h_lbl), run_time=1.4)

        self.at("One protein")
        grp = VGroup(rec, hormone)
        self.play(FadeOut(rec_lbl), grp.animate.move_to([2.1, 0.35, 0]), run_time=0.6)

        self.at("binds the hormone")
        p_lig = grp.get_center() + RIGHT * 1.1
        arr_lig = Arrow(p_lig + UP * 1.15 + RIGHT * 0.5, p_lig + UP * 0.38, buff=0.05, color=YELLOW, stroke_width=4.5)
        lbl_lig = T("Binds ligand", size=28, color=YELLOW).next_to(arr_lig.get_start(), UP, buff=0.12)
        self.play(GrowArrow(arr_lig), FadeIn(lbl_lig), run_time=0.55)

        self.at("grips")
        self.play(grp.animate.shift(DOWN * 0.78), arr_lig.animate.shift(DOWN * 0.78),
                  lbl_lig.animate.shift(DOWN * 0.78), run_time=1.0)
        p_dna = rec.dna_grip.get_bottom() + LEFT * 0.15
        arr_dna = Arrow(p_dna + LEFT * 1.35 + UP * 0.22, p_dna + LEFT * 0.45 + UP * 0.15,
                        buff=0.05, color=CREAM, stroke_width=4.5)
        lbl_grip = T("Binds DNA", size=28, color=CREAM).next_to(arr_dna.get_start(), LEFT, buff=0.12)
        self.play(GrowArrow(arr_dna), FadeIn(lbl_grip), run_time=0.7)

        rna_len = ValueTracker(0.0)
        x_start = 3.0

        def mk_rna():
            L = rna_len.get_value()
            if L < 0.05:
                return VMobject()
            xs = np.linspace(0.0, L, max(3, int(35 * L)))
            pts = [np.array([x_start + s * 0.82, -1.32 + 0.44 * s + 0.11 * np.sin(6.0 * s), 0.0]) for s in xs]
            return VMobject(stroke_color=GREEN, stroke_width=5.5).set_points_as_corners(pts)

        rna_live = always_redraw(mk_rna)
        rna_lbl = T("RNA", size=28, color=GREEN).move_to([5.45, 0.55, 0])

        self.at("copy into")
        self.add(rna_live)
        self.play(FadeIn(rna_lbl), rna_len.animate.set_value(1.8), run_time=3.5, rate_func=linear)

        self.at("Here the receptor")
        cap = caption("Receptor is the transcription factor", size=30, color=TEAL)
        self.play(FadeIn(cap), rna_len.animate.set_value(2.5), run_time=1.2, rate_func=linear)
        self.play(rna_len.animate.set_value(3.0), run_time=1.6, rate_func=linear)
        self.finish()


class S03Domains(SpokenScene):
    def construct(self):
        dna = build_dna_strand(x0=-5.8, x1=5.8, y=-1.65, amp=0.18, freq=2.4, stroke=4.5)
        lbl_dna = T("DNA", size=28, color=CREAM).move_to([-5.3, -2.30, 0])
        tag = scope_tag("schematic", color=LABEL_MUTED)

        n_genes = ValueTracker(1.0)
        cnt = counter("{:.0f} human receptor genes", n_genes, at=[-3.6, 3.05, 0], size=28, color=TEAL, mono=False)

        rec_start = build_compact_receptor(center=[0.0, 0.15, 0], scale=1.1, pocket_open=0.3)
        mod = build_modular_receptor(center=[0.0, 0.25, 0], scale=1.02)

        self.play(FadeIn(dna), FadeIn(lbl_dna), FadeIn(rec_start), FadeIn(cnt), FadeIn(tag), run_time=0.35)
        self.play(n_genes.animate.set_value(48.0), run_time=0.50)

        self.at("48")
        self.play(rec_start.animate.stretch(1.8, 0), run_time=2.2)
        self.play(FadeOut(rec_start, run_time=0.25), FadeIn(mod, run_time=0.35))
        self.play(LaggedStart(
            Indicate(mod.af1, color=ORANGE, scale_factor=1.05),
            Indicate(mod.dbd, color=TEAL, scale_factor=1.05),
            Indicate(mod.lbd, color=TEAL, scale_factor=1.05),
            lag_ratio=0.35), run_time=2.0)

        lig_p = ValueTracker(0.0)
        p_start = np.array([5.5, 2.2, 0.0])
        p_end = mod.pocket.get_center()
        lig = always_redraw(lambda: Dot(
            (1 - lig_p.get_value()) * p_start + lig_p.get_value() * p_end + UP * 0.3 * np.sin(PI * lig_p.get_value()),
            radius=0.22, color=YELLOW
        ))
        lbl_lig = T("Ligand", size=28, color=YELLOW).next_to(mod.lbd, DOWN, buff=0.30)

        self.at("A ligand")
        self.add(lig)
        self.play(lig_p.animate.set_value(1.0), FadeIn(lbl_lig), run_time=5.0, rate_func=linear)

        lbl_af1 = T("AF-1", size=30, color=ORANGE).next_to(mod.af1, UP, buff=0.26)
        self.at("One end")
        self.play(FadeIn(lbl_af1), Indicate(mod.af1, color=ORANGE, scale_factor=1.06), run_time=2.6)

        lbl_lbd = T("Ligand pocket + AF-2", size=28, color=TEAL).next_to(mod.lbd, UP, buff=0.26)
        self.at("other holds")
        self.play(FadeIn(lbl_lbd), Indicate(mod.lbd, color=TEAL, scale_factor=1.05), run_time=2.2)

        lbl_zn = T("2 zinc ions", size=28, color=GOLD).next_to(mod.dbd, UP, buff=0.26)
        lbl_hinge = T("Hinge", size=26, color=TEAL).next_to(mod.hinge, UP, buff=0.80)
        self.at("Between them")
        self.play(FadeIn(lbl_zn), FadeIn(lbl_hinge),
                  Indicate(mod.zincs, color=GOLD, scale_factor=1.2), run_time=1.3)

        x_dbd = mod.dbd.get_center()[0]
        ticks = VGroup(*[
            Line([x_dbd - 0.75 + i * 0.3, -1.92, 0], [x_dbd - 0.75 + i * 0.3, -1.38, 0], color=GOLD, stroke_width=5.5)
            for i in range(6)
        ])
        lbl_6bp = T("Reads DNA", size=26, color=GOLD).move_to([x_dbd, -2.42, 0])

        self.at("zinc reads")
        self.play(LaggedStart(*[Create(tk) for tk in ticks], lag_ratio=0.18),
                  FadeIn(lbl_6bp, run_time=0.45), run_time=0.7)
        self.finish()


class S04Pairs(SpokenScene):
    def construct(self):
        dna = build_dna_strand(x0=-5.9, x1=5.9, y=-1.55, amp=0.18, freq=2.4, stroke=4.5)
        tag = scope_tag("schematic", color=LABEL_MUTED)

        r1 = build_modular_receptor(center=[-3.05, 0.35, 0], scale=0.56, mirror=False)
        lig1 = Dot(r1.pocket.get_center(), radius=0.16, color=YELLOW)
        g1 = VGroup(r1, lig1)

        r2 = build_modular_receptor(center=[3.05, 0.35, 0], scale=0.56, mirror=True)
        lig2 = Dot(r2.pocket.get_center(), radius=0.16, color=YELLOW)
        g2 = VGroup(r2, lig2).shift(RIGHT * 4.5)

        self.play(FadeIn(dna), FadeIn(g1), FadeIn(tag), run_time=0.6)

        self.at("work in pairs")
        self.play(g2.animate.shift(LEFT * 4.5), run_time=2.0)

        hs1 = RoundedRectangle(corner_radius=0.08, width=1.55, height=0.52, stroke_color=GOLD, stroke_width=4,
                               fill_color=GOLD, fill_opacity=0.26).move_to([r1.dbd.get_center()[0], -1.55, 0])
        hs2 = RoundedRectangle(corner_radius=0.08, width=1.55, height=0.52, stroke_color=GOLD, stroke_width=4,
                               fill_color=GOLD, fill_opacity=0.26).move_to([r2.dbd.get_center()[0], -1.55, 0])
        lbl_hs1 = T("Half-site 1", size=26, color=GOLD).next_to(hs1, DOWN, buff=0.22)
        lbl_hs2 = T("Half-site 2", size=26, color=GOLD).next_to(hs2, DOWN, buff=0.22)
        lbl_re = T("Response element", size=30, color=CREAM).move_to([0.0, -2.90, 0])

        self.at("Their site")
        self.play(FadeIn(hs1), FadeIn(hs2), run_time=1.8)
        self.at("two matching halves")
        self.play(FadeIn(lbl_hs1), FadeIn(lbl_hs2), FadeIn(lbl_re), run_time=1.6)

        br_lig = Brace(VGroup(r1.lbd, r2.lbd), UP, buff=0.20, color=YELLOW)
        lbl_clig = T("Chooses ligand", size=28, color=YELLOW).next_to(br_lig, UP, buff=0.16)
        self.at("Ligand")
        self.play(FadeIn(br_lig), FadeIn(lbl_clig),
                  Indicate(VGroup(r1.lbd, r2.lbd), color=YELLOW, scale_factor=1.04), run_time=1.8)

        lbl_cgene = T("Chooses gene", size=28, color=TEAL).move_to([-4.35, 2.25, 0])
        arr_g1 = Arrow(lbl_cgene.get_bottom() + RIGHT * 0.2, r1.dbd.get_top() + UP * 0.10,
                       buff=0.05, color=TEAL, stroke_width=4)
        self.at("separate modules")
        self.play(FadeIn(lbl_cgene), GrowArrow(arr_g1),
                  Indicate(VGroup(r1.dbd, r2.dbd), color=TEAL, scale_factor=1.04), run_time=1.4)

        self.at("So one protein")
        trace_pts = [
            r1.pocket.get_center(),
            r1.hinge.get_center(),
            r1.dbd.get_center(),
            hs1.get_center(),
        ]
        sig = ValueTracker(0.0)

        def mk_pulse():
            u = float(np.clip(sig.get_value(), 0.0, 1.0))
            seg_f = u * (len(trace_pts) - 1)
            i = min(len(trace_pts) - 2, int(seg_f))
            f = seg_f - i
            pos = (1 - f) * trace_pts[i] + f * trace_pts[i + 1]
            return Dot(pos, radius=0.17, color=GREEN, stroke_color=TEXT, stroke_width=2.5)

        pulse_dot = always_redraw(mk_pulse)
        self.add(pulse_dot)
        self.play(sig.animate.set_value(1.0), run_time=3.5, rate_func=linear)
        self.finish()


class S05WaitChaperone(SpokenScene):
    def construct(self):
        head = T("Before hormone arrives: how does a receptor wait?", size=30, color=GOLD).move_to([0.0, 3.20, 0])
        tag = scope_tag("schematic", color=LABEL_MUTED)

        lane1_box = RoundedRectangle(corner_radius=0.18, width=12.4, height=3.70, stroke_color=TEAL, stroke_width=2.8,
                                     fill_color=TEAL, fill_opacity=0.05).move_to([0.0, 0.90, 0])
        lane1_lbl = T("Route 1: Waiting off DNA", size=26, color=TEAL).move_to([-3.95, 2.42, 0])
        nuc_env1 = build_nuclear_envelope(x=1.35, y0=-0.80, y1=2.55, pore_y=0.95, pore_h=0.95)
        dna1 = build_dna_strand(x0=1.95, x1=5.85, y=0.25, amp=0.14, freq=2.6)
        lbl_cyto = T("Cytoplasm", size=24, color=TEXT).move_to([-0.25, 2.42, 0])
        lbl_nuc = T("Nucleus", size=24, color=TEXT).move_to([3.9, 2.42, 0])
        lbl_dna = T("DNA", size=24, color=CREAM).move_to([5.25, -0.35, 0])

        lane2_box = RoundedRectangle(corner_radius=0.18, width=10.6, height=1.85, stroke_color=SLATE, stroke_width=2.2,
                                     fill_color=SLATE, fill_opacity=0.04).move_to([-0.9, -2.20, 0])
        lane2_lbl = T("Route 2: Waiting on DNA", size=26, color=LABEL_MUTED).move_to([-3.95, -1.58, 0])
        dna2 = build_dna_strand(x0=0.4, x1=4.1, y=-2.60, amp=0.10, freq=2.6, color=CREAM)
        rec2_ph = RoundedRectangle(corner_radius=0.14, width=1.4, height=0.62, stroke_color=INDIGO, stroke_width=2.8,
                                   fill_color=INDIGO, fill_opacity=0.24).move_to([2.25, -2.02, 0])

        # Start receptor near center, glide leftward into Route 1 cytoplasm when lanes split
        rec1 = build_compact_receptor(center=[-1.5, 0.92, 0], scale=0.76, pocket_open=1.0)
        lbl_ga = T("Glucocorticoid / Androgen R", size=24, color=TEAL).move_to([-3.75, -0.58, 0])

        self.play(FadeIn(head), FadeIn(rec1), FadeIn(tag), run_time=0.7)
        # Keep receptor sliding smoothly leftward while waiting for "two routes" so no 4s static hold
        self.play(rec1.animate.move_to([-3.65, 0.92, 0]), run_time=4.0, rate_func=linear)

        self.at("two routes")
        self.play(FadeIn(lane1_box), FadeIn(lane1_lbl), FadeIn(nuc_env1), FadeIn(dna1),
                  FadeIn(lbl_cyto), FadeIn(lbl_nuc), FadeIn(lbl_dna),
                  FadeIn(lane2_box), FadeIn(lane2_lbl), FadeIn(dna2), FadeIn(rec2_ph), run_time=1.3)

        self.at("Glucocorticoid")
        self.play(FadeIn(lbl_ga), rec1.animate.shift(LEFT * 0.20), run_time=1.2)

        # Clamps approach smoothly from the right (cytoplasm) so they never cross Route 1 or Glucocorticoid labels
        clamps = build_hsp90_clamps(rec1, radius=0.76, color=GREY)
        clamps_start = clamps.copy().shift(RIGHT * 1.45)
        lbl_hsp = T("Hsp90 chaperones", size=26, color=TEXT).move_to([-0.85, 1.78, 0])
        self.play(FadeIn(clamps_start, run_time=0.5), run_time=0.5)
        self.play(clamps_start.animate.shift(LEFT * 0.65), run_time=2.8, rate_func=linear)

        self.at("Hsp90 chaperones")
        self.play(Transform(clamps_start, clamps), FadeIn(lbl_hsp), run_time=1.8)
        self.remove(clamps_start)
        self.add(clamps)

        self.at("holds a")
        lbl_pock = T("Pocket ready", size=26, color=YELLOW).move_to([-0.85, 1.00, 0])
        self.play(clamps[0].animate.shift(UP * 0.14), FadeIn(lbl_pock), run_time=2.5)

        self.at("off")
        barrier = Line([1.05, 0.25, 0], [1.05, 1.65, 0], color=RED, stroke_width=5.5)
        lbl_off = T("Kept off DNA", size=26, color=RED).move_to([-0.65, 0.22, 0])
        self.play(clamps[1].animate.shift(UP * 0.14), Create(barrier), FadeIn(lbl_off), run_time=1.6)
        self.finish()


class S06ChaperoneRelease(SpokenScene):
    def construct(self):
        lane1_lbl = T("Route 1: Waiting off DNA", size=28, color=TEAL).move_to([-3.9, 3.18, 0])
        lane1_box = RoundedRectangle(corner_radius=0.18, width=12.4, height=4.15, stroke_color=TEAL, stroke_width=2.8,
                                     fill_color=TEAL, fill_opacity=0.05).move_to([0.0, 0.72, 0])
        # Bilayer at x=-4.55 so Cortisol & label start completely clear to the left inside lane1_box (-6.2)
        bilayer = build_bilayer(x=-4.55, y0=-1.15, y1=2.45)
        nuc_env = build_nuclear_envelope(x=-0.35, y0=-1.20, y1=2.65, pore_y=0.80, pore_h=1.2)
        dna1 = build_dna_strand(x0=0.35, x1=5.85, y=-0.72, amp=0.14, freq=2.6)
        lbl_dna = T("DNA", size=24, color=CREAM).move_to([5.40, -1.12, 0])
        lbl_nuc = T("Nucleus", size=24, color=TEXT).move_to([5.15, 2.45, 0])

        lane2_box = RoundedRectangle(corner_radius=0.18, width=10.6, height=1.45, stroke_color=SLATE, stroke_width=2.2,
                                     fill_color=SLATE, fill_opacity=0.04).move_to([-0.9, -2.35, 0])
        lane2_lbl = T("Route 2: Waiting on DNA", size=24, color=LABEL_MUTED).move_to([-4.0, -1.92, 0])
        dna2 = build_dna_strand(x0=0.4, x1=4.1, y=-2.65, amp=0.09, freq=2.6)
        tag = scope_tag("schematic", color=LABEL_MUTED)

        rec1 = build_compact_receptor(center=[-2.85, 0.80, 0], scale=0.76, pocket_open=1.0)
        clamps1 = build_hsp90_clamps(rec1, radius=0.76, color=GREY)
        lbl_hsp = T("Hsp90", size=24, color=TEXT).next_to(clamps1[0], UP, buff=0.14)

        # Cortisol at x=-5.45, label BELOW at y=0.25 (clear of bilayer x=-4.55 and lane1_box left -6.2)
        cortisol = Dot([-5.45, 0.80, 0], radius=0.18, color=YELLOW)
        lbl_cort = T("Cortisol", size=24, color=YELLOW).move_to([-5.45, 0.25, 0])

        self.add(lane1_lbl, lane1_box, bilayer, nuc_env, dna1, lbl_dna, lbl_nuc,
                 lane2_box, lane2_lbl, dna2, rec1, clamps1, lbl_hsp, cortisol, lbl_cort, tag)

        self.at("cortisol enters")
        self.play(FadeOut(lbl_cort, run_time=0.35), cortisol.animate.move_to(rec1.get_center() + RIGHT * 0.80), run_time=1.8)

        self.at("rearranges")
        self.play(clamps1[0].animate.shift(UP * 0.18), clamps1[1].animate.shift(DOWN * 0.18),
                  lbl_hsp.animate.shift(UP * 0.18), run_time=1.3)

        self.at("enters the nucleus")
        self.play(FadeOut(lbl_hsp), run_time=0.35)
        complex_grp = VGroup(rec1, cortisol, clamps1)
        self.play(complex_grp.animate.shift(RIGHT * 4.45), run_time=1.35)

        self.at("sheds its")
        self.play(clamps1[0].animate.shift(UP * 0.45 + LEFT * 0.25).set_opacity(0.0),
                  clamps1[1].animate.shift(DOWN * 0.14 + LEFT * 0.35).set_opacity(0.0),
                  run_time=1.4)

        self.at("pairs with")
        rec_pair = build_compact_receptor(center=[4.35, 1.35, 0], scale=0.76, pocket_open=0.2, flip_x=True)
        cort2 = Dot(rec_pair.get_center() + LEFT * 0.80, radius=0.18, color=YELLOW)
        pair_grp = VGroup(rec_pair, cort2)
        self.play(FadeIn(pair_grp), run_time=0.5)
        self.play(VGroup(rec1, cortisol).animate.move_to([1.40, 0.02, 0]),
                  pair_grp.animate.move_to([4.35, 0.02, 0]), run_time=1.9)

        # Estrogen receptor at x=1.05 (right edge ~1.85), wrapped 2-line label cleanly to the right at x=4.15
        self.at("Estrogen receptors")
        er_rec = build_compact_receptor(center=[1.05, 1.78, 0], scale=0.45, pocket_open=0.8)
        er_clamps = build_hsp90_clamps(er_rec, radius=0.42, color=GREY)
        er_lbl = T("Estrogen R:\nHsp90 in nucleus", size=24, color=TEAL, line_spacing=0.85).move_to([4.15, 1.85, 0])
        self.play(FadeIn(er_rec), FadeIn(er_clamps), FadeIn(er_lbl), run_time=1.2)
        self.play(er_clamps[0].animate.shift(UP * 0.08), er_clamps[1].animate.shift(DOWN * 0.05), run_time=3.2)
        self.finish()


class S07WaitDnaPredict(SpokenScene):
    def construct(self):
        lane1_ph = RoundedRectangle(corner_radius=0.18, width=12.4, height=3.8, stroke_color=TEAL, stroke_width=2.2,
                                    fill_color=TEAL, fill_opacity=0.05).move_to([0.0, 1.0, 0])
        lane1_txt = T("Route 1: Waiting off DNA", size=26, color=LABEL_MUTED).move_to([-3.9, 2.55, 0])

        stage = build_tr_rxr_stage()
        rxr_full = VGroup(stage[9], stage[10], stage[11])
        meter_full = VGroup(stage[12:])
        tr_full = VGroup(stage[5], stage[6], stage[7], stage[8])

        self.add(lane1_ph, lane1_txt)
        self.play(FadeOut(lane1_ph), FadeOut(lane1_txt), run_time=0.5)
        self.play(FadeIn(stage[0]), FadeIn(stage[1]), FadeIn(stage[2]), FadeIn(stage[3]), FadeIn(stage[4]),
                  run_time=1.0)

        self.at("stay in the nucleus")
        self.play(FadeIn(tr_full), run_time=1.4)

        self.at("paired with")
        # Keep RXR starting cleanly inside nuc_box (right edge 2.45; rxr at +1.1 has right edge 2.0)
        rxr_full.shift(RIGHT * 1.68)
        self.play(FadeIn(rxr_full), run_time=0.4)
        self.play(rxr_full.animate.shift(LEFT * 1.68), run_time=1.6)

        self.at("Picture an empty")
        empty_lbl = T("Empty pocket", size=24, color=YELLOW).move_to([-5.0, 0.12, 0])
        arr_emp = Arrow(empty_lbl.get_right() + RIGHT * 0.06, stage.pocket.get_left() + LEFT * 0.06,
                        buff=0.04, color=YELLOW, stroke_width=3.5)
        # Pulse only an outline ring (never fill the empty pocket with solid yellow!)
        ring_emp = Circle(radius=0.38, stroke_color=YELLOW, stroke_width=4, fill_opacity=0).move_to(stage.pocket)
        self.play(FadeIn(empty_lbl), GrowArrow(arr_emp), Create(ring_emp), run_time=1.4)
        self.play(FadeOut(ring_emp), run_time=1.2)

        self.at("Is that gene")
        val = ValueTracker(0.0)
        _, mdot = meter_fill_and_dot(stage.bar_x, stage.y_mid, val, stage.y_bot, stage.y_top, neutral=True)
        q = question_card("Empty thyroid receptor on DNA: baseline or quieter?",
                          y=BOTTOM_Y + 0.1, color=GOLD, size=30, max_w=10.2)
        qmark = T("?", size=38, color=GOLD).move_to([stage.bar_x + 0.58, stage.y_mid - 0.65, 0])

        self.play(FadeIn(meter_full), FadeIn(q), FadeIn(qmark), run_time=0.8)
        self.add(mdot)
        # Keep meter sweeping neutrally up to scene end, settling at Baseline (0.0)
        self.play(val.animate.set_value(-0.78), run_time=1.15)
        self.play(val.animate.set_value(0.05), run_time=1.15)
        self.play(val.animate.set_value(-0.72), run_time=1.15)
        self.play(val.animate.set_value(0.0), run_time=1.15)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Empty thyroid receptor on DNA: baseline or quieter?"
    CARD = {"y": BOTTOM_Y + 0.1, "size": 30, "max_w": 10.2}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        stage = build_tr_rxr_stage()
        empty_lbl = T("Empty pocket", size=24, color=YELLOW).move_to([-5.0, 0.12, 0])
        arr_emp = Arrow(empty_lbl.get_right() + RIGHT * 0.06, stage.pocket.get_left() + LEFT * 0.06,
                        buff=0.04, color=YELLOW, stroke_width=3.5)
        val = ValueTracker(0.0)
        _, mdot = meter_fill_and_dot(stage.bar_x, stage.y_mid, val, stage.y_bot, stage.y_top, neutral=True)
        qmark = T("?", size=38, color=GOLD).move_to([stage.bar_x + 0.58, stage.y_mid - 0.65, 0])
        return VGroup(stage, empty_lbl, arr_emp, mdot, qmark)


class S09RevealActiveOff(SpokenScene):
    def construct(self):
        stage = build_tr_rxr_stage()
        empty_lbl = T("Empty pocket", size=24, color=YELLOW).move_to([-5.0, 0.12, 0])
        arr_emp = Arrow(empty_lbl.get_right() + RIGHT * 0.06, stage.pocket.get_left() + LEFT * 0.06,
                        buff=0.04, color=YELLOW, stroke_width=3.5)
        val = ValueTracker(0.0)
        mfill, mdot = meter_fill_and_dot(stage.bar_x, stage.y_mid, val, stage.y_bot, stage.y_top)
        qmark = T("?", size=38, color=GOLD).move_to([stage.bar_x + 0.58, stage.y_mid - 0.65, 0])
        q_old = question_card("Empty thyroid receptor on DNA: baseline or quieter?",
                              y=BOTTOM_Y + 0.1, color=GOLD, size=30, max_w=10.2)

        self.add(stage, empty_lbl, arr_emp, mfill, mdot, qmark, q_old)

        lbl_active_off = T("Active off", size=24, color=RED).move_to([5.35, stage.y_bot + 0.15, 0])
        self.play(FadeOut(q_old), FadeOut(qmark),
                  swap(stage.lbl_off, lbl_active_off, run_time=1.3),
                  val.animate.set_value(-0.92), run_time=1.3)

        self.at("empty receptor")
        corep = RoundedRectangle(corner_radius=0.16, width=2.45, height=0.80, stroke_color=RED, stroke_width=3.5,
                                 fill_color=RED, fill_opacity=0.28).move_to([-2.75, 1.02, 0])
        corep_lbl = T("Co-repressor", size=26, color=RED).move_to(corep)
        corep_grp = VGroup(corep, corep_lbl).shift(UP * 0.95)
        self.play(FadeOut(stage.tr_lbl, run_time=0.3), FadeIn(corep_grp, run_time=0.4))
        self.play(corep_grp.animate.shift(DOWN * 0.95), run_time=1.5)

        # Histone spools downstream (base_cx = 1.35, clear of RXR right edge 0.32 and nuc_box right 2.45)
        spool_x = ValueTracker(0.54)
        base_cx = 1.35

        def mk_histones():
            dx = spool_x.get_value()
            g = VGroup()
            for i in (-1, 0, 1):
                sp = Circle(radius=0.31, stroke_color=CREAM, stroke_width=3.8, fill_color=CREAM, fill_opacity=0.28)\
                    .move_to([base_cx + i * dx, -1.35, 0])
                g.add(sp)
            return g

        histones = always_redraw(mk_histones)
        lbl_hist = T("Histones", size=24, color=CREAM).move_to([1.35, -1.94, 0])
        tags = VGroup(*[
            Dot([base_cx + i * 0.54 + s * 0.12, -0.88, 0], radius=0.12, color=GREEN)
            for i in (-1, 0, 1) for s in (-1, 1)
        ])
        lbl_ac = T("Acetyl tags", size=24, color=GREEN).move_to([1.35, -0.38, 0])

        self.at("bring enzymes")
        self.play(FadeIn(histones), FadeIn(lbl_hist), FadeIn(tags), FadeIn(lbl_ac), run_time=0.8)

        self.at("strip acetyl tags")
        self.play(FadeOut(lbl_ac), run_time=0.35)
        self.play(LaggedStart(*[t.animate.shift(UP * 1.15).set_opacity(0.0) for t in tags], lag_ratio=0.25),
                  run_time=5.4)

        self.at("packs tighter")
        self.play(spool_x.animate.set_value(0.28), run_time=0.85)

        self.at("blocks")
        # RNA pol at x=1.35, width=1.40 -> 0.65..2.05 (clear of RXR 0.32 and nuc_box 2.45!)
        pol = RoundedRectangle(corner_radius=0.25, width=1.40, height=0.62, stroke_color=TEXT, stroke_width=3.2,
                               fill_color=TEXT, fill_opacity=0.22).move_to([1.35, 1.10, 0])
        pol_txt = T("RNA pol", size=24, color=TEXT).move_to(pol)
        pol_grp = VGroup(pol, pol_txt)
        blk = T("Blocked", size=26, color=RED).move_to([1.35, 1.75, 0])
        self.play(FadeIn(pol_grp), run_time=0.4)
        self.play(pol_grp.animate.move_to([1.35, -0.58, 0]), run_time=1.3)
        self.play(pol_grp.animate.move_to([1.35, 0.50, 0]), FadeIn(blk), run_time=1.5)
        self.finish()


class S10SwapAndClose(SpokenScene):
    def construct(self):
        # Rebuild exact end state of S09
        stage = build_tr_rxr_stage(active_off=True)
        stage.remove(stage.tr_lbl)
        empty_lbl = T("Empty pocket", size=24, color=YELLOW).move_to([-5.0, 0.12, 0])
        arr_emp = Arrow(empty_lbl.get_right() + RIGHT * 0.06, stage.pocket.get_left() + LEFT * 0.06,
                        buff=0.04, color=YELLOW, stroke_width=3.5)

        val = ValueTracker(-0.92)
        mfill, mdot = meter_fill_and_dot(stage.bar_x, stage.y_mid, val, stage.y_bot, stage.y_top)

        corep = RoundedRectangle(corner_radius=0.16, width=2.45, height=0.80, stroke_color=RED, stroke_width=3.5,
                                 fill_color=RED, fill_opacity=0.28).move_to([-2.75, 1.02, 0])
        corep_lbl = T("Co-repressor", size=26, color=RED).move_to(corep)
        corep_grp = VGroup(corep, corep_lbl)

        spool_x = ValueTracker(0.28)
        base_cx = 1.35

        def mk_histones():
            dx = spool_x.get_value()
            g = VGroup()
            for i in (-1, 0, 1):
                sp = Circle(radius=0.31, stroke_color=CREAM, stroke_width=3.8, fill_color=CREAM, fill_opacity=0.28)\
                    .move_to([base_cx + i * dx, -1.35, 0])
                g.add(sp)
            return g

        histones = always_redraw(mk_histones)
        lbl_hist = T("Histones", size=24, color=CREAM).move_to([1.35, -1.94, 0])
        self.add(stage, empty_lbl, arr_emp, mfill, mdot, corep_grp, histones, lbl_hist)

        # Thyroid hormone enters pocket (wrapped 2-line label cleanly inside [-6.25, -3.85])
        self.at("thyroid hormone binds")
        t3 = Dot([-5.05, 0.12, 0], radius=0.22, color=YELLOW)
        t3_lbl = T("Thyroid\nhormone", size=24, color=YELLOW, line_spacing=0.85).move_to([-5.05, -0.50, 0])
        self.play(FadeOut(empty_lbl, run_time=0.25), FadeOut(arr_emp, run_time=0.25),
                  FadeIn(t3, run_time=0.35), FadeIn(t3_lbl, run_time=0.35))
        self.play(FadeOut(t3_lbl, run_time=0.35), t3.animate.move_to(stage.pocket.get_center()), run_time=1.3)

        self.at("receptor drops")
        self.play(corep_grp.animate.shift(UP * 0.95 + LEFT * 0.4).set_opacity(0.0), run_time=1.2)

        self.at("recruits")
        coact = RoundedRectangle(corner_radius=0.16, width=2.45, height=0.80, stroke_color=GREEN, stroke_width=3.5,
                                 fill_color=GREEN, fill_opacity=0.28).move_to([-2.75, 1.02, 0])
        coact_lbl = T("Co-activator", size=26, color=GREEN).move_to(coact)
        coact_grp = VGroup(coact, coact_lbl).shift(UP * 0.95)
        self.play(FadeIn(coact_grp, run_time=0.3))
        self.play(coact_grp.animate.shift(DOWN * 0.95), run_time=1.5)

        self.at("add acetyl tags")
        def mk_tags():
            dx = spool_x.get_value()
            return VGroup(*[
                Dot([base_cx + i * dx + s * 0.12, -0.88, 0], radius=0.12, color=GREEN)
                for i in (-1, 0, 1) for s in (-1, 1)
            ])

        tags = mk_tags()
        lbl_ac = T("Acetyl tags", size=24, color=GREEN).move_to([1.35, -0.38, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tags], lag_ratio=0.18),
                  FadeIn(lbl_ac), run_time=2.0)

        self.at("loosening")
        tags_live = always_redraw(mk_tags)
        self.remove(tags)
        self.add(tags_live)
        self.play(spool_x.animate.set_value(0.54), FadeOut(lbl_ac, run_time=0.5), run_time=1.3)

        self.at("transcription starts")
        rna_len = ValueTracker(0.0)

        def mk_rna():
            L = rna_len.get_value()
            if L < 0.05:
                return VMobject()
            xs = np.linspace(0.0, L, max(3, int(35 * L)))
            pts = [np.array([0.44 + 0.14 * (s ** 1.6), -1.30 + 0.78 * s + 0.06 * np.sin(6.0 * s), 0.0]) for s in xs]
            return VMobject(stroke_color=GREEN, stroke_width=5.5).set_points_as_corners(pts)

        rna_live = always_redraw(mk_rna)
        rna_lbl = T("RNA", size=26, color=GREEN).move_to([1.85, 1.65, 0])
        self.add(rna_live)
        self.play(val.animate.set_value(0.88), rna_len.animate.set_value(1.5), FadeIn(rna_lbl),
                  run_time=2.0, rate_func=linear)

        # Other family members sense lipids: visible lipid flux cleanly left of receptor
        self.at("Other family members")
        lip1 = Dot([-5.7, 1.05, 0], radius=0.22, color=YELLOW)
        lbl_fa = T("Fatty acids", size=24, color=YELLOW).move_to([-5.15, 1.55, 0])
        lip2 = Dot([-5.7, -0.35, 0], radius=0.22, color=YELLOW)
        lbl_ba = T("Bile acids", size=24, color=YELLOW).move_to([-5.15, -0.82, 0])
        lip_grp = VGroup(lip1, lbl_fa, lip2, lbl_ba)
        self.play(FadeIn(lip_grp, run_time=0.5))
        self.play(lip1.animate.shift(RIGHT * 1.45), lip2.animate.shift(RIGHT * 1.45),
                  rna_len.animate.set_value(2.4), run_time=4.4, rate_func=linear)

        self.at("In this route")
        cap = caption("Ligand + DNA -> Transcription", size=30, color=TEXT)
        self.play(FadeOut(lip_grp, run_time=0.45), rna_len.animate.set_value(2.7), run_time=0.6)
        # Keep t3 bright YELLOW; highlight ligand->DNA->RNA bridge cleanly
        self.play(FadeIn(cap), rna_len.animate.set_value(2.76), run_time=0.45, rate_func=linear)
        self.play(rna_len.animate(rate_func=linear).set_value(3.35),
                  Indicate(stage.tr, color=TEAL, scale_factor=1.04, rate_func=there_and_back),
                  run_time=4.75)
        self.finish()


class S11End(EndCard):
    LINE = "A nuclear receptor binds both ligand and DNA to control transcription."
