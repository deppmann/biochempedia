"""When cGMP Rises: Arteries and Drugs — STEMhop Chapter 2 Explainer.

COLOUR MAP (one colour per concept, carried across every scene):
- BG          #0F1117   Dark slate ground (from bp_style)
- TEXT        #E8EAF0   Primary labels, drug blocker (Sildenafil), actin filaments
- CGMP_COL    #2DD4BF   cGMP messenger, cGMP gauge, cGMP curve, PKG activation
- SGC_COL     #34D399   Soluble guanylyl cyclase (sGC), intact endothelium, synthesis
- PDE_COL     #F43F5E   Phosphodiesterases (PDE5 in muscle, PDE6 in rod), breakdown
- NO_COL      #C084FC   Nitric oxide (NO) gas & nitroglycerin-derived NO
- ACH_COL     #FACC15   Acetylcholine (ACh)
- CA_COL      #FB923C   Calcium (Ca2+) & endothelial NO synthase
- MEMB_COL    #64748B   Vessel membranes & structural borders
- GMP_COL     #8B93A1   Inactive hydrolyzed GMP particles

CARRIED PICTURE OF THE WORLD:
An artery-wall cross-section (lumen at top, single-cell endothelium beneath,
vascular smooth muscle cell below holding sGC, a live teal cGMP gauge, PKG,
contractile filaments, and rose PDE5) plus a rod-cell echo for contrast.

SCENE-BY-SCENE COMPUTED CHANGES:
- s00_title:              Standard STEMhop TitleCard (2.0 s).
- s01_hook:               Left rod inset gauge + cGMP hydrolysis dots computed down (0.86 -> 0.16) as light hits; dissolves so artery wall fills frame with low cGMP gauge and sliding taut filaments.
- s02_endothelium_puzzle: Paired artery rings (seed-7 ACh cloud); intact ring radius widens via relaxation tracker (1.0 -> 1.44) while rubbed ring stays at 1.0.
- s03_no_diffusion:       ACh wave docks, Ca2+ bar & 12 ions rise and converge onto NO synthase, seed-7 2D random-walk NO dots diffuse across both membranes and decay exponentially (exp(-age/tau)).
- s04_cgmp_rise:          NO stream docks in sGC heme pocket; ODE dc/dt = k_syn - k_deg*c drives cGMP gauge (0.20 -> 0.90), cGMP stream, PKG glow, filament lengthening, lumen widening.
- s05_predict_q:          NO fades, sGC dims, cGMP holds high; left rod inset animates PDE6 hydrolysis dropping rod cGMP (0.78 -> 0.18); top question card enters.
- s06_predict_pause:      PredictPause holds s05 world + question card while countdown ring empties over 4.5 s.
- s07_predict_reveal:     PDE5 brightens/labels, converts cGMP to fading GMP; ODE decays cGMP (0.85 -> 0.20 baseline), filaments shorten, lumen narrows.
- s08_drugs:              Nitroglycerin plume drives sGC synthesis ODE up; Sildenafil wedge plugs PDE5 pocket, slowing ODE hydrolysis rate (k_deg * 0.28) on next NO burst.
- s09_rod_contrast:       TwoPanel simultaneous ODEs: rod PDE6 drops cGMP (0.85 -> 0.18) while muscle sGC/NO raises cGMP (0.20 -> 0.85) with opposite dot fluxes.
- s10_takehome:           Plot integrates dc/dt = s(t) - k_deg*c for normal vs PDE5-blocked burst (taller, longer teal curve + shaded areas) synced to gauge and capped PDE5.
- s11_end:                Standard STEMhop EndCard with exact take-home line.
"""

from bp_parts import *

# ------------------------------------------------------------------ Colour map
CGMP_COL = "#2DD4BF"   # teal: cGMP
SGC_COL = "#34D399"    # emerald: soluble guanylyl cyclase & intact endothelium
PDE_COL = "#F43F5E"    # rose: PDE5 / PDE6 phosphodiesterases
NO_COL = "#C084FC"     # violet: nitric oxide (NO)
ACH_COL = "#FACC15"    # gold: acetylcholine (ACh)
CA_COL = "#FB923C"     # coral-orange: calcium (Ca2+) & NO synthase
MEMB_COL = "#64748B"   # slate: lipid membranes & vessel borders
GMP_COL = "#8B93A1"    # muted slate: inactive hydrolyzed GMP particles
CELL_BG = "#1A253A"    # deep navy-slate interior for smooth muscle cell


# ------------------------------------------------------------------ Shared ODE & geometry helpers
def simulate_cgmp_trace(t_arr, s_fn, k_deg, c0):
    """Integrate dc/dt = s(t) - k_deg * c via sub-stepped Euler for smooth curves."""
    n = len(t_arr)
    c = np.zeros(n, dtype=float)
    c[0] = c0
    for i in range(1, n):
        dt = (t_arr[i] - t_arr[i - 1]) / 10.0
        val = c[i - 1]
        for k in range(10):
            tk = t_arr[i - 1] + k * dt
            val = val + dt * (s_fn(tk) - k_deg * val)
        c[i] = val
    return c


def no_burst_rate(t, t0=1.0, width=1.6, amp=1.05, basal=0.22):
    """Smooth nitric oxide synthesis pulse s(t) = basal + amp * burst(t)."""
    if t < t0:
        return basal
    u = (t - t0) / width
    return basal + amp * u * np.exp(1.0 - u)


def make_sgc(pos, active=0.0, scale=1.0):
    """Two-lobed soluble guanylyl cyclase with a recessed heme pocket on top-left."""
    c = np.array(pos, dtype=float)
    pts = [
        (-0.85, -0.42), (0.85, -0.42), (0.95, 0.0), (0.72, 0.44),
        (-0.10, 0.44), (-0.18, 0.14), (-0.52, 0.14), (-0.62, 0.44),
        (-0.92, 0.30), (-0.95, -0.10),
    ]
    body = Polygon(*[c + np.array([x * scale, y * scale, 0]) for x, y in pts],
                   stroke_color=SGC_COL, stroke_width=3.8,
                   fill_color=SGC_COL, fill_opacity=0.24 + 0.28 * active)
    if active < 0.25:
        body.set_stroke(opacity=0.58 + 0.42 * active)
    heme_pos = c + np.array([-0.35 * scale, 0.27 * scale, 0])
    heme = Circle(radius=0.15 * scale, stroke_color=ACH_COL if active > 0.5 else SGC_COL,
                  stroke_width=3.0, fill_color=ACH_COL if active > 0.5 else SGC_COL,
                  fill_opacity=0.28 + 0.52 * active).move_to(heme_pos)
    g = VGroup(body, heme)
    g.heme_pos = heme_pos
    g.body = body
    g.heme = heme
    return g


def make_pde(pos, color=PDE_COL, active=1.0, scale=1.0):
    """Phosphodiesterase with a deep catalytic pocket on the top-left for cGMP or wedge."""
    c = np.array(pos, dtype=float)
    pts = [
        (-0.78, -0.45), (0.78, -0.45), (0.88, 0.05), (0.68, 0.48),
        (0.08, 0.48), (-0.02, 0.02), (-0.42, 0.02), (-0.52, 0.48),
        (-0.86, 0.32), (-0.88, -0.12),
    ]
    body = Polygon(*[c + np.array([x * scale, y * scale, 0]) for x, y in pts],
                   stroke_color=color, stroke_width=3.8,
                   fill_color=color, fill_opacity=0.18 + 0.24 * active)
    body.set_stroke(opacity=0.45 + 0.55 * active)
    pocket = c + np.array([-0.22 * scale, 0.26 * scale, 0])
    g = VGroup(body)
    g.pocket = pocket
    g.body = body
    return g


def make_sildenafil_wedge(scale=1.0):
    """Crisp white wedge shaped to seat inside the PDE5 catalytic pocket."""
    pts = [(-0.23, 0.42), (0.23, 0.42), (0.15, -0.17), (-0.15, -0.17)]
    return Polygon(*[np.array([x * scale, y * scale, 0]) for x, y in pts],
                   stroke_color=TEXT, stroke_width=2.5,
                   fill_color=TEXT, fill_opacity=0.92)


def make_cgmp_gauge(tracker, center, width=0.56, height=2.15, baseline=0.20,
                    label="cGMP", base_side=LEFT, base_text="baseline"):
    """Live vertical teal cGMP gauge driven by a 0..1 ValueTracker, with dashed baseline."""
    cx, cy, _ = np.array(center, dtype=float)
    y_bot = cy - height / 2

    outer = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                             stroke_color=TEXT, stroke_width=2.8,
                             fill_color=BG, fill_opacity=0.90).move_to([cx, cy, 0])

    def mk_fill():
        v = float(np.clip(tracker.get_value(), 0.03, 0.98))
        h = max(0.08, v * (height - 0.08))
        r = RoundedRectangle(corner_radius=0.07, width=width - 0.08, height=h,
                             stroke_width=0, fill_color=CGMP_COL, fill_opacity=0.92)
        r.move_to([cx, y_bot + 0.04 + h / 2, 0])
        return r

    fill = always_redraw(mk_fill)
    base_y = y_bot + 0.04 + baseline * (height - 0.08)
    base_line = DashedLine([cx - width / 2 - 0.14, base_y, 0],
                           [cx + width / 2 + 0.14, base_y, 0],
                           color=TEXT, stroke_width=2.5, dash_length=0.09)
    top_lbl = T(label, 26, CGMP_COL, weight=BOLD).next_to(outer, UP, buff=0.16)
    g = VGroup(outer, fill, base_line, top_lbl)
    if base_text:
        base_lbl = T(base_text, 22, TEXT).next_to(base_line, base_side, buff=0.12)
        g.add(base_lbl)
    return g


def make_filaments(tracker, center_x_tr, cy, y_sep=0.28):
    """Actin-myosin contractile filament pairs sliding apart as cGMP rises."""
    def mk():
        cx = float(center_x_tr.get_value()) if hasattr(center_x_tr, "get_value") else float(center_x_tr)
        v = float(np.clip(tracker.get_value(), 0.0, 1.0))
        relax = float(np.clip((v - 0.20) / 0.65, 0.0, 1.0))
        span = 0.62 + 0.48 * relax
        g = VGroup()
        for dy in (-y_sep, y_sep):
            y = cy + dy
            myo = RoundedRectangle(corner_radius=0.04, width=1.30, height=0.14,
                                   stroke_width=0, fill_color="#94A3B8",
                                   fill_opacity=0.90 - 0.22 * relax).move_to([cx, y, 0])
            act_l1 = Line([cx - span - 0.92, y + 0.07, 0], [cx - span + 0.30, y + 0.07, 0],
                          color=TEXT, stroke_width=4.8)
            act_r1 = Line([cx + span - 0.30, y + 0.07, 0], [cx + span + 0.92, y + 0.07, 0],
                          color=TEXT, stroke_width=4.8)
            act_l2 = Line([cx - span - 0.92, y - 0.07, 0], [cx - span + 0.30, y - 0.07, 0],
                          color=TEXT, stroke_width=4.8)
            act_r2 = Line([cx + span - 0.30, y - 0.07, 0], [cx + span + 0.92, y - 0.07, 0],
                          color=TEXT, stroke_width=4.8)
            g.add(myo, act_l1, act_r1, act_l2, act_r2)
        return g

    return always_redraw(mk)


def make_artery_wall_shell(cgmp_tracker, x_left=-5.9, x_right=5.9, y_bot=-3.05,
                           y_endo_base=1.18, endo_h=0.78, y_top_limit=3.20):
    """Dynamic artery-wall cross-section: lumen at top widens as cgmp_tracker rises."""
    def mk():
        v = float(np.clip(cgmp_tracker.get_value(), 0.0, 1.0))
        relax = float(np.clip((v - 0.20) / 0.65, 0.0, 1.0))
        y_sm_top = y_endo_base - 0.30 * relax
        y_en_top = y_sm_top + endo_h
        w = x_right - x_left
        cx = (x_left + x_right) / 2

        lumen_h = max(0.35, y_top_limit - y_en_top)
        lumen_rect = Rectangle(width=w, height=lumen_h, stroke_width=0,
                               fill_color=PDE_COL, fill_opacity=0.22).move_to([cx, y_en_top + lumen_h / 2, 0])
        lumen_top = Line([x_left, y_top_limit, 0], [x_right, y_top_limit, 0],
                         color=MEMB_COL, stroke_width=4.5)

        endo_box = RoundedRectangle(corner_radius=0.10, width=w, height=endo_h,
                                    stroke_color=SGC_COL, stroke_width=4.0,
                                    fill_color=SGC_COL, fill_opacity=0.24).move_to([cx, (y_sm_top + y_en_top) / 2, 0])

        sm_h = y_sm_top - y_bot - 0.14
        sm_box = RoundedRectangle(corner_radius=0.14, width=w, height=sm_h,
                                  stroke_color=MEMB_COL, stroke_width=4.0,
                                  fill_color=CELL_BG, fill_opacity=0.88).move_to([cx, y_bot + sm_h / 2, 0])

        return VGroup(lumen_rect, lumen_top, endo_box, sm_box)

    return always_redraw(mk)


def make_rod_inset(cgmp_tracker, center=(-4.55, -0.35, 0), w=3.05, h=4.75,
                   pde_label="PDE6", show_light=True):
    """Echo of the first film's rod outer segment with a dropping cGMP gauge & PDE6."""
    cx, cy, _ = np.array(center, dtype=float)
    frame = RoundedRectangle(corner_radius=0.16, width=w, height=h,
                             stroke_color=CGMP_COL, stroke_width=3.2,
                             fill_color=CELL_BG, fill_opacity=0.95).move_to([cx, cy, 0])
    head = T("Rod (first film)", 24, CGMP_COL, weight=BOLD).move_to([cx, cy + h / 2 - 0.38, 0])

    gw, gh = 0.56, 2.05
    gx, gy = cx - 0.72, cy - 0.25
    g_box = RoundedRectangle(corner_radius=0.07, width=gw, height=gh,
                             stroke_color=TEXT, stroke_width=2.5).move_to([gx, gy, 0])

    def mk_rod_fill():
        v = float(np.clip(cgmp_tracker.get_value(), 0.04, 0.96))
        fh = max(0.06, v * (gh - 0.06))
        r = RoundedRectangle(corner_radius=0.05, width=gw - 0.06, height=fh,
                             stroke_width=0, fill_color=CGMP_COL, fill_opacity=0.92)
        r.move_to([gx, gy - gh / 2 + 0.03 + fh / 2, 0])
        return r

    g_fill = always_redraw(mk_rod_fill)
    g_lbl = T("cGMP", 22, CGMP_COL).next_to(g_box, DOWN, buff=0.18)

    pde = make_pde([cx + 0.56, cy - 0.25, 0], color=PDE_COL, active=1.0, scale=0.62)
    plab = T(pde_label, 22, PDE_COL, weight=BOLD).next_to(pde, DOWN, buff=0.20)

    g = VGroup(frame, head, g_box, g_fill, g_lbl, pde, plab)
    if show_light:
        photon = T("light", 22, ACH_COL, weight=BOLD).move_to([cx + 0.56, cy + 1.05, 0])
        parr = Arrow([cx + 0.56, cy + 0.85, 0], [cx + 0.56, cy + 0.20, 0],
                     color=ACH_COL, stroke_width=3.8, buff=0.05, max_tip_length_to_length_ratio=0.35)
        g.add(photon, parr)
    return g


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Sensing the World: Vision, Smell, Nitric Oxide and cGMP"
    TITLE = "When cGMP Rises: Arteries and Drugs"


class S01Hook(SpokenScene):
    def construct(self):
        rod_cgmp = ValueTracker(0.86)
        art_cgmp = ValueTracker(0.20)

        wall = make_artery_wall_shell(art_cgmp, x_left=-2.2, x_right=6.0,
                                      y_bot=-3.0, y_endo_base=1.18, endo_h=0.78, y_top_limit=3.20)
        lumen_lbl = T("Lumen", 26, TEXT).move_to([1.9, 2.75, 0])
        endo_lbl = always_redraw(lambda: T("Endothelium", 26, SGC_COL, weight=BOLD).move_to(
            [1.9, 1.18 - 0.30 * np.clip((art_cgmp.get_value() - 0.20) / 0.65, 0.0, 1.0) + 0.39, 0]))
        sm_lbl = T("Smooth muscle", 26, TEXT, weight=BOLD).move_to([-0.2, 0.32, 0])

        sgc_quiet = make_sgc([-0.3, -0.85, 0], active=0.0, scale=0.85)
        pde_quiet = make_pde([2.2, -1.35, 0], active=0.0, scale=0.72)
        filaments = make_filaments(art_cgmp, -0.2, -2.30)
        gauge = make_cgmp_gauge(art_cgmp, [5.15, -1.25, 0], width=0.54, height=2.10, baseline=0.20)

        art_group = VGroup(wall, lumen_lbl, endo_lbl, sm_lbl, sgc_quiet, pde_quiet, filaments, gauge)
        rod_inset = make_rod_inset(rod_cgmp, center=(-4.45, -0.15, 0), w=3.15, h=4.9, pde_label="PDE6", show_light=True)

        # Animated cGMP dots being broken inside rod inset while rod_cgmp drops
        rod_dots = always_redraw(lambda: VGroup(*[
            Dot([-4.45 - 0.72 + 0.16 * np.cos(i * 1.4 + rod_cgmp.get_value() * 8),
                 -0.40 + 0.7 * np.sin(i * 1.1 + rod_cgmp.get_value() * 5), 0],
                radius=0.085, color=CGMP_COL).set_opacity(np.clip(rod_cgmp.get_value() * 1.1, 0.12, 0.95))
            for i in range(6)
        ]))

        self.add(art_group, rod_inset, rod_dots)
        self.at("In the first film")
        self.play(rod_cgmp.animate.set_value(0.62), run_time=2.0, rate_func=linear)

        self.at("driving CGMP down")
        self.play(rod_cgmp.animate.set_value(0.16), run_time=3.5, rate_func=smooth)

        self.at("Why does that")
        self.remove(rod_dots)
        self.play(FadeOut(rod_inset, shift=LEFT * 0.4), run_time=0.6)

        full_wall = make_artery_wall_shell(art_cgmp, x_left=-5.9, x_right=5.9,
                                           y_bot=-3.0, y_endo_base=1.18, endo_h=0.78, y_top_limit=3.20)
        full_lumen_lbl = T("Lumen", 26, TEXT).move_to([0.0, 2.75, 0])
        full_endo_lbl = always_redraw(lambda: T("Endothelium", 26, SGC_COL, weight=BOLD).move_to(
            [-3.9, 1.18 - 0.30 * np.clip((art_cgmp.get_value() - 0.20) / 0.65, 0.0, 1.0) + 0.39, 0]))
        full_sm_lbl = T("Smooth muscle", 28, TEXT, weight=BOLD).move_to([-3.8, 0.32, 0])
        full_sgc = make_sgc([-3.4, -0.90, 0], active=0.0, scale=0.92)
        full_pde = make_pde([2.0, -1.35, 0], active=0.0, scale=0.80)
        full_fils = make_filaments(art_cgmp, -0.8, -2.30)
        full_gauge = make_cgmp_gauge(art_cgmp, [5.15, -1.25, 0], width=0.56, height=2.15, baseline=0.20)

        self.play(
            ReplacementTransform(wall, full_wall),
            ReplacementTransform(lumen_lbl, full_lumen_lbl),
            ReplacementTransform(endo_lbl, full_endo_lbl),
            ReplacementTransform(sm_lbl, full_sm_lbl),
            ReplacementTransform(sgc_quiet, full_sgc),
            ReplacementTransform(pde_quiet, full_pde),
            ReplacementTransform(filaments, full_fils),
            ReplacementTransform(gauge, full_gauge),
            run_time=0.8
        )

        self.at("rise to relax")
        q_mark = T("rise?", 30, CGMP_COL, weight=BOLD).move_to([3.4, -0.25, 0])
        self.play(art_cgmp.animate.set_value(0.65), FadeIn(q_mark, run_time=0.35), run_time=2.0)

        self.at("how do drugs")
        drug_q = T("drugs?", 28, ACH_COL, weight=BOLD).next_to(q_mark, DOWN, buff=0.32)
        self.play(FadeIn(drug_q, run_time=0.35), art_cgmp.animate.set_value(0.22), run_time=2.0)

        self.at("classic vessel experiment")
        taut_lbl = T("taut filaments", 26, TEXT).move_to([-0.8, -1.62, 0])
        self.play(FadeOut(q_mark, run_time=0.3), FadeOut(drug_q, run_time=0.3),
                  FadeIn(taut_lbl, run_time=0.4), art_cgmp.animate.set_value(0.16), run_time=1.8)
        self.play(art_cgmp.animate.set_value(0.20), run_time=1.0)
        self.finish()


class S02EndotheliumPuzzle(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        tp = TwoPanel("Intact lining", "Second ring", colors=(SGC_COL, PDE_COL), top=2.80, bottom=-2.50)
        right_head_init = tp.right_head
        right_head_init.set_color(TEXT)
        tp.remove(right_head_init)
        tp.right_frame.set_stroke(color=TEXT)
        tag = scope_tag("schematic")

        r_left = ValueTracker(1.0)
        r_right = ValueTracker(1.0)
        lining_alpha = ValueTracker(1.0)

        def mk_ring(center, r_tr, has_lining=False):
            cx, cy, _ = np.array(center, dtype=float)

            def draw():
                ri = float(r_tr.get_value()) * 0.78
                ro = ri + 0.48
                muscle = Annulus(inner_radius=ri, outer_radius=ro,
                                 color=MEMB_COL, stroke_width=3.5,
                                 fill_color=MEMB_COL, fill_opacity=0.46).move_to([cx, cy, 0])
                g = VGroup(muscle)
                for k in range(12):
                    ang = k * TAU / 12.0
                    rm = (ri + ro) / 2.0
                    p1 = np.array([cx + rm * np.cos(ang - 0.14), cy + rm * np.sin(ang - 0.14), 0])
                    p2 = np.array([cx + rm * np.cos(ang + 0.14), cy + rm * np.sin(ang + 0.14), 0])
                    g.add(Line(p1, p2, color=TEXT, stroke_width=2.8))
                if has_lining:
                    endo = Annulus(inner_radius=ri - 0.08, outer_radius=ri,
                                   color=SGC_COL, stroke_width=2.2,
                                   fill_color=SGC_COL, fill_opacity=0.92).move_to([cx, cy, 0])
                    g.add(endo)
                else:
                    op = float(lining_alpha.get_value())
                    if op > 0.05:
                        endo = Annulus(inner_radius=ri - 0.08, outer_radius=ri,
                                       color=SGC_COL, stroke_width=2.2,
                                       fill_color=SGC_COL, fill_opacity=0.92 * op).move_to([cx, cy, 0])
                        g.add(endo)
                return g

            return always_redraw(draw)

        lc, _, _ = tp.area("left")
        rc, _, _ = tp.area("right")
        ring_l = mk_ring(lc + UP * 0.05, r_left, has_lining=True)
        ring_r = mk_ring(rc + UP * 0.05, r_right, has_lining=False)
        bath_lbl = T("warm oxygenated salt solution", 26, TEXT).move_to([-0.9, -3.1, 0])

        self.add(tp, right_head_init, ring_l, ring_r, tag)
        self.at("Mount a ring")
        self.play(r_left.animate.set_value(1.06), r_right.animate.set_value(1.06), run_time=1.4)

        self.at("warm, oxygenated salt solution")
        self.play(FadeIn(bath_lbl, run_time=0.45), r_left.animate.set_value(1.0), r_right.animate.set_value(1.0), run_time=1.8)

        ach_t = ValueTracker(0.0)
        n_ach = 20
        starts_l = np.column_stack([rng.uniform(lc[0] - 2.1, lc[0] + 2.1, n_ach),
                                    rng.uniform(lc[1] + 1.3, lc[1] + 1.8, n_ach)])
        angles_l = rng.uniform(0, TAU, n_ach)
        radii_l = rng.uniform(1.06, 1.42, n_ach)
        ends_l = np.column_stack([lc[0] + radii_l * np.cos(angles_l),
                                  lc[1] + 0.05 + radii_l * np.sin(angles_l)])
        starts_r = starts_l.copy()
        starts_r[:, 0] += (rc[0] - lc[0])
        ends_r = ends_l.copy()
        ends_r[:, 0] += (rc[0] - lc[0])

        def mk_ach_cloud():
            t = float(ach_t.get_value())
            p = float(np.clip(t, 0.0, 1.0))
            swirl = max(0.0, t - 1.0)
            g = VGroup()
            for idx, (sl, el, sr, er) in enumerate(zip(starts_l, ends_l, starts_r, ends_r)):
                pl = sl + p * (el - sl) + np.array([0.14 * np.sin(swirl * 2.5 + idx), 0.10 * np.cos(swirl * 2.1 + idx)])
                pr = sr + p * (er - sr) + np.array([0.14 * np.sin(swirl * 2.5 + idx), 0.10 * np.cos(swirl * 2.1 + idx)])
                g.add(Dot([pl[0], pl[1], 0], radius=0.085, color=ACH_COL),
                      Dot([pr[0], pr[1], 0], radius=0.085, color=ACH_COL))
            return g

        ach_cloud = always_redraw(mk_ach_cloud)
        ach_lbl = T("acetylcholine", 28, ACH_COL, weight=BOLD).move_to([0.0, 3.25, 0])

        self.at("add acetylcholine")
        self.add(ach_cloud)
        self.play(FadeIn(ach_lbl, run_time=0.4), ach_t.animate.set_value(0.55), run_time=2.8)

        self.at("the endothelium")
        endo_callout = T("endothelium", 24, SGC_COL, weight=BOLD).move_to([lc[0] - 0.9, lc[1] - 1.85, 0])
        endo_ptr_init = Arrow(
            endo_callout.get_top() + UP * 0.05,
            lc + DOWN * (r_left.get_value() * 0.78 + 0.04) + LEFT * 0.20,
            color=SGC_COL, stroke_width=3.2, buff=0.04, max_tip_length_to_length_ratio=0.25,
        )
        self.play(FadeIn(endo_callout, run_time=0.4), GrowArrow(endo_ptr_init), ach_t.animate.set_value(0.85), run_time=2.2)
        endo_ptr = always_redraw(lambda: Arrow(
            endo_callout.get_top() + UP * 0.05,
            lc + DOWN * (r_left.get_value() * 0.78 + 0.04) + LEFT * 0.20,
            color=SGC_COL, stroke_width=3.2, buff=0.04, max_tip_length_to_length_ratio=0.25,
        ))
        self.remove(endo_ptr_init)
        self.add(endo_ptr)

        self.at("relaxes and widens")
        wide_lbl = T("relaxes & widens", 26, SGC_COL, weight=BOLD).move_to([lc[0], lc[1] + 1.85, 0])
        self.play(r_left.animate.set_value(1.36), ach_t.animate.set_value(1.15),
                  FadeIn(wide_lbl, run_time=0.4), run_time=2.6)

        self.at("Rub that lining off")
        swab = Line(rc + UL * 0.85, rc + DR * 0.85, color=PDE_COL, stroke_width=6.0)
        removed_head = fit_text("Lining removed", max_w=tp.right_frame.width - 0.5, size=32, color=PDE_COL).move_to(
            [right_head_init.get_center()[0], 2.80 - 0.45, 0]
        )
        self.play(Create(swab), lining_alpha.animate.set_value(0.0), ach_t.animate.set_value(1.30),
                  tp.right_frame.animate.set_stroke(color=PDE_COL),
                  swap(right_head_init, removed_head, run_time=0.9), run_time=0.9)
        self.play(FadeOut(swab, run_time=0.35), ach_t.animate.set_value(1.40), run_time=0.4)

        self.at("no longer relaxes")
        tight_lbl = T("stays tight", 26, PDE_COL, weight=BOLD).move_to([rc[0], rc[1] + 1.85, 0])
        self.play(FadeIn(tight_lbl, run_time=0.4), r_right.animate.set_value(0.94),
                  r_left.animate.set_value(1.44), ach_t.animate.set_value(1.85), run_time=2.2)
        self.play(r_right.animate.set_value(1.0), ach_t.animate.set_value(2.15), run_time=1.3)

        self.at("pass a signal")
        sig_lbl = T("signal?", 24, NO_COL, weight=BOLD).move_to([lc[0] + 0.15, lc[1] - 0.25, 0])
        sig_arr = Arrow([lc[0] + 0.15, lc[1] - 0.65, 0], [lc[0] + 0.15, lc[1] - 1.25, 0],
                        color=NO_COL, stroke_width=4.8, buff=0.02, max_tip_length_to_length_ratio=0.32)
        self.play(FadeIn(sig_lbl, run_time=0.4), GrowArrow(sig_arr),
                  ach_t.animate.set_value(2.75), run_time=2.4)
        self.finish()


class S03NoDiffusion(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        tag = scope_tag("schematic")

        lumen_rect = Rectangle(width=11.8, height=1.10, stroke_width=0,
                               fill_color=PDE_COL, fill_opacity=0.22).move_to([0, 2.75, 0])
        lumen_top = Line([-5.9, 3.30, 0], [5.9, 3.30, 0], color=MEMB_COL, stroke_width=4.5)
        lumen_lbl = T("Lumen", 26, TEXT).move_to([-4.8, 2.90, 0])

        endo_box = RoundedRectangle(corner_radius=0.12, width=11.8, height=1.55,
                                    stroke_color=SGC_COL, stroke_width=4.0,
                                    fill_color=SGC_COL, fill_opacity=0.24).move_to([0, 1.425, 0])
        # Shifted right to -3.85 so it has wide clearance from the Ca2+ bar at -5.5
        endo_lbl = T("Endothelial cell", 26, SGC_COL, weight=BOLD).move_to([-3.85, 1.85, 0])

        rec = Polygon([-2.55, 2.20, 0], [-2.55, 2.52, 0], [-2.35, 2.52, 0], [-2.35, 2.28, 0],
                      [-2.05, 2.28, 0], [-2.05, 2.52, 0], [-1.85, 2.52, 0], [-1.85, 2.20, 0],
                      stroke_color=ACH_COL, stroke_width=3.2, fill_color=ACH_COL, fill_opacity=0.28)
        rec_lbl = T("receptor", 24, ACH_COL).next_to(rec, RIGHT, buff=0.20).shift(UP * 0.10)

        nos_box = boxed_label("NO synthase", CA_COL, size=26, pad=0.20, fill_opacity=0.24).move_to([0.85, 1.42, 0])

        sm_box = RoundedRectangle(corner_radius=0.14, width=11.8, height=3.40,
                                  stroke_color=MEMB_COL, stroke_width=4.0,
                                  fill_color=CELL_BG, fill_opacity=0.88).move_to([0, -1.35, 0])
        sm_lbl = T("Smooth muscle cell", 26, TEXT, weight=BOLD).move_to([-4.0, -0.05, 0])
        memb_lbl = T("two membranes (no channels needed)", 24, TEXT).move_to([-2.8, -2.70, 0])

        # Live endothelial Ca2+ bar at x = -5.50
        ca_level = ValueTracker(0.15)
        ca_bar_bg = RoundedRectangle(corner_radius=0.06, width=0.40, height=1.10,
                                     stroke_color=CA_COL, stroke_width=2.5,
                                     fill_color=BG, fill_opacity=0.92).move_to([-5.50, 1.42, 0])
        ca_bar_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.04, width=0.32, height=max(0.06, 1.00 * ca_level.get_value()),
            stroke_width=0, fill_color=CA_COL, fill_opacity=0.92
        ).move_to([-5.50, 0.92 + max(0.06, 1.00 * ca_level.get_value()) / 2, 0]))

        self.add(lumen_rect, lumen_top, lumen_lbl, endo_box, endo_lbl, rec, rec_lbl,
                 nos_box, sm_box, sm_lbl, ca_bar_bg, ca_bar_fill, tag)

        self.at("On an endothelial cell")
        # Larger ACh wave sweeping across lumen from right (+3.8) toward receptor (-2.2)
        ach_wave = VGroup(*[Dot([1.6 + 0.6 * i, 2.95, 0], radius=0.12, color=ACH_COL) for i in range(6)])
        ach_dot = ach_wave[0]
        ach_tag = T("ACh", 24, ACH_COL, weight=BOLD).move_to([-3.05, 2.85, 0])
        self.play(FadeIn(ach_wave, run_time=0.3), FadeIn(ach_tag, run_time=0.3),
                  ach_wave.animate.shift(LEFT * 3.8), run_time=2.0, rate_func=smooth)

        self.at("acetylcholine binds its receptor")
        self.play(ach_dot.animate.move_to([-2.2, 2.38, 0]),
                  FadeOut(VGroup(*ach_wave[1:]), run_time=0.4),
                  ach_tag.animate.move_to([-3.05, 2.65, 0]),
                  rec.animate.set_fill(opacity=0.70), run_time=1.8)

        ca_pts_start = np.array([[-1.4, 1.05], [-1.1, 1.55], [-0.8, 1.15], [-0.6, 1.65],
                                 [-1.2, 1.30], [-0.7, 1.40], [-0.45, 1.10], [-0.95, 1.72],
                                 [-1.55, 1.45], [-0.35, 1.52], [-1.05, 1.02], [-0.55, 1.28]])
        ca_dots = VGroup(*[Dot([x, y, 0], radius=0.105, color=CA_COL) for x, y in ca_pts_start])
        ca_lbl = T("Ca2+ rises", 24, CA_COL, weight=BOLD).move_to([-3.95, 1.15, 0])
        self.at("raises its calcium")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in ca_dots], lag_ratio=0.08),
                  ca_level.animate.set_value(0.95), FadeIn(ca_lbl, run_time=0.4), run_time=2.5)

        self.at("switches on nitric oxide")
        dock_targets = [nos_box.get_left() + LEFT * 0.24 + UP * (0.28 - 0.05 * i) for i in range(len(ca_dots))]
        # Keep fill opacity <= 0.28 so coral text inside keeps high contrast; thicken stroke to show ON state
        self.play(
            *[d.animate.move_to(t) for d, t in zip(ca_dots, dock_targets)],
            nos_box.box.animate.set_stroke(width=5.5).set_fill(opacity=0.28),
            FadeOut(ca_lbl, run_time=0.4),
            run_time=4.0, rate_func=smooth
        )

        # Computed 2D random walk + exponential decay of NO gas molecules across BOTH membranes!
        sim_t = ValueTracker(0.0)
        n_no = 38
        birth_t = rng.uniform(0.0, 11.2, n_no)
        vx0 = rng.uniform(-0.30, 0.30, n_no)
        vy0 = rng.uniform(-0.55, -0.22, n_no)
        dt_sim = 0.1
        n_steps = 160
        paths = np.zeros((n_no, n_steps, 2), dtype=float)
        origin = nos_box.get_bottom() + DOWN * 0.10
        for i in range(n_no):
            px, py = origin[0] + rng.uniform(-0.38, 0.38), origin[1]
            for s in range(n_steps):
                t_local = s * dt_sim
                if t_local >= birth_t[i]:
                    px += vx0[i] * dt_sim + rng.normal(0.0, 0.085)
                    py += vy0[i] * dt_sim + rng.normal(0.0, 0.085)
                    px = float(np.clip(px, -1.6, 5.2))
                    py = float(np.clip(py, -2.20, nos_box.get_bottom()[1] - 0.14))
                paths[i, s] = (px, py)

        tau = 3.8

        def mk_no_cloud():
            cur_t = float(sim_t.get_value())
            g = VGroup()
            for i in range(n_no):
                age = cur_t - birth_t[i]
                if age <= 0.0:
                    continue
                idx = min(n_steps - 1, int(cur_t / dt_sim))
                px, py = paths[i, idx]
                op = float(np.exp(-age / tau))
                if op < 0.08:
                    continue
                g.add(Dot([px, py, 0], radius=0.115, color=NO_COL).set_opacity(op))
            return g

        no_cloud = always_redraw(mk_no_cloud)
        arg_lbl = T("arginine -> NO", 24, NO_COL).move_to([3.85, 1.65, 0])
        no_lbl = T("nitric oxide (NO)", 26, NO_COL, weight=BOLD).move_to([3.85, 1.05, 0])

        self.at("from arginine")
        self.add(no_cloud)
        self.play(FadeIn(arg_lbl, run_time=0.4), FadeIn(no_lbl, run_time=0.4),
                  sim_t.animate.set_value(2.6), run_time=2.2, rate_func=linear)

        self.at("Small and uncharged")
        self.play(sim_t.animate.set_value(5.2), run_time=2.2, rate_func=linear)

        self.at("no vesicles or channels")
        self.play(FadeIn(memb_lbl, run_time=0.4), sim_t.animate.set_value(7.8), run_time=2.5, rate_func=linear)

        self.at("diffuses freely across")
        self.play(sim_t.animate.set_value(10.6), run_time=2.4, rate_func=linear)

        self.at("reacts away")
        react_lbl = T("short-lived: reacts in seconds", 24, NO_COL).move_to([3.4, -2.70, 0])
        self.play(FadeIn(react_lbl, run_time=0.4), sim_t.animate.set_value(13.0), run_time=2.0, rate_func=linear)

        self.at("only near neighbors")
        self.play(sim_t.animate.set_value(15.2), run_time=1.9, rate_func=linear)
        self.finish()


class S04CgmpRise(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(11)
        cgmp = ValueTracker(0.20)
        relax_tr = ValueTracker(0.20)
        sgc_on = ValueTracker(0.0)
        pkg_on = ValueTracker(0.0)

        wall = make_artery_wall_shell(relax_tr, x_left=-5.9, x_right=5.9,
                                      y_bot=-3.05, y_endo_base=1.18, endo_h=0.78, y_top_limit=3.20)
        lumen_lbl = T("Lumen", 26, TEXT).move_to([0.0, 2.82, 0])
        endo_lbl = always_redraw(lambda: T("Endothelium", 26, SGC_COL, weight=BOLD).move_to(
            [-4.1, 1.18 - 0.30 * np.clip((relax_tr.get_value() - 0.20) / 0.65, 0.0, 1.0) + 0.39, 0]))
        # Place "Smooth muscle" cleanly on upper-right away from incoming NO cloud
        sm_lbl = T("Smooth muscle", 26, TEXT, weight=BOLD).move_to([3.4, 0.40, 0])

        sgc = always_redraw(lambda: make_sgc([-3.2, -0.85, 0], active=sgc_on.get_value(), scale=0.92))
        sgc_lbl = T("soluble guanylyl cyclase", 24, SGC_COL).move_to([-3.2, -1.62, 0])

        def mk_pkg():
            act = pkg_on.get_value()
            col = CGMP_COL if act > 0.4 else GREY
            return boxed_label("PKG", col, size=28, pad=0.20,
                               fill_opacity=0.20 + 0.25 * act).move_to([0.2, -0.35, 0])

        pkg = always_redraw(mk_pkg)
        fils = make_filaments(relax_tr, -0.2, -2.25)
        fil_lbl = T("contractile filaments", 24, TEXT).move_to([-0.2, -2.80, 0])

        pde_dim = make_pde([2.4, -1.35, 0], color=PDE_COL, active=0.0, scale=0.68)
        gauge = make_cgmp_gauge(cgmp, [5.25, -1.25, 0], width=0.56, height=2.15, baseline=0.20)

        # Larger NO arrival stream across 0..5.6s
        no_arr_t = ValueTracker(0.0)
        no_dots_in = always_redraw(lambda: VGroup(*[
            Dot([-3.52 + 0.65 * np.sin(i * 1.3 + no_arr_t.get_value() * 1.2),
                 0.95 - ((no_arr_t.get_value() * 0.50 + i * 0.14) % 1.0) * 1.50, 0],
                radius=0.115, color=NO_COL).set_opacity(0.90)
            for i in range(10)
        ]))
        no_dot = Dot([-3.52, 0.15, 0], radius=0.13, color=NO_COL)
        no_lbl = T("NO", 24, NO_COL, weight=BOLD).move_to([-4.75, -0.35, 0])
        heme_lbl = T("heme", 22, ACH_COL, weight=BOLD).move_to([-2.05, -0.05, 0])
        heme_ptr = Arrow(heme_lbl.get_left() + LEFT * 0.04, np.array([-3.36, -0.48, 0]),
                         color=ACH_COL, stroke_width=2.8, buff=0.04, max_tip_length_to_length_ratio=0.18)

        self.add(wall, lumen_lbl, endo_lbl, sm_lbl, sgc, sgc_lbl, pkg, fils, fil_lbl, pde_dim, gauge, no_dots_in)
        self.at("In smooth muscle")
        self.play(no_arr_t.animate.set_value(1.8), run_time=1.4, rate_func=linear)

        self.at("nitric oxide binds")
        self.play(FadeIn(no_dot, run_time=0.3), FadeIn(no_lbl, run_time=0.3),
                  no_dot.animate.move_to([-3.52, -0.60, 0]),
                  no_lbl.animate.move_to([-4.65, -0.65, 0]),
                  no_arr_t.animate.set_value(3.4), run_time=1.4, rate_func=linear)

        self.at("heme iron")
        self.play(FadeIn(heme_lbl, run_time=0.35), GrowArrow(heme_ptr, run_time=0.35),
                  no_arr_t.animate.set_value(6.2), run_time=2.8, rate_func=linear)

        self.at("enzyme switches on")
        self.remove(no_dots_in)
        self.play(sgc_on.animate.set_value(1.0), FadeOut(heme_lbl, run_time=0.35),
                  FadeOut(heme_ptr, run_time=0.35), cgmp.animate.set_value(0.32), run_time=1.5)

        stream_t = ValueTracker(0.0)
        n_dots = 22
        phases = rng.uniform(0.0, 1.0, n_dots)
        y_jit = rng.uniform(-0.14, 0.14, n_dots)

        def mk_cgmp_stream():
            t = float(stream_t.get_value())
            g = VGroup()
            for ph, yj in zip(phases, y_jit):
                u = (t * 0.45 + ph) % 1.0
                px = -2.15 + u * 6.85
                s = float(np.clip((px + 2.15) / 1.75, 0.0, 1.0))
                s_sm = s * s * (3.0 - 2.0 * s)
                py = -0.85 + 0.43 * s_sm + yj * 0.5
                if px > 3.2:
                    py -= 0.22 * ((px - 3.2) / 1.5) ** 2
                if -0.48 <= px <= 0.88 and -0.80 <= py <= 0.10:
                    continue
                g.add(Dot([px, py, 0], radius=0.095, color=CGMP_COL).set_opacity(0.92 * (1.0 - 0.20 * u)))
            return g

        stream = always_redraw(mk_cgmp_stream)
        self.at("climbs sharply")
        self.add(stream)
        self.play(cgmp.animate.set_value(0.84), stream_t.animate.set_value(2.4),
                  run_time=2.8, rate_func=smooth)

        self.at("activates protein kinase")
        self.play(pkg_on.animate.set_value(1.0), stream_t.animate.set_value(4.2), run_time=2.0, rate_func=linear)

        self.at("works against contraction")
        self.play(relax_tr.animate.set_value(0.40), stream_t.animate.set_value(6.2), run_time=2.2, rate_func=linear)

        self.at("muscle relaxes")
        self.play(cgmp.animate.set_value(0.90), relax_tr.animate.set_value(0.65),
                  stream_t.animate.set_value(7.8), run_time=1.6, rate_func=linear)

        self.at("artery widens")
        wide_lbl = T("widened lumen", 26, SGC_COL, weight=BOLD).move_to([3.5, 2.82, 0])
        self.play(FadeIn(wide_lbl, run_time=0.4), relax_tr.animate.set_value(0.90),
                  stream_t.animate.set_value(9.2), run_time=1.4, rate_func=linear)
        self.finish()


def _s05_s06_backdrop():
    """Shared world builder for s05_predict_q end state and s06_predict_pause (exact match)."""
    cgmp = ValueTracker(0.85)
    rod_cgmp = ValueTracker(0.18)

    wall = make_artery_wall_shell(cgmp, x_left=-2.6, x_right=6.0,
                                  y_bot=-3.05, y_endo_base=1.18, endo_h=0.78, y_top_limit=2.55)
    lumen_lbl = T("Lumen", 24, TEXT).move_to([1.7, 2.25, 0])
    endo_lbl = T("Endothelium", 24, SGC_COL, weight=BOLD).move_to([1.7, 1.27, 0])
    sm_lbl = T("Smooth muscle", 26, TEXT, weight=BOLD).move_to([-0.8, 0.32, 0])

    sgc = make_sgc([-0.9, -0.85, 0], active=0.12, scale=0.82)
    sgc_lbl = T("sGC (quiet)", 24, TEXT).move_to([-0.9, -1.55, 0])
    pkg = boxed_label("PKG", CGMP_COL, size=26, pad=0.18, fill_opacity=0.28).move_to([1.5, -0.35, 0])
    fils = make_filaments(cgmp, 0.8, -2.25)
    pde_dim = make_pde([2.9, -1.35, 0], color=PDE_COL, active=0.0, scale=0.66)
    gauge = make_cgmp_gauge(cgmp, [5.25, -1.25, 0], width=0.52, height=2.10, baseline=0.20)
    rod = make_rod_inset(rod_cgmp, center=(-4.55, -0.35, 0), w=3.05, h=4.75, pde_label="PDE6", show_light=True)
    return VGroup(wall, lumen_lbl, endo_lbl, sm_lbl, sgc, sgc_lbl, pkg, fils, pde_dim, gauge, rod)


class S05PredictQ(SpokenScene):
    def construct(self):
        cgmp = ValueTracker(0.85)
        sgc_act = ValueTracker(1.0)
        sgc_x = ValueTracker(-3.2)
        fil_x = ValueTracker(-0.2)
        pde_x = ValueTracker(2.4)
        no_op = ValueTracker(1.0)

        wall = make_artery_wall_shell(cgmp, x_left=-5.9, x_right=5.9,
                                      y_bot=-3.05, y_endo_base=1.18, endo_h=0.78, y_top_limit=2.55)
        lumen_lbl = T("Lumen", 24, TEXT).move_to([0.0, 2.25, 0])
        endo_lbl = always_redraw(lambda: T("Endothelium", 24, SGC_COL, weight=BOLD).move_to(
            [-4.1, 1.18 - 0.30 * np.clip((cgmp.get_value() - 0.20) / 0.65, 0.0, 1.0) + 0.39, 0]))
        sm_lbl = T("Smooth muscle", 26, TEXT, weight=BOLD).move_to([-4.0, 0.32, 0])

        sgc = always_redraw(lambda: make_sgc([sgc_x.get_value(), -0.85, 0], active=sgc_act.get_value(), scale=0.82))
        sgc_lbl = T("sGC", 24, SGC_COL).move_to([-3.2, -1.55, 0])
        pkg = boxed_label("PKG", CGMP_COL, size=26, pad=0.18, fill_opacity=0.28).move_to([0.2, -0.35, 0])
        fils = make_filaments(cgmp, fil_x, -2.25)
        pde_dim = always_redraw(lambda: make_pde([pde_x.get_value(), -1.35, 0], color=PDE_COL, active=0.0, scale=0.66))
        gauge = make_cgmp_gauge(cgmp, [5.25, -1.25, 0], width=0.52, height=2.10, baseline=0.20)

        no_dots = always_redraw(lambda: VGroup(*[
            Dot([-3.52 + 0.4 * (i % 3) - 0.3, -0.80 + 0.25 * (i // 3) + (1.0 - no_op.get_value()) * 0.15, 0],
                radius=0.11, color=NO_COL).set_opacity(no_op.get_value())
            for i in range(9)
        ]))

        self.add(wall, lumen_lbl, endo_lbl, sm_lbl, sgc, sgc_lbl, pkg, fils, pde_dim, gauge, no_dots)
        self.at("But nitric oxide")
        self.play(no_op.animate.set_value(0.25), run_time=3.0)

        self.at("stops arriving")
        self.play(no_op.animate.set_value(0.0), run_time=1.0)

        self.at("cyclase falls quiet")
        sgc_quiet_lbl = T("sGC (quiet)", 24, TEXT).move_to([-3.2, -1.55, 0])
        self.play(sgc_act.animate.set_value(0.12), swap(sgc_lbl, sgc_quiet_lbl), run_time=1.8)

        self.at("Think back to the rod")
        rod_cgmp = ValueTracker(0.78)
        rod = make_rod_inset(rod_cgmp, center=(-4.55, -0.35, 0), w=3.05, h=4.75, pde_label="PDE6", show_light=True)
        wall_r = make_artery_wall_shell(cgmp, x_left=-2.6, x_right=6.0,
                                        y_bot=-3.05, y_endo_base=1.18, endo_h=0.78, y_top_limit=2.55)
        endo_lbl_r = T("Endothelium", 24, SGC_COL, weight=BOLD).move_to([1.7, 1.27, 0])
        self.play(
            ReplacementTransform(wall, wall_r),
            ReplacementTransform(endo_lbl, endo_lbl_r),
            lumen_lbl.animate.move_to([1.7, 2.25, 0]),
            sm_lbl.animate.move_to([-0.8, 0.32, 0]),
            sgc_x.animate.set_value(-0.9),
            sgc_quiet_lbl.animate.move_to([-0.9, -1.55, 0]),
            pkg.animate.move_to([1.5, -0.35, 0]),
            fil_x.animate.set_value(0.8),
            pde_x.animate.set_value(2.9),
            FadeIn(rod, shift=RIGHT * 0.3),
            run_time=1.4
        )

        self.at("enzyme destroyed")
        self.play(rod_cgmp.animate.set_value(0.32), run_time=2.8, rate_func=linear)

        self.at("What could bring")
        q = question_card("Nitric oxide stops: what lowers cGMP?", y=3.15, color=TEXT, size=32, max_w=11.0)
        q.question.move_to([-0.4, 3.15, 0])
        self.play(FadeIn(q.question, run_time=0.5), rod_cgmp.animate.set_value(0.20), run_time=2.2)

        self.at("muscle tightens again")
        self.play(rod_cgmp.animate.set_value(0.18), cgmp.animate.set_value(0.84), run_time=0.8)
        self.play(cgmp.animate.set_value(0.85), run_time=0.6)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "Nitric oxide stops: what lowers cGMP?"
    CARD = {"y": 3.15, "color": TEXT, "size": 32, "max_w": 11.0}
    RING_AT = (6.0, 3.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _s05_s06_backdrop()

    def construct(self):
        self.add(self.backdrop())
        qc = question_card(self.QUESTION, **self.CARD)
        qc.question.move_to([-0.4, 3.15, 0])
        self.add(qc)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S07PredictReveal(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(19)
        cgmp = ValueTracker(0.85)
        pde_act = ValueTracker(0.0)
        pde_x = ValueTracker(2.9)
        pde_y = ValueTracker(-1.35)
        fil_x = ValueTracker(0.8)
        sgc_x = ValueTracker(-0.9)
        pkg_x = ValueTracker(1.5)
        pkg_on = ValueTracker(1.0)

        wall_r = make_artery_wall_shell(cgmp, x_left=-2.6, x_right=6.0,
                                        y_bot=-3.05, y_endo_base=1.18, endo_h=0.78, y_top_limit=2.55)
        lumen_lbl = T("Lumen", 24, TEXT).move_to([1.7, 2.25, 0])
        endo_x = ValueTracker(1.7)
        endo_lbl = always_redraw(lambda: T("Endothelium", 24, SGC_COL, weight=BOLD).move_to(
            [endo_x.get_value(),
             1.18 - 0.30 * np.clip((cgmp.get_value() - 0.20) / 0.65, 0.0, 1.0) + 0.39, 0]))
        sm_lbl = T("Smooth muscle", 26, TEXT, weight=BOLD).move_to([-0.8, 0.32, 0])
        sgc = always_redraw(lambda: make_sgc([sgc_x.get_value(), -0.85, 0], active=0.12, scale=0.82))
        sgc_lbl = T("sGC (quiet)", 24, TEXT).move_to([-0.9, -1.55, 0])
        pkg = always_redraw(lambda: boxed_label("PKG", CGMP_COL if pkg_on.get_value() > 0.4 else GREY,
                                               size=26, pad=0.18,
                                               fill_opacity=0.20 + 0.22 * pkg_on.get_value()).move_to([pkg_x.get_value(), -0.35, 0]))
        fils = make_filaments(cgmp, fil_x, -2.25)
        pde = always_redraw(lambda: make_pde([pde_x.get_value(), pde_y.get_value(), 0], color=PDE_COL,
                                           active=pde_act.get_value(), scale=0.72))
        gauge = make_cgmp_gauge(cgmp, [5.25, -1.25, 0], width=0.52, height=2.15, baseline=0.20)
        rod = make_rod_inset(ValueTracker(0.18), center=(-4.55, -0.35, 0), w=3.05, h=4.75,
                             pde_label="PDE6", show_light=True)
        qc = question_card("Nitric oxide stops: what lowers cGMP?", y=3.15, color=TEXT, size=32, max_w=11.0)
        qc.question.move_to([-0.4, 3.15, 0])

        self.add(wall_r, lumen_lbl, endo_lbl, sm_lbl, sgc, sgc_lbl, pkg, fils, pde, gauge, rod, qc)

        self.at("A phosphodiesterase")
        full_wall = make_artery_wall_shell(cgmp, x_left=-5.9, x_right=5.9,
                                           y_bot=-3.05, y_endo_base=1.18, endo_h=0.78, y_top_limit=3.20)
        self.play(FadeOut(qc), FadeOut(rod, shift=LEFT * 0.4), run_time=0.45)
        self.play(
            ReplacementTransform(wall_r, full_wall),
            lumen_lbl.animate.move_to([0.0, 2.82, 0]),
            endo_x.animate.set_value(-4.1),
            sm_lbl.animate.move_to([-4.0, 0.35, 0]),
            sgc_x.animate.set_value(-3.5),
            sgc_lbl.animate.move_to([-3.5, -1.55, 0]),
            pkg_x.animate.set_value(-0.2),
            fil_x.animate.set_value(-0.8),
            pde_x.animate.set_value(2.4),
            pde_y.animate.set_value(-0.75),
            run_time=1.35
        )

        self.at("called PDE5")
        pde_lbl = T("PDE5", 28, PDE_COL, weight=BOLD).move_to([2.4, -1.42, 0])
        self.play(pde_act.animate.set_value(1.0), FadeIn(pde_lbl, run_time=0.4), run_time=1.4)

        hydro_t = ValueTracker(0.0)
        n_part = 18
        ph = rng.uniform(0.0, 1.0, n_part)
        dy_j = rng.uniform(-0.14, 0.14, n_part)

        def mk_hydro():
            t = float(hydro_t.get_value())
            g = VGroup()
            for p0, dy in zip(ph, dy_j):
                u = (t * 0.48 + p0) % 1.0
                if u < 0.5:
                    f = u / 0.5
                    px = 0.55 + f * 1.35
                    py = -0.80 + dy * (1.0 - f)
                    g.add(Dot([px, py, 0], radius=0.095, color=CGMP_COL).set_opacity(0.92))
                else:
                    f = (u - 0.5) / 0.5
                    px = 2.65 + f * 1.00
                    py = -0.75 - f * 0.65 + dy * f
                    op = max(0.08, 1.0 - f)
                    g.add(Dot([px, py, 0], radius=0.08, color=GMP_COL).set_opacity(op))
            return g

        hydro_stream = always_redraw(mk_hydro)
        gmp_lbl = T("GMP (inactive)", 24, TEXT).move_to([2.85, -2.55, 0])

        self.at("it breaks")
        self.add(hydro_stream)
        self.play(hydro_t.animate.set_value(1.8), cgmp.animate.set_value(0.62),
                  run_time=1.8, rate_func=linear)

        self.at("GMP")
        self.play(FadeIn(gmp_lbl, run_time=0.4), hydro_t.animate.set_value(3.2),
                  cgmp.animate.set_value(0.48), run_time=1.9, rate_func=linear)

        self.at("Relaxation lasts")
        self.play(hydro_t.animate.set_value(6.5), cgmp.animate.set_value(0.36),
                  run_time=4.6, rate_func=linear)

        self.at("When synthesis stops")
        self.play(hydro_t.animate.set_value(7.6), cgmp.animate.set_value(0.24),
                  pkg_on.animate.set_value(0.0), run_time=1.3, rate_func=linear)

        self.at("muscle tightens again")
        self.play(cgmp.animate.set_value(0.20), hydro_t.animate.set_value(9.0),
                  run_time=1.6, rate_func=smooth)
        self.finish()


class S08Drugs(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(23)
        cgmp = ValueTracker(0.20)
        sgc_act = ValueTracker(0.15)
        tag = scope_tag("schematic")

        wall = make_artery_wall_shell(cgmp, x_left=-5.9, x_right=5.9,
                                      y_bot=-3.05, y_endo_base=1.18, endo_h=0.78, y_top_limit=3.20)
        lumen_lbl = T("Lumen", 26, TEXT).move_to([0.0, 2.82, 0])
        endo_lbl = always_redraw(lambda: T("Endothelium (quiet)", 24, TEXT).move_to(
            [-3.9, 1.18 - 0.30 * np.clip((cgmp.get_value() - 0.20) / 0.65, 0.0, 1.0) + 0.39, 0]))
        sm_lbl = T("Smooth muscle", 26, TEXT, weight=BOLD).move_to([-4.25, 0.44, 0])

        sgc = always_redraw(lambda: make_sgc([-1.85, -0.70, 0], active=sgc_act.get_value(), scale=0.84))
        sgc_lbl = T("sGC", 26, SGC_COL, weight=BOLD).move_to([-1.85, -1.42, 0])

        pde = make_pde([2.2, -0.70, 0], color=PDE_COL, active=1.0, scale=0.84)
        pde_lbl = T("PDE5", 26, PDE_COL, weight=BOLD).move_to([2.2, -1.42, 0])

        fils = make_filaments(cgmp, -1.75, -2.35)
        gauge = make_cgmp_gauge(cgmp, [5.25, -1.25, 0], width=0.56, height=2.15, baseline=0.20)

        syn_lbl = T("synthesis", 24, SGC_COL, weight=BOLD).move_to([-1.85, 0.08, 0])
        brk_lbl = T("breakdown", 24, PDE_COL, weight=BOLD).move_to([2.2, 0.08, 0])

        self.add(wall, lumen_lbl, endo_lbl, sm_lbl, sgc, sgc_lbl, pde, pde_lbl,
                 fils, gauge, syn_lbl, brk_lbl, tag)

        self.at("Two familiar drugs")
        bal_arr_l = Arrow([-0.90, -0.70, 0], [-0.05, -0.70, 0], color=SGC_COL, stroke_width=4.5)
        bal_arr_r = Arrow([0.25, -0.70, 0], [1.15, -0.70, 0], color=PDE_COL, stroke_width=4.5)
        self.play(GrowArrow(bal_arr_l), GrowArrow(bal_arr_r), cgmp.animate.set_value(0.26), run_time=2.4)
        self.play(cgmp.animate.set_value(0.20), FadeOut(bal_arr_l, run_time=0.4),
                  FadeOut(bal_arr_r, run_time=0.4), run_time=2.0)

        nitro = boxed_label("Nitroglycerin", NO_COL, size=24, pad=0.14, fill_opacity=0.24).move_to([-4.55, -0.70, 0])
        plume_t = ValueTracker(0.0)
        n_plume = 18
        p_ph = rng.uniform(0.0, 1.0, n_plume)
        p_dy = rng.uniform(-0.18, 0.18, n_plume)

        def mk_plume():
            t = float(plume_t.get_value())
            if t <= 0.0:
                return VGroup()
            g = VGroup()
            for ph, dy in zip(p_ph, p_dy):
                u = (t * 0.55 + ph) % 1.0
                px = -3.25 + u * 1.15
                py = -0.68 + 0.36 * np.sin(u * PI) + dy * (1.0 - 0.6 * u)
                g.add(Dot([px, py, 0], radius=0.095, color=NO_COL).set_opacity(0.92 * (1.0 - 0.2 * u)))
            return g

        plume = always_redraw(mk_plume)
        no_tag = T("NO", 24, NO_COL, weight=BOLD).move_to([-3.25, -0.05, 0])

        self.at("Nitroglycerin")
        self.add(plume)
        self.play(FadeIn(nitro, shift=RIGHT * 0.25, run_time=0.5),
                  plume_t.animate.set_value(1.8), run_time=2.2, rate_func=linear)

        self.at("converted in tissue")
        self.play(FadeIn(no_tag, run_time=0.4), plume_t.animate.set_value(4.0),
                  sgc_act.animate.set_value(1.0), cgmp.animate.set_value(0.45),
                  run_time=3.0, rate_func=linear)

        self.at("drives synthesis up")
        self.play(cgmp.animate.set_value(0.85), plume_t.animate.set_value(7.2),
                  run_time=3.6, rate_func=smooth)

        self.play(plume_t.animate.set_value(0.0), sgc_act.animate.set_value(0.35),
                  cgmp.animate.set_value(0.55), FadeOut(no_tag, run_time=0.35), run_time=1.3)

        wedge = make_sildenafil_wedge(scale=0.84).move_to([pde.pocket[0], 0.02, 0])
        sild_lbl = T("Sildenafil", 26, TEXT, weight=BOLD).move_to([2.02, 0.47, 0])

        self.at("Sildenafil sits")
        self.play(FadeIn(wedge, run_time=0.4), swap(brk_lbl, sild_lbl, run_time=0.6),
                  cgmp.animate.set_value(0.48), run_time=1.0)
        self.at("catalytic pocket")
        self.play(wedge.animate.move_to(pde.pocket + DOWN * 0.04),
                  cgmp.animate.set_value(0.58), run_time=2.4)

        self.at("slowing hydrolysis")
        # Placed cleanly under PDE5 at x = 2.2, well clear of shifted filaments and baseline
        slow_lbl = T("hydrolysis slowed", 24, CGMP_COL, weight=BOLD).move_to([2.2, -2.30, 0])
        self.play(FadeIn(slow_lbl, run_time=0.4), cgmp.animate.set_value(0.76), run_time=2.4)

        self.at("last longer")
        self.play(cgmp.animate.set_value(0.85), run_time=2.2, rate_func=smooth)
        self.finish()


class S09RodContrast(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(31)
        tp = TwoPanel("Rod cell (light)", "Smooth muscle (NO)", colors=(CGMP_COL, SGC_COL), top=3.00, bottom=-2.60)
        tag = scope_tag("schematic")

        rod_cgmp = ValueTracker(0.85)
        art_cgmp = ValueTracker(0.20)
        flux_t = ValueTracker(0.0)

        lc, _, _ = tp.area("left")
        rc, _, _ = tp.area("right")

        light_arr = Arrow([lc[0] - 2.35, lc[1] + 1.45, 0], [lc[0] - 1.35, lc[1] + 1.45, 0],
                          color=ACH_COL, stroke_width=4.0, buff=0.05)
        light_lbl = T("light", 24, ACH_COL, weight=BOLD).next_to(light_arr, UP, buff=0.10)
        pde6 = make_pde([lc[0] - 0.55, lc[1] + 1.15, 0], color=PDE_COL, active=1.0, scale=0.66)
        pde6_tag = T("PDE6", 24, PDE_COL, weight=BOLD).next_to(pde6, DOWN, buff=0.14)
        rod_gauge = make_cgmp_gauge(rod_cgmp, [lc[0] + 1.85, lc[1] - 0.05, 0],
                                    width=0.52, height=2.20, baseline=0.80, base_side=LEFT)

        no_arr = Arrow([rc[0] - 2.35, rc[1] + 1.45, 0], [rc[0] - 1.35, rc[1] + 1.45, 0],
                       color=NO_COL, stroke_width=4.0, buff=0.05)
        no_lbl = T("NO", 24, NO_COL, weight=BOLD).next_to(no_arr, UP, buff=0.10)
        sgc_r = make_sgc([rc[0] - 0.55, rc[1] + 1.15, 0], active=1.0, scale=0.66)
        sgc_tag = T("sGC", 24, SGC_COL, weight=BOLD).next_to(sgc_r, DOWN, buff=0.14)
        pde5 = make_pde([rc[0] - 0.70, rc[1] - 0.75, 0], color=PDE_COL, active=1.0, scale=0.64)
        pde5_tag = T("PDE5", 24, PDE_COL, weight=BOLD).next_to(pde5, DOWN, buff=0.14)
        art_gauge = make_cgmp_gauge(art_cgmp, [rc[0] + 1.85, rc[1] - 0.05, 0],
                                    width=0.52, height=2.20, baseline=0.20, base_side=LEFT)

        n_f = 16
        f_ph = rng.uniform(0.0, 1.0, n_f)
        f_dx = rng.uniform(-0.22, 0.22, n_f)

        def mk_fluxes():
            t = float(flux_t.get_value())
            g = VGroup()
            for ph, dx in zip(f_ph, f_dx):
                u = (t * 0.50 + ph) % 1.0
                ly = lc[1] + 0.10 - u * 1.15
                lx = lc[0] - 1.95 + dx
                if u < 0.6:
                    g.add(Dot([lx, ly, 0], radius=0.095, color=CGMP_COL).set_opacity(0.92))
                else:
                    g.add(Dot([lx, ly, 0], radius=0.08, color=GMP_COL).set_opacity(0.85 * (1.0 - (u - 0.6) / 0.4)))
                ry = rc[1] - 0.15 + u * 0.75
                rx = rc[0] - 2.05 + dx
                g.add(Dot([rx, ry, 0], radius=0.095, color=CGMP_COL).set_opacity(0.92 * (1.0 - 0.3 * u)))
            return g

        fluxes = always_redraw(mk_fluxes)

        self.add(tp, light_arr, light_lbl, pde6, pde6_tag, rod_gauge,
                 no_arr, no_lbl, sgc_r, sgc_tag, pde5, pde5_tag, art_gauge, tag, fluxes)

        self.at("place the rod")
        self.play(rod_cgmp.animate.set_value(0.68), art_cgmp.animate.set_value(0.32),
                  flux_t.animate.set_value(1.5), run_time=2.0, rate_func=linear)

        self.at("smooth muscle cell")
        self.play(rod_cgmp.animate.set_value(0.45), art_cgmp.animate.set_value(0.55),
                  flux_t.animate.set_value(3.5), run_time=3.2, rate_func=linear)

        self.at("phosphodiesterase")
        self.play(rod_cgmp.animate.set_value(0.18), art_cgmp.animate.set_value(0.85),
                  flux_t.animate.set_value(6.2), run_time=3.8, rate_func=smooth)

        self.at("wiring reverses")
        rev_l = T("cGMP falls", 24, CGMP_COL, weight=BOLD).move_to([lc[0] - 0.15, lc[1] - 0.50, 0])
        rev_r = T("cGMP rises", 24, CGMP_COL, weight=BOLD).move_to([rc[0] - 0.15, rc[1] + 0.18, 0])
        self.play(FadeIn(rev_l, run_time=0.4), FadeIn(rev_r, run_time=0.4),
                  rod_cgmp.animate.set_value(0.14), art_cgmp.animate.set_value(0.89),
                  flux_t.animate.set_value(8.4), run_time=2.6, rate_func=linear)

        self.at("In the rod")
        rod_rule = T("PDE6 makes the signal", 26, PDE_COL, weight=BOLD).move_to([lc[0], lc[1] - 1.95, 0])
        self.play(FadeIn(rod_rule, run_time=0.4), rod_cgmp.animate.set_value(0.18),
                  flux_t.animate.set_value(10.6), run_time=3.0, rate_func=linear)

        self.at("In the artery")
        art_rule = T("PDE5 ends the signal", 26, PDE_COL, weight=BOLD).move_to([rc[0], rc[1] - 1.95, 0])
        self.play(FadeIn(art_rule, run_time=0.4), art_cgmp.animate.set_value(0.85),
                  flux_t.animate.set_value(12.8), run_time=3.0, rate_func=linear)
        self.finish()


class S10Takehome(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")

        t_max = 12.0
        ts = np.linspace(0.0, t_max, 240)
        c_base = 0.22
        c_norm_arr = simulate_cgmp_trace(ts, no_burst_rate, k_deg=1.0, c0=c_base)
        c_blk_arr = simulate_cgmp_trace(ts, lambda t: no_burst_rate(t, basal=0.22 * 0.28, amp=1.05),
                                        k_deg=0.28, c0=c_base)

        norm_fn = lambda t: float(np.interp(t, ts, c_norm_arr))
        blk_fn = lambda t: float(np.interp(t, ts, c_blk_arr))

        P = Plot(box=(-5.6, 1.3, -1.6, 2.3), xr=(0, t_max), yr=(0, 3.2),
                 xticks=[], yticks=[], xlabel="time (burst of NO)", ylabel="cGMP (schematic)")
        base_line = P.hline(c_base, label=None, color=GREY)
        base_lbl = T("baseline", 22, TEXT).next_to(P.pt(t_max, c_base), RIGHT, buff=0.28)

        pde = make_pde([3.4, 1.15, 0], color=PDE_COL, active=1.0, scale=0.80)
        pde_lbl = T("PDE5", 24, PDE_COL, weight=BOLD).next_to(pde, DOWN, buff=0.14)
        wedge = make_sildenafil_wedge(scale=0.80).move_to([3.4, 2.45, 0])
        wedge_lbl = T("blocker", 22, TEXT).next_to(wedge, UP, buff=0.10)

        t_tr = ValueTracker(0.0)
        gauge_tr = ValueTracker(c_base / 3.2)
        gauge = make_cgmp_gauge(gauge_tr, [5.35, 0.35, 0], width=0.56, height=2.7,
                                baseline=c_base / 3.2, base_text="")

        self.add(P, base_line, base_lbl, pde, pde_lbl, gauge, tag)
        self.at("Because arteries signal")

        def mk_norm_area():
            x1 = float(t_tr.get_value())
            if x1 <= 0.1:
                return VGroup()
            xs = np.linspace(0.0, x1, max(4, int(x1 * 10)))
            pts = [P.pt(0.0, c_base)] + [P.pt(x, norm_fn(x)) for x in xs] + [P.pt(x1, c_base)]
            return Polygon(*pts, stroke_width=0, fill_color=GREY, fill_opacity=0.20)

        norm_area = always_redraw(mk_norm_area)
        norm_live = P.live_curve(norm_fn, t_tr, color=GREY, width=5.2)
        norm_dot = P.dot(lambda: t_tr.get_value(), lambda: norm_fn(t_tr.get_value()), color=GREY, ring=TEXT, radius=0.13)
        self.add(norm_area, norm_live, norm_dot)
        norm_lbl = T("normal PDE5", 24, TEXT).move_to(P.pt(8.2, 0.92))

        def sync_norm(m):
            gauge_tr.set_value(norm_fn(t_tr.get_value()) / 3.2)

        gauge.add_updater(sync_norm)
        self.play(t_tr.animate.set_value(t_max), FadeIn(norm_lbl, run_time=0.4), run_time=3.5, rate_func=linear)
        gauge.remove_updater(sync_norm)
        self.remove(norm_dot)

        self.at("slowing breakdown")
        self.play(FadeIn(wedge, run_time=0.35), FadeIn(wedge_lbl, run_time=0.35), run_time=0.5)
        self.play(wedge.animate.move_to(pde.pocket + DOWN * 0.04),
                  wedge_lbl.animate.next_to(pde, UP, buff=0.20), run_time=1.0)

        t_blk = ValueTracker(0.0)

        def mk_area():
            x1 = float(t_blk.get_value())
            if x1 <= 0.1:
                return VGroup()
            xs = np.linspace(0.0, x1, max(4, int(x1 * 12)))
            pts = [P.pt(0.0, c_base)] + [P.pt(x, blk_fn(x)) for x in xs] + [P.pt(x1, c_base)]
            return Polygon(*pts, stroke_width=0, fill_color=CGMP_COL, fill_opacity=0.26)

        blk_area = always_redraw(mk_area)
        blk_live = P.live_curve(blk_fn, t_blk, color=CGMP_COL, width=7.5)
        blk_dot = P.dot(lambda: t_blk.get_value(), lambda: blk_fn(t_blk.get_value()), color=CGMP_COL, ring=TEXT, radius=0.14)
        blk_lbl = T("PDE5 blocked", 26, CGMP_COL, weight=BOLD).move_to(P.pt(8.6, 2.65))

        def sync_blk(m):
            gauge_tr.set_value(blk_fn(t_blk.get_value()) / 3.2)

        gauge.add_updater(sync_blk)
        self.add(blk_area, blk_live, blk_dot)
        self.play(t_blk.animate.set_value(4.5), FadeIn(blk_lbl, run_time=0.4), run_time=3.6, rate_func=linear)

        self.at("Same molecule")
        self.play(t_blk.animate.set_value(7.5), run_time=3.5, rate_func=linear)

        self.at("Keep this rule")
        self.play(t_blk.animate.set_value(9.5), run_time=2.5, rate_func=linear)

        self.at("When rising")
        rule = fit_text("When rising cGMP carries the signal, blocking breakdown amplifies it.",
                        max_w=10.6, size=26, color=TEXT, max_lines=1).move_to([-0.9, -3.1, 0])
        self.play(FadeIn(rule, run_time=0.4), t_blk.animate.set_value(11.0), run_time=2.6, rate_func=linear)

        self.at("blocking breakdown")
        self.play(t_blk.animate.set_value(t_max), run_time=1.8, rate_func=linear)
        gauge.remove_updater(sync_blk)
        self.finish()


class S11End(EndCard):
    LINE = "When rising cGMP carries the signal, blocking breakdown amplifies it."
