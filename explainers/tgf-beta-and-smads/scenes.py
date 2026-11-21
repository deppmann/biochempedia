"""
COLOUR MAP (one colour per concept across the whole film):
- TYPE2_COL  = BLUE (#58C4DD, cyan)      : Type II receptor serine/threonine kinase (always active)
- TYPE1_COL  = "#7B88FF" (indigo)        : Type I receptor serine/threonine kinase (locked at rest)
- LIGAND_COL = "#F29938" (amber)         : TGF-beta / activin ligand dimer
- FKBP_COL   = GREY (#8B93A1, slate)     : FKBP12 safety catch (labels in TEXT)
- PHOS_COL   = YELLOW (#F5D547, yellow)  : Phosphate group (P)
- RSMAD_COL  = "#4CD48B" (emerald green) : TGF-beta/activin R-Smad (Smad2 / Smad3)
- SMAD4_COL  = "#C27CFF" (violet)        : Shared partner Smad4
- BMP_COL    = RED (#FC6255, coral)      : BMP ligand dimer and BMP R-Smad (Smad1 / Smad5 / Smad8)
- NUC_COL    = GOLD (#D4A843, gold)      : Nuclear rim and DNA
- MEM_COL    = TEAL (#3FB8C0, teal)      : Cell membrane lipid bilayer

ONE CARRIED WORLD:
A cross-section of a cell from the extracellular space across the plasma membrane bilayer
into the cytosol and down to the golden nuclear rim and DNA. Membrane-only scenes zoom in
on the receptor bilayer while keeping the same receptor geometry, colours, and side-by-side
positions.

WHAT CHANGES IN EACH SPOKEN SCENE (and what drives it):
- s01_hook             : Always-active Type II catalytic arcs + orbiting active-site beads rotate with a phase tracker while locked Type I separates laterally; a dashed pathway arrow + tracer dot grows down to DNA.
- s02_two_receptors    : A 4-step multi-enzyme relay fires sequentially with a signal bead tracing down to DNA, then clears away as the membrane expands; Type II catalytic arcs and match-flame cue activate while Type I stays locked.
- s03_bridge           : Type I receptors settle apart locked by GS + FKBP12; an amber TGF-beta dimer descends, two cyan Type II chains slide inward to clamp it, and two indigo Type I chains glide laterally into a 4-receptor complex.
- s04_predict          : The 4-receptor complex resets to separated receptors with Type II's active site switched off (broken ring) and the amber TGF-beta dimer hovering above as the question card enters.
- s06_reveal_transphos : Question card clears; the four outer chains assemble around TGF-beta while inner Type I stays blocked; Type II restores, yellow P discs + transfer arrows jump onto GS, FKBP12 pops off, and GS opens lighting Type I.
- s07_smad_shortcut    : An emerald R-Smad (MH1 + MH2 + tail) glides up from cytosol to dock on Type I's phosphorylated GS pocket, receives two yellow P discs on its tail, detaches slightly, and links straight toward DNA.
- s08_smad4_trimer     : Two phosphorylated R-Smads slot tail-to-pocket with one violet Smad4 into a 3-part ring that enters the nucleus onto DNA while active Type I turns over a second R-Smad batch.
- s09_two_branches     : The membrane splits into two parallel bays (TGF-beta/activin -> Smad2/3 vs. BMP tightly gripping Type I -> Smad1/5/8); receptors clamp ligands, yellow P flows one way in both, and both converge on shared violet Smad4.
- s10_return_rule      : View unifies to the single membrane; TGF-beta bridges Type II and Type I, FKBP12 pops off, a yellow P pulse rides all the way through the Smad4 trimer to DNA, and two '?' branches diverge.
"""

from bp_parts import *

# ---- Concept Palette ----
TYPE2_COL = BLUE        # #58C4DD cyan
TYPE1_COL = "#7B88FF"   # indigo
LIGAND_COL = "#F29938"  # amber
FKBP_COL = GREY         # #8B93A1 slate
PHOS_COL = YELLOW       # #F5D547 bright yellow
RSMAD_COL = "#4CD48B"   # emerald green
SMAD4_COL = "#C27CFF"   # violet
BMP_COL = RED           # #FC6255 coral
NUC_COL = GOLD          # #D4A843 gold
MEM_COL = TEAL          # #3FB8C0 teal


# ==============================================================================
# Reusable Biological Schematic Builders (no molecular structures)
# ==============================================================================

def make_membrane(x0=-6.4, x1=6.4, y=1.5, gap=0.24):
    """Lipid bilayer cross-section: two parallel lines with a tinted core."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    band = Rectangle(
        width=w, height=gap, stroke_width=0,
        fill_color=MEM_COL, fill_opacity=0.22,
    ).move_to([cx, y, 0])
    top = Line([x0, y + gap / 2, 0], [x1, y + gap / 2, 0], color=MEM_COL, stroke_width=3.5)
    bot = Line([x0, y - gap / 2, 0], [x1, y - gap / 2, 0], color=MEM_COL, stroke_width=3.5)
    g = VGroup(band, top, bot)
    g.layout_ok = True  # membrane lines span behind receptor stalks by design
    return g


def make_nucleus_band(y_rim=-2.05, x0=-6.3, x1=6.3, y_dna=None):
    """Glowing golden nuclear envelope arc with schematic DNA strand below."""
    pts = [
        np.array([x0, y_rim - 0.35, 0]),
        np.array([(x0 + x1) / 2, y_rim + 0.12, 0]),
        np.array([x1, y_rim - 0.35, 0]),
    ]
    rim = ArcBetweenPoints(pts[0], pts[2], angle=-0.20, color=NUC_COL, stroke_width=5.0)
    glow = ArcBetweenPoints(pts[0], pts[2], angle=-0.20, color=NUC_COL, stroke_width=16.0).set_stroke(opacity=0.24)
    rim.layout_ok = True
    glow.layout_ok = True

    if y_dna is None:
        y_dna = y_rim - 0.95
    s1 = FunctionGraph(lambda x: y_dna + 0.08 * np.sin(2.4 * x), x_range=[-2.3, 2.3], color=NUC_COL, stroke_width=3.6)
    s2 = FunctionGraph(lambda x: y_dna - 0.08 * np.sin(2.4 * x), x_range=[-2.3, 2.3], color=TEXT, stroke_width=2.8)
    dna_lbl = T("DNA", size=28, color=NUC_COL, weight=BOLD).move_to([3.1, y_dna, 0])
    nuc_lbl = T("Nucleus", size=28, color=NUC_COL).move_to([-3.7, y_dna, 0])
    g = VGroup(glow, rim, s1, s2, dna_lbl, nuc_lbl)
    g.dna_center = np.array([0.0, y_dna, 0.0])
    g.rim_y = y_rim
    return g


def make_phos(radius=0.22, size=22):
    """Bright yellow phosphate disc ('P') with generous padding so border never touches text."""
    circ = Circle(radius=radius, color=PHOS_COL, stroke_color=GOLD, stroke_width=2.5,
                  fill_color=PHOS_COL, fill_opacity=0.96)
    txt = T("P", size=size, color=BG, weight=BOLD).move_to(circ)
    g = VGroup(circ, txt)
    g.set_z_index(12)
    return g


def make_dimer(color=LIGAND_COL, width=1.65, lobe_h=0.60):
    """Schematic two-lobe ligand dimer (no molecular structure)."""
    r = lobe_h / 2
    lw = width * 0.44
    left_lobe = RoundedRectangle(corner_radius=r * 0.85, width=lw, height=lobe_h,
                                 stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.45)
    right_lobe = RoundedRectangle(corner_radius=r * 0.85, width=lw, height=lobe_h,
                                  stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.45)
    bridge = Rectangle(width=width * 0.26, height=lobe_h * 0.36,
                       stroke_color=color, stroke_width=2.8, fill_color=color, fill_opacity=0.65)
    left_lobe.move_to(LEFT * (width * 0.26))
    right_lobe.move_to(RIGHT * (width * 0.26))
    bridge.move_to(ORIGIN)
    return VGroup(bridge, left_lobe, right_lobe)


def make_active_arc(center_fn, radius=0.34, color=PHOS_COL, phase_tracker=None, offset=0.0):
    """Rotating catalytic readiness arc + catalytic bead tied dynamically to center_fn()."""
    if phase_tracker is None:
        return Arc(radius=radius, start_angle=0.3, angle=1.45 * PI, arc_center=center_fn(),
                   color=color, stroke_width=6.5)

    def _build():
        c = center_fn()
        ang = phase_tracker.get_value() + offset
        arc = Arc(radius=radius, start_angle=ang, angle=1.35 * PI, arc_center=c, color=color, stroke_width=6.8)
        tip = c + radius * np.array([np.cos(ang + 1.35 * PI), np.sin(ang + 1.35 * PI), 0.0])
        bead = Dot(tip, radius=0.075, color=TEXT)
        return VGroup(arc, bead)

    return always_redraw(_build)


def make_flame_icon(pos, scale=1.0):
    """Minimal geometric 'lit match' spark/flame icon (NOT a molecular structure)."""
    outer = Polygon(
        pos + UP * 0.34 * scale,
        pos + RIGHT * 0.18 * scale + UP * 0.04 * scale,
        pos + DOWN * 0.18 * scale,
        pos + LEFT * 0.18 * scale + UP * 0.04 * scale,
        color=LIGAND_COL, stroke_width=2.2, fill_color=LIGAND_COL, fill_opacity=0.90,
    )
    inner = Polygon(
        pos + UP * 0.17 * scale,
        pos + RIGHT * 0.09 * scale,
        pos + DOWN * 0.10 * scale,
        pos + LEFT * 0.09 * scale,
        color=PHOS_COL, stroke_width=1.5, fill_color=PHOS_COL, fill_opacity=0.96,
    )
    return VGroup(outer, inner)


def make_dead_site(center, scale=1.0):
    """Broken/crossed catalytic ring for kinase-dead Type II."""
    r = 0.24 * scale
    return VGroup(
        Circle(radius=r + 0.06 * scale, color=GREY, stroke_width=3.2).move_to(center),
        Line(center + UL * r * 0.72, center + DR * r * 0.72, color=RED, stroke_width=4.5),
        Line(center + UR * r * 0.72, center + DL * r * 0.72, color=RED, stroke_width=4.5),
    )


def make_type2(x, y_mem, side="left", active=True, dead=False, scale=1.0, phase_tracker=None):
    """
    Type II receptor serine/threonine kinase spanning membrane at y_mem.
    Active arc tracks lobe.get_center() dynamically so moving the receptor moves the arc.
    """
    col = TYPE2_COL
    outer = RoundedRectangle(
        corner_radius=0.14, width=0.62 * scale, height=0.84 * scale,
        stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=0.30,
    ).move_to([x, y_mem + 0.56 * scale, 0])

    stalk = Rectangle(
        width=0.20 * scale, height=0.56 * scale,
        stroke_color=col, stroke_width=2.8, fill_color=col, fill_opacity=0.42,
    ).move_to([x, y_mem, 0])

    fill_op = 0.08 if dead else (0.32 if active else 0.16)
    lobe_col = GREY if dead else col
    lobe = RoundedRectangle(
        corner_radius=0.22, width=1.10 * scale, height=1.22 * scale,
        stroke_color=lobe_col, stroke_width=3.6, fill_color=lobe_col, fill_opacity=fill_op,
    ).move_to([x, y_mem - 0.94 * scale, 0])

    if dead:
        site = make_dead_site(lobe.get_center(), scale=scale)
    elif active:
        site = make_active_arc(
            lobe.get_center, radius=0.32 * scale, color=PHOS_COL,
            phase_tracker=phase_tracker, offset=(0.0 if side == "left" else PI),
        )
    else:
        site = Circle(radius=0.22 * scale, color=col, stroke_width=2.5).set_opacity(0.45).move_to(lobe.get_center())

    g = VGroup(stalk, outer, lobe, site)
    g.outer = outer
    g.stalk = stalk
    g.lobe = lobe
    g.site = site
    g.side = side
    return g


def make_type1(x, y_mem, side="left", locked=True, active=False, gs_open=False,
               phos_gs=0, scale=1.0, phase_tracker=None, show_fkbp=None):
    """
    Type I receptor serine/threonine kinase with hinged GS flap and FKBP12 safety catch.
    When phosphorylated (phos_gs > 0), P discs sit cleanly inside the upper GS zone of the
    Type I lobe with generous spacing so they never straddle or have tight borders.
    """
    if show_fkbp is None:
        show_fkbp = locked
    sgn = 1.0 if side == "left" else -1.0
    col = TYPE1_COL

    outer = RoundedRectangle(
        corner_radius=0.14, width=0.58 * scale, height=0.78 * scale,
        stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=0.28,
    ).move_to([x, y_mem + 0.52 * scale, 0])

    stalk = Rectangle(
        width=0.20 * scale, height=0.86 * scale,
        stroke_color=col, stroke_width=2.8, fill_color=col, fill_opacity=0.42,
    ).move_to([x, y_mem - 0.27 * scale, 0])

    fill_op = 0.34 if active else 0.18
    lobe_h = (1.50 if phos_gs > 0 else 1.24) * scale
    lobe_w = (1.36 if phos_gs > 0 else 1.12) * scale
    lobe = RoundedRectangle(
        corner_radius=0.22, width=lobe_w, height=lobe_h,
        stroke_color=col, stroke_width=3.6, fill_color=col, fill_opacity=fill_op,
    ).move_to([x, y_mem - (0.68 * scale + lobe_h / 2), 0])

    gs_col = PHOS_COL if phos_gs > 0 else col
    gs_flap = RoundedRectangle(
        corner_radius=0.08, width=1.12 * scale, height=0.20 * scale,
        stroke_color=gs_col, stroke_width=3.0, fill_color=gs_col, fill_opacity=0.36 if phos_gs else 0.28,
    ).move_to(lobe.get_top() + UP * 0.04 * scale)

    if gs_open:
        pivot = gs_flap.get_left() if side == "left" else gs_flap.get_right()
        gs_flap.rotate(-sgn * 1.92, about_point=pivot)

    p_group = VGroup()
    if phos_gs >= 1:
        p1 = make_phos(radius=0.21, size=22).move_to(lobe.get_top() + LEFT * 0.23 + DOWN * 0.38)
        p_group.add(p1)
    if phos_gs >= 2:
        p2 = make_phos(radius=0.21, size=22).move_to(lobe.get_top() + RIGHT * 0.23 + DOWN * 0.38)
        p_group.add(p2)

    fkbp = VGroup()
    if show_fkbp:
        cap = RoundedRectangle(
            corner_radius=0.11, width=0.78 * scale, height=0.34 * scale,
            stroke_color=FKBP_COL, stroke_width=2.8, fill_color=FKBP_COL, fill_opacity=0.45,
        ).move_to(gs_flap.get_center() + UP * 0.25 * scale)
        fkbp.add(cap)

    arc_offset = DOWN * (0.28 * scale if phos_gs > 0 else 0.10 * scale)
    arc_rad = 0.24 * scale if phos_gs > 0 else 0.30 * scale
    if active:
        site = make_active_arc(
            lambda l=lobe, o=arc_offset: l.get_center() + o,
            radius=arc_rad, color=PHOS_COL,
            phase_tracker=phase_tracker, offset=(0.6 if side == "left" else 3.7),
        )
    else:
        site = Circle(radius=0.21 * scale, color=col, stroke_width=2.2).set_opacity(0.42).move_to(
            lobe.get_center() + arc_offset
        )

    g = VGroup(stalk, outer, lobe, gs_flap, site, p_group, fkbp)
    g.outer = outer
    g.stalk = stalk
    g.lobe = lobe
    g.gs_flap = gs_flap
    g.fkbp = fkbp
    g.p_group = p_group
    g.site = site
    g.side = side
    g.arc_offset = arc_offset
    return g


def make_rsmad(color=RSMAD_COL, show_domains=True, phos_tail=0, pocket_dir=RIGHT, scale=1.0):
    """
    Schematic R-Smad with MH1 lobe, linker, wide MH2 lobe (clear pocket notch), and C-terminal tail.
    """
    mh1_w = max(1.38 * scale, 1.18)
    mh2_w = max(1.54 * scale, 1.38)
    mh1 = RoundedRectangle(
        corner_radius=0.22, width=mh1_w, height=0.76 * scale,
        stroke_color=color, stroke_width=3.4, fill_color=color, fill_opacity=0.30,
    )
    mh2 = RoundedRectangle(
        corner_radius=0.22, width=mh2_w, height=0.82 * scale,
        stroke_color=color, stroke_width=3.4, fill_color=color, fill_opacity=0.34,
    )
    mh1.move_to(DOWN * 0.58 * scale)
    mh2.move_to(UP * 0.44 * scale)

    linker = Line(mh1.get_top(), mh2.get_bottom(), color=color, stroke_width=4.5)

    p_dir = np.array(pocket_dir, dtype=float)
    pocket = RoundedRectangle(
        corner_radius=0.06, width=0.24 * scale, height=0.28 * scale,
        stroke_color=color, stroke_width=2.4, fill_color=BG, fill_opacity=0.96,
    ).move_to(mh2.get_center() + p_dir * (mh2_w / 2 - 0.13 * scale))

    tail_start = mh2.get_top()
    tail_end = tail_start + UP * 0.52 * scale
    tail = Line(tail_start, tail_end, color=color, stroke_width=5.0)

    p_discs = VGroup()
    if phos_tail >= 1:
        p_discs.add(make_phos(radius=0.21, size=22).move_to(tail_end + LEFT * 0.27 + UP * 0.26))
    if phos_tail >= 2:
        p_discs.add(make_phos(radius=0.21, size=22).move_to(tail_end + RIGHT * 0.27 + UP * 0.26))

    parts = VGroup(linker, mh1, mh2, pocket, tail, p_discs)
    if show_domains:
        dom_size = max(22, int(round(26 * scale)))
        t1 = T("MH1", size=dom_size, color=TEXT, weight=BOLD).move_to(mh1)
        t2 = T("MH2", size=dom_size, color=TEXT, weight=BOLD).move_to(mh2.get_center() - p_dir * 0.16 * scale)
        parts.add(t1, t2)

    parts.mh1 = mh1
    parts.mh2 = mh2
    parts.pocket = pocket
    parts.tail = tail
    parts.p_discs = p_discs
    return parts


def make_smad4(scale=1.0, label="Smad4"):
    """Violet shared partner Smad4 with wide body so notches stay clear of label."""
    body = RoundedRectangle(
        corner_radius=0.30, width=2.08 * scale, height=1.02 * scale,
        stroke_color=SMAD4_COL, stroke_width=3.5, fill_color=SMAD4_COL, fill_opacity=0.32,
    )
    notch_l = RoundedRectangle(
        corner_radius=0.06, width=0.22 * scale, height=0.26 * scale,
        stroke_color=SMAD4_COL, stroke_width=2.4, fill_color=BG, fill_opacity=0.96,
    ).move_to(body.get_left() + RIGHT * 0.14 * scale)
    notch_r = RoundedRectangle(
        corner_radius=0.06, width=0.22 * scale, height=0.26 * scale,
        stroke_color=SMAD4_COL, stroke_width=2.4, fill_color=BG, fill_opacity=0.96,
    ).move_to(body.get_right() + LEFT * 0.14 * scale)
    lbl = T(label, size=26, color=TEXT, weight=BOLD).move_to(body)
    g = VGroup(body, notch_l, notch_r, lbl)
    g.body = body
    return g


def make_compact_trimer(rsmad_col=RSMAD_COL, smad_label="R-Smad", scale=1.0):
    """Compact 3-part ring: 2 phosphorylated R-Smads + 1 violet Smad4 with generous padding."""
    if scale >= 0.99:
        sw, sh, s4w = 1.72, 0.82, 1.80
        sx, sy, s4y = 1.18, 0.62, -0.72
        px, py, pr = 0.74, -0.05, 0.21
        t_size, p_size = 24, 22
    else:
        # Keep font_size >= 22 while shrinking geometry so trimer fits cleanly inside nucleus.
        sw = max(1.72 * scale, 1.32)
        s4w = max(1.80 * scale, 1.36)
        sh = 0.44
        sx = max(1.18 * scale, sw / 2 + 0.12)
        sy = 0.52
        s4y = -0.52
        px, py, pr = 0.52, 0.0, 0.21
        t_size, p_size = 22, 22

    s_left = RoundedRectangle(
        corner_radius=0.22 * scale, width=sw, height=sh,
        stroke_color=rsmad_col, stroke_width=3.4, fill_color=rsmad_col, fill_opacity=0.32,
    ).move_to([-sx, sy, 0])
    s_right = RoundedRectangle(
        corner_radius=0.22 * scale, width=sw, height=sh,
        stroke_color=rsmad_col, stroke_width=3.4, fill_color=rsmad_col, fill_opacity=0.32,
    ).move_to([sx, sy, 0])
    s4 = RoundedRectangle(
        corner_radius=0.24 * scale, width=s4w, height=sh,
        stroke_color=SMAD4_COL, stroke_width=3.6, fill_color=SMAD4_COL, fill_opacity=0.34,
    ).move_to([0.0, s4y, 0])

    t_l = T(smad_label, size=t_size, color=TEXT, weight=BOLD).move_to(s_left)
    t_r = T(smad_label, size=t_size, color=TEXT, weight=BOLD).move_to(s_right)
    t_4 = T("Smad4", size=t_size, color=TEXT, weight=BOLD).move_to(s4)

    p1 = make_phos(radius=pr, size=p_size).move_to([-px, py, 0])
    p2 = make_phos(radius=pr, size=p_size).move_to([px, py, 0])

    top_link = Line(s_left.get_right(), s_right.get_left(), color=rsmad_col, stroke_width=3.8)
    l1 = Line(s_left.get_bottom() + RIGHT * 0.25 * scale, p1.get_top(), color=PHOS_COL, stroke_width=3.2)
    l2 = Line(p1.get_bottom(), s4.get_top() + LEFT * 0.45 * scale, color=PHOS_COL, stroke_width=3.2)
    r1 = Line(s_right.get_bottom() + LEFT * 0.25 * scale, p2.get_top(), color=PHOS_COL, stroke_width=3.2)
    r2 = Line(p2.get_bottom(), s4.get_top() + RIGHT * 0.45 * scale, color=PHOS_COL, stroke_width=3.2)

    g = VGroup(top_link, l1, l2, r1, r2, s_left, s_right, s4, p1, p2, t_l, t_r, t_4)
    g.s_left = s_left
    g.s_right = s_right
    g.s4 = s4
    return g


def make_fkbp_label(t1_r):
    """Place FKBP12 label cleanly below the membrane bilayer with a short leader to t1_r.fkbp."""
    lbl = T("FKBP12", size=24, color=TEXT, weight=BOLD).next_to(t1_r.lobe, RIGHT, buff=0.22)
    lbl.set_y(t1_r.fkbp.get_y() - 0.30)
    leader = Line(
        lbl.get_top() + LEFT * 0.22 + UP * 0.08,
        t1_r.fkbp.get_corner(DR) + UP * 0.06,
        color=FKBP_COL, stroke_width=2.5,
    )
    return VGroup(lbl, leader)


def build_predict_backdrop():
    """
    Shared world builder for S04Predict end state and S05Pause.backdrop().
    Separated kinase-dead Type II + normal locked Type I, with amber TGF-beta hovering above.
    """
    y_mem = 1.45
    mem = make_membrane(-6.3, 6.3, y=y_mem)
    t2_l = make_type2(-1.45, y_mem, side="left", active=False, dead=True, scale=1.02)
    t2_r = make_type2(1.45, y_mem, side="right", active=False, dead=True, scale=1.02)
    t1_l = make_type1(-4.35, y_mem, side="left", locked=True, active=False, scale=1.02)
    t1_r = make_type1(4.35, y_mem, side="right", locked=True, active=False, scale=1.02)

    dimer = make_dimer(LIGAND_COL, width=1.60, lobe_h=0.56).move_to([0.0, y_mem + 1.25, 0])
    dimer_lbl = T("TGF-β dimer", size=28, color=LIGAND_COL, weight=BOLD).next_to(dimer, UP, buff=0.14)

    t2_lbl = T("Type II (kinase-dead)", size=28, color=TEXT, weight=BOLD).move_to([0.0, y_mem - 2.30, 0])
    t1_l_lbl = T("Type I (normal)", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_l.lobe, DOWN, buff=0.22)
    t1_r_lbl = T("Type I (normal)", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_r.lobe, DOWN, buff=0.22)
    fkbp_r_lbl = make_fkbp_label(t1_r)

    tag = scope_tag("schematic")
    g = VGroup(mem, t2_l, t2_r, t1_l, t1_r, dimer, dimer_lbl, t2_lbl, t1_l_lbl, t1_r_lbl, fkbp_r_lbl, tag)
    g.parts = dict(
        mem=mem, t2_l=t2_l, t2_r=t2_r, t1_l=t1_l, t1_r=t1_r,
        dimer=dimer, dimer_lbl=dimer_lbl, t2_lbl=t2_lbl,
        t1_l_lbl=t1_l_lbl, t1_r_lbl=t1_r_lbl, fkbp_r_lbl=fkbp_r_lbl, tag=tag,
    )
    return g


# ==============================================================================
# Scenes
# ==============================================================================

class S00Title(TitleCard):
    LESSON = "TGF-β and Smads"
    TITLE = "One-Way Relay: Two Kinases to a Smad"


class S01Hook(SpokenScene):
    """
    Hook: active Type II sits in the membrane while locked Type I separates laterally;
    a dashed path arrow + signal tracer grows down to DNA to pose the opening question.
    """
    def construct(self):
        y_mem = 1.65
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        mem = make_membrane(-6.3, 6.3, y=y_mem)
        nuc = make_nucleus_band(y_rim=-2.05)

        t2_l = make_type2(-3.3, y_mem, side="left", active=True, scale=1.08, phase_tracker=phase)
        t2_r = make_type2(-1.4, y_mem, side="right", active=True, scale=1.08, phase_tracker=phase)
        t1_l = make_type1(1.6, y_mem, side="left", locked=True, active=False, scale=1.08)
        t1_r = make_type1(3.6, y_mem, side="right", locked=True, active=False, scale=1.08)

        t2_lbl = T("Type II (active)", size=28, color=TYPE2_COL, weight=BOLD).move_to([-2.35, y_mem - 2.12, 0])
        t1_lbl = T("Type I (locked)", size=28, color=TYPE1_COL, weight=BOLD).move_to([2.60, y_mem - 2.38, 0])
        tag = scope_tag("schematic")

        self.add(mem, nuc, t2_l, t2_r, t1_l, t1_r, t2_lbl, t1_lbl, tag)

        # Lateral membrane drift keeping Type I separated from Type II
        self.play(
            t1_l.animate.shift(RIGHT * 0.65),
            t1_r.animate.shift(RIGHT * 0.65),
            t1_lbl.animate.shift(RIGHT * 0.65),
            run_time=3.5,
        )

        self.at("stays quiet")
        self.play(
            t2_l.lobe.animate.set_fill(TYPE2_COL, opacity=0.48),
            t2_r.lobe.animate.set_fill(TYPE2_COL, opacity=0.48),
            rate_func=there_and_back, run_time=2.0,
        )

        self.at("holds it back")
        tgf_q = T("TGF-β ?", size=32, color=LIGAND_COL, weight=BOLD).move_to([-2.35, y_mem + 1.80, 0])
        lock_ring = SurroundingRectangle(t1_l.fkbp, color=PHOS_COL, corner_radius=0.10, buff=0.08, stroke_width=3.6)
        self.play(FadeIn(tgf_q), Create(lock_ring), run_time=1.0)
        self.play(
            tgf_q.animate.shift(DOWN * 0.45),
            lock_ring.animate.set_stroke(width=5.5),
            rate_func=smooth, run_time=2.4,
        )

        self.at("reach DNA")
        start_pt = np.array([-0.4, y_mem - 1.65, 0])
        end_pt = np.array([0.0, nuc.dna_center[1] + 0.40, 0])
        arrow_path = DashedLine(start_pt, end_pt, color=PHOS_COL, stroke_width=5.0, dash_length=0.20)
        arrow_tip = Triangle(color=PHOS_COL, fill_color=PHOS_COL, fill_opacity=1.0).scale(0.16).rotate(PI).move_to(
            end_pt + DOWN * 0.03
        )
        tracer = Dot(start_pt, radius=0.15, color=PHOS_COL)
        q_mark = T("?", size=40, color=PHOS_COL, weight=BOLD).next_to(arrow_path, RIGHT, buff=0.24)
        self.play(Create(arrow_path), MoveAlongPath(tracer, Line(start_pt, end_pt)), FadeIn(q_mark), run_time=2.2)
        self.play(FadeIn(arrow_tip), FadeOut(tracer), run_time=0.4)
        self.finish()


class S02TwoReceptors(SpokenScene):
    """
    Left side shows a multi-enzyme cascade that clears away as the membrane expands;
    Type II glows always-active (lit match) while Type I stays locked.
    """
    def construct(self):
        y_mem = 1.65
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        chain_boxes = VGroup(*[
            boxed_label(f"Enzyme {i}", GREY, size=24, box=(1.9, 0.56))
            for i in range(1, 5)
        ]).arrange(DOWN, buff=0.42).move_to([-4.2, 0.35, 0])
        chain_arrows = VGroup(*[
            Arrow(chain_boxes[i].get_bottom(), chain_boxes[i + 1].get_top(), buff=0.06,
                  color=GREY, stroke_width=3.2, max_tip_length_to_length_ratio=0.25)
            for i in range(3)
        ])
        chain_head = T("Multi-step relay", size=26, color=TEXT).next_to(chain_boxes, UP, buff=0.22)
        chain_grp = VGroup(chain_head, chain_boxes, chain_arrows)

        mem = make_membrane(-0.8, 6.3, y=y_mem)
        t2_l = make_type2(0.8, y_mem, side="left", active=True, scale=0.95, phase_tracker=phase)
        t2_r = make_type2(2.4, y_mem, side="right", active=True, scale=0.95, phase_tracker=phase)
        t1_l = make_type1(4.0, y_mem, side="left", locked=True, active=False, scale=0.95)
        t1_r = make_type1(5.5, y_mem, side="right", locked=True, active=False, scale=0.95)
        nuc = make_nucleus_band(y_rim=-2.05)
        tag = scope_tag("schematic")

        self.add(chain_head, chain_boxes[0], mem, t2_l, t2_r, t1_l, t1_r, nuc, tag)

        for i in range(3):
            self.play(GrowArrow(chain_arrows[i]), FadeIn(chain_boxes[i + 1]), run_time=1.7)

        # Signal bead propagates down the outside of the 4-enzyme relay while "before any gene responds" finishes
        sig_bead = Dot(chain_boxes[0].get_right() + RIGHT * 0.28, radius=0.14, color=PHOS_COL)
        self.play(FadeIn(sig_bead), run_time=0.3)
        self.play(sig_bead.animate.move_to(chain_boxes[3].get_right() + RIGHT * 0.28), run_time=3.1)

        self.at("takes a shortcut")
        new_mem = make_membrane(-6.3, 6.3, y=y_mem)
        self.play(
            FadeOut(chain_grp, shift=LEFT * 0.4), FadeOut(sig_bead),
            Transform(mem, new_mem),
            t2_l.animate.shift(LEFT * 4.1),
            t2_r.animate.shift(LEFT * 4.0),
            t1_l.animate.shift(LEFT * 1.7),
            t1_r.animate.shift(LEFT * 1.2),
            run_time=1.8,
        )

        self.at("serine and threonine")
        head = T("Serine / threonine kinases", size=32, color=TEXT, weight=BOLD).move_to([0.0, HEAD_Y, 0])
        t2_lbl = T("Type II", size=30, color=TYPE2_COL, weight=BOLD).move_to([-2.45, y_mem - 2.05, 0])
        t1_lbl = T("Type I", size=30, color=TYPE1_COL, weight=BOLD).move_to([3.30, y_mem - 2.18, 0])
        self.play(FadeIn(head), FadeIn(t2_lbl), FadeIn(t1_lbl), run_time=1.2)

        self.at("stays active")
        flame_l = make_flame_icon(t2_l.lobe.get_center() + DOWN * 0.85, scale=1.08)
        flame_r = make_flame_icon(t2_r.lobe.get_center() + DOWN * 0.85, scale=1.08)
        always_lbl = T("Always active", size=28, color=PHOS_COL, weight=BOLD).next_to(t2_lbl, DOWN, buff=0.28)

        self.play(
            FadeIn(flame_l, scale=0.7), FadeIn(flame_r, scale=0.7),
            FadeIn(always_lbl),
            run_time=1.2,
        )
        self.play(
            flame_l.animate.scale(1.18), flame_r.animate.scale(1.18),
            rate_func=there_and_back, run_time=2.8,
        )
        self.finish()


class S03Bridge(SpokenScene):
    """
    Zoomed upper-membrane view: Type I is locked by GS + FKBP12; amber TGF-beta dimer
    descends, binds two cyan Type II chains first, and pulls two indigo Type I chains into a 4-receptor complex.
    """
    def construct(self):
        y_mem = 1.20
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        mem = make_membrane(-6.3, 6.3, y=y_mem)
        t2_l = make_type2(-1.45, y_mem, side="left", active=True, scale=1.12, phase_tracker=phase)
        t2_r = make_type2(1.45, y_mem, side="right", active=True, scale=1.12, phase_tracker=phase)
        t1_l = make_type1(-4.25, y_mem, side="left", locked=True, active=False, scale=1.12)
        t1_r = make_type1(4.25, y_mem, side="right", locked=True, active=False, scale=1.12)

        t2_lbl = T("Type II", size=30, color=TYPE2_COL, weight=BOLD).move_to([0.0, y_mem - 2.25, 0])
        t1_lbl_l = T("Type I (locked)", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_l.lobe, DOWN, buff=0.22)
        t1_lbl_r = T("Type I (locked)", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_r.lobe, DOWN, buff=0.22)
        tag = scope_tag("schematic")

        self.add(mem, t2_l, t2_r, t1_l, t1_r, t2_lbl, t1_lbl_l, t1_lbl_r, tag)

        # Locked Type I chains separate outward to rest apart from Type II
        self.play(
            t1_l.animate.shift(LEFT * 0.40),
            t1_r.animate.shift(RIGHT * 0.40),
            t1_lbl_l.animate.shift(LEFT * 0.40),
            t1_lbl_r.animate.shift(RIGHT * 0.40),
            run_time=3.2,
        )

        self.at("GS domain folds")
        gs_hi_l = SurroundingRectangle(t1_l.gs_flap, color=PHOS_COL, corner_radius=0.08, buff=0.06, stroke_width=3.2)
        gs_hi_r = SurroundingRectangle(t1_r.gs_flap, color=PHOS_COL, corner_radius=0.08, buff=0.06, stroke_width=3.2)
        gs_lbl = T("GS domain (regulatory stretch)", size=28, color=PHOS_COL, weight=BOLD).move_to([-2.95, -2.05, 0])
        self.play(Create(gs_hi_l), Create(gs_hi_r), FadeIn(gs_lbl), run_time=1.5)

        self.at("safety catch")
        fk_hi_l = SurroundingRectangle(t1_l.fkbp, color=TEXT, corner_radius=0.08, buff=0.06, stroke_width=3.2)
        fk_hi_r = SurroundingRectangle(t1_r.fkbp, color=TEXT, corner_radius=0.08, buff=0.06, stroke_width=3.2)
        fk_lbl = T("FKBP12 cap", size=28, color=TEXT, weight=BOLD).move_to([2.95, -2.05, 0])
        self.play(
            FadeOut(gs_hi_l), FadeOut(gs_hi_r),
            Create(fk_hi_l), Create(fk_hi_r), FadeIn(fk_lbl),
            run_time=1.6,
        )

        self.at("amber TGF")
        self.play(FadeOut(fk_hi_l), FadeOut(fk_hi_r), FadeOut(gs_lbl), FadeOut(fk_lbl), run_time=0.6)
        dimer = make_dimer(LIGAND_COL, width=1.65, lobe_h=0.58).move_to([0.0, y_mem + 1.50, 0])
        dimer_lbl = T("TGF-β dimer", size=28, color=LIGAND_COL, weight=BOLD).next_to(dimer, UP, buff=0.14)
        self.play(FadeIn(dimer, shift=DOWN * 0.15), FadeIn(dimer_lbl), run_time=0.9)
        self.play(
            dimer.animate.move_to([0.0, y_mem + 0.82, 0]),
            dimer_lbl.animate.move_to([0.0, y_mem + 1.48, 0]),
            run_time=2.5,
        )

        self.at("binds two cyan")
        self.play(
            t2_l.animate.shift(RIGHT * 0.50),
            t2_r.animate.shift(LEFT * 0.50),
            run_time=2.0,
        )

        self.at("pulls two indigo")
        head = T("4-receptor complex", size=32, color=TEXT, weight=BOLD).move_to([0.0, HEAD_Y, 0])
        self.play(
            t1_l.animate.shift(RIGHT * 2.40),
            t1_r.animate.shift(LEFT * 2.40),
            t1_lbl_l.animate.move_to([-3.65, y_mem - 2.50, 0]),
            t1_lbl_r.animate.move_to([3.65, y_mem - 2.50, 0]),
            FadeIn(head),
            run_time=2.6,
        )
        self.finish()


class S04Predict(SpokenScene):
    """
    Predict setup: separate receptors back to resting positions, break Type II kinase,
    keep Type I normal, hover TGF-beta above, and show question card matching S05Pause.
    """
    def construct(self):
        y_mem = 1.45
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        mem = make_membrane(-6.3, 6.3, y=y_mem)
        t2_l = make_type2(-0.95, y_mem, side="left", active=True, scale=1.02, phase_tracker=phase)
        t2_r = make_type2(0.95, y_mem, side="right", active=True, scale=1.02, phase_tracker=phase)
        t1_l = make_type1(-2.25, y_mem, side="left", locked=True, active=False, scale=1.02)
        t1_r = make_type1(2.25, y_mem, side="right", locked=True, active=False, scale=1.02)
        t2_lbl = T("Type II (active)", size=28, color=TYPE2_COL, weight=BOLD).move_to([0.0, y_mem - 2.15, 0])
        t1_l_lbl = T("Type I", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_l.lobe, DOWN, buff=0.22)
        t1_r_lbl = T("Type I", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_r.lobe, DOWN, buff=0.22)
        tag = scope_tag("schematic")

        self.add(mem, t2_l, t2_r, t1_l, t1_r, t2_lbl, t1_l_lbl, t1_r_lbl, tag)

        self.play(
            t2_l.animate.shift(LEFT * 0.50),
            t2_r.animate.shift(RIGHT * 0.50),
            t1_l.animate.shift(LEFT * 2.10),
            t1_r.animate.shift(RIGHT * 2.10),
            t1_l_lbl.animate.shift(LEFT * 2.10),
            t1_r_lbl.animate.shift(RIGHT * 2.10),
            run_time=2.2,
        )

        self.at("breaks the type 2")
        t2_l.site.clear_updaters()
        t2_r.site.clear_updaters()
        dead_site_l = make_dead_site(t2_l.lobe.get_center(), scale=1.02)
        dead_site_r = make_dead_site(t2_r.lobe.get_center(), scale=1.02)
        dead_lbl = T("Type II (kinase-dead)", size=28, color=TEXT, weight=BOLD).move_to([0.0, y_mem - 2.30, 0])
        self.play(
            FadeOut(t2_l.site), FadeOut(t2_r.site),
            FadeIn(dead_site_l), FadeIn(dead_site_r),
            t2_l.lobe.animate.set_stroke(GREY).set_fill(GREY, opacity=0.08),
            t2_r.lobe.animate.set_stroke(GREY).set_fill(GREY, opacity=0.08),
            swap(t2_lbl, dead_lbl, run_time=1.0),
            run_time=2.0,
        )

        self.at("type 1 stays normal")
        norm_l = T("Type I (normal)", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_l.lobe, DOWN, buff=0.22)
        norm_r = T("Type I (normal)", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_r.lobe, DOWN, buff=0.22)
        fkbp_r_lbl = make_fkbp_label(t1_r)
        self.play(
            swap(t1_l_lbl, norm_l, run_time=0.8),
            swap(t1_r_lbl, norm_r, run_time=0.8),
            FadeIn(fkbp_r_lbl),
            run_time=1.6,
        )

        self.at("When TGF")
        dimer = make_dimer(LIGAND_COL, width=1.60, lobe_h=0.56).move_to([0.0, y_mem + 1.50, 0])
        dimer_lbl = T("TGF-β dimer", size=28, color=LIGAND_COL, weight=BOLD).next_to(dimer, UP, buff=0.14)
        self.play(FadeIn(dimer), FadeIn(dimer_lbl), run_time=0.8)
        self.play(
            dimer.animate.move_to([0.0, y_mem + 1.25, 0]),
            dimer_lbl.animate.move_to([0.0, y_mem + 1.25 + 0.56 / 2 + 0.14 + dimer_lbl.height / 2, 0]),
            run_time=1.4,
        )

        self.at("still assemble")
        q = question_card(
            "Type II kinase dead: Do receptors assemble? Is Type I phosphorylated?",
            max_w=6.8,
        )
        self.play(FadeIn(q.question), run_time=1.3)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Type II kinase dead: Do receptors assemble? Is Type I phosphorylated?"
    OPTIONS = ()
    CARD = {"max_w": 6.8}
    RING_AT = (5.85, -2.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_backdrop()


class S06RevealTransphos(SpokenScene):
    """
    Reveal: outer assembly happens with kinase-dead Type II, inner GS stays blocked;
    restore Type II kinase -> yellow P discs jump onto GS -> FKBP12 pops off -> Type I opens active.
    """
    def construct(self):
        y_mem = 1.45
        bd = build_predict_backdrop()
        p = bd.parts
        q = question_card(
            "Type II kinase dead: Do receptors assemble? Is Type I phosphorylated?",
            max_w=6.8,
        )
        self.add(bd, q)

        self.at("four chains still")
        self.play(FadeOut(q), FadeOut(p["fkbp_r_lbl"]), run_time=0.5)
        self.play(
            p["dimer"].animate.move_to([0.0, y_mem + 0.78, 0]),
            p["dimer_lbl"].animate.move_to([0.0, y_mem + 1.40, 0]),
            p["t2_l"].animate.shift(RIGHT * 0.52),
            p["t2_r"].animate.shift(LEFT * 0.52),
            p["t1_l_lbl"].animate.move_to([-4.70, y_mem - 2.30, 0]),
            p["t1_r_lbl"].animate.move_to([4.70, y_mem - 2.30, 0]),
            run_time=1.4,
        )
        self.play(
            p["t1_l"].animate.shift(RIGHT * 2.15),
            p["t1_r"].animate.shift(LEFT * 2.15),
            run_time=1.6,
        )
        outer_hi = SurroundingRectangle(
            VGroup(p["t1_l"].outer, p["t1_r"].outer, p["dimer"]),
            color=RSMAD_COL, corner_radius=0.14, buff=0.06, stroke_width=3.2,
        )
        outer_badge = T("Outer assembly: YES", size=30, color=RSMAD_COL, weight=BOLD).move_to([0.0, HEAD_Y + 0.15, 0])
        self.play(
            Create(outer_hi), FadeIn(outer_badge),
            p["t1_l_lbl"].animate.move_to([-4.70, y_mem - 1.15, 0]),
            p["t1_r_lbl"].animate.move_to([4.70, y_mem - 1.15, 0]),
            run_time=1.4,
        )

        self.at("nothing happens")
        inner_badge = T("Type I phosphorylated: NO", size=28, color=RED, weight=BOLD).move_to([0.0, -2.55, 0])
        no_arr_l = Arrow(p["t2_l"].lobe.get_left(), p["t1_l"].lobe.get_right(), color=RED, stroke_width=4.0, buff=0.05)
        no_arr_r = Arrow(p["t2_r"].lobe.get_right(), p["t1_r"].lobe.get_left(), color=RED, stroke_width=4.0, buff=0.05)
        self.play(FadeOut(outer_hi), FadeIn(inner_badge), GrowArrow(no_arr_l), GrowArrow(no_arr_r), run_time=1.5)
        self.play(no_arr_l.animate.set_opacity(0.25), no_arr_r.animate.set_opacity(0.25), rate_func=there_and_back, run_time=2.2)

        self.at("Restore the")
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        act2_l = make_active_arc(p["t2_l"].lobe.get_center, radius=0.32, color=PHOS_COL, phase_tracker=phase, offset=0.0)
        act2_r = make_active_arc(p["t2_r"].lobe.get_center, radius=0.32, color=PHOS_COL, phase_tracker=phase, offset=PI)
        new_t2_lbl = T("Type II (active)", size=28, color=TYPE2_COL, weight=BOLD).move_to([0.0, y_mem - 2.30, 0])

        self.play(
            FadeOut(outer_badge), FadeOut(inner_badge), FadeOut(no_arr_l), FadeOut(no_arr_r),
            FadeOut(p["t2_l"].site), FadeOut(p["t2_r"].site),
            FadeIn(act2_l), FadeIn(act2_r),
            p["t2_l"].lobe.animate.set_stroke(TYPE2_COL).set_fill(TYPE2_COL, opacity=0.36),
            p["t2_r"].lobe.animate.set_stroke(TYPE2_COL).set_fill(TYPE2_COL, opacity=0.36),
            swap(p["t2_lbl"], new_t2_lbl, run_time=0.8),
            run_time=1.8,
        )

        self.at("phosphates jump")
        p_gs_l = make_phos(radius=0.22, size=22)
        p_gs_r = make_phos(radius=0.22, size=22)
        src_l = p["t2_l"].lobe.get_center()
        src_r = p["t2_r"].lobe.get_center()
        dst_l = p["t1_l"].lobe.get_top() + DOWN * 0.34
        dst_r = p["t1_r"].lobe.get_top() + DOWN * 0.34
        path_l = CubicBezier(src_l, src_l + DOWN * 0.55, (src_l + dst_l) / 2 + DOWN * 0.55, dst_l)
        path_r = CubicBezier(src_r, src_r + DOWN * 0.55, (src_r + dst_r) / 2 + DOWN * 0.55, dst_r)
        p_gs_l.move_to(src_l)
        p_gs_r.move_to(src_r)

        tr_l = Arrow(src_l + LEFT * 0.35, dst_l + RIGHT * 0.35, color=PHOS_COL, stroke_width=4.5, buff=0.08)
        tr_r = Arrow(src_r + RIGHT * 0.35, dst_r + LEFT * 0.35, color=PHOS_COL, stroke_width=4.5, buff=0.08)

        self.play(FadeIn(p_gs_l, scale=0.6), FadeIn(p_gs_r, scale=0.6), GrowArrow(tr_l), GrowArrow(tr_r), run_time=0.8)
        self.play(
            MoveAlongPath(p_gs_l, path_l),
            MoveAlongPath(p_gs_r, path_r),
            p["t1_l"].gs_flap.animate.set_stroke(PHOS_COL).set_fill(PHOS_COL, opacity=0.45),
            p["t1_r"].gs_flap.animate.set_stroke(PHOS_COL).set_fill(PHOS_COL, opacity=0.45),
            FadeOut(tr_l), FadeOut(tr_r),
            run_time=2.2,
        )

        self.at("FKBP12")
        self.play(
            p["t1_l"].fkbp.animate.shift(LEFT * 1.8 + DOWN * 0.7).rotate(0.4).set_opacity(0),
            p["t1_r"].fkbp.animate.shift(RIGHT * 1.8 + DOWN * 0.7).rotate(-0.4).set_opacity(0),
            run_time=1.8,
        )

        self.at("opens active")
        act1_l = make_active_arc(
            lambda l=p["t1_l"].lobe: l.get_center() + DOWN * 0.22,
            radius=0.26, color=PHOS_COL, phase_tracker=phase, offset=0.8,
        )
        act1_r = make_active_arc(
            lambda l=p["t1_r"].lobe: l.get_center() + DOWN * 0.22,
            radius=0.26, color=PHOS_COL, phase_tracker=phase, offset=3.9,
        )
        open_lbl_l = T("Type I (active)", size=28, color=TYPE1_COL, weight=BOLD).move_to(p["t1_l_lbl"].get_center())
        open_lbl_r = T("Type I (active)", size=28, color=TYPE1_COL, weight=BOLD).move_to(p["t1_r_lbl"].get_center())

        self.play(
            Rotate(p["t1_l"].gs_flap, angle=-1.92, about_point=p["t1_l"].gs_flap.get_left()),
            Rotate(p["t1_r"].gs_flap, angle=1.92, about_point=p["t1_r"].gs_flap.get_right()),
            p["t1_l"].lobe.animate.set_fill(TYPE1_COL, opacity=0.38),
            p["t1_r"].lobe.animate.set_fill(TYPE1_COL, opacity=0.38),
            FadeOut(p["t1_l"].site), FadeOut(p["t1_r"].site),
            FadeIn(act1_l), FadeIn(act1_r),
            swap(p["t1_l_lbl"], open_lbl_l, run_time=0.8),
            swap(p["t1_r_lbl"], open_lbl_r, run_time=0.8),
            run_time=2.2,
        )
        self.finish()


class S07SmadShortcut(SpokenScene):
    """
    Active Type I docks emerald R-Smad (MH1 + MH2 + tail), adds two yellow P discs to its tail,
    and shows the direct Type II -> Type I -> R-Smad shortcut toward DNA.
    """
    def construct(self):
        y_mem = 2.05
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        mem = make_membrane(-6.3, 6.3, y=y_mem)
        nuc = make_nucleus_band(y_rim=-2.45)
        dimer = make_dimer(LIGAND_COL, width=1.45, lobe_h=0.50).move_to([0.0, y_mem + 0.72, 0])
        t2_l = make_type2(-0.85, y_mem, side="left", active=True, scale=0.92, phase_tracker=phase)
        t2_r = make_type2(0.85, y_mem, side="right", active=True, scale=0.92, phase_tracker=phase)
        t1_l = make_type1(-2.22, y_mem, side="left", locked=False, active=True, gs_open=True, phos_gs=2, scale=0.92, phase_tracker=phase)
        t1_r = make_type1(2.22, y_mem, side="right", locked=False, active=True, gs_open=True, phos_gs=2, scale=0.92, phase_tracker=phase)

        t2_lbl = T("Type II", size=28, color=TYPE2_COL, weight=BOLD).move_to([0.0, y_mem - 1.95, 0])
        t1_lbl = T("Type I (active)", size=28, color=TYPE1_COL, weight=BOLD).next_to(t1_r.lobe, RIGHT, buff=0.42)
        tag = scope_tag("schematic")

        self.add(mem, nuc, dimer, t2_l, t2_r, t1_l, t1_r, t2_lbl, t1_lbl, tag)

        self.at("now docks")
        rsmad = make_rsmad(RSMAD_COL, show_domains=True, phos_tail=0, pocket_dir=RIGHT, scale=0.82)
        rsmad.move_to([2.22, -1.45, 0])
        rsmad_lbl = T("R-Smad", size=28, color=RSMAD_COL, weight=BOLD).next_to(rsmad.mh1, RIGHT, buff=0.30)
        self.play(FadeIn(rsmad, shift=UP * 0.2), FadeIn(rsmad_lbl), run_time=1.0)

        dock_pos = np.array([2.22, -1.25, 0])
        self.play(
            rsmad.animate.move_to(dock_pos),
            rsmad_lbl.animate.move_to([4.00, -1.45, 0]),
            run_time=2.4,
        )

        self.at("transcription factor")
        tf_badge = T("Transcription factor", size=26, color=RSMAD_COL, weight=BOLD).next_to(
            rsmad_lbl, DOWN, aligned_edge=LEFT, buff=0.22
        )
        mh1_hi = SurroundingRectangle(rsmad.mh1, color=PHOS_COL, corner_radius=0.18, buff=0.07, stroke_width=3.2)
        self.play(Create(mh1_hi), FadeIn(tf_badge), run_time=1.6)

        # Beat: "adds two phosphates" -> P discs start and land cleanly below Type I lobe edge (zero straddle!)
        self.at("adds two phosphates")
        self.play(FadeOut(mh1_hi), run_time=0.4)
        tail_tip = rsmad.tail.get_end()
        p1 = make_phos(radius=0.21, size=22)
        p2 = make_phos(radius=0.21, size=22)
        src1 = t1_r.lobe.get_bottom() + LEFT * 0.30 + DOWN * 0.26
        src2 = t1_r.lobe.get_bottom() + RIGHT * 0.30 + DOWN * 0.26
        dst1 = tail_tip + LEFT * 0.27 + DOWN * 0.04
        dst2 = tail_tip + RIGHT * 0.27 + DOWN * 0.04
        p1.move_to(src1)
        p2.move_to(src2)
        self.play(FadeIn(p1, scale=0.6), FadeIn(p2, scale=0.6), run_time=0.5)
        self.play(p1.animate.move_to(dst1), p2.animate.move_to(dst2), run_time=1.8)
        rsmad.p_discs.add(p1, p2)
        # Release slightly downward after phosphorylation
        self.play(rsmad.animate.shift(DOWN * 0.10), run_time=1.2)

        self.at("signaled straight")
        relay_box = VGroup(
            T("Type II", size=28, color=TYPE2_COL, weight=BOLD),
            T("→", size=28, color=TEXT, weight=BOLD),
            T("Type I", size=28, color=TYPE1_COL, weight=BOLD),
            T("→", size=28, color=TEXT, weight=BOLD),
            T("R-Smad", size=28, color=RSMAD_COL, weight=BOLD),
        ).arrange(RIGHT, buff=0.16).move_to([-3.3, -0.70, 0])
        dna_arr = Arrow(
            rsmad.mh1.get_bottom() + DOWN * 0.08,
            [1.6, nuc.dna_center[1] + 0.32, 0],
            color=PHOS_COL, stroke_width=4.6, buff=0.08,
        )
        self.play(FadeIn(relay_box), GrowArrow(dna_arr), run_time=2.2)
        self.finish()


class S08Smad4Trimer(SpokenScene):
    """
    Two phosphorylated R-Smads slot tail-to-pocket with one violet Smad4 into a 3-part ring
    that enters the nucleus onto DNA while active Type I turns over a second R-Smad batch.
    """
    def construct(self):
        y_mem = 2.60
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        mem = make_membrane(-6.3, 6.3, y=y_mem)
        nuc = make_nucleus_band(y_rim=-1.30, y_dna=-3.25)
        dimer = make_dimer(LIGAND_COL, width=1.40, lobe_h=0.46).move_to([0.0, y_mem + 0.65, 0])
        t2_l = make_type2(-0.80, y_mem, side="left", active=True, scale=0.78, phase_tracker=phase)
        t2_r = make_type2(0.80, y_mem, side="right", active=True, scale=0.78, phase_tracker=phase)
        t1_l = make_type1(-2.05, y_mem, side="left", locked=False, active=True, gs_open=True, phos_gs=2, scale=0.78, phase_tracker=phase)
        t1_r = make_type1(2.05, y_mem, side="right", locked=False, active=True, gs_open=True, phos_gs=2, scale=0.78, phase_tracker=phase)
        tag = scope_tag("schematic")

        smad_a = make_rsmad(RSMAD_COL, show_domains=True, phos_tail=2, pocket_dir=RIGHT, scale=0.68)
        smad_b = make_rsmad(RSMAD_COL, show_domains=True, phos_tail=2, pocket_dir=LEFT, scale=0.68)
        smad_a.move_to([-2.05, -0.22, 0])
        smad_b.move_to([2.05, -0.22, 0])

        self.add(mem, nuc, dimer, t2_l, t2_r, t1_l, t1_r, smad_a, smad_b, tag)

        self.at("fits a pocket")
        tail_hi = SurroundingRectangle(smad_a.p_discs, color=PHOS_COL, corner_radius=0.08, buff=0.05, stroke_width=3.0)
        fit_lbl = T("P-tail fits pocket", size=22, color=PHOS_COL, weight=BOLD).move_to([-0.04, -0.62, 0])
        pocket_arr = Arrow(fit_lbl.get_right() + RIGHT * 0.08, smad_b.pocket.get_left() + LEFT * 0.08,
                           color=PHOS_COL, stroke_width=3.6, buff=0.02, max_tip_length_to_length_ratio=0.35)
        self.play(Create(tail_hi), FadeIn(fit_lbl), GrowArrow(pocket_arr), run_time=1.4)

        # Beat: "two phosphorylated" -> spawn Smad4 in open center gap and keep R-Smads clear of Type I lobes and nuclear rim
        self.at("two phosphorylated")
        self.play(FadeOut(tail_hi), FadeOut(fit_lbl), FadeOut(pocket_arr), run_time=0.5)
        smad4 = make_smad4(scale=0.84, label="Smad4").move_to([0.0, -0.55, 0])
        s4_lbl = T("1× Smad4", size=28, color=SMAD4_COL, weight=BOLD).next_to(smad4, UP, buff=0.18)
        r2_lbl = T("2× R-Smad", size=28, color=RSMAD_COL, weight=BOLD).move_to([-4.2, -0.45, 0])

        self.play(FadeIn(smad4, shift=UP * 0.2), FadeIn(s4_lbl), FadeIn(r2_lbl), run_time=1.2)

        trimer = make_compact_trimer(RSMAD_COL, smad_label="R-Smad", scale=0.66).move_to([0.0, -0.45, 0])
        self.play(
            FadeOut(s4_lbl), FadeOut(r2_lbl),
            smad_a.animate.move_to([-1.65, -0.22, 0]),
            smad_b.animate.move_to([1.65, -0.22, 0]),
            smad4.animate.move_to([0.0, -0.85, 0]),
            run_time=1.1,
        )
        self.play(FadeOut(smad_a, run_time=0.20), FadeOut(smad_b, run_time=0.20), FadeOut(smad4, run_time=0.20))
        self.play(FadeIn(trimer, run_time=0.40))

        tri_lbl = T("2 R-Smad + 1 Smad4", size=28, color=TEXT, weight=BOLD).next_to(trimer, LEFT, buff=0.36)
        self.play(FadeIn(tri_lbl), run_time=0.9)

        # Beat: "three" -> dock trimer left-of-center inside nucleus above DNA
        self.at("three")
        self.play(FadeOut(tri_lbl), run_time=0.4)
        dna_dock = np.array([-0.75, -2.35, 0])
        self.play(trimer.animate.move_to(dna_dock), run_time=2.5)
        bind_l = Line(trimer.s4.get_bottom() + LEFT * 0.25, [-1.00, nuc.dna_center[1] + 0.08, 0], color=NUC_COL, stroke_width=3.2)
        bind_r = Line(trimer.s4.get_bottom() + RIGHT * 0.25, [-0.50, nuc.dna_center[1] + 0.08, 0], color=NUC_COL, stroke_width=3.2)
        self.play(Create(bind_l), Create(bind_r), run_time=0.8)

        # Beat: "keeps phosphorylating" -> second R-Smad docks centered directly beneath t1_r at x=2.05
        self.at("keeps phosphorylating")
        turn_lbl = T("Catalytic turnover", size=28, color=TYPE1_COL, weight=BOLD).move_to([-4.0, 0.05, 0])
        new_smad = make_rsmad(RSMAD_COL, show_domains=True, phos_tail=0, pocket_dir=RIGHT, scale=0.82)
        new_smad.move_to([4.5, -0.35, 0])
        self.play(FadeIn(turn_lbl), FadeIn(new_smad), run_time=0.8)
        self.play(new_smad.animate.move_to([2.05, -0.35, 0]), run_time=1.3)

        tp1 = make_phos(radius=0.21, size=22).move_to(t1_r.lobe.get_bottom() + LEFT * 0.27 + DOWN * 0.24)
        tp2 = make_phos(radius=0.21, size=22).move_to(t1_r.lobe.get_bottom() + RIGHT * 0.27 + DOWN * 0.24)
        t_tip = new_smad.tail.get_end()
        self.play(FadeIn(tp1), FadeIn(tp2), run_time=0.35)
        self.play(
            tp1.animate.move_to(t_tip + LEFT * 0.27 + UP * 0.02),
            tp2.animate.move_to(t_tip + RIGHT * 0.27 + UP * 0.02),
            run_time=1.1,
        )
        new_smad.p_discs.add(tp1, tp2)
        self.play(new_smad.animate.move_to([3.3, -0.35, 0]), run_time=1.2)
        self.finish()


class S09TwoBranches(SpokenScene):
    """
    Two parallel membrane bays: TGF-beta/activin -> emerald Smad2/3 vs. BMP tightly
    gripping Type I -> coral Smad1/5/8; yellow P flows one way in both toward shared violet Smad4.
    """
    def construct(self):
        y_mem = 1.65
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        mem = make_membrane(-6.3, 6.3, y=y_mem)
        divider = DashedLine([0.0, -1.25, 0], [0.0, 3.45, 0], color=GREY, stroke_width=2.5, dash_length=0.18)
        nuc = make_nucleus_band(y_rim=-2.35)
        tag = scope_tag("schematic")

        lx = -3.25
        h_left = T("TGF-β / Activin", size=30, color=LIGAND_COL, weight=BOLD).move_to([lx, HEAD_Y, 0])
        l_t2 = make_type2(lx - 1.10, y_mem, side="left", active=True, scale=0.86, phase_tracker=phase)
        l_t1 = make_type1(lx + 1.10, y_mem, side="right", locked=False, active=True, gs_open=True, phos_gs=2, scale=0.86, phase_tracker=phase)
        l_dimer = make_dimer(LIGAND_COL, width=1.40, lobe_h=0.48).move_to([lx, y_mem + 1.08, 0])
        l_t2_lbl = T("Type II", size=24, color=TYPE2_COL, weight=BOLD).next_to(l_t2.lobe, LEFT, buff=0.14)
        l_t1_lbl = T("Type I", size=24, color=TYPE1_COL, weight=BOLD).next_to(l_t1.lobe, RIGHT, buff=0.40)

        rx = 3.25
        h_right = T("BMP", size=30, color=BMP_COL, weight=BOLD).move_to([rx, HEAD_Y, 0])
        r_t1 = make_type1(rx - 1.10, y_mem, side="left", locked=False, active=True, gs_open=True, phos_gs=2, scale=0.86, phase_tracker=phase)
        r_t2 = make_type2(rx + 1.10, y_mem, side="right", active=True, scale=0.86, phase_tracker=phase)
        r_dimer = make_dimer(BMP_COL, width=1.40, lobe_h=0.48).move_to([rx, y_mem + 1.08, 0])
        r_t1_lbl = T("Type I", size=24, color=TYPE1_COL, weight=BOLD).next_to(r_t1.lobe, LEFT, buff=0.40)
        r_t2_lbl = T("Type II", size=24, color=TYPE2_COL, weight=BOLD).next_to(r_t2.lobe, RIGHT, buff=0.14)

        smad4_hub = make_smad4(scale=0.96, label="Smad4").move_to([0.0, -1.75, 0])

        self.add(
            mem, divider, nuc, tag, h_left, h_right,
            l_t2, l_t1, l_t2_lbl, l_t1_lbl,
            r_t1, r_t2, r_t1_lbl, r_t2_lbl,
            smad4_hub,
        )
        # Receptors slide into bay pairs during opening statement
        self.play(
            l_t2.animate.shift(RIGHT * 0.20), l_t1.animate.shift(LEFT * 0.20),
            l_t2_lbl.animate.shift(RIGHT * 0.20), l_t1_lbl.animate.shift(LEFT * 0.20),
            r_t1.animate.shift(RIGHT * 0.20), r_t2.animate.shift(LEFT * 0.20),
            r_t1_lbl.animate.shift(RIGHT * 0.20), r_t2_lbl.animate.shift(LEFT * 0.20),
            run_time=3.5,
        )

        self.at("TGF beta")
        smad23 = boxed_label("Smad2 / Smad3", RSMAD_COL, size=26, pad=0.22).move_to([lx, -1.25, 0])
        p_left = make_phos(radius=0.21, size=22).move_to(l_t2.lobe.get_bottom() + DOWN * 0.22)
        self.play(FadeIn(l_dimer), FadeIn(smad23), run_time=0.8)
        self.play(l_dimer.animate.move_to([lx, y_mem + 0.68, 0]), smad23.animate.shift(UP * 0.14), run_time=1.2)
        self.play(FadeIn(p_left), run_time=0.3)
        self.play(p_left.animate.move_to(l_t1.lobe.get_bottom() + DOWN * 0.22), run_time=1.0)
        self.play(p_left.animate.move_to(smad23.get_top() + UP * 0.28), run_time=1.0)

        self.at("Bone morphogenetic")
        smad158 = boxed_label("Smad1 / 5 / 8", BMP_COL, size=26, pad=0.22).move_to([rx, -1.25, 0])
        self.play(FadeIn(r_dimer), FadeIn(smad158), run_time=0.8)
        self.play(r_dimer.animate.move_to([rx, y_mem + 0.68, 0]), run_time=0.8)

        # Beat: "BMP receptors" (at 13.90s -> runs right on cue!)
        self.at("BMP receptors")
        p_right_a = make_phos(radius=0.21, size=22).move_to(r_t2.lobe.get_bottom() + DOWN * 0.22)
        self.play(FadeIn(p_right_a), smad158.animate.shift(UP * 0.14), run_time=0.8)
        self.play(p_right_a.animate.move_to(r_t1.lobe.get_bottom() + DOWN * 0.22), run_time=1.4)
        self.play(p_right_a.animate.move_to(smad158.get_top() + UP * 0.28), run_time=1.4)

        self.at("grip type")
        tight_ring = SurroundingRectangle(VGroup(r_dimer, r_t1.outer), color=BMP_COL, corner_radius=0.14, buff=0.06, stroke_width=3.4)
        self.play(
            r_dimer.animate.shift(LEFT * 0.22 + DOWN * 0.06),
            r_t1.outer.animate.set_stroke(BMP_COL, width=4.4),
            Create(tight_ring),
            run_time=1.6,
        )

        self.at("phosphate still flows")
        p_right_b = make_phos(radius=0.21, size=22).move_to(r_t2.lobe.get_bottom() + DOWN * 0.22)
        arr_l = Arrow(smad23.get_bottom(), smad4_hub.get_left() + UP * 0.12, color=RSMAD_COL, stroke_width=4.2, buff=0.12)
        arr_r = Arrow(smad158.get_bottom(), smad4_hub.get_right() + UP * 0.12, color=BMP_COL, stroke_width=4.2, buff=0.12)
        self.play(FadeIn(p_right_b), run_time=0.25)
        self.play(p_right_b.animate.move_to(r_t1.lobe.get_bottom() + DOWN * 0.22), run_time=0.8)
        self.play(p_right_b.animate.move_to(smad158.get_top() + UP * 0.28 + RIGHT * 0.50), run_time=0.8)
        self.play(GrowArrow(arr_l), GrowArrow(arr_r), FadeOut(tight_ring), run_time=1.2)
        self.finish()


class S10ReturnRule(SpokenScene):
    """
    Pull back to unified single membrane: TGF-beta is not an enzyme; it bridges Type II and
    locked Type I, sending phosphate one way to a Smad -> Smad4 trimer to DNA -> two '?' cell contexts.
    """
    def construct(self):
        y_mem = 2.30
        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: phase.increment_value(3.4 * dt))
        self.add(phase)

        mem = make_membrane(-6.3, 6.3, y=y_mem)
        nuc = make_nucleus_band(y_rim=-1.35, y_dna=-3.25)
        t2_l = make_type2(-1.15, y_mem, side="left", active=True, scale=0.84, phase_tracker=phase)
        t2_r = make_type2(1.15, y_mem, side="right", active=True, scale=0.84, phase_tracker=phase)
        t1_l = make_type1(-3.65, y_mem, side="left", locked=True, active=False, scale=0.84)
        t1_r = make_type1(3.65, y_mem, side="right", locked=True, active=False, scale=0.84)
        tag = scope_tag("schematic")

        self.add(mem, nuc, t2_l, t2_r, t1_l, t1_r, tag)
        self.play(
            t1_l.animate.shift(RIGHT * 0.35),
            t1_r.animate.shift(LEFT * 0.35),
            run_time=3.5,
        )

        self.at("not an enzyme")
        dimer = make_dimer(LIGAND_COL, width=1.50, lobe_h=0.50).move_to([0.0, y_mem + 0.64, 0])
        not_enz = T("TGF-β: bridge, not enzyme", size=28, color=LIGAND_COL, weight=BOLD).move_to([0.0, 3.50, 0])
        self.play(FadeIn(dimer, shift=DOWN * 0.15), FadeIn(not_enz), run_time=1.4)

        self.at("It bridges")
        self.play(
            dimer.animate.move_to([0.0, y_mem + 0.56, 0]),
            t2_l.animate.shift(RIGHT * 0.35),
            t2_r.animate.shift(LEFT * 0.35),
            t1_l.animate.shift(RIGHT * 1.35),
            t1_r.animate.shift(LEFT * 1.35),
            run_time=1.6,
        )
        act1_l = make_active_arc(
            lambda l=t1_l.lobe, o=t1_l.arc_offset: l.get_center() + o,
            radius=0.26, color=PHOS_COL, phase_tracker=phase, offset=0.8,
        )
        act1_r = make_active_arc(
            lambda l=t1_r.lobe, o=t1_r.arc_offset: l.get_center() + o,
            radius=0.26, color=PHOS_COL, phase_tracker=phase, offset=3.9,
        )
        self.play(
            t1_l.fkbp.animate.shift(LEFT * 0.9 + DOWN * 0.3).set_opacity(0),
            t1_r.fkbp.animate.shift(RIGHT * 0.9 + DOWN * 0.3).set_opacity(0),
            t1_l.gs_flap.animate.set_stroke(PHOS_COL).set_fill(PHOS_COL, opacity=0.45),
            t1_r.gs_flap.animate.set_stroke(PHOS_COL).set_fill(PHOS_COL, opacity=0.45),
            run_time=0.5,
        )
        self.play(
            Rotate(t1_l.gs_flap, angle=-1.92, about_point=t1_l.gs_flap.get_left()),
            Rotate(t1_r.gs_flap, angle=1.92, about_point=t1_r.gs_flap.get_right()),
            t1_l.lobe.animate.set_fill(TYPE1_COL, opacity=0.34),
            t1_r.lobe.animate.set_fill(TYPE1_COL, opacity=0.34),
            FadeOut(t1_l.site), FadeOut(t1_r.site),
            FadeIn(act1_l), FadeIn(act1_r),
            run_time=0.7,
        )

        # Beat: "sending phosphate" -> P pulse routes cleanly below Type I lobe onto R-Smad tail
        self.at("sending phosphate")
        rsmad = make_rsmad(RSMAD_COL, show_domains=True, phos_tail=0, pocket_dir=RIGHT, scale=0.72).move_to([2.35, -0.45, 0])
        smad4 = make_smad4(scale=0.88, label="Smad4").move_to([-2.0, -0.45, 0])
        p_pulse = make_phos(radius=0.21, size=22).move_to(t2_r.lobe.get_bottom() + DOWN * 0.22)
        self.play(FadeIn(rsmad), FadeIn(smad4), FadeIn(p_pulse), run_time=0.5)
        self.play(p_pulse.animate.move_to(t1_r.lobe.get_bottom() + DOWN * 0.22), run_time=0.7)
        self.play(p_pulse.animate.move_to(rsmad.tail.get_end() + LEFT * 0.27 - UP * 0.03), run_time=0.7)
        rsmad.p_discs.add(p_pulse)

        # Beat: "Next see" -> non-overlapping slide at y=-0.45, swap to compact trimer, dock inside nucleus above DNA
        self.at("Next see")
        trimer = make_compact_trimer(RSMAD_COL, smad_label="R-Smad", scale=0.66).move_to([0.0, -0.45, 0])
        self.play(
            rsmad.animate.move_to([1.65, -0.35, 0]),
            smad4.animate.move_to([-1.65, -0.45, 0]),
            run_time=0.8,
        )
        self.play(FadeOut(rsmad, run_time=0.2), FadeOut(p_pulse, run_time=0.2), FadeOut(smad4, run_time=0.2))
        self.remove(p_pulse)
        self.play(FadeIn(trimer, run_time=0.4))
        self.play(trimer.animate.move_to([0.0, nuc.dna_center[1] + 0.90, 0]), run_time=1.3)

        arr_out_l = Arrow([-2.05, nuc.dna_center[1] + 0.55, 0], [-4.2, -1.15, 0], color=RSMAD_COL, stroke_width=4.4, buff=0.05)
        arr_out_r = Arrow([2.05, nuc.dna_center[1] + 0.55, 0], [4.2, -1.15, 0], color=LIGAND_COL, stroke_width=4.4, buff=0.05)
        q_l = T("?", size=40, color=RSMAD_COL, weight=BOLD).next_to(arr_out_l.get_end(), UP, buff=0.14)
        q_r = T("?", size=40, color=LIGAND_COL, weight=BOLD).next_to(arr_out_r.get_end(), UP, buff=0.14)
        self.play(GrowArrow(arr_out_l), GrowArrow(arr_out_r), FadeIn(q_l), FadeIn(q_r), run_time=1.0)
        self.finish()


class S11End(EndCard):
    LINE = "TGF-β bridges two kinases, passing phosphate one way to a Smad."
