# =============================================================================
# FILM PLAN: "Two Ways to Start, Several Ways to Stop" (transcription__chapter-2)
#
# COLOUR MAP (one colour per concept, preserved from Film 1 across all scenes):
#   BLUE   (#58C4DD) : Template DNA strand (read 3' -> 5')
#   GOLD   (#D4A843) : Coding DNA strand (5' -> 3', matches RNA with T for U)
#   GREEN  (#83C167) : Growing RNA transcript (synthesized 5' -> 3')
#   TEAL   (#3FB8C0) : Promoter elements (-35, -10, core promoter, +1 start) & poly(A) signal
#   TEXT   (#E8EAF0) : RNA Polymerase (bacterial core, nuclear Pol I, Pol II, Pol III)
#   VIOLET (#B888E8) : Bacterial regulatory factors (sigma specificity key, Rho termination ring)
#   YELLOW (#F5D547) : Nuclear general transcription factors (recognize, position, open platform)
#   ORANGE (#FF8C42) : Nuclear following enzyme (5'->3' exonuclease pursuing Pol II)
#   RED    (#FC6255) : Termination cleavage / complex destabilization / release gate
#
# CARRIED WORLD PICTURE:
#   A horizontal double-stranded DNA transcription track (BLUE template 3'->5' paired with
#   GOLD coding strand 5'->3', TEAL notched promoter region upstream of the +1 start marker,
#   WHITE C-cleft RNA polymerase opening a local transcription bubble, and GREEN nascent RNA
#   extruding 5'->3' from the exit channel). Splits into parallel E. coli and nucleus lanes
#   when comparing systems, zooms into one lane for mechanism, and merges for shared elongation.
#
# WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
#   s01_hook             : Polymerase Position Tracker x_pol(t) advances along the single duplex
#                          opening a Gaussian bubble and extending RNA, then splits y_sep(t) into
#                          E. coli and nucleus lanes with sinusoidal pulsing docking outlines and
#                          cycling Pol I/II/III silhouettes at the nuclear promoter.
#   s03_shared_job       : Synchronized stage tracker prog(t) drives promoter clamping, polymerase
#                          docking, bubble opening b(t), downstream elongation x(t) with growing
#                          green RNA length L(t), and complex dissociation r(t) across both lanes.
#   s04_bacteria         : Bacterial core position x_core(t) transcribes then slides past three
#                          teal promoters without locking; violet sigma key docks y_sig(t) into
#                          core's socket and the holoenzyme locks into the -35/-10 notches over +1.
#   s05_predict          : Sigma detaches upward y_det(t) leaving core drifting past the promoter
#                          while two choice cards (RNA-joining vs target-start) pulse sinusoidally.
#   s07_bacterial_reveal : Target-start card highlights; sigma redocks onto core to clamp closed
#                          DNA, bubble height b(t) opens around +1, three abortive short RNA tiles
#                          eject along parabolic trajectories, and holoenzyme escapes downstream.
#   s08_nuclear_division : Single nuclear polymerase divides into Pol I, Pol II, and Pol III lanes;
#                          three independent trackers p1(t), p2(t), p3(t) drive polymerase travel
#                          and green RNA ribbon flow into their three respective product bins.
#   s09_pol_two          : Pol II lane zooms to full frame; general factor blocks ('recognize',
#                          'position', 'open') assemble stepwise on the teal core promoter, Pol II
#                          settles in as template DNA bends into its cleft, and bound/free factor
#                          copies continuously exchange positions via sinusoidal swap trajectories.
#   s10_escape           : Shared trackers open both lanes' bubbles, grow green RNAs, drive
#                          promoter escape x_esc(t), and merge both lanes vertically y_merge(t)
#                          into one large elongation complex adding nucleotides 5' -> 3'.
#   s11_bacterial_stop   : Elongation track splits into two branches: top branch folds emerging
#                          RNA into a stem-loop hairpin beside a U-rich tract to lift polymerase
#                          off DNA; bottom branch translocates a violet Rho ring x_rho(t) along
#                          RNA until it collides with and releases polymerase.
#   s12_pol_two_stop     : Pol II crosses a teal poly(A) signal, a red cleavage cut severs the
#                          pre-mRNA, and an orange following enzyme chases along the attached RNA
#                          at constant speed while Pol II decelerates (v_pol(t) falls from 1.0 to
#                          0.15 on a live speed gauge) until pursuit catches and releases Pol II.
#   s13_close            : Full-width journey track with Start Gate (+1) and Release Gate;
#                          initiation teams place polymerase at the start, termination routes arm
#                          the release gate, and journey tracker x_j(t) drives directional synthesis
#                          from start gate to release gate.
# =============================================================================

from bp_parts import *

VIOLET = "#B888E8"
ORANGE = "#FF8C42"
WHITE_POL = "#F2F4F8"
DARK_PANEL = "#1C2436"


def _lane_backdrop(x0, x1, y0, y1, color=BLUE, opacity=0.22):
    """Stroke-free background band at z_index -5 so it adds visual body without crossing labels."""
    c = 0.20
    pts = [
        [x0 + c, y0, 0], [x1 - c, y0, 0], [x1, y0 + c, 0],
        [x1, y1 - c, 0], [x1 - c, y1, 0], [x0 + c, y1, 0],
        [x0, y1 - c, 0], [x0, y0 + c, 0],
    ]
    p = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)
    p.set_z_index(-5)
    return p


def _duplex_track(x0, x1, yc, s=1.0, prom_x=(-3.8, -1.8), start_x=-1.4,
                  bubble_x=None, bubble_w=1.5, bubble_open=0.0, show_notches=True):
    """Build a computed DNA duplex at y = yc with optional promoter block and open bubble."""
    g = VGroup()
    dy = 0.19 * s
    b_amp = 0.22 * s * float(np.clip(bubble_open, 0.0, 1.0))

    xs = np.linspace(x0, x1, 140)
    top_pts, bot_pts = [], []
    for x in xs:
        sep = 0.0
        if bubble_x is not None and b_amp > 1e-4:
            u = (x - bubble_x) / (0.55 * bubble_w)
            if abs(u) < 2.5:
                sep = b_amp * np.exp(-1.4 * u * u)
        top_pts.append([x, yc + dy + sep, 0.0])
        bot_pts.append([x, yc - dy - sep, 0.0])

    poly_pts = top_pts + bot_pts[::-1]
    interior = Polygon(*poly_pts, stroke_width=0, fill_color=BLUE, fill_opacity=0.22)
    g.add(interior)

    rungs = VGroup()
    n_rungs = int((x1 - x0) / (0.34 * max(s, 0.65)))
    for x in np.linspace(x0 + 0.25, x1 - 0.25, n_rungs):
        in_prom = prom_x is not None and (prom_x[0] <= x <= prom_x[1])
        sep = 0.0
        if bubble_x is not None and b_amp > 1e-4:
            u = (x - bubble_x) / (0.55 * bubble_w)
            if abs(u) < 1.15:
                continue
            if abs(u) < 2.5:
                sep = b_amp * np.exp(-1.4 * u * u)
        y_t = yc + dy + sep
        y_b = yc - dy - sep
        col = TEAL if in_prom else BLUE
        rungs.add(Line([x, y_b + 0.02, 0], [x, y_t - 0.02, 0],
                       stroke_color=col, stroke_width=2.8 * s, stroke_opacity=0.65))
    g.add(rungs)

    if prom_x is not None:
        px0, px1 = prom_x
        ph = 0.28 * s
        if show_notches:
            n1a = px0 + 0.18 * (px1 - px0)
            n1b = px0 + 0.38 * (px1 - px0)
            n2a = px0 + 0.62 * (px1 - px0)
            n2b = px0 + 0.82 * (px1 - px0)
            nd = 0.10 * s
            p_pts = [
                [px0, yc - ph, 0], [px1, yc - ph, 0],
                [px1, yc + ph, 0],
                [n2b, yc + ph, 0], [n2b, yc + ph - nd, 0], [n2a, yc + ph - nd, 0], [n2a, yc + ph, 0],
                [n1b, yc + ph, 0], [n1b, yc + ph - nd, 0], [n1a, yc + ph - nd, 0], [n1a, yc + ph, 0],
                [px0, yc + ph, 0],
            ]
        else:
            p_pts = [[px0, yc - ph, 0], [px1, yc - ph, 0], [px1, yc + ph, 0], [px0, yc + ph, 0]]
        prom_poly = Polygon(*p_pts, stroke_color=TEAL, stroke_width=3.5,
                            fill_color=TEAL, fill_opacity=0.38)
        g.add(prom_poly)

    coding = VMobject(stroke_color=GOLD, stroke_width=6.0 * max(s, 0.75), fill_opacity=0)
    coding.set_points_as_corners(top_pts)
    template = VMobject(stroke_color=BLUE, stroke_width=6.0 * max(s, 0.75), fill_opacity=0)
    template.set_points_as_corners(bot_pts)
    g.add(coding, template)

    if start_x is not None:
        st_line = Line([start_x, yc - 0.32 * s, 0], [start_x, yc + 0.32 * s, 0],
                       stroke_color=TEAL, stroke_width=4.5)
        st_dot = Dot([start_x, yc, 0], radius=0.08 * s, color=TEAL)
        g.add(st_line, st_dot)

    return g


def _pol_body(x, yc, s=1.0, color=WHITE_POL, fill_op=0.36, socket=False):
    """Draw a schematic RNA polymerase clamp with an active-site cleft (as a Polygon)."""
    w = 1.60 * s
    h = 0.96 * s
    hw, hh = w / 2, h / 2
    if socket:
        pts = [
            [x - hw, yc - hh, 0],
            [x + hw * 0.85, yc - hh, 0],
            [x + hw, yc - hh * 0.25, 0],
            [x + hw * 0.35, yc - hh * 0.12, 0],
            [x + hw * 0.35, yc + hh * 0.18, 0],
            [x + hw, yc + hh * 0.32, 0],
            [x + hw * 0.85, yc + hh, 0],
            [x + hw * 0.25, yc + hh, 0],
            [x + hw * 0.15, yc + hh * 0.62, 0],
            [x - hw * 0.35, yc + hh * 0.62, 0],
            [x - hw * 0.45, yc + hh, 0],
            [x - hw, yc + hh, 0],
        ]
    else:
        pts = [
            [x - hw, yc - hh, 0],
            [x + hw * 0.85, yc - hh, 0],
            [x + hw, yc - hh * 0.25, 0],
            [x + hw * 0.30, yc - hh * 0.10, 0],
            [x + hw * 0.30, yc + hh * 0.18, 0],
            [x + hw, yc + hh * 0.32, 0],
            [x + hw * 0.85, yc + hh, 0],
            [x - hw, yc + hh, 0],
        ]
    body = Polygon(*pts, stroke_color=color, stroke_width=3.8, fill_color=color, fill_opacity=fill_op)
    active = Dot([x - 0.05 * s, yc - 0.10 * s, 0], radius=0.08 * s, color=TEXT)
    return VGroup(body, active)


def _sigma_key(x, yc, s=1.0):
    """Draw a violet sigma factor with a core-docking wedge and two promoter-reading teeth."""
    w = 1.28 * s
    h = 0.44 * s
    hw = w / 2
    pts = [
        [x - hw, yc + h, 0],
        [x + hw, yc + h, 0],
        [x + hw, yc, 0],
        [x + hw * 0.55, yc, 0],
        [x + hw * 0.55, yc - 0.26 * s, 0],
        [x + hw * 0.22, yc - 0.26 * s, 0],
        [x + hw * 0.22, yc, 0],
        [x - hw * 0.22, yc, 0],
        [x - hw * 0.22, yc - 0.26 * s, 0],
        [x - hw * 0.55, yc - 0.26 * s, 0],
        [x - hw * 0.55, yc, 0],
        [x - hw, yc, 0],
    ]
    return Polygon(*pts, stroke_color=VIOLET, stroke_width=3.5, fill_color=VIOLET, fill_opacity=0.45)


def _rna_ribbon(x_pol, yc, length, s=1.0, arch_up=True):
    """Draw a nascent GREEN RNA strand pairing inside the bubble and emerging 5'->3'."""
    g = VGroup()
    if length <= 0.02:
        return g
    n_pts = 36
    ts = np.linspace(0.0, 1.0, n_pts)
    pts = []
    sign = 1.0 if arch_up else -1.0
    for u in ts:
        dx = -u * length
        dy = -0.12 * s + sign * (0.50 * s * (1.0 - np.exp(-2.6 * u)) + 0.05 * s * np.sin(5.0 * u))
        pts.append([x_pol + dx, yc + dy, 0.0])
    rib = VMobject(stroke_color=GREEN, stroke_width=6.8 * max(s, 0.75), fill_opacity=0)
    rib.set_points_as_corners(pts)
    tip3 = Dot(pts[0], radius=0.07 * s, color=GREEN)
    tip5 = Dot(pts[-1], radius=0.06 * s, color=GREEN)
    g.add(rib, tip3, tip5)
    return g


# =============================================================================
# SCENE 01: s01_hook
# =============================================================================
class S01Hook(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        pol_x = ValueTracker(-1.2)
        split_t = ValueTracker(0.0)
        pulse_t = ValueTracker(0.0)
        start_pin = ValueTracker(0.0)
        nuc_choice = ValueTracker(0.0)

        legend = VGroup(
            boxed_label("template DNA 3'→5'", BLUE, size=24, pad=0.14, fill_opacity=0.22),
            boxed_label("coding DNA 5'→3'", GOLD, size=24, pad=0.14, fill_opacity=0.22),
            boxed_label("promoter", TEAL, size=24, pad=0.14, fill_opacity=0.22),
            boxed_label("polymerase", TEXT, size=24, pad=0.14, fill_opacity=0.22),
            boxed_label("RNA 5'→3'", GREEN, size=24, pad=0.14, fill_opacity=0.22),
        ).arrange(RIGHT, buff=0.22).move_to([0.0, 3.25, 0])
        self.add(legend)

        def build_world():
            grp = VGroup()
            sp = split_t.get_value()
            px = pol_x.get_value()
            pt = pulse_t.get_value()
            pin = start_pin.get_value()
            nc = nuc_choice.get_value()

            if sp < 0.02:
                yc = 0.0
                bg = _lane_backdrop(-5.9, 5.9, -1.55, 1.65, color=TEAL, opacity=0.18)
                tr = _duplex_track(-5.4, 5.4, yc, s=1.10, prom_x=(-4.2, -1.8), start_x=-1.4,
                                   bubble_x=px, bubble_w=1.65, bubble_open=1.0)
                rna_len = max(0.15, (px - (-1.4)) * 0.78)
                rna = _rna_ribbon(px, yc, rna_len, s=1.10, arch_up=True)
                pol = _pol_body(px, yc, s=1.05, color=WHITE_POL, fill_op=0.38)
                grp.add(bg, tr, rna, pol)
            else:
                y_top = 1.25 * sp
                y_bot = -1.65 * sp
                s_lane = 1.05 * (1.0 - 0.22 * sp)

                bg_top = _lane_backdrop(-5.9, 5.9, y_top - 0.65, y_top + 0.65, color=VIOLET, opacity=0.18)
                bg_bot = _lane_backdrop(-5.9, 5.9, y_bot - 0.65, y_bot + 0.65, color=YELLOW, opacity=0.18)

                tr_top = _duplex_track(-5.2, 5.2, y_top, s=s_lane, prom_x=(-3.2, -1.3), start_x=-1.0,
                                       bubble_x=None, bubble_open=0.0, show_notches=True)
                tr_bot = _duplex_track(-5.2, 5.2, y_bot, s=s_lane, prom_x=(-3.2, -1.3), start_x=-1.0,
                                       bubble_x=None, bubble_open=0.0, show_notches=False)
                grp.add(bg_top, bg_bot, tr_top, tr_bot)

                if pt > 0.01:
                    sw_pulse = 3.0 + 2.0 * np.sin(4.5 * pt)
                    op_pulse = 0.20 + 0.12 * np.sin(4.5 * pt)
                    dock_top = DashedVMobject(
                        Polygon(
                            [-3.25, y_top - 0.42, 0], [-0.45, y_top - 0.42, 0],
                            [-0.45, y_top + 0.45, 0], [-3.25, y_top + 0.45, 0],
                            stroke_color=VIOLET, stroke_width=sw_pulse
                        ),
                        num_dashes=24
                    )
                    fill_top = Polygon(
                        [-3.25, y_top - 0.42, 0], [-0.45, y_top - 0.42, 0],
                        [-0.45, y_top + 0.45, 0], [-3.25, y_top + 0.45, 0],
                        stroke_width=0, fill_color=VIOLET, fill_opacity=op_pulse * 0.55
                    )
                    dock_bot = DashedVMobject(
                        Polygon(
                            [-3.35, y_bot - 0.42, 0], [-0.25, y_bot - 0.42, 0],
                            [-0.25, y_bot + 0.45, 0], [-3.35, y_bot + 0.45, 0],
                            stroke_color=YELLOW, stroke_width=sw_pulse
                        ),
                        num_dashes=24
                    )
                    fill_bot = Polygon(
                        [-3.35, y_bot - 0.42, 0], [-0.25, y_bot - 0.42, 0],
                        [-0.25, y_bot + 0.45, 0], [-3.35, y_bot + 0.45, 0],
                        stroke_width=0, fill_color=YELLOW, fill_opacity=op_pulse * 0.55
                    )
                    grp.add(fill_top, dock_top, fill_bot, dock_bot)

                if pin > 0.01:
                    sx = -1.0
                    for yy in (y_top, y_bot):
                        ring = Circle(radius=0.22 + 0.04 * np.sin(5.0 * pt), color=TEAL,
                                      stroke_width=4.0, fill_color=TEAL, fill_opacity=0.28 * pin).move_to([sx, yy, 0])
                        grp.add(ring)
                    conn = DashedLine([sx, y_bot + 0.48, 0], [sx, y_top - 0.48, 0],
                                      color=TEAL, stroke_width=3.2 * pin, dash_length=0.14)
                    grp.add(conn)

                if nc > 0.01:
                    for idx_p, dx_base in enumerate([1.4, 2.7, 4.0]):
                        cur_x = dx_base - 0.45 * nc + 0.10 * np.sin(4.0 * pt + idx_p * 1.8)
                        mini_p = _pol_body(cur_x, y_bot, s=0.48, color=WHITE_POL,
                                           fill_op=0.25 + 0.18 * (1 if idx_p == 1 else 0))
                        grp.add(mini_p)

            return grp

        world = always_redraw(build_world)
        self.add(world)

        # Beat 1 (0.0 -> 4.86s)
        self.play(pol_x.animate.set_value(3.4), run_time=4.6, rate_func=linear)

        # Beat 2 (5.06 -> 10.8s)
        self.at("why do bacteria")
        ecoli_tag = boxed_label("E. coli lane", VIOLET, size=25, pad=0.14, fill_opacity=0.24).move_to([-4.85, 2.28, 0])
        nuc_tag = boxed_label("Nucleus lane", YELLOW, size=25, pad=0.14, fill_opacity=0.24).move_to([-4.80, -0.62, 0])
        q_banner = boxed_label("Why different initiation teams for the same reaction?", GOLD, size=26,
                               pad=0.16, fill_opacity=0.22).move_to([-0.5, -3.15, 0])
        self.play(
            split_t.animate.set_value(1.0),
            pulse_t.animate.set_value(0.6),
            run_time=2.1,
            rate_func=smooth
        )
        self.play(
            pulse_t.animate.set_value(1.8),
            FadeIn(ecoli_tag),
            FadeIn(nuc_tag),
            FadeIn(q_banner),
            run_time=3.3,
            rate_func=smooth
        )

        # Beat 3 (11.04 -> 13.3s)
        self.at("keep watching the promoter")
        prom_lbl_top = T("promoter (+1)", size=24, color=TEAL).move_to([-2.18, 2.28, 0])
        prom_lbl_bot = T("promoter (+1)", size=24, color=TEAL).move_to([-2.18, -0.62, 0])
        self.play(
            pulse_t.animate.set_value(3.6),
            FadeIn(prom_lbl_top),
            FadeIn(prom_lbl_bot),
            run_time=2.1,
            rate_func=linear
        )

        # Beat 4 (13.50 -> 17.1s)
        self.at("the team assembled")
        where_lbl = boxed_label("decides where Pol begins (+1)", TEAL, size=24, pad=0.14,
                                fill_opacity=0.24).move_to([1.9, 2.28, 0])
        self.play(
            start_pin.animate.set_value(1.0),
            pulse_t.animate.set_value(6.2),
            FadeIn(where_lbl),
            run_time=3.5,
            rate_func=linear
        )

        # Beat 5 (17.38 -> 19.95s)
        self.at("in the nucleus")
        which_lbl = boxed_label("and which polymerase (I, II, III)", TEXT, size=24, pad=0.14,
                                fill_opacity=0.24).move_to([2.2, -0.62, 0])
        self.play(
            nuc_choice.animate.set_value(1.0),
            pulse_t.animate.set_value(8.5),
            FadeIn(which_lbl),
            run_time=2.4,
            rate_func=linear
        )
        self.finish()


# =============================================================================
# SCENE 02: s02_title (silent: 2.0 s)
# =============================================================================
class S02Title(TitleCard):
    LESSON = "Transcription: From DNA to RNA"
    TITLE = "Two Ways to Start, Several Ways to Stop"

    def construct(self):
        expand_t = ValueTracker(0.55)
        glow_t = ValueTracker(0.0)

        brand = T("BIOCHEMISTRYPEDIA · TRANSCRIPTION: FROM DNA TO RNA", size=24, color=TEAL, weight=BOLD)
        title = T(self.TITLE, size=48, font=TITLE_FONT, color=TEXT)
        fit(title, max_w=11.8)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4)
        header = VGroup(brand, title, rule).arrange(DOWN, buff=0.26).move_to([0.0, 2.15, 0])

        def build_lanes():
            ex = expand_t.get_value()
            gl = glow_t.get_value()
            y_top = -0.60 * (1.0 - ex) + 0.15 * ex
            y_bot = -2.25 * (1.0 - ex) + (-1.95) * ex
            sc = 0.72 * (1.0 - ex) + 0.90 * ex
            w_half = 4.6 * (1.0 - ex) + 5.5 * ex

            bg_top = _lane_backdrop(-w_half - 0.3, w_half + 0.3, y_top - 0.62 * sc, y_top + 0.62 * sc,
                                    color=VIOLET, opacity=0.18)
            bg_bot = _lane_backdrop(-w_half - 0.3, w_half + 0.3, y_bot - 0.62 * sc, y_bot + 0.62 * sc,
                                    color=YELLOW, opacity=0.18)
            tr1 = _duplex_track(-w_half, w_half, y_top, s=sc, prom_x=(-3.2, -1.2), start_x=-0.9 + 0.25 * gl)
            tr2 = _duplex_track(-w_half, w_half, y_bot, s=sc, prom_x=(-3.2, -1.2), start_x=-0.9 + 0.25 * gl)
            return VGroup(bg_top, bg_bot, tr1, tr2)

        lanes = always_redraw(build_lanes)
        self.add(lanes, header)
        self.play(expand_t.animate.set_value(0.0), run_time=0.35, rate_func=smooth)
        self.play(glow_t.animate.set_value(1.0), run_time=1.25, rate_func=linear)
        self.play(expand_t.animate.set_value(0.75), run_time=0.40, rate_func=smooth)
        self.finish()


# =============================================================================
# SCENE 03: s03_shared_job
# =============================================================================
class S03SharedJob(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        rec_t = ValueTracker(0.0)
        place_t = ValueTracker(0.0)
        open_t = ValueTracker(0.0)
        rna_t = ValueTracker(0.0)
        rel_t = ValueTracker(0.0)
        sweep_t = ValueTracker(0.0)

        b1 = boxed_label("1. recognize", TEAL, size=24, pad=0.14, fill_opacity=0.24)
        b2 = boxed_label("2. place Pol", TEXT, size=24, pad=0.14, fill_opacity=0.24)
        b3 = boxed_label("3. open DNA", BLUE, size=24, pad=0.14, fill_opacity=0.24)
        b4 = boxed_label("4. start RNA", GREEN, size=24, pad=0.14, fill_opacity=0.24)
        b5 = boxed_label("5. release", RED, size=24, pad=0.14, fill_opacity=0.24)
        job_row = VGroup(b1, b2, b3, b4, b5).arrange(RIGHT, buff=0.24).move_to([0.0, 3.22, 0])

        l_ecoli = boxed_label("E. coli", VIOLET, size=25, pad=0.14, fill_opacity=0.24).move_to([-5.15, 2.22, 0])
        l_nuc = boxed_label("Nucleus", YELLOW, size=25, pad=0.14, fill_opacity=0.24).move_to([-5.10, -0.58, 0])
        self.add(l_ecoli, l_nuc)

        def build_jobs():
            g = VGroup()
            rc = rec_t.get_value()
            pl = place_t.get_value()
            op = open_t.get_value()
            rn = rna_t.get_value()
            rl = rel_t.get_value()
            sw = sweep_t.get_value()

            pol_x = -4.2 * (1.0 - rc) + (-1.2) * rc + 4.85 * rn
            bub_open = op * (1.0 - rl)

            for idx, (yc, col_lane) in enumerate([(1.15, VIOLET), (-1.65, YELLOW)]):
                bg = _lane_backdrop(-5.9, 5.9, yc - 0.72, yc + 0.72, color=col_lane, opacity=0.18)
                tr = _duplex_track(-5.4, 5.4, yc, s=0.84, prom_x=(-3.8, -1.6), start_x=-1.2,
                                   bubble_x=pol_x, bubble_w=1.55, bubble_open=bub_open, show_notches=(idx == 0))
                g.add(bg, tr)

                rel_gate = Polygon(
                    [3.45, yc - 0.48, 0], [4.25, yc - 0.48, 0],
                    [4.25, yc + 0.48, 0], [3.45, yc + 0.48, 0],
                    stroke_color=RED, stroke_width=3.2, fill_color=RED, fill_opacity=0.20 + 0.22 * rl
                )
                g.add(rel_gate)

                if rc > 0.01:
                    y_br = yc + 0.42 - 0.08 * rc
                    br = Polygon(
                        [-3.85, y_br + 0.20, 0], [-1.55, y_br + 0.20, 0],
                        [-1.55, y_br, 0], [-3.85, y_br, 0],
                        stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.45 * rc
                    )
                    g.add(br)

                y_pol = yc + (1.0 - pl) * 0.42 + rl * 0.52
                pol = _pol_body(pol_x + rl * 0.45, y_pol, s=0.78, color=WHITE_POL, fill_op=0.38)
                g.add(pol)

                if rn > 0.01:
                    rna_len = 0.35 + 2.55 * rn
                    y_rna = yc + rl * 0.46
                    rna = _rna_ribbon(pol_x - rl * 0.25, y_rna, rna_len, s=0.80, arch_up=True)
                    g.add(rna)

                if sw > 0.01:
                    sx = -4.6 + 9.2 * sw
                    marker = Circle(radius=0.18, color=GOLD, stroke_width=4, fill_color=GOLD,
                                    fill_opacity=0.35).move_to([sx, yc, 0])
                    g.add(marker)

            return g

        world = always_redraw(build_jobs)
        self.add(world)

        self.play(rec_t.animate.set_value(0.65), run_time=4.0, rate_func=linear)

        self.at("recognize a promoter")
        self.play(FadeIn(b1), rec_t.animate.set_value(1.0), run_time=1.3, rate_func=smooth)

        self.at("place polymerase")
        self.play(FadeIn(b2), place_t.animate.set_value(1.0), run_time=1.0, rate_func=smooth)

        self.at("open dna")
        self.play(FadeIn(b3), open_t.animate.set_value(1.0), run_time=1.0, rate_func=smooth)

        self.at("start rna")
        self.play(FadeIn(b4), rna_t.animate.set_value(1.0), run_time=3.9, rate_func=linear)

        self.at("release the rna")
        self.play(FadeIn(b5), rel_t.animate.set_value(1.0), run_time=2.9, rate_func=smooth)

        self.at("the parts differ")
        summary_cap = caption("Same 5 physical jobs in both systems: recognize, place, open, start RNA, release.",
                              size=26, color=GOLD, y=-3.18)
        self.play(
            FadeIn(summary_cap),
            sweep_t.animate.set_value(1.0),
            run_time=2.8,
            rate_func=linear
        )
        self.finish()


# =============================================================================
# SCENE 04: s04_bacteria
# =============================================================================
class S04Bacteria(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        head = boxed_label("E. coli: core polymerase + sigma factor → holoenzyme", VIOLET,
                           size=28, pad=0.18, fill_opacity=0.24).move_to([0.0, 3.22, 0])
        self.add(head)

        core_x = ValueTracker(-4.2)
        core_y = ValueTracker(-0.20)
        cat_rna = ValueTracker(0.1)
        sig_dock = ValueTracker(0.0)
        lock_t = ValueTracker(0.0)

        def build_bacteria():
            cx = core_x.get_value()
            cy = core_y.get_value()
            cr = cat_rna.get_value()
            sd = sig_dock.get_value()
            lk = lock_t.get_value()

            yc = -0.55
            bg = _lane_backdrop(-6.0, 6.0, -1.25, 1.45, color=VIOLET, opacity=0.18)
            tr = _duplex_track(-5.5, 5.5, yc, s=1.12, prom_x=(1.1, 2.9), start_x=3.35,
                               bubble_x=3.35 if lk > 0.2 else None, bubble_w=1.55,
                               bubble_open=0.35 * lk, show_notches=True)
            p1_box = Polygon([-4.7, yc - 0.31, 0], [-3.5, yc - 0.31, 0],
                             [-3.5, yc + 0.31, 0], [-4.7, yc + 0.31, 0],
                             stroke_color=TEAL, stroke_width=3.2, fill_color=TEAL, fill_opacity=0.34)
            p2_box = Polygon([-1.9, yc - 0.31, 0], [-0.7, yc - 0.31, 0],
                             [-0.7, yc + 0.31, 0], [-1.9, yc + 0.31, 0],
                             stroke_color=TEAL, stroke_width=3.2, fill_color=TEAL, fill_opacity=0.34)
            out = VGroup(bg, tr, p1_box, p2_box)

            if cr > 0.02 and sd < 0.1:
                rna_demo = _rna_ribbon(cx, cy, 0.35 + 1.05 * cr, s=0.90, arch_up=True)
                out.add(rna_demo)

            pol = _pol_body(cx, cy, s=1.08, color=WHITE_POL, fill_op=0.38, socket=True)
            out.add(pol)

            if sd > 0.01:
                sy = cy + 0.48 + (1.0 - sd) * 0.65
                sx = cx - 0.10
                sig = _sigma_key(sx, sy, s=1.05)
                out.add(sig)

            if lk > 0.05:
                st_ring = Circle(radius=0.24, color=TEAL, stroke_width=4.5,
                                 fill_color=TEAL, fill_opacity=0.30 * lk).move_to([3.35, yc, 0])
                out.add(st_ring)

            return out

        world = always_redraw(build_bacteria)
        self.add(world)

        # Static labels added AFTER world, well clear of the track [-1.25, +1.45]
        p1_lbl = T("promoter 1", size=24, color=TEAL).move_to([-4.1, -1.68, 0])
        p2_lbl = T("promoter 2", size=24, color=TEAL).move_to([-1.3, -1.68, 0])
        p3_lbl = T("promoter (−35 / −10)", size=24, color=TEAL).move_to([1.35, -1.68, 0])
        st_lbl = T("+1 start", size=24, color=TEAL).move_to([4.05, -1.68, 0])
        self.add(p1_lbl, p2_lbl, p3_lbl, st_lbl)

        state_lbl = boxed_label("core polymerase: joins RNA nucleotides", TEXT,
                                size=26, pad=0.16, fill_opacity=0.24).move_to([0.0, 2.25, 0])
        self.add(state_lbl)

        # Beat 1 (0.0 -> 7.4s)
        self.play(
            core_x.animate.set_value(-1.5),
            cat_rna.animate.set_value(1.0),
            run_time=7.3,
            rate_func=linear
        )

        # Beat 2 (7.60 -> 10.0s)
        self.at("core can join")
        self.play(
            core_x.animate.set_value(-4.4),
            cat_rna.animate.set_value(0.2),
            run_time=2.3,
            rate_func=smooth
        )

        # Beat 3 (10.10 -> 12.55s)
        self.at("finds promoters poorly")
        poor_lbl = boxed_label("core alone: slides past promoters without locking", GOLD,
                               size=26, pad=0.16, fill_opacity=0.24).move_to([0.0, 2.25, 0])
        self.remove(state_lbl)
        self.add(poor_lbl)
        self.play(
            core_x.animate.set_value(1.0),
            cat_rna.animate.set_value(0.0),
            run_time=2.4,
            rate_func=linear
        )

        # Beat 4 (12.76 -> 14.6s)
        self.at("sigma factor docks")
        sig_lbl = boxed_label("sigma factor (promoter key)", VIOLET,
                              size=26, pad=0.16, fill_opacity=0.26).move_to([0.0, 2.25, 0])
        self.remove(poor_lbl)
        self.add(sig_lbl)
        self.play(
            sig_dock.animate.set_value(1.0),
            run_time=1.8,
            rate_func=smooth
        )

        # Beat 5 (14.72 -> 17.4s)
        self.at("forming")
        holo_lbl = boxed_label("holoenzyme (core + sigma)", VIOLET,
                               size=26, pad=0.16, fill_opacity=0.28).move_to([0.0, 2.25, 0])
        self.remove(sig_lbl)
        self.add(holo_lbl)
        self.play(
            core_x.animate.set_value(1.85),
            run_time=2.6,
            rate_func=smooth
        )

        # Beat 6 (17.58 -> 20.8s)
        self.at("sigma recognizes promoter")
        rec_cap = caption("Sigma binds promoter elements (−35 / −10) and positions the active site over +1.",
                          size=26, color=TEXT, y=-2.95)
        self.play(
            FadeIn(rec_cap),
            core_x.animate.set_value(2.25),
            core_y.animate.set_value(-0.42),
            run_time=3.1,
            rate_func=smooth
        )

        # Beat 7 (20.96 -> 23.0s)
        self.at("active site over the start")
        self.play(
            core_x.animate.set_value(2.45),
            lock_t.animate.set_value(1.0),
            run_time=2.0,
            rate_func=smooth
        )
        self.finish()


# =============================================================================
# SHARED HELPER FOR PREDICT + PAUSE (S05 & S06)
# =============================================================================
def _predict_choice_icons(pulse_tracker, highlight_second=0.0):
    """Build only the two animated icons above the choice labels (never crossing text boxes)."""
    pt = pulse_tracker.get_value()
    hl = highlight_second
    sw_base = 3.0 + 1.8 * np.sin(4.2 * pt) * (1.0 - hl)

    # Icon 1 (above Choice 1 at y = 1.95): Green growing-RNA tiles
    c1_y = 1.92
    tiles1 = VGroup(*[
        Polygon([2.15 + i * 0.42, c1_y - 0.18, 0], [2.48 + i * 0.42, c1_y - 0.18, 0],
                [2.48 + i * 0.42, c1_y + 0.18, 0], [2.15 + i * 0.42, c1_y + 0.18, 0],
                stroke_color=GREEN, stroke_width=sw_base * 0.85, fill_color=GREEN, fill_opacity=0.45)
        for i in range(4)
    ])

    # Icon 2 (above Choice 2 at y = -0.05): Teal target-start promoter + ring
    c2_y = -0.05
    sw2 = sw_base if hl < 0.1 else 5.5
    col2 = GOLD if hl > 0.5 else TEAL
    p_icon = Polygon([2.25, c2_y - 0.18, 0], [3.35, c2_y - 0.18, 0],
                     [3.35, c2_y + 0.18, 0], [2.25, c2_y + 0.18, 0],
                     stroke_color=TEAL, stroke_width=sw2 * 0.85, fill_color=TEAL, fill_opacity=0.45)
    ring_icon = Circle(radius=0.22, color=col2, stroke_width=sw2,
                       fill_color=col2, fill_opacity=0.28).move_to([3.65, c2_y, 0])
    icon2 = VGroup(p_icon, ring_icon)

    return VGroup(tiles1, icon2)


# =============================================================================
# SCENE 05: s05_predict
# =============================================================================
class S05Predict(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        det_t = ValueTracker(0.0)
        drift_x = ValueTracker(-1.8)
        pulse_t = ValueTracker(0.0)
        show_c1 = ValueTracker(0.0)
        show_c2 = ValueTracker(0.0)

        head = boxed_label("Remove sigma, leave core intact", VIOLET,
                           size=28, pad=0.16, fill_opacity=0.24).move_to([-2.7, 3.15, 0])
        self.add(head)

        def build_left():
            d = det_t.get_value()
            dx = drift_x.get_value()
            yc = -0.35
            bg = _lane_backdrop(-6.0, 0.45, -1.05, 1.55, color=VIOLET, opacity=0.18)
            tr = _duplex_track(-5.6, 0.1, yc, s=0.92, prom_x=(-3.6, -1.6), start_x=-1.2,
                               bubble_x=None, bubble_open=0.0, show_notches=True)
            pol = _pol_body(dx, yc + 0.28 * d, s=0.88, color=WHITE_POL, fill_op=0.38, socket=True)
            sig = _sigma_key(-3.8, yc + 0.48 + 0.92 * d, s=0.86)
            icons = VGroup()
            if show_c1.get_value() > 0.5:
                icons.add(_predict_choice_icons(pulse_t)[0])
            if show_c2.get_value() > 0.5:
                icons.add(_predict_choice_icons(pulse_t)[1])
            return VGroup(bg, tr, pol, sig, icons)

        left_world = always_redraw(build_left)
        self.add(left_world)

        sig_out_lbl = T("sigma removed", size=25, color=VIOLET).move_to([-1.5, 1.88, 0])
        prom_tag = T("promoter (+1)", size=24, color=TEAL).move_to([-2.4, -1.42, 0])
        self.add(prom_tag)

        # Beat 1 (0.0 -> 4.3s)
        self.play(
            det_t.animate.set_value(1.0),
            drift_x.animate.set_value(-3.2),
            FadeIn(sig_out_lbl),
            run_time=4.2,
            rate_func=smooth
        )

        # Beat 2 (4.50 -> 6.8s)
        self.at("which ability fails")
        q_card = question_card("Without sigma, which ability fails most directly?",
                               options=(), y=-2.95, color=GOLD, size=28, max_w=10.0)
        self.play(
            FadeIn(q_card),
            drift_x.animate.set_value(-1.6),
            run_time=2.3,
            rate_func=linear
        )

        c1_lbl = boxed_label("joining RNA nucleotides", GREEN, size=25, pad=0.16,
                             fill_opacity=0.24).move_to([3.35, 1.15, 0])
        c2_lbl = boxed_label("starting accurately at promoters", TEAL, size=25, pad=0.16,
                             fill_opacity=0.24).move_to([3.35, -0.82, 0])

        # Beat 3 (7.08 -> 9.1s)
        self.at("joining rna nucleotides")
        show_c1.set_value(1.0)
        self.add(c1_lbl)
        self.play(
            pulse_t.animate.set_value(1.5),
            drift_x.animate.set_value(-0.9),
            run_time=2.0,
            rate_func=linear
        )

        # Beat 4 (9.28 -> 11.575s)
        self.at("starting accurately at promoters")
        show_c2.set_value(1.0)
        self.add(c2_lbl)
        self.play(
            pulse_t.animate.set_value(3.8),
            drift_x.animate.set_value(-2.8),
            run_time=2.2,
            rate_func=linear
        )
        self.finish()


# =============================================================================
# SCENE 06: s06_pause (silent: 4.5 s)
# =============================================================================
class S06Pause(PredictPause):
    QUESTION = "Without sigma, which ability fails most directly?"
    OPTIONS = ()
    CARD = {"y": -2.95, "size": 28, "max_w": 10.0}
    RING_AT = (5.75, -2.95, 0)
    SECONDS = 4.5

    def backdrop(self):
        t_hold = ValueTracker(0.0)
        head = boxed_label("Remove sigma, leave core intact", VIOLET,
                           size=28, pad=0.16, fill_opacity=0.24).move_to([-2.7, 3.15, 0])
        sig_out_lbl = T("sigma removed", size=25, color=VIOLET).move_to([-1.5, 1.88, 0])
        prom_tag = T("promoter (+1)", size=24, color=TEAL).move_to([-2.4, -1.42, 0])
        c1_lbl = boxed_label("joining RNA nucleotides", GREEN, size=25, pad=0.16,
                             fill_opacity=0.24).move_to([3.35, 1.15, 0])
        c2_lbl = boxed_label("starting accurately at promoters", TEAL, size=25, pad=0.16,
                             fill_opacity=0.24).move_to([3.35, -0.82, 0])

        def build_pause_scene():
            t = t_hold.get_value()
            yc = -0.35
            dx = -2.8 + 1.8 * np.sin(0.8 * t)
            bg = _lane_backdrop(-6.0, 0.45, -1.05, 1.55, color=VIOLET, opacity=0.18)
            tr = _duplex_track(-5.6, 0.1, yc, s=0.92, prom_x=(-3.6, -1.6), start_x=-1.2,
                               bubble_x=None, bubble_open=0.0, show_notches=True)
            pol = _pol_body(dx, yc + 0.28, s=0.88, color=WHITE_POL, fill_op=0.38, socket=True)
            sig = _sigma_key(-3.8, yc + 1.40, s=0.86)
            icons = _predict_choice_icons(t_hold, highlight_second=0.0)
            return VGroup(bg, tr, pol, sig, icons)

        live = always_redraw(build_pause_scene)
        live.add_updater(lambda m, dt: t_hold.increment_value(dt))
        return VGroup(live, head, sig_out_lbl, prom_tag, c1_lbl, c2_lbl)


# =============================================================================
# SCENE 07: s07_bacterial_reveal
# =============================================================================
class S07BacterialReveal(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        phase_t = ValueTracker(0.0)
        redock_t = ValueTracker(0.0)
        open_t = ValueTracker(0.0)
        abort_t = ValueTracker(0.0)
        escape_t = ValueTracker(0.0)
        drift_t = ValueTracker(0.0)

        head = boxed_label("Answer: Accurate starting at promoters fails without sigma", GOLD,
                           size=28, pad=0.16, fill_opacity=0.26).move_to([0.0, 3.22, 0])
        self.add(head)

        def build_reveal():
            ph = phase_t.get_value()
            rd = redock_t.get_value()
            op = open_t.get_value()
            ab = abort_t.get_value()
            es = escape_t.get_value()
            dr = drift_t.get_value()

            yc = -0.45
            if ph < 0.5:
                bg = _lane_backdrop(-6.0, 0.45, -1.15, 1.45, color=VIOLET, opacity=0.18)
                tr = _duplex_track(-5.6, 0.1, yc, s=0.92, prom_x=(-3.6, -1.6), start_x=-1.2,
                                   bubble_x=None, bubble_open=0.0, show_notches=True)
                dx = -2.6 + 1.5 * np.sin(1.4 * dr)
                pol = _pol_body(dx, yc + 0.28, s=0.88, color=WHITE_POL, fill_op=0.38, socket=True)
                sig = _sigma_key(-3.8, yc + 1.35, s=0.86)
                icons = _predict_choice_icons(drift_t, highlight_second=1.0)
                return VGroup(bg, tr, pol, sig, icons)
            else:
                pol_x = -1.6 + 4.8 * es
                bg = _lane_backdrop(-6.0, 6.0, -1.25, 1.45, color=VIOLET, opacity=0.18)
                tr = _duplex_track(-5.5, 5.5, yc, s=1.12, prom_x=(-3.8, -1.6), start_x=-1.2,
                                   bubble_x=pol_x if op > 0.02 else None, bubble_w=1.60,
                                   bubble_open=op, show_notches=True)
                y_pol = yc + 0.30 * (1.0 - rd)
                pol = _pol_body(pol_x, y_pol, s=1.08, color=WHITE_POL, fill_op=0.38, socket=True)
                sy = y_pol + 0.48 + (1.0 - rd) * 0.65
                sx = pol_x - 0.10 - (1.0 - rd) * 1.2
                sig = _sigma_key(sx, sy, s=1.05)
                grp = VGroup(bg, tr, pol, sig)

                if ab > 0.02 and es < 0.85:
                    for k in range(3):
                        prog_k = np.clip((ab - k * 0.22) / 0.55, 0.0, 1.0)
                        if prog_k > 0.01:
                            tx = -1.2 - 0.65 * prog_k - 0.35 * k
                            ty = yc + 0.55 + 0.65 * prog_k
                            tile = Polygon(
                                [tx - 0.22, ty - 0.10, 0], [tx + 0.22, ty - 0.10, 0],
                                [tx + 0.22, ty + 0.10, 0], [tx - 0.22, ty + 0.10, 0],
                                stroke_color=GREEN, stroke_width=2.8, fill_color=GREEN, fill_opacity=0.55
                            )
                            grp.add(tile)

                if es > 0.02:
                    rna = _rna_ribbon(pol_x, yc, 0.45 + 3.1 * es, s=1.10, arch_up=True)
                    grp.add(rna)

                return grp

        world = always_redraw(build_reveal)
        self.add(world)

        c1_lbl = boxed_label("joining RNA nucleotides (intact)", GREEN, size=25, pad=0.16,
                             fill_opacity=0.20).move_to([3.35, 1.15, 0])
        c2_lbl = boxed_label("✓ starting accurately at promoters fails", GOLD, size=25, pad=0.16,
                             fill_opacity=0.32).move_to([3.35, -0.82, 0])
        self.add(c1_lbl, c2_lbl)

        # Beat 1 (0.0 -> 2.9s)
        self.play(drift_t.animate.set_value(2.0), run_time=2.8, rate_func=linear)

        # Beat 2 (3.08 -> 8.5s)
        self.at("core remains")
        cap1 = caption("Core still joins nucleotides, but without sigma it chooses promoter starts poorly.",
                       size=26, color=TEXT, y=-3.05)
        self.add(cap1)
        self.play(
            drift_t.animate.set_value(5.2),
            run_time=5.3,
            rate_func=linear
        )

        # Beat 3 (8.70 -> 13.2s)
        self.at("restore sigma")
        self.remove(head, cap1, c1_lbl, c2_lbl)
        head2 = boxed_label("Bacterial initiation: closed complex → open complex → escape", VIOLET,
                            size=27, pad=0.16, fill_opacity=0.26).move_to([0.0, 3.22, 0])
        phase_t.set_value(1.0)
        stage_badge = boxed_label("1. closed complex (DNA still double-stranded)", TEAL,
                                  size=26, pad=0.16, fill_opacity=0.26).move_to([0.0, 2.22, 0])
        prom_lbl = T("promoter (−35 / −10)", size=24, color=TEAL).move_to([-3.0, -1.68, 0])
        st_lbl = T("+1 start", size=24, color=TEAL).move_to([-0.4, -1.68, 0])
        self.add(head2, stage_badge, prom_lbl, st_lbl)
        self.play(
            redock_t.animate.set_value(1.0),
            run_time=4.4,
            rate_func=smooth
        )

        # Beat 4 (13.48 -> 16.6s)
        self.at("dna then opens")
        open_badge = boxed_label("2. open complex (DNA melts around +1)", BLUE,
                                 size=26, pad=0.16, fill_opacity=0.26).move_to([0.0, 2.22, 0])
        self.remove(stage_badge)
        self.add(open_badge)
        self.play(
            open_t.animate.set_value(1.0),
            run_time=3.1,
            rate_func=smooth
        )

        # Beat 5 (16.86 -> 18.9s)
        self.at("short rnas")
        abort_badge = boxed_label("3. abortive initiation: short RNAs released", GREEN,
                                  size=26, pad=0.16, fill_opacity=0.26).move_to([0.0, 2.22, 0])
        self.remove(open_badge)
        self.add(abort_badge)
        self.play(
            abort_t.animate.set_value(1.0),
            run_time=2.0,
            rate_func=linear
        )

        # Beat 6 (19.08 -> 21.875s)
        self.at("polymerase escapes")
        esc_badge = boxed_label("4. promoter escape → productive elongation", GREEN,
                                size=26, pad=0.16, fill_opacity=0.28).move_to([0.0, 2.22, 0])
        self.remove(abort_badge)
        self.add(esc_badge)
        self.play(
            escape_t.animate.set_value(1.0),
            run_time=2.7,
            rate_func=smooth
        )
        self.finish()


# =============================================================================
# SCENE 08: s08_nuclear_division
# =============================================================================
class S08NuclearDivision(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        head = boxed_label("Eukaryotic nucleus: 3 polymerases divide the work", YELLOW,
                           size=28, pad=0.16, fill_opacity=0.24).move_to([0.0, 3.25, 0])
        self.add(head)

        split_t = ValueTracker(0.0)
        dock_t = ValueTracker(0.0)
        p1_t = ValueTracker(0.0)
        p2_t = ValueTracker(0.0)
        p3_t = ValueTracker(0.0)

        def build_nuclear_lanes():
            sp = split_t.get_value()
            dk = dock_t.get_value()
            t1, t2, t3 = p1_t.get_value(), p2_t.get_value(), p3_t.get_value()
            g = VGroup()

            ys = [1.85 * sp, 0.05, -1.75 * sp]
            progs = [t1, t2, t3]
            cols = [BLUE, GOLD, TEAL]

            for i in range(3):
                yc = ys[i]
                pr = progs[i]
                bg = _lane_backdrop(-4.35, 0.85, yc - 0.62, yc + 0.62, color=cols[i], opacity=0.18)
                px = (-3.7 * (1.0 - dk) + (-2.8) * dk) + 2.5 * pr
                tr = _duplex_track(-4.10, 0.55, yc, s=0.66, prom_x=(-3.8, -2.7), start_x=-2.5,
                                   bubble_x=px if pr > 0.02 else None, bubble_w=1.1,
                                   bubble_open=min(1.0, pr * 2.5), show_notches=False)
                pol = _pol_body(px, yc, s=0.62, color=WHITE_POL, fill_op=0.38)
                g.add(bg, tr, pol)

                if pr > 0.02:
                    x_start = px - 0.22
                    x_end = x_start + (0.82 - x_start) * pr
                    pts = [[x, yc + 0.24 + 0.06 * np.sin(6.0 * (x - x_start)), 0]
                           for x in np.linspace(x_start, max(x_start + 0.15, x_end), 24)]
                    rib = VMobject(stroke_color=GREEN, stroke_width=6.0, fill_opacity=0)
                    rib.set_points_as_corners(pts)
                    dot_end = Dot(pts[-1], radius=0.07, color=GREEN)
                    g.add(rib, dot_end)

            return g

        lanes_live = always_redraw(build_nuclear_lanes)
        self.add(lanes_live)

        l_pol1 = boxed_label("Pol I", BLUE, size=26, pad=0.16, fill_opacity=0.26).move_to([-5.30, 1.85, 0])
        l_pol2 = boxed_label("Pol II", GOLD, size=26, pad=0.16, fill_opacity=0.26).move_to([-5.30, 0.05, 0])
        l_pol3 = boxed_label("Pol III", TEAL, size=26, pad=0.16, fill_opacity=0.26).move_to([-5.30, -1.75, 0])

        # Product bins placed at x = 3.55 (spanning x = 1.25 to 5.85, completely clear of tracks and frame edge)
        bin1 = boxed_label("large rRNA precursor", GREEN, size=25, pad=0.20, fill_opacity=0.22).move_to([3.55, 1.85, 0])
        bin2 = boxed_label("mRNA precursors,\nsnRNAs, miRNA precursors", GREEN, size=24, pad=0.18, fill_opacity=0.22).move_to([3.55, 0.05, 0])
        bin3 = boxed_label("tRNAs, 5S rRNA, small RNAs", GREEN, size=25, pad=0.20, fill_opacity=0.22).move_to([3.55, -1.75, 0])

        # Beat 1 (0.0 -> 6.1s)
        self.play(
            split_t.animate.set_value(1.0),
            run_time=1.3,
            rate_func=smooth
        )
        self.add(l_pol1, l_pol2, l_pol3)
        self.play(
            dock_t.animate.set_value(1.0),
            run_time=4.5,
            rate_func=smooth
        )

        # Beat 2 (6.30 -> 11.2s)
        self.at("large ribosomal")
        self.play(
            FadeIn(bin1),
            p1_t.animate.set_value(1.0),
            run_time=3.5,
            rate_func=linear
        )

        # Beat 3 (11.44 -> 19.9s)
        self.at("messenger rna")
        self.play(
            FadeIn(bin2),
            p2_t.animate.set_value(0.55),
            run_time=2.5,
            rate_func=linear
        )
        self.at("small nuclear")
        self.play(
            p2_t.animate.set_value(1.0),
            run_time=4.6,
            rate_func=linear
        )

        # Beat 4 (20.24 -> 27.125s)
        self.at("transfer rnas")
        self.play(
            FadeIn(bin3),
            p3_t.animate.set_value(0.55),
            run_time=1.8,
            rate_func=linear
        )
        self.at("separate ribosomal")
        self.play(
            p3_t.animate.set_value(1.0),
            run_time=3.6,
            rate_func=linear
        )
        self.finish()


# =============================================================================
# SCENE 09: s09_pol_two
# =============================================================================
class S09PolTwo(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        head = boxed_label("Pol II lane: general transcription factors build the start platform",
                           GOLD, size=27, pad=0.16, fill_opacity=0.24).move_to([0.0, 3.25, 0])
        self.add(head)

        zoom_t = ValueTracker(0.0)
        rec_f = ValueTracker(0.0)
        pos_f = ValueTracker(0.0)
        open_f = ValueTracker(0.0)
        exch_t = ValueTracker(0.0)

        def build_pol_two():
            zm = zoom_t.get_value()
            rf = rec_f.get_value()
            pf = pos_f.get_value()
            of = open_f.get_value()
            ex = exch_t.get_value()

            yc = -0.60
            sc = 0.85 + 0.30 * zm
            bg = _lane_backdrop(-6.0, 6.0, -1.30, 1.40, color=GOLD, opacity=0.18)
            tr = _duplex_track(-5.5, 5.5, yc, s=sc, prom_x=(-3.4, -1.1), start_x=-0.6,
                               bubble_x=-0.4 if of > 0.02 else None, bubble_w=1.60,
                               bubble_open=of, show_notches=False)
            g = VGroup(bg, tr)

            if rf > 0.01:
                ry = yc + 0.38 + (1.0 - rf) * 0.75 + 0.06 * np.sin(4.5 * ex) * (1.0 if ex > 0.01 else 0.0)
                f_rec = Polygon(
                    [-3.25, ry - 0.22, 0], [-1.45, ry - 0.22, 0],
                    [-1.60, ry + 0.22, 0], [-3.10, ry + 0.22, 0],
                    stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.45 * rf
                )
                g.add(f_rec)

            if pf > 0.01:
                py = yc + 0.38 + (1.0 - pf) * 0.75 + 0.06 * np.cos(4.5 * ex) * (1.0 if ex > 0.01 else 0.0)
                f_pos = Polygon(
                    [-1.42, py - 0.22, 0], [-0.15, py - 0.22, 0],
                    [-0.15, py + 0.22, 0], [-1.42, py + 0.22, 0],
                    stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.45 * pf
                )
                g.add(f_pos)

            if of > 0.01:
                oy = yc + 0.32 + (1.0 - of) * 0.75 - 0.06 * np.sin(4.5 * ex) * (1.0 if ex > 0.01 else 0.0)
                f_open = Polygon(
                    [0.25, oy - 0.24, 0], [1.55, oy - 0.24, 0],
                    [1.55, oy + 0.24, 0], [0.25, oy + 0.24, 0],
                    stroke_color=ORANGE, stroke_width=3.5, fill_color=ORANGE, fill_opacity=0.45 * of
                )
                g.add(f_open)

            pol_x = 2.6 * (1.0 - pf) + (-0.65) * pf
            pol_y = (yc + 1.05) * (1.0 - pf) + (yc + 0.10) * pf
            pol = _pol_body(pol_x, pol_y, s=1.08, color=WHITE_POL, fill_op=0.38)
            g.add(pol)

            if ex > 0.01:
                for k, (col_k, x_base) in enumerate([(TEAL, -2.35), (YELLOW, -0.80), (ORANGE, 0.90)]):
                    phase = 3.6 * ex + k * 2.1
                    ex_x = x_base + 0.50 * np.cos(phase)
                    ex_y = yc + 1.15 + 0.20 * np.sin(phase)
                    dup = Polygon(
                        [ex_x - 0.40, ex_y - 0.14, 0], [ex_x + 0.40, ex_y - 0.14, 0],
                        [ex_x + 0.40, ex_y + 0.14, 0], [ex_x - 0.40, ex_y + 0.14, 0],
                        stroke_color=col_k, stroke_width=2.8, fill_color=col_k, fill_opacity=0.36
                    )
                    g.add(dup)

            return g

        world = always_redraw(build_pol_two)
        self.add(world)

        prom_lbl = T("core promoter", size=25, color=TEAL).move_to([-2.4, -1.68, 0])
        start_lbl = T("+1 start", size=25, color=TEAL).move_to([-0.4, -1.68, 0])
        self.add(prom_lbl, start_lbl)

        pol2_tag = boxed_label("Pol II (makes mRNA precursors)", TEXT,
                               size=25, pad=0.14, fill_opacity=0.24).move_to([2.6, 2.25, 0])
        self.add(pol2_tag)

        # Beat 1 (0.0 -> 6.0s)
        self.play(zoom_t.animate.set_value(1.0), run_time=5.8, rate_func=smooth)

        # Beat 2 (6.22 -> 10.9s)
        self.at("general transcription factors")
        gtf_tag = boxed_label("general transcription factors", YELLOW,
                              size=25, pad=0.14, fill_opacity=0.24).move_to([-2.6, 2.25, 0])
        self.play(
            FadeIn(gtf_tag),
            rec_f.animate.set_value(0.35),
            run_time=4.6,
            rate_func=smooth
        )

        # Beat 3 (11.34 -> 14.0s)
        self.at("recognize promoter dna")
        lbl_rec = boxed_label("recognize", TEAL, size=25, pad=0.14, fill_opacity=0.28).move_to([-4.2, 2.25, 0])
        self.remove(gtf_tag)
        self.add(lbl_rec)
        self.play(
            rec_f.animate.set_value(1.0),
            run_time=2.6,
            rate_func=smooth
        )

        # Beat 4 (14.22 -> 16.1s)
        self.at("others position polymerase")
        lbl_pos = boxed_label("position", YELLOW, size=25, pad=0.14, fill_opacity=0.28).move_to([-2.0, 2.25, 0])
        self.remove(pol2_tag)
        self.add(lbl_pos)
        self.play(
            pos_f.animate.set_value(1.0),
            run_time=1.9,
            rate_func=smooth
        )

        # Beat 5 (16.26 -> 18.5s)
        self.at("help open the template")
        lbl_open = boxed_label("open", ORANGE, size=25, pad=0.14, fill_opacity=0.28).move_to([0.1, 2.25, 0])
        self.add(lbl_open)
        self.play(
            open_f.animate.set_value(1.0),
            run_time=2.2,
            rate_func=smooth
        )

        # Beat 6 (18.74 -> 24.2s)
        self.at("classic sequence is useful")
        cap = caption("Classic assembly order is a useful guide; in living nuclei, factors exchange rapidly.",
                      size=26, color=GOLD, y=-3.05)
        self.play(FadeIn(cap), exch_t.animate.set_value(0.8), run_time=2.1, rate_func=linear)

        self.at("living complexes exchange")
        ex_tag = boxed_label("living complexes: rapid exchange", GOLD,
                             size=24, pad=0.14, fill_opacity=0.26).move_to([3.4, 2.25, 0])
        self.add(ex_tag)
        self.play(
            exch_t.animate.set_value(3.2),
            run_time=3.1,
            rate_func=linear
        )
        self.finish()


# =============================================================================
# SCENE 10: s10_escape
# =============================================================================
class S10Escape(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        open_t = ValueTracker(0.0)
        rna_t = ValueTracker(0.0)
        esc_x = ValueTracker(-3.2)
        shed_t = ValueTracker(0.0)
        merge_t = ValueTracker(0.0)

        head = boxed_label("Promoter escape → shared directional elongation", GREEN,
                           size=28, pad=0.16, fill_opacity=0.24).move_to([0.0, 3.25, 0])
        self.add(head)

        def build_escape():
            op = open_t.get_value()
            rn = rna_t.get_value()
            px = esc_x.get_value()
            sh = shed_t.get_value()
            mg = merge_t.get_value()
            g = VGroup()

            if mg < 0.98:
                y_top = 1.15 * (1.0 - mg) + (-0.25) * mg
                y_bot = -1.65 * (1.0 - mg) + (-0.25) * mg
                sc = 0.84 + 0.30 * mg

                for idx, (yc, col_l) in enumerate([(y_top, VIOLET), (y_bot, YELLOW)]):
                    bg = _lane_backdrop(-5.9, 5.9, yc - 0.72, yc + 0.72, color=col_l, opacity=0.18)
                    tr = _duplex_track(-5.4, 5.4, yc, s=sc, prom_x=(-4.2, -2.0), start_x=-1.8,
                                       bubble_x=px, bubble_w=1.55, bubble_open=op, show_notches=(idx == 0))
                    rna = _rna_ribbon(px, yc, 0.25 + 2.6 * rn, s=sc, arch_up=True) if rn > 0.01 else VGroup()
                    pol = _pol_body(px, yc, s=sc * 0.92, color=WHITE_POL, fill_op=0.38, socket=(idx == 0))
                    g.add(bg, tr, rna, pol)

                    if mg < 0.5:
                        fade_fac = max(0.0, 1.0 - 1.8 * mg)
                        if idx == 0:
                            # Sigma factor releases / lifts behind as polymerase escapes
                            sig_x = -3.2 - 0.65 * sh
                            sig_y = yc + 0.42 + 0.38 * sh
                            sig = _sigma_key(sig_x, sig_y, s=0.72 * sc)
                            sig.set_opacity(0.45 * fade_fac)
                            g.add(sig)
                        else:
                            # GTF platform stays behind at core promoter
                            gtf = Polygon(
                                [-4.0, yc + 0.16, 0], [-2.1, yc + 0.16, 0],
                                [-2.2, yc + 0.46, 0], [-3.9, yc + 0.46, 0],
                                stroke_color=YELLOW, stroke_width=3.0, fill_color=YELLOW, fill_opacity=0.38 * fade_fac
                            )
                            g.add(gtf)
            else:
                yc = -0.25
                sc = 1.16
                bg = _lane_backdrop(-6.0, 6.0, -1.15, 1.25, color=GREEN, opacity=0.18)
                tr = _duplex_track(-5.5, 5.5, yc, s=sc, prom_x=(-4.6, -2.6), start_x=-2.3,
                                   bubble_x=px, bubble_w=1.7, bubble_open=1.0, show_notches=False)
                rna = _rna_ribbon(px, yc, 0.4 + 3.2 * rn, s=sc, arch_up=True)
                pol = _pol_body(px, yc, s=1.12, color=WHITE_POL, fill_op=0.40)
                g.add(bg, tr, rna, pol)

            return g

        world = always_redraw(build_escape)
        self.add(world)

        l_ecoli = boxed_label("E. coli", VIOLET, size=25, pad=0.14, fill_opacity=0.24).move_to([-5.15, 2.25, 0])
        l_nuc = boxed_label("Nucleus (Pol II)", YELLOW, size=25, pad=0.14, fill_opacity=0.24).move_to([-4.65, -0.55, 0])
        self.add(l_ecoli, l_nuc)

        # Beat 1 (0.0 -> 3.9s)
        self.play(
            open_t.animate.set_value(0.65),
            esc_x.animate.set_value(-2.1),
            shed_t.animate.set_value(0.55),
            run_time=3.8,
            rate_func=linear
        )

        # Beat 2 (4.10 -> 5.4s)
        self.at("dna opens")
        self.play(
            open_t.animate.set_value(1.0),
            esc_x.animate.set_value(-1.4),
            shed_t.animate.set_value(1.0),
            run_time=1.3,
            rate_func=linear
        )

        # Beat 3 (5.58 -> 7.1s)
        self.at("green rna begins")
        self.play(
            rna_t.animate.set_value(0.42),
            esc_x.animate.set_value(-0.5),
            run_time=1.5,
            rate_func=linear
        )

        # Beat 4 (7.30 -> 9.9s)
        self.at("polymerase escapes")
        self.play(
            esc_x.animate.set_value(0.8),
            rna_t.animate.set_value(0.70),
            run_time=2.6,
            rate_func=linear
        )

        # Beat 5 (11.08 -> 13.6s)
        self.at("direction rule still applies")
        self.remove(l_ecoli, l_nuc)
        dir_temp = boxed_label("template DNA read 3' → 5'", BLUE, size=25, pad=0.14, fill_opacity=0.26).move_to([-2.8, -1.72, 0])
        dir_cod = boxed_label("coding DNA 5' → 3'", GOLD, size=25, pad=0.14, fill_opacity=0.26).move_to([2.6, -1.72, 0])
        dir_rna = boxed_label("RNA grows 5' → 3'", GREEN, size=26, pad=0.16, fill_opacity=0.28).move_to([2.2, 2.05, 0])
        self.play(
            merge_t.animate.set_value(1.0),
            esc_x.animate.set_value(1.4),
            FadeIn(dir_temp),
            FadeIn(dir_cod),
            FadeIn(dir_rna),
            run_time=2.6,
            rate_func=smooth
        )

        # Beat 6 (13.84 -> 16.0s)
        self.at("different proteins chose")
        start_team = boxed_label("start chosen by sigma or GTFs", TEAL,
                                 size=25, pad=0.14, fill_opacity=0.26).move_to([-2.8, 2.05, 0])
        self.play(
            FadeIn(start_team),
            esc_x.animate.set_value(2.4),
            rna_t.animate.set_value(0.86),
            run_time=2.1,
            rate_func=linear
        )

        # Beat 7 (16.18 -> 19.075s)
        self.at("chemistry fixes")
        self.play(
            esc_x.animate.set_value(3.6),
            rna_t.animate.set_value(1.0),
            run_time=2.8,
            rate_func=linear
        )
        self.finish()


# =============================================================================
# SCENE 11: s11_bacterial_stop
# =============================================================================
class S11BacterialStop(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        head = boxed_label("Bacterial termination: two routes to release RNA and polymerase",
                           RED, size=27, pad=0.16, fill_opacity=0.24).move_to([0.0, 3.25, 0])
        self.add(head)

        split_t = ValueTracker(0.0)
        elong_t = ValueTracker(0.0)
        hp_fold = ValueTracker(0.0)
        utract_t = ValueTracker(0.0)
        destab_t = ValueTracker(0.0)
        rho_bind = ValueTracker(0.0)
        rho_adv = ValueTracker(0.0)
        rho_rel = ValueTracker(0.0)

        def build_bact_stop():
            sp = split_t.get_value()
            el = elong_t.get_value()
            hf = hp_fold.get_value()
            ut = utract_t.get_value()
            ds = destab_t.get_value()
            rb = rho_bind.get_value()
            ra = rho_adv.get_value()
            rr = rho_rel.get_value()

            g = VGroup()
            y_top = 0.95 * sp
            y_bot = -1.95 * sp

            bg_top = _lane_backdrop(-5.9, 5.9, y_top - 0.65, y_top + 0.65, color=GREEN, opacity=0.18)
            pol_x1 = -1.2 * (1.0 - el) + 1.4 * el + 0.35 * hf + 0.45 * ds
            pol_y1 = y_top + 0.28 * ds
            tr_top = _duplex_track(-5.4, 5.4, y_top, s=0.78, prom_x=None, start_x=None,
                                   bubble_x=pol_x1, bubble_w=1.45, bubble_open=1.0 - 0.85 * ds, show_notches=False)
            g.add(bg_top, tr_top)

            if ut > 0.01:
                u_strip = Polygon(
                    [pol_x1 - 0.70, y_top - 0.26, 0], [pol_x1 + 0.30, y_top - 0.26, 0],
                    [pol_x1 + 0.30, y_top + 0.02, 0], [pol_x1 - 0.70, y_top + 0.02, 0],
                    stroke_color=GOLD, stroke_width=3.2, fill_color=GOLD, fill_opacity=0.48 * ut * (1.0 - 0.6 * ds)
                )
                g.add(u_strip)

            hx = pol_x1 - 1.15 - 0.12 * ds
            hy = pol_y1 + 0.10
            if hf < 0.05:
                rna1 = _rna_ribbon(pol_x1, pol_y1, 1.4 + 0.6 * el, s=0.78, arch_up=True)
                g.add(rna1)
            else:
                stem_h = 0.24 * hf
                hp_stem = Polygon(
                    [hx - 0.14, hy, 0], [hx + 0.14, hy, 0],
                    [hx + 0.14, hy + stem_h, 0], [hx - 0.14, hy + stem_h, 0],
                    stroke_color=GREEN, stroke_width=4.0, fill_color=GREEN, fill_opacity=0.45
                )
                hp_loop = Circle(radius=0.15 * hf + 0.04, color=GREEN, stroke_width=4.5,
                                 fill_color=GREEN, fill_opacity=0.35).move_to([hx, hy + stem_h + 0.12 * hf, 0])
                conn1 = Line([pol_x1 - 0.32, pol_y1 + 0.04, 0], [hx + 0.14, hy, 0],
                             stroke_color=GREEN, stroke_width=5.5)
                tail1 = Line([hx - 0.14, hy, 0], [hx - 0.85, hy - 0.06, 0],
                             stroke_color=GREEN, stroke_width=5.5)
                g.add(conn1, tail1, hp_stem, hp_loop)

            pol1 = _pol_body(pol_x1, pol_y1, s=0.76, color=WHITE_POL, fill_op=0.38)
            g.add(pol1)

            if sp > 0.05:
                bg_bot = _lane_backdrop(-5.9, 5.9, y_bot - 0.65, y_bot + 0.65, color=VIOLET, opacity=0.18)
                pol_x2 = -0.8 * (1.0 - el) + 1.8 * el + 0.45 * rr
                pol_y2 = y_bot + 0.46 * rr
                tr_bot = _duplex_track(-5.4, 5.4, y_bot, s=0.78, prom_x=None, start_x=None,
                                       bubble_x=pol_x2, bubble_w=1.45, bubble_open=1.0 - 0.85 * rr, show_notches=False)
                rna2 = _rna_ribbon(pol_x2 - 0.25 * rr, pol_y2 + 0.10 * rr, 2.2 + 1.0 * el, s=0.78, arch_up=True)
                pol2 = _pol_body(pol_x2, pol_y2, s=0.76, color=WHITE_POL, fill_op=0.38)
                g.add(bg_bot, tr_bot, rna2, pol2)

                if rb > 0.01:
                    rx = (pol_x2 - 2.85) * (1.0 - ra) + (pol_x2 - 0.72) * ra
                    ry = pol_y2 + 0.30
                    rho_outer = Circle(radius=0.26, color=VIOLET, stroke_width=5.0,
                                       fill_color=VIOLET, fill_opacity=0.45 * rb).move_to([rx, ry, 0])
                    rho_inner = Circle(radius=0.10, color=TEXT, stroke_width=2.5,
                                       fill_color=DARK_PANEL, fill_opacity=0.9).move_to([rx, ry, 0])
                    g.add(rho_outer, rho_inner)

            return g

        world = always_redraw(build_bact_stop)
        self.add(world)

        l_intr = boxed_label("Route 1: Intrinsic (hairpin + U-rich tract)", GREEN,
                             size=24, pad=0.14, fill_opacity=0.25).move_to([-3.0, 2.42, 0])
        l_rho = boxed_label("Route 2: Rho-dependent", VIOLET,
                            size=25, pad=0.14, fill_opacity=0.25).move_to([-3.8, -0.45, 0])

        # Beat 1 (0.0 -> 4.2s)
        self.play(
            split_t.animate.set_value(1.0),
            elong_t.animate.set_value(1.0),
            FadeIn(l_intr),
            FadeIn(l_rho),
            run_time=4.1,
            rate_func=smooth
        )

        # Beat 2 (5.26 -> 6.9s)
        self.at("rna folds into a hairpin")
        hp_tag = boxed_label("RNA hairpin", GREEN, size=24, pad=0.14, fill_opacity=0.26).move_to([2.1, 2.38, 0])
        self.play(
            FadeIn(hp_tag),
            hp_fold.animate.set_value(1.0),
            run_time=1.7,
            rate_func=smooth
        )

        # Beat 3 (7.04 -> 10.2s)
        self.at("followed by")
        u_tag = boxed_label("U-rich tract", GOLD, size=24, pad=0.14, fill_opacity=0.26).move_to([4.3, 2.38, 0])
        self.play(
            FadeIn(u_tag),
            utract_t.animate.set_value(1.0),
            run_time=3.1,
            rate_func=smooth
        )

        # Beat 4 (10.86 -> 13.3s)
        self.at("destabilize the complex")
        self.play(destab_t.animate.set_value(1.0), run_time=2.4, rate_func=smooth)

        # Beat 5 (14.38 -> 15.7s)
        self.at("rho binds the rna")
        rho_tag = boxed_label("Rho factor binds RNA & advances", VIOLET,
                              size=24, pad=0.14, fill_opacity=0.26).move_to([2.4, -0.45, 0])
        self.play(
            FadeIn(rho_tag),
            rho_bind.animate.set_value(1.0),
            run_time=1.3,
            rate_func=smooth
        )

        # Beat 6 (15.90 -> 17.5s)
        self.at("advances toward polymerase")
        self.play(rho_adv.animate.set_value(1.0), run_time=1.6, rate_func=linear)

        # Beat 7 (17.70 -> 19.175s)
        self.at("promotes release")
        self.play(rho_rel.animate.set_value(1.0), run_time=1.4, rate_func=smooth)
        self.finish()


# =============================================================================
# SCENE 12: s12_pol_two_stop
# =============================================================================
class S12PolTwoStop(SpokenScene):
    def construct(self):
        self.add(scope_tag("supported model, schematic", size=24, color=TEXT))

        head = boxed_label("Pol II termination: RNA cut at poly(A) site + exonuclease pursuit",
                           ORANGE, size=27, pad=0.16, fill_opacity=0.24).move_to([-0.8, 3.25, 0])
        self.add(head)

        pol_x = ValueTracker(-3.2)
        pol_speed = ValueTracker(1.00)
        cut_t = ValueTracker(0.0)
        chase_t = ValueTracker(0.0)
        rel_t = ValueTracker(0.0)

        def build_pol2_stop():
            px = pol_x.get_value()
            sp = pol_speed.get_value()
            ct = cut_t.get_value()
            ch = chase_t.get_value()
            rl = rel_t.get_value()

            yc = -0.45
            bg = _lane_backdrop(-6.0, 6.0, -1.20, 1.35, color=GOLD, opacity=0.18)
            tr = _duplex_track(-5.5, 5.5, yc, s=1.10, prom_x=(-1.8, -0.6), start_x=None,
                               bubble_x=px, bubble_w=1.60, bubble_open=1.0 - 0.8 * rl, show_notches=False)
            g = VGroup(bg, tr)

            bar_w = 2.6
            bar_bg = Polygon([3.05, 1.62, 0], [3.05 + bar_w, 1.62, 0],
                             [3.05 + bar_w, 1.84, 0], [3.05, 1.84, 0],
                             stroke_color=TEXT, stroke_width=2.2, fill_color=DARK_PANEL, fill_opacity=0.9)
            fill_w = max(0.06, bar_w * sp)
            bar_fill = Polygon([3.05, 1.62, 0], [3.05 + fill_w, 1.62, 0],
                               [3.05 + fill_w, 1.84, 0], [3.05, 1.84, 0],
                               stroke_width=0, fill_color=GOLD if sp > 0.5 else RED, fill_opacity=0.85)
            bar_dot = Dot([3.05 + fill_w, 1.73, 0], radius=0.10, color=TEXT)
            g.add(bar_bg, bar_fill, bar_dot)

            pol_y = yc + 0.35 * rl
            if ct < 0.05:
                rna_len = max(0.5, (px - (-3.6)) * 0.85)
                rna = _rna_ribbon(px, pol_y, rna_len, s=1.08, arch_up=True)
                g.add(rna)
            else:
                free_x = -1.6 - 0.9 * ct
                free_y = yc + 0.55 + 0.25 * ct
                free_rna = Line([free_x - 1.8, free_y + 0.12, 0], [free_x, free_y, 0],
                                stroke_color=GREEN, stroke_width=7.5)
                pa_badge = Polygon([free_x - 0.55, free_y - 0.14, 0], [free_x - 0.05, free_y - 0.14, 0],
                                   [free_x - 0.05, free_y + 0.14, 0], [free_x - 0.55, free_y + 0.14, 0],
                                   stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.55)
                cut_mark = VGroup(
                    Line([free_x + 0.18, free_y - 0.20, 0], [free_x + 0.42, free_y + 0.20, 0], stroke_color=RED, stroke_width=4.5),
                    Line([free_x + 0.18, free_y + 0.20, 0], [free_x + 0.42, free_y - 0.20, 0], stroke_color=RED, stroke_width=4.5),
                )
                g.add(free_rna, pa_badge, cut_mark)

                stub_start_x = (-0.9) * (1.0 - ch) + (px - 0.55) * ch
                if px - 0.25 > stub_start_x + 0.08:
                    stub = Line([stub_start_x, pol_y + 0.32, 0], [px - 0.25, pol_y + 0.10, 0],
                                stroke_color=GREEN, stroke_width=7.0)
                    g.add(stub)

                if ch > 0.01:
                    fx = stub_start_x
                    fy = pol_y + 0.34
                    follower = Polygon(
                        [fx - 0.44, fy - 0.24, 0], [fx + 0.26, fy - 0.24, 0],
                        [fx + 0.05, fy, 0], [fx + 0.26, fy + 0.24, 0],
                        [fx - 0.44, fy + 0.24, 0],
                        stroke_color=ORANGE, stroke_width=3.8, fill_color=ORANGE, fill_opacity=0.55
                    )
                    g.add(follower)

            p_col = WHITE_POL if sp > 0.45 else GOLD
            pol = _pol_body(px, pol_y, s=1.08, color=p_col, fill_op=0.40)
            g.add(pol)

            return g

        world = always_redraw(build_pol2_stop)
        self.add(world)

        speed_panel = Readout(
            [("Pol II speed", lambda: pol_speed.get_value(), "{:4.2f}x", TEXT)],
            at=[4.35, 2.35, 0], size=25, widest=[1.00], color=GOLD
        )
        pa_lbl = T("poly(A) signal", size=25, color=TEAL).move_to([-1.2, -1.68, 0])
        self.add(speed_panel, pa_lbl)

        # Beat 1 (0.0 -> 5.4s)
        self.play(pol_x.animate.set_value(-0.9), run_time=5.3, rate_func=linear)

        # Beat 2 (5.64 -> 7.6s)
        self.at("copies a polyadenylation signal")
        self.play(pol_x.animate.set_value(0.4), run_time=2.0, rate_func=linear)

        # Beat 3 (7.74 -> 9.9s)
        self.at("the rna is cut")
        cut_lbl = boxed_label("RNA cut downstream of poly(A) signal", RED,
                              size=25, pad=0.14, fill_opacity=0.26).move_to([-2.4, 2.25, 0])
        self.add(cut_lbl)
        self.play(
            cut_t.animate.set_value(1.0),
            pol_x.animate.set_value(1.2),
            pol_speed.animate.set_value(0.75),
            run_time=2.2,
            rate_func=linear
        )

        # Beat 4 (10.24 -> 14.9s)
        self.at("following enzyme degrades")
        foll_lbl = boxed_label("following enzyme degrades attached RNA", ORANGE,
                               size=25, pad=0.14, fill_opacity=0.26).move_to([-2.2, 2.25, 0])
        self.remove(cut_lbl)
        self.add(foll_lbl)
        self.play(
            chase_t.animate.set_value(0.60),
            pol_x.animate.set_value(2.4),
            pol_speed.animate.set_value(0.45),
            run_time=4.6,
            rate_func=linear
        )

        # Beat 5 (15.20 -> 19.3s)
        self.at("evidence supports this pursuit")
        cap = caption("Pursuit works together with changes that slow Pol II after the poly(A) site.",
                      size=26, color=GOLD, y=-2.95)
        self.add(cap)
        self.play(
            chase_t.animate.set_value(0.90),
            pol_x.animate.set_value(3.0),
            pol_speed.animate.set_value(0.22),
            run_time=4.1,
            rate_func=linear
        )

        # Beat 6 (19.48 -> 20.875s)
        self.at("ready to stop")
        stop_lbl = boxed_label("Pol II slows & stops → release", GOLD,
                               size=25, pad=0.14, fill_opacity=0.28).move_to([-2.2, 2.25, 0])
        self.remove(foll_lbl)
        self.add(stop_lbl)
        self.play(
            chase_t.animate.set_value(1.0),
            pol_speed.animate.set_value(0.10),
            rel_t.animate.set_value(1.0),
            run_time=1.3,
            rate_func=smooth
        )
        self.finish()


# =============================================================================
# SCENE 13: s13_close
# =============================================================================
class S13Close(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic", size=24, color=TEXT))

        head = boxed_label("Two separate control gates around one shared directional reaction",
                           GOLD, size=27, pad=0.16, fill_opacity=0.24).move_to([0.0, 3.25, 0])
        self.add(head)

        gates_t = ValueTracker(0.0)
        init_t = ValueTracker(0.0)
        term_t = ValueTracker(0.0)
        journey_t = ValueTracker(0.0)
        rel_end = ValueTracker(0.0)

        init_box1 = boxed_label("E. coli: sigma + core", VIOLET, size=24, pad=0.14, fill_opacity=0.26).move_to([-4.1, 2.18, 0])
        init_box2 = boxed_label("Nucleus: GTFs + Pol I / II / III", YELLOW, size=24, pad=0.14, fill_opacity=0.26).move_to([-3.7, 1.42, 0])

        term_box1 = boxed_label("Bacteria: hairpin + U-tract or Rho", GREEN, size=24, pad=0.14, fill_opacity=0.26).move_to([3.55, 2.18, 0])
        term_box2 = boxed_label("Pol II: poly(A) cut + pursuit (supported)", ORANGE, size=24, pad=0.14, fill_opacity=0.26).move_to([3.45, 1.42, 0])

        def build_full_journey():
            gt = gates_t.get_value()
            it = init_t.get_value()
            tt = term_t.get_value()
            jt = journey_t.get_value()
            re = rel_end.get_value()

            yc = -0.55
            bg = _lane_backdrop(-6.0, 6.0, -1.35, 0.75, color=BLUE, opacity=0.18)
            px = -5.0 * (1.0 - it) + (-4.0) * it + 8.1 * jt
            tr = _duplex_track(-5.5, 5.5, yc, s=1.08, prom_x=(-4.8, -3.4), start_x=-4.0,
                               bubble_x=px if it > 0.2 else None, bubble_w=1.6,
                               bubble_open=min(1.0, it * 1.4) * (1.0 - 0.85 * re), show_notches=True)
            g = VGroup(bg, tr)

            gh = 0.68 * gt
            start_gate = Polygon(
                [-4.45, yc - gh, 0], [-3.55, yc - gh, 0],
                [-3.55, yc + gh, 0], [-4.45, yc + gh, 0],
                stroke_color=TEAL, stroke_width=4.0, fill_color=TEAL, fill_opacity=0.28 + 0.16 * it
            )
            rel_gate = Polygon(
                [3.75, yc - gh, 0], [4.65, yc - gh, 0],
                [4.65, yc + gh, 0], [3.75, yc + gh, 0],
                stroke_color=RED, stroke_width=4.0, fill_color=RED, fill_opacity=0.28 + 0.18 * tt
            )
            g.add(start_gate, rel_gate)

            pol_y = yc + (1.0 - it) * 0.48 + 0.46 * re
            rna_len = 0.25 + 3.4 * jt
            if jt > 0.01:
                rna = _rna_ribbon(px - 0.22 * re, yc + 0.42 * re, rna_len, s=1.02, arch_up=True)
                g.add(rna)
            pol = _pol_body(px + 0.30 * re, pol_y, s=1.00, color=WHITE_POL, fill_op=0.40)
            g.add(pol)

            return g

        world = always_redraw(build_full_journey)
        self.add(world)

        lbl_start_gate = T("START GATE (+1)", size=24, color=TEAL).move_to([-4.35, -1.78, 0])
        lbl_elong = T("template 3'→5' | RNA 5'→3'", size=24, color=GREEN).move_to([0.10, -1.78, 0])
        lbl_rel_gate = T("RELEASE GATE", size=24, color=RED).move_to([4.35, -1.78, 0])
        self.add(lbl_start_gate, lbl_elong, lbl_rel_gate)

        # Beat 1 (0.0 -> 4.8s)
        self.play(
            gates_t.animate.set_value(1.0),
            init_t.animate.set_value(0.35),
            run_time=4.6,
            rate_func=smooth
        )

        # Beat 2 (5.02 -> 8.2s)
        self.at("initiation machinery")
        self.play(
            FadeIn(init_box1),
            FadeIn(init_box2),
            init_t.animate.set_value(0.80),
            run_time=3.2,
            rate_func=smooth
        )

        # Beat 3 (8.40 -> 10.6s)
        self.at("places the enzyme")
        self.play(
            init_t.animate.set_value(1.0),
            journey_t.animate.set_value(0.18),
            run_time=2.2,
            rate_func=smooth
        )

        # Beat 4 (10.82 -> 14.3s)
        self.at("termination signals and factors")
        self.play(
            FadeIn(term_box1),
            term_t.animate.set_value(0.55),
            journey_t.animate.set_value(0.52),
            run_time=3.5,
            rate_func=linear
        )

        # Beat 5 (14.52 -> 17.8s)
        self.at("remodel the elongation complex")
        self.play(
            FadeIn(term_box2),
            term_t.animate.set_value(1.0),
            journey_t.animate.set_value(0.84),
            run_time=3.2,
            rate_func=linear
        )

        # Beat 6 (18.04 -> 22.15s)
        self.at("between them")
        cap = caption("Different teams choose the start and stop; between them, RNA grows 5' → 3'.",
                      size=26, color=GOLD, y=-2.95)
        self.add(cap)
        self.play(
            journey_t.animate.set_value(1.0),
            rel_end.animate.set_value(1.0),
            run_time=3.9,
            rate_func=smooth
        )
        self.finish()


# =============================================================================
# SCENE 14: s14_end (silent: 3.5 s)
# =============================================================================
class S14End(EndCard):
    LINE = "Different initiation teams place polymerase;\ntermination releases RNA and enzyme."
