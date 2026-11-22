"""
The Mitochondrial Gate: BCL-2 and Cytochrome c
Film 2 of "Death Receptors, BCL-2 and Caspases"

COLOUR MAP (one colour per concept, carried across the entire film):
- #94A3B8 (CELL_COL)       : Plasma membrane and nuclear envelope outlines
- #14B8A6 (MITO_TEAL)      : Outer and inner mitochondrial membranes (the gate)
- #A855F7 (FAS_VIOLET)     : Fas death receptor (surface DISC, Film 1 continuity)
- #22D3EE (FADD_CYAN)      : FADD adaptor (surface DISC, Film 1 continuity)
- #818CF8 (APAF_INDIGO)    : APAF-1 and the 7-spoke apoptosome wheel
- #FACC15 (CYTC_GOLD)      : Cytochrome c (inner-membrane carrier / released death signal)
- #34D399 (DATP_MINT)      : dATP nucleotide cofactor
- #FB923C (EFFECTOR_CORAL) : Effectors (BAX, BAK) that open outer-membrane pores
- #3B82F6 (GUARD_BLUE)     : Guards (BCL-2) with BH3-binding surface groove
- #F59E0B (SENSOR_AMBER)   : Sensors (BH3-only proteins, including BID)
- #FB7185 (PRO9_ROSE)      : Procaspase-9 chains
- #EF4444 (ACTIVE_RED)     : Active initiator caspases (caspase-8, paired caspase-9)
- #FDBA74 (EXEC_DIMER)     : Inactive executioner caspase dimers
- #F97316 (EXEC_CUT)       : Active cleaved executioner cutters
- #E8EAF0 (TEXT)           : Primary labels and titles

CARRIED WORLD:
A cross-section of the same schematic cell from Film 1 (upper plasma membrane with the
surface DISC, nucleus corner, and the teal mitochondrion whose outer membrane separates
the cytosol from the intermembrane space where cytochrome c shuttles along cristae).
Scenes zoom into the outer mitochondrial membrane and back out to the whole cell.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_link_hook      : Highlight shifts from the upper DISC to a DNA-damage break in the
                       nucleus, then camera zooms smoothly onto the mitochondrion while
                       two compartment zones ('Cytosol' and 'Intermembrane space') light up
                       (computed zoom interpolation + Cytochrome c orbits inside).
- s02_two_rooms      : Folded APAF-1 units drift along deterministic sinusoidal paths in
                       the cytosol while Cytochrome c spheres shuttle along the inner
                       membrane curve; a Cytochrome c probes the solid teal barrier and is
                       turned back, then nudges toward an exit preview.
- s03_three_classes  : Outer membrane gate highlights, coral effector briefly opens and
                       closes a membrane gap, royal-blue guard slides in and clamps the
                       effector in its U-groove, and an amber BH3 sensor wedge glides down
                       to seat inside an open guard groove.
- s04_predict_q      : An amber sensor demonstrates the double-negative release of a
                       clamped effector and direct effector touch, then resets to 5 guards
                       (2 clamped, 3 spare) as 2 amber sensors drift toward the 3 spare
                       grooves and the predict question settles in the bottom band.
- s06_predict_reveal : The 2 sensors snap into 2 of the 3 spare guards while the membrane
                       stays sealed; then a 5-sensor wave fills all guards, displacing
                       BAX/BAK effectors that dive into the membrane and split it open into
                       two coral-lined pores.
- s07_apoptosome     : Cytochrome c spheres stream out of the coral pores, bind mint dATP
                       and 7 folded APAF-1 units that unfold radially by angle k*TAU/7 into
                       the rotating 7-spoke apoptosome wheel; procaspase-9 chains gather
                       and pair at the hub, flare red, and cleave executioner dimers into
                       active cutters.
- s08_crosstalk      : Full-cell view: red caspase-8 from the upper DISC clips an amber
                       BID block; cut BID travels along a computed Bezier trajectory to the
                       mitochondrion to trigger BAX/BAK pores and cytochrome c release.
- s09_closing_rule   : A computed balance beam overlays the outer membrane; its tilt angle
                       updates from the net weight of blue Guards vs. coral Effectors +
                       amber Sensors piling on until the scale tips, opening the pores,
                       assembling the wheel, and starting irreversible cutting.
"""
import numpy as np
from bp_parts import *

# ------------------------------------------------------------------ COLOUR MAP
CELL_COL = "#94A3B8"
MITO_TEAL = "#14B8A6"
FAS_VIOLET = "#A855F7"
FADD_CYAN = "#22D3EE"
APAF_INDIGO = "#818CF8"
CYTC_GOLD = "#FACC15"
DATP_MINT = "#34D399"
EFFECTOR_CORAL = "#FB923C"
GUARD_BLUE = "#3B82F6"
SENSOR_AMBER = "#F59E0B"
PRO9_ROSE = "#FB7185"
ACTIVE_RED = "#EF4444"
EXEC_DIMER = "#FDBA74"
EXEC_CUT = "#F97316"

RNG = np.random.default_rng(7)


# ------------------------------------------------------------------ SHARED GEOMETRY BUILDERS
def _outer_membrane_y(x, base_y=-0.35, curve=0.22):
    return base_y + curve * (1.0 - (x / 6.3) ** 2)


def _inner_cristae_pts(y_base=-2.55, amp=0.55, x0=-6.15, x1=6.15, n=180):
    xs = np.linspace(x0, x1, n)
    folds = (
        np.exp(-((xs + 3.4) / 0.55) ** 2)
        + np.exp(-((xs - 0.0) / 0.55) ** 2)
        + np.exp(-((xs - 3.4) / 0.55) ** 2)
    )
    ys = y_base + amp * folds
    return np.column_stack([xs, ys, np.zeros(n)])


def make_membrane_wall(base_y=-0.35, curve=0.22, pore_xs=(), pore_half_w=0.52, x0=-6.35, x1=6.35):
    """Build the curved teal outer mitochondrial membrane, cleanly split around any open pores."""
    pores = sorted(pore_xs)
    spans = []
    cur = x0
    for px in pores:
        if px - pore_half_w > cur + 0.05:
            spans.append((cur, px - pore_half_w))
        cur = max(cur, px + pore_half_w)
    if x1 > cur + 0.05:
        spans.append((cur, x1))

    g = VGroup()
    for a, b in spans:
        xs = np.linspace(a, b, max(12, int((b - a) * 14)))
        top_pts = [np.array([x, _outer_membrane_y(x, base_y + 0.12, curve), 0.0]) for x in xs]
        bot_pts = [np.array([x, _outer_membrane_y(x, base_y - 0.12, curve), 0.0]) for x in xs]
        poly_pts = top_pts + list(reversed(bot_pts))
        band = Polygon(*poly_pts, stroke_width=0, fill_color=MITO_TEAL, fill_opacity=0.45)
        top_ln = VMobject(stroke_color=MITO_TEAL, stroke_width=5.0).set_points_as_corners(top_pts)
        bot_ln = VMobject(stroke_color=MITO_TEAL, stroke_width=4.0).set_points_as_corners(bot_pts)
        g.add(band, top_ln, bot_ln)
    return g


def make_inner_membrane(y_base=-2.55, amp=0.55, floor_y=-3.35):
    pts = _inner_cristae_pts(y_base=y_base, amp=amp)
    curve = VMobject(stroke_color=MITO_TEAL, stroke_width=4.0, stroke_opacity=0.90).set_points_as_corners(pts)
    poly_pts = list(pts) + [np.array([6.15, floor_y, 0.0]), np.array([-6.15, floor_y, 0.0])]
    fill = Polygon(*poly_pts, stroke_width=0, fill_color=MITO_TEAL, fill_opacity=0.22)
    return VGroup(fill, curve), pts


def make_cyt_c(radius=0.20):
    outer = Circle(radius=radius, color=CYTC_GOLD, stroke_width=2.5, fill_color=CYTC_GOLD, fill_opacity=0.92)
    core = Dot(radius=radius * 0.35, color="#FEF9C3").shift(UL * radius * 0.25)
    return VGroup(outer, core)


def attach_shuttle(mob, pts, speed=0.18, phase=0.0, y_off=0.30):
    """Move a Cytochrome c sphere smoothly back and forth along the inner membrane curve."""
    mob._st = phase

    def u(m, dt):
        mob._st += dt * speed
        s = 0.5 - 0.5 * np.cos(mob._st * PI)
        idx_f = s * (len(pts) - 1)
        i0 = int(np.clip(np.floor(idx_f), 0, len(pts) - 2))
        frac = idx_f - i0
        p = pts[i0] * (1 - frac) + pts[i0 + 1] * frac
        m.move_to(p + UP * y_off)

    return mob.add_updater(u)


def make_apaf1(open_frac=0.0, scale=1.0):
    """APAF-1 monomer: folded compact indigo hinge at open_frac=0, extended spoke arm at 1."""
    folded = [
        np.array([-0.28, -0.20, 0.0]),
        np.array([0.24, -0.24, 0.0]),
        np.array([0.30, 0.18, 0.0]),
        np.array([-0.15, 0.24, 0.0]),
    ]
    opened = [
        np.array([0.0, 0.0, 0.0]),
        np.array([0.55, 0.0, 0.0]),
        np.array([1.15, 0.0, 0.0]),
        np.array([1.62, 0.0, 0.0]),
    ]
    pts = [(1 - open_frac) * a + open_frac * b for a, b in zip(folded, opened)]
    arm = VMobject(stroke_color=APAF_INDIGO, stroke_width=9 * scale, fill_opacity=0)
    arm.set_points_as_corners(pts)
    cap_a = Dot(pts[0], radius=0.12 * scale, color=APAF_INDIGO)
    cap_b = Circle(radius=0.15 * scale, stroke_color=APAF_INDIGO, stroke_width=3.5 * scale,
                   fill_color=APAF_INDIGO, fill_opacity=0.45).move_to(pts[-1])
    return VGroup(arm, cap_a, cap_b)


def make_guard(scale=1.0):
    """Royal-blue BCL-2 guard with a clear U-shaped BH3-binding groove at top."""
    pts = [
        (-0.58, 0.46), (-0.23, 0.46), (-0.21, -0.04), (0.21, -0.04),
        (0.23, 0.46), (0.58, 0.46), (0.54, -0.46), (-0.54, -0.46),
    ]
    return Polygon(*[np.array([x * scale, y * scale, 0.0]) for x, y in pts],
                   stroke_color=GUARD_BLUE, stroke_width=4, fill_color=GUARD_BLUE, fill_opacity=0.42)


def make_effector(scale=1.0):
    """Coral-orange BAX/BAK effector shaped to sit in the guard groove or insert in membrane."""
    return RoundedRectangle(corner_radius=0.16 * scale, width=0.40 * scale, height=0.88 * scale,
                            stroke_color=EFFECTOR_CORAL, stroke_width=3, fill_color=EFFECTOR_CORAL, fill_opacity=0.88)


def make_sensor(scale=1.0):
    """Amber BH3-only sensor wedge whose tapered tip matches the guard's U-groove."""
    pts = [
        (-0.35, 0.42), (0.35, 0.42), (0.19, -0.34), (0.0, -0.45), (-0.19, -0.34),
    ]
    return Polygon(*[np.array([x * scale, y * scale, 0.0]) for x, y in pts],
                   stroke_color=SENSOR_AMBER, stroke_width=3, fill_color=SENSOR_AMBER, fill_opacity=0.88)


def make_pore_walls(x, base_y=-0.35, curve=0.22, half_w=0.48):
    """Two coral BAX/BAK pore walls lining an opening in the outer membrane."""
    ym = _outer_membrane_y(x, base_y, curve)
    left = RoundedRectangle(corner_radius=0.10, width=0.26, height=0.78,
                            stroke_color=EFFECTOR_CORAL, stroke_width=3, fill_color=EFFECTOR_CORAL, fill_opacity=0.90)
    right = left.copy()
    left.move_to([x - half_w + 0.08, ym, 0])
    right.move_to([x + half_w - 0.08, ym, 0])
    return VGroup(left, right)


def make_apoptosome(center=ORIGIN, radius=2.05, with_datp=True, with_cytc=True):
    """Seven-spoke indigo APAF-1 apoptosome wheel with Cytochrome c and dATP."""
    c = np.array(center, dtype=float)
    hub = Circle(radius=0.50, stroke_color=APAF_INDIGO, stroke_width=4.5, fill_color=APAF_INDIGO, fill_opacity=0.28).move_to(c)
    spokes = VGroup()
    cytcs = VGroup()
    datps = VGroup()
    for k in range(7):
        ang = PI / 2 + k * TAU / 7
        dir_v = np.array([np.cos(ang), np.sin(ang), 0.0])
        p0 = c + dir_v * 0.50
        p1 = c + dir_v * (radius - 0.22)
        arm = Line(p0, p1, color=APAF_INDIGO, stroke_width=8)
        cradle = Circle(radius=0.17, stroke_color=APAF_INDIGO, stroke_width=3.5,
                        fill_color=APAF_INDIGO, fill_opacity=0.38).move_to(p1)
        spokes.add(arm, cradle)
        if with_cytc:
            cytcs.add(make_cyt_c(0.16).move_to(c + dir_v * radius))
        if with_datp:
            d = Dot(radius=0.10, color=DATP_MINT).move_to(c + dir_v * (0.50 + (radius - 0.72) * 0.45))
            datps.add(d)
    return VGroup(hub, spokes, datps, cytcs)


def make_executioner(cut=False):
    """Executioner dimer: two muted orange blocks linked together, or split active amber-red cutters."""
    col = EXEC_CUT if cut else EXEC_DIMER
    left = RoundedRectangle(corner_radius=0.12, width=0.62, height=0.50,
                            stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=0.84)
    right = left.copy()
    if not cut:
        left.move_to(LEFT * 0.44)
        right.move_to(RIGHT * 0.44)
        linker = Line(LEFT * 0.13, RIGHT * 0.13, color=TEXT, stroke_width=4.5)
        return VGroup(linker, left, right)
    else:
        left.move_to(LEFT * 0.60).rotate(0.16)
        right.move_to(RIGHT * 0.60).rotate(-0.16)
        return VGroup(left, right)


def make_cell_diagram():
    """Schematic cell shared between S01 and S08: plasma membrane, DISC at top-left, nucleus corner, mitochondrion."""
    cell_outer = RoundedRectangle(corner_radius=1.8, width=11.8, height=6.4,
                                  stroke_color=CELL_COL, stroke_width=3.5, fill_color=CELL_COL, fill_opacity=0.04)
    nuc_arc = Arc(radius=2.05, start_angle=0.0, angle=PI / 2, arc_center=[-5.6, -3.0, 0],
                  stroke_color=CELL_COL, stroke_width=3.5)

    # Surface DISC at upper-left plasma membrane
    disc_x = -2.2
    disc_y = 3.05
    fas_receptors = VGroup(*[
        Line([disc_x + dx, disc_y + 0.25, 0], [disc_x + dx, disc_y - 0.35, 0], color=FAS_VIOLET, stroke_width=5)
        for dx in (-0.36, 0.0, 0.36)
    ])
    fadd_adaptors = VGroup(*[
        RoundedRectangle(corner_radius=0.06, width=0.22, height=0.34,
                         stroke_color=FADD_CYAN, stroke_width=2.5, fill_color=FADD_CYAN, fill_opacity=0.60).move_to([disc_x + dx, disc_y - 0.55, 0])
        for dx in (-0.36, 0.0, 0.36)
    ])
    c8_pair = VGroup(*[
        RoundedRectangle(corner_radius=0.06, width=0.20, height=0.40,
                         stroke_color=ACTIVE_RED, stroke_width=2.5, fill_color=ACTIVE_RED, fill_opacity=0.85).move_to([disc_x + dx, disc_y - 0.96, 0])
        for dx in (-0.15, 0.15)
    ])
    disc = VGroup(fas_receptors, fadd_adaptors, c8_pair)

    # Whole mitochondrion (outer shell outline only so interior intermembrane space stays dark & high-contrast;
    # inner membrane cristae has crisp fill inside the matrix)
    mito_outer = Ellipse(width=6.6, height=3.8, stroke_color=MITO_TEAL, stroke_width=5.5,
                         fill_opacity=0.0).move_to([1.5, -0.5, 0])
    inner_pts = []
    for i in range(72):
        th = i * TAU / 72
        rx = 2.35 + 0.36 * np.cos(6 * th)
        ry = 1.15 + 0.24 * np.cos(6 * th)
        inner_pts.append(np.array([1.5 + rx * np.cos(th), -0.5 + ry * np.sin(th), 0.0]))
    inner_pts.append(inner_pts[0].copy())
    mito_inner = VMobject(stroke_color=MITO_TEAL, stroke_width=3.5, stroke_opacity=0.90,
                          fill_color=MITO_TEAL, fill_opacity=0.16).set_points_as_corners(inner_pts)
    mito = VGroup(mito_outer, mito_inner)

    g = VGroup(cell_outer, nuc_arc, disc, mito)
    g.cell_outer = cell_outer
    g.nuc = nuc_arc
    g.disc = disc
    g.mito = mito
    g.mito_outer = mito_outer
    g.mito_inner = mito_inner
    return g


# ------------------------------------------------------------------ SCENE 0: TITLE
class S00Title(TitleCard):
    LESSON = "Death Receptors, BCL-2 and Caspases"
    TITLE = "The Mitochondrial Gate: BCL-2 and Cytochrome c"


# ------------------------------------------------------------------ SCENE 1: LINK & HOOK
class S01LinkHook(SpokenScene):
    def construct(self):
        cell = make_cell_diagram()
        cell.mito_outer.set_stroke(opacity=0.70)
        cell.mito_inner.set_stroke(opacity=0.70)
        cell.nuc.set_stroke(opacity=0.65)
        # Start with the two Caspase-8 blocks separated beneath FADD so "gather" animates them pairing
        c8_pair = cell.disc[2]
        c8_pair[0].shift(LEFT * 0.25)
        c8_pair[1].shift(RIGHT * 0.25)
        disc_lab = T("Surface DISC (Caspase-8)", 28, FAS_VIOLET).move_to([1.15, 2.35, 0])

        # Cytochrome c spheres already orbiting quietly inside the mitochondrion from t=0
        mito_c0 = cell.mito_outer.get_center()
        cytc_dots = VGroup(*[make_cyt_c(0.14) for _ in range(4)])
        for k, d in enumerate(cytc_dots):
            d._ang = k * 1.5
            def orb0(m, dt, c=cell.mito_outer):
                m._ang += dt * 0.55
                ctr = c.get_center()
                rx = c.width * 0.41
                ry = c.height * 0.40
                m.move_to(ctr + np.array([rx * np.cos(m._ang), ry * np.sin(m._ang), 0]))
            d.add_updater(orb0)

        # DNA double strand inside nucleus corner
        dna_pts1 = [np.array([-5.2 + 0.14 * i, -2.55 + 0.12 * np.sin(i * 0.9), 0]) for i in range(11)]
        dna_pts2 = [np.array([-5.2 + 0.14 * i, -2.80 - 0.12 * np.sin(i * 0.9), 0]) for i in range(11)]
        dna = VGroup(
            VMobject(stroke_color=TEXT, stroke_width=3).set_points_as_corners(dna_pts1),
            VMobject(stroke_color=TEXT, stroke_width=3).set_points_as_corners(dna_pts2),
        )
        dmg_lab = T("Damaged DNA", 28, ACTIVE_RED).move_to([-3.95, -0.55, 0])

        self.add(cell, cytc_dots, dna)
        self.at("outside death receptor")
        self.play(FadeIn(disc_lab), run_time=1.0)

        self.at("platform to gather")
        self.play(
            c8_pair[0].animate.shift(RIGHT * 0.25),
            c8_pair[1].animate.shift(LEFT * 0.25),
            run_time=1.3,
        )

        self.at("danger starts")
        cell.disc.set_opacity(0.35)
        break_mark = VGroup(
            Line([-4.55, -2.45, 0], [-4.35, -2.90, 0], color=ACTIVE_RED, stroke_width=5),
            Line([-4.35, -2.45, 0], [-4.55, -2.90, 0], color=ACTIVE_RED, stroke_width=5),
        )
        self.play(
            FadeOut(disc_lab, run_time=0.35),
            FadeIn(break_mark),
            FadeIn(dmg_lab),
            cell.mito_outer.animate.set_stroke(opacity=1.0),
            cell.mito_inner.animate.set_stroke(opacity=1.0),
            run_time=1.2,
        )

        self.at("no outside signal")
        # Fade out damaged DNA callout quickly before zooming onto the mitochondrion
        self.play(FadeOut(break_mark), FadeOut(dmg_lab), run_time=0.35)
        # Fade out outer cell parts cleanly and zoom the mitochondrion to center filling ~68% height
        self.play(
            FadeOut(dna),
            FadeOut(cell.disc), FadeOut(cell.nuc), FadeOut(cell.cell_outer),
            cell.mito.animate.scale(1.42).move_to([0.2, 0.0, 0]),
            run_time=2.25,
        )

        self.at("separate rooms")
        mito_c = cell.mito_outer.get_center()
        cyto_lab = T("Cytosol", 30, TEXT).move_to([-4.6, 2.75, 0])
        ims_lab = T("Intermembrane space", 28, MITO_TEAL).move_to([-2.8, -2.95, 0])
        ims_arr = Arrow(ims_lab.get_top() + UP * 0.08, mito_c + np.array([-2.2, -1.65, 0]),
                        color=MITO_TEAL, stroke_width=3.5, buff=0.05)

        self.play(FadeIn(cyto_lab), FadeIn(ims_lab), GrowArrow(ims_arr), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ SCENE 2: TWO ROOMS
class S02TwoRooms(SpokenScene):
    def construct(self):
        membrane = make_membrane_wall(base_y=-0.15, curve=0.25)
        inner, inner_pts = make_inner_membrane(y_base=-2.55, amp=0.62)

        cyto_zone = T("Cytosol", 28, TEXT).move_to([-5.3, 3.15, 0])
        ims_zone = T("Intermembrane space", 28, MITO_TEAL).move_to([-4.1, -0.90, 0])
        mem_lab = T("Outer mitochondrial membrane", 28, MITO_TEAL).move_to([3.3, 0.45, 0])

        # 5 folded APAF-1 units floating quietly in the cytosol
        apaf_anchors = [
            np.array([-3.8, 1.90, 0]),
            np.array([-1.4, 2.35, 0]),
            np.array([1.1, 2.15, 0]),
            np.array([3.5, 2.35, 0]),
            np.array([4.9, 1.50, 0]),
        ]
        apafs = VGroup(*[make_apaf1(0.0, scale=1.18).move_to(p) for p in apaf_anchors])
        for k, a in enumerate(apafs):
            a._t0 = k * 1.3
            a._base = apaf_anchors[k].copy()
            def drift(m, dt):
                m._t0 += dt
                m.move_to(m._base + np.array([0.22 * np.sin(0.9 * m._t0), 0.14 * np.cos(1.1 * m._t0), 0]))
            a.add_updater(drift)
        apaf_lab = T("APAF-1", 30, APAF_INDIGO).move_to([-1.4, 3.15, 0])

        # 5 golden Cytochrome c spheres shuttling along the inner membrane curve
        cytcs = VGroup(*[make_cyt_c(0.21) for _ in range(5)])
        for k, c in enumerate(cytcs):
            attach_shuttle(c, inner_pts, speed=0.22, phase=k * 0.42, y_off=0.34)
        cytc_lab = T("Cytochrome c", 30, CYTC_GOLD).move_to([3.6, -1.25, 0])

        self.add(membrane, inner, cyto_zone, ims_zone)
        self.at("One part")
        self.play(FadeIn(apafs), FadeIn(apaf_lab), run_time=1.3)

        self.at("Its partner")
        self.play(FadeIn(cytcs), FadeIn(cytc_lab), run_time=1.3)

        self.at("Keeping Cytochrome")
        probe_c = make_cyt_c(0.22).move_to([0.0, -1.45, 0])
        self.play(FadeIn(mem_lab), FadeIn(probe_c), run_time=0.8)
        self.play(probe_c.animate.move_to([0.0, -0.30, 0]), run_time=1.1)
        barrier_flash = make_membrane_wall(base_y=-0.15, curve=0.25).set_stroke(TEXT, width=6)
        self.play(FadeIn(barrier_flash, run_time=0.25), probe_c.animate.move_to([0.0, -1.30, 0]), run_time=1.2)
        self.play(FadeOut(barrier_flash), run_time=0.5)

        self.at("escaping that room")
        esc_arrow = Arrow([0.0, -1.05, 0], [0.0, 1.05, 0], color=CYTC_GOLD, stroke_width=5, buff=0)
        esc_lab = T("Death signal", 28, CYTC_GOLD).move_to([1.55, 1.05, 0])
        self.play(GrowArrow(esc_arrow), FadeIn(esc_lab), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ SCENE 3: THREE CLASSES
class S03ThreeClasses(SpokenScene):
    def construct(self):
        membrane = make_membrane_wall(base_y=-0.45, curve=0.20)
        inner, inner_pts = make_inner_membrane(y_base=-2.65, amp=0.58)
        cytcs = VGroup(*[make_cyt_c(0.20) for _ in range(5)])
        for k, c in enumerate(cytcs):
            attach_shuttle(c, inner_pts, speed=0.22, phase=k * 0.4, y_off=0.30)

        title = T("BCL-2 family (three classes)", 30, TEXT).move_to([-2.8, 3.2, 0])
        gate_lab = T("Outer membrane gate", 28, MITO_TEAL).move_to([3.5, 0.35, 0])
        tag = scope_tag("schematic")

        self.add(membrane, inner, cytcs, tag)
        self.at("protein family")
        self.play(FadeIn(title), run_time=0.9)

        self.at("controls that outer")
        # Highlight outer membrane as the controlled gate
        mem_hi = make_membrane_wall(base_y=-0.45, curve=0.20).set_stroke(TEXT, width=6)
        self.play(FadeIn(gate_lab), FadeIn(mem_hi, run_time=0.5), run_time=1.0)
        self.play(FadeOut(mem_hi), run_time=0.8)

        # Class 1: Effectors (BAX, BAK) on left
        eff_x = -3.8
        eff = make_effector(scale=1.18).move_to([eff_x, 0.85, 0])
        eff_lab = T("Effectors (BAX, BAK)", 28, EFFECTOR_CORAL).move_to([eff_x, 2.25, 0])

        self.at("Effectors called")
        self.play(FadeOut(gate_lab, run_time=0.4), FadeIn(eff), FadeIn(eff_lab), run_time=0.9)

        self.at("open pores")
        split_mem = make_membrane_wall(base_y=-0.45, curve=0.20, pore_xs=[eff_x], pore_half_w=0.44)
        pore = make_pore_walls(eff_x, base_y=-0.45, curve=0.20, half_w=0.42)
        self.play(
            FadeOut(membrane, run_time=0.3),
            FadeIn(split_mem, run_time=0.3),
            ReplacementTransform(eff, pore),
            run_time=1.0,
        )
        eff2 = make_effector(scale=1.18).move_to([eff_x, 0.60, 0])
        mem2 = make_membrane_wall(base_y=-0.45, curve=0.20)
        self.play(
            FadeOut(split_mem, run_time=0.3),
            FadeIn(mem2, run_time=0.3),
            ReplacementTransform(pore, eff2),
            run_time=0.9,
        )

        # Class 2: Guards (BCL-2) slide in to clamp Effector in groove
        self.at("Guards like")
        guard1 = make_guard(scale=1.20).move_to([-0.2, 0.35, 0])
        guard_lab = T("Guards (BCL-2)", 28, GUARD_BLUE).move_to([0.0, 2.55, 0])
        self.play(FadeIn(guard1), FadeIn(guard_lab), run_time=0.9)

        self.at("gripping them")
        self.play(
            guard1.animate.move_to([eff_x, 0.32, 0]),
            eff2.animate.move_to([eff_x, 0.66, 0]),
            run_time=1.2,
        )
        guard2 = make_guard(scale=1.20).move_to([0.3, 0.32, 0])
        groove_lab = T("Surface groove", 28, GUARD_BLUE).move_to([0.3, -1.05, 0])
        self.play(
            FadeIn(guard2),
            guard_lab.animate.move_to([0.3, 2.55, 0]),
            FadeIn(groove_lab),
            run_time=0.9,
        )

        # Class 3: Sensors (BH3-only) wedge approaching from cytosol on right, matching groove
        self.at("Sensors share")
        sensor = make_sensor(scale=1.15).move_to([4.0, 1.50, 0])
        sensor_lab = T("Sensors (BH3-only)", 28, SENSOR_AMBER).move_to([4.0, 2.55, 0])
        self.play(FadeIn(sensor), FadeIn(sensor_lab), run_time=1.0)

        self.at("fits that groove")
        # Sensor glides horizontally over the groove, then drops vertically into guard2's U-groove
        self.play(sensor.animate.move_to([0.3, 1.50, 0]), run_time=0.75)
        self.play(sensor.animate.move_to([0.3, 0.72, 0]), run_time=0.55)
        self.finish()


# ------------------------------------------------------------------ SHARED BUILDER FOR S04 / S05 / S06
def build_threshold_stage(open_pores=False, show_spare_label=True):
    """Build the 5-guard outer-membrane stage carried identically across S04 -> S05 -> S06.
    Bottom band (y < -2.45) stays completely clean dark BG for the predict question & answer."""
    gx = [-4.6, -2.3, 0.0, 2.3, 4.6]
    base_y, curve = -0.35, 0.18
    pore_xs = (gx[0], gx[1]) if open_pores else ()
    membrane = make_membrane_wall(base_y=base_y, curve=curve, pore_xs=pore_xs, pore_half_w=0.46)
    inner, inner_pts = make_inner_membrane(y_base=-1.95, amp=0.32, floor_y=-2.35)
    cytcs = VGroup(*[make_cyt_c(0.17) for _ in range(5)])
    for k, c in enumerate(cytcs):
        attach_shuttle(c, inner_pts, speed=0.20, phase=k * 0.42, y_off=0.25)

    guards = VGroup()
    effectors = VGroup()
    for i, x in enumerate(gx):
        gy = _outer_membrane_y(x, base_y + 0.56, curve)
        g = make_guard(scale=1.05).move_to([x, gy, 0])
        guards.add(g)
        if i < 2 and not open_pores:
            e = make_effector(scale=0.98).move_to([x, gy + 0.34, 0])
            effectors.add(e)

    stage = VGroup(membrane, inner, cytcs, guards, effectors)
    stage.gx = gx
    stage.base_y = base_y
    stage.curve = curve
    stage.guards = guards
    stage.effectors = effectors
    stage.membrane = membrane
    stage.cytcs = cytcs
    stage.inner_pts = inner_pts
    if show_spare_label:
        spare_lab = T("Spare guards", 28, GUARD_BLUE).move_to([4.4, 2.05, 0])
        stage.spare_lab = spare_lab
        stage.add(spare_lab)
    return stage


def _top_scope_tag(text="schematic"):
    t = T(text, 24, TEXT)
    return t.move_to([5.6, 3.25, 0])


# ------------------------------------------------------------------ SCENE 4: PREDICT QUESTION
class S04PredictQ(SpokenScene):
    def construct(self):
        stage = build_threshold_stage(show_spare_label=False)
        eff_lab = T("BAX / BAK", 28, EFFECTOR_CORAL).move_to([-4.45, 2.35, 0])
        guard_lab = T("Guards", 28, GUARD_BLUE).move_to([2.3, 1.62, 0])
        tag = _top_scope_tag("schematic")

        self.add(stage, eff_lab, guard_lab, tag)
        self.at("blocking the guards")
        demo_s = make_sensor(scale=0.98).move_to([stage.gx[1], 2.35, 0])
        demo_lab = T("Sensor blocks guard", 28, SENSOR_AMBER).move_to([stage.gx[1], 3.15, 0])
        self.play(FadeIn(demo_s), FadeIn(demo_lab), run_time=0.8)
        gy1 = stage.guards[1].get_center()[1]
        self.play(
            demo_s.animate.move_to([stage.gx[1], gy1 + 0.36, 0]),
            stage.effectors[1].animate.move_to([stage.gx[1] + 0.78, gy1 + 1.25, 0]),
            run_time=1.3,
        )

        self.at("activate")
        direct_s = make_sensor(scale=0.98).move_to([stage.gx[1] + 1.85, gy1 + 1.25, 0])
        direct_lab = T("Sensor activates BAX / BAK", 28, SENSOR_AMBER).move_to([stage.gx[1] + 0.3, 3.15, 0])
        self.play(
            FadeIn(direct_s, run_time=0.4),
            direct_s.animate.move_to([stage.gx[1] + 1.38, gy1 + 1.25, 0]),
            swap(demo_lab, direct_lab, run_time=0.6),
            run_time=1.0,
        )

        self.at("mild stress")
        # Clear demo cleanly BEFORE introducing Spare guards and Few sensors
        self.play(
            FadeOut(demo_s), FadeOut(direct_lab), FadeOut(direct_s), FadeOut(guard_lab),
            stage.effectors[1].animate.move_to([stage.gx[1], gy1 + 0.34, 0]),
            run_time=0.8,
        )
        spare_lab = T("Spare guards", 28, GUARD_BLUE).move_to([4.4, 2.05, 0])
        two_sensors = VGroup(
            make_sensor(scale=0.98).move_to([stage.gx[2], 2.55, 0]),
            make_sensor(scale=0.98).move_to([stage.gx[3], 2.55, 0]),
        )
        sens_lab = T("Few sensors", 28, SENSOR_AMBER).move_to([1.15, 3.22, 0])
        self.play(FadeIn(spare_lab), FadeIn(two_sensors), FadeIn(sens_lab), run_time=0.9)
        self.play(two_sensors.animate.shift(DOWN * 0.25), run_time=1.3)

        self.at("Pause and predict")
        q = question_card("Fewer sensors than spare guards: does the membrane open yet?", y=-3.05)
        self.play(FadeIn(q), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ SCENE 5: PREDICT PAUSE (4.5s)
class S05Pause(PredictPause):
    QUESTION = "Fewer sensors than spare guards: does the membrane open yet?"
    CARD = {"y": -3.05}
    RING_AT = (6.0, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        stage = build_threshold_stage(show_spare_label=True)
        eff_lab = T("BAX / BAK", 28, EFFECTOR_CORAL).move_to([-4.45, 2.35, 0])
        two_sensors = VGroup(
            make_sensor(scale=0.98).move_to([stage.gx[2], 2.30, 0]),
            make_sensor(scale=0.98).move_to([stage.gx[3], 2.30, 0]),
        )
        bob(two_sensors[0], amp=0.06, speed=2.2, seed=0)
        bob(two_sensors[1], amp=0.06, speed=2.2, seed=1.5)
        sens_lab = T("Few sensors", 28, SENSOR_AMBER).move_to([1.15, 3.22, 0])
        return VGroup(stage, eff_lab, two_sensors, sens_lab, _top_scope_tag("schematic"))


# ------------------------------------------------------------------ SCENE 6: PREDICT REVEAL
class S06PredictReveal(SpokenScene):
    def construct(self):
        stage = build_threshold_stage(show_spare_label=True)
        eff_lab = T("BAX / BAK", 28, EFFECTOR_CORAL).move_to([-4.45, 2.35, 0])
        two_sensors = VGroup(
            make_sensor(scale=0.98).move_to([stage.gx[2], 2.30, 0]),
            make_sensor(scale=0.98).move_to([stage.gx[3], 2.30, 0]),
        )
        sens_lab = T("Few sensors", 28, SENSOR_AMBER).move_to([1.15, 3.22, 0])
        q = question_card("Fewer sensors than spare guards: does the membrane open yet?", y=-3.05)
        tag = _top_scope_tag("schematic")
        self.add(stage, eff_lab, two_sensors, sens_lab, q, tag)

        self.at("Not yet")
        ans = T("Not yet — membrane stays sealed", 30, GUARD_BLUE).move_to([-0.5, -3.05, 0])
        self.play(swap(q, ans, run_time=0.8))

        self.at("spare guards soak")
        gy2 = stage.guards[2].get_center()[1]
        gy3 = stage.guards[3].get_center()[1]
        self.play(
            two_sensors[0].animate.move_to([stage.gx[2], gy2 + 0.36, 0]),
            two_sensors[1].animate.move_to([stage.gx[3], gy3 + 0.36, 0]),
            run_time=1.3,
        )

        self.at("stay clamped")
        lock_rings = VGroup(*[
            SurroundingRectangle(VGroup(stage.guards[i], stage.effectors[i]), color=GUARD_BLUE, buff=0.08, corner_radius=0.14)
            for i in range(2)
        ])
        self.play(Create(lock_rings), run_time=0.9)
        self.play(FadeOut(lock_rings), run_time=0.7)

        self.at("sustained stress")
        # Clear Few sensors, Spare guards, BAX / BAK & bottom answer cleanly before wave enters
        self.play(FadeOut(sens_lab), FadeOut(ans), FadeOut(stage.spare_lab), FadeOut(eff_lab), run_time=0.45)
        wave = VGroup(*[
            make_sensor(scale=0.98).move_to([stage.gx[i], 2.25, 0])
            for i in (0, 1, 4)
        ] + [
            make_sensor(scale=0.98).move_to([x, 2.35, 0])
            for x in (-1.15, 1.15)
        ])
        wave_lab = T("Sustained stress: sensors fill guards", 28, SENSOR_AMBER).move_to([-0.6, 3.22, 0])
        self.play(FadeIn(wave), FadeIn(wave_lab), run_time=0.8)

        self.at("fill the guards")
        gy0 = stage.guards[0].get_center()[1]
        gy1 = stage.guards[1].get_center()[1]
        gy4 = stage.guards[4].get_center()[1]
        self.play(
            wave[0].animate.move_to([stage.gx[0], gy0 + 0.36, 0]),
            wave[1].animate.move_to([stage.gx[1], gy1 + 0.36, 0]),
            wave[2].animate.move_to([stage.gx[4], gy4 + 0.36, 0]),
            wave[3].animate.move_to([-1.15, 1.85, 0]),
            wave[4].animate.move_to([1.15, 1.85, 0]),
            stage.effectors[0].animate.move_to([stage.gx[0], 1.75, 0]),
            stage.effectors[1].animate.move_to([stage.gx[1], 1.75, 0]),
            run_time=1.3,
        )

        self.at("assemble into pores")
        px0, px1 = -5.25, -2.75
        open_mem = make_membrane_wall(base_y=stage.base_y, curve=stage.curve, pore_xs=[px0, px1], pore_half_w=0.40)
        pores = VGroup(
            make_pore_walls(px0, base_y=stage.base_y, curve=stage.curve, half_w=0.38),
            make_pore_walls(px1, base_y=stage.base_y, curve=stage.curve, half_w=0.38),
        )
        self.play(
            stage.guards[0].animate.shift(RIGHT * 0.60),
            wave[0].animate.shift(RIGHT * 0.60),
            stage.guards[1].animate.shift(RIGHT * 0.82),
            wave[1].animate.shift(RIGHT * 0.82),
            FadeOut(stage.membrane, run_time=0.3),
            FadeIn(open_mem, run_time=0.3),
            ReplacementTransform(stage.effectors, pores),
            run_time=1.3,
        )
        pore_lab = T("BAX / BAK pores", 28, EFFECTOR_CORAL).move_to([-4.0, 1.65, 0])
        self.play(FadeIn(pore_lab), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ SCENE 7: APOPTOSOME
class S07Apoptosome(SpokenScene):
    def construct(self):
        px0, px1 = -4.2, -1.6
        open_mem = make_membrane_wall(base_y=-2.55, curve=0.14, pore_xs=[px0, px1], pore_half_w=0.48)
        pores = VGroup(
            make_pore_walls(px0, base_y=-2.55, curve=0.14, half_w=0.46),
            make_pore_walls(px1, base_y=-2.55, curve=0.14, half_w=0.46),
        )
        pore_lab = T("BAX / BAK pores", 26, EFFECTOR_CORAL).move_to([0.7, -1.95, 0])
        tag = scope_tag("schematic")

        # Carry folded APAF-1 units already present in cytosol so opening frames are populated
        wheel_c = np.array([-2.2, 0.55, 0.0])
        wheel_r = 2.00
        folded_apafs = VGroup()
        for k in range(7):
            ang = PI / 2 + k * TAU / 7
            dir_v = np.array([np.cos(ang), np.sin(ang), 0.0])
            folded_apafs.add(make_apaf1(0.0, scale=1.0).move_to(wheel_c + dir_v * 1.55))

        stream_c = VGroup(*[make_cyt_c(0.17).move_to([px0 if i % 2 == 0 else px1, -3.15, 0]) for i in range(7)])
        self.add(open_mem, pores, pore_lab, folded_apafs, stream_c, tag)

        self.at("cytochrome c pours")
        targets = [wheel_c + wheel_r * np.array([np.cos(PI / 2 + k * TAU / 7), np.sin(PI / 2 + k * TAU / 7), 0]) for k in range(7)]
        self.play(
            FadeOut(pore_lab, run_time=0.4),
            *[stream_c[k].animate.move_to(targets[k]) for k in range(7)],
            run_time=2.2,
        )

        self.at("nucleotide datp")
        datps = VGroup()
        for k in range(7):
            ang = PI / 2 + k * TAU / 7
            dir_v = np.array([np.cos(ang), np.sin(ang), 0.0])
            datps.add(Dot(radius=0.10, color=DATP_MINT).move_to(wheel_c + dir_v * 1.15))
        datp_lab = T("dATP", 28, DATP_MINT).move_to([0.75, 2.25, 0])
        self.play(FadeIn(datps), FadeIn(datp_lab), run_time=1.2)

        self.at("seven copies")
        wheel = make_apoptosome(center=wheel_c, radius=wheel_r)
        self.play(
            ReplacementTransform(folded_apafs, wheel[1]),
            FadeIn(wheel[0]),
            ReplacementTransform(datps, wheel[2]),
            ReplacementTransform(stream_c, wheel[3]),
            run_time=2.3,
        )

        self.at("the apoptosome")
        apop_lab = T("Apoptosome (7-spoke wheel)", 30, APAF_INDIGO).move_to([-2.2, 3.12, 0])
        # Continuous slow wheel rotation while apoptosome label lands -> eliminates any static freeze!
        self.play(
            FadeIn(apop_lab),
            FadeOut(datp_lab, run_time=0.4),
            Rotate(wheel, angle=3 * TAU / 14, about_point=wheel_c, rate_func=linear),
            run_time=3.2,
        )

        self.at("its hub gathers")
        pro9 = VGroup(
            RoundedRectangle(corner_radius=0.08, width=0.24, height=0.56, stroke_color=PRO9_ROSE, stroke_width=2.5,
                             fill_color=PRO9_ROSE, fill_opacity=0.85).move_to([1.1, 0.9, 0]),
            RoundedRectangle(corner_radius=0.08, width=0.24, height=0.56, stroke_color=PRO9_ROSE, stroke_width=2.5,
                             fill_color=PRO9_ROSE, fill_opacity=0.85).move_to([1.1, 0.1, 0]),
        )
        pro9_lab = T("Procaspase-9", 28, PRO9_ROSE).move_to([2.65, 1.55, 0])
        self.play(FadeIn(pro9), FadeIn(pro9_lab), run_time=0.7)
        self.play(
            pro9[0].animate.move_to(wheel_c + LEFT * 0.15),
            pro9[1].animate.move_to(wheel_c + RIGHT * 0.15),
            run_time=1.0,
        )

        self.at("paired copies")
        c9_lab = T("Active Caspase-9", 28, ACTIVE_RED).move_to([2.65, 1.55, 0])
        self.play(
            pro9.animate.set_color(ACTIVE_RED),
            swap(pro9_lab, c9_lab, run_time=0.5),
            run_time=0.7,
        )

        self.at("cut and unlock")
        ex1 = make_executioner(cut=False).move_to([3.6, 0.15, 0])
        ex2 = make_executioner(cut=False).move_to([3.6, -0.85, 0])
        ex_lab = T("Executioners", 28, EXEC_DIMER).move_to([3.6, -1.75, 0])
        self.play(FadeIn(ex1), FadeIn(ex2), FadeIn(ex_lab), run_time=0.5)
        cut_ray = Arrow(wheel_c + RIGHT * 0.50, [2.7, -0.25, 0], color=ACTIVE_RED, stroke_width=4, buff=0.05)
        ex1_cut = make_executioner(cut=True).move_to([3.6, 0.15, 0])
        ex2_cut = make_executioner(cut=True).move_to([3.6, -0.85, 0])
        ex_act_lab = T("Active cutters", 28, EXEC_CUT).move_to([3.6, -1.75, 0])
        self.play(
            GrowArrow(cut_ray, run_time=0.4),
            ReplacementTransform(ex1, ex1_cut),
            ReplacementTransform(ex2, ex2_cut),
            swap(ex_lab, ex_act_lab, run_time=0.5),
            run_time=1.1,
        )
        self.finish()


# ------------------------------------------------------------------ SCENE 8: CROSSTALK
class S08Crosstalk(SpokenScene):
    def construct(self):
        cell = make_cell_diagram()
        mito_c = cell.mito_outer.get_center()
        guard = make_guard(scale=0.88).move_to(mito_c + np.array([-2.2, 1.45, 0])).rotate(0.45)
        eff = make_effector(scale=0.88).move_to(mito_c + np.array([-1.30, 1.65, 0])).rotate(0.15)
        cytcs = VGroup(*[
            make_cyt_c(0.15).move_to(mito_c + np.array([1.8 * np.cos(k * 1.4), 0.9 * np.sin(k * 1.4), 0]))
            for k in range(5)
        ])
        for k, c in enumerate(cytcs):
            c._ang = k * 1.4
            def orb(m, dt, ctr=mito_c):
                m._ang += dt * 0.50
                m.move_to(ctr + np.array([2.0 * np.cos(m._ang), 1.0 * np.sin(m._ang), 0]))
            c.add_updater(orb)

        disc_lab = T("Surface DISC", 28, FAS_VIOLET).move_to([-4.2, 2.35, 0])
        mito_lab = T("Mitochondrial gate", 28, MITO_TEAL).move_to([1.5, -2.80, 0])
        tag = scope_tag("schematic")
        self.add(cell, guard, eff, cytcs, disc_lab, mito_lab, tag)

        self.at("from the surface platform")
        c8_lab = T("Caspase-8", 28, ACTIVE_RED).move_to([-0.55, 2.55, 0])
        bid_cap = RoundedRectangle(corner_radius=0.08, width=0.32, height=0.36,
                                   stroke_color=CELL_COL, stroke_width=2.5, fill_color=CELL_COL, fill_opacity=0.45).move_to([-2.2, 0.72, 0])
        bid_wedge = make_sensor(scale=0.90).move_to([-2.2, 0.25, 0])
        bid = VGroup(bid_cap, bid_wedge)
        bid_lab = T("BID", 28, SENSOR_AMBER).move_to([-3.2, 0.45, 0])
        self.play(cell.disc[2].animate.scale(1.18), FadeIn(c8_lab), FadeIn(bid), FadeIn(bid_lab), run_time=0.9)

        self.at("cut a sensor")
        self.play(cell.disc[2].animate.move_to([-2.2, 0.90, 0]), run_time=0.7)
        cut_lab = T("Cut BID", 28, SENSOR_AMBER).move_to([-3.3, 0.25, 0])
        self.play(
            FadeOut(bid_cap, shift=UP * 0.3),
            swap(bid_lab, cut_lab, run_time=0.5),
            cell.disc[2].animate.scale(1.0 / 1.18).move_to([-2.2, 2.09, 0]),
            run_time=0.8,
        )

        self.at("Cut BID travels")
        path = CubicBezier(
            [-2.2, 0.25, 0],
            [-1.6, 1.35, 0],
            [-0.9, 1.65, 0],
            mito_c + np.array([-2.34, 1.74, 0]),
        )
        start_wedge = bid_wedge.copy()

        def move_and_tilt(m, alpha):
            m.become(start_wedge)
            m.rotate(0.45 * alpha)
            m.move_to(path.point_from_proportion(alpha))

        self.play(
            UpdateFromAlphaFunc(bid_wedge, move_and_tilt),
            FadeOut(cut_lab, run_time=0.4),
            run_time=1.7,
        )

        self.at("helps trigger")
        # Effector opens a visible coral pore gap in cell.mito_outer and Cytochrome c releases clear of all text labels
        th0 = float(np.arccos(-1.00 / 3.3))
        dth = 0.14
        ths = np.linspace(th0 + dth, th0 - dth + TAU, 90)
        open_pts = [mito_c + np.array([3.3 * np.cos(t), 1.9 * np.sin(t), 0.0]) for t in ths]
        open_outer = VMobject(stroke_color=MITO_TEAL, stroke_width=5.5).set_points_as_corners(open_pts)
        pore_walls = VGroup()
        for t in (th0 - 0.10, th0 + 0.10):
            p = mito_c + np.array([3.3 * np.cos(t), 1.9 * np.sin(t), 0.0])
            w = RoundedRectangle(corner_radius=0.08, width=0.20, height=0.50,
                                 stroke_color=EFFECTOR_CORAL, stroke_width=2.5, fill_color=EFFECTOR_CORAL, fill_opacity=0.90)
            w.move_to(p).rotate(0.18)
            pore_walls.add(w)
        self.play(
            FadeOut(cell.mito_outer, run_time=0.25),
            FadeIn(open_outer, run_time=0.25),
            ReplacementTransform(eff, pore_walls),
            run_time=0.8,
        )
        released = VGroup(*[make_cyt_c(0.15).move_to(mito_c + np.array([-1.00, 1.48, 0])) for _ in range(3)])
        rel_targets = [
            mito_c + np.array([-1.50, 2.35, 0]),
            mito_c + np.array([-0.95, 2.55, 0]),
            mito_c + np.array([-0.40, 2.35, 0]),
        ]
        self.play(*[released[k].animate.move_to(rel_targets[k]) for k in range(3)], run_time=1.3)

        self.at("guards sensors and effectors")
        summary = fit_text("Guards, Sensors & Effectors set threshold", max_w=3.8, size=26, color=TEXT).move_to([3.30, 2.15, 0])
        self.play(FadeIn(summary), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ SCENE 9: CLOSING RULE
class S09ClosingRule(SpokenScene):
    def construct(self):
        membrane = make_membrane_wall(base_y=-1.65, curve=0.14)
        inner, inner_pts = make_inner_membrane(y_base=-3.05, amp=0.30)
        cytcs = VGroup(*[make_cyt_c(0.16) for _ in range(5)])
        for k, c in enumerate(cytcs):
            attach_shuttle(c, inner_pts, speed=0.22, phase=k * 0.42, y_off=0.24)

        sensor_n = ValueTracker(0.0)
        pivot = np.array([-1.8, 1.35, 0.0])
        beam_half = 2.40

        def get_angle():
            net = 3.0 - (1.0 + sensor_n.get_value() * 0.7)
            return float(np.clip(net * 0.15, -0.24, 0.24))

        fulcrum = Polygon(
            pivot, pivot + np.array([-0.32, -0.52, 0]), pivot + np.array([0.32, -0.52, 0]),
            stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25,
        )

        def mk_beam():
            ang = get_angle()
            dx, dy = beam_half * np.cos(ang), beam_half * np.sin(ang)
            lp = pivot + np.array([-dx, -dy, 0])
            rp = pivot + np.array([dx, dy, 0])
            beam = Line(lp, rp, color=TEXT, stroke_width=6)
            # Hang pans 1.25 below the beam endpoints with V-shaped cords clear of all weights
            hang_d = 1.25
            l_pan = Line(lp + DOWN * hang_d + LEFT * 0.96, lp + DOWN * hang_d + RIGHT * 0.96, color=GUARD_BLUE, stroke_width=5)
            r_pan = Line(rp + DOWN * hang_d + LEFT * 1.02, rp + DOWN * hang_d + RIGHT * 1.02, color=SENSOR_AMBER, stroke_width=5)
            l_hang = VGroup(
                Line(lp, l_pan.get_start(), color=CELL_COL, stroke_width=3),
                Line(lp, l_pan.get_end(), color=CELL_COL, stroke_width=3),
            )
            r_hang = VGroup(
                Line(rp, r_pan.get_start(), color=CELL_COL, stroke_width=3),
                Line(rp, r_pan.get_end(), color=CELL_COL, stroke_width=3),
            )
            g_blocks = VGroup(*[
                RoundedRectangle(corner_radius=0.06, width=0.36, height=0.36, stroke_color=GUARD_BLUE, stroke_width=2.5,
                                 fill_color=GUARD_BLUE, fill_opacity=0.72).move_to(l_pan.get_center() + UP * 0.22 + RIGHT * (-0.40 + i * 0.40))
                for i in range(3)
            ])
            r_blocks = VGroup(
                RoundedRectangle(corner_radius=0.06, width=0.34, height=0.36, stroke_color=EFFECTOR_CORAL, stroke_width=2.5,
                                 fill_color=EFFECTOR_CORAL, fill_opacity=0.82).move_to(r_pan.get_center() + UP * 0.22 + LEFT * 0.44)
            )
            n_int = int(np.floor(sensor_n.get_value() + 0.05))
            for k in range(n_int):
                if k < 2:
                    pos = r_pan.get_center() + UP * 0.20 + RIGHT * (0.02 + k * 0.42)
                else:
                    pos = r_pan.get_center() + UP * 0.56 + RIGHT * (-0.18 + (k - 2) * 0.36)
                r_blocks.add(make_sensor(scale=0.40).move_to(pos))
            return VGroup(beam, l_hang, r_hang, l_pan, r_pan, g_blocks, r_blocks)

        scale_dyn = always_redraw(mk_beam)
        guards_lab = T("Guards", 28, GUARD_BLUE).move_to([-4.2, 2.85, 0])
        sens_eff_lab = T("Sensors + Effectors", 28, SENSOR_AMBER).move_to([0.7, 2.85, 0])
        tag = scope_tag("schematic")

        self.add(membrane, inner, cytcs, fulcrum, scale_dyn, guards_lab, sens_eff_lab, tag)

        self.at("fill the free guards")
        self.play(sensor_n.animate.set_value(2.0), run_time=1.8)

        self.at("tip the scale")
        self.play(sensor_n.animate.set_value(4.0), run_time=1.2)
        scale_dyn.clear_updaters()
        scale_dyn.become(mk_beam())

        self.at("escapes")
        px = -1.8
        open_mem = make_membrane_wall(base_y=-1.65, curve=0.14, pore_xs=[px], pore_half_w=0.50)
        pore = make_pore_walls(px, base_y=-1.65, curve=0.14, half_w=0.48)
        esc_c = VGroup(*[make_cyt_c(0.16).move_to([px, -2.15, 0]) for _ in range(4)])
        self.play(
            FadeOut(membrane, run_time=0.2),
            FadeIn(open_mem, run_time=0.2),
            FadeIn(pore, run_time=0.25),
            *[esc_c[k].animate.move_to([3.9 + 1.05 * np.cos(k * 1.4), 1.15 + 1.05 * np.sin(k * 1.4), 0]) for k in range(4)],
            run_time=0.85,
        )

        self.at("wheel assembles")
        wheel = make_apoptosome(center=[4.1, 1.15, 0], radius=1.20)
        wheel_lab = T("Apoptosome", 28, APAF_INDIGO).move_to([4.1, 2.85, 0])
        self.play(ReplacementTransform(esc_c, wheel), FadeIn(wheel_lab), run_time=0.80)

        self.at("irreversible cutting")
        cutters = make_executioner(cut=True).move_to([4.1, -0.80, 0])
        cut_lab = T("Irreversible cutting", 28, EXEC_CUT).move_to([1.25, -0.80, 0])
        self.play(FadeIn(cutters), FadeIn(cut_lab), run_time=0.85)

        self.at("family balance decides")
        self.play(Indicate(scale_dyn, scale_factor=1.03, color=CYTC_GOLD), run_time=1.5)
        self.finish()


# ------------------------------------------------------------------ SCENE 10: END CARD
class S10End(EndCard):
    LINE = "The BCL-2 family balance decides whether mitochondria release cytochrome c."
