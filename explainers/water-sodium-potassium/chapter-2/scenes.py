"""Potassium on Two Clocks — STEMhop narrated animation (Water, Sodium and Potassium Balance, Chapter 2).

COLOUR MAP (one colour per concept, carried across the whole film):
    BLUE    (#58C4DD) : water, extracellular/tubular fluid, delivery dial
    GOLD    (#D4A843) : sodium ions
    PURPLE  (#B589FF) : potassium ions, potassium channels (ROMK, BK), potassium pools/bars
    TEXT    (#E8EAF0) : membranes, gauge, clocks, brackets, readings and primary labels
    RED     (#FC6255) : sodium-potassium pump (Na+/K+-ATPase)
    TEAL    (#3FB8C0) : insulin and insulin receptor
    MAGENTA (#F062C0) : epinephrine and beta2-adrenergic receptor
    ORANGE  (#F59E42) : sodium-loop hormones (aldosterone, angiotensin II)
    GREY    (#8B93A1) : schematic scope tag and faint inactive tracks only

CARRIED WORLD:
    A 16:9 cross-section with a pale BLUE fluid tank on the left (split by a dashed TEXT membrane
    into "cells" on the left 2/3 and "outside cells" on the right 1/3), a tap above "outside cells",
    a collecting duct outlet at bottom right, and a tall TEXT plasma-concentration gauge on the right.
    The view zooms to the nephron / distal tubule cells when renal secretion is the subject and pulls
    back to the full world for the two-clock synthesis.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s00_link_and_question : Ghost 1 L of BLUE water pours from tap and equilibrates across both
                            compartments (computed spread fraction 0->1); GOLD Na+ dims, PURPLE K+
                            brightens in Brownian walk (~60 inside, 5 outside); gauge morphs from
                            140 (Na+) to 4.2 on a 3..6 scale (K+).
    s02_pool              : Brownian K+ ions continue; cells side adds muscle-fibre stripes;
                            equation "14 L x 4.2 = about 59 mEq" builds under outside; a 3,500 mEq
                            bar grows above the tank with a computed 1.7% (59/3500) PURPLE sliver.
    s03_load              : Two PURPLE bars grow in exact 59:70 length ratio; food tap fills with
                            PURPLE dots queuing at its mouth; three RED pumps appear along membrane
                            while duct dims.
    s04_shift             : Food tap pours PURPLE dots into outside cells; TEAL insulin and MAGENTA
                            epinephrine dock on receptors; RED pumps spin faster and drive computed
                            trans-membrane K+ trajectories into cells; needle stays in 3.5..5.0;
                            "minutes" clock sweeps rapidly.
    s05_idea              : Full world highlights the fast pump/"minutes" shift arrow into cells
                            and the slow duct/"hours" secretion arrow into urine while K+ dots flow
                            along both paths.
    s06_filter            : Tank shrinks to top half; nephron strip opens below with continuous fluid
                            flow; computed stream of K+ enters at filter (756/day), ~90% diverts up
                            reabsorption arrow to tank, <10% trickles into distal segment.
    s07_secrete           : Zoom to distal wall (principal + intercalated cells); food tap pours and
                            urine K+ stream thickens; RED pump imports K+ into principal cell; ROMK
                            door opens, then flow accelerates and BK (flow) door opens on intercalated
                            cell, pouring more K+ into lumen.
    s08_rate              : Schematic aldosterone and delivery dials swing their needles; ORANGE
                            aldosterone docks on principal cell widening ROMK; BLUE fluid with GOLD
                            Na+ accelerates from upstream, raising K+ efflux through both doors.
    s09_predict           : Distal segment splits into two identical stacked lanes ("after volume loss"
                            and "high plasma potassium"), both with docked ORANGE aldosterone: high;
                            slow baseline flow and bobbing K+ dots; question card appears at top.
    s11_answer            : Bottom lane delivery fluid widens and accelerates (GOLD Na+ + BLUE water),
                            faint angiotensin II outline, K+ pours through ROMK & BK ("potassium
                            excreted"); then top lane thins to trickle, solid ORANGE angiotensin II
                            narrows ROMK, only a trickle passes ("potassium kept").
    s12_paradox           : Both lanes keep flowing at their contrasting rates while both aldosterone
                            tokens pulse together, then delivery and angiotensin II pulse in turn, and
                            a TEXT bracket joins both lanes as "aldosterone paradox".
    s13_close             : Lanes merge back into full world (tank + pumps + minutes clock above,
                            nephron + hours clock below, gauge at right); food tap pours, pumps spin
                            and "minutes" clock sweeps fast while K+ enters muscle, then "hours" clock
                            sweeps slowly as K+ leaves via distal cells into urine.
"""

import numpy as np
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B589FF"
MAGENTA = "#F062C0"
ORANGE = "#F59E42"

# Tank and gauge geometry (16:9 safe frame x in [-6.3, 6.3], y in [-3.5, 3.5])
TANK_X0, TANK_X1 = -6.1, 2.2
TANK_Y0, TANK_Y1 = -2.15, 1.65
MEMB_X = -0.55   # left 2/3 = cells (-6.1..-0.55), right 1/3 = outside (-0.55..2.2)
GAUGE_X = 4.55


def _clamp_box(p, x0, x1, y0, y1, r, avoid_boxes=()):
    """Keep a particle inside [x0+r, x1-r] x [y0+r, y1-r] and outside any avoid_boxes."""
    p[0] = np.clip(p[0], x0 + r, x1 - r)
    p[1] = np.clip(p[1], y0 + r, y1 - r)
    for bx0, bx1, by0, by1 in avoid_boxes:
        if bx0 - r < p[0] < bx1 + r and by0 - r < p[1] < by1 + r:
            dists = [
                (abs(p[0] - (bx0 - r)), np.array([bx0 - r, p[1], 0.0])),
                (abs((bx1 + r) - p[0]), np.array([bx1 + r, p[1], 0.0])),
                (abs(p[1] - (by0 - r)), np.array([p[0], by0 - r, 0.0])),
                (abs((by1 + r) - p[1]), np.array([p[0], by1 + r, 0.0])),
            ]
            _, best = min(dists, key=lambda item: item[0])
            p[0], p[1] = np.clip(best[0], x0 + r, x1 - r), np.clip(best[1], y0 + r, y1 - r)
    return p


def make_ion_swarm(n, bounds, color, radius=0.072, seed=7, speed=0.65, opacity=1.0, avoid_boxes=()):
    """Create a VGroup of ions performing a bounded computed 2D random walk."""
    x0, x1, y0, y1 = bounds
    mx = min(0.14, max(0.01, (x1 - x0) * 0.2))
    my = min(0.14, max(0.01, (y1 - y0) * 0.2))
    r_pad = min(radius + 0.04, max(0.01, (x1 - x0) * 0.25), max(0.01, (y1 - y0) * 0.25))
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(n):
        p = np.array([rng.uniform(x0 + mx, x1 - mx), rng.uniform(y0 + my, y1 - my), 0.0])
        _clamp_box(p, x0, x1, y0, y1, r_pad, avoid_boxes)
        d = Dot(p, radius=radius, color=color, fill_opacity=opacity)
        d._vel = rng.normal(0.0, speed, size=2)
        dots.add(d)

    def step(group, dt, x0=x0, x1=x1, y0=y0, y1=y1, r=r_pad, rng=rng, speed=speed, avoid=avoid_boxes):
        if dt <= 0:
            return
        dt_c = min(dt, 0.08)
        for d in group:
            d._vel += rng.normal(0.0, speed * 2.4 * np.sqrt(dt_c), size=2)
            sp = np.linalg.norm(d._vel)
            if sp > speed * 1.5:
                d._vel = d._vel / sp * (speed * 1.5)
            p = d.get_center().copy()
            p[0] += d._vel[0] * dt_c
            p[1] += d._vel[1] * dt_c
            if p[0] < x0 + r or p[0] > x1 - r:
                d._vel[0] *= -1
            if p[1] < y0 + r or p[1] > y1 - r:
                d._vel[1] *= -1
            _clamp_box(p, x0, x1, y0, y1, r, avoid)
            d.move_to(p)

    dots.add_updater(step)
    return dots


def make_fluid_stream(n, x0, x1, y_center, spread_y=0.28, speed_tracker=None, base_speed=0.25,
                      color=BLUE, dash_len=0.42, seed=31):
    """Stream of horizontal fluid flow streaks moving left-to-right through a tubule segment."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        u0 = (i / n + rng.uniform(-0.02, 0.02)) % 1.0
        yy = y_center + rng.uniform(-spread_y, spread_y)
        xx = x0 + u0 * (x1 - x0 - dash_len)
        ln = Line([xx, yy, 0], [xx + dash_len, yy, 0], color=color, stroke_width=4.5, stroke_opacity=0.68)
        ln._u = u0
        ln._yy = yy
        g.add(ln)

    def upd(grp, dt):
        if dt <= 0:
            return
        sp = speed_tracker.get_value() if speed_tracker is not None else base_speed
        span = x1 - x0 - dash_len
        for ln in grp:
            ln._u = (ln._u + sp * dt) % 1.0
            xx = x0 + ln._u * span
            ln.put_start_and_end_on([xx, ln._yy, 0], [xx + dash_len, ln._yy, 0])

    g.add_updater(upd)
    return g


def build_pump_icon(center, color=RED, scale=1.0):
    """Build a recognisable membrane transporter pump shape (paired channel arms + central rotor)."""
    c = np.array(center, dtype=float)
    top_cap = RoundedRectangle(corner_radius=0.06, width=0.46 * scale, height=0.14 * scale,
                               color=color, fill_color=color, fill_opacity=0.85, stroke_width=2).move_to(c + UP * 0.14 * scale)
    bot_cap = RoundedRectangle(corner_radius=0.06, width=0.46 * scale, height=0.14 * scale,
                               color=color, fill_color=color, fill_opacity=0.85, stroke_width=2).move_to(c + DOWN * 0.14 * scale)
    rotor = Circle(radius=0.10 * scale, color=TEXT, stroke_width=2.5, fill_color=color, fill_opacity=0.5).move_to(c)
    spoke = Line(c + LEFT * 0.08 * scale, c + RIGHT * 0.08 * scale, color=TEXT, stroke_width=2.5)
    g = VGroup(top_cap, bot_cap, rotor, spoke)
    g.rotor_spoke = VGroup(rotor, spoke)
    return g


def build_clock(center, label_text, radius=0.34, speed_rad=0.0, label_dir=DOWN):
    """Build a TEXT clock icon. The hand is still until g.spin(rad_per_s) is called at the narrated cue
    (g.spin(0) stops it). The updater sits on the face, which is in the scene, so the hand really turns."""
    c = np.array(center, dtype=float)
    face = Circle(radius=radius, color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.85).move_to(c)
    tick12 = Line(c + UP * (radius * 0.72), c + UP * (radius * 0.96), color=TEXT, stroke_width=2.5)
    tick3 = Line(c + RIGHT * (radius * 0.72), c + RIGHT * (radius * 0.96), color=TEXT, stroke_width=2.5)
    center_dot = Dot(c, radius=0.035, color=TEXT)
    theta = ValueTracker(PI / 2)
    hand = always_redraw(lambda: Line(
        c, c + radius * 0.74 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0.0]),
        color=TEXT, stroke_width=3.5
    ))
    lab = T(label_text, size=26, color=TEXT).next_to(face, label_dir, buff=0.14)
    g = VGroup(face, tick12, tick3, center_dot, hand, lab)

    def spin(rad_per_s, face=face, theta=theta):
        face.clear_updaters()
        if rad_per_s:
            face.add_updater(lambda m, dt, s=rad_per_s: theta.increment_value(-s * dt))
    g.spin = spin
    if speed_rad:
        spin(speed_rad)
    g.theta = theta
    g.face = face
    g.label = lab
    return g


def build_tank_world(show_muscle_stripes=False, cells_label="cells", tap_label=None,
                     duct_opacity=1.0, show_tap=True):
    """Build the carried tank world (cells + outside cells + membrane + tap + duct)."""
    h = TANK_Y1 - TANK_Y0
    ymid = (TANK_Y0 + TANK_Y1) / 2

    water_bg = Rectangle(width=TANK_X1 - TANK_X0, height=h, stroke_width=0,
                         fill_color=BLUE, fill_opacity=0.12).move_to([(TANK_X0 + TANK_X1) / 2, ymid, 0])
    outer_box = RoundedRectangle(corner_radius=0.14, width=TANK_X1 - TANK_X0, height=h,
                                 stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(water_bg)
    membrane = DashedLine([MEMB_X, TANK_Y1 - 0.04, 0], [MEMB_X, TANK_Y0 + 0.04, 0],
                          color=TEXT, stroke_width=3, dash_length=0.14)

    # 4 faint muscle-fibre stripes strictly below the 98% inside label zone
    stripes = VGroup()
    if show_muscle_stripes:
        for sy in (0.28, -0.32, -0.92, -1.52):
            ln = Line([TANK_X0 + 0.25, sy, 0], [MEMB_X - 0.25, sy, 0],
                      color=PURPLE, stroke_width=1.8, stroke_opacity=0.24)
            stripes.add(ln)

    lbl_cells = T(cells_label, size=28, color=TEXT).move_to([(TANK_X0 + MEMB_X) / 2, TANK_Y1 - 0.28, 0])
    lbl_out = T("outside cells", size=28, color=TEXT).move_to([(MEMB_X + TANK_X1) / 2, TANK_Y1 - 0.28, 0])

    tap_x = 1.55
    tap = VGroup()
    if show_tap:
        neck = Rectangle(width=0.38, height=0.55, stroke_color=TEXT, stroke_width=2.5,
                         fill_color=BLUE, fill_opacity=0.18).move_to([tap_x, TANK_Y1 + 0.30, 0])
        spout = Line([tap_x - 0.22, TANK_Y1 + 0.03, 0], [tap_x + 0.22, TANK_Y1 + 0.03, 0], color=TEXT, stroke_width=3)
        valve = Line([tap_x - 0.24, TANK_Y1 + 0.62, 0], [tap_x + 0.24, TANK_Y1 + 0.62, 0], color=TEXT, stroke_width=4)
        tap.add(neck, spout, valve)
        if tap_label:
            tl = T(tap_label, size=26, color=TEXT).next_to(neck, LEFT, buff=0.14)
            tap.add(tl)
            tap.label = tl

    duct_x = 1.55
    duct_h = 0.72
    duct_bg = Rectangle(width=0.46, height=duct_h, stroke_width=0,
                        fill_color=BLUE, fill_opacity=0.15 * duct_opacity).move_to([duct_x, TANK_Y0 - duct_h / 2, 0])
    duct_l = Line([duct_x - 0.23, TANK_Y0, 0], [duct_x - 0.23, TANK_Y0 - duct_h, 0],
                  color=TEXT, stroke_width=3, stroke_opacity=duct_opacity)
    duct_r = Line([duct_x + 0.23, TANK_Y0, 0], [duct_x + 0.23, TANK_Y0 - duct_h, 0],
                  color=TEXT, stroke_width=3, stroke_opacity=duct_opacity)
    duct = VGroup(duct_bg, duct_l, duct_r)

    world = VGroup(water_bg, stripes, outer_box, membrane, lbl_cells, lbl_out, tap, duct)
    world.water_bg = water_bg
    world.outer_box = outer_box
    world.membrane = membrane
    world.stripes = stripes
    world.lbl_cells = lbl_cells
    world.lbl_out = lbl_out
    world.tap = tap
    world.duct = duct
    world.tap_x = tap_x
    world.duct_x = duct_x
    return world


def build_gauge(val_tracker, title_text="plasma potassium", scale_range=(3.0, 6.0),
                ticks=(3, 4, 5, 6), fmt="{:.1f}", unit_text="mEq / L", show_band=True,
                center_x=GAUGE_X, y0=-1.65, y1=1.45, live=True, show_readout=True):
    """Build the tall vertical TEXT gauge driven by `val_tracker` (marker and readout always agree)."""
    bar_x = center_x - 0.35
    scale_line = Line([bar_x, y0, 0], [bar_x, y1, 0], color=TEXT, stroke_width=3.5)

    def y_of(v):
        f = np.clip((v - scale_range[0]) / (scale_range[1] - scale_range[0]), 0.0, 1.0)
        return y0 + f * (y1 - y0)

    tick_group = VGroup()
    for tv in ticks:
        ty = y_of(tv)
        tk = Line([bar_x - 0.14, ty, 0], [bar_x, ty, 0], color=TEXT, stroke_width=2.5)
        tick_group.add(tk)   # tick marks only: the narration never says 3, 5, 6, 130, 140 or 150

    band_group = VGroup()
    if show_band and scale_range == (3.0, 6.0):
        yb0, yb1 = y_of(3.5), y_of(5.0)
        band = Rectangle(width=0.34, height=yb1 - yb0, stroke_color=TEXT, stroke_width=2.2,
                         fill_color=TEXT, fill_opacity=0.10).move_to([bar_x + 0.17, (yb0 + yb1) / 2, 0])
        band_lab = T("usual\nrange", size=24, color=TEXT, line_spacing=0.8).next_to(band, RIGHT, buff=0.18)
        band_group.add(band, band_lab)

    title = T(title_text, size=28, color=TEXT).move_to([center_x, y1 + 0.72, 0])
    unit = T(unit_text, size=22, color=TEXT).move_to([center_x, y1 + 0.32, 0])

    def mk_needle():
        vy = y_of(val_tracker.get_value())
        return Polygon(
            [bar_x + 0.04, vy, 0], [bar_x + 0.32, vy + 0.11, 0], [bar_x + 0.32, vy - 0.11, 0],
            color=TEXT, fill_color=TEXT, fill_opacity=1.0, stroke_width=1.5
        )

    def mk_readout():
        return M(fmt.format(val_tracker.get_value()), size=32, color=TEXT).move_to([center_x, y0 - 0.54, 0])

    needle = always_redraw(mk_needle) if live else mk_needle()
    readout = (always_redraw(mk_readout) if live else mk_readout()) if show_readout else VGroup()

    g = VGroup(scale_line, tick_group, band_group, title, unit, needle, readout)
    g.y_of = y_of
    g.title = title
    g.unit = unit
    g.readout = readout
    g.bar_x = bar_x
    return g


def build_pumps_on_membrane():
    """Return 3 RED pumps evenly spaced along the dashed tank membrane."""
    return VGroup(*[build_pump_icon([MEMB_X, py, 0], color=RED, scale=0.95) for py in (0.65, -0.30, -1.25)])


def _make_flowing_dots(n, path_fn, color, radius=0.065, speed_tracker=None, base_speed=0.25, seed=11):
    """Particles moving smoothly along a parametric path path_fn(u in [0,1])."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        u0 = (i / n + rng.uniform(-0.02, 0.02)) % 1.0
        d = Dot(path_fn(u0), radius=radius, color=color)
        d._u = u0
        g.add(d)

    def upd(grp, dt):
        if dt <= 0:
            return
        sp = speed_tracker.get_value() if speed_tracker is not None else base_speed
        for d in grp:
            d._u = (d._u + sp * dt) % 1.0
            d.move_to(path_fn(d._u))

    g.add_updater(upd)
    return g


# ==============================================================================
# SCENE 00: Link and Question (spoken, 16.4s)
# ==============================================================================
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        world = build_tank_world(show_tap=True)
        na_val = ValueTracker(140.0)
        gauge = build_gauge(na_val, title_text="plasma sodium", scale_range=(130.0, 150.0),
                            ticks=(130, 140, 150), fmt="{:.0f}", show_band=False, live=False, show_readout=False)

        avoid_c = [(-4.2, -2.4, 1.10, 1.65)]
        avoid_o = [(0.0, 1.85, 1.10, 1.65)]
        na_out = make_ion_swarm(26, (MEMB_X + 0.08, TANK_X1 - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                                GOLD, radius=0.068, seed=101, speed=0.60, opacity=0.95, avoid_boxes=avoid_o)
        na_in = make_ion_swarm(4, (TANK_X0 + 0.08, MEMB_X - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                               GOLD, radius=0.068, seed=102, speed=0.60, opacity=0.95, avoid_boxes=avoid_c)
        k_in = make_ion_swarm(60, (TANK_X0 + 0.08, MEMB_X - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                              PURPLE, radius=0.068, seed=103, speed=0.58, opacity=0.30, avoid_boxes=avoid_c)
        k_out = make_ion_swarm(5, (MEMB_X + 0.08, TANK_X1 - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                               PURPLE, radius=0.068, seed=104, speed=0.58, opacity=0.30, avoid_boxes=avoid_o)

        self.add(world, gauge, na_out, na_in, k_in, k_out, scope_tag("schematic"))

        # First sentence: ghost 1 L water pours from tap and spreads through BOTH compartments
        spread = ValueTracker(0.0)
        ghost_pour = always_redraw(lambda: Rectangle(
            width=0.22, height=max(0.02, min(1.0, spread.get_value() * 3.0) * 0.7),
            stroke_width=0, fill_color=BLUE, fill_opacity=0.45
        ).move_to([world.tap_x, TANK_Y1 - 0.35 * min(1.0, spread.get_value() * 3.0), 0]))
        ghost_pool = always_redraw(lambda: Rectangle(
            width=max(0.05, (TANK_X1 - MEMB_X) + spread.get_value() * (MEMB_X - TANK_X0)),
            height=0.55 + 0.35 * spread.get_value(),
            stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.22
        ).move_to([
            TANK_X1 - 0.5 * ((TANK_X1 - MEMB_X) + spread.get_value() * (MEMB_X - TANK_X0)),
            TANK_Y0 + 0.35 + 0.15 * spread.get_value(), 0
        ]))
        last_tag = T("last time", size=26, color=BLUE).move_to([-4.7, 2.15, 0])

        self.at("water spread")
        self.add(ghost_pour, ghost_pool)
        self.play(FadeIn(last_tag), spread.animate.set_value(1.0), run_time=2.3, rate_func=smooth)

        # Highlight plasma sodium readout on "plasma sodium"
        self.at("plasma sodium")
        na_ring = Circle(radius=0.30, color=GOLD, stroke_width=3
                         ).move_to([gauge.bar_x + 0.18, gauge.y_of(140.0), 0])
        self.play(Create(na_ring), run_time=0.8)

        # Transition to potassium
        self.at("potassium")
        self.play(
            FadeOut(ghost_pour), FadeOut(ghost_pool), FadeOut(last_tag), FadeOut(na_ring),
            na_out.animate.set_opacity(0.18), na_in.animate.set_opacity(0.18),
            k_in.animate.set_opacity(1.0), k_out.animate.set_opacity(1.0),
            run_time=1.0
        )

        # Highlight cells compartment
        self.at("inside cells")
        cells_glow = Rectangle(width=MEMB_X - TANK_X0 - 0.08, height=TANK_Y1 - TANK_Y0 - 0.06,
                               stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.10
                               ).move_to([(TANK_X0 + MEMB_X - 0.04) / 2, (TANK_Y0 + TANK_Y1) / 2, 0])
        self.play(FadeIn(cells_glow), run_time=0.8)

        # Question + gauge morph to plasma potassium 3..6 at 4.2 (sequential fade avoids motion overlap)
        self.at("what guards")
        k_val = ValueTracker(4.2)
        new_gauge = build_gauge(k_val, title_text="plasma potassium", scale_range=(3.0, 6.0),
                                ticks=(3, 4, 5, 6), fmt="{:.1f}", show_band=False, live=False)
        q_text = T("What guards the potassium outside?", size=34, color=TEXT).move_to([-1.9, 2.85, 0])
        self.play(FadeOut(cells_glow), FadeOut(gauge), run_time=0.4)
        self.remove(gauge)
        self.play(FadeIn(new_gauge), FadeIn(q_text, shift=DOWN * 0.1), run_time=0.65)
        self.finish()


# ==============================================================================
# SCENE 01: Title Card (2.0s silent)
# ==============================================================================
class S01Title(TitleCard):
    LESSON = "Water, Sodium and Potassium Balance"
    TITLE = "Potassium on Two Clocks"


# ==============================================================================
# SCENE 02: Body Potassium Pool (18.95s)
# ==============================================================================
class S02Pool(SpokenScene):
    def construct(self):
        world = build_tank_world(show_muscle_stripes=False, cells_label="cells", show_tap=True)
        k_val = ValueTracker(4.2)
        gauge = build_gauge(k_val, title_text="plasma potassium", scale_range=(3.0, 6.0),
                            ticks=(3, 4, 5, 6), fmt="{:.1f}", show_band=True, live=False)

        avoid_c = [(-4.5, -2.1, 0.25, 1.65)]
        avoid_o = [(0.0, 1.85, 1.10, 1.65)]
        k_in = make_ion_swarm(65, (TANK_X0 + 0.08, MEMB_X - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                              PURPLE, radius=0.070, seed=201, speed=0.60, avoid_boxes=avoid_c)
        k_out = make_ion_swarm(5, (MEMB_X + 0.08, TANK_X1 - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                               PURPLE, radius=0.070, seed=202, speed=0.60, avoid_boxes=avoid_o)
        self.add(world, gauge, k_in, k_out, scope_tag("schematic"))

        # 98% inside
        self.at("98")
        lbl_98 = boxed_label("98% inside", color=TEXT, size=30, pad=0.14, fill_opacity=0.0).move_to([-3.3, 0.66, 0])
        lbl_98.box.set_fill(BG, opacity=0.88).set_stroke(PURPLE, width=2)
        self.play(FadeIn(lbl_98), run_time=0.8)

        # Skeletal muscle stripes + relabel
        self.at("skeletal muscle")
        stripes = VGroup()
        for sy in (0.12, -0.45, -1.02, -1.58):
            ln = Line([TANK_X0 + 0.25, sy, 0], [MEMB_X - 0.25, sy, 0],
                      color=PURPLE, stroke_width=1.8, stroke_opacity=0.24)
            stripes.add(ln)
        new_cells_lbl = T("cells, mostly muscle", size=28, color=TEXT).move_to(world.lbl_cells.get_center())
        self.play(Create(stripes), swap(world.lbl_cells, new_cells_lbl, run_time=0.8), run_time=1.0)

        # Outside: 14 L and highlight 4.2 on gauge (roomy RoundedRectangle so no overflow or near tick)
        self.at("14 liters")
        vol_lbl = M("14 L", size=30, color=TEXT).move_to([-2.3, -2.75, 0])
        glow_42 = RoundedRectangle(corner_radius=0.12, width=1.15, height=0.54, color=GOLD, stroke_width=3
                                   ).move_to(gauge.readout.get_center())
        self.play(FadeIn(vol_lbl), Create(glow_42), run_time=0.8)

        # 14 L x 4.2 = about 59 mEq (centered well left of collecting duct)
        self.at("about 59")
        sum_lbl = M("14 L × 4.2 = about 59 mEq", size=28, color=TEXT).move_to([-2.45, -2.75, 0])
        self.play(FadeOut(glow_42), swap(vol_lbl, sum_lbl, run_time=0.7), run_time=0.9)

        # 3,500 mEq bar along top with computed 1.7% PURPLE sliver
        self.at("1")
        bar_w = 8.1
        bar_x0, bar_x1, bar_y = -6.0, -6.0 + bar_w, 2.66
        sliver_w = (59.0 / 3500.0) * bar_w
        frac = ValueTracker(0.0)
        full_bar = always_redraw(lambda: Rectangle(
            width=max(0.02, frac.get_value() * bar_w), height=0.26,
            stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.22
        ).move_to([bar_x0 + 0.5 * max(0.02, frac.get_value() * bar_w), bar_y, 0]))
        bar_lbl = T("about 3,500 mEq", size=28, color=TEXT).move_to([-3.3, 3.20, 0])
        self.add(full_bar)
        self.play(frac.animate.set_value(1.0), FadeIn(bar_lbl), run_time=1.3)

        sliver = Rectangle(width=sliver_w, height=0.26, stroke_color=PURPLE, stroke_width=2,
                           fill_color=PURPLE, fill_opacity=1.0).move_to([bar_x1 - sliver_w / 2, bar_y, 0])
        out_pct = T("outside: 1.7%", size=26, color=PURPLE).move_to([0.72, 3.20, 0])
        ptr = Arrow(out_pct.get_right() + RIGHT * 0.08 + DOWN * 0.06, sliver.get_top() + UP * 0.05,
                    buff=0.04, color=PURPLE, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        self.play(FadeIn(sliver), FadeIn(out_pct), GrowArrow(ptr), run_time=0.8)
        self.finish()


# ==============================================================================
# SCENE 03: Daily Intake Load vs Outside Pool (10.575s)
# ==============================================================================
class S03Load(SpokenScene):
    def construct(self):
        world = build_tank_world(show_muscle_stripes=True, cells_label="cells, mostly muscle",
                                 tap_label="food", show_tap=True)
        k_val = ValueTracker(4.2)
        gauge = build_gauge(k_val, title_text="plasma potassium", scale_range=(3.0, 6.0),
                            ticks=(3, 4, 5, 6), fmt="{:.1f}", show_band=True, live=False)

        avoid_c = [(-4.9, -1.7, 1.10, 1.65)]
        avoid_o = [(0.0, 1.85, 1.10, 1.65)]
        k_in = make_ion_swarm(65, (TANK_X0 + 0.08, MEMB_X - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                              PURPLE, radius=0.070, seed=301, speed=0.60, avoid_boxes=avoid_c)
        k_out = make_ion_swarm(5, (MEMB_X + 0.08, TANK_X1 - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                               PURPLE, radius=0.070, seed=302, speed=0.60, avoid_boxes=avoid_o)
        tap_dots = make_ion_swarm(10, (world.tap_x - 0.14, world.tap_x + 0.14, TANK_Y1 + 0.06, TANK_Y1 + 0.52),
                                  PURPLE, radius=0.045, seed=303, speed=0.35)
        self.add(world, gauge, k_in, k_out, tap_dots, scope_tag("schematic"))

        # Two horizontal PURPLE bars drawn to exact 59 : 70 scale
        self.at("intake")
        base_len = 2.8
        len_59 = base_len * (59.0 / 70.0)
        len_70 = base_len
        bx0 = -6.0
        bar_59 = Rectangle(width=len_59, height=0.28, stroke_color=PURPLE, stroke_width=2,
                           fill_color=PURPLE, fill_opacity=0.85).move_to([bx0 + len_59 / 2, 2.38, 0])
        lbl_59 = T("outside pool: about 59", size=26, color=PURPLE).next_to(bar_59, RIGHT, buff=0.2)

        grow70 = ValueTracker(0.05)
        bar_70 = always_redraw(lambda: Rectangle(
            width=max(0.04, grow70.get_value() * len_70), height=0.28,
            stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.95
        ).move_to([bx0 + 0.5 * max(0.04, grow70.get_value() * len_70), 3.00, 0]))
        lbl_70 = T("daily intake: about 70", size=26, color=PURPLE).move_to([bx0 + len_70 + 1.85, 3.00, 0])

        self.add(bar_70)
        self.play(
            FadeIn(bar_59), FadeIn(lbl_59),
            grow70.animate.set_value(1.0), FadeIn(lbl_70),
            run_time=1.3
        )

        # Highlight that 70 > 59 on "more than the whole pool"
        self.at("more than the whole pool")
        excess_mark = DashedLine([bx0 + len_59, 2.15, 0], [bx0 + len_59, 3.22, 0], color=TEXT, stroke_width=2.5)
        self.play(Create(excess_mark), run_time=0.8)

        # Muscle cell defense: membrane glows + 3 RED pumps appear; duct dims
        self.at("muscle cell")
        pumps = build_pumps_on_membrane()
        pump_lbl = T("sodium-potassium pump", size=26, color=RED).move_to([-2.5, -2.65, 0])
        pump_ptr = Arrow(pump_lbl.get_top() + UP * 0.04, pumps[2].get_bottom() + DOWN * 0.08,
                         buff=0.05, color=RED, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        memb_glow = Line([MEMB_X, TANK_Y1 - 0.04, 0], [MEMB_X, TANK_Y0 + 0.04, 0],
                         color=TEXT, stroke_width=7, stroke_opacity=0.55)
        self.play(FadeIn(memb_glow), FadeIn(pumps), FadeIn(pump_lbl), GrowArrow(pump_ptr), run_time=0.8)

        self.at("not the kidney")
        self.play(world.duct.animate.set_opacity(0.3), run_time=0.6)
        self.finish()


# ==============================================================================
# SCENE 04: Shift into Muscle via Insulin & Epinephrine (17.0s)
# ==============================================================================
class S04Shift(SpokenScene):
    def construct(self):
        world = build_tank_world(show_muscle_stripes=True, cells_label="cells, mostly muscle",
                                 tap_label="food", duct_opacity=0.3, show_tap=True)
        k_val = ValueTracker(4.2)
        # The needle and readout stay at 4.2 (script: schematic, inside the band; 4.2 is the only reading narrated).
        gauge = build_gauge(k_val, title_text="plasma potassium", scale_range=(3.0, 6.0),
                            ticks=(3, 4, 5, 6), fmt="{:.1f}", show_band=True, live=False)
        pumps = build_pumps_on_membrane()

        avoid_c = [(-4.9, -1.7, 1.10, 1.65)]
        # keep ions out of the zone where the receptor tags, tokens and their labels dock
        avoid_o = [(0.0, 1.85, 1.10, 1.65), (-0.45, 2.15, -0.98, 0.92)]
        k_in = make_ion_swarm(65, (TANK_X0 + 0.08, MEMB_X - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                              PURPLE, radius=0.070, seed=401, speed=0.60, avoid_boxes=avoid_c)
        k_out = make_ion_swarm(6, (MEMB_X + 0.08, TANK_X1 - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                               PURPLE, radius=0.070, seed=402, speed=0.60, avoid_boxes=avoid_o)
        tap_dots = make_ion_swarm(10, (world.tap_x - 0.14, world.tap_x + 0.14, TANK_Y1 + 0.06, TANK_Y1 + 0.52),
                                  PURPLE, radius=0.045, seed=403, speed=0.35)
        self.add(world, gauge, pumps, k_in, k_out, tap_dots, scope_tag("schematic"))

        # Pumps and the dots they carry are still until the narrator speaks of them.
        pump_rate = ValueTracker(0.0)
        for p in pumps:
            p.rotor_spoke.add_updater(lambda m, dt, r=pump_rate: m.rotate(-3.4 * r.get_value() * dt))

        # Dots leave each pump into the muscle (cells) side; drawn clear of the receptor tags beside the pumps.
        shift_dots = VGroup()
        for idx, py in enumerate((0.65, -0.30, -1.25)):
            shift_dots.add(_make_flowing_dots(
                4, lambda u, py=py: np.array([MEMB_X - 0.30 - u * 1.4, py, 0.0]),
                PURPLE, radius=0.065, speed_tracker=pump_rate, seed=410 + idx
            ))

        self.at("into muscle")
        self.add(shift_dots)
        self.play(pump_rate.animate.set_value(0.30), run_time=0.8)

        self.at("stimulating")
        self.play(pump_rate.animate.set_value(0.55), run_time=1.0)

        # Insulin tokens dock on the TEAL 'insulin receptor' tag beside the top pump (never on the pump itself).
        self.at("insulin acts")
        ins_rec = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.26,
                                   color=TEAL, fill_color=TEAL, fill_opacity=0.6).move_to([MEMB_X + 0.42, 0.65, 0])
        ins_rec_lbl = T("insulin receptor", size=24, color=TEAL).move_to([0.9, 0.20, 0]).align_to(ins_rec, LEFT)
        ins_tok = boxed_label("insulin", color=TEAL, size=24, pad=0.10).move_to([1.40, 0.65, 0])
        self.play(FadeIn(ins_rec), FadeIn(ins_rec_lbl), FadeIn(ins_tok), run_time=0.5)
        self.play(
            ins_tok.animate.next_to(ins_rec, RIGHT, buff=0.10),
            pump_rate.animate.set_value(0.75),
            run_time=1.0
        )

        # Epinephrine docks on the MAGENTA 'beta2' tag beside the middle pump.
        self.at("epinephrine acts")
        b2_rec = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.26,
                                  color=MAGENTA, fill_color=MAGENTA, fill_opacity=0.6).move_to([MEMB_X + 0.42, -0.30, 0])
        b2_lbl = T("beta2", size=24, color=MAGENTA).move_to([0.2, -0.76, 0]).align_to(b2_rec, LEFT)
        epi_tok = boxed_label("epinephrine", color=MAGENTA, size=24, pad=0.10).move_to([1.20, -0.30, 0])
        self.play(FadeIn(b2_rec), FadeIn(b2_lbl), FadeIn(epi_tok), run_time=0.5)
        self.play(
            epi_tok.animate.next_to(b2_rec, RIGHT, buff=0.10),
            pump_rate.animate.set_value(1.10),
            run_time=1.1
        )

        # Fast minutes clock by the pumps
        self.at("in minutes")
        clk = build_clock([-2.5, 2.55, 0], "minutes", radius=0.34, label_dir=RIGHT)
        self.play(FadeIn(clk), run_time=0.6)
        clk.spin(4.5)
        self.finish()


# ==============================================================================
# SCENE 05: The One Idea — Two Clocks (10.575s)
# ==============================================================================
class S05Idea(SpokenScene):
    def construct(self):
        world = build_tank_world(show_muscle_stripes=True, cells_label="cells, mostly muscle",
                                 duct_opacity=0.5, show_tap=True)
        k_val = ValueTracker(4.2)
        gauge = build_gauge(k_val, title_text="plasma potassium", scale_range=(3.0, 6.0),
                            ticks=(3, 4, 5, 6), fmt="{:.1f}", show_band=True, live=False)
        pumps = build_pumps_on_membrane()   # still until "shifting into cells"

        avoid_c = [(-4.9, -1.7, 1.10, 1.65), (-4.2, -1.0, -1.18, -0.40)]
        avoid_o = [(0.0, 1.85, 1.10, 1.65)]
        k_in = make_ion_swarm(65, (TANK_X0 + 0.08, MEMB_X - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                              PURPLE, radius=0.070, seed=501, speed=0.58, avoid_boxes=avoid_c)
        k_out = make_ion_swarm(6, (MEMB_X + 0.08, TANK_X1 - 0.08, TANK_Y0 + 0.08, TANK_Y1 - 0.50),
                               PURPLE, radius=0.070, seed=502, speed=0.58, avoid_boxes=avoid_o)
        clk_min = build_clock([-2.6, 2.55, 0], "minutes", radius=0.34, label_dir=RIGHT)

        shift_dots = _make_flowing_dots(
            5, lambda u: np.array([MEMB_X + 1.3 - u * 2.6, -0.30, 0.0]),
            PURPLE, radius=0.065, base_speed=0.55, seed=503
        )
        self.add(world, gauge, pumps, k_in, k_out, clk_min, scope_tag("schematic"))

        # First arm: into cells (minutes) — dark pill backing + avoid box keeps dots clear of letters
        self.at("shifting into cells")
        self.add(shift_dots)
        clk_min.spin(4.2)
        for p in pumps:
            p.rotor_spoke.add_updater(lambda m, dt: m.rotate(-2.8 * dt))
        arr_cells = Arrow([MEMB_X + 0.85, -0.30, 0], [MEMB_X - 1.15, -0.30, 0],
                          color=PURPLE, stroke_width=6, buff=0)
        lbl_first = boxed_label("first: into cells", color=PURPLE, size=26, pad=0.10, fill_opacity=0.0).move_to([-2.6, -0.82, 0])
        lbl_first.box.set_fill(BG, opacity=0.90).set_stroke(PURPLE, width=1.8)
        self.play(GrowArrow(arr_cells), FadeIn(lbl_first), run_time=0.8)

        # Second arm: into urine (hours)
        self.at("then the kidney")
        clk_hrs = build_clock([2.45, -2.95, 0], "hours", radius=0.34, label_dir=RIGHT)
        arr_urine = Arrow([world.duct_x, TANK_Y0 + 0.65, 0], [world.duct_x, TANK_Y0 - 0.65, 0],
                          color=PURPLE, stroke_width=6, buff=0)
        lbl_then = T("then: into urine", size=28, color=PURPLE).move_to([-0.2, -2.65, 0])
        urine_dots = _make_flowing_dots(
            4, lambda u: np.array([world.duct_x, TANK_Y0 + 0.6 - u * 1.3, 0.0]),
            PURPLE, radius=0.06, base_speed=0.25, seed=504
        )
        self.add(urine_dots)
        self.play(
            world.duct.animate.set_opacity(1.0),
            FadeIn(clk_hrs), GrowArrow(arr_urine), FadeIn(lbl_then),
            run_time=0.9
        )
        clk_hrs.spin(0.45)
        self.finish()


# ==============================================================================
# SCENE 06: Kidney Arm — Filtration vs Reabsorption vs Distal (19.925s)
# ==============================================================================
def build_top_world_compact(tx0=-6.0, tx1=1.8, ty0=0.55, ty1=3.10, mx=-0.8, label_size=24):
    """Compact tank built directly at target coordinates so labels stay >= 24 pt."""
    water = Rectangle(width=tx1 - tx0, height=ty1 - ty0, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.12).move_to([(tx0 + tx1) / 2, (ty0 + ty1) / 2, 0])
    box = RoundedRectangle(corner_radius=0.12, width=tx1 - tx0, height=ty1 - ty0,
                           stroke_color=TEXT, stroke_width=2.5, fill_opacity=0).move_to(water)
    memb = DashedLine([mx, ty1 - 0.04, 0], [mx, ty0 + 0.04, 0], color=TEXT, stroke_width=2.5, dash_length=0.12)
    lc = T("cells", size=label_size, color=TEXT).move_to([(tx0 + mx) / 2, ty1 - 0.28, 0])
    lo = T("outside cells", size=label_size, color=TEXT).move_to([(mx + tx1) / 2, ty1 - 0.28, 0])
    py1 = ty0 + (ty1 - ty0) * 0.56
    py2 = ty0 + (ty1 - ty0) * 0.24
    pumps = VGroup(*[build_pump_icon([mx, py, 0], color=RED, scale=0.72) for py in (py1, py2)])
    g = VGroup(water, box, memb, lc, lo, pumps)
    g.bounds = (tx0, tx1, ty0, ty1, mx)
    g.pumps = pumps
    return g


class S06Filter(SpokenScene):
    def construct(self):
        top_w = build_top_world_compact()
        tx0, tx1, ty0, ty1, mx = top_w.bounds
        k_val = ValueTracker(4.2)
        gauge = build_gauge(k_val, title_text="plasma K+", scale_range=(3.0, 6.0),
                            ticks=(3, 4, 5, 6), fmt="{:.1f}", show_band=True,
                            center_x=4.65, y0=0.85, y1=2.70, live=False)

        k_in = make_ion_swarm(45, (tx0 + 0.08, mx - 0.08, ty0 + 0.08, ty1 - 0.52),
                              PURPLE, radius=0.065, seed=601, speed=0.55)
        k_out = make_ion_swarm(4, (mx + 0.08, tx1 - 0.08, ty0 + 0.08, ty1 - 0.52),
                               PURPLE, radius=0.065, seed=602, speed=0.55)

        ny = -1.65
        tuft = Circle(radius=0.52, color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.22).move_to([-5.2, ny, 0])
        capsule = Arc(radius=0.72, start_angle=PI * 0.6, angle=PI * 0.8, arc_center=[-5.2, ny, 0],
                      color=TEXT, stroke_width=3)
        prox_loop = Rectangle(width=4.8, height=0.72, stroke_color=TEXT, stroke_width=2.5,
                              fill_color=BLUE, fill_opacity=0.16).move_to([-2.0, ny, 0])
        distal = Rectangle(width=3.2, height=0.72, stroke_color=TEXT, stroke_width=2.5,
                           fill_color=BLUE, fill_opacity=0.16).move_to([2.0, ny, 0])
        urine_out = Arrow([3.6, ny, 0], [4.55, ny, 0], color=BLUE, stroke_width=4, buff=0)

        lbl_filter = T("filter", size=26, color=TEXT).next_to(tuft, DOWN, buff=0.26)
        lbl_prox = T("proximal + loop", size=26, color=TEXT).next_to(prox_loop, DOWN, buff=0.22)
        lbl_dist = T("distal", size=26, color=TEXT).next_to(distal, DOWN, buff=0.22)
        lbl_urine = T("urine", size=26, color=TEXT).next_to(urine_out, RIGHT, buff=0.14)

        neph_flow = make_fluid_stream(12, -4.35, 3.55, ny, spread_y=0.20, base_speed=0.28, dash_len=0.35, seed=610)
        nephron = VGroup(tuft, capsule, prox_loop, distal, urine_out, lbl_filter, lbl_prox, lbl_dist, lbl_urine)
        self.add(top_w, gauge, k_in, k_out, nephron, neph_flow, scope_tag("schematic"))

        self.at("filter")
        self.play(Indicate(tuft, color=RED, scale_factor=1.08), run_time=0.8)

        # Dense stream entering at filter (~756/day)
        self.at("about 756")
        filt_dots = _make_flowing_dots(
            18, lambda u: np.array([-4.6 + u * 2.2, ny, 0.0]),
            PURPLE, radius=0.06, base_speed=0.48, seed=603
        )
        filt_lbl = T("filtered: about 756 a day", size=26, color=PURPLE).move_to([-3.9, -0.42, 0])
        self.add(filt_dots)
        self.play(FadeIn(filt_lbl), run_time=0.8)

        # Broad reabsorption arrow returning ~90% back up to outside cells
        self.at("take most of it back")
        reabs_arr = CurvedArrow([-1.2, ny + 0.40, 0], [0.5, ty0 - 0.06, 0], angle=-0.35,
                                color=PURPLE, stroke_width=8)
        reabs_dots = _make_flowing_dots(
            14, lambda u: reabs_arr.point_from_proportion(u),
            PURPLE, radius=0.06, base_speed=0.50, seed=604
        )
        self.add(reabs_dots)
        self.play(Create(reabs_arr), run_time=0.9)

        # Thin trickle (<10%: under 76) enters distal segment
        self.at("less than 10")
        distal_dots = _make_flowing_dots(
            3, lambda u: np.array([0.4 + u * 3.4, ny, 0.0]),
            PURPLE, radius=0.06, base_speed=0.28, seed=605
        )
        dist_lbl = T("under 10%", size=26, color=PURPLE).move_to([2.0, -0.42, 0])
        self.add(distal_dots)
        self.play(FadeIn(dist_lbl), run_time=0.8)
        self.finish()


# ==============================================================================
# SCENE 07: Distal Secretion — Principal & Intercalated Cells (18.925s)
# ==============================================================================
def build_distal_cells_stage(y_cell_bot=-0.85, y_cell_top=0.75, y_lumen_bot=-2.55,
                             romk_gap=0.38, bk_gap=0.0, show_top_tank=True):
    """Build zoomed distal tubule wall with off-center channels so K+ paths never cross labels."""
    g = VGroup()
    if show_top_tank:
        # Built directly at compact size; wider outside compartment keeps tap pour clear of "outside cells"
        top_w = build_top_world_compact(tx0=-5.4, tx1=1.2, ty0=1.70, ty1=3.35, mx=-1.6, label_size=24)
        g.add(top_w)
        g.top_w = top_w

    blood_lbl = T("blood", size=26, color=TEXT).move_to([-5.45, (y_cell_bot + y_cell_top) / 2 + 0.95, 0])
    g.add(blood_lbl)
    g.blood_lbl = blood_lbl

    # Cells: principal (-4.5..-0.3, center -2.4) & intercalated (0.3..4.5, center 2.4)
    p_box = RoundedRectangle(corner_radius=0.14, width=4.2, height=y_cell_top - y_cell_bot,
                             stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.85
                             ).move_to([-2.4, (y_cell_bot + y_cell_top) / 2, 0])
    i_box = RoundedRectangle(corner_radius=0.14, width=4.2, height=y_cell_top - y_cell_bot,
                             stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.85
                             ).move_to([2.4, (y_cell_bot + y_cell_top) / 2, 0])
    # Place cell names cleanly on LEFT side of each cell; channels & paths on RIGHT side (x = -1.05 and x = 3.75)
    p_lbl = T("principal cell", size=28, color=TEXT).move_to([-2.95, (y_cell_bot + y_cell_top) / 2 + 0.24, 0])
    i_lbl = T("intercalated cell", size=28, color=TEXT).move_to([1.85, (y_cell_bot + y_cell_top) / 2 + 0.24, 0])

    g.romk_x = -1.05
    g.bk_x = 3.75
    romk = Rectangle(width=max(0.14, romk_gap), height=0.22, stroke_color=PURPLE, stroke_width=2.5,
                     fill_color=PURPLE, fill_opacity=0.8).move_to([g.romk_x, y_cell_bot, 0])
    romk_lbl = T("ROMK", size=24, color=PURPLE).move_to([g.romk_x - 0.95, y_cell_bot + 0.34, 0])

    bk = Rectangle(width=max(0.14, bk_gap) if bk_gap > 0 else 0.14, height=0.22,
                   stroke_color=PURPLE, stroke_width=2.5,
                   fill_color=PURPLE, fill_opacity=0.8 if bk_gap > 0 else 0.15
                   ).move_to([g.bk_x, y_cell_bot, 0])
    bk_lbl = T("BK (flow)", size=24, color=PURPLE).move_to([g.bk_x - 1.10, y_cell_bot + 0.34, 0])

    lumen = Rectangle(width=11.6, height=y_cell_bot - y_lumen_bot - 0.15, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.18).move_to([0.0, (y_cell_bot + y_lumen_bot) / 2 - 0.05, 0])
    lumen_bot_line = Line([-5.8, y_lumen_bot, 0], [5.8, y_lumen_bot, 0], color=TEXT, stroke_width=3)
    lumen_lbl = T("tubular fluid", size=26, color=BLUE).move_to([-4.2, y_lumen_bot - 0.35, 0])
    urine_lbl = T("urine", size=26, color=TEXT).move_to([5.4, (y_cell_bot + y_lumen_bot) / 2, 0])

    g.add(lumen, lumen_bot_line, p_box, i_box, p_lbl, i_lbl, romk, romk_lbl, bk, bk_lbl, lumen_lbl, urine_lbl)
    g.p_box, g.i_box = p_box, i_box
    g.romk, g.romk_lbl = romk, romk_lbl
    g.bk, g.bk_lbl = bk, bk_lbl
    g.lumen = lumen
    return g


class S07Secrete(SpokenScene):
    def construct(self):
        stage = build_distal_cells_stage(romk_gap=0.45, bk_gap=0.48, show_top_tank=True)
        stage.remove(stage.romk, stage.romk_lbl, stage.bk, stage.bk_lbl)

        tx0, tx1, ty0, ty1, mx = stage.top_w.bounds
        k_in = make_ion_swarm(26, (tx0 + 0.08, mx - 0.08, ty0 + 0.08, ty1 - 0.48),
                              PURPLE, radius=0.055, seed=700, speed=0.55)
        k_out = make_ion_swarm(4, (mx + 0.08, tx1 - 0.08, ty0 + 0.08, ty1 - 0.48),
                               PURPLE, radius=0.055, seed=709, speed=0.55)

        flow_sp = ValueTracker(0.24)
        lumen_y = -1.70
        fluid_streaks = make_fluid_stream(12, -5.6, 4.9, lumen_y, spread_y=0.48, speed_tracker=flow_sp,
                                          dash_len=0.42, seed=701)
        fluid_dots = _make_flowing_dots(
            12, lambda u: np.array([-5.6 + u * 10.6, lumen_y, 0.0]),
            BLUE, radius=0.058, speed_tracker=flow_sp, seed=702
        )

        tap_x, tap_y = tx1 - 0.30, ty1 + 0.22
        food_tap = VGroup(
            Rectangle(width=0.30, height=0.42, stroke_color=TEXT, stroke_width=2,
                      fill_color=BLUE, fill_opacity=0.2).move_to([tap_x, tap_y, 0]),
            T("food", size=24, color=TEXT).move_to([tap_x + 0.62, tap_y, 0])
        )
        tap_pour = _make_flowing_dots(
            5, lambda u: np.array([tap_x, tap_y + 0.15 - u * 0.85, 0.0]),
            PURPLE, radius=0.05, base_speed=0.55, seed=703
        )
        urine_stream = _make_flowing_dots(
            6, lambda u: np.array([2.5 + u * 2.1, lumen_y, 0.0]),
            PURPLE, radius=0.06, speed_tracker=flow_sp, seed=704
        )
        self.add(stage, k_in, k_out, fluid_streaks, fluid_dots, urine_stream, scope_tag("schematic"))

        # Follows intake: food tap pours and urine stream thickens
        self.at("follows intake")
        self.add(tap_pour)
        self.play(FadeIn(food_tap), flow_sp.animate.set_value(0.38), run_time=0.9)

        # Secreted from blood into cells and out into lumen along channel x = stage.romk_x
        self.at("is secreted")
        sec_path = _make_flowing_dots(
            6, lambda u: np.array([stage.romk_x, 1.35 - u * 2.85, 0.0]),
            PURPLE, radius=0.06, base_speed=0.42, seed=705
        )
        self.add(sec_path)
        self.wait(0.8)

        # Principal cells: RED pump on blood side + ROMK door on tubule side
        self.at("principal cells")
        p_pump = build_pump_icon([stage.romk_x, 0.75, 0], color=RED, scale=0.85)
        p_pump.rotor_spoke.add_updater(lambda m, dt: m.rotate(-3.2 * dt))
        self.play(FadeIn(p_pump), FadeIn(stage.romk), FadeIn(stage.romk_lbl), run_time=0.9)

        # High flow: fluid speeds up + BK (flow) opens on intercalated cell
        self.at("at high flow")
        bk_path = _make_flowing_dots(
            6, lambda u: np.array([stage.bk_x, 1.35 - u * 2.85, 0.0]),
            PURPLE, radius=0.06, base_speed=0.55, seed=706
        )
        self.add(bk_path)
        self.play(
            flow_sp.animate.set_value(0.78),
            FadeIn(stage.bk), FadeIn(stage.bk_lbl),
            run_time=0.9
        )
        self.finish()


# ==============================================================================
# SCENE 08: Two Major Influences — Aldosterone & Delivery (11.05s)
# ==============================================================================
def build_schematic_dial(tracker, center, label, color, radius=0.72):
    """Half-circle schematic dial with NO numbers (per script s08 visual note)."""
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=8)
    val = always_redraw(lambda: Arc(
        radius=radius, start_angle=PI, angle=-PI * float(np.clip(tracker.get_value(), 0.02, 1.0)),
        arc_center=c, stroke_color=color, stroke_width=8
    ))
    needle = always_redraw(lambda: Line(
        c, c + 0.82 * radius * np.array([
            np.cos(PI - PI * float(np.clip(tracker.get_value(), 0.02, 1.0))),
            np.sin(PI - PI * float(np.clip(tracker.get_value(), 0.02, 1.0))), 0.0
        ]), color=TEXT, stroke_width=4
    ))
    hub = Dot(c, radius=0.06, color=TEXT)
    lab = T(label, size=26, color=color).next_to(track, DOWN, buff=0.16)
    return VGroup(track, val, needle, hub, lab)


class S08Rate(SpokenScene):
    def construct(self):
        stage = build_distal_cells_stage(romk_gap=0.35, bk_gap=0.35, show_top_tank=False)
        stage.blood_lbl.move_to([-5.55, 0.25, 0])  # safely left of cells and aldosterone token
        p_pump = build_pump_icon([stage.romk_x, 0.75, 0], color=RED, scale=0.85)   # still: s08 does not speak of the pump

        aldo_v = ValueTracker(0.25)
        deliv_v = ValueTracker(0.25)
        d_aldo = build_schematic_dial(aldo_v, [-2.4, 2.35, 0], "aldosterone", ORANGE, radius=0.72)
        d_deliv = build_schematic_dial(deliv_v, [2.4, 2.35, 0], "delivery", BLUE, radius=0.72)

        flow_sp = ValueTracker(0.28)
        fluid_streaks = make_fluid_stream(12, -5.6, 4.9, -1.70, spread_y=0.45, speed_tracker=flow_sp,
                                          dash_len=0.42, seed=800)
        na_dots = _make_flowing_dots(
            10, lambda u: np.array([-5.6 + u * 10.6, -1.55, 0.0]),
            GOLD, radius=0.06, speed_tracker=flow_sp, seed=801
        )
        k_romk = _make_flowing_dots(
            5, lambda u: np.array([stage.romk_x, 0.65 - u * 2.15, 0.0]),
            PURPLE, radius=0.06, speed_tracker=flow_sp, seed=802
        )
        k_bk = _make_flowing_dots(
            5, lambda u: np.array([stage.bk_x, 0.65 - u * 2.15, 0.0]),
            PURPLE, radius=0.06, speed_tracker=flow_sp, seed=803
        )
        self.add(stage, p_pump, d_aldo, d_deliv, fluid_streaks, na_dots, k_romk, k_bk, scope_tag("schematic"))

        # Aldosterone docks cleanly on top-left of principal cell, far from blood label and pump
        self.at("aldosterone")
        aldo_tok = boxed_label("aldosterone", color=ORANGE, size=24, pad=0.14).move_to([-4.6, 1.32, 0])
        self.play(FadeIn(aldo_tok), run_time=0.4)
        self.play(
            aldo_tok.animate.move_to([-3.25, 1.12, 0]),
            aldo_v.animate.set_value(0.85),
            stage.romk.animate.stretch_to_fit_width(0.75),
            run_time=1.0
        )

        # Sodium and water delivered from upstream (label above lumen so fluid streaks never cross it)
        self.at("sodium and water delivered")
        deliv_lbl = T("delivery", size=26, color=BLUE).move_to([-5.30, -0.58, 0])
        deliv_arr = Arrow([-5.30, -0.78, 0], [-5.30, -1.25, 0], color=BLUE, stroke_width=3.5, buff=0)
        self.play(
            deliv_v.animate.set_value(0.65),
            FadeIn(deliv_lbl), GrowArrow(deliv_arr),
            flow_sp.animate.set_value(0.50),
            run_time=1.0
        )

        # Higher flow accelerates secretion
        self.at("higher flow")
        self.play(
            deliv_v.animate.set_value(0.95),
            flow_sp.animate.set_value(0.95),
            stage.bk.animate.stretch_to_fit_width(0.70),
            run_time=1.0
        )
        self.finish()


# ==============================================================================
# SCENE 09 & 10: Predict + Pause (10.7s + 4.5s silent)
# ==============================================================================
def build_lane(y_center, label_text, flow_speed=0.20, fluid_h=0.52, romk_w=0.34, bk_w=0.34,
               bob_only=True, fluid_opacity=0.22, seed=900):
    """Build one compact distal-segment lane with clean spacing and zero pill/label collisions."""
    g = VGroup()
    yc = y_center
    lbl = T(label_text, size=24, color=TEXT, line_spacing=0.85).move_to([-5.15, yc + 0.15, 0])

    # Principal (-2.35) & Intercalated (+0.85) cells (width 2.95 > tw+1.2 so layout_check treats them as cells)
    px, ix = -2.35, 0.85
    p_box = RoundedRectangle(corner_radius=0.10, width=2.95, height=0.96, stroke_color=TEXT, stroke_width=2.5,
                             fill_color=BG, fill_opacity=0.85).move_to([px, yc + 0.48, 0])
    i_box = RoundedRectangle(corner_radius=0.10, width=2.95, height=0.96, stroke_color=TEXT, stroke_width=2.5,
                             fill_color=BG, fill_opacity=0.85).move_to([ix, yc + 0.48, 0])
    p_lbl = T("principal", size=24, color=TEXT).move_to([px - 0.15, yc + 0.72, 0])
    i_lbl = T("intercalated", size=24, color=TEXT).move_to([ix - 0.10, yc + 0.72, 0])

    romk_x, bk_x = px + 0.80, ix + 0.80
    romk = Rectangle(width=romk_w, height=0.16, stroke_color=PURPLE, stroke_width=2,
                     fill_color=PURPLE, fill_opacity=0.8).move_to([romk_x, yc + 0.02, 0])
    bk = Rectangle(width=bk_w, height=0.16, stroke_color=PURPLE, stroke_width=2,
                   fill_color=PURPLE, fill_opacity=0.8).move_to([bk_x, yc + 0.02, 0])
    romk_t = T("ROMK", size=22, color=PURPLE).move_to([px - 0.35, yc + 0.25, 0])
    bk_t = T("BK", size=22, color=PURPLE).move_to([ix - 0.35, yc + 0.25, 0])

    lumen = Rectangle(width=6.2, height=fluid_h, stroke_width=0,
                      fill_color=BLUE, fill_opacity=fluid_opacity).move_to([-0.75, yc - 0.36, 0])
    lumen_bot = Line([-3.85, yc - 0.68, 0], [2.35, yc - 0.68, 0], color=TEXT, stroke_width=2.5)

    aldo = boxed_label("aldosterone: high", color=ORANGE, size=22, pad=0.11).move_to([px - 0.15, yc + 1.34, 0])

    sp_tr = ValueTracker(flow_speed)
    fluid_streaks = make_fluid_stream(6, -3.55, 2.22, yc - 0.36, spread_y=max(0.04, fluid_h * 0.28),
                                      speed_tracker=sp_tr, dash_len=0.30, seed=seed + 1)
    fluid_dots = _make_flowing_dots(
        7, lambda u, yc=yc: np.array([-3.5 + u * 5.6, yc - 0.36, 0.0]),
        GOLD, radius=0.052, speed_tracker=sp_tr, seed=seed
    )

    k_dots = VGroup()
    if bob_only:
        for i, kx in enumerate((romk_x, bk_x)):
            kd = Dot([kx, yc - 0.08, 0], radius=0.06, color=PURPLE)   # held still: no bobbing
            k_dots.add(kd)
    else:
        kd1 = _make_flowing_dots(4, lambda u, yc=yc, rx=romk_x: np.array([rx, yc + 0.25 - u * 0.72, 0.0]),
                                 PURPLE, radius=0.056, speed_tracker=sp_tr, seed=seed + 10)
        kd2 = _make_flowing_dots(4, lambda u, yc=yc, bx=bk_x: np.array([bx, yc + 0.25 - u * 0.72, 0.0]),
                                 PURPLE, radius=0.056, speed_tracker=sp_tr, seed=seed + 20)
        k_dots.add(kd1, kd2)

    g.add(lumen, lumen_bot, p_box, i_box, p_lbl, i_lbl, romk, bk, romk_t, bk_t, lbl, aldo,
          fluid_streaks, fluid_dots, k_dots)
    g.lbl, g.aldo, g.romk, g.bk, g.lumen = lbl, aldo, romk, bk, lumen
    g.sp_tr, g.fluid_dots, g.k_dots = sp_tr, fluid_dots, k_dots
    g.px, g.ix, g.romk_x, g.bk_x = px, ix, romk_x, bk_x
    return g


def build_mini_tank_icon():
    """Small carried tank icon at top left for s09/s10."""
    box = RoundedRectangle(corner_radius=0.08, width=1.4, height=0.72, stroke_color=TEXT, stroke_width=2,
                           fill_color=BLUE, fill_opacity=0.14).move_to([-5.4, 3.05, 0])
    memb = DashedLine([-5.25, 3.39, 0], [-5.25, 2.71, 0], color=TEXT, stroke_width=2, dash_length=0.08)
    dots = VGroup(*[Dot([-5.85 + 0.14 * (i % 4), 2.86 + 0.18 * (i // 4), 0], radius=0.035, color=PURPLE)
                    for i in range(8)])
    return VGroup(box, memb, dots)


def build_predict_backdrop():
    """Exact two-lane backdrop shared by S09Predict (final state) and S10Pause."""
    tank_icon = build_mini_tank_icon()
    top_lane = build_lane(1.02, "after volume\nloss", flow_speed=0.22, bob_only=True, seed=910)
    bot_lane = build_lane(-1.72, "high plasma\npotassium", flow_speed=0.22, bob_only=True, seed=920)
    sep = DashedLine([-6.0, -0.05, 0], [3.2, -0.05, 0], color=GREY, stroke_width=1.5, dash_length=0.16)
    return VGroup(tank_icon, top_lane, bot_lane, sep)


def lane_ring(yc, color):
    """Outline that marks the lane the narrator is naming (put on and taken off on the spoken words)."""
    return RoundedRectangle(corner_radius=0.10, width=6.65, height=2.42, stroke_color=color, stroke_width=2.5,
                            fill_opacity=0).move_to([-0.775, yc + 0.41, 0])


class S09Predict(SpokenScene):
    def construct(self):
        tank_icon = build_mini_tank_icon()
        top_lane = build_lane(1.02, "after volume\nloss", flow_speed=0.22, bob_only=True, seed=910)
        bot_lane = build_lane(-1.72, "high plasma\npotassium", flow_speed=0.22, bob_only=True, seed=920)
        sep = DashedLine([-6.0, -0.05, 0], [3.2, -0.05, 0], color=GREY, stroke_width=1.5, dash_length=0.16)
        top_aldo, bot_aldo = top_lane.aldo, bot_lane.aldo
        top_lane.remove(top_aldo)
        bot_lane.remove(bot_aldo)
        self.add(tank_icon, top_lane, bot_lane, sep, scope_tag("schematic"))

        # FadeIn (never set_opacity(0)->set_opacity(1) on boxed_label!)
        self.at("two states")
        self.play(FadeIn(top_aldo), FadeIn(bot_aldo), run_time=0.8)

        # the lane being named is outlined while it is named (no pulsing, no scaling)
        top_ring, bot_ring = lane_ring(1.02, GOLD), lane_ring(-1.72, PURPLE)
        self.at("after a volume loss")
        self.add(top_ring)
        self.wait(0.1)

        self.at("when plasma potassium")
        self.remove(top_ring)
        self.add(bot_ring)
        self.wait(0.1)

        self.at("in which")
        self.remove(bot_ring)
        qc = question_card("Which lane secretes more potassium?", y=3.05, color=TEXT, size=32, left=-4.2, max_w=9.4)
        self.play(FadeIn(qc.question), run_time=0.7)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Which lane secretes more potassium?"
    CARD = {"y": 3.05, "color": TEXT, "size": 32, "left": -4.2, "max_w": 9.4}
    RING_AT = (5.8, 3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_backdrop()


# ==============================================================================
# SCENE 11: The Answer — Delivery and Angiotensin II (20.2s)
# ==============================================================================
class S11Answer(SpokenScene):
    def construct(self):
        tank_icon = build_mini_tank_icon()
        top_lane = build_lane(1.02, "after volume\nloss", flow_speed=0.20, bob_only=False, seed=1110)
        bot_lane = build_lane(-1.72, "high plasma\npotassium", flow_speed=0.20, bob_only=False, seed=1120)
        sep = DashedLine([-6.0, -0.05, 0], [3.2, -0.05, 0], color=GREY, stroke_width=1.5, dash_length=0.16)
        qc = question_card("Which lane secretes more potassium?", y=3.05, color=TEXT, size=32, left=-4.2, max_w=9.4)
        self.add(tank_icon, top_lane, bot_lane, sep, qc, scope_tag("schematic"))

        # Bottom lane first: delivery normal or higher
        self.at("when potassium is high")
        self.play(FadeOut(qc), run_time=0.5)

        self.at("delivery")
        deliv_ring = Rectangle(width=6.26, height=0.72, stroke_color=BLUE, stroke_width=2.5,
                               fill_opacity=0).move_to([-0.75, -1.72 - 0.36, 0])
        self.add(deliv_ring)
        bot_deliv_lbl = T("delivery: normal or higher", size=24, color=BLUE).move_to([-0.68, -2.79, 0])
        self.play(
            bot_lane.lumen.animate.stretch_to_fit_height(0.66).set_fill(BLUE, opacity=0.35),
            run_time=1.0
        )

        self.at("normal or higher")
        self.remove(deliv_ring)
        self.play(
            bot_lane.sp_tr.animate.set_value(0.68),
            FadeIn(bot_deliv_lbl),
            run_time=1.0
        )

        # Angiotensin II: not raised (faint outline, cleanly right of aldosterone: high)
        self.at("angiotensin")
        ang2_bot = boxed_label("angiotensin II: not raised", color=ORANGE, size=22, pad=0.11, fill_opacity=0.02)
        ang2_bot.box.set_stroke(ORANGE, width=1.8, opacity=0.65)
        ang2_bot.label.set_opacity(0.85)
        ang2_bot.move_to([1.35, -1.72 + 1.34, 0])
        ang_ring = SurroundingRectangle(ang2_bot, color=ORANGE, buff=0.07, corner_radius=0.16)
        self.add(ang_ring)
        self.play(FadeIn(ang2_bot), run_time=0.7)

        self.at("potassium itself")
        self.remove(ang_ring)
        bot_out_lbl = T("potassium\nexcreted", size=24, color=PURPLE, line_spacing=0.85).move_to([3.35, -1.72, 0])
        extra_k_bot = _make_flowing_dots(
            5, lambda u: np.array([bot_lane.romk_x, -0.60 - u * 1.48, 0.0]),
            PURPLE, radius=0.062, base_speed=0.75, seed=1130
        )
        self.add(extra_k_bot)
        self.play(
            bot_lane.romk.animate.stretch_to_fit_width(0.60),
            bot_lane.bk.animate.stretch_to_fit_width(0.60),
            bot_lane.sp_tr.animate.set_value(0.95),
            FadeIn(bot_out_lbl),
            run_time=1.0
        )

        # Top lane: delivery low, angiotensin II high restrains ROMK -> potassium kept
        self.at("after a volume loss")
        top_dim = RoundedRectangle(corner_radius=0.10, width=2.95, height=0.96, stroke_color=GOLD, stroke_width=2.5
                                   ).move_to([top_lane.px, 1.02 + 0.48, 0])
        self.add(top_dim)
        self.wait(0.1)

        self.at("delivery is low")
        self.remove(top_dim)
        top_deliv_lbl = T("delivery: low", size=24, color=BLUE).move_to([-5.15, 0.28, 0])
        self.play(
            top_lane.lumen.animate.stretch_to_fit_height(0.20).set_fill(BLUE, opacity=0.14),
            top_lane.sp_tr.animate.set_value(0.08),
            FadeIn(top_deliv_lbl),
            run_time=0.9
        )

        self.at("angiotensin", nth=1)
        ang2_top = boxed_label("angiotensin II: high", color=ORANGE, size=22, pad=0.11, fill_opacity=0.85)
        ang2_top.label.set_color(BG)
        ang2_top.move_to([1.35, 1.02 + 1.34, 0])
        top_out_lbl = T("potassium\nkept", size=24, color=PURPLE, line_spacing=0.85).move_to([3.35, 1.02, 0])
        self.play(FadeIn(ang2_top), run_time=0.7)

        self.at("restrains secretion")
        press_ring = RoundedRectangle(corner_radius=0.14, width=3.12, height=1.10, stroke_color=ORANGE, stroke_width=3
                                      ).move_to([top_lane.px, 1.02 + 0.48, 0])
        self.add(press_ring)
        self.play(
            top_lane.romk.animate.stretch_to_fit_width(0.14),
            top_lane.bk.animate.stretch_to_fit_width(0.12),
            FadeIn(top_out_lbl),
            run_time=1.6
        )
        self.remove(press_ring)
        self.finish()


# ==============================================================================
# SCENE 12: The Aldosterone Paradox (10.95s)
# ==============================================================================
class S12Paradox(SpokenScene):
    def construct(self):
        tank_icon = build_mini_tank_icon()
        top_lane = build_lane(1.02, "after volume\nloss", flow_speed=0.08, fluid_h=0.20,
                              romk_w=0.14, bk_w=0.12, bob_only=False, fluid_opacity=0.14, seed=1210)
        bot_lane = build_lane(-1.72, "high plasma\npotassium", flow_speed=0.90, fluid_h=0.66,
                              romk_w=0.60, bk_w=0.60, bob_only=False, fluid_opacity=0.35, seed=1220)
        sep = DashedLine([-6.0, -0.05, 0], [3.2, -0.05, 0], color=GREY, stroke_width=1.5, dash_length=0.16)

        top_deliv_lbl = T("delivery: low", size=24, color=BLUE).move_to([-5.15, 0.28, 0])
        bot_deliv_lbl = T("delivery: normal or higher", size=24, color=BLUE).move_to([-0.68, -2.79, 0])
        ang2_top = boxed_label("angiotensin II: high", color=ORANGE, size=22, pad=0.11, fill_opacity=0.85)
        ang2_top.label.set_color(BG)
        ang2_top.move_to([1.35, 1.02 + 1.34, 0])
        ang2_bot = boxed_label("angiotensin II: not raised", color=ORANGE, size=22, pad=0.11, fill_opacity=0.02)
        ang2_bot.box.set_stroke(ORANGE, width=1.8, opacity=0.65)
        ang2_bot.label.set_opacity(0.85)
        ang2_bot.move_to([1.35, -1.72 + 1.34, 0])
        top_out_lbl = T("potassium\nkept", size=24, color=PURPLE, line_spacing=0.85).move_to([3.35, 1.02, 0])
        bot_out_lbl = T("potassium\nexcreted", size=24, color=PURPLE, line_spacing=0.85).move_to([3.35, -1.72, 0])

        self.add(tank_icon, top_lane, bot_lane, sep, top_deliv_lbl, bot_deliv_lbl,
                 ang2_top, ang2_bot, top_out_lbl, bot_out_lbl, scope_tag("schematic"))

        # Aldosterone high in both
        self.at("high in both")
        r1 = SurroundingRectangle(top_lane.aldo, color=GOLD, buff=0.05, corner_radius=0.14)
        r2 = SurroundingRectangle(bot_lane.aldo, color=GOLD, buff=0.05, corner_radius=0.14)
        self.play(Create(r1), Create(r2), run_time=0.8)
        self.play(FadeOut(r1), FadeOut(r2), run_time=0.5)

        # What comes with it: delivery and angiotensin II
        self.at("what comes with it")
        d1 = SurroundingRectangle(top_deliv_lbl, color=BLUE, buff=0.14, corner_radius=0.10)
        d2 = SurroundingRectangle(bot_deliv_lbl, color=BLUE, buff=0.14, corner_radius=0.10)
        self.play(Create(d1), Create(d2), run_time=0.7)
        a1 = SurroundingRectangle(ang2_top, color=ORANGE, buff=0.05, corner_radius=0.14)
        a2 = SurroundingRectangle(ang2_bot, color=ORANGE, buff=0.05, corner_radius=0.14)
        self.play(FadeOut(d1), FadeOut(d2), Create(a1), Create(a2), run_time=0.8)
        self.play(FadeOut(a1), FadeOut(a2), run_time=0.5)

        # Aldosterone paradox bracket cleanly in right margin (no shifting needed)
        self.at("aldosterone paradox")
        bracket = Brace(VGroup(top_out_lbl, bot_out_lbl), direction=RIGHT, color=TEXT, buff=0.16)
        para_lbl = T("aldosterone\nparadox", size=26, color=TEXT, line_spacing=0.85).next_to(bracket, RIGHT, buff=0.14)
        self.play(Create(bracket), FadeIn(para_lbl), run_time=0.9)
        self.finish()


# ==============================================================================
# SCENE 13: Closing Synthesis — Two Lines of Defence on Two Clocks (14.55s)
# ==============================================================================
class S13Close(SpokenScene):
    def construct(self):
        top_w = build_top_world_compact(tx0=-6.0, tx1=2.0, ty0=0.55, ty1=3.10, mx=-0.8, label_size=24)
        tx0, tx1, ty0, ty1, mx = top_w.bounds
        k_val = ValueTracker(4.2)
        gauge = build_gauge(k_val, title_text="plasma K+", scale_range=(3.0, 6.0),
                            ticks=(3, 4, 5, 6), fmt="{:.1f}", show_band=True,
                            center_x=4.65, y0=-1.65, y1=1.45, live=False)

        k_in = make_ion_swarm(45, (tx0 + 0.08, mx - 0.08, ty0 + 0.08, ty1 - 0.52),
                              PURPLE, radius=0.065, seed=1301, speed=0.55)
        k_out = make_ion_swarm(5, (mx + 0.08, tx1 - 0.08, ty0 + 0.08, ty1 - 0.52),
                               PURPLE, radius=0.065, seed=1302, speed=0.55)

        # Place tap cleanly right of "outside cells" (centered at 0.6, right edge ~1.35)
        tap_x = 1.72
        food_tap = VGroup(
            Rectangle(width=0.32, height=0.42, stroke_color=TEXT, stroke_width=2,
                      fill_color=BLUE, fill_opacity=0.18).move_to([tap_x, ty1 + 0.21, 0]),
            T("food", size=24, color=TEXT).move_to([tap_x + 0.65, ty1 + 0.21, 0])
        )

        ny = -1.75
        tuft = Circle(radius=0.40, color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.22).move_to([-5.3, ny, 0])
        prox = Rectangle(width=3.6, height=0.62, stroke_color=TEXT, stroke_width=2.2,
                         fill_color=BLUE, fill_opacity=0.16).move_to([-2.9, ny, 0])
        distal = Rectangle(width=2.8, height=0.62, stroke_color=TEXT, stroke_width=2.2,
                           fill_color=BLUE, fill_opacity=0.16).move_to([0.3, ny, 0])
        urine_out = Arrow([1.7, ny, 0], [2.55, ny, 0], color=BLUE, stroke_width=4, buff=0)
        neph_lbls = VGroup(
            T("filter", size=24, color=TEXT).next_to(tuft, DOWN, buff=0.20),
            T("proximal + loop", size=24, color=TEXT).next_to(prox, DOWN, buff=0.20),
            T("distal", size=24, color=TEXT).next_to(distal, DOWN, buff=0.20),
            T("urine", size=24, color=TEXT).next_to(urine_out, RIGHT, buff=0.12),
        )
        neph_flow = make_fluid_stream(9, -4.6, 1.65, ny, spread_y=0.18, base_speed=0.28, dash_len=0.30, seed=1310)
        nephron = VGroup(tuft, prox, distal, urine_out, neph_lbls)

        clk_min = build_clock([-2.6, -0.05, 0], "minutes", radius=0.32, label_dir=RIGHT)
        clk_hrs = build_clock([0.3, -0.05, 0], "hours", radius=0.32, label_dir=RIGHT)

        self.add(top_w, food_tap, gauge, k_in, k_out, nephron, neph_flow, clk_min, clk_hrs, scope_tag("schematic"))

        # Within minutes: food tap pours, pumps spin, K+ into muscle, minutes clock sweeps fast
        # (the needle and readout stay at 4.2 throughout; nothing here starts before the narrator says it)
        self.at("within minutes")
        pump_sp = ValueTracker(1.2)
        for p in top_w.pumps:
            p.rotor_spoke.add_updater(lambda m, dt, s=pump_sp: m.rotate(-3.0 * s.get_value() * dt))
        pour_dots = _make_flowing_dots(
            5, lambda u: np.array([tap_x, ty1 + 0.35 - u * 1.15, 0.0]),
            PURPLE, radius=0.05, base_speed=0.55, seed=1303
        )
        shift_dots = _make_flowing_dots(
            5, lambda u: np.array([mx + 1.1 - u * 2.4, 1.55, 0.0]),
            PURPLE, radius=0.055, speed_tracker=pump_sp, seed=1304
        )
        self.add(pour_dots, shift_dots)
        clk_min.spin(4.5)
        self.wait(0.3)

        # Over hours: the minutes picture stops; K+ moves slowly down to distal and out with urine; hours clock sweeps slowly
        self.at("over hours")
        clk_min.spin(0)
        for p in top_w.pumps:
            p.rotor_spoke.clear_updaters()
        self.play(FadeOut(pour_dots), FadeOut(shift_dots), run_time=0.6)
        self.remove(pour_dots, shift_dots)
        renal_dots = _make_flowing_dots(
            5, lambda u: np.array([0.3 + u * 2.1, ny, 0.0]),
            PURPLE, radius=0.055, base_speed=0.25, seed=1305
        )
        down_dots = _make_flowing_dots(
            4, lambda u: np.array([0.25, ty0 - u * (ty0 - ny), 0.0]),
            PURPLE, radius=0.055, base_speed=0.24, seed=1306
        )
        self.add(renal_dots, down_dots)
        clk_hrs.spin(0.45)
        self.wait(0.3)

        # Aldosterone & delivery highlight
        self.at("steered by aldosterone")
        aldo_tok = boxed_label("aldosterone", color=ORANGE, size=22, pad=0.14).move_to([-1.35, -0.88, 0])
        deliv_lbl = T("delivery", size=24, color=BLUE).move_to([1.45, -0.88, 0])
        self.play(FadeIn(aldo_tok), FadeIn(deliv_lbl), run_time=0.8)
        self.finish()


# ==============================================================================
# SCENE 14: End Card (3.5s silent)
# ==============================================================================
class S14End(EndCard):
    LINE = "Potassium moves into cells in minutes; the kidney excretes it over hours."
