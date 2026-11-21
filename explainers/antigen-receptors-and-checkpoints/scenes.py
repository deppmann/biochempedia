"""Two Phosphates on Partner Tails — Antigen Receptors and Checkpoints.

COLOUR MAP (one colour per concept for the whole film)
  APC_COL     = #6E7F94   presenting cell membrane & MHC protein
  PEPTIDE_COL = #E8EAF0   peptide held in MHC groove (TEXT)
  TCR_COL     = #58C4DD   alpha-beta T-cell receptor recognition chains (BLUE)
  PARTNER_COL = #3FB8C0   CD3 and zeta partner chains (TEAL)
  CORECEP_COL = #83C167   CD4 / CD8 co-receptor (GREEN)
  LCK_COL     = #F0A23B   Lck tyrosine kinase (amber)
  PHOS_COL    = #F5D547   phosphate tags & tyrosine ITAM rings (YELLOW)
  CD45_COL    = #9AA5B4   CD45 phosphatase (cool grey)
  ZAP_COL     = #FC6255   ZAP-70 kinase & tandem SH2 claws (RED / coral)
  LAT_COL     = #B07CFF   LAT membrane scaffold (violet)
  CA_COL      = #46E8B5   Ca2+ -> NFAT branch (mint-aqua)
  PKC_COL     = #F472B6   DAG / PKC -> NF-kB branch (rose-magenta)
  RAS_COL     = #B8EC42   Ras / ERK -> AP-1 branch (chartreuse-lime)
  NUC_COL     = #3B5998   nuclear envelope & IL-2 gene region

CARRIED WORLD
  Two parallel horizontal membranes — presenting cell above, T cell below — with the MHC-peptide
  complex at the top centre, the alpha-beta TCR gripping it with a stubby inner tail, flanked by
  CD3 and zeta partner tails carrying 10 ITAMs into the T-cell cytosol, membrane-anchored and
  co-receptor-bound Lck, tall CD45 stalks in the gap, and downstream LAT fanning three pathways
  into the nuclear arc below.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from)
  s01_hook          TCR rises to grip peptide-MHC; view zooms onto the stubby tail; an empty enzyme
                    slot is rejected with X and a kinase (+P) fails to dock; ? ring traces around gap.
  s02_partners      View pulls back; CD3 and zeta partner chains slide in and grow long inner tails;
                    10 ITAMs (4 CD3 + 6 zeta, paired tyrosines at fixed spacing) appear sequentially.
  s03_lck           Free Lck glides along inner membrane; CD4/CD8 slides in carrying Lck to grip MHC;
                    both Lck active-site indicators cycle and sample near tails at resting turnover.
  s04_predict_setup Lck repeatedly adds gold P onto an ITAM ring while tall unlabelled grey stalks sweep
                    across and strip each P back to hollow; live lasting-P readout stays at 0.
  s06_reveal_cd45   Tall stalks are labelled CD45 and strip P; membranes press closer (gap tracker
                    2.30 -> 1.22), physically pushing tall CD45 outward so paired gold Ps hold inside.
  s07_coincidence   Zoom onto one horizontal ITAM pair; Lck tags 1 ring -> ZAP-70's single SH2 claw
                    wobbles and slips off; Lck tags both -> both claws clamp, body hinges open, Lck activates it.
  s08_lat_scaffold  View pans right keeping active TCR-ZAP-70 on left; ZAP-70 fires P onto violet LAT's
                    docking bays one by one; 3 branch stubs emerge downward.
  s09_three_branches Computed 0->7 s clock runs continuously as 3 signal streams (Ca2+->NFAT,
                    DAG/PKC->NF-kB, Ras/ERK->AP-1) flow from LAT bays into the nuclear arc (4-7 s).
  s10_convergence   NFAT, NF-kB, and AP-1 dock together on IL-2 gene bar launching an activation wave;
                    view zooms back out to frame the whole active synapse and highlights the 2-P lock.
"""

from bp_parts import *

# ---- Concept palette ----
APC_COL     = "#6E7F94"
APC_FILL    = "#2A3958"
TMEM_COL    = "#7D8FA6"
TCELL_FILL  = "#172033"
PEPTIDE_COL = TEXT
TCR_COL     = BLUE
PARTNER_COL = TEAL
CORECEP_COL = GREEN
LCK_COL     = "#F0A23B"
PHOS_COL    = YELLOW
CD45_COL    = "#9AA5B4"
ZAP_COL     = RED
LAT_COL     = "#B07CFF"
CA_COL      = "#46E8B5"
PKC_COL     = "#F472B6"
RAS_COL     = "#B8EC42"
NUC_FILL    = "#18294A"
NUC_STROKE  = "#5A82C4"
DNA_COL     = "#98B8F0"

# Canonical synapse coordinates (full view)
GAP_TOP_Y = 2.40
GAP_BOT_Y = 0.10
GAP_NARROW_TOP = 1.32


# ------------------------------------------------------------------ shared geometry builders
def build_cell_bands(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y):
    """Presenting cell above (top) and T cell below (bottom) as filled regions + lipid bilayers."""
    apc_bg = Rectangle(width=15.0, height=3.2, fill_color=APC_FILL, fill_opacity=1.0, stroke_width=0)
    apc_bg.move_to([0, gap_top + 1.68, 0])
    apc_mem = RoundedRectangle(corner_radius=0.05, width=15.0, height=0.18,
                               fill_color=APC_COL, fill_opacity=0.90, stroke_color="#94A6BC", stroke_width=2)
    apc_mem.move_to([0, gap_top + 0.09, 0])

    t_bg = Rectangle(width=15.0, height=5.2, fill_color=TCELL_FILL, fill_opacity=1.0, stroke_width=0)
    t_bg.move_to([0, gap_bot - 2.68, 0])
    t_mem = RoundedRectangle(corner_radius=0.05, width=15.0, height=0.18,
                             fill_color=TMEM_COL, fill_opacity=0.90, stroke_color="#A3B4C8", stroke_width=2)
    t_mem.move_to([0, gap_bot - 0.09, 0])

    apc_bg.set_z_index(-5)
    t_bg.set_z_index(-5)
    apc_mem.set_z_index(-2)
    t_mem.set_z_index(-2)
    return VGroup(apc_bg, t_bg, apc_mem, t_mem), apc_mem, t_mem


def build_mhc_peptide(anchor_y=GAP_TOP_Y, cx=0.0):
    """Slate MHC block with an open groove holding the warm-white peptide pill."""
    base = RoundedRectangle(corner_radius=0.10, width=1.65, height=0.48,
                            fill_color=APC_COL, fill_opacity=0.95, stroke_color="#9EB0C6", stroke_width=2.5)
    base.move_to([cx, anchor_y - 0.24, 0])
    left_arm = RoundedRectangle(corner_radius=0.08, width=0.40, height=0.54,
                                fill_color=APC_COL, fill_opacity=0.95, stroke_color="#9EB0C6", stroke_width=2.5)
    left_arm.move_to([cx - 0.56, anchor_y - 0.64, 0])
    right_arm = RoundedRectangle(corner_radius=0.08, width=0.40, height=0.54,
                                 fill_color=APC_COL, fill_opacity=0.95, stroke_color="#9EB0C6", stroke_width=2.5)
    right_arm.move_to([cx + 0.56, anchor_y - 0.64, 0])
    mhc = VGroup(base, left_arm, right_arm)

    pep = RoundedRectangle(corner_radius=0.12, width=0.76, height=0.24,
                           fill_color=PEPTIDE_COL, fill_opacity=1.0, stroke_color=GOLD, stroke_width=2)
    pep.move_to([cx, anchor_y - 0.64, 0])
    return VGroup(mhc, pep), mhc, pep


def build_tcr(anchor_y=GAP_BOT_Y, cx=0.0, top_y=1.55):
    """Alpha-beta TCR: two steel-blue recognition chains gripping peptide-MHC, with stubby inner tails."""
    h_ext = max(0.4, top_y - anchor_y)
    chains = VGroup()
    for dx in (-0.22, 0.22):
        stem = RoundedRectangle(corner_radius=0.09, width=0.28, height=h_ext,
                                fill_color=TCR_COL, fill_opacity=0.92, stroke_color=TCR_COL, stroke_width=2.5)
        stem.move_to([cx + dx, anchor_y + h_ext / 2, 0])
        tip = RoundedRectangle(corner_radius=0.08, width=0.32, height=0.32,
                               fill_color=TCR_COL, fill_opacity=0.98, stroke_color=TEXT, stroke_width=2)
        tip.move_to([cx + dx * 1.15, top_y + 0.04, 0])
        stub = RoundedRectangle(corner_radius=0.05, width=0.16, height=0.36,
                                fill_color=TCR_COL, fill_opacity=0.92, stroke_color=TCR_COL, stroke_width=2)
        stub.move_to([cx + dx, anchor_y - 0.28, 0])
        chains.add(stem, tip, stub)
    return chains


def make_itam_pair(cx, y_top, dy=0.24, filled=False, radius=0.085, horizontal=False):
    """One ITAM: two tyrosine rings at fixed spacing connected by a partner spacer bar."""
    if horizontal:
        p1 = np.array([cx - dy / 2, y_top, 0.0])
        p2 = np.array([cx + dy / 2, y_top, 0.0])
    else:
        p1 = np.array([cx, y_top, 0.0])
        p2 = np.array([cx, y_top - dy, 0.0])
    bar = Line(p1, p2, color=PARTNER_COL, stroke_width=4.5)
    rings = VGroup()
    for p in (p1, p2):
        r = Circle(radius=radius, stroke_color=PHOS_COL, stroke_width=3,
                   fill_color=PHOS_COL if filled else TCELL_FILL, fill_opacity=1.0).move_to(p)
        rings.add(r)
    return VGroup(bar, rings)


def build_partners(anchor_y=GAP_BOT_Y, cx=0.0, filled=False):
    """Four CD3 chains (1 ITAM each) + two zeta chains (3 ITAMs each) = 10 ITAMs total."""
    specs = [
        (-1.95, 1.35, [0.72]),
        (-1.35, 1.35, [0.72]),
        (-0.52, 2.70, [0.66, 1.46, 2.26]),
        ( 0.52, 2.70, [0.66, 1.46, 2.26]),
        ( 1.35, 1.35, [0.72]),
        ( 1.95, 1.35, [0.72]),
    ]
    tails_grp = VGroup()
    itams_grp = VGroup()
    for dx, tlen, offsets in specs:
        x = cx + dx
        ect = RoundedRectangle(corner_radius=0.07, width=0.22, height=0.28,
                               fill_color=PARTNER_COL, fill_opacity=0.88, stroke_color=PARTNER_COL, stroke_width=2)
        ect.move_to([x, anchor_y + 0.14, 0])
        tail = Line([x, anchor_y - 0.08, 0], [x, anchor_y - tlen, 0], color=PARTNER_COL, stroke_width=6)
        tails_grp.add(VGroup(ect, tail))
        for off in offsets:
            itams_grp.add(make_itam_pair(x, anchor_y - off, dy=0.24, filled=filled, radius=0.085))
    return tails_grp, itams_grp


def build_lck_block(cx, y, active=True):
    """Amber Lck kinase block tethered to the inner membrane leaflet, with external active-site ring."""
    tether = Line([cx, y + 0.32, 0], [cx, y + 0.14, 0], color=LCK_COL, stroke_width=4)
    body = RoundedRectangle(corner_radius=0.10, width=0.78, height=0.44,
                            fill_color=LCK_COL, fill_opacity=0.95, stroke_color="#FFD28A", stroke_width=2)
    body.move_to([cx, y - 0.06, 0])
    lab = T("Lck", size=24, color=BG, weight=BOLD).move_to(body)
    g = VGroup(tether, body, lab)
    if active:
        # Active-site arc clearly outside the right edge of body so it never touches 'Lck' or box
        arc = Arc(radius=0.14, start_angle=-1.1, angle=2.2,
                  arc_center=[cx + 0.54, y - 0.06, 0], color=PHOS_COL, stroke_width=3.5)
        g.add(arc)
        g.arc = arc
    return g


def build_coreceptor_lck(anchor_y=GAP_BOT_Y, base_x=-2.85, grip_pt=(-0.72, 1.82), active=True):
    """Olive CD4/CD8 co-receptor gripping MHC and carrying an amber Lck on its inner tail."""
    gx, gy = grip_pt
    stem = CubicBezier(
        [base_x, anchor_y - 0.05, 0],
        [base_x, anchor_y + 0.85, 0],
        [gx - 0.70, gy - 0.35, 0],
        [gx, gy, 0],
        color=CORECEP_COL, stroke_width=9,
    )
    head = RoundedRectangle(corner_radius=0.07, width=0.32, height=0.26,
                            fill_color=CORECEP_COL, fill_opacity=0.98, stroke_color=TEXT, stroke_width=2)
    head.move_to([gx, gy, 0])
    tail = Line([base_x, anchor_y - 0.05, 0], [base_x, anchor_y - 0.42, 0], color=CORECEP_COL, stroke_width=6)
    lck = build_lck_block(base_x, anchor_y - 0.58, active=active)
    return VGroup(stem, head, tail, lck), lck


def build_cd45(x, anchor_y=GAP_BOT_Y, ecto_h=1.95):
    """Tall cool-grey CD45 phosphatase spanning most of the resting inter-membrane gap."""
    stalk = Line([x, anchor_y - 0.52, 0], [x, anchor_y + ecto_h, 0], color=CD45_COL, stroke_width=7)
    cap_top = RoundedRectangle(corner_radius=0.14, width=0.64, height=0.95,
                               fill_color=CD45_COL, fill_opacity=0.45, stroke_color=CD45_COL, stroke_width=3)
    cap_top.move_to([x, anchor_y + ecto_h - 0.48, 0])
    cap_mid = RoundedRectangle(corner_radius=0.10, width=0.42, height=0.52,
                               fill_color=CD45_COL, fill_opacity=0.40, stroke_color=CD45_COL, stroke_width=2.5)
    cap_mid.move_to([x, anchor_y + ecto_h - 1.24, 0])
    blade = RoundedRectangle(corner_radius=0.10, width=0.62, height=0.40,
                             fill_color=CD45_COL, fill_opacity=0.90, stroke_color=TEXT, stroke_width=2)
    blade.move_to([x, anchor_y - 0.72, 0])
    return VGroup(stalk, cap_top, cap_mid, blade)


def build_zap70(center, claw_sep=2.6, open_frac=0.0, activated=False, p_label=True):
    """Coral ZAP-70 with two curved SH2 claws spaced at `claw_sep` and a hinged kinase body."""
    cx, cy, _ = np.array(center, dtype=float)
    cup_r = min(0.25, claw_sep * 0.40)
    neck_off = min(0.48, claw_sep * 0.30)
    bridge_w = min(1.32, max(0.66, claw_sep * 0.95))
    hinge_x = cx + min(0.45, bridge_w * 0.36)
    claws = VGroup()
    for sgn in (-1, 1):
        kx = cx + sgn * (claw_sep / 2.0)
        cup = Arc(radius=cup_r, start_angle=PI * 1.05, angle=PI * 0.90,
                  arc_center=[kx, cy + 0.58, 0], color=ZAP_COL, stroke_width=10)
        neck = Line([kx, cy + 0.58 - cup_r + 0.01, 0], [cx + sgn * neck_off, cy + 0.08, 0], color=ZAP_COL, stroke_width=8)
        claws.add(cup, neck)

    bridge = RoundedRectangle(corner_radius=0.10, width=bridge_w, height=0.34,
                              fill_color=ZAP_COL, fill_opacity=0.95, stroke_color="#FFAAA3", stroke_width=2.2)
    bridge.move_to([cx, cy + 0.08, 0])

    # Hinged catalytic kinase domain: folded under bridge at open_frac=0, swings DOWNWARD at open_frac=1
    hinge_pt = np.array([hinge_x, cy - 0.06, 0.0])
    angle = 0.08 + 1.15 * open_frac  # positive rotation swings left-extending lobe DOWNWARD
    lobe = RoundedRectangle(corner_radius=0.18, width=1.45, height=0.66,
                            fill_color=ZAP_COL, fill_opacity=0.96,
                            stroke_color=PHOS_COL if activated else "#FFAAA3",
                            stroke_width=4 if activated else 2.5)
    dx_lobe = -0.62 * np.cos(angle) - (-0.26) * np.sin(angle)
    dy_lobe = -0.62 * np.sin(angle) + (-0.26) * np.cos(angle)
    lobe.rotate(angle).move_to([hinge_pt[0] + dx_lobe, hinge_pt[1] + dy_lobe, 0])
    hinge_dot = Dot(hinge_pt, radius=0.07, color=TEXT)
    g = VGroup(claws, bridge, lobe, hinge_dot)
    if activated:
        p_badge = Circle(radius=0.19, fill_color=PHOS_COL, fill_opacity=1.0, stroke_color=TEXT, stroke_width=2)
        p_badge.move_to(lobe.get_center())
        g.add(p_badge)
        if p_label:
            p_txt = T("P", size=24, color=BG, weight=BOLD).move_to(p_badge)
            g.add(p_txt)
    g.lobe = lobe
    return g


def build_synapse_state(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y, filled_itams=False, cd45_xs=(-4.3, 4.3)):
    """Rebuild the canonical full synapse at rest or compressed (used across s03-s06)."""
    cells, apc_mem, t_mem = build_cell_bands(gap_top=gap_top, gap_bot=gap_bot)
    mhc_all, mhc, pep = build_mhc_peptide(anchor_y=gap_top, cx=0.0)
    tcr = build_tcr(anchor_y=gap_bot, cx=0.0, top_y=gap_top - 0.85)
    tails, itams = build_partners(anchor_y=gap_bot, cx=0.0, filled=filled_itams)
    corecep_all, cd4_lck = build_coreceptor_lck(
        anchor_y=gap_bot, base_x=-2.85, grip_pt=(-0.72, gap_top - 0.58), active=True
    )
    free_lck = build_lck_block(3.20, gap_bot - 0.42, active=True)
    cd4_lck.set_z_index(4)
    free_lck.set_z_index(4)
    cd45s = VGroup(*[build_cd45(x, anchor_y=gap_bot, ecto_h=1.95) for x in cd45_xs])
    cd45s.set_z_index(1)
    return VGroup(cells, mhc_all, tcr, tails, itams, corecep_all, free_lck, cd45s), {
        "cells": cells, "mhc_all": mhc_all, "mhc": mhc, "pep": pep,
        "tcr": tcr, "tails": tails, "itams": itams,
        "corecep": corecep_all, "cd4_lck": cd4_lck, "free_lck": free_lck, "cd45s": cd45s,
    }


def make_p_packet(pos, radius=0.14):
    """Bright gold phosphate packet (no tiny text inside)."""
    return Circle(radius=radius, fill_color=PHOS_COL, fill_opacity=1.0, stroke_color=TEXT, stroke_width=2).move_to(pos)


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Antigen Receptors and Checkpoints"
    TITLE = "Two Phosphates on Partner Tails"


class S01Hook(SpokenScene):
    def construct(self):
        cells, _, _ = build_cell_bands(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y)
        mhc_all, mhc, pep = build_mhc_peptide(anchor_y=GAP_TOP_Y, cx=0.0)
        tcr = build_tcr(anchor_y=GAP_BOT_Y, cx=0.0, top_y=1.12)
        tcr.shift(DOWN * 0.45)

        lbl_apc = T("Infected cell", size=28, color=TEXT).move_to([-4.6, 3.05, 0])
        lbl_tcell = T("T cell", size=28, color=TEXT).move_to([-5.1, -3.05, 0])
        lbl_mhc = T("MHC + peptide", size=26, color=PEPTIDE_COL).move_to([2.65, 1.85, 0])
        lbl_tcr = T("αβ TCR", size=28, color=TCR_COL).move_to([-1.75, 0.85, 0])
        tag = scope_tag("schematic", color=TEXT)

        self.play(FadeIn(cells), FadeIn(lbl_apc), FadeIn(lbl_tcell), FadeIn(tag), run_time=0.8)
        self.play(FadeIn(mhc_all), FadeIn(lbl_mhc), FadeIn(tcr), run_time=0.6)

        self.at("spots an infected cell")
        tcr_docked = build_tcr(anchor_y=GAP_BOT_Y, cx=0.0, top_y=GAP_TOP_Y - 0.85)
        self.play(Transform(tcr, tcr_docked), FadeIn(lbl_tcr, run_time=0.45), run_time=1.8)

        self.at("inner tail is tiny")
        # Fade out upper APC & MHC cleanly as we zoom onto the T-cell membrane & tiny inner tail
        self.play(
            FadeOut(lbl_apc), FadeOut(lbl_tcell), FadeOut(lbl_mhc), FadeOut(lbl_tcr),
            FadeOut(cells[0]), FadeOut(cells[2]), FadeOut(mhc_all),
            run_time=0.45,
        )
        zoom_grp = VGroup(cells[1], cells[3], tcr)
        self.play(
            zoom_grp.animate.shift(UP * 0.75).scale(1.38, about_point=ORIGIN),
            run_time=1.4,
        )
        slot_center = np.array([0.0, -0.35, 0.0])
        empty_slot = DashedVMobject(
            RoundedRectangle(corner_radius=0.18, width=2.6, height=1.20, color=TCR_COL, stroke_width=3.5)
        ).move_to(slot_center)
        stub_bracket = Line([-0.55, 0.46, 0], [0.55, 0.46, 0], color=PHOS_COL, stroke_width=3.5)
        lbl_tiny = T("tiny inner tail", size=30, color=TCR_COL).move_to([-2.95, 0.48, 0])
        self.play(Create(empty_slot), Create(stub_bracket), FadeIn(lbl_tiny), run_time=0.85)

        self.at("holds no enzyme")
        x_mark = VGroup(
            Line(slot_center + [-0.55, -0.35, 0], slot_center + [0.55, 0.35, 0], color=RED, stroke_width=8),
            Line(slot_center + [-0.55, 0.35, 0], slot_center + [0.55, -0.35, 0], color=RED, stroke_width=8),
        )
        lbl_no_enz = T("no enzyme", size=30, color=RED).next_to(empty_slot, RIGHT, buff=0.40)
        self.play(Create(x_mark), FadeIn(lbl_no_enz, run_time=0.4), run_time=0.9)

        self.at("not even a kinase")
        kin_box = RoundedRectangle(corner_radius=0.14, width=2.6, height=0.74,
                                   fill_color=LCK_COL, fill_opacity=0.28, stroke_color=LCK_COL, stroke_width=3)
        kin_txt = T("kinase (+P)", size=28, color=LCK_COL).move_to(kin_box)
        kin = VGroup(kin_box, kin_txt).move_to([0.0, -2.25, 0])
        self.play(FadeIn(kin, shift=UP * 0.2), run_time=0.55)

        self.at("adds phosphate groups")
        p_dot = make_p_packet([-0.6, -1.75, 0], radius=0.16)
        self.play(
            kin.animate.move_to([0.0, -1.48, 0]),
            FadeIn(p_dot),
            p_dot.animate.move_to([0.0, -1.02, 0]),
            run_time=1.0,
        )
        self.play(
            kin.animate.shift(DOWN * 0.90).set_opacity(0.35),
            FadeOut(p_dot),
            run_time=0.9,
        )
        self.play(FadeOut(kin), run_time=0.35)

        self.at("How does it fire")
        q_ring_t = ValueTracker(0.0)
        q_arc = always_redraw(lambda: Arc(
            radius=0.46, start_angle=PI / 2, angle=max(0.05, q_ring_t.get_value()) * TAU,
            arc_center=slot_center, color=PHOS_COL, stroke_width=5
        ))
        q_mark = T("?", size=58, color=PHOS_COL, weight=BOLD).move_to(slot_center)
        q_text = caption("How does it fire without firing by accident?", size=30, color=PHOS_COL)
        self.play(FadeOut(x_mark), FadeOut(lbl_no_enz), FadeIn(q_mark), FadeIn(q_text), run_time=0.55)
        self.add(q_arc)
        self.play(q_ring_t.animate.set_value(1.0), run_time=2.6, rate_func=linear)
        self.finish()


class S02Partners(SpokenScene):
    def construct(self):
        cells, _, _ = build_cell_bands(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y)
        mhc_all, mhc, pep = build_mhc_peptide(anchor_y=GAP_TOP_Y, cx=0.0)
        tcr = build_tcr(anchor_y=GAP_BOT_Y, cx=0.0, top_y=GAP_TOP_Y - 0.85)
        zoom_grp = VGroup(cells[1], cells[3], tcr)
        zoom_grp.save_state()
        zoom_grp.shift(UP * 0.75).scale(1.38, about_point=ORIGIN)
        upper_grp = VGroup(cells[0], cells[2], mhc_all)
        upper_grp.set_opacity(0)

        tag = scope_tag("schematic", color=TEXT)
        self.add(zoom_grp, upper_grp, tag)

        self.at("splits the job in two")
        self.play(Restore(zoom_grp), upper_grp.animate.set_opacity(1.0), run_time=1.4)
        lbl_rec = T("1. Recognition", size=28, color=TCR_COL).move_to([-4.2, 1.35, 0])
        lbl_sig = T("2. Signalling", size=28, color=PARTNER_COL).move_to([-5.0, -1.35, 0])
        self.play(FadeIn(lbl_rec, run_time=0.5), FadeIn(lbl_sig, run_time=0.5))

        self.at("alpha and beta chains")
        lbl_ab = T("αβ TCR", size=26, color=TCR_COL).move_to([1.65, 1.05, 0])
        self.play(FadeIn(lbl_ab, run_time=0.4), Indicate(tcr, color=TEXT, scale_factor=1.06), run_time=1.2)

        self.at("short peptide")
        lbl_pep = T("peptide", size=26, color=PEPTIDE_COL).move_to([1.85, 1.52, 0])
        pep_arr = Arrow(lbl_pep.get_left() + LEFT * 0.10, [0.20, GAP_TOP_Y - 0.64, 0],
                        buff=0, color=PEPTIDE_COL, stroke_width=3, max_tip_length_to_length_ratio=0.18).set_z_index(3)
        self.play(FadeIn(lbl_pep, run_time=0.4), GrowArrow(pep_arr), run_time=0.8)

        self.at("MHC groove")
        lbl_mhc = T("MHC", size=26, color=TEXT).move_to([1.60, 2.15, 0])
        self.play(FadeIn(lbl_mhc, run_time=0.4), Indicate(mhc, color=PEPTIDE_COL, scale_factor=1.04), run_time=1.0)

        self.at("partner chains")
        tails, itams = build_partners(anchor_y=GAP_BOT_Y, cx=0.0, filled=False)
        left_chains = VGroup(tails[0], tails[1])
        mid_chains = VGroup(tails[2], tails[3])
        right_chains = VGroup(tails[4], tails[5])
        left_chains.shift(LEFT * 1.1).set_opacity(0)
        right_chains.shift(RIGHT * 1.1).set_opacity(0)
        mid_chains.set_opacity(0)
        self.play(
            left_chains.animate.shift(RIGHT * 1.1).set_opacity(1),
            right_chains.animate.shift(LEFT * 1.1).set_opacity(1),
            mid_chains.animate.set_opacity(1),
            run_time=1.4,
        )

        self.at("CD3 and Zeta")
        lbl_cd3 = T("CD3", size=28, color=PARTNER_COL).move_to([2.95, -0.65, 0])
        lbl_zeta = T("ζ chains", size=28, color=PARTNER_COL).move_to([1.55, -2.50, 0])
        self.play(FadeIn(lbl_cd3, run_time=0.4), FadeIn(lbl_zeta, run_time=0.4))

        self.at("long inner tails")
        self.play(
            *[Indicate(tails[i][1], color=PARTNER_COL, scale_factor=1.04) for i in range(6)],
            run_time=1.2,
        )

        self.at("paired tyrosines")
        self.play(LaggedStart(*[FadeIn(it, scale=1.15) for it in itams], lag_ratio=0.14), run_time=2.0)

        self.at("called ITAMs")
        lbl_itam = T("ITAM (paired Y–Y)", size=28, color=PHOS_COL).move_to([-3.85, -2.25, 0])
        arr_itam = Arrow(lbl_itam.get_right() + RIGHT * 0.10, itams[4].get_left() + LEFT * 0.14,
                         buff=0, color=PHOS_COL, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        badge_box = boxed_label("10 ITAMs per complex (schematic)", color=PHOS_COL, size=24)
        badge_box.move_to([-3.75, -3.10, 0])
        self.play(FadeIn(lbl_itam, run_time=0.4), GrowArrow(arr_itam), FadeIn(badge_box, run_time=0.4), run_time=0.8)
        self.finish()


class S03Lck(SpokenScene):
    def construct(self):
        cells, _, _ = build_cell_bands(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y)
        mhc_all, mhc, pep = build_mhc_peptide(anchor_y=GAP_TOP_Y, cx=0.0)
        tcr = build_tcr(anchor_y=GAP_BOT_Y, cx=0.0, top_y=GAP_TOP_Y - 0.85)
        tails, itams = build_partners(anchor_y=GAP_BOT_Y, cx=0.0, filled=False)
        lbl_mhc = T("MHC", size=26, color=TEXT).move_to([1.60, 2.15, 0])
        lbl_tcr = T("αβ TCR", size=26, color=TCR_COL).move_to([1.65, 1.05, 0])
        lbl_partners = T("CD3 & ζ", size=26, color=PARTNER_COL).move_to([3.05, -1.45, 0])
        tag = scope_tag("schematic", color=TEXT)
        self.add(cells, mhc_all, tcr, tails, itams, lbl_mhc, lbl_tcr, lbl_partners, tag)

        self.at("where is the kinase")
        q_kin = T("? kinase", size=30, color=LCK_COL).move_to([3.55, -0.35, 0])
        self.play(
            FadeIn(q_kin, shift=UP * 0.1),
            *[
                r.animate(rate_func=there_and_back).scale(1.22).set_stroke(color=TEXT, width=5)
                for pair in itams for r in pair[1]
            ],
            run_time=1.8,
        )

        self.at("tyrosine kinase LCK")
        free_lck = build_lck_block(5.4, GAP_BOT_Y - 0.42, active=True)
        lbl_lck = T("Lck kinase", size=28, color=LCK_COL).move_to([4.55, -1.05, 0])
        self.play(FadeOut(q_kin), FadeIn(free_lck), run_time=0.6)

        self.at("anchored in the")
        self.play(free_lck.animate.move_to([3.35, GAP_BOT_Y - 0.42, 0]), FadeIn(lbl_lck, run_time=0.4), run_time=2.5)

        self.at("A share of it")
        corecep_all, cd4_lck = build_coreceptor_lck(
            anchor_y=GAP_BOT_Y, base_x=-2.85, grip_pt=(-0.72, GAP_TOP_Y - 0.58), active=True
        )
        corecep_all.shift(LEFT * 3.0)
        self.play(corecep_all.animate.shift(RIGHT * 3.0), free_lck.animate.shift(LEFT * 0.25), run_time=2.4)

        self.at("CD4 or CD8")
        lbl_cd4 = T("CD4 / CD8", size=28, color=CORECEP_COL).move_to([-4.2, 1.35, 0])
        lbl_cd4_lck = T("Lck (on tail)", size=26, color=LCK_COL).move_to([-4.35, -1.05, 0])
        self.play(FadeIn(lbl_cd4, run_time=0.4), FadeIn(lbl_cd4_lck, run_time=0.4), free_lck.animate.shift(RIGHT * 0.25), run_time=2.2)

        self.at("grips the same MHC")
        grip_ring = Circle(radius=0.34, color=CORECEP_COL, stroke_width=5).move_to([-0.72, GAP_TOP_Y - 0.58, 0])
        self.play(Create(grip_ring), run_time=0.9)
        self.play(FadeOut(grip_ring), Indicate(corecep_all[0], color=CORECEP_COL, scale_factor=1.04), free_lck.animate.shift(LEFT * 0.25), run_time=2.0)

        self.at("partly active even at rest")
        lbl_rest = caption("Lck is already partly active at rest", size=28, color=LCK_COL)
        p1 = make_p_packet(cd4_lck[1].get_right() + RIGHT * 0.28, radius=0.14)
        p2 = make_p_packet(free_lck[1].get_left() + LEFT * 0.28, radius=0.14)
        self.play(FadeIn(lbl_rest, run_time=0.4), FadeIn(p1), FadeIn(p2), run_time=0.6)
        self.play(
            free_lck.animate.shift(RIGHT * 0.25),
            p1.animate.move_to(itams[0][1][0].get_center()),
            p2.animate.move_to(itams[8][1][0].get_center()),
            run_time=1.3,
        )
        self.play(FadeOut(p1), FadeOut(p2), run_time=0.5)
        self.finish()


class S04PredictSetup(SpokenScene):
    def construct(self):
        world, objs = build_synapse_state(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y, filled_itams=False, cd45_xs=(-4.3, 4.3))
        cd45s = objs["cd45s"]
        cd45s.set_opacity(0)
        lbl_tails = T("ITAMs", size=26, color=PHOS_COL).move_to([-1.95, -1.85, 0])
        tag = scope_tag("schematic", color=TEXT)
        self.add(world, lbl_tails, tag)

        self.at("active LCK sits right")
        target_ring = objs["itams"][0][1][0]
        p_pkt = make_p_packet(objs["cd4_lck"][1].get_right() + RIGHT * 0.12, radius=0.12)
        self.add(p_pkt)
        self.play(p_pkt.animate.move_to(target_ring.get_center()), run_time=0.9)
        self.remove(p_pkt)
        target_ring.set_fill(PHOS_COL, opacity=1.0)

        self.at("paired tyrosines")
        stalk_l, stalk_r = cd45s[0], cd45s[1]
        stalk_l.shift(LEFT * 0.35)
        stalk_r.shift(RIGHT * 0.35)
        self.play(
            stalk_l.animate.set_opacity(1.0).shift(RIGHT * 0.35),
            stalk_r.animate.set_opacity(1.0).shift(LEFT * 0.35),
            run_time=1.8,
        )

        self.at("resting T cell stays quiet")
        status = boxed_label("lasting P: 0", color=TEXT, size=26).move_to([-4.65, -2.55, 0])
        self.play(
            FadeIn(status, run_time=0.45),
            stalk_l.animate.shift(LEFT * 0.25),
            stalk_r.animate.shift(RIGHT * 0.25),
            run_time=1.0,
        )
        self.play(
            target_ring.animate.set_fill(TCELL_FILL, opacity=1.0),
            stalk_l.animate.shift(RIGHT * 0.25),
            stalk_r.animate.shift(LEFT * 0.25),
            run_time=0.9,
        )

        self.at("no lasting phosphate")
        target_r = objs["itams"][9][1][0]
        p_pkt2 = make_p_packet(objs["free_lck"][1].get_left() + LEFT * 0.12, radius=0.12)
        self.add(p_pkt2)
        self.play(p_pkt2.animate.move_to(target_r.get_center()), run_time=0.7)
        self.remove(p_pkt2)
        target_r.set_fill(PHOS_COL, opacity=1.0)
        self.play(
            stalk_l.animate.shift(LEFT * 0.25),
            stalk_r.animate.shift(RIGHT * 0.25),
            run_time=0.7,
        )
        self.play(
            target_r.animate.set_fill(TCELL_FILL, opacity=1.0),
            stalk_l.animate.shift(RIGHT * 0.25),
            stalk_r.animate.shift(LEFT * 0.25),
            run_time=0.7,
        )

        self.at("What holds the switch off")
        q = question_card("Active Lck is right there. Why is a resting T cell quiet?", y=3.25, max_w=11.5)
        self.play(FadeIn(q.question, run_time=0.5), run_time=0.9)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Active Lck is right there. Why is a resting T cell quiet?"
    CARD = {"y": 3.25, "max_w": 11.5}
    RING_AT = (5.85, -2.35, 0)
    SECONDS = 4.5

    def backdrop(self):
        world, _ = build_synapse_state(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y, filled_itams=False, cd45_xs=(-4.3, 4.3))
        lbl_tails = T("ITAMs", size=26, color=PHOS_COL).move_to([-1.95, -1.85, 0])
        status = boxed_label("lasting P: 0", color=TEXT, size=26).move_to([-4.65, -2.55, 0])
        tag = scope_tag("schematic", color=TEXT)
        return VGroup(world, lbl_tails, status, tag)


def _apc_profile_y(x, center_y, edge_y=GAP_TOP_Y, x_flat=3.2, x_edge=4.8):
    ax = abs(x)
    if ax <= x_flat:
        return center_y
    if ax >= x_edge:
        return edge_y
    t = (ax - x_flat) / (x_edge - x_flat)
    s = t * t * (3.0 - 2.0 * t)
    return center_y + (edge_y - center_y) * s


def build_apc_bowed(center_y, edge_y=GAP_TOP_Y):
    xs = np.linspace(-7.5, 7.5, 81)
    bot_pts = [[x, _apc_profile_y(x, center_y, edge_y), 0.0] for x in xs]
    top_pts = [[x, _apc_profile_y(x, center_y, edge_y) + 0.18, 0.0] for x in reversed(xs)]
    apc_mem = Polygon(*(bot_pts + top_pts), fill_color=APC_COL, fill_opacity=0.90,
                      stroke_color="#94A6BC", stroke_width=2).set_z_index(-2)
    bg_bot = [[x, _apc_profile_y(x, center_y, edge_y) + 0.09, 0.0] for x in xs]
    bg_top = [[7.5, 5.2, 0.0], [-7.5, 5.2, 0.0]]
    apc_bg = Polygon(*(bg_bot + bg_top), fill_color=APC_FILL, fill_opacity=1.0,
                     stroke_width=0).set_z_index(-5)
    return apc_bg, apc_mem


class S06RevealCd45(SpokenScene):
    def construct(self):
        world, objs = build_synapse_state(gap_top=GAP_TOP_Y, gap_bot=GAP_BOT_Y, filled_itams=False, cd45_xs=(-4.3, 4.3))
        lbl_tails = T("ITAMs", size=26, color=PHOS_COL).move_to([-1.95, -1.85, 0])
        q = question_card("Active Lck is right there. Why is a resting T cell quiet?", y=3.25, max_w=11.5)
        tag = scope_tag("schematic", color=TEXT)
        self.add(world, lbl_tails, q.question, tag)

        cd45_l, cd45_r = objs["cd45s"][0], objs["cd45s"][1]

        self.at("phosphatase called CD45")
        lbl_cd45 = T("CD45\nphosphatase", size=26, color=TEXT).move_to([2.05, 1.58, 0])
        arr_cd45 = Arrow(lbl_cd45.get_right() + RIGHT * 0.12, cd45_r[1].get_left() + LEFT * 0.12,
                         buff=0, color=TEXT, stroke_width=3, max_tip_length_to_length_ratio=0.16)
        self.play(FadeOut(q.question), FadeIn(lbl_cd45, run_time=0.35), GrowArrow(arr_cd45), run_time=0.75)

        self.at("keeps erasing them")
        ring_ex = objs["itams"][9][1][0]
        p_pkt = make_p_packet(objs["free_lck"][1].get_left() + LEFT * 0.12, radius=0.12)
        self.add(p_pkt)
        self.play(
            FadeOut(arr_cd45, run_time=0.3),
            lbl_cd45.animate.move_to([4.3, 3.18, 0]),
            p_pkt.animate.move_to(ring_ex.get_center()),
            run_time=0.6,
        )
        self.remove(p_pkt)
        ring_ex.set_fill(PHOS_COL, opacity=1.0)
        self.play(cd45_r.animate.move_to([2.15, cd45_r.get_center()[1], 0]), run_time=0.9)

        self.at("strips phosphate groups off")
        ring_ex.set_fill(TCELL_FILL, opacity=1.0)
        self.play(cd45_r.animate.move_to([4.3, cd45_r.get_center()[1], 0]), run_time=0.9)

        self.at("outer part is tall")
        # Height bracket placed cleanly to the LEFT of right CD45 (x = 3.70) with label at x = 2.15
        top_pt = [3.70, GAP_BOT_Y + 1.95, 0]
        bot_pt = [3.70, GAP_BOT_Y + 0.05, 0]
        tall_line = Line(bot_pt, top_pt, color=PHOS_COL, stroke_width=3.5)
        tall_caps = VGroup(
            Line([3.58, bot_pt[1], 0], [3.82, bot_pt[1], 0], color=PHOS_COL, stroke_width=3.5),
            Line([3.58, top_pt[1], 0], [3.82, top_pt[1], 0], color=PHOS_COL, stroke_width=3.5),
        )
        lbl_tall = T("tall outer part", size=26, color=PHOS_COL).move_to([2.25, 0.88, 0])
        self.play(FadeOut(lbl_cd45), Create(tall_line), Create(tall_caps), FadeIn(lbl_tall, run_time=0.45), run_time=0.9)

        self.at("two cells press close")
        dy = GAP_TOP_Y - GAP_NARROW_TOP  # 1.08
        apc_bg_flat, apc_mem_flat = build_apc_bowed(GAP_TOP_Y, GAP_TOP_Y)
        apc_bg_bow, apc_mem_bow = build_apc_bowed(GAP_NARROW_TOP, GAP_TOP_Y)
        objs["cells"].remove(objs["cells"][0], objs["cells"][2])
        self.add(apc_bg_flat, apc_mem_flat)
        tcr_pressed = build_tcr(anchor_y=GAP_BOT_Y, cx=0.0, top_y=GAP_NARROW_TOP - 0.85)
        corecep_pressed, _ = build_coreceptor_lck(
            anchor_y=GAP_BOT_Y, base_x=-2.85, grip_pt=(-0.72, GAP_NARROW_TOP - 0.58), active=True
        )
        self.play(
            FadeOut(tall_line), FadeOut(tall_caps), FadeOut(lbl_tall),
            Transform(apc_bg_flat, apc_bg_bow),
            Transform(apc_mem_flat, apc_mem_bow),
            objs["mhc_all"].animate.shift(DOWN * dy),
            Transform(objs["tcr"], tcr_pressed),
            Transform(objs["corecep"], corecep_pressed),
            run_time=1.8,
        )

        self.at("no longer fits")
        lbl_excl = T("CD45 pushed out", size=26, color=TEXT).move_to([3.10, 0.82, 0])
        arr_excl = Arrow(lbl_excl.get_right() + RIGHT * 0.10, [5.15, 1.30, 0],
                         buff=0, color=TEXT, stroke_width=3, max_tip_length_to_length_ratio=0.16)
        self.play(
            cd45_l.animate.move_to([-5.55, cd45_l.get_center()[1], 0]),
            cd45_r.animate.move_to([ 5.55, cd45_r.get_center()[1], 0]),
            FadeIn(lbl_excl, run_time=0.45), GrowArrow(arr_excl),
            run_time=1.3,
        )

        self.at("one leading model")
        hedge = boxed_label("one leading model — still debated", color=TEXT, size=24).move_to([-3.25, 3.05, 0])
        pkts = []
        anims = []
        target_pairs = [objs["itams"][4], objs["itams"][5], objs["itams"][6], objs["itams"][7]]
        for idx, pair in enumerate(target_pairs):
            src = objs["cd4_lck"][1].get_right() if idx % 2 == 0 else objs["free_lck"][1].get_left()
            for r in pair[1]:
                pk = make_p_packet(src, radius=0.10)
                self.add(pk)
                pkts.append((pk, r))
                anims.append(pk.animate.move_to(r.get_center()))
        self.play(FadeIn(hedge, run_time=0.45), LaggedStart(*anims, lag_ratio=0.05), run_time=0.6)
        for pk, r in pkts:
            self.remove(pk)
            r.set_fill(PHOS_COL, opacity=1.0)

        self.at("lets phosphate stay")
        self.finish()


class S07Coincidence(SpokenScene):
    def construct(self):
        tail_y = 1.55
        tail_bg = Rectangle(width=15.0, height=8.5, fill_color=TCELL_FILL, fill_opacity=1.0, stroke_width=0).set_z_index(-5)
        left_x, right_x = -1.30, 1.30
        # Draw tail line and ITAM bar cleanly behind rings
        tail_line = Line([-5.6, tail_y, 0], [5.6, tail_y, 0], color=PARTNER_COL, stroke_width=9).set_z_index(0)
        itam_bar = Line([left_x, tail_y, 0], [right_x, tail_y, 0], color=PHOS_COL, stroke_width=6).set_z_index(1)
        ring_l = Circle(radius=0.24, stroke_color=PHOS_COL, stroke_width=4.5, fill_color=TCELL_FILL, fill_opacity=1.0).move_to([left_x, tail_y, 0]).set_z_index(2)
        ring_r = Circle(radius=0.24, stroke_color=PHOS_COL, stroke_width=4.5, fill_color=TCELL_FILL, fill_opacity=1.0).move_to([right_x, tail_y, 0]).set_z_index(2)

        lbl_tail = T("partner tail (ITAM)", size=28, color=PARTNER_COL).move_to([4.55, tail_y + 0.56, 0])
        lbl_y1 = T("Y", size=26, color=TEXT).move_to([left_x, tail_y + 0.52, 0])
        lbl_y2 = T("Y", size=26, color=TEXT).move_to([right_x, tail_y + 0.52, 0])

        lck = build_lck_block(-3.8, tail_y + 1.05, active=True)
        tag = scope_tag("schematic", color=TEXT)
        self.add(tail_bg, tail_line, itam_bar, ring_l, ring_r, lck, tag)

        self.at("reads those marks")
        self.play(FadeIn(lbl_tail, run_time=0.45), FadeIn(lbl_y1, run_time=0.45), FadeIn(lbl_y2, run_time=0.45))

        self.at("ZAP70 is a second kinase")
        zap_home = np.array([0.0, -1.65, 0.0])
        zap = build_zap70(zap_home, claw_sep=2.60, open_frac=0.0, activated=False)
        lbl_zap = T("ZAP-70 (folded)", size=28, color=ZAP_COL).move_to([0.0, -2.95, 0])
        self.play(FadeIn(zap, shift=UP * 0.25, run_time=0.6), FadeIn(lbl_zap, run_time=0.45))

        self.at("two SH2 claws")
        lbl_claws = T("two SH2 claws", size=26, color=ZAP_COL).move_to([3.55, -0.95, 0])
        arr_claw = Arrow(lbl_claws.get_left() + LEFT * 0.10, [1.55, -1.08, 0],
                         buff=0, color=ZAP_COL, stroke_width=3, max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(lbl_claws, run_time=0.4), GrowArrow(arr_claw), run_time=0.7)

        self.at("spaced to fit one pair")
        brace_line = DashedLine([left_x, 0.50, 0], [right_x, 0.50, 0], color=PHOS_COL, stroke_width=3, dash_length=0.14)
        lbl_space = T("fixed spacing", size=24, color=PHOS_COL).move_to([0.0, 0.78, 0])
        self.play(Create(brace_line), FadeIn(lbl_space, run_time=0.4), run_time=0.8)

        self.at("One phosphate holds a single claw")
        self.play(
            FadeOut(brace_line), FadeOut(lbl_space), FadeOut(lbl_claws), FadeOut(arr_claw),
            lck.animate.move_to([left_x, tail_y + 1.15, 0]),
            run_time=0.75,
        )
        pkt_l = make_p_packet([left_x, tail_y + 0.75, 0], radius=0.16)
        self.add(pkt_l)
        self.play(pkt_l.animate.move_to(ring_l.get_center()), run_time=0.45)
        self.remove(pkt_l)
        ring_l.set_fill(PHOS_COL, opacity=1.0)
        lbl_yp1 = T("Y–P", size=26, color=PHOS_COL, weight=BOLD).move_to([left_x, tail_y + 0.52, 0])
        self.play(swap(lbl_y1, lbl_yp1, run_time=0.4))

        dock_y = tail_y - 0.84
        pivot_l = np.array([left_x, tail_y - 0.15, 0.0])
        zap_tilted = zap.copy().move_to([0.0, dock_y, 0.0]).rotate(-0.22, about_point=pivot_l)
        self.play(Transform(zap, zap_tilted), run_time=0.85)

        self.at("ZAP70 slips off")
        weak_lbl = T("1 phosphate: weak grip — slips off", size=28, color=RED).move_to([0.0, -3.15, 0])
        self.play(swap(lbl_zap, weak_lbl, run_time=0.45))
        self.play(Rotate(zap, angle=-0.08, about_point=pivot_l), run_time=0.40)
        self.play(Rotate(zap, angle=0.06, about_point=pivot_l), run_time=0.40)
        self.play(zap.animate.rotate(0.24).move_to(zap_home), run_time=0.85)

        self.at("keeps a stray mark")
        stray_badge = boxed_label("stray mark ignored", color=RED, size=24).move_to([3.95, 0.45, 0])
        self.play(FadeIn(stray_badge, run_time=0.35), run_time=0.5)

        self.at("both tyrosines tagged")
        self.play(FadeOut(weak_lbl), FadeOut(stray_badge), lck.animate.move_to([right_x, tail_y + 1.15, 0]), run_time=0.75)
        pkt_r = make_p_packet([right_x, tail_y + 0.75, 0], radius=0.16)
        self.add(pkt_r)
        self.play(pkt_r.animate.move_to(ring_r.get_center()), run_time=0.45)
        self.remove(pkt_r)
        ring_r.set_fill(PHOS_COL, opacity=1.0)
        lbl_yp2 = T("Y–P", size=26, color=PHOS_COL, weight=BOLD).move_to([right_x, tail_y + 0.52, 0])
        self.play(swap(lbl_y2, lbl_yp2, run_time=0.4))

        self.at("both claws clamp tight")
        clamp_lbl = T("2 phosphates: both claws clamp tight", size=28, color=PHOS_COL).move_to([0.0, -3.15, 0])
        self.play(
            zap.animate.move_to([0.0, dock_y, 0.0]),
            FadeIn(clamp_lbl, run_time=0.4),
            run_time=0.8,
        )

        self.at("Docking opens ZAP70")
        open_t = ValueTracker(0.0)
        zap_open_anim = always_redraw(lambda: build_zap70(
            [0.0, dock_y, 0.0], claw_sep=2.60, open_frac=open_t.get_value(), activated=False
        ))
        lck_path = VMobject().set_points_as_corners([
            [right_x, tail_y + 1.15, 0],
            [2.45, tail_y + 1.15, 0],
            [2.45, -0.35, 0],
            [2.95, -0.35, 0],
        ])
        lck_move = MoveAlongPath(lck, lck_path)
        self.remove(zap)
        self.add(zap_open_anim)
        self.play(open_t.animate.set_value(1.0), lck_move, run_time=1.3)

        self.at("and LCK")
        self.remove(zap_open_anim)
        zap_open = build_zap70([0.0, dock_y, 0.0], claw_sep=2.60, open_frac=1.0, activated=False)
        self.add(zap_open)
        act_pkt = make_p_packet(lck[1].get_left() + LEFT * 0.12, radius=0.16)
        self.add(act_pkt)
        self.play(act_pkt.animate.move_to(zap_open.lobe.get_center()), run_time=0.35)
        self.remove(act_pkt)
        zap_active = build_zap70([0.0, dock_y, 0.0], claw_sep=2.60, open_frac=1.0, activated=True)
        lbl_active = T("ZAP-70 active", size=28, color=PHOS_COL).move_to([0.0, -2.25, 0])
        self.play(Transform(zap_open, zap_active), FadeOut(clamp_lbl), FadeIn(lbl_active, run_time=0.35), run_time=0.35)
        self.finish()


class S08LatScaffold(SpokenScene):
    def construct(self):
        mem_y = 1.15
        t_bg = Rectangle(width=15.0, height=5.8, fill_color=TCELL_FILL, fill_opacity=1.0, stroke_width=0).move_to([0, mem_y - 2.9, 0]).set_z_index(-5)
        t_mem = RoundedRectangle(corner_radius=0.05, width=15.0, height=0.18,
                                 fill_color=TMEM_COL, fill_opacity=0.90, stroke_color="#A3B4C8", stroke_width=2).move_to([0, mem_y - 0.09, 0]).set_z_index(-2)

        cx_l = -3.6
        tcr_l = build_tcr(anchor_y=mem_y, cx=cx_l, top_y=mem_y + 0.90)
        tail_l = Line([cx_l, mem_y - 0.05, 0], [cx_l, mem_y - 2.15, 0], color=PARTNER_COL, stroke_width=6)
        itam_l = make_itam_pair(cx_l, mem_y - 0.95, dy=0.84, filled=True, radius=0.13, horizontal=True)
        zap_l = build_zap70([cx_l, mem_y - 1.55, 0], claw_sep=0.84 / 0.85, open_frac=1.0, activated=True, p_label=False).scale(0.85, about_point=[cx_l, mem_y - 1.55, 0])
        lbl_rec = T("active receptor + ZAP-70", size=26, color=ZAP_COL).move_to([-3.6, -2.55, 0])

        tag = scope_tag("schematic", color=TEXT)
        self.add(t_bg, t_mem, tcr_l, tail_l, itam_l, zap_l, lbl_rec, tag)

        self.at("first core rule")
        rule_card = boxed_label("Core rule: Two phosphates on partner ITAMs switch on the receptor",
                                color=PHOS_COL, size=26).move_to([0.0, 3.10, 0])
        self.play(FadeIn(rule_card, run_time=0.5), run_time=0.8)

        self.at("Two phosphates on partner ITAMs")
        self.play(Indicate(itam_l, color=PHOS_COL, scale_factor=1.18), run_time=1.6)
        self.play(Indicate(zap_l, color=PHOS_COL, scale_factor=1.06), run_time=1.8)

        self.at("Once active")
        lat_x = 1.65
        lat_ect = RoundedRectangle(corner_radius=0.07, width=0.30, height=0.44,
                                   fill_color=LAT_COL, fill_opacity=0.92, stroke_color=TEXT, stroke_width=2).move_to([lat_x, mem_y + 0.16, 0])
        lat_bar = RoundedRectangle(corner_radius=0.12, width=0.40, height=3.20,
                                   fill_color=LAT_COL, fill_opacity=0.90, stroke_color="#D7BFFF", stroke_width=2.5).move_to([lat_x, mem_y - 1.60, 0])
        slot_ys = [0.45, -0.35, -1.15, -1.95]
        lat_slots = VGroup(*[
            Circle(radius=0.16, stroke_color=PHOS_COL, stroke_width=3.5, fill_color=BG, fill_opacity=1.0).move_to([lat_x + 0.38, y, 0])
            for y in slot_ys
        ])
        lat_grp = VGroup(lat_ect, lat_bar, lat_slots).shift(RIGHT * 4.8)
        lbl_lat = T("LAT scaffold", size=28, color=LAT_COL).move_to([lat_x, mem_y + 0.85, 0])
        self.play(lat_grp.animate.shift(LEFT * 4.8), run_time=1.2)

        self.at("phosphorylates LAT")
        self.play(FadeIn(lbl_lat, run_time=0.4), run_time=0.5)

        self.at("a membrane scaffold")
        zap_src = zap_l.get_right() + RIGHT * 0.08
        for slot in lat_slots:
            pkt = make_p_packet(zap_src, radius=0.16)
            ring_pulse = Circle(radius=0.30, stroke_color=PHOS_COL, stroke_width=3).move_to(slot.get_center())
            self.add(pkt)
            self.play(pkt.animate.move_to(slot.get_center()), run_time=0.65)
            self.remove(pkt)
            slot.set_fill(PHOS_COL, opacity=1.0)
            self.play(Create(ring_pulse), run_time=0.25)
            self.play(FadeOut(ring_pulse), run_time=0.25)

        self.at("become docking bays")
        lbl_bays = T("docking bays", size=26, color=PHOS_COL).move_to([4.55, 0.45, 0])
        arr_bay = Arrow(lbl_bays.get_left() + LEFT * 0.10, lat_slots[0].get_right() + RIGHT * 0.12,
                        buff=0, color=PHOS_COL, stroke_width=3, max_tip_length_to_length_ratio=0.16)
        self.play(FadeIn(lbl_bays, run_time=0.4), GrowArrow(arr_bay), run_time=0.7)

        self.at("split the signal three ways")
        stubs = VGroup(
            Arrow(lat_slots[1].get_right() + RIGHT * 0.12, [3.35, -0.65, 0], buff=0, color=CA_COL, stroke_width=6),
            Arrow(lat_slots[2].get_right() + RIGHT * 0.12, [3.55, -1.45, 0], buff=0, color=PKC_COL, stroke_width=6),
            Arrow(lat_slots[3].get_right() + RIGHT * 0.12, [3.35, -2.25, 0], buff=0, color=RAS_COL, stroke_width=6),
        )
        b_labs = VGroup(
            T("Ca²⁺", size=24, color=CA_COL).next_to(stubs[0].get_end(), RIGHT, buff=0.16),
            T("DAG / PKC", size=24, color=PKC_COL).next_to(stubs[1].get_end(), RIGHT, buff=0.16),
            T("Ras / ERK", size=24, color=RAS_COL).next_to(stubs[2].get_end(), RIGHT, buff=0.16),
        )
        self.play(LaggedStart(*[GrowArrow(s) for s in stubs], lag_ratio=0.18), FadeIn(b_labs, run_time=0.45), run_time=1.3)
        self.finish()


class S09ThreeBranches(SpokenScene):
    def construct(self):
        mem_y = 2.65
        t_bg = Rectangle(width=15.0, height=7.2, fill_color=TCELL_FILL, fill_opacity=1.0, stroke_width=0).move_to([0, mem_y - 3.6, 0]).set_z_index(-5)
        t_mem = RoundedRectangle(corner_radius=0.05, width=15.0, height=0.18,
                                 fill_color=TMEM_COL, fill_opacity=0.90, stroke_color="#A3B4C8", stroke_width=2).move_to([0, mem_y - 0.09, 0]).set_z_index(-2)

        tcr_ref = build_tcr(anchor_y=mem_y, cx=-4.6, top_y=mem_y + 0.65).scale(0.8, about_point=[-4.6, mem_y, 0])
        tail_ref = Line([-4.6, mem_y - 0.05, 0], [-4.6, mem_y - 1.10, 0], color=PARTNER_COL, stroke_width=5)
        zap_badge = boxed_label("ZAP-70 active", color=ZAP_COL, size=24).move_to([-4.6, mem_y - 1.45, 0])

        lat_bar = RoundedRectangle(corner_radius=0.12, width=3.0, height=0.40,
                                   fill_color=LAT_COL, fill_opacity=0.92, stroke_color="#D7BFFF", stroke_width=2.5).move_to([0.0, mem_y - 0.45, 0])
        bay_xs = [-1.05, 0.0, 1.05]
        bays = VGroup(*[
            Circle(radius=0.14, fill_color=PHOS_COL, fill_opacity=1.0, stroke_color=TEXT, stroke_width=2).move_to([bx, mem_y - 0.72, 0])
            for bx in bay_xs
        ])
        lbl_lat = T("LAT (phosphorylated)", size=26, color=LAT_COL).move_to([0.0, mem_y + 0.35, 0])

        nuc_arc = Arc(radius=7.4, start_angle=PI * 0.28, angle=PI * 0.44,
                      arc_center=[0.0, -9.15, 0], color=NUC_STROKE, stroke_width=5)
        nuc_fill = Sector(radius=7.4, start_angle=PI * 0.28, angle=PI * 0.44,
                          arc_center=[0.0, -9.15, 0], fill_color=NUC_FILL, fill_opacity=0.95, stroke_width=0).set_z_index(-3)
        lbl_nuc = T("Nucleus", size=28, color=TEXT).move_to([0.0, -3.32, 0])

        t_clock = ValueTracker(0.0)
        clock_readout = counter("{:4.1f} s (schematic)", t_clock, at=[4.55, 3.15, 0], size=26, color=PHOS_COL)
        tag = scope_tag("schematic", color=TEXT)

        self.add(t_bg, t_mem, tcr_ref, tail_ref, zap_badge, lat_bar, bays, lbl_lat, nuc_fill, nuc_arc, lbl_nuc, clock_readout, tag)

        # Paths terminate cleanly on the nuclear envelope arc (arc top at x=0 is -1.75, at x=+-3.8 is -2.80)
        p_ca = CubicBezier([-1.05, mem_y - 0.86, 0], [-2.5, 0.85, 0], [-3.8, -0.35, 0], [-3.8, -2.80, 0], color=CA_COL, stroke_width=6)
        p_pkc = CubicBezier([0.0, mem_y - 0.86, 0], [0.0, 0.90, 0], [0.0, 0.05, 0], [0.0, -1.75, 0], color=PKC_COL, stroke_width=6)
        p_ras = CubicBezier([1.05, mem_y - 0.86, 0], [2.5, 0.85, 0], [3.8, -0.35, 0], [3.8, -2.80, 0], color=RAS_COL, stroke_width=6)

        # Continuous stream tracker running across the whole scene so active pathways flow visibly
        stream_t = ValueTracker(0.0)
        stream_t.add_updater(lambda m, dt: m.increment_value(0.55 * dt))
        self.add(stream_t)

        def make_stream(path, color, count=4):
            grp = VGroup()
            for k in range(count):
                off = k / count
                grp.add(always_redraw(lambda o=off: VGroup(
                    Dot(path.point_from_proportion((stream_t.get_value() + o) % 1.0),
                        radius=0.26, color=color).set_opacity(0.32),
                    Dot(path.point_from_proportion((stream_t.get_value() + o) % 1.0),
                        radius=0.17, color=color, stroke_color=TEXT, stroke_width=2.5),
                )))
            return grp

        self.at("three branches fan out")
        self.play(
            t_clock.animate.set_value(4.0),
            Create(p_ca), Create(p_pkc), Create(p_ras),
            run_time=2.8,
        )

        self.at("raises calcium")
        lbl_ca_path = T("Ca²⁺", size=26, color=CA_COL).move_to([-4.65, 0.35, 0])
        ca_stream = make_stream(p_ca, CA_COL)
        self.add(ca_stream)
        self.play(FadeIn(lbl_ca_path, run_time=0.4), t_clock.animate.set_value(6.5), run_time=1.2)

        self.at("NFAT into the nucleus")
        nfat_tok = boxed_label("NFAT", color=CA_COL, size=26).move_to([-2.40, -3.05, 0])
        self.play(FadeIn(nfat_tok, shift=DOWN * 0.25, run_time=0.6), t_clock.animate.set_value(7.0), run_time=1.8)

        self.at("A second runs")
        lbl_pkc_path = T("DAG / PKC", size=26, color=PKC_COL).move_to([1.35, 0.35, 0])
        pkc_stream = make_stream(p_pkc, PKC_COL)
        self.add(pkc_stream)
        self.play(FadeIn(lbl_pkc_path, run_time=0.4), run_time=1.8)

        self.at("to NF kappa B")
        nfkb_tok = boxed_label("NF-κB", color=PKC_COL, size=26).move_to([0.0, -2.42, 0])
        self.play(FadeIn(nfkb_tok, shift=DOWN * 0.25, run_time=0.6), run_time=1.5)

        self.at("A third")
        lbl_ras_path = T("Ras / ERK", size=26, color=RAS_COL).move_to([4.75, 0.35, 0])
        ras_stream = make_stream(p_ras, RAS_COL)
        self.add(ras_stream)
        self.play(FadeIn(lbl_ras_path, run_time=0.4), run_time=1.1)

        self.at("to drive ERK")
        ap1_tok = boxed_label("AP-1", color=RAS_COL, size=26).move_to([2.40, -3.05, 0])
        self.play(FadeIn(ap1_tok, shift=DOWN * 0.25, run_time=0.6))
        self.finish()


class S10Convergence(SpokenScene):
    def construct(self):
        nuc_bg = Rectangle(width=15.0, height=8.5, fill_color=NUC_FILL, fill_opacity=1.0, stroke_width=0).set_z_index(-5)
        dna_bar = RoundedRectangle(corner_radius=0.10, width=9.4, height=0.34,
                                   fill_color=DNA_COL, fill_opacity=0.88, stroke_color=TEXT, stroke_width=2).move_to([0.0, -0.95, 0])
        lbl_gene = T("IL-2 gene", size=30, color=TEXT, weight=BOLD).move_to([0.0, -1.68, 0])

        nfat_tok = boxed_label("NFAT", color=CA_COL, size=28).move_to([-3.6, 1.35, 0])
        nfkb_tok = boxed_label("NF-κB", color=PKC_COL, size=28).move_to([0.0, 1.55, 0])
        ap1_tok = boxed_label("AP-1", color=RAS_COL, size=28).move_to([3.6, 1.35, 0])
        tag = scope_tag("schematic", color=TEXT)

        self.add(nuc_bg, dna_bar, lbl_gene, nfat_tok, nfkb_tok, ap1_tok, tag)

        self.at("meet on target genes")
        self.play(
            nfat_tok.animate.move_to([-2.3, -0.36, 0]),
            nfkb_tok.animate.move_to([0.0, -0.36, 0]),
            ap1_tok.animate.move_to([2.3, -0.36, 0]),
            run_time=1.6,
        )

        self.at("interleukin")
        self.play(Indicate(dna_bar, color=PHOS_COL, scale_factor=1.06), run_time=1.0)

        self.at("T cell to divide")
        wave1 = Arc(radius=1.25, start_angle=PI * 0.18, angle=PI * 0.64, arc_center=[0, -0.8, 0], color=PHOS_COL, stroke_width=5)
        wave2 = Arc(radius=2.15, start_angle=PI * 0.18, angle=PI * 0.64, arc_center=[0, -0.8, 0], color=PHOS_COL, stroke_width=4)
        lbl_div = T("T cell divides", size=30, color=PHOS_COL).move_to([0.0, 2.05, 0])
        self.play(Create(wave1), Create(wave2), FadeIn(lbl_div, run_time=0.45), run_time=1.4)

        self.at("never needed its own enzyme")
        nuc_view = VGroup(nuc_bg, dna_bar, lbl_gene, nfat_tok, nfkb_tok, ap1_tok, wave1, wave2, lbl_div)

        cells, _, _ = build_cell_bands(gap_top=2.45, gap_bot=0.95)
        mhc_all, _, _ = build_mhc_peptide(anchor_y=2.45, cx=-2.0)
        tcr = build_tcr(anchor_y=0.95, cx=-2.0, top_y=1.60)
        corecep, _ = build_coreceptor_lck(anchor_y=0.95, base_x=-4.95, grip_pt=(-2.72, 1.88), active=True)
        tails, itams = build_partners(anchor_y=0.95, cx=-2.0, filled=True)
        zap_center = np.array([-1.19, -1.43, 0.0])
        zap = build_zap70(zap_center, claw_sep=0.48, open_frac=1.0, activated=True, p_label=False)
        zap.scale(0.50, about_point=zap_center).rotate(PI / 2, about_point=zap_center)

        lat_bar = RoundedRectangle(corner_radius=0.10, width=0.36, height=2.05,
                                   fill_color=LAT_COL, fill_opacity=0.92, stroke_color="#D7BFFF", stroke_width=2).move_to([2.2, -0.05, 0])
        lat_bays = VGroup(*[
            Circle(radius=0.12, fill_color=PHOS_COL, fill_opacity=1.0, stroke_color=TEXT, stroke_width=1.5).move_to([2.50, y, 0])
            for y in (0.45, -0.05, -0.55)
        ])
        mini_nuc = RoundedRectangle(corner_radius=0.22, width=2.2, height=1.25,
                                    fill_color=NUC_FILL, fill_opacity=0.95, stroke_color=NUC_STROKE, stroke_width=3).move_to([4.95, -2.00, 0])
        b1 = Arrow([2.64, 0.45, 0], [3.78, -1.55, 0], buff=0, color=CA_COL, stroke_width=4.5)
        b2 = Arrow([2.64, -0.05, 0], [3.78, -2.00, 0], buff=0, color=PKC_COL, stroke_width=4.5)
        b3 = Arrow([2.64, -0.55, 0], [3.78, -2.45, 0], buff=0, color=RAS_COL, stroke_width=4.5)
        zap_to_lat = DashedLine(zap.get_right() + RIGHT * 0.12, [1.95, -0.05, 0], color=PHOS_COL, stroke_width=3)

        lbl_ov_tcr = T("αβ TCR", size=24, color=TCR_COL).move_to([-0.35, 1.95, 0])
        lbl_ov_cd4 = T("CD4/CD8 + Lck", size=24, color=CORECEP_COL).move_to([-4.65, 2.05, 0])
        lbl_ov_tails = T("partner tails (ITAMs)", size=24, color=PARTNER_COL).move_to([-4.65, -1.05, 0])
        lbl_ov_zap = T("ZAP-70", size=24, color=ZAP_COL).move_to([-0.25, -2.35, 0])
        lbl_ov_lat = T("LAT", size=24, color=LAT_COL).move_to([2.2, 1.38, 0])
        lbl_ov_il2 = T("IL-2 gene", size=24, color=TEXT).move_to([4.95, -2.00, 0])

        overview = VGroup(
            cells, mhc_all, tcr, corecep, tails, itams, zap, zap_to_lat,
            lat_bar, lat_bays, mini_nuc, b1, b2, b3,
            lbl_ov_tcr, lbl_ov_cd4, lbl_ov_tails, lbl_ov_zap, lbl_ov_lat, lbl_ov_il2,
        )
        self.play(FadeOut(nuc_view), run_time=0.55)
        self.play(FadeIn(overview), run_time=0.75)

        self.at("Partner tails carry the switch")
        self.play(Indicate(itams, color=PHOS_COL, scale_factor=1.08), run_time=1.3)

        self.at("demanding two phosphates")
        lock_box = RoundedRectangle(corner_radius=0.14, width=1.60, height=1.18,
                                    stroke_color=PHOS_COL, stroke_width=4, fill_opacity=0).move_to([-1.15, -1.43, 0])
        lbl_lock = T("Two phosphates required — noise filtered out", size=26, color=PHOS_COL).move_to([-1.2, -3.18, 0])
        self.play(Create(lock_box), FadeIn(lbl_lock, run_time=0.45), run_time=1.2)

        self.at("keeps noise")
        self.play(Indicate(lock_box, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.finish()


class S11End(EndCard):
    LINE = "Two phosphates on partner ITAMs switch on the antigen receptor."
