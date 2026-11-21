"""
Sealed Rooms, Safe Passage — Intro Biochemistry & Cell Biology, Chapter 2

COLOUR MAP (one colour per concept for the whole film):
- BLUE   = membrane (cell outline, rough ER ribbons, Golgi plates, lysosome wall, transport bubbles)
- GOLD   = GM2 (link-back to first film in s00 only)
- TEAL   = lysosome's digestive enzymes (six animated pair-of-jaws shapes, plus trafficked/escaped jaws)
- GREEN  = delivery into the lysosome (delivery bubbles and safe check mark in s04)
- PURPLE = small parts (broken-down protein/cargo dots; also soft lavender Golgi tint in s05)
- RED    = trouble / cytosol's protein-destroying machinery (drifting RED barrel icon; large-leak warning in s08)
- PINK   = acidic interior (lysosome interior, acid lock, computed H+ ion dots in s09)
- ORANGE = new protein made for export (rounded folded ribbon blob, cartoon only; insulin chip in s04; faint ER tint in s05)
- TEXT   = labels, folding enzymes cups, disulfide clip, sugar chain beads, held-back bar, cargo shapes, pH 7.2 chip

CARRIED WORLD:
A large rounded BLUE cell outline centered at [-1.1, -0.35, 0] (10.0 x 6.0 units, ~75% of frame height),
leaving top band (y > 2.65) for titles/questions and right exterior (x > 3.9) for secreted insulin.
Inside, kept in the same places across scenes:
- rough ER at left ([-4.2, 0.25, 0]): three stacked folded BLUE ribbons with ribosome dots, labelled 'rough ER'
- Golgi at centre ([-0.8, 0.25, 0]): four curved BLUE plates, labelled 'Golgi'
- lysosome at lower right ([2.0, -1.45, 0], r=0.96): PINK interior, BLUE wall, six opening/closing TEAL jaws, labelled 'lysosome'
- protein destroyer at lower left cytosol ([-3.7, -1.90, 0]): plain RED barrel drifting slowly via updater, labelled 'protein destroyer'
Close-ups ease cleanly into rough ER (s03) and lysosome (s06-s10) and pull back to the whole cell (s11).

WHAT CHANGES ON SCREEN (and what it is computed from):
- s00_link_and_question: Swollen first-film lysosome with 4 computed layers of GOLD GM2 lozenges eases to normal size as GOLD fades, 6 TEAL jaws start snapping, camera pulls back to whole cell, ORANGE blob forms, RED barrel drifts, dashed ORANGE route draws.
- s01_title: Question card and dashed route fade out as title fades in above the living cell (jaws snapping, barrel drifting).
- s02_belt: ORANGE blob buds from ER inside a BLUE bubble, merges through 4 Golgi plates in sequence, buds toward cell surface while 3 route chips light in turn and cytosol tints.
- s03_checked: Camera zooms into rough ER; loose ORANGE ribbon folds inside closing TEXT cups, disulfide clip snaps, branched sugar beads attach; tangled misfolded blob bounces off held-back bar then exits to cytosol where RED barrel shreds it into PURPLE dots (seed=7).
- s04_never_meets: Drifting RED barrel bumps and slides off waiting BLUE bubble; bubble fuses with plasma membrane, releasing 3 ORANGE insulin blobs outside.
- s05_idea: Three rooms tint in sequence (ER faint ORANGE, Golgi faint PURPLE, lysosome PINK) with brightening walls; GREEN-outlined delivery bubble merges into lysosome; jaws and PINK interior pulse.
- s06_predict: TEAL jaw rides BLUE bubble ER -> Golgi -> lysosome; camera zooms to lysosome + cytosol strip; dashed escaped TEAL jaw appears beside 3 cell protein blobs; question card slides up.
- s07_think: PredictPause holds question for 4.5 s with countdown ring running and lysosome TEAL jaws opening/closing.
- s08_answer: Computed schematic activity bars compare full TEAL (lysosome) vs near-empty (escaped); inside jaws snap fast while escaped jaw barely opens/closes on intact blob; 8 dashed jaws and RED tint flash for large leak then recede to 1 jaw.
- s09_acid: pH 4.5-5 vs pH 7.2 chips and 2.5-unit ladder (x10, x10, about x3); two equal squares show 1 vs 316 jiggling PINK dots computed from 10**(7.2 - 4.7) = 316 (seed=7).
- s10_membrane: Lysosome BLUE wall thickens; 2 TEAL jaws bump inner wall and rebound; GREEN-outlined bubble delivers 3 cargo shapes that TEAL jaws cut into PURPLE dots; both lock chips pulse.
- s11_return: Camera pulls back to whole cell; fresh ORANGE blob rides sealed rooms ER -> Golgi -> surface past drifting RED barrel while lock chips glow and each room pulses in turn.
- s12_end: Standard EndCard with take-home line.
"""
from bp_parts import *

# Carried cell layout constants
CELL_CENTER = np.array([-1.1, -0.35, 0.0])
CELL_W = 10.0
CELL_H = 6.0
CELL_R = 1.45

ER_CENTER = np.array([-4.2, 0.25, 0.0])
GOLGI_CENTER = np.array([-0.8, 0.25, 0.0])
LYSO_CENTER = np.array([2.0, -1.45, 0.0])
LYSO_R = 0.96
BARREL_CENTER = np.array([-3.7, -1.90, 0.0])

# Zoomed lysosome layout (s06-s10)
Z_LYSO_CENTER = np.array([2.6, 0.55, 0.0])
Z_LYSO_R = 2.25


# ------------------------------------------------------------------ builders
def make_jaw(radius=0.22, color=TEAL, angle=0.55, dashed=False):
    """A pair-of-jaws digestive enzyme shape (upper + lower wedge) that opens/closes."""
    def half_wedge(upper=True):
        a = angle * 0.5
        poly = VMobject(stroke_color=color, stroke_width=2.5, fill_color=color,
                        fill_opacity=0.0 if dashed else 0.88)
        poly.set_points_as_corners([
            ORIGIN,
            *[np.array([radius * np.cos(t), radius * np.sin(t), 0.0])
              for t in (np.linspace(a, PI, 14) if upper else np.linspace(PI, TAU - a, 14))],
            ORIGIN,
        ])
        if dashed:
            return DashedVMobject(poly, num_dashes=10, dashed_ratio=0.55).set_stroke(color, 2.5)
        return poly

    g = VGroup(half_wedge(True), half_wedge(False))
    g._anchor = np.array(ORIGIN)
    return g


def set_jaw_angle(jaw, angle, radius=0.22):
    """Update a non-dashed jaw's mouth angle smoothly around its fixed anchor."""
    a = float(np.clip(angle, 0.08, 1.25)) * 0.5
    c = getattr(jaw, "_anchor", jaw.get_center())
    up_pts = [c, *[c + np.array([radius * np.cos(t), radius * np.sin(t), 0.0])
                   for t in np.linspace(a, PI, 14)], c]
    lo_pts = [c, *[c + np.array([radius * np.cos(t), radius * np.sin(t), 0.0])
                   for t in np.linspace(PI, TAU - a, 14)], c]
    jaw[0].set_points_as_corners(up_pts)
    jaw[1].set_points_as_corners(lo_pts)


def animate_jaws(jaws, radii, speed=5.0, base_phase=0.0, swim_amp=0.06):
    """Attach a deterministic opening/closing + subtle swimming updater to TEAL jaws."""
    for i, (jaw, rad) in enumerate(zip(jaws, radii)):
        jaw._jaw_t = base_phase + i * 0.9

        def _u(m, dt, r=rad, sp=speed, idx=i):
            m._jaw_t += dt * sp
            ang = 0.56 + 0.50 * np.sin(m._jaw_t)
            base_anchor = getattr(m, "_base_anchor", m._anchor)
            m._base_anchor = base_anchor
            drift = swim_amp * np.array([np.cos(0.45 * m._jaw_t + idx), np.sin(0.55 * m._jaw_t + idx * 1.3), 0.0])
            m._anchor = base_anchor + drift
            set_jaw_angle(m, ang, radius=r)

        jaw.add_updater(_u)


def make_barrel(center=BARREL_CENTER, scale=1.0):
    """Plain RED barrel icon representing cytosol's protein-destroying machinery."""
    w, h = 0.72 * scale, 0.90 * scale
    body = RoundedRectangle(corner_radius=0.16 * scale, width=w, height=h,
                            stroke_color=RED, stroke_width=4.5,
                            fill_color=RED, fill_opacity=0.35)
    band1 = Line(LEFT * w * 0.46 + UP * h * 0.18, RIGHT * w * 0.46 + UP * h * 0.18,
                 color=RED, stroke_width=3.5)
    band2 = Line(LEFT * w * 0.46 + DOWN * h * 0.18, RIGHT * w * 0.46 + DOWN * h * 0.18,
                 color=RED, stroke_width=3.5)
    cap = Line(LEFT * w * 0.34 + UP * h * 0.38, RIGHT * w * 0.34 + UP * h * 0.38,
               color=RED, stroke_width=2.5)
    return VGroup(body, band1, band2, cap).move_to(center)


def add_barrel_drift(barrel, anchor=BARREL_CENTER, ax=0.52, ay=0.18, speed=1.15, phase=0.0):
    """Slow bounded drift in lower-left cytosol via updater."""
    barrel._bt = phase

    def _u(m, dt):
        m._bt += dt * speed
        offset = np.array([ax * np.sin(m._bt), ay * np.sin(1.4 * m._bt + 0.5), 0.0])
        m.move_to(anchor + offset)

    barrel.add_updater(_u)
    return barrel


def make_orange_blob(center=ORIGIN, scale=1.0, tangled=False, loose=False):
    """Cartoon folded ORANGE export protein (no molecular structure)."""
    if loose:
        pts = [[-0.38, 0.18], [-0.18, -0.18], [0.02, 0.20], [0.22, -0.16], [0.38, 0.12]]
        curve = VMobject(stroke_color=ORANGE, stroke_width=7 * scale)
        curve.set_points_smoothly([center + np.array([x * scale, y * scale, 0.0]) for x, y in pts])
        return VGroup(curve)
    if tangled:
        pts = [[-0.28, 0.16], [0.16, 0.24], [-0.18, -0.08], [0.26, -0.16], [-0.08, -0.24], [0.18, 0.08]]
        curve = VMobject(stroke_color=ORANGE, stroke_width=6.5 * scale)
        curve.set_points_smoothly([center + np.array([x * scale, y * scale, 0.0]) for x, y in pts])
        bg = Circle(radius=0.28 * scale, stroke_color=ORANGE, stroke_width=2,
                    fill_color=ORANGE, fill_opacity=0.22).move_to(center)
        return VGroup(bg, curve)
    outer = RoundedRectangle(corner_radius=0.18 * scale, width=0.52 * scale, height=0.38 * scale,
                             stroke_color=ORANGE, stroke_width=3.5, fill_color=ORANGE, fill_opacity=0.85)
    fold = Arc(radius=0.13 * scale, start_angle=0.3, angle=2.4, arc_center=ORIGIN,
               stroke_color=BG, stroke_width=2.5).shift(UP * 0.02 * scale)
    return VGroup(outer, fold).move_to(center)


def make_bubble(cargo, center=ORIGIN, radius=0.40, outline=BLUE, halo=None):
    """A sealed BLUE membrane vesicle carrying cargo inside."""
    shell = Circle(radius=radius, stroke_color=outline, stroke_width=4.0,
                   fill_color=outline, fill_opacity=0.18).move_to(center)
    grp = VGroup(shell)
    if halo is not None:
        ring = Circle(radius=radius + 0.07, stroke_color=halo, stroke_width=4.5, fill_opacity=0).move_to(center)
        grp.add(ring)
    cargo.move_to(center)
    grp.add(cargo)
    grp.shell = shell
    grp.cargo = cargo
    return grp


def make_rough_er(center=ER_CENTER, scale=1.0, fill_color=BLUE, fill_opacity=0.15):
    """Three stacked, folded BLUE ribbons with dark ribosome dots on outer surface."""
    ribbons = VGroup()
    dots = VGroup()
    widths = [2.10, 2.30, 2.00]
    offsets_y = [0.85, 0.0, -0.85]
    for w, dy in zip(widths, offsets_y):
        rib = RoundedRectangle(corner_radius=0.28 * scale, width=w * scale, height=0.54 * scale,
                               stroke_color=BLUE, stroke_width=4.0,
                               fill_color=fill_color, fill_opacity=fill_opacity)
        rib.move_to(center + UP * dy * scale)
        ribbons.add(rib)
        for dx in np.linspace(-0.76 * w / 2, 0.76 * w / 2, 5):
            for sign in (1, -1):
                d = Dot(rib.get_center() + np.array([dx * scale, sign * 0.29 * scale, 0.0]),
                        radius=0.052 * scale, color=BG, stroke_color=BLUE, stroke_width=1.8)
                dots.add(d)
    n1 = Line(center + np.array([-0.72 * scale, 0.58 * scale, 0]),
              center + np.array([-0.72 * scale, 0.27 * scale, 0]), color=BLUE, stroke_width=3.5)
    n2 = Line(center + np.array([0.72 * scale, -0.27 * scale, 0]),
              center + np.array([0.72 * scale, -0.58 * scale, 0]), color=BLUE, stroke_width=3.5)
    bridges = VGroup(n1, n2)
    grp = VGroup(ribbons, bridges, dots)
    grp.ribbons = ribbons
    grp.bridges = bridges
    grp.dots = dots
    return grp


def make_golgi(center=GOLGI_CENTER, scale=1.0, fill_color=BLUE, fill_opacity=0.15):
    """Four curved BLUE cisterna plates stacked left to right."""
    plates = VGroup()
    xs = [-0.84, -0.28, 0.28, 0.84]
    heights = [1.85, 2.15, 2.05, 1.75]
    for dx, h in zip(xs, heights):
        p = RoundedRectangle(corner_radius=0.16 * scale, width=0.32 * scale, height=h * scale,
                             stroke_color=BLUE, stroke_width=4.0,
                             fill_color=fill_color, fill_opacity=fill_opacity)
        p.move_to(center + RIGHT * dx * scale)
        plates.add(p)
    return plates


def make_lysosome(center=LYSO_CENTER, radius=LYSO_R, jaw_speed=5.0, dashed_jaws=False, stroke_w=5.0):
    """Sealed BLUE-walled lysosome with PINK acidic interior and 6 animated TEAL jaws."""
    wall = Circle(radius=radius, stroke_color=BLUE, stroke_width=stroke_w,
                  fill_color=PINK, fill_opacity=0.26).move_to(center)
    jaws = VGroup()
    jaw_r = 0.21 * (radius / LYSO_R)
    ring_r = radius * 0.56
    radii = []
    for k in range(6):
        ang = k * TAU / 6 + PI / 6
        pos = center + np.array([ring_r * np.cos(ang), ring_r * np.sin(ang), 0.0])
        j = make_jaw(radius=jaw_r, color=TEAL, angle=0.50, dashed=dashed_jaws).move_to(pos)
        j._anchor = pos.copy()
        jaws.add(j)
        radii.append(jaw_r)
    if not dashed_jaws and jaw_speed > 0:
        animate_jaws(jaws, radii, speed=jaw_speed)
    grp = VGroup(wall, jaws)
    grp.wall = wall
    grp.jaws = jaws
    return grp


def make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0):
    """Build the whole carried cell in its canonical position."""
    cell_wall = RoundedRectangle(corner_radius=CELL_R, width=CELL_W, height=CELL_H,
                                 stroke_color=BLUE, stroke_width=6.0,
                                 fill_color=BLUE, fill_opacity=0.05).move_to(CELL_CENTER)
    er = make_rough_er(ER_CENTER)
    golgi = make_golgi(GOLGI_CENTER)
    lyso = make_lysosome(LYSO_CENTER, LYSO_R, jaw_speed=jaw_speed)

    world = VGroup(cell_wall, er, golgi, lyso)
    world.cell_wall = cell_wall
    world.er = er
    world.golgi = golgi
    world.lyso = lyso

    if include_barrel:
        barrel = make_barrel(BARREL_CENTER)
        add_barrel_drift(barrel, BARREL_CENTER)
        world.barrel = barrel
        world.add(barrel)

    if include_labels:
        er_lab = T("rough ER", 30, BLUE).move_to(ER_CENTER + UP * 1.65)
        golgi_lab = T("Golgi", 30, BLUE).move_to(GOLGI_CENTER + UP * 1.55)
        lyso_lab = T("lysosome", 30, BLUE).move_to(LYSO_CENTER + DOWN * (LYSO_R + 0.36))
        world.er_lab = er_lab
        world.golgi_lab = golgi_lab
        world.lyso_lab = lyso_lab
        world.add(er_lab, golgi_lab, lyso_lab)
        if include_barrel:
            bar_lab = T("protein destroyer", 30, RED).move_to(BARREL_CENTER + DOWN * 0.96)
            world.bar_lab = bar_lab
            world.add(bar_lab)
    return world


def make_zoomed_lyso(center=Z_LYSO_CENTER, radius=Z_LYSO_R, jaw_speed=5.5, stroke_w=6.0):
    """Build the zoomed-in lysosome with 6 jaws in a clear outer ring (center free for pH chip)."""
    wall = Circle(radius=radius, stroke_color=BLUE, stroke_width=stroke_w,
                  fill_color=PINK, fill_opacity=0.28).move_to(center)
    jaws = VGroup()
    jaw_r = 0.34
    ring_r = radius * 0.65
    radii = []
    for k in range(6):
        ang = k * TAU / 6 + PI / 6
        pos = center + np.array([ring_r * np.cos(ang), ring_r * np.sin(ang), 0.0])
        j = make_jaw(radius=jaw_r, color=TEAL, angle=0.52).move_to(pos)
        j._anchor = pos.copy()
        jaws.add(j)
        radii.append(jaw_r)
    if jaw_speed > 0:
        animate_jaws(jaws, radii, speed=jaw_speed)
    grp = VGroup(wall, jaws)
    grp.wall = wall
    grp.jaws = jaws
    return grp


def make_sugar_chain(anchor):
    """Short branched chain of small TEXT-outline beads (cartoon tag, no structure)."""
    p0 = anchor
    p1 = p0 + np.array([0.24, 0.16, 0.0])
    p2 = p1 + np.array([0.24, 0.12, 0.0])
    p3 = p1 + np.array([0.18, -0.14, 0.0])
    lines = VGroup(
        Line(p0, p1, color=TEXT, stroke_width=2.5),
        Line(p1, p2, color=TEXT, stroke_width=2.5),
        Line(p1, p3, color=TEXT, stroke_width=2.5),
    )
    beads = VGroup(*[
        Circle(radius=0.075, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(p)
        for p in (p1, p2, p3)
    ])
    return VGroup(lines, beads)


def make_disulfide_clip(anchor):
    """Small bright TEXT U-clip snapping across a folded protein."""
    pts = [anchor + np.array([-0.10, 0.09, 0]), anchor + np.array([-0.10, -0.06, 0]),
           anchor + np.array([0.10, -0.06, 0]), anchor + np.array([0.10, 0.09, 0])]
    clip = VMobject(stroke_color=TEXT, stroke_width=4.0)
    clip.set_points_as_corners(pts)
    return clip


def make_folding_cups(center):
    """Two TEXT-outline cupped shapes that close around a folding protein."""
    left_cup = Arc(radius=0.52, start_angle=PI * 0.65, angle=PI * 0.7,
                   arc_center=center, stroke_color=TEXT, stroke_width=4.0).shift(LEFT * 0.24)
    right_cup = Arc(radius=0.52, start_angle=-PI * 0.35, angle=PI * 0.7,
                    arc_center=center, stroke_color=TEXT, stroke_width=4.0).shift(RIGHT * 0.24)
    return VGroup(left_cup, right_cup)


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        swollen_r = 2.25
        swollen_wall = Circle(radius=swollen_r, stroke_color=BLUE, stroke_width=6.0,
                              fill_color=PINK, fill_opacity=0.25).move_to(ORIGIN)
        lozenges = VGroup()
        rng = np.random.default_rng(7)
        row_ys = [-1.25, -0.55, 0.15, 0.85]
        for ry in row_ys:
            n_col = 4 if abs(ry) < 0.7 else 3
            xs = np.linspace(-0.95, 0.95, n_col)
            for cx in xs:
                loz = RoundedRectangle(corner_radius=0.14, width=0.56, height=0.26,
                                       stroke_color=GOLD, stroke_width=2.5,
                                       fill_color=GOLD, fill_opacity=0.78)
                loz.rotate(rng.uniform(-0.18, 0.18))
                loz.move_to([cx + rng.uniform(-0.08, 0.08), ry + rng.uniform(-0.04, 0.04), 0.0])
                lozenges.add(loz)

        tag_first = T("first film", 28, TEXT).move_to([0.0, 2.85, 0.0])
        self.add(swollen_wall, lozenges, tag_first)

        self.play(
            swollen_wall.animate.scale(1.05),
            lozenges.animate.scale(1.05),
            run_time=4.8,
            rate_func=there_and_back,
        )

        self.at("trap trouble")
        flash_ring = swollen_wall.copy().set_stroke(TEXT, width=10)
        self.play(FadeIn(flash_ring, run_time=0.22), FadeOut(tag_first, run_time=0.25))
        self.play(FadeOut(flash_ring, run_time=0.28))

        self.at("keep it away")
        world = make_cell_world(include_labels=True, include_barrel=False, jaw_speed=5.0)
        self.play(
            FadeOut(lozenges, run_time=0.55),
            swollen_wall.animate(run_time=1.35).scale(LYSO_R / swollen_r).move_to(LYSO_CENTER).set_stroke(width=5.0),
            FadeIn(world.cell_wall, run_time=1.0),
            FadeIn(world.er, world.er_lab, run_time=1.0),
            FadeIn(world.golgi, world.golgi_lab, run_time=1.0),
        )
        self.remove(swollen_wall)
        self.add(world.lyso, world.lyso_lab)

        self.at("new proteins")
        blob = make_orange_blob(ER_CENTER, scale=0.95)
        self.play(GrowFromCenter(blob), run_time=0.6)

        self.at("machinery that destroys proteins")
        barrel = make_barrel(BARREL_CENTER)
        bar_lab = T("protein destroyer", 30, RED).move_to(BARREL_CENTER + DOWN * 0.96)
        self.play(FadeIn(barrel), FadeIn(bar_lab), run_time=0.7)
        add_barrel_drift(barrel, BARREL_CENTER)

        self.at("How does a new protein")
        pts = [
            ER_CENTER + RIGHT * 0.6,
            GOLGI_CENTER + LEFT * 0.6,
            GOLGI_CENTER + RIGHT * 0.7,
            np.array([CELL_CENTER[0] + CELL_W / 2 - 0.15, 0.25, 0.0]),
        ]
        route = VMobject(stroke_color=ORANGE, stroke_width=4.0)
        route.set_points_as_corners(pts)
        dashed_route = DashedVMobject(route, num_dashes=26, dashed_ratio=0.55).set_stroke(ORANGE, 4.0)
        q_card = T("Safe to the surface?", 36, TEXT).move_to([0.0, 3.18, 0.0])
        self.play(Create(dashed_route), FadeIn(q_card, shift=DOWN * 0.12), run_time=1.4)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        blob = make_orange_blob(ER_CENTER, scale=0.95)
        pts = [
            ER_CENTER + RIGHT * 0.6,
            GOLGI_CENTER + LEFT * 0.6,
            GOLGI_CENTER + RIGHT * 0.7,
            np.array([CELL_CENTER[0] + CELL_W / 2 - 0.15, 0.25, 0.0]),
        ]
        route = VMobject(stroke_color=ORANGE, stroke_width=4.0)
        route.set_points_as_corners(pts)
        dashed_route = DashedVMobject(route, num_dashes=26, dashed_ratio=0.55).set_stroke(ORANGE, 4.0)
        q_card = T("Safe to the surface?", 36, TEXT).move_to([0.0, 3.18, 0.0])
        title = T("Sealed Rooms, Safe Passage", 54, TEXT, font=TITLE_FONT).move_to([0.0, 3.18, 0.0])
        fit(title, max_w=11.5)

        self.add(world, blob, dashed_route, q_card)
        self.play(
            swap(q_card, title, run_time=0.9),
            FadeOut(dashed_route, run_time=0.9),
        )
        self.finish()


class S02Belt(SpokenScene):
    def construct(self):
        world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        blob = make_orange_blob(ER_CENTER, scale=0.95)
        title = T("Sealed Rooms, Safe Passage", 54, TEXT, font=TITLE_FONT).move_to([0.0, 3.18, 0.0])
        fit(title, max_w=11.5)
        self.add(world, blob, title)

        self.play(FadeOut(title, run_time=0.6))

        self.at("made at the rough")
        self.play(blob.animate.scale(1.18), run_time=0.45, rate_func=there_and_back)

        self.at("conveyor belt")
        cargo = make_orange_blob(ER_CENTER + RIGHT * 1.15, scale=0.82)
        bubble1 = make_bubble(cargo, center=ER_CENTER + RIGHT * 1.15, radius=0.38)
        self.play(FadeOut(blob, run_time=0.2), FadeIn(bubble1, run_time=0.35))

        plate_xs = [p.get_center()[0] for p in world.golgi]
        plate_y = GOLGI_CENTER[1] + 0.15
        self.play(bubble1.animate.move_to([plate_xs[0] - 0.35, plate_y, 0.0]), run_time=1.35)
        cargo_in_golgi = make_orange_blob([plate_xs[0], plate_y, 0.0], scale=0.82)
        self.play(bubble1.animate.move_to([plate_xs[0], plate_y, 0.0]), run_time=0.25)
        self.remove(bubble1)
        shell_fade = bubble1.shell.copy()
        self.add(shell_fade, cargo_in_golgi)
        self.play(FadeOut(shell_fade, scale=1.35, run_time=0.25))

        c_er = chip("ER", TEXT, size=30).move_to([ER_CENTER[0], 3.18, 0.0])
        c_golgi = chip("Golgi", TEXT, size=30).move_to([GOLGI_CENTER[0], 3.18, 0.0])
        c_surf = chip("surface", TEXT, size=30).move_to([3.2, 3.18, 0.0])

        self.at("ER", nth=1)
        self.play(FadeIn(c_er), run_time=0.35)

        self.at("Golgi")
        self.play(FadeIn(c_golgi), run_time=0.3)
        for px in plate_xs[1:]:
            self.play(cargo_in_golgi.animate.move_to([px, plate_y, 0.0]), run_time=0.36)

        self.at("surface")
        self.play(FadeIn(c_surf), run_time=0.3)
        surf_stop = np.array([CELL_CENTER[0] + CELL_W / 2 - 0.68, 0.45, 0.0])
        bubble2 = make_bubble(cargo_in_golgi.copy(), center=[plate_xs[-1] + 0.35, plate_y, 0.0], radius=0.40)
        self.remove(cargo_in_golgi)
        self.play(FadeIn(bubble2, run_time=0.3))
        self.play(bubble2.animate.move_to(surf_stop), run_time=1.35)

        self.at("never passes through")
        cytosol_label = T("cytosol:\nopen workspace", 25, TEXT).move_to([1.75, 1.45, 0.0])
        bright_shell = bubble2.shell.copy().set_stroke(BLUE, width=8.0)
        self.play(
            world.cell_wall.animate.set_fill(BLUE, opacity=0.09),
            FadeIn(cytosol_label),
            Transform(bubble2.shell, bright_shell),
            run_time=0.9,
        )
        self.finish()


class S03Checked(SpokenScene):
    def construct(self):
        world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        surf_stop = np.array([CELL_CENTER[0] + CELL_W / 2 - 0.68, 0.45, 0.0])
        waiting_bubble = make_bubble(make_orange_blob(surf_stop, scale=0.82), center=surf_stop, radius=0.40)
        waiting_bubble.shell.set_stroke(BLUE, width=8.0)
        self.add(world, waiting_bubble)

        z_er_center = np.array([-2.8, 0.05, 0.0])
        z_scale = 2.05
        z_er = make_rough_er(z_er_center, scale=z_scale)
        z_er_lab = T("rough ER", 30, BLUE).move_to(z_er_center + UP * 2.95)
        z_wall = RoundedRectangle(corner_radius=2.0, width=15.0, height=7.4,
                                  stroke_color=BLUE, stroke_width=6.0,
                                  fill_color=BLUE, fill_opacity=0.05).move_to([-1.25, 0.0, 0.0])
        z_wait_pos = np.array([5.50, 0.45, 0.0])

        loose_blob = make_orange_blob(z_er_center + LEFT * 0.2, scale=1.30, loose=True)

        for j in world.lyso.jaws:
            j.clear_updaters()
        world.barrel.clear_updaters()

        self.play(
            FadeOut(world.golgi, world.golgi_lab, world.lyso, world.lyso_lab,
                    world.barrel, world.bar_lab, run_time=0.85),
            Transform(world.cell_wall, z_wall, run_time=1.25),
            Transform(world.er, z_er, run_time=1.25),
            world.er_lab.animate(run_time=1.25).move_to(z_er_lab.get_center()),
            waiting_bubble.animate(run_time=1.25).move_to(z_wait_pos),
            Create(loose_blob, run_time=1.1),
        )
        self.play(loose_blob.animate.scale(1.06), run_time=2.5, rate_func=there_and_back)

        self.at("folding enzymes")
        blob_pos = z_er_center + LEFT * 0.2
        cups = make_folding_cups(blob_pos)
        enz_lab = T("folding enzymes", 30, TEXT).move_to([2.0, 1.35, 0.0])
        enz_ptr = Line(blob_pos + RIGHT * 0.72, enz_lab.get_left() + LEFT * 0.14, color=TEXT, stroke_width=2.5)
        folded_blob = make_orange_blob(blob_pos, scale=1.40)
        self.play(FadeIn(cups, enz_lab, enz_ptr), run_time=0.5)
        self.play(
            cups[0].animate.shift(RIGHT * 0.18),
            cups[1].animate.shift(LEFT * 0.18),
            Transform(loose_blob, folded_blob),
            run_time=1.25,
        )

        self.at("disulfide bonds")
        clip = make_disulfide_clip(blob_pos + UP * 0.05)
        clip_lab = T("disulfide bond", 28, TEXT).move_to([2.0, 0.45, 0.0])
        clip_ptr = Line(blob_pos + RIGHT * 0.45 + UP * 0.05, clip_lab.get_left() + LEFT * 0.14, color=TEXT, stroke_width=2.5)
        self.play(FadeOut(cups, enz_lab, enz_ptr, run_time=0.45), Create(clip, run_time=0.5), FadeIn(clip_lab, clip_ptr, run_time=0.45))
        self.play(loose_blob.animate.scale(1.04), run_time=1.2, rate_func=there_and_back)

        self.at("sugar chains")
        sugars = make_sugar_chain(blob_pos + np.array([0.34, 0.16, 0.0]))
        sugar_lab = T("sugar chain", 28, TEXT).move_to([2.0, -0.40, 0.0])
        sugar_ptr = Line(blob_pos + np.array([0.82, 0.16, 0.0]), sugar_lab.get_left() + LEFT * 0.14, color=TEXT, stroke_width=2.5)
        self.play(FadeOut(clip_lab, clip_ptr, run_time=0.35), Create(sugars, run_time=0.7), FadeIn(sugar_lab, sugar_ptr, run_time=0.45))

        tangled = make_orange_blob(z_er_center + np.array([-1.4, -1.74, 0.0]), scale=1.05, tangled=True)
        self.play(GrowFromCenter(tangled), run_time=1.1)
        self.play(tangled.animate.move_to(z_er_center + np.array([-0.3, -1.74, 0.0])), run_time=1.2)

        self.at("Misfolded proteins")
        bar = Line(z_er_center + np.array([2.55, -1.32, 0.0]),
                   z_er_center + np.array([2.55, -2.14, 0.0]),
                   color=TEXT, stroke_width=6.0)
        held_lab = T("held back", 28, TEXT).move_to([1.35, -1.74, 0.0])
        self.play(FadeOut(sugar_lab, sugar_ptr, run_time=0.35), FadeIn(bar, held_lab, run_time=0.45))
        self.play(tangled.animate.move_to(z_er_center + np.array([2.05, -1.74, 0.0])), run_time=0.85)
        self.play(tangled.animate.move_to(z_er_center + np.array([0.75, -1.74, 0.0])), run_time=0.75)
        self.play(tangled.animate.move_to(z_er_center + np.array([1.75, -1.74, 0.0])), run_time=0.7)
        self.play(tangled.animate.move_to(z_er_center + np.array([0.85, -1.74, 0.0])), run_time=0.65)

        self.at("pushed out to the cytosol")
        full_world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        full_world.barrel.clear_updaters()
        self.play(
            FadeOut(loose_blob, clip, sugars, bar, held_lab, run_time=0.5),
            tangled.animate(run_time=1.05).scale(0.65).move_to(ER_CENTER + DOWN * 1.65),
            Transform(world.cell_wall, full_world.cell_wall, run_time=1.05),
            Transform(world.er, full_world.er, run_time=1.05),
            world.er_lab.animate(run_time=1.05).move_to(full_world.er_lab.get_center()),
            waiting_bubble.animate(run_time=1.05).move_to(surf_stop),
            FadeIn(full_world.golgi, full_world.golgi_lab,
                   full_world.lyso, full_world.lyso_lab,
                   full_world.barrel, full_world.bar_lab, run_time=0.95),
        )
        self.play(
            full_world.barrel.animate.move_to(ER_CENTER + DOWN * 1.65),
            tangled.animate.scale(0.45).move_to(ER_CENTER + DOWN * 1.65),
            run_time=0.75,
        )
        self.remove(tangled)
        rng = np.random.default_rng(7)
        shred_center = full_world.barrel.get_center()
        dots = VGroup(*[
            Dot(shred_center + np.array([rng.uniform(-0.1, 0.1), rng.uniform(-0.1, 0.1), 0.0]),
                radius=0.06, color=PURPLE)
            for _ in range(14)
        ])
        self.add(dots)
        scatter_anims = [
            d.animate.shift(np.array([rng.uniform(-0.85, 0.85), rng.uniform(-0.65, 0.65), 0.0])).set_opacity(0.0)
            for d in dots
        ]
        self.play(
            *scatter_anims,
            full_world.barrel.animate.move_to(BARREL_CENTER),
            run_time=1.25,
        )
        add_barrel_drift(full_world.barrel, BARREL_CENTER)
        self.finish()


class S04NeverMeets(SpokenScene):
    def construct(self):
        world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        surf_stop = np.array([CELL_CENTER[0] + CELL_W / 2 - 0.68, 0.45, 0.0])
        bubble = make_bubble(make_orange_blob(surf_stop, scale=0.82), center=surf_stop, radius=0.40)
        bubble.shell.set_stroke(BLUE, width=8.0)
        self.add(world, bubble)

        self.at("waits out in the cytosol")
        world.barrel.clear_updaters()
        self.play(world.barrel.animate.scale(1.15), run_time=0.45, rate_func=there_and_back)
        bump_pt = surf_stop + np.array([-0.75, 0.0, 0.0])
        self.play(world.barrel.animate.move_to([-1.5, -1.7, 0.0]), run_time=0.8)
        self.play(world.barrel.animate.move_to([0.5, -1.1, 0.0]), run_time=0.8)
        self.play(world.barrel.animate.move_to([1.1, 0.45, 0.0]), run_time=0.75)
        self.play(world.barrel.animate.move_to(bump_pt), run_time=0.6)

        self.at("never meets it")
        tick = VMobject(stroke_color=GREEN, stroke_width=6.0)
        t_c = surf_stop + np.array([-0.75, 0.58, 0.0])
        tick.set_points_as_corners([t_c + LEFT * 0.16 + UP * 0.02, t_c + DOWN * 0.14, t_c + RIGHT * 0.24 + UP * 0.26])
        self.play(
            Create(tick, run_time=0.55),
            world.barrel.animate(run_time=0.65).move_to([1.1, 0.45, 0.0]),
        )
        self.play(world.barrel.animate.move_to([0.5, -1.1, 0.0]), run_time=0.75)
        self.play(world.barrel.animate.move_to([-1.5, -1.7, 0.0]), run_time=0.8)
        self.play(world.barrel.animate.move_to(BARREL_CENTER), run_time=0.75)
        add_barrel_drift(world.barrel, BARREL_CENTER)

        self.at("fuses with the outer membrane")
        wall_x = CELL_CENTER[0] + CELL_W / 2
        self.play(
            FadeOut(tick, run_time=0.35),
            bubble.animate.move_to([wall_x - 0.44, 0.45, 0.0]),
            run_time=1.1,
        )
        b1 = bubble.cargo.copy()
        b2 = make_orange_blob(b1.get_center(), scale=0.78)
        b3 = make_orange_blob(b1.get_center(), scale=0.78)
        shell_fade = bubble.shell.copy()
        self.remove(bubble)
        self.add(shell_fade, b1, b2, b3)
        self.play(
            FadeOut(shell_fade, scale=1.35, run_time=0.5),
            b1.animate(run_time=2.6).move_to([wall_x + 0.72, 0.85, 0.0]),
            b2.animate(run_time=2.6).move_to([wall_x + 1.42, 0.40, 0.0]),
            b3.animate(run_time=2.6).move_to([wall_x + 0.76, -0.08, 0.0]),
        )

        self.at("releases insulin")
        ins_chip = chip("insulin,\nfrom beta cells", ORANGE, size=26, pad=0.16)
        ins_chip.move_to([wall_x + 1.55, -1.25, 0.0])
        self.play(FadeIn(ins_chip, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        wall_x = CELL_CENTER[0] + CELL_W / 2
        b1 = make_orange_blob([wall_x + 0.72, 0.85, 0.0], scale=0.78)
        b2 = make_orange_blob([wall_x + 1.42, 0.40, 0.0], scale=0.78)
        b3 = make_orange_blob([wall_x + 0.76, -0.08, 0.0], scale=0.78)
        ins_chip = chip("insulin,\nfrom beta cells", ORANGE, size=26, pad=0.16).move_to([wall_x + 1.55, -1.25, 0.0])
        self.add(world, b1, b2, b3, ins_chip)
        self.play(FadeOut(b1, b2, b3, ins_chip, run_time=0.6))

        self.at("each room")
        top_lab = T("own enzymes, own conditions", 32, TEXT).move_to([0.0, 3.18, 0.0])
        self.play(FadeIn(top_lab), run_time=0.55)

        self.play(
            world.er.ribbons.animate.set_fill(ORANGE, opacity=0.20).set_stroke(width=6.5),
            run_time=0.85,
        )
        self.play(
            world.golgi.animate.set_fill(PURPLE, opacity=0.20).set_stroke(width=6.5),
            run_time=0.85,
        )
        self.play(
            world.lyso.wall.animate.set_fill(PINK, opacity=0.32).set_stroke(width=7.5),
            run_time=0.85,
        )

        self.at("what reaches each room")
        deliv_dot = Dot(GOLGI_CENTER + RIGHT * 1.15, radius=0.12, color=GREEN)
        deliv = make_bubble(deliv_dot, center=GOLGI_CENTER + RIGHT * 1.15, radius=0.34, outline=BLUE, halo=GREEN)
        self.play(FadeIn(deliv), run_time=0.35)
        self.play(deliv.animate.move_to(LYSO_CENTER + np.array([-0.80, 0.60, 0.0])), run_time=0.85)
        self.play(FadeOut(deliv, scale=0.6), run_time=0.35)

        self.at("what it holds")
        self.play(world.lyso.jaws.animate.scale(1.18), run_time=0.45, rate_func=there_and_back)

        self.at("how it is kept")
        acid_chip = chip("acidic", TEXT, size=30).next_to(world.lyso.wall, UP, buff=0.18)
        self.play(
            world.lyso.wall.animate.set_fill(PINK, opacity=0.45),
            FadeIn(acid_chip, shift=DOWN * 0.08),
            run_time=0.55,
            rate_func=there_and_back,
        )
        self.play(FadeIn(acid_chip), run_time=0.3)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        world.er.ribbons.set_fill(ORANGE, opacity=0.20).set_stroke(width=6.5)
        world.golgi.set_fill(PURPLE, opacity=0.20).set_stroke(width=6.5)
        world.lyso.wall.set_fill(PINK, opacity=0.32).set_stroke(width=7.5)
        top_lab = T("own enzymes, own conditions", 32, TEXT).move_to([0.0, 3.18, 0.0])
        acid_chip = chip("acidic", TEXT, size=30).next_to(world.lyso.wall, UP, buff=0.18)
        self.add(world, top_lab, acid_chip)

        self.play(
            FadeOut(top_lab, acid_chip, run_time=0.5),
            world.er.ribbons.animate.set_fill(BLUE, opacity=0.15).set_stroke(width=4.0),
            world.golgi.animate.set_fill(BLUE, opacity=0.15).set_stroke(width=4.0),
            world.lyso.wall.animate.set_fill(PINK, opacity=0.26).set_stroke(width=5.5),
            run_time=0.7,
        )

        self.at("made at the rough")
        traj_jaw = make_jaw(radius=0.18, color=TEAL, angle=0.55).move_to(ER_CENTER)
        ves = make_bubble(traj_jaw, center=ER_CENTER + RIGHT * 1.15, radius=0.36)
        self.play(FadeIn(ves), run_time=0.35)
        self.play(ves.animate.move_to(GOLGI_CENTER), run_time=0.8)

        self.at("addressed to the lysosome")
        self.play(ves.animate.move_to(LYSO_CENTER + LEFT * 0.4), run_time=0.85)
        self.play(FadeOut(ves, scale=0.65), run_time=0.35)

        for j in world.lyso.jaws:
            j.clear_updaters()
        world.barrel.clear_updaters()

        z_lyso = make_zoomed_lyso(Z_LYSO_CENTER, Z_LYSO_R, jaw_speed=0)
        self.play(
            FadeOut(world.cell_wall, world.er, world.er_lab, world.golgi, world.golgi_lab,
                    world.barrel, world.bar_lab, world.lyso_lab, run_time=0.75),
            Transform(world.lyso.wall, z_lyso.wall, run_time=1.0),
            Transform(world.lyso.jaws, z_lyso.jaws, run_time=1.0),
        )
        self.remove(world)
        self.add(z_lyso)
        animate_jaws(z_lyso.jaws, [0.34] * 6, speed=5.5)

        self.at("Suppose one escapes")
        escaped_jaw = make_jaw(radius=0.34, color=TEAL, angle=0.50, dashed=True).move_to([-4.1, 0.55, 0.0])
        what_if = T("what if?", 28, TEXT).move_to([-4.1, 1.55, 0.0])
        blobs = VGroup(
            Ellipse(width=0.56, height=0.38, stroke_color=TEXT, stroke_width=2.8).move_to([-2.1, 1.15, 0.0]),
            Ellipse(width=0.52, height=0.42, stroke_color=TEXT, stroke_width=2.8).move_to([-1.8, 0.45, 0.0]),
            Ellipse(width=0.58, height=0.36, stroke_color=TEXT, stroke_width=2.8).move_to([-2.2, -0.25, 0.0]),
        )
        blobs_lab = T("cell's own proteins", 28, TEXT).move_to([-2.1, -1.05, 0.0])
        self.play(FadeIn(escaped_jaw, what_if, blobs, blobs_lab), run_time=0.7)

        self.at("Does it work")
        q = question_card("Does it work out here?", y=-3.0, size=36, color=TEXT)
        self.play(FadeIn(q, shift=UP * 0.25), run_time=0.6)
        self.finish()


class S07Think(PredictPause):
    QUESTION = "Does it work out here?"
    CARD = {"y": -3.0, "size": 36, "color": TEXT}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        z_lyso = make_zoomed_lyso(Z_LYSO_CENTER, Z_LYSO_R, jaw_speed=5.5)
        escaped_jaw = make_jaw(radius=0.34, color=TEAL, angle=0.50, dashed=True).move_to([-4.1, 0.55, 0.0])
        what_if = T("what if?", 28, TEXT).move_to([-4.1, 1.55, 0.0])
        blobs = VGroup(
            Ellipse(width=0.56, height=0.38, stroke_color=TEXT, stroke_width=2.8).move_to([-2.1, 1.15, 0.0]),
            Ellipse(width=0.52, height=0.42, stroke_color=TEXT, stroke_width=2.8).move_to([-1.8, 0.45, 0.0]),
            Ellipse(width=0.58, height=0.36, stroke_color=TEXT, stroke_width=2.8).move_to([-2.2, -0.25, 0.0]),
        )
        blobs_lab = T("cell's own proteins", 28, TEXT).move_to([-2.1, -1.05, 0.0])
        return VGroup(z_lyso, escaped_jaw, what_if, blobs, blobs_lab)


class S08Answer(SpokenScene):
    def construct(self):
        z_lyso = make_zoomed_lyso(Z_LYSO_CENTER, Z_LYSO_R, jaw_speed=5.5)
        escaped_start = make_jaw(radius=0.34, color=TEAL, angle=0.50, dashed=True).move_to([-4.1, 0.55, 0.0])
        what_if = T("what if?", 28, TEXT).move_to([-4.1, 1.55, 0.0])
        blobs = VGroup(
            Ellipse(width=0.56, height=0.38, stroke_color=TEXT, stroke_width=2.8).move_to([-2.1, 1.15, 0.0]),
            Ellipse(width=0.52, height=0.42, stroke_color=TEXT, stroke_width=2.8).move_to([-1.8, 0.45, 0.0]),
            Ellipse(width=0.58, height=0.36, stroke_color=TEXT, stroke_width=2.8).move_to([-2.2, -0.25, 0.0]),
        )
        blobs_lab = T("cell's own proteins", 28, TEXT).move_to([-2.1, -1.05, 0.0])
        q = question_card("Does it work out here?", y=-3.0, size=36, color=TEXT)
        self.add(z_lyso, escaped_start, what_if, blobs, blobs_lab, q)

        self.at("Much less well")
        bar_w, bar_h = 0.44, 1.9
        esc_bar_bg = Rectangle(width=bar_w, height=bar_h, stroke_color=TEXT, stroke_width=2.5).move_to([-1.45, 0.55, 0.0])
        esc_bar_fill = Rectangle(width=bar_w - 0.06, height=0.14, stroke_width=0,
                                 fill_color=TEAL, fill_opacity=0.85).align_to(esc_bar_bg, DOWN).shift(UP * 0.03)
        esc_bar_fill.set_x(esc_bar_bg.get_center()[0])

        lyso_bar_bg = Rectangle(width=bar_w, height=bar_h, stroke_color=TEXT, stroke_width=2.5).move_to([-0.25, 0.55, 0.0])
        lyso_bar_fill = Rectangle(width=bar_w - 0.06, height=bar_h - 0.06, stroke_width=0,
                                  fill_color=TEAL, fill_opacity=0.85).move_to(lyso_bar_bg)

        act_lab = T("activity,\nschematic", 28, TEXT).move_to([-0.72, 2.18, 0.0])
        self.play(
            FadeOut(q, shift=DOWN * 0.4, run_time=0.55),
            FadeOut(what_if, run_time=0.4),
            escaped_start.animate(run_time=0.6).move_to([-5.0, 0.55, 0.0]),
            blobs.animate(run_time=0.6).shift(LEFT * 1.4),
            blobs_lab.animate(run_time=0.6).shift(LEFT * 1.4),
            FadeIn(esc_bar_bg, lyso_bar_bg, act_lab, run_time=0.5),
            GrowFromEdge(esc_bar_fill, DOWN, run_time=1.0),
            GrowFromEdge(lyso_bar_fill, DOWN, run_time=1.0),
        )

        self.at("work best in acid")
        for j in z_lyso.jaws:
            j.clear_updaters()
        animate_jaws(z_lyso.jaws, [0.34] * 6, speed=12.0, swim_amp=0.08)
        self.play(
            lyso_bar_bg.animate.set_stroke(TEAL, width=4.5),
            z_lyso.wall.animate.set_fill(PINK, opacity=0.38),
            run_time=1.3,
            rate_func=there_and_back,
        )

        self.at("poorly at the")
        self.play(escaped_start.animate.move_to(blobs[0].get_center() + LEFT * 0.52), run_time=1.0)
        for target_blob in blobs:
            self.play(escaped_start.animate.move_to(target_blob.get_center() + LEFT * 0.52), run_time=0.8)
            jaw_c = escaped_start.get_center()
            self.play(
                Rotate(escaped_start[0], angle=0.22, about_point=jaw_c),
                Rotate(escaped_start[1], angle=-0.22, about_point=jaw_c),
                run_time=1.1,
                rate_func=there_and_back,
            )

        self.at("a large leak")
        cytosol_tint = Rectangle(width=4.55, height=4.4, stroke_width=0,
                                 fill_color=RED, fill_opacity=0.14).move_to([-4.025, 0.60, 0.0])
        leak_coords = [
            [-5.7, 2.3], [-4.5, 2.3], [-3.2, 2.3],
            [-5.7, 1.3], [-4.5, 1.4], [-2.5, 1.4],
            [-5.7, 0.1], [-5.5, -1.0],
        ]
        extra_jaws = VGroup(*[
            make_jaw(radius=0.25, color=TEAL, angle=0.45, dashed=True).move_to([x, y, 0.0])
            for x, y in leak_coords
        ])
        kill_chip = chip("large leak can kill", RED, size=30).move_to([-3.6, -2.55, 0.0])
        self.add(cytosol_tint)
        cytosol_tint.set_z_index(-1)
        self.play(FadeIn(cytosol_tint, extra_jaws, kill_chip), run_time=0.55)
        self.wait(0.75)
        self.play(FadeOut(cytosol_tint, extra_jaws, kill_chip, run_time=0.65))
        self.finish()


class S09Acid(SpokenScene):
    def construct(self):
        z_lyso = make_zoomed_lyso(Z_LYSO_CENTER, Z_LYSO_R, jaw_speed=5.5)
        blobs = VGroup(
            Ellipse(width=0.56, height=0.38, stroke_color=TEXT, stroke_width=2.8).move_to([-3.5, 1.15, 0.0]),
            Ellipse(width=0.52, height=0.42, stroke_color=TEXT, stroke_width=2.8).move_to([-3.2, 0.45, 0.0]),
            Ellipse(width=0.58, height=0.36, stroke_color=TEXT, stroke_width=2.8).move_to([-3.6, -0.25, 0.0]),
        )
        escaped_jaw = make_jaw(radius=0.34, color=TEAL, angle=0.50, dashed=True).move_to(blobs[2].get_center() + LEFT * 0.52)
        blobs_lab = T("cell's own proteins", 28, TEXT).move_to([-3.5, -1.05, 0.0])
        bar_w, bar_h = 0.44, 1.9
        esc_bar_bg = Rectangle(width=bar_w, height=bar_h, stroke_color=TEXT, stroke_width=2.5).move_to([-1.45, 0.55, 0.0])
        esc_bar_fill = Rectangle(width=bar_w - 0.06, height=0.14, stroke_width=0,
                                 fill_color=TEAL, fill_opacity=0.85).align_to(esc_bar_bg, DOWN).shift(UP * 0.03)
        esc_bar_fill.set_x(esc_bar_bg.get_center()[0])
        lyso_bar_bg = Rectangle(width=bar_w, height=bar_h, stroke_color=TEXT, stroke_width=2.5).move_to([-0.25, 0.55, 0.0])
        lyso_bar_fill = Rectangle(width=bar_w - 0.06, height=bar_h - 0.06, stroke_width=0,
                                  fill_color=TEAL, fill_opacity=0.85).move_to(lyso_bar_bg)
        act_lab = T("activity,\nschematic", 28, TEXT).move_to([-0.72, 2.18, 0.0])

        self.add(z_lyso, escaped_jaw, blobs, blobs_lab,
                 esc_bar_bg, esc_bar_fill, lyso_bar_bg, lyso_bar_fill, act_lab)

        lock_acid = chip("lock: acid", PINK, size=30).move_to([Z_LYSO_CENTER[0], 3.38, 0.0])
        self.play(
            FadeOut(escaped_jaw, blobs, blobs_lab, esc_bar_bg, esc_bar_fill,
                    lyso_bar_bg, lyso_bar_fill, act_lab, run_time=1.4),
            FadeIn(lock_acid, run_time=1.4),
        )

        self.at("Inside a lysosome")
        ph_lyso = boxed_label("pH 4.5 to 5", PINK, size=28, pad=0.26, fill_opacity=0.0).move_to(Z_LYSO_CENTER)
        ph_lyso.box.set_fill(BG, opacity=0.88)
        self.play(
            FadeIn(ph_lyso, run_time=1.5),
            z_lyso.wall.animate(run_time=1.5, rate_func=there_and_back).set_fill(PINK, opacity=0.40),
        )

        self.at("cytosol sits near")
        ph_cyt = chip("pH 7.2", TEXT, size=30).move_to([-4.6, 0.55, 0.0])
        self.play(FadeIn(ph_cyt), run_time=1.4)

        self.at("Each pH unit")
        lad_y = 0.55
        x0, x1, x2, x3 = -3.4, -2.2, -1.0, -0.4
        seg1 = Line([x0, lad_y, 0], [x1, lad_y, 0], color=TEXT, stroke_width=4.0)
        seg2 = Line([x1, lad_y, 0], [x2, lad_y, 0], color=TEXT, stroke_width=4.0)
        seg3 = Line([x2, lad_y, 0], [x3, lad_y, 0], color=TEXT, stroke_width=4.0)
        ticks = [Line([x, lad_y - 0.16, 0], [x, lad_y + 0.16, 0], color=TEXT, stroke_width=3.5)
                 for x in (x0, x1, x2, x3)]
        r1 = T("×10", 28, TEXT).move_to([(x0 + x1) / 2, lad_y + 0.42, 0.0])
        r2 = T("×10", 28, TEXT).move_to([(x1 + x2) / 2, lad_y - 0.42, 0.0])
        r3 = T("about ×3", 28, TEXT).move_to([(x2 + x3) / 2 + 0.15, lad_y + 0.42, 0.0])
        self.play(Create(ticks[0]), Create(seg1), Create(ticks[1]), FadeIn(r1), run_time=1.0)
        self.play(Create(seg2), Create(ticks[2]), FadeIn(r2), run_time=1.0)
        self.play(Create(seg3), Create(ticks[3]), FadeIn(r3), run_time=1.0)

        self.at("a few hundred times")
        n_lyso = round(10 ** (7.2 - 4.7))
        sq_side = 1.45
        sq_y = -2.60
        sq_left = Square(side_length=sq_side, stroke_color=TEXT, stroke_width=3.0).move_to([-2.4, sq_y, 0.0])
        sq_right = Square(side_length=sq_side, stroke_color=PINK, stroke_width=3.0).move_to([0.4, sq_y, 0.0])

        cyt_label = T("cytosol", 28, TEXT).next_to(sq_left, LEFT, buff=0.25)
        lyso_count_lab = T(f"about {n_lyso // 100 * 100} times", 30, PINK).next_to(sq_right, RIGHT, buff=0.28)

        rng = np.random.default_rng(7)
        half = sq_side / 2 - 0.09
        cyt_base = sq_left.get_center()
        dot_cyt = Dot(cyt_base, radius=0.045, color=PINK)
        dot_cyt._t = 0.0
        dot_cyt.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt * 3.0),
                                           m.move_to(cyt_base + np.array([0.04 * np.sin(m._t), 0.04 * np.cos(1.3 * m._t), 0]))))

        lyso_base = sq_right.get_center()
        offsets = rng.uniform(-half, half, size=(n_lyso, 2))
        phases = rng.uniform(0, TAU, size=(n_lyso, 2))
        lyso_dots = VGroup(*[
            Dot(lyso_base + np.array([ox, oy, 0.0]), radius=0.025, color=PINK)
            for ox, oy in offsets
        ])

        self.play(Create(sq_left), Create(sq_right), FadeIn(cyt_label, dot_cyt), run_time=0.8)
        self.play(
            FadeIn(lyso_dots, lag_ratio=0.015, run_time=2.2),
            FadeIn(lyso_count_lab, run_time=1.0),
        )
        lyso_dots._t = 0.0

        def _jiggle(grp, dt):
            grp._t += dt * 3.2
            dx = 0.025 * np.sin(grp._t + phases[:, 0])
            dy = 0.025 * np.cos(1.25 * grp._t + phases[:, 1])
            for k, m in enumerate(grp):
                m.move_to(lyso_base + np.array([offsets[k, 0] + dx[k], offsets[k, 1] + dy[k], 0.0]))

        lyso_dots.add_updater(_jiggle)
        self.finish()


class S10Membrane(SpokenScene):
    def construct(self):
        z_lyso = make_zoomed_lyso(Z_LYSO_CENTER, Z_LYSO_R, jaw_speed=5.5)
        lock_acid = chip("lock: acid", PINK, size=30).move_to([Z_LYSO_CENTER[0], 3.38, 0.0])
        ph_lyso = boxed_label("pH 4.5 to 5", PINK, size=28, pad=0.26, fill_opacity=0.0).move_to(Z_LYSO_CENTER)
        ph_lyso.box.set_fill(BG, opacity=0.88)
        ph_cyt = chip("pH 7.2", TEXT, size=30).move_to([-4.6, 0.55, 0.0])
        lad_y = 0.55
        x0, x1, x2, x3 = -3.4, -2.2, -1.0, -0.4
        ladder = VGroup(
            Line([x0, lad_y, 0], [x1, lad_y, 0], color=TEXT, stroke_width=4.0),
            Line([x1, lad_y, 0], [x2, lad_y, 0], color=TEXT, stroke_width=4.0),
            Line([x2, lad_y, 0], [x3, lad_y, 0], color=TEXT, stroke_width=4.0),
            *[Line([x, lad_y - 0.16, 0], [x, lad_y + 0.16, 0], color=TEXT, stroke_width=3.5)
              for x in (x0, x1, x2, x3)],
        )
        r1 = T("×10", 28, TEXT).move_to([(x0 + x1) / 2, lad_y + 0.42, 0.0])
        r2 = T("×10", 28, TEXT).move_to([(x1 + x2) / 2, lad_y - 0.42, 0.0])
        r3 = T("about ×3", 28, TEXT).move_to([(x2 + x3) / 2 + 0.15, lad_y + 0.42, 0.0])

        sq_side, sq_y = 1.45, -2.60
        sq_left = Square(side_length=sq_side, stroke_color=TEXT, stroke_width=3.0).move_to([-2.4, sq_y, 0.0])
        sq_right = Square(side_length=sq_side, stroke_color=PINK, stroke_width=3.0).move_to([0.4, sq_y, 0.0])
        cyt_label = T("cytosol", 28, TEXT).next_to(sq_left, LEFT, buff=0.25)
        lyso_count_lab = T("about 300 times", 30, PINK).next_to(sq_right, RIGHT, buff=0.28)
        dot_cyt = Dot(sq_left.get_center(), radius=0.045, color=PINK)
        rng = np.random.default_rng(7)
        half = sq_side / 2 - 0.09
        n_lyso = round(10 ** (7.2 - 4.7))
        offsets = rng.uniform(-half, half, size=(n_lyso, 2))
        lyso_dots = VGroup(*[
            Dot(sq_right.get_center() + np.array([ox, oy, 0.0]), radius=0.025, color=PINK)
            for ox, oy in offsets
        ])

        self.add(z_lyso, lock_acid, ph_lyso, ph_cyt, ladder, r1, r2, r3,
                 sq_left, sq_right, cyt_label, lyso_count_lab, dot_cyt, lyso_dots)

        self.play(FadeOut(ph_lyso, ph_cyt, ladder, r1, r2, r3,
                          sq_left, sq_right, cyt_label, lyso_count_lab, dot_cyt, lyso_dots, run_time=0.6))

        self.at("the membrane")
        lock_mem = chip("lock: membrane", BLUE, size=30)
        pair = VGroup(lock_acid.copy(), lock_mem).arrange(RIGHT, buff=0.30).move_to([Z_LYSO_CENTER[0], 3.38, 0.0])
        self.play(
            lock_acid.animate.move_to(pair[0].get_center()),
            FadeIn(lock_mem.move_to(pair[1].get_center())),
            z_lyso.wall.animate.set_stroke(width=11.0),
            run_time=0.7,
        )

        self.at("cannot get out")
        j_left = z_lyso.jaws[2]
        j_up_left = z_lyso.jaws[1]
        j_left.clear_updaters()
        j_up_left.clear_updaters()
        p_left0 = j_left._anchor.copy()
        p_ul0 = j_up_left._anchor.copy()
        self.play(
            j_left.animate.move_to(Z_LYSO_CENTER + np.array([-Z_LYSO_R + 0.44, 0.65, 0.0])),
            j_up_left.animate.move_to(Z_LYSO_CENTER + np.array([-0.15, Z_LYSO_R - 0.44, 0.0])),
            run_time=0.65,
        )
        self.play(
            j_left.animate.move_to(p_left0),
            j_up_left.animate.move_to(p_ul0),
            run_time=0.65,
        )
        j_left._anchor = p_left0.copy()
        j_up_left._anchor = p_ul0.copy()
        animate_jaws([j_left, j_up_left], [0.34, 0.34], speed=5.5)

        self.at("routes the cell builds")
        cargo_chips = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.26, height=0.14,
                             stroke_color=TEXT, stroke_width=2.2, fill_opacity=0)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.06)
        route_ves = make_bubble(cargo_chips, center=[-4.4, 0.55, 0.0], radius=0.58, outline=BLUE, halo=GREEN)
        cargo_lab = T("cargo", 28, TEXT).next_to(route_ves, UP, buff=0.18)
        self.play(FadeIn(route_ves, cargo_lab), run_time=0.4)
        self.play(
            FadeOut(cargo_lab, run_time=0.35),
            route_ves.animate.move_to(Z_LYSO_CENTER + LEFT * (Z_LYSO_R - 0.1)),
            run_time=0.95,
        )
        cargo_in = route_ves.cargo.copy()
        shell_fade = route_ves.shell.copy()
        halo_fade = route_ves[1].copy()
        self.remove(route_ves)
        self.add(shell_fade, halo_fade, cargo_in)
        self.play(
            FadeOut(shell_fade, halo_fade, scale=1.3, run_time=0.35),
            cargo_in.animate.move_to(Z_LYSO_CENTER),
            run_time=0.55,
        )
        p_dots = VGroup(*[
            Dot(Z_LYSO_CENTER + np.array([rng.uniform(-0.55, 0.55), rng.uniform(-0.45, 0.45), 0.0]),
                radius=0.055, color=PURPLE)
            for _ in range(12)
        ])
        self.play(FadeOut(cargo_in, run_time=0.25), FadeIn(p_dots, run_time=0.3))

        self.at("Two locks")
        self.play(
            FadeOut(p_dots, run_time=0.45),
            lock_acid.animate.scale(1.12),
            lock_mem.animate.scale(1.12),
            run_time=0.55,
            rate_func=there_and_back,
        )
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        z_lyso = make_zoomed_lyso(Z_LYSO_CENTER, Z_LYSO_R, jaw_speed=0, stroke_w=11.0)
        lock_acid_z = chip("lock: acid", PINK, size=30)
        lock_mem_z = chip("lock: membrane", BLUE, size=30)
        VGroup(lock_acid_z, lock_mem_z).arrange(RIGHT, buff=0.30).move_to([Z_LYSO_CENTER[0], 3.38, 0.0])
        self.add(z_lyso, lock_acid_z, lock_mem_z)

        world = make_cell_world(include_labels=True, include_barrel=True, jaw_speed=5.0)
        lock_acid = chip("lock: acid", PINK, size=24, pad=0.14).move_to([LYSO_CENTER[0], -0.04, 0.0])
        lock_mem = chip("lock: membrane", BLUE, size=24, pad=0.14).move_to([LYSO_CENTER[0], 0.72, 0.0])

        self.play(
            Transform(z_lyso.wall, world.lyso.wall, run_time=0.95),
            Transform(z_lyso.jaws, world.lyso.jaws, run_time=0.95),
            Transform(lock_acid_z, lock_acid, run_time=0.95),
            Transform(lock_mem_z, lock_mem, run_time=0.95),
            FadeIn(world.cell_wall, world.er, world.er_lab,
                   world.golgi, world.golgi_lab, world.lyso_lab,
                   world.barrel, world.bar_lab, run_time=0.9),
        )
        self.remove(z_lyso, lock_acid_z, lock_mem_z)
        self.add(world.lyso, lock_acid, lock_mem)

        self.at("build proteins")
        blob = make_orange_blob(ER_CENTER, scale=0.95)
        self.play(GrowFromCenter(blob), run_time=0.55)

        self.at("digest them")
        self.play(world.lyso.jaws.animate.scale(1.18), run_time=0.45, rate_func=there_and_back)

        self.at("rides sealed rooms")
        ves = make_bubble(make_orange_blob(ER_CENTER + RIGHT * 1.15, scale=0.82),
                          center=ER_CENTER + RIGHT * 1.15, radius=0.38)
        self.play(FadeOut(blob, run_time=0.2), FadeIn(ves, run_time=0.3))
        world.barrel.clear_updaters()
        self.play(
            ves.animate.move_to(GOLGI_CENTER + UP * 0.45),
            world.barrel.animate.move_to([-2.4, -0.75, 0.0]),
            run_time=1.0,
        )
        wall_x = CELL_CENTER[0] + CELL_W / 2
        self.play(
            ves.animate.move_to([0.4, 1.45, 0.0]),
            run_time=0.6,
        )
        self.play(
            ves.animate.move_to([wall_x - 0.44, 1.45, 0.0]),
            world.barrel.animate.move_to(BARREL_CENTER),
            run_time=1.0,
        )
        add_barrel_drift(world.barrel, BARREL_CENTER)
        released = ves.cargo.copy()
        shell_fade = ves.shell.copy()
        self.remove(ves)
        self.add(shell_fade, released)
        self.play(
            FadeOut(shell_fade, scale=1.3, run_time=0.35),
            released.animate.move_to([wall_x + 0.85, 1.45, 0.0]),
            run_time=0.65,
        )

        self.at("behind membrane and acid")
        self.play(
            lock_acid.animate.scale(1.12),
            lock_mem.animate.scale(1.12),
            run_time=0.6,
            rate_func=there_and_back,
        )

        self.at("where each job can happen")
        self.play(world.er.ribbons.animate.set_stroke(width=8.0), run_time=0.45, rate_func=there_and_back)
        self.play(world.golgi.animate.set_stroke(width=8.0), run_time=0.45, rate_func=there_and_back)
        self.play(world.lyso.wall.animate.set_stroke(width=9.0), run_time=0.45, rate_func=there_and_back)
        self.finish()


class S12End(EndCard):
    LINE = "Sealed rooms keep their own enzymes and conditions, so jobs stay apart."
