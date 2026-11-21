"""
COLOUR MAP (one colour per concept for the whole film):
- water (drops, lumen streams, load/stool bars): CYAN (#38E8FF)
- sodium ions (Na+): BLUE (#4D88FF)
- chloride ions (Cl-): GREEN (#83C167)
- sugar / glucose: GOLD (#F5C542)
- sodium pump (basolateral Na+/K+ pump): RED (#FC6255)
- cholera toxin & cyclic AMP: MAGENTA (#E65CFF)
- ledger frames, rules, headings, numbers, wall labels: WHITE (#E8EAF0)
- gut-lining epithelial cells: pale grey fill (#2B3240) with grey outline (#8B93A1)

THE ONE WORLD (carried from scene to scene):
Left 68%: cut-away gut tube (mouth 'in' at left, villi + crypts along the lower wall over a dark 'blood' band, narrow outlet 'out' at right), zooming into one crypt + one villus on the same geometry in s08-s11.
Right 32%: the Ledger (tall 'load' bar 0-12 L/day, magnified 'stool water' bar 0-0.25 L/day, round 'captured' dial, 'teaching numbers' / 'schematic' tag).

WHAT CHANGES ON SCREEN (per spoken scene, and what it is computed from):
- s00_hook: CYAN water drops pour in at 'in', sink through the wall into 'blood' (0.99 captured), and drip thinly at 'out' (0.11 L/d); load bar fills to 11 L while stool-water bar barely rises; question appears.
- s02_load: CYAN drops enter mouth (2 L) then 5 secretion inlets open one by one (+9 L); load bar stacks drink (2) + secretions (9) = 11 L; sinking stream thickens and dial swings to 99%.
- s03_rule: Outlet drip is highlighted; formula writes across bottom; 1% sliver slides from top of 11 L load bar across to fill stool-water bar to 11 * (1 - 0.99) = 0.11 L a day.
- s04_predict: Option cards A (12 L, 99%) and B (11 L, 98%) slide in; ghost extra litre glows on load bar for A; dial needle twitches toward 98% and back for B while stool bar stays at 0.11; question appears.
- s06_answer: Load grows to 12 L and stool water rises to 12 * 0.01 = 0.12 L (mark A: 0.12); reset to 11 L, dial drops to 98%, outlet drip doubles and stool water rises to 11 * 0.02 = 0.22 L (mark B: 0.22, bracket x 2).
- s07_idea: Ledger resets to 11 L, 99%, 0.11 L; inflow and outlet drip highlight together; dial needle wobbles 99% <-> 98% while stool-water bar and drip swing inversely via load * (1 - captured); load rises slightly to show proportional change.
- s08_crypt: Zooms into crypt + villus wall; RED Na+ pump cycles and NKCC1 loads GREEN Cl- from below into crypt cell; CFTR swings open so Cl- pours into gut, BLUE Na+ slips between cells, CYAN water follows, load bar edges up.
- s09_villus: Camera highlights villus; NHE3 + partner import BLUE Na+ and GREEN Cl-; SGLT1 turnstile rotates importing 2 BLUE Na+ with 1 GOLD sugar; CYAN water crosses into blood; crypt-up and villus-down arrows appear.
- s10_balance: Secretion up-arrow and absorption down-arrow glow; one villus cell briefly shows CFTR; pulls back to full tube; outlet drip pulses; colon stretch brightens and draws extra CYAN drops into blood.
- s11_cholera: Pushes back into crypt + villus; MAGENTA toxin chips land, G protein switch jams 'on', MAGENTA cyclic AMP fills cells; crypt CFTR opens wide (load bar rises, no number), villus NHE3 slows/dims (dial drops, no number), SGLT1 keeps turning unlabelled.
- s12_close: Pulls back to full tube, toxin clears, ledger returns to 11 L, 99%, 0.11 L; sinking stream glows; dial dips 99% -> 98% and outlet drip + stool bar double from 0.11 to 0.22 L, then return.
"""

from bp_parts import *  # noqa: F401,F403

# ------------------------------------------------------------------ COLOUR MAP
CYAN = "#38E8FF"       # water
NA_BLUE = "#4D88FF"    # sodium
CL_GREEN = "#83C167"   # chloride
SUGAR_GOLD = "#F5C542" # sugar
PUMP_RED = "#FC6255"   # sodium pump
TOXIN_MAG = "#E65CFF"  # cholera toxin & cyclic AMP
BAR_WHITE = "#E8EAF0"  # ledger bars, numbers, main labels
CELL_FILL = "#2B3240"  # gut-lining cells pale grey fill
CELL_EDGE = "#8B93A1"  # cell outline
BLOOD_BG = "#1B141D"   # dark blood band

TUBE_X0 = -5.35
TUBE_X1 = 1.05
TUBE_Y_TOP = 1.55
TUBE_Y_BASE = -0.35
BLOOD_Y_TOP = -1.15
BLOOD_Y_BOT = -2.10


def _wall_y(x):
    """Smooth villus-and-crypt lower gut wall from TUBE_X0 to TUBE_X1."""
    u = (x - TUBE_X0) / (TUBE_X1 - TUBE_X0)
    phase = u * 6.0 * TAU
    s = np.sin(phase - PI / 2)
    return -0.38 + 0.50 * s - 0.12 * np.cos(2 * phase)


class GutTubeWorld:
    """Left 68%: cut-away gut tube with villi/crypts, blood band, inlets, outlet drip, and computed water flow."""

    def __init__(self, load_t, cap_t, inlets_t=None, colon_t=None, drip_vis_t=None, stool_override_t=None, seed=7):
        self.load_t = load_t
        self.cap_t = cap_t
        self.inlets_t = inlets_t if inlets_t is not None else ValueTracker(5.0)
        self.colon_t = colon_t if colon_t is not None else ValueTracker(0.0)
        self.drip_vis_t = drip_vis_t if drip_vis_t is not None else ValueTracker(1.0)
        self.stool_override_t = stool_override_t
        self.rng = np.random.default_rng(seed)

        self.root = VGroup()
        self.static = VGroup()
        self.inlets = VGroup()
        self.inlet_xs = [-4.25, -3.15, -2.05, -0.95, 0.15]

        # Blood band (Polygon so layout_check does not treat it as a panel Rectangle)
        blood_poly = Polygon(
            [-5.65, BLOOD_Y_BOT, 0],
            [1.25, BLOOD_Y_BOT, 0],
            [1.25, BLOOD_Y_TOP, 0],
            [-5.65, BLOOD_Y_TOP, 0],
            fill_color=BLOOD_BG,
            fill_opacity=1.0,
            stroke_color=CELL_EDGE,
            stroke_width=2.0,
        )
        self.blood_label = T("blood", 24, BAR_WHITE).move_to([-5.05, -1.62, 0])

        # Epithelial wall with villi and crypts
        xs = np.linspace(TUBE_X0, TUBE_X1, 180)
        wall_pts = [[float(x), float(_wall_y(x)), 0.0] for x in xs]
        wall_poly_pts = wall_pts + [[TUBE_X1, BLOOD_Y_TOP, 0.0], [TUBE_X0, BLOOD_Y_TOP, 0.0]]
        self.wall_fill = Polygon(
            *wall_poly_pts,
            fill_color=CELL_FILL,
            fill_opacity=0.82,
            stroke_color=CELL_EDGE,
            stroke_width=2.5,
        )

        # Upper tube wall + flared left mouth ('in') + narrow right outlet ('out')
        upper_pts = [
            [-6.05, 1.85, 0],
            [TUBE_X0, TUBE_Y_TOP, 0],
            [TUBE_X1, TUBE_Y_TOP, 0],
            [1.58, 0.72, 0],
        ]
        self.upper_wall = VMobject(stroke_color=CELL_EDGE, stroke_width=3.5).set_points_as_corners(upper_pts)

        mouth_bot = VMobject(stroke_color=CELL_EDGE, stroke_width=3.5).set_points_as_corners([
            [-6.05, -0.45, 0],
            [TUBE_X0, float(_wall_y(TUBE_X0)), 0],
        ])
        outlet_bot = VMobject(stroke_color=CELL_EDGE, stroke_width=3.5).set_points_as_corners([
            [TUBE_X1, float(_wall_y(TUBE_X1)), 0],
            [1.58, 0.38, 0],
        ])

        self.in_label = T("in", 28, BAR_WHITE).move_to([-5.85, 2.18, 0])
        # Placed cleanly clear of the sloped upper outlet wall
        self.out_label = T("out", 28, BAR_WHITE).move_to([1.74, 1.38, 0])

        # 5 secretion inlets along top wall
        for ix in self.inlet_xs:
            pipe = VGroup(
                Line([ix - 0.12, TUBE_Y_TOP, 0], [ix - 0.12, TUBE_Y_TOP + 0.42, 0], stroke_color=CYAN, stroke_width=2.5),
                Line([ix + 0.12, TUBE_Y_TOP, 0], [ix + 0.12, TUBE_Y_TOP + 0.42, 0], stroke_color=CYAN, stroke_width=2.5),
            )
            pipe.set_opacity(0.0)
            self.inlets.add(pipe)

        # Colon highlight stretch (last stretch before outlet, x = -0.35 to 1.05)
        c_xs = np.linspace(-0.35, TUBE_X1, 40)
        c_pts = [[float(x), float(_wall_y(x)), 0.0] for x in c_xs] + [[TUBE_X1, BLOOD_Y_TOP, 0], [-0.35, BLOOD_Y_TOP, 0]]
        self.colon_glow = Polygon(
            *c_pts,
            fill_color=CYAN,
            fill_opacity=0.0,
            stroke_color=CYAN,
            stroke_width=0.0,
        )

        self.static.add(blood_poly, self.wall_fill, self.colon_glow, self.upper_wall, mouth_bot, outlet_bot,
                        self.inlets, self.blood_label, self.in_label, self.out_label)

        # Faint blood dots flowing left-to-right strictly clear of 'blood' label (x > -4.35)
        self.blood_dots = VGroup()
        for _ in range(16):
            d = Dot(radius=0.042, color=PUMP_RED).set_opacity(0.32)
            d._bx = float(self.rng.uniform(-4.25, 1.15))
            d._by = float(self.rng.uniform(BLOOD_Y_BOT + 0.16, BLOOD_Y_TOP - 0.16))
            d.move_to([d._bx, d._by, 0])
            self.blood_dots.add(d)

        # Lumen water drops (computed from load_t, cap_t, inlets_t, colon_t)
        self.water_drops = VGroup()
        self._n_drops = 44
        for i in range(self._n_drops):
            d = Dot(radius=0.068, color=CYAN)
            d._phase = (i / self._n_drops + float(self.rng.uniform(0, 0.02))) % 1.0
            d._lane = float(self.rng.uniform(0.18, 0.85))
            d._sink_x = float(self.rng.uniform(TUBE_X0 + 0.35, TUBE_X1 - 0.20))
            d._inlet_idx = i % 5
            d._is_sec = (i % 4 != 0)
            d._blood_y = float(self.rng.uniform(BLOOD_Y_BOT + 0.18, BLOOD_Y_TOP - 0.18))
            self.water_drops.add(d)

        # Outlet drips (computed directly from stool_water = load * (1 - cap) * drip_vis)
        self.drips = VGroup()
        self._drip_t = 0.0
        for i in range(4):
            dr = Dot(radius=0.05, color=CYAN)
            dr._offset = i / 4.0
            self.drips.add(dr)

        self.root.add(self.static, self.blood_dots, self.water_drops, self.drips)
        self.root.add_updater(lambda m, dt: self._step(dt))
        self._step(0.0)

    def _step(self, dt):
        load = max(0.0, float(self.load_t.get_value()))
        cap = float(np.clip(self.cap_t.get_value(), 0.0, 1.0))
        inl = float(np.clip(self.inlets_t.get_value(), 0.0, 5.0))
        col = float(np.clip(self.colon_t.get_value(), 0.0, 1.0))
        dvis = float(np.clip(self.drip_vis_t.get_value(), 0.0, 1.0))

        self.colon_glow.set_fill(opacity=0.28 * col)
        self.colon_glow.set_stroke(width=3.0 * col, opacity=0.85 * col)

        for idx, pipe in enumerate(self.inlets):
            pipe.set_opacity(float(np.clip(inl - idx, 0.0, 1.0)))

        for d in self.blood_dots:
            d._bx += 0.35 * dt
            if d._bx > 1.15:
                d._bx = -4.25
            d.move_to([d._bx, d._by, 0])

        active_n = int(np.clip(round(load / 12.0 * self._n_drops), 0, self._n_drops))
        speed = 0.24 + 0.012 * load
        for idx, d in enumerate(self.water_drops):
            d._phase = (d._phase + speed * dt) % 1.0
            if idx >= active_n:
                d.set_opacity(0.0)
                continue

            use_inlet = d._is_sec and (inl > d._inlet_idx + 0.3)
            p = d._phase
            sink_x = d._sink_x
            if col > 0.3 and idx % 3 == 0:
                sink_x = -0.25 + 1.15 * ((idx % 7) / 7.0)

            if use_inlet:
                sx = self.inlet_xs[d._inlet_idx]
                sy0 = TUBE_Y_TOP + 0.32
                if p < 0.18:
                    f = p / 0.18
                    x = sx + 0.15 * f
                    y = sy0 - f * (sy0 - (TUBE_Y_TOP - 0.35 - 0.6 * d._lane))
                elif p < 0.48:
                    f = (p - 0.18) / 0.30
                    x = (sx + 0.15) + f * (max(sink_x, sx + 0.3) - (sx + 0.15))
                    y = TUBE_Y_TOP - 0.35 - 0.6 * d._lane
                elif p < 0.72:
                    f = (p - 0.48) / 0.24
                    tx = min(max(sink_x, sx + 0.3), TUBE_X1 - 0.15)
                    y_top = TUBE_Y_TOP - 0.35 - 0.6 * d._lane
                    x = tx
                    y = y_top + f * (d._blood_y - y_top)
                else:
                    f = (p - 0.72) / 0.28
                    tx = min(max(sink_x, sx + 0.3), TUBE_X1 - 0.15)
                    x = tx + f * (1.12 - tx)
                    y = d._blood_y
            else:
                if p < 0.42:
                    f = p / 0.42
                    x = -5.95 + f * (sink_x - (-5.95))
                    y = 0.25 + d._lane * 1.05
                elif p < 0.72:
                    f = (p - 0.42) / 0.30
                    y_top = 0.25 + d._lane * 1.05
                    x = sink_x
                    y = y_top + f * (d._blood_y - y_top)
                else:
                    f = (p - 0.72) / 0.28
                    x = sink_x + f * (1.12 - sink_x)
                    y = d._blood_y

            if y < BLOOD_Y_TOP + 0.05 and x < -4.30:
                x = -4.30
            d.move_to([x, y, 0])
            op = 0.92 if p < 0.90 else 0.92 * (1.0 - (p - 0.90) / 0.10)
            if y < BLOOD_Y_TOP:
                op *= 0.65
            d.set_opacity(float(np.clip(op, 0.0, 1.0)))

        if self.stool_override_t is not None:
            stool = float(self.stool_override_t.get_value()) * dvis
        else:
            stool = load * (1.0 - cap) * dvis
        self._drip_t += dt * (0.45 + 2.2 * min(stool, 0.6))
        drip_r = float(np.clip(0.036 + 0.16 * stool, 0.036, 0.095))
        for i, dr in enumerate(self.drips):
            if stool <= 0.005:
                dr.set_opacity(0.0)
                continue
            if stool < 0.15 and i % 2 == 1:
                dr.set_opacity(0.0)
                continue
            ph = (self._drip_t + dr._offset) % 1.0
            x = 1.58 + 0.12 * ph
            y = 0.48 - 1.15 * (ph ** 1.4)
            dr.scale(drip_r / max(dr.radius, 1e-6))
            dr.radius = drip_r
            dr.move_to([x, y, 0])
            dr.set_opacity(0.95 * (1.0 - max(0.0, ph - 0.8) / 0.2))


class LedgerRig:
    """Right 32%: load bar (0-12 L), stool-water bar (0-0.25 L), captured dial, and scope tag."""

    def __init__(self, load_t, cap_t, drink_t=None, stool_vis_t=None, stool_override_t=None,
                 show_numbers=True, split_load=False, tag_text="teaching numbers"):
        self.load_t = load_t
        self.cap_t = cap_t
        self.drink_t = drink_t
        self.stool_vis_t = stool_vis_t if stool_vis_t is not None else ValueTracker(1.0)
        self.stool_override_t = stool_override_t
        self.show_numbers = show_numbers
        self.split_load = split_load

        self.root = VGroup()
        self.bar_h = 1.90
        self.bar_w = 0.56
        self.bar_y0 = -0.18
        self.load_x = 3.05
        self.stool_x = 5.55

        # Load bar frame (0 to 12 L/day)
        self.load_frame = Rectangle(
            width=self.bar_w, height=self.bar_h,
            stroke_color=BAR_WHITE, stroke_width=2.5, fill_opacity=0.0,
        ).move_to([self.load_x, self.bar_y0 + self.bar_h / 2, 0])
        self.load_title = T("load", 26, BAR_WHITE).move_to([self.load_x, self.bar_y0 + self.bar_h + 0.36, 0])

        load_ticks = VGroup()
        for val, txt in ((0, "0"), (6, "6"), (12, "12")):
            yy = self.bar_y0 + (val / 12.0) * self.bar_h
            tk = Line([self.load_x - self.bar_w / 2 - 0.08, yy, 0],
                      [self.load_x - self.bar_w / 2, yy, 0], stroke_color=BAR_WHITE, stroke_width=2.0)
            lb = T(txt, 22, BAR_WHITE).next_to(tk, LEFT, buff=0.08)
            load_ticks.add(tk, lb)

        # Stool-water bar frame (0 to 0.25 L/day)
        self.stool_frame = Rectangle(
            width=self.bar_w, height=self.bar_h,
            stroke_color=BAR_WHITE, stroke_width=2.5, fill_opacity=0.0,
        ).move_to([self.stool_x, self.bar_y0 + self.bar_h / 2, 0])
        self.stool_title = T("stool water", 26, BAR_WHITE).move_to([self.stool_x, self.bar_y0 + self.bar_h + 0.36, 0])

        stool_ticks = VGroup()
        for val, txt in ((0, "0"), (0.25, "0.25")):
            yy = self.bar_y0 + (val / 0.25) * self.bar_h
            tk = Line([self.stool_x + self.bar_w / 2, yy, 0],
                      [self.stool_x + self.bar_w / 2 + 0.08, yy, 0], stroke_color=BAR_WHITE, stroke_width=2.0)
            lb = T(txt, 22, BAR_WHITE).next_to(tk, RIGHT, buff=0.08)
            stool_ticks.add(tk, lb)

        def _stool_val():
            vis = float(np.clip(self.stool_vis_t.get_value(), 0.0, 1.0))
            if self.stool_override_t is not None:
                return float(self.stool_override_t.get_value()) * vis
            return max(0.0, float(self.load_t.get_value()) * (1.0 - float(self.cap_t.get_value()))) * vis

        def mk_load_fill():
            tot = float(np.clip(self.load_t.get_value(), 0.0, 12.6))
            g = VGroup()
            if self.split_load and self.drink_t is not None:
                dr = float(np.clip(self.drink_t.get_value(), 0.0, tot))
                if dr > 0.05:
                    h1 = (dr / 12.0) * self.bar_h
                    r1 = Rectangle(width=self.bar_w - 0.04, height=h1, fill_color=CYAN, fill_opacity=0.92, stroke_width=0)
                    r1.move_to([self.load_x, self.bar_y0 + h1 / 2, 0])
                    g.add(r1)
                sec = max(0.0, tot - dr)
                if sec > 0.05:
                    h2 = (sec / 12.0) * self.bar_h
                    y_bot = self.bar_y0 + (dr / 12.0) * self.bar_h
                    r2 = Rectangle(width=self.bar_w - 0.04, height=h2, fill_color="#8FF0FF", fill_opacity=0.62, stroke_width=0)
                    r2.move_to([self.load_x, y_bot + h2 / 2, 0])
                    g.add(r2)
            else:
                if tot > 0.05:
                    h = (min(tot, 12.0) / 12.0) * self.bar_h
                    r = Rectangle(width=self.bar_w - 0.04, height=h, fill_color=CYAN, fill_opacity=0.85, stroke_width=0)
                    r.move_to([self.load_x, self.bar_y0 + h / 2, 0])
                    g.add(r)
                    if tot > 12.0:
                        h_ex = ((tot - 12.0) / 12.0) * self.bar_h
                        r_ex = Rectangle(width=self.bar_w - 0.04, height=h_ex, fill_color=TOXIN_MAG, fill_opacity=0.80, stroke_width=0)
                        r_ex.move_to([self.load_x, self.bar_y0 + self.bar_h + h_ex / 2, 0])
                        g.add(r_ex)
            return g

        def mk_stool_fill():
            stool = _stool_val()
            if stool <= 0.002:
                return VGroup()
            h = (min(stool, 0.25) / 0.25) * self.bar_h
            r = Rectangle(width=self.bar_w - 0.04, height=h, fill_color=BAR_WHITE, fill_opacity=0.90, stroke_width=0)
            r.move_to([self.stool_x, self.bar_y0 + h / 2, 0])
            return r

        self.load_fill = always_redraw(mk_load_fill)
        self.stool_fill = always_redraw(mk_stool_fill)

        self.load_num = always_redraw(
            lambda: M(f"{self.load_t.get_value():.0f} L a day", 22, BAR_WHITE).move_to([self.load_x, self.bar_y0 - 0.34, 0])
            if self.show_numbers else VGroup()
        )
        self.stool_num = always_redraw(
            lambda: M(f"{_stool_val():.2f} L a day", 22, BAR_WHITE).move_to([self.stool_x, self.bar_y0 - 0.34, 0])
            if self.show_numbers else VGroup()
        )

        # Captured dial
        dc = np.array([4.35, -1.78, 0.0])
        rad = 0.80
        track = Arc(radius=rad, start_angle=PI, angle=-PI, arc_center=dc, stroke_color=CELL_EDGE, stroke_width=9)
        v = lambda: float(np.clip(self.cap_t.get_value(), 0.001, 1.0))
        val_arc = always_redraw(lambda: Arc(radius=rad, start_angle=PI, angle=-PI * v(), arc_center=dc, stroke_color=CYAN, stroke_width=9))
        needle = always_redraw(lambda: Line(
            dc, dc + 0.78 * rad * np.array([np.cos(PI - PI * v()), np.sin(PI - PI * v()), 0]),
            color=BAR_WHITE, stroke_width=4.5,
        ))
        dial_num = always_redraw(
            lambda: M(f"{self.cap_t.get_value() * 100.0:.0f}%", 32, BAR_WHITE).move_to(dc + DOWN * 0.40)
            if self.show_numbers else VGroup()
        )
        dial_lab = T("captured", 26, BAR_WHITE).move_to(dc + DOWN * 0.86)
        self.dial = VGroup(track, val_arc, needle, dial_num, dial_lab)

        self.tag = scope_tag(tag_text, size=24, color=BAR_WHITE)

        self.root.add(
            self.load_fill, self.stool_fill,
            self.load_frame, self.load_title, load_ticks,
            self.stool_frame, self.stool_title, stool_ticks,
            self.load_num, self.stool_num,
            self.dial, self.tag,
        )

    def y_for_load(self, litres):
        return self.bar_y0 + (litres / 12.0) * self.bar_h

    def y_for_stool(self, litres):
        return self.bar_y0 + (litres / 0.25) * self.bar_h


class CryptVillusWorld:
    """Zoomed crypt (left) + villus (right) epithelial wall in x = [-6.35, 1.95], y = [-2.45, 2.65]."""

    def __init__(self, cftr_open=0.0, nhe3_rate=1.0, sglt1_rate=1.0, cholera=False, seed=11):
        self.cftr_t = ValueTracker(cftr_open)
        self.nhe3_t = ValueTracker(nhe3_rate)
        self.sglt1_t = ValueTracker(sglt1_rate)
        self.cholera = cholera
        self.rng = np.random.default_rng(seed)

        self.root = VGroup()
        self._t = 0.0

        # Blood band along bottom (y = -2.45..-1.75)
        self.blood_band = Polygon(
            [-6.30, -2.45, 0], [1.90, -2.45, 0], [1.90, -1.75, 0], [-6.30, -1.75, 0],
            fill_color=BLOOD_BG, fill_opacity=1.0, stroke_color=CELL_EDGE, stroke_width=2.0,
        )
        self.blood_label = T("blood", 24, BAR_WHITE).move_to([-5.65, -2.10, 0])

        self.blood_dots = VGroup()
        for _ in range(16):
            d = Dot(radius=0.048, color=PUMP_RED).set_opacity(0.42)
            d._bx = float(self.rng.uniform(-4.75, 1.80))
            d._by = float(self.rng.uniform(-2.32, -1.88))
            d.move_to([d._bx, d._by, 0])
            self.blood_dots.add(d)

        # ---- CRYPT CELLS (left, x = -6.28 to -2.20) ----
        self.crypt_outer = Polygon(
            [-6.28, -1.20, 0], [-5.80, -1.20, 0], [-5.80, 1.25, 0], [-6.28, 1.25, 0],
            fill_color=CELL_FILL, fill_opacity=0.85, stroke_color=CELL_EDGE, stroke_width=2.5,
        )
        self.crypt_cell = RoundedRectangle(
            corner_radius=0.12, width=2.22, height=1.25,
            fill_color=CELL_FILL, fill_opacity=0.88, stroke_color=CELL_EDGE, stroke_width=2.5,
        ).move_to([-4.66, -0.58, 0])  # x: -5.77..-3.55, y: -1.205..+0.045
        self.crypt_right_cell = RoundedRectangle(
            corner_radius=0.12, width=0.95, height=1.25,
            fill_color=CELL_FILL, fill_opacity=0.85, stroke_color=CELL_EDGE, stroke_width=2.5,
        ).move_to([-2.65, -0.58, 0])  # gap at x = -3.55..-3.125

        # ---- VILLUS (right, curved arch rising above crypt) ----
        self.villus_base = Polygon(
            [-1.78, -1.20, 0], [1.56, -1.20, 0], [1.56, 0.15, 0], [-1.78, 0.15, 0],
            fill_color=CELL_FILL, fill_opacity=0.45, stroke_color=CELL_EDGE, stroke_width=2.0,
        )
        self.villus_cell = RoundedRectangle(
            corner_radius=0.28, width=3.24, height=1.30,
            fill_color=CELL_FILL, fill_opacity=0.88, stroke_color=CELL_EDGE, stroke_width=2.5,
        ).move_to([-0.10, 0.70, 0])  # x: -1.72..+1.52, y: +0.05..+1.35

        # ---- CRYPT TRANSPORTERS ----
        # RED Na+ pump at base (-5.62, -1.20)
        self.pump_c = np.array([-5.62, -1.20, 0.0])
        self._pump_scale = 1.0
        self.pump_icon = VGroup(
            Circle(radius=0.17, fill_color=PUMP_RED, fill_opacity=0.94, stroke_color=BAR_WHITE, stroke_width=2.0),
            Line([-0.08, 0, 0], [0.08, 0, 0], stroke_color=BAR_WHITE, stroke_width=2.5),
        ).move_to(self.pump_c)
        self.pump_label = T("Na+ pump", 22, PUMP_RED).move_to([-5.76, -1.53, 0])

        # NKCC1 carrier at base (-3.70, -1.20); uptake dots at -3.60; label cleanly left at -4.24
        self.nkcc1_icon = RoundedRectangle(
            corner_radius=0.06, width=0.38, height=0.26,
            fill_color=CL_GREEN, fill_opacity=0.28, stroke_color=CL_GREEN, stroke_width=2.5,
        ).move_to([-3.70, -1.20, 0])
        self.nkcc1_label = T("NKCC1", 22, CL_GREEN).move_to([-4.24, -1.53, 0])

        # CFTR hinged channel at apical top (-4.52, +0.05)
        self.show_cftr = ValueTracker(1.0)
        self.cftr_pivot_l = np.array([-4.74, 0.05, 0.0])
        self.cftr_pivot_r = np.array([-4.30, 0.05, 0.0])
        self.cftr_gate = always_redraw(self._mk_cftr_gate)
        # Cleanly right of crypt_outer (-5.80) and left of Cl- stream (-4.52)
        self.cftr_label = T("CFTR", 24, CL_GREEN).move_to([-5.26, 0.56, 0])

        # ---- VILLUS TRANSPORTERS ----
        # NHE3 + partner on left top of villus cell (x = -1.16, -0.78)
        self.nhe3_icon = VGroup(
            RoundedRectangle(corner_radius=0.05, width=0.28, height=0.24, fill_color=NA_BLUE, fill_opacity=0.55,
                             stroke_color=NA_BLUE, stroke_width=2.5).move_to([-1.16, 1.35, 0]),
            RoundedRectangle(corner_radius=0.05, width=0.28, height=0.24, fill_color=CL_GREEN, fill_opacity=0.55,
                             stroke_color=CL_GREEN, stroke_width=2.5).move_to([-0.78, 1.35, 0]),
        )
        self.nhe3_label = T("NHE3 + partner", 24, BAR_WHITE).move_to([-0.98, 2.48, 0])

        # SGLT1 rotating turnstile on right top of villus cell (+0.96, +1.35)
        self.sglt1_c = np.array([0.96, 1.35, 0.0])
        self.sglt1_ring = Circle(radius=0.24, fill_color=CELL_FILL, fill_opacity=0.95,
                                 stroke_color=SUGAR_GOLD, stroke_width=2.8).move_to(self.sglt1_c)
        self.sglt1_spokes = VGroup(
            Line(self.sglt1_c + LEFT * 0.21, self.sglt1_c + RIGHT * 0.21, stroke_color=SUGAR_GOLD, stroke_width=2.5),
            Line(self.sglt1_c + DOWN * 0.21, self.sglt1_c + UP * 0.21, stroke_color=SUGAR_GOLD, stroke_width=2.5),
        )
        self.sglt1_label = T("SGLT1", 24, SUGAR_GOLD).move_to([0.98, 2.48, 0])

        # ---- PARTICLES ----
        # Gut lumen ambient fluid stream passing rightward across top (y = 1.62..2.12, clear of top labels at 2.48)
        self.lumen_flow = VGroup()
        for j in range(12):
            d = Dot(radius=0.068, color=CYAN)
            d._lx = -5.4 + j * 0.60
            d._ly = 1.65 + (j % 3) * 0.18
            d.move_to([d._lx, d._ly, 0])
            self.lumen_flow.add(d)

        # NKCC1 Cl- dots entering from below into crypt cell (-3.92, y = -1.68..-0.75)
        self.crypt_nkcc1_in = VGroup()
        for j in range(5):
            d = Dot(radius=0.062, color=CL_GREEN)
            d._ph = j / 5.0
            self.crypt_nkcc1_in.add(d)

        # Crypt packed Cl- inside upper half of focus crypt cell (leaves lower half clear for G protein in s11!)
        self.crypt_cl_inside = VGroup()
        for j in range(8):
            d = Dot(radius=0.058, color=CL_GREEN)
            d._cx = -5.45 + (j % 4) * 0.34 + 0.14 * (j // 4)
            d._cy = -0.32 + (j // 4) * 0.22
            d.move_to([d._cx, d._cy, 0])
            self.crypt_cl_inside.add(d)

        # Crypt Cl- stream through CFTR (x = -4.52)
        self.crypt_cl_stream = VGroup()
        for j in range(8):
            d = Dot(radius=0.066, color=CL_GREEN)
            d._ph = j / 8.0
            self.crypt_cl_stream.add(d)

        # Crypt paracellular Na+ stream through gap (x = -3.34)
        self.crypt_na_stream = VGroup()
        for j in range(7):
            d = Dot(radius=0.064, color=NA_BLUE)
            d._ph = j / 7.0
            self.crypt_na_stream.add(d)

        # Crypt osmotic water drops rising beside gap/CFTR (x = -3.76)
        self.crypt_h2o_stream = VGroup()
        for j in range(7):
            d = Dot(radius=0.070, color=CYAN)
            d._ph = j / 7.0
            self.crypt_h2o_stream.add(d)

        # Villus NHE3 Na+ and Cl- entering (x = -1.16, -0.78 from y = 2.02 down to 0.72)
        self.villus_nhe3_dots = VGroup()
        for j in range(5):
            na = Dot(radius=0.058, color=NA_BLUE)
            cl = Dot(radius=0.058, color=CL_GREEN)
            na._ph = j / 5.0
            cl._ph = (j + 0.5) / 5.0 % 1.0
            na._kind, cl._kind = "na", "cl"
            self.villus_nhe3_dots.add(na, cl)

        # Villus SGLT1 2 Na+ + 1 sugar entering (+0.96 from y = 2.02 down to 0.72)
        self.villus_sglt1_dots = VGroup()
        for j in range(4):
            na1 = Dot(radius=0.054, color=NA_BLUE)
            na2 = Dot(radius=0.054, color=NA_BLUE)
            sug = Dot(radius=0.068, color=SUGAR_GOLD)
            na1._ph = j / 4.0
            na2._ph = j / 4.0
            sug._ph = j / 4.0
            na1._off, na2._off, sug._off = -0.11, 0.11, 0.0
            na1._dy, na2._dy, sug._dy = 0.08, 0.08, -0.06
            self.villus_sglt1_dots.add(na1, na2, sug)

        # Villus absorbed water crossing from gut (y = 1.98) down through villus into blood (y = -2.02) at x = +0.54..0.68
        self.villus_h2o_stream = VGroup()
        for j in range(8):
            d = Dot(radius=0.068, color=CYAN)
            d._ph = j / 8.0
            d._x = 0.54 + (j % 2) * 0.14
            self.villus_h2o_stream.add(d)

        # Layer flags
        self.show_pump = ValueTracker(1.0)
        self.show_nkcc1 = ValueTracker(1.0)
        self.show_cl_inside = ValueTracker(1.0)
        self.show_na_para = ValueTracker(1.0)
        self.show_crypt_h2o = ValueTracker(1.0)
        self.show_villus_nhe3 = ValueTracker(1.0)
        self.show_villus_sglt1 = ValueTracker(1.0)
        self.show_villus_sglt1_label = ValueTracker(1.0)
        self.show_villus_h2o = ValueTracker(1.0)

        self.root.add(
            self.blood_band, self.blood_dots, self.blood_label,
            self.lumen_flow,
            self.crypt_outer, self.crypt_cell, self.crypt_right_cell,
            self.villus_base, self.villus_cell,
            self.pump_icon, self.pump_label,
            self.nkcc1_icon, self.nkcc1_label,
            self.cftr_gate, self.cftr_label,
            self.nhe3_icon, self.nhe3_label,
            self.sglt1_ring, self.sglt1_spokes, self.sglt1_label,
            self.crypt_nkcc1_in, self.crypt_cl_inside, self.crypt_cl_stream,
            self.crypt_na_stream, self.crypt_h2o_stream,
            self.villus_nhe3_dots, self.villus_sglt1_dots, self.villus_h2o_stream,
        )
        self.root.add_updater(lambda m, dt: self._step(dt))
        self._step(0.0)

    def _mk_cftr_gate(self):
        op = float(np.clip(self.cftr_t.get_value(), 0.0, 1.0))
        vis = float(np.clip(self.show_cftr.get_value(), 0.0, 1.0))
        ang = op * 1.15
        l_end = self.cftr_pivot_l + np.array([0.22 * np.cos(ang), 0.22 * np.sin(ang), 0.0])
        r_end = self.cftr_pivot_r + np.array([-0.22 * np.cos(ang), 0.22 * np.sin(ang), 0.0])
        return VGroup(
            Line(self.cftr_pivot_l, l_end, stroke_color=CL_GREEN, stroke_width=5.0, stroke_opacity=vis),
            Line(self.cftr_pivot_r, r_end, stroke_color=CL_GREEN, stroke_width=5.0, stroke_opacity=vis),
        )

    def _step(self, dt):
        self._t += dt
        cftr = float(np.clip(self.cftr_t.get_value(), 0.0, 1.0))
        nhe3 = float(np.clip(self.nhe3_t.get_value(), 0.0, 1.0))
        sglt1 = float(np.clip(self.sglt1_t.get_value(), 0.0, 1.0))

        for d in self.blood_dots:
            d._bx += 0.45 * dt
            if d._bx > 1.80:
                d._bx = -4.75
            d.move_to([d._bx, d._by, 0])

        # Lumen water drops moving rightward in gut lumen above epithelium
        for d in self.lumen_flow:
            d._lx += 0.72 * dt
            if d._lx > 1.75:
                d._lx = -5.65
            d.move_to([d._lx, d._ly, 0])

        self.sglt1_spokes.rotate(1.6 * sglt1 * dt, about_point=self.sglt1_c)

        sp = float(self.show_pump.get_value())
        sn = float(self.show_nkcc1.get_value())
        self.pump_icon.set_opacity(sp)
        self.pump_label.set_opacity(sp)
        if sp > 0.5:
            s_pump = 1.0 + 0.12 * np.sin(4.0 * self._t)
            self.pump_icon.scale(s_pump / self._pump_scale)
            self._pump_scale = s_pump
        self.nkcc1_icon.set_opacity(sn)
        self.nkcc1_label.set_opacity(sn)

        # NKCC1 loading Cl- from interstitium/blood into crypt cell
        for d in self.crypt_nkcc1_in:
            d._ph = (d._ph + 0.55 * dt) % 1.0
            if sn < 0.05:
                d.set_opacity(0.0)
                continue
            y = -1.68 + d._ph * 0.92
            d.move_to([-3.60, y, 0])
            d.set_opacity(0.95 * sn)

        ci = float(self.show_cl_inside.get_value())
        for j, d in enumerate(self.crypt_cl_inside):
            d.set_opacity(0.92 * ci)
            d.move_to([d._cx + 0.05 * np.sin(2.5 * self._t + j), d._cy + 0.04 * np.cos(2.1 * self._t + j), 0])

        # Cl- pouring through CFTR
        cl_spd = 0.48 + 0.45 * cftr
        for d in self.crypt_cl_stream:
            d._ph = (d._ph + cl_spd * dt) % 1.0
            if cftr < 0.08:
                d.set_opacity(0.0)
                continue
            y = -0.10 + d._ph * 2.15
            x = -4.52 + max(0.0, d._ph - 0.65) * 1.1
            d.move_to([x, y, 0])
            d.set_opacity(0.95 * min(1.0, cftr * 1.4))

        # Paracellular Na+ through gap
        np_on = float(self.show_na_para.get_value())
        for d in self.crypt_na_stream:
            d._ph = (d._ph + (0.45 + 0.35 * cftr) * dt) % 1.0
            if np_on < 0.05:
                d.set_opacity(0.0)
                continue
            y = -1.55 + d._ph * 3.25
            d.move_to([-3.34, y, 0])
            d.set_opacity(0.95 * np_on)

        # Crypt water following
        ch_on = float(self.show_crypt_h2o.get_value())
        for d in self.crypt_h2o_stream:
            d._ph = (d._ph + (0.42 + 0.35 * cftr) * dt) % 1.0
            if ch_on < 0.05:
                d.set_opacity(0.0)
                continue
            y = -1.55 + d._ph * 3.35
            d.move_to([-3.55, y, 0])
            d.set_opacity(0.94 * ch_on)

        # Villus NHE3 + partner (keep label readable at >= 0.72 opacity even when slowed)
        vn_on = float(self.show_villus_nhe3.get_value())
        self.nhe3_icon.set_opacity(vn_on * (0.35 + 0.65 * nhe3))
        self.nhe3_label.set_opacity(vn_on * (0.72 + 0.28 * nhe3))
        for d in self.villus_nhe3_dots:
            d._ph = (d._ph + 0.45 * max(nhe3, 0.15) * dt) % 1.0
            if vn_on < 0.05:
                d.set_opacity(0.0)
                continue
            x = -1.16 if d._kind == "na" else -0.78
            y = 2.02 - d._ph * 1.28
            d.move_to([x, y, 0])
            d.set_opacity(0.95 * vn_on * (0.35 + 0.65 * nhe3))

        # Villus SGLT1 (2 Na + 1 sugar)
        vs_on = float(self.show_villus_sglt1.get_value())
        vsl_on = float(self.show_villus_sglt1_label.get_value())
        self.sglt1_ring.set_opacity(vs_on)
        self.sglt1_spokes.set_opacity(vs_on)
        self.sglt1_label.set_opacity(vs_on * vsl_on)
        for d in self.villus_sglt1_dots:
            d._ph = (d._ph + 0.42 * sglt1 * dt) % 1.0
            if vs_on < 0.05:
                d.set_opacity(0.0)
                continue
            x = 0.96 + d._off
            y = 2.02 - d._ph * 1.28 + d._dy
            d.move_to([x, y, 0])
            d.set_opacity(0.95 * vs_on)

        # Villus water moving from gut into blood
        vh_on = float(self.show_villus_h2o.get_value())
        vh_spd = 0.24 + 0.26 * nhe3
        for idx, d in enumerate(self.villus_h2o_stream):
            d._ph = (d._ph + vh_spd * dt) % 1.0
            if vh_on < 0.05 or (nhe3 < 0.5 and idx % 2 == 1):
                d.set_opacity(0.0)
                continue
            y = 1.98 - d._ph * 4.00
            d.move_to([d._x, y, 0])
            d.set_opacity(0.92 * vh_on)


def build_world(load=11.0, cap=0.99, drink=2.0, inlets=5.0, colon=0.0, stool_vis=1.0, drip_vis=1.0,
                stool_override=None, show_numbers=True, split_load=False, tag_text="teaching numbers"):
    load_t = ValueTracker(load)
    cap_t = ValueTracker(cap)
    drink_t = ValueTracker(drink)
    inlets_t = ValueTracker(inlets)
    colon_t = ValueTracker(colon)
    stool_vis_t = ValueTracker(stool_vis)
    drip_vis_t = ValueTracker(drip_vis)
    stool_override_t = ValueTracker(stool_override) if stool_override is not None else None
    tube = GutTubeWorld(load_t, cap_t, inlets_t, colon_t, drip_vis_t=drip_vis_t, stool_override_t=stool_override_t)
    ledger = LedgerRig(load_t, cap_t, drink_t=drink_t, stool_vis_t=stool_vis_t, stool_override_t=stool_override_t,
                       show_numbers=show_numbers, split_load=split_load, tag_text=tag_text)
    return dict(
        load_t=load_t, cap_t=cap_t, drink_t=drink_t, inlets_t=inlets_t, colon_t=colon_t,
        stool_vis_t=stool_vis_t, drip_vis_t=drip_vis_t, stool_override_t=stool_override_t,
        tube=tube, ledger=ledger, group=VGroup(tube.root, ledger.root),
    )


def option_cards():
    ca = boxed_label("A: load 12 L, 99%", BAR_WHITE, size=24, pad=0.14)
    cb = boxed_label("B: load 11 L, 98%", BAR_WHITE, size=24, pad=0.14)
    row = VGroup(ca, cb).arrange(RIGHT, buff=0.22).move_to([3.55, 2.95, 0])
    return row, ca, cb


# ------------------------------------------------------------------ SCENES
class S00Hook(SpokenScene):
    def construct(self):
        w = build_world(load=0.0, cap=0.99, inlets=0.0)
        self.add(w["group"])

        self.at("9 to 11")
        self.play(w["load_t"].animate.set_value(11.0), run_time=2.6)

        self.at("A couple of hundred")
        self.wait(0.8)

        self.at("Where did that water go")
        q = T("Where did the water go?", 34, BAR_WHITE).move_to([-2.0, 3.15, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=0.0)
        q = T("Where did the water go?", 34, BAR_WHITE).move_to([-2.0, 3.15, 0])
        title = T("What the Gut Lets Go", 42, BAR_WHITE, font=TITLE_FONT).move_to([-2.0, 3.15, 0])
        rule = Line([-4.2, 2.78, 0], [0.2, 2.78, 0], color=SUGAR_GOLD, stroke_width=3.5)
        self.add(w["group"], q)

        self.play(
            swap(q, title, run_time=0.6),
            GrowFromCenter(rule, run_time=0.6),
            w["load_t"].animate(run_time=0.6).set_value(0.0),
        )
        self.play(w["cap_t"].animate(run_time=0.5).set_value(0.0))
        self.wait(max(0.05, self.narration_s - 1.55))
        self.play(FadeOut(title), FadeOut(rule), run_time=0.4)
        self.finish()


class S02Load(SpokenScene):
    def construct(self):
        w = build_world(load=0.0, cap=0.0, drink=0.0, inlets=0.0, stool_vis=0.0, drip_vis=0.0, split_load=True)
        self.add(w["group"])
        L = w["ledger"]

        self.at("what you drink")
        drink_lab = T("drink: 2", 22, CYAN).move_to([4.35, L.y_for_load(1.0), 0])
        self.play(
            w["drink_t"].animate.set_value(2.0),
            w["load_t"].animate.set_value(2.0),
            run_time=0.8,
        )
        self.play(FadeIn(drink_lab), run_time=0.4)

        self.at("secretions")
        sec_lab = VGroup(
            T("secretions: 9", 22, "#8FF0FF"),
            T("(round)", 22, "#8FF0FF"),
        ).arrange(DOWN, buff=0.06).move_to([4.30, L.y_for_load(6.5), 0])
        self.play(
            w["inlets_t"].animate.set_value(5.0),
            w["load_t"].animate.set_value(11.0),
            run_time=4.8,
        )
        self.play(FadeIn(sec_lab), run_time=0.6)

        self.at("About 99")
        self.play(w["cap_t"].animate.set_value(0.99), run_time=1.5)
        self.finish()


class S03Rule(SpokenScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0, stool_vis=0.0, drip_vis=1.0, split_load=True)
        L = w["ledger"]
        drink_lab = T("drink: 2", 22, CYAN).move_to([4.35, L.y_for_load(1.0), 0])
        sec_lab = VGroup(
            T("secretions: 9", 22, "#8FF0FF"),
            T("(round)", 22, "#8FF0FF"),
        ).arrange(DOWN, buff=0.06).move_to([4.30, L.y_for_load(6.5), 0])
        self.add(w["group"], drink_lab, sec_lab)

        self.at("what leaves")
        ring_out = Circle(radius=0.38, color=SUGAR_GOLD, stroke_width=3.5).move_to([1.62, 0.42, 0])
        self.play(Create(ring_out), run_time=0.7)

        self.at("Stool water equals")
        rule_txt = M("stool water = load × (1 − captured)", 30, BAR_WHITE).move_to([-1.8, -3.15, 0])
        self.play(Write(rule_txt), FadeOut(drink_lab), FadeOut(sec_lab), run_time=2.4)

        self.at("11 liters")
        y_top_11 = L.y_for_load(11.0)
        sliver = Rectangle(width=L.bar_w - 0.04, height=0.10, fill_color=CYAN, fill_opacity=0.95, stroke_width=0)
        sliver.move_to([L.load_x, y_top_11, 0])
        h_011 = L.y_for_stool(0.11) - L.bar_y0
        target_sliver = Rectangle(
            width=L.bar_w - 0.04, height=h_011, fill_color=BAR_WHITE, fill_opacity=0.90, stroke_width=0,
        ).move_to([L.stool_x, L.bar_y0 + h_011 / 2, 0])
        self.add(sliver)
        self.play(
            Transform(sliver, target_sliver),
            w["stool_vis_t"].animate.set_value(1.0),
            run_time=1.8,
        )
        self.remove(sliver)
        self.play(FadeOut(ring_out), run_time=0.4)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        # Lock stool_water at 0.11 while option B needle twitches toward 98% and back
        w = build_world(load=11.0, cap=0.99, inlets=5.0, stool_override=0.11)
        L = w["ledger"]
        self.add(w["group"])

        self.at("Try two changes")
        row, ca, cb = option_cards()
        self.play(FadeIn(row, shift=DOWN * 0.2), run_time=1.0)

        self.at("Add one liter")
        ghost = Rectangle(
            width=L.bar_w - 0.04, height=L.y_for_load(12.0) - L.y_for_load(11.0),
            fill_color=CYAN, fill_opacity=0.35, stroke_color=CYAN, stroke_width=2.5,
        ).move_to([L.load_x, (L.y_for_load(11.0) + L.y_for_load(12.0)) / 2, 0])
        self.play(ca.animate.set_stroke(SUGAR_GOLD, 3.5), FadeIn(ghost), run_time=1.2)

        self.at("Or keep the load")
        self.play(
            ca.animate.set_stroke(BAR_WHITE, 2.5),
            FadeOut(ghost),
            cb.animate.set_stroke(SUGAR_GOLD, 3.5),
            run_time=0.6,
        )
        self.play(w["cap_t"].animate.set_value(0.98), run_time=0.7)
        self.play(w["cap_t"].animate.set_value(0.99), run_time=0.7)

        self.at("which raises")
        q = question_card("Which raises stool water more?", y=3.15, color=BAR_WHITE, size=32, left=-6.3, max_w=6.8)
        self.play(cb.animate.set_stroke(BAR_WHITE, 2.5), FadeIn(q), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which raises stool water more?"
    CARD = {"y": 3.15, "color": BAR_WHITE, "size": 32, "left": -6.3, "max_w": 6.8}
    RING_AT = (1.55, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0)
        row, _, _ = option_cards()
        return Group(w["group"], row)


class S06Answer(SpokenScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0)
        L = w["ledger"]
        row, ca, cb = option_cards()
        q = question_card("Which raises stool water more?", y=3.15, color=BAR_WHITE, size=32, left=-6.3, max_w=6.8)
        self.add(w["group"], row, q)

        self.at("The extra liter")
        self.play(FadeOut(q), ca.animate.set_stroke(SUGAR_GOLD, 3.5), run_time=0.6)
        self.play(w["load_t"].animate.set_value(12.0), run_time=1.8)
        mark_a = Line(
            [L.stool_x - L.bar_w / 2 - 0.14, L.y_for_stool(0.12), 0],
            [L.stool_x - L.bar_w / 2, L.y_for_stool(0.12), 0],
            stroke_color=SUGAR_GOLD, stroke_width=3.5,
        )
        lab_a = M("A: 0.12", 22, SUGAR_GOLD).next_to(mark_a, LEFT, buff=0.08)
        self.play(Create(mark_a), FadeIn(lab_a), run_time=0.7)

        self.at("One point less")
        self.play(
            ca.animate.set_stroke(BAR_WHITE, 2.5),
            cb.animate.set_stroke(SUGAR_GOLD, 3.5),
            w["load_t"].animate.set_value(11.0),
            run_time=0.9,
        )
        self.play(w["cap_t"].animate.set_value(0.98), run_time=1.8)
        mark_b = Line(
            [L.stool_x - L.bar_w / 2 - 0.14, L.y_for_stool(0.22), 0],
            [L.stool_x - L.bar_w / 2, L.y_for_stool(0.22), 0],
            stroke_color=SUGAR_GOLD, stroke_width=3.5,
        )
        lab_b = M("B: 0.22", 22, SUGAR_GOLD).next_to(mark_b, LEFT, buff=0.08)
        self.play(Create(mark_b), FadeIn(lab_b), run_time=0.7)

        self.at("It doubles")
        y11 = L.y_for_stool(0.11)
        y22 = L.y_for_stool(0.22)
        bx = L.stool_x + L.bar_w / 2 + 0.16
        br = VMobject(stroke_color=BAR_WHITE, stroke_width=3.0).set_points_as_corners([
            [bx - 0.08, y11, 0], [bx, y11, 0], [bx, y22, 0], [bx - 0.08, y22, 0],
        ])
        x2_lab = M("× 2", 24, BAR_WHITE).move_to([bx + 0.34, (y11 + y22) / 2, 0])
        self.play(Create(br), FadeIn(x2_lab), run_time=0.8)
        self.finish()


class S07Idea(SpokenScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0)
        self.add(w["group"])
        top_eq = M("residue = load × (1 − captured)", 32, BAR_WHITE).move_to([-1.2, 3.15, 0])
        self.play(FadeIn(top_eq), run_time=0.7)

        self.at("small residue")
        mouth_ring = Circle(radius=0.55, color=CYAN, stroke_width=3.5).move_to([-5.65, 0.72, 0])
        out_ring = Circle(radius=0.35, color=SUGAR_GOLD, stroke_width=3.5).move_to([1.62, 0.42, 0])
        self.play(Create(mouth_ring), Create(out_ring), run_time=0.8)
        self.wait(0.8)
        self.play(FadeOut(mouth_ring), FadeOut(out_ring), run_time=0.5)

        self.at("When capture")
        for tgt in (0.98, 0.99, 0.98, 0.99):
            self.play(w["cap_t"].animate.set_value(tgt), run_time=0.9)

        self.at("A bigger load")
        self.play(w["load_t"].animate.set_value(12.0), run_time=1.0)
        self.play(w["load_t"].animate.set_value(11.0), run_time=0.9)
        self.finish()


class S08Crypt(SpokenScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0)
        self.add(w["group"])

        cv = CryptVillusWorld(cftr_open=0.0, nhe3_rate=0.0, sglt1_rate=0.0)
        cv.show_pump.set_value(0.0)
        cv.show_nkcc1.set_value(0.0)
        cv.show_cl_inside.set_value(0.0)
        cv.show_na_para.set_value(0.0)
        cv.show_crypt_h2o.set_value(0.0)
        cv.show_villus_nhe3.set_value(0.0)
        cv.show_villus_sglt1.set_value(0.0)
        cv.show_villus_sglt1_label.set_value(0.0)
        cv.show_villus_h2o.set_value(0.0)
        cv.cftr_label.set_opacity(0.0)
        cv.show_cftr.set_value(0.0)

        self.at("In pits called crypts")
        self.play(FadeOut(w["tube"].root), FadeIn(cv.root), run_time=1.0)
        self.remove(w["tube"].root)

        self.at("sodium pump")
        self.play(cv.show_pump.animate.set_value(1.0), run_time=0.7)

        self.at("NKCC1")
        self.play(
            cv.show_nkcc1.animate.set_value(1.0),
            cv.show_cl_inside.animate.set_value(1.0),
            run_time=1.4,
        )

        self.at("When the channel")
        self.play(
            cv.show_cftr.animate.set_value(1.0),
            cv.cftr_label.animate.set_opacity(1.0),
            cv.cftr_t.animate.set_value(0.85),
            run_time=1.2,
        )

        self.at("chloride pours")
        self.wait(0.8)

        self.at("Sodium follows")
        self.play(cv.show_na_para.animate.set_value(1.0), run_time=0.8)

        self.at("water follows")
        self.play(
            cv.show_crypt_h2o.animate.set_value(1.0),
            w["load_t"].animate.set_value(11.6),
            run_time=1.2,
        )
        self.finish()


class S09Villus(SpokenScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0)
        cv = CryptVillusWorld(cftr_open=0.65, nhe3_rate=1.0, sglt1_rate=1.0)
        cv.show_villus_nhe3.set_value(0.0)
        cv.show_villus_sglt1.set_value(0.0)
        cv.show_villus_sglt1_label.set_value(0.0)
        cv.show_villus_h2o.set_value(0.0)
        self.add(w["ledger"].root, cv.root)

        arr_crypt = Arrow([-6.04, 0.35, 0], [-6.04, 1.85, 0], color=CL_GREEN, stroke_width=5, buff=0)
        arr_villus = Arrow([1.72, 1.55, 0], [1.72, -1.05, 0], color=CYAN, stroke_width=5, buff=0)

        self.at("On the fingers")
        self.play(GrowArrow(arr_crypt), GrowArrow(arr_villus), run_time=1.2)

        self.at("NHE3")
        self.play(cv.show_villus_nhe3.animate.set_value(1.0), run_time=1.4)

        self.at("SGLT1")
        self.play(
            cv.show_villus_sglt1.animate.set_value(1.0),
            cv.show_villus_sglt1_label.animate.set_value(1.0),
            run_time=1.4,
        )

        self.at("Water follows")
        self.play(cv.show_villus_h2o.animate.set_value(1.0), run_time=1.2)
        self.finish()


class S10Balance(SpokenScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0)
        cv = CryptVillusWorld(cftr_open=0.65, nhe3_rate=1.0, sglt1_rate=1.0)
        arr_crypt = Arrow([-6.04, 0.35, 0], [-6.04, 1.85, 0], color=CL_GREEN, stroke_width=5, buff=0)
        lab_sec = T("mostly secrete", 24, CL_GREEN).move_to([-5.05, 2.45, 0])
        arr_villus = Arrow([1.72, 1.55, 0], [1.72, -1.05, 0], color=CYAN, stroke_width=5, buff=0)
        lab_abs = T("mostly absorb", 24, CYAN).move_to([-0.85, -1.48, 0])
        self.add(w["ledger"].root, cv.root, arr_crypt, arr_villus)

        self.at("Secretion mostly")
        self.play(FadeIn(lab_sec), arr_crypt.animate.set_stroke(width=8), run_time=0.8)

        self.at("and absorption mostly")
        self.play(FadeIn(lab_abs), arr_villus.animate.set_stroke(width=8), run_time=0.8)

        self.at("one cell can")
        small_cftr = VGroup(
            Line([-0.25, 1.35, 0], [-0.08, 1.50, 0], stroke_color=CL_GREEN, stroke_width=4),
            Line([0.12, 1.35, 0], [-0.05, 1.50, 0], stroke_color=CL_GREEN, stroke_width=4),
        )
        small_cftr_lab = T("CFTR", 22, CL_GREEN).move_to([-0.06, 1.05, 0])
        self.play(FadeIn(small_cftr), FadeIn(small_cftr_lab), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(small_cftr), FadeOut(small_cftr_lab), run_time=0.5)

        self.at("Stool water is")
        self.play(
            FadeOut(cv.root), FadeOut(arr_crypt), FadeOut(lab_sec), FadeOut(arr_villus), FadeOut(lab_abs),
            FadeIn(w["tube"].root),
            run_time=1.0,
        )
        self.remove(cv.root)
        out_ring = Circle(radius=0.35, color=SUGAR_GOLD, stroke_width=3.5).move_to([1.62, 0.42, 0])
        self.play(Create(out_ring), run_time=0.5)
        self.play(FadeOut(out_ring), run_time=0.5)

        self.at("the colon")
        colon_lab = T("colon: up to 4-5 L a day", 24, CYAN).move_to([-0.15, 2.42, 0])
        self.play(w["colon_t"].animate.set_value(1.0), FadeIn(colon_lab), run_time=1.4)
        self.finish()


class S11Cholera(SpokenScene):
    def construct(self):
        w = build_world(load=11.0, cap=0.99, inlets=5.0, show_numbers=True, tag_text="teaching numbers")
        L = w["ledger"]
        cv = CryptVillusWorld(cftr_open=0.55, nhe3_rate=1.0, sglt1_rate=1.0, cholera=True)
        # Keep SGLT1 unlabelled and unhighlighted per visual note
        cv.show_villus_sglt1_label.set_value(0.0)

        self.add(w["group"])
        new_tag = scope_tag("schematic", size=24, color=BAR_WHITE)
        self.play(
            FadeOut(w["tube"].root),
            FadeIn(cv.root),
            swap(L.tag, new_tag, run_time=0.6),
            run_time=1.1,
        )
        self.remove(w["tube"].root)
        L.tag = new_tag
        L.show_numbers = False

        self.at("Its toxin")
        toxins = VGroup(
            RoundedRectangle(corner_radius=0.08, width=0.36, height=0.20, fill_color=TOXIN_MAG, fill_opacity=0.92,
                             stroke_color=BAR_WHITE, stroke_width=1.5).move_to([-4.10, 1.95, 0]),
            RoundedRectangle(corner_radius=0.08, width=0.36, height=0.20, fill_color=TOXIN_MAG, fill_opacity=0.92,
                             stroke_color=BAR_WHITE, stroke_width=1.5).move_to([0.20, 1.95, 0]),
        )
        self.play(FadeIn(toxins), run_time=0.4)
        self.play(
            toxins[0].animate.move_to([-4.15, 0.16, 0]),
            toxins[1].animate.move_to([-0.20, 1.46, 0]),
            run_time=0.8,
        )

        self.at("G protein")
        # Opaque backing on G protein switches keeps them crisp and clear of dots
        gp_crypt = boxed_label("G protein: on", TOXIN_MAG, size=22, pad=0.09, fill_opacity=0.0).move_to([-4.72, -0.66, 0])
        gp_crypt_bg = RoundedRectangle(corner_radius=0.12, width=gp_crypt.box.width, height=gp_crypt.box.height,
                                       fill_color=BG, fill_opacity=0.94, stroke_width=0).move_to(gp_crypt)
        gp_villus = boxed_label("G protein: on", TOXIN_MAG, size=22, pad=0.09, fill_opacity=0.0).move_to([-0.32, 0.36, 0])
        gp_villus_bg = RoundedRectangle(corner_radius=0.12, width=gp_villus.box.width, height=gp_villus.box.height,
                                        fill_color=BG, fill_opacity=0.94, stroke_width=0).move_to(gp_villus)
        self.play(FadeIn(gp_crypt_bg), FadeIn(gp_crypt), FadeIn(gp_villus_bg), FadeIn(gp_villus), run_time=0.9)

        self.at("keep making")
        camp_lab = T("cyclic\nAMP", 22, TOXIN_MAG, line_spacing=0.75).move_to([-0.12, 0.98, 0])
        self.play(
            cv.crypt_cell.animate.set_fill(TOXIN_MAG, opacity=0.28),
            cv.villus_cell.animate.set_fill(TOXIN_MAG, opacity=0.28),
            FadeIn(camp_lab),
            run_time=1.1,
        )

        self.at("In the crypts")
        self.play(
            cv.cftr_t.animate.set_value(1.0),
            w["load_t"].animate.set_value(12.5),
            run_time=1.8,
        )

        self.at("On the villi")
        self.play(
            cv.nhe3_t.animate.set_value(0.22),
            w["cap_t"].animate.set_value(0.90),
            run_time=2.0,
        )
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        w = build_world(load=12.4, cap=0.92, inlets=5.0, show_numbers=False, tag_text="schematic")
        L = w["ledger"]
        cv = CryptVillusWorld(cftr_open=1.0, nhe3_rate=0.25, sglt1_rate=1.0, cholera=True)
        cv.show_villus_sglt1_label.set_value(0.0)
        cv._step(0.0)
        cv.sglt1_label.set_opacity(0.0)
        self.add(L.root, cv.root)

        new_tag = scope_tag("teaching numbers", size=24, color=BAR_WHITE)
        self.play(
            FadeOut(cv.root),
            FadeIn(w["tube"].root),
            w["load_t"].animate.set_value(11.0),
            w["cap_t"].animate.set_value(0.99),
            swap(L.tag, new_tag, run_time=0.6),
            run_time=1.2,
        )
        self.remove(cv.root)
        L.tag = new_tag
        L.show_numbers = True

        self.at("takes back")
        wall_glow = Line([-5.2, -0.55, 0], [0.95, -0.55, 0], stroke_color=CYAN, stroke_width=8).set_opacity(0.55)
        self.play(FadeIn(wall_glow), run_time=0.7)
        self.play(FadeOut(wall_glow), run_time=0.7)

        self.at("a small slip")
        self.play(w["cap_t"].animate.set_value(0.98), run_time=1.3)
        self.wait(0.8)
        self.play(w["cap_t"].animate.set_value(0.99), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "When capture is nearly complete, small slips multiply what leaves."
