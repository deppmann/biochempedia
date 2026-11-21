"""Ras to ERK: Three Kinases in Series — animation for ras-to-mapk.

COLOUR MAP (one colour per concept for the whole film):
- GOLD   (#D4A843): Growth factor ligand, receptor tyrosine kinase (RTK), active gene (c-fos)
- CORAL  (#FF7A59): Ras protein (GTPase switch, lipid-anchored at inner membrane)
- TEAL   (#3FB8C0): Adaptors & scaffold (Grb2, SOS, Scaffold KSR)
- GREEN  (#83C167): Raf (Tier 1 kinase, folded -> open -> paired)
- BLUE   (#58C4DD): MEK (Tier 2 dual-specificity kinase)
- VIOLET (#B388FF): ERK (Tier 3 kinase) and nuclear transcription factor target (Elk-1)
- YELLOW (#F5D547): Phosphate tags (P) and GTP
- RED    (#FC6255): Phosphatase & negative feedback control
- INDIGO (#7B8CDE): Nucleus envelope & DNA track
- GREY   (#8B93A1): GDP (inactive nucleotide), resting/silenced outlines, parallel JNK/p38 lanes, 1-site reference

CARRIED WORLD:
A 16:9 dark-navy cross-section of the cell: warm amber plasma membrane strip across the top,
deep cytosol in the middle, soft indigo nuclear arc and gene bar at the bottom. Full-cell scenes
(S01, S08, S10) use this complete cross-section; mechanistic scenes (S02, S03, S04, S05/S06, S07,
S09) zoom into the membrane inner face, the three-kinase cascade, ERK's two-phosphate lock, or the
nuclear/scaffold modules and carry exact geometry across consecutive scenes.

WHAT CHANGES IN EACH SPOKEN SCENE (and what drives it):
- s01_hook: Growth factor docks on membrane RTK outside the cell, lighting its tail; 3 numbered relay slots appear and a signal tracer traverses down across the cytoplasm into the nucleus genes (driven by narration cues).
- s02_ras_switch: Grb2 and SOS dock onto the lit RTK tail; SOS makes Ras eject GDP and bind GTP from the cytosol pool; Ras brightens and its slack loops snap taut into 'Switch loops' (driven by narration cues).
- s03_raf_pairing: Folded Raf rises from the cytosol onto Ras-GTP's notch, remains shut while bound alone, unfolds when touching membrane lipids, and a second open Raf slides side-to-side to form Paired Raf (driven by narration cues).
- s04_mek_erk: Paired Raf transfers two P badges onto MEK's Ser sites; typical-kinase target chips swap into dual-specificity; active MEK stamps Thr-P and Tyr-P one residue apart onto ERK's loop, locking ERK active (driven by narration cues).
- s05_predict_q: On zoomed active ERK (Thr-P, Tyr-P), a crimson Phosphatase moves in and positions jaws beside Tyr-P while Thr-P is ringed as staying attached, and the predict question card appears (identical end frame to S06PredictPause).
- s07_reveal_sharp: Phosphatase clips Tyr-P off and ERK dims to OFF (0%) with active-site lobes misaligned; a computed Plot draws y=p and sweeps y=p² from 0 to 1, builds the worked pair word-by-word ('p = 0.1 -> p² = 0.01', 'p = 0.5 -> p² = 0.25') with plot markers, traces the low-MEK flat then steep climb, and adds the schematic crowding footnote.
- s08_three_tiers_fan: In the full cell, active Raf multiplies signal across MEK blocks (amplify), 2-P lock sharpens ERK, phosphatase/feedback arrows mark control points, MEK funnels through a narrow pipe to ERK, and ERK fans signal dots out to cytoplasm and nucleus (driven by narration cues).
- s09_targets_scaffolds: In the nucleus, ERK stamps P onto Elk-1 and switches on c-fos with 'Immediate early genes = first genes on, within minutes', while in the cytosol above, cyan KSR Scaffold clamps Raf-MEK-ERK beside parallel JNK and p38 lanes (driven by narration cues).
- s10_close: Full-cell relay fires top-to-bottom in sync with the summary: Ras-GTP grips Paired Raf, three tiers amplify/sharpen/control the signal, and ERK fans out to cytoplasmic proteins and nuclear c-fos (driven by narration cues).
"""
from bp_parts import *

# Concept palette
CORAL = "#FF7A59"
VIOLET = "#B388FF"
INDIGO = "#7B8CDE"

MEM_FILL = "#2D2315"
NUC_FILL = "#202744"
DIM_FILL = "#181C26"
DIM_STROKE = "#5E6778"


# ------------------------------------------------------------------ shared builders
def make_block(label_text, color, width=2.2, height=0.85, fill_opacity=0.22,
               stroke_width=3.5, font_size=28, text_color=TEXT, corner=0.18):
    """Labelled protein/compartment block sized cleanly around its label."""
    lab = T(label_text, size=font_size, color=text_color)
    w = max(width, lab.width + 0.56)
    h = max(height, lab.height + 0.42)
    box = RoundedRectangle(
        corner_radius=min(corner, h / 2),
        width=w, height=h,
        stroke_color=color, stroke_width=stroke_width,
        fill_color=color, fill_opacity=fill_opacity,
    )
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box = box
    g.label = lab
    return g


def make_p_badge(tag="P", color=YELLOW, radius=0.26, font_size=22):
    """Phosphate circle badge with high-contrast dark label and comfortable internal padding."""
    c = Circle(radius=radius, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.95)
    t = T(tag, size=font_size, color=BG, weight=BOLD).move_to(c)
    g = VGroup(c, t)
    g.circle = c
    g.label = t
    return g


def make_cell_stage(mem_y=2.25, mem_h=0.52, nuc_top=-1.85, show_labels=True):
    """Full-cell cross-section shared across S01, S08, and S10."""
    W = 11.8
    mem_rect = Rectangle(
        width=W, height=mem_h,
        stroke_width=0, fill_color=MEM_FILL, fill_opacity=1.0,
    ).move_to([0, mem_y, 0])
    mem_top = Line([-W / 2, mem_y + mem_h / 2, 0], [W / 2, mem_y + mem_h / 2, 0], color=GOLD, stroke_width=3.5)
    mem_bot = Line([-W / 2, mem_y - mem_h / 2, 0], [W / 2, mem_y - mem_h / 2, 0], color=GOLD, stroke_width=3.5)
    membrane = VGroup(mem_rect, mem_top, mem_bot)

    nuc_bot = -3.45
    nuc_h = nuc_top - nuc_bot
    nuc_box = RoundedRectangle(
        corner_radius=0.55, width=9.4, height=nuc_h,
        stroke_color=INDIGO, stroke_width=3.5,
        fill_color=NUC_FILL, fill_opacity=1.0,
    ).move_to([0, (nuc_top + nuc_bot) / 2, 0])

    # DNA/gene track split around gene_bar so the line never crosses the Genes label
    dna_y = -2.85
    gene_bar = RoundedRectangle(
        corner_radius=0.10, width=2.0, height=0.50,
        stroke_color=INDIGO, stroke_width=2.8,
        fill_color=DIM_FILL, fill_opacity=1.0,
    ).move_to([0.9, dna_y, 0])
    gene_lab = T("Genes", size=24, color=TEXT).move_to(gene_bar)
    dna_l = Line([-3.4, dna_y, 0], [gene_bar.get_left()[0], dna_y, 0], color=INDIGO, stroke_width=4)
    dna_r = Line([gene_bar.get_right()[0], dna_y, 0], [3.4, dna_y, 0], color=INDIGO, stroke_width=4)
    dna_line = VGroup(dna_l, dna_r)

    g = VGroup(membrane, nuc_box, dna_line, gene_bar, gene_lab)
    g.membrane = membrane
    g.mem_top_y = mem_y + mem_h / 2
    g.mem_bot_y = mem_y - mem_h / 2
    g.nuc_box = nuc_box
    g.dna_line = dna_line
    g.gene_bar = gene_bar
    g.gene_lab = gene_lab

    if show_labels:
        out_lab = T("Outside cell", size=24, color=TEXT).move_to([-4.8, mem_y + mem_h / 2 + 0.42, 0])
        mem_lab = T("Membrane", size=24, color=GOLD).move_to([-4.6, mem_y - mem_h / 2 - 0.34, 0])
        cyto_lab = T("Cytoplasm", size=26, color=TEXT).move_to([-4.6, 0.25, 0])
        nuc_lab = T("Nucleus", size=26, color=INDIGO).move_to([-3.2, -2.35, 0])
        g.add(out_lab, mem_lab, cyto_lab, nuc_lab)
        g.out_lab, g.mem_lab, g.cyto_lab, g.nuc_lab = out_lab, mem_lab, cyto_lab, nuc_lab
    return g


def make_rtk(x=0.0, mem_top=2.51, mem_bot=1.99, tail_y=1.15, active=False):
    """Transmembrane receptor tyrosine kinase with extracellular cup and cytoplasmic tail."""
    col = GOLD if active else DIM_STROKE
    sw = 4.5 if active else 3.0
    left_stem = Line([x - 0.16, mem_top + 0.22, 0], [x - 0.16, tail_y, 0], color=col, stroke_width=sw)
    right_stem = Line([x + 0.16, mem_top + 0.22, 0], [x + 0.16, tail_y, 0], color=col, stroke_width=sw)
    cup = ArcBetweenPoints(
        [x - 0.38, mem_top + 0.42, 0], [x + 0.38, mem_top + 0.42, 0],
        angle=1.3, color=col, stroke_width=sw,
    )
    tail_bar = RoundedRectangle(
        corner_radius=0.1, width=0.64, height=0.42,
        stroke_color=col, stroke_width=sw,
        fill_color=col, fill_opacity=0.28 if active else 0.12,
    ).move_to([x, tail_y, 0])
    g = VGroup(left_stem, right_stem, cup, tail_bar)
    g.cup_center = np.array([x, mem_top + 0.44, 0.0])
    g.tail_bar = tail_bar
    return g


def make_membrane_band(y=2.2, h=0.65, label_x=-1.0):
    """Zoomed horizontal plasma membrane strip across upper frame (S02, S03)."""
    W = 12.2
    rect = Rectangle(width=W, height=h, stroke_width=0, fill_color=MEM_FILL, fill_opacity=1.0).move_to([0, y, 0])
    top = Line([-W / 2, y + h / 2, 0], [W / 2, y + h / 2, 0], color=GOLD, stroke_width=4)
    bot = Line([-W / 2, y - h / 2, 0], [W / 2, y - h / 2, 0], color=GOLD, stroke_width=4)
    lab = T("Plasma membrane", size=24, color=GOLD).move_to([label_x, y, 0])
    g = VGroup(rect, top, bot, lab)
    g.top_y = y + h / 2
    g.bot_y = y - h / 2
    return g


def make_ras_unit(x, mem_bot_y, active=False, with_gdp=False, with_gtp=False):
    """Lipid-anchored Ras with switch loops (slack when GDP, taut gripping notch when GTP)."""
    col = CORAL if active else DIM_STROKE
    anchor = VMobject(color=GOLD, stroke_width=3.5)
    anchor.set_points_as_corners([
        [x, mem_bot_y, 0],
        [x - 0.1, mem_bot_y - 0.16, 0],
        [x + 0.1, mem_bot_y - 0.32, 0],
        [x, mem_bot_y - 0.48, 0],
    ])
    body_y = mem_bot_y - 1.18
    body = RoundedRectangle(
        corner_radius=0.28, width=2.45, height=1.35,
        stroke_color=col, stroke_width=4.5 if active else 3.0,
        fill_color=CORAL if active else DIM_FILL, fill_opacity=0.28 if active else 0.75,
    ).move_to([x, body_y, 0])
    lab = T("Ras", size=30, color=TEXT if active else CORAL).move_to([x - 0.45, body_y + 0.12, 0])

    if active:
        loop1 = Line([x - 0.55, body_y - 0.67, 0], [x - 0.12, body_y - 0.96, 0], color=CORAL, stroke_width=5)
        loop2 = Line([x + 0.55, body_y - 0.67, 0], [x + 0.12, body_y - 0.96, 0], color=CORAL, stroke_width=5)
    else:
        loop1 = ArcBetweenPoints([x - 0.75, body_y - 0.67, 0], [x - 0.1, body_y - 0.78, 0], angle=0.7, color=DIM_STROKE, stroke_width=3.5)
        loop2 = ArcBetweenPoints([x + 0.1, body_y - 0.78, 0], [x + 0.75, body_y - 0.67, 0], angle=0.7, color=DIM_STROKE, stroke_width=3.5)

    g = VGroup(anchor, body, lab, loop1, loop2)
    g.anchor = anchor
    g.body = body
    g.label = lab
    g.loop1 = loop1
    g.loop2 = loop2
    g.pocket_pos = np.array([x + 0.52, body_y + 0.12, 0.0])
    g.notch_pos = np.array([x, body_y - 1.0, 0.0])

    if with_gdp:
        g.nuc = chip("GDP", GREY, size=24, pad=0.14, fill_opacity=0.25).move_to(g.pocket_pos)
        g.add(g.nuc)
    elif with_gtp:
        g.nuc = chip("GTP", YELLOW, size=24, pad=0.14, fill_opacity=0.28).move_to(g.pocket_pos)
        g.add(g.nuc)
    else:
        g.nuc = None
    return g


def make_erk_predict_block(center=(-1.1, 0.75, 0), active=True, with_tyr=True):
    """Large zoomed ERK block with activation loop cleanly inside body (shared S05/S06/S07)."""
    cx, cy, _ = center
    col = VIOLET if active else DIM_STROKE
    body = RoundedRectangle(
        corner_radius=0.32, width=5.3, height=2.25,
        stroke_color=col, stroke_width=5.0 if active else 3.0,
        fill_color=VIOLET if active else DIM_FILL, fill_opacity=0.28 if active else 0.85,
    ).move_to([cx, cy, 0])
    erk_lab = T("ERK", size=38, color=TEXT if active else GREY, weight=BOLD).move_to([cx - 1.45, cy + 0.30, 0])
    state_lab = T("Active" if active else "OFF (0%)", size=28, color=VIOLET if active else RED, weight=BOLD).move_to([cx - 1.45, cy - 0.42, 0])

    # Activation loop nested cleanly inside the right side of ERK body (never poking out)
    loop_y = cy
    loop_arc = RoundedRectangle(
        corner_radius=0.24, width=2.45, height=1.50,
        stroke_color=col, stroke_width=3.8 if active else 2.8,
        fill_color=BG, fill_opacity=0.92,
    ).move_to([cx + 1.12, loop_y, 0])

    thr_chip = T("Thr", size=24, color=TEXT).move_to([cx + 0.56, loop_y + 0.38, 0])
    tyr_chip = T("Tyr", size=24, color=TEXT).move_to([cx + 1.68, loop_y + 0.38, 0])
    thr_p = make_p_badge("P", YELLOW, radius=0.25, font_size=22).move_to([cx + 0.56, loop_y - 0.24, 0])
    thr_ring = Circle(radius=0.34, color=GREEN, stroke_width=3.5).move_to(thr_p)

    g = VGroup(body, erk_lab, state_lab, loop_arc, thr_chip, tyr_chip, thr_p, thr_ring)
    g.body = body
    g.erk_lab = erk_lab
    g.state_lab = state_lab
    g.loop_arc = loop_arc
    g.thr_chip = thr_chip
    g.tyr_chip = tyr_chip
    g.thr_p = thr_p
    g.thr_ring = thr_ring
    g.tyr_pos = np.array([cx + 1.68, loop_y - 0.24, 0.0])

    if with_tyr:
        tyr_p = make_p_badge("P", YELLOW, radius=0.25, font_size=22).move_to(g.tyr_pos)
        g.add(tyr_p)
        g.tyr_p = tyr_p
    else:
        empty_slot = DashedVMobject(Circle(radius=0.25, color=RED, stroke_width=2.5), num_dashes=10).move_to(g.tyr_pos)
        g.add(empty_slot)
        g.tyr_p = None
    return g


def make_phosphatase(pos=(1.80, 0.56, 0)):
    """Crimson crescent-like phosphatase shape with crisp label."""
    px, py, _ = pos
    crescent = AnnularSector(
        inner_radius=0.42, outer_radius=0.90,
        angle=1.35 * PI, start_angle=1.32 * PI,
        color=RED, stroke_width=3.0, fill_color=RED, fill_opacity=0.28,
    ).move_to([px, py, 0])
    lab = T("Phosphatase", size=28, color=RED, weight=BOLD).next_to(crescent, DOWN, buff=0.24)
    g = VGroup(crescent, lab)
    g.crescent = crescent
    g.label = lab
    return g


def erk_predict_world():
    """Exact shared backdrop for S05PredictQ end and S06PredictPause."""
    erk = make_erk_predict_block(center=(-1.85, 0.78, 0), active=True, with_tyr=True)
    # Phosphatase positioned right of ERK body (right edge = -1.85 + 2.65 = 0.80)
    phos = make_phosphatase(pos=(1.80, 0.56, 0))
    keep_tag = T("Thr-P stays", size=24, color=GREEN).move_to([erk.thr_p.get_x(), erk.body.get_bottom()[1] - 0.36, 0])
    # Dashed snip marker clearly to the right of Tyr-P (between Tyr-P and Phosphatase)
    cut_line = DashedLine(
        [erk.tyr_p.get_right()[0] + 0.14, erk.tyr_p.get_top()[1] + 0.08, 0],
        [erk.tyr_p.get_right()[0] + 0.14, erk.tyr_p.get_bottom()[1] - 0.08, 0],
        color=RED, stroke_width=4.0,
    )
    return VGroup(erk, phos, keep_tag, cut_line)


# ------------------------------------------------------------------ S00 Title
class S00Title(TitleCard):
    LESSON = "Ras to MAPK: The Kinase Cascade"
    TITLE = "Ras to ERK: Three Kinases in Series"


# ------------------------------------------------------------------ S01 Hook
class S01Hook(SpokenScene):
    def construct(self):
        stage = make_cell_stage()
        rtk = make_rtk(x=0.0, mem_top=stage.mem_top_y, mem_bot=stage.mem_bot_y, tail_y=1.35, active=False)
        gf = VGroup(
            Dot(radius=0.26, color=GOLD),
            T("Growth factor", size=26, color=GOLD),
        )
        gf[0].move_to([-0.8, 3.24, 0])
        gf[1].next_to(gf[0], LEFT, buff=0.2)

        self.play(FadeIn(stage), FadeIn(rtk), FadeIn(gf), run_time=0.7)
        self.at("outside the cell")
        self.play(
            gf[0].animate.move_to([0.0, stage.mem_top_y + 0.72, 0]),
            gf[1].animate.move_to([-1.65, stage.mem_top_y + 0.72, 0]),
            run_time=1.8,
        )

        self.at("three kinases")
        slots = VGroup()
        slot_ys = [0.75, -0.10, -0.95]
        for idx, sy in enumerate(slot_ys, 1):
            box = DashedVMobject(
                RoundedRectangle(corner_radius=0.14, width=2.45, height=0.58, color=TEAL, stroke_width=3),
                num_dashes=18,
            ).move_to([0, sy, 0])
            num = T(f"Kinase {idx} (?)", size=26, color=TEXT).move_to(box)
            slots.add(VGroup(box, num))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in slots], lag_ratio=0.3), run_time=3.2)

        self.at("at the surface")
        lit_rtk = make_rtk(x=0.0, mem_top=stage.mem_top_y, mem_bot=stage.mem_bot_y, tail_y=1.35, active=True)
        self.play(
            gf[0].animate.move_to(rtk.cup_center),
            gf[1].animate.next_to(rtk.cup_center, LEFT, buff=0.45),
            ReplacementTransform(rtk, lit_rtk),
            run_time=1.4,
        )

        self.at("genes lie deep inside")
        self.play(
            stage.gene_bar.animate.set_stroke(GOLD, 3.5).set_fill(GOLD, opacity=0.25),
            stage.gene_lab.animate.set_color(GOLD),
            run_time=1.6,
        )

        self.at("Carrying that order")
        conn1 = Arrow([1.4, 1.25, 0], [1.4, 0.75, 0], buff=0, color=GOLD, stroke_width=4, tip_length=0.18)
        conn2 = Arrow([1.4, 0.65, 0], [1.4, -0.10, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.18)
        conn3 = Arrow([1.4, -0.20, 0], [1.4, -0.95, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.18)
        conn4 = Arrow([1.4, -1.05, 0], [1.4, -2.45, 0], buff=0, color=GOLD, stroke_width=4, tip_length=0.18)
        relay_note = T("3-kinase relay", size=28, color=TEAL, weight=BOLD).move_to([3.4, -0.1, 0])

        p_prog = ValueTracker(0.0)
        tracer = always_redraw(lambda: Dot(
            [1.4, 1.25 - p_prog.get_value() * 3.7, 0.0],
            radius=0.16, color=YELLOW,
        ))
        self.play(
            Create(conn1), Create(conn2), Create(conn3), Create(conn4),
            FadeIn(relay_note),
            run_time=1.0,
        )
        self.add(tracer)
        self.play(
            p_prog.animate.set_value(1.0),
            *[s[0].animate.set_color(GOLD) for s in slots],
            run_time=3.5, rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ S02 Ras Switch
class S02RasSwitch(SpokenScene):
    def construct(self):
        mem = make_membrane_band(y=2.3, h=0.62, label_x=-1.0)
        rtk = make_rtk(x=-4.2, mem_top=mem.top_y, mem_bot=mem.bot_y, tail_y=0.55, active=True)
        gf = Dot(radius=0.24, color=GOLD).move_to(rtk.cup_center)
        rtk_lab = T("Active RTK", size=26, color=GOLD).next_to(rtk.tail_bar, DOWN, buff=0.24)

        ras = make_ras_unit(x=2.4, mem_bot_y=mem.bot_y, active=False, with_gdp=True)
        loop_lab = T("Slack loops", size=24, color=TEXT).move_to([2.4, -0.62, 0])

        grb2 = make_block("Grb2", TEAL, width=1.45, height=0.72, fill_opacity=0.24).move_to([-2.4, -2.15, 0])
        sos = make_block("SOS", TEAL, width=1.45, height=0.72, fill_opacity=0.24).move_to([-0.6, -2.15, 0])

        gtp_pos = [[1.2, -2.4, 0], [2.4, -2.75, 0], [3.6, -2.1, 0], [4.6, -2.7, 0], [5.1, -1.7, 0]]
        gtps = VGroup(*[chip("GTP", YELLOW, size=24, pad=0.14, fill_opacity=0.24).move_to(p) for p in gtp_pos])
        pool_lab = T("Plentiful GTP", size=24, color=YELLOW).move_to([3.4, -1.28, 0])

        self.play(
            FadeIn(mem), FadeIn(rtk), FadeIn(gf), FadeIn(rtk_lab),
            FadeIn(ras), FadeIn(loop_lab),
            FadeIn(grb2), FadeIn(sos), FadeIn(gtps), FadeIn(pool_lab),
            run_time=0.65,
        )

        self.at("active receptor recruits")
        self.play(grb2.animate.move_to([-2.95, 0.65, 0]), run_time=1.8)

        self.at("to the membrane")
        self.play(sos.animate.move_to([-1.15, 0.72, 0]), run_time=2.2)

        self.at("drop")
        # SOS shifts toward Ras; GDP pops clearly to the left of Switch loops label
        gdp_chip = ras.nuc
        self.play(
            sos.animate.shift(RIGHT * 0.60),
            gdp_chip.animate.move_to([0.15, -0.45, 0]),
            run_time=1.4,
        )
        dropped_lab = T("GDP dropped", size=24, color=GREY).next_to(gdp_chip, DOWN, buff=0.22)
        self.play(FadeIn(dropped_lab), run_time=0.6)

        self.at("binds instead")
        chosen_gtp = gtps[2]
        self.play(
            chosen_gtp.animate.move_to(ras.pocket_pos),
            FadeOut(gdp_chip), FadeOut(dropped_lab),
            run_time=1.5,
        )

        self.at("not a kinase")
        not_k = chip("Binding switch (not a kinase)", CORAL, size=26, pad=0.16, fill_opacity=0.18).move_to([-2.7, -1.5, 0])
        self.play(FadeIn(not_k, shift=UP * 0.1), run_time=1.4)

        self.at("switch loops")
        taut_l1 = Line([2.4 - 0.55, ras.body.get_bottom()[1], 0], [2.4 - 0.12, ras.body.get_bottom()[1] - 0.34, 0], color=CORAL, stroke_width=5.5)
        taut_l2 = Line([2.4 + 0.55, ras.body.get_bottom()[1], 0], [2.4 + 0.12, ras.body.get_bottom()[1] - 0.34, 0], color=CORAL, stroke_width=5.5)
        grip_lab = T("Switch loops", size=26, color=CORAL, weight=BOLD).move_to([2.4, -0.62, 0])
        self.play(
            ras.body.animate.set_stroke(CORAL, 5.0).set_fill(CORAL, opacity=0.30),
            ras.label.animate.set_color(TEXT),
            Transform(ras.loop1, taut_l1),
            Transform(ras.loop2, taut_l2),
            swap(loop_lab, grip_lab, run_time=0.9),
            run_time=1.8,
        )
        self.finish()


# ------------------------------------------------------------------ S03 Raf Pairing
def make_folded_raf(center, tag="Raf"):
    """Folded resting Raf: kinase lobe below, hinged inhibitory flap cleanly above (no overlap)."""
    cx, cy, _ = center
    kin = RoundedRectangle(
        corner_radius=0.18, width=1.45, height=0.82,
        stroke_color=GREEN, stroke_width=3.0, fill_color=DIM_FILL, fill_opacity=0.92,
    ).move_to([cx, cy - 0.20, 0])
    flap = RoundedRectangle(
        corner_radius=0.12, width=1.28, height=0.38,
        stroke_color=GREEN, stroke_width=2.8, fill_color=GREEN, fill_opacity=0.22,
    ).move_to([cx, cy + 0.48, 0])
    lab = T(tag, size=28, color=GREEN, weight=BOLD).move_to(kin)
    g = VGroup(kin, flap, lab)
    g.kin = kin
    g.flap = flap
    g.label = lab
    return g


class S03RafPairing(SpokenScene):
    def construct(self):
        mem = make_membrane_band(y=2.55, h=0.6, label_x=0.0)
        ras1 = make_ras_unit(x=-3.1, mem_bot_y=mem.bot_y, active=True, with_gtp=True)
        ras2 = make_ras_unit(x=3.1, mem_bot_y=mem.bot_y, active=True, with_gtp=True)

        raf1 = make_folded_raf(center=(-3.1, -2.0, 0), tag="Raf")
        raf2 = make_folded_raf(center=(3.1, -2.0, 0), tag="Raf")
        folded_note = T("Folded, resting Raf", size=26, color=GREEN).move_to([0.0, -2.1, 0])

        self.play(
            FadeIn(mem), FadeIn(ras1), FadeIn(ras2),
            FadeIn(raf1), FadeIn(raf2), FadeIn(folded_note),
            run_time=0.65,
        )

        self.at("acts by contact")
        contact_ring = Circle(radius=0.34, color=YELLOW, stroke_width=3.5).move_to(ras1.notch_pos)
        contact_lab = T("Acts by contact", size=26, color=CORAL).move_to([0.0, 0.35, 0])
        self.play(Create(contact_ring), FadeIn(contact_lab), run_time=1.8)

        self.at("catches folded")
        # Smooth continuous ascent over ~4.8s so Raf catches and holds at the membrane right up to Binding alone
        target_y1 = ras1.notch_pos[1] - 0.72
        self.play(
            FadeOut(contact_ring), FadeOut(folded_note),
            raf1.animate.move_to([-3.1, target_y1, 0]),
            run_time=4.8,
        )

        self.at("Binding alone")
        shut_note = T("Bound — still folded shut", size=26, color=TEXT).move_to([0.0, -0.55, 0])
        self.play(
            FadeOut(contact_lab),
            FadeIn(shut_note),
            raf1.flap.animate.set_stroke(YELLOW, 3.5),
            run_time=2.5,
        )

        self.at("membrane lipids")
        # Lipid interaction arc between membrane and Raf on the inner right side, with label centered cleanly between Ras1 and Ras2
        lipid_arc = ArcBetweenPoints(
            [-1.45, mem.bot_y, 0], [-2.25, target_y1 + 0.15, 0],
            angle=-0.60, color=GOLD, stroke_width=4,
        )
        lipid_lab = T("Membrane lipids", size=24, color=GOLD).move_to([0.0, 1.45, 0])
        self.play(Create(lipid_arc), FadeIn(lipid_lab), run_time=1.3)

        self.at("help it unfold")
        # Hinged flaps rotate onto the outer sides of kin (staying attached and clear of Ras & GTP)
        target_y2 = ras2.notch_pos[1] - 0.72
        open_note = T("Raf unfolds", size=26, color=GREEN).move_to([0.0, -0.55, 0])
        self.play(
            raf1.flap.animate.rotate(PI / 2).next_to(raf1.kin, LEFT, buff=0.06).set_stroke(GREEN, 2.8),
            raf1.kin.animate.set_fill(GREEN, opacity=0.32).set_stroke(GREEN, 4.5),
            raf1.label.animate.set_color(TEXT),
            raf2.animate.move_to([3.1, target_y2, 0]),
            swap(shut_note, open_note, run_time=0.8),
            run_time=1.55,
        )
        self.play(
            raf2.flap.animate.rotate(-PI / 2).next_to(raf2.kin, RIGHT, buff=0.06),
            raf2.kin.animate.set_fill(GREEN, opacity=0.32).set_stroke(GREEN, 4.5),
            raf2.label.animate.set_color(TEXT),
            FadeOut(lipid_arc), FadeOut(lipid_lab),
            run_time=1.15,
        )

        self.at("kinase domains then pair")
        # Align kin domains side-by-side at x=-0.82 and x=+0.82, y=-0.85 so flaps stay attached and clear of Ras
        dx1 = -0.82 - raf1.kin.get_center()[0]
        dy1 = -0.85 - raf1.kin.get_center()[1]
        dx2 = 0.82 - raf2.kin.get_center()[0]
        dy2 = -0.85 - raf2.kin.get_center()[1]
        self.play(
            FadeOut(open_note),
            raf1.animate.shift([dx1, dy1, 0]),
            raf2.animate.shift([dx2, dy2, 0]),
            run_time=2.3,
        )
        # Surround the paired Raf subunits cleanly without cutting across the attached flaps
        pair_glow = SurroundingRectangle(
            VGroup(raf1.kin, raf2.kin, raf1.flap, raf2.flap), buff=0.14,
            corner_radius=0.22, color=GREEN, stroke_width=5.0,
            fill_color=GREEN, fill_opacity=0.10,
        )
        pair_lab = T("Paired Raf (active)", size=30, color=GREEN, weight=BOLD).next_to(pair_glow, DOWN, buff=0.28)
        self.play(Create(pair_glow), FadeIn(pair_lab), run_time=1.8)
        self.finish()


# ------------------------------------------------------------------ S04 MEK & ERK
class S04MekErk(SpokenScene):
    def construct(self):
        raf_pair = make_block("Paired Raf", GREEN, width=2.9, height=1.1, fill_opacity=0.32, stroke_width=5.0, font_size=30).move_to([-4.2, 1.9, 0])

        mek = make_block("MEK", BLUE, width=2.8, height=1.35, fill_opacity=0.14, stroke_width=3.0, font_size=32, text_color=BLUE).move_to([0.0, 1.35, 0])
        ser1 = chip("Ser", GREY, size=24, pad=0.14, fill_opacity=0.15).move_to([-0.68, 2.38, 0])
        ser2 = chip("Ser", GREY, size=24, pad=0.14, fill_opacity=0.15).move_to([0.68, 2.38, 0])

        # ERK at bottom-right with tall activation loop box above it so Thr-P and Tyr-P sit cleanly inside
        erk_box = RoundedRectangle(
            corner_radius=0.25, width=3.5, height=1.55,
            stroke_color=DIM_STROKE, stroke_width=3.2, fill_color=DIM_FILL, fill_opacity=0.85,
        ).move_to([3.7, -1.55, 0])
        erk_lab = T("ERK", size=34, color=VIOLET, weight=BOLD).move_to(erk_box)
        loop_box = RoundedRectangle(
            corner_radius=0.20, width=3.5, height=1.22,
            stroke_color=VIOLET, stroke_width=3.0, fill_color=BG, fill_opacity=0.95,
        ).move_to([3.7, 0.08, 0])
        thr_lab = T("Thr", size=24, color=TEXT).move_to([2.65, 0.36, 0])
        gap_lab = T("•", size=24, color=GREY).move_to([3.7, 0.36, 0])
        tyr_lab = T("Tyr", size=24, color=TEXT).move_to([4.75, 0.36, 0])
        erk = VGroup(erk_box, erk_lab, loop_box, thr_lab, gap_lab, tyr_lab)

        self.play(FadeIn(raf_pair), FadeIn(mek), FadeIn(ser1), FadeIn(ser2), run_time=0.7)

        self.at("middle kinase")
        self.play(mek.box.animate.set_stroke(BLUE, 4.0), run_time=0.6)

        self.at("on two serines")
        p_s1 = make_p_badge("P", YELLOW, radius=0.25, font_size=22).move_to(raf_pair.get_right() + RIGHT * 0.1)
        p_s2 = make_p_badge("P", YELLOW, radius=0.25, font_size=22).move_to(raf_pair.get_right() + RIGHT * 0.1)
        arr_raf_mek = Arrow(raf_pair.get_right() + RIGHT * 0.08, mek.get_left() + LEFT * 0.08, buff=0, color=GREEN, stroke_width=4)
        self.play(Create(arr_raf_mek), run_time=0.7)
        self.play(p_s1.animate.move_to([-0.68, 3.05, 0]), run_time=1.3)
        self.play(
            p_s2.animate.move_to([0.68, 3.05, 0]),
            mek.box.animate.set_fill(BLUE, opacity=0.32).set_stroke(BLUE, 5.0),
            mek.label.animate.set_color(TEXT),
            run_time=1.4,
        )

        self.at("Most kinases target")
        typ1 = chip("Most kinases: Ser / Thr", GREY, size=26, pad=0.16, fill_opacity=0.18).move_to([-3.6, -1.0, 0])
        typ2 = chip("or Tyr alone", GREY, size=26, pad=0.16, fill_opacity=0.18).move_to([-3.6, -1.85, 0])
        self.play(FadeIn(typ1, shift=RIGHT * 0.15), run_time=1.2)

        self.at("or tyrosine alone")
        self.play(FadeIn(typ2, shift=RIGHT * 0.15), run_time=1.2)

        self.at("dual specificity kinase")
        dual_chip = chip("MEK: Dual-specificity (Thr + Tyr)", BLUE, size=26, pad=0.18, fill_opacity=0.24).move_to([-3.35, -1.45, 0])
        self.play(
            Succession(
                FadeOut(VGroup(typ1, typ2), run_time=0.45),
                FadeIn(dual_chip, run_time=0.65),
            )
        )

        self.at("tags ERK")
        arr_mek_erk = Arrow([1.45, 0.90, 0], [2.15, 0.65, 0], buff=0, color=BLUE, stroke_width=4.5)
        self.play(FadeIn(erk), Create(arr_mek_erk), run_time=0.7)

        self.at("threonine and a tyrosine")
        p_thr = make_p_badge("P", YELLOW, radius=0.25, font_size=22).move_to([1.3, 1.35, 0])
        p_tyr = make_p_badge("P", YELLOW, radius=0.25, font_size=22).move_to([1.3, 1.35, 0])
        # Stamp squarely inside loop_box under Thr and Tyr (clear of loop_box border)
        self.play(p_thr.animate.move_to([2.65, -0.18, 0]), run_time=0.75)
        self.play(p_tyr.animate.move_to([4.75, -0.18, 0]), run_time=0.75)

        self.at("one residue apart")
        apart_note = T("1 residue apart", size=24, color=YELLOW).next_to(loop_box, UP, buff=0.20)
        self.play(FadeIn(apart_note), run_time=0.8)

        self.at("2 phosphate lock")
        lock_lab = T("2-phosphate lock: ON", size=26, color=VIOLET, weight=BOLD).move_to([3.7, -2.75, 0])
        self.play(
            erk_box.animate.set_stroke(VIOLET, 5.5).set_fill(VIOLET, opacity=0.32),
            erk_lab.animate.set_color(TEXT),
            FadeIn(lock_lab),
            run_time=1.3,
        )
        self.finish()


# ------------------------------------------------------------------ S05 Predict Q
class S05PredictQ(SpokenScene):
    def construct(self):
        erk = make_erk_predict_block(center=(-1.85, 0.78, 0), active=True, with_tyr=True)
        phos = make_phosphatase(pos=(1.80, 0.56, 0))

        self.play(FadeIn(erk), run_time=0.8)

        self.at("Suppose a phosphatase")
        phos_start = phos.copy().shift(RIGHT * 2.2)
        self.play(FadeIn(phos_start), run_time=0.35)
        self.play(phos_start.animate.move_to(phos.get_center()), run_time=0.6)
        self.remove(phos_start)
        self.add(phos)

        self.at("removes just one")
        cut_line = DashedLine(
            [erk.tyr_p.get_right()[0] + 0.14, erk.tyr_p.get_top()[1] + 0.08, 0],
            [erk.tyr_p.get_right()[0] + 0.14, erk.tyr_p.get_bottom()[1] - 0.08, 0],
            color=RED, stroke_width=4.0,
        )
        self.play(Create(cut_line), run_time=0.9)

        self.at("leaving the other")
        keep_tag = T("Thr-P stays", size=24, color=GREEN).move_to([erk.thr_p.get_x(), erk.body.get_bottom()[1] - 0.36, 0])
        self.play(
            erk.thr_ring.animate.set_stroke(GREEN, 5.0),
            FadeIn(keep_tag),
            run_time=1.2,
        )

        self.at("Does ERK stay")
        q = question_card(
            "One phosphate removed: half-active or off?",
            ["half-active", "off completely"],
            chips_at=[4.85, 0.78, 0],
        )
        self.play(FadeIn(q.question), FadeIn(q.chips), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ S06 Predict Pause
class S06PredictPause(PredictPause):
    QUESTION = "One phosphate removed: half-active or off?"
    OPTIONS = ["half-active", "off completely"]
    CHIPS_AT = [4.85, 0.78, 0]
    SECONDS = 4.5

    def backdrop(self):
        return erk_predict_world()


# ------------------------------------------------------------------ S07 Reveal Sharp
class S07RevealSharp(SpokenScene):
    def construct(self):
        world = erk_predict_world()
        erk, phos, keep_tag, cut_line = world[0], world[1], world[2], world[3]
        self.add(erk, phos, keep_tag, cut_line)

        self.at("shuts off completely")
        off_state = T("OFF (0%)", size=28, color=RED, weight=BOLD).move_to(erk.state_lab)
        empty_slot = DashedVMobject(Circle(radius=0.25, color=RED, stroke_width=2.5), num_dashes=10).move_to(erk.tyr_pos)
        self.play(
            FadeOut(cut_line),
            erk.tyr_p.animate.shift(RIGHT * 1.1 + UP * 0.8).set_opacity(0.0),
            FadeIn(empty_slot),
            erk.body.animate.set_stroke(DIM_STROKE, 3.0).set_fill(DIM_FILL, opacity=0.85),
            erk.erk_lab.animate.set_color(GREY),
            erk.loop_arc.animate.set_stroke(DIM_STROKE, 2.8),
            swap(erk.state_lab, off_state, run_time=0.7),
            run_time=1.4,
        )
        erk.remove(erk.state_lab)

        self.at("Removing either phosphate")
        miss_ring = Circle(radius=0.34, color=RED, stroke_width=4.0).move_to(erk.tyr_pos)
        self.play(
            Create(miss_ring),
            empty_slot.animate.set_stroke(RED, 3.8),
            erk.thr_ring.animate.set_stroke(YELLOW, 5.0),
            run_time=1.8,
        )

        self.at("requires both")
        self.play(
            Indicate(erk.thr_p, scale_factor=1.22, color=YELLOW),
            Indicate(miss_ring, scale_factor=1.22, color=RED),
            run_time=1.0,
        )

        self.at("align its active site")
        # Animate the active-site loop shifting clearly out of alignment without rotating text bounds
        need_both = T("Needs both P to align active site", size=26, color=TEXT).move_to([-1.3, -1.35, 0])
        delta = RIGHT * 0.28 + DOWN * 0.20
        loop_parts = [erk.thr_chip, erk.tyr_chip, erk.thr_p, erk.thr_ring, empty_slot, miss_ring]
        self.play(
            FadeIn(need_both),
            erk.loop_arc.animate.shift(delta).set_stroke(RED, 3.8),
            *[m.animate.shift(delta) for m in loop_parts],
            run_time=1.0,
        )
        self.play(
            erk.loop_arc.animate.shift(-delta).set_stroke(DIM_STROKE, 2.8),
            *[m.animate.shift(-delta) for m in loop_parts],
            run_time=0.9,
        )

        self.at("In the test tube")
        # Replace zoomed ERK with a clean, unscaled compact summary card (every label >= 24 pt)
        compact_box = RoundedRectangle(
            corner_radius=0.24, width=3.8, height=1.70,
            stroke_color=DIM_STROKE, stroke_width=3.0, fill_color=DIM_FILL, fill_opacity=0.88,
        ).move_to([-4.0, 1.55, 0])
        c_erk = T("ERK: OFF (0%)", size=26, color=RED, weight=BOLD).move_to([-4.0, 1.95, 0])
        c_p = make_p_badge("P", YELLOW, radius=0.24, font_size=22).move_to([-4.55, 1.22, 0])
        c_ring = Circle(radius=0.31, color=GREEN, stroke_width=3.0).move_to(c_p)
        c_empty = DashedVMobject(Circle(radius=0.24, color=RED, stroke_width=2.5), num_dashes=10).move_to([-3.45, 1.22, 0])
        compact_card = VGroup(compact_box, c_erk, c_p, c_ring, c_empty)
        compact_note = T("1 P alone: 0% active", size=24, color=RED).next_to(compact_card, DOWN, buff=0.20)

        old_zoom = VGroup(erk, off_state, phos, keep_tag, empty_slot, miss_ring, need_both)
        self.play(
            Succession(
                FadeOut(old_zoom, run_time=0.25),
                FadeIn(VGroup(compact_card, compact_note), run_time=0.35),
            )
        )

        P = Plot(
            box=(0.2, 5.7, -1.65, 2.35),
            xr=(0.0, 1.0), yr=(0.0, 1.0),
            xticks=[(0.0, "0"), (0.5, "0.5"), (1.0, "1.0")],
            yticks=[(0.0, "0"), (0.5, "0.5"), (1.0, "1.0")],
            xlabel="MEK site occupancy (p)",
            ylabel="Active ERK fraction",
            color=GREY, size=24, label_size=24,
        )
        p_tr = ValueTracker(0.0)
        c1 = P.curve(lambda p: p, color=GREY, width=4.5)
        c2 = P.live_curve(lambda p: p ** 2, p_tr, color=VIOLET, width=6.0)
        leg1 = T("1-site (p)", size=24, color=GREY).move_to([1.50, 1.98, 0])
        leg2 = T("2-site (p²)", size=24, color=VIOLET, weight=BOLD).move_to([1.50, 1.50, 0])

        self.play(Create(P), run_time=0.50)

        self.at("one hit")
        self.play(Create(c1), FadeIn(leg1), run_time=1.0)

        self.at("two independent hits")
        self.add(c2)
        self.play(p_tr.animate.set_value(1.0), FadeIn(leg2), run_time=2.2, rate_func=linear)

        # Live tracker dot + dashed axis drop-lines move along the curves in sync with the worked numbers
        p_live = ValueTracker(0.0)
        vline_live = always_redraw(lambda: DashedLine(
            P.pt(p_live.get_value(), 0.0),
            P.pt(p_live.get_value(), p_live.get_value()),
            color=GREY, stroke_width=2.5, dash_length=0.10,
        ) if p_live.get_value() > 0.02 else VGroup())
        hline_live = always_redraw(lambda: DashedLine(
            P.pt(0.0, p_live.get_value() ** 2),
            P.pt(p_live.get_value(), p_live.get_value() ** 2),
            color=VIOLET, stroke_width=2.5, dash_length=0.10,
        ) if p_live.get_value() > 0.02 else VGroup())
        dot_live = always_redraw(lambda: Dot(
            P.pt(p_live.get_value(), p_live.get_value() ** 2),
            radius=0.12, color=VIOLET, stroke_color=YELLOW, stroke_width=3,
        ) if p_live.get_value() > 0.03 else VGroup())
        self.add(vline_live, hline_live, dot_live)

        # Worked pair built word-by-word in time with the spoken numbers (never shown early)
        r1_a = M("p = 0.1", size=26, color=TEXT)
        r1_b = M("→ p² = 0.01", size=26, color=VIOLET)
        r1 = VGroup(r1_a, r1_b).arrange(RIGHT, buff=0.14).move_to([-5.85, -0.55, 0], aligned_edge=LEFT)

        r2_a = M("p = 0.5", size=26, color=TEXT)
        r2_b = M("→ p² = 0.25", size=26, color=VIOLET)
        r2 = VGroup(r2_a, r2_b).arrange(RIGHT, buff=0.14).move_to([-5.85, -1.30, 0], aligned_edge=LEFT)

        self.at("one in ten")
        dot_01_p = Dot(P.pt(0.1, 0.1), radius=0.08, color=GREY)
        self.play(p_live.animate.set_value(0.1), FadeIn(r1_a), FadeIn(dot_01_p), run_time=0.65)

        self.at("one in a hundred")
        dot_01_p2 = Dot(P.pt(0.1, 0.01), radius=0.10, color=YELLOW)
        self.play(FadeIn(r1_b), FadeIn(dot_01_p2), run_time=0.65)

        self.at("one half")
        dot_05_p = Dot(P.pt(0.5, 0.5), radius=0.08, color=GREY)
        self.play(p_live.animate.set_value(0.5), FadeIn(r2_a), FadeIn(dot_05_p), run_time=0.65)

        self.at("one quarter")
        dot_05_p2 = Dot(P.pt(0.5, 0.25), radius=0.10, color=YELLOW)
        self.play(FadeIn(r2_b), FadeIn(dot_05_p2), run_time=0.65)

        self.at("P squared stays tiny")
        self.play(p_live.animate.set_value(0.05), run_time=0.6, rate_func=linear)
        self.play(p_live.animate.set_value(0.32), run_time=0.8, rate_func=linear)

        self.at("climbs steeply")
        crowd_curve = DashedVMobject(P.curve(lambda p: p ** 1.25, color=TEAL, width=4.5), num_dashes=26)
        crowd_note = caption(
            "Schematic: in some cells, crowding may make this nearly one step",
            size=24, color=TEAL, y=-3.15,
        )
        self.play(
            AnimationGroup(
                p_live.animate(run_time=1.25, rate_func=linear).set_value(1.0),
                Create(crowd_curve, run_time=1.0),
                FadeIn(crowd_note, run_time=0.45),
            )
        )
        self.finish()


# ------------------------------------------------------------------ S08 Three Tiers Fan
class S08ThreeTiersFan(SpokenScene):
    def construct(self):
        stage = make_cell_stage(mem_y=2.7, mem_h=0.48, nuc_top=-2.15, show_labels=False)
        rtk = make_rtk(x=0.0, mem_top=stage.mem_top_y, mem_bot=stage.mem_bot_y, tail_y=2.12, active=True)
        gf = Dot(radius=0.2, color=GOLD).move_to(rtk.cup_center)

        ras = make_block("Ras-GTP", CORAL, width=1.8, height=0.58, fill_opacity=0.28, font_size=26).move_to([0.0, 1.55, 0])
        raf = make_block("Paired Raf", GREEN, width=2.1, height=0.60, fill_opacity=0.28, font_size=26).move_to([0.0, 0.80, 0])

        mek_l = make_block("MEK", BLUE, width=1.3, height=0.60, fill_opacity=0.14, font_size=26, text_color=BLUE).move_to([-2.0, -0.28, 0])
        mek_c = make_block("MEK", BLUE, width=1.3, height=0.60, fill_opacity=0.14, font_size=26, text_color=BLUE).move_to([0.0, -0.28, 0])
        mek_r = make_block("MEK", BLUE, width=1.3, height=0.60, fill_opacity=0.14, font_size=26, text_color=BLUE).move_to([2.0, -0.28, 0])
        meks = VGroup(mek_l, mek_c, mek_r)

        erk = make_block("ERK", VIOLET, width=1.8, height=0.64, fill_opacity=0.14, font_size=28, text_color=VIOLET).move_to([0.0, -1.32, 0])

        t_left = make_block("Target 1", TEXT, width=1.65, height=0.56, fill_opacity=0.12, font_size=24).move_to([-4.55, -1.46, 0])
        t_right = make_block("Target 2", TEXT, width=1.65, height=0.56, fill_opacity=0.12, font_size=24).move_to([4.75, -1.46, 0])

        self.play(
            FadeIn(stage), FadeIn(rtk), FadeIn(gf),
            FadeIn(ras), FadeIn(raf), FadeIn(meks), FadeIn(erk),
            FadeIn(t_left), FadeIn(t_right),
            run_time=0.6,
        )

        self.at("more than carry")
        t1_tag = T("1", size=24, color=GREEN, weight=BOLD).next_to(raf, LEFT, buff=0.22)
        t2_tag = T("2", size=24, color=BLUE, weight=BOLD).next_to(mek_l, LEFT, buff=0.22)
        t3_tag = T("3", size=24, color=VIOLET, weight=BOLD).move_to([-1.20, -1.02, 0])
        self.play(FadeIn(t1_tag), FadeIn(t2_tag), FadeIn(t3_tag), run_time=1.8)

        self.at("amplify the signal")
        arr_raf_meks = VGroup(
            Arrow(raf.get_bottom() + LEFT * 0.4 + DOWN * 0.04, mek_l.get_top() + UP * 0.04, buff=0, color=GREEN, stroke_width=3.5, tip_length=0.16),
            Arrow(raf.get_bottom() + DOWN * 0.04, mek_c.get_top() + UP * 0.04, buff=0, color=GREEN, stroke_width=3.5, tip_length=0.16),
            Arrow(raf.get_bottom() + RIGHT * 0.4 + DOWN * 0.04, mek_r.get_top() + UP * 0.04, buff=0, color=GREEN, stroke_width=3.5, tip_length=0.16),
        )
        amp_lab = T("Amplify", size=26, color=GREEN, weight=BOLD).move_to([3.65, 0.55, 0])
        self.play(
            Create(arr_raf_meks),
            *[m.box.animate.set_fill(BLUE, opacity=0.30).set_stroke(BLUE, 4.5) for m in meks],
            *[m.label.animate.set_color(TEXT) for m in meks],
            FadeIn(amp_lab),
            run_time=1.4,
        )

        self.at("sharpen its rise")
        p1 = make_p_badge("P", YELLOW, radius=0.22, font_size=22).move_to([1.28, -1.05, 0])
        p2 = make_p_badge("P", YELLOW, radius=0.22, font_size=22).move_to([1.28, -1.59, 0])
        sharp_lab = T("Sharpen (2-P)", size=26, color=VIOLET, weight=BOLD).move_to([3.85, -0.86, 0])
        self.play(
            FadeIn(p1), FadeIn(p2), FadeIn(sharp_lab),
            erk.box.animate.set_fill(VIOLET, opacity=0.32).set_stroke(VIOLET, 5.0),
            erk.label.animate.set_color(TEXT),
            run_time=1.3,
        )

        self.at("open control points")
        # Feedback arrow originates from ERK bottom-left, routes cleanly below/around Target 1 and outside MEK_l up to Paired Raf
        ctrl_lab = T("Control: phosphatases & feedback", size=24, color=RED).move_to([-4.05, 1.55, 0])
        fb_arrow = TipableVMobject(color=RED, stroke_width=4.0)
        fb_arrow.set_points_as_corners([
            [-0.45, -1.70, 0],
            [-1.80, -1.78, 0],
            [-3.50, -1.80, 0],
            [-5.10, -1.80, 0],
            [-5.64, -1.54, 0],
            [-5.64, -0.35, 0],
            [-5.20, 0.55, 0],
            [-3.50, 0.80, 0],
            [-1.68, 0.80, 0],
        ])
        fb_arrow.make_smooth()
        fb_arrow.add_tip(tip_length=0.20, tip_width=0.20)
        self.play(Create(fb_arrow), FadeIn(ctrl_lab), run_time=1.8)
        fb_prog = ValueTracker(0.0)
        fb_dot = always_redraw(lambda: Dot(fb_arrow.point_from_proportion(fb_prog.get_value()), radius=0.14, color=RED))
        self.add(fb_dot)
        self.play(fb_prog.animate.set_value(1.0), run_time=2.4, rate_func=linear)
        self.remove(fb_dot)

        self.at("narrow pipe")
        pipe_l = Line(mek_l.get_bottom() + DOWN * 0.05, erk.get_top() + LEFT * 0.35 + UP * 0.05, color=BLUE, stroke_width=5.5)
        pipe_c = Line(mek_c.get_bottom() + DOWN * 0.05, erk.get_top() + UP * 0.05, color=BLUE, stroke_width=5.5)
        pipe_r = Line(mek_r.get_bottom() + DOWN * 0.05, erk.get_top() + RIGHT * 0.35 + UP * 0.05, color=BLUE, stroke_width=5.5)
        pipe_lab = T("Narrow pipe", size=24, color=BLUE, weight=BOLD).move_to([-3.20, -0.88, 0])
        self.play(Create(pipe_l), Create(pipe_c), Create(pipe_r), FadeIn(pipe_lab), run_time=1.5)
        # Prominent signal packets funnel from all 3 MEKs down the narrow pipe into ERK
        pipe_prog = ValueTracker(0.0)
        p_dots = always_redraw(lambda: VGroup(
            Dot(pipe_l.point_from_proportion(pipe_prog.get_value()), radius=0.14, color=YELLOW),
            Dot(pipe_c.point_from_proportion(pipe_prog.get_value()), radius=0.14, color=YELLOW),
            Dot(pipe_r.point_from_proportion(pipe_prog.get_value()), radius=0.14, color=YELLOW),
        ))
        self.add(p_dots)
        self.play(
            pipe_prog.animate.set_value(1.0),
            erk.box.animate.set_fill(VIOLET, opacity=0.45),
            run_time=2.5, rate_func=linear,
        )
        self.remove(p_dots)

        self.at("fans out widely")
        fan_l = Arrow(erk.get_left() + LEFT * 0.08, t_left.get_right() + RIGHT * 0.08, buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)
        fan_r = Arrow([1.62, -1.32, 0], t_right.get_left() + LEFT * 0.08, buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)
        fan_n1 = Arrow(erk.get_bottom() + LEFT * 0.3 + DOWN * 0.06, [-0.9, -2.55, 0], buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)
        fan_n2 = Arrow(erk.get_bottom() + RIGHT * 0.3 + DOWN * 0.06, [0.9, -2.55, 0], buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)
        fan_lab = T("Wide fan", size=26, color=VIOLET, weight=BOLD).move_to([2.6, -1.72, 0])
        self.play(
            Create(fan_l), Create(fan_r), Create(fan_n1), Create(fan_n2),
            FadeIn(fan_lab),
            t_left.box.animate.set_stroke(VIOLET, 3.5).set_fill(VIOLET, opacity=0.22),
            t_right.box.animate.set_stroke(VIOLET, 3.5).set_fill(VIOLET, opacity=0.22),
            stage.gene_bar.animate.set_stroke(GOLD, 3.5).set_fill(GOLD, opacity=0.28),
            stage.gene_lab.animate.set_color(GOLD),
            run_time=1.4,
        )
        t_prog = ValueTracker(0.0)
        tracers = always_redraw(lambda: VGroup(
            Dot(fan_l.point_from_proportion(t_prog.get_value()), radius=0.14, color=YELLOW),
            Dot(fan_r.point_from_proportion(t_prog.get_value()), radius=0.14, color=YELLOW),
            Dot(fan_n1.point_from_proportion(t_prog.get_value()), radius=0.14, color=YELLOW),
            Dot(fan_n2.point_from_proportion(t_prog.get_value()), radius=0.14, color=YELLOW),
        ))
        self.add(tracers)
        self.play(t_prog.animate.set_value(1.0), run_time=2.0, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S09 Targets & Scaffolds
class S09TargetsScaffolds(SpokenScene):
    def construct(self):
        # Bottom half: indigo nucleus where ERK -> Elk-1 -> c-fos occurs
        nuc = RoundedRectangle(
            corner_radius=0.45, width=11.8, height=3.35,
            stroke_color=INDIGO, stroke_width=3.5, fill_color=NUC_FILL, fill_opacity=1.0,
        ).move_to([0.0, -1.75, 0])
        nuc_title = T("Nucleus", size=24, color=INDIGO, weight=BOLD).move_to([-4.95, -0.42, 0])

        erk_n = make_block("ERK", VIOLET, width=1.55, height=0.72, fill_opacity=0.32, stroke_width=4.5, font_size=26).move_to([-4.2, -1.25, 0])
        elk = make_block("Elk-1", VIOLET, width=1.75, height=0.72, fill_opacity=0.16, stroke_width=3.0, font_size=26).move_to([-1.2, -1.25, 0])
        cfos = make_block("c-fos", DIM_STROKE, width=1.9, height=0.62, fill_opacity=0.85, stroke_width=3.0, font_size=26, text_color=TEXT).move_to([1.6, -2.55, 0])
        dna_l = Line([-2.0, -2.55, 0], [cfos.get_left()[0], -2.55, 0], color=INDIGO, stroke_width=4.5)
        dna_r = Line([cfos.get_right()[0], -2.55, 0], [4.4, -2.55, 0], color=INDIGO, stroke_width=4.5)
        dna = VGroup(dna_l, dna_r)

        ieg_line1 = T("Immediate early genes", size=24, color=GOLD, weight=BOLD).move_to([2.90, -0.82, 0])
        ieg_line2 = T("= first genes on, within minutes", size=24, color=GOLD).move_to([2.90, -1.25, 0])

        # Top half: cytosol module with cyan KSR scaffold + parallel JNK & p38 lanes (on-screen context)
        row_ys = [2.72, 1.88, 1.04]
        raf_b = make_block("Raf", GREEN, width=1.28, height=0.44, fill_opacity=0.26, font_size=24).move_to([-2.85, row_ys[0], 0])
        mek_b = make_block("MEK", BLUE, width=1.28, height=0.44, fill_opacity=0.26, font_size=24).move_to([-2.85, row_ys[1], 0])
        erk_b = make_block("ERK", VIOLET, width=1.28, height=0.44, fill_opacity=0.26, font_size=24).move_to([-2.85, row_ys[2], 0])
        a1 = Arrow(raf_b.get_bottom() + DOWN * 0.04, mek_b.get_top() + UP * 0.04, buff=0, color=GREEN, stroke_width=3.5, tip_length=0.14)
        a2 = Arrow(mek_b.get_bottom() + DOWN * 0.04, erk_b.get_top() + UP * 0.04, buff=0, color=BLUE, stroke_width=3.5, tip_length=0.14)
        erk_lane = VGroup(raf_b, mek_b, erk_b, a1, a2)

        sc_x = -3.75
        ksr_spine = Line([sc_x, 2.96, 0], [sc_x, 0.80, 0], color=TEAL, stroke_width=6)
        ksr_arm1 = Line([sc_x, row_ys[0], 0], [raf_b.get_left()[0], row_ys[0], 0], color=TEAL, stroke_width=4)
        ksr_arm2 = Line([sc_x, row_ys[1], 0], [mek_b.get_left()[0], row_ys[1], 0], color=TEAL, stroke_width=4)
        ksr_arm3 = Line([sc_x, row_ys[2], 0], [erk_b.get_left()[0], row_ys[2], 0], color=TEAL, stroke_width=4)
        ksr_lab = T("Scaffold (KSR)", size=24, color=TEAL, weight=BOLD).move_to([-4.98, row_ys[1], 0])
        sc_note = T("Scaffolds hold each module together", size=24, color=TEAL).move_to([-3.35, 0.26, 0])
        ksr = VGroup(ksr_spine, ksr_arm1, ksr_arm2, ksr_arm3, ksr_lab)

        def make_stress_lane(x, end_name):
            t1 = make_block("MAP3K", GREY, width=1.42, height=0.44, fill_opacity=0.14, font_size=24, text_color=TEXT).move_to([x, row_ys[0], 0])
            t2 = make_block("MAP2K", GREY, width=1.42, height=0.44, fill_opacity=0.14, font_size=24, text_color=TEXT).move_to([x, row_ys[1], 0])
            t3 = make_block(end_name, GREY, width=1.42, height=0.44, fill_opacity=0.20, font_size=24, text_color=TEXT).move_to([x, row_ys[2], 0])
            ar1 = Arrow(t1.get_bottom() + DOWN * 0.04, t2.get_top() + UP * 0.04, buff=0, color=GREY, stroke_width=3, tip_length=0.13)
            ar2 = Arrow(t2.get_bottom() + DOWN * 0.04, t3.get_top() + UP * 0.04, buff=0, color=GREY, stroke_width=3, tip_length=0.13)
            lbl = T(f"{end_name} pathway", size=24, color=TEXT).move_to([x, 0.26, 0])
            return VGroup(t1, t2, t3, ar1, ar2, lbl)

        jnk_lane = make_stress_lane(1.65, "JNK")
        p38_lane = make_stress_lane(4.45, "p38")
        stress_head = T("Parallel stress cascades: JNK, p38", size=24, color=TEXT).move_to([3.05, 3.28, 0])

        self.play(
            FadeIn(nuc), FadeIn(nuc_title), FadeIn(erk_n), FadeIn(elk), FadeIn(dna), FadeIn(cfos),
            FadeIn(erk_lane), FadeIn(ksr),
            run_time=0.7,
        )

        self.at("phosphorylates")
        arr_e = Arrow(erk_n.get_right() + RIGHT * 0.06, elk.get_left() + LEFT * 0.06, buff=0, color=VIOLET, stroke_width=4, tip_length=0.16)
        p_elk = make_p_badge("P", YELLOW, radius=0.23, font_size=22).move_to(erk_n.get_right() + RIGHT * 0.1)
        self.play(
            Create(arr_e),
            p_elk.animate.move_to(elk.get_top() + UP * 0.28),
            elk.box.animate.set_fill(VIOLET, opacity=0.32).set_stroke(VIOLET, 4.5),
            run_time=1.35,
        )

        self.at("switch on")
        arr_gene = Arrow(elk.get_bottom() + DOWN * 0.05, cfos.get_left() + LEFT * 0.1 + UP * 0.25, buff=0, color=GOLD, stroke_width=4, tip_length=0.16)
        self.play(
            Create(arr_gene),
            cfos.box.animate.set_stroke(GOLD, 4.5).set_fill(GOLD, opacity=0.32),
            cfos.label.animate.set_color(GOLD),
            FadeIn(jnk_lane, shift=LEFT * 0.2),
            FadeIn(p38_lane, shift=LEFT * 0.2),
            FadeIn(stress_head),
            FadeIn(sc_note),
            run_time=1.6,
        )

        self.at("immediate early gene")
        tx_prog = ValueTracker(0.0)
        tx_dot = always_redraw(lambda: Dot(
            [cfos.get_right()[0] + tx_prog.get_value() * (4.4 - cfos.get_right()[0]), -2.55, 0.0],
            radius=0.10, color=GOLD,
        ))
        self.add(tx_dot)
        self.play(FadeIn(ieg_line1), tx_prog.animate.set_value(1.0), run_time=1.4, rate_func=linear)

        self.at("first genes on")
        sig_prog = ValueTracker(0.0)
        sig_dot = always_redraw(lambda: Dot(
            a1.point_from_proportion(min(1.0, sig_prog.get_value() * 2.0))
            if sig_prog.get_value() < 0.5
            else a2.point_from_proportion((sig_prog.get_value() - 0.5) * 2.0),
            radius=0.10, color=YELLOW,
        ))
        self.add(sig_dot)
        self.play(
            AnimationGroup(
                FadeIn(ieg_line2, run_time=0.55),
                sig_prog.animate(run_time=1.7, rate_func=linear).set_value(1.0),
            )
        )
        self.finish()


# ------------------------------------------------------------------ S10 Close
class S10Close(SpokenScene):
    def construct(self):
        stage = make_cell_stage(mem_y=2.65, mem_h=0.48, nuc_top=-2.0, show_labels=False)
        rtk = make_rtk(x=0.0, mem_top=stage.mem_top_y, mem_bot=stage.mem_bot_y, tail_y=1.95, active=True)
        gf = Dot(radius=0.2, color=GOLD).move_to(rtk.cup_center)

        ras = make_block("Ras-GTP", CORAL, width=1.9, height=0.62, fill_opacity=0.28, font_size=26).move_to([-1.25, 1.38, 0])
        raf = make_block("Paired Raf", GREEN, width=2.0, height=0.62, fill_opacity=0.28, font_size=26).move_to([1.35, 1.38, 0])
        grip_arr = Arrow(ras.get_right() + RIGHT * 0.06, raf.get_left() + LEFT * 0.06, buff=0, color=CORAL, stroke_width=4.5, tip_length=0.16)

        mek = make_block("MEK (narrow pipe)", BLUE, width=3.1, height=0.62, fill_opacity=0.26, font_size=26).move_to([1.35, 0.25, 0])
        erk = make_block("ERK (2-P)", VIOLET, width=2.2, height=0.62, fill_opacity=0.28, font_size=26).move_to([1.35, -0.88, 0])

        sc_x = 3.65
        ksr = VGroup(
            Line([sc_x, 1.65, 0], [sc_x, -1.15, 0], color=TEAL, stroke_width=6),
            Line([sc_x, 1.38, 0], [raf.get_right()[0] + 0.05, 1.38, 0], color=TEAL, stroke_width=4),
            Line([sc_x, 0.25, 0], [mek.get_right()[0] + 0.05, 0.25, 0], color=TEAL, stroke_width=4),
            Line([sc_x, -0.88, 0], [erk.get_right()[0] + 0.05, -0.88, 0], color=TEAL, stroke_width=4),
            T("Scaffold", size=24, color=TEAL).move_to([4.55, 0.25, 0]),
        )

        a12 = Arrow(raf.get_bottom() + DOWN * 0.05, mek.get_top() + UP * 0.05, buff=0, color=GREEN, stroke_width=4, tip_length=0.16)
        a23 = Arrow(mek.get_bottom() + DOWN * 0.05, erk.get_top() + UP * 0.05, buff=0, color=BLUE, stroke_width=4, tip_length=0.16)

        p_left = make_block("Cytoplasmic targets", VIOLET, width=2.8, height=0.58, fill_opacity=0.18, font_size=24).move_to([-3.8, -1.05, 0])
        fan_c = Arrow(erk.get_left() + LEFT * 0.06, p_left.get_right() + RIGHT * 0.06, buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)
        fan_g = Arrow(erk.get_bottom() + DOWN * 0.06, [0.9, -2.55, 0], buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)

        self.play(
            FadeIn(stage), FadeIn(rtk), FadeIn(gf),
            FadeIn(ras), FadeIn(raf), FadeIn(grip_arr),
            run_time=1.2,
        )
        # Receptor-to-Ras activation dot glides cleanly while narration introduces the chain
        init_dot = Dot(rtk.tail_bar.get_bottom(), radius=0.09, color=YELLOW)
        self.add(init_dot)
        self.play(init_dot.animate.move_to(ras.get_top() + UP * 0.05), run_time=2.2, rate_func=linear)
        self.remove(init_dot)

        self.at("gripping RAF")
        self.play(
            ras.box.animate.set_stroke(YELLOW, 4.5),
            raf.box.animate.set_stroke(YELLOW, 4.5),
            run_time=1.4,
        )

        self.at("Three kinases in series")
        self.play(
            FadeIn(mek), FadeIn(erk), FadeIn(ksr),
            Create(a12), Create(a23),
            run_time=1.5,
        )

        self.at("amplify")
        tag_amp = T("Amplify", size=26, color=GREEN, weight=BOLD).move_to([-3.4, 0.72, 0])
        self.play(FadeIn(tag_amp), mek.box.animate.set_fill(BLUE, opacity=0.38), run_time=0.75)

        self.at("sharpen")
        tag_sharp = T("Sharpen", size=26, color=VIOLET, weight=BOLD).move_to([-3.4, 0.22, 0])
        self.play(FadeIn(tag_sharp), erk.box.animate.set_fill(VIOLET, opacity=0.38), run_time=0.75)

        self.at("control that signal")
        tag_ctrl = T("Control", size=26, color=RED, weight=BOLD).move_to([-3.4, -0.28, 0])
        self.play(FadeIn(tag_ctrl), run_time=0.9)

        self.at("Finally")
        self.play(
            FadeIn(p_left), Create(fan_c), Create(fan_g),
            stage.gene_bar.animate.set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.32),
            stage.gene_lab.animate.set_color(GOLD),
            run_time=1.0,
        )

        f_prog = ValueTracker(0.0)
        ft = always_redraw(lambda: VGroup(
            Dot(fan_c.point_from_proportion(f_prog.get_value()), radius=0.14, color=YELLOW),
            Dot(fan_g.point_from_proportion(f_prog.get_value()), radius=0.14, color=YELLOW),
        ))
        self.add(ft)
        self.play(f_prog.animate.set_value(1.0), run_time=1.9, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S11 End
class S11End(EndCard):
    LINE = "A three-kinase relay can amplify, sharpen, and control a membrane signal."
