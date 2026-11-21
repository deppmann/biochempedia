"""Within Reach — Digestion Chapter 2: fat digestion and absorption.

COLOUR MAP (one colour per concept for the whole film):
- BLUE (#58C4DD): active enzyme (lipase)
- LIGHT_BLUE (#9FE3F2): colipase partner tab on lipase
- GREEN (#83C167): fat substrate and lipid cargo (drop, droplets, glycerol, fatty acids, triacylglycerol, short/medium stubs, cholesterol/vitamin cargo)
- YELLOW (#F5D547): ester bonds (about to be cut, intact, or rebuilt)
- WATER (#7D8EE8): water and watery gut lumen
- GREY (#8B93A1): dormant zymogen with 'pro' tab and ghost outlines
- GOLD (#D4A843): trypsin (link-back) and predict/callout highlights
- RED (#FC6255): lock or block (padlock icon, cross)
- ORANGE (#F28C38): bile salts (coats, specks, micelle rims)
- PURPLE (#B278E6): lymph and the lacteal
- CRIMSON (#9E2B3C): blood capillary, portal blood, liver route
- TEXT (#E8EAF0): primary labels, titles, sugars/amino acids
- WHITE (#FFFFFF): brush-border edge and chylomicron protein shell

ONE WORLD (carried across the film):
A 16:9 cross-section of the small intestine. Upper zone: watery gut lumen (WATER) holding the fat drop,
droplet cloud, lipase, water, and bile salts. Lower zone (revealed from s09 onward): gut epithelial cells
with a WHITE brush-border edge facing the lumen, and the villus core below containing the PURPLE lacteal
(overlapping flaps with wide loose junctions) beside the CRIMSON blood capillary (narrow gaps) leading to
the CRIMSON liver outline at right.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: ghost zymogens flip BLUE via GOLD trypsin; GREEN fat drop with 12 seeded YELLOW bonds builds as ghost fades; BLUE lipase cutters drift in along edge trajectories, pulse once on activation, and pose the question.
- s02_surface: WATER particles compute radial deflection off the drop continuously; BLUE lipase cutters dock and step along the rim, snipping the 3 rim YELLOW bonds while the 9 interior bonds remain out of reach.
- s03_bile: ORANGE bile salts swirl in and coat the drop; drop splits in computed volume-conserving stages (1 -> 8 -> 24 droplets) carrying the 9 intact YELLOW bonds to droplet edges; ghost original circle compares geometry.
- s04_predict: left 1 mm drop vs right 48-droplet patch (1 um each, seeded non-overlapping grid), with BLUE surface outlines tracing both continuously.
- s06_answer: broken-axis bar pair grows dynamically from 1 to 1,000x (computed from D_drop / D_droplet = 1 mm / 1 um = 1000) via ValueTracker + synced counter; BLUE lipase floods droplet edges and lights reachable YELLOW bonds.
- s07_cut: zoomed triacylglycerol block cartoon (glycerol spine + 3 tail blocks + 3 YELLOW links); lipase+colipase docks and spends 2 WATER drops to snap the two outer ester links sequentially, separating 1 monoacylglycerol + 2 free fatty acids.
- s08_idea: pullback to droplet cloud; ghost 'pro' tab gets RED cross and fades; large drop (unreached interior) vs small droplets (lipase stepping/snipping edges) compared; ORANGE bile coats pulse on exposure.
- s09_micelle: camera pans down to gut cells + WHITE brush border; ORANGE bile salts gather loose GREEN pieces into 4 micelles that ferry across the WATER layer, release cargo into the gut cell, and return empty.
- s10_rebuild: zoomed gut cell; incoming GREEN pieces attach to spines with new YELLOW links; live ValueTracker gauge ('free pieces inside') stays low as arrivals rebuild; detergent-ghost tail nudging membrane snaps onto a third spine.
- s11_chylomicron: rebuilt blocks pack into a WHITE-shelled chylomicron that exits the cell, drifts to the CRIMSON capillary (narrow gaps), bounces off, and triggers the RED padlock.
- s12_lacteal: PURPLE lacteal flaps flex open; chylomicrons slip through and flow along a curving PURPLE lymph path while GREEN cholesterol/vitamin cargo specks highlight inside.
- s13_sort: WHITE sugar/amino-acid dots and GREEN short/medium stubs exit the cell straight through CRIMSON capillary gaps to portal blood and liver, side-by-side with PURPLE lymph chylomicrons.
- s14_close: full ONE WORLD view; lipase pulses on access, then surface cloud, micelle ferry, and wide lacteal door illuminate in sequence as chylomicron slips through flaps and sugars keep flowing.
"""

import numpy as np
from bp_parts import *  # noqa: F401,F403
from bp_parts import (
    T, M, chip, fit, fit_text, boxed_label, counter, countdown,
    PredictPause, place_label, scope_tag, swap,
)
from bp_style import BG, BLUE, YELLOW, GREEN, RED, GREY, TEXT, GOLD, TITLE_FONT, NarratedScene

LIGHT_BLUE = "#9FE3F2"
WATER = "#7D8EE8"
ORANGE = "#F28C38"
PURPLE = "#B278E6"
CRIMSON = "#9E2B3C"

# Lesson numbers (from lesson_for_context.mdx)
DROP_DIAM_MM = 1.0
DROPLET_DIAM_UM = 1.0
SURFACE_RATIO = int(round((DROP_DIAM_MM * 1000.0) / DROPLET_DIAM_UM))  # 1,000x


# ------------------------------------------------------------------ shared visual builders
def make_lumen_bg(y_min=-3.8, y_max=3.8, opacity=0.10):
    """Subtle static watery lumen field in the upper/full gut zone."""
    rect = Rectangle(
        width=14.4, height=y_max - y_min,
        stroke_width=0, fill_color=WATER, fill_opacity=opacity,
    ).move_to([0, (y_min + y_max) / 2, 0]).set_z_index(-8)
    rect.layout_ok = True
    return rect


def make_lipase(with_colipase=False, scale=1.0):
    """Active BLUE lipase enzyme shape (notched cutter) with optional LIGHT_BLUE colipase tab."""
    body = Sector(
        radius=0.36 * scale, start_angle=0.45, angle=TAU - 0.9,
        color=BLUE, fill_color=BLUE, fill_opacity=0.92,
        stroke_color=TEXT, stroke_width=2.0,
    )
    if not with_colipase:
        return VGroup(body)
    tab = RoundedRectangle(
        corner_radius=0.06, width=0.30 * scale, height=0.22 * scale,
        color=LIGHT_BLUE, fill_color=LIGHT_BLUE, fill_opacity=0.94,
        stroke_color=TEXT, stroke_width=1.6,
    ).next_to(body, DOWN, buff=-0.05 * scale).shift(LEFT * 0.08 * scale)
    return VGroup(tab, body)


def make_zymogen(text="protease"):
    """Dormant GREY zymogen chip with a clearly separated 'pro' tab (>= 24pt font)."""
    core_lab = T(text, size=24, color=TEXT)
    core = RoundedRectangle(
        corner_radius=0.12, width=core_lab.width + 0.42, height=core_lab.height + 0.30,
        stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.25,
    )
    core_lab.move_to(core)
    pro_txt = T("pro", size=24, color=TEXT)
    pro_box = RoundedRectangle(
        corner_radius=0.08, width=pro_txt.width + 0.32, height=pro_txt.height + 0.24,
        stroke_color=GREY, stroke_width=2.2, fill_color=GREY, fill_opacity=0.36,
    ).next_to(core, RIGHT, buff=0.10)
    pro_txt.move_to(pro_box)
    g = VGroup(core, core_lab, pro_box, pro_txt)
    g.core, g.lab, g.pro = core, core_lab, VGroup(pro_box, pro_txt)
    return g


def make_bond_mark(center=ORIGIN, angle=0.0, size=0.24, color=YELLOW, opacity=1.0):
    """Short YELLOW ester bond bar (schematic mark, not a chemical structure)."""
    bar = RoundedRectangle(
        corner_radius=0.04, width=size, height=size * 0.44,
        stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=0.95 * opacity,
    ).set_stroke(opacity=opacity)
    bar.rotate(angle).move_to(center)
    return bar


def make_padlock(center=ORIGIN, scale=0.9):
    """RED padlock icon reused from the first film for a blocked path."""
    shackle = Arc(
        radius=0.16 * scale, start_angle=0, angle=PI,
        stroke_color=RED, stroke_width=5 * scale,
    ).move_to(center + UP * (0.14 * scale))
    body = RoundedRectangle(
        corner_radius=0.06 * scale, width=0.44 * scale, height=0.34 * scale,
        stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.90,
    ).move_to(center + DOWN * (0.06 * scale))
    keyhole = Dot(center + DOWN * (0.06 * scale), radius=0.05 * scale, color=BG)
    return VGroup(shackle, body, keyhole)


def make_water_drop(center=ORIGIN, scale=1.0):
    """Simple periwinkle water drop (circle + pointed tip, no structure)."""
    top = Triangle(color=WATER, fill_color=WATER, fill_opacity=0.95, stroke_width=0).scale(0.15 * scale)
    bot = Circle(radius=0.14 * scale, color=WATER, fill_color=WATER, fill_opacity=0.95, stroke_width=0)
    bot.move_to(center + DOWN * 0.04 * scale)
    top.move_to(center + UP * 0.09 * scale)
    return VGroup(bot, top)


def make_fat_drop_with_bonds(center=ORIGIN, radius=2.3, seed=7):
    """Large GREEN fat drop with 3 rim bonds + 9 interior bonds at fixed seeded positions."""
    drop = Circle(
        radius=radius, color=GREEN, stroke_width=4.5,
        fill_color=GREEN, fill_opacity=0.42,
    ).move_to(center)
    rim_angles = [0.62, 2.35, 4.10]
    rim_bonds = VGroup(*[
        make_bond_mark(
            center + (radius - 0.16) * np.array([np.cos(a), np.sin(a), 0.0]),
            angle=a + PI / 2, size=0.26,
        )
        for a in rim_angles
    ])
    rng = np.random.default_rng(seed)
    pts = []
    # Keep central band clear so 'out of reach' text sits unobstructed
    while len(pts) < 9:
        r = radius * np.sqrt(rng.uniform(0.20, 0.72))
        th = rng.uniform(0, TAU)
        p = np.array([r * np.cos(th), r * np.sin(th), 0.0])
        if abs(p[1]) < 0.48 and abs(p[0]) < 1.5:
            continue
        if all(np.linalg.norm(p - q) > 0.60 for q in pts):
            pts.append(p)
    inner_bonds = VGroup(*[
        make_bond_mark(center + p, angle=rng.uniform(0, PI), size=0.24, opacity=0.60)
        for p in pts
    ])
    return drop, rim_bonds, inner_bonds


def make_droplet_cloud(center=np.array([0.0, -0.1, 0.0]), n=24, radius=0.35, spread=(3.6, 1.85), seed=11):
    """Non-overlapping cloud of ORANGE-coated GREEN droplets with edge YELLOW bonds."""
    rng = np.random.default_rng(seed)
    centers = []
    tries = 0
    while len(centers) < n and tries < 2500:
        tries += 1
        p = np.array([rng.uniform(-spread[0], spread[0]), rng.uniform(-spread[1], spread[1]), 0.0])
        if (p[0] / (spread[0] + 0.1)) ** 2 + (p[1] / (spread[1] + 0.1)) ** 2 > 1.0:
            continue
        if all(np.linalg.norm((p + center) - q) > 2.45 * radius for q in centers):
            centers.append(p + center)
    droplets = VGroup()
    bonds = VGroup()
    coats = VGroup()
    for i, c in enumerate(centers):
        d = Circle(radius=radius, color=GREEN, stroke_width=2.2, fill_color=GREEN, fill_opacity=0.45).move_to(c)
        coat = Circle(radius=radius + 0.05, color=ORANGE, stroke_width=3.8, fill_opacity=0).move_to(c)
        droplets.add(d)
        coats.add(coat)
        if i % 2 == 0:
            ang = rng.uniform(0, TAU)
            b = make_bond_mark(c + (radius - 0.06) * np.array([np.cos(ang), np.sin(ang), 0.0]), angle=ang + PI / 2, size=0.17)
            bonds.add(b)
    return droplets, coats, bonds, centers


def make_predict_backdrop():
    """Shared backdrop for s04_predict and s05_predict_pause: 1 mm drop -> 1 um droplets (not to scale)."""
    lumen = make_lumen_bg()
    left_c = np.array([-3.45, 0.25, 0.0])
    drop = Circle(radius=1.50, color=GREEN, stroke_width=2.8, fill_color=GREEN, fill_opacity=0.44).move_to(left_c)
    drop_outline = Circle(radius=1.56, color=BLUE, stroke_width=6.0, fill_opacity=0).move_to(left_c)
    lbl_l = T("1 mm across", size=28, color=TEXT).move_to([left_c[0], -1.75, 0])

    arrow = Arrow([-1.45, 0.25, 0], [-0.20, 0.25, 0], color=TEXT, stroke_width=4.5, buff=0)

    right_c = np.array([2.80, 0.25, 0.0])
    rng = np.random.default_rng(19)
    droplets = VGroup()
    outlines = VGroup()
    for row in range(6):
        for col in range(8):
            x = right_c[0] + (col - 3.5) * 0.52 + rng.uniform(-0.04, 0.04)
            y = right_c[1] + (row - 2.5) * 0.48 + rng.uniform(-0.04, 0.04)
            d = Circle(radius=0.17, color=GREEN, stroke_width=1.6, fill_color=GREEN, fill_opacity=0.46).move_to([x, y, 0])
            o = Circle(radius=0.20, color=BLUE, stroke_width=3.0, fill_opacity=0).move_to([x, y, 0])
            droplets.add(d)
            outlines.add(o)
    lbl_r = T("1 µm each", size=28, color=TEXT).move_to([right_c[0], -1.75, 0])
    same_tag = boxed_label("same total fat", color=GREEN, size=26, pad=0.16).move_to([-0.3, 2.25, 0])
    scale_tag = T("schematic — not to scale", size=24, color=TEXT).move_to([-4.6, -3.25, 0])
    return VGroup(lumen, drop, drop_outline, lbl_l, arrow, droplets, outlines, lbl_r, same_tag, scale_tag)


def make_brush_border_row(y_top=-0.45, cell_h=1.55, highlight_center=True):
    """Row of gut epithelial cells cleanly inside safe width [-6.45, 6.45] with WHITE brush-border edge."""
    cells = VGroup()
    widths = [2.4, 2.4, 2.8, 2.4, 2.4]
    xs = [-5.25, -2.75, 0.0, 2.75, 5.25]
    for i, (w, x) in enumerate(zip(widths, xs)):
        c = RoundedRectangle(
            corner_radius=0.1, width=w - 0.08, height=cell_h,
            stroke_color=GREY, stroke_width=2.4,
            fill_color=GREY, fill_opacity=0.22 if (not highlight_center or i != 2) else 0.30,
        ).move_to([x, y_top - cell_h / 2, 0])
        cells.add(c)
    pts = []
    for k in range(86):
        xx = -6.4 + k * (12.8 / 85.0)
        yy = y_top + (0.14 if k % 2 == 0 else 0.0)
        pts.append([xx, yy, 0.0])
    bb = VMobject(stroke_color=WHITE, stroke_width=3.5)
    bb.set_points_as_corners(pts)
    return cells, bb


def make_lacteal_vessel(x_c=-2.3, y_top=-2.05, y_bot=-3.55, width=1.18, open_gap=0.0, brightened=True):
    """PURPLE lacteal lymph tube drawn with overlapping flaps / loose junctions."""
    col = PURPLE
    op = 0.96 if brightened else 0.42
    fill_op = 0.24 if brightened else 0.10
    bg_tube = RoundedRectangle(
        corner_radius=0.25, width=width, height=y_top - y_bot,
        stroke_width=0, fill_color=col, fill_opacity=fill_op,
    ).move_to([x_c, (y_top + y_bot) / 2, 0])
    left_wall = Line([x_c - width / 2, y_top, 0], [x_c - width / 2, y_bot, 0], color=col, stroke_width=4.5, stroke_opacity=op)
    flap1 = Line([x_c + width / 2, y_top, 0], [x_c + width / 2 - 0.12, (y_top + y_bot) / 2 + 0.15, 0], color=col, stroke_width=4.5, stroke_opacity=op)
    flap2 = Line([x_c + width / 2 + 0.12 + open_gap * 0.35, (y_top + y_bot) / 2 - 0.05, 0], [x_c + width / 2, y_bot, 0], color=col, stroke_width=4.5, stroke_opacity=op)
    cap = Arc(radius=width / 2, start_angle=0, angle=PI, arc_center=[x_c, y_top, 0], color=col, stroke_width=4.5, stroke_opacity=op)
    return VGroup(bg_tube, left_wall, flap1, flap2, cap)


def make_capillary_vessel(x_c=2.4, y_top=-2.1, y_bot=-3.55, width=0.90, brightened=True):
    """CRIMSON blood capillary with narrow wall gaps (0.16 units wide)."""
    op = 0.96 if brightened else 0.45
    fill_op = 0.34 if brightened else 0.14
    bg_tube = RoundedRectangle(
        corner_radius=0.18, width=width, height=y_top - y_bot,
        stroke_width=0, fill_color=CRIMSON, fill_opacity=fill_op,
    ).move_to([x_c, (y_top + y_bot) / 2, 0])
    left_segs = VGroup(
        Line([x_c - width / 2, y_top, 0], [x_c - width / 2, y_top - 0.45, 0], color=CRIMSON, stroke_width=4.8, stroke_opacity=op),
        Line([x_c - width / 2, y_top - 0.62, 0], [x_c - width / 2, y_bot + 0.42, 0], color=CRIMSON, stroke_width=4.8, stroke_opacity=op),
        Line([x_c - width / 2, y_bot + 0.25, 0], [x_c - width / 2, y_bot, 0], color=CRIMSON, stroke_width=4.8, stroke_opacity=op),
    )
    right_wall = Line([x_c + width / 2, y_top, 0], [x_c + width / 2, y_bot, 0], color=CRIMSON, stroke_width=4.8, stroke_opacity=op)
    cap = Arc(radius=width / 2, start_angle=0, angle=PI, arc_center=[x_c, y_top, 0], color=CRIMSON, stroke_width=4.8, stroke_opacity=op)
    return VGroup(bg_tube, left_segs, right_wall, cap)


def make_chylomicron(center=ORIGIN, radius=0.58, with_cargo=True, seed=23):
    """WHITE protein-wrapped sphere packed with rebuilt GREEN fat blocks + optional cargo specks."""
    rng = np.random.default_rng(seed)
    shell = Circle(
        radius=radius, color=WHITE, stroke_width=3.5,
        fill_color=GREEN, fill_opacity=0.42,
    ).move_to(center)
    blocks = VGroup()
    for dx, dy in [(-0.18, 0.16), (0.18, 0.15), (-0.16, -0.17), (0.17, -0.16)]:
        b = RoundedRectangle(
            corner_radius=0.05, width=0.26 * (radius / 0.58), height=0.20 * (radius / 0.58),
            color=GREEN, stroke_width=1.4, fill_color=GREEN, fill_opacity=0.85,
        ).move_to(center + np.array([dx * (radius / 0.58), dy * (radius / 0.58), 0.0]))
        blocks.add(b)
    cargo = VGroup()
    if with_cargo:
        for _ in range(4):
            a = rng.uniform(0, TAU)
            r = rng.uniform(0.08, 0.32) * (radius / 0.58)
            cargo.add(Dot(center + np.array([r * np.cos(a), r * np.sin(a), 0]), radius=0.05 * (radius / 0.58), color="#B8F29B"))
    g = VGroup(shell, blocks, cargo)
    g.shell, g.blocks, g.cargo = shell, blocks, cargo
    return g


def make_micelle(center=ORIGIN, radius=0.38, seed=31):
    """ORANGE bile-salt ring ferrying GREEN fatty acid & monoacylglycerol pieces."""
    rng = np.random.default_rng(seed)
    rim = Circle(radius=radius, color=ORANGE, stroke_width=4.2, fill_color=ORANGE, fill_opacity=0.14).move_to(center)
    specks = VGroup()
    for k in range(8):
        a = k * TAU / 8
        specks.add(Dot(center + radius * np.array([np.cos(a), np.sin(a), 0]), radius=0.058, color=ORANGE))
    pieces = VGroup()
    for dx, dy in [(-0.12, 0.08), (0.12, -0.06), (0.0, -0.13)]:
        p = RoundedRectangle(
            corner_radius=0.03, width=0.17, height=0.08,
            color=GREEN, fill_color=GREEN, fill_opacity=0.95, stroke_width=0,
        ).rotate(rng.uniform(-0.5, 0.5)).move_to(center + np.array([dx, dy, 0]))
        pieces.add(p)
    g = VGroup(rim, specks, pieces)
    g.rim, g.specks, g.pieces = rim, specks, pieces
    return g


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        lumen = make_lumen_bg()
        tag = scope_tag("schematic")
        self.add(lumen, tag)

        # Link-back ghost of the first film: dormant GREY zymogens flipped BLUE by GOLD trypsin
        z1 = make_zymogen("protease").move_to([-3.8, 1.15, 0])
        z2 = make_zymogen("protease").move_to([-3.8, -0.15, 0])
        tryp_box = RoundedRectangle(corner_radius=0.12, width=1.65, height=0.58, stroke_color=GOLD, stroke_width=3.0, fill_color=BG, fill_opacity=0.90).move_to([-1.35, -1.65, 0])
        tryp_lbl = T("trypsin", size=26, color=GOLD).move_to(tryp_box)
        tryp = VGroup(tryp_box, tryp_lbl)
        last_tag = T("last time", size=26, color=TEXT).move_to([-3.8, 2.25, 0])
        ghost_group = VGroup(last_tag, z1, z2, tryp).set_opacity(0.90)

        self.play(FadeIn(ghost_group), run_time=0.5)
        self.play(
            tryp.animate.move_to([-1.35, 0.5, 0]),
            z1.core.animate.set_color(BLUE).set_fill(BLUE, opacity=0.30),
            z2.core.animate.set_color(BLUE).set_fill(BLUE, opacity=0.30),
            FadeOut(z1.pro), FadeOut(z2.pro),
            run_time=1.8,
        )
        z1.remove(z1.pro)
        z2.remove(z2.pro)
        # Hold ghost steadily until right before 'Lipase' so there is NEVER an empty frame
        wait_to_lip = max(0.2, self.t_of("Lipase") - 0.65 - self.elapsed())
        if wait_to_lip > 0.25:
            self.play(tryp.animate.shift(RIGHT * 0.25), run_time=wait_to_lip, rate_func=linear)

        # On 'Lipase', large GREEN fat drop grows in after ghost fades out
        drop_center = np.array([0.0, -0.2, 0.0])
        drop, rim_bonds, inner_bonds = make_fat_drop_with_bonds(drop_center, radius=2.3, seed=7)
        lip_starts = [[-5.4, 2.0, 0], [5.4, 1.9, 0], [-5.3, -2.0, 0], [5.4, -1.9, 0]]
        lip_mids = [[-3.5, 1.45, 0], [3.5, 1.35, 0], [-3.4, -1.25, 0], [3.4, -1.15, 0]]
        lipases = VGroup(*[make_lipase(scale=1.18).move_to(p) for p in lip_starts])
        lip_label = always_redraw(lambda: T("lipase", size=28, color=BLUE).next_to(lipases[0], UP, buff=0.22))

        self.play(
            FadeOut(ghost_group),
            FadeIn(lipases), FadeIn(lip_label),
            run_time=0.45,
        )
        self.at("Lipase")
        self.play(
            GrowFromCenter(drop), FadeIn(rim_bonds), FadeIn(inner_bonds),
            run_time=0.9,
        )
        self.play(
            *[m.animate.move_to(p) for m, p in zip(lipases, lip_mids)],
            run_time=2.2,
            rate_func=linear,
        )

        # On 'secreted already active', each lipase pulses BLUE once cleanly
        self.at("secreted already active")
        halos = VGroup(*[
            Circle(radius=0.46, color=BLUE, stroke_width=4).move_to(m.get_center())
            for m in lipases
        ])
        halos.layout_ok = True
        self.play(
            *[FadeIn(h, scale=0.85) for h in halos],
            *[m[0].animate.set_fill(BLUE, opacity=1.0) for m in lipases],
            run_time=0.45,
        )
        self.play(
            *[FadeOut(h, scale=1.45) for h in halos],
            *[m[0].animate.set_fill(BLUE, opacity=0.92) for m in lipases],
            run_time=0.55,
        )

        # On 'why is fat', large white text at top while lipases glide toward drop
        self.at("why is fat")
        q_text = T("Why is fat the hard one?", size=38, color=TEXT).move_to([0.0, 3.08, 0.0])
        lip_ends = [[-3.05, 1.15, 0], [3.05, 1.05, 0], [-2.95, -0.95, 0], [2.95, -0.9, 0]]
        self.play(
            Write(q_text),
            *[m.animate.move_to(p) for m, p in zip(lipases, lip_ends)],
            run_time=1.8,
        )
        rest = max(0.3, self.narration_s + 0.35 - self.elapsed())
        self.play(
            *[m.animate.shift((drop_center - m.get_center()) * 0.08) for m in lipases],
            run_time=rest,
            rate_func=linear,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        lumen = make_lumen_bg()
        tag = scope_tag("schematic")
        drop_center = np.array([0.0, -0.2, 0.0])
        drop, rim_bonds, inner_bonds = make_fat_drop_with_bonds(drop_center, radius=2.3, seed=7)
        lip_pos = [[-2.82, 1.05, 0], [2.82, 0.96, 0], [-2.72, -0.88, 0], [2.72, -0.83, 0]]
        lipases = VGroup(*[make_lipase(scale=1.18).move_to(p) for p in lip_pos])
        q_text = T("Why is fat the hard one?", size=38, color=TEXT).move_to([0.0, 3.08, 0.0])
        title = T("Within Reach", size=46, color=TEXT, font=TITLE_FONT).move_to([0.0, 3.08, 0.0])

        self.add(lumen, tag, drop, rim_bonds, inner_bonds, lipases, q_text)

        t_wob = ValueTracker(0.0)
        drop_wob = always_redraw(
            lambda: drop.copy().stretch(1.0 + 0.020 * np.sin(t_wob.get_value() * 4.5), 0)
            .stretch(1.0 - 0.020 * np.sin(t_wob.get_value() * 4.5), 1)
        )
        self.remove(drop)
        self.add(drop_wob)

        lip_targets = [[-2.62, 0.98, 0], [2.62, 0.90, 0], [-2.56, -0.80, 0], [2.56, -0.76, 0]]
        self.play(
            swap(q_text, title, run_time=0.65),
            t_wob.animate(run_time=1.35, rate_func=linear).set_value(1.35),
            *[m.animate(run_time=1.35, rate_func=linear).move_to(p) for m, p in zip(lipases, lip_targets)],
        )
        self.play(
            FadeOut(title, run_time=0.45),
            t_wob.animate(run_time=0.55, rate_func=linear).set_value(1.9),
        )
        self.finish()


class S02Surface(SpokenScene):
    def construct(self):
        lumen = make_lumen_bg()
        tag = scope_tag("schematic")
        drop_center = np.array([0.0, -0.2, 0.0])
        R = 2.3
        drop, rim_bonds, inner_bonds = make_fat_drop_with_bonds(drop_center, radius=R, seed=7)
        lip_pos = [[-2.62, 0.98, 0], [2.62, 0.90, 0], [-2.56, -0.80, 0], [2.56, -0.76, 0]]
        lipases = VGroup(*[make_lipase(scale=1.18).move_to(p) for p in lip_pos])
        drop_lbl = T("fat drop", size=30, color=GREEN).move_to([0.0, 3.20, 0.0])

        self.add(lumen, tag, drop, rim_bonds, inner_bonds, lipases)
        self.at("one drop")
        self.play(FadeIn(drop_lbl), run_time=0.7)

        # Keep rim lightly breathing while waiting for 'will not dissolve'
        wait_w = max(0.1, self.t_of("will not dissolve") - 0.25 - self.elapsed())
        if wait_w > 0.25:
            self.play(*[b.animate.scale(1.12) for b in rim_bonds], run_time=wait_w, rate_func=linear)

        # On 'will not dissolve', computed water drops deflect off the hydrophobic drop boundary
        self.at("will not dissolve")
        rng = np.random.default_rng(13)
        y_offsets = [-1.6, -1.0, -0.4, 0.3, 1.0, 1.6, -1.3, -0.6, 0.1, 0.7, 1.3, 1.8]
        water_dots = VGroup(*[
            make_water_drop(
                [-5.9 if i % 2 == 0 else 5.9, drop_center[1] + y_offsets[i], 0.0],
                scale=0.85,
            )
            for i in range(len(y_offsets))
        ])
        self.play(FadeIn(water_dots), run_time=0.3)

        def water_path(start, dir_x):
            pts = [start.copy()]
            p = start.copy()
            for _ in range(20):
                dt = 0.24
                rel = p - drop_center
                dist = np.linalg.norm(rel)
                if dist < R + 0.30:
                    n = rel / max(dist, 1e-6)
                    tang = np.array([-n[1], n[0], 0.0])
                    if np.dot(tang, np.array([dir_x, 0.0, 0.0])) < 0:
                        tang = -tang
                    vel = tang * 2.3 + n * 0.65
                else:
                    vel = np.array([dir_x * 2.2, rng.uniform(-0.12, 0.12), 0.0])
                p = p + vel * dt
                rel2 = p - drop_center
                if np.linalg.norm(rel2) < R + 0.20:
                    p = drop_center + (R + 0.20) * rel2 / np.linalg.norm(rel2)
                pts.append(p.copy())
            m = VMobject()
            m.set_points_as_corners(pts)
            return m

        paths = [water_path(d.get_center(), 1.0 if i % 2 == 0 else -1.0) for i, d in enumerate(water_dots)]
        self.play(
            *[MoveAlongPath(d, p) for d, p in zip(water_dots, paths)],
            run_time=2.5,
            rate_func=linear,
        )
        self.play(FadeOut(water_dots), run_time=0.25)

        # On 'lipase reaches', lipase cutters land right on the rim beside the 3 rim bonds
        self.at("lipase reaches")
        rim_angles = [0.62, 2.35, 4.10]
        target_angles = [0.62, 2.35, 4.10, 5.45]
        rim_targets = [
            drop_center + (R + 0.36) * np.array([np.cos(a), np.sin(a), 0.0])
            for a in target_angles
        ]
        self.play(
            *[m.animate.move_to(p) for m, p in zip(lipases, rim_targets)],
            run_time=0.9,
        )

        # On 'bonds at the', rim bonds brighten and lipase snips them
        self.at("bonds at the")
        self.play(*[b.animate.set_fill(YELLOW, opacity=1.0).scale(1.3) for b in rim_bonds], run_time=0.4)
        snip_anims = []
        for b, a in zip(rim_bonds, rim_angles):
            tang = np.array([-np.sin(a), np.cos(a), 0.0]) * 0.30
            snip_anims.append(FadeOut(b, shift=tang, scale=0.4))
        self.play(*snip_anims, run_time=0.7)

        # Keep rim cutters jostling smoothly until 'Every bond inside waits'
        ang_track = ValueTracker(0.0)
        for i, m in enumerate(lipases):
            base_a = target_angles[i]
            m.add_updater(lambda mob, ba=base_a, idx=i: mob.move_to(
                drop_center + (R + 0.36) * np.array([
                    np.cos(ba + 0.14 * np.sin(ang_track.get_value() * 3.0 + idx)),
                    np.sin(ba + 0.14 * np.sin(ang_track.get_value() * 3.0 + idx)),
                    0.0,
                ])
            ))
        wait_in = max(0.1, self.t_of("Every bond inside waits") - 0.25 - self.elapsed())
        if wait_in > 0.2:
            self.play(ang_track.animate.set_value(wait_in), run_time=wait_in, rate_func=linear)

        # On 'Every bond inside waits', label inside the drop clear of interior bonds
        self.at("Every bond inside waits")
        out_lbl = T("out of reach", size=30, color=TEXT).move_to(drop_center)
        self.play(
            FadeIn(out_lbl),
            ang_track.animate.set_value(ang_track.get_value() + 0.7),
            run_time=0.65,
            rate_func=linear,
        )
        rest = max(0.4, self.narration_s + 0.35 - self.elapsed())
        self.play(
            ang_track.animate.set_value(ang_track.get_value() + rest),
            run_time=rest,
            rate_func=linear,
        )
        for m in lipases:
            m.clear_updaters()
        self.finish()


class S03Bile(SpokenScene):
    def construct(self):
        lumen = make_lumen_bg()
        tag = scope_tag("schematic")
        drop_center = np.array([0.0, -0.15, 0.0])
        R = 2.25
        drop, _, inner_bonds = make_fat_drop_with_bonds(drop_center, radius=R, seed=7)
        inner_bonds.set_opacity(0.90)
        lipases = VGroup(*[
            make_lipase(scale=1.0).move_to(p)
            for p in [[-5.2, 1.3, 0], [5.2, 1.3, 0], [-5.2, -1.3, 0], [5.2, -1.3, 0]]
        ])
        self.add(lumen, tag, drop, inner_bonds, lipases)

        # On 'Bile salts', ORANGE bile-salt specks swirl in from upper left and coat the drop
        self.at("Bile salts")
        bile_lbl = T("bile salts", size=28, color=ORANGE).move_to([-4.6, 2.95, 0])
        bile_specks = VGroup(*[
            Dot(radius=0.085, color=ORANGE).move_to([-5.6 + (k % 4) * 0.25, 2.4 - (k // 4) * 0.25, 0])
            for k in range(12)
        ])
        coat_ring = Circle(radius=R + 0.08, color=ORANGE, stroke_width=6.5, fill_opacity=0).move_to(drop_center)
        self.play(FadeIn(bile_lbl), FadeIn(bile_specks), run_time=0.45)

        self.at("break the drop apart")
        ring_targets = [
            drop_center + (R + 0.08) * np.array([np.cos(k * TAU / 12), np.sin(k * TAU / 12), 0])
            for k in range(12)
        ]
        self.play(
            *[s.animate.move_to(p) for s, p in zip(bile_specks, ring_targets)],
            Create(coat_ring),
            run_time=1.3,
        )
        self.play(FadeOut(bile_specks), FadeOut(bile_lbl), run_time=0.3)

        # Stage 1 split: 1 drop -> 8 well-separated medium droplets (r8 = 0.58, spaced on wide ellipse)
        r8 = 0.58
        angles8 = [k * TAU / 8 for k in range(8)]
        c8 = [drop_center + np.array([2.80 * np.cos(a), 1.85 * np.sin(a), 0]) for a in angles8]
        drops8 = VGroup(*[
            Circle(radius=r8, color=GREEN, stroke_width=2.6, fill_color=GREEN, fill_opacity=0.42).move_to(c)
            for c in c8
        ])
        coats8 = VGroup(*[
            Circle(radius=r8 + 0.06, color=ORANGE, stroke_width=4.5, fill_opacity=0).move_to(c)
            for c in c8
        ])
        b8_targets = [c8[i % 8] + np.array([0.18 * np.cos(i), 0.18 * np.sin(i), 0]) for i in range(len(inner_bonds))]

        self.play(
            ReplacementTransform(drop, drops8),
            ReplacementTransform(coat_ring, coats8),
            *[b.animate.move_to(p) for b, p in zip(inner_bonds, b8_targets)],
            run_time=2.1,
        )

        # On 'becomes a cloud', split 8 into 24 smaller droplets with YELLOW bonds at edges
        self.at("becomes a cloud")
        drops24, coats24, _, c24 = make_droplet_cloud(drop_center, n=24, radius=0.35, spread=(3.4, 1.80), seed=11)
        b24_targets = [
            c24[i * 2] + 0.26 * np.array([np.cos(i * 1.1), np.sin(i * 1.1), 0])
            for i in range(len(inner_bonds))
        ]
        self.play(
            ReplacementTransform(drops8, drops24),
            ReplacementTransform(coats8, coats24),
            *[b.animate.move_to(p).scale(0.8) for b, p in zip(inner_bonds, b24_targets)],
            run_time=2.0,
        )

        # On 'No bond has been cut', every YELLOW mark brightens whole + tag 'no bonds cut'
        self.at("No bond has been cut")
        no_cut_tag = boxed_label("no bonds cut", color=YELLOW, size=28, pad=0.16).move_to([0.0, 2.95, 0.0])
        self.play(
            FadeIn(no_cut_tag),
            *[b.animate.set_fill(YELLOW, opacity=1.0).scale(1.25) for b in inner_bonds],
            run_time=0.8,
        )

        # Keep subtle outward drift until 'pure geometry'
        wait_geo = max(0.1, self.t_of("pure geometry") - 0.25 - self.elapsed())
        if wait_geo > 0.2:
            self.play(drops24.animate.scale(1.02), coats24.animate.scale(1.02), run_time=wait_geo, rate_func=linear)

        # On 'pure geometry', ghost outline of original 1 drop appears behind cloud
        self.at("pure geometry")
        ghost_drop = DashedVMobject(
            Circle(radius=R, color=GREY, stroke_width=3.2).move_to(drop_center),
            num_dashes=36,
        )
        ghost_drop.layout_ok = True
        self.play(Create(ghost_drop), run_time=0.8)
        self.play(
            drops24.animate.scale(1.02),
            coats24.animate.scale(1.02),
            run_time=max(0.4, self.narration_s + 0.3 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        backdrop = make_predict_backdrop()
        lumen, drop, drop_outline, lbl_l, arrow, droplets, outlines, lbl_r, same_tag, scale_tag = backdrop
        self.add(lumen, scale_tag)

        q_card = T("How much more surface?", size=38, color=TEXT).move_to([0.0, 3.15, 0.0])

        self.at("Say bile splits")
        self.play(FadeIn(drop), FadeIn(lbl_l), run_time=0.75)
        self.play(Create(drop_outline), run_time=0.85)
        self.play(GrowArrow(arrow), run_time=0.65)

        self.at("into droplets")
        self.play(FadeIn(droplets), FadeIn(lbl_r), run_time=0.9)
        self.play(Create(outlines), run_time=1.8)

        self.at("total amount of fat")
        self.play(FadeIn(same_tag), run_time=0.9)

        wait_q = max(0.1, self.t_of("How much more surface") - 0.25 - self.elapsed())
        if wait_q > 0.2:
            self.play(outlines.animate.set_stroke(width=4.2), run_time=wait_q, rate_func=linear)

        self.at("How much more surface")
        self.play(Write(q_card), run_time=1.0)
        rest = max(0.4, self.narration_s + 0.35 - self.elapsed())
        self.play(
            outlines.animate.set_stroke(width=3.0),
            drop_outline.animate.set_stroke(width=7.0),
            run_time=rest,
            rate_func=linear,
        )
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = "How much more surface?"
    CARD = {"y": 3.15, "color": TEXT, "size": 38}
    RING_AT = (5.9, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        return make_predict_backdrop()


class S06Answer(SpokenScene):
    def construct(self):
        backdrop = make_predict_backdrop()
        lumen, drop, drop_outline, lbl_l, arrow, droplets, outlines, lbl_r, same_tag, scale_tag = backdrop
        q_card = T("How much more surface?", size=38, color=TEXT).move_to([0.0, 3.15, 0.0])
        self.add(lumen, drop, drop_outline, lbl_l, arrow, droplets, outlines, lbl_r, same_tag, scale_tag, q_card)

        # On 'thousand times more', scale ONLY picture shapes (never labels!) to left, rebuild labels at >=24pt
        self.at("thousand times more")
        ans_card = T("1,000 × the surface", size=40, color=GOLD).move_to([0.0, 3.15, 0.0])
        pic_shapes = VGroup(drop, drop_outline, arrow, droplets, outlines)
        new_lbl_l = T("1 mm across", size=24, color=TEXT).move_to([-4.95, -1.65, 0])
        new_lbl_r = T("1 µm each", size=24, color=TEXT).move_to([-0.85, -1.65, 0])
        new_same = boxed_label("same total fat", color=GREEN, size=24, pad=0.14).move_to([-2.85, 1.38, 0])

        self.play(
            swap(q_card, ans_card, run_time=0.6),
            pic_shapes.animate.scale(0.68).move_to([-2.75, -0.05, 0.0]),
            ReplacementTransform(lbl_l, new_lbl_l),
            ReplacementTransform(lbl_r, new_lbl_r),
            ReplacementTransform(same_tag, new_same),
            run_time=1.0,
        )

        # Computed broken-axis bar chart at right (x: 1.8..5.8, y: -2.0..2.0)
        x_ax = Line([1.8, -2.0, 0], [5.8, -2.0, 0], color=TEXT, stroke_width=3)
        y_bot = Line([1.8, -2.0, 0], [1.8, -0.65, 0], color=TEXT, stroke_width=3)
        y_top = Line([1.8, -0.25, 0], [1.8, 2.0, 0], color=TEXT, stroke_width=3)
        brk1 = Line([1.65, -0.72, 0], [1.95, -0.56, 0], color=GOLD, stroke_width=3)
        brk2 = Line([1.65, -0.42, 0], [1.95, -0.26, 0], color=GOLD, stroke_width=3)
        y_lbl = T("surface area", size=24, color=TEXT).move_to([2.55, 2.35, 0])
        bar_l_lbl = T("one drop", size=24, color=TEXT).move_to([2.85, -2.38, 0])
        bar_r_lbl = T("droplets", size=24, color=TEXT).move_to([4.75, -2.38, 0])

        bar1 = Rectangle(width=0.95, height=0.28, color=BLUE, fill_color=BLUE, fill_opacity=0.85, stroke_width=2).move_to([2.85, -2.0 + 0.14, 0])
        val1 = M("1×", size=24, color=TEXT).next_to(bar1, UP, buff=0.14)

        ratio_t = ValueTracker(1.0)

        def _tall_bar():
            v = ratio_t.get_value()
            if v <= 10.0:
                h = 0.28 + (v - 1.0) / 9.0 * 0.9
            else:
                h = 1.18 + (v - 10.0) / (SURFACE_RATIO - 10.0) * 2.52
            return Rectangle(
                width=0.95, height=h, color=BLUE, fill_color=BLUE, fill_opacity=0.90, stroke_width=2,
            ).move_to([4.75, -2.0 + h / 2.0, 0])

        bar2 = always_redraw(_tall_bar)
        val2 = always_redraw(lambda: M(f"{ratio_t.get_value():,.0f}×", size=26, color=GOLD).next_to(bar2, UP, buff=0.14))

        self.play(
            Create(x_ax), Create(y_bot), Create(y_top), Create(brk1), Create(brk2),
            FadeIn(y_lbl), FadeIn(bar_l_lbl), FadeIn(bar_r_lbl),
            FadeIn(bar1), FadeIn(val1),
            run_time=0.8,
        )
        self.add(bar2, val2)

        self.at("spreads over")
        self.play(ratio_t.animate.set_value(SURFACE_RATIO), run_time=2.8, rate_func=smooth)

        wait_lip = max(0.1, self.t_of("where lipase works") - 0.25 - self.elapsed())
        if wait_lip > 0.2:
            self.play(outlines.animate.set_stroke(width=4.0), run_time=wait_lip, rate_func=linear)

        # On 'where lipase works', spread-out BLUE lipase cutters dock across droplet patch + YELLOW bonds light up
        self.at("where lipase works")
        rng = np.random.default_rng(29)
        lip_starts = [[-6.0, 2.2, 0], [-6.1, 0.8, 0], [-6.0, -0.6, 0], [-5.9, -2.0, 0], [0.6, 2.1, 0], [0.6, -1.9, 0]]
        target_indices = [1, 14, 17, 29, 34, 46]
        lip_targets = [
            droplets[idx].get_center() + np.array([0.16, 0.10, 0])
            for idx in target_indices
        ]
        lip_swarm = VGroup(*[make_lipase(scale=0.55).move_to(p) for p in lip_starts])
        edge_bonds = VGroup(*[
            Dot(droplets[idx].get_center() + np.array([rng.uniform(-0.07, 0.07), -0.08, 0]), radius=0.052, color=YELLOW)
            for idx in range(0, 48, 3)
        ])
        self.play(
            FadeIn(lip_swarm),
            *[m.animate.move_to(p) for m, p in zip(lip_swarm, lip_targets)],
            FadeIn(edge_bonds),
            run_time=2.0,
        )
        self.play(
            *[b.animate.scale(1.35) for b in edge_bonds],
            *[m.animate.shift(LEFT * 0.08) for m in lip_swarm],
            run_time=max(0.4, self.narration_s + 0.35 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S07Cut(SpokenScene):
    def construct(self):
        lumen = make_lumen_bg()
        tag = scope_tag("schematic")
        self.add(lumen, tag)

        # Block cartoon of one triacylglycerol filling ~60% of frame height (height ~4.1)
        spine = RoundedRectangle(
            corner_radius=0.14, width=1.65, height=4.1,
            color=GREEN, stroke_width=3.2, fill_color=GREEN, fill_opacity=0.42,
        ).move_to([-1.65, -0.15, 0])
        spine_lbl = T("glycerol", size=26, color=TEXT).move_to(spine)

        tail_ys = [1.28, -0.15, -1.58]
        tails = VGroup(*[
            RoundedRectangle(
                corner_radius=0.12, width=3.15, height=0.74,
                color=GREEN, stroke_width=3.2, fill_color=GREEN, fill_opacity=0.42,
            ).move_to([1.45, y, 0])
            for y in tail_ys
        ])
        links = VGroup(*[
            RoundedRectangle(
                corner_radius=0.05, width=0.72, height=0.28,
                color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.95,
            ).move_to([-0.47, y, 0])
            for y in tail_ys
        ])
        mol_lbl = T("triacylglycerol", size=34, color=GREEN).move_to([0.0, 2.95, 0])

        self.play(
            FadeIn(spine), FadeIn(spine_lbl),
            FadeIn(links), FadeIn(tails), FadeIn(mol_lbl),
            run_time=0.48,
        )

        # On 'lipase cuts' and 'colipase', place labels cleanly to LEFT of enzyme (never touching spine!)
        self.at("lipase cuts")
        enz = make_lipase(with_colipase=True, scale=1.2).move_to([-4.2, 2.2, 0])
        enz_lbl = T("lipase", size=26, color=BLUE).next_to(enz[1], LEFT, buff=0.22)
        colip_lbl = T("colipase", size=24, color=LIGHT_BLUE).next_to(enz[0], LEFT, buff=0.22)
        enz_group = VGroup(enz, enz_lbl, colip_lbl)
        self.play(FadeIn(enz), FadeIn(enz_lbl), run_time=0.55)

        self.at("colipase")
        self.play(FadeIn(colip_lbl), enz_group.animate.move_to([-4.25, 1.32, 0]), run_time=1.3)

        # On 'two outer ester bonds', snap top and bottom YELLOW links one after another with water drops
        self.at("two outer ester bonds")
        w1 = make_water_drop([-0.47, 2.25, 0], scale=1.1)
        self.play(links[0].animate.scale(1.25), FadeIn(w1), run_time=0.55)
        self.play(w1.animate.move_to(links[0].get_center()), run_time=0.5)
        self.play(
            FadeOut(w1),
            FadeOut(links[0], scale=0.3),
            tails[0].animate.shift(RIGHT * 0.95 + UP * 0.2),
            run_time=0.8,
        )

        w2 = make_water_drop([-0.47, -2.55, 0], scale=1.1)
        self.play(
            enz_group.animate.move_to([-4.25, -1.58, 0]),
            links[2].animate.scale(1.25),
            FadeIn(w2),
            run_time=0.95,
        )
        self.play(w2.animate.move_to(links[2].get_center()), run_time=0.5)
        self.play(
            FadeOut(w2),
            FadeOut(links[2], scale=0.3),
            tails[2].animate.shift(RIGHT * 0.95 + DOWN * 0.2),
            run_time=0.8,
        )

        # On 'one monoacylglycerol' and 'two free fatty acids', pieces drift apart and relabel
        self.at("one monoacylglycerol")
        mono_lbl = T("monoacylglycerol", size=30, color=GREEN).move_to([-1.1, 2.95, 0])
        self.play(
            swap(mol_lbl, mono_lbl, run_time=0.65),
            FadeOut(enz_group),
            run_time=0.8,
        )

        self.at("two free fatty acids")
        fa1 = T("fatty acid", size=26, color=TEXT).move_to(tails[0].get_center() + RIGHT * 0.35)
        fa2 = T("fatty acid", size=26, color=TEXT).move_to(tails[2].get_center() + RIGHT * 0.35)
        self.play(
            tails[0].animate.shift(RIGHT * 0.35),
            tails[2].animate.shift(RIGHT * 0.35),
            FadeIn(fa1, run_time=0.45),
            FadeIn(fa2, run_time=0.45),
            run_time=0.65,
        )
        rest = max(0.3, self.narration_s + 0.35 - self.elapsed())
        self.play(
            VGroup(tails[0], fa1).animate.shift(RIGHT * 0.15 + UP * 0.08),
            VGroup(tails[2], fa2).animate.shift(RIGHT * 0.15 + DOWN * 0.08),
            run_time=rest,
            rate_func=linear,
        )
        self.finish()


class S08Idea(SpokenScene):
    def construct(self):
        lumen = make_lumen_bg()
        tag = scope_tag("schematic")
        self.add(lumen, tag)

        # Keep droplet cloud to the right (x >= -2.5) so left space is clean for 'pro' demo
        droplets, coats, bonds, _ = make_droplet_cloud(np.array([1.15, -0.25, 0.0]), n=16, radius=0.34, spread=(3.6, 1.8), seed=17)
        self.add(droplets, coats, bonds)

        self.at("one idea")
        idea_hdr = T("active enzyme + exposed bond", size=36, color=TEXT).move_to([0.0, 3.05, 0.0])
        self.play(Write(idea_hdr), droplets.animate.shift(RIGHT * 0.1), coats.animate.shift(RIGHT * 0.1), bonds.animate.shift(RIGHT * 0.1), run_time=1.4)

        # On 'never needed switching', ghost GREY 'pro' tab gets RED cross and fades
        self.at("never needed switching")
        lip_demo = make_lipase(scale=1.2).move_to([-4.95, 0.2, 0])
        pro_txt = T("pro", size=24, color=TEXT)
        pro_box = RoundedRectangle(corner_radius=0.08, width=pro_txt.width + 0.32, height=pro_txt.height + 0.24, stroke_color=GREY, stroke_width=2.2, fill_color=GREY, fill_opacity=0.28).next_to(lip_demo, RIGHT, buff=0.14)
        pro_txt.move_to(pro_box)
        pro_tab = VGroup(pro_box, pro_txt)
        cross = VGroup(
            Line(pro_box.get_corner(DL) + [-0.08, -0.08, 0], pro_box.get_corner(UR) + [0.08, 0.08, 0], color=RED, stroke_width=5),
            Line(pro_box.get_corner(UL) + [-0.08, 0.08, 0], pro_box.get_corner(DR) + [0.08, -0.08, 0], color=RED, stroke_width=5),
        )
        cross.layout_ok = True  # deliberate strike-through over the ghost 'pro' tab
        self.play(FadeIn(lip_demo), FadeIn(pro_tab), run_time=0.6)
        self.play(Create(cross), run_time=0.6)
        self.play(FadeOut(pro_tab), FadeOut(cross), run_time=0.6)

        wait_act = max(0.1, self.t_of("active enzyme cuts") - 0.25 - self.elapsed())
        if wait_act > 0.2:
            self.play(lip_demo.animate.shift(RIGHT * 0.35), run_time=wait_act, rate_func=linear)

        # On 'active enzyme cuts', large unreached drop vs 4 small droplets with active snipping
        self.at("active enzyme cuts")
        big_drop, _, big_in = make_fat_drop_with_bonds(np.array([-1.0, -0.25, 0.0]), radius=1.55, seed=9)
        small_grp = VGroup()
        small_coats = VGroup()
        small_edges = VGroup()
        small_lips = VGroup()
        small_centers = [[2.55, 0.78, 0], [4.35, 0.78, 0], [2.55, -0.95, 0], [4.35, -0.95, 0]]
        for p in small_centers:
            d = Circle(radius=0.44, color=GREEN, stroke_width=2.2, fill_color=GREEN, fill_opacity=0.45).move_to(p)
            c = Circle(radius=0.50, color=ORANGE, stroke_width=4.2, fill_opacity=0).move_to(p)
            b = make_bond_mark(np.array(p) + np.array([0.35, 0.0, 0]), angle=PI / 2, size=0.18)
            lp = make_lipase(scale=0.68).move_to(np.array(p) + np.array([0.78, 0.0, 0]))
            small_grp.add(d)
            small_coats.add(c)
            small_edges.add(b)
            small_lips.add(lp)

        self.play(
            FadeOut(droplets), FadeOut(coats), FadeOut(bonds), FadeOut(lip_demo),
            FadeIn(big_drop), FadeIn(big_in),
            FadeIn(small_grp), FadeIn(small_coats), FadeIn(small_edges), FadeIn(small_lips),
            run_time=1.0,
        )
        self.play(
            *[FadeOut(b, scale=0.3) for b in small_edges],
            *[lp.animate.shift(LEFT * 0.16) for lp in small_lips],
            run_time=1.0,
        )

        # Continuous enzyme stepping along the 4 small droplets until 'exposure'
        step_t = ValueTracker(0.0)
        for i, lp in enumerate(small_lips):
            c_pt = np.array(small_centers[i])
            lp.add_updater(lambda mob, cp=c_pt, idx=i: mob.move_to(
                cp + (0.66 + 0.10 * np.sin(step_t.get_value() * 5.0 + idx)) * np.array([
                    np.cos(1.1 * np.sin(step_t.get_value() * 2.5 + idx)),
                    np.sin(1.1 * np.sin(step_t.get_value() * 2.5 + idx)),
                    0.0,
                ])
            ))
        wait_exp = max(0.1, self.t_of("exposure") - 0.25 - self.elapsed())
        if wait_exp > 0.2:
            self.play(step_t.animate.set_value(wait_exp), run_time=wait_exp, rate_func=linear)

        # On 'exposure', ORANGE bile coats pulse once + exposure label
        self.at("exposure")
        exp_lbl = T("exposure", size=32, color=ORANGE).move_to([3.45, -2.15, 0])
        self.play(
            FadeIn(exp_lbl),
            *[c.animate.set_stroke(width=8) for c in small_coats],
            step_t.animate.set_value(step_t.get_value() + 0.55),
            run_time=0.55,
            rate_func=linear,
        )
        self.play(
            *[c.animate.set_stroke(width=4.2) for c in small_coats],
            step_t.animate.set_value(step_t.get_value() + 0.55),
            run_time=0.55,
            rate_func=linear,
        )
        for lp in small_lips:
            lp.clear_updaters()
        self.finish()


class S09Micelle(SpokenScene):
    def construct(self):
        lumen = make_lumen_bg(y_min=-0.45, y_max=3.8, opacity=0.10)
        tag = scope_tag("schematic")
        cells, bb = make_brush_border_row(y_top=-0.45, cell_h=1.55, highlight_center=True)
        lacteal_dim = make_lacteal_vessel(x_c=-1.6, y_top=-2.65, y_bot=-3.65, brightened=False)
        cap_dim = make_capillary_vessel(x_c=1.9, y_top=-2.65, y_bot=-3.65, brightened=False)
        cell_lbl = T("gut cell", size=28, color=TEXT).move_to([0.0, -1.22, 0])

        top_drops, top_coats, _, _ = make_droplet_cloud(np.array([0.0, 2.95, 0.0]), n=12, radius=0.26, spread=(4.5, 0.45), seed=5)
        rng = np.random.default_rng(41)
        loose_pieces = VGroup(*[
            RoundedRectangle(corner_radius=0.03, width=0.24, height=0.10, color=GREEN, fill_color=GREEN, fill_opacity=0.95, stroke_width=0)
            .rotate(rng.uniform(-0.6, 0.6))
            .move_to([x, y, 0])
            for x, y in [(-2.8, 1.7), (-2.3, 1.45), (-1.1, 1.85), (-0.7, 1.5), (0.8, 1.8), (1.3, 1.45), (2.6, 1.65), (3.1, 1.4)]
        ])
        bile_specks = VGroup(*[
            Dot(radius=0.065, color=ORANGE).move_to([x, y, 0])
            for x, y in [(-3.4, 2.15), (-2.0, 2.25), (-1.4, 2.05), (-0.2, 2.15), (0.4, 2.25), (1.6, 2.05), (2.2, 2.15), (3.4, 2.15)]
        ])

        self.add(lumen, tag, cells, bb, lacteal_dim, cap_dim, cell_lbl, top_drops, top_coats, loose_pieces, bile_specks)

        self.play(
            loose_pieces.animate.shift(DOWN * 0.3),
            bile_specks.animate.shift(DOWN * 0.3),
            run_time=2.8,
            rate_func=linear,
        )

        self.at("Bile salts gather")
        mic_xs = [-2.5, -0.8, 0.9, 2.6]
        micelles = VGroup(*[make_micelle(center=[x, 1.25, 0], radius=0.40, seed=31 + i) for i, x in enumerate(mic_xs)])
        self.at("micelles")
        mic_lbl = T("micelles", size=30, color=ORANGE).move_to([-4.6, 1.25, 0])
        self.play(
            FadeOut(loose_pieces), FadeOut(bile_specks),
            FadeIn(micelles), FadeIn(mic_lbl),
            run_time=1.3,
        )

        wait_ferry = max(0.1, self.t_of("ferry them") - 0.25 - self.elapsed())
        if wait_ferry > 0.2:
            self.play(*[m.animate.shift(DOWN * 0.2) for m in micelles], run_time=wait_ferry, rate_func=linear)

        self.at("ferry them")
        self.play(*[m.animate.move_to([x, 0.0, 0]) for m, x in zip(micelles, mic_xs)], run_time=1.4)

        released = VGroup(*[m.pieces.copy() for m in micelles])
        self.add(released)
        for m in micelles:
            m.remove(m.pieces)
        self.play(
            *[r.animate.move_to([0.0 + (i - 1.5) * 0.48, -0.78, 0]) for i, r in enumerate(released)],
            *[m.animate.move_to([x, 1.55, 0]) for m, x in zip(micelles, mic_xs)],
            run_time=max(1.2, self.narration_s + 0.35 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S10Rebuild(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        cell = RoundedRectangle(
            corner_radius=0.22, width=7.6, height=4.8,
            stroke_color=GREY, stroke_width=3.2, fill_color=GREY, fill_opacity=0.22,
        ).move_to([-1.4, -0.25, 0])
        bb_pts = [[-5.1 + k * (7.4 / 45.0), 2.15 + (0.14 if k % 2 == 0 else 0.0), 0.0] for k in range(46)]
        bb = VMobject(stroke_color=WHITE, stroke_width=3.5).set_points_as_corners(bb_pts)
        cell_hdr = T("inside the gut cell", size=28, color=TEXT).move_to([-1.4, -2.95, 0])
        self.add(tag, cell, bb, cell_hdr)

        free_val = ValueTracker(2.0)
        gauge_box = RoundedRectangle(
            corner_radius=0.14, width=3.2, height=3.4,
            stroke_color=GREY, stroke_width=2.4, fill_color=BG, fill_opacity=0.92,
        ).move_to([4.45, 0.0, 0])
        gauge_lbl = fit_text("free pieces inside", max_w=2.9, size=26, color=TEXT).move_to([4.45, 1.2, 0])
        gauge_track = Rectangle(width=0.75, height=1.7, color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.18).move_to([4.45, -0.2, 0])
        gauge_bar = always_redraw(
            lambda: Rectangle(
                width=0.71, height=max(0.12, 0.17 * free_val.get_value()),
                color=GREEN, stroke_width=0, fill_color=GREEN, fill_opacity=0.90,
            ).move_to([4.45, -1.05 + max(0.12, 0.17 * free_val.get_value()) / 2.0, 0])
        )
        gauge_note = T("low (schematic)", size=22, color=GREEN).move_to([4.45, -1.38, 0])

        spine1 = RoundedRectangle(corner_radius=0.06, width=0.45, height=1.35, color=GREEN, stroke_width=2.4, fill_color=GREEN, fill_opacity=0.45).move_to([-3.6, 0.0, 0])
        tails1 = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=1.1, height=0.28, color=GREEN, stroke_width=2.4, fill_color=GREEN, fill_opacity=0.55).move_to([-1.6, y, 0])
            for y in [0.45, 0.0, -0.45]
        ])
        links1 = VGroup(*[
            RoundedRectangle(corner_radius=0.03, width=0.35, height=0.14, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95, stroke_width=0).move_to([-3.1, y, 0])
            for y in [0.45, 0.0, -0.45]
        ])

        self.play(FadeIn(spine1), FadeIn(tails1), run_time=0.6)

        self.at("rebuilt into fat")
        rebuilt_lbl = T("rebuilt", size=28, color=GREEN).move_to([-2.7, 1.25, 0])
        self.play(
            *[t.animate.move_to([-2.38, y, 0]) for t, y in zip(tails1, [0.45, 0.0, -0.45])],
            FadeIn(links1),
            FadeIn(rebuilt_lbl),
            run_time=1.3,
        )

        self.at("Why undo digestion")
        why_txt = T("why undo it?", size=36, color=TEXT).move_to([-1.4, 3.05, 0])
        self.play(Write(why_txt), run_time=0.9)

        self.at("uses the pieces up")
        self.play(FadeIn(gauge_box), FadeIn(gauge_lbl), FadeIn(gauge_track), FadeIn(gauge_note), run_time=0.5)
        self.add(gauge_bar)

        spine2 = RoundedRectangle(corner_radius=0.06, width=0.45, height=1.35, color=GREEN, stroke_width=2.4, fill_color=GREEN, fill_opacity=0.45).move_to([-0.2, 0.0, 0])
        incoming = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=1.1, height=0.28, color=GREEN, stroke_width=2.4, fill_color=GREEN, fill_opacity=0.55).move_to([-0.8 + i * 1.1, 2.7, 0])
            for i in range(3)
        ])
        links2 = VGroup(*[
            RoundedRectangle(corner_radius=0.03, width=0.35, height=0.14, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95, stroke_width=0).move_to([0.3, y, 0])
            for y in [0.45, 0.0, -0.45]
        ])
        self.play(FadeIn(spine2), FadeIn(incoming), free_val.animate.set_value(3.3), run_time=0.8)
        self.play(
            *[t.animate.move_to([1.02, y, 0]) for t, y in zip(incoming, [0.45, 0.0, -0.45])],
            FadeIn(links2),
            free_val.animate.set_value(1.5),
            run_time=1.8,
        )

        # Wait gently while gauge breathes slightly up to 'stops free fatty acids'
        wait_det = max(0.1, self.t_of("stops free fatty acids") - 0.25 - self.elapsed())
        if wait_det > 0.2:
            self.play(free_val.animate.set_value(2.1), run_time=wait_det, rate_func=linear)

        # On 'stops free fatty acids', detergent ghost nudges membrane, then snaps onto a waiting third spine
        self.at("stops free fatty acids")
        spine3 = RoundedRectangle(corner_radius=0.06, width=0.45, height=0.75, color=GREEN, stroke_width=2.4, fill_color=GREEN, fill_opacity=0.45).move_to([-0.2, -1.55, 0])
        det_tail = RoundedRectangle(corner_radius=0.05, width=1.1, height=0.28, color=GREEN, stroke_width=2.4, fill_color=GREEN, fill_opacity=0.85).move_to([-0.5, 1.55, 0])
        det_ghost = RoundedRectangle(corner_radius=0.05, width=1.1, height=0.28, color=RED, stroke_width=3, fill_opacity=0).move_to([-0.5, 2.02, 0])
        det_lbl = T("no detergent damage", size=26, color=RED).move_to([0.4, 2.95, 0])
        link3 = RoundedRectangle(corner_radius=0.03, width=0.35, height=0.14, color=YELLOW, fill_color=YELLOW, fill_opacity=0.95, stroke_width=0).move_to([0.3, -1.55, 0])
        self.play(FadeOut(why_txt), FadeIn(det_tail), FadeIn(spine3), run_time=0.45)
        self.play(det_tail.animate.shift(UP * 0.42), FadeIn(det_ghost), FadeIn(det_lbl), run_time=0.9)
        self.play(
            FadeOut(det_ghost),
            det_tail.animate.move_to([1.02, -1.55, 0]),
            FadeIn(link3),
            free_val.animate.set_value(1.2),
            run_time=max(0.8, self.narration_s + 0.35 - self.elapsed()),
        )
        self.finish()


class S11Chylomicron(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic sizes")
        cell = RoundedRectangle(
            corner_radius=0.18, width=8.4, height=2.5,
            stroke_color=GREY, stroke_width=2.8, fill_color=GREY, fill_opacity=0.22,
        ).move_to([0.0, 2.05, 0])
        lacteal = make_lacteal_vessel(x_c=-3.0, y_top=-0.45, y_bot=-3.4, brightened=False)
        capillary = make_capillary_vessel(x_c=2.7, y_top=-0.45, y_bot=-3.4, width=0.95, brightened=True)
        cap_lbl = T("blood capillary", size=28, color=TEXT).move_to([4.75, -1.65, 0])

        rebuilt_blocks = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=0.44, height=0.32, color=GREEN, stroke_width=1.5, fill_color=GREEN, fill_opacity=0.80)
            .move_to([-0.5 + (i % 2) * 0.56, 2.25 - (i // 2) * 0.44, 0])
            for i in range(4)
        ])
        self.add(tag, cell, lacteal, capillary, cap_lbl, rebuilt_blocks)

        self.at("wrapped in protein")
        chylo = make_chylomicron(center=np.array([-0.25, 2.0, 0]), radius=0.62)
        chylo_lbl = T("chylomicron", size=28, color=TEXT).next_to(chylo, UP, buff=0.22)
        self.play(ReplacementTransform(rebuilt_blocks, chylo), FadeIn(chylo_lbl), run_time=1.1)

        self.at("shipped out")
        # Keep label above chylomicron as it exits into the villus core so their paths never cross
        self.play(
            chylo.animate.move_to([0.2, -0.95, 0]),
            chylo_lbl.animate.move_to([0.2, 0.05, 0]),
            run_time=1.4,
        )

        wait_big = max(0.1, self.t_of("far larger than") - 0.25 - self.elapsed())
        if wait_big > 0.2:
            self.play(
                chylo.animate.shift(RIGHT * 0.35),
                chylo_lbl.animate.shift(RIGHT * 0.35),
                run_time=wait_big,
                rate_func=linear,
            )

        self.at("far larger than")
        self.play(
            chylo.animate.move_to([1.52, -1.05, 0]),
            chylo_lbl.animate.move_to([1.1, 0.05, 0]),
            run_time=1.1,
        )
        padlock = make_padlock(center=np.array([2.25, -1.05, 0]), scale=0.95)
        self.play(
            FadeIn(padlock),
            chylo.animate.move_to([0.75, -1.05, 0]),
            chylo_lbl.animate.move_to([0.75, 0.05, 0]),
            run_time=0.9,
        )
        self.play(
            chylo.animate.move_to([0.45, -1.05, 0]),
            chylo_lbl.animate.move_to([0.45, 0.05, 0]),
            run_time=max(0.4, self.narration_s + 0.35 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S12Lacteal(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        cell = RoundedRectangle(
            corner_radius=0.18, width=8.4, height=2.2,
            stroke_color=GREY, stroke_width=2.8, fill_color=GREY, fill_opacity=0.22,
        ).move_to([0.0, 2.25, 0])
        lacteal = make_lacteal_vessel(x_c=-2.6, y_top=-0.25, y_bot=-3.4, width=1.25, open_gap=0.0, brightened=False)
        capillary = make_capillary_vessel(x_c=3.0, y_top=-0.25, y_bot=-3.4, width=0.95, brightened=False)
        chylo1 = make_chylomicron(center=np.array([0.45, -1.05, 0]), radius=0.56)
        chylo2 = make_chylomicron(center=np.array([-0.3, 2.25, 0]), radius=0.56)
        self.add(tag, cell, lacteal, capillary, chylo1, chylo2)

        # Gentle approach while intro line runs (keep chylo2 inside cell y >= 1.75)
        self.play(chylo1.animate.shift(LEFT * 0.4), chylo2.animate.shift(DOWN * 0.35), run_time=1.8, rate_func=linear)

        self.at("lymph vessel")
        lacteal_bright = make_lacteal_vessel(x_c=-2.6, y_top=-0.25, y_bot=-3.4, width=1.25, open_gap=0.25, brightened=True)
        lac_lbl = T("lacteal (lymph)", size=28, color=PURPLE).move_to([-4.95, -0.5, 0])
        self.play(ReplacementTransform(lacteal, lacteal_bright), FadeIn(lac_lbl), run_time=1.0)

        self.at("loose junctions")
        lacteal_open = make_lacteal_vessel(x_c=-2.6, y_top=-0.25, y_bot=-3.4, width=1.25, open_gap=0.75, brightened=True)
        self.play(ReplacementTransform(lacteal_bright, lacteal_open), run_time=0.9)

        self.at("Chylomicrons slip through")
        self.play(
            chylo1.animate.move_to([-2.6, -1.15, 0]),
            chylo2.animate.move_to([0.0, -0.75, 0]),
            run_time=1.4,
        )

        self.at("scenic route")
        lymph_lbl = T("lymph", size=30, color=PURPLE).move_to([-4.6, -2.85, 0])
        self.play(
            FadeIn(lymph_lbl, run_time=0.45),
            chylo1.animate.move_to([-2.6, -2.55, 0]),
            chylo2.animate.move_to([-2.6, -1.15, 0]),
            run_time=2.1,
            rate_func=linear,
        )

        self.at("Cholesterol")
        ride_lbl = T("along for the ride", size=26, color=GREEN).move_to([0.1, -2.4, 0])
        self.play(
            FadeIn(ride_lbl, run_time=0.45),
            chylo1.cargo.animate.scale(1.6),
            chylo2.cargo.animate.scale(1.6),
            chylo1.animate.move_to([-2.6, -2.85, 0]),
            chylo2.animate.move_to([-2.6, -1.45, 0]),
            run_time=max(0.8, self.narration_s + 0.35 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S13Sort(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        cell = RoundedRectangle(
            corner_radius=0.18, width=8.4, height=2.1,
            stroke_color=GREY, stroke_width=2.8, fill_color=GREY, fill_opacity=0.22,
        ).move_to([-0.5, 2.35, 0])
        lacteal = make_lacteal_vessel(x_c=-3.4, y_top=-0.25, y_bot=-3.4, width=1.2, open_gap=0.45, brightened=True)
        lac_lbl = T("lymph", size=28, color=PURPLE).move_to([-5.15, -2.7, 0])

        cap_bg = RoundedRectangle(corner_radius=0.18, width=0.95, height=3.15, stroke_width=0, fill_color=CRIMSON, fill_opacity=0.35).move_to([1.4, -1.8, 0])
        cap_l = VGroup(
            Line([0.92, -0.25, 0], [0.92, -0.75, 0], color=CRIMSON, stroke_width=4.8),
            Line([0.92, -1.02, 0], [0.92, -2.15, 0], color=CRIMSON, stroke_width=4.8),
            Line([0.92, -2.42, 0], [0.92, -3.35, 0], color=CRIMSON, stroke_width=4.8),
        )
        cap_cap = Arc(radius=0.475, start_angle=0, angle=PI, arc_center=[1.4, -0.25, 0], color=CRIMSON, stroke_width=4.8)
        portal_line = Line([1.88, -1.95, 0], [4.1, -1.95, 0], color=CRIMSON, stroke_width=14, stroke_opacity=0.55)
        liver = Polygon(
            [4.05, -0.9, 0], [5.95, -1.2, 0], [5.85, -2.55, 0], [4.15, -2.55, 0],
            color=CRIMSON, stroke_width=3.8, fill_color=CRIMSON, fill_opacity=0.35,
        )
        liver_lbl = T("liver", size=28, color=TEXT).move_to([5.0, -1.35, 0])
        portal_lbl = T("portal blood", size=26, color=TEXT).move_to([2.95, -2.65, 0])

        # Chylomicrons flowing down PURPLE lymph path cleanly inside frame (y >= -2.9)
        c_ly1 = make_chylomicron(center=np.array([-3.4, -0.8, 0]), radius=0.45)
        c_ly2 = make_chylomicron(center=np.array([-3.4, -1.95, 0]), radius=0.45)

        self.add(tag, cell, lacteal, lac_lbl, cap_bg, cap_l, cap_cap, portal_line, liver, liver_lbl, portal_lbl, c_ly1, c_ly2)

        # Continuous lymph flow during opening sentence
        self.play(
            c_ly1.animate.shift(DOWN * 0.35),
            c_ly2.animate.shift(DOWN * 0.30),
            run_time=2.5,
            rate_func=linear,
        )

        # Place both labels clearly to the right of the particle path, between cell bottom and capillary cap
        self.at("Sugars")
        sugars = VGroup(*[Dot([x, 1.55, 0], radius=0.08, color=WHITE) for x in [-0.7, -0.2, 0.3]])
        sug_lbl = T("sugars, amino acids", size=26, color=TEXT).move_to([1.25, 0.90, 0], aligned_edge=LEFT)
        self.play(
            FadeIn(sugars), FadeIn(sug_lbl),
            c_ly1.animate.shift(DOWN * 0.25),
            c_ly2.animate.shift(DOWN * 0.22),
            run_time=1.3,
        )

        self.at("short and medium")
        stubs = VGroup(*[
            RoundedRectangle(corner_radius=0.03, width=0.26, height=0.10, color=GREEN, fill_color=GREEN, fill_opacity=0.95, stroke_width=0).move_to([x, 1.18, 0])
            for x in [-0.6, 0.1]
        ])
        stub_lbl = T("short, medium chains", size=24, color=GREEN).move_to([1.25, 0.46, 0], aligned_edge=LEFT)
        self.play(
            FadeIn(stubs), FadeIn(stub_lbl),
            sugars.animate.move_to([0.2, -0.88, 0]),
            c_ly1.animate.shift(DOWN * 0.22),
            c_ly2.animate.shift(DOWN * 0.20),
            run_time=2.2,
        )

        wait_port = max(0.1, self.t_of("leave for the portal blood") - 0.25 - self.elapsed())
        if wait_port > 0.2:
            self.play(
                stubs.animate.move_to([0.35, -1.65, 0]),
                sugars.animate.move_to([1.35, -1.95, 0]),
                run_time=wait_port,
                rate_func=linear,
            )

        # Route sugars & stubs into lower portal blood & lower liver edge (never covering 'liver' at y = -1.35!)
        self.at("leave for the portal blood")
        self.play(
            FadeOut(sug_lbl), FadeOut(stub_lbl),
            sugars.animate.move_to([4.55, -2.08, 0]),
            stubs.animate.move_to([3.35, -2.08, 0]),
            c_ly1.animate.shift(DOWN * 0.25),
            c_ly2.animate.shift(DOWN * 0.20),
            run_time=max(1.2, self.narration_s + 0.35 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        lumen = make_lumen_bg(y_min=0.55, y_max=3.8, opacity=0.10)
        tag = scope_tag("schematic")
        cells, bb = make_brush_border_row(y_top=0.55, cell_h=1.25, highlight_center=False)
        lacteal = make_lacteal_vessel(x_c=-2.6, y_top=-1.35, y_bot=-3.45, width=1.18, open_gap=0.55, brightened=True)
        capillary = make_capillary_vessel(x_c=2.4, y_top=-1.35, y_bot=-3.45, width=0.92, brightened=True)

        clouds, coats, _, _ = make_droplet_cloud(np.array([-2.8, 1.95, 0.0]), n=10, radius=0.25, spread=(2.2, 0.6), seed=3)
        lipases = VGroup(*[make_lipase(scale=0.68).move_to(p) for p in [[-4.7, 2.35, 0], [-1.0, 2.25, 0], [-2.7, 1.25, 0]]])
        mic1 = make_micelle(center=np.array([0.8, 1.85, 0]), radius=0.35, seed=4)
        mic2 = make_micelle(center=np.array([2.4, 1.65, 0]), radius=0.35, seed=5)
        chylo = make_chylomicron(center=np.array([-1.05, -1.55, 0]), radius=0.45)
        sugars = VGroup(*[Dot([2.4, -1.30 - 0.42 * i, 0], radius=0.075, color=WHITE) for i in range(3)])

        self.add(lumen, tag, cells, bb, lacteal, capillary, clouds, coats, lipases, mic1, mic2, chylo, sugars)

        # Continuous motion while intro sentence plays
        self.play(
            mic1.animate.shift(DOWN * 0.25),
            mic2.animate.shift(DOWN * 0.20),
            sugars.animate.shift(DOWN * 0.25),
            run_time=2.2,
            rate_func=linear,
        )

        self.at("access, not activation")
        hdr = T("access, not activation", size=36, color=TEXT).move_to([1.5, 3.05, 0])
        self.play(
            Write(hdr),
            *[lp[0].animate.set_fill(BLUE, opacity=1.0).scale(1.15) for lp in lipases],
            run_time=0.85,
        )
        self.play(*[lp[0].animate.scale(1 / 1.15) for lp in lipases], run_time=0.55)

        wait_s1 = max(0.1, self.t_of("Make surface") - 0.25 - self.elapsed())
        if wait_s1 > 0.2:
            self.play(sugars.animate.shift(DOWN * 0.15), run_time=wait_s1, rate_func=linear)

        self.at("Make surface")
        s1_lbl = T("1. surface", size=28, color=ORANGE).move_to([-4.9, 3.05, 0])
        self.play(
            FadeIn(s1_lbl),
            *[c.animate.set_stroke(width=6.8) for c in coats],
            run_time=0.65,
        )

        self.at("ferry the pieces")
        s2_lbl = T("2. ferry", size=28, color=ORANGE).move_to([4.5, 1.95, 0])
        self.play(
            FadeIn(s2_lbl),
            mic1.animate.shift(DOWN * 0.50),
            mic2.animate.shift(DOWN * 0.20),
            sugars.animate.shift(DOWN * 0.25),
            run_time=1.0,
        )

        self.at("door wide enough")
        s3_lbl = T("3. wide door", size=28, color=PURPLE).move_to([-5.0, -2.1, 0])
        self.play(
            FadeIn(s3_lbl, run_time=0.35),
            chylo.animate.move_to([-2.6, -1.75, 0]),
            sugars.animate.shift(DOWN * 0.30),
            run_time=1.2,
            rate_func=linear,
        )
        self.play(
            chylo.animate.shift(DOWN * 0.75),
            sugars.animate.shift(DOWN * 0.20),
            run_time=max(0.4, self.narration_s + 0.35 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S15End(EndCard):
    LINE = "Lipase is born switched on; fat's problem is reach."
