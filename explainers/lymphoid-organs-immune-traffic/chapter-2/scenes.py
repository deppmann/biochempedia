"""
One Node, or Every Node — Lymphoid Organs and Immune Traffic (Chapter 2)

COLOUR MAP (one colour per concept, kept for the whole film):
  YELLOW (#F5D547) : lymphocytes (traveling and counted cells)
  RED    (#FC6255) : blood (blood band, spleen artery, node entry arrows, blood share)
  BLUE   (#58C4DD) : lymph (efferent lymph return line)
  PURPLE (#B189F5) : entry machinery (high endothelial venule gate markers)
  TEAL   (#3FB8C0) : S1P / S1P1, the normal exit (exit arrows, exit dial)
  ORANGE (#F59E42) : exit slowed or blocked
  GREEN  (#83C167) : cells held (held bars, nodes' share of the pool)
  GREY   (#8B93A1) : organ blocks, axes, schematic tags, unlabelled spleen share
  TEXT   (#E8EAF0) : primary labels, question card, tracked-cell ring

THE ONE WORLD CARRIED THROUGH THE FILM:
  Left 62%: recirculation loop — thick RED blood band across top with streaming YELLOW cells,
  GREY spleen block at far left (RED artery in, TEAL exit back to blood), five GREY rounded
  node blocks in a row (RED entry arrows from blood, TEAL exit arrows into BLUE lymph line
  returning up to blood).
  Right 30%: GREEN/GREY/RED stacked bar 'where the pool sits', computed from the 3-compartment
  rat model (blood, spleen, subcutaneous nodes: S/B = 0.056/0.007 = 8.0, N/B = 2*0.026/0.0034 = 15.3).
  Zoomed scenes ease into the spleen or middle node of the same world.

WHAT CHANGES IN EACH SPOKEN SCENE (computed):
  s00_link_and_question : Recap on the loop — middle node exit halves (TEAL->ORANGE, 0.5x width)
                          and its GREEN held bar doubles (2x); then all five node exits thin
                          to 0.5x ORANGE together while circulating YELLOW dots keep moving.
  s02_chance_exit       : Zoomed spleen — tracked YELLOW dot executes a seeded random walk that
                          misses the exit; minute counter ticks as 0.7% of spleen dots flash and
                          leave per minute, holding at 0.7%/min when density triples (schematic).
  s03_entry_not_in_stay : Zoomed middle node — RED entry arrow oscillates while TEAL exit dial
                          stays fixed at 1.0x; equal-width streams of 1,000/h CD4 dots and
                          1,000/h CD8 rings enter and wander.
  s04_cd4_cd8           : Same node — horizontal stay bars grow to 12.2 h (CD4) and 21.2 h (CD8);
                          GREEN held bars rise to entry*stay = 12,200 and 21,200 (ratio 1.74x).
  s05_rule              : Full loop — middle exit/entry pulse with their rules; blood density
                          briefly drops to 0.35x and all RED entry arrows thin proportionally.
  s06_predict           : Full loop — blood segment highlights at 4.1%; all five node exits turn
                          ORANGE and thin to 0.5x (stay x2) while stacked bar waits unchanged.
  s08_answer            : Closed-pool outline closes; exit factor ramps 1.0->0.5 in the 3-compartment
                          model so blood thins to 0.61x (4.1%->2.5%), entry arrows thin to 0.61x,
                          spleen shifts 32.9%->20.2%, and nodes grow 63.0%->77.3% (held x1.23).
  s09_one_node          : Baseline loop extended with schematic row of distant nodes; only middle
                          exit halves (ORANGE), blood and stacked bar stay steady, middle GREEN
                          held bar rises to 2x.
  s10_why_hold          : Zoomed draining node — ringed rare matching YELLOW dot random-walks past
                          the central antigen star, finds it on a later pass (both glow), then
                          ORANGE exit widens back to TEAL and GREEN held bar settles toward 1x.
  s11_close             : Full loop — middle exit & blood pulse; single-node 2x held pulse resets;
                          all five exits thin ORANGE, blood thins 0.61x, stacked bar shifts to
                          2.5% / 20.2% / 77.3% (stay x2, held x1.23).
"""
from bp_parts import *

# ------------------------------------------------------------------ Film palette
PURPLE = "#B189F5"
ORANGE = "#F59E42"
ORGAN_FILL = "#141822"

# ------------------------------------------------------------------ Rat 3-compartment model
# Ganusov & Auerbach (2014): S/B = k_S / e_S = 0.056 / 0.007 = 8.0
# Subcutaneous nodes (2 series subcompartments): N/B = 2 * 0.026 / 0.0034 = 15.294 (15.3 in lesson)
K_SPLEEN, E_SPLEEN = 0.056, 0.007
K_NODE, E_NODE = 0.026, 0.0034
S_OVER_B = K_SPLEEN / E_SPLEEN                 # 8.0
N_OVER_B_BASE = round(2 * K_NODE / E_NODE, 1)  # 15.3


def pool_shares(node_exit_scale=1.0):
    """Return (blood_pct, spleen_pct, nodes_pct, blood_ratio) for node exit rate scaled by node_exit_scale."""
    n_over_b = N_OVER_B_BASE / max(node_exit_scale, 0.1)
    total = 1.0 + S_OVER_B + n_over_b
    base_total = 1.0 + S_OVER_B + N_OVER_B_BASE
    blood_ratio = base_total / total
    return 100.0 / total, 100.0 * S_OVER_B / total, 100.0 * n_over_b / total, blood_ratio


# ------------------------------------------------------------------ Loop geometry constants
BLOOD_X0, BLOOD_X1 = -5.7, 1.65
BLOOD_Y, BLOOD_H = 1.78, 0.46
SPLEEN_CENTER = np.array([-4.85, 0.0, 0.0])
SPLEEN_W, SPLEEN_H = 1.32, 1.36
NODE_XS = [-2.65, -1.70, -0.75, 0.20, 1.15]
NODE_Y = 0.0
NODE_W, NODE_H = 0.56, 1.06
LYMPH_Y = -1.42
LYMPH_UP_X = 1.75

BAR_X0, BAR_X1 = 3.25, 4.45
BAR_Y0, BAR_Y1 = -1.85, 2.05


def _make_arrow(start, end, color, stroke_width=6.0, tip_len=0.18):
    """Compact clean arrow whose shaft thickness can be read/updated cleanly."""
    return Arrow(
        start, end, buff=0, color=color,
        stroke_width=stroke_width, max_tip_length_to_length_ratio=0.38,
        tip_length=tip_len,
    )


class LymphTrafficSim:
    """Deterministic lymphocyte recirculation simulation across blood, spleen, 5 nodes, and lymph."""

    def __init__(self, seed=7, n_blood=30, n_spleen=18, n_per_node=11, n_lymph=12):
        self.rng = np.random.default_rng(seed)
        self.blood_density = 1.0
        self.node_exit_scales = [1.0] * 5  # 1.0 normal, 0.5 slowed

        # Blood particles: x in [BLOOD_X0, BLOOD_X1], y_off in [-0.14, 0.14], speed
        self.blood_pts = []
        for i in range(n_blood):
            self.blood_pts.append([
                self.rng.uniform(BLOOD_X0 + 0.1, BLOOD_X1 - 0.1),
                self.rng.uniform(-0.13, 0.13),
                self.rng.uniform(1.30, 1.85),
                i / max(n_blood - 1, 1),  # normalized rank for density thinning
            ])

        # Spleen particles: local (dx, dy, vx, vy) inside SPLEEN_W x SPLEEN_H
        self.spleen_pts = []
        for _ in range(n_spleen):
            self.spleen_pts.append([
                self.rng.uniform(-SPLEEN_W * 0.36, SPLEEN_W * 0.36),
                self.rng.uniform(-SPLEEN_H * 0.36, SPLEEN_H * 0.36),
                self.rng.uniform(-0.35, 0.35),
                self.rng.uniform(-0.35, 0.35),
            ])

        # Node particles: per node, list of [dx, dy, vx, vy, rank]
        self.node_pts = []
        for _ in range(5):
            pts = []
            for j in range(n_per_node):
                pts.append([
                    self.rng.uniform(-NODE_W * 0.30, NODE_W * 0.30),
                    self.rng.uniform(-NODE_H * 0.34, NODE_H * 0.34),
                    self.rng.uniform(-0.28, 0.28),
                    self.rng.uniform(-0.28, 0.28),
                    j / max(n_per_node - 1, 1),
                ])
            self.node_pts.append(pts)

        # Lymph particles: progress s in [0, 1] along horizontal lymph line + upward return
        self.lymph_pts = [self.rng.uniform(0.0, 1.0) for _ in range(n_lymph)]

    def step(self, dt):
        if dt <= 0:
            return
        dt = min(dt, 0.1)
        bw = BLOOD_X1 - BLOOD_X0
        for p in self.blood_pts:
            p[0] += p[2] * dt * (0.75 + 0.25 * self.blood_density)
            if p[0] > BLOOD_X1:
                p[0] -= bw

        hw, hh = SPLEEN_W * 0.38, SPLEEN_H * 0.38
        for p in self.spleen_pts:
            p[2] += self.rng.normal(0, 0.6) * dt
            p[3] += self.rng.normal(0, 0.6) * dt
            sp = np.hypot(p[2], p[3])
            if sp > 0.45:
                p[2] *= 0.45 / sp
                p[3] *= 0.45 / sp
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            if abs(p[0]) > hw:
                p[0] = np.sign(p[0]) * hw
                p[2] *= -1
            if abs(p[1]) > hh:
                p[1] = np.sign(p[1]) * hh
                p[3] *= -1

        nw, nh = NODE_W * 0.32, NODE_H * 0.36
        for idx, pts in enumerate(self.node_pts):
            sc = self.node_exit_scales[idx]
            vmax = 0.38 * (0.65 + 0.35 * sc)
            for p in pts:
                p[2] += self.rng.normal(0, 0.5) * dt
                p[3] += self.rng.normal(0, 0.5) * dt
                sp = np.hypot(p[2], p[3])
                if sp > vmax:
                    p[2] *= vmax / sp
                    p[3] *= vmax / sp
                p[0] += p[2] * dt
                p[1] += p[3] * dt
                if abs(p[0]) > nw:
                    p[0] = np.sign(p[0]) * nw
                    p[2] *= -1
                if abs(p[1]) > nh:
                    p[1] = np.sign(p[1]) * nh
                    p[3] *= -1

        for k in range(len(self.lymph_pts)):
            self.lymph_pts[k] = (self.lymph_pts[k] + 0.22 * dt) % 1.0


def build_world(sim, exit_factor_tracker=None, blood_density_tracker=None,
                node_scales=(1.0, 1.0, 1.0, 1.0, 1.0), show_labels=True,
                show_bar=True, dimmed=False):
    """Build the carried recirculation loop + stacked bar in identical coordinates across scenes."""
    world = VGroup()
    alpha = 0.22 if dimmed else 1.0
    if exit_factor_tracker is None:
        exit_factor_tracker = ValueTracker(1.0)
    if blood_density_tracker is None:
        blood_density_tracker = ValueTracker(1.0)

    # Blood band across top
    blood_band = RoundedRectangle(
        corner_radius=0.14, width=BLOOD_X1 - BLOOD_X0, height=BLOOD_H,
        stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.22 * alpha,
    ).move_to([(BLOOD_X0 + BLOOD_X1) / 2, BLOOD_Y, 0]).set_stroke(opacity=alpha)

    # Spleen block at far left
    spleen_box = RoundedRectangle(
        corner_radius=0.18, width=SPLEEN_W, height=SPLEEN_H,
        stroke_color=GREY, stroke_width=2.8, fill_color=GREY, fill_opacity=0.12 * alpha,
    ).move_to(SPLEEN_CENTER).set_stroke(opacity=alpha)

    spleen_in = _make_arrow(
        [SPLEEN_CENTER[0] - 0.24, BLOOD_Y - BLOOD_H / 2, 0],
        [SPLEEN_CENTER[0] - 0.24, SPLEEN_CENTER[1] + SPLEEN_H / 2 + 0.04, 0],
        RED, stroke_width=5.5,
    ).set_opacity(alpha)
    spleen_out = _make_arrow(
        [SPLEEN_CENTER[0] + 0.24, SPLEEN_CENTER[1] + SPLEEN_H / 2 + 0.04, 0],
        [SPLEEN_CENTER[0] + 0.24, BLOOD_Y - BLOOD_H / 2, 0],
        TEAL, stroke_width=5.5,
    ).set_opacity(alpha)

    # Five node blocks + dynamic entry/exit arrows
    node_boxes = VGroup()
    entry_arrows = VGroup()
    exit_arrows = VGroup()
    for i, nx in enumerate(NODE_XS):
        nb = RoundedRectangle(
            corner_radius=0.14, width=NODE_W, height=NODE_H,
            stroke_color=GREY, stroke_width=2.6, fill_color=GREY, fill_opacity=0.12 * alpha,
        ).move_to([nx, NODE_Y, 0]).set_stroke(opacity=alpha)
        node_boxes.add(nb)

        ea = _make_arrow(
            [nx, BLOOD_Y - BLOOD_H / 2, 0],
            [nx, NODE_Y + NODE_H / 2 + 0.04, 0],
            RED, stroke_width=6.0,
        ).set_opacity(alpha)
        entry_arrows.add(ea)

        sc = node_scales[i]
        ex_col = ORANGE if sc < 0.75 else TEAL
        xa = _make_arrow(
            [nx, NODE_Y - NODE_H / 2 - 0.04, 0],
            [nx, LYMPH_Y + 0.05, 0],
            ex_col, stroke_width=6.0 * sc,
        ).set_opacity(alpha)
        exit_arrows.add(xa)

    # BLUE lymph line running under the nodes and back up to the blood band
    lymph_horiz = Line(
        [NODE_XS[0] - 0.1, LYMPH_Y, 0], [LYMPH_UP_X, LYMPH_Y, 0],
        color=BLUE, stroke_width=5.0,
    ).set_opacity(alpha)
    lymph_up = _make_arrow(
        [LYMPH_UP_X, LYMPH_Y, 0], [LYMPH_UP_X, BLOOD_Y - BLOOD_H / 2, 0],
        BLUE, stroke_width=5.0,
    ).set_opacity(alpha)
    lymph_line = VGroup(lymph_horiz, lymph_up)

    # Dynamic YELLOW lymphocyte dots driven by LymphTrafficSim
    dots_layer = VGroup()
    dots_layer.layout_ok = True  # moving cell swarm inside vessels/organs
    blood_dot_mobs = VGroup(*[Dot(radius=0.062, color=YELLOW) for _ in sim.blood_pts])
    spleen_dot_mobs = VGroup(*[Dot(radius=0.055, color=YELLOW) for _ in sim.spleen_pts])
    node_dot_mobs = VGroup(*[
        VGroup(*[Dot(radius=0.055, color=YELLOW) for _ in pts])
        for pts in sim.node_pts
    ])
    lymph_dot_mobs = VGroup(*[Dot(radius=0.055, color=YELLOW) for _ in sim.lymph_pts])
    dots_layer.add(blood_dot_mobs, spleen_dot_mobs, node_dot_mobs, lymph_dot_mobs)

    def _update_dots(mob, dt):
        sim.blood_density = blood_density_tracker.get_value()
        sim.step(dt)
        bd = sim.blood_density
        for d, p in zip(blood_dot_mobs, sim.blood_pts):
            d.move_to([p[0], BLOOD_Y + p[1], 0])
            vis = p[3] <= bd + 1e-6
            d.set_opacity(alpha if vis else 0.0)
        for d, p in zip(spleen_dot_mobs, sim.spleen_pts):
            d.move_to([SPLEEN_CENTER[0] + p[0], SPLEEN_CENTER[1] + p[1], 0]).set_opacity(alpha)
        for idx, (grp, pts) in enumerate(zip(node_dot_mobs, sim.node_pts)):
            for d, p in zip(grp, pts):
                d.move_to([NODE_XS[idx] + p[0], NODE_Y + p[1], 0]).set_opacity(alpha)
        h_len = LYMPH_UP_X - (NODE_XS[0] - 0.1)
        v_len = (BLOOD_Y - BLOOD_H / 2) - LYMPH_Y
        tot = h_len + v_len
        for d, s in zip(lymph_dot_mobs, sim.lymph_pts):
            dist = s * tot
            if dist <= h_len:
                d.move_to([NODE_XS[0] - 0.1 + dist, LYMPH_Y, 0])
            else:
                d.move_to([LYMPH_UP_X, LYMPH_Y + (dist - h_len), 0])
            d.set_opacity(alpha)

    dots_layer.add_updater(_update_dots)
    _update_dots(dots_layer, 0.0)

    loop_grp = VGroup(
        blood_band, spleen_box, spleen_in, spleen_out,
        node_boxes, entry_arrows, exit_arrows, lymph_line, dots_layer,
    )

    labels_grp = VGroup()
    if show_labels and not dimmed:
        blood_lbl = T("blood", 28, RED).move_to([-4.85, BLOOD_Y + 0.58, 0])
        spleen_lbl = T("spleen", 28, TEXT).move_to([SPLEEN_CENTER[0], -1.02, 0])
        nodes_lbl = T("nodes under the skin", 28, TEXT).move_to([-0.75, -1.92, 0])
        sch_lbl = T("schematic: many nodes", 24, GREY).move_to([-0.75, -2.35, 0])
        labels_grp.add(blood_lbl, spleen_lbl, nodes_lbl, sch_lbl)

    bar_grp = VGroup()
    if show_bar and not dimmed:
        bar_w = BAR_X1 - BAR_X0
        bar_h = BAR_Y1 - BAR_Y0
        bar_cx = (BAR_X0 + BAR_X1) / 2
        bar_title = T("where the pool sits", 28, TEXT).move_to([bar_cx + 0.35, 2.48, 0])

        def _mk_bar():
            ef = exit_factor_tracker.get_value()
            b_pct, s_pct, n_pct, _ = pool_shares(ef)
            hg = bar_h * (n_pct / 100.0)
            hs = bar_h * (s_pct / 100.0)
            hb = bar_h * (b_pct / 100.0)

            rg = Rectangle(
                width=bar_w, height=max(hg, 0.02),
                stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.68,
            ).move_to([bar_cx, BAR_Y0 + hg / 2, 0])
            rs = Rectangle(
                width=bar_w, height=max(hs, 0.02),
                stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.45,
            ).move_to([bar_cx, BAR_Y0 + hg + hs / 2, 0])
            rb = Rectangle(
                width=bar_w, height=max(hb, 0.02),
                stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.80,
            ).move_to([bar_cx, BAR_Y0 + hg + hs + hb / 2, 0])

            b_y = BAR_Y0 + hg + hs + hb / 2
            n_y = BAR_Y0 + hg / 2
            b_tick = Line([BAR_X1 + 0.04, b_y, 0], [BAR_X1 + 0.22, b_y, 0], color=RED, stroke_width=3)
            b_lbl = T(f"blood {b_pct:.1f}%", 24, RED).move_to([BAR_X1 + 0.30, b_y, 0], aligned_edge=LEFT)
            n_tick = Line([BAR_X1 + 0.04, n_y, 0], [BAR_X1 + 0.22, n_y, 0], color=GREEN, stroke_width=3)
            n_lbl = T(f"nodes {n_pct:.1f}%", 24, GREEN).move_to([BAR_X1 + 0.30, n_y, 0], aligned_edge=LEFT)
            return VGroup(rg, rs, rb, b_tick, b_lbl, n_tick, n_lbl)

        bar_live = always_redraw(_mk_bar)
        bar_grp.add(bar_title, bar_live)

    world.add(loop_grp, labels_grp, bar_grp)
    world.loop_grp = loop_grp
    world.blood_band = blood_band
    world.spleen_box = spleen_box
    world.node_boxes = node_boxes
    world.entry_arrows = entry_arrows
    world.exit_arrows = exit_arrows
    world.lymph_line = lymph_line
    world.dots_layer = dots_layer
    world.labels_grp = labels_grp
    world.bar_grp = bar_grp
    return world


def make_held_bar(node_idx=2, scale_tracker=None, color=GREEN):
    """Small GREEN held bar right beside node `node_idx` (base y = -0.53)."""
    if scale_tracker is None:
        scale_tracker = ValueTracker(1.0)
    bx = NODE_XS[node_idx] + NODE_W / 2 + 0.14
    base_y = NODE_Y - NODE_H / 2
    base_h = 0.44

    def _mk():
        h = base_h * scale_tracker.get_value()
        return Rectangle(
            width=0.18, height=max(h, 0.02),
            stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.80,
        ).move_to([bx, base_y + h / 2, 0])

    return always_redraw(_mk), np.array([bx, base_y, 0.0])


# ------------------------------------------------------------------ S00 Hook
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=7)
        ef = ValueTracker(1.0)
        bd = ValueTracker(1.0)
        world = build_world(sim, ef, bd)
        held_scale = ValueTracker(1.0)
        held_bar, _ = make_held_bar(2, held_scale)

        self.add(world)
        self.at("one node halved")
        mid_exit = world.exit_arrows[2]
        halved_exit = _make_arrow(
            [NODE_XS[2], NODE_Y - NODE_H / 2 - 0.04, 0],
            [NODE_XS[2], LYMPH_Y + 0.05, 0],
            ORANGE, stroke_width=3.0,
        )
        sim.node_exit_scales[2] = 0.5
        self.play(Transform(mid_exit, halved_exit), run_time=0.6)

        last_tag = T("last time: ×2", 26, GREEN).move_to([-0.25, -2.92, 0])
        self.add(held_bar)
        self.play(
            held_scale.animate.set_value(2.0),
            FadeIn(last_tag, shift=UP * 0.08),
            run_time=1.0,
        )

        self.at("With entry fixed")
        self.play(Indicate(world.entry_arrows[2], color=RED, scale_factor=1.12), run_time=0.8)

        self.at("every node slowed")
        new_exits = [
            _make_arrow(
                [nx, NODE_Y - NODE_H / 2 - 0.04, 0],
                [nx, LYMPH_Y + 0.05, 0],
                ORANGE, stroke_width=3.0,
            )
            for nx in NODE_XS
        ]
        for idx in range(5):
            sim.node_exit_scales[idx] = 0.5
        q_top = T("Every node at once?", 38, TEXT).move_to([-1.4, 3.05, 0])
        self.play(
            *[Transform(world.exit_arrows[i], new_exits[i]) for i in range(5)],
            FadeOut(last_tag),
            FadeOut(held_bar),
            FadeIn(q_top, shift=DOWN * 0.1),
            run_time=1.1,
        )
        self.finish()


# ------------------------------------------------------------------ S01 Title (2.0s silent)
class S01Title(NarratedScene):
    def construct(self):
        sim = LymphTrafficSim(seed=11)
        ef = ValueTracker(1.0)
        bd = ValueTracker(1.0)
        world = build_world(sim, ef, bd, node_scales=(0.5, 0.5, 0.5, 0.5, 0.5))
        q_top = T("Every node at once?", 38, TEXT).move_to([-1.4, 3.05, 0])
        title = T("One Node, or Every Node", 44, TEXT, font=TITLE_FONT).move_to([-1.4, 3.05, 0])
        fit(title, max_w=7.8)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.14)

        self.add(world, q_top)
        teal_exits = [
            _make_arrow(
                [nx, NODE_Y - NODE_H / 2 - 0.04, 0],
                [nx, LYMPH_Y + 0.05, 0],
                TEAL, stroke_width=6.0,
            )
            for nx in NODE_XS
        ]
        self.play(
            FadeOut(q_top, run_time=0.45),
            *[Transform(world.exit_arrows[i], teal_exits[i], run_time=0.8) for i in range(5)],
        )
        self.play(FadeIn(title, shift=UP * 0.08), GrowFromCenter(rule), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ S02 Chance exit in spleen
class S02ChanceExit(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=17)
        dim_world = build_world(sim, show_labels=False, show_bar=False, dimmed=True)
        dim_world.layout_ok = True
        dim_world.set_z_index(-5)
        self.add(dim_world)

        # Compact pool inset at top right (all text >= 22pt, numbers match main bar)
        b_pct, s_pct, n_pct, _ = pool_shares(1.0)
        inset_box = RoundedRectangle(
            corner_radius=0.12, width=2.95, height=1.85,
            stroke_color=GREY, stroke_width=2.0, fill_color=BG, fill_opacity=0.95,
        ).move_to([4.65, 2.55, 0])
        inset_title = T("pool", 24, TEXT).move_to([4.65, 3.22, 0])
        ib_w, ib_h = 0.52, 1.10
        ib_x = 3.65
        ib_y0 = 1.85
        ig = Rectangle(width=ib_w, height=ib_h * n_pct / 100, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.7).move_to([ib_x, ib_y0 + ib_h * n_pct / 200, 0])
        is_ = Rectangle(width=ib_w, height=ib_h * s_pct / 100, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.45).move_to([ib_x, ib_y0 + ib_h * (n_pct + s_pct / 2) / 100, 0])
        ib = Rectangle(width=ib_w, height=ib_h * b_pct / 100, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.8).move_to([ib_x, ib_y0 + ib_h * (n_pct + s_pct + b_pct / 2) / 100, 0])
        in_lbl = T(f"nodes {n_pct:.1f}%", 22, GREEN).move_to([4.05, ib_y0 + 0.35, 0], aligned_edge=LEFT)
        ib_lbl = T(f"blood {b_pct:.1f}%", 22, RED).move_to([4.05, ib_y0 + 0.98, 0], aligned_edge=LEFT)
        inset = VGroup(inset_box, inset_title, ig, is_, ib, in_lbl, ib_lbl)

        # Zoomed spleen (~65% of frame height = 4.4u, opaque dark interior so backdrop does not clutter)
        sp_c = np.array([-1.0, -0.25, 0.0])
        sp_w, sp_h = 5.6, 4.4
        spleen = RoundedRectangle(
            corner_radius=0.35, width=sp_w, height=sp_h,
            stroke_color=GREY, stroke_width=3.5, fill_color=ORGAN_FILL, fill_opacity=0.96,
        ).move_to(sp_c)
        sp_lbl = T("spleen", 30, TEXT).next_to(spleen, DOWN, buff=0.18)

        art_in = _make_arrow([sp_c[0] - 1.8, sp_c[1] + sp_h / 2 + 0.95, 0], [sp_c[0] - 1.8, sp_c[1] + sp_h / 2 + 0.04, 0], RED, stroke_width=7.0)
        ex_pos = np.array([sp_c[0] + 1.8, sp_c[1] + sp_h / 2 + 0.04, 0])
        ex_out = _make_arrow(ex_pos, [sp_c[0] + 1.8, sp_c[1] + sp_h / 2 + 0.95, 0], TEAL, stroke_width=7.0)
        ex_lbl = T("exit", 26, TEAL).next_to(ex_out, RIGHT, buff=0.18)

        # Random-walk dots inside zoomed spleen (100 baseline, expandable to 300)
        rng = np.random.default_rng(42)
        n_base, n_dense = 100, 300
        density_tr = ValueTracker(1.0)
        walkers = []
        for i in range(n_dense):
            walkers.append([
                rng.uniform(-sp_w * 0.42, sp_w * 0.42),
                rng.uniform(-sp_h * 0.40, sp_h * 0.40),
                rng.uniform(-0.6, 0.6),
                rng.uniform(-0.6, 0.6),
                i,
                0.0,  # flash timer
            ])

        dot_group = VGroup(*[Dot(radius=0.055, color=YELLOW) for _ in range(n_dense)])
        dot_group.layout_ok = True

        # Pool of exiting dot animations slipping up through the TEAL exit arrow
        ex_pool = VGroup(*[Dot(radius=0.070, color=TEAL) for _ in range(8)])
        ex_pool.layout_ok = True
        ex_state = [[0.0, 0.0, -1.0] for _ in range(8)]  # [x, y, life (-1 inactive)]

        # Tracked special dot with hollow white ring (NEVER call set_opacity on Circle!)
        track_pos = np.array([sp_c[0] - 0.5, sp_c[1] - 0.2, 0.0])
        track_dot = Dot(track_pos, radius=0.075, color=YELLOW)
        track_ring = Circle(radius=0.17, stroke_color=TEXT, stroke_width=3.2, fill_opacity=0.0).move_to(track_pos)
        track_grp = VGroup(track_dot, track_ring)
        track_grp.layout_ok = True
        track_mode = {"on": False, "t": 0.0}

        way_t = [0.0, 1.4, 2.6, 3.8, 5.2, 7.0, 9.5, 13.0, 17.0, 22.0]
        way_p = [
            sp_c + np.array([-0.5, -0.2, 0.0]),
            sp_c + np.array([0.8, 0.9, 0.0]),
            sp_c + np.array([1.65, 1.85, 0.0]),   # nears the TEAL exit
            sp_c + np.array([1.2, 0.7, 0.0]),     # turns away!
            sp_c + np.array([-0.4, -0.5, 0.0]),
            sp_c + np.array([-1.6, 0.4, 0.0]),
            sp_c + np.array([-0.2, 1.1, 0.0]),
            sp_c + np.array([0.9, -1.0, 0.0]),
            sp_c + np.array([-1.1, -0.8, 0.0]),
            sp_c + np.array([0.3, 0.2, 0.0]),
        ]

        minute_tr = ValueTracker(0.0)
        last_tick_min = {"m": 0}

        def _update_spleen(mob, dt):
            if dt <= 0:
                return
            dt = min(dt, 0.1)
            active_n = int(round(n_base + (n_dense - n_base) * np.clip((density_tr.get_value() - 1.0) / 2.0, 0.0, 1.0)))
            hw, hh = sp_w * 0.44, sp_h * 0.42
            for w in walkers:
                w[2] += rng.normal(0, 1.4) * dt
                w[3] += rng.normal(0, 1.4) * dt
                sp = np.hypot(w[2], w[3])
                if sp > 0.85:
                    w[2] *= 0.85 / sp
                    w[3] *= 0.85 / sp
                w[0] += w[2] * dt
                w[1] += w[3] * dt
                if abs(w[0]) > hw:
                    w[0] = np.sign(w[0]) * hw
                    w[2] *= -1
                if abs(w[1]) > hh:
                    w[1] = np.sign(w[1]) * hh
                    w[3] *= -1
                if w[5] > 0:
                    w[5] = max(0.0, w[5] - dt)

            cur_m = int(minute_tr.get_value())
            if cur_m > last_tick_min["m"]:
                last_tick_min["m"] = cur_m
                n_leave = max(1, int(round(0.007 * active_n)))
                picks = rng.choice(active_n, size=min(n_leave, active_n), replace=False)
                for idx in picks:
                    walkers[idx][5] = 0.45
                    for st in ex_state:
                        if st[2] < 0:
                            st[0] = ex_pos[0] + rng.uniform(-0.08, 0.08)
                            st[1] = ex_pos[1] - 0.12
                            st[2] = 0.0
                            break
                    walkers[idx][0] = -1.8 + rng.uniform(-0.2, 0.2)
                    walkers[idx][1] = hh * 0.95

            for st, em in zip(ex_state, ex_pool):
                if st[2] >= 0:
                    st[2] += dt
                    st[1] += 1.45 * dt
                    em.move_to([st[0], st[1], 0]).set_opacity(1.0)
                    if st[2] > 0.72:
                        st[2] = -1.0
                        em.set_opacity(0.0)
                else:
                    em.set_opacity(0.0)

            for i, d in enumerate(dot_group):
                w = walkers[i]
                if i < active_n:
                    d.move_to(sp_c + np.array([w[0], w[1], 0.0]))
                    if w[5] > 0:
                        d.set_color(TEAL).scale_to_fit_width(0.16)
                    else:
                        d.set_color(YELLOW).scale_to_fit_width(0.11)
                    d.set_opacity(1.0)
                else:
                    d.set_opacity(0.0)

            if track_mode["on"]:
                track_mode["t"] += dt
                tt = track_mode["t"]
                p = np.array([
                    np.interp(tt, way_t, [q[0] for q in way_p]),
                    np.interp(tt, way_t, [q[1] for q in way_p]),
                    0.0,
                ])
                track_dot.move_to(p).set_opacity(1.0)
                track_ring.move_to(p).set_stroke(opacity=1.0)
            else:
                track_dot.set_opacity(0.0)
                track_ring.set_stroke(opacity=0.0)

        dot_group.add_updater(_update_spleen)
        _update_spleen(dot_group, 0.01)

        self.play(
            FadeIn(spleen), FadeIn(sp_lbl), FadeIn(art_in), FadeIn(ex_out), FadeIn(ex_lbl),
            FadeIn(inset), run_time=0.9,
        )
        self.add(dot_group, ex_pool, track_grp)

        self.at("no scheduled departure")
        track_mode["on"] = True

        self.at("chance")
        min_counter = counter("minute {:.0f}", minute_tr, at=[4.5, 0.55, 0], size=30, color=TEXT)
        rate_lbl = T("0.7% per minute", 28, TEAL).move_to([4.5, -0.15, 0])
        self.play(FadeIn(min_counter), FadeIn(rate_lbl), run_time=0.5)
        self.play(minute_tr.animate.set_value(10), run_time=7.0, rate_func=linear)

        self.at("That holds for")
        billion_lbl = T("a billion (schematic)", 24, YELLOW).move_to([4.5, -1.05, 0])
        self.play(FadeIn(billion_lbl), run_time=0.35)
        self.play(
            density_tr.animate.set_value(3.0),
            minute_tr.animate.set_value(14),
            run_time=2.2,
            rate_func=linear,
        )
        self.play(
            density_tr.animate.set_value(1.0),
            FadeOut(billion_lbl),
            minute_tr.animate.set_value(16),
            run_time=1.3,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ S03 Entry not in stay
class S03EntryNotInStay(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=23)
        dim_world = build_world(sim, show_labels=False, show_bar=False, dimmed=True)
        dim_world.layout_ok = True
        dim_world.set_z_index(-5)
        self.add(dim_world)

        # Zoomed middle node (~60% frame height, opaque interior)
        nd_c = np.array([-1.8, 0.35, 0.0])
        nd_w, nd_h = 4.6, 3.6
        node = RoundedRectangle(
            corner_radius=0.35, width=nd_w, height=nd_h,
            stroke_color=GREY, stroke_width=3.5, fill_color=ORGAN_FILL, fill_opacity=0.96,
        ).move_to(nd_c)
        node_lbl = T("mouse node", 28, TEXT).next_to(node, LEFT, buff=0.22)

        ent_top_y = nd_c[1] + nd_h / 2 + 1.05
        ent_bot_y = nd_c[1] + nd_h / 2 + 0.05
        ent_x1 = nd_c[0] - 0.95
        ent_x2 = nd_c[0] + 0.95

        ent_w = ValueTracker(8.0)
        entry_main = always_redraw(lambda: _make_arrow(
            [nd_c[0], ent_top_y, 0], [nd_c[0], ent_bot_y, 0], RED, stroke_width=ent_w.get_value(),
        ))
        exit_arrow = _make_arrow(
            [nd_c[0], nd_c[1] - nd_h / 2 - 0.04, 0],
            [nd_c[0], nd_c[1] - nd_h / 2 - 0.95, 0],
            TEAL, stroke_width=7.0,
        )

        # TEAL exit dial beside the node, fixed at 1.0x
        ex_val = ValueTracker(0.5)
        ex_dial = dial(ex_val, center=[3.6, 0.5, 0], radius=1.3, label="exit rate (fixed)", color=TEAL, fmt="{:.1f}×", scale=2.0, size=34)

        # Wandering cells inside zoomed node (filled dots = CD4, open rings = CD8)
        rng = np.random.default_rng(31)
        cd4_data = [[rng.uniform(-1.8, 1.8), rng.uniform(-1.4, 1.4), rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)] for _ in range(28)]
        cd8_data = [[rng.uniform(-1.8, 1.8), rng.uniform(-1.4, 1.4), rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)] for _ in range(28)]
        cd4_dots = VGroup(*[Dot(radius=0.06, color=YELLOW) for _ in cd4_data])
        cd8_rings = VGroup(*[Circle(radius=0.075, stroke_color=YELLOW, stroke_width=2.6, fill_opacity=0.0) for _ in cd8_data])
        cd4_dots.layout_ok = True
        cd8_rings.layout_ok = True
        show_cd4 = {"on": False}
        show_cd8 = {"on": False}

        def _walk_node(mob, dt):
            if dt <= 0:
                return
            dt = min(dt, 0.1)
            hw, hh = nd_w * 0.42, nd_h * 0.40
            for group_data, group_mobs, is_ring, flag in (
                (cd4_data, cd4_dots, False, show_cd4["on"]),
                (cd8_data, cd8_rings, True, show_cd8["on"]),
            ):
                for p, m in zip(group_data, group_mobs):
                    p[2] += rng.normal(0, 1.1) * dt
                    p[3] += rng.normal(0, 1.1) * dt
                    sp = np.hypot(p[2], p[3])
                    if sp > 0.7:
                        p[2] *= 0.7 / sp
                        p[3] *= 0.7 / sp
                    p[0] += p[2] * dt
                    p[1] += p[3] * dt
                    if abs(p[0]) > hw:
                        p[0] = np.sign(p[0]) * hw
                        p[2] *= -1
                    if abs(p[1]) > hh:
                        p[1] = np.sign(p[1]) * hh
                        p[3] *= -1
                    m.move_to(nd_c + np.array([p[0], p[1], 0.0]))
                    if is_ring:
                        m.set_stroke(opacity=1.0 if flag else 0.0)
                    else:
                        m.set_opacity(1.0 if flag else 0.0)

        cd4_dots.add_updater(_walk_node)
        _walk_node(cd4_dots, 0.01)

        self.play(FadeIn(node), FadeIn(node_lbl), FadeIn(entry_main), FadeIn(exit_arrow), FadeIn(ex_dial), run_time=0.8)
        self.add(cd4_dots, cd8_rings)

        self.at("has no effect")
        for target in (14.0, 4.0, 14.0, 8.0):
            self.play(ent_w.animate.set_value(target), run_time=0.55)

        self.at("Try made")
        made_tag = T("made-up entry", 26, TEXT).move_to([nd_c[0], ent_top_y + 0.35, 0])
        e_left = _make_arrow([ent_x1, ent_top_y, 0], [ent_x1, ent_bot_y, 0], RED, stroke_width=7.0)
        e_right = _make_arrow([ent_x2, ent_top_y, 0], [ent_x2, ent_bot_y, 0], RED, stroke_width=7.0)
        self.play(FadeOut(entry_main), FadeIn(e_left), FadeIn(e_right), FadeIn(made_tag), run_time=0.6)

        self.at("A thousand naive")
        show_cd4["on"] = True
        cd4_lbl = T("CD4: 1,000 per h", 26, YELLOW).next_to(e_left, LEFT, buff=0.20)
        self.play(FadeIn(cd4_lbl, shift=DOWN * 0.1), run_time=0.6)

        self.at("So do a thousand")
        show_cd8["on"] = True
        cd8_lbl = T("CD8: 1,000 per h", 26, YELLOW).next_to(e_right, RIGHT, buff=0.14)
        self.play(FadeIn(cd8_lbl, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ S04 CD4 vs CD8
class S04Cd4Cd8(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=29)
        dim_world = build_world(sim, show_labels=False, show_bar=False, dimmed=True)
        dim_world.layout_ok = True
        dim_world.set_z_index(-5)
        self.add(dim_world)

        nd_c = np.array([-1.8, 0.55, 0.0])
        nd_w, nd_h = 4.6, 3.2
        node = RoundedRectangle(
            corner_radius=0.35, width=nd_w, height=nd_h,
            stroke_color=GREY, stroke_width=3.5, fill_color=ORGAN_FILL, fill_opacity=0.96,
        ).move_to(nd_c)
        node_lbl = T("mouse node", 28, TEXT).next_to(node, LEFT, buff=0.22)

        ent_top_y = nd_c[1] + nd_h / 2 + 0.95
        ent_bot_y = nd_c[1] + nd_h / 2 + 0.05
        ent_x1 = nd_c[0] - 0.95
        ent_x2 = nd_c[0] + 0.95
        e_left = _make_arrow([ent_x1, ent_top_y, 0], [ent_x1, ent_bot_y, 0], RED, stroke_width=7.0)
        e_right = _make_arrow([ent_x2, ent_top_y, 0], [ent_x2, ent_bot_y, 0], RED, stroke_width=7.0)
        made_tag = T("made-up entry", 26, TEXT).move_to([nd_c[0], ent_top_y + 0.32, 0])
        cd4_lbl = T("CD4: 1,000 per h", 24, YELLOW).next_to(e_left, LEFT, buff=0.18)
        cd8_lbl = T("CD8: 1,000 per h", 24, YELLOW).next_to(e_right, RIGHT, buff=0.14)

        rng = np.random.default_rng(37)
        cd4_data = [[rng.uniform(-1.8, 1.8), rng.uniform(-1.2, 1.2), rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)] for _ in range(24)]
        cd8_data = [[rng.uniform(-1.8, 1.8), rng.uniform(-1.2, 1.2), rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)] for _ in range(42)]
        cd4_dots = VGroup(*[Dot(radius=0.055, color=YELLOW) for _ in cd4_data])
        cd8_rings = VGroup(*[Circle(radius=0.07, stroke_color=YELLOW, stroke_width=2.5, fill_opacity=0.0) for _ in cd8_data])
        cd4_dots.layout_ok = True
        cd8_rings.layout_ok = True

        def _walk_both(mob, dt):
            if dt <= 0:
                return
            dt = min(dt, 0.1)
            hw, hh = nd_w * 0.42, nd_h * 0.38
            for grp_d, grp_m in ((cd4_data, cd4_dots), (cd8_data, cd8_rings)):
                for p, m in zip(grp_d, grp_m):
                    p[2] += rng.normal(0, 1.0) * dt
                    p[3] += rng.normal(0, 1.0) * dt
                    sp = np.hypot(p[2], p[3])
                    if sp > 0.65:
                        p[2] *= 0.65 / sp
                        p[3] *= 0.65 / sp
                    p[0] += p[2] * dt
                    p[1] += p[3] * dt
                    if abs(p[0]) > hw:
                        p[0] = np.sign(p[0]) * hw
                        p[2] *= -1
                    if abs(p[1]) > hh:
                        p[1] = np.sign(p[1]) * hh
                        p[3] *= -1
                    m.move_to(nd_c + np.array([p[0], p[1], 0.0]))

        cd4_dots.add_updater(_walk_both)
        _walk_both(cd4_dots, 0.01)

        # Shared horizontal stay axis below the node: 0 to 24 h
        ax_x0, ax_x1 = -4.2, 0.6
        ax_y = -2.85
        stay_axis = Line([ax_x0, ax_y, 0], [ax_x1, ax_y, 0], color=GREY, stroke_width=3)
        xticks = VGroup()
        for h in (0, 6, 12, 18, 24):
            px = ax_x0 + (h / 24.0) * (ax_x1 - ax_x0)
            xticks.add(Line([px, ax_y, 0], [px, ax_y - 0.10, 0], color=GREY, stroke_width=2.5))
            xticks.add(T(f"{h} h" if h == 24 else f"{h}", 22, GREY).move_to([px, ax_y - 0.32, 0]))

        cd4_h_tr = ValueTracker(0.0)
        cd8_h_tr = ValueTracker(0.0)
        y_cd4 = -1.70
        y_cd8 = -2.30

        def _stay_bar(tr, y, col):
            w = max(0.02, (tr.get_value() / 24.0) * (ax_x1 - ax_x0))
            return Rectangle(
                width=w, height=0.34, stroke_color=col, stroke_width=2.5,
                fill_color=col, fill_opacity=0.65,
            ).move_to([ax_x0 + w / 2, y, 0])

        bar_cd4_stay = always_redraw(lambda: _stay_bar(cd4_h_tr, y_cd4, TEAL))
        bar_cd8_stay = always_redraw(lambda: _stay_bar(cd8_h_tr, y_cd8, TEAL))
        lbl_cd4_stay = T("CD4 ~12 h", 26, TEXT).move_to([ax_x0 - 0.25, y_cd4, 0], aligned_edge=RIGHT)
        lbl_cd8_stay = T("CD8 ~21 h", 26, TEXT).move_to([ax_x0 - 0.25, y_cd8, 0], aligned_edge=RIGHT)

        # GREEN held bars beside the node on the right: computed = 1000 * stay (wide separation)
        hb_y0 = -1.05
        hb_max_h = 2.95
        hb_x1, hb_x2 = 2.05, 4.45
        cd4_held_tr = ValueTracker(0.0)
        cd8_held_tr = ValueTracker(0.0)
        max_held = 24000.0

        def _held_bar_mk(tr, x, prefix):
            val = tr.get_value()
            h = max(0.02, (val / max_held) * hb_max_h)
            r = Rectangle(
                width=0.88, height=h, stroke_color=GREEN, stroke_width=2.5,
                fill_color=GREEN, fill_opacity=0.72,
            ).move_to([x, hb_y0 + h / 2, 0])
            num = M(f"{prefix}: {val:,.0f}", 24, GREEN).move_to([x, hb_y0 - 0.36, 0])
            return VGroup(r, num)

        held_cd4_mob = always_redraw(lambda: _held_bar_mk(cd4_held_tr, hb_x1, "CD4"))
        held_cd8_mob = always_redraw(lambda: _held_bar_mk(cd8_held_tr, hb_x2, "CD8"))
        held_title = T("cells held\n(entry × stay)", 26, GREEN).move_to([3.35, 2.25, 0])

        self.add(node, node_lbl, e_left, e_right, made_tag, cd4_lbl, cd8_lbl, cd4_dots, cd8_rings)
        self.play(FadeIn(stay_axis), FadeIn(xticks), FadeIn(lbl_cd4_stay), FadeIn(lbl_cd8_stay), run_time=0.7)
        self.add(bar_cd4_stay, bar_cd8_stay)

        self.at("CD4 cells cross")
        self.play(cd4_h_tr.animate.set_value(12.2), run_time=1.8)

        self.at("CD8 cells take")
        self.play(cd8_h_tr.animate.set_value(21.2), run_time=1.8)

        self.at("the node holds")
        self.play(FadeIn(held_title), run_time=0.35)
        self.add(held_cd4_mob, held_cd8_mob)
        self.play(
            cd4_held_tr.animate.set_value(12200.0),
            cd8_held_tr.animate.set_value(21200.0),
            run_time=2.0,
        )
        top1 = hb_y0 + (12200.0 / max_held) * hb_max_h
        top2 = hb_y0 + (21200.0 / max_held) * hb_max_h
        br_x = hb_x2 + 0.68
        bracket = VGroup(
            Line([hb_x1 + 0.48, top1, 0], [br_x, top1, 0], color=GOLD, stroke_width=3),
            Line([br_x, top1, 0], [br_x, top2, 0], color=GOLD, stroke_width=3),
            Line([hb_x2 + 0.48, top2, 0], [br_x, top2, 0], color=GOLD, stroke_width=3),
        )
        ratio_lbl = T("×1.74", 28, GOLD).next_to(bracket, RIGHT, buff=0.14)
        self.play(Create(bracket), FadeIn(ratio_lbl), run_time=0.8)

        self.at("Entry was equal")
        self.play(
            Indicate(e_left, color=RED, scale_factor=1.18),
            Indicate(e_right, color=RED, scale_factor=1.18),
            run_time=0.9,
        )

        self.at("the stay alone")
        glow1 = SurroundingRectangle(bar_cd4_stay, color=GOLD, buff=0.06, stroke_width=3)
        glow2 = SurroundingRectangle(bar_cd8_stay, color=GOLD, buff=0.06, stroke_width=3)
        self.play(
            e_left.animate.set_opacity(0.3),
            e_right.animate.set_opacity(0.3),
            Create(glow1),
            Create(glow2),
            run_time=0.8,
        )
        self.finish()


# ------------------------------------------------------------------ S05 The whole rule
class S05Rule(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=41)
        ef = ValueTracker(1.0)
        bd = ValueTracker(1.0)
        world = build_world(sim, ef, bd)
        self.add(world)

        dyn_entries = VGroup()
        for nx in NODE_XS:
            def _mk_ea(nx=nx):
                w = 6.0 * bd.get_value()
                return _make_arrow([nx, BLOOD_Y - BLOOD_H / 2, 0], [nx, NODE_Y + NODE_H / 2 + 0.04, 0], RED, stroke_width=w)
            dyn_entries.add(always_redraw(_mk_ea))
        self.remove(world.entry_arrows)
        world.entry_arrows = dyn_entries
        self.add(dyn_entries)

        self.at("Exit sets how long")
        exit_lbl = T("exit: how long", 28, TEAL).move_to([-0.75, -2.92, 0])
        exit_leader = VGroup(
            DashedLine([exit_lbl.get_right()[0] + 0.14, -2.92, 0], [1.45, -2.92, 0], color=TEAL, stroke_width=2.2, dash_length=0.10),
            DashedLine([1.45, -2.92, 0], [1.45, -1.63, 0], color=TEAL, stroke_width=2.2, dash_length=0.10),
            DashedLine([1.45, -1.63, 0], [-0.28, -1.63, 0], color=TEAL, stroke_width=2.2, dash_length=0.10),
            DashedLine([-0.28, -1.63, 0], [-0.28, -0.97, 0], color=TEAL, stroke_width=2.2, dash_length=0.10),
            Arrow([-0.28, -0.97, 0], [NODE_XS[2] + 0.12, -0.97, 0], color=TEAL, stroke_width=2.2, buff=0, tip_length=0.14, max_tip_length_to_length_ratio=0.45),
        )
        self.play(
            FadeIn(exit_lbl), Create(exit_leader),
            Indicate(world.exit_arrows[2], color=TEAL, scale_factor=1.22),
            run_time=1.0,
        )

        self.at("Entry sets how many")
        entry_lbl = T("entry: how many", 28, RED).move_to([-0.75, 2.95, 0])
        entry_ptr = VGroup(
            DashedLine([-1.22, 2.68, 0], [-1.22, 1.06, 0], color=RED, stroke_width=2.5, dash_length=0.10),
            Arrow([-1.22, 1.06, 0], [NODE_XS[2] - 0.12, 1.06, 0], color=RED, stroke_width=2.5, buff=0, tip_length=0.14, max_tip_length_to_length_ratio=0.45),
        )
        self.play(
            FadeIn(entry_lbl), Create(entry_ptr),
            Indicate(dyn_entries[2], color=RED, scale_factor=1.2),
            run_time=1.0,
        )

        self.at("rises and falls with the cells in blood")
        fed_lbl = T("fed by blood", 24, RED).move_to([1.15, 2.48, 0])
        fed_line = Line([0.05, BLOOD_Y + BLOOD_H / 2, 0], [0.05, 2.48, 0], color=RED, stroke_width=2.5)
        fed_line2 = Line([0.05, 2.48, 0], [fed_lbl.get_left()[0] - 0.12, 2.48, 0], color=RED, stroke_width=2.5)
        self.play(Create(fed_line), Create(fed_line2), FadeIn(fed_lbl), run_time=0.5)
        self.play(bd.animate.set_value(0.35), run_time=1.2)
        self.play(bd.animate.set_value(1.0), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ S06 Predict
class S06Predict(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=47)
        ef = ValueTracker(1.0)
        bd = ValueTracker(1.0)
        world = build_world(sim, ef, bd)
        self.add(world)

        model_tag = T("rat model: three compartments", 26, TEXT).move_to([-3.65, 3.12, 0])
        self.play(FadeIn(model_tag), run_time=0.7)

        self.at("Blood holds about")
        blood_glow = RoundedRectangle(
            corner_radius=0.08, width=BAR_X1 - BAR_X0 + 0.14, height=0.28,
            stroke_color=GOLD, stroke_width=3.5, fill_opacity=0,
        ).move_to([(BAR_X0 + BAR_X1) / 2, BAR_Y1 - 0.08, 0])
        self.play(Create(blood_glow), run_time=0.7)

        self.at("the exit rate constant of all those nodes")
        new_exits = [
            _make_arrow(
                [nx, NODE_Y - NODE_H / 2 - 0.04, 0],
                [nx, LYMPH_Y + 0.05, 0],
                ORANGE, stroke_width=3.0,
            )
            for nx in NODE_XS
        ]
        for idx in range(5):
            sim.node_exit_scales[idx] = 0.5
        exits_lbl = T("all node exits ×1/2", 26, ORANGE).move_to([0.2, -2.92, 0])
        self.play(
            FadeOut(blood_glow),
            *[Transform(world.exit_arrows[i], new_exits[i]) for i in range(5)],
            FadeIn(exits_lbl),
            run_time=1.0,
        )

        self.at("stays twice as long")
        stay_tag = T("stay ×2", 26, ORANGE).move_to([-4.6, -2.92, 0])
        self.play(FadeIn(stay_tag), run_time=0.7)

        self.at("Do the nodes hold")
        q = question_card("Nodes hold twice as many?", color=TEXT, y=-3.05, max_w=9.8)
        self.play(FadeOut(exits_lbl), FadeOut(stay_tag), run_time=0.25)
        self.play(FadeIn(q), run_time=0.35)
        self.finish()


# ------------------------------------------------------------------ S07 Predict Pause (4.5s silent)
class S07Pause(PredictPause):
    QUESTION = "Nodes hold twice as many?"
    CARD = {"color": TEXT, "y": -3.05, "max_w": 9.8}
    SECONDS = 4.5

    def backdrop(self):
        sim = LymphTrafficSim(seed=53)
        for idx in range(5):
            sim.node_exit_scales[idx] = 0.5
        world = build_world(sim, node_scales=(0.5, 0.5, 0.5, 0.5, 0.5))
        model_tag = T("rat model: three compartments", 26, TEXT).move_to([-3.65, 3.12, 0])
        return VGroup(world, model_tag)


# ------------------------------------------------------------------ S08 Answer
class S08Answer(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=59)
        for idx in range(5):
            sim.node_exit_scales[idx] = 0.5
        ef = ValueTracker(1.0)
        bd = ValueTracker(1.0)
        world = build_world(sim, ef, bd, node_scales=(0.5, 0.5, 0.5, 0.5, 0.5))

        dyn_entries = VGroup()
        for nx in NODE_XS:
            def _mk_ea(nx=nx):
                w = 6.0 * bd.get_value()
                return _make_arrow([nx, BLOOD_Y - BLOOD_H / 2, 0], [nx, NODE_Y + NODE_H / 2 + 0.04, 0], RED, stroke_width=w)
            dyn_entries.add(always_redraw(_mk_ea))
        world.remove(world.entry_arrows)
        world.entry_arrows = dyn_entries
        world.add(dyn_entries)

        model_tag = T("rat model: three compartments", 26, TEXT).move_to([-3.65, 3.12, 0])
        q = question_card("Nodes hold twice as many?", color=TEXT, y=-3.05, max_w=9.8)
        self.add(world, model_tag, q)
        self.play(FadeOut(q), run_time=0.5)

        self.at("The pool is closed")
        # Encloses blood band + spleen + 5 nodes + lymph line cleanly below 'blood' and above 'nodes under the skin'
        pool_box = RoundedRectangle(
            corner_radius=0.25, width=8.25, height=3.65,
            stroke_color=GREY, stroke_width=3.0, fill_opacity=0,
        ).move_to([-1.92, 0.265, 0])
        closed_tag = T("closed pool", 26, TEXT).move_to([-3.65, 3.12, 0])
        self.play(Create(pool_box), swap(model_tag, closed_tag, run_time=0.7), run_time=0.9)

        self.at("Blood's share falls")
        _, _, _, target_br = pool_shares(0.5)
        self.play(
            ef.animate.set_value(0.72),
            bd.animate.set_value(1.0 - 0.56 * (1.0 - target_br)),
            run_time=3.8,
            rate_func=linear,
        )

        self.at("Entry into the nodes falls")
        self.play(
            ef.animate.set_value(0.58),
            bd.animate.set_value(1.0 - 0.84 * (1.0 - target_br)),
            Indicate(dyn_entries, color=RED, scale_factor=1.06),
            run_time=3.0,
            rate_func=linear,
        )

        self.at("Their share rises")
        self.play(
            ef.animate.set_value(0.5),
            bd.animate.set_value(target_br),
            run_time=3.2,
            rate_func=linear,
        )

        stay_tag = T("stay ×2", 26, ORANGE).move_to([3.30, -2.50, 0])
        held_tag = T("held ×1.23", 26, GREEN).move_to([5.15, -2.50, 0])
        self.play(FadeIn(stay_tag), FadeIn(held_tag), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ S09 One draining node
class S09OneNode(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=61)
        ef = ValueTracker(1.0)
        bd = ValueTracker(1.0)
        world = build_world(sim, ef, bd)
        held_scale = ValueTracker(1.0)
        held_bar, _ = make_held_bar(2, held_scale)

        extra_nodes = VGroup()
        for k, x in enumerate((-3.45, -3.90, 2.02, 2.40)):
            op = 0.55 if abs(k - 1.5) < 1 else 0.28
            extra_nodes.add(RoundedRectangle(
                corner_radius=0.06, width=0.28, height=0.52,
                stroke_color=GREY, stroke_width=1.8, fill_color=GREY, fill_opacity=0.08,
            ).move_to([x, NODE_Y, 0]).set_opacity(op))
        many_tag = T("one among hundreds (schematic)", 26, TEXT).move_to([-1.2, 3.05, 0])

        self.add(world)
        self.play(FadeIn(extra_nodes), FadeIn(many_tag), run_time=0.7)

        mid_exit = world.exit_arrows[2]
        halved_exit = _make_arrow(
            [NODE_XS[2], NODE_Y - NODE_H / 2 - 0.04, 0],
            [NODE_XS[2], LYMPH_Y + 0.05, 0],
            ORANGE, stroke_width=3.0,
        )
        sim.node_exit_scales[2] = 0.5
        drain_lbl = T("draining node", 26, ORANGE).move_to([NODE_XS[2] + 0.35, -2.92, 0])
        self.play(Transform(mid_exit, halved_exit), FadeIn(drain_lbl), run_time=0.8)

        self.at("barely changes the blood count")
        self.play(Indicate(world.blood_band, color=RED, scale_factor=1.03), run_time=1.0)

        self.at("keeps its old rate")
        self.play(Indicate(world.entry_arrows[2], color=RED, scale_factor=1.18), run_time=1.0)

        self.at("doubles what it holds")
        self.add(held_bar)
        x2_tag = T("×2", 26, GREEN).move_to([NODE_XS[2] + 0.44, 0.90, 0])
        self.play(held_scale.animate.set_value(2.0), FadeIn(x2_tag), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ S10 Why hold cells there
class S10WhyHold(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=67)
        dim_world = build_world(sim, show_labels=False, show_bar=False, dimmed=True)
        dim_world.layout_ok = True
        dim_world.set_z_index(-5)
        self.add(dim_world)

        nd_c = np.array([-0.8, -0.1, 0.0])
        nd_w, nd_h = 5.4, 4.3
        node = RoundedRectangle(
            corner_radius=0.38, width=nd_w, height=nd_h,
            stroke_color=GREY, stroke_width=3.5, fill_color=ORGAN_FILL, fill_opacity=0.96,
        ).move_to(nd_c)
        node_lbl = T("draining node", 28, TEXT).next_to(node, LEFT, buff=0.22)

        entry_a = _make_arrow([nd_c[0], nd_c[1] + nd_h / 2 + 0.95, 0], [nd_c[0], nd_c[1] + nd_h / 2 + 0.04, 0], RED, stroke_width=7.0)

        ex_width = ValueTracker(3.5)
        ex_color = {"c": ORANGE}
        exit_a = always_redraw(lambda: _make_arrow(
            [nd_c[0], nd_c[1] - nd_h / 2 - 0.04, 0],
            [nd_c[0], nd_c[1] - nd_h / 2 - 0.95, 0],
            ex_color["c"], stroke_width=ex_width.get_value(),
        ))

        hb_scale = ValueTracker(2.0)
        hb_x = nd_c[0] + nd_w / 2 + 0.65
        hb_base_y = nd_c[1] - nd_h / 2
        hb_unit = 1.55
        held_bar = always_redraw(lambda: Rectangle(
            width=0.55, height=max(0.05, hb_unit * hb_scale.get_value()),
            stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.75,
        ).move_to([hb_x, hb_base_y + hb_unit * hb_scale.get_value() / 2, 0]))
        held_lbl = T("cells held", 26, GREEN).move_to([hb_x, hb_base_y - 0.35, 0])

        star_pos = nd_c + np.array([0.55, 0.15, 0.0])
        antigen = Star(n=6, outer_radius=0.26, inner_radius=0.12, color=GREY, fill_color=GREY, fill_opacity=0.85, stroke_width=2).move_to(star_pos)
        antigen_lbl = T("antigen", 26, TEXT).move_to([nd_c[0] + 1.8, nd_c[1] + nd_h / 2 + 0.55, 0])
        ptr_end = antigen_lbl.get_bottom() + DOWN * 0.08
        ptr_dir = ptr_end - star_pos
        ptr_dir = ptr_dir / np.linalg.norm(ptr_dir)
        antigen_ptr = DashedLine(star_pos + ptr_dir * 0.34, ptr_end, color=GREY, stroke_width=2.2)

        rng = np.random.default_rng(71)
        crowd = [[rng.uniform(-2.1, 2.1), rng.uniform(-1.6, 1.6), rng.uniform(-0.55, 0.55), rng.uniform(-0.55, 0.55)] for _ in range(70)]
        crowd_mobs = VGroup(*[Dot(radius=0.055, color=YELLOW) for _ in crowd])
        crowd_mobs.layout_ok = True

        # Rare cell arrives at star_pos at t=9.8s, BEFORE at("more time to find it") (~10.24s)
        wt = [0.0, 2.0, 4.2, 6.2, 8.0, 9.8, 16.5]
        wp = [
            nd_c + np.array([-1.6, 1.2, 0.0]),
            nd_c + np.array([-0.5, 0.3, 0.0]),
            nd_c + np.array([0.8, 1.1, 0.0]),    # misses above the star
            nd_c + np.array([1.7, -0.7, 0.0]),
            nd_c + np.array([-0.6, -1.1, 0.0]),
            star_pos + np.array([-0.22, -0.08, 0.0]),
            star_pos + np.array([-0.22, -0.08, 0.0]),
        ]
        rare_t = {"t": 0.0}
        rare_dot = Dot(wp[0], radius=0.075, color=YELLOW)
        rare_ring = Circle(radius=0.17, stroke_color=TEXT, stroke_width=3.2, fill_opacity=0.0).move_to(wp[0])
        rare_grp = VGroup(rare_dot, rare_ring)
        rare_grp.layout_ok = True

        def _update_draining(mob, dt):
            if dt <= 0:
                return
            dt = min(dt, 0.1)
            hw, hh = nd_w * 0.43, nd_h * 0.41
            for p, m in zip(crowd, crowd_mobs):
                p[2] += rng.normal(0, 1.1) * dt
                p[3] += rng.normal(0, 1.1) * dt
                sp = np.hypot(p[2], p[3])
                if sp > 0.65:
                    p[2] *= 0.65 / sp
                    p[3] *= 0.65 / sp
                p[0] += p[2] * dt
                p[1] += p[3] * dt
                if abs(p[0]) > hw:
                    p[0] = np.sign(p[0]) * hw
                    p[2] *= -1
                if abs(p[1]) > hh:
                    p[1] = np.sign(p[1]) * hh
                    p[3] *= -1
                m.move_to(nd_c + np.array([p[0], p[1], 0.0]))
            rare_t["t"] += dt
            tt = rare_t["t"]
            rp = np.array([
                np.interp(tt, wt, [q[0] for q in wp]),
                np.interp(tt, wt, [q[1] for q in wp]),
                0.0,
            ])
            rare_dot.move_to(rp)
            rare_ring.move_to(rp)

        crowd_mobs.add_updater(_update_draining)
        _update_draining(crowd_mobs, 0.01)

        rare_lbl = T("rare matching cell", 26, TEXT).move_to([-2.75, nd_c[1] + nd_h / 2 + 0.55, 0])
        self.play(
            FadeIn(node), FadeIn(node_lbl), FadeIn(entry_a), FadeIn(exit_a),
            FadeIn(held_bar), FadeIn(held_lbl), FadeIn(antigen), FadeIn(antigen_lbl),
            FadeIn(antigen_ptr), FadeIn(rare_lbl), run_time=0.8,
        )
        self.add(crowd_mobs, rare_grp)

        self.at("more time to find it")
        self.play(
            antigen.animate.set_color(GOLD),
            rare_ring.animate.set_stroke(color=GOLD),
            Indicate(antigen, color=GOLD, scale_factor=1.35),
            run_time=1.0,
        )

        self.at("exit resumes")
        ex_color["c"] = TEAL
        resumes_tag = T("exit resumes", 26, TEAL).next_to(exit_a, RIGHT, buff=0.22)
        self.play(
            ex_width.animate.set_value(7.0),
            hb_scale.animate.set_value(1.0),
            FadeIn(resumes_tag),
            run_time=1.2,
        )
        self.finish()


# ------------------------------------------------------------------ S11 Close
class S11Close(SpokenScene):
    def construct(self):
        sim = LymphTrafficSim(seed=79)
        ef = ValueTracker(1.0)
        bd = ValueTracker(1.0)
        world = build_world(sim, ef, bd)
        held_scale = ValueTracker(1.0)
        held_bar, _ = make_held_bar(2, held_scale)

        dyn_entries = VGroup()
        for nx in NODE_XS:
            def _mk_ea(nx=nx):
                w = 6.0 * bd.get_value()
                return _make_arrow([nx, BLOOD_Y - BLOOD_H / 2, 0], [nx, NODE_Y + NODE_H / 2 + 0.04, 0], RED, stroke_width=w)
            dyn_entries.add(always_redraw(_mk_ea))
        world.remove(world.entry_arrows)
        world.entry_arrows = dyn_entries
        world.add(dyn_entries)

        self.add(world)

        self.at("sets the stay")
        self.play(Indicate(world.exit_arrows[2], color=TEAL, scale_factor=1.2), run_time=0.8)

        self.at("blood supplies the cells")
        self.play(Indicate(world.blood_band, color=RED, scale_factor=1.03), run_time=0.8)

        self.at("One node can draw")
        mid_exit = world.exit_arrows[2]
        halved_mid = _make_arrow([NODE_XS[2], NODE_Y - NODE_H / 2 - 0.04, 0], [NODE_XS[2], LYMPH_Y + 0.05, 0], ORANGE, stroke_width=3.0)
        teal_mid = _make_arrow([NODE_XS[2], NODE_Y - NODE_H / 2 - 0.04, 0], [NODE_XS[2], LYMPH_Y + 0.05, 0], TEAL, stroke_width=6.0)
        sim.node_exit_scales[2] = 0.5
        self.add(held_bar)
        x2_tag = T("×2", 26, GREEN).move_to([NODE_XS[2] + 0.44, 0.90, 0])
        self.play(
            Transform(mid_exit, halved_mid),
            held_scale.animate.set_value(2.0),
            FadeIn(x2_tag),
            run_time=1.0,
        )
        self.wait(0.7)
        sim.node_exit_scales[2] = 1.0
        self.play(
            Transform(mid_exit, teal_mid),
            held_scale.animate.set_value(1.0),
            FadeOut(x2_tag),
            FadeOut(held_bar),
            run_time=0.6,
        )

        self.at("every node draws at once")
        all_halved = [
            _make_arrow([nx, NODE_Y - NODE_H / 2 - 0.04, 0], [nx, LYMPH_Y + 0.05, 0], ORANGE, stroke_width=3.0)
            for nx in NODE_XS
        ]
        for idx in range(5):
            sim.node_exit_scales[idx] = 0.5
        _, _, _, target_br = pool_shares(0.5)
        stay_tag = T("stay ×2", 26, ORANGE).move_to([3.30, -2.50, 0])
        held_tag = T("held ×1.23", 26, GREEN).move_to([5.15, -2.50, 0])
        self.play(
            *[Transform(world.exit_arrows[i], all_halved[i]) for i in range(5)],
            ef.animate.set_value(0.5),
            bd.animate.set_value(target_br),
            run_time=2.8,
        )
        self.play(FadeIn(stay_tag), FadeIn(held_tag), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ S12 End Card
class S12End(EndCard):
    LINE = "Exit sets the stay; entry, fed by blood, sets how many."
