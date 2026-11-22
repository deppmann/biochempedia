"""
Beyond the Pocket, Against the Network — STEMhop Chapter 2 ("Drugs Against a Part")

COLOUR MAP (one colour per concept across the whole film):
  PROTEIN_COL = "#4A90D9"  # Slate-blue: signalling proteins and binding pockets (ABL, K-Ras, Receptor, Raf, MEK, ERK)
  NUC_COL     = "#E8A838"  # Amber-gold: high-energy nucleotides (ATP, GTP)
  GDP_COL     = "#EBCD86"  # Pale-gold: spent nucleotide (GDP, off state)
  DRUG_COL    = "#2EC4B6"  # Teal: targeted drugs (imatinib, reversible drug, sotorasib, antibody, allosteric block)
  MUT_COL     = "#E05A47"  # Coral-red: mutant Cys 12 thiol and network pushback (feedback bursts, GTP pulses, MET bypass)
  SIG_COL     = "#4CAF50"  # Emerald-green: active downstream pathway signal (ON output)
  TEXT        = "#E8EAF0"  # Crisp white: labels, formulas, readouts
  GREY        = "#8B93A1"  # Neutral structural lines (membrane, inactive dashed brake line)

CARRIED WORLD:
  A continuous view of targeted drug landing sites and living pathway circuits:
  we zoom from a kinase pocket vs. K-Ras's locked GTP switch (s01), into computed [ligand]/Kd
  pocket-share arithmetic (s02-s03), into K-Ras G12C's slow GTP->GDP cycle and induced Switch II
  covalent pocket (s04-s05), then pull back to the carried vertical cell-membrane pathway
  (Receptor -> K-Ras -> Raf -> MEK -> ERK) where outer-face, side-pocket, and covalent drugs
  meet GTP reloading, relieved negative feedback, and MET bypass (s06-s10).

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
  s01_hook: Imatinib settles into ABL's pocket then escape nudges a redesigned drug in; camera pans to K-Ras gripping GTP while a teal drug rebounds off its smooth surface and network pushback pulses loop around it.
  s02_kinase_math: Half-fill Kd bar grows to 50%, then ValueTrackers for ATP (1 mM / 10 uM = 100) and drug (1 uM / 1 nM = 1,000) drive a computed occupancy bar, share readout (~91%), and 11-pocket grid (10/11 drug-bound).
  s03_ras_math: ValueTrackers compute K-Ras GTP (0.5 mM / 10 pM = 50,000,000) vs reversible drug (5 uM / 1 nM = 5,000), shrinking the drug bar to a 1-in-10,000 hairline sliver while K-Ras stays locked on GTP and deflects reversible drug attempts.
  s04_g12c_cycle: Gly 12 transforms into protruding coral-red Cys 12 thiol with pulsing reactive ring, then slow hydrolysis sheds one phosphate from GTP->GDP and smoothly opens the Switch II loop into the off shape.
  s05_covalent: Switch II loop opens continuously beside GDP, sotorasib glides in and snaps a covalent bond to Cys 12, then scene cleanly swaps to compare untouched normal K-Ras (no Cys 12, GTP-bound) as sotorasib passes by.
  s06_other_sites: Camera pulls back onto the carried membrane pathway (Receptor->K-Ras->Raf->MEK->ERK) as downward signal pulses are intercepted sequentially by an outer-face antibody on Receptor and an allosteric block gliding into MEK's side pocket while ATP remains seated.
  s07_predict: K-Ras visibly cycles GTP<->GDP while sotorasib waits beside it, then upstream Receptor wakes up and sends coral-red activation pulses carrying fresh GTP tokens toward K-Ras as the predict card rises.
  s09_network_pushback: Three beats on the carried pathway: (1) GTP flood closes K-Ras and shrinks the GDP pool gauge, (2) MEK block drops ERK's brake line and flares upstream coral-red bursts, (3) three amplified MET receptors relight emerald-green downstream bypass pulses.
  s10_rule: Carried pathway highlights all three landing sites sequentially, locks them against competition, and sends coral-red ripple waves across the full circuit.
"""
from bp_parts import *

# ------------------------------------------------------------------ film palette
PROTEIN_COL = "#4A90D9"
NUC_COL = "#E8A838"
GDP_COL = "#EBCD86"
DRUG_COL = "#2EC4B6"
MUT_COL = "#E05A47"
SIG_COL = "#4CAF50"

# Carried pathway geometry (shared by s06, s07, s08, s09, s10)
PATH_X = -2.25
MEMB_Y = 2.28
NODE_Y = {
    "Receptor": 2.28,
    "K-Ras": 0.90,
    "Raf": -0.05,
    "MEK": -1.00,
    "ERK": -1.95,
}


# ------------------------------------------------------------------ reusable builders
def drug_chip(text, color=DRUG_COL, size=24, pad_x=0.24, pad_y=0.16):
    """Rounded drug chip sized dynamically from its label so letters never overflow or touch borders."""
    lab = T(text, size=size, color=TEXT, weight=BOLD)
    box = RoundedRectangle(
        corner_radius=0.13,
        width=lab.width + 2 * pad_x,
        height=lab.height + 2 * pad_y,
        stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.42,
    )
    g = VGroup(box, lab.move_to(box))
    g.box, g.label = box, lab
    return g


def make_nucleotide(kind="GTP", scale=1.0):
    """Amber-gold GTP (3 phosphates) or pale-gold GDP (2 phosphates) pill."""
    col = NUC_COL if kind == "GTP" else GDP_COL
    n_p = 3 if kind == "GTP" else 2
    lab = T(kind, size=max(24, int(26 * scale)), color=col, weight=BOLD)
    pill = RoundedRectangle(
        corner_radius=0.18,
        width=max(1.48 * scale, lab.width + 0.50),
        height=max(0.58 * scale, lab.height + 0.28),
        stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.28,
    )
    lab.move_to(pill)
    ps = VGroup()
    for _ in range(n_p):
        c = Circle(radius=0.12 * scale, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.48)
        ps.add(c)
    ps.arrange(RIGHT, buff=0.05 * scale).next_to(pill, RIGHT, buff=0.14 * scale)
    g = VGroup(pill, lab, ps)
    g.pill, g.label, g.phosphates = pill, lab, ps
    return g


def make_kinase_body(center, scale=1.0, title="ABL"):
    """Schematic kinase with a generous C-shaped ATP pocket on the right."""
    c = np.array(center, dtype=float)
    w, h = 4.3 * scale, 3.1 * scale
    pw, ph = 1.90 * scale, 1.38 * scale
    hw, hh = w / 2, h / 2
    pts = [
        [-hw, hh, 0], [hw, hh, 0], [hw, ph / 2, 0],
        [hw - pw, ph / 2, 0], [hw - pw, -ph / 2, 0], [hw, -ph / 2, 0],
        [hw, -hh, 0], [-hw, -hh, 0],
    ]
    body = Polygon(*pts, stroke_color=PROTEIN_COL, stroke_width=3.5, fill_color=PROTEIN_COL, fill_opacity=0.28)
    body.round_corners(radius=0.28 * scale).move_to(c)
    lab = T(title, size=32, color=TEXT, weight=BOLD).move_to(body.get_left() + RIGHT * (1.05 * scale))
    g = VGroup(body, lab)
    g.body, g.label = body, lab
    g.pocket_center = body.get_right() + LEFT * (pw * 0.44)
    return g


def make_kras_shell(center, width=5.6, height=3.4, nucleotide="GTP", pocket_open=0.0,
                    g12c=False, cys_visible=True, title="K-Ras", title_size=28):
    """Schematic K-Ras with upper nucleotide cradle and articulated bottom Switch II loop."""
    c = np.array(center, dtype=float)
    top_h = height * 0.58
    top_body = RoundedRectangle(
        corner_radius=0.44, width=width, height=top_h,
        stroke_color=PROTEIN_COL, stroke_width=3.5, fill_color=PROTEIN_COL, fill_opacity=0.28,
    ).move_to(c + UP * (height * 0.22))

    cradle_w = width * 0.49
    cradle = RoundedRectangle(
        corner_radius=0.18, width=cradle_w, height=top_h * 0.62,
        stroke_color=PROTEIN_COL, stroke_width=2.5, fill_color=BG, fill_opacity=1.0,
    ).move_to(top_body.get_right() + LEFT * (cradle_w / 2 + 0.18))

    nuc = make_nucleotide(nucleotide, scale=0.84)
    if nuc.width > cradle_w - 0.24:
        nuc.scale_to_fit_width(cradle_w - 0.24)
    nuc.move_to(cradle)

    loop_w = width * 0.86
    loop_h = height * 0.24
    drop = 1.00 * pocket_open
    closed_center = top_body.get_bottom() + DOWN * (loop_h * 0.45 + drop) + RIGHT * (width * 0.03)
    loop_rect = RoundedRectangle(
        corner_radius=0.18, width=loop_w, height=loop_h,
        stroke_color=PROTEIN_COL, stroke_width=3.2, fill_color=PROTEIN_COL, fill_opacity=0.34,
    ).move_to(closed_center)

    def _draw_hinges():
        y_top = top_body.get_bottom()[1]
        y_bot = loop_rect.get_top()[1]
        gap = y_top - y_bot
        if gap <= 0.02:
            return VGroup(Line(top_body.get_bottom(), top_body.get_bottom(), stroke_width=0, stroke_opacity=0))
        hinge_w = 0.22
        x_l = loop_rect.get_left()[0] + 0.24
        x_r = min(top_body.get_right()[0] - 0.50, loop_rect.get_right()[0] - 0.22)
        ymid = (y_top + y_bot) / 2
        parts = VGroup()
        for hx in (x_l, x_r):
            fill_bar = Rectangle(
                width=hinge_w, height=gap + 0.04,
                stroke_width=0, fill_color=PROTEIN_COL, fill_opacity=0.28,
            ).move_to([hx, ymid, 0])
            edge_l = Line([hx - hinge_w / 2, y_top, 0], [hx - hinge_w / 2, y_bot, 0], color=PROTEIN_COL, stroke_width=3.2)
            edge_r = Line([hx + hinge_w / 2, y_top, 0], [hx + hinge_w / 2, y_bot, 0], color=PROTEIN_COL, stroke_width=3.2)
            parts.add(fill_bar, edge_l, edge_r)
        return parts

    hinges = always_redraw(_draw_hinges)

    res_pos = top_body.get_bottom() + RIGHT * (width * 0.30)
    if g12c:
        res = Polygon(
            [-0.14, 0.06, 0], [0.14, 0.06, 0], [0.07, -0.34, 0], [-0.07, -0.34, 0],
            stroke_color=MUT_COL, stroke_width=2.5, fill_color=MUT_COL, fill_opacity=0.90,
        ).move_to(res_pos + DOWN * 0.16)
    else:
        res = Dot(res_pos, radius=0.09, color=GREY)
    if not cys_visible:
        res.set_opacity(0)

    left_zone_w = width - cradle_w - 0.35
    k_lab = T(title, size=title_size, color=TEXT, weight=BOLD)
    if k_lab.width > left_zone_w:
        k_lab = T(title, size=24, color=TEXT, weight=BOLD)
    k_lab.move_to(top_body.get_left() + RIGHT * (left_zone_w / 2 + 0.12))

    g = VGroup(hinges, top_body, cradle, nuc, loop_rect, res, k_lab)
    g.hinges = hinges
    g.top_body = top_body
    g.cradle = cradle
    g.nuc = nuc
    g.loop = loop_rect
    g.res = res
    g.label = k_lab
    g.pocket_spot = top_body.get_bottom() + DOWN * 0.52 + LEFT * (width * 0.04)
    return g


def make_occupancy_bar(center, width, height, nat_tracker, drug_tracker, nat_col=NUC_COL, drug_col=DRUG_COL):
    """Computed pocket occupancy bar with fixed 4-child topology so always_redraw never drops fills."""
    c = np.array(center, dtype=float)

    def _draw():
        a = max(0.0, float(nat_tracker.get_value()))
        d = max(0.0, float(drug_tracker.get_value()))
        total = a + d
        frame = RoundedRectangle(
            corner_radius=0.14, width=width, height=height,
            stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=0.95,
        ).move_to(c)
        inner_w = width - 0.08
        inner_h = height - 0.08
        left_x = c[0] - inner_w / 2

        if total <= 1e-9:
            r_a = Rectangle(width=0.002, height=inner_h, stroke_width=0, fill_color=nat_col, fill_opacity=0.0).move_to([left_x, c[1], 0])
            r_d = Rectangle(width=0.002, height=inner_h, stroke_width=0, fill_color=drug_col, fill_opacity=0.0).move_to([left_x + inner_w, c[1], 0])
        else:
            f_d = d / total
            dw = max(0.08, inner_w * f_d) if d > 0 else 0.0
            aw = max(0.0, inner_w - dw) if a > 0 else 0.0
            if aw > 0.01:
                r_a = Rectangle(width=aw, height=inner_h, stroke_width=0, fill_color=nat_col, fill_opacity=0.84).move_to([left_x + aw / 2, c[1], 0])
            else:
                r_a = Rectangle(width=0.002, height=inner_h, stroke_width=0, fill_color=nat_col, fill_opacity=0.0).move_to([left_x, c[1], 0])
            if dw > 0.01:
                r_d = Rectangle(width=dw, height=inner_h, stroke_width=0, fill_color=drug_col, fill_opacity=0.94).move_to([left_x + aw + dw / 2, c[1], 0])
            else:
                r_d = Rectangle(width=0.002, height=inner_h, stroke_width=0, fill_color=drug_col, fill_opacity=0.0).move_to([left_x + inner_w, c[1], 0])

        border = RoundedRectangle(
            corner_radius=0.14, width=width, height=height,
            stroke_color=TEXT, stroke_width=2.5, fill_opacity=0.0,
        ).move_to(c)
        return VGroup(frame, r_a, r_d, border)

    return always_redraw(_draw)


def make_antibody(pos, scale=1.0):
    """Teal Y-shaped antibody schematic."""
    p = np.array(pos, dtype=float)
    stem = Line([0, 0.55 * scale, 0], [0, 0.14 * scale, 0], color=DRUG_COL, stroke_width=6.5 * scale)
    arm_l = Line([0, 0.14 * scale, 0], [-0.30 * scale, -0.22 * scale, 0], color=DRUG_COL, stroke_width=6.5 * scale)
    arm_r = Line([0, 0.14 * scale, 0], [0.30 * scale, -0.22 * scale, 0], color=DRUG_COL, stroke_width=6.5 * scale)
    return VGroup(stem, arm_l, arm_r).move_to(p)


def build_pathway(x=PATH_X):
    """Build the carried cell-membrane vertical pathway: Receptor -> K-Ras -> Raf -> MEK -> ERK."""
    memb_top = Line([-6.2, MEMB_Y + 0.16, 0], [6.2, MEMB_Y + 0.16, 0], color=GREY, stroke_width=3)
    memb_bot = Line([-6.2, MEMB_Y - 0.16, 0], [6.2, MEMB_Y - 0.16, 0], color=GREY, stroke_width=3)
    memb_fill = Rectangle(width=12.4, height=0.32, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([0, MEMB_Y, 0])
    memb = VGroup(memb_fill, memb_top, memb_bot)

    out_lab = T("Outside cell", size=24, color=TEXT).move_to([-5.05, MEMB_Y + 0.46, 0])
    in_lab = T("Inside cell", size=24, color=TEXT).move_to([-5.15, MEMB_Y - 0.46, 0])

    rec_outer = RoundedRectangle(
        corner_radius=0.16, width=1.25, height=0.54,
        stroke_color=PROTEIN_COL, stroke_width=3, fill_color=PROTEIN_COL, fill_opacity=0.34,
    ).move_to([x, MEMB_Y + 0.44, 0])
    rec_stalk = Rectangle(
        width=0.46, height=0.42,
        stroke_color=PROTEIN_COL, stroke_width=2.5, fill_color=PROTEIN_COL, fill_opacity=0.34,
    ).move_to([x, MEMB_Y, 0])
    rec_inner = RoundedRectangle(
        corner_radius=0.14, width=2.05, height=0.52,
        stroke_color=PROTEIN_COL, stroke_width=3, fill_color=PROTEIN_COL, fill_opacity=0.30,
    ).move_to([x, MEMB_Y - 0.44, 0])
    rec_lab = T("Receptor", size=24, color=TEXT, weight=BOLD).move_to(rec_inner)
    rec = VGroup(rec_stalk, rec_outer, rec_inner, rec_lab)
    rec.outer, rec.inner, rec.label = rec_outer, rec_inner, rec_lab

    def node_box(name, y, w=2.45, h=0.62):
        b = RoundedRectangle(
            corner_radius=0.14, width=w, height=h,
            stroke_color=PROTEIN_COL, stroke_width=3, fill_color=PROTEIN_COL, fill_opacity=0.30,
        ).move_to([x, y, 0])
        l = T(name, size=26, color=TEXT, weight=BOLD).move_to(b)
        g = VGroup(b, l)
        g.box, g.label = b, l
        return g

    kras = node_box("K-Ras", NODE_Y["K-Ras"], w=2.45, h=0.62)
    raf = node_box("Raf", NODE_Y["Raf"], w=2.10, h=0.58)
    mek = node_box("MEK", NODE_Y["MEK"], w=2.55, h=0.64)
    erk = node_box("ERK", NODE_Y["ERK"], w=2.10, h=0.58)

    def conn(top_mob, bot_mob, color=SIG_COL):
        a = top_mob.get_bottom() + DOWN * 0.04
        b = bot_mob.get_top() + UP * 0.04
        return Arrow(a, b, buff=0.0, stroke_width=4.5, max_tip_length_to_length_ratio=0.35, color=color)

    arrows = VGroup(
        conn(rec_inner, kras),
        conn(kras, raf),
        conn(raf, mek),
        conn(mek, erk),
    )

    world = VGroup(memb, out_lab, in_lab, rec, kras, raf, mek, erk, arrows)
    world.memb = memb
    world.out_lab = out_lab
    world.in_lab = in_lab
    world.rec = rec
    world.kras = kras
    world.raf = raf
    world.mek = mek
    world.erk = erk
    world.arrows = arrows
    return world


def make_signal_pill(path_mob, color=SIG_COL, speed=1.3, phase=0.0, w=0.34, h=0.17):
    """Substantial moving signal pulse pill along a line/arrow/curve."""
    pill = RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.95)
    pill._t = phase

    def _u(mob, dt):
        mob._t = (mob._t + dt * speed) % 1.0
        mob.move_to(path_mob.point_from_proportion(mob._t))

    pill.add_updater(_u)
    return pill


# ================================================================== SCENES

class S00Title(TitleCard):
    LESSON = "Drugs Against a Part"
    TITLE = "Beyond the Pocket, Against the Network"


class S01Hook(SpokenScene):
    def construct(self):
        abl = make_kinase_body([-3.0, 0.25, 0], scale=1.0, title="ABL")
        abl_tag = T("Kinase pocket", size=28, color=PROTEIN_COL).next_to(abl, UP, buff=0.3)
        imat = drug_chip("Imatinib", size=24, pad_x=0.22, pad_y=0.15).move_to(abl.pocket_center + RIGHT * 1.95)

        self.play(FadeIn(abl), FadeIn(abl_tag), FadeIn(imat), run_time=0.9)
        self.at("imatinib won")
        self.play(imat.animate.move_to(abl.pocket_center + RIGHT * 0.14), run_time=0.9)

        self.at("escape guided")
        bump = Circle(radius=0.18, stroke_color=MUT_COL, stroke_width=2.5, fill_color=MUT_COL, fill_opacity=0.88)
        bump.move_to(abl.pocket_center + LEFT * 0.64 + UP * 0.42)
        nd = drug_chip("Next drug", size=24, pad_x=0.20, pad_y=0.14).move_to(abl.pocket_center + RIGHT * 2.4 + DOWN * 0.15)
        self.play(FadeIn(bump, scale=1.3), imat.animate.shift(RIGHT * 2.0 + UP * 0.8).set_opacity(0), run_time=0.65)
        self.remove(imat)
        self.play(FadeIn(nd), run_time=0.3)
        self.play(nd.animate.move_to(abl.pocket_center + RIGHT * 0.28 + DOWN * 0.12), run_time=0.7)

        self.at("why did that")
        kras = make_kras_shell([7.6, 0.25, 0], width=5.4, height=3.3, nucleotide="GTP", pocket_open=0.0, title="K-Ras")
        kras_tag = T("Locked switch", size=30, color=PROTEIN_COL).next_to(kras, UP, buff=0.3)
        left_grp = VGroup(abl, abl_tag, bump, nd)
        right_grp = VGroup(kras, kras_tag)
        self.play(
            left_grp.animate.shift(LEFT * 9.0).set_opacity(0),
            right_grp.animate.shift(LEFT * 7.8),
            run_time=1.3,
        )
        self.remove(left_grp)
        q_tag = T("No open pocket", size=28, color=NUC_COL).next_to(kras, DOWN, buff=0.35)
        self.play(FadeIn(q_tag), run_time=0.45)

        self.at("cancer switch")
        db = drug_chip("Drug", size=26, pad_x=0.32, pad_y=0.16).move_to([5.1, -0.35, 0])
        self.play(FadeIn(db), run_time=0.25)
        self.play(db.animate.move_to(kras.get_right() + RIGHT * 0.90 + DOWN * 0.25), run_time=0.55)
        self.play(db.animate.shift(RIGHT * 1.40 + DOWN * 0.35).rotate(-0.20), run_time=0.65)

        self.at("networks push back")
        self.play(FadeOut(q_tag), kras_tag.animate.shift(UP * 0.30), run_time=0.3)
        arc_top = CurvedArrow(
            [kras.get_right()[0] + 0.40, kras.top_body.get_top()[1] + 0.05, 0],
            [kras.get_left()[0] - 0.40, kras.top_body.get_top()[1] + 0.05, 0],
            angle=0.35, color=MUT_COL, stroke_width=4.5,
        )
        arc_bot = CurvedArrow(
            [kras.get_left()[0] - 0.40, kras.loop.get_bottom()[1] - 0.12, 0],
            [kras.get_right()[0] + 0.40, kras.loop.get_bottom()[1] - 0.12, 0],
            angle=0.35, color=MUT_COL, stroke_width=4.5,
        )
        push_lab = T("Network pushback?", size=30, color=MUT_COL, weight=BOLD).next_to(arc_bot, DOWN, buff=0.25)
        p_top = make_signal_pill(arc_top, MUT_COL, speed=0.95, phase=0.0, w=0.36, h=0.18)
        p_bot = make_signal_pill(arc_bot, MUT_COL, speed=0.95, phase=0.0, w=0.36, h=0.18)
        self.play(Create(arc_top), Create(arc_bot), FadeIn(push_lab), run_time=0.75)
        self.add(p_top, p_bot)
        self.finish()


class S02KinaseMath(SpokenScene):
    def construct(self):
        formula = M("Share scales with  [ligand] / Kd", size=34, color=TEXT).move_to([0, 3.05, 0])
        atp_s = ValueTracker(0.0)
        drug_s = ValueTracker(0.0)
        bar = make_occupancy_bar([0, -0.35, 0], width=11.0, height=1.20, nat_tracker=atp_s, drug_tracker=drug_s)
        self.play(Write(formula), FadeIn(bar), run_time=1.2)

        self.at("a ligand's share")
        kd_note = T("At [ligand] = Kd, half the sites fill", size=28, color=NUC_COL).move_to([0, 1.72, 0])
        half_bar = RoundedRectangle(
            corner_radius=0.12, width=7.0, height=0.62,
            stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=0.95,
        ).move_to([0, 0.96, 0])
        half_trk = ValueTracker(0.02)
        half_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.08, 6.90 * half_trk.get_value()), height=0.52,
                stroke_width=0, fill_color=NUC_COL, fill_opacity=0.84,
            ).move_to([half_bar.get_left()[0] + 0.05 + max(0.08, 6.90 * half_trk.get_value()) / 2, 0.96, 0])
        )
        self.play(FadeIn(half_bar), run_time=0.6)

        self.at("dissociation constant")
        self.play(FadeIn(kd_note), run_time=0.55)
        self.add(half_fill)
        self.play(
            half_trk.animate.set_value(0.50),
            run_time=max(0.9, self.t_of("fills half the sites") + 0.9 - self.elapsed()),
            rate_func=linear,
        )

        self.at("for a typical kinase")
        half_fill.clear_updaters()
        self.play(FadeOut(kd_note), FadeOut(half_bar), FadeOut(half_fill), run_time=0.4)
        case_head = T("Typical kinase pocket", size=32, color=PROTEIN_COL, weight=BOLD).move_to([0, 2.30, 0])
        self.play(FadeIn(case_head), run_time=0.45)

        atp_card = RoundedRectangle(
            corner_radius=0.14, width=5.4, height=1.28,
            stroke_color=NUC_COL, stroke_width=2.5, fill_color=NUC_COL, fill_opacity=0.18,
        ).move_to([-2.95, 1.25, 0])
        atp_expr = M("ATP: 1 mM ÷ 10 µM", size=26, color=NUC_COL).move_to([-2.95, 1.54, 0])
        atp_num = counter("= {:.0f}", atp_s, at=[-2.95, 0.98, 0], size=28, color=NUC_COL)

        self.at("1 millimolar")
        self.play(FadeIn(atp_card), FadeIn(atp_expr), run_time=0.6)

        self.at("10 micromolar")
        pockets = VGroup()
        for _ in range(11):
            sq = RoundedRectangle(
                corner_radius=0.1, width=0.74, height=0.74,
                stroke_color=PROTEIN_COL, stroke_width=2.5, fill_color=NUC_COL, fill_opacity=0.72,
            )
            pockets.add(sq)
        pockets.arrange(RIGHT, buff=0.22).move_to([0, -2.15, 0])
        self.add(atp_num)
        self.play(atp_s.animate.set_value(100.0), FadeIn(pockets), run_time=1.6)

        self.at("a drug with")
        drug_card = RoundedRectangle(
            corner_radius=0.14, width=5.4, height=1.28,
            stroke_color=DRUG_COL, stroke_width=2.5, fill_color=DRUG_COL, fill_opacity=0.18,
        ).move_to([2.95, 1.25, 0])
        drug_expr = M("Drug: 1 µM ÷ 1 nM", size=26, color=DRUG_COL).move_to([2.95, 1.54, 0])
        drug_num = counter("= {:,.0f}", drug_s, at=[2.95, 0.98, 0], size=28, color=DRUG_COL)
        self.play(FadeIn(drug_card), FadeIn(drug_expr), run_time=0.7)

        share_readout = always_redraw(
            lambda: M(
                f"Drug share: ~{100.0 * drug_s.get_value() / max(1.0, atp_s.get_value() + drug_s.get_value()):.0f}%",
                size=30, color=DRUG_COL,
            ).move_to([0, -1.32, 0])
        )

        def _upd_pockets(grp):
            a = atp_s.get_value()
            d = drug_s.get_value()
            n_drug = int(round(11.0 * d / max(1.0, a + d)))
            for idx, sq in enumerate(grp):
                if idx >= 11 - n_drug:
                    sq.set_fill(DRUG_COL, opacity=0.82)
                else:
                    sq.set_fill(NUC_COL, opacity=0.72)

        pockets.add_updater(_upd_pockets)

        self.at("reaching")
        self.add(drug_num, share_readout)
        self.play(drug_s.animate.set_value(1000.0), run_time=2.05)

        self.at("wins the pocket")
        win_tag = T("Drug claims ~91% of sites", size=28, color=TEXT, weight=BOLD).move_to([0, -2.95, 0])
        self.play(FadeIn(win_tag), run_time=0.4)
        self.finish()


class S03RasMath(SpokenScene):
    def construct(self):
        formula = M("Share scales with  [ligand] / Kd", size=34, color=TEXT).move_to([0, 3.05, 0])
        case_head = T("K-Ras pocket", size=32, color=PROTEIN_COL, weight=BOLD).move_to([0, 2.30, 0])

        gtp_s = ValueTracker(0.0)
        drug_s = ValueTracker(0.0)
        bar = make_occupancy_bar([0, -0.35, 0], width=11.0, height=1.20, nat_tracker=gtp_s, drug_tracker=drug_s)
        kras_locked = make_kras_shell([-3.35, -2.18, 0], width=4.65, height=2.2, nucleotide="GTP", pocket_open=0.0, title="K-Ras", title_size=24)
        self.add(formula, case_head, bar, kras_locked)

        gtp_card = RoundedRectangle(
            corner_radius=0.14, width=5.6, height=1.28,
            stroke_color=NUC_COL, stroke_width=2.5, fill_color=NUC_COL, fill_opacity=0.18,
        ).move_to([-2.95, 1.25, 0])
        gtp_conc = M("GTP: 0.5 mM", size=26, color=NUC_COL).move_to([-3.85, 1.54, 0])
        gtp_kd = M("÷ 10 pM", size=26, color=NUC_COL).next_to(gtp_conc, RIGHT, buff=0.18)

        # Keep visual motion real: stream amber-gold GTP tokens toward K-Ras from the right without crossing K-Ras
        gtp_flow = VGroup(*[
            RoundedRectangle(corner_radius=0.10, width=0.58, height=0.28, stroke_color=NUC_COL, stroke_width=2, fill_color=NUC_COL, fill_opacity=0.85)
            for _ in range(3)
        ])
        for idx, tok in enumerate(gtp_flow):
            tok.move_to([1.35 + idx * 0.76, -1.75, 0])

        self.at("cellular gtp")
        self.play(FadeIn(gtp_card), FadeIn(gtp_conc), run_time=0.7)

        self.at("while ras holds")
        self.play(FadeIn(gtp_kd), FadeIn(gtp_flow), run_time=0.55)
        gtp_num = counter("= {:,.0f}", gtp_s, at=[-2.95, 0.98, 0], size=28, color=NUC_COL)
        self.add(gtp_num)
        self.play(
            gtp_s.animate.set_value(26_000_000.0),
            gtp_flow.animate.shift(LEFT * 1.45),
            run_time=max(0.8, self.t_of("is 50 million") - 0.2 - self.elapsed()),
            rate_func=linear,
        )

        self.at("is 50 million")
        self.play(
            gtp_s.animate.set_value(50_000_000.0),
            FadeOut(gtp_flow, shift=LEFT * 0.35),
            run_time=0.6,
        )

        self.at("a strong reversible drug")
        drug_card = RoundedRectangle(
            corner_radius=0.14, width=5.6, height=1.28,
            stroke_color=DRUG_COL, stroke_width=2.5, fill_color=DRUG_COL, fill_opacity=0.18,
        ).move_to([2.95, 1.25, 0])
        drug_expr = M("Drug: 5 µM ÷ 1 nM", size=26, color=DRUG_COL).move_to([2.95, 1.54, 0])
        drug_num = counter("= {:,.0f}", drug_s, at=[2.95, 0.98, 0], size=28, color=DRUG_COL)
        bouncer = drug_chip("Drug", size=24, pad_x=0.18, pad_y=0.12).move_to([-0.15, -2.18, 0])
        self.play(FadeIn(drug_card), FadeIn(drug_expr), FadeIn(bouncer), run_time=0.7)
        self.add(drug_num)
        self.play(
            drug_s.animate.set_value(2200.0),
            bouncer.animate.move_to(kras_locked.get_right() + RIGHT * 0.58),
            run_time=max(0.5, self.t_of("scores") - 0.2 - self.elapsed()),
            rate_func=linear,
        )

        self.at("scores")
        self.play(
            drug_s.animate.set_value(5000.0),
            bouncer.animate.move_to([-0.15, -2.18, 0]),
            run_time=0.7,
        )

        self.at("that leaves barely")
        sliver_pt = [5.42, -0.95, 0]
        sliver_lab = T("1 in 10,000 holding drug", size=28, color=DRUG_COL, weight=BOLD).move_to([3.10, -2.05, 0])
        ptr = Arrow(sliver_lab.get_top() + UP * 0.08 + RIGHT * 0.6, sliver_pt, buff=0.04, color=DRUG_COL, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        gtp_locked_lab = T("GTP stays locked in pocket", size=26, color=NUC_COL).move_to([3.10, -2.75, 0])
        self.play(GrowArrow(ptr), FadeIn(sliver_lab), run_time=0.75)
        self.play(FadeIn(gtp_locked_lab), run_time=0.45)
        self.play(bouncer.animate.move_to(kras_locked.get_right() + RIGHT * 0.58), run_time=0.6)
        self.play(bouncer.animate.move_to([-0.20, -2.18, 0]), run_time=0.6)
        self.finish()


class S04G12cCycle(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        kras = make_kras_shell([0, 0.25, 0], width=5.8, height=3.4, nucleotide="GTP", pocket_open=0.0, g12c=False, title="K-Ras", title_size=28)
        head = T("K-Ras nucleotide cycle", size=32, color=PROTEIN_COL, weight=BOLD).move_to([0, 3.05, 0])
        self.add(tag, kras, head)

        self.at("stopped fighting")
        rd = drug_chip("Drug", size=26, pad_x=0.28, pad_y=0.16).move_to([4.7, 0.9, 0])
        self.play(FadeIn(rd), run_time=0.35)
        self.play(rd.animate.shift(LEFT * 1.1), run_time=0.6)
        self.play(rd.animate.shift(RIGHT * 1.3), run_time=0.55)
        self.play(FadeOut(rd, shift=RIGHT * 1.0), run_time=0.55)

        # Visible target ring zooming onto Gly 12 before mutation
        gly_lab = T("Gly 12", size=28, color=TEXT).move_to([4.25, -0.35, 0])
        gly_ptr = Arrow(gly_lab.get_left() + LEFT * 0.14, kras.res.get_right() + RIGHT * 0.16, buff=0, color=TEXT, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        focus_ring = Circle(radius=0.55, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(kras.res)
        self.play(FadeIn(gly_lab), GrowArrow(gly_ptr), Create(focus_ring), run_time=0.8)
        self.play(focus_ring.animate.scale(0.45).set_stroke(MUT_COL, width=4), run_time=1.3)

        self.at("replaces glycine")
        cys_prong = Polygon(
            [-0.16, 0.06, 0], [0.16, 0.06, 0], [0.08, -0.44, 0], [-0.08, -0.44, 0],
            stroke_color=MUT_COL, stroke_width=3, fill_color=MUT_COL, fill_opacity=0.90,
        ).move_to(kras.top_body.get_bottom() + RIGHT * (5.8 * 0.30) + DOWN * 0.19)
        new_head = T("K-Ras G12C", size=32, color=PROTEIN_COL, weight=BOLD).move_to([0, 3.05, 0])
        cys_lab = T("Cys 12", size=28, color=MUT_COL, weight=BOLD).move_to([4.25, -0.35, 0])
        cys_ptr = Arrow(cys_lab.get_left() + LEFT * 0.16, cys_prong.get_right() + RIGHT * 0.16, buff=0, color=MUT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        self.play(
            FadeOut(focus_ring),
            FadeOut(gly_ptr),
            Transform(kras.res, cys_prong),
            swap(gly_lab, cys_lab, run_time=0.6),
            swap(head, new_head, run_time=0.6),
            GrowArrow(cys_ptr),
            run_time=1.0,
        )
        # Keep reactive site visibly active as narrator describes cysteine replacing glycine
        self.play(kras.loop.animate.shift(DOWN * 0.16), run_time=1.0)
        self.play(kras.loop.animate.shift(UP * 0.16), run_time=1.0)

        self.at("reactive sulfur")
        thiol_tip = Circle(radius=0.15, stroke_color=MUT_COL, stroke_width=3, fill_color=NUC_COL, fill_opacity=0.95).move_to(cys_prong.get_bottom())
        thiol_lab = T("Cys 12 thiol", size=30, color=MUT_COL, weight=BOLD).move_to([4.45, -0.35, 0])
        thiol_ptr = Arrow(thiol_lab.get_left() + LEFT * 0.16, thiol_tip.get_right() + RIGHT * 0.16, buff=0, color=MUT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        self.play(
            FadeIn(thiol_tip, scale=1.4),
            FadeOut(cys_ptr),
            swap(cys_lab, thiol_lab, run_time=0.6),
            GrowArrow(thiol_ptr),
            run_time=0.9,
        )

        self.play(thiol_tip.animate.scale(1.25), rate_func=there_and_back, run_time=1.1)

        # Smoothly begin slow GTP -> GDP hydrolysis and Switch II shift on "Even mutant K-Ras G12C still slowly cuts"
        self.at("even mutant")
        p3 = kras.nuc.phosphates[2]
        gdp_nuc = make_nucleotide("GDP", scale=0.84).move_to(kras.cradle)
        gdp_nuc.set_opacity(0)
        off_lab = T("GDP shape (off)", size=28, color=GDP_COL, weight=BOLD).move_to([0, -2.65, 0])

        self.play(
            p3.animate.shift(UR * 0.6).set_opacity(0.45),
            kras.loop.animate.shift(DOWN * 0.25),
            run_time=max(0.8, self.t_of("slowly cuts") - 0.2 - self.elapsed()),
            rate_func=linear,
        )

        self.at("slowly cuts")
        self.play(
            p3.animate.shift(UR * 0.65).set_opacity(0),
            kras.nuc.pill.animate.set_stroke(GDP_COL).set_fill(GDP_COL, opacity=0.28),
            kras.nuc.phosphates[0].animate.set_stroke(GDP_COL).set_fill(GDP_COL, opacity=0.48),
            kras.nuc.phosphates[1].animate.set_stroke(GDP_COL).set_fill(GDP_COL, opacity=0.48),
            kras.loop.animate.shift(DOWN * 0.47),
            run_time=1.45,
        )
        gdp_nuc.label.move_to(kras.nuc.pill)
        self.play(swap(kras.nuc.label, gdp_nuc.label.set_opacity(1), run_time=0.55), run_time=0.55)
        self.play(FadeIn(off_lab), run_time=0.45)
        self.finish()


class S05Covalent(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        kras = make_kras_shell([-0.2, 0.35, 0], width=5.6, height=3.3, nucleotide="GDP", pocket_open=0.72, g12c=True, title="K-Ras G12C")
        thiol_tip = Circle(radius=0.14, stroke_color=MUT_COL, stroke_width=3, fill_color=NUC_COL, fill_opacity=0.95)
        thiol_tip.move_to(kras.res.get_bottom() + DOWN * 0.04)
        cys_lab = T("Cys 12", size=28, color=MUT_COL, weight=BOLD).move_to([3.95, -0.20, 0])
        cys_ptr = Arrow(cys_lab.get_left() + LEFT * 0.14, thiol_tip.get_right() + RIGHT * 0.14, buff=0, color=MUT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        self.add(tag, kras, thiol_tip, cys_lab, cys_ptr)

        self.at("hidden pocket opens")
        pocket_glow = RoundedRectangle(
            corner_radius=0.18, width=2.45, height=0.84,
            stroke_color=DRUG_COL, stroke_width=2.5, fill_color=DRUG_COL, fill_opacity=0.16,
        ).move_to(kras.pocket_spot)
        sw_lab = T("Switch II pocket", size=28, color=PROTEIN_COL, weight=BOLD).move_to([-4.45, -0.75, 0])
        sw_ptr = Arrow(sw_lab.get_right() + RIGHT * 0.1, pocket_glow.get_left() + LEFT * 0.1, buff=0, color=PROTEIN_COL, stroke_width=3.5, max_tip_length_to_length_ratio=0.22)
        self.play(kras.loop.animate.shift(DOWN * 0.36), FadeIn(sw_lab), run_time=1.5)
        self.play(FadeIn(pocket_glow, scale=0.85), GrowArrow(sw_ptr), run_time=0.9)
        self.play(pocket_glow.animate.set_fill(DRUG_COL, opacity=0.30), run_time=1.4)

        self.at("enters and forms")
        soto = drug_chip("Sotorasib", size=24, pad_x=0.22, pad_y=0.14).move_to([-4.6, pocket_glow.get_y(), 0]).set_z_index(2)
        self.play(FadeOut(sw_ptr), FadeOut(sw_lab), run_time=0.28)
        self.play(FadeIn(soto), run_time=0.25)
        self.play(soto.animate.move_to(pocket_glow.get_center() + LEFT * 0.22), run_time=0.85)

        self.at("permanent covalent bond")
        bond = Line(
            soto.get_right(), thiol_tip.get_left() + LEFT * 0.04,
            color=MUT_COL, stroke_width=7,
        )
        bond_lab = T("Permanent covalent bond", size=28, color=DRUG_COL, weight=BOLD).move_to([0, -2.75, 0])
        self.play(Create(bond), FadeIn(bond_lab), run_time=0.85)

        self.at("lack cysteine")
        kras_left = make_kras_shell([-3.35, 0.35, 0], width=4.8, height=2.9, nucleotide="GDP", pocket_open=1.0, g12c=True, title="K-Ras G12C", title_size=24)
        thiol_left = Circle(radius=0.12, stroke_color=MUT_COL, stroke_width=3, fill_color=NUC_COL, fill_opacity=0.95).move_to(kras_left.res.get_bottom() + DOWN * 0.03)
        soto_left = drug_chip("Sotorasib", size=24, pad_x=0.18, pad_y=0.12).move_to(kras_left.pocket_spot + LEFT * 0.28)
        bond_left = Line(soto_left.get_right(), thiol_left.get_left() + LEFT * 0.03, color=MUT_COL, stroke_width=6)
        cys_left = T("Cys 12", size=24, color=MUT_COL, weight=BOLD).move_to([-0.25, thiol_left.get_center()[1], 0])
        cys_left_ptr = Arrow(cys_left.get_left() + LEFT * 0.10, thiol_left.get_right() + RIGHT * 0.10, buff=0, color=MUT_COL, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        bond_left_lab = T("Covalent bond", size=26, color=DRUG_COL, weight=BOLD).move_to([-3.75, -2.30, 0])

        norm_kras = make_kras_shell([3.35, 0.35, 0], width=4.9, height=2.9, nucleotide="GTP", pocket_open=0.0, g12c=False, title="Normal Ras", title_size=24)
        no_cys = T("No Cys 12", size=26, color=TEXT).move_to([3.35, -1.30, 0])
        soto2 = drug_chip("Sotorasib", size=24, pad_x=0.18, pad_y=0.12).move_to([5.0, -2.30, 0])

        old_all = VGroup(kras, thiol_tip, cys_lab, cys_ptr, pocket_glow, soto, bond, bond_lab)
        new_left = VGroup(kras_left, thiol_left, soto_left, bond_left, cys_left, cys_left_ptr, bond_left_lab)
        self.play(FadeOut(old_all), run_time=0.40)
        self.play(FadeIn(new_left), FadeIn(norm_kras), FadeIn(no_cys), FadeIn(soto2), run_time=0.65)

        self.at("spares it")
        spare_lab = T("Spares normal Ras", size=28, color=DRUG_COL, weight=BOLD).move_to([3.35, 2.50, 0])
        self.play(
            soto2.animate.move_to([1.2, -2.30, 0]),
            FadeIn(spare_lab),
            run_time=2.3,
        )
        self.finish()


class S06OtherSites(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        pw = build_pathway(PATH_X)
        pulses = VGroup(*[make_signal_pill(a, SIG_COL, speed=1.15, phase=0.25 * i, w=0.34, h=0.16) for i, a in enumerate(pw.arrows)])

        soto = drug_chip("Sotorasib", size=24, pad_x=0.20, pad_y=0.13).move_to(pw.kras.get_right() + RIGHT * 1.25)
        cov_dot = Dot(pw.kras.get_right() + RIGHT * 0.12, radius=0.09, color=MUT_COL)
        cov_link = Line(pw.kras.get_right(), soto.get_left(), color=MUT_COL, stroke_width=5)
        cov_lab = T("Covalent: Cys 12", size=28, color=DRUG_COL, weight=BOLD).move_to([3.75, NODE_Y["K-Ras"], 0])
        cov_ptr = Arrow(cov_lab.get_left() + LEFT * 0.12, soto.get_right() + RIGHT * 0.10, buff=0, color=DRUG_COL, stroke_width=3, max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(pw), FadeIn(tag), run_time=0.9)
        self.add(pulses)
        pulses[1].clear_updaters()
        pulses[1].set_opacity(0)
        pulses[2].clear_updaters()
        pulses[2].set_opacity(0)
        self.play(
            FadeIn(soto), Create(cov_link), FadeIn(cov_dot), FadeIn(cov_lab), GrowArrow(cov_ptr),
            pw.arrows[1].animate.set_color(GREY).set_opacity(0.45),
            pw.arrows[2].animate.set_color(GREY).set_opacity(0.45),
            run_time=0.8,
        )

        self.at("antibodies grab")
        ab = make_antibody([PATH_X, 3.35, 0], scale=0.88)
        out_callout = T("Outside: antibody", size=28, color=DRUG_COL, weight=BOLD).move_to([3.75, 3.00, 0])
        out_ptr = Arrow(out_callout.get_left() + LEFT * 0.12, [PATH_X + 0.62, 3.00, 0], buff=0, color=DRUG_COL, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(ab), run_time=0.3)
        self.play(ab.animate.move_to([PATH_X, MEMB_Y + 0.88, 0]), FadeIn(out_callout), GrowArrow(out_ptr), run_time=0.9)
        pulses[0].clear_updaters()
        pulses[0].set_opacity(0)
        pw.arrows[0].set_color(GREY).set_opacity(0.45)

        self.at("allosteric inhibitors")
        atp_pill = RoundedRectangle(
            corner_radius=0.12, width=0.95, height=0.48,
            stroke_color=NUC_COL, stroke_width=2.5, fill_color=NUC_COL, fill_opacity=0.38,
        ).move_to(pw.mek.get_left() + LEFT * 0.68)
        atp_lab = T("ATP", size=24, color=NUC_COL, weight=BOLD).move_to(atp_pill)
        atp_grp = VGroup(atp_pill, atp_lab)

        allo = drug_chip("Allosteric", size=24, pad_x=0.20, pad_y=0.13).move_to([1.8, NODE_Y["MEK"], 0])
        self.play(FadeIn(atp_grp), FadeIn(allo), run_time=0.8)
        # Glide partway toward MEK while narrator describes side pocket beside active site
        self.play(allo.animate.move_to([0.35, NODE_Y["MEK"], 0]), run_time=2.5)

        self.at("lock kinases")
        beside_lab = T("Beside: side pocket", size=28, color=DRUG_COL, weight=BOLD).move_to([3.85, NODE_Y["MEK"], 0])
        beside_ptr = Arrow(beside_lab.get_left() + LEFT * 0.12, pw.mek.get_right() + RIGHT * 2.15, buff=0, color=DRUG_COL, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        self.play(allo.animate.move_to(pw.mek.get_right() + RIGHT * 1.15), FadeIn(beside_lab), GrowArrow(beside_ptr), run_time=0.85)

        self.at("without displacing")
        atp_stays = T("ATP stays in site", size=26, color=NUC_COL).move_to([-4.85, NODE_Y["MEK"] - 0.55, 0])
        pulses[3].clear_updaters()
        pulses[3].set_opacity(0)
        pw.arrows[3].set_color(GREY).set_opacity(0.45)
        self.play(
            pw.mek.box.animate.set_stroke(DRUG_COL, width=4),
            FadeIn(atp_stays),
            run_time=0.75,
        )
        self.finish()


def _predict_backdrop():
    """Shared pathway backdrop for s07_predict end and s08_pause."""
    pw = build_pathway(PATH_X)
    soto = drug_chip("Sotorasib", size=24, pad_x=0.20, pad_y=0.13).move_to(pw.kras.get_right() + RIGHT * 1.35)

    pw.rec.outer.set_stroke(MUT_COL, width=4).set_fill(MUT_COL, opacity=0.38)
    pw.rec.inner.set_stroke(MUT_COL, width=4).set_fill(MUT_COL, opacity=0.38)
    pw.arrows[0].set_color(MUT_COL)

    gtp_badge = RoundedRectangle(
        corner_radius=0.12, width=1.10, height=0.48,
        stroke_color=NUC_COL, stroke_width=2.5, fill_color=NUC_COL, fill_opacity=0.38,
    ).move_to([0.95, 1.56, 0])
    gtp_txt = T("GTP", size=24, color=NUC_COL, weight=BOLD).move_to(gtp_badge)
    gtp_tok = VGroup(gtp_badge, gtp_txt)
    reload_lab = T("Receptors reload GTP", size=28, color=MUT_COL, weight=BOLD).move_to([3.85, 0.94, 0])

    p_up = make_signal_pill(pw.arrows[0], NUC_COL, speed=1.45, phase=0.0, w=0.34, h=0.17)
    p_up2 = make_signal_pill(pw.arrows[0], MUT_COL, speed=1.45, phase=0.5, w=0.34, h=0.17)
    p_down = VGroup(*[make_signal_pill(a, SIG_COL, speed=1.25, phase=0.25 * i, w=0.32, h=0.15) for i, a in enumerate(pw.arrows[1:])])
    tag = scope_tag("schematic", color=TEXT)
    return VGroup(pw, soto, gtp_tok, reload_lab, p_up, p_up2, p_down, tag)


class S07Predict(SpokenScene):
    def construct(self):
        pw = build_pathway(PATH_X)
        soto = drug_chip("Sotorasib", size=24, pad_x=0.20, pad_y=0.13).move_to(pw.kras.get_right() + RIGHT * 1.35)
        tag = scope_tag("schematic", color=TEXT)

        self.play(FadeIn(pw), FadeIn(soto), FadeIn(tag), run_time=0.8)
        pulses = VGroup(*[make_signal_pill(a, SIG_COL, speed=1.25, phase=0.25 * i, w=0.34, h=0.16) for i, a in enumerate(pw.arrows)])
        self.add(pulses)

        # Actively cycle K-Ras GTP <-> GDP while Sotorasib probes and waits (stays clear of K-Ras outline!)
        gtp_ind = T("GTP", size=24, color=NUC_COL, weight=BOLD).move_to([-4.25, NODE_Y["K-Ras"], 0])
        self.play(
            FadeIn(gtp_ind),
            pw.kras.box.animate.set_stroke(NUC_COL, width=4).set_fill(NUC_COL, opacity=0.28),
            run_time=1.0,
        )
        self.play(
            pw.kras.box.animate.set_stroke(PROTEIN_COL, width=3).set_fill(PROTEIN_COL, opacity=0.30),
            soto.animate.shift(LEFT * 0.22),
            run_time=1.3,
        )
        self.play(
            soto.animate.shift(RIGHT * 0.22),
            pw.kras.box.animate.set_stroke(NUC_COL, width=4).set_fill(NUC_COL, opacity=0.28),
            run_time=1.3,
        )

        self.at("brief gdp state")
        gdp_tag = T("Brief GDP state only", size=28, color=GDP_COL, weight=BOLD).move_to([3.85, 0.94, 0])
        gdp_ind = T("GDP", size=24, color=GDP_COL, weight=BOLD).move_to([-4.25, NODE_Y["K-Ras"], 0])
        for p in pulses[1:]:
            p.suspend_updating()
        self.play(
            pw.kras.box.animate.set_stroke(GDP_COL, width=4).set_fill(GDP_COL, opacity=0.26),
            soto.animate.next_to(pw.kras, RIGHT, buff=0.10),
            *[p.animate.set_fill(opacity=0.15) for p in pulses[1:]],
            *[a.animate.set_color(GREY).set_opacity(0.45) for a in pw.arrows[1:]],
            swap(gtp_ind, gdp_ind, run_time=0.5),
            FadeIn(gdp_tag),
            run_time=0.8,
        )

        self.at("pause and predict")
        q = question_card("What if receptors reload Ras with GTP?")
        self.play(FadeIn(q.question, shift=UP * 0.15), run_time=0.6)

        self.at("wake up and reload")
        gtp_badge = RoundedRectangle(
            corner_radius=0.12, width=1.10, height=0.48,
            stroke_color=NUC_COL, stroke_width=2.5, fill_color=NUC_COL, fill_opacity=0.38,
        ).move_to([0.95, 1.56, 0])
        gtp_txt = T("GTP", size=24, color=NUC_COL, weight=BOLD).move_to(gtp_badge)
        gtp_tok = VGroup(gtp_badge, gtp_txt)
        reload_lab = T("Receptors reload GTP", size=28, color=MUT_COL, weight=BOLD).move_to([3.85, 0.94, 0])

        pulses[0].clear_updaters()
        pulses[0].set_opacity(0)
        p_up = make_signal_pill(pw.arrows[0], NUC_COL, speed=1.45, phase=0.0, w=0.34, h=0.17)
        p_up2 = make_signal_pill(pw.arrows[0], MUT_COL, speed=1.45, phase=0.5, w=0.34, h=0.17)
        self.add(p_up, p_up2)
        for p in pulses[1:]:
            p.set_fill(opacity=0.95)
            p.resume_updating()
        self.play(
            FadeOut(gdp_ind),
            soto.animate.move_to(pw.kras.get_right() + RIGHT * 1.35),
            *[a.animate.set_color(SIG_COL).set_opacity(1.0) for a in pw.arrows[1:]],
            pw.rec.outer.animate.set_stroke(MUT_COL, width=4).set_fill(MUT_COL, opacity=0.38),
            pw.rec.inner.animate.set_stroke(MUT_COL, width=4).set_fill(MUT_COL, opacity=0.38),
            pw.arrows[0].animate.set_color(MUT_COL),
            pw.kras.box.animate.set_stroke(PROTEIN_COL, width=3).set_fill(PROTEIN_COL, opacity=0.30),
            swap(gdp_tag, reload_lab, run_time=0.6),
            FadeIn(gtp_tok, shift=DOWN * 0.25),
            run_time=1.0,
        )
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "What if receptors reload Ras with GTP?"
    SECONDS = 4.5
    RING_AT = (5.9, -2.25, 0)

    def backdrop(self):
        return _predict_backdrop()


class S09NetworkPushback(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        pw = build_pathway(PATH_X)
        pw.rec.outer.set_stroke(MUT_COL, width=4).set_fill(MUT_COL, opacity=0.38)
        pw.rec.inner.set_stroke(MUT_COL, width=4).set_fill(MUT_COL, opacity=0.38)
        pw.arrows[0].set_color(MUT_COL)
        soto = drug_chip("Sotorasib", size=24, pad_x=0.20, pad_y=0.13).move_to(pw.kras.get_right() + RIGHT * 1.25)

        pool_x = 4.05
        pool_w = 2.90
        pool_title = T("GDP pool", size=28, color=GDP_COL, weight=BOLD).move_to([pool_x, 1.35, 0])
        pool_frame = RoundedRectangle(
            corner_radius=0.12, width=pool_w, height=0.62,
            stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=0.9,
        ).move_to([pool_x, 0.72, 0])
        pool_tracker = ValueTracker(0.75)
        pool_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.14, (pool_w - 0.10) * pool_tracker.get_value()), height=0.52,
                stroke_width=0, fill_color=GDP_COL, fill_opacity=0.84,
            ).move_to([pool_frame.get_left()[0] + 0.05 + max(0.14, (pool_w - 0.10) * pool_tracker.get_value()) / 2, 0.72, 0])
        )
        gtp_flood_lab = T("Fewer Ras trapped", size=28, color=MUT_COL, weight=BOLD).move_to([pool_x, -0.05, 0])
        self.add(pw, soto, tag, pool_title, pool_frame, pool_fill)
        p_up = make_signal_pill(pw.arrows[0], NUC_COL, speed=1.55, phase=0.0, w=0.34, h=0.17)
        p_down = VGroup(*[make_signal_pill(a, SIG_COL, speed=1.25, phase=0.25 * i, w=0.32, h=0.15) for i, a in enumerate(pw.arrows[1:])])
        self.add(p_up, p_down)

        self.at("shrinks the gdp pool")
        self.play(
            pool_tracker.animate.set_value(0.12),
            pw.kras.box.animate.set_stroke(NUC_COL, width=4),
            soto.animate.shift(RIGHT * 0.28),
            FadeIn(gtp_flood_lab),
            run_time=2.5,
        )
        # Keep K-Ras GTP surge active until Beat 2
        self.play(soto.animate.shift(RIGHT * 0.12), run_time=1.0)

        # Beat 2: Negative feedback relieved on MEK block
        self.at("networks push back")
        p_up.clear_updaters()
        self.remove(p_up)
        self.play(
            FadeOut(pool_title), FadeOut(pool_frame), FadeOut(pool_fill), FadeOut(gtp_flood_lab), FadeOut(soto),
            pw.rec.outer.animate.set_stroke(PROTEIN_COL, width=3).set_fill(PROTEIN_COL, opacity=0.34),
            pw.rec.inner.animate.set_stroke(PROTEIN_COL, width=3).set_fill(PROTEIN_COL, opacity=0.30),
            pw.kras.box.animate.set_stroke(PROTEIN_COL, width=3),
            pw.arrows[0].animate.set_color(SIG_COL),
            run_time=0.6,
        )

        brake_x = -3.95
        brake_line = DashedVMobject(
            VMobject().set_points_as_corners([
                pw.erk.get_left() + LEFT * 0.08,
                [brake_x, NODE_Y["ERK"], 0],
                [brake_x, NODE_Y["K-Ras"], 0],
                pw.kras.get_left() + LEFT * 0.12,
            ]),
            num_dashes=26, color=TEXT, stroke_width=3,
        )
        brake_bar = Line(
            [pw.kras.get_left()[0] - 0.12, NODE_Y["K-Ras"] - 0.18, 0],
            [pw.kras.get_left()[0] - 0.12, NODE_Y["K-Ras"] + 0.18, 0],
            color=TEXT, stroke_width=4,
        )
        fb_lab = T("Negative\nfeedback", size=24, color=TEXT).move_to([-5.15, -0.50, 0])

        mb = drug_chip("MEK block", size=24, pad_x=0.20, pad_y=0.13).move_to(pw.mek.get_right() + RIGHT * 1.25)
        self.play(Create(brake_line), Create(brake_bar), run_time=0.7)

        self.at("block mek")
        p_down[2].clear_updaters()
        p_down[2].set_opacity(0)
        self.play(
            FadeIn(mb),
            pw.arrows[3].animate.set_color(GREY).set_opacity(0.45),
            run_time=0.6,
        )

        self.at("drops its")
        self.play(
            brake_line.animate.set_stroke(GREY, opacity=0.35),
            brake_bar.animate.set_stroke(GREY, opacity=0.35),
            run_time=0.75,
        )

        self.at("called negative feedback")
        self.play(FadeIn(fb_lab), run_time=0.5)

        self.at("upstream steps push harder")
        rel_lab = T("Feedback relieved", size=28, color=MUT_COL, weight=BOLD).move_to([2.6, 0.94, 0])
        flare_rec = pw.rec.inner.animate.set_stroke(MUT_COL, width=5).set_fill(MUT_COL, opacity=0.45)
        flare_ras = pw.kras.box.animate.set_stroke(MUT_COL, width=5).set_fill(MUT_COL, opacity=0.42)
        burst = VGroup(
            Line([-4.05, NODE_Y["K-Ras"] + 0.22, 0], [-3.70, NODE_Y["K-Ras"] + 0.12, 0], color=MUT_COL, stroke_width=4),
            Line([-4.05, NODE_Y["K-Ras"] - 0.22, 0], [-3.70, NODE_Y["K-Ras"] - 0.12, 0], color=MUT_COL, stroke_width=4),
            Line([-3.80, NODE_Y["Receptor"] - 0.35, 0], [-3.45, NODE_Y["Receptor"] - 0.42, 0], color=MUT_COL, stroke_width=4),
        )
        self.play(FadeOut(brake_line), FadeOut(brake_bar), FadeOut(fb_lab), run_time=0.35)
        self.play(flare_rec, flare_ras, FadeIn(rel_lab), Create(burst), run_time=0.75)
        self.play(burst.animate.scale(1.18), run_time=0.7)

        # Beat 3: Blocked EGFR + 3 amplified MET receptors bypassing
        self.at("amplify another receptor")
        for pd in p_down:
            pd.clear_updaters()
        self.remove(p_down)
        self.play(
            FadeOut(mb), FadeOut(rel_lab), FadeOut(burst),
            pw.rec.outer.animate.set_stroke(PROTEIN_COL, width=3).set_fill(PROTEIN_COL, opacity=0.34),
            pw.rec.inner.animate.set_stroke(PROTEIN_COL, width=3).set_fill(PROTEIN_COL, opacity=0.30),
            pw.kras.box.animate.set_stroke(PROTEIN_COL, width=3).set_fill(PROTEIN_COL, opacity=0.30),
            pw.arrows[3].animate.set_color(SIG_COL).set_opacity(1.0),
            run_time=0.45,
        )
        egfr_lab = T("EGFR", size=24, color=TEXT, weight=BOLD).move_to(pw.rec.inner)
        egfr_blk = make_antibody([PATH_X, 0, 0], scale=0.65).next_to(pw.rec.outer, UP, buff=0.06)

        mets = VGroup()
        for mx in (0.40, 1.90, 3.40):
            mo = RoundedRectangle(corner_radius=0.12, width=0.76, height=0.42, stroke_color=MUT_COL, stroke_width=3, fill_color=MUT_COL, fill_opacity=0.48).move_to([mx, MEMB_Y + 0.38, 0])
            ms = Rectangle(width=0.28, height=0.36, stroke_color=MUT_COL, stroke_width=2, fill_color=MUT_COL, fill_opacity=0.42).move_to([mx, MEMB_Y, 0])
            mi = RoundedRectangle(corner_radius=0.10, width=0.94, height=0.40, stroke_color=MUT_COL, stroke_width=3, fill_color=MUT_COL, fill_opacity=0.42).move_to([mx, MEMB_Y - 0.38, 0])
            ml = T("MET", size=24, color=TEXT, weight=BOLD).move_to(mi)
            mets.add(VGroup(ms, mo, mi, ml))

        self.play(
            swap(pw.rec.label, egfr_lab, run_time=0.35),
            FadeIn(egfr_blk),
            pw.arrows[0].animate.set_color(GREY).set_opacity(0.45),
            FadeIn(mets, lag_ratio=0.18),
            run_time=0.9,
        )

        self.at("bypass the block")
        bypass_arr = CurvedArrow([1.90, MEMB_Y - 0.62, 0], pw.kras.get_right() + RIGHT * 0.1, angle=-0.35, color=SIG_COL, stroke_width=5)
        bypass_lab = T("Bypass signal", size=28, color=SIG_COL, weight=BOLD).move_to([3.0, 0.25, 0])
        p_byp = make_signal_pill(bypass_arr, SIG_COL, speed=1.4, phase=0.0, w=0.34, h=0.17)
        p_down2 = VGroup(*[make_signal_pill(a, SIG_COL, speed=1.4, phase=0.2 * i, w=0.32, h=0.15) for i, a in enumerate(pw.arrows[1:])])
        self.play(Create(bypass_arr), FadeIn(bypass_lab), run_time=0.65)
        self.add(p_byp, p_down2)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        pw = build_pathway(PATH_X)

        ab = make_antibody([PATH_X, MEMB_Y + 0.88, 0], scale=0.88)
        out_lab = T("Outer face", size=28, color=DRUG_COL, weight=BOLD).move_to([3.75, 3.00, 0])
        out_ptr = Arrow(out_lab.get_left() + LEFT * 0.12, [PATH_X + 0.62, 3.00, 0], buff=0, color=DRUG_COL, stroke_width=3, max_tip_length_to_length_ratio=0.2)

        soto = drug_chip("Sotorasib", size=24, pad_x=0.20, pad_y=0.13).move_to(pw.kras.get_right() + RIGHT * 1.25)
        cov_link = Line(pw.kras.get_right(), soto.get_left(), color=MUT_COL, stroke_width=5)
        cov_lab = T("Covalent bond", size=28, color=DRUG_COL, weight=BOLD).move_to([3.75, NODE_Y["K-Ras"], 0])
        cov_ptr = Arrow(cov_lab.get_left() + LEFT * 0.12, soto.get_right() + RIGHT * 0.10, buff=0, color=DRUG_COL, stroke_width=3, max_tip_length_to_length_ratio=0.2)

        allo = drug_chip("Allosteric", size=24, pad_x=0.20, pad_y=0.13).move_to(pw.mek.get_right() + RIGHT * 1.15)
        side_lab = T("Side pocket", size=28, color=DRUG_COL, weight=BOLD).move_to([3.75, NODE_Y["MEK"], 0])
        side_ptr = Arrow(side_lab.get_left() + LEFT * 0.12, allo.get_right() + RIGHT * 0.10, buff=0, color=DRUG_COL, stroke_width=3, max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(pw), FadeIn(tag), run_time=0.8)
        self.play(FadeIn(ab), FadeIn(soto), Create(cov_link), FadeIn(allo), run_time=0.8)

        self.at("side pockets")
        self.play(FadeIn(side_lab), GrowArrow(side_ptr), run_time=0.45)

        self.at("outer faces")
        self.play(FadeIn(out_lab), GrowArrow(out_ptr), run_time=0.55)

        self.at("covalent bonds")
        self.play(FadeIn(cov_lab), GrowArrow(cov_ptr), run_time=0.6)

        self.play(
            pw.kras.box.animate.set_stroke(DRUG_COL, width=4),
            pw.mek.box.animate.set_stroke(DRUG_COL, width=4),
            pw.rec.outer.animate.set_stroke(DRUG_COL, width=4),
            run_time=1.3,
        )

        self.at("even then")
        fb_x = pw.mek.get_left()[0] - 0.35
        fb_arr = CurvedArrow([fb_x, NODE_Y["ERK"], 0], [fb_x, MEMB_Y - 0.44, 0], angle=-0.60, color=MUT_COL, stroke_width=4.5)
        fb_lab = T("Circuit\nripples", size=28, color=MUT_COL, weight=BOLD).move_to([-5.35, 0.0, 0])
        p_fb1 = make_signal_pill(fb_arr, MUT_COL, speed=0.90, phase=0.0, w=0.34, h=0.17)
        p_fb2 = make_signal_pill(fb_arr, MUT_COL, speed=0.90, phase=0.5, w=0.34, h=0.17)
        p_dn = VGroup(*[make_signal_pill(a, MUT_COL, speed=1.25, phase=0.25 * i, w=0.32, h=0.15) for i, a in enumerate(pw.arrows)])
        self.play(Create(fb_arr), FadeIn(fb_lab), run_time=1.0)
        self.add(p_fb1, p_fb2, p_dn)

        self.at("ripples through")
        for nd in (pw.rec.inner, pw.kras.box, pw.raf.box, pw.mek.box, pw.erk.box):
            self.play(nd.animate.set_fill(MUT_COL, opacity=0.40), run_time=0.26)
            self.play(nd.animate.set_fill(PROTEIN_COL, opacity=0.30), run_time=0.22)
        self.finish()


class S11End(EndCard):
    LINE = "New sites and covalent bonds bypass competition, yet networks push back."
