"""AMPK: The Energy Veto — mTOR and AMPK, Chapter 2.

COLOUR MAP (one colour per concept for the entire film):
    TEAL   (#3FB8C0) : Lysosome compartment / membrane & muscle cell surface
    GREEN  (#83C167) : Growth factor signal, Akt, Rheb-GTP, active output / income (fat burn, glucose uptake)
    BLUE   (#58C4DD) : Amino acids, Rag GTPases, GLUT4 glucose transporters
    GOLD   (#D4A843) : mTORC1 complex & Raptor subunit
    ORANGE (#F08C3A) : AMPK complex (Alpha, Beta, Gamma) & AMP fuel-alarm signal
    YELLOW (#F5D547) : Phosphate (P / Thr172), ADP & ACC
    RED    (#FC6255) : TSC2 brake, inhibitory bars (cut spending), AMPK ON active flare
    GREY   (#8B93A1) : Inactive / GDP state, Phosphatase, missing TSC2 outline, schematic tags
    TEXT   (#E8EAF0) : Primary text & ATP bar

ONE CARRIED WORLD:
    Cross-section of a single cell: left side holds the ATP/AMP energy gauge and AMPK three-subunit
    complex (plus metabolic budget outputs); right side holds the TEAL lysosome with Growth factor ->
    TSC2 -| Rheb-GTP and Amino acids -> Rags -> mTORC1 (Raptor) -> Protein building.
    Every zoomed view (adenylate kinase chart, AMPK structure, phosphatase protection) zooms into
    and pulls back out of this same cell world.

SCENES — WHAT CHANGES AND WHAT IT IS COMPUTED FROM:
    s00_title                 : Standard TitleCard ("mTOR and AMPK: Reading Nutrients and Energy" / "AMPK: The Energy Veto").
    s01_link_and_hook         : Right side shows active mTORC1 on lysosome with amino-acid/protein flow; left side fades in ATP dial (100% -> 80%) and quiet AMPK block.
    s02_why_amp               : Computed equilibrium curve & live bars for 2 ADP <-> ATP + AMP (K = 0.5, total pool = 5.525 mM) from 100% to 80% ATP; equations build word-by-word, 90% worked point marked after spoken.
    s03_ampk_structure_switch : Zoomed 3-subunit AMPK; AMP tokens stream into Gamma pocket displacing ATP, LKB1 stamps yellow P onto Alpha (Thr172).
    s04_amp_protects_and_boosts: Phosphatase strips P when ATP sits in Gamma; AMP docks in Gamma, subunits flex inward shielding P so phosphatase bounces off, Alpha flares AMPK ON.
    s05_predict_setup         : Full cell with both gauges; ATP dips, AMPK ON; TSC2 fades to dashed missing outline while Rheb-GTP and mTORC1 stay lit; top question banner asks predict question with NO answer shown.
    s06_pause                 : PredictPause (4.5 s) holding exact s05 predict frame and question banner with countdown ring, NO answer shown.
    s07_veto_reveal           : Inset 'Normal cell' stamps P on TSC2 -> Rheb-GDP; main frame stamps P on Raptor (mTORC1 subunit) -> mTORC1 dims partway and protein-building arrow thins.
    s08_budget_shift          : Left/right budget panels: AMPK cuts fat/cholesterol synthesis, builds 'ACC -> malonyl-CoA -| fatty acid entry' then opens mitochondrial door as ACC turns off, and moves glucose transporters to muscle surface.
    s09_scope_close           : Full cell settled in energy-saving state; Gamma note 'AMP:ATP ratio (+ ADP & calcium inputs)' builds as spoken; veto overrides both growth yeses.
    s10_end                   : Standard EndCard ("AMPK reads rising AMP to conserve energy and veto mTORC1.").
"""

import numpy as np
from bp_parts import *

ORANGE = "#F08C3A"

# ------------------------------------------------------------------ adenylate kinase equilibrium model
K_AK = 0.5
ATP_REST = 5.0
ADP_REST = 0.50
AMP_REST = K_AK * (ADP_REST ** 2) / ATP_REST   # 0.025 mM
A_TOTAL = ATP_REST + ADP_REST + AMP_REST       # 5.525 mM


def ak_concentrations(atp_pct):
    """Given ATP as % of rest (80..100), return (ATP, ADP, AMP) in mM from 2 ADP <-> ATP + AMP."""
    t = ATP_REST * (atp_pct / 100.0)
    a = K_AK / t
    d = (-1.0 + np.sqrt(1.0 - 4.0 * a * (t - A_TOTAL))) / (2.0 * a)
    m = K_AK * (d ** 2) / t
    return float(t), float(d), float(m)


# ------------------------------------------------------------------ shared world builders
def build_cell_right(
    x_center=2.85,
    tsc2_missing=False,
    rheb_gdp=False,
    mtor_dim=False,
    mtor_label="mTORC1 ON",
    show_raptor_tag=False,
    raptor_p=False,
    protein_thin=False,
):
    """Build the right-hand mTORC1 / lysosome half of the cell world with clear clearances."""
    g = VGroup()

    # Lysosome compartment: y in [-2.10, +1.00] (top=1.00, bottom=-2.10)
    lyso = RoundedRectangle(
        corner_radius=0.5, width=5.65, height=3.1,
        stroke_color=TEAL, stroke_width=4.0,
        fill_color=TEAL, fill_opacity=0.14,
    ).move_to([x_center, -0.55, 0])
    # Place Lysosome label in bottom-left of lysosome so protein arrow on the right stays clear
    lyso_lbl = T("Lysosome", size=26, color=TEAL).move_to([x_center - 1.65, -1.78, 0])
    g.add(lyso, lyso_lbl)

    # Top inputs cleanly above TSC2 / Rags
    gf = boxed_label("Growth factor", color=GREEN, size=24, pad=0.14).move_to([x_center - 1.55, 2.55, 0])
    aa = boxed_label("Amino acids", color=BLUE, size=24, pad=0.14).move_to([x_center + 1.55, 2.55, 0])
    g.add(gf, aa)

    # TSC2 sits cleanly ABOVE the lysosome top rim (y = 1.48 > 1.00)
    if tsc2_missing:
        tsc_box = DashedVMobject(
            RoundedRectangle(
                corner_radius=0.12, width=1.65, height=0.62,
                stroke_color=GREY, stroke_width=2.5,
            ),
            num_dashes=16,
        ).move_to([x_center - 1.55, 1.48, 0])
        tsc_txt = T("TSC2", size=24, color=GREY).move_to(tsc_box)
        tsc_miss = T("missing", size=24, color=GREY).next_to(tsc_box, RIGHT, buff=0.16)
        tsc_group = VGroup(tsc_box, tsc_txt, tsc_miss)
    else:
        tsc_group = boxed_label("TSC2", color=RED, size=24, pad=0.14).move_to([x_center - 1.55, 1.48, 0])
    g.add(tsc_group)

    gf_arrow = Arrow(
        gf.get_bottom() + DOWN * 0.06,
        tsc_group[0].get_top() + UP * 0.06,
        color=GREEN, stroke_width=3.2, buff=0.0, max_tip_length_to_length_ratio=0.22,
    )
    g.add(gf_arrow)

    # Rags sits cleanly ABOVE the lysosome top rim on the right (y = 1.48 > 1.00)
    rags = boxed_label("Rags", color=BLUE, size=24, pad=0.14).move_to([x_center + 1.55, 1.48, 0])
    aa_arrow = Arrow(
        aa.get_bottom() + DOWN * 0.06,
        rags.get_top() + UP * 0.06,
        color=BLUE, stroke_width=3.2, buff=0.0, max_tip_length_to_length_ratio=0.22,
    )
    g.add(rags, aa_arrow)

    # Rheb docked inside upper-left of lysosome (y = -0.10)
    rheb_col = GREY if rheb_gdp else GREEN
    rheb_txt = "Rheb-GDP" if rheb_gdp else "Rheb-GTP"
    rheb = boxed_label(rheb_txt, color=rheb_col, size=24, pad=0.14).move_to([x_center - 1.72, -0.10, 0])
    g.add(rheb)

    # mTORC1 complex docked on the right inside lysosome (sized wide enough for 'mTORC1 VETOED' / 'mTORC1 dimmed')
    mtor_col = GOLD
    mtor_fill = 0.09 if mtor_dim else 0.25
    mtor_stroke = 2.5 if mtor_dim else 3.8
    mtor_lbl_obj = T(mtor_label, size=26, color=mtor_col)
    mtor_w = max(3.05, mtor_lbl_obj.width + 0.55)
    mtor_box = RoundedRectangle(
        corner_radius=0.16, width=mtor_w, height=0.90,
        stroke_color=mtor_col, stroke_width=mtor_stroke,
        fill_color=mtor_col, fill_opacity=mtor_fill,
    ).move_to([x_center + 1.05, -0.10, 0])
    mtor_lbl_obj.move_to(mtor_box.get_center())
    g.add(mtor_box, mtor_lbl_obj)

    raptor_group = VGroup()
    if show_raptor_tag:
        rap = T("Raptor\n(mTORC1 subunit)", size=24, color=GOLD, line_spacing=0.85).move_to([x_center - 0.15, -1.15, 0])
        raptor_group.add(rap)
        g.add(rap)
    if raptor_p:
        p_badge = VGroup(
            Circle(radius=0.25, color=YELLOW, fill_color=YELLOW, fill_opacity=0.28, stroke_width=2.5),
            T("P", size=24, color=YELLOW, weight=BOLD),
        )
        p_badge[1].move_to(p_badge[0])
        p_badge.move_to(mtor_box.get_top() + UP * 0.31 + LEFT * 0.5)
        raptor_group.add(p_badge)
        g.add(p_badge)

    # Rheb -> mTORC1 link
    rheb_link = Arrow(
        rheb.get_right() + RIGHT * 0.08,
        mtor_box.get_left() + LEFT * 0.08,
        color=GREY if (rheb_gdp or mtor_dim) else GREEN,
        stroke_width=2.2 if (rheb_gdp or mtor_dim) else 3.8,
        buff=0.0, max_tip_length_to_length_ratio=0.28,
    )
    g.add(rheb_link)

    # Protein building output arrow straight down at x_center + 1.15 (clear of Lysosome, Raptor, & countdown ring!)
    out_w = 2.2 if protein_thin else 5.2
    out_col = GREY if protein_thin else GREEN
    prot_lbl = T("Protein building", size=24, color=out_col).move_to([x_center + 1.15, -2.65, 0])
    prot_start = np.array([x_center + 1.60, mtor_box.get_bottom()[1] - 0.12, 0])
    prot_end = np.array([x_center + 1.60, prot_lbl.get_top()[1] + 0.12, 0])
    prot_arr = Arrow(
        prot_start, prot_end,
        color=out_col, stroke_width=out_w, buff=0.0, max_tip_length_to_length_ratio=0.18,
    )
    prot_lbl.move_to([x_center + 1.15, -2.65, 0])
    g.add(prot_arr, prot_lbl)

    g.lyso = lyso
    g.lyso_lbl = lyso_lbl
    g.gf = gf
    g.aa = aa
    g.tsc2 = tsc_group
    g.gf_arrow = gf_arrow
    g.aa_arrow = aa_arrow
    g.rheb = rheb
    g.rags = rags
    g.mtor_box = mtor_box
    g.mtor_lbl = mtor_lbl_obj
    g.raptor_group = raptor_group
    g.rheb_link = rheb_link
    g.prot_arr = prot_arr
    g.prot_lbl = prot_lbl
    return g


def build_ampk_three_part(center=(-3.4, -1.1, 0), scale=1.0, active=False, flexed=False, has_p=False, label_subunits=False):
    """Build the schematic 3-subunit AMPK block (Alpha, Beta, Gamma) with generous box padding."""
    c = np.array(center, dtype=float)
    col = RED if active else ORANGE
    fill_op = 0.28 if active else 0.15

    # Boxes sized so labels fit inside with zero overflow and zero overlap even when flexed
    alpha_w, alpha_h = 2.05 * scale, 1.00 * scale
    gamma_w, gamma_h = 2.05 * scale, 1.00 * scale
    beta_w, beta_h = 2.95 * scale, 0.76 * scale

    dx = (1.20 if not flexed else 1.10) * scale
    dy = (0.58 if not flexed else 0.50) * scale
    by = (-0.48 if not flexed else -0.44) * scale

    alpha_box = RoundedRectangle(
        corner_radius=0.14, width=alpha_w, height=alpha_h,
        stroke_color=col, stroke_width=3.6 if active else 3.0,
        fill_color=col, fill_opacity=fill_op + (0.12 if active else 0.0),
    ).move_to(c + LEFT * dx + UP * dy)

    gamma_box = RoundedRectangle(
        corner_radius=0.14, width=gamma_w, height=gamma_h,
        stroke_color=col, stroke_width=3.0, fill_color=col, fill_opacity=fill_op,
    ).move_to(c + RIGHT * dx + UP * dy)

    beta_box = RoundedRectangle(
        corner_radius=0.14, width=beta_w, height=beta_h,
        stroke_color=col, stroke_width=3.0, fill_color=col, fill_opacity=fill_op,
    ).move_to(c + UP * by)

    sz = max(24, int(round(25 * scale)))
    if label_subunits:
        a_txt = T("Alpha\n(kinase)", size=sz, color=col, line_spacing=0.85).move_to(alpha_box)
        b_txt = T("Beta (scaffold)", size=sz, color=col).move_to(beta_box)
        g_txt = T("Gamma\n(sensor)", size=sz, color=col, line_spacing=0.85).move_to(gamma_box)
    else:
        a_txt = T("α", size=max(26, sz + 4), color=col).move_to(alpha_box)
        b_txt = T("β", size=max(26, sz + 4), color=col).move_to(beta_box)
        g_txt = T("γ", size=max(26, sz + 4), color=col).move_to(gamma_box)

    grp = VGroup(beta_box, alpha_box, gamma_box, b_txt, a_txt, g_txt)
    grp.alpha_box = alpha_box
    grp.beta_box = beta_box
    grp.gamma_box = gamma_box
    grp.alpha_txt = a_txt
    grp.beta_txt = b_txt
    grp.gamma_txt = g_txt

    if has_p:
        p_circ = Circle(radius=0.27, color=YELLOW, fill_color=YELLOW, fill_opacity=0.28, stroke_width=2.5)
        p_lbl = T("P", size=24, color=YELLOW, weight=BOLD).move_to(p_circ)
        p_badge = VGroup(p_circ, p_lbl).move_to(alpha_box.get_top() + UP * 0.36)
        grp.add(p_badge)
        grp.p_badge = p_badge
    else:
        grp.p_badge = None

    return grp


def make_flow_dots(path_fn, count=3, radius=0.11, color=GREEN, speed=0.65):
    """Create `count` evenly staggered biological signal/metabolite tokens moving along `path_fn(u in 0..1)`."""
    dots = VGroup()
    for k in range(count):
        d = Dot(radius=radius, color=color)
        d._t = k / count
        d.move_to(path_fn(d._t))

        def _upd(m, dt, fn=path_fn, sp=speed):
            sp_val = sp() if callable(sp) else sp
            m._t = (m._t + dt * sp_val) % 1.0
            m.move_to(fn(m._t))

        d.add_updater(_upd)
        dots.add(d)
    return dots


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "mTOR and AMPK: Reading Nutrients and Energy"
    TITLE = "AMPK: The Energy Veto"


class S01LinkAndHook(SpokenScene):
    def construct(self):
        cell_right = build_cell_right(x_center=2.85, mtor_label="mTORC1 ON")
        tag = scope_tag("schematic")

        aa_dots = make_flow_dots(
            lambda u: (cell_right.aa.get_bottom() + DOWN * 0.1) * (1.0 - u) + (cell_right.rags.get_top() + UP * 0.1) * u,
            count=3, radius=0.10, color=BLUE, speed=0.7,
        )
        gf_dots = make_flow_dots(
            lambda u: (cell_right.gf.get_bottom() + DOWN * 0.1) * (1.0 - u) + (cell_right.tsc2[0].get_top() + UP * 0.1) * u,
            count=3, radius=0.10, color=GREEN, speed=0.7,
        )
        prot_dots = make_flow_dots(
            lambda u: cell_right.prot_arr.get_start() * (1.0 - u) + cell_right.prot_arr.get_end() * u,
            count=3, radius=0.11, color=GREEN, speed=0.8,
        )

        self.play(FadeIn(cell_right.lyso, cell_right.lyso_lbl, tag), run_time=0.8)
        self.at("growth factors")
        self.play(
            FadeIn(cell_right.gf, cell_right.aa, cell_right.gf_arrow, cell_right.aa_arrow, cell_right.tsc2, cell_right.rheb, cell_right.rags),
            run_time=1.0,
        )
        self.add(aa_dots, gf_dots)
        self.at("at the lysosome")
        self.play(
            FadeIn(cell_right.mtor_box, cell_right.mtor_lbl, cell_right.rheb_link, cell_right.prot_arr, cell_right.prot_lbl),
            run_time=0.9,
        )
        self.add(prot_dots)

        # Left side: ATP fuel gauge appears and dips smoothly across the hook
        atp_lvl = ValueTracker(1.0)
        atp_dial = dial(atp_lvl, center=[-3.6, 1.4, 0], radius=1.28, label="Cellular ATP", color=ORANGE, fmt="{:.0f}%", scale=100.0, size=34)

        self.at("when its ATP")
        self.play(FadeIn(atp_dial), run_time=0.8)
        self.play(atp_lvl.animate.set_value(0.88), run_time=2.6, rate_func=linear)

        self.at("Running out")
        self.play(atp_lvl.animate.set_value(0.80), run_time=4.5, rate_func=linear)

        # Quiet 3-part AMPK block fades in on the left
        ampk_blk = build_ampk_three_part(center=(-3.6, -1.35, 0), scale=0.75, active=False)
        ampk_lbl = T("AMPK", size=30, color=ORANGE).next_to(ampk_blk, DOWN, buff=0.22)
        self.at("second master kinase")
        self.play(FadeIn(ampk_blk, ampk_lbl), run_time=1.0)
        self.play(atp_lvl.animate.set_value(0.76), run_time=4.5, rate_func=linear)
        self.finish()


class S02WhyAmp(SpokenScene):
    def construct(self):
        # Start with the fuel dial on the left holding ATP nearly steady (100% -> 98% -> 100%)
        atp_lvl = ValueTracker(1.0)
        atp_dial = dial(
            atp_lvl, center=[-3.8, 0.8, 0], radius=1.35,
            label="ATP gauge", color=GREEN, fmt="{:.0f}%", scale=100.0, size=34,
        )
        stead_lbl = T("Working cell holds ATP nearly steady", size=28, color=TEXT).move_to([1.5, 0.8, 0])
        self.play(FadeIn(atp_dial), run_time=0.7)

        self.at("holds ATP nearly steady")
        self.play(FadeIn(stead_lbl), atp_lvl.animate.set_value(0.98), run_time=2.8, rate_func=linear)
        self.play(atp_lvl.animate.set_value(0.99), run_time=2.8, rate_func=linear)

        # Computed chart on the left-center: fold change of ATP, ADP, AMP vs ATP remaining
        chart_title = T("Computed: adenylate kinase, K = 0.5", size=26, color=TEXT).move_to([-2.4, 3.2, 0])
        P = Plot(
            box=(-5.5, 0.7, -2.0, 1.3),
            xr=(0, 20), yr=(0, 9.0),
            xticks=[(0, "100%"), (10, "90%"), (20, "80%")],
            yticks=[(1, "×1"), (4, "×4"), (8, "×8")],
            xlabel="ATP remaining (% of rest)",
            ylabel="Fold change",
            size=24, label_size=24,
        )
        P.xlabel.shift(DOWN * 0.08)

        fn_atp = lambda drop: ak_concentrations(100.0 - drop)[0] / ATP_REST
        fn_adp = lambda drop: ak_concentrations(100.0 - drop)[1] / ADP_REST
        fn_amp = lambda drop: ak_concentrations(100.0 - drop)[2] / AMP_REST

        drop_tr = ValueTracker(0.0)
        curve_atp = P.live_curve(fn_atp, drop_tr, color=TEXT, width=5)
        curve_adp = P.live_curve(fn_adp, drop_tr, color=YELLOW, width=5)
        curve_amp = P.live_curve(fn_amp, drop_tr, color=ORANGE, width=6)

        dot_atp = P.dot(lambda: drop_tr.get_value(), lambda: fn_atp(drop_tr.get_value()), color=TEXT, ring=GREEN, radius=0.07)
        dot_adp = P.dot(lambda: drop_tr.get_value(), lambda: fn_adp(drop_tr.get_value()), color=YELLOW, ring=YELLOW, radius=0.07)
        dot_amp = P.dot(lambda: drop_tr.get_value(), lambda: fn_amp(drop_tr.get_value()), color=ORANGE, ring=RED, radius=0.08)

        # Live bar panel on the right
        bar_base_y = -2.0
        bar_max_h = 3.1
        bar_xs = [2.1, 3.55, 5.0]
        bar_names = [("ATP", TEXT), ("ADP", YELLOW), ("AMP", ORANGE)]
        bar_fns = [fn_atp, fn_adp, fn_amp]

        bar_mobs = VGroup()
        for x, (nm, col), fn in zip(bar_xs, bar_names, bar_fns):
            lbl = T(nm, size=26, color=col).move_to([x, bar_base_y - 0.38, 0])
            bar = always_redraw(lambda x=x, col=col, fn=fn: Rectangle(
                width=0.78,
                height=max(0.08, min(bar_max_h, (fn(drop_tr.get_value()) / 9.0) * bar_max_h)),
                color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.65,
            ).move_to([x, bar_base_y + max(0.08, min(bar_max_h, (fn(drop_tr.get_value()) / 9.0) * bar_max_h)) / 2, 0]))
            val_lbl = always_redraw(lambda x=x, col=col, fn=fn: M(
                f"×{fn(drop_tr.get_value()):.1f}", 24, col
            ).move_to([x, bar_base_y + max(0.08, min(bar_max_h, (fn(drop_tr.get_value()) / 9.0) * bar_max_h)) + 0.28, 0]))
            bar_mobs.add(lbl, bar, val_lbl)

        lamp_circ = Circle(radius=0.22, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([5.65, 3.2, 0])
        lamp_txt = T("LOW FUEL", size=24, color=GREY).next_to(lamp_circ, LEFT, buff=0.15)
        lamp = VGroup(lamp_circ, lamp_txt)

        self.at("adenylate kinase")
        self.play(
            FadeOut(atp_dial, stead_lbl),
            FadeIn(chart_title, P, bar_mobs, lamp),
            run_time=0.9,
        )
        self.add(curve_atp, curve_adp, curve_amp, dot_atp, dot_adp, dot_amp)

        # Equations placed over the LEFT half (x = -2.3), cleanly away from the right-side worked box!
        eq1_a = M("2 ADP", size=28, color=YELLOW)
        eq1_b = M("⇌ ATP", size=28, color=TEXT)
        eq1_c = M("+ AMP", size=28, color=ORANGE)
        eq1 = VGroup(eq1_a, eq1_b, eq1_c).arrange(RIGHT, buff=0.16).move_to([-2.3, 2.55, 0])

        self.at("balances")
        self.play(FadeIn(eq1_a), drop_tr.animate.set_value(0.5), run_time=0.6)
        self.at("against")
        self.play(FadeIn(eq1_b), drop_tr.animate.set_value(1.0), run_time=0.6)
        self.at("plus")
        self.play(FadeIn(eq1_c), drop_tr.animate.set_value(1.5), run_time=0.6)

        eq2_a = M("AMP ∝", size=28, color=ORANGE)
        eq2_b = M("ADP²", size=28, color=YELLOW)
        eq2_c = M("÷ ATP", size=28, color=TEXT)
        eq2 = VGroup(eq2_a, eq2_b, eq2_c).arrange(RIGHT, buff=0.16).move_to([-2.3, 1.98, 0])

        self.play(FadeIn(eq2_a), drop_tr.animate.set_value(2.0), run_time=1.8, rate_func=linear)
        self.at("squared")
        self.play(FadeIn(eq2_b), run_time=0.4)
        self.at("divided by")
        self.play(FadeIn(eq2_c), run_time=0.45)

        # Animate drop 2 -> 10% (90% ATP) on "When ATP dips"
        self.at("When ATP dips")
        self.play(drop_tr.animate.set_value(10.0), run_time=2.5, rate_func=linear)

        # Mark 90% ATP point with the lesson's worked numbers (ONLY after ten percent / fourfold spoken)
        p90 = P.pt(10.0, fn_amp(10.0))
        v90 = DashedLine(P.pt(10.0, 0), p90, color=GOLD, stroke_width=2.5)
        worked_box = boxed_label(
            "ATP 5.0 → 4.5 mM\nAMP 0.025 → 0.096 mM (≈ ×4)",
            color=GOLD, size=24, pad=0.14,
        ).move_to([3.55, 2.25, 0])
        if worked_box.get_right()[0] > 6.35:
            worked_box.shift(LEFT * (worked_box.get_right()[0] - 6.35))

        lamp_on_circ = Circle(radius=0.22, color=RED, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9).move_to(lamp_circ)
        lamp_on_txt = T("LOW FUEL", size=24, color=ORANGE, weight=BOLD).next_to(lamp_on_circ, LEFT, buff=0.15)

        self.at("almost fourfold")
        self.play(
            Create(v90),
            FadeIn(worked_box),
            ReplacementTransform(lamp_circ, lamp_on_circ),
            swap(lamp_txt, lamp_on_txt, run_time=0.4),
            run_time=0.6,
        )
        # Continue AMP bar to 80% ATP while holding worked_box for >= 2 s
        self.play(drop_tr.animate.set_value(20.0), run_time=1.6, rate_func=linear)
        self.finish()


class S03AmpkStructureSwitch(SpokenScene):
    def construct(self):
        lamp_circ = Circle(radius=0.22, color=RED, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9).move_to([5.65, 3.15, 0])
        lamp_txt = T("LOW FUEL", size=24, color=ORANGE, weight=BOLD).next_to(lamp_circ, LEFT, buff=0.15)
        amp_bar_bg = RoundedRectangle(corner_radius=0.08, width=0.8, height=3.4, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.12).move_to([-5.2, -0.2, 0])
        amp_fill = ValueTracker(0.75)
        amp_bar = always_redraw(lambda: Rectangle(
            width=0.72, height=3.2 * amp_fill.get_value(),
            color=ORANGE, fill_color=ORANGE, fill_opacity=0.78, stroke_width=0,
        ).move_to([-5.2, -1.85 + 1.6 * amp_fill.get_value(), 0]))
        amp_lbl = T("AMP", size=28, color=ORANGE).next_to(amp_bar_bg, DOWN, buff=0.2)

        self.play(FadeIn(lamp_circ, lamp_txt, amp_bar_bg, amp_bar, amp_lbl), run_time=0.7)
        self.play(amp_fill.animate.set_value(0.92), run_time=4.2, rate_func=linear)

        # Centered-left 3-subunit AMPK complex with generous padding for labels
        ampk = build_ampk_three_part(center=(-0.6, -0.35, 0), scale=1.22, active=False, label_subunits=True)
        # Pocket positioned cleanly to the right of Gamma, connected by a short line
        pocket_box = RoundedRectangle(corner_radius=0.12, width=1.85, height=0.65, stroke_color=ORANGE, stroke_width=2.5, fill_color=BG, fill_opacity=0.85).move_to([4.15, 0.25, 0])
        pocket_link = Line(ampk.gamma_box.get_right() + RIGHT * 0.05, pocket_box.get_left() + LEFT * 0.05, color=ORANGE, stroke_width=2.5)
        atp_tok = boxed_label("ATP", color=GREY, size=24, pad=0.10).move_to(pocket_box)
        pocket_lbl = T("Same pocket:\nAMP vs ATP", size=24, color=ORANGE, line_spacing=0.85).next_to(pocket_box, DOWN, buff=0.25)
        ratio_tag = T("reads AMP : ATP ratio", size=24, color=TEXT).next_to(pocket_box, UP, buff=0.25)
        tag = scope_tag("schematic")
        self.add(tag)

        self.at("three subunits")
        self.play(FadeIn(ampk.alpha_box, ampk.beta_box, ampk.gamma_box), run_time=0.9)

        self.at("Alpha carries")
        self.play(FadeIn(ampk.alpha_txt), Indicate(ampk.alpha_box, color=GOLD, scale_factor=1.04), run_time=1.0)

        self.at("beta holds")
        self.play(FadeIn(ampk.beta_txt), Indicate(ampk.beta_box, color=GOLD, scale_factor=1.04), run_time=1.5)

        self.at("gamma subunit")
        self.play(FadeIn(ampk.gamma_txt, pocket_link, pocket_box, atp_tok), run_time=1.2)

        # AMP tokens stream smoothly along a curved path below Beta (scaffold) into Gamma pocket
        amp_path = CubicBezier(
            np.array([-4.55, -0.75, 0]),
            np.array([-2.20, -3.10, 0]),
            np.array([2.20, -2.60, 0]),
            np.array([3.10, 0.25, 0]),
        )
        amp_stream = make_flow_dots(
            lambda u: amp_path.point_from_proportion(u),
            count=3, radius=0.12, color=ORANGE, speed=0.55,
        )
        tok_path = VMobject()
        tok_path.set_points_as_corners([
            *[amp_path.point_from_proportion(u) for u in np.linspace(0.0, 1.0, 40)],
            pocket_box.get_center(),
        ])
        self.at("compete")
        amp_tok = boxed_label("AMP", color=ORANGE, size=24, pad=0.10).move_to([-4.25, -0.75, 0])
        self.play(FadeIn(pocket_lbl), FadeOut(atp_tok), run_time=0.3)
        self.play(FadeIn(amp_tok), run_time=0.2)
        self.play(MoveAlongPath(amp_tok, tok_path), run_time=0.7)
        self.add(amp_stream)

        self.at("reads their ratio")
        self.play(FadeIn(ratio_tag), amp_fill.animate.set_value(0.98), run_time=1.0)

        # Alpha's Thr172 activation loop tag cleanly to the left of Alpha
        thr_lbl = T("Thr172", size=24, color=YELLOW).next_to(ampk.alpha_box, LEFT, buff=0.25)
        self.at("phosphate on alpha")
        self.play(FadeIn(thr_lbl), run_time=1.4)

        # LKB1 steady block above alpha places yellow P onto alpha
        lkb1 = boxed_label("LKB1 (always active)", color=TEAL, size=26, pad=0.16).move_to([ampk.alpha_box.get_center()[0], 2.55, 0])
        p_circ = Circle(radius=0.27, color=YELLOW, fill_color=YELLOW, fill_opacity=0.28, stroke_width=3)
        p_txt = T("P", size=26, color=YELLOW, weight=BOLD).move_to(p_circ)
        p_badge = VGroup(p_circ, p_txt).move_to(lkb1.get_bottom() + DOWN * 0.35)

        self.at("called LKB1")
        self.play(FadeIn(lkb1, p_badge), run_time=0.6)
        self.play(p_badge.animate.move_to(ampk.alpha_box.get_top() + UP * 0.36), run_time=1.5)
        self.finish()


class S04AmpProtectsAndBoosts(SpokenScene):
    def construct(self):
        ampk = build_ampk_three_part(center=(-0.6, -0.45, 0), scale=1.22, active=False, flexed=False, has_p=True, label_subunits=True)
        lkb1 = boxed_label("LKB1 (always active)", color=TEAL, size=26, pad=0.16).move_to([ampk.alpha_box.get_center()[0], 2.55, 0])
        thr_lbl = T("Thr172", size=24, color=YELLOW).next_to(ampk.alpha_box, LEFT, buff=0.25)
        pocket_box = RoundedRectangle(corner_radius=0.12, width=1.65, height=0.65, stroke_color=ORANGE, stroke_width=2.5, fill_color=BG, fill_opacity=0.85).move_to([3.95, 0.15, 0])
        pocket_link = Line(ampk.gamma_box.get_right() + RIGHT * 0.05, pocket_box.get_left() + LEFT * 0.05, color=ORANGE, stroke_width=2.5)
        atp_tok = boxed_label("ATP", color=GREY, size=24, pad=0.10).move_to(pocket_box)
        status_lbl = T("AMPK quiet", size=30, color=ORANGE).move_to([-0.6, -2.75, 0])
        tag = scope_tag("schematic")

        self.add(ampk, lkb1, thr_lbl, pocket_link, pocket_box, atp_tok, status_lbl, tag)

        # Phosphatase approaches P from above-right (clear of Alpha & Gamma boxes!)
        phosph = boxed_label("Phosphatase", color=GREY, size=26, pad=0.15).move_to([3.65, 2.35, 0])
        p_target = ampk.p_badge.get_center()
        self.at("stay quiet")
        self.play(FadeIn(phosph), run_time=0.8)
        self.play(phosph.animate.move_to(p_target + RIGHT * 1.45 + UP * 0.45), run_time=2.0)

        self.at("phosphatases keep stripping")
        self.play(
            ampk.p_badge.animate.shift(UP * 0.5 + RIGHT * 0.6).set_opacity(0.0),
            phosph.animate.move_to([3.65, 2.35, 0]),
            run_time=1.8,
        )
        new_p = VGroup(
            Circle(radius=0.27, color=YELLOW, fill_color=YELLOW, fill_opacity=0.28, stroke_width=2.5),
            T("P", size=24, color=YELLOW, weight=BOLD),
        )
        new_p[1].move_to(new_p[0])
        new_p.move_to(lkb1.get_bottom() + DOWN * 0.35)
        self.play(FadeIn(new_p), run_time=0.5)
        self.play(new_p.animate.move_to(p_target), run_time=1.5)

        # AMP docks into Gamma pocket, displacing ATP cleanly
        amp_tok = boxed_label("AMP", color=ORANGE, size=24, pad=0.10).move_to([5.4, 0.15, 0])
        self.at("When AMP binds")
        self.play(FadeOut(atp_tok), FadeIn(amp_tok), run_time=0.4)
        self.play(amp_tok.animate.move_to(pocket_box.get_center()), run_time=0.9)

        # AMPK subunits flex inward cleanly without overlapping boxes, shielding P
        ampk_flex = build_ampk_three_part(center=(-0.6, -0.45, 0), scale=1.22, active=False, flexed=True, has_p=False, label_subunits=True)
        shield_lbl = T("Shape shifts:\nP shielded", size=26, color=YELLOW, line_spacing=0.85).next_to(ampk_flex.alpha_box, LEFT, buff=0.28)
        new_pocket_link = Line(ampk_flex.gamma_box.get_right() + RIGHT * 0.05, pocket_box.get_left() + LEFT * 0.05, color=ORANGE, stroke_width=2.5)

        self.at("AMPK shifts")
        self.play(
            ReplacementTransform(ampk.alpha_box, ampk_flex.alpha_box),
            ReplacementTransform(ampk.beta_box, ampk_flex.beta_box),
            ReplacementTransform(ampk.gamma_box, ampk_flex.gamma_box),
            ReplacementTransform(ampk.alpha_txt, ampk_flex.alpha_txt),
            ReplacementTransform(ampk.beta_txt, ampk_flex.beta_txt),
            ReplacementTransform(ampk.gamma_txt, ampk_flex.gamma_txt),
            ReplacementTransform(pocket_link, new_pocket_link),
            new_p.animate.move_to(ampk_flex.alpha_box.get_top() + UP * 0.36),
            swap(thr_lbl, shield_lbl, run_time=0.6),
            run_time=1.3,
        )

        # Phosphatase approaches shield and bounces off harmlessly
        self.at("cannot easily remove")
        self.play(phosph.animate.move_to(new_p.get_center() + RIGHT * 1.45 + UP * 0.45), run_time=1.0)
        self.play(phosph.animate.move_to([3.85, 2.35, 0]), run_time=1.1)
        self.play(phosph.animate.set_opacity(0.45), run_time=0.6)

        # Direct allosteric boost: Alpha flares bright orange-red ("AMPK ON")
        ampk_on = build_ampk_three_part(center=(-0.6, -0.45, 0), scale=1.22, active=True, flexed=True, has_p=False, label_subunits=True)
        status_on = T("AMPK ON", size=30, color=RED, weight=BOLD).move_to([-0.6, -2.75, 0])
        self.at("direct allosteric boost")
        self.play(
            ReplacementTransform(ampk_flex.alpha_box, ampk_on.alpha_box),
            ReplacementTransform(ampk_flex.beta_box, ampk_on.beta_box),
            ReplacementTransform(ampk_flex.gamma_box, ampk_on.gamma_box),
            ReplacementTransform(ampk_flex.alpha_txt, ampk_on.alpha_txt),
            ReplacementTransform(ampk_flex.beta_txt, ampk_on.beta_txt),
            ReplacementTransform(ampk_flex.gamma_txt, ampk_on.gamma_txt),
            run_time=1.3,
        )
        self.at("strongly on")
        self.play(swap(status_lbl, status_on, run_time=0.7))
        self.finish()


def build_predict_frame(ampk_active=True, tsc2_missing=True):
    """Exact predict frame shared between end of S05PredictSetup and S06Pause.backdrop()."""
    cell_right = build_cell_right(
        x_center=2.85,
        tsc2_missing=tsc2_missing,
        rheb_gdp=False,
        mtor_dim=False,
        mtor_label="mTORC1 ON",
    )
    tsc_sub = T("TSC2 =\nsubunit of TSC", size=24, color=GREY, line_spacing=0.85).move_to([-0.75, 2.02, 0])

    atp_lvl = ValueTracker(0.80 if ampk_active else 1.0)
    atp_dial = dial(
        atp_lvl, center=[-3.6, 1.4, 0], radius=1.1,
        label="ATP", color=RED if ampk_active else GREEN, fmt="{:.0f}%", scale=100.0, size=32,
    )
    ampk_blk = build_ampk_three_part(
        center=(-3.6, -1.25, 0), scale=0.78, active=ampk_active, flexed=ampk_active, has_p=ampk_active,
    )
    ampk_lbl = T("AMPK ON" if ampk_active else "AMPK quiet", size=30, color=RED if ampk_active else ORANGE, weight=BOLD if ampk_active else NORMAL).next_to(ampk_blk, DOWN, buff=0.22)
    tag = scope_tag("schematic")
    return VGroup(cell_right, tsc_sub, atp_dial, ampk_blk, ampk_lbl, tag)


class S05PredictSetup(SpokenScene):
    def construct(self):
        cell_right = build_cell_right(x_center=2.85, tsc2_missing=False, rheb_gdp=False, mtor_dim=False, mtor_label="mTORC1 ON")
        tsc_sub = T("TSC2 =\nsubunit of TSC", size=24, color=GREY, line_spacing=0.85).move_to([-0.75, 2.02, 0])

        atp_lvl = ValueTracker(1.0)
        atp_dial = dial(atp_lvl, center=[-3.6, 1.4, 0], radius=1.1, label="ATP", color=GREEN, fmt="{:.0f}%", scale=100.0, size=32)
        ampk_blk = build_ampk_three_part(center=(-3.6, -1.25, 0), scale=0.78, active=False)
        ampk_lbl = T("AMPK quiet", size=30, color=ORANGE).next_to(ampk_blk, DOWN, buff=0.22)
        tag = scope_tag("schematic")

        # Continuous active signaling and protein-building flow while mTORC1 is ON
        gf_dots = make_flow_dots(
            lambda u: (cell_right.gf.get_bottom() + DOWN * 0.08) * (1.0 - u) + (cell_right.tsc2[0].get_top() + UP * 0.08) * u,
            count=2, radius=0.09, color=GREEN, speed=0.65,
        )
        aa_dots = make_flow_dots(
            lambda u: (cell_right.aa.get_bottom() + DOWN * 0.08) * (1.0 - u) + (cell_right.rags.get_top() + UP * 0.08) * u,
            count=2, radius=0.09, color=BLUE, speed=0.65,
        )
        prot_dots = make_flow_dots(
            lambda u: cell_right.prot_arr.get_start() * (1.0 - u) + cell_right.prot_arr.get_end() * u,
            count=3, radius=0.11, color=GREEN, speed=0.75,
        )

        self.at("both gauges")
        self.play(FadeIn(cell_right, atp_dial, ampk_blk, ampk_lbl, tag), run_time=1.0)
        self.add(gf_dots, aa_dots, prot_dots)

        self.at("Growth factors")
        self.play(Indicate(cell_right.gf, color=GREEN, scale_factor=1.06), Indicate(cell_right.aa, color=BLUE, scale_factor=1.06), run_time=1.2)

        ampk_on_blk = build_ampk_three_part(center=(-3.6, -1.25, 0), scale=0.78, active=True, flexed=True, has_p=True)
        ampk_on_lbl = T("AMPK ON", size=30, color=RED, weight=BOLD).next_to(ampk_on_blk, DOWN, buff=0.22)

        self.at("ATP dips")
        self.play(atp_lvl.animate.set_value(0.80), run_time=1.2, rate_func=linear)
        self.at("AMPK switches on")
        self.play(
            ReplacementTransform(ampk_blk, ampk_on_blk),
            swap(ampk_lbl, ampk_on_lbl, run_time=0.6),
            run_time=1.0,
        )

        # Tentative veto route arrow toward TSC2 (cleanly from AMPK right to TSC2 left)
        veto_arr = Arrow(
            ampk_on_blk.get_right() + RIGHT * 0.12,
            cell_right.tsc2.get_left() + LEFT * 0.14,
            color=ORANGE, stroke_width=3.5, buff=0.0, max_tip_length_to_length_ratio=0.16,
        )
        self.at("One veto route")
        self.play(Create(veto_arr), FadeIn(tsc_sub), run_time=1.3)

        # Test it: TSC2 is lost -> fades to dashed grey outline, Rheb stays GTP, mTORC1 stays lit (NO ANSWER!)
        self.at("lost TSC2")
        cell_missing = build_cell_right(x_center=2.85, tsc2_missing=True, rheb_gdp=False, mtor_dim=False, mtor_label="mTORC1 ON")
        self.play(
            ReplacementTransform(cell_right.tsc2, cell_missing.tsc2),
            FadeOut(veto_arr),
            run_time=1.5,
        )

        q_banner = question_card(
            "No TSC2, ATP falling: can AMPK still turn mTORC1 down?",
            y=3.28, size=30, max_w=12.0,
        )
        self.at("Can AMPK still")
        self.play(FadeIn(q_banner), run_time=0.9)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "No TSC2, ATP falling: can AMPK still turn mTORC1 down?"
    CARD = {"y": 3.28, "max_w": 12.0, "size": 30}
    RING_AT = (6.05, -2.95, 0)
    SECONDS = 4.5

    def backdrop(self):
        bf = build_predict_frame(ampk_active=True, tsc2_missing=True)
        bf[-1].move_to([-5.5, -3.2, 0])
        return bf


class S07VetoReveal(SpokenScene):
    def construct(self):
        cell_right = build_cell_right(x_center=2.85, tsc2_missing=True, rheb_gdp=False, mtor_dim=False, mtor_label="mTORC1 ON")
        ampk_blk = build_ampk_three_part(center=(-3.6, -1.4, 0), scale=0.78, active=True, flexed=True, has_p=True)
        ampk_lbl = T("AMPK ON", size=30, color=RED, weight=BOLD).next_to(ampk_blk, DOWN, buff=0.22)
        q_banner = question_card("No TSC2, ATP falling: can AMPK still turn mTORC1 down?", y=3.28, size=30, max_w=12.0)
        tag = scope_tag("schematic")

        # Continuous protein-building tokens (initially normal speed, slow after mTORC1 dims)
        prot_speed = ValueTracker(0.7)
        prot_dots = make_flow_dots(
            lambda u: cell_right.prot_arr.get_start() * (1.0 - u) + cell_right.prot_arr.get_end() * u,
            count=3, radius=0.11, color=GREEN, speed=lambda: prot_speed.get_value(),
        )

        self.add(cell_right, ampk_blk, ampk_lbl, q_banner, tag, prot_dots)
        self.play(FadeOut(q_banner), run_time=0.7)

        # Inset 'Normal cell' (top-left) showing AMPK -> P on TSC2 -> Rheb-GDP
        inset_box = RoundedRectangle(corner_radius=0.16, width=5.6, height=2.9, stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to([-3.4, 1.85, 0])
        inset_title = T("Normal cell", size=26, color=TEXT).move_to([inset_box.get_left()[0] + 1.05, inset_box.get_top()[1] - 0.35, 0])
        in_ampk = boxed_label("AMPK", color=RED, size=24, pad=0.12).move_to([-5.25, 1.75, 0])
        in_tsc = boxed_label("TSC2", color=RED, size=24, pad=0.12).move_to([-3.45, 1.75, 0])
        in_rheb_gtp = boxed_label("Rheb-GTP", color=GREEN, size=24, pad=0.12).move_to([-1.6, 1.75, 0])
        in_rheb_gdp = boxed_label("Rheb-GDP", color=GREY, size=24, pad=0.12).move_to([-1.6, 1.75, 0])
        in_arr1 = Arrow(in_ampk.get_right() + RIGHT * 0.08, in_tsc.get_left() + LEFT * 0.08, color=ORANGE, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.25)
        in_arr2 = Arrow(in_tsc.get_right() + RIGHT * 0.08, in_rheb_gtp.get_left() + LEFT * 0.08, color=RED, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.25)
        in_p = VGroup(
            Circle(radius=0.25, color=YELLOW, fill_color=YELLOW, fill_opacity=0.28, stroke_width=2.5),
            T("P", size=24, color=YELLOW, weight=BOLD),
        )
        in_p[1].move_to(in_p[0])
        in_p.move_to(in_tsc.get_top() + UP * 0.34)
        brake_note = T("TSC brake ON", size=24, color=RED).move_to([-3.4, 0.85, 0])

        self.at("two separate")
        self.play(FadeIn(inset_box, inset_title, in_ampk, in_tsc, in_rheb_gtp, in_arr1, in_arr2), run_time=0.9)

        self.at("Normally")
        self.play(FadeIn(in_p, brake_note), run_time=1.8)

        self.at("draining")
        self.play(ReplacementTransform(in_rheb_gtp, in_rheb_gdp), run_time=2.0)

        # Main frame: Raptor label neatly inside lysosome bottom-center, clear of Lysosome & prot_arr
        raptor_tag = T("Raptor\n(mTORC1 subunit)", size=24, color=GOLD, line_spacing=0.85).move_to([cell_right.lyso.get_center()[0] - 0.15, -1.15, 0])
        self.at("Raptor")
        self.play(FadeIn(raptor_tag), run_time=1.2)

        # Bright amber arc from AMPK directly to mTORC1 left edge (clear of Raptor text)
        arc = CurvedArrow(
            ampk_blk.get_right() + RIGHT * 0.12,
            cell_right.mtor_box.get_left() + LEFT * 0.12 + DOWN * 0.25,
            angle=0.18, color=ORANGE, stroke_width=4.5,
        )
        arc_dots = make_flow_dots(
            lambda u: arc.point_from_proportion(u),
            count=3, radius=0.11, color=ORANGE, speed=0.55,
        )
        rap_p = VGroup(
            Circle(radius=0.25, color=YELLOW, fill_color=YELLOW, fill_opacity=0.30, stroke_width=2.5),
            T("P", size=24, color=YELLOW, weight=BOLD),
        )
        rap_p[1].move_to(rap_p[0])
        rap_p.move_to(cell_right.mtor_box.get_top() + UP * 0.31 + LEFT * 0.5)

        self.at("complex directly")
        self.play(Create(arc), run_time=1.4)
        self.play(FadeIn(rap_p), run_time=0.8)
        self.add(arc_dots)

        # mTORC1 dims partway and protein-building arrow thins (never vanishes!)
        mtor_dim_lbl = T("mTORC1 dimmed", size=26, color=GOLD).move_to(cell_right.mtor_box)
        thin_arr = Arrow(
            cell_right.prot_arr.get_start(),
            cell_right.prot_arr.get_end(),
            color=GREY, stroke_width=2.2, buff=0.0, max_tip_length_to_length_ratio=0.18,
        )
        thin_lbl = T("Protein building (dimmed)", size=24, color=GREY).move_to(cell_right.prot_lbl)

        self.at("dim protein building")
        self.play(
            cell_right.mtor_box.animate.set_fill(GOLD, opacity=0.09).set_stroke(GOLD, width=2.2),
            swap(cell_right.mtor_lbl, mtor_dim_lbl, run_time=0.6),
            ReplacementTransform(cell_right.prot_arr, thin_arr),
            swap(cell_right.prot_lbl, thin_lbl, run_time=0.6),
            prot_speed.animate.set_value(0.25),
            prot_dots.animate.set_color(GREY),
            run_time=1.4,
        )
        self.finish()


class S08BudgetShift(SpokenScene):
    def construct(self):
        # Active AMPK on the far left; two custom framed schematic panels on the right (no shifted TwoPanel!)
        ampk_blk = build_ampk_three_part(center=(-4.85, 0.2, 0), scale=0.75, active=True, flexed=True, has_p=True)
        ampk_lbl = T("AMPK ON", size=30, color=RED, weight=BOLD).next_to(ampk_blk, DOWN, buff=0.22)
        tag = scope_tag("schematic")

        lp_frame = RoundedRectangle(corner_radius=0.18, width=4.35, height=5.85, stroke_color=RED, stroke_width=2.5).move_to([-0.55, 0.25, 0])
        lp_head = T("Cut spending (schematic)", size=26, color=RED).move_to([-0.55, 2.75, 0])
        rp_frame = RoundedRectangle(corner_radius=0.18, width=4.35, height=5.85, stroke_color=GREEN, stroke_width=2.5).move_to([4.05, 0.25, 0])
        rp_head = T("Raise income (schematic)", size=26, color=GREEN).move_to([4.05, 2.75, 0])

        self.play(FadeIn(ampk_blk, ampk_lbl, lp_frame, lp_head, rp_frame, rp_head, tag), run_time=0.9)

        # Left panel (x = -0.55, width = 4.35 -> inner x in [-2.55, +1.45])
        lc_x = -0.55
        fat_chol = boxed_label("Fat & cholesterol\nsynthesis", color=RED, size=24, box=(3.2, 0.96), pad=0.12).move_to([lc_x + 0.15, 1.85, 0])
        inhibit_bar = Line(
            ampk_blk.get_right() + RIGHT * 0.14,
            fat_chol.get_left() + LEFT * 0.12,
            color=RED, stroke_width=4,
        )
        t_head = Line(
            fat_chol.get_left() + LEFT * 0.12 + UP * 0.18,
            fat_chol.get_left() + LEFT * 0.12 + DOWN * 0.18,
            color=RED, stroke_width=4,
        )

        self.at("cuts spending")
        self.play(FadeIn(fat_chol), Create(inhibit_bar), Create(t_head), run_time=1.0)

        # ACC -> malonyl-CoA -| fatty acid entry (inside left panel cleanly!)
        acc_box = boxed_label("ACC", color=YELLOW, size=24, pad=0.12).move_to([lc_x - 1.25, 0.72, 0])
        mal_box = boxed_label("malonyl-CoA", color=RED, size=24, pad=0.12).move_to([lc_x + 0.78, 0.72, 0])
        arr_acc_mal = Arrow(acc_box.get_right() + RIGHT * 0.06, mal_box.get_left() + LEFT * 0.06, color=YELLOW, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.25)

        mito = RoundedRectangle(corner_radius=0.45, width=3.45, height=1.25, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.12).move_to([lc_x, -1.15, 0])
        mito_lbl = T("Mitochondrion", size=24, color=ORANGE).move_to(mito.get_center() + DOWN * 0.22)
        door = Line(mito.get_top() + LEFT * 0.45, mito.get_top() + RIGHT * 0.45, color=RED, stroke_width=6)
        block_bar = Line(mal_box.get_bottom() + DOWN * 0.06, door.get_center() + UP * 0.16, color=RED, stroke_width=3)
        block_t = Line(door.get_center() + UP * 0.16 + LEFT * 0.16, door.get_center() + UP * 0.16 + RIGHT * 0.16, color=RED, stroke_width=3)

        self.at("first")
        self.play(FadeIn(acc_box), run_time=0.7)
        self.at("makes a blocker")
        self.play(Create(arr_acc_mal), FadeIn(mal_box), run_time=0.9)
        self.at("into mitochondria")
        self.play(FadeIn(mito, mito_lbl, door), Create(block_bar), Create(block_t), run_time=1.0)

        # Switching ACC off opens the door outward; fatty acids enter mitochondrion -> Burn fat
        acc_off = boxed_label("ACC OFF", color=GREY, size=24, pad=0.12).move_to(acc_box)
        fa_arr = Arrow(
            [lc_x, 0.12, 0],
            [lc_x, mito.get_top()[1] - 0.12, 0],
            color=GREEN, stroke_width=4.5, buff=0, max_tip_length_to_length_ratio=0.25,
        )
        burn_lbl = T("Burn fat", size=26, color=GREEN, weight=BOLD).move_to([lc_x, -2.18, 0])

        fa_dots = make_flow_dots(
            lambda u: fa_arr.get_start() * (1.0 - u) + fa_arr.get_end() * u,
            count=3, radius=0.10, color=GREEN, speed=0.85,
        )

        self.at("opens that door")
        self.play(
            ReplacementTransform(acc_box, acc_off),
            FadeOut(arr_acc_mal, mal_box, block_bar, block_t),
            door.animate.rotate(PI / 2.6, about_point=door.get_start()).set_color(GREEN),
            run_time=1.0,
        )
        self.at("burned for fuel")
        self.play(Create(fa_arr), FadeIn(burn_lbl), run_time=0.9)
        self.add(fa_dots)

        # Right panel (x = +4.05, width = 4.35)
        rc_x = 4.05
        pm_line = Line([rc_x - 1.85, 1.75, 0], [rc_x + 1.85, 1.75, 0], color=TEAL, stroke_width=5)
        pm_lbl = T("Muscle cell surface", size=24, color=TEAL).next_to(pm_line, UP, buff=0.14)
        glut1 = boxed_label("GLUT4", color=BLUE, size=24, pad=0.1).move_to([rc_x - 0.95, -0.25, 0])
        glut2 = boxed_label("GLUT4", color=BLUE, size=24, pad=0.1).move_to([rc_x + 0.95, -0.25, 0])
        income_lbl = T("Glucose uptake\n(Raise income)", size=26, color=GREEN, line_spacing=0.85).move_to([rc_x, -1.75, 0])

        self.at("In muscle")
        self.play(Create(pm_line), FadeIn(pm_lbl, glut1, glut2), run_time=0.9)

        self.at("glucose transporters")
        self.play(
            glut1.animate.move_to([rc_x - 0.95, 1.32, 0]),
            glut2.animate.move_to([rc_x + 0.95, 1.32, 0]),
            run_time=1.1,
        )

        # Glucose arrows pass neatly below GLUT4
        glc_arr1 = Arrow([rc_x - 0.95, 0.92, 0], [rc_x - 0.95, -0.55, 0], color=GREEN, stroke_width=4.0, buff=0, max_tip_length_to_length_ratio=0.22)
        glc_arr2 = Arrow([rc_x + 0.95, 0.92, 0], [rc_x + 0.95, -0.55, 0], color=GREEN, stroke_width=4.0, buff=0, max_tip_length_to_length_ratio=0.22)

        glc_dots1 = make_flow_dots(
            lambda u: glc_arr1.get_start() * (1.0 - u) + glc_arr1.get_end() * u,
            count=3, radius=0.10, color=GREEN, speed=0.85,
        )
        glc_dots2 = make_flow_dots(
            lambda u: glc_arr2.get_start() * (1.0 - u) + glc_arr2.get_end() * u,
            count=3, radius=0.10, color=GREEN, speed=0.85,
        )

        self.at("raise fuel income")
        self.play(Create(glc_arr1), Create(glc_arr2), FadeIn(income_lbl), run_time=0.9)
        self.add(glc_dots1, glc_dots2)
        self.finish()


class S09ScopeClose(SpokenScene):
    def construct(self):
        cell_right = build_cell_right(
            x_center=2.85,
            tsc2_missing=False,
            rheb_gdp=True,
            mtor_dim=True,
            mtor_label="mTORC1 VETOED",
            raptor_p=True,
            protein_thin=True,
        )
        ampk_blk = build_ampk_three_part(center=(-3.55, 0.35, 0), scale=0.82, active=True, flexed=True, has_p=True)
        ampk_lbl = T("AMPK ON", size=30, color=RED, weight=BOLD).next_to(ampk_blk, DOWN, buff=0.22)

        save_tag = boxed_label("Fat burn ↑  |  Glucose uptake ↑", color=GREEN, size=24, pad=0.14).move_to([-3.55, -2.15, 0])

        # Route veto arrows cleanly ABOVE and BELOW Rheb-GDP so neither crosses Rheb-GDP!
        veto_tsc = CurvedArrow(
            ampk_blk.get_right() + RIGHT * 0.14,
            cell_right.tsc2.get_left() + LEFT * 0.14,
            angle=-0.18, color=RED, stroke_width=3.5,
        )
        veto_rap = CurvedArrow(
            ampk_blk.beta_box.get_right() + RIGHT * 0.12,
            cell_right.mtor_box.get_bottom() + LEFT * 0.35 + DOWN * 0.12,
            angle=0.28, color=ORANGE, stroke_width=3.5,
        )
        tag = scope_tag("schematic")

        # Continuous biological veto signals & both growth yeses arriving
        prot_dots = make_flow_dots(
            lambda u: cell_right.prot_arr.get_start() * (1.0 - u) + cell_right.prot_arr.get_end() * u,
            count=2, radius=0.08, color=GREY, speed=0.28,
        )
        tsc_dots = make_flow_dots(
            lambda u: veto_tsc.point_from_proportion(u),
            count=3, radius=0.11, color=RED, speed=0.55,
        )
        rap_dots = make_flow_dots(
            lambda u: veto_rap.point_from_proportion(u),
            count=3, radius=0.11, color=ORANGE, speed=0.55,
        )
        gf_dots = make_flow_dots(
            lambda u: (cell_right.gf.get_bottom() + DOWN * 0.08) * (1.0 - u) + (cell_right.tsc2[0].get_top() + UP * 0.08) * u,
            count=2, radius=0.09, color=GREEN, speed=0.60,
        )
        aa_dots = make_flow_dots(
            lambda u: (cell_right.aa.get_bottom() + DOWN * 0.08) * (1.0 - u) + (cell_right.rags.get_top() + UP * 0.08) * u,
            count=2, radius=0.09, color=BLUE, speed=0.60,
        )

        self.play(FadeIn(cell_right, ampk_blk, ampk_lbl, save_tag, veto_tsc, veto_rap, tag), run_time=1.0)
        self.add(prot_dots, tsc_dots, rap_dots, gf_dots, aa_dots)

        # Build Gamma note piece by piece as spoken
        g_note1 = T("AMP:ATP ratio", size=24, color=ORANGE)
        g_note2 = T("(+ ADP & calcium inputs)", size=24, color=YELLOW)
        g_note = VGroup(g_note1, g_note2).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([-3.55, 2.55, 0])

        self.at("Gamma senses")
        self.play(FadeIn(g_note1), run_time=0.8)
        self.at("ADP and calcium")
        self.play(FadeIn(g_note2), run_time=0.9)

        self.at("overrides both")
        self.play(
            Indicate(veto_tsc, color=YELLOW, scale_factor=1.03),
            Indicate(veto_rap, color=YELLOW, scale_factor=1.03),
            run_time=1.4,
        )

        self.at("Protecting cellular energy")
        self.play(Indicate(ampk_lbl, color=ORANGE, scale_factor=1.05), run_time=1.2)
        self.finish()


class S10End(EndCard):
    LINE = "AMPK reads rising AMP to conserve energy and veto mTORC1."
