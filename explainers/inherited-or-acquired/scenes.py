"""
What Can Cross a Generation? — STEMhop Explainer Film ("Inherited or Acquired?")

COLOUR MAP (one colour per concept for the entire film):
- Genes and alleles:       BLUE  (#58C4DD) — gene cards, allele variants
- Environment:             GREEN (#83C167) — environment ring, soil, food, soil arrows
- Acquired body changes:   GOLD  (#D4A843) — scar, dyed hair, piano skill, exercise muscle, body ripples
- Routes to offspring:     TEAL  (#3FB8C0) — inherited path, sex-cell chamber & gate, seed route
- Stopped routes:          RED   (#FC6255) — blocked body-cell gate & stop bar
- Other structures / text: GREY  (#8B93A1) / TEXT (#E8EAF0)
- Schematic flower states: #D8DCE6 (neutral), #5B9BD5 (acidic-soil blue), #E87EA1 (less-acidic-soil pink)

ONE PICTURE OF THE WORLD CARRIED SCENE TO SCENE:
- Scenes s00–s06: A large grey parent mouse on the left with a gold scar and blue gene cards inside,
  linked across routes/gates to an unmarked young mouse on the right (zooming into the parent's
  skin, muscle, and sex cells in s03–s06).
- Scenes s07–s10: The blue gene cards remain in place as the world transforms into a plant cutting
  with leaves, roots, soil, environment ring, and schematic flower cluster, splitting into matching
  bigleaf hydrangea cuttings and tracing soil-to-flower vs gene-to-offspring routes.

WHAT CHANGES ON SCREEN IN EACH SPOKEN SCENE (and what it is computed from):
- s00_hook:        A gold scar grows across the parent's skin along a curved seam, then blue gene cards
                   stream along a computed Bezier trajectory toward the question mark before the young mouse.
- s02_two_sources: The question mark transforms into an upper teal inherited path (carrying gene cards to
                   the young) and a lower gold acquired loop inside the parent; the lower-path icon morphs
                   in place through scar, dyed hair, piano keys, and flexing muscle.
- s03_cell_map:    The parent zooms into skin, muscle, and sex-cell compartments; teal arrows extend from
                   sex cells to the young mouse while computed radial gold ripples expand inside skin and
                   muscle and stop at the compartment boundary.
- s04_predict:     A gold scar icon and a blue gene card advance along extending tracks to pause beside two
                   neutral grey gates under the question "Which path reaches the young?".
- s06_reveal:      The sex-cell gate opens in teal as blue gene cards travel through it to settle in the
                   young mouse, while the body-cell gate turns red and stops advancing gold scar tokens.
- s07_environment: The mouse map transforms around the stationary blue gene cards into a plant cutting,
                   building a green environment ring as soil rises, light rays extend, water droplets fall,
                   food appears, and a thermometer gauge rises to shape the flower phenotype.
- s08_variation:   Four neighboring plants grow from the central cutting; allele cards vary on the left and
                   environment rings vary on the right, shifting computed flower heights and colors before
                   genes-only and environment-only boxes slide away for overlapping blue and green circles.
- s09_hydrangea:   The plant splits into two matching cuttings with identical unchanged blue gene cards;
                   left soil acidifies as aluminum dots rise through roots to turn the left flower blue,
                   while right soil turns less acidic and its flower shifts pink.
- s10_scope:       A row of schematic possible flower colors appears above the gene cards as a green soil
                   arrow selects between them; both matching cuttings return to trace green soil arrows
                   ending at flowers and a teal gene route reaching seed offspring.
"""

from bp_parts import *


# ------------------------------------------------------------------ house colors & constants
HYD_NEUTRAL = "#D8DCE6"
HYD_BLUE = "#5B9BD5"
HYD_PINK = "#E87EA1"
HYD_MID = "#9B7EC8"
SOIL_ACID = "#4CA87A"
SOIL_LESS = "#8EA85A"


def corner_hex():
    """Small STEMhop Hex mark in the top-right safe corner."""
    h = hex_mascot(0.44)
    h.move_to([6.15, 3.35, 0])
    h.set_z_index(20)
    return h


# ------------------------------------------------------------------ modular subject builders
def gene_card(variant=0, scale=1.0, fill_opacity=0.42):
    """Rounded BLUE gene card with internal locus bars (not a molecular structure)."""
    w, h = 0.52 * scale, 0.72 * scale
    card = RoundedRectangle(
        corner_radius=0.08 * scale,
        width=w,
        height=h,
        stroke_color=BLUE,
        stroke_width=3.0,
        fill_color=BLUE,
        fill_opacity=fill_opacity,
    )
    bar_specs = [
        [(0.17, 0.28), (-0.01, 0.34), (-0.18, 0.22)],
        [(0.17, 0.16), (-0.01, 0.20), (-0.18, 0.36)],
        [(0.17, 0.32), (-0.01, 0.14), (-0.18, 0.30)],
    ][variant % 3]
    bars = VGroup()
    for y_off, bw in bar_specs:
        bars.add(
            Line(
                [-bw * scale * 0.5, y_off * scale, 0],
                [bw * scale * 0.5, y_off * scale, 0],
                color=TEXT,
                stroke_width=3.2 * scale,
            )
        )
    return VGroup(card, bars)


def gene_card_cluster(n=3, variant=0, scale=0.88, buff=0.10):
    """A small horizontal row of blue gene cards."""
    cards = VGroup(*[gene_card((variant + i) % 3, scale=scale) for i in range(n)])
    cards.arrange(RIGHT, buff=buff * scale)
    return cards


def scar_mark(scale=1.0):
    """Gold scar: curved seam with cross-stitches."""
    pts = [
        np.array([-0.55, 0.12, 0]) * scale,
        np.array([-0.18, 0.22, 0]) * scale,
        np.array([0.18, 0.08, 0]) * scale,
        np.array([0.55, 0.18, 0]) * scale,
    ]
    seam = VMobject(color=GOLD, stroke_width=6.5 * scale)
    seam.set_points_smoothly(pts)
    stitches = VGroup()
    for x, y, tilt in [(-0.34, 0.17, 0.35), (-0.05, 0.16, -0.25), (0.24, 0.12, 0.3), (0.42, 0.16, -0.2)]:
        dx = 0.09 * scale * np.sin(tilt)
        dy = 0.14 * scale * np.cos(tilt)
        c = np.array([x * scale, y * scale, 0])
        stitches.add(Line(c + np.array([-dx, -dy, 0]), c + np.array([dx, dy, 0]), color=GOLD, stroke_width=4.0 * scale))
    return VGroup(seam, stitches)


def mouse_silhouette(scale=1.0, facing=RIGHT, color=GREY, fill_opacity=0.30):
    """Clean, recognizable mouse drawing made from smooth vector curves."""
    body = Ellipse(width=2.65, height=1.60, color=color, stroke_width=4.0, fill_color=color, fill_opacity=fill_opacity)
    head = Polygon(
        [0.95, 0.42, 0],
        [1.55, 0.35, 0],
        [2.05, -0.05, 0],
        [1.55, -0.45, 0],
        [0.95, -0.48, 0],
        color=color,
        stroke_width=3.6,
        fill_color=color,
        fill_opacity=fill_opacity + 0.04,
    ).round_corners(0.18)
    ear = Circle(radius=0.36, color=color, stroke_width=3.6, fill_color=color, fill_opacity=fill_opacity + 0.08).move_to([1.08, 0.68, 0])
    inner_ear = Circle(radius=0.18, color=color, stroke_width=2.4, fill_color=BG, fill_opacity=0.55).move_to([1.08, 0.66, 0])
    eye = Dot([1.50, 0.12, 0], radius=0.075, color=TEXT)
    nose = Dot([2.03, -0.05, 0], radius=0.07, color=TEXT)
    whiskers = VGroup(
        Line([1.88, -0.02, 0], [2.32, 0.14, 0], color=color, stroke_width=2.2),
        Line([1.88, -0.09, 0], [2.32, -0.18, 0], color=color, stroke_width=2.2),
    )
    leg1 = RoundedRectangle(corner_radius=0.1, width=0.48, height=0.34, color=color, stroke_width=3.2, fill_color=color, fill_opacity=fill_opacity).move_to([-0.68, -0.80, 0])
    leg2 = RoundedRectangle(corner_radius=0.1, width=0.48, height=0.34, color=color, stroke_width=3.2, fill_color=color, fill_opacity=fill_opacity).move_to([0.65, -0.80, 0])
    tail = VMobject(color=color, stroke_width=5.0)
    tail.set_points_smoothly([[-1.25, -0.10, 0], [-1.85, -0.35, 0], [-2.25, 0.10, 0], [-2.55, 0.45, 0]])
    g = VGroup(tail, leg1, leg2, body, head, ear, inner_ear, eye, nose, whiskers)
    if np.allclose(facing, LEFT):
        g.flip(UP)
    g.scale(scale)
    return g


def eye_icon(scale=1.0):
    """Simple eye cartoon for inherited trait example (no extra labels)."""
    top = ArcBetweenPoints([-0.55, 0, 0], [0.55, 0, 0], angle=-1.35, color=TEXT, stroke_width=3.6)
    bot = ArcBetweenPoints([-0.55, 0, 0], [0.55, 0, 0], angle=1.35, color=TEXT, stroke_width=3.6)
    iris = Circle(radius=0.22, color=BLUE, stroke_width=3, fill_color=TEAL, fill_opacity=0.78)
    pupil = Dot(ORIGIN, radius=0.09, color=BG)
    glint = Dot([0.07, 0.07, 0], radius=0.03, color=TEXT)
    return VGroup(top, bot, iris, pupil, glint).scale(scale)


def dyed_hair_icon(scale=1.0):
    """Head silhouette with a gold dyed streak (no extra labels)."""
    head = Circle(radius=0.36, color=GREY, stroke_width=3.4, fill_color=GREY, fill_opacity=0.26).shift(DOWN * 0.08)
    hair = Arc(radius=0.42, start_angle=0.15, angle=PI - 0.3, arc_center=[0, -0.05, 0], color=GREY, stroke_width=9)
    streak = Arc(radius=0.43, start_angle=0.45, angle=1.15, arc_center=[0, -0.05, 0], color=GOLD, stroke_width=10)
    return VGroup(head, hair, streak).scale(scale)


def piano_keys_icon(scale=1.0):
    """Small piano keyboard with a gold pressed key (no extra labels)."""
    keys = VGroup()
    for i in range(4):
        fill_c = GOLD if i == 2 else TEXT
        fill_op = 0.88 if i == 2 else 0.24
        keys.add(
            Rectangle(width=0.26, height=0.68, stroke_color=TEXT, stroke_width=2.5, fill_color=fill_c, fill_opacity=fill_op)
            .move_to([(i - 1.5) * 0.27, 0, 0])
        )
    sharps = VGroup()
    for idx in (-1, 0, 1):
        sharps.add(
            Rectangle(width=0.15, height=0.40, stroke_color=BG, stroke_width=1.5, fill_color=BG, fill_opacity=0.95)
            .move_to([idx * 0.27, 0.14, 0])
        )
    return VGroup(keys, sharps).scale(scale)


def muscle_icon(scale=1.0):
    """Flexed arm silhouette with clear gold bicep bulge (no extra labels)."""
    arm_pts = [
        [-0.48, -0.22, 0],
        [-0.22, -0.28, 0],
        [0.24, -0.24, 0],
        [0.44, 0.18, 0],
        [0.34, 0.44, 0],
        [0.14, 0.42, 0],
        [0.18, 0.08, 0],
        [-0.02, 0.18, 0],
        [-0.32, 0.08, 0],
    ]
    arm = Polygon(*arm_pts, color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.40).round_corners(0.14)
    bicep = ArcBetweenPoints([-0.30, 0.04, 0], [0.12, 0.06, 0], angle=-1.35, color=GOLD, stroke_width=4.8)
    return VGroup(arm, bicep).scale(scale)


def build_cell_map(show_young=True, show_arrows=False):
    """Shared parent cell map + young mouse builder for s03, s04, s05, s06.

    Coordinates are fixed so carried scenes match pixel-for-pixel:
    - Parent outer contour centered at (-3.1, 0.0), width 6.0, height 5.4
    - Sex-cell gene cards centered at (-1.25, -0.45) (preserved into s07!)
    - Young mouse at (4.85, -0.25)
    """
    outer = Ellipse(width=6.0, height=5.4, color=GREY, stroke_width=4.2, fill_color=GREY, fill_opacity=0.22).move_to([-3.1, 0.0, 0])

    # Skin cells (top-left inside parent)
    skin_cells = VGroup()
    for cx, cy in [(-4.35, 1.55), (-3.55, 1.72), (-2.75, 1.55), (-3.95, 1.12), (-3.15, 1.12)]:
        skin_cells.add(RoundedRectangle(corner_radius=0.12, width=0.74, height=0.42, color=GREY, stroke_width=2.8, fill_color=GREY, fill_opacity=0.30).move_to([cx, cy, 0]))
    scar = scar_mark(0.95).move_to([-3.55, 2.02, 0])
    skin_lbl = T("skin cells", size=26, color=GOLD).move_to([-3.65, 0.58, 0])

    # Muscle cells (bottom-left inside parent)
    muscle_cells = VGroup()
    for dy in (-0.30, 0.0, 0.30):
        muscle_cells.add(Ellipse(width=2.05, height=0.28, color=GREY, stroke_width=2.8, fill_color=GOLD, fill_opacity=0.26).move_to([-3.75, -1.05 + dy, 0]))
    muscle_patch = Ellipse(width=1.18, height=0.50, color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.45).move_to([-3.75, -1.05, 0])
    muscle_lbl = T("muscle cells", size=26, color=GOLD).move_to([-3.75, -1.92, 0])

    # Barrier separating body cells from sex cells
    barrier = DashedLine([-2.22, 1.45, 0], [-2.22, -1.75, 0], color=GREY, stroke_width=3.2, dash_length=0.14)

    # Sex-cell chamber (right side of parent)
    sex_chamber = Ellipse(width=2.05, height=2.15, color=TEAL, stroke_width=3.8, fill_color=TEAL, fill_opacity=0.24).move_to([-1.25, -0.45, 0])
    cards = gene_card_cluster(n=3, variant=0, scale=0.72, buff=0.07).move_to([-1.25, -0.45, 0])
    sex_lbl = T("sex cells", size=26, color=TEAL).move_to([-1.25, 0.92, 0])

    parent_group = VGroup(outer, skin_cells, scar, skin_lbl, muscle_cells, muscle_patch, muscle_lbl, barrier, sex_chamber, cards, sex_lbl)

    young = mouse_silhouette(scale=0.68, facing=RIGHT, color=GREY, fill_opacity=0.30).move_to([4.85, -0.25, 0])

    arrows = VGroup()
    if show_arrows:
        a1 = Arrow([-0.18, -0.25, 0], [3.32, -0.20, 0], color=TEAL, stroke_width=6.0, buff=0.05, max_tip_length_to_length_ratio=0.12)
        a2 = Arrow([-0.18, -0.65, 0], [3.32, -0.50, 0], color=TEAL, stroke_width=5.0, buff=0.05, max_tip_length_to_length_ratio=0.12)
        arrows.add(a1, a2)

    return {
        "outer": outer,
        "skin_cells": skin_cells,
        "scar": scar,
        "skin_lbl": skin_lbl,
        "muscle_cells": muscle_cells,
        "muscle_patch": muscle_patch,
        "muscle_lbl": muscle_lbl,
        "barrier": barrier,
        "sex_chamber": sex_chamber,
        "cards": cards,
        "sex_lbl": sex_lbl,
        "parent": parent_group,
        "young": young,
        "arrows": arrows,
    }


def build_gate_tracks():
    """Tracks and neutral grey gates for s04, s05, s06."""
    upper_track = CubicBezier(
        [-2.38, 1.55, 0],
        [-0.10, 1.38, 0],
        [2.00, 0.96, 0],
        [3.55, 0.05, 0],
        color=GREY,
        stroke_width=4.5,
    )
    upper_gate_y = 0.80
    upper_gate_top = Line([1.85, upper_gate_y + 0.45, 0], [1.85, upper_gate_y + 0.15, 0], color=GREY, stroke_width=8)
    upper_gate_bot = Line([1.85, upper_gate_y - 0.15, 0], [1.85, upper_gate_y - 0.45, 0], color=GREY, stroke_width=8)
    upper_gate_bar = Line([1.85, upper_gate_y + 0.15, 0], [1.85, upper_gate_y - 0.15, 0], color=GREY, stroke_width=6)
    upper_gate = VGroup(upper_gate_top, upper_gate_bot, upper_gate_bar)

    lower_track = Line([-0.22, -0.45, 0], [3.55, -0.45, 0], color=GREY, stroke_width=4.5)
    lower_gate_top = Line([1.85, -0.02, 0], [1.85, -0.30, 0], color=GREY, stroke_width=8)
    lower_gate_bot = Line([1.85, -0.60, 0], [1.85, -0.88, 0], color=GREY, stroke_width=8)
    lower_gate_bar = Line([1.85, -0.30, 0], [1.85, -0.60, 0], color=GREY, stroke_width=6)
    lower_gate = VGroup(lower_gate_top, lower_gate_bot, lower_gate_bar)

    scar_token = scar_mark(0.84).move_to([1.05, 1.03, 0])
    card_token = gene_card(0, scale=0.80, fill_opacity=0.50).move_to([1.05, -0.45, 0])

    return {
        "upper_track": upper_track,
        "upper_gate": upper_gate,
        "upper_bar": upper_gate_bar,
        "upper_gate_y": upper_gate_y,
        "lower_track": lower_track,
        "lower_gate": lower_gate,
        "lower_bar": lower_gate_bar,
        "scar_token": scar_token,
        "card_token": card_token,
    }


def flower_corymb(center, radius=0.68, color=HYD_NEUTRAL):
    """Schematic hydrangea corymb cluster of florets."""
    g = VGroup()
    offsets = [
        (0.0, 0.0),
        (0.45, 0.14),
        (-0.45, 0.14),
        (0.26, 0.40),
        (-0.26, 0.40),
        (0.28, -0.26),
        (-0.28, -0.26),
        (0.0, 0.48),
    ]
    r = radius * 0.36
    for dx, dy in offsets:
        floret = VGroup()
        for ang in (0, PI / 2, PI, 3 * PI / 2):
            p = Circle(
                radius=r * 0.52,
                stroke_color=color,
                stroke_width=1.8,
                fill_color=color,
                fill_opacity=0.90,
            ).shift([r * 0.42 * np.cos(ang), r * 0.42 * np.sin(ang), 0])
            floret.add(p)
        floret.add(Dot(ORIGIN, radius=r * 0.16, color=BG))
        floret.move_to(np.array(center) + np.array([dx * radius, dy * radius, 0]))
        g.add(floret)
    return g


def build_plant(
    gene_pos=(-1.25, -0.45, 0),
    height_scale=1.0,
    flower_color=HYD_NEUTRAL,
    soil_color=GREEN,
    allele_variant=0,
    show_soil=True,
    show_cards=True,
):
    """Build a plant cutting centered horizontally on gene_pos[0] with gene cards at gene_pos."""
    gx, gy = gene_pos[0], gene_pos[1]
    s = height_scale

    soil_pts = [
        [gx - 1.52, gy - 1.88, 0],
        [gx - 1.30, gy - 1.24, 0],
        [gx + 1.30, gy - 1.24, 0],
        [gx + 1.52, gy - 1.88, 0],
    ]
    soil = Polygon(*soil_pts, color=soil_color, stroke_width=3.6, fill_color=soil_color, fill_opacity=0.46).round_corners(0.18)

    roots = VGroup()
    for dx0, dx1, dy in [(-0.08, -0.78, -1.66), (-0.03, -0.34, -1.72), (0.04, 0.36, -1.70), (0.09, 0.80, -1.62)]:
        r = VMobject(color="#B8C2D4", stroke_width=3.8)
        r.set_points_smoothly([
            [gx + dx0, gy - 0.92, 0],
            [gx + dx1 * 0.55, gy - 1.32, 0],
            [gx + dx1, gy + dy, 0],
        ])
        roots.add(r)

    stem_bot = Line([gx, gy - 0.95, 0], [gx, gy - 0.34, 0], color=GREEN, stroke_width=10)
    flower_y = gy + 2.30 * s
    stem_top = Line([gx, gy + 0.34, 0], [gx, flower_y - 0.20, 0], color=GREEN, stroke_width=10)

    leaves = VGroup()
    for side, ly in ((-1, gy + 0.75 * s), (1, gy + 0.92 * s), (-1, gy + 1.42 * s), (1, gy + 1.52 * s)):
        leaf = Ellipse(width=1.06 * min(1.1, 0.75 + 0.25 * s), height=0.46, color=GREEN, stroke_width=3.2, fill_color=GREEN, fill_opacity=0.46)
        leaf.rotate(side * (-0.38))
        leaf.move_to([gx + side * 0.56, ly, 0])
        leaves.add(leaf)

    node = Ellipse(width=1.84, height=0.76, color=TEAL, stroke_width=3.2, fill_color=BG, fill_opacity=0.92).move_to([gx, gy, 0])
    cards = gene_card_cluster(n=3, variant=allele_variant, scale=0.66, buff=0.07).move_to([gx, gy, 0])
    flower = flower_corymb([gx, flower_y, 0], radius=0.74 * (0.85 + 0.15 * s), color=flower_color)

    all_parts = VGroup()
    if show_soil:
        all_parts.add(soil)
    all_parts.add(roots, stem_bot, stem_top, leaves, node)
    if show_cards:
        all_parts.add(cards)
    all_parts.add(flower)

    return {
        "group": all_parts,
        "soil": soil,
        "roots": roots,
        "stem_bot": stem_bot,
        "stem_top": stem_top,
        "leaves": leaves,
        "node": node,
        "cards": cards,
        "flower": flower,
        "flower_y": flower_y,
        "gx": gx,
        "gy": gy,
    }


# ------------------------------------------------------------------ SCENE 00: HOOK
class S00Hook(SpokenScene):
    def construct(self):
        self.add(corner_hex())

        parent = mouse_silhouette(scale=1.45, facing=RIGHT, color=GREY, fill_opacity=0.32).move_to([-3.35, -0.20, 0])
        scar = scar_mark(1.25).move_to([-3.20, 0.80, 0])
        cards = gene_card_cluster(n=3, variant=0, scale=0.86, buff=0.10).move_to([-3.05, -0.38, 0])

        q_mark = T("?", size=124, color=GOLD, font=TITLE_FONT, weight=BOLD).move_to([1.65, 0.10, 0])
        young = mouse_silhouette(scale=0.76, facing=RIGHT, color=GREY, fill_opacity=0.32).move_to([4.50, -0.22, 0])

        # Beat 1: A parent can gain a scar.
        self.at("parent can gain")
        self.play(FadeIn(parent), run_time=0.8)
        self.play(Create(scar), FadeIn(cards, scale=0.9), run_time=1.8)

        # Beat 2: Why is a baby not born with that scar?
        self.at("baby not born")
        self.play(FadeIn(young, shift=LEFT * 0.35), FadeIn(q_mark, scale=0.85), run_time=1.8)
        scar_glow = Ellipse(width=1.8, height=0.75, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.22).move_to(scar)
        self.play(FadeIn(scar_glow), q_mark.animate.scale(1.14), rate_func=there_and_back, run_time=1.2)
        self.remove(scar_glow)

        # Beat 3: Follow the gold mark on the skin.
        self.at("follow the gold")
        skin_loop = ArcBetweenPoints([-2.4, 0.72, 0], [-0.85, 0.20, 0], angle=-0.5, color=GOLD, stroke_width=8)
        scar_probe = scar_mark(0.85).move_to([-2.4, 0.72, 0])
        probe_halo = Circle(radius=0.65, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.30).move_to([-2.4, 0.72, 0])
        self.play(Create(skin_loop), MoveAlongPath(VGroup(probe_halo, scar_probe), skin_loop), run_time=2.0)
        self.play(FadeOut(scar_probe), FadeOut(probe_halo), FadeOut(skin_loop), run_time=0.45)

        # Beat 4: Then follow the blue gene cards toward a young animal.
        self.at("follow the blue")
        stream_path = CubicBezier(
            [-2.2, -0.35, 0],
            [-0.9, -0.10, 0],
            [0.05, 0.05, 0],
            [0.72, 0.08, 0],
            color=TEAL,
            stroke_width=7.5,
        )
        travelers = [gene_card(i, scale=0.74, fill_opacity=0.62).move_to([-2.2, -0.35, 0]) for i in range(4)]
        self.play(Create(stream_path), run_time=0.55)
        self.play(
            LaggedStart(
                *[MoveAlongPath(c, stream_path, run_time=1.85) for c in travelers],
                lag_ratio=0.18,
            )
        )
        self.finish()


# ------------------------------------------------------------------ SCENE 01: TITLE CARD
class S01Title(TitleCard):
    LESSON = "Inherited or Acquired?"
    TITLE = "What Can Cross a Generation?"


# ------------------------------------------------------------------ SCENE 02: TWO SOURCES
class S02TwoSources(SpokenScene):
    def construct(self):
        self.add(corner_hex())

        parent = mouse_silhouette(scale=1.18, facing=RIGHT, color=GREY, fill_opacity=0.30).move_to([-3.95, -0.15, 0])
        scar_on_skin = scar_mark(1.0).move_to([-3.85, 0.68, 0])
        cards = gene_card_cluster(n=3, variant=0, scale=0.72, buff=0.07).move_to([-3.75, -0.30, 0])
        young = mouse_silhouette(scale=0.68, facing=RIGHT, color=GREY, fill_opacity=0.30).move_to([4.65, 1.15, 0])
        q_mark = T("?", size=104, color=GOLD, font=TITLE_FONT, weight=BOLD).move_to([0.65, 0.25, 0])

        self.add(parent, scar_on_skin, cards, young, q_mark)

        upper_curve = CubicBezier(
            [-2.75, -0.15, 0],
            [-0.85, 1.45, 0],
            [1.65, 1.45, 0],
            [3.25, 1.15, 0],
            color=TEAL,
            stroke_width=8.0,
        )
        upper_tip = Arrow([2.95, 1.20, 0], [3.55, 1.15, 0], color=TEAL, stroke_width=8.0, buff=0, max_tip_length_to_length_ratio=0.55)
        lbl_inherited = T("inherited", size=34, color=TEAL, weight=BOLD).move_to([0.45, 2.08, 0])

        lower_loop = ArcBetweenPoints([-3.65, -0.95, 0], [-1.35, -1.65, 0], angle=0.7, color=GOLD, stroke_width=8.0)
        lower_return = ArcBetweenPoints([-1.35, -1.65, 0], [-2.95, -1.35, 0], angle=0.5, color=GOLD, stroke_width=6.0)
        lbl_acquired = T("acquired", size=34, color=GOLD, weight=BOLD).move_to([-2.15, -2.55, 0])

        # Beat 1: An inherited trait passes from parent to offspring through genes.
        self.at("an inherited trait")
        movers = [gene_card(i, scale=0.70, fill_opacity=0.62).move_to([-2.75, -0.15, 0]) for i in range(2)]
        self.play(
            ReplacementTransform(q_mark, upper_curve),
            FadeIn(upper_tip),
            FadeIn(lbl_inherited, shift=UP * 0.1),
            run_time=1.4,
        )
        self.play(
            LaggedStart(*[MoveAlongPath(m, upper_curve, run_time=2.2) for m in movers], lag_ratio=0.35),
        )
        settled_card = gene_card(0, scale=0.62, fill_opacity=0.55).move_to([4.55, 1.12, 0])
        self.play(ReplacementTransform(VGroup(*movers), settled_card), run_time=0.7)

        # Beat 2: An acquired trait develops during life.
        self.at("an acquired trait")
        gold_tracer = Dot([-3.65, -0.95, 0], radius=0.14, color=GOLD)
        self.play(
            Create(lower_loop),
            Create(lower_return),
            FadeIn(lbl_acquired, shift=DOWN * 0.1),
            run_time=1.6,
        )
        self.play(
            Succession(MoveAlongPath(gold_tracer, lower_loop, run_time=0.9), MoveAlongPath(gold_tracer, lower_return, run_time=0.8)),
        )
        self.remove(gold_tracer)

        # Beat 3: Eye color is inherited.
        self.at("eye color")
        eye_halo = Circle(radius=0.72, color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.18).move_to([0.45, 0.35, 0])
        eye = eye_icon(1.38).move_to([0.45, 0.35, 0])
        self.play(FadeIn(eye_halo), FadeIn(eye, scale=0.85), run_time=1.8)

        # Beat 4-7: Small cartoons transform in place beside the lower path (no extra labels!)
        stage_pos = [0.65, -1.65, 0]
        stage_halo = Circle(radius=0.85, color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.16).move_to(stage_pos)
        cur_icon = scar_mark(1.30).move_to(stage_pos)

        self.at("a scar")
        self.play(FadeIn(stage_halo), FadeIn(cur_icon, scale=0.85), run_time=0.45)

        self.at("dyed hair")
        next_hair = dyed_hair_icon(1.45).move_to(stage_pos)
        self.play(ReplacementTransform(cur_icon, next_hair), run_time=0.7)
        cur_icon = next_hair

        self.at("a learned skill")
        next_piano = piano_keys_icon(1.40).move_to(stage_pos)
        self.play(ReplacementTransform(cur_icon, next_piano), run_time=0.7)
        cur_icon = next_piano

        self.at("exercise")
        next_muscle = muscle_icon(1.50).move_to(stage_pos)
        self.play(ReplacementTransform(cur_icon, next_muscle), run_time=1.1)
        self.play(
            next_muscle.animate.scale(1.18),
            stage_halo.animate.scale(1.14),
            rate_func=there_and_back,
            run_time=1.4,
        )

        # Beat 8-9: These labels describe where the characteristic comes from, not whether genes act alone.
        self.at("these labels describe")
        card_flow = gene_card(1, scale=0.64, fill_opacity=0.62).move_to([-2.75, -0.15, 0])
        self.play(
            lbl_inherited.animate.scale(1.14),
            lbl_acquired.animate.scale(1.14),
            MoveAlongPath(card_flow, upper_curve),
            run_time=2.4,
        )
        self.remove(card_flow)
        self.at("not whether genes")
        self.play(
            lbl_inherited.animate.scale(1 / 1.14),
            lbl_acquired.animate.scale(1 / 1.14),
            cards.animate.scale(1.16),
            rate_func=there_and_back,
            run_time=2.0,
        )
        self.finish()


# ------------------------------------------------------------------ SCENE 03: CELL MAP
class S03CellMap(SpokenScene):
    def construct(self):
        self.add(corner_hex())
        w = build_cell_map(show_young=True, show_arrows=True)

        small_parent = w["outer"].copy().scale(0.65).move_to([-3.95, -0.15, 0])
        small_cards = w["cards"].copy().move_to([-3.75, -0.30, 0])
        self.add(small_parent, small_cards, w["young"])

        self.play(
            ReplacementTransform(small_parent, w["outer"]),
            ReplacementTransform(small_cards, w["cards"]),
            FadeIn(w["sex_chamber"]),
            run_time=2.6,
        )

        # Beat 1: Offspring begin from sex cells.
        self.at("offspring begin from")
        self.play(
            FadeIn(w["sex_lbl"]),
            GrowArrow(w["arrows"][0]),
            GrowArrow(w["arrows"][1]),
            run_time=2.2,
        )

        # Beat 2: Those cells carry the parent's genes.
        self.at("carry the")
        carry_cards = [gene_card(i, scale=0.68, fill_opacity=0.55).move_to(w["cards"].get_center()) for i in range(2)]
        self.play(
            Indicate(w["cards"], color=BLUE, scale_factor=1.15),
            LaggedStart(*[c.animate.move_to([3.4, -0.25, 0]) for c in carry_cards], lag_ratio=0.3),
            run_time=2.2,
        )
        self.play(FadeOut(VGroup(*carry_cards)), run_time=0.35)

        # Beat 3: Skin cells can heal into a scar (gold ripples stay cleanly inside skin compartment).
        self.at("skin cells")
        self.play(FadeIn(w["skin_cells"]), FadeIn(w["skin_lbl"]), Create(w["scar"]), run_time=1.1)
        r_skin1 = Circle(radius=0.30, color=GOLD, stroke_width=5.0, fill_color=GOLD, fill_opacity=0.22).move_to([-3.55, 1.55, 0])
        r_skin2 = Circle(radius=0.25, color=GOLD, stroke_width=4.5, fill_color=GOLD, fill_opacity=0.18).move_to([-3.55, 1.55, 0])
        self.play(
            r_skin1.animate.scale(2.4).set_stroke(opacity=0).set_fill(opacity=0),
            Succession(Wait(0.35), r_skin2.animate.scale(2.4).set_stroke(opacity=0).set_fill(opacity=0)),
            run_time=1.8,
        )
        self.remove(r_skin1, r_skin2)

        # Beat 4: Muscle cells can grow with exercise (gold ripples stay cleanly inside muscle compartment).
        self.at("muscle cells")
        self.play(FadeIn(w["muscle_cells"]), FadeIn(w["muscle_lbl"]), FadeIn(w["muscle_patch"]), run_time=1.0)
        r_mus1 = Circle(radius=0.35, color=GOLD, stroke_width=7.5, fill_color=GOLD, fill_opacity=0.32).move_to([-3.75, -1.05, 0])
        r_mus2 = Circle(radius=0.28, color=GOLD, stroke_width=6.5, fill_color=GOLD, fill_opacity=0.26).move_to([-3.75, -1.05, 0])
        self.play(
            w["muscle_patch"].animate.scale(1.28),
            r_mus1.animate.scale(2.1).set_stroke(opacity=0).set_fill(opacity=0),
            Succession(Wait(0.35), r_mus2.animate.scale(2.1).set_stroke(opacity=0).set_fill(opacity=0)),
            run_time=2.0,
        )
        self.remove(r_mus1, r_mus2)

        # Beat 5: Those body-cell changes do not change the genes inside the sex cells.
        self.at("body cell changes")
        self.play(Create(w["barrier"]), run_time=0.7)
        r1 = Circle(radius=0.35, color=GOLD, stroke_width=7.5, fill_color=GOLD, fill_opacity=0.34).move_to([-3.55, 1.55, 0])
        r2 = Circle(radius=0.35, color=GOLD, stroke_width=7.5, fill_color=GOLD, fill_opacity=0.34).move_to([-3.75, -1.05, 0])
        r3 = Circle(radius=0.28, color=GOLD, stroke_width=6.5, fill_color=GOLD, fill_opacity=0.28).move_to([-3.55, 1.55, 0])
        r4 = Circle(radius=0.28, color=GOLD, stroke_width=6.5, fill_color=GOLD, fill_opacity=0.28).move_to([-3.75, -1.05, 0])
        self.play(
            r1.animate.scale(2.2).set_stroke(opacity=0).set_fill(opacity=0),
            r2.animate.scale(2.1).set_stroke(opacity=0).set_fill(opacity=0),
            Succession(Wait(0.5), r3.animate.scale(2.2).set_stroke(opacity=0).set_fill(opacity=0)),
            Succession(Wait(0.5), r4.animate.scale(2.1).set_stroke(opacity=0).set_fill(opacity=0)),
            w["sex_chamber"].animate.set_fill(TEAL, opacity=0.40),
            run_time=4.2,
        )
        self.remove(r1, r2, r3, r4)
        self.finish()


# ------------------------------------------------------------------ SCENE 04: PREDICT
class S04Predict(SpokenScene):
    def construct(self):
        self.add(corner_hex())
        w = build_cell_map(show_young=True, show_arrows=False)
        g = build_gate_tracks()

        g["scar_token"].move_to([-2.38, 1.55, 0])
        g["card_token"].move_to([-0.22, -0.45, 0])

        self.add(
            w["parent"],
            w["young"],
            g["upper_gate"],
            g["lower_gate"],
            g["scar_token"],
            g["card_token"],
        )

        # Beat 1: The skin change and the gene cards now sit beside different paths.
        self.at("the skin change")
        self.play(
            Create(g["upper_track"]),
            Create(g["lower_track"]),
            run_time=2.2,
        )
        self.play(
            g["scar_token"].animate.move_to([1.05, 1.03, 0]),
            g["card_token"].animate.move_to([1.05, -0.45, 0]),
            run_time=2.5,
        )

        # Beat 2: Which path can reach the offspring?
        self.at("which path")
        q = question_card("Which path reaches the young?", y=3.25, size=32)
        gate_halo_u = Circle(radius=0.55, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.18).move_to([1.85, g["upper_gate_y"], 0])
        gate_halo_l = Circle(radius=0.55, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.18).move_to([1.85, -0.45, 0])
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=1.0)
        self.play(FadeIn(gate_halo_u), FadeIn(gate_halo_l), run_time=0.9)

        # Beat 3: Keep watching both routes before you decide.
        self.at("keep watching")
        bob(g["scar_token"], amp=0.05, speed=2.2, seed=0)
        bob(g["card_token"], amp=0.05, speed=2.2, seed=1)
        self.play(
            gate_halo_u.animate.scale(1.25).set_opacity(0),
            gate_halo_l.animate.scale(1.25).set_opacity(0),
            run_time=2.0,
        )
        self.remove(gate_halo_u, gate_halo_l)
        self.finish()


# ------------------------------------------------------------------ SCENE 05: PAUSE
class S05Pause(PredictPause):
    QUESTION = "Which path reaches the young?"
    CARD = {"y": 3.25, "size": 32}
    SECONDS = 4.5

    def backdrop(self):
        w = build_cell_map(show_young=True, show_arrows=False)
        g = build_gate_tracks()
        bob(g["scar_token"], amp=0.05, speed=2.2, seed=0)
        bob(g["card_token"], amp=0.05, speed=2.2, seed=1)
        return VGroup(
            corner_hex(),
            w["parent"],
            w["young"],
            g["upper_track"],
            g["lower_track"],
            g["upper_gate"],
            g["lower_gate"],
            g["scar_token"],
            g["card_token"],
        )


# ------------------------------------------------------------------ SCENE 06: REVEAL
class S06Reveal(SpokenScene):
    def construct(self):
        self.add(corner_hex())
        w = build_cell_map(show_young=True, show_arrows=False)
        g = build_gate_tracks()

        self.add(
            w["parent"],
            w["young"],
            g["upper_track"],
            g["lower_track"],
            g["upper_gate"],
            g["lower_gate"],
            g["scar_token"],
            g["card_token"],
        )

        # Beat 1: Blue cards pass through the sex-cell gate into the young mouse.
        self.at("the blue cards")
        teal_route = Line([-0.22, -0.45, 0], [3.55, -0.45, 0], color=TEAL, stroke_width=9)
        settled_cards = gene_card_cluster(n=2, variant=0, scale=0.56, buff=0.06).move_to([4.85, -0.28, 0])
        stream_cards = [gene_card(i, scale=0.70, fill_opacity=0.58).move_to([-0.15, -0.45, 0]) for i in range(3)]
        self.play(
            g["lower_gate"].animate.set_color(TEAL),
            g["lower_bar"].animate.shift(UP * 0.52).set_opacity(0.0),
            Create(teal_route),
            run_time=1.0,
        )
        self.play(
            g["card_token"].animate.move_to([4.15, -0.35, 0]),
            LaggedStart(*[c.animate.move_to([4.50, -0.28, 0]) for c in stream_cards], lag_ratio=0.30),
            run_time=2.6,
        )
        self.play(ReplacementTransform(VGroup(g["card_token"], *stream_cards), settled_cards), run_time=0.8)

        # Beat 2: The scar reaches a red stop at the body-cell gate.
        self.at("the scar reaches")
        uy = g["upper_gate_y"]
        stop_bar = Line([1.85, uy + 0.54, 0], [1.85, uy - 0.54, 0], color=RED, stroke_width=10)
        stop_cross = VGroup(
            Line([1.62, uy + 0.23, 0], [2.08, uy - 0.23, 0], color=RED, stroke_width=8),
            Line([1.62, uy - 0.23, 0], [2.08, uy + 0.23, 0], color=RED, stroke_width=8),
        )
        stop_halo = Circle(radius=0.55, color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.22).move_to([1.85, uy, 0])
        self.play(
            g["upper_gate"].animate.set_color(RED),
            g["upper_track"].animate.set_color(RED),
            ReplacementTransform(g["upper_bar"], stop_bar),
            g["scar_token"].animate.move_to([1.45, 0.92, 0]),
            run_time=2.0,
        )
        self.play(FadeIn(stop_cross, scale=0.8), FadeIn(stop_halo), run_time=0.8)
        self.play(FadeOut(stop_halo), run_time=0.4)

        # Beat 3: Show the guiding rule once below the moving routes.
        self.at("gene coded traits")
        rule = T(
            "Gene-coded traits can pass on;\nordinary changes gained during life cannot.",
            size=24,
            color=TEXT,
            line_spacing=0.82,
        ).move_to([0.0, -3.18, 0])
        extra_cards = [gene_card(i, scale=0.72, fill_opacity=0.65).move_to([0.0, -0.45, 0]) for i in range(3)]
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.play(LaggedStart(*[c.animate.move_to([4.35, -0.32, 0]) for c in extra_cards], lag_ratio=0.25), run_time=1.8)
        self.play(FadeOut(VGroup(*extra_cards)), run_time=0.2)

        # Beat 4: Ordinary changes gained during life cannot.
        self.at("ordinary changes")
        stop_pulse = Circle(radius=0.35, color=RED, stroke_width=7, fill_color=RED, fill_opacity=0.38).move_to([1.85, uy, 0])
        blocked_token = scar_mark(0.84).move_to([0.10, 1.24, 0])
        self.play(
            blocked_token.animate.move_to([1.45, 0.92, 0]),
            stop_pulse.animate.scale(3.0).set_stroke(opacity=0).set_fill(opacity=0),
            run_time=2.6,
        )
        self.remove(stop_pulse, blocked_token)

        # Beat 5: Fade the sentence while the map remains; highlight ordinary body changes inside parent.
        self.at("ordinary means")
        self.play(FadeOut(rule), run_time=0.7)
        r_s = Circle(radius=0.35, color=GOLD, stroke_width=7, fill_color=GOLD, fill_opacity=0.34).move_to([-3.55, 1.55, 0])
        r_m = Circle(radius=0.35, color=GOLD, stroke_width=7, fill_color=GOLD, fill_opacity=0.34).move_to([-3.75, -1.05, 0])
        self.play(
            r_s.animate.scale(2.2).set_stroke(opacity=0).set_fill(opacity=0),
            r_m.animate.scale(2.1).set_stroke(opacity=0).set_fill(opacity=0),
            w["muscle_patch"].animate.scale(1.22),
            run_time=2.6,
        )
        self.remove(r_s, r_m)
        self.finish()


# ------------------------------------------------------------------ SCENE 07: ENVIRONMENT
class S07Environment(SpokenScene):
    def construct(self):
        self.add(corner_hex())
        w = build_cell_map(show_young=False, show_arrows=False)
        carried_cards = w["cards"]  # sits at (-1.25, -0.45, 0)

        plant = build_plant(gene_pos=(-1.25, -0.45, 0), height_scale=1.0, flower_color=HYD_NEUTRAL, soil_color=GREEN)
        env_ring = Circle(radius=2.95, color=GREEN, stroke_width=5.0, fill_color=GREEN, fill_opacity=0.15).move_to([-1.25, 0.10, 0])
        env_lbl = T("environment", size=28, color=GREEN, weight=BOLD).move_to([-1.25, 3.32, 0])

        prev_ghost = VGroup(w["outer"], w["skin_cells"], w["scar"], w["muscle_cells"], w["muscle_patch"], w["sex_chamber"])
        self.add(prev_ghost, carried_cards)

        # Beat 1: Genes are not the whole story.
        self.at("genes are not")
        self.play(
            FadeOut(prev_ghost),
            FadeIn(plant["node"]),
            Create(plant["stem_bot"]),
            Create(plant["stem_top"]),
            FadeIn(plant["leaves"]),
            FadeIn(plant["roots"]),
            FadeIn(plant["flower"]),
            run_time=2.2,
        )
        self.bring_to_front(carried_cards)

        # Beat 2: The environment is everything around a living thing that can affect it.
        self.at("the environment")
        self.play(Create(env_ring), FadeIn(env_lbl), run_time=3.2)

        # Beat 3-7: Soil, light, water, food, and temperature belong to it.
        self.at("soil")
        soil_lbl = T("soil", size=26, color=GREEN, weight=BOLD).move_to([-4.65, -2.05, 0])
        plant["soil"].save_state()
        plant["soil"].shift(DOWN * 0.7).set_opacity(0)
        self.play(plant["soil"].animate.restore(), FadeIn(soil_lbl), run_time=0.32)

        self.at("light")
        rays = VGroup(
            Line([-4.45, 2.35, 0], [-3.25, 1.45, 0], color=GOLD, stroke_width=5.0),
            Line([-4.25, 2.65, 0], [-3.00, 1.75, 0], color=GOLD, stroke_width=5.0),
            Line([-4.65, 2.05, 0], [-3.45, 1.20, 0], color=GOLD, stroke_width=5.0),
        )
        light_lbl = T("light", size=26, color=GOLD, weight=BOLD).move_to([-5.25, 2.55, 0])
        self.play(Create(rays), FadeIn(light_lbl), run_time=0.35)

        self.at("water")
        drops = VGroup(
            Dot([1.18, 1.45, 0], radius=0.095, color=TEAL),
            Dot([1.45, 1.15, 0], radius=0.095, color=TEAL),
            Dot([1.30, 0.80, 0], radius=0.095, color=TEAL),
        )
        water_lbl = T("water", size=26, color=TEAL, weight=BOLD).move_to([2.45, 1.15, 0])
        self.play(FadeIn(drops, shift=DOWN * 0.2), FadeIn(water_lbl), run_time=0.35)

        self.at("food")
        food_chip = chip("food", GREEN, size=24, pad=0.16).move_to([2.45, 0.05, 0])
        self.play(FadeIn(food_chip, scale=0.88), run_time=0.32)

        self.at("temperature")
        therm_stem = RoundedRectangle(corner_radius=0.10, width=0.28, height=1.22, color=TEXT, stroke_width=3.2).move_to([2.15, -1.30, 0])
        therm_bulb = Circle(radius=0.22, color=RED, stroke_width=3.0, fill_color=RED, fill_opacity=0.92).move_to([2.15, -1.96, 0])
        therm_fill = Rectangle(width=0.18, height=0.80, color=RED, stroke_width=0, fill_color=RED, fill_opacity=0.92).move_to([2.15, -1.48, 0])
        temp_lbl = T("temperature", size=26, color=TEXT).move_to([3.60, -1.55, 0])
        self.play(FadeIn(therm_stem), FadeIn(therm_bulb), GrowFromEdge(therm_fill, DOWN), FadeIn(temp_lbl), run_time=1.8)

        # Beat 8-9: Genes and environment work together to shape the phenotype, the trait that appears.
        self.at("genes and environment")
        arrow_g = Arrow([-0.35, -0.35, 0], [-0.58, 1.50, 0], color=BLUE, stroke_width=7.5, buff=0.08, max_tip_length_to_length_ratio=0.18)
        arrow_e = Arrow([1.45, 0.15, 0], [-0.28, 1.72, 0], color=GREEN, stroke_width=7.5, buff=0.08, max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(arrow_g), GrowArrow(arrow_e), env_ring.animate.set_fill(GREEN, opacity=0.22), run_time=2.2)

        self.at("the phenotype")
        pheno_lbl = T("phenotype", size=32, color=TEXT, weight=BOLD).move_to([2.80, 2.25, 0])
        pheno_ptr = Arrow([1.55, 2.20, 0], [-0.30, 1.98, 0], color=TEXT, stroke_width=4.5, buff=0.05, max_tip_length_to_length_ratio=0.12)
        self.play(
            FadeIn(pheno_lbl, shift=RIGHT * 0.15),
            GrowArrow(pheno_ptr),
            plant["flower"].animate.scale(1.22),
            run_time=2.0,
        )
        self.finish()


# ------------------------------------------------------------------ SCENE 08: VARIATION
class S08Variation(SpokenScene):
    def construct(self):
        self.add(corner_hex())
        self.add(scope_tag("schematic"))

        xs = [-5.0, -2.5, 0.0, 2.5, 5.0]
        plants = [
            build_plant(gene_pos=(x, -0.82, 0), height_scale=0.92, flower_color=HYD_NEUTRAL, soil_color=GREEN)
            for x in xs
        ]
        rings = [
            Circle(radius=1.06, color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.14).move_to([x, -0.48, 0])
            for x in xs
        ]
        for p in plants:
            p["group"].scale(0.82, about_point=[p["gx"], -0.82, 0])

        # Beat 1: Variation means differences among living things of the same kind.
        self.at("variation means")
        self.add(plants[2]["group"], rings[2])
        self.play(
            LaggedStart(
                *[AnimationGroup(FadeIn(plants[i]["group"], scale=0.85), Create(rings[i])) for i in (0, 1, 3, 4)],
                lag_ratio=0.22,
            ),
            run_time=4.2,
        )

        # Beat 2: Some differences trace to inherited alleles (left two plants vary alleles + flowers).
        self.at("trace to inherited")
        new_cards_0 = gene_card_cluster(n=3, variant=1, scale=0.54, buff=0.06).move_to(plants[0]["cards"].get_center())
        new_cards_1 = gene_card_cluster(n=3, variant=2, scale=0.54, buff=0.06).move_to(plants[1]["cards"].get_center())
        self.play(
            ReplacementTransform(plants[0]["cards"], new_cards_0),
            ReplacementTransform(plants[1]["cards"], new_cards_1),
            plants[0]["flower"].animate.set_color(HYD_BLUE).scale(1.14).shift(UP * 0.30),
            plants[0]["stem_top"].animate.stretch(1.18, 1, about_point=plants[0]["stem_top"].get_bottom()),
            plants[1]["flower"].animate.set_color(HYD_PINK).scale(0.90).shift(DOWN * 0.18),
            run_time=2.8,
        )

        # Beat 3: Others develop as environments differ (right two plants vary environment rings + flowers).
        self.at("develop as environments")
        self.play(
            rings[3].animate.scale(1.10).set_stroke(GREEN, width=5.5).set_fill(GREEN, opacity=0.22),
            rings[4].animate.scale(0.84).set_stroke(SOIL_LESS, width=3.0),
            plants[3]["soil"].animate.set_fill(SOIL_ACID, opacity=0.55).set_stroke(SOIL_ACID),
            plants[4]["soil"].animate.set_fill(SOIL_LESS, opacity=0.38).set_stroke(SOIL_LESS),
            plants[3]["flower"].animate.scale(1.20).shift(UP * 0.32).set_color(HYD_BLUE),
            plants[3]["stem_top"].animate.stretch(1.20, 1, about_point=plants[3]["stem_top"].get_bottom()),
            plants[4]["flower"].animate.scale(0.84).shift(DOWN * 0.24).set_color(HYD_PINK),
            run_time=3.2,
        )

        # Beat 4: Many traits reflect both (center plant responds to both).
        self.at("reflect both")
        self.play(
            Indicate(plants[2]["node"], color=BLUE, scale_factor=1.18),
            Indicate(rings[2], color=GREEN, scale_factor=1.10),
            plants[2]["flower"].animate.set_color(HYD_MID).shift(UP * 0.22),
            plants[2]["stem_top"].animate.stretch(1.14, 1, about_point=plants[2]["stem_top"].get_bottom()),
            run_time=2.1,
        )

        # Beat 5-6: Matching gene sets can meet different surroundings and produce different visible results.
        self.at("matching gene sets")
        hl_1 = SurroundingRectangle(plants[2]["node"], color=BLUE, stroke_width=4.5, buff=0.08)
        hl_2 = SurroundingRectangle(plants[3]["node"], color=BLUE, stroke_width=4.5, buff=0.08)
        self.play(Create(hl_1), Create(hl_2), run_time=2.0)

        self.at("different visible results")
        self.play(
            plants[2]["flower"].animate.scale(1.22),
            plants[3]["flower"].animate.scale(1.20),
            rings[2].animate.set_fill(GREEN, opacity=0.30).set_stroke(GREEN, width=6.5),
            rings[3].animate.set_fill(SOIL_ACID, opacity=0.30).set_stroke(SOIL_ACID, width=6.5),
            run_time=1.8,
        )
        self.play(
            plants[2]["flower"].animate.scale(1 / 1.22),
            plants[3]["flower"].animate.scale(1 / 1.20),
            FadeOut(hl_1),
            FadeOut(hl_2),
            run_time=1.2,
        )

        # Beat 7-8: Slide away two large boxes (genes only / environment only); replace with overlapping circles.
        self.at("a genes")
        box_g = RoundedRectangle(corner_radius=0.16, width=4.6, height=4.6, color=BLUE, stroke_width=5.5, fill_color=BLUE, fill_opacity=0.22).move_to([-2.55, 0.15, 0])
        lbl_g = T("genes only", size=28, color=BLUE, weight=BOLD).move_to([-2.55, 2.80, 0])
        box_e = RoundedRectangle(corner_radius=0.16, width=4.6, height=4.6, color=GREEN, stroke_width=5.5, fill_color=GREEN, fill_opacity=0.22).move_to([2.55, 0.15, 0])
        lbl_e = T("environment only", size=28, color=GREEN, weight=BOLD).move_to([2.55, 2.80, 0])
        self.play(FadeIn(box_g, shift=RIGHT * 1.2), FadeIn(lbl_g), run_time=0.8)

        self.at("an environment")
        self.play(FadeIn(box_e, shift=LEFT * 1.2), FadeIn(lbl_e), run_time=0.8)

        self.at("box", lead=0.0, nth=1)
        circ_g = Circle(radius=2.35, color=BLUE, stroke_width=5.0, fill_color=BLUE, fill_opacity=0.18).move_to([-1.25, 0.15, 0]).set_z_index(-2)
        circ_e = Circle(radius=2.35, color=GREEN, stroke_width=5.0, fill_color=GREEN, fill_opacity=0.18).move_to([1.25, 0.15, 0]).set_z_index(-2)
        lbl_circ_g = T("genes", size=28, color=BLUE, weight=BOLD).move_to([-2.3, 2.80, 0])
        lbl_circ_e = T("environment", size=28, color=GREEN, weight=BOLD).move_to([2.3, 2.80, 0])
        self.play(
            FadeOut(box_g, shift=LEFT * 2.2),
            FadeOut(box_e, shift=RIGHT * 2.2),
            swap(lbl_g, lbl_circ_g, run_time=0.75),
            swap(lbl_e, lbl_circ_e, run_time=0.75),
            FadeIn(circ_g),
            FadeIn(circ_e),
            run_time=0.75,
        )
        self.finish()


# ------------------------------------------------------------------ SCENE 09: HYDRANGEA
class S09Hydrangea(SpokenScene):
    def construct(self):
        self.add(corner_hex())
        self.add(scope_tag("color response is schematic"))

        left = build_plant(gene_pos=(-3.25, -0.50, 0), height_scale=1.02, flower_color=HYD_NEUTRAL, soil_color=GREEN)
        right = build_plant(gene_pos=(3.25, -0.50, 0), height_scale=1.02, flower_color=HYD_NEUTRAL, soil_color=GREEN)
        center = build_plant(gene_pos=(0.0, -0.50, 0), height_scale=1.02, flower_color=HYD_NEUTRAL, soil_color=GREEN)
        self.add(center["group"])

        # Beat 1: Watch matching cuttings from a bigleaf hydrangea.
        self.at("watch matching cuttings")
        self.play(
            ReplacementTransform(center["group"], VGroup(left["group"], right["group"])),
            run_time=3.2,
        )

        # Beat 2: Their blue gene cards stay the same.
        self.at("blue gene cards")
        box_l = SurroundingRectangle(left["cards"], color=BLUE, stroke_width=3.8, buff=0.10)
        box_r = SurroundingRectangle(right["cards"], color=BLUE, stroke_width=3.8, buff=0.10)
        lbl_same = T("same blue gene cards", size=28, color=BLUE, weight=BOLD).move_to([0.0, -0.50, 0])
        self.play(Create(box_l), Create(box_r), FadeIn(lbl_same), run_time=2.6)

        # Beat 3: In many kinds, acidic soil lets roots take up more aluminum.
        self.at("acidic soil")
        lbl_acid = T("acidic soil", size=28, color=SOIL_ACID, weight=BOLD).move_to([-3.25, -2.75, 0])
        al_dots = VGroup(*[
            Dot([-3.25 + dx, -2.10 + dy, 0], radius=0.095, color=TEXT)
            for dx, dy in [(-0.55, 0.0), (-0.20, 0.12), (0.20, -0.05), (0.55, 0.08), (-0.05, -0.10), (0.05, 0.15)]
        ])
        al_lbl = T("aluminum", size=26, color=TEXT).move_to([-5.20, -1.35, 0])
        self.play(
            left["soil"].animate.set_fill(SOIL_ACID, opacity=0.56).set_stroke(SOIL_ACID),
            FadeIn(lbl_acid),
            FadeIn(al_dots),
            FadeIn(al_lbl),
            run_time=1.3,
        )
        self.play(
            LaggedStart(*[d.animate.move_to([-3.25 + (i % 3 - 1) * 0.18, 1.55, 0]) for i, d in enumerate(al_dots)], lag_ratio=0.12),
            run_time=2.4,
        )

        # Beat 4: That helps flowers become blue.
        self.at("flowers become blue")
        self.play(
            left["flower"].animate.set_color(HYD_BLUE).scale(1.06),
            FadeOut(al_dots),
            FadeOut(al_lbl),
            run_time=2.0,
        )

        # Beat 5: Less acidic soil can give pink flowers.
        self.at("less acidic soil")
        lbl_less = T("less acidic soil", size=28, color=SOIL_LESS, weight=BOLD).move_to([3.25, -2.75, 0])
        self.play(
            right["soil"].animate.set_fill(SOIL_LESS, opacity=0.44).set_stroke(SOIL_LESS),
            FadeIn(lbl_less),
            run_time=1.0,
        )
        self.play(
            right["flower"].animate.set_color(HYD_PINK).scale(1.06),
            run_time=2.0,
        )

        # Beat 6: The soil changes the phenotype, not the cutting's genes.
        self.at("the soil changes")
        self.play(
            Indicate(left["flower"], color=HYD_BLUE, scale_factor=1.15),
            Indicate(right["flower"], color=HYD_PINK, scale_factor=1.15),
            Indicate(box_l, color=BLUE, scale_factor=1.10),
            Indicate(box_r, color=BLUE, scale_factor=1.10),
            run_time=2.8,
        )
        self.finish()


# ------------------------------------------------------------------ SCENE 10: SCOPE
class S10Scope(SpokenScene):
    def construct(self):
        self.add(corner_hex())
        self.add(scope_tag("schematic"))

        # Part A: Short row of schematic possible flower colors above the gene cards
        cards = gene_card_cluster(n=3, variant=0, scale=0.98, buff=0.12).move_to([0.0, -0.85, 0])
        cards_lbl = T("genes set possible colors", size=28, color=BLUE).move_to([0.0, -1.85, 0])

        swatch_b = flower_corymb([-2.2, 1.35, 0], radius=0.62, color=HYD_BLUE)
        swatch_m = flower_corymb([0.0, 1.35, 0], radius=0.62, color=HYD_MID)
        swatch_p = flower_corymb([2.2, 1.35, 0], radius=0.62, color=HYD_PINK)
        swatches = VGroup(swatch_b, swatch_m, swatch_p)
        links = VGroup(
            Line([0.0, -0.20, 0], [-2.2, 0.52, 0], color=BLUE, stroke_width=3.6),
            Line([0.0, -0.20, 0], [0.0, 0.52, 0], color=BLUE, stroke_width=3.6),
            Line([0.0, -0.20, 0], [2.2, 0.52, 0], color=BLUE, stroke_width=3.6),
        )

        # Beat 1: Genes set which colors are possible
        self.at("genes set which")
        self.play(FadeIn(cards), FadeIn(cards_lbl), run_time=0.8)
        self.play(Create(links), FadeIn(swatches), run_time=1.2)

        # Beat 2: while soil helps decide which appears.
        self.at("while soil helps")
        soil_arrow = Arrow([-2.2, 2.75, 0], [-2.2, 2.02, 0], color=GREEN, stroke_width=7.5, buff=0, max_tip_length_to_length_ratio=0.30)
        soil_tag = T("soil", size=28, color=GREEN, weight=BOLD).next_to(soil_arrow, UP, buff=0.14)
        self.play(GrowArrow(soil_arrow), FadeIn(soil_tag), run_time=0.8)
        self.play(
            soil_arrow.animate.shift(RIGHT * 4.4),
            soil_tag.animate.shift(RIGHT * 4.4),
            run_time=1.8,
        )

        # Beat 3: Return the main matching cuttings to center and show soil transforming their phenotypes.
        self.at("the same logic")
        part_a = VGroup(cards, cards_lbl, links, swatches, soil_arrow, soil_tag)
        cut_l = build_plant(gene_pos=(-4.1, -0.70, 0), height_scale=0.98, flower_color=HYD_NEUTRAL, soil_color=GREEN)
        cut_r = build_plant(gene_pos=(-0.7, -0.70, 0), height_scale=0.98, flower_color=HYD_NEUTRAL, soil_color=GREEN)
        for c in (cut_l, cut_r):
            c["group"].scale(0.88, about_point=[c["gx"], -0.70, 0])

        self.play(FadeOut(part_a), run_time=0.6)
        self.play(FadeIn(cut_l["group"]), FadeIn(cut_r["group"]), run_time=2.0)
        self.play(
            cut_l["soil"].animate.set_fill(SOIL_ACID, opacity=0.60).set_stroke(SOIL_ACID),
            cut_r["soil"].animate.set_fill(SOIL_LESS, opacity=0.46).set_stroke(SOIL_LESS),
            cut_l["flower"].animate.set_color(HYD_BLUE).scale(1.06),
            cut_r["flower"].animate.set_color(HYD_PINK).scale(1.06),
            run_time=3.6,
        )

        # Beat 4: Phenotype tells what appears, not which cause acted.
        self.at("phenotype tells")
        q_l = VGroup(
            Circle(radius=0.40, color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.22),
            T("?", size=42, color=GOLD, font=TITLE_FONT, weight=BOLD),
        ).move_to([-5.05, 1.40, 0])
        q_r = VGroup(
            Circle(radius=0.40, color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.22),
            T("?", size=42, color=GOLD, font=TITLE_FONT, weight=BOLD),
        ).move_to([0.25, 1.40, 0])
        self.play(
            FadeIn(q_l, scale=0.85),
            FadeIn(q_r, scale=0.85),
            cut_l["flower"].animate.scale(1.14),
            cut_r["flower"].animate.scale(1.14),
            run_time=2.0,
        )
        self.play(
            FadeOut(q_l),
            FadeOut(q_r),
            cut_l["flower"].animate.scale(1 / 1.14),
            cut_r["flower"].animate.scale(1 / 1.14),
            run_time=1.8,
        )

        # Beat 5: First trace the cause (green soil arrows end at the flowers).
        self.at("first trace")
        soil_ar_l = Arrow([-5.50, -1.75, 0], [-4.95, 1.10, 0], color=GREEN, stroke_width=7.5, buff=0.06, max_tip_length_to_length_ratio=0.14)
        soil_ar_r = Arrow([0.75, -1.75, 0], [0.20, 1.10, 0], color=GREEN, stroke_width=7.5, buff=0.06, max_tip_length_to_length_ratio=0.14)
        lbl_soil_end = T("soil \u2192 flower", size=26, color=GREEN, weight=BOLD).move_to([-2.4, 2.65, 0])
        self.play(GrowArrow(soil_ar_l), GrowArrow(soil_ar_r), FadeIn(lbl_soil_end), run_time=2.6)

        # Beat 6: Then ask whether it can enter the gene route to offspring.
        self.at("enter the gene")
        seed_oval = Ellipse(width=0.84, height=1.14, color=TEAL, stroke_width=4.0, fill_color=TEAL, fill_opacity=0.28).move_to([4.85, -0.70, 0])
        sprout = VGroup(
            Line([4.85, -0.18, 0], [4.85, 0.44, 0], color=GREEN, stroke_width=6.0),
            Ellipse(width=0.60, height=0.28, color=GREEN, stroke_width=3.0, fill_color=GREEN, fill_opacity=0.48).rotate(0.4).move_to([4.58, 0.36, 0]),
            Ellipse(width=0.60, height=0.28, color=GREEN, stroke_width=3.0, fill_color=GREEN, fill_opacity=0.48).rotate(-0.4).move_to([5.12, 0.36, 0]),
        )
        seed_lbl = T("seed offspring", size=26, color=TEAL, weight=BOLD).move_to([4.85, -1.75, 0])
        gene_route = Arrow([0.10, -0.70, 0], [4.28, -0.70, 0], color=TEAL, stroke_width=7.0, buff=0.08, max_tip_length_to_length_ratio=0.12)
        travel_card = gene_card(0, scale=0.62, fill_opacity=0.58).move_to([0.10, -0.70, 0])
        lbl_gene_route = T("gene route", size=26, color=TEAL, weight=BOLD).move_to([2.15, -0.18, 0])

        self.play(
            FadeIn(seed_oval),
            FadeIn(sprout),
            FadeIn(seed_lbl),
            GrowArrow(gene_route),
            FadeIn(lbl_gene_route),
            run_time=1.3,
        )
        self.play(travel_card.animate.move_to([4.85, -0.70, 0]), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------ SCENE 11: END CARD
class S11End(EndCard):
    LINE = "Gene-coded traits can pass on; ordinary changes gained during life cannot."
