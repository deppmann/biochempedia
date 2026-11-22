"""Selectivity and Escape at One Pocket — animation for "Drugs Against a Part".

COLOUR MAP (one colour per concept across the whole film):
    KINASE_BLUE = "#4A90D9"   # slate-blue: protein kinases, ABL / BCR-ABL, conserved ATP pockets
    ATP_GOLD    = "#E8A838"   # amber-gold: ATP molecules and the transferred end phosphate
    DRUG_TEAL   = "#2EC4B6"   # bright teal: targeted small-molecule drugs (imatinib, ponatinib)
    SIGNAL_GRN  = "#4CAF50"   # emerald-green: active catalysis / downstream cell-growth signal
    MUTANT_RED  = "#E05A47"   # coral-red: gatekeeper resistance change (Ile 315) / drug clash
    TEXT        = "#E8EAF0"   # primary crisp labels
    GREY        = "#8B93A1"   # muted inactive signals, schematic tag, secondary markers

ONE CARRIED PICTURE:
    A schematic two-lobed kinase pocket (slate-blue) with an ATP site at the mouth and a deeper
    back alcove guarded by residue 315 on the pocket wall, interacting with amber-gold ATP,
    teal drugs, and an emerald-green catalysis/growth arrow. Outward scenes (s01-s04, s10) show
    collections or cells built from this pocket; inward scenes (s05-s09) zoom into its cross-section.

WHAT CHANGES PER SPOKEN SCENE (and what drives it):
    s01_hook          : Grid of schematic kinase pockets expands (12 -> 40) as a ValueTracker
                        count advances to ~500; computed ATP trajectories dock into every cleft
                        while one teal drug probes the conserved pocket and meets a red clash.
    s02_shared_pocket : Three active kinases transfer computed phosphate-bead arcs from ATP onto
                        target proteins, fold their clefts via a tracker into identical working
                        shapes, and are all fitted by the teal drug.
    s03_idle_shape    : The same three kinases highlight matching working shapes, then morph via an
                        idle-shape tracker into three distinct switched-off shapes; imatinib glides
                        into ABL and rebounds off unrelated pockets while the short-list ledger builds.
    s04_dependence    : Normal cell (ABL, PDGFR, KIT) sits beside a CML cell whose BCR and ABL
                        chips fuse into BCR-ABL driving a green growth arrow; imatinib enters both,
                        shrinking the CML cell while the normal cell pauses intact.
    s05_relapse       : Zooms into the rebounding CML cell's ABL pocket; a blood-derived codon
                        strip flips ACT -> ATT as a bulk tracker swells Thr 315 into protruding
                        coral-red Ile 315 beside imatinib.
    s06_gatekeeper    : Cross-section of the pocket: Thr 315 lets imatinib reach the back alcove
                        and form a hydrogen bond; morphing to Ile 315 snaps the bond and pushes
                        imatinib out while ATP glides cleanly into the ATP site and fires signal.
    s07_predict       : Same pocket cross-section: imatinib repeatedly approaches and rebounds off
                        Ile 315 while ATP cycles phosphate along the active green signal arrow,
                        ending with the predict question card in the bottom band.
    s09_ponatinib     : Bulky imatinib clashes against Ile 315, morphs via a neck-width tracker
                        into ponatinib with a slim central bridge, ejects ATP and glides cleanly
                        past Ile 315 into the alcove, dimming the green signal arrow to grey.
    s10_rule          : Pulls back into paired panels showing left (idle-shape ABL + imatinib and
                        target dependence) and right (Ile 315 escape -> slim-bridge ponatinib).
"""
from bp_parts import *

KINASE_BLUE = "#4A90D9"
ATP_GOLD = "#E8A838"
DRUG_TEAL = "#2EC4B6"
SIGNAL_GRN = "#4CAF50"
MUTANT_RED = "#E05A47"


# ------------------------------------------------------------------ shared geometry helpers
def _mini_kinase(cleft_gap=0.22, lobe_shift=0.0, width=1.1, height=0.82, color=KINASE_BLUE, fill_op=0.28):
    """A compact schematic two-lobed kinase block with a central ATP cleft."""
    top_h = (height - cleft_gap) / 2
    bot_h = (height - cleft_gap) / 2
    top = RoundedRectangle(
        corner_radius=0.10, width=width, height=top_h,
        stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill_op,
    ).shift(UP * (cleft_gap / 2 + top_h / 2) + RIGHT * lobe_shift)
    bot = RoundedRectangle(
        corner_radius=0.10, width=width, height=bot_h,
        stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill_op,
    ).shift(DOWN * (cleft_gap / 2 + bot_h / 2))
    hinge = Rectangle(
        width=0.16, height=cleft_gap + 0.08,
        stroke_color=color, stroke_width=2.0, fill_color=color, fill_opacity=fill_op + 0.12,
    ).move_to([width / 2 - 0.10, 0, 0])
    return VGroup(top, bot, hinge)


def _atp_token(scale=1.0, with_label=False):
    """Amber-gold ATP block with a distinct glowing end-phosphate bead."""
    body = RoundedRectangle(
        corner_radius=0.10 * scale, width=0.58 * scale, height=0.34 * scale,
        stroke_color=ATP_GOLD, stroke_width=2.5, fill_color=ATP_GOLD, fill_opacity=0.32,
    )
    phos = Dot(radius=0.11 * scale, color=ATP_GOLD, stroke_color=TEXT, stroke_width=2.0)
    phos.next_to(body, RIGHT, buff=-0.03 * scale)
    g = VGroup(body, phos)
    g.body = body
    g.phos = phos
    if with_label:
        lbl = T("ATP", size=24, color=ATP_GOLD)
        lbl.next_to(g, UP, buff=0.14)
        g.add(lbl)
        g.lbl = lbl
    return g


def _drug_block(neck_h=0.52, width=1.65, color=DRUG_TEAL, fill_op=0.32):
    """Schematic kinase drug: left grip (ATP site), central bridge, right grip (back alcove)."""
    left_pad = RoundedRectangle(
        corner_radius=0.12, width=0.52, height=0.72,
        stroke_color=color, stroke_width=2.8, fill_color=color, fill_opacity=fill_op,
    ).shift(LEFT * (width / 2 - 0.26))
    right_pad = RoundedRectangle(
        corner_radius=0.12, width=0.48, height=0.68,
        stroke_color=color, stroke_width=2.8, fill_color=color, fill_opacity=fill_op,
    ).shift(RIGHT * (width / 2 - 0.24))
    bridge = RoundedRectangle(
        corner_radius=min(0.08, neck_h / 2), width=width - 0.84, height=neck_h,
        stroke_color=color, stroke_width=2.6, fill_color=color, fill_opacity=fill_op + 0.12,
    )
    g = VGroup(left_pad, bridge, right_pad)
    g.left_pad = left_pad
    g.bridge = bridge
    g.right_pad = right_pad
    return g


def _chamfer_box(w, h, r=0.14):
    """8-vertex chamfered Polygon (not a panel class) for interior pocket zones."""
    hw, hh = w / 2, h / 2
    pts = [
        [-hw + r, hh, 0], [hw - r, hh, 0],
        [hw, hh - r, 0], [hw, -hh + r, 0],
        [hw - r, -hh, 0], [-hw + r, -hh, 0],
        [-hw, -hh + r, 0], [-hw, hh - r, 0],
    ]
    return pts


def _pocket_cross_section(bulk=0.0, center=ORIGIN, scale=1.0):
    """Cross-section of the slate-blue ABL pocket with ATP site (left), neck gatekeeper 315, and back alcove (right)."""
    upper_pts = [
        [-3.2, 1.75, 0], [3.55, 1.75, 0], [3.55, 0.0, 0],
        [3.10, 0.0, 0], [3.10, 0.92, 0], [0.95, 0.92, 0],
        [0.85, 1.05, 0], [-0.35, 1.05, 0], [-0.55, 1.15, 0],
        [-3.2, 1.15, 0],
    ]
    lower_pts = [
        [-3.2, -1.75, 0], [3.55, -1.75, 0], [3.55, 0.0, 0],
        [3.10, 0.0, 0], [3.10, -0.92, 0], [0.95, -0.92, 0],
        [0.85, -1.05, 0], [-0.35, -1.05, 0], [-0.55, -1.15, 0],
        [-3.2, -1.15, 0],
    ]
    upper = Polygon(*upper_pts, stroke_color=KINASE_BLUE, stroke_width=3.2,
                    fill_color=KINASE_BLUE, fill_opacity=0.25)
    lower = Polygon(*lower_pts, stroke_color=KINASE_BLUE, stroke_width=3.2,
                    fill_color=KINASE_BLUE, fill_opacity=0.25)

    atp_zone = Polygon(
        *_chamfer_box(2.45, 1.85, 0.14),
        stroke_color=ATP_GOLD, stroke_width=1.8, fill_color=ATP_GOLD, fill_opacity=0.06,
    ).move_to([-1.85, 0.0, 0])
    alcove_zone = Polygon(
        *_chamfer_box(2.05, 1.68, 0.14),
        stroke_color=KINASE_BLUE, stroke_width=2.0, fill_color=KINASE_BLUE, fill_opacity=0.10,
    ).move_to([2.02, 0.0, 0])

    # Residue 315 gatekeeper nub/block on top neck wall
    w = 0.42 + 0.62 * bulk
    h = 0.42 + 0.68 * bulk
    col = interpolate_color(ManimColor(KINASE_BLUE), ManimColor(MUTANT_RED), bulk)
    gk = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        stroke_color=col, stroke_width=3.0, fill_color=col, fill_opacity=0.45 + 0.25 * bulk,
    ).move_to([0.28, 1.05 - h / 2, 0])

    g = VGroup(atp_zone, alcove_zone, upper, lower, gk)
    g.scale(scale).move_to(center)
    g.upper = upper
    g.lower = lower
    g.atp_zone = atp_zone
    g.alcove_zone = alcove_zone
    g.gk = gk
    return g


def _build_315_backdrop(center=ORIGIN, scale=0.95):
    """Canonical mutant Ile 315 pocket state with ATP docked and active signal arrow (used by s06 end, s07, s08)."""
    pocket = _pocket_cross_section(bulk=1.0, center=center, scale=scale)
    atp = _atp_token(scale=1.65 * scale)
    atp.move_to(pocket.atp_zone.get_center() + LEFT * 0.12 * scale)
    atp_lbl = T("ATP", size=24, color=ATP_GOLD).next_to(atp, DOWN, buff=0.16)

    ile_lbl = T("Ile 315", size=26, color=MUTANT_RED).next_to(pocket.upper, UP, buff=0.22).shift(RIGHT * 0.35 * scale)
    ile_ptr = Arrow(
        ile_lbl.get_bottom() + DOWN * 0.04,
        pocket.gk.get_top() + UP * 0.06,
        buff=0, stroke_width=2.8, color=MUTANT_RED, max_tip_length_to_length_ratio=0.25,
    )
    ile_ptr.layout_ok = True

    alc_lbl = T("Back alcove", size=24, color=KINASE_BLUE).next_to(pocket, RIGHT, buff=0.30).shift(UP * 0.15)
    alc_ptr = Arrow(
        alc_lbl.get_left() + LEFT * 0.04,
        pocket.alcove_zone.get_right() + RIGHT * 0.04 + UP * 0.15,
        buff=0, stroke_width=2.2, color=KINASE_BLUE, max_tip_length_to_length_ratio=0.20,
    )
    alc_ptr.layout_ok = True
    sig_start = pocket.lower.get_bottom() + DOWN * 0.12 + LEFT * 1.4 * scale
    sig_end = sig_start + DOWN * 0.85
    sig_arrow = Arrow(sig_start, sig_end, buff=0, stroke_width=6.0, color=SIGNAL_GRN,
                      max_tip_length_to_length_ratio=0.32)
    sig_lbl = T("catalysis intact", size=26, color=SIGNAL_GRN).next_to(sig_arrow, RIGHT, buff=0.22)

    drug = _drug_block(neck_h=0.52 * scale, width=2.2 * scale, color=DRUG_TEAL)
    drug.move_to(pocket.get_left() + LEFT * 1.65 * scale + UP * 0.05 * scale)
    drug_lbl = T("imatinib", size=26, color=DRUG_TEAL).next_to(drug, UP, buff=0.18)

    g = VGroup(pocket, atp, atp_lbl, ile_lbl, ile_ptr, alc_lbl, alc_ptr, sig_arrow, sig_lbl, drug, drug_lbl)
    g.pocket = pocket
    g.atp = atp
    g.atp_lbl = atp_lbl
    g.ile_lbl = ile_lbl
    g.ile_ptr = ile_ptr
    g.alc_lbl = alc_lbl
    g.alc_ptr = alc_ptr
    g.sig_arrow = sig_arrow
    g.sig_lbl = sig_lbl
    g.drug = drug
    g.drug_lbl = drug_lbl
    return g


def _imatinib_approach_gk(
    scene, scene_g, step_times=(0.20, 0.20, 0.20, 0.25, 0.25, 0.20, 0.20, 0.20),
    on_peak=None, extra_in=(), extra_out=(),
):
    """Move ATP out the open pocket mouth while imatinib approaches Ile 315 (stopping at gk.get_left()), then return."""
    pocket = scene_g.pocket
    atp = scene_g.atp
    atp_lbl = scene_g.atp_lbl
    drug = scene_g.drug
    drug_lbl = scene_g.drug_lbl

    atp_orig = atp.get_center().copy()
    atp_lbl_orig = atp_lbl.get_center().copy()
    drug_orig = drug.get_center().copy()
    drug_lbl_orig = drug_lbl.get_center().copy()

    pc = pocket.get_center()
    atp_mid = np.array([pocket.get_left()[0] + 0.05, pc[1], 0.0])
    atp_out_hi = np.array([pocket.get_left()[0] - 1.40, pc[1] - 0.12, 0.0])
    atp_out_lo = np.array([pocket.get_left()[0] - 1.40, pc[1] - 0.72, 0.0])

    hit_y = pc[1] + 0.02
    hit_x = pocket.gk.get_left()[0] - drug.width / 2 - 0.02
    drug_lift = np.array([drug_orig[0], pc[1] + 0.68, 0.0])
    drug_lbl_lift = drug_lbl_orig + (drug_lift - drug_orig)
    drug_ready = np.array([drug_orig[0], hit_y, 0.0])
    drug_lbl_ready = np.array([drug_orig[0], hit_y + drug.height / 2 + 0.06 + drug_lbl.height / 2, 0.0])
    drug_hit = np.array([hit_x, hit_y, 0.0])
    drug_lbl_hit = np.array([hit_x - 0.14, drug_lbl_ready[1], 0.0])

    t1, t2a, t2b, t2c, t3a, t3b, t3c, t4 = step_times
    scene.play(
        drug.animate.move_to(drug_lift),
        drug_lbl.animate.move_to(drug_lbl_lift),
        atp.animate.move_to(atp_mid),
        FadeOut(atp_lbl),
        run_time=t1,
    )
    scene.play(
        atp.animate.move_to(atp_out_hi),
        run_time=t2a,
    )
    atp_lbl.move_to(atp_lbl_orig + (atp_out_lo - atp_orig))
    scene.play(
        atp.animate.move_to(atp_out_lo),
        FadeIn(atp_lbl),
        drug.animate.move_to(drug_ready),
        drug_lbl.animate.move_to(drug_lbl_ready),
        run_time=t2b,
    )
    scene.play(
        drug.animate.move_to(drug_hit),
        drug_lbl.animate.move_to(drug_lbl_hit),
        *extra_in,
        run_time=t2c,
    )
    if on_peak is not None:
        on_peak()
    scene.play(
        drug.animate.move_to(drug_ready),
        drug_lbl.animate.move_to(drug_lbl_ready),
        *extra_out,
        run_time=t3a,
    )
    scene.play(
        drug.animate.move_to(drug_lift),
        drug_lbl.animate.move_to(drug_lbl_lift),
        atp.animate.move_to(atp_out_hi),
        FadeOut(atp_lbl),
        run_time=t3b,
    )
    scene.play(
        atp.animate.move_to(atp_mid),
        run_time=t3c,
    )
    atp_lbl.move_to(atp_lbl_orig)
    scene.play(
        drug.animate.move_to(drug_orig),
        drug_lbl.animate.move_to(drug_lbl_orig),
        atp.animate.move_to(atp_orig),
        FadeIn(atp_lbl),
        run_time=t4,
    )


# ------------------------------------------------------------------ Scene 0: Title
class S00Title(TitleCard):
    LESSON = "Drugs Against a Part"
    TITLE = "Selectivity and Escape at One Pocket"


# ------------------------------------------------------------------ Scene 1: Hook
class S01Hook(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        heading = T("About 500 human kinases", size=34, color=TEXT).move_to([0, 3.28, 0])
        tag = scope_tag("schematic")

        cols0, rows0 = 4, 3
        grid0 = VGroup(*[
            _mini_kinase(cleft_gap=0.24, width=1.45, height=1.05, fill_op=0.30)
            for _ in range(cols0 * rows0)
        ]).arrange_in_grid(rows=rows0, cols=cols0, buff=(0.45, 0.35)).move_to([0, -0.25, 0])

        cols1, rows1 = 8, 5
        grid1 = VGroup(*[
            _mini_kinase(cleft_gap=0.16, width=0.98, height=0.70, fill_op=0.26)
            for _ in range(cols1 * rows1)
        ]).arrange_in_grid(rows=rows1, cols=cols1, buff=(0.24, 0.18)).move_to([0, -0.52, 0])

        count_tr = ValueTracker(12.0)
        count_readout = counter("kinases: ~{:.0f}", count_tr, at=[-4.2, 2.68, 0], size=28, color=KINASE_BLUE)

        self.play(FadeIn(heading), FadeIn(grid0), FadeIn(count_readout), FadeIn(tag), run_time=0.2)
        self.play(
            ReplacementTransform(grid0, grid1),
            count_tr.animate.set_value(500.0),
            run_time=0.55,
        )

        self.at("nearly the same")
        atp_tokens = VGroup()
        atp_anims = []
        for idx, k in enumerate(grid1):
            tok = _atp_token(scale=0.58)
            start_offset = np.array([rng.uniform(-1.1, 1.1), rng.uniform(0.5, 1.4), 0.0])
            target_pos = k.get_center() + LEFT * 0.04
            tok.move_to(target_pos + start_offset)
            tok.set_opacity(0.0)
            atp_tokens.add(tok)
            atp_anims.append(tok.animate(lag_ratio=0.02).move_to(target_pos).set_opacity(1.0))

        atp_lbl = T("ATP in every pocket", size=28, color=ATP_GOLD).move_to([3.7, 2.68, 0])
        self.play(FadeIn(atp_lbl), AnimationGroup(*atp_anims, lag_ratio=0.025), run_time=2.5)

        self.at("one small drug")
        target_k = grid1[2 * cols1 + 3]
        target_ring = SurroundingRectangle(target_k, corner_radius=0.14, color=DRUG_TEAL, stroke_width=3.5, buff=0.08)
        drug = _drug_block(neck_h=0.42, width=1.9, color=DRUG_TEAL, fill_op=0.50).scale(0.50)
        drug.move_to([0.0, 1.98, 0])
        drug_lbl = T("one small drug", size=28, color=DRUG_TEAL).move_to([0.0, 2.68, 0])
        q_lbl = T("shut down just one?", size=28, color=DRUG_TEAL).move_to([0, -3.05, 0])

        self.play(FadeIn(drug), FadeIn(drug_lbl), Create(target_ring), FadeIn(q_lbl), run_time=0.9)
        probe_pts = [
            grid1[1 * cols1 + 2].get_center() + UP * 0.50,
            grid1[2 * cols1 + 5].get_center() + UP * 0.50,
            target_k.get_center() + UP * 0.48,
        ]
        for pt in probe_pts:
            self.play(drug.animate.move_to(pt), run_time=1.15)

        self.at("tumor fights back")
        escape_lbl = T("or tumour fights back?", size=28, color=MUTANT_RED).move_to([0, -3.05, 0])
        self.play(
            target_ring.animate.set_color(MUTANT_RED),
            target_k.animate.set_color(MUTANT_RED),
            drug.animate.shift(UP * 0.72),
            swap(q_lbl, escape_lbl, run_time=0.6),
            run_time=1.4,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 2: Shared Pocket
class S02SharedPocket(SpokenScene):
    def construct(self):
        heading = T("Active pockets fold into one working shape", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        xs = [-3.9, 0.0, 3.9]
        init_gaps = [0.64, 0.44, 0.72]
        init_shifts = [-0.14, 0.14, -0.10]

        fold_tr = ValueTracker(0.0)
        kinases = VGroup()
        for idx, x in enumerate(xs):
            def make_k(i=idx, cx=x):
                t = fold_tr.get_value()
                gap = init_gaps[i] + (0.50 - init_gaps[i]) * t
                sh = init_shifts[i] * (1.0 - t)
                return _mini_kinase(cleft_gap=gap, lobe_shift=sh, width=2.45, height=2.25, fill_op=0.28).move_to([cx, 0.35, 0])
            kinases.add(always_redraw(make_k))

        atps = VGroup(*[_atp_token(scale=1.05).move_to([x - 0.18, 0.35, 0]) for x in xs])
        targets = VGroup(*[
            RoundedRectangle(
                corner_radius=0.14, width=2.2, height=0.72,
                stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.10,
            ).move_to([x, -1.80, 0])
            for x in xs
        ])
        target_lbl = T("target protein", size=24, color=TEXT).move_to(targets[0])
        atp_lbl = T("ATP", size=26, color=ATP_GOLD).next_to(kinases[0], LEFT, buff=0.22)

        self.play(FadeIn(heading), FadeIn(kinases), FadeIn(atps), FadeIn(targets), FadeIn(target_lbl), FadeIn(atp_lbl), FadeIn(tag), run_time=0.8)

        self.at("moves the end")
        phos_beads = VGroup()
        transfer_anims = []
        p_lbl = T("P", size=26, color=ATP_GOLD).move_to([xs[0] + 1.55, -0.45, 0])
        for idx, x in enumerate(xs):
            p = Dot(radius=0.15, color=ATP_GOLD, stroke_color=TEXT, stroke_width=2.5)
            start_pt = atps[idx].phos.get_center()
            end_pt = targets[idx].get_top() + UP * 0.22 + RIGHT * 0.45
            p.move_to(start_pt)
            phos_beads.add(p)
            arc = ArcBetweenPoints(start_pt, end_pt, angle=-0.65)
            transfer_anims.append(MoveAlongPath(p, arc))

        self.play(FadeIn(p_lbl), AnimationGroup(*transfer_anims, lag_ratio=0.12), run_time=2.8)

        self.at("onto another")
        # Target proteins light up bright emerald-green and shift slightly upward to engage the kinase
        self.play(
            *[t.animate.set_stroke(SIGNAL_GRN, width=3.5).set_fill(SIGNAL_GRN, opacity=0.28).shift(UP * 0.10) for t in targets],
            target_lbl.animate.shift(UP * 0.10),
            FadeOut(phos_beads), FadeOut(p_lbl),
            run_time=2.2,
        )

        self.at("active kinases")
        # Fold all three clefts into identical active working shapes over the full beat
        self.play(fold_tr.animate.set_value(1.0), run_time=2.6)

        self.at("nearly the same")
        cleft_highlights = VGroup(*[
            Polygon(
                *_chamfer_box(2.25, 0.56, 0.10),
                stroke_color=ATP_GOLD, stroke_width=3.8, fill_color=ATP_GOLD, fill_opacity=0.12,
            ).move_to([x - 0.12, 0.35, 0])
            for x in xs
        ])
        same_cap = caption("Active clefts share nearly the same shape", size=28, color=ATP_GOLD)
        self.play(FadeIn(cleft_highlights), FadeIn(same_cap), run_time=2.2)

        self.at("drug was expected")
        drugs = VGroup(*[_drug_block(neck_h=0.40, width=1.9, color=DRUG_TEAL).move_to([x - 0.3, 2.15, 0]) for x in xs])
        drug_lbl = T("one pocket's drug", size=26, color=DRUG_TEAL).next_to(drugs[1], UP, buff=0.14)
        jam_cap = caption("Expected: one drug jams dozens of kinases", size=28, color=DRUG_TEAL)

        self.play(FadeIn(drugs), FadeIn(drug_lbl), swap(same_cap, jam_cap, run_time=0.7), run_time=1.1)
        self.play(
            *[d.animate.move_to([x - 0.15, 0.35, 0]) for d, x in zip(drugs, xs)],
            *[a.animate.shift(LEFT * 1.15).set_opacity(0.25) for a in atps],
            FadeOut(atp_lbl),
            FadeOut(drug_lbl),
            *[t.animate.set_stroke(GREY, width=2.0).set_fill(GREY, opacity=0.08) for t in targets],
            run_time=2.2,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 3: Idle Shape
class S03IdleShape(SpokenScene):
    def construct(self):
        heading = T("1. Idle-shape selectivity", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        xs = [-4.0, 0.0, 4.0]
        idle_tr = ValueTracker(0.0)

        def make_k0():
            t = idle_tr.get_value()
            gap = 0.50 + 0.22 * t
            return _mini_kinase(cleft_gap=gap, lobe_shift=0.12 * t, width=2.45, height=2.25, fill_op=0.30).move_to([xs[0], 0.35, 0])

        def make_k1():
            t = idle_tr.get_value()
            gap = 0.50 - 0.30 * t
            return _mini_kinase(cleft_gap=gap, lobe_shift=-0.22 * t, width=2.45, height=2.25, fill_op=0.30).move_to([xs[1], 0.35, 0])

        def make_k2():
            t = idle_tr.get_value()
            k = _mini_kinase(cleft_gap=0.50 - 0.14 * t, lobe_shift=0.0, width=2.45, height=2.25, fill_op=0.30).move_to([xs[2], 0.35, 0])
            if t > 0.05:
                lip = RoundedRectangle(
                    corner_radius=0.08, width=0.45 * t, height=0.65 * t,
                    stroke_color=KINASE_BLUE, stroke_width=2.2, fill_color=KINASE_BLUE, fill_opacity=0.45,
                ).move_to([xs[2] - 0.72, 0.35, 0])
                k.add(lip)
            return k

        k0, k1, k2 = always_redraw(make_k0), always_redraw(make_k1), always_redraw(make_k2)
        kinases = VGroup(k0, k1, k2)
        drugs = VGroup(*[_drug_block(neck_h=0.40, width=1.9, color=DRUG_TEAL).move_to([x - 0.15, 0.35, 0]) for x in xs])

        self.play(FadeIn(heading), FadeIn(kinases), FadeIn(drugs), FadeIn(tag), run_time=0.8)
        self.play(*[d.animate.move_to([x - 1.35, -1.55, 0]) for d, x in zip(drugs, xs)], run_time=1.8)

        self.at("working shapes")
        work_cap = caption("Working shapes must match to pass phosphate", size=28, color=TEXT)
        work_rings = VGroup(*[
            Polygon(*_chamfer_box(2.25, 0.56, 0.10), stroke_color=ATP_GOLD, stroke_width=3.0, fill_opacity=0.0).move_to([x - 0.12, 0.35, 0])
            for x in xs
        ])
        self.play(FadeIn(work_cap), Create(work_rings), run_time=1.8)
        self.play(FadeOut(work_rings), run_time=1.1)

        self.at("differ between kinases")
        idle_cap = caption("Idle shapes thought to differ across kinases", size=28, color=KINASE_BLUE)
        k_labels = VGroup(
            T("ABL", size=26, color=TEXT).move_to([xs[0], 1.85, 0]),
            T("other kinase", size=24, color=GREY).move_to([xs[1], 1.85, 0]),
            T("other kinase", size=24, color=GREY).move_to([xs[2], 1.85, 0]),
        )
        self.play(idle_tr.animate.set_value(1.0), FadeIn(k_labels), swap(work_cap, idle_cap, run_time=0.7), run_time=2.2)

        self.at("Imatinib fits")
        ima_lbl = T("imatinib", size=26, color=DRUG_TEAL).next_to(drugs[0], DOWN, buff=0.18)
        self.play(FadeIn(ima_lbl), run_time=0.6)
        self.play(
            drugs[0].animate.move_to([xs[0] - 0.12, 0.35, 0]),
            ima_lbl.animate.move_to([xs[0], -1.15, 0]),
            drugs[1].animate.move_to([xs[1] - 1.25, 0.35, 0]),
            drugs[2].animate.move_to([xs[2] - 1.45, 0.35, 0]),
            run_time=1.6,
        )
        no1 = T("no fit", size=26, color=GREY).move_to([xs[1], -1.15, 0])
        no2 = T("no fit", size=26, color=GREY).move_to([xs[2], -1.15, 0])
        fit0 = T("fits idle ABL", size=26, color=DRUG_TEAL).move_to([xs[0], -1.55, 0])
        self.play(
            drugs[1].animate.move_to([xs[1] - 0.6, -2.0, 0]).set_opacity(0.35),
            drugs[2].animate.move_to([xs[2] - 0.6, -2.0, 0]).set_opacity(0.35),
            FadeIn(no1), FadeIn(no2),
            swap(ima_lbl, fit0, run_time=0.6),
            run_time=1.6,
        )

        self.at("a short")
        self.play(
            FadeOut(k1), FadeOut(k2), FadeOut(drugs[1]), FadeOut(drugs[2]),
            FadeOut(no1), FadeOut(no2), FadeOut(k_labels[1]), FadeOut(k_labels[2]),
            FadeOut(idle_cap),
            run_time=0.6,
        )
        abl_static = _mini_kinase(cleft_gap=0.72, lobe_shift=0.12, width=2.85, height=2.60, fill_op=0.32).move_to([-3.3, 0.25, 0])
        drug_static = _drug_block(neck_h=0.46, width=2.2, color=DRUG_TEAL, fill_op=0.38).move_to([-3.45, 0.25, 0])
        self.remove(k0)
        self.play(
            FadeIn(abl_static),
            ReplacementTransform(drugs[0], drug_static),
            k_labels[0].animate.move_to([-3.3, 1.95, 0]),
            fit0.animate.move_to([-3.3, -1.45, 0]),
            run_time=0.7,
        )

        short_list = Ledger(
            [
                ("ABL", "imatinib fits idle shape", DRUG_TEAL),
                ("PDGFR", "PDGF receptor", DRUG_TEAL),
                ("KIT", "KIT receptor kinase", DRUG_TEAL),
            ],
            top_left=(0.4, 1.65), title="Short list hit by imatinib", row_h=0.72, key_w=1.85, width=5.6, size=28,
        )
        self.play(FadeIn(short_list), short_list.reveal(0), run_time=0.8)

        self.at("the PDGF")
        self.play(short_list.reveal(1), run_time=0.8)

        self.at("and KIT")
        self.play(short_list.reveal(2), short_list.mark(0, color=DRUG_TEAL), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ Scene 4: Dependence
class S04Dependence(SpokenScene):
    def construct(self):
        heading = T("2. Target dependence", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        tp = TwoPanel("Leukaemia cell (CML)", "Normal cell", colors=(MUTANT_RED, KINASE_BLUE), top=2.65, bottom=-2.35, size=30)

        # Right panel: Normal cell with ABL, PDGFR, KIT
        norm_c = tp.area("right")[0] + DOWN * 0.1
        norm_cell = RoundedRectangle(
            corner_radius=1.1, width=4.8, height=3.4,
            stroke_color=KINASE_BLUE, stroke_width=3.2, fill_color=KINASE_BLUE, fill_opacity=0.12,
        ).move_to(norm_c)
        norm_chips = VGroup(
            chip("ABL", KINASE_BLUE, size=24),
            chip("PDGFR", KINASE_BLUE, size=24),
            chip("KIT", KINASE_BLUE, size=24),
        ).arrange(DOWN, buff=0.22).move_to(norm_c + LEFT * 1.25)
        norm_arrow = Arrow(norm_chips[1].get_right() + RIGHT * 0.25, norm_chips[1].get_right() + RIGHT * 1.45,
                           buff=0, stroke_width=4.5, color=SIGNAL_GRN)
        norm_sig_lbl = T("normal\ngrowth", size=22, color=SIGNAL_GRN).next_to(norm_arrow, DOWN, buff=0.16)

        self.play(FadeIn(heading), FadeIn(tp.right_frame), FadeIn(tp.right_head), FadeIn(norm_cell),
                  FadeIn(norm_chips), FadeIn(norm_arrow), FadeIn(norm_sig_lbl), FadeIn(tag), run_time=0.6)

        self.at("normal cells use")
        same3_cap = caption("Normal cells also use ABL, PDGFR, and KIT", size=28, color=KINASE_BLUE)
        self.play(FadeIn(same3_cap), run_time=1.4)

        self.at("the second layer")
        dep_cap = caption("Layer 2: how strongly a cell depends on the blocked kinase", size=28, color=TEXT)
        self.play(swap(same3_cap, dep_cap, run_time=0.6), run_time=1.0)

        # Normal cell passes green growth beads along its arrow while target dependence is explained
        norm_bead = Dot(radius=0.12, color=SIGNAL_GRN, stroke_color=TEXT, stroke_width=1.5).move_to(norm_arrow.get_start())
        self.play(FadeIn(norm_bead), run_time=0.4)
        self.play(norm_bead.animate.move_to(norm_arrow.get_end()), run_time=2.2)
        norm_bead.move_to(norm_arrow.get_start())
        self.play(norm_bead.animate.move_to(norm_arrow.get_end()), run_time=2.2)
        self.play(FadeOut(norm_bead), run_time=0.4)

        self.at("leukemia cells")
        cml_c = tp.area("left")[0] + DOWN * 0.1
        cml_scale = ValueTracker(1.0)
        cml_cell = always_redraw(lambda: RoundedRectangle(
            corner_radius=1.1 * cml_scale.get_value(),
            width=4.8 * cml_scale.get_value(),
            height=3.4 * cml_scale.get_value(),
            stroke_color=MUTANT_RED, stroke_width=3.2, fill_color=MUTANT_RED, fill_opacity=0.14,
        ).move_to(cml_c))
        bcr_box = chip("BCR", GOLD, size=26).move_to(cml_c + LEFT * 1.45 + UP * 0.72)
        abl_box = chip("ABL", KINASE_BLUE, size=26).move_to(cml_c + RIGHT * 0.65 + UP * 0.72)
        self.play(
            FadeIn(tp.left_frame), FadeIn(tp.left_head),
            FadeIn(cml_cell), FadeIn(bcr_box), FadeIn(abl_box),
            run_time=0.75,
        )
        self.play(
            bcr_box.animate.move_to(cml_c + LEFT * 0.92 + UP * 0.72),
            abl_box.animate.move_to(cml_c + RIGHT * 0.42 + UP * 0.72),
            cml_scale.animate.set_value(1.04),
            run_time=0.65,
        )

        self.at("fused")
        fused_box = chip("BCR-ABL", KINASE_BLUE, size=26).move_to(cml_c + UP * 0.72)
        cml_arrow = Arrow(fused_box.get_bottom() + DOWN * 0.15, cml_c + DOWN * 0.72,
                          buff=0, stroke_width=7.5, color=SIGNAL_GRN, max_tip_length_to_length_ratio=0.28)
        cml_sig_lbl = T("always on:\ndivision", size=22, color=SIGNAL_GRN).next_to(cml_arrow, RIGHT, buff=0.35)
        self.play(ReplacementTransform(VGroup(bcr_box, abl_box), fused_box), run_time=1.0)
        self.play(GrowArrow(cml_arrow), FadeIn(cml_sig_lbl), run_time=0.9)
        self.play(cml_scale.animate.set_value(1.07), run_time=1.1)

        self.at("cannot live without")
        # Both drugs start cleanly inside their cells and dock clear of chip borders and signal arrow
        ima_left = _drug_block(neck_h=0.45, width=2.0, color=DRUG_TEAL, fill_op=0.50).scale(0.45).move_to(cml_c + LEFT * 1.45 + DOWN * 0.22)
        ima_right = _drug_block(neck_h=0.45, width=2.0, color=DRUG_TEAL, fill_op=0.50).scale(0.45).move_to(norm_c + RIGHT * 1.45 + UP * 0.65)
        self.play(FadeIn(ima_left), FadeIn(ima_right), run_time=0.35)
        self.play(
            ima_left.animate.move_to(cml_c + LEFT * 1.15 + UP * 0.10),
            ima_right.animate.move_to(norm_chips[0].get_right() + RIGHT * 0.62),
            run_time=0.75,
        )
        dead_lbl = T("signal lost: cell dies", size=24, color=GREY).move_to(cml_c + DOWN * 1.65)
        short_arrow = Arrow(cml_c + UP * 0.02, cml_c + DOWN * 0.72,
                            buff=0, stroke_width=5.5, color=GREY, max_tip_length_to_length_ratio=0.30).set_opacity(0.40)
        self.play(
            Transform(cml_arrow, short_arrow),
            FadeOut(cml_sig_lbl),
            cml_scale.animate.set_value(0.70),
            fused_box.animate.move_to(cml_c + RIGHT * 0.45 + UP * 0.55),
            ima_left.animate.move_to(cml_c + LEFT * 1.00 + UP * 0.55),
            FadeIn(dead_lbl),
            run_time=0.95,
        )

        self.at("Normal cells tolerate")
        paused_lbl = T("pauses,\nstays intact", size=22, color=KINASE_BLUE).next_to(norm_arrow, DOWN, buff=0.16)
        self.play(
            norm_arrow.animate.set_color(GREY).set_opacity(0.45),
            swap(norm_sig_lbl, paused_lbl, run_time=0.6),
            norm_cell.animate.scale(0.95),
            run_time=1.3,
        )

        self.at("tissue injury")
        warn_cap = caption("Tissue injury can still occur", size=28, color=ATP_GOLD)
        self.play(swap(dep_cap, warn_cap, run_time=0.6), norm_cell.animate.set_stroke(ATP_GOLD, width=3.2), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ Scene 5: Relapse
class S05Relapse(SpokenScene):
    def construct(self):
        heading = T("Relapse: one changed residue at 315", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        cell_ring = RoundedRectangle(
            corner_radius=1.1, width=10.4, height=3.8,
            stroke_color=MUTANT_RED, stroke_width=3.2, fill_color=MUTANT_RED, fill_opacity=0.07,
        ).move_to([0, -0.15, 0])
        cell_lbl = T("rebounding leukaemia cell", size=24, color=MUTANT_RED).move_to([0, 2.38, 0])

        pocket = _pocket_cross_section(bulk=0.0, center=[0.0, -0.15, 0], scale=0.88)
        drug = _drug_block(neck_h=0.45 * 0.88, width=2.2 * 0.88, color=DRUG_TEAL, fill_op=0.42)
        drug.move_to(pocket.get_center() + RIGHT * 0.15 * 0.88)
        drug_lbl = T("imatinib", size=26, color=DRUG_TEAL).next_to(pocket, LEFT, buff=0.30)

        # Gene strip sized cleanly around text so box borders never touch letters
        codon_title = T("BCR-ABL codon 315:", size=24, color=GREY)
        codon_act = M("ACT", size=28, color=KINASE_BLUE)
        codon_row = VGroup(codon_title, codon_act).arrange(RIGHT, buff=0.22).move_to([0, 2.38, 0])
        codon_box = RoundedRectangle(
            corner_radius=0.12, width=codon_row.width + 0.60, height=0.68,
            stroke_color=GREY, stroke_width=2.2, fill_color=BG, fill_opacity=0.9,
        ).move_to(codon_row)

        self.play(FadeIn(heading), FadeIn(pocket), FadeIn(drug), FadeIn(drug_lbl), FadeIn(tag), run_time=0.8)

        self.at("improved on imatinib")
        status_ok = T("imatinib holds pocket", size=26, color=DRUG_TEAL).move_to([0, -3.02, 0])
        self.play(FadeIn(status_ok), run_time=1.2)

        self.at("later relapsed")
        status_rel = T("patients later relapsed", size=26, color=MUTANT_RED).move_to([0, -3.02, 0])
        self.play(
            FadeIn(cell_ring), FadeIn(cell_lbl),
            cell_ring.animate.scale(1.10),
            swap(status_ok, status_rel, run_time=0.6),
            run_time=1.8,
        )

        self.at("from their blood")
        # Sequencing scan sweep across codon_box
        scan_bar = Rectangle(width=0.32, height=0.64, stroke_width=0, fill_color=ATP_GOLD, fill_opacity=0.35)
        scan_bar.move_to(codon_box.get_left() + RIGHT * 0.35)
        self.play(FadeOut(cell_ring), FadeOut(cell_lbl), FadeOut(status_rel), run_time=0.4)
        self.play(
            FadeIn(codon_box), FadeIn(codon_title), FadeIn(codon_act),
            run_time=0.8,
        )
        self.play(FadeIn(scan_bar), run_time=0.3)
        self.play(scan_bar.animate.move_to(codon_box.get_right() + LEFT * 0.35), run_time=1.5)
        self.play(FadeOut(scan_bar), run_time=0.35)

        self.at("position 315")
        thr_lbl = T("Thr 315", size=26, color=KINASE_BLUE).move_to([4.15, 1.35, 0])
        thr_ptr = Arrow(
            thr_lbl.get_left() + LEFT * 0.06,
            pocket.gk.get_right() + RIGHT * 0.06 + UP * 0.05,
            buff=0, stroke_width=2.6, color=KINASE_BLUE, max_tip_length_to_length_ratio=0.25,
        )
        thr_ptr.layout_ok = True
        self.play(
            FadeIn(thr_lbl), Create(thr_ptr),
            pocket.gk.animate.set_fill(KINASE_BLUE, opacity=0.80),
            run_time=1.4,
        )

        self.at("Threonine")
        self.play(pocket.gk.animate.set_stroke(ATP_GOLD, width=4.5), run_time=0.5)

        self.at("turned into")
        bulk_tr = ValueTracker(0.0)
        ile_lbl = T("Ile 315", size=28, color=MUTANT_RED).move_to([4.15, 1.35, 0])
        codon_att = M("ATT", size=28, color=MUTANT_RED).move_to(codon_act)

        def update_gk(m):
            b = bulk_tr.get_value()
            w = (0.42 + 0.62 * b) * 0.88
            h = (0.42 + 0.68 * b) * 0.88
            col = interpolate_color(ManimColor(KINASE_BLUE), ManimColor(MUTANT_RED), b)
            new_gk = RoundedRectangle(
                corner_radius=0.12 * 0.88, width=w, height=h,
                stroke_color=col, stroke_width=3.0, fill_color=col, fill_opacity=0.45 + 0.25 * b,
            )
            top_anchor = [pocket.gk.get_center()[0], pocket.gk.get_top()[1], 0]
            new_gk.move_to([top_anchor[0], top_anchor[1] - h / 2, 0])
            m.become(new_gk)

        pocket.gk.add_updater(update_gk)
        self.play(
            bulk_tr.animate.set_value(1.0),
            swap(thr_lbl, ile_lbl, run_time=0.7),
            swap(codon_act, codon_att, run_time=0.7),
            thr_ptr.animate.set_color(MUTANT_RED),
            run_time=1.8,
        )

        self.at("a bulkier")
        bulk_note = T("bulkier side chain beside the drug", size=28, color=MUTANT_RED).move_to([0, -3.02, 0])
        self.play(
            drug.animate.shift(LEFT * 1.60),
            FadeIn(bulk_note, run_time=0.6),
            run_time=2.1,
        )
        pocket.gk.clear_updaters()
        self.finish()


# ------------------------------------------------------------------ Scene 6: Gatekeeper
class S06Gatekeeper(SpokenScene):
    def construct(self):
        heading = T("Gatekeeper 315 guards the back alcove", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        pocket = _pocket_cross_section(bulk=0.0, center=[0.1, 0.1, 0], scale=0.95)
        thr_lbl = T("Gatekeeper 315 (Thr)", size=26, color=KINASE_BLUE).next_to(pocket.upper, UP, buff=0.22).shift(RIGHT * 0.4)
        gk_ptr = Arrow(
            thr_lbl.get_bottom() + DOWN * 0.04,
            pocket.gk.get_top() + UP * 0.06,
            buff=0, stroke_width=2.6, color=KINASE_BLUE, max_tip_length_to_length_ratio=0.25,
        )
        gk_ptr.layout_ok = True

        self.play(FadeIn(heading), FadeIn(pocket), FadeIn(tag), run_time=0.8)

        self.at("gatekeeper residue")
        self.play(FadeIn(thr_lbl), Create(gk_ptr), pocket.gk.animate.set_fill(KINASE_BLUE, opacity=0.75), run_time=2.1)

        self.at("back alcove")
        alc_lbl = T("Back alcove", size=24, color=KINASE_BLUE).next_to(pocket, RIGHT, buff=0.30).shift(UP * 0.15)
        alc_ptr = Arrow(
            alc_lbl.get_left() + LEFT * 0.04,
            pocket.alcove_zone.get_right() + RIGHT * 0.04 + UP * 0.15,
            buff=0, stroke_width=2.2, color=KINASE_BLUE, max_tip_length_to_length_ratio=0.20,
        )
        alc_ptr.layout_ok = True
        self.play(
            pocket.alcove_zone.animate.set_fill(KINASE_BLUE, opacity=0.32).set_stroke(KINASE_BLUE, width=3.2),
            FadeIn(alc_lbl), Create(alc_ptr),
            run_time=1.3,
        )

        self.at("the ATP site")
        atp_site_lbl = T("ATP site", size=24, color=ATP_GOLD).move_to(pocket.atp_zone)
        self.play(
            pocket.atp_zone.animate.set_fill(ATP_GOLD, opacity=0.22).set_stroke(ATP_GOLD, width=3.0),
            FadeIn(atp_site_lbl),
            run_time=1.8,
        )

        self.at("Imatinib reaches")
        drug = _drug_block(neck_h=0.52 * 0.95, width=2.2 * 0.95, color=DRUG_TEAL, fill_op=0.40)
        drug.move_to(pocket.get_left() + LEFT * 1.45)
        drug_lbl = T("imatinib", size=26, color=DRUG_TEAL).next_to(drug, UP, buff=0.18)
        self.play(FadeIn(drug), FadeIn(drug_lbl), FadeOut(atp_site_lbl), run_time=0.7)
        self.play(
            drug.animate.move_to(pocket.get_center() + RIGHT * 0.25),
            drug_lbl.animate.next_to(pocket.atp_zone, LEFT, buff=0.30).shift(UP * 0.35),
            run_time=1.8,
        )

        self.at("hydrogen bond")
        hbond = DashedLine(
            pocket.gk.get_bottom() + DOWN * 0.02,
            drug.bridge.get_top() + UP * 0.02,
            color=ATP_GOLD, stroke_width=3.5, dash_length=0.08,
        )
        hb_lbl = T("H-bond", size=24, color=ATP_GOLD).move_to([pocket.atp_zone.get_center()[0] + 0.15, 0.74, 0])
        hb_ptr = Arrow(hb_lbl.get_right() + RIGHT * 0.06, hbond.get_center() + LEFT * 0.12,
                       buff=0, stroke_width=2.2, color=ATP_GOLD, tip_length=0.14)
        hb_ptr.layout_ok = True
        self.play(Create(hbond), FadeIn(hb_lbl), Create(hb_ptr), run_time=1.4)

        self.at("Bulkier")
        ile_lbl = T("Ile 315", size=26, color=MUTANT_RED).next_to(pocket.upper, UP, buff=0.22).shift(RIGHT * 0.4)
        top_anchor = [pocket.gk.get_center()[0], pocket.gk.get_top()[1], 0]
        ile_gk = RoundedRectangle(
            corner_radius=0.12 * 0.95, width=1.04 * 0.95, height=1.10 * 0.95,
            stroke_color=MUTANT_RED, stroke_width=3.0, fill_color=MUTANT_RED, fill_opacity=0.70,
        )
        ile_gk.move_to([top_anchor[0], top_anchor[1] - ile_gk.height / 2, 0])

        self.play(
            Transform(pocket.gk, ile_gk),
            gk_ptr.animate.set_color(MUTANT_RED),
            swap(thr_lbl, ile_lbl, run_time=0.6),
            FadeOut(hbond), FadeOut(hb_lbl), FadeOut(hb_ptr),
            run_time=1.6,
        )

        self.at("blocks imatinib")
        drug_park = pocket.get_left() + LEFT * 1.55 + UP * 0.90
        self.play(
            drug.animate.move_to(drug_park),
            drug_lbl.animate.next_to(drug_park + UP * (drug.height / 2), UP, buff=0.16),
            run_time=1.6,
        )

        self.at("never uses the alcove")
        atp = _atp_token(scale=1.65 * 0.95)
        atp_target = pocket.atp_zone.get_center() + LEFT * 0.12 * 0.95
        atp.move_to([pocket.get_left()[0] - 1.4, atp_target[1], 0])
        atp_lbl = T("ATP", size=24, color=ATP_GOLD).next_to(atp, DOWN, buff=0.16)
        atp_grp = VGroup(atp, atp_lbl)
        self.play(FadeIn(atp), FadeIn(atp_lbl), run_time=0.5)
        self.play(
            atp_grp.animate.shift(RIGHT * (atp_target[0] - atp.get_center()[0])),
            run_time=1.7,
        )

        self.at("keeps firing")
        sig_start = pocket.lower.get_bottom() + DOWN * 0.12 + LEFT * 1.4 * 0.95
        sig_end = sig_start + DOWN * 0.85
        sig_arrow = Arrow(sig_start, sig_end, buff=0, stroke_width=6.0, color=SIGNAL_GRN,
                          max_tip_length_to_length_ratio=0.32)
        sig_lbl = T("kinase keeps firing", size=26, color=SIGNAL_GRN).next_to(sig_arrow, RIGHT, buff=0.22)
        self.play(GrowArrow(sig_arrow), FadeIn(sig_lbl), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ Scene 7: Predict
class S07Predict(SpokenScene):
    def construct(self):
        heading = T("Relapse proves the target", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        scene_g = _build_315_backdrop(center=[0.1, 0.25, 0], scale=0.92)
        pocket = scene_g.pocket
        drug = scene_g.drug
        drug_lbl = scene_g.drug_lbl
        sig_arrow = scene_g.sig_arrow

        self.play(FadeIn(heading), FadeIn(scene_g), FadeIn(tag), run_time=0.8)

        self.at("works like an experiment")
        p_bead = Dot(radius=0.14, color=ATP_GOLD, stroke_color=TEXT, stroke_width=2.0).move_to(sig_arrow.get_start())
        self.play(FadeIn(p_bead), run_time=0.3)
        self.play(p_bead.animate.move_to(sig_arrow.get_end()), run_time=1.4)
        self.play(FadeOut(p_bead), run_time=0.3)

        self.at("Changing one drug contact")
        _imatinib_approach_gk(
            self, scene_g, step_times=(0.20, 0.20, 0.20, 0.25, 0.25, 0.20, 0.20, 0.20),
            extra_out=(pocket.gk.animate.set_stroke(ATP_GOLD, width=5.5).set_fill(MUTANT_RED, opacity=0.90),),
        )

        self.at("catalysis intact")
        # Show phosphate travelling from ATP out along the green catalysis arrow
        p_bead2 = Dot(radius=0.15, color=ATP_GOLD, stroke_color=TEXT, stroke_width=2.2).move_to(scene_g.atp.phos.get_center())
        self.play(pocket.gk.animate.set_stroke(MUTANT_RED, width=3.0).set_fill(MUTANT_RED, opacity=0.70), FadeIn(p_bead2), run_time=0.4)
        self.play(p_bead2.animate.move_to(sig_arrow.get_start()), run_time=0.7)
        self.play(p_bead2.animate.move_to(sig_arrow.get_end()), sig_arrow.animate.set_stroke(width=8.5), run_time=0.9)
        self.play(FadeOut(p_bead2), sig_arrow.animate.set_stroke(width=6.0), run_time=0.3)

        self.at("hit the right target")
        proof_lbl = T("same target confirmed", size=26, color=SIGNAL_GRN).next_to(scene_g.sig_lbl, RIGHT, buff=0.45)
        self.play(FadeIn(proof_lbl), pocket.atp_zone.animate.set_fill(ATP_GOLD, opacity=0.14), run_time=1.3)

        self.at("still needed that kinase")
        _imatinib_approach_gk(
            self, scene_g, step_times=(0.22, 0.22, 0.22, 0.28, 0.28, 0.22, 0.22, 0.22),
            extra_in=(pocket.atp_zone.animate.set_fill(ATP_GOLD, opacity=0.06),),
        )

        self.at("Pause and predict")
        q = question_card("How must the next drug change at position 315?", y=-2.95, color=GOLD, size=30, max_w=10.2)
        self.play(FadeOut(tag), FadeOut(proof_lbl), FadeIn(q), run_time=0.9)

        self.at("To beat this mutant")
        p_bead3 = Dot(radius=0.15, color=ATP_GOLD, stroke_color=TEXT, stroke_width=2.2).move_to(sig_arrow.get_start())
        self.play(FadeIn(p_bead3), run_time=0.3)
        _imatinib_approach_gk(
            self, scene_g, step_times=(0.25, 0.25, 0.25, 0.55, 0.55, 0.25, 0.25, 0.25),
            extra_out=(p_bead3.animate.move_to(sig_arrow.get_end()),),
        )
        self.play(FadeOut(p_bead3), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ Scene 8: Pause (PredictPause)
class S08Pause(PredictPause):
    QUESTION = "How must the next drug change at position 315?"
    CARD = {"y": -2.95, "color": GOLD, "size": 30, "max_w": 10.2}
    SECONDS = 4.5

    def backdrop(self):
        heading = T("Relapse proves the target", size=34, color=TEXT).move_to([0, 3.22, 0])
        scene_g = _build_315_backdrop(center=[0.1, 0.25, 0], scale=0.92)
        # Visual note explicitly specifies: coral-red Ile 315 pulses slowly during the 4.5 s pause
        gk = scene_g.pocket.gk
        gk._pulse_t = 0.0
        base_op = 0.68

        def slow_pulse(mob, dt):
            mob._pulse_t += dt
            s = np.sin(2.4 * mob._pulse_t)
            mob.set_fill(MUTANT_RED, opacity=base_op + 0.28 * s)
            mob.set_stroke(width=3.2 + 2.4 * s)

        gk.add_updater(slow_pulse)
        return VGroup(heading, scene_g)


# ------------------------------------------------------------------ Scene 9: Ponatinib
class S09Ponatinib(SpokenScene):
    def construct(self):
        heading = T("Ponatinib clears Ile 315 with a slim bridge", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        scene_g = _build_315_backdrop(center=[0.1, 0.15, 0], scale=0.92)
        pocket = scene_g.pocket
        atp = scene_g.atp
        atp_lbl = scene_g.atp_lbl
        sig_arrow = scene_g.sig_arrow
        sig_lbl = scene_g.sig_lbl
        drug = scene_g.drug
        drug_lbl = scene_g.drug_lbl

        self.play(FadeIn(heading), FadeIn(scene_g), FadeIn(tag), run_time=0.8)

        self.at("depends on")
        # Show imatinib bumping into Ile 315 and highlighting its thick middle bridge without overlapping ATP
        def show_clash():
            clash_box = SurroundingRectangle(drug.bridge, color=MUTANT_RED, stroke_width=3.2, buff=0.06)
            self.play(Create(clash_box), run_time=0.65)
            self.play(FadeOut(clash_box), run_time=0.30)

        _imatinib_approach_gk(self, scene_g, step_times=(0.25, 0.25, 0.25, 0.40, 0.40, 0.25, 0.25, 0.25), on_peak=show_clash)

        self.at("without that contact")
        # Highlight both end grip regions (ATP site + back alcove)
        self.play(
            pocket.alcove_zone.animate.set_fill(DRUG_TEAL, opacity=0.22).set_stroke(DRUG_TEAL, width=3.0),
            pocket.atp_zone.animate.set_fill(DRUG_TEAL, opacity=0.14).set_stroke(DRUG_TEAL, width=2.8),
            run_time=2.2,
        )

        self.at("gave ponatinib")
        neck_tr = ValueTracker(0.52 * 0.92)
        drug_center = drug.get_center().copy()

        def make_slim_drug():
            nh = neck_tr.get_value()
            frac = np.clip((0.52 * 0.92 - nh) / (0.52 * 0.92 - 0.10), 0.0, 1.0)
            w = (2.2 + 0.35 * frac) * 0.92
            d = _drug_block(neck_h=nh, width=w, color=DRUG_TEAL, fill_op=0.45)
            d.move_to(drug_center)
            return d

        slim_drug = always_redraw(make_slim_drug)
        self.remove(drug)
        self.add(slim_drug)

        pona_lbl = T("ponatinib", size=26, color=DRUG_TEAL).next_to(drug_center, UP, buff=0.52)
        self.play(
            neck_tr.animate.set_value(0.10),
            swap(drug_lbl, pona_lbl, run_time=0.6),
            pocket.atp_zone.animate.set_fill(ATP_GOLD, opacity=0.06).set_stroke(ATP_GOLD, width=1.8),
            run_time=2.2,
        )

        self.at("triple")
        slim_static = _drug_block(neck_h=0.10, width=2.55 * 0.92, color=DRUG_TEAL, fill_op=0.45).move_to(drug_center)
        self.remove(slim_drug)
        self.add(slim_static)

        bridge_lbl = T("Slim triple-bond bridge", size=24, color=DRUG_TEAL).move_to([-4.35, -1.98, 0])
        bridge_ptr = Arrow(
            bridge_lbl.get_top() + UP * 0.06,
            slim_static.bridge.get_bottom() + DOWN * 0.06,
            buff=0, stroke_width=2.4, color=DRUG_TEAL, max_tip_length_to_length_ratio=0.22,
        )
        bridge_ptr.layout_ok = True
        self.play(FadeIn(bridge_lbl), Create(bridge_ptr), run_time=1.3)
        # Advance ponatinib to pocket mouth aligned with the clear passage below Ile 315
        shift_vec = RIGHT * 0.35 + DOWN * 0.30 * 0.92
        new_ptr = Arrow(
            bridge_lbl.get_top() + UP * 0.06,
            slim_static.bridge.get_bottom() + shift_vec + DOWN * 0.06,
            buff=0, stroke_width=2.4, color=DRUG_TEAL, max_tip_length_to_length_ratio=0.22,
        )
        new_ptr.layout_ok = True
        self.play(
            slim_static.animate.shift(shift_vec),
            Transform(bridge_ptr, new_ptr),
            pona_lbl.animate.shift(shift_vec),
            run_time=1.5,
        )

        self.at("slender bridge")
        # Eject ATP straight left out of the open mouth before dropping to eject_pt, while slim_static steps aside above
        eject_pt = pocket.get_left() + LEFT * 1.45 + DOWN * 2.05
        atp_exit_mid = np.array([pocket.get_left()[0] - 0.30, pocket.get_center()[1] - 0.27, 0.0])
        atp_exit_left = np.array([eject_pt[0], atp_exit_mid[1], 0.0])
        self.play(
            FadeOut(bridge_ptr), FadeOut(bridge_lbl), FadeOut(atp_lbl),
            slim_static.animate.shift(UP * 0.75),
            pona_lbl.animate.shift(UP * 0.75),
            atp.animate.move_to(atp_exit_mid),
            run_time=0.5,
        )
        self.play(
            atp.animate.move_to(atp_exit_left),
            run_time=0.5,
        )
        atp_lbl.move_to(eject_pt + LEFT * 1.15).set_opacity(0.35)
        self.play(
            atp.animate.move_to(eject_pt).set_opacity(0.35),
            run_time=0.55,
        )
        target_x = pocket.get_center()[0] + 0.12
        target_y = pocket.get_center()[1] - 0.30 * 0.92
        self.play(
            FadeIn(atp_lbl),
            slim_static.animate.set_y(target_y),
            pona_lbl.animate.shift(DOWN * 0.75),
            run_time=0.35,
        )
        self.play(
            slim_static.animate.move_to([target_x, target_y, 0]),
            pona_lbl.animate.next_to(pocket.get_left() + LEFT * 1.15 + UP * 0.5, UP, buff=0.1),
            run_time=1.5,
        )

        self.at("shuts down")
        off_lbl = T("mutant kinase shut down", size=26, color=GREY).next_to(sig_arrow, RIGHT, buff=0.22)
        self.play(
            sig_arrow.animate.set_color(GREY).set_opacity(0.35),
            swap(sig_lbl, off_lbl, run_time=0.6),
            run_time=1.6,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 10: Rule
class S10Rule(SpokenScene):
    def construct(self):
        heading = T("Two principles of targeted drugs", size=34, color=TEXT).move_to([0, 3.22, 0])
        tag = scope_tag("schematic")

        tp = TwoPanel(
            "1. Shape + target dependence",
            "2. Escape guides next drug",
            colors=(DRUG_TEAL, MUTANT_RED),
            top=2.65, bottom=-2.35, size=28,
        )

        # Left panel contents: larger pockets (0.56 scale) filling panels cleanly
        lc = tp.area("left")[0]
        l_pocket = _pocket_cross_section(bulk=0.0, center=lc + UP * 0.55, scale=0.56)
        l_ima = _drug_block(neck_h=0.45, width=2.2, color=DRUG_TEAL, fill_op=0.45).scale(0.56).move_to(l_pocket.get_center() + RIGHT * 0.15 * 0.56)
        l_thr = T("Thr 315", size=24, color=KINASE_BLUE).next_to(l_pocket.upper, UP, buff=0.14)

        l_cml = chip("CML shrinks", MUTANT_RED, size=24).move_to(lc + DOWN * 1.35 + LEFT * 1.45)
        l_norm = chip("Normal intact", KINASE_BLUE, size=24).move_to(lc + DOWN * 1.35 + RIGHT * 1.45)

        # Right panel contents
        rc = tp.area("right")[0]
        r_pocket = _pocket_cross_section(bulk=1.0, center=rc + UP * 0.55, scale=0.56)
        r_pona_target = r_pocket.get_center() + RIGHT * 0.048 + DOWN * 0.30 * 0.56
        r_pona = _drug_block(neck_h=0.10, width=2.55, color=DRUG_TEAL, fill_op=0.45).scale(0.56).move_to(r_pona_target)
        r_ile = T("Ile 315", size=24, color=MUTANT_RED).next_to(r_pocket.upper, UP, buff=0.14)

        r_esc = chip("Ile 315 escape", MUTANT_RED, size=22).move_to(rc + DOWN * 1.35 + LEFT * 1.60)
        r_next = chip("Ponatinib clears", DRUG_TEAL, size=22).move_to(rc + DOWN * 1.35 + RIGHT * 1.55)
        r_arrow = Arrow(r_esc.get_right() + RIGHT * 0.08, r_next.get_left() + LEFT * 0.08,
                        buff=0, stroke_width=3.2, color=TEXT, max_tip_length_to_length_ratio=0.28)

        # Reveal panels AND both pockets right at start so panels are never empty
        self.play(FadeIn(heading), FadeIn(tp), FadeIn(tag), run_time=0.5)

        self.at("two principles")
        self.play(
            FadeIn(l_pocket), FadeIn(l_thr),
            FadeIn(r_pocket), FadeIn(r_ile),
            run_time=1.2,
        )

        self.at("where a drug binds")
        l_ima_start = l_pocket.get_left() + LEFT * 0.35
        l_ima.move_to(l_ima_start)
        self.play(FadeIn(l_ima), run_time=0.5)
        self.play(
            l_ima.animate.move_to(l_pocket.get_center() + RIGHT * 0.15 * 0.56),
            l_pocket.alcove_zone.animate.set_fill(DRUG_TEAL, opacity=0.24),
            run_time=2.5,
        )

        self.at("relies on that target")
        self.play(FadeIn(l_cml), FadeIn(l_norm), run_time=1.0)
        self.play(
            l_cml[0].animate.set_stroke(MUTANT_RED, width=3.5),
            l_norm[0].animate.set_stroke(KINASE_BLUE, width=3.5),
            run_time=1.8,
        )

        self.at("alters a drug contact")
        self.play(FadeIn(r_esc), Indicate(r_pocket.gk, color=ATP_GOLD, scale_factor=1.10), run_time=1.5)

        self.at("guides the next drug")
        r_pona_start = r_pocket.get_left() + LEFT * 0.35 + DOWN * 0.30 * 0.56
        r_pona.move_to(r_pona_start)
        self.play(GrowArrow(r_arrow), FadeIn(r_next), FadeIn(r_pona), run_time=0.6)
        self.play(r_pona.animate.move_to(r_pona_target), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ Scene 11: End
class S11End(EndCard):
    LINE = "Where a drug binds shapes selectivity, and escape guides the next drug."
