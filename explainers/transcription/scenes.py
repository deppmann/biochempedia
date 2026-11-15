"""
Film: "The Strand Is Chosen at the Start" (Lesson: Transcription: From DNA to RNA)

COLOUR MAP (one colour per concept across the whole film):
- Template DNA: BLUE (#58C4DD)
- Coding DNA:   GOLD (#D4A843)
- RNA:          GREEN (#83C167)
- Promoter:     TEAL (#3FB8C0)
- Polymerase:   TEXT (#E8EAF0, white)
- Unassigned / neutral duplex DNA: TEXT (#E8EAF0, white)

THE ONE CARRIED WORLD:
One schematic 12-bp double-stranded DNA duplex (from the lesson's sequence:
top 5'-ACGTTTCATGGA-3' / bottom 3'-TGCAAAGTACCT-5') with nucleotide tiles,
outer sugar-phosphate backbones, base-pair ticks, and 5'/3' end labels,
acted on by a white open-jaw RNA polymerase clamp, directional teal promoter
blocks, and a growing green RNA strand computed from the polymerase's position.

WHAT CHANGES ON SCREEN (and what it is computed from):
- s01_hook:     Base pairs build and pulse along the 12-bp duplex; the white polymerase
                drifts in, flips orientation twice, and leaves opposing oscillating
                question arrows above and below both unassigned strands.
- s02_title:    (silent) The 12-bp duplex compresses into the gold title rule under
                'The Strand Is Chosen at the Start', then expands back into the duplex.
- s03_promoter: A directional teal promoter block grows from the duplex; polymerase flips
                to match its arrow, locks at +1, and opens a cosine-computed bubble whose
                lower strand bends into the active site (blue) while the upper turns gold.
- s04_growth:   A position tracker x_poly drives the polymerase rightward; DNA unzips
                ahead and rezips behind while green RNA tiles dock only at the glowing
                3' end and the fixed 5' tail peels out cleanly through the gap.
- s05_predict:  The duplex resets to neutral; the promoter flips to a leftward teal
                arrow with a continuously orbiting pulse, flanked by two possible
                polymerase choices and the question card between them.
- s06_pause:    (silent) Holds the question, gently brightens the reversed promoter, bobs
                both polymerase choices, and runs the 4.5 s countdown ring.
- s07_reverse:  Selects the leftward polymerase; keeping the duplex fixed in place, the
                top strand bends into the active site as the new blue template, bottom
                becomes gold coding, and polymerase drives leftward building 5'->3' RNA.
- s08_coding:   Zooms the active 8-bp stretch: green RNA aligns with gold coding to show
                exact sequence match with U<->T highlight, then moves beneath blue
                template with base-pair ticks and opposite 5'->3' antiparallel arrows.
- s09_bare:     Fades promoter and RNA and drains strand colours to white as a template?
                badge jumps between strands; re-introduces the RNA strip to match gold
                coding and pair with blue template.
- s10_bubble:   Full-width moving bubble driven continuously by x_poly: pairs unzip ahead,
                rejoin behind, and green RNA curves out through its own exit path.
- s11_checks:   Transforms into three large connected checkpoint panels where bottom DNA
                swaps to 5'->3', RNA U swaps to T against coding, and RNA pairs
                antiparallel to template; a large green pulse sweeps into a travel arrow.
- s12_scope:    While the computed bubble and RNA synthesis continue smoothly, the teal
                promoter morphs through varied schematic silhouettes, locking +1 and
                both direction arrows at the end.
- s13_end:      (silent) Standard EndCard with the take-home line.
"""
from bp_parts import *

# ------------------------------------------------------------------ shared sequence & geometry
# First 12 bp of the lesson's 18-bp duplex (lesson_for_context.mdx):
# top (5'->3' left-to-right):    A C G T T T C A T G G A
# bottom (3'->5' left-to-right): T G C A A A G T A C C T
TOP_BASES = list("ACGTTTCATGGA")
BOT_BASES = list("TGCAAAGTACCT")
COMP_RNA = {"A": "U", "T": "A", "C": "G", "G": "C"}

N_BP = len(TOP_BASES)
PITCH = 0.84
XS = np.array([-4.62 + i * PITCH for i in range(N_BP)], dtype=float)
TILE_W = 0.60
TILE_H = 0.48
BUBBLE_HALF_W = 2.45
BUBBLE_LIFT = 1.24


def smoothstep(u):
    u = float(np.clip(u, 0.0, 1.0))
    return u * u * (3.0 - 2.0 * u)


def bubble_offset(x, x_poly, open_frac):
    """Computed raised-cosine strand separation around x_poly."""
    if open_frac <= 1e-4:
        return 0.0
    d = abs(x - x_poly) / BUBBLE_HALF_W
    if d >= 1.0:
        return 0.0
    return float(open_frac * BUBBLE_LIFT * 0.5 * (1.0 + np.cos(np.pi * d)))


def make_tile(letter, color=TEXT, w=TILE_W, h=TILE_H, font_size=24, fill_opacity=0.18):
    box = RoundedRectangle(
        corner_radius=0.10,
        width=w,
        height=h,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    lab = T(letter, size=font_size, color=color, weight=BOLD)
    lab.move_to(box)
    g = VGroup(box, lab)
    g.box = box
    g.lab = lab
    g.set_z_index(2)
    return g


def build_duplex(
    y0=0.0,
    top_color=TEXT,
    bot_color=TEXT,
    x_poly_tr=None,
    open_tr=None,
    show_ends=True,
):
    """Build the 12-bp schematic DNA duplex with computed bubble updaters."""
    top_tiles = VGroup(*[make_tile(b, top_color) for b in TOP_BASES])
    bot_tiles = VGroup(*[make_tile(b, bot_color) for b in BOT_BASES])
    rungs = VGroup()
    for i, x in enumerate(XS):
        top_tiles[i].move_to([x, y0 + 0.38, 0])
        bot_tiles[i].move_to([x, y0 - 0.38, 0])
        rung = Line([x, y0 + 0.11, 0], [x, y0 - 0.11, 0], color=TEXT, stroke_width=2.5)
        rung.set_z_index(1)
        rungs.add(rung)

    top_bb = VMobject(stroke_color=top_color, stroke_width=3.8, fill_opacity=0).set_z_index(1)
    bot_bb = VMobject(stroke_color=bot_color, stroke_width=3.8, fill_opacity=0).set_z_index(1)

    sample_xs = np.linspace(XS[0] - 0.45, XS[-1] + 0.45, 72)

    def _bb_env(x, xp, op):
        return max(
            bubble_offset(x, xp, op),
            bubble_offset(x - 0.30, xp, op) - 0.04,
            bubble_offset(x + 0.30, xp, op) - 0.04,
        )

    top_bb.set_points_smoothly([np.array([x, y0 + 0.78, 0]) for x in sample_xs])
    bot_bb.set_points_smoothly([np.array([x, y0 - 0.78, 0]) for x in sample_xs])

    ends = VGroup()
    if show_ends:
        t5 = M("5′", size=28, color=top_color).move_to([XS[0] - 0.76, y0 + 0.46, 0])
        t3 = M("3′", size=28, color=top_color).move_to([XS[-1] + 0.76, y0 + 0.46, 0])
        b3 = M("3′", size=28, color=bot_color).move_to([XS[0] - 0.76, y0 - 0.46, 0])
        b5 = M("5′", size=28, color=bot_color).move_to([XS[-1] + 0.76, y0 - 0.46, 0])
        ends.add(t5, t3, b3, b5)
        ends.set_z_index(3)

    if x_poly_tr is not None and open_tr is not None:
        for i, x in enumerate(XS):
            def _make_top_u(xi):
                return lambda m: m.set_y(y0 + 0.38 + bubble_offset(xi, x_poly_tr.get_value(), open_tr.get_value()))

            def _make_bot_u(xi):
                return lambda m: m.set_y(y0 - 0.38 - bubble_offset(xi, x_poly_tr.get_value(), open_tr.get_value()))

            def _make_rung_u(xi):
                def _u(m):
                    off = bubble_offset(xi, x_poly_tr.get_value(), open_tr.get_value())
                    op = max(0.0, 1.0 - off / 0.14)
                    m.set_stroke(opacity=op)
                return _u

            top_tiles[i].add_updater(_make_top_u(x))
            bot_tiles[i].add_updater(_make_bot_u(x))
            rungs[i].add_updater(_make_rung_u(x))

        def _bb_top_u(m):
            xp, op = x_poly_tr.get_value(), open_tr.get_value()
            pts = [np.array([x, y0 + 0.78 + _bb_env(x, xp, op), 0]) for x in sample_xs]
            m.set_points_smoothly(pts)

        def _bb_bot_u(m):
            xp, op = x_poly_tr.get_value(), open_tr.get_value()
            pts = [np.array([x, y0 - 0.78 - _bb_env(x, xp, op), 0]) for x in sample_xs]
            m.set_points_smoothly(pts)

        top_bb.add_updater(_bb_top_u)
        bot_bb.add_updater(_bb_bot_u)

    g = VGroup(top_bb, bot_bb, rungs, top_tiles, bot_tiles, ends)
    g.top_tiles = top_tiles
    g.bot_tiles = bot_tiles
    g.rungs = rungs
    g.top_bb = top_bb
    g.bot_bb = bot_bb
    g.ends = ends
    return g


def build_polymerase(direction=1, template_side="bottom", with_label=True):
    """Open-jaw white polymerase schematic clamp: DNA passes cleanly through open sides."""
    w, h = 3.90, 4.44
    body = RoundedRectangle(
        corner_radius=0.45,
        width=w,
        height=h,
        stroke_width=0,
        fill_color=TEXT,
        fill_opacity=0.11,
    ).set_z_index(0)

    upper_jaw = VMobject(stroke_color=TEXT, stroke_width=4.0, fill_opacity=0).set_z_index(3)
    upper_jaw.set_points_smoothly([
        np.array([-1.95, 2.24, 0]),
        np.array([-1.15, 2.38, 0]),
        np.array([0.0, 2.42, 0]),
        np.array([1.15, 2.38, 0]),
        np.array([1.95, 2.24, 0]),
    ])
    lower_jaw = VMobject(stroke_color=TEXT, stroke_width=4.0, fill_opacity=0).set_z_index(3)
    lower_jaw.set_points_smoothly([
        np.array([-1.95, -2.24, 0]),
        np.array([-1.15, -2.38, 0]),
        np.array([0.0, -2.42, 0]),
        np.array([1.15, -2.38, 0]),
        np.array([1.95, -2.24, 0]),
    ])

    slot_y = -1.30 if template_side == "bottom" else 1.30
    slot = RoundedRectangle(
        corner_radius=0.20,
        width=2.65,
        height=1.24,
        stroke_width=0,
        fill_color=BLUE,
        fill_opacity=0.10,
    ).move_to([0, slot_y, 0]).set_z_index(0)

    arr_dir = RIGHT if direction > 0 else LEFT
    dir_arrow = Arrow(
        -0.72 * arr_dir,
        0.72 * arr_dir,
        buff=0,
        color=TEXT,
        stroke_width=4.5,
        max_tip_length_to_length_ratio=0.28,
    ).move_to([0, 2.53, 0]).set_z_index(4)

    g = VGroup(body, slot, upper_jaw, lower_jaw, dir_arrow)
    g.body = body
    g.slot = slot
    g.upper_jaw = upper_jaw
    g.lower_jaw = lower_jaw
    g.dir_arrow = dir_arrow
    if with_label:
        lbl = T("polymerase", size=28, color=TEXT).move_to([0, 3.06, 0]).set_z_index(4)
        g.add(lbl)
        g.lbl = lbl
    else:
        g.lbl = None
    return g


def place_poly(poly, x, y=0.0):
    """Position polymerase by its body center so dir_arrow never pulls the jaws downward."""
    c = poly.body.get_center()
    return poly.shift([x - c[0], y - c[1], 0])


def build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=3.02, shape="arrow", tick_bottom=2.30):
    """Directional teal promoter block placed cleanly above the bubble/RNA lane with +1 marker.

    All shape variants share an identical 9-vertex perimeter ordering so Transform morphs cleanly.
    When tick_bottom >= 2.25 (polymerase active underneath), start_tick stays cleanly above the
    polymerase arrow (y=2.53) and below the +1 label/glow instead of overlapping outlines.
    """
    xl, xr = x_start, x_end
    if direction > 0:
        tip = xr + 0.35
        xs_top = [xr, xr - 0.45, xr - 0.72, xl + 0.72, xl + 0.45, xl]
        if shape == "twin":
            ys_top = [y + 0.46, y + 0.46, y + 0.28, y + 0.28, y + 0.46, y + 0.46]
        elif shape == "saddle":
            ys_top = [y + 0.46, y + 0.34, y + 0.26, y + 0.26, y + 0.34, y + 0.46]
        else:
            ys_top = [y + 0.34] * 6
        pts = [[xl, y - 0.34, 0], [xr, y - 0.34, 0], [tip, y, 0]] + [
            [xt, yt, 0] for xt, yt in zip(xs_top, ys_top)
        ]
        plus_x = tip + 0.30
    else:
        tip = xl - 0.35
        xs_top = [xl, xl + 0.45, xl + 0.72, xr - 0.72, xr - 0.45, xr]
        ys_top = [y + 0.34] * 6
        pts = [[xr, y - 0.34, 0], [xl, y - 0.34, 0], [tip, y, 0]] + [
            [xt, yt, 0] for xt, yt in zip(xs_top, ys_top)
        ]
        plus_x = tip - 0.30

    poly = Polygon(*pts, color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.22).set_z_index(2)
    lbl = T("promoter", size=26, color=TEXT).move_to([(x_start + x_end) / 2, y, 0]).set_z_index(4)
    if tick_bottom >= 2.25:
        start_tick = DashedLine([plus_x, y + 0.08, 0], [plus_x, y - 0.26, 0], color=TEAL, stroke_width=2.5, dash_length=0.09).set_z_index(2)
    else:
        start_tick = DashedLine([plus_x, y - 0.40, 0], [plus_x, tick_bottom, 0], color=TEAL, stroke_width=2.5, dash_length=0.10).set_z_index(1)
    plus_lbl = M("+1", size=24, color=TEAL).move_to([plus_x, y + 0.41, 0]).set_z_index(4)
    g = VGroup(poly, lbl, start_tick, plus_lbl)
    g.poly = poly
    g.lbl = lbl
    g.start_tick = start_tick
    g.plus_lbl = plus_lbl
    return g


def glide_and_show(scene, xp_tr, target_x, total_t, *anims, anim_t=0.45):
    """Glide xp_tr at constant linear speed over total_t while completing label fades within anim_t."""
    t_anim = min(anim_t, max(0.15, total_t * 0.6))
    x0 = xp_tr.get_value()
    xm = x0 + (target_x - x0) * (t_anim / max(total_t, 1e-4))
    scene.play(*anims, xp_tr.animate.set_value(xm), run_time=t_anim, rate_func=linear)
    rem_t = total_t - t_anim
    if rem_t > 0.03:
        scene.play(xp_tr.animate.set_value(target_x), run_time=rem_t, rate_func=linear)


def build_rna_strip(indices, direction=1, x_poly_tr=None, y0=0.0, template_side="bottom", duplex=None, show_5_prime=False):
    """Computed green RNA tiles: dock only at 3' end inside active site, peel cleanly through inter-tile gap."""
    ordered = list(indices) if direction > 0 else list(reversed(indices))
    tiles = VGroup()
    pairs = VGroup()
    paired_y = y0 - 0.44 if template_side == "bottom" else y0 + 0.44
    exit_y = y0 + 1.84 if template_side == "bottom" else y0 - 1.84
    y_off = 0.35 if template_side == "bottom" else -0.35
    peel_start = 1.28
    peel_span = 0.015

    for k, bp_i in enumerate(ordered):
        xi = XS[bp_i]
        tmpl_base = BOT_BASES[bp_i] if template_side == "bottom" else TOP_BASES[bp_i]
        rna_base = COMP_RNA[tmpl_base]
        tile = make_tile(rna_base, GREEN, w=TILE_W, h=TILE_H, font_size=24, fill_opacity=0.20)
        tile.move_to([xi, paired_y, 0])
        tile.set_z_index(3)

        pbar = Line([xi, paired_y, 0], [xi, paired_y - 0.2, 0], color=GREEN, stroke_width=3.0).set_z_index(2)

        def _make_tile_u(xi_val):
            def _u(m):
                xp = x_poly_tr.get_value()
                prog = (xp - xi_val) if direction > 0 else (xi_val - xp)
                if prog < -0.22:
                    m.box.set_stroke(opacity=0.0)
                    m.box.set_fill(opacity=0.0)
                    m.lab.set_opacity(0.0)
                    return
                vis = smoothstep((prog + 0.22) / 0.30)
                m.box.set_stroke(opacity=vis)
                m.box.set_fill(opacity=0.20 * vis)
                m.lab.set_opacity(vis)
                peel = smoothstep((prog - peel_start) / peel_span)
                yy = paired_y + peel * (exit_y - paired_y)
                m.move_to([xi_val, yy, 0])
            return _u

        def _make_bar_u(xi_val, tile_ref, bp_idx):
            def _u(m):
                xp = x_poly_tr.get_value()
                prog = (xp - xi_val) if direction > 0 else (xi_val - xp)
                peel = smoothstep((prog - peel_start) / peel_span)
                if prog < -0.10 or peel > 0.04:
                    m.set_stroke(opacity=0.0)
                    return
                if duplex is not None:
                    tmpl_tile = duplex.bot_tiles[bp_idx] if template_side == "bottom" else duplex.top_tiles[bp_idx]
                    tmpl_cy = tmpl_tile.get_center()[1]
                else:
                    tmpl_cy = y0 - 0.38 - bubble_offset(xi_val, xp, 1.0) if template_side == "bottom" else y0 + 0.38 + bubble_offset(xi_val, xp, 1.0)
                rna_cy = tile_ref.get_center()[1]
                half_h = TILE_H / 2.0 + 0.07
                if template_side == "bottom":
                    y_lo, y_hi = tmpl_cy + half_h, rna_cy - half_h
                else:
                    y_lo, y_hi = rna_cy + half_h, tmpl_cy - half_h
                if y_hi - y_lo < 0.08:
                    m.set_stroke(opacity=0.0)
                    return
                fade_in = smoothstep((prog + 0.10) / 0.22)
                fade_out = 1.0 - smoothstep((prog - 1.06) / 0.20)
                op = min(fade_in, fade_out)
                m.put_start_and_end_on([xi_val, y_lo, 0], [xi_val, y_hi, 0])
                m.set_stroke(opacity=op)
            return _u

        tile.add_updater(_make_tile_u(xi))
        pbar.add_updater(_make_bar_u(xi, tile, bp_i))
        tiles.add(tile)
        pairs.add(pbar)

    # Backbone connecting visible RNA tiles: stays strictly outside tile boxes (y_off = +/-0.38)
    # and routes any bubble-to-exit transition vertically through the inter-tile midpoint x_mid.
    bb = VMobject(stroke_color=GREEN, stroke_width=3.5, fill_opacity=0).set_z_index(2)

    def _bb_u(m):
        xp = x_poly_tr.get_value()
        vis_pts = []
        for idx, tile in enumerate(tiles):
            xi_val = XS[ordered[idx]]
            prog = (xp - xi_val) if direction > 0 else (xi_val - xp)
            if prog >= -0.05:
                c = tile.get_center()
                vis_pts.append((c[0], c[1] + y_off))
        if len(vis_pts) < 2:
            m.set_stroke(opacity=0.0)
            return

        poly_pts = []
        for j, (x0, y_a) in enumerate(vis_pts):
            poly_pts.append(np.array([x0, y_a, 0.0]))
            if j + 1 < len(vis_pts):
                x1, y_b = vis_pts[j + 1]
                if abs(y_b - y_a) > 0.015 and abs(x1 - x0) > 0.3:
                    xm = 0.5 * (x0 + x1)
                    sgn = float(np.sign(x0 - xm))
                    # Hold flat outside tile x0 until inside inter-tile gap [xm - 0.03, xm + 0.03]
                    poly_pts.append(np.array([xm + sgn * 0.03, y_a, 0.0]))
                    for s in np.linspace(0.0, 1.0, 7)[1:-1]:
                        sm = smoothstep(s)
                        xs_step = xm + sgn * 0.03 * (1.0 - 2.0 * sm)
                        ys_step = y_a + (y_b - y_a) * sm
                        poly_pts.append(np.array([xs_step, ys_step, 0.0]))
                    poly_pts.append(np.array([xm - sgn * 0.03, y_b, 0.0]))
        m.set_stroke(opacity=1.0)
        m.set_points_as_corners(poly_pts)

    bb.add_updater(_bb_u)

    # Outer rounded halo around the active 3' tile + 3' label in open bubble center
    tip_ring = RoundedRectangle(
        corner_radius=0.14,
        width=TILE_W + 0.14,
        height=TILE_H + 0.14,
        color=GREEN,
        stroke_width=3.5,
        fill_opacity=0,
    ).set_z_index(4)
    tip_lbl = M("3′", size=24, color=GREEN).set_z_index(4)

    def _tip_u(m):
        xp = x_poly_tr.get_value()
        active_idx = None
        for idx in range(len(tiles)):
            xi_val = XS[ordered[idx]]
            prog = (xp - xi_val) if direction > 0 else (xi_val - xp)
            if prog >= -0.08:
                active_idx = idx
        if active_idx is None:
            tip_ring.set_stroke(opacity=0.0)
            tip_lbl.set_opacity(0.0)
            return
        active = tiles[active_idx]
        tip_ring.set_stroke(opacity=1.0)
        tip_lbl.set_opacity(1.0)
        tip_ring.move_to(active.get_center())
        v_dir = UP if template_side == "bottom" else DOWN
        tip_lbl.move_to(active.get_center() + v_dir * 0.62 + direction * RIGHT * 0.04)

    tip_group = VGroup(tip_ring, tip_lbl)
    tip_group.add_updater(_tip_u)

    # Update order MUST run tiles BEFORE pairs/bb/tip_group so bb reads current frame tile positions!
    bb.set_z_index(1)
    pairs.set_z_index(2)
    tiles.set_z_index(3)
    g = VGroup(tiles, pairs, bb, tip_group)
    if show_5_prime:
        end5 = M("5′", size=24, color=GREEN).set_z_index(4)

        def _end5_u(m):
            xp = x_poly_tr.get_value()
            x0 = XS[ordered[0]]
            prog0 = (xp - x0) if direction > 0 else (x0 - xp)
            peel0 = smoothstep((prog0 - peel_start) / peel_span)
            if peel0 < 0.96:
                m.set_opacity(0.0)
            else:
                m.set_opacity(1.0)
                c0 = tiles[0].get_center()
                m.move_to(c0 + (-direction * RIGHT) * 0.56)

        end5.add_updater(_end5_u)
        g.add(end5)
        g.end5 = end5

    g.tiles = tiles
    g.pairs = pairs
    g.bb = bb
    g.tip = tip_group
    g.tip_ring = tip_ring
    g.tip_lbl = tip_lbl
    g.update()
    return g


# ------------------------------------------------------------------ Scene 1: Hook
class S01Hook(SpokenScene):
    def construct(self):
        duplex = build_duplex(y0=0.0, top_color=TEXT, bot_color=TEXT, show_ends=True)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(tag)
        self.play(Create(duplex.top_bb), Create(duplex.bot_bb), FadeIn(duplex.ends), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(t, shift=DOWN * 0.08) for t in duplex.top_tiles], lag_ratio=0.05),
            LaggedStart(*[FadeIn(t, shift=UP * 0.08) for t in duplex.bot_tiles], lag_ratio=0.05),
            Create(duplex.rungs),
            run_time=1.0,
        )

        # Complementary pulse along base pairs
        self.at("complementary information")
        self.play(
            LaggedStart(
                *[Indicate(VGroup(duplex.top_tiles[i], duplex.bot_tiles[i], duplex.rungs[i]), color=TEAL, scale_factor=1.08)
                  for i in range(N_BP)],
                lag_ratio=0.10,
            ),
            run_time=2.5,
        )

        # Question header & polymerase drifts in smoothly from right side
        self.at("How does a cell choose")
        q_head = T("Which strand does polymerase read?", size=34, color=GOLD).move_to([0, 3.28, 0])
        poly = build_polymerase(direction=1, template_side="bottom", with_label=True)
        poly.slot.set_opacity(0.0)
        poly.scale(0.80)
        poly.move_to([7.6, 0.25, 0])
        self.add(poly)
        self.play(
            FadeIn(q_head, shift=DOWN * 0.15),
            poly.animate.move_to([4.6, 0.25, 0]),
            run_time=2.8,
            rate_func=smooth,
        )

        self.at("Watch the same polymerase")
        self.play(poly.animate.move_to([0.0, 0.25, 0]), run_time=2.3, rate_func=smooth)

        self.at("with no promoter")
        no_prom = chip("no promoter marked", color=TEAL, size=26).move_to([-3.8, -2.55, 0])
        self.play(FadeIn(no_prom), poly.animate.shift(LEFT * 0.25), run_time=0.9)
        self.play(poly.animate.shift(RIGHT * 0.25), run_time=0.9)

        # Flips orientation twice
        self.at("It could face either way")
        poly_l = build_polymerase(direction=-1, template_side="top", with_label=True).scale(0.80).move_to([0, 0.25, 0])
        poly_l.slot.set_opacity(0.0)
        poly_r = build_polymerase(direction=1, template_side="bottom", with_label=True).scale(0.80).move_to([0, 0.25, 0])
        poly_r.slot.set_opacity(0.0)
        self.play(Transform(poly, poly_l), run_time=0.6)
        self.play(Transform(poly, poly_r), run_time=0.6)

        # Neutral unassigned opposing moving question arrows (no gold/blue colour claim yet)
        self.at("so these base pairs")
        t_osc = ValueTracker(0.0)
        top_q = VGroup(
            Arrow(LEFT * 1.1, RIGHT * 1.1, color=TEAL, stroke_width=5),
            T("?  read this way?", size=26, color=TEXT),
        ).arrange(RIGHT, buff=0.22).move_to([0, 1.55, 0])
        bot_q = VGroup(
            T("?  or this way?", size=26, color=TEXT),
            Arrow(RIGHT * 1.1, LEFT * 1.1, color=TEAL, stroke_width=5),
        ).arrange(RIGHT, buff=0.22).move_to([0, -1.55, 0])

        top_q.add_updater(lambda m: m.set_x(0.65 * np.sin(2.4 * t_osc.get_value())))
        bot_q.add_updater(lambda m: m.set_x(-0.65 * np.sin(2.4 * t_osc.get_value())))

        self.play(FadeOut(poly), FadeOut(no_prom), FadeIn(top_q), FadeIn(bot_q), run_time=0.55)
        rem = max(0.5, self.narration_s + 0.35 - self.elapsed())
        self.play(t_osc.animate.set_value(rem), run_time=rem, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ Scene 2: Title
class S02Title(NarratedScene):
    def construct(self):
        duplex = build_duplex(y0=0.0, top_color=TEXT, bot_color=TEXT, show_ends=True)
        self.add(duplex)

        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=5).move_to([0, -0.35, 0])
        title = T("The Strand Is Chosen at the Start", size=50, font=TITLE_FONT, color=TEXT).move_to([0, 0.45, 0])
        fit(title, max_w=11.8)

        self.play(
            ReplacementTransform(duplex, rule),
            FadeIn(title, shift=UP * 0.15),
            run_time=0.45,
        )
        self.wait(1.10)
        duplex2 = build_duplex(y0=0.0, top_color=TEXT, bot_color=TEXT, show_ends=True)
        self.play(
            FadeOut(title, shift=UP * 0.15),
            ReplacementTransform(rule, duplex2),
            run_time=0.45,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 3: Promoter
class S03Promoter(SpokenScene):
    def construct(self):
        xp = ValueTracker(-1.8)
        op = ValueTracker(0.0)
        duplex = build_duplex(y0=0.0, top_color=TEXT, bot_color=TEXT, x_poly_tr=xp, open_tr=op, show_ends=True)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, tag)

        self.at("A promoter changes that")
        # Align +1 cleanly with XS[3] = -2.10: tip = -2.40, xr = -2.75
        prom = build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=3.02, tick_bottom=2.30)
        prom_site = SurroundingRectangle(VGroup(duplex.top_tiles[0], duplex.bot_tiles[2]), color=TEAL, buff=0.14, corner_radius=0.12, stroke_width=3.5)
        self.play(Create(prom_site), run_time=1.0)
        self.play(ReplacementTransform(prom_site, prom.poly), FadeIn(prom.lbl), run_time=1.5)
        self.play(Indicate(prom.poly, color=TEAL, scale_factor=1.08), run_time=1.2)

        self.at("where initiation machinery")
        poly = build_polymerase(direction=-1, template_side="bottom", with_label=False)
        poly.slot.set_opacity(0.0)
        place_poly(poly, 7.6, 0.0)
        self.add(poly)
        self.play(
            Create(prom.start_tick),
            FadeIn(prom.plus_lbl),
            poly.animate.move_to([3.2, poly.get_center()[1], 0]),
            run_time=2.8,
            rate_func=smooth,
        )

        self.at("Its orientation")
        poly_right = build_polymerase(direction=1, template_side="bottom", with_label=False)
        poly_right.slot.set_opacity(0.0)
        place_poly(poly_right, 3.2, 0.0)
        self.play(Transform(poly, poly_right), run_time=1.1)

        self.at("a start site")
        self.play(poly.animate.shift(LEFT * 5.0), run_time=1.0)

        self.at("facing downstream")
        down_lbl = T("downstream →", size=28, color=TEXT).move_to([3.2, 2.75, 0])
        self.play(FadeIn(down_lbl, shift=RIGHT * 0.3), run_time=0.9)

        self.at("The polymerase opens")
        self.play(op.animate.set_value(1.0), run_time=2.0)

        self.at("One strand enters")
        anims = [
            duplex.bot_bb.animate.set_stroke(color=BLUE),
            duplex.top_bb.animate.set_stroke(color=GOLD),
            duplex.ends[0].animate.set_color(GOLD),
            duplex.ends[1].animate.set_color(GOLD),
            duplex.ends[2].animate.set_color(BLUE),
            duplex.ends[3].animate.set_color(BLUE),
            poly.slot.animate.set_opacity(0.15),
        ]
        for t in duplex.bot_tiles:
            anims.append(t.box.animate.set_stroke(color=BLUE).set_fill(color=BLUE, opacity=0.18))
            anims.append(t.lab.animate.set_color(BLUE))
        for t in duplex.top_tiles:
            anims.append(t.box.animate.set_stroke(color=GOLD).set_fill(color=GOLD, opacity=0.18))
            anims.append(t.lab.animate.set_color(GOLD))
        self.play(*anims, run_time=1.3)

        tmpl_tag = T("template strand", size=28, color=BLUE).move_to([0.0, -2.85, 0])
        self.play(FadeIn(tmpl_tag), run_time=0.6)

        rem = max(0.3, self.narration_s + 0.2 - self.elapsed())
        if rem > 0.3:
            self.play(xp.animate.set_value(-1.62), run_time=rem * 0.5)
            self.play(xp.animate.set_value(-1.80), run_time=rem * 0.5)
        self.finish()


# ------------------------------------------------------------------ Scene 4: Growth
class S04Growth(SpokenScene):
    def construct(self):
        xp = ValueTracker(-2.35)
        op = ValueTracker(1.0)
        duplex = build_duplex(y0=0.0, top_color=GOLD, bot_color=BLUE, x_poly_tr=xp, open_tr=op, show_ends=True)
        prom = build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=3.02, tick_bottom=2.30)
        poly = build_polymerase(direction=1, template_side="bottom", with_label=False)
        place_poly(poly, xp.get_value(), 0.0)
        poly.add_updater(lambda m: place_poly(m, xp.get_value(), 0.0))
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, prom, poly, tag)

        rna = build_rna_strip(
            indices=range(3, 10),
            direction=1,
            x_poly_tr=xp,
            y0=0.0,
            template_side="bottom",
            duplex=duplex,
            show_5_prime=True,
        )
        self.add(rna)

        self.at("RNA polymerase now matches")
        self.play(xp.animate.set_value(XS[4] + 0.10), run_time=4.4, rate_func=linear)

        self.at("It joins each new letter")
        self.play(xp.animate.set_value(XS[5] + 0.10), run_time=3.1, rate_func=linear)

        self.at("That growing end")
        grow_lbl = T("growing 3′ end", size=28, color=GREEN).move_to([2.6, -2.85, 0])
        glide_and_show(self, xp, XS[6] + 0.10, 2.8, FadeIn(grow_lbl), anim_t=0.45)

        self.at("RNA therefore extends")
        rna_dir = T("RNA grows: 5′ → 3′", size=28, color=GREEN).move_to([2.2, 3.05, 0])
        glide_and_show(self, xp, XS[7] + 0.10, 2.9, FadeOut(grow_lbl), FadeIn(rna_dir), anim_t=0.45)

        self.at("The polymerase moves")
        poly_dir = T("polymerase reads template: 3′ → 5′", size=28, color=BLUE).move_to([0.0, -2.85, 0])
        rem = max(0.8, self.narration_s + 0.15 - self.elapsed())
        glide_and_show(self, xp, XS[9] + 0.10, rem, FadeIn(poly_dir), anim_t=0.45)
        self.finish()


# ------------------------------------------------------------------ Scene 5: Predict
def _predict_world():
    """Shared frozen duplex + reversed teal promoter + two possible polymerase choices."""
    duplex = build_duplex(y0=1.18, top_color=TEXT, bot_color=TEXT, show_ends=True)
    prom = build_promoter(direction=-1, x_start=2.75, x_end=5.15, y=3.02, tick_bottom=2.02)

    choice_r = build_polymerase(direction=1, template_side="bottom", with_label=False).scale(0.44)
    choice_r.slot.set_opacity(0.0)
    place_poly(choice_r, -4.35, -1.28)
    lbl_r = T("lower strand, → ?", size=26, color=TEXT).move_to([-4.35, -2.85, 0])

    choice_l = build_polymerase(direction=-1, template_side="top", with_label=False).scale(0.44)
    choice_l.slot.set_opacity(0.0)
    place_poly(choice_l, 4.35, -1.28)
    lbl_l = T("upper strand, ← ?", size=26, color=TEXT).move_to([4.35, -2.85, 0])

    return duplex, prom, VGroup(choice_r, lbl_r), VGroup(choice_l, lbl_l)


def _perimeter_dot(poly_mob, t_val):
    verts = poly_mob.get_vertices()
    c = poly_mob.get_center()
    closed = np.vstack([verts, verts[0:1]])
    segs = np.linalg.norm(np.diff(closed, axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(segs)])
    s = (t_val % 1.0) * cum[-1]
    idx = int(np.searchsorted(cum, s, side="right")) - 1
    idx = max(0, min(idx, len(segs) - 1))
    frac = (s - cum[idx]) / max(segs[idx], 1e-6)
    pt = closed[idx] * (1 - frac) + closed[idx + 1] * frac
    # Offset outward cleanly outside promoter stroke so pulse never sits on top of outline
    out = pt - c
    n = np.linalg.norm(out[:2])
    if n > 1e-4:
        pt = pt + np.array([out[0] / n, out[1] / n, 0.0]) * 0.09
    return pt


class S05Predict(SpokenScene):
    def construct(self):
        duplex, prom, opt_r, opt_l = _predict_world()
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, tag)

        self.at("Suppose the promoter")
        old_prom = build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=2.84, tick_bottom=2.02)
        self.play(FadeIn(old_prom), run_time=0.45)

        self.at("points the other way")
        self.play(ReplacementTransform(old_prom, prom), run_time=0.8)

        t_pulse = ValueTracker(0.0)

        def _make_pulse():
            pos = _perimeter_dot(prom.poly, t_pulse.get_value())
            return VGroup(
                Circle(radius=0.11, color=TEAL, stroke_width=2.5, fill_opacity=0.0).move_to(pos),
                Dot(pos, radius=0.055, color=GOLD),
            ).set_z_index(5)

        p_dot = always_redraw(_make_pulse)
        self.add(p_dot)
        self.play(t_pulse.animate.set_value(0.9), run_time=2.6, rate_func=linear)

        self.at("Which strand will enter")
        self.play(
            FadeIn(opt_r, shift=UP * 0.15),
            FadeIn(opt_l, shift=UP * 0.15),
            t_pulse.animate.set_value(1.5),
            run_time=1.8,
            rate_func=linear,
        )

        self.at("which way will RNA grow")
        q = question_card("Which strand enters, and which way does RNA grow?", y=-1.35, left=-2.25, max_w=4.5, size=26)
        self.play(FadeIn(q), t_pulse.animate.set_value(1.9), run_time=0.9, rate_func=linear)

        rem = max(0.2, self.narration_s + 0.2 - self.elapsed())
        self.play(t_pulse.animate.set_value(1.9 + rem * 0.45), run_time=rem, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ Scene 6: Predict Pause
class S06Pause(PredictPause):
    QUESTION = "Which strand enters, and which way does RNA grow?"
    CARD = {"y": -1.35, "left": -2.25, "max_w": 4.5, "size": 26}
    RING_AT = (0.0, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        duplex, prom, opt_r, opt_l = _predict_world()
        bob(opt_r, amp=0.06, speed=2.2, seed=0)
        bob(opt_l, amp=0.06, speed=2.2, seed=2)

        prom._bt = 0.0

        def _brighten(m, dt):
            m._bt += dt
            op = 0.22 + 0.22 * (m._bt / 4.5)
            m.poly.set_fill(color=TEAL, opacity=min(0.46, op))

        prom.add_updater(_brighten)
        tag = scope_tag("schematic", size=24, color=TEXT)
        return VGroup(duplex, prom, opt_r, opt_l, tag)


# ------------------------------------------------------------------ Scene 7: Reverse
class S07Reverse(SpokenScene):
    def construct(self):
        duplex, prom, opt_r, opt_l = _predict_world()
        q = question_card("Which strand enters, and which way does RNA grow?", y=-1.35, left=-2.25, max_w=4.5, size=26)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, prom, opt_r, opt_l, q, tag)

        self.at("The whole arrangement reverses")
        xp = ValueTracker(2.35)
        op = ValueTracker(0.0)
        active_duplex = build_duplex(y0=0.0, top_color=TEXT, bot_color=TEXT, x_poly_tr=xp, open_tr=op, show_ends=True)
        # Align +1 cleanly with XS[8] = 2.10: tip = 2.40, xl = 2.75
        active_prom = build_promoter(direction=-1, x_start=2.75, x_end=5.15, y=3.02, tick_bottom=2.30)
        poly = build_polymerase(direction=-1, template_side="top", with_label=False)
        poly.slot.set_opacity(0.0)
        place_poly(poly, 2.35, 0.0)

        self.play(FadeOut(opt_r), FadeOut(opt_l[1]), FadeOut(q), run_time=0.35)
        self.play(
            ReplacementTransform(duplex, active_duplex),
            ReplacementTransform(prom, active_prom),
            ReplacementTransform(opt_l[0], poly),
            run_time=1.0,
        )
        poly.add_updater(lambda m: place_poly(m, xp.get_value(), 0.0))

        self.at("The other DNA strand")
        self.play(op.animate.set_value(1.0), run_time=1.0)
        anims = [
            active_duplex.top_bb.animate.set_stroke(color=BLUE),
            active_duplex.bot_bb.animate.set_stroke(color=GOLD),
            active_duplex.ends[0].animate.set_color(BLUE),
            active_duplex.ends[1].animate.set_color(BLUE),
            active_duplex.ends[2].animate.set_color(GOLD),
            active_duplex.ends[3].animate.set_color(GOLD),
            poly.slot.animate.set_opacity(0.15),
        ]
        for t in active_duplex.top_tiles:
            anims.append(t.box.animate.set_stroke(color=BLUE).set_fill(color=BLUE, opacity=0.18))
            anims.append(t.lab.animate.set_color(BLUE))
        for t in active_duplex.bot_tiles:
            anims.append(t.box.animate.set_stroke(color=GOLD).set_fill(color=GOLD, opacity=0.18))
            anims.append(t.lab.animate.set_color(GOLD))
        self.play(*anims, run_time=1.1)

        rna = build_rna_strip(
            indices=range(2, 9),
            direction=-1,
            x_poly_tr=xp,
            y0=0.0,
            template_side="top",
            duplex=active_duplex,
            show_5_prime=True,
        )
        self.add(rna)

        self.at("polymerase travels")
        self.play(xp.animate.set_value(XS[7] - 0.10), run_time=3.2, rate_func=linear)

        self.at("Chemistry has not changed")
        chem_lbl = T("RNA grows: 5′ → 3′ (same chemistry)", size=28, color=GREEN).move_to([-1.8, -2.90, 0])
        glide_and_show(self, xp, XS[6] - 0.10, 2.2, FadeIn(chem_lbl), anim_t=0.45)

        self.at("RNA still grows")
        self.play(xp.animate.set_value(XS[5] - 0.10), run_time=2.4, rate_func=linear)

        self.at("Flipping the start's orientation")
        flip_note = T("← reversed template & travel", size=28, color=BLUE).move_to([-1.8, 2.95, 0])
        rem = max(0.8, self.narration_s + 0.15 - self.elapsed())
        glide_and_show(self, xp, XS[2] - 0.10, rem, FadeIn(flip_note), anim_t=0.45)
        self.finish()


# ------------------------------------------------------------------ Scene 8: Coding vs Template
class S08Coding(SpokenScene):
    def construct(self):
        sub_n = 8
        pitch = 1.05
        cxs = np.array([-3.675 + i * pitch for i in range(sub_n)], dtype=float)
        tw, th = 0.78, 0.66

        top_seq = TOP_BASES[:sub_n]
        bot_seq = BOT_BASES[:sub_n]
        rna_seq = [COMP_RNA[b] for b in top_seq]

        top_row = VGroup(*[make_tile(b, BLUE, w=tw, h=th, font_size=30) for b in top_seq])
        bot_row = VGroup(*[make_tile(b, GOLD, w=tw, h=th, font_size=30) for b in bot_seq])
        rna_row = VGroup(*[make_tile(b, GREEN, w=tw, h=th, font_size=30) for b in rna_seq])

        for i, x in enumerate(cxs):
            top_row[i].move_to([x, 1.55, 0])
            rna_row[i].move_to([x, 0.45, 0])
            bot_row[i].move_to([x, -1.65, 0])

        top_ends = VGroup(M("5′", 28, BLUE).move_to([cxs[0] - 0.85, 1.55, 0]), M("3′", 28, BLUE).move_to([cxs[-1] + 0.85, 1.55, 0]))
        bot_ends = VGroup(M("3′", 28, GOLD).move_to([cxs[0] - 0.85, -1.65, 0]), M("5′", 28, GOLD).move_to([cxs[-1] + 0.85, -1.65, 0]))
        rna_ends = VGroup(M("3′", 28, GREEN).move_to([cxs[0] - 0.85, 0.45, 0]), M("5′", 28, GREEN).move_to([cxs[-1] + 0.85, 0.45, 0]))

        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(top_row, rna_row, bot_row, top_ends, bot_ends, rna_ends, tag)

        self.play(Indicate(bot_row, color=GOLD, scale_factor=1.03), run_time=2.2)

        self.at("coding strand")
        code_lbl = T("coding strand", size=30, color=GOLD).move_to([0, -2.55, 0])
        self.play(FadeIn(code_lbl), run_time=0.6)

        self.at("Read in the same direction")
        self.play(
            rna_row.animate.shift(DOWN * 1.15),
            rna_ends.animate.shift(DOWN * 1.15),
            run_time=0.9,
        )
        arr_rna = Arrow([3.6, 0.05, 0], [-3.6, 0.05, 0], color=GREEN, stroke_width=4).set_z_index(2)
        arr_cod = Arrow([3.6, -2.25, 0], [-3.6, -2.25, 0], color=GOLD, stroke_width=4).set_z_index(2)
        self.play(Create(arr_rna), Create(arr_cod), code_lbl.animate.move_to([0, -2.95, 0]), run_time=0.8)

        self.at("Its sequence matches")
        match_bars = VGroup()
        for i, x in enumerate(cxs):
            if bot_seq[i] == rna_seq[i]:
                b = M("=", size=28, color=TEXT).move_to([x, -1.18, 0])
                match_bars.add(b)
        self.play(FadeIn(match_bars), run_time=0.8)
        self.play(
            LaggedStart(*[Indicate(VGroup(rna_row[i], bot_row[i]), color=GOLD, scale_factor=1.06) for i in range(1, 7)], lag_ratio=0.12),
            run_time=1.6,
        )

        self.at("RNA uses U")
        ut_boxes = VGroup()
        for i, x in enumerate(cxs):
            if bot_seq[i] == "T":
                b = SurroundingRectangle(VGroup(rna_row[i], bot_row[i]), color=TEAL, buff=0.08, corner_radius=0.10, stroke_width=3.5)
                ut_boxes.add(b)
        ut_lbl = T("RNA uses U where DNA uses T", size=28, color=TEAL).move_to([-0.9, -2.95, 0])
        self.play(Create(ut_boxes), swap(code_lbl, ut_lbl, run_time=0.6), run_time=1.2)
        self.play(Indicate(ut_boxes, color=TEAL, scale_factor=1.05), run_time=1.2)

        self.at("The RNA pairs with")
        self.play(
            FadeOut(match_bars),
            FadeOut(ut_boxes),
            FadeOut(arr_rna),
            FadeOut(arr_cod),
            FadeOut(ut_lbl),
            run_time=0.5,
        )
        self.play(
            rna_row.animate.move_to([0, 0.55, 0]),
            rna_ends[0].animate.move_to([cxs[0] - 0.85, 0.55, 0]),
            rna_ends[1].animate.move_to([cxs[-1] + 0.85, 0.55, 0]),
            run_time=1.4,
        )

        self.at("complementary")
        pair_bars = VGroup(*[
            Line([x, 1.16, 0], [x, 0.94, 0], color=TEAL, stroke_width=4.0) for x in cxs
        ])
        self.play(LaggedStart(*[Create(b) for b in pair_bars], lag_ratio=0.08), run_time=1.1)

        anti_top = VGroup(
            T("template 5′→3′", size=28, color=BLUE),
            Arrow(LEFT * 0.9, RIGHT * 0.9, color=BLUE, stroke_width=4),
        ).arrange(RIGHT, buff=0.2).move_to([0, 2.38, 0])
        anti_rna = VGroup(
            Arrow(RIGHT * 0.9, LEFT * 0.9, color=GREEN, stroke_width=4),
            T("RNA 5′→3′ (antiparallel)", size=28, color=GREEN),
        ).arrange(RIGHT, buff=0.2).move_to([0, -0.35, 0])
        self.play(FadeIn(anti_top), FadeIn(anti_rna), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ Scene 9: Bare duplex + RNA rescue
class S09Bare(SpokenScene):
    def construct(self):
        duplex = build_duplex(y0=0.0, top_color=BLUE, bot_color=GOLD, show_ends=True)
        prom = build_promoter(direction=-1, x_start=2.75, x_end=5.15, y=2.35, tick_bottom=0.92)
        rna_tiles = VGroup(*[make_tile(COMP_RNA[b], GREEN) for b in TOP_BASES[:8]])
        for i in range(8):
            rna_tiles[i].move_to([XS[i], -1.65, 0])
        rna_ends = VGroup(M("3′", 26, GREEN).move_to([XS[0] - 0.65, -1.65, 0]), M("5′", 26, GREEN).move_to([XS[7] + 0.65, -1.65, 0]))
        rna_strip = VGroup(rna_tiles, rna_ends)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, prom, rna_strip, tag)

        self.at("Now remove the promoter")
        self.play(FadeOut(prom), FadeOut(rna_strip), run_time=1.3)

        self.at("leaving only the duplex")
        drain_anims = [
            duplex.top_bb.animate.set_stroke(color=TEXT),
            duplex.bot_bb.animate.set_stroke(color=TEXT),
            duplex.ends.animate.set_color(TEXT),
        ]
        for t in duplex.top_tiles:
            drain_anims.append(t.box.animate.set_stroke(color=TEXT).set_fill(color=TEXT, opacity=0.14))
            drain_anims.append(t.lab.animate.set_color(TEXT))
        for t in duplex.bot_tiles:
            drain_anims.append(t.box.animate.set_stroke(color=TEXT).set_fill(color=TEXT, opacity=0.14))
            drain_anims.append(t.lab.animate.set_color(TEXT))
        self.play(*drain_anims, run_time=1.6)

        self.at("The template label")
        t_badge = chip("template?", color=TEAL, size=28).move_to([0, 1.45, 0])
        self.play(FadeIn(t_badge), run_time=0.4)
        t_badge_lo = t_badge.copy().move_to([0, -1.45, 0])
        self.play(FadeOut(t_badge, shift=DOWN * 0.1), FadeIn(t_badge_lo, shift=DOWN * 0.1), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(t_badge_lo, shift=UP * 0.1), FadeIn(t_badge, shift=UP * 0.1), run_time=0.5)
        self.wait(0.6)

        self.at("An RNA product")
        self.play(FadeOut(t_badge, shift=UP * 0.15), run_time=0.35)
        rna_strip.move_to([(XS[0] + XS[7]) / 2, -2.45, 0])
        self.play(FadeIn(rna_strip, shift=UP * 0.25), run_time=0.9)

        self.at("it matches coding DNA")
        self.play(rna_strip.animate.move_to([(XS[0] + XS[7]) / 2, -1.35, 0]), run_time=0.8)
        gold_anims = [duplex.bot_bb.animate.set_stroke(color=GOLD), duplex.ends[2].animate.set_color(GOLD), duplex.ends[3].animate.set_color(GOLD)]
        for t in duplex.bot_tiles:
            gold_anims.append(t.box.animate.set_stroke(color=GOLD).set_fill(color=GOLD, opacity=0.18))
            gold_anims.append(t.lab.animate.set_color(GOLD))
        cod_tag = T("coding strand", size=28, color=GOLD).move_to([3.2, -2.35, 0])
        self.play(*gold_anims, FadeIn(cod_tag), run_time=1.0)

        self.at("pairs with template DNA")
        self.play(rna_strip.animate.move_to([(XS[0] + XS[7]) / 2, 1.35, 0]), run_time=0.8)
        pair_ticks = VGroup(*[Line([XS[i], 0.82, 0], [XS[i], 1.07, 0], color=TEAL, stroke_width=3.5) for i in range(8)])
        blue_anims = [duplex.top_bb.animate.set_stroke(color=BLUE), duplex.ends[0].animate.set_color(BLUE), duplex.ends[1].animate.set_color(BLUE)]
        for t in duplex.top_tiles:
            blue_anims.append(t.box.animate.set_stroke(color=BLUE).set_fill(color=BLUE, opacity=0.18))
            blue_anims.append(t.lab.animate.set_color(BLUE))
        tmpl_tag = T("template strand", size=28, color=BLUE).move_to([3.2, 2.35, 0])
        self.play(*blue_anims, Create(pair_ticks), FadeIn(tmpl_tag), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ Scene 10: Moving Bubble
class S10Bubble(SpokenScene):
    def construct(self):
        xp = ValueTracker(2.94)
        op = ValueTracker(1.0)
        duplex = build_duplex(y0=0.0, top_color=BLUE, bot_color=GOLD, x_poly_tr=xp, open_tr=op, show_ends=True)
        poly = build_polymerase(direction=-1, template_side="top", with_label=False)
        place_poly(poly, xp.get_value(), 0.0)
        poly.add_updater(lambda m: place_poly(m, xp.get_value(), 0.0))
        rna = build_rna_strip(
            indices=range(1, 10),
            direction=-1,
            x_poly_tr=xp,
            y0=0.0,
            template_side="top",
            duplex=duplex,
            show_5_prime=True,
        )
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, poly, rna, tag)

        self.at("DNA opens ahead")
        ahead_lbl = T("opens ahead", size=28, color=TEXT).move_to([-4.35, 2.86, 0])
        glide_and_show(self, xp, XS[7] - 0.10, 2.5, FadeIn(ahead_lbl), anim_t=0.4)

        self.at("closes behind it")
        behind_lbl = T("closes behind", size=28, color=TEXT).move_to([4.35, 2.86, 0])
        glide_and_show(self, xp, XS[5] - 0.10, 2.1, FadeIn(behind_lbl), anim_t=0.4)

        self.at("The growing RNA peels away")
        exit_lbl = T("RNA exit path", size=28, color=GREEN).move_to([3.2, -2.85, 0])
        glide_and_show(self, xp, XS[4] - 0.10, 3.5, FadeIn(exit_lbl), anim_t=0.4)

        self.at("Polymerase reads one strand")
        read_lbl = T("reads template", size=28, color=BLUE).move_to([-3.2, -2.85, 0])
        glide_and_show(self, xp, XS[3] - 0.10, 2.0, FadeIn(read_lbl), anim_t=0.4)

        self.at("while preserving")
        pres_lbl = T("preserves coding sequence in RNA", size=28, color=GOLD).move_to([0.0, 3.32, 0])
        rem = max(0.8, self.narration_s + 0.15 - self.elapsed())
        glide_and_show(self, xp, XS[1] - 0.10, rem, FadeIn(pres_lbl), anim_t=0.45)
        self.finish()


# ------------------------------------------------------------------ Scene 11: Three Checks
class S11Checks(SpokenScene):
    def construct(self):
        duplex = build_duplex(y0=0.0, top_color=BLUE, bot_color=GOLD, show_ends=False)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, tag)

        xs_p = [-4.25, 0.0, 4.25]
        frames = VGroup()
        titles_grp = VGroup()
        titles = ["1. Orient 5′→3′", "2. Match coding", "3. Pair template"]
        cols = [TEXT, GOLD, BLUE]
        for x, ttl, col in zip(xs_p, titles, cols):
            frame = RoundedRectangle(corner_radius=0.18, width=3.90, height=4.4, stroke_color=col, stroke_width=3.0, fill_opacity=0.0).move_to([x, 0.45, 0])
            hd = T(ttl, size=28, color=col).move_to([x, 2.22, 0])
            frames.add(frame)
            titles_grp.add(hd)

        c12 = Arrow([xs_p[0] + 1.98, 0.45, 0], [xs_p[1] - 1.98, 0.45, 0], buff=0, color=TEXT, stroke_width=4)
        c23 = Arrow([xs_p[1] + 1.98, 0.45, 0], [xs_p[2] - 1.98, 0.45, 0], buff=0, color=TEXT, stroke_width=4)

        self.at("Use these checks")
        # Fade tile letters out cleanly before morphing backbones into frames (zero mid-flight letter overlap)
        self.play(FadeOut(duplex.top_tiles), FadeOut(duplex.bot_tiles), FadeOut(duplex.rungs), run_time=0.4)
        self.play(
            ReplacementTransform(VGroup(duplex.top_bb, duplex.bot_bb), frames),
            FadeIn(titles_grp),
            Create(c12),
            Create(c23),
            run_time=1.3,
        )
        self.play(Indicate(titles_grp[0], color=TEXT, scale_factor=1.06), frames[0].animate(rate_func=there_and_back).set_stroke(width=6.5), run_time=1.1)

        # Panel 1: orient both DNA strands 5'->3'
        self.at("Write both DNA strands")
        p1_top = M("5′-ACGTTTCA-3′", size=24, color=TEXT).move_to([xs_p[0], 0.95, 0])
        p1_bot = M("3′-TGCAAAGT-5′", size=24, color=TEXT).move_to([xs_p[0], 0.15, 0])
        p1_bot_rev = M("5′-TGAAACGT-3′", size=24, color=GOLD).move_to([xs_p[0], 0.15, 0])
        p1_note = T("both read 5′→3′", size=24, color=TEXT).move_to([xs_p[0], -0.88, 0])
        self.play(FadeIn(p1_top), FadeIn(p1_bot), run_time=0.9)
        self.play(swap(p1_bot, p1_bot_rev, run_time=1.1), FadeIn(p1_note), run_time=1.3)
        self.play(Indicate(titles_grp[0], color=TEXT, scale_factor=1.06), frames[0].animate(rate_func=there_and_back).set_stroke(width=6.5), Indicate(c12, color=GOLD, scale_factor=1.15), run_time=0.9)

        # Panel 2: swap U for T and match coding DNA (all text >= 24 pt)
        self.at("Match RNA to coding DNA")
        p2_rna = M("RNA 5′-UGAAACGU-3′", size=24, color=GREEN).move_to([xs_p[1], 1.05, 0])
        p2_swap = M("U→T 5′-TGAAACGT-3′", size=24, color=TEAL).move_to([xs_p[1], 1.05, 0])
        p2_eq = M("||||||||", size=24, color=GOLD).move_to([xs_p[1], 0.50, 0])
        p2_dna = M("DNA 5′-TGAAACGT-3′", size=24, color=GOLD).move_to([xs_p[1], -0.05, 0])
        p2_note = T("matches coding strand", size=24, color=GOLD).move_to([xs_p[1], -0.88, 0])
        fit(p2_rna, max_w=3.55)
        fit(p2_swap, max_w=3.55)
        fit(p2_dna, max_w=3.55)
        self.play(FadeIn(p2_rna), run_time=0.8)
        self.play(swap(p2_rna, p2_swap, run_time=1.0), run_time=1.1)
        self.play(FadeIn(p2_dna), Create(p2_eq), FadeIn(p2_note), run_time=1.3)
        self.play(Indicate(titles_grp[1], color=GOLD, scale_factor=1.06), frames[1].animate(rate_func=there_and_back).set_stroke(width=6.5), Indicate(c23, color=BLUE, scale_factor=1.15), run_time=1.0)

        # Panel 3: confirm antiparallel pairing with template
        self.at("Then confirm that RNA pairs")
        p3_top = M("5′-ACGTTTCA-3′", size=24, color=BLUE).move_to([xs_p[2], 1.05, 0])
        p3_rna = M("3′-UGCAAAGU-5′", size=24, color=GREEN).move_to([xs_p[2], 0.15, 0])
        p3_bars = M("||||||||", size=24, color=TEAL).move_to([xs_p[2], 0.60, 0])
        p3_note = T("antiparallel to template", size=24, color=BLUE).move_to([xs_p[2], -0.88, 0])
        self.play(FadeIn(p3_top), FadeIn(p3_rna), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(ch) for ch in p3_bars], lag_ratio=0.14), run_time=1.8)
        self.play(FadeIn(p3_note), Indicate(titles_grp[2], color=BLUE, scale_factor=1.06), frames[2].animate(rate_func=there_and_back).set_stroke(width=6.5), run_time=1.2)

        # Green pulse sweeps cleanly along the open bottom lane (y=-1.42) inside panels, then drops below -1.75
        self.at("Together these checks")
        pulse_ring = Circle(radius=0.24, color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.25).move_to([xs_p[0], -1.42, 0]).set_z_index(5)
        pulse_core = Dot([xs_p[0], -1.42, 0], radius=0.10, color=TEXT).set_z_index(6)
        pulse_grp = VGroup(pulse_ring, pulse_core)
        self.play(FadeIn(pulse_grp), frames[0].animate.set_stroke(color=GREEN, width=4.5), run_time=0.6)
        self.play(
            pulse_grp.animate.move_to([xs_p[1], -1.42, 0]),
            frames[1].animate.set_stroke(color=GREEN, width=4.5),
            run_time=1.1,
        )
        self.play(
            pulse_grp.animate.move_to([xs_p[2], -1.42, 0]),
            frames[2].animate.set_stroke(color=GREEN, width=4.5),
            run_time=1.1,
        )
        self.play(pulse_grp.animate.move_to([xs_p[2], -2.55, 0]), run_time=0.55)
        self.play(pulse_grp.animate.move_to([-4.2, -2.55, 0]), run_time=0.65)

        self.at("The polymerase moves")
        dir_arrow = Arrow(RIGHT * 1.4, LEFT * 1.4, color=GREEN, stroke_width=6).move_to([-4.2, -2.55, 0])
        dir_txt = T("polymerase moves toward template 5′ end", size=28, color=GREEN).next_to(dir_arrow, RIGHT, buff=0.3)
        VGroup(dir_arrow, dir_txt).move_to([-0.4, -2.55, 0])
        self.play(ReplacementTransform(pulse_grp, dir_arrow), FadeIn(dir_txt), run_time=1.1)
        self.play(Indicate(dir_arrow, color=TEAL, scale_factor=1.12), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------ Scene 12: Scope
class S12Scope(SpokenScene):
    def construct(self):
        xp = ValueTracker(-2.35)
        op = ValueTracker(1.0)
        duplex = build_duplex(y0=0.0, top_color=GOLD, bot_color=BLUE, x_poly_tr=xp, open_tr=op, show_ends=True)
        prom = build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=3.02, shape="arrow", tick_bottom=2.30)
        poly = build_polymerase(direction=1, template_side="bottom", with_label=False)
        place_poly(poly, xp.get_value(), 0.0)
        poly.add_updater(lambda m: place_poly(m, xp.get_value(), 0.0))
        rna = build_rna_strip(
            indices=range(3, 10),
            direction=1,
            x_poly_tr=xp,
            y0=0.0,
            template_side="bottom",
            duplex=duplex,
            show_5_prime=True,
        )
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(duplex, prom, poly, rna, tag)

        self.at("This rule applies")
        self.play(xp.animate.set_value(XS[4] + 0.10), run_time=5.4, rate_func=linear)

        self.at("Promoters vary")
        prom_twin = build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=3.02, shape="twin", tick_bottom=2.30)
        prom_sad = build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=3.02, shape="saddle", tick_bottom=2.30)
        prom_arr = build_promoter(direction=1, x_start=-5.15, x_end=-2.75, y=3.02, shape="arrow", tick_bottom=2.30)
        self.play(Transform(prom.poly, prom_twin.poly), xp.animate.set_value(XS[5] + 0.10), run_time=1.8, rate_func=linear)
        self.play(Transform(prom.poly, prom_sad.poly), xp.animate.set_value(XS[6] + 0.10), run_time=1.8, rate_func=linear)
        self.play(Transform(prom.poly, prom_arr.poly), xp.animate.set_value(XS[7] + 0.10), run_time=1.8, rate_func=linear)

        self.at("Yet once a start")
        start_glow = Circle(radius=0.31, color=GOLD, stroke_width=4.5, fill_opacity=0).move_to(prom.plus_lbl.get_center()).set_z_index(4)
        glide_and_show(self, xp, XS[8] + 0.10, 2.3, Create(start_glow), anim_t=0.55)

        self.at("RNA grows by adding")
        rna_arr = T("RNA: 5′ → 3′ (add at 3′)", size=28, color=GREEN).move_to([2.0, 3.05, 0])
        glide_and_show(self, xp, XS[9] + 0.10, 3.5, FadeIn(rna_arr), anim_t=0.45)

        self.at("pairing then makes")
        tmpl_arr = T("template read: 3′ → 5′  →", size=28, color=BLUE).move_to([0.0, -2.85, 0])
        rem = max(1.0, self.narration_s + 0.15 - self.elapsed())
        glide_and_show(self, xp, XS[10] + 0.10, rem, FadeIn(tmpl_arr), anim_t=0.45)
        self.finish()


# ------------------------------------------------------------------ Scene 13: End
class S13End(EndCard):
    LINE = "The start site and its orientation determine which strand is read."
