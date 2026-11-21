"""
Receptor Tails, Specificity, and Brakes (Cytokine Receptors and JAK-STAT, Chapter 2)

COLOUR MAP (one colour per concept, carried across all scenes):
  - Plasma membrane / structure : #64748B (slate grey)
  - Cytokine / EPO / V617F mark : #F59E0B (amber)
  - EPO receptor pair           : #3B82F6 (slate blue)
  - Immune receptor pair        : #06B6D4 (indigo-cyan)
  - JAK kinases (JAK1/2/TYK2)   : #EF4444 (coral-red; JAK1 #F87171, JAK2 #EF4444, TYK2 #DC2626)
  - JAK3 (immune receptor)      : #F97316 (crimson-coral)
  - Pseudokinase lobe           : #FB7185 (rose)
  - STAT proteins               : #10B981 (emerald-teal; second matched STAT #34D399)
  - Phosphotyrosine 'P' tags    : #FACC15 (gold)
  - Nuclear DNA helix           : #A78BFA (violet)
  - Tyrosine phosphatases       : #38BDF8 (cool cyan-silver)
  - SOCS feedback shields       : #C084FC (violet-plum)

ONE WORLD CARRIED SCENE TO SCENE:
  A cell cross-section with the plasma membrane across the top (y = 1.85), intracellular
  receptor tails extending into the cytoplasm, and the dashed nuclear envelope enclosing a
  schematic violet DNA double helix at the bottom (y = -2.65). Zoomed scenes (s02, s09) focus
  tightly on the membrane-tail region while keeping the same receptor geometry and colours.

PER-SCENE CHANGES (what moves/transforms on screen and what drives it):
  - s01_link_question     : STAT travels receptor -> JAK -> DNA along relay; 4 JAKs, 7 STATs, and a fan
                            of cytokines expand; glowing brackets mark Receptor tails and Brakes.
  - s02_tail_sorting      : Zoomed tails reveal distinct JAK brackets and notched phosphotyrosine sites;
                            two differently notched STATs drift up and lock only into matching tail notches.
  - s03_two_receptors     : Amber cytokines bind EPO (JAK2) and Immune (JAK3) receptors side by side,
                            activating their JAKs and sending matched STAT pairs down to red vs immune cells.
  - s04_predict_loss      : Four similar JAKs are compared; JAK2 fades out from EPO receptor leaving empty
                            dashed 'No JAK2' sockets; EPO binds and pairs the bare receptor chains.
  - s05_predict_pause     : Held bound EPO receptor with empty 'No JAK2' sockets; intact JAK1/3/TYK2 drift
                            gently nearby without docking while the 4.5 s countdown ring empties.
  - s06_reveal_specificity: Question clears; JAK1/3/TYK2 drift in and bounce away from bare tails; adult
                            red-cell slot empties to 'No lasting (adult-type) red cells' + STAT5 hedge badge.
  - s07_phosphatases      : Active STAT dimer clamps onto DNA; cyan-silver phosphatase crescents sweep
                            across JAK2, tails, and dimer, stripping 'P' tags so STATs return to cytoplasm.
  - s08_socs_feedback     : Active STAT dimer travels to DNA to switch on SOCS gene; after a running clock
                            delay, SOCS shields rise, block one JAK kinase lobe, and tag another for breakdown.
  - s09_stuck_on          : Zoomed two-lobed JAK2s with no EPO outside; V617F amber dot loosens rose
                            pseudokinase restraint, lobes pull together, 'P' tags fire, STATs stream down.
  - s10_rule_close        : Split cell summary transforms missing-JAK2 vs V617F contrast into balanced
                            left 'Tail sorting' and right 'Brakes' (pseudokinase, phosphatases, SOCS).
"""
from bp_parts import *

# Concept palette
MEMBRANE_COL = "#64748B"
CYTOKINE_COL = "#F59E0B"
EPO_REC_COL = "#3B82F6"
IMM_REC_COL = "#06B6D4"
JAK_COL = "#EF4444"
JAK1_COL = "#F87171"
JAK2_COL = "#EF4444"
JAK3_COL = "#F97316"
TYK2_COL = "#DC2626"
PSEUDO_COL = "#FB7185"
STAT_COL = "#10B981"
STAT2_COL = "#34D399"
PHOS_COL = "#FACC15"
DNA_COL = "#A78BFA"
PHOSPHATASE_COL = "#38BDF8"
SOCS_COL = "#C084FC"


# ------------------------------------------------------------------ shared builders
def build_membrane(y=1.85, x_span=6.35):
    """Plasma membrane bilayer bar across the frame."""
    top = Line([-x_span, y + 0.21, 0], [x_span, y + 0.21, 0], color=MEMBRANE_COL, stroke_width=5.0)
    bot = Line([-x_span, y - 0.21, 0], [x_span, y - 0.21, 0], color=MEMBRANE_COL, stroke_width=5.0)
    band = Rectangle(width=2 * x_span, height=0.42, stroke_width=0, fill_color=MEMBRANE_COL, fill_opacity=0.34).move_to([0, y, 0])
    ticks = VGroup(*[
        Line([x, y - 0.17, 0], [x, y + 0.17, 0], color=MEMBRANE_COL, stroke_width=2.2, stroke_opacity=0.65)
        for x in np.linspace(-x_span + 0.15, x_span - 0.15, 38)
    ])
    g = VGroup(band, ticks, top, bot)
    g.layout_ok = True
    return g


def build_dna_helix(y=-2.65, width=7.6, amp=0.22):
    """Schematic DNA double helix (sinusoidal strands + rungs)."""
    xs = np.linspace(-width / 2, width / 2, 120)
    s1 = VMobject(color=DNA_COL, stroke_width=5.0).set_points_as_corners([[x, y + amp * np.sin(2.5 * x), 0] for x in xs])
    s2 = VMobject(color=DNA_COL, stroke_width=5.0, stroke_opacity=0.85).set_points_as_corners([[x, y - amp * np.sin(2.5 * x), 0] for x in xs])
    rungs = VGroup(*[
        Line([x, y + amp * np.sin(2.5 * x), 0], [x, y - amp * np.sin(2.5 * x), 0], color=DNA_COL, stroke_width=2.8, stroke_opacity=0.72)
        for x in np.linspace(-width / 2 + 0.2, width / 2 - 0.2, 24)
    ])
    g = VGroup(rungs, s1, s2)
    g.layout_ok = True
    return g


def build_cell_world(membrane_y=1.85, dna_y=-2.65, show_labels=True, nuc_offset=0.72):
    """Standard cell cross-section: plasma membrane, nuclear envelope, schematic DNA."""
    mem = build_membrane(y=membrane_y)
    nuc_y = dna_y + nuc_offset
    nuc_line = DashedLine([-6.3, nuc_y, 0], [6.3, nuc_y, 0], color=DNA_COL, stroke_width=3.0, stroke_opacity=0.68, dash_length=0.22)
    nuc_line.layout_ok = True
    dna = build_dna_helix(y=dna_y, width=7.4)
    g = VGroup(mem, nuc_line, dna)
    if show_labels:
        mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, membrane_y + 0.50, 0])
        nuc_lab = T("Nucleus", 26, DNA_COL).move_to([-5.45, nuc_y - 0.36, 0])
        dna_lab = T("DNA", 28, DNA_COL, weight=BOLD).next_to(dna, LEFT, buff=0.25)
        g.add(mem_lab, nuc_lab, dna_lab)
    return g


def build_receptor_pair(cx, color, membrane_y=1.85, spread=0.46, tail_len=1.85, bracket_style="square", notch_style=None):
    """Two-chain cytokine receptor pair embedded in the membrane with intracellular tails."""
    chains = VGroup()
    tail_ends = []
    bracket_pts = []
    notch_pts = []
    for side in (-1, 1):
        x = cx + side * spread
        ext = Line([x, membrane_y + 0.21, 0], [x, membrane_y + 0.48, 0], color=color, stroke_width=8)
        cup = Line([x, membrane_y + 0.48, 0], [x - side * 0.18, membrane_y + 0.66, 0], color=color, stroke_width=8)
        tm = Line([x, membrane_y - 0.21, 0], [x, membrane_y + 0.21, 0], color=color, stroke_width=13)
        tail = Line([x, membrane_y - 0.21, 0], [x, membrane_y - 0.21 - tail_len, 0], color=color, stroke_width=8)

        by = membrane_y - 0.66
        if bracket_style == "square":
            brk = VMobject(color=color, stroke_width=5.5).set_points_as_corners([
                [x, by + 0.18, 0], [x + side * 0.18, by + 0.18, 0],
                [x + side * 0.18, by - 0.18, 0], [x, by - 0.18, 0],
            ])
        else:
            brk = VMobject(color=color, stroke_width=5.5).set_points_as_corners([
                [x, by + 0.20, 0], [x + side * 0.22, by, 0], [x, by - 0.20, 0],
            ])
        bracket_pts.append(np.array([x + side * 0.22, by, 0]))

        parts = VGroup(ext, cup, tm, tail, brk)
        if notch_style is not None:
            ny = membrane_y - 0.21 - tail_len + 0.48
            if notch_style == "tri":
                nt = VMobject(color=color, stroke_width=5.5).set_points_as_corners([
                    [x, ny + 0.20, 0], [x + side * 0.24, ny, 0], [x, ny - 0.20, 0],
                ])
            else:
                nt = VMobject(color=color, stroke_width=5.5).set_points_as_corners([
                    [x, ny + 0.18, 0], [x + side * 0.22, ny + 0.18, 0],
                    [x + side * 0.22, ny - 0.18, 0], [x, ny - 0.18, 0],
                ])
            parts.add(nt)
            notch_pts.append(np.array([x + side * 0.26, ny, 0]))
        chains.add(parts)
        tail_ends.append(np.array([x, membrane_y - 0.21 - tail_len, 0]))

    chains.layout_ok = True
    chains.bracket_pts = bracket_pts
    chains.notch_pts = notch_pts
    chains.tail_ends = tail_ends
    chains.cup_center = np.array([cx, membrane_y + 0.74, 0])
    return chains


def build_p_tag(pos=ORIGIN):
    """High-contrast gold phosphotyrosine 'P' badge."""
    circ = Circle(radius=0.28, stroke_color=PHOS_COL, stroke_width=3.6, fill_color=BG, fill_opacity=1.0)
    txt = T("P", 24, PHOS_COL, weight=BOLD).move_to(circ)
    return VGroup(circ, txt).move_to(pos)


def build_cytokine(label="", color=CYTOKINE_COL, width=None, height=0.66):
    """Amber cytokine oval sized generously for any label."""
    if label:
        txt = T(label, 24, color, weight=BOLD)
        w = width if width is not None else max(1.32, txt.width + 0.88)
        bg = Ellipse(width=w, height=height, stroke_width=0, fill_color=BG, fill_opacity=1.0)
        oval = Ellipse(width=w, height=height, stroke_color=color, stroke_width=3.8, fill_color=color, fill_opacity=0.34)
        return VGroup(bg, oval, txt.move_to(oval))
    w = width if width is not None else 0.98
    bg = Ellipse(width=w, height=height, stroke_width=0, fill_color=BG, fill_opacity=1.0)
    oval = Ellipse(width=w, height=height, stroke_color=color, stroke_width=3.8, fill_color=color, fill_opacity=0.34)
    return VGroup(bg, oval)


def build_stat_block(label="STAT", color=STAT_COL, notch_style=None, side=1):
    """Compact STAT block with optional matching SH2 notch tip."""
    box = boxed_label(label, color=color, size=26, box=(1.40, 0.58), fill_opacity=0.34)
    if notch_style == "tri":
        tip = Polygon([0, 0.16, 0], [-side * 0.20, 0, 0], [0, -0.16, 0],
                      color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.45)
        tip.next_to(box, LEFT if side == 1 else RIGHT, buff=0.0)
        tip.layout_ok = True
        return VGroup(box, tip)
    elif notch_style == "square":
        tip = Rectangle(width=0.18, height=0.30, color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.45)
        tip.next_to(box, LEFT if side == 1 else RIGHT, buff=0.0)
        tip.layout_ok = True
        return VGroup(box, tip)
    return box


def build_stat_dimer(label="STAT", color=STAT_COL, with_p=True):
    """Paired STAT dimer with gold 'P' badges clearly outside each unit."""
    s_l = boxed_label(label, color=color, size=24, box=(1.22, 0.56), fill_opacity=0.34).shift(LEFT * 0.66)
    s_r = boxed_label(label, color=color, size=24, box=(1.22, 0.56), fill_opacity=0.34).shift(RIGHT * 0.66)
    g = VGroup(s_l, s_r)
    if with_p:
        p_l = build_p_tag(s_l.get_left() + LEFT * 0.38)
        p_r = build_p_tag(s_r.get_right() + RIGHT * 0.38)
        g.add(p_l, p_r)
        g.p_tags = VGroup(p_l, p_r)
    g.left_stat, g.right_stat = s_l, s_r
    return g


def build_phosphatase(pos=ORIGIN):
    """Cool cyan-silver crescent labelled 'Phosphatase' (label clear to the right)."""
    cres = AnnularSector(inner_radius=0.26, outer_radius=0.45, angle=PI * 1.15, start_angle=PI * 0.42,
                         color=PHOSPHATASE_COL, fill_opacity=0.92, stroke_width=3.0)
    cres.layout_ok = True
    lab = T("Phosphatase", 26, PHOSPHATASE_COL, weight=BOLD).next_to(cres, RIGHT, buff=0.18)
    return VGroup(cres, lab).move_to(pos)


def build_socs_shield(label="SOCS"):
    """Violet-plum SOCS feedback shield sized cleanly around label."""
    pts = [[-0.78, 0.36, 0], [0.78, 0.36, 0], [0.78, -0.06, 0], [0, -0.42, 0], [-0.78, -0.06, 0]]
    poly = Polygon(*pts, color=SOCS_COL, stroke_width=3.6, fill_color=SOCS_COL, fill_opacity=0.34)
    txt = T(label, 24, SOCS_COL, weight=BOLD).move_to(poly.get_center() + UP * 0.05)
    return VGroup(poly, txt)


def build_red_cells(count=3, color=JAK2_COL):
    """Schematic red blood cell cluster (simple discs, no molecular structure)."""
    cells = VGroup()
    for _ in range(count):
        outer = Circle(radius=0.25, color=color, stroke_width=3.8, fill_color=color, fill_opacity=0.42)
        inner = Circle(radius=0.10, color=color, stroke_width=2.4, fill_color=BG, fill_opacity=0.85)
        cells.add(VGroup(outer, inner))
    cells.arrange(RIGHT, buff=0.14)
    cells.layout_ok = True
    return cells


def build_immune_cells(count=3, color=IMM_REC_COL):
    """Schematic immune cell cluster."""
    cells = VGroup(*[
        Circle(radius=0.24, color=color, stroke_width=3.8, fill_color=color, fill_opacity=0.38)
        for _ in range(count)
    ]).arrange(RIGHT, buff=0.14)
    cells.layout_ok = True
    return cells


def build_epo_predict_stage():
    """Carried stage for s04_predict_loss and s05_predict_pause (bound EPO receptor, No JAK2, intact JAK1/3/TYK2)."""
    world = build_cell_world(membrane_y=1.85, dna_y=-2.35, show_labels=False)
    mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, 2.35, 0])
    dna_lab = T("DNA", 28, DNA_COL, weight=BOLD).move_to([-4.65, -2.35, 0])
    world.add(mem_lab, dna_lab)

    rec = build_receptor_pair(-2.1, EPO_REC_COL, membrane_y=1.85, spread=0.38, tail_len=1.85, bracket_style="square")
    rec_lab = T("EPO receptor", 28, EPO_REC_COL, weight=BOLD).move_to([-2.1, 3.50, 0])
    epo = build_cytokine("EPO").move_to(rec.cup_center + UP * 0.28)

    sock_l = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.24, height=0.56, stroke_color=JAK2_COL, stroke_width=3.2), num_dashes=12)
    sock_r = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.24, height=0.56, stroke_color=JAK2_COL, stroke_width=3.2), num_dashes=12)
    sock_l.next_to(rec.bracket_pts[0], LEFT, buff=0.06)
    sock_r.next_to(rec.bracket_pts[1], RIGHT, buff=0.06)
    sock_l.layout_ok = True
    sock_r.layout_ok = True
    no_jak = T("No JAK2", 28, JAK2_COL, weight=BOLD).move_to([-2.1, -0.45, 0])

    j1 = boxed_label("JAK1", JAK1_COL, 26, box=(1.36, 0.60), fill_opacity=0.34).move_to([2.0, 1.25, 0])
    j3 = boxed_label("JAK3", JAK3_COL, 26, box=(1.36, 0.60), fill_opacity=0.34).move_to([4.1, 0.70, 0])
    tyk = boxed_label("TYK2", TYK2_COL, 26, box=(1.36, 0.60), fill_opacity=0.34).move_to([2.2, 0.10, 0])
    other_lab = T("Intact other JAKs", 28, TEXT, weight=BOLD).move_to([3.05, 2.55, 0])

    return VGroup(world, rec, rec_lab, epo, sock_l, sock_r, no_jak, other_lab), VGroup(j1, j3, tyk)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Cytokine Receptors and JAK-STAT"
    TITLE = "Receptor Tails, Specificity, and Brakes"


class S01LinkQuestion(SpokenScene):
    def construct(self):
        world = build_cell_world(membrane_y=1.85, dna_y=-2.65)
        rec = build_receptor_pair(-3.4, EPO_REC_COL, membrane_y=1.85, spread=0.44, tail_len=1.60)
        cyto = build_cytokine("Cytokine", height=0.66).move_to(rec.cup_center + UP * 0.32)
        jak = boxed_label("JAK", JAK_COL, 26, box=(1.12, 0.56), fill_opacity=0.34).next_to(rec.bracket_pts[1], RIGHT, buff=0.06)
        stat = build_stat_block("STAT", STAT_COL).move_to([-2.05, -0.35, 0])
        relay_arrow = Arrow([-3.4, -0.82, 0], [-3.4, -2.35, 0], color=STAT_COL, stroke_width=5.5, buff=0.05)

        self.add(world, scope_tag("schematic"))
        self.play(FadeIn(rec), FadeIn(cyto), FadeIn(jak), run_time=1.0)
        self.play(FadeIn(stat), run_time=0.8)
        self.play(stat.animate.move_to([-3.4, -0.46, 0]), run_time=2.2)
        self.play(GrowArrow(relay_arrow), run_time=2.0)

        self.at("four jacks")
        jaks_row = VGroup(
            boxed_label("JAK1", JAK1_COL, 26, box=(1.28, 0.58), fill_opacity=0.34),
            boxed_label("JAK2", JAK2_COL, 26, box=(1.28, 0.58), fill_opacity=0.34),
            boxed_label("JAK3", JAK3_COL, 26, box=(1.28, 0.58), fill_opacity=0.34),
            boxed_label("TYK2", TYK2_COL, 26, box=(1.28, 0.58), fill_opacity=0.34),
        ).arrange(RIGHT, buff=0.22).move_to([3.05, 1.00, 0])
        self.play(LaggedStart(*[FadeIn(j, shift=UP * 0.15) for j in jaks_row], lag_ratio=0.10), run_time=0.7)

        self.at("seven stats")
        stats_row = VGroup(
            *[boxed_label(s, STAT_COL, 24, box=(1.28, 0.56), fill_opacity=0.32)
              for s in ("STAT1", "STAT2", "STAT3", "STAT4", "STAT5A", "STAT5B", "STAT6")]
        ).arrange_in_grid(rows=2, cols=4, buff=0.18).move_to([3.05, -0.55, 0])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.12) for s in stats_row], lag_ratio=0.08), run_time=0.8)

        self.at("dozens of cytokines")
        fan = VGroup(*[
            build_cytokine("", width=0.66, height=0.40).move_to([3.05 + dx, 2.75 + dy, 0])
            for dx, dy in [(-2.1, 0.12), (-1.4, -0.08), (-0.7, 0.16), (0.0, -0.05), (0.7, 0.16), (1.4, -0.08), (2.1, 0.12)]
        ])
        fan.layout_ok = True
        fan_lab = T("Dozens of cytokines", 28, CYTOKINE_COL, weight=BOLD).move_to([3.05, 3.32, 0])
        self.play(FadeIn(fan, shift=DOWN * 0.25), FadeIn(fan_lab), run_time=0.9)

        self.at("keep their signals apart")
        sep_line = DashedLine([-0.2, 1.60, 0], [-0.2, -1.75, 0], color=GOLD, stroke_width=3.8)
        sep_line.layout_ok = True
        self.play(Create(sep_line), fan.animate.shift(DOWN * 0.18), run_time=0.9)

        self.at("and shut off")
        self.play(relay_arrow.animate.set_opacity(0.30), stat.animate.set_opacity(0.35), fan.animate.shift(UP * 0.18), run_time=1.8)
        self.play(stat[0].animate.set_fill(opacity=0.34).set_stroke(opacity=1.0), stat[1].animate.set_opacity(1.0), relay_arrow.animate.set_opacity(1.0), run_time=1.5)

        self.at("the receptor tails")
        tails_box = RoundedRectangle(width=2.65, height=1.68, corner_radius=0.16, color=EPO_REC_COL, stroke_width=3.8).move_to([-2.725, 0.76, 0])
        tails_box.layout_ok = True
        tails_tag = boxed_label("1. Receptor tails", EPO_REC_COL, 26, fill_opacity=0.34).move_to([-5.05, -1.35, 0])
        self.play(Create(tails_box), FadeIn(tails_tag), run_time=0.7)

        self.at("and the cells")
        brakes_tag = boxed_label("2. Brakes", SOCS_COL, 26, fill_opacity=0.34).move_to([-1.75, -1.35, 0])
        self.play(FadeIn(brakes_tag, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S02TailSorting(SpokenScene):
    def construct(self):
        mem = build_membrane(y=2.20)
        mem_lab = T("Membrane", 26, TEXT).move_to([0.0, 2.68, 0])
        rec_l = build_receptor_pair(-4.5, EPO_REC_COL, membrane_y=2.20, spread=0.42, tail_len=2.85, bracket_style="square", notch_style="tri")
        rec_r = build_receptor_pair(4.5, IMM_REC_COL, membrane_y=2.20, spread=0.42, tail_len=2.85, bracket_style="angle", notch_style="square")

        self.add(mem, mem_lab, scope_tag("schematic"))
        self.play(Create(rec_l), Create(rec_r), run_time=1.2)

        self.at("receptor tails")
        head = T("Tail selects JAK and STAT", 30, GOLD, weight=BOLD).move_to([0, 3.28, 0])
        self.play(FadeIn(head), run_time=0.9)
        stat_l = build_stat_block("STAT A", STAT_COL, notch_style="tri", side=1).move_to([-2.4, -3.05, 0])
        stat_r = build_stat_block("STAT B", STAT2_COL, notch_style="square", side=-1).move_to([2.4, -3.05, 0])
        self.play(FadeIn(stat_l, shift=UP * 0.3), FadeIn(stat_r, shift=UP * 0.3), run_time=2.5)

        self.at("holds a particular jack")
        jak_l = boxed_label("JAK A", JAK2_COL, 26, box=(1.26, 0.58), fill_opacity=0.34).next_to(rec_l.bracket_pts[1], RIGHT, buff=0.55)
        jak_r = boxed_label("JAK B", JAK3_COL, 26, box=(1.26, 0.58), fill_opacity=0.34).next_to(rec_r.bracket_pts[0], LEFT, buff=0.55)
        brk_lab = fit_text("Near-membrane JAK bracket", max_w=2.4, size=24, color=TEXT).move_to([0.0, 1.48, 0])
        self.play(FadeIn(jak_l), FadeIn(jak_r), FadeIn(brk_lab), run_time=1.0)
        self.play(
            jak_l.animate.next_to(rec_l.bracket_pts[1], RIGHT, buff=0.06),
            jak_r.animate.next_to(rec_r.bracket_pts[0], LEFT, buff=0.06),
            run_time=2.8,
        )

        self.at("distinct docking tyrosines")
        p_l = build_p_tag(rec_l.notch_pts[1] + RIGHT * 0.36)
        p_r = build_p_tag(rec_r.notch_pts[0] + LEFT * 0.36)
        tyr_lab = fit_text("Docking tyrosines", max_w=2.2, size=24, color=PHOS_COL).move_to([0.0, 0.15, 0])
        self.play(FadeIn(p_l, scale=1.3), FadeIn(p_r, scale=1.3), FadeIn(tyr_lab), run_time=1.2)
        self.play(stat_l.animate.shift(UP * 0.65), stat_r.animate.shift(UP * 0.65), run_time=1.4)

        self.at("amino acids")
        flank_l = VGroup(
            Dot(rec_l.notch_pts[1] + UP * 0.24 + RIGHT * 0.04, radius=0.09, color=EPO_REC_COL),
            Dot(rec_l.notch_pts[1] + DOWN * 0.24 + RIGHT * 0.04, radius=0.09, color=EPO_REC_COL),
        )
        flank_r = VGroup(
            Square(side_length=0.15, color=IMM_REC_COL, fill_opacity=0.95).move_to(rec_r.notch_pts[0] + UP * 0.24 + LEFT * 0.04),
            Square(side_length=0.15, color=IMM_REC_COL, fill_opacity=0.95).move_to(rec_r.notch_pts[0] + DOWN * 0.24 + LEFT * 0.04),
        )
        flank_l.layout_ok = True
        flank_r.layout_ok = True
        flank_lab = fit_text("Flanking amino acids select fit", max_w=2.4, size=24, color=TEXT).move_to([0.0, -1.65, 0])
        self.play(FadeIn(flank_l), FadeIn(flank_r), FadeIn(flank_lab), run_time=1.2)
        self.play(stat_l.animate.shift(UP * 0.60), stat_r.animate.shift(UP * 0.60), run_time=1.4)

        self.at("which stats")
        self.play(
            stat_l.animate.move_to(rec_l.notch_pts[1] + RIGHT * 1.56),
            stat_r.animate.move_to(rec_r.notch_pts[0] + LEFT * 1.56),
            run_time=2.2,
        )
        self.finish()


class S03TwoReceptors(SpokenScene):
    def construct(self):
        world = build_cell_world(membrane_y=1.85, dna_y=-2.65, show_labels=False)
        mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, 2.35, 0])
        dna_lab = T("DNA", 28, DNA_COL, weight=BOLD).move_to([-4.65, -2.65, 0])

        rec_l = build_receptor_pair(-3.0, EPO_REC_COL, membrane_y=1.85, spread=0.46, tail_len=1.80, bracket_style="square", notch_style="tri")
        rec_r = build_receptor_pair(2.8, IMM_REC_COL, membrane_y=1.85, spread=0.46, tail_len=1.80, bracket_style="angle", notch_style="square")

        self.add(world, mem_lab, dna_lab, rec_l, rec_r, scope_tag("schematic"))
        vs_line = DashedLine([0, 1.60, 0], [0, -1.85, 0], color=MEMBRANE_COL, stroke_width=3.0)
        vs_line.layout_ok = True
        self.play(Create(vs_line), run_time=1.4)

        self.at("the erythropoietin receptor")
        epo_lab = T("EPO receptor", 28, EPO_REC_COL, weight=BOLD).move_to([-3.0, 3.50, 0])
        jak2_l = boxed_label("JAK2", JAK2_COL, 26, box=(1.22, 0.56), fill_opacity=0.34).next_to(rec_l.bracket_pts[0], LEFT, buff=0.06)
        jak2_r = boxed_label("JAK2", JAK2_COL, 26, box=(1.22, 0.56), fill_opacity=0.34).next_to(rec_l.bracket_pts[1], RIGHT, buff=0.06)
        epo_oval = build_cytokine("EPO").move_to(rec_l.cup_center + UP * 0.28 + RIGHT * 1.35)
        self.play(FadeIn(epo_lab), FadeIn(jak2_l), FadeIn(jak2_r), FadeIn(epo_oval), run_time=1.0)
        self.play(epo_oval.animate.move_to(rec_l.cup_center + UP * 0.28), run_time=1.8)

        self.at("red blood cell")
        p_l = build_p_tag(rec_l.notch_pts[1] + RIGHT * 0.36)
        stat_l = build_stat_dimer("STAT", STAT_COL).move_to([-3.5, -0.36, 0])
        arr_l = Arrow([-3.5, -1.00, 0], [-3.5, -1.65, 0], color=STAT_COL, stroke_width=5.0, buff=0.04)
        rbc_lab = T("Red blood cells", 24, JAK2_COL, weight=BOLD).move_to([-1.40, -1.18, 0])
        rbc_icon = build_red_cells(3).next_to(rbc_lab, DOWN, buff=0.14)
        self.play(FadeIn(p_l), FadeIn(stat_l), run_time=0.5)
        self.play(stat_l.animate.move_to([-3.5, -0.62, 0]), GrowArrow(arr_l), FadeIn(rbc_lab), FadeIn(rbc_icon), run_time=1.8)

        self.at("in immune cells")
        imm_lab = T("Immune receptor", 28, IMM_REC_COL, weight=BOLD).move_to([2.8, 3.35, 0])
        jak3_l = boxed_label("JAK3", JAK3_COL, 26, box=(1.22, 0.56), fill_opacity=0.34).next_to(rec_r.bracket_pts[0], LEFT, buff=0.06)
        jak3_r = boxed_label("JAK3", JAK3_COL, 26, box=(1.22, 0.56), fill_opacity=0.34).next_to(rec_r.bracket_pts[1], RIGHT, buff=0.06)
        imm_oval = build_cytokine("").move_to(rec_r.cup_center + UP * 0.08 + LEFT * 1.35)
        self.play(FadeIn(imm_lab), FadeIn(jak3_l), FadeIn(jak3_r), FadeIn(imm_oval), run_time=1.0)
        self.play(imm_oval.animate.move_to(rec_r.cup_center + UP * 0.08), run_time=1.4)

        p_r = build_p_tag(rec_r.notch_pts[0] + LEFT * 0.36)
        stat_r = build_stat_dimer("STAT", STAT2_COL).move_to([2.3, -0.36, 0])
        arr_r = Arrow([2.3, -1.00, 0], [2.3, -1.65, 0], color=STAT2_COL, stroke_width=5.0, buff=0.04)
        imm_cell_lab = T("Immune cells", 24, IMM_REC_COL, weight=BOLD).move_to([4.60, -1.18, 0])
        imm_icon = build_immune_cells(3).next_to(imm_cell_lab, DOWN, buff=0.14)
        self.play(FadeIn(p_r), FadeIn(stat_r), run_time=0.4)
        self.play(stat_r.animate.move_to([2.3, -0.62, 0]), GrowArrow(arr_r), FadeIn(imm_cell_lab), FadeIn(imm_icon), run_time=1.5)

        self.at("different tails")
        cap = caption("Different tails assign different JAKs to different jobs.", size=28, color=GOLD, y=-3.28)
        self.play(FadeIn(cap), run_time=0.9)
        self.play(rbc_icon.animate.shift(RIGHT * 0.14), imm_icon.animate.shift(LEFT * 0.14), run_time=1.2)
        self.play(rbc_icon.animate.shift(LEFT * 0.14), imm_icon.animate.shift(RIGHT * 0.14), run_time=1.2)
        self.finish()


class S04PredictLoss(SpokenScene):
    def construct(self):
        world = build_cell_world(membrane_y=1.85, dna_y=-2.35, show_labels=False)
        mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, 2.35, 0])
        dna_lab = T("DNA", 28, DNA_COL, weight=BOLD).move_to([-4.65, -2.35, 0])
        world.add(mem_lab, dna_lab)

        rec = build_receptor_pair(-2.1, EPO_REC_COL, membrane_y=1.85, spread=0.50, tail_len=1.85, bracket_style="square")
        rec_lab = T("EPO receptor", 28, EPO_REC_COL, weight=BOLD).move_to([-2.1, 3.50, 0])
        jak2_l = boxed_label("JAK2", JAK2_COL, 26, box=(1.24, 0.56), fill_opacity=0.34).next_to(rec.bracket_pts[0], LEFT, buff=0.06)
        jak2_r = boxed_label("JAK2", JAK2_COL, 26, box=(1.24, 0.56), fill_opacity=0.34).next_to(rec.bracket_pts[1], RIGHT, buff=0.06)

        j1 = boxed_label("JAK1", JAK1_COL, 26, box=(1.36, 0.60), fill_opacity=0.34).move_to([2.0, 1.25, 0])
        j3 = boxed_label("JAK3", JAK3_COL, 26, box=(1.36, 0.60), fill_opacity=0.34).move_to([4.1, 0.70, 0])
        tyk = boxed_label("TYK2", TYK2_COL, 26, box=(1.36, 0.60), fill_opacity=0.34).move_to([2.2, 0.10, 0])
        other_lab = T("Intact other JAKs", 28, TEXT, weight=BOLD).move_to([3.05, 2.55, 0])

        self.add(world, rec, rec_lab, jak2_l, jak2_r)
        self.play(FadeIn(j1, shift=DOWN * 0.2), FadeIn(j3, shift=DOWN * 0.2), FadeIn(tyk, shift=DOWN * 0.2), FadeIn(other_lab), run_time=1.3)
        sim_lab = T("Similar sequence across all 4 JAKs", 26, GOLD).move_to([3.05, -0.95, 0])
        self.play(FadeIn(sim_lab), run_time=1.0)
        self.play(j1.animate.shift(LEFT * 0.45), j3.animate.shift(LEFT * 0.45), tyk.animate.shift(LEFT * 0.45), run_time=2.2)

        self.at("cover for one another")
        probe_arr = Arrow([1.00, 1.25, 0], [-0.15, 1.25, 0], color=GOLD, stroke_width=4.5)
        self.play(GrowArrow(probe_arr), FadeOut(sim_lab), run_time=1.0)
        self.play(
            j1.animate.move_to([2.0, 1.25, 0]),
            j3.animate.move_to([4.1, 0.70, 0]),
            tyk.animate.move_to([2.2, 0.10, 0]),
            FadeOut(probe_arr),
            run_time=2.2,
        )

        self.at("mouse embryo lacks")
        sock_l = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.24, height=0.56, stroke_color=JAK2_COL, stroke_width=3.2), num_dashes=12)
        sock_r = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.24, height=0.56, stroke_color=JAK2_COL, stroke_width=3.2), num_dashes=12)
        sock_l.move_to(jak2_l)
        sock_r.move_to(jak2_r)
        sock_l.layout_ok = True
        sock_r.layout_ok = True
        no_jak = T("No JAK2", 28, JAK2_COL, weight=BOLD).move_to([-2.1, -0.58, 0])
        self.play(FadeOut(jak2_l), FadeOut(jak2_r), Create(sock_l), Create(sock_r), FadeIn(no_jak), run_time=1.5)

        self.at("will the other three")
        rec_bound = build_receptor_pair(-2.1, EPO_REC_COL, membrane_y=1.85, spread=0.38, tail_len=1.85, bracket_style="square")
        epo = build_cytokine("EPO").move_to(rec_bound.cup_center + UP * 0.28 + LEFT * 1.45)
        sock_l_b = sock_l.copy().next_to(rec_bound.bracket_pts[0], LEFT, buff=0.06)
        sock_r_b = sock_r.copy().next_to(rec_bound.bracket_pts[1], RIGHT, buff=0.06)
        sock_l_b.layout_ok = True
        sock_r_b.layout_ok = True
        q = question_card("Will other JAKs substitute for JAK2?", max_w=10.5)
        self.play(FadeIn(epo), run_time=0.4)
        self.play(
            epo.animate.move_to(rec_bound.cup_center + UP * 0.28),
            Transform(rec, rec_bound),
            Transform(sock_l, sock_l_b),
            Transform(sock_r, sock_r_b),
            FadeIn(q),
            run_time=2.2,
        )
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = "Will other JAKs substitute for JAK2?"
    OPTIONS = ()
    CARD = {"max_w": 10.5}
    SECONDS = 4.5

    def backdrop(self):
        static_stage, jaks = build_epo_predict_stage()
        for idx, j in enumerate(jaks):
            bob(j, amp=0.12, speed=2.2, seed=idx)
        return VGroup(static_stage, jaks)


class S06RevealSpecificity(SpokenScene):
    def construct(self):
        static_stage, jaks = build_epo_predict_stage()
        q = question_card("Will other JAKs substitute for JAK2?", max_w=10.5)
        self.add(static_stage, jaks, q, scope_tag("schematic"))

        self.at("that pathway fails")
        fail_lab = T("Pathway fails", 28, JAK2_COL, weight=BOLD).move_to([-2.1, -1.10, 0])
        self.play(FadeOut(q), FadeIn(fail_lab), run_time=1.0)
        self.play(jaks.animate.shift(LEFT * 0.45), run_time=2.8)

        self.at("early wave of red cells")
        early_cells = build_red_cells(2).move_to([-5.05, -1.10, 0])
        early_lab = T("Early wave", 24, TEXT).next_to(early_cells, UP, buff=0.14)
        self.play(FadeIn(early_cells), FadeIn(early_lab), run_time=1.2)

        self.at("none of the lasting")
        empty_slot = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=5.25, height=0.72, stroke_color=JAK2_COL, stroke_width=3.2), num_dashes=24).move_to([-1.32, -1.22, 0])
        empty_slot.layout_ok = True
        no_adult = T("No lasting (adult-type) red cells", 24, JAK2_COL, weight=BOLD).move_to(empty_slot)
        self.play(FadeOut(fail_lab), Create(empty_slot), FadeIn(no_adult), run_time=1.2)

        self.at("the other three jacks")
        orig_pos = [[2.0, 1.25, 0], [4.1, 0.70, 0], [2.2, 0.10, 0]]
        self.play(
            jaks[0].animate.move_to([0.60, 1.18, 0]),
            jaks[1].animate.move_to([0.60, 0.50, 0]),
            jaks[2].animate.move_to([0.25, -0.18, 0]),
            run_time=1.5,
        )
        self.play(*[j.animate.move_to(p) for j, p in zip(jaks, orig_pos)], run_time=1.6)

        self.at("do not substitute")
        not_rep = boxed_label("JAK2 is not replaced", JAK2_COL, 26, fill_opacity=0.30).move_to([3.45, -1.05, 0])
        hedge = boxed_label("STAT5A & 5B partly overlap", STAT_COL, 24, fill_opacity=0.26).move_to([2.5, -3.20, 0])
        self.play(FadeIn(not_rep), FadeIn(hedge), run_time=1.0)
        self.finish()


class S07Phosphatases(SpokenScene):
    def construct(self):
        world = build_cell_world(membrane_y=1.85, dna_y=-2.65, show_labels=False, nuc_offset=1.05)
        mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, 2.35, 0])
        dna_lab = T("DNA", 28, DNA_COL, weight=BOLD).move_to([-4.65, -2.65, 0])

        rec = build_receptor_pair(-2.6, EPO_REC_COL, membrane_y=1.85, spread=0.45, tail_len=1.85, bracket_style="square", notch_style="tri")
        epo = build_cytokine("EPO").move_to(rec.cup_center + UP * 0.28)
        jak_l = boxed_label("JAK2", JAK2_COL, 26, box=(1.22, 0.56), fill_opacity=0.34).next_to(rec.bracket_pts[0], LEFT, buff=0.06)
        jak_r = boxed_label("JAK2", JAK2_COL, 26, box=(1.22, 0.56), fill_opacity=0.34).next_to(rec.bracket_pts[1], RIGHT, buff=0.06)
        p_jl = build_p_tag(jak_l.get_left() + LEFT * 0.36)
        p_jr = build_p_tag(jak_r.get_right() + RIGHT * 0.36)
        p_tl = build_p_tag(rec.notch_pts[0] + LEFT * 0.38)
        p_tr = build_p_tag(rec.notch_pts[1] + RIGHT * 0.38)

        dimer = build_stat_dimer("STAT", STAT_COL).move_to([-0.2, -0.35, 0])
        status = T("Healthy active signal", 28, STAT_COL, weight=BOLD).move_to([2.9, 3.20, 0])

        self.add(world, mem_lab, dna_lab, rec, epo, jak_l, jak_r, p_jl, p_jr, p_tl, p_tr, dimer, status, scope_tag("schematic"))
        self.play(dimer.animate.move_to([0.0, -2.10, 0]), run_time=3.2)

        self.at("two main breaks")
        brake_title = T("Brake 1: Tyrosine phosphatases", 28, PHOSPHATASE_COL, weight=BOLD).move_to([2.9, 3.20, 0])
        self.play(swap(status, brake_title), run_time=1.0)
        phos = build_phosphatase([4.3, 1.05, 0])
        self.play(FadeIn(phos, shift=LEFT * 0.5), run_time=2.4)

        self.at("tyrosine phosphatases")
        self.play(phos.animate.move_to([2.2, 1.05, 0]), run_time=1.2)

        self.at("from jax")
        self.play(phos.animate.move_to([1.75, 1.05, 0]), run_time=0.7)
        self.play(FadeOut(p_jl, shift=UP * 0.2), FadeOut(p_jr, shift=UP * 0.2), run_time=0.5)

        self.at("receptor tails")
        self.play(phos.animate.move_to([1.55, 0.25, 0]), run_time=0.6)
        self.play(FadeOut(p_tl, shift=UP * 0.2), FadeOut(p_tr, shift=UP * 0.2), run_time=0.5)

        self.at("and stats")
        self.play(phos.animate.move_to([3.55, -1.94, 0]), run_time=1.2)

        self.at("loses its phosphate")
        self.play(FadeOut(dimer.p_tags, shift=UP * 0.25), run_time=0.9)
        s_l, s_r = dimer.left_stat, dimer.right_stat
        self.play(s_l.animate.shift(LEFT * 0.45 + UP * 0.90), s_r.animate.shift(RIGHT * 0.45 + UP * 0.90), run_time=1.0)

        self.at("returns to the cytoplasm")
        reuse_lab = boxed_label("STAT returns: ready for reuse", STAT_COL, 26, fill_opacity=0.28).move_to([3.05, 0.65, 0])
        self.play(
            phos.animate.move_to([-4.2, -0.85, 0]),
            s_l.animate.move_to([2.1, -0.45, 0]),
            s_r.animate.move_to([3.8, -0.45, 0]),
            FadeIn(reuse_lab),
            run_time=2.2,
        )
        self.finish()


class S08SocsFeedback(SpokenScene):
    def construct(self):
        world = build_cell_world(membrane_y=1.85, dna_y=-2.65, show_labels=False, nuc_offset=1.05)
        mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, 2.35, 0])
        dna_lab = T("DNA", 28, DNA_COL, weight=BOLD).move_to([-4.65, -2.65, 0])

        rec_l = build_receptor_pair(-2.8, EPO_REC_COL, membrane_y=1.85, spread=0.42, tail_len=1.80, bracket_style="square")
        epo_l = build_cytokine("EPO").move_to(rec_l.cup_center + UP * 0.28)
        jak_l_p = boxed_label("Pseudo", PSEUDO_COL, 24, box=(1.26, 0.50), fill_opacity=0.34).next_to(rec_l.bracket_pts[1], RIGHT, buff=0.06).set_y(1.25)
        jak_l_k = boxed_label("Kinase", JAK2_COL, 24, box=(1.26, 0.50), fill_opacity=0.34).next_to(jak_l_p, DOWN, buff=0.10)

        rec_r = build_receptor_pair(2.6, EPO_REC_COL, membrane_y=1.85, spread=0.42, tail_len=1.80, bracket_style="square")
        epo_r = build_cytokine("EPO").move_to(rec_r.cup_center + UP * 0.28)
        jak_r = boxed_label("JAK2", JAK2_COL, 26, box=(1.22, 0.56), fill_opacity=0.34).next_to(rec_r.bracket_pts[1], RIGHT, buff=0.06)

        dimer = build_stat_dimer("STAT", STAT_COL).move_to([-0.2, -0.25, 0])
        title = T("Brake 2: SOCS negative feedback", 28, SOCS_COL, weight=BOLD).move_to([0, 3.55, 0])

        self.add(world, mem_lab, dna_lab, rec_l, epo_l, jak_l_p, jak_l_k, rec_r, epo_r, jak_r, dimer, title, scope_tag("schematic"))
        self.play(dimer.animate.move_to([-0.2, -2.10, 0]), run_time=3.6)

        self.at("genes that stats switch on")
        gene_box = RoundedRectangle(corner_radius=0.10, width=2.2, height=0.54, stroke_color=SOCS_COL, stroke_width=3.5, fill_color=SOCS_COL, fill_opacity=0.28).move_to([2.4, -2.65, 0])
        gene_lab = T("SOCS gene", 24, SOCS_COL, weight=BOLD).next_to(gene_box, RIGHT, buff=0.42)
        self.play(Create(gene_box), FadeIn(gene_lab), run_time=1.3)
        tx_arrow = Arrow([2.4, -2.30, 0], [2.4, -1.60, 0], color=SOCS_COL, stroke_width=4.0)
        self.play(GrowArrow(tx_arrow), run_time=1.6)

        self.at("suppressors of cytokine signaling")
        socs_def = T("SOCS: Suppressor of Cytokine Signaling", 26, SOCS_COL).move_to([0.0, -3.28, 0])
        self.play(FadeIn(socs_def), FadeOut(tx_arrow), run_time=1.4)

        self.at("after a delay")
        clock_ring = Circle(radius=0.40, color=GOLD, stroke_width=4.0).move_to([-5.0, -0.35, 0])
        ang = ValueTracker(PI / 2)
        hand = always_redraw(lambda: Line(
            clock_ring.get_center(),
            clock_ring.get_center() + 0.30 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
            color=GOLD, stroke_width=4.0,
        ))
        delay_lab = T("Delay", 26, GOLD, weight=BOLD).next_to(clock_ring, DOWN, buff=0.14)
        socs1 = build_socs_shield("SOCS").move_to([2.0, -1.35, 0])
        socs2 = build_socs_shield("SOCS").move_to([3.6, -1.35, 0])
        self.play(FadeIn(clock_ring), FadeIn(delay_lab), run_time=0.3)
        self.add(hand)
        self.play(ang.animate.set_value(PI / 2 - TAU), FadeIn(socs1, shift=UP * 0.25), FadeIn(socs2, shift=UP * 0.25), run_time=1.6)

        self.at("dock on the active receptor")
        self.play(
            socs1.animate.move_to(jak_l_k.get_center() + DOWN * 0.85),
            socs2.animate.move_to(jak_r.get_center() + DOWN * 0.78),
            run_time=1.5,
        )

        self.at("block the jack directly")
        blk_lab = boxed_label("Blocks JAK", SOCS_COL, 26, fill_opacity=0.30).move_to([-2.8, -0.80, 0])
        self.play(FadeOut(jak_l_k), socs1.animate.move_to(jak_l_k.get_center() + DOWN * 0.10), FadeIn(blk_lab), run_time=1.2)

        self.at("tag the complex")
        beads = VGroup(*[
            Dot(jak_r.get_right() + RIGHT * (0.24 + i * 0.24), radius=0.12, color=SOCS_COL)
            for i in range(3)
        ])
        beads.layout_ok = True
        tag_lab = boxed_label("Tagged for breakdown", SOCS_COL, 26, fill_opacity=0.30).move_to([3.2, -0.80, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=1.3) for b in beads], lag_ratio=0.15), FadeIn(tag_lab), run_time=1.4)
        self.finish()


class S09StuckOn(SpokenScene):
    def construct(self):
        mem = build_membrane(y=2.25)
        mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, 2.78, 0])
        rec = build_receptor_pair(-0.4, EPO_REC_COL, membrane_y=2.25, spread=1.95, tail_len=2.60, bracket_style="square")
        no_epo = T("No EPO outside", 28, CYTOKINE_COL, weight=BOLD).move_to([-0.4, 3.25, 0])

        pseudo_l = boxed_label("Pseudo", PSEUDO_COL, 24, box=(1.36, 0.56), fill_opacity=0.34).move_to([-1.45, 1.25, 0])
        kin_l = boxed_label("Kinase", JAK2_COL, 24, box=(1.36, 0.56), fill_opacity=0.34).next_to(pseudo_l, DOWN, buff=0.16)
        pseudo_r = boxed_label("Pseudo", PSEUDO_COL, 24, box=(1.36, 0.56), fill_opacity=0.34).move_to([0.65, 1.25, 0])
        kin_r = boxed_label("Kinase", JAK2_COL, 24, box=(1.36, 0.56), fill_opacity=0.34).next_to(pseudo_r, DOWN, buff=0.16)

        status = T("Restrained (OFF)", 28, PSEUDO_COL, weight=BOLD).move_to([-4.35, -1.55, 0])
        self.add(mem, mem_lab, scope_tag("schematic"))
        self.play(Create(rec), FadeIn(no_epo), run_time=1.6)
        self.play(
            FadeIn(pseudo_l, shift=DOWN * 0.2), FadeIn(kin_l, shift=UP * 0.25),
            FadeIn(pseudo_r, shift=DOWN * 0.2), FadeIn(kin_r, shift=UP * 0.25),
            FadeIn(status), run_time=1.8,
        )

        self.at("the pseudokinase lobe")
        clamp_l = Arrow(pseudo_l.get_bottom(), kin_l.get_top(), color=PSEUDO_COL, stroke_width=5.0, buff=0.02)
        clamp_r = Arrow(pseudo_r.get_bottom(), kin_r.get_top(), color=PSEUDO_COL, stroke_width=5.0, buff=0.02)
        clamp_l.layout_ok = True
        clamp_r.layout_ok = True
        self.play(GrowArrow(clamp_l), GrowArrow(clamp_r), run_time=1.4)
        self.play(kin_l.animate.shift(DOWN * 0.25), kin_r.animate.shift(DOWN * 0.25), run_time=1.8)
        self.play(kin_l.animate.shift(UP * 0.25), kin_r.animate.shift(UP * 0.25), run_time=1.8)

        self.at("one amino acid change")
        pv_lab = T("Polycythaemia vera", 28, CYTOKINE_COL, weight=BOLD).move_to([4.05, 3.25, 0])
        dot_l = Dot(pseudo_l.get_corner(UR), radius=0.09, color=CYTOKINE_COL)
        dot_r = Dot(pseudo_r.get_corner(UL), radius=0.09, color=CYTOKINE_COL)
        v617_l = T("V617F", 24, CYTOKINE_COL, weight=BOLD).next_to(pseudo_l, UP, buff=0.20)
        v617_r = T("V617F", 24, CYTOKINE_COL, weight=BOLD).next_to(pseudo_r, UP, buff=0.20)
        self.play(FadeIn(pv_lab), FadeIn(dot_l, scale=1.6), FadeIn(dot_r, scale=1.6), FadeIn(v617_l), FadeIn(v617_r), run_time=1.5)
        self.play(dot_l.animate.scale(1.45), dot_r.animate.scale(1.45), run_time=0.8)
        self.play(dot_l.animate.scale(1 / 1.45), dot_r.animate.scale(1 / 1.45), run_time=1.8)

        self.at("weakens restraint")
        status_weak = T("Restraint weakened", 28, CYTOKINE_COL, weight=BOLD).move_to([-4.25, -1.55, 0])
        self.play(FadeOut(clamp_l), FadeOut(clamp_r), swap(status, status_weak, run_time=0.9), run_time=0.9)

        self.at("helps two jacks pair")
        pair_l = VGroup(pseudo_l, dot_l, v617_l)
        pair_r = VGroup(pseudo_r, dot_r, v617_r)
        self.play(pair_l.animate.shift(RIGHT * 0.20), pair_r.animate.shift(LEFT * 0.20), run_time=1.5)

        self.at("then fires")
        p1 = build_p_tag([-2.75, 0.53, 0])
        p2 = build_p_tag([1.95, 0.53, 0])
        p3 = build_p_tag([-1.75, -0.20, 0])
        p4 = build_p_tag([0.95, -0.20, 0])
        status_on = T("Active without EPO", 28, JAK2_COL, weight=BOLD).move_to([-4.25, -1.55, 0])
        self.play(
            FadeIn(p1, scale=1.4), FadeIn(p2, scale=1.4), FadeIn(p3, scale=1.4), FadeIn(p4, scale=1.4),
            swap(status_weak, status_on, run_time=1.4),
            run_time=1.4,
        )

        self.at("producing too many red cells")
        stats = VGroup(
            build_stat_dimer("STAT", STAT_COL, with_p=False).move_to([-0.4, -1.25, 0]),
            build_stat_dimer("STAT", STAT_COL, with_p=False).move_to([-0.4, -2.15, 0]),
        )
        rbc_many = VGroup(build_red_cells(4), build_red_cells(4)).arrange(DOWN, buff=0.14).move_to([4.0, -1.75, 0])
        rbc_lab = T("Too many red cells", 26, JAK2_COL, weight=BOLD).next_to(rbc_many, UP, buff=0.16)
        self.play(FadeIn(stats, shift=DOWN * 0.45), FadeIn(rbc_many), FadeIn(rbc_lab), run_time=1.6)
        self.finish()


class S10RuleClose(SpokenScene):
    def construct(self):
        mem = build_membrane(y=2.45)
        mem_lab = T("Membrane", 26, TEXT).move_to([-5.35, 2.95, 0])
        dna = build_dna_helix(y=-2.50, width=7.2)
        dna_lab = T("DNA", 28, DNA_COL, weight=BOLD).next_to(dna, LEFT, buff=0.25)
        tp = TwoPanel("Tail sorting", "Brakes", colors=(EPO_REC_COL, SOCS_COL), top=2.12, bottom=-1.80, gap=0.5, width=12.4, size=30)
        self.add(mem, mem_lab, dna, dna_lab, tp, scope_tag("schematic"))

        miss_txt = boxed_label("No JAK2 -> EPO receptor silent", JAK2_COL, 26, fill_opacity=0.30).move_to([-3.25, 0.70, 0])
        self.play(FadeIn(miss_txt), run_time=1.5)
        self.play(miss_txt.animate.shift(DOWN * 0.25), run_time=2.2)

        self.at("loosening its restraint")
        stuck_txt = boxed_label("V617F -> JAK2 stuck ON", CYTOKINE_COL, 26, fill_opacity=0.30).move_to([3.25, 0.70, 0])
        self.play(FadeIn(stuck_txt), run_time=1.5)
        self.play(stuck_txt.animate.shift(DOWN * 0.25), run_time=2.2)

        self.at("so receptor tails")
        left_group = VGroup(
            VGroup(
                boxed_label("EPO receptor", EPO_REC_COL, 24, box=(2.2, 0.54), fill_opacity=0.30),
                boxed_label("JAK2", JAK2_COL, 24, box=(1.1, 0.54), fill_opacity=0.32),
                boxed_label("STAT", STAT_COL, 24, box=(1.1, 0.54), fill_opacity=0.32),
            ).arrange(RIGHT, buff=0.16),
            VGroup(
                boxed_label("Immune rec.", IMM_REC_COL, 24, box=(2.2, 0.54), fill_opacity=0.30),
                boxed_label("JAK3", JAK3_COL, 24, box=(1.1, 0.54), fill_opacity=0.32),
                boxed_label("STAT", STAT2_COL, 24, box=(1.1, 0.54), fill_opacity=0.32),
            ).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, buff=0.35).move_to([-3.25, -0.25, 0])
        self.play(FadeOut(miss_txt), FadeIn(left_group), run_time=1.4)

        self.at("while breaks restrain")
        right_group = VGroup(
            boxed_label("1. Pseudokinase restraint", PSEUDO_COL, 24, box=(4.6, 0.54), fill_opacity=0.30),
            boxed_label("2. Tyrosine phosphatases", PHOSPHATASE_COL, 24, box=(4.6, 0.54), fill_opacity=0.30),
            boxed_label("3. SOCS feedback shields", SOCS_COL, 24, box=(4.6, 0.54), fill_opacity=0.30),
        ).arrange(DOWN, buff=0.26).move_to([3.25, -0.25, 0])
        self.play(FadeOut(stuck_txt), FadeIn(right_group), run_time=1.4)

        self.at("together receptor sorting")
        rule = caption("Receptor tails select specific JAKs and STATs, while brakes restrain signaling.", size=26, color=GOLD, y=-3.25)
        self.play(FadeIn(rule), run_time=1.4)
        self.play(left_group.animate.shift(UP * 0.16), right_group.animate.shift(DOWN * 0.16), run_time=2.2)
        self.play(left_group.animate.shift(DOWN * 0.16), right_group.animate.shift(UP * 0.16), run_time=2.2)
        self.finish()


class S11End(EndCard):
    LINE = "Receptor tails select specific JAKs and STATs, while brakes restrain signaling."
