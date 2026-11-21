# ==============================================================================
# FILM: "When Leak Outruns Lymph" (capillary-exchange-and-lymph__chapter-2)
#
# COLOUR MAP (one colour per concept, constant across the whole film):
#   BLOOD_COL   = RED    (#FC6255) -- blood plasma tint, blood cells, node blood vessel
#   ALBUMIN_COL = GOLD   (#D4A843) -- plasma protein (albumin) dots & hold-back arrows
#   PUSH_COL    = TEXT   (#E8EAF0) -- capillary hydrostatic push arrows & net-out meter
#   FLUID_COL   = BLUE   (#58C4DD) -- water / filtrate drops, 'leak' bar, 'collects' band
#   GLYCO_COL   = GREEN  (#83C167) -- glycocalyx mat lining the capillary lumen
#   LYMPH_COL   = PURPLE (#B88CE8) -- lymph vessels, flaps, valves, lymphangion, node, 'drain' bar
#   GLOB_COL    = TEAL   (#3FB8C0) -- globulins dots & added inward arrow (s13)
#   TISSUE_FILL = "#21283B", TISSUE_EDGE = GREY (#8B93A1) -- tissue band & structural borders
#
# ONE WORLD CARRIED ACROSS ALL SCENES:
#   Top: capillary tube left-to-right ('arterial end' -> 'venous end') lined by GREEN glycocalyx,
#        with RED flowing blood cells, GOLD albumin dots, WHITE outward push arrows, GOLD inward
#        hold-back arrows, and BLUE filtrate drops seeping out along its whole length.
#   Middle: dark 'tissue' band whose height grows/shrinks with computed fluid accumulation.
#   Bottom: PURPLE blind-ended initial lymph vessel -> valved collecting lymphangions ->
#        PURPLE 'lymph node' -> exit arrow 'to neck veins'.
#   Right: two vertical schematic bars ('leak' BLUE, 'drain' PURPLE) driven by Starling balance.
#
# WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
#   s00_link_and_question: Albumin drops from 28 to 3 dots -> Starling hold-back shrinks,
#                          filtration rate (leak_bar) rises, tissue band swells slightly.
#   s02_initial:           Zoomed cross-section of overlapping PURPLE cells; flap angle swings
#                          inward on net inward flow and shuts against outward push.
#   s03_pump:              Lymphangion radius contracts sinusoidally, stepping BLUE drops past
#                          opening/closing valves; muscle bulge & breathing wave boost drain bar.
#   s04_home:              Half of nodal BLUE drops divert into a RED blood vessel; rest exit
#                          along the 'to neck veins' arrow; bars hold level at 8 L/day rate.
#   s05_idea:              Leak bar rises above drain bar -> shaded 'collects' gap grows and
#                          tissue thickness integrates (leak - drain) upward, then resets.
#   s06_routes_push:       Route 1 raises Pc (push arrows grow, leak > drain, swells, resets);
#                          Route 2 lowers plasma protein (albumin/hold-back shrink, swells, resets).
#   s07_routes_leak:       Route 3 opens venular wall gaps (albumin + drops escape, swells, resets);
#                          Route 4 blocks lymph with X (drain bar falls to ~0, drops pile up).
#   s08_predict:           Leak rises above drain -> tissue swells slowly; unnumbered tissue
#                          pressure gauge appears at its resting mark under the question card.
#   s10_safety:            (1) Tissue pressure gauge climbs & push arrows shrink; (2) tissue GOLD
#                          protein washes into lymph & hold-back grows; (3) lymphangion speeds up
#                          & drain bar climbs to meet leak.
#   s11_albumin:           Live Starling net = (Pc - Pi) - sigma * (pi_p - pi_g) drives needle &
#                          readout from 1.0 to 11.8 (pi_p 26->14), then washout to 8.2 (pi_g 6->2).
#   s12_not_harmless:      Meter holds at 8.2 mmHg above 1; all three safety factors act together
#                          to raise drain bar to meet elevated leak bar and hold swelling mild.
#   s13_globulins:         Albumin fades to almost none; TEAL globulins + inward arrow partially
#                          restore hold-back; tissue settles mild, briefly touches resting, returns.
#   s14_close:             Restored steady balance (leak = drain), brief leak rise swells tissue,
#                          then all three safety factors push back to restore level bars.
# ==============================================================================

from bp_parts import *

# ---- Concept palette ----
BLOOD_COL = RED
ALBUMIN_COL = GOLD
PUSH_COL = TEXT
FLUID_COL = BLUE
GLYCO_COL = GREEN
LYMPH_COL = "#B88CE8"
GLOB_COL = TEAL
TISSUE_FILL = "#21283B"
TISSUE_EDGE = GREY

# ---- Lesson Starling model (resting skeletal muscle teaching numbers) ----
SIGMA_BASE = 0.9
PC_MEAN = 18.0
PI_REST = -1.0
PI_P_REST = 26.0
PI_G_REST = 6.0


def starling_net(pc=PC_MEAN, pi=PI_REST, pi_p=PI_P_REST, pi_g=PI_G_REST, sigma=SIGMA_BASE):
    """Net outward pressure in mmHg: (Pc - Pi) - sigma * (pi_p - pi_g)."""
    return (pc - pi) - sigma * (pi_p - pi_g)


class CapillaryWorld:
    """Reusable, animated capillary-tissue-lymph world carried across scenes.

    Every rate, bar height, tissue thickness, and arrow length is driven by ValueTrackers.
    """

    def __init__(
        self,
        x_left=-6.1,
        x_right=3.4,
        bars_x=(4.80, 5.72),
        bars_y0=-1.10,
        bars_max_h=2.55,
        leak_0=0.45,
        drain_0=0.45,
        tissue_h_0=1.65,
        albumin_frac_0=1.0,
        push_scale_0=1.0,
        hold_scale_0=1.0,
        tissue_prot_frac_0=1.0,
        pump_rate_0=1.0,
        show_gauge=False,
        gauge_val_0=0.0,
        gauge_tremble=0.0,
        venular_gaps=False,
        lymph_blocked=False,
        node_rejoin=False,
        globulin_frac_0=0.0,
        seed=7,
    ):
        self.xl = x_left
        self.xr = x_right
        self.w = x_right - x_left
        self.cx = 0.5 * (x_left + x_right)
        self.bars_x = bars_x
        self.bars_y0 = bars_y0
        self.bars_max_h = bars_max_h
        self.rng = np.random.default_rng(seed)

        # Vertical geometry
        self.cap_y = 1.94
        self.cap_h = 0.86
        self.cap_top = self.cap_y + self.cap_h / 2
        self.cap_bot = self.cap_y - self.cap_h / 2

        self.tissue_cy = -0.04
        self.lymph_y = -2.22
        self.lymph_h = 0.54

        # Trackers (time_tr added to self.root so updaters tick every frame!)
        self.leak_tr = ValueTracker(leak_0)
        self.drain_tr = ValueTracker(drain_0)
        self.tissue_h_tr = ValueTracker(tissue_h_0)
        self.albumin_tr = ValueTracker(albumin_frac_0)
        self.push_tr = ValueTracker(push_scale_0)
        self.hold_tr = ValueTracker(hold_scale_0)
        self.tprot_tr = ValueTracker(tissue_prot_frac_0)
        self.pump_tr = ValueTracker(pump_rate_0)
        self.gauge_tr = ValueTracker(gauge_val_0)
        self.gap_tr = ValueTracker(1.0 if venular_gaps else 0.0)
        self.block_tr = ValueTracker(1.0 if lymph_blocked else 0.0)
        self.rejoin_tr = ValueTracker(1.0 if node_rejoin else 0.0)
        self.glob_tr = ValueTracker(globulin_frac_0)
        self.gauge_tremble = gauge_tremble
        self.time_tr = ValueTracker(0.0)
        self.time_tr.add_updater(lambda m, dt: m.increment_value(dt))

        # Section boundaries along x
        self.node_w = 1.28
        self.node_h = 0.80
        self.node_x = self.xr - 1.45
        self.coll_start = self.xl + 0.45 * self.w
        self.coll_end = self.node_x - self.node_w / 2 - 0.05
        self.init_start = self.xl + 0.22
        self.init_end = self.coll_start

        self.root = VGroup()
        self.root.add_updater(lambda m, dt: self.time_tr.increment_value(dt))
        self._build_tissue()
        self._build_capillary()
        self._build_arrows()
        self._build_lymph()
        self._build_particles()
        self._build_bars()
        self.gauge_group = None
        if show_gauge:
            self.add_gauge()

    def _build_tissue(self):
        def mk_tissue():
            h = float(self.tissue_h_tr.get_value())
            return Rectangle(
                width=self.w,
                height=h,
                fill_color=TISSUE_FILL,
                fill_opacity=0.88,
                stroke_color=TISSUE_EDGE,
                stroke_width=2.0,
            ).move_to([self.cx, self.tissue_cy, 0])

        self.tissue_bg = always_redraw(mk_tissue)
        self.tissue_bg.layout_ok = True
        self.tissue_label = T("tissue", size=26, color=TEXT).move_to([self.xl + 0.72, self.tissue_cy, 0])
        self.tissue_label.layout_ok = "contrast"
        self.root.add(self.tissue_bg, self.tissue_label)

    def _build_capillary(self):
        self.blood_fill = Rectangle(
            width=self.w,
            height=self.cap_h,
            fill_color=BLOOD_COL,
            fill_opacity=0.22,
            stroke_width=0,
        ).move_to([self.cx, self.cap_y, 0])
        self.blood_fill.layout_ok = True

        gly_h = 0.08
        self.gly_top = Rectangle(
            width=self.w, height=gly_h, fill_color=GLYCO_COL, fill_opacity=0.55, stroke_width=0
        ).move_to([self.cx, self.cap_top - gly_h / 2, 0])

        def mk_bot_wall():
            gap = float(self.gap_tr.get_value())
            g = VGroup()
            if gap < 0.15:
                gly = Rectangle(
                    width=self.w, height=gly_h, fill_color=GLYCO_COL, fill_opacity=0.55, stroke_width=0
                ).move_to([self.cx, self.cap_bot + gly_h / 2, 0])
                top_line = Line([self.xl, self.cap_top, 0], [self.xr, self.cap_top, 0], color=BLOOD_COL, stroke_width=3)
                bot_line = Line([self.xl, self.cap_bot, 0], [self.xr, self.cap_bot, 0], color=BLOOD_COL, stroke_width=3)
                g.add(gly, top_line, bot_line)
            else:
                top_line = Line([self.xl, self.cap_top, 0], [self.xr, self.cap_top, 0], color=BLOOD_COL, stroke_width=3)
                g.add(top_line)
                split_x = self.xl + 0.64 * self.w
                seg_w = (self.xr - split_x) / 3.0
                gw = 0.22 * gap
                segs = [(self.xl, split_x)]
                cur = split_x
                for _ in range(3):
                    segs.append((cur + gw, cur + seg_w - gw * 0.3))
                    cur += seg_w
                for a, b in segs:
                    if b > a + 0.05:
                        g.add(
                            Rectangle(
                                width=b - a, height=gly_h, fill_color=GLYCO_COL, fill_opacity=0.55, stroke_width=0
                            ).move_to([(a + b) / 2, self.cap_bot + gly_h / 2, 0])
                        )
                        g.add(Line([a, self.cap_bot, 0], [b, self.cap_bot, 0], color=BLOOD_COL, stroke_width=3))
            return g

        self.cap_walls = always_redraw(mk_bot_wall)
        self.cap_walls.layout_ok = True

        self.art_label = T("arterial end", size=24, color=TEXT).move_to([self.xl + 0.92, self.cap_top + 0.26, 0])
        self.ven_label = T("venous end", size=24, color=TEXT).move_to([self.xr - 0.85, self.cap_top + 0.26, 0])
        self.root.add(self.blood_fill, self.gly_top, self.cap_walls, self.art_label, self.ven_label)

    def _build_arrows(self):
        xs = [self.xl + f * self.w for f in (0.14, 0.32, 0.50, 0.68, 0.86)]
        base_push = [0.54, 0.49, 0.45, 0.41, 0.38]

        def mk_arrows():
            ps = float(self.push_tr.get_value())
            hs = float(self.hold_tr.get_value())
            gf = float(self.glob_tr.get_value())
            g = VGroup()
            for x, bp in zip(xs, base_push):
                plen = np.clip(bp * ps, 0.14, 0.80)
                pa = Arrow(
                    [x - 0.10, self.cap_bot + 0.08, 0],
                    [x - 0.10, self.cap_bot + 0.08 - plen, 0],
                    buff=0,
                    color=PUSH_COL,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.32,
                )
                hlen = np.clip(0.30 * hs, 0.08, 0.62)
                ha = Arrow(
                    [x + 0.10, self.cap_bot - hlen + 0.05, 0],
                    [x + 0.10, self.cap_bot + 0.05, 0],
                    buff=0,
                    color=ALBUMIN_COL,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.35,
                )
                g.add(pa, ha)
                if gf > 0.05:
                    glen = 0.19 * gf
                    ga = Arrow(
                        [x + 0.24, self.cap_bot - glen + 0.05, 0],
                        [x + 0.24, self.cap_bot + 0.05, 0],
                        buff=0,
                        color=GLOB_COL,
                        stroke_width=3.5,
                        max_tip_length_to_length_ratio=0.38,
                    )
                    g.add(ga)
            return g

        self.arrows = always_redraw(mk_arrows)
        self.arrows.layout_ok = True
        self.root.add(self.arrows)

    def _build_lymph(self):
        y = self.lymph_y
        h = self.lymph_h
        r = h / 2

        def mk_lymph():
            t = float(self.time_tr.get_value())
            pr = float(self.pump_tr.get_value())
            blk = float(self.block_tr.get_value())
            rej = float(self.rejoin_tr.get_value())
            g = VGroup()

            init_len = self.coll_start - self.init_start
            cap_arc = Arc(radius=r, start_angle=PI / 2, angle=PI, arc_center=[self.init_start + r, y, 0],
                          color=LYMPH_COL, stroke_width=3.5)
            init_fill = RoundedRectangle(
                corner_radius=r, width=init_len, height=h, fill_color=LYMPH_COL, fill_opacity=0.18, stroke_width=0
            ).move_to([(self.init_start + self.coll_start) / 2, y, 0])
            bot_init = Line([self.init_start + r, y - r, 0], [self.coll_start, y - r, 0], color=LYMPH_COL, stroke_width=3.5)
            top_init = VGroup()
            n_flaps = 4
            dx = (self.coll_start - (self.init_start + r)) / n_flaps
            for k in range(n_flaps):
                fx0 = self.init_start + r + k * dx
                fx1 = fx0 + dx
                top_init.add(Line([fx0, y + r, 0], [fx1 - 0.14, y + r, 0], color=LYMPH_COL, stroke_width=3.5))
                flap_swing = 0.08 * (0.5 + 0.5 * np.sin(2.5 * t + k))
                top_init.add(Line([fx1 - 0.16, y + r - flap_swing, 0], [fx1 + 0.02, y + r + 0.04, 0],
                                  color=LYMPH_COL, stroke_width=3))
            g.add(init_fill, cap_arc, bot_init, top_init)

            n_seg = 3
            seg_w = (self.coll_end - self.coll_start) / n_seg
            for s in range(n_seg):
                sx0 = self.coll_start + s * seg_w
                sx1 = sx0 + seg_w
                phase = 2.8 * pr * t - s * 1.4
                squeeze = 0.24 * max(0.0, np.sin(phase)) if blk < 0.5 else 0.0
                sh = h * (1.0 - squeeze)
                sr = sh / 2
                seg_fill = Rectangle(width=seg_w, height=sh, fill_color=LYMPH_COL, fill_opacity=0.22, stroke_width=0
                                     ).move_to([(sx0 + sx1) / 2, y, 0])
                seg_top = Line([sx0, y + sr, 0], [sx1, y + sr, 0], color=LYMPH_COL, stroke_width=3.5)
                seg_bot = Line([sx0, y - sr, 0], [sx1, y - sr, 0], color=LYMPH_COL, stroke_width=3.5)
                g.add(seg_fill, seg_top, seg_bot)
                open_amt = 0.45 * max(0.0, np.sin(phase - 0.8)) if blk < 0.5 else 0.0
                tip_y = r * (0.15 + 0.55 * open_amt)
                g.add(
                    Line([sx0 - 0.02, y + r * 0.9, 0], [sx0 + 0.15, y + tip_y, 0], color=LYMPH_COL, stroke_width=3),
                    Line([sx0 - 0.02, y - r * 0.9, 0], [sx0 + 0.15, y - tip_y, 0], color=LYMPH_COL, stroke_width=3),
                )
            g.add(
                Line([self.coll_end - 0.02, y + r * 0.9, 0], [self.coll_end + 0.15, y + r * 0.2, 0], color=LYMPH_COL, stroke_width=3),
                Line([self.coll_end - 0.02, y - r * 0.9, 0], [self.coll_end + 0.15, y - r * 0.2, 0], color=LYMPH_COL, stroke_width=3),
            )

            node = Ellipse(
                width=self.node_w, height=self.node_h, color=LYMPH_COL, stroke_width=3.5,
                fill_color=LYMPH_COL, fill_opacity=0.24
            ).move_to([self.node_x, y, 0])
            g.add(node)

            if rej > 0.2:
                bv = ArcBetweenPoints(
                    [self.node_x - 0.15, y + self.node_h * 0.35, 0],
                    [self.node_x + 0.85, y + self.node_h * 0.65, 0],
                    angle=-0.45,
                    color=BLOOD_COL,
                    stroke_width=4.5,
                ).set_opacity(rej)
                g.add(bv)

            ex_x0 = self.node_x + self.node_w / 2
            ex_x1 = max(self.xr + 0.8, self.node_x + 2.8)
            ex_arr = Arrow(
                [ex_x0, y, 0], [ex_x1, y, 0], buff=0, color=LYMPH_COL, stroke_width=5,
                max_tip_length_to_length_ratio=0.14
            )
            g.add(ex_arr)

            if blk > 0.2:
                bx = self.coll_end - 0.15
                x1 = Line([bx - 0.24, y - 0.32, 0], [bx + 0.24, y + 0.32, 0], color=BLOOD_COL, stroke_width=6)
                x2 = Line([bx - 0.24, y + 0.32, 0], [bx + 0.24, y - 0.32, 0], color=BLOOD_COL, stroke_width=6)
                g.add(x1, x2)
            return g

        self.lymph_geom = always_redraw(mk_lymph)
        self.lymph_geom.layout_ok = True
        self.node_label = T("lymph node", size=24, color=LYMPH_COL).move_to([self.node_x, y - self.node_h / 2 - 0.34, 0])
        neck_x = max(self.node_x + self.node_w / 2 + 1.55, 4.35)
        self.neck_label = T("to neck veins", size=24, color=LYMPH_COL).move_to([neck_x, y - 0.42, 0])
        self.root.add(self.lymph_geom, self.node_label, self.neck_label)

    def _build_particles(self):
        n_rbc = 16
        rbc_x = self.rng.uniform(0.0, 1.0, n_rbc)
        rbc_y = self.rng.uniform(-0.24, 0.24, n_rbc)

        n_alb = 28
        alb_x = self.rng.uniform(0.0, 1.0, n_alb)
        alb_y = self.rng.uniform(-0.28, 0.28, n_alb)

        n_glob = 10
        glob_x = self.rng.uniform(0.0, 1.0, n_glob)
        glob_y = self.rng.uniform(-0.26, 0.26, n_glob)

        n_drops = 26
        drop_u = self.rng.uniform(0.0, 1.0, n_drops)
        drop_v = self.rng.uniform(0.0, 1.0, n_drops)

        n_tp = 8
        tp_u = np.linspace(0.24, 0.92, n_tp)
        tp_v = self.rng.uniform(0.15, 0.55, n_tp)

        n_ld = 10
        ld_u = np.linspace(0.02, 0.95, n_ld)

        def mk_parts():
            t = float(self.time_tr.get_value())
            lk = float(self.leak_tr.get_value())
            pr = float(self.pump_tr.get_value())
            af = float(self.albumin_tr.get_value())
            gf = float(self.glob_tr.get_value())
            tf = float(self.tprot_tr.get_value())
            gap = float(self.gap_tr.get_value())
            blk = float(self.block_tr.get_value())
            rej = float(self.rejoin_tr.get_value())
            th = float(self.tissue_h_tr.get_value())

            g = VGroup()
            for i in range(n_rbc):
                px = self.xl + 0.15 + ((rbc_x[i] + 0.14 * t) % 1.0) * (self.w - 0.3)
                py = self.cap_y + rbc_y[i]
                g.add(Dot([px, py, 0], radius=0.065, color=BLOOD_COL).set_opacity(0.78))

            n_show_alb = int(round(af * n_alb))
            for i in range(n_show_alb):
                px = self.xl + 0.15 + ((alb_x[i] + 0.11 * t) % 1.0) * (self.w - 0.3)
                py = self.cap_y + alb_y[i]
                if gap > 0.3 and i % 4 == 0 and px > self.xl + 0.64 * self.w:
                    py -= 0.45 * ((0.6 * t + i * 0.2) % 1.0)
                g.add(Dot([px, py, 0], radius=0.048, color=ALBUMIN_COL))

            if gf > 0.05:
                n_show_glob = int(round(gf * n_glob))
                for i in range(n_show_glob):
                    px = self.xl + 0.15 + ((glob_x[i] + 0.11 * t) % 1.0) * (self.w - 0.3)
                    py = self.cap_y + glob_y[i]
                    g.add(Dot([px, py, 0], radius=0.052, color=GLOB_COL))

            n_show_tp = int(round(tf * n_tp))
            y_top = self.cap_bot - 0.14
            y_bot = self.lymph_y + self.lymph_h / 2
            for i in range(n_tp):
                if i < n_show_tp:
                    px = self.xl + tp_u[i] * self.w
                    py = y_top - tp_v[i] * (y_top - y_bot) * 0.55
                    g.add(Dot([px, py, 0], radius=0.045, color=ALBUMIN_COL).set_opacity(0.85))
                elif tf > 0.05:
                    px = self.xl + tp_u[i] * self.w
                    py = y_top - (0.55 + 0.45 * (1.0 - tf)) * (y_top - y_bot)
                    g.add(Dot([px, py, 0], radius=0.045, color=ALBUMIN_COL).set_opacity(0.5))

            n_active = int(np.clip(round(12 + 18 * lk), 8, n_drops))
            speed = 0.16 + 0.38 * lk
            x_min_d = self.xl + 2.25  # clear of 'tissue' label & 'tissue pressure' gauge/text at left
            for i in range(n_active):
                u = drop_u[i]
                px = x_min_d + u * (self.xr - 0.25 - x_min_d)
                phase = (drop_v[i] + speed * t) % 1.0
                if blk > 0.5 and i % 2 == 0:
                    py = self.tissue_cy + (drop_v[i] - 0.5) * (th * 0.70)
                else:
                    py = self.cap_bot - 0.05 - phase * (self.cap_bot - 0.05 - (self.lymph_y + 0.1))
                g.add(Dot([px, py, 0], radius=0.052, color=FLUID_COL).set_opacity(0.92))

            if blk < 0.5:
                l_speed = 0.16 * pr
                ex_end = max(self.xr + 0.65, self.node_x + 2.6)
                for i in range(n_ld):
                    lu = (ld_u[i] + l_speed * t) % 1.0
                    px = self.init_start + 0.25 + lu * (ex_end - self.init_start - 0.25)
                    py = self.lymph_y
                    if rej > 0.2 and i % 2 == 1 and px > self.node_x - 0.1 and px < self.node_x + 0.95:
                        frac = (px - (self.node_x - 0.1)) / 1.05
                        py = self.lymph_y + frac * 0.58
                    g.add(Dot([px, py, 0], radius=0.055, color=FLUID_COL))
            return g

        self.particles = always_redraw(mk_parts)
        self.particles.layout_ok = True
        self.root.add(self.particles)

    def _build_bars(self):
        lx, dx = self.bars_x
        bar_w = 0.48
        bar_max_h = self.bars_max_h
        bar_y0 = self.bars_y0

        def mk_bars():
            lv = float(np.clip(self.leak_tr.get_value(), 0.03, 1.0))
            dv = float(np.clip(self.drain_tr.get_value(), 0.03, 1.0))
            lh = lv * bar_max_h
            dh = dv * bar_max_h
            l_track = Rectangle(width=bar_w, height=bar_max_h, stroke_color=GREY, stroke_width=2, fill_opacity=0
                                ).move_to([lx, bar_y0 + bar_max_h / 2, 0])
            d_track = Rectangle(width=bar_w, height=bar_max_h, stroke_color=GREY, stroke_width=2, fill_opacity=0
                                ).move_to([dx, bar_y0 + bar_max_h / 2, 0])
            l_fill = Rectangle(width=bar_w, height=lh, fill_color=FLUID_COL, fill_opacity=0.85, stroke_width=0
                               ).move_to([lx, bar_y0 + lh / 2, 0])
            d_fill = Rectangle(width=bar_w, height=dh, fill_color=LYMPH_COL, fill_opacity=0.85, stroke_width=0
                               ).move_to([dx, bar_y0 + dh / 2, 0])
            return VGroup(l_fill, d_fill, l_track, d_track)

        self.bars_geom = always_redraw(mk_bars)
        self.bars_geom.layout_ok = True
        self.leak_label = T("leak", size=24, color=FLUID_COL).move_to([lx, bar_y0 - 0.28, 0])
        self.drain_label = T("drain", size=24, color=LYMPH_COL).move_to([dx, bar_y0 - 0.28, 0])
        self.root.add(self.bars_geom, self.leak_label, self.drain_label)

    def add_gauge(self, center=None):
        """Add unnumbered 'tissue pressure' gauge inside left side of tissue band (clear of borders)."""
        if center is None:
            center = [self.xl + 1.18, self.tissue_cy - 0.06, 0]
        self.tissue_label.move_to([self.xl + 1.18, self.tissue_cy + 0.50, 0])
        c = np.array(center, dtype=float)
        rad = 0.34

        def mk_g():
            t = float(self.time_tr.get_value())
            v = float(np.clip(self.gauge_tr.get_value(), 0.0, 1.0))
            jitter = self.gauge_tremble * np.sin(14.0 * t)
            ang = PI / 2 - 0.95 * v + jitter
            back = Circle(radius=rad, color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to(c)
            arc = Arc(radius=rad * 0.8, start_angle=PI * 0.85, angle=-PI * 0.7, arc_center=c,
                      color=GREY, stroke_width=3)
            rest_tick = Line(c + UP * rad * 0.65, c + UP * rad * 0.95, color=ALBUMIN_COL, stroke_width=3)
            needle = Line(c, c + rad * 0.75 * np.array([np.cos(ang), np.sin(ang), 0]), color=PUSH_COL, stroke_width=4)
            hub = Dot(c, radius=0.04, color=PUSH_COL)
            return VGroup(back, arc, rest_tick, needle, hub)

        self.gauge_mob = always_redraw(mk_g)
        self.gauge_mob.layout_ok = True
        self.gauge_label = T("tissue pressure", size=22, color=TEXT).move_to([c[0], c[1] - rad - 0.20, 0])
        self.gauge_label.layout_ok = "contrast"
        self.gauge_group = VGroup(self.gauge_mob, self.gauge_label)
        self.root.add(self.gauge_group)
        return self.gauge_group


# ==============================================================================
# SCENES
# ==============================================================================

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        w = CapillaryWorld()
        self.add(w.root, scope_tag("schematic", color=TEXT))

        self.at("slows the leak")
        self.play(w.hold_tr.animate.set_value(1.15), run_time=0.45, rate_func=there_and_back)

        self.at("albumin supplies")
        alb_glow = SurroundingRectangle(
            Rectangle(width=w.w - 0.4, height=w.cap_h - 0.1).move_to([w.cx, w.cap_y, 0]),
            color=ALBUMIN_COL,
            stroke_width=3,
            buff=0.04,
        )
        alb_glow.layout_ok = True
        self.play(FadeIn(alb_glow), run_time=0.4)
        self.play(FadeOut(alb_glow), run_time=0.45)

        self.at("almost none")
        no_alb = T("almost no albumin", size=26, color=ALBUMIN_COL).move_to([-1.3, w.cap_top + 0.30, 0])
        self.play(
            w.albumin_tr.animate.set_value(0.11),
            w.hold_tr.animate.set_value(0.35),
            FadeIn(no_alb),
            run_time=0.40,
        )

        self.at("usually swell")
        self.play(
            w.leak_tr.animate.set_value(0.70),
            w.tissue_h_tr.animate.set_value(1.92),
            run_time=1.2,
        )

        self.at("what protects them")
        q_top = T("What protects them?", size=38, color=TEXT, weight=BOLD).move_to([0, HEAD_Y, 0])
        self.play(FadeIn(q_top, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = CapillaryWorld(leak_0=0.70, tissue_h_0=1.92, albumin_frac_0=0.11, hold_scale_0=0.35)
        no_alb = T("almost no albumin", size=26, color=ALBUMIN_COL).move_to([-1.3, w.cap_top + 0.30, 0])
        q_top = T("What protects them?", size=38, color=TEXT, weight=BOLD).move_to([0, HEAD_Y, 0])
        self.add(w.root, no_alb, q_top, scope_tag("schematic", color=TEXT))

        title = T("When Leak Outruns Lymph", size=42, font=TITLE_FONT, color=TEXT).move_to([0, HEAD_Y, 0])
        self.play(
            FadeOut(q_top),
            FadeOut(no_alb),
            w.albumin_tr.animate.set_value(1.0),
            w.hold_tr.animate.set_value(1.0),
            w.leak_tr.animate.set_value(0.45),
            w.tissue_h_tr.animate.set_value(1.65),
            run_time=0.45,
        )
        self.play(FadeIn(title), run_time=0.45)
        self.wait(0.7)
        self.play(FadeOut(title), run_time=0.35)
        self.finish()


class S02Initial(SpokenScene):
    def construct(self):
        w = CapillaryWorld()
        tag = scope_tag("schematic", color=TEXT)
        self.add(w.root, tag)

        self.at("blind")
        blind_ring = Circle(radius=0.42, color=LYMPH_COL, stroke_width=4).move_to([w.init_start + 0.27, w.lymph_y, 0])
        blind_ring.layout_ok = True
        blind_lab = T("blind end", size=26, color=LYMPH_COL).next_to(blind_ring, DOWN, buff=0.18)
        self.play(Create(blind_ring), FadeIn(blind_lab), run_time=0.5)

        self.at("overlapping cells")
        flap_ang = ValueTracker(0.0)
        zoom_t = ValueTracker(0.0)
        zoom_t.add_updater(lambda m, dt: m.increment_value(dt))

        def mk_zoom():
            ang = float(flap_ang.get_value())
            t = float(zoom_t.get_value())
            g = VGroup()
            lumen_bg = Rectangle(width=10.6, height=2.0, fill_color=LYMPH_COL, fill_opacity=0.14, stroke_width=0
                                 ).move_to([0, -0.6, 0])
            bot_wall = Line([-5.3, -1.6, 0], [5.3, -1.6, 0], color=LYMPH_COL, stroke_width=5)
            cell_l = RoundedRectangle(corner_radius=0.14, width=3.4, height=0.42, color=LYMPH_COL, stroke_width=4,
                                      fill_color=LYMPH_COL, fill_opacity=0.28).move_to([-3.5, 0.55, 0])
            cell_r = RoundedRectangle(corner_radius=0.14, width=3.4, height=0.42, color=LYMPH_COL, stroke_width=4,
                                      fill_color=LYMPH_COL, fill_opacity=0.28).move_to([3.5, 0.55, 0])
            cell_mid = RoundedRectangle(corner_radius=0.14, width=3.0, height=0.42, color=LYMPH_COL, stroke_width=4,
                                        fill_color=LYMPH_COL, fill_opacity=0.28).move_to([0, 0.74, 0])
            p_l = np.array([-1.85, 0.50, 0])
            flap_l = Line(p_l, p_l + 1.05 * np.array([np.cos(ang), np.sin(ang), 0]), color=LYMPH_COL, stroke_width=7)
            p_r = np.array([1.85, 0.50, 0])
            flap_r = Line(p_r, p_r + 1.05 * np.array([-np.cos(ang), np.sin(ang), 0]), color=LYMPH_COL, stroke_width=7)
            g.add(lumen_bg, bot_wall, cell_l, cell_r, cell_mid, flap_l, flap_r)

            rng = np.random.default_rng(7)
            xs_d = rng.uniform(-1.0, 1.0, 8)
            for k, dx in enumerate(xs_d):
                if ang < -0.18:
                    side = -1.65 if k % 2 == 0 else 1.65
                    phase = (0.9 * t + k * 0.25) % 1.0
                    py = 1.75 - phase * 2.4
                    px = side + 0.08 * dx
                    g.add(Dot([px, py, 0], radius=0.09, color=FLUID_COL))
                else:
                    px = dx * 2.6
                    py = -0.85 + 0.25 * np.sin(3.5 * t + k)
                    g.add(Dot([px, py, 0], radius=0.09, color=FLUID_COL))
            return g

        zoom_view = always_redraw(mk_zoom)
        zoom_view.layout_ok = True
        flaps_lab = T("flaps", size=30, color=LYMPH_COL).move_to([0.0, 0.05, 0])
        tiss_tag = T("tissue", size=26, color=TEXT).move_to([-4.6, 1.85, 0])
        lymp_tag = T("initial lymph vessel", size=26, color=LYMPH_COL).move_to([-3.6, -2.0, 0])
        zoom_group = VGroup(zoom_view, flaps_lab, tiss_tag, lymp_tag)

        self.play(FadeOut(w.root), FadeOut(blind_ring), FadeOut(blind_lab), run_time=0.45)
        self.add(zoom_t)
        self.play(FadeIn(zoom_group), run_time=0.5)

        self.at("let fluid in")
        self.play(flap_ang.animate.set_value(-0.62), run_time=0.6)

        self.at("not out")
        self.play(flap_ang.animate.set_value(0.0), run_time=0.45)
        self.wait(0.25)

        self.play(FadeOut(zoom_group), run_time=0.4)
        self.remove(zoom_t)
        self.play(FadeIn(w.root), run_time=0.4)
        self.finish()


class S03Pump(SpokenScene):
    def construct(self):
        w = CapillaryWorld(drain_0=0.38, pump_rate_0=0.8)
        self.add(w.root, scope_tag("schematic", color=TEXT))

        self.at("each segment between two valves")
        seg_w = (w.coll_end - w.coll_start) / 3.0
        sx0 = w.coll_start + seg_w
        seg_box = RoundedRectangle(
            corner_radius=0.08, width=seg_w - 0.06, height=w.lymph_h + 0.16, color=ALBUMIN_COL, stroke_width=3.5
        ).move_to([sx0 + seg_w / 2, w.lymph_y, 0])
        seg_box.layout_ok = True
        # Place 'lymphangion' ABOVE the vessel so 'muscle' below never touches it
        seg_lab = T("lymphangion", size=24, color=LYMPH_COL).move_to([sx0 + seg_w / 2, w.lymph_y + 0.62, 0])
        self.play(Create(seg_box), FadeIn(seg_lab), run_time=0.6)

        self.at("contracts as a pump")
        self.play(w.pump_tr.animate.set_value(1.55), run_time=0.7)

        self.at("squeezing from nearby muscle")
        muscle_pos = [w.coll_start + seg_w * 0.45, w.lymph_y - 0.68, 0]
        muscle = RoundedRectangle(
            corner_radius=0.18, width=1.8, height=0.36, color=BLOOD_COL, stroke_width=2.5,
            fill_color=BLOOD_COL, fill_opacity=0.22
        ).move_to(muscle_pos)
        muscle.layout_ok = True
        m_lab = T("muscle", size=24, color=BLOOD_COL).next_to(muscle, DOWN, buff=0.10)
        self.play(FadeIn(muscle), FadeIn(m_lab), run_time=0.4)
        self.play(muscle.animate.shift(UP * 0.24).stretch(1.20, 1), run_time=0.45, rate_func=there_and_back)

        self.at("from breathing")
        wave = Rectangle(width=1.0, height=1.1, fill_color=TEXT, fill_opacity=0.14, stroke_width=0
                         ).move_to([w.coll_start - 0.2, w.lymph_y + 0.1, 0])
        wave.layout_ok = True
        b_lab = T("breathing", size=24, color=TEXT).move_to([w.coll_start - 1.1, w.lymph_y + 0.62, 0])
        b_lab.layout_ok = "contrast"
        self.play(
            FadeIn(wave),
            FadeIn(b_lab),
            w.drain_tr.animate.set_value(0.45),
            w.pump_tr.animate.set_value(1.25),
            run_time=0.5,
        )
        self.play(wave.animate.shift(RIGHT * 2.1), run_time=1.1, rate_func=linear)
        self.play(FadeOut(wave), FadeOut(b_lab), FadeOut(muscle), FadeOut(m_lab), FadeOut(seg_box), FadeOut(seg_lab), run_time=0.45)
        self.finish()


class S04Home(SpokenScene):
    def construct(self):
        w = CapillaryWorld(pump_rate_0=1.1)
        self.add(w.root, scope_tag("schematic", color=TEXT))

        self.at("daily filtration")
        daily_lab = T("about 8 L a day (reviews)", size=24, color=FLUID_COL).move_to([-1.2, w.cap_top + 0.30, 0])
        self.play(FadeIn(daily_lab), run_time=0.5)

        self.at("rejoin the blood")
        node_glow = Ellipse(
            width=w.node_w + 0.18, height=w.node_h + 0.18, color=ALBUMIN_COL, stroke_width=4
        ).move_to([w.node_x, w.lymph_y, 0])
        node_glow.layout_ok = True
        est_lab = T("estimate, mainly animal studies", size=22, color=TEXT).move_to(
            [-1.3, w.lymph_y - 0.92, 0]
        )
        self.play(w.rejoin_tr.animate.set_value(1.0), Create(node_glow), FadeIn(est_lab), run_time=0.7)

        self.at("base of the neck")
        neck_hi = SurroundingRectangle(w.neck_label, color=LYMPH_COL, stroke_width=2.5, buff=0.08)
        self.play(FadeOut(node_glow), Create(neck_hi), run_time=0.5)
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        w = CapillaryWorld(x_left=-6.2, x_right=1.6, bars_x=(2.8, 4.1))
        self.add(w.root, scope_tag("schematic", color=TEXT))

        lx, dx = 2.8, 4.1
        bar_w = 0.72
        max_h = 3.1
        y0 = -1.22

        def mk_big_bars():
            lv = float(np.clip(w.leak_tr.get_value(), 0.03, 1.0))
            dv = float(np.clip(w.drain_tr.get_value(), 0.03, 1.0))
            lh, dh = lv * max_h, dv * max_h
            g = VGroup()
            g.add(
                Rectangle(width=bar_w, height=lh, fill_color=FLUID_COL, fill_opacity=0.85, stroke_width=0).move_to([lx, y0 + lh / 2, 0]),
                Rectangle(width=bar_w, height=dh, fill_color=LYMPH_COL, fill_opacity=0.85, stroke_width=0).move_to([dx, y0 + dh / 2, 0]),
                Rectangle(width=bar_w, height=max_h, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([lx, y0 + max_h / 2, 0]),
                Rectangle(width=bar_w, height=max_h, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([dx, y0 + max_h / 2, 0]),
            )
            if lv > dv + 0.05:
                gap_h = (lv - dv) * max_h
                gap_y = y0 + dh + gap_h / 2
                # Shade the gap cleanly above the drain bar without overlapping either track border
                g.add(
                    Rectangle(width=bar_w - 0.04, height=gap_h, fill_color=FLUID_COL, fill_opacity=0.35,
                              stroke_color=FLUID_COL, stroke_width=2).move_to([dx, gap_y, 0]),
                    DashedLine([lx + bar_w / 2, y0 + lh, 0], [dx + bar_w / 2, y0 + lh, 0], color=FLUID_COL, stroke_width=2.5),
                )
            return g

        big_bars = always_redraw(mk_big_bars)
        big_bars.layout_ok = True
        big_l_lab = T("leak", size=28, color=FLUID_COL).move_to([lx, y0 - 0.34, 0])
        big_d_lab = T("drain", size=28, color=LYMPH_COL).move_to([dx, y0 - 0.34, 0])

        self.at("one idea")
        self.play(FadeOut(w.bars_geom), FadeOut(w.leak_label), FadeOut(w.drain_label), run_time=0.25)
        self.play(FadeIn(big_bars), FadeIn(big_l_lab), FadeIn(big_d_lab), run_time=0.35)

        self.at("filtration outrunning lymph")
        collects_lab = T("collects", size=26, color=FLUID_COL).move_to([dx + bar_w / 2 + 0.88, y0 + 0.65 * max_h, 0])
        edema_lab = T("edema", size=30, color=FLUID_COL, weight=BOLD).move_to([-2.2, w.tissue_cy, 0])
        edema_lab.layout_ok = "contrast"
        self.play(
            w.leak_tr.animate.set_value(0.84),
            w.tissue_h_tr.animate.set_value(2.35),
            FadeIn(collects_lab),
            FadeIn(edema_lab),
            run_time=1.3,
        )

        self.at("more leaves the capillaries")
        self.wait(1.6)

        rule = T("edema = leak beats drain", size=36, color=TEXT, weight=BOLD).move_to([0, HEAD_Y, 0])
        self.play(
            w.leak_tr.animate.set_value(0.45),
            w.tissue_h_tr.animate.set_value(1.65),
            FadeOut(collects_lab),
            FadeOut(edema_lab),
            FadeIn(rule),
            run_time=0.85,
        )
        self.finish()


def _route_slots(filled_texts=()):
    """Build the 4 numbered route slots across the top band."""
    cols = [PUSH_COL, ALBUMIN_COL, BLOOD_COL, LYMPH_COL]
    xs = [-4.6, -1.55, 1.55, 4.6]
    slots = VGroup()
    for idx in range(4):
        txt = filled_texts[idx] if idx < len(filled_texts) else f"{idx + 1}. ..."
        col = cols[idx] if idx < len(filled_texts) else GREY
        b = boxed_label(txt, color=col, size=24, box=(2.75, 0.56))
        b.move_to([xs[idx], HEAD_Y, 0])
        slots.add(b)
    return slots


class S06RoutesPush(SpokenScene):
    def construct(self):
        w = CapillaryWorld()
        self.add(w.root, scope_tag("schematic", color=TEXT))

        slots = _route_slots()
        self.at("four ways")
        self.play(FadeIn(slots), run_time=0.6)

        self.at("raise capillary pressure")
        self.play(
            w.push_tr.animate.set_value(1.65),
            w.leak_tr.animate.set_value(0.84),
            w.tissue_h_tr.animate.set_value(2.30),
            run_time=1.2,
        )
        self.at("the push grows")
        s1_new = boxed_label("1. pressure up", color=PUSH_COL, size=24, box=(2.75, 0.56)).move_to(slots[0].get_center())
        self.play(swap(slots[0], s1_new, run_time=0.45))
        slots.submobjects[0] = s1_new

        self.play(
            w.push_tr.animate.set_value(1.0),
            w.leak_tr.animate.set_value(0.45),
            w.tissue_h_tr.animate.set_value(1.65),
            run_time=0.55,
        )

        self.at("lower plasma protein")
        self.play(
            w.albumin_tr.animate.set_value(0.28),
            w.hold_tr.animate.set_value(0.32),
            w.leak_tr.animate.set_value(0.82),
            w.tissue_h_tr.animate.set_value(2.26),
            run_time=1.1,
        )
        self.at("the holdback shrinks")
        s2_new = boxed_label("2. protein down", color=ALBUMIN_COL, size=24, box=(2.75, 0.56)).move_to(slots[1].get_center())
        self.play(swap(slots[1], s2_new, run_time=0.45))
        slots.submobjects[1] = s2_new

        self.play(
            w.albumin_tr.animate.set_value(1.0),
            w.hold_tr.animate.set_value(1.0),
            w.leak_tr.animate.set_value(0.45),
            w.tissue_h_tr.animate.set_value(1.65),
            run_time=0.5,
        )
        self.finish()


class S07RoutesLeak(SpokenScene):
    def construct(self):
        w = CapillaryWorld()
        slots = _route_slots(("1. pressure up", "2. protein down"))
        self.add(w.root, slots, scope_tag("schematic", color=TEXT))

        self.at("leaky")
        self.play(w.gap_tr.animate.set_value(1.0), run_time=0.6)

        self.at("protein escapes")
        self.play(
            w.hold_tr.animate.set_value(0.34),
            w.leak_tr.animate.set_value(0.84),
            w.tissue_h_tr.animate.set_value(2.30),
            run_time=1.2,
        )
        s3_new = boxed_label("3. leaky wall", color=BLOOD_COL, size=24, box=(2.75, 0.56)).move_to(slots[2].get_center())
        self.play(swap(slots[2], s3_new, run_time=0.45))
        slots.submobjects[2] = s3_new

        self.play(
            w.gap_tr.animate.set_value(0.0),
            w.hold_tr.animate.set_value(1.0),
            w.leak_tr.animate.set_value(0.45),
            w.tissue_h_tr.animate.set_value(1.65),
            run_time=0.6,
        )

        self.at("or block the lymph")
        self.play(
            w.block_tr.animate.set_value(1.0),
            w.drain_tr.animate.set_value(0.06),
            w.tissue_h_tr.animate.set_value(2.32),
            run_time=1.2,
        )
        self.at("drainage fails")
        s4_new = boxed_label("4. drain blocked", color=LYMPH_COL, size=24, box=(2.75, 0.56)).move_to(slots[3].get_center())
        self.play(swap(slots[3], s4_new, run_time=0.45))
        slots.submobjects[3] = s4_new

        self.play(
            w.block_tr.animate.set_value(0.0),
            w.drain_tr.animate.set_value(0.45),
            w.tissue_h_tr.animate.set_value(1.65),
            run_time=0.55,
        )
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        w = CapillaryWorld()
        slots = _route_slots(("1. pressure up", "2. protein down", "3. leaky wall", "4. drain blocked"))
        self.add(w.root, slots, scope_tag("schematic", color=TEXT))

        self.at("filtration outruns lymph")
        self.play(
            FadeOut(slots),
            w.leak_tr.animate.set_value(0.65),
            w.tissue_h_tr.animate.set_value(2.00),
            run_time=1.2,
        )

        self.at("collect in the tissue")
        g_mob = w.add_gauge()
        self.play(FadeIn(g_mob), run_time=0.6)

        self.at("which way does tissue pressure")
        q = question_card("Tissue pressure: up or down?", y=HEAD_Y, color=TEXT, size=34, max_w=10.5)
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Tissue pressure: up or down?"
    CARD = {"y": HEAD_Y, "color": TEXT, "size": 34, "max_w": 10.5}
    RING_AT = (6.0, -3.02, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = CapillaryWorld(leak_0=0.65, tissue_h_0=2.00, show_gauge=True, gauge_tremble=0.05)
        w.root.add_updater(lambda m, dt: w.tissue_h_tr.set_value(min(2.22, w.tissue_h_tr.get_value() + 0.045 * dt)))
        return w.root


def _safety_list(x_center=5.12, lit=False):
    """Build the 3 safety-factor labels stacked neatly at top right (s10..s13), clear of bars and frame edge."""
    ys = [2.98, 2.40, 1.82]
    cols = [PUSH_COL, ALBUMIN_COL, LYMPH_COL]
    texts = ["1 tissue pressure up", "2 washout", "3 lymph up"]
    items = VGroup()
    for t, y, col in zip(texts, ys, cols):
        b = boxed_label(
            t,
            color=col,
            size=24,
            box=(2.46, 0.44),
            stroke=3.5 if lit else 2.0,
            fill_opacity=0.28 if lit else 0.14,
        ).move_to([x_center, y, 0])
        items.add(b)
    return items


class S10Safety(SpokenScene):
    def construct(self):
        w = CapillaryWorld(
            x_left=-6.2,
            x_right=1.65,
            bars_x=(4.70, 5.62),
            bars_y0=-1.18,
            bars_max_h=2.08,
            leak_0=0.65,
            tissue_h_0=2.20,
            show_gauge=True,
        )
        q = question_card("Tissue pressure: up or down?", y=HEAD_Y, color=TEXT, size=34, max_w=10.5)
        self.add(w.root, q, scope_tag("schematic", color=TEXT))

        s_list = _safety_list(x_center=5.12, lit=False)

        self.play(FadeOut(q), w.gauge_tr.animate.set_value(0.85), run_time=0.9)

        self.at("the push shrinks")
        self.play(w.push_tr.animate.set_value(0.72), FadeIn(s_list[0]), run_time=0.8)

        self.at("rinses protein out")
        self.play(w.tprot_tr.animate.set_value(0.15), run_time=1.3)

        self.at("strengthens the holdback")
        self.play(w.hold_tr.animate.set_value(1.22), FadeIn(s_list[1]), run_time=0.9)

        self.at("lymph flow itself rises")
        self.play(
            w.pump_tr.animate.set_value(1.85),
            w.drain_tr.animate.set_value(0.58),
            w.leak_tr.animate.set_value(0.58),
            FadeIn(s_list[2]),
            run_time=1.2,
        )
        self.finish()


def _net_out_meter(pi_p_tr, pi_g_tr, center=(2.78, 1.98, 0)):
    """Half-circle 'net out' pressure meter computed directly from pi_p and pi_g."""
    c = np.array(center, dtype=float)
    rad = 0.62
    track = Arc(radius=rad, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=7)
    ref_ang = PI - PI * (1.0 / 15.0)
    ref_tick = Line(
        c + rad * 0.85 * np.array([np.cos(ref_ang), np.sin(ref_ang), 0]),
        c + rad * 1.12 * np.array([np.cos(ref_ang), np.sin(ref_ang), 0]),
        color=ALBUMIN_COL,
        stroke_width=3.5,
    )

    def net_val():
        return float(np.clip(starling_net(pi_p=pi_p_tr.get_value(), pi_g=pi_g_tr.get_value()), 0.0, 15.0))

    val_arc = always_redraw(
        lambda: Arc(
            radius=rad,
            start_angle=PI,
            angle=-PI * max(0.01, net_val() / 15.0),
            arc_center=c,
            stroke_color=PUSH_COL,
            stroke_width=7,
        )
    )
    needle = always_redraw(
        lambda: Line(
            c,
            c + 0.78 * rad * np.array([np.cos(PI - PI * (net_val() / 15.0)), np.sin(PI - PI * (net_val() / 15.0)), 0]),
            color=PUSH_COL,
            stroke_width=4,
        )
    )
    num = always_redraw(lambda: M(f"{net_val():.1f}", 26, PUSH_COL).move_to(c + DOWN * 0.25))
    title = T("net out", size=22, color=PUSH_COL).move_to(c + UP * (rad + 0.26))
    unit = T("mmHg", size=22, color=TEXT).move_to(c + DOWN * 0.60)
    g = VGroup(track, ref_tick, val_arc, needle, num, title, unit)
    val_arc.layout_ok = True
    needle.layout_ok = True
    return g


class S11Albumin(SpokenScene):
    def construct(self):
        w = CapillaryWorld(
            x_left=-6.2,
            x_right=1.65,
            bars_x=(4.70, 5.62),
            bars_y0=-1.18,
            bars_max_h=2.08,
            show_gauge=True,
        )
        s_list = _safety_list(x_center=5.12, lit=False)
        tag = scope_tag("teaching numbers", color=TEXT)
        self.add(w.root, s_list, tag)

        pi_p_tr = ValueTracker(PI_P_REST)
        pi_g_tr = ValueTracker(PI_G_REST)
        meter = _net_out_meter(pi_p_tr, pi_g_tr)

        self.at("round teaching example")
        self.play(FadeIn(meter), run_time=0.6)

        self.at("lifts the net outward")
        alb_lab = T("albumin 4 to 2 g/dL", size=24, color=ALBUMIN_COL).move_to([-2.3, HEAD_Y, 0])
        self.play(w.albumin_tr.animate.set_value(0.50), w.hold_tr.animate.set_value(0.45), FadeIn(alb_lab), run_time=0.7)

        self.at("from 1")
        self.play(
            pi_p_tr.animate.set_value(14.0),
            w.leak_tr.animate.set_value(0.90),
            w.tissue_h_tr.animate.set_value(2.24),
            run_time=2.2,
        )

        self.at("washout brings it down")
        wash_lab = T("tissue-side protein 6 to 2", size=24, color=ALBUMIN_COL).move_to([-2.3, HEAD_Y, 0])
        about_8 = T("about 8", size=24, color=PUSH_COL).move_to([2.78, 1.00, 0])
        self.play(
            swap(alb_lab, wash_lab, run_time=0.5),
            w.tprot_tr.animate.set_value(0.25),
            w.hold_tr.animate.set_value(0.60),
            pi_g_tr.animate.set_value(2.0),
            w.leak_tr.animate.set_value(0.72),
            FadeIn(about_8),
            run_time=1.4,
        )
        self.finish()


class S12NotHarmless(SpokenScene):
    def construct(self):
        w = CapillaryWorld(
            x_left=-6.2,
            x_right=1.65,
            bars_x=(4.70, 5.62),
            bars_y0=-1.18,
            bars_max_h=2.08,
            leak_0=0.72,
            drain_0=0.45,
            tissue_h_0=2.12,
            albumin_frac_0=0.50,
            hold_scale_0=0.60,
            tissue_prot_frac_0=0.25,
            show_gauge=True,
        )
        pi_p_tr = ValueTracker(14.0)
        pi_g_tr = ValueTracker(2.0)
        meter = _net_out_meter(pi_p_tr, pi_g_tr)
        about_8 = T("about 8", size=24, color=PUSH_COL).move_to([2.78, 1.00, 0])
        s_list = _safety_list(x_center=5.12, lit=False)
        self.add(w.root, meter, about_8, s_list, scope_tag("teaching numbers", color=TEXT))

        self.at("filtration does rise")
        leak_hi = SurroundingRectangle(w.leak_label, color=FLUID_COL, stroke_width=2.5, buff=0.06)
        self.play(Create(leak_hi), run_time=0.5)

        self.at("all three safety factors")
        s_lit = _safety_list(x_center=5.12, lit=True)
        self.play(
            FadeOut(leak_hi),
            Transform(s_list, s_lit),
            w.gauge_tr.animate.set_value(0.85),
            w.push_tr.animate.set_value(0.78),
            w.tprot_tr.animate.set_value(0.10),
            w.pump_tr.animate.set_value(1.85),
            w.drain_tr.animate.set_value(0.72),
            w.tissue_h_tr.animate.set_value(1.90),
            run_time=1.6,
        )
        self.finish()


class S13Globulins(SpokenScene):
    def construct(self):
        w = CapillaryWorld(
            x_left=-6.2,
            x_right=1.65,
            bars_x=(4.70, 5.62),
            bars_y0=-1.18,
            bars_max_h=2.08,
            leak_0=0.64,
            drain_0=0.64,
            tissue_h_0=1.90,
            albumin_frac_0=0.50,
            hold_scale_0=0.55,
            tissue_prot_frac_0=0.10,
            pump_rate_0=1.7,
            show_gauge=True,
            gauge_val_0=0.75,
        )
        s_lit = _safety_list(x_center=5.12, lit=True)
        self.add(w.root, s_lit, scope_tag("schematic", color=TEXT))

        self.at("born without albumin")
        no_alb = T("almost no albumin", size=24, color=ALBUMIN_COL).move_to([-4.2, HEAD_Y, 0])
        self.play(w.albumin_tr.animate.set_value(0.11), w.hold_tr.animate.set_value(0.22), FadeIn(no_alb), run_time=0.8)

        self.at("globulins")
        glob_lab = T("globulins (may help)", size=24, color=GLOB_COL).move_to([-0.2, HEAD_Y, 0])
        self.play(w.glob_tr.animate.set_value(1.0), FadeIn(glob_lab), run_time=0.9)

        self.at("usually mild")
        self.play(w.tissue_h_tr.animate.set_value(1.86), run_time=0.7)

        self.at("a few have none")
        self.play(w.tissue_h_tr.animate.set_value(1.65), run_time=0.6)
        self.wait(0.35)
        self.play(w.tissue_h_tr.animate.set_value(1.84), run_time=0.55)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        w = CapillaryWorld(show_gauge=True, gauge_val_0=0.0)
        self.add(w.root, scope_tag("schematic", color=TEXT))

        self.at("steady leak is normal")
        self.wait(1.2)

        self.at("beats the drain")
        self.play(w.leak_tr.animate.set_value(0.72), w.tissue_h_tr.animate.set_value(2.12), run_time=1.0)

        self.at("three fronts")
        self.play(
            w.gauge_tr.animate.set_value(0.80),
            w.push_tr.animate.set_value(0.78),
            w.tprot_tr.animate.set_value(0.15),
            w.pump_tr.animate.set_value(1.75),
            w.drain_tr.animate.set_value(0.62),
            w.leak_tr.animate.set_value(0.62),
            w.tissue_h_tr.animate.set_value(1.86),
            run_time=1.3,
        )
        self.finish()


class S15End(EndCard):
    LINE = "Edema forms when filtration outruns what lymph can carry."
