"""
COLOUR MAP (one colour per concept for the whole film)
- BG       #0f1117 : dark background (from bp_style)
- GREEN    #83C167 : afferent arteriole, its smooth-muscle tap ring, and A1 receptor wall
- YELLOW   #F5D547 : efferent arteriole and its nozzle
- RED      #FC6255 : plasma flow (plasma dots and broad flow arrow)
- PURPLE   #B589D6 : plasma protein dots (held back by the filter)
- CYAN     #38D9E8 : filtrate drops, tubule lumen/fluid, and autoregulation curve
- BLUE     #58C4DD : Bowman's space band
- MAGENTA  #E066C0 : macula densa cells and ATP / adenosine signal
- PINK     #F28BA8 : renin dots released by afferent wall cells
- GOLD     #D4A843 : glucose dots (diabetes / SGLT2 test)
- ORANGE   #F2994A : push bar from the first film's push-pull strip (s00 only)
- TEXT     #E8EAF0 : all labels, arterial pressure dial, salt (NaCl) specks, Ca specks, signal arrows

CARRIED WORLD
One continuous 16:9 nephron-vascular picture carried across scenes:
- Far left: WHITE arterial pressure dial gauge.
- Middle: GREEN afferent arteriole + tap ring -> straight glomerular capillary -> YELLOW efferent arteriole + nozzle,
  with RED plasma dots, broad RED flow arrow, PURPLE protein dots, pale BLUE Bowman's space beneath, and CYAN filtrate drops.
- From s04 onward: CYAN tubule loop draining Bowman's space, looping along the bottom, rising to touch the
  GREEN afferent ring at the MAGENTA macula densa plaque.

WHAT CHANGES PER SCENE (and what it is computed from)
- s00_link_and_question : Dial needle oscillates sinusoidally (p_art); GREEN/YELLOW rings pulse; RED/PURPLE dots advance with flow; CYAN drops fall steadily.
- s01_title             : Title fades in above the carried world while dial needle continues swinging and drops fall evenly.
- s02_plateau           : Computed autoregulation curve y(p) draws over [20, 215] mmHg; dial needle and curve dot are driven by one p_art tracker swinging [80, 180] mmHg; graph shrinks to icon.
- s03_myogenic          : Zoomed afferent muscle wall radius r(t) bulges outward with rising dial pressure, depolarization wave travels x(t) along muscle, Ca specks brighten, muscle contracts inward and flow normalizes.
- s04_macula_densa      : Full world with CYAN tubule path parameterized over s in [0, 1]; CYAN drops travel along the loop to light up the MAGENTA macula densa and feedback arrow.
- s05_feedback_rule     : Salt speck density in tubule switches high -> low -> mid; GREEN aperture narrows/widens inversely, changing RED flow speed/arrow width and CYAN drop rate; PINK renin puffs out on low salt.
- s06_signal            : Zoomed macula densa cells + A1 wall; WHITE salt specks traverse NKCC2 door, MAGENTA ATP sparks cross gap into rings docking at A1 slots, GREEN wall narrows; zooms out with slower drops.
- s07_idea              : Dial needle swings [80, 180] mmHg; GREEN aperture is computed inversely from p_art so capillary flow and CYAN drop rate stay steady; stretch and salt arrows pulse.
- s08_diabetes_predict  : Dial steady; GOLD glucose dots enter plasma, filter into Bowman's space and tubule, and co-exit with WHITE salt specks through SGLT2 door, thinning salt downstream at macula densa.
- s09_pause             : PredictPause holding question card with 4.5 s countdown ring while drops fall and sparse salt/glucose specks drift in the tubule.
- s10_answer            : GREEN aperture widens; RED arrow and flow broaden; CYAN drop rate increases (hyperfiltration); two open-question tags appear.
- s11_return            : Gold dots and tags fade; dial swings [80, 180] mmHg while GREEN aperture counter-adjusts inversely to hold CYAN drops steady; stretch & salt arrows pulse together.
- s12_end               : Standard EndCard with exact take-home line.
"""

from bp_parts import *

# Extended house palette (one colour per concept)
CYAN = "#38D9E8"
PURPLE = "#B589D6"
MAGENTA = "#E066C0"
PINK = "#F28BA8"
ORANGE = "#F2994A"


# ------------------------------------------------------------------ computed physiology helpers
def autoreg_flow(p):
    """Normalized RBF/GFR curve over perfusion pressure p (mmHg): schematic plateau over 80..180."""
    if p < 80.0:
        # Smooth ramp from 0 around p=15 to ~0.95 at p=80
        t = np.clip((p - 15.0) / 65.0, 0.0, 1.0)
        return 0.95 * (t ** 1.35) * (1.5 - 0.5 * t)
    if p <= 180.0:
        # Nearly flat plateau (slight ~5% rise across 80..180)
        return 0.95 + 0.06 * ((p - 80.0) / 100.0)
    # Steep rise above 180
    return 1.01 + 0.36 * (((p - 180.0) / 40.0) ** 1.25)


def aff_from_pressure(p):
    """Counter-adjusting afferent aperture (1.0 at p=115, narrower at high pressure, wider at low)."""
    return float(np.clip(1.0 - 0.34 * (p - 115.0) / 65.0, 0.62, 1.38))


def tubule_polyline():
    """Rounded schematic tubule centerline from Bowman's space right end to macula densa at (-2.9, -0.15)."""
    pts = []
    # 1. Proximal exit rightward: (2.05, -0.42) -> (4.65, -0.42)
    pts.append(np.array([2.05, -0.42, 0.0]))
    pts.append(np.array([4.65, -0.42, 0.0]))
    # Corner 1
    for a in np.linspace(PI / 2, 0, 8)[1:]:
        pts.append(np.array([4.65 + 0.30 * np.cos(a), -0.72 + 0.30 * np.sin(a), 0.0]))
    # 2. Descending limb on right: y = -0.72 -> -2.05
    pts.append(np.array([4.95, -2.05, 0.0]))
    # Corner 2
    for a in np.linspace(0, -PI / 2, 8)[1:]:
        pts.append(np.array([4.65 + 0.30 * np.cos(a), -2.05 + 0.30 * np.sin(a), 0.0]))
    # 3. Bottom loop leftward: (4.65, -2.35) -> (-2.60, -2.35)
    pts.append(np.array([-2.60, -2.35, 0.0]))
    # Corner 3
    for a in np.linspace(-PI / 2, -PI, 8)[1:]:
        pts.append(np.array([-2.60 + 0.30 * np.cos(a), -2.05 + 0.30 * np.sin(a), 0.0]))
    # 4. Thick ascending limb rising to green afferent ring at x = -2.90, y = -0.15
    pts.append(np.array([-2.90, -0.15, 0.0]))
    return np.array(pts)


_TUB_PTS = tubule_polyline()
_TUB_SEGS = np.linalg.norm(np.diff(_TUB_PTS, axis=0), axis=1)
_TUB_CUM = np.concatenate([[0.0], np.cumsum(_TUB_SEGS)])
_TUB_LEN = float(_TUB_CUM[-1])


def tubule_pt(s):
    """Point along tubule centerline for s in [0, 1]."""
    d = float(np.clip(s, 0.0, 1.0)) * _TUB_LEN
    i = int(np.searchsorted(_TUB_CUM, d, side="right")) - 1
    i = max(0, min(i, len(_TUB_PTS) - 2))
    seg = _TUB_SEGS[i]
    f = (d - _TUB_CUM[i]) / seg if seg > 1e-9 else 0.0
    return _TUB_PTS[i] * (1.0 - f) + _TUB_PTS[i + 1] * f


def tubule_tangent(s):
    """Unit tangent along tubule at s in [0, 1]."""
    ds = 0.004
    p1 = tubule_pt(max(0.0, s - ds))
    p2 = tubule_pt(min(1.0, s + ds))
    v = p2 - p1
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else RIGHT


# ------------------------------------------------------------------ carried world builder
class NephronWorld:
    """Builds the shared 16:9 nephron-vascular stage with ValueTracker-driven physiological motion."""

    def __init__(self, p_init=110.0, aff_init=1.0, flow_init=1.0, gfr_init=1.0,
                 with_tubule=False, with_macula=False, dim_efferent=False,
                 salt_mode="none", glucose_mode="none", sglt2_open=False,
                 y_offset=0.0, seed=7):
        self.rng = np.random.default_rng(seed)
        self.y_off = y_offset
        self.p_art = ValueTracker(p_init)
        self.aff_open = ValueTracker(aff_init)
        self.flow_rate = ValueTracker(flow_init)
        self.gfr_rate = ValueTracker(gfr_init)
        self.salt_rate = ValueTracker(1.0 if salt_mode == "normal" else (1.8 if salt_mode == "high" else (0.35 if salt_mode == "low" else 0.0)))
        self.macula_glow = ValueTracker(0.0)
        self.macula_alpha = ValueTracker(1.0 if with_macula else 0.0)
        self.glucose_alpha = ValueTracker(1.0 if glucose_mode == "high" else 0.0)
        self.sglt2_frac = ValueTracker(1.0 if sglt2_open else 0.0)
        self.salt_mode = salt_mode
        self.glucose_mode = glucose_mode
        self.sglt2_open = sglt2_open

        self.root = VGroup()
        self.y_vessel = 0.38 + y_offset

        # 1. Arterial pressure dial (far left)
        self.dial_c = np.array([-5.35, 0.35 + y_offset, 0.0])
        self.dial_r = 0.85
        self.dial_group = self._build_dial()
        self.root.add(self.dial_group)

        # 2. Bowman's space band (behind capillary drops)
        self.bowman_box = RoundedRectangle(
            corner_radius=0.22, width=4.25, height=0.82,
            stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.16
        ).move_to([0.10, self.y_vessel - 0.78, 0.0])
        self.bowman_label = T("Bowman's space", 26, TEXT).next_to(self.bowman_box, DOWN, buff=0.14)
        self.root.add(self.bowman_box, self.bowman_label)

        # 3. Tubule (optional)
        self.tubule_group = VGroup()
        if with_tubule:
            self._build_tubule(with_macula=with_macula)
            self.root.add(self.tubule_group)

        # 4. Blood vessels (afferent GREEN, capillary, efferent YELLOW) + tap ring + nozzle + flow arrow
        self._build_vessels(dim_efferent=dim_efferent)

        # 5. Dynamic particle layers (blood plasma, protein, filtrate drops, tubule drops, salt, glucose)
        self._build_particles(with_tubule=with_tubule)

        # 6. Schematic tag (always bottom right)
        self.schematic = scope_tag("schematic", size=24, color=TEXT)
        self.root.add(self.schematic)

    def _dial_angle(self, p):
        frac = np.clip((p - 40.0) / 180.0, 0.0, 1.0)
        return PI - PI * frac

    def _build_dial(self):
        c, r = self.dial_c, self.dial_r
        track = Arc(radius=r, start_angle=PI, angle=-PI, arc_center=c, stroke_color=TEXT, stroke_width=5)
        # Subtle ticks at 80 and 180 mmHg on the dial rim
        ticks = VGroup()
        for p in (80.0, 130.0, 180.0):
            ang = self._dial_angle(p)
            p_in = c + (r - 0.12) * np.array([np.cos(ang), np.sin(ang), 0.0])
            p_out = c + (r + 0.05) * np.array([np.cos(ang), np.sin(ang), 0.0])
            ticks.add(Line(p_in, p_out, color=TEXT, stroke_width=2.5))
        hub = Dot(c, radius=0.07, color=TEXT)
        needle = always_redraw(lambda: Line(
            c,
            c + 0.76 * r * np.array([
                np.cos(self._dial_angle(self.p_art.get_value())),
                np.sin(self._dial_angle(self.p_art.get_value())),
                0.0,
            ]),
            color=TEXT, stroke_width=5
        ))
        lbl = T("arterial\npressure", 24, TEXT, line_spacing=0.85).move_to(c + DOWN * 0.56)
        return VGroup(track, ticks, hub, needle, lbl)

    def _build_vessels(self, dim_efferent=False):
        yv = self.y_vessel
        # Afferent vessel walls (-4.25 .. -1.95) driven by aff_open
        def mk_aff():
            ap = self.aff_open.get_value()
            half_h = 0.22 * ap
            fill = Rectangle(width=2.30, height=2 * half_h, stroke_width=0, fill_color=GREEN, fill_opacity=0.14).move_to([-3.10, yv, 0])
            top = Line([-4.25, yv + half_h, 0], [-1.95, yv + half_h, 0], color=GREEN, stroke_width=6)
            bot = Line([-4.25, yv - half_h, 0], [-1.95, yv - half_h, 0], color=GREEN, stroke_width=6)
            # Tap ring (smooth muscle cuff at x = -2.90)
            ring_top = RoundedRectangle(corner_radius=0.07, width=0.58, height=0.18, stroke_color=GREEN, stroke_width=3,
                                        fill_color=GREEN, fill_opacity=0.55).move_to([-2.90, yv + half_h + 0.11, 0])
            ring_bot = RoundedRectangle(corner_radius=0.07, width=0.58, height=0.18, stroke_color=GREEN, stroke_width=3,
                                        fill_color=GREEN, fill_opacity=0.55).move_to([-2.90, yv - half_h - 0.11, 0])
            return VGroup(fill, top, bot, ring_top, ring_bot)

        self.afferent = always_redraw(mk_aff)

        # Glomerular capillary (-1.95 .. +2.15), straight across middle
        cap_fill = Rectangle(width=4.10, height=0.66, stroke_width=0, fill_color=RED, fill_opacity=0.10).move_to([0.10, yv, 0])
        cap_top = Line([-1.95, yv + 0.33, 0], [2.15, yv + 0.33, 0], color=TEXT, stroke_width=5)
        # Bottom porous filtration barrier (dashed segments)
        cap_bot = DashedLine([-1.95, yv - 0.33, 0], [2.15, yv - 0.33, 0], color=TEXT, stroke_width=4, dash_length=0.20)
        self.capillary = VGroup(cap_fill, cap_top, cap_bot)

        # Efferent arteriole (+2.15 .. +4.75) + yellow nozzle
        eff_op = 0.45 if dim_efferent else 1.0
        eff_fill = Rectangle(width=2.60, height=0.40, stroke_width=0, fill_color=YELLOW, fill_opacity=0.12 * eff_op).move_to([3.45, yv, 0])
        eff_top = Line([2.15, yv + 0.20, 0], [4.75, yv + 0.20, 0], color=YELLOW, stroke_width=5, stroke_opacity=eff_op)
        eff_bot = Line([2.15, yv - 0.20, 0], [4.75, yv - 0.20, 0], color=YELLOW, stroke_width=5, stroke_opacity=eff_op)
        noz_top = RoundedRectangle(corner_radius=0.06, width=0.46, height=0.16, stroke_color=YELLOW, stroke_width=3,
                                   fill_color=YELLOW, fill_opacity=0.48 * eff_op).set_stroke(opacity=eff_op).move_to([3.10, yv + 0.29, 0])
        noz_bot = RoundedRectangle(corner_radius=0.06, width=0.46, height=0.16, stroke_color=YELLOW, stroke_width=3,
                                   fill_color=YELLOW, fill_opacity=0.48 * eff_op).set_stroke(opacity=eff_op).move_to([3.10, yv - 0.29, 0])
        self.efferent = VGroup(eff_fill, eff_top, eff_bot, noz_top, noz_bot)

        # Broad RED flow arrow above inflow (thickness responds to flow_rate)
        def mk_arrow():
            fr = float(np.clip(self.flow_rate.get_value(), 0.45, 1.65))
            sw = 7.0 * fr
            arr = Arrow([-4.15, yv + 0.72, 0], [-2.15, yv + 0.72, 0], buff=0,
                        color=RED, stroke_width=sw, max_tip_length_to_length_ratio=0.22)
            return arr

        self.flow_arrow = always_redraw(mk_arrow)
        self.root.add(self.afferent, self.capillary, self.efferent, self.flow_arrow)

    def _build_tubule(self, with_macula=False):
        shift = UP * self.y_off
        # Compute left and right wall offsets along centerline
        left_pts, right_pts = [], []
        half_w = 0.18
        for i in range(len(_TUB_PTS)):
            p = _TUB_PTS[i]
            p_prev = _TUB_PTS[max(0, i - 1)]
            p_next = _TUB_PTS[min(len(_TUB_PTS) - 1, i + 1)]
            t = p_next - p_prev
            nrm = np.linalg.norm(t)
            t = t / nrm if nrm > 1e-9 else RIGHT
            perp = np.array([-t[1], t[0], 0.0])
            left_pts.append(p + perp * half_w)
            right_pts.append(p - perp * half_w)

        wall_l = VMobject(stroke_color=CYAN, stroke_width=4, fill_opacity=0).set_points_as_corners(left_pts)
        wall_r = VMobject(stroke_color=CYAN, stroke_width=4, fill_opacity=0).set_points_as_corners(right_pts)
        lumen_poly = Polygon(*(left_pts + right_pts[::-1]), stroke_width=0, fill_color=CYAN, fill_opacity=0.13)
        self.tubule_walls = VGroup(lumen_poly, wall_l, wall_r).shift(shift)
        self.tubule_group.add(self.tubule_walls)

        # SGLT2 door on proximal descending limb (x ~ 4.95, y ~ -1.38)
        if self.sglt2_open or self.glucose_mode != "none":
            def mk_sglt2():
                op = self.sglt2_frac.get_value()
                if op < 0.02:
                    return VGroup()
                door_bg = Rectangle(width=0.22, height=0.42, stroke_width=0, fill_color=BG, fill_opacity=op).move_to([5.13, -1.38 + self.y_off, 0])
                door_top = Line([4.95, -1.17 + self.y_off, 0], [5.28, -1.17 + self.y_off, 0], color=GOLD, stroke_width=4).set_stroke(opacity=op)
                door_bot = Line([4.95, -1.59 + self.y_off, 0], [5.28, -1.59 + self.y_off, 0], color=GOLD, stroke_width=4).set_stroke(opacity=op)
                return VGroup(door_bg, door_top, door_bot)
            self.sglt2_door = always_redraw(mk_sglt2)
            self.tubule_group.add(self.sglt2_door)

        # Macula densa plaque at ascending limb near green ring (x = -2.90, y = -0.58 .. -0.18)
        self.macula_cells = VGroup()
        for k in range(3):
            cy = -0.22 - k * 0.22 + self.y_off
            cell = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.18, stroke_color=MAGENTA,
                                    stroke_width=2.5, fill_color=MAGENTA, fill_opacity=0.65).move_to([-2.72, cy, 0])
            self.macula_cells.add(cell)
        if not with_macula:
            self.macula_cells.set_opacity(0.0)
        else:
            def upd_mac(mob):
                a = self.macula_alpha.get_value()
                g = self.macula_glow.get_value()
                for c in mob:
                    c.set_fill(opacity=(0.65 + 0.35 * g) * a)
                    c.set_stroke(width=2.5 + 2.5 * g, opacity=a)
            self.macula_cells.add_updater(upd_mac)
            upd_mac(self.macula_cells)
        self.tubule_group.add(self.macula_cells)

    def _build_particles(self, with_tubule=False):
        yv = self.y_vessel
        # RED plasma dots (22 dots flowing x = -4.2 .. +4.7)
        self.plasma_dots = VGroup()
        for i in range(22):
            d = Dot(radius=0.062, color=RED)
            d._x = -4.2 + (i / 22.0) * 8.9
            d._yr = float(self.rng.uniform(-0.7, 0.7))

            def upd_p(mob, dt):
                fr = float(np.clip(self.flow_rate.get_value(), 0.3, 1.8))
                mob._x += dt * 1.9 * fr
                if mob._x > 4.72:
                    mob._x -= 8.92
                if mob._x < -1.95:
                    hh = 0.16 * self.aff_open.get_value()
                elif mob._x < 2.15:
                    hh = 0.26
                else:
                    hh = 0.14
                mob.move_to([mob._x, yv + mob._yr * hh, 0])

            d.add_updater(upd_p)
            upd_p(d, 0.0)
            self.plasma_dots.add(d)

        # PURPLE protein dots (10 larger dots staying inside capillary)
        self.protein_dots = VGroup()
        for i in range(10):
            d = Dot(radius=0.068, color=PURPLE)
            d._x = -4.0 + (i / 10.0) * 8.7
            d._yr = float(self.rng.uniform(-0.6, 0.6))

            def upd_prot(mob, dt):
                fr = float(np.clip(self.flow_rate.get_value(), 0.3, 1.8))
                mob._x += dt * 1.45 * fr
                if mob._x > 4.70:
                    mob._x -= 8.70
                if mob._x < -1.95:
                    hh = 0.14 * self.aff_open.get_value()
                elif mob._x < 2.15:
                    hh = 0.24
                else:
                    hh = 0.12
                mob.move_to([mob._x, yv + mob._yr * hh, 0])

            d.add_updater(upd_prot)
            upd_prot(d, 0.0)
            self.protein_dots.add(d)

        # CYAN filtrate drops falling from capillary bottom into Bowman's space
        self.filtrate_drops = VGroup()
        for i in range(9):
            d = Dot(radius=0.065, color=CYAN)
            d._x = -1.65 + (i / 8.0) * 3.40
            d._phase = (i * 0.37) % 1.0

            def upd_drop(mob, dt):
                gr = float(np.clip(self.gfr_rate.get_value(), 0.25, 2.2))
                mob._phase = (mob._phase + dt * 0.72 * gr) % 1.0
                y = (yv - 0.34) - mob._phase * 0.74
                op = 1.0 if mob._phase < 0.78 else (1.0 - mob._phase) / 0.22
                mob.move_to([mob._x, y, 0]).set_opacity(float(np.clip(op, 0.0, 1.0)))

            d.add_updater(upd_drop)
            upd_drop(d, 0.0)
            self.filtrate_drops.add(d)

        self.root.add(self.plasma_dots, self.protein_dots, self.filtrate_drops)

        if with_tubule:
            # CYAN tubule drops flowing along s in [0, 1]
            self.tubule_drops = VGroup()
            for i in range(16):
                d = Dot(radius=0.070, color=CYAN)
                d._s = i / 16.0
                d._off = float(self.rng.uniform(-0.07, 0.07))

                def upd_td(mob, dt):
                    gr = float(np.clip(self.gfr_rate.get_value(), 0.3, 2.0))
                    mob._s = (mob._s + dt * 0.11 * gr) % 1.0
                    p = tubule_pt(mob._s) + UP * self.y_off
                    t = tubule_tangent(mob._s)
                    perp = np.array([-t[1], t[0], 0.0])
                    mob.move_to(p + perp * mob._off)

                d.add_updater(upd_td)
                upd_td(d, 0.0)
                self.tubule_drops.add(d)
            self.root.add(self.tubule_drops)

            # WHITE salt specks (if salt_mode != 'none')
            self.salt_specks = VGroup()
            if self.salt_mode != "none":
                for i in range(28):
                    sp = Dot(radius=0.036, color=TEXT)
                    sp._s = (i / 28.0 + 0.015) % 1.0
                    sp._off = float(self.rng.uniform(-0.09, 0.09))
                    sp._idx = i

                    def upd_salt(mob, dt):
                        sr = self.salt_rate.get_value()
                        gr = float(np.clip(self.gfr_rate.get_value(), 0.4, 1.8))
                        mob._s = (mob._s + dt * 0.11 * gr) % 1.0
                        # Visibility depends on salt_rate and SGLT2 depletion
                        if sr <= 0.01:
                            mob.set_opacity(0.0)
                            return
                        keep_frac = np.clip(sr / 1.8, 0.18, 1.0)
                        sglt2_on = self.sglt2_frac.get_value() > 0.5
                        if sglt2_on and mob._s > 0.32:
                            # 75% of salt specks absorbed through SGLT2 in diabetes test
                            visible = (mob._idx % 4 == 0)
                        else:
                            visible = (mob._idx / 28.0) <= keep_frac
                        # If sglt2_open, some specks divert outward at s ~ 0.25..0.34
                        p = tubule_pt(mob._s) + UP * self.y_off
                        t = tubule_tangent(mob._s)
                        perp = np.array([-t[1], t[0], 0.0])
                        if sglt2_on and (mob._idx % 4 != 0) and 0.24 < mob._s < 0.35:
                            frac_out = (mob._s - 0.24) / 0.11
                            mob.move_to(p + RIGHT * (0.15 + 0.75 * frac_out))
                            mob.set_opacity(float(1.0 - frac_out))
                        else:
                            mob.move_to(p + perp * mob._off)
                            mob.set_opacity(0.95 if visible else 0.0)

                    sp.add_updater(upd_salt)
                    upd_salt(sp, 0.0)
                    self.salt_specks.add(sp)
                self.root.add(self.salt_specks)

            # GOLD glucose dots (diabetes / predict / answer)
            self.glucose_dots = VGroup()
            if self.glucose_mode != "none":
                # Plasma + filtered glucose dots
                for i in range(14):
                    gd = Dot(radius=0.052, color=GOLD)
                    gd._phase = i / 14.0
                    gd._lane = i % 3

                    def upd_gl_p(mob, dt):
                        ga = self.glucose_alpha.get_value()
                        fr = float(np.clip(self.flow_rate.get_value(), 0.4, 1.8))
                        mob._phase = (mob._phase + dt * 0.22 * fr) % 1.0
                        if mob._lane == 0:
                            # Stays in blood
                            x = -4.2 + mob._phase * 8.9
                            hh = 0.16 * self.aff_open.get_value() if x < -1.95 else (0.24 if x < 2.15 else 0.12)
                            mob.move_to([x, yv + (0.06 if mob._phase > 0.5 else -0.06) * hh / 0.16, 0])
                            mob.set_opacity(0.95 * ga)
                        else:
                            # Enters capillary, drops into Bowman's space -> tubule start
                            if mob._phase < 0.35:
                                x = -4.2 + (mob._phase / 0.35) * 4.5
                                mob.move_to([x, yv - 0.06, 0]).set_opacity(0.95 * ga)
                            elif mob._phase < 0.65:
                                f = (mob._phase - 0.35) / 0.30
                                mob.move_to([0.3 + f * 1.4, (yv - 0.1) - f * 0.75, 0]).set_opacity(0.95 * ga)
                            else:
                                f = (mob._phase - 0.65) / 0.35
                                mob.move_to(tubule_pt(f * 0.22) + UP * self.y_off).set_opacity(0.95 * (1.0 - 0.5 * f) * ga)

                    gd.add_updater(upd_gl_p)
                    upd_gl_p(gd, 0.0)
                    self.glucose_dots.add(gd)

                # Proximal tubule glucose exiting via SGLT2 door
                for i in range(8):
                    gt = Dot(radius=0.052, color=GOLD)
                    gt._s = (i / 8.0) * 0.34

                    def upd_gl_t(mob, dt):
                        ga = self.glucose_alpha.get_value()
                        gr = float(np.clip(self.gfr_rate.get_value(), 0.4, 1.8))
                        mob._s = (mob._s + dt * 0.11 * gr) % 0.36
                        p = tubule_pt(mob._s) + UP * self.y_off
                        if self.sglt2_frac.get_value() > 0.5 and mob._s > 0.24:
                            f = (mob._s - 0.24) / 0.12
                            mob.move_to(p + RIGHT * (0.14 + 0.75 * f)).set_opacity(float((1.0 - f) * ga))
                        else:
                            mob.move_to(p).set_opacity(0.95 * ga)

                    gt.add_updater(upd_gl_t)
                    upd_gl_t(gt, 0.0)
                    self.glucose_dots.add(gt)
                self.root.add(self.glucose_dots)


# ------------------------------------------------------------------ Scene 00
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        w = NephronWorld(p_init=115.0)
        # First film's push-pull strip faintly above the capillary
        push_bar = Rectangle(width=3.6, height=0.14, stroke_width=0, fill_color=ORANGE, fill_opacity=0.45).move_to([0.1, 1.38, 0])
        pull_bar = Rectangle(width=3.6, height=0.14, stroke_width=0, fill_color=PURPLE, fill_opacity=0.45).move_to([0.1, 1.18, 0])
        strip = VGroup(push_bar, pull_bar)
        self.add(w.root, strip)

        # On 'Two tiny arterioles', pulse green ring then yellow ring
        self.at("Two tiny arterioles")
        g_ring = Circle(radius=0.52, color=GREEN, stroke_width=6).move_to([-2.90, w.y_vessel, 0])
        y_ring = Circle(radius=0.46, color=YELLOW, stroke_width=6).move_to([3.10, w.y_vessel, 0])
        self.play(ShowPassingFlash(g_ring, time_width=0.6), run_time=0.8)
        self.play(ShowPassingFlash(y_ring, time_width=0.6), run_time=0.8)

        # Fade out first film's push-pull strip before arterial pressure beat
        self.play(FadeOut(strip), run_time=0.8)

        # On 'changes', arterial dial needle starts swinging slowly up and down
        self.at("changes")
        t_sw = [0.0]

        def swing_p(mob, dt):
            t_sw[0] += dt
            mob.set_value(125.0 + 42.0 * np.sin(1.45 * t_sw[0]))

        w.p_art.add_updater(swing_p)
        self.add(w.p_art)

        # On 'How does filtration', white text across top
        self.at("How does filtration")
        q = T("Steady filtration?", 38, TEXT).move_to([0.0, 2.85, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 01 (2.0s silent title)
class S01Title(NarratedScene):
    def construct(self):
        w = NephronWorld(p_init=125.0)
        t_sw = [1.8]
        w.p_art.add_updater(lambda mob, dt: (t_sw.__setitem__(0, t_sw[0] + dt), mob.set_value(125.0 + 42.0 * np.sin(1.45 * t_sw[0]))))
        self.add(w.p_art)

        q = T("Steady filtration?", 38, TEXT).move_to([0.0, 2.85, 0])
        title = T("Stretch, Salt and a Steady Filter", 44, TEXT, font=TITLE_FONT).move_to([0.0, 2.65, 0])
        fit(title, max_w=11.8)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.22)
        self.add(w.root, q)

        self.play(
            Succession(
                FadeOut(q, run_time=0.35),
                AnimationGroup(FadeIn(title, shift=UP * 0.08), GrowFromCenter(rule), run_time=0.55)
            )
        )
        self.finish()


# ------------------------------------------------------------------ Scene 02
class S02Plateau(SpokenScene):
    def construct(self):
        # Carried world shifted smoothly down to make room for the graph above
        w = NephronWorld(p_init=125.0, y_offset=-1.15)
        t_sw = [4.0]
        swing_mode = ["free"]

        def upd_dial(mob, dt):
            t_sw[0] += dt
            if swing_mode[0] == "free":
                mob.set_value(125.0 + 42.0 * np.sin(1.15 * t_sw[0]))
            else:
                # Sweep cleanly between 80 and 180 mmHg
                mob.set_value(130.0 + 50.0 * np.sin(0.95 * t_sw[0]))

        w.p_art.add_updater(upd_dial)
        self.add(w.p_art, w.root)

        # Build the autoregulation plot in the upper space
        P = Plot(box=(-3.2, 4.9, 1.05, 3.15), xr=(0, 220), yr=(0, 1.45),
                 xticks=[80, 180], yticks=[],
                 xlabel="perfusion pressure (mmHg)", ylabel="flow and filtration",
                 color=TEXT, size=24, label_size=26)
        self.play(Create(P.axes), FadeIn(P.xlabel), FadeIn(P.ylabel), run_time=1.0)

        self.at("perfusion pressures")
        v80 = P.vline(80, color=TEXT, dashed=True).set_stroke(opacity=0.45)
        v180 = P.vline(180, color=TEXT, dashed=True).set_stroke(opacity=0.45)
        self.play(FadeIn(P.ticks), FadeIn(P.tick_labels), Create(v80), Create(v180), run_time=0.9)

        self.at("On a graph")
        swing_mode[0] = "plateau"
        t_curve = ValueTracker(20.0)
        live = P.live_curve(autoreg_flow, t_curve, color=CYAN, width=6, x0=20.0)
        self.add(live)
        self.play(t_curve.animate.set_value(210.0), run_time=2.4, rate_func=linear)
        curve_done = P.curve(autoreg_flow, x0=20.0, x1=210.0, color=CYAN, width=6)
        self.remove(live)
        self.add(curve_done)

        # White dot riding along the flat part in exact step with the dial needle
        dot = P.dot(lambda: float(np.clip(w.p_art.get_value(), 20.0, 210.0)),
                    lambda: autoreg_flow(float(np.clip(w.p_art.get_value(), 20.0, 210.0))),
                    color=TEXT, ring=CYAN, radius=0.11)
        self.add(dot)

        self.at("autoregulation")
        auto_lbl = T("autoregulation", 28, TEXT).move_to(P.pt(130, 1.25))
        self.play(FadeIn(auto_lbl, shift=DOWN * 0.08), run_time=0.6)

        self.at("Two mechanisms")
        tag1 = boxed_label("1", color=TEXT, size=24, pad=0.12).move_to([-3.55, w.y_vessel + 0.72, 0])
        tag2 = boxed_label("2", color=TEXT, size=24, pad=0.12).move_to([-2.35, w.y_vessel + 0.72, 0])
        # Avoid touching broad red arrow (y_vessel + 0.72): put tags below green ring at y_vessel - 0.65
        tag1.move_to([-3.35, w.y_vessel - 0.72, 0])
        tag2.move_to([-2.45, w.y_vessel - 0.72, 0])
        self.play(FadeIn(tag1), FadeIn(tag2), run_time=0.6)

        self.at("afferent")
        glow_ring = Circle(radius=0.52, color=GREEN, stroke_width=7).move_to([-2.90, w.y_vessel, 0])
        self.play(ShowPassingFlash(glow_ring, time_width=0.7), run_time=0.9)

        # Hold briefly, then shrink graph axes+curve to a small icon in top-left corner
        rest = self.narration_s - self.elapsed() - 0.9
        if rest > 0.2:
            self.wait(rest)
        icon = VGroup(P.axes.copy(), curve_done.copy())
        self.play(
            FadeOut(VGroup(P.ticks, P.tick_labels, P.xlabel, P.ylabel, v80, v180, auto_lbl, dot), run_time=0.30)
        )
        self.play(
            FadeOut(P.axes, run_time=0.4), FadeOut(curve_done, run_time=0.4),
            icon.animate(run_time=0.7).scale(0.22).move_to([-5.65, 3.05, 0]),
        )
        self.finish()


# ------------------------------------------------------------------ Scene 03
class S03Myogenic(SpokenScene):
    def construct(self):
        # Dial stays visible at far left edge; zoomed-in GREEN afferent arteriole fills frame height
        dial_p = ValueTracker(100.0)
        dial_c = np.array([-5.45, 0.0, 0.0])
        dial_r = 0.85

        def d_ang(p):
            return PI - PI * np.clip((p - 40.0) / 180.0, 0.0, 1.0)

        track = Arc(radius=dial_r, start_angle=PI, angle=-PI, arc_center=dial_c, stroke_color=TEXT, stroke_width=5)
        ticks = VGroup()
        for p in (80.0, 130.0, 180.0):
            ang = d_ang(p)
            p_in = dial_c + (dial_r - 0.12) * np.array([np.cos(ang), np.sin(ang), 0.0])
            p_out = dial_c + (dial_r + 0.05) * np.array([np.cos(ang), np.sin(ang), 0.0])
            ticks.add(Line(p_in, p_out, color=TEXT, stroke_width=2.5))
        hub = Dot(dial_c, radius=0.07, color=TEXT)
        needle = always_redraw(lambda: Line(
            dial_c,
            dial_c + 0.76 * dial_r * np.array([np.cos(d_ang(dial_p.get_value())), np.sin(d_ang(dial_p.get_value())), 0]),
            color=TEXT, stroke_width=5
        ))
        dial_lbl = T("arterial\npressure", 24, TEXT, line_spacing=0.85).move_to(dial_c + DOWN * 0.56)
        dial_grp = VGroup(track, ticks, hub, needle, dial_lbl)

        # Zoomed smooth muscle wall: lumen radius tracker
        r_wall = ValueTracker(1.05)
        flow_speed = ValueTracker(1.0)
        depol_x = ValueTracker(-4.0)
        depol_on = ValueTracker(0.0)
        ca_alpha = ValueTracker(0.0)

        x0, x1 = -3.6, 5.8
        xc = (x0 + x1) / 2.0
        w_len = x1 - x0

        def mk_walls():
            rw = r_wall.get_value()
            thick = 0.62
            lumen = Rectangle(width=w_len, height=2 * rw, stroke_width=0, fill_color=RED, fill_opacity=0.10).move_to([xc, 0, 0])
            top_band = RoundedRectangle(corner_radius=0.14, width=w_len, height=thick, stroke_color=GREEN, stroke_width=5,
                                        fill_color=GREEN, fill_opacity=0.25).move_to([xc, rw + thick / 2, 0])
            bot_band = RoundedRectangle(corner_radius=0.14, width=w_len, height=thick, stroke_color=GREEN, stroke_width=5,
                                        fill_color=GREEN, fill_opacity=0.25).move_to([xc, -(rw + thick / 2), 0])
            return VGroup(lumen, top_band, bot_band)

        walls = always_redraw(mk_walls)

        # Depolarization ripple along both green muscle bands
        def mk_ripple():
            op = depol_on.get_value()
            if op < 0.02:
                return VGroup()
            rx = depol_x.get_value()
            rw = r_wall.get_value()
            rt = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.52, stroke_width=0, fill_color=TEXT, fill_opacity=0.40 * op).move_to([rx, rw + 0.31, 0])
            rb = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.52, stroke_width=0, fill_color=TEXT, fill_opacity=0.40 * op).move_to([rx, -(rw + 0.31), 0])
            return VGroup(rt, rb)

        ripple = always_redraw(mk_ripple)

        # Red plasma dots flowing through the zoomed arteriole
        rng = np.random.default_rng(7)
        pdots = VGroup()
        for i in range(28):
            d = Dot(radius=0.07, color=RED)
            d._x = x0 + (i / 28.0) * w_len
            d._yr = float(rng.uniform(-0.78, 0.78))

            def upd_pd(mob, dt):
                mob._x += dt * 2.4 * flow_speed.get_value()
                if mob._x > x1:
                    mob._x -= w_len
                mob.move_to([mob._x, mob._yr * (r_wall.get_value() - 0.12), 0])

            d.add_updater(upd_pd)
            upd_pd(d, 0.0)
            pdots.add(d)

        # Calcium specks inside the muscle bands (brighten on 'Calcium inside it rises')
        ca_specks = VGroup()
        for i in range(24):
            sx = x0 + 0.35 + (i % 12) * 0.78
            side = 1.0 if i < 12 else -1.0
            dy = float(rng.uniform(-0.18, 0.18))
            sp = Dot(radius=0.055, color=TEXT)
            sp._sx, sp._side, sp._dy = sx, side, dy
            sp.add_updater(lambda m: m.move_to([m._sx, m._side * (r_wall.get_value() + 0.31) + m._dy, 0]).set_opacity(ca_alpha.get_value()))
            ca_specks.add(sp)

        # Tag 1 in top left
        tag1 = boxed_label("1", color=TEXT, size=28, pad=0.16).move_to([-5.45, 2.85, 0])
        schem = scope_tag("schematic", size=24, color=TEXT)
        self.add(walls, ripple, pdots, ca_specks, dial_grp, tag1, schem)

        self.at("reads stretch")
        tag1_stretch = boxed_label("1: stretch", color=GREEN, size=28, pad=0.16).move_to([-5.05, 2.85, 0])
        self.play(swap(tag1, tag1_stretch, run_time=0.5))

        self.at("rising pressure")
        # Outward white stretch arrows pressing on the walls; place label clear above the wall
        arr_up = VGroup(*[Arrow([px, 0.75, 0], [px, 1.45, 0], buff=0, color=TEXT, stroke_width=5) for px in (-1.2, 1.1, 3.4)])
        arr_dn = VGroup(*[Arrow([px, -0.75, 0], [px, -1.45, 0], buff=0, color=TEXT, stroke_width=5) for px in (-1.2, 1.1, 3.4)])
        stretch_lbl = T("stretch", 30, TEXT).move_to([1.1, 2.75, 0])
        self.play(
            dial_p.animate.set_value(165.0),
            r_wall.animate.set_value(1.52),
            flow_speed.animate.set_value(1.65),
            FadeIn(arr_up), FadeIn(arr_dn), FadeIn(stretch_lbl),
            run_time=1.8
        )

        self.at("depolarizes")
        depol_x.set_value(-3.2)
        depol_on.set_value(1.0)
        self.play(depol_x.animate.set_value(5.3), run_time=1.6, rate_func=linear)
        depol_on.set_value(0.0)

        self.at("Calcium inside")
        self.play(ca_alpha.animate.set_value(1.0), run_time=1.0)

        self.at("it contracts")
        self.play(
            FadeOut(arr_up), FadeOut(arr_dn), FadeOut(stretch_lbl),
            r_wall.animate.set_value(0.84),
            flow_speed.animate.set_value(1.0),
            run_time=1.5
        )

        self.at("myogenic response")
        myo_lbl = T("myogenic response", 34, GREEN).move_to([1.1, 2.85, 0])
        bay_lbl = T("Bayliss, 1902", 24, TEXT).next_to(myo_lbl, DOWN, buff=0.14)
        self.play(FadeIn(myo_lbl, shift=DOWN * 0.08), FadeIn(bay_lbl, shift=DOWN * 0.08), run_time=0.8)

        self.at("still debated")
        # Show stretch arrows + '?' clear of plasma dots above the top wall
        arr_hint = VGroup(
            Arrow([4.25, 1.55, 0], [4.25, 2.15, 0], buff=0, color=TEXT, stroke_width=4),
            Arrow([4.25, -1.55, 0], [4.25, -2.15, 0], buff=0, color=TEXT, stroke_width=4),
        )
        q_mark = T("?", 38, TEXT, weight=BOLD).move_to([4.72, 1.85, 0])
        self.play(FadeIn(arr_hint), FadeIn(q_mark), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ Scene 04
class S04MaculaDensa(SpokenScene):
    def construct(self):
        w = NephronWorld(p_init=120.0, with_tubule=True, with_macula=True)
        w.macula_alpha.set_value(0.0)

        tag1 = boxed_label("1: stretch", color=GREEN, size=24, pad=0.12).move_to([-4.65, 2.65, 0])
        tag2 = boxed_label("2", color=TEXT, size=24, pad=0.12).move_to([-2.90, 2.65, 0])
        self.add(w.root, tag1, tag2)

        self.at("comes back to touch")
        touch_glow = Circle(radius=0.45, color=CYAN, stroke_width=6).move_to([-2.90, -0.15, 0])
        self.play(ShowPassingFlash(touch_glow, time_width=0.9), run_time=1.3)

        self.at("end of the thick")
        asc_hi = Line([-2.90, -1.70, 0], [-2.90, -0.15, 0], color=CYAN, stroke_width=10)
        self.play(ShowPassingFlash(asc_hi, time_width=0.8), run_time=1.1)

        self.at("the macula densa")
        self.play(w.macula_alpha.animate.set_value(1.0), w.macula_glow.animate.set_value(0.8), run_time=0.6)
        md_lbl = T("macula densa", 26, MAGENTA).move_to([-1.15, -1.62, 0])
        md_ptr = Arrow(md_lbl.get_left() + LEFT * 0.08, [-2.55, -0.52, 0], buff=0.05, color=MAGENTA, stroke_width=3.5)
        self.play(FadeIn(md_lbl), Create(md_ptr), run_time=0.5)

        self.at("adjust filtration")
        fb_arrow = CurvedArrow([-2.55, -0.52, 0], [-2.58, w.y_vessel - 0.36, 0], angle=0.55, color=TEXT, stroke_width=4.5)
        self.play(Create(fb_arrow), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ Scene 05
class S05FeedbackRule(SpokenScene):
    def construct(self):
        w = NephronWorld(p_init=120.0, with_tubule=True, with_macula=True, salt_mode="high")
        tag1 = boxed_label("1: stretch", color=GREEN, size=24, pad=0.12).move_to([-4.65, 2.65, 0])
        tag2 = boxed_label("2", color=TEXT, size=24, pad=0.12).move_to([-2.90, 2.65, 0])
        md_lbl = T("macula densa", 26, MAGENTA).move_to([-1.15, -1.62, 0])
        md_ptr = Arrow(md_lbl.get_left() + LEFT * 0.08, [-2.55, -0.52, 0], buff=0.05, color=MAGENTA, stroke_width=3.5)
        self.add(w.root, tag1, tag2, md_lbl, md_ptr)

        # More salt arrives -> constrict
        self.at("constricts")
        more_lbl = boxed_label("more salt: constrict", color=TEXT, size=28, pad=0.16).move_to([1.2, 2.65, 0])
        self.play(
            w.aff_open.animate.set_value(0.58),
            w.flow_rate.animate.set_value(0.55),
            w.gfr_rate.animate.set_value(0.55),
            w.macula_glow.animate.set_value(1.0),
            FadeIn(more_lbl, shift=DOWN * 0.06),
            run_time=1.3
        )

        # Less salt arrives -> clear old answer first, then dilate + release renin
        self.at("Less salt")
        less_lbl = boxed_label("less salt: dilate", color=GREEN, size=28, pad=0.16).move_to([1.2, 2.65, 0])
        self.play(
            FadeOut(more_lbl, run_time=0.35),
            w.salt_rate.animate.set_value(0.35),
            w.macula_glow.animate.set_value(0.2),
            run_time=0.5
        )
        self.play(
            w.aff_open.animate.set_value(1.38),
            w.flow_rate.animate.set_value(1.45),
            w.gfr_rate.animate.set_value(1.45),
            FadeIn(less_lbl, shift=DOWN * 0.06),
            run_time=1.0
        )

        self.at("renin")
        renin_dots = VGroup(*[Dot(radius=0.065, color=PINK).move_to([-2.38 + dx, w.y_vessel + 0.36, 0]) for dx in (-0.18, 0.0, 0.18)])
        renin_lbl = T("renin", 26, PINK).move_to([-1.65, w.y_vessel + 1.40, 0])
        self.play(
            FadeIn(renin_dots, run_time=0.3),
            renin_dots.animate(run_time=0.8).shift(UP * 0.58 + RIGHT * 0.55),
            FadeIn(renin_lbl, run_time=0.4),
        )

        self.at("tubuloglomerular feedback")
        tag2_salt = boxed_label("2: salt", color=CYAN, size=24, pad=0.12).move_to([-2.90, 2.65, 0])
        tgf_lbl = T("tubuloglomerular feedback", 28, CYAN).move_to([1.1, -2.92, 0])
        self.play(
            FadeOut(less_lbl), FadeOut(renin_dots), FadeOut(renin_lbl),
            w.aff_open.animate.set_value(1.0),
            w.flow_rate.animate.set_value(1.0),
            w.gfr_rate.animate.set_value(1.0),
            w.salt_rate.animate.set_value(1.0),
            swap(tag2, tag2_salt, run_time=0.6),
            FadeIn(tgf_lbl, shift=UP * 0.06),
            run_time=1.1
        )
        self.finish()


# ------------------------------------------------------------------ Scene 06
class S06Signal(SpokenScene):
    def construct(self):
        # Zoom in on the magenta macula densa patch touching the green afferent wall
        # Left: CYAN tubule lumen (-5.6 .. -3.2); Center-left: MAGENTA cells (-3.2 .. -0.3)
        # Gap: (-0.3 .. +1.6); Right: GREEN arteriole wall (+1.6 .. +3.2) & blood lumen (+3.2 .. +5.8)
        rng = np.random.default_rng(7)
        schem = scope_tag("schematic", size=24, color=TEXT)

        tub_bg = Rectangle(width=2.4, height=5.8, stroke_width=0, fill_color=CYAN, fill_opacity=0.12).move_to([-4.4, 0, 0])
        tub_l = Line([-5.6, -2.9, 0], [-5.6, 2.9, 0], color=CYAN, stroke_width=5)
        tub_r = Line([-3.2, -2.9, 0], [-3.2, 2.9, 0], color=CYAN, stroke_width=5)

        # 3 rounded macula densa cells; middle cell has NKCC2 door
        cells = VGroup(
            RoundedRectangle(corner_radius=0.22, width=2.7, height=1.6, stroke_color=MAGENTA, stroke_width=4,
                             fill_color=MAGENTA, fill_opacity=0.22).move_to([-1.75, 1.95, 0]),
            RoundedRectangle(corner_radius=0.22, width=2.7, height=1.7, stroke_color=MAGENTA, stroke_width=4,
                             fill_color=MAGENTA, fill_opacity=0.25).move_to([-1.75, 0.0, 0]),
            RoundedRectangle(corner_radius=0.22, width=2.7, height=1.6, stroke_color=MAGENTA, stroke_width=4,
                             fill_color=MAGENTA, fill_opacity=0.22).move_to([-1.75, -1.95, 0]),
        )
        # NKCC2 door on left wall of middle cell
        nkcc_gap = Rectangle(width=0.35, height=0.52, stroke_width=0, fill_color=BG, fill_opacity=1.0).move_to([-3.10, 0.0, 0])
        nkcc_top = Line([-3.30, 0.26, 0], [-2.90, 0.26, 0], color=TEXT, stroke_width=4)
        nkcc_bot = Line([-3.30, -0.26, 0], [-2.90, -0.26, 0], color=TEXT, stroke_width=4)
        nkcc_txt = T("NKCC2", 26, TEXT).move_to([-4.38, 0.88, 0]).set_z_index(6)
        nkcc_bg = RoundedRectangle(corner_radius=0.10, width=nkcc_txt.width + 0.26, height=nkcc_txt.height + 0.20,
                                   stroke_color=CYAN, stroke_width=2, fill_color=BG, fill_opacity=0.94).move_to(nkcc_txt).set_z_index(5)
        nkcc_lbl = VGroup(nkcc_bg, nkcc_txt)

        # GREEN afferent arteriole wall on right (squeeze shifts left/wall inward)
        wall_shift = ValueTracker(0.0)
        flow_sp = ValueTracker(1.0)

        def mk_green_wall():
            dx = wall_shift.get_value()
            wall = RoundedRectangle(corner_radius=0.18, width=1.45, height=5.8, stroke_color=GREEN, stroke_width=5,
                                    fill_color=GREEN, fill_opacity=0.24).move_to([2.3 + dx, 0, 0])
            # A1 receptor U-slot on left edge of green wall
            slot = Arc(radius=0.26, start_angle=-PI / 2, angle=PI, arc_center=[1.57 + dx, 0.0, 0],
                       stroke_color=GREEN, stroke_width=5)
            blood = Rectangle(width=2.6 - dx, height=5.8, stroke_width=0, fill_color=RED, fill_opacity=0.10).move_to([4.35 + dx / 2, 0, 0])
            return VGroup(blood, wall, slot)

        green_wall = always_redraw(mk_green_wall)
        a1_txt = T("A1\nreceptor", 26, GREEN, line_spacing=0.85).move_to([0.58, -1.65, 0])
        a1_ptr = Arrow(a1_txt.get_top() + UP * 0.06, [1.45, -0.22, 0], buff=0.04, color=GREEN, stroke_width=3.5)
        a1_lbl = VGroup(a1_txt, a1_ptr)

        # RED blood dots moving upward in right lumen
        bdots = VGroup()
        for i in range(14):
            d = Dot(radius=0.075, color=RED)
            d._y = -2.7 + (i / 14.0) * 5.4
            d._xr = float(rng.uniform(3.65, 5.45))

            def upd_bd(mob, dt):
                mob._y += dt * 1.9 * flow_sp.get_value()
                if mob._y > 2.75:
                    mob._y -= 5.5
                mob.move_to([max(mob._xr, 3.35 + wall_shift.get_value()), mob._y, 0])

            d.add_updater(upd_bd)
            upd_bd(d, 0.0)
            bdots.add(d)

        # Flowing salt specks in tubule lumen
        salt_lumen = VGroup()
        for i in range(14):
            sp = Dot(radius=0.05, color=TEXT)
            sp._y = -2.7 + (i / 14.0) * 5.4
            sp._x = float(rng.uniform(-5.2, -3.5))

            def upd_sl(mob, dt):
                mob._y += dt * 1.3
                if mob._y > 2.75:
                    mob._y -= 5.5
                mob.move_to([mob._x, mob._y, 0])

            sp.add_updater(upd_sl)
            upd_sl(sp, 0.0)
            salt_lumen.add(sp)

        zoom_grp = VGroup(tub_bg, tub_l, tub_r, cells, nkcc_gap, nkcc_top, nkcc_bot, green_wall, bdots, salt_lumen, schem)
        self.add(zoom_grp)

        # Cue 1: NKCC2
        self.at("NKCC2")
        salt_enter = VGroup(*[Dot(radius=0.06, color=TEXT).move_to([-3.65 - 0.3 * i, (i - 1) * 0.10, 0]) for i in range(3)])
        self.play(FadeIn(nkcc_lbl), FadeIn(salt_enter), run_time=0.6)
        self.play(salt_enter.animate.shift(RIGHT * 2.1), run_time=1.3)

        # Cue 2: When more arrives -> release ATP
        self.at("When more arrives")
        more_salt = VGroup(*[Dot(radius=0.06, color=TEXT).move_to([-3.85 - 0.25 * i, (i - 2) * 0.08, 0]) for i in range(5)])
        self.play(FadeIn(more_salt), more_salt.animate.shift(RIGHT * 2.2), run_time=1.0)

        self.at("release")
        atp_sparks = VGroup(*[Star(5, outer_radius=0.14, inner_radius=0.06, color=MAGENTA, fill_opacity=0.95).move_to([-0.25, (i - 1) * 0.30, 0]) for i in range(3)])
        atp_lbl = T("ATP", 28, MAGENTA).move_to([0.55, 1.05, 0])
        self.play(
            FadeIn(atp_sparks, run_time=0.35),
            FadeIn(atp_lbl, run_time=0.35),
            atp_sparks.animate(run_time=0.85).shift(RIGHT * 0.75),
        )

        # Cue 3: Adenosine -> sparks morph into small rings
        self.at("denosine")
        ad_rings = VGroup(*[Circle(radius=0.11, color=MAGENTA, stroke_width=5).move_to(s.get_center() + RIGHT * 0.35) for s in atp_sparks])
        ad_lbl = T("adenosine", 26, MAGENTA).move_to([0.45, 1.05, 0])
        self.play(ReplacementTransform(atp_sparks, ad_rings, run_time=0.8), swap(atp_lbl, ad_lbl, run_time=0.5))

        # Cue 4: A1 receptors -> dock in slots on GREEN wall
        self.at("acts on")
        self.play(FadeIn(a1_lbl, run_time=0.45), ad_rings.animate(run_time=0.85).move_to([1.50, 0.0, 0]))

        # Cue 5: constricts -> green wall squeezes inward
        self.at("constricts")
        self.play(wall_shift.animate.set_value(0.65), flow_sp.animate.set_value(0.55), run_time=1.0)

        # Cue 6: Zoom back out to full world -> slower drops + two down-arrows
        self.at("pressure and filtration")
        w = NephronWorld(p_init=120.0, aff_init=0.62, flow_init=0.58, gfr_init=0.55,
                         with_tubule=True, with_macula=True, salt_mode="high")
        w.macula_glow.set_value(0.9)
        down_p = VGroup(Arrow([0.1, 1.65, 0], [0.1, 1.05, 0], buff=0, color=TEXT, stroke_width=5),
                        T("filter pressure", 26, TEXT)).arrange(RIGHT, buff=0.12).move_to([-1.3, 1.75, 0])
        down_f = VGroup(Arrow([0.1, 1.65, 0], [0.1, 1.05, 0], buff=0, color=TEXT, stroke_width=5),
                        T("filtration", 26, TEXT)).arrange(RIGHT, buff=0.12).move_to([1.9, 1.75, 0])
        self.play(FadeOut(VGroup(zoom_grp, nkcc_lbl, salt_enter, more_salt, ad_rings, ad_lbl, a1_lbl), run_time=0.35))
        self.play(FadeIn(w.root, run_time=0.5), FadeIn(down_p, run_time=0.5), FadeIn(down_f, run_time=0.5))
        self.play(w.gfr_rate.animate.set_value(0.6), w.flow_rate.animate.set_value(0.85), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ Scene 07
class S07Idea(SpokenScene):
    def construct(self):
        # Full world, down-arrows gone, yellow nozzle still & slightly dimmed
        w = NephronWorld(p_init=125.0, with_tubule=True, with_macula=True, dim_efferent=True, salt_mode="normal")
        w.macula_glow.set_value(0.5)

        # Dial needle swings again; green ring counter-adjusts inversely while flow and drops stay steady!
        t_sw = [0.0]

        def swing_counter(mob, dt):
            t_sw[0] += dt
            p = 130.0 + 50.0 * np.sin(1.25 * t_sw[0])
            mob.set_value(p)
            w.aff_open.set_value(aff_from_pressure(p))

        w.p_art.add_updater(swing_counter)
        self.add(w.p_art, w.root)

        self.at("Two signals")
        str_arr = Arrow([-4.55, w.y_vessel + 0.55, 0], [-3.20, w.y_vessel + 0.30, 0], buff=0.05, color=TEXT, stroke_width=5)
        str_lbl = T("stretch", 26, TEXT).move_to([-4.25, 1.55, 0])
        salt_arr = CurvedArrow([-2.55, -0.52, 0], [-2.58, w.y_vessel - 0.34, 0], angle=0.55, color=TEXT, stroke_width=5)
        salt_lbl = T("salt", 26, TEXT).move_to([-2.05, -1.45, 0])
        self.play(Create(str_arr), FadeIn(str_lbl), Create(salt_arr), FadeIn(salt_lbl), run_time=0.5)

        self.at("stretch", nth=1)
        self.play(
            Indicate(VGroup(str_arr, str_lbl), color=GREEN, scale_factor=1.12),
            ShowPassingFlash(Circle(radius=0.52, color=GREEN, stroke_width=7).move_to([-2.90, w.y_vessel, 0]), time_width=0.6),
            run_time=1.0
        )

        self.at("salt", nth=1)
        self.play(
            Indicate(VGroup(salt_arr, salt_lbl), color=CYAN, scale_factor=1.12),
            ShowPassingFlash(Circle(radius=0.52, color=GREEN, stroke_width=7).move_to([-2.90, w.y_vessel, 0]), time_width=0.6),
            run_time=1.0
        )

        self.at("one valve")
        valve_lbl = boxed_label("one valve, upstream", color=GREEN, size=30, pad=0.16).move_to([-2.3, 2.55, 0])
        self.play(
            Indicate(VGroup(str_arr, salt_arr), color=TEXT, scale_factor=1.08),
            FadeIn(valve_lbl, shift=DOWN * 0.08),
            run_time=1.0
        )
        self.finish()


# ------------------------------------------------------------------ Scene 08
class S08DiabetesPredict(SpokenScene):
    def construct(self):
        # Dial steadies; normal salt before diabetes glucose rises
        w = NephronWorld(p_init=115.0, with_tubule=True, with_macula=True, salt_mode="normal", glucose_mode="high", sglt2_open=False)
        w.glucose_alpha.set_value(0.0)
        w.macula_glow.set_value(0.4)
        self.add(w.root)

        self.at("High plasma glucose")
        gl_lbl = boxed_label("high glucose", color=GOLD, size=26, pad=0.14).move_to([0.1, 2.15, 0])
        self.play(w.glucose_alpha.animate.set_value(1.0), FadeIn(gl_lbl, shift=DOWN * 0.08), run_time=0.9)

        self.at("proximal tubule")
        prox_lbl = T("proximal tubule", 26, CYAN).move_to([3.35, -1.08, 0])
        sglt2_lbl = boxed_label("SGLT2", color=GOLD, size=26, pad=0.12).move_to([5.90, -0.78, 0])
        self.play(FadeIn(prox_lbl), FadeIn(sglt2_lbl), run_time=0.5)

        self.at("SGLT2")
        self.play(w.sglt2_frac.animate.set_value(1.0), Indicate(sglt2_lbl, color=GOLD, scale_factor=1.10), run_time=0.7)

        self.at("less salt")
        self.play(w.macula_glow.animate.set_value(0.15), run_time=0.8)

        self.at("What happens")
        q = question_card("Less salt arriving: filtration?", y=3.20, color=TEXT, size=34)
        self.play(FadeOut(gl_lbl, run_time=0.35), FadeIn(q, run_time=0.6))
        self.finish()


# ------------------------------------------------------------------ Scene 09 (4.5s silent predict pause)
class S09Pause(PredictPause):
    QUESTION = "Less salt arriving: filtration?"
    OPTIONS = ()
    CARD = {"y": 3.20, "color": TEXT, "size": 34}
    RING_AT = (5.9, 3.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = NephronWorld(p_init=115.0, with_tubule=True, with_macula=True, salt_mode="normal", glucose_mode="high", sglt2_open=True)
        # Gentle glow on macula densa
        t_gl = [0.0]
        w.macula_glow.set_value(0.25)
        prox_lbl = T("proximal tubule", 26, CYAN).move_to([3.35, -1.08, 0])
        sglt2_lbl = boxed_label("SGLT2", color=GOLD, size=26, pad=0.12).move_to([5.90, -0.78, 0])
        self.add(w.macula_glow)
        return VGroup(w.root, prox_lbl, sglt2_lbl)


# ------------------------------------------------------------------ Scene 10
class S10Answer(SpokenScene):
    def construct(self):
        w = NephronWorld(p_init=115.0, with_tubule=True, with_macula=True, salt_mode="normal", glucose_mode="high", sglt2_open=True)
        prox_lbl = T("proximal tubule", 26, CYAN).move_to([3.35, -1.08, 0])
        sglt2_lbl = boxed_label("SGLT2", color=GOLD, size=26, pad=0.12).move_to([5.90, -0.78, 0])
        q = question_card("Less salt arriving: filtration?", y=3.20, color=TEXT, size=34)
        self.add(w.root, prox_lbl, sglt2_lbl, q)

        self.at("It rises")
        self.play(FadeOut(q), run_time=0.5)

        self.at("dilates")
        self.play(
            w.aff_open.animate.set_value(1.42),
            w.flow_rate.animate.set_value(1.55),
            run_time=1.0
        )

        self.at("Pressure in the filter")
        up_filt = VGroup(
            Arrow([0.0, 0.0, 0], [0.0, 0.58, 0], buff=0, color=TEXT, stroke_width=5),
            T("filtration", 28, TEXT)
        ).arrange(RIGHT, buff=0.12).move_to([0.10, 1.55, 0])
        self.play(w.gfr_rate.animate.set_value(1.85), FadeIn(up_filt, shift=UP * 0.08), run_time=1.0)

        self.at("hyperfiltration")
        hyp_lbl = boxed_label("hyperfiltration", color=GOLD, size=32, pad=0.16).move_to([0.10, 2.55, 0])
        self.play(FadeIn(hyp_lbl, shift=DOWN * 0.08), run_time=0.8)

        self.at("blunted feedback")
        tag_bf = boxed_label("blunted feedback?", color=TEXT, size=24, pad=0.12).move_to([-4.55, 2.85, 0])
        self.play(FadeIn(tag_bf, shift=RIGHT * 0.06), run_time=0.7)

        self.at("other upstream dilation")
        tag_od = boxed_label("other dilation?", color=TEXT, size=24, pad=0.12).move_to([-4.55, 2.15, 0])
        self.play(FadeIn(tag_od, shift=RIGHT * 0.06), run_time=0.7)

        self.at("still open")
        self.play(Indicate(VGroup(tag_bf, tag_od), color=GOLD, scale_factor=1.05), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ Scene 11
class S11Return(SpokenScene):
    def construct(self):
        # Continuous world returning from diabetes hyperfiltration back to steady autoregulation
        w = NephronWorld(p_init=115.0, aff_init=1.42, flow_init=1.55, gfr_init=1.85,
                         with_tubule=True, with_macula=True, dim_efferent=True,
                         salt_mode="normal", glucose_mode="high", sglt2_open=True)
        hyp_lbl = boxed_label("hyperfiltration", color=GOLD, size=32, pad=0.16).move_to([0.10, 2.55, 0])
        tag_bf = boxed_label("blunted feedback?", color=TEXT, size=24, pad=0.12).move_to([-4.55, 2.85, 0])
        tag_od = boxed_label("other dilation?", color=TEXT, size=24, pad=0.12).move_to([-4.55, 2.15, 0])
        self.add(w.root, hyp_lbl, tag_bf, tag_od)

        str_arr = Arrow([-4.55, w.y_vessel + 0.55, 0], [-3.20, w.y_vessel + 0.30, 0], buff=0.05, color=TEXT, stroke_width=5)
        str_lbl = T("stretch", 26, TEXT).move_to([-4.25, 1.55, 0])
        salt_arr = CurvedArrow([-2.55, -0.52, 0], [-2.58, w.y_vessel - 0.34, 0], angle=0.55, color=TEXT, stroke_width=5)
        salt_lbl = T("salt", 26, TEXT).move_to([-2.05, -1.45, 0])

        self.play(
            FadeOut(VGroup(hyp_lbl, tag_bf, tag_od), run_time=0.35),
            w.glucose_alpha.animate(run_time=0.8).set_value(0.0),
            w.sglt2_frac.animate(run_time=0.8).set_value(0.0),
            w.aff_open.animate(run_time=0.8).set_value(1.0),
            w.flow_rate.animate(run_time=0.8).set_value(1.0),
            w.gfr_rate.animate(run_time=0.8).set_value(1.0),
            w.macula_glow.animate(run_time=0.8).set_value(0.5),
        )
        self.play(FadeIn(str_arr), FadeIn(str_lbl), FadeIn(salt_arr), FadeIn(salt_lbl), run_time=0.45)

        # Dial swings between 80 and 180 mmHg while green ring counter-adjusts inversely
        t_sw = [0.0]

        def swing_counter(mob, dt):
            t_sw[0] += dt
            p = 130.0 + 50.0 * np.sin(1.25 * t_sw[0])
            mob.set_value(p)
            w.aff_open.set_value(aff_from_pressure(p))

        w.p_art.add_updater(swing_counter)
        self.add(w.p_art)

        self.at("reads the pressure")
        self.play(Indicate(VGroup(str_arr, str_lbl), color=GREEN, scale_factor=1.14), run_time=0.9)

        self.at("reads the salt")
        self.play(Indicate(VGroup(salt_arr, salt_lbl), color=CYAN, scale_factor=1.14), run_time=0.9)

        self.at("same upstream valve")
        self.play(
            Indicate(VGroup(str_arr, salt_arr), color=TEXT, scale_factor=1.10),
            ShowPassingFlash(Circle(radius=0.52, color=GREEN, stroke_width=7).move_to([-2.90, w.y_vessel, 0]), time_width=0.7),
            run_time=1.1
        )
        self.finish()


# ------------------------------------------------------------------ Scene 12 (EndCard)
class S12End(EndCard):
    LINE = "Stretch and salt signals tune the afferent arteriole, keeping filtration nearly steady."
