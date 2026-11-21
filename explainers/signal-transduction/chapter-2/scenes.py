"""The OFF Switch Decides — STEMhop teaching film (Signal-Transduction Pathways, Chapter 2).

COLOUR MAP (one colour per concept for the whole film):
- BG (#0f1117): dark canvas
- TEXT (#E8EAF0): primary labels, ON lamp state (WHITE #FFFFFF glow)
- GREY (#8B93A1): structural lines, plasma membrane, OFF lamp outline/dim state (never used for text)
- GREEN (#83C167): ON arm (reaction pushing a switch ON)
- RED (#FC6255): OFF arm (reaction pulling a switch OFF, built-in GTPase timer)
- ORANGE (#FF9F43): epinephrine (first messenger outside the membrane)
- GOLD (#D4A843): cyclic AMP (second messenger inside the cell), gain/counter highlight
- PALE_BLUE (#8AD8F0): glucose units (liver cell output)
- CYAN (#2FE6E6): chloride and water (gut cell output in cholera)
- PURPLE (#B87DFF): cholera toxin

THE ONE WORLD CARRIED THROUGH THE FILM:
One tall schematic cell cross-section filling ~70% of the frame height, with the plasma membrane
across the top, a tissue label above top-left, a 'schematic' tag at bottom right, THE RELAY ROW
of four switch lamps stacked down the middle ('receptor' in the membrane, 'Gs alpha', 'cyclase',
'PKA') each flanked by a GREEN ON arrow (left) and a RED OFF arrow (right), and one OUTPUT TILE
at the bottom whose label and output dots follow the cell type.

WHAT CHANGES IN EACH SPOKEN SCENE (computed from the lesson's numbers):
- s00_link_and_hook: Epinephrine docks on the liver-cell receptor, lamps switch ON top to bottom,
  computed cAMP particles spill from cyclase, and glucose particles stream out; then the tissue
  switches to gut cell, cholera toxin drifts in and breaks Gs alpha's RED OFF arrow, Gs alpha
  stays WHITE, cAMP pours continuously, and cyan chloride/water drops stream out the bottom.
- s02_contest: Focused on Gs alpha: GDP swaps for GTP as the receptor pushes ON; a computed
  countdown stopwatch runs on the RED OFF arrow and flips GTP back to GDP; then the two arms
  oscillate in a computed contest settling at 50% glow with an ON-versus-OFF tug line.
- s03_gain: Focused on Gs alpha + cyclase: a single ValueTracker t_on (0..10 s) simultaneously fills
  the ON-time bar, runs down the RED stopwatch (1 - t_on/10), emits cAMP dots into the counter
  box, and updates the counter as 10 * t_on up to 100; slowing the timer extends the bar past 100
  and overflows the cAMP column to 'more' before resetting.
- s04_multiply: Full relay cascades ON as a single running-total counter and log10 gain bar step
  through the computed cumulative product of the lesson's teaching gains [10, 1, 100, 0.5, 10, 10,
  1000] from 10 to 50,000,000 ('tens of millions') and pale BLUE glucose dots flood the lower cell.
- s05_idea: All four lamps glow with ON-time bars feeding the running total while glucose streams;
  when epinephrine lifts off, each lamp decays exponentially along exp(-t/tau_i) with PKA's
  slowest OFF step setting the thinning rate of the glucose stream.
- s06_cholera: In the gut cell, cholera toxin freezes the ticking RED stopwatch and cracks Gs
  alpha's OFF arrow; a padlock locks Gs alpha WHITE while cAMP pours nonstop and cyan drops fill
  a growing pool below the cell ('into intestine').
- s07_predict: Focused on PKA's clamp and active subunit: cAMP dots open the clamp and light the
  core, then leave so it closes; morphing to an adrenal cell ('cortisol'), the active subunit
  changes edge shape so it cannot fit the clamp while upper RED OFF arrows glow intact and all
  cAMP drains away.
- s09_answer: Question swaps to 'ON'; the misshapen PKA core lights full WHITE, slides free of
  the empty clamp, and drives steady WHITE cortisol output dots with no hormone at the receptor
  and intact RED arrows above, while PKA's GREEN ON arrow fades to a ghost.
- s10_ways_to_stick: Pulling back to the liver cell, three computed failure icons assemble on the
  left: cracked RED arrow ('lost OFF arm'), lit lamp with ghost GREEN arrow ('needs no ON signal'),
  and a weak-ON/strong-OFF switch ('weak ON arm', 'insulin resistance') with a thin 'too little'
  trickle.
- s11_close: Returning to the intact relay, RED OFF arrows brighten, running total and ON-time bars
  glow while glucose flows, then Gs alpha's RED arrow cracks as epinephrine floats away while cAMP
  and glucose keep pouring without hormone.
"""

import numpy as np
from bp_parts import *  # noqa: F401,F403
from kx_manim import TAIL

# Concept colours (in addition to BG, TEXT, GREY, GREEN, RED, GOLD, BLUE from bp_parts/bp_style)
ORANGE = "#FF9F43"
PALE_BLUE = "#8AD8F0"
CYAN = "#2FE6E6"
PURPLE = "#B87DFF"
LAMP_OFF_FILL = "#2D374E"
LAMP_ON_FILL = "#FFFFFF"
CELL_FILL = "#242E44"

GAINS = [10, 1, 100, 0.5, 10, 10, 1000]
GAIN_LABELS = ["×10", "×1", "×100", "×½", "×10", "×10", "×1,000"]


def make_lamp(name, width=2.0, height=0.56, size=26, on=False):
    """One switch lamp: rounded pill whose fill/border show OFF (dim slate) or ON (bright WHITE)."""
    fill = LAMP_ON_FILL if on else LAMP_OFF_FILL
    stroke = WHITE if on else GREY
    text_col = BG if on else TEXT
    rect = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        stroke_color=stroke,
        stroke_width=3.0 if on else 2.5,
        fill_color=fill,
        fill_opacity=0.96 if on else 0.94,
    )
    lab = T(name, size=size, color=text_col, weight=BOLD if on else NORMAL).move_to(rect)
    g = VGroup(rect, lab)
    g.rect = rect
    g.label = lab
    g.lamp_name = name
    return g


def set_lamp_state(lamp, frac, on_color=LAMP_ON_FILL):
    """Update a lamp's glow smoothly between 0 (OFF) and 1 (ON)."""
    frac = float(np.clip(frac, 0.0, 1.0))
    fill = interpolate_color(ManimColor(LAMP_OFF_FILL), ManimColor(on_color), frac)
    stroke = interpolate_color(ManimColor(GREY), ManimColor(WHITE), frac)
    txt_col = interpolate_color(ManimColor(TEXT), ManimColor(BG), 1.0 if frac > 0.65 else 0.0)
    lamp.rect.set_fill(fill, opacity=0.94 + 0.05 * frac)
    lamp.rect.set_stroke(stroke, width=2.5 + 1.1 * frac)
    lamp.label.set_color(txt_col)


def make_on_arrow(lamp, length=1.05, buff=0.12, stroke_width=6.0, color=GREEN):
    """GREEN ON arrow pushing from the left toward a lamp (never touching its border)."""
    tip = lamp.rect.get_left() + LEFT * buff
    start = tip + LEFT * length
    return Arrow(
        start,
        tip,
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.28,
        tip_length=0.22,
    )


def make_off_arrow(lamp, length=1.05, buff=0.12, stroke_width=6.0, color=RED):
    """RED OFF arrow pulling from the right toward a lamp (never touching its border)."""
    tip = lamp.rect.get_right() + RIGHT * buff
    start = tip + RIGHT * length
    return Arrow(
        start,
        tip,
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.28,
        tip_length=0.22,
    )


def cracked_arrow_shape(arrow, color=GREY):
    """A jagged broken arrow replacing an intact RED OFF arrow."""
    s = arrow.get_start()
    e = arrow.get_end()
    mid = (s + e) / 2
    p1 = Line(s, mid + RIGHT * 0.12 + UP * 0.08, color=color, stroke_width=4.8)
    p2 = Line(mid + LEFT * 0.12 + DOWN * 0.08, e + RIGHT * 0.12, color=color, stroke_width=4.8)
    crack = Line(mid + UP * 0.22 + LEFT * 0.05, mid + DOWN * 0.22 + RIGHT * 0.05, color=RED, stroke_width=3.5)
    return VGroup(p1, p2, crack)


def make_epinephrine(radius=0.23):
    """ORANGE epinephrine ball (no molecular structure)."""
    return Dot(radius=radius, color=ORANGE, stroke_color=TEXT, stroke_width=2.0)


def make_toxin(radius=0.30):
    """PURPLE cholera toxin token (plain pentagon badge, no molecular structure)."""
    return RegularPolygon(
        n=5, radius=radius, color=PURPLE, fill_color=PURPLE, fill_opacity=0.95, stroke_color=TEXT, stroke_width=2.2
    )


def make_padlock(scale=1.0, color=GOLD):
    """Simple geometric padlock icon for 'locked ON'."""
    body = RoundedRectangle(
        corner_radius=0.06, width=0.38 * scale, height=0.28 * scale, color=color, fill_color=color, fill_opacity=0.92, stroke_width=2
    )
    shackle = Arc(radius=0.13 * scale, start_angle=0, angle=PI, color=TEXT, stroke_width=3.5 * scale)
    shackle.next_to(body, UP, buff=-0.02)
    return VGroup(shackle, body)


def make_stopwatch(tracker, center, radius=0.42, label_text="timer", label_dir=UP, color=RED, label_size=26):
    """Live RED countdown stopwatch tied to a ValueTracker (1.0 -> 0.0)."""
    c = np.array(center, dtype=float)
    ring = Circle(radius=radius, color=GREY, stroke_width=4.5, fill_color=BG, fill_opacity=0.6).move_to(c)
    knob = Line(c + UP * radius, c + UP * (radius + 0.11), color=GREY, stroke_width=5.2)
    arc = always_redraw(
        lambda: Arc(
            radius=radius,
            start_angle=PI / 2,
            angle=max(float(tracker.get_value()), 0.002) * TAU,
            arc_center=c,
            color=color,
            stroke_width=6.0,
        )
    )
    hand = always_redraw(
        lambda: Line(
            c,
            c + 0.78 * radius * np.array([
                np.sin(TAU * float(tracker.get_value())),
                np.cos(TAU * float(tracker.get_value())),
                0.0,
            ]),
            color=TEXT,
            stroke_width=3.8,
        )
    )
    g = VGroup(ring, knob, arc, hand)
    if label_text:
        lab = T(label_text, size=label_size, color=color).next_to(ring, label_dir, buff=0.14)
        g.add(lab)
        g.label = lab
    g.ring = ring
    return g


def make_output_tile(text, color=PALE_BLUE, width=2.8, height=0.56, size=26):
    """Output tile at the bottom of the cell."""
    lab = T(text, size=size, color=color)
    w = max(width, lab.width + 0.44)
    rect = RoundedRectangle(
        corner_radius=0.14,
        width=w,
        height=height,
        stroke_color=color,
        stroke_width=2.8,
        fill_color=color,
        fill_opacity=0.22,
    )
    lab.move_to(rect)
    g = VGroup(rect, lab)
    g.rect = rect
    g.label = lab
    return g


def make_cytoplasm_backdrop(width=12.4, top_y=2.95, bot_y=-3.05, x_center=0.0):
    """Carried cell cytoplasm fill for zoomed-in scenes (borderless so outer labels stay clear)."""
    h = top_y - bot_y
    fill = RoundedRectangle(
        corner_radius=0.35, width=width, height=h, stroke_width=0,
        fill_color=CELL_FILL, fill_opacity=0.88,
    ).move_to([x_center, (top_y + bot_y) / 2.0, 0])
    fill.set_z_index(-5)
    return fill


def build_cell_world(x_center=0.0, tissue="liver cell", output="glucose", output_color=PALE_BLUE,
                     cell_w=6.2, top_y=2.50, bot_y=-2.50):
    """Build the carried cell cross-section, split plasma membrane, relay row, arrows, and output tile."""
    world = VGroup()
    h = top_y - bot_y
    mid_y = (top_y + bot_y) / 2.0

    body_fill = RoundedRectangle(
        corner_radius=0.35,
        width=cell_w,
        height=h,
        stroke_width=0,
        fill_color=CELL_FILL,
        fill_opacity=0.96,
    ).move_to([x_center, mid_y, 0])

    xL = x_center - cell_w / 2.0
    xR = x_center + cell_w / 2.0
    walls = VMobject(color=GREY, stroke_width=3.2, fill_opacity=0)
    walls.set_points_as_corners([
        [xL, top_y - 0.18, 0],
        [xL, bot_y + 0.2, 0],
        [xL + 0.2, bot_y, 0],
        [xR - 0.2, bot_y, 0],
        [xR, bot_y + 0.2, 0],
        [xR, top_y - 0.18, 0],
    ])

    ys = [top_y - 0.15, top_y - 1.18, top_y - 2.21, top_y - 3.24]
    names = ["receptor", "Gs alpha", "cyclase", "PKA"]
    lamps = []
    on_arrows = []
    off_arrows = []
    connectors = VGroup()

    for nm, yy in zip(names, ys):
        lp = make_lamp(nm, width=2.05, height=0.56, size=26, on=False).move_to([x_center, yy, 0])
        oa = make_on_arrow(lp, length=1.1, buff=0.12)
        fa = make_off_arrow(lp, length=1.1, buff=0.12)
        lamps.append(lp)
        on_arrows.append(oa)
        off_arrows.append(fa)

    rec_l = lamps[0].rect.get_left()[0] - 0.08
    rec_r = lamps[0].rect.get_right()[0] + 0.08
    mem_left = VGroup(
        Rectangle(width=rec_l - xL, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to([(xL + rec_l) / 2, top_y - 0.09, 0]),
        Line([xL, top_y, 0], [rec_l, top_y, 0], color=GREY, stroke_width=4.2),
        Line([xL, top_y - 0.18, 0], [rec_l, top_y - 0.18, 0], color=GREY, stroke_width=3.2),
    )
    mem_right = VGroup(
        Rectangle(width=xR - rec_r, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to([(rec_r + xR) / 2, top_y - 0.09, 0]),
        Line([rec_r, top_y, 0], [xR, top_y, 0], color=GREY, stroke_width=4.2),
        Line([rec_r, top_y - 0.18, 0], [xR, top_y - 0.18, 0], color=GREY, stroke_width=3.2),
    )

    tissue_lab = T(tissue, size=28, color=TEXT).move_to([xL + 0.15, top_y + 0.30, 0], aligned_edge=LEFT)

    for idx in range(len(lamps) - 1):
        a = lamps[idx].rect.get_bottom() + DOWN * 0.06
        b = lamps[idx + 1].rect.get_top() + UP * 0.06
        connectors.add(Line(a, b, color=GREY, stroke_width=2.8))

    tile = make_output_tile(output, color=output_color, width=2.45, height=0.54, size=26).move_to([x_center, bot_y + 0.52, 0])
    connectors.add(Line(lamps[-1].rect.get_bottom() + DOWN * 0.06, tile.rect.get_top() + UP * 0.06, color=GREY, stroke_width=2.8))

    world.add(body_fill, walls, mem_left, mem_right, tissue_lab, connectors, *lamps, *on_arrows, *off_arrows, tile)
    world.body = body_fill
    world.walls = walls
    world.membrane = VGroup(mem_left, mem_right)
    world.tissue_lab = tissue_lab
    world.connectors = connectors
    world.lamps = lamps
    world.receptor, world.gs, world.cyclase, world.pka = lamps
    world.on_arrows = on_arrows
    world.off_arrows = off_arrows
    world.tile = tile
    world.x_center = x_center
    world.cell_w = cell_w
    world.top_y = top_y
    world.bot_y = bot_y
    return world


def make_particle_stream(start_pt, end_pt, phase_tracker, count=12, color=GOLD, radius=0.085, spread=0.65, seed=7):
    """Computed particle stream drifting smoothly from start_pt to end_pt driven by phase_tracker."""
    rng = np.random.default_rng(seed)
    offsets = rng.uniform(-spread, spread, size=count)
    phases = np.linspace(0.0, 1.0, count, endpoint=False)
    s = np.array(start_pt, dtype=float)
    e = np.array(end_pt, dtype=float)
    dx = np.array([1.0, 0.0, 0.0])

    def mk():
        p0 = float(phase_tracker.get_value())
        g = VGroup()
        for off, ph in zip(offsets, phases):
            u = (p0 + ph) % 1.0
            pos = s + (e - s) * u + dx * off * np.sin(u * PI)
            alpha = float(np.sin(u * PI)) ** 0.35
            g.add(Dot(pos, radius=radius, color=color).set_opacity(max(0.35, alpha)))
        return g

    return always_redraw(mk)


def make_pka_assembly(center=(0.0, -0.55, 0.0), open_amt=0.0, shape_mutant=False, lit=False):
    """Zoomed-in PKA lamp: two plain bracket shapes ('clamp') around an 'active subunit' core."""
    c = np.array(center, dtype=float)
    gap = 0.98 + 0.60 * open_amt

    def bracket(side):
        w, h, t = 0.44, 1.48, 0.15
        if side < 0:
            pts = [
                [t, h / 2, 0], [-w, h / 2, 0], [-w, -h / 2, 0], [t, -h / 2, 0],
                [t, -h / 2 + t, 0], [-w + t, -h / 2 + t, 0], [-w + t, h / 2 - t, 0], [t, h / 2 - t, 0],
            ]
        else:
            pts = [
                [-t, h / 2, 0], [w, h / 2, 0], [w, -h / 2, 0], [-t, -h / 2, 0],
                [-t, -h / 2 + t, 0], [w - t, -h / 2 + t, 0], [w - t, h / 2 - t, 0], [-t, h / 2 - t, 0],
            ]
        p = Polygon(*pts, color=TEAL, stroke_width=3.0, fill_color=TEAL, fill_opacity=0.32)
        return p.move_to(c + RIGHT * side * gap)

    left_b = bracket(-1)
    right_b = bracket(+1)

    fill_col = LAMP_ON_FILL if lit else LAMP_OFF_FILL
    stroke_col = WHITE if lit else GREY
    txt_col = BG if lit else TEXT
    if not shape_mutant:
        core_shape = Circle(
            radius=0.80,
            color=stroke_col,
            stroke_width=3.2 if lit else 2.6,
            fill_color=fill_col,
            fill_opacity=0.96 if lit else 0.94,
        ).move_to(c)
    else:
        pts = [
            [0.0, 0.86, 0], [0.58, 0.64, 0], [0.96, 0.22, 0], [0.70, 0.0, 0],
            [0.96, -0.22, 0], [0.58, -0.64, 0], [0.0, -0.86, 0], [-0.58, -0.64, 0],
            [-0.96, -0.22, 0], [-0.70, 0.0, 0], [-0.96, 0.22, 0], [-0.58, 0.64, 0],
        ]
        core_shape = Polygon(
            *pts,
            color=stroke_col,
            stroke_width=3.2 if lit else 2.6,
            fill_color=fill_col,
            fill_opacity=0.96 if lit else 0.94,
        ).move_to(c)

    core_lab = T("active\nsubunit", size=26, color=txt_col, line_spacing=0.88).move_to(core_shape)
    core = VGroup(core_shape, core_lab)
    core.shape = core_shape
    core.label = core_lab

    clamp_lab = T("clamp", size=26, color=TEAL).next_to(left_b, DOWN, buff=0.18)
    g = VGroup(left_b, right_b, core, clamp_lab)
    g.left_b = left_b
    g.right_b = right_b
    g.core = core
    g.clamp_lab = clamp_lab
    return g


# ------------------------------------------------------------------ scenes

class S00LinkAndHook(SpokenScene):
    def construct(self):
        world = build_cell_world(x_center=0.0, tissue="liver cell", output="glucose", output_color=PALE_BLUE)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(world, tag)

        epi = make_epinephrine().move_to(world.receptor.rect.get_top() + UP * 0.95 + LEFT * 0.4)
        phase = ValueTracker(0.0)
        camp_stream = make_particle_stream(
            world.cyclase.rect.get_bottom() + DOWN * 0.06,
            world.pka.rect.get_top() + UP * 0.06,
            phase,
            count=8,
            color=GOLD,
            radius=0.075,
            spread=0.4,
            seed=7,
        )
        gluc_stream = make_particle_stream(
            world.tile.rect.get_bottom() + DOWN * 0.05,
            world.tile.rect.get_bottom() + DOWN * 0.72,
            phase,
            count=10,
            color=PALE_BLUE,
            radius=0.07,
            spread=0.65,
            seed=11,
        )

        self.at("epinephrine")
        self.play(FadeIn(epi), epi.animate.move_to(world.receptor.rect.get_top() + UP * 0.23), run_time=0.6)
        set_lamp_state(world.receptor, 1.0)
        self.play(Indicate(world.on_arrows[0], color=GREEN, scale_factor=1.15), run_time=0.25)
        set_lamp_state(world.gs, 1.0)
        set_lamp_state(world.cyclase, 1.0)
        self.add(camp_stream)
        self.play(phase.animate.set_value(0.65), run_time=0.55, rate_func=linear)
        set_lamp_state(world.pka, 1.0)
        self.add(gluc_stream)
        self.play(phase.animate.set_value(1.55), run_time=0.85, rate_func=linear)

        self.remove(camp_stream, gluc_stream)
        self.play(FadeOut(epi), run_time=0.35)
        for lp in world.lamps:
            set_lamp_state(lp, 0.0)

        self.at("Now picture")
        gut_lab = T("gut cell", size=28, color=TEXT).move_to(world.tissue_lab, aligned_edge=LEFT)
        cl_tile = make_output_tile("chloride and water", color=CYAN, width=3.1, height=0.54, size=26).move_to(world.tile)
        toxin = make_toxin().move_to([5.4, world.gs.get_y() + 0.45, 0])
        self.play(
            swap(world.tissue_lab, gut_lab, run_time=0.6),
            ReplacementTransform(world.tile, cl_tile),
            FadeIn(toxin),
            run_time=0.75,
        )
        world.tissue_lab = gut_lab
        world.tile = cl_tile
        self.play(
            toxin.animate.move_to([3.4, world.gs.get_y() + 0.35, 0]),
            Indicate(world.gs.rect, color=PURPLE, scale_factor=1.08),
            run_time=2.4,
            rate_func=linear,
        )

        self.at("switches nothing")
        self.play(
            toxin.animate.move_to(world.off_arrows[1].get_center() + UP * 0.30),
            Indicate(world.on_arrows[1], color=GREEN, scale_factor=1.18),
            run_time=0.9,
        )

        self.at("breaks one")
        cracked = cracked_arrow_shape(world.off_arrows[1], color=GREY)
        self.play(ReplacementTransform(world.off_arrows[1], cracked), run_time=0.5)
        world.off_arrows[1] = cracked
        set_lamp_state(world.gs, 1.0)
        set_lamp_state(world.cyclase, 1.0)
        set_lamp_state(world.pka, 1.0)

        camp_pour = make_particle_stream(
            world.cyclase.rect.get_bottom() + DOWN * 0.06,
            world.pka.rect.get_top() + UP * 0.06,
            phase,
            count=10,
            color=GOLD,
            radius=0.08,
            spread=0.45,
            seed=13,
        )
        cyan_pour = make_particle_stream(
            world.tile.rect.get_bottom() + DOWN * 0.04,
            [world.x_center, -3.6, 0],
            phase,
            count=16,
            color=CYAN,
            radius=0.09,
            spread=0.85,
            seed=17,
        )
        self.add(camp_pour, cyan_pour)

        self.at("why can that")
        q_text = T("Why is this deadly?", size=38, color=TEXT, weight=BOLD).move_to([0, 3.28, 0])
        self.play(FadeIn(q_text, shift=DOWN * 0.1), phase.animate.set_value(2.5), run_time=0.65, rate_func=linear)
        rem = max(0.1, self.narration_s + TAIL - self.elapsed())
        self.play(phase.animate.set_value(2.5 + rem * 1.15), run_time=rem, rate_func=linear)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = build_cell_world(x_center=0.0, tissue="gut cell", output="chloride and water", output_color=CYAN)
        tag = scope_tag("schematic", size=24, color=TEXT)
        cracked = cracked_arrow_shape(world.off_arrows[1], color=GREY)
        world.off_arrows[1].become(cracked)
        set_lamp_state(world.gs, 1.0)
        set_lamp_state(world.cyclase, 1.0)
        set_lamp_state(world.pka, 1.0)
        toxin = make_toxin().move_to(world.off_arrows[1].get_center() + UP * 0.28)
        q_text = T("Why is this deadly?", size=38, color=TEXT, weight=BOLD).move_to([0, 3.28, 0])

        rng = np.random.default_rng(7)
        c_dots = VGroup(*[
            Dot([rng.uniform(-1.5, 1.5), rng.uniform(-1.2, 0.8), 0], radius=0.07, color=GOLD).set_opacity(0.85)
            for _ in range(10)
        ])
        self.add(world, tag, toxin, q_text, c_dots)

        title = T("The OFF Switch Decides", size=44, font=TITLE_FONT, color=TEXT).move_to([0, 3.28, 0])
        liver_lab = T("liver cell", size=28, color=TEXT).move_to(world.tissue_lab, aligned_edge=LEFT)
        gluc_tile = make_output_tile("glucose", color=PALE_BLUE, width=2.45, height=0.54, size=26).move_to(world.tile)
        intact_off = make_off_arrow(world.gs, length=1.1, buff=0.12)

        self.play(FadeOut(q_text), run_time=0.25)
        for lp in world.lamps:
            set_lamp_state(lp, 0.0)
        self.play(
            FadeIn(title, shift=DOWN * 0.08),
            FadeOut(toxin),
            FadeOut(c_dots, shift=UP * 0.15),
            ReplacementTransform(world.off_arrows[1], intact_off),
            swap(world.tissue_lab, liver_lab, run_time=0.6),
            ReplacementTransform(world.tile, gluc_tile),
            run_time=1.3,
        )
        self.wait(max(0.05, self.narration_s + TAIL - self.elapsed()))
        self.finish()


class S02Contest(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        cyto = make_cytoplasm_backdrop(width=11.0, top_y=2.9, bot_y=-3.05, x_center=0.0)
        gs = make_lamp("Gs alpha", width=3.2, height=1.05, size=34, on=False).move_to([0, 0.2, 0])
        rec = make_lamp("receptor", width=2.25, height=0.54, size=26, on=False).move_to([0, 2.45, 0])
        cyc = make_lamp("cyclase", width=2.25, height=0.54, size=26, on=False).move_to([0, -2.65, 0])
        on_arr = make_on_arrow(gs, length=2.1, buff=0.16, stroke_width=8.0)
        off_arr = make_off_arrow(gs, length=2.1, buff=0.16, stroke_width=8.0)
        c1 = Line(rec.rect.get_bottom() + DOWN * 0.06, gs.rect.get_top() + UP * 0.06, color=GREY, stroke_width=2.8)
        cell_lbl = T("liver cell", size=28, color=TEXT).move_to([-5.3, 3.22, 0], aligned_edge=LEFT)

        focus = VGroup(rec, c1, gs, on_arr, off_arr, cyc)
        focus.save_state()
        focus.scale(0.90)
        self.add(cyto, focus, cell_lbl, tag)
        self.play(focus.animate.restore(), run_time=1.6)

        epi = make_epinephrine(radius=0.23).move_to(rec.rect.get_top() + UP * 0.62)
        gdp = boxed_label("GDP", color=TEXT, size=26, pad=0.16).move_to([0.0, -0.80, 0])
        gtp = boxed_label("GTP", color=GOLD, size=26, pad=0.16).move_to([-2.8, -0.80, 0])

        self.at("receptor pushes")
        self.play(FadeIn(epi), epi.animate.move_to(rec.rect.get_top() + UP * 0.23), run_time=0.6)
        set_lamp_state(rec, 0.9)
        self.play(on_arr.animate.shift(RIGHT * 0.22), FadeIn(gdp), run_time=0.55)

        self.at("swapping")
        self.play(gdp.animate.shift(RIGHT * 2.7), run_time=0.55)
        self.play(FadeOut(gdp), FadeIn(gtp), run_time=0.25)
        self.play(gtp.animate.move_to([0.0, -0.80, 0]), on_arr.animate.shift(LEFT * 0.22), run_time=0.6)
        set_lamp_state(gs, 1.0)

        t_rem = ValueTracker(1.0)
        sw = make_stopwatch(t_rem, center=[3.3, 1.65, 0], radius=0.48, label_text="timer", label_dir=UP, color=RED, label_size=26)
        self.at("Its own")
        self.play(FadeIn(sw), run_time=0.5)

        self.at("pulls it")
        self.play(
            t_rem.animate.set_value(0.0),
            off_arr.animate.shift(LEFT * 0.22),
            run_time=1.5,
            rate_func=linear,
        )
        gdp_back = boxed_label("GDP", color=TEXT, size=26, pad=0.16).move_to([0.0, -0.80, 0])
        self.play(swap(gtp, gdp_back, run_time=0.35), off_arr.animate.shift(RIGHT * 0.22), run_time=0.45)
        set_lamp_state(gs, 0.0)

        self.at("How much is")
        rope = Line([-3.6, -1.42, 0], [3.6, -1.42, 0], color=GOLD, stroke_width=4.5)
        rope_lbl = T("ON versus OFF", size=28, color=GOLD).next_to(rope, DOWN, buff=0.14)
        self.play(FadeOut(gdp_back), run_time=0.25)
        self.play(Create(rope), FadeIn(rope_lbl, shift=UP * 0.08), run_time=0.45)

        contest_t = ValueTracker(0.0)
        def update_contest(m):
            v = contest_t.get_value()
            lvl = 0.5 + 0.45 * np.exp(-0.9 * v) * np.sin(5.2 * v)
            set_lamp_state(gs, lvl)
            dx = 0.22 * np.exp(-0.9 * v) * np.sin(5.2 * v)
            on_arr.move_to([-2.81 + dx, 0.2, 0])
            off_arr.move_to([2.81 + dx, 0.2, 0])

        gs.add_updater(update_contest)
        rem = max(0.5, self.narration_s + TAIL - self.elapsed())
        self.play(contest_t.animate.set_value(3.2), run_time=rem, rate_func=linear)
        gs.remove_updater(update_contest)
        set_lamp_state(gs, 0.5)
        self.finish()


class S03Gain(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        cyto = make_cytoplasm_backdrop(width=11.6, top_y=3.0, bot_y=-2.65, x_center=0.0)
        gs = make_lamp("Gs alpha", width=2.55, height=0.80, size=28, on=True).move_to([-3.0, 1.15, 0])
        cyc = make_lamp("cyclase", width=2.55, height=0.80, size=28, on=True).move_to([-3.0, -1.25, 0])
        on_gs = make_on_arrow(gs, length=1.15, buff=0.12)
        off_gs = make_off_arrow(gs, length=1.15, buff=0.12)
        on_cyc = make_on_arrow(cyc, length=1.15, buff=0.12)
        off_cyc = make_off_arrow(cyc, length=1.15, buff=0.12)
        conn = Line(gs.rect.get_bottom() + DOWN * 0.06, cyc.rect.get_top() + UP * 0.06, color=TEXT, stroke_width=3.5)

        t_on = ValueTracker(0.0)
        sw_center = np.array([-0.8, 2.25, 0.0])
        sw_r = 0.42
        sw_ring = Circle(radius=sw_r, color=GREY, stroke_width=4.5, fill_color=BG, fill_opacity=0.6).move_to(sw_center)
        sw_knob = Line(sw_center + UP * sw_r, sw_center + UP * (sw_r + 0.1), color=GREY, stroke_width=5.2)
        sw_arc = always_redraw(
            lambda: Arc(
                radius=sw_r,
                start_angle=PI / 2,
                angle=max(1.0 - t_on.get_value() / 10.0, 0.002) * TAU,
                arc_center=sw_center,
                color=RED,
                stroke_width=6.0,
            )
        )
        sw_hand = always_redraw(
            lambda: Line(
                sw_center,
                sw_center + 0.78 * sw_r * np.array([
                    np.sin(TAU * max(0.0, 1.0 - t_on.get_value() / 10.0)),
                    np.cos(TAU * max(0.0, 1.0 - t_on.get_value() / 10.0)),
                    0.0,
                ]),
                color=TEXT,
                stroke_width=3.8,
            )
        )
        sw_lbl = T("timer", size=26, color=RED).next_to(sw_ring, UP, buff=0.12)
        sw_group = VGroup(sw_ring, sw_knob, sw_arc, sw_hand, sw_lbl)

        bar_left = 0.9
        bar_w = 3.5
        bar_y = 1.95
        on_time_lbl = T("ON time", size=28, color=TEXT).move_to([bar_left + bar_w / 2, bar_y + 0.55, 0])
        bar_track = RoundedRectangle(corner_radius=0.08, width=bar_w, height=0.38, stroke_color=GREY, stroke_width=2.6,
                                     fill_color=LAMP_OFF_FILL, fill_opacity=0.9).move_to([bar_left + bar_w / 2, bar_y, 0])
        bar_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.02, bar_w * min(1.0, t_on.get_value() / 10.0)),
                height=0.32,
                stroke_width=0,
                fill_color=WHITE,
                fill_opacity=0.96,
            ).move_to([bar_left + max(0.02, bar_w * min(1.0, t_on.get_value() / 10.0)) / 2, bar_y, 0])
        )
        clock_lbl = always_redraw(
            lambda: M(f"{min(10.0, t_on.get_value()):4.1f} s", size=26, color=TEXT).next_to(bar_track, RIGHT, buff=0.18)
        )

        cbox = RoundedRectangle(corner_radius=0.16, width=4.0, height=2.25, stroke_color=GOLD, stroke_width=3.0,
                                fill_color=BG, fill_opacity=0.85).move_to([2.85, -0.1, 0])
        cbox_title = T("cyclic AMP made", size=28, color=GOLD).move_to([2.85, 0.68, 0])
        cbox_num = always_redraw(
            lambda: M(f"{int(round(10 * min(10.0, t_on.get_value()))):d}", size=52, color=TEXT).move_to([2.85, -0.18, 0])
        )
        fill_bg = Rectangle(width=3.4, height=0.28, stroke_color=GREY, stroke_width=1.8, fill_opacity=0.0).move_to([2.85, -0.88, 0])
        fill_bar = always_redraw(
            lambda: Rectangle(
                width=max(0.02, 3.4 * min(1.0, t_on.get_value() / 10.0)),
                height=0.24,
                stroke_width=0,
                fill_color=GOLD,
                fill_opacity=0.94,
            ).move_to([2.85 - 1.7 + max(0.02, 3.4 * min(1.0, t_on.get_value() / 10.0)) / 2, -0.88, 0])
        )

        self.add(cyto, gs, cyc, on_gs, off_gs, on_cyc, off_cyc, conn, sw_group,
                 on_time_lbl, bar_track, bar_fill, clock_lbl, cbox, cbox_title, cbox_num, fill_bg, fill_bar, tag)

        phase = ValueTracker(0.0)
        camp_dots = make_particle_stream(
            cyc.rect.get_right() + RIGHT * 0.1,
            cbox.get_left() + LEFT * 0.1,
            phase,
            count=10,
            color=GOLD,
            radius=0.09,
            spread=0.4,
            seed=21,
        )

        self.at("cyclase makes")
        self.add(camp_dots)
        self.play(phase.animate.set_value(1.8), t_on.animate.set_value(2.0), run_time=2.3, rate_func=linear)

        self.at("10 a second")
        self.play(
            t_on.animate.set_value(10.0),
            phase.animate.set_value(5.4),
            run_time=3.2,
            rate_func=linear,
        )
        self.remove(camp_dots)
        set_lamp_state(gs, 0.0)
        set_lamp_state(cyc, 0.0)

        self.at("gain is its")
        eq_lbl = T("gain = speed × ON time", size=28, color=TEXT).move_to([2.85, -1.78, 0])
        self.play(FadeIn(eq_lbl, shift=UP * 0.1), run_time=0.55)
        self.play(Indicate(cyc.rect, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.play(Indicate(bar_track, color=WHITE, scale_factor=1.08), Indicate(on_time_lbl, color=GOLD, scale_factor=1.08), run_time=1.0)

        self.at("Slow the timer")
        t_on.set_value(0.0)
        set_lamp_state(gs, 1.0)
        set_lamp_state(cyc, 1.0)
        self.add(camp_dots)
        self.remove(clock_lbl)

        ext_bar = Rectangle(width=1.45, height=0.32, stroke_color=WHITE, stroke_width=2.0,
                            fill_color=WHITE, fill_opacity=0.72).move_to([bar_left + bar_w + 0.72, bar_y, 0])
        more_bar_lbl = T("more", size=26, color=GOLD).next_to(ext_bar, DOWN, buff=0.14)

        self.play(t_on.animate.set_value(10.0), phase.animate.set_value(7.0), run_time=1.4, rate_func=linear)
        more_val = T("more", size=44, color=GOLD, weight=BOLD).move_to([2.85, -0.18, 0])
        self.remove(cbox_num)
        self.add(more_val)
        self.play(
            FadeIn(ext_bar, shift=RIGHT * 0.2),
            FadeIn(more_bar_lbl),
            phase.animate.set_value(8.8),
            run_time=1.5,
            rate_func=linear,
        )
        self.remove(camp_dots, more_val, ext_bar, more_bar_lbl)
        t_on.set_value(0.0)
        self.add(cbox_num)
        set_lamp_state(gs, 0.0)
        set_lamp_state(cyc, 0.0)
        self.finish()


class S04Multiply(SpokenScene):
    def construct(self):
        world = build_cell_world(x_center=-1.9, tissue="liver cell", output="glucose", output_color=PALE_BLUE, cell_w=5.8)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(world, tag)

        rt_box = RoundedRectangle(corner_radius=0.16, width=4.6, height=2.9, stroke_color=GOLD, stroke_width=3.0,
                                  fill_color=CELL_FILL, fill_opacity=0.95).move_to([3.85, 0.15, 0])
        rt_title = T("running total", size=28, color=GOLD).move_to([3.85, 1.25, 0])
        rt_val = M("1", size=42, color=TEXT).move_to([3.85, 0.45, 0])
        step_lbl = T("step gain: ×1", size=26, color=TEAL).move_to([3.85, -0.25, 0])
        # Computed log10 amplification bar inside running total box (0..8 decades -> 1..100,000,000)
        bar_bg = Rectangle(width=3.8, height=0.28, stroke_color=GREY, stroke_width=1.8, fill_opacity=0.0).move_to([3.85, -0.88, 0])
        bar_fill = Rectangle(width=0.06, height=0.24, stroke_width=0, fill_color=TEAL, fill_opacity=0.92).move_to([3.85 - 1.9 + 0.03, -0.88, 0])
        teach_tag = T("teaching values", size=24, color=TEXT).next_to(rt_box, DOWN, buff=0.22)
        self.add(rt_box, rt_title, rt_val, step_lbl, bar_bg, bar_fill)

        self.at("its own")
        for i in range(4):
            self.play(
                Indicate(world.on_arrows[i], color=GREEN, scale_factor=1.24),
                Indicate(world.off_arrows[i], color=RED, scale_factor=1.24),
                Indicate(world.lamps[i].rect, color=TEXT, scale_factor=1.06),
                run_time=0.72,
            )

        self.at("the gains multiply")
        epi = make_epinephrine().move_to(world.receptor.rect.get_top() + UP * 0.7)
        self.play(FadeIn(epi), epi.animate.move_to(world.receptor.rect.get_top() + UP * 0.23), run_time=0.45)

        cum = []
        prod = 1.0
        for g in GAINS:
            prod *= g
            cum.append(int(round(prod)))

        self.at("one epinephrine")
        lamp_map = [0, 1, 2, 3, 3, 3, 3]
        for val, gl, li in zip(cum, GAIN_LABELS, lamp_map):
            set_lamp_state(world.lamps[li], 1.0)
            new_val = M(f"{val:,}", size=40 if val < 1_000_000 else 34, color=TEXT).move_to([3.85, 0.45, 0])
            new_step = T(f"step gain: {gl}", size=26, color=TEAL).move_to([3.85, -0.25, 0])
            frac = float(np.clip(np.log10(max(val, 1)) / 8.0, 0.02, 1.0))
            w = 3.8 * frac
            new_bar = Rectangle(width=w, height=0.24, stroke_width=0, fill_color=TEAL, fill_opacity=0.92).move_to([3.85 - 1.9 + w / 2, -0.88, 0])
            rt_val.become(new_val)
            step_lbl.become(new_step)
            self.play(
                Transform(bar_fill, new_bar),
                Indicate(world.lamps[li].rect, color=GOLD, scale_factor=1.08),
                run_time=0.30,
            )

        self.at("tens of millions")
        phase = ValueTracker(0.0)
        camp_flow = make_particle_stream(
            world.cyclase.rect.get_bottom() + DOWN * 0.06,
            world.pka.rect.get_top() + UP * 0.06,
            phase,
            count=12,
            color=GOLD,
            radius=0.085,
            spread=0.5,
            seed=29,
        )
        gluc_flood = make_particle_stream(
            world.tile.rect.get_bottom() + DOWN * 0.02,
            [world.x_center, world.bot_y + 0.02, 0],
            phase,
            count=26,
            color=PALE_BLUE,
            radius=0.095,
            spread=2.2,
            seed=31,
        )
        self.add(camp_flow, gluc_flood)
        tens_lbl = T("tens of millions", size=34, color=PALE_BLUE, weight=BOLD).move_to([3.85, 0.45, 0])
        self.play(
            swap(rt_val, tens_lbl, run_time=0.4),
            FadeIn(teach_tag),
            phase.animate.set_value(0.8),
            run_time=0.65,
            rate_func=linear,
        )
        rem = max(0.1, self.narration_s + TAIL - self.elapsed())
        self.play(phase.animate.set_value(0.8 + rem * 1.2), run_time=rem, rate_func=linear)
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        world = build_cell_world(x_center=-2.2, tissue="liver cell", output="glucose", output_color=PALE_BLUE, cell_w=5.2)
        for lp in world.lamps:
            set_lamp_state(lp, 1.0)
        tag = scope_tag("schematic", size=24, color=TEXT)
        banner = T("ON arm versus OFF arm", size=36, color=TEXT, weight=BOLD).move_to([1.1, 3.38, 0])
        epi = make_epinephrine().move_to(world.receptor.rect.get_top() + UP * 0.23)

        rt_box = RoundedRectangle(corner_radius=0.16, width=3.7, height=1.8, stroke_color=GOLD, stroke_width=2.8,
                                  fill_color=CELL_FILL, fill_opacity=0.95).move_to([4.3, -0.35, 0])
        rt_title = T("running total", size=28, color=GOLD).move_to([4.3, 0.15, 0])
        rt_val = T("tens of millions", size=30, color=PALE_BLUE, weight=BOLD).move_to([4.3, -0.55, 0])

        phase = ValueTracker(0.0)
        flow_amp = ValueTracker(1.0)
        rng = np.random.default_rng(41)
        g_offs = rng.uniform(-1.6, 1.6, size=24)
        g_ph = np.linspace(0.0, 1.0, 24, endpoint=False)

        def mk_gluc():
            p0 = float(phase.get_value())
            amp = float(flow_amp.get_value())
            g = VGroup()
            n_show = max(1, int(round(24 * amp)))
            for off, ph in zip(g_offs[:n_show], g_ph[:n_show]):
                u = (p0 + ph) % 1.0
                pos = world.tile.rect.get_bottom() + DOWN * (0.02 + 0.56 * u) + RIGHT * off * u
                g.add(Dot(pos, radius=0.09, color=PALE_BLUE).set_opacity(max(0.35, amp)))
            return g

        gluc = always_redraw(mk_gluc)
        self.add(world, epi, banner, rt_box, rt_title, rt_val, gluc, tag)
        self.play(phase.animate.set_value(1.2), run_time=1.8, rate_func=linear)

        self.at("pushed on")
        self.play(*[Indicate(a, color=GREEN, scale_factor=1.22) for a in world.on_arrows],
                  phase.animate.set_value(2.1), run_time=1.0, rate_func=linear)

        self.at("pulled off")
        self.play(*[Indicate(a, color=RED, scale_factor=1.22) for a in world.off_arrows],
                  phase.animate.set_value(3.0), run_time=1.0, rate_func=linear)

        self.at("how long")
        on_bars = VGroup(*[
            Rectangle(width=w, height=0.22, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([0.65 + w / 2, lp.get_y(), 0])
            for lp, w in zip(world.lamps, [0.42, 0.68, 0.52, 0.90])
        ])
        bar_lbl = T("ON time", size=24, color=TEXT).next_to(on_bars[0], UP, buff=0.14)
        self.play(FadeIn(on_bars), FadeIn(bar_lbl), phase.animate.set_value(4.0), run_time=1.0, rate_func=linear)

        self.at("how big")
        feed_lines = VGroup(*[
            Line(b.get_right() + RIGHT * 0.08, [rt_box.get_left()[0] - 0.08, rt_box.get_center()[1], 0], color=GOLD, stroke_width=2.6)
            for b in on_bars
        ])
        self.play(
            Create(feed_lines),
            rt_box.animate.set_stroke(WHITE, width=4.0),
            phase.animate.set_value(5.2),
            run_time=1.2,
            rate_func=linear,
        )

        self.at("once the signal")
        slow_sw_t = ValueTracker(1.0)
        slow_sw = make_stopwatch(slow_sw_t, center=[2.7, -2.25, 0], radius=0.38, label_text="slowest OFF step", label_dir=RIGHT, color=RED, label_size=24)
        self.play(
            epi.animate.shift(UP * 1.4).set_opacity(0.0),
            FadeIn(slow_sw),
            FadeOut(feed_lines),
            run_time=0.7,
        )
        self.remove(epi)

        taus = [0.65, 1.2, 1.0, 3.8]
        fade_t = ValueTracker(0.0)

        def update_fade(m):
            t = float(fade_t.get_value())
            for lp, bar, tau in zip(world.lamps, on_bars, taus):
                lvl = float(np.exp(-t / tau))
                set_lamp_state(lp, lvl)
                bar.set_opacity(max(0.15, lvl))
            slow_lvl = float(np.exp(-t / taus[-1]))
            flow_amp.set_value(slow_lvl)
            slow_sw_t.set_value(max(0.0, 1.0 - t / 5.0))

        world.add_updater(update_fade)
        rem = max(0.5, self.narration_s + TAIL - self.elapsed())
        self.play(
            fade_t.animate.set_value(4.5),
            phase.animate.set_value(5.2 + rem * 1.15),
            run_time=rem,
            rate_func=linear,
        )
        world.remove_updater(update_fade)
        self.finish()


class S06Cholera(SpokenScene):
    def construct(self):
        world = build_cell_world(x_center=0.0, tissue="liver cell", output="glucose", output_color=PALE_BLUE, cell_w=5.8, top_y=2.55, bot_y=-1.90)
        tag = scope_tag("schematic", size=24, color=TEXT)
        self.add(world, tag)

        gut_lab = T("gut cell", size=28, color=TEXT).move_to(world.tissue_lab, aligned_edge=LEFT)
        cl_tile = make_output_tile("chloride and water", color=CYAN, width=3.1, height=0.54, size=26).move_to(world.tile)
        sw_t = ValueTracker(1.0)
        sw = make_stopwatch(sw_t, center=[4.15, world.gs.get_y() + 0.85, 0], radius=0.40, label_text="", color=RED)
        toxin = make_toxin().move_to([5.6, world.gs.get_y(), 0])

        self.play(
            swap(world.tissue_lab, gut_lab, run_time=0.5),
            ReplacementTransform(world.tile, cl_tile),
            FadeIn(sw),
            sw_t.animate.set_value(0.60),
            run_time=1.4,
            rate_func=linear,
        )
        world.tissue_lab = gut_lab
        world.tile = cl_tile

        self.at("The toxin")
        self.play(FadeIn(toxin), sw_t.animate.set_value(0.38), run_time=0.75, rate_func=linear)
        self.play(
            toxin.animate.move_to(world.off_arrows[1].get_center() + UP * 0.28),
            Indicate(world.gs.rect, color=PURPLE, scale_factor=1.08),
            sw_t.animate.set_value(0.24),
            run_time=1.35,
            rate_func=linear,
        )

        self.at("no longer cut")
        cracked = cracked_arrow_shape(world.off_arrows[1], color=GREY)
        broken_lbl = T("OFF arm broken", size=26, color=RED).move_to([3.25, world.gs.get_y() - 0.12, 0], aligned_edge=LEFT)
        self.play(
            ReplacementTransform(world.off_arrows[1], cracked),
            FadeIn(broken_lbl),
            run_time=0.7,
        )
        world.off_arrows[1] = cracked

        self.at("locked on")
        set_lamp_state(world.gs, 1.0)
        padlock = make_padlock(scale=0.95, color=GOLD).next_to(world.gs.rect, UL, buff=0.10)
        locked_lbl = T("locked ON", size=26, color=GOLD).move_to([-3.25, world.gs.get_y(), 0], aligned_edge=RIGHT)
        self.play(FadeIn(padlock), FadeIn(locked_lbl), run_time=0.6)

        self.at("Cyclic AMP")
        set_lamp_state(world.cyclase, 1.0)
        set_lamp_state(world.pka, 1.0)
        phase = ValueTracker(0.0)
        camp_pour = make_particle_stream(
            world.cyclase.rect.get_bottom() + DOWN * 0.06,
            world.pka.rect.get_top() + UP * 0.06,
            phase,
            count=10,
            color=GOLD,
            radius=0.08,
            spread=0.45,
            seed=43,
        )
        self.add(camp_pour)
        self.play(phase.animate.set_value(0.9), run_time=0.9, rate_func=linear)

        self.at("chloride and water")
        cyan_pour = make_particle_stream(
            world.tile.rect.get_bottom() + DOWN * 0.04,
            [0.0, -2.52, 0],
            phase,
            count=16,
            color=CYAN,
            radius=0.085,
            spread=0.8,
            seed=47,
        )
        pool_h = ValueTracker(0.08)
        pool = always_redraw(
            lambda: RoundedRectangle(
                corner_radius=0.18,
                width=2.2 + 3.6 * min(1.0, pool_h.get_value()),
                height=0.22 + 0.36 * min(1.0, pool_h.get_value()),
                stroke_color=CYAN,
                stroke_width=2.8,
                fill_color=CYAN,
                fill_opacity=0.45,
            ).move_to([0.0, -2.78, 0])
        )
        pool_lbl = T("into intestine", size=26, color=CYAN).move_to([0.0, -3.32, 0])
        self.add(cyan_pour, pool, pool_lbl)

        rem = max(0.2, self.narration_s + TAIL - self.elapsed())
        self.play(
            pool_h.animate.set_value(1.0),
            phase.animate.set_value(0.9 + rem * 1.25),
            run_time=rem,
            rate_func=linear,
        )
        self.finish()


def _s07_world_state(mutant=True, open_amt=1.0, mid_glow=False, show_question=True):
    """Shared builder for the end of s07_predict, s08_pause backdrop, and s09_answer start."""
    tag = scope_tag("schematic", size=24, color=TEXT)
    cyto = make_cytoplasm_backdrop(width=12.6, top_y=2.92, bot_y=-3.05, x_center=0.0)
    rec = make_lamp("receptor", width=2.25, height=0.52, size=26, on=False).move_to([0.0, 2.45, 0])
    gs = make_lamp("Gs alpha", width=2.25, height=0.52, size=26, on=False).move_to([0.0, 1.66, 0])
    cyc = make_lamp("cyclase", width=2.25, height=0.52, size=26, on=False).move_to([0.0, 0.87, 0])
    off_rec = make_off_arrow(rec, length=0.85, buff=0.12, stroke_width=6.0)
    off_gs = make_off_arrow(gs, length=0.85, buff=0.12, stroke_width=6.0)
    off_cyc = make_off_arrow(cyc, length=0.85, buff=0.12, stroke_width=6.0)
    pka_on = Arrow([-4.05, -0.55, 0], [-2.65, -0.55, 0], buff=0, color=GREEN, stroke_width=6.0, tip_length=0.22)

    pka = make_pka_assembly(center=(0.0, -0.55, 0.0), open_amt=open_amt, shape_mutant=mutant, lit=False)
    if mid_glow:
        pka.core.shape.set_fill(ManimColor("#767D8A"), opacity=0.94)
        pka.core.shape.set_stroke(TEXT, width=2.8)

    tile = make_output_tile("cortisol", color=GOLD, width=2.45, height=0.52, size=26).move_to([0.0, -2.42, 0])
    cell_lbl = T("adrenal cell", size=28, color=TEXT).move_to([-5.6, 2.45, 0], aligned_edge=LEFT)
    cush_lbl = T("Cushing's (some cases)", size=24, color=GOLD).move_to([2.35, 2.45, 0], aligned_edge=LEFT)
    g = VGroup(cyto, rec, gs, cyc, off_rec, off_gs, off_cyc, pka_on, pka, tile, cell_lbl, cush_lbl, tag)
    if show_question:
        q = T("No cyclic AMP: ON or OFF?", size=34, color=TEXT, weight=BOLD).move_to([0.0, 3.30, 0])
        g.add(q)
        g.question = q
    g.cyto = cyto
    g.rec, g.gs, g.cyc = rec, gs, cyc
    g.off_arrows = VGroup(off_rec, off_gs, off_cyc)
    g.pka_on = pka_on
    g.pka = pka
    g.tile = tile
    g.cell_lbl = cell_lbl
    g.cush_lbl = cush_lbl
    g.tag = tag
    return g


class S07Predict(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", size=24, color=TEXT)
        cyto = make_cytoplasm_backdrop(width=12.6, top_y=2.92, bot_y=-3.05, x_center=0.0)
        rec = make_lamp("receptor", width=2.25, height=0.52, size=26, on=False).move_to([0.0, 2.45, 0])
        gs = make_lamp("Gs alpha", width=2.25, height=0.52, size=26, on=False).move_to([0.0, 1.66, 0])
        cyc = make_lamp("cyclase", width=2.25, height=0.52, size=26, on=False).move_to([0.0, 0.87, 0])
        off_rec = make_off_arrow(rec, length=0.85, buff=0.12, stroke_width=6.0)
        off_gs = make_off_arrow(gs, length=0.85, buff=0.12, stroke_width=6.0)
        off_cyc = make_off_arrow(cyc, length=0.85, buff=0.12, stroke_width=6.0)
        pka_on = Arrow([-4.05, -0.55, 0], [-2.65, -0.55, 0], buff=0, color=GREEN, stroke_width=6.0, tip_length=0.22)
        pka = make_pka_assembly(center=(0.0, -0.55, 0.0), open_amt=0.0, shape_mutant=False, lit=False)
        tile = make_output_tile("glucose", color=PALE_BLUE, width=2.45, height=0.52, size=26).move_to([0.0, -2.42, 0])
        cell_lbl = T("liver cell", size=28, color=TEXT).move_to([-5.6, 2.45, 0], aligned_edge=LEFT)

        grp = VGroup(rec, gs, cyc, off_rec, off_gs, off_cyc, pka_on, pka, tile)
        grp.save_state()
        grp.scale(0.90)
        self.add(cyto, grp, cell_lbl, tag)
        self.play(grp.animate.restore(), run_time=1.4)

        self.at("PKA sits clamped")
        self.play(
            pka.left_b.animate.shift(RIGHT * 0.08),
            pka.right_b.animate.shift(LEFT * 0.08),
            Indicate(pka.left_b, color=TEAL, scale_factor=1.16),
            Indicate(pka.right_b, color=TEAL, scale_factor=1.16),
            run_time=1.1,
        )
        self.play(
            pka.left_b.animate.shift(LEFT * 0.08),
            pka.right_b.animate.shift(RIGHT * 0.08),
            run_time=0.5,
        )

        self.at("until cyclic AMP")
        camp_dots = VGroup(
            Dot([-2.7, 0.35, 0], radius=0.12, color=GOLD),
            Dot([-2.1, 0.55, 0], radius=0.12, color=GOLD),
            Dot([2.1, 0.55, 0], radius=0.12, color=GOLD),
            Dot([2.7, 0.35, 0], radius=0.12, color=GOLD),
        )
        targets = [
            pka.left_b.get_top() + UP * 0.14 + LEFT * 0.1,
            pka.left_b.get_top() + UP * 0.14 + RIGHT * 0.12,
            pka.right_b.get_top() + UP * 0.14 + LEFT * 0.12,
            pka.right_b.get_top() + UP * 0.14 + RIGHT * 0.1,
        ]
        pka_open = make_pka_assembly(center=(0.0, -0.55, 0.0), open_amt=1.0, shape_mutant=False, lit=True)
        self.play(
            FadeIn(camp_dots),
            *[d.animate.move_to(t) for d, t in zip(camp_dots, targets)],
            run_time=0.8,
        )
        self.play(
            pka.left_b.animate.shift(LEFT * 0.60),
            pka.right_b.animate.shift(RIGHT * 0.60),
            pka.clamp_lab.animate.shift(LEFT * 0.60),
            Transform(pka.core, pka_open.core),
            run_time=0.85,
        )
        pka_closed = make_pka_assembly(center=(0.0, -0.55, 0.0), open_amt=0.0, shape_mutant=False, lit=False)
        self.play(
            FadeOut(camp_dots),
            pka.left_b.animate.shift(RIGHT * 0.60),
            pka.right_b.animate.shift(LEFT * 0.60),
            pka.clamp_lab.animate.shift(RIGHT * 0.60),
            Transform(pka.core, pka_closed.core),
            run_time=0.85,
        )

        self.at("Cushing")
        adr_lbl = T("adrenal cell", size=28, color=TEXT).move_to([-5.6, 2.45, 0], aligned_edge=LEFT)
        cort_tile = make_output_tile("cortisol", color=GOLD, width=2.45, height=0.52, size=26).move_to([0.0, -2.42, 0])
        cush_lbl = T("Cushing's (some cases)", size=24, color=GOLD).move_to([2.35, 2.45, 0], aligned_edge=LEFT)
        self.play(
            swap(cell_lbl, adr_lbl, run_time=0.55),
            ReplacementTransform(tile, cort_tile),
            FadeIn(cush_lbl),
            run_time=0.75,
        )

        self.at("cannot bind")
        pka_mut = make_pka_assembly(center=(0.0, -0.55, 0.0), open_amt=1.0, shape_mutant=True, lit=False)
        pka_mut.core.shape.set_fill(ManimColor("#767D8A"), opacity=0.94)
        pka_mut.core.shape.set_stroke(TEXT, width=2.8)
        self.play(
            pka.left_b.animate.shift(LEFT * 0.60),
            pka.right_b.animate.shift(RIGHT * 0.60),
            pka.clamp_lab.animate.shift(LEFT * 0.60),
            ReplacementTransform(pka.core, pka_mut.core),
            run_time=0.95,
        )

        # Residual cAMP dots drain completely away while RED OFF arrows pulse intact
        drain_dots = VGroup(*[Dot([-2.5 + i * 1.0, 0.35, 0], radius=0.085, color=GOLD) for i in range(6)])
        self.add(drain_dots)
        self.at("Every off enzyme")
        for arr in (off_rec, off_gs, off_cyc):
            self.play(Indicate(arr, color=RED, scale_factor=1.28), drain_dots.animate.shift(RIGHT * 0.6).set_opacity(0.45), run_time=0.65)

        self.at("With no cyclic")
        q = T("No cyclic AMP: ON or OFF?", size=34, color=TEXT, weight=BOLD).move_to([0.0, 3.30, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), drain_dots.animate.shift(RIGHT * 1.2).set_opacity(0.0), run_time=1.0)
        self.remove(drain_dots)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "No cyclic AMP: ON or OFF?"
    CARD = {"y": 3.30, "color": TEXT, "size": 34, "max_w": 11.0}
    RING_AT = (5.8, -2.4, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _s07_world_state(mutant=True, open_amt=1.0, mid_glow=True, show_question=False)


class S09Answer(SpokenScene):
    def construct(self):
        st = _s07_world_state(mutant=True, open_amt=1.0, mid_glow=True, show_question=True)
        self.add(st)

        on_banner = T("ON", size=44, color=TEXT, weight=BOLD).move_to([0.0, 3.30, 0])
        pka_lit = make_pka_assembly(center=(0.0, -0.55, 0.0), open_amt=1.0, shape_mutant=True, lit=True)
        self.play(
            swap(st.question, on_banner, run_time=0.45),
            Transform(st.pka.core, pka_lit.core),
            run_time=0.6,
        )

        self.at("escapes its clamp")
        self.play(st.pka.core.animate.move_to([3.0, -0.55, 0]), run_time=0.95)

        self.at("cortisol production")
        no_hormone = T("no hormone", size=26, color=ORANGE).next_to(st.rec.rect, LEFT, buff=0.24)
        phase = ValueTracker(0.0)
        cort_stream = make_particle_stream(
            st.tile.rect.get_bottom() + DOWN * 0.04,
            [0.0, -3.68, 0],
            phase,
            count=20,
            color=WHITE,
            radius=0.095,
            spread=1.35,
            seed=53,
        )
        self.add(cort_stream)
        self.play(
            FadeIn(no_hormone),
            st.tile.rect.animate.set_stroke(WHITE, width=4.0),
            phase.animate.set_value(1.5),
            run_time=1.3,
            rate_func=linear,
        )

        self.at("Nothing is wrong")
        for arr in st.off_arrows:
            self.play(
                Indicate(arr, color=RED, scale_factor=1.3),
                phase.animate.increment_value(0.85),
                run_time=0.8,
                rate_func=linear,
            )

        self.at("no longer needs")
        self.play(
            st.pka_on.animate.set_opacity(0.2),
            phase.animate.increment_value(1.1),
            run_time=1.0,
            rate_func=linear,
        )
        rem = max(0.1, self.narration_s + TAIL - self.elapsed())
        self.play(phase.animate.increment_value(rem * 1.25), run_time=rem, rate_func=linear)
        self.finish()


class S10WaysToStick(SpokenScene):
    def construct(self):
        world = build_cell_world(x_center=2.6, tissue="liver cell", output="glucose", output_color=PALE_BLUE, cell_w=5.8)
        set_lamp_state(world.gs, 1.0)
        set_lamp_state(world.pka, 1.0)
        tag = scope_tag("schematic", size=24, color=TEXT)
        world.save_state()
        world.shift(LEFT * 1.8)
        self.add(world, tag)
        # Pull back smoothly to right-aligned full cell so left column opens for 3 failure icons
        self.play(world.animate.restore(), run_time=1.3)

        i1_arr = Arrow([-5.0, 2.05, 0], [-5.9, 2.05, 0], buff=0, color=RED, stroke_width=4.8, tip_length=0.18)
        i1_crack = cracked_arrow_shape(i1_arr, color=GREY)
        i1_lbl = T("lost OFF arm", size=28, color=RED).next_to(i1_crack, RIGHT, buff=0.25)
        icon1 = VGroup(i1_crack, i1_lbl)

        i2_lamp = make_lamp("ON", width=0.95, height=0.5, size=24, on=True).move_to([-5.0, 0.45, 0])
        i2_on = make_on_arrow(i2_lamp, length=0.75, buff=0.1, stroke_width=4.2).set_opacity(0.22)
        i2_lbl = T("needs no ON signal", size=28, color=GOLD).next_to(i2_lamp, RIGHT, buff=0.25)
        icon2 = VGroup(i2_on, i2_lamp, i2_lbl)

        i3_lamp = make_lamp("dim", width=0.95, height=0.5, size=24, on=False).move_to([-4.8, -1.25, 0])
        set_lamp_state(i3_lamp, 0.15)
        i3_on = Arrow([-6.05, -1.25, 0], [-5.35, -1.25, 0], buff=0, color=GREEN, stroke_width=2.2, tip_length=0.14).set_opacity(0.45)
        i3_off = Arrow([-3.35, -1.25, 0], [-4.22, -1.25, 0], buff=0, color=RED, stroke_width=7.5, tip_length=0.24)
        i3_lbl = T("weak ON arm", size=28, color=TEAL).move_to([-4.6, -0.60, 0])
        i3_tag = T("insulin resistance", size=24, color=TEXT).move_to([-3.8, -2.15, 0], aligned_edge=LEFT)
        i3_little = T("too little", size=24, color=PALE_BLUE).move_to([-4.8, -3.05, 0])

        phase = ValueTracker(0.0)
        phase.add_updater(lambda m, dt: m.increment_value(dt * 0.9))
        self.add(phase)
        trickle = make_particle_stream(
            i3_lamp.rect.get_bottom() + DOWN * 0.06,
            [-4.8, -2.72, 0],
            phase,
            count=5,
            color=PALE_BLUE,
            radius=0.065,
            spread=0.12,
            seed=61,
        )
        stuck_gluc = make_particle_stream(
            world.tile.rect.get_bottom() + DOWN * 0.02,
            [world.x_center, world.bot_y + 0.02, 0],
            phase,
            count=16,
            color=PALE_BLUE,
            radius=0.085,
            spread=1.6,
            seed=67,
        )
        self.add(stuck_gluc)

        self.at("loses its off")
        cracked_gs = cracked_arrow_shape(world.off_arrows[1], color=GREY)
        self.play(
            ReplacementTransform(world.off_arrows[1], cracked_gs),
            FadeIn(icon1, shift=RIGHT * 0.15),
            run_time=0.55,
        )
        world.off_arrows[1] = cracked_gs

        self.at("stops needing")
        self.play(
            world.on_arrows[3].animate.set_opacity(0.22),
            FadeIn(icon2, shift=RIGHT * 0.15),
            run_time=0.55,
        )

        self.at("tip the other")
        self.play(
            FadeIn(i3_lamp),
            FadeIn(i3_on),
            FadeIn(i3_off),
            run_time=0.8,
        )

        self.at("Weaken an")
        self.add(trickle)
        self.play(FadeIn(i3_lbl), run_time=0.85)

        self.at("insulin resistance")
        self.play(FadeIn(i3_tag), run_time=0.85)

        self.at("too small")
        self.play(FadeIn(i3_little), run_time=0.65)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        world = build_cell_world(x_center=-2.2, tissue="liver cell", output="glucose", output_color=PALE_BLUE, cell_w=5.2)
        for lp in world.lamps:
            set_lamp_state(lp, 1.0)
        epi = make_epinephrine().move_to(world.receptor.rect.get_top() + UP * 0.23)
        tag = scope_tag("schematic", size=24, color=TEXT)
        phase = ValueTracker(0.0)
        camp_pour = make_particle_stream(
            world.cyclase.rect.get_bottom() + DOWN * 0.06,
            world.pka.rect.get_top() + UP * 0.06,
            phase,
            count=10,
            color=GOLD,
            radius=0.08,
            spread=0.4,
            seed=71,
        )
        gluc_pour = make_particle_stream(
            world.tile.rect.get_bottom() + DOWN * 0.04,
            [world.x_center, world.bot_y + 0.04, 0],
            phase,
            count=14,
            color=PALE_BLUE,
            radius=0.075,
            spread=0.85,
            seed=73,
        )
        self.add(world, epi, camp_pour, gluc_pour, tag)

        self.at("the off")
        self.play(*[Indicate(a, color=RED, scale_factor=1.24) for a in world.off_arrows],
                  phase.animate.increment_value(0.9), run_time=0.85, rate_func=linear)

        self.at("how big")
        rt_box = RoundedRectangle(corner_radius=0.16, width=3.7, height=1.8, stroke_color=WHITE, stroke_width=3.2,
                                  fill_color=CELL_FILL, fill_opacity=0.95).move_to([4.3, 0.2, 0])
        rt_title = T("running total", size=28, color=GOLD).move_to([4.3, 0.7, 0])
        rt_val = T("tens of millions", size=30, color=PALE_BLUE, weight=BOLD).move_to([4.3, -0.1, 0])
        self.play(FadeIn(rt_box), FadeIn(rt_title), FadeIn(rt_val),
                  phase.animate.increment_value(0.7), run_time=0.65, rate_func=linear)

        self.at("how long")
        on_bars = VGroup(*[
            Rectangle(width=w, height=0.22, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([0.65 + w / 2, lp.get_y(), 0])
            for lp, w in zip(world.lamps, [0.42, 0.68, 0.52, 0.90])
        ])
        bar_lbl = T("ON time", size=24, color=TEXT).next_to(on_bars[0], UP, buff=0.14)
        self.play(FadeIn(on_bars), FadeIn(bar_lbl), phase.animate.increment_value(0.8), run_time=0.75, rate_func=linear)

        self.at("When one fails")
        cracked = cracked_arrow_shape(world.off_arrows[1], color=GREY)
        self.play(
            ReplacementTransform(world.off_arrows[1], cracked),
            epi.animate.shift(UP * 1.4).set_opacity(0.0),
            phase.animate.increment_value(0.9),
            run_time=0.75,
            rate_func=linear,
        )
        self.remove(epi)
        set_lamp_state(world.receptor, 0.0)
        rem = max(0.1, self.narration_s + TAIL - self.elapsed())
        self.play(phase.animate.increment_value(rem * 1.25), run_time=rem, rate_func=linear)
        self.finish()


class S12End(EndCard):
    LINE = "Every switch is a contest: the OFF arm sets size and duration."
