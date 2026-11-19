"""
Two Taps on One Filter — Glomerular Filtration and Renal Blood Flow

COLOUR MAP (one colour per concept for the whole film, full opacity on BG #0f1117):
  BG          #0f1117  dark background
  COL_PLASMA  #FC6255  (RED)    blood plasma flow dots and broad flow arrow
  COL_PROTEIN #C08CFF  (PURPLE) plasma protein dots, luminal concentration tint, and oncotic pull line
  COL_WATER   #49D8F2  (CYAN)   water/filtrate drops, net filtration gap fill, and filtration curve
  COL_AFFERENT #6BD072 (GREEN)  afferent arteriole (inflow) tube, ring, and tap handle
  COL_EFFERENT #F5D547 (YELLOW) efferent arteriole (outflow) tube, ring, and nozzle
  COL_PUSH    #FF9442  (ORANGE) hydrostatic push line (P_GC - P_BS)
  COL_BOWMAN  #7DB8E8  (BLUE)   Bowman's capsule cup and Bowman's space band
  TEXT        #E8EAF0  (WHITE)  all text labels (full opacity), equilibrium dot, pincers, arterial ceiling, FF curve

ONE WORLD CARRIED FROM SCENE TO SCENE:
  Starts as a glomerular capillary tuft cupped in Bowman's capsule between a GREEN afferent arteriole (left)
  and a YELLOW efferent arteriole (right), with RED plasma and PURPLE protein dots streaming through and
  CYAN filtrate drops dripping out the base. In s02 the tuft unwinds into one straight horizontal capillary
  above a pale BLUE Bowman's space band, and in s04 a push-and-pull pressure strip opens directly above it,
  lined up end-to-end with the capillary. Every subsequent scene (s04-s13) acts directly on that same
  two-tap hose and its aligned strip.

WHAT CHANGES IN EACH SPOKEN SCENE (AND WHAT IT IS COMPUTED FROM):
  s00_hook:        Red/purple dots stream along parametric tuft loops and cyan drops drip out the outlet; white pincers squeeze the yellow vessel as drip rate quickens (2.1x) then slows (0.35x) with alternating up/down arrows.
  s02_filter:      Tuft unwinds into the straight horizontal capillary and Bowman's space band; a magnifier opens on the lower wall showing cyan drops and white solute specks passing three plain stripes while purple protein dots turn back.
  s03_protein:     Capillary filtration ODE drives local plasma velocity v(u) = Q_p(u)/Q_0 so purple protein dots physically crowd left-to-right and luminal purple tint deepens along the capillary while cyan drops leave the bottom wall.
  s04_push_pull:   Aligned strip draws flat orange push = 55 - 15 = 40 mmHg and Starling ODE purple pull rising from 25 to 35.6 mmHg; cyan gap fills between them and drop columns below scale column-by-column with local (push - pull).
  s05_equilibrium: Starling ODE Kf ramps 1.2 -> 4.2 so purple pull steepens to meet orange push at u_eq = 0.67; cyan shading and drops vanish to the right of the equilibrium dot while rat (tick) and human (?) silhouettes appear and clear.
  s06_two_things:  Orange push line pulses with "pressure" label, then a broad red flow arrow grows inside the capillary with brightened red dots and "flow" label while the equilibrium dot and 2/3 filtration pattern hold.
  s07_hose:        Capillary and aligned strip ease smoothly from x=[-4.2,4.2] to [-3.3,3.3] to frame both arterioles; green ring grows a tap handle, yellow ring becomes a nozzle, and the leaky capillary pulses.
  s08_idea:        Series-resistor model (Pa=100, Pv=10, R_A=R_E=1 -> flow 45, P_GC 55) highlights total resistance then efferent share, then live R_A constriction moves flow and push down together while R_E constriction moves flow down and push up.
  s09_predict:     Yellow nozzle tightens in three computed steps (R_E = 1.0 -> 1.5 -> 2.3 -> 3.5); orange push climbs (40 -> 49 -> 57.7 -> 65 mmHg) while flow slows and red arrow thins, with purple pull and drops held neutral for the predict question.
  s11_answer:      Nozzle squeezes further (R_E -> 13.5) and ODE unlocks: red flow crawls, purple dots crowd earlier, purple pull steepens and equilibrium dot slides left enlarging the dry stretch, while orange push climbs in shrinking steps beneath the arterial ceiling (Pa - P_BS = 85).
  s12_biphasic:    Strip morphs into an efferent-squeeze graph; replaying R_E from 1.0 to 3.2 draws the exact ODE biphasic cyan filtration curve (mild rise to peak then fall above start, matching live drop rate below) and the steadily rising white filtration-fraction curve.
  s13_return:      Nozzle relaxes back to R_E = 1.0 and graph morphs back to baseline push-and-pull strip; cyan gap pulses on push-beats-pull, both rings and red arrow pulse on combined resistance, and a glow slides from green to yellow ring as orange push pulses.
"""

from bp_parts import *

# ------------------------------------------------------------------ Palette
COL_PLASMA = "#FC6255"     # RED
COL_PROTEIN = "#C08CFF"    # PURPLE (high contrast on BG)
COL_WATER = "#49D8F2"      # CYAN
COL_AFFERENT = "#6BD072"   # GREEN
COL_EFFERENT = "#F5D547"   # YELLOW
COL_PUSH = "#FF9442"       # ORANGE
COL_BOWMAN = "#7DB8E8"     # pale BLUE
COL_WALL = "#D98A82"       # capillary wall outline
COL_LUMEN = "#1B151D"      # dark capillary interior
COL_AXIS = "#A8B2C4"       # crisp axis line

# ------------------------------------------------------------------ Shared geometry
CAP_Y = -0.62              # vertical centre of straight capillary
CAP_H = 1.00               # capillary outer height -> y in [-1.12, -0.12]
CAP_TOP = CAP_Y + CAP_H / 2
CAP_BOT = CAP_Y - CAP_H / 2
BOW_BOT = -2.55            # bottom of Bowman's space band -> y in [-2.55, -1.12]
PLOT_Y0 = 0.45             # push-pull strip bottom
PLOT_Y1 = 2.90             # push-pull strip top
PLOT_YR = (0.0, 90.0)      # mmHg (push=40, pull starts 25, arterial ceiling Pa-Pbs=85)

# ------------------------------------------------------------------ Physics model (from lesson_for_context.mdx)
P_A = 100.0
P_V = 10.0
P_BS = 15.0
PI_0 = 25.0


def resistor_model(r_a, r_e):
    """Two-resistor series circuit from the lesson: Flow and P_GC."""
    tot = max(r_a + r_e, 1e-6)
    flow = (P_A - P_V) / tot
    p_gc = P_V + (P_A - P_V) * (r_e / tot)
    push = p_gc - P_BS
    return flow, p_gc, push


def solve_capillary(r_a=1.0, r_e=1.0, kf=3.3, quad=0.25, n=80, net_cutoff=0.85):
    """Coupled Starling filtration ODE along normalized capillary length u in [0, 1].
    Returns dict with arrays u, pi, net, qp_frac (Q_p(u)/Q_0), plus scalars flow, p_gc, push, gfr, ff, u_eq.
    """
    flow, p_gc, push = resistor_model(r_a, r_e)
    du = 1.0 / n
    us = np.linspace(0.0, 1.0, n + 1)
    pis = np.empty(n + 1)
    nets = np.empty(n + 1)
    qfrac = np.empty(n + 1)
    F = 0.0
    u_eq = None
    for i in range(n + 1):
        frac = max(1.0 - F / max(flow, 1e-6), 0.08)
        r = 1.0 / frac
        pi = PI_0 * ((1.0 - quad) * r + quad * r * r)
        if pi >= push - net_cutoff:
            pi = min(pi, push)
            if u_eq is None and i > 0:
                u_eq = us[i]
        net = max(0.0, push - pi)
        if u_eq is not None:
            pi = push
            net = 0.0
        pis[i] = pi
        nets[i] = net
        qfrac[i] = frac
        if i < n:
            dF = kf * net * du
            F = min(F + dF, flow * 0.90)
    return dict(
        u=us, pi=pis, net=nets, qfrac=qfrac,
        flow=flow, p_gc=p_gc, push=push,
        gfr=F, ff=F / max(flow, 1e-6), u_eq=u_eq,
    )


def precompute_biphasic(r_min=1.0, r_max=3.2, kf=1.2, quad=0.0, m=90):
    """Compute exact GFR(R_E) and FF(R_E) across an efferent squeeze sweep."""
    rs = np.linspace(r_min, r_max, m)
    gfrs = np.empty(m)
    ffs = np.empty(m)
    for idx, r_e in enumerate(rs):
        s = solve_capillary(1.0, r_e, kf=kf, quad=quad, n=120)
        gfrs[idx] = s["gfr"]
        ffs[idx] = s["ff"]
    return rs, gfrs, ffs


# ------------------------------------------------------------------ Form A: Tuft World (s00, s01, start of s02)
def _tuft_paths():
    """Return parametric polylines for afferent -> rounded tuft coils -> efferent."""
    ts = np.linspace(0, 1, 90)
    loops = []
    # 3 distinct rounded looping paths forming a true glomerular tuft ball inside the cup
    # Loop 0 (upper arching dome loop)
    p0 = np.column_stack([
        -1.65 + 3.30 * ts - 0.16 * np.sin(2 * PI * ts),
        1.12 + 0.68 * np.sin(PI * ts) + 0.14 * np.sin(3 * PI * ts),
        np.zeros_like(ts),
    ])
    # Loop 1 (central winding coil)
    p1 = np.column_stack([
        -1.65 + 3.30 * ts + 0.30 * np.sin(2 * PI * ts),
        1.05 - 1.12 * np.sin(PI * ts) + 0.42 * np.sin(3 * PI * ts),
        np.zeros_like(ts),
    ])
    # Loop 2 (lower rounded U-loop)
    p2 = np.column_stack([
        -1.65 + 3.30 * ts - 0.25 * np.sin(2 * PI * ts),
        1.02 - 2.15 * np.sin(PI * ts) - 0.14 * np.sin(3 * PI * ts),
        np.zeros_like(ts),
    ])
    aff_x = np.linspace(-6.05, -1.65, 35)
    aff_y = 1.38 - 0.28 * ((aff_x + 6.05) / 4.40) ** 2
    aff = np.column_stack([aff_x, aff_y, np.zeros_like(aff_x)])

    eff_x = np.linspace(1.65, 6.05, 35)
    eff_y = 1.10 + 0.28 * (1.0 - (1.0 - (eff_x - 1.65) / 4.40) ** 2)
    eff = np.column_stack([eff_x, eff_y, np.zeros_like(eff_x)])

    for lp in (p0, p1, p2):
        lp[0] = [-1.65, 1.10, 0.0]
        lp[-1] = [1.65, 1.10, 0.0]
        full = np.vstack([aff[:-1], lp, eff[1:]])
        loops.append(full)
    return aff, eff, [p0, p1, p2], loops


def _sample_polyline(pts, s):
    """Interpolate point at fraction s in [0, 1] along polyline pts (N, 3)."""
    s = float(np.clip(s, 0.0, 1.0))
    idx_f = s * (len(pts) - 1)
    i = min(int(idx_f), len(pts) - 2)
    f = idx_f - i
    return pts[i] * (1.0 - f) + pts[i + 1] * f


def build_tuft_world(pinch_tr=None, flow_tr=None, drip_tr=None, seed=7):
    """Build the glomerular tuft in Bowman's capsule with live particle & drop updaters.
    Returns (root_group, refs_dict).
    """
    rng = np.random.default_rng(seed)
    pinch_tr = pinch_tr or ValueTracker(0.0)
    flow_tr = flow_tr or ValueTracker(1.0)
    drip_tr = drip_tr or ValueTracker(1.0)

    # 1. Bowman's capsule cup + cleanly open bottom outlet (pale BLUE)
    left_wall_pts = [
        [-2.05, 1.85, 0],
        [-2.58, 0.90, 0],
        [-2.55, -0.55, 0],
        [-1.85, -1.85, 0],
        [-0.50, -2.35, 0],
        [-0.50, -3.32, 0],
    ]
    right_wall_pts = [[-p[0], p[1], 0] for p in left_wall_pts]
    fill_pts = (
        left_wall_pts
        + [[0.50, -3.32, 0]]
        + list(reversed(right_wall_pts[:-1]))
        + [[0.0, 2.02, 0]]
    )
    cup_fill = VMobject(fill_color=COL_BOWMAN, fill_opacity=0.18, stroke_width=0)
    cup_fill.set_points_smoothly(fill_pts)
    wall_l = VMobject(stroke_color=COL_BOWMAN, stroke_width=5.5, fill_opacity=0).set_points_smoothly(left_wall_pts)
    wall_r = VMobject(stroke_color=COL_BOWMAN, stroke_width=5.5, fill_opacity=0).set_points_smoothly(right_wall_pts)
    cup_grp = VGroup(cup_fill, wall_l, wall_r)

    # 2. Afferent (GREEN) and Efferent (YELLOW) arterioles + rings
    aff_pts, eff_pts, tuft_loops, full_loops = _tuft_paths()

    def make_vessel_tube(pts, color, half_w=0.25, pinch_fn=None):
        top_p, bot_p = [], []
        n = len(pts)
        for i, p in enumerate(pts):
            u = i / max(n - 1, 1)
            hw = half_w * (1.0 - (pinch_fn(u) if pinch_fn else 0.0))
            top_p.append(p + UP * hw)
            bot_p.append(p + DOWN * hw)
        poly = Polygon(*(top_p + list(reversed(bot_p))),
                       fill_color=COL_LUMEN, fill_opacity=0.92, stroke_width=0)
        w_top = VMobject(stroke_color=color, stroke_width=5.5).set_points_as_corners(top_p)
        w_bot = VMobject(stroke_color=color, stroke_width=5.5).set_points_as_corners(bot_p)
        return VGroup(poly, w_top, w_bot)

    aff_tube = make_vessel_tube(aff_pts, COL_AFFERENT, half_w=0.26)
    aff_ring = RoundedRectangle(corner_radius=0.10, width=0.42, height=0.80,
                                stroke_color=COL_AFFERENT, stroke_width=5.5,
                                fill_color=COL_AFFERENT, fill_opacity=0.25).move_to([-3.85, 1.31, 0])

    # Efferent tube narrows dynamically at u=0.5 when pinch_tr increases
    def _mk_eff():
        p_val = float(pinch_tr.get_value())
        pinch_fn = lambda u: 0.42 * p_val * np.exp(-((u - 0.50) / 0.14) ** 2)
        return make_vessel_tube(eff_pts, COL_EFFERENT, half_w=0.26, pinch_fn=pinch_fn)

    eff_tube = always_redraw(_mk_eff)

    def _mk_eff_ring():
        p_val = float(pinch_tr.get_value())
        h = 0.80 * (1.0 - 0.30 * p_val)
        return RoundedRectangle(corner_radius=0.10, width=0.42, height=h,
                                stroke_color=COL_EFFERENT, stroke_width=5.5,
                                fill_color=COL_EFFERENT, fill_opacity=0.25).move_to([3.85, 1.31, 0])

    eff_ring = always_redraw(_mk_eff_ring)

    # 3. Tuft capillary loops (thick lumen + wall)
    tuft_grp = VGroup()
    for lp in tuft_loops:
        bg_c = VMobject(stroke_color=COL_LUMEN, stroke_width=24).set_points_as_corners(lp)
        out_c = VMobject(stroke_color=COL_WALL, stroke_width=29).set_points_as_corners(lp)
        in_c = VMobject(stroke_color="#2A161C", stroke_width=21).set_points_as_corners(lp)
        tuft_grp.add(out_c, bg_c, in_c)

    # 4. Streaming RED plasma dots + PURPLE protein dots along the 3 full loops
    dots_grp = VGroup()
    dot_specs = []
    for k in range(36):
        is_prot = (k % 3 == 0)
        loop_idx = k % 3
        phase = (k / 36.0) + rng.uniform(-0.01, 0.01)
        jitter_y = rng.uniform(-0.06, 0.06)
        col = COL_PROTEIN if is_prot else COL_PLASMA
        rad = 0.075 if is_prot else 0.068
        d = Dot(radius=rad, color=col)
        d._phase = phase % 1.0
        d._loop = loop_idx
        d._jy = jitter_y
        pos = _sample_polyline(full_loops[loop_idx], d._phase)
        d.move_to(pos + UP * jitter_y)
        dots_grp.add(d)
        dot_specs.append(d)

    def _update_dots(mob, dt):
        spd = 0.22 * float(flow_tr.get_value())
        for d in dot_specs:
            d._phase = (d._phase + spd * dt) % 1.0
            pos = _sample_polyline(full_loops[d._loop], d._phase)
            d.move_to(pos + UP * d._jy)

    dots_grp.add_updater(_update_dots)

    # 5. Cyan filtrate drops dripping from the tuft into Bowman's cup & out the outlet
    drops_grp = VGroup()
    drop_specs = []
    drop_xs = [-1.45, -0.90, -0.35, 0.20, 0.75, 1.30]
    for idx in range(18):
        col_i = idx % len(drop_xs)
        x0 = drop_xs[col_i] + rng.uniform(-0.12, 0.12)
        y_start = -0.35 - 0.55 * np.cos(x0 * 0.9) + rng.uniform(-0.15, 0.10)
        phase = (idx / 18.0 + rng.uniform(0, 0.04)) % 1.0
        dr = Dot(radius=0.072, color=COL_WATER)
        dr._phase = phase
        dr._x0 = x0
        dr._ystart = y_start
        drops_grp.add(dr)
        drop_specs.append(dr)

    def _place_drop(dr):
        p = dr._phase
        if p < 0.62:
            f = p / 0.62
            x = dr._x0 * (1.0 - 0.55 * f * f)
            y = dr._ystart + f * (-2.15 - dr._ystart)
        else:
            f = (p - 0.62) / 0.38
            x = dr._x0 * 0.45 * (1.0 - 0.65 * f)
            y = -2.15 + f * (-3.25 - (-2.15))
        dr.move_to([x, y, 0.0])
        op = min(1.0, p / 0.12) * min(1.0, (1.0 - p) / 0.12)
        dr.set_opacity(float(op))

    for dr in drop_specs:
        _place_drop(dr)

    def _update_drops(mob, dt):
        spd = 0.42 * float(drip_tr.get_value())
        for dr in drop_specs:
            dr._phase = (dr._phase + spd * dt) % 1.0
            _place_drop(dr)

    drops_grp.add_updater(_update_drops)

    # 6. White pincers (hidden until added/shown in s00_hook)
    def make_pincers():
        def _mk():
            pv = float(pinch_tr.get_value())
            gap = 0.68 - 0.36 * pv
            cx, cy = 3.85, 1.31
            top_jaw = VMobject(stroke_color=TEXT, stroke_width=6)
            top_jaw.set_points_as_corners([
                [cx - 0.32, cy + gap + 0.45, 0],
                [cx - 0.16, cy + gap + 0.08, 0],
                [cx + 0.16, cy + gap + 0.08, 0],
                [cx + 0.32, cy + gap + 0.45, 0],
            ])
            top_arm = Line([cx, cy + gap + 0.45, 0], [cx, cy + gap + 0.88, 0], color=TEXT, stroke_width=5)
            bot_jaw = VMobject(stroke_color=TEXT, stroke_width=6)
            bot_jaw.set_points_as_corners([
                [cx - 0.32, cy - gap - 0.45, 0],
                [cx - 0.16, cy - gap - 0.08, 0],
                [cx + 0.16, cy - gap - 0.08, 0],
                [cx + 0.32, cy - gap - 0.45, 0],
            ])
            bot_arm = Line([cx, cy - gap - 0.45, 0], [cx, cy - gap - 0.88, 0], color=TEXT, stroke_width=5)
            return VGroup(top_jaw, top_arm, bot_jaw, bot_arm)
        return always_redraw(_mk)

    root = VGroup(cup_grp, aff_tube, eff_tube, tuft_grp, drops_grp, dots_grp, aff_ring, eff_ring)
    refs = dict(
        cup=cup_grp, tuft=tuft_grp, aff_tube=aff_tube, eff_tube=eff_tube,
        aff_ring=aff_ring, eff_ring=eff_ring, dots=dots_grp, drops=drops_grp,
        make_pincers=make_pincers, pinch_tr=pinch_tr, flow_tr=flow_tr, drip_tr=drip_tr,
    )
    return root, refs


# ------------------------------------------------------------------ Form B: Straight Capillary Hose World (s02-s13)
class HoseWorld:
    """Straight horizontal capillary + green afferent + yellow efferent + Bowman's space band,
    driven live by trackers (cap_half_w, r_a, r_e, kf, conc_vis, drop_mod, ode_blend, has_tap, has_nozzle, ...).
    """

    def __init__(
        self,
        cap_hw=4.2,
        r_a=1.0,
        r_e=1.0,
        kf=1.2,
        quad=0.25,
        conc_vis=0.0,       # 0 = uniform protein tint, 1 = full ODE protein crowding & purple tint
        drop_mod=0.0,       # 0 = uniform drops along capillary, 1 = modulated by ODE net(u)
        ode_freeze=None,    # optional frozen ODE dict (for s09_predict / s10_pause no-spoiler drops)
        drop_rate_tr=None,  # optional direct global drop multiplier (for s12_biphasic)
        show_tap=False,
        show_nozzle=False,
        show_arrow=False,
        bright_red=False,
        keep_lower_lane_clear=False,  # keeps y < -0.70 clear of dots when 'flow' label is inside tube
        seed=7,
    ):
        self.rng = np.random.default_rng(seed)
        self.hw_tr = ValueTracker(cap_hw)
        self.ra_tr = ValueTracker(r_a)
        self.re_tr = ValueTracker(r_e)
        self.kf_tr = ValueTracker(kf)
        self.quad = quad
        self.conc_tr = ValueTracker(conc_vis)
        self.mod_tr = ValueTracker(drop_mod)
        self.ode_blend_tr = ValueTracker(0.0 if ode_freeze is not None else 1.0)
        self.ode_freeze = ode_freeze
        self.drop_rate_tr = drop_rate_tr
        self.show_tap = show_tap
        self.show_nozzle = show_nozzle
        self.show_arrow = show_arrow
        self.bright_red = ValueTracker(1.0 if bright_red else 0.0)
        self.keep_lower = ValueTracker(1.0 if keep_lower_lane_clear else 0.0)
        self.aff_glow = ValueTracker(0.0)
        self.eff_glow = ValueTracker(0.0)
        self.wall_pulse = ValueTracker(0.0)
        self.arrow_pulse = ValueTracker(0.0)

        self.outer_x = 6.10  # outer ends of afferent and efferent tubes

        # Cache latest ODE solve per frame
        self._cache_key = None
        self._cache_sol = None

        self._build()

    def sol(self):
        ra = round(float(self.ra_tr.get_value()), 4)
        re = round(float(self.re_tr.get_value()), 4)
        kf = round(float(self.kf_tr.get_value()), 4)
        key = (ra, re, kf)
        if key != self._cache_key:
            self._cache_sol = solve_capillary(ra, re, kf=kf, quad=self.quad, n=80)
            self._cache_key = key
        return self._cache_sol

    def effective_sol(self):
        """Returns blended ODE solution (used when unlocking ODE in s11_answer)."""
        live = self.sol()
        if self.ode_freeze is None:
            return live
        b = float(np.clip(self.ode_blend_tr.get_value(), 0.0, 1.0))
        if b <= 1e-4:
            return self.ode_freeze
        if b >= 1.0 - 1e-4:
            return live
        fr = self.ode_freeze
        u_eq = None
        if fr["u_eq"] is not None and live["u_eq"] is not None:
            u_eq = fr["u_eq"] * (1.0 - b) + live["u_eq"] * b
        elif live["u_eq"] is not None:
            u_eq = 1.0 * (1.0 - b) + live["u_eq"] * b
        return dict(
            u=live["u"],
            pi=fr["pi"] * (1.0 - b) + live["pi"] * b,
            net=fr["net"] * (1.0 - b) + live["net"] * b,
            qfrac=fr["qfrac"] * (1.0 - b) + live["qfrac"] * b,
            flow=live["flow"],
            p_gc=live["p_gc"],
            push=live["push"],
            gfr=fr["gfr"] * (1.0 - b) + live["gfr"] * b,
            ff=fr["ff"] * (1.0 - b) + live["ff"] * b,
            u_eq=u_eq,
        )

    def cap_x0(self):
        return -float(self.hw_tr.get_value())

    def cap_x1(self):
        return float(self.hw_tr.get_value())

    def aff_ring_x(self):
        return 0.5 * (-self.outer_x + self.cap_x0())

    def eff_ring_x(self):
        return 0.5 * (self.cap_x1() + self.outer_x)

    def _build(self):
        # 1. Bowman's space pale BLUE band directly beneath capillary
        def _mk_bowman():
            x0, x1 = self.cap_x0(), self.cap_x1()
            w = x1 - x0
            h = CAP_BOT - BOW_BOT
            rect = Rectangle(
                width=w, height=h,
                fill_color=COL_BOWMAN, fill_opacity=0.16,
                stroke_color=COL_BOWMAN, stroke_width=3.5,
            ).move_to([0.0, 0.5 * (CAP_BOT + BOW_BOT), 0.0])
            return rect

        self.bowman_band = always_redraw(_mk_bowman)

        # 2. Capillary lumen + smooth seamless purple concentration gradient + walls
        def _mk_capillary():
            x0, x1 = self.cap_x0(), self.cap_x1()
            w = x1 - x0
            lumen = Rectangle(
                width=w, height=CAP_H,
                fill_color=COL_LUMEN, fill_opacity=0.96, stroke_width=0,
            ).move_to([0.0, CAP_Y, 0.0])
            g = VGroup(lumen)
            cv = float(self.conc_tr.get_value())
            if cv > 0.01:
                sol = self.effective_sol()
                q_end = float(sol["qfrac"][-1])
                conc_excess = max(0.0, (1.0 / max(q_end, 0.18)) - 1.0)
                end_mix = min(0.52, cv * 0.56 * conc_excess)
                if end_mix > 0.01:
                    col_left = ManimColor(COL_LUMEN)
                    col_right = interpolate_color(ManimColor(COL_LUMEN), ManimColor(COL_PROTEIN), end_mix)
                    # Single seamless linear-gradient rectangle (zero vertical seams!)
                    grad = Rectangle(
                        width=w, height=CAP_H - 0.04, stroke_width=0,
                    ).move_to([0.0, CAP_Y, 0.0])
                    grad.set_fill(color=[col_left, col_right], opacity=0.96)
                    grad.set_sheen_direction(RIGHT)
                    g.add(grad)
            wp = float(self.wall_pulse.get_value())
            sw = 4.5 + 4.5 * wp
            col_w = interpolate_color(ManimColor(COL_WALL), ManimColor(TEXT), 0.55 * wp)
            top_w = Line([x0, CAP_TOP, 0], [x1, CAP_TOP, 0], color=col_w, stroke_width=sw)
            bot_w = DashedLine([x0, CAP_BOT, 0], [x1, CAP_BOT, 0], color=col_w, stroke_width=sw,
                               dash_length=0.22, dashed_ratio=0.72)
            g.add(top_w, bot_w)
            return g

        self.capillary = always_redraw(_mk_capillary)

        # 3. Afferent (GREEN) and Efferent (YELLOW) arteriole tubes with dynamic constriction
        def _mk_arteriole(side):
            is_aff = (side == "aff")
            col = COL_AFFERENT if is_aff else COL_EFFERENT
            x_a = -self.outer_x if is_aff else self.cap_x1()
            x_b = self.cap_x0() if is_aff else self.outer_x
            r_val = float(self.ra_tr.get_value() if is_aff else self.re_tr.get_value())
            glow = float(self.aff_glow.get_value() if is_aff else self.eff_glow.get_value())
            # Constriction visual fraction: 0 at r=1, saturates smoothly toward 0.55 at high r
            sq = np.clip(0.55 * (1.0 - 1.0 / max(r_val, 0.5)), -0.15, 0.58)
            xs = np.linspace(x_a, x_b, 25)
            top_p, bot_p = [], []
            for i, x in enumerate(xs):
                u = i / 24.0
                hw = 0.34 * (1.0 - sq * np.exp(-((u - 0.5) / 0.22) ** 2))
                top_p.append([x, CAP_Y + hw, 0.0])
                bot_p.append([x, CAP_Y - hw, 0.0])
            poly = Polygon(*(top_p + list(reversed(bot_p))),
                           fill_color=COL_LUMEN, fill_opacity=0.95, stroke_width=0)
            c_use = interpolate_color(ManimColor(col), ManimColor(TEXT), 0.35 * glow)
            sw = 5.0 + 3.5 * glow
            wt = VMobject(stroke_color=c_use, stroke_width=sw).set_points_as_corners(top_p)
            wb = VMobject(stroke_color=c_use, stroke_width=sw).set_points_as_corners(bot_p)
            return VGroup(poly, wt, wb)

        self.aff_tube = always_redraw(lambda: _mk_arteriole("aff"))
        self.eff_tube = always_redraw(lambda: _mk_arteriole("eff"))

        # 4. Rings + optional tap handle (green) and nozzle (yellow)
        def _mk_aff_ring():
            rx = self.aff_ring_x()
            r_val = float(self.ra_tr.get_value())
            glow = float(self.aff_glow.get_value())
            sq = np.clip(0.45 * (1.0 - 1.0 / max(r_val, 0.5)), -0.1, 0.50)
            h = 0.90 * (1.0 - 0.45 * sq)
            c_use = interpolate_color(ManimColor(COL_AFFERENT), ManimColor(TEXT), 0.45 * glow)
            ring = RoundedRectangle(
                corner_radius=0.09, width=0.40, height=h,
                stroke_color=c_use, stroke_width=5.0 + 4.0 * glow,
                fill_color=COL_AFFERENT, fill_opacity=0.25 + 0.30 * glow,
            ).move_to([rx, CAP_Y, 0.0])
            g = VGroup(ring)
            if self.show_tap:
                # Tap stem + T-bar handle sitting cleanly above the ring; turns slightly when tightened
                top_y = CAP_Y + h / 2
                stem = Line([rx, top_y, 0], [rx, top_y + 0.32, 0], color=c_use, stroke_width=6)
                bar_w = 0.62 * (1.0 - 0.35 * sq)
                bar = Line([rx - bar_w / 2, top_y + 0.32, 0], [rx + bar_w / 2, top_y + 0.32, 0],
                           color=c_use, stroke_width=8)
                g.add(stem, bar)
            return g

        def _mk_eff_ring():
            rx = self.eff_ring_x()
            r_val = float(self.re_tr.get_value())
            glow = float(self.eff_glow.get_value())
            sq = np.clip(0.55 * (1.0 - 1.0 / max(r_val, 0.5)), -0.1, 0.58)
            h = 0.90 * (1.0 - 0.48 * sq)
            c_use = interpolate_color(ManimColor(COL_EFFERENT), ManimColor(TEXT), 0.45 * glow)
            if not self.show_nozzle:
                ring = RoundedRectangle(
                    corner_radius=0.09, width=0.40, height=h,
                    stroke_color=c_use, stroke_width=5.0 + 4.0 * glow,
                    fill_color=COL_EFFERENT, fill_opacity=0.25 + 0.30 * glow,
                ).move_to([rx, CAP_Y, 0.0])
                return VGroup(ring)
            # Tapered nozzle sleeve + outer knurled clamp collar
            hw_l = h / 2 + 0.06
            hw_r = max(0.16, h / 2 - 0.10 - 0.14 * sq)
            nozzle = Polygon(
                [rx - 0.34, CAP_Y + hw_l, 0],
                [rx + 0.34, CAP_Y + hw_r, 0],
                [rx + 0.34, CAP_Y - hw_r, 0],
                [rx - 0.34, CAP_Y - hw_l, 0],
                stroke_color=c_use, stroke_width=5.0 + 4.0 * glow,
                fill_color=COL_EFFERENT, fill_opacity=0.28 + 0.30 * glow,
            )
            # Two small pinch-jaw chevrons above & below nozzle showing squeeze intensity
            jaw_t = Line([rx - 0.18, CAP_Y + hw_l + 0.14, 0], [rx + 0.18, CAP_Y + hw_r + 0.12, 0],
                         color=c_use, stroke_width=5)
            jaw_b = Line([rx - 0.18, CAP_Y - hw_l - 0.14, 0], [rx + 0.18, CAP_Y - hw_r - 0.12, 0],
                         color=c_use, stroke_width=5)
            return VGroup(nozzle, jaw_t, jaw_b)

        self.aff_ring = always_redraw(_mk_aff_ring)
        self.eff_ring = always_redraw(_mk_eff_ring)

        # 5. Broad RED flow arrow inside capillary (thickness proportional to Flow)
        def _mk_flow_arrow():
            if not self.show_arrow:
                return VGroup()
            sol = self.sol()
            flow_frac = np.clip(sol["flow"] / 45.0, 0.14, 1.35)
            ap = float(self.arrow_pulse.get_value())
            hw = float(self.hw_tr.get_value())
            x_l = -0.52 * hw
            x_r = 0.22 * hw
            y_a = CAP_Y + 0.22  # upper-mid lumen, leaving clean lane at y = -0.84 for 'flow' label
            sw = (10.0 * flow_frac + 4.0) * (1.0 + 0.35 * ap)
            tip_l = 0.24 + 0.14 * flow_frac
            col_a = interpolate_color(ManimColor(COL_PLASMA), ManimColor(TEXT), 0.30 * ap)
            arr = Arrow(
                [x_l, y_a, 0], [x_r, y_a, 0],
                buff=0, color=col_a, stroke_width=sw,
                max_tip_length_to_length_ratio=0.28,
                tip_length=tip_l,
            )
            arr.set_opacity(0.88)
            return arr

        self.flow_arrow = always_redraw(_mk_flow_arrow)

        # 6. Streaming RED plasma dots & PURPLE protein dots (in-place updater, fast & exact conservation!)
        self.dots_grp = VGroup()
        self._red_dots = []
        self._prot_dots = []
        # 26 red dots + 22 purple dots
        for i in range(26):
            d = Dot(radius=0.062, color=COL_PLASMA)
            d._s = (i / 26.0 + self.rng.uniform(-0.01, 0.01)) % 1.0
            d._lane = self.rng.uniform(0.0, 1.0)
            self._red_dots.append(d)
            self.dots_grp.add(d)
        for i in range(22):
            d = Dot(radius=0.072, color=COL_PROTEIN)
            d._s = (i / 22.0 + self.rng.uniform(-0.01, 0.01)) % 1.0
            d._lane = self.rng.uniform(0.0, 1.0)
            self._prot_dots.append(d)
            self.dots_grp.add(d)

        self._place_all_dots(0.0)
        self.dots_grp.add_updater(lambda m, dt: self._place_all_dots(dt))

        # 7. Cyan filtrate drops falling into Bowman's space (in-place updater, driven by local net(u))
        self.drops_grp = VGroup()
        self._drops = []
        n_cols = 12
        n_per_col = 3
        for ci in range(n_cols):
            u_col = (ci + 0.45) / n_cols
            for j in range(n_per_col):
                dr = Dot(radius=0.068, color=COL_WATER)
                dr._u = u_col
                dr._phase = (j / n_per_col + ci * 0.27 + self.rng.uniform(0, 0.05)) % 1.0
                self._drops.append(dr)
                self.drops_grp.add(dr)

        self._place_all_drops(0.0)
        self.drops_grp.add_updater(lambda m, dt: self._place_all_drops(dt))

        self.group = VGroup(
            self.bowman_band,
            self.aff_tube,
            self.eff_tube,
            self.capillary,
            self.drops_grp,
            self.dots_grp,
            self.flow_arrow,
            self.aff_ring,
            self.eff_ring,
        )

    def _dot_y(self, lane, in_cap):
        if not in_cap:
            return CAP_Y + (lane - 0.5) * 0.42
        kl = float(self.keep_lower.get_value())
        # When 'flow' label sits at y=-0.84 inside capillary, dots occupy y in [-0.57, -0.22]
        y_lo = -0.98 * (1.0 - kl) + (-0.57) * kl
        y_hi = -0.22
        return y_lo + lane * (y_hi - y_lo)

    def _place_all_dots(self, dt):
        sol = self.effective_sol()
        flow_scale = float(self.sol()["flow"]) / 45.0
        cv = float(self.conc_tr.get_value())
        br = float(self.bright_red.get_value())
        x0, x1 = self.cap_x0(), self.cap_x1()
        ox = self.outer_x
        total_w = 2.0 * ox

        for is_prot, lst in ((False, self._red_dots), (True, self._prot_dots)):
            base_spd = 0.23 * flow_scale
            for d in lst:
                x = -ox + d._s * total_w
                in_cap = (x0 <= x <= x1)
                if in_cap:
                    u = (x - x0) / max(x1 - x0, 1e-6)
                    q_f = float(np.interp(u, sol["u"], sol["qfrac"]))
                    # By conservation c(u)*v(u) = const, slowing purple speed by q_f^2.2 makes crowding unmistakably clear
                    slow_f = (1.0 - cv) + cv * (q_f ** 2.2)
                    local_spd = base_spd * (slow_f if is_prot else (0.55 + 0.45 * slow_f))
                elif x > x1:
                    q_end = float(sol["qfrac"][-1])
                    slow_f = (1.0 - cv) + cv * (q_end ** 2.2)
                    local_spd = base_spd * (slow_f if is_prot else (0.55 + 0.45 * slow_f))
                else:
                    local_spd = base_spd
                d._s = (d._s + local_spd * dt) % 1.0
                x = -ox + d._s * total_w
                in_cap = (x0 <= x <= x1)
                y = self._dot_y(d._lane, in_cap)
                d.move_to([x, y, 0.0])
                if not is_prot:
                    d.set_opacity(0.78 + 0.22 * br)

    def _place_all_drops(self, dt):
        sol = self.effective_sol()
        mod = float(self.mod_tr.get_value())
        x0, x1 = self.cap_x0(), self.cap_x1()
        global_mult = float(self.drop_rate_tr.get_value()) if self.drop_rate_tr is not None else 1.0
        for dr in self._drops:
            net_u = float(np.interp(dr._u, sol["u"], sol["net"]))
            rel = np.clip(net_u / 15.0, 0.0, 2.2)
            if mod > 0.5 and net_u <= 0.10:
                eff_strength = 0.0
            else:
                # Keep drops clearly visible all the way up to equilibrium, tapering smoothly
                vis_rel = (0.36 + 0.64 * np.sqrt(rel)) if net_u > 0.10 else 0.0
                strength = (1.0 - mod) * 1.0 + mod * vis_rel
                eff_strength = strength * global_mult
            if eff_strength < 0.04:
                dr.set_opacity(0.0)
                dr.move_to([x0 + dr._u * (x1 - x0), CAP_BOT - 0.15, 0.0])
                continue
            spd = 0.55 * (0.45 + 0.55 * np.clip(eff_strength, 0.2, 2.0))
            dr._phase = (dr._phase + spd * dt) % 1.0
            x = x0 + dr._u * (x1 - x0)
            y = (CAP_BOT - 0.08) - dr._phase * (CAP_BOT - BOW_BOT - 0.24)
            dr.move_to([x, y, 0.0])
            fade = min(1.0, dr._phase / 0.14) * min(1.0, (1.0 - dr._phase) / 0.16)
            op = float(fade * np.clip(eff_strength * 1.10, 0.0, 1.0))
            dr.set_opacity(op)
            sc = float(np.clip(0.58 + 0.52 * eff_strength, 0.50, 1.25))
            dr.scale_to_fit_width(2 * 0.068 * sc)


# ------------------------------------------------------------------ Push-and-Pull Plot Strip Builder
def make_strip_axes(hw=4.2, show_ticks=True, show_ylabel=True):
    """Build the pressure strip aligned with capillary [-hw, +hw]."""
    P = Plot(
        box=(-hw, hw, PLOT_Y0, PLOT_Y1),
        xr=(0.0, 1.0),
        yr=PLOT_YR,
        xticks=(),
        yticks=[0, 40] if show_ticks else (),
        xlabel="",
        ylabel="mmHg" if show_ylabel else "",
        color=TEXT,
        size=24,
        label_size=24,
        stroke=3,
    )
    P.axes.set_stroke(COL_AXIS, width=3)
    P.ticks.set_stroke(COL_AXIS, width=2.5)
    return P


def strip_pt(hw, u, y_mmhg):
    x = -hw + u * (2.0 * hw)
    y = PLOT_Y0 + (y_mmhg - PLOT_YR[0]) / (PLOT_YR[1] - PLOT_YR[0]) * (PLOT_Y1 - PLOT_Y0)
    return np.array([x, y, 0.0])


def draw_pi(us, pis, push, k=2.6):
    """Schematic pull curve for drawing only: steepest at the afferent end, flattening to its end value."""
    us = np.asarray(us, float); pis = np.asarray(pis, float)
    hit = np.where(pis >= push - 1e-6)[0]
    j = int(hit[0]) if len(hit) else len(us) - 1
    u_end = max(us[j], 1e-6)
    p0, pe = float(pis[0]), float(min(pis[j], push))
    t = np.clip(us / u_end, 0.0, 1.0)
    out = p0 + (pe - p0) * (1.0 - (1.0 - t) ** k)
    out = np.where(us > u_end, push, out)
    return out


def make_live_strip_curves(hw_tr, sol_fn, push_draw_tr=None, pull_draw_tr=None, fill_op_tr=None,
                           push_pulse_tr=None, gap_pulse_tr=None):
    """Build always_redraw push line, pull curve, and cyan gap polygon driven by hw_tr and sol_fn()."""
    def _mk_gap():
        op_mult = float(fill_op_tr.get_value()) if fill_op_tr is not None else 1.0
        if op_mult <= 0.01:
            return VMobject(fill_opacity=0, stroke_opacity=0)
        hw = float(hw_tr.get_value())
        sol = sol_fn()
        us, pis, push = sol["u"], sol["pi"], sol["push"]
        pis = draw_pi(us, pis, push)
        # Only shade where push > pi
        mask = (push - pis) > 0.15
        if not np.any(mask):
            return VMobject(fill_opacity=0, stroke_opacity=0)
        idx = np.where(mask)[0]
        i0, i1 = int(idx[0]), int(idx[-1])
        # Include exact intersection point if next point exists
        if i1 + 1 < len(us):
            i1 += 1
        top_pts = [strip_pt(hw, us[i], push) for i in range(i0, i1 + 1)]
        bot_pts = [strip_pt(hw, us[i], min(push, pis[i])) for i in range(i1, i0 - 1, -1)]
        gp = float(gap_pulse_tr.get_value()) if gap_pulse_tr is not None else 0.0
        poly = Polygon(
            *(top_pts + bot_pts),
            fill_color=COL_WATER,
            fill_opacity=(0.30 + 0.32 * gp) * op_mult,
            stroke_width=0,
        )
        return poly

    def _mk_push():
        frac = float(push_draw_tr.get_value()) if push_draw_tr is not None else 1.0
        if frac <= 0.01:
            return VMobject(stroke_opacity=0)
        hw = float(hw_tr.get_value())
        sol = sol_fn()
        push = sol["push"]
        pp = float(push_pulse_tr.get_value()) if push_pulse_tr is not None else 0.0
        col = interpolate_color(ManimColor(COL_PUSH), ManimColor(TEXT), 0.35 * pp)
        return Line(
            strip_pt(hw, 0.0, push),
            strip_pt(hw, frac, push),
            color=col,
            stroke_width=6.0 + 4.5 * pp,
        )

    def _mk_pull():
        frac = float(pull_draw_tr.get_value()) if pull_draw_tr is not None else 1.0
        if frac <= 0.01:
            return VMobject(stroke_opacity=0)
        hw = float(hw_tr.get_value())
        sol = sol_fn()
        us, pis, push = sol["u"], sol["pi"], sol["push"]
        pis = draw_pi(us, pis, push)
        k = max(2, int(round(frac * (len(us) - 1))) + 1)
        pts = [strip_pt(hw, us[i], min(push, pis[i])) for i in range(k)]
        m = VMobject(stroke_color=COL_PROTEIN, stroke_width=6.0, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m

    return always_redraw(_mk_gap), always_redraw(_mk_push), always_redraw(_mk_pull)


# ------------------------------------------------------------------ Clean geometric silhouettes for s05
def make_rat_silhouette(color=TEXT, height=0.58):
    """Simple, unmistakable geometric rat silhouette (body, head, ear, tail)."""
    body = Ellipse(width=0.95, height=0.48, fill_color=color, fill_opacity=0.92, stroke_width=0)
    head = Ellipse(width=0.48, height=0.30, fill_color=color, fill_opacity=0.92, stroke_width=0).move_to([0.52, -0.02, 0])
    ear = Circle(radius=0.11, fill_color=color, fill_opacity=0.92, stroke_width=0).move_to([0.36, 0.18, 0])
    tail = VMobject(stroke_color=color, stroke_width=4.5)
    tail.set_points_smoothly([[-0.45, -0.05, 0], [-0.78, 0.04, 0], [-1.02, -0.08, 0], [-1.18, 0.05, 0]])
    g = VGroup(tail, body, head, ear)
    g.set_height(height)
    return g


def make_human_silhouette(color=TEXT, height=0.68):
    """Simple, unmistakable human head-and-shoulders silhouette."""
    head = Circle(radius=0.18, fill_color=color, fill_opacity=0.92, stroke_width=0).move_to([0, 0.24, 0])
    shoulders = VMobject(fill_color=color, fill_opacity=0.92, stroke_width=0)
    shoulders.set_points_smoothly([
        [-0.34, -0.32, 0], [-0.30, -0.04, 0], [-0.14, 0.04, 0],
        [0.14, 0.04, 0], [0.30, -0.04, 0], [0.34, -0.32, 0],
    ])
    g = VGroup(shoulders, head)
    g.set_height(height)
    return g


def make_check_mark(color=TEXT, height=0.38):
    m = VMobject(stroke_color=color, stroke_width=6.0)
    m.set_points_as_corners([[-0.18, 0.0, 0], [-0.04, -0.16, 0], [0.24, 0.22, 0]])
    m.set_height(height)
    return m


# ------------------------------------------------------------------ Common bottom labels
def bowman_label(hw=4.2):
    return T("Bowman's space", 26, COL_BOWMAN).move_to([-hw + 1.45, -3.00, 0.0])


def right_tag(text="one capillary, schematic"):
    return scope_tag(text, size=24, color=TEXT)


# ================================================================== SCENES

class S00Hook(SpokenScene):
    def construct(self):
        pinch_tr = ValueTracker(0.0)
        flow_tr = ValueTracker(1.0)
        drip_tr = ValueTracker(1.0)
        world, refs = build_tuft_world(pinch_tr=pinch_tr, flow_tr=flow_tr, drip_tr=drip_tr)
        self.add(world)

        pincers = refs["make_pincers"]()
        up_arr = Arrow([1.05, -3.15, 0], [1.05, -2.35, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.25)
        dn_arr = Arrow([1.65, -2.35, 0], [1.65, -3.15, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.25)
        q_txt = T("Rise or fall?", 40, TEXT, weight=BOLD).move_to([0.0, 3.25, 0.0])

        # Highlight the two tiny vessels as narrator introduces them
        self.at("two tiny vessels")
        self.play(
            Indicate(refs["aff_ring"], color=TEXT, scale_factor=1.18),
            Indicate(refs["eff_ring"], color=TEXT, scale_factor=1.18),
            run_time=0.9,
        )

        # Squeeze the draining (yellow) vessel
        self.at("squeeze")
        self.play(FadeIn(pincers), run_time=0.35)
        self.play(pinch_tr.animate.set_value(1.0), flow_tr.animate.set_value(0.68), run_time=0.85)

        # Rise
        self.at("rise")
        self.play(drip_tr.animate.set_value(2.1), FadeIn(up_arr, shift=UP * 0.12), run_time=0.22)

        # Or fall
        self.at("or fall")
        self.play(
            drip_tr.animate.set_value(0.35),
            up_arr.animate.set_opacity(0.35),
            FadeIn(dn_arr, shift=DOWN * 0.12),
            run_time=0.45,
        )
        # Alternate arrows cleanly in turn
        self.play(up_arr.animate.set_opacity(1.0), dn_arr.animate.set_opacity(0.35), run_time=0.45)
        self.play(up_arr.animate.set_opacity(0.35), dn_arr.animate.set_opacity(1.0), run_time=0.45)

        # Question across top
        self.at("which")
        self.play(FadeIn(q_txt, shift=DOWN * 0.1), up_arr.animate.set_opacity(1.0), run_time=0.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        pinch_tr = ValueTracker(1.0)
        flow_tr = ValueTracker(0.68)
        drip_tr = ValueTracker(0.35)
        world, refs = build_tuft_world(pinch_tr=pinch_tr, flow_tr=flow_tr, drip_tr=drip_tr)
        pincers = refs["make_pincers"]()
        up_arr = Arrow([1.05, -3.15, 0], [1.05, -2.35, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.25)
        dn_arr = Arrow([1.65, -2.35, 0], [1.65, -3.15, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.25)
        q_txt = T("Rise or fall?", 40, TEXT, weight=BOLD).move_to([0.0, 3.25, 0.0])
        self.add(world, pincers, up_arr, dn_arr, q_txt)

        title = T("Two Taps on One Filter", 46, TEXT, font=TITLE_FONT).move_to([0.0, 3.12, 0.0])
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.14)

        # Fade out old question & arrows first (zero overlap), then fade in title while pincers open
        self.play(
            FadeOut(q_txt), FadeOut(up_arr), FadeOut(dn_arr),
            pinch_tr.animate.set_value(0.0),
            flow_tr.animate.set_value(1.0),
            drip_tr.animate.set_value(1.0),
            run_time=0.45,
        )
        self.play(FadeIn(title, shift=UP * 0.08), GrowFromCenter(rule), FadeOut(pincers), run_time=0.55)
        self.finish()


class S02Filter(SpokenScene):
    def construct(self):
        world, refs = build_tuft_world()
        self.add(world)

        lbl_glom = T("glomerulus", 28, TEXT).move_to([-2.75, 2.55, 0.0])
        lbl_cap = T("Bowman's capsule", 28, COL_BOWMAN).move_to([4.35, -1.65, 0.0])

        self.at("glomerulus")
        self.play(
            Indicate(refs["tuft"], color=COL_PLASMA, scale_factor=1.05),
            FadeIn(lbl_glom),
            run_time=0.65,
        )

        self.at("bowman's capsule")
        self.play(
            Indicate(refs["cup"], color=TEXT, scale_factor=1.03),
            FadeIn(lbl_cap),
            run_time=0.65,
        )

        # Unwind tuft into permanent straight horizontal capillary
        self.wait(0.25)
        hose = HoseWorld(cap_hw=4.2, r_a=1.0, r_e=1.0, kf=1.2, conc_vis=0.0, drop_mod=0.0)
        b_lbl = bowman_label(4.2)
        tag = right_tag("one capillary, schematic")

        # Freeze tuft updaters during morph so ReplacementTransform is crisp
        refs["dots"].clear_updaters()
        refs["drops"].clear_updaters()
        self.play(FadeOut(lbl_glom), FadeOut(lbl_cap), run_time=0.3)
        self.play(
            ReplacementTransform(world, hose.group),
            FadeIn(tag),
            run_time=1.05,
        )
        self.play(FadeIn(b_lbl), run_time=0.3)

        # Magnifier over lower capillary wall showing 3 plain layers
        self.at("three layers")
        spot = Circle(radius=0.22, color=TEXT, stroke_width=3.5).move_to([-1.65, CAP_BOT, 0.0])
        lens_c = np.array([-1.65, 1.55, 0.0])
        lens_r = 1.48
        stem = Line(spot.get_top(), lens_c + DOWN * lens_r, color=TEXT, stroke_width=3.0)
        lens_bg = Circle(radius=lens_r, fill_color=BG, fill_opacity=0.96, stroke_color=TEXT, stroke_width=4.5).move_to(lens_c)

        # Three plain stripes inside lens (no molecular structures!)
        y_l1, y_l2, y_l3 = lens_c[1] + 0.42, lens_c[1] + 0.02, lens_c[1] - 0.38
        # 1. Fenestrated endothelium: plain dashed horizontal segments (pores)
        endo = VGroup(*[
            RoundedRectangle(corner_radius=0.04, width=0.38, height=0.14,
                             fill_color=COL_WALL, fill_opacity=0.9, stroke_width=0)
            .move_to([lens_c[0] + dx, y_l1, 0])
            for dx in (-0.82, -0.28, 0.28, 0.82)
        ])
        # 2. Basement membrane: plain translucent solid stripe
        bmem = RoundedRectangle(corner_radius=0.05, width=2.45, height=0.18,
                                fill_color=COL_BOWMAN, fill_opacity=0.55,
                                stroke_color=COL_BOWMAN, stroke_width=2).move_to([lens_c[0], y_l2, 0])
        # 3. Podocyte slits: plain blocks with narrow slits
        podo = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=0.46, height=0.20,
                             fill_color=COL_AFFERENT, fill_opacity=0.72, stroke_width=0)
            .move_to([lens_c[0] + dx, y_l3, 0])
            for dx in (-0.84, -0.28, 0.28, 0.84)
        ])
        lens_rim = Circle(radius=lens_r, fill_opacity=0, stroke_color=TEXT, stroke_width=4.5).move_to(lens_c)

        # Three labels cleanly to the right of the lens, connected by short horizontal pointers
        x_lbl = 0.65
        t_endo = T("fenestrated endothelium", 26, TEXT).move_to([x_lbl, y_l1 + 0.32, 0], aligned_edge=LEFT)
        t_bmem = T("basement membrane", 26, TEXT).move_to([x_lbl, y_l2, 0], aligned_edge=LEFT)
        t_podo = T("podocyte slits", 26, TEXT).move_to([x_lbl, y_l3 - 0.32, 0], aligned_edge=LEFT)
        p_endo = Line([lens_c[0] + 1.25, y_l1, 0], [x_lbl - 0.14, y_l1 + 0.32, 0], color=COL_AXIS, stroke_width=2.5)
        p_bmem = Line([lens_c[0] + 1.48, y_l2, 0], [x_lbl - 0.14, y_l2, 0], color=COL_AXIS, stroke_width=2.5)
        p_podo = Line([lens_c[0] + 1.25, y_l3, 0], [x_lbl - 0.14, y_l3 - 0.32, 0], color=COL_AXIS, stroke_width=2.5)

        mag_static = VGroup(spot, stem, lens_bg, endo, bmem, podo, lens_rim, p_endo, p_bmem, p_podo, t_endo, t_bmem, t_podo)
        self.play(FadeIn(mag_static, scale=0.92), run_time=0.95)

        # Water and small solutes pass freely through all 3 stripes
        self.at("water")
        pass_mobs = VGroup()
        pass_anims = []
        for dx, is_water in ((-0.56, True), (0.0, False), (0.56, True), (-0.02, True), (0.54, False)):
            m = Dot(radius=0.075 if is_water else 0.045, color=COL_WATER if is_water else TEXT)
            m.move_to([lens_c[0] + dx, lens_c[1] + 0.98, 0])
            pass_mobs.add(m)
            pass_anims.append(m.animate.move_to([lens_c[0] + dx, lens_c[1] - 0.96, 0]))
        self.play(FadeIn(pass_mobs), run_time=0.2)
        self.play(LaggedStart(*pass_anims, lag_ratio=0.18), run_time=1.8, rate_func=linear)
        self.play(FadeOut(pass_mobs), run_time=0.25)

        # Plasma protein mostly stays behind (purple dots approach wall and turn back)
        self.at("protein")
        prot_mobs = VGroup()
        turn_anims = []
        for dx in (-0.45, 0.10, 0.55):
            pm = Dot(radius=0.105, color=COL_PROTEIN).move_to([lens_c[0] + dx, lens_c[1] + 0.98, 0])
            prot_mobs.add(pm)
            path = VMobject()
            path.set_points_smoothly([
                [lens_c[0] + dx, lens_c[1] + 0.98, 0],
                [lens_c[0] + dx, y_l1 + 0.24, 0],
                [lens_c[0] + dx + 0.22, lens_c[1] + 0.90, 0],
            ])
            turn_anims.append(MoveAlongPath(pm, path))
        self.play(FadeIn(prot_mobs), run_time=0.2)
        self.play(*turn_anims, run_time=1.25)

        # Close magnifier cleanly before end of scene
        self.play(FadeOut(prot_mobs), FadeOut(mag_static, scale=0.85), run_time=0.55)
        self.finish()


class S03Protein(SpokenScene):
    def construct(self):
        hose = HoseWorld(cap_hw=4.2, r_a=1.0, r_e=1.0, kf=3.3, conc_vis=0.15, drop_mod=0.0)
        b_lbl = bowman_label(4.2)
        tag = right_tag("one capillary, schematic")
        self.add(hose.group, b_lbl, tag)

        # As filtrate leaves protein behind, purple crowding & internal purple tint ramp up left-to-right
        self.at("leaves its protein")
        self.play(hose.conc_tr.animate.set_value(0.55), run_time=2.0)

        self.at("less water")
        self.play(hose.conc_tr.animate.set_value(1.0), run_time=2.2)

        self.at("more concentrated")
        lbl_conc = T("protein concentrates", 28, COL_PROTEIN).move_to([2.15, 0.35, 0.0])
        self.play(FadeIn(lbl_conc, shift=UP * 0.1), run_time=0.65)
        self.finish()


class S04PushPull(SpokenScene):
    def construct(self):
        hose = HoseWorld(cap_hw=4.2, r_a=1.0, r_e=1.0, kf=1.2, quad=0.25, conc_vis=1.0, drop_mod=0.0)
        b_lbl = bowman_label(4.2)
        tag = right_tag("one capillary, schematic")
        lbl_conc = T("protein concentrates", 28, COL_PROTEIN).move_to([2.15, 0.35, 0.0])
        self.add(hose.group, b_lbl, tag, lbl_conc)

        # Strip axes directly above capillary, exact same horizontal span [-4.2, +4.2]
        P = make_strip_axes(hw=4.2, show_ticks=True, show_ylabel=True)
        ill_tag = T("illustrative numbers", 24, TEXT).move_to([4.2, 3.22, 0.0], aligned_edge=RIGHT)

        push_draw = ValueTracker(0.0)
        pull_draw = ValueTracker(0.0)
        fill_op = ValueTracker(0.0)
        push_pulse = ValueTracker(0.0)
        gap_mob, push_mob, pull_mob = make_live_strip_curves(
            hose.hw_tr, hose.effective_sol,
            push_draw_tr=push_draw, pull_draw_tr=pull_draw,
            fill_op_tr=fill_op, push_pulse_tr=push_pulse,
        )

        self.at("lines")
        self.play(FadeOut(lbl_conc), run_time=0.3)
        self.play(Create(P), FadeIn(ill_tag), run_time=1.0)
        self.add(gap_mob, push_mob, pull_mob)

        # Orange push line flat at 40 (55 - 15)
        self.at("the push")
        lbl_push = T("push", 28, COL_PUSH).move_to(strip_pt(4.2, 0.44, 55.0))
        self.play(push_draw.animate.set_value(1.0), run_time=1.4, rate_func=linear)
        self.play(FadeIn(lbl_push), run_time=0.4)

        self.at("stays nearly flat")
        self.play(push_pulse.animate.set_value(1.0), run_time=0.45)
        self.play(push_pulse.animate.set_value(0.0), run_time=0.55)

        # Purple pull line starts at 25 and climbs (ODE solution, staying below 40)
        self.at("the pull")
        lbl_pull = T("pull", 28, COL_PROTEIN).move_to(strip_pt(4.2, 0.55, 13.0))
        self.play(pull_draw.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        self.play(FadeIn(lbl_pull), run_time=0.4)

        # Cyan gap between push and pull labelled 'net filtration' (cleanly left of 'push'!)
        self.at("starts lower")
        lbl_net = T("net filtration", 26, COL_WATER).move_to(strip_pt(4.2, 0.19, 73.0))
        leader_net = Line(
            lbl_net.get_bottom() + DOWN * 0.08,
            strip_pt(4.2, 0.16, 35.0),
            color=COL_WATER, stroke_width=2.5,
        )
        self.play(fill_op.animate.set_value(1.0), FadeIn(lbl_net), Create(leader_net), run_time=1.1)

        # Drops below thicken at left and thin out to right in step with shading
        self.at("wherever")
        self.play(hose.mod_tr.animate.set_value(1.0), run_time=1.4)
        self.finish()


class S05Equilibrium(SpokenScene):
    def construct(self):
        hose = HoseWorld(cap_hw=4.2, r_a=1.0, r_e=1.0, kf=1.2, quad=0.25, conc_vis=1.0, drop_mod=1.0)
        b_lbl = bowman_label(4.2)
        tag = right_tag("one capillary, schematic")
        P = make_strip_axes(hw=4.2, show_ticks=True, show_ylabel=True)
        ill_tag = T("illustrative numbers", 24, TEXT).move_to([4.2, 3.22, 0.0], aligned_edge=RIGHT)
        gap_mob, push_mob, pull_mob = make_live_strip_curves(hose.hw_tr, hose.effective_sol)

        lbl_push = T("push", 28, COL_PUSH).move_to(strip_pt(4.2, 0.44, 55.0))
        lbl_pull = T("pull", 28, COL_PROTEIN).move_to(strip_pt(4.2, 0.55, 13.0))
        lbl_net = T("net filtration", 26, COL_WATER).move_to(strip_pt(4.2, 0.19, 73.0))
        leader_net = Line(lbl_net.get_bottom() + DOWN * 0.08, strip_pt(4.2, 0.16, 35.0),
                          color=COL_WATER, stroke_width=2.5)

        self.add(hose.group, b_lbl, tag, P, ill_tag, gap_mob, push_mob, pull_mob,
                 lbl_push, lbl_pull, lbl_net, leader_net)

        # Steepening pull meets push at u_eq = 0.66
        self.at("pull rises")
        self.play(hose.kf_tr.animate.set_value(3.3), run_time=1.35)

        # Mark equilibrium point
        sol_eq = hose.effective_sol()
        u_eq = sol_eq["u_eq"] if sol_eq["u_eq"] is not None else 0.66
        eq_pt = strip_pt(4.2, u_eq, 40.0)
        eq_dot = Dot(eq_pt, radius=0.11, color=TEXT, stroke_color=BG, stroke_width=2.5)
        lbl_eq = T("equilibrium", 26, TEXT).move_to(strip_pt(4.2, u_eq, 54.0))

        self.at("before the far end")
        self.play(FadeIn(eq_dot, scale=1.3), FadeIn(lbl_eq, shift=UP * 0.08), run_time=0.55)

        # Show dry stretch beyond equilibrium
        self.at("beyond that point")
        drop_guide = DashedLine(
            eq_pt + DOWN * 0.14,
            [eq_pt[0], CAP_TOP + 0.06, 0.0],
            color=COL_AXIS, stroke_width=2.5, dash_length=0.12,
        )
        self.play(Create(drop_guide), run_time=0.55)

        # Rat silhouette + white tick cleanly above-left of equilibrium, well clear of human silhouette
        self.at("rats")
        rat = make_rat_silhouette(TEXT, height=0.46).move_to([1.10, 2.66, 0.0])
        tick = make_check_mark(TEXT, height=0.32).next_to(rat, RIGHT, buff=0.16)
        rat_grp = VGroup(rat, tick)
        self.play(FadeIn(rat_grp, scale=0.9), run_time=0.45)

        # Human silhouette + white '?' well to the right of rat+tick
        self.at("human")
        hum = make_human_silhouette(TEXT, height=0.52).move_to([3.20, 2.66, 0.0])
        qmk = T("?", 34, TEXT, weight=BOLD).next_to(hum, RIGHT, buff=0.16)
        hum_grp = VGroup(hum, qmk)
        self.play(FadeIn(hum_grp, scale=0.9), run_time=0.45)

        # Fade out both silhouettes and net filtration label cleanly at end of scene
        self.wait(max(0.1, 15.8 - self.elapsed()))
        self.play(FadeOut(rat_grp), FadeOut(hum_grp), FadeOut(drop_guide),
                  FadeOut(lbl_net), FadeOut(leader_net), run_time=0.5)
        self.finish()


class S06TwoThings(SpokenScene):
    def construct(self):
        hose = HoseWorld(
            cap_hw=4.2, r_a=1.0, r_e=1.0, kf=3.3, quad=0.25,
            conc_vis=1.0, drop_mod=1.0, show_arrow=False,
        )
        b_lbl = bowman_label(4.2)
        tag = right_tag("one capillary, schematic")
        P = make_strip_axes(hw=4.2, show_ticks=True, show_ylabel=True)
        ill_tag = T("illustrative numbers", 24, TEXT).move_to([4.2, 3.22, 0.0], aligned_edge=RIGHT)
        push_pulse = ValueTracker(0.0)
        gap_mob, push_mob, pull_mob = make_live_strip_curves(
            hose.hw_tr, hose.effective_sol, push_pulse_tr=push_pulse,
        )

        sol_eq = hose.effective_sol()
        u_eq = sol_eq["u_eq"] or 0.66
        eq_dot = Dot(strip_pt(4.2, u_eq, 40.0), radius=0.11, color=TEXT, stroke_color=BG, stroke_width=2.5)
        lbl_eq = T("equilibrium", 26, TEXT).move_to(strip_pt(4.2, u_eq, 54.0))
        lbl_push = T("push", 28, COL_PUSH).move_to(strip_pt(4.2, 0.44, 55.0))
        lbl_pull = T("pull", 28, COL_PROTEIN).move_to(strip_pt(4.2, 0.55, 13.0))

        self.add(hose.group, b_lbl, tag, P, ill_tag, gap_mob, push_mob, pull_mob,
                 eq_dot, lbl_eq, lbl_push, lbl_pull)

        # 'How high the pressure is' — swap 'push' -> 'pressure' at left end for clean continuity into s07
        self.at("how high")
        lbl_pres = T("pressure", 28, TEXT).move_to(strip_pt(4.2, 0.12, 55.0))
        self.play(push_pulse.animate.set_value(1.0), swap(lbl_push, lbl_pres, run_time=0.5), run_time=0.55)
        self.play(push_pulse.animate.set_value(0.0), run_time=0.45)

        # 'how much plasma flows through'
        self.at("how much plasma")
        hose.show_arrow = True
        lbl_flow = T("flow", 26, TEXT).move_to([-0.65, -0.84, 0.0])
        self.play(
            hose.bright_red.animate.set_value(1.0),
            hose.keep_lower.animate.set_value(1.0),
            FadeIn(lbl_flow),
            run_time=0.75,
        )
        self.finish()


class S07Hose(SpokenScene):
    def construct(self):
        hose = HoseWorld(
            cap_hw=4.2, r_a=1.0, r_e=1.0, kf=3.3, quad=0.25,
            conc_vis=1.0, drop_mod=1.0, show_arrow=True,
            bright_red=True, keep_lower_lane_clear=True,
        )
        b_lbl = always_redraw(lambda: T("Bowman's space", 26, COL_BOWMAN).move_to(
            [-hose.hw_tr.get_value() + 1.45, -3.00, 0.0]
        ))
        tag = right_tag("one capillary, schematic")

        P = always_redraw(lambda: make_strip_axes(hw=hose.hw_tr.get_value(), show_ticks=True, show_ylabel=True))
        ill_tag = always_redraw(lambda: T("illustrative numbers", 24, TEXT).move_to(
            [hose.hw_tr.get_value(), 3.22, 0.0], aligned_edge=RIGHT
        ))
        gap_mob, push_mob, pull_mob = make_live_strip_curves(hose.hw_tr, hose.effective_sol)

        sol_eq = hose.effective_sol()
        u_eq = sol_eq["u_eq"] or 0.66
        eq_dot = always_redraw(lambda: Dot(strip_pt(hose.hw_tr.get_value(), u_eq, 40.0),
                                           radius=0.11, color=TEXT, stroke_color=BG, stroke_width=2.5))
        lbl_eq = always_redraw(lambda: T("equilibrium", 26, TEXT).move_to(
            strip_pt(hose.hw_tr.get_value(), u_eq, 54.0)
        ))
        lbl_pres = always_redraw(lambda: T("pressure", 28, TEXT).move_to(
            strip_pt(hose.hw_tr.get_value(), 0.14, 55.0)
        ))
        lbl_pull = always_redraw(lambda: T("pull", 28, COL_PROTEIN).move_to(
            strip_pt(hose.hw_tr.get_value(), 0.55, 13.0)
        ))
        lbl_flow = always_redraw(lambda: T("flow", 26, TEXT).move_to(
            [-0.15 * hose.hw_tr.get_value(), -0.84, 0.0]
        ))

        self.add(hose.group, b_lbl, tag, P, ill_tag, gap_mob, push_mob, pull_mob,
                 eq_dot, lbl_eq, lbl_pres, lbl_pull, lbl_flow)

        # Ease back immediately so both arterioles fit generously
        self.play(hose.hw_tr.animate.set_value(3.3), run_time=1.05)

        # Afferent arteriole
        self.at("afferent")
        lbl_aff = T("afferent: in", 26, COL_AFFERENT).move_to([-4.85, 0.72, 0.0])
        self.play(hose.aff_glow.animate.set_value(1.0), FadeIn(lbl_aff, shift=UP * 0.08), run_time=0.5)
        self.play(hose.aff_glow.animate.set_value(0.0), run_time=0.35)

        # Efferent arteriole
        self.at("efferent")
        lbl_eff = T("efferent: out", 26, COL_EFFERENT).move_to([4.85, 0.72, 0.0])
        self.play(hose.eff_glow.animate.set_value(1.0), FadeIn(lbl_eff, shift=UP * 0.08), run_time=0.5)
        self.play(hose.eff_glow.animate.set_value(0.0), run_time=0.35)

        # Tap near spigot
        self.at("tap")
        hose.show_tap = True
        self.play(hose.aff_glow.animate.set_value(0.9), run_time=0.35)
        self.play(hose.aff_glow.animate.set_value(0.0), run_time=0.35)

        # Nozzle at far end
        self.at("nozzle")
        hose.show_nozzle = True
        self.play(hose.eff_glow.animate.set_value(0.9), run_time=0.35)
        self.play(hose.eff_glow.animate.set_value(0.0), run_time=0.35)

        # Leaky stretch between
        self.at("leaky stretch")
        self.play(hose.wall_pulse.animate.set_value(1.0), run_time=0.35)
        self.play(hose.wall_pulse.animate.set_value(0.0), run_time=0.45)
        self.finish()


class S08Idea(SpokenScene):
    def construct(self):
        hose = HoseWorld(
            cap_hw=3.3, r_a=1.0, r_e=1.0, kf=3.3, quad=0.25,
            conc_vis=1.0, drop_mod=1.0, show_tap=True, show_nozzle=True,
            show_arrow=True, bright_red=True, keep_lower_lane_clear=True,
        )
        b_lbl = bowman_label(3.3)
        tag = right_tag("one capillary, schematic")
        P = make_strip_axes(hw=3.3, show_ticks=True, show_ylabel=True)
        ill_tag = T("illustrative numbers", 24, TEXT).move_to([3.3, 3.22, 0.0], aligned_edge=RIGHT)
        gap_mob, push_mob, pull_mob = make_live_strip_curves(hose.hw_tr, hose.effective_sol)

        eq_dot = always_redraw(lambda: Dot(
            strip_pt(3.3, hose.effective_sol()["u_eq"] if hose.effective_sol()["u_eq"] is not None else 0.99,
                     hose.effective_sol()["push"]),
            radius=0.11, color=TEXT, stroke_color=BG, stroke_width=2.5,
        ).set_opacity(1.0 if hose.effective_sol()["u_eq"] is not None else 0.0))

        lbl_pres = T("pressure", 26, TEXT).move_to(strip_pt(3.3, 0.16, 55.0))
        lbl_pull = T("pull", 26, COL_PROTEIN).move_to(strip_pt(3.3, 0.55, 13.0))
        lbl_flow = T("flow", 26, TEXT).move_to([-0.50, -0.84, 0.0])
        lbl_aff = T("afferent: in", 26, COL_AFFERENT).move_to([-4.85, 0.72, 0.0])
        lbl_eff = T("efferent: out", 26, COL_EFFERENT).move_to([4.85, 0.72, 0.0])

        self.add(hose.group, b_lbl, tag, P, ill_tag, gap_mob, push_mob, pull_mob,
                 eq_dot, lbl_pres, lbl_pull, lbl_flow, lbl_aff, lbl_eff)

        # Round numbers appear
        self.at("two")
        n_art = T("arterial 100", 24, TEXT).move_to([-5.15, 1.38, 0.0])
        n_ven = T("venous 10", 24, TEXT).move_to([5.15, 1.38, 0.0])
        n_ra = T("1 unit", 24, TEXT).move_to([-4.70, -1.52, 0.0])
        n_re = T("1 unit", 24, TEXT).move_to([4.70, -1.52, 0.0])
        n_flow = T("flow 45 units", 24, TEXT).move_to([-0.50, -0.84, 0.0])
        n_cap = T("capillary 55", 24, TEXT).move_to(strip_pt(3.3, 0.22, 55.0))

        self.play(
            FadeIn(n_art), FadeIn(n_ven), FadeIn(n_ra), FadeIn(n_re),
            swap(lbl_flow, n_flow, run_time=0.7),
            swap(lbl_pres, n_cap, run_time=0.7),
            run_time=0.85,
        )

        # Total resistance sets the flow: both rings glow + bracket spanning them
        # Label sits cleanly inside open upper strip at y=2.52 (far below 'illustrative numbers' at y=3.22!)
        self.at("total resistance")
        br_l = Line([-4.70, -1.82, 0], [-4.70, -2.72, 0], color=TEXT, stroke_width=3.5)
        br_r = Line([4.70, -1.82, 0], [4.70, -2.72, 0], color=TEXT, stroke_width=3.5)
        br_h = Line([-4.70, -2.72, 0], [4.70, -2.72, 0], color=TEXT, stroke_width=3.5)
        bracket = VGroup(br_l, br_h, br_r)
        lbl_tot = T("total sets flow", 28, TEXT).move_to([0.0, 2.52, 0.0])
        self.play(
            hose.aff_glow.animate.set_value(1.0),
            hose.eff_glow.animate.set_value(1.0),
            Create(bracket),
            FadeIn(lbl_tot),
            b_lbl.animate.shift(DOWN * 0.22),
            run_time=0.8,
        )

        # Efferent share sets pressure: only yellow ring glows
        self.at("efferent share")
        lbl_shr = T("share sets pressure", 28, COL_EFFERENT).move_to([0.0, 2.52, 0.0])
        self.play(
            hose.aff_glow.animate.set_value(0.0),
            FadeOut(bracket),
            swap(lbl_tot, lbl_shr, run_time=0.7),
            b_lbl.animate.shift(UP * 0.22),
            run_time=0.8,
        )

        # Afferent moves pressure and flow the same way (arrows only, no new numbers, tag 'schematic directions')
        self.at("afferent moves")
        tag_dir = T("schematic directions", 24, TEXT).move_to([3.3, 3.22, 0.0], aligned_edge=RIGHT)
        lbl_flow_clean = T("flow", 26, TEXT).move_to([-0.50, -0.84, 0.0])
        self.play(
            hose.eff_glow.animate.set_value(0.0),
            FadeOut(lbl_shr), FadeOut(n_art), FadeOut(n_ven),
            FadeOut(n_ra), FadeOut(n_re), FadeOut(n_cap),
            swap(n_flow, lbl_flow_clean, run_time=0.45),
            swap(ill_tag, tag_dir, run_time=0.45),
            run_time=0.5,
        )

        # Tighten green tap: orange push drops AND red arrow thins (clear hold so arrows read cleanly)
        arr_push_dn = Arrow([0.8, 2.05, 0], [0.8, 1.30, 0], buff=0, color=COL_PUSH, stroke_width=6, tip_length=0.22)
        arr_flow_dn = Arrow([1.4, -0.22, 0], [1.4, -0.74, 0], buff=0, color=COL_PLASMA, stroke_width=6, tip_length=0.22)
        self.play(
            hose.ra_tr.animate.set_value(1.90),
            hose.aff_glow.animate.set_value(0.9),
            FadeIn(arr_push_dn), FadeIn(arr_flow_dn),
            run_time=0.95,
        )
        self.wait(0.35)
        self.play(
            hose.ra_tr.animate.set_value(1.0),
            hose.aff_glow.animate.set_value(0.0),
            FadeOut(arr_push_dn), FadeOut(arr_flow_dn),
            run_time=0.75,
        )

        # Efferent moves them opposite ways: yellow nozzle tightens -> orange push rises, red arrow thins
        self.at("efferent moves")
        arr_push_up = Arrow([0.8, 1.48, 0], [0.8, 2.25, 0], buff=0, color=COL_PUSH, stroke_width=6, tip_length=0.22)
        arr_flow_dn2 = Arrow([1.4, -0.22, 0], [1.4, -0.74, 0], buff=0, color=COL_PLASMA, stroke_width=6, tip_length=0.22)
        self.play(
            hose.re_tr.animate.set_value(1.95),
            hose.eff_glow.animate.set_value(0.9),
            FadeIn(arr_push_up), FadeIn(arr_flow_dn2),
            run_time=0.95,
        )
        self.wait(0.35)
        self.play(
            hose.re_tr.animate.set_value(1.0),
            hose.eff_glow.animate.set_value(0.0),
            FadeOut(arr_push_up), FadeOut(arr_flow_dn2),
            run_time=0.75,
        )
        self.finish()


def _build_predict_world(re_init=1.0):
    """Shared builder for s09_predict, s10_pause, and start of s11_answer (no-spoiler frozen pull & drops)."""
    base_sol = solve_capillary(1.0, 1.0, kf=3.3, quad=0.25, n=80)
    hose = HoseWorld(
        cap_hw=3.3, r_a=1.0, r_e=re_init, kf=3.3, quad=0.25,
        conc_vis=1.0, drop_mod=1.0, ode_freeze=base_sol,
        show_tap=True, show_nozzle=True, show_arrow=True,
        bright_red=True, keep_lower_lane_clear=True,
    )
    # Omit mmHg y-label on the tickless schematic strip so top band stays spotless for question card
    P = make_strip_axes(hw=3.3, show_ticks=False, show_ylabel=False)
    b_lbl = bowman_label(3.3)
    tag = right_tag("one capillary, schematic")
    lbl_aff = T("afferent: in", 26, COL_AFFERENT).move_to([-4.85, 0.72, 0.0])
    lbl_eff = T("efferent: out", 26, COL_EFFERENT).move_to([4.85, 0.72, 0.0])
    lbl_flow = T("flow", 26, TEXT).move_to([-0.50, -0.84, 0.0])
    lbl_pull = T("pull", 26, COL_PROTEIN).move_to(strip_pt(3.3, 0.55, 13.0))

    push_pulse = ValueTracker(0.0)

    def _mk_push():
        push = hose.sol()["push"]
        pp = float(push_pulse.get_value())
        col = interpolate_color(ManimColor(COL_PUSH), ManimColor(TEXT), 0.35 * pp)
        return Line(strip_pt(3.3, 0.0, push), strip_pt(3.3, 1.0, push),
                    color=col, stroke_width=6.0 + 4.0 * pp)

    def _mk_pull_frozen():
        sol = hose.effective_sol()
        us, pis, push = sol["u"], sol["pi"], sol["push"]
        pis = draw_pi(us, pis, push)
        pts = [strip_pt(3.3, us[i], min(push, pis[i])) for i in range(len(us))]
        m = VMobject(stroke_color=COL_PROTEIN, stroke_width=6.0, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m

    def _mk_gap_frozen():
        sol = hose.effective_sol()
        us, pis, push_eff = sol["u"], sol["pi"], sol["push"]
        b = float(hose.ode_blend_tr.get_value())
        p_top = 40.0 * (1.0 - b) + push_eff * b
        pis = draw_pi(us, pis, p_top)
        mask = (p_top - pis) > 0.15
        if not np.any(mask):
            return VMobject(fill_opacity=0, stroke_opacity=0)
        idx = np.where(mask)[0]
        i0, i1 = int(idx[0]), int(idx[-1])
        if i1 + 1 < len(us):
            i1 += 1
        top_pts = [strip_pt(3.3, us[i], p_top) for i in range(i0, i1 + 1)]
        bot_pts = [strip_pt(3.3, us[i], min(p_top, pis[i])) for i in range(i1, i0 - 1, -1)]
        return Polygon(*(top_pts + bot_pts), fill_color=COL_WATER, fill_opacity=0.28, stroke_width=0)

    def _mk_eq_dot():
        sol = hose.effective_sol()
        b = float(hose.ode_blend_tr.get_value())
        u_eq = sol["u_eq"] if sol["u_eq"] is not None else 0.66
        p_top = 40.0 * (1.0 - b) + sol["push"] * b
        return Dot(strip_pt(3.3, u_eq, p_top), radius=0.11, color=TEXT, stroke_color=BG, stroke_width=2.5)

    gap_mob = always_redraw(_mk_gap_frozen)
    push_mob = always_redraw(_mk_push)
    pull_mob = always_redraw(_mk_pull_frozen)
    eq_dot = always_redraw(_mk_eq_dot)

    all_mobs = VGroup(hose.group, P, b_lbl, tag, lbl_aff, lbl_eff, lbl_flow, lbl_pull,
                      gap_mob, push_mob, pull_mob, eq_dot)
    return all_mobs, dict(hose=hose, P=P, push_pulse=push_pulse, eq_dot=eq_dot,
                          lbl_pull=lbl_pull, tag=tag, gap=gap_mob, push=push_mob, pull=pull_mob)


class S09Predict(SpokenScene):
    def construct(self):
        all_mobs, refs = _build_predict_world(re_init=1.0)
        hose = refs["hose"]
        self.add(all_mobs)

        # Three slow steps squeezing the yellow nozzle
        self.at("squeeze")
        self.play(hose.re_tr.animate.set_value(1.5), run_time=0.85)

        self.at("harder")
        self.play(hose.re_tr.animate.set_value(2.3), run_time=0.70)

        self.at("harder again")
        self.play(hose.re_tr.animate.set_value(3.5), run_time=0.85)

        self.at("pressure")
        self.play(refs["push_pulse"].animate.set_value(1.0), run_time=0.4)
        self.play(refs["push_pulse"].animate.set_value(0.0), run_time=0.45)

        self.at("does filtration")
        q = question_card("Harder squeeze, more filtration?", y=3.35, color=TEXT, size=34)
        self.play(FadeIn(q, shift=DOWN * 0.08), run_time=0.55)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Harder squeeze, more filtration?"
    CARD = {"y": 3.35, "color": TEXT, "size": 34}
    RING_AT = (5.95, 3.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        all_mobs, _ = _build_predict_world(re_init=3.5)
        return all_mobs


class S11Answer(SpokenScene):
    def construct(self):
        all_mobs, refs = _build_predict_world(re_init=3.5)
        hose = refs["hose"]
        q = question_card("Harder squeeze, more filtration?", y=3.35, color=TEXT, size=34)
        self.add(all_mobs, q)

        # Dissolve question card
        self.play(FadeOut(q), run_time=0.55)

        # Cuts the flow: squeeze further
        self.at("cuts the flow")
        self.play(hose.re_tr.animate.set_value(4.3), run_time=1.2)

        # Protein concentrates sooner -> unlock ODE so purple steepens, equilibrium dot slides left, dry stretch grows
        self.at("protein concentrates")
        self.play(hose.ode_blend_tr.animate.set_value(1.0), run_time=1.55)

        # Pull catches up earlier -> squeeze further (u_eq ~ 0.14: dramatic shift while left drops stay visible!)
        self.at("catches up")
        self.play(hose.re_tr.animate.set_value(5.0), run_time=1.25)

        # Never exceed arterial pressure -> dashed WHITE ceiling line at Pa - P_BS = 85
        self.at("never exceed")
        ceil_y = P_A - P_BS  # 85 mmHg
        ceil_line = DashedLine(
            strip_pt(3.3, 0.0, ceil_y),
            strip_pt(3.3, 1.0, ceil_y),
            color=TEXT, stroke_width=3.5, dash_length=0.16,
        )
        lbl_ceil = T("arterial pressure", 26, TEXT).move_to([3.3, 3.16, 0.0], aligned_edge=RIGHT)
        self.play(Create(ceil_line), FadeIn(lbl_ceil), run_time=0.85)

        # Gain levels off: squeeze harder in two steps while push climbs in ever-smaller steps beneath ceiling
        self.at("gain levels off")
        self.play(hose.re_tr.animate.set_value(5.8), run_time=0.75)
        self.play(hose.re_tr.animate.set_value(6.8), run_time=0.75)
        self.finish()


class S12Biphasic(SpokenScene):
    def construct(self):
        rs, gfrs, ffs = precompute_biphasic(r_min=1.0, r_max=3.2, kf=1.2, quad=0.0, m=100)
        g_start = float(gfrs[0])   # 12.17
        g_peak = float(gfrs.max()) # 16.17
        gfr_y = lambda r: 0.38 + 0.34 * (float(np.interp(r, rs, gfrs)) - g_start) / (g_peak - g_start)
        ff_y = lambda r: 0.16 + 0.72 * (float(np.interp(r, rs, ffs)) - float(ffs[0])) / (float(ffs[-1]) - float(ffs[0]))

        re_tr = ValueTracker(1.0)
        ff_tr = ValueTracker(1.0)
        drop_mult = ValueTracker(1.0)
        drop_mult.add_updater(lambda m, dt: m.set_value(
            0.55 + 1.15 * ((float(np.interp(re_tr.get_value(), rs, gfrs)) - g_start) / (g_peak - g_start) + 0.35)
        ))

        hose = HoseWorld(
            cap_hw=3.3, r_a=1.0, r_e=1.0, kf=1.2, quad=0.0,
            conc_vis=1.0, drop_mod=0.0, drop_rate_tr=drop_mult,
            show_tap=True, show_nozzle=True, show_arrow=True,
            bright_red=True, keep_lower_lane_clear=True,
        )
        hose.re_tr.add_updater(lambda m, dt: m.set_value(re_tr.get_value()))
        self.add(drop_mult, hose.re_tr)

        b_lbl = bowman_label(3.3)
        tag = right_tag("schematic")
        lbl_aff = T("afferent: in", 26, COL_AFFERENT).move_to([-4.85, 0.72, 0.0])
        lbl_eff = T("efferent: out", 26, COL_EFFERENT).move_to([4.85, 0.72, 0.0])
        lbl_flow = T("flow", 26, TEXT).move_to([-0.50, -0.84, 0.0])

        G = Plot(
            box=(-3.3, 3.3, 0.70, 2.95),
            xr=(1.0, 3.2),
            yr=(0.0, 1.0),
            xticks=(),
            yticks=(),
            xlabel="efferent squeeze",
            ylabel="",
            color=TEXT,
            size=24,
            label_size=26,
            stroke=3,
        )
        G.axes.set_stroke(COL_AXIS, width=3)

        gfr_curve = G.live_curve(gfr_y, re_tr, color=COL_WATER, width=6.5)
        gfr_dot = G.dot(lambda: re_tr.get_value(), lambda: gfr_y(re_tr.get_value()),
                        color=COL_WATER, ring=TEXT, radius=0.10)
        ff_curve = G.live_curve(ff_y, ff_tr, color=TEXT, width=5.5)

        self.add(hose.group, b_lbl, tag, lbl_aff, lbl_eff, lbl_flow, G, gfr_curve, gfr_dot, ff_curve)

        self.at("mild squeeze")
        self.play(re_tr.animate.set_value(1.72), run_time=2.2, rate_func=smooth)

        self.at("hard squeeze")
        lbl_filt = T("filtration", 26, COL_WATER).move_to([3.52, G.pt(3.2, gfr_y(3.2))[1], 0.0], aligned_edge=LEFT)
        self.play(re_tr.animate.set_value(3.2), run_time=2.2, rate_func=smooth)
        self.play(FadeIn(lbl_filt), run_time=0.45)

        self.at("throughout")
        self.play(ff_tr.animate.set_value(3.2), run_time=3.1, rate_func=linear)

        self.at("filtration fraction")
        lbl_ff = T("filtration fraction", 26, TEXT).move_to([3.52, G.pt(3.2, ff_y(3.2))[1], 0.0], aligned_edge=LEFT)
        self.play(FadeIn(lbl_ff), run_time=0.5)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        rs, gfrs, ffs = precompute_biphasic(r_min=1.0, r_max=3.2, kf=1.2, quad=0.0, m=100)
        g_start, g_peak = float(gfrs[0]), float(gfrs.max())
        gfr_y = lambda r: 0.38 + 0.34 * (float(np.interp(r, rs, gfrs)) - g_start) / (g_peak - g_start)
        ff_y = lambda r: 0.16 + 0.72 * (float(np.interp(r, rs, ffs)) - float(ffs[0])) / (float(ffs[-1]) - float(ffs[0]))

        hose = HoseWorld(
            cap_hw=3.3, r_a=1.0, r_e=3.2, kf=1.2, quad=0.25,
            conc_vis=1.0, drop_mod=1.0, show_tap=True, show_nozzle=True,
            show_arrow=True, bright_red=True, keep_lower_lane_clear=True,
        )
        b_lbl = bowman_label(3.3)
        tag = right_tag("one capillary, schematic")
        lbl_aff = T("afferent: in", 26, COL_AFFERENT).move_to([-4.85, 0.72, 0.0])
        lbl_eff = T("efferent: out", 26, COL_EFFERENT).move_to([4.85, 0.72, 0.0])
        lbl_flow = T("flow", 26, TEXT).move_to([-0.50, -0.84, 0.0])

        G = Plot(box=(-3.3, 3.3, 0.70, 2.95), xr=(1.0, 3.2), yr=(0.0, 1.0),
                 xticks=(), yticks=(), xlabel="efferent squeeze", ylabel="",
                 color=TEXT, size=24, label_size=26, stroke=3)
        G.axes.set_stroke(COL_AXIS, width=3)
        old_gfr = G.curve(gfr_y, color=COL_WATER, width=6.5)
        old_ff = G.curve(ff_y, color=TEXT, width=5.5)
        old_lbl_f = T("filtration", 26, COL_WATER).move_to([3.52, G.pt(3.2, gfr_y(3.2))[1], 0.0], aligned_edge=LEFT)
        old_lbl_ff = T("filtration fraction", 26, TEXT).move_to([3.52, G.pt(3.2, ff_y(3.2))[1], 0.0], aligned_edge=LEFT)
        old_graph = VGroup(G, old_gfr, old_ff, old_lbl_f, old_lbl_ff)

        self.add(hose.group, b_lbl, tag, lbl_aff, lbl_eff, lbl_flow, old_graph)

        # Morph graph back into baseline push-and-pull strip while nozzle relaxes to 1.0
        P = make_strip_axes(hw=3.3, show_ticks=True, show_ylabel=True)
        push_pulse = ValueTracker(0.0)
        gap_pulse = ValueTracker(0.0)
        gap_mob, push_mob, pull_mob = make_live_strip_curves(
            hose.hw_tr, hose.effective_sol, push_pulse_tr=push_pulse, gap_pulse_tr=gap_pulse,
        )
        lbl_push = T("push", 26, COL_PUSH).move_to(strip_pt(3.3, 0.38, 55.0))
        lbl_pull = T("pull", 26, COL_PROTEIN).move_to(strip_pt(3.3, 0.55, 13.0))

        self.play(
            hose.re_tr.animate.set_value(1.0),
            FadeOut(old_graph),
            run_time=1.0,
        )
        self.play(FadeIn(P), FadeIn(gap_mob), FadeIn(push_mob), FadeIn(pull_mob), run_time=0.55)
        self.play(FadeIn(lbl_push), FadeIn(lbl_pull), run_time=0.35)

        # Filtering needs push to beat pull -> cyan gap pulses
        self.at("filtering")
        self.play(gap_pulse.animate.set_value(1.0), run_time=0.55)
        self.play(gap_pulse.animate.set_value(0.0), run_time=0.65)

        # Combined resistance decides how much plasma arrives -> both rings glow + red arrow pulses
        self.at("combined resistance")
        self.play(
            hose.aff_glow.animate.set_value(1.0),
            hose.eff_glow.animate.set_value(1.0),
            hose.arrow_pulse.animate.set_value(1.0),
            run_time=0.8,
        )
        self.play(
            hose.aff_glow.animate.set_value(0.0),
            hose.eff_glow.animate.set_value(0.0),
            hose.arrow_pulse.animate.set_value(0.0),
            run_time=0.8,
        )

        # Where that resistance sits -> glow slides from green ring to yellow ring and orange line pulses
        self.at("where that")
        bead = Dot([-4.70, CAP_Y, 0.0], radius=0.18, color=GOLD, fill_opacity=0.95)
        self.play(FadeIn(bead), hose.aff_glow.animate.set_value(1.0), run_time=0.35)
        self.play(
            bead.animate.move_to([4.70, CAP_Y, 0.0]),
            hose.aff_glow.animate.set_value(0.0),
            hose.eff_glow.animate.set_value(1.0),
            run_time=1.1,
        )
        self.play(
            FadeOut(bead),
            push_pulse.animate.set_value(1.0),
            run_time=0.55,
        )
        self.play(
            push_pulse.animate.set_value(0.0),
            hose.eff_glow.animate.set_value(0.0),
            run_time=0.6,
        )
        self.finish()


class S14End(EndCard):
    LINE = "Total arteriole resistance sets flow; the efferent share sets filter pressure."
