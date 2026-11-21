"""
A Borrowed Kinase, Straight to DNA — Cytokine Receptors and JAK-STAT

COLOUR MAP (one colour per concept across the whole film):
    CYTOKINE  = "#F59E0B"   # warm amber: interferon / cytokine ligand
    RECEPTOR  = "#3B82F6"   # slate blue: single-pass cytokine receptor chains & tails
    JAK_KIN   = "#EF4444"   # coral red: JAK working tyrosine kinase lobe
    JAK_PSEU  = "#FB7185"   # muted rose: JAK pseudokinase (inactive look-alike) lobe
    PHOSPHATE = "#FACC15"   # bright gold: phosphate ('P') tags & active phospho-glow
    STAT_COL  = "#10B981"   # emerald teal: STAT transcription factor & SH2 pocket
    DNA_COL   = "#A78BFA"   # soft violet: DNA double helix & target gene
    IRF9_COL  = "#60A5FA"   # soft blue: IRF9 partner protein in type I interferon complex
    TEXT / GREY / BG        # house typography and structural membrane/nuclear lines

CARRIED WORLD:
    A 16:9 cross-section of a human cell (extracellular space at top, horizontal plasma
    membrane, open cytoplasm, curved nuclear envelope with central pore, violet DNA
    double helix at bottom), zoomed onto the plasma membrane in s02-s07 and pulled back
    to follow STAT into the nucleus in s08-s10.

SCENE ACTION PLAN (what changes on screen and what drives it):
    s00_title             Standard TitleCard ("A Borrowed Kinase, Straight to DNA").
    s01_hook              Amber interferon drifts to receptors; clock arc ticks "Minutes"
                          while gene lights up; crossed-out new-protein badge; waiting
                          cytoplasmic silhouettes appear and bob.
    s02_borrowed_jak      Zoomed membrane; cytokine carries message across extracellular
                          space; two separated receptor chains with breathing JAKs.
    s03_pair_and_activate Pseudokinase presses against kinase; cytokine draws chains together;
                          JAKs reach across, flash 'P' tags onto each other, and glow on.
    s04_dock_stat         Active JAKs add 'P' landing pads to tail side-pegs; two STATs
                          drift up and cradle the tail 'P' pads inside their SH2 pockets.
    s05_tag_stat_question Active JAKs transfer 'P' to each STAT's tail peg; SH2 and 'P'
                          highlighted; STATs loosen and bob as question card appears.
    s06_predict_pause     PredictPause (4.5 s): tagged STATs bob gently under question.
    s07_two_grips         STATs detach from tails and lock head-to-head into a two-grip
                          reciprocal clamp; reversible docking and "1 -> 2 grips" shown.
    s08_to_dna            Ghosted loose pair snaps into tight clamp, glides through nuclear
                          pore onto DNA, sweeps gene-ON arrow; IRF9 inset at lower right.
    s09_direct_path       Full cell pullback; glowing direct relay wave travels receptor->DNA
                          alongside a crossed-out schematic multi-step cascade.
    s10_scope_close       Full cell with golden signal pulse flowing to gene, clock ticking
                          "Minutes", and tidy scope tags ("Class I & II cytokine receptors").
    s11_end               Standard EndCard.
"""

import numpy as np
from bp_parts import *

CYTOKINE = "#F59E0B"
RECEPTOR = "#3B82F6"
JAK_KIN = "#EF4444"
JAK_PSEU = "#FB7185"
PHOSPHATE = "#FACC15"
STAT_COL = "#10B981"
DNA_COL = "#A78BFA"
IRF9_COL = "#60A5FA"


# ------------------------------------------------------------------ shared builders
def build_membrane(y=1.65, x_span=6.5, thickness=0.32):
    """Horizontal plasma membrane bilayer with crisp lipid-bilayer contrast."""
    top = Line([-x_span, y + thickness / 2, 0], [x_span, y + thickness / 2, 0], color=GREY, stroke_width=4.5)
    bot = Line([-x_span, y - thickness / 2, 0], [x_span, y - thickness / 2, 0], color=GREY, stroke_width=4.5)
    band = Polygon(
        [-x_span, y + thickness / 2, 0],
        [x_span, y + thickness / 2, 0],
        [x_span, y - thickness / 2, 0],
        [-x_span, y - thickness / 2, 0],
        stroke_width=0,
        fill_color=GREY,
        fill_opacity=0.34,
    )
    band.set_z_index(-2)
    return VGroup(band, top, bot)


def build_nuclear_envelope(y=-1.20, x_span=6.5, pore_half=1.02, pore_x=0.0):
    """Gently curved nuclear envelope with a nuclear pore opening centered at pore_x."""
    xs_l = np.linspace(-x_span, pore_x - pore_half, 36)
    xs_r = np.linspace(pore_x + pore_half, x_span, 36)
    curve = lambda x: y - 0.012 * (x ** 2)
    pts_l = [np.array([x, curve(x), 0.0]) for x in xs_l]
    pts_r = [np.array([x, curve(x), 0.0]) for x in xs_r]
    arc_l = VMobject(stroke_color=GREY, stroke_width=5).set_points_as_corners(pts_l)
    arc_r = VMobject(stroke_color=GREY, stroke_width=5).set_points_as_corners(pts_r)
    lip_l = Dot([pore_x - pore_half, curve(pore_x - pore_half), 0], radius=0.07, color=GREY)
    lip_r = Dot([pore_x + pore_half, curve(pore_x + pore_half), 0], radius=0.07, color=GREY)
    return VGroup(arc_l, arc_r, lip_l, lip_r)


def build_dna(center=(0.0, -2.55, 0.0), width=10.8, amp=0.26, cycles=3.2, color=DNA_COL):
    """Schematic DNA double helix (two intertwined sinusoids + base-pair rungs)."""
    cx, cy, _ = center
    n = 140
    xs = np.linspace(cx - width / 2, cx + width / 2, n)
    phase = (xs - (cx - width / 2)) / width * cycles * TAU
    y1 = cy + amp * np.sin(phase)
    y2 = cy - amp * np.sin(phase)
    s1 = VMobject(stroke_color=color, stroke_width=5.5).set_points_as_corners(
        [np.array([x, y, 0.0]) for x, y in zip(xs, y1)]
    )
    s2 = VMobject(stroke_color=color, stroke_width=5.5, stroke_opacity=0.82).set_points_as_corners(
        [np.array([x, y, 0.0]) for x, y in zip(xs, y2)]
    )
    rungs = VGroup()
    for i in range(6, n - 4, 8):
        rungs.add(Line([xs[i], y1[i], 0], [xs[i], y2[i], 0], color=color, stroke_width=3, stroke_opacity=0.60))
    return VGroup(rungs, s1, s2)


def build_phosphate(at=ORIGIN, radius=0.27, font_size=24):
    """Gold phosphate 'P' badge sized cleanly so letters never overflow or crowd the border."""
    c = Circle(radius=radius, stroke_color=PHOSPHATE, stroke_width=2.5, fill_color=PHOSPHATE, fill_opacity=0.96)
    p = T("P", size=font_size, color=BG, weight=BOLD).move_to(c)
    g = VGroup(c, p).move_to(at)
    g.circle, g.letter = c, p
    return g


def build_cytokine(at=ORIGIN, rx=0.72, ry=0.42):
    """Warm amber cytokine (interferon) oval."""
    outer = Ellipse(width=2 * rx, height=2 * ry, stroke_color=CYTOKINE, stroke_width=3.5,
                    fill_color=CYTOKINE, fill_opacity=0.48).move_to(at)
    core = Ellipse(width=1.25 * rx, height=1.25 * ry, stroke_width=0,
                   fill_color=CYTOKINE, fill_opacity=0.72).move_to(at)
    return VGroup(outer, core)


def build_receptor_chain(x, mem_y=1.65, top_y=2.72, tail_y=-0.95, side=-1, has_side_peg=True):
    """Single-pass receptor chain: extracellular binding cup, transmembrane rod, flexible intracellular tail.
    side=-1 for left chain, side=+1 for right chain.
    The tyrosine side-peg juts outward to x + 0.50*side so the 'P' badge never touches the tail or notch.
    """
    ext_rod = RoundedRectangle(
        corner_radius=0.12, width=0.40, height=top_y - (mem_y - 0.42),
        stroke_color=RECEPTOR, stroke_width=3.5, fill_color=RECEPTOR, fill_opacity=0.52,
    ).move_to([x, (top_y + mem_y - 0.42) / 2, 0])
    cup = Polygon(
        [x - 0.18 * side, top_y - 0.05, 0],
        [x + 0.20 * side, top_y - 0.05, 0],
        [x + 0.30 * side, top_y + 0.20, 0],
        [x - 0.06 * side, top_y + 0.20, 0],
        stroke_color=RECEPTOR, stroke_width=3, fill_color=RECEPTOR, fill_opacity=0.45,
    )
    pts = [
        np.array([x, mem_y - 0.38, 0.0]),
        np.array([x + 0.05 * side, (mem_y - 0.38 + tail_y) / 2 + 0.15, 0.0]),
        np.array([x + 0.02 * side, tail_y, 0.0]),
    ]
    tail = VMobject(stroke_color=RECEPTOR, stroke_width=9).set_points_smoothly(pts)
    ty_y = tail_y + 0.28
    ty_stub_x = x + 0.04 * side
    peg_center = np.array([x + 0.50 * side, ty_y, 0.0])
    g = VGroup(tail, ext_rod, cup)
    if has_side_peg:
        stub = Line([ty_stub_x, ty_y, 0], [x + 0.24 * side, ty_y, 0], color=RECEPTOR, stroke_width=5)
        g.add(stub)
    g.tail = tail
    g.ext_rod = ext_rod
    g.ty_pt = peg_center
    g.jak_anchor = np.array([x + 0.46 * side, mem_y - 0.92, 0.0])
    return g


def build_jak(anchor, side=-1, active=False):
    """Two-lobed JAK block: coral-red working kinase lobe (inner) + muted rose pseudokinase lobe (outer)."""
    kin_x = anchor[0] - 0.58 * side
    pseu_x = anchor[0] + 0.18 * side
    kin = RoundedRectangle(
        corner_radius=0.14, width=0.70, height=0.78,
        stroke_color=PHOSPHATE if active else JAK_KIN,
        stroke_width=4.5 if active else 3.5,
        fill_color=JAK_KIN, fill_opacity=0.68 if active else 0.48,
    ).move_to([kin_x, anchor[1] - 0.04, 0])
    pseu = RoundedRectangle(
        corner_radius=0.14, width=0.56, height=0.64,
        stroke_color=JAK_PSEU, stroke_width=3,
        fill_color=JAK_PSEU, fill_opacity=0.45,
    ).move_to([pseu_x, anchor[1] + 0.06, 0])
    g = VGroup(pseu, kin)
    g.kin = kin
    g.pseu = pseu
    return g


def build_stat(side="right", tagged=False, ghost=False, p_size=24, inverted=False, p_radius=0.27):
    """Emerald-teal STAT block with a wide, deep U-shaped SH2 pocket and a C-terminal tyrosine tail peg.

    When inverted=True, the geometry is built mirrored across Y (SH2 cup opens DOWN, tail peg points DOWN)
    with an upright 'P' label so no Text mobject is ever flipped upside down!
    Local body origin is always (0, 0) (use place_stat_at(stat, pt) to position by body center!).
    """
    sx = 1.0 if side == "right" else -1.0
    sy = -1.0 if inverted else 1.0
    op_fill = 0.18 if ghost else 0.50
    op_stroke = 0.60 if ghost else 1.0

    body = Polygon(
        [-0.94 * sx, -0.38 * sy, 0],
        [0.94 * sx, -0.38 * sy, 0],
        [0.94 * sx, 0.38 * sy, 0],
        [-0.10 * sx, 0.38 * sy, 0],
        [-0.10 * sx, -0.10 * sy, 0],
        [-0.18 * sx, -0.18 * sy, 0],
        [-0.72 * sx, -0.18 * sy, 0],
        [-0.80 * sx, -0.10 * sy, 0],
        [-0.80 * sx, 0.38 * sy, 0],
        [-0.94 * sx, 0.38 * sy, 0],
        stroke_color=STAT_COL, stroke_width=3.5, stroke_opacity=op_stroke,
        fill_color=STAT_COL, fill_opacity=op_fill,
    )
    tail_stem = Line([0.45 * sx, 0.38 * sy, 0], [0.45 * sx, 0.78 * sy, 0],
                     color=STAT_COL, stroke_width=6, stroke_opacity=op_stroke)
    peg_pos = np.array([0.45 * sx, 1.04 * sy, 0])
    if tagged:
        peg = build_phosphate(peg_pos, radius=p_radius, font_size=p_size)
    else:
        peg = Circle(radius=0.14, stroke_color=TEXT, stroke_width=3, stroke_opacity=op_stroke,
                     fill_color=BG, fill_opacity=0.9).move_to(peg_pos)

    g = VGroup(body, tail_stem, peg)
    g.body = body
    g.peg = peg
    g.sh2_local = np.array([-0.45 * sx, 0.12 * sy, 0])
    g.peg_local = peg_pos
    return g


def place_stat_at(stat, body_center):
    """Position a STAT mobject by its main body's center (NOT bbox center including tail peg)."""
    return stat.shift(np.array(body_center, dtype=float) - stat.body.get_center())


def build_clock_arc(progress_tracker, center=(5.25, 2.75, 0), radius=0.44):
    """Live ticking clock arc labelled 'Minutes' for rapid response."""
    c = np.array(center, dtype=float)
    rim = Circle(radius=radius, color=GREY, stroke_width=4, stroke_opacity=0.80).move_to(c)
    wedge = always_redraw(
        lambda: Arc(
            radius=radius,
            start_angle=PI / 2,
            angle=-max(0.01, progress_tracker.get_value()) * TAU * 0.55,
            arc_center=c,
            stroke_color=PHOSPHATE,
            stroke_width=8,
        )
    )
    hand = always_redraw(
        lambda: Line(
            c,
            c + 0.72 * radius * np.array([
                np.cos(PI / 2 - progress_tracker.get_value() * TAU * 0.55),
                np.sin(PI / 2 - progress_tracker.get_value() * TAU * 0.55),
                0.0,
            ]),
            color=TEXT,
            stroke_width=3.5,
        )
    )
    lab = T("Minutes", size=26, color=PHOSPHATE).next_to(rim, DOWN, buff=0.16)
    return VGroup(rim, wedge, hand, lab)


def build_zoomed_stage(paired=False, active_jaks=False, tail_p=False):
    """Zoomed plasma membrane stage carried across s02-s07 (subject fills >70% of frame height)."""
    mem = build_membrane(y=1.65, x_span=6.5, thickness=0.32)
    dx = 0.96 if paired else 2.20
    rec_l = build_receptor_chain(-dx, mem_y=1.65, top_y=2.72, tail_y=-0.95, side=-1)
    rec_r = build_receptor_chain(dx, mem_y=1.65, top_y=2.72, tail_y=-0.95, side=1)
    jak_l = build_jak(rec_l.jak_anchor, side=-1, active=active_jaks)
    jak_r = build_jak(rec_r.jak_anchor, side=1, active=active_jaks)
    g = VGroup(mem, rec_l, rec_r, jak_l, jak_r)
    p_l = p_r = None
    if tail_p:
        p_l = build_phosphate(rec_l.ty_pt, radius=0.24, font_size=26)
        p_r = build_phosphate(rec_r.ty_pt, radius=0.24, font_size=26)
        g.add(p_l, p_r)
    return g, mem, rec_l, rec_r, jak_l, jak_r, p_l, p_r


def build_full_cell():
    """Full cell cross-section carried across s01, s09, s10."""
    mem = build_membrane(y=1.65, x_span=6.4, thickness=0.30)
    nuc = build_nuclear_envelope(y=-1.05, x_span=6.4, pore_half=1.02)
    dna = build_dna(center=(0.0, -2.62, 0.0), width=10.6, amp=0.24, cycles=3.0)
    rec_l = build_receptor_chain(-1.05, mem_y=1.65, top_y=2.60, tail_y=0.35, side=-1, has_side_peg=False)
    rec_r = build_receptor_chain(1.05, mem_y=1.65, top_y=2.60, tail_y=0.35, side=1, has_side_peg=False)
    return VGroup(mem, nuc, dna, rec_l, rec_r), mem, nuc, dna, rec_l, rec_r


def build_docked_state(tagged_stats=False):
    """Exact carried end-of-s04 / s05 / s06 stage so transitions across s04->s05->s06->s07 match."""
    stage, mem, rec_l, rec_r, jak_l, jak_r, p_l, p_r = build_zoomed_stage(paired=True, active_jaks=True, tail_p=True)
    cyto = build_cytokine([0.0, 2.54, 0], rx=0.72, ry=0.42)
    target_l = rec_l.ty_pt - np.array([0.45, 0.12, 0.0])
    target_r = rec_r.ty_pt - np.array([-0.45, 0.12, 0.0])
    stat_l = place_stat_at(build_stat("left", tagged=tagged_stats), target_l)
    stat_r = place_stat_at(build_stat("right", tagged=tagged_stats), target_r)
    sh2_l = T("SH2", size=26, color=TEXT).move_to(target_l + np.array([0.45, -0.68, 0]))
    sh2_r = T("SH2", size=26, color=TEXT).move_to(target_r + np.array([-0.45, -0.68, 0]))
    return stage, cyto, rec_l, rec_r, jak_l, jak_r, p_l, p_r, stat_l, stat_r, sh2_l, sh2_r


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Cytokine Receptors and JAK-STAT"
    TITLE = "A Borrowed Kinase, Straight to DNA"


class S01Hook(SpokenScene):
    def construct(self):
        world, mem, nuc, dna, rec_l, rec_r = build_full_cell()
        dna_lab = T("DNA", size=28, color=DNA_COL).next_to(dna, LEFT, buff=0.22)
        gene_bar = RoundedRectangle(
            corner_radius=0.08, width=2.8, height=0.32,
            stroke_color=PHOSPHATE, stroke_width=3.5, fill_color=PHOSPHATE, fill_opacity=0.10,
        ).move_to([0.0, -2.62, 0])
        gene_bar.set_opacity(0.25)

        wait_jak_l = build_jak(rec_l.jak_anchor, side=-1).set_opacity(0.45)
        wait_jak_r = build_jak(rec_r.jak_anchor, side=1).set_opacity(0.45)
        wait_stat_l = build_stat("left", ghost=True).scale(0.68).move_to([-2.3, -0.15, 0])
        wait_stat_r = build_stat("right", ghost=True).scale(0.68).move_to([2.1, -0.15, 0])
        waiting_parts = VGroup(wait_jak_l, wait_jak_r, wait_stat_l, wait_stat_r)

        ifn_1 = build_cytokine([-0.3, 3.25, 0], rx=0.52, ry=0.30)
        ifn_2 = build_cytokine([0.45, 3.30, 0], rx=0.48, ry=0.28)
        ifn_lab = T("Interferon", size=28, color=CYTOKINE).move_to([-2.95, 3.25, 0])

        clock_t = ValueTracker(0.05)
        clock = build_clock_arc(clock_t, center=(5.25, 2.75, 0), radius=0.44)

        self.add(world, dna_lab, gene_bar)

        self.at("Add interferon")
        self.play(FadeIn(ifn_1), FadeIn(ifn_2), FadeIn(ifn_lab), run_time=0.7)
        self.play(
            ifn_1.animate.move_to([0.0, 2.58, 0]),
            ifn_2.animate.move_to([0.0, 3.00, 0]),
            ifn_lab.animate.move_to([-3.35, 2.45, 0]),
            run_time=1.3,
        )
        bob(ifn_1, amp=0.08, speed=2.2, seed=0)

        self.at("genes switch on")
        gene_on_lab = T("Genes ON", size=28, color=PHOSPHATE).next_to(dna, DOWN, buff=0.22)
        self.play(
            FadeIn(clock),
            gene_bar.animate.set_opacity(1.0).set_fill(PHOSPHATE, opacity=0.65),
            FadeIn(gene_on_lab),
            clock_t.animate.set_value(0.45),
            run_time=1.5,
        )
        pulse(gene_bar, base=5.0, amp=3.5, speed=4.0)

        self.at("without new protein")
        no_prot = boxed_label("× No new protein", color=CYTOKINE, size=26, pad=0.18).move_to([4.55, 0.85, 0])
        self.play(FadeIn(no_prot), clock_t.animate.set_value(0.65), run_time=1.2)

        self.at("receptor with no enzyme")
        no_enz = T("No enzyme", size=28, color=RECEPTOR).move_to([-3.35, 0.95, 0])
        q_path = DashedLine([0.0, 0.35, 0], [0.0, -1.9, 0], color=GOLD, stroke_width=4.5, dash_length=0.16)
        q_mark = T("?", size=42, color=GOLD, weight=BOLD).move_to([0.45, -0.45, 0])
        self.play(FadeIn(no_enz), Create(q_path), FadeIn(q_mark), clock_t.animate.set_value(1.0), run_time=3.6, rate_func=linear)

        self.at("already sit inside")
        wait_lab = T("Waiting inside cell", size=28, color=STAT_COL).move_to([4.55, -0.30, 0])
        self.play(
            FadeOut(q_mark),
            FadeOut(q_path),
            FadeIn(waiting_parts),
            FadeIn(wait_lab),
            run_time=1.2,
        )
        wait_jak_l.set_opacity(0.85)
        wait_jak_r.set_opacity(0.85)
        bob(wait_stat_l, amp=0.09, speed=2.4, seed=1)
        bob(wait_stat_r, amp=0.09, speed=2.4, seed=3)
        self.finish()


class S02BorrowedJak(SpokenScene):
    def construct(self):
        stage, mem, rec_l, rec_r, jak_l, jak_r, _, _ = build_zoomed_stage(paired=False, active_jaks=False)
        jak_l.set_opacity(0)
        jak_r.set_opacity(0)

        cyto = build_cytokine([-4.5, 3.35, 0], rx=0.72, ry=0.42)
        cyto_lab = T("Cytokine", size=28, color=CYTOKINE).move_to([0.0, 3.55, 0])

        self.add(stage)

        self.at("Interferon is a cytokine")
        self.play(FadeIn(cyto), FadeIn(cyto_lab), run_time=0.8)
        # Cytokine arcs over the left receptor before descending between the two binding cups
        cyto_path = VMobject().set_points_smoothly([
            np.array([-4.5, 3.35, 0.0]),
            np.array([-2.6, 3.42, 0.0]),
            np.array([-1.65, 3.36, 0.0]),
            np.array([-1.15, 2.92, 0.0]),
            np.array([0.0, 2.70, 0.0]),
        ])
        self.play(MoveAlongPath(cyto, cyto_path), run_time=4.8, rate_func=smooth)
        self.wait(0.4)
        self.play(FadeOut(cyto), FadeOut(cyto_lab), run_time=0.8)

        self.at("Each receptor chain")
        rec_lab = T("Single-pass receptor", size=28, color=RECEPTOR).move_to([-4.4, 2.35, 0])
        self.play(FadeIn(rec_lab), Indicate(rec_l.ext_rod, color=TEXT), Indicate(rec_r.ext_rod, color=TEXT), run_time=1.5)

        self.at("no enzyme of its own")
        no_enz = T("No enzyme", size=28, color=RECEPTOR).move_to([-4.4, 0.25, 0])
        self.play(FadeIn(no_enz), run_time=1.2)

        self.at("inner tail holds")
        tail_lab = T("Receptor tail", size=28, color=RECEPTOR).move_to([4.85, -0.55, 0])
        tail_arr = Arrow(tail_lab.get_left() + LEFT * 0.1, [2.40, -0.55, 0],
                         color=RECEPTOR, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.18)
        self.play(swap(no_enz, tail_lab, run_time=0.8), Create(tail_arr), run_time=1.1)

        self.at("tyrosine kinase")
        jak_lab = T("JAK kinase", size=28, color=JAK_KIN).move_to([-5.10, 0.65, 0])
        jak_arr = Arrow(jak_lab.get_right() + RIGHT * 0.1, jak_l.pseu.get_left() + LEFT * 0.12,
                        color=JAK_KIN, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.18)
        self.play(
            jak_l.animate.set_opacity(1.0),
            jak_r.animate.set_opacity(1.0),
            FadeIn(jak_lab),
            Create(jak_arr),
            run_time=1.3,
        )

        self.at("waits there before")
        wait_note = T("Waits on tail", size=26, color=TEXT).next_to(jak_lab, DOWN, buff=0.30)
        self.play(FadeIn(wait_note), run_time=0.9)
        bob(jak_l, amp=0.08, speed=2.4, seed=1)
        bob(jak_r, amp=0.08, speed=2.4, seed=4)
        self.finish()


class S03PairAndActivate(SpokenScene):
    def construct(self):
        stage, mem, rec_l, rec_r, jak_l, jak_r, _, _ = build_zoomed_stage(paired=False, active_jaks=False)
        cyto = build_cytokine([0.0, 2.95, 0], rx=0.72, ry=0.42)
        self.add(stage, cyto)
        bob(cyto, amp=0.08, speed=2.2, seed=0)

        self.at("working kinase")
        kin_lab = T("Working kinase", size=28, color=JAK_KIN).move_to([-4.45, -0.35, 0])
        kin_arr = Arrow(kin_lab.get_right() + RIGHT * 0.1, jak_l.kin.get_bottom() + DOWN * 0.1,
                        color=JAK_KIN, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.16)
        self.play(FadeIn(kin_lab), Create(kin_arr), Indicate(jak_l.kin, color=PHOSPHATE), run_time=1.0)

        self.at("pseudokinase")
        pseu_lab = fit_text("Pseudokinase\n(inactive look-alike)", max_w=2.6, size=26, color=JAK_PSEU).move_to([5.35, 0.72, 0])
        pseu_arr = Arrow(pseu_lab.get_left() + LEFT * 0.1, jak_r.pseu.get_right() + RIGHT * 0.1,
                         color=JAK_PSEU, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(pseu_lab), Create(pseu_arr), run_time=1.1)

        self.at("holds the real kinase")
        rest_lab = T("Restrained", size=28, color=JAK_PSEU).move_to([-4.45, 0.85, 0])
        pseu_arr_shifted = Arrow(
            pseu_lab.get_left() + LEFT * 0.1,
            jak_r.pseu.get_right() + RIGHT * 0.1 + LEFT * 0.14,
            color=JAK_PSEU, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.18,
        )
        self.play(
            jak_l.pseu.animate.shift(RIGHT * 0.14),
            jak_r.pseu.animate.shift(LEFT * 0.14),
            Transform(pseu_arr, pseu_arr_shifted),
            FadeIn(rest_lab),
            run_time=1.6,
        )

        self.at("cytokine binds outside")
        cyto.clear_updaters()
        cyto_lab = T("Cytokine", size=28, color=CYTOKINE).move_to([0.0, 3.45, 0])
        self.play(
            FadeOut(kin_lab), FadeOut(kin_arr), FadeOut(pseu_lab), FadeOut(pseu_arr), FadeOut(rest_lab),
            FadeIn(cyto_lab),
            cyto.animate.move_to([0.0, 2.54, 0]),
            run_time=1.3,
        )

        self.at("brings two receptor chains")
        dx_shift = 2.20 - 0.96
        self.play(
            rec_l.animate.shift(RIGHT * dx_shift),
            jak_l.animate.shift(RIGHT * dx_shift),
            rec_r.animate.shift(LEFT * dx_shift),
            jak_r.animate.shift(LEFT * dx_shift),
            FadeOut(cyto_lab),
            run_time=2.4,
        )

        self.at("reach across")
        self.play(
            jak_l.kin.animate.shift(RIGHT * 0.16),
            jak_r.kin.animate.shift(LEFT * 0.16),
            run_time=0.9,
        )

        self.at("phosphorylate each other")
        p_lr = build_phosphate(jak_l.kin.get_center(), radius=0.24, font_size=26)
        p_rl = build_phosphate(jak_r.kin.get_center(), radius=0.24, font_size=26)
        self.play(
            p_lr.animate.move_to(jak_r.kin.get_center()),
            p_rl.animate.move_to(jak_l.kin.get_center()),
            run_time=1.1,
        )

        self.at("switch both kinases")
        act_lab = T("JAKs activate each other", size=28, color=PHOSPHATE).move_to([0.0, -2.05, 0])
        self.play(
            jak_l.kin.animate.set_fill(JAK_KIN, opacity=0.72).set_stroke(PHOSPHATE, width=5),
            jak_r.kin.animate.set_fill(JAK_KIN, opacity=0.72).set_stroke(PHOSPHATE, width=5),
            jak_l.pseu.animate.shift(LEFT * 0.14),
            jak_r.pseu.animate.shift(RIGHT * 0.14),
            FadeIn(act_lab),
            run_time=1.5,
        )

        self.at("borrowed an enzyme")
        bor_lab = T("Borrowed enzyme: ON", size=28, color=JAK_KIN).move_to([4.15, 0.70, 0])
        self.play(FadeIn(bor_lab), run_time=1.0)
        pulse(jak_l.kin, base=6.0, amp=3.5, speed=4.2)
        pulse(jak_r.kin, base=6.0, amp=3.5, speed=4.2)
        bob(cyto, amp=0.07, speed=2.2, seed=0)
        self.finish()


class S04DockStat(SpokenScene):
    def construct(self):
        stage, mem, rec_l, rec_r, jak_l, jak_r, _, _ = build_zoomed_stage(paired=True, active_jaks=True)
        cyto = build_cytokine([0.0, 2.54, 0], rx=0.72, ry=0.42)
        self.add(stage, cyto)
        bob(cyto, amp=0.07, speed=2.2, seed=0)
        pulse(jak_l.kin, base=5.5, amp=3.0, speed=4.0)
        pulse(jak_r.kin, base=5.5, amp=3.0, speed=4.0)

        p_l = build_phosphate(jak_l.kin.get_center(), radius=0.27, font_size=24)
        p_r = build_phosphate(jak_r.kin.get_center(), radius=0.27, font_size=24)

        self.at("add phosphate tags")
        self.play(p_l.animate.move_to(rec_l.ty_pt), run_time=0.95)
        self.play(p_r.animate.move_to(rec_r.ty_pt), run_time=0.95)

        self.at("landing pads")
        pad_lab = T("Landing pads (pY)", size=28, color=PHOSPHATE).move_to([4.35, -0.15, 0])
        pad_arr = Arrow(pad_lab.get_left() + LEFT * 0.1, p_r.get_right() + RIGHT * 0.12,
                        color=PHOSPHATE, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(pad_lab), Create(pad_arr), Indicate(p_l.circle, color=TEXT), Indicate(p_r.circle, color=TEXT), run_time=2.2)

        self.at("STAT drifts up")
        stat_l = place_stat_at(build_stat("left", tagged=False), [-2.5, -2.90, 0])
        stat_r = place_stat_at(build_stat("right", tagged=False), [2.5, -2.90, 0])
        stat_lab = T("STAT", size=28, color=STAT_COL).move_to([-4.6, -2.15, 0])
        self.play(
            FadeIn(stat_l), FadeIn(stat_r), FadeIn(stat_lab),
            stat_l.animate.shift(UP * 1.15 + RIGHT * 0.35),
            stat_r.animate.shift(UP * 1.15 + LEFT * 0.35),
            run_time=2.8,
        )

        self.at("SH2 domain")
        sh2_r = T("SH2", size=26, color=TEXT).move_to(stat_r.body.get_center() + np.array([-0.45, -0.68, 0]))
        sh2_l = T("SH2", size=26, color=TEXT).move_to(stat_l.body.get_center() + np.array([0.45, -0.68, 0]))
        self.play(FadeOut(pad_lab), FadeOut(pad_arr), FadeIn(sh2_r), FadeIn(sh2_l), run_time=1.0)

        self.at("pocket that grips")
        empathy_lab = boxed_label("SH2 = grips pY", color=PHOSPHATE, size=26, pad=0.18).move_to([4.75, -1.15, 0])
        self.play(FadeIn(empathy_lab), run_time=1.1)

        self.at("STAT docks beside")
        target_l = rec_l.ty_pt - np.array([0.45, 0.12, 0.0])
        target_r = rec_r.ty_pt - np.array([-0.45, 0.12, 0.0])
        d_l = target_l - stat_l.body.get_center()
        d_r = target_r - stat_r.body.get_center()
        self.play(
            stat_l.animate.shift(d_l),
            stat_r.animate.shift(d_r),
            sh2_l.animate.move_to(target_l + np.array([0.45, -0.68, 0])),
            sh2_r.animate.move_to(target_r + np.array([-0.45, -0.68, 0])),
            stat_lab.animate.move_to([-4.35, -0.85, 0]),
            run_time=1.8,
        )
        bob(stat_l, amp=0.07, speed=2.4, seed=1)
        bob(stat_r, amp=0.07, speed=2.4, seed=3)
        self.finish()


class S05TagStatQuestion(SpokenScene):
    def construct(self):
        stage, cyto, rec_l, rec_r, jak_l, jak_r, p_l, p_r, stat_l, stat_r, sh2_l, sh2_r = build_docked_state(tagged_stats=False)
        self.add(stage, cyto, stat_l, stat_r, sh2_l, sh2_r)
        bob(cyto, amp=0.07, speed=2.2, seed=0)
        pulse(jak_l.kin, base=5.5, amp=3.0, speed=4.0)
        pulse(jak_r.kin, base=5.5, amp=3.0, speed=4.0)

        new_p_l = build_phosphate(jak_l.kin.get_center(), radius=0.24, font_size=26)
        new_p_r = build_phosphate(jak_r.kin.get_center(), radius=0.24, font_size=26)
        peg_l_pos = stat_l.body.get_center() + np.array([-0.45, 1.04, 0])
        peg_r_pos = stat_r.body.get_center() + np.array([0.45, 1.04, 0])

        self.at("adds one phosphate")
        self.play(
            FadeOut(stat_l.peg, run_time=0.4),
            FadeOut(stat_r.peg, run_time=0.4),
            new_p_l.animate.move_to(peg_l_pos),
            new_p_r.animate.move_to(peg_r_pos),
            run_time=2.2,
        )
        self.remove(stat_l.peg, stat_r.peg)
        stat_l.peg, stat_r.peg = new_p_l, new_p_r
        stat_l.add(new_p_l)
        stat_r.add(new_p_r)

        self.at("Notice what has changed")
        self.play(Indicate(stat_l.body, color=TEXT), Indicate(stat_r.body, color=TEXT), run_time=1.4)

        self.at("used its SH2 domain")
        sh2_note = T("SH2 (docked)", size=26, color=STAT_COL).move_to([-4.25, -1.45, 0])
        self.play(FadeIn(sh2_note), Indicate(sh2_l, color=PHOSPHATE), Indicate(sh2_r, color=PHOSPHATE), run_time=1.8)

        self.at("carries its own")
        p_note = T("Own P tag", size=26, color=PHOSPHATE).move_to([4.25, 0.25, 0])
        self.play(
            FadeIn(p_note),
            stat_l.animate.shift(DOWN * 0.16),
            stat_r.animate.shift(DOWN * 0.16),
            sh2_l.animate.shift(DOWN * 0.16),
            sh2_r.animate.shift(DOWN * 0.16),
            run_time=1.4,
        )
        bob(stat_l, amp=0.07, speed=2.4, seed=1)
        bob(stat_r, amp=0.07, speed=2.4, seed=3)

        self.at("what can two tagged")
        q = question_card("What can two tagged STATs do next?")
        self.play(FadeIn(q.question), run_time=1.1)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "What can two tagged STATs do next?"
    SECONDS = 4.5

    def backdrop(self):
        stage, cyto, _, _, _, _, _, _, stat_l, stat_r, sh2_l, sh2_r = build_docked_state(tagged_stats=True)
        stat_l.shift(DOWN * 0.16)
        stat_r.shift(DOWN * 0.16)
        sh2_l.shift(DOWN * 0.16)
        sh2_r.shift(DOWN * 0.16)
        sh2_note = T("SH2 (docked)", size=26, color=STAT_COL).move_to([-4.25, -1.45, 0])
        p_note = T("Own P tag", size=26, color=PHOSPHATE).move_to([4.25, 0.25, 0])
        bob(stat_l, amp=0.07, speed=2.4, seed=1)
        bob(stat_r, amp=0.07, speed=2.4, seed=3)
        return VGroup(stage, cyto, stat_l, stat_r, sh2_l, sh2_r, sh2_note, p_note)


class S07TwoGrips(SpokenScene):
    def construct(self):
        stage, cyto, rec_l, rec_r, jak_l, jak_r, p_l, p_r, stat_l, stat_r, sh2_l, sh2_r = build_docked_state(tagged_stats=True)
        stat_l.shift(DOWN * 0.16)
        stat_r.shift(DOWN * 0.16)
        sh2_l.shift(DOWN * 0.16)
        sh2_r.shift(DOWN * 0.16)
        q = question_card("What can two tagged STATs do next?")
        self.add(stage, cyto, stat_l, stat_r, sh2_l, sh2_r, q)
        bob(cyto, amp=0.07, speed=2.2, seed=0)
        pulse(jak_l.kin, base=5.5, amp=3.0, speed=4.0)
        pulse(jak_r.kin, base=5.5, amp=3.0, speed=4.0)

        self.play(FadeOut(q), run_time=0.35)

        self.at("trade one grip")
        self.play(
            FadeOut(sh2_l), FadeOut(sh2_r),
            stat_l.animate.shift(DOWN * 0.45),
            stat_r.animate.shift(DOWN * 0.45),
            run_time=1.3,
        )

        self.at("SH2 domain locks")
        clamp_y = -2.05
        tight_top = place_stat_at(build_stat("left", tagged=True, inverted=True), [0.0, clamp_y + 0.58, 0])
        tight_bot = place_stat_at(build_stat("right", tagged=True, inverted=False), [0.0, clamp_y - 0.58, 0])
        self.play(
            ReplacementTransform(stat_l, tight_top),
            ReplacementTransform(stat_r, tight_bot),
            run_time=2.2,
        )

        sh2_top = T("SH2", size=26, color=TEXT).move_to([0.45, clamp_y + 1.24, 0])
        sh2_bot = T("SH2", size=26, color=TEXT).move_to([-0.45, clamp_y - 1.24, 0])
        self.play(FadeIn(sh2_top), FadeIn(sh2_bot), run_time=0.8)

        self.at("Receptor docking")
        rev_lab = T("Receptor docking: reversible", size=26, color=RECEPTOR).move_to([4.15, -0.55, 0])
        rev_arr = DoubleArrow(
            [rec_r.ty_pt[0] + 0.30, rec_r.ty_pt[1], 0],
            [rev_lab.get_left()[0] - 0.12, -0.55, 0],
            color=RECEPTOR, stroke_width=3.5, buff=0.05, max_tip_length_to_length_ratio=0.18,
        )
        self.play(FadeIn(rev_lab), Create(rev_arr), run_time=1.5)

        self.at("two reciprocal grips")
        # Rings radius 0.36 centered cleanly around each locked 'P' badge (radius 0.24)
        lock_l = Circle(radius=0.36, stroke_color=PHOSPHATE, stroke_width=4).move_to(tight_top.peg.get_center())
        lock_r = Circle(radius=0.36, stroke_color=PHOSPHATE, stroke_width=4).move_to(tight_bot.peg.get_center())
        badge = boxed_label("1 grip on tail → 2 grips in pair", color=PHOSPHATE, size=26, pad=0.18).move_to([-4.05, -2.05, 0])
        self.play(Create(lock_l), Create(lock_r), FadeIn(badge), run_time=1.6)
        pulse(lock_l, base=4.5, amp=3.0, speed=4.0)
        pulse(lock_r, base=4.5, amp=3.0, speed=4.0)

        self.at("same SH2 domain")
        twice_lab = boxed_label("SH2 used twice", color=STAT_COL, size=28, pad=0.18).move_to([4.05, -2.05, 0])
        self.play(FadeOut(rev_lab), FadeOut(rev_arr), FadeIn(twice_lab), run_time=1.2)
        self.finish()


class S08ToDna(SpokenScene):
    def construct(self):
        nuc = build_nuclear_envelope(y=0.05, x_span=6.4, pore_half=1.08)
        dna = build_dna(center=(-1.65, -2.62, 0.0), width=7.5, amp=0.22, cycles=2.5)
        dna_lab = T("DNA", size=28, color=DNA_COL).next_to(dna, LEFT, buff=0.20)
        nuc_lab = T("Nucleus", size=26, color=GREY).move_to([-5.3, -0.78, 0])
        self.add(nuc, dna, dna_lab, nuc_lab)

        loose_top = place_stat_at(build_stat("left", tagged=False, ghost=True, inverted=True), [0.0, 2.38, 0])
        loose_bot = place_stat_at(build_stat("right", tagged=False, ghost=True, inverted=False), [0.0, 1.12, 0])
        loose_pair = VGroup(loose_top, loose_bot)
        loose_lab = T("Loose inactive pair", size=28, color=STAT_COL).move_to([-4.05, 1.75, 0])

        self.at("loose")
        self.play(FadeIn(loose_pair), FadeIn(loose_lab), run_time=1.1)
        bob(loose_top, amp=0.07, speed=2.2, seed=1)
        bob(loose_bot, amp=0.07, speed=2.2, seed=3)

        self.at("Phosphorylation flips")
        loose_top.clear_updaters()
        loose_bot.clear_updaters()
        tight_top = place_stat_at(build_stat("left", tagged=True, p_size=26, inverted=True), [0.0, 2.32, 0])
        tight_bot = place_stat_at(build_stat("right", tagged=True, p_size=26, inverted=False), [0.0, 1.16, 0])
        tight_pair = VGroup(tight_top, tight_bot)
        tight_lab = T("Tight active clamp", size=28, color=PHOSPHATE).move_to([-4.05, 1.75, 0])
        self.play(
            ReplacementTransform(loose_pair, tight_pair),
            swap(loose_lab, tight_lab, run_time=0.9),
            run_time=1.8,
        )

        self.at("moves into the nucleus")
        self.play(
            FadeOut(tight_lab),
            tight_pair.animate.scale(0.88).move_to([0.0, 0.15, 0]),
            run_time=1.5,
        )

        self.at("clamps onto a specific")
        target_x = -1.65
        self.play(tight_pair.animate.move_to([target_x, -1.48, 0]), run_time=1.4)
        targ_lab = T("Specific DNA site", size=26, color=DNA_COL).move_to([-1.65, -3.22, 0])
        self.play(FadeIn(targ_lab), run_time=0.7)

        self.at("switch on genes")
        tx_arrow = Arrow([target_x + 1.05, -1.55, 0], [target_x + 3.05, -1.55, 0],
                         color=PHOSPHATE, stroke_width=5, buff=0.0, max_tip_length_to_length_ratio=0.22)
        tx_lab = T("Genes ON", size=28, color=PHOSPHATE).next_to(tx_arrow, UP, buff=0.18)
        self.play(Create(tx_arrow), FadeIn(tx_lab), run_time=1.2)

        self.at("For some interferons")
        inset_box = RoundedRectangle(
            corner_radius=0.16, width=4.0, height=2.55,
            stroke_color=IRF9_COL, stroke_width=3, fill_color=BG, fill_opacity=0.95,
        ).move_to([4.25, -1.85, 0])
        inset_head = T("Some interferons: + IRF9", size=24, color=IRF9_COL).move_to([4.25, -0.88, 0])
        mini_dna = Line([2.65, -2.65, 0], [5.85, -2.65, 0], color=DNA_COL, stroke_width=5)
        mini_stat = RoundedRectangle(
            corner_radius=0.10, width=1.45, height=0.62,
            stroke_color=STAT_COL, stroke_width=3, fill_color=STAT_COL, fill_opacity=0.45,
        ).move_to([3.65, -2.10, 0])
        mini_stat_lab = T("STAT pair", size=22, color=STAT_COL).move_to(mini_stat)
        self.play(FadeIn(inset_box), FadeIn(inset_head), Create(mini_dna), FadeIn(mini_stat), FadeIn(mini_stat_lab), run_time=1.3)

        self.at("IRF9")
        irf9 = boxed_label("IRF9", color=IRF9_COL, size=24, pad=0.16).move_to([5.45, -1.45, 0])
        self.play(FadeIn(irf9), run_time=0.6)
        self.play(irf9.animate.move_to([5.05, -2.10, 0]), run_time=1.0)
        bob(tight_pair, amp=0.06, speed=2.2, seed=2)
        self.finish()


class S09DirectPath(SpokenScene):
    def construct(self):
        mem = build_membrane(y=1.65, x_span=6.4, thickness=0.30)
        nuc = build_nuclear_envelope(y=-0.70, x_span=6.4, pore_half=1.02, pore_x=-2.3)
        dna = build_dna(center=(-2.3, -2.72, 0.0), width=6.8, amp=0.22, cycles=2.2)

        rec_l = build_receptor_chain(-3.15, mem_y=1.65, top_y=2.60, tail_y=0.45, side=-1, has_side_peg=False)
        rec_r = build_receptor_chain(-1.45, mem_y=1.65, top_y=2.60, tail_y=0.45, side=1, has_side_peg=False)
        cyto = build_cytokine([-2.3, 2.52, 0], rx=0.60, ry=0.34)
        jak_l = build_jak(rec_l.jak_anchor, side=-1, active=True)
        jak_r = build_jak(rec_r.jak_anchor, side=1, active=True)

        # Clamped STAT pair sitting cleanly inside nucleus below the pore (top ~ -1.17, bottom ~ -2.47)
        stat_t = place_stat_at(build_stat("left", tagged=True, p_size=33, inverted=True, p_radius=0.32), [0.0, 0.58, 0])
        stat_b = place_stat_at(build_stat("right", tagged=True, p_size=33, inverted=False, p_radius=0.32), [0.0, -0.58, 0])
        stat_pair = VGroup(stat_t, stat_b).scale(0.68).move_to([-2.3, -1.82, 0])

        self.add(mem, nuc, dna, rec_l, rec_r, cyto, jak_l, jak_r, stat_pair)
        bob(cyto, amp=0.07, speed=2.2, seed=0)
        pulse(jak_l.kin, base=5.5, amp=3.0, speed=4.0)
        pulse(jak_r.kin, base=5.5, amp=3.0, speed=4.0)

        c_title = T("No cascade (schematic)", size=26, color=TEXT).move_to([4.15, 2.55, 0])
        no_x = VGroup(
            Line([-0.13, -0.13, 0], [0.13, 0.13, 0], color=JAK_KIN, stroke_width=4),
            Line([-0.13, 0.13, 0], [0.13, -0.13, 0], color=JAK_KIN, stroke_width=4),
        ).next_to(c_title, LEFT, buff=0.16)
        c_nodes = VGroup(
            boxed_label("2nd messenger", color=GREY, size=22, pad=0.10),
            boxed_label("Kinase 1", color=GREY, size=22, pad=0.10),
            boxed_label("Kinase 2", color=GREY, size=22, pad=0.10),
            boxed_label("Kinase 3", color=GREY, size=22, pad=0.10),
        ).arrange(DOWN, buff=0.15).move_to([4.05, 0.32, 0])
        for nd in c_nodes:
            nd.label.set_color(TEXT)
        c_arrows = VGroup(*[
            Arrow(c_nodes[i].get_bottom(), c_nodes[i + 1].get_top(),
                  color=TEXT, stroke_width=3.5, buff=0.01, max_tip_length_to_length_ratio=0.42)
            for i in range(3)
        ])
        cascade = VGroup(c_nodes, c_arrows).set_opacity(0.72)

        self.at("Step back")
        self.play(Indicate(cyto), Indicate(stat_t.body), Indicate(stat_b.body), run_time=1.8)

        self.at("no second messenger")
        self.play(FadeIn(c_title), FadeIn(cascade), run_time=1.3)

        self.at("no chain of kinases")
        self.play(Create(no_x), cascade.animate.set_opacity(0.58), run_time=1.0)

        self.at("One borrowed kinase")
        relay_line = DashedLine([-2.3, 1.10, 0], [-2.3, -1.10, 0], color=PHOSPHATE, stroke_width=5, dash_length=0.15)
        relay_lab = T("Direct relay", size=28, color=PHOSPHATE).move_to([-4.65, -0.15, 0])
        sig_t = ValueTracker(0.0)
        sig_dot = always_redraw(
            lambda: VGroup(
                Circle(radius=0.24, stroke_color=PHOSPHATE, stroke_width=3, fill_color=PHOSPHATE, fill_opacity=0.30),
                Dot(ORIGIN, radius=0.14, color=PHOSPHATE),
            ).move_to([-2.3, 1.10 - 2.20 * (sig_t.get_value() % 1.0), 0])
        )
        self.play(Create(relay_line), FadeIn(relay_lab), FadeIn(sig_dot), run_time=1.2)

        self.at("travels straight to DNA")
        self.play(sig_t.animate.set_value(1.0), run_time=2.2, rate_func=linear)

        self.at("Cytokine receptors borrow")
        gene_glow = RoundedRectangle(
            corner_radius=0.08, width=2.4, height=0.28,
            stroke_color=PHOSPHATE, stroke_width=3.5, fill_color=PHOSPHATE, fill_opacity=0.60,
        ).move_to([-0.1, -2.72, 0])
        self.play(FadeIn(gene_glow), sig_t.animate.set_value(3.0), run_time=4.2, rate_func=linear)
        pulse(gene_glow, base=5.0, amp=3.5, speed=4.0)
        self.finish()


class S10ScopeClose(SpokenScene):
    def construct(self):
        world, mem, nuc, dna, rec_l, rec_r = build_full_cell()
        cyto = build_cytokine([0.0, 2.52, 0], rx=0.60, ry=0.34)
        jak_l = build_jak(rec_l.jak_anchor, side=-1, active=True)
        jak_r = build_jak(rec_r.jak_anchor, side=1, active=True)

        stat_t = place_stat_at(build_stat("left", tagged=True, p_size=27, inverted=True), [0.0, 0.58, 0])
        stat_b = place_stat_at(build_stat("right", tagged=True, p_size=27, inverted=False), [0.0, -0.58, 0])
        stat_pair = VGroup(stat_t, stat_b).scale(0.84).move_to([0.0, -1.60, 0])

        gene_bar = RoundedRectangle(
            corner_radius=0.08, width=2.6, height=0.30,
            stroke_color=PHOSPHATE, stroke_width=3.5, fill_color=PHOSPHATE, fill_opacity=0.60,
        ).move_to([2.65, -2.62, 0])
        tx_arrow = Arrow([1.45, -1.95, 0], [3.85, -1.95, 0],
                         color=PHOSPHATE, stroke_width=5, buff=0.0, max_tip_length_to_length_ratio=0.22)

        arc_t = ValueTracker(0.0)
        arc_curve = ArcBetweenPoints(
            np.array([0.0, 1.25, 0]),
            np.array([0.0, -0.65, 0]),
            angle=-0.38,
            stroke_color=PHOSPHATE,
            stroke_width=5,
        )
        sig_bead = always_redraw(
            lambda: VGroup(
                Circle(radius=0.24, stroke_color=PHOSPHATE, stroke_width=3, fill_color=PHOSPHATE, fill_opacity=0.30),
                Dot(ORIGIN, radius=0.14, color=PHOSPHATE),
            ).move_to(arc_curve.point_from_proportion(arc_t.get_value() % 1.0))
        )

        clock_t = ValueTracker(0.1)
        clock = build_clock_arc(clock_t, center=(-5.2, 2.75, 0), radius=0.44)

        self.add(world, cyto, jak_l, jak_r, stat_pair, gene_bar, tx_arrow, arc_curve, sig_bead)
        pulse(gene_bar, base=5.0, amp=3.5, speed=4.0)
        bob(cyto, amp=0.06, speed=2.2, seed=0)

        self.at("most cytokine receptors")
        scope_1 = boxed_label("Class I & II cytokine receptors", color=RECEPTOR, size=24, pad=0.16).move_to([4.05, 2.85, 0])
        self.play(FadeIn(scope_1), arc_t.animate.set_value(1.2), run_time=2.2, rate_func=linear)

        self.at("borrowed kinase")
        jak_tag = T("Borrowed JAK", size=28, color=JAK_KIN).move_to([-4.05, 0.70, 0])
        self.play(FadeIn(jak_tag), Indicate(jak_l.kin, color=TEXT, rate_func=there_and_back),
                  arc_t.animate(rate_func=linear).set_value(2.2), run_time=1.3)

        self.at("waiting stat")
        stat_tag = T("Waiting STAT", size=28, color=STAT_COL).move_to([-4.05, -0.55, 0])
        self.play(FadeIn(stat_tag), Indicate(stat_t.body, color=TEXT, rate_func=there_and_back),
                  Indicate(stat_b.body, color=TEXT, rate_func=there_and_back),
                  arc_t.animate(rate_func=linear).set_value(3.5), run_time=2.0)

        self.at("No new protein")
        scope_2 = boxed_label("Waiting parts → rapid response", color=STAT_COL, size=24, pad=0.16).move_to([4.15, -0.15, 0])
        self.play(FadeIn(scope_2), FadeIn(clock), arc_t.animate.set_value(5.5), run_time=3.5, rate_func=linear)

        self.at("within minutes")
        self.play(clock_t.animate.set_value(1.0), arc_t.animate.set_value(6.8), run_time=1.6, rate_func=linear)
        self.finish()


class S11End(EndCard):
    LINE = "Cytokine receptors borrow JAKs to send paired STATs straight to DNA."
