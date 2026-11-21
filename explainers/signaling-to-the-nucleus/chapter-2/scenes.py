# ==============================================================================
# FILM: "Pairing Up to Launch the Second Wave" (signaling-to-the-nucleus__chapter-2)
#
# COLOUR MAP (one colour per concept for the entire film):
#   MEMBRANE   = "#64748B"   # slate-blue plasma membrane
#   CYTOSOL    = "#141A29"   # dark cytosol interior
#   NUCLEUS    = "#262366"   # deep-indigo nucleus interior
#   NUC_EDGE   = "#6366F1"   # indigo nuclear envelope
#   DNA_COL    = "#E8EAF0"   # white DNA bar (TEXT)
#   PHOS_P     = "#F59E0B"   # amber phosphate badge ('P')
#   CREB_COL   = "#A78BFA"   # violet CREB factor
#   NFAT_COL   = "#38BDF8"   # sky-blue NFAT factor
#   MRNA_COL   = "#34D399"   # mint mRNA transcripts (c-fos, first wave)
#   JUN_COL    = "#FBBF24"   # gold-ochre Jun rods
#   FOS_COL    = "#E879F9"   # magenta-pink Fos rods
#   GENERIC_A  = "#58C4DD"   # neutral protein A in s03 math
#   GENERIC_B  = "#FB923C"   # neutral protein B in s03 math
#   GENERIC_C  = "#818CF8"   # neutral protein C in s03 math
#
# CARRIED WORLD PICTURE:
#   2D cell cross-section (slate-blue membrane at top, dark cytosol in middle,
#   deep-indigo nucleus at bottom with nuclear pore and horizontal white DNA bar),
#   zooming onto the white DNA bar inside the nucleus for bZIP pairing mechanics
#   and returning to the full cross-section to follow c-fos transcription, translation,
#   nuclear import of Fos, AP-1 + NFAT assembly on IL-2, and the two-wave program.
#
# WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
#   s01_bridge_hook    : Amber 'P' snaps onto CREB, sky-blue NFAT glides through the
#                        nuclear pore onto DNA, mint mRNA grows, and a schematic
#                        clock sector + needle sweeps linearly from minutes to hours.
#   s02_bzip_structure : A single CREB rod sweeps/slips across DNA (cannot grip alone),
#                        then a second rod glides in, zips along 5 leucine dots
#                        (zip tracker 0->1), and parts its '+' tips like chopsticks
#                        (grip tracker 0->1) to bind two '-' DNA half-sites.
#   s03_free_math      : Partner B slides in to replace A shifting DNA site; then
#                        duplicate lower-triangle cells fold away as 3x3 upper-triangle
#                        cells illuminate one by one with a live counter (0->6).
#   s04_fos_jun_rule   : Gold Jun and magenta Fos rods slide into 3 lanes above DNA;
#                        Jun-Jun and Fos-Jun (AP-1) zip and dock, while two Fos rods
#                        flash '-' flank charges and rebound apart under repulsion.
#   s05_predict_prompt : 2 Jun + 2 Fos rods and 4x4 grid build step-by-step, then the
#                        3 Fos-Fos cells dim and cross out ('x') while Fos-Fos rods
#                        push apart beside the bottom question card.
#   s07_predict_reveal : Live counter, illuminated cells, and proportional tally bars
#                        grow sequentially: 3 Jun-Jun (2*3/2=3), 4 Fos-Jun (2*2=4),
#                        +0 Fos-Fos, 3+4=7 vs 4*5/2=10 if free.
#   s08_sites_and_cfos : Jun-Jun rocks loosely while Fos-Jun clamps onto a 7-letter
#                        slot and CREB onto an 8-letter slot; camera pulls back to
#                        the cell as CREB launches growing mint c-fos mRNA ribbons.
#   s09_ap1_and_nfat   : Cytosolic ribosomes translate c-fos mRNA into a growing magenta
#                        Fos rod, which imports through the nuclear pore, zips with Jun
#                        on IL-2, and meets sky-blue NFAT with twin pathway pulses.
#   s10_second_wave    : Computed bimodal schematic Plot sweeps a live time cursor +
#                        shaded area for fast mint first wave (c-fos, minutes) and
#                        delayed broad Fos-Jun second wave (AP-1 targets, hours);
#                        an upper inset stains 2 of 5 excited neuron nuclei magenta.
# ==============================================================================

from bp_parts import *

# ---- Concept Palette ----
MEMBRANE = "#64748B"
CYTOSOL = "#141A29"
NUCLEUS = "#262366"
NUC_EDGE = "#6366F1"
DNA_COL = TEXT        # "#E8EAF0"
PHOS_P = "#F59E0B"
CREB_COL = "#A78BFA"
NFAT_COL = "#38BDF8"
MRNA_COL = "#34D399"
JUN_COL = "#FBBF24"
FOS_COL = "#E879F9"

GENERIC_A = "#58C4DD"
GENERIC_B = "#FB923C"
GENERIC_C = "#818CF8"


# ---- Shared World & Component Helpers ----
def build_cell_world(y_mem=1.65, y_nuc=-0.10, y_bot=-2.95, x_half=6.1, pore_half=1.25,
                     dna_y=-2.05, dna_w=8.4):
    """Carried 2D cell cross-section: membrane, cytosol, nucleus with pore, and DNA bar."""
    w = 2 * x_half
    cyto_h = y_mem - y_nuc
    nuc_h = y_nuc - y_bot

    cyto = Rectangle(width=w, height=cyto_h, fill_color=CYTOSOL, fill_opacity=0.95,
                     stroke_width=0).move_to([0, (y_mem + y_nuc) / 2, 0])
    mem_bar = RoundedRectangle(corner_radius=0.08, width=w, height=0.28,
                               fill_color=MEMBRANE, fill_opacity=0.92,
                               stroke_color=MEMBRANE, stroke_width=2).move_to([0, y_mem, 0])

    nuc_w = w - 0.5
    nuc_fill = RoundedRectangle(corner_radius=0.30, width=nuc_w, height=nuc_h,
                                fill_color=NUCLEUS, fill_opacity=0.95,
                                stroke_width=0).move_to([0, (y_nuc + y_bot) / 2, 0])
    nuc_x = nuc_w / 2
    env_l = Line([-nuc_x, y_nuc, 0], [-pore_half, y_nuc, 0], color=NUC_EDGE, stroke_width=4.5)
    env_r = Line([pore_half, y_nuc, 0], [nuc_x, y_nuc, 0], color=NUC_EDGE, stroke_width=4.5)
    env_bot = Line([-nuc_x, y_bot, 0], [nuc_x, y_bot, 0], color=NUC_EDGE, stroke_width=3.5)
    env_sl = Line([-nuc_x, y_nuc, 0], [-nuc_x, y_bot, 0], color=NUC_EDGE, stroke_width=3.5)
    env_sr = Line([nuc_x, y_nuc, 0], [nuc_x, y_bot, 0], color=NUC_EDGE, stroke_width=3.5)
    env = VGroup(env_l, env_r, env_bot, env_sl, env_sr)

    dna = VGroup(
        Line([-dna_w / 2, dna_y + 0.09, 0], [dna_w / 2, dna_y + 0.09, 0], color=DNA_COL, stroke_width=4.5),
        Line([-dna_w / 2, dna_y - 0.09, 0], [dna_w / 2, dna_y - 0.09, 0], color=DNA_COL, stroke_width=4.5),
    )
    for rx in np.linspace(-dna_w / 2 + 0.30, dna_w / 2 - 0.30, 15):
        dna.add(Line([rx, dna_y - 0.09, 0], [rx, dna_y + 0.09, 0], color=DNA_COL, stroke_width=2).set_opacity(0.5))

    dna_lbl = T("DNA", 24, DNA_COL).next_to(dna, LEFT, buff=0.18)
    cyt_lbl = T("cytosol", 24, TEXT).move_to([-x_half + 0.95, y_mem - 0.48, 0])
    nuc_lbl = T("nucleus", 24, TEXT).move_to([-x_half + 1.15, y_nuc - 0.42, 0])

    world = VGroup(cyto, nuc_fill, mem_bar, env, dna, dna_lbl, cyt_lbl, nuc_lbl)
    world.y_mem = y_mem
    world.y_nuc = y_nuc
    world.y_bot = y_bot
    world.dna_y = dna_y
    world.dna = dna
    return world


def make_phos_badge(center=ORIGIN, radius=0.22):
    """Small amber 'P' circle badge."""
    c = Circle(radius=radius, fill_color=PHOS_P, fill_opacity=0.95, stroke_color=TEXT, stroke_width=2).move_to(center)
    p = T("P", 22, BG, weight=BOLD).move_to(c)
    return VGroup(c, p)


def make_mrna_ribbon(start, end, amp=0.13, waves=3.5, color=MRNA_COL, stroke_width=5, frac=1.0):
    """Wavy mRNA ribbon between start and end, drawn up to frac (0..1)."""
    p0 = np.array(start, dtype=float)
    p1 = np.array(end, dtype=float)
    d = p1 - p0
    L = np.linalg.norm(d)
    u = d / max(L, 1e-6)
    perp = np.array([-u[1], u[0], 0.0])
    f = float(np.clip(frac, 0.02, 1.0))
    ts = np.linspace(0, f, max(4, int(48 * f)))
    pts = [p0 + t * d + perp * (amp * np.sin(t * waves * TAU)) for t in ts]
    m = VMobject(stroke_color=color, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


def make_dna_bar(width=10.8, y=-2.2, slots=None, color=DNA_COL):
    """Zoomed-in white DNA bar with optional highlighted slot brackets."""
    bar = VGroup(
        Line([-width / 2, y + 0.13, 0], [width / 2, y + 0.13, 0], color=color, stroke_width=5.5),
        Line([-width / 2, y - 0.13, 0], [width / 2, y - 0.13, 0], color=color, stroke_width=5.5),
    )
    n_rungs = int(width * 2.4)
    for rx in np.linspace(-width / 2 + 0.25, width / 2 - 0.25, n_rungs):
        bar.add(Line([rx, y - 0.13, 0], [rx, y + 0.13, 0], color=color, stroke_width=2.2).set_opacity(0.5))
    if slots:
        for sx, sw, scol in slots:
            slot_box = RoundedRectangle(
                corner_radius=0.08, width=sw, height=0.36,
                stroke_color=scol, stroke_width=3, fill_color=scol, fill_opacity=0.22
            ).move_to([sx, y, 0])
            bar.add(slot_box)
    return bar


def make_bzip_pair(cx=0.0, dna_y=-2.2, left_col=CREB_COL, right_col=CREB_COL,
                   zip_t=1.0, grip_t=1.0, lift=0.0, rod_w=0.28,
                   upper_len=1.85, lower_len=1.35):
    """Build a dynamic pair of bZIP rods from zip_t (0..1) and grip_t (0..1)."""
    hinge_y = dna_y + lower_len * 1.07 + lift
    sep = 1.05 * (1.0 - zip_t) + 0.17 * zip_t
    ang = 0.42 * grip_t

    g = VGroup()
    for side, col in ((-1, left_col), (1, right_col)):
        hx = cx + side * sep
        top_pt = np.array([hx, hinge_y + upper_len, 0.0])
        hinge_pt = np.array([hx, hinge_y, 0.0])
        tip_pt = hinge_pt + np.array([side * lower_len * np.sin(ang), -lower_len * np.cos(ang), 0.0])

        upper_seg = Line(top_pt, hinge_pt, color=col, stroke_width=rod_w * 58)
        upper_seg.set_cap_style(CapStyleType.ROUND)
        lower_seg = Line(hinge_pt, tip_pt, color=col, stroke_width=rod_w * 58)
        lower_seg.set_cap_style(CapStyleType.ROUND)
        joint = Dot(hinge_pt, radius=rod_w * 0.48, color=col)
        g.add(upper_seg, lower_seg, joint)

    if zip_t > 0.35:
        op = np.clip((zip_t - 0.35) / 0.55, 0.0, 1.0)
        n_dots = max(3, min(5, int(upper_len * 2.8)))
        for k in range(n_dots):
            ly = hinge_y + (k + 0.9) * (upper_len / (n_dots + 0.8))
            dot = Dot([cx, ly, 0], radius=0.07, color=TEXT).set_opacity(op)
            g.add(dot)
    return g


def build_pairing_grid(labels, cols, cell_w=1.24, cell_h=0.94, top_left=(-5.7, 2.55),
                       dim_fos_fos=False, show_names=False):
    """Build an N x N upper-triangle pairing grid with row & column headers."""
    n = len(labels)
    x0, y0 = top_left
    g = VGroup()
    col_heads, row_heads = VGroup(), VGroup()
    cells = {}

    for j, (lab, col) in enumerate(zip(labels, cols)):
        ch = boxed_label(lab, col, size=26, box=(cell_w - 0.14, 0.54))
        ch.move_to([x0 + (j + 1) * cell_w, y0, 0])
        col_heads.add(ch)

    for i, (lab, col) in enumerate(zip(labels, cols)):
        rh = boxed_label(lab, col, size=26, box=(0.98, cell_h - 0.16))
        rh.move_to([x0, y0 - (i + 1) * cell_h + 0.12, 0])
        row_heads.add(rh)

    for r in range(n):
        for c in range(r, n):
            cx = x0 + (c + 1) * cell_w
            cy = y0 - (r + 1) * cell_h + 0.12
            is_ff = dim_fos_fos and labels[r].startswith("F") and labels[c].startswith("F")
            stroke_col = GREY if is_ff else (cols[r] if cols[r] == cols[c] else TEXT)
            box = RoundedRectangle(
                corner_radius=0.1, width=cell_w - 0.12, height=cell_h - 0.14,
                stroke_color=stroke_col, stroke_width=2.5,
                fill_color=NUCLEUS, fill_opacity=0.88 if not is_ff else 0.40
            ).move_to([cx, cy, 0])

            if is_ff:
                mark = T("×", 30, RED)
            elif show_names:
                mark = T(f"{labels[r]}–{labels[c]}", 24, TEXT)
            else:
                mark = T("?", 28, GOLD)
            mark.move_to(box)
            cell = VGroup(box, mark)
            cell.box = box
            cell.mark = mark
            cell.is_ff = is_ff
            cell.pair_name = f"{labels[r]}–{labels[c]}"
            cells[(r, c)] = cell
            g.add(cell)

    g.add(col_heads, row_heads)
    return {"group": g, "cells": cells, "col_heads": col_heads, "row_heads": row_heads}


def build_2j2f_grid(dim_ff=True, show_q=True):
    """Shared 2 Jun + 2 Fos 4x4 upper-triangle grid for s05, s06_pause, and s07."""
    labels = ["J1", "J2", "F1", "F2"]
    cols = [JUN_COL, JUN_COL, FOS_COL, FOS_COL]
    return build_pairing_grid(
        labels, cols, cell_w=1.24, cell_h=0.94,
        top_left=(-5.7, 2.55), dim_fos_fos=dim_ff, show_names=not show_q
    )


def build_neuron(center, stained=False):
    """Schematic neuron with branching dendrites, axon, and nucleus."""
    cx, cy = center[0], center[1]
    soma_col = FOS_COL if stained else MEMBRANE
    nuc_col = FOS_COL if stained else NUCLEUS
    nuc_edge = FOS_COL if stained else MEMBRANE
    soma = Circle(radius=0.38, fill_color=CYTOSOL, fill_opacity=0.95,
                  stroke_color=soma_col, stroke_width=3.5).move_to([cx, cy, 0])
    nuc = Circle(radius=0.18, fill_color=nuc_col, fill_opacity=0.92 if stained else 0.70,
                 stroke_color=nuc_edge, stroke_width=2.5).move_to([cx, cy, 0])
    branches = VGroup()
    for ang in (0.55, 1.35, 2.15, 2.85):
        p0 = np.array([cx + 0.38 * np.cos(ang), cy + 0.38 * np.sin(ang), 0.0])
        p1 = p0 + np.array([0.36 * np.cos(ang), 0.36 * np.sin(ang), 0.0])
        branches.add(Line(p0, p1, color=soma_col, stroke_width=3))
    axon = Line([cx, cy - 0.38, 0], [cx, cy - 0.92, 0], color=soma_col, stroke_width=3.5)
    return VGroup(branches, axon, soma, nuc), nuc


# ==============================================================================
# SCENES
# ==============================================================================
class S00Title(TitleCard):
    LESSON = "Signaling to the Nucleus: CREB, AP-1 and Immediate Early Genes"
    TITLE = "Pairing Up to Launch the Second Wave"


class S01BridgeHook(SpokenScene):
    def construct(self):
        world = build_cell_world(y_mem=1.65, y_nuc=-0.10, y_bot=-2.95, x_half=6.1, pore_half=1.25,
                                 dna_y=-2.05, dna_w=8.4)
        creb = make_bzip_pair(cx=-2.2, dna_y=-2.05, left_col=CREB_COL, right_col=CREB_COL,
                              zip_t=1.0, grip_t=1.0, rod_w=0.18, upper_len=0.70, lower_len=0.58)
        creb_lbl = T("CREB", 26, CREB_COL).next_to(creb, LEFT, buff=0.22).shift(DOWN * 0.25)

        phos = make_phos_badge(center=[-2.2, 0.95, 0])
        nfat = boxed_label("NFAT", NFAT_COL, size=26, box=(1.25, 0.54)).move_to([0.0, 0.95, 0])

        # Schematic clock at top-right with filling sector + sweeping needle
        clk_c = np.array([5.10, 2.75, 0.0])
        clk_ring = Circle(radius=0.68, stroke_color=TEXT, stroke_width=3.5, fill_color=NUCLEUS, fill_opacity=0.88).move_to(clk_c)
        sweep_tr = ValueTracker(0.02)
        sector = always_redraw(lambda: Sector(
            radius=0.62, start_angle=PI / 2, angle=-sweep_tr.get_value() * TAU,
            arc_center=clk_c, fill_color=TEAL, fill_opacity=0.60, stroke_width=0
        ))
        needle = always_redraw(lambda: Line(
            clk_c,
            clk_c + 0.52 * np.array([np.cos(PI / 2 - sweep_tr.get_value() * TAU),
                                     np.sin(PI / 2 - sweep_tr.get_value() * TAU), 0.0]),
            color=GOLD, stroke_width=5
        ))
        clk_dot = Dot(clk_c, radius=0.06, color=GOLD)
        min_lbl = T("minutes", 24, MRNA_COL).move_to([3.55, 3.05, 0])
        hr_lbl = T("hours", 24, FOS_COL).move_to([3.55, 2.45, 0])
        clk_grp = VGroup(clk_ring, sector, needle, clk_dot, min_lbl)

        self.add(world, creb, creb_lbl, phos, nfat, clk_grp, scope_tag("schematic"))
        self.play(phos.animate.shift(DOWN * 0.28), nfat.animate.shift(DOWN * 0.28),
                  sweep_tr.animate.set_value(0.10), run_time=1.3, rate_func=linear)

        # Beat 1: signals flipped pre-made factors -> P onto CREB, NFAT through pore onto DNA
        self.at("signals flipped")
        self.play(
            phos.animate.move_to(creb.get_top() + UP * 0.24),
            nfat.animate.move_to([0.0, -0.10, 0]),
            sweep_tr.animate.set_value(0.22),
            run_time=0.85,
        )
        self.play(nfat.animate.move_to([2.45, -1.62, 0]),
                  sweep_tr.animate.set_value(0.32), run_time=0.85)

        # Beat 2: launch genes in minutes -> mint mRNA grows steadily
        self.at("launch genes in minutes")
        mrna_tr = ValueTracker(0.04)
        mrna1 = always_redraw(lambda: make_mrna_ribbon([-1.25, -1.95, 0], [0.55, -0.75, 0], amp=0.11, waves=2.8, frac=mrna_tr.get_value()))
        mrna2 = always_redraw(lambda: make_mrna_ribbon([-1.05, -1.95, 0], [0.85, -1.25, 0], amp=0.09, waves=2.4, frac=mrna_tr.get_value()))
        mrna_lbl = T("mRNA", 26, MRNA_COL).move_to([1.05, -0.55, 0])
        self.add(mrna1, mrna2)
        self.play(mrna_tr.animate.set_value(0.55), FadeIn(mrna_lbl),
                  sweep_tr.animate.set_value(0.45), run_time=2.0, rate_func=linear)

        # Beat 3: opening question appears cleanly at top-left while mRNA + clock sweep
        self.at("How does a cell")
        q1 = fit_text("1. Many DNA switches from few genes?", max_w=7.4, size=28, color=GOLD).move_to([-2.0, 3.05, 0])
        q2 = fit_text("2. Stretch a brief signal into hours?", max_w=7.4, size=28, color=GOLD).move_to([-2.0, 2.45, 0])
        self.play(FadeIn(q1, shift=DOWN * 0.1), mrna_tr.animate.set_value(0.75), run_time=0.65)
        self.play(mrna_tr.animate.set_value(1.0), sweep_tr.animate.set_value(0.72),
                  run_time=3.5, rate_func=linear)

        # Beat 4: stretch a brief signal into hours
        self.at("stretch a brief signal")
        self.play(FadeIn(q2, shift=DOWN * 0.1), FadeIn(hr_lbl), run_time=0.55)
        self.play(sweep_tr.animate.set_value(0.95), run_time=1.8, rate_func=linear)
        self.finish()


class S02BzipStructure(SpokenScene):
    def construct(self):
        nuc_bg = RoundedRectangle(corner_radius=0.3, width=13.4, height=7.4,
                                  fill_color=NUCLEUS, fill_opacity=0.85, stroke_width=0)
        dna_y = -2.25
        dna = make_dna_bar(width=10.8, y=dna_y, slots=[(-0.75, 1.15, CREB_COL), (0.75, 1.15, CREB_COL)])
        dna_lbl = T("DNA", 28, DNA_COL).next_to(dna, LEFT, buff=0.18)

        zip_tr = ValueTracker(0.0)
        grip_tr = ValueTracker(0.0)
        lift_tr = ValueTracker(0.55)
        single_x = ValueTracker(-2.4)
        upper_len, lower_len = 2.05, 1.45

        def build_single():
            sx = single_x.get_value()
            hinge_y = dna_y + lower_len * 1.07 + lift_tr.get_value()
            top_p = np.array([sx, hinge_y + upper_len, 0.0])
            hinge_p = np.array([sx, hinge_y, 0.0])
            tip_p = hinge_p + DOWN * lower_len
            s1 = Line(top_p, hinge_p, color=CREB_COL, stroke_width=18)
            s1.set_cap_style(CapStyleType.ROUND)
            s2 = Line(hinge_p, tip_p, color=CREB_COL, stroke_width=18)
            s2.set_cap_style(CapStyleType.ROUND)
            return VGroup(s1, s2)

        single_rod = always_redraw(build_single)
        head = T("CREB (bZIP family)", 32, CREB_COL).move_to([0, 3.20, 0])

        self.add(nuc_bg, dna, dna_lbl, single_rod)
        self.play(single_x.animate.set_value(-0.9), lift_tr.animate.set_value(0.25), run_time=1.8)

        # Beat 1: basic leucine zipper, or bZIP, family, including CREB
        self.at("basic")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.55)
        self.play(single_x.animate.set_value(1.5), lift_tr.animate.set_value(0.45), run_time=2.8)
        self.play(single_x.animate.set_value(0.0), lift_tr.animate.set_value(0.20), run_time=2.7)

        # Beat 2: cannot grip DNA well alone -> dips and slides/bounces off
        self.at("cannot grip")
        alone_lbl = T("alone: weak grip", 28, RED).move_to([3.7, 0.55, 0])
        self.play(lift_tr.animate.set_value(0.02), single_x.animate.set_value(-0.65), run_time=0.6)
        self.play(lift_tr.animate.set_value(0.65), single_x.animate.set_value(0.0),
                  FadeIn(alone_lbl), run_time=1.1, rate_func=smooth)

        # Beat 3: works as a pair -> second rod slides in
        self.at("works as a pair")
        pair_mob = always_redraw(lambda: make_bzip_pair(
            cx=0.0, dna_y=dna_y, left_col=CREB_COL, right_col=CREB_COL,
            zip_t=zip_tr.get_value(), grip_t=grip_tr.get_value(), lift=lift_tr.get_value(),
            rod_w=0.31, upper_len=upper_len, lower_len=lower_len
        ))
        self.remove(single_rod)
        self.add(pair_mob)
        self.play(FadeOut(alone_lbl), lift_tr.animate.set_value(0.42), run_time=0.9)

        # Beat 4: Two helices zip along a stripe of leucines
        self.at("Two helices zip")
        zip_y0 = 0.63 + lift_tr.get_value()
        zip_lbl = T("Leucine zipper", 30, TEXT).move_to([2.25, zip_y0, 0], aligned_edge=LEFT)
        zip_arrow = Arrow([2.10, zip_y0, 0], [0.55, zip_y0, 0], color=TEXT, buff=0.0, stroke_width=3)
        self.play(zip_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.play(FadeIn(zip_lbl), GrowArrow(zip_arrow), run_time=0.6)
        zip_lbl.add_updater(lambda m: m.set_y(0.63 + lift_tr.get_value()))
        zip_arrow.add_updater(lambda m: m.set_y(0.63 + lift_tr.get_value()))

        # Beat 5: Below that zipper, positively charged tips
        self.at("Below that zipper")
        tips_lbl = T("Basic tips (+)", 30, GOLD).move_to([2.25, -0.35, 0], aligned_edge=LEFT)
        plus_l = T("+", 28, GOLD, weight=BOLD).move_to([-0.55, -0.75, 0])
        plus_r = T("+", 28, GOLD, weight=BOLD).move_to([0.55, -0.75, 0])
        self.play(FadeIn(tips_lbl), FadeIn(plus_l), FadeIn(plus_r),
                  grip_tr.animate.set_value(0.18), lift_tr.animate.set_value(0.28), run_time=1.5)

        # Beat 6: drawn to negatively charged DNA
        self.at("drawn to negatively charged")
        minus_marks = VGroup(
            T("−", 28, RED, weight=BOLD).move_to([-0.75, dna_y - 0.44, 0]),
            T("−", 28, RED, weight=BOLD).move_to([0.75, dna_y - 0.44, 0]),
        )
        dna_charge_lbl = T("DNA (−)", 28, RED).move_to([-3.6, dna_y - 0.45, 0])
        self.play(FadeIn(minus_marks), FadeIn(dna_charge_lbl),
                  grip_tr.animate.set_value(0.32), lift_tr.animate.set_value(0.18), run_time=1.8)

        # Beat 7: part like chopsticks to grip two half-sites
        self.at("part like chopsticks")
        hs_lbl = T("two half-sites", 28, CREB_COL).move_to([0.0, dna_y - 0.85, 0])
        self.play(
            grip_tr.animate.set_value(1.0),
            lift_tr.animate.set_value(0.02),
            plus_l.animate.move_to([-1.05, dna_y + 0.55, 0]),
            plus_r.animate.move_to([1.05, dna_y + 0.55, 0]),
            FadeIn(hs_lbl),
            run_time=2.2,
            rate_func=smooth,
        )
        self.finish()


class S03FreeMath(SpokenScene):
    def construct(self):
        dna_y = -2.45
        dna_bg = RoundedRectangle(corner_radius=0.22, width=5.9, height=3.15,
                                  fill_color=NUCLEUS, fill_opacity=0.85,
                                  stroke_color=NUC_EDGE, stroke_width=2.5).move_to([3.3, -1.78, 0])
        dna = make_dna_bar(width=5.2, y=dna_y, slots=[(-0.52, 0.85, GENERIC_A), (0.52, 0.85, GENERIC_A)])
        dna.move_to([3.3, dna_y, 0])

        # Dynamic pair using ValueTrackers so partner swap visibly slides rods horizontally
        pair_aa = make_bzip_pair(cx=3.3, dna_y=dna_y, left_col=GENERIC_A, right_col=GENERIC_A,
                                 zip_t=1.0, grip_t=1.0, rod_w=0.20, upper_len=0.82, lower_len=0.64)
        pair_lbl = T("A–A  ->  site 1", 28, GENERIC_A).move_to([3.3, dna_y - 0.62, 0])

        grid = build_pairing_grid(
            ["A", "B", "C"], [GENERIC_A, GENERIC_B, GENERIC_C],
            cell_w=1.44, cell_h=1.08, top_left=(-5.6, 2.35),
            dim_fos_fos=False, show_names=True
        )
        for cell in grid["cells"].values():
            cell.box.set_fill(opacity=0.28)
            cell.mark.set_opacity(0.0)

        formula = M("Pairs = n(n + 1) ÷ 2", 30, GOLD).move_to([3.3, 2.85, 0])
        cnt_tr = ValueTracker(0)
        cnt_lbl = counter("pairs = {:.0f}", cnt_tr, at=[3.3, 1.45, 0], size=28, color=TEXT)

        self.add(dna_bg, dna, pair_aa, pair_lbl, grid["group"])
        self.play(pair_aa.animate.shift(LEFT * 0.45), run_time=1.8, rate_func=there_and_back)

        # Beat 1: swapping one partner changes which DNA site the pair prefers
        self.at("swapping one partner")
        pair_ab = make_bzip_pair(cx=4.1, dna_y=dna_y, left_col=GENERIC_A, right_col=GENERIC_B,
                                 zip_t=1.0, grip_t=1.0, lift=0.22, rod_w=0.20, upper_len=0.82, lower_len=0.64)
        pair_lbl_ab = T("A–B  ->  site 2", 28, GENERIC_B).move_to([3.3, dna_y - 0.62, 0])
        dna_b = make_dna_bar(width=5.2, y=dna_y, slots=[(0.28, 0.85, GENERIC_A), (1.32, 0.85, GENERIC_B)])
        dna_b.move_to([3.3, dna_y, 0])
        self.play(
            ReplacementTransform(pair_aa, pair_ab),
            ReplacementTransform(dna, dna_b),
            swap(pair_lbl, pair_lbl_ab, run_time=0.8),
            run_time=1.8,
        )
        self.play(pair_ab.animate.shift(DOWN * 0.22), run_time=2.5)

        # Beat 2: With n proteins that all pair freely
        self.at("With N proteins")
        self.play(FadeIn(formula), run_time=0.7)
        # Show duplicate lower-triangle cells sliding onto upper-triangle partners to illustrate ÷ 2
        dup_pairs = [
            ((1, 0), (0, 1)),
            ((2, 0), (0, 2)),
            ((2, 1), (1, 2)),
        ]
        dup_cells = VGroup()
        targets = []
        for (r, c), (tr, tc) in dup_pairs:
            cx = -5.6 + (c + 1) * 1.44
            cy = 2.35 - (r + 1) * 1.08 + 0.12
            b = RoundedRectangle(corner_radius=0.1, width=1.32, height=0.94,
                                 stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.35).move_to([cx, cy, 0])
            dup_cells.add(b)
            targets.append(grid["cells"][(tr, tc)].box.get_center())
        self.play(FadeIn(dup_cells), run_time=1.2)
        self.play(*[b.animate.move_to(pos).set_opacity(0.0) for b, pos in zip(dup_cells, targets)],
                  *[c.box.animate.set_fill(TEAL, opacity=0.35) for c in grid["cells"].values()],
                  run_time=3.5)
        self.remove(dup_cells)

        # Beat 3: same-partner pairs on diagonal
        self.at("That counts same")
        diag = [grid["cells"][(i, i)] for i in range(3)]
        self.play(*[c.box.animate.set_fill(GENERIC_A, opacity=0.45) for c in diag],
                  *[c.mark.animate.set_opacity(1.0) for c in diag],
                  run_time=1.2)

        # Beat 4: plus mixed pairs
        self.at("plus mixed pairs")
        mixed = [grid["cells"][(0, 1)], grid["cells"][(0, 2)], grid["cells"][(1, 2)]]
        self.play(*[c.box.animate.set_fill(GENERIC_C, opacity=0.45) for c in mixed],
                  *[c.mark.animate.set_opacity(1.0) for c in mixed],
                  run_time=1.2)

        # Beat 5: Take three proteins -> show n = 3
        self.at("Take three proteins")
        n_line = M("n = 3", 28, TEXT).move_to([3.3, 2.10, 0])
        self.play(FadeIn(n_line), run_time=0.6)

        # Beat 6: 3 times 4 is 12
        self.at("3 times 4")
        step1 = M("3 × 4 = 12", 28, TEAL).move_to([3.3, 0.80, 0])
        self.play(FadeIn(step1), run_time=0.9)

        # Beat 7: divided by 2 gives 6 distinct pairs -> step through 6 cells + live counter
        self.at("divided by 2 gives")
        self.play(FadeIn(cnt_lbl), run_time=0.15)
        order = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
        for k, key in enumerate(order, 1):
            c = grid["cells"][key]
            self.play(c.box.animate.set_stroke(GOLD, width=4.5).set_fill(GOLD, opacity=0.28),
                      cnt_tr.animate.set_value(k), run_time=0.18)
        self.at("gives 6")
        step2 = M("12 ÷ 2 = 6 pairs", 30, GOLD).move_to([3.3, 0.15, 0])
        self.play(FadeIn(step2), *[c.box.animate.set_fill(GOLD, opacity=0.38) for c in grid["cells"].values()],
                  run_time=0.5)
        self.finish()


class S04FosJunRule(SpokenScene):
    def construct(self):
        nuc_bg = RoundedRectangle(corner_radius=0.3, width=13.4, height=7.4,
                                  fill_color=NUCLEUS, fill_opacity=0.85, stroke_width=0)
        dna_y = -2.25
        dna = make_dna_bar(width=11.8, y=dna_y, slots=[(-4.0, 1.5, JUN_COL), (0.0, 1.5, FOS_COL)])
        head = T("AP-1 partner rule", 34, TEXT).move_to([0, 3.15, 0])

        jj_zip, jj_grip, jj_lift = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.65)
        fj_zip, fj_grip, fj_lift = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.65)
        ff_sep = ValueTracker(1.25)

        jj_pair = always_redraw(lambda: make_bzip_pair(
            cx=-4.0, dna_y=dna_y, left_col=JUN_COL, right_col=JUN_COL,
            zip_t=jj_zip.get_value(), grip_t=jj_grip.get_value(), lift=jj_lift.get_value(),
            rod_w=0.25, upper_len=1.55, lower_len=1.10
        ))
        fj_pair = always_redraw(lambda: make_bzip_pair(
            cx=0.0, dna_y=dna_y, left_col=FOS_COL, right_col=JUN_COL,
            zip_t=fj_zip.get_value(), grip_t=fj_grip.get_value(), lift=fj_lift.get_value(),
            rod_w=0.25, upper_len=1.55, lower_len=1.10
        ))

        def build_ff():
            sep = ff_sep.get_value()
            hinge_y = dna_y + 1.10 * 1.07 + 0.65
            g = VGroup()
            for side in (-1, 1):
                hx = 4.0 + side * sep
                top_p = [hx, hinge_y + 1.55, 0]
                bot_p = [hx, hinge_y - 1.10, 0]
                rod = Line(top_p, bot_p, color=FOS_COL, stroke_width=15)
                rod.set_cap_style(CapStyleType.ROUND)
                g.add(rod)
            return g

        ff_pair = always_redraw(build_ff)
        jj_lbl = T("Jun–Jun", 28, JUN_COL).move_to([-4.0, 2.45, 0])
        fj_lbl = T("Fos–Jun (AP-1)", 28, FOS_COL).move_to([0.0, 2.45, 0])
        ff_lbl = T("Fos–Fos", 28, FOS_COL).move_to([4.0, 2.45, 0])

        self.add(nuc_bg, dna, jj_pair, fj_pair, ff_pair)
        self.play(jj_lift.animate.set_value(0.38), fj_lift.animate.set_value(0.38),
                  ff_sep.animate.set_value(0.95), run_time=3.5)

        # Beat 1: Two bZIP families, Jun and Fos, build AP-1
        self.at("build the factor")
        self.play(FadeIn(head), FadeIn(jj_lbl), FadeIn(fj_lbl), FadeIn(ff_lbl), run_time=1.3)

        # Beat 2: Jun pairs with Jun
        self.at("Jun pairs with")
        self.play(jj_zip.animate.set_value(1.0), jj_grip.animate.set_value(1.0),
                  jj_lift.animate.set_value(0.05), run_time=0.8)

        # Beat 3: or with Fos (AP-1 snaps tightly onto DNA)
        self.at("or with")
        tight_halo = RoundedRectangle(corner_radius=0.14, width=1.9, height=0.54,
                                      stroke_color=FOS_COL, stroke_width=4,
                                      fill_color=FOS_COL, fill_opacity=0.22).move_to([0.0, dna_y, 0])
        self.play(fj_zip.animate.set_value(1.0), fj_grip.animate.set_value(1.0),
                  fj_lift.animate.set_value(0.0), FadeIn(tight_halo), run_time=1.1)

        # Beat 4: Fos cannot pair stably with itself
        self.at("cannot pair stably")
        self.play(ff_sep.animate.set_value(0.62), run_time=1.3)

        # Beat 5: negatively charged residues beside its zipper
        self.at("negatively charged")
        minus_l = VGroup(*[T("−", 26, RED, weight=BOLD).move_to([3.68, dna_y + 2.05 + k * 0.45, 0]) for k in range(3)])
        minus_r = VGroup(*[T("−", 26, RED, weight=BOLD).move_to([4.32, dna_y + 2.05 + k * 0.45, 0]) for k in range(3)])
        repel_arcs = VGroup(
            ArcBetweenPoints([3.88, dna_y + 2.50, 0], [4.12, dna_y + 2.50, 0], angle=0.6, color=RED, stroke_width=3),
            ArcBetweenPoints([4.12, dna_y + 2.22, 0], [3.88, dna_y + 2.22, 0], angle=0.6, color=RED, stroke_width=3),
        )
        self.play(FadeIn(minus_l), FadeIn(minus_r), Create(repel_arcs), run_time=1.1)

        # Beat 6: repel each other -> bounce apart
        self.at("repel each other")
        unstable_lbl = T("repel (×)", 28, RED).move_to([4.0, dna_y - 0.65, 0])
        self.play(
            ff_sep.animate.set_value(1.30),
            minus_l.animate.shift(LEFT * 0.68),
            minus_r.animate.shift(RIGHT * 0.68),
            FadeOut(repel_arcs),
            FadeIn(unstable_lbl),
            run_time=1.2,
            rate_func=smooth,
        )
        self.finish()


class S05PredictPrompt(SpokenScene):
    def construct(self):
        grid = build_2j2f_grid(dim_ff=False, show_q=True)
        title = T("Partner rule check", 32, TEXT).move_to([3.35, 2.55, 0])

        rod_j1 = VGroup(Line([1.85, 1.75, 0], [1.85, -0.35, 0], color=JUN_COL, stroke_width=14).set_cap_style(CapStyleType.ROUND),
                        T("J1", 26, JUN_COL).move_to([1.85, -0.75, 0]))
        rod_j2 = VGroup(Line([2.75, 1.75, 0], [2.75, -0.35, 0], color=JUN_COL, stroke_width=14).set_cap_style(CapStyleType.ROUND),
                        T("J2", 26, JUN_COL).move_to([2.75, -0.75, 0]))
        rod_f1 = VGroup(Line([3.95, 1.75, 0], [3.95, -0.35, 0], color=FOS_COL, stroke_width=14).set_cap_style(CapStyleType.ROUND),
                        T("F1", 26, FOS_COL).move_to([3.95, -0.75, 0]))
        rod_f2 = VGroup(Line([4.85, 1.75, 0], [4.85, -0.35, 0], color=FOS_COL, stroke_width=14).set_cap_style(CapStyleType.ROUND),
                        T("F2", 26, FOS_COL).move_to([4.85, -0.75, 0]))

        # Show empty upper-triangle grid outline immediately so frame is never sparse
        empty_outline = VGroup(*[c.box.copy().set_fill(opacity=0.25) for c in grid["cells"].values()])
        self.add(title, empty_outline)
        self.play(Create(empty_outline), run_time=1.8)

        # Beat 1: Suppose a cell makes two Jun proteins
        self.at("Suppose a cell")
        j_cells = [grid["cells"][(0, 0)], grid["cells"][(0, 1)], grid["cells"][(1, 1)]]
        self.play(
            FadeIn(grid["col_heads"][0]), FadeIn(grid["col_heads"][1]),
            FadeIn(grid["row_heads"][0]), FadeIn(grid["row_heads"][1]),
            *[FadeIn(c) for c in j_cells],
            FadeIn(rod_j1, shift=UP * 0.25), FadeIn(rod_j2, shift=UP * 0.25),
            run_time=1.3,
        )

        # Beat 2: and two Fos proteins
        self.at("and two")
        rem_cells = [c for k, c in grid["cells"].items() if k not in ((0, 0), (0, 1), (1, 1))]
        self.play(
            FadeIn(grid["col_heads"][2]), FadeIn(grid["col_heads"][3]),
            FadeIn(grid["row_heads"][2]), FadeIn(grid["row_heads"][3]),
            *[FadeIn(c) for c in rem_cells],
            FadeIn(rod_f1, shift=UP * 0.25), FadeIn(rod_f2, shift=UP * 0.25),
            run_time=1.4,
        )
        self.remove(empty_outline)

        # Beat 3: Pause and predict
        self.at("Pause and predict")
        q = question_card("2 Jun + 2 Fos (no Fos–Fos) -> How many pairs?", y=BOTTOM_Y + 0.15)
        self.play(FadeIn(q.question), run_time=0.9)

        # Beat 4: pairs allowed -> dim & mark 'x' on Fos-Fos cells + show F1/F2 separation
        self.at("pairs allowed")
        ff_keys = [(2, 2), (2, 3), (3, 3)]
        anims = []
        for k in ff_keys:
            cell = grid["cells"][k]
            new_mark = T("×", 30, RED).move_to(cell.box)
            anims.append(cell.box.animate.set_stroke(GREY).set_fill(opacity=0.40))
            anims.append(swap(cell.mark, new_mark, run_time=0.7))
        no_ff = T("×", 30, RED).move_to([4.40, 0.70, 0])
        self.play(*anims, rod_f1.animate.shift(LEFT * 0.18), rod_f2.animate.shift(RIGHT * 0.18),
                  FadeIn(no_ff), run_time=1.0)

        # Beat 5: how many distinct pairs can form?
        self.at("how many distinct")
        open_boxes = [c.box for k, c in grid["cells"].items() if k not in ff_keys]
        self.play(*[b.animate.set_stroke(GOLD, width=3.5).set_fill(NUCLEUS, opacity=0.95) for b in open_boxes],
                  run_time=1.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "2 Jun + 2 Fos (no Fos–Fos) -> How many pairs?"
    SECONDS = 4.5

    def backdrop(self):
        grid = build_2j2f_grid(dim_ff=True, show_q=True)
        for k, cell in grid["cells"].items():
            if not cell.is_ff:
                pulse(cell.box, base=3.0, amp=1.5, speed=3.5)
        return grid["group"]


class S07PredictReveal(SpokenScene):
    def construct(self):
        grid = build_2j2f_grid(dim_ff=True, show_q=False)
        for k, cell in grid["cells"].items():
            if not cell.is_ff:
                cell.mark.set_opacity(0.0)
                cell.box.set_fill(opacity=0.25)

        badge = boxed_label("7 pairs", GOLD, size=34, box=(2.6, 0.78)).move_to([3.35, 2.45, 0])
        cnt_tr = ValueTracker(0)
        cnt = counter("count = {:.0f}", cnt_tr, at=[3.35, 1.55, 0], size=28, color=TEXT)

        self.add(grid["group"], badge, cnt)
        # Sweep highlight across the 7 open cells while "7 pairs" is introduced
        open_cells = [c.box for c in grid["cells"].values() if not c.is_ff]
        self.play(*[b.animate.set_fill(GOLD, opacity=0.28) for b in open_cells], run_time=1.5)
        self.play(*[b.animate.set_fill(NUCLEUS, opacity=0.25) for b in open_cells], run_time=1.5)

        # Beat 1: 2 Jun proteins make 3 Jun pairs
        self.at("proteins make")
        jj_keys = [(0, 0), (0, 1), (1, 1)]
        for idx, k in enumerate(jj_keys, 1):
            c = grid["cells"][k]
            self.play(
                c.box.animate.set_fill(JUN_COL, opacity=0.40).set_stroke(JUN_COL, width=3.5),
                c.mark.animate.set_opacity(1.0),
                cnt_tr.animate.set_value(idx),
                run_time=0.30,
            )

        # Beat 2: 2 times 3 divided by 2 is 3
        self.at("2 times 3")
        line_jj = M("Jun–Jun:  2 × 3 ÷ 2 = 3", 28, JUN_COL).move_to([3.35, 0.70, 0])
        bar_jj = RoundedRectangle(corner_radius=0.06, width=1.2, height=0.22,
                                  fill_color=JUN_COL, fill_opacity=0.85, stroke_width=0).move_to([1.6, 0.28, 0], aligned_edge=LEFT)
        self.play(FadeIn(line_jj), GrowFromEdge(bar_jj, LEFT), run_time=1.8)

        # Beat 3: 2 Fos times 2 Jun add 4 mixed pairs
        self.at("2 Fos")
        fj_keys = [(0, 2), (0, 3), (1, 2), (1, 3)]
        line_fj = M("Fos–Jun:  2 × 2 = 4", 28, FOS_COL).move_to([3.35, -0.20, 0])
        bar_fj = RoundedRectangle(corner_radius=0.06, width=1.6, height=0.22,
                                  fill_color=FOS_COL, fill_opacity=0.85, stroke_width=0).move_to([1.6, -0.62, 0], aligned_edge=LEFT)
        ff_zero = M("+ 0  (no Fos–Fos)", 26, RED).move_to([3.35, -1.08, 0])
        fj_steps = Succession(*[
            AnimationGroup(
                grid["cells"][k].box.animate.set_fill(FOS_COL, opacity=0.35).set_stroke(FOS_COL, width=3.5),
                grid["cells"][k].mark.animate.set_opacity(1.0),
                run_time=0.30,
            )
            for k in fj_keys
        ])
        self.play(
            fj_steps,
            cnt_tr.animate(run_time=1.2, rate_func=linear).set_value(7),
            FadeIn(line_fj, run_time=0.9),
            GrowFromEdge(bar_fj, LEFT, run_time=1.2),
            FadeIn(ff_zero, run_time=0.9),
        )

        # Beat 4: 3 plus 4 is 7
        self.at("3 plus 4")
        line_tot = M("Total:    3 + 4 = 7", 30, GOLD).move_to([3.35, -1.75, 0])
        bar_tot = RoundedRectangle(corner_radius=0.06, width=2.8, height=0.18,
                                   fill_color=GOLD, fill_opacity=0.85, stroke_width=0).move_to([1.6, -2.08, 0], aligned_edge=LEFT)
        self.play(FadeIn(line_tot), GrowFromEdge(bar_tot, LEFT), run_time=1.4)

        # Beat 5: 4 free proteins would make 4 times 5, over 2, or 10
        self.at("4 free proteins")
        line_free = M("If free:  4 × 5 ÷ 2 = 10", 28, TEAL).move_to([3.35, -2.50, 0])
        bar_free = RoundedRectangle(corner_radius=0.06, width=4.0, height=0.18,
                                    fill_color=TEAL, fill_opacity=0.85, stroke_width=0).move_to([1.6, -2.84, 0], aligned_edge=LEFT)
        ff_cells = [grid["cells"][(2, 2)].box, grid["cells"][(2, 3)].box, grid["cells"][(3, 3)].box]
        self.play(FadeIn(line_free), GrowFromEdge(bar_free, LEFT),
                  *[b.animate.set_stroke(TEAL, width=3.0) for b in ff_cells], run_time=2.5)
        self.finish()


class S08SitesAndCfos(SpokenScene):
    def construct(self):
        nuc_bg = RoundedRectangle(corner_radius=0.3, width=13.4, height=7.4,
                                  fill_color=NUCLEUS, fill_opacity=0.85, stroke_width=0)
        dna_y = -1.65
        dna = make_dna_bar(width=11.6, y=dna_y)

        slots_jj = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=0.28, height=0.34,
                             stroke_color=JUN_COL, stroke_width=2.5, fill_color=JUN_COL, fill_opacity=0.20)
            for _ in range(7)
        ]).arrange(RIGHT, buff=0.06).move_to([-4.0, dna_y, 0])

        slots_fj = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=0.28, height=0.34,
                             stroke_color=FOS_COL, stroke_width=3, fill_color=FOS_COL, fill_opacity=0.28)
            for _ in range(7)
        ]).arrange(RIGHT, buff=0.06).move_to([0.0, dna_y, 0])

        slots_cr = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=0.28, height=0.34,
                             stroke_color=CREB_COL, stroke_width=3, fill_color=CREB_COL, fill_opacity=0.28)
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.06).move_to([4.0, dna_y, 0])

        jj_lift = ValueTracker(0.45)
        fj_lift = ValueTracker(0.45)
        jj_cx = ValueTracker(-4.0)
        jj_pair = always_redraw(lambda: make_bzip_pair(
            cx=jj_cx.get_value(), dna_y=dna_y, left_col=JUN_COL, right_col=JUN_COL,
            zip_t=1.0, grip_t=1.0, lift=jj_lift.get_value(), rod_w=0.22, upper_len=1.40, lower_len=1.05
        ))
        fj_pair = always_redraw(lambda: make_bzip_pair(
            cx=0.0, dna_y=dna_y, left_col=FOS_COL, right_col=JUN_COL,
            zip_t=1.0, grip_t=1.0, lift=fj_lift.get_value(), rod_w=0.22, upper_len=1.40, lower_len=1.05
        ))
        cr_pair = make_bzip_pair(
            cx=4.0, dna_y=dna_y, left_col=CREB_COL, right_col=CREB_COL,
            zip_t=1.0, grip_t=1.0, lift=0.0, rod_w=0.22, upper_len=1.40, lower_len=1.05
        )

        jj_lbl = T("Jun–Jun", 28, JUN_COL).move_to([-4.0, 2.55, 0])
        fj_lbl = T("Fos–Jun", 28, FOS_COL).move_to([0.0, 2.55, 0])
        cr_lbl = T("CREB", 28, CREB_COL).move_to([4.0, 2.55, 0])

        part1 = VGroup(nuc_bg, dna, slots_jj, slots_fj, slots_cr, jj_pair, fj_pair, cr_pair, jj_lbl, fj_lbl, cr_lbl)
        self.add(part1)
        self.play(jj_lift.animate.set_value(0.22), fj_lift.animate.set_value(0.22), run_time=2.5)

        # Beat 1: Fos-Jun holds DNA more tightly than Jun-Jun
        self.at("holds DNA")
        fj_glow = RoundedRectangle(corner_radius=0.14, width=2.7, height=0.52,
                                   stroke_color=FOS_COL, stroke_width=4,
                                   fill_color=FOS_COL, fill_opacity=0.25).move_to([0.0, dna_y, 0])
        grip_jj = T("looser grip", 26, JUN_COL).move_to([-4.0, dna_y - 0.65, 0])
        grip_fj = T("tighter grip", 26, FOS_COL).move_to([0.0, dna_y - 0.65, 0])
        self.play(
            jj_lift.animate.set_value(0.18),
            fj_lift.animate.set_value(0.0),
            FadeIn(fj_glow),
            FadeIn(grip_jj),
            FadeIn(grip_fj),
            run_time=1.3,
        )
        self.play(jj_cx.animate.set_value(-3.75), jj_lift.animate.set_value(0.32), run_time=0.8)
        self.play(jj_cx.animate.set_value(-4.0), jj_lift.animate.set_value(0.18), run_time=0.8)

        # Beat 2: prefers a seven-letter DNA site
        self.at("prefers a seven")
        lbl_7 = T("7 letters", 28, FOS_COL).move_to([0.0, dna_y - 1.25, 0])
        for s in slots_fj:
            self.play(s.animate.set_fill(opacity=0.85), run_time=0.18)
        self.play(FadeIn(lbl_7), run_time=0.5)

        # Beat 3: one letter shorter than CREB's eight-letter site
        self.at("one letter shorter")
        lbl_8 = T("8 letters", 28, CREB_COL).move_to([4.0, dna_y - 1.25, 0])
        for s in slots_cr:
            self.play(s.animate.set_fill(opacity=0.85), run_time=0.18)
        self.play(FadeIn(lbl_8), run_time=0.6)

        # Beat 4: Back to the first film's gene, c-fos
        self.at("Back to the first")
        world = build_cell_world(y_mem=2.15, y_nuc=-0.10, y_bot=-2.95, x_half=6.1, pore_half=1.25,
                                 dna_y=-2.05, dna_w=8.4)
        creb_cell = make_bzip_pair(cx=-2.2, dna_y=-2.05, left_col=CREB_COL, right_col=CREB_COL,
                                   zip_t=1.0, grip_t=1.0, rod_w=0.18, upper_len=0.68, lower_len=0.58)
        phos_cell = make_phos_badge(center=creb_cell.get_top() + UP * 0.22)
        cfos_gene_lbl = T("c-fos gene", 28, MRNA_COL).move_to([1.2, -2.55, 0])

        part1_all = VGroup(part1, fj_glow, grip_jj, grip_fj, lbl_7, lbl_8)
        self.play(
            FadeOut(part1_all),
            FadeIn(world),
            FadeIn(creb_cell),
            FadeIn(phos_cell),
            FadeIn(cfos_gene_lbl),
            run_time=1.5,
        )

        # Beat 5: Pre-made factors switch on c-fos transcripts within minutes
        self.at("switch on")
        mrna_tr = ValueTracker(0.03)
        r1 = always_redraw(lambda: make_mrna_ribbon([-0.8, -1.9, 0], [1.6, -0.45, 0], amp=0.12, waves=3.0, frac=mrna_tr.get_value()))
        r2 = always_redraw(lambda: make_mrna_ribbon([-0.5, -1.9, 0], [2.4, -0.85, 0], amp=0.12, waves=3.5, frac=mrna_tr.get_value()))
        r3 = always_redraw(lambda: make_mrna_ribbon([-0.2, -1.9, 0], [0.2, 0.75, 0], amp=0.10, waves=3.0, frac=mrna_tr.get_value()))
        mrna_lbl = T("c-fos mRNA (minutes)", 28, MRNA_COL).move_to([2.6, 0.85, 0])
        self.add(r1, r2, r3)
        self.play(FadeIn(mrna_lbl), mrna_tr.animate.set_value(0.15), run_time=0.6, rate_func=linear)
        self.play(mrna_tr.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


class S09Ap1AndNfat(SpokenScene):
    def construct(self):
        world = build_cell_world(y_mem=2.25, y_nuc=-0.05, y_bot=-2.95, x_half=6.1, pore_half=1.25,
                                 dna_y=-2.05, dna_w=8.4)
        il2_slot = RoundedRectangle(corner_radius=0.08, width=3.6, height=0.34,
                                    stroke_color=NFAT_COL, stroke_width=3,
                                    fill_color=NFAT_COL, fill_opacity=0.22).move_to([0.85, -2.05, 0])
        il2_lbl = T("IL-2 site", 28, TEXT).move_to([0.85, -2.60, 0])

        mrna_cyto = make_mrna_ribbon([-3.9, 1.10, 0], [-0.5, 1.10, 0], amp=0.10, waves=4.0)
        mrna_lbl = T("c-fos mRNA", 26, MRNA_COL).move_to([-2.4, 1.68, 0])
        ribo_x = ValueTracker(-3.4)
        ribo = always_redraw(lambda: VGroup(
            Ellipse(width=0.68, height=0.38, fill_color=TEXT, fill_opacity=0.88, stroke_width=0).move_to([ribo_x.get_value(), 1.30, 0]),
            Ellipse(width=0.54, height=0.30, fill_color=TEXT, fill_opacity=0.68, stroke_width=0).move_to([ribo_x.get_value(), 0.90, 0]),
        ))
        ribo_lbl = T("ribosome", 24, TEXT).move_to([-3.2, 0.45, 0])

        jun_rod = Line([-0.65, -0.55, 0], [-0.65, -1.75, 0], color=JUN_COL, stroke_width=13)
        jun_rod.set_cap_style(CapStyleType.ROUND)
        jun_lbl = T("Jun", 26, JUN_COL).next_to(jun_rod, LEFT, buff=0.20)

        self.add(world, mrna_cyto, mrna_lbl, ribo, ribo_lbl, jun_rod, jun_lbl)
        self.play(ribo_x.animate.set_value(-2.3), run_time=1.8)

        # Beat 1: ribosomes running -> build new Fos protein
        self.at("build new")
        fos_cyto = Line([-1.25, 1.25, 0], [-1.25, 1.15, 0], color=FOS_COL, stroke_width=13)
        fos_cyto.set_cap_style(CapStyleType.ROUND)
        fos_lbl = T("Fos", 26, FOS_COL).move_to([-0.55, 1.55, 0])
        self.play(ribo_x.animate.set_value(-1.25), run_time=1.0)
        fos_full = Line([-1.25, 1.75, 0], [-1.25, 0.55, 0], color=FOS_COL, stroke_width=13)
        fos_full.set_cap_style(CapStyleType.ROUND)
        self.play(Transform(fos_cyto, fos_full), FadeIn(fos_lbl), run_time=1.1)

        # Beat 2: Fos enters the nucleus
        self.at("enters the nucleus")
        self.play(FadeOut(fos_lbl), fos_cyto.animate.move_to([-0.25, -0.15, 0]), run_time=0.75)
        self.play(fos_cyto.animate.move_to([0.05, -1.15, 0]), run_time=0.55)

        # Beat 3: zips with Jun to form AP-1
        self.at("zips with Jun")
        ap1_zip = ValueTracker(0.72)
        ap1_pair = always_redraw(lambda: make_bzip_pair(
            cx=-0.35, dna_y=-2.05, left_col=JUN_COL, right_col=FOS_COL,
            zip_t=ap1_zip.get_value(),
            grip_t=np.clip((ap1_zip.get_value() - 0.72) / 0.28, 0.0, 1.0),
            lift=0.17 * (1.0 - np.clip((ap1_zip.get_value() - 0.72) / 0.28, 0.0, 1.0)),
            rod_w=0.18, upper_len=0.75, lower_len=0.62
        ))
        self.remove(fos_cyto, jun_rod, jun_lbl)
        self.add(ap1_pair)
        ap1_lbl = T("AP-1", 28, FOS_COL).move_to([-2.15, -1.25, 0])
        self.play(ap1_zip.animate.set_value(1.0), run_time=1.0)
        self.play(FadeIn(ap1_lbl), run_time=0.4)

        # Beat 4: On immune genes like interleukin-2
        self.at("On immune genes")
        nfat_box = boxed_label("NFAT", NFAT_COL, size=26, box=(1.28, 0.54)).move_to([3.3, 1.55, 0])
        self.play(FadeIn(il2_slot), FadeIn(il2_lbl), FadeIn(nfat_box), run_time=1.3)
        self.play(nfat_box.animate.move_to([0.8, 0.75, 0]),
                  il2_slot.animate.set_stroke(GOLD, width=5).set_fill(NFAT_COL, opacity=0.32), run_time=1.8)

        # Beat 5: AP-1 sits beside NFAT from the first film
        self.at("sits beside")
        self.play(nfat_box.animate.move_to([0.45, -0.10, 0]), run_time=1.2)
        self.play(nfat_box.animate.move_to([1.95, -1.55, 0]), run_time=1.6)

        # Beat 6: Two pathways then meet at one DNA site
        self.at("Two pathways")
        arr_ap1 = Arrow([-1.6, 0.45, 0], [-0.75, -0.80, 0], color=FOS_COL, stroke_width=5, buff=0.0)
        arr_nfat = Arrow([3.2, 0.85, 0], [2.25, -1.05, 0], color=NFAT_COL, stroke_width=5, buff=0.0)
        meet_lbl = T("2 pathways -> 1 site", 28, GOLD).move_to([3.55, 1.35, 0])
        p_dot1 = Dot([-1.6, 0.45, 0], radius=0.11, color=FOS_COL)
        p_dot2 = Dot([3.2, 0.85, 0], radius=0.11, color=NFAT_COL)
        self.play(GrowArrow(arr_ap1), GrowArrow(arr_nfat), FadeIn(meet_lbl), run_time=1.2)
        self.add(p_dot1, p_dot2)
        self.play(p_dot1.animate.move_to([-0.75, -0.80, 0]),
                  p_dot2.animate.move_to([2.25, -1.05, 0]), run_time=2.2)
        self.remove(p_dot1, p_dot2)
        self.finish()


class S10SecondWave(SpokenScene):
    def construct(self):
        wave1 = lambda x: 0.92 * ((x / 0.65) ** 2.2) * np.exp(2.2 * (1.0 - x / 0.65)) if x > 0 else 0.0
        wave2 = lambda x: 0.78 * (((x - 1.2) / 2.6) ** 2.0) * np.exp(2.0 * (1.0 - (x - 1.2) / 2.6)) if x > 1.2 else 0.0

        P = Plot(
            box=(-5.5, 5.5, -2.55, 0.45),
            xr=(0, 6.0), yr=(0, 1.1),
            xticks=[(0.0, "0"), (0.7, "minutes"), (3.8, "hours")],
            yticks=[(0, "0"), (0.5, "0.5"), (1.0, "1.0")],
            xlabel="time after signal",
            ylabel="gene activity (schematic)",
            color=TEXT, size=24, label_size=26,
        )
        t_tr = ValueTracker(0.0)

        def make_area(fn, x0, color):
            x1 = t_tr.get_value()
            if x1 <= x0 + 1e-3:
                return VMobject()
            xs = np.linspace(x0, x1, max(4, int(50 * (x1 - x0))))
            pts = [P.pt(x0, 0)] + [P.pt(x, fn(x)) for x in xs] + [P.pt(x1, 0)]
            return Polygon(*pts, fill_color=color, fill_opacity=0.22, stroke_width=0)

        area1 = always_redraw(lambda: make_area(wave1, 0.0, MRNA_COL))
        area2 = always_redraw(lambda: make_area(wave2, 1.2, FOS_COL))
        live1 = P.live_curve(wave1, t_tr, color=MRNA_COL, width=6)
        live2 = P.live_curve(wave2, t_tr, color=FOS_COL, width=6, x0=1.2)
        cursor = always_redraw(lambda: DashedLine(
            P.pt(t_tr.get_value(), 0),
            P.pt(t_tr.get_value(), max(wave1(t_tr.get_value()), wave2(t_tr.get_value()), 0.05)),
            color=GREY, stroke_width=2.5, dash_length=0.10
        ))
        dot1 = P.dot(lambda: min(t_tr.get_value(), 2.8), lambda: wave1(min(t_tr.get_value(), 2.8)),
                     color=MRNA_COL, ring=TEXT, radius=0.09)

        top_title = T("From minutes to hours", 32, GOLD).move_to([0.0, 3.25, 0])
        sig_chip = boxed_label("brief signal", GOLD, size=26, box=(2.3, 0.58)).move_to([-4.2, 2.1, 0])
        w1_chip = boxed_label("c-fos mRNA", MRNA_COL, size=26, box=(2.4, 0.58)).move_to([-0.4, 2.1, 0])
        ap1_chip = boxed_label("Fos + Jun = AP-1", FOS_COL, size=26, box=(3.0, 0.58)).move_to([3.7, 2.1, 0])
        a1 = Arrow(sig_chip.get_right() + RIGHT * 0.1, w1_chip.get_left() + LEFT * 0.1, color=TEXT, buff=0.0, stroke_width=3)
        a2 = Arrow(w1_chip.get_right() + RIGHT * 0.1, ap1_chip.get_left() + LEFT * 0.1, color=TEXT, buff=0.0, stroke_width=3)
        upper_strip = VGroup(top_title, sig_chip, w1_chip, ap1_chip, a1, a2)

        w1_lbl = T("First wave: c-fos", 26, MRNA_COL).move_to([-2.2, 0.15, 0])
        w2_lbl = T("Second wave: AP-1 targets", 26, FOS_COL).move_to([2.8, 0.15, 0])

        self.add(P, area1, live1, cursor, dot1, upper_strip, scope_tag("schematic"))

        # Beat 1: First wave draws live (minutes)
        self.play(FadeIn(w1_lbl), run_time=0.5)
        self.play(t_tr.animate.set_value(2.0), w1_chip.box.animate.set_stroke(MRNA_COL, width=4.5),
                  run_time=4.8, rate_func=linear)

        # Beat 2: Newly assembled AP-1 switches on later genes over hours
        self.at("Newly assembled")
        self.add(area2, live2)
        dot2 = P.dot(lambda: max(t_tr.get_value(), 1.2), lambda: wave2(max(t_tr.get_value(), 1.2)),
                     color=FOS_COL, ring=GOLD, radius=0.10)
        self.add(dot2)
        self.play(FadeIn(w2_lbl), run_time=0.5)
        self.play(t_tr.animate.set_value(4.4), ap1_chip.box.animate.set_stroke(FOS_COL, width=4.5),
                  run_time=4.2, rate_func=linear)

        # Beat 3: waits for newly made Fos and other first-wave proteins
        self.at("Because that wave")
        wait_lbl = T("waits for new Fos", 26, JUN_COL).move_to([0.75, -1.68, 0])
        self.play(FadeIn(wait_lbl), run_time=0.5)
        self.play(t_tr.animate.set_value(6.0), run_time=4.0, rate_func=linear)

        # Beat 4: a brief signal becomes a lasting program
        self.at("a brief signal")
        self.remove(cursor)
        sig_mark = P.vline(0.15, label=None, color=GOLD, size=24)
        sig_lbl = T("signal", 24, GOLD).move_to([-4.60, 0.18, 0])
        prog_span = Line(P.pt(0.15, 0.08), P.pt(5.8, 0.08), color=GOLD, stroke_width=4)
        self.play(Create(sig_mark), FadeIn(sig_lbl), Create(prog_span), run_time=2.5)

        # Beat 5: Staining Fos hours later marks neurons that were strongly excited
        self.at("Staining")
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        excited = [False, True, False, True, False]
        neurons = VGroup()
        nucs_to_stain = []
        for x, exc in zip(xs, excited):
            neu, nuc = build_neuron([x, 2.05, 0], stained=False)
            neurons.add(neu)
            if exc:
                nucs_to_stain.append(nuc)
        stain_lbl = T("Fos stain (hours later)", 28, FOS_COL).move_to([0.0, 3.25, 0])

        self.play(FadeOut(upper_strip), run_time=0.45)
        self.play(FadeIn(neurons), FadeIn(stain_lbl), run_time=0.85)
        self.play(*[n.animate.set_fill(FOS_COL, opacity=0.95).set_stroke(FOS_COL) for n in nucs_to_stain],
                  run_time=2.3)
        self.finish()


class S11End(EndCard):
    LINE = "Paired factors widen gene choices and drive a slower second wave."
