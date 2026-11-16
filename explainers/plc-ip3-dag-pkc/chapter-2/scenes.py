"""
How Conventional PKC Reads Both Branches
======================================

COLOUR MAP (one colour per concept, carried across the whole film):
- PIP2: GOLD (#D4A843)
- IP3: BLUE (#58C4DD)
- DAG / phorbol ester: ORANGE (#FF862F)
- Calcium (Ca2+): GREEN (#83C167)
- PLC: WHITE (#FFFFFF)
- Conventional PKC (and PKC domains / fragments): TEAL (#3FB8C0)
- Gq route: PURPLE (#9A72AC)
- Receptor-tyrosine-kinase route: MAGENTA (#D147BD)
- Neutral substrates / protein partner / membrane lipids: TEXT (#E8EAF0) / GREY (#8B93A1)
- Phosphate badge (P) / predict question accent: YELLOW (#F5D547) / GOLD (#D4A843)

CARRIED WORLD:
A 16:9 schematic cell cross-section with the plasma membrane at the top (carrying an anionic-lipid
patch and DAG on its inner leaflet), the endoplasmic reticulum (ER) with an IP3-gated calcium
channel at bottom-left, and the cytosol in the middle. Close-up scenes zoom onto the single
continuous 4-block PKC chain (pseudosubstrate - C1 - C2 - kinase); comparison scenes divide the
carried plasma membrane into three panels.

SPOKEN SCENES — WHAT CHANGES AND WHAT IT IS COMPUTED FROM:
- s00_link_question: IP3 travels along a computed cubic Bezier path to the ER gate; Ca2+ dots
  stream upward along computed trajectories (default_rng(7)); DAG sways sinusoidally in the
  inner leaflet; folded TEAL PKC enters cytosol with GREEN and ORANGE arrows pointing to it.
- s02_closed: Zoomed folded PKC fills frame; neutral substrate advances along x, collides with the
  pseudosubstrate plug in the active-site slot and recoils; highlight arc and bead trace the
  continuous 4-block chain; C2 gains GREEN outline and C1 gains ORANGE outline.
- s03_calcium: IP3 traces path to ER and opens gate; Ca2+ swarm (default_rng(11)) streams out of
  the ER and 3 ions converge onto C2; folded PKC glides upward until C2 touches the anionic-lipid
  patch and C1 probes the local membrane.
- s04_dag: C1 sweeps laterally along the inner leaflet (oscillatory scan) until gripping DAG;
  parameterized open_frac tracker slides pseudosubstrate out of the active-site slot; neutral
  substrate enters the open active-site mouth from below and carries away a P badge.
- s05_predict: Carried membrane divides into 3 panels ('calcium', 'DAG', 'calcium + DAG'); identical
  folded PKCs sit below each; Ca2+ swarm (default_rng(13)), DAG block, and combined inputs
  populate them sequentially; top predict question card enters and panel options highlight.
- s07_cooperation: In 'calcium' and 'DAG' panels, PKC touches membrane briefly and drifts back
  with short 'weaker' retention arrows; in 'calcium + DAG' panel, both contacts hold, PKC unfolds
  (open_frac 0->1), phosphorylates substrate, and a tall 'stronger' retention arrow grows.
- s08_timing: Single ValueTracker t in [0, 10] drives computed Gaussian-pulse Ca2+ curve, delayed
  DAG curve, and cooperative (Ca2+ * DAG) PKC activity curve, synced to PKC vertical recruitment,
  DAG grip, unfolding, and activity halo dimming to zero as Ca2+ falls.
- s09_classes: Three PKC class cartoons ('conventional', 'novel', 'atypical') animate to the
  membrane or protein partner only under their specific described inputs (Ca2+ + DAG, DAG only,
  or protein partner).
- s10_phorbol: DAG swaps to a striped ORANGE 'phorbol ester' block; ValueTracker advances clock
  hands continuously while phorbol ester stays bound; active PKC breaks into 7 computed fragments
  (default_rng(19)) that disperse downward as 'degradation'.
- s11_rule: Original cell cross-section and legend restore; Ca2+ targets PKC to membrane while
  GREEN 'targeting' arrow grows; DAG engages C1, pseudosubstrate opens, substrate receives P badge
  while ORANGE 'activation' arrow grows; both arrows merge into TEAL 'conventional PKC output'.
"""

from bp_parts import *

ORANGE = "#FF862F"
PURPLE = "#9A72AC"
MAGENTA = "#D147BD"
WHITE = "#FFFFFF"


def build_membrane(y_bot=1.95, y_top=2.45, x0=-6.2, x1=6.2, label="plasma membrane",
                   anionic_span=(-0.6, 3.6), show_anionic_label=True):
    """Build the plasma membrane bilayer bar with an optional anionic-lipid inner-leaflet patch."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    h = y_top - y_bot
    cy = (y_bot + y_top) / 2
    body = Rectangle(width=w, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.18).move_to([cx, cy, 0])
    top_line = Line([x0, y_top, 0], [x1, y_top, 0], color=GREY, stroke_width=3)
    bot_line = Line([x0, y_bot, 0], [x1, y_bot, 0], color=GREY, stroke_width=3)
    g = VGroup(body, top_line, bot_line)
    g.y_bot, g.y_top = y_bot, y_top
    if label:
        lab = T(label, 24, TEXT).move_to([x0 + 0.1, y_top + 0.28, 0], aligned_edge=LEFT)
        g.add(lab)
        g.label = lab
    if anionic_span is not None:
        ax0, ax1 = anionic_span
        patch = Rectangle(width=ax1 - ax0, height=0.12, stroke_color=TEAL, stroke_width=2,
                          fill_color=TEAL, fill_opacity=0.28).move_to([(ax0 + ax1) / 2, y_bot + 0.06, 0])
        g.add(patch)
        g.patch = patch
        if show_anionic_label:
            alab = T("anionic lipids", 24, TEAL).move_to([(ax0 + ax1) / 2, y_top + 0.28, 0])
            g.add(alab)
            g.anionic_label = alab
    return g


def build_er(x0=-5.9, x1=-1.7, y0=-2.75, y1=-1.15, gate_open=0.0):
    """Build the ER compartment at bottom-left with an IP3-gated channel on its top edge."""
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    gate_x = cx + 0.4
    box = RoundedRectangle(corner_radius=0.22, width=w, height=h, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.14).move_to([cx, cy, 0])
    gap = 0.16 + 0.34 * gate_open
    post_l = Rectangle(width=0.18, height=0.34, stroke_color=BLUE, stroke_width=2,
                       fill_color=BLUE, fill_opacity=0.35).move_to([gate_x - gap / 2 - 0.09, y1, 0])
    post_r = Rectangle(width=0.18, height=0.34, stroke_color=BLUE, stroke_width=2,
                       fill_color=BLUE, fill_opacity=0.35).move_to([gate_x + gap / 2 + 0.09, y1, 0])
    lab = T("ER", 28, TEXT).move_to([cx - 0.5, cy - 0.1, 0])
    g = VGroup(box, post_l, post_r, lab)
    g.gate_pos = np.array([gate_x, y1, 0.0])
    g.posts = (post_l, post_r)
    return g


def build_dag(pos, width=0.56, height=0.38, label="DAG", label_y=None, striped=False):
    """Build an ORANGE DAG (or striped phorbol ester) block embedded inside the inner leaflet."""
    rect = RoundedRectangle(corner_radius=0.07, width=width, height=height, stroke_color=ORANGE,
                            stroke_width=3, fill_color=ORANGE, fill_opacity=0.40).move_to(pos)
    parts = [rect]
    if striped:
        stripes = VGroup()
        for frac in (-0.30, -0.10, 0.10, 0.30):
            sx = pos[0] + frac * width
            ln = Line([sx - 0.08, pos[1] - height * 0.40, 0],
                      [sx + 0.08, pos[1] + height * 0.40, 0],
                      color=BG, stroke_width=4)
            ln.layout_ok = True
            stripes.add(ln)
        parts.append(stripes)
    g = VGroup(*parts)
    g.block = rect
    if label:
        ly = label_y if label_y is not None else (pos[1] + height / 2 + 0.36)
        lab = T(label, 24, ORANGE).move_to([pos[0], ly, 0])
        g.add(lab)
        g.label = lab
    return g


def _kinase_with_slot(center, w, h, color=TEAL, fill_opacity=0.22):
    """Create a kinase block with a visible left-facing active-site U-notch."""
    cx, cy, _ = center
    hw, hh = w / 2, h / 2
    slot_d = w * 0.23
    slot_hh = hh * 0.40
    pts = [
        [cx - hw, cy + hh, 0],
        [cx + hw, cy + hh, 0],
        [cx + hw, cy - hh, 0],
        [cx - hw, cy - hh, 0],
        [cx - hw, cy - slot_hh, 0],
        [cx - hw + slot_d, cy - slot_hh, 0],
        [cx - hw + slot_d, cy + slot_hh, 0],
        [cx - hw, cy + slot_hh, 0],
    ]
    poly = Polygon(*pts, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill_opacity)
    slot_center = np.array([cx - hw + slot_d * 0.45, cy, 0.0])
    return poly, slot_center, slot_d, slot_hh * 2


def build_pkc(center=(0, 0, 0), w=3.2, h=2.1, open_frac=0.0, c2_color=TEAL, c1_color=TEAL,
              pkc_color=TEAL, show_labels=True, label_size=24, show_ps_label=True,
              c2_text="C2", c1_text="C1", glow=0.0, always_halo=False):
    """Build the continuous 4-block conventional (or novel/atypical) PKC cartoon.

    Topology (single chain): pseudosubstrate -> C1 -> C2 -> kinase.
    """
    cx, cy, _ = np.array(center, dtype=float)
    wide = (len(c1_text) > 3) or (len(c2_text) > 3)
    c1_pos = np.array([cx - (0.31 if wide else 0.28) * w, cy + 0.30 * h, 0.0])
    c2_pos = np.array([cx + (0.31 if wide else 0.28) * w, cy + 0.30 * h, 0.0])
    kin_pos = np.array([cx + 0.22 * w, cy - 0.26 * h, 0.0])

    c1_w = w * (0.49 if len(c1_text) > 3 else 0.36)
    c2_w = w * (0.49 if len(c2_text) > 3 else 0.36)
    c1_h = h * 0.30
    c2_h = h * 0.30
    kin_w = w * 0.56
    kin_h = h * 0.43

    c1_box = RoundedRectangle(corner_radius=0.10, width=c1_w, height=c1_h,
                              stroke_color=c1_color, stroke_width=3.5,
                              fill_color=c1_color, fill_opacity=0.22).move_to(c1_pos)
    c2_box = RoundedRectangle(corner_radius=0.10, width=c2_w, height=c2_h,
                              stroke_color=c2_color, stroke_width=3.5,
                              fill_color=c2_color, fill_opacity=0.22).move_to(c2_pos)
    kin_box, slot_center, slot_d, slot_h = _kinase_with_slot(kin_pos, kin_w, kin_h, color=pkc_color,
                                                             fill_opacity=0.22 + 0.20 * glow)

    ps_w = max(slot_d * 1.08, w * 0.14)
    ps_h = slot_h * 0.80
    ps_closed = slot_center + LEFT * (ps_w * 0.14)
    ps_open = slot_center + LEFT * (w * 0.62) + DOWN * (h * 0.20)
    ps_pos = (1.0 - open_frac) * ps_closed + open_frac * ps_open
    ps_box = RoundedRectangle(corner_radius=0.07, width=ps_w, height=ps_h,
                              stroke_color=pkc_color, stroke_width=3,
                              fill_color=pkc_color, fill_opacity=0.35).move_to(ps_pos)

    c1_attach = (c1_box.get_bottom() + LEFT * (c1_w * 0.36)) if open_frac > 0.3 else (c1_box.get_bottom() + LEFT * (c1_w * 0.10))
    l1 = Line(ps_box.get_top(), c1_attach, color=pkc_color, stroke_width=4)
    l2 = Line(c1_box.get_right(), c2_box.get_left(), color=pkc_color, stroke_width=4)
    l3 = Line(c2_box.get_bottom() + RIGHT * (c2_w * 0.10), kin_box.get_top() + RIGHT * (kin_w * 0.15),
              color=pkc_color, stroke_width=4)

    g = VGroup()
    if always_halo or glow > 0.05:
        op = min(0.95, glow) if glow > 0.05 else 0.0
        halo = SurroundingRectangle(kin_box, buff=0.10, corner_radius=0.16,
                                    stroke_color=YELLOW, stroke_width=3 + 4 * glow,
                                    stroke_opacity=op, fill_opacity=0)
        halo.layout_ok = True
        g.add(halo)
        g.halo = halo

    g.add(l1, l2, l3, kin_box, c1_box, c2_box, ps_box)

    if show_labels:
        lc1 = T(c1_text, label_size, TEXT).move_to(c1_box)
        lc2 = T(c2_text, label_size, TEXT).move_to(c2_box)
        lkin = T("kinase", label_size, TEXT).move_to(kin_pos + RIGHT * (slot_d * 0.45))
        g.add(lc1, lc2, lkin)
        g.c1_label, g.c2_label, g.kin_label = lc1, lc2, lkin
        if show_ps_label:
            ps_sz = max(24, label_size - 2)
            if open_frac < 0.5:
                lps = T("pseudosubstrate", ps_sz, TEXT).next_to(ps_box, LEFT, buff=0.18)
            else:
                lps = T("pseudosubstrate", ps_sz, TEXT).next_to(ps_box, DOWN, buff=0.18)
            g.add(lps)
            g.ps_label = lps

    g.c1, g.c2, g.kinase, g.ps = c1_box, c2_box, kin_box, ps_box
    g.links = VGroup(l1, l2, l3)
    g.slot_center = slot_center
    return g


def build_substrate(pos, w=1.0, h=0.50, phosphorylated=False, label="substrate", label_size=24):
    """Build a neutral substrate protein block sized to its label, optionally with a GOLD phosphate badge."""
    lab = T(label, label_size, TEXT) if label else None
    bw = max(w, (lab.width + 0.30) if lab is not None else w)
    bh = max(h, (lab.height + 0.26) if lab is not None else h)
    box = RoundedRectangle(corner_radius=0.09, width=bw, height=bh, stroke_color=TEXT, stroke_width=2.5,
                           fill_color=TEXT, fill_opacity=0.18).move_to(pos)
    g = VGroup(box)
    if lab is not None:
        lab.move_to(box)
        g.add(lab)
        g.label = lab
    if phosphorylated:
        p_circ = Circle(radius=0.19, stroke_color=BG, stroke_width=2,
                        fill_color=GOLD, fill_opacity=1.0).move_to(box.get_top() + UP * 0.24)
        p_txt = T("P", 22, BG, weight=BOLD).move_to(p_circ)
        p_txt.layout_ok = True
        g.add(p_circ, p_txt)
        g.phosphate = VGroup(p_circ, p_txt)
    g.box = box
    return g


def build_legend(items, top_left=(-6.1, -3.20), size=22):
    """Compact horizontal colour legend chip row."""
    row = VGroup()
    for name, col in items:
        sw = Square(side_length=0.22, stroke_width=0, fill_color=col, fill_opacity=0.95)
        tx = T(name, size, col)
        row.add(VGroup(sw, tx).arrange(RIGHT, buff=0.09))
    row.arrange(RIGHT, buff=0.28)
    row.move_to([top_left[0], top_left[1], 0.0], aligned_edge=LEFT)
    return row


def _ca_swarm(origin, n, rng, max_rise=2.5, spread_x=2.0):
    """Precompute fixed-seed calcium trajectories rising from the ER channel."""
    pts0, vels = [], []
    for _ in range(n):
        x0 = origin[0] + rng.uniform(-0.16, 0.16)
        y0 = origin[1] + rng.uniform(0.08, 0.30)
        vx = rng.uniform(-spread_x * 0.22, spread_x * 0.28)
        vy = rng.uniform(0.45, max_rise * 0.42)
        pts0.append(np.array([x0, y0, 0.0]))
        vels.append(np.array([vx, vy, 0.0]))
    return pts0, vels


# =====================================================================
# SCENE 0: Hook / Link Question (spoken, 21.2 s)
# =====================================================================
class S00LinkQuestion(SpokenScene):
    def construct(self):
        mem = build_membrane(y_bot=1.95, y_top=2.45, anionic_span=(-0.6, 3.6), show_anionic_label=False)
        er = build_er(gate_open=1.0)
        dag_t = ValueTracker(0.0)
        dag_base = np.array([1.8, 2.13, 0.0])
        dag = always_redraw(lambda: build_dag(
            dag_base + RIGHT * 0.16 * np.sin(1.7 * dag_t.get_value()),
            label="DAG", label_y=mem.y_top + 0.28
        ))

        ip3_p = ValueTracker(0.0)
        p0 = np.array([-3.3, 1.85, 0.0])
        p1 = np.array([-4.3, 0.9, 0.0])
        p2 = np.array([-2.3, 0.1, 0.0])
        p3 = er.gate_pos + UP * 0.15
        path_curve = CubicBezier(p0, p1, p2, p3, stroke_color=BLUE, stroke_width=3.5,
                                 stroke_opacity=0.55, fill_opacity=0.0)
        path_curve.layout_ok = True

        def ip3_pos():
            s = ip3_p.get_value() % 1.0
            u = 1.0 - s
            return (u**3) * p0 + 3 * (u**2) * s * p1 + 3 * u * (s**2) * p2 + (s**3) * p3

        ip3_dot = always_redraw(lambda: Dot(ip3_pos(), radius=0.14, color=BLUE))
        ip3_lab = T("IP3", 26, BLUE).move_to([-5.0, 1.25, 0])

        rng = np.random.default_rng(7)
        pts0, vels = _ca_swarm(er.gate_pos, 12, rng, max_rise=2.3, spread_x=1.6)
        ca_clock = ValueTracker(0.0)

        def make_ca():
            t = ca_clock.get_value()
            g = VGroup()
            for i, (q0, v) in enumerate(zip(pts0, vels)):
                phase = (t * 0.55 + i * 0.11) % 1.0
                pos = q0 + np.array([v[0] * phase * 2.0, v[1] * phase * 2.0, 0.0])
                g.add(Dot(pos, radius=0.11, color=GREEN))
            return g

        ca_dots = always_redraw(make_ca)
        ca_lab = T("calcium", 26, GREEN).move_to([-1.15, -0.05, 0])

        tag = scope_tag("schematic")
        self.add(mem, er, path_curve, ip3_dot, ip3_lab, ca_dots, ca_lab, dag, tag)

        self.play(ip3_p.animate.set_value(0.95), ca_clock.animate.set_value(1.8),
                  dag_t.animate.set_value(3.2), run_time=self.t_of("in the membrane") - 0.1,
                  rate_func=linear)

        self.at("How can conventional")
        pkc = build_pkc(center=(3.2, -0.35, 0), w=3.2, h=2.15, open_frac=0.0,
                        c2_color=TEAL, c1_color=TEAL, show_labels=True, label_size=24, show_ps_label=True)
        pkc_tag = T("conventional PKC", 28, TEAL).next_to(pkc.kinase, DOWN, buff=0.22)
        q_card = fit_text("How can conventional PKC use both branches?", max_w=9.8, size=28, color=GOLD).move_to([-0.6, -3.15, 0])
        arr_ca = Arrow(ca_lab.get_right() + RIGHT * 0.12, pkc.c1.get_left() + LEFT * 0.16,
                       buff=0.04, color=GREEN, stroke_width=5)
        arr_dag = Arrow([dag_base[0], 1.85, 0], pkc.c1.get_top() + UP * 0.14,
                        buff=0.04, color=ORANGE, stroke_width=5)
        arr_ca.layout_ok = True
        arr_dag.layout_ok = True

        self.play(
            FadeIn(pkc, shift=LEFT * 0.3),
            FadeIn(pkc_tag),
            FadeIn(q_card),
            GrowArrow(arr_ca),
            GrowArrow(arr_dag),
            ca_clock.animate.set_value(3.0),
            dag_t.animate.set_value(5.0),
            ip3_p.animate.set_value(1.5),
            run_time=2.0,
            rate_func=linear,
        )

        self.at("The branches reach")
        loc_cyto = T("cytosol", 24, GREEN).next_to(ca_lab, DOWN, buff=0.22)
        loc_mem = T("membrane", 24, ORANGE).move_to([3.7, 1.62, 0])
        self.play(
            FadeIn(loc_cyto), FadeIn(loc_mem),
            ca_clock.animate.set_value(4.8),
            dag_t.animate.set_value(8.0),
            ip3_p.animate.set_value(2.1),
            run_time=2.4,
            rate_func=linear,
        )

        self.at("Return to the same")
        self.play(
            FadeOut(arr_ca), FadeOut(arr_dag), FadeOut(loc_cyto), FadeOut(loc_mem),
            ca_clock.animate.set_value(6.5),
            dag_t.animate.set_value(11.0),
            ip3_p.animate.set_value(2.7),
            run_time=2.4,
            rate_func=linear,
        )

        rem = max(0.3, self.narration_s + 0.4 - self.elapsed())
        self.play(
            ca_clock.animate.set_value(6.5 + rem * 0.7),
            dag_t.animate.set_value(11.0 + rem * 1.6),
            ip3_p.animate.set_value(2.7 + rem * 0.35),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


# =====================================================================
# SCENE 1: Title Card (silent, 2.0 s)
# =====================================================================
class S01Title(TitleCard):
    LESSON = "PLC, IP3, DAG and Protein Kinase C"
    TITLE = "How Conventional PKC Reads Both Branches"


# =====================================================================
# SCENE 2: Closed PKC at Rest (spoken, 21.15 s)
# =====================================================================
class S02Closed(SpokenScene):
    def construct(self):
        pkc = build_pkc(center=(-0.1, 0.25, 0), w=6.8, h=4.4, open_frac=0.0,
                        c2_color=TEAL, c1_color=TEAL, show_labels=True, label_size=30, show_ps_label=True)
        active_lab = T("active site", 26, YELLOW).move_to(pkc.slot_center + DOWN * 1.48 + RIGHT * 0.25)
        active_arr = Arrow(active_lab.get_top() + UP * 0.06, pkc.slot_center + DOWN * 0.45,
                           buff=0.04, color=YELLOW, stroke_width=4)
        active_arr.layout_ok = True

        self.play(FadeIn(pkc, scale=0.88), run_time=3.0)
        self.at("Its pseudosubstrate")
        self.play(FadeIn(active_lab), GrowArrow(active_arr),
                  pkc.ps.animate.set_fill(TEAL, opacity=0.55), run_time=1.8)

        self.at("blocking real substrates")
        # Shift pseudosubstrate label down slightly during approach so substrate enters cleanly at slot y
        sub_y = pkc.slot_center[1]
        sub_start = np.array([-5.2, sub_y, 0.0])
        sub = build_substrate(pos=sub_start, w=1.9, h=0.82, label_size=26)
        bump_pt = np.array([pkc.ps.get_left()[0] - sub.width / 2 - 0.25, sub_y, 0.0])
        self.play(pkc.ps_label.animate.shift(DOWN * 0.72), FadeIn(sub), run_time=0.4)
        self.play(sub.animate.move_to(bump_pt), run_time=0.85, rate_func=rush_into)
        self.play(sub.animate.move_to(sub_start), run_time=0.95, rate_func=rush_from)
        self.play(FadeOut(sub), pkc.ps_label.animate.shift(UP * 0.72), run_time=0.35)

        self.at("All four parts")
        seg1 = Line(pkc.links[0].get_start(), pkc.links[0].get_end(), color=YELLOW, stroke_width=9)
        seg2 = Line(pkc.links[1].get_start(), pkc.links[1].get_end(), color=YELLOW, stroke_width=9)
        seg3 = Line(pkc.links[2].get_start(), pkc.links[2].get_end(), color=YELLOW, stroke_width=9)
        for s in (seg1, seg2, seg3):
            s.layout_ok = True
        self.play(Create(seg1), pkc.c1.animate.set_fill(TEAL, opacity=0.45), run_time=0.9)
        self.play(Create(seg2), pkc.c2.animate.set_fill(TEAL, opacity=0.45), run_time=0.9)
        self.play(Create(seg3), pkc.kinase.animate.set_fill(TEAL, opacity=0.45), run_time=0.9)
        self.play(FadeOut(seg1), FadeOut(seg2), FadeOut(seg3),
                  pkc.c1.animate.set_fill(TEAL, opacity=0.22),
                  pkc.c2.animate.set_fill(TEAL, opacity=0.22),
                  pkc.kinase.animate.set_fill(TEAL, opacity=0.22),
                  run_time=0.6)

        self.at("C2 domain can")
        c2_ring = SurroundingRectangle(pkc.c2, buff=0.05, corner_radius=0.12, color=GREEN, stroke_width=6)
        c2_ring.layout_ok = True
        ca_hint = T("responds to Ca²⁺", 26, GREEN).next_to(pkc.c2, RIGHT, buff=0.25)
        ca_icons = VGroup(*[Dot(pkc.c2.get_top() + UP * 0.28 + RIGHT * (0.30 * i), radius=0.13, color=GREEN)
                            for i in (-1, 0, 1)])
        self.play(pkc.c2.animate.set_stroke(GREEN, 5).set_fill(GREEN, opacity=0.32),
                  Create(c2_ring), FadeIn(ca_hint),
                  FadeIn(ca_icons, shift=DOWN * 0.4), run_time=2.6)

        self.at("C1 domain can")
        c1_ring = SurroundingRectangle(pkc.c1, buff=0.05, corner_radius=0.12, color=ORANGE, stroke_width=6)
        c1_ring.layout_ok = True
        dag_hint = T("recognizes DAG", 26, ORANGE).next_to(pkc.c1, LEFT, buff=0.25)
        self.play(pkc.c1.animate.set_stroke(ORANGE, 5).set_fill(ORANGE, opacity=0.32),
                  Create(c1_ring), FadeIn(dag_hint), run_time=2.5)

        self.finish()


# =====================================================================
# SCENE 3: Calcium Targets C2 to Membrane (spoken, 23.575 s)
# =====================================================================
class S03Calcium(SpokenScene):
    def construct(self):
        mem = build_membrane(y_bot=1.95, y_top=2.45, anionic_span=(-0.4, 4.2), show_anionic_label=True)
        er = build_er(gate_open=0.0)
        dag = build_dag(np.array([-2.2, 2.13, 0.0]), label="DAG", label_y=mem.y_top + 0.28)
        pkc_start = np.array([2.5, -1.15, 0.0])
        pkc = build_pkc(center=pkc_start, w=3.2, h=2.15, open_frac=0.0,
                        c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=24, show_ps_label=True)
        tag = scope_tag("schematic")
        self.add(mem, er, dag, pkc, tag)

        # IP3 moves along visible trail to above the ER gate and opens it
        ip3_dest = er.gate_pos + UP * 0.45
        ip3 = Dot([-3.8, 1.75, 0], radius=0.18, color=BLUE)
        ip3_lab = T("IP3", 26, BLUE).next_to(ip3, LEFT, buff=0.20)
        ip3_path = Line([-3.8, 1.75, 0], ip3_dest, color=BLUE, stroke_width=5).set_stroke(opacity=0.7)
        ip3_path.layout_ok = True
        self.play(FadeIn(ip3), FadeIn(ip3_lab), run_time=0.4)
        self.play(
            Create(ip3_path),
            ip3.animate.move_to(ip3_dest),
            ip3_lab.animate.next_to(ip3_dest, LEFT, buff=0.25),
            run_time=2.2,
        )
        self.play(
            er.posts[0].animate.shift(LEFT * 0.28),
            er.posts[1].animate.shift(RIGHT * 0.28),
            FadeOut(ip3), FadeOut(ip3_lab), FadeOut(ip3_path),
            run_time=0.8,
        )

        self.at("raising cytosolic calcium")
        rng = np.random.default_rng(11)
        pts0, vels = _ca_swarm(er.gate_pos, 18, rng, max_rise=2.9, spread_x=2.2)
        ca_clock = ValueTracker(0.0)

        def make_stream():
            t = ca_clock.get_value()
            g = VGroup()
            for i, (q0, v) in enumerate(zip(pts0, vels)):
                ph = (t * 0.65 + i * 0.07) % 1.0
                g.add(Dot(q0 + np.array([v[0] * ph * 2.2, v[1] * ph * 2.2, 0.0]), radius=0.13, color=GREEN))
            return g

        stream = always_redraw(make_stream)
        ca_lab = T("Ca²⁺", 26, GREEN).move_to([-5.2, 0.35, 0])
        self.add(stream)
        self.play(FadeIn(ca_lab), ca_clock.animate.set_value(2.8), run_time=2.8, rate_func=linear)

        self.at("Calcium binds C2")
        c2_offsets = [np.array([-0.28, 0.30, 0]), np.array([0.0, 0.33, 0]), np.array([0.28, 0.30, 0])]
        bound_ca = VGroup(*[Dot(er.gate_pos + UP * 0.6 + RIGHT * (0.7 * i), radius=0.13, color=GREEN) for i in range(3)])
        self.add(bound_ca)
        targets = [pkc.c2.get_center() + off for off in c2_offsets]
        self.play(
            *[d.animate.move_to(t) for d, t in zip(bound_ca, targets)],
            pkc.c2.animate.set_stroke(GREEN, 6).set_fill(GREEN, opacity=0.35),
            ca_clock.animate.set_value(5.6),
            run_time=3.2,
            rate_func=linear,
        )

        self.at("C2 then engages")
        dy = (mem.patch.get_bottom()[1] - 0.05) - pkc.c2.get_top()[1]
        dx = -0.3
        shift_vec = np.array([dx, dy, 0.0])
        pkc_and_ca = VGroup(pkc, bound_ca)
        self.play(
            pkc_and_ca.animate.shift(shift_vec),
            ca_clock.animate.set_value(10.0),
            run_time=5.4,
            rate_func=smooth,
        )

        self.at("close enough to sample")
        probe = Arrow(pkc.c1.get_left() + LEFT * 0.55, pkc.c1.get_left() + LEFT * 0.05,
                      buff=0, color=ORANGE, stroke_width=5)
        probe.layout_ok = True
        rem = max(0.3, self.narration_s + 0.4 - self.elapsed())
        self.play(
            GrowArrow(probe),
            ca_clock.animate.set_value(10.0 + rem * 0.9),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


# =====================================================================
# SCENE 4: C1 Scans Membrane and Grips DAG (spoken, 15.55 s)
# =====================================================================
class S04Dag(SpokenScene):
    def construct(self):
        mem = build_membrane(y_bot=1.85, y_top=2.45, anionic_span=(-0.2, 5.2), show_anionic_label=True)
        dag_pos = np.array([-2.3, 2.04, 0.0])
        dag = build_dag(dag_pos, width=0.80, height=0.38, label="DAG", label_y=mem.y_top + 0.28)
        tag = scope_tag("schematic")

        scan_x = ValueTracker(0.75)
        open_f = ValueTracker(0.0)
        glow_f = ValueTracker(0.0)

        def make_pkc():
            sx = scan_x.get_value()
            op = open_f.get_value()
            gl = glow_f.get_value()
            p = build_pkc(center=(sx, 0.15, 0), w=5.0, h=3.1, open_frac=op,
                          c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=26,
                          show_ps_label=True, glow=gl, always_halo=True)
            dy = (mem.patch.get_bottom()[1] - 0.05) - p.c2.get_top()[1]
            p.shift(UP * dy)
            for dx in (-0.35, 0.0, 0.35):
                p.add(Dot(p.c2.get_center() + np.array([dx, 0.34, 0]), radius=0.12, color=GREEN))
            return p

        pkc = always_redraw(make_pkc)
        self.add(mem, dag, pkc, tag)

        self.at("C1 can search")
        self.play(scan_x.animate.set_value(-0.1), run_time=0.9, rate_func=smooth)
        self.play(scan_x.animate.set_value(0.35), run_time=0.7, rate_func=smooth)

        # Align C1 directly beneath DAG (c1_x = sx - 0.28 * 5.0 = sx - 1.40 -> sx = -0.90)
        self.at("binding strengthens")
        self.play(scan_x.animate.set_value(-0.90), run_time=1.4, rate_func=smooth)

        self.at("displace the pseudosubstrate")
        self.play(open_f.animate.set_value(1.0), glow_f.animate.set_value(0.9), run_time=2.4, rate_func=smooth)

        self.at("The active site opens")
        self.at("phosphorylate protein substrates")
        static_open = build_pkc(center=(-0.90, 0.15, 0), w=5.0, h=3.1, open_frac=1.0)
        dy0 = (mem.patch.get_bottom()[1] - 0.05) - static_open.c2.get_top()[1]
        slot_pt = static_open.slot_center + UP * dy0

        sub_unp = build_substrate(pos=np.array([static_open.kinase.get_left()[0] - 0.95, -2.55, 0.0]),
                                  w=1.5, h=0.62, phosphorylated=False, label_size=24)
        dock_pt = np.array([static_open.kinase.get_left()[0] - sub_unp.box.width / 2 - 0.14,
                            slot_pt[1], 0.0])
        sub_pho = build_substrate(pos=dock_pt, w=1.5, h=0.62, phosphorylated=True, label_size=24)
        self.play(FadeIn(sub_unp), run_time=0.4)
        self.play(sub_unp.animate.move_to(dock_pt), run_time=1.4, rate_func=smooth)
        self.remove(sub_unp)
        self.add(sub_pho)
        self.play(sub_pho.animate.move_to([dock_pt[0], -2.45, 0.0]), run_time=1.8, rate_func=smooth)
        self.finish()


# =====================================================================
# THREE-PANEL HELPER FOR S05 / S06 / S07
# =====================================================================
def build_three_condition_panels():
    """Build the three carried membrane panels: 'calcium', 'DAG', 'calcium + DAG'."""
    xs = [-4.2, 0.0, 4.2]
    titles = ["calcium", "DAG", "calcium + DAG"]
    cols = [GREEN, ORANGE, TEAL]
    panels = []
    for x, ttl, col in zip(xs, titles, cols):
        frame = RoundedRectangle(corner_radius=0.16, width=3.9, height=5.1,
                                 stroke_color=col, stroke_width=2.5,
                                 fill_color=BG, fill_opacity=0.0).move_to([x, -0.05, 0])
        head = T(ttl, 28, col).move_to([x, 2.15, 0])
        mem = build_membrane(y_bot=1.32, y_top=1.72, x0=x - 1.75, x1=x + 1.75,
                             label="", anionic_span=(x - 1.1, x + 1.1), show_anionic_label=False)
        pkc = build_pkc(center=(x, -1.00, 0), w=2.65, h=1.80, open_frac=0.0,
                        c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=24,
                        show_ps_label=False)
        g = VGroup(frame, head, mem, pkc)
        g.frame, g.head, g.mem, g.pkc = frame, head, mem, pkc
        g.x = x
        panels.append(g)
    return panels


def _populate_panel_inputs(panels):
    """Return deterministic inputs (Ca2+ dots, DAG block, both) for panels 0, 1, 2."""
    rng = np.random.default_rng(13)
    # Place panel 0 Ca2+ dots cleanly left of C2's text zone or below C1/C2 path so C2 never sits on a dot
    ca0 = VGroup(*[Dot([panels[0].x + rng.uniform(-1.35, -0.15), rng.uniform(-0.05, 0.85), 0],
                       radius=0.09, color=GREEN) for _ in range(7)])
    dag1 = build_dag([panels[1].x - 0.74, 1.48, 0], width=0.50, height=0.32, label="", striped=False)
    ca2 = VGroup(*[Dot([panels[2].x + rng.uniform(0.15, 1.15), rng.uniform(0.05, 0.95), 0],
                       radius=0.09, color=GREEN) for _ in range(7)])
    dag2 = build_dag([panels[2].x - 0.74, 1.48, 0], width=0.50, height=0.32, label="", striped=False)
    return ca0, dag1, ca2, dag2


# =====================================================================
# SCENE 5: Predict Three Conditions (spoken, 15.275 s)
# =====================================================================
class S05Predict(SpokenScene):
    def construct(self):
        panels = build_three_condition_panels()
        ca0, dag1, ca2, dag2 = _populate_panel_inputs(panels)
        tag = scope_tag("schematic")
        self.play(*[FadeIn(p) for p in panels], FadeIn(tag), run_time=1.0)

        self.at("calcium without")
        self.play(FadeIn(ca0), panels[0].frame.animate.set_stroke(width=4), run_time=1.2)

        self.at("without raised calcium")
        self.play(FadeIn(dag1), panels[1].frame.animate.set_stroke(width=4), run_time=1.2)

        self.at("both branches together")
        self.play(FadeIn(ca2), FadeIn(dag2), panels[2].frame.animate.set_stroke(width=4), run_time=1.4)

        self.at("Which condition should")
        q = question_card("Strongest membrane retention?", y=3.15, size=34, max_w=11.0)
        self.play(FadeIn(q), run_time=1.2)
        # Briefly highlight each panel option in turn as the question finishes
        for p, col in zip(panels, (GREEN, ORANGE, TEAL)):
            self.play(p.frame.animate.set_fill(col, opacity=0.10), run_time=0.8)
            self.play(p.frame.animate.set_fill(BG, opacity=0.0), run_time=0.8)
        self.finish()


# =====================================================================
# SCENE 6: Predict Pause (silent, 4.5 s)
# =====================================================================
class S06Pause(PredictPause):
    QUESTION = "Strongest membrane retention?"
    SECONDS = 4.5
    CARD = {"y": 3.15, "size": 34, "max_w": 11.0}
    RING_AT = (5.9, 3.15, 0)

    def backdrop(self):
        panels = build_three_condition_panels()
        for p in panels:
            p.frame.set_stroke(width=4)
        ca0, dag1, ca2, dag2 = _populate_panel_inputs(panels)
        return VGroup(*panels, ca0, dag1, ca2, dag2, scope_tag("schematic"))


# =====================================================================
# SCENE 7: Cooperation / Synergy (spoken, 20.125 s)
# =====================================================================
class S07Cooperation(SpokenScene):
    def construct(self):
        panels = build_three_condition_panels()
        for p in panels:
            p.frame.set_stroke(width=4)
        ca0, dag1, ca2, dag2 = _populate_panel_inputs(panels)
        tag = scope_tag("schematic")
        self.add(*panels, ca0, dag1, ca2, dag2, tag)

        # Panel 0 (calcium only): C2 touches membrane briefly, then drifts back -> 'weaker'
        dy0 = (panels[0].mem.patch.get_bottom()[1] - 0.05) - panels[0].pkc.c2.get_top()[1]
        self.play(panels[0].pkc.animate.shift(UP * dy0), run_time=1.0, rate_func=smooth)
        self.play(panels[0].pkc.animate.shift(DOWN * (dy0 * 0.85)), run_time=1.1, rate_func=smooth)
        w0 = T("weaker", 28, TEXT).move_to([panels[0].x, -2.2, 0])
        arr0 = Arrow([panels[0].x + 1.48, -1.6, 0], [panels[0].x + 1.48, -0.5, 0],
                     buff=0, color=GREEN, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        arr0.layout_ok = True
        self.play(FadeIn(w0), GrowArrow(arr0), run_time=0.6)

        # Panel 1 (DAG only): C1 samples briefly and releases -> 'weaker'
        dy1 = (dag1.block.get_bottom()[1] - 0.06) - panels[1].pkc.c1.get_top()[1]
        self.play(panels[1].pkc.animate.shift(UP * dy1), run_time=1.0, rate_func=smooth)
        self.play(panels[1].pkc.animate.shift(DOWN * (dy1 * 0.85)), run_time=1.1, rate_func=smooth)
        w1 = T("weaker", 28, TEXT).move_to([panels[1].x, -2.2, 0])
        arr1 = Arrow([panels[1].x + 1.48, -1.6, 0], [panels[1].x + 1.48, -0.5, 0],
                     buff=0, color=ORANGE, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        arr1.layout_ok = True
        self.play(FadeIn(w1), GrowArrow(arr1), run_time=0.6)

        # Panel 2 (calcium + DAG): C2 and C1 engage together -> stays, unfolds, phosphorylates -> 'stronger'
        self.at("Together their binding")
        dy2 = (dag2.block.get_bottom()[1] - 0.06) - panels[2].pkc.c1.get_top()[1]
        arr2 = Arrow([panels[2].x + 1.55, -1.6, 0], [panels[2].x + 1.55, 1.15, 0],
                     buff=0, color=TEAL, stroke_width=7, max_tip_length_to_length_ratio=0.16)
        arr2.layout_ok = True
        self.play(
            panels[2].pkc.animate.shift(UP * dy2),
            ca2.animate.shift(UP * 0.25),
            GrowArrow(arr2),
            run_time=2.5,
            rate_func=smooth,
        )

        self.at("Conventional PKC gives")
        open_pkc2 = build_pkc(center=(panels[2].x, -1.00 + dy2, 0), w=2.65, h=1.80, open_frac=1.0,
                              c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=24,
                              show_ps_label=False, glow=0.8)
        s2 = T("stronger", 30, TEAL, weight=BOLD).move_to([panels[2].x, -2.27, 0])
        self.play(Transform(panels[2].pkc, open_pkc2), FadeIn(s2), run_time=2.6)

        sub_x = open_pkc2.kinase.get_left()[0] - 0.45
        sub_home = np.array([sub_x, -1.52, 0])
        sub = build_substrate(pos=sub_home, w=0.72, h=0.44, phosphorylated=False, label="sub.", label_size=24)
        dock_pt = np.array([open_pkc2.kinase.get_left()[0] - sub.box.width / 2 - 0.08,
                            open_pkc2.slot_center[1], 0.0])
        sub_p = build_substrate(pos=dock_pt, w=0.72, h=0.44, phosphorylated=True, label="sub.", label_size=24)
        self.play(FadeIn(sub), run_time=0.6)
        self.play(sub.animate.move_to(dock_pt), run_time=2.4)
        self.remove(sub)
        self.add(sub_p)
        self.play(sub_p.animate.move_to([dock_pt[0], -1.52, 0]), run_time=2.6)
        self.finish()


# =====================================================================
# SCENE 8: Graded Timing Detector (spoken, 17.375 s)
# =====================================================================
class S08Timing(SpokenScene):
    def construct(self):
        mem = build_membrane(y_bot=2.10, y_top=2.55, x0=-5.9, x1=5.9,
                             label="plasma membrane", anionic_span=(-0.8, 3.8), show_anionic_label=False)
        tag = scope_tag("schematic")

        ca_fn = lambda t: 0.88 * np.exp(-((t - 3.0) / 1.55) ** 2) if t < 3.0 else 0.88 * np.exp(-((t - 3.0) / 2.2) ** 2)
        dag_fn = lambda t: 0.85 * np.exp(-((t - 5.2) / 1.45) ** 2) if t < 5.2 else 0.85 * np.exp(-((t - 5.2) / 2.1) ** 2)
        act_fn = lambda t: 1.35 * ca_fn(t) * dag_fn(t) / (0.32 + ca_fn(t) * dag_fn(t))

        P = Plot(box=(-5.4, 5.4, -3.00, -0.75), xr=(0, 10), yr=(0, 0.98),
                 xticks=(), yticks=(), xlabel="time (schematic)", ylabel="level", color=TEXT)
        t_tr = ValueTracker(0.0)

        ca_curve = P.live_curve(ca_fn, t_tr, color=GREEN, width=5)
        dag_curve = P.live_curve(dag_fn, t_tr, color=ORANGE, width=5)
        act_curve = P.live_curve(act_fn, t_tr, color=TEAL, width=7)
        cursor = always_redraw(lambda: DashedLine(
            P.pt(t_tr.get_value(), 0), P.pt(t_tr.get_value(), 0.96),
            color=TEXT, stroke_width=2, dash_length=0.10
        ))

        leg = VGroup(
            T("calcium", 26, GREEN),
            T("DAG", 26, ORANGE),
            T("PKC activity", 26, TEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.3, 0.85, 0])

        dag_pos = np.array([-2.0, 2.26, 0.0])

        def live_dag():
            d_lvl = dag_fn(t_tr.get_value())
            op = float(np.clip(d_lvl / 0.35, 0.0, 1.0))
            return build_dag(dag_pos, width=0.62, height=0.34, label="DAG",
                             label_y=mem.y_top + 0.28).set_opacity(op)

        def live_pkc():
            tv = t_tr.get_value()
            c_lvl = ca_fn(tv)
            d_lvl = dag_fn(tv)
            a_lvl = act_fn(tv)
            lift = float(np.clip(c_lvl / 0.45, 0.0, 1.0))
            unfold = float(np.clip(a_lvl / 0.70, 0.0, 1.0))
            # Keep C1/C2/Ca2+ dots cleanly below mem.y_bot = 2.10 at peak lift
            cy = 0.20 + 0.72 * lift
            cx = -0.35 - 0.75 * float(np.clip(d_lvl / 0.4, 0.0, 1.0)) * lift
            p = build_pkc(center=(cx, cy, 0), w=3.2, h=1.80, open_frac=unfold,
                          c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=24,
                          show_ps_label=False, glow=a_lvl, always_halo=True)
            n_ca = int(round(3 * np.clip(c_lvl / 0.45, 0.0, 1.0)))
            # Keep fixed submobject count across frames inside always_redraw
            for idx in range(3):
                d = Dot(p.c2.get_center() + np.array([(idx - 1) * 0.28, 0.36, 0]),
                        radius=0.09, color=GREEN).set_opacity(1.0 if idx < n_ca else 0.0)
                p.add(d)
            return p

        self.add(mem, P, leg, ca_curve, dag_curve, act_curve, cursor, always_redraw(live_dag), always_redraw(live_pkc), tag)

        self.at("Calcium can recruit")
        self.play(t_tr.animate.set_value(3.0), run_time=2.6, rate_func=linear)

        self.at("engages C1")
        self.play(t_tr.animate.set_value(5.3), run_time=2.0, rate_func=linear)

        self.at("The response is graded")
        self.play(t_tr.animate.set_value(7.2), run_time=2.2, rate_func=linear)

        self.at("The detector integrates")
        rem = max(0.3, self.narration_s + 0.4 - self.elapsed())
        self.play(t_tr.animate.set_value(9.8), run_time=rem, rate_func=linear)
        self.finish()


# =====================================================================
# SCENE 9: Three PKC Classes (spoken, 17.5 s)
# =====================================================================
class S09Classes(SpokenScene):
    def construct(self):
        xs = [-4.2, 0.0, 4.2]
        titles = ["conventional", "novel", "atypical"]
        tcols = [TEAL, ORANGE, TEXT]
        panels = []
        for x, ttl, col in zip(xs, titles, tcols):
            frame = RoundedRectangle(corner_radius=0.16, width=3.9, height=5.5,
                                     stroke_color=GREY, stroke_width=2,
                                     fill_opacity=0).move_to([x, 0.15, 0])
            head = T(ttl, 30, col, weight=BOLD).move_to([x, 2.55, 0])
            mem = build_membrane(y_bot=1.55, y_top=1.95, x0=x - 1.75, x1=x + 1.75,
                                 label="", anionic_span=None)
            panels.append((frame, head, mem))

        pkc_conv = build_pkc(center=(xs[0], -1.0, 0), w=2.8, h=1.80, open_frac=0.0,
                             c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=24,
                             show_ps_label=False)
        pkc_nov = build_pkc(center=(xs[1], -1.0, 0), w=2.8, h=1.80, open_frac=0.0,
                            c2_color=GREY, c1_color=ORANGE, show_labels=True, label_size=24,
                            show_ps_label=False, c2_text="C2-like")
        pkc_aty = build_pkc(center=(xs[2], -1.0, 0), w=2.8, h=1.80, open_frac=0.0,
                            c2_color=GREY, c1_color=GREY, show_labels=True, label_size=24,
                            show_ps_label=False, c2_text="reg.", c1_text="C1-like")

        tag = scope_tag("schematic")
        self.play(
            *[FadeIn(f) for f, _, _ in panels],
            *[FadeIn(h) for _, h, _ in panels],
            *[FadeIn(m) for _, _, m in panels],
            FadeIn(pkc_conv), FadeIn(pkc_nov), FadeIn(pkc_aty),
            FadeIn(tag),
            run_time=1.0,
        )

        # Conventional: Ca2+ + DAG
        ca_c = VGroup(*[Dot([xs[0] + dx, 0.85, 0], radius=0.09, color=GREEN) for dx in (0.45, 0.80, 1.15)])
        dag_c = build_dag([xs[0] - 0.78, 1.71, 0], width=0.50, height=0.30, label="")
        self.play(FadeIn(ca_c), FadeIn(dag_c), run_time=0.45)
        dy_c = (dag_c.block.get_bottom()[1] - 0.06) - pkc_conv.c1.get_top()[1]
        self.play(pkc_conv.animate.shift(UP * dy_c), ca_c.animate.shift(UP * 0.72), run_time=1.4)

        # Novel: DAG-driven recruitment without calcium
        self.at("Novel PKC has")
        dag_n = build_dag([xs[1] - 0.78, 1.71, 0], width=0.50, height=0.30, label="DAG", label_y=2.20)
        no_ca = T("no Ca²⁺ needed", 24, ORANGE).move_to([xs[1], -2.25, 0])
        self.play(FadeIn(dag_n), FadeIn(no_ca), run_time=0.6)
        self.at("recruitment without calcium")
        dy_n = (dag_n.block.get_bottom()[1] - 0.06) - pkc_nov.c1.get_top()[1]
        self.play(pkc_nov.animate.shift(UP * dy_n), run_time=2.0)

        # Atypical: neither messenger, uses protein partner
        self.at("responds to neither")
        neither = T("no Ca²⁺, no DAG", 24, TEXT).move_to([xs[2], -2.25, 0])
        self.play(FadeIn(neither), run_time=0.6)

        self.at("uses protein partners")
        partner_box = RoundedRectangle(corner_radius=0.12, width=2.55, height=0.62,
                                       stroke_color=YELLOW, stroke_width=2.5,
                                       fill_color=YELLOW, fill_opacity=0.18).move_to([xs[2], 1.15, 0])
        partner_lab = T("protein partner", 24, YELLOW).move_to(partner_box)
        partner = VGroup(partner_box, partner_lab)
        self.play(FadeIn(partner), run_time=0.8)
        dy_a = (partner_box.get_bottom()[1] - 0.07) - pkc_aty.c2.get_top()[1]
        self.play(pkc_aty.animate.shift(UP * dy_a), run_time=1.8)

        self.finish()


# =====================================================================
# SCENE 10: Phorbol Ester & Kinase Degradation (spoken, 17.05 s)
# =====================================================================
class S10Phorbol(SpokenScene):
    def construct(self):
        mem = build_membrane(y_bot=1.85, y_top=2.45, anionic_span=(-0.2, 4.2), show_anionic_label=False)
        dag_pos = np.array([-1.6, 2.04, 0.0])
        dag = build_dag(dag_pos, width=0.95, height=0.38, label="DAG", label_y=mem.y_top + 0.28, striped=False)
        phorbol = build_dag(dag_pos, width=1.15, height=0.38, label="phorbol ester", label_y=mem.y_top + 0.28, striped=True)
        tag = scope_tag("schematic")

        pkc = build_pkc(center=(-0.26, 0.15, 0), w=4.8, h=3.0, open_frac=1.0,
                        c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=26,
                        show_ps_label=True, glow=0.7)
        dy = (dag.block.get_bottom()[1] - 0.06) - pkc.c1.get_top()[1]
        pkc.shift(UP * dy)

        clock_c = np.array([4.4, 0.1, 0.0])
        clock_r = 1.25
        rim = Circle(radius=clock_r, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=0.8).move_to(clock_c)
        ticks = VGroup(*[
            Line(clock_c + clock_r * 0.84 * np.array([np.cos(a), np.sin(a), 0]),
                 clock_c + clock_r * 0.96 * np.array([np.cos(a), np.sin(a), 0]),
                 color=GREY, stroke_width=3)
            for a in np.linspace(0, TAU, 12, endpoint=False)
        ])
        ang = ValueTracker(PI / 2)
        min_hand = always_redraw(lambda: Line(
            clock_c, clock_c + clock_r * 0.72 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
            color=ORANGE, stroke_width=5
        ))
        hr_hand = always_redraw(lambda: Line(
            clock_c, clock_c + clock_r * 0.45 * np.array([np.cos(PI / 2 + (ang.get_value() - PI / 2) / 12.0),
                                                          np.sin(PI / 2 + (ang.get_value() - PI / 2) / 12.0), 0]),
            color=TEXT, stroke_width=6
        ))
        clock_lab = T("time", 26, TEXT).next_to(rim, DOWN, buff=0.22)
        clock = VGroup(rim, ticks, min_hand, hr_hand, clock_lab)

        self.add(mem, dag, pkc, tag)

        self.at("ester can occupy")
        self.play(FadeOut(dag), FadeIn(phorbol), run_time=0.8)

        self.at("activate PKC directly")
        self.play(FadeIn(clock), ang.animate.set_value(PI / 2 - TAU * 1.5), run_time=2.5, rate_func=linear)

        self.at("is cleared slowly")
        stay_lab = T("persists in C1", 26, ORANGE).move_to([-4.2, 1.30, 0])
        self.play(FadeIn(stay_lab), ang.animate.set_value(PI / 2 - TAU * 3.5), run_time=2.5, rate_func=linear)

        self.at("kinase degradation")
        rng = np.random.default_rng(19)
        frag_base = pkc.get_center()
        frags = VGroup()
        targets = []
        for _ in range(7):
            fw, fh = rng.uniform(0.55, 0.95), rng.uniform(0.32, 0.55)
            dx, dy_i = rng.uniform(-1.3, 1.3), rng.uniform(-0.8, 0.7)
            f = RoundedRectangle(corner_radius=0.07, width=fw, height=fh, stroke_color=TEAL,
                                 stroke_width=2.5, fill_color=TEAL, fill_opacity=0.35).move_to(frag_base + np.array([dx, dy_i, 0]))
            frags.add(f)
            targets.append(frag_base + np.array([dx * 1.35, dy_i - rng.uniform(1.1, 1.8), 0]))

        deg_lab = T("degradation", 30, TEAL, weight=BOLD).move_to([frag_base[0], -2.65, 0])
        self.play(FadeOut(pkc), FadeIn(frags), FadeIn(deg_lab), run_time=0.5)
        self.play(
            *[f.animate.move_to(t).set_opacity(0.45) for f, t in zip(frags, targets)],
            ang.animate.set_value(PI / 2 - TAU * 5.5),
            run_time=3.2,
            rate_func=linear,
        )

        rem = max(0.2, self.narration_s + 0.4 - self.elapsed())
        self.play(ang.animate.set_value(PI / 2 - TAU * 6.5), run_time=rem, rate_func=linear)
        self.finish()


# =====================================================================
# SCENE 11: Return to Membrane & Summary Rule (spoken, 20.075 s)
# =====================================================================
class S11Rule(SpokenScene):
    def construct(self):
        mem = build_membrane(y_bot=1.95, y_top=2.45, anionic_span=(0.5, 4.6), show_anionic_label=False)
        er = build_er(gate_open=1.0)
        dag = build_dag([1.40, 2.13, 0], width=0.58, height=0.36, label="DAG", label_y=mem.y_top + 0.28)
        legend = build_legend([("PIP2", GOLD), ("IP3", BLUE), ("DAG", ORANGE), ("Ca²⁺", GREEN), ("cPKC", TEAL)],
                              top_left=(-6.1, -3.20), size=22)
        tag = scope_tag("schematic")

        pkc = build_pkc(center=(2.4, -0.75, 0), w=3.6, h=2.2, open_frac=0.0,
                        c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=24, show_ps_label=False)
        rng = np.random.default_rng(23)
        ca_dots = VGroup(*[Dot([er.gate_pos[0] + rng.uniform(-0.3, 1.2), er.gate_pos[1] + rng.uniform(0.2, 0.9), 0],
                               radius=0.10, color=GREEN) for _ in range(6)])

        self.add(mem, er, dag, pkc, ca_dots, legend, tag)

        self.at("Calcium changes C2")
        dy = (dag.block.get_bottom()[1] - 0.06) - pkc.c1.get_top()[1]
        arr_targ = Arrow([-5.6, 1.05, 0], [-2.9, 0.65, 0], buff=0, color=GREEN, stroke_width=6)
        arr_targ.layout_ok = True
        lab_targ = T("targeting", 28, GREEN).move_to([-4.35, 1.42, 0])
        self.play(
            pkc.animate.shift(UP * dy),
            ca_dots.animate.shift(RIGHT * 2.8 + UP * 1.1),
            GrowArrow(arr_targ),
            FadeIn(lab_targ),
            run_time=2.5,
            rate_func=smooth,
        )

        self.at("changes C1")
        open_pkc = build_pkc(center=(2.4, -0.75 + dy, 0), w=3.6, h=2.2, open_frac=1.0,
                             c2_color=GREEN, c1_color=ORANGE, show_labels=True, label_size=24,
                             show_ps_label=False, glow=0.8)
        arr_act = Arrow([-5.6, -0.15, 0], [-2.9, 0.25, 0], buff=0, color=ORANGE, stroke_width=6)
        arr_act.layout_ok = True
        lab_act = T("activation", 28, ORANGE).move_to([-4.35, -0.52, 0])

        enter_pt = np.array([open_pkc.kinase.get_left()[0] - 0.72, -1.45, 0])
        sub = build_substrate(pos=enter_pt, w=1.2, h=0.48, phosphorylated=False, label="sub.", label_size=24)
        dock_pt = np.array([open_pkc.kinase.get_left()[0] - sub.box.width / 2 - 0.12,
                            open_pkc.slot_center[1], 0.0])
        sub_p = build_substrate(pos=dock_pt, w=1.2, h=0.48, phosphorylated=True, label="sub.", label_size=24)
        self.play(
            Transform(pkc, open_pkc),
            GrowArrow(arr_act),
            FadeIn(lab_act),
            FadeIn(sub),
            run_time=1.8,
        )
        self.play(sub.animate.move_to(dock_pt), run_time=1.1)
        self.remove(sub)
        self.add(sub_p)
        self.play(sub_p.animate.move_to([dock_pt[0], -1.45, 0]), run_time=1.1)

        self.at("Keep this rule")
        arr_out = Arrow([-2.75, 0.45, 0], [-0.55, 0.45, 0], buff=0, color=TEAL, stroke_width=8)
        arr_out.layout_ok = True
        lab_out = T("conventional\nPKC output", 28, TEAL, weight=BOLD, line_spacing=0.85).move_to([-1.65, 1.30, 0])
        rule_cap = caption("Conventional PKC integrates calcium targeting with DAG activation at membranes.",
                           size=28, color=TEXT, y=-2.35)
        self.play(
            FadeOut(er), FadeOut(ca_dots), FadeOut(sub_p),
            arr_targ.animate.put_start_and_end_on([-5.5, 0.85, 0], [-2.85, 0.50, 0]),
            arr_act.animate.put_start_and_end_on([-5.5, 0.05, 0], [-2.85, 0.40, 0]),
            GrowArrow(arr_out),
            FadeIn(lab_out),
            run_time=3.2,
        )
        self.play(FadeIn(rule_cap), run_time=2.8)
        self.finish()


# =====================================================================
# SCENE 12: End Card (silent, 3.5 s)
# =====================================================================
class S12End(EndCard):
    LINE = "Conventional PKC integrates calcium targeting with DAG activation at membranes."
