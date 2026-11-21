"""How the Number Was Made — Endocrine Axes and How to Test Them (Chapter 2)

COLOUR MAP (one colour per concept for the whole film):
    PURPLE  (#C084FC)  releasing signal (hypothalamus -> pituitary)
    YELLOW  (#F5D547)  trophic hormone (TSH)
    ORANGE  (#FF862F)  target hormone (T4 / free T4)
    BLUE    (#58C4DD)  long-loop feedback
    TEAL    (#3FB8C0)  blood sample, assay, antibodies, signal meter, measurement
    RED     (#FC6255)  failure / broken rule
    GREEN   (#83C167)  intact / healthy / rule holds
    GREY    (#8B93A1)  outlines, carrier proteins, inactive/dimmed well
    MAGENTA (#E86ED0)  biotin
    TEXT    (#E8EAF0)  white signal tags, primary text

CARRIED WORLD:
    Top strip (y 2.38..3.34): Hypothalamus -> Anterior pituitary -> Thyroid with PURPLE, YELLOW,
    ORANGE arrows and BLUE long-loop feedback bar below them.
    Left stage (x -6.25..1.50, y -2.55..2.10): TEAL-outlined 'the assay' panel (splits into
    two wells, compresses into two platforms, opens into the blood sample pool, and splits back
    into biotin-catch vs no-biotin-step wells).
    Right stage (x 2.45..6.25, y -2.55..2.10): vertical bar gauges (TSH in YELLOW, free T4 in
    ORANGE, plus dashed total T4 in ORANGE when binding globulin rises), driven by ValueTrackers.

WHAT CHANGES PER SPOKEN SCENE (computed from lesson numbers / assay mechanics):
    s00_link_and_question: Top axis glows in sequence; Thyroid marked intact (GREEN); TSH bar
        drops to 0.14 and free T4 bar rises to 0.86; blood sample tube drops into assay panel.
    s02_sandwich: Assay panel splits into two wells; 5 YELLOW TSH molecules drift to floor Y
        antibodies, 5 WHITE-tagged signal Y antibodies land on top, and signal meter climbs
        in proportion to captured sandwich complexes (0 -> 0.90).
    s03_competitive: One small ORANGE free T4 cannot fit two Y antibodies (they collide and
        recoil); 4 limited Y sites fill with 3 WHITE-tagged copies + 1 sample (signal 0.75),
        then excess sample ORANGE dots jostle and displace 2 tagged copies so signal drops to 0.25.
    s04_biotin: Both wells show streptavidin hooks catching complexes (signals 0.25 -> 0.75);
        MAGENTA biotin dots pour from the sample tube onto both floors, blocking hooks so
        complexes detach and both signal meters fall together (0.75 -> 0.20 / 0.25).
    s05_misread: Low sandwich and competitive signals travel along TEAL arrows to push TSH bar
        down (0.50 -> 0.14) and, via a flip icon, push free T4 bar up (0.50 -> 0.86).
    s06_study: Assay panel compresses into two platforms; 10 GREEN adult icons send MAGENTA
        biotin dots to both; platform 1 mini bars split (TSH 0.18, free T4 0.84) while
        platform 2 mini bars stay flat at 0.50; large gauges echo platform 1.
    s07_idea: Platforms merge back to clean wells (biotin clears); TEAL bracket wraps gauges;
        sample tube and receptor cup show and resolve '?'; closing rule appears.
    s08_predict: Assay panel opens into blood pool with 5 GREY carriers (20 bound ORANGE T4)
        and 3 free ORANGE T4 drifting; oral estrogen adds 4 more loaded carriers while free
        count stays 3 and dashed total T4 bar rises (0.50 -> 0.88); '?' placed on free T4 & TSH.
    s10_answer: '?' removed, free T4 & TSH hold at usual (0.50) while pool keeps 3 free dots;
        TEAL link joins TSH to raised total T4 ('rule seems broken' RED), then swings to
        free T4 ('rule holds' GREEN).
    s11_close: Pool splits into 'biotin catch' well (MAGENTA dots block hooks, TSH low / free T4
        high) and 'no biotin step' well (clean catch, both gauges settle at usual 0.50); top
        axis glows in order with Thyroid GREEN tick steady.
"""
import numpy as np
from bp_parts import *

PURPLE = "#C084FC"
MAGENTA = "#E86ED0"

# Fixed layout coordinates kept across the entire film
PANEL_BOX = (-6.25, 1.42, -2.55, 2.10)      # width 7.67, height 4.65
GAUGE_BOX = (2.52, 6.25, -2.55, 2.10)       # width 3.73, height 4.65 (gap 1.10 between panels)
TRACK_Y0, TRACK_Y1 = -1.55, 0.85            # bar height 2.40, leaves y 0.85..2.05 open above


# ------------------------------------------------------------------ shared carried world
def build_top_strip(thyroid_ok=False):
    """Top endocrine axis strip (y ~ 2.40..3.35)."""
    g = VGroup()
    h_box = boxed_label("Hypothalamus", color=GREY, size=24, box=(2.35, 0.54), pad=0.14).move_to([-4.85, 3.04, 0])
    p_box = boxed_label("Anterior pituitary", color=GREY, size=24, box=(2.95, 0.54), pad=0.14).move_to([-1.20, 3.04, 0])
    t_box = boxed_label("Thyroid", color=GREEN if thyroid_ok else GREY, size=24, box=(1.85, 0.54), pad=0.14).move_to([2.15, 3.04, 0])

    a_purple = Arrow(
        h_box.get_right() + RIGHT * 0.06,
        p_box.get_left() + LEFT * 0.06,
        buff=0, color=PURPLE, stroke_width=5, max_tip_length_to_length_ratio=0.22,
    )
    a_yellow = Arrow(
        p_box.get_right() + RIGHT * 0.06,
        t_box.get_left() + LEFT * 0.06,
        buff=0, color=YELLOW, stroke_width=5, max_tip_length_to_length_ratio=0.22,
    )
    a_orange = Arrow(
        t_box.get_right() + RIGHT * 0.06,
        t_box.get_right() + RIGHT * 0.92,
        buff=0, color=ORANGE, stroke_width=5, max_tip_length_to_length_ratio=0.28,
    )

    fb_y = 2.42
    fb_stem = Line([t_box.get_center()[0], t_box.get_bottom()[1] - 0.05, 0], [t_box.get_center()[0], fb_y, 0], color=BLUE, stroke_width=4)
    fb_horiz = Line([t_box.get_center()[0], fb_y, 0], [h_box.get_center()[0], fb_y, 0], color=BLUE, stroke_width=4)
    fb_up_h = Arrow([h_box.get_center()[0], fb_y, 0], [h_box.get_center()[0], h_box.get_bottom()[1] - 0.05, 0],
                    buff=0, color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=0.35)
    fb_up_p = Arrow([p_box.get_center()[0], fb_y, 0], [p_box.get_center()[0], p_box.get_bottom()[1] - 0.05, 0],
                    buff=0, color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=0.35)
    fb_group = VGroup(fb_stem, fb_horiz, fb_up_h, fb_up_p)

    g.add(h_box, p_box, t_box, a_purple, a_yellow, a_orange, fb_group)
    g.hypo, g.pit, g.thy = h_box, p_box, t_box
    g.a_purple, g.a_yellow, g.a_orange, g.fb = a_purple, a_yellow, a_orange, fb_group
    g.tick = None
    if thyroid_ok:
        g.tick = make_green_tick().next_to(t_box, RIGHT, buff=0.08).shift(UP * 0.22)
        g.add(g.tick)
    return g


def make_green_tick():
    pts = [np.array([-0.14, 0.0, 0]), np.array([-0.03, -0.12, 0]), np.array([0.18, 0.14, 0])]
    tick = VMobject(color=GREEN, stroke_width=5)
    tick.set_points_as_corners(pts)
    return tick


def make_bar_gauge(x_center, label_text, color, tracker, width=0.76, dashed_only=False, usual_band=False):
    """Vertical bar gauge tied to a ValueTracker in [0, 1]."""
    h = TRACK_Y1 - TRACK_Y0
    y_mid = (TRACK_Y0 + TRACK_Y1) / 2
    if dashed_only:
        track = DashedVMobject(
            RoundedRectangle(corner_radius=0.10, width=width, height=h, stroke_color=color, stroke_width=3),
            num_dashes=24,
        ).move_to([x_center, y_mid, 0])
    else:
        track = RoundedRectangle(
            corner_radius=0.10, width=width, height=h,
            stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.6,
        ).move_to([x_center, y_mid, 0])

    fill_opacity = 0.28 if dashed_only else 0.78
    stroke_w = 2.5 if dashed_only else 0

    def _mk_fill():
        v = float(np.clip(tracker.get_value(), 0.03, 1.0))
        fh = max(0.08, v * (h - 0.10))
        r = Rectangle(
            width=width - 0.12, height=fh,
            stroke_color=color, stroke_width=stroke_w,
            fill_color=color, fill_opacity=fill_opacity,
        )
        r.move_to([x_center, TRACK_Y0 + 0.05 + fh / 2, 0])
        return r

    fill = always_redraw(_mk_fill)
    lab = T(label_text, size=24, color=color).move_to([x_center, TRACK_Y0 - 0.36, 0])

    g = VGroup(track, fill, lab)
    if usual_band:
        u_y = TRACK_Y0 + 0.50 * (h - 0.10) + 0.05
        band = Rectangle(
            width=width + 0.04, height=0.38,
            stroke_color=GREEN, stroke_width=2, stroke_opacity=0.60,
            fill_color=GREEN, fill_opacity=0.12,
        ).move_to([x_center, u_y, 0])
        g.add(band)
        g.usual_band = band
    g.track, g.fill, g.label = track, fill, lab
    g.top_anchor = np.array([x_center, TRACK_Y1 + 0.12, 0])
    return g


def build_two_gauges(tsh_val=0.50, ft4_val=0.50, usual_band=False):
    """Carried two-bar gauge panel on the right (x 2.52..6.25)."""
    x0, x1, y0, y1 = GAUGE_BOX
    tsh_tr = ValueTracker(tsh_val)
    ft4_tr = ValueTracker(ft4_val)
    frame = RoundedRectangle(
        corner_radius=0.18, width=x1 - x0, height=y1 - y0,
        stroke_color=GREY, stroke_width=2.0, fill_color=BG, fill_opacity=0.5,
    ).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    g_tsh = make_bar_gauge(3.60, "TSH", YELLOW, tsh_tr, width=0.80, usual_band=usual_band)
    g_ft4 = make_bar_gauge(5.18, "free T4", ORANGE, ft4_tr, width=0.80, usual_band=usual_band)
    note = T("not to scale", size=22, color=GREY).move_to([5.32, -2.35, 0])
    g = VGroup(frame, g_tsh, g_ft4, note)
    g.frame, g.tsh, g.ft4, g.note = frame, g_tsh, g_ft4, note
    g.tsh_tr, g.ft4_tr = tsh_tr, ft4_tr
    return g


def build_three_gauges(tot_val=0.50, tsh_val=0.50, ft4_val=0.50, usual_band=True):
    """Three-bar gauge panel used in s08..s10: dashed total T4 + TSH + free T4."""
    x0, x1, y0, y1 = GAUGE_BOX
    tot_tr = ValueTracker(tot_val)
    tsh_tr = ValueTracker(tsh_val)
    ft4_tr = ValueTracker(ft4_val)
    frame = RoundedRectangle(
        corner_radius=0.18, width=x1 - x0, height=y1 - y0,
        stroke_color=GREY, stroke_width=2.0, fill_color=BG, fill_opacity=0.5,
    ).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    g_tot = make_bar_gauge(3.15, "total T4", ORANGE, tot_tr, width=0.48, dashed_only=True, usual_band=False)
    g_tsh = make_bar_gauge(4.22, "TSH", YELLOW, tsh_tr, width=0.48, usual_band=usual_band)
    g_ft4 = make_bar_gauge(5.60, "free T4", ORANGE, ft4_tr, width=0.48, usual_band=usual_band)
    note = T("not to scale", size=22, color=GREY).move_to([5.32, -2.35, 0])
    g = VGroup(frame, g_tot, g_tsh, g_ft4, note)
    g.frame, g.tot, g.tsh, g.ft4, g.note = frame, g_tot, g_tsh, g_ft4, note
    g.tot_tr, g.tsh_tr, g.ft4_tr = tot_tr, tsh_tr, ft4_tr
    return g


def build_assay_panel(title="the assay"):
    x0, x1, y0, y1 = PANEL_BOX
    box = RoundedRectangle(
        corner_radius=0.18, width=x1 - x0, height=y1 - y0,
        stroke_color=TEAL, stroke_width=3.0, fill_color=TEAL, fill_opacity=0.06,
    ).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    head = T(title, size=28, color=TEAL).move_to([x0 + 0.30, y1 - 0.32, 0], aligned_edge=LEFT)
    g = VGroup(box, head)
    g.box, g.head = box, head
    return g


def make_sample_tube(label="one blood sample", scale=1.0):
    w, h = 0.56 * scale, 1.55 * scale
    body = RoundedRectangle(
        corner_radius=w / 2, width=w, height=h,
        stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.22,
    )
    rim = Line(body.get_corner(UL) + LEFT * 0.08 * scale, body.get_corner(UR) + RIGHT * 0.08 * scale, color=TEAL, stroke_width=5)
    liq = Rectangle(
        width=w - 0.10 * scale, height=h * 0.52,
        stroke_width=0, fill_color=TEAL, fill_opacity=0.55,
    ).move_to(body.get_bottom() + UP * (h * 0.28))
    tube = VGroup(liq, body, rim)
    if label:
        lab = T(label, size=26, color=TEAL).next_to(tube, DOWN, buff=0.18)
        g = VGroup(tube, lab)
        g.tube, g.label = tube, lab
        return g
    g = VGroup(tube)
    g.tube = tube
    return g


def make_antibody_y(color=TEAL, scale=1.0, flip_down=False, tag=False, hook=False):
    s = scale
    stem = Line([0, -0.30 * s, 0], [0, 0.02 * s, 0], color=color, stroke_width=4.5)
    arm_l = Line([0, 0.02 * s, 0], [-0.21 * s, 0.26 * s, 0], color=color, stroke_width=4.5)
    arm_r = Line([0, 0.02 * s, 0], [0.21 * s, 0.26 * s, 0], color=color, stroke_width=4.5)
    parts = [stem, arm_l, arm_r]
    if hook:
        hk = Arc(radius=0.07 * s, start_angle=PI, angle=PI, arc_center=[0, -0.35 * s, 0], color=MAGENTA, stroke_width=4)
        parts.append(hk)
    g = VGroup(*parts)
    if flip_down:
        g.rotate(PI, about_point=ORIGIN)
    if tag:
        tail_pt = np.array([0, 0.36 * s, 0]) if flip_down else np.array([0, -0.36 * s, 0])
        halo = Circle(radius=0.13 * s, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.25).move_to(tail_pt)
        core = Dot(point=tail_pt, radius=0.075 * s, color=WHITE)
        g.add(halo, core)
        g.tag = VGroup(halo, core)
    return g


def make_tagged_t4(scale=1.0):
    d = Dot(radius=0.095 * scale, color=ORANGE)
    halo = Circle(radius=0.14 * scale, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.22).next_to(d, UR, buff=-0.04 * scale)
    core = Dot(radius=0.055 * scale, color=WHITE).move_to(halo)
    return VGroup(d, halo, core)


def build_two_wells(left_dim=False, right_dim=False, floor_label="capture surface", catch_hooks=False, gap=0.30):
    """Two side-by-side wells inside PANEL_BOX (-6.25..1.42) with zero border collisions."""
    w_top, w_bot = 1.38, -2.10
    w_h = w_top - w_bot
    # Total width inside (-6.05..1.22) is 7.27
    w_w = (7.27 - gap) / 2
    lx = -6.05 + w_w / 2
    rx = 1.22 - w_w / 2

    def _one_well(cx, title, title_col, dim):
        op = 0.38 if dim else 1.0
        fill_op = 0.04 if dim else 0.11
        box = RoundedRectangle(
            corner_radius=0.14, width=w_w, height=w_h,
            stroke_color=TEAL, stroke_width=2.5, stroke_opacity=op,
            fill_color=TEAL, fill_opacity=fill_op,
        ).move_to([cx, (w_top + w_bot) / 2, 0])
        head = T(title, size=22 if w_w < 3.3 else 24, color=title_col if not dim else GREY).move_to([cx, w_top - 0.26, 0])

        mx = cx + w_w / 2 - 0.44
        my0, my1 = -1.40, 0.44
        m_tr = ValueTracker(0.0)
        m_track = RoundedRectangle(
            corner_radius=0.06, width=0.26, height=my1 - my0,
            stroke_color=TEAL, stroke_width=2, stroke_opacity=op,
            fill_color=BG, fill_opacity=0.65,
        ).move_to([mx, (my0 + my1) / 2, 0])

        def _mk_mfill():
            v = float(np.clip(m_tr.get_value(), 0.02, 1.0))
            fh = max(0.05, v * (my1 - my0 - 0.08))
            return Rectangle(
                width=0.18, height=fh, stroke_width=0,
                fill_color=TEAL, fill_opacity=0.85 if not dim else 0.30,
            ).move_to([mx, my0 + 0.04 + fh / 2, 0])

        m_fill = always_redraw(_mk_mfill)
        m_lab = T("signal", size=22, color=TEAL if not dim else GREY).move_to([mx - 0.04, my1 + 0.24, 0])
        wg = VGroup(box, head, m_track, m_fill, m_lab)
        wg.box, wg.head, wg.m_track, wg.m_fill, wg.m_lab, wg.m_tr = box, head, m_track, m_fill, m_lab, m_tr
        wg.cx = cx
        wg.meter_x = mx
        wg.meter_top = my1
        wg.meter_bot = my0
        return wg

    left_w = _one_well(lx, "sandwich: TSH", YELLOW, left_dim)
    right_w = _one_well(rx, "competitive: free T4", ORANGE, right_dim)

    floor_y = -1.58
    floor_l = Line([lx - w_w / 2 + 0.20, floor_y, 0], [lx + w_w / 2 - 0.68, floor_y, 0], color=TEAL, stroke_width=4)
    floor_r = Line([rx - w_w / 2 + 0.20, floor_y, 0], [rx + w_w / 2 - 0.68, floor_y, 0], color=TEAL, stroke_width=4)
    floor_line = VGroup(floor_l, floor_r)
    # Placed cleanly BELOW both well boxes (-2.10) and ABOVE outer panel bottom (-2.55)
    flab = T(floor_label, size=22, color=TEAL).move_to([(lx + rx) / 2, -2.33, 0])

    hooks = VGroup()
    if catch_hooks:
        l_xs = [lx - 1.25 + k * 0.62 for k in range(4)]
        r_xs = [rx - 1.25 + k * 0.62 for k in range(4)]
        for sx in l_xs + r_xs:
            cup = Arc(radius=0.085, start_angle=PI, angle=PI, arc_center=[sx, floor_y + 0.04, 0], color=TEAL, stroke_width=4)
            hooks.add(cup)

    g = VGroup(left_w, right_w, floor_line, flab, hooks)
    g.left_w, g.right_w, g.floor_line, g.flab, g.hooks = left_w, right_w, floor_line, flab, hooks
    g.floor_y = floor_y
    g.lx, g.rx, g.w_w = lx, rx, w_w
    return g


def glow_axis_sequence(scene, strip, step_time=0.95):
    """Smooth clean sequential highlight along the top thyroid axis preserving concept colours."""
    for mob, col, base_w in (
        (strip.a_purple, PURPLE, 5),
        (strip.a_yellow, YELLOW, 5),
        (strip.a_orange, ORANGE, 5),
        (strip.fb, BLUE, 4),
    ):
        scene.play(mob.animate.set_stroke(width=10), run_time=step_time * 0.45)
        scene.play(mob.animate.set_stroke(width=base_w), run_time=step_time * 0.55)


# ------------------------------------------------------------------ S00
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=False)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.50, ft4_val=0.50)
        self.add(strip, panel, gauges)

        self.at("Read a trophic")
        glow_axis_sequence(self, strip, step_time=1.2)
        pair_box = SurroundingRectangle(VGroup(gauges.tsh, gauges.ft4), color=TEAL, buff=0.14, corner_radius=0.14, stroke_width=2.5)
        self.play(Create(pair_box), run_time=0.8)
        self.play(FadeOut(pair_box), run_time=0.8)

        self.at("healthy adult")
        tick = make_green_tick().next_to(strip.thy, RIGHT, buff=0.08).shift(UP * 0.22)
        self.play(
            strip.thy.box.animate.set_stroke(GREEN, 3).set_fill(GREEN, 0.16),
            strip.thy.label.animate.set_color(GREEN),
            FadeIn(tick, scale=1.2),
            run_time=0.85,
        )
        pulse(tick, base=5.0, amp=2.2, speed=4.0)

        self.at("TSH reads low")
        self.play(gauges.tsh_tr.animate.set_value(0.14), run_time=1.3)

        self.at("free T4 reads high")
        self.play(gauges.ft4_tr.animate.set_value(0.86), run_time=3.1)

        self.at("overactive thyroid")
        over_tag = boxed_label("looks overactive", color=ORANGE, size=24, pad=0.12).move_to([4.35, 1.56, 0])
        self.play(FadeIn(over_tag, shift=DOWN * 0.1), run_time=1.4)
        self.play(Indicate(over_tag, color=ORANGE, scale_factor=1.06), run_time=1.0)

        self.at("where did it")
        tube = make_sample_tube("one blood sample", scale=0.95).move_to([-2.38, 1.25, 0])
        q_txt = T("Where did this come from?", size=34, color=TEXT).move_to([-2.38, -1.25, 0])
        self.play(tube.animate.move_to([-2.38, 0.35, 0]), FadeIn(q_txt, shift=UP * 0.15), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------ S01
class S01Title(NarratedScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.14, ft4_val=0.86)
        over_tag = boxed_label("looks overactive", color=ORANGE, size=24, pad=0.12).move_to([4.35, 1.56, 0])
        tube = make_sample_tube("one blood sample", scale=0.95).move_to([-2.38, 0.35, 0])
        q_txt = T("Where did this come from?", size=34, color=TEXT).move_to([-2.38, -1.25, 0])

        self.add(strip, panel, gauges, over_tag, tube, q_txt)
        pulse(gauges.tsh.track, base=2.5, amp=1.2, speed=5.0)
        pulse(gauges.ft4.track, base=2.5, amp=1.2, speed=5.0)

        # Tilt tube to left side of assay panel and pour onto left floor, leaving center-right clear for title
        title = T("How the Number Was Made", size=36, font=TITLE_FONT, color=TEXT)
        fit(title, max_w=5.8)
        title.move_to([-1.65, -0.30, 0])
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.18)

        pour_end = np.array([-5.25, -1.66, 0])
        floor_ln = Line([-5.85, -1.66, 0], [1.10, -1.66, 0], color=TEAL, stroke_width=4)

        self.play(FadeOut(q_txt), FadeOut(tube.label), run_time=0.35)
        self.play(
            tube.tube.animate.move_to([-5.25, 0.60, 0]).rotate(-2.1),
            FadeIn(title, shift=UP * 0.1),
            GrowFromCenter(rule),
            run_time=0.7,
        )
        pour = ArcBetweenPoints(tube.tube[2].get_center(), pour_end, angle=0.10, color=TEAL, stroke_width=4)
        self.play(Create(pour), Create(floor_ln), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ S02
class S02Sandwich(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.14, ft4_val=0.86)
        over_tag = boxed_label("looks overactive", color=ORANGE, size=24, pad=0.12).move_to([4.35, 1.56, 0])
        self.add(strip, panel, gauges, over_tag)

        wells = build_two_wells(left_dim=False, right_dim=True, floor_label="capture")
        lw = wells.left_w
        floor_xs = [wells.lx - 1.38 + k * 0.48 for k in range(5)]
        cap_ys = VGroup(*[make_antibody_y(TEAL, scale=0.78).move_to([x, wells.floor_y + 0.25, 0]) for x in floor_xs])

        self.at("The answer lies")
        self.play(FadeIn(wells), run_time=1.0)
        self.play(FadeIn(cap_ys, shift=UP * 0.15, lag_ratio=0.15), run_time=2.2)

        tsh_dots = VGroup(*[Dot(radius=0.14, color=YELLOW).move_to([x, 0.55 + (i % 2) * 0.12, 0]) for i, x in enumerate(floor_xs)])
        sig_ys = VGroup(*[make_antibody_y(TEAL, scale=0.78, flip_down=True, tag=True).move_to([x, 0.58, 0]) for x in floor_xs])

        self.at("For TSH")
        self.play(FadeIn(tsh_dots[:3], shift=DOWN * 0.12), run_time=0.9)
        self.play(
            *[tsh_dots[i].animate.move_to([floor_xs[i], wells.floor_y + 0.54, 0]) for i in range(3)],
            run_time=3.5,
        )

        self.at("One holds it")
        self.play(*[Indicate(cap_ys[i], color=TEAL, scale_factor=1.12) for i in range(3)], run_time=0.9)

        self.at("the other carries")
        self.play(FadeIn(sig_ys[:3], shift=DOWN * 0.12), run_time=0.5)
        self.play(
            *[sig_ys[i].animate.move_to([floor_xs[i], wells.floor_y + 0.94, 0]) for i in range(3)],
            lw.m_tr.animate.set_value(0.54),
            run_time=1.6,
        )

        self.at("More hormone")
        self.play(FadeIn(tsh_dots[3:], shift=DOWN * 0.12), FadeIn(sig_ys[3:], shift=DOWN * 0.12), run_time=0.5)
        self.play(
            *[tsh_dots[i].animate.move_to([floor_xs[i], wells.floor_y + 0.54, 0]) for i in (3, 4)],
            *[sig_ys[i].animate.move_to([floor_xs[i], wells.floor_y + 0.94, 0]) for i in (3, 4)],
            lw.m_tr.animate.set_value(0.90),
            run_time=1.5,
        )
        self.finish()


# ------------------------------------------------------------------ S03
class S03Competitive(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.14, ft4_val=0.86)
        over_tag = boxed_label("looks overactive", color=ORANGE, size=24, pad=0.12).move_to([4.35, 1.56, 0])
        wells = build_two_wells(left_dim=True, right_dim=False, floor_label="capture")
        wells.left_w.m_tr.set_value(0.90)

        floor_xs_l = [wells.lx - 1.38 + k * 0.48 for k in range(5)]
        left_complexes = VGroup()
        for x in floor_xs_l:
            left_complexes.add(
                make_antibody_y(TEAL, scale=0.78).move_to([x, wells.floor_y + 0.25, 0]).set_opacity(0.38),
                Dot(radius=0.14, color=YELLOW).move_to([x, wells.floor_y + 0.54, 0]).set_opacity(0.38),
                make_antibody_y(TEAL, scale=0.78, flip_down=True, tag=True).move_to([x, wells.floor_y + 0.94, 0]).set_opacity(0.38),
            )
        self.add(strip, panel, gauges, over_tag, wells, left_complexes)

        rw = wells.right_w
        cx_r = wells.rx - 0.38
        small_t4 = Dot(radius=0.10, color=ORANGE).move_to([cx_r, -0.35, 0])
        ab_l = make_antibody_y(TEAL, scale=0.88).rotate(-PI / 2).move_to([cx_r - 0.85, -0.35, 0])
        ab_r = make_antibody_y(TEAL, scale=0.88).rotate(PI / 2).move_to([cx_r + 0.85, -0.35, 0])

        self.at("Free T4 is too small")
        self.play(FadeIn(small_t4), FadeIn(ab_l), FadeIn(ab_r), run_time=0.5)
        self.play(ab_l.animate.shift(RIGHT * 0.52), ab_r.animate.shift(LEFT * 0.52), run_time=1.0)
        self.play(ab_l.animate.shift(LEFT * 0.40), ab_r.animate.shift(RIGHT * 0.40), run_time=0.8)
        self.play(ab_l.animate.shift(RIGHT * 0.40), ab_r.animate.shift(LEFT * 0.40), run_time=0.8)
        self.play(ab_l.animate.shift(LEFT * 0.52), ab_r.animate.shift(RIGHT * 0.52), run_time=0.9)

        self.at("usually measured")
        floor_xs_r = [wells.rx - 1.35 + k * 0.54 for k in range(4)]
        lim_ys = VGroup(*[make_antibody_y(TEAL, scale=0.78).move_to([x, wells.floor_y + 0.25, 0]) for x in floor_xs_r])
        lim_lab = T("limited antibody", size=22, color=TEAL).move_to([wells.rx - 0.15, -1.84, 0])
        self.play(FadeOut(small_t4), FadeOut(ab_l), FadeOut(ab_r), run_time=0.45)
        self.play(FadeIn(lim_ys, shift=UP * 0.15, lag_ratio=0.18), FadeIn(lim_lab), run_time=2.5)

        self.at("Sample hormone")
        rng = np.random.default_rng(7)
        bound_tagged = [make_tagged_t4().move_to([floor_xs_r[i], -0.05 + rng.uniform(-0.04, 0.04), 0]) for i in range(3)]
        bound_plain = Dot(radius=0.10, color=ORANGE).move_to([floor_xs_r[3], -0.04, 0])
        # Stacked legend at top-left of competitive well, completely clear of heading (1.12), 'signal' (0.68), and dots (y <= 0.05)
        lab_copy = T("labelled copy", size=22, color=TEXT).move_to([wells.rx - 1.54, 0.70, 0], aligned_edge=LEFT)
        lab_sample = T("sample", size=22, color=ORANGE).move_to([wells.rx - 1.54, 0.41, 0], aligned_edge=LEFT)

        self.play(
            *[FadeIn(m, shift=DOWN * 0.10) for m in (*bound_tagged, bound_plain)],
            FadeIn(lab_copy), FadeIn(lab_sample),
            run_time=0.6,
        )
        # Jostle across fluid then settle onto the 4 limited sites
        self.play(
            bound_tagged[0].animate.move_to([floor_xs_r[1], -0.45, 0]),
            bound_tagged[1].animate.move_to([floor_xs_r[0], -0.35, 0]),
            bound_tagged[2].animate.move_to([floor_xs_r[3], -0.42, 0]),
            bound_plain.animate.move_to([floor_xs_r[2], -0.38, 0]),
            run_time=1.8,
        )
        self.play(
            *[bound_tagged[i].animate.move_to([floor_xs_r[i], wells.floor_y + 0.50, 0]) for i in range(3)],
            bound_plain.animate.move_to([floor_xs_r[3], wells.floor_y + 0.50, 0]),
            rw.m_tr.animate.set_value(0.75),
            run_time=2.3,
        )

        self.at("More sample hormone")
        extra_plain = VGroup(*[
            Dot(radius=0.10, color=ORANGE).move_to([floor_xs_r[i] + rng.uniform(-0.08, 0.08), -0.04 + (i % 2) * 0.05, 0])
            for i in range(4)
        ])
        self.play(FadeIn(extra_plain, shift=DOWN * 0.10), run_time=0.5)
        self.play(
            extra_plain[1].animate.move_to([floor_xs_r[1], wells.floor_y + 0.50, 0]),
            extra_plain[2].animate.move_to([floor_xs_r[2], wells.floor_y + 0.50, 0]),
            bound_tagged[1].animate.move_to([floor_xs_r[1], -0.42, 0]).set_opacity(0.45),
            bound_tagged[2].animate.move_to([floor_xs_r[2], -0.36, 0]).set_opacity(0.45),
            extra_plain[0].animate.move_to([floor_xs_r[0] - 0.10, -0.58, 0]),
            extra_plain[3].animate.move_to([floor_xs_r[3] + 0.06, -0.50, 0]),
            run_time=2.0,
        )

        self.at("signal falls")
        rule_tag = T("signal down = hormone up", size=22, color=ORANGE).move_to([wells.rx, -2.92, 0])
        self.play(FadeIn(rule_tag, shift=UP * 0.1), run_time=0.6)
        self.play(
            rw.m_tr.animate.set_value(0.25),
            bound_tagged[1].animate.move_to([floor_xs_r[1], -0.08, 0]).set_opacity(0.20),
            bound_tagged[2].animate.move_to([floor_xs_r[2], -0.05, 0]).set_opacity(0.20),
            extra_plain[0].animate.shift(RIGHT * 0.28 + UP * 0.12),
            extra_plain[3].animate.shift(LEFT * 0.28 + DOWN * 0.12),
            run_time=2.4,
        )
        self.finish()


# ------------------------------------------------------------------ S04
class S04Biotin(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.50, ft4_val=0.50)
        wells = build_two_wells(left_dim=False, right_dim=False, floor_label="streptavidin catch", catch_hooks=True)
        wells.left_w.m_tr.set_value(0.25)
        wells.right_w.m_tr.set_value(0.25)
        stag = T("schematic", size=22, color=GREY).move_to([0.46, -2.33, 0])

        lxs = [wells.lx - 1.25 + k * 0.62 for k in range(4)]
        rxs = [wells.rx - 1.25 + k * 0.62 for k in range(4)]
        l_complexes = VGroup(*[
            VGroup(
                make_antibody_y(TEAL, scale=0.72, hook=True).move_to([x, wells.floor_y + 0.28, 0]),
                Dot(radius=0.13, color=YELLOW).move_to([x, wells.floor_y + 0.54, 0]),
                make_antibody_y(TEAL, scale=0.72, flip_down=True, tag=True).move_to([x, wells.floor_y + 0.92, 0]),
            )
            for x in lxs
        ])
        r_complexes = VGroup(*[
            VGroup(
                make_antibody_y(TEAL, scale=0.72, hook=True).move_to([x, wells.floor_y + 0.28, 0]),
                (make_tagged_t4(0.90) if i < 3 else Dot(radius=0.09, color=ORANGE)).move_to([x, wells.floor_y + 0.50, 0]),
            )
            for i, x in enumerate(rxs)
        ])
        # Start complexes slightly above the catch hooks so catching happens during "Some assays catch"
        l_complexes.shift(UP * 0.40)
        r_complexes.shift(UP * 0.40)
        self.add(strip, panel, gauges, wells, l_complexes, r_complexes, stag)

        self.at("Some assays catch")
        self.play(
            l_complexes.animate.shift(DOWN * 0.40),
            r_complexes.animate.shift(DOWN * 0.40),
            wells.left_w.m_tr.animate.set_value(0.75),
            wells.right_w.m_tr.animate.set_value(0.75),
            run_time=3.0,
        )
        self.play(*[Indicate(h, color=MAGENTA, scale_factor=1.3) for h in wells.hooks], run_time=1.5)

        self.at("biotin supplement")
        rng = np.random.default_rng(11)
        tube = make_sample_tube("", scale=0.42).rotate(-0.45).move_to([-2.40, 1.72, 0])
        biotin_lab = T("biotin", size=24, color=MAGENTA).move_to([-1.45, 1.76, 0])
        biotin_dots = VGroup(*[
            Dot(radius=0.075, color=MAGENTA).move_to([-2.40 + rng.uniform(-0.08, 0.08), 1.25 + rng.uniform(-0.06, 0.06), 0])
            for _ in range(14)
        ])
        self.play(FadeIn(tube), FadeIn(biotin_lab), FadeIn(biotin_dots), run_time=0.6)
        targets = lxs + rxs + [wells.lx - 0.94, wells.lx + 0.30, wells.rx - 0.94, wells.rx + 0.30, wells.lx - 0.32, wells.rx - 0.32]
        # Drop down central gap below 'signal' (y=0.68) first, then fan onto both catch floors
        self.play(
            *[biotin_dots[i].animate.move_to([-2.40 + (-0.25 if i % 2 == 0 else 0.25), 0.25 + (i % 3) * 0.06, 0]) for i in range(14)],
            run_time=1.0,
        )
        self.play(
            *[biotin_dots[i].animate.move_to([targets[i], wells.floor_y + 0.07 + (i // 8) * 0.11, 0]) for i in range(14)],
            run_time=1.4,
        )

        self.at("Less complex is captured")
        self.play(
            *[l_complexes[i].animate.shift(UP * 1.15).set_opacity(0.22) for i in (0, 2, 3)],
            *[r_complexes[i].animate.shift(UP * 1.15).set_opacity(0.22) for i in (0, 2)],
            run_time=1.8,
        )

        self.at("signal falls in both")
        self.play(
            wells.left_w.m_tr.animate.set_value(0.20),
            wells.right_w.m_tr.animate.set_value(0.25),
            run_time=2.0,
        )
        self.finish()


# ------------------------------------------------------------------ S05
class S05Misread(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.50, ft4_val=0.50)
        wells = build_two_wells(left_dim=False, right_dim=False, floor_label="streptavidin catch", catch_hooks=True)
        wells.left_w.m_tr.set_value(0.20)
        wells.right_w.m_tr.set_value(0.25)

        lxs = [wells.lx - 1.25 + k * 0.62 for k in range(4)]
        rxs = [wells.rx - 1.25 + k * 0.62 for k in range(4)]
        kept_l = VGroup(
            make_antibody_y(TEAL, scale=0.72, hook=True).move_to([lxs[1], wells.floor_y + 0.28, 0]),
            Dot(radius=0.13, color=YELLOW).move_to([lxs[1], wells.floor_y + 0.54, 0]),
            make_antibody_y(TEAL, scale=0.72, flip_down=True, tag=True).move_to([lxs[1], wells.floor_y + 0.92, 0]),
        )
        kept_r = VGroup(
            make_antibody_y(TEAL, scale=0.72, hook=True).move_to([rxs[1], wells.floor_y + 0.28, 0]),
            make_tagged_t4(0.90).move_to([rxs[1], wells.floor_y + 0.50, 0]),
            make_antibody_y(TEAL, scale=0.72, hook=True).move_to([rxs[3], wells.floor_y + 0.28, 0]),
            Dot(radius=0.09, color=ORANGE).move_to([rxs[3], wells.floor_y + 0.50, 0]),
        )
        biotin_floor = VGroup(*[
            Dot(radius=0.075, color=MAGENTA).move_to([x, wells.floor_y + 0.07, 0])
            for x in (lxs[0], lxs[2], lxs[3], rxs[0], rxs[2], wells.lx - 0.94, wells.lx + 0.30, wells.rx - 0.94, wells.rx + 0.30)
        ])
        self.add(strip, panel, gauges, wells, kept_l, kept_r, biotin_floor)

        self.at("turns signal into")
        arr_tsh = CurvedArrow(
            [wells.left_w.meter_x + 0.18, 0.15, 0],
            [gauges.tsh.track.get_left()[0] - 0.08, 0.25, 0],
            angle=-0.28, color=TEAL, stroke_width=4,
        )
        flip_box = boxed_label("↓→↑", color=TEAL, size=24, box=(0.86, 0.50), pad=0.10).move_to([1.97, -0.75, 0])
        arr_ft4_a = Line([wells.right_w.meter_x + 0.18, -0.75, 0], [flip_box.get_left()[0] - 0.06, -0.75, 0], color=TEAL, stroke_width=4)
        arr_ft4_b_pts = [
            np.array([flip_box.get_right()[0] + 0.06, -0.75, 0]),
            np.array([2.84, -0.75, 0]),
            np.array([2.84, -2.18, 0]),
            np.array([4.38, -2.18, 0]),
            np.array([4.38, -0.75, 0]),
            np.array([gauges.ft4.track.get_left()[0] - 0.08, -0.75, 0]),
        ]
        arr_ft4_b_path = VMobject(color=TEAL, stroke_width=4)
        arr_ft4_b_path.set_points_as_corners(arr_ft4_b_pts[:-1])
        arr_ft4_b_head = Arrow(
            arr_ft4_b_pts[-2], arr_ft4_b_pts[-1],
            buff=0, color=TEAL, stroke_width=4, max_tip_length_to_length_ratio=0.45,
        )
        arr_ft4_b_trace = VMobject().set_points_as_corners(arr_ft4_b_pts)
        self.play(Create(arr_tsh), Create(arr_ft4_a), FadeIn(flip_box), Create(arr_ft4_b_path), Create(arr_ft4_b_head), run_time=2.2)

        self.at("In the sandwich assay")
        sig_dot_1 = Dot(radius=0.10, color=TEAL).move_to(arr_tsh.get_start())
        tsh_tag = T("reads low", size=24, color=YELLOW).move_to([3.50, 1.12, 0])
        self.play(MoveAlongPath(sig_dot_1, arr_tsh), run_time=1.8)
        self.play(FadeOut(sig_dot_1), gauges.tsh_tr.animate.set_value(0.14), run_time=1.4)
        self.play(FadeIn(tsh_tag), run_time=0.45)

        self.at("In the competitive assay")
        sig_dot_2 = Dot(radius=0.10, color=TEAL).move_to(arr_ft4_a.get_start())
        ft4_tag = T("reads high", size=24, color=ORANGE).move_to([5.28, 1.12, 0])
        self.play(sig_dot_2.animate.move_to(arr_ft4_a.get_end()), run_time=1.2)
        self.play(FadeOut(sig_dot_2), Indicate(flip_box, color=TEAL, scale_factor=1.15), run_time=0.6)
        sig_dot_2b = Dot(radius=0.10, color=TEAL).move_to(arr_ft4_b_pts[0])
        self.play(MoveAlongPath(sig_dot_2b, arr_ft4_b_trace), run_time=1.2)
        self.play(FadeOut(sig_dot_2b), gauges.ft4_tr.animate.set_value(0.86), run_time=1.4)
        self.play(FadeIn(ft4_tag), run_time=0.45)

        self.at("Together they draw")
        over_tag = boxed_label("looks overactive", color=ORANGE, size=24, pad=0.10).move_to([4.38, 1.64, 0])
        self.play(FadeOut(tsh_tag), FadeOut(ft4_tag), run_time=0.4)
        self.play(FadeIn(over_tag, shift=DOWN * 0.08), run_time=1.4)

        self.at("not there")
        pulse(strip.thy.box, base=4.0, amp=2.2, speed=6.0)
        assay_frame = SurroundingRectangle(over_tag, color=TEAL, buff=0.08, corner_radius=0.10, stroke_width=3)
        from_assay = T("from the assay", size=22, color=TEAL).move_to([4.38, 1.10, 0])
        self.play(Create(assay_frame), FadeIn(from_assay), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ S06
class S06Study(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.50, ft4_val=0.50)
        self.add(strip, panel, gauges)

        study_tag = T("2020: 10 healthy adults", size=24, color=TEXT).move_to([-2.30, 1.76, 0])
        people = VGroup()
        for i in range(10):
            px = -5.55 + i * 0.70
            head = Circle(radius=0.11, color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.12).move_to([px, 1.15, 0])
            body = Arc(radius=0.17, start_angle=0, angle=PI, arc_center=[px, 0.78, 0], color=GREEN, stroke_width=2.5)
            people.add(VGroup(head, body))

        def _machine(cx, label_str):
            box = RoundedRectangle(corner_radius=0.16, width=3.40, height=2.28, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.10).move_to([cx, -0.78, 0])
            lab = T(label_str, size=26, color=TEAL).move_to([cx, 0.08, 0])
            t_tr, f_tr = ValueTracker(0.50), ValueTracker(0.50)
            b_tsh = always_redraw(lambda: Rectangle(
                width=0.44, height=max(0.08, t_tr.get_value() * 1.00),
                stroke_width=0, fill_color=YELLOW, fill_opacity=0.85,
            ).move_to([cx - 0.65, -1.46 + max(0.08, t_tr.get_value() * 1.00) / 2, 0]))
            b_ft4 = always_redraw(lambda: Rectangle(
                width=0.44, height=max(0.08, f_tr.get_value() * 1.00),
                stroke_width=0, fill_color=ORANGE, fill_opacity=0.85,
            ).move_to([cx + 0.65, -1.46 + max(0.08, f_tr.get_value() * 1.00) / 2, 0]))
            lt = T("TSH", size=22, color=YELLOW).move_to([cx - 0.65, -1.70, 0])
            lf = T("free T4", size=22, color=ORANGE).move_to([cx + 0.65, -1.70, 0])
            m = VGroup(box, lab, b_tsh, b_ft4, lt, lf)
            m.box, m.t_tr, m.f_tr, m.lt, m.lf = box, t_tr, f_tr, lt, lf
            return m

        p1 = _machine(-4.22, "platform 1")
        p2 = _machine(-0.52, "platform 2")

        self.at("In a 2020 study")
        self.play(FadeIn(study_tag), FadeIn(people, lag_ratio=0.10), FadeIn(p1), FadeIn(p2), run_time=2.0)
        for _ in range(2):
            biotin_pellets = VGroup(*[
                Dot(radius=0.08, color=MAGENTA).move_to(people[i].get_bottom() + DOWN * 0.08)
                for i in range(10)
            ])
            self.play(FadeIn(biotin_pellets), run_time=0.35)
            self.play(
                *[biotin_pellets[i].animate.move_to([p1.box.get_center()[0], -0.25, 0] if i < 5 else [p2.box.get_center()[0], -0.25, 0]) for i in range(10)],
                run_time=1.3,
            )
            self.play(FadeOut(biotin_pellets), run_time=0.25)

        self.at("Two hours after")
        self.at("one platform read")
        dn_arr = Arrow([-5.25, -0.50, 0], [-5.25, -1.35, 0], buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.28)
        up_arr = Arrow([-3.18, -1.35, 0], [-3.18, -0.50, 0], buff=0, color=ORANGE, stroke_width=4, max_tip_length_to_length_ratio=0.28)
        self.play(FadeIn(dn_arr), FadeIn(up_arr), run_time=0.45)
        self.play(
            p1.t_tr.animate.set_value(0.18),
            p1.f_tr.animate.set_value(0.84),
            gauges.tsh_tr.animate.set_value(0.18),
            gauges.ft4_tr.animate.set_value(0.84),
            run_time=3.2,
        )

        self.at("Another")
        no_chg = T("no significant change", size=22, color=GREEN).move_to([-0.52, -2.22, 0])
        self.play(
            FadeIn(no_chg, shift=UP * 0.08),
            gauges.animate.set_opacity(0.68),
            run_time=2.4,
        )
        self.finish()


# ------------------------------------------------------------------ S07
class S07Idea(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.18, ft4_val=0.84)
        gauges.set_opacity(0.68)

        # Start from two platform boxes (carried from S06) and merge/open into clean two wells
        p1_box = RoundedRectangle(corner_radius=0.16, width=3.40, height=2.28, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.10).move_to([-4.22, -0.78, 0])
        p2_box = RoundedRectangle(corner_radius=0.16, width=3.40, height=2.28, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.10).move_to([-0.52, -0.78, 0])

        wells = build_two_wells(left_dim=False, right_dim=False, floor_label="capture surface", gap=0.95)
        l_xs = [wells.lx - 0.90 + k * 0.56 for k in range(3)]
        r_xs = [wells.rx - 0.90 + k * 0.56 for k in range(3)]
        l_idle = VGroup(*[make_antibody_y(TEAL, scale=0.72).move_to([x, wells.floor_y + 0.25, 0]) for x in l_xs])
        r_idle = VGroup(*[make_antibody_y(TEAL, scale=0.72).move_to([x, wells.floor_y + 0.25, 0]) for x in r_xs])
        old_biotin = VGroup(*[Dot(radius=0.075, color=MAGENTA).move_to([x, wells.floor_y + 0.07, 0]) for x in (l_xs[0], l_xs[2], r_xs[0], r_xs[2])])
        self.add(strip, panel, gauges, p1_box, p2_box)

        self.at("Here is the one idea")
        self.play(
            FadeOut(p1_box), FadeOut(p2_box),
            FadeIn(wells), FadeIn(l_idle), FadeIn(r_idle), FadeIn(old_biotin),
            gauges.animate.set_opacity(1.0),
            run_time=1.8,
        )
        self.play(old_biotin.animate.shift(UP * 1.4).set_opacity(0.0), run_time=1.8)
        self.remove(old_biotin)

        self.at("what the assay detected")
        br = BraceBetweenPoints([3.10, 0.98, 0], [5.60, 0.98, 0], direction=UP, color=TEAL)
        br_lab = T("what the assay detected", size=22, color=TEAL).move_to([4.385, 1.66, 0])
        self.play(
            FadeIn(br), FadeIn(br_lab),
            Indicate(gauges.tsh.track, color=TEAL, scale_factor=1.05),
            Indicate(gauges.ft4.track, color=TEAL, scale_factor=1.05),
            run_time=2.5,
        )

        self.at("what the blood holds")
        tube = make_sample_tube("", scale=0.62).move_to([-2.38, -0.05, 0])
        q1 = T("?", size=34, color=GOLD).next_to(tube, UP, buff=0.14)
        blood_lab = T("what blood holds", size=24, color=TEAL).move_to([-2.38, 1.76, 0])
        self.play(FadeIn(tube), FadeIn(q1), FadeIn(blood_lab), run_time=1.2)

        self.at("what a receptor sees")
        rec_cup = Arc(radius=0.18, start_angle=PI, angle=PI, arc_center=[4.25, 3.04, 0], color=GREEN, stroke_width=5)
        q2 = T("?", size=30, color=GOLD).next_to(rec_cup, RIGHT, buff=0.12)
        sig_t4 = Dot(radius=0.09, color=ORANGE).move_to(strip.a_orange.get_start())
        self.play(Create(rec_cup), FadeIn(q2), run_time=1.1)
        self.play(sig_t4.animate.move_to([4.25, 3.08, 0]), run_time=1.8)
        self.play(FadeOut(sig_t4), run_time=0.5)

        self.at("ask what the assay measured")
        rule_line = caption("ask what the assay measured", size=32, color=TEXT, y=-3.05)
        self.play(
            FadeOut(q1), FadeOut(q2),
            FadeIn(rule_line, shift=UP * 0.12),
            run_time=1.4,
        )
        self.finish()


# ------------------------------------------------------------------ S08..S10
def build_blood_pool_world(extra_carriers=False, with_questions=False):
    strip = build_top_strip(thyroid_ok=True)
    pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
    panel = build_assay_panel("blood sample")
    panel.box.set_fill(TEAL, 0.12)
    gauges = build_three_gauges(tot_val=0.88 if extra_carriers else 0.50, tsh_val=0.50, ft4_val=0.50, usual_band=True)

    rng = np.random.default_rng(42)
    base_pos = [(-4.9, 0.75), (-2.6, 0.90), (-0.3, 0.65), (-4.2, -0.75), (-1.4, -0.85)]
    extra_pos = [(-5.1, -0.05), (-2.7, -0.10), (-0.1, -0.15), (-2.6, -1.65)]
    positions = base_pos + (extra_pos if extra_carriers else [])

    carriers = VGroup()
    for i, (cx, cy) in enumerate(positions):
        pill = RoundedRectangle(corner_radius=0.24, width=1.16, height=0.46, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.30).move_to([cx, cy, 0])
        dots = VGroup(*[
            Dot(radius=0.075, color=ORANGE).move_to([cx - 0.36 + k * 0.24, cy + rng.uniform(-0.08, 0.08), 0])
            for k in range(4)
        ])
        c = VGroup(pill, dots)
        c.home = np.array([cx, cy, 0.0])
        c.phase = i * 1.1
        carriers.add(c)

    free_pos = [(-3.8, 0.25), (-1.5, 0.15), (-3.2, -1.25)]
    free_dots = VGroup()
    for i, (fx, fy) in enumerate(free_pos):
        d = Dot(radius=0.095, color=ORANGE).move_to([fx, fy, 0])
        d.home = np.array([fx, fy, 0.0])
        d.phase = i * 1.7
        free_dots.add(d)

    def _attach_swim(mobs, amp_x=0.14, amp_y=0.09, speed=1.4):
        for m in mobs:
            m._st = m.phase

            def _u(mob, dt, ax=amp_x, ay=amp_y, sp=speed):
                mob._st += dt
                mob.move_to(mob.home + RIGHT * ax * np.sin(sp * mob._st) + UP * ay * np.cos(sp * 0.8 * mob._st))

            m.add_updater(_u)

    _attach_swim(carriers, amp_x=0.10, amp_y=0.06, speed=1.1)
    _attach_swim(free_dots, amp_x=0.22, amp_y=0.14, speed=1.9)

    lab_carrier = T("carrier protein", size=24, color=GREY).move_to([-4.65, -2.22, 0])
    lab_free = T("free", size=24, color=ORANGE).move_to([-0.80, -2.22, 0])
    # Placed cleanly in the 0.86-unit clear gap between TSH (4.48) and free T4 (5.34)
    usual_tag = T("usual", size=22, color=GREEN).move_to([4.91, -0.35, 0])

    world = VGroup(strip, panel, gauges, carriers, free_dots, lab_carrier, lab_free, usual_tag)
    world.strip, world.panel, world.gauges = strip, panel, gauges
    world.carriers, world.free_dots = carriers, free_dots
    world.lab_carrier, world.lab_free, world.usual_tag = lab_carrier, lab_free, usual_tag

    if with_questions:
        qt = T("?", size=32, color=GOLD).move_to(gauges.tsh.top_anchor + UP * 0.14)
        qf = T("?", size=32, color=GOLD).move_to(gauges.ft4.top_anchor + UP * 0.14)
        world.add(qt, qf)
        world.qt, world.qf = qt, qf
    return world


class S08Predict(SpokenScene):
    def construct(self):
        world = build_blood_pool_world(extra_carriers=False, with_questions=False)
        self.add(world)

        self.at("Nearly all T4")
        self.play(Indicate(world.carriers, color=ORANGE, scale_factor=1.04), run_time=1.0)

        self.at("Only the free part")
        # Pulse size only (keep ORANGE color!)
        self.play(*[Indicate(d, color=ORANGE, scale_factor=1.55) for d in world.free_dots], run_time=1.0)

        self.at("Oral estrogen raises")
        rng = np.random.default_rng(99)
        extra_pos = [(-5.1, -0.05), (-2.7, -0.10), (-0.1, -0.15), (-2.6, -1.65)]
        new_carriers = VGroup()
        for i, (cx, cy) in enumerate(extra_pos):
            pill = RoundedRectangle(corner_radius=0.24, width=1.16, height=0.46, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.30).move_to([cx, cy, 0])
            dots = VGroup(*[
                Dot(radius=0.075, color=ORANGE).move_to([cx - 0.36 + k * 0.24, cy + rng.uniform(-0.08, 0.08), 0])
                for k in range(4)
            ])
            c = VGroup(pill, dots)
            c.home = np.array([cx, cy, 0.0])
            c._st = (5 + i) * 1.1
            new_carriers.add(c)
        self.play(FadeIn(new_carriers, shift=DOWN * 0.12), run_time=1.0)
        for c in new_carriers:
            def _u(mob, dt):
                mob._st += dt
                mob.move_to(mob.home + RIGHT * 0.10 * np.sin(1.1 * mob._st) + UP * 0.06 * np.cos(0.88 * mob._st))
            c.add_updater(_u)

        self.at("so total T4 rises")
        self.play(world.gauges.tot_tr.animate.set_value(0.88), run_time=1.2)

        self.at("What do free T4")
        qt = T("?", size=32, color=GOLD).move_to(world.gauges.tsh.top_anchor + UP * 0.14)
        qf = T("?", size=32, color=GOLD).move_to(world.gauges.ft4.top_anchor + UP * 0.14)
        qcard = question_card("Free T4? TSH?", y=-3.05, color=TEXT, size=32)
        self.play(FadeIn(qt), FadeIn(qf), FadeIn(qcard), run_time=0.8)
        self.finish()


class S09PredictPause(PredictPause):
    QUESTION = "Free T4? TSH?"
    OPTIONS = ()
    CARD = {"y": -3.05, "color": TEXT, "size": 32}
    RING_AT = (5.85, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_blood_pool_world(extra_carriers=True, with_questions=True)


class S10Answer(SpokenScene):
    def construct(self):
        world = build_blood_pool_world(extra_carriers=True, with_questions=True)
        self.add(world)
        gauges = world.gauges

        self.at("Free T4 stays")
        near_tag = T("near\nusual", size=22, color=GREEN, line_spacing=0.82).move_to([4.91, -0.35, 0])
        self.play(FadeOut(world.qt), FadeOut(world.qf), run_time=0.35)
        self.play(
            swap(world.usual_tag, near_tag, run_time=0.8),
            Indicate(gauges.ft4.usual_band, color=GREEN, scale_factor=1.08),
            Indicate(gauges.tsh.usual_band, color=GREEN, scale_factor=1.08),
            run_time=0.85,
        )

        self.at("Pair TSH with")
        link_bad = ArcBetweenPoints(
            gauges.tsh.top_anchor + UP * 0.04,
            gauges.tot.top_anchor + UP * 0.04,
            angle=0.50, color=TEAL, stroke_width=4,
        )
        broken_tag = boxed_label("rule seems broken", color=RED, size=22, pad=0.10).move_to([4.05, 1.66, 0])
        self.play(Create(link_bad), FadeIn(broken_tag, shift=DOWN * 0.08), run_time=1.0)

        self.at("Pair it with Free")
        link_good = ArcBetweenPoints(
            gauges.tsh.top_anchor + UP * 0.04,
            gauges.ft4.top_anchor + UP * 0.04,
            angle=-0.50, color=TEAL, stroke_width=4,
        )
        holds_tag = boxed_label("rule holds", color=GREEN, size=22, pad=0.10).move_to([4.91, 1.66, 0])
        self.play(FadeOut(link_bad), FadeOut(broken_tag), run_time=0.45)
        self.play(Create(link_good), FadeIn(holds_tag, shift=DOWN * 0.08), run_time=0.95)
        self.finish()


# ------------------------------------------------------------------ S11
class S11Close(SpokenScene):
    def construct(self):
        strip = build_top_strip(thyroid_ok=True)
        pulse(strip.tick, base=5.0, amp=2.2, speed=4.0)
        panel = build_assay_panel("the assay")
        gauges = build_two_gauges(tsh_val=0.14, ft4_val=0.86, usual_band=True)
        self.add(strip, panel, gauges)

        self.at("Back to our")
        tube = make_sample_tube("", scale=0.32).move_to([-2.40, 1.78, 0])
        wells = build_two_wells(left_dim=False, right_dim=False, floor_label="capture floor", catch_hooks=True)
        wells.left_w.head.become(T("biotin catch", size=24, color=MAGENTA).move_to(wells.left_w.head))
        wells.right_w.head.become(T("no biotin step", size=24, color=GREEN).move_to(wells.right_w.head))
        wells.left_w.m_tr.set_value(0.20)
        wells.right_w.m_tr.set_value(0.75)
        self.play(FadeIn(wells), FadeIn(tube), run_time=1.5)

        self.at("Rerun the same blood")
        # Route pour streams along y = 1.48 (above well tops 1.38) then down inside LEFT edge of each well,
        # completely clear of 'signal' meters and headings!
        drop_l = VMobject(color=TEAL, stroke_width=3.5)
        drop_l.set_points_as_corners([np.array([-2.54, 1.50, 0]), np.array([-5.78, 1.50, 0]), np.array([-5.78, 0.35, 0])])
        drop_r = VMobject(color=TEAL, stroke_width=3.5)
        drop_r.set_points_as_corners([np.array([-2.26, 1.50, 0]), np.array([-2.02, 1.50, 0]), np.array([-2.02, 0.35, 0])])
        l_xs = [wells.lx - 1.25 + k * 0.62 for k in range(4)]
        r_xs = [wells.rx - 1.25 + k * 0.62 for k in range(3)]
        biotin_l = VGroup(*[Dot(radius=0.075, color=MAGENTA).move_to([x, wells.floor_y + 0.07, 0]) for x in l_xs])
        clean_r = VGroup(*[
            VGroup(
                make_antibody_y(TEAL, scale=0.72).move_to([x, wells.floor_y + 0.25, 0]),
                Dot(radius=0.12, color=YELLOW).move_to([x, wells.floor_y + 0.52, 0]),
                make_antibody_y(TEAL, scale=0.72, flip_down=True, tag=True).move_to([x, wells.floor_y + 0.90, 0]),
            )
            for x in r_xs
        ])
        res_l = T("TSH low,\nfree T4 high", size=22, color=ORANGE, line_spacing=0.85).move_to([wells.lx - 0.35, -0.45, 0])
        res_r = T("usual", size=26, color=GREEN).move_to([wells.rx - 0.35, 0.05, 0])
        self.play(Create(drop_l), Create(drop_r), run_time=1.0)
        self.play(
            FadeIn(biotin_l, lag_ratio=0.12), FadeIn(clean_r, lag_ratio=0.12),
            FadeIn(res_l), FadeIn(res_r),
            gauges.tsh_tr.animate.set_value(0.50),
            gauges.ft4_tr.animate.set_value(0.50),
            run_time=2.8,
        )

        self.at("A real change")
        self.play(Indicate(res_r, color=GREEN, scale_factor=1.15), Indicate(gauges.tsh.usual_band, color=GREEN), Indicate(gauges.ft4.usual_band, color=GREEN), run_time=1.6)

        self.at("only on one")
        art_frame = SurroundingRectangle(res_l, color=TEAL, buff=0.10, corner_radius=0.10, stroke_width=3)
        art_lab = T("artefact", size=22, color=TEAL).next_to(art_frame, UP, buff=0.08)
        self.play(Create(art_frame), FadeIn(art_lab), run_time=1.2)

        self.at("The pair still points")
        glow_axis_sequence(self, strip, step_time=1.05)
        self.play(
            Indicate(gauges.tsh, color=YELLOW, scale_factor=1.04),
            Indicate(gauges.ft4, color=ORANGE, scale_factor=1.04),
            run_time=0.8,
        )
        self.finish()


# ------------------------------------------------------------------ S12
class S12End(EndCard):
    LINE = "Before you read a pair, know what the assay measured."
