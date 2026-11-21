"""Thrombin Needs a Surface — STEMhop Explainer Film (Chapter 2 of Blood Cells, Hematocrit and Clotting)

COLOUR MAP (one colour per concept, kept across every scene):
- RED     (#FC6255): red blood cells in flow
- AMBER   (#F0B85A): blood plasma (pale translucent lumen tint) and unactivated plasma zymogens/factors
- WHITE   (#E8EAF0, TEXT): intact inner vessel lining, fibrin threads, rulers, headings and scope tags
- TAN     (#D9AF82): subendothelial cells beneath the vessel wall and their tissue factor studs
- VIOLET  (#A678DE): platelets
- GOLD    (#D4A843): activated platelet phosphatidylserine rim and surface highlight
- MAGENTA (#E84A9E): thrombin dots and the right-edge thrombin gauge
- GREEN   (#83C167): factor IXa, VIIIa and the IXa + VIIIa enzyme complex
- ORANGE  (#F28C38): factor Xa, Va and the Xa + Va prothrombinase complex
- CYAN    (#3FB8C0): intact-lining brakes (TFPI, antithrombin, surface sugar, thrombomodulin, protein C,
                     prostacyclin, nitric oxide, plasmin) and the brief link-back kidney patch

ONE WORLD (carried across the whole film):
A longitudinal cross-section of a blood vessel with red cells and plasma flowing left to right above a
thin bright WHITE inner lining, a single torn gap at centre plugged by VIOLET platelets over a TAN layer
of tissue-factor-bearing cells, and a vertical MAGENTA gauge ("thrombin here", tagged "schematic") at
the right edge. The camera zooms into the tear, slides along intact lining, and splits into a cut vs
intact vessel comparison at the close.

WHAT CHANGES PER SPOKEN SCENE:
- s00_link_and_question: Kidney-patch ghost fades; camera slides right past flowing red cells over intact
  lining and back to the tear; "Why only here?" appears. (Poiseuille flow + sliding viewport tracker.)
- s02_surface: Camera pushes into the plug; inward rim ticks on VIOLET platelets rotate outward one by
  one and light up GOLD; flow arrow "held at the breach" and "procoagulant surface" appear. (Zoom & rotation.)
- s03_trickle: Ghost lining parts to expose TAN studs; VIIa binds, X->Xa and IX->IXa are cut, Xa+Va
  emits a thin MAGENTA dot stream; right gauge climbs to 6% ("trickle"). (Advection-diffusion + gauge.)
- s04_signal: CYAN TFPI shuts down TF-VIIa-Xa; released MAGENTA dots travel up to activate remaining
  platelets (GOLD rim) and cut V->Va, VIII->VIIIa (leaving carrier) and XI->XIa. (Particle transport.)
- s05_burst: GREEN (IXa+VIIIa) and ORANGE (Xa+Va) pairs lock onto the GOLD edge; Xa slides between them;
  prothrombin cuts release a dense MAGENTA plume; gauge climbs 6%->95%; split bar shows >90% vs ~6%.
- s06_idea: Pull back to whole vessel; unbound GREEN/ORANGE pairs in midstream drift apart and wash away
  with zero thrombin; bound pairs on GOLD edge pulse and brighten plume; "Made on a surface" appears.
- s07_fibrin: MAGENTA dots cut fibrinogen blocks into WHITE threads knitting a mesh; Factor XIII cuts
  and lays WHITE cross-links that tighten the mesh against a computed arterial-pressure bulge test.
- s08_predict: Pull back with plug at left; MAGENTA dots spill downstream, extinguished by CYAN
  antithrombin; CYAN surface sugar fringe accelerates wall extinction (x100 to x1000); 2-mark ruler lays down.
- s10_reach: Far mark fades; near mark ("1 to 5 µm") and computed concentration band exp(-x/lambda) match
  wall thickness; hiding CYAN fringe stretches lambda ~10x ("tens of µm"); faster flow contracts it.
- s11_brakes: Thrombomodulin turns MAGENTA thrombin CYAN to cut protein C, knocking Va/VIIIa off the plug
  (plume thins, gauge drops); prostacyclin/NO keep passing platelets VIOLET; clock ticks and plasmin clears fibrin.
- s12_close: Whole-vessel recap lights up plug surface -> trickle -> burst in order, then splits into
  TwoPanel comparing the cut finger vessel (full gauge, mesh) vs intact lung vessel (empty gauge, free flow).
"""

import numpy as np
from bp_parts import *
from bp_parts import _touch

# Film-specific concept colours (never grey for text; high contrast on BG #0f1117)
AMBER = "#F0B85A"
TAN = "#D9AF82"
VIOLET = "#A678DE"
MAGENTA = "#E84A9E"
ORANGE = "#F28C38"
CYAN = "#3FB8C0"
WHITE = TEXT

TRICKLE_LEVEL = 0.06
BURST_LEVEL = 0.95
POST_APC_LEVEL = 0.52


# ------------------------------------------------------------------ shared helpers
def make_gauge(tracker, x=5.55, y0=-1.65, y1=1.95, width=0.42, show_trickle_tick=False):
    """Vertical MAGENTA thrombin gauge at the right edge, driven by a single ValueTracker (0..1)."""
    cx = x
    h = y1 - y0
    frame = RoundedRectangle(
        corner_radius=0.08, width=width, height=h,
        stroke_color=WHITE, stroke_width=2.5, fill_color=BG, fill_opacity=0.9,
    ).move_to([cx, (y0 + y1) / 2, 0]).set_z_index(12)

    def _fill():
        v = float(np.clip(tracker.get_value(), 0.0, 1.0))
        fh = max(0.02, v * (h - 0.08))
        r = Rectangle(
            width=width - 0.08, height=fh,
            stroke_width=0, fill_color=MAGENTA, fill_opacity=0.88 if v > 0.005 else 0.0,
        )
        r.move_to([cx, y0 + 0.04 + fh / 2, 0]).set_z_index(13)
        return r

    fill = always_redraw(_fill)
    title = T("thrombin\nhere", size=24, color=MAGENTA, line_spacing=0.85).move_to([cx, y1 + 0.55, 0]).set_z_index(14)
    tag = T("schematic", size=24, color=WHITE).move_to([cx, y0 - 0.42, 0]).set_z_index(14)
    g = VGroup(frame, fill, title, tag)
    g.frame, g.fill, g.title, g.tag = frame, fill, title, tag
    g.y0, g.y1, g.cx, g.h, g.w = y0, y1, cx, h, width
    if show_trickle_tick:
        ty = y0 + 0.04 + TRICKLE_LEVEL * (h - 0.08)
        tick = DashedLine([cx - width / 2 - 0.06, ty, 0], [cx + width / 2 + 0.06, ty, 0],
                          color=WHITE, stroke_width=2.5, dash_length=0.08).set_z_index(14)
        g.add(tick)
        g.trickle_tick = tick
    return g


def make_red_cell(w=0.66, h=0.28):
    """Biconcave-style red blood cell silhouette (no molecular detail)."""
    outer = Ellipse(width=w, height=h, stroke_color="#FF8A80", stroke_width=2.0,
                    fill_color=RED, fill_opacity=0.82)
    dimple = Ellipse(width=w * 0.52, height=h * 0.36, stroke_width=0,
                     fill_color="#8C1D18", fill_opacity=0.65)
    return VGroup(outer, dimple).set_z_index(2)


def spawn_red_cells(n, x_min, x_max, y_bot, y_top, seed=7, w=0.66, h=0.28):
    rng = np.random.default_rng(seed)
    cells = VGroup()
    xs = np.linspace(x_min + 0.3, x_max - 0.3, n) + rng.uniform(-0.22, 0.22, size=n)
    ys = rng.uniform(y_bot + 0.26, y_top - 0.26, size=n)
    for x, y in zip(xs, ys):
        c = make_red_cell(w=w, h=h)
        c.move_to([float(np.clip(x, x_min + 0.2, x_max - 0.2)), float(y), 0])
        c._base_y = float(y)
        c._tilt = float(rng.uniform(-0.08, 0.08))
        c.rotate(c._tilt)
        cells.add(c)
    return cells


def attach_lumen_flow(cells, x_min, x_max, y_bot, y_top, speed_tracker=None,
                      base_speed=1.35, plug_box=None):
    """Attach computed Poiseuille parabolic velocity advection to red cells."""
    yc = 0.5 * (y_bot + y_top)
    half_r = max(0.3, 0.5 * (y_top - y_bot))

    def _u(mob, dt):
        sp = base_speed * (speed_tracker.get_value() if speed_tracker is not None else 1.0)
        for c in mob:
            x, y = c.get_center()[:2]
            rel = np.clip((y - yc) / half_r, -0.92, 0.92)
            vx = sp * (1.0 - 0.55 * rel * rel)
            nx = x + vx * dt
            if nx > x_max - 0.15:
                nx = x_min + 0.15
            ny = c._base_y
            if plug_box is not None:
                px0, px1, py_top = plug_box
                if px0 - 0.3 < nx < px1 + 0.3 and ny < py_top + 0.26:
                    # Smooth streamline deflection over the plug
                    t = np.cos(np.clip((nx - (px0 + px1) / 2) / max(0.2, (px1 - px0) / 2 + 0.3), -1, 1) * PI / 2)
                    ny = max(ny, c._base_y + t * max(0.0, py_top + 0.28 - c._base_y))
            c.move_to([nx, float(np.clip(ny, y_bot + 0.22, y_top - 0.22)), 0])

    cells.add_updater(_u)
    return cells


def make_platelet_disc(center, radius=0.45, activated=False, ticks_out=False, tick_angles=None):
    """VIOLET platelet disc with inward/outward phosphatidylserine marks and optional GOLD rim."""
    c = np.array([center[0], center[1], 0.0], dtype=float)
    rim_col = GOLD if activated else VIOLET
    rim_w = 5.5 if activated else 3.0
    body = Circle(radius=radius, stroke_color=rim_col, stroke_width=rim_w,
                  fill_color=VIOLET, fill_opacity=0.42).move_to(c).set_z_index(4)
    g = VGroup(body)
    g.body = body
    g.marks = VGroup()
    angles = tick_angles if tick_angles is not None else np.linspace(0.15 * PI, 0.85 * PI, 7)
    for ang in angles:
        p = c + radius * np.array([np.cos(ang), np.sin(ang), 0.0])
        u = np.array([np.cos(ang), np.sin(ang), 0.0])
        seg = Line(p, p + (0.14 if ticks_out else -0.14) * u,
                   color=GOLD if ticks_out else VIOLET, stroke_width=3.0).set_z_index(5)
        seg._anchor = p
        seg._out_vec = u
        g.marks.add(seg)
    g.add(g.marks)
    return g


def make_block(text, color, size=24, pad=0.14, fill_opacity=0.22):
    """Compact labelled factor/protein chip sized cleanly to its text."""
    return boxed_label(text, color=color, size=size, pad=pad, min_size=22, stroke=2.5,
                       fill_opacity=fill_opacity).set_z_index(9)


def make_pair(left_txt, right_txt, color, size=24, pad=0.14):
    """Two enzyme/cofactor blocks snapped together as one complex pair."""
    a = make_block(left_txt, color, size=size, pad=pad)
    b = make_block(right_txt, color, size=size, pad=pad)
    b.next_to(a, RIGHT, buff=0.08)
    g = VGroup(a, b).set_z_index(9)
    g.left_block, g.right_block = a, b
    return g


def build_tan_layer(x0, x1, y0, y1, stud_xs, stud_h=0.34, dividers_on=True):
    """Subendothelial TAN cell layer with protruding tissue factor studs."""
    cell = RoundedRectangle(
        corner_radius=0.14, width=x1 - x0, height=y1 - y0,
        stroke_color=TAN, stroke_width=3.0, fill_color=TAN, fill_opacity=0.16,
    ).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]).set_z_index(2)
    dividers = VGroup()
    if dividers_on:
        n_cells = max(2, int((x1 - x0) / 2.3))
        for k in range(1, n_cells):
            xd = x0 + k * (x1 - x0) / n_cells
            dividers.add(Line([xd, y0 + 0.08, 0], [xd, y1 - 0.08, 0],
                              color=TAN, stroke_width=1.8, stroke_opacity=0.6).set_z_index(2))
    studs = VGroup()
    for sx in stud_xs:
        stem = Line([sx, y1, 0], [sx, y1 + stud_h, 0], color=TAN, stroke_width=5.0).set_z_index(4)
        knob = Circle(radius=0.08, color=TAN, fill_color=TAN, fill_opacity=1.0, stroke_width=0).move_to(
            [sx, y1 + stud_h, 0]).set_z_index(4)
        s = VGroup(stem, knob)
        s.tip = np.array([sx, y1 + stud_h, 0.0])
        studs.add(s)
    g = VGroup(cell, dividers, studs)
    g.cell, g.dividers, g.studs = cell, dividers, studs
    return g


def build_whole_vessel(plug_activated=True, show_mesh=False, mesh_seed=19):
    """Standard whole-vessel layout in [-6.4, 4.4] x [-2.25, 2.35] (~58% frame height)."""
    x0, x1 = -6.4, 4.4
    y_bot, y_top = -0.85, 2.35
    gap_l, gap_r = -1.15, 1.15

    lumen = Rectangle(
        width=x1 - x0, height=y_top - y_bot,
        stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
    ).move_to([(x0 + x1) / 2, (y_bot + y_top) / 2, 0]).set_z_index(0)

    top_line = Line([x0, y_top, 0], [x1, y_top, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
    bot_left = Line([x0, y_bot, 0], [gap_l, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
    bot_right = Line([gap_r, y_bot, 0], [x1, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
    wall_ticks = VGroup()
    for tx in np.arange(-5.6, 4.2, 1.1):
        wall_ticks.add(Line([tx, y_top, 0], [tx, y_top + 0.14, 0], color=WHITE, stroke_width=2.0).set_z_index(5))
        if tx < gap_l - 0.15 or tx > gap_r + 0.15:
            wall_ticks.add(Line([tx, y_bot, 0], [tx, y_bot - 0.14, 0], color=WHITE, stroke_width=2.0).set_z_index(5))

    tan = build_tan_layer(-3.6, 3.6, -2.2, -0.92, stud_xs=[-0.7, 0.0, 0.7], stud_h=0.28)
    # Cover intact left/right TAN flanks with subtle wall backing so blood doesn't touch them
    flank_l = Rectangle(width=gap_l - (-3.6), height=0.12, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to(
        [(-3.6 + gap_l) / 2, y_bot - 0.05, 0]).set_z_index(4)
    flank_r = Rectangle(width=3.6 - gap_r, height=0.12, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to(
        [(gap_r + 3.6) / 2, y_bot - 0.05, 0]).set_z_index(4)

    plug_centers = [(-0.72, -0.68), (0.0, -0.66), (0.72, -0.68), (-0.36, -0.34), (0.36, -0.34)]
    plug = VGroup(*[make_platelet_disc(p, radius=0.36, activated=plug_activated, ticks_out=plug_activated)
                    for p in plug_centers]).set_z_index(6)

    g = VGroup(lumen, tan, flank_l, flank_r, top_line, bot_left, bot_right, wall_ticks, plug)
    g.lumen, g.tan, g.plug = lumen, tan, plug
    g.top_line, g.bot_left, g.bot_right = top_line, bot_left, bot_right
    g.bounds = (x0, x1, y_bot, y_top)
    if show_mesh:
        mesh = build_fibrin_mesh(-1.05, 1.05, -0.82, -0.05, seed=mesh_seed, n_threads=14, cross_links=True)
        g.add(mesh)
        g.mesh = mesh
    return g


def build_fibrin_mesh(x0, x1, y0, y1, seed=19, n_threads=18, cross_links=True):
    """Deterministic WHITE fibrin mesh + optional cross-links."""
    rng = np.random.default_rng(seed)
    threads = VGroup()
    links = VGroup()
    pts_top = []
    pts_bot = []
    for i in range(n_threads):
        xa = rng.uniform(x0, x1)
        xb = np.clip(xa + rng.uniform(-0.9, 0.9), x0, x1)
        ya = y0 + rng.uniform(0.0, 0.35 * (y1 - y0))
        yb = y1 - rng.uniform(0.0, 0.35 * (y1 - y0))
        ln = Line([xa, ya, 0], [xb, yb, 0], color=WHITE, stroke_width=2.8).set_z_index(7)
        threads.add(ln)
        pts_top.append(np.array([(xa + xb) / 2, (ya + yb) / 2, 0.0]))
        if i > 0 and cross_links and i % 2 == 0:
            p1 = pts_top[-1]
            p2 = pts_top[-2]
            if np.linalg.norm(p1 - p2) < 1.2:
                links.add(Line(p1, p2, color=WHITE, stroke_width=3.4).set_z_index(7))
    g = VGroup(threads, links)
    g.threads, g.links = threads, links
    return g


def attach_thrombin_stream(dots, origin_fn, x_bounds, y_bounds, active_fn,
                           vx_fn=None, diff_coeff=0.14, k_fn=None, seed=11,
                           dot_color=MAGENTA, on_hit_fn=None):
    """Computed 2D advection-diffusion + first-order decay updater for MAGENTA thrombin dots."""
    rng = np.random.default_rng(seed)
    for d in dots:
        d._alive = False
        d.set_opacity(0.0)
        d._age = 0.0

    def _u(mob, dt):
        dt_c = min(dt, 0.05)
        sig = np.sqrt(2.0 * diff_coeff * dt_c)
        for d in mob:
            if not d._alive:
                if active_fn() and rng.random() < 0.28:
                    p = origin_fn(rng)
                    d.move_to(p)
                    d._alive = True
                    d._age = 0.0
                    d.set_color(dot_color)
                    d.set_opacity(0.95)
                continue
            x, y = d.get_center()[:2]
            vx = vx_fn(x, y) if vx_fn else 0.7
            vy_drift = 0.25 if vx_fn is None else 0.0
            nx = x + vx * dt_c + rng.normal(0.0, sig)
            ny = y + vy_drift * dt_c + rng.normal(0.0, sig)
            d._age += dt_c
            k = k_fn(nx, ny) if k_fn else 0.25
            p_kill = 1.0 - np.exp(-k * dt_c)
            out = (nx < x_bounds[0] or nx > x_bounds[1] or ny < y_bounds[0] or ny > y_bounds[1])
            if out or rng.random() < p_kill or (on_hit_fn and on_hit_fn(d, nx, ny)):
                d._alive = False
                d.set_opacity(0.0)
            else:
                d.move_to([nx, ny, 0])

    dots.add_updater(_u)
    return dots


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        gauge_val = ValueTracker(0.0)
        gauge = make_gauge(gauge_val)

        # Sliding viewport offset tracker (0 -> -5.5 -> 0) to travel down intact vessel
        shift_x = ValueTracker(0.0)
        x0, x1, y_bot, y_top = -6.4, 4.4, -0.85, 2.35
        lumen = Rectangle(
            width=x1 - x0, height=y_top - y_bot,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
        ).move_to([(x0 + x1) / 2, (y_bot + y_top) / 2, 0]).set_z_index(0)
        top_line = Line([x0, y_top, 0], [x1, y_top, 0], color=WHITE, stroke_width=4.0).set_z_index(5)

        def _sliding_world():
            dx = shift_x.get_value()
            g = VGroup()
            # Intact lower lining segments clipped to [x0, x1]
            gap_l, gap_r = -1.15 + dx, 1.15 + dx
            if gap_l > x0:
                g.add(Line([x0, y_bot, 0], [min(gap_l, x1), y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5))
            if gap_r < x1:
                g.add(Line([max(gap_r, x0), y_bot, 0], [x1, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5))
            # Wall ticks spaced every 1.1 units
            for tx_base in np.arange(-6.0, 12.0, 1.1):
                tx = tx_base + dx
                if x0 + 0.1 < tx < x1 - 0.1:
                    g.add(Line([tx, y_top, 0], [tx, y_top + 0.14, 0], color=WHITE, stroke_width=2.0).set_z_index(5))
                    if tx < gap_l - 0.15 or tx > gap_r + 0.15:
                        g.add(Line([tx, y_bot, 0], [tx, y_bot - 0.14, 0], color=WHITE, stroke_width=2.0).set_z_index(5))
            # TAN subendothelial cell layer and plug (shown when inside viewport)
            tan_l, tan_r = max(x0, -3.6 + dx), min(x1, 3.6 + dx)
            if tan_r - tan_l > 0.4:
                tan = RoundedRectangle(
                    corner_radius=0.12, width=tan_r - tan_l, height=1.28,
                    stroke_color=TAN, stroke_width=3.0, fill_color=TAN, fill_opacity=0.16,
                ).move_to([(tan_l + tan_r) / 2, -1.56, 0]).set_z_index(2)
                g.add(tan)
                for sx_b in (-0.7, 0.0, 0.7):
                    sx = sx_b + dx
                    if x0 + 0.2 < sx < x1 - 0.2:
                        g.add(Line([sx, -0.92, 0], [sx, -0.64, 0], color=TAN, stroke_width=5.0).set_z_index(4))
            for px_b, py_b in [(-0.72, -0.68), (0.0, -0.66), (0.72, -0.68), (-0.36, -0.34), (0.36, -0.34)]:
                px = px_b + dx
                if x0 + 0.4 < px < x1 - 0.4:
                    g.add(Circle(radius=0.36, stroke_color=VIOLET, stroke_width=3.0,
                                 fill_color=VIOLET, fill_opacity=0.45).move_to([px, py_b, 0]).set_z_index(6))
            return g

        sliding = always_redraw(_sliding_world)
        cells = spawn_red_cells(10, x0, x1, y_bot, y_top, seed=7)
        attach_lumen_flow(cells, x0, x1, y_bot, y_top, base_speed=1.35)

        # Flowing pale AMBER clotting proteins (small unlabelled dots drifting untouched)
        rng = np.random.default_rng(3)
        proteins = VGroup(*[
            Dot([rng.uniform(x0 + 0.2, x1 - 0.2), rng.uniform(y_bot + 0.35, y_top - 0.35), 0],
                radius=0.055, color=AMBER).set_opacity(0.85).set_z_index(3)
            for _ in range(14)
        ])
        for p in proteins:
            p._base_y = p.get_center()[1]
            p._tilt = 0.0
        attach_lumen_flow(proteins, x0, x1, y_bot, y_top, base_speed=1.55)

        self.add(lumen, top_line, sliding, cells, proteins, gauge)

        # Ghost kidney patch from Chapter 1
        self.at("a global number")
        tubule1 = RoundedRectangle(corner_radius=0.25, width=1.1, height=0.55, stroke_color=WHITE,
                                   stroke_width=2.5, fill_color=BG, fill_opacity=0.65)
        tubule2 = RoundedRectangle(corner_radius=0.25, width=1.1, height=0.55, stroke_color=WHITE,
                                   stroke_width=2.5, fill_color=BG, fill_opacity=0.65).next_to(tubule1, DOWN, buff=0.45)
        kcell = Ellipse(width=0.55, height=0.28, stroke_color=CYAN, stroke_width=3.0,
                        fill_color=CYAN, fill_opacity=0.35).move_to((tubule1.get_center() + tubule2.get_center()) / 2)
        halo = Circle(radius=0.52, stroke_color=CYAN, stroke_width=2.5).move_to(kcell)
        patch = VGroup(tubule1, tubule2, kcell, halo).move_to([-3.6, 0.75, 0]).set_z_index(11)
        patch.layout_ok = True
        lt_tag = T("last time", size=26, color=CYAN).move_to([-3.6, 2.72, 0]).set_z_index(12)
        self.play(FadeIn(patch), FadeIn(lt_tag), run_time=0.7)

        self.at("a kidney cell")
        self.wait(2.2)
        self.play(FadeOut(patch), FadeOut(lt_tag), run_time=0.6)

        self.at("a cut seals")
        self.play(shift_x.animate.set_value(-5.6), run_time=2.6, rate_func=smooth)
        self.at("flow through every")
        self.wait(1.2)
        self.play(shift_x.animate.set_value(0.0), run_time=1.8, rate_func=smooth)

        self.at("where is the line")
        q_txt = T("Why only here?", size=38, color=WHITE).move_to([-0.9, 3.12, 0]).set_z_index(14)
        self.play(FadeIn(q_txt, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        vessel = build_whole_vessel(plug_activated=False)
        x0, x1, y_bot, y_top = vessel.bounds
        cells = spawn_red_cells(10, x0, x1, y_bot, y_top, seed=7)
        attach_lumen_flow(cells, x0, x1, y_bot, y_top, base_speed=1.35)
        gauge = make_gauge(ValueTracker(0.0))
        q_txt = T("Why only here?", size=38, color=WHITE).move_to([-0.9, 3.12, 0]).set_z_index(14)

        self.add(vessel, cells, gauge, q_txt)
        title = T("Thrombin Needs a Surface", size=44, font=TITLE_FONT, color=WHITE).move_to([-0.9, 3.22, 0]).set_z_index(14)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.12).set_z_index(14)
        self.play(FadeOut(q_txt, run_time=0.45))
        self.play(FadeIn(title, shift=UP * 0.08), GrowFromCenter(rule), run_time=0.7)
        self.finish()


class S02Surface(SpokenScene):
    def construct(self):
        gauge = make_gauge(ValueTracker(0.0))
        title = T("Thrombin Needs a Surface", size=44, font=TITLE_FONT, color=WHITE).move_to([-0.9, 3.22, 0]).set_z_index(14)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.12).set_z_index(14)

        # Zoomed geometry: plug fills ~65% of height, flow + top WHITE lining stay above
        x0, x1 = -6.4, 4.4
        y_bot_flow, y_top_flow = 0.85, 2.75
        lumen = Rectangle(
            width=x1 - x0, height=y_top_flow - y_bot_flow,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
        ).move_to([(x0 + x1) / 2, (y_bot_flow + y_top_flow) / 2, 0]).set_z_index(0)
        top_line = Line([x0, y_top_flow, 0], [x1, y_top_flow, 0], color=WHITE, stroke_width=4.5).set_z_index(5)
        bot_l = Line([x0, -0.35, 0], [-3.4, -0.35, 0], color=WHITE, stroke_width=4.5).set_z_index(5)
        bot_r = Line([2.6, -0.35, 0], [x1, -0.35, 0], color=WHITE, stroke_width=4.5).set_z_index(5)

        tan = build_tan_layer(-4.6, 3.8, -3.15, -2.05, stud_xs=[-1.8, -0.4, 1.0], stud_h=0.28, dividers_on=False)
        cells = spawn_red_cells(8, x0, x1, y_bot_flow + 0.15, y_top_flow - 0.15, seed=13, w=0.82, h=0.34)
        attach_lumen_flow(cells, x0, x1, y_bot_flow + 0.15, y_top_flow - 0.15, base_speed=1.5)

        # Five VIOLET platelet discs packed in the breach, with inward phosphatidylserine marks
        specs = [
            ((-2.0, -1.25), 0.72, np.linspace(0.35 * PI, 0.85 * PI, 5)),
            ((-0.4, -1.35), 0.75, np.linspace(0.25 * PI, 0.75 * PI, 5)),
            ((1.2, -1.25), 0.72, np.linspace(0.15 * PI, 0.65 * PI, 5)),
            ((-1.2, -0.32), 0.72, np.linspace(0.20 * PI, 0.80 * PI, 6)),
            ((0.45, -0.30), 0.74, np.linspace(0.20 * PI, 0.80 * PI, 6)),
        ]
        platelets = VGroup(*[
            make_platelet_disc(pos, radius=rad, activated=False, ticks_out=False, tick_angles=angs)
            for pos, rad, angs in specs
        ]).set_z_index(6)

        self.add(lumen, tan, top_line, bot_l, bot_r, platelets, cells, gauge, title, rule)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.6)

        self.at("it anchored a")
        held_lbl = T("held at the breach", size=28, color=WHITE).move_to([1.6, 3.25, 0]).set_z_index(12)
        arr = Arrow(held_lbl.get_bottom() + DOWN * 0.10 + LEFT * 0.4, [0.55, 0.52, 0],
                    buff=0.05, color=WHITE, stroke_width=3.5, max_tip_length_to_length_ratio=0.14).set_z_index(12)
        self.play(FadeIn(held_lbl), GrowArrow(arr), run_time=0.8)

        self.at("turn their")
        # Rotate inward marks outward 180 deg and light up GOLD rim platelet by platelet
        for p in platelets:
            anims = [p.body.animate.set_stroke(GOLD, 6.0)]
            for seg in p.marks:
                target_end = seg._anchor + 0.18 * seg._out_vec
                new_seg = Line(seg._anchor, target_end, color=GOLD, stroke_width=3.5).set_z_index(7)
                anims.append(Transform(seg, new_seg))
            self.play(*anims, run_time=0.55)

        self.at("procoagulant surface")
        surf_lbl = T("procoagulant\nsurface", size=28, color=GOLD, line_spacing=0.85).move_to([-3.35, 0.44, 0]).set_z_index(12)
        surf_arr = Arrow(surf_lbl.get_right() + RIGHT * 0.08, [-1.82, 0.14, 0],
                         color=GOLD, stroke_width=3.5, buff=0.04, max_tip_length_to_length_ratio=0.22).set_z_index(12)
        self.play(FadeIn(surf_lbl), GrowArrow(surf_arr), run_time=0.6)
        self.finish()


class S03Trickle(SpokenScene):
    def construct(self):
        gauge_val = ValueTracker(0.0)
        gauge = make_gauge(gauge_val)

        x0, x1 = -6.4, 4.4
        y_lumen_bot, y_lumen_top = -0.55, 1.85
        lumen = Rectangle(
            width=x1 - x0, height=y_lumen_top - y_lumen_bot,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
        ).move_to([(x0 + x1) / 2, (y_lumen_bot + y_lumen_top) / 2, 0]).set_z_index(0)

        # Plug with GOLD edge visible at top of frame
        top_plug = VGroup(
            make_platelet_disc((-2.2, 2.55), radius=0.72, activated=True, ticks_out=True,
                               tick_angles=np.linspace(1.15 * PI, 1.85 * PI, 5)),
            make_platelet_disc((-0.7, 2.48), radius=0.74, activated=True, ticks_out=True,
                               tick_angles=np.linspace(1.15 * PI, 1.85 * PI, 5)),
            make_platelet_disc((0.8, 2.55), radius=0.72, activated=True, ticks_out=True,
                               tick_angles=np.linspace(1.15 * PI, 1.85 * PI, 5)),
        ).set_z_index(6)
        top_l = Line([x0, 2.15, 0], [-2.9, 2.15, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        top_r = Line([1.5, 2.15, 0], [x1, 2.15, 0], color=WHITE, stroke_width=4.0).set_z_index(5)

        # TAN layer filling lower half of frame (dividers clear of label)
        tan = build_tan_layer(-4.6, 3.3, -3.2, -0.65, stud_xs=[-2.4, -0.4, 1.6], stud_h=0.45, dividers_on=False)
        # Intact ghost lining initially covering the TAN studs
        ghost_lining = DashedLine([-4.6, -0.05, 0], [3.3, -0.05, 0],
                                  color=WHITE, stroke_width=3.5, dash_length=0.18).set_opacity(0.65).set_z_index(5)

        cells = spawn_red_cells(6, x0, x1, 0.72, y_lumen_top - 0.15, seed=21, w=0.72, h=0.28)
        attach_lumen_flow(cells, x0, x1, 0.72, y_lumen_top - 0.15, base_speed=1.3)

        # Stream of MAGENTA dots active on last sentence
        stream_on = False
        stream_dots = VGroup(*[
            Dot([0.8, -0.4, 0], radius=0.065, color=MAGENTA).set_opacity(0.0).set_z_index(8)
            for _ in range(14)
        ])
        attach_thrombin_stream(
            stream_dots,
            origin_fn=lambda r: np.array([0.85 + r.uniform(-0.15, 0.15), 0.15, 0.0]),
            x_bounds=(-3.5, 3.5),
            y_bounds=(0.05, 1.75),
            active_fn=lambda: stream_on,
            vx_fn=lambda x, y: 0.25,
            diff_coeff=0.08,
            k_fn=lambda x, y: 0.35,
            seed=17,
        )

        self.add(lumen, tan, top_plug, top_l, top_r, ghost_lining, cells, stream_dots, gauge)
        tf_lbl = T("tissue factor", size=28, color=TAN).move_to([-2.4, -1.75, 0]).set_z_index(12)
        self.play(FadeIn(tf_lbl), run_time=0.6)

        self.at("until the wall")
        left_part = Line([-4.6, -0.05, 0], [-3.4, -0.05, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        right_part = Line([2.2, -0.05, 0], [3.3, -0.05, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        self.play(FadeOut(ghost_lining), FadeIn(left_part), FadeIn(right_part), run_time=0.8)

        self.at("it binds factor")
        b_viia = make_block("VIIa", AMBER, size=24).move_to([-4.2, 0.35, 0])
        self.play(FadeIn(b_viia), run_time=0.35)
        self.play(b_viia.animate.move_to(tan.studs[0].tip + UP * 0.26), run_time=0.9)

        self.at("cuts factor 10")
        b_x = make_block("X", WHITE, size=24).move_to([-1.2, 1.05, 0])
        b_ix = make_block("IX", WHITE, size=24).move_to([-5.2, 0.35, 0])
        self.play(FadeIn(b_x), FadeIn(b_ix), run_time=0.35)
        self.play(
            b_x.animate.move_to(tan.studs[0].tip + np.array([0.85, 0.35, 0])),
            b_ix.animate.move_to(tan.studs[0].tip + np.array([-0.85, 0.55, 0])),
            run_time=0.75,
        )
        b_xa = make_block("Xa", ORANGE, size=24).move_to(b_x.get_center())
        b_ixa = make_block("IXa", GREEN, size=24).move_to(b_ix.get_center())
        self.play(swap(b_x, b_xa, run_time=0.4), swap(b_ix, b_ixa, run_time=0.4))

        self.at("factor 10", nth=1)
        b_va = make_block("Va", ORANGE, size=24).move_to([1.05, -0.30, 0])
        self.play(FadeIn(b_va), run_time=0.4)
        self.play(b_xa.animate.next_to(b_va, LEFT, buff=0.08), run_time=0.75)

        self.at("a little thrombin")
        stream_on = True
        trickle_lbl = T("trickle", size=26, color=MAGENTA).move_to([4.35, gauge.y0 + 0.12, 0]).set_z_index(14)
        self.play(gauge_val.animate.set_value(TRICKLE_LEVEL), FadeIn(trickle_lbl), run_time=0.9)
        self.finish()


class S04Signal(SpokenScene):
    def construct(self):
        gauge_val = ValueTracker(TRICKLE_LEVEL)
        gauge = make_gauge(gauge_val)
        trickle_lbl = T("trickle", size=26, color=MAGENTA).move_to([4.35, gauge.y0 + 0.12, 0]).set_z_index(14)

        x0, x1 = -6.4, 4.4
        lumen = Rectangle(
            width=x1 - x0, height=2.3,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
        ).move_to([(x0 + x1) / 2, 0.5, 0]).set_z_index(0)

        # Plug at top: 1 already GOLD, 2 flanking still plain VIOLET until signal lands
        p_mid = make_platelet_disc((-0.7, 2.42), radius=0.68, activated=True, ticks_out=True,
                                   tick_angles=np.linspace(1.15 * PI, 1.85 * PI, 5))
        p_l = make_platelet_disc((-2.1, 2.52), radius=0.66, activated=False, ticks_out=False,
                                 tick_angles=np.linspace(1.15 * PI, 1.85 * PI, 4))
        p_r = make_platelet_disc((0.7, 2.52), radius=0.66, activated=False, ticks_out=False,
                                 tick_angles=np.linspace(1.15 * PI, 1.85 * PI, 4))
        top_plug = VGroup(p_l, p_mid, p_r).set_z_index(6)
        top_l = Line([x0, 2.15, 0], [-2.85, 2.15, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        top_r = Line([1.45, 2.15, 0], [x1, 2.15, 0], color=WHITE, stroke_width=4.0).set_z_index(5)

        tan = build_tan_layer(-4.6, 3.3, -3.2, -0.65, stud_xs=[-2.4, -0.4, 1.6], stud_h=0.45, dividers_on=False)
        left_part = Line([-4.6, -0.05, 0], [-3.4, -0.05, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        right_part = Line([2.2, -0.05, 0], [3.3, -0.05, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        tf_lbl = T("tissue factor", size=28, color=TAN).move_to([-2.4, -1.75, 0]).set_z_index(12)

        b_viia = make_block("VIIa", AMBER, size=24).move_to(tan.studs[0].tip + UP * 0.26)
        b_va = make_block("Va", ORANGE, size=24).move_to([1.05, -0.30, 0])
        b_xa = make_block("Xa", ORANGE, size=24).next_to(b_va, LEFT, buff=0.08)

        # Keep red cells strictly in middle flow lane [0.65, 1.20] away from lower & upper blocks
        cells = spawn_red_cells(5, x0, x1, 0.65, 1.20, seed=29, w=0.64, h=0.22)
        attach_lumen_flow(cells, x0, x1, 0.65, 1.20, base_speed=1.2)

        stream_on = True
        signal_rise = False
        stream_dots = VGroup(*[
            Dot([0.85, 0.1 + 0.1 * i, 0], radius=0.068, color=MAGENTA).set_opacity(0.9).set_z_index(8)
            for i in range(6)
        ])

        def _signal_u(mob, dt):
            for i, d in enumerate(mob):
                x, y = d.get_center()[:2]
                if signal_rise:
                    tx = -2.1 + 1.4 * (i % 3)
                    d.move_to([x + (tx - x) * min(1.0, 2.2 * dt), min(1.82, y + 1.45 * dt), 0])
                elif stream_on:
                    ny = y + 0.65 * dt
                    if ny > 1.25:
                        ny = -0.05
                    d.move_to([0.85 + 0.15 * np.sin(3 * ny + i), ny, 0])

        stream_dots.add_updater(_signal_u)
        self.add(lumen, tan, top_plug, top_l, top_r, left_part, right_part, tf_lbl,
                 b_viia, b_va, b_xa, cells, stream_dots, gauge, trickle_lbl)

        self.at("nowhere near enough")
        brace = BraceBetweenPoints(
            [gauge.cx - gauge.w / 2 - 0.12, gauge.y0 + 0.35, 0],
            [gauge.cx - gauge.w / 2 - 0.12, gauge.y1, 0],
            direction=LEFT, color=WHITE,
        ).set_z_index(14)
        not_en = T("not enough", size=26, color=WHITE).next_to(brace, LEFT, buff=0.14).set_z_index(14)
        self.play(FadeIn(brace), FadeIn(not_en), run_time=0.7)

        self.at("pathway inhibitor")
        tfpi = make_block("TFPI", CYAN, size=24).move_to([-1.5, 1.05, 0])
        self.play(FadeIn(tfpi), run_time=0.35)
        self.play(tfpi.animate.next_to(b_viia, RIGHT, buff=0.12), run_time=0.8)

        self.at("shuts that assembly")
        stream_on = False
        b_viia.layout_ok = True
        b_xa.layout_ok = True
        b_va.layout_ok = True
        self.play(
            FadeOut(brace), FadeOut(not_en),
            b_viia.animate.set_opacity(0.32),
            b_xa.animate.set_opacity(0.32),
            b_va.animate.set_opacity(0.32),
            run_time=0.75,
        )

        self.at("is a signal")
        signal_rise = True
        self.wait(0.8)

        self.at("activates platelets")
        anims = []
        for p in (p_l, p_r):
            anims.append(p.body.animate.set_stroke(GOLD, 6.0))
            for seg in p.marks:
                new_seg = Line(seg._anchor, seg._anchor + 0.18 * seg._out_vec,
                               color=GOLD, stroke_width=3.5).set_z_index(7)
                anims.append(Transform(seg, new_seg))
        self.play(*anims, run_time=0.75)

        self.at("cuts factors 5")
        b_v = make_block("V", WHITE, size=24).move_to([-3.2, 1.48, 0])
        b_viii = make_block("VIII", WHITE, size=24).move_to([-0.6, 1.48, 0])
        b_xi = make_block("XI", WHITE, size=24).move_to([2.0, 1.48, 0])
        self.play(FadeIn(b_v), FadeIn(b_viii), FadeIn(b_xi), run_time=0.35)

        b_va2 = make_block("Va", ORANGE, size=24).move_to([-3.2, 1.48, 0])
        b_viiia = make_block("VIIIa", GREEN, size=24).move_to([-0.6, 1.48, 0])
        carrier = make_block("carrier", AMBER, size=24, pad=0.10).move_to([0.55, 1.48, 0])
        b_xia = make_block("XIa", GOLD, size=24).move_to([2.0, 1.48, 0])

        self.play(swap(b_v, b_va2, run_time=0.45))
        self.play(swap(b_viii, b_viiia, run_time=0.45), FadeIn(carrier, shift=DOWN * 0.12, run_time=0.45))
        self.play(swap(b_xi, b_xia, run_time=0.45))
        self.play(carrier.animate.shift(RIGHT * 1.1).set_opacity(0.0), run_time=0.5)
        self.finish()


class S05Burst(SpokenScene):
    def construct(self):
        gauge_val = ValueTracker(TRICKLE_LEVEL)
        gauge = make_gauge(gauge_val, show_trickle_tick=True)
        trickle_lbl = T("trickle", size=24, color=WHITE).move_to([
            gauge.cx - gauge.w / 2 - 0.72, gauge.trickle_tick.get_y(), 0]).set_z_index(14)

        x0, x1 = -6.4, 4.4
        lumen = Rectangle(
            width=x1 - x0, height=3.8,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
        ).move_to([(x0 + x1) / 2, 1.3, 0]).set_z_index(0)

        # Shift plug left so x=[1.5..4.6] is clear for the split bar + labels
        plug = VGroup(
            make_platelet_disc((-4.1, -1.05), radius=0.78, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
            make_platelet_disc((-2.5, -1.00), radius=0.80, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
            make_platelet_disc((-0.9, -1.00), radius=0.80, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
            make_platelet_disc((0.7, -1.05), radius=0.76, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
        ).set_z_index(6)
        gold_edge = Line([-4.95, -0.18, 0], [1.45, -0.18, 0], color=GOLD, stroke_width=6.0).set_z_index(7)
        tan_small = build_tan_layer(-4.9, 1.4, -3.25, -2.35, stud_xs=[-2.7, -0.7], stud_h=0.22, dividers_on=False)

        # Red cells strictly in upper band [2.25, 3.05], away from blocks below
        cells = spawn_red_cells(7, x0, x1, 2.25, 3.05, seed=31, w=0.72, h=0.26)
        attach_lumen_flow(cells, x0, x1, 2.25, 3.05, base_speed=1.35)

        plume_on = False
        plume_dots = VGroup(*[
            Dot([0.1, 0.72, 0], radius=0.072, color=MAGENTA).set_opacity(0.0).set_z_index(8)
            for _ in range(28)
        ])
        attach_thrombin_stream(
            plume_dots,
            origin_fn=lambda r: np.array([-0.1 + r.uniform(-0.35, 0.35), 0.72, 0.0]),
            x_bounds=(-4.5, 1.15),
            y_bounds=(0.62, 2.45),
            active_fn=lambda: plume_on,
            vx_fn=lambda x, y: 0.45,
            diff_coeff=0.22,
            k_fn=lambda x, y: 0.24,
            seed=37,
        )

        self.add(lumen, tan_small, plug, gold_edge, cells, plume_dots, gauge, trickle_lbl)

        self.at("assembles on")
        b_ixa = make_block("IXa", GREEN, size=24).move_to([-3.4, -2.0, 0])
        b_viiia = make_block("VIIIa", GREEN, size=24).move_to([-2.2, 1.65, 0])
        b_va = make_block("Va", ORANGE, size=24).move_to([0.55, 1.65, 0])
        self.play(FadeIn(b_ixa), FadeIn(b_viiia), FadeIn(b_va), run_time=0.45)

        green_pair_target = np.array([-3.1, 0.25, 0.0])
        orange_pair_target = np.array([-0.1, 0.25, 0.0])
        self.play(
            b_ixa.animate.move_to(green_pair_target + LEFT * 0.52),
            b_viiia.animate.move_to(green_pair_target + RIGHT * 0.52),
            b_va.animate.move_to(orange_pair_target + RIGHT * 0.52),
            run_time=1.0,
        )

        self.at("factor 9 with")
        b_xa = make_block("Xa", ORANGE, size=24).move_to(green_pair_target + RIGHT * 1.45)
        self.play(FadeIn(b_xa), run_time=0.35)
        self.play(b_xa.animate.move_to(orange_pair_target + LEFT * 0.52), run_time=0.75)

        self.at("10 with 5")
        proth = make_block("prothrombin", AMBER, size=24).move_to([-0.1, 1.75, 0])
        self.play(FadeIn(proth), run_time=0.3)
        self.play(proth.animate.move_to(orange_pair_target + UP * 0.72), run_time=0.65)
        plume_on = True
        self.play(
            FadeOut(proth, run_time=0.35),
            gauge_val.animate(run_time=2.5, rate_func=smooth).set_value(BURST_LEVEL),
        )

        self.at("usual estimate")
        bx = 4.35
        by0, by1 = gauge.y0, gauge.y1
        bh = by1 - by0
        tan_h = bh * TRICKLE_LEVEL
        plt_h = bh * (1.0 - TRICKLE_LEVEL)
        bar_tan = Rectangle(width=0.34, height=tan_h, stroke_color=TAN, stroke_width=2.0,
                            fill_color=TAN, fill_opacity=0.85).move_to([bx, by0 + tan_h / 2, 0]).set_z_index(13)
        bar_plt = Rectangle(width=0.34, height=plt_h, stroke_color=GOLD, stroke_width=2.0,
                            fill_color=GOLD, fill_opacity=0.75).move_to([bx, by0 + tan_h + plt_h / 2, 0]).set_z_index(13)
        lbl_tan = T("on the tan cells", size=24, color=TAN).next_to(bar_tan, LEFT, buff=0.40).set_z_index(14)
        lbl_plt = T("on platelets\n(>90%)", size=26, color=GOLD, line_spacing=0.85).move_to([2.3, 1.15, 0]).set_z_index(14)
        plt_arr = Arrow(lbl_plt.get_right() + RIGHT * 0.10, [bx - 0.22, 1.15, 0],
                        color=GOLD, stroke_width=2.5, buff=0.04, max_tip_length_to_length_ratio=0.18).set_z_index(14)
        est_tag = T("usual\nestimate", size=24, color=WHITE, line_spacing=0.85).move_to([bx, by0 - 0.50, 0]).set_z_index(14)
        self.play(FadeOut(trickle_lbl), run_time=0.35)
        self.play(
            FadeIn(bar_tan), FadeIn(bar_plt), FadeIn(lbl_tan), FadeIn(lbl_plt), FadeIn(plt_arr), FadeIn(est_tag),
            run_time=0.85,
        )
        self.finish()


class S06Idea(SpokenScene):
    def construct(self):
        vessel = build_whole_vessel(plug_activated=True)
        x0, x1, y_bot, y_top = vessel.bounds
        # Red cells stay in upper half of lumen so gp/op at y=0.45 stay clear
        cells = spawn_red_cells(10, x0, x1, 1.25, y_top, seed=7)
        attach_lumen_flow(cells, x0, x1, 1.25, y_top, base_speed=1.35)
        gauge = make_gauge(ValueTracker(BURST_LEVEL), show_trickle_tick=True)

        gp = make_pair("IXa", "VIIIa", GREEN, size=22, pad=0.12).move_to([-0.92, 0.54, 0])
        op = make_pair("Xa", "Va", ORANGE, size=22, pad=0.12).move_to([0.92, 0.54, 0])

        plume_dots = VGroup(*[
            Dot([0.0, 0.7, 0], radius=0.06, color=MAGENTA).set_opacity(0.0).set_z_index(8)
            for _ in range(18)
        ])
        attach_thrombin_stream(
            plume_dots,
            origin_fn=lambda r: np.array([0.8 + r.uniform(-0.25, 0.25), 0.95, 0.0]),
            x_bounds=(-3.0, 4.0),
            y_bounds=(0.85, 2.15),
            active_fn=lambda: True,
            vx_fn=lambda x, y: 0.65,
            diff_coeff=0.14,
            k_fn=lambda x, y: 0.3,
            seed=41,
        )

        self.add(vessel, cells, gp, op, plume_dots, gauge)

        self.at("on surfaces")
        head = T("Made on a surface", size=36, color=WHITE).move_to([-0.9, 3.12, 0]).set_z_index(14)
        self.play(FadeIn(head), run_time=0.6)

        self.at("not in solution")
        # Ghost copies in midstream (below red cells at y=1.25..2.35) drift apart and wash downstream
        g_ixa = make_block("IXa", GREEN, size=22, pad=0.10, fill_opacity=0.08).move_to([-4.5, 1.04, 0])
        g_viiia = make_block("VIIIa", GREEN, size=22, pad=0.10, fill_opacity=0.08).next_to(g_ixa, RIGHT, buff=0.08)
        g_xa = make_block("Xa", ORANGE, size=22, pad=0.10, fill_opacity=0.08).move_to([-2.7, 1.04, 0])
        g_va = make_block("Va", ORANGE, size=22, pad=0.10, fill_opacity=0.08).next_to(g_xa, RIGHT, buff=0.08)
        ghosts = VGroup(g_ixa, g_viiia, g_xa, g_va)
        for m in ghosts:
            m.box.set_stroke(opacity=0.55)
            m.label.set_opacity(0.85)
        self.play(FadeIn(ghosts), run_time=0.4)
        self.play(
            g_ixa.animate.shift(RIGHT * 4.0 + UP * 0.25).set_opacity(0.0),
            g_viiia.animate.shift(RIGHT * 5.2 + DOWN * 0.25).set_opacity(0.0),
            g_xa.animate.shift(RIGHT * 4.5 + UP * 0.20).set_opacity(0.0),
            g_va.animate.shift(RIGHT * 5.4 + DOWN * 0.25).set_opacity(0.0),
            run_time=1.8,
        )
        self.remove(ghosts)

        self.at("where a surface")
        ring = SurroundingRectangle(VGroup(gp, op), corner_radius=0.14, color=GOLD, stroke_width=4.0, buff=0.14).set_z_index(10)
        bracket = BraceBetweenPoints([-1.2, -2.32, 0], [1.2, -2.32, 0], direction=DOWN, color=GOLD).set_z_index(12)
        surf_lbl = T("surfaces", size=28, color=GOLD).next_to(bracket, DOWN, buff=0.14).set_z_index(12)
        self.play(Create(ring), FadeIn(bracket), FadeIn(surf_lbl), run_time=0.7)
        self.play(FadeOut(ring), run_time=0.5)
        self.finish()


class S07Fibrin(SpokenScene):
    def construct(self):
        gauge = make_gauge(ValueTracker(BURST_LEVEL), show_trickle_tick=True)

        x0, x1 = -6.4, 4.4
        lumen = Rectangle(
            width=x1 - x0, height=3.8,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
        ).move_to([(x0 + x1) / 2, 1.3, 0]).set_z_index(0)

        plug = VGroup(
            make_platelet_disc((-2.4, -1.05), radius=0.76, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
            make_platelet_disc((-0.7, -1.00), radius=0.78, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
            make_platelet_disc((1.0, -1.00), radius=0.78, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
            make_platelet_disc((2.6, -1.05), radius=0.74, activated=True, ticks_out=True,
                               tick_angles=np.linspace(0.25 * PI, 0.75 * PI, 5)),
        ).set_z_index(5)
        tan_small = build_tan_layer(-3.4, 3.2, -3.50, -2.68, stud_xs=[-1.0, 1.0], stud_h=0.22, dividers_on=False)
        cells = spawn_red_cells(7, x0, x1, 2.05, 3.05, seed=43, w=0.72, h=0.26)
        attach_lumen_flow(cells, x0, x1, 2.05, 3.05, base_speed=1.35)

        plume_dots = VGroup(*[
            Dot([0.0, 0.2, 0], radius=0.068, color=MAGENTA).set_opacity(0.0).set_z_index(8)
            for _ in range(20)
        ])
        attach_thrombin_stream(
            plume_dots,
            origin_fn=lambda r: np.array([r.uniform(-2.0, 2.0), 0.1, 0.0]),
            x_bounds=(-3.8, 4.0),
            y_bounds=(-0.4, 2.2),
            active_fn=lambda: True,
            vx_fn=lambda x, y: 0.4,
            diff_coeff=0.18,
            k_fn=lambda x, y: 0.28,
            seed=47,
        )

        mesh = build_fibrin_mesh(-2.9, 3.0, -1.55, 0.15, seed=19, n_threads=20, cross_links=True)
        self.add(lumen, tan_small, plug, cells, plume_dots, gauge)

        self.at("cuts fibrinogen")
        fib1 = make_block("fibrinogen", AMBER, size=24).move_to([-4.2, 1.35, 0])
        fib2 = make_block("fibrinogen", AMBER, size=24).move_to([2.4, 1.35, 0])
        self.play(FadeIn(fib1), FadeIn(fib2), run_time=0.4)
        self.play(fib1.animate.move_to([-1.2, 0.45, 0]), fib2.animate.move_to([1.2, 0.45, 0]), run_time=0.7)

        self.at("a mesh through")
        self.play(
            FadeOut(fib1, run_time=0.3), FadeOut(fib2, run_time=0.3),
            Create(mesh.threads, run_time=1.4),
        )

        self.at("activates factor 13")
        f13 = make_block("XIII", WHITE, size=24).move_to([-3.6, 0.65, 0])
        self.play(FadeIn(f13), run_time=0.35)
        self.play(f13.animate.move_to([0.0, 0.35, 0]), run_time=0.65)
        self.play(Create(mesh.links), FadeOut(f13), run_time=0.9)

        self.at("against arterial")
        ghost_bulge = mesh.threads.copy().set_stroke(WHITE, 2.0, opacity=0.35)
        self.add(ghost_bulge)
        p_arrow = Arrow([-0.1, 1.45, 0], [-0.1, 0.35, 0], color=RED, stroke_width=4.5, buff=0.05).set_z_index(12)
        self.play(
            GrowArrow(p_arrow),
            ghost_bulge.animate.shift(DOWN * 0.28).scale(1.06),
            mesh.animate.shift(DOWN * 0.04),
            run_time=0.65,
        )
        fib_lbl = T("fibrin, cross-linked", size=28, color=WHITE).move_to([-0.1, -2.08, 0]).set_z_index(12)
        self.play(FadeOut(ghost_bulge), FadeOut(p_arrow), mesh.animate.shift(UP * 0.04), FadeIn(fib_lbl), run_time=0.55)
        self.finish()


def _build_reach_backdrop(show_far_mark=True, speed_mult=1.0, show_sugar=True, slow_pause=False):
    """Shared left-plug + long-intact-lining world for s08, s09, s10, s11."""
    x0, x1 = -6.4, 4.4
    y_bot, y_top = -0.85, 2.35
    lumen = Rectangle(
        width=x1 - x0, height=y_top - y_bot,
        stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
    ).move_to([(x0 + x1) / 2, (y_bot + y_top) / 2, 0]).set_z_index(0)
    top_line = Line([x0, y_top, 0], [x1, y_top, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
    bot_left = Line([x0, y_bot, 0], [-5.8, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
    bot_right = Line([-3.8, y_bot, 0], [x1, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
    tan = build_tan_layer(-6.0, -3.85, -2.15, -0.92, stud_xs=[-5.1, -4.4], stud_h=0.26, dividers_on=False)

    plug = VGroup(
        make_platelet_disc((-5.3, -0.64), radius=0.38, activated=True, ticks_out=True),
        make_platelet_disc((-4.6, -0.60), radius=0.40, activated=True, ticks_out=True),
        make_platelet_disc((-4.0, -0.64), radius=0.38, activated=True, ticks_out=True),
        make_platelet_disc((-4.7, -0.28), radius=0.36, activated=True, ticks_out=True),
    ).set_z_index(6)
    mesh = build_fibrin_mesh(-5.6, -3.8, -0.80, -0.05, seed=19, n_threads=12, cross_links=True)

    sugar = VGroup()
    if show_sugar:
        for sx in np.arange(-3.65, 4.35, 0.25):
            sugar.add(Line([sx, y_bot, 0], [sx, y_bot + 0.16, 0], color=CYAN, stroke_width=2.8).set_z_index(6))

    ruler_y = -1.35
    ruler = Line([-3.8, ruler_y, 0], [3.8, ruler_y, 0], color=WHITE, stroke_width=3.0).set_z_index(10)
    near_tick = Line([-3.15, ruler_y - 0.15, 0], [-3.15, ruler_y + 0.15, 0], color=GOLD, stroke_width=4.5).set_z_index(11)
    far_tick = Line([3.2, ruler_y - 0.15, 0], [3.2, ruler_y + 0.15, 0], color=WHITE, stroke_width=4.0).set_z_index(11)
    ruler_grp = VGroup(ruler, near_tick)
    if show_far_mark:
        ruler_grp.add(far_tick)

    # Keep red cells in upper lumen [0.75, 2.2] so lower-wall chips stay clear
    cells = spawn_red_cells(9, x0, x1, 0.75, y_top - 0.1, seed=53)
    st = ValueTracker(speed_mult)
    attach_lumen_flow(cells, x0, x1, 0.75, y_top - 0.1, speed_tracker=st, base_speed=0.45 if slow_pause else 1.35)

    g = VGroup(lumen, tan, top_line, bot_left, bot_right, plug, mesh, sugar, ruler_grp, cells)
    g.sugar, g.ruler, g.near_tick, g.far_tick = sugar, ruler, near_tick, far_tick
    g.cells, g.speed_tracker, g.bounds = cells, st, (x0, x1, y_bot, y_top)
    return g


class S08Predict(SpokenScene):
    def construct(self):
        bd = _build_reach_backdrop(show_far_mark=False, show_sugar=False)
        # Hide ruler initially until question
        bd.near_tick.set_opacity(0.0)
        bd.ruler.set_opacity(0.0)
        gauge = make_gauge(ValueTracker(BURST_LEVEL), show_trickle_tick=True)

        sugar_fringe = VGroup(*[
            Line([sx, -0.85, 0], [sx, -0.69, 0], color=CYAN, stroke_width=2.8).set_z_index(6)
            for sx in np.arange(-3.65, 4.35, 0.25)
        ])
        sugar_active = False

        dots = VGroup(*[
            Dot([-3.8, -0.2, 0], radius=0.065, color=MAGENTA).set_opacity(0.0).set_z_index(8)
            for _ in range(26)
        ])
        attach_thrombin_stream(
            dots,
            origin_fn=lambda r: np.array([-3.9, r.uniform(-0.65, -0.05), 0.0]),
            x_bounds=(-4.2, 4.1),
            y_bounds=(-0.82, 2.1),
            active_fn=lambda: True,
            vx_fn=lambda x, y: 1.55,
            diff_coeff=0.14,
            k_fn=lambda x, y: (3.2 if (sugar_active and x > -3.5) else 0.45),
            seed=59,
        )

        self.add(bd, dots, gauge)
        self.at("drift downstream")
        self.wait(1.4)

        self.at("antithrombin destroys")
        at_block = make_block("antithrombin", CYAN, size=24).move_to([0.2, 0.20, 0])
        self.play(FadeIn(at_block), run_time=0.5)
        self.play(at_block.animate.move_to([-1.2, 0.05, 0]), run_time=1.0)

        self.at("a surface sugar")
        sugar_active = True
        sugar_lbl = T("surface sugar", size=26, color=CYAN).move_to([1.6, -2.05, 0]).set_z_index(12)
        speed_chip = make_block("×100 to ×1,000", CYAN, size=24).move_to([1.6, -0.25, 0])
        self.play(Create(sugar_fringe), FadeIn(sugar_lbl), run_time=0.9)
        self.play(at_block.animate.move_to([-1.8, -0.45, 0]), FadeIn(speed_chip), run_time=0.8)

        self.at("how far does")
        bd.ruler.set_opacity(1.0)
        bd.near_tick.set_opacity(1.0)
        far_tick = Line([3.2, -1.50, 0], [3.2, -1.20, 0], color=WHITE, stroke_width=4.0).set_z_index(11)
        q_txt = T("How far does thrombin get?", size=36, color=WHITE).move_to([-0.9, 3.12, 0]).set_z_index(14)
        self.play(
            FadeOut(at_block), FadeOut(speed_chip), FadeOut(sugar_lbl),
            Create(bd.ruler), FadeIn(bd.near_tick), FadeIn(far_tick), FadeIn(q_txt),
            run_time=0.8,
        )
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "How far does thrombin get?"
    CARD = {"y": 3.12, "color": WHITE, "size": 36}
    RING_AT = (5.8, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        bd = _build_reach_backdrop(show_far_mark=True, show_sugar=True, slow_pause=True)
        gauge = make_gauge(ValueTracker(BURST_LEVEL), show_trickle_tick=True)
        # A few MAGENTA dots hovering slowly just outside the plug
        dots = VGroup(*[
            Dot([-3.65 + 0.14 * i, -0.55 + 0.18 * (i % 3), 0], radius=0.06, color=MAGENTA).set_z_index(8)
            for i in range(6)
        ])

        def _hover(mob, dt):
            for k, d in enumerate(mob):
                x, y = d.get_center()[:2]
                nx = x + 0.12 * dt
                if nx > -3.1:
                    nx = -3.75
                d.move_to([nx, -0.55 + 0.18 * (k % 3) + 0.03 * np.sin(2.5 * nx + k), 0])

        dots.add_updater(_hover)
        return VGroup(bd, dots, gauge)


class S10Reach(SpokenScene):
    def construct(self):
        bd = _build_reach_backdrop(show_far_mark=True, show_sugar=True, slow_pause=False)
        gauge = make_gauge(ValueTracker(BURST_LEVEL), show_trickle_tick=True)
        q_txt = T("How far does thrombin get?", size=36, color=WHITE).move_to([-0.9, 3.12, 0]).set_z_index(14)

        # Computed reach lambda = sqrt(D / k) in scene units (1 unit ~ 4 um with sugar; ~40 um open plasma)
        reach_w = ValueTracker(0.65)
        sugar_on = True

        def _band():
            w = reach_w.get_value()
            # Computed exponential decay profile C(x) = exp(-(x - x0)/lambda) rendered as banded strip
            strip = VGroup()
            n_slices = 14
            for i in range(n_slices):
                f0, f1 = i / n_slices, (i + 1) / n_slices
                x_left = -3.8 + f0 * w
                sw = w / n_slices
                op = 0.42 * np.exp(-2.2 * f0)
                strip.add(Rectangle(
                    width=sw + 0.005, height=3.12, stroke_width=0,
                    fill_color=MAGENTA, fill_opacity=float(op),
                ).move_to([x_left + sw / 2, 0.75, 0]).set_z_index(1))
            return strip

        band = always_redraw(_band)

        dots = VGroup(*[
            Dot([-3.8, -0.2, 0], radius=0.062, color=MAGENTA).set_opacity(0.0).set_z_index(8)
            for _ in range(28)
        ])
        attach_thrombin_stream(
            dots,
            origin_fn=lambda r: np.array([-3.85, r.uniform(-0.70, -0.05), 0.0]),
            x_bounds=(-4.1, 4.1),
            y_bounds=(-0.82, 2.2),
            active_fn=lambda: True,
            vx_fn=lambda x, y: 1.4 * bd.speed_tracker.get_value(),
            diff_coeff=0.14,
            k_fn=lambda x, y: (4.8 if sugar_on else 0.45),
            seed=61,
        )

        self.add(bd, band, dots, gauge, q_txt)

        self.at("1 to 5")
        near_lbl = T("1 to 5 µm", size=28, color=GOLD).next_to(bd.near_tick, DOWN, buff=0.18).align_to(bd.near_tick, LEFT).set_z_index(12)
        self.play(FadeOut(q_txt), FadeOut(bd.far_tick), FadeIn(near_lbl), run_time=0.6)

        self.at("few cell thicknesses")
        # Show lining thickness reference matching the shaded 1-5 um band width (0.65 units)
        wall_cell = Rectangle(width=0.65, height=0.22, stroke_color=WHITE, stroke_width=2.5,
                              fill_color=WHITE, fill_opacity=0.2).move_to([-3.475, -0.96, 0]).set_z_index(11)
        thick_lbl = T("1 to a few cell thicknesses", size=26, color=WHITE).move_to([-0.9, 3.05, 0]).set_z_index(14)
        self.play(FadeIn(wall_cell), FadeIn(thick_lbl), run_time=0.7)

        self.at("order of magnitude")
        est_tag = T("order-of-magnitude estimate", size=26, color=WHITE).move_to([-0.2, -2.85, 0]).set_z_index(14)
        self.play(FadeIn(est_tag), run_time=0.6)

        self.at("in open plasma")
        sugar_on = False
        tens_lbl = T("tens of µm", size=28, color=MAGENTA).move_to([0.2, -1.88, 0]).set_z_index(12)
        self.play(
            bd.sugar.animate.set_opacity(0.0),
            reach_w.animate.set_value(5.6),
            swap(near_lbl, tens_lbl, run_time=0.45),
            FadeOut(thick_lbl, run_time=0.45),
            run_time=1.3,
        )
        self.wait(0.8)
        sugar_on = True
        near_lbl2 = T("1 to 5 µm", size=28, color=GOLD).next_to(bd.near_tick, DOWN, buff=0.18).align_to(bd.near_tick, LEFT).set_z_index(12)
        thick_lbl2 = T("1 to a few cell thicknesses", size=26, color=WHITE).move_to([-0.9, 3.05, 0]).set_z_index(14)
        self.play(
            bd.sugar.animate.set_opacity(1.0),
            reach_w.animate.set_value(0.65),
            swap(tens_lbl, near_lbl2, run_time=0.45),
            FadeIn(thick_lbl2, run_time=0.45),
            run_time=0.75,
        )

        self.at("flow only shortens")
        self.play(
            bd.speed_tracker.animate.set_value(2.4),
            reach_w.animate.set_value(0.42),
            run_time=0.9,
        )
        self.finish()


class S11Brakes(SpokenScene):
    def construct(self):
        x0, x1 = -6.4, 4.4
        y_bot, y_top = -0.85, 2.35
        lumen = Rectangle(
            width=x1 - x0, height=y_top - y_bot,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.11,
        ).move_to([(x0 + x1) / 2, (y_bot + y_top) / 2, 0]).set_z_index(0)
        top_line = Line([x0, y_top, 0], [x1, y_top, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        bot_left = Line([x0, y_bot, 0], [-5.8, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        bot_right = Line([-3.5, y_bot, 0], [x1, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        tan = build_tan_layer(-6.0, -3.3, -2.15, -0.92, stud_xs=[-5.0, -4.2], stud_h=0.26, dividers_on=False)
        plug = VGroup(
            make_platelet_disc((-5.3, -0.62), radius=0.38, activated=True, ticks_out=True),
            make_platelet_disc((-4.5, -0.58), radius=0.40, activated=True, ticks_out=True),
            make_platelet_disc((-3.8, -0.62), radius=0.38, activated=True, ticks_out=True),
            make_platelet_disc((-4.5, -0.25), radius=0.36, activated=True, ticks_out=True),
        ).set_z_index(6)
        mesh = build_fibrin_mesh(-5.6, -3.6, -0.80, 0.05, seed=19, n_threads=14, cross_links=True)

        gp = make_pair("IXa", "VIIIa", GREEN, size=22, pad=0.10).move_to([-5.25, 0.48, 0])
        op = make_pair("Xa", "Va", ORANGE, size=22, pad=0.10).move_to([-3.45, 0.48, 0])

        gauge_val = ValueTracker(BURST_LEVEL)
        gauge = make_gauge(gauge_val, show_trickle_tick=True)

        cells = spawn_red_cells(8, x0, x1, 0.95, y_top - 0.1, seed=67)
        attach_lumen_flow(cells, x0, x1, 0.95, y_top - 0.1, base_speed=1.3)

        plume_strength = ValueTracker(1.0)
        plume_dots = VGroup(*[
            Dot([-4.0, 0.65, 0], radius=0.06, color=MAGENTA).set_opacity(0.0).set_z_index(8)
            for _ in range(20)
        ])
        attach_thrombin_stream(
            plume_dots,
            origin_fn=lambda r: np.array([-3.6 + r.uniform(-0.35, 0.35), 0.92, 0.0]),
            x_bounds=(-5.8, 3.8),
            y_bounds=(0.82, 2.2),
            active_fn=lambda: plume_strength.get_value() > 0.15,
            vx_fn=lambda x, y: 1.0,
            diff_coeff=0.14,
            k_fn=lambda x, y: 0.65 / max(0.25, plume_strength.get_value()),
            seed=71,
        )

        self.add(lumen, tan, top_line, bot_left, bot_right, plug, mesh, gp, op, cells, plume_dots, gauge)

        self.at("thrombomodulin")
        tm_cup = Arc(radius=0.22, start_angle=PI, angle=PI, arc_center=[-1.3, -0.63, 0],
                     color=CYAN, stroke_width=5.0).set_z_index(9)
        tm_lbl = T("thrombomodulin", size=26, color=CYAN).move_to([-1.3, -1.35, 0]).set_z_index(12)
        t_dot = Dot([-2.4, 0.48, 0], radius=0.11, color=MAGENTA).set_z_index(10)
        self.play(Create(tm_cup), FadeIn(tm_lbl), FadeIn(t_dot), run_time=0.6)
        self.play(t_dot.animate.move_to([-1.3, -0.63, 0]), run_time=0.8)
        self.play(t_dot.animate.set_color(CYAN), run_time=0.4)

        self.at("protein c")
        pc = make_block("protein C", CYAN, size=24).move_to([1.0, 0.42, 0])
        self.play(FadeIn(pc), run_time=0.35)
        self.play(pc.animate.move_to([-1.3, -0.05, 0]), run_time=0.65)

        self.at("inactivates factors")
        # Protein C travels beside plug complexes (clear of Va/Xa) and knocks VIIIa and Va off
        self.play(pc.animate.move_to([-1.85, 0.48, 0]), run_time=0.75)
        plume_strength.set_value(0.22)
        self.play(
            gp.right_block.animate.shift(UP * 0.9 + RIGHT * 1.4).set_opacity(0.0),
            op.right_block.animate.shift(UP * 0.9 + RIGHT * 1.4).set_opacity(0.0),
            FadeOut(pc),
            gauge_val.animate.set_value(POST_APC_LEVEL),
            run_time=1.0,
        )

        self.at("and nitric oxide")
        puff1 = Circle(radius=0.18, stroke_color=CYAN, stroke_width=2.5, fill_color=CYAN, fill_opacity=0.25).move_to([1.9, -0.55, 0]).set_z_index(7)
        puff2 = Circle(radius=0.18, stroke_color=CYAN, stroke_width=2.5, fill_color=CYAN, fill_opacity=0.25).move_to([3.1, -0.55, 0]).set_z_index(7)
        pno_lbl = T("prostacyclin + NO", size=26, color=CYAN).move_to([2.4, -1.35, 0]).set_z_index(12)
        passing_plt = make_platelet_disc((0.5, 0.45), radius=0.28, activated=False).set_z_index(7)
        self.play(FadeIn(puff1), FadeIn(puff2), FadeIn(pno_lbl), FadeIn(passing_plt), run_time=0.5)
        self.play(
            puff1.animate.move_to([2.1, 0.2, 0]).scale(1.4).set_opacity(0.0),
            puff2.animate.move_to([3.3, 0.2, 0]).scale(1.4).set_opacity(0.0),
            passing_plt.animate.shift(RIGHT * 3.2),
            run_time=1.4,
        )
        self.remove(puff1, puff2, passing_plt)

        self.at("and later")
        days = ValueTracker(0.0)
        clock = counter("+{:.0f} h", days, at=[-0.9, 3.12, 0], size=32, color=WHITE).set_z_index(14)
        plasmin = make_block("plasmin", CYAN, size=24).move_to([-0.8, 0.35, 0])
        healed_line = Line([-5.8, y_bot, 0], [-3.5, y_bot, 0], color=WHITE, stroke_width=4.0).set_z_index(5)
        self.add(clock)
        self.play(FadeIn(plasmin), days.animate.set_value(48), run_time=1.0)
        plume_strength.set_value(0.0)
        self.play(
            plasmin.animate.move_to([-4.6, -0.25, 0]),
            FadeOut(mesh), FadeOut(gp.left_block), FadeOut(op.left_block),
            FadeOut(plug), FadeOut(tan.studs), Create(healed_line),
            gauge_val.animate.set_value(0.05),
            run_time=1.2,
        )
        self.play(FadeOut(plasmin), run_time=0.35)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        vessel = build_whole_vessel(plug_activated=True, show_mesh=True)
        x0, x1, y_bot, y_top = vessel.bounds
        cells = spawn_red_cells(10, x0, x1, 1.15, y_top - 0.1, seed=7)
        attach_lumen_flow(cells, x0, x1, 1.15, y_top - 0.1, base_speed=1.35)

        gp = make_pair("IXa", "VIIIa", GREEN, size=22, pad=0.10).move_to([-0.92, 0.54, 0])
        op = make_pair("Xa", "Va", ORANGE, size=22, pad=0.10).move_to([0.92, 0.54, 0])
        gauge_val = ValueTracker(TRICKLE_LEVEL)
        gauge = make_gauge(gauge_val, show_trickle_tick=True)

        self.add(vessel, cells, gp, op, gauge)

        self.at("the plug puts")
        s1_ring = SurroundingRectangle(vessel.plug, corner_radius=0.14, color=GOLD, stroke_width=4.0, buff=0.08).set_z_index(11)
        s1_lbl = T("1. plug surface", size=28, color=GOLD).move_to([-2.4, 2.95, 0]).set_z_index(14)
        self.play(Create(s1_ring), FadeIn(s1_lbl), run_time=0.7)

        self.at("the trickle switches")
        s2_ring = SurroundingRectangle(vessel.tan.studs, corner_radius=0.1, color=TAN, stroke_width=3.5, buff=0.1).set_z_index(11)
        s2_lbl = T("2. trickle", size=28, color=TAN).move_to([0.2, 2.95, 0]).set_z_index(14)
        self.play(FadeOut(s1_ring), Create(s2_ring), FadeIn(s2_lbl), run_time=0.7)

        self.at("the burst happens")
        s3_ring = SurroundingRectangle(VGroup(gp, op), corner_radius=0.12, color=MAGENTA, stroke_width=4.0, buff=0.14).set_z_index(11)
        s3_lbl = T("3. burst", size=28, color=MAGENTA).move_to([2.5, 2.95, 0]).set_z_index(14)
        self.play(
            FadeOut(s2_ring), Create(s3_ring), FadeIn(s3_lbl),
            gauge_val.animate.set_value(BURST_LEVEL),
            run_time=0.9,
        )

        self.at("your finger clots")
        self.play(
            FadeOut(vessel), FadeOut(cells), FadeOut(gp), FadeOut(op), FadeOut(gauge),
            FadeOut(s3_ring), FadeOut(s1_lbl), FadeOut(s2_lbl), FadeOut(s3_lbl),
            run_time=0.4,
        )

        tp = TwoPanel("finger: cut vessel", "lung: intact vessel", colors=(GOLD, CYAN), top=3.2, bottom=-2.3)

        # Left panel: cut vessel + plug + mesh + full gauge (cleanly inside l_box)
        l_box = Rectangle(width=4.5, height=2.2, stroke_color=WHITE, stroke_width=3.0,
                          fill_color=AMBER, fill_opacity=0.11)
        l_plug = VGroup(*[Circle(radius=0.20, stroke_color=GOLD, stroke_width=3.5,
                                 fill_color=VIOLET, fill_opacity=0.5).move_to([-0.28 + 0.28 * i, -0.86, 0])
                          for i in range(3)])
        l_mesh = build_fibrin_mesh(-0.5, 0.5, -0.98, -0.50, seed=7, n_threads=8, cross_links=True)
        l_gauge = Rectangle(width=0.28, height=1.8, stroke_color=WHITE, stroke_width=2.0,
                            fill_color=MAGENTA, fill_opacity=0.88).move_to([2.7, 0.0, 0])
        l_cells = spawn_red_cells(5, -2.0, 2.0, -0.45, 0.9, seed=79, w=0.52, h=0.22)
        left_pic = VGroup(l_box, l_plug, l_mesh, l_gauge, l_cells)
        tp.put(left_pic, "left")

        # Right panel: intact vessel + empty gauge + unpaired blocks + free red cells
        r_box = Rectangle(width=4.5, height=2.2, stroke_color=WHITE, stroke_width=3.0,
                          fill_color=AMBER, fill_opacity=0.11)
        r_lining = Line([-2.25, -1.1, 0], [2.25, -1.1, 0], color=CYAN, stroke_width=4.5)
        r_gauge = Rectangle(width=0.28, height=1.8, stroke_color=WHITE, stroke_width=2.0,
                            fill_color=BG, fill_opacity=0.9).move_to([2.7, 0.0, 0])
        r_b1 = make_block("IXa", GREEN, size=24, pad=0.10).move_to([-1.3, 0.58, 0])
        r_b2 = make_block("VIIIa", GREEN, size=24, pad=0.10).move_to([0.0, 0.58, 0])
        r_b3 = make_block("Xa", ORANGE, size=24, pad=0.10).move_to([1.3, 0.58, 0])
        r_cells = spawn_red_cells(5, -2.0, 2.0, -0.75, -0.05, seed=83, w=0.52, h=0.22)
        right_pic = VGroup(r_box, r_lining, r_gauge, r_b1, r_b2, r_b3, r_cells)
        tp.put(right_pic, "right")

        # Gentle continuous flow inside both panels
        lc = tp.left_frame.get_center()
        rc = tp.right_frame.get_center()
        attach_lumen_flow(l_cells, lc[0] - 2.2, lc[0] + 1.5, lc[1] - 0.45, lc[1] + 0.8, base_speed=0.9)
        attach_lumen_flow(r_cells, rc[0] - 2.2, rc[0] + 1.5, rc[1] - 0.75, rc[1] - 0.05, base_speed=1.1)

        cap = caption("same proteins, both panels", size=30, color=WHITE, y=-2.95)
        self.play(FadeIn(tp), FadeIn(left_pic), FadeIn(right_pic), FadeIn(cap), run_time=0.9)
        self.finish()


class S13End(EndCard):
    LINE = "A clot grows only where a surface holds the enzymes."
