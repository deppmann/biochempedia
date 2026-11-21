"""
The Toll Paid Back — Chapter 2 of Membranes: The Impermeable Sheet That Builds Itself.

COLOUR MAP (kept consistent across every scene):
- BLUE   (#58C4DD): water, hydration shell droplets (6 per ion), and filter carbonyl oxygens (plain dots)
- GOLD   (#D4A843): oily hydrophobic core of the lipid bilayer
- TEAL   (#3FB8C0): potassium channel / selectivity filter walls, energy paid back, held-site highlight
- VIOLET (#B189C6): potassium ion (K+, drawn larger than Na+, with '+')
- YELLOW (#F5D547): sodium ion (Na+, drawn smaller than K+, with '+')
- RED    (#FC6255): dehydration toll for leaving water, and like-charge repulsion push arrows
- TEXT   (#E8EAF0): primary labels, question cards, computed kJ/mol bracket
- GREY   (#8B93A1): axes, schematic sieve outline, Newton's cradle, 'schematic' scope tag

CARRIED WORLD:
One horizontal schematic lipid bilayer (GOLD oily core left and right of a central pore, BLUE water
above and below) spanned by a TEAL potassium channel whose narrowest central stretch is a 4-site
(S1-S4) selectivity filter lined by rings of 8 BLUE oxygen dots, paired with RED/TEAL toll-and-payback
bars (and a computed 0-80 kJ/mol Plot in s06-s07) on the right.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
- s00_link_and_hook: Na+ sheds 6 water droplets to cross the generic channel while the red toll bar
  shrinks; the pore narrows to the K+ channel, K+ streams through while smaller Na+ bounces back
  twice, and the K+:Na+ ratio counter climbs to 1000:1 (lesson ratio > 1000:1).
- s02_filter: Camera zooms into the selectivity filter (70% frame height), BLUE oxygens light up along
  the walls and gather into 4 rings (S1-S4), S2 rotates to display 8 oxygens, and a grey sieve lets a
  ghost Na+ slip through before fading with '?'.
- s03_potassium: K+ sheds 6 water droplets as the RED toll bar rises; 8 oxygens close snugly around K+
  in S1 and the TEAL payback bar fills downward leaving a thin red sliver ('small net cost').
- s04_sodium: Na+ sheds tighter water droplets as a taller RED toll bar (+70/330 proportional height)
  rises; Na+ rattles inside the K+-sized 8-oxygen ring touching only 2-3 oxygens at a time, receives
  partial TEAL payback leaving a tall red remainder, and stalls outside while K+ passes below.
- s05_idea: Size bracket appears over K+ and Na+ then fades; K+ and Na+ toll/payback bars slide side by
  side ('potassium: nearly repaid' vs 'sodium: underpaid') as K+ ions step down S1-S4.
- s06_how_exact: Bar pairs transform into a computed 0-80 kJ/mol Plot: RED bar rises to 70 (extra
  Na+ toll) and a white bracket computed from RT*ln(1000) = 2.58*ln(1000) = 17.82 kJ/mol at 37 C
  marks 'about 18' at the top while K+ steps through the small filter at left.
- s07_slack: On the same Plot, a TEAL bar rises from 0 to computed 70 - 17.82 = 52.18 ('about 52:
  extra payback allowed') below the 18 bracket, then an unnumbered schematic 'simulations' bar rises
  partway below 52 without closing the gap.
- s08_predict: Chart fades and filter zooms to 70% height with one K+ held snugly in S2's 8 oxygens;
  the throughput counter climbs to 'about 100,000,000 per s' (10^8/s), a second K+ waits above S1,
  and the question card appears.
- s10_knock_on: Question card clears, three K+ ions occupy S2-S4, RED repulsion arrows appear between
  neighbours, and a continuous knock-on cycle pushes an entering K+ into S1 and the lowest K+ out.
- s11_hedges: Knock-on keeps running at left; at right a schematic Newton's cradle swings once and is
  marked X ('image only'), followed by water-separated ('still argued', dimmed graphic) and direct
  contact ('recent evidence: contact') ion pairs.
- s12_return: Pulls back to opening bilayer + tall K+ channel with knock-on stream; K+ and Na+ toll/
  payback bars appear as Na+ bounces off the entrance, size bracket fades out, and TEAL bars highlight.
"""

import numpy as np
from bp_parts import *  # noqa: F401,F403
from kx_manim import TAIL

VIOLET = "#B189C6"

# Physical & lesson constants (from lesson_for_context.mdx)
K_RADIUS = 0.24
NA_RADIUS = 0.17          # 0.95 A / 1.33 A ~ 0.714 -> 0.24 * 0.71 ~ 0.17
RT_37 = 2.58              # kJ/mol at 37 C
DELTA_TOLL = 70.0         # kJ/mol (Na+ hydration toll minus K+ toll)
NEEDED_GAP = RT_37 * float(np.log(1000.0))   # 17.82 kJ/mol -> "about 18"
SLACK_PAYBACK = DELTA_TOLL - NEEDED_GAP       # 52.18 kJ/mol -> "about 52"
K_TOLL_REL = 1.0
NA_TOLL_REL = 1.0 + DELTA_TOLL / 330.0       # proportional to 400 vs 330 kJ/mol teaching scale


def make_ion(kind="K", radius=None, scale=1.0):
    """Circle with dark geometric '+' inside (no small Text to avoid font-floor warnings)."""
    is_k = (kind == "K")
    r = (K_RADIUS if is_k else NA_RADIUS) * scale if radius is None else radius
    col = VIOLET if is_k else YELLOW
    circ = Circle(radius=r, color=col, fill_color=col, fill_opacity=0.94,
                  stroke_color=TEXT, stroke_width=2.0)
    arm = r * 0.44
    sw = max(2.2, 10.5 * r)
    plus = VGroup(
        Line(LEFT * arm, RIGHT * arm, color=BG, stroke_width=sw),
        Line(DOWN * arm, UP * arm, color=BG, stroke_width=sw),
    )
    return VGroup(circ, plus)


def make_water_shell(center, ion_r, tight=False, droplet_r=None):
    """Six BLUE water-shell droplets around an ion."""
    dr = (0.068 if droplet_r is None else droplet_r)
    orbit = ion_r + (0.095 if tight else 0.155)
    c = np.array(center, dtype=float)
    drops = VGroup()
    for k in range(6):
        ang = k * TAU / 6.0 + PI / 6.0
        pos = c + orbit * np.array([np.cos(ang), np.sin(ang), 0.0])
        drops.add(Dot(pos, radius=dr, color=BLUE))
    return drops


def make_bilayer(pore_half_w=0.58, y_mid=0.0, core_h=2.8, x_lim=6.1):
    """GOLD oily bilayer core left and right of the pore, plus subtle water boundary lines."""
    y0, y1 = y_mid - core_h / 2.0, y_mid + core_h / 2.0
    w_side = x_lim - pore_half_w
    left_core = Rectangle(
        width=w_side, height=core_h,
        fill_color=GOLD, fill_opacity=0.22, stroke_color=GOLD, stroke_width=2.5,
    ).move_to([-(pore_half_w + w_side / 2.0), y_mid, 0])
    right_core = Rectangle(
        width=w_side, height=core_h,
        fill_color=GOLD, fill_opacity=0.22, stroke_color=GOLD, stroke_width=2.5,
    ).move_to([pore_half_w + w_side / 2.0, y_mid, 0])
    # Subtle BLUE water regions top and bottom (open horizontal lines, no closed panels)
    water_top = Line([-x_lim, y1 + 0.08, 0], [x_lim, y1 + 0.08, 0], color=BLUE, stroke_width=2).set_opacity(0.45)
    water_bot = Line([-x_lim, y0 - 0.08, 0], [x_lim, y0 - 0.08, 0], color=BLUE, stroke_width=2).set_opacity(0.45)
    return VGroup(left_core, right_core, water_top, water_bot)


def make_channel_walls(cx=0.0, y_mid=0.0, half_w=0.52, wall_w=0.24, height=3.4):
    """Two TEAL channel wall blocks flanking the pore."""
    y0, y1 = y_mid - height / 2.0, y_mid + height / 2.0
    lw = Rectangle(
        width=wall_w, height=height,
        fill_color=TEAL, fill_opacity=0.32, stroke_color=TEAL, stroke_width=3.0,
    ).move_to([cx - half_w - wall_w / 2.0, y_mid, 0])
    rw = Rectangle(
        width=wall_w, height=height,
        fill_color=TEAL, fill_opacity=0.32, stroke_color=TEAL, stroke_width=3.0,
    ).move_to([cx + half_w + wall_w / 2.0, y_mid, 0])
    # Short flared mouth caps at top/bottom for visual clarity
    return VGroup(lw, rw), y0, y1


def make_filter_tube(cx=-1.6, y_top=2.3, y_bot=-2.1, half_w=0.72, wall_w=0.28, label_sites=True, right_band_w=0.85):
    """Tall zoomed selectivity filter with 4 binding-site rings (S1-S4) of 8 BLUE oxygen dots."""
    h = y_top - y_bot
    ym = (y_top + y_bot) / 2.0
    lw = Rectangle(
        width=wall_w, height=h,
        fill_color=TEAL, fill_opacity=0.28, stroke_color=TEAL, stroke_width=3.2,
    ).move_to([cx - half_w - wall_w / 2.0, ym, 0])
    rw = Rectangle(
        width=wall_w, height=h,
        fill_color=TEAL, fill_opacity=0.28, stroke_color=TEAL, stroke_width=3.2,
    ).move_to([cx + half_w + wall_w / 2.0, ym, 0])

    # Bilayer GOLD bands flanking the tube
    b_h = h * 0.80
    left_band = Rectangle(
        width=max(0.6, cx - half_w - wall_w - (-6.1)), height=b_h,
        fill_color=GOLD, fill_opacity=0.18, stroke_color=GOLD, stroke_width=2.0,
    )
    left_band.move_to([(-6.1 + (cx - half_w - wall_w)) / 2.0, ym, 0])
    right_band = Rectangle(
        width=right_band_w, height=b_h,
        fill_color=GOLD, fill_opacity=0.18, stroke_color=GOLD, stroke_width=2.0,
    ).move_to([cx + half_w + wall_w + right_band_w / 2.0, ym, 0])

    site_ys = [y_top - h * f for f in (0.21, 0.40, 0.60, 0.79)]
    rings = VGroup()
    site_labels = VGroup()
    ox_r = 0.075 * (h / 4.4)
    for idx, sy in enumerate(site_ys, 1):
        # 8 BLUE oxygens shown as 4 pairs along the inner walls (or 8 around a tilted ellipse)
        ring = VGroup()
        for k in range(8):
            ang = k * TAU / 8.0 + PI / 8.0
            dx = (half_w - 0.14) * np.cos(ang)
            dy = 0.15 * (h / 4.4) * np.sin(ang)
            ring.add(Dot([cx + dx, sy + dy, 0], radius=ox_r, color=BLUE))
        rings.add(ring)
        if label_sites:
            lbl = T(f"S{idx}", 24, BLUE).move_to([cx - half_w - wall_w - 0.42, sy, 0])
            site_labels.add(lbl)

    g = VGroup(left_band, right_band, lw, rw, rings, site_labels)
    g.cx = cx
    g.y_top = y_top
    g.y_bot = y_bot
    g.half_w = half_w
    g.wall_w = wall_w
    g.site_ys = site_ys
    g.rings = rings
    g.site_labels = site_labels
    g.lw = lw
    g.rw = rw
    g.bands = VGroup(left_band, right_band)
    return g


def make_size_bracket(k_pos, na_pos, r_scale=1.0, show_bracket=True):
    """K+ and Na+ side by side with optional size comparison bracket above them."""
    k_ion = make_ion("K", scale=r_scale)
    na_ion = make_ion("Na", scale=r_scale)
    k_ion.move_to(k_pos)
    na_ion.move_to(na_pos)
    k_lbl = T("K⁺", 26, VIOLET).next_to(k_ion, DOWN, buff=0.14)
    na_lbl = T("Na⁺", 26, YELLOW).next_to(na_ion, DOWN, buff=0.14)
    g = VGroup(k_ion, na_ion, k_lbl, na_lbl)
    if show_bracket:
        top_y = max(k_ion.get_top()[1], na_ion.get_top()[1]) + 0.18
        br = VGroup(
            Line([na_ion.get_left()[0], top_y, 0], [na_ion.get_right()[0], top_y, 0], color=YELLOW, stroke_width=3),
            Line([na_ion.get_left()[0], top_y - 0.08, 0], [na_ion.get_left()[0], top_y + 0.08, 0], color=YELLOW, stroke_width=3),
            Line([na_ion.get_right()[0], top_y - 0.08, 0], [na_ion.get_right()[0], top_y + 0.08, 0], color=YELLOW, stroke_width=3),
        )
        txt = T("smaller", 24, YELLOW).next_to(br, UP, buff=0.10)
        g.bracket = VGroup(br, txt)
        g.add(g.bracket)
    return g


def make_toll_bar_pair(x, y_base, max_h, toll_frac=1.0, pay_frac=0.92, label_text="", label_col=TEXT):
    """Schematic vertical RED toll bar filled downward by TEAL payback bar."""
    bar_w = 0.65
    toll_h = max_h * toll_frac
    pay_h = toll_h * pay_frac
    red_bar = Rectangle(
        width=bar_w, height=toll_h,
        fill_color=RED, fill_opacity=0.88, stroke_color=RED, stroke_width=2.0,
    ).move_to([x, y_base + toll_h / 2.0, 0])
    teal_bar = Rectangle(
        width=bar_w, height=max(0.02, pay_h),
        fill_color=TEAL, fill_opacity=0.90, stroke_color=TEAL, stroke_width=2.0,
    ).move_to([x, y_base + toll_h - pay_h / 2.0, 0])
    g = VGroup(red_bar, teal_bar)
    g.red_bar = red_bar
    g.teal_bar = teal_bar
    if label_text:
        lbl = T(label_text, 24, label_col).move_to([x, y_base - 0.36, 0])
        g.lbl = lbl
        g.add(lbl)
    return g


def make_exact_plot():
    """Computed 0-80 kJ/mol Plot shared across s06_how_exact and s07_slack."""
    P = Plot(
        box=(-1.1, 4.5, -1.9, 2.7),
        xr=(0, 3),
        yr=(0, 80),
        xticks=[],
        yticks=[(v, str(v)) for v in range(0, 81, 10)],
        xlabel="",
        ylabel="kJ per mole",
        color=GREY,
        size=24,
        label_size=26,
    )
    return P


def add_small_left_filter(scene, k_speed=1.3, show_na_hover=False):
    """Compact active 4-site filter on the left for s05/s06/s07 with continuous K+ stepping."""
    ft = make_filter_tube(cx=-4.2, y_top=1.9, y_bot=-1.7, half_w=0.52, wall_w=0.22, label_sites=False)
    ft.bands[0].stretch_to_fit_width(0.85).move_to([-4.2 - 0.52 - 0.22 - 0.425, 0.1, 0])
    ft.bands[1].stretch_to_fit_width(0.85).move_to([-4.2 + 0.52 + 0.22 + 0.425, 0.1, 0])
    scene.add(ft)

    # Continuous K+ stepping stream inside the small filter
    n_ions = 4
    ys_path = [2.4, *ft.site_ys, -2.3]
    ions = VGroup(*[make_ion("K", radius=0.18) for _ in range(n_ions)])
    phase = ValueTracker(0.0)

    def update_stream(mob):
        p = phase.get_value()
        for idx, ion in enumerate(mob):
            u = (p + idx / n_ions) % 1.0
            seg_f = u * (len(ys_path) - 1)
            k = min(int(seg_f), len(ys_path) - 2)
            frac = seg_f - k
            # Slight pause at each site then quick step
            smooth_f = 0.5 * (1 - np.cos(PI * np.clip((frac - 0.15) / 0.7, 0, 1)))
            y = ys_path[k] * (1 - smooth_f) + ys_path[k + 1] * smooth_f
            ion.move_to([ft.cx, y, 0])
            ion.set_opacity(1.0 if -2.1 <= y <= 2.2 else max(0.0, 1.0 - abs(y - 0.1) * 0.4))

    ions.add_updater(update_stream)
    update_stream(ions)
    scene.add(ions)

    if show_na_hover:
        na = make_ion("Na", radius=0.14).move_to([ft.cx + 0.38, ft.y_top + 0.48, 0])
        t_na = ValueTracker(0.0)
        na.add_updater(lambda m: m.move_to([
            ft.cx + 0.38,
            ft.y_top + 0.45 + 0.08 * np.sin(2.5 * t_na.get_value()),
            0,
        ]))
        scene.add(na)
        return ft, phase, t_na
    return ft, phase


# ==============================================================================
# SCENES
# ==============================================================================

class S00LinkAndHook(SpokenScene):
    def construct(self):
        bilayer = make_bilayer(pore_half_w=0.68, y_mid=0.0, core_h=2.7, x_lim=6.1)
        walls, wy0, wy1 = make_channel_walls(cx=0.0, y_mid=0.0, half_w=0.58, wall_w=0.25, height=3.2)
        grip_dots = VGroup(
            *[Dot([-0.42, y, 0], radius=0.07, color=BLUE) for y in (-0.8, 0.0, 0.8)],
            *[Dot([0.42, y, 0], radius=0.07, color=BLUE) for y in (-0.8, 0.0, 0.8)],
        )

        # Recap RED toll bar at left
        toll_base = np.array([-4.4, -0.80, 0])
        toll_h = ValueTracker(1.65)
        toll_frame = Rectangle(width=0.55, height=1.70, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(
            toll_base + UP * 0.85
        )
        toll_bar = always_redraw(lambda: Rectangle(
            width=0.55, height=max(0.04, toll_h.get_value()),
            fill_color=RED, fill_opacity=0.88, stroke_color=RED, stroke_width=2,
        ).move_to(toll_base + UP * (max(0.04, toll_h.get_value()) / 2.0)))
        toll_lbl = T("toll", 26, RED).move_to([-4.4, -1.80, 0])

        na_recap = make_ion("Na", radius=NA_RADIUS).move_to([0.0, 2.25, 0])
        na_shell = make_water_shell([0.0, 2.25, 0], NA_RADIUS, tight=False)
        tag = scope_tag("schematic")

        self.add(bilayer, walls, grip_dots, toll_frame, toll_bar, toll_lbl, na_recap, na_shell, tag)

        # First sentence (0..3.8s): Na+ sheds water shell to grip dots and crosses while toll bar shrinks
        self.play(
            na_recap.animate.move_to([0.0, 0.85, 0]),
            na_shell.animate.move_to([0.0, 0.85, 0]),
            run_time=1.3,
        )
        self.play(
            FadeOut(na_shell),
            toll_h.animate.set_value(0.45),
            na_recap.animate.move_to([0.0, -2.0, 0]),
            run_time=2.2,
        )
        self.play(FadeOut(na_recap), FadeOut(toll_frame), FadeOut(toll_bar), FadeOut(toll_lbl), run_time=0.45)

        # "A potassium channel goes further." -> narrow channel into tall K+ channel
        self.at("potassium channel")
        narrow_bilayer = make_bilayer(pore_half_w=0.48, y_mid=0.0, core_h=2.7, x_lim=6.1)
        narrow_walls, _, _ = make_channel_walls(cx=0.0, y_mid=0.0, half_w=0.38, wall_w=0.26, height=3.8)
        narrow_dots = VGroup(
            *[Dot([-0.26, y, 0], radius=0.06, color=BLUE) for y in (-1.0, -0.33, 0.33, 1.0)],
            *[Dot([0.26, y, 0], radius=0.06, color=BLUE) for y in (-1.0, -0.33, 0.33, 1.0)],
        )
        ch_lbl = T("potassium channel", 28, TEAL).move_to([3.55, 1.95, 0])
        self.play(
            Transform(bilayer, narrow_bilayer),
            Transform(walls, narrow_walls),
            Transform(grip_dots, narrow_dots),
            FadeIn(ch_lbl),
            run_time=1.0,
        )

        # Counter beside the tube: potassium: 1000 vs sodium: 1
        k_count = ValueTracker(1.0)
        ro = Readout(
            [
                ("potassium", lambda: k_count.get_value(), "{:4.0f}", VIOLET),
                ("sodium", lambda: 1, "{:4.0f}", YELLOW),
            ],
            at=[3.55, 0.0, 0],
            size=26,
            widest=[1000, 1],
            title="relative crossings",
        )
        self.play(FadeIn(ro), run_time=0.5)

        # Continuous stream of VIOLET K+ ions downward + YELLOW Na+ bouncing twice at entrance
        stream_t = ValueTracker(0.0)
        k_ions = VGroup(*[make_ion("K", radius=K_RADIUS) for _ in range(4)])

        def update_k_stream(mob):
            t = stream_t.get_value()
            for idx, ion in enumerate(mob):
                u = (t * 0.42 + idx / 4.0) % 1.0
                y = 2.6 - u * 5.2
                ion.move_to([0.0, y, 0])
                op = 1.0
                if y > 2.2:
                    op = max(0.0, (2.6 - y) / 0.4)
                elif y < -2.2:
                    op = max(0.0, (y + 2.6) / 0.4)
                ion.set_opacity(op)

        k_ions.add_updater(update_k_stream)
        update_k_stream(k_ions)

        na_bounce = make_ion("Na", radius=NA_RADIUS).move_to([-0.85, 2.55, 0])
        self.add(k_ions, na_bounce)

        # Bounce 1 and counter tick up while K+ streams
        t_smaller = self.t_of("smaller ion") - 0.2
        dt_stream = max(1.5, t_smaller - self.elapsed())
        # Piecewise Na+ bounce path via tracker
        na_phase = ValueTracker(0.0)

        def update_na_bounce(m):
            p = na_phase.get_value()
            # Two bounces at p=0.25 and p=0.70 against top entrance [0.0, 2.05]
            if p < 0.25:
                f = p / 0.25
                pos = np.array([-0.85 * (1 - f), 2.55 * (1 - f) + 2.08 * f, 0.0])
            elif p < 0.50:
                f = (p - 0.25) / 0.25
                pos = np.array([0.85 * f, 2.08 * (1 - f) + 2.55 * f, 0.0])
            elif p < 0.75:
                f = (p - 0.50) / 0.25
                pos = np.array([0.85 * (1 - f), 2.55 * (1 - f) + 2.08 * f, 0.0])
            else:
                f = (p - 0.75) / 0.25
                pos = np.array([-0.85 * f, 2.08 * (1 - f) + 2.55 * f, 0.0])
            m.move_to(pos)

        na_bounce.add_updater(update_na_bounce)
        self.play(
            stream_t.animate.set_value(dt_stream),
            na_phase.animate.set_value(1.0),
            k_count.animate.set_value(1000.0),
            run_time=dt_stream,
            rate_func=linear,
        )
        na_bounce.clear_updaters()
        self.play(FadeOut(na_bounce), run_time=0.25)

        # "Yet sodium is the smaller ion. How can a pore turn away the smaller ion?"
        self.at("smaller ion")
        comp = make_size_bracket([-4.1, 2.15, 0], [-2.9, 2.15, 0], r_scale=0.90, show_bracket=True)
        q_text = T("Why is the smaller ion refused?", 32, TEXT).move_to([0.75, 3.24, 0])
        self.play(FadeIn(comp), FadeIn(q_text), run_time=0.7)

        rem = max(0.5, self.narration_s + TAIL - self.elapsed())
        self.play(stream_t.animate.set_value(stream_t.get_value() + rem), run_time=rem, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Membranes: The Impermeable Sheet That Builds Itself"
    TITLE = "The Toll Paid Back"


class S02Filter(SpokenScene):
    def construct(self):
        # Start from zoomed-out pore and dive into the selectivity filter (~70% frame height)
        ft = make_filter_tube(cx=0.0, y_top=2.35, y_bot=-2.35, half_w=0.85, wall_w=0.32, label_sites=False)
        # Initially scale down from opening channel proportions, then zoom in smoothly
        ft_start = make_filter_tube(cx=0.0, y_top=1.5, y_bot=-1.5, half_w=0.45, wall_w=0.22, label_sites=False)
        ft_start.rings.set_opacity(0.0)
        ft.rings.set_opacity(0.0)

        lbl = T("selectivity filter", 32, TEAL).move_to([0.0, 3.05, 0])
        tag = scope_tag("schematic")

        self.add(ft_start, tag)
        self.play(Transform(ft_start, ft), FadeIn(lbl), run_time=2.6)
        self.remove(ft_start)
        self.add(ft)

        # "lined mostly with oxygens"
        self.at("lined mostly with")
        wall_dots = VGroup(
            *[Dot([-ft.half_w + 0.14, y, 0], radius=0.085, color=BLUE) for y in np.linspace(-1.85, 1.85, 8)],
            *[Dot([ft.half_w - 0.14, y, 0], radius=0.085, color=BLUE) for y in np.linspace(-1.85, 1.85, 8)],
        )
        oxy_lbl = T("oxygens", 28, BLUE).move_to([3.55, 1.45, 0])
        self.play(FadeIn(wall_dots), FadeIn(oxy_lbl), run_time=0.9)

        # "Four binding sites sit in a row."
        self.at("four binding sites")
        ft.rings.set_opacity(1.0)
        # Re-add site labels neatly at left of left wall
        site_lbls = VGroup(*[
            T(f"S{i}", 26, BLUE).move_to([ft.cx - ft.half_w - ft.wall_w - 0.48, sy, 0])
            for i, sy in enumerate(ft.site_ys, 1)
        ])
        self.play(FadeOut(wall_dots), FadeIn(ft.rings), FadeIn(site_lbls), run_time=1.0)

        # "Each site is a cage of eight oxygens."
        self.at("cage of eight")
        s2_y = ft.site_ys[1]
        cage_center = np.array([3.95, 0.35, 0])
        cage_r = 0.80
        cage_ang = ValueTracker(0.0)
        cage_dots = always_redraw(lambda: VGroup(*[
            Dot(
                cage_center + cage_r * np.array([np.cos(k * TAU / 8.0 + cage_ang.get_value()),
                                                 np.sin(k * TAU / 8.0 + cage_ang.get_value()), 0.0]),
                radius=0.11, color=BLUE,
            )
            for k in range(8)
        ]))
        cage_ring = Circle(radius=cage_r, color=TEAL, stroke_width=2.0).set_opacity(0.45).move_to(cage_center)
        lead_line = DashedLine([ft.cx + ft.half_w + ft.wall_w + 0.05, s2_y, 0],
                               [cage_center[0] - cage_r - 0.15, cage_center[1], 0],
                               color=TEAL, stroke_width=2.5)
        eight_lbl = T("8 oxygens", 28, BLUE).next_to(cage_ring, DOWN, buff=0.22)
        self.play(FadeOut(oxy_lbl), FadeIn(cage_ring), FadeIn(cage_dots), Create(lead_line), FadeIn(eight_lbl), run_time=0.6)
        self.play(cage_ang.animate.set_value(PI / 2.0), run_time=1.6, rate_func=linear)

        # "A sieve this narrow would favor sodium."
        self.at("sieve")
        sieve_lines = VGroup(
            *[Line([-ft.half_w, y, 0], [ft.half_w, y, 0], color=GREY, stroke_width=2.5) for y in np.linspace(-1.9, 1.9, 9)],
            *[Line([x, -2.1, 0], [x, 2.1, 0], color=GREY, stroke_width=2.5) for x in (-0.42, 0.0, 0.42)],
        ).set_opacity(0.55)
        ghost_na = make_ion("Na", radius=NA_RADIUS * 1.25).set_opacity(0.65).move_to([0.0, 2.55, 0])
        self.play(FadeIn(sieve_lines), FadeIn(ghost_na), run_time=0.4)
        self.play(ghost_na.animate.move_to([0.0, -2.55, 0]), run_time=1.2)
        q_mark = T("?", 46, YELLOW).move_to([0.0, 0.0, 0])
        self.play(FadeOut(sieve_lines), FadeOut(ghost_na), FadeIn(q_mark), run_time=0.45)
        self.finish()


class S03Potassium(SpokenScene):
    def construct(self):
        ft = make_filter_tube(cx=-2.0, y_top=2.3, y_bot=-2.1, half_w=0.76, wall_w=0.28, label_sites=True)
        # Adjust S1 ring radius slightly open at start so 8 oxygens can visibly close in on K+
        s1_y = ft.site_ys[0]
        s1_open_r = ValueTracker(0.66)
        ft.rings[0].set_opacity(0.0)
        s1_ring = always_redraw(lambda: VGroup(*[
            Dot([ft.cx + s1_open_r.get_value() * np.cos(k * TAU / 8.0 + PI / 8.0),
                 s1_y + 0.16 * np.sin(k * TAU / 8.0 + PI / 8.0), 0], radius=0.085, color=BLUE)
            for k in range(8)
        ]))

        k_r = 0.34
        k_ion = make_ion("K", radius=k_r).move_to([ft.cx, 2.95, 0])
        k_shell = make_water_shell([ft.cx, 2.95, 0], k_r, tight=False, droplet_r=0.08)

        # Energy bar frame at right
        bar_x = 2.6
        bar_base = -1.7
        bar_max_h = 3.2
        toll_h = ValueTracker(0.01)
        pay_h = ValueTracker(0.01)
        bar_title = T("K⁺ toll & payback", 28, VIOLET).move_to([bar_x, 2.45, 0])
        red_bar = always_redraw(lambda: Rectangle(
            width=0.95, height=max(0.02, toll_h.get_value()),
            fill_color=RED, fill_opacity=0.88, stroke_color=RED, stroke_width=2.0,
        ).move_to([bar_x, bar_base + max(0.02, toll_h.get_value()) / 2.0, 0]))
        teal_bar = always_redraw(lambda: Rectangle(
            width=0.95, height=max(0.02, pay_h.get_value()),
            fill_color=TEAL, fill_opacity=0.90, stroke_color=TEAL, stroke_width=2.0,
        ).move_to([bar_x, bar_base + toll_h.get_value() - max(0.02, pay_h.get_value()) / 2.0, 0]))
        k_lbl = T("K⁺", 28, VIOLET).move_to([bar_x, bar_base - 0.36, 0])
        tag = scope_tag("schematic")

        self.add(ft, s1_ring, k_ion, k_shell, bar_title, red_bar, teal_bar, k_lbl, tag)

        # Descend to entrance smoothly
        self.play(
            k_ion.animate.move_to([ft.cx, 2.55, 0]),
            k_shell.animate.move_to([ft.cx, 2.55, 0]),
            run_time=1.6,
        )

        # "shed its water shell and pay the toll"
        self.at("shed its water")
        peel_anims = [d.animate.shift((d.get_center() - k_ion.get_center()) * 1.4).set_opacity(0.0) for d in k_shell]
        k_toll_target = bar_max_h * K_TOLL_REL
        self.play(
            *peel_anims,
            k_ion.animate.move_to([ft.cx, s1_y, 0]),
            toll_h.animate.set_value(k_toll_target),
            run_time=3.6,
        )
        self.remove(k_shell)

        # "Inside a site, eight oxygens sit close, where its water sat."
        self.at("eight oxygens sit")
        eight_lbl = T("8 oxygens", 26, BLUE).move_to([0.92, s1_y, 0])
        self.play(
            s1_open_r.animate.set_value(k_r + 0.10),
            FadeIn(eight_lbl),
            run_time=3.2,
        )

        # "They pay back nearly all of it."
        self.at("pay back nearly")
        net_cost_h = 0.22
        self.play(pay_h.animate.set_value(k_toll_target - net_cost_h), run_time=3.6)

        # "So potassium enters at little net cost."
        self.at("little net cost")
        sliver_arrow = Arrow([bar_x + 0.72, bar_base + net_cost_h / 2.0, 0],
                             [bar_x + 0.50, bar_base + net_cost_h / 2.0, 0],
                             buff=0, color=RED, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        sliver_lbl = T("small net cost", 26, RED).next_to(sliver_arrow, RIGHT, buff=0.14)
        self.play(FadeIn(sliver_lbl), Create(sliver_arrow), run_time=1.0)

        # Settle into S1 until scene ends
        rem = max(0.3, self.narration_s + TAIL - self.elapsed())
        t_settle = ValueTracker(0.0)
        k_ion.add_updater(lambda m: m.move_to([ft.cx, s1_y + 0.05 * np.sin(3.5 * t_settle.get_value()), 0]))
        self.play(t_settle.animate.set_value(rem), run_time=rem, rate_func=linear)
        self.finish()


class S04Sodium(SpokenScene):
    def construct(self):
        ft = make_filter_tube(cx=-2.2, y_top=2.3, y_bot=-2.1, half_w=0.76, wall_w=0.28, label_sites=True)
        s1_y = ft.site_ys[0]
        # Keep 8 oxygens at K+-sized cage in S1 (we animate individual oxygen flashes below)
        ft.rings[0].set_opacity(0.0)
        s1_ring = VGroup(*[
            Dot([ft.cx + 0.44 * np.cos(k * TAU / 8.0 + PI / 8.0),
                 s1_y + 0.16 * np.sin(k * TAU / 8.0 + PI / 8.0), 0], radius=0.085, color=BLUE)
            for k in range(8)
        ])

        # Carried K+ bar pair at x=2.0; new Na+ bar pair beside it at x=4.1
        bar_base = -1.7
        bar_max_h = 3.0
        k_bar = make_toll_bar_pair(2.0, bar_base, bar_max_h, toll_frac=K_TOLL_REL, pay_frac=0.93,
                                   label_text="K⁺", label_col=VIOLET)

        na_r = 0.24  # 0.34 * 0.71
        na_ion = make_ion("Na", radius=na_r).move_to([ft.cx, 2.95, 0])
        na_shell = make_water_shell([ft.cx, 2.95, 0], na_r, tight=True, droplet_r=0.075)
        tag = scope_tag("schematic")

        self.add(ft, s1_ring, k_bar, na_ion, na_shell, tag)
        self.play(
            na_ion.animate.move_to([ft.cx, 2.55, 0]),
            na_shell.animate.move_to([ft.cx, 2.55, 0]),
            run_time=2.6,
        )

        # "so its toll is larger"
        self.at("toll is larger")
        na_x = 4.1
        na_toll_h = ValueTracker(0.01)
        na_pay_h = ValueTracker(0.01)
        na_red = always_redraw(lambda: Rectangle(
            width=0.80, height=max(0.02, na_toll_h.get_value()),
            fill_color=RED, fill_opacity=0.88, stroke_color=RED, stroke_width=2.0,
        ).move_to([na_x, bar_base + max(0.02, na_toll_h.get_value()) / 2.0, 0]))
        na_teal = always_redraw(lambda: Rectangle(
            width=0.80, height=max(0.02, na_pay_h.get_value()),
            fill_color=TEAL, fill_opacity=0.90, stroke_color=TEAL, stroke_width=2.0,
        ).move_to([na_x, bar_base + na_toll_h.get_value() - max(0.02, na_pay_h.get_value()) / 2.0, 0]))
        na_lbl = T("Na⁺", 28, YELLOW).move_to([na_x, bar_base - 0.36, 0])
        self.add(na_red, na_teal, na_lbl)

        peel = [d.animate.shift((d.get_center() - na_ion.get_center()) * 1.5).set_opacity(0.0) for d in na_shell]
        na_toll_target = bar_max_h * NA_TOLL_REL
        self.play(
            *peel,
            na_ion.animate.move_to([ft.cx, s1_y, 0]),
            na_toll_h.animate.set_value(na_toll_target),
            run_time=2.2,
        )
        self.remove(na_shell)

        # Rattling Na+ touches 2-3 oxygens on one side at a time; touched dots flash bright with contact halo
        rattle_t = ValueTracker(0.0)

        def update_rattle(m):
            t = rattle_t.get_value()
            dx = 0.32 * np.cos(8.5 * t)
            dy = 0.09 * np.sin(12.0 * t)
            m.move_to([ft.cx + dx, s1_y + dy, 0])

        def update_ring(ring):
            c = na_ion.get_center()
            for dot in ring:
                dist = np.linalg.norm(dot.get_center() - c)
                if dist < 0.28:
                    dot.set_color(TEXT).scale_to_fit_width(0.24)
                else:
                    dot.set_color(BLUE).scale_to_fit_width(0.17)

        na_ion.add_updater(update_rattle)
        s1_ring.add_updater(update_ring)
        contact_halo = always_redraw(lambda: VGroup(*[
            Circle(radius=0.13, color=YELLOW, stroke_width=3.5).move_to(dot.get_center())
            for dot in s1_ring
            if np.linalg.norm(dot.get_center() - na_ion.get_center()) < 0.28
        ]))
        self.add(contact_halo)
        t_too = self.t_of("too small to") - 0.2
        pre_dur = max(0.3, t_too - self.elapsed())
        self.play(rattle_t.animate.set_value(pre_dur), run_time=pre_dur, rate_func=linear)

        # "too small to touch all eight oxygens at once"
        self.at("too small to")
        snug_tag = T("snug-fit picture", 26, GREY).move_to([3.05, 2.85, 0])
        self.play(
            FadeIn(snug_tag),
            rattle_t.animate.set_value(rattle_t.get_value() + 0.4),
            run_time=0.4,
            rate_func=linear,
        )

        t_not_paid = self.t_of("not paid back") - 0.2
        rattle_dur = max(1.0, t_not_paid - self.elapsed())
        self.play(rattle_t.animate.set_value(rattle_t.get_value() + rattle_dur), run_time=rattle_dur, rate_func=linear)
        na_ion.clear_updaters()
        s1_ring.clear_updaters()
        self.remove(contact_halo)
        for dot in s1_ring:
            dot.set_color(BLUE).scale_to_fit_width(0.17)

        # "is not paid back enough"
        self.at("not paid back")
        self.play(na_pay_h.animate.set_value(na_toll_target * 0.56), run_time=1.8)

        # "So it stalls." -> Na+ backs out while a violet K+ ion below moves down through S2-S4
        self.at("so it stalls")
        k_below = make_ion("K", radius=0.28).move_to([ft.cx, ft.site_ys[1], 0])
        self.add(k_below)
        self.play(
            na_ion.animate.move_to([ft.cx, ft.y_top + 0.55, 0]),
            k_below.animate.move_to([ft.cx, ft.y_bot - 0.45, 0]),
            run_time=1.2,
        )
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        ft, phase = add_small_left_filter(self, show_na_hover=False)
        ft.shift(RIGHT * 0.8)  # move slightly right to cx = -3.4
        ft.cx = -3.4

        # Rebuild stream at cx = -3.4 cleanly
        self.clear()
        ft = make_filter_tube(cx=-3.4, y_top=1.9, y_bot=-1.9, half_w=0.62, wall_w=0.24, label_sites=False)
        ft.bands[0].stretch_to_fit_width(1.2).move_to([-3.4 - 0.62 - 0.24 - 0.6, 0.0, 0])
        ft.bands[1].stretch_to_fit_width(1.2).move_to([-3.4 + 0.62 + 0.24 + 0.6, 0.0, 0])
        self.add(ft)

        stream_t = ValueTracker(0.0)
        ys_path = [2.3, *ft.site_ys, -2.4]
        k_ions = VGroup(*[make_ion("K", radius=0.21) for _ in range(4)])

        def upd_stream(mob):
            p = stream_t.get_value() * 0.35
            for idx, ion in enumerate(mob):
                u = (p + idx / 4.0) % 1.0
                sf = u * (len(ys_path) - 1)
                k = min(int(sf), len(ys_path) - 2)
                f = sf - k
                sfm = 0.5 * (1 - np.cos(PI * np.clip((f - 0.15) / 0.7, 0, 1)))
                y = ys_path[k] * (1 - sfm) + ys_path[k + 1] * sfm
                ion.move_to([ft.cx, y, 0])
                ion.set_opacity(1.0 if -1.85 <= y <= 1.9 else float(np.clip((2.25 - abs(y)) / 0.35, 0.0, 1.0)))

        k_ions.add_updater(upd_stream)
        upd_stream(k_ions)

        bar_base = -1.6
        bar_max_h = 2.9
        k_bar = make_toll_bar_pair(1.1, bar_base, bar_max_h, toll_frac=K_TOLL_REL, pay_frac=0.93)
        na_bar = make_toll_bar_pair(4.2, bar_base, bar_max_h, toll_frac=NA_TOLL_REL, pay_frac=0.56)
        comp = make_size_bracket([2.0, 2.45, 0], [3.3, 2.45, 0], r_scale=1.0, show_bracket=True)
        comp.bracket.set_opacity(0.0)
        tag = scope_tag("schematic")
        self.add(k_ions, k_bar, na_bar, comp, tag)

        # Wait to "not sort ions" while K+ streams
        t_not = self.t_of("not sort ions") - 0.2
        if t_not > self.elapsed():
            self.play(stream_t.animate.set_value(t_not), run_time=t_not - self.elapsed(), rate_func=linear)

        # "does not sort ions by size" -> show bracket then fade it
        self.at("not sort ions")
        self.play(
            comp.bracket.animate.set_opacity(1.0),
            stream_t.animate.set_value(stream_t.get_value() + 1.1),
            run_time=1.1,
            rate_func=linear,
        )
        self.play(
            FadeOut(comp),
            stream_t.animate.set_value(stream_t.get_value() + 0.9),
            run_time=0.9,
            rate_func=linear,
        )

        # "It sorts them by how much of each toll it pays back."
        self.at("sorts them")
        lbl_k = T("K⁺: nearly repaid", 26, TEAL).move_to([1.3, bar_base - 0.48, 0])
        lbl_na = T("Na⁺: underpaid", 26, RED).move_to([4.6, bar_base - 0.48, 0])
        self.play(
            k_bar.animate.move_to([1.3, k_bar.get_center()[1], 0]),
            na_bar.animate.move_to([4.6, na_bar.get_center()[1], 0]),
            FadeIn(lbl_k),
            FadeIn(lbl_na),
            stream_t.animate.set_value(stream_t.get_value() + 1.4),
            run_time=1.4,
            rate_func=linear,
        )

        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(stream_t.animate.set_value(stream_t.get_value() + rem), run_time=rem, rate_func=linear)
        self.finish()


class S06HowExact(SpokenScene):
    def construct(self):
        ft, phase, t_na = add_small_left_filter(self, show_na_hover=True)
        P = make_exact_plot()
        tag = scope_tag("schematic")
        self.add(P, tag)

        # Keep small filter moving until "toll is about"
        t_70 = self.t_of("toll is about") - 0.2
        if t_70 > self.elapsed():
            dt = t_70 - self.elapsed()
            self.play(
                phase.animate.set_value(phase.get_value() + dt * 0.35),
                t_na.animate.set_value(t_na.get_value() + dt),
                run_time=dt,
                rate_func=linear,
            )

        # "Sodium's toll is about 70 kJ per mole larger than potassium's."
        self.at("toll is about")
        bar_val = ValueTracker(0.5)
        x_l, x_r = 0.55, 1.95

        def mk_red_bar():
            v = bar_val.get_value()
            p0 = P.pt(x_l, 0)
            p1 = P.pt(x_r, v)
            return Rectangle(
                width=p1[0] - p0[0], height=max(0.02, p1[1] - p0[1]),
                fill_color=RED, fill_opacity=0.82, stroke_color=RED, stroke_width=2.5,
            ).move_to([(p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0, 0])

        red_bar = always_redraw(mk_red_bar)
        val_lbl = always_redraw(lambda: M(f"{bar_val.get_value():.0f}", 28, RED).move_to(
            P.pt((x_l + x_r) / 2.0, bar_val.get_value()) + UP * 0.26
        ))
        self.add(red_bar, val_lbl)
        self.play(
            bar_val.animate.set_value(DELTA_TOLL),
            phase.animate.set_value(phase.get_value() + 2.2 * 0.35),
            t_na.animate.set_value(t_na.get_value() + 2.2),
            run_time=2.2,
            rate_func=linear,
        )
        top_lbl = T("extra toll: Na⁺", 26, RED).next_to(val_lbl, UP, buff=0.14)
        self.play(
            FadeIn(top_lbl),
            phase.animate.set_value(phase.get_value() + 0.6 * 0.35),
            t_na.animate.set_value(t_na.get_value() + 0.6),
            run_time=0.6,
            rate_func=linear,
        )

        # Wait until "preference needs"
        t_pref = self.t_of("preference needs") - 0.2
        if t_pref > self.elapsed():
            dt = t_pref - self.elapsed()
            self.play(
                phase.animate.set_value(phase.get_value() + dt * 0.35),
                t_na.animate.set_value(t_na.get_value() + dt),
                run_time=dt,
                rate_func=linear,
            )

        # "A thousand-fold preference needs a gap of only about 18."
        self.at("preference needs")
        p_bot = P.pt(x_r + 0.14, SLACK_PAYBACK)
        p_top = P.pt(x_r + 0.14, DELTA_TOLL)
        bracket = VGroup(
            Line(p_bot, p_top, color=TEXT, stroke_width=4),
            Line(p_bot + LEFT * 0.12, p_bot, color=TEXT, stroke_width=4),
            Line(p_top + LEFT * 0.12, p_top, color=TEXT, stroke_width=4),
        )
        gap_lbl = VGroup(
            T("about 18", 28, TEXT),
            T("needed for 1000:1", 24, TEXT),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(bracket, RIGHT, buff=0.18)
        self.play(
            Create(bracket),
            FadeIn(gap_lbl),
            phase.animate.set_value(phase.get_value() + 1.5 * 0.35),
            t_na.animate.set_value(t_na.get_value() + 1.5),
            run_time=1.5,
            rate_func=linear,
        )

        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(
            phase.animate.set_value(phase.get_value() + rem * 0.35),
            t_na.animate.set_value(t_na.get_value() + rem),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


class S07Slack(SpokenScene):
    def construct(self):
        ft, phase, t_na = add_small_left_filter(self, show_na_hover=True)
        P = make_exact_plot()
        x_l, x_r = 0.55, 1.95
        p0, p1 = P.pt(x_l, 0), P.pt(x_r, DELTA_TOLL)
        red_bar = Rectangle(
            width=p1[0] - p0[0], height=p1[1] - p0[1],
            fill_color=RED, fill_opacity=0.82, stroke_color=RED, stroke_width=2.5,
        ).move_to([(p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0, 0])
        val_lbl = M("70", 28, RED).move_to(P.pt((x_l + x_r) / 2.0, DELTA_TOLL) + UP * 0.26)
        top_lbl = T("extra toll: Na⁺", 26, RED).next_to(val_lbl, UP, buff=0.14)

        p_bot = P.pt(x_r + 0.14, SLACK_PAYBACK)
        p_top = P.pt(x_r + 0.14, DELTA_TOLL)
        bracket = VGroup(
            Line(p_bot, p_top, color=TEXT, stroke_width=4),
            Line(p_bot + LEFT * 0.12, p_bot, color=TEXT, stroke_width=4),
            Line(p_top + LEFT * 0.12, p_top, color=TEXT, stroke_width=4),
        )
        gap_lbl = VGroup(
            T("about 18", 28, TEXT),
            T("needed for 1000:1", 24, TEXT),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(bracket, RIGHT, buff=0.18)
        tag = scope_tag("schematic")

        self.add(P, red_bar, val_lbl, top_lbl, bracket, gap_lbl, tag)

        # Wait until "give sodium"
        t_give = self.t_of("give sodium") - 0.2
        if t_give > self.elapsed():
            dt = t_give - self.elapsed()
            self.play(
                phase.animate.set_value(phase.get_value() + dt * 0.35),
                t_na.animate.set_value(t_na.get_value() + dt),
                run_time=dt,
                rate_func=linear,
            )

        # "So the filter could even give sodium, about 52, more than potassium."
        self.at("give sodium")
        slack_val = ValueTracker(0.5)
        sx_l, sx_r = 0.60, 1.20

        def mk_slack():
            v = slack_val.get_value()
            q0, q1 = P.pt(sx_l, 0), P.pt(sx_r, v)
            return Rectangle(
                width=q1[0] - q0[0], height=max(0.02, q1[1] - q0[1]),
                fill_color=TEAL, fill_opacity=0.92, stroke_color=TEAL, stroke_width=2.0,
            ).move_to([(q0[0] + q1[0]) / 2.0, (q0[1] + q1[1]) / 2.0, 0])

        slack_bar = always_redraw(mk_slack)
        lbl_x = P.pt(x_r + 0.14, 0)[0] + 0.35
        slack_lbl = always_redraw(lambda: VGroup(
            M(f"about {slack_val.get_value():.0f}", 26, TEAL),
            T("extra payback allowed", 24, TEAL),
        ).arrange(DOWN, buff=0.10, aligned_edge=LEFT).move_to([lbl_x + 1.45, P.pt(0, 42)[1], 0]).align_to([lbl_x, 0, 0], LEFT))
        self.add(slack_bar, slack_lbl)
        self.play(
            slack_val.animate.set_value(SLACK_PAYBACK),
            phase.animate.set_value(phase.get_value() + 3.4 * 0.85),
            t_na.animate.set_value(t_na.get_value() + 3.4),
            run_time=3.4,
            rate_func=linear,
        )
        slack_line = DashedLine(P.pt(sx_r, SLACK_PAYBACK), P.pt(x_r + 0.10, SLACK_PAYBACK), color=TEAL, stroke_width=2.5)
        self.play(
            Create(slack_line),
            phase.animate.set_value(phase.get_value() + 0.9 * 0.85),
            t_na.animate.set_value(t_na.get_value() + 0.9),
            run_time=0.9,
            rate_func=linear,
        )

        # Wait until "simulations suggest"
        t_sim = self.t_of("simulations suggest") - 0.2
        if t_sim > self.elapsed():
            dt = t_sim - self.elapsed()
            self.play(
                phase.animate.set_value(phase.get_value() + dt * 0.85),
                t_na.animate.set_value(t_na.get_value() + dt),
                run_time=dt,
                rate_func=linear,
            )

        # "Simulations suggest the oxygens do give sodium more. Just not enough more."
        self.at("simulations suggest")
        sim_val = ValueTracker(0.5)
        gx_l, gx_r = 1.28, 1.88

        def mk_sim():
            v = sim_val.get_value()
            q0, q1 = P.pt(gx_l, 0), P.pt(gx_r, v)
            return Rectangle(
                width=q1[0] - q0[0], height=max(0.02, q1[1] - q0[1]),
                fill_color=TEAL, fill_opacity=0.45, stroke_color=TEXT, stroke_width=2.0,
            ).move_to([(q0[0] + q1[0]) / 2.0, (q0[1] + q1[1]) / 2.0, 0])

        sim_bar = always_redraw(mk_sim)
        self.add(sim_bar)
        self.play(
            sim_val.animate.set_value(35.0),  # unnumbered schematic height below 52
            phase.animate.set_value(phase.get_value() + 2.6 * 0.65),
            t_na.animate.set_value(t_na.get_value() + 2.6),
            run_time=2.6,
            rate_func=linear,
        )
        sim_lbl = VGroup(
            T("simulations", 24, TEXT),
            T("(schematic)", 24, GREY),
        ).arrange(DOWN, buff=0.10, aligned_edge=LEFT).move_to([lbl_x + 0.9, P.pt(0, 14)[1], 0]).align_to([lbl_x, 0, 0], LEFT)
        sim_ptr = Arrow(sim_lbl.get_left() + LEFT * 0.08, P.pt(gx_r + 0.04, 14), buff=0.04, color=TEXT, stroke_width=3,
                        max_tip_length_to_length_ratio=0.18)
        self.play(
            FadeIn(sim_lbl),
            Create(sim_ptr),
            phase.animate.set_value(phase.get_value() + 0.8 * 0.65),
            t_na.animate.set_value(t_na.get_value() + 0.8),
            run_time=0.8,
            rate_func=linear,
        )

        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(
            phase.animate.set_value(phase.get_value() + rem * 0.65),
            t_na.animate.set_value(t_na.get_value() + rem),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


def build_s08_s09_world():
    """Shared builder so S08Predict's end frame matches S09Pause's start frame identically."""
    ft = make_filter_tube(cx=-2.3, y_top=2.65, y_bot=-2.05, half_w=0.78, wall_w=0.28, label_sites=True, right_band_w=0.80)
    s2_y = ft.site_ys[1]
    ft.rings[1].set_opacity(0.0)
    k_r = 0.34
    s2_snug = VGroup(*[
        Dot([ft.cx + (k_r + 0.11) * np.cos(k * TAU / 8.0 + PI / 8.0),
             s2_y + 0.16 * np.sin(k * TAU / 8.0 + PI / 8.0), 0], radius=0.085, color=BLUE)
        for k in range(8)
    ])
    held_glow = Circle(radius=0.52, color=TEAL, stroke_width=5).set_opacity(0.75).move_to([ft.cx, s2_y, 0])
    held_lbl = T("held", 26, TEAL).move_to([0.20, s2_y, 0])
    k_held = make_ion("K", radius=k_r).move_to([ft.cx, s2_y, 0])
    k_wait = make_ion("K", radius=k_r).move_to([ft.cx, ft.y_top + 0.45, 0])
    tag = scope_tag("schematic")
    return ft, s2_snug, held_glow, held_lbl, k_held, k_wait, tag


class S08Predict(SpokenScene):
    def construct(self):
        ft, s2_snug, held_glow, held_lbl, k_held, k_wait, tag = build_s08_s09_world()
        s2_y = ft.site_ys[1]
        # Start slightly smaller to match growth back from left-side view
        ft_init = ft.copy().scale(0.65).move_to([-4.0, 0.2, 0])
        self.add(ft_init, tag)
        self.play(Transform(ft_init, ft), run_time=1.3)
        self.remove(ft_init)

        # K+ descends into S2 and oxygens close snugly while held ring forms
        k_start = k_held.copy().move_to([ft.cx, ft.y_top + 0.4, 0])
        self.add(ft, s2_snug, k_start)
        self.play(
            k_start.animate.move_to([ft.cx, s2_y, 0]),
            FadeIn(held_glow),
            FadeIn(held_lbl),
            run_time=2.5,
        )
        self.remove(k_start)
        self.add(k_held)

        # "Yet around 100 million potassium ions can cross each second."
        self.at("around 100 million")
        rate = ValueTracker(0.0)
        flow_hdr = T("observed flow:", 26, GREY).move_to([2.4, 0.75, 0]).align_to([1.25, 0, 0], LEFT)
        flow_num = always_redraw(lambda: M(f"about {rate.get_value():,.0f} per s", 28, VIOLET).next_to(
            flow_hdr, DOWN, buff=0.14, aligned_edge=LEFT
        ))
        flow_bar_bg = Rectangle(width=4.2, height=0.22, color=GREY, stroke_width=2, fill_opacity=0.15).next_to(
            flow_hdr, DOWN, buff=0.72, aligned_edge=LEFT
        )
        flow_bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.04, 4.2 * (rate.get_value() / 100_000_000.0)), height=0.22,
            fill_color=VIOLET, fill_opacity=0.88, stroke_width=0,
        ).align_to(flow_bar_bg, LEFT).match_y(flow_bar_bg))
        self.add(flow_hdr, flow_num, flow_bar_bg, flow_bar_fill)
        self.play(rate.animate.set_value(100_000_000.0), run_time=4.5, rate_func=linear)

        # "What lets a tightly held ion leave?"
        self.at("what lets")
        k_wait_start = k_wait.copy().shift(UP * 0.7).set_opacity(0.0)
        self.add(k_wait_start)
        q = question_card("What lets a tightly held ion leave?")
        self.play(
            Transform(k_wait_start, k_wait),
            FadeIn(q.question),
            run_time=1.1,
        )
        self.remove(k_wait_start)
        self.add(k_wait)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "What lets a tightly held ion leave?"
    SECONDS = 4.5
    RING_AT = (5.8, -1.9, 0)

    def backdrop(self):
        ft, s2_snug, held_glow, held_lbl, k_held, k_wait, tag = build_s08_s09_world()
        flow_hdr = T("observed flow:", 26, GREY).move_to([2.4, 0.75, 0]).align_to([1.25, 0, 0], LEFT)
        flow_num = M("about 100,000,000 per s", 28, VIOLET).next_to(flow_hdr, DOWN, buff=0.14, aligned_edge=LEFT)
        flow_bar_bg = Rectangle(width=4.2, height=0.22, color=GREY, stroke_width=2, fill_opacity=0.15).next_to(
            flow_hdr, DOWN, buff=0.72, aligned_edge=LEFT
        )
        flow_bar_fill = Rectangle(
            width=4.2, height=0.22, fill_color=VIOLET, fill_opacity=0.88, stroke_width=0,
        ).align_to(flow_bar_bg, LEFT).match_y(flow_bar_bg)
        # Subtle held-well jiggle inside S2 during predict pause
        base = k_held.get_center().copy()
        k_held.add_updater(lambda m, dt: (
            setattr(m, "_jt", getattr(m, "_jt", 0.0) + dt),
            m.move_to(base + UP * 0.04 * np.sin(5.0 * m._jt)),
        ))
        return VGroup(ft, s2_snug, held_glow, held_lbl, k_held, k_wait, flow_hdr, flow_num, flow_bar_bg, flow_bar_fill, tag)


def build_knock_on_filter(cx=-2.0, y_top=2.4, y_bot=-2.2, half_w=0.78, wall_w=0.28, label_sites=True):
    ft = make_filter_tube(cx=cx, y_top=y_top, y_bot=y_bot, half_w=half_w, wall_w=wall_w, label_sites=label_sites)
    return ft


def run_knock_on_cycle(ft, cycle_t, n_ions=4):
    """Return an updater-driven VGroup of K+ ions running the continuous knock-on step cycle."""
    # Cycle: 3 ions occupy S2, S3, S4 and 1 approaches S1 -> all shift down 1 site, bottom exits
    k_r = 0.28 * ((ft.y_top - ft.y_bot) / 4.6)
    s_ys = ft.site_ys
    dy_step = s_ys[0] - s_ys[1]
    ions = VGroup(*[make_ion("K", radius=k_r) for _ in range(n_ions + 1)])

    def upd(mob):
        # f in [0, 1) is one knock-on step: each ion moves down by 1 site index
        p = cycle_t.get_value() % 1.0
        # Smooth push step in middle of cycle: slow approach then crisp push
        step = 0.5 * (1 - np.cos(PI * np.clip((p - 0.15) / 0.65, 0.0, 1.0)))
        for idx, ion in enumerate(mob):
            # idx 0..4 correspond to positions: above S1 (0), S1 (1), S2 (2), S3 (3), S4 (4)
            pos_idx = idx + step
            if pos_idx < 1.0:
                y = (ft.y_top + 0.55) * (1 - pos_idx) + s_ys[0] * pos_idx
                op = min(1.0, 0.4 + 0.6 * pos_idx)
            elif pos_idx <= 4.0:
                k = min(int(pos_idx) - 1, 2)
                frac = pos_idx - (k + 1)
                y = s_ys[k] * (1 - frac) + s_ys[k + 1] * frac
                op = 1.0
            else:
                frac = pos_idx - 4.0
                y = s_ys[3] * (1 - frac) + (ft.y_bot - 0.65) * frac
                op = max(0.0, 1.0 - frac * 1.1)
            ion.move_to([ft.cx, y, 0])
            ion.set_opacity(op)

    ions.add_updater(upd)
    upd(ions)
    return ions


class S10KnockOn(SpokenScene):
    def construct(self):
        ft = build_knock_on_filter(cx=-2.2, y_top=2.4, y_bot=-2.2, half_w=0.78, wall_w=0.28, label_sites=True)
        k_r = 0.28
        # Held K+ in S2, waiting K+ above S1; S3 and S4 ions slide in on crowding cue
        k_wait = make_ion("K", radius=k_r).move_to([ft.cx, ft.y_top + 0.55, 0])
        k_s2 = make_ion("K", radius=k_r).move_to([ft.cx, ft.site_ys[1], 0])
        k_s3 = make_ion("K", radius=k_r).move_to([ft.cx, ft.y_bot - 0.45, 0]).set_opacity(0.0)
        k_s4 = make_ion("K", radius=k_r).move_to([ft.cx, ft.y_bot - 0.55, 0]).set_opacity(0.0)
        tag = scope_tag("schematic")
        self.add(ft, k_wait, k_s2, k_s3, k_s4, tag)

        # "The answer is probably crowding. Several potassium ions sit in the filter at once,"
        self.at("answer is probably")
        crowd_lbl = T("crowding in the filter", 28, VIOLET).move_to([2.6, 1.5, 0]).align_to([0.9, 0, 0], LEFT)
        k_s3.move_to([ft.cx, ft.site_ys[2] + 0.28, 0]).set_opacity(0.0)
        k_s4.move_to([ft.cx, ft.site_ys[3] + 0.28, 0]).set_opacity(0.0)
        self.play(
            FadeIn(crowd_lbl),
            k_s3.animate.move_to([ft.cx, ft.site_ys[2], 0]).set_opacity(1.0),
            k_s4.animate.move_to([ft.cx, ft.site_ys[3], 0]).set_opacity(1.0),
            run_time=2.2,
        )
        self.play(k_wait.animate.move_to([ft.cx, ft.y_top + 0.22, 0]), run_time=2.6)

        # "and like charges repel."
        self.at("like charges repel")
        arrows = VGroup(
            Arrow([ft.cx, ft.site_ys[1] - 0.30, 0], [ft.cx, ft.site_ys[1] - 0.50, 0], buff=0, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.4),
            Arrow([ft.cx, ft.site_ys[2] + 0.30, 0], [ft.cx, ft.site_ys[2] + 0.50, 0], buff=0, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.4),
            Arrow([ft.cx, ft.site_ys[2] - 0.30, 0], [ft.cx, ft.site_ys[2] - 0.50, 0], buff=0, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.4),
            Arrow([ft.cx, ft.site_ys[3] + 0.30, 0], [ft.cx, ft.site_ys[3] + 0.50, 0], buff=0, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.4),
        )
        repel_lbl = T("like charges repel", 28, RED).move_to([2.6, 0.55, 0]).align_to([0.9, 0, 0], LEFT)
        self.play(FadeIn(arrows), FadeIn(repel_lbl), run_time=0.9)
        self.play(
            k_s2.animate.shift(UP * 0.14),
            k_s4.animate.shift(DOWN * 0.14),
            run_time=1.4,
            rate_func=there_and_back,
        )

        # "When another ion enters, that repulsion lowers the barrier for the leading ion to leave."
        self.at("another ion enters")
        self.remove(k_wait, k_s2, k_s3, k_s4, arrows)
        cycle_t = ValueTracker(0.0)
        stream = run_knock_on_cycle(ft, cycle_t, n_ions=4)
        # Repulsion arrows pulse on the push phase
        dyn_arrows = always_redraw(lambda: VGroup(*[
            Arrow([ft.cx, y - 0.30, 0], [ft.cx, y - 0.52, 0], buff=0, color=RED, stroke_width=4.5, max_tip_length_to_length_ratio=0.4)
            for y in ft.site_ys[:3]
        ]).set_opacity(0.45 + 0.55 * np.sin(PI * np.clip(((cycle_t.get_value() % 1.0) - 0.15) / 0.65, 0, 1))))
        self.add(stream, dyn_arrows)

        t_knock = self.t_of("the knock") - 0.2
        dt1 = max(1.0, t_knock - self.elapsed())
        self.play(cycle_t.animate.set_value(dt1 * 0.55), run_time=dt1, rate_func=linear)

        # "This is the knock-on mechanism."
        self.at("the knock")
        ko_lbl = T("knock-on", 32, GOLD).move_to([2.6, -0.55, 0]).align_to([0.9, 0, 0], LEFT)
        self.play(
            FadeIn(ko_lbl),
            cycle_t.animate.set_value(cycle_t.get_value() + 1.0 * 0.55),
            run_time=1.0,
            rate_func=linear,
        )
        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(cycle_t.animate.set_value(cycle_t.get_value() + rem * 0.55), run_time=rem, rate_func=linear)
        self.finish()


class S11Hedges(SpokenScene):
    def construct(self):
        ft = build_knock_on_filter(cx=-3.3, y_top=2.4, y_bot=-2.2, half_w=0.72, wall_w=0.26, label_sites=True)
        cycle_t = ValueTracker(0.0)
        stream = run_knock_on_cycle(ft, cycle_t, n_ions=4)
        tag = scope_tag("schematic")
        self.add(ft, stream, tag)

        # "A Newton's cradle is a fair image, but only an image."
        self.at("cradle")
        cradle_top = np.array([2.6, 2.55, 0])
        bar = Line(cradle_top + LEFT * 1.15, cradle_top + RIGHT * 1.15, color=GREY, stroke_width=4)
        L_len = 1.05
        BALL_RAD = 0.14
        xs_mid = [-0.28, 0.0, 0.28]
        mid_balls = VGroup(*[
            VGroup(
                Line([cradle_top[0] + dx, cradle_top[1], 0], [cradle_top[0] + dx, cradle_top[1] - L_len, 0], color=GREY, stroke_width=2),
                Circle(radius=BALL_RAD, color=GREY, fill_color=GREY, fill_opacity=0.85).move_to([cradle_top[0] + dx, cradle_top[1] - L_len, 0]),
            )
            for dx in xs_mid
        ])
        ang_l = ValueTracker(-0.45)
        ang_r = ValueTracker(0.0)

        def mk_ball(piv_x, ang_tr):
            piv = np.array([cradle_top[0] + piv_x, cradle_top[1], 0])
            a = ang_tr.get_value()
            pos = piv + L_len * np.array([np.sin(a), -np.cos(a), 0])
            return VGroup(
                Line(piv, pos, color=GREY, stroke_width=2),
                Circle(radius=BALL_RAD, color=GREY, fill_color=GREY, fill_opacity=0.85).move_to(pos),
            )

        ball_l = always_redraw(lambda: mk_ball(-0.56, ang_l))
        ball_r = always_redraw(lambda: mk_ball(0.56, ang_r))
        cradle = VGroup(bar, mid_balls, ball_l, ball_r)
        self.add(cradle)

        self.play(
            ang_l.animate.set_value(0.0),
            cycle_t.animate.set_value(cycle_t.get_value() + 0.7 * 0.55),
            run_time=0.7,
            rate_func=linear,
        )
        self.play(
            ang_r.animate.set_value(0.45),
            cycle_t.animate.set_value(cycle_t.get_value() + 0.7 * 0.55),
            run_time=0.7,
            rate_func=linear,
        )

        # "only an image" -> white X across the swinging ball + tag "image only"
        self.at("only an")
        p_ball = cradle_top + np.array([0.56, 0, 0]) + L_len * np.array([np.sin(0.45), -np.cos(0.45), 0])
        x_mark = VGroup(
            Line(p_ball + np.array([-0.2, -0.2, 0]), p_ball + np.array([0.2, 0.2, 0]), color=TEXT, stroke_width=4.5),
            Line(p_ball + np.array([-0.2, 0.2, 0]), p_ball + np.array([0.2, -0.2, 0]), color=TEXT, stroke_width=4.5),
        )
        img_lbl = T("image only", 26, TEXT).move_to([2.6, 0.95, 0])
        self.play(
            Create(x_mark),
            FadeIn(img_lbl),
            cycle_t.animate.set_value(cycle_t.get_value() + 1.0 * 0.55),
            run_time=1.0,
            rate_func=linear,
        )

        t_water = self.t_of("water molecules separate") - 0.2
        if t_water > self.elapsed():
            dt = t_water - self.elapsed()
            self.play(cycle_t.animate.set_value(cycle_t.get_value() + dt * 0.55), run_time=dt, rate_func=linear)

        # "Whether water molecules separate the ions is still argued,"
        self.at("water molecules separate")
        y_w = -0.35
        k1_w = make_ion("K", radius=0.24).move_to([0.15, y_w, 0])
        h2o = Dot([0.70, y_w, 0], radius=0.13, color=BLUE)
        k2_w = make_ion("K", radius=0.24).move_to([1.25, y_w, 0])
        w_gfx = VGroup(k1_w, h2o, k2_w)
        w_lbl = T("still argued", 26, BLUE).move_to([3.0, y_w, 0]).align_to([1.85, 0, 0], LEFT)
        self.play(
            FadeIn(w_gfx),
            FadeIn(w_lbl),
            cycle_t.animate.set_value(cycle_t.get_value() + 1.6 * 0.55),
            run_time=1.6,
            rate_func=linear,
        )

        # "though recent evidence favours direct contact."
        self.at("recent evidence")
        y_c = -1.75
        k1_c = make_ion("K", radius=0.24).move_to([0.46, y_c, 0])
        k2_c = make_ion("K", radius=0.24).move_to([0.94, y_c, 0])
        c_gfx = VGroup(k1_c, k2_c)
        c_lbl = T("recent evidence: contact", 26, VIOLET).move_to([3.6, y_c, 0]).align_to([1.85, 0, 0], LEFT)
        self.play(
            w_gfx.animate.set_opacity(0.45),
            FadeIn(c_gfx),
            FadeIn(c_lbl),
            cycle_t.animate.set_value(cycle_t.get_value() + 1.4 * 0.55),
            run_time=1.4,
            rate_func=linear,
        )

        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(cycle_t.animate.set_value(cycle_t.get_value() + rem * 0.55), run_time=rem, rate_func=linear)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        # Opening composition: carried bilayer, tall teal K+ channel, knock-on K+ stream
        bilayer = make_bilayer(pore_half_w=0.48, y_mid=0.0, core_h=2.7, x_lim=6.1)
        walls, _, _ = make_channel_walls(cx=0.0, y_mid=0.0, half_w=0.38, wall_w=0.26, height=3.8)
        grip_dots = VGroup(
            *[Dot([-0.26, y, 0], radius=0.06, color=BLUE) for y in (-1.0, -0.33, 0.33, 1.0)],
            *[Dot([0.26, y, 0], radius=0.06, color=BLUE) for y in (-1.0, -0.33, 0.33, 1.0)],
        )
        ch_lbl = T("potassium channel", 28, TEAL).move_to([0.0, 2.85, 0])
        comp = make_size_bracket([-4.4, 2.15, 0], [-3.2, 2.15, 0], r_scale=1.0, show_bracket=True)
        tag = scope_tag("schematic")
        self.add(bilayer, walls, grip_dots, ch_lbl, comp, tag)

        stream_t = ValueTracker(0.0)
        k_ions = VGroup(*[make_ion("K", radius=0.22) for _ in range(4)])

        def upd_stream(mob):
            t = stream_t.get_value() * 0.45
            for idx, ion in enumerate(mob):
                u = (t + idx / 4.0) % 1.0
                y = 2.55 - u * 5.1
                ion.move_to([0.0, y, 0])
                op = 1.0
                if y > 2.15:
                    op = max(0.0, (2.55 - y) / 0.4)
                elif y < -2.15:
                    op = max(0.0, (y + 2.55) / 0.4)
                ion.set_opacity(op)

        k_ions.add_updater(upd_stream)
        upd_stream(k_ions)
        self.add(k_ions)

        # Wait to "almost its whole"
        t_whole = self.t_of("almost its whole") - 0.2
        if t_whole > self.elapsed():
            dt = t_whole - self.elapsed()
            self.play(stream_t.animate.set_value(stream_t.get_value() + dt), run_time=dt, rate_func=linear)

        # "hands potassium back almost its whole toll"
        self.at("almost its whole")
        bar_base = -0.74
        bar_max_h = 1.52
        k_bar = make_toll_bar_pair(2.7, bar_base, bar_max_h, toll_frac=K_TOLL_REL, pay_frac=0.93,
                                   label_text="K⁺", label_col=VIOLET)
        self.play(
            FadeIn(k_bar),
            stream_t.animate.set_value(stream_t.get_value() + 1.0),
            run_time=1.0,
            rate_func=linear,
        )

        # "and sodium too little"
        self.at("sodium too little")
        na_bar = make_toll_bar_pair(4.5, bar_base, bar_max_h, toll_frac=NA_TOLL_REL, pay_frac=0.56,
                                   label_text="Na⁺", label_col=YELLOW)
        na_bounce = make_ion("Na", radius=NA_RADIUS).move_to([0.95, 2.35, 0])
        self.add(na_bounce)
        self.play(
            FadeIn(na_bar),
            na_bounce.animate.move_to([0.0, 2.02, 0]),
            stream_t.animate.set_value(stream_t.get_value() + 1.1),
            run_time=1.1,
            rate_func=linear,
        )
        self.play(
            na_bounce.animate.move_to([-1.05, 2.45, 0]),
            stream_t.animate.set_value(stream_t.get_value() + 1.1),
            run_time=1.1,
            rate_func=linear,
        )

        t_size = self.t_of("size never decided") - 0.2
        if t_size > self.elapsed():
            dt = t_size - self.elapsed()
            self.play(stream_t.animate.set_value(stream_t.get_value() + dt), run_time=dt, rate_func=linear)

        # "Size never decided it." -> size bracket fades out for good
        self.at("size never decided")
        self.play(
            FadeOut(comp.bracket),
            stream_t.animate.set_value(stream_t.get_value() + 0.9),
            run_time=0.9,
            rate_func=linear,
        )

        # "The payback did." -> both TEAL bars highlight
        self.at("the payback did")
        hl_k = SurroundingRectangle(k_bar.teal_bar, color=GOLD, buff=0.04, stroke_width=3.5)
        hl_na = SurroundingRectangle(na_bar.teal_bar, color=GOLD, buff=0.04, stroke_width=3.5)
        self.play(
            FadeIn(hl_k),
            FadeIn(hl_na),
            stream_t.animate.set_value(stream_t.get_value() + 0.6),
            run_time=0.6,
            rate_func=linear,
        )

        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(stream_t.animate.set_value(stream_t.get_value() + rem), run_time=rem, rate_func=linear)
        self.finish()


class S13End(EndCard):
    LINE = "A potassium channel selects by repaying the toll, not by size."
