"""
Animation for "What a Hard Breath Out Reveals" (Lung Mechanics and Surfactant, Chapter 2).

COLOUR MAP (one colour per concept, continued from Film 1):
- BLUE   (#58C4DD): air in the alveolus / alveolar gas
- YELLOW (#F5D547): bare air-liquid surface (high tension, without surfactant)
- GREEN  (#83C167): surfactant lining (easing tension)
- ORANGE (#FF862F): recoil pressure / transpulmonary pressure matching recoil
- RED    (#FC6255): problem (dynamic compression pinch, airway narrowing, abnormal/below-limit bar)
- CYAN   (#26E2D5): pleural space and pleural pressure (pleural band and pressure gauge)
- WHITE  (#E8EAF0): airflow arrows and spirogram curve/pen
- GREY   (#8B93A1): chest wall arc, airway tube walls, alveolar tethers, axes, schematic tags

ONE WORLD CARRIED:
- Left 60% ('lung panel'): vertical CYAN pleural-pressure gauge (-10 to +10 cmH2O, 0 = atmospheric,
  positive half marked 'schematic'); thick GREY chest-wall arc enclosing a CYAN pleural band;
  one large BLUE alveolus with GREEN surfactant rim, ORANGE inward recoil arrows, thin GREY
  airway tether spokes, and a vertical GREY airway tube rising to a mouth opening with WHITE
  airflow arrows.
- Right 40% ('spirogram panel'): Plot of volume out (0 to 3.5 L) against time (0 to 6 s),
  with ratio / capacity bars neatly below the axes when needed.

PER-SCENE COMPUTED CHANGE:
- s00_link_and_question: Two small ghost alveoli shrink under YELLOW surface tension, turn GREEN
  with surfactant and merge into the main alveolus; alveolus then inflates and blasts air out
  while the spirogram pen traces the initial forced curve V(t) = 3.0 * (1 - 0.5^t).
- s01_title: Silent 2 s title fade-in over the continuously breathing lung (quiet-breath cycle
  with gauge needle swaying between -5 and -8 cmH2O and WHITE airflow arrows cycling).
- s02_two_drops: Quiet-breath cycle driven by P_pl = -6.5 + 1.5 cos(theta) - sin(theta) swings
  gauge -5..-8..-5.5..-5 while the ORANGE wall arrow grows/shrinks with P_tp and airway arrows
  reverse with P_alv; CYAN branches connect gauge to both drops.
- s03_forced: Chest-wall arc squeezes inward, gauge needle climbs from -8 past 0 into positive
  schematic zone, stacked ORANGE+CYAN bar grows to show alveolar pressure = recoil + pleural,
  and alveolus deflates rapidly as thick WHITE arrows stream out.
- s04_squeeze: Lung view zooms smoothly onto the airway tube; CYAN band presses inward, computed
  pressure-drop tiles shade along the lumen from alveolus to mouth, WHITE ring marks the tile
  matching pleural pressure, and the downstream airway pinches narrow in RED.
- s05_dynamic: Zoomed airway demonstrates how weakening ORANGE recoil or narrowing the upstream
  lumen lowers pressure tiles, shifts compression, and thins WHITE maximal flow arrows, then
  reverses and zooms back out to the full dual-panel world.
- s06_spirogram: Forced blow empties alveolus in sync with pen tracing V(t) = 3.0 * (1 - 0.5^t)
  to 6 s (marking FEV1 1.5 L at 1 s and FVC 3.0 L); ratio bar grows to 0.50 below 0.68 limit
  and turns RED ('obstructive').
- s07_idea: Spirogram dims to 30% (stroke-only, no chord fill); lung returns to quiet breathing
  while CYAN gauge drives ORANGE recoil branch (arrows grow/shrink) and resistance branch
  (lumen narrows/widens).
- s08_emphysema: Alveolar wall opens gaps while breathing, ORANGE recoil shrinks, GREY tethers
  fade one by one, forced blow triggers RED pinch earlier toward the alveolus, and Volunteer 1
  spirogram + RED ratio bar brighten and pulse.
- s09_predict: Emphysema reverses; thick dense GREY walls/tethers and large ORANGE recoil form,
  fibrotic alveolus inflates only to smaller TLC inside a dashed old-TLC outline ('TLC falls'),
  spirogram clears, and question card asks 'Does FEV1/FVC fall?'.
- s10_pause: PredictPause holds question while stiff fibrotic alveolus breathes in small rapid
  cycles, gauge needle sways, and empty spirogram displays '?'.
- s11_answer: Question swaps to 'No.'; stiff lung runs a forced blow with large ORANGE recoil
  and thick tethers keeping the RED pinch high near the mouth; schematic FEV1 and FVC bars
  shrink together while their ratio bar stays long ('normal or high').
- s12_restrictive: Deflating fibrotic alveolus stops around a persistent BLUE core ('never
  leaves'); spirogram traces Volunteer 2 V(t) = 2.6 * (1 - 0.154^t) giving FEV1 2.2 L, FVC
  2.6 L, ratio 0.85 within limits; GREY 'body box' encloses lung while RED TLC bar stops at
  3.9 L short of 4.6 L limit.
- s13_rds: Body box and spirogram fade; lung scales down to newborn chest breathing rapidly as
  GREEN rim turns bare YELLOW and ORANGE recoil grows; deep negative CYAN gauge swings dent
  the soft chest wall inward ('retractions') and the alveolus collapses flat on expiration
  ('alveoli close').
- s14_close: Adult lung with GREEN rim resumes quiet breathing beside empty spirogram axes; CYAN
  gauge lights recoil branch (emphysema, fibrosis, RDS) and resistance branch while upstream
  airway narrows in RED (asthma, chronic bronchitis) and relaxes.
- s15_end: Standard EndCard with word-for-word take-home line.
"""
from bp_parts import *

CYAN = "#26E2D5"
WHITE = TEXT

LUNG_CX = -1.92
LUNG_CY = -1.00
GAUGE_X = -5.78

VOL1_V = lambda t: 3.0 * (1.0 - 0.5 ** t)
VOL2_V = lambda t: 2.6 * (1.0 - 0.154 ** t)


def make_spirogram(y_shift=0.0):
    """Build the right-hand spirogram Plot in a fixed position across all scenes."""
    return Plot(
        box=(2.40, 6.05, -0.85 + y_shift, 2.05 + y_shift),
        xr=(0, 6),
        yr=(0, 3.5),
        xticks=[0, 1, 2, 3, 4, 5, 6],
        yticks=[(0, "0"), (1, "1"), (2, "2"), (3, "3")],
        xlabel="time (s)",
        ylabel="volume out (L)",
        color=GREY,
        size=22,
        label_size=24,
        stroke=4.0,
    )


def set_open_curve_opacity(mob, alpha):
    """Dim a mobject or VGroup without turning fill_opacity > 0 on open lines/curves."""
    for sub in mob.family_members_with_points():
        try:
            f_op = float(np.max(sub.get_fill_opacities())) if len(sub.get_fill_opacities()) else 0.0
        except Exception:
            f_op = 0.0
        try:
            s_op = float(np.max(sub.get_stroke_opacities())) if len(sub.get_stroke_opacities()) else 0.0
        except Exception:
            s_op = 0.0
        if f_op > 0.01:
            sub.set_fill(opacity=alpha)
        else:
            sub.set_fill(opacity=0.0)
        if s_op > 0.01:
            sub.set_stroke(opacity=alpha)
    return mob


def mchip(text, color=BLUE, size=22, pad=0.18, fill_opacity=0.18):
    """Multi-line safe rounded labelled box."""
    label = T(text, size=size, color=color, line_spacing=0.82)
    box = RoundedRectangle(
        corner_radius=0.14,
        width=label.width + 2 * pad,
        height=label.height + 2 * pad,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    return VGroup(box, label.move_to(box))


class PleuralGauge(VGroup):
    """Vertical CYAN gauge (-10 to +10 cmH2O) on the far left with live needle driven by p_trk."""

    def __init__(self, p_trk, x=GAUGE_X):
        super().__init__()
        self.p_trk = p_trk
        self.gx = x
        y_bot, y_top = -1.9, 1.9
        self._y_of = lambda p: float(np.clip(p, -10.0, 10.0)) * 0.19

        spine_neg = Line([x, y_bot, 0], [x, 0.0, 0], color=CYAN, stroke_width=6.5)
        spine_pos = DashedLine([x, 0.0, 0], [x, y_top, 0], color=CYAN, stroke_width=6.5, dash_length=0.10)
        bar_bg = Rectangle(width=0.26, height=y_top - y_bot, stroke_width=0, fill_color=CYAN, fill_opacity=0.14).move_to([x, 0, 0])
        self.add(bar_bg, spine_neg, spine_pos)

        for val, lbl in [(-10, "-10"), (-5, "-5"), (0, "0"), (10, "+10")]:
            yy = self._y_of(val)
            tk = Line([x - 0.12, yy, 0], [x + 0.12, yy, 0], color=CYAN if val <= 0 else GREY, stroke_width=3.5)
            t = M(lbl, size=22, color=TEXT if val == 0 else GREY).move_to([x - 0.30, yy, 0], aligned_edge=RIGHT)
            self.add(tk, t)

        atm = T("atmospheric", size=22, color=TEXT).move_to([x + 0.24, 0.0, 0], aligned_edge=LEFT)
        sch = T("schematic", size=22, color=GREY).move_to([x + 0.24, 1.15, 0], aligned_edge=LEFT)
        ttl = T("pleural\npressure", size=24, color=CYAN, line_spacing=0.85).move_to([x, 2.52, 0])
        unit = T("cmH2O", size=22, color=GREY).move_to([x, -2.30, 0])
        self.add(atm, sch, ttl, unit)

        def mk_needle():
            yy = self._y_of(p_trk.get_value())
            col = RED if p_trk.get_value() > 0.2 else CYAN
            tri = Triangle(color=col, fill_color=col, fill_opacity=1.0, stroke_width=1).scale(0.08).rotate(-PI / 2)
            tri.move_to([x - 0.14, yy, 0])
            bar = Line([x - 0.06, yy, 0], [x + 0.14, yy, 0], color=col, stroke_width=6)
            return VGroup(tri, bar)

        self.needle = always_redraw(mk_needle)
        self.add(self.needle)

    def gauge_right_point(self):
        return np.array([self.gx + 0.16, self._y_of(self.p_trk.get_value()), 0.0])


class LungWorld(VGroup):
    """Carried lung + chest wall + pleural band + alveolus + airway + tethers + airflow arrows."""

    def __init__(
        self,
        r=1.10,
        recoil=1.0,
        flow=0.0,
        squeeze=0.0,
        retract=0.0,
        surf=1.0,
        wall_gap=0.0,
        tether_op=1.0,
        thick=0.0,
        pinch=0.0,
        pinch_y=0.55,
        up_narrow=0.0,
        core=0.0,
        scale=1.0,
        zoom=0.0,
        collapse=0.0,
        tiles_op=0.0,
        pleural_bright=0.0,
        pleural_arrows=0.0,
    ):
        super().__init__()
        self.r_trk = ValueTracker(r)
        self.recoil_trk = ValueTracker(recoil)
        self.flow_trk = ValueTracker(flow)
        self.squeeze_trk = ValueTracker(squeeze)
        self.retract_trk = ValueTracker(retract)
        self.surf_trk = ValueTracker(surf)
        self.wall_gap_trk = ValueTracker(wall_gap)
        self.tether_op_trk = ValueTracker(tether_op)
        self.thick_trk = ValueTracker(thick)
        self.pinch_trk = ValueTracker(pinch)
        self.pinch_y_trk = ValueTracker(pinch_y)
        self.up_narrow_trk = ValueTracker(up_narrow)
        self.core_trk = ValueTracker(core)
        self.scale_trk = ValueTracker(scale)
        self.zoom_trk = ValueTracker(zoom)
        self.collapse_trk = ValueTracker(collapse)
        self.tiles_op_trk = ValueTracker(tiles_op)
        self.pleural_bright_trk = ValueTracker(pleural_bright)
        self.pleural_arrows_trk = ValueTracker(pleural_arrows)
        self.phase_trk = ValueTracker(0.0)

        self._phase_driver = VMobject()
        self._phase_driver.add_updater(lambda m, dt: self.phase_trk.increment_value(self.flow_trk.get_value() * dt * 2.0))
        self.add(self._phase_driver)

        self._build_dynamic_world()

    def _geom(self):
        z = float(np.clip(self.zoom_trk.get_value(), 0.0, 1.0))
        sc = float(self.scale_trk.get_value())
        cx = LUNG_CX
        cy = LUNG_CY * (1.0 - z) + (-1.95) * z
        r_raw = float(self.r_trk.get_value()) * sc
        col = float(np.clip(self.collapse_trk.get_value(), 0.0, 0.85))
        rx = r_raw * (1.0 - 0.12 * col) * (1.0 - 0.22 * z)
        ry = r_raw * (1.0 - 0.70 * col) * (1.0 - 0.48 * z)
        w_air = (0.26 * (1.0 - z) + 0.38 * z) * sc
        y_air_bot = cy + ry * 0.72
        y_air_top = (2.32 * (1.0 - z) + 2.35 * z) * (1.0 if sc >= 0.9 else 0.85)
        y_pleural_top = (1.76 * (1.0 - z) + 1.92 * z) * (1.0 if sc >= 0.9 else 0.85)
        return cx, cy, rx, ry, w_air, y_air_bot, y_air_top, y_pleural_top, z, sc

    def _airway_half_width(self, y, y_bot, y_top, y_pl_top, w_air, z):
        """Return half-width of airway lumen at vertical position y."""
        frac = np.clip((y - y_bot) / max(y_pl_top - y_bot, 1e-4), 0.0, 1.0)
        pinch = float(np.clip(self.pinch_trk.get_value(), 0.0, 1.0))
        pf = float(np.clip(self.pinch_y_trk.get_value(), 0.15, 0.88))
        up_n = float(np.clip(self.up_narrow_trk.get_value(), 0.0, 1.0))

        hw = w_air
        if pinch > 0.01 and y <= y_pl_top + 0.08:
            s = np.clip((frac - pf) / 0.12, 0.0, 1.0)
            s_end = np.clip((1.02 - frac) / 0.10, 0.0, 1.0)
            hw -= pinch * (0.58 * w_air) * s * s_end
        if up_n > 0.01:
            u_mid = max(0.22, pf * 0.55)
            u_bell = np.exp(-((frac - u_mid) / 0.16) ** 2)
            hw -= up_n * (0.44 * w_air) * u_bell
        if y > y_pl_top:
            m_f = np.clip((y - y_pl_top) / max(y_top - y_pl_top, 1e-4), 0.0, 1.0)
            hw += 0.16 * w_air * (m_f ** 1.5)
        return max(0.06, hw)

    def _build_dynamic_world(self):
        def mk_world():
            cx, cy, rx, ry, w_air, y_bot, y_top, y_pl_top, z, sc = self._geom()
            g = VGroup()

            sq = float(self.squeeze_trk.get_value())
            ret = float(self.retract_trk.get_value())
            pb = float(self.pleural_bright_trk.get_value())
            thick = float(self.thick_trk.get_value())
            surf = float(np.clip(self.surf_trk.get_value(), 0.0, 1.0))
            w_gap = float(np.clip(self.wall_gap_trk.get_value(), 0.0, 1.0))
            teth_op = float(np.clip(self.tether_op_trk.get_value(), 0.0, 1.0))
            pinch = float(np.clip(self.pinch_trk.get_value(), 0.0, 1.0))
            pf = float(np.clip(self.pinch_y_trk.get_value(), 0.15, 0.88))
            up_n = float(np.clip(self.up_narrow_trk.get_value(), 0.0, 1.0))

            # 1. CYAN pleural space band
            pl_pad_r = (0.24 + 0.05 * z - 0.05 * sq) * sc
            pl_pad_x = (0.18 + 0.14 * z - 0.04 * sq) * sc

            ang_start = np.arcsin(np.clip((w_air + pl_pad_x) / max(rx + pl_pad_r, 0.2), -0.95, 0.95))
            thetas = np.linspace(PI / 2 + ang_start, 2 * PI + PI / 2 - ang_start, 44)
            outer_pts = []
            ys_side = np.linspace(y_pl_top, cy + (ry + pl_pad_r) * np.cos(ang_start), 10)
            for yy in ys_side:
                outer_pts.append([cx + w_air + pl_pad_x, yy, 0.0])
            for th in reversed(thetas):
                outer_pts.append([cx + (rx + pl_pad_r) * np.cos(th), cy + (ry + pl_pad_r) * np.sin(th), 0.0])
            for yy in reversed(ys_side):
                outer_pts.append([cx - w_air - pl_pad_x, yy, 0.0])

            pleural_poly = Polygon(
                *outer_pts,
                stroke_color=CYAN,
                stroke_width=4.0 + 1.5 * pb,
                fill_color=CYAN,
                fill_opacity=0.35 + 0.18 * pb,
            )
            g.add(pleural_poly)

            # 2. Thick GREY chest-wall arc outside pleural band
            cw_off = (0.14 - 0.04 * sq) * sc
            cw_side_x = (rx + pl_pad_r + cw_off) * (1.0 - z) + (w_air + pl_pad_x + 0.20) * z
            cw_pts_r, cw_pts_l = [], []
            dent = ret * 0.24 * sc
            for yy in np.linspace(y_pl_top + 0.06, cy, 12):
                blend_bot = float(np.clip((yy - cy) / max(y_pl_top - cy, 0.4), 0.0, 1.0))
                frac_d = np.exp(-((yy - (cy + 0.5)) / 0.7) ** 2) * np.sin(PI * blend_bot)
                x_wall = cw_side_x * blend_bot + (rx + pl_pad_r + cw_off) * (1.0 - blend_bot)
                cw_pts_r.append([cx + x_wall - dent * frac_d, yy, 0.0])
                cw_pts_l.append([cx - x_wall + dent * frac_d, yy, 0.0])
            bottom_thetas = np.linspace(0, -PI, 26)
            cw_bot = [
                [cx + (rx + pl_pad_r + cw_off) * np.cos(th), cy + (ry + pl_pad_r + cw_off) * np.sin(th), 0.0]
                for th in bottom_thetas
            ]
            cw_all = cw_pts_r + cw_bot + list(reversed(cw_pts_l))
            chest_wall = VMobject(stroke_color=GREY, stroke_width=20.0 + 4.0 * sq, fill_opacity=0)
            chest_wall.set_points_as_corners(cw_all)
            g.add(chest_wall)

            # 3. Alveolus BLUE air + GREEN/YELLOW rim
            neck_ang = np.arcsin(np.clip(w_air / max(rx, 0.15), -0.92, 0.92))
            alv_thetas = np.linspace(PI / 2 + neck_ang, 2 * PI + PI / 2 - neck_ang, 48)
            alv_pts = [[cx + rx * np.cos(th), cy + ry * np.sin(th), 0.0] for th in alv_thetas]
            air_fill_pts = (
                [[cx - w_air, y_bot + 0.15, 0.0]]
                + alv_pts
                + [[cx + w_air, y_bot + 0.15, 0.0]]
            )
            alv_fill = Polygon(*air_fill_pts, stroke_width=0, fill_color=BLUE, fill_opacity=0.58)
            g.add(alv_fill)

            core_v = float(np.clip(self.core_trk.get_value(), 0.0, 1.0))
            if core_v > 0.02:
                core_circ = Ellipse(
                    width=rx * 0.90,
                    height=ry * 0.90,
                    stroke_color=BLUE,
                    stroke_width=3.0,
                    fill_color=BLUE,
                    fill_opacity=0.72 * core_v,
                ).move_to([cx, cy, 0])
                g.add(core_circ)

            rim_col = interpolate_color(ManimColor(YELLOW), ManimColor(GREEN), surf)
            rim_w = 7.0 + 4.5 * thick
            if w_gap < 0.05:
                rim = VMobject(stroke_color=rim_col, stroke_width=rim_w, fill_opacity=0)
                rim.set_points_as_corners(alv_pts)
                g.add(rim)
            else:
                n_seg = 6
                seg_len = len(alv_pts) // n_seg
                for k in range(n_seg):
                    i0 = k * seg_len
                    i1 = min(len(alv_pts), (k + 1) * seg_len - int(round(w_gap * seg_len * 0.48)))
                    if i1 - i0 >= 2:
                        seg = VMobject(stroke_color=rim_col, stroke_width=rim_w, fill_opacity=0)
                        seg.set_points_as_corners(alv_pts[i0:i1])
                        g.add(seg)

            if thick > 0.05:
                outer_tis = VMobject(stroke_color=GREY, stroke_width=6.5 * thick, fill_opacity=0)
                outer_tis.set_points_as_corners([[cx + (rx + 0.06) * np.cos(th), cy + (ry + 0.06) * np.sin(th), 0.0] for th in alv_thetas])
                g.add(outer_tis)

            # 4. Airway tube
            ys = np.linspace(y_bot, y_top, 26)
            left_wall_pts = [[cx - self._airway_half_width(y, y_bot, y_top, y_pl_top, w_air, z), y, 0.0] for y in ys]
            right_wall_pts = [[cx + self._airway_half_width(y, y_bot, y_top, y_pl_top, w_air, z), y, 0.0] for y in ys]

            lumen_poly = Polygon(*(left_wall_pts + list(reversed(right_wall_pts))), stroke_width=0, fill_color=BLUE, fill_opacity=0.38)
            g.add(lumen_poly)

            t_op = float(np.clip(self.tiles_op_trk.get_value(), 0.0, 1.0))
            if t_op > 0.02:
                n_tiles = 12
                yt_edges = np.linspace(y_bot + 0.05, y_pl_top - 0.05, n_tiles + 1)
                rec_s = float(np.clip(self.recoil_trk.get_value(), 0.3, 1.5))
                for i in range(n_tiles):
                    ya, yb = yt_edges[i], yt_edges[i + 1]
                    hw_a = self._airway_half_width(ya, y_bot, y_top, y_pl_top, w_air, z) * 0.86
                    hw_b = self._airway_half_width(yb, y_bot, y_top, y_pl_top, w_air, z) * 0.86
                    f_pos = i / (n_tiles - 1)
                    steep = 1.0 + 0.55 * up_n + 0.4 * max(0.0, 1.0 - rec_s)
                    bright = float(np.clip(1.0 - 0.92 * (f_pos ** (1.0 / steep)), 0.06, 1.0))
                    tile_col = interpolate_color(ManimColor("#172130"), ManimColor("#FFF3B0"), bright)
                    tile = Polygon(
                        [cx - hw_a, ya + 0.02, 0.0],
                        [cx + hw_a, ya + 0.02, 0.0],
                        [cx + hw_b, yb - 0.02, 0.0],
                        [cx - hw_b, yb - 0.02, 0.0],
                        stroke_width=0,
                        fill_color=tile_col,
                        fill_opacity=0.80 * t_op,
                    )
                    g.add(tile)

            y_pinch = y_bot + pf * (y_pl_top - y_bot)
            for side_pts in (left_wall_pts, right_wall_pts):
                for i in range(len(side_pts) - 1):
                    p0, p1 = side_pts[i], side_pts[i + 1]
                    ym = 0.5 * (p0[1] + p1[1])
                    col = GREY
                    sw = 5.0 + 1.5 * thick
                    if pinch > 0.25 and y_pinch <= ym <= y_pl_top + 0.05:
                        col = RED
                        sw = 6.0
                    elif up_n > 0.25 and (y_bot + 0.1 * (y_pl_top - y_bot)) <= ym < y_pinch - 0.05:
                        col = RED
                        sw = 6.0
                    g.add(Line(p0, p1, color=col, stroke_width=sw))

            if pinch > 0.25 or t_op > 0.3:
                hw_p = self._airway_half_width(y_pinch, y_bot, y_top, y_pl_top, w_air, z)
                ring = RoundedRectangle(
                    width=2 * hw_p + 0.16,
                    height=0.20,
                    corner_radius=0.07,
                    stroke_color=WHITE,
                    stroke_width=3.5,
                    fill_opacity=0,
                ).move_to([cx, y_pinch, 0.0])
                g.add(ring)

            # 5. Thin GREY tether spokes holding airway round
            if teth_op > 0.03:
                teth_w = 2.6 + 3.4 * thick
                for idx, fy in enumerate([0.16, 0.34, 0.52]):
                    yt = y_bot + fy * (y_pl_top - y_bot)
                    hw = self._airway_half_width(yt, y_bot, y_top, y_pl_top, w_air, z)
                    dx_out = (rx * 0.85 + 0.12 * idx) * (0.95 - 0.15 * z)
                    dy_out = -0.35 - 0.12 * idx
                    for sgn in (-1, 1):
                        sp = Line(
                            [cx + sgn * hw, yt, 0.0],
                            [cx + sgn * min(dx_out, rx + pl_pad_r - 0.06), max(cy - ry * 0.1, yt + dy_out), 0.0],
                            color=GREY,
                            stroke_width=teth_w,
                            stroke_opacity=0.90 * teth_op,
                        )
                        g.add(sp)

            # 6. ORANGE inward recoil arrows
            rec_scale = float(np.clip(self.recoil_trk.get_value(), 0.2, 1.7))
            max_len = min(rx * 0.45, ry * 0.46)
            rec_len = min(max_len, (0.26 + 0.10 * sc) * rec_scale)
            angles = [PI * 0.82, PI * 1.18, PI * 1.82, PI * 2.18] if z < 0.4 else [PI * 0.78, PI * 0.22]
            for th in angles:
                rim_pt = np.array([cx + rx * np.cos(th), cy + ry * np.sin(th), 0.0])
                inward = np.array([-np.cos(th), -np.sin(th), 0.0])
                inward /= max(np.linalg.norm(inward), 1e-6)
                a = Arrow(
                    rim_pt - inward * 0.02,
                    rim_pt + inward * rec_len,
                    buff=0,
                    color=ORANGE,
                    stroke_width=5.0,
                    max_tip_length_to_length_ratio=0.42,
                )
                g.add(a)

            # 7. CYAN inward pleural pressure arrows on airway walls (s04)
            pa = float(np.clip(self.pleural_arrows_trk.get_value(), 0.0, 1.0))
            if pa > 0.05:
                for fy in [0.28, 0.55, 0.80]:
                    ya = y_bot + fy * (y_pl_top - y_bot)
                    hw = self._airway_half_width(ya, y_bot, y_top, y_pl_top, w_air, z)
                    for sgn in (-1, 1):
                        g.add(
                            Arrow(
                                [cx + sgn * (hw + 0.28), ya, 0.0],
                                [cx + sgn * (hw + 0.04), ya, 0.0],
                                buff=0,
                                color=CYAN,
                                stroke_width=3.5,
                                stroke_opacity=pa,
                                max_tip_length_to_length_ratio=0.42,
                            )
                        )

            # 8. WHITE airflow arrows moving smoothly along airway centerline
            fl = float(self.flow_trk.get_value())
            if abs(fl) > 0.06:
                ph = float(self.phase_trk.get_value()) % 1.0
                n_arr = 4
                dir_y = 1.0 if fl > 0 else -1.0
                mag = float(np.clip(abs(fl), 0.25, 2.5))
                arr_len = 0.32 + 0.14 * min(mag, 1.6)
                sw_f = 4.5 + 2.2 * min(mag, 1.6)
                span_bot = y_bot + 0.12
                span_top = y_top + 0.28
                for k in range(n_arr):
                    u = (k / n_arr + ph) % 1.0
                    yy = span_bot + u * (span_top - span_bot)
                    fade = np.sin(PI * u) ** 0.5
                    a = Arrow(
                        [cx, yy - 0.5 * dir_y * arr_len, 0.0],
                        [cx, yy + 0.5 * dir_y * arr_len, 0.0],
                        buff=0,
                        color=WHITE,
                        stroke_width=sw_f,
                        stroke_opacity=0.95 * fade,
                        fill_opacity=0.95 * fade,
                        max_tip_length_to_length_ratio=0.45,
                    )
                    g.add(a)

            return g

        self.dynamic_body = always_redraw(mk_world)
        self.add(self.dynamic_body)

    def chest_right_x(self):
        cx, cy, rx, ry, w_air, y_bot, y_top, y_pl_top, z, sc = self._geom()
        sq = float(self.squeeze_trk.get_value())
        pl_pad_r = (0.24 + 0.05 * z - 0.05 * sq) * sc
        cw_off = (0.13 - 0.04 * sq) * sc
        return cx + rx + pl_pad_r + cw_off

    def wall_anchor_right(self):
        cx, cy, rx, ry, w_air, y_bot, y_top, y_pl_top, z, sc = self._geom()
        return np.array([cx + rx, cy - 0.1, 0.0])

    def pleural_anchor_right(self):
        cx, cy, rx, ry, w_air, y_bot, y_top, y_pl_top, z, sc = self._geom()
        sq = float(self.squeeze_trk.get_value())
        pl_pad_r = (0.24 + 0.05 * z - 0.05 * sq) * sc
        return np.array([cx + rx + pl_pad_r * 0.92, cy - 0.1, 0.0])

    def airway_mid_right(self):
        cx, cy, rx, ry, w_air, y_bot, y_top, y_pl_top, z, sc = self._geom()
        ym = 0.5 * (y_bot + y_pl_top)
        hw = self._airway_half_width(ym, y_bot, y_top, y_pl_top, w_air, z)
        return np.array([cx + hw + 0.22, ym, 0.0])

    def pinch_point_right(self):
        cx, cy, rx, ry, w_air, y_bot, y_top, y_pl_top, z, sc = self._geom()
        pf = float(np.clip(self.pinch_y_trk.get_value(), 0.15, 0.88))
        yp = y_bot + pf * (y_pl_top - y_bot)
        hw = self._airway_half_width(yp, y_bot, y_top, y_pl_top, w_air, z)
        return np.array([cx + hw + 0.26, yp, 0.0])

    def pinch_zone_right(self):
        cx, cy, rx, ry, w_air, y_bot, y_top, y_pl_top, z, sc = self._geom()
        pf = float(np.clip(self.pinch_y_trk.get_value(), 0.15, 0.88))
        yp = y_bot + pf * (y_pl_top - y_bot)
        ym = 0.5 * (yp + y_pl_top)
        hw = self._airway_half_width(ym, y_bot, y_top, y_pl_top, w_air, z)
        return np.array([cx + hw + 0.22, ym, 0.0])


def attach_quiet_breathing(world, gauge, theta_start=0.0, speed=1.45, r_base=1.06, r_amp=0.14, p_offset=0.0, flow_amp=0.95):
    """Attach continuous quiet-breathing cycle matching the lesson's table (-5, -7.5, -8, -5.5)."""
    theta = ValueTracker(theta_start)

    def step(mob, dt):
        theta.increment_value(speed * dt)
        th = theta.get_value()
        v_frac = 0.5 * (1.0 - np.cos(th))
        world.r_trk.set_value(r_base + r_amp * v_frac)
        world.flow_trk.set_value(-flow_amp * np.sin(th))
        gauge.p_trk.set_value(p_offset + (-6.5 + 1.5 * np.cos(th) - 1.0 * np.sin(th)))
        world.squeeze_trk.set_value(-0.18 * v_frac)

    driver = VMobject()
    driver.add_updater(step)
    return theta, driver


def build_base_world(**world_kw):
    """Build standard gauge + LungWorld + spirogram axes."""
    p_trk = ValueTracker(world_kw.pop("p_init", -5.0))
    gauge = PleuralGauge(p_trk)
    world = LungWorld(**world_kw)
    plot = make_spirogram()
    return gauge, world, plot


def make_ratio_bar(x0=2.40, x1=6.05, y=-2.35, val_trk=None, limit=0.68, max_v=1.0, limit_label="limit 0.68 (made-up)", bar_label_fn=None):
    """Horizontal computed bar from 0 to max_v with a limit tick and live value readout."""
    w = x1 - x0
    track = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=6)
    tick_x = x0 + (limit / max_v) * w
    tick = Line([tick_x, y - 0.14, 0], [tick_x, y + 0.14, 0], color=TEXT, stroke_width=3.5)
    lim_txt = T(limit_label, size=22, color=GREY).move_to([tick_x, y + 0.36, 0])
    if lim_txt.get_right()[0] > 6.20:
        lim_txt.shift(LEFT * (lim_txt.get_right()[0] - 6.20))

    def mk_bar():
        v = float(np.clip(val_trk.get_value(), 0.001, max_v))
        col = RED if v < limit - 1e-4 else GREEN
        bx = x0 + (v / max_v) * w
        bar = Line([x0, y, 0], [bx, y, 0], color=col, stroke_width=18)
        dot = Dot([bx, y, 0], radius=0.08, color=col)
        g = VGroup(bar, dot)
        if bar_label_fn is not None:
            lbl = M(bar_label_fn(v), size=22, color=col).move_to([(x0 + x1) / 2, y - 0.33, 0])
            if lbl.get_right()[0] > 6.20:
                lbl.shift(LEFT * (lbl.get_right()[0] - 6.20))
            g.add(lbl)
        return g

    return VGroup(track, tick, lim_txt, always_redraw(mk_bar))


def spiro_tag(text, color=GREY):
    """Right-aligned tag cleanly above 'volume out (L)' at top of spirogram."""
    return T(text, size=22, color=color).move_to([6.10, 2.98, 0], aligned_edge=RIGHT)


# ====================================================================== SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.06, p_init=-5.0, flow=0.0, surf=1.0)
        self.add(gauge, world, plot)

        g_r1 = ValueTracker(0.42)
        g_r2 = ValueTracker(0.28)
        g_surf = ValueTracker(0.0)
        g_center = np.array([0.90, 1.30, 0.0])

        def mk_ghost():
            col = interpolate_color(ManimColor(YELLOW), ManimColor(GREEN), float(g_surf.get_value()))
            c1 = Circle(radius=float(g_r1.get_value()), stroke_color=col, stroke_width=4.5, fill_color=BLUE, fill_opacity=0.38).move_to(g_center + LEFT * 0.45)
            c2 = Circle(radius=float(g_r2.get_value()), stroke_color=col, stroke_width=4.5, fill_color=BLUE, fill_opacity=0.38).move_to(g_center + RIGHT * 0.42)
            arrs = VGroup()
            a_scale = 1.0 - 0.65 * float(g_surf.get_value())
            for circ in (c1, c2):
                cc = circ.get_center()
                rr = circ.radius
                for th in (PI * 0.25, PI * 0.75, PI * 1.25, PI * 1.75):
                    p0 = cc + rr * np.array([np.cos(th), np.sin(th), 0])
                    inw = np.array([-np.cos(th), -np.sin(th), 0])
                    arrs.add(Arrow(p0, p0 + inw * 0.22 * a_scale, buff=0, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.5))
            return VGroup(c1, c2, arrs)

        ghost = always_redraw(mk_ghost)
        theta0, drv0 = attach_quiet_breathing(world, gauge, theta_start=0.0, speed=1.45)
        self.add(drv0)
        self.play(FadeIn(ghost), run_time=0.45)

        self.at("wet lining")
        self.play(g_r1.animate.set_value(0.30), g_r2.animate.set_value(0.19), run_time=1.8, rate_func=smooth)

        self.at("surfactant")
        self.play(
            g_surf.animate.set_value(1.0),
            g_r1.animate.set_value(0.38),
            g_r2.animate.set_value(0.25),
            run_time=1.1,
        )
        self.play(ghost.animate.move_to([LUNG_CX, LUNG_CY, 0]).scale(0.35).set_opacity(0), run_time=0.75)
        self.remove(ghost)

        self.at("breathe in")
        self.remove(drv0)
        self.play(
            world.r_trk.animate.set_value(1.24),
            gauge.p_trk.animate.set_value(-8.5),
            world.flow_trk.animate.set_value(-1.0),
            world.squeeze_trk.animate.set_value(-0.22),
            run_time=0.95,
        )

        self.at("blow out hard")
        t_spi = ValueTracker(0.0)
        live_hook = plot.live_curve(VOL1_V, t_spi, color=WHITE, width=6)
        dot_hook = plot.dot(lambda: t_spi.get_value(), lambda: VOL1_V(t_spi.get_value()), color=WHITE, ring=CYAN, radius=0.09)
        self.add(live_hook, dot_hook)
        self.play(
            world.r_trk.animate.set_value(0.74),
            gauge.p_trk.animate.set_value(4.5),
            world.flow_trk.animate.set_value(2.2),
            world.squeeze_trk.animate.set_value(0.85),
            t_spi.animate.set_value(1.6),
            run_time=1.55,
            rate_func=rush_from,
        )
        world.flow_trk.set_value(0.5)

        self.at("What does")
        q_txt = T("What does a hard blow reveal?", size=38, color=WHITE).move_to([0.0, 3.12, 0])
        self.play(FadeIn(q_txt, shift=DOWN * 0.1), run_time=0.65)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.06, p_init=-5.0, flow=0.0, surf=1.0)
        q_txt = T("What does a hard blow reveal?", size=38, color=WHITE).move_to([0.0, 3.12, 0])
        title = T("What a Hard Breath Out Reveals", size=44, font=TITLE_FONT, color=WHITE).move_to([0.0, 3.12, 0])
        theta, drv = attach_quiet_breathing(world, gauge, theta_start=0.2, speed=2.4)
        self.add(gauge, world, plot, drv, q_txt)
        self.play(FadeOut(q_txt), run_time=self.beat(0.18))
        self.play(FadeIn(title), run_time=self.beat(0.22))
        self.wait(self.beat(0.42))
        self.play(FadeOut(title), run_time=self.beat(0.18))
        self.finish()


class S02TwoDrops(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.06, p_init=-5.0, flow=0.0, surf=1.0)
        theta, drv = attach_quiet_breathing(world, gauge, theta_start=1.4, speed=1.45)
        self.add(gauge, world, plot, drv)

        def mk_tp_arrow():
            p_in = world.wall_anchor_right() + LEFT * 0.08
            p_out = world.pleural_anchor_right() + RIGHT * 0.02
            return DoubleArrow(p_in, p_out, buff=0, color=ORANGE, stroke_width=4.5, tip_length=0.14)

        tp_arrow = always_redraw(mk_tp_arrow)
        lbl_tp = T("transpulmonary\n= recoil", size=24, color=ORANGE, line_spacing=0.85).move_to([-0.15, -1.65, 0], aligned_edge=LEFT)
        tp_leader = always_redraw(
            lambda: Line(world.chest_right_x() * RIGHT + (LUNG_CY - 0.1) * UP + RIGHT * 0.04, lbl_tp.get_left() + LEFT * 0.10, color=ORANGE, stroke_width=2.5)
        )
        tp_leader.layout_ok = "covered"

        lbl_aw = T("airway drop:\nmoves air", size=24, color=WHITE, line_spacing=0.85).move_to([-0.15, 1.15, 0], aligned_edge=LEFT)
        aw_leader = always_redraw(
            lambda: Line(world.airway_mid_right(), lbl_aw.get_left() + LEFT * 0.10, color=WHITE, stroke_width=2.5)
        )
        aw_leader.layout_ok = "covered"

        self.at("Every breath")
        self.wait(0.3)

        self.at("Across")
        self.play(FadeIn(tp_arrow), run_time=0.6)

        self.at("transpulmonary")
        self.play(FadeIn(tp_leader), FadeIn(lbl_tp), run_time=0.7)

        self.at("Along")
        self.play(FadeIn(aw_leader), FadeIn(lbl_aw), run_time=0.7)

        self.at("pays for both")
        c_line1 = always_redraw(lambda: Line(gauge.gauge_right_point(), lbl_tp.get_left() + LEFT * 0.12, color=CYAN, stroke_width=2.4))
        c_line2 = always_redraw(lambda: Line(gauge.gauge_right_point(), lbl_aw.get_left() + LEFT * 0.12, color=CYAN, stroke_width=2.4))
        c_line1.layout_ok = "covered"
        c_line2.layout_ok = "covered"
        self.play(
            Create(c_line1),
            Create(c_line2),
            lbl_tp.animate.set_color(GOLD),
            lbl_aw.animate.set_color(GOLD),
            run_time=0.7,
        )
        self.finish()


class S03Forced(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.20, p_init=-8.0, flow=0.0, surf=1.0, squeeze=-0.2)
        self.add(gauge, world, plot)

        self.at("Blow out hard")
        self.at("expiratory muscles")
        self.play(
            world.squeeze_trk.animate.set_value(1.0),
            gauge.p_trk.animate.set_value(5.0),
            run_time=1.7,
        )

        self.at("Alveolar pressure")
        bar_x = 0.42
        bar_y0 = -1.65
        bar_w = 0.76
        h_rec = ValueTracker(0.01)
        h_pl = ValueTracker(0.01)

        def mk_stack():
            hr = float(h_rec.get_value())
            hp = float(h_pl.get_value())
            r_rect = Rectangle(width=bar_w, height=max(0.02, hr), stroke_color=ORANGE, stroke_width=3.5, fill_color=ORANGE, fill_opacity=0.45)
            r_rect.move_to([bar_x, bar_y0 + hr / 2, 0])
            p_rect = Rectangle(width=bar_w, height=max(0.02, hp), stroke_color=CYAN, stroke_width=3.5, fill_color=CYAN, fill_opacity=0.45)
            p_rect.move_to([bar_x, bar_y0 + hr + hp / 2, 0])
            return VGroup(r_rect, p_rect)

        stack = always_redraw(mk_stack)
        lbl_top = T("alveolar\npressure", size=26, color=WHITE, line_spacing=0.85).move_to([bar_x + 0.18, bar_y0 + 2.45, 0])
        lbl_rec = T("recoil", size=24, color=ORANGE).move_to([bar_x + 0.52, bar_y0 + 0.48, 0], aligned_edge=LEFT)
        lbl_pl = T("pleural", size=24, color=CYAN).move_to([bar_x + 0.52, bar_y0 + 1.44, 0], aligned_edge=LEFT)
        sch = T("schematic", size=22, color=GREY).move_to([bar_x + 0.18, bar_y0 - 0.38, 0])
        self.add(stack)
        self.play(FadeIn(lbl_top), FadeIn(sch), run_time=0.45)

        self.at("recoil plus")
        self.play(h_rec.animate.set_value(0.95), world.r_trk.animate.set_value(1.10), FadeIn(lbl_rec), run_time=0.75)
        self.play(h_pl.animate.set_value(0.95), world.r_trk.animate.set_value(1.00), FadeIn(lbl_pl), run_time=0.75)

        self.at("air rushes out")
        self.play(
            world.flow_trk.animate.set_value(2.4),
            world.r_trk.animate.set_value(0.70),
            run_time=1.35,
        )
        self.finish()


class S04Squeeze(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(
            r=1.14, p_init=5.0, flow=1.8, squeeze=0.85, surf=1.0, zoom=0.0
        )
        self.add(gauge, world, plot)

        self.play(world.zoom_trk.animate.set_value(1.0), run_time=1.0)

        self.at("same")
        self.play(
            world.pleural_bright_trk.animate.set_value(1.0),
            world.pleural_arrows_trk.animate.set_value(1.0),
            world.r_trk.animate.set_value(1.06),
            run_time=0.95,
        )

        self.at("Friction uses up")
        lbl_drop = T("pressure falling\nalong airway\n(schematic)", size=24, color=TEXT, line_spacing=0.85).move_to([-0.50, -0.75, 0], aligned_edge=LEFT)
        self.play(
            world.tiles_op_trk.animate.set_value(1.0),
            world.r_trk.animate.set_value(0.96),
            FadeIn(lbl_drop),
            run_time=1.4,
        )

        self.at("pressure inside falls")
        lbl_eq = T("inside = pleural", size=26, color=WHITE).move_to([-0.50, 0.35, 0], aligned_edge=LEFT)
        eq_line = always_redraw(lambda: Line(world.pinch_point_right() + LEFT * 0.14, lbl_eq.get_left() + LEFT * 0.12, color=WHITE, stroke_width=2.5))
        eq_line.layout_ok = "covered"
        self.play(
            world.pinch_trk.animate.set_value(0.3),
            world.r_trk.animate.set_value(0.88),
            FadeIn(eq_line),
            FadeIn(lbl_eq),
            run_time=1.0,
        )

        self.at("airway beyond is squeezed")
        lbl_sq = T("squeezed", size=28, color=RED).move_to([-0.50, 1.40, 0], aligned_edge=LEFT)
        sq_line = always_redraw(lambda: Line(world.pinch_zone_right() + LEFT * 0.05, lbl_sq.get_left() + LEFT * 0.12, color=RED, stroke_width=2.5))
        sq_line.layout_ok = "covered"
        self.play(
            world.pinch_trk.animate.set_value(1.0),
            world.r_trk.animate.set_value(0.78),
            FadeIn(sq_line),
            FadeIn(lbl_sq),
            run_time=1.2,
        )
        self.finish()


class S05Dynamic(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(
            r=1.08, p_init=5.0, flow=1.8, squeeze=0.85, surf=1.0, zoom=1.0,
            tiles_op=1.0, pleural_bright=1.0, pleural_arrows=1.0, pinch=1.0, pinch_y=0.55,
        )
        lbl_sq = T("squeezed", size=28, color=RED).move_to([-0.50, 1.40, 0], aligned_edge=LEFT)
        lbl_dyn = T("dynamic\ncompression", size=28, color=RED, line_spacing=0.85).move_to([-0.50, 1.40, 0], aligned_edge=LEFT)
        self.add(gauge, world, plot, lbl_sq)

        self.at("dynamic compression")
        self.play(swap(lbl_sq, lbl_dyn, run_time=0.55), world.r_trk.animate.set_value(1.00), run_time=0.75)

        self.at("weak recoil")
        self.play(
            world.recoil_trk.animate.set_value(0.35),
            world.pinch_y_trk.animate.set_value(0.34),
            world.flow_trk.animate.set_value(0.45),
            world.r_trk.animate.set_value(0.86),
            run_time=0.85,
        )
        self.play(
            world.recoil_trk.animate.set_value(1.0),
            world.pinch_y_trk.animate.set_value(0.55),
            world.flow_trk.animate.set_value(1.6),
            world.r_trk.animate.set_value(1.02),
            run_time=0.55,
        )

        self.at("narrowed airways upstream")
        self.play(
            world.up_narrow_trk.animate.set_value(1.0),
            world.flow_trk.animate.set_value(0.42),
            world.r_trk.animate.set_value(0.88),
            run_time=1.35,
        )

        self.at("low maximal flow")
        lbl_low = T("low maximal flow", size=24, color=WHITE).move_to([-0.55, 2.20, 0], aligned_edge=LEFT)
        self.play(FadeIn(lbl_low), world.r_trk.animate.set_value(0.78), run_time=0.8)
        self.wait(0.25)

        self.play(FadeOut(lbl_dyn), FadeOut(lbl_low), run_time=0.35)
        self.play(
            world.up_narrow_trk.animate.set_value(0.0),
            world.tiles_op_trk.animate.set_value(0.0),
            world.pleural_bright_trk.animate.set_value(0.0),
            world.pleural_arrows_trk.animate.set_value(0.0),
            world.pinch_trk.animate.set_value(0.0),
            world.zoom_trk.animate.set_value(0.0),
            world.flow_trk.animate.set_value(0.5),
            world.r_trk.animate.set_value(0.98),
            run_time=1.1,
        )
        self.finish()


class S06Spirogram(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.22, p_init=-8.0, flow=0.0, squeeze=-0.18, surf=1.0)
        tag = spiro_tag("volunteer 1 (made-up)")
        t_spi = ValueTracker(0.0)
        live = plot.live_curve(VOL1_V, t_spi, color=WHITE, width=6)
        dot = plot.dot(lambda: t_spi.get_value(), lambda: VOL1_V(t_spi.get_value()), color=WHITE, ring=CYAN, radius=0.07)
        self.add(gauge, world, plot, tag, live)

        def sync_blow(m, dt):
            tt = t_spi.get_value()
            if tt > 0.01:
                v_out = VOL1_V(tt)
                world.r_trk.set_value(1.22 - 0.50 * (v_out / 3.0))
                rate = 3.0 * np.log(2.0) * (0.5 ** tt)
                world.flow_trk.set_value(max(0.24, min(2.4, rate * 1.15)))

        drv = VMobject().add_updater(sync_blow)
        self.add(drv)

        self.at("records the blast")
        self.add(dot)
        self.play(
            gauge.p_trk.animate.set_value(5.0),
            world.squeeze_trk.animate.set_value(0.95),
            world.pinch_trk.animate.set_value(1.0),
            t_spi.animate.set_value(1.0),
            run_time=2.5,
            rate_func=linear,
        )

        self.at("FEV1")
        p1 = plot.pt(1.0, 1.5)
        v1_line = DashedLine(plot.pt(1.0, 0.0), p1, color=YELLOW, stroke_width=3.5, dash_length=0.12)
        d1 = Dot(p1, radius=0.08, color=YELLOW)
        lbl_fev1 = T("FEV1 1.5 L", size=24, color=YELLOW).move_to([4.05, 0.15, 0])
        fev_arrow = Line(lbl_fev1.get_left() + LEFT * 0.08, p1 + RIGHT * 0.10, color=YELLOW, stroke_width=2.4)
        self.play(
            Create(v1_line),
            FadeIn(d1),
            FadeIn(fev_arrow),
            FadeIn(lbl_fev1),
            t_spi.animate.set_value(4.5),
            run_time=3.5,
            rate_func=linear,
        )

        self.at("FVC")
        fvc_line = DashedLine(plot.pt(0.0, 3.0), plot.pt(6.0, 3.0), color=CYAN, stroke_width=3.5, dash_length=0.12)
        lbl_fvc = T("FVC 3.0 L", size=24, color=CYAN).move_to([5.25, 1.98, 0])
        self.play(Create(fvc_line), FadeIn(lbl_fvc), t_spi.animate.set_value(6.0), run_time=2.5, rate_func=linear)

        self.at("volunteer")
        self.wait(0.2)

        self.at("The ratio")
        r_val = ValueTracker(0.01)
        r_bar = make_ratio_bar(
            x0=2.40,
            x1=6.05,
            y=-2.55,
            val_trk=r_val,
            limit=0.68,
            max_v=1.0,
            limit_label="limit 0.68 (made-up)",
            bar_label_fn=lambda v: f"FEV1/FVC = {v:.2f}",
        )
        self.play(FadeIn(r_bar), run_time=0.4)
        self.play(r_val.animate.set_value(0.50), run_time=4.2, rate_func=smooth)

        self.at("Obstructive")
        obs = boxed_label("obstructive", RED, size=24).move_to([5.05, 0.85, 0])
        self.play(FadeIn(obs, scale=1.06), run_time=0.55)
        self.finish()


class S07Idea(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.06, p_init=-5.0, flow=0.0, surf=1.0)
        dim_spi = VGroup(
            plot,
            plot.curve(VOL1_V, color=WHITE, width=6),
            DashedLine(plot.pt(1.0, 0.0), plot.pt(1.0, 1.5), color=YELLOW, stroke_width=3.5),
            DashedLine(plot.pt(0.0, 3.0), plot.pt(6.0, 3.0), color=CYAN, stroke_width=3.5),
            spiro_tag("volunteer 1 (made-up)"),
        )
        set_open_curve_opacity(dim_spi, 0.30)
        theta, drv = attach_quiet_breathing(world, gauge, theta_start=0.0, speed=1.45)
        self.add(dim_spi, gauge, world, drv)

        self.at("one idea")
        head = T("The one idea", size=34, color=GOLD).move_to([-2.0, 3.12, 0])
        self.play(FadeIn(head), run_time=0.55)

        self.at("pays for")
        lbl_rec = T("recoil", size=28, color=ORANGE).move_to([0.05, -1.55, 0], aligned_edge=LEFT)
        lbl_res = T("resistance", size=28, color=WHITE).move_to([0.05, 1.05, 0], aligned_edge=LEFT)
        b1 = always_redraw(lambda: Line(gauge.gauge_right_point(), lbl_rec.get_left() + LEFT * 0.14, color=CYAN, stroke_width=2.8))
        b2 = always_redraw(lambda: Line(gauge.gauge_right_point(), lbl_res.get_left() + LEFT * 0.14, color=CYAN, stroke_width=2.8))
        b1.layout_ok = "covered"
        b2.layout_ok = "covered"

        self.at("recoil")
        self.play(Create(b1), FadeIn(lbl_rec), run_time=0.6)

        self.at("moving air")
        self.play(Create(b2), FadeIn(lbl_res), run_time=0.6)

        self.at("Disease changes")
        sub = T("disease: recoil or resistance", size=28, color=TEXT).move_to([-1.8, -3.02, 0])
        self.play(FadeIn(sub), world.recoil_trk.animate.set_value(1.55), run_time=0.6)
        self.play(world.recoil_trk.animate.set_value(0.55), run_time=0.55)
        self.play(world.recoil_trk.animate.set_value(1.0), run_time=0.4)

        self.at("resistance")
        self.play(world.up_narrow_trk.animate.set_value(1.0), run_time=0.55)
        self.play(world.up_narrow_trk.animate.set_value(0.0), run_time=0.55)
        self.finish()


class S08Emphysema(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.06, p_init=-5.0, flow=0.6, surf=1.0)
        v1_curve = plot.curve(VOL1_V, color=WHITE, width=6)
        v1_fev = DashedLine(plot.pt(1.0, 0.0), plot.pt(1.0, 1.5), color=YELLOW, stroke_width=3.5)
        v1_fvc = DashedLine(plot.pt(0.0, 3.0), plot.pt(6.0, 3.0), color=CYAN, stroke_width=3.5)
        tag_old = spiro_tag("volunteer 1 (made-up)")
        r_val = ValueTracker(0.50)
        r_bar = make_ratio_bar(
            x0=2.40, x1=6.05, y=-2.52, val_trk=r_val, limit=0.68, max_v=1.0,
            limit_label="limit 0.68 (made-up)", bar_label_fn=lambda v: f"FEV1/FVC = {v:.2f}",
        )
        spi_all = VGroup(plot, v1_curve, v1_fev, v1_fvc, tag_old, r_bar)
        set_open_curve_opacity(spi_all, 0.30)
        head = T("emphysema: too little recoil", size=30, color=ORANGE).move_to([-2.0, 3.12, 0])

        # Gentle breathing in the first half of s08 so the world stays alive until the forced blow
        theta = ValueTracker(0.0)
        r_mid = ValueTracker(1.06)

        def breath_step(m, dt):
            theta.increment_value(1.6 * dt)
            th = theta.get_value()
            v = 0.5 * (1.0 - np.cos(th))
            world.r_trk.set_value(r_mid.get_value() + 0.12 * v)
            world.flow_trk.set_value(-0.75 * np.sin(th))
            gauge.p_trk.set_value(-5.5 + 1.2 * np.cos(th) - 0.8 * np.sin(th))

        drv = VMobject().add_updater(breath_step)
        self.add(spi_all, gauge, world, head, drv)

        self.at("destroys alveolar walls")
        self.play(
            world.wall_gap_trk.animate.set_value(1.0),
            r_mid.animate.set_value(1.16),
            run_time=1.8,
        )

        self.at("recoil is too little")
        self.play(world.recoil_trk.animate.set_value(0.32), run_time=2.2)

        self.at("Without walls")
        self.play(world.tether_op_trk.animate.set_value(0.0), run_time=2.0)

        # Switch from quiet breathing to forced blow
        self.remove(drv)
        self.at("compress earlier")
        lbl_early = T("compresses\nearlier", size=24, color=RED, line_spacing=0.85).move_to([-0.25, 0.15, 0], aligned_edge=LEFT)
        early_line = always_redraw(lambda: Line(world.pinch_point_right(), lbl_early.get_left() + LEFT * 0.10, color=RED, stroke_width=2.5))
        early_line.layout_ok = "covered"
        self.play(
            gauge.p_trk.animate.set_value(5.0),
            world.squeeze_trk.animate.set_value(0.90),
            world.pinch_y_trk.animate.set_value(0.28),
            world.pinch_trk.animate.set_value(1.0),
            world.r_trk.animate.set_value(0.90),
            world.flow_trk.animate.set_value(0.5),
            FadeIn(early_line),
            FadeIn(lbl_early),
            run_time=1.8,
        )

        self.at("FEV1")
        tag_new = spiro_tag("obstructive pattern", color=RED)
        self.play(
            UpdateFromAlphaFunc(spi_all, lambda m, a: set_open_curve_opacity(m, 0.30 + 0.70 * a)),
            swap(tag_old, tag_new, run_time=0.6),
            run_time=1.2,
        )

        self.at("the ratio falls")
        self.play(r_val.animate.set_value(0.38), run_time=0.65)
        self.play(r_val.animate.set_value(0.50), run_time=0.65)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(
            r=1.12, p_init=-5.0, flow=0.4, surf=1.0, wall_gap=1.0, tether_op=0.0, recoil=0.35
        )
        head_old = T("emphysema: too little recoil", size=30, color=ORANGE).move_to([-2.0, 3.12, 0])
        head_new = T("fibrosis: too much recoil", size=30, color=ORANGE).move_to([-2.0, 3.12, 0])
        self.add(gauge, world, plot, head_old)

        self.play(
            world.wall_gap_trk.animate.set_value(0.0),
            world.tether_op_trk.animate.set_value(1.0),
            world.recoil_trk.animate.set_value(1.0),
            world.r_trk.animate.set_value(1.00),
            swap(head_old, head_new, run_time=0.7),
            run_time=1.3,
        )

        self.at("scarred tissue")
        self.play(world.thick_trk.animate.set_value(1.0), run_time=0.9)

        self.at("too much recoil")
        self.play(world.recoil_trk.animate.set_value(1.50), run_time=0.9)

        self.at("total lung capacity falls")
        old_tlc = DashedVMobject(
            Circle(radius=1.24, stroke_color=GREY, stroke_width=2.5).move_to([LUNG_CX, LUNG_CY, 0]),
            num_dashes=28,
        )
        lbl_tlc = T("TLC falls", size=26, color=RED).move_to([-0.20, -1.75, 0], aligned_edge=LEFT)
        self.play(
            FadeIn(old_tlc),
            world.r_trk.animate.set_value(0.88),
            FadeIn(lbl_tlc),
            run_time=1.1,
        )

        self.at("Does its ratio")
        q_card = question_card("Does FEV1/FVC fall?", y=-3.05, color=WHITE, size=30)
        q_mark = T("?", size=56, color=WHITE).move_to(plot.pt(3.0, 1.75))
        self.play(FadeIn(q_card), FadeIn(q_mark), run_time=0.7)
        self.finish()


def _fibrosis_pause_backdrop():
    gauge, world, plot = build_base_world(
        r=0.84, p_init=-6.5, flow=0.0, surf=1.0, thick=1.0, recoil=1.50
    )
    head = T("fibrosis: too much recoil", size=30, color=ORANGE).move_to([-2.0, 3.12, 0])
    old_tlc = DashedVMobject(
        Circle(radius=1.24, stroke_color=GREY, stroke_width=2.5).move_to([LUNG_CX, LUNG_CY, 0]),
        num_dashes=28,
    )
    lbl_tlc = T("TLC falls", size=26, color=RED).move_to([-0.20, -1.75, 0], aligned_edge=LEFT)
    q_mark = T("?", size=56, color=WHITE).move_to(plot.pt(3.0, 1.75))
    _, drv = attach_quiet_breathing(world, gauge, theta_start=0.5, speed=2.8, r_base=0.78, r_amp=0.10, p_offset=-1.2)
    return VGroup(gauge, world, plot, head, old_tlc, lbl_tlc, q_mark, drv)


class S10Pause(PredictPause):
    QUESTION = "Does FEV1/FVC fall?"
    CARD = {"y": -3.05, "color": WHITE, "size": 30}
    RING_AT = (5.85, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _fibrosis_pause_backdrop()


class S11Answer(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(
            r=0.88, p_init=-7.5, flow=0.0, surf=1.0, thick=1.0, recoil=1.50
        )
        head = T("fibrosis: too much recoil", size=30, color=ORANGE).move_to([-2.0, 3.12, 0])
        old_tlc = DashedVMobject(
            Circle(radius=1.24, stroke_color=GREY, stroke_width=2.5).move_to([LUNG_CX, LUNG_CY, 0]),
            num_dashes=28,
        )
        lbl_tlc = T("TLC falls", size=26, color=RED).move_to([-0.20, -1.75, 0], aligned_edge=LEFT)
        q_old = question_card("Does FEV1/FVC fall?", y=-3.05, color=WHITE, size=30)
        q_mark = T("?", size=56, color=WHITE).move_to(plot.pt(3.0, 1.75))
        self.add(gauge, world, plot, head, old_tlc, lbl_tlc, q_old, q_mark)

        ans_no = T("No.", size=36, color=GREEN, weight=BOLD).move_to([-0.5, -3.05, 0])
        self.play(FadeOut(q_mark), swap(q_old, ans_no, run_time=0.55), run_time=0.65)

        self.at("high recoil")
        self.play(
            gauge.p_trk.animate.set_value(5.0),
            world.squeeze_trk.animate.set_value(0.85),
            world.flow_trk.animate.set_value(2.2),
            world.r_trk.animate.set_value(0.62),
            run_time=1.8,
        )

        self.at("stiff tissue")
        self.play(
            world.pinch_y_trk.animate.set_value(0.78),
            world.pinch_trk.animate.set_value(1.0),
            run_time=1.2,
        )

        self.at("FEV1 and FVC")
        self.play(FadeOut(plot), run_time=0.45)
        bar_scale = ValueTracker(1.0)
        base_y = -1.15

        def mk_bars():
            s = float(bar_scale.get_value())
            h_fev = 2.1 * s
            h_fvc = 2.6 * s
            b1 = Rectangle(width=0.72, height=h_fev, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.40).move_to([2.95, base_y + h_fev / 2, 0])
            b2 = Rectangle(width=0.72, height=h_fvc, stroke_color=CYAN, stroke_width=3.5, fill_color=CYAN, fill_opacity=0.40).move_to([4.15, base_y + h_fvc / 2, 0])
            return VGroup(b1, b2)

        bars = always_redraw(mk_bars)
        l1 = T("FEV1", size=26, color=YELLOW).move_to([2.95, base_y - 0.35, 0])
        l2 = T("FVC", size=26, color=CYAN).move_to([4.15, base_y - 0.35, 0])
        sch = T("schematic", size=22, color=GREY).move_to([3.55, base_y - 0.85, 0])
        self.add(bars, l1, l2, sch)

        self.at("fall together")
        self.play(bar_scale.animate.set_value(0.62), run_time=1.5)

        self.at("ratio is normal or high")
        rat_bar = Rectangle(width=0.68, height=2.25, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.40).move_to([5.40, base_y + 1.125, 0])
        l3 = T("ratio:\nnormal\nor high", size=24, color=GREEN, line_spacing=0.85).move_to([5.40, base_y - 0.72, 0])
        self.play(FadeIn(rat_bar), FadeIn(l3), run_time=0.85)
        self.finish()


class S12Restrictive(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(
            r=0.86, p_init=3.0, flow=0.9, surf=1.0, thick=1.0, recoil=1.50, pinch=1.0, pinch_y=0.78
        )
        head_old = T("fibrosis: too much recoil", size=30, color=ORANGE).move_to([-2.0, 3.12, 0])
        stamp = boxed_label("restrictive", RED, size=28).move_to([-0.90, 3.12, 0])
        self.add(gauge, world, head_old)

        self.at("restrictive pattern")
        self.play(swap(head_old, stamp, run_time=0.65), world.r_trk.animate.set_value(0.70), run_time=3.5)

        self.at("gas that never leaves")
        lbl_core = T("never leaves", size=24, color=BLUE).move_to([-0.15, -1.70, 0], aligned_edge=LEFT)
        core_line = always_redraw(lambda: Line([LUNG_CX + 0.25, LUNG_CY - 0.15, 0], lbl_core.get_left() + LEFT * 0.10, color=BLUE, stroke_width=2.4))
        core_line.layout_ok = "covered"
        self.play(
            world.r_trk.animate.set_value(0.60),
            world.core_trk.animate.set_value(1.0),
            world.flow_trk.animate.set_value(0.0),
            FadeIn(core_line),
            FadeIn(lbl_core),
            run_time=2.2,
        )

        self.at("volunteer")
        plot = make_spirogram(y_shift=0.30)
        t_spi = ValueTracker(0.0)
        tag = spiro_tag("volunteer 2 (made-up)").shift(UP * 0.14)
        live = plot.live_curve(VOL2_V, t_spi, color=WHITE, width=6)
        dot = plot.dot(lambda: t_spi.get_value(), lambda: VOL2_V(t_spi.get_value()), color=WHITE, ring=CYAN, radius=0.07)
        self.play(FadeIn(plot), FadeIn(tag), run_time=0.35)
        self.add(live, dot)
        self.play(t_spi.animate.set_value(6.0), run_time=1.35, rate_func=linear)

        d1 = Dot(plot.pt(1.0, 2.2), radius=0.08, color=YELLOW)
        lbl_f1 = T("FEV1 2.2 L", size=24, color=YELLOW).move_to([3.80, 0.75, 0])
        fvc_ln = DashedLine(plot.pt(0.0, 2.6), plot.pt(6.0, 2.6), color=CYAN, stroke_width=3.5)
        lbl_f2 = T("FVC 2.6 L", size=24, color=CYAN).move_to([5.30, 1.98, 0])

        r_val = ValueTracker(0.01)
        r_bar = make_ratio_bar(
            x0=2.40, x1=6.05, y=-2.18, val_trk=r_val, limit=0.68, max_v=1.0,
            limit_label="limit 0.68", bar_label_fn=lambda v: f"FEV1/FVC = {v:.2f}" + (" (within limits)" if v >= 0.68 else ""),
        )
        self.play(FadeIn(d1), FadeIn(lbl_f1), Create(fvc_ln), FadeIn(lbl_f2), FadeIn(r_bar), run_time=0.40)
        self.play(r_val.animate.set_value(0.85), run_time=0.65)

        self.at("body box")
        box_rect = Rectangle(width=2.95, height=4.85, stroke_color=GREY, stroke_width=4.5, fill_opacity=0).move_to([LUNG_CX, 0.0, 0])
        lbl_box = T("body box", size=26, color=GREY).move_to([LUNG_CX - 1.05, 2.76, 0])
        tlc_val = ValueTracker(0.1)
        tlc_bar = make_ratio_bar(
            x0=2.40, x1=6.05, y=-3.26, val_trk=tlc_val, limit=4.6, max_v=6.0,
            limit_label="limit 4.6 L (made-up)", bar_label_fn=lambda v: f"TLC = {v:.1f} L",
        )
        self.play(Create(box_rect), FadeIn(lbl_box), FadeIn(tlc_bar), run_time=0.6)
        self.play(tlc_val.animate.set_value(3.9), run_time=1.35)
        self.finish()


class S13Rds(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(
            r=1.06, p_init=-5.0, flow=0.0, surf=1.0, scale=1.0
        )
        head = T("RDS: too much surface recoil", size=30, color=RED).move_to([-1.2, 3.12, 0])
        self.add(gauge, world, head)

        # Continuous newborn shallow rapid breathing until the deep negative swing
        theta = ValueTracker(0.0)

        def nb_breath(m, dt):
            theta.increment_value(2.6 * dt)
            th = theta.get_value()
            v = 0.5 * (1.0 - np.cos(th))
            world.r_trk.set_value(0.88 + 0.14 * v)
            world.flow_trk.set_value(-0.90 * np.sin(th))
            gauge.p_trk.set_value(-6.0 + 1.5 * np.cos(th) - 1.0 * np.sin(th))

        drv = VMobject().add_updater(nb_breath)
        self.add(drv)

        self.at("newborn")
        self.play(world.scale_trk.animate.set_value(0.76), run_time=0.55)

        self.at("enough surfactant")
        self.play(world.surf_trk.animate.set_value(0.05), run_time=1.8)

        self.at("too much surface recoil")
        self.play(world.recoil_trk.animate.set_value(1.55), run_time=1.8)

        self.remove(drv)
        self.at("large negative swing")
        lbl_ret = T("retractions", size=28, color=GREY).move_to([-0.15, -0.55, 0], aligned_edge=LEFT)
        lbl_cls = T("alveoli close", size=28, color=RED).move_to([-0.15, -1.65, 0], aligned_edge=LEFT)

        self.play(
            gauge.p_trk.animate.set_value(-9.8),
            world.retract_trk.animate.set_value(1.0),
            world.r_trk.animate.set_value(1.06),
            world.flow_trk.animate.set_value(-1.1),
            run_time=2.0,
        )

        self.at("soft chest wall inward")
        self.play(FadeIn(lbl_ret), run_time=0.6)
        self.play(
            gauge.p_trk.animate.set_value(-3.5),
            world.retract_trk.animate.set_value(0.0),
            world.r_trk.animate.set_value(0.74),
            world.flow_trk.animate.set_value(0.8),
            run_time=1.8,
        )

        self.at("alveoli close")
        self.play(
            world.collapse_trk.animate.set_value(1.0),
            world.flow_trk.animate.set_value(0.0),
            FadeIn(lbl_cls),
            run_time=0.9,
        )
        self.play(
            gauge.p_trk.animate.set_value(-9.5),
            world.collapse_trk.animate.set_value(0.0),
            world.retract_trk.animate.set_value(0.9),
            world.r_trk.animate.set_value(0.98),
            world.flow_trk.animate.set_value(-1.0),
            run_time=1.0,
        )
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        gauge, world, plot = build_base_world(r=1.06, p_init=-5.0, flow=0.0, surf=1.0, scale=1.0)
        theta, drv = attach_quiet_breathing(world, gauge, theta_start=0.0, speed=1.45)
        self.add(gauge, world, plot, drv)

        self.at("pays for")
        lbl_rec = T("recoil", size=28, color=ORANGE).move_to([0.05, -0.95, 0], aligned_edge=LEFT)
        lbl_res = T("resistance", size=28, color=WHITE).move_to([0.05, 1.52, 0], aligned_edge=LEFT)
        b1 = always_redraw(lambda: Line(gauge.gauge_right_point(), lbl_rec.get_left() + LEFT * 0.14, color=CYAN, stroke_width=2.8))

        def _make_b2():
            p0 = gauge.gauge_right_point()
            p_mid = np.array([-3.45, -0.58, 0.0])
            p1 = lbl_res.get_left() + LEFT * 0.14
            return VMobject(color=CYAN, stroke_width=2.8).set_points_as_corners([p0, p_mid, p1])

        b2 = always_redraw(_make_b2)
        b1.layout_ok = "covered"
        b2.layout_ok = "covered"
        self.play(Create(b1), Create(b2), FadeIn(lbl_rec), FadeIn(lbl_res), run_time=0.7)

        t_emp = mchip("emphysema", ORANGE, size=22)
        t_fib = mchip("fibrosis", ORANGE, size=22)
        t_rds = mchip("RDS", ORANGE, size=22)
        rec_tags = VGroup(t_emp, t_fib, t_rds).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([0.05, -2.42, 0], aligned_edge=LEFT)

        self.at("Emphysema")
        self.play(FadeIn(t_emp, shift=LEFT * 0.15), run_time=0.45)
        self.at("fibrosis")
        self.play(FadeIn(t_fib, shift=LEFT * 0.15), run_time=0.45)
        self.at("change the recoil")
        self.play(FadeIn(t_rds, shift=LEFT * 0.15), world.recoil_trk.animate.set_value(1.45), run_time=0.55)
        self.play(world.recoil_trk.animate.set_value(1.0), run_time=0.4)

        t_ast = mchip("asthma", RED, size=22)
        t_cb = mchip("chronic\nbronchitis", RED, size=22)
        res_tags = VGroup(t_ast, t_cb).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([0.05, 0.35, 0], aligned_edge=LEFT)

        self.at("Asthma")
        self.play(FadeIn(t_ast, shift=LEFT * 0.15), run_time=0.30)
        self.at("chronic bronchitis")
        self.play(FadeIn(t_cb, shift=LEFT * 0.15), run_time=0.35)
        self.at("narrow the airways")
        self.play(world.up_narrow_trk.animate.set_value(1.0), run_time=0.6)
        self.play(world.up_narrow_trk.animate.set_value(0.0), run_time=0.6)
        self.finish()


class S15End(EndCard):
    LINE = "Each breath pays for recoil and airflow; disease changes either one."
