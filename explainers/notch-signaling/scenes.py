"""Notch: Signaling by Contact and by Cutting (12 scenes, ~197 s).

COLOUR MAP (one colour per concept across the whole film):
    SENDER_COL   = "#F59E0B"   # warm amber: sending cell, membrane-anchored ligand (Delta/Jagged)
    NOTCH_COL    = TEAL        # cool teal (#3FB8C0): receiving cell membrane & outer Notch receptor stalk
    NICD_COL     = BLUE        # cyan-teal (#58C4DD): Notch inner tail / freed NICD signal
    LOCK_COL     = YELLOW      # bright gold (#F5D547): compact extracellular lock (NRR) & predict highlight
    CUT_COL      = RED         # coral-red (#FC6255): exposed Cut 2 site, ADAM protease shears, ubiquitin tags
    GAMMA_COL    = "#A855F7"   # violet: gamma-secretase complex & presenilin core
    WATER_COL    = "#38BDF8"   # sky blue: water pocket inside presenilin
    NUCLEUS_COL  = "#4F46E5"   # deep indigo: receiving cell nucleus & nuclear envelope
    GENE_ON_COL  = GREEN       # emerald (#83C167): Mastermind co-activator, active target gene, Hes repressors
    CSL_COL      = "#94A3B8"   # slate: CSL DNA-binding block, co-repressors, inactive gene
    KINASE_COL   = "#60A5FA"   # steel-blue: kinase cascade comparison panel & products

CARRIED WORLD:
    A two-cell cross-section: warm amber Sending cell above, cool teal Receiving cell below with a
    deep indigo Nucleus at its base. Depending on the scene's focus, we view the full two-cell
    junction (s01-s02), zoom onto the receiving membrane & cleft (s03-s06), zoom into the lipid
    bilayer (s07), follow NICD into the nucleus (s08, s10), or compare 10 receptors side-by-side
    in a two-panel schematic (s09).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s01_hook    : A 20-cell sheet computed with rng(7) switches skin fates to all-nerve ("no Notch");
                  two touching cells expand and anchored ligand touches Notch ("not you").
    s02_contact : 5 soluble signal trajectories (Brownian + drift, rng(12)) stream out of the upper
                  cell, then anchored Ligand and Notch bolt into opposing membranes and slide to latch.
    s03_predict : Gold lock modules fold shut over the red cut site; a loose ligand fragment follows a
                  computed solution drift (rng(3)) to dock on Notch and bobs with zero upward pull.
    s05_pull    : Loose ligand drifts off; sending cell returns and a Gaussian endocytic pit
                  y(x) = y0 + d*pull*exp(-(x/w)^2) (pull 0->1) tugs Notch upward, peeling the lock open.
    s06_adam    : Prep-cut seam highlights ("halves stay joined") then clears; coral-red ADAM shears
                  glide in and snip the exposed site; outer Notch + ligand rise, leaving a stub.
    s07_gamma   : Violet gamma-secretase slides through the bilayer to fit the trimmed stub;
                  "Cut = hydrolysis (needs H2O)" and dry interior show why presenilin needs a
                  water pocket; intramembrane cut frees NICD to glide toward the nucleus.
    s08_nucleus : NICD enters the nucleus, docks onto CSL on DNA, displaces co-repressors, recruits
                  Mastermind, switches the target gene emerald, and emits rising Hes repressors.
    s09_count   : Two ValueTrackers (0..10) drive 10 Notch cuts (intact 10->0, NICD 0->10) alongside
                  10 active kinases multiplying a computed 10x20 grid of 200 products (intact stays 10).
    s10_brief   : Local count (3 pulled -> 3 NICD) settles; nuclear kinase adds P marks, ubiquitin beads
                  attach, proteasome barrel draws NICD in and dissolves it, and the gene dims to OFF.
"""

from bp_parts import *

# ------------------------------------------------------------------ Concept palette
SENDER_COL = "#F59E0B"
NOTCH_COL = TEAL
NICD_COL = BLUE
LOCK_COL = YELLOW
CUT_COL = RED
GAMMA_COL = "#A855F7"
WATER_COL = "#38BDF8"
NUCLEUS_COL = "#4F46E5"
GENE_ON_COL = GREEN
CSL_COL = "#94A3B8"
KINASE_COL = "#60A5FA"


# ------------------------------------------------------------------ Shared geometry builders
def bilayer_band(y_center, x_left=-6.6, x_right=6.6, thickness=0.38, color=NOTCH_COL,
                 fill_opacity=0.30, stroke_width=4.0):
    """A lipid bilayer strip: two parallel membrane boundaries with oily interior tint."""
    w = x_right - x_left
    cx = (x_left + x_right) / 2
    interior = Rectangle(width=w, height=thickness, stroke_width=0,
                         fill_color=color, fill_opacity=fill_opacity).move_to([cx, y_center, 0])
    top_line = Line([x_left, y_center + thickness / 2, 0], [x_right, y_center + thickness / 2, 0],
                    color=color, stroke_width=stroke_width)
    bot_line = Line([x_left, y_center - thickness / 2, 0], [x_right, y_center - thickness / 2, 0],
                    color=color, stroke_width=stroke_width)
    return VGroup(interior, top_line, bot_line)


def cell_chamber(y_edge, y_far, x_left=-6.5, x_right=6.5, color=SENDER_COL,
                 fill_opacity=0.17):
    """A cross-section of a cell body bounded by a double membrane at y_edge."""
    cx = (x_left + x_right) / 2
    w = x_right - x_left
    h = abs(y_far - y_edge)
    cy = (y_edge + y_far) / 2
    body = Rectangle(width=w, height=h, stroke_width=0,
                     fill_color=color, fill_opacity=fill_opacity).move_to([cx, cy, 0])
    mem = bilayer_band(y_edge, x_left, x_right, thickness=0.26, color=color, fill_opacity=0.34)
    side_l = Line([x_left, y_edge, 0], [x_left, y_far, 0], color=color, stroke_width=3).set_opacity(0.55)
    side_r = Line([x_right, y_edge, 0], [x_right, y_far, 0], color=color, stroke_width=3).set_opacity(0.55)
    return VGroup(body, side_l, side_r, mem)


def nucleus_dome(y_top=-1.8, y_bot=-3.45, x_left=-5.2, x_right=5.2):
    """Deep indigo nucleus dome at the bottom of the receiving cell."""
    w = x_right - x_left
    h = y_top - y_bot
    cx = (x_left + x_right) / 2
    cy = (y_top + y_bot) / 2
    return RoundedRectangle(corner_radius=0.55, width=w, height=h,
                            stroke_color=NUCLEUS_COL, stroke_width=4,
                            fill_color=NUCLEUS_COL, fill_opacity=0.26).move_to([cx, cy, 0])


def build_ligand(x=0.0, y_mem=1.25, stalk_len=1.05, anchored=True):
    """Warm amber Notch ligand: membrane-spanning anchor + extracellular stalk + binding tip."""
    g = VGroup()
    if anchored:
        anchor = RoundedRectangle(corner_radius=0.07, width=0.26, height=0.46,
                                  stroke_color=SENDER_COL, stroke_width=3,
                                  fill_color=SENDER_COL, fill_opacity=0.60).move_to([x, y_mem, 0])
        cyto = Line([x, y_mem + 0.22, 0], [x, y_mem + 0.60, 0], color=SENDER_COL, stroke_width=7)
        g.add(cyto, anchor)
    stalk = Line([x, y_mem - (0.20 if anchored else 0.0), 0], [x, y_mem - stalk_len, 0],
                 color=SENDER_COL, stroke_width=9)
    tip = ArcBetweenPoints([x - 0.18, y_mem - stalk_len, 0], [x + 0.18, y_mem - stalk_len, 0],
                           angle=PI * 0.85, color=SENDER_COL, stroke_width=8)
    g.add(stalk, tip)
    g.tip_pt = np.array([x, y_mem - stalk_len, 0.0])
    return g


def build_notch_receptor(x=0.0, y_mem=-1.25, outer_len=1.15, inner_len=0.85, cut_y_rel=0.35):
    """Teal Notch outer stalk + red cut mark + cyan-teal inner tail (NICD)."""
    outer = Line([x, y_mem, 0], [x, y_mem + outer_len, 0], color=NOTCH_COL, stroke_width=9)
    tip = RoundedRectangle(corner_radius=0.08, width=0.32, height=0.22,
                           stroke_color=NOTCH_COL, stroke_width=3,
                           fill_color=NOTCH_COL, fill_opacity=0.50).move_to([x, y_mem + outer_len, 0])
    tm = RoundedRectangle(corner_radius=0.07, width=0.26, height=0.42,
                          stroke_color=NOTCH_COL, stroke_width=3,
                          fill_color=NICD_COL, fill_opacity=0.50).move_to([x, y_mem, 0])
    inner = Line([x, y_mem - 0.18, 0], [x, y_mem - 0.18 - inner_len, 0],
                 color=NICD_COL, stroke_width=9)
    tail_end = Dot([x, y_mem - 0.18 - inner_len, 0], radius=0.13, color=NICD_COL)
    cut_pt = np.array([x, y_mem + cut_y_rel, 0.0])
    cut_mark = VGroup(
        Line(cut_pt + LEFT * 0.22 + UP * 0.06, cut_pt + RIGHT * 0.22 - UP * 0.06,
             color=CUT_COL, stroke_width=6),
        Dot(cut_pt, radius=0.08, color=CUT_COL),
    )
    g = VGroup(outer, tip, tm, inner, tail_end, cut_mark)
    g.outer, g.tip, g.tm, g.inner, g.tail_end, g.cut_mark = outer, tip, tm, inner, tail_end, cut_mark
    g.tip_pt = np.array([x, y_mem + outer_len + 0.11, 0.0])
    g.cut_pt = cut_pt
    return g


def build_lock(center, open_frac=0.0, scale=1.0):
    """Three gold NRR lock modules that clasp shut around `center` (0) or peel open (1)."""
    c = np.array(center, dtype=float)
    left_arm = Arc(radius=0.30 * scale, start_angle=PI * 0.55, angle=PI * 0.9,
                   color=LOCK_COL, stroke_width=9)
    right_arm = Arc(radius=0.30 * scale, start_angle=-PI * 0.45, angle=PI * 0.9,
                    color=LOCK_COL, stroke_width=9)
    cap = Arc(radius=0.22 * scale, start_angle=0.15, angle=PI - 0.3,
              color=LOCK_COL, stroke_width=8)
    left_arm.move_to(c + LEFT * (0.11 + 0.36 * open_frac) * scale)
    right_arm.move_to(c + RIGHT * (0.11 + 0.36 * open_frac) * scale)
    cap.move_to(c + UP * (0.16 + 0.24 * open_frac) * scale)
    if open_frac > 0:
        left_arm.rotate(0.55 * open_frac)
        right_arm.rotate(-0.55 * open_frac)
    return VGroup(left_arm, right_arm, cap)


def build_receiving_zoom_stage(y_mem=-1.35, mem_thickness=0.42):
    """Zoomed receiving membrane in lower-mid frame + cytosolic fill below."""
    cyto = Rectangle(width=13.2, height=3.0, stroke_width=0,
                     fill_color=NOTCH_COL, fill_opacity=0.14).move_to([0, y_mem - 1.5, 0])
    mem = bilayer_band(y_mem, x_left=-6.6, x_right=6.6, thickness=mem_thickness,
                       color=NOTCH_COL, fill_opacity=0.32, stroke_width=4.5)
    return cyto, mem


def build_shears(pos, angle=0.0):
    """Coral-red ADAM protease shears."""
    b1 = Polygon([0, 0, 0], [-0.62, 0.18, 0], [-0.50, 0.32, 0],
                 color=CUT_COL, stroke_width=2, fill_color=CUT_COL, fill_opacity=0.88)
    b2 = Polygon([0, 0, 0], [-0.62, -0.18, 0], [-0.50, -0.32, 0],
                 color=CUT_COL, stroke_width=2, fill_color=CUT_COL, fill_opacity=0.88)
    h1 = Arc(radius=0.18, start_angle=0, angle=TAU, color=CUT_COL, stroke_width=5).move_to([0.38, 0.24, 0])
    h2 = Arc(radius=0.18, start_angle=0, angle=TAU, color=CUT_COL, stroke_width=5).move_to([0.38, -0.24, 0])
    s1 = Line([0, 0, 0], [0.24, 0.18, 0], color=CUT_COL, stroke_width=5)
    s2 = Line([0, 0, 0], [0.24, -0.18, 0], color=CUT_COL, stroke_width=5)
    pivot = Dot([0, 0, 0], radius=0.07, color=TEXT)
    g = VGroup(b1, b2, s1, s2, h1, h2, pivot).move_to(pos)
    if angle:
        g.rotate(angle)
    g.b1, g.b2 = b1, b2
    return g


def build_gamma_secretase(center):
    """Violet gamma-secretase ring (Ellipse to avoid panel-box check) + presenilin core."""
    c = np.array(center, dtype=float)
    outer_ring = Ellipse(width=3.4, height=2.5, stroke_color=GAMMA_COL, stroke_width=5,
                         fill_color=GAMMA_COL, fill_opacity=0.26).move_to(c)
    gate_l = Line(c + [-0.52, 1.18, 0], c + [-0.52, 1.48, 0], color=GAMMA_COL, stroke_width=6)
    gate_r = Line(c + [0.52, 1.18, 0], c + [0.52, 1.48, 0], color=GAMMA_COL, stroke_width=6)
    presenilin = Circle(radius=0.78, stroke_color=GAMMA_COL, stroke_width=4,
                        fill_color=GAMMA_COL, fill_opacity=0.40).move_to(c)
    g = VGroup(outer_ring, gate_l, gate_r, presenilin)
    g.outer_ring, g.presenilin = outer_ring, presenilin
    return g


def build_dna_stage(y_dna=-1.35):
    """DNA double strand across the nucleus with an off-state target gene bar on the right."""
    s1 = Line([-5.2, y_dna + 0.07, 0], [5.2, y_dna + 0.07, 0], color=CSL_COL, stroke_width=4.5)
    s2 = Line([-5.2, y_dna - 0.07, 0], [5.2, y_dna - 0.07, 0], color=CSL_COL, stroke_width=4.5)
    rungs = VGroup(*[
        Line([x, y_dna - 0.07, 0], [x, y_dna + 0.07, 0], color=CSL_COL, stroke_width=2.5)
        for x in np.linspace(-5.0, 5.0, 26)
    ])
    gene_bar = RoundedRectangle(corner_radius=0.10, width=3.3, height=0.50,
                                stroke_color=CSL_COL, stroke_width=3.5,
                                fill_color=CSL_COL, fill_opacity=0.25).move_to([2.6, y_dna, 0])
    dna = VGroup(s1, s2, rungs, gene_bar)
    dna.gene_bar = gene_bar
    return dna


def build_proteasome(center):
    """Barrel-shaped proteasome built of four stacked rings."""
    c = np.array(center, dtype=float)
    rings = VGroup()
    cols = [CSL_COL, "#64748B", "#64748B", CSL_COL]
    for i, col in enumerate(cols):
        y = c[1] + (1.5 - i) * 0.42
        r = RoundedRectangle(corner_radius=0.14, width=1.55, height=0.36,
                             stroke_color=col, stroke_width=3,
                             fill_color=col, fill_opacity=0.32).move_to([c[0], y, 0])
        rings.add(r)
    return rings


def _endocytic_membrane(y_base, pull_frac, x_left=-6.6, x_right=6.6, depth=0.90, width=1.20):
    """Computed Gaussian endocytic pocket in the sending membrane."""
    xs = np.linspace(x_left, x_right, 81)
    ys_bot = y_base + depth * pull_frac * np.exp(-(xs / width) ** 2)
    ys_top = ys_bot + 0.26
    bot_pts = [[x, y, 0] for x, y in zip(xs, ys_bot)]
    top_pts = [[x, y, 0] for x, y in zip(xs[::-1], ys_top[::-1])]
    poly = Polygon(*(bot_pts + top_pts), stroke_color=SENDER_COL, stroke_width=4,
                   fill_color=SENDER_COL, fill_opacity=0.34)
    fill_pts = bot_pts + [[x_right, 3.7, 0], [x_left, 3.7, 0]]
    cyto = Polygon(*fill_pts, stroke_width=0, fill_color=SENDER_COL, fill_opacity=0.15)
    return VGroup(cyto, poly)


def build_predict_backdrop():
    """Shared ending state of s03_predict and backdrop of s04_pause."""
    cyto, mem = build_receiving_zoom_stage(y_mem=-1.35, mem_thickness=0.42)
    notch = build_notch_receptor(x=0.0, y_mem=-1.35, outer_len=2.15, inner_len=1.25, cut_y_rel=0.68)
    notch.cut_mark.set_opacity(0.0)
    lock = build_lock(notch.cut_pt, open_frac=0.0, scale=1.45)
    loose_lig = build_ligand(x=0.0, y_mem=notch.tip_pt[1] + 1.15, stalk_len=1.05, anchored=False)

    mem_lbl = T("Receiving cell membrane", 26, NOTCH_COL).move_to([-3.9, -2.05, 0]).set_z_index(10)
    notch_lbl = T("Notch", 28, NOTCH_COL).move_to([1.15, 0.25, 0]).set_z_index(10)
    lock_lbl = T("Lock", 28, LOCK_COL).next_to(lock, LEFT, buff=0.38).set_z_index(10)
    lig_lbl = T("Loose ligand (no cell)", 28, SENDER_COL).next_to(loose_lig, LEFT, buff=0.35).set_z_index(10)
    tail_lbl = T("Inner tail", 26, NICD_COL).next_to(notch.inner, RIGHT, buff=0.32).set_z_index(10)

    # Bob both the loose ligand and Notch tip gently to show jiggling with zero upward pull
    bob(loose_lig, amp=0.10, speed=2.5, seed=1)
    return VGroup(cyto, mem, notch, lock, loose_lig, mem_lbl, notch_lbl, lock_lbl, lig_lbl, tail_lbl)


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Notch: Signaling by Contact and by Cutting"
    TITLE = "The Pull and the Cuts: One Receptor, One Message"


class S01Hook(SpokenScene):
    def construct(self):
        # Immediate non-black initial frame: carried two cells + computed 20-cell sheet
        sending = cell_chamber(0.45, 3.25, x_left=-1.2, x_right=6.1, color=SENDER_COL)
        receiving = cell_chamber(-0.15, -3.25, x_left=-1.2, x_right=6.1, color=NOTCH_COL)
        nuc = nucleus_dome(y_top=-1.85, y_bot=-3.10, x_left=-0.6, x_right=5.5)

        send_lbl = T("Sending cell", 28, SENDER_COL).move_to([2.45, 2.25, 0]).set_z_index(10)
        recv_lbl = T("Receiving cell", 28, NOTCH_COL).move_to([2.45, -1.15, 0]).set_z_index(10)
        nuc_lbl = T("Nucleus", 26, TEXT).move_to([2.45, -2.48, 0]).set_z_index(10)

        rng = np.random.default_rng(7)
        coords = [(c * 0.50, r * 0.48) for r in range(4) for c in range(5)]
        nerve_norm = {1, 8, 12, 19}
        norm_dots = VGroup(*[
            Circle(radius=0.18, color=SENDER_COL if i in nerve_norm else NOTCH_COL,
                   fill_opacity=0.88, stroke_width=2).move_to([-4.55 + dx, 1.35 + dy, 0])
            for i, (dx, dy) in enumerate(coords)
        ])
        norm_head = T("Normal: skin + nerve", 24, TEXT).next_to(norm_dots, UP, buff=0.20).set_z_index(10)

        nonotch_dots = VGroup(*[
            Circle(radius=0.18, color=SENDER_COL if i in nerve_norm else NOTCH_COL,
                   fill_opacity=0.88, stroke_width=2).move_to([-4.55 + dx, -1.65 + dy, 0])
            for i, (dx, dy) in enumerate(coords)
        ])
        nonotch_head = T("schematic: no Notch", 24, CUT_COL).next_to(nonotch_dots, UP, buff=0.20).set_z_index(10)
        callout = VGroup(norm_head, norm_dots, nonotch_head, nonotch_dots)

        self.add(sending, receiving, nuc, send_lbl, recv_lbl, nuc_lbl, callout)

        # Beat 1: Flip skin cells in "no Notch" grid to nerve cells using rng(7)
        self.at("too much nervous system")
        flip_order = [i for i in rng.permutation(20) if i not in nerve_norm]
        self.play(
            LaggedStart(*[
                nonotch_dots[i].animate.set_color(SENDER_COL).set_fill(SENDER_COL, opacity=0.92).scale(1.18)
                for i in flip_order
            ], lag_ratio=0.08),
            run_time=3.5,
        )

        # Beat 2: Dissolve callout, expand touching cells across full frame
        self.at("How does one cell")
        wide_send = cell_chamber(0.45, 3.25, x_left=-6.0, x_right=6.0, color=SENDER_COL)
        wide_recv = cell_chamber(-0.15, -3.25, x_left=-6.0, x_right=6.0, color=NOTCH_COL)
        wide_nuc = nucleus_dome(y_top=-1.85, y_bot=-3.10, x_left=-4.5, x_right=4.5)
        lig = build_ligand(x=0.0, y_mem=0.45, stalk_len=0.35, anchored=True)
        notch = build_notch_receptor(x=0.0, y_mem=-0.15, outer_len=0.25, inner_len=0.85, cut_y_rel=0.12)
        notch.cut_mark.set_opacity(0.0)

        self.play(
            FadeOut(callout),
            Transform(sending, wide_send),
            Transform(receiving, wide_recv),
            Transform(nuc, wide_nuc),
            send_lbl.animate.move_to([-3.6, 2.25, 0]),
            recv_lbl.animate.move_to([-3.6, -1.15, 0]),
            nuc_lbl.animate.move_to([0.0, -2.48, 0]),
            FadeIn(lig), FadeIn(notch),
            run_time=1.0,
        )

        self.at("not you")
        msg_chip = boxed_label("“not you”", color=LOCK_COL, size=28).move_to([2.8, -1.15, 0]).set_z_index(10)
        msg_arrow = Arrow([0.25, -0.15, 0], msg_chip.get_left() + LEFT * 0.14,
                          color=LOCK_COL, stroke_width=4, buff=0)
        self.play(FadeIn(msg_chip), GrowArrow(msg_arrow), run_time=0.8)

        self.at("never leaves")
        tether_lbl = T("Signal stays anchored", 28, SENDER_COL).move_to([3.3, 1.55, 0]).set_z_index(10)
        tether_arrow = Arrow([0.22, 0.55, 0], tether_lbl.get_left() + LEFT * 0.14,
                             color=SENDER_COL, stroke_width=4, buff=0)
        self.play(FadeIn(tether_lbl), GrowArrow(tether_arrow), run_time=0.6)
        for _ in range(3):
            self.play(lig.animate.shift(DOWN * 0.10), run_time=0.45, rate_func=there_and_back)
        self.finish()


class S02Contact(SpokenScene):
    def construct(self):
        sending = cell_chamber(1.55, 3.30, x_left=-6.1, x_right=6.1, color=SENDER_COL)
        receiving = cell_chamber(-1.35, -3.35, x_left=-6.1, x_right=6.1, color=NOTCH_COL)
        nuc = nucleus_dome(y_top=-2.20, y_bot=-3.25, x_left=-4.5, x_right=4.5)

        send_lbl = T("Sending cell", 28, SENDER_COL).move_to([-4.2, 2.45, 0]).set_z_index(10)
        recv_lbl = T("Receiving cell", 28, NOTCH_COL).move_to([-4.2, -1.80, 0]).set_z_index(10)
        nuc_lbl = T("Nucleus", 24, TEXT).move_to([0.0, -2.72, 0]).set_z_index(10)

        self.add(sending, receiving, nuc, send_lbl, recv_lbl, nuc_lbl)

        # Beat 1: soluble signals diffuse across the gap continuously up to 4.5s
        rng = np.random.default_rng(12)
        sol_dots = VGroup(*[
            Dot([-4.6 + 0.45 * i, 1.70, 0], radius=0.12, color=TEXT)
            for i in range(5)
        ])
        sol_lbl = T("Most signals leave the cell", 28, TEXT).move_to([3.2, 0.55, 0]).set_z_index(10)
        self.add(sol_dots, sol_lbl)

        steps = 12
        dt_step = 3.4 / steps
        vels = [np.array([rng.uniform(0.45, 0.85), rng.uniform(-0.85, -0.50), 0.0]) for _ in range(5)]
        for _ in range(steps):
            self.play(*[
                sol_dots[k].animate.shift((vels[k] + np.array([rng.normal(0, 0.14), rng.normal(0, 0.10), 0.0])) * dt_step)
                for k in range(5)
            ], run_time=dt_step, rate_func=linear)

        # Beat 2: Notch ligand stays bolted in sending cell's membrane, drifting laterally
        self.at("Notch ligands")
        lig = build_ligand(x=-2.5, y_mem=1.55, stalk_len=1.30, anchored=True)
        lig_lbl = T("Ligand", 28, SENDER_COL).next_to(lig, LEFT, buff=0.30).shift(DOWN * 0.2).set_z_index(10)
        self.play(FadeOut(sol_dots), FadeOut(sol_lbl), FadeIn(lig, shift=DOWN * 0.25), FadeIn(lig_lbl), run_time=0.6)
        self.play(lig.animate.shift(RIGHT * 0.85), lig_lbl.animate.shift(RIGHT * 0.85),
                  run_time=2.8, rate_func=linear)

        # Beat 3: Notch receptor stays bolted in receiving cell's membrane, drifting laterally
        self.at("The notch receptor")
        notch = build_notch_receptor(x=2.5, y_mem=-1.35, outer_len=1.35, inner_len=0.50, cut_y_rel=0.42)
        notch.cut_mark.set_opacity(0.0)
        lock = build_lock(notch.cut_pt, open_frac=0.0, scale=0.95)
        notch_lbl = T("Notch", 28, NOTCH_COL).next_to(notch.outer, RIGHT, buff=0.35).set_z_index(10)
        self.play(FadeIn(notch, shift=UP * 0.25), FadeIn(lock), FadeIn(notch_lbl), run_time=0.7)
        self.play(
            lig.animate.shift(RIGHT * 0.75), lig_lbl.animate.shift(RIGHT * 0.75),
            notch.animate.shift(LEFT * 1.15), lock.animate.shift(LEFT * 1.15),
            notch_lbl.animate.shift(LEFT * 1.15),
            run_time=4.4, rate_func=linear,
        )

        # Beat 4: Two cell surfaces draw together and Ligand + Notch latch cleanly
        self.at("Because both proteins")
        close_send = cell_chamber(1.05, 3.30, x_left=-6.1, x_right=6.1, color=SENDER_COL)
        close_recv = cell_chamber(-0.95, -3.35, x_left=-6.1, x_right=6.1, color=NOTCH_COL)
        lig_target = build_ligand(x=0.0, y_mem=1.05, stalk_len=0.95, anchored=True)
        notch_target = build_notch_receptor(x=0.0, y_mem=-0.95, outer_len=1.00, inner_len=0.80, cut_y_rel=0.34)
        notch_target.cut_mark.set_opacity(0.0)
        lock_target = build_lock(notch_target.cut_pt, open_frac=0.0, scale=0.95)

        self.play(
            Transform(sending, close_send),
            Transform(receiving, close_recv),
            Transform(lig, lig_target),
            Transform(notch, notch_target),
            Transform(lock, lock_target),
            lig_lbl.animate.move_to([-1.35, 0.45, 0]),
            notch_lbl.animate.move_to([1.35, -0.35, 0]),
            run_time=3.6,
        )

        self.at("two cell surfaces touch")
        contact_ring = Circle(radius=0.34, color=LOCK_COL, stroke_width=4.5).move_to([0.0, 0.08, 0])
        contact_lbl = T("Meet where surfaces touch", 28, LOCK_COL).move_to([3.4, 0.25, 0]).set_z_index(10)
        self.play(Create(contact_ring), FadeIn(contact_lbl), run_time=0.8)
        self.play(contact_ring.animate.scale(1.18).set_stroke(opacity=0.6), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        # Immediate non-black initial frame: zoomed receiving membrane + Notch with cut site exposed
        cyto, mem = build_receiving_zoom_stage(y_mem=-1.35, mem_thickness=0.42)
        notch = build_notch_receptor(x=0.0, y_mem=-1.35, outer_len=2.15, inner_len=1.25, cut_y_rel=0.68)
        mem_lbl = T("Receiving cell membrane", 26, NOTCH_COL).move_to([-3.9, -2.05, 0]).set_z_index(10)
        notch_lbl = T("Notch", 28, NOTCH_COL).move_to([1.15, 0.25, 0]).set_z_index(10)
        tail_lbl = T("Inner tail", 26, NICD_COL).next_to(notch.inner, RIGHT, buff=0.32).set_z_index(10)
        cut_lbl = T("Cut site", 26, CUT_COL).next_to(notch.cut_mark, LEFT, buff=0.65).set_z_index(10)

        self.add(cyto, mem, notch, mem_lbl, notch_lbl, tail_lbl, cut_lbl)
        self.play(notch.cut_mark.animate.scale(1.15), run_time=1.2, rate_func=there_and_back)

        # Beat 2: compact gold lock folds tightly around Notch, hiding its cutting spot
        self.at("notch folds")
        lock = build_lock(notch.cut_pt, open_frac=1.05, scale=1.45)
        closed_lock = build_lock(notch.cut_pt, open_frac=0.0, scale=1.45)
        lock_lbl = T("Lock", 28, LOCK_COL).next_to(closed_lock, LEFT, buff=0.38).set_z_index(10)
        self.play(FadeOut(cut_lbl), FadeIn(lock), run_time=0.55)
        self.play(
            Transform(lock, closed_lock),
            notch.cut_mark.animate.set_opacity(0.0),
            FadeIn(lock_lbl),
            run_time=3.6,
        )

        # Beat 3: loose amber ligand drifts freely in solution along computed path (rng(3))
        self.at("Now picture")
        rng = np.random.default_rng(3)
        loose_lig = build_ligand(x=-4.6, y_mem=2.15, stalk_len=1.05, anchored=False)
        # Keep label to the RIGHT while approaching from the left so it stays inside the frame
        lig_lbl_r = T("Loose ligand (no cell)", 28, SENDER_COL).next_to(loose_lig, RIGHT, buff=0.32).set_z_index(10)
        self.play(FadeIn(loose_lig), FadeIn(lig_lbl_r), run_time=0.45)

        target_top = notch.tip_pt[1] + 1.15
        n_steps = 8
        step_dt = 3.1 / n_steps
        for k in range(1, n_steps + 1):
            frac = k / n_steps
            bx = -4.6 * (1 - frac) + 0.0 * frac
            by = 2.15 * (1 - frac) + target_top * frac
            if k < n_steps:
                by += float(rng.normal(0, 0.12))
            cur_c = loose_lig.get_center()
            new_c = np.array([bx, by - 0.525, 0.0])
            self.play(
                loose_lig.animate.shift(new_c - cur_c),
                lig_lbl_r.animate.move_to(new_c + RIGHT * 2.35),
                run_time=step_dt,
                rate_func=linear,
            )

        # Beat 4: binds Notch with no cell holding on to pull; bobs visibly
        self.at("It binds notch")
        exact_lig = build_ligand(x=0.0, y_mem=target_top, stalk_len=1.05, anchored=False)
        lig_lbl = T("Loose ligand (no cell)", 28, SENDER_COL).next_to(exact_lig, LEFT, buff=0.35).set_z_index(10)
        self.play(
            Transform(loose_lig, exact_lig),
            swap(lig_lbl_r, lig_lbl, run_time=0.6),
            run_time=0.7,
        )
        bob(loose_lig, amp=0.10, speed=2.5, seed=1)
        self.wait(2.8)

        # Beat 5: Question card at top matching s04_pause
        self.at("Will the receptor")
        q = question_card("Loose ligand binds with no pull: does Notch switch on?",
                          y=3.15, left=-6.1, max_w=10.8, size=30, color=LOCK_COL)
        self.play(FadeIn(q.question), run_time=0.6)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Loose ligand binds with no pull: does Notch switch on?"
    CARD = {"y": 3.15, "left": -6.1, "max_w": 10.8, "size": 30, "color": LOCK_COL}
    RING_AT = (6.0, 3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_backdrop()


class S05Pull(SpokenScene):
    def construct(self):
        # Start on exact s04_pause frame (minus countdown ring)
        cyto, mem = build_receiving_zoom_stage(y_mem=-1.35, mem_thickness=0.42)
        notch = build_notch_receptor(x=0.0, y_mem=-1.35, outer_len=2.15, inner_len=1.25, cut_y_rel=0.68)
        notch.cut_mark.set_opacity(0.0)
        lock = build_lock(notch.cut_pt, open_frac=0.0, scale=1.45)
        loose_lig = build_ligand(x=0.0, y_mem=notch.tip_pt[1] + 1.15, stalk_len=1.05, anchored=False)

        mem_lbl = T("Receiving cell membrane", 26, NOTCH_COL).move_to([-3.9, -2.05, 0]).set_z_index(10)
        notch_lbl = T("Notch", 28, NOTCH_COL).move_to([1.15, 0.25, 0]).set_z_index(10)
        lock_lbl = T("Lock", 28, LOCK_COL).next_to(lock, LEFT, buff=0.38).set_z_index(10)
        lig_lbl = T("Loose ligand (no cell)", 28, SENDER_COL).next_to(loose_lig, LEFT, buff=0.35).set_z_index(10)
        tail_lbl = T("Inner tail", 26, NICD_COL).next_to(notch.inner, RIGHT, buff=0.32).set_z_index(10)
        q = question_card("Loose ligand binds with no pull: does Notch switch on?",
                          y=3.15, left=-6.1, max_w=10.8, size=30, color=LOCK_COL)

        bob(loose_lig, amp=0.10, speed=2.5, seed=1)
        self.add(cyto, mem, notch, lock, loose_lig, mem_lbl, notch_lbl, lock_lbl, lig_lbl, tail_lbl, q)
        self.play(lock.animate.scale(1.06), run_time=0.7, rate_func=there_and_back)

        # Beat 1: No — binding alone leaves the lock shut
        self.at("binding alone")
        ans = boxed_label("No — lock stays shut", color=CUT_COL, size=28).move_to([3.55, 1.45, 0]).set_z_index(10)
        self.play(FadeOut(q.question), FadeIn(ans), run_time=0.7)

        self.at("loose ligand")
        loose_lig.clear_updaters()
        self.play(
            loose_lig.animate.shift(LEFT * 2.5 + UP * 0.6).set_opacity(0.0),
            lig_lbl.animate.shift(LEFT * 2.5 + UP * 0.6).set_opacity(0.0),
            run_time=3.2,
        )
        self.remove(loose_lig, lig_lbl)

        # Beat 2: Sending cell returns above with anchored ligand
        self.at("In the standard account")
        pull = ValueTracker(0.0)
        send_mem = always_redraw(lambda: _endocytic_membrane(2.05, pull.get_value()))
        send_lbl = T("Sending cell (endocytosis)", 26, SENDER_COL).move_to([-3.6, 2.85, 0]).set_z_index(10)

        anchored_lig = always_redraw(lambda: build_ligand(
            x=0.0, y_mem=2.05 + 0.90 * pull.get_value(),
            stalk_len=2.05 + 0.90 * pull.get_value() - (notch.tip_pt[1] + 0.48 * pull.get_value()),
            anchored=True,
        ))
        anch_lbl = T("Ligand", 28, SENDER_COL).move_to([-1.35, 1.45, 0]).set_z_index(10)

        self.play(FadeOut(ans), FadeIn(send_mem, shift=DOWN * 0.3), FadeIn(send_lbl),
                  FadeIn(anchored_lig), FadeIn(anch_lbl), run_time=1.4)

        # Beat 3: Sending cell draws bound ligand inward by endocytosis (pull 0 -> 0.50)
        self.at("draws its bound ligand")
        self.remove(notch, lock)
        def _live_notch():
            n = build_notch_receptor(
                x=0.0, y_mem=-1.35, outer_len=2.15 + 0.48 * pull.get_value(),
                inner_len=1.25, cut_y_rel=0.68 + 0.25 * pull.get_value()
            )
            n.cut_mark.set_opacity(float(np.clip((pull.get_value() - 0.45) / 0.35, 0.0, 1.0)))
            return n

        live_notch = always_redraw(_live_notch)
        live_lock = always_redraw(lambda: build_lock(
            [0.0, -1.35 + 0.68 + 0.25 * pull.get_value(), 0.0],
            open_frac=float(np.clip((pull.get_value() - 0.45) / 0.55, 0.0, 1.0)),
            scale=1.45,
        ))
        self.add(live_notch, live_lock)

        tension_lbl = T("Pull", 26, LOCK_COL).move_to([1.35, 1.50, 0]).set_z_index(10)
        t_arr_u = Arrow([0.65, 1.05, 0], [0.65, 2.05, 0], color=LOCK_COL, stroke_width=5, buff=0)
        self.play(
            pull.animate.set_value(0.50),
            notch_lbl.animate.move_to([1.35, 0.25, 0]),
            FadeIn(tension_lbl), GrowArrow(t_arr_u),
            run_time=3.5,
            rate_func=linear,
        )

        # Beat 4: Tug peels the gold lock open, exposing the red Cut site
        self.at("That tug")
        cut_lbl = T("Cut site", 26, CUT_COL).move_to([-1.75, -0.45, 0]).set_z_index(10)
        self.play(
            pull.animate.set_value(1.0),
            notch_lbl.animate.move_to([1.35, 0.35, 0]),
            swap(lock_lbl, T("Lock", 28, LOCK_COL).move_to([2.25, -0.45, 0]).set_z_index(10)),
            FadeIn(cut_lbl),
            run_time=2.4,
        )
        self.finish()


class S06Adam(SpokenScene):
    def construct(self):
        # Rebuild exact end state of s05_pull with live pull tracker so tension stays active
        pull = ValueTracker(1.0)
        cyto, mem = build_receiving_zoom_stage(y_mem=-1.35, mem_thickness=0.42)
        send_mem = always_redraw(lambda: _endocytic_membrane(2.05, pull.get_value()))
        send_lbl = T("Sending cell (endocytosis)", 26, SENDER_COL).move_to([-3.6, 2.85, 0]).set_z_index(10)
        mem_lbl = T("Receiving cell membrane", 26, NOTCH_COL).move_to([-3.9, -2.05, 0]).set_z_index(10)

        notch = always_redraw(lambda: build_notch_receptor(
            x=0.0, y_mem=-1.35, outer_len=2.15 + 0.48 * pull.get_value(),
            inner_len=1.25, cut_y_rel=0.68 + 0.25 * pull.get_value()
        ))
        lock = always_redraw(lambda: build_lock(
            [0.0, -1.35 + 0.68 + 0.25 * pull.get_value(), 0.0], open_frac=1.0, scale=1.45
        ))
        lig = always_redraw(lambda: build_ligand(
            x=0.0, y_mem=2.05 + 0.90 * pull.get_value(),
            stalk_len=(2.05 + 0.90 * pull.get_value()) - (-1.35 + 2.15 + 0.48 * pull.get_value() + 0.11),
            anchored=True,
        ))

        notch_lbl = T("Notch", 28, NOTCH_COL).move_to([1.35, 0.35, 0]).set_z_index(10)
        lock_lbl = T("Lock (open)", 26, LOCK_COL).move_to([2.25, -0.45, 0]).set_z_index(10)
        cut_lbl = T("Cut site", 26, CUT_COL).move_to([-1.75, -0.45, 0]).set_z_index(10)
        lig_lbl = T("Ligand", 28, SENDER_COL).move_to([-1.35, 1.65, 0]).set_z_index(10)
        tail_lbl = T("Inner tail", 26, NICD_COL).move_to([1.35, -2.15, 0]).set_z_index(10)

        self.add(cyto, mem, send_mem, send_lbl, mem_lbl, notch, lock, lig,
                 notch_lbl, lock_lbl, cut_lbl, lig_lbl, tail_lbl)

        # Beat 1: Mammalian earlier prep cut (furin-like, halves stay joined)
        self.at("preparation cut")
        prep_pt = np.array([0.0, 0.85, 0.0])
        prep_mark = DashedLine(prep_pt + LEFT * 0.32, prep_pt + RIGHT * 0.32, color=TEXT, stroke_width=5)
        prep_lbl = fit_text("Prep cut:\nhalves stay joined", max_w=3.8, size=26, color=TEXT).move_to([4.15, 1.25, 0]).set_z_index(10)
        prep_arr = Arrow(prep_lbl.get_left() + LEFT * 0.12, prep_pt + RIGHT * 0.36,
                         color=TEXT, stroke_width=3, buff=0)
        self.play(FadeIn(prep_mark), FadeIn(prep_lbl), GrowArrow(prep_arr), run_time=0.8)
        self.play(pull.animate.set_value(1.10), run_time=1.8, rate_func=there_and_back)

        self.at("stay clasped")
        clasp_ring = Circle(radius=0.22, color=TEXT, stroke_width=3.5).move_to(prep_pt)
        self.play(Create(clasp_ring), pull.animate.set_value(1.08), run_time=1.6, rate_func=there_and_back)

        self.at("Now the")
        self.play(FadeOut(prep_mark), FadeOut(clasp_ring), FadeOut(prep_lbl), FadeOut(prep_arr), FadeOut(lock_lbl), run_time=0.6)

        # Beat 2: Pull triggers active cuts at the exposed site
        self.at("triggers the active cuts")
        cut_y_val = -1.35 + 0.93
        cut_pt_val = np.array([0.0, cut_y_val, 0.0])
        cut_ring = Circle(radius=0.25, color=CUT_COL, stroke_width=4.5).move_to(cut_pt_val)
        self.play(Create(cut_ring), pull.animate.set_value(1.12), run_time=1.0)
        self.play(cut_ring.animate.scale(1.5).set_stroke(opacity=0.25), pull.animate.set_value(1.0), run_time=1.2)
        self.remove(cut_ring)

        # Beat 3: ADAM protease shears the newly exposed site outside the membrane
        self.at("First")
        shears = build_shears([5.2, cut_y_val, 0.0]).scale(1.25)
        adam_lbl = T("ADAM protease", 28, CUT_COL).move_to([4.6, cut_y_val + 0.82, 0]).set_z_index(10)
        self.play(FadeIn(shears), FadeIn(adam_lbl), run_time=0.5)

        self.at("protease shears")
        self.play(
            shears.animate.move_to(cut_pt_val + RIGHT * 0.50),
            adam_lbl.animate.move_to([3.65, cut_y_val + 0.82, 0]),
            run_time=3.5,
            rate_func=linear,
        )
        for _ in range(2):
            self.play(
                Rotate(shears.b1, -0.35, about_point=shears.get_center() + LEFT * 0.18),
                Rotate(shears.b2, 0.35, about_point=shears.get_center() + LEFT * 0.18),
                run_time=0.55,
                rate_func=there_and_back,
            )

        # Beat 4: Outer piece departs upward with ligand, leaving a short stub
        self.at("The outer piece")
        # Freeze static versions before splitting
        self.remove(send_mem, notch, lock, lig)
        send_mem_s = _endocytic_membrane(2.05, 1.0)
        lock_s = build_lock(cut_pt_val, open_frac=1.0, scale=1.45)
        lig_s = build_ligand(x=0.0, y_mem=2.95, stalk_len=2.95 - (-1.35 + 2.63 + 0.11), anchored=True)
        stub = build_notch_receptor(x=0.0, y_mem=-1.35, outer_len=0.93, inner_len=1.25, cut_y_rel=0.93)
        stub.cut_mark.set_opacity(0.0)
        stub.tip.set_opacity(0.0)
        outer_seg = VGroup(
            Line([0.0, cut_y_val, 0], [0.0, -1.35 + 2.63, 0], color=NOTCH_COL, stroke_width=9),
            RoundedRectangle(corner_radius=0.08, width=0.32, height=0.22, stroke_color=NOTCH_COL,
                             stroke_width=3, fill_color=NOTCH_COL, fill_opacity=0.50).move_to([0.0, -1.35 + 2.63, 0]),
        )
        self.add(send_mem_s, stub, outer_seg, lock_s, lig_s)

        self.play(
            FadeOut(cut_lbl), FadeOut(adam_lbl), FadeOut(lig_lbl), FadeOut(notch_lbl),
            shears.animate.shift(RIGHT * 1.8).set_opacity(0.0),
            run_time=0.6,
        )
        self.remove(shears)

        depart_grp = VGroup(outer_seg, lock_s, lig_s)
        stub_lbl = T("Short stub", 28, NOTCH_COL).move_to([1.55, -0.55, 0]).set_z_index(10)
        self.play(
            depart_grp.animate.shift(UP * 0.95).scale(0.65).set_opacity(0.0),
            FadeIn(stub_lbl),
            run_time=3.2,
        )
        self.remove(depart_grp)
        self.finish()


class S07Gamma(SpokenScene):
    def construct(self):
        # Immediate non-black frame: zoomed oily receiving bilayer (y = -1.25..+1.05)
        cyto = Rectangle(width=13.2, height=2.6, stroke_width=0,
                         fill_color=NOTCH_COL, fill_opacity=0.14).move_to([0, -2.55, 0])
        mem = bilayer_band(-0.10, x_left=-6.6, x_right=6.6, thickness=2.30,
                           color=NOTCH_COL, fill_opacity=0.28, stroke_width=4.5)
        # Lipid-tail ticks along top and bottom leaflets, leaving central corridor open for enzyme labels
        lipid_lines = VGroup(
            *[Line([x, 0.55, 0], [x, 1.00, 0], color=NOTCH_COL, stroke_width=2).set_opacity(0.32)
              for x in np.linspace(-6.0, 6.0, 41)],
            *[Line([x, -1.20, 0], [x, -0.75, 0], color=NOTCH_COL, stroke_width=2).set_opacity(0.32)
              for x in np.linspace(-6.0, 6.0, 41)],
        )

        stub_outer = Line([0.0, -0.10, 0], [0.0, 1.85, 0], color=NOTCH_COL, stroke_width=11)
        stub_tm = Line([0.0, -1.25, 0], [0.0, -0.10, 0], color=NICD_COL, stroke_width=11)
        nicd_tail = VGroup(
            Line([0.0, -1.25, 0], [0.0, -2.55, 0], color=NICD_COL, stroke_width=11),
            Dot([0.0, -2.55, 0], radius=0.15, color=NICD_COL),
        )
        # Place Oily membrane label cleanly above the bilayer on the right
        mem_lbl = T("Oily membrane", 28, NOTCH_COL).move_to([4.5, 1.48, 0]).set_z_index(10)
        stub_lbl = T("Short stub", 28, NOTCH_COL).move_to([1.55, 1.65, 0]).set_z_index(10)
        tail_lbl = T("Inner tail", 28, NICD_COL).move_to([1.55, -1.95, 0]).set_z_index(10)

        self.add(cyto, mem, lipid_lines, stub_outer, stub_tm, nicd_tail, mem_lbl, stub_lbl, tail_lbl)
        # Zoom focus subtly onto the intramembrane cut zone
        self.play(
            VGroup(mem, lipid_lines, stub_outer, stub_tm, nicd_tail).animate.scale(1.03),
            run_time=2.2,
            rate_func=there_and_back,
        )

        # Beat 1: Cut inside the oily membrane itself
        self.at("inside the oily membrane")
        cut_ring = Circle(radius=0.30, color=CUT_COL, stroke_width=4.5).move_to([0.0, -0.25, 0])
        gs = build_gamma_secretase([-5.2, -0.25, 0.0])
        gs_lbl = T("γ-Secretase", 28, GAMMA_COL).move_to([-4.6, 1.55, 0]).set_z_index(10)
        self.play(Create(cut_ring), FadeIn(gs), run_time=1.0)
        self.play(cut_ring.animate.scale(1.5).set_stroke(opacity=0.25), gs.animate.shift(RIGHT * 0.8), run_time=1.6)
        self.remove(cut_ring)

        # Beat 2: Gamma-secretase slides steadily through the membrane to embrace the short stub
        self.at("Gamma secretase")
        self.play(FadeIn(gs_lbl), run_time=0.45)
        self.play(
            gs.animate.move_to([0.0, -0.25, 0.0]),
            gs_lbl.animate.move_to([-2.4, 1.55, 0.0]),
            run_time=5.4,
            rate_func=linear,
        )

        # Beat 2b: Hydrolysis needs water, but the membrane's interior is dry
        self.at("Cutting a protein")
        hydro_lbl = T("Cut = hydrolysis\n(needs H2O)", 25, WATER_COL, line_spacing=0.85).move_to([-4.15, -0.10, 0]).set_z_index(10)
        self.play(FadeIn(hydro_lbl), run_time=0.8)

        self.at("interior is dry")
        dry_lbl = T("Oily interior: dry", 26, LOCK_COL).move_to([4.10, -0.10, 0]).set_z_index(10)
        self.play(FadeIn(dry_lbl), run_time=0.6)
        self.play(mem[0].animate.set_fill(NOTCH_COL, opacity=0.42), run_time=1.8, rate_func=there_and_back)

        # Beat 3: Presenilin cutting subunit and water pocket inside the membrane
        self.at("cutting subunit")
        pres_lbl = T("Presenilin", 26, GAMMA_COL).move_to([3.5, 0.15, 0]).set_z_index(10)
        pres_arrow = Arrow(pres_lbl.get_left() + LEFT * 0.12, [0.75, 0.05, 0],
                           color=GAMMA_COL, stroke_width=3.5, buff=0)
        self.play(
            swap(dry_lbl, pres_lbl, run_time=0.6),
            GrowArrow(pres_arrow),
            gs.presenilin.animate.set_fill(GAMMA_COL, opacity=0.62),
            run_time=1.8,
        )

        self.at("pocket water can reach")
        water_pocket = Circle(radius=0.44, stroke_color=WATER_COL, stroke_width=4,
                              fill_color=WATER_COL, fill_opacity=0.50).move_to([0.0, -0.25, 0])
        water_lbl = T("Water pocket", 26, WATER_COL).move_to([3.7, -0.45, 0]).set_z_index(10)
        water_arrow = Arrow(water_lbl.get_left() + LEFT * 0.12, [0.42, -0.35, 0],
                            color=WATER_COL, stroke_width=3.5, buff=0)
        w_arcs = VGroup(*[
            Arc(radius=0.22 + 0.10 * i, start_angle=PI * 0.25, angle=PI * 0.5,
                color=WATER_COL, stroke_width=3.5).move_to([0.0, -1.75, 0])
            for i in range(3)
        ])
        self.play(FadeIn(water_pocket, scale=0.25), FadeIn(water_lbl), GrowArrow(water_arrow), FadeIn(w_arcs), run_time=0.9)
        self.play(w_arcs.animate.shift(UP * 1.45).set_opacity(0.0), run_time=1.3)
        self.remove(w_arcs)

        # Beat 4: Snip the stub inside the bilayer, freeing NICD downward toward the nucleus
        self.at("It snips the stub")
        nuc = nucleus_dome(y_top=-2.65, y_bot=-3.55, x_left=-5.0, x_right=5.0)
        nuc_lbl = T("Nucleus", 24, TEXT).move_to([-2.8, -3.10, 0]).set_z_index(10)
        nicd_lbl = T("NICD", 28, NICD_COL).move_to([1.55, -1.95, 0]).set_z_index(10)

        self.play(
            FadeIn(nuc, shift=UP * 0.2), FadeIn(nuc_lbl),
            swap(tail_lbl, nicd_lbl, run_time=0.6),
            stub_tm.animate.set_opacity(0.30),
            run_time=0.7,
        )
        self.play(
            nicd_tail.animate.shift(DOWN * 0.85),
            nicd_lbl.animate.shift(DOWN * 0.35),
            run_time=2.2,
            rate_func=linear,
        )
        self.finish()


class S08Nucleus(SpokenScene):
    def construct(self):
        # Deep indigo nucleus fills ~70% of the frame; DNA ribbon at y = -1.45
        nuc = RoundedRectangle(corner_radius=0.6, width=12.2, height=5.9,
                               stroke_color=NUCLEUS_COL, stroke_width=4.5,
                               fill_color=NUCLEUS_COL, fill_opacity=0.24).move_to([0, -0.35, 0])
        # Put Nucleus label on top-right so NICD entering on left never crosses it
        nuc_lbl = T("Nucleus", 28, TEXT).move_to([4.5, 2.15, 0]).set_z_index(10)
        dna = build_dna_stage(y_dna=-1.45)
        gene_lbl = T("Target gene: OFF", 26, TEXT).move_to([2.6, -2.20, 0]).set_z_index(10)

        # NICD already entering inside top-left of nucleus at t=0 (no black frame)
        nicd = VGroup(
            RoundedRectangle(corner_radius=0.14, width=1.50, height=0.54,
                             stroke_color=NICD_COL, stroke_width=3,
                             fill_color=NICD_COL, fill_opacity=0.38),
            T("NICD", 28, NICD_COL),
        ).move_to([-4.2, 2.00, 0]).set_z_index(10)

        self.add(nuc, nuc_lbl, dna, gene_lbl, nicd)

        self.at("travels directly")
        self.play(nicd.animate.move_to([-3.6, 0.75, 0]).scale(1.06), run_time=3.5, rate_func=linear)

        # Beat 2: CSL sits on DNA with Co-repressors holding target gene off
        self.at("CSL sits")
        csl = VGroup(
            RoundedRectangle(corner_radius=0.12, width=1.50, height=0.64,
                             stroke_color=CSL_COL, stroke_width=3,
                             fill_color=CSL_COL, fill_opacity=0.30),
            T("CSL", 28, TEXT),
        ).move_to([-4.0, -0.88, 0]).set_z_index(9)

        corep = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.55, height=0.58,
                             stroke_color=CSL_COL, stroke_width=2.5,
                             fill_color=CSL_COL, fill_opacity=0.24),
            T("Co-repressors", 26, TEXT),
        ).move_to([0.05, 0.60, 0]).set_z_index(9)

        self.play(FadeIn(csl), FadeIn(corep), run_time=0.6)
        self.play(
            csl.animate.move_to([-1.5, -0.88, 0]),
            corep.animate.move_to([0.05, -0.10, 0]),
            nicd.animate.move_to([-3.1, 0.35, 0]).scale(1 / 1.06),
            run_time=4.2,
            rate_func=linear,
        )

        # Beat 3: NICD binds CSL (clear of Co-repressors on the right)
        self.at("NICD binds CSL")
        self.play(nicd.animate.move_to([-2.35, -0.05, 0]), run_time=1.8)

        # Beat 4: displaces Co-repressors cleanly to the right and fades them out
        self.at("displaces")
        self.play(corep.animate.shift(RIGHT * 2.4 + UP * 1.4).set_opacity(0.0), run_time=1.3)
        self.remove(corep)

        # Beat 5: recruits Mastermind into the groove between NICD and CSL
        self.at("recruits mastermind")
        mam = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.20, height=0.54,
                             stroke_color=GENE_ON_COL, stroke_width=3,
                             fill_color=GENE_ON_COL, fill_opacity=0.32),
            T("Mastermind", 26, GENE_ON_COL),
        ).move_to([2.4, 1.45, 0]).set_z_index(10)
        self.play(FadeIn(mam), run_time=0.4)
        self.play(mam.animate.move_to([-0.15, -0.05, 0]), run_time=1.2)

        # Beat 6: Target genes turn on and emit rising Hes repressors ("not you")
        self.at("Target genes turn on")
        gene_on_lbl = T("Target gene: ON", 26, GENE_ON_COL).move_to([2.6, -2.20, 0]).set_z_index(10)
        act_arrow = Arrow([-0.70, -1.05, 0], [0.85, -1.35, 0], color=GENE_ON_COL, stroke_width=5, buff=0)
        self.play(
            dna.gene_bar.animate.set_stroke(GENE_ON_COL, width=4.5).set_fill(GENE_ON_COL, opacity=0.48),
            GrowArrow(act_arrow),
            swap(gene_lbl, gene_on_lbl, run_time=0.7),
            run_time=1.0,
        )

        self.at("many make repressors")
        not_you = T("“not you”", 28, LOCK_COL).move_to([4.90, 0.70, 0]).set_z_index(10)
        h1 = boxed_label("Hes repressor", color=GENE_ON_COL, size=24).move_to([2.6, -0.55, 0])
        h2 = boxed_label("Hes repressor", color=GENE_ON_COL, size=24).move_to([2.6, -0.55, 0])
        h3 = boxed_label("Hes repressor", color=GENE_ON_COL, size=24).move_to([2.6, -0.55, 0])
        delayed_fade = lambda t: float(np.clip((t - 0.65) / 0.35, 0.0, 1.0))
        self.play(FadeIn(not_you), FadeIn(h1), run_time=0.4)
        self.play(h1.animate.move_to([2.6, 1.40, 0]), FadeIn(h2, rate_func=delayed_fade), run_time=0.8)
        self.play(h2.animate.move_to([2.6, 0.50, 0]), FadeIn(h3, rate_func=delayed_fade), run_time=0.8)
        self.play(h3.animate.move_to([2.6, -0.40, 0]), run_time=0.7)
        self.finish()


class S09Count(SpokenScene):
    def construct(self):
        # Immediate non-black frame: single Notch on left pulled -> cut -> NICD enters nucleus
        rule_mem = bilayer_band(1.25, x_left=-5.6, x_right=-0.4, thickness=0.38, color=NOTCH_COL, fill_opacity=0.30)
        one_lig = build_ligand(x=-3.0, y_mem=2.65, stalk_len=0.45, anchored=True)
        one_notch = build_notch_receptor(x=-3.0, y_mem=1.25, outer_len=0.95, inner_len=0.85, cut_y_rel=0.35)
        rule_nuc = nucleus_dome(y_top=-1.1, y_bot=-2.9, x_left=-5.6, x_right=-0.4)
        rule_nuc_lbl = T("Nucleus", 24, TEXT).move_to([-3.0, -2.35, 0]).set_z_index(10)
        rule_txt = fit_text("1 pulled Notch  ->  1 nuclear signal", max_w=5.8, size=30, color=NICD_COL).move_to([2.8, 0.2, 0])
        self.add(rule_mem, one_lig, one_notch, rule_nuc, rule_nuc_lbl, rule_txt)

        stretched_notch = build_notch_receptor(x=-3.0, y_mem=1.25, outer_len=1.50, inner_len=0.85, cut_y_rel=0.68)
        pull_arrow = Arrow([-2.35, 2.05, 0], [-2.35, 2.85, 0], color=LOCK_COL, stroke_width=5, buff=0)
        self.play(
            one_lig.animate.shift(UP * 0.55),
            Transform(one_notch, stretched_notch),
            GrowArrow(pull_arrow),
            run_time=3.9,
            rate_func=linear,
        )

        self.at("cut one notch")
        cut_y_pos = 1.25 + 0.68
        cut_flash = Circle(radius=0.22, color=CUT_COL, stroke_width=5).move_to([-3.0, cut_y_pos, 0])
        freed_nicd = boxed_label("NICD", color=NICD_COL, size=24).move_to([-3.0, 0.55, 0])
        stub_outer = Line([-3.0, 1.25, 0], [-3.0, cut_y_pos - 0.10, 0], color=NOTCH_COL, stroke_width=9)
        upper_outer = Line([-3.0, cut_y_pos + 0.10, 0], [-3.0, 2.75, 0], color=NOTCH_COL, stroke_width=9)
        self.play(
            Create(cut_flash),
            one_notch.cut_mark.animate.scale(1.4).set_opacity(0.0),
            FadeOut(one_notch.inner),
            FadeOut(one_notch.tail_end),
            FadeIn(freed_nicd),
            FadeOut(pull_arrow),
            run_time=0.55,
        )
        self.remove(one_notch.outer, one_notch.cut_mark, one_notch.inner, one_notch.tail_end)
        one_notch.remove(one_notch.outer, one_notch.cut_mark, one_notch.inner, one_notch.tail_end)
        one_notch.add(stub_outer)
        depart_outer = VGroup(one_lig, upper_outer, one_notch.tip)
        one_notch.remove(one_notch.tip)
        self.add(upper_outer)
        self.play(
            depart_outer.animate.shift(UP * 0.75).set_opacity(0.0),
            cut_flash.animate.scale(2.0).set_stroke(opacity=0.0),
            freed_nicd.animate.move_to([-3.0, -1.75, 0]),
            rule_nuc.animate.set_fill(NUCLEUS_COL, opacity=0.45),
            run_time=2.8,
            rate_func=linear,
        )
        self.remove(depart_outer, cut_flash)

        # Beat 2: Open TwoPanel schematic comparison
        self.at("Compare notch")
        tp = TwoPanel("Notch (no relay)", "Kinase cascade",
                      colors=(NOTCH_COL, KINASE_COL), top=3.2, bottom=-2.45, gap=0.4, width=12.6, size=30)
        sc_tag = scope_tag("schematic comparison")
        self.play(FadeOut(rule_mem), FadeOut(one_notch), FadeOut(freed_nicd),
                  FadeOut(rule_nuc), FadeOut(rule_nuc_lbl), FadeOut(rule_txt), run_time=0.55)
        self.play(FadeIn(tp), FadeIn(sc_tag), run_time=0.75)

        lx = tp.area("left")[0][0]
        rx = tp.area("right")[0][0]

        notch_mem = bilayer_band(1.70, x_left=lx - 2.6, x_right=lx + 2.6, thickness=0.26, color=NOTCH_COL, fill_opacity=0.30)
        kin_mem = bilayer_band(1.70, x_left=rx - 2.6, x_right=rx + 2.6, thickness=0.26, color=KINASE_COL, fill_opacity=0.30)

        xs_l = np.linspace(lx - 2.2, lx + 2.2, 10)
        xs_r = np.linspace(rx - 2.2, rx + 2.2, 10)
        notch_recs = VGroup(*[Line([x, 1.30, 0], [x, 2.10, 0], color=NOTCH_COL, stroke_width=6.5) for x in xs_l])
        nicd_dots = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.28, height=0.28,
                             stroke_color=NICD_COL, stroke_width=2.5,
                             fill_color=NICD_COL, fill_opacity=0.75).move_to([x, 0.25, 0]).set_opacity(0.0)
            for x in xs_l
        ])
        kin_recs = VGroup(*[
            Line([x, 1.30, 0], [x, 2.10, 0], color=KINASE_COL, stroke_width=6.5).set_opacity(0.42)
            for x in xs_r
        ])

        prod_dots = VGroup(*[
            Dot([xs_r[c], 1.05 - r * 0.068, 0], radius=0.035, color=KINASE_COL).set_opacity(0.0)
            for c in range(10) for r in range(20)
        ])

        n_pulled = ValueTracker(0.0)
        k_active = ValueTracker(0.0)

        ro_left = Readout(
            [("pulled", lambda: int(round(n_pulled.get_value())), "{:3d}", SENDER_COL),
             ("NICD", lambda: int(round(n_pulled.get_value())), "{:3d}", NICD_COL),
             ("intact", lambda: 10 - int(round(n_pulled.get_value())), "{:3d}", NOTCH_COL)],
            at=[lx, -1.45, 0], size=26, widest=[10, 10, 10], color=NOTCH_COL, pad=0.22,
        )
        ro_right = Readout(
            [("active", lambda: int(round(k_active.get_value())), "{:3d}", KINASE_COL),
             ("products", lambda: int(round(20 * k_active.get_value())), "{:3d}", KINASE_COL),
             ("intact", lambda: 10, "{:3d}", KINASE_COL)],
            at=[rx, -1.45, 0], size=26, widest=[10, 200, 10], color=KINASE_COL, pad=0.22,
        )

        self.play(
            FadeIn(notch_mem), FadeIn(kin_mem),
            FadeIn(notch_recs), FadeIn(nicd_dots), FadeIn(kin_recs), FadeIn(prod_dots),
            FadeIn(ro_left), FadeIn(ro_right),
            run_time=0.8,
        )

        def update_notch_panel(mob):
            val = n_pulled.get_value()
            k = int(round(val))
            for i in range(10):
                if i < k:
                    notch_recs[i].set_opacity(0.18)
                    # Smoothly descend from membrane (y=1.15) to nuclear band (y=0.15) as it is cut
                    frac = float(np.clip(val - i, 0.0, 1.0))
                    nicd_dots[i].move_to([xs_l[i], 1.15 - 1.00 * frac, 0]).set_opacity(0.85)
                else:
                    notch_recs[i].set_opacity(1.0)
                    nicd_dots[i].set_opacity(0.0)

        def update_kinase_panel(mob):
            val = k_active.get_value()
            m = int(round(20 * val))
            for c in range(10):
                if val > c + 0.02:
                    kin_recs[c].set_opacity(1.0).set_stroke(width=10.0)
                else:
                    kin_recs[c].set_opacity(0.42).set_stroke(width=6.5)
            for i in range(200):
                prod_dots[i].set_opacity(0.95 if i < m else 0.0)

        notch_recs.add_updater(update_notch_panel)
        prod_dots.add_updater(update_kinase_panel)

        self.at("Watch the schematic")
        self.play(
            k_active.animate.set_value(10.0),
            n_pulled.animate.set_value(5.0),
            run_time=7.0,
            rate_func=linear,
        )

        self.at("Notch has no")
        self.play(
            n_pulled.animate.set_value(10.0),
            run_time=4.0,
            rate_func=linear,
        )

        self.at("Each cut receptor")
        cap = caption("Each cut receptor is used up once.", size=28, color=LOCK_COL, y=-3.05)
        self.play(FadeIn(cap), run_time=0.8)
        self.finish()


class S10Brief(SpokenScene):
    def construct(self):
        # Immediate non-black frame: taller nucleus (top at +1.75) well clear of Ub tags & top membrane
        nuc = RoundedRectangle(corner_radius=0.55, width=12.0, height=5.0,
                               stroke_color=NUCLEUS_COL, stroke_width=4,
                               fill_color=NUCLEUS_COL, fill_opacity=0.24).move_to([0, -0.75, 0])
        dna = build_dna_stage(y_dna=-2.05)
        gene_lbl = T("Target gene: ON", 26, GENE_ON_COL).move_to([2.6, -2.75, 0]).set_z_index(10)
        dna.gene_bar.set_stroke(GENE_ON_COL, width=4.5).set_fill(GENE_ON_COL, opacity=0.48)

        csl = VGroup(
            RoundedRectangle(corner_radius=0.12, width=1.50, height=0.64,
                             stroke_color=CSL_COL, stroke_width=3, fill_color=CSL_COL, fill_opacity=0.30),
            T("CSL", 28, TEXT),
        ).move_to([-1.8, -1.48, 0]).set_z_index(9)
        nicd = VGroup(
            RoundedRectangle(corner_radius=0.14, width=1.55, height=0.54,
                             stroke_color=NICD_COL, stroke_width=3, fill_color=NICD_COL, fill_opacity=0.38),
            T("NICD", 28, NICD_COL),
        ).move_to([-2.45, -0.58, 0]).set_z_index(10)
        mam = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.20, height=0.54,
                             stroke_color=GENE_ON_COL, stroke_width=3, fill_color=GENE_ON_COL, fill_opacity=0.32),
            T("Mastermind", 26, GENE_ON_COL),
        ).move_to([-0.25, -0.58, 0]).set_z_index(10)

        top_mem = bilayer_band(3.05, x_left=-5.8, x_right=5.8, thickness=0.28, color=NOTCH_COL, fill_opacity=0.30)
        top_recs = VGroup(*[Line([-4.0 + i * 0.8, 2.75, 0], [-4.0 + i * 0.8, 3.35, 0], color=NOTCH_COL, stroke_width=6.5) for i in range(3)])
        cnt_lbl = T("Direct local count: 3 pulled -> 3 NICD", 26, NICD_COL).move_to([1.6, 2.22, 0]).set_z_index(10)

        self.add(nuc, dna, gene_lbl, csl, nicd, mam, top_mem, top_recs)

        self.at("direct local count")
        fresh_capsules = VGroup(*[
            RoundedRectangle(corner_radius=0.10, width=0.68, height=0.34, stroke_color=NICD_COL,
                             stroke_width=3, fill_color=NICD_COL, fill_opacity=0.65).move_to([-4.0 + i * 0.88, 2.55, 0])
            for i in range(3)
        ])
        self.play(FadeIn(cnt_lbl), FadeIn(fresh_capsules), top_recs.animate.set_opacity(0.25), run_time=0.7)
        self.play(fresh_capsules.animate.shift(DOWN * 1.95), run_time=4.5, rate_func=linear)

        # Beat 2: Message stays brief
        self.at("stays brief")
        brief_lbl = T("Signal cleared quickly", 28, LOCK_COL).move_to([0.0, 2.22, 0]).set_z_index(10)
        self.play(FadeOut(top_recs), FadeOut(fresh_capsules), swap(cnt_lbl, brief_lbl, run_time=0.8), run_time=0.9)

        # Beat 3: Nuclear kinase marks the freed tail with P tags
        self.at("A nuclear kinase")
        kinase = boxed_label("Nuclear kinase", color=KINASE_COL, size=26).move_to([-4.6, 0.75, 0]).set_z_index(10)
        p_marks = VGroup(*[
            VGroup(Circle(radius=0.24, color=LOCK_COL, fill_color=LOCK_COL, fill_opacity=0.88, stroke_width=2),
                   T("P", 22, BG, weight=BOLD)).move_to([-2.75 + i * 0.60, 0.00, 0]).set_z_index(11)
            for i in range(2)
        ])
        self.play(FadeIn(kinase), run_time=0.4)
        self.play(kinase.animate.move_to([-2.6, 0.75, 0]), FadeIn(p_marks), run_time=1.8)
        self.play(FadeOut(kinase), run_time=0.4)

        # Beat 4: Ubiquitin tags attach directly above NICD, clear of Mastermind
        self.at("ubiquitin tags attach")
        ub_pos = [[-3.15, 0.62, 0], [-2.45, 0.74, 0], [-1.75, 0.62, 0]]
        ub_tags = VGroup(*[
            VGroup(Circle(radius=0.32, color=CUT_COL, fill_color=CUT_COL, fill_opacity=0.88, stroke_width=2),
                   T("Ub", 22, TEXT, weight=BOLD)).move_to(pos).set_z_index(11)
            for pos in ub_pos
        ])
        ub_lbl = T("Ubiquitin tags", 26, CUT_COL).next_to(ub_tags, LEFT, buff=0.15).set_z_index(10)
        self.play(FadeIn(ub_tags, shift=DOWN * 0.2), FadeIn(ub_lbl), run_time=1.2)

        # Beat 5: Proteasome draws tagged NICD in and destroys it (route UP inside nucleus then RIGHT)
        self.at("and the proteasome")
        prot = build_proteasome([3.6, -0.15, 0])
        prot_lbl = T("Proteasome", 26, TEXT).next_to(prot, DOWN, buff=0.18).set_z_index(10)
        self.play(FadeIn(prot), FadeIn(prot_lbl), FadeOut(brief_lbl), run_time=0.7)

        tagged_nicd = VGroup(nicd, p_marks, ub_tags)
        self.play(FadeOut(ub_lbl), tagged_nicd.animate.shift(UP * 0.62), run_time=0.55)
        self.play(tagged_nicd.animate.move_to([1.55, 0.72, 0]), run_time=0.70)
        self.play(
            tagged_nicd.animate.move_to(prot.get_center()).scale(0.35).set_opacity(0.0),
            run_time=0.95,
        )
        self.remove(tagged_nicd)

        # Beat 6: Pulling stops -> no fresh tails arrive -> Mastermind leaves, co-repressors return, gene dims OFF
        self.at("Once pulling stops")
        stop_lbl = T("Pulling stopped: no fresh tails arrive", 26, TEXT).move_to([0.0, 2.22, 0]).set_z_index(10)
        self.play(FadeIn(stop_lbl), FadeOut(prot), FadeOut(prot_lbl), run_time=1.2)

        self.at("direct target genes")
        corep = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.55, height=0.58,
                             stroke_color=CSL_COL, stroke_width=2.5,
                             fill_color=CSL_COL, fill_opacity=0.24),
            T("Co-repressors", 26, TEXT),
        ).move_to([-0.25, -0.58, 0]).set_z_index(9)
        gene_off_lbl = T("Target gene: OFF", 26, TEXT).move_to([2.6, -2.75, 0]).set_z_index(10)

        self.play(
            swap(mam, corep, run_time=0.9),
            dna.gene_bar.animate.set_stroke(CSL_COL, width=3.5).set_fill(CSL_COL, opacity=0.25),
            swap(gene_lbl, gene_off_lbl, run_time=0.9),
            run_time=2.8,
        )
        self.finish()


class S11End(EndCard):
    LINE = "A neighbour’s pull lets proteases cut one Notch into one nuclear signal."
