"""Signal Two and Two Brakes — Antigen Receptors and Checkpoints (Chapter 2)

COLOUR MAP (one colour per concept for the whole film):
- TCR_BLUE      (#58C4DD): TCR recognition chains and active T-cell membrane signal
- ZETA_TEAL     (#3FB8C0): partner signalling tails (CD3 / zeta) and CAR zeta tail
- PHOS_GOLD     (#F5D547): phosphate badges (signal-1 and signal-2 marks) and activation flare
- MHC_SLATE     (#94A3B8): MHC protein and resting presenting-cell membrane
- PEPTIDE_WHITE (#E8EAF0): peptide in MHC groove and primary text
- CD28_GREEN    (#83C167): CD28 co-stimulatory receptor and CD28/4-1BB cytoplasmic block
- B7_EMERALD    (#2ECC71): B7 co-stimulatory ligand on presenting cell
- CTLA4_CRIMSON (#FC6255): CTLA-4 brake (outside) and endosome destruction path
- PD1_MAGENTA   (#E056A0): PD-1 brake (inside)
- PDL1_PLUM     (#A864D8): PD-L1 ligand on tissue or tumour cell
- SHP2_ORANGE   (#F08C3A): SHP-2 phosphatase (two SH2 grips and swinging catalytic end)
- AB_CYAN       (#67E8F9): checkpoint-blocking antibodies and CAR antibody tip
- SURF_PROT     (#93C5FD): tumour surface protein / tumour peptide target (distinct from PD-L1)
- CAUTION_AMBER (#F59E0B): self-peptide caution and autoimmune inflammation risk
- DIM_GREY      (#6C7482): anergy / dimmed unresponsive cell state (shapes only, never text)

SHARED WORLD:
A cross-section of the immune synapse carried from scene to scene: the presenting, tissue, or
tumour cell membrane above and the T-cell membrane below, shifting vertically only when the
story zooms inside the T cell (s04-s06) to follow SHP-2's catalytic arm, then pulling back
to align all natural and synthetic receptors along the same membrane (s10).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_link_hook: Gold phosphates light up on partner ITAMs and drive an activation surge in the
  T-cell membrane; several TCR tips cycle through random shapes from np.random.default_rng(7)
  before one locks onto a self-peptide; amber caution glow grows around the T cell.
- s02_signal_two: CD28 probes an empty top membrane while T-cell activation tracker drains from
  0.85 to 0.0 (anergy); emerald B7 rises smoothly from the presenting cell, locks CD28, flashes
  gold tail phosphates, and drives the activation tracker from 0.0 to 1.0 as extra B7 rises.
- s03_ctla4_outside: T-cell activation rises then crimson CTLA-4 dimer emerges from inside the
  T cell, spreads its twin arms to grip two B7 proteins at once while CD28's tail phosphates
  fade, then drags both B7 proteins down into a T-cell endosome where they shrink away.
- s04_predict_pd1: Top cell transitions smoothly to plum tissue/tumour displaying PD-L1; magenta
  PD-1 meets PD-L1, two gold phosphates grow on PD-1's ITSM tail, and burnt-orange SHP-2 rises
  across the cytoplasm as the question banner appears.
- s06_reveal_pd1: SHP-2 clamps both SH2 cups onto PD-1's two phosphates, then its catalytic arm
  swings along a computed circular arc to CD28 and TCR partner tails, erasing their gold
  phosphates and driving the T-cell activation tracker progressively down from 1.0 to 0.0.
- s07_checkpoint_drugs: Cyan Y-antibodies sweep in onto CTLA-4 and PD-1 on the T cell; B7 returns
  to CD28, PD-L1 releases, SHP-2 detaches downward, gold phosphates return, T-cell activation
  tracker surges to 1.0, and an amber autoimmune risk badge appears.
- s08_car_t: Mismatched natural TCR slides aside as a continuous synthetic CAR chain assembles
  across the membrane (cyan-white antibody tip, hinge, teal zeta tail with 3 ITAMs), extends to
  grip a tumour surface protein directly without MHC, and lights 3 gold phosphates.
- s09_car_signal_two: Zeta-only CAR flashes then fades dim while a T-cell persistence circle
  shrinks; green CD28/4-1BB block slides into the chain above zeta, both light gold on one
  binding event, and the T cell divides smoothly into 1 -> 2 -> 4 daughter cells.
- s10_return_rule: Two-signal CAR holds on the right as the camera pulls back to align
  TCR + CD28-B7, CTLA-4, PD-1/SHP-2, checkpoint antibody, and two-signal CAR along one synapse,
  with the shared wiring banner and signal highlight sweeping across.
"""
from bp_parts import *

# ------------------------------------------------------------------ Colour map
TCR_BLUE = "#58C4DD"
ZETA_TEAL = "#3FB8C0"
PHOS_GOLD = "#F5D547"
MHC_SLATE = "#94A3B8"
PEPTIDE_WHITE = "#E8EAF0"
CD28_GREEN = "#83C167"
B7_EMERALD = "#2ECC71"
CTLA4_CRIMSON = "#FC6255"
PD1_MAGENTA = "#E056A0"
PDL1_PLUM = "#A864D8"
SHP2_ORANGE = "#F08C3A"
AB_CYAN = "#67E8F9"
SURF_PROT = "#93C5FD"
CAUTION_AMBER = "#F59E0B"
DIM_GREY = "#6C7482"


# ------------------------------------------------------------------ Shared builders
def make_cell_band(y_mem, is_top=True, color=MHC_SLATE, fill_opacity=0.13,
                   label=None, label_pos=None, outer_y=None):
    """Build a cell membrane bar + soft interior fill spanning the safe width."""
    x0, x1 = -6.35, 6.35
    if outer_y is None:
        outer_y = 3.55 if is_top else -3.55
    h = abs(outer_y - y_mem)
    cy = (outer_y + y_mem) / 2.0
    fill = Rectangle(
        width=x1 - x0, height=h, stroke_width=0,
        fill_color=color, fill_opacity=fill_opacity,
    ).move_to([0.0, cy, 0.0]).set_z_index(-5)
    mem = Line([x0, y_mem, 0], [x1, y_mem, 0], color=color, stroke_width=4.5).set_z_index(-2)
    g = VGroup(fill, mem)
    g.fill_rect = fill
    g.membrane = mem
    if label:
        pos = label_pos if label_pos is not None else (
            [-4.6, (y_mem + outer_y) / 2.0 + (0.10 if is_top else -0.10), 0]
        )
        lab = T(label, size=26, color=TEXT, weight=BOLD).move_to(pos)
        g.add(lab)
        g.label = lab
    return g


def make_phos(pos, radius=0.15, color=PHOS_GOLD):
    """Gold phosphate circle with P."""
    c = Circle(radius=radius, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.92).move_to(pos)
    p = T("P", size=max(22, int(round(radius * 128))), color=BG, weight=BOLD).move_to(pos)
    p.layout_ok = True  # tight P centered inside its own phosphate badge
    return VGroup(c, p).set_z_index(4)


def make_mhc_peptide(x, y_top, peptide_color=PEPTIDE_WHITE, mhc_color=MHC_SLATE, stalk_h=0.58):
    """Slate MHC protein hanging from top membrane, holding a short peptide badge."""
    stalk = Rectangle(width=0.34, height=stalk_h, color=mhc_color, stroke_width=3,
                      fill_color=mhc_color, fill_opacity=0.22).move_to([x, y_top - stalk_h / 2.0, 0])
    cup_y = y_top - stalk_h - 0.04
    cup = Arc(radius=0.36, start_angle=PI, angle=PI, arc_center=[x, cup_y, 0],
              color=mhc_color, stroke_width=5)
    pep = RoundedRectangle(corner_radius=0.09, width=0.46, height=0.19,
                           color=peptide_color, stroke_width=2.5,
                           fill_color=peptide_color, fill_opacity=0.92).move_to([x, cup_y - 0.14, 0])
    g = VGroup(stalk, cup, pep)
    g.cup = cup
    g.peptide = pep
    return g


def make_tcr_complex(x, y_bot, tip_notch=0.16, has_phosphates=True,
                     tcr_color=TCR_BLUE, tail_color=ZETA_TEAL,
                     chain_h=1.28, tail_len=1.05):
    """Steel-blue TCR recognition chains above y_bot + teal partner ITAM tails strictly below y_bot."""
    l_chain = RoundedRectangle(corner_radius=0.08, width=0.20, height=chain_h,
                               color=tcr_color, stroke_width=3,
                               fill_color=tcr_color, fill_opacity=0.25).move_to([x - 0.14, y_bot + chain_h / 2.0, 0])
    r_chain = RoundedRectangle(corner_radius=0.08, width=0.20, height=chain_h,
                               color=tcr_color, stroke_width=3,
                               fill_color=tcr_color, fill_opacity=0.25).move_to([x + 0.14, y_bot + chain_h / 2.0, 0])
    tip_y = y_bot + chain_h
    pts = [
        [x - 0.34, tip_y - 0.08, 0],
        [x - 0.26, tip_y + 0.22, 0],
        [x - tip_notch, tip_y + 0.09, 0],
        [x + tip_notch, tip_y + 0.09, 0],
        [x + 0.26, tip_y + 0.22, 0],
        [x + 0.34, tip_y - 0.08, 0],
    ]
    tip = Polygon(*pts, color=tcr_color, stroke_width=3, fill_color=tcr_color, fill_opacity=0.35)

    tl_x = x - 0.36
    tr_x = x + 0.36
    tail_l = Line([tl_x, y_bot, 0], [tl_x, y_bot - tail_len, 0], color=tail_color, stroke_width=5)
    tail_r = Line([tr_x, y_bot, 0], [tr_x, y_bot - tail_len, 0], color=tail_color, stroke_width=5)
    partner_l = RoundedRectangle(corner_radius=0.06, width=0.14, height=0.46,
                                 color=tail_color, stroke_width=2.5,
                                 fill_color=tail_color, fill_opacity=0.25).move_to([tl_x, y_bot + 0.23, 0])
    partner_r = RoundedRectangle(corner_radius=0.06, width=0.14, height=0.46,
                                 color=tail_color, stroke_width=2.5,
                                 fill_color=tail_color, fill_opacity=0.25).move_to([tr_x, y_bot + 0.23, 0])
    phos = VGroup()
    if has_phosphates:
        for px in (tl_x, tr_x):
            phos.add(make_phos([px, y_bot - tail_len * 0.42, 0], radius=0.14))
            phos.add(make_phos([px, y_bot - tail_len * 0.84, 0], radius=0.14))
    g = VGroup(l_chain, r_chain, tip, partner_l, partner_r, tail_l, tail_r, phos)
    g.tip = tip
    g.tails = VGroup(tail_l, tail_r)
    g.phosphates = phos
    g.chains = VGroup(l_chain, r_chain, partner_l, partner_r)
    return g


def make_cd28(x, y_bot, height=1.20, tail_len=0.95, has_phosphates=False, color=CD28_GREEN):
    """Green CD28 co-stimulatory dimer on T-cell membrane with optional tail phosphate."""
    stalk = RoundedRectangle(corner_radius=0.08, width=0.22, height=height,
                             color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.24).move_to([x, y_bot + height / 2.0, 0])
    cup = Arc(radius=0.28, start_angle=PI, angle=PI,
              arc_center=[x, y_bot + height + 0.08, 0], color=color, stroke_width=5)
    tail = Line([x, y_bot, 0], [x, y_bot - tail_len, 0], color=color, stroke_width=5)
    phos = VGroup()
    if has_phosphates:
        phos.add(make_phos([x, y_bot - tail_len * 0.58, 0], radius=0.14))
    g = VGroup(stalk, cup, tail, phos)
    g.stalk, g.cup, g.tail, g.phosphates = stalk, cup, tail, phos
    return g


def make_b7(x, y_top, height=1.15, color=B7_EMERALD):
    """Emerald B7 protein extending downward from the presenting-cell membrane."""
    stalk = Line([x, y_top, 0], [x, y_top - height + 0.22, 0], color=color, stroke_width=5)
    head = RoundedRectangle(corner_radius=0.16, width=0.42, height=0.42,
                            color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.84).move_to([x, y_top - height + 0.14, 0])
    g = VGroup(stalk, head)
    g.stalk, g.head = stalk, head
    return g


def make_ctla4_dimer(x, y_bot, height=1.45, spread=0.50, color=CTLA4_CRIMSON):
    """Crimson CTLA-4 dimer with twin arms that bridge two B7 ligands at once."""
    base = Line([x, y_bot, 0], [x, y_bot + 0.52, 0], color=color, stroke_width=5)
    arm_l = Line([x, y_bot + 0.48, 0], [x - spread, y_bot + height, 0], color=color, stroke_width=5)
    arm_r = Line([x, y_bot + 0.48, 0], [x + spread, y_bot + height, 0], color=color, stroke_width=5)
    cup_l = Arc(radius=0.25, start_angle=PI, angle=PI,
                arc_center=[x - spread, y_bot + height + 0.08, 0], color=color, stroke_width=5)
    cup_r = Arc(radius=0.25, start_angle=PI, angle=PI,
                arc_center=[x + spread, y_bot + height + 0.08, 0], color=color, stroke_width=5)
    tail = Line([x, y_bot, 0], [x, y_bot - 0.36, 0], color=color, stroke_width=4)
    g = VGroup(base, arm_l, arm_r, cup_l, cup_r, tail)
    g.cups = VGroup(cup_l, cup_r)
    return g


def make_pd1(x, y_bot, height=0.80, tail_len=1.45, has_phosphates=True, color=PD1_MAGENTA):
    """Magenta PD-1 receptor with cytoplasmic ITSM tail carrying two phosphates."""
    stalk = RoundedRectangle(corner_radius=0.08, width=0.20, height=height,
                             color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.25).move_to([x, y_bot + height / 2.0, 0])
    cup = Arc(radius=0.24, start_angle=PI, angle=PI,
              arc_center=[x, y_bot + height + 0.06, 0], color=color, stroke_width=5)
    tail = Line([x, y_bot, 0], [x, y_bot - tail_len, 0], color=color, stroke_width=5)
    phos = VGroup()
    if has_phosphates:
        phos.add(make_phos([x, y_bot - tail_len * 0.42, 0], radius=0.15))
        phos.add(make_phos([x, y_bot - tail_len * 0.84, 0], radius=0.15))
    g = VGroup(stalk, cup, tail, phos)
    g.tail, g.phosphates, g.cup = tail, phos, cup
    return g


def make_pdl1(x, y_top, height=0.68, color=PDL1_PLUM):
    """Plum PD-L1 ligand on tissue or tumour cell."""
    stalk = Line([x, y_top, 0], [x, y_top - height + 0.18, 0], color=color, stroke_width=5)
    head = RoundedRectangle(corner_radius=0.14, width=0.38, height=0.34,
                            color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.85).move_to([x, y_top - height + 0.10, 0])
    return VGroup(stalk, head)


def make_shp2(dock_pos, arm_angle_deg=-130.0, arm_len=0.95, color=SHP2_ORANGE):
    """Burnt-orange SHP-2 with two SH2 cups and an articulated catalytic working arm."""
    cx, cy = dock_pos[0], dock_pos[1]
    body = RoundedRectangle(corner_radius=0.18, width=0.72, height=0.88,
                            color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.26).move_to([cx, cy, 0])
    sh2_top = Arc(radius=0.20, start_angle=PI / 2, angle=PI,
                  arc_center=[cx + 0.45, cy + 0.325, 0], color=color, stroke_width=5)
    sh2_bot = Arc(radius=0.20, start_angle=PI / 2, angle=PI,
                  arc_center=[cx + 0.45, cy - 0.325, 0], color=color, stroke_width=5)
    pivot = np.array([cx - 0.18, cy - 0.34, 0.0])
    rad = np.deg2rad(arm_angle_deg)
    tip = pivot + arm_len * np.array([np.cos(rad), np.sin(rad), 0.0])
    arm = Line(pivot, tip, color=color, stroke_width=6)
    eraser = Circle(radius=0.20, color=color, stroke_width=3.5,
                    fill_color=color, fill_opacity=0.88).move_to(tip)
    g = VGroup(body, sh2_top, sh2_bot, arm, eraser)
    g.body, g.sh2_top, g.sh2_bot, g.arm, g.eraser = body, sh2_top, sh2_bot, arm, eraser
    return g


def make_antibody_y(center, angle=0.0, scale=0.75, color=AB_CYAN):
    """Cyan Y-shaped checkpoint-blocking antibody."""
    stem = Line([0, 0, 0], [0, -0.55 * scale, 0], color=color, stroke_width=5.5)
    arm_l = Line([0, 0, 0], [-0.42 * scale, 0.45 * scale, 0], color=color, stroke_width=5.5)
    arm_r = Line([0, 0, 0], [0.42 * scale, 0.45 * scale, 0], color=color, stroke_width=5.5)
    g = VGroup(stem, arm_l, arm_r).move_to(center)
    if angle:
        g.rotate(angle)
    return g


def make_car_receptor(x, y_bot, tip_h=1.85, has_costim=False, lit=False,
                      tip_color=AB_CYAN, zeta_len=1.05):
    """Continuous synthetic CAR chain anchored in the membrane at y_bot."""
    tip_stem = Line([x, y_bot, 0], [x, y_bot + tip_h, 0], color=tip_color, stroke_width=5.5)
    cup = Arc(radius=0.34, start_angle=PI, angle=PI,
              arc_center=[x, y_bot + tip_h + 0.18, 0], color=tip_color, stroke_width=6)
    tip_glow = Circle(radius=0.14, color=PEPTIDE_WHITE, stroke_width=2.5,
                      fill_color=PEPTIDE_WHITE, fill_opacity=0.85).move_to([x, y_bot + tip_h + 0.08, 0])

    zeta_top = y_bot
    costim_grp = VGroup()
    if has_costim:
        cbox = RoundedRectangle(corner_radius=0.10, width=0.52, height=0.56,
                                color=CD28_GREEN, stroke_width=3,
                                fill_color=CD28_GREEN, fill_opacity=0.35 if lit else 0.18
                                ).move_to([x, y_bot - 0.30, 0])
        costim_grp.add(cbox)
        if lit:
            costim_grp.add(make_phos([x + 0.44, y_bot - 0.30, 0], radius=0.13))
        zeta_top = y_bot - 0.58

    zeta_tail = Line([x, zeta_top, 0], [x, zeta_top - zeta_len, 0], color=ZETA_TEAL, stroke_width=6)
    itams = VGroup()
    for frac in (0.24, 0.54, 0.84):
        py = zeta_top - zeta_len * frac
        if lit:
            itams.add(make_phos([x + 0.34, py, 0], radius=0.13))
        else:
            itams.add(Circle(radius=0.12, color=PHOS_GOLD, stroke_width=3,
                             fill_color=BG, fill_opacity=0.85).move_to([x + 0.34, py, 0]))
    g = VGroup(tip_stem, cup, tip_glow, costim_grp, zeta_tail, itams)
    g.tip = VGroup(tip_stem, cup, tip_glow)
    g.tip_stem = tip_stem
    g.costim = costim_grp
    g.zeta_tail = zeta_tail
    g.itams = itams
    return g


# ------------------------------------------------------------------ S00 Title
class S00Title(TitleCard):
    LESSON = "Antigen Receptors and Checkpoints"
    TITLE = "Signal Two and Two Brakes"


# ------------------------------------------------------------------ S01 Link Hook
class S01LinkHook(SpokenScene):
    def construct(self):
        act_lvl = ValueTracker(0.20)
        top_cell = make_cell_band(2.05, is_top=True, color=MHC_SLATE, fill_opacity=0.13,
                                  label="presenting cell", label_pos=[-4.4, 2.85, 0])
        bot_fill = always_redraw(lambda: Rectangle(
            width=12.7, height=2.20, stroke_width=0,
            fill_color=interpolate_color(ManimColor(TCR_BLUE), ManimColor(PHOS_GOLD), 0.28 * act_lvl.get_value()),
            fill_opacity=0.12 + 0.16 * act_lvl.get_value(),
        ).move_to([0.0, -2.45, 0.0]).set_z_index(-5))
        bot_mem = always_redraw(lambda: Line(
            [-6.35, -1.35, 0], [6.35, -1.35, 0],
            color=interpolate_color(ManimColor(TCR_BLUE), ManimColor(PHOS_GOLD), 0.35 * act_lvl.get_value()),
            stroke_width=4.5 + 2.5 * act_lvl.get_value(),
        ).set_z_index(-2))
        t_lab = T("T cell", 26, TEXT, weight=BOLD).move_to([-5.1, -2.95, 0])

        mhc = make_mhc_peptide(0.0, 2.05, peptide_color=PEPTIDE_WHITE)
        tcr = make_tcr_complex(0.0, -1.35, has_phosphates=False, chain_h=1.35, tail_len=1.08)
        tcr_lab = place_label(T("TCR", 28, TCR_BLUE, weight=BOLD), tcr.chains, dirs=(LEFT,), buff=0.3)
        mhc_lab = place_label(T("MHC", 28, MHC_SLATE, weight=BOLD), mhc.cup, dirs=(LEFT,), buff=0.3)

        self.add(top_cell, bot_fill, bot_mem, t_lab, mhc, tcr, tcr_lab, mhc_lab, scope_tag("schematic", color=TEXT))
        self.play(mhc.animate.shift(DOWN * 0.08), run_time=1.1)

        # Beat 1: two phosphates on partner tails switch receptor on
        self.at("two phosphates")
        phos = VGroup(
            make_phos([-0.36, -1.80, 0], radius=0.15),
            make_phos([-0.36, -2.26, 0], radius=0.15),
            make_phos([0.36, -1.80, 0], radius=0.15),
            make_phos([0.36, -2.26, 0], radius=0.15),
        )
        tails_lab = T("partner tails (ITAMs)", 26, ZETA_TEAL).move_to([-2.40, -2.02, 0])
        pulse_ring = Circle(radius=0.30, color=PHOS_GOLD, stroke_width=4).move_to([0.0, -2.02, 0]).set_opacity(0.9)
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.7) for p in phos], lag_ratio=0.18),
            FadeIn(tails_lab),
            act_lvl.animate.set_value(1.0),
            run_time=2.2,
        )
        self.play(pulse_ring.animate.scale(3.6).set_opacity(0.0), act_lvl.animate.set_value(0.55), run_time=2.3)
        self.remove(pulse_ring)

        # Beat 2: several TCR tips cycle shapes randomly (fixed seed RNG)
        self.at("vary almost at random")
        rng = np.random.default_rng(7)
        tcr_l = make_tcr_complex(-4.6, -1.35, tip_notch=0.24, has_phosphates=False, chain_h=1.25, tail_len=0.80)
        tcr_r = make_tcr_complex(3.4, -1.35, tip_notch=0.08, has_phosphates=False, chain_h=1.25, tail_len=0.80)
        self.play(FadeIn(tcr_l, shift=UP * 0.25), FadeIn(tcr_r, shift=UP * 0.25), run_time=0.5)
        for _ in range(4):
            n_c, n_l, n_r = rng.uniform(0.06, 0.29, size=3)
            mk_tip = lambda x, y, n: Polygon(
                [x - 0.34, y - 0.08, 0], [x - 0.26, y + 0.22, 0],
                [x - n, y + 0.09, 0], [x + n, y + 0.09, 0],
                [x + 0.26, y + 0.22, 0], [x + 0.34, y - 0.08, 0],
                color=TCR_BLUE, stroke_width=3, fill_color=TCR_BLUE, fill_opacity=0.45,
            )
            self.play(
                Transform(tcr.tip, mk_tip(0.0, 0.0, n_c)),
                Transform(tcr_l.tip, mk_tip(-4.6, -0.10, n_l)),
                Transform(tcr_r.tip, mk_tip(3.4, -0.10, n_r)),
                run_time=0.34,
            )

        # Beat 3: one locks onto self peptide
        self.at("some recognize our own")
        self_badge = boxed_label("self peptide", CAUTION_AMBER, size=26).move_to([2.25, 1.25, 0])
        tall_tcr = make_tcr_complex(0.0, -1.35, tip_notch=0.16, has_phosphates=False, chain_h=2.07, tail_len=1.08)
        self.play(
            FadeOut(tcr_l), FadeOut(tcr_r),
            mhc.peptide.animate.set_color(CAUTION_AMBER),
            Transform(tcr, tall_tcr),
            tcr_lab.animate.next_to(tall_tcr.chains, LEFT, buff=0.3),
            FadeIn(self_badge, shift=LEFT * 0.15),
            run_time=2.3,
        )

        # Beat 4: caution glow around T cell
        self.at("What stops")
        caution_line = Line([-6.35, -1.35, 0], [6.35, -1.35, 0], color=CAUTION_AMBER, stroke_width=7).set_z_index(-1)
        q_badge = boxed_label("What stops attack on healthy tissue?", CAUTION_AMBER, size=28).move_to([0.0, -3.05, 0])
        self.play(
            Create(caution_line),
            act_lvl.animate.set_value(1.0),
            FadeIn(q_badge, shift=UP * 0.15),
            run_time=2.5,
        )
        caution_fill = Rectangle(width=12.7, height=2.20, stroke_width=0,
                                 fill_color=CAUTION_AMBER, fill_opacity=0.14).move_to([0.0, -2.45, 0.0]).set_z_index(-4)
        self.play(FadeIn(caution_fill), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ S02 Signal Two
class S02SignalTwo(SpokenScene):
    def construct(self):
        act_lvl = ValueTracker(0.85)

        top_cell = make_cell_band(2.05, is_top=True, color=MHC_SLATE, fill_opacity=0.13,
                                  label="presenting cell", label_pos=[-4.4, 2.85, 0])
        bot_fill = always_redraw(lambda: Rectangle(
            width=12.7, height=2.20, stroke_width=0,
            fill_color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            fill_opacity=0.14 + 0.15 * act_lvl.get_value(),
        ).move_to([0.0, -2.45, 0.0]).set_z_index(-5))
        bot_mem = always_redraw(lambda: Line(
            [-6.35, -1.35, 0], [6.35, -1.35, 0],
            color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            stroke_width=4.5 + 2.5 * act_lvl.get_value(),
        ).set_z_index(-2))
        t_lab = T("T cell", 26, TEXT, weight=BOLD).move_to([-5.1, -2.95, 0])

        mhc = make_mhc_peptide(-2.6, 2.05)
        tcr = make_tcr_complex(-2.6, -1.35, has_phosphates=True, chain_h=2.02, tail_len=1.05)
        sig1_lab = T("signal 1", 26, PHOS_GOLD, weight=BOLD).move_to([-4.65, -1.85, 0])

        cd28 = make_cd28(1.3, -1.35, height=1.25, tail_len=0.95, has_phosphates=False)
        gap_line = DashedLine([1.3, 0.05, 0], [1.3, 1.98, 0], color=DIM_GREY, stroke_width=3.5)
        empty_lab = T("no signal 2", 26, TEXT).move_to([2.55, 1.35, 0])

        self.add(top_cell, bot_fill, bot_mem, t_lab, mhc, tcr, sig1_lab, cd28,
                 gap_line, empty_lab, scope_tag("schematic"))
        self.play(act_lvl.animate.set_value(0.55), run_time=1.3)

        # Beat 1: does not trust signal 1 alone
        self.at("signal 1 alone")
        cd28_probe = make_cd28(1.3, -1.35, height=1.43, tail_len=0.95, has_phosphates=False)
        self.play(act_lvl.animate.set_value(0.35),
                  Transform(cd28, cd28_probe), run_time=1.8)

        # Beat 2: without a second cue -> anergy (T-cell dims smoothly to flat grey)
        self.at("Without a second")
        cd28_rest = make_cd28(1.3, -1.35, height=1.25, tail_len=0.95, has_phosphates=False)
        self.play(Transform(cd28, cd28_rest),
                  act_lvl.animate.set_value(0.15), run_time=2.2)

        self.at("fall into")
        anergy_badge = boxed_label("anergy (cultured cells)", TEXT, size=28, stroke=2.5, fill_opacity=0.16).move_to([1.3, -2.90, 0])
        self.play(
            act_lvl.animate.set_value(0.0),
            FadeIn(anergy_badge, shift=UP * 0.1),
            run_time=3.4,
        )

        # Beat 3: Full activation needs CD28 to grip B7
        self.at("Full activation needs")
        b7_main = make_b7(1.3, 2.05, height=1.15)
        b7_main.save_state()
        b7_main.shift(UP * 0.7).set_opacity(0)
        b7_lab = T("B7", 28, B7_EMERALD, weight=BOLD).move_to([2.15, 1.45, 0])
        cd28_tall = make_cd28(1.3, -1.35, height=1.87, tail_len=0.95, has_phosphates=False)
        cd28_lab = place_label(T("CD28", 28, CD28_GREEN, weight=BOLD), cd28_tall.stalk, dirs=(RIGHT,), buff=0.25)
        cd28_phos = make_phos([1.3, -1.90, 0], radius=0.15)
        active_badge = boxed_label("full activation", PHOS_GOLD, size=28).move_to([1.3, -2.90, 0])

        self.play(FadeOut(gap_line), FadeOut(empty_lab), FadeOut(anergy_badge), run_time=0.6)
        self.play(b7_main.animate.restore(), FadeIn(b7_lab), FadeIn(cd28_lab), run_time=1.6)
        self.play(
            Transform(cd28, cd28_tall),
            FadeIn(cd28_phos, scale=0.7),
            act_lvl.animate.set_value(1.0),
            FadeIn(active_badge),
            run_time=2.2,
        )

        # Beat 4: Presenting cells raise B7 when they sense infection
        self.at("Presenting cells raise")
        inf_badge = boxed_label("infection sensed -> more B7", B7_EMERALD, size=25).move_to([3.55, 2.85, 0])
        b7_extra = make_b7(3.15, 2.05, height=1.15)
        b7_extra.save_state()
        b7_extra.shift(UP * 0.6).set_opacity(0)
        self.play(
            FadeIn(inf_badge, shift=DOWN * 0.1),
            b7_lab.animate.move_to([3.95, 1.45, 0]),
            run_time=0.6,
        )
        self.play(
            b7_extra.animate.restore(),
            run_time=2.2,
        )
        self.finish()


# ------------------------------------------------------------------ S03 CTLA-4 Outside
class S03Ctla4Outside(SpokenScene):
    def construct(self):
        act_lvl = ValueTracker(0.55)
        top_cell = make_cell_band(2.05, is_top=True, color=MHC_SLATE, fill_opacity=0.13,
                                  label="presenting cell", label_pos=[-4.4, 2.85, 0])
        bot_fill = always_redraw(lambda: Rectangle(
            width=12.7, height=2.20, stroke_width=0,
            fill_color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            fill_opacity=0.14 + 0.14 * act_lvl.get_value(),
        ).move_to([0.0, -2.45, 0.0]).set_z_index(-5))
        bot_mem = always_redraw(lambda: Line(
            [-6.35, -1.35, 0], [6.35, -1.35, 0],
            color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            stroke_width=4.5 + 2.0 * act_lvl.get_value(),
        ).set_z_index(-2))
        t_lab = T("T cell", 26, TEXT, weight=BOLD).move_to([-5.1, -2.95, 0])

        mhc = make_mhc_peptide(-4.0, 2.05)
        tcr = make_tcr_complex(-4.0, -1.35, has_phosphates=True, chain_h=2.02, tail_len=1.05)

        cd28 = make_cd28(-0.6, -1.35, height=1.82, tail_len=0.95, has_phosphates=True)
        cd28_lab = T("CD28", 28, CD28_GREEN, weight=BOLD).move_to([-1.55, -0.30, 0])
        b7_l = make_b7(-0.6, 2.05, height=1.15)
        b7_r = make_b7(2.4, 2.05, height=1.15)
        b7_lab = T("B7", 28, B7_EMERALD, weight=BOLD).move_to([3.20, 1.45, 0])

        self.add(top_cell, bot_fill, bot_mem, t_lab, mhc, tcr, cd28, cd28_lab, b7_l, b7_r, b7_lab, scope_tag("schematic"))
        self.play(act_lvl.animate.set_value(1.0), run_time=1.6)

        # Beat 1: T cell puts up CTLA-4 from inside
        self.at("puts up")
        ctla4 = make_ctla4_dimer(1.5, -1.35, height=1.40, spread=0.45)
        ctla4.save_state()
        ctla4.shift(DOWN * 1.1).set_opacity(0)
        ctla4_lab = T("CTLA-4", 28, CTLA4_CRIMSON, weight=BOLD).move_to([3.05, -0.45, 0])
        self.play(ctla4.animate.restore(), FadeIn(ctla4_lab), run_time=2.4)

        # Beat 2: resembles CD28 and binds the same B7
        self.at("resembles CD28")
        tall_ctla4 = make_ctla4_dimer(1.5, -1.35, height=1.85, spread=0.45)
        self.play(
            Transform(ctla4, tall_ctla4),
            act_lvl.animate.set_value(0.75),
            run_time=3.5,
        )

        # Beat 3: brake outside (placed cleanly above schematic and clear of endosome/CTLA-4 label)
        self.at("But it is")
        brake_badge = boxed_label("brake: outside", CTLA4_CRIMSON, size=26).move_to([4.65, -2.45, 0])
        self.play(FadeIn(brake_badge, shift=UP * 0.1), act_lvl.animate.set_value(0.55), run_time=2.4)

        # Beat 4: dimer grips two B7 at once
        self.at("dimer grips two")
        wide_ctla4 = make_ctla4_dimer(1.5, -1.35, height=2.25, spread=0.85)
        self.play(
            Transform(ctla4, wide_ctla4),
            b7_l.animate.move_to([0.65, 1.48, 0]),
            b7_r.animate.move_to([2.35, 1.48, 0]),
            b7_lab.animate.move_to([3.20, 1.35, 0]),
            run_time=2.2,
        )

        # Beat 5: about 10x tighter in solution
        self.at("about ten times")
        tight_badge = boxed_label("about 10× tighter in solution", CTLA4_CRIMSON, size=24).move_to([3.3, 2.85, 0])
        self.play(FadeIn(tight_badge, shift=DOWN * 0.1), act_lvl.animate.set_value(0.35), run_time=2.2)

        # Beat 6: CD28 is left empty & gold tail phosphates fade
        self.at("So CD28 is left")
        empty_dash = DashedLine([-0.6, 0.25, 0], [-0.6, 1.98, 0], color=DIM_GREY, stroke_width=3.5)
        empty_txt = T("empty", 26, TEXT).move_to([-1.65, 1.35, 0])
        short_cd28 = make_cd28(-0.6, -1.35, height=1.34, tail_len=0.95, has_phosphates=False)
        self.play(
            Transform(VGroup(cd28.stalk, cd28.cup), VGroup(short_cd28.stalk, short_cd28.cup)),
            FadeOut(cd28.phosphates),
            Create(empty_dash),
            FadeIn(empty_txt),
            act_lvl.animate.set_value(0.15),
            run_time=2.4,
        )

        # Beat 7: drags B7 away to be destroyed in endosome
        self.at("drags B7 away")
        endo = Circle(radius=0.72, color=CTLA4_CRIMSON, stroke_width=3.5,
                      fill_color=CTLA4_CRIMSON, fill_opacity=0.14).move_to([1.5, -2.25, 0])
        endo_lab = T("endosome", 24, TEXT).move_to([1.5, -3.22, 0])
        self.play(FadeIn(endo), FadeIn(endo_lab), FadeOut(b7_lab), run_time=0.6)
        self.play(
            ctla4.animate.move_to([1.5, -2.05, 0]).scale(0.55),
            b7_l.animate.move_to([1.22, -2.25, 0]).scale(0.52),
            b7_r.animate.move_to([1.78, -2.25, 0]).scale(0.52),
            ctla4_lab.animate.move_to([3.00, -1.58, 0]),
            run_time=1.8,
        )
        self.play(b7_l.animate.scale(0.25).set_opacity(0.15),
                  b7_r.animate.scale(0.25).set_opacity(0.15), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ Helper for S04/S05/S06 zoomed inside world
def build_pd1_inside_world(show_pdl1=True, show_pd1_phos=True, shp2_pos=(1.6, -1.90, 0)):
    """Shared zoomed-in cytoplasm builder for s04, s05, and s06."""
    top_cell = make_cell_band(2.00, is_top=True, color=PDL1_PLUM if show_pdl1 else MHC_SLATE,
                              fill_opacity=0.14, outer_y=2.82,
                              label="tissue or tumour cell", label_pos=[-3.8, 2.38, 0])
    bot_fill = Rectangle(width=12.7, height=4.15, stroke_width=0,
                         fill_color=TCR_BLUE, fill_opacity=0.16).move_to([0.0, -1.475, 0.0]).set_z_index(-5)
    bot_mem = Line([-6.35, 0.60, 0], [6.35, 0.60, 0], color=TCR_BLUE, stroke_width=4.5).set_z_index(-2)
    t_lab = T("T cell", 26, TEXT, weight=BOLD).move_to([-5.3, -3.10, 0])

    mhc = make_mhc_peptide(-4.2, 2.00, stalk_h=0.32)
    tcr = make_tcr_complex(-4.2, 0.60, has_phosphates=True, chain_h=0.58, tail_len=1.45)

    b7 = make_b7(-1.5, 2.00, height=0.65)
    cd28 = make_cd28(-1.5, 0.60, height=0.55, tail_len=1.40, has_phosphates=True)
    cd28_lab = T("CD28", 26, CD28_GREEN, weight=BOLD).move_to([-2.4, 0.95, 0])

    pd1 = make_pd1(1.6, 0.60, height=0.55, tail_len=1.55, has_phosphates=show_pd1_phos)
    pd1_lab = T("PD-1", 28, PD1_MAGENTA, weight=BOLD).move_to([2.65, 0.95, 0])
    itsm_lab = T("ITSM tail", 26, PD1_MAGENTA).move_to([3.05, -0.35, 0])

    pdl1 = make_pdl1(1.6, 2.00, height=0.68) if show_pdl1 else VGroup()
    pdl1_lab = T("PD-L1", 28, PDL1_PLUM, weight=BOLD).move_to([2.65, 1.65, 0]) if show_pdl1 else VGroup()

    shp2 = make_shp2(shp2_pos, arm_angle_deg=-130.0, arm_len=0.95) if shp2_pos is not None else VGroup()
    shp2_lab = T("SHP-2", 28, SHP2_ORANGE, weight=BOLD).move_to([shp2_pos[0] + 1.15, shp2_pos[1], 0]) if shp2_pos is not None else VGroup()

    g = VGroup(top_cell, bot_fill, bot_mem, t_lab, mhc, tcr, b7, cd28, cd28_lab,
               pd1, pd1_lab, itsm_lab, pdl1, pdl1_lab, shp2, shp2_lab, scope_tag("schematic"))
    g.top_cell = top_cell
    g.bot_fill, g.bot_mem = bot_fill, bot_mem
    g.tcr, g.cd28, g.pd1 = tcr, cd28, pd1
    g.pdl1, g.pdl1_lab = pdl1, pdl1_lab
    g.itsm_lab = itsm_lab
    g.shp2, g.shp2_lab = shp2, shp2_lab
    return g


# ------------------------------------------------------------------ S04 Predict PD-1
class S04PredictPd1(SpokenScene):
    def construct(self):
        w = build_pd1_inside_world(show_pdl1=False, show_pd1_phos=False, shp2_pos=None)
        w.top_cell.label.set_opacity(0)
        w.itsm_lab.set_opacity(0)
        w.pd1.tail.put_start_and_end_on([1.6, 0.60, 0], [1.6, 0.25, 0])
        self.add(w)
        self.play(w.pd1.tail.animate.put_start_and_end_on([1.6, 0.60, 0], [1.6, -0.95, 0]), run_time=1.4)

        # Beat 1: second brake PD-1 works from inside
        self.at("works from inside")
        inside_badge = boxed_label("brake: inside", PD1_MAGENTA, size=26).move_to([4.5, -2.55, 0])
        self.play(FadeIn(inside_badge), w.bot_fill.animate.set_fill(TCR_BLUE, opacity=0.22), run_time=1.8)

        # Beat 2: healthy cells and tumours display PD-L1
        self.at("Many healthy cells")
        pdl1 = make_pdl1(1.6, 2.00, height=0.68)
        pdl1.save_state()
        pdl1.shift(UP * 0.75).set_opacity(0)
        pdl1_lab = T("PD-L1", 28, PDL1_PLUM, weight=BOLD).move_to([2.65, 1.65, 0])
        self.play(
            w.top_cell.membrane.animate.set_color(PDL1_PLUM),
            w.top_cell.fill_rect.animate.set_fill(PDL1_PLUM, opacity=0.24),
            w.top_cell.label.animate.set_opacity(1),
            run_time=2.6,
        )
        self.play(
            pdl1.animate.restore(),
            FadeIn(pdl1_lab),
            w.top_cell.fill_rect.animate.set_fill(PDL1_PLUM, opacity=0.14),
            w.bot_fill.animate.set_fill(TCR_BLUE, opacity=0.12),
            run_time=3.5,
        )

        # Beat 3: two phosphates appear on PD-1's tail
        self.at("two phosphates appear")
        p1 = make_phos([1.6, 0.60 - 1.55 * 0.42, 0], radius=0.15)
        p2 = make_phos([1.6, 0.60 - 1.55 * 0.84, 0], radius=0.15)
        ring = Circle(radius=0.35, color=PHOS_GOLD, stroke_width=6).move_to([1.6, -0.35, 0])
        self.play(FadeIn(p1, scale=0.6), FadeIn(p2, scale=0.6),
                  w.itsm_lab.animate.set_opacity(1),
                  w.bot_fill.animate.set_fill(TCR_BLUE, opacity=0.24),
                  ring.animate.scale(3.4).set_opacity(0.0), run_time=3.2)
        self.remove(ring)

        # Beat 4: SHP-2 rises smoothly across cytoplasm toward them
        self.at("They call in")
        shp2 = make_shp2((1.6, -1.90, 0), arm_angle_deg=-130.0, arm_len=0.95)
        shp2.save_state()
        shp2.shift(DOWN * 1.4).set_opacity(0)
        shp2_lab = T("SHP-2", 28, SHP2_ORANGE, weight=BOLD).move_to([2.75, -1.90, 0])
        self.play(FadeOut(inside_badge), run_time=0.4)
        self.play(shp2.animate.restore(), FadeIn(shp2_lab),
                  w.bot_fill.animate.set_fill(TCR_BLUE, opacity=0.15), run_time=4.2)

        # Beat 5: Predict question banner at top
        self.at("So does it strip")
        q = question_card("SHP-2 strips phosphates. Does it strip these two?",
                          y=3.20, left=-5.9, max_w=11.8, size=30)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=2.2)
        self.finish()


# ------------------------------------------------------------------ S05 Pause
class S05Pause(PredictPause):
    QUESTION = "SHP-2 strips phosphates. Does it strip these two?"
    CARD = {"y": 3.20, "left": -5.9, "max_w": 11.8, "size": 30}
    RING_AT = (5.8, -2.20, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_pd1_inside_world(show_pdl1=True, show_pd1_phos=True, shp2_pos=(1.6, -1.90, 0))


# ------------------------------------------------------------------ S06 Reveal PD-1
class S06RevealPd1(SpokenScene):
    def construct(self):
        w = build_pd1_inside_world(show_pdl1=True, show_pd1_phos=True, shp2_pos=(1.6, -1.90, 0))
        q = question_card("SHP-2 strips phosphates. Does it strip these two?",
                          y=3.20, left=-5.9, max_w=11.8, size=30)
        self.add(w, q)

        # Beat 1: No, because those two phosphates are its anchor
        self.at("No")
        anchor_lab = boxed_label("docking site, not the target", PHOS_GOLD, size=28).move_to([0.0, 3.20, 0])
        self.play(swap(q, anchor_lab), run_time=1.0)
        self.play(w.shp2.animate.shift(UP * 0.40 + LEFT * 0.45), w.shp2_lab.animate.shift(UP * 0.40 + LEFT * 0.45), run_time=2.8)

        # Beat 2: SHP-2 grips both with two SH2 domains
        self.at("grips both")
        dock_target = np.array([1.15, -0.38, 0.0])
        sh2_tag = T("2 SH2 grips", 24, SHP2_ORANGE, weight=BOLD).move_to([2.95, 0.22, 0])
        self.play(
            w.shp2.animate.shift(dock_target - w.shp2.body.get_center()),
            w.shp2_lab.animate.move_to([2.75, -1.10, 0]),
            w.itsm_lab.animate.move_to([4.15, -0.35, 0]),
            run_time=2.0,
        )
        self.play(FadeIn(sh2_tag), w.bot_fill.animate.set_fill(TCR_BLUE, opacity=0.22), run_time=1.8)

        # Beat 3: working end swings sideways using computed circular arc + length
        self.at("Its working end")
        theta = ValueTracker(-130.0)
        arm_len = ValueTracker(0.95)
        pivot = w.shp2.body.get_center() + np.array([-0.18, -0.34, 0.0])
        w.shp2.arm.add_updater(
            lambda m: m.put_start_and_end_on(
                pivot,
                pivot + arm_len.get_value() * np.array([np.cos(np.deg2rad(theta.get_value())),
                                                        np.sin(np.deg2rad(theta.get_value())), 0.0]),
            )
        )
        w.shp2.eraser.add_updater(
            lambda m: m.move_to(
                pivot + arm_len.get_value() * np.array([np.cos(np.deg2rad(theta.get_value())),
                                                        np.sin(np.deg2rad(theta.get_value())), 0.0])
            )
        )
        self.play(theta.animate.set_value(-172.0), arm_len.animate.set_value(2.45),
                  w.bot_fill.animate.set_fill(TCR_BLUE, opacity=0.14), run_time=2.4)

        # Beat 4: erases activating phosphates on CD28 then TCR partner tails, progressively dimming cell
        self.at("erases activating phosphates")
        self.play(
            theta.animate.set_value(-192.0),
            arm_len.animate.set_value(2.52),
            FadeOut(w.cd28.phosphates, scale=0.4),
            w.cd28.stalk.animate.set_color(DIM_GREY),
            w.cd28.tail.animate.set_color(DIM_GREY),
            w.bot_fill.animate.set_fill(DIM_GREY, opacity=0.12),
            run_time=2.6,
        )
        self.play(
            theta.animate.set_value(-185.0),
            arm_len.animate.set_value(5.15),
            FadeOut(w.tcr.phosphates, scale=0.4),
            w.tcr.tails.animate.set_color(DIM_GREY),
            w.bot_fill.animate.set_fill(DIM_GREY, opacity=0.18),
            w.bot_mem.animate.set_color(DIM_GREY),
            run_time=2.8,
        )
        w.shp2.arm.clear_updaters()
        w.shp2.eraser.clear_updaters()

        # Beat 5: dims the cell from inside + recall CTLA-4 outside
        self.at("dims the cell")
        recall_box = RoundedRectangle(corner_radius=0.14, width=2.9, height=1.40,
                                      color=CTLA4_CRIMSON, stroke_width=2.5,
                                      fill_color=BG, fill_opacity=0.92).move_to([4.75, -2.25, 0])
        recall_ttl = T("recall: CTLA-4", 24, CTLA4_CRIMSON, weight=BOLD).move_to([4.75, -1.85, 0])
        recall_sub = T("outside (for B7)", 24, TEXT).move_to([4.75, -2.45, 0])
        dim_badge = boxed_label("cell dimmed from inside", TEXT, size=26).move_to([-1.6, -3.05, 0])
        self.play(
            FadeIn(dim_badge),
            FadeIn(recall_box), FadeIn(recall_ttl), FadeIn(recall_sub),
            run_time=1.4,
        )
        self.finish()


# ------------------------------------------------------------------ S07 Checkpoint Drugs
class S07CheckpointDrugs(SpokenScene):
    def construct(self):
        rule_ban = boxed_label("Rule: full activation needs signal 2; checkpoints brake outside or inside",
                               PHOS_GOLD, size=25).move_to([0.0, 3.22, 0])
        top_cell = make_cell_band(1.80, is_top=True, color=PDL1_PLUM, fill_opacity=0.13, outer_y=2.76,
                                  label="tumour / presenting cell", label_pos=[-3.9, 2.28, 0])
        act_lvl = ValueTracker(0.05)
        bot_fill = always_redraw(lambda: Rectangle(
            width=12.7, height=2.20, stroke_width=0,
            fill_color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            fill_opacity=0.14 + 0.16 * act_lvl.get_value(),
        ).move_to([0.0, -2.45, 0.0]).set_z_index(-5))
        bot_mem = always_redraw(lambda: Line(
            [-6.35, -1.35, 0], [6.35, -1.35, 0],
            color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            stroke_width=4.5 + 2.5 * act_lvl.get_value(),
        ).set_z_index(-2))
        t_lab = T("patient's T cell", 26, TEXT, weight=BOLD).move_to([-4.90, -3.02, 0])

        cd28 = make_cd28(-4.4, -1.35, height=1.10, tail_len=0.80, has_phosphates=False)
        cd28_lab = T("CD28", 24, CD28_GREEN, weight=BOLD).move_to([-5.25, -0.75, 0])
        b7 = make_b7(-2.3, 1.80, height=1.18)
        ctla4 = make_ctla4_dimer(-2.3, -1.35, height=1.82, spread=0.45)
        ctla4_lab = T("CTLA-4", 26, CTLA4_CRIMSON, weight=BOLD).move_to([-1.15, -0.70, 0])

        mhc = make_mhc_peptide(0.3, 1.80)
        tcr = make_tcr_complex(0.3, -1.35, has_phosphates=False, chain_h=1.40, tail_len=0.85)

        pdl1 = make_pdl1(3.2, 1.80, height=1.15)
        pd1 = make_pd1(3.2, -1.35, height=1.85, tail_len=0.85, has_phosphates=True)
        pd1_lab = T("PD-1", 26, PD1_MAGENTA, weight=BOLD).move_to([4.25, -0.75, 0])
        shp2 = make_shp2((2.70, -1.90, 0), arm_angle_deg=-165.0, arm_len=1.20)

        self.add(top_cell, bot_fill, bot_mem, t_lab, cd28, cd28_lab, b7, ctla4, ctla4_lab,
                 mhc, tcr, pdl1, pd1, pd1_lab, shp2, scope_tag("schematic"))
        self.play(act_lvl.animate.set_value(0.25), run_time=1.8)

        # Beat 1: second core rule + highlight CTLA-4 outside / PD-1 inside
        self.at("Full activation needs")
        self.play(FadeIn(rule_ban, shift=DOWN * 0.1), act_lvl.animate.set_value(0.10), run_time=1.8)
        self.at("outside")
        out_tag = boxed_label("outside brake", CTLA4_CRIMSON, size=24).move_to([-2.3, -2.25, 0])
        self.play(FadeIn(out_tag, shift=UP * 0.08), Indicate(VGroup(ctla4, b7), color=CTLA4_CRIMSON, scale_factor=1.06), run_time=0.8)
        self.at("inside")
        in_tag = boxed_label("inside brake", PD1_MAGENTA, size=24).move_to([4.85, -2.05, 0])
        self.play(FadeIn(in_tag, shift=UP * 0.08), Indicate(VGroup(pd1, shp2), color=PD1_MAGENTA, scale_factor=1.06), run_time=1.2)

        # Beat 2: checkpoint is a brake
        self.at("A checkpoint is")
        self.play(
            Indicate(VGroup(ctla4, pd1), color=CAUTION_AMBER, scale_factor=1.05),
            act_lvl.animate.set_value(0.20),
            run_time=2.6,
        )

        # Beat 3: Blocking antibodies swoop in and cap CTLA-4 & PD-1 on T cells
        self.at("Blocking antibodies")
        ab_l = make_antibody_y([-2.3, 0.55, 0], angle=PI, scale=0.65, color=AB_CYAN)
        ab_l.save_state()
        ab_l.move_to([-5.6, 0.65, 0]).set_opacity(0)
        ab_r = make_antibody_y([3.2, 0.35, 0], angle=PI, scale=0.65, color=AB_CYAN)
        ab_r.save_state()
        ab_r.move_to([5.6, 0.65, 0]).set_opacity(0)
        ab_lab = T("blocking antibodies", 24, AB_CYAN, weight=BOLD).move_to([4.95, 0.95, 0])

        short_pdl1 = make_pdl1(3.2, 1.80, height=0.45).set_opacity(0.35)
        b7_at_cd28 = make_b7(-4.4, 1.80, height=1.18)
        self.play(
            FadeOut(out_tag), FadeOut(in_tag),
            ab_l.animate.restore(), ab_r.animate.restore(),
            Transform(b7, b7_at_cd28),
            Transform(pdl1, short_pdl1),
            run_time=2.2,
        )
        self.play(FadeIn(ab_lab), run_time=0.6)
        cd28_phos = make_phos([-4.4, -1.80, 0], radius=0.14)
        tcr_phos = VGroup(
            make_phos([0.3 - 0.36, -1.75, 0], radius=0.14),
            make_phos([0.3 + 0.36, -1.75, 0], radius=0.14),
        )
        tall_cd28 = make_cd28(-4.4, -1.35, height=1.65, tail_len=0.80, has_phosphates=False)
        tall_tcr = make_tcr_complex(0.3, -1.35, has_phosphates=False, chain_h=1.95, tail_len=0.85)
        self.play(
            Transform(VGroup(cd28.stalk, cd28.cup), VGroup(tall_cd28.stalk, tall_cd28.cup)),
            cd28_lab.animate.move_to([-5.25, -0.45, 0]),
            Transform(VGroup(tcr.chains, tcr.tip), VGroup(tall_tcr.chains, tall_tcr.tip)),
            shp2.animate.shift(DOWN * 1.1).set_opacity(0.0),
            FadeOut(pd1.phosphates),
            FadeIn(cd28_phos), FadeIn(tcr_phos),
            act_lvl.animate.set_value(0.65),
            run_time=3.6,
        )

        # Beat 4: keep firing
        self.at("keep firing")
        firing_badge = boxed_label("T cells keep firing", PHOS_GOLD, size=25).move_to([-1.85, -3.02, 0])
        self.play(act_lvl.animate.set_value(1.0), FadeIn(firing_badge), run_time=1.0)

        # Beat 5: healthy tissue can inflame
        self.at("though")
        risk_badge = boxed_label("risk: autoimmune inflammation", CAUTION_AMBER, size=24).move_to([2.35, -3.02, 0])
        self.play(FadeIn(risk_badge, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ S08 CAR-T
class S08CarT(SpokenScene):
    def construct(self):
        top_cell = make_cell_band(2.00, is_top=True, color=PDL1_PLUM, fill_opacity=0.13,
                                  label="tumour cell", label_pos=[-4.7, 2.85, 0])
        bot_cell = make_cell_band(-1.10, is_top=False, color=TCR_BLUE, fill_opacity=0.16,
                                  label="T cell", label_pos=[-5.2, -3.05, 0])

        tcr = make_tcr_complex(-2.2, -1.10, has_phosphates=False, chain_h=1.20, tail_len=0.90)
        no_match = T("TCR: no match", 26, TEXT).move_to([-4.2, 0.50, 0])
        tumour_mhc = make_mhc_peptide(-2.2, 2.00, peptide_color=SURF_PROT)

        self.add(top_cell, bot_cell, tcr, no_match, tumour_mhc, scope_tag("schematic"))
        self.play(Indicate(no_match, color=CAUTION_AMBER, scale_factor=1.05), run_time=0.8)

        # Beat 1: helps only if T cells already recognise the tumour
        self.at("helps only if")
        self.play(
            VGroup(tcr, tumour_mhc).animate.shift(LEFT * 1.3),
            no_match.animate.move_to([-5.15, 0.50, 0]),
            run_time=3.2,
        )

        # Beat 2: engineers build a CAR on the right
        self.at("engineers build")
        car_title = T("chimeric antigen receptor (CAR)", 28, AB_CYAN, weight=BOLD).move_to([1.9, 2.85, 0])
        eng_lab = T("engineered T cell", 26, TEXT, weight=BOLD).move_to([-4.2, -3.05, 0])
        self.play(
            tcr.animate.set_opacity(0.32),
            tumour_mhc.animate.set_opacity(0.32),
            no_match.animate.set_opacity(0.32),
            swap(bot_cell.label, eng_lab, run_time=0.8),
            FadeIn(car_title),
            run_time=3.0,
        )

        # Beat 3: antibody tip outside (continuous from membrane y = -1.10)
        self.at("An antibody tip")
        tip_stem = Line([1.6, -1.10, 0], [1.6, 0.10, 0], color=AB_CYAN, stroke_width=6)
        tip_cup = Arc(radius=0.38, start_angle=PI, angle=PI, arc_center=[1.6, 0.34, 0],
                      color=AB_CYAN, stroke_width=6)
        tip_core = Circle(radius=0.15, color=PEPTIDE_WHITE, stroke_width=2.5,
                          fill_color=PEPTIDE_WHITE, fill_opacity=0.88).move_to([1.6, 0.22, 0])
        tip_lab = T("antibody tip", 26, AB_CYAN, weight=BOLD).move_to([3.55, 0.15, 0])
        self.play(Create(tip_stem), Create(tip_cup), FadeIn(tip_core), FadeIn(tip_lab), run_time=2.2)

        # Beat 4: fused to zeta tail inside (3 hollow ITAM rings)
        self.at("to the zeta tail")
        zeta_tail = Line([1.6, -1.10, 0], [1.6, -2.55, 0], color=ZETA_TEAL, stroke_width=6.5)
        itams = VGroup(*[
            Circle(radius=0.14, color=PHOS_GOLD, stroke_width=3,
                   fill_color=BG, fill_opacity=0.85).move_to([1.96, -1.10 - 1.45 * f, 0])
            for f in (0.25, 0.55, 0.85)
        ])
        zeta_lab = T("zeta tail (3 ITAMs)", 26, ZETA_TEAL, weight=BOLD).move_to([3.85, -1.85, 0])
        sig1_lab = T("signal 1", 26, PHOS_GOLD, weight=BOLD).move_to([0.20, -1.85, 0])
        self.play(Create(zeta_tail), FadeIn(itams), FadeIn(zeta_lab), FadeIn(sig1_lab), run_time=2.4)

        # Beat 5: grips surface proteins directly (stretch stalk continuously from -1.10!)
        self.at("grips surface proteins")
        surf_prot = RoundedRectangle(corner_radius=0.18, width=0.52, height=0.72,
                                     color=SURF_PROT, stroke_width=3,
                                     fill_color=SURF_PROT, fill_opacity=0.85).move_to([1.6, 1.64, 0])
        surf_lab = T("tumour surface protein", 25, SURF_PROT, weight=BOLD).move_to([3.95, 1.60, 0])
        lit_itams = VGroup(*[
            make_phos([1.96, -1.10 - 1.45 * f, 0], radius=0.14)
            for f in (0.25, 0.55, 0.85)
        ])
        self.play(FadeIn(surf_prot, shift=DOWN * 0.2), FadeIn(surf_lab), run_time=0.8)
        self.play(
            tip_stem.animate.put_start_and_end_on([1.6, -1.10, 0], [1.6, 1.05, 0]),
            VGroup(tip_cup, tip_core).animate.shift(UP * 0.95),
            tip_lab.animate.shift(UP * 0.65),
            FadeOut(itams, run_time=0.3),
            FadeIn(lit_itams, scale=0.85),
            run_time=1.3,
        )

        # Beat 6: no MHC needed
        self.at("no MHC")
        no_mhc = boxed_label("no MHC needed", AB_CYAN, size=26).move_to([-0.55, 0.90, 0])
        self.play(FadeIn(no_mhc, shift=RIGHT * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ S09 CAR Signal Two
class S09CarSignalTwo(SpokenScene):
    def construct(self):
        top_cell = make_cell_band(2.05, is_top=True, color=PDL1_PLUM, fill_opacity=0.12,
                                  label="tumour cell", label_pos=[-4.7, 2.85, 0])
        act_lvl = ValueTracker(0.85)
        bot_fill = always_redraw(lambda: Rectangle(
            width=12.7, height=2.60, stroke_width=0,
            fill_color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            fill_opacity=0.13 + 0.15 * act_lvl.get_value(),
        ).move_to([0.0, -2.25, 0.0]).set_z_index(-5))
        bot_mem = always_redraw(lambda: Line(
            [-6.35, -0.95, 0], [6.35, -0.95, 0],
            color=interpolate_color(ManimColor(DIM_GREY), ManimColor(TCR_BLUE), act_lvl.get_value()),
            stroke_width=4.5 + 2.0 * act_lvl.get_value(),
        ).set_z_index(-2))
        t_lab = T("CAR T cell", 26, TEXT, weight=BOLD).move_to([-4.8, -3.10, 0])

        surf_prot = RoundedRectangle(corner_radius=0.18, width=0.52, height=0.72,
                                     color=SURF_PROT, stroke_width=3,
                                     fill_color=SURF_PROT, fill_opacity=0.85).move_to([-2.4, 1.69, 0])
        car = make_car_receptor(-2.4, -0.95, tip_h=2.12, has_costim=False, lit=True, zeta_len=1.22)

        state_lab = boxed_label("signal 1 only", PHOS_GOLD, size=26).move_to([-4.6, -1.90, 0])
        pop_center = np.array([3.45, 0.70, 0.0])
        cell_one = Circle(radius=0.52, color=TCR_BLUE, stroke_width=3.5,
                          fill_color=TCR_BLUE, fill_opacity=0.22).move_to(pop_center)
        pop_lab = T("T-cell persistence", 26, TEXT, weight=BOLD).move_to([3.45, 1.65, 0])

        self.add(top_cell, bot_fill, bot_mem, t_lab, surf_prot, car, state_lab,
                 cell_one, pop_lab, scope_tag("schematic"))

        # Beat 1: zeta tail alone gives signal 1 without signal 2
        self.at("zeta tail alone")
        self.play(act_lvl.animate.set_value(0.20),
                  cell_one.animate.scale(0.80), run_time=4.8)

        # Beat 2: early cells failed to persist -> fades dim
        self.at("failed to persist")
        poor_lab = boxed_label("signal 1 only — poor persistence", TEXT, size=25).move_to([3.45, -0.42, 0])
        self.play(
            act_lvl.animate.set_value(0.0),
            car.itams.animate.set_opacity(0.25),
            cell_one.animate.scale(0.68).set_color(DIM_GREY).set_opacity(0.35),
            FadeIn(poor_lab),
            run_time=2.6,
        )

        # Beat 3: Engineers spliced CD28 or 4-1BB inside
        self.at("Engineers spliced")
        costim_block = RoundedRectangle(corner_radius=0.10, width=0.54, height=0.58,
                                        color=CD28_GREEN, stroke_width=3,
                                        fill_color=CD28_GREEN, fill_opacity=0.30).move_to([-2.4, -1.27, 0])
        costim_txt = T("CD28 / 4-1BB", 25, CD28_GREEN, weight=BOLD).move_to([-0.35, -1.27, 0])
        both_lab = boxed_label("signal 1 + signal 2", CD28_GREEN, size=26).move_to([-4.6, -1.90, 0])
        costim_block.save_state()
        costim_block.shift(LEFT * 0.65 + DOWN * 0.45).set_opacity(0)

        self.play(FadeOut(poor_lab), swap(state_lab, both_lab, run_time=0.7), run_time=0.7)
        self.play(
            car.zeta_tail.animate.shift(DOWN * 0.62),
            car.itams.animate.shift(DOWN * 0.62),
            costim_block.animate.restore(),
            run_time=2.0,
        )
        self.play(FadeIn(costim_txt), run_time=0.6)

        # Beat 4: One binding event supplies both signals -> daughter cells divide cleanly without overlap
        self.at("One binding event")
        sig2_p = make_phos([-1.98, -1.27, 0], radius=0.13)
        daughters_2 = VGroup(
            Circle(radius=0.40, color=TCR_BLUE, stroke_width=3.5, fill_color=TCR_BLUE, fill_opacity=0.30).move_to([2.75, 0.70, 0]),
            Circle(radius=0.40, color=TCR_BLUE, stroke_width=3.5, fill_color=TCR_BLUE, fill_opacity=0.30).move_to([4.15, 0.70, 0]),
        )
        daughters_4 = VGroup(
            Circle(radius=0.32, color=TCR_BLUE, stroke_width=3.5, fill_color=TCR_BLUE, fill_opacity=0.35).move_to([2.55, 0.90, 0]),
            Circle(radius=0.32, color=TCR_BLUE, stroke_width=3.5, fill_color=TCR_BLUE, fill_opacity=0.35).move_to([3.45, 0.90, 0]),
            Circle(radius=0.32, color=TCR_BLUE, stroke_width=3.5, fill_color=TCR_BLUE, fill_opacity=0.35).move_to([4.35, 0.90, 0]),
            Circle(radius=0.32, color=TCR_BLUE, stroke_width=3.5, fill_color=TCR_BLUE, fill_opacity=0.35).move_to([3.45, 0.08, 0]),
        )
        persist_lab = boxed_label("active daughter cells", PHOS_GOLD, size=25).move_to([3.45, -1.75, 0])
        self.play(
            act_lvl.animate.set_value(1.0),
            car.itams.animate.set_opacity(1.0),
            FadeIn(sig2_p, scale=0.6),
            Transform(cell_one, daughters_2),
            run_time=0.85,
        )
        self.play(Transform(cell_one, daughters_4), FadeIn(persist_lab), run_time=0.85)
        self.finish()


# ------------------------------------------------------------------ S10 Return Rule
class S10ReturnRule(SpokenScene):
    def construct(self):
        top_cell = make_cell_band(1.85, is_top=True, color=MHC_SLATE, fill_opacity=0.12, outer_y=2.76,
                                  label="presenting / tumour cell", label_pos=[-4.1, 2.30, 0])
        bot_cell = make_cell_band(-1.15, is_top=False, color=TCR_BLUE, fill_opacity=0.16,
                                  label="T cell", label_pos=[-5.2, -3.05, 0])

        car_surf = RoundedRectangle(corner_radius=0.14, width=0.40, height=0.55,
                                    color=SURF_PROT, stroke_width=2.5,
                                    fill_color=SURF_PROT, fill_opacity=0.85).move_to([4.65, 1.57, 0])
        car = make_car_receptor(4.65, -1.15, tip_h=1.95, has_costim=True, lit=True, zeta_len=1.08)
        car_lab = T("2-signal CAR", 24, AB_CYAN, weight=BOLD).move_to([4.65, -3.05, 0])

        self.add(top_cell, bot_cell, car_surf, car, car_lab, scope_tag("schematic"))
        self.play(Indicate(car.costim, color=CD28_GREEN, scale_factor=1.10), run_time=0.9)

        # Beat 1: That domain lets engineered T cells last
        self.at("engineered T cells last")
        self.play(Indicate(car.itams, color=PHOS_GOLD, scale_factor=1.12), run_time=2.2)

        # Beat 2: From natural checkpoints to synthetic receptors — align all 5 side-by-side
        self.at("From natural checkpoints")
        mhc = make_mhc_peptide(-4.9, 1.85)
        tcr = make_tcr_complex(-4.9, -1.15, has_phosphates=True, chain_h=1.78, tail_len=0.85)
        b7 = make_b7(-3.2, 1.85, height=0.95)
        cd28 = make_cd28(-3.2, -1.15, height=1.55, tail_len=0.82, has_phosphates=True)
        g1_lab = T("TCR + CD28-B7", 24, CD28_GREEN, weight=BOLD).move_to([-4.05, -2.42, 0])

        ctla4 = make_ctla4_dimer(-1.1, -1.15, height=1.35, spread=0.45)
        g2_lab = T("CTLA-4", 24, CTLA4_CRIMSON, weight=BOLD).move_to([-1.1, -2.42, 0])

        pdl1 = make_pdl1(0.95, 1.85, height=0.72)
        pd1 = make_pd1(0.95, -1.15, height=1.15, tail_len=1.00, has_phosphates=True)
        shp2 = make_shp2((0.35, -1.78, 0), arm_angle_deg=-145.0, arm_len=0.52)
        shp2.scale(0.68)
        shp2.shift(np.array([0.48, -1.78, 0.0]) - shp2.body.get_center())
        g3_lab = T("PD-1 / SHP-2", 24, PD1_MAGENTA, weight=BOLD).move_to([0.95, -2.60, 0])

        ab = make_antibody_y([2.8, 0.35, 0], angle=PI, scale=0.85, color=AB_CYAN)
        g4_lab = T("antibody", 24, AB_CYAN, weight=BOLD).move_to([2.8, -0.65, 0])

        self.play(
            FadeIn(mhc), FadeIn(tcr), FadeIn(b7), FadeIn(cd28), FadeIn(g1_lab),
            FadeIn(ctla4), FadeIn(g2_lab),
            FadeIn(pdl1), FadeIn(pd1), FadeIn(shp2), FadeIn(g3_lab),
            FadeIn(ab), FadeIn(g4_lab),
            run_time=2.5,
        )

        # Beat 3: the same wiring rules the response
        self.at("the same wiring")
        rule_cap = boxed_label("same wiring: signal 1 + signal 2, regulated outside & inside",
                               PHOS_GOLD, size=25).move_to([0.0, 3.22, 0])
        self.play(FadeIn(rule_cap, shift=DOWN * 0.1), run_time=0.6)
        self.play(Indicate(VGroup(g1_lab, g2_lab, g3_lab, g4_lab), color=PHOS_GOLD), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ S11 End
class S11End(EndCard):
    LINE = "Full activation needs a second signal, and checkpoints brake outside or inside."
