"""
The Messenger Level: Made and Erased (camp-and-pka)

COLOUR MAP (one colour per concept across the whole film):
- YELLOW (#F5D547): Adrenaline (outer / first messenger)
- GOLD   (#D4A843): cAMP (inner / second messenger, cAMP level gauge, computed curves)
- BLUE   (#58C4DD): Synthesis machinery & arrows (adenylyl cyclase, synthesis rate)
- GREEN  (#83C167): Gs (stimulatory G protein)
- PURPLE (#A888E0): Gi (inhibitory G protein)
- RED    (#FC6255): Breakdown machinery & arrows (phosphodiesterase, removal rate)
- AMP_MUTED (#B57C7C): 5'-AMP (opened, inactive breakdown product)
- TEAL   (#3FB8C0): Intracellular effectors (unnamed until handoff)
- GREY   (#8B93A1): Plasma membrane, receptor scaffold, plot axes, reference lines
- TEXT   (#E8EAF0): Subject and plot labels (full opacity, >= 28 pt; 24 pt floor for scope_tag)

ONE CARRIED PICTURE OF THE WORLD:
A cross-section of a liver cell with extracellular space in the upper third, a thick GREY
plasma membrane spanning horizontally across the upper-middle, and the cytosol filling the
lower two-thirds, with a vertical GOLD cAMP-level gauge at the right that transforms into
the computed first-order concentration plot and back again.

WHAT CHANGES IN EACH SPOKEN SCENE (and what computes it):
- s00_hook: Adrenaline drifts down to the membrane receptor and stops at the membrane while
  6 GOLD inner-signal tokens emerge below and diffuse down a fixed-seed random walk (rng=7).
- s02_relay: Receptor tail pivots on activation, GREEN Gs slides laterally to BLUE cyclase,
  and ATP chips enter cyclase and transform into GOLD cAMP tokens drifting into cytosol.
- s03_second_messenger: Cyclase emits 18 GOLD tokens on random-walk trajectories (rng=11),
  incrementing a shared ValueTracker that raises the right-side GOLD gauge and lights effectors.
- s03_amplification: Three cyclase bursts add tokens (10 -> 30) tracked by one counter and
  the rising GOLD gauge, followed by a location reticle and a turning lifetime clock ring.
- s04_source_and_sink: GOLD gauge climbs toward 0.96, RED phosphodiesterase rises, tokens
  enter it and transform into muted 5'-AMP chips, and the gauge retreats to 0.35.
- s05_balance_curve: Gauge transforms into a Plot; a ValueTracker sweeps C(t)=2.5+(1.1-2.5)e^(-4t)
  while a RED breakdown arrow thickens proportionally to C(t) until it matches BLUE synthesis.
- s06_predict: Original plateau holds dashed at C=2.5, RED removal arrow widens to 2x BLUE width
  while flux chevrons move along both arrows, and the two-choice question appears above.
- s08_reveal: 'below' fills RED; ValueTracker sweeps C(t)=1.25+(2.5-1.25)e^(-8t) down to the
  lower plateau while RED arrow width narrows from 2x back to 1x to match BLUE synthesis.
- s09_control: Plot returns to membrane world; Gs pushes a synthesis slider up, Gi pulls a
  separate 'some cyclase forms' slider down, while PDE steadily converts cAMP to 5'-AMP.
- s09_signal_end: Adrenaline floats off, Gs swaps GTP->GDP and fades, synthesis thins to
  resting rate, and two computed returns C(t)=0.5+2.0e^(-kt) (k=4, k=8) fall to resting level.
- s10_handoff: GOLD gauge rises to moderate level while a clock ring turns; GOLD tokens walk to
  three TEAL effectors whose outputs remain '?', zooming toward one unlabelled TEAL effector.
"""

from bp_parts import *
import numpy as np

# Concept colours (in addition to bp_style imports)
PURPLE = "#A888E0"
AMP_MUTED = "#B57C7C"
MEMBRANE_Y = 1.45
MEMBRANE_H = 0.44

# Lesson kinetic parameters (from lesson_for_context.mdx):
# Resting synthesis = 2 uM/s, stimulated synthesis = 10 uM/s
# Baseline PDE k = 4 /s, stronger PDE k = 8 /s
V_REST = 2.0
V_STIM = 10.0
K_BASE = 4.0
K_FAST = 8.0
C_REST = V_REST / K_BASE   # 0.5
C_PLAT = V_STIM / K_BASE   # 2.5
C_LOW = V_STIM / K_FAST    # 1.25
C_S04_END = 1.1            # gauge level 0.344 of yr=(0, 3.2) carried from s04 into s05


def c_rise(t):
    """First-order rise from s04 end level to stimulated plateau."""
    return C_PLAT + (C_S04_END - C_PLAT) * np.exp(-K_BASE * t)


def c_drop_fast(t):
    """First-order drop from old plateau when PDE doubles (s08_reveal)."""
    return C_LOW + (C_PLAT - C_LOW) * np.exp(-K_FAST * t)


def c_return(t, k=K_BASE):
    """First-order return from stimulated plateau toward resting level (s09_signal_end)."""
    return C_REST + (C_PLAT - C_REST) * np.exp(-k * t)


def make_membrane(y=MEMBRANE_Y, h=MEMBRANE_H, width=14.2):
    """Horizontal plasma membrane spanning full width."""
    band = Rectangle(width=width, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to([0, y, 0])
    top_line = Line([-width / 2, y + h / 2, 0], [width / 2, y + h / 2, 0], color=GREY, stroke_width=3.5)
    bot_line = Line([-width / 2, y - h / 2, 0], [width / 2, y - h / 2, 0], color=GREY, stroke_width=3.5)
    return VGroup(band, top_line, bot_line)


def make_receptor(x=-3.8, y=MEMBRANE_Y, scale=1.0):
    """Schematic membrane receptor with extracellular pocket and pivoting cytosolic tail."""
    body = RoundedRectangle(
        corner_radius=0.14 * scale, width=0.72 * scale, height=0.88 * scale,
        stroke_color=GREY, stroke_width=3.0, fill_color=GREY, fill_opacity=0.22,
    ).move_to([x, y, 0])
    # Cup rim on extracellular side
    cup = Arc(
        radius=0.34 * scale, start_angle=PI, angle=PI,
        arc_center=[x, y + 0.44 * scale, 0], color=TEXT, stroke_width=3.5,
    )
    tail_top = np.array([x, y - 0.44 * scale, 0])
    tail_bot = np.array([x, y - 0.92 * scale, 0])
    tail = Line(tail_top, tail_bot, color=GREY, stroke_width=6.0 * scale)
    g = VGroup(body, cup, tail)
    g.body, g.cup, g.tail, g.pivot = body, cup, tail, tail_top
    return g


def make_cyclase(x=-1.1, y=MEMBRANE_Y, scale=1.0, label=True, mem_h=MEMBRANE_H):
    """Schematic BLUE adenylyl cyclase embedded in membrane with cytosolic catalytic lobe."""
    tm = RoundedRectangle(
        corner_radius=0.14 * scale, width=1.18 * scale, height=mem_h + 0.18 * scale,
        stroke_color=BLUE, stroke_width=3.0, fill_color=BLUE, fill_opacity=0.22,
    ).move_to([x, y, 0])
    lab = T("adenylyl\ncyclase", size=max(26, int(28 * scale)), color=BLUE, line_spacing=0.85)
    lobe_w = max(1.80 * scale, lab.width + 0.44)
    lobe_h = max(0.84 * scale, lab.height + 0.34)
    lobe = RoundedRectangle(
        corner_radius=0.18 * scale, width=lobe_w, height=lobe_h,
        stroke_color=BLUE, stroke_width=3.0, fill_color=BLUE, fill_opacity=0.25,
    ).next_to(tm, DOWN, buff=0.05)
    g = VGroup(tm, lobe)
    if label:
        lab.move_to(lobe)
        g.add(lab)
        g.label = lab
    g.tm, g.lobe = tm, lobe
    return g


def make_adrenaline(pos=(-5.3, 2.75, 0), radius=0.28, label_text="adrenaline"):
    """YELLOW adrenaline circle with non-overlapping label placed above/right."""
    dot = Circle(radius=radius, color=YELLOW, stroke_width=3.0, fill_color=YELLOW, fill_opacity=0.88).move_to(pos)
    if label_text:
        lab = T(label_text, size=28, color=YELLOW)
        lab.next_to(dot, RIGHT, buff=0.18)
        g = VGroup(dot, lab)
        g.dot, g.label = dot, lab
    else:
        g = VGroup(dot)
        g.dot, g.label = dot, None
    return g


def make_camp_token(pos=(0, 0, 0), radius=0.14, labelled=False):
    """GOLD cAMP token."""
    d = Circle(radius=radius, color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.9)
    d.move_to(pos)
    if labelled:
        t = T("cAMP", size=28, color=GOLD).next_to(d, RIGHT, buff=0.14)
        return VGroup(d, t)
    return d


def make_pde(pos=(1.6, -1.0, 0), w=2.35, h=1.25):
    """Large RED phosphodiesterase block with left-side intake notch."""
    lab = T("phospho-\ndiesterase", size=26, color=RED, line_spacing=0.85)
    box_w = max(w, lab.width + 0.72)
    box_h = max(h, lab.height + 0.36)
    box = RoundedRectangle(
        corner_radius=0.18, width=box_w, height=box_h,
        stroke_color=RED, stroke_width=3.2, fill_color=RED, fill_opacity=0.22,
    ).move_to(pos)
    lab.move_to(box.get_center() + RIGHT * 0.16)
    intake = Arc(
        radius=0.18, start_angle=-PI / 2, angle=PI,
        arc_center=box.get_left() + RIGHT * 0.02, color=RED, stroke_width=3.5,
    )
    g = VGroup(box, intake, lab)
    g.box, g.lab = box, lab
    return g


def make_effector(pos=(-3.6, -2.1, 0), glow=0.25, show_q=True):
    """Unnamed TEAL effector block with an internal activity bar and '?' output."""
    box = RoundedRectangle(
        corner_radius=0.16, width=1.6, height=0.82,
        stroke_color=TEAL, stroke_width=2.8, fill_color=TEAL, fill_opacity=glow * 0.45,
    ).move_to(pos)
    bar_bg = RoundedRectangle(
        corner_radius=0.06, width=1.1, height=0.16,
        stroke_color=TEAL, stroke_width=1.5, fill_color=BG, fill_opacity=0.8,
    ).move_to([pos[0], pos[1] - 0.14, 0])
    bar_fill = RoundedRectangle(
        corner_radius=0.05, width=max(0.12, 1.04 * glow), height=0.12,
        stroke_width=0, fill_color=TEAL, fill_opacity=min(1.0, 0.35 + glow * 0.65),
    ).align_to(bar_bg, LEFT).shift(RIGHT * 0.03)
    bar_fill.set_y(bar_bg.get_y())
    title = T("effector", size=24, color=TEAL).move_to([pos[0], pos[1] + 0.16, 0])
    g = VGroup(box, bar_bg, bar_fill, title)
    if show_q:
        arr = Arrow(box.get_right() + RIGHT * 0.04, box.get_right() + RIGHT * 0.55,
                    buff=0, color=TEAL, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        q = T("?", size=30, color=GOLD, weight=BOLD).next_to(arr, RIGHT, buff=0.1)
        g.add(arr, q)
        g.q = q
    g.box, g.bar_fill = box, bar_fill
    return g


def make_gauge(tracker, center=(5.1, -0.6, 0), height=3.0, width=0.62, label="cAMP level"):
    """Vertical GOLD cAMP level gauge driven directly by a 0..1 ValueTracker."""
    cx, cy = center[0], center[1]
    frame = RoundedRectangle(
        corner_radius=0.1, width=width, height=height,
        stroke_color=GOLD, stroke_width=3.0, fill_color=BG, fill_opacity=0.85,
    ).move_to([cx, cy, 0])
    bot_y = cy - height / 2 + 0.05
    max_fill_h = height - 0.10

    def mk_fill():
        frac = float(np.clip(tracker.get_value(), 0.02, 1.0))
        fh = max(0.08, frac * max_fill_h)
        r = RoundedRectangle(
            corner_radius=0.06, width=width - 0.10, height=fh,
            stroke_width=0, fill_color=GOLD, fill_opacity=0.82,
        )
        r.move_to([cx, bot_y + fh / 2, 0])
        return r

    fill = always_redraw(mk_fill)
    lab = T(label, size=28, color=GOLD).next_to(frame, UP, buff=0.22)
    if lab.get_right()[0] > 6.35:
        lab.align_to([6.3, 0, 0], RIGHT)
    g = VGroup(frame, fill, lab)
    g.frame, g.fill, g.label = frame, fill, lab
    return g


def make_clock_ring(tracker, center=(2.2, -1.3, 0), radius=0.45, color=GOLD, label=None):
    """Circular lifetime clock driven by tracker (0..1 turns)."""
    c = np.array(center, dtype=float)
    rim = Circle(radius=radius, color=color, stroke_width=3.5).move_to(c)
    hand = always_redraw(lambda: Line(
        c,
        c + 0.72 * radius * np.array([
            np.sin(TAU * tracker.get_value()),
            np.cos(TAU * tracker.get_value()),
            0.0,
        ]),
        color=TEXT, stroke_width=3.5,
    ))
    dot = Dot(c, radius=0.05, color=color)
    g = VGroup(rim, hand, dot)
    if label:
        t = T(label, size=26, color=color).next_to(rim, DOWN, buff=0.14)
        g.add(t)
    return g


def make_thick_arrow(start, end, thickness_fn, color, label=None, label_dir=UP, label_size=28):
    """Variable-thickness horizontal rate arrow driven by thickness_fn()."""
    p0 = np.array(start, dtype=float)
    p1 = np.array(end, dtype=float)
    dx = p1[0] - p0[0]
    sgn = 1.0 if dx >= 0 else -1.0
    length = abs(dx)

    def mk():
        w = float(np.clip(thickness_fn(), 0.08, 0.95))
        head_len = min(0.45, 0.32 * length)
        head_w = max(w + 0.24, w * 1.45)
        sx0 = p0[0]
        sx1 = p1[0] - sgn * head_len
        cy = p0[1]
        pts = [
            [sx0, cy - w / 2, 0],
            [sx1, cy - w / 2, 0],
            [sx1, cy - head_w / 2, 0],
            [p1[0], cy, 0],
            [sx1, cy + head_w / 2, 0],
            [sx1, cy + w / 2, 0],
            [sx0, cy + w / 2, 0],
        ]
        return Polygon(*pts, stroke_color=color, stroke_width=2.0, fill_color=color, fill_opacity=0.82)

    poly = always_redraw(mk)
    g = VGroup(poly)
    if label:
        mid = (p0 + p1) / 2
        t = T(label, size=label_size, color=color).move_to(mid + label_dir * 0.88)
        g.add(t)
        g.label = t
    return g


def make_flux_chevrons(start_x, end_x, y, phase_tracker, n=3, size=0.14, color=TEXT):
    """Crisp filled chevron polygons marching inside a horizontal rate arrow from start_x to end_x."""
    sgn = 1.0 if end_x >= start_x else -1.0
    span = abs(end_x - start_x)

    def mk():
        ph = phase_tracker.get_value() % 1.0
        g = VGroup()
        for k in range(n):
            f = (k / n + ph) % 1.0
            cx = start_x + sgn * f * span
            pts = [
                [cx - sgn * size * 0.55, y + size * 0.85, 0.0],
                [cx + sgn * size * 0.10, y + size * 0.85, 0.0],
                [cx + sgn * size * 0.75, y, 0.0],
                [cx + sgn * size * 0.10, y - size * 0.85, 0.0],
                [cx - sgn * size * 0.55, y - size * 0.85, 0.0],
                [cx + sgn * size * 0.10, y, 0.0],
            ]
            g.add(Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=0.88))
        return g

    return always_redraw(mk)


def make_balance_plot():
    """Shared computed first-order plot for s05, s06, s07, s08."""
    P = Plot(
        box=(-3.4, 5.4, -2.35, 2.15),
        xr=(0.0, 1.5),
        yr=(0.0, 3.2),
        xticks=(),
        yticks=(),
        xlabel="time",
        ylabel="cAMP",
        color=TEXT,
        size=24,
        label_size=28,
        stroke=3.5,
    )
    return P


def add_random_walk_updater(tokens, rng, x_bounds, y_bounds, speed=0.45):
    """Attach computed 2D random-walk diffusion to a VGroup of tokens (fixed seed)."""
    dirs = rng.uniform(0, TAU, size=len(tokens))
    for i, tok in enumerate(tokens):
        tok._angle = float(dirs[i])

        def step(m, dt, idx=i):
            m._angle += float(rng.normal(0, 1.4)) * np.sqrt(max(dt, 0.001))
            vx = speed * np.cos(m._angle)
            vy = speed * np.sin(m._angle)
            m.shift([vx * dt, vy * dt, 0])
            x, y = m.get_x(), m.get_y()
            if x < x_bounds[0]:
                m.set_x(x_bounds[0])
                m._angle = 0.0
            elif x > x_bounds[1]:
                m.set_x(x_bounds[1])
                m._angle = PI
            if y < y_bounds[0]:
                m.set_y(y_bounds[0])
                m._angle = PI / 2
            elif y > y_bounds[1]:
                m.set_y(y_bounds[1])
                m._angle = -PI / 2

        tok.add_updater(step)


# ==============================================================================
# SCENES
# ==============================================================================

class S00Hook(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-3.5, y=MEMBRANE_Y)
        ext_lab = T("extracellular", size=28, color=TEXT).move_to([-5.0, 3.15, 0])
        mem_lab = T("plasma membrane", size=28, color=TEXT).move_to([4.5, 2.02, 0])
        cyt_lab = T("cytosol", size=28, color=TEXT).move_to([-5.3, -3.1, 0])
        tag = scope_tag("schematic", color=TEXT)

        adren = make_adrenaline(pos=(-5.2, 2.55, 0), radius=0.28, label_text="adrenaline")
        q_mark = T("?", size=72, color=GOLD, weight=BOLD).move_to([2.2, -0.45, 0])

        effectors = VGroup(
            make_effector((-3.8, -2.2, 0), glow=0.18, show_q=False),
            make_effector((-1.3, -2.2, 0), glow=0.18, show_q=False),
            make_effector((1.2, -2.2, 0), glow=0.18, show_q=False),
        )
        enz_lab = T("enzymes inside", size=28, color=TEAL).next_to(effectors, DOWN, buff=0.18)

        # Inner signal tokens emerging below the membrane (random walk)
        tokens = VGroup(*[
            make_camp_token([-3.5 + rng.uniform(-0.45, 0.45), -0.25 + rng.uniform(-0.35, 0.25), 0], radius=0.14)
            for _ in range(9)
        ])

        self.add(membrane, receptor, ext_lab, mem_lab, cyt_lab, effectors, enz_lab, tag)
        self.play(FadeIn(adren), run_time=0.5)

        # Drift adrenaline steadily toward the receptor pocket while staying outside
        self.play(adren.animate.move_to([-3.9, 2.48, 0]), run_time=2.8, rate_func=linear)

        self.at("how can enzymes")
        self.play(FadeIn(q_mark, scale=1.2), adren.animate.move_to([-3.55, 2.45, 0]), run_time=0.8, rate_func=linear)
        self.play(adren.animate.move_to([-2.4, 2.38, 0]), run_time=2.8, rate_func=linear)

        self.at("stop at the membrane")
        # Dock adrenaline circle right into receptor cup (x=-3.5, y=1.88), label stays clean to right
        self.play(
            adren.dot.animate.move_to([-3.5, 1.88, 0]),
            adren.label.animate.move_to([-1.85, 2.18, 0]),
            run_time=0.9,
        )
        stop_bar = Line([-4.15, 1.50, 0], [-2.85, 1.50, 0], color=YELLOW, stroke_width=5)
        self.play(Create(stop_bar), run_time=0.4)

        self.at("an inner signal")
        inner_lab = T("inner signal", size=28, color=GOLD).move_to([-0.3, 0.62, 0])
        self.play(FadeIn(tokens), FadeIn(inner_lab), run_time=0.5)
        add_random_walk_updater(tokens, rng, x_bounds=(-4.8, 0.8), y_bounds=(-1.38, 0.15), speed=0.95)
        self.wait(1.6)

        self.at("connect both spaces")
        bridge = DashedLine([-3.5, 1.80, 0], [-3.5, 0.75, 0], color=GOLD, stroke_width=3.5)
        self.play(Create(bridge), run_time=0.6)

        self.at("without carrying adrenaline")
        # Show blocked bypass arrow next to receptor
        bypass = CurvedArrow([-4.9, 2.05, 0], [-4.9, 0.65, 0], angle=0.55, color=RED, stroke_width=3.5)
        cross_a = Line([-5.25, 1.55, 0], [-4.75, 1.05, 0], color=RED, stroke_width=4.5)
        cross_b = Line([-5.25, 1.05, 0], [-4.75, 1.55, 0], color=RED, stroke_width=4.5)
        self.play(Create(bypass), Create(cross_a), Create(cross_b), run_time=0.7)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        rng = np.random.default_rng(17)
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-3.5, y=MEMBRANE_Y)
        pulse(receptor.cup, base=3.5, amp=1.8, speed=5.0)
        adren_dot = Circle(radius=0.28, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.88).move_to([-3.5, 1.88, 0])
        adren_lab = T("adrenaline", size=28, color=YELLOW).move_to([-1.85, 2.18, 0])
        tokens = VGroup(*[
            make_camp_token([rng.uniform(-4.8, 4.8), rng.uniform(0.18, 0.92), 0], radius=0.12)
            for _ in range(9)
        ])
        add_random_walk_updater(tokens, rng, x_bounds=(-5.5, 5.5), y_bounds=(0.12, 0.98), speed=0.5)

        card_box = RoundedRectangle(
            corner_radius=0.22, width=10.6, height=2.9,
            stroke_color=GOLD, stroke_width=2.8, fill_color=BG, fill_opacity=0.94,
        ).move_to([0, -1.65, 0])
        lesson_t = T("cAMP AND PROTEIN KINASE A", size=24, color=TEAL)
        title_t = T("The Messenger Level: Made and Erased", size=44, font=TITLE_FONT, color=TEXT)
        fit(title_t, max_w=9.8)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        tg = VGroup(lesson_t, title_t, rule).arrange(DOWN, buff=0.26).move_to(card_box)

        self.add(membrane, receptor, adren_dot, adren_lab, tokens)
        self.play(FadeIn(card_box), FadeIn(tg), run_time=0.45)
        self.wait(1.1)
        self.play(FadeOut(card_box), FadeOut(tg), run_time=0.35)
        self.finish()


class S02Relay(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(23)
        # Zoomed membrane view: membrane sits higher and thicker
        membrane = make_membrane(y=1.75, h=0.68)
        receptor = make_receptor(x=-4.3, y=1.75, scale=1.22)
        adren_dot = Circle(radius=0.32, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([-4.3, 2.34, 0])
        adren_lab = T("adrenaline", size=28, color=YELLOW).next_to(adren_dot, UP, buff=0.22)

        gs_box = RoundedRectangle(
            corner_radius=0.14, width=1.15, height=0.62,
            stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.14,
        ).move_to([-2.7, 0.78, 0])
        gs_lab = T("Gs", size=28, color=GREEN).move_to(gs_box)
        gs = VGroup(gs_box, gs_lab)

        cyclase = make_cyclase(x=1.45, y=1.75, scale=1.22, label=True, mem_h=0.68)
        cyt_lab = T("cytosol", size=28, color=TEXT).move_to([-5.3, -3.1, 0])
        ext_lab = T("extracellular", size=28, color=TEXT).move_to([4.9, 3.1, 0])
        tag = scope_tag("schematic", color=TEXT)

        self.add(membrane, receptor, adren_dot, adren_lab, gs, cyclase, cyt_lab, ext_lab, tag)

        # Beat 1: receptor changes shape
        self.at("changes shape")
        self.play(
            Rotate(receptor.tail, angle=0.52, about_point=receptor.pivot),
            receptor.tail.animate.set_color(YELLOW),
            run_time=1.1,
        )

        # Beat 2: activates Gs and starts moving toward cyclase
        self.at("activates gs")
        target_x = cyclase.lobe.get_left()[0] - gs_box.width / 2 - 0.16
        mid_x = (-2.7 + target_x) / 2
        self.play(
            gs_box.animate.set_fill(GREEN, opacity=0.45).set_stroke(GREEN, width=4),
            gs.animate.move_to([mid_x, cyclase.lobe.get_y(), 0]),
            run_time=2.6,
            rate_func=linear,
        )

        # Beat 3: Gs reaches adenylyl cyclase and turns catalytic lobe active
        self.at("gs reaches")
        self.play(gs.animate.move_to([target_x, cyclase.lobe.get_y(), 0]), run_time=2.2, rate_func=linear)
        self.play(
            cyclase.lobe.animate.set_fill(BLUE, opacity=0.45).set_stroke(BLUE, width=4.5),
            run_time=1.8,
        )

        # Beat 4: turns ATP into cyclic AMP
        self.at("turns a tp")
        entry_y = cyclase.lobe.get_bottom()[1] - 0.42
        atp1 = boxed_label("ATP", color=BLUE, size=26, pad=0.24).move_to([1.45, -1.85, 0])
        self.play(FadeIn(atp1, shift=UP * 0.25), run_time=0.35)
        self.play(atp1.animate.move_to([1.45, entry_y, 0]), run_time=0.55)

        self.at("into cyclic amp")
        camp1 = make_camp_token(pos=[1.45, entry_y, 0], radius=0.18, labelled=True)
        self.play(FadeOut(atp1, run_time=0.22), FadeIn(camp1, run_time=0.28))
        self.play(camp1.animate.move_to([4.25, -0.45, 0]), run_time=0.9)

        # Continuous synthesis stream for the last beat
        self.at("the membrane holds")
        brace = Brace(VGroup(receptor, cyclase), UP, color=BLUE, buff=0.12)
        step_lab = T("first step at membrane", size=28, color=BLUE).next_to(brace, UP, buff=0.14)
        # Keep step_lab clear of adren_lab if needed
        if step_lab.get_left()[0] < adren_lab.get_right()[0] + 0.2:
            step_lab.shift(RIGHT * (adren_lab.get_right()[0] + 0.25 - step_lab.get_left()[0]))
        self.play(FadeIn(brace), FadeIn(step_lab), run_time=0.6)

        # Spawn 4 more ATP -> cAMP tokens sequentially so motion runs to end
        spawned = VGroup()
        self.add(spawned)
        dests = [[-0.6, -2.0, 0], [0.9, -2.2, 0], [3.2, -1.7, 0], [4.3, -2.25, 0]]
        for k in range(4):
            dx = (k - 1.5) * 0.55
            a = boxed_label("ATP", color=BLUE, size=24, pad=0.26).move_to([1.45 + dx * 0.3, -1.9, 0])
            self.play(FadeIn(a), run_time=0.16)
            self.play(a.animate.move_to([1.45, entry_y, 0]), run_time=0.32)
            tok = make_camp_token([1.45, entry_y, 0], radius=0.16)
            self.play(FadeOut(a, run_time=0.12), FadeIn(tok, run_time=0.15))
            spawned.add(tok)
            self.play(tok.animate.move_to(dests[k]), run_time=0.32)
        add_random_walk_updater(spawned, rng, x_bounds=(-1.4, 4.7), y_bounds=(-2.55, -1.25), speed=1.0)

        self.finish()


class S03SecondMessenger(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(11)
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-4.2, y=MEMBRANE_Y)
        receptor.tail.rotate(0.45, about_point=receptor.pivot)
        adren = make_adrenaline(pos=(-4.2, 1.88, 0), radius=0.28, label_text="first messenger")
        adren.label.move_to([-4.2, 2.75, 0])

        cyclase = make_cyclase(x=-1.1, y=MEMBRANE_Y, scale=0.95, label=True)
        gs = boxed_label("Gs", color=GREEN, size=26, box=(0.85, 0.52)).next_to(cyclase.lobe, LEFT, buff=0.18)

        level_vt = ValueTracker(0.10)
        gauge = make_gauge(level_vt, center=(5.1, -0.78, 0), height=2.75, label="cAMP level")

        eff_pos = [(-4.2, -2.25, 0), (-1.4, -2.25, 0), (1.4, -2.25, 0)]
        effs = VGroup(*[make_effector(p, glow=0.20, show_q=False) for p in eff_pos])

        cyt_lab = T("cytosol", size=28, color=TEXT).move_to([-5.3, -3.15, 0])
        tag = scope_tag("schematic", color=TEXT)

        self.add(membrane, receptor, adren, gs, cyclase, gauge, effs, cyt_lab, tag)

        # Beat 1: cAMP is the second messenger
        self.at("cyclic amp is")
        spawn_pt = [-1.1, cyclase.lobe.get_bottom()[1] - 0.18, 0]
        first_tok = make_camp_token(spawn_pt, radius=0.16)
        sec_lab = T("second messenger", size=28, color=GOLD).move_to([1.7, 0.35, 0])
        self.play(FadeIn(first_tok), FadeIn(sec_lab), run_time=0.6)
        self.play(first_tok.animate.move_to([-0.2, -0.45, 0]), run_time=0.8)

        # Beat 2: its level changes inside after first messenger binds outside
        self.at("its level changes")
        batch1 = VGroup(*[make_camp_token(spawn_pt, radius=0.14) for _ in range(5)])
        self.add(batch1)
        targets1 = [[-2.6 + i * 0.95, -0.65 + rng.uniform(-0.30, 0.30), 0] for i in range(5)]
        self.play(
            *[tok.animate.move_to(pt) for tok, pt in zip(batch1, targets1)],
            level_vt.animate.set_value(0.36),
            run_time=1.35,
        )
        add_random_walk_updater(batch1, rng, x_bounds=(-4.8, 3.0), y_bounds=(-1.62, -0.32), speed=0.75)

        self.at("after the first messenger")
        ring = Circle(radius=0.45, color=YELLOW, stroke_width=4).move_to(adren.dot)
        self.play(Create(ring), run_time=0.8)
        self.play(FadeOut(ring, scale=1.3), run_time=0.8)

        # Beat 3: many copies carry one receptor input toward effectors
        self.at("many copies")
        batch2 = VGroup(*[make_camp_token(spawn_pt, radius=0.14) for _ in range(12)])
        self.add(batch2)
        targets2 = [[rng.uniform(-4.6, 2.7), rng.uniform(-1.60, -0.35), 0] for _ in range(12)]
        self.play(
            FadeOut(sec_lab),
            *[tok.animate.move_to(pt) for tok, pt in zip(batch2, targets2)],
            level_vt.animate.set_value(0.68),
            run_time=2.2,
        )
        add_random_walk_updater(first_tok, rng, x_bounds=(-4.8, 3.0), y_bounds=(-1.62, -0.32), speed=0.75)
        add_random_walk_updater(batch2, rng, x_bounds=(-4.8, 3.0), y_bounds=(-1.62, -0.32), speed=0.75)

        self.at("toward intracellular effectors")
        self.play(
            *[ef.box.animate.set_fill(TEAL, opacity=0.42) for ef in effs],
            *[ef.bar_fill.animate.stretch_to_fit_width(0.92, about_edge=LEFT).set_opacity(0.95) for ef in effs],
            level_vt.animate.set_value(0.76),
            run_time=1.4,
        )

        # Beat 4: unlike adrenaline, never need to cross
        self.at("unlike adrenaline")
        stay_lab = T("stays outside", size=28, color=YELLOW).move_to([-0.8, 2.85, 0])
        self.play(FadeIn(stay_lab), run_time=0.5)

        self.at("never need to cross")
        stop_line = Line([-4.8, 1.55, 0], [-3.6, 1.55, 0], color=YELLOW, stroke_width=5)
        self.play(Create(stop_line), run_time=0.6)
        self.finish()


class S03Amplification(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(31)
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-4.2, y=MEMBRANE_Y)
        receptor.tail.rotate(0.45, about_point=receptor.pivot)
        adren = make_adrenaline(pos=(-4.2, 1.88, 0), radius=0.28, label_text="first messenger")
        adren.label.move_to([-4.2, 2.75, 0])
        cyclase = make_cyclase(x=-1.1, y=MEMBRANE_Y, scale=0.95, label=True)
        gs = boxed_label("Gs", color=GREEN, size=26, box=(0.85, 0.52)).next_to(cyclase.lobe, LEFT, buff=0.18)

        # Shared tracker driving both gauge and token counter
        count_vt = ValueTracker(10.0)
        gauge_vt = ValueTracker(10.0 / 35.0)
        gauge = make_gauge(gauge_vt, center=(5.2, -0.75, 0), height=2.7, label="cAMP level")
        cnt = counter("{:.0f} tokens", count_vt, at=[5.2, -2.55, 0], size=28, color=GOLD)

        effs = VGroup(
            make_effector((-4.2, -2.25, 0), glow=0.75, show_q=False),
            make_effector((-1.4, -2.25, 0), glow=0.75, show_q=False),
            make_effector((1.4, -2.25, 0), glow=0.75, show_q=False),
        )
        initial_tokens = VGroup(*[
            make_camp_token([rng.uniform(-4.4, 2.0), rng.uniform(-1.55, -0.62), 0], radius=0.13)
            for _ in range(10)
        ])
        add_random_walk_updater(initial_tokens, rng, x_bounds=(-4.8, 2.1), y_bounds=(-1.58, -0.60), speed=0.75)
        tag = scope_tag("schematic", color=TEXT)

        self.add(membrane, receptor, adren, gs, cyclase, effs, initial_tokens, gauge, cnt, tag)

        spawn_pt = [-1.1, cyclase.lobe.get_bottom()[1] - 0.16, 0]

        def rec_pulse():
            ring = Circle(radius=0.42, color=YELLOW, stroke_width=3.5).move_to(adren.dot)
            return Succession(FadeIn(ring, run_time=0.2), FadeOut(ring, scale=1.35, run_time=0.35))

        # Beat 1: membrane step keeps making messenger (burst 1: +7 tokens)
        self.at("the membrane step")
        burst1 = VGroup(*[make_camp_token(spawn_pt, radius=0.13) for _ in range(7)])
        self.add(burst1)
        pts1 = [[rng.uniform(-4.4, 2.0), rng.uniform(-1.55, -0.62), 0] for _ in range(7)]
        self.play(
            rec_pulse(),
            *[t.animate.move_to(p) for t, p in zip(burst1, pts1)],
            count_vt.animate.set_value(17.0),
            gauge_vt.animate.set_value(17.0 / 35.0),
            run_time=2.8,
        )
        add_random_walk_updater(burst1, rng, x_bounds=(-4.8, 2.1), y_bounds=(-1.58, -0.60), speed=0.75)

        # Beat 2: every gold token carries the same chemical information
        self.at("every gold token")
        sample_tok = make_camp_token([2.7, -0.45, 0], radius=0.14)
        halo = Circle(radius=0.28, color=GOLD, stroke_width=3.5).move_to(sample_tok)
        same_lab = T("same signal", size=28, color=GOLD).move_to([2.7, 0.25, 0])
        self.play(FadeIn(sample_tok), Create(halo), FadeIn(same_lab), run_time=0.6)

        self.at("quantity becomes adjustable")
        # Burst 2: +6 tokens
        burst2 = VGroup(*[make_camp_token(spawn_pt, radius=0.13) for _ in range(6)])
        self.add(burst2)
        pts2 = [[rng.uniform(-4.4, 2.0), rng.uniform(-1.55, -0.62), 0] for _ in range(6)]
        self.play(
            rec_pulse(),
            FadeOut(halo), FadeOut(same_lab), FadeOut(sample_tok),
            *[t.animate.move_to(p) for t, p in zip(burst2, pts2)],
            count_vt.animate.set_value(23.0),
            gauge_vt.animate.set_value(23.0 / 35.0),
            run_time=1.8,
        )
        add_random_walk_updater(burst2, rng, x_bounds=(-4.8, 2.1), y_bounds=(-1.58, -0.60), speed=0.75)

        # Beat 3: more tokens raise the level (+7 tokens -> 30)
        self.at("more tokens raise")
        burst3 = VGroup(*[make_camp_token(spawn_pt, radius=0.13) for _ in range(7)])
        self.add(burst3)
        pts3 = [[rng.uniform(-4.4, 2.0), rng.uniform(-1.55, -0.62), 0] for _ in range(7)]
        self.play(
            rec_pulse(),
            *[t.animate.move_to(p) for t, p in zip(burst3, pts3)],
            count_vt.animate.set_value(30.0),
            gauge_vt.animate.set_value(30.0 / 35.0),
            run_time=1.8,
        )
        add_random_walk_updater(burst3, rng, x_bounds=(-4.8, 2.1), y_bounds=(-1.58, -0.60), speed=0.75)

        # Beat 4: location and lifetime preview
        self.at("their location")
        loc_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.15, width=1.9, height=0.92, color=TEAL, stroke_width=3.0).move_to([-2.9, -1.04, 0])
        )
        loc_lab = T("location", size=28, color=TEAL).next_to(loc_box, UP, buff=0.30)
        self.play(Create(loc_box), FadeIn(loc_lab), run_time=0.5)

        self.at("and lifetime")
        clk_vt = ValueTracker(0.0)
        clk = make_clock_ring(clk_vt, center=(3.3, -0.75, 0), radius=0.48, color=GOLD, label="lifetime")
        self.play(FadeIn(clk), run_time=0.4)
        self.play(clk_vt.animate.set_value(0.85), run_time=1.5, rate_func=linear)
        self.finish()


class S04SourceAndSink(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(43)
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-4.6, y=MEMBRANE_Y)
        receptor.tail.rotate(0.45, about_point=receptor.pivot)
        adren = make_adrenaline(pos=(-4.6, 1.88, 0), radius=0.28, label_text="adrenaline")
        adren.label.move_to([-4.6, 2.75, 0])
        cyclase = make_cyclase(x=-2.1, y=MEMBRANE_Y, scale=0.95, label=True)
        gs = boxed_label("Gs", color=GREEN, size=26, box=(0.8, 0.5)).next_to(cyclase.lobe, LEFT, buff=0.18)

        level_vt = ValueTracker(0.76)
        gauge = make_gauge(level_vt, center=(5.3, -0.75, 0), height=2.8, label="cAMP level")
        tag = scope_tag("schematic", color=TEXT)

        tokens = VGroup(*[
            make_camp_token([rng.uniform(-4.5, -0.4), rng.uniform(-1.7, -0.4), 0], radius=0.13)
            for _ in range(12)
        ])
        add_random_walk_updater(tokens, rng, x_bounds=(-4.8, -0.35), y_bounds=(-2.1, -0.35), speed=0.4)

        self.add(membrane, receptor, adren, gs, cyclase, tokens, gauge, tag)

        # Beat 1: keep accumulating -> gauge approaches top with upward arrow
        self.at("keep accumulating")
        up_arr = Arrow([4.45, -1.05, 0], [4.45, 0.55, 0], color=GOLD, stroke_width=5)
        self.play(level_vt.animate.set_value(0.96), FadeIn(up_arr), run_time=1.5)

        # Beat 2: Phosphodiesterase rises at right
        self.at("phosphodiesterase provides removal")
        pde = make_pde(pos=(1.15, -0.95, 0), w=2.35, h=1.25)
        self.play(FadeOut(up_arr), FadeIn(pde, shift=UP * 0.6), run_time=1.1)

        # Beat 3: Opens cAMP ring -> 5'-AMP (erasing message)
        self.at("opens cyclic")
        in_toks = VGroup(*[make_camp_token([-0.7, -0.95 + (i - 1) * 0.28, 0], radius=0.14) for i in range(3)])
        self.play(FadeIn(in_toks), run_time=0.3)
        intake_pt = pde.box.get_left() + LEFT * 0.14
        self.play(*[t.animate.move_to(intake_pt) for t in in_toks], run_time=0.8)

        self.at("erasing the message")
        amp_chips = VGroup(*[
            boxed_label("5′-AMP", color=AMP_MUTED, size=24, box=(1.25, 0.46)).move_to([3.55, -0.45 - i * 0.58, 0])
            for i in range(3)
        ])
        # Gauge retreats from top down to 0.344 (C0 = 1.1 out of 3.2) for continuity with s05
        self.play(
            FadeOut(in_toks, shift=RIGHT * 0.22),
            FadeIn(amp_chips, shift=RIGHT * 0.35),
            level_vt.animate.set_value(C_S04_END / 3.2),
            run_time=1.8,
        )

        # Beat 4: Cannot switch on the kinase that reads cyclic AMP
        self.at("that product cannot")
        inactive_lab = T("5′-AMP: PKA inactive", size=28, color=RED).move_to([1.6, -2.55, 0])
        self.play(FadeIn(inactive_lab), run_time=0.7)
        self.finish()


class S05BalanceCurve(SpokenScene):
    def construct(self):
        # Carried gauge on right transforms into Plot
        dummy_vt = ValueTracker(C_S04_END / 3.2)
        old_gauge = make_gauge(dummy_vt, center=(5.3, -0.75, 0), height=2.8, label="cAMP level")
        self.add(old_gauge)

        P = make_balance_plot()
        t_vt = ValueTracker(0.0)
        live = P.live_curve(c_rise, t_vt, color=GOLD, width=6)
        dot = P.dot(lambda: t_vt.get_value(), lambda: c_rise(t_vt.get_value()), color=GOLD, ring=TEXT, radius=0.12)

        # Left-side rate arrows: BLUE constant width 0.42, RED proportional to C(t)/C_PLAT * 0.42
        base_w = 0.42
        blue_arr = make_thick_arrow(
            [-6.15, 0.85, 0], [-3.85, 0.85, 0],
            lambda: base_w, color=BLUE, label="synthesis", label_dir=UP, label_size=28,
        )
        red_arr = make_thick_arrow(
            [-3.85, -0.75, 0], [-6.15, -0.75, 0],
            lambda: base_w * (c_rise(t_vt.get_value()) / C_PLAT),
            color=RED, label="breakdown", label_dir=DOWN, label_size=28,
        )
        tag = scope_tag("in this model", color=TEXT)

        flux_b_vt = ValueTracker(0.0)
        flux_r_vt = ValueTracker(0.0)
        flux_b = make_flux_chevrons(-6.05, -4.35, 0.85, flux_b_vt, n=3, size=0.13, color=TEXT)
        flux_r = make_flux_chevrons(-3.95, -5.65, -0.75, flux_r_vt, n=3, size=0.13, color=TEXT)
        flux_b.add_updater(lambda m, dt: flux_b_vt.increment_value(dt * 0.65))
        flux_r.add_updater(lambda m, dt: flux_r_vt.increment_value(dt * 0.65 * (c_rise(t_vt.get_value()) / C_PLAT)))

        # Live GOLD level column beside y-axis tied to the same t_vt ValueTracker
        def mk_ybar():
            val = c_rise(t_vt.get_value())
            y_bot = P.pt(0.0, 0.0)[1]
            y_top = P.pt(0.0, val)[1]
            h = max(0.06, y_top - y_bot)
            return Rectangle(
                width=0.18, height=h, stroke_width=0, fill_color=GOLD, fill_opacity=0.65,
            ).move_to([P.x0 - 0.14, y_bot + h / 2, 0])

        ybar = always_redraw(mk_ybar)

        self.play(ReplacementTransform(old_gauge, P), run_time=0.9)
        self.add(ybar, live, dot, blue_arr, red_arr, flux_b, flux_r, tag)

        # Beat 1: proportional removal strengthens as cAMP accumulates
        self.at("it strengthens")
        self.play(t_vt.animate.set_value(0.32), run_time=3.5, rate_func=linear)

        # Beat 2: higher level -> encounters more frequent -> curve climbs
        self.at("a higher level")
        self.play(t_vt.animate.set_value(0.75), run_time=4.8, rate_func=linear)

        # Beat 3: settles when synthesis and breakdown match
        self.at("the level settles")
        self.play(t_vt.animate.set_value(1.45), run_time=1.3, rate_func=linear)

        self.at("synthesis and breakdown match")
        match_line = P.hline(C_PLAT, None, color=GOLD, size=28, dashed=True)
        match_lab = T("rates match", size=28, color=GOLD).move_to(P.pt(0.72, C_PLAT) + UP * 0.34)
        self.play(Create(match_line), FadeIn(match_lab), run_time=0.8)

        # Beat 4: computed from first-order model
        self.at("this curve is computed")
        model_lab = T("computed first-order curve", size=28, color=TEXT).move_to([1.0, 2.95, 0])
        self.play(FadeIn(model_lab), run_time=0.6)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        P = make_balance_plot()
        orig_curve = P.curve(c_rise, color=GOLD, width=5, opacity=0.45)
        old_plat = P.hline(C_PLAT, "old plateau", color=GOLD, size=26, dashed=True)

        base_w = 0.42
        red_mult = ValueTracker(1.0)
        blue_arr = make_thick_arrow(
            [-6.15, 0.85, 0], [-3.85, 0.85, 0],
            lambda: base_w, color=BLUE, label="synthesis", label_dir=UP, label_size=28,
        )
        red_arr = make_thick_arrow(
            [-3.85, -0.75, 0], [-6.15, -0.75, 0],
            lambda: base_w * red_mult.get_value(),
            color=RED, label="breakdown", label_dir=DOWN, label_size=28,
        )
        tag = scope_tag("in this model", color=TEXT)

        # Ongoing flux chevrons moving along the arrows (real flux motion)
        flux_b_vt = ValueTracker(0.0)
        flux_r_vt = ValueTracker(0.0)
        flux_b = make_flux_chevrons(-6.05, -4.35, 0.85, flux_b_vt, n=3, size=0.13, color=TEXT)
        flux_r = make_flux_chevrons(-3.95, -5.65, -0.75, flux_r_vt, n=3, size=0.13, color=TEXT)
        flux_b.add_updater(lambda m, dt: flux_b_vt.increment_value(dt * 0.65))
        flux_r.add_updater(lambda m, dt: flux_r_vt.increment_value(dt * 0.65 * red_mult.get_value()))

        self.add(P, orig_curve, old_plat, blue_arr, red_arr, flux_b, flux_r, tag)

        # Beat 1: keep blue source unchanged
        self.at("keep the blue source")
        hold_badge = T("unchanged", size=26, color=BLUE).move_to([-5.0, 2.2, 0])
        self.play(FadeIn(hold_badge), run_time=0.6)

        # Beat 2: strengthen red removal
        self.at("strengthen the red removal")
        strong_badge = T("stronger", size=26, color=RED).move_to([-5.0, -2.15, 0])
        self.play(red_mult.animate.set_value(2.0), FadeIn(strong_badge), run_time=1.8, rate_func=linear)

        # Beat 3: nothing else changes
        self.at("nothing else")
        self.wait(3.5)

        # Beat 4: question and empty choice chips in top band (clear of plot)
        self.at("where will the cyclic")
        q_txt = T("New plateau: above or below?", size=30, color=GOLD).move_to([-2.1, 3.15, 0])
        above_chip = boxed_label("above", color=TEXT, size=28, box=(1.55, 0.56)).move_to([2.45, 3.15, 0])
        below_chip = boxed_label("below", color=TEXT, size=28, box=(1.55, 0.56)).move_to([4.35, 3.15, 0])

        self.play(FadeIn(q_txt), FadeIn(above_chip), FadeIn(below_chip), run_time=1.0)
        self.finish()


class S07PredictPause(NarratedScene):
    def construct(self):
        P = make_balance_plot()
        orig_curve = P.curve(c_rise, color=GOLD, width=5, opacity=0.45)
        old_plat = P.hline(C_PLAT, "old plateau", color=GOLD, size=26, dashed=True)
        base_w = 0.42
        blue_arr = make_thick_arrow(
            [-6.15, 0.85, 0], [-3.85, 0.85, 0],
            lambda: base_w, color=BLUE, label="synthesis", label_dir=UP, label_size=28,
        )
        red_arr = make_thick_arrow(
            [-3.85, -0.75, 0], [-6.15, -0.75, 0],
            lambda: base_w * 2.0, color=RED, label="breakdown", label_dir=DOWN, label_size=28,
        )
        flux_b_vt = ValueTracker(0.0)
        flux_r_vt = ValueTracker(0.0)
        flux_b = make_flux_chevrons(-6.05, -4.35, 0.85, flux_b_vt, n=3, size=0.13, color=TEXT)
        flux_r = make_flux_chevrons(-3.95, -5.65, -0.75, flux_r_vt, n=3, size=0.13, color=TEXT)
        flux_b.add_updater(lambda m, dt: flux_b_vt.increment_value(dt * 0.65))
        flux_r.add_updater(lambda m, dt: flux_r_vt.increment_value(dt * 1.30))
        hold_badge = T("unchanged", size=26, color=BLUE).move_to([-5.0, 2.2, 0])
        strong_badge = T("stronger", size=26, color=RED).move_to([-5.0, -2.15, 0])
        q_txt = T("New plateau: above or below?", size=30, color=GOLD).move_to([-2.1, 3.15, 0])
        above_chip = boxed_label("above", color=TEXT, size=28, box=(1.55, 0.56)).move_to([2.45, 3.15, 0])
        below_chip = boxed_label("below", color=TEXT, size=28, box=(1.55, 0.56)).move_to([4.35, 3.15, 0])

        ring, run = countdown(4.5, center=(6.0, -3.0, 0), radius=0.42, color=GOLD)
        self.add(P, orig_curve, old_plat, blue_arr, red_arr, flux_b, flux_r,
                 hold_badge, strong_badge, q_txt, above_chip, below_chip, ring)
        self.play(run)
        self.finish()


class S08Reveal(SpokenScene):
    def construct(self):
        P = make_balance_plot()
        orig_curve = DashedVMobject(P.curve(c_rise, color=GOLD, width=4.5, opacity=0.75), num_dashes=28)
        old_plat = P.hline(C_PLAT, "old plateau", color=GOLD, size=26, dashed=True)

        t_vt = ValueTracker(0.0)
        base_w = 0.42
        blue_arr = make_thick_arrow(
            [-6.15, 0.85, 0], [-3.85, 0.85, 0],
            lambda: base_w, color=BLUE, label="synthesis", label_dir=UP, label_size=28,
        )
        # RED breakdown rate = K_FAST * C(t). At t=0 (C=2.5), rate=20=2*V_STIM -> width=2*base_w.
        # As C(t) drops to 1.25, rate=10=V_STIM -> width=base_w (matches BLUE!).
        red_arr = make_thick_arrow(
            [-3.85, -0.75, 0], [-6.15, -0.75, 0],
            lambda: base_w * (K_FAST * c_drop_fast(t_vt.get_value()) / V_STIM),
            color=RED, label="breakdown", label_dir=DOWN, label_size=28,
        )
        q_txt = T("New plateau: above or below?", size=30, color=GOLD).move_to([-2.1, 3.15, 0])
        above_chip = boxed_label("above", color=TEXT, size=28, box=(1.55, 0.56)).move_to([2.45, 3.15, 0])
        below_chip = boxed_label("below", color=TEXT, size=28, box=(1.55, 0.56)).move_to([4.35, 3.15, 0])
        tag = scope_tag("in this model", color=TEXT)

        new_live = P.live_curve(c_drop_fast, t_vt, color=GOLD, width=6.5)
        dot = P.dot(lambda: t_vt.get_value(), lambda: c_drop_fast(t_vt.get_value()), color=GOLD, ring=TEXT, radius=0.12)

        def mk_ybar():
            val = c_drop_fast(t_vt.get_value())
            y_bot = P.pt(0.0, 0.0)[1]
            y_top = P.pt(0.0, val)[1]
            h = max(0.06, y_top - y_bot)
            return Rectangle(
                width=0.18, height=h, stroke_width=0, fill_color=GOLD, fill_opacity=0.65,
            ).move_to([P.x0 - 0.14, y_bot + h / 2, 0])

        ybar = always_redraw(mk_ybar)

        flux_b_vt = ValueTracker(0.0)
        flux_r_vt = ValueTracker(0.0)
        flux_b = make_flux_chevrons(-6.05, -4.35, 0.85, flux_b_vt, n=3, size=0.13, color=TEXT)
        flux_r = make_flux_chevrons(-3.95, -5.65, -0.75, flux_r_vt, n=3, size=0.13, color=TEXT)
        flux_b.add_updater(lambda m, dt: flux_b_vt.increment_value(dt * 0.65))
        flux_r.add_updater(lambda m, dt: flux_r_vt.increment_value(dt * 0.65 * (K_FAST * c_drop_fast(t_vt.get_value()) / V_STIM)))

        self.add(P, orig_curve, old_plat, blue_arr, red_arr, flux_b, flux_r,
                 q_txt, above_chip, below_chip, ybar, new_live, dot, tag)

        # Beat 1: Below! Fill 'below' chip in RED
        self.at("below")
        below_red = boxed_label("below", color=RED, size=28, box=(1.55, 0.56), fill_opacity=0.35).move_to(below_chip)
        self.play(Transform(below_chip, below_red), FadeOut(above_chip), run_time=0.6)

        # Beat 2: at every level stronger PDE removes more
        self.at("at every cyclic")
        self.play(t_vt.animate.set_value(0.28), run_time=5.0, rate_func=linear)

        # Beat 3: lower concentration enough to match unchanged source -> computed plateau falls
        self.at("a lower concentration")
        self.play(t_vt.animate.set_value(0.82), run_time=4.5, rate_func=linear)

        self.at("computed plateau falls")
        self.play(t_vt.animate.set_value(1.48), run_time=2.2, rate_func=linear)

        # Beat 4: balance returns at a different level; label both curves 'computed'
        self.at("the balance returns")
        new_plat = P.hline(C_LOW, "new plateau", color=GOLD, size=26, dashed=True)
        # Keep label clear of curve: put one 'computed' above old curve at t=0.5, one below new curve at t=0.5
        comp1 = T("computed", size=26, color=TEXT).move_to(P.pt(0.65, 2.15))
        comp2 = T("computed", size=26, color=TEXT).move_to(P.pt(0.65, 0.72))
        self.play(Create(new_plat), FadeIn(comp1), FadeIn(comp2), run_time=0.9)
        self.finish()


class S09Control(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(59)
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-4.7, y=MEMBRANE_Y)
        receptor.tail.rotate(0.45, about_point=receptor.pivot)
        adren = make_adrenaline(pos=(-4.7, 1.88, 0), radius=0.28, label_text="adrenaline")
        adren.label.move_to([-4.7, 2.75, 0])
        cyclase = make_cyclase(x=-1.6, y=MEMBRANE_Y, scale=0.95, label=True)

        level_vt = ValueTracker(0.75)
        gauge = make_gauge(level_vt, center=(5.3, -0.75, 0), height=2.8, label="cAMP level")
        pde = make_pde(pos=(3.15, -0.95, 0), w=2.35, h=1.2)
        tag = scope_tag("schematic", color=TEXT)

        # Two separate sliders (not combined!): Gs pushes synthesis up, Gi pulls 'some cyclase forms' down
        gs_track = Line([-3.65, -1.25, 0], [-3.65, -0.02, 0], color=BLUE, stroke_width=6)
        gs_knob = RoundedRectangle(corner_radius=0.08, width=0.55, height=0.26, color=BLUE, fill_color=BLUE, fill_opacity=0.8).move_to([-3.65, -0.82, 0])
        gs_lab = T("synthesis", size=26, color=BLUE).next_to(gs_track, DOWN, buff=0.16)
        gs_chip = boxed_label("Gs", color=GREEN, size=26, box=(0.8, 0.48)).move_to([-4.85, -0.82, 0])

        gi_track = Line([-0.22, -1.25, 0], [-0.22, -0.02, 0], color=BLUE, stroke_width=6)
        gi_knob = RoundedRectangle(corner_radius=0.08, width=0.55, height=0.26, color=BLUE, fill_color=BLUE, fill_opacity=0.8).move_to([-0.22, -0.35, 0])
        gi_lab = T("some cyclase\nforms", size=26, color=BLUE, line_spacing=0.85).next_to(gi_track, DOWN, buff=0.16)
        gi_chip = boxed_label("Gi", color=PURPLE, size=26, box=(0.8, 0.48)).move_to([0.92, -0.35, 0])

        tokens = VGroup(*[
            make_camp_token([1.45 + rng.uniform(-0.1, 0.35), -0.95 + rng.uniform(-0.35, 0.35), 0], radius=0.14)
            for _ in range(7)
        ])
        add_random_walk_updater(tokens, rng, x_bounds=(1.42, 1.85), y_bounds=(-1.55, -0.35), speed=1.15)

        self.add(membrane, receptor, adren, cyclase, gauge, pde, gs_track, gs_knob, gs_lab, gs_chip,
                 gi_track, gi_knob, gi_lab, gi_chip, tokens, tag)

        # Beat 1: Gs raises synthesis
        self.at("gs raises synthesis")
        up_arr = Arrow([-4.22, -1.05, 0], [-4.22, -0.10, 0], color=GREEN, stroke_width=4.5)
        self.play(
            gs_knob.animate.move_to([-3.65, -0.22, 0]),
            gs_chip.animate.move_to([-4.85, -0.22, 0]),
            FadeIn(up_arr),
            run_time=1.3,
        )

        # Beat 2: Gi lowers some forms of cyclase
        self.at("while gi lowers")
        dn_arr = Arrow([0.32, -0.25, 0], [0.32, -1.15, 0], color=PURPLE, stroke_width=4.5)
        self.play(
            gi_knob.animate.move_to([-0.22, -1.02, 0]),
            gi_chip.animate.move_to([0.92, -1.02, 0]),
            FadeIn(dn_arr),
            run_time=1.3,
        )

        # Beat 3: Phosphodiesterases set removal
        self.at("phosphodiesterases set removal")
        amp_chip = boxed_label("5′-AMP", color=AMP_MUTED, size=24, box=(1.2, 0.44)).move_to([3.15, -2.05, 0])
        self.play(FadeIn(amp_chip, shift=DOWN * 0.25), run_time=0.9)

        # Beat 4: before any downstream target is chosen
        self.at("these controls change")
        gate = DashedLine([-5.8, -2.62, 0], [4.2, -2.62, 0], color=TEAL, stroke_width=3)
        gate_lab = T("before downstream targets", size=28, color=TEAL).move_to([-0.8, -3.10, 0])
        self.play(Create(gate), FadeIn(gate_lab), run_time=1.0)
        self.finish()


class S09SignalEnd(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(71)
        # Left side: carried membrane world; Right side: computed first-order return Plot
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-5.1, y=MEMBRANE_Y)
        receptor.tail.rotate(0.45, about_point=receptor.pivot)
        adren = make_adrenaline(pos=(-5.1, 1.88, 0), radius=0.26, label_text="adrenaline")
        adren.label.move_to([-5.1, 2.68, 0])

        cyclase = make_cyclase(x=-2.1, y=MEMBRANE_Y, scale=0.88, label=True)
        gs_box = RoundedRectangle(corner_radius=0.12, width=1.45, height=0.56, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.35).move_to([-3.75, 0.72, 0])
        gs_txt = T("Gs·GTP", size=24, color=GREEN).move_to(gs_box)
        gs = VGroup(gs_box, gs_txt)

        syn_w = ValueTracker(0.40)
        syn_arr = make_thick_arrow([-2.1, -0.38, 0], [-0.4, -0.38, 0], lambda: syn_w.get_value(), color=BLUE)
        syn_lab = T("synthesis", size=26, color=BLUE).move_to([-1.25, -0.84, 0])

        pde = make_pde(pos=(-1.75, -1.85, 0), w=2.3, h=1.05)
        rem_w = ValueTracker(0.40)
        rem_arr = make_thick_arrow([-3.25, -1.85, 0], [-4.55, -1.85, 0], lambda: rem_w.get_value(), color=RED)

        tokens = VGroup(*[
            make_camp_token([-4.4 + rng.uniform(-0.3, 0.8), -1.85 + rng.uniform(-0.3, 0.3), 0], radius=0.13)
            for _ in range(7)
        ])
        add_random_walk_updater(tokens, rng, x_bounds=(-5.5, -3.25), y_bounds=(-2.45, -1.1), speed=0.75)

        flux_s_vt = ValueTracker(0.0)
        flux_r_vt = ValueTracker(0.0)
        flux_s = make_flux_chevrons(-2.02, -0.78, -0.38, flux_s_vt, n=2, size=0.09, color=TEXT)
        flux_r = make_flux_chevrons(-3.32, -4.22, -1.85, flux_r_vt, n=2, size=0.11, color=TEXT)
        flux_s.add_updater(lambda m, dt: flux_s_vt.increment_value(dt * 0.65 * (syn_w.get_value() / 0.40)))
        flux_r.add_updater(lambda m, dt: flux_r_vt.increment_value(dt * 0.65 * (rem_w.get_value() / 0.40)))

        # Right side: computed return Plot
        P = Plot(
            box=(0.9, 5.9, -2.3, 1.9),
            xr=(0.0, 1.5),
            yr=(0.0, 3.0),
            xticks=(),
            yticks=(),
            xlabel="time",
            ylabel="cAMP",
            color=TEXT,
            size=24,
            label_size=28,
            stroke=3.5,
        )
        rest_line = P.hline(C_REST, "resting level", color=GOLD, size=26, dashed=True)
        t_ret = ValueTracker(0.0)
        t_fast = ValueTracker(0.0)
        ret_curve = P.live_curve(lambda t: c_return(t, K_BASE), t_ret, color=GOLD, width=6)
        ret_dot = P.dot(lambda: t_ret.get_value(), lambda: c_return(t_ret.get_value(), K_BASE), color=GOLD, ring=TEXT, radius=0.11)
        fast_curve = P.live_curve(lambda t: c_return(t, K_FAST), t_fast, color=RED, width=5.5)

        tag = scope_tag("in this model", color=TEXT)
        self.add(membrane, receptor, adren, cyclase, gs, syn_arr, syn_lab, pde, rem_arr, flux_s, flux_r, tokens,
                 P, rest_line, ret_curve, ret_dot, fast_curve, tag)

        # Beat 1: Adrenaline leaves, receptor stops activating new Gs
        self.at("when adrenaline leaves")
        self.play(adren.animate.shift(UP * 1.4 + LEFT * 0.6).set_opacity(0.0), run_time=1.3)
        self.remove(adren)

        self.at("stops activating")
        self.play(
            Rotate(receptor.tail, angle=-0.45, about_point=receptor.pivot),
            receptor.tail.animate.set_color(GREY),
            run_time=0.8,
        )

        # Beat 2: Active Gs lingers, splits GTP, cyclase drive fades
        self.at("lingers until")
        self.wait(0.7)
        self.at("splits its gtp")
        gs_gdp = T("Gs·GDP", size=24, color=TEXT).move_to(gs_box)
        self.play(
            Transform(gs_txt, gs_gdp),
            gs_box.animate.set_fill(GREY, opacity=0.18).set_stroke(GREY, width=2),
            run_time=0.8,
        )

        self.at("cyclase drive fades")
        self.play(gs.animate.shift(DOWN * 0.4).set_opacity(0.0), run_time=1.1)
        self.remove(gs)

        # Beat 3: Synthesis falls back to resting rate (narrow, never zero)
        self.at("synthesis falls back")
        rest_syn_lab = T("resting synthesis", size=26, color=BLUE).move_to([-1.25, -0.84, 0])
        self.play(
            syn_w.animate.set_value(0.11),
            swap(syn_lab, rest_syn_lab, run_time=0.7),
            run_time=1.2,
        )

        # Beat 4: PDE returns cAMP along computed curve toward resting level
        self.at("phosphodiesterase then returns")
        ret_title = T("computed first-order return", size=26, color=TEXT).move_to([3.75, 2.55, 0])
        amp_out = boxed_label("5′-AMP", color=AMP_MUTED, size=24, box=(1.15, 0.42)).move_to([-1.75, -2.95, 0])
        self.play(
            FadeIn(ret_title),
            FadeIn(amp_out, shift=DOWN * 0.2),
            t_ret.animate.set_value(1.48),
            run_time=3.5,
            rate_func=linear,
        )

        # Beat 5: Faster removal makes return briefer
        self.at("faster removal makes")
        fast_lab = T("faster removal", size=26, color=RED).move_to(P.pt(0.75, 1.85))
        self.play(
            rem_w.animate.set_value(0.82),
            t_fast.animate.set_value(1.48),
            FadeIn(fast_lab),
            run_time=1.9,
            rate_func=linear,
        )
        self.finish()


class S10Handoff(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(83)
        membrane = make_membrane(y=MEMBRANE_Y)
        receptor = make_receptor(x=-4.5, y=MEMBRANE_Y)
        receptor.tail.rotate(0.45, about_point=receptor.pivot)
        adren = make_adrenaline(pos=(-4.5, 1.88, 0), radius=0.28, label_text="adrenaline")
        adren.label.move_to([-4.5, 2.75, 0])
        cyclase = make_cyclase(x=-1.5, y=MEMBRANE_Y, scale=0.92, label=True)
        gs = boxed_label("Gs", color=GREEN, size=26, box=(0.8, 0.5)).next_to(cyclase.lobe, LEFT, buff=0.18)

        level_vt = ValueTracker(0.25)
        gauge = make_gauge(level_vt, center=(5.3, -0.65, 0), height=2.6, label="cAMP level")
        clk_vt = ValueTracker(0.0)
        clk = make_clock_ring(clk_vt, center=(5.3, -2.55, 0), radius=0.40, color=GOLD)
        clk.add_updater(lambda m, dt: clk_vt.increment_value(dt * 0.22))
        tag = scope_tag("schematic", color=TEXT)
        life_lab = T("lifetime", size=26, color=GOLD).next_to(clk, LEFT, buff=0.22)

        pool_tokens = VGroup(*[
            make_camp_token([rng.uniform(-4.4, 2.8), rng.uniform(-1.35, -0.25), 0], radius=0.13)
            for _ in range(9)
        ])
        add_random_walk_updater(pool_tokens, rng, x_bounds=(-4.8, 3.2), y_bounds=(-1.45, -0.20), speed=0.80)

        self.add(membrane, receptor, adren, gs, cyclase, pool_tokens, gauge, clk, life_lab, tag)

        # Beat 1: adjustable height and lifetime
        self.at("adjustable height")
        self.play(level_vt.animate.set_value(0.62), run_time=1.8)

        # Beat 2: amount is not the response itself
        self.at("its amount is not")
        not_lab = T("amount is not the response", size=28, color=TEXT).move_to([-0.5, -2.25, 0])
        self.play(FadeIn(not_lab), run_time=0.4)

        # Beat 3: several possible effectors wait in the same cytosol
        self.at("several possible effectors")
        eff1 = make_effector((-4.2, -1.9, 0), glow=0.45, show_q=True)
        eff2 = make_effector((-1.0, -2.55, 0), glow=0.45, show_q=True)
        eff3 = make_effector((1.3, -1.25, 0), glow=0.45, show_q=True)
        self.play(FadeOut(not_lab), run_time=0.30)
        # Keep 5 pool tokens diffusing in upper-right cytosol clear of cyclase and effectors until handoff
        for k, tok in enumerate(pool_tokens):
            tok.clear_updaters()
            if k < 5:
                tok.move_to([rng.uniform(0.3, 3.2), rng.uniform(-0.45, -0.15), 0])
            else:
                tok.set_opacity(0.0)
        add_random_walk_updater(VGroup(*pool_tokens[:5]), rng, x_bounds=(0.2, 3.3), y_bounds=(-0.50, -0.10), speed=0.80)
        self.play(FadeIn(eff1), FadeIn(eff2), FadeIn(eff3), run_time=0.65)

        spawn_pt = [-1.5, cyclase.lobe.get_bottom()[1] - 0.16, 0]
        toks = VGroup(
            make_camp_token(spawn_pt, radius=0.13),
            make_camp_token(spawn_pt, radius=0.13),
            make_camp_token(spawn_pt, radius=0.13),
        )
        self.add(toks)
        self.play(
            toks[0].animate.move_to(eff1.box.get_top() + UP * 0.18),
            toks[1].animate.move_to(eff2.box.get_top() + UP * 0.18),
            toks[2].animate.move_to(eff3.box.get_top() + UP * 0.18),
            run_time=1.4,
        )

        # Beat 4: next question -> zoom/focus toward one unlabelled TEAL effector
        self.at("the next question")
        focus_ring = RoundedRectangle(
            corner_radius=0.22, width=3.15, height=1.38,
            stroke_color=TEAL, stroke_width=4, fill_opacity=0,
        ).move_to(eff3.get_center())
        self.play(Create(focus_ring), run_time=0.7)

        self.at("turns that level")
        # Emphasize eff3 + its '?' for handoff without naming PKA
        handoff_group = VGroup(eff3, toks[2], focus_ring)
        self.play(FadeOut(eff1), FadeOut(eff2), FadeOut(toks[0]), FadeOut(toks[1]), FadeOut(pool_tokens), run_time=0.4)
        self.play(handoff_group.animate.scale(1.35).move_to([0.0, -1.55, 0]), run_time=1.1)
        self.finish()


class S11End(EndCard):
    LINE = "cAMP levels reflect the balance of synthesis and breakdown."
