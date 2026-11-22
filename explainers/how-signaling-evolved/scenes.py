"""Copy Old Pathways, Mostly at the Top — scenes.py

COLOUR MAP (one colour per concept for the entire film):
  TEAL   (#3FB8C0) : Receptor tyrosine kinases (RTKs) / ancestral receptor layer & original signal
  YELLOW (#F5D547) : EGF receptors / evolved new-job receptor & new signal
  RED    (#FC6255) : Downstream kinase core (MAP kinases / Ras hub)
  BLUE   (#58C4DD) : Whole kinome / comparative baseline (all protein kinases, yeast, invertebrates)
  GREEN  (#83C167) : Active functional gene copy / tissue regulatory DNA switches (Gut / Nerve)
  GREY   (#8B93A1) : Cell membrane bilayer, 1.0x reference lines, decayed pseudogene
  TEXT   (#E8EAF0) : Headings, labels, and live readouts

CARRIED WORLD:
  A two-layer cell cross-section: a grey horizontal membrane strip at the top holding
  transmembrane receptors (TEAL / YELLOW) with extracellular pockets above, and a
  cytoplasmic core below holding downstream kinases and hubs (RED). Every quantitative
  comparison sits beside or directly scales the layers of this same cell.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s01_hook             : Human (518 kinases, 58 RTKs) and yeast (125 midpoint of 120-130 kinases, 0 RTKs)
                         bars and ValueTracker counters grow proportionally (h = count / 550 * max_h) while
                         RTK blocks populate the human membrane strip and catch extracellular signals.
  s02_shared_pathways  : Hypothetical extra pathways on Human collapse; 8 shared animal pathways illuminate
                         in matching Fly/Human pairs; Human's top RTK membrane layer multiplies (1 -> 4)
                         and fires into the RTK slot while the 8-pathway count stays fixed.
  s03_genome_bars      : Ratio numerator/denominator share blocks assemble; 1.0x reference band sweeps to
                         position; gene-adjusted horizontal bars (Amit et al., 2007: 1.2x, 1.8x, 2.5x, 2.9x)
                         grow to computed x-positions beside the carried cell whose layers scale with them.
  s04_duplication      : Single EGF receptor (1) and DNA bar undergo two doublings (1 * 2 = 2, 2 * 2 = 4)
                         driven by a copy counter, with whole-genome doubling waves transforming Fly (1)
                         into Human (4).
  s05_fates_loss_split : Left: spare copy cracks, drains to grey pseudogene, and its output collapses;
                         Right: duplicate copies with Gut and Nerve DNA switches each lose one switch and
                         its corresponding tissue output bar drops to 0, locking both copies in place.
  s06_fates_new        : Spare receptor pocket reshapes from round TEAL cup to wedge YELLOW pocket and
                         catches a triangular YELLOW ligand; family expands to 4 distinct receptors catching
                         4 matching ligands above an unwired cytoplasm.
  s07_predict_setup    : 1-receptor + 3-kinase track (4 genes) replicates into 4 tracks (4 * 4 = 16) on left
                         and funnels 4 receptors into 1 shared 3-kinase core (4 + 3 = 7) on right, with
                         live gene counters and compact genome-bar reminder.
  s09_reveal_and_rule  : 16-gene track dims and exits as 7-gene shared core expands to center; signal waves
                         travel from all 4 receptors into a RED Ras hub (pulsing on arrival), which expands
                         modestly (1 -> 3 linked nodes) to reflect 1.8x core growth.
"""
from bp_parts import *

# Canonical concept colours
C_RTK = TEAL
C_EGF = YELLOW
C_CORE = RED
C_KINOME = BLUE
C_KEEP = GREEN
C_STRUCT = GREY


# ------------------------------------------------------------------ shared world builders
def make_membrane(x0, x1, y, stroke=3.5, color=C_STRUCT):
    """Two parallel bilayer lines spanning [x0, x1] around y."""
    top = Line([x0, y + 0.065, 0], [x1, y + 0.065, 0], color=color, stroke_width=stroke)
    bot = Line([x0, y - 0.065, 0], [x1, y - 0.065, 0], color=color, stroke_width=stroke)
    return VGroup(top, bot)


def make_cytoplasm(x0, x1, y_bot, y_top, color=C_KINOME, fill_opacity=0.15):
    """Subtle filled intracellular compartment below a membrane."""
    w = x1 - x0
    h = y_top - y_bot
    return Rectangle(
        width=w, height=h,
        stroke_width=0,
        fill_color=color, fill_opacity=fill_opacity,
    ).move_to([(x0 + x1) / 2.0, (y_bot + y_top) / 2.0, 0])


def make_receptor(x, y_mem, color=C_RTK, pocket="round", scale=1.0):
    """Transmembrane receptor spanning a membrane at y_mem: pocket above, stem across, tail below."""
    s = scale
    if pocket == "round":
        head = Arc(radius=0.22 * s, start_angle=PI, angle=PI, color=color, stroke_width=5.5 * s)
        head.move_to([x, y_mem + 0.34 * s, 0])
    elif pocket == "wedge":
        p1 = [x - 0.22 * s, y_mem + 0.45 * s, 0]
        p2 = [x, y_mem + 0.22 * s, 0]
        p3 = [x + 0.22 * s, y_mem + 0.45 * s, 0]
        head = VMobject(stroke_color=color, stroke_width=5.5 * s)
        head.set_points_as_corners([p1, p2, p3])
    elif pocket == "square":
        p1 = [x - 0.20 * s, y_mem + 0.45 * s, 0]
        p2 = [x - 0.20 * s, y_mem + 0.22 * s, 0]
        p3 = [x + 0.20 * s, y_mem + 0.22 * s, 0]
        p4 = [x + 0.20 * s, y_mem + 0.45 * s, 0]
        head = VMobject(stroke_color=color, stroke_width=5.5 * s)
        head.set_points_as_corners([p1, p2, p3, p4])
    else:  # diamond / wide cup
        p1 = [x - 0.26 * s, y_mem + 0.42 * s, 0]
        p2 = [x - 0.11 * s, y_mem + 0.22 * s, 0]
        p3 = [x + 0.11 * s, y_mem + 0.22 * s, 0]
        p4 = [x + 0.26 * s, y_mem + 0.42 * s, 0]
        head = VMobject(stroke_color=color, stroke_width=5.5 * s)
        head.set_points_as_corners([p1, p2, p3, p4])

    stem = RoundedRectangle(
        corner_radius=0.06 * s,
        width=0.22 * s,
        height=0.44 * s,
        stroke_color=color,
        stroke_width=3.0 * s,
        fill_color=color,
        fill_opacity=0.55,
    ).move_to([x, y_mem, 0])
    tail = Line([x, y_mem - 0.22 * s, 0], [x, y_mem - 0.46 * s, 0], color=color, stroke_width=5.0 * s)
    return VGroup(head, stem, tail)


def make_ligand(color=C_RTK, shape="round", scale=1.0):
    """Extracellular signal ligand matching a receptor pocket."""
    s = scale
    if shape == "round":
        return Circle(radius=0.14 * s, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.9)
    if shape == "wedge":
        return Triangle(color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.9).rotate(PI).scale(0.18 * s)
    if shape == "square":
        return Square(side_length=0.24 * s, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.9)
    return RegularPolygon(n=4, color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.9).scale(0.18 * s)


def make_kinase_stack(x, y_top, step=0.48, radius=0.16, color=C_CORE):
    """Three-kinase vertical core stack below a membrane."""
    nodes = VGroup()
    links = VGroup()
    for i in range(3):
        cy = y_top - i * step
        c = Circle(radius=radius, color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.40).move_to([x, cy, 0])
        nodes.add(c)
        if i > 0:
            prev_y = y_top - (i - 1) * step
            links.add(Line([x, prev_y - radius, 0], [x, cy + radius, 0], color=color, stroke_width=3.0))
    return VGroup(links, nodes)


def make_genome_bar_reminder():
    """Compact top reminder of the Amit et al. 2007 ratios for S07/S08/S09 (non-overlapping by construction)."""
    lbl = T("Genome bars:", size=24, color=TEXT)
    rtk_bar = Rectangle(width=2.9 * 0.40, height=0.24, stroke_color=C_RTK, stroke_width=1.5, fill_color=C_RTK, fill_opacity=0.88)
    rtk_txt = T("RTKs 2.9×", size=24, color=C_RTK)
    rtk_grp = VGroup(rtk_bar, rtk_txt).arrange(RIGHT, buff=0.14)

    mapk_bar = Rectangle(width=1.8 * 0.40, height=0.24, stroke_color=C_CORE, stroke_width=1.5, fill_color=C_CORE, fill_opacity=0.88)
    mapk_txt = T("MAPKs 1.8×", size=24, color=C_CORE)
    mapk_grp = VGroup(mapk_bar, mapk_txt).arrange(RIGHT, buff=0.14)

    inner = VGroup(lbl, rtk_grp, mapk_grp).arrange(RIGHT, buff=0.45).move_to([0, 3.16, 0])
    box = RoundedRectangle(
        corner_radius=0.12, width=inner.width + 0.70, height=0.72,
        stroke_color=C_STRUCT, stroke_width=2.2, fill_color=BG, fill_opacity=0.92,
    ).move_to(inner)
    return VGroup(box, lbl, rtk_grp, mapk_grp)


def build_s07_s08_panels(show_panels=True):
    """Shared layout builder for S07 end state, S08 Pause backdrop, and S09 start state."""
    tp = TwoPanel("4 separate tracks", "Shared core", colors=(C_KINOME, C_RTK), top=2.60, bottom=-2.25, gap=0.45, width=12.6, size=30)

    # Left panel: 4 separate 1-receptor + 3-kinase tracks = 16 genes
    lx0, lx1 = -5.75, -0.55
    l_xs = np.linspace(-5.05, -1.25, 4)
    l_mem_y = 1.05
    l_cyto = make_cytoplasm(lx0, lx1, -1.35, l_mem_y, color=C_KINOME, fill_opacity=0.13)
    l_mem = make_membrane(lx0, lx1, l_mem_y, stroke=3.0)
    l_recs = VGroup(*[
        make_receptor(x, l_mem_y, color=(C_RTK if i % 2 == 0 else C_EGF),
                      pocket=("round" if i % 2 == 0 else "wedge"), scale=0.75)
        for i, x in enumerate(l_xs)
    ])
    l_stacks = VGroup()
    l_wires = VGroup()
    for x in l_xs:
        st = make_kinase_stack(x, y_top=0.15, step=0.48, radius=0.16, color=C_CORE)
        l_stacks.add(st)
        l_wires.add(Line([x, l_mem_y - 0.35, 0], [x, 0.31, 0], color=C_STRUCT, stroke_width=2.8))
    l_tally = M("4 × 4 = 16 genes", size=28, color=C_KINOME).move_to([-3.15, -1.78, 0])
    left_world = VGroup(l_cyto, l_mem, l_recs, l_wires, l_stacks, l_tally)

    # Right panel: 4 receptors sharing 1 stack of 3 kinases = 7 genes
    rx0, rx1 = 0.55, 5.75
    r_xs = np.linspace(1.25, 5.05, 4)
    r_mem_y = 1.05
    r_cyto = make_cytoplasm(rx0, rx1, -1.35, r_mem_y, color=C_RTK, fill_opacity=0.13)
    r_mem = make_membrane(rx0, rx1, r_mem_y, stroke=3.0)
    r_recs = VGroup(*[
        make_receptor(x, r_mem_y, color=(C_RTK if i % 2 == 0 else C_EGF),
                      pocket=("round" if i % 2 == 0 else "wedge"), scale=0.75)
        for i, x in enumerate(r_xs)
    ])
    r_stack = make_kinase_stack(3.15, y_top=0.15, step=0.48, radius=0.19, color=C_CORE)
    r_wires = VGroup(*[
        Line([x, r_mem_y - 0.35, 0], [3.15, 0.34, 0], color=C_RTK, stroke_width=2.8)
        for x in r_xs
    ])
    r_tally = M("4 + 3 = 7 genes", size=28, color=C_RTK).move_to([3.15, -1.78, 0])
    right_world = VGroup(r_cyto, r_mem, r_recs, r_wires, r_stack, r_tally)

    reminder = make_genome_bar_reminder()
    if not show_panels:
        return reminder, tp, left_world, right_world
    return VGroup(reminder, tp, left_world, right_world)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "How Signaling Evolved"
    TITLE = "Copy Old Pathways, Mostly at the Top"


class S01Hook(SpokenScene):
    def construct(self):
        # Computed vertical column chart (0..550 kinases) + carried top-layer cell preview
        base_y = -2.25
        max_h = 4.30
        scale_y = max_h / 550.0
        col_w = 2.55

        yeast_x = -2.75
        human_x = 1.85

        # Y-axis with clean ticks (no interior dashed gridlines crossing live readouts)
        y_axis = Line([-4.65, base_y, 0], [-4.65, base_y + max_h, 0], color=C_STRUCT, stroke_width=2.5)
        base = Line([-4.65, base_y, 0], [3.75, base_y, 0], color=C_STRUCT, stroke_width=3.0)
        yticks = VGroup()
        for val in [0, 100, 200, 300, 400, 500]:
            gy = base_y + val * scale_y
            yticks.add(Line([-4.65, gy, 0], [-4.77, gy, 0], color=C_STRUCT, stroke_width=2.5))
            yticks.add(M(f"{val}", size=22, color=TEXT).move_to([-5.18, gy, 0]))

        yeast_lbl = T("Baker's yeast", size=30, color=C_KINOME).move_to([yeast_x, -2.78, 0])
        human_lbl = T("Human", size=30, color=C_RTK).move_to([human_x, -2.78, 0])

        # Carried cell top-layer card on right (x = 4.05 .. 6.25)
        cell_panel = RoundedRectangle(
            corner_radius=0.18, width=2.25, height=4.10,
            stroke_color=C_RTK, stroke_width=2.5, fill_color=C_KINOME, fill_opacity=0.14,
        ).move_to([5.15, -0.20, 0])
        mem_y = 0.55
        mem = make_membrane(4.20, 6.10, mem_y, stroke=3.0)
        mem_tag = T("top layer", size=24, color=C_RTK).move_to([5.15, 1.55, 0])
        core_hint = Circle(radius=0.22, color=C_CORE, stroke_width=2.5, fill_color=C_CORE, fill_opacity=0.38).move_to([5.15, -1.05, 0])
        core_txt = T("core", size=24, color=C_CORE).next_to(core_hint, DOWN, buff=0.14)

        self.play(
            Create(y_axis), Create(base), FadeIn(yticks),
            FadeIn(yeast_lbl), FadeIn(human_lbl),
            FadeIn(cell_panel), FadeIn(mem), FadeIn(mem_tag), FadeIn(core_hint), FadeIn(core_txt),
            run_time=0.8,
        )

        # Trackers driving bar heights and live numerical readouts
        h_tot = ValueTracker(0.0)
        h_rtk = ValueTracker(0.0)
        y_tot = ValueTracker(0.0)

        human_bar = always_redraw(lambda: Rectangle(
            width=col_w,
            height=max(0.02, h_tot.get_value() * scale_y),
            stroke_color=C_KINOME, stroke_width=2.5,
            fill_color=C_KINOME, fill_opacity=0.40,
        ).move_to([human_x, base_y + max(0.02, h_tot.get_value() * scale_y) / 2.0, 0]))

        human_num = always_redraw(lambda: M(
            f"{int(round(h_tot.get_value()))} kinases", size=28, color=TEXT,
        ).move_to([human_x, base_y + max(40.0, h_tot.get_value()) * scale_y + 0.34, 0]))

        self.at("Human")
        self.add(human_bar, human_num)
        self.play(h_tot.animate.set_value(518), run_time=1.4, rate_func=smooth)

        # 58 RTKs band at top of Human column
        rtk_band = always_redraw(lambda: Rectangle(
            width=col_w,
            height=max(0.02, h_rtk.get_value() * scale_y),
            stroke_color=C_RTK, stroke_width=2.5,
            fill_color=C_RTK, fill_opacity=0.85,
        ).move_to([human_x, base_y + 518 * scale_y - max(0.02, h_rtk.get_value() * scale_y) / 2.0, 0]))

        rtk_num = always_redraw(lambda: M(
            f"{int(round(h_rtk.get_value()))} RTKs", size=28, color=C_RTK,
        ).move_to([human_x - 2.18, 1.56, 0]))

        rtk_recs = VGroup(*[
            make_receptor(x, mem_y, color=C_RTK, pocket="round", scale=0.66)
            for x in [4.55, 5.15, 5.75]
        ])
        rtk_ligs = VGroup(*[
            make_ligand(C_RTK, "round", scale=0.66).move_to([x, mem_y + 0.68, 0])
            for x in [4.55, 5.15, 5.75]
        ])

        self.at("including")
        self.add(rtk_band, rtk_num)
        self.play(
            h_rtk.animate.set_value(58),
            LaggedStart(*[FadeIn(r, shift=DOWN * 0.12) for r in rtk_recs], lag_ratio=0.22),
            run_time=1.0,
        )
        self.play(FadeIn(rtk_ligs), run_time=0.35)
        self.play(*[rtk_ligs[i].animate.move_to([x, mem_y + 0.25, 0]) for i, x in enumerate([4.55, 5.15, 5.75])], run_time=0.9)

        # Yeast column: rises to midpoint 125, settles to "120-130 kinases"
        yeast_bar = always_redraw(lambda: Rectangle(
            width=col_w,
            height=max(0.02, y_tot.get_value() * scale_y),
            stroke_color=C_KINOME, stroke_width=2.5,
            fill_color=C_KINOME, fill_opacity=0.40,
        ).move_to([yeast_x, base_y + max(0.02, y_tot.get_value() * scale_y) / 2.0, 0]))

        yeast_live = always_redraw(lambda: M(
            f"{int(round(y_tot.get_value()))} kinases", size=28, color=TEXT,
        ).move_to([yeast_x, base_y + max(40.0, y_tot.get_value()) * scale_y + 0.34, 0]))

        self.at("yeast")
        self.add(yeast_bar, yeast_live)
        self.play(y_tot.animate.set_value(125), run_time=2.6, rate_func=smooth)

        yeast_settled = M("120–130 kinases", size=28, color=TEXT).move_to([yeast_x, base_y + 125 * scale_y + 0.34, 0])
        self.remove(yeast_live)
        self.add(yeast_settled)

        # Empty 0 RTK slot on Yeast + clean comparison highlight
        slot_y = yeast_settled.get_top()[1] + 0.24
        zero_slot = DashedLine(
            [yeast_x - col_w / 2.0, slot_y, 0],
            [yeast_x + col_w / 2.0, slot_y, 0],
            color=C_RTK, stroke_width=3.0, dash_length=0.14,
        )
        zero_lbl = M("0 RTKs", size=28, color=C_RTK).next_to(zero_slot, UP, buff=0.16)

        self.at("none of those")
        self.play(Create(zero_slot), run_time=0.9)
        self.play(FadeIn(zero_lbl), run_time=0.45)

        # Highlight comparison arrow between 0 RTKs and 58 RTKs before question
        cmp_arr = DashedLine(zero_lbl.get_right() + RIGHT * 0.15, rtk_num.get_left() + LEFT * 0.15, color=GOLD, stroke_width=2.5, dash_length=0.14)
        self.play(Create(cmp_arr), run_time=1.0)

        # Closing hook question
        q_badge = boxed_label("Where did ours come from?", color=GOLD, size=30).move_to([-0.4, 2.95, 0])
        self.at("where did ours")
        self.play(FadeIn(q_badge, shift=DOWN * 0.12), run_time=0.55)
        self.finish()


class S02SharedPathways(SpokenScene):
    def construct(self):
        tp = TwoPanel("Fruit fly", "Human", colors=(C_KINOME, C_RTK), top=3.05, bottom=-2.45, gap=0.45, width=12.6, size=32)

        # Two-layer cell interiors + membranes inside each panel
        fly_cyto = make_cytoplasm(-5.85, -0.50, -2.20, 1.50, color=C_KINOME, fill_opacity=0.14)
        hum_cyto = make_cytoplasm(0.50, 5.85, -2.20, 1.50, color=C_RTK, fill_opacity=0.14)
        fly_mem = make_membrane(-5.85, -0.50, 1.50, stroke=3.0)
        hum_mem = make_membrane(0.50, 5.85, 1.50, stroke=3.0)
        self.play(FadeIn(tp), FadeIn(fly_cyto), FadeIn(hum_cyto), FadeIn(fly_mem), FadeIn(hum_mem), run_time=0.4)

        # Beat 1: hypothetical dozens of new pathways on Human side
        hyp_boxes = VGroup()
        for r in range(4):
            for c in range(3):
                bx = 1.65 + c * 1.50
                by = 0.82 - r * 0.62
                d = RoundedRectangle(
                    corner_radius=0.1, width=1.25, height=0.44,
                    stroke_color=GOLD, stroke_width=2.2, fill_color=GOLD, fill_opacity=0.20,
                ).move_to([bx, by, 0])
                hyp_boxes.add(d)
        hyp_txt = T("dozens of new pathways?", size=26, color=GOLD).move_to([3.15, -1.80, 0])

        self.at("expect humans")
        self.play(FadeIn(hyp_txt), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(b, scale=0.85) for b in hyp_boxes], lag_ratio=0.12), run_time=3.1)

        # Beat 2: collapse hypothetical boxes cleanly and stage 8 faint pathway slots
        names = ["GPCR", "Nuclear", "TGF-beta", "Notch", "JAK-STAT", "Hedgehog", "Wnt", "RTK"]
        fly_chips, hum_chips = VGroup(), VGroup()
        fly_slots, hum_slots = VGroup(), VGroup()
        for idx, nm in enumerate(names):
            col_idx = idx % 2
            row_idx = idx // 2
            col_c = C_RTK if nm == "RTK" else C_KINOME
            fy = 0.70 - row_idx * 0.78
            fx = -4.55 + col_idx * 2.80
            hx = 1.75 + col_idx * 2.80
            fc = boxed_label(nm, color=col_c, size=24, box=(2.45, 0.54), pad=0.14).move_to([fx, fy, 0])
            hc = boxed_label(nm, color=col_c, size=24, box=(2.45, 0.54), pad=0.14).move_to([hx, fy, 0])
            fly_chips.add(fc)
            hum_chips.add(hc)
            fly_slots.add(RoundedRectangle(corner_radius=0.12, width=2.45, height=0.54, stroke_color=C_STRUCT, stroke_width=1.5, fill_opacity=0).move_to([fx, fy, 0]).set_stroke(opacity=0.35))
            hum_slots.add(RoundedRectangle(corner_radius=0.12, width=2.45, height=0.54, stroke_color=C_STRUCT, stroke_width=1.5, fill_opacity=0).move_to([hx, fy, 0]).set_stroke(opacity=0.35))

        fly_rec = make_receptor(-3.15, 1.50, color=C_RTK, pocket="round", scale=0.72)
        hum_rec = make_receptor(1.25, 1.50, color=C_RTK, pocket="round", scale=0.72)

        self.at("Genomes show the opposite")
        self.play(FadeOut(hyp_boxes, scale=0.6), FadeOut(hyp_txt), run_time=1.0)
        self.play(
            FadeIn(fly_rec, shift=DOWN * 0.15), FadeIn(hum_rec, shift=DOWN * 0.15),
            LaggedStart(*[FadeIn(s) for s in fly_slots], lag_ratio=0.06),
            LaggedStart(*[FadeIn(s) for s in hum_slots], lag_ratio=0.06),
            run_time=1.4,
        )

        # Beat 3: 8 core animal pathways illuminate symmetrically in Fly & Human
        count_t = ValueTracker(0)
        shared_cnt = always_redraw(lambda: M(
            f"Shared core pathways: {int(round(count_t.get_value()))}", size=28, color=TEXT,
        ).move_to([0, -2.95, 0]))

        self.at("Fruit flies")
        self.add(shared_cnt)
        for i in range(8):
            self.play(
                FadeOut(fly_slots[i]), FadeOut(hum_slots[i]),
                FadeIn(fly_chips[i], shift=RIGHT * 0.08),
                FadeIn(hum_chips[i], shift=RIGHT * 0.08),
                count_t.animate.set_value(i + 1),
                run_time=0.35,
            )

        # Beat 4: Human top receptor layer multiplies (1 -> 4) evenly spaced across membrane
        extra_hum_recs = VGroup(*[
            make_receptor(x, 1.50, color=(C_RTK if j % 2 == 0 else C_EGF),
                          pocket=("round" if j % 2 == 0 else "wedge"), scale=0.72)
            for j, x in enumerate([2.50, 3.75, 5.00], start=1)
        ])
        fly_1 = T("1 copy at top", size=24, color=C_KINOME).move_to([-1.65, 1.98, 0])
        hum_copy = T("more copies at top", size=24, color=C_RTK).move_to([3.15, 2.15, 0])

        self.at("What changed")
        self.play(FadeIn(fly_1), run_time=0.4)
        for idx, r in enumerate(extra_hum_recs, start=2):
            anims = [TransformFromCopy(hum_rec, r)]
            if idx == 2:
                anims.append(FadeIn(hum_copy))
            self.play(*anims, run_time=0.95)
        top_hl = SurroundingRectangle(VGroup(hum_rec, extra_hum_recs), color=C_RTK, buff=0.08, stroke_width=2.5)
        self.play(Create(top_hl), run_time=0.7)
        # Single signal pulse routed down the right margin outside all chips to RTK slot
        pulse_dot = Dot(radius=0.09, color=C_RTK).move_to([5.00, 1.15, 0])
        pulse_path = VMobject()
        pulse_path.set_points_as_corners([
            [5.00, 1.15, 0],
            [6.02, 1.15, 0],
            [6.02, hum_chips[7].get_center()[1], 0],
            hum_chips[7].get_right() + RIGHT * 0.10,
        ])
        self.add(pulse_dot)
        self.play(MoveAlongPath(pulse_dot, pulse_path), run_time=0.9, rate_func=linear)
        self.play(FadeOut(pulse_dot), run_time=0.2)
        self.finish()


class S03GenomeBars(SpokenScene):
    def construct(self):
        title = T("Human vs. 4 invertebrates (gene-adjusted)", size=32, color=TEXT).move_to([-0.2, 3.25, 0])
        src = scope_tag("Amit et al., 2007")

        # Carried cell on right (x = 1.95 .. 6.15, y = -2.35 .. 1.90)
        cell_box = RoundedRectangle(
            corner_radius=0.2, width=4.20, height=4.25,
            stroke_color=C_KINOME, stroke_width=2.5, fill_color=C_KINOME, fill_opacity=0.14,
        ).move_to([4.05, -0.22, 0])
        cell_head = T("Cell layers", size=26, color=TEXT).move_to([4.05, 1.58, 0])
        mem_y = 0.55
        mem = make_membrane(2.20, 5.90, mem_y, stroke=3.0)
        base_rec = make_receptor(3.25, mem_y, color=C_RTK, pocket="round", scale=0.74)
        base_egf = make_receptor(4.85, mem_y, color=C_EGF, pocket="wedge", scale=0.74)
        top_lbl = T("receptors", size=24, color=C_RTK).move_to([4.05, 1.15, 0])
        core_dot = Circle(radius=0.30, color=C_CORE, stroke_width=3.0, fill_color=C_CORE, fill_opacity=0.45).move_to([4.05, -1.00, 0])
        core_lbl = T("core", size=24, color=C_CORE).next_to(core_dot, DOWN, buff=0.16)

        # Horizontal bar chart frame on left (x0 = -3.05, x1 = 1.25 -> 0..3.3x)
        x0, x1 = -3.05, 1.25
        xr_max = 3.3
        x_at = lambda v: x0 + (v / xr_max) * (x1 - x0)
        y_rows = [1.00, 0.12, -0.76, -1.64]
        axis_y = -2.30

        x_axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=C_STRUCT, stroke_width=3)
        y_axis = Line([x0, axis_y, 0], [x0, 1.50, 0], color=C_STRUCT, stroke_width=3)
        xticks = VGroup()
        for tv in [0, 1, 2, 3]:
            tx = x_at(tv)
            xticks.add(Line([tx, axis_y, 0], [tx, axis_y - 0.10, 0], color=C_STRUCT, stroke_width=2.5))
            xticks.add(M(f"{tv}×", size=22, color=TEXT).move_to([tx, axis_y - 0.34, 0]))

        self.play(
            FadeIn(title), FadeIn(src),
            FadeIn(cell_box), FadeIn(cell_head), FadeIn(mem),
            FadeIn(base_rec), FadeIn(base_egf), FadeIn(top_lbl),
            FadeIn(core_dot), FadeIn(core_lbl),
            run_time=1.0,
        )

        # Beat 1: adjusting for gene number
        adj_tag = boxed_label("adjusted for total gene count", color=C_KINOME, size=24).move_to([-0.9, 1.95, 0])
        self.at("adjusting for gene")
        self.play(FadeIn(adj_tag, shift=DOWN * 0.08), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(adj_tag), run_time=0.45)

        # Formula builds piece by piece above the chart (y = 2.38)
        eq_lhs = M("ratio =", size=26, color=TEXT)
        eq_num = M("(family ÷ all genes, human)", size=24, color=C_RTK)
        eq_div = M("÷", size=26, color=TEXT)
        eq_den = M("(family ÷ all genes, inv.)", size=24, color=C_KINOME)
        VGroup(eq_lhs, eq_num, eq_div, eq_den).arrange(RIGHT, buff=0.16).move_to([-0.2, 2.38, 0])

        # Visual share blocks strictly to the right of y_axis
        h_s_lbl = T("human share", size=24, color=C_RTK).move_to([-1.85, 0.32, 0])
        h_share = Rectangle(width=1.45, height=0.44, stroke_color=C_RTK, stroke_width=2, fill_color=C_RTK, fill_opacity=0.65).next_to(h_s_lbl, RIGHT, buff=0.22)
        div_bar = Line([-2.70, -0.22, 0], [0.95, -0.22, 0], color=TEXT, stroke_width=2.5)
        i_s_lbl = T("inv. share", size=24, color=C_KINOME).move_to([-1.85, -0.76, 0])
        i_share = Rectangle(width=0.90, height=0.44, stroke_color=C_KINOME, stroke_width=2, fill_color=C_KINOME, fill_opacity=0.65).next_to(i_s_lbl, RIGHT, buff=0.35)

        self.at("Each ratio")
        self.play(FadeIn(eq_lhs), FadeIn(eq_num), FadeIn(h_s_lbl), run_time=0.5)
        self.play(GrowFromEdge(h_share, LEFT), run_time=1.8)
        self.play(FadeIn(eq_div), FadeIn(eq_den), FadeIn(i_s_lbl), run_time=0.5)
        self.play(Create(div_bar), GrowFromEdge(i_share, LEFT), run_time=1.8)
        self.play(FadeOut(h_share), FadeOut(h_s_lbl), FadeOut(div_bar), FadeOut(i_share), FadeOut(i_s_lbl), run_time=0.55)
        self.play(Create(x_axis), Create(y_axis), FadeIn(xticks), run_time=0.8)

        # 1.0x reference line + active sweep from 0 to 1.0x
        ref_x = x_at(1.0)
        ref_line = DashedLine([ref_x, axis_y, 0], [ref_x, 1.50, 0], color=TEXT, stroke_width=2.8, dash_length=0.14).set_opacity(0.45).set_z_index(1)
        ref_lbl = T("1.0× = in step", size=24, color=TEXT).next_to([ref_x, 1.50, 0], UP, buff=0.10)
        sweep = Rectangle(width=ref_x - x0, height=1.50 - axis_y, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([(x0 + ref_x) / 2.0, (axis_y + 1.50) / 2.0, 0])

        self.at("One means growth")
        self.play(FadeIn(ref_lbl), run_time=0.4)
        self.play(Create(ref_line), GrowFromEdge(sweep, LEFT), run_time=1.5)
        self.play(FadeOut(sweep), run_time=0.7)

        # Helper to animate one computed bar + readout
        def grow_bar(y, name, target, col, extra_anim=None, run_t=2.0):
            lbl = T(name, size=24, color=col).move_to([x0 - 0.18, y, 0], aligned_edge=RIGHT)
            tr = ValueTracker(0.0)
            bar = always_redraw(lambda: Rectangle(
                width=max(0.02, x_at(tr.get_value()) - x0),
                height=0.50,
                stroke_color=col, stroke_width=2,
                fill_color=col, fill_opacity=0.85,
            ).move_to([x0 + max(0.02, x_at(tr.get_value()) - x0) / 2.0, y, 0]).set_z_index(2))
            def _mk_num():
                txt = M(f"{tr.get_value():.1f}×", size=24, color=TEXT).move_to([x_at(tr.get_value()) + 0.45, y, 0]).set_z_index(5)
                bg = Rectangle(
                    width=txt.width + 0.14, height=txt.height + 0.10,
                    stroke_width=0, fill_color=BG, fill_opacity=1.0,
                ).move_to(txt).set_z_index(4)
                return VGroup(bg, txt)
            num = always_redraw(_mk_num)
            self.add(lbl, bar, num)
            anims = [tr.animate.set_value(target)]
            if extra_anim:
                anims.extend(extra_anim)
            self.play(*anims, run_time=run_t, rate_func=smooth)
            return VGroup(lbl, bar, num)

        # 1.2x All kinases
        self.at("All protein kinases")
        grow_bar(y_rows[0], "All kinases", 1.2, C_KINOME, [cell_box.animate.set_fill(C_KINOME, opacity=0.22)], run_t=2.6)

        # 1.8x MAP kinases -> core swells modestly
        self.at("kinases score", nth=1, lead=0.75)
        core_2 = Circle(radius=0.24, color=C_CORE, stroke_width=3, fill_color=C_CORE, fill_opacity=0.55).move_to([3.30, -1.00, 0])
        core_3 = Circle(radius=0.24, color=C_CORE, stroke_width=3, fill_color=C_CORE, fill_opacity=0.55).move_to([4.80, -1.00, 0])
        grow_bar(y_rows[1], "MAP kinases", 1.8, C_CORE, [FadeIn(core_2, scale=0.5), FadeIn(core_3, scale=0.5)], run_t=1.2)

        # 2.5x EGF receptors -> extra EGF receptors appear on membrane
        self.at("EGF receptors")
        egf_2 = make_receptor(5.45, mem_y, color=C_EGF, pocket="wedge", scale=0.74)
        egf_3 = make_receptor(4.30, mem_y, color=C_EGF, pocket="wedge", scale=0.74)
        grow_bar(y_rows[2], "EGF receptors", 2.5, C_EGF, [FadeIn(egf_2, shift=UP * 0.15), FadeIn(egf_3, shift=UP * 0.15)], run_t=1.6)

        # 2.9x All RTKs -> top RTK layer swells visibly
        self.at("Receptor tyrosine kinases")
        rtk_2 = make_receptor(2.65, mem_y, color=C_RTK, pocket="round", scale=0.74)
        rtk_3 = make_receptor(3.78, mem_y, color=C_RTK, pocket="square", scale=0.74)
        grow_bar(
            y_rows[3], "All RTKs", 2.9, C_RTK,
            [FadeIn(rtk_2, shift=UP * 0.15), FadeIn(rtk_3, shift=UP * 0.15)],
            run_t=3.2,
        )
        self.finish()


class S04Duplication(SpokenScene):
    def construct(self):
        mem_y = 0.85
        cyto = make_cytoplasm(-5.5, 5.5, -0.45, mem_y, color=C_KINOME, fill_opacity=0.14)
        mem = make_membrane(-5.5, 5.5, mem_y, stroke=3.5)
        dna_y = -1.15
        dna_bar = Line([-5.2, dna_y, 0], [5.2, dna_y, 0], color=C_KINOME, stroke_width=7)
        dna_lbl = T("genome DNA", size=24, color=C_KINOME).move_to([-4.3, dna_y - 0.55, 0])

        r1 = make_receptor(0.0, mem_y, color=C_EGF, pocket="wedge", scale=0.95)
        g1 = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.40, stroke_color=C_EGF, stroke_width=2.8, fill_color=C_EGF, fill_opacity=0.45).move_to([0.0, dna_y, 0])
        g1_lbl = M("EGF-R", size=22, color=TEXT).next_to(g1, DOWN, buff=0.14)

        count_tr = ValueTracker(1)
        count_read = always_redraw(lambda: M(
            f"EGF receptors: {int(round(count_tr.get_value()))}", size=32, color=C_EGF,
        ).move_to([0, 2.85, 0]))

        self.play(FadeIn(cyto), FadeIn(mem), Create(dna_bar), FadeIn(dna_lbl), FadeIn(r1), FadeIn(g1), FadeIn(g1_lbl), FadeIn(count_read), run_time=0.8)

        # Beat 1: copying errors — single gene or whole genome
        single_badge = boxed_label("single-gene copy", color=C_KINOME, size=26).move_to([-3.2, -2.55, 0])
        whole_badge = boxed_label("whole-genome doubling (×2)", color=C_EGF, size=26).move_to([2.4, -2.55, 0])

        self.at("Copying errors")
        self.play(FadeIn(single_badge, shift=UP * 0.1), run_time=0.5)
        self.wait(0.8)
        self.play(FadeIn(whole_badge, shift=UP * 0.1), run_time=0.5)
        self.play(dna_bar.animate.set_stroke(C_EGF, width=9), run_time=1.8)

        # Beat 2: two whole-genome doublings with visible genome doubling wave
        wgd1 = boxed_label("Doubling 1 (×2)", color=C_EGF, size=26).move_to([-2.4, 2.05, 0])
        wgd2 = boxed_label("Doubling 2 (×2)", color=C_EGF, size=26).move_to([2.4, 2.05, 0])
        wave = Line([-5.2, dna_y + 0.16, 0], [-5.2, dna_y - 0.16, 0], color=TEXT, stroke_width=6)

        self.play(FadeOut(single_badge), FadeOut(whole_badge), run_time=0.4)
        self.at("two whole genome")
        self.play(FadeIn(wgd1), FadeIn(wgd2), run_time=0.45)
        self.add(wave)
        self.play(wave.animate.shift(RIGHT * 10.4), run_time=1.8, rate_func=linear)
        self.remove(wave)

        # Beat 3: 1 * 2 = 2
        r2a = make_receptor(-2.0, mem_y, color=C_EGF, pocket="wedge", scale=0.95)
        r2b = make_receptor(2.0, mem_y, color=C_EGF, pocket="wedge", scale=0.95)
        g2a = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.40, stroke_color=C_EGF, stroke_width=2.8, fill_color=C_EGF, fill_opacity=0.45).move_to([-2.0, dna_y, 0])
        g2b = g2a.copy().move_to([2.0, dna_y, 0])
        g2a_lbl = M("EGF-R", size=22, color=TEXT).next_to(g2a, DOWN, buff=0.14)
        g2b_lbl = M("EGF-R", size=22, color=TEXT).next_to(g2b, DOWN, buff=0.14)
        step1_eq = M("1 × 2 = 2", size=30, color=TEXT).move_to([0, 0.0, 0])

        self.at("One EGF receptor")
        self.play(FadeOut(g1_lbl), FadeIn(step1_eq), run_time=0.35)
        self.play(
            ReplacementTransform(r1, r2a),
            TransformFromCopy(r1, r2b),
            ReplacementTransform(g1, g2a),
            TransformFromCopy(g1, g2b),
            count_tr.animate.set_value(2),
            run_time=1.9,
        )
        self.play(FadeIn(g2a_lbl), FadeIn(g2b_lbl), run_time=0.35)

        # Beat 4: 2 * 2 = 4
        xs4 = [-4.2, -1.4, 1.4, 4.2]
        r4 = [make_receptor(x, mem_y, color=C_EGF, pocket="wedge", scale=0.90) for x in xs4]
        g4 = [RoundedRectangle(corner_radius=0.08, width=0.95, height=0.40, stroke_color=C_EGF, stroke_width=2.8, fill_color=C_EGF, fill_opacity=0.45).move_to([x, dna_y, 0]) for x in xs4]
        g4_lbl = [M("EGF-R", size=22, color=TEXT).next_to(g, DOWN, buff=0.14) for g in g4]
        step2_eq = M("2 × 2 = 4", size=30, color=C_EGF).move_to([0, 0.0, 0])

        self.at("and two times two")
        self.play(FadeOut(g2a_lbl), FadeOut(g2b_lbl), FadeOut(dna_lbl), run_time=0.25)
        self.play(
            ReplacementTransform(r2a, r4[0]), TransformFromCopy(r2a, r4[1]),
            ReplacementTransform(r2b, r4[2]), TransformFromCopy(r2b, r4[3]),
            ReplacementTransform(g2a, g4[0]), TransformFromCopy(g2a, g4[1]),
            ReplacementTransform(g2b, g4[2]), TransformFromCopy(g2b, g4[3]),
            count_tr.animate.set_value(4),
            swap(step1_eq, step2_eq, run_time=0.65),
            run_time=2.0,
        )
        self.play(*[FadeIn(lb) for lb in g4_lbl], run_time=0.35)

        # Beat 5: Fly: 1 -> Human: 4 (likely route)
        fly_box = boxed_label("Fly: 1 EGF receptor", color=C_KINOME, size=28).move_to([-3.3, -2.65, 0])
        hum_box = boxed_label("Human: 4 EGF receptors", color=C_EGF, size=28).move_to([3.0, -2.65, 0])
        route_arr = Arrow(fly_box.get_right() + RIGHT * 0.12, hum_box.get_left() + LEFT * 0.12, color=TEXT, stroke_width=3, buff=0.05)
        hedge = T("likely route", size=24, color=TEXT).next_to(route_arr, UP, buff=0.10)

        self.at("likely route")
        self.play(FadeIn(fly_box), FadeIn(hum_box), FadeIn(hedge), run_time=0.45)
        self.play(GrowArrow(route_arr), run_time=1.4)
        self.finish()


class S05FatesLossSplit(SpokenScene):
    def construct(self):
        # Start centered with Original + Spare on membrane (width 5.0 so it fits inside Left panel later)
        mem_y = 0.95
        c_cyto = make_cytoplasm(-2.55, 2.55, -1.45, mem_y, color=C_RTK, fill_opacity=0.15)
        mem_c = make_membrane(-2.55, 2.55, mem_y, stroke=3.0)
        orig = make_receptor(-1.15, mem_y, color=C_RTK, pocket="round", scale=0.9)
        spare = make_receptor(1.15, mem_y, color=C_RTK, pocket="round", scale=0.9)
        orig_lbl = T("Original", size=26, color=C_RTK).move_to([-1.15, 2.15, 0])
        spare_lbl = T("Spare", size=26, color=C_RTK).move_to([1.15, 2.15, 0])

        self.play(FadeIn(c_cyto), FadeIn(mem_c), FadeIn(orig), FadeIn(spare), FadeIn(orig_lbl), FadeIn(spare_lbl), run_time=0.7)

        # Original keeps working (active bar + signal flow) while Spare is free to change
        sig_dot = make_ligand(C_RTK, "round", scale=0.9).move_to([-1.15, 1.68, 0])
        work_arr = Arrow([-1.15, mem_y - 0.50, 0], [-1.15, -0.45, 0], color=C_KEEP, stroke_width=5.0, buff=0)
        work_bar = Rectangle(width=1.7, height=0.28, stroke_color=C_KEEP, stroke_width=2, fill_color=C_KEEP, fill_opacity=0.78).move_to([-1.15, -1.22, 0])
        work_tag = T("keeps working", size=24, color=C_KEEP).move_to([-1.35, -0.78, 0])
        free_tag = T("free to change", size=24, color=C_EGF).move_to([1.35, -0.78, 0])

        self.at("the original keeps working")
        self.play(FadeIn(work_tag), FadeIn(free_tag), run_time=0.45)
        self.play(
            sig_dot.animate.move_to([-1.15, mem_y + 0.34, 0]),
            GrowArrow(work_arr),
            GrowFromEdge(work_bar, LEFT),
            run_time=2.5,
        )

        # Beat 2: Left panel "1. Loss (most spares)" -> Spare cracks into grey Pseudogene & output drops
        tp = TwoPanel("1. Loss (most spares)", "2. Job split", colors=(C_STRUCT, C_KEEP), top=3.05, bottom=-2.50, gap=0.45, width=12.6, size=30)
        left_target_grp = VGroup(c_cyto, mem_c, orig, spare, orig_lbl, spare_lbl, sig_dot, work_arr, work_bar, work_tag)

        self.at("Most spares decay")
        self.play(FadeOut(free_tag), run_time=0.35)
        self.play(left_target_grp.animate.shift(LEFT * 3.15), run_time=0.7)
        self.play(FadeIn(tp.left_frame), FadeIn(tp.left_head), run_time=0.4)

        sx = 1.15 - 3.15
        crack = VMobject(stroke_color=C_STRUCT, stroke_width=5.5).set_z_index(2)
        crack.set_points_as_corners([
            [sx - 0.16, mem_y + 0.30, 0],
            [sx + 0.12, mem_y + 0.10, 0],
            [sx - 0.10, mem_y - 0.12, 0],
            [sx + 0.16, mem_y - 0.32, 0],
        ])
        pseudo_box = Rectangle(width=1.7, height=0.28, stroke_color=C_STRUCT, stroke_width=2, fill_color=C_STRUCT, fill_opacity=0.25).move_to([sx, -1.28, 0])
        pseudo_lbl = T("Pseudogene\n(no protein)", size=24, color=C_STRUCT).move_to([sx, -0.72, 0])

        self.play(FadeIn(pseudo_lbl), FadeIn(pseudo_box), run_time=0.45)
        self.play(
            Create(crack),
            spare.animate.set_color(C_STRUCT).set_opacity(0.45),
            spare_lbl.animate.set_color(C_STRUCT),
            pseudo_box.animate.stretch(0.05, 0).set_opacity(0.1),
            run_time=2.8,
        )

        # Beat 3: Right panel "2. Job split"
        r_cx = 3.15
        r_cyto = make_cytoplasm(0.60, 5.70, -1.90, mem_y, color=C_KEEP, fill_opacity=0.13)
        r_mem = make_membrane(0.60, 5.70, mem_y, stroke=3.0)
        anc_rec = make_receptor(r_cx, mem_y, color=C_RTK, pocket="round", scale=0.88)
        anc_gut = boxed_label("Gut DNA", color=C_KEEP, size=24).move_to([r_cx - 1.10, -0.25, 0])
        anc_nerve = boxed_label("Nerve DNA", color=C_KEEP, size=24).move_to([r_cx + 1.10, -0.25, 0])

        self.at("divide the old job")
        self.play(FadeIn(tp.right_frame), FadeIn(tp.right_head), FadeIn(r_cyto), FadeIn(r_mem), run_time=0.5)
        self.play(FadeIn(anc_rec), FadeIn(anc_gut), FadeIn(anc_nerve), run_time=1.3)

        # Beat 4: Duplicate into Copy A & Copy B each with Gut + Nerve DNA + large tissue bars
        ax, bx = 1.85, 4.45
        copy_a = make_receptor(ax, mem_y, color=C_RTK, pocket="round", scale=0.82)
        copy_b = make_receptor(bx, mem_y, color=C_RTK, pocket="round", scale=0.82)
        lbl_a = T("Copy A", size=24, color=C_RTK).move_to([ax, 1.82, 0])
        lbl_b = T("Copy B", size=24, color=C_RTK).move_to([bx, 1.82, 0])

        a_gut = boxed_label("Gut", color=C_KEEP, size=24, box=(1.25, 0.44)).move_to([ax, -0.05, 0])
        a_nerve = boxed_label("Nerve", color=C_KEEP, size=24, box=(1.25, 0.44)).move_to([ax, -0.70, 0])
        b_gut = boxed_label("Gut", color=C_KEEP, size=24, box=(1.25, 0.44)).move_to([bx, -0.05, 0])
        b_nerve = boxed_label("Nerve", color=C_KEEP, size=24, box=(1.25, 0.44)).move_to([bx, -0.70, 0])

        a_bar = Rectangle(width=1.70, height=0.32, stroke_color=C_KEEP, stroke_width=2, fill_color=C_KEEP, fill_opacity=0.82).move_to([ax, -1.24, 0])
        b_bar = Rectangle(width=1.70, height=0.32, stroke_color=C_KEEP, stroke_width=2, fill_color=C_KEEP, fill_opacity=0.82).move_to([bx, -1.24, 0])

        self.at("worked in gut and nerve")
        self.play(FadeOut(anc_gut), FadeOut(anc_nerve), run_time=0.35)
        self.play(
            ReplacementTransform(anc_rec, copy_a),
            TransformFromCopy(anc_rec, copy_b),
            FadeIn(lbl_a), FadeIn(lbl_b),
            FadeIn(a_gut), FadeIn(a_nerve),
            FadeIn(b_gut), FadeIn(b_nerve),
            GrowFromEdge(a_bar, LEFT), GrowFromEdge(b_bar, LEFT),
            run_time=2.2,
        )

        # Beat 5: Copy A loses Gut DNA (turns grey, shrinks away, bar drops to Nerve only)
        self.at("loses the DNA")
        lost_a = T("lost", size=22, color=C_STRUCT).next_to(a_gut, RIGHT, buff=0.10)
        self.play(a_gut.box.animate.set_stroke(C_STRUCT, width=3.5), FadeIn(lost_a), run_time=0.45)
        self.play(
            FadeOut(a_gut, scale=0.4), FadeOut(lost_a),
            a_bar.animate.stretch_to_fit_width(0.85),
            a_nerve.box.animate.set_fill(C_KEEP, opacity=0.38),
            run_time=1.8,
        )

        # Beat 6: Copy B loses Nerve DNA (turns grey, shrinks away, bar drops to Gut only)
        self.at("the other the nerve")
        lost_b = T("lost", size=22, color=C_STRUCT).next_to(b_nerve, LEFT, buff=0.10)
        self.play(b_nerve.box.animate.set_stroke(C_STRUCT, width=3.5), FadeIn(lost_b), run_time=0.45)
        self.play(
            FadeOut(b_nerve, scale=0.4), FadeOut(lost_b),
            b_bar.animate.stretch_to_fit_width(0.85),
            b_gut.box.animate.set_fill(C_KEEP, opacity=0.38),
            run_time=1.8,
        )

        # Beat 7: Bracket locks both copies in place
        self.at("Now both must stay")
        lock_line = VMobject(stroke_color=C_KEEP, stroke_width=4.0)
        lock_line.set_points_as_corners([
            [ax, -1.48, 0], [ax, -1.75, 0], [bx, -1.75, 0], [bx, -1.48, 0],
        ])
        lock_lbl = T("Job split — both stay", size=26, color=C_KEEP).move_to([r_cx, -2.14, 0])
        self.play(FadeIn(lock_lbl), Create(lock_line), a_bar.animate.set_fill(C_KEEP, opacity=0.95), b_bar.animate.set_fill(C_KEEP, opacity=0.95), run_time=0.7)
        self.finish()


class S06FatesNew(SpokenScene):
    def construct(self):
        head = T("3. New job (rarer)", size=34, color=C_EGF).move_to([0, 3.15, 0])
        mem_y = 0.25
        cyto = make_cytoplasm(-5.5, 5.5, -2.25, mem_y, color=C_KINOME, fill_opacity=0.14)
        mem = make_membrane(-5.5, 5.5, mem_y, stroke=3.5)

        rec_orig = make_receptor(-2.2, mem_y, color=C_RTK, pocket="round", scale=1.05)
        rec_spare = make_receptor(2.2, mem_y, color=C_RTK, pocket="round", scale=1.05)
        lig_orig = make_ligand(C_RTK, "round", scale=1.05).move_to([-2.2, 2.00, 0])

        self.play(FadeIn(head), FadeIn(cyto), FadeIn(mem), FadeIn(rec_orig), FadeIn(rec_spare), FadeIn(lig_orig), run_time=0.8)

        # Beat 1: Spare receptor reshapes its outer pocket and shifts to YELLOW
        rec_new = make_receptor(2.2, mem_y, color=C_EGF, pocket="wedge", scale=1.05)
        new_lbl = T("new receptor", size=26, color=C_EGF).move_to([2.2, 1.35, 0])
        orig_lbl = T("original", size=26, color=C_RTK).move_to([-2.2, 1.35, 0])

        self.at("evolves a new job")
        self.play(FadeIn(orig_lbl), FadeIn(new_lbl), run_time=0.4)
        self.play(ReplacementTransform(rec_spare, rec_new), run_time=1.6)

        # Beat 2: New triangular ligand docks + signal bars grow downward into cytoplasm
        lig_new = make_ligand(C_EGF, "wedge", scale=1.05).move_to([2.2, 2.00, 0])
        self.at("binding a different signal")
        self.play(FadeOut(orig_lbl), FadeOut(new_lbl), FadeIn(lig_new), run_time=0.4)
        self.play(
            lig_orig.animate.move_to([-2.2, mem_y + 0.38, 0]),
            lig_new.animate.move_to([2.2, mem_y + 0.42, 0]),
            run_time=1.3,
        )
        sig_a = Rectangle(width=0.22, height=1.55, stroke_color=C_RTK, stroke_width=2, fill_color=C_RTK, fill_opacity=0.65).move_to([-2.2, -1.05, 0])
        sig_b = Rectangle(width=0.22, height=1.55, stroke_color=C_EGF, stroke_width=2, fill_color=C_EGF, fill_opacity=0.65).move_to([2.2, -1.05, 0])
        self.play(GrowFromEdge(sig_a, UP), GrowFromEdge(sig_b, UP), run_time=1.8)

        # Beat 3: Expands into a family of 4 distinct relatives across the membrane
        xs4 = [-4.2, -1.4, 1.4, 4.2]
        shapes = ["round", "square", "wedge", "diamond"]
        colors = [C_RTK, C_RTK, C_EGF, C_EGF]
        fam_recs = VGroup(*[
            make_receptor(x, mem_y, color=col, pocket=sh, scale=0.95)
            for x, col, sh in zip(xs4, colors, shapes)
        ])
        fam_lbl = T("family of receptors", size=28, color=TEXT).move_to([0, 2.35, 0])

        self.at("family of relatives")
        self.play(FadeOut(lig_orig), FadeOut(lig_new), FadeOut(sig_a), FadeOut(sig_b), FadeIn(fam_lbl), run_time=0.45)
        self.play(
            ReplacementTransform(rec_orig, fam_recs[0]),
            TransformFromCopy(rec_orig, fam_recs[1]),
            ReplacementTransform(rec_new, fam_recs[2]),
            TransformFromCopy(rec_new, fam_recs[3]),
            run_time=1.8,
        )

        # Beat 4: 4 distinct outside ligands descend into the 4 pockets
        fam_ligs = VGroup(*[
            make_ligand(col, sh, scale=0.95).move_to([x, 1.65, 0])
            for x, col, sh in zip(xs4, colors, shapes)
        ])
        self.at("different outside messages")
        self.play(FadeIn(fam_ligs), run_time=0.4)
        self.play(
            *[fam_ligs[i].animate.move_to([xs4[i], mem_y + 0.36, 0]) for i in range(4)],
            run_time=1.8,
        )

        # Beat 5: Empty cytoplasm below raises a wiring puzzle
        q_wires = VGroup(*[
            DashedLine([x, mem_y - 0.48, 0], [x, -1.45, 0], color=TEXT, stroke_width=3.5, dash_length=0.14)
            for x in xs4
        ])
        q_marks = VGroup(*[M("?", size=36, color=GOLD).move_to([x, -1.85, 0]) for x in xs4])
        puzzle_lbl = T("How do 4 receptors wire below?", size=30, color=GOLD).move_to([0, -2.75, 0])

        self.at("raise a wiring puzzle")
        self.play(FadeIn(puzzle_lbl), FadeIn(q_marks), run_time=0.45)
        self.play(*[Create(w) for w in q_wires], run_time=1.3)
        self.finish()


class S07PredictSetup(SpokenScene):
    def construct(self):
        reminder, tp, left_world, right_world = build_s07_s08_panels(show_panels=False)
        self.play(FadeIn(reminder), run_time=0.55)

        # Beat 1: One single pathway (1 receptor over 3-kinase core = 4 genes) at center
        c_cyto = make_cytoplasm(-1.6, 1.6, -1.35, 1.05, color=C_RTK, fill_opacity=0.15)
        c_mem = make_membrane(-1.6, 1.6, 1.05, stroke=3.0)
        c_rec = make_receptor(0.0, 1.05, color=C_RTK, pocket="round", scale=0.85)
        c_wire = Line([0, 0.65, 0], [0, 0.33, 0], color=C_RTK, stroke_width=3.0)
        c_stack = make_kinase_stack(0.0, y_top=0.15, step=0.48, radius=0.19, color=C_CORE)
        c_lbl = M("1 + 3 = 4 genes", size=30, color=TEXT).move_to([0, -1.78, 0])

        self.at("one receptor over")
        self.play(FadeIn(c_cyto), FadeIn(c_mem), FadeIn(c_rec), Create(c_wire), Create(c_stack), run_time=1.8)

        # Phosphate/signal dot passes down the 3-kinase cascade
        p_dot = Dot(radius=0.15, color=C_RTK).move_to([0, 0.65, 0])
        self.at("four genes in all")
        self.play(FadeIn(c_lbl), run_time=0.4)
        self.add(p_dot)
        self.play(p_dot.animate.move_to([0, -0.81, 0]), run_time=1.1)
        self.play(FadeOut(p_dot), run_time=0.25)

        # Beat 2: Left panel — 4 separate pathways = 16 genes with live counter
        l_cyto, l_mem, l_recs, l_wires, l_stacks, l_tally = left_world
        cnt16 = ValueTracker(4)
        live16 = always_redraw(lambda: M(
            f"genes: {int(round(cnt16.get_value()))}", size=28, color=C_KINOME,
        ).move_to([-3.15, -1.78, 0]))

        self.at("Four separate pathways")
        self.play(FadeOut(c_cyto), FadeOut(c_mem), FadeOut(c_rec), FadeOut(c_wire), FadeOut(c_stack), FadeOut(c_lbl), run_time=0.4)
        self.play(FadeIn(tp.left_frame), FadeIn(tp.left_head), FadeIn(l_cyto), FadeIn(l_mem), run_time=0.45)
        self.add(live16)
        self.play(
            LaggedStart(*[FadeIn(l_recs[i]) for i in range(4)], lag_ratio=0.14),
            LaggedStart(*[Create(l_wires[i]) for i in range(4)], lag_ratio=0.14),
            LaggedStart(*[Create(l_stacks[i]) for i in range(4)], lag_ratio=0.14),
            cnt16.animate.set_value(16),
            run_time=2.0,
        )
        self.at("sixteen genes")
        self.play(FadeOut(live16), run_time=0.2)
        self.play(FadeIn(l_tally), run_time=0.25)

        # Beat 3: Right panel — 4 receptors sharing 1 core = 7 genes with live counter
        r_cyto, r_mem, r_recs, r_wires, r_stack, r_tally = right_world
        cnt7 = ValueTracker(4)
        live7 = always_redraw(lambda: M(
            f"genes: {int(round(cnt7.get_value()))}", size=28, color=C_RTK,
        ).move_to([3.15, -1.78, 0]))

        self.at("Four receptors sharing")
        self.play(FadeIn(tp.right_frame), FadeIn(tp.right_head), FadeIn(r_cyto), FadeIn(r_mem), run_time=0.45)
        self.add(live7)
        self.play(
            LaggedStart(*[FadeIn(r_recs[i]) for i in range(4)], lag_ratio=0.14),
            LaggedStart(*[Create(r_wires[i]) for i in range(4)], lag_ratio=0.14),
            Create(r_stack),
            cnt7.animate.set_value(7),
            run_time=2.4,
        )
        self.at("seven genes")
        self.play(FadeOut(live7), run_time=0.2)
        self.play(FadeIn(r_tally), run_time=0.25)

        # Highlight top genome bar reminder before asking the question
        hl_box = SurroundingRectangle(reminder, color=GOLD, buff=0.06, stroke_width=2.5)
        self.at("Looking at our genome")
        self.play(Create(hl_box), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(hl_box), run_time=0.5)

        # Beat 4: Question card matches S08Pause pixel-for-pixel
        q = question_card("Which layout fits the genome bars better?", y=-2.95, max_w=10.2)
        self.at("which layout fits better")
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Which layout fits the genome bars better?"
    OPTIONS = ()
    CARD = {"y": -2.95, "max_w": 10.2}
    SECONDS = 4.5

    def backdrop(self):
        return build_s07_s08_panels(show_panels=True)


class S09RevealAndRule(SpokenScene):
    def construct(self):
        reminder, tp, left_world, right_world = build_s07_s08_panels(show_panels=False)
        self.add(reminder, tp, left_world, right_world)

        l_cyto, l_mem, l_recs, l_wires, l_stacks, l_tally = left_world
        r_cyto, r_mem, r_recs, r_wires, r_stack, r_tally = right_world

        # Beat 1: Shared core fits better — highlight right panel, dim left panel stroke/items cleanly
        self.at("shared core fits better")
        self.play(
            tp.right_frame.animate.set_stroke(C_RTK, width=4.5),
            tp.left_frame.animate.set_stroke(opacity=0.25),
            tp.left_head.animate.set_opacity(0.35),
            l_cyto.animate.set_fill(opacity=0.04),
            l_mem.animate.set_stroke(opacity=0.30),
            *[r[0].animate.set_stroke(opacity=0.30) for r in l_recs],
            *[r[1].animate.set_opacity(0.20) for r in l_recs],
            *[r[2].animate.set_stroke(opacity=0.30) for r in l_recs],
            l_wires.animate.set_stroke(opacity=0.30),
            l_stacks.animate.set_opacity(0.30),
            l_tally.animate.set_opacity(0.35),
            run_time=1.3,
        )

        # Beat 2: Receptors multiplied faster — highlight RTKs 2.9x + receptor layer + glowing wire flashes
        rtk_hl = SurroundingRectangle(reminder[2], color=C_RTK, buff=0.06, stroke_width=2.5)
        rec_hl = SurroundingRectangle(r_recs, color=C_RTK, buff=0.10, stroke_width=2.5)
        self.at("receptors multiplied faster")
        self.play(Create(rtk_hl), Create(rec_hl), run_time=1.0)
        flash_wires = r_wires.copy().set_stroke(C_EGF, width=7)
        self.play(ShowPassingFlash(flash_wires, time_width=0.6), run_time=1.8)
        self.play(FadeOut(rec_hl), run_time=0.4)

        # Beat 3: Separate tracks would grow both layers equally, then remove left panel and center shared core
        eq_note = T("both layers 4×", size=24, color=C_KINOME).move_to([-3.15, -2.55, 0])
        self.at("Separate")
        self.play(FadeIn(eq_note), run_time=0.45)
        self.wait(1.6)

        self.play(FadeOut(tp), FadeOut(left_world), FadeOut(eq_note), FadeOut(r_tally), FadeOut(rtk_hl), run_time=0.55)

        c_xs = [-3.6, -1.2, 1.2, 3.6]
        c_mem_y = 1.20
        c_cyto = make_cytoplasm(-5.2, 5.2, -2.10, c_mem_y, color=C_RTK, fill_opacity=0.15)
        c_mem = make_membrane(-5.2, 5.2, c_mem_y, stroke=3.5)
        c_recs = VGroup(*[
            make_receptor(x, c_mem_y, color=(C_RTK if i % 2 == 0 else C_EGF),
                          pocket=("round" if i % 2 == 0 else "wedge"), scale=0.95)
            for i, x in enumerate(c_xs)
        ])
        hub_pos = np.array([0.0, -0.35, 0.0])
        hub_circle = Circle(radius=0.48, color=C_CORE, stroke_width=3.5, fill_color=C_CORE, fill_opacity=0.38).move_to(hub_pos)
        c_wires = VGroup(*[
            Line([x, c_mem_y - 0.48, 0], hub_pos + UP * 0.48, color=(C_RTK if i % 2 == 0 else C_EGF), stroke_width=3.5)
            for i, x in enumerate(c_xs)
        ])
        down_arrow = Arrow(hub_pos + DOWN * 0.48, [0, -1.95, 0], color=C_CORE, stroke_width=4.5, buff=0.05)
        down_lbl = T("shared core", size=26, color=C_CORE).next_to(down_arrow, RIGHT, buff=0.20)

        self.play(
            ReplacementTransform(r_cyto, c_cyto),
            ReplacementTransform(r_mem, c_mem),
            *[ReplacementTransform(r_recs[i], c_recs[i]) for i in range(4)],
            *[ReplacementTransform(r_wires[i], c_wires[i]) for i in range(4)],
            ReplacementTransform(r_stack, hub_circle),
            run_time=1.3,
        )
        self.play(GrowArrow(down_arrow), FadeIn(down_lbl), run_time=0.5)

        # Beat 4: Signal waves funnel from all 4 receptors into Ras hub (never late!)
        self.at("heavily connected proteins")
        pulses = VGroup(*[
            Dot(radius=0.16, color=(C_RTK if i % 2 == 0 else C_EGF)).move_to([c_xs[i], c_mem_y - 0.48, 0])
            for i in range(4)
        ])
        self.add(pulses)
        self.play(
            *[pulses[i].animate.move_to(hub_pos + UP * 0.48) for i in range(4)],
            ShowPassingFlash(c_wires.copy().set_stroke(width=8), time_width=0.6),
            run_time=1.2,
        )
        self.play(FadeOut(pulses), hub_circle.animate.set_fill(C_CORE, opacity=0.72), run_time=0.35)

        hub_lbl = T("Ras hub", size=28, color=TEXT).move_to([1.35, -0.35, 0])
        self.at("called hubs")
        self.play(FadeIn(hub_lbl, shift=RIGHT * 0.1), hub_circle.animate.set_fill(C_CORE, opacity=0.38), run_time=0.8)

        # Beat 5: Core grew modestly too (1 node -> 3 smaller linked RED circles)
        core_3 = VGroup(
            Circle(radius=0.28, color=C_CORE, stroke_width=3, fill_color=C_CORE, fill_opacity=0.38).move_to([-0.75, -0.35, 0]),
            Circle(radius=0.28, color=C_CORE, stroke_width=3, fill_color=C_CORE, fill_opacity=0.38).move_to([0.0, -0.35, 0]),
            Circle(radius=0.28, color=C_CORE, stroke_width=3, fill_color=C_CORE, fill_opacity=0.38).move_to([0.75, -0.35, 0]),
        )
        core_links = VGroup(
            Line([-0.47, -0.35, 0], [-0.28, -0.35, 0], color=C_CORE, stroke_width=3),
            Line([0.28, -0.35, 0], [0.47, -0.35, 0], color=C_CORE, stroke_width=3),
        )
        new_wires = VGroup(*[
            Line([x, c_mem_y - 0.48, 0], core_3[1 if i in (1, 2) else (0 if i == 0 else 2)].get_top(),
                 color=(C_RTK if i % 2 == 0 else C_EGF), stroke_width=3.5)
            for i, x in enumerate(c_xs)
        ])
        modest_lbl = T("core grew modestly (1.8×)", size=24, color=C_CORE).move_to([-2.45, -0.95, 0])

        self.at("grew modestly")
        self.play(FadeIn(modest_lbl), hub_lbl.animate.move_to([2.05, -0.35, 0]), run_time=0.4)
        self.play(
            ReplacementTransform(hub_circle, core_3[1]),
            FadeIn(core_3[0], scale=0.6), FadeIn(core_3[2], scale=0.6),
            Create(core_links),
            *[ReplacementTransform(c_wires[i], new_wires[i]) for i in range(4)],
            run_time=1.8,
        )

        # Beat 6: Caveat — Counts alone do not prove wiring + signal wave
        caveat = caption("Counts alone do not prove wiring.", size=28, color=TEXT, y=-2.95)
        self.at("cannot prove wiring")
        self.play(FadeIn(caveat, shift=UP * 0.1), run_time=0.5)
        self.play(ShowPassingFlash(new_wires.copy().set_stroke(width=8), time_width=0.6), run_time=1.6)

        # Beat 7: Final takeaway rule + receptor layer highlight + final pulse
        top_rule = T("Copied old pathways", size=30, color=TEXT)
        top_end = T("— mostly at the receptor end", size=30, color=C_RTK)
        top_grp = VGroup(top_rule, top_end).arrange(RIGHT, buff=0.14).move_to([0, 2.35, 0])

        self.at("copying old pathways")
        self.play(FadeIn(top_grp[0], shift=DOWN * 0.1), run_time=0.5)
        self.play(ShowPassingFlash(new_wires.copy().set_stroke(width=8), time_width=0.6), run_time=1.4)

        final_pulses = VGroup(*[
            Dot(radius=0.15, color=(C_RTK if i % 2 == 0 else C_EGF)).move_to([c_xs[i], c_mem_y - 0.48, 0])
            for i in range(4)
        ])
        rec_top_hl = SurroundingRectangle(c_recs, color=C_RTK, buff=0.12, stroke_width=2.5)
        self.at("mostly at the receptor end")
        self.play(FadeIn(top_grp[1], shift=RIGHT * 0.1), run_time=0.45)
        self.add(final_pulses)
        self.play(
            Create(rec_top_hl),
            *[final_pulses[i].animate.move_to(core_3[1 if i in (1, 2) else (0 if i == 0 else 2)].get_top()) for i in range(4)],
            run_time=1.5,
        )
        self.play(FadeOut(final_pulses), run_time=0.25)
        self.finish()


class S10End(EndCard):
    LINE = "Animal signaling expanded by copying old pathways, mostly at the receptor end."
