"""
How Bacteria Make Human Insulin — STEMhop ("Engineering Genes")

COLOUR MAP (one colour per concept for the entire film):
    BLUE   (#58C4DD) = bacterial plasmid
    GREEN  (#83C167) = intended gene, working control tab, or insulin product
    YELLOW (#F5D547) = tools (restriction enzyme, DNA ligase, recognition marks)
    RED    (#FC6255) = selection or risk (antibiotic plate, resistance marker, non-working tab warning)
    TEAL   (#3FB8C0) = evidence (1982 FDA approval, testing question mark)
    PURPLE (#9A72AC) = values (reserved in house colour map)
    GREY   (#8B93A1) = bacteria, main chromosome, introns, bacterial reader, schematic tag
    TEXT   (#E8EAF0) = neutral labels, animal icons, medicine vials

CARRIED WORLD:
    A schematic view of a gray bacterium and a circular blue plasmid into which a green
    intron-free human insulin gene and control tab are cut and joined by yellow tools,
    selected on a red antibiotic plate, and read into green insulin product vials.

WHAT CHANGES IN EACH SPOKEN SCENE (computed / animated from the narration):
    s01_hook:        Missing green gene slot pulses above a large gray bacterium; cattle & pig
                     icons slide in ("from the 1920s") then slide aside as the green gene enters
                     the bacterium ("1982 FDA approval") and an insulin vial moves beside it.
    s02_instruction: Green insulin DNA grows; gray intron segments drop out and green coding
                     segments fuse into one intron-free block; control tab locks onto its left
                     edge; gray bacterial reader sweeps across and pauses.
    s03_cut:         Yellow restriction enzyme visits matching yellow marks on the green gene
                     and blue plasmid, cutting both open into complementary stepped sticky ends.
    s04_join:        Green gene slides into the opened blue plasmid; yellow DNA ligase seals both
                     joins; completed recombinant loop rotates smoothly, then copies separately
                     beside a bacterium's main chromosome.
    s05_predict:     Warning stripes fade across the control tab of the large recombinant plasmid;
                     gray bacterial reader approaches and stops short; predict question appears.
    s07_reveal:      Striped control tab slides away and a working green tab locks in; reader sweeps
                     across the gene while green insulin-product blocks grow along a dotted path
                     into an insulin-product collection vial.
    s08_select:      Recombinant plasmid enters 1 of 3 bacteria; all move onto a red antibiotic
                     plate; plasmid-free cells fade to outlines while the plasmid-bearing cell
                     divides into a growing colony (1 -> 2 -> 4 -> 8 cells).
    s09_copy:        Surviving cell divides twice (1 -> 2 -> 4 daughters) with computed plasmid
                     duplication into each daughter; green product blocks stream through a
                     schematic purification funnel into insulin vials ("if switched on" held).
    s10_rule:        Carried objects transform left-to-right into the 5-step chain (cut, join,
                     carry, select, read) followed by a teal question mark and the rule caption.
"""

from bp_parts import *

PURPLE = "#9A72AC"


# ---------------------------------------------------------------------------
# Shared schematic builders (rebuilt in matching coordinates across scenes)
# ---------------------------------------------------------------------------

def make_bacterium(center=ORIGIN, width=4.6, height=2.1, color=GREY, chromosome=True, fill_opacity=0.28):
    """Schematic rod-shaped bacterium with optional outline-only tangled main chromosome."""
    outer = RoundedRectangle(
        corner_radius=height / 2, width=width, height=height,
        stroke_color=color, stroke_width=5.0, fill_color=color, fill_opacity=fill_opacity,
    ).move_to(center)
    inner = RoundedRectangle(
        corner_radius=max(0.1, height / 2 - 0.1),
        width=width - 0.24, height=height - 0.24,
        stroke_color=color, stroke_width=2.0, fill_opacity=0,
    ).move_to(center)
    g = VGroup(outer, inner)
    g.body = outer
    g.inner = inner
    g.chromosome = None
    if chromosome:
        rx, ry = width * 0.16, height * 0.24
        cx = center[0] + width * 0.20
        cy = center[1]
        chrom = ParametricFunction(
            lambda t: np.array([
                cx + rx * np.sin(2 * t + 0.4) * np.cos(t * 0.5),
                cy + ry * np.sin(3 * t),
                0.0,
            ]),
            t_range=[0, TAU], color=color, stroke_width=3.2, fill_opacity=0,
        ).set_fill(opacity=0).set_stroke(opacity=0.85)
        g.add(chrom)
        g.chromosome = chrom
    return g


def make_vial(center=ORIGIN, height=1.8, liquid_color=GREEN, liquid_frac=0.55):
    """Schematic glass medicine vial with liquid strictly inside body bounds."""
    w = height * 0.56
    body_h = height * 0.68
    neck_h = height * 0.14
    cap_h = height * 0.14
    c = np.array(center, dtype=float)
    body = RoundedRectangle(
        corner_radius=0.1, width=w, height=body_h,
        stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.14,
    ).move_to(c + DOWN * (height * 0.14))
    neck = Rectangle(
        width=w * 0.46, height=neck_h,
        stroke_color=TEXT, stroke_width=3.0, fill_color=TEXT, fill_opacity=0.14,
    ).next_to(body, UP, buff=0)
    cap = RoundedRectangle(
        corner_radius=0.04, width=w * 0.64, height=cap_h,
        stroke_color=GREY, stroke_width=2.8, fill_color=GREY, fill_opacity=0.65,
    ).next_to(neck, UP, buff=0)
    liq_h = max(0.08, (body_h - 0.14) * liquid_frac)
    liq = Rectangle(
        width=w - 0.14, height=liq_h,
        stroke_width=0, fill_color=liquid_color, fill_opacity=0.78,
    )
    liq.move_to([body.get_center()[0], body.get_bottom()[1] + 0.07 + liq_h / 2, 0])
    g = VGroup(liq, body, neck, cap)
    g.body = body
    g.liquid = liq
    return g


def make_cattle_icon(center=ORIGIN, scale=1.0, color=TEXT):
    """Simple geometric cattle silhouette."""
    c = np.array(center, dtype=float)
    body = RoundedRectangle(corner_radius=0.18, width=1.2, height=0.65, stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.28)
    head = RoundedRectangle(corner_radius=0.1, width=0.44, height=0.40, stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.28)
    head.next_to(body, RIGHT, buff=-0.06).shift(UP * 0.14)
    horn_l = ArcBetweenPoints(head.get_top() + LEFT * 0.1, head.get_top() + LEFT * 0.22 + UP * 0.22, angle=0.6, color=color, stroke_width=3.0)
    horn_r = ArcBetweenPoints(head.get_top() + RIGHT * 0.1, head.get_top() + RIGHT * 0.22 + UP * 0.22, angle=-0.6, color=color, stroke_width=3.0)
    legs = VGroup(*[
        Line(body.get_bottom() + RIGHT * dx, body.get_bottom() + RIGHT * dx + DOWN * 0.30, color=color, stroke_width=3.5)
        for dx in (-0.38, -0.18, 0.2, 0.4)
    ])
    return VGroup(legs, body, head, horn_l, horn_r).scale(scale).move_to(c)


def make_pig_icon(center=ORIGIN, scale=1.0, color=TEXT):
    """Simple geometric pig silhouette."""
    c = np.array(center, dtype=float)
    body = RoundedRectangle(corner_radius=0.25, width=1.05, height=0.62, stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.28)
    head = Circle(radius=0.23, stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.28)
    head.next_to(body, RIGHT, buff=-0.08).shift(UP * 0.04)
    snout = RoundedRectangle(corner_radius=0.05, width=0.16, height=0.16, stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.35)
    snout.next_to(head, RIGHT, buff=-0.04)
    ear = Polygon(head.get_top() + LEFT * 0.08, head.get_top() + RIGHT * 0.04, head.get_top() + UP * 0.16 + LEFT * 0.04,
                  stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.3)
    legs = VGroup(*[
        Line(body.get_bottom() + RIGHT * dx, body.get_bottom() + RIGHT * dx + DOWN * 0.24, color=color, stroke_width=3.5)
        for dx in (-0.3, -0.12, 0.16, 0.32)
    ])
    return VGroup(legs, body, head, snout, ear).scale(scale).move_to(c)


def make_gene_block(width=3.6, height=0.92, color=GREEN, sticky=False, notch=0.40, ticks=True, fill_opacity=0.40,
                    left_sticky=None, right_sticky=None):
    """Schematic DNA gene block with optional stepped sticky-end overhangs."""
    hw, hh = width / 2, height / 2
    if left_sticky is None:
        left_sticky = sticky
    if right_sticky is None:
        right_sticky = sticky
    if not left_sticky and not right_sticky:
        shape = RoundedRectangle(
            corner_radius=0.1, width=width, height=height,
            stroke_color=color, stroke_width=4.0, fill_color=color, fill_opacity=fill_opacity,
        )
    else:
        pts = [[-hw - notch, hh, 0]] if left_sticky else [[-hw, hh, 0]]
        if right_sticky:
            pts.extend([[hw, hh, 0], [hw, 0, 0], [hw + notch, 0, 0], [hw + notch, -hh, 0]])
        else:
            pts.extend([[hw, hh, 0], [hw, -hh, 0]])
        if left_sticky:
            pts.extend([[-hw, -hh, 0], [-hw, 0, 0], [-hw - notch, 0, 0]])
        else:
            pts.append([-hw, -hh, 0])
        shape = Polygon(*pts, stroke_color=color, stroke_width=4.0, fill_color=color, fill_opacity=fill_opacity)
    g = VGroup(shape)
    g.shape = shape
    g.rungs = VGroup()
    if ticks:
        n_ticks = max(4, int(width / 0.45))
        xs = np.linspace(-hw + 0.25, hw - 0.25, n_ticks)
        rung_lines = VGroup(*[
            Line([x, -hh + 0.14, 0], [x, hh - 0.14, 0], color=color, stroke_width=2.4).set_opacity(0.75)
            for x in xs
        ])
        g.add(rung_lines)
        g.rungs = rung_lines
    return g


def make_control_tab(width=1.4, height=0.92, working=True, striped=False, sticky=False, notch=0.40):
    """Bacterial control DNA tab locking onto the left edge of a gene block."""
    hw, hh = width / 2, height / 2
    if sticky:
        pts = [
            [-hw - notch, hh, 0],
            [hw, hh, 0],
            [hw, -hh, 0],
            [-hw, -hh, 0],
            [-hw, 0, 0],
            [-hw - notch, 0, 0],
        ]
    else:
        pts = [
            [-hw + 0.2, hh, 0],
            [hw, hh, 0],
            [hw, -hh, 0],
            [-hw + 0.2, -hh, 0],
            [-hw, 0, 0],
        ]
    col = GREEN
    tab = Polygon(*pts, stroke_color=col, stroke_width=4.0, fill_color=col, fill_opacity=0.45 if working else 0.26)
    arrow_mark = Triangle(stroke_color=col if not striped else RED, stroke_width=2, fill_color=col if not striped else RED, fill_opacity=0.9)
    arrow_mark.scale(0.18).rotate(-PI / 2).move_to([0.05, 0, 0])
    g = VGroup(tab, arrow_mark)
    g.body = tab
    if striped:
        stripes = VGroup()
        for dx in (-0.28, 0.02, 0.32):
            stripes.add(Line([dx - 0.12, -hh + 0.08, 0], [dx + 0.16, hh - 0.08, 0], color=RED, stroke_width=4.5))
        g.add(stripes)
        g.stripes = stripes
    return g


def make_reader(center=ORIGIN, scale=1.0, color=GREY):
    """Schematic bacterial reader clamp riding along DNA."""
    top = RoundedRectangle(corner_radius=0.32, width=1.1, height=0.68, stroke_color=TEXT, stroke_width=3.0, fill_color=color, fill_opacity=0.78)
    bot = RoundedRectangle(corner_radius=0.18, width=0.86, height=0.34, stroke_color=TEXT, stroke_width=3.0, fill_color=color, fill_opacity=0.68)
    bot.next_to(top, DOWN, buff=0.12)
    return VGroup(top, bot).scale(scale).move_to(center)


def make_enzyme_tool(center=ORIGIN, scale=1.0, color=YELLOW):
    """Yellow restriction-enzyme cutting tool (scissors-jaw icon)."""
    b1 = Polygon([0, 0, 0], [0.75, 0.24, 0], [0.68, 0.04, 0], [0.05, -0.06, 0], stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.9)
    b2 = Polygon([0, 0, 0], [0.75, -0.24, 0], [0.68, -0.04, 0], [0.05, 0.06, 0], stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.9)
    h1 = Circle(radius=0.16, stroke_color=color, stroke_width=4.0).move_to([-0.2, 0.18, 0])
    h2 = Circle(radius=0.16, stroke_color=color, stroke_width=4.0).move_to([-0.2, -0.18, 0])
    return VGroup(b1, b2, h1, h2).scale(scale).move_to(center)


def make_ligase_tool(center=ORIGIN, scale=1.0, color=YELLOW):
    """Yellow DNA ligase sealing clamp."""
    arc = Arc(radius=0.38, start_angle=PI * 0.25, angle=PI * 1.5, stroke_color=color, stroke_width=8.0)
    tip1 = Dot([0.38 * np.cos(PI * 0.25), 0.38 * np.sin(PI * 0.25), 0], radius=0.09, color=TEXT)
    tip2 = Dot([0.38 * np.cos(-PI * 0.25), 0.38 * np.sin(-PI * 0.25), 0], radius=0.09, color=TEXT)
    return VGroup(arc, tip1, tip2).scale(scale).move_to(center)


def make_opened_plasmid(center=ORIGIN, radius=1.9, thickness=0.44, gap_rad=1.05):
    """Opened blue circular plasmid with stepped single-stranded sticky-end notches at top."""
    c = np.array(center, dtype=float)
    r_in = radius - thickness / 2
    r_out = radius + thickness / 2
    start = PI / 2 + gap_rad / 2
    span = TAU - gap_rad
    main = AnnularSector(
        inner_radius=r_in, outer_radius=r_out,
        angle=span, start_angle=start, arc_center=c,
        color=BLUE, fill_opacity=0.82, stroke_color=BLUE, stroke_width=2.5,
    )
    over_ang = 0.22
    left_over = AnnularSector(
        inner_radius=r_in, outer_radius=radius,
        angle=over_ang, start_angle=start - over_ang, arc_center=c,
        color=BLUE, fill_opacity=0.92, stroke_color=BLUE, stroke_width=2,
    )
    right_over = AnnularSector(
        inner_radius=radius, outer_radius=r_out,
        angle=over_ang, start_angle=PI / 2 - gap_rad / 2, arc_center=c,
        color=BLUE, fill_opacity=0.92, stroke_color=BLUE, stroke_width=2,
    )
    g = VGroup(main, left_over, right_over)
    g.main = main
    g.left_over = left_over
    g.right_over = right_over
    g.radius = radius
    g.center_pt = c
    return g


def make_recombinant_plasmid(center=ORIGIN, radius=1.9, thickness=0.46, include_tab=True,
                             tab_striped=False, resistance_marker=False, res_highlight=False):
    """Sealed blue plasmid carrying the green insulin gene (+ optional control tab & red resistance marker)."""
    c = np.array(center, dtype=float)
    r_in = radius - thickness / 2
    r_out = radius + thickness / 2

    gene_span = 0.92
    tab_span = 0.34 if include_tab else 0.0
    res_span = 0.45 if resistance_marker else 0.0

    gene_start = PI / 2 - gene_span / 2 - (tab_span / 2 if include_tab else 0)
    tab_start = gene_start + gene_span
    blue_start = tab_start + tab_span
    blue_span = TAU - gene_span - tab_span

    if resistance_marker:
        res_start = -PI / 2 - res_span / 2
        b1_span = res_start - blue_start if res_start > blue_start else (res_start + TAU - blue_start)
        b2_start = res_start + res_span
        b2_span = gene_start - b2_start if gene_start > b2_start else (gene_start + TAU - b2_start)
        blue_part = VGroup(
            AnnularSector(inner_radius=r_in, outer_radius=r_out, angle=b1_span, start_angle=blue_start,
                          arc_center=c, color=BLUE, fill_opacity=0.82, stroke_color=BLUE, stroke_width=2),
            AnnularSector(inner_radius=r_in, outer_radius=r_out, angle=b2_span, start_angle=b2_start,
                          arc_center=c, color=BLUE, fill_opacity=0.82, stroke_color=BLUE, stroke_width=2),
        )
        res_arc = AnnularSector(
            inner_radius=r_in - 0.02, outer_radius=r_out + 0.02, angle=res_span, start_angle=res_start,
            arc_center=c, color=RED, fill_opacity=0.94 if res_highlight else 0.84, stroke_color=RED, stroke_width=3,
        )
    else:
        blue_part = AnnularSector(
            inner_radius=r_in, outer_radius=r_out, angle=blue_span, start_angle=blue_start,
            arc_center=c, color=BLUE, fill_opacity=0.82, stroke_color=BLUE, stroke_width=2,
        )
        res_arc = None

    gene_arc = AnnularSector(
        inner_radius=r_in - 0.02, outer_radius=r_out + 0.02, angle=gene_span, start_angle=gene_start,
        arc_center=c, color=GREEN, fill_opacity=0.88, stroke_color=GREEN, stroke_width=2.5,
    )
    g = VGroup(blue_part, gene_arc)
    g.blue_part = blue_part
    g.gene_arc = gene_arc
    g.res_arc = res_arc
    if res_arc is not None:
        g.add(res_arc)

    g.tab_arc = None
    g.stripes = None
    if include_tab:
        tab_arc = AnnularSector(
            inner_radius=r_in - 0.05, outer_radius=r_out + 0.05, angle=tab_span, start_angle=tab_start,
            arc_center=c, color=GREEN, fill_opacity=0.50 if tab_striped else 0.96,
            stroke_color=TEXT if not tab_striped else RED, stroke_width=2.5,
        )
        g.add(tab_arc)
        g.tab_arc = tab_arc
        if tab_striped:
            stripes = VGroup()
            for frac in (0.2, 0.5, 0.8):
                ang = tab_start + frac * tab_span
                p0 = c + np.array([np.cos(ang), np.sin(ang), 0]) * (r_in - 0.03)
                p1 = c + np.array([np.cos(ang + 0.08), np.sin(ang + 0.08), 0]) * (r_out + 0.03)
                stripes.add(Line(p0, p1, color=RED, stroke_width=4.5))
            g.add(stripes)
            g.stripes = stripes

    g.radius = radius
    g.center_pt = c
    g.gene_mid_angle = gene_start + gene_span / 2
    g.tab_mid_angle = tab_start + tab_span / 2
    return g


def make_plate(center=ORIGIN, radius=2.8, color=RED):
    """Schematic red antibiotic selection plate."""
    c = np.array(center, dtype=float)
    rim = Circle(radius=radius, stroke_color=color, stroke_width=5.0, fill_color=color, fill_opacity=0.22).move_to(c)
    inner = Circle(radius=radius - 0.14, stroke_color=color, stroke_width=2.0, fill_color=color, fill_opacity=0.14).move_to(c)
    return VGroup(rim, inner)


def make_funnel(center=ORIGIN, width=2.7, height=2.9, color=GREY):
    """Schematic purification funnel."""
    c = np.array(center, dtype=float)
    hw, hh = width / 2, height / 2
    pts = [
        [-hw, hh, 0],
        [hw, hh, 0],
        [0.30, -0.1, 0],
        [0.30, -hh, 0],
        [-0.30, -hh, 0],
        [-0.30, -0.1, 0],
    ]
    return Polygon(*pts, stroke_color=TEXT, stroke_width=3.5, fill_color=color, fill_opacity=0.28).move_to(c)


def clean_arrow(start, end, color=TEXT, buff=0.12, stroke_width=3.8):
    """Arrow with fixed tip size and clean clearance."""
    return Arrow(start, end, color=color, buff=buff, stroke_width=stroke_width, max_tip_length_to_length_ratio=0.22)


# ---------------------------------------------------------------------------
# Scene 1: s01_hook
# ---------------------------------------------------------------------------

class S01Hook(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        bact = make_bacterium(center=[0, -0.8, 0], width=7.6, height=3.4)
        bact_lbl = T("bacterium", 30, GREY).next_to(bact, DOWN, buff=0.22)

        slot_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.12, width=3.8, height=0.92, stroke_color=GREEN, stroke_width=4),
            num_dashes=18,
        ).move_to([0, 1.95, 0])
        slot_q = T("human insulin gene ?", 30, GREEN).next_to(slot_box, UP, buff=0.2)
        slot_grp = VGroup(slot_box, slot_q)

        self.play(FadeIn(bact), FadeIn(bact_lbl), run_time=1.3)
        self.play(FadeIn(slot_grp, shift=DOWN * 0.2), run_time=1.2)
        pulse(slot_box, base=4.0, amp=1.8, speed=3.5)
        self.wait(1.2)

        self.at("How can they make")
        q_arrow = DashedLine(slot_box.get_bottom() + DOWN * 0.08, bact.get_top() + UP * 0.08, color=GREEN, stroke_width=3.5)
        q_mark = T("?", 38, GREEN, weight=BOLD).next_to(q_arrow, RIGHT, buff=0.2)
        self.play(Create(q_arrow), FadeIn(q_mark), run_time=1.2)

        self.at("Before engineered microbes")
        slot_box.clear_updaters()
        self.play(FadeOut(slot_grp), FadeOut(q_arrow), FadeOut(q_mark), run_time=0.5)

        bact_right = VGroup(bact, bact_lbl)
        self.play(bact_right.animate.scale(0.84).move_to([2.65, -0.45, 0]), run_time=0.9)

        cow = make_cattle_icon(center=[-4.4, 1.15, 0], scale=1.2)
        pig = make_pig_icon(center=[-4.4, -0.85, 0], scale=1.2)
        animals_lbl = T("from the 1920s", 28, TEAL).move_to([-4.4, 2.5, 0])
        vial_old = make_vial(center=[-1.55, 0.15, 0], height=2.2, liquid_color=TEXT, liquid_frac=0.55)
        vial_old_lbl = T("insulin", 28, TEXT).next_to(vial_old, DOWN, buff=0.2)
        arr_cow = clean_arrow(cow.get_right(), vial_old.get_left() + UP * 0.3, color=GREY, buff=0.14)
        arr_pig = clean_arrow(pig.get_right(), vial_old.get_left() + DOWN * 0.3, color=GREY, buff=0.14)

        self.play(FadeIn(cow, shift=RIGHT * 0.3), FadeIn(pig, shift=RIGHT * 0.3), FadeIn(animals_lbl), run_time=1.1)

        self.at("cattle and pig")
        self.play(Create(arr_cow), Create(arr_pig), FadeIn(vial_old), FadeIn(vial_old_lbl), run_time=1.1)

        self.at("Then bacteria carrying")
        self.play(
            FadeOut(VGroup(cow, pig, animals_lbl, arr_cow, arr_pig, vial_old, vial_old_lbl), shift=LEFT * 1.4),
            run_time=0.45,
        )
        self.play(bact_right.animate.move_to([-2.15, -0.4, 0]), run_time=0.55)
        gene_in = make_gene_block(width=2.2, height=0.72, color=GREEN, ticks=True).move_to([-3.3, -0.2, 0])
        fda_lbl = T("1982 FDA approval", 30, TEAL).next_to(bact, UP, buff=0.35)
        vial_new = make_vial(center=[3.45, -0.3, 0], height=2.7, liquid_color=GREEN, liquid_frac=0.3)
        vial_new_lbl = T("human insulin", 30, GREEN).next_to(vial_new, DOWN, buff=0.22)
        make_arr = clean_arrow(bact.get_right(), vial_new.get_left(), color=GREEN, buff=0.18)

        self.play(FadeIn(gene_in, shift=DOWN * 0.5), FadeIn(fda_lbl), run_time=0.9)

        self.at("making the medicine")
        self.play(Create(make_arr), FadeIn(vial_new, shift=LEFT * 0.4), FadeIn(vial_new_lbl), run_time=0.9)
        self.play(vial_new.liquid.animate.stretch_to_fit_height(1.25, about_edge=DOWN), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 2: s00_title
# ---------------------------------------------------------------------------

class S00Title(TitleCard):
    LESSON = "Engineering Genes"
    TITLE = "How Bacteria Make Human Insulin"


# ---------------------------------------------------------------------------
# Scene 3: s02_instruction
# ---------------------------------------------------------------------------

class S02Instruction(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        gene_full = make_gene_block(width=9.8, height=2.2, color=GREEN, ticks=True).move_to([0, 0.25, 0])
        top_lbl = T("human insulin DNA", 36, GREEN).move_to([0, 2.05, 0])
        self.add(gene_full, top_lbl)
        self.play(LaggedStart(*[Indicate(r, color=YELLOW, scale_factor=1.18) for r in gene_full.rungs], lag_ratio=0.08), run_time=3.6)

        self.at("same genetic code")
        code_lbl = T("same genetic code across living things", 30, TEXT).move_to([0, -1.75, 0])
        self.play(FadeIn(code_lbl, shift=UP * 0.15), run_time=0.8)
        self.play(Indicate(gene_full.shape, color=GREEN, scale_factor=1.02), run_time=1.4)

        self.at("most human genes")
        seg_w = [2.3, 1.5, 2.4, 1.5, 2.3]  # total 10.0
        x_cur = -sum(seg_w) / 2
        segs = VGroup()
        introns = VGroup()
        exons = VGroup()
        for i, w in enumerate(seg_w):
            cx = x_cur + w / 2
            x_cur += w
            is_intron = (i % 2 == 1)
            blk = make_gene_block(
                width=w - 0.04, height=2.2,
                color=GREY if is_intron else GREEN,
                ticks=not is_intron,
                fill_opacity=0.36 if is_intron else 0.40,
            ).move_to([cx, 0.25, 0])
            segs.add(blk)
            if is_intron:
                ilbl = T("intron", 26, GREY).next_to(blk, DOWN, buff=0.25)
                introns.add(VGroup(blk, ilbl))
            else:
                exons.add(blk)

        self.play(FadeOut(code_lbl), FadeOut(gene_full), FadeIn(segs), run_time=0.8)
        self.play(*[FadeIn(ig[1]) for ig in introns], run_time=0.7)

        self.at("human cells cut out")
        self.play(*[FadeOut(ig, shift=DOWN * 0.9) for ig in introns], run_time=1.0)

        self.at("bacteria cannot")
        joined_gene = make_gene_block(width=6.9, height=2.2, color=GREEN, ticks=True).move_to([0.75, 0.25, 0])
        self.play(
            exons[0].animate.move_to([-1.55, 0.25, 0]),
            exons[1].animate.move_to([0.75, 0.25, 0]),
            exons[2].animate.move_to([3.05, 0.25, 0]),
            run_time=0.9,
        )

        self.at("A bacterium can read")
        intron_free_lbl = T("intron-free", 36, GREEN).move_to([0.75, 2.05, 0])
        self.play(
            FadeOut(exons, run_time=0.2),
            FadeIn(joined_gene, run_time=0.3),
            swap(top_lbl, intron_free_lbl, run_time=0.7),
        )
        self.play(LaggedStart(*[Indicate(r, color=YELLOW, scale_factor=1.12) for r in joined_gene.rungs], lag_ratio=0.06), run_time=2.2)

        self.at("bacterial control DNA")
        ctrl_tab = make_control_tab(width=2.1, height=2.2, working=True)
        ctrl_tab.next_to(joined_gene, LEFT, buff=0.9)
        ctrl_lbl = T("bacterial control DNA", 28, GREEN).move_to([-3.4, -1.7, 0])
        self.play(FadeIn(ctrl_tab, shift=LEFT * 0.3), FadeIn(ctrl_lbl), run_time=0.8)
        self.play(ctrl_tab.animate.next_to(joined_gene, LEFT, buff=0), run_time=0.7)

        self.at("The gene is the")
        gene_role = T("gene = instruction", 28, GREEN).move_to([1.6, -1.7, 0])
        self.play(FadeIn(gene_role), run_time=0.7)

        self.at("The control tab helps")
        # Reader height fits comfortably inside 2.2-tall joined_gene
        reader = make_reader(center=[ctrl_tab.get_center()[0], 0.25, 0], scale=1.45)
        reader_lbl = T("bacterial reader", 30, TEXT).move_to([ctrl_tab.get_center()[0], 2.05, 0])
        self.play(FadeOut(intron_free_lbl), FadeIn(reader), FadeIn(reader_lbl), run_time=0.55)
        target_x = joined_gene.get_right()[0] - 0.98
        dx = target_x - reader.get_center()[0]
        self.play(
            VGroup(reader, reader_lbl).animate.shift(RIGHT * dx),
            run_time=2.8, rate_func=smooth,
        )
        self.finish()


# ---------------------------------------------------------------------------
# Scene 4: s03_cut
# ---------------------------------------------------------------------------

class S03Cut(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        gene = make_gene_block(width=5.2, height=1.0, color=GREEN, sticky=False, ticks=True).move_to([0.35, 1.85, 0])
        ctrl = make_control_tab(width=1.4, height=1.0, working=True).next_to(gene, LEFT, buff=0)
        gene_stub_l = make_gene_block(width=0.75, height=1.0, color=GREY, ticks=False, fill_opacity=0.28).next_to(ctrl, LEFT, buff=0)
        gene_stub_r = make_gene_block(width=0.75, height=1.0, color=GREY, ticks=False, fill_opacity=0.28).next_to(gene, RIGHT, buff=0)
        mark_gl = Line(ctrl.get_corner(UL) + UP * 0.1, ctrl.get_corner(DL) + DOWN * 0.1, color=YELLOW, stroke_width=6)
        mark_gr = Line(gene.get_corner(UR) + UP * 0.1, gene.get_corner(DR) + DOWN * 0.1, color=YELLOW, stroke_width=6)

        plasmid_c = np.array([0.0, -1.25, 0.0])
        plasmid_r = 1.85
        plasmid_ring = Annulus(
            inner_radius=plasmid_r - 0.22, outer_radius=plasmid_r + 0.22,
            arc_center=plasmid_c, color=BLUE, fill_opacity=0.82,
        )
        mark_p = Line(
            plasmid_c + np.array([0, plasmid_r - 0.30, 0]),
            plasmid_c + np.array([0, plasmid_r + 0.30, 0]),
            color=YELLOW, stroke_width=6.5,
        )
        gene_lbl = T("human insulin gene", 28, GREEN).move_to([0.0, 3.42, 0])
        plasmid_lbl = T("blue plasmid", 28, BLUE).move_to([3.7, -1.25, 0])

        self.play(
            FadeIn(gene), FadeIn(ctrl), FadeIn(gene_stub_l), FadeIn(gene_stub_r),
            FadeIn(mark_gl), FadeIn(mark_gr), FadeIn(gene_lbl),
            FadeIn(plasmid_ring), FadeIn(mark_p), FadeIn(plasmid_lbl),
            run_time=0.85,
        )

        self.at("A restriction enzyme")
        enzyme = make_enzyme_tool(center=[-5.0, 1.0, 0], scale=1.2)
        enz_lbl = T("restriction enzyme", 26, YELLOW).move_to([-4.6, -0.05, 0])
        self.play(FadeIn(enzyme), FadeIn(enz_lbl), run_time=0.65)
        self.play(FadeOut(enz_lbl), run_time=0.35)
        # Position enzyme cleanly above/left of the cut mark so handles never poke inside gene rectangle
        self.play(enzyme.animate.move_to(mark_gl.get_top() + UP * 0.35 + LEFT * 0.45), run_time=1.3)

        self.at("The yellow tool cuts")
        self.play(enzyme.animate.rotate(-0.25), rate_func=there_and_back, run_time=0.4)
        self.play(FadeOut(gene_stub_l, shift=LEFT * 0.6), FadeOut(mark_gl), run_time=0.5)
        self.play(enzyme.animate.move_to(mark_gr.get_top() + UP * 0.35 + RIGHT * 0.45), run_time=0.85)
        self.play(enzyme.animate.rotate(-0.25), rate_func=there_and_back, run_time=0.4)

        gene_sticky = make_gene_block(
            width=4.9, height=1.0, color=GREEN, left_sticky=False, right_sticky=True, notch=0.46, ticks=True,
        ).move_to([0.35, 1.85, 0])
        ctrl_sticky = make_control_tab(width=1.4, height=1.0, working=True, sticky=True, notch=0.46).next_to(gene_sticky, LEFT, buff=0)
        self.play(
            FadeOut(gene_stub_r, shift=RIGHT * 0.6), FadeOut(mark_gr),
            FadeOut(gene), FadeOut(ctrl),
            FadeIn(gene_sticky), FadeIn(ctrl_sticky),
            run_time=0.6,
        )

        self.at("and a blue plasmid")
        self.play(enzyme.animate.move_to(mark_p.get_center() + UP * 0.35 + LEFT * 0.45), run_time=0.85)
        self.play(enzyme.animate.rotate(-0.25), rate_func=there_and_back, run_time=0.4)
        opened_p = make_opened_plasmid(center=plasmid_c, radius=plasmid_r, thickness=0.44, gap_rad=1.25)
        self.play(FadeOut(plasmid_ring), FadeOut(mark_p), FadeIn(opened_p), run_time=0.65)
        self.play(FadeOut(enzyme, shift=LEFT * 1.2), run_time=0.5)

        self.at("sticky ends")
        # Label sticky ends on the RIGHT pointing clearly at the right sticky overhangs of gene and plasmid
        sticky_lbl = T("sticky ends", 30, YELLOW).move_to([4.15, 0.5, 0])
        arr_p = clean_arrow(sticky_lbl.get_left(), opened_p.right_over.get_center() + RIGHT * 0.1, color=YELLOW, buff=0.14)
        arr_g = clean_arrow(sticky_lbl.get_top(), gene_sticky.get_right() + DOWN * 0.25, color=YELLOW, buff=0.14)
        self.play(FadeIn(sticky_lbl), run_time=0.35)
        self.play(
            Create(arr_p), Create(arr_g),
            opened_p.left_over.animate.set_color(YELLOW),
            opened_p.right_over.animate.set_color(YELLOW),
            run_time=0.65,
        )
        self.play(Indicate(opened_p.right_over, color=YELLOW), run_time=1.0)

        self.at("Their shapes show")
        gene_pair = VGroup(gene_sticky, ctrl_sticky)
        self.play(
            gene_pair.animate.shift(DOWN * 0.25),
            Indicate(opened_p.left_over, color=YELLOW),
            Indicate(opened_p.right_over, color=YELLOW),
            run_time=1.2,
        )

        self.at("The cuts do not add")
        self.play(FadeOut(arr_p), FadeOut(arr_g), FadeOut(sticky_lbl), run_time=0.55)
        self.play(Indicate(gene_pair, color=GREEN, scale_factor=1.03), run_time=1.1)

        self.at("They create pieces")
        self.play(
            opened_p.left_over.animate.set_color(BLUE),
            opened_p.right_over.animate.set_color(BLUE),
            gene_pair.animate.shift(DOWN * 0.25),
            run_time=1.5,
        )
        self.finish()


# ---------------------------------------------------------------------------
# Scene 5: s04_join
# ---------------------------------------------------------------------------

class S04Join(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        plasmid_c = np.array([0.0, -0.55, 0.0])
        plasmid_r = 2.25
        opened_p = make_opened_plasmid(center=plasmid_c, radius=plasmid_r, thickness=0.46, gap_rad=1.26)
        gene_sticky = make_gene_block(
            width=3.3, height=0.72, color=GREEN, left_sticky=False, right_sticky=True, notch=0.36, ticks=True,
        ).move_to([0.4, 2.35, 0])
        ctrl_sticky = make_control_tab(width=1.0, height=0.72, working=True, sticky=True, notch=0.36).next_to(gene_sticky, LEFT, buff=0)
        insert_grp = VGroup(gene_sticky, ctrl_sticky)
        self.add(opened_p, insert_grp)

        self.at("The matching ends meet")
        recomb = make_recombinant_plasmid(center=plasmid_c, radius=plasmid_r, thickness=0.46, include_tab=True)
        ang_r = PI / 2 - 0.92 / 2 - 0.34 / 2
        ang_l = ang_r + 0.92 + 0.34
        seam_l = Line(
            plasmid_c + np.array([np.cos(ang_l), np.sin(ang_l), 0]) * (plasmid_r - 0.28),
            plasmid_c + np.array([np.cos(ang_l), np.sin(ang_l), 0]) * (plasmid_r + 0.28),
            color=YELLOW, stroke_width=6,
        )
        seam_r = Line(
            plasmid_c + np.array([np.cos(ang_r), np.sin(ang_r), 0]) * (plasmid_r - 0.28),
            plasmid_c + np.array([np.cos(ang_r), np.sin(ang_r), 0]) * (plasmid_r + 0.28),
            color=YELLOW, stroke_width=6,
        )
        # Smooth 3.0s descent into the opened plasmid gap (eliminates long pre-ligase pause)
        self.play(insert_grp.animate.move_to(plasmid_c + UP * (plasmid_r + 0.20)).scale(0.86), run_time=2.6, rate_func=smooth)
        self.play(
            FadeOut(opened_p), FadeOut(insert_grp),
            FadeIn(recomb), FadeIn(seam_l), FadeIn(seam_r),
            run_time=0.65,
        )

        self.at("seals the gaps")
        ligase = make_ligase_tool(center=seam_l.get_center() + UP * 0.6, scale=1.15)
        lig_lbl = T("DNA ligase", 28, YELLOW).next_to(ligase, UP, buff=0.18)
        self.play(FadeIn(ligase), FadeIn(lig_lbl), run_time=0.45)
        self.play(ligase.animate.move_to(seam_l.get_center()), run_time=0.45)
        self.play(FadeOut(seam_l), run_time=0.3)
        self.play(ligase.animate.move_to(seam_r.get_center()), FadeOut(lig_lbl), run_time=0.65)
        self.play(FadeOut(seam_r), run_time=0.3)
        self.play(FadeOut(ligase), run_time=0.35)

        self.at("The blue loop now carries")
        self.play(recomb.animate.move_to([0, 0.35, 0]).scale(1.12), run_time=0.9)
        self.play(Rotate(recomb, angle=PI * 0.45, about_point=recomb.get_center()), run_time=2.2, rate_func=linear)

        self.at("This is recombinant")
        rec_lbl = T("recombinant DNA", 36, TEXT).move_to([0, -2.85, 0])
        self.play(
            Rotate(recomb, angle=PI * 0.45, about_point=recomb.get_center()),
            FadeIn(rec_lbl, shift=UP * 0.15),
            run_time=2.0, rate_func=linear,
        )

        self.at("DNA from different sources")
        self.play(
            Rotate(recomb, angle=PI * 0.70, about_point=recomb.get_center()),
            run_time=3.2, rate_func=linear,
        )

        self.at("The plasmid can copy")
        self.play(FadeOut(rec_lbl), run_time=0.3)
        self.play(recomb.animate.scale(0.62).move_to([-3.45, 0.15, 0]), run_time=0.7)
        bact = make_bacterium(center=[2.3, 0.15, 0], width=5.8, height=3.2, chromosome=True)
        chrom_lbl = T("main chromosome", 28, GREY).next_to(bact, DOWN, buff=0.24)
        p_copy1 = make_recombinant_plasmid(center=[0.85, 0.15, 0], radius=0.48, thickness=0.14, include_tab=True)
        p_copy2 = make_recombinant_plasmid(center=[0.85, 0.15, 0], radius=0.48, thickness=0.14, include_tab=True)
        copy_lbl = T("plasmid copies separately", 28, BLUE).move_to([2.3, 2.4, 0])
        self.play(FadeIn(bact), FadeIn(chrom_lbl), FadeIn(p_copy1), FadeIn(copy_lbl), run_time=0.8)
        self.play(
            p_copy1.animate.move_to([0.85, 0.75, 0]),
            FadeIn(p_copy2),
            p_copy2.animate.move_to([0.95, -0.45, 0]),
            Rotate(recomb, angle=PI * 0.5, about_point=recomb.get_center()),
            run_time=2.6,
        )
        self.finish()


# ---------------------------------------------------------------------------
# Scene 6 & 7: s05_predict and s06_pause (shared world builder)
# ---------------------------------------------------------------------------

def _predict_world():
    """Shared picture for S05Predict end state and S06Pause backdrop."""
    plasmid = make_recombinant_plasmid(
        center=[0.3, -0.55, 0], radius=2.32, thickness=0.48,
        include_tab=True, tab_striped=True,
    )
    ang_stop = plasmid.tab_mid_angle + 0.58
    r_pos = plasmid.center_pt + np.array([np.cos(ang_stop), np.sin(ang_stop), 0]) * (plasmid.radius + 0.38)
    reader = make_reader(center=r_pos, scale=1.15).rotate(ang_stop - PI / 2)
    return plasmid, reader


class S05Predict(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        plasmid_clean = make_recombinant_plasmid(
            center=[0.3, -0.55, 0], radius=2.32, thickness=0.48,
            include_tab=True, tab_striped=False,
        )
        self.play(FadeIn(plasmid_clean), run_time=0.9)
        self.play(Rotate(plasmid_clean, angle=0.35, about_point=plasmid_clean.get_center()), run_time=1.6)

        self.at("Predict this")
        self.play(Rotate(plasmid_clean, angle=-0.35, about_point=plasmid_clean.get_center()), run_time=1.4)

        self.at("carries insulin DNA")
        gene_lbl = T("insulin DNA", 30, GREEN).move_to([4.05, 1.55, 0])
        self.play(FadeIn(gene_lbl), run_time=0.7)

        self.at("control tab does not work")
        plasmid_striped, reader = _predict_world()
        tab_lbl = T("control tab blocked", 28, RED).move_to([-4.2, -1.75, 0])
        self.play(
            FadeOut(gene_lbl),
            FadeIn(plasmid_striped.stripes),
            plasmid_clean.tab_arc.animate.set_fill(opacity=0.45).set_stroke(RED),
            FadeIn(tab_lbl),
            run_time=0.9,
        )
        reader_start = reader.get_center() + LEFT * 1.5 + UP * 0.45
        reader_stop = reader.get_center().copy()
        reader.move_to(reader_start)
        self.play(FadeIn(reader), run_time=0.4)
        self.play(reader.animate.move_to(reader_stop), run_time=1.4, rate_func=smooth)

        self.at("Will the cell make")
        q = question_card("Will the cell make insulin?", y=3.05, size=34)
        self.play(FadeOut(tab_lbl), FadeIn(q), run_time=0.9)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Will the cell make insulin?"
    CARD = {"y": 3.05, "size": 34}
    RING_AT = (-5.9, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        plasmid, reader = _predict_world()
        pulse(plasmid.tab_arc, base=2.8, amp=1.8, speed=3.0)
        return VGroup(plasmid, reader, scope_tag("schematic"))


# ---------------------------------------------------------------------------
# Scene 8: s07_reveal
# ---------------------------------------------------------------------------

class S07Reveal(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        plasmid, reader = _predict_world()
        plasmid_grp = VGroup(plasmid, reader)
        q_old = question_card("Will the cell make insulin?", y=3.05, size=34)
        self.add(plasmid, reader, q_old)

        ans_no = T("No — blocked at the control tab", 32, RED).move_to([0, 3.05, 0])
        self.play(swap(q_old, ans_no, run_time=0.5))

        self.at("Carrying a gene is not enough")
        self.play(plasmid_grp.animate.scale(0.9).move_to([-2.4, -0.35, 0]), run_time=1.8)
        plasmid.center_pt = plasmid.get_center()

        self.at("The cell must recognize")
        self.play(FadeOut(ans_no), run_time=0.5)
        stop_bar = Line(
            plasmid.tab_arc.get_left() + UP * 0.25 + LEFT * 0.1,
            plasmid.tab_arc.get_left() + DOWN * 0.25 + LEFT * 0.1,
            color=RED, stroke_width=6.5,
        )
        ctrl_need = T("needs bacterial control DNA", 28, RED).move_to([-2.4, 2.95, 0])
        self.play(Create(stop_bar), FadeIn(ctrl_need), run_time=1.2)
        self.play(
            reader.animate.shift(LEFT * 0.25),
            rate_func=there_and_back, run_time=1.8,
        )
        self.play(FadeOut(stop_bar), FadeOut(ctrl_need), run_time=0.8)

        self.at("Replace the tab")
        old_tab = VGroup(plasmid.tab_arc, plasmid.stripes)
        new_tab = plasmid.tab_arc.copy().set_fill(GREEN, opacity=0.96).set_stroke(TEXT, width=2.5)
        new_tab_start = new_tab.get_center() + UP * 1.4 + LEFT * 0.6
        new_tab_end = new_tab.get_center().copy()
        new_tab.move_to(new_tab_start)
        tab_lbl = T("working bacterial control tab", 28, GREEN).move_to([-2.4, 2.95, 0])

        self.play(FadeOut(old_tab, shift=UP * 1.1 + LEFT * 0.4), run_time=0.6)
        self.play(FadeIn(new_tab), new_tab.animate.move_to(new_tab_end), run_time=0.9)
        self.play(FadeIn(tab_lbl), run_time=0.4)

        self.at("Now the reader moves")
        r_center = plasmid.get_center()
        self.play(Rotate(reader, angle=-1.35, about_point=r_center), run_time=1.6, rate_func=smooth)

        self.at("green insulin product block")
        vial = make_vial(center=[4.3, -0.35, 0], height=2.8, liquid_color=GREEN, liquid_frac=0.22)
        vial_lbl = T("insulin product", 30, GREEN).next_to(vial, DOWN, buff=0.22)
        path_start = plasmid.gene_arc.get_right() + RIGHT * 0.18
        path_end = vial.get_left() + LEFT * 0.18 + UP * 0.4
        dotted = DashedLine(path_start, path_end, color=GREEN, stroke_width=4.5, dash_length=0.16)
        prod1 = RoundedRectangle(corner_radius=0.08, width=0.82, height=0.54, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.86).move_to(path_start)

        self.play(FadeIn(vial), FadeIn(vial_lbl), Create(dotted), FadeIn(prod1), run_time=0.75)
        self.play(prod1.animate.move_to(path_end), run_time=1.0, rate_func=smooth)
        self.play(FadeOut(prod1), vial.liquid.animate.stretch_to_fit_height(0.8, about_edge=DOWN), run_time=0.5)

        self.at("The instruction was present")
        prod2 = RoundedRectangle(corner_radius=0.08, width=0.82, height=0.54, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.86).move_to(path_start)
        prod3 = prod2.copy()
        self.play(FadeIn(prod2), run_time=0.45)
        self.play(prod2.animate.move_to(path_end), run_time=1.4, rate_func=smooth)
        self.play(FadeOut(prod2), vial.liquid.animate.stretch_to_fit_height(1.15, about_edge=DOWN), run_time=0.55)
        self.play(FadeIn(prod3), run_time=0.45)
        self.play(prod3.animate.move_to(path_end), run_time=1.4, rate_func=smooth)
        self.play(FadeOut(prod3), vial.liquid.animate.stretch_to_fit_height(1.45, about_edge=DOWN), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 9: s08_select
# ---------------------------------------------------------------------------

class S08Select(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        c_pos = [[-4.35, 2.0, 0], [-4.35, 0.0, 0], [-4.35, -2.0, 0]]
        cells = VGroup(*[make_bacterium(center=p, width=2.9, height=1.28, chromosome=True) for p in c_pos])
        plasmid = make_recombinant_plasmid(
            center=[0.5, 0.0, 0], radius=1.32, thickness=0.28,
            include_tab=True, resistance_marker=True,
        )
        self.play(FadeIn(cells), FadeIn(plasmid), run_time=0.85)

        target_p = np.array([-4.95, 0.0, 0])
        self.play(plasmid.animate.scale(0.28).move_to(target_p), run_time=1.1)
        carrier = VGroup(cells[1], plasmid)

        self.at("carries an")
        res_callout = make_recombinant_plasmid(
            center=[0.8, 0.15, 0], radius=1.45, thickness=0.32,
            include_tab=True, resistance_marker=True, res_highlight=True,
        )
        res_lbl = T("antibiotic-resistance gene", 28, RED).next_to(res_callout, DOWN, buff=0.35)
        ins_lbl = T("insulin gene", 28, GREEN).next_to(res_callout, UP, buff=0.35)
        self.play(FadeIn(res_callout), FadeIn(res_lbl), FadeIn(ins_lbl), run_time=0.9)

        self.at("selection step")
        self.play(FadeOut(res_callout), FadeOut(res_lbl), FadeOut(ins_lbl), run_time=0.65)

        self.at("On antibiotic")
        plate = make_plate(center=[2.55, -0.1, 0], radius=2.8, color=RED)
        plate_lbl = T("antibiotic plate", 30, RED).next_to(plate, UP, buff=0.22)
        self.play(FadeIn(plate), FadeIn(plate_lbl), run_time=0.75)

        self.play(
            cells[0].animate.scale(0.54).move_to([1.32, 0.95, 0]),
            carrier.animate.scale(0.60).move_to([3.3, 0.0, 0]),
            cells[2].animate.scale(0.54).move_to([1.32, -1.05, 0]),
            run_time=1.0,
        )

        self.at("cells without a plasmid")
        self.play(
            cells[0].body.animate.set_fill(opacity=0).set_stroke(opacity=0.28),
            cells[0].inner.animate.set_stroke(opacity=0.2),
            cells[0].chromosome.animate.set_stroke(opacity=0.2),
            cells[2].body.animate.set_fill(opacity=0).set_stroke(opacity=0.28),
            cells[2].inner.animate.set_stroke(opacity=0.2),
            cells[2].chromosome.animate.set_stroke(opacity=0.2),
            run_time=1.0,
        )

        self.at("Surviving colonies")
        colony_offsets = [
            [2.85, 0.65, 0], [4.15, 0.65, 0],
            [2.85, -0.55, 0], [4.15, -0.55, 0],
            [3.50, 1.35, 0], [3.50, -1.25, 0],
            [2.40, 0.05, 0], [4.55, 0.05, 0],
        ]
        daughters = VGroup()
        for pos in colony_offsets[1:]:
            cb = make_bacterium(center=pos, width=1.28, height=0.58, chromosome=False)
            cp = make_recombinant_plasmid(
                center=np.array(pos) + LEFT * 0.22, radius=0.16, thickness=0.055,
                include_tab=True, resistance_marker=True,
            )
            daughters.add(VGroup(cb, cp))

        self.play(carrier.animate.scale(0.75).move_to(colony_offsets[0]), run_time=0.6)
        self.play(FadeIn(daughters[0], shift=RIGHT * 0.3), run_time=0.65)
        self.play(FadeIn(daughters[1:3], shift=DOWN * 0.3), run_time=0.75)
        col_lbl = T("surviving colony", 30, TEXT).next_to(plate, DOWN, buff=0.22)
        self.play(FadeIn(daughters[3:], lag_ratio=0.12), FadeIn(col_lbl), run_time=1.1)

        self.at("The resistance marker")
        note_box = make_recombinant_plasmid(
            center=[-3.55, -0.1, 0], radius=1.45, thickness=0.34,
            include_tab=True, resistance_marker=True, res_highlight=True,
        )
        m_lbl = T("resistance marker", 28, RED).next_to(note_box, DOWN, buff=0.28)
        self.play(FadeIn(note_box), FadeIn(m_lbl), run_time=0.7)
        self.play(Indicate(note_box.res_arc, color=RED, scale_factor=1.18), run_time=1.3)

        self.at("Insulin itself does not")
        ins_note = T("insulin does not give resistance", 26, GREEN).next_to(note_box, UP, buff=0.28)
        self.play(FadeIn(ins_note), run_time=0.45)
        self.play(Indicate(note_box.gene_arc, color=GREEN, scale_factor=1.15), run_time=1.8)
        self.play(Indicate(note_box.res_arc, color=RED, scale_factor=1.15), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 10: s09_copy
# ---------------------------------------------------------------------------

class S09Copy(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        c0 = make_bacterium(center=[-4.0, 0.0, 0], width=3.3, height=1.45, chromosome=True)
        p0 = make_recombinant_plasmid(center=[-4.5, 0.0, 0], radius=0.34, thickness=0.10, include_tab=True)
        self.play(FadeIn(c0), FadeIn(p0), run_time=0.65)

        self.at("they copy the plasmid")
        p0_copy = make_recombinant_plasmid(center=[-4.5, 0.0, 0], radius=0.34, thickness=0.10, include_tab=True)
        self.play(p0.animate.shift(LEFT * 0.42), FadeIn(p0_copy), p0_copy.animate.shift(RIGHT * 0.42), run_time=0.8)

        d2_centers = [[-4.0, 1.3, 0], [-4.0, -1.3, 0]]
        d2 = VGroup(*[
            VGroup(
                make_bacterium(center=pos, width=2.9, height=1.20, chromosome=True),
                make_recombinant_plasmid(center=np.array(pos) + LEFT * 0.5, radius=0.28, thickness=0.085, include_tab=True),
            )
            for pos in d2_centers
        ])
        self.play(FadeOut(c0), FadeOut(p0), FadeOut(p0_copy), FadeIn(d2[0], shift=UP * 0.5), FadeIn(d2[1], shift=DOWN * 0.5), run_time=0.9)

        d4_centers = [[-4.15, 2.25, 0], [-4.15, 0.75, 0], [-4.15, -0.75, 0], [-4.15, -2.25, 0]]
        d4 = VGroup(*[
            VGroup(
                make_bacterium(center=pos, width=2.7, height=1.08, chromosome=False),
                make_recombinant_plasmid(center=np.array(pos) + LEFT * 0.48, radius=0.25, thickness=0.08, include_tab=True),
                make_recombinant_plasmid(center=np.array(pos) + RIGHT * 0.40, radius=0.25, thickness=0.08, include_tab=True),
            )
            for pos in d4_centers
        ])
        self.play(FadeOut(d2), FadeIn(d4, lag_ratio=0.12), run_time=0.95)

        self.at("If the gene is switched on")
        cond_lbl = T("if switched on", 32, GREEN).move_to([0.3, 2.95, 0])
        self.play(FadeIn(cond_lbl), run_time=0.6)

        blocks = VGroup(*[
            RoundedRectangle(corner_radius=0.07, width=0.48, height=0.32, stroke_color=GREEN, stroke_width=2.8, fill_color=GREEN, fill_opacity=0.88).move_to(np.array(pos) + RIGHT * 1.55)
            for pos in d4_centers
        ])
        self.play(FadeIn(blocks, shift=RIGHT * 0.3), run_time=0.8)

        self.at("Scientists then purify")
        funnel = make_funnel(center=[0.3, 0.0, 0], width=2.7, height=2.9)
        fun_lbl = T("purify & process", 28, TEXT).next_to(funnel, DOWN, buff=0.24)
        vial1 = make_vial(center=[3.35, -0.25, 0], height=2.5, liquid_color=GREEN, liquid_frac=0.2)
        vial2 = make_vial(center=[5.05, -0.25, 0], height=2.5, liquid_color=GREEN, liquid_frac=0.2)
        vials_lbl = T("insulin medicine", 30, GREEN).move_to([4.2, -2.0, 0])

        cap1, cap2 = vial1[3], vial2[3]
        vial1_open = VGroup(vial1.liquid, vial1.body, vial1[2])
        vial2_open = VGroup(vial2.liquid, vial2.body, vial2[2])

        self.play(FadeIn(funnel), FadeIn(fun_lbl), FadeIn(vial1_open), FadeIn(vial2_open), FadeIn(vials_lbl), run_time=0.85)

        above_funnel = funnel.get_top() + UP * 0.25
        top_target = funnel.get_top() + DOWN * 0.35
        stem_target = funnel.get_bottom() + UP * 0.24
        self.play(*[b.animate.move_to([-1.85 + i * 0.22, 1.80, 0]) for i, b in enumerate(blocks)], run_time=0.55)
        self.play(*[b.animate.move_to(above_funnel + RIGHT * (i - 1.5) * 0.4) for i, b in enumerate(blocks)], run_time=0.45)
        self.play(*[b.animate.move_to(top_target + RIGHT * (i - 1.5) * 0.4) for i, b in enumerate(blocks)], run_time=0.45)
        self.play(*[b.animate.move_to(stem_target) for b in blocks], run_time=0.55)
        self.play(
            *[b.animate(path_arc=1.2).move_to([2.10, 1.25, 0]) for b in blocks],
            run_time=0.65,
        )
        self.play(
            blocks[0].animate.move_to([3.35, 1.15, 0]),
            blocks[1].animate.move_to([3.35, 1.15, 0]),
            blocks[2].animate.move_to([5.05, 1.15, 0]),
            blocks[3].animate.move_to([5.05, 1.15, 0]),
            run_time=0.55,
        )
        self.play(
            FadeOut(blocks[:2], target_position=vial1.body.get_center()),
            FadeOut(blocks[2:], target_position=vial2.body.get_center()),
            vial1.liquid.animate.stretch_to_fit_height(1.0, about_edge=DOWN),
            vial2.liquid.animate.stretch_to_fit_height(1.0, about_edge=DOWN),
            run_time=0.45,
        )
        self.play(
            FadeIn(cap1, shift=DOWN * 0.2),
            FadeIn(cap2, shift=DOWN * 0.2),
            run_time=0.30,
        )

        self.at("Each daughter can inherit")
        # Visible plasmid inheritance highlight + second product stream into vials (eliminates 9s freeze)
        rings = VGroup(*[
            Circle(radius=0.36, color=YELLOW, stroke_width=4.5).move_to(cell[1].get_center())
            for cell in d4
        ])
        rings2 = VGroup(*[
            Circle(radius=0.36, color=YELLOW, stroke_width=4.5).move_to(cell[2].get_center())
            for cell in d4
        ])
        self.play(Create(rings, lag_ratio=0.2), run_time=1.8)
        self.play(FadeOut(rings), Create(rings2, lag_ratio=0.2), run_time=1.8)

        self.at("the colony keeps")
        keep_lbl = T("colony keeps instruction", 26, BLUE).move_to([-4.15, -3.12, 0])
        self.play(FadeIn(keep_lbl), FadeOut(rings2), run_time=0.45)
        self.play(
            vial1.liquid.animate.stretch_to_fit_height(1.3, about_edge=DOWN),
            vial2.liquid.animate.stretch_to_fit_height(1.3, about_edge=DOWN),
            run_time=1.4,
        )
        self.finish()


# ---------------------------------------------------------------------------
# Scene 11: s10_rule
# ---------------------------------------------------------------------------

class S10Rule(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        xs = [-5.25, -3.15, -1.05, 1.05, 3.15]
        y0 = 0.70

        ic_cut = make_enzyme_tool(center=[xs[0], y0, 0], scale=1.22)
        ic_join = make_recombinant_plasmid(center=[xs[1], y0, 0], radius=0.72, thickness=0.20, include_tab=True)
        ic_carry = VGroup(
            make_bacterium(center=[xs[2], y0, 0], width=1.60, height=0.88, chromosome=False),
            make_recombinant_plasmid(center=[xs[2], y0, 0], radius=0.25, thickness=0.075, include_tab=True),
        )
        ic_select = VGroup(
            make_plate(center=[xs[3], y0, 0], radius=0.76, color=RED),
            make_bacterium(center=[xs[3], y0, 0], width=0.84, height=0.42, chromosome=False),
        )
        ic_read = make_vial(center=[xs[4], y0, 0], height=1.65, liquid_color=GREEN, liquid_frac=0.65)

        icons = [ic_cut, ic_join, ic_carry, ic_select, ic_read]
        names = [("cut", YELLOW), ("join", BLUE), ("carry", GREY), ("select", RED), ("read", GREEN)]
        labels = [T(txt, 30, col).move_to([x, y0 - 1.32, 0]) for x, (txt, col) in zip(xs, names)]
        arrows = [
            clean_arrow([xs[i] + 0.84, y0, 0], [xs[i + 1] - 0.84, y0, 0], color=TEXT, buff=0.06, stroke_width=3.5)
            for i in range(4)
        ]

        self.at("The moving chain is cut")
        self.play(FadeIn(icons[0]), FadeIn(labels[0]), run_time=0.4)

        self.at("Join")
        self.play(Create(arrows[0]), FadeIn(icons[1]), FadeIn(labels[1]), run_time=0.3)

        self.at("carry")
        self.play(Create(arrows[1]), FadeIn(icons[2]), FadeIn(labels[2]), run_time=0.3)

        self.at("select")
        self.play(Create(arrows[2]), FadeIn(icons[3]), FadeIn(labels[3]), run_time=0.3)

        self.at("and read")
        self.play(Create(arrows[3]), FadeIn(icons[4]), FadeIn(labels[4]), run_time=0.35)

        self.at("Each step supports")
        q_x = 5.25
        arr_q = clean_arrow([xs[4] + 0.60, y0, 0], [q_x - 0.68, y0, 0], color=TEAL, buff=0.06, stroke_width=4.0)
        q_ring = Circle(radius=0.70, stroke_color=TEAL, stroke_width=4.5, fill_color=TEAL, fill_opacity=0.24).move_to([q_x, y0, 0])
        q_mark = T("?", 60, TEAL, weight=BOLD).move_to([q_x, y0, 0])
        q_lbl = T("test", 30, TEAL).move_to([q_x, y0 - 1.32, 0])

        self.play(
            LaggedStart(*[arr.animate.set_color(GOLD) for arr in arrows], lag_ratio=0.35),
            run_time=2.2,
        )

        self.at("none guarantees")
        self.play(Create(arr_q), FadeIn(q_ring), FadeIn(q_mark), FadeIn(q_lbl), run_time=1.0)
        self.play(Indicate(q_ring, color=TEAL, scale_factor=1.15), run_time=1.4)

        self.at("Engineering changes")
        cap = caption("Engineering changes a cell's DNA;\ntest the effects, judge each use separately.", size=26)
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.9)

        self.at("Test the effects")
        self.play(Indicate(VGroup(q_ring, q_mark), color=TEAL, scale_factor=1.12), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------
# Scene 12: s11_end
# ---------------------------------------------------------------------------

class S11End(EndCard):
    LINE = "Engineering changes a cell's DNA; test the effects, judge each use separately."
