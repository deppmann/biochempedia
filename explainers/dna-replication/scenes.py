"""What the Halfway Band Means — Meselson & Stahl's CsCl density-gradient experiment.

COLOUR MAP (one colour per concept, entire film):
- PURPLE (#BC8CF2): parental / old (15N) DNA strands
- CYAN   (#58C4DD): new (14N) DNA strands
- GOLD   (#D4A843): experimental observations, observed bands, predict questions
- RED    (#FC6255): eliminated / ruled-out models
- TEXT   (#E8EAF0): primary text, tube outlines, level guides
- GREY   (#8B93A1): subtle structural tick marks inside the CsCl gradient only (never text)

CARRIED WORLD:
A vertical CsCl density-gradient centrifuge tube with computed equilibrium band positions
y(f_old) = y_light + f_old * (y_heavy - y_light) (1.0 = heavy, 0.5 = hybrid, 0.25 = 1/4,
0.0 = light), paired with schematic two-strand DNA duplexes (no molecular structures/bonds).

PER-SCENE CHANGES (computed from the lesson's model):
- s00_hook:        Purple heavy duplex turns continuously; heavy band (f_old=1.0) dissolves into
                   one GOLD band settling at computed halfway position (f_old=0.5); "Why halfway?" appears.
- s01_title:       Standard TitleCard (2.0 s).
- s02_setup:       Purple duplex opens into old strands; cyan partner builds a hybrid; CsCl tube
                   gains computed gradient and guides; heavy (1.0), light (0.0), hybrid (0.5) settle.
- s03_models:      Starting purple duplex transforms in place through Conservative, Semiconservative,
                   and Uniform Dispersive (computed alternating segments), resetting cleanly between each.
- s04_band_meaning: Zoom into GOLD hybrid band -> 18 small duplexes (fixed RNG seed 7) inside fixed
                   band envelope; molecules alternate between intact strands and 50/50 segments.
- s05_predict:     Three tubes appear; each model builds its gen-1 daughters above its tube, then
                   daughters hover gently toward the tubes under the predict question card.
- s06_predict_pause: Standard PredictPause (4.5 s) holding the three tubes, hovering daughters, and question.
- s07_first_test:  Daughters settle to computed y(f_old): Conservative -> 1.0 & 0.0 (RED outline);
                   Semiconservative & Dispersive -> 0.5 (match GOLD observation marker).
- s08_next_round:  Conservative removed; Semiconservative copies 2->4 and settles to 0.5 & 0.0;
                   Dispersive shrinks purple segments 0.5->0.25 as band rises from 0.5 to 0.25.
- s09_observation: GOLD observed tube slides over Semiconservative (0.5 & 0.0 match); Dispersive
                   gets RED outline; purple material is highlighted as conserved across growing cyan.
- s10_scope:       Heat wave sweeps across hybrid duplex; subunits pull apart and tube band splits
                   from 0.5 to 1.0 (heavy) and 0.0 (light); "consistent with strands" & "subunit identity?".
- s11_rule:        Large purple strand grows; cyan blocks join left-to-right; pair aligns with GOLD
                   hybrid band above the label "semiconservative".
- s12_end:         Standard EndCard with the take-home line.
"""
from bp_parts import *

PURPLE = "#BC8CF2"   # parental / old DNA (15N)
CYAN = "#58C4DD"     # new DNA (14N)
LIQUID_COL = "#3D4F6B"  # subtle CsCl solution density column tint

RNG_SEED = 7
TUBE_R = 0.36


def density_y(frac_old, y_light, y_heavy):
    """Map old-DNA fraction (0=light .. 1=heavy) to vertical scene coordinate."""
    return y_light + frac_old * (y_heavy - y_light)


def make_tube(center, width=2.6, height=5.4, outline_color=TEXT, show_guides=True,
              label_side=LEFT, label_buff=0.28, show_gradient=True, label_size=26):
    """Build a CsCl centrifuge tube with computed density gradient and guide heights."""
    cx, cy = center[0], center[1]
    hw = width / 2.0
    top_y = cy + height / 2.0
    bot_y = cy - height / 2.0
    r = min(TUBE_R, hw * 0.45)

    n_arc = 16
    bot_pts = []
    for i in range(n_arc + 1):
        ang = PI + PI * i / n_arc
        px = cx + hw * np.cos(ang)
        py = (bot_y + r * 1.35) + r * 1.35 * np.sin(ang)
        bot_pts.append([px, py, 0])

    meniscus_y = top_y - 0.35
    y_light = bot_y + height * 0.72
    y_heavy = bot_y + height * 0.20
    y_hybrid = density_y(0.5, y_light, y_heavy)

    # Computed CsCl liquid density column (opacity increases linearly from light top to heavy bottom)
    liquid = VGroup()
    if show_gradient:
        n_slices = 14
        col_top = meniscus_y
        col_bot = bot_y + r * 0.55
        sh = (col_top - col_bot) / n_slices
        for k in range(n_slices):
            frac = (k + 0.5) / n_slices  # 0 at top (light), 1 at bottom (heavy)
            yk = col_top - (k + 0.5) * sh
            sl = Rectangle(width=width - 0.08, height=sh + 0.01, stroke_width=0,
                           fill_color=LIQUID_COL, fill_opacity=0.14 + 0.30 * frac).move_to([cx, yk, 0])
            liquid.add(sl)

    wall = VMobject(stroke_color=outline_color, stroke_width=4.5, fill_opacity=0)
    wall.set_points_as_corners([[cx - hw, top_y, 0]] + bot_pts + [[cx + hw, top_y, 0]])
    lip = Line([cx - hw - 0.12, top_y, 0], [cx + hw + 0.12, top_y, 0], color=outline_color, stroke_width=5)
    meniscus = Line([cx - hw + 0.06, meniscus_y, 0], [cx + hw - 0.06, meniscus_y, 0],
                    color=outline_color, stroke_width=2.2).set_opacity(0.55)

    g = VGroup(liquid, wall, lip, meniscus)
    g.liquid = liquid
    g.wall = wall
    g.lip = lip
    g.cx = cx
    g.cy = cy
    g.tube_w = width
    g.tube_h = height
    g.inner_w = width - 0.24
    g.y_light = y_light
    g.y_hybrid = y_hybrid
    g.y_heavy = y_heavy
    g.top_y = top_y
    g.bot_y = bot_y

    if show_gradient:
        grad_ticks = VGroup()
        for k in range(9):
            f = k / 8.0
            yk = density_y(f, y_light + 0.35, y_heavy - 0.35)
            tk_len = 0.10 + 0.14 * f
            tk = Line([cx + hw - 0.10 - tk_len, yk, 0], [cx + hw - 0.10, yk, 0],
                      color=GREY, stroke_width=2.2).set_opacity(0.45 + 0.45 * f)
            grad_ticks.add(tk)
        g.grad_ticks = grad_ticks
        g.add(grad_ticks)
    else:
        g.grad_ticks = VGroup()

    guides = VGroup()
    labels = VGroup()
    if show_guides:
        for name, yy in (("light", y_light), ("hybrid", y_hybrid), ("heavy", y_heavy)):
            ln = DashedLine([cx - hw + 0.08, yy, 0], [cx + hw - 0.08, yy, 0],
                            color=GREY, stroke_width=2.4, dash_length=0.12).set_opacity(0.65)
            guides.add(ln)
            if label_side is not None:
                lb = T(name, size=label_size, color=TEXT)
                edge_x = cx - hw if np.allclose(label_side, LEFT) else cx + hw
                lb.next_to([edge_x, yy, 0], label_side, buff=label_buff)
                labels.add(lb)
        g.add(guides, labels)
    g.guides = guides
    g.labels = labels
    return g


def make_band(tube, frac_old, color=GOLD, thickness=0.26, opacity=0.95, width_scale=0.92):
    """A crisp density band positioned at computed y(frac_old) inside `tube`."""
    y = density_y(frac_old, tube.y_light, tube.y_heavy)
    w = tube.inner_w * width_scale
    core = RoundedRectangle(corner_radius=thickness * 0.42, width=w, height=thickness,
                            stroke_width=0, fill_color=color, fill_opacity=opacity).move_to([tube.cx, y, 0])
    halo = RoundedRectangle(corner_radius=thickness * 0.65, width=w * 0.96, height=thickness * 1.45,
                            stroke_width=0, fill_color=color, fill_opacity=opacity * 0.28).move_to([tube.cx, y, 0])
    return VGroup(halo, core)


def live_band(tube, frac_tracker, color=GOLD, thickness=0.26, opacity_tracker=None, width_scale=0.92):
    """Band whose vertical position (and optional opacity) tracks a ValueTracker."""
    def mk():
        op = 0.95 if opacity_tracker is None else float(np.clip(opacity_tracker.get_value(), 0.0, 0.95))
        return make_band(tube, frac_tracker.get_value(), color=color, thickness=thickness,
                         opacity=op, width_scale=width_scale)
    return always_redraw(mk)


def make_strand_bar(center, width=2.4, height=0.16, color=PURPLE):
    """One schematic single DNA strand (rounded bar, no molecular bonds)."""
    return RoundedRectangle(corner_radius=height * 0.45, width=width, height=height,
                            stroke_width=0, fill_color=color, fill_opacity=1.0).move_to(center)


def make_duplex(center, width=2.4, gap=0.20, top_color=PURPLE, bot_color=PURPLE,
                strand_h=0.15, segments=0, old_frac=0.5):
    """Schematic two-strand DNA duplex (either solid strands or alternating purple/cyan segments)."""
    cx, cy = center[0], center[1]
    dy = gap / 2.0 + strand_h / 2.0
    if segments <= 0:
        top = make_strand_bar([cx, cy + dy, 0], width=width, height=strand_h, color=top_color)
        bot = make_strand_bar([cx, cy - dy, 0], width=width, height=strand_h, color=bot_color)
        g = VGroup(top, bot)
        g.top_strand, g.bot_strand = top, bot
        return g

    unit_w = width / segments
    inner_gap = min(0.05, unit_w * 0.10)
    usable_w = unit_w - inner_gap
    top_segs, bot_segs = VGroup(), VGroup()
    x_start = cx - width / 2.0 + inner_gap / 2.0
    for row_grp, y_row, phase_shift in ((top_segs, cy + dy, 0), (bot_segs, cy - dy, 1)):
        for i in range(segments):
            ux = x_start + i * unit_w
            pw = max(0.01, usable_w * old_frac)
            cw = max(0.01, usable_w * (1.0 - old_frac))
            if (i + phase_shift) % 2 == 0:
                a_w, a_c, b_w, b_c = pw, PURPLE, cw, CYAN
            else:
                a_w, a_c, b_w, b_c = cw, CYAN, pw, PURPLE
            r1 = RoundedRectangle(corner_radius=0.04, width=a_w, height=strand_h,
                                  stroke_width=0, fill_color=a_c, fill_opacity=1.0).move_to([ux + a_w / 2.0, y_row, 0])
            r2 = RoundedRectangle(corner_radius=0.04, width=b_w, height=strand_h,
                                  stroke_width=0, fill_color=b_c, fill_opacity=1.0).move_to([ux + a_w + b_w / 2.0, y_row, 0])
            row_grp.add(r1, r2)
    g = VGroup(top_segs, bot_segs)
    g.top_strand, g.bot_strand = top_segs, bot_segs
    return g


def make_turning_duplex(center, length=4.2, amp=0.40, phase=0.0, cycles=2.0,
                        color_a=PURPLE, color_b=PURPLE, stroke_w=13):
    """Computed parametric two-strand wave turning cleanly around its axis (no bonds)."""
    cx, cy = center[0], center[1]
    u = np.linspace(-0.5, 0.5, 90)
    theta = 2.0 * PI * cycles * u + phase
    xa = cx + u * length
    ya = cy + amp * np.sin(theta)
    yb = cy + amp * np.sin(theta + PI)
    pts_a = np.column_stack([xa, ya, np.zeros_like(u)])
    pts_b = np.column_stack([xa, yb, np.zeros_like(u)])
    s_a = VMobject(stroke_color=color_a, stroke_width=stroke_w, fill_opacity=0).set_points_as_corners(pts_a)
    s_b = VMobject(stroke_color=color_b, stroke_width=stroke_w, fill_opacity=0).set_points_as_corners(pts_b)
    return VGroup(s_a, s_b)


def make_tube_red_frame(tube):
    """A tight RED elimination border closing around an eliminated tube (clear of outer labels and lip)."""
    return RoundedRectangle(corner_radius=0.20, width=tube.tube_w + 0.34, height=tube.tube_h + 0.28,
                            stroke_color=RED, stroke_width=4.5, fill_opacity=0).move_to([tube.cx, tube.cy, 0])


# ==============================================================================
# S00: HOOK (14.475 s)
# ==============================================================================
class S00Hook(SpokenScene):
    def construct(self):
        # Place tube at x=1.9 so right-side "halfway" label stays well inside frame
        tube = make_tube(center=[1.9, 0.05, 0], width=3.0, height=5.7,
                         outline_color=TEXT, show_guides=True, label_side=LEFT, label_buff=0.25,
                         show_gradient=True, label_size=28)
        tube.labels[1].set_opacity(0)  # keep "light" and "heavy" visible; hide "hybrid" word in hook

        heavy_op = ValueTracker(0.95)
        gold_frac = ValueTracker(1.0)
        gold_op = ValueTracker(0.0)
        phi = ValueTracker(0.0)

        heavy_band = always_redraw(lambda: make_band(tube, 1.0, color=PURPLE, thickness=0.28,
                                                     opacity=heavy_op.get_value()))
        gold_band = live_band(tube, gold_frac, color=GOLD, thickness=0.28, opacity_tracker=gold_op)
        duplex = always_redraw(lambda: make_turning_duplex(center=[-3.2, 0.65, 0], length=4.6, amp=0.45,
                                                           phase=phi.get_value(), cycles=2.0,
                                                           color_a=PURPLE, color_b=PURPLE, stroke_w=13))
        phi.add_updater(lambda m, dt: m.increment_value(1.6 * dt))

        gen_val = ValueTracker(0.0)
        gen_readout = counter("generation {:.1f}", gen_val, at=[-3.2, 2.45, 0], size=32, color=TEXT)
        stag = scope_tag("schematic", size=24, color=TEXT)

        self.add(tube, heavy_band, gold_band, duplex, gen_readout, stag, phi)

        # Switched to ordinary nitrogen: generation 0 -> 1, purple heavy band dissolves into rising GOLD band
        self.at("switched to ordinary")
        self.play(
            gen_val.animate.set_value(1.0),
            heavy_op.animate.set_value(0.0),
            gold_op.animate.set_value(0.95),
            gold_frac.animate.set_value(0.5),
            run_time=4.2,
            rate_func=smooth,
        )

        # "That band sat halfway between heavy and light."
        self.at("halfway between heavy")
        y_top, y_mid, y_bot = tube.y_light, tube.y_hybrid, tube.y_heavy
        rx = tube.cx + tube.width / 2.0 + 0.25
        eq_top = BraceBetweenPoints([rx, y_mid, 0], [rx, y_top, 0], direction=RIGHT, color=GOLD)
        eq_bot = BraceBetweenPoints([rx, y_bot, 0], [rx, y_mid, 0], direction=RIGHT, color=GOLD)
        half_tag = T("halfway", size=28, color=GOLD).next_to(VGroup(eq_top, eq_bot), RIGHT, buff=0.18)
        self.play(FadeIn(eq_top), FadeIn(eq_bot), FadeIn(half_tag), run_time=1.0)

        # "Why did none remain fully heavy?"
        self.at("Why did none")
        q_box = boxed_label("Why halfway?", color=GOLD, size=36, pad=0.28).move_to([-3.2, -1.45, 0])
        self.play(FadeIn(q_box, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ==============================================================================
# S01: TITLE CARD (2.0 s, silent)
# ==============================================================================
class S01Title(TitleCard):
    LESSON = "DNA Replication: Semiconservative Copying and Its Machinery"
    TITLE = "What the Halfway Band Means"


# ==============================================================================
# S02: SETUP (20.175 s)
# ==============================================================================
class S02Setup(SpokenScene):
    def construct(self):
        tube = make_tube(center=[2.8, 0.0, 0], width=3.0, height=5.7,
                         outline_color=TEXT, show_guides=False, label_side=LEFT, show_gradient=False)
        stag = scope_tag("schematic", size=24, color=TEXT)
        phi = ValueTracker(0.0)
        amp_t = ValueTracker(0.42)
        turn_duplex = always_redraw(lambda: make_turning_duplex(center=[-3.2, 0.85, 0], length=4.4,
                                                                amp=amp_t.get_value(), phase=phi.get_value(),
                                                                cycles=2.0, color_a=PURPLE, color_b=PURPLE, stroke_w=13))
        phi.add_updater(lambda m, dt: m.increment_value(1.5 * dt))
        self.add(tube, turn_duplex, stag, phi)

        # "To follow old DNA, Meselson and Stahl grew cells with heavy nitrogen."
        self.at("grew cells with")
        self.play(amp_t.animate.set_value(0.10), run_time=1.8, rate_func=smooth)

        # "Old strands appear purple" -> straighten into two separated purple strands; label clearly above
        self.at("Old strands appear")
        phi.clear_updaters()
        self.remove(turn_duplex, phi)
        p_top = make_strand_bar([-3.2, 1.35, 0], width=4.2, height=0.20, color=PURPLE)
        p_bot = make_strand_bar([-3.2, 0.35, 0], width=4.2, height=0.20, color=PURPLE)
        self.add(p_top, p_bot)
        old_lbl = T("old strands", size=28, color=PURPLE).move_to([-3.2, 2.25, 0])
        self.play(
            p_top.animate.move_to([-3.2, 1.55, 0]),
            p_bot.animate.move_to([-3.2, -0.25, 0]),
            FadeIn(old_lbl),
            run_time=1.3,
        )

        # "strands built after the switch appear cyan." -> cyan strand slides beside top purple strand
        self.at("strands built after")
        c_new = make_strand_bar([-3.2, -2.0, 0], width=4.2, height=0.20, color=CYAN)
        new_lbl = T("new strand", size=28, color=CYAN).move_to([-3.2, 0.45, 0])
        self.play(
            FadeOut(p_bot, run_time=0.45),
            c_new.animate.move_to([-3.2, 1.15, 0]),
            FadeIn(new_lbl),
            run_time=1.4,
        )

        # "In a cesium chloride gradient, heavy DNA settles lower than light DNA."
        self.at("cesium chloride gradient")
        tube_full = make_tube(center=[2.8, 0.0, 0], width=3.0, height=5.7,
                              outline_color=TEXT, show_guides=True, label_side=LEFT, label_buff=0.26,
                              show_gradient=True, label_size=28)
        grad_title = T("CsCl gradient", size=28, color=TEXT).next_to(tube_full.lip, UP, buff=0.18)
        self.play(
            FadeIn(tube_full.liquid),
            FadeIn(tube_full.grad_ticks),
            FadeIn(tube_full.guides),
            FadeIn(tube_full.labels),
            FadeIn(grad_title),
            run_time=1.2,
        )

        # Heavy purple duplex settles low (starts centered above tube mouth, clear of labels)
        self.at("heavy DNA settles")
        ref_heavy = make_duplex([-3.2, tube_full.y_heavy, 0], width=2.4, gap=0.18,
                                top_color=PURPLE, bot_color=PURPLE, strand_h=0.15)
        mini_h = make_duplex([tube_full.cx, tube_full.top_y - 0.1, 0], width=1.9, gap=0.14,
                             top_color=PURPLE, bot_color=PURPLE, strand_h=0.11)
        self.play(FadeIn(ref_heavy, run_time=0.4), mini_h.animate.move_to([tube_full.cx, tube_full.y_heavy, 0]), run_time=1.1)
        band_h = make_band(tube_full, 1.0, color=PURPLE, thickness=0.26)
        self.play(FadeOut(mini_h, run_time=0.25), FadeIn(band_h, run_time=0.35))

        # Light cyan duplex settles high
        self.at("than light")
        ref_light = make_duplex([-3.2, tube_full.y_light, 0], width=2.4, gap=0.18,
                                top_color=CYAN, bot_color=CYAN, strand_h=0.15)
        mini_l = make_duplex([tube_full.cx, tube_full.top_y - 0.1, 0], width=1.9, gap=0.14,
                             top_color=CYAN, bot_color=CYAN, strand_h=0.11)
        # Move old_lbl/new_lbl/hybrid pair neatly to hybrid height or keep legend clean above!
        self.play(
            FadeOut(old_lbl, run_time=0.3),
            FadeOut(new_lbl, run_time=0.3),
            VGroup(p_top, c_new).animate.scale(0.57).move_to([-3.2, tube_full.y_hybrid, 0]),
            FadeIn(ref_light, run_time=0.4),
            mini_l.animate.move_to([tube_full.cx, tube_full.y_light, 0]),
            run_time=1.1,
        )
        band_l = make_band(tube_full, 0.0, color=CYAN, thickness=0.26)
        self.play(FadeOut(mini_l, run_time=0.25), FadeIn(band_l, run_time=0.35))

        # "Hybrid DNA settles between them."
        self.at("Hybrid DNA settles")
        mini_m = make_duplex([-3.2, tube_full.y_hybrid, 0], width=2.4, gap=0.18,
                             top_color=PURPLE, bot_color=CYAN, strand_h=0.15)
        self.add(mini_m)  # keep reference hybrid duplex on left beside hybrid level!
        self.play(
            VGroup(p_top, c_new).animate.move_to([tube_full.cx, tube_full.y_hybrid, 0]),
            run_time=1.2,
        )
        band_m = make_band(tube_full, 0.5, color=GOLD, thickness=0.28)
        self.play(FadeOut(VGroup(p_top, c_new), run_time=0.25), FadeIn(band_m, run_time=0.45))
        self.finish()


# ==============================================================================
# S03: THREE MODELS (24.625 s)
# ==============================================================================
class S03Models(SpokenScene):
    def construct(self):
        stag = scope_tag("schematic", size=24, color=TEXT)
        model_lbl = T("three models", size=36, color=PURPLE).move_to([0, 2.95, 0])
        parent = make_duplex([0, 0.0, 0], width=6.6, gap=0.34, top_color=PURPLE, bot_color=PURPLE, strand_h=0.26)
        self.add(model_lbl, stag)
        self.play(GrowFromEdge(parent, LEFT), run_time=2.2)

        # Beat 1: Conservative
        self.at("Conservative copying")
        lbl_con = T("conservative", size=38, color=TEXT).move_to([0, 2.95, 0])
        self.play(FadeOut(model_lbl, run_time=0.25))
        self.play(FadeIn(lbl_con, run_time=0.25))

        c_top = make_strand_bar([-3.3, -1.05, 0], width=0.05, height=0.26, color=CYAN)
        c_bot = make_strand_bar([-3.3, -1.65, 0], width=0.05, height=0.26, color=CYAN)
        target_c_top = make_strand_bar([0, -1.05, 0], width=6.6, height=0.26, color=CYAN)
        target_c_bot = make_strand_bar([0, -1.65, 0], width=6.6, height=0.26, color=CYAN)
        self.play(parent.animate.move_to([0, 1.35, 0]), run_time=1.0)
        self.add(c_top, c_bot)
        self.play(
            Transform(c_top, target_c_top),
            Transform(c_bot, target_c_bot),
            run_time=2.6,
            rate_func=smooth,
        )

        # Beat 2: Semiconservative (reset smoothly without ghosting)
        self.at("Semi")
        lbl_semi = T("semiconservative", size=38, color=TEXT).move_to([0, 2.95, 0])
        self.play(FadeOut(lbl_con, run_time=0.22), FadeOut(c_top, run_time=0.3), FadeOut(c_bot, run_time=0.3))
        self.play(FadeIn(lbl_semi, run_time=0.22), parent.animate.move_to([0, 0.0, 0]), run_time=0.6)

        self.at("separates the old")
        self.play(
            parent.top_strand.animate.move_to([0, 1.65, 0]),
            parent.bot_strand.animate.move_to([0, -1.05, 0]),
            run_time=1.3,
        )

        self.at("gives each a new")
        sc_top = make_strand_bar([-3.3, 1.05, 0], width=0.05, height=0.26, color=CYAN)
        sc_bot = make_strand_bar([-3.3, -1.65, 0], width=0.05, height=0.26, color=CYAN)
        t_sc_top = make_strand_bar([0, 1.05, 0], width=6.6, height=0.26, color=CYAN)
        t_sc_bot = make_strand_bar([0, -1.65, 0], width=6.6, height=0.26, color=CYAN)
        self.add(sc_top, sc_bot)
        self.play(Transform(sc_top, t_sc_top), Transform(sc_bot, t_sc_bot), run_time=1.8)

        # Beat 3: Uniform dispersive (clean reset)
        self.at("Uniform dispersive")
        lbl_disp = T("uniform dispersive", size=38, color=TEXT).move_to([0, 2.95, 0])
        fresh_parent = make_duplex([0, 0.0, 0], width=6.6, gap=0.34, top_color=PURPLE, bot_color=PURPLE, strand_h=0.26)
        self.play(FadeOut(lbl_semi, run_time=0.22), FadeOut(sc_top, run_time=0.25), FadeOut(sc_bot, run_time=0.25), FadeOut(parent, run_time=0.25))
        self.play(FadeIn(lbl_disp, run_time=0.22), FadeIn(fresh_parent, run_time=0.4))

        self.at("breaks the old")
        broken_segs = VGroup()
        seg_u = 6.6 / 4.0
        for row_y, shift_i in ((0.30, 0), (-0.30, 1)):
            for i in range(4):
                sx = -3.3 + (i + (0.25 if (i + shift_i) % 2 == 0 else 0.75)) * seg_u
                r = RoundedRectangle(corner_radius=0.05, width=seg_u * 0.45, height=0.26,
                                     stroke_width=0, fill_color=PURPLE, fill_opacity=1.0).move_to([sx, row_y, 0])
                broken_segs.add(r)
        self.play(ReplacementTransform(fresh_parent, broken_segs), run_time=1.5)

        self.at("mixes those segments")
        d1 = make_duplex([0, 1.35, 0], width=6.6, gap=0.34, strand_h=0.26, segments=4, old_frac=0.5)
        d2 = make_duplex([0, -1.35, 0], width=6.6, gap=0.34, strand_h=0.26, segments=4, old_frac=0.5)
        self.play(ReplacementTransform(broken_segs, VGroup(d1, d2)), run_time=2.2)
        self.finish()


# ==============================================================================
# S04: BAND MEANING (21.85 s)
# ==============================================================================
class S04BandMeaning(SpokenScene):
    def construct(self):
        tube = make_tube(center=[0, 0.0, 0], width=3.2, height=5.7,
                         outline_color=TEXT, show_guides=True, label_side=LEFT, label_buff=0.26,
                         show_gradient=True, label_size=28)
        band = make_band(tube, 0.5, color=GOLD, thickness=0.30)
        stag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tube, band, stag)

        rng = np.random.default_rng(RNG_SEED)
        positions = []
        cols, rows = 3, 6
        for r in range(rows):
            for c in range(cols):
                px = -3.6 + c * 2.7 + rng.uniform(-0.18, 0.18)
                py = -1.65 + r * 0.66 + rng.uniform(-0.07, 0.07)
                positions.append([px, py, 0])

        intact_crowd = VGroup(*[
            make_duplex(p, width=1.85, gap=0.12, top_color=PURPLE, bot_color=CYAN, strand_h=0.11)
            for p in positions
        ])
        disp_crowd = VGroup(*[
            make_duplex(p, width=1.85, gap=0.12, strand_h=0.11, segments=4, old_frac=0.5)
            for p in positions
        ])
        band_box = RoundedRectangle(corner_radius=0.25, width=8.6, height=4.5,
                                    stroke_color=GOLD, stroke_width=3.5,
                                    fill_color=GOLD, fill_opacity=0.07).move_to([-0.9, 0.0, 0])

        # Clear tube BEFORE expanding band_box so no transient label overlap happens
        self.at("marks many DNA")
        self.play(FadeOut(tube, run_time=0.4))
        self.play(ReplacementTransform(band, band_box), FadeIn(intact_crowd, lag_ratio=0.04), run_time=1.9)

        self.at("same buoyant density")
        b_brace = Brace(band_box, RIGHT, color=GOLD)
        b_lbl = T("same buoyant\ndensity", size=28, color=GOLD).next_to(b_brace, RIGHT, buff=0.20)
        tight_crowd = VGroup(*[
            make_duplex([p[0], p[1] * 0.88, 0], width=1.85, gap=0.12, top_color=PURPLE, bot_color=CYAN, strand_h=0.11)
            for p in positions
        ])
        self.play(Create(b_brace), FadeIn(b_lbl), Transform(intact_crowd, tight_crowd), run_time=2.6)

        # "One intermediate band could mean every molecule is half old."
        self.at("every molecule is")
        half_lbl = T("every molecule: half old", size=28, color=TEXT).move_to([-0.9, 2.75, 0])
        open_crowd = VGroup(*[
            make_duplex([p[0], p[1] * 0.88, 0], width=1.85, gap=0.24, top_color=PURPLE, bot_color=CYAN, strand_h=0.11)
            for p in positions
        ])
        self.play(FadeIn(half_lbl, run_time=0.6), Transform(intact_crowd, open_crowd, run_time=3.8))

        # "whether that half is one intact strand or many segments"
        self.at("one intact strand")
        lbl_intact = T("one intact strand", size=30, color=PURPLE).move_to([-0.9, -2.85, 0])
        closed_crowd = VGroup(*[
            make_duplex(p, width=1.85, gap=0.12, top_color=PURPLE, bot_color=CYAN, strand_h=0.11)
            for p in positions
        ])
        self.play(FadeIn(lbl_intact, run_time=0.45), Transform(intact_crowd, closed_crowd, run_time=1.0))

        self.at("or many segments")
        lbl_segs = T("many segments", size=30, color=CYAN).move_to([-0.9, -2.85, 0])
        self.play(FadeOut(lbl_intact, run_time=0.20), FadeIn(lbl_segs, run_time=0.25))
        self.play(Transform(intact_crowd, disp_crowd), run_time=1.4)

        # "until another generation separates their predictions."
        self.at("until another generation")
        split_crowd = VGroup()
        for idx, p in enumerate(positions):
            if idx // cols >= 3:
                split_crowd.add(make_duplex(p, width=1.85, gap=0.12, top_color=PURPLE, bot_color=CYAN, strand_h=0.11))
            else:
                split_crowd.add(make_duplex(p, width=1.85, gap=0.12, strand_h=0.11, segments=4, old_frac=0.5))
        lbl_both = T("same band — two internal patterns", size=28, color=GOLD).move_to([-0.9, -2.85, 0])
        self.play(FadeOut(lbl_segs, run_time=0.20), FadeIn(lbl_both, run_time=0.30))
        self.play(Transform(intact_crowd, split_crowd), run_time=1.9)
        self.finish()


# ==============================================================================
# SHARED BUILDER FOR S05 + S06 + S07
# ==============================================================================
THREE_TUBE_XS = (-3.6, 0.0, 3.6)
THREE_MODELS = ("conservative", "semiconservative", "uniform dispersive")


def build_three_tubes_world():
    """Three CsCl tubes across the frame with model headings above."""
    tubes, heads = VGroup(), VGroup()
    for i, (x, name) in enumerate(zip(THREE_TUBE_XS, THREE_MODELS)):
        lside = LEFT if i == 0 else None
        t = make_tube(center=[x, -0.35, 0], width=2.1, height=3.8,
                      outline_color=TEXT, show_guides=True, label_side=lside,
                      label_buff=0.30, show_gradient=True, label_size=24)
        h = T(name, size=28, color=TEXT).move_to([x, 3.15, 0])
        tubes.add(t)
        heads.add(h)
    return tubes, heads


def build_gen1_hover_daughters():
    """Two initial daughters hovering above each of the three tubes."""
    y_top, y_bot = 2.40, 1.92
    d_con = VGroup(
        make_duplex([THREE_TUBE_XS[0], y_top, 0], width=1.75, gap=0.12, top_color=PURPLE, bot_color=PURPLE, strand_h=0.10),
        make_duplex([THREE_TUBE_XS[0], y_bot, 0], width=1.75, gap=0.12, top_color=CYAN, bot_color=CYAN, strand_h=0.10),
    )
    d_semi = VGroup(
        make_duplex([THREE_TUBE_XS[1], y_top, 0], width=1.75, gap=0.12, top_color=PURPLE, bot_color=CYAN, strand_h=0.10),
        make_duplex([THREE_TUBE_XS[1], y_bot, 0], width=1.75, gap=0.12, top_color=PURPLE, bot_color=CYAN, strand_h=0.10),
    )
    d_disp = VGroup(
        make_duplex([THREE_TUBE_XS[2], y_top, 0], width=1.75, gap=0.12, strand_h=0.10, segments=4, old_frac=0.5),
        make_duplex([THREE_TUBE_XS[2], y_bot, 0], width=1.75, gap=0.12, strand_h=0.10, segments=4, old_frac=0.5),
    )
    return VGroup(d_con, d_semi, d_disp)


# ==============================================================================
# S05: PREDICT (9.775 s)
# ==============================================================================
class S05Predict(SpokenScene):
    def construct(self):
        tubes, heads = build_three_tubes_world()
        daughters = build_gen1_hover_daughters()
        stag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tubes, heads, stag)

        starts = VGroup(*[
            make_duplex([x, 2.16, 0], width=1.75, gap=0.12, top_color=PURPLE, bot_color=PURPLE, strand_h=0.10)
            for x in THREE_TUBE_XS
        ])
        self.play(FadeIn(starts), run_time=0.6)
        self.play(ReplacementTransform(starts, daughters), run_time=2.2)

        self.at("which models can")
        q = question_card("Which can make only a hybrid band?", y=-2.95, color=GOLD, size=30)
        self.play(FadeIn(q.question), run_time=0.9)

        for idx, d in enumerate(daughters):
            bob(d, amp=0.08, speed=2.2, seed=idx)
        self.wait(4.5)
        for d in daughters:
            d.clear_updaters()
        self.finish()


# ==============================================================================
# S06: PREDICT PAUSE (4.5 s, silent)
# ==============================================================================
class S06PredictPause(PredictPause):
    QUESTION = "Which can make only a hybrid band?"
    CARD = {"y": -2.95, "size": 30}
    RING_AT = (5.85, -2.05, 0)  # clearly above "schematic" and right of tube 3
    SECONDS = 4.5

    def backdrop(self):
        tubes, heads = build_three_tubes_world()
        daughters = build_gen1_hover_daughters()
        return VGroup(tubes, heads, daughters, scope_tag("schematic", size=24, color=TEXT))


# ==============================================================================
# S07: FIRST TEST (26.3 s)
# ==============================================================================
class S07FirstTest(SpokenScene):
    def construct(self):
        tubes, heads = build_three_tubes_world()
        daughters = build_gen1_hover_daughters()
        stag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tubes, heads, daughters, stag)

        d_con, d_semi, d_disp = daughters
        t_con, t_semi, t_disp = tubes

        # "Conservative copying makes one heavy duplex and one light duplex."
        self.at("Conservative copying")
        self.play(
            d_con[0].animate.scale(0.85).move_to([t_con.cx, t_con.y_heavy, 0]),
            d_con[1].animate.scale(0.85).move_to([t_con.cx, t_con.y_light, 0]),
            run_time=3.5,
        )
        b_con_h = make_band(t_con, 1.0, color=PURPLE, thickness=0.22)
        b_con_l = make_band(t_con, 0.0, color=CYAN, thickness=0.22)
        self.play(
            FadeOut(d_con, run_time=0.45),
            FadeIn(b_con_h, run_time=0.8),
            FadeIn(b_con_l, run_time=0.8),
        )

        # "A single hybrid band, after one generation, rules out conservative copying."
        # Start obs_line at left wall of tube 0 (never crossing "hybrid" label!)
        self.at("single hybrid band")
        obs_y = t_con.y_hybrid
        obs_line = DashedLine([t_con.cx - t_con.tube_w / 2.0 - 0.05, obs_y, 0],
                              [t_disp.cx + t_disp.tube_w / 2.0 + 0.15, obs_y, 0],
                              color=GOLD, stroke_width=3.2, dash_length=0.16)
        obs_zone = Rectangle(width=t_disp.cx - t_con.cx + t_con.tube_w, height=0.26,
                             stroke_width=0, fill_color=GOLD, fill_opacity=0.16).move_to([0.0, obs_y, 0])
        obs_tag = T("observed", size=26, color=GOLD).next_to([t_disp.cx + t_disp.tube_w / 2.0 + 0.20, obs_y, 0],
                                                            UR, buff=0.12)
        self.play(Create(obs_line), FadeIn(obs_zone), FadeIn(obs_tag), run_time=2.2)

        self.at("rules out conservative")
        red_frame = make_tube_red_frame(t_con)
        ruled_lbl = T("ruled out", size=26, color=RED).move_to([t_con.cx, -2.75, 0])
        self.play(
            Create(red_frame),
            FadeIn(ruled_lbl),
            heads[0].animate.set_color(RED),
            t_con.wall.animate.set_stroke(RED, opacity=0.75),
            b_con_h.animate.set_opacity(0.32),
            b_con_l.animate.set_opacity(0.32),
            FadeOut(obs_zone, run_time=0.6),
            run_time=2.4,
        )

        # "Semiconservative copying makes two purple-cyan hybrids."
        self.at("Semiconservative copying")
        self.play(
            d_semi[0].animate.scale(0.85).move_to([t_semi.cx, t_semi.y_hybrid + 0.07, 0]),
            d_semi[1].animate.scale(0.85).move_to([t_semi.cx, t_semi.y_hybrid - 0.07, 0]),
            run_time=3.2,
        )
        b_semi_m = make_band(t_semi, 0.5, color=GOLD, thickness=0.25)
        self.play(FadeOut(d_semi, run_time=0.4), FadeIn(b_semi_m, run_time=0.9))

        # "Uniform dispersive copying can also put equal old and new material in every molecule."
        self.at("Uniform dispersive")
        self.play(
            d_disp[0].animate.scale(0.85).move_to([t_disp.cx, t_disp.y_hybrid + 0.07, 0]),
            d_disp[1].animate.scale(0.85).move_to([t_disp.cx, t_disp.y_hybrid - 0.07, 0]),
            run_time=3.8,
        )
        b_disp_m = make_band(t_disp, 0.5, color=GOLD, thickness=0.25)
        self.play(FadeOut(d_disp, run_time=0.4), FadeIn(b_disp_m, run_time=1.0))

        # "Both survive the initial test."
        self.at("Both survive the")
        mark_s = SurroundingRectangle(b_semi_m, color=GOLD, buff=0.06, stroke_width=3.2, corner_radius=0.08)
        mark_d = SurroundingRectangle(b_disp_m, color=GOLD, buff=0.06, stroke_width=3.2, corner_radius=0.08)
        surv_s = T("survives", size=26, color=GOLD).move_to([t_semi.cx, -2.75, 0])
        surv_d = T("survives", size=26, color=GOLD).move_to([t_disp.cx, -2.75, 0])
        self.play(
            Create(mark_s), Create(mark_d),
            FadeIn(surv_s), FadeIn(surv_d),
            heads[1].animate.set_color(GOLD),
            heads[2].animate.set_color(GOLD),
            run_time=1.8,
        )
        self.finish()


# ==============================================================================
# SHARED BUILDER FOR S08 + S09 (2-lane comparison)
# ==============================================================================
def build_two_lane_tubes():
    """Inner pair of tubes (x=-2.0 and x=+2.0) leaving generous 2.0-unit center gap for guides."""
    t_semi = make_tube(center=[-2.0, -0.15, 0], width=2.0, height=5.0,
                       outline_color=TEXT, show_guides=True, label_side=None, show_gradient=True, label_size=24)
    t_disp = make_tube(center=[2.0, -0.15, 0], width=2.0, height=5.0,
                       outline_color=TEXT, show_guides=True, label_side=None, show_gradient=True, label_size=24)
    center_labels = VGroup()
    for name, yy in (("light", t_semi.y_light), ("hybrid", t_semi.y_hybrid), ("heavy", t_semi.y_heavy)):
        center_labels.add(T(name, size=26, color=TEXT).move_to([0.0, yy, 0]))
    h_semi = T("semiconservative", size=30, color=TEXT).move_to([-4.35, 3.10, 0])
    h_disp = T("uniform dispersive", size=30, color=TEXT).move_to([4.35, 3.10, 0])
    return t_semi, t_disp, center_labels, h_semi, h_disp


# ==============================================================================
# S08: NEXT ROUND — GENERATION 2 (26.1 s)
# ==============================================================================
class S08NextRound(SpokenScene):
    def construct(self):
        t_semi, t_disp, center_labels, h_semi, h_disp = build_two_lane_tubes()
        stag = scope_tag("schematic", size=24, color=TEXT)

        b_semi_g1 = make_band(t_semi, 0.5, color=GOLD, thickness=0.22)
        disp_frac = ValueTracker(0.5)
        disp_band = live_band(t_disp, disp_frac, color=GOLD, thickness=0.22)

        semi_g1 = VGroup(
            make_duplex([-4.9, 1.1, 0], width=2.3, gap=0.18, top_color=PURPLE, bot_color=CYAN, strand_h=0.14),
            make_duplex([-4.9, -1.3, 0], width=2.3, gap=0.18, top_color=PURPLE, bot_color=CYAN, strand_h=0.14),
        )
        disp_g1 = VGroup(
            make_duplex([4.9, 1.1, 0], width=2.3, gap=0.18, strand_h=0.14, segments=4, old_frac=0.5),
            make_duplex([4.9, -1.3, 0], width=2.3, gap=0.18, strand_h=0.14, segments=4, old_frac=0.5),
        )
        gen_t = ValueTracker(1.0)
        gen_c = counter("generation {:.0f}", gen_t, at=[0.0, 3.10, 0], size=28, color=GOLD)

        self.add(t_semi, t_disp, center_labels, h_semi, h_disp, b_semi_g1, disp_band, semi_g1, disp_g1, gen_c, stag)

        # "Now let the survivors copy again in ordinary nitrogen."
        self.at("copy again")
        ys4 = (1.75, 0.55, -0.65, -1.85)
        s0_p, s0_c = semi_g1[0].top_strand, semi_g1[0].bot_strand
        s1_p, s1_c = semi_g1[1].top_strand, semi_g1[1].bot_strand
        d0_t, d0_b = disp_g1[0].top_strand, disp_g1[0].bot_strand
        d1_t, d1_b = disp_g1[1].top_strand, disp_g1[1].bot_strand
        self.play(
            gen_t.animate.set_value(2.0),
            s0_p.animate.move_to([-4.9, ys4[0] + 0.14, 0]),
            s0_c.animate.move_to([-4.9, ys4[1] - 0.14, 0]),
            s1_p.animate.move_to([-4.9, ys4[2] + 0.14, 0]),
            s1_c.animate.move_to([-4.9, ys4[3] - 0.14, 0]),
            d0_t.animate.move_to([4.9, ys4[0] + 0.14, 0]),
            d0_b.animate.move_to([4.9, ys4[1] - 0.14, 0]),
            d1_t.animate.move_to([4.9, ys4[2] + 0.14, 0]),
            d1_b.animate.move_to([4.9, ys4[3] - 0.14, 0]),
            run_time=3.3,
        )

        # "Semiconservative copying keeps each purple strand in one hybrid."
        self.at("Semiconservative copying")
        hyb_new_0 = make_strand_bar([-4.9, ys4[0] - 0.14, 0], width=2.3, height=0.14, color=CYAN)
        hyb_new_1 = make_strand_bar([-4.9, ys4[2] - 0.14, 0], width=2.3, height=0.14, color=CYAN)
        hyb_plates = VGroup(
            RoundedRectangle(corner_radius=0.08, width=2.55, height=0.58, stroke_color=GOLD, stroke_width=2.5,
                             fill_color=GOLD, fill_opacity=0.18).move_to([-4.9, ys4[0], 0]),
            RoundedRectangle(corner_radius=0.08, width=2.55, height=0.58, stroke_color=GOLD, stroke_width=2.5,
                             fill_color=GOLD, fill_opacity=0.18).move_to([-4.9, ys4[2], 0]),
        )
        self.play(GrowFromEdge(hyb_new_0, LEFT), GrowFromEdge(hyb_new_1, LEFT), FadeIn(hyb_plates), run_time=2.6)
        self.play(hyb_plates.animate.set_fill(opacity=0.06), run_time=1.0)

        # "The other daughters are fully cyan."
        self.at("other daughters are")
        lgt_new_0 = make_strand_bar([-4.9, ys4[1] + 0.14, 0], width=2.3, height=0.14, color=CYAN)
        lgt_new_1 = make_strand_bar([-4.9, ys4[3] + 0.14, 0], width=2.3, height=0.14, color=CYAN)
        lgt_plates = VGroup(
            RoundedRectangle(corner_radius=0.08, width=2.55, height=0.58, stroke_color=CYAN, stroke_width=2.5,
                             fill_color=CYAN, fill_opacity=0.18).move_to([-4.9, ys4[1], 0]),
            RoundedRectangle(corner_radius=0.08, width=2.55, height=0.58, stroke_color=CYAN, stroke_width=2.5,
                             fill_color=CYAN, fill_opacity=0.18).move_to([-4.9, ys4[3], 0]),
        )
        self.play(GrowFromEdge(lgt_new_0, LEFT), GrowFromEdge(lgt_new_1, LEFT), FadeIn(lgt_plates), run_time=2.3)

        # "Its tube gains separate hybrid and light bands."
        self.at("tube gains separate")
        hyb_copies = VGroup(
            make_duplex([-4.9, ys4[0], 0], width=1.4, gap=0.10, top_color=PURPLE, bot_color=CYAN, strand_h=0.09),
            make_duplex([-4.9, ys4[2], 0], width=1.4, gap=0.10, top_color=PURPLE, bot_color=CYAN, strand_h=0.09),
        )
        lgt_copies = VGroup(
            make_duplex([-4.9, ys4[1], 0], width=1.4, gap=0.10, top_color=CYAN, bot_color=CYAN, strand_h=0.09),
            make_duplex([-4.9, ys4[3], 0], width=1.4, gap=0.10, top_color=CYAN, bot_color=CYAN, strand_h=0.09),
        )
        b_semi_hyb = make_band(t_semi, 0.5, color=GOLD, thickness=0.22)
        b_semi_lgt = make_band(t_semi, 0.0, color=CYAN, thickness=0.22)
        self.play(
            FadeOut(hyb_plates, run_time=0.35),
            FadeOut(lgt_plates, run_time=0.35),
            hyb_copies[0].animate.move_to([t_semi.cx, t_semi.y_hybrid + 0.05, 0]),
            hyb_copies[1].animate.move_to([t_semi.cx, t_semi.y_hybrid - 0.05, 0]),
            lgt_copies[0].animate.move_to([t_semi.cx, t_semi.y_light + 0.05, 0]),
            lgt_copies[1].animate.move_to([t_semi.cx, t_semi.y_light - 0.05, 0]),
            run_time=2.1,
        )
        self.play(
            FadeOut(hyb_copies, run_time=0.35),
            FadeOut(lgt_copies, run_time=0.35),
            ReplacementTransform(b_semi_g1, b_semi_hyb),
            FadeIn(b_semi_lgt),
            run_time=1.0,
        )

        # "Uniform dispersive copying halves the old fraction inside every molecule again."
        self.at("Uniform dispersive")
        mol_frac = ValueTracker(0.5)
        disp_4 = always_redraw(lambda: VGroup(*[
            make_duplex([4.9, yy, 0], width=2.3, gap=0.16, strand_h=0.14,
                        segments=4, old_frac=mol_frac.get_value())
            for yy in ys4
        ]))
        self.play(FadeOut(disp_g1, run_time=0.5), FadeIn(disp_4, run_time=0.9))

        self.at("halves the old")
        self.play(mol_frac.animate.set_value(0.25), run_time=4.1, rate_func=smooth)

        # "Its single band shifts toward light."
        self.at("single band shifts")
        self.play(disp_frac.animate.set_value(0.25), run_time=1.8, rate_func=smooth)
        frac_lbl = T("1/4 old", size=24, color=GOLD).move_to(
            [t_disp.cx, density_y(0.25, t_disp.y_light, t_disp.y_heavy) + 0.34, 0]
        )
        self.play(FadeIn(frac_lbl), run_time=0.6)
        self.finish()


# ==============================================================================
# S09: OBSERVATION (28.475 s)
# ==============================================================================
class S09Observation(SpokenScene):
    def construct(self):
        t_semi, t_disp, center_labels, h_semi, h_disp = build_two_lane_tubes()
        stag = scope_tag("schematic", size=24, color=TEXT)
        ys4 = (1.75, 0.55, -0.65, -1.85)

        semi_4 = VGroup(
            make_duplex([-4.9, ys4[0], 0], width=2.3, gap=0.16, top_color=PURPLE, bot_color=CYAN, strand_h=0.14),
            make_duplex([-4.9, ys4[1], 0], width=2.3, gap=0.16, top_color=CYAN, bot_color=CYAN, strand_h=0.14),
            make_duplex([-4.9, ys4[2], 0], width=2.3, gap=0.16, top_color=PURPLE, bot_color=CYAN, strand_h=0.14),
            make_duplex([-4.9, ys4[3], 0], width=2.3, gap=0.16, top_color=CYAN, bot_color=CYAN, strand_h=0.14),
        )
        disp_4 = VGroup(*[
            make_duplex([4.9, yy, 0], width=2.3, gap=0.16, strand_h=0.14, segments=4, old_frac=0.25)
            for yy in ys4
        ])
        b_semi_hyb = make_band(t_semi, 0.5, color=GOLD, thickness=0.22)
        b_semi_lgt = make_band(t_semi, 0.0, color=CYAN, thickness=0.22)
        b_disp_qtr = make_band(t_disp, 0.25, color=GOLD, thickness=0.24)
        gen_lbl = T("generation 2", size=28, color=GOLD).move_to([0.0, 3.10, 0])

        self.add(t_semi, t_disp, center_labels, h_semi, h_disp, semi_4, disp_4,
                 b_semi_hyb, b_semi_lgt, b_disp_qtr, gen_lbl, stag)

        # "After two generations, the extracted DNA formed hybrid and light bands in equal amounts."
        self.at("the extracted DNA")
        obs_tube = make_tube(center=[t_semi.cx, -0.15, 0], width=2.16, height=5.15,
                             outline_color=GOLD, show_guides=False, label_side=None, show_gradient=False)
        obs_b1 = SurroundingRectangle(b_semi_hyb, color=GOLD, buff=0.06, stroke_width=3.5, corner_radius=0.07)
        obs_b2 = SurroundingRectangle(b_semi_lgt, color=GOLD, buff=0.06, stroke_width=3.5, corner_radius=0.07)
        obs_tag = T("observed", size=28, color=GOLD).move_to([t_semi.cx, t_semi.bot_y - 0.35, 0])
        self.play(Create(obs_tube), FadeIn(obs_tag), run_time=2.0)
        self.play(Create(obs_b1), Create(obs_b2), run_time=2.2)

        # "That matches the semiconservative distribution, not one uniformly mixed band."
        self.at("matches the")
        match_lbl = T("equal hybrid + light", size=26, color=GOLD).move_to([t_semi.cx, -3.10, 0])
        hyb_plates = VGroup(
            SurroundingRectangle(semi_4[0], color=GOLD, buff=0.07, stroke_width=2.8, fill_color=GOLD, fill_opacity=0.20),
            SurroundingRectangle(semi_4[2], color=GOLD, buff=0.07, stroke_width=2.8, fill_color=GOLD, fill_opacity=0.20),
        )
        lgt_plates = VGroup(
            SurroundingRectangle(semi_4[1], color=CYAN, buff=0.07, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.20),
            SurroundingRectangle(semi_4[3], color=CYAN, buff=0.07, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.20),
        )
        hyb_links = VGroup(
            Line([-3.70, ys4[0], 0], [t_semi.cx - t_semi.tube_w / 2.0 - 0.04, t_semi.y_hybrid, 0],
                 color=GOLD, stroke_width=3.8),
            Line([-3.70, ys4[2], 0], [t_semi.cx - t_semi.tube_w / 2.0 - 0.04, t_semi.y_hybrid, 0],
                 color=GOLD, stroke_width=3.8),
        )
        lgt_links = VGroup(
            Line([-3.70, ys4[1], 0], [t_semi.cx - t_semi.tube_w / 2.0 - 0.04, t_semi.y_light, 0],
                 color=CYAN, stroke_width=3.8),
            Line([-3.70, ys4[3], 0], [t_semi.cx - t_semi.tube_w / 2.0 - 0.04, t_semi.y_light, 0],
                 color=CYAN, stroke_width=3.8),
        )
        self.play(FadeOut(obs_tag, run_time=0.25), FadeIn(match_lbl, run_time=0.35), run_time=0.35)
        self.play(FadeIn(hyb_plates), Create(hyb_links), run_time=2.1)
        self.play(FadeIn(lgt_plates), Create(lgt_links), run_time=2.1)

        not_lbl = T("not one band", size=26, color=RED).move_to([t_disp.cx, -3.10, 0])
        q_y = density_y(0.25, t_disp.y_light, t_disp.y_heavy)
        q_box = SurroundingRectangle(b_disp_qtr, color=RED, buff=0.09, stroke_width=3.2,
                                     fill_color=RED, fill_opacity=0.24, corner_radius=0.07)
        miss_lines = VGroup(
            DashedLine([t_disp.cx + t_disp.tube_w / 2.0 + 0.08, q_y, 0],
                       [t_disp.cx + t_disp.tube_w / 2.0 + 0.55, t_disp.y_light, 0],
                       color=RED, stroke_width=3.6, dash_length=0.10),
            DashedLine([t_disp.cx + t_disp.tube_w / 2.0 + 0.08, q_y, 0],
                       [t_disp.cx + t_disp.tube_w / 2.0 + 0.55, t_disp.y_hybrid, 0],
                       color=RED, stroke_width=3.6, dash_length=0.10),
        )
        self.play(FadeIn(not_lbl), run_time=0.35)
        self.play(FadeIn(q_box), Create(miss_lines), run_time=2.5)

        # "Hybrid and light bands after two generations rule out uniform dispersive copying."
        self.at("rule out uniform")
        red_frame = make_tube_red_frame(t_disp)
        cross_x = VGroup(
            Line([t_disp.cx - 0.72, q_y - 0.22, 0], [t_disp.cx + 0.72, q_y + 0.22, 0], color=RED, stroke_width=4.0),
            Line([t_disp.cx - 0.72, q_y + 0.22, 0], [t_disp.cx + 0.72, q_y - 0.22, 0], color=RED, stroke_width=4.0),
        )
        self.play(
            Create(red_frame),
            Create(cross_x),
            FadeOut(q_box, run_time=0.4),
            h_disp.animate.set_color(RED),
            t_disp.wall.animate.set_stroke(RED, opacity=0.75),
            FadeOut(miss_lines, run_time=0.5),
            run_time=2.4,
        )

        # "The old material never disappears. It only spreads among more molecules, and where it sits is decisive."
        self.at("old material never")
        p_left = VGroup(semi_4[0].top_strand, semi_4[2].top_strand)
        hl_left = VGroup(*[
            SurroundingRectangle(m, color=GOLD, buff=0.07, stroke_width=3.0, fill_color=GOLD, fill_opacity=0.22)
            for m in p_left
        ])
        cons_lbl = T("old DNA kept, sorted differently", size=28, color=PURPLE).move_to([0.0, -3.10, 0])
        self.play(
            FadeOut(match_lbl, run_time=0.25), FadeOut(not_lbl, run_time=0.25),
            FadeOut(hyb_plates, run_time=0.35), FadeOut(lgt_plates, run_time=0.35),
        )
        self.play(FadeIn(cons_lbl, run_time=0.35))
        self.play(Create(hl_left), run_time=2.0)

        self.at("spreads among more")
        for d in disp_4:
            box = SurroundingRectangle(d, color=PURPLE, buff=0.07, stroke_width=2.8,
                                       fill_color=PURPLE, fill_opacity=0.16)
            self.play(Create(box), run_time=0.95)
        self.finish()


# ==============================================================================
# S10: SCOPE (23.05 s)
# ==============================================================================
class S10Scope(SpokenScene):
    def construct(self):
        tube = make_tube(center=[2.8, 0.0, 0], width=3.0, height=5.7,
                         outline_color=TEXT, show_guides=True, label_side=LEFT, label_buff=0.26,
                         show_gradient=True, label_size=28)
        hybrid_band = make_band(tube, 0.5, color=GOLD, thickness=0.28)
        duplex = make_duplex([-3.1, 0.45, 0], width=4.6, gap=0.30, top_color=PURPLE, bot_color=CYAN, strand_h=0.20)
        scope_hdr = T("tracked: inherited DNA", size=30, color=TEXT).move_to([-3.1, 2.75, 0])
        stag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tube, hybrid_band, duplex, scope_hdr, stag)

        # "The experiment tracked inherited material, not enzymes."
        self.at("not enzymes")
        self.play(duplex.animate.shift(UP * 0.12), run_time=0.9)
        self.play(duplex.animate.shift(DOWN * 0.12), run_time=0.9)

        # "Heating the hybrid DNA separated heavy and light subunits, consistent with old and new strands."
        self.at("Heating the hybrid")
        heat_waves = VGroup(*[
            FunctionGraph(lambda x, k=k: 0.14 * np.sin(5.5 * x), x_range=[-2.0, 2.0], color=GOLD, stroke_width=4.0)
            .move_to([-3.1, 0.0 + k * 0.45, 0])
            for k in (-1, 0, 1)
        ])
        heat_lbl = T("heat", size=30, color=GOLD).move_to([-3.1, -1.2, 0])
        self.play(Create(heat_waves), FadeIn(heat_lbl), run_time=1.0)

        self.at("separated heavy and")
        b_heavy = make_band(tube, 1.0, color=PURPLE, thickness=0.26)
        b_light = make_band(tube, 0.0, color=CYAN, thickness=0.26)
        self.play(
            FadeOut(heat_waves, run_time=0.4),
            FadeOut(heat_lbl, run_time=0.4),
            duplex.top_strand.animate.move_to([-3.1, 1.50, 0]),
            duplex.bot_strand.animate.move_to([-3.1, -0.55, 0]),
            ReplacementTransform(hybrid_band, VGroup(b_heavy, b_light)),
            run_time=2.2,
        )

        self.at("consistent with old")
        sub_grp = VGroup(duplex.top_strand, duplex.bot_strand)
        cons_brace = Brace(sub_grp, DOWN, color=GOLD)
        cons_lbl = T("consistent with strands", size=28, color=GOLD).next_to(cons_brace, DOWN, buff=0.20)
        hl_top = SurroundingRectangle(duplex.top_strand, color=PURPLE, buff=0.08, stroke_width=3.0,
                                      fill_color=PURPLE, fill_opacity=0.14)
        hl_bot = SurroundingRectangle(duplex.bot_strand, color=CYAN, buff=0.08, stroke_width=3.0,
                                      fill_color=CYAN, fill_opacity=0.14)
        self.play(Create(cons_brace), FadeIn(cons_lbl), Create(hl_top), Create(hl_bot), run_time=2.8)

        # "Meselson and Stahl still stated their limit carefully."
        self.at("stated their limit")
        q_tag = boxed_label("subunit identity?", color=GOLD, size=28, pad=0.22).move_to([-3.1, 2.65, 0])
        self.play(FadeOut(scope_hdr, run_time=0.35), FadeOut(hl_top, run_time=0.35), FadeOut(hl_bot, run_time=0.35))
        self.play(FadeIn(q_tag, run_time=0.8))

        # "Their bands did not alone show that each conserved subunit was one polynucleotide chain."
        self.at("Their bands did")
        scan_box = SurroundingRectangle(duplex.top_strand, color=GOLD, buff=0.10, stroke_width=3.5)
        chain_lbl = T("one polynucleotide chain?", size=24, color=GOLD).move_to([-3.1, 0.72, 0])
        marker = RoundedRectangle(corner_radius=0.08, width=2.1, height=0.62, stroke_color=GOLD,
                                  stroke_width=3.2, fill_color=GOLD, fill_opacity=0.28).move_to([-4.35, 1.50, 0])
        self.play(FadeIn(chain_lbl), run_time=0.35)
        self.play(Create(scan_box), FadeIn(marker), run_time=1.0)
        self.play(marker.animate.move_to([-1.85, 1.50, 0]), run_time=3.5, rate_func=smooth)
        self.play(FadeOut(marker, run_time=0.5))
        self.finish()


# ==============================================================================
# S11: THE RULE (16.3 s)
# ==============================================================================
class S11Rule(SpokenScene):
    def construct(self):
        tube = make_tube(center=[3.9, 0.0, 0], width=2.6, height=5.4,
                         outline_color=TEXT, show_guides=True, label_side=LEFT, label_buff=0.26,
                         show_gradient=True, label_size=26)
        b_hyb = make_band(tube, 0.5, color=GOLD, thickness=0.26)
        stag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tube, stag)

        # "Each daughter molecule keeps one old strand and builds one new strand."
        parent_p = make_duplex([-2.2, 1.35, 0], width=6.6, gap=0.32, top_color=PURPLE, bot_color=PURPLE, strand_h=0.25)
        self.play(FadeIn(parent_p, shift=RIGHT * 0.8), run_time=1.4)
        old_strand = parent_p.top_strand
        other_old = parent_p.bot_strand
        self.play(
            old_strand.animate.move_to([-2.2, 1.10, 0]),
            FadeOut(other_old, shift=DOWN * 0.9),
            run_time=1.3,
        )

        self.at("builds one new")
        n_blocks = 12
        bw = 6.6 / n_blocks
        blocks = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=bw - 0.04, height=0.26,
                             stroke_width=0, fill_color=CYAN, fill_opacity=1.0)
            .move_to([-2.2 - 3.3 + (i + 0.5) * bw, 0.55, 0])
            for i in range(n_blocks)
        ])
        for blk in blocks:
            self.play(FadeIn(blk, shift=UP * 0.12), run_time=0.18)
        joined_cyan = make_strand_bar([-2.2, 0.55, 0], width=6.6, height=0.26, color=CYAN)
        self.play(ReplacementTransform(blocks, joined_cyan), run_time=0.5)

        # "That logic predicts later band patterns and gives replication its name, semiconservative."
        self.at("predicts later band")
        pair = VGroup(old_strand, joined_cyan)
        b_ring = SurroundingRectangle(b_hyb, color=GOLD, buff=0.07, stroke_width=3.2, corner_radius=0.07)
        self.play(
            pair.animate.move_to([-2.2, tube.y_hybrid, 0]),
            FadeIn(b_hyb),
            Create(b_ring),
            run_time=1.8,
        )

        self.at("gives replication its")
        name_lbl = T("semiconservative", size=42, color=GOLD).next_to(pair, DOWN, buff=0.65)
        pill = SurroundingRectangle(name_lbl, corner_radius=0.18, color=GOLD, stroke_width=3.2,
                                    fill_color=GOLD, fill_opacity=0.10, buff=0.22)
        self.play(FadeIn(name_lbl, shift=UP * 0.15), run_time=1.0)
        self.play(Create(pill), run_time=2.2)

        # "Keep the rule for chromosome replication in this lesson."
        self.at("Keep the rule")
        rule_line = Line(pill.get_left(), pill.get_right(), color=GOLD, stroke_width=4.5)
        rule_line.next_to(pill, DOWN, buff=0.20)
        pair_box = SurroundingRectangle(pair, color=TEXT, buff=0.14, stroke_width=2.6, corner_radius=0.10)
        self.play(Create(rule_line), Create(pair_box), run_time=2.2)
        self.finish()


# ==============================================================================
# S12: END CARD (3.5 s, silent)
# ==============================================================================
class S12End(EndCard):
    LINE = "Each daughter molecule keeps one old strand and builds one new strand."
