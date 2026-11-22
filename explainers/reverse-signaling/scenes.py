"""When a Ligand Listens — Reverse Signaling: When the Ligand Is Also a Receptor.

COLOUR MAP (one colour per concept for the entire film):
  RECEPTOR_COL = "#2DD4BF"  (teal)   — Receptor cell, Eph receptor (EphB / EphA), forward signal
  LIGAND_COL   = "#F59E0B"  (amber)  — Ligand cell, membrane ligand (Ephrin-B / Ephrin-A), GPI anchor,
                                       cholesterol-rich patch, reverse signal
  PHOS_COL     = "#F43F5E"  (coral)  — Phosphate groups (P) and kinases (Src-family kinases, Fyn)
  PARTNER_COL  = "#A78BFA"  (violet) — Cytosolic adaptors, actin, phosphatase, PDZ partner, p75 partner
  MEM_COL      = "#64748B"  (slate)  — Lipid bilayer leaflets and structural membrane outlines
  TEXT         = "#E8EAF0"  (white)  — Primary labels and questions

CARRIED WORLD:
  A two-cell contact cross-section (teal receptor cell above, amber ligand cell below, facing across an
  extracellular cleft), zooming in (s03..s09) onto the ligand cell's separated dual-leaflet bilayer
  (outer leaflet above, inner leaflet below, cytosol filling the lower frame) and pulling back (s10)
  to the full two-cell contact view.

WHAT CHANGES PER SPOKEN SCENE (and what drives it):
  s01_hook:             Right-side anchored ligand+receptor clasp and pulse bidirectional '?' waves;
                        left-side free amber ligand detaches and drifts along a computed arc across the
                        cleft (progress tracker 0->1), triggers an upward teal forward wave, and breaks
                        its home link.
  s02_names:            Left free ligand clears as the anchored ligand slides to center (tracker 0->1) and
                        clasps the teal receptor at the cleft midline; forward (teal up) and reverse
                        (amber down) signal wave packets travel continuously along their arrows while
                        Receptor/Ligand highlight rings swap.
  s03_two_needs:        Camera zooms smoothly (scale/shift tracker) from the two-cell contact into the
                        separated dual-leaflet ligand bilayer; anchor bracket locks on the transmembrane
                        segment, cytosolic path opens below with a downward test wave, and the view
                        splits into Tail vs Partner waves.
  s04_ephrin_b_puzzle:  Single Ephrin-B spans the bilayer with computed Y-site coordinates; teal EphB outer
                        tip glides down from above to dock, 'No kinase' tags mark both proteins, and coral P
                        tags pop sequentially onto the Y sites with expanding ripples and a '?' puzzle.
  s05_src_and_adaptor:  Three EphB tips descend to bind Ephrin-B, then slide laterally along a clustering
                        tracker (0->1) into a tight cluster; coral Src-family kinases glide up along curved
                        trajectories, convert Y->P sites, and a violet Adaptor docks to bend an elastic
                        Actin filament computed from a deflection tracker.
  s06_off_switch_pdz:   Notched PDZ tip lights up; a computed circular timer arc sweeps (0->TAU) for the
                        delay, then a violet Phosphatase glides alongside the tail stripping P badges
                        back to Y; beside it, a PDZ partner docks and launches a second violet wave.
  s07_gpi_setup_predict: Ephrin-B transmembrane stalk and cytosolic tail retract and dissolve (tracker 1->0)
                        into Ephrin-A tethered solely to the outer leaflet by a computed sinusoidal GPI stem;
                        two more Ephrin-A + EphA tips cluster laterally while the question card slides in.
  s09_gpi_reveal:       Question card clears and cluster splits; on the left a violet transmembrane p75
                        partner slides through both leaflets to pair with Ephrin-A and send a violet inward
                        wave; on the right a cholesterol-rich patch glows while coral Fyn kinases gather
                        along the inner leaflet under a dashed '?' bridge ('Not yet settled').
  s10_close:            Zoom pulls back smoothly to the full two-cell world building Tail (left) and Partner
                        (right) clasped to receptors along the contact zone, with synchronized forward
                        (teal up) and reverse (amber down) signal waves traveling into both cells.
"""

from bp_parts import *
import numpy as np

# ------------------------------------------------------------------ Film colour map
RECEPTOR_COL = "#2DD4BF"
LIGAND_COL = "#F59E0B"
PHOS_COL = "#F43F5E"
PARTNER_COL = "#A78BFA"
MEM_COL = "#64748B"
MEM_EDGE = "#94A3B8"
DARK_INK = "#0F1117"

# ------------------------------------------------------------------ Membrane geometry
X_MAX = 6.38


def _top_mem_y(x):
    return 0.96 + 0.85 * (x / X_MAX) ** 2


def _bot_mem_y(x):
    return -0.96 - 0.85 * (x / X_MAX) ** 2


def _curved_cell(y_fn, top_edge, color, mem_stroke, n=48):
    """Build a cell body polygon + double-leaflet membrane band along y_fn(x)."""
    xs = np.linspace(-X_MAX, X_MAX, n)
    pts_outer = [np.array([x, y_fn(x), 0.0]) for x in xs]
    sign = 1.0 if top_edge > 0 else -1.0
    pts_inner = [np.array([x, y_fn(x) + sign * 0.24, 0.0]) for x in xs]

    body_pts = pts_outer + [np.array([X_MAX, top_edge, 0.0]), np.array([-X_MAX, top_edge, 0.0])]
    body = Polygon(*body_pts, stroke_width=0, fill_color=color, fill_opacity=0.14)
    body.layout_ok = True

    outer_line = VMobject(stroke_color=mem_stroke, stroke_width=3.0)
    outer_line.set_points_as_corners(pts_outer)
    inner_line = VMobject(stroke_color=mem_stroke, stroke_width=2.2)
    inner_line.set_points_as_corners(pts_inner)

    bilayer_fill = Polygon(*(pts_outer + list(reversed(pts_inner))),
                           stroke_width=0, fill_color=MEM_COL, fill_opacity=0.36)
    bilayer_fill.layout_ok = True
    return VGroup(body, bilayer_fill, outer_line, inner_line)


def build_two_cell_world():
    """Carried two-cell contact cross-section: Receptor cell (top) & Ligand cell (bottom)."""
    upper = _curved_cell(_top_mem_y, 3.6, RECEPTOR_COL, RECEPTOR_COL)
    lower = _curved_cell(_bot_mem_y, -3.6, LIGAND_COL, LIGAND_COL)
    lbl_rec = T("Receptor cell", size=28, color=RECEPTOR_COL, weight=BOLD).move_to([-4.6, 2.95, 0])
    lbl_lig = T("Ligand cell", size=28, color=LIGAND_COL, weight=BOLD).move_to([-4.6, -2.95, 0])
    return VGroup(upper, lower), lbl_rec, lbl_lig


# Zoomed bilayer y-coordinates (used in s03..s09)
OUTER_TOP = 1.26
OUTER_BOT = 0.98
INNER_TOP = 0.84
INNER_BOT = 0.56


def build_zoomed_bilayer(show_leaflet_labels=False):
    """Separated outer and inner membrane leaflets + cytosol background (no panel strokes)."""
    cytosol = Rectangle(width=12.76, height=4.16, stroke_width=0, fill_color=LIGAND_COL, fill_opacity=0.13)
    cytosol.move_to([0.0, INNER_BOT - 2.08, 0.0])
    cytosol.layout_ok = True

    outer_fill = Rectangle(width=12.76, height=OUTER_TOP - OUTER_BOT, stroke_width=0,
                           fill_color=MEM_COL, fill_opacity=0.42).move_to([0.0, (OUTER_TOP + OUTER_BOT) / 2, 0.0])
    outer_fill.layout_ok = True
    inner_fill = Rectangle(width=12.76, height=INNER_TOP - INNER_BOT, stroke_width=0,
                           fill_color=MEM_COL, fill_opacity=0.42).move_to([0.0, (INNER_TOP + INNER_BOT) / 2, 0.0])
    inner_fill.layout_ok = True

    lines = VGroup(
        Line([-X_MAX, OUTER_TOP, 0], [X_MAX, OUTER_TOP, 0], color=MEM_EDGE, stroke_width=2.6),
        Line([-X_MAX, OUTER_BOT, 0], [X_MAX, OUTER_BOT, 0], color=MEM_EDGE, stroke_width=1.8),
        Line([-X_MAX, INNER_TOP, 0], [X_MAX, INNER_TOP, 0], color=MEM_EDGE, stroke_width=1.8),
        Line([-X_MAX, INNER_BOT, 0], [X_MAX, INNER_BOT, 0], color=MEM_EDGE, stroke_width=2.6),
    )
    grp = VGroup(cytosol, outer_fill, inner_fill, lines)
    if show_leaflet_labels:
        l_out = T("Outer leaflet", size=24, color=TEXT).move_to([-5.15, 1.50, 0])
        l_in = T("Inner leaflet", size=24, color=TEXT).move_to([-5.15, 0.28, 0])
        grp.add(l_out, l_in)
    return grp


# ------------------------------------------------------------------ Schematic protein parts
def solid_chip(text, fill_col, text_col=DARK_INK, size=24, pad_x=0.22, pad_y=0.14):
    """Solid-fill protein/kinase chip auto-sized around its text so letters never overflow."""
    lbl = T(text, size=size, color=text_col, weight=BOLD)
    box = RoundedRectangle(
        corner_radius=0.14,
        width=lbl.width + 2 * pad_x,
        height=lbl.height + 2 * pad_y,
        color=fill_col,
        stroke_width=2.6,
        fill_color=fill_col,
        fill_opacity=0.92,
    )
    return VGroup(box, lbl.move_to(box))


def eph_receptor_block(x, y_tip, stem_up=True, stalk_top=None, color=RECEPTOR_COL, scale=1.0):
    """Teal Y-cup receptor outer tip facing downward to grip a ligand."""
    cup = Polygon(
        [-0.44, 0.34, 0], [-0.26, 0.34, 0], [-0.20, 0.10, 0],
        [0.20, 0.10, 0], [0.26, 0.34, 0], [0.44, 0.34, 0],
        [0.36, -0.04, 0], [-0.36, -0.04, 0],
        color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.28,
    )
    cup.flip(RIGHT)
    cup.scale(scale)
    cup.move_to([x, y_tip, 0])
    parts = VGroup(cup)
    if stem_up:
        cup_top = cup.get_top()[1]
        s_top = stalk_top if stalk_top is not None else (cup_top + 0.78 * scale)
        sh = max(0.35, s_top - cup_top + 0.04)
        stalk = RoundedRectangle(corner_radius=0.06, width=0.22 * scale, height=sh,
                                 color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.24)
        stalk.move_to([x, cup_top + sh / 2 - 0.02, 0])
        parts.add(stalk)
    return parts


def two_cell_ligand(x, y_bot_mem, y_head=0.0):
    """Amber ligand anchored in lower cell membrane reaching up to clasp at y_head."""
    head = RoundedRectangle(corner_radius=0.16, width=0.50, height=0.40,
                            color=LIGAND_COL, stroke_width=2.6, fill_color=LIGAND_COL, fill_opacity=0.40)
    head.move_to([x, y_head, 0])
    s_bot = y_bot_mem - 0.24
    s_top = y_head - 0.14
    sh = max(0.4, s_top - s_bot)
    stalk = Rectangle(width=0.22, height=sh, color=LIGAND_COL, stroke_width=2.5,
                      fill_color=LIGAND_COL, fill_opacity=0.34).move_to([x, (s_top + s_bot) / 2, 0])
    return VGroup(stalk, head)


def ephrin_b_complex(x, tail_len=2.40, with_y_sites=False, notch=False):
    """Amber B-type ephrin: extracellular head + single transmembrane stalk + cytosolic tail."""
    head = RoundedRectangle(corner_radius=0.18, width=0.58, height=0.46,
                            color=LIGAND_COL, stroke_width=2.8, fill_color=LIGAND_COL, fill_opacity=0.38)
    head.move_to([x, OUTER_TOP + 0.26, 0])

    stalk_h = OUTER_TOP - INNER_BOT + 0.08
    stalk = Rectangle(width=0.22, height=stalk_h,
                      stroke_width=0, fill_color=LIGAND_COL, fill_opacity=0.55)
    stalk.move_to([x, (OUTER_TOP + INNER_BOT) / 2, 0])

    tail_top = INNER_BOT
    tail_bot = INNER_BOT - tail_len
    if notch:
        hw = 0.11
        tail = Polygon(
            [x - hw, tail_top, 0],
            [x + hw, tail_top, 0],
            [x + hw, tail_bot, 0],
            [x + 0.05, tail_bot + 0.22, 0],
            [x - 0.05, tail_bot + 0.22, 0],
            [x - hw, tail_bot, 0],
            stroke_width=0, fill_color=LIGAND_COL, fill_opacity=0.68,
        )
    else:
        tail = RoundedRectangle(corner_radius=0.08, width=0.22, height=tail_len,
                                stroke_width=0, fill_color=LIGAND_COL, fill_opacity=0.68)
        tail.move_to([x, tail_top - tail_len / 2, 0])

    grp = VGroup(stalk, tail, head)
    grp.head = head
    grp.stalk = stalk
    grp.tail = tail
    grp.y_pts = [np.array([x, tail_top - tail_len * f, 0.0]) for f in (0.18, 0.45, 0.72)]
    grp.tip_pt = np.array([x, tail_bot, 0.0])

    if with_y_sites:
        ys = VGroup(*[y_badge(p) for p in grp.y_pts])
        grp.ys = ys
        grp.add(ys)
    return grp


def y_badge(pos):
    """Open circle marked Y for a conserved tyrosine site."""
    c = Circle(radius=0.25, color=TEXT, stroke_width=2.4, fill_color=DARK_INK, fill_opacity=0.98).move_to(pos)
    t = T("Y", size=22, color=TEXT, weight=BOLD).move_to(pos)
    return VGroup(c, t)


def p_badge(pos):
    """Coral phosphate circle marked P."""
    c = Circle(radius=0.25, color=PHOS_COL, stroke_width=2.6, fill_color=PHOS_COL, fill_opacity=0.98).move_to(pos)
    t = T("P", size=22, color=DARK_INK, weight=BOLD).move_to(pos)
    return VGroup(c, t)


def wavy_gpi_stem(x, y_top=OUTER_TOP + 0.04, y_bot=OUTER_BOT + 0.05, amp=0.07):
    """Computed sinusoidal GPI lipid stem anchored ONLY inside the outer leaflet."""
    ts = np.linspace(0.0, 1.0, 28)
    pts = [np.array([x + amp * np.sin(3.5 * PI * t), y_top + (y_bot - y_top) * t, 0.0]) for t in ts]
    m = VMobject(stroke_color=LIGAND_COL, stroke_width=4.0)
    m.set_points_as_corners(pts)
    return m


def ephrin_a_unit(x):
    """Amber A-type ephrin outer block + wavy GPI stem confined to the outer leaflet."""
    head = RoundedRectangle(corner_radius=0.18, width=0.58, height=0.46,
                            color=LIGAND_COL, stroke_width=2.8, fill_color=LIGAND_COL, fill_opacity=0.38)
    head.move_to([x, OUTER_TOP + 0.26, 0])
    stem = wavy_gpi_stem(x)
    g = VGroup(stem, head)
    g.head = head
    g.stem = stem
    return g


def signal_stream(start, end, color, phase_tracker, n_pulses=3):
    """Arrow shaft plus computed traveling signal wave packets and target-cell wavefronts."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    vec = end - start
    length = max(np.linalg.norm(vec), 1e-6)
    u = vec / length
    perp = np.array([-u[1], u[0], 0.0])
    ang = np.arctan2(u[1], u[0])
    shaft = Arrow(start, end, color=color, stroke_width=5.5, buff=0.0, max_tip_length_to_length_ratio=0.18)

    def make_pulses():
        p = phase_tracker.get_value()
        pulses = VGroup()
        for k in range(n_pulses):
            frac = (p + k / n_pulses) % 1.0
            pos = start + vec * (0.08 + 0.76 * frac)
            alpha = 0.35 + 0.65 * np.sin(PI * frac)
            halo = Circle(radius=0.15, stroke_width=0, fill_color=color, fill_opacity=0.80 * alpha).move_to(pos)
            core = Dot(pos, radius=0.08, color=TEXT).set_opacity(alpha)
            chev = VMobject(stroke_color=TEXT, stroke_width=3.2, stroke_opacity=alpha)
            chev.set_points_as_corners([pos - u * 0.11 + perp * 0.15, pos + u * 0.09, pos - u * 0.11 - perp * 0.15])
            pulses.add(halo, core, chev)
        # Propagating wavefront arcs exiting arrow tip into the cell
        for w in range(2):
            wf = (p + 0.5 * w) % 1.0
            r = 0.18 + 0.65 * wf
            arc = Arc(radius=r, start_angle=ang - 0.65, angle=1.30, arc_center=end - u * 0.12,
                      stroke_color=color, stroke_width=4.0 * (1.0 - 0.6 * wf), stroke_opacity=0.85 * (1.0 - wf))
            pulses.add(arc)
        return pulses

    return shaft, always_redraw(make_pulses)


def actin_curve(deflect_val, y_base=-2.62, x_half=4.2):
    """Computed elastic beam deflection curve for the actin filament under adaptor pull."""
    xs = np.linspace(-x_half, x_half, 60)
    pts = []
    for x in xs:
        dy = -deflect_val * np.exp(-(x / 1.45) ** 2)
        pts.append(np.array([x, y_base + dy, 0.0]))
    m = VMobject(stroke_color=PARTNER_COL, stroke_width=5.5)
    m.set_points_as_corners(pts)
    return m


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Reverse Signaling: When the Ligand Is Also a Receptor"
    TITLE = "When a Ligand Listens"


class S01Hook(SpokenScene):
    def construct(self):
        world, lbl_rec, lbl_lig = build_two_cell_world()
        tag = scope_tag("schematic")
        self.add(world, lbl_rec, lbl_lig, tag)

        # Right side: anchored ligand + receptor clasping at y = 0
        rx = 2.9
        y_top_r, y_bot_r = _top_mem_y(rx), _bot_mem_y(rx)
        r_rec = eph_receptor_block(rx, 0.14, stem_up=True, stalk_top=y_top_r + 0.24, color=RECEPTOR_COL, scale=1.0)
        r_rec.shift(UP * 0.45)
        anchored = two_cell_ligand(rx, y_bot_r, y_head=-0.02)

        # Left side: free ligand starts embedded at lower cell, ready to detach
        lx = -2.8
        y_top_l, y_bot_l = _top_mem_y(lx), _bot_mem_y(lx)
        l_rec = eph_receptor_block(lx, y_top_l - 0.36, stem_up=True, stalk_top=y_top_l + 0.24, color=RECEPTOR_COL, scale=1.0)
        free_dot = Dot([lx, y_bot_l + 0.22, 0], radius=0.24, color=LIGAND_COL, stroke_color=TEXT, stroke_width=2.0)
        lbl_free = T("Free ligand", size=28, color=LIGAND_COL).move_to([-4.65, -0.15, 0])

        self.play(FadeIn(r_rec), FadeIn(anchored), FadeIn(l_rec), FadeIn(free_dot), run_time=0.8)
        # Receptor descends to clasp the anchored ligand as narration opens
        self.play(r_rec.animate.shift(DOWN * 0.45), run_time=3.2, rate_func=smooth)

        # Beat 1: "how can both cells get a message?"
        self.at("how can both")
        q_phase = ValueTracker(0.0)
        q_up, q_up_pls = signal_stream([rx, y_top_r + 0.25, 0], [rx, y_top_r + 1.35, 0], RECEPTOR_COL, q_phase, n_pulses=2)
        q_dn, q_dn_pls = signal_stream([rx, y_bot_r - 0.25, 0], [rx, y_bot_r - 1.35, 0], LIGAND_COL, q_phase, n_pulses=2)
        q_up_t = T("?", size=34, color=RECEPTOR_COL, weight=BOLD).next_to(q_up, RIGHT, buff=0.28)
        q_dn_t = T("?", size=34, color=LIGAND_COL, weight=BOLD).next_to(q_dn, RIGHT, buff=0.28)
        self.add(q_up_pls, q_dn_pls)
        self.play(GrowArrow(q_up), GrowArrow(q_dn), FadeIn(q_up_t), FadeIn(q_dn_t),
                  q_phase.animate.set_value(1.2), run_time=2.5, rate_func=linear)

        # Beat 2: "Most signals we learn float freely across space."
        self.at("Most signals we")
        self.play(FadeIn(lbl_free, run_time=0.4), q_phase.animate.set_value(1.6), run_time=0.5, rate_func=linear)

        drift_t = ValueTracker(0.0)
        start_pt = np.array([lx, y_bot_l + 0.22, 0.0])
        end_pt = np.array([lx, y_top_l - 0.40, 0.0])

        def update_free(m):
            u = drift_t.get_value()
            pos = start_pt + (end_pt - start_pt) * u + np.array([0.28 * np.sin(PI * u), 0.0, 0.0])
            m.move_to(pos)

        free_dot.add_updater(update_free)
        dotted_trail = DashedLine(start_pt, end_pt + DOWN * 0.22, color=LIGAND_COL, stroke_width=3.0, dash_length=0.14)
        self.play(drift_t.animate.set_value(1.0), Create(dotted_trail), q_phase.animate.set_value(2.8),
                  run_time=2.5, rate_func=linear)
        free_dot.remove_updater(update_free)

        phase = ValueTracker(0.0)
        fwd_arrow, fwd_pulses = signal_stream([lx, y_top_l + 0.28, 0], [lx, y_top_l + 1.38, 0], RECEPTOR_COL, phase)
        self.add(fwd_arrow, fwd_pulses)
        self.play(phase.animate.set_value(1.0), q_phase.animate.set_value(3.4), run_time=1.0, rate_func=linear)

        # Beat 3: "Once a free ligand leaves its home cell, that connection is gone."
        self.at("Once a free")
        x_mark = VGroup(
            Line([-0.20, -0.20, 0], [0.20, 0.20, 0], color=MEM_EDGE, stroke_width=5.5),
            Line([-0.20, 0.20, 0], [0.20, -0.20, 0], color=MEM_EDGE, stroke_width=5.5),
        ).move_to([lx, y_bot_l + 0.12, 0])
        lost_lbl = T("Connection lost", size=28, color=MEM_EDGE).move_to([lx, y_bot_l - 0.65, 0])
        self.play(FadeOut(dotted_trail), FadeIn(x_mark), FadeIn(lost_lbl),
                  phase.animate.set_value(2.0), q_phase.animate.set_value(4.4), run_time=1.5, rate_func=linear)
        rem = max(0.2, self.narration_s + 0.3 - self.elapsed())
        self.play(phase.animate.set_value(2.0 + rem * 0.8), q_phase.animate.set_value(4.4 + rem * 0.8),
                  run_time=rem, rate_func=linear)
        self.finish()


class S02Names(SpokenScene):
    def construct(self):
        world, lbl_rec, lbl_lig = build_two_cell_world()
        tag = scope_tag("schematic")
        self.add(world, lbl_rec, lbl_lig, tag)

        # Rebuild carried objects from end of S01
        rx = 2.9
        y_top_r, y_bot_r = _top_mem_y(rx), _bot_mem_y(rx)
        r_rec = eph_receptor_block(rx, 0.14, stem_up=True, stalk_top=y_top_r + 0.24, color=RECEPTOR_COL, scale=1.0)
        anchored = two_cell_ligand(rx, y_bot_r, y_head=-0.02)

        lx = -2.8
        y_top_l, y_bot_l = _top_mem_y(lx), _bot_mem_y(lx)
        left_group = VGroup(
            eph_receptor_block(lx, y_top_l - 0.36, stem_up=True, stalk_top=y_top_l + 0.24, color=RECEPTOR_COL, scale=1.0),
            Dot([lx, y_top_l - 0.40, 0], radius=0.24, color=LIGAND_COL, stroke_color=TEXT, stroke_width=2.0),
            T("Free ligand", size=28, color=LIGAND_COL).move_to([-4.65, -0.15, 0]),
            T("Connection lost", size=28, color=MEM_EDGE).move_to([lx, y_bot_l - 0.65, 0]),
        )
        self.add(left_group, r_rec, anchored)

        # Beat 1: "Now tether that ligand in its own cell's membrane."
        self.play(FadeOut(left_group), run_time=0.7)

        y_top_0, y_bot_0 = _top_mem_y(0.0), _bot_mem_y(0.0)
        r_target = eph_receptor_block(0.0, 0.12, stem_up=True, stalk_top=y_top_0 + 0.24, color=RECEPTOR_COL, scale=1.0)
        a_target = two_cell_ligand(0.0, y_bot_0, y_head=-0.02)
        self.play(
            Transform(r_rec, r_target),
            Transform(anchored, a_target),
            run_time=2.4, rate_func=smooth,
        )

        rec_chip = boxed_label("Receptor", RECEPTOR_COL, size=28).move_to([-1.75, 0.50, 0])
        lig_chip = boxed_label("Ligand", LIGAND_COL, size=28).move_to([-1.75, -0.50, 0])
        self.play(FadeIn(rec_chip), FadeIn(lig_chip), run_time=0.8)

        # Beat 2: "the receptor cell gets the forward signal"
        self.at("the receptor cell")
        fwd_phase = ValueTracker(0.0)
        fwd_arr, fwd_pulses = signal_stream([0.0, y_top_0 + 0.25, 0], [0.0, y_top_0 + 1.95, 0], RECEPTOR_COL, fwd_phase)
        fwd_lbl = T("Forward signal", size=30, color=RECEPTOR_COL, weight=BOLD).move_to([2.45, 2.05, 0])
        self.add(fwd_arr, fwd_pulses)
        self.play(Create(fwd_arr), FadeIn(fwd_lbl, run_time=0.4), fwd_phase.animate.set_value(1.5), run_time=2.2, rate_func=linear)

        # Beat 3: "The ligand cell can get a reverse signal, too."
        self.at("The ligand cell")
        rev_phase = ValueTracker(0.0)
        rev_arr, rev_pulses = signal_stream([0.0, y_bot_0 - 0.25, 0], [0.0, y_bot_0 - 1.95, 0], LIGAND_COL, rev_phase)
        rev_lbl = T("Reverse signal", size=30, color=LIGAND_COL, weight=BOLD).move_to([2.45, -2.05, 0])
        bidi_lbl = boxed_label("Bidirectional", TEXT, size=28).move_to([2.85, 0.0, 0])
        self.add(rev_arr, rev_pulses)
        self.play(
            Create(rev_arr), FadeIn(rev_lbl, run_time=0.4), FadeIn(bidi_lbl, run_time=0.4),
            fwd_phase.animate.set_value(3.0),
            rev_phase.animate.set_value(1.5),
            run_time=2.4, rate_func=linear,
        )

        # Beat 4: "Why still call it a ligand?" / "Those names only record which role biologists saw first."
        self.at("Why still call")
        ring_rec = SurroundingRectangle(rec_chip, color=GOLD, buff=0.05, corner_radius=0.14, stroke_width=3.5)
        ring_lig = SurroundingRectangle(lig_chip, color=GOLD, buff=0.05, corner_radius=0.14, stroke_width=3.5)
        seen_lbl = fit_text("Named by\nfirst role seen", max_w=2.4, size=28, color=TEXT).move_to([-4.65, 0.0, 0])
        self.play(Create(ring_rec), fwd_phase.animate.set_value(4.0), rev_phase.animate.set_value(2.5), run_time=1.3)

        self.at("Those names only")
        self.play(FadeOut(ring_rec, run_time=0.22), fwd_phase.animate.set_value(4.3), rev_phase.animate.set_value(2.8), run_time=0.35, rate_func=linear)
        self.play(
            FadeIn(ring_lig, run_time=0.25),
            FadeIn(seen_lbl, run_time=0.4),
            fwd_phase.animate.set_value(5.8),
            rev_phase.animate.set_value(4.3),
            run_time=2.2, rate_func=linear,
        )
        self.play(
            fwd_phase.animate.set_value(7.2),
            rev_phase.animate.set_value(5.7),
            run_time=max(0.2, self.narration_s + 0.3 - self.elapsed()), rate_func=linear,
        )
        self.finish()


class S03TwoNeeds(SpokenScene):
    def construct(self):
        world, lbl_rec, lbl_lig = build_two_cell_world()
        tag = scope_tag("schematic")
        self.add(world, lbl_rec, lbl_lig, tag)

        bilayer = build_zoomed_bilayer(show_leaflet_labels=True)
        lig0 = ephrin_b_complex(0.0, tail_len=1.85)
        rec0 = eph_receptor_block(0.0, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=1.0)

        zoom_group = VGroup(bilayer, lig0, rec0)
        zoom_group.save_state()
        zoom_group.scale(0.45).move_to([0.0, -1.25, 0.0]).set_opacity(0.0)
        self.play(
            FadeOut(world), FadeOut(lbl_rec), FadeOut(lbl_lig),
            Restore(zoom_group),
            run_time=2.2, rate_func=smooth,
        )
        self.play(Indicate(lig0.head, color=LIGAND_COL), run_time=1.0)

        # Beat 1: "First, the ligand must stay attached to its own membrane."
        self.at("First, the ligand")
        anchor_box = RoundedRectangle(
            corner_radius=0.10, width=0.48, height=OUTER_TOP - INNER_BOT - 0.02,
            color=LIGAND_COL, stroke_width=3.5,
        ).move_to([0.0, (OUTER_TOP + INNER_BOT + 0.04) / 2, 0.0])
        need1 = boxed_label("1. Stay anchored", LIGAND_COL, size=28).move_to([-3.2, 2.25, 0])
        need1_line = Line(need1.get_bottom(), anchor_box.get_left(), color=LIGAND_COL, stroke_width=2.6)
        self.play(Create(anchor_box), FadeIn(need1), Create(need1_line), run_time=1.6)

        # Beat 2: "Second, it needs a path into the cytosol."
        self.at("Second, it needs")
        tail_box = RoundedRectangle(
            corner_radius=0.10, width=0.48, height=1.94,
            color=TEXT, stroke_width=3.5,
        ).move_to([0.0, INNER_BOT - 0.03 - 1.94 / 2, 0.0])
        need2 = boxed_label("2. Path into cytosol", TEXT, size=28).move_to([3.3, -0.55, 0])
        need2_line = Line(need2.get_left(), tail_box.get_right() + RIGHT * 0.05, color=TEXT, stroke_width=2.6)
        self.play(Create(tail_box), FadeIn(need2), Create(need2_line), run_time=1.6)

        # Beat 3: "A cytosolic tail is what you normally expect on a receptor."
        self.at("A cytosolic tail")
        tail_lbl = T("Cytosolic tail", size=28, color=LIGAND_COL, weight=BOLD).move_to([-3.0, -0.55, 0])
        test_p = ValueTracker(0.0)
        test_arr, test_pls = signal_stream([-0.55, INNER_BOT - 0.25, 0], [-0.55, -1.65, 0], LIGAND_COL, test_p)
        self.play(FadeIn(tail_lbl, run_time=0.4), Indicate(lig0.tail, color=GOLD, run_time=0.8))
        self.add(test_arr, test_pls)
        self.play(Create(test_arr), test_p.animate.set_value(1.8), run_time=3.0, rate_func=linear)

        # Beat 4: "A membrane ligand can signal inward through a tail or partner."
        self.at("A membrane ligand")
        self.play(
            FadeOut(anchor_box), FadeOut(need1), FadeOut(need1_line),
            FadeOut(tail_box), FadeOut(need2), FadeOut(need2_line),
            FadeOut(tail_lbl), FadeOut(test_arr), FadeOut(test_pls),
            run_time=0.5,
        )

        left_x, right_x = -2.8, 2.8
        left_lig = ephrin_b_complex(left_x, tail_len=1.85)
        left_rec = eph_receptor_block(left_x, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95)
        lbl_tail = boxed_label("Tail", LIGAND_COL, size=30).move_to([left_x, -2.90, 0])

        right_lig = ephrin_a_unit(right_x - 0.45)
        right_rec = eph_receptor_block(right_x - 0.45, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95)
        partner = RoundedRectangle(corner_radius=0.12, width=0.42, height=2.45,
                                   color=PARTNER_COL, stroke_width=2.8, fill_color=PARTNER_COL, fill_opacity=0.35)
        partner.move_to([right_x + 0.38, OUTER_TOP - 0.95, 0])
        lbl_partner = boxed_label("Partner", PARTNER_COL, size=30).move_to([right_x, -2.90, 0])

        self.play(
            ReplacementTransform(VGroup(lig0, rec0), VGroup(left_lig, left_rec)),
            FadeIn(right_lig, run_time=0.6), FadeIn(right_rec, run_time=0.6), FadeIn(partner, run_time=0.6),
            FadeIn(lbl_tail, run_time=0.6), FadeIn(lbl_partner, run_time=0.6),
            run_time=0.8,
        )

        p_wave = ValueTracker(0.0)
        arr_l, pls_l = signal_stream([left_x + 0.55, INNER_BOT - 0.25, 0], [left_x + 0.55, -1.60, 0], LIGAND_COL, p_wave)
        arr_r, pls_r = signal_stream([right_x + 0.95, INNER_BOT - 0.25, 0], [right_x + 0.95, -1.60, 0], PARTNER_COL, p_wave)
        self.add(arr_l, pls_l, arr_r, pls_r)
        self.play(Create(arr_l), Create(arr_r), p_wave.animate.set_value(2.0),
                  run_time=max(0.5, self.narration_s + 0.3 - self.elapsed()), rate_func=linear)
        self.finish()


class S04EphrinBPuzzle(SpokenScene):
    def construct(self):
        bilayer = build_zoomed_bilayer(show_leaflet_labels=False)
        tag = scope_tag("schematic")
        self.add(bilayer, tag)

        ephrin = ephrin_b_complex(0.0, tail_len=2.40, with_y_sites=False)
        lbl_ephrin = T("Ephrin-B", size=32, color=LIGAND_COL, weight=BOLD).move_to([-2.4, 1.95, 0])
        self.play(FadeIn(ephrin.head), GrowFromEdge(ephrin.stalk, UP), GrowFromEdge(ephrin.tail, UP),
                  FadeIn(lbl_ephrin), run_time=2.8)

        # Beat 1: "Each crosses the membrane once and ends in a short cytosolic tail."
        self.at("Each crosses the")
        ys = VGroup(*[y_badge(p) for p in ephrin.y_pts])
        pass_lbl = T("1 transmembrane pass", size=28, color=TEXT).move_to([3.35, 0.02, 0])
        pass_line = Line([0.16, 0.88, 0], [2.05, 0.22, 0], color=TEXT, stroke_width=2.2)
        tail_lbl = T("Short cytosolic tail", size=28, color=LIGAND_COL).move_to([-3.1, -0.55, 0])
        self.play(
            Indicate(ephrin.stalk, color=TEXT),
            FadeIn(pass_lbl, run_time=0.45), Create(pass_line),
            FadeIn(tail_lbl, run_time=0.45),
            LaggedStart(*[FadeIn(y, scale=0.6) for y in ys], lag_ratio=0.35),
            run_time=3.4,
        )

        # Beat 2: "That tail has no kinase enzyme."
        self.at("That tail has")
        no_kin_tail = boxed_label("No kinase", MEM_EDGE, size=28).move_to([-2.85, -1.55, 0])
        kin_arrow_tail = DashedLine(no_kin_tail.get_right() + RIGHT * 0.05, [-0.35, -1.55, 0], color=MEM_EDGE, stroke_width=2.5)
        self.play(FadeIn(no_kin_tail), Create(kin_arrow_tail), run_time=1.8)

        # Beat 3: "Neither does the receptor's outer binding tip."
        self.at("Neither does the")
        ephb = eph_receptor_block(0.0, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=1.05)
        ephb_start = ephb.get_center() + UP * 1.3
        ephb_end = ephb.get_center()
        ephb.move_to(ephb_start)
        lbl_ephb = T("EphB outer tip", size=30, color=RECEPTOR_COL, weight=BOLD).move_to([2.75, 2.62, 0])
        no_kin_rec = boxed_label("No kinase", MEM_EDGE, size=28).move_to([2.75, 1.90, 0])

        self.add(ephb)
        self.play(ephb.animate.move_to(ephb_end), FadeIn(lbl_ephb, run_time=0.5), run_time=2.0, rate_func=smooth)
        self.play(FadeIn(no_kin_rec), run_time=0.9)

        # Beat 4: "Yet receptor contact puts phosphate onto tyrosines in that tail."
        self.at("Yet receptor contact")
        p_badges = VGroup(*[p_badge(p) for p in ephrin.y_pts])
        q_mark = T("?", size=48, color=PHOS_COL, weight=BOLD).move_to([1.65, -0.78, 0])
        q_note = T("Where does P come from?", size=28, color=TEXT).move_to([3.35, -1.55, 0])

        for y_b, p_b in zip(ys, p_badges):
            ripple = Circle(radius=0.25, color=PHOS_COL, stroke_width=3.0).move_to(p_b.get_center())
            self.play(FadeOut(y_b, run_time=0.14))
            self.play(FadeIn(p_b, scale=1.3, run_time=0.24),
                      ripple.animate(run_time=0.55).scale(2.2).set_stroke(opacity=0))
            self.remove(ripple)

        self.play(FadeIn(q_mark, scale=1.2), FadeIn(q_note, run_time=0.5), run_time=1.0)
        self.play(Indicate(q_mark, color=GOLD), run_time=max(0.2, self.narration_s + 0.3 - self.elapsed()))
        self.finish()


class S05SrcAndAdaptor(SpokenScene):
    def construct(self):
        bilayer = build_zoomed_bilayer(show_leaflet_labels=False)
        tag = scope_tag("schematic")
        self.add(bilayer, tag)

        xs_start = [-2.95, 0.0, 2.95]
        xs_clust = [-2.25, 0.0, 2.25]

        ephrins = VGroup(*[ephrin_b_complex(x, tail_len=2.25, with_y_sites=True) for x in xs_start])
        receptors = VGroup(*[eph_receptor_block(x, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95) for x in xs_start])
        for r in receptors:
            r.shift(UP * 0.9)
        lbl_ephb = T("EphB tips", size=28, color=RECEPTOR_COL, weight=BOLD).move_to([-4.85, 2.55, 0])
        lbl_ephrin = T("Ephrin-B", size=28, color=LIGAND_COL, weight=BOLD).move_to([-4.85, 1.68, 0])
        q_puzzle = T("?", size=44, color=PHOS_COL, weight=BOLD).move_to([1.25, -0.5, 0])

        self.add(ephrins, receptors, lbl_ephb, lbl_ephrin, q_puzzle)
        self.play(*[r.animate.shift(DOWN * 0.9) for r in receptors], run_time=3.6, rate_func=smooth)

        # Beat 1: "Receptor binding pulls ephrins into dense clusters."
        self.at("Receptor binding pulls")
        clust_t = ValueTracker(0.0)
        e_starts = [e.get_center().copy() for e in ephrins]
        r_starts = [r.get_center().copy() for r in receptors]
        for i in range(3):
            dx = xs_clust[i] - xs_start[i]
            ephrins[i].add_updater(lambda m, s=e_starts[i], d=dx: m.move_to(s + RIGHT * d * clust_t.get_value()))
            receptors[i].add_updater(lambda m, s=r_starts[i], d=dx: m.move_to(s + RIGHT * d * clust_t.get_value()))

        cluster_lbl = T("Clustered tails", size=28, color=LIGAND_COL, weight=BOLD).move_to([4.65, 1.68, 0])
        self.play(FadeOut(q_puzzle), clust_t.animate.set_value(1.0), run_time=3.2, rate_func=smooth)
        for i in range(3):
            ephrins[i].clear_updaters()
            receptors[i].clear_updaters()
        self.play(FadeIn(cluster_lbl), run_time=0.5)

        # Beat 2: "Clustered tails draw SARC family kinases from inside the ephrins' own cell."
        self.at("Clustered tails draw")
        kin_targets = [
            np.array([-3.10, -0.45, 0.0]),
            np.array([0.88, -0.85, 0.0]),
            np.array([3.10, -0.45, 0.0]),
        ]
        kin_starts = [
            np.array([-3.10, -2.85, 0.0]),
            np.array([0.88, -2.85, 0.0]),
            np.array([4.30, -2.55, 0.0]),
        ]
        kinases = VGroup(*[solid_chip("Src", PHOS_COL, size=24, pad_x=0.20, pad_y=0.14).move_to(ks) for ks in kin_starts])

        lbl_src = boxed_label("Src-family\nkinases", PHOS_COL, size=24, pad=0.14).move_to([-4.85, -1.95, 0])
        self.play(FadeIn(kinases, run_time=0.5), FadeIn(lbl_src, run_time=0.5))

        kin_t = ValueTracker(0.0)
        for i in range(3):
            kinases[i].add_updater(
                lambda m, s=kin_starts[i], e=kin_targets[i]: m.move_to(
                    interpolate(s, e, kin_t.get_value()) + UP * 0.22 * np.sin(PI * kin_t.get_value())
                )
            )
        self.play(kin_t.animate.set_value(1.0), run_time=3.4, rate_func=smooth)
        for i in range(3):
            kinases[i].clear_updaters()

        # Beat 3: "Those kinases add the phosphates."
        self.at("Those kinases add")
        p_groups = VGroup()
        for idx, e in enumerate(ephrins):
            cx = xs_clust[idx]
            pg = VGroup(*[p_badge([cx, p[1], 0]) for p in e.y_pts])
            p_groups.add(pg)
        self.play(*[FadeOut(e.ys, run_time=0.2) for e in ephrins])
        self.play(LaggedStart(*[FadeIn(pg, scale=1.2) for pg in p_groups], lag_ratio=0.22), run_time=2.4)

        # Beat 4: "An adapter then docks there and links the tail to actin."
        self.at("docks there")
        deflect = ValueTracker(0.0)
        actin = always_redraw(lambda: actin_curve(deflect.get_value(), y_base=-2.65, x_half=4.2))
        lbl_actin = T("Actin", size=28, color=PARTNER_COL, weight=BOLD).move_to([4.95, -2.65, 0])
        self.add(actin)
        self.play(Create(actin), FadeIn(lbl_actin, run_time=0.4), run_time=0.6)

        adaptor = solid_chip("Adaptor", PARTNER_COL, size=24, pad_x=0.16, pad_y=0.11).move_to([-1.12, -2.02, 0])
        adaptor_target = np.array([-1.12, -1.06, 0.0])
        self.play(FadeIn(adaptor, run_time=0.3))
        self.play(adaptor.animate.move_to(adaptor_target), run_time=1.0, rate_func=smooth)

        link_seg = always_redraw(lambda: Line(
            adaptor.get_bottom(),
            np.array([-1.12, -2.65 - deflect.get_value() * np.exp(-(-1.12 / 1.45) ** 2), 0.0]),
            color=PARTNER_COL, stroke_width=5.0,
        ))
        self.add(link_seg)
        self.play(deflect.animate.set_value(0.42), run_time=max(0.8, self.narration_s + 0.3 - self.elapsed()), rate_func=smooth)
        self.finish()


class S06OffSwitchPdz(SpokenScene):
    def construct(self):
        bilayer = build_zoomed_bilayer(show_leaflet_labels=False)
        tag = scope_tag("schematic")
        self.add(bilayer, tag)

        lx, rx = -2.0, 2.0
        e_left = ephrin_b_complex(lx, tail_len=2.00, with_y_sites=False, notch=True)
        e_right = ephrin_b_complex(rx, tail_len=2.00, with_y_sites=False, notch=True)
        r_left = eph_receptor_block(lx, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95)
        r_right = eph_receptor_block(rx, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95)

        p_left = VGroup(*[p_badge(pt) for pt in e_left.y_pts])
        y_right = VGroup(*[y_badge(pt) for pt in e_right.y_pts])
        self.add(e_left, e_right, r_left, r_right, p_left, y_right)

        # Beat 1: "The same tail carries a second handle at its very tip, a PDZ binding site."
        self.at("a second handle")
        tip_ring_l = Circle(radius=0.18, color=GOLD, stroke_width=3.5).move_to(e_left.tip_pt + UP * 0.08)
        tip_ring_r = Circle(radius=0.18, color=GOLD, stroke_width=3.5).move_to(e_right.tip_pt + UP * 0.08)
        pdz_lbl = boxed_label("PDZ site", GOLD, size=28).move_to([0.0, -1.36, 0])
        pdz_arr_l = Line(pdz_lbl.get_left(), tip_ring_l.get_right() + RIGHT * 0.05, color=GOLD, stroke_width=2.5)
        pdz_arr_r = Line(pdz_lbl.get_right(), tip_ring_r.get_left() + LEFT * 0.05, color=GOLD, stroke_width=2.5)
        self.play(Create(tip_ring_l), Create(tip_ring_r), FadeIn(pdz_lbl), Create(pdz_arr_l), Create(pdz_arr_r), run_time=3.5)
        self.play(Indicate(tip_ring_l, color=TEXT), Indicate(tip_ring_r, color=TEXT), run_time=1.8)

        # Beat 2: "After a delay, a phosphatase binds that end and strips the phosphates off."
        self.at("After a delay")
        timer_c = np.array([-4.95, -0.55, 0.0])
        timer_bg = Circle(radius=0.50, color=MEM_EDGE, stroke_width=4.0).move_to(timer_c).set_opacity(0.45)
        timer_t = ValueTracker(0.001)
        timer_arc = always_redraw(lambda: Arc(
            radius=0.50, start_angle=PI / 2, angle=-timer_t.get_value() * TAU,
            color=PARTNER_COL, stroke_width=8.0, arc_center=timer_c,
        ))
        timer_lbl = T("Delay", size=26, color=TEXT).next_to(timer_bg, DOWN, buff=0.18)
        self.add(timer_bg, timer_arc, timer_lbl)
        self.play(timer_t.animate.set_value(1.0), run_time=1.6, rate_func=linear)
        self.play(FadeOut(timer_bg), FadeOut(timer_arc), FadeOut(timer_lbl), run_time=0.25)

        # Clear PDZ tip highlight before Phosphatase docks to avoid overlap
        phosphatase = solid_chip("Phosphatase", PARTNER_COL, size=24, pad_x=0.24, pad_y=0.14).move_to([lx, -2.95, 0])
        self.play(FadeOut(pdz_arr_l), FadeOut(tip_ring_l), FadeOut(pdz_lbl), FadeOut(pdz_arr_r),
                  FadeIn(phosphatase, run_time=0.3), run_time=0.4)
        self.play(phosphatase.animate.move_to([lx, e_left.tip_pt[1] - 0.34, 0]), run_time=0.6)
        self.play(phosphatase.animate.move_to([lx - 1.80, e_left.tip_pt[1] - 0.34, 0]), run_time=0.35)

        # Phosphatase sweeps along x = lx - 1.80 so it clears Y/P badges completely
        y_restored = VGroup(*[y_badge(pt) for pt in e_left.y_pts])
        for idx in reversed(range(3)):
            pt = e_left.y_pts[idx]
            self.play(
                phosphatase.animate.move_to([lx - 1.80, pt[1], 0]),
                p_left[idx].animate.shift(RIGHT * 0.65 + DOWN * 0.35).set_opacity(0.0),
                run_time=0.42,
            )
            self.play(FadeIn(y_restored[idx], scale=1.15), run_time=0.24)

        off_lbl = T("Phosphates stripped", size=26, color=PARTNER_COL).move_to([-4.25, -2.65, 0])
        self.play(FadeIn(off_lbl, run_time=0.4), run_time=0.5)

        # Beat 3: "Other PDZ proteins also bind there, giving the tail a second root."
        self.at("Other PDZ proteins")
        pdz_partner = solid_chip("PDZ partner", PARTNER_COL, size=24, pad_x=0.24, pad_y=0.14).move_to([rx + 2.4, -2.55, 0])
        self.play(FadeOut(tip_ring_r), FadeIn(pdz_partner, run_time=0.35), run_time=0.45)
        self.play(pdz_partner.animate.move_to([rx, e_right.tip_pt[1] - 0.34, 0]), run_time=0.8)

        wave_t = ValueTracker(0.0)
        route2_arr, route2_pls = signal_stream([rx, e_right.tip_pt[1] - 0.70, 0], [rx, -2.88, 0], PARTNER_COL, wave_t, n_pulses=2)
        route2_lbl = T("Route 2: PDZ signal", size=26, color=PARTNER_COL, weight=BOLD).move_to([4.20, -2.50, 0])
        self.add(route2_arr, route2_pls)
        self.play(Create(route2_arr), FadeIn(route2_lbl, run_time=0.4), run_time=0.5)
        self.play(wave_t.animate.set_value(1.5),
                  run_time=max(0.4, self.narration_s + 0.3 - self.elapsed()), rate_func=linear)
        self.finish()


def _gpi_backdrop():
    """Shared backdrop for the end of S07 and the whole S08PredictPause."""
    bilayer = build_zoomed_bilayer(show_leaflet_labels=True)
    xs = [-1.45, 0.0, 1.45]
    units = VGroup(*[ephrin_a_unit(x) for x in xs])
    tips = VGroup(*[eph_receptor_block(x, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95) for x in xs])
    lbl_ea = T("Ephrin-A", size=30, color=LIGAND_COL, weight=BOLD).move_to([-4.75, 2.25, 0])
    lbl_epha = T("EphA tips", size=28, color=RECEPTOR_COL, weight=BOLD).move_to([4.55, 2.55, 0])
    lbl_gpi = fit_text("GPI anchor\n(outer layer only)", max_w=3.2, size=26, color=LIGAND_COL).move_to([4.25, -0.05, 0])
    gpi_line = Line(lbl_gpi.get_corner(UL) + np.array([0.15, 0.06, 0.0]), [1.55, 1.02, 0], color=LIGAND_COL, stroke_width=2.2)

    q_badge = boxed_label("?", GOLD, size=32).move_to([0.0, -0.78, 0])
    q_arrow_top = DashedLine([0.0, OUTER_BOT - 0.04, 0], q_badge.get_top() + UP * 0.08, color=GOLD, stroke_width=4.0, dash_length=0.14)
    q_arrow_bot = DashedLine(q_badge.get_bottom() + DOWN * 0.08, [0.0, -1.85, 0], color=GOLD, stroke_width=4.0, dash_length=0.14)
    return VGroup(bilayer, units, tips, lbl_ea, lbl_epha, lbl_gpi, gpi_line, q_arrow_top, q_badge, q_arrow_bot)


class S07GpiSetupPredict(SpokenScene):
    def construct(self):
        bilayer = build_zoomed_bilayer(show_leaflet_labels=True)
        tag = scope_tag("schematic")
        self.add(bilayer, tag)

        ephrin_b = ephrin_b_complex(0.0, tail_len=2.15, with_y_sites=False)
        lbl_name = T("Ephrin-B", size=30, color=LIGAND_COL, weight=BOLD).move_to([-4.75, 2.25, 0])
        self.add(ephrin_b, lbl_name)

        # Beat 1: "Now watch what happens when the tail disappears completely."
        self.at("watch what happens")
        retract = ValueTracker(1.0)
        stalk0, tail0 = ephrin_b.stalk, ephrin_b.tail

        def retract_stalk(m):
            f = max(0.02, retract.get_value())
            m.stretch_to_fit_height(max(0.02, 0.78 * f))
            m.move_to([0.0, OUTER_TOP - 0.39 * f, 0.0])
            m.set_opacity(f)

        def retract_tail(m):
            f = max(0.02, retract.get_value())
            m.stretch_to_fit_height(max(0.02, 2.40 * f))
            m.move_to([0.0, INNER_BOT - 1.20 * f, 0.0])
            m.set_opacity(f)

        stalk0.add_updater(retract_stalk)
        tail0.add_updater(retract_tail)
        self.play(retract.animate.set_value(0.0), run_time=3.6, rate_func=smooth)
        stalk0.clear_updaters()
        tail0.clear_updaters()
        self.remove(stalk0, tail0)

        # Beat 2: "A-type ephrin has no transmembrane segment and no cytosolic tail."
        self.at("type")
        lbl_ea = T("Ephrin-A", size=30, color=LIGAND_COL, weight=BOLD).move_to([-4.75, 2.25, 0])
        no_tail_lbl = T("No transmembrane segment, no cytosolic tail", size=28, color=TEXT).move_to([0.0, -0.95, 0])
        self.play(swap(lbl_name, lbl_ea), FadeIn(no_tail_lbl, run_time=0.5), run_time=1.5)
        self.play(Indicate(no_tail_lbl, color=LIGAND_COL), run_time=2.5)

        # Beat 3: "A lipid called a GPI anchor holds it only in the outer membrane layer."
        self.at("A lipid called")
        stem = wavy_gpi_stem(0.0)
        lbl_gpi = fit_text("GPI anchor\n(outer layer only)", max_w=3.2, size=26, color=LIGAND_COL).move_to([4.25, -0.05, 0])
        gpi_start = lbl_gpi.get_corner(UL) + np.array([0.15, 0.06, 0.0])
        gpi_line = Line(gpi_start, [0.12, 1.02, 0], color=LIGAND_COL, stroke_width=2.2)
        self.play(Create(stem), FadeIn(lbl_gpi, run_time=0.5), Create(gpi_line), run_time=2.8)

        # Beat 4: "When a receptor clusters it, how could a signal cross?"
        self.at("When a receptor")
        left_u = ephrin_a_unit(-2.9)
        right_u = ephrin_a_unit(2.9)
        tips_start = [-2.9, 0.0, 2.9]
        tips_end = [-1.45, 0.0, 1.45]
        tips = VGroup(*[eph_receptor_block(x, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95) for x in tips_start])
        lbl_epha = T("EphA tips", size=28, color=RECEPTOR_COL, weight=BOLD).move_to([4.55, 2.55, 0])

        self.play(FadeOut(no_tail_lbl), FadeIn(left_u), FadeIn(right_u), FadeIn(tips), FadeIn(lbl_epha), run_time=0.55)

        q_badge = boxed_label("?", GOLD, size=32).move_to([0.0, -0.78, 0])
        q_arrow_top = DashedLine([0.0, OUTER_BOT - 0.04, 0], q_badge.get_top() + UP * 0.08, color=GOLD, stroke_width=4.0, dash_length=0.14)
        q_arrow_bot = DashedLine(q_badge.get_bottom() + DOWN * 0.08, [0.0, -1.85, 0], color=GOLD, stroke_width=4.0, dash_length=0.14)
        q_card = question_card("No tail inside — how can a signal cross?", color=TEXT, size=30)

        self.play(
            left_u.animate.shift(RIGHT * (tips_end[0] - tips_start[0])),
            right_u.animate.shift(LEFT * (tips_start[2] - tips_end[2])),
            tips[0].animate.shift(RIGHT * (tips_end[0] - tips_start[0])),
            tips[2].animate.shift(LEFT * (tips_start[2] - tips_end[2])),
            gpi_line.animate.put_start_and_end_on(gpi_start, [1.55, 1.02, 0]),
            Create(q_arrow_top), FadeIn(q_badge), Create(q_arrow_bot),
            FadeIn(q_card),
            run_time=2.6, rate_func=smooth,
        )
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "No tail inside — how can a signal cross?"
    CARD = {"color": TEXT, "size": 30}
    SECONDS = 4.5

    def backdrop(self):
        return _gpi_backdrop()


class S09GpiReveal(SpokenScene):
    def construct(self):
        bd = _gpi_backdrop()
        q_card = question_card("No tail inside — how can a signal cross?", color=TEXT, size=30)
        tag = scope_tag("schematic")
        self.add(bd, q_card, tag)

        bilayer, units, tips, lbl_ea, lbl_epha, lbl_gpi, gpi_line, q_arrow_top, q_badge, q_arrow_bot = bd
        self.play(FadeOut(q_card), FadeOut(q_arrow_top), FadeOut(q_badge), FadeOut(q_arrow_bot),
                  FadeOut(lbl_gpi), FadeOut(gpi_line), run_time=0.6)

        # Beat 1: "It borrows a partner that reaches the inside..."
        lx, rx = -3.0, 2.10
        p75 = RoundedRectangle(corner_radius=0.12, width=0.46, height=2.55,
                               color=PARTNER_COL, stroke_width=2.8, fill_color=PARTNER_COL, fill_opacity=0.38)
        p75.move_to([-0.55, OUTER_TOP - 0.98, 0])
        p75_target = np.array([lx + 0.95, OUTER_TOP - 0.98, 0.0])

        u_left_2 = ephrin_a_unit(lx + 0.25)
        t_left_2 = eph_receptor_block(lx + 0.25, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95)
        u_right_1 = ephrin_a_unit(rx - 0.45)
        t_right_1 = eph_receptor_block(rx - 0.45, OUTER_TOP + 0.50, stem_up=True, color=RECEPTOR_COL, scale=0.95)
        rule_lbl = T("Signal must cross to the cytosol", size=28, color=TEXT).move_to([0.0, -1.95, 0])

        self.play(
            FadeOut(units[1]), FadeOut(tips[1]),
            units[0].animate.shift(RIGHT * ((lx - 0.65) - (-1.45))),
            tips[0].animate.shift(RIGHT * ((lx - 0.65) - (-1.45))),
            units[2].animate.shift(RIGHT * ((rx + 0.45) - 1.45)),
            tips[2].animate.shift(RIGHT * ((rx + 0.45) - 1.45)),
            lbl_ea.animate.move_to([-4.95, 2.15, 0]),
            lbl_epha.animate.move_to([4.75, 2.55, 0]),
            FadeIn(p75),
            run_time=2.0, rate_func=smooth,
        )
        self.play(
            FadeIn(u_left_2), FadeIn(t_left_2), FadeIn(u_right_1), FadeIn(t_right_1),
            FadeIn(rule_lbl),
            run_time=0.8,
        )
        self.play(Indicate(p75, color=GOLD), Indicate(rule_lbl, color=GOLD), run_time=2.4)
        self.play(FadeOut(rule_lbl), run_time=0.6)

        # Beat 2: "In some cells, a membrane spanning protein such as P -75 pairs with the ephron."
        self.at("In some cells")
        lbl_p75 = boxed_label("p75 partner", PARTNER_COL, size=28).move_to([lx - 1.35, -1.05, 0])

        self.play(FadeIn(lbl_p75, run_time=0.4))
        self.play(p75.animate.move_to(p75_target), run_time=2.0, rate_func=smooth)

        self.at("pairs with")
        p75_phase = ValueTracker(0.0)
        p75_arr, p75_pls = signal_stream([lx + 0.95, -1.10, 0], [lx + 0.95, -2.75, 0], PARTNER_COL, p75_phase)
        p75_sig_lbl = T("Inward signal", size=28, color=PARTNER_COL, weight=BOLD).move_to([lx - 1.25, -2.35, 0])
        self.add(p75_arr, p75_pls)
        self.play(Create(p75_arr), FadeIn(p75_sig_lbl, run_time=0.4), p75_phase.animate.set_value(1.5),
                  run_time=1.8, rate_func=linear)

        # Beat 3: "In cholesterol -rich patches, inner leaflet kinases like fin gather underneath."
        self.at("patches")
        patch = Rectangle(width=2.45, height=OUTER_TOP - INNER_BOT + 0.04,
                          stroke_color=LIGAND_COL, stroke_width=2.8, fill_color=LIGAND_COL, fill_opacity=0.22)
        patch.move_to([rx, (OUTER_TOP + INNER_BOT) / 2, 0.0])
        patch.layout_ok = "outside"
        lbl_patch = fit_text("Cholesterol-rich\npatch", max_w=2.45, size=26, color=LIGAND_COL, weight=BOLD).move_to([4.75, 1.80, 0])
        patch_line = Line(lbl_patch.get_bottom() + DOWN * 0.05, [rx + 1.24, 1.12, 0], color=LIGAND_COL, stroke_width=2.2)
        self.play(FadeIn(patch), FadeIn(lbl_patch, run_time=0.45), Create(patch_line), p75_phase.animate.set_value(2.8),
                  run_time=1.8, rate_func=linear)

        self.at("gather underneath")
        fyn_starts = [np.array([5.15, 0.14, 0.0]), np.array([0.05, 0.14, 0.0])]
        fyn_ends = [np.array([rx + 0.72, INNER_BOT - 0.30, 0.0]), np.array([rx - 0.72, INNER_BOT - 0.30, 0.0])]
        fyns = VGroup(*[solid_chip("Fyn", PHOS_COL, size=24, pad_x=0.22, pad_y=0.14).move_to(fs) for fs in fyn_starts])
        self.play(FadeIn(fyns, run_time=0.4), p75_phase.animate.set_value(3.3), run_time=0.5)

        fyn_t = ValueTracker(0.0)
        for i in range(2):
            fyns[i].add_updater(lambda m, s=fyn_starts[i], e=fyn_ends[i]: m.move_to(interpolate(s, e, fyn_t.get_value())))
        self.play(fyn_t.animate.set_value(1.0), p75_phase.animate.set_value(4.8), run_time=1.8, rate_func=smooth)
        for i in range(2):
            fyns[i].clear_updaters()

        # Beat 4: "How a lipid patch alone crosses the bilayer remains unresolved."
        self.at("a lipid patch")
        hedge_arrow = DashedLine([rx, OUTER_BOT - 0.02, 0], [rx, INNER_BOT - 0.45, 0], color=GOLD, stroke_width=4.0, dash_length=0.10)
        hedge_q = T("?", size=32, color=GOLD, weight=BOLD).move_to([rx + 0.50, -0.68, 0])
        hedge_lbl = boxed_label("Not yet settled", GOLD, size=28).move_to([rx + 0.35, -1.65, 0])
        hedge_line = Line(hedge_lbl.get_top(), [rx, INNER_BOT - 0.55, 0], color=GOLD, stroke_width=2.4)
        self.play(
            Create(hedge_arrow), FadeIn(hedge_q), FadeIn(hedge_lbl), Create(hedge_line),
            p75_phase.animate.set_value(6.5),
            run_time=2.0, rate_func=linear,
        )
        self.play(p75_phase.animate.set_value(8.0),
                  run_time=max(0.2, self.narration_s + 0.3 - self.elapsed()), rate_func=linear)
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        world, lbl_rec, lbl_lig = build_two_cell_world()
        tag = scope_tag("schematic")
        self.add(world, lbl_rec, lbl_lig, tag)

        # Left side: Ephrin-B (Tail route) at x = -2.8, receptor clasping ligand at y = 0
        lx = -2.8
        yl_top, yl_bot = _top_mem_y(lx), _bot_mem_y(lx)
        l_rec = eph_receptor_block(lx, 0.14, stem_up=True, stalk_top=yl_top + 0.24, color=RECEPTOR_COL, scale=0.95)
        l_lig = two_cell_ligand(lx, yl_bot, y_head=-0.02)
        l_tail_ext = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.80,
                                      stroke_width=0, fill_color=LIGAND_COL, fill_opacity=0.65).move_to([lx, yl_bot - 0.46, 0])
        l_src = Circle(radius=0.18, color=PHOS_COL, stroke_width=2.4, fill_color=PHOS_COL, fill_opacity=0.9).move_to([lx - 0.35, yl_bot - 0.42, 0])
        l_adp = RoundedRectangle(corner_radius=0.10, width=0.44, height=0.28,
                                 color=PARTNER_COL, stroke_width=2.4, fill_color=PARTNER_COL, fill_opacity=0.88).move_to([lx + 0.38, yl_bot - 0.60, 0])
        lbl_tail = boxed_label("Ephrin-B:\nTail", LIGAND_COL, size=26).move_to([-4.95, 0.0, 0])

        # Right side: Ephrin-A (Partner route) at x = +2.8, receptor clasping ligand at y = 0
        rx = 2.8
        yr_top, yr_bot = _top_mem_y(rx), _bot_mem_y(rx)
        r_rec = eph_receptor_block(rx, 0.14, stem_up=True, stalk_top=yr_top + 0.24, color=RECEPTOR_COL, scale=0.95)
        r_head = RoundedRectangle(corner_radius=0.14, width=0.50, height=0.38,
                                  color=LIGAND_COL, stroke_width=2.5, fill_color=LIGAND_COL, fill_opacity=0.40).move_to([rx, -0.02, 0])
        r_gpi = wavy_gpi_stem(rx, y_top=-0.20, y_bot=yr_bot + 0.02, amp=0.06)
        r_part = RoundedRectangle(corner_radius=0.10, width=0.34, height=1.45,
                                  color=PARTNER_COL, stroke_width=2.5, fill_color=PARTNER_COL, fill_opacity=0.38).move_to([rx + 0.48, yl_bot - 0.08, 0])
        r_fyn = Circle(radius=0.18, color=PHOS_COL, stroke_width=2.4, fill_color=PHOS_COL, fill_opacity=0.9).move_to([rx - 0.35, yr_bot - 0.40, 0])
        lbl_part = boxed_label("Ephrin-A:\nPartner", PARTNER_COL, size=26).move_to([4.95, 0.0, 0])

        # Sequential build across 0.0..6.5s so there is no static freeze before "Stay anchored at"
        self.play(FadeIn(l_rec), FadeIn(l_lig), FadeIn(l_tail_ext), FadeIn(l_src), FadeIn(l_adp), FadeIn(lbl_tail),
                  run_time=2.8)
        self.play(FadeIn(r_rec), FadeIn(r_head), Create(r_gpi), FadeIn(r_part), FadeIn(r_fyn), FadeIn(lbl_part),
                  run_time=2.8)

        # Beat 1: "Stay anchored at the surface and couple receptor grip to an inward path."
        self.at("Stay anchored at")
        br_l = SurroundingRectangle(VGroup(l_rec, l_lig, l_tail_ext, l_src, l_adp), color=GOLD, buff=0.10, corner_radius=0.14, stroke_width=3.2)
        br_r = SurroundingRectangle(VGroup(r_rec, r_head, r_part, r_fyn), color=GOLD, buff=0.10, corner_radius=0.14, stroke_width=3.2)
        logic_lbl = fit_text("Anchored +\ncoupled inward", max_w=2.8, size=28, color=GOLD, weight=BOLD).move_to([0.0, 0.0, 0])
        self.play(Create(br_l), Create(br_r), FadeIn(logic_lbl), run_time=2.2)
        self.play(FadeOut(br_l), FadeOut(br_r), run_time=1.0)

        # Beat 2: "Whether through a tail or a partner, a membrane ligand can listen as well as speak."
        self.at("Whether through a")
        sig_p = ValueTracker(0.0)
        f_arr_l, f_pls_l = signal_stream([lx, yl_top + 0.28, 0], [lx, yl_top + 1.38, 0], RECEPTOR_COL, sig_p)
        f_arr_r, f_pls_r = signal_stream([rx, yr_top + 0.28, 0], [rx, yr_top + 1.38, 0], RECEPTOR_COL, sig_p)
        r_arr_l, r_pls_l = signal_stream([lx, yl_bot - 0.90, 0], [lx, yl_bot - 1.85, 0], LIGAND_COL, sig_p)
        r_arr_r, r_pls_r = signal_stream([rx + 0.48, yr_bot - 0.85, 0], [rx + 0.48, yr_bot - 1.82, 0], LIGAND_COL, sig_p)

        lbl_fwd = T("Forward", size=28, color=RECEPTOR_COL, weight=BOLD).move_to([0.0, 2.35, 0])
        lbl_rev = T("Reverse", size=28, color=LIGAND_COL, weight=BOLD).move_to([0.0, -2.35, 0])

        self.add(f_arr_l, f_pls_l, f_arr_r, f_pls_r, r_arr_l, r_pls_l, r_arr_r, r_pls_r)
        self.play(
            Create(f_arr_l), Create(f_arr_r), Create(r_arr_l), Create(r_arr_r),
            FadeIn(lbl_fwd), FadeIn(lbl_rev),
            sig_p.animate.set_value(1.5),
            run_time=2.0, rate_func=linear,
        )
        self.play(
            sig_p.animate.set_value(3.8),
            run_time=max(0.5, self.narration_s + 0.3 - self.elapsed()), rate_func=linear,
        )
        self.finish()


class S11End(EndCard):
    LINE = "A membrane ligand can signal inward through a tail or partner."
